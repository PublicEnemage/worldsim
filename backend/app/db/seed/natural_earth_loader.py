"""
Natural Earth 110m country boundary loader — ADR-003 Decision 4.

Fetches or reads cached Natural Earth 110m admin-0 countries GeoJSON,
validates territorial positions via TerritorialValidator (hard gate — no
records written if validation fails), and inserts Entity records with
geometry and ten Level 1 attributes into simulation_entities.

Level 1 attributes loaded from Natural Earth 110m properties:
  1.  population_total      — STOCK, persons        (NE: POP_EST)
  2.  gdp_usd_millions      — FLOW, USD millions    (NE: GDP_MD)
  3.  pop_rank              — DIMENSIONLESS          (NE: POP_RANK)
  4.  economy_tier          — DIMENSIONLESS          (NE: ECONOMY)
  5.  income_group          — DIMENSIONLESS          (NE: INCOME_GRP)
  6.  continent             — DIMENSIONLESS          (NE: CONTINENT)
  7.  un_region             — DIMENSIONLESS          (NE: REGION_UN)
  8.  subregion             — DIMENSIONLESS          (NE: SUBREGION)
  9.  map_color_group       — DIMENSIONLESS          (NE: MAPCOLOR7)
  10. ne_scale_rank         — DIMENSIONLESS          (NE: SCALERANK)

NE estimates are confidence_tier=3 (research estimates with documented
methodology). Economic World Bank / IMF data (tier 1) will be loaded by
a separate WDI/WEO loader in a later Milestone 2 task.

Source registration: NE_110M_2024 must be registered in source_registry
before this loader runs. The loader will raise if the source is absent.

Territorial validation is a hard gate: TerritorialValidator.validate_all()
is called on every feature before any INSERT. A single validation failure
halts the entire load and leaves the database unchanged.

POLYGON geometries from Natural Earth are stored as MULTIPOLYGON. Features
with POLYGON geometry are promoted before INSERT.
"""
from __future__ import annotations

import json
import logging
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import TYPE_CHECKING, Any

import httpx

from app.db.territorial_validator import TerritorialValidator
from app.simulation.engine.quantity import VariableType

if TYPE_CHECKING:
    import asyncpg

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Natural Earth source constants
# ---------------------------------------------------------------------------

NE_SOURCE_ID = "NE_110M_2024"
NE_110M_URL = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    "master/geojson/ne_110m_admin_0_countries.geojson"
)
NE_DEFAULT_CACHE_PATH = Path(__file__).parent / "cache" / "ne_110m_admin_0_countries.geojson"

# Confidence tier for NE editorial data (Tier 3 — research estimates).
NE_CONFIDENCE_TIER = 3

# Observation date for NE 2024 data.
NE_OBSERVATION_DATE = date(2024, 1, 1)


# ---------------------------------------------------------------------------
# Attribute definitions — Level 1 attributes from NE 110m properties
# ---------------------------------------------------------------------------

