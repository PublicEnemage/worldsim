"""ADR-016 Scenario Grounding — two read-only endpoints.

GET /entities/{entity_id}/data-quality?year={year}
    Component 1: pre-creation data quality preview per entity and year.
    Reads from entity_data_quality_coverage. Returns empty frameworks list
    (not 404) for entities not in the registry (SF-1 guard).

GET /scenarios/{scenario_id}/initial-state
    Component 2: source-cited step-0 indicators for a completed scenario.
    Reads step-0 snapshot state_data and joins to source_registry for source
    and vintage attribution. Returns empty frameworks dict (not 404) for
    scenarios with no source-registry-linked indicators (SF-2 guard).

ADR reference: ADR-016 — Scenario Grounding Architecture (Accepted 2026-06-16)
Sprint: M14-G3 — backend infrastructure for G4 frontend
"""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.db.connection import get_asyncpg_pool

if TYPE_CHECKING:
    from datetime import date

router = APIRouter(tags=["grounding"])

# ---------------------------------------------------------------------------
# Static display name registry (grows as new indicators are seeded)
# ---------------------------------------------------------------------------

_DISPLAY_NAMES: dict[str, str] = {
    "reserve_coverage_months": "Reserve coverage",
    "gdp_growth": "GDP growth rate",
    "trend_growth": "Trend growth rate",
    "unemployment_rate": "Unemployment rate",
    "health_expenditure_pct_gdp": "Health expenditure (% GDP)",
    "net_enrollment_rate": "Net primary enrollment rate",
    "population_total": "Total population",
    "gdp_usd_millions": "GDP (USD millions)",
    "debt_to_gdp": "Debt-to-GDP ratio",
    "current_account_balance_pct_gdp": "Current account balance (% GDP)",
    "inflation_rate": "Inflation rate",
    "primary_balance_pct_gdp": "Primary fiscal balance (% GDP)",
}


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------


class DataQualityFramework(BaseModel):
    framework: str
    confidence_tier: int
    source_institution: str | None = None
    data_vintage: str | None = None
    is_synthetic: bool
    synthetic_basis: str | None = None


class DataQualityResponse(BaseModel):
    entity_id: str
    year: int
    frameworks: list[DataQualityFramework]


class InitialStateIndicator(BaseModel):
    name: str
    display_name: str
    value: float | None
    unit: str | None = None
    source: str | None = None
    vintage: str | None = None
    confidence_tier: int
    is_synthetic: bool


class InitialStateFramework(BaseModel):
    indicators: list[InitialStateIndicator]


class InitialStateResponse(BaseModel):
    scenario_id: str
    entity_id: str
    step_0_year: int | None
    frameworks: dict[str, InitialStateFramework]


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _coverage_end_to_vintage(coverage_end: date | None) -> str | None:
    """Convert a coverage_end date to a 'YYYY-QN' vintage string."""
    if coverage_end is None:
        return None
    month = coverage_end.month
    quarter = (month - 1) // 3 + 1
    return f"{coverage_end.year}-Q{quarter}"


# ---------------------------------------------------------------------------
# GET /entities/{entity_id}/data-quality
# ---------------------------------------------------------------------------


