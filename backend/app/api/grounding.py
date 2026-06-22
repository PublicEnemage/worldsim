"""ADR-016 Scenario Grounding — read-only and Path 1 endpoints.

GET /entities/{entity_id}/data-quality?year={year}
    Component 1: pre-creation data quality preview per entity and year.
    Reads from entity_data_quality_coverage. Falls back to source_registry
    (loadable=True) or ADR-007 synthetic (loadable=False) for unknown entities.

GET /scenarios/{scenario_id}/initial-state
    Component 2: source-cited step-0 indicators for a completed scenario.
    Reads step-0 snapshot state_data and joins to source_registry for source
    and vintage attribution. Returns empty frameworks dict (not 404) for
    scenarios with no source-registry-linked indicators (SF-2 guard).

POST /entities/{entity_id}/pull?year={year}
    DA-G4-2: trigger an async data pull job for a non-preloaded registered-source
    entity. Populates entity_data_quality_coverage from source_registry metadata.
    M15 scope: does NOT fetch live data from external APIs (M16+ capability).

GET /entities/{entity_id}/pull/{job_id}
    DA-G4-2: poll the status of a data pull job.

GET /scenarios/{scenario_id}/fidelity-context
    DA-G4-4: Chief Methodologist analogous-case contextualisation for a scenario.
    Rule-based entity→case mapping. Returns analogous_case: null for entities
    not in the mapping table (not an error).

ADR reference: ADR-016 — Scenario Grounding Architecture (Accepted 2026-06-16)
Sprint: M15-G4 — Path 1 approved source network + fidelity contextualisation
"""
from __future__ import annotations

import asyncio
import json
import uuid as _uuid
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
# DA-G4-4: Chief Methodologist analogous-case mapping table
# ---------------------------------------------------------------------------

_ANALOGOUS_CASE_MAP: dict[str, dict[str, object]] = {
    "ZMB": {
        "case_id": "ARG",
        "case_name": "Argentina 2001–2002",
        "mechanism_type": "external_debt_restructuring",
        "mechanism_match": (
            "External debt restructuring under IMF engagement;"
            " reserve depletion under capital account pressure."
        ),
        "directional_accuracy_validated": True,
        "magnitude_validated": False,
        "use_for": "direction and threshold detection",
    },
    "JOR": {
        "case_id": "GRC",
        "case_name": "Greece 2010–2012",
        "mechanism_type": "fiscal_consolidation_external_conditionality",
        "mechanism_match": (
            "Fiscal consolidation programme with IMF/EU conditionality;"
            " programme survival probability as binding constraint."
        ),
        "directional_accuracy_validated": True,
        "magnitude_validated": False,
        "use_for": "direction and threshold detection",
    },
    "EGY": {
        "case_id": "ARG",
        "case_name": "Argentina 2001–2002",
        "mechanism_type": "external_debt_restructuring",
        "mechanism_match": (
            "External debt restructuring + IMF SBA programme;"
            " large informal economy; reserve drawdown under IMF surveillance."
        ),
        "directional_accuracy_validated": True,
        "magnitude_validated": False,
        "use_for": "direction and threshold detection",
    },
    "GRC": {
        "case_id": "GRC",
        "case_name": "Greece 2010–2012",
        "mechanism_type": "fiscal_consolidation_external_conditionality",
        "mechanism_match": "Exact match — the primary calibration case for this simulation engine.",
        "directional_accuracy_validated": True,
        "magnitude_validated": True,
        "use_for": "direction and threshold detection",
    },
}

# ---------------------------------------------------------------------------
# Variable sets for framework inference from simulation_variables
# ---------------------------------------------------------------------------

_FINANCIAL_VARS: frozenset[str] = frozenset({
    "gdp_growth", "inflation_rate", "debt_to_gdp", "reserve_coverage_months",
    "primary_balance_pct_gdp", "current_account_balance_pct_gdp", "gdp_usd_millions",
})
_HD_VARS: frozenset[str] = frozenset({
    "health_expenditure_pct_gdp", "net_enrollment_rate", "population_total",
})


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
    loadable: bool = False
    load_action_available: bool = False


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


class PullJobResponse(BaseModel):
    job_id: str
    entity_id: str
    year: int
    status: str


class PullJobStatusResponse(BaseModel):
    job_id: str
    status: str
    frameworks_loaded: list[str]
    error: str | None = None


class AnalogousCase(BaseModel):
    case_id: str
    case_name: str
    mechanism_type: str
    mechanism_match: str
    directional_accuracy_validated: bool
    magnitude_validated: bool
    use_for: str


class FidelityContextResponse(BaseModel):
    scenario_id: str
    entity_id: str
    analogous_case: AnalogousCase | None = None


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


def _infer_covered_frameworks(sim_vars: list[str]) -> list[str]:
    """Infer which measurement frameworks a source covers from its simulation_variables."""
    covered: list[str] = []
    if any(v in _FINANCIAL_VARS for v in sim_vars):
        covered.append("financial")
    if any(v in _HD_VARS for v in sim_vars):
        covered.append("human_development")
    if not covered:
        covered = ["financial", "human_development"]
    return covered