def _build_attributes(props: dict[str, Any]) -> dict[str, Any]:
    """Build the JSONB attribute envelope from Natural Earth feature properties.

    Returns a dict of attribute_key → Quantity-as-dict for the ten Level 1
    attributes. Values are serialised with value as str (Decimal → str) per
    the ADR-003 wire format.

    Attributes that are absent in the source feature are skipped rather than
    gap-filled — the attribute key simply does not appear in the entity's
    attribute store.
    """
    attrs: dict[str, Any] = {}

    def _qty(
        value: Any,  # noqa: ANN401
        unit: str,
        vtype: VariableType,
        *,
        raw_is_float: bool = False,
    ) -> dict[str, Any] | None:
        """Serialise a Quantity to the ADR-003 JSONB envelope format."""
        if value is None or value == "" or value == -99 or value == -99.0:
            return None
        try:
            # Decimal(str(...)) handles both int and float inputs without
            # accumulating the float representation error before conversion.
            decimal_value = Decimal(str(value))
        except Exception:  # noqa: BLE001 — broad catch on type-unsafe NE data
            return None
        return {
            "value": str(decimal_value),
            "unit": unit,
            "variable_type": vtype.value,
            "confidence_tier": NE_CONFIDENCE_TIER,
            "observation_date": NE_OBSERVATION_DATE.isoformat(),
            "source_registry_id": NE_SOURCE_ID,
            "measurement_framework": None,
        }

    # 1. Population total (STOCK — level at a point in time)
    if (pop := _qty(props.get("POP_EST"), "persons", VariableType.STOCK)):
        attrs["population_total"] = pop

    # 2. GDP in USD millions (FLOW — period measure; NE vintage is ~2019)
    if (gdp := _qty(props.get("GDP_MD"), "USD_millions_current", VariableType.FLOW)):
        attrs["gdp_usd_millions"] = gdp

    # 3. Population rank (DIMENSIONLESS — ordinal index)
    if (pr := _qty(props.get("POP_RANK"), "dimensionless", VariableType.DIMENSIONLESS)):
        attrs["pop_rank"] = pr

    # 4. Economy tier — NE 1-7 scale ("1. Developed region: G7", etc.)
    economy_raw = props.get("ECONOMY", "")
    if economy_raw and economy_raw not in ("-99", ""):
        # Store the first character (the tier digit) as a DIMENSIONLESS index.
        tier_str = str(economy_raw).strip()[:1]
        et = tier_str.isdigit() and _qty(int(tier_str), "dimensionless", VariableType.DIMENSIONLESS)
        if et:
            attrs["economy_tier"] = et

    # 5. Income group — NE 1-5 ordinal
    income_raw = props.get("INCOME_GRP", "")
    if income_raw and income_raw not in ("-99", ""):
        tier_str = str(income_raw).strip()[:1]
        ig = tier_str.isdigit() and _qty(int(tier_str), "dimensionless", VariableType.DIMENSIONLESS)
        if ig:
            attrs["income_group"] = ig

    # 6–10: Categorical region descriptors stored as DIMENSIONLESS index 0.
    # These carry the string value in the entity metadata, not the attribute
    # store (which is typed Quantity). Index 0 acts as a presence flag.
    for attr_key, ne_key in (
        ("continent_code",    "CONTINENT"),
        ("un_region_code",    "REGION_UN"),
        ("subregion_code",    "SUBREGION"),
        ("map_color_group",   "MAPCOLOR7"),
        ("ne_scale_rank",     "SCALERANK"),
    ):
        raw = props.get(ne_key)
        if raw is not None and raw not in ("", -99):
            v = _qty(raw, "dimensionless", VariableType.DIMENSIONLESS)  # noqa: SIM102
            if v:
                attrs[attr_key] = v

    return attrs


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def _ensure_multipolygon(geometry: dict[str, Any]) -> dict[str, Any]:
    """Promote POLYGON geometry to MULTIPOLYGON for schema consistency."""
    if geometry.get("type") == "Polygon":
        return {
            "type": "MultiPolygon",
            "coordinates": [geometry["coordinates"]],
        }
    return geometry


def _derive_entity_id(props: dict[str, Any]) -> str | None:
    """Derive the entity_id (ISO alpha-3) from Natural Earth properties.

    Tries ISO_A3 first; falls back to ADM0_A3. Returns None if no valid
    code is found. NE uses '-99' as the sentinel for missing codes.
    """
    for key in ("ISO_A3", "ADM0_A3"):
        code = str(props.get(key, "")).strip()
        if code and code != "-99" and len(code) == 3:  # noqa: PLR2004
            return code
    return None


# ---------------------------------------------------------------------------
# GeoJSON fetch / cache
# ---------------------------------------------------------------------------

async def _fetch_or_load_geojson(cache_path: Path | None) -> dict[str, Any]:
    """Return the NE 110m GeoJSON FeatureCollection.

    Uses the local cache if present; downloads from GitHub otherwise.
    The cache is written on first download so subsequent runs are offline-capable.
    """
    resolved = cache_path or NE_DEFAULT_CACHE_PATH

    if resolved.exists():
        logger.info("Loading Natural Earth 110m from cache: %s", resolved)
        with resolved.open(encoding="utf-8") as fh:
            return json.load(fh)  # type: ignore[no-any-return]

    logger.info("Downloading Natural Earth 110m from %s", NE_110M_URL)
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(NE_110M_URL)
        response.raise_for_status()
        raw = response.text

    resolved.parent.mkdir(parents=True, exist_ok=True)
    with resolved.open("w", encoding="utf-8") as fh:
        fh.write(raw)
    logger.info("Cached Natural Earth 110m to %s", resolved)

    return json.loads(raw)  # type: ignore[no-any-return]


# ---------------------------------------------------------------------------
# Source registry check
# ---------------------------------------------------------------------------