@router.get("/entities/{entity_id}/data-quality", response_model=DataQualityResponse)
async def get_entity_data_quality(
    entity_id: str,
    year: int = Query(..., ge=1900, le=2100, description="Scenario start year"),
) -> DataQualityResponse:
    """Return per-framework data quality metadata for an entity in a given year.

    Reads entity_data_quality_coverage. Returns HTTP 200 with empty frameworks
    list for entities not in the registry (SF-1 guard — not 404).
    """
    pool = get_asyncpg_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT
                measurement_framework,
                confidence_tier,
                source_institution,
                data_vintage,
                is_synthetic,
                synthetic_basis
            FROM entity_data_quality_coverage
            WHERE entity_id = $1
              AND coverage_year_from <= $2
              AND (coverage_year_to IS NULL OR coverage_year_to >= $2)
            ORDER BY measurement_framework
            """,
            entity_id,
            year,
        )

    frameworks = [
        DataQualityFramework(
            framework=row["measurement_framework"],
            confidence_tier=row["confidence_tier"],
            source_institution=row["source_institution"],
            data_vintage=row["data_vintage"],
            is_synthetic=row["is_synthetic"],
            synthetic_basis=row["synthetic_basis"],
        )
        for row in rows
    ]

    return DataQualityResponse(entity_id=entity_id, year=year, frameworks=frameworks)


# ---------------------------------------------------------------------------
# GET /scenarios/{scenario_id}/initial-state
# ---------------------------------------------------------------------------


@router.get("/scenarios/{scenario_id}/initial-state", response_model=InitialStateResponse)
async def get_scenario_initial_state(scenario_id: str) -> InitialStateResponse:
    """Return source-cited step-0 indicators for a completed scenario.

    Reads the step-0 snapshot state_data, parses SA-09 Quantity envelopes,
    joins to source_registry for source and vintage attribution, and returns
    indicators grouped by measurement_framework.

    Returns HTTP 200 with empty frameworks dict for scenarios with no
    source-registry-linked indicator data (SF-2 guard — not 404).
    """
    pool = get_asyncpg_pool()
    async with pool.acquire() as conn:
        # Confirm scenario exists
        scenario_row = await conn.fetchrow(
            "SELECT scenario_id, configuration FROM scenarios WHERE scenario_id = $1",
            scenario_id,
        )
        if scenario_row is None:
            raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found.")

        # Fetch the step-0 snapshot
        snapshot_row = await conn.fetchrow(
            """
            SELECT state_data, timestep
            FROM scenario_state_snapshots
            WHERE scenario_id = $1 AND step = 0
            ORDER BY id
            LIMIT 1
            """,
            scenario_id,
        )

    if snapshot_row is None:
        # Scenario exists but has not been run yet — return empty frameworks (SF-2)
        return InitialStateResponse(
            scenario_id=scenario_id,
            entity_id="",
            step_0_year=None,
            frameworks={},
        )

    # Parse state_data JSONB
    state_data_raw = snapshot_row["state_data"]
    if isinstance(state_data_raw, str):
        state_data: dict[str, Any] = json.loads(state_data_raw)
    else:
        state_data = dict(state_data_raw)

    step_0_year: int | None = None
    if snapshot_row["timestep"] is not None:
        step_0_year = snapshot_row["timestep"].year

    # Collect entity attribute envelopes — skip metadata keys (underscore-prefixed)
    # In G3 scope, each scenario has at most one primary entity; we take the first.
    entity_id = ""
    all_envelopes: list[dict[str, Any]] = []

    for key, value in state_data.items():
        if key.startswith("_") or not isinstance(value, dict):
            continue
        entity_id = key
        for attr_key, envelope in value.items():
            if attr_key.startswith("_") or not isinstance(envelope, dict):
                continue
            if "_envelope_version" not in envelope:
                continue
            all_envelopes.append({"attr_key": attr_key, "envelope": envelope})

    if not all_envelopes:
        # No source-registry-linked data — SF-2 guard
        return InitialStateResponse(
            scenario_id=scenario_id,
            entity_id=entity_id,
            step_0_year=step_0_year,
            frameworks={},
        )

    # Collect distinct source_registry_ids to look up in one query
    source_ids = {
        e["envelope"]["source_registry_id"]
        for e in all_envelopes
        if e["envelope"].get("source_registry_id")
    }

    source_lookup: dict[str, dict[str, Any]] = {}
    if source_ids:
        async with pool.acquire() as conn:
            source_rows = await conn.fetch(
                """
                SELECT source_id, provider, coverage_end
                FROM source_registry
                WHERE source_id = ANY($1)
                """,
                list(source_ids),
            )
        for row in source_rows:
            source_lookup[row["source_id"]] = {
                "provider": row["provider"],
                "vintage": _coverage_end_to_vintage(row["coverage_end"]),
            }

    # Group indicators by measurement_framework
    frameworks_dict: dict[str, list[InitialStateIndicator]] = {}

    for item in all_envelopes:
        attr_key = item["attr_key"]
        envelope = item["envelope"]

        framework = str(envelope.get("measurement_framework", ""))
        if not framework:
            continue

        source_id = envelope.get("source_registry_id")
        source_info = source_lookup.get(source_id, {}) if source_id else {}

        raw_value = envelope.get("value")
        try:
            float_value: float | None = float(raw_value) if raw_value is not None else None
        except (TypeError, ValueError):
            float_value = None

        tier = int(envelope.get("confidence_tier", 5))

        indicator = InitialStateIndicator(
            name=attr_key,
            display_name=_DISPLAY_NAMES.get(attr_key, attr_key.replace("_", " ").title()),
            value=float_value,
            unit=envelope.get("unit"),
            source=source_info.get("provider"),
            vintage=source_info.get("vintage"),
            confidence_tier=tier,
            is_synthetic=(tier >= 3),
        )

        if framework not in frameworks_dict:
            frameworks_dict[framework] = []
        frameworks_dict[framework].append(indicator)

    frameworks_response = {
        fw: InitialStateFramework(indicators=indicators)
        for fw, indicators in frameworks_dict.items()
    }

    return InitialStateResponse(
        scenario_id=scenario_id,
        entity_id=entity_id,
        step_0_year=step_0_year,
        frameworks=frameworks_response,
    )
