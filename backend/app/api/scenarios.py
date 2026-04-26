"""Scenario endpoints — ADR-004 Decisions 1, 2, 4, and 5; ADR-005 Decision 2.

Nine endpoints covering scenario configuration lifecycle, execution, and HCL output:
  POST   /scenarios                                        — create scenario (status: pending)
  GET    /scenarios                                        — list all scenarios (created_at desc)
  GET    /scenarios/compare         — snapshot delta; optional step alignment (ADR-004 D5)
  GET    /scenarios/{scenario_id}                          — full detail with scheduled inputs
  DELETE /scenarios/{scenario_id}                          — tombstone + cascade delete, returns 204
  POST   /scenarios/{scenario_id}/run                      — execute pending scenario to completion
  POST   /scenarios/{scenario_id}/advance                  — advance one step (ADR-004 Decision 4)
  GET    /scenarios/{scenario_id}/snapshots                — list all snapshots (ADR-004 Decision 3)
  GET    /scenarios/{scenario_id}/measurement-output — HCL output (ADR-005 Decision 2)

Validation runs at creation time (structural) — entity existence check,
n_steps bounds, step index bounds, non-empty name. Semantic validation
of ControlInput payloads runs at execution time (Issue #111).

All queries use asyncpg directly per ADR-003 Decision 2. Schema management
uses SQLAlchemy ORM via Alembic.

DELETE writes a tombstone to scenario_deleted_tombstones before the CASCADE
executes (ADR-004 Decision 1 Amendment, CONFLICT C-1 disposition). The tombstone
captures full configuration JSONB and scheduled_inputs so the scenario output can
be reconstructed from first principles (SA-11 determinism).
"""
from __future__ import annotations

import contextlib
import json
import uuid
from decimal import Decimal
from typing import Annotated, Any

import asyncpg  # noqa: TCH002 — used in Annotated[] resolved at runtime by FastAPI
from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.deps import get_db  # noqa: TCH001 — used as Depends(get_db) at runtime
from app.schemas import (
    AdvanceResponse,
    CompareResponse,
    DeltaRecord,
    FrameworkOutput,
    MDAAlert,
    MultiFrameworkOutput,
    QuantitySchema,
    RunSummaryResponse,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScenarioDetailResponse,
    ScenarioResponse,
    ScheduledInputSchema,
    SnapshotRecord,
)
from app.simulation.mda_checker import alerts_from_events_snapshot
from app.simulation.repositories.quantity_serde import IA1_CANONICAL_PHRASE

# Engine version for tombstone records — must match app version in main.py.
_ENGINE_VERSION = "0.3.0"

router = APIRouter(tags=["scenarios"])


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def _validate_create_request(req: ScenarioCreateRequest) -> None:
    """Raise HTTPException(422) for any structural validation failure."""
    errors: list[str] = []

    if not req.name.strip():
        errors.append("name must not be empty.")

    n = req.configuration.n_steps
    if n < 1 or n > 100:
        errors.append(f"n_steps must be between 1 and 100 (got {n}).")

    invalid_steps = [
        si.step
        for si in req.scheduled_inputs
        if si.step < 0 or si.step > n - 1
    ]
    if invalid_steps:
        errors.append(
            f"scheduled_inputs contain steps outside valid range 0–{n - 1}: "
            f"{sorted(set(invalid_steps))}."
        )

    if errors:
        raise HTTPException(status_code=422, detail=" ".join(errors))


async def _validate_entities_exist(
    conn: asyncpg.Connection,
    entity_ids: list[str],
) -> None:
    """Raise HTTPException(422) listing any entity_ids not in simulation_entities."""
    if not entity_ids:
        return
    rows = await conn.fetch(
        "SELECT entity_id FROM simulation_entities WHERE entity_id = ANY($1::text[])",
        entity_ids,
    )
    found = {row["entity_id"] for row in rows}
    missing = sorted(set(entity_ids) - found)
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Entity IDs not found in simulation_entities: {missing}.",
        )


# ---------------------------------------------------------------------------
# Response builders
# ---------------------------------------------------------------------------


