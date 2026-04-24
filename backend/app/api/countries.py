"""Country endpoints — ADR-003 Decision 2.

Six endpoints covering the full country data surface for Milestone 2:
  GET /countries                    — summary list (no geometry, no attributes)
  GET /countries/{entity_id}        — full detail with attributes
  GET /countries/{entity_id}/geometry — GeoJSON Feature
  GET /countries/{entity_id}/attributes — attributes only
  GET /choropleth/{attribute_key}   — primary MapLibre endpoint
  GET /attributes/available         — attribute key discovery

All queries use asyncpg directly per ADR-003 Decision 2. The choropleth query
joins geometry and attribute data in a single PostGIS round-trip.

`attribute_value` is always serialized as a string (Decimal → str). MapLibre
parses the string to float at the rendering boundary only.
"""
from __future__ import annotations

import contextlib
import json
from typing import Annotated, Any

import asyncpg  # noqa: TCH002 — used in Annotated[] resolved at runtime by FastAPI
from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_db  # noqa: TCH001 — used as Depends(get_db) at runtime
from app.schemas import (
    AttributeSummary,
    CountryDetail,
    CountrySummary,
    GeoJSONFeature,
    GeoJSONFeatureCollection,
    QuantitySchema,
)

router = APIRouter(tags=["countries"])


def _extract_name(metadata: dict[str, Any]) -> str:
    return str(metadata.get("name_en") or metadata.get("name_long") or "")


def _extract_iso_a2(metadata: dict[str, Any]) -> str:
    return str(metadata.get("iso_a2") or "")


def _extract_iso_a3(metadata: dict[str, Any]) -> str:
    return str(metadata.get("iso_a3") or "")


def _parse_attributes(attrs_raw: Any) -> dict[str, QuantitySchema]:  # noqa: ANN401
    """Deserialize a JSONB attributes dict to QuantitySchema instances."""
    if attrs_raw is None:
        return {}
    if isinstance(attrs_raw, str):
        attrs_raw = json.loads(attrs_raw)
    if not isinstance(attrs_raw, dict):
        return {}
    result: dict[str, QuantitySchema] = {}
    for key, val in attrs_raw.items():
        if isinstance(val, dict):
            with contextlib.suppress(Exception):
                result[key] = QuantitySchema.from_jsonb(val)
    return result


# ---------------------------------------------------------------------------
# GET /countries
# ---------------------------------------------------------------------------

@router.get("/countries", response_model=list[CountrySummary])
async def list_countries(
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
    entity_type: str = "country",
    limit: int = 250,
    offset: int = 0,
) -> list[CountrySummary]:
    """Return summary list of entities.

    No geometry, no attributes — lightweight for populating UI selectors.
    Default entity_type is 'country'; pass entity_type=region for regions.
    """
    rows = await conn.fetch(
        """
        SELECT entity_id, entity_type, metadata
        FROM simulation_entities
        WHERE entity_type = $1
        ORDER BY entity_id
        LIMIT $2 OFFSET $3
        """,
        entity_type,
        limit,
        offset,
    )
    summaries: list[CountrySummary] = []
    for row in rows:
        md = row["metadata"] or {}
        if isinstance(md, str):
            md = json.loads(md)
        summaries.append(
            CountrySummary(
                entity_id=row["entity_id"],
                entity_type=row["entity_type"],
                name=_extract_name(md),
                iso_a2=_extract_iso_a2(md),
                iso_a3=_extract_iso_a3(md),
            )
        )
    return summaries


# ---------------------------------------------------------------------------
# GET /countries/{entity_id}
# ---------------------------------------------------------------------------

