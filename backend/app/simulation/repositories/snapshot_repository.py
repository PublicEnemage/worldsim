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
enforces this; application code cannot omit it. validate_ia1_disclosure() is
called at write time to guard against empty or whitespace-only strings that
would satisfy NOT NULL but provide no disclosure value (ARCH-REVIEW-003
BI3-I-01, Issue #144).

Envelope v2: state_data JSONB carries top-level _envelope_version = "2" and
_modules_active = [] (empty for M3; populated when M4 domain modules are active).
This allows API consumers to detect snapshot schema generation without content-
level parsing. See ARCH-REVIEW-003 BI3-I-02 and Issue #145.
"""
from __future__ import annotations

import json
import uuid
from typing import TYPE_CHECKING

import asyncpg  # noqa: TCH002 — used in method signatures at runtime

from app.simulation.repositories.quantity_serde import (
    IA1_CANONICAL_PHRASE,
    STATE_DATA_ENVELOPE_VERSION,
    quantity_to_jsonb_envelope,
    validate_ia1_disclosure,
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
        modules_active: list[str] | None = None,
        events_snapshot: list[dict[str, object]] | None = None,
    ) -> None:
        """Serialize SimulationState and insert a snapshot row.

        Args:
            conn: asyncpg connection. Not closed by this method.
            scenario_id: FK to scenarios.scenario_id.
            step: Step index (0 = initial state).
            timestep: Simulation time for this step.
            state: Full SimulationState at this step.
            modules_active: Names of domain modules that contributed to this
                snapshot. Empty list for M3 (no domain modules implemented).
                Populated in M4+ when DemographicModule and others are active.
            events_snapshot: MDA breach events for this step from MDAChecker.
                None (stored as SQL NULL) when no breaches occurred or at step 0.
        """
        disclosure = IA1_CANONICAL_PHRASE
        validate_ia1_disclosure(disclosure)
        state_data = _serialize_state(state, modules_active or [])
        events_json = json.dumps(events_snapshot) if events_snapshot is not None else None

        await conn.execute(
            """
            INSERT INTO scenario_state_snapshots
                (id, scenario_id, step, timestep, state_data, ia1_disclosure, events_snapshot)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (scenario_id, step) DO NOTHING
            """,
            str(uuid.uuid4()),
            scenario_id,
            step,
            timestep,
            json.dumps(state_data),
            disclosure,
            events_json,
        )


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _serialize_state(
    state: SimulationState,
    modules_active: list[str],
) -> dict[str, object]:
    """Serialize a SimulationState to the v2 state_data JSONB envelope format.

    Top-level keys:
      _envelope_version — STATE_DATA_ENVELOPE_VERSION ("2")
      _modules_active   — list of domain module names that contributed
      <entity_id>       — dict[attr_key → SA-09 Quantity envelope]

    Metadata keys use underscore prefix to distinguish them from entity IDs.
    The compare endpoint iterates entity IDs and skips non-dict values, so
    metadata keys are invisible to existing comparison logic.
    """
    data: dict[str, object] = {
        "_envelope_version": STATE_DATA_ENVELOPE_VERSION,
        "_modules_active": modules_active,
    }
    for entity_id, entity in state.entities.items():
        data[entity_id] = {
            attr_key: quantity_to_jsonb_envelope(qty)
            for attr_key, qty in entity.attributes.items()
        }
    return data
