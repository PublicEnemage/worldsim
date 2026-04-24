"""ScenarioSnapshotRepository — writes simulation state snapshots to PostGIS.

ADR-004 Decision 2. After each timestep, the WebScenarioRunner calls write_snapshot()
to persist the full SimulationState as JSONB in scenario_state_snapshots.

SA-12 compliance: every Quantity stored here must round-trip through
QuantitySchema.from_jsonb() → quantity_from_schema() without data loss.
The round-trip test in test_web_scenario_runner.py verifies this contract.

SA-09 compliance: all Quantity values use the canonical envelope format
(quantity_to_jsonb_envelope) with _envelope_version = "1".

IA-1 compliance: every snapshot row carries IA1_CANONICAL_PHRASE verbatim
in ia1_disclosure. The column is NOT NULL with no server default — the DB
enforces this; application code cannot omit it.
"""
from __future__ import annotations

import json
import uuid
from typing import TYPE_CHECKING

import asyncpg  # noqa: TCH002 — used in method signatures at runtime

from app.simulation.repositories.quantity_serde import (
    IA1_CANONICAL_PHRASE,
    quantity_to_jsonb_envelope,
)

if TYPE_CHECKING:
    from datetime import datetime

    from app.simulation.engine.models import SimulationState


class ScenarioSnapshotRepository:
    """Writes simulation step snapshots to scenario_state_snapshots.

    Each call to write_snapshot() inserts one row. The ON CONFLICT DO NOTHING
    clause makes writes idempotent — re-running a step that already has a
    snapshot is safe (the existing snapshot is preserved).
    """

    async def write_snapshot(
        self,
        conn: asyncpg.Connection,
        scenario_id: str,
        step: int,
        timestep: datetime,
        state: SimulationState,
    ) -> None:
        """Serialize SimulationState and insert a snapshot row.

        Args:
            conn: asyncpg connection. Not closed by this method.
            scenario_id: FK to scenarios.scenario_id.
            step: Step index (0 = initial state).
            timestep: Simulation time for this step.
            state: Full SimulationState at this step.
        """
        state_data = _serialize_state(state)

        await conn.execute(
            """
            INSERT INTO scenario_state_snapshots
                (id, scenario_id, step, timestep, state_data, ia1_disclosure)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (scenario_id, step) DO NOTHING
            """,
            str(uuid.uuid4()),
            scenario_id,
            step,
            timestep,
            json.dumps(state_data),
            IA1_CANONICAL_PHRASE,
        )


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _serialize_state(state: SimulationState) -> dict[str, dict[str, object]]:
    """Serialize a SimulationState to the JSONB envelope format.

    Returns Dict[entity_id → Dict[attr_key → envelope_dict]] where each
    envelope_dict follows the SA-09 Quantity JSONB Envelope Format.
    """
    return {
        entity_id: {
            attr_key: quantity_to_jsonb_envelope(qty)
            for attr_key, qty in entity.attributes.items()
        }
        for entity_id, entity in state.entities.items()
    }