@router.get("/countries/{entity_id}", response_model=CountryDetail)
async def get_country(
    entity_id: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> CountryDetail:
    """Return full entity detail including all attributes.

    Geometry is excluded — use /countries/{entity_id}/geometry for GeoJSON.
    This prevents loading a 2 MB geometry payload when only attributes are needed.
    """
    row = await conn.fetchrow(
        """
        SELECT entity_id, entity_type, attributes, metadata
        FROM simulation_entities
        WHERE entity_id = $1
        """,
        entity_id.upper(),
    )
    if row is None:
        raise HTTPException(status_code=404, detail=f"Entity '{entity_id}' not found.")

    md = row["metadata"] or {}
    if isinstance(md, str):
        md = json.loads(md)

    return CountryDetail(
        entity_id=row["entity_id"],
        entity_type=row["entity_type"],
        name=_extract_name(md),
        iso_a2=_extract_iso_a2(md),
        iso_a3=_extract_iso_a3(md),
        metadata=md,
        attributes=_parse_attributes(row["attributes"]),
    )


# ---------------------------------------------------------------------------
# GET /countries/{entity_id}/geometry
# ---------------------------------------------------------------------------

@router.get("/countries/{entity_id}/geometry", response_model=GeoJSONFeature)
async def get_country_geometry(
    entity_id: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> GeoJSONFeature:
    """Return GeoJSON Feature for one entity.

    Uses PostGIS ST_AsGeoJSON for serialization. Properties contain only
    entity_id and entity_type — no attributes.
    """
    row = await conn.fetchrow(
        """
        SELECT entity_id, entity_type, ST_AsGeoJSON(geometry) AS geometry_json
        FROM simulation_entities
        WHERE entity_id = $1
        """,
        entity_id.upper(),
    )
    if row is None or row["geometry_json"] is None:
        raise HTTPException(
            status_code=404,
            detail=f"Entity '{entity_id}' not found or has no geometry.",
        )

    return GeoJSONFeature(
        geometry=json.loads(row["geometry_json"]),
        properties={"entity_id": row["entity_id"], "entity_type": row["entity_type"]},
    )


# ---------------------------------------------------------------------------
# GET /countries/{entity_id}/attributes
# ---------------------------------------------------------------------------

@router.get(
    "/countries/{entity_id}/attributes",
    response_model=dict[str, QuantitySchema],
)
async def get_country_attributes(
    entity_id: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> dict[str, QuantitySchema]:
    """Return attributes only for one entity — no geometry, no metadata."""
    row = await conn.fetchrow(
        "SELECT attributes FROM simulation_entities WHERE entity_id = $1",
        entity_id.upper(),
    )
    if row is None:
        raise HTTPException(status_code=404, detail=f"Entity '{entity_id}' not found.")
    return _parse_attributes(row["attributes"])


# ---------------------------------------------------------------------------
# GET /choropleth/{attribute_key}
# ---------------------------------------------------------------------------

@router.get("/choropleth/{attribute_key}", response_model=GeoJSONFeatureCollection)
async def choropleth(
    attribute_key: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
    scenario_id: str | None = None,
    step: int | None = None,
) -> GeoJSONFeatureCollection:
    """Return GeoJSON FeatureCollection for MapLibre choropleth rendering.

    Each Feature carries the country geometry and a properties object with the
    requested attribute value. The geometry-attribute join is performed in a
    single PostGIS query — geometry and data in one round-trip.

    `attribute_value` is the Decimal value serialized as a string.
    MapLibre parses it to float at the rendering boundary only.

    `has_territorial_note` and `territorial_note` are populated from
    territorial_designations for disputed entities, enabling MapLibre to
    render an info icon and display DATA_STANDARDS.md display_note text on hover.

    When both `scenario_id` and `step` are provided, attribute values come from
    the scenario snapshot at that step (ADR-004 Decision 4). Geometry still
    comes from simulation_entities (unchanged between steps).

    Returns 404 if no country entities have the requested attribute.
    Returns 422 if only one of scenario_id/step is provided.
    """
    if (scenario_id is None) != (step is None):
        raise HTTPException(
            status_code=422,
            detail="Both 'scenario_id' and 'step' must be provided together, or neither.",
        )

    if scenario_id is not None and step is not None:
        return await _choropleth_from_snapshot(conn, attribute_key, scenario_id, step)

    rows = await conn.fetch(
        """
        SELECT
            ST_AsGeoJSON(e.geometry)        AS geometry_json,
            e.entity_id,
            e.entity_type,
            e.metadata,
            e.attributes->$1               AS attribute_json,
            td.display_note                AS territorial_note
        FROM simulation_entities e
        LEFT JOIN territorial_designations td
            ON td.entity_id = e.entity_id
            AND td.effective_date = (
                SELECT MAX(effective_date)
                FROM territorial_designations
                WHERE entity_id = e.entity_id
            )
        WHERE e.entity_type = 'country'
          AND e.attributes ? $1
        ORDER BY e.entity_id
        """,
        attribute_key,
    )

    if not rows:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No country entities have attribute '{attribute_key}'. "
                f"Use GET /api/v1/attributes/available to see available attribute keys."
            ),
        )

    features: list[GeoJSONFeature] = []
    for row in rows:
        if not row["geometry_json"]:
            continue

        md = row["metadata"] or {}
        if isinstance(md, str):
            md = json.loads(md)

        attr_raw = row["attribute_json"]
        if isinstance(attr_raw, str):
            attr_data: dict[str, Any] = json.loads(attr_raw)
        elif isinstance(attr_raw, dict):
            attr_data = attr_raw
        else:
            continue

        territorial_note = row["territorial_note"]

        features.append(
            GeoJSONFeature(
                geometry=json.loads(row["geometry_json"]),
                properties={
                    "entity_id": row["entity_id"],
                    "entity_type": row["entity_type"],
                    "name": _extract_name(md),
                    "attribute_key": attribute_key,
                    "attribute_value": str(attr_data.get("value", "")),
                    "attribute_unit": str(attr_data.get("unit", "")),
                    "variable_type": str(attr_data.get("variable_type", "")),
                    "confidence_tier": int(attr_data.get("confidence_tier", 5)),
                    "observation_date": attr_data.get("observation_date"),
                    "has_territorial_note": territorial_note is not None,
                    "territorial_note": territorial_note,
                },
            )
        )

    return GeoJSONFeatureCollection(features=features)


# ---------------------------------------------------------------------------
# Step-aware choropleth helper — ADR-004 Decision 4
# ---------------------------------------------------------------------------


async def _choropleth_from_snapshot(
    conn: asyncpg.Connection,
    attribute_key: str,
    scenario_id: str,
    step: int,
) -> GeoJSONFeatureCollection:
    """Build a choropleth FeatureCollection from a scenario snapshot.

    Attribute values come from scenario_state_snapshots at the given step.
    Geometry and territorial designations come from simulation_entities
    (unchanged between steps).
    """
    snap_row = await conn.fetchrow(
        "SELECT state_data FROM scenario_state_snapshots "
        "WHERE scenario_id = $1 AND step = $2",
        scenario_id,
        step,
    )
    if snap_row is None:
        raise HTTPException(
            status_code=404,
            detail=f"No snapshot for scenario '{scenario_id}' at step {step}.",
        )

    state_data = snap_row["state_data"]
    if isinstance(state_data, str):
        state_data = json.loads(state_data)

    entity_ids_with_attr = [
        eid for eid, attrs in state_data.items()
        if isinstance(attrs, dict) and attribute_key in attrs
    ]

    if not entity_ids_with_attr:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No entities in scenario '{scenario_id}' step {step} "
                f"have attribute '{attribute_key}'."
            ),
        )

    rows = await conn.fetch(
        """
        SELECT
            e.entity_id,
            e.entity_type,
            e.metadata,
            ST_AsGeoJSON(e.geometry) AS geometry_json,
            td.display_note AS territorial_note
        FROM simulation_entities e
        LEFT JOIN territorial_designations td
            ON td.entity_id = e.entity_id
            AND td.effective_date = (
                SELECT MAX(effective_date)
                FROM territorial_designations
                WHERE entity_id = e.entity_id
            )
        WHERE e.entity_id = ANY($1::text[])
        ORDER BY e.entity_id
        """,
        entity_ids_with_attr,
    )

    features: list[GeoJSONFeature] = []
    for row in rows:
        if not row["geometry_json"]:
            continue

        md = row["metadata"] or {}
        if isinstance(md, str):
            md = json.loads(md)

        attr_data = state_data.get(row["entity_id"], {}).get(attribute_key, {})
        if not isinstance(attr_data, dict):
            continue

        territorial_note = row["territorial_note"]
        features.append(
            GeoJSONFeature(
                geometry=json.loads(row["geometry_json"]),
                properties={
                    "entity_id": row["entity_id"],
                    "entity_type": row["entity_type"],
                    "name": _extract_name(md),
                    "attribute_key": attribute_key,
                    "attribute_value": str(attr_data.get("value", "")),
                    "attribute_unit": str(attr_data.get("unit", "")),
                    "variable_type": str(attr_data.get("variable_type", "")),
                    "confidence_tier": int(attr_data.get("confidence_tier", 5)),
                    "observation_date": attr_data.get("observation_date"),
                    "has_territorial_note": territorial_note is not None,
                    "territorial_note": territorial_note,
                },
            )
        )

    return GeoJSONFeatureCollection(features=features)


# ---------------------------------------------------------------------------
# GET /attributes/available
# ---------------------------------------------------------------------------

@router.get("/attributes/available", response_model=list[AttributeSummary])
async def available_attributes(
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> list[AttributeSummary]:
    """Return the set of attribute keys present across all country entities.

    Used by the frontend variable selector. Includes the unit and variable_type
    of the first occurrence of each key (all occurrences of a given key share
    the same unit and variable_type by DATA_STANDARDS.md contract).
    """
    rows = await conn.fetch(
        """
        SELECT DISTINCT
            attr_key,
            attributes->attr_key->>'unit'          AS unit,
            attributes->attr_key->>'variable_type' AS variable_type
        FROM simulation_entities,
             LATERAL jsonb_object_keys(attributes) AS attr_key
        WHERE entity_type = 'country'
        ORDER BY attr_key
        """
    )
    return [
        AttributeSummary(
            attribute_key=row["attr_key"],
            unit=str(row["unit"] or ""),
            variable_type=str(row["variable_type"] or ""),
        )
        for row in rows
    ]