def _row_to_response(row: dict[str, Any]) -> ScenarioResponse:
    created_at = row["created_at"]
    created_at_str = created_at.isoformat() if hasattr(created_at, "isoformat") else str(created_at)
    return ScenarioResponse(
        scenario_id=row["scenario_id"],
        name=row["name"],
        description=row["description"],
        status=row["status"],
        version=row["version"],
        created_at=created_at_str,
    )


def _build_detail_response(
    row: dict[str, Any],
    inputs: list[dict[str, Any]],
) -> ScenarioDetailResponse:
    created_at = row["created_at"]
    created_at_str = created_at.isoformat() if hasattr(created_at, "isoformat") else str(created_at)

    cfg_raw = row["configuration"]
    if isinstance(cfg_raw, str):
        cfg_raw = json.loads(cfg_raw)

    config = ScenarioConfigSchema(**cfg_raw)
    scheduled = [
        ScheduledInputSchema(
            step=inp["step"],
            input_type=inp["input_type"],
            input_data=inp["input_data"] if isinstance(inp["input_data"], dict)
            else json.loads(inp["input_data"]),
        )
        for inp in inputs
    ]
    return ScenarioDetailResponse(
        scenario_id=row["scenario_id"],
        name=row["name"],
        description=row["description"],
        status=row["status"],
        version=row["version"],
        created_at=created_at_str,
        configuration=config,
        scheduled_inputs=scheduled,
    )


# ---------------------------------------------------------------------------
# POST /scenarios
# ---------------------------------------------------------------------------