async def _assert_source_registered(conn: asyncpg.Connection) -> None:
    """Raise if NE_110M_2024 is not registered in source_registry."""
    row = await conn.fetchrow(
        "SELECT source_id FROM source_registry WHERE source_id = $1",
        NE_SOURCE_ID,
    )
    if row is None:
        raise RuntimeError(
            f"Source '{NE_SOURCE_ID}' is not registered in source_registry. "
            f"Register it via the SourceRegistration model before running the loader. "
            f"See DATA_STANDARDS.md § Data Provenance Requirements."
        )


# ---------------------------------------------------------------------------
# Main loader entry point
# ---------------------------------------------------------------------------

async def load_natural_earth_boundaries(
    conn: asyncpg.Connection,
    *,
    cache_path: Path | None = None,
    skip_source_check: bool = False,
) -> int:
    """Load Natural Earth 110m country boundaries into simulation_entities.

    The load is fully transactional: either all features are inserted or none
    (TerritorialValidationError before the transaction starts leaves the DB
    unchanged; a mid-load database error rolls back the transaction).

    Args:
        conn: An asyncpg connection to a PostGIS-enabled PostgreSQL database.
        cache_path: Optional path to a locally cached GeoJSON file. If None,
            uses the default cache path and downloads if absent.
        skip_source_check: Skip the source_registry check. For use in tests
            only — production code must always register the source first.

    Returns:
        The number of entity records inserted or updated.

    Raises:
        TerritorialValidationError: If any feature fails the territorial
            position validation. No records are written.
        RuntimeError: If NE_SOURCE_ID is not registered in source_registry
            (unless skip_source_check=True).
        httpx.HTTPError: If the GeoJSON download fails and no cache exists.
    """
    if not skip_source_check:
        await _assert_source_registered(conn)

    fc = await _fetch_or_load_geojson(cache_path)
    features = fc.get("features", [])
    logger.info("Loaded %d Natural Earth features", len(features))

    # Derive entity IDs and filter features with valid codes.
    valid_features: list[tuple[str, dict[str, Any]]] = []
    skipped = 0
    for feature in features:
        props = feature.get("properties") or {}
        entity_id = _derive_entity_id(props)
        if entity_id is None:
            logger.warning(
                "Skipping NE feature with no valid ISO_A3/ADM0_A3: NAME=%s",
                props.get("NAME", "<unknown>"),
            )
            skipped += 1
            continue
        valid_features.append((entity_id, props))

    if skipped:
        logger.warning("Skipped %d features with missing ISO codes", skipped)

    # Hard gate — validate all features before any INSERT.
    validator = TerritorialValidator()
    validator.validate_all(valid_features)
    logger.info("Territorial validation passed for %d features", len(valid_features))

    # All features valid — insert in a single transaction.
    inserted = 0
    async with conn.transaction():
        for entity_id, props in valid_features:
            feature_geom = next(
                f["geometry"]
                for f in features
                if _derive_entity_id(f.get("properties") or {}) == entity_id
            )
            geometry_json = json.dumps(_ensure_multipolygon(feature_geom))
            attributes = _build_attributes(props)
            metadata = {
                "name_en": props.get("NAME", ""),
                "name_long": props.get("NAME_LONG", ""),
                "iso_a3": entity_id,
                "iso_a2": props.get("ISO_A2", ""),
                "name_key": f"country.{entity_id}.name",
                "continent": props.get("CONTINENT", ""),
                "un_region": props.get("REGION_UN", ""),
                "subregion": props.get("SUBREGION", ""),
                "economy_label": props.get("ECONOMY", ""),
                "income_group_label": props.get("INCOME_GRP", ""),
                "ne_source": NE_SOURCE_ID,
            }

            await conn.execute(
                """
                INSERT INTO simulation_entities
                    (entity_id, entity_type, geometry, attributes, metadata)
                VALUES
                    ($1, 'country', ST_GeomFromGeoJSON($2), $3::jsonb, $4::jsonb)
                ON CONFLICT (entity_id) DO UPDATE
                    SET geometry   = EXCLUDED.geometry,
                        attributes = EXCLUDED.attributes,
                        metadata   = EXCLUDED.metadata,
                        updated_at = NOW()
                """,
                entity_id,
                geometry_json,
                json.dumps(attributes),
                json.dumps(metadata),
            )
            inserted += 1

    logger.info(
        "Natural Earth 110m load complete: %d entities inserted/updated", inserted
    )
    return inserted