# ---------------------------------------------------------------------------
# GET /entities/{entity_id}/data-quality
# ---------------------------------------------------------------------------


@router.get("/entities/{entity_id}/data-quality", response_model=DataQualityResponse)
async def get_entity_data_quality(
    entity_id: str,
    year: int = Query(..., ge=1900, le=2100, description="Scenario start year"),
) -> DataQualityResponse:
    """Return per-framework data quality metadata for an entity in a given year.

    Priority order:
    1. entity_data_quality_coverage rows (preloaded) → loadable: false
    2. source_registry registered coverage (not yet pulled) → loadable: true
    3. ADR-007 synthetic fallback → confidence_tier: 4, is_synthetic: true

    Returns HTTP 200 in all cases (SF-1 guard — never 404 for unknown entity_id).
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

    if rows:
        # Entity is preloaded — all frameworks are loadable: false
        frameworks = [
            DataQualityFramework(
                framework=row["measurement_framework"],
                confidence_tier=row["confidence_tier"],
                source_institution=row["source_institution"],
                data_vintage=row["data_vintage"],
                is_synthetic=row["is_synthetic"],
                synthetic_basis=row["synthetic_basis"],
                loadable=False,
                load_action_available=False,
            )
            for row in rows
        ]
        return DataQualityResponse(entity_id=entity_id, year=year, frameworks=frameworks)

    # No preloaded data — check source_registry for registered coverage
    async with pool.acquire() as conn:
        source_rows = await conn.fetch(
            """
            SELECT source_id, provider, coverage_end, quality_tier, simulation_variables
            FROM source_registry
            WHERE $1 = ANY(coverage_countries)
              AND coverage_start <= make_date($2, 1, 1)
            ORDER BY quality_tier, coverage_end DESC NULLS LAST
            """,
            entity_id,
            year,
        )

    if source_rows:
        # Entity has registered source coverage but data not yet pulled
        best_source = source_rows[0]
        vintage = _coverage_end_to_vintage(best_source["coverage_end"])
        sim_vars = list(best_source["simulation_variables"] or [])
        covered_frameworks = _infer_covered_frameworks(sim_vars)

        frameworks = [
            DataQualityFramework(
                framework=fw,
                confidence_tier=int(best_source["quality_tier"]),
                source_institution=best_source["provider"],
                data_vintage=vintage,
                is_synthetic=False,
                synthetic_basis=None,
                loadable=True,
                load_action_available=True,
            )
            for fw in covered_frameworks
        ]
        # Add ecological as synthetic (T4) — no registered coverage for non-preloaded entities
        frameworks.append(
            DataQualityFramework(
                framework="ecological",
                confidence_tier=4,
                source_institution=None,
                data_vintage=None,
                is_synthetic=True,
                synthetic_basis="Global comparable economies — no registered source coverage",
                loadable=False,
                load_action_available=False,
            )
        )
        return DataQualityResponse(entity_id=entity_id, year=year, frameworks=frameworks)

    # No registered coverage — ADR-007 synthetic fallback
    synthetic_frameworks = [
        DataQualityFramework(
            framework=fw,
            confidence_tier=4,
            source_institution=None,
            data_vintage=None,
            is_synthetic=True,
            synthetic_basis="Global comparable economies — no registered source coverage",
            loadable=False,
            load_action_available=False,
        )
        for fw in ["financial", "human_development", "ecological", "governance"]
    ]
    return DataQualityResponse(entity_id=entity_id, year=year, frameworks=synthetic_frameworks)


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


# ---------------------------------------------------------------------------
# POST /entities/{entity_id}/pull  — DA-G4-2
# ---------------------------------------------------------------------------


@router.post("/entities/{entity_id}/pull", response_model=PullJobResponse)
async def trigger_data_pull(
    entity_id: str,
    year: int = Query(..., ge=1900, le=2100, description="Scenario start year"),
) -> PullJobResponse:
    """Trigger an async data pull job for a non-preloaded registered-source entity.

    M15 scope: populates entity_data_quality_coverage from source_registry metadata.
    Does not fetch live data from external APIs (M16+ capability).
    Status transitions: queued → running → complete | failed.
    """
    pool = get_asyncpg_pool()
    job_id = str(_uuid.uuid4())

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO data_pull_jobs (job_id, entity_id, year, status, frameworks_loaded)
            VALUES ($1, $2, $3, 'queued', '{}')
            """,
            job_id, entity_id, year,
        )

    # Run the pull job asynchronously in the background
    asyncio.create_task(_run_pull_job(job_id, entity_id, year))

    return PullJobResponse(
        job_id=job_id, entity_id=entity_id, year=year, status="queued"
    )