@router.post("/scenarios", response_model=ScenarioResponse, status_code=201)
async def create_scenario(
    req: ScenarioCreateRequest,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> ScenarioResponse:
    """Create a new scenario in pending status.

    Validates structural constraints (non-empty name, n_steps bounds, step
    index bounds) and confirms all entity_ids exist in simulation_entities
    before writing. Returns 422 with a human-readable message on any failure.
    """
    _validate_create_request(req)
    await _validate_entities_exist(conn, req.configuration.entities)

    scenario_id = str(uuid.uuid4())
    config_json = req.configuration.model_dump(mode="json")

    async with conn.transaction():
        row = await conn.fetchrow(
            """
            INSERT INTO scenarios (scenario_id, name, description, status, configuration, version)
            VALUES ($1, $2, $3, 'pending', $4, 1)
            RETURNING scenario_id, name, description, status, version, created_at
            """,
            scenario_id,
            req.name,
            req.description,
            json.dumps(config_json),
        )

        for si in req.scheduled_inputs:
            await conn.execute(
                """
                INSERT INTO scenario_scheduled_inputs
                    (id, scenario_id, step, input_type, input_data)
                VALUES ($1, $2, $3, $4, $5)
                """,
                str(uuid.uuid4()),
                scenario_id,
                si.step,
                si.input_type,
                json.dumps(si.input_data),
            )

    return _row_to_response(dict(row))


# ---------------------------------------------------------------------------
# GET /scenarios
# ---------------------------------------------------------------------------


@router.get("/scenarios", response_model=list[ScenarioResponse])
async def list_scenarios(
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> list[ScenarioResponse]:
    """Return all scenarios ordered by created_at descending."""
    rows = await conn.fetch(
        """
        SELECT scenario_id, name, description, status, version, created_at
        FROM scenarios
        ORDER BY created_at DESC
        """
    )
    return [_row_to_response(dict(row)) for row in rows]


# ---------------------------------------------------------------------------
# GET /scenarios/compare — ADR-004 Decision 5
# ---------------------------------------------------------------------------


def _compute_delta(value_a: str, value_b: str, tier_a: int, tier_b: int) -> DeltaRecord:
    from decimal import Decimal  # noqa: PLC0415

    dec_a = Decimal(value_a)
    dec_b = Decimal(value_b)
    delta = dec_b - dec_a
    if delta > 0:
        direction = "increase"
    elif delta < 0:
        direction = "decrease"
    else:
        direction = "unchanged"
    return DeltaRecord(
        value_a=value_a,
        value_b=value_b,
        delta=str(delta),
        direction=direction,
        confidence_tier=max(tier_a, tier_b),
    )


@router.get("/scenarios/compare", response_model=CompareResponse)
async def compare_scenarios(
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
    scenario_a: str,
    scenario_b: str,
    attr: str | None = None,
    step: int | None = None,
) -> CompareResponse:
    """Return attribute deltas between two scenarios.

    Computes delta = value_b - value_a for each shared entity and attribute.
    Only entities and attributes present in both snapshots are included.
    Filter to a single attribute with `attr`. ADR-004 Decision 5.

    `step` — when provided, both scenarios must have a snapshot at exactly
    that step. Returns 404 identifying which scenario is missing the step.
    When omitted, compares the final (highest-step) snapshot of each scenario.

    Returns 404 if either scenario is not found.
    Returns 404 if `step` is provided and either scenario has no snapshot at
    that step (with a message identifying the missing scenario).
    Returns 409 if `step` is omitted and either scenario has no snapshots yet.
    """
    for sid in (scenario_a, scenario_b):
        row = await conn.fetchrow(
            "SELECT scenario_id FROM scenarios WHERE scenario_id = $1", sid
        )
        if row is None:
            raise HTTPException(
                status_code=404, detail=f"Scenario '{sid}' not found."
            )

    if step is not None:
        snap_a = await conn.fetchrow(
            "SELECT step, state_data FROM scenario_state_snapshots "
            "WHERE scenario_id = $1 AND step = $2",
            scenario_a,
            step,
        )
        if snap_a is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Scenario '{scenario_a}' has no snapshot at step {step}. "
                    "Advance the scenario to this step before comparing."
                ),
            )
        snap_b = await conn.fetchrow(
            "SELECT step, state_data FROM scenario_state_snapshots "
            "WHERE scenario_id = $1 AND step = $2",
            scenario_b,
            step,
        )
        if snap_b is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Scenario '{scenario_b}' has no snapshot at step {step}. "
                    "Advance the scenario to this step before comparing."
                ),
            )
    else:
        snap_a = await conn.fetchrow(
            "SELECT step, state_data FROM scenario_state_snapshots "
            "WHERE scenario_id = $1 ORDER BY step DESC LIMIT 1",
            scenario_a,
        )
        snap_b = await conn.fetchrow(
            "SELECT step, state_data FROM scenario_state_snapshots "
            "WHERE scenario_id = $1 ORDER BY step DESC LIMIT 1",
            scenario_b,
        )
        if snap_a is None:
            raise HTTPException(
                status_code=409,
                detail=f"Scenario '{scenario_a}' has no snapshots. Run it first.",
            )
        if snap_b is None:
            raise HTTPException(
                status_code=409,
                detail=f"Scenario '{scenario_b}' has no snapshots. Run it first.",
            )

    state_a: dict[str, Any] = snap_a["state_data"]
    state_b: dict[str, Any] = snap_b["state_data"]
    if isinstance(state_a, str):
        state_a = json.loads(state_a)
    if isinstance(state_b, str):
        state_b = json.loads(state_b)

    shared_entities = set(state_a) & set(state_b)
    deltas: dict[str, dict[str, DeltaRecord]] = {}

    for eid in sorted(shared_entities):
        attrs_a: dict[str, Any] = state_a[eid]
        attrs_b: dict[str, Any] = state_b[eid]
        if not isinstance(attrs_a, dict) or not isinstance(attrs_b, dict):
            continue

        shared_attrs = set(attrs_a) & set(attrs_b)
        if attr is not None:
            shared_attrs = shared_attrs & {attr}

        entity_deltas: dict[str, DeltaRecord] = {}
        for key in sorted(shared_attrs):
            a_env = attrs_a[key]
            b_env = attrs_b[key]
            if not isinstance(a_env, dict) or not isinstance(b_env, dict):
                continue
            val_a = str(a_env.get("value", ""))
            val_b = str(b_env.get("value", ""))
            try:
                entity_deltas[key] = _compute_delta(
                    val_a,
                    val_b,
                    int(a_env.get("confidence_tier", 5)),
                    int(b_env.get("confidence_tier", 5)),
                )
            except Exception:  # noqa: BLE001 S112
                continue

        if entity_deltas:
            deltas[eid] = entity_deltas

    return CompareResponse(
        scenario_a_id=scenario_a,
        scenario_b_id=scenario_b,
        step_a=snap_a["step"],
        step_b=snap_b["step"],
        deltas=deltas,
    )


