"""WebScenarioRunner — ADR-004 Decision 2.

Wraps the in-memory ScenarioRunner with database I/O. Loads scenario config and
initial state from PostGIS, executes the scenario step-by-step using the existing
ScenarioRunner.advance_timestep(), persists a snapshot after each step, and
updates scenario status throughout (SA-04 lifecycle state machine).

SA-04 status transitions enforced here:
  pending → running    (before execution begins)
  running → completed  (all steps finished without exception)
  running → failed     (any unhandled exception during execution)

Status is set to 'failed' and the exception is re-raised — never swallowed.

SA-11 determinism: same scenario_id, same DB state, same engine_version → identical
snapshot contents. The ScenarioRunner is deterministic (no random state). The base
timestep is derived from configuration; if absent, defaults to 2000-01-01 UTC.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING, Any

import asyncpg  # noqa: TCH002 — used in method signatures at runtime

from app.schemas import ScenarioConfigSchema
from app.simulation.orchestration.inputs import (
    EmergencyInstrument,
    EmergencyPolicyInput,
    FiscalInstrument,
    FiscalPolicyInput,
    InputSource,
    MonetaryRateInput,
    MonetaryRateInstrument,
    StructuralInstrument,
    StructuralPolicyInput,
    TradeInstrument,
    TradePolicyInput,
)
from app.simulation.orchestration.runner import ScenarioRunner
from app.simulation.repositories.quantity_serde import quantity_from_jsonb, quantity_from_schema
from app.simulation.repositories.snapshot_repository import ScenarioSnapshotRepository
from app.simulation.repositories.state_repository import (
    SimulationStateRepository,
    _default_timestep,
)

if TYPE_CHECKING:
    from datetime import datetime

    from app.simulation.engine.models import SimulationState
    from app.simulation.orchestration.inputs import ControlInput

# `datetime` and `SimulationState` above are annotation-only (PEP 563).
# `_reconstruct_state_from_snapshot` imports engine models locally at runtime.


# Engine version recorded in tombstone records.
_ENGINE_VERSION = "0.3.0"

# ---------------------------------------------------------------------------
# Return type
# ---------------------------------------------------------------------------


@dataclass
class RunSummary:
    """Result of a WebScenarioRunner.run() call."""

    scenario_id: str
    steps_executed: int
    final_status: str
    duration_seconds: float


@dataclass
class StepSummary:
    """Result of a WebScenarioRunner.run_single_step() call."""

    scenario_id: str
    step_executed: int
    steps_remaining: int
    final_status: str
    is_complete: bool


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------


class WebScenarioRunner:
    """Orchestrates scenario execution against the live database.

    Usage::

        runner = WebScenarioRunner()
        summary = await runner.run(conn, scenario_id)
    """

    async def run(
        self,
        conn: asyncpg.Connection,
        scenario_id: str,
    ) -> RunSummary:
        """Execute a pending scenario to completion.

        Loads scenario configuration, transitions status to 'running', executes
        all steps using ScenarioRunner.advance_timestep(), writes a snapshot after
        each step, then transitions to 'completed' (or 'failed' on exception).

        Args:
            conn: asyncpg connection. Caller owns the lifecycle.
            scenario_id: scenarios.scenario_id to execute.

        Returns:
            RunSummary with final status and timing.

        Raises:
            ValueError: If scenario not found or configuration is malformed.
            Any exception from the engine is re-raised after setting status=failed.
        """
        t_start = time.monotonic()

        # Load scenario configuration
        row = await conn.fetchrow(
            """
            SELECT scenario_id, name, status, configuration
            FROM scenarios
            WHERE scenario_id = $1
            """,
            scenario_id,
        )
        if row is None:
            raise ValueError(f"Scenario {scenario_id!r} not found.")

        cfg_raw = row["configuration"]
        if isinstance(cfg_raw, str):
            cfg_raw = json.loads(cfg_raw)
        config = ScenarioConfigSchema(**cfg_raw)

        # SA-04: pending → running (within transaction for atomicity)
        async with conn.transaction():
            await conn.execute(
                "UPDATE scenarios SET status = 'running', updated_at = NOW() "
                "WHERE scenario_id = $1",
                scenario_id,
            )

        try:
            return await self._execute(conn, scenario_id, row["name"], config, t_start)
        except Exception:
            # SA-04: running → failed — re-raise after marking status
            async with conn.transaction():
                await conn.execute(
                    "UPDATE scenarios SET status = 'failed', updated_at = NOW() "
                    "WHERE scenario_id = $1",
                    scenario_id,
                )
            raise

    async def run_single_step(
        self,
        conn: asyncpg.Connection,
        scenario_id: str,
    ) -> StepSummary:
        """Advance a scenario by exactly one simulation step.

        Loads the most recent snapshot to reconstruct state, applies scheduled
        inputs for the next step, advances one timestep, writes the new snapshot,
        and transitions status to 'completed' if the last step was just executed.

        Args:
            conn: asyncpg connection. Caller owns the lifecycle.
            scenario_id: scenarios.scenario_id to advance.

        Returns:
            StepSummary with step_executed, steps_remaining, and is_complete.

        Raises:
            ValueError: If scenario not found or is already completed.
        """
        row = await conn.fetchrow(
            "SELECT scenario_id, name, status, configuration FROM scenarios WHERE scenario_id = $1",
            scenario_id,
        )
        if row is None:
            raise ValueError(f"Scenario {scenario_id!r} not found.")

        if row["status"] == "completed":
            raise ValueError(
                f"Scenario {scenario_id!r} is already completed. Cannot advance further."
            )

        cfg_raw = row["configuration"]
        if isinstance(cfg_raw, str):
            cfg_raw = json.loads(cfg_raw)
        config = ScenarioConfigSchema(**cfg_raw)

        max_step_row = await conn.fetchrow(
            "SELECT MAX(step) AS max_step FROM scenario_state_snapshots WHERE scenario_id = $1",
            scenario_id,
        )
        current_step: int = (
            max_step_row["max_step"]
            if max_step_row and max_step_row["max_step"] is not None
            else -1
        )

        snap_repo = ScenarioSnapshotRepository()

        if current_step < 0:
            # No snapshots — initialise step 0 then advance to step 1
            base_timestep = _default_timestep()
            state_repo = SimulationStateRepository()
            current_state = await state_repo.load_initial_state(
                conn, config.entities, scenario_id, row["name"], base_timestep,
            )
            _apply_initial_overrides(current_state, config)
            await snap_repo.write_snapshot(conn, scenario_id, 0, base_timestep, current_state)
            current_step = 0

        else:
            snap_row = await conn.fetchrow(
                "SELECT timestep, state_data FROM scenario_state_snapshots "
                "WHERE scenario_id = $1 AND step = $2",
                scenario_id,
                current_step,
            )
            if snap_row is None:
                raise ValueError(
                    f"Snapshot for step {current_step} not found for scenario {scenario_id!r}."
                )
            state_raw = snap_row["state_data"]
            if isinstance(state_raw, str):
                state_raw = json.loads(state_raw)
            current_state = await _reconstruct_state_from_snapshot(
                conn, scenario_id, row["name"], state_raw, snap_row["timestep"],
            )

        next_step = current_step + 1
        if next_step > config.n_steps:
            raise ValueError(
                f"Scenario {scenario_id!r} has already executed all {config.n_steps} steps."
            )

        # SA-04: pending → running (only if currently pending)
        async with conn.transaction():
            await conn.execute(
                "UPDATE scenarios SET status = 'running', updated_at = NOW() "
                "WHERE scenario_id = $1 AND status = 'pending'",
                scenario_id,
            )

        try:
            inputs_by_step = await _load_scheduled_inputs(conn, scenario_id, config.entities)
            step_inputs = inputs_by_step.get(next_step, [])

            runner = ScenarioRunner(
                initial_state=current_state,
                scheduled_inputs=[],
                modules=[],
                n_steps=config.n_steps,
            )
            new_state = runner.advance_timestep(
                current_state=current_state,
                modules=[],
                scheduled_inputs=step_inputs,
            )
            await snap_repo.write_snapshot(
                conn, scenario_id, next_step, new_state.timestep, new_state
            )

            steps_remaining = config.n_steps - next_step
            is_complete = steps_remaining == 0
            final_status = "completed" if is_complete else "running"

            if is_complete:
                async with conn.transaction():
                    await conn.execute(
                        "UPDATE scenarios SET status = 'completed', updated_at = NOW() "
                        "WHERE scenario_id = $1",
                        scenario_id,
                    )

            return StepSummary(
                scenario_id=scenario_id,
                step_executed=next_step,
                steps_remaining=steps_remaining,
                final_status=final_status,
                is_complete=is_complete,
            )
        except Exception:
            async with conn.transaction():
                await conn.execute(
                    "UPDATE scenarios SET status = 'failed', updated_at = NOW() "
                    "WHERE scenario_id = $1",
                    scenario_id,
                )
            raise

    async def _execute(
        self,
        conn: asyncpg.Connection,
        scenario_id: str,
        scenario_name: str,
        config: ScenarioConfigSchema,
        t_start: float,
    ) -> RunSummary:
        """Inner execution: load state, run steps, write snapshots."""
        base_timestep = _default_timestep()
        state_repo = SimulationStateRepository()
        snap_repo = ScenarioSnapshotRepository()

        # Load initial state from simulation_entities
        initial_state = await state_repo.load_initial_state(
            conn,
            config.entities,
            scenario_id,
            scenario_name,
            base_timestep,
        )

        # Apply initial_attributes overrides from scenario config
        _apply_initial_overrides(initial_state, config)

        # Load scheduled inputs grouped by step
        inputs_by_step = await _load_scheduled_inputs(conn, scenario_id, config.entities)

        # Write step-0 snapshot (initial state)
        await snap_repo.write_snapshot(conn, scenario_id, 0, base_timestep, initial_state)

        # Execute n_steps using ScenarioRunner
        runner = ScenarioRunner(
            initial_state=initial_state,
            scheduled_inputs=[],
            modules=[],
            n_steps=config.n_steps,
        )

        current_state = initial_state
        for step_num in range(1, config.n_steps + 1):
            step_inputs = inputs_by_step.get(step_num, [])
            current_state = runner.advance_timestep(
                current_state=current_state,
                modules=[],
                scheduled_inputs=step_inputs,
            )
            await snap_repo.write_snapshot(
                conn, scenario_id, step_num, current_state.timestep, current_state
            )

        # SA-04: running → completed
        async with conn.transaction():
            await conn.execute(
                "UPDATE scenarios SET status = 'completed', updated_at = NOW() "
                "WHERE scenario_id = $1",
                scenario_id,
            )

        return RunSummary(
            scenario_id=scenario_id,
            steps_executed=config.n_steps,
            final_status="completed",
            duration_seconds=round(time.monotonic() - t_start, 3),
        )


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _apply_initial_overrides(
    state: SimulationState,
    config: ScenarioConfigSchema,
) -> None:
    """Apply initial_attributes overrides from scenario config onto loaded entities."""
    for entity_id, attr_overrides in config.initial_attributes.items():
        entity = state.entities.get(entity_id)
        if entity is None:
            continue
        for attr_key, qty_schema in attr_overrides.items():
            entity.set_attribute(attr_key, quantity_from_schema(qty_schema))


async def _load_scheduled_inputs(
    conn: asyncpg.Connection,
    scenario_id: str,
    entity_ids: list[str],
) -> dict[int, list[ControlInput]]:
    """Load and deserialize scheduled inputs grouped by step number."""
    rows = await conn.fetch(
        """
        SELECT step, input_type, input_data
        FROM scenario_scheduled_inputs
        WHERE scenario_id = $1
        ORDER BY step, created_at
        """,
        scenario_id,
    )

    inputs_by_step: dict[int, list[ControlInput]] = {}
    for row in rows:
        idata = row["input_data"]
        if isinstance(idata, str):
            idata = json.loads(idata)
        ctrl = _deserialize_control_input(row["input_type"], idata, entity_ids)
        inputs_by_step.setdefault(row["step"], []).append(ctrl)

    return inputs_by_step


def _deserialize_control_input(
    input_type: str,
    data: dict[str, Any],
    entity_ids: list[str],
) -> ControlInput:
    """Deserialize a JSONB input_data dict to the appropriate ControlInput subclass.

    The input_data format is the user-provided dict from ScheduledInputSchema.input_data,
    not the full dataclasses.asdict() serialization. Only the type-specific fields
    need to be present; base ControlInput fields default to safe values.

    target_entity defaults to the first entity in the scenario's entity list if
    not explicitly set in input_data.
    """
    default_target = entity_ids[0] if entity_ids else ""
    target_entity = str(data.get("target_entity", default_target))

    if input_type == "FiscalPolicyInput":
        return FiscalPolicyInput(
            target_entity=target_entity,
            instrument=FiscalInstrument(data["instrument"]),
            sector=str(data.get("sector", "")),
            value=Decimal(str(data.get("value", "0"))),
            duration_years=int(data.get("duration_years", 1)),
            source=InputSource.SCENARIO_SCRIPT,
        )
    if input_type == "EmergencyPolicyInput":
        return EmergencyPolicyInput(
            target_entity=target_entity,
            instrument=EmergencyInstrument(data["instrument"]),
            parameters={k: v for k, v in data.items() if k not in {"instrument", "target_entity"}},
            expected_duration=int(data.get("expected_duration", 1)),
            source=InputSource.SCENARIO_SCRIPT,
        )
    if input_type == "TradePolicyInput":
        return TradePolicyInput(
            target_entity=target_entity,
            instrument=TradeInstrument(data["instrument"]),
            source_entity=str(data.get("source_entity", default_target)),
            affected_sector=str(data.get("affected_sector", "")),
            value=Decimal(str(data.get("value", "0"))),
            retaliation_modeled=bool(data.get("retaliation_modeled", False)),
            source=InputSource.SCENARIO_SCRIPT,
        )
    if input_type == "MonetaryRateInput":
        return MonetaryRateInput(
            target_entity=target_entity,
            instrument=MonetaryRateInstrument(data["instrument"]),
            value=Decimal(str(data.get("value", "0"))),
            duration_periods=int(data.get("duration_periods", 1)),
            source=InputSource.SCENARIO_SCRIPT,
        )
    if input_type == "StructuralPolicyInput":
        return StructuralPolicyInput(
            target_entity=target_entity,
            instrument=StructuralInstrument(data["instrument"]),
            affected_sector=str(data.get("affected_sector", "")),
            parameters={k: v for k, v in data.items()
                        if k not in {"instrument", "target_entity", "affected_sector"}},
            implementation_years=int(data.get("implementation_years", 1)),
            source=InputSource.SCENARIO_SCRIPT,
        )
    raise ValueError(
        f"Unknown ControlInput type: {input_type!r}. "
        "Supported: FiscalPolicyInput, EmergencyPolicyInput, TradePolicyInput, "
        "MonetaryRateInput, StructuralPolicyInput."
    )


async def _reconstruct_state_from_snapshot(
    conn: asyncpg.Connection,
    scenario_id: str,
    scenario_name: str,
    state_data: dict[str, Any],
    timestep: datetime,
) -> SimulationState:
    """Rebuild a SimulationState from a snapshot's state_data dict.

    Fetches entity_type and metadata from simulation_entities; attribute values
    come from the snapshot state_data (SA-09 envelope format).
    """
    from app.simulation.engine.models import (  # noqa: PLC0415
        ResolutionConfig,
        ScenarioConfig,
        SimulationEntity,
        SimulationState,
    )

    entity_ids = list(state_data.keys())
    rows = await conn.fetch(
        "SELECT entity_id, entity_type, metadata FROM simulation_entities "
        "WHERE entity_id = ANY($1::text[])",
        entity_ids,
    )
    entity_meta = {row["entity_id"]: row for row in rows}

    entities: dict[str, SimulationEntity] = {}
    for entity_id, attr_data in state_data.items():
        meta_row = entity_meta.get(entity_id)
        if meta_row is None:
            continue
        meta_raw = meta_row["metadata"] or {}
        if isinstance(meta_raw, str):
            meta_raw = json.loads(meta_raw)

        attributes = {}
        if isinstance(attr_data, dict):
            import contextlib  # noqa: PLC0415

            for attr_key, envelope in attr_data.items():
                if isinstance(envelope, dict):
                    with contextlib.suppress(ValueError, KeyError):
                        attributes[attr_key] = quantity_from_jsonb(envelope)

        entities[entity_id] = SimulationEntity(
            id=entity_id,
            entity_type=meta_row["entity_type"],
            attributes=attributes,
            metadata=meta_raw,
        )

    scenario_cfg = ScenarioConfig(
        scenario_id=scenario_id,
        name=scenario_name,
        description="",
        start_date=timestep,
        end_date=timestep,
    )

    return SimulationState(
        timestep=timestep,
        resolution=ResolutionConfig(),
        entities=entities,
        relationships=[],
        events=[],
        scenario_config=scenario_cfg,
    )