async def _run_pull_job(job_id: str, entity_id: str, year: int) -> None:
    """Background task: populate entity_data_quality_coverage from source_registry metadata."""
    pool = get_asyncpg_pool()
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE data_pull_jobs"
                " SET status = 'running', updated_at = now()"
                " WHERE job_id = $1",
                job_id,
            )
            # Look up registered source coverage for this entity
            source_rows = await conn.fetch(
                """
                SELECT source_id, provider, coverage_end, quality_tier, simulation_variables
                FROM source_registry
                WHERE $1 = ANY(coverage_countries)
                  AND coverage_start <= make_date($2, 1, 1)
                ORDER BY quality_tier, coverage_end DESC NULLS LAST
                LIMIT 1
                """,
                entity_id, year,
            )
            if not source_rows:
                await conn.execute(
                    "UPDATE data_pull_jobs"
                    " SET status = 'failed', error = $2, updated_at = now()"
                    " WHERE job_id = $1",
                    job_id, f"No registered source coverage for entity {entity_id!r}",
                )
                return

            best = source_rows[0]
            sim_vars = list(best["simulation_variables"] or [])
            covered = _infer_covered_frameworks(sim_vars)

            vintage = _coverage_end_to_vintage(best["coverage_end"])
            tier = int(best["quality_tier"])

            for fw in covered:
                # Use WHERE NOT EXISTS to avoid duplicate rows (table has no unique constraint)
                await conn.execute(
                    """
                    INSERT INTO entity_data_quality_coverage
                        (entity_id, measurement_framework, confidence_tier,
                         source_institution, data_vintage, is_synthetic,
                         synthetic_basis, coverage_year_from, coverage_year_to)
                    SELECT $1, $2, $3, $4, $5, false, null, $6, null
                    WHERE NOT EXISTS (
                        SELECT 1 FROM entity_data_quality_coverage
                        WHERE entity_id = $1
                          AND measurement_framework = $2
                          AND coverage_year_from = $6
                    )
                    """,
                    entity_id, fw, tier, best["provider"], vintage, year,
                )

            await conn.execute(
                """
                UPDATE data_pull_jobs
                SET status = 'complete', frameworks_loaded = $2, updated_at = now()
                WHERE job_id = $1
                """,
                job_id, covered,
            )
    except Exception as exc:
        try:
            async with pool.acquire() as conn:
                await conn.execute(
                    "UPDATE data_pull_jobs"
                    " SET status = 'failed', error = $2, updated_at = now()"
                    " WHERE job_id = $1",
                    job_id, str(exc),
                )
        except Exception:  # noqa: BLE001 S110
            pass


# ---------------------------------------------------------------------------
# GET /entities/{entity_id}/pull/{job_id}  — DA-G4-2
# ---------------------------------------------------------------------------


@router.get("/entities/{entity_id}/pull/{job_id}", response_model=PullJobStatusResponse)
async def get_pull_job_status(entity_id: str, job_id: str) -> PullJobStatusResponse:
    """Poll the status of a data pull job."""
    pool = get_asyncpg_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT job_id, status, frameworks_loaded, error
            FROM data_pull_jobs
            WHERE job_id = $1 AND entity_id = $2
            """,
            job_id, entity_id,
        )
    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Pull job '{job_id}' not found for entity '{entity_id}'.",
        )
    return PullJobStatusResponse(
        job_id=row["job_id"],
        status=row["status"],
        frameworks_loaded=list(row["frameworks_loaded"] or []),
        error=row["error"],
    )


# ---------------------------------------------------------------------------
# GET /scenarios/{scenario_id}/fidelity-context  — DA-G4-4
# ---------------------------------------------------------------------------


@router.get("/scenarios/{scenario_id}/fidelity-context", response_model=FidelityContextResponse)
async def get_fidelity_context(scenario_id: str) -> FidelityContextResponse:
    """Return the Chief Methodologist analogous-case contextualisation for a scenario.

    DA-G4-4: rule-based entity→case mapping. Returns analogous_case: null for entities
    not in the mapping table (fallback path, not an error).
    db_reads: [scenarios]
    """
    pool = get_asyncpg_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT configuration FROM scenarios WHERE scenario_id = $1",
            scenario_id,
        )
    if row is None:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found.")

    config_raw = row["configuration"]
    if isinstance(config_raw, str):
        config: dict[str, object] = json.loads(config_raw)
    else:
        config = dict(config_raw)

    entities_raw = config.get("entities", [])
    entities = entities_raw if isinstance(entities_raw, list) else []
    entity_id = str(entities[0]) if entities else ""

    case_data = _ANALOGOUS_CASE_MAP.get(entity_id)
    analogous_case: AnalogousCase | None = None
    if case_data is not None:
        analogous_case = AnalogousCase(
            case_id=str(case_data["case_id"]),
            case_name=str(case_data["case_name"]),
            mechanism_type=str(case_data["mechanism_type"]),
            mechanism_match=str(case_data["mechanism_match"]),
            directional_accuracy_validated=bool(case_data["directional_accuracy_validated"]),
            magnitude_validated=bool(case_data["magnitude_validated"]),
            use_for=str(case_data["use_for"]),
        )

    return FidelityContextResponse(
        scenario_id=scenario_id,
        entity_id=entity_id,
        analogous_case=analogous_case,
    )