# ---------------------------------------------------------------------------
# GET /scenarios/{scenario_id}
# ---------------------------------------------------------------------------


@router.get("/scenarios/{scenario_id}", response_model=ScenarioDetailResponse)
async def get_scenario(
    scenario_id: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> ScenarioDetailResponse:
    """Return full scenario detail including configuration and scheduled inputs."""
    row = await conn.fetchrow(
        """
        SELECT scenario_id, name, description, status, version, created_at, configuration
        FROM scenarios
        WHERE scenario_id = $1
        """,
        scenario_id,
    )
    if row is None:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found.")

    input_rows = await conn.fetch(
        """
        SELECT step, input_type, input_data
        FROM scenario_scheduled_inputs
        WHERE scenario_id = $1
        ORDER BY step, created_at
        """,
        scenario_id,
    )
    return _build_detail_response(dict(row), [dict(r) for r in input_rows])


# ---------------------------------------------------------------------------
# DELETE /scenarios/{scenario_id}
# ---------------------------------------------------------------------------


@router.delete("/scenarios/{scenario_id}", status_code=204)
async def delete_scenario(
    scenario_id: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> Response:
    """Delete a scenario and all cascaded rows. Returns 204 No Content.

    Writes a tombstone to scenario_deleted_tombstones before the CASCADE
    executes. Tombstone and DELETE are in one transaction — atomic.
    ADR-004 Decision 1 Amendment (CONFLICT C-1 disposition).
    """
    async with conn.transaction():
        row = await conn.fetchrow(
            """
            SELECT scenario_id, name, configuration, created_at
            FROM scenarios
            WHERE scenario_id = $1
            """,
            scenario_id,
        )
        if row is None:
            raise HTTPException(
                status_code=404, detail=f"Scenario '{scenario_id}' not found."
            )

        cfg_raw = row["configuration"]
        if isinstance(cfg_raw, str):
            cfg_raw = json.loads(cfg_raw)

        input_rows = await conn.fetch(
            """
            SELECT step, input_type, input_data
            FROM scenario_scheduled_inputs
            WHERE scenario_id = $1
            ORDER BY step, created_at
            """,
            scenario_id,
        )
        scheduled_inputs_snap = [
            {
                "step": r["step"],
                "input_type": r["input_type"],
                "input_data": (
                    r["input_data"]
                    if isinstance(r["input_data"], dict)
                    else json.loads(r["input_data"])
                ),
            }
            for r in input_rows
        ]

        await conn.execute(
            """
            INSERT INTO scenario_deleted_tombstones
                (scenario_id, name, configuration, scheduled_inputs,
                 engine_version, original_created_at, deleted_at, deleted_by)
            VALUES ($1, $2, $3, $4, $5, $6, NOW(), $7)
            """,
            scenario_id,
            row["name"],
            json.dumps(cfg_raw),
            json.dumps(scheduled_inputs_snap),
            _ENGINE_VERSION,
            row["created_at"],
            "api",
        )

        await conn.execute(
            "DELETE FROM scenarios WHERE scenario_id = $1",
            scenario_id,
        )

    return Response(status_code=204)


# ---------------------------------------------------------------------------
# POST /scenarios/{scenario_id}/run
# ---------------------------------------------------------------------------


@router.post("/scenarios/{scenario_id}/run", response_model=RunSummaryResponse)
async def run_scenario(
    scenario_id: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> RunSummaryResponse:
    """Execute a pending scenario to completion.

    Validates that the scenario exists and is in 'pending' status.
    Returns 404 if not found, 409 if status is not pending.
    Delegates execution to WebScenarioRunner (ADR-004 Decision 2).
    Status transitions: pending → running → completed | failed.
    """
    status_row = await conn.fetchrow(
        "SELECT status FROM scenarios WHERE scenario_id = $1",
        scenario_id,
    )
    if status_row is None:
        raise HTTPException(
            status_code=404, detail=f"Scenario '{scenario_id}' not found."
        )
    if status_row["status"] != "pending":
        raise HTTPException(
            status_code=409,
            detail=(
                f"Scenario is in '{status_row['status']}' status. "
                "Only scenarios in 'pending' status can be run."
            ),
        )

    from app.simulation.web_scenario_runner import WebScenarioRunner  # noqa: PLC0415

    summary = await WebScenarioRunner().run(conn, scenario_id)
    return RunSummaryResponse(
        scenario_id=summary.scenario_id,
        steps_executed=summary.steps_executed,
        final_status=summary.final_status,
        duration_seconds=summary.duration_seconds,
    )


# ---------------------------------------------------------------------------
# POST /scenarios/{scenario_id}/advance — ADR-004 Decision 4
# ---------------------------------------------------------------------------


@router.post("/scenarios/{scenario_id}/advance", response_model=AdvanceResponse)
async def advance_scenario(
    scenario_id: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> AdvanceResponse:
    """Advance a scenario by exactly one simulation step.

    Executes the next pending step, writes a snapshot, and returns the step
    index and remaining steps. Returns 404 if scenario not found, 409 if
    already completed. ADR-004 Decision 4 — step-by-step advance pattern.
    """
    status_row = await conn.fetchrow(
        "SELECT status FROM scenarios WHERE scenario_id = $1",
        scenario_id,
    )
    if status_row is None:
        raise HTTPException(
            status_code=404, detail=f"Scenario '{scenario_id}' not found."
        )
    if status_row["status"] == "completed":
        raise HTTPException(
            status_code=409,
            detail=f"Scenario '{scenario_id}' is already completed. Cannot advance further.",
        )

    from app.simulation.web_scenario_runner import WebScenarioRunner  # noqa: PLC0415

    summary = await WebScenarioRunner().run_single_step(conn, scenario_id)
    return AdvanceResponse(
        scenario_id=summary.scenario_id,
        step_executed=summary.step_executed,
        steps_remaining=summary.steps_remaining,
        final_status=summary.final_status,
        is_complete=summary.is_complete,
    )


# ---------------------------------------------------------------------------
# GET /scenarios/{scenario_id}/snapshots — ADR-004 Decision 3
# ---------------------------------------------------------------------------


@router.get("/scenarios/{scenario_id}/snapshots", response_model=list[SnapshotRecord])
async def list_snapshots(
    scenario_id: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> list[SnapshotRecord]:
    """Return all snapshots for a scenario ordered by step ascending.

    Used by the backtesting test to evaluate fidelity thresholds against
    each simulated timestep's state_data. ADR-004 Decision 3.
    """
    scenario_row = await conn.fetchrow(
        "SELECT scenario_id FROM scenarios WHERE scenario_id = $1",
        scenario_id,
    )
    if scenario_row is None:
        raise HTTPException(
            status_code=404, detail=f"Scenario '{scenario_id}' not found."
        )

    rows = await conn.fetch(
        """
        SELECT scenario_id, step, timestep, state_data
        FROM scenario_state_snapshots
        WHERE scenario_id = $1
        ORDER BY step ASC
        """,
        scenario_id,
    )

    result = []
    for row in rows:
        state_raw = row["state_data"]
        if isinstance(state_raw, str):
            state_raw = json.loads(state_raw)
        state_dict: dict[str, Any] = state_raw if isinstance(state_raw, dict) else {}
        modules_active: list[str] = state_dict.get("_modules_active", [])
        if not isinstance(modules_active, list):
            modules_active = []
        timestep = row["timestep"]
        timestep_str = timestep.isoformat() if hasattr(timestep, "isoformat") else str(timestep)
        result.append(SnapshotRecord(
            scenario_id=row["scenario_id"],
            step=row["step"],
            timestep=timestep_str,
            state_data=state_dict,
            modules_active=modules_active,
        ))
    return result


# ---------------------------------------------------------------------------
# GET /scenarios/{scenario_id}/measurement-output — ADR-005 Decision 2
# ---------------------------------------------------------------------------

_UNIMPLEMENTED_FRAMEWORKS = {"ecological", "governance"}
_UNIMPLEMENTED_NOTES = {
    "ecological": "Ecological module not yet implemented — see module-capability-registry.md",
    "governance": "Governance module not yet implemented — see module-capability-registry.md",
}
_ALL_FRAMEWORKS = ["financial", "human_development", "ecological", "governance"]


def _parse_entity_attrs(
    state_dict: dict[str, Any],
) -> dict[str, dict[str, QuantitySchema]]:
    """Extract and parse all entity attribute dicts from a state_data snapshot.

    Skips metadata keys (underscore-prefixed) and non-dict values.
    Returns entity_id → {attr_key → QuantitySchema}.
    """
    result: dict[str, dict[str, QuantitySchema]] = {}
    for key, val in state_dict.items():
        if key.startswith("_") or not isinstance(val, dict):
            continue
        parsed: dict[str, QuantitySchema] = {}
        for attr_key, envelope in val.items():
            if isinstance(envelope, dict):
                with contextlib.suppress(Exception):
                    parsed[attr_key] = QuantitySchema.from_jsonb(envelope)
        result[key] = parsed
    return result


def _compute_composite_score(
    entity_indicators: dict[str, QuantitySchema],
    all_entity_attrs: dict[str, dict[str, QuantitySchema]],
    framework: str,
) -> str | None:
    """Mean percentile rank of entity indicators across all entities at this step.

    For each indicator, ranks the entity's value among all entities carrying
    that indicator in this framework. Returns str(Decimal) rounded to 4 decimal
    places, or None if no numeric indicators exist for this framework.
    ADR-005 Decision 2 §Composite score normalization.
    """
    if not entity_indicators:
        return None

    percentile_ranks: list[Decimal] = []
    for attr_key, target_qty in entity_indicators.items():
        try:
            target_val = Decimal(target_qty.value)
        except Exception:  # noqa: BLE001, S112
            continue

        all_vals: list[Decimal] = []
        for other_attrs in all_entity_attrs.values():
            qty = other_attrs.get(attr_key)
            if qty is not None and (qty.measurement_framework or "financial") == framework:
                with contextlib.suppress(Exception):
                    all_vals.append(Decimal(qty.value))

        if not all_vals:
            continue

        rank = Decimal(sum(1 for v in all_vals if v <= target_val)) / Decimal(len(all_vals))
        percentile_ranks.append(rank)

    if not percentile_ranks:
        return None

    score = sum(percentile_ranks) / Decimal(len(percentile_ranks))
    return str(score.quantize(Decimal("0.0001")))


def _alert_matches_framework(
    alert: MDAAlert,
    framework: str,
    target_attrs: dict[str, QuantitySchema],
) -> bool:
    """Return True if the alert's indicator belongs to the given framework.

    Looks up the indicator_key in target_attrs to find its measurement_framework
    tag. Untagged indicators fall into 'financial' per the backward-compatibility
    rule in CODING_STANDARDS.md §measurement_framework Tagging.
    """
    qty = target_attrs.get(alert.indicator_key)
    indicator_fw = (qty.measurement_framework or "financial") if qty is not None else "financial"
    return indicator_fw == framework


@router.get(
    "/scenarios/{scenario_id}/measurement-output",
    response_model=MultiFrameworkOutput,
)
async def get_measurement_output(
    scenario_id: str,
    entity_id: str,
    step: int,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> MultiFrameworkOutput:
    """Multi-framework measurement output for one entity at a given step.

    Groups the entity's attributes by measurement_framework tag. Attributes
    with no tag are classified as FINANCIAL (M1–M3 backward-compatibility rule,
    CODING_STANDARDS.md §measurement_framework Tagging). Composite scores are
    percentile-based across all entities present in the snapshot. ECOLOGICAL and
    GOVERNANCE return composite_score=null with a note until those modules are
    implemented. ia1_disclosure is always IA1_CANONICAL_PHRASE. ADR-005 Decision 2.

    Query params:
        step      — snapshot step index (required)
        entity_id — ISO 3166-1 alpha-3 entity identifier (required)
    """
    scenario_row = await conn.fetchrow(
        "SELECT scenario_id FROM scenarios WHERE scenario_id = $1",
        scenario_id,
    )
    if scenario_row is None:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found.")

    snap_row = await conn.fetchrow(
        """
        SELECT scenario_id, step, timestep, state_data, events_snapshot
        FROM scenario_state_snapshots
        WHERE scenario_id = $1 AND step = $2
        """,
        scenario_id,
        step,
    )
    if snap_row is None:
        raise HTTPException(
            status_code=404,
            detail=f"No snapshot at step {step} for scenario '{scenario_id}'.",
        )

    state_raw = snap_row["state_data"]
    if isinstance(state_raw, str):
        state_raw = json.loads(state_raw)
    state_dict: dict[str, Any] = state_raw if isinstance(state_raw, dict) else {}

    if entity_id not in state_dict:
        raise HTTPException(
            status_code=404,
            detail=f"Entity '{entity_id}' not found in snapshot at step {step}.",
        )

    entity_row = await conn.fetchrow(
        "SELECT metadata FROM simulation_entities WHERE entity_id = $1",
        entity_id,
    )
    metadata_str = entity_row["metadata"] if entity_row else None
    metadata_dict = json.loads(metadata_str) if metadata_str else {}
    entity_name: str = metadata_dict.get("name_en") or metadata_dict.get("name", entity_id)

    timestep = snap_row["timestep"]
    timestep_str: str = timestep.isoformat() if hasattr(timestep, "isoformat") else str(timestep)

    # Load MDA alerts from events_snapshot. Empty list for pre-M4 snapshots (events_snapshot=NULL).
    raw_events = snap_row["events_snapshot"]
    if raw_events is None:
        all_mda_alerts = []
    else:
        if isinstance(raw_events, str):
            raw_events = json.loads(raw_events)
        all_mda_alerts = alerts_from_events_snapshot(
            list(raw_events) if isinstance(raw_events, list) else [],
            entity_id=entity_id,
        )

    all_entity_attrs = _parse_entity_attrs(state_dict)
    target_attrs = all_entity_attrs.get(entity_id, {})

    outputs: dict[str, FrameworkOutput] = {}
    for fw in _ALL_FRAMEWORKS:
        fw_alerts = [a for a in all_mda_alerts if _alert_matches_framework(a, fw, target_attrs)]
        has_below_floor = any(
            a.consecutive_breach_steps >= 1 for a in fw_alerts
        )

        if fw in _UNIMPLEMENTED_FRAMEWORKS:
            outputs[fw] = FrameworkOutput(
                framework=fw,
                entity_id=entity_id,
                timestep=timestep_str,
                indicators={},
                composite_score=None,
                mda_alerts=fw_alerts,
                has_below_floor_indicator=has_below_floor,
                note=_UNIMPLEMENTED_NOTES[fw],
            )
            continue

        indicators = {
            k: v
            for k, v in target_attrs.items()
            if (v.measurement_framework or "financial") == fw
        }
        composite = _compute_composite_score(indicators, all_entity_attrs, fw)
        outputs[fw] = FrameworkOutput(
            framework=fw,
            entity_id=entity_id,
            timestep=timestep_str,
            indicators=indicators,
            composite_score=composite,
            mda_alerts=fw_alerts,
            has_below_floor_indicator=has_below_floor,
            note=None,
        )

    return MultiFrameworkOutput(
        entity_id=entity_id,
        entity_name=entity_name,
        timestep=timestep_str,
        scenario_id=scenario_id,
        step_index=step,
        outputs=outputs,
        ia1_disclosure=IA1_CANONICAL_PHRASE,
    )
