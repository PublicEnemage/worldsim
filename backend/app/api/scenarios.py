"""Scenario endpoints — ADR-004 Decision 1.

Four endpoints covering scenario configuration lifecycle:
  POST   /scenarios                — create scenario (status: pending)
  GET    /scenarios                — list all scenarios (created_at desc)
  GET    /scenarios/{scenario_id}  — full detail with scheduled inputs
  DELETE /scenarios/{scenario_id}  — delete + cascade, returns 204

Validation runs at creation time (structural) — entity existence check,
n_steps bounds, step index bounds, non-empty name. Semantic validation
of ControlInput payloads is deferred to execution (Issue #111).

All queries use asyncpg directly per ADR-003 Decision 2. Schema management
uses SQLAlchemy ORM via Alembic.
"""
from __future__ import annotations

import json
import uuid
from typing import Annotated, Any

import asyncpg  # noqa: TCH002 — used in Annotated[] resolved at runtime by FastAPI
from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.deps import get_db  # noqa: TCH001 — used as Depends(get_db) at runtime
from app.schemas import (
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScenarioDetailResponse,
    ScenarioResponse,
    ScheduledInputSchema,
)

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
    """Delete a scenario and all cascaded rows. Returns 204 No Content."""
    result = await conn.execute(
        "DELETE FROM scenarios WHERE scenario_id = $1",
        scenario_id,
    )
    # asyncpg returns 'DELETE N' — N=0 means row didn't exist
    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found.")
    return Response(status_code=204)
