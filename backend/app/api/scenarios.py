"""Scenario endpoints — ADR-004 Decisions 1 and 2.

Six endpoints covering scenario configuration lifecycle and execution:
  POST   /scenarios                        — create scenario (status: pending)
  GET    /scenarios                        — list all scenarios (created_at desc)
  GET    /scenarios/{scenario_id}          — full detail with scheduled inputs
  DELETE /scenarios/{scenario_id}          — tombstone + cascade delete, returns 204
  POST   /scenarios/{scenario_id}/run     — execute pending scenario to completion

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

import json
import uuid
from typing import Annotated, Any

import asyncpg  # noqa: TCH002 — used in Annotated[] resolved at runtime by FastAPI
from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.deps import get_db  # noqa: TCH001 — used as Depends(get_db) at runtime
from app.schemas import (
    RunSummaryResponse,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScenarioDetailResponse,
    ScenarioResponse,
    ScheduledInputSchema,
    SnapshotRecord,
)

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
        timestep = row["timestep"]
        timestep_str = timestep.isoformat() if hasattr(timestep, "isoformat") else str(timestep)
        result.append(SnapshotRecord(
            scenario_id=row["scenario_id"],
            step=row["step"],
            timestep=timestep_str,
            state_data=state_raw if isinstance(state_raw, dict) else {},
        ))
    return result
