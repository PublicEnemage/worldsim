"""Integration tests for the Natural Earth boundary loader and DB seed pipeline.

Marked pytest.mark.integration — requires a running PostGIS database with
DATABASE_URL set in the environment. All tests are skipped gracefully when
DATABASE_URL is absent.

Tests cover:
  1. TerritorialValidator blocks a feature with a prohibited Taiwan label
     before any INSERT (no DB needed — validator is pure Python)
  2. Validator passes a representative set of clean NE-like features
  3. Entity records have geometry that is valid PostGIS geometry  [DB required]
  4. JSONB attribute values deserialize to Quantity-compatible dicts [DB required]
"""
from __future__ import annotations

import json
import os
from decimal import Decimal
from typing import Any

import pytest

from app.db.territorial_validator import TerritorialValidationError, TerritorialValidator

# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------

_DATABASE_URL = os.environ.get("DATABASE_URL", "")
_DB_AVAILABLE = bool(_DATABASE_URL)

pytestmark = pytest.mark.integration


def _require_db() -> None:
    """Skip test gracefully when no DATABASE_URL is configured."""
    if not _DB_AVAILABLE:
        pytest.skip("DATABASE_URL not set — skipping PostGIS integration test")


def _make_country_feature(
    iso_a3: str,
    name: str,
    *,
    adm0_a3: str | None = None,
) -> tuple[str, dict[str, Any]]:
    """Build a minimal (entity_id, ne_properties) pair for validator testing."""
    props: dict[str, Any] = {
        "NAME": name,
        "ISO_A3": iso_a3,
        "POP_EST": 1_000_000,
        "GDP_MD": 5000,
        "POP_RANK": 10,
    }
    if adm0_a3:
        props["ADM0_A3"] = adm0_a3
    return iso_a3, props


# ---------------------------------------------------------------------------
# 1. TerritorialValidator blocks prohibited Taiwan label (no DB required)
# ---------------------------------------------------------------------------


def test_validator_blocks_taiwan_province_of_china() -> None:
    """Validator raises TerritorialValidationError on prohibited Taiwan name.

    This fires before any INSERT — the pipeline never reaches the database.
    No DATABASE_URL is required for this test.
    """
    validator = TerritorialValidator()
    entities = [
        _make_country_feature("TWN", "Taiwan, Province of China"),
        _make_country_feature("USA", "United States of America"),
    ]
    with pytest.raises(TerritorialValidationError) as exc_info:
        validator.validate_all(entities)
    msg = str(exc_info.value)
    assert "[TWN]" in msg
    assert "Taiwan, Province of China" in msg
    # Pipeline-halt guarantee: message must signal no records were written
    assert "no records written" in msg.lower()


def test_validator_blocks_all_prohibited_names_in_batch() -> None:
    """All five POLICY.md violations are collected in one batch-error raise."""
    validator = TerritorialValidator()
    entities = [
        ("TWN", {"NAME": "Taiwan, Province of China", "ISO_A3": "TWN"}),
        ("PSE", {"NAME": "Palestine", "ISO_A3": "ISR"}),
        ("XKX", {"NAME": "Kosovo", "ISO_A3": "-99", "ADM0_A3": "SRB"}),
        ("ESH", {"NAME": "Western Sahara", "ISO_A3": "MAR"}),
        ("CRM", {"NAME": "Crimea"}),
    ]
    with pytest.raises(TerritorialValidationError) as exc_info:
        validator.validate_all(entities)
    msg = str(exc_info.value)
    assert "5 territorial validation violation(s)" in msg


# ---------------------------------------------------------------------------
# 2. Validator passes clean Natural-Earth-like features (no DB required)
# ---------------------------------------------------------------------------


def test_validator_passes_clean_ne_representative_set() -> None:
    """A representative set of clean NE features passes without error."""
    validator = TerritorialValidator()
    clean_entities = [
        _make_country_feature("USA", "United States of America"),
        _make_country_feature("DEU", "Germany"),
        _make_country_feature("BRA", "Brazil"),
        _make_country_feature("NGA", "Nigeria"),
        _make_country_feature("IND", "India"),
        _make_country_feature("CHN", "China"),
        _make_country_feature("TWN", "Taiwan"),
        ("PSE", {"NAME": "Palestine", "ISO_A3": "PSE", "ADM0_A3": "PSE"}),
        ("XKX", {"NAME": "Kosovo", "ISO_A3": "-99", "ADM0_A3": "XKX"}),
        _make_country_feature("ESH", "Western Sahara"),
        _make_country_feature("UKR", "Ukraine"),
    ]
    # Must not raise
    validator.validate_all(clean_entities)


# ---------------------------------------------------------------------------
# 3 & 4. Database-backed tests (require PostGIS)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_loaded_entity_has_valid_postgis_geometry() -> None:
    """Entity records inserted by the NE loader have valid PostGIS geometry.

    Requires PostGIS with the NE_110M_2024 source registered.
    """
    _require_db()

    try:
        import asyncpg
    except ImportError:
        pytest.skip("asyncpg not installed")

    conn: asyncpg.Connection = await asyncpg.connect(_DATABASE_URL)
    try:
        row = await conn.fetchrow(
            """
            SELECT entity_id, ST_IsValid(geometry) AS geom_valid,
                   ST_GeometryType(geometry) AS geom_type
            FROM simulation_entities
            WHERE entity_type = 'country'
            LIMIT 1
            """
        )
        if row is None:
            pytest.skip("simulation_entities is empty — run the NE loader first")

        assert row["geom_valid"] is True, (
            f"geometry for {row['entity_id']} is not valid PostGIS geometry"
        )
        assert row["geom_type"] == "ST_MultiPolygon", (
            f"expected ST_MultiPolygon, got {row['geom_type']} for {row['entity_id']}"
        )
    finally:
        await conn.close()


@pytest.mark.asyncio
async def test_loaded_entity_attributes_deserialize_to_quantity_shape() -> None:
    """JSONB attributes on a loaded entity match the ADR-003 Quantity envelope.

    Each attribute value must have: value (str Decimal), unit (str),
    variable_type, confidence_tier (int), observation_date, source_registry_id.
    """
    _require_db()

    try:
        import asyncpg
    except ImportError:
        pytest.skip("asyncpg not installed")

    conn: asyncpg.Connection = await asyncpg.connect(_DATABASE_URL)
    try:
        row = await conn.fetchrow(
            """
            SELECT entity_id, attributes
            FROM simulation_entities
            WHERE entity_type = 'country'
              AND attributes != '{}'::jsonb
            LIMIT 1
            """
        )
        if row is None:
            pytest.skip("No entities with non-empty attributes — run the NE loader first")

        attributes: dict[str, Any] = row["attributes"]
        if isinstance(attributes, str):
            attributes = json.loads(attributes)

        assert isinstance(attributes, dict), "attributes must be a JSON object"
        assert len(attributes) > 0, "expected at least one attribute"

        for attr_key, qty in attributes.items():
            assert isinstance(qty, dict), f"{attr_key}: expected dict, got {type(qty)}"
            assert "value" in qty, f"{attr_key}: missing 'value' field"
            assert "unit" in qty, f"{attr_key}: missing 'unit' field"
            assert "variable_type" in qty, f"{attr_key}: missing 'variable_type' field"
            assert "confidence_tier" in qty, f"{attr_key}: missing 'confidence_tier' field"
            assert "observation_date" in qty, f"{attr_key}: missing 'observation_date' field"
            assert "source_registry_id" in qty, f"{attr_key}: missing 'source_registry_id' field"

            # value must be a string encoding of a Decimal, not a JSON number
            assert isinstance(qty["value"], str), (
                f"{attr_key}: 'value' must be a string (ADR-003 float prohibition), "
                f"got {type(qty['value'])}"
            )
            # Must parse as Decimal without error
            Decimal(qty["value"])

            assert isinstance(qty["confidence_tier"], int), (
                f"{attr_key}: confidence_tier must be int, got {type(qty['confidence_tier'])}"
            )
            assert 1 <= qty["confidence_tier"] <= 5, (
                f"{attr_key}: confidence_tier {qty['confidence_tier']} out of range 1–5"
            )
    finally:
        await conn.close()


@pytest.mark.asyncio
async def test_entity_count_matches_loaded_features() -> None:
    """After a full NE load, at least 170 country entities should be present.

    Natural Earth 110m includes ~177 features with valid ISO_A3 codes.
    This is a lower-bound sanity check, not an exact-count assertion.
    """
    _require_db()

    try:
        import asyncpg
    except ImportError:
        pytest.skip("asyncpg not installed")

    conn: asyncpg.Connection = await asyncpg.connect(_DATABASE_URL)
    try:
        row = await conn.fetchrow(
            "SELECT COUNT(*) AS n FROM simulation_entities WHERE entity_type = 'country'"
        )
        if row is None or row["n"] == 0:
            pytest.skip("simulation_entities is empty — run the NE loader first")
        assert row["n"] >= 170, f"expected ≥ 170 country entities, got {row['n']}"
    finally:
        await conn.close()
