"""Unit tests for duplicate event_id detection warning in ScenarioRunner.

Issue #223: advance_timestep() should log a WARNING when two events with the
same event_id are present before propagation, since duplicate event_ids cause
both deltas to be applied, silently doubling the effect.

The guard is a WARNING, not an exception, so the simulation continues and the
full duplicate pattern remains observable.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationModule,
    SimulationState,
)
from app.simulation.engine.quantity import Quantity, VariableType
from app.simulation.orchestration.runner import ScenarioRunner

_BASE_DATE = datetime(2025, 1, 1)
_RUNNER_LOGGER = "app.simulation.orchestration.runner"
_DUPLICATE_ID = "duplicate-event-id-sentinel"


def _q(value: float = 0.0) -> Quantity:
    return Quantity(
        value=Decimal(str(value)),
        unit="dimensionless",
        variable_type=VariableType.RATIO,
    )


def _entity(entity_id: str, **attributes: float) -> SimulationEntity:
    return SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes={k: _q(v) for k, v in attributes.items()},
        metadata={},
    )


def _state(entities: dict[str, SimulationEntity] | None = None) -> SimulationState:
    return SimulationState(
        timestep=_BASE_DATE,
        resolution=ResolutionConfig(),
        entities=entities or {},
        relationships=[],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="TEST",
            name="Test",
            description="",
            start_date=_BASE_DATE,
            end_date=_BASE_DATE + timedelta(days=3650),
        ),
    )


class _FixedIdModule(SimulationModule):
    """Always emits an event with the same fixed event_id regardless of entity."""

    def compute(
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime,
    ) -> list[Event]:
        return [
            Event(
                event_id=_DUPLICATE_ID,
                source_entity_id=entity.id,
                event_type="test_duplicate",
                affected_attributes={},
                propagation_rules=[],
                timestep_originated=timestep,
                framework=MeasurementFramework.FINANCIAL,
            )
        ]

    def get_subscribed_events(self) -> list[str]:
        return []


class _UniqueIdModule(SimulationModule):
    """Emits an event with an entity-scoped unique event_id — no duplicates."""

    def compute(
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime,
    ) -> list[Event]:
        return [
            Event(
                event_id=f"unique-{entity.id}-{timestep.isoformat()}",
                source_entity_id=entity.id,
                event_type="test_unique",
                affected_attributes={},
                propagation_rules=[],
                timestep_originated=timestep,
                framework=MeasurementFramework.FINANCIAL,
            )
        ]

    def get_subscribed_events(self) -> list[str]:
        return []


# ---------------------------------------------------------------------------
# Duplicate warning fires
# ---------------------------------------------------------------------------


def test_duplicate_event_id_warning_fires(caplog: pytest.LogCaptureFixture) -> None:
    """Two entities running _FixedIdModule produce the same event_id; warning must fire."""
    state = _state(entities={"A": _entity("A"), "B": _entity("B")})
    runner = ScenarioRunner(
        initial_state=state,
        scheduled_inputs=[],
        modules=[_FixedIdModule()],
        n_steps=1,
    )
    with caplog.at_level(logging.WARNING, logger=_RUNNER_LOGGER):
        runner.run()

    warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert warnings, "Expected at least one WARNING but got none"
    assert any("Duplicate event_id" in r.message for r in warnings), (
        f"Warning text must contain 'Duplicate event_id'. Got: {[r.message for r in warnings]}"
    )


def test_duplicate_event_id_warning_names_the_event_id(caplog: pytest.LogCaptureFixture) -> None:
    """The warning message must include the actual duplicate event_id."""
    state = _state(entities={"A": _entity("A"), "B": _entity("B")})
    runner = ScenarioRunner(
        initial_state=state,
        scheduled_inputs=[],
        modules=[_FixedIdModule()],
        n_steps=1,
    )
    with caplog.at_level(logging.WARNING, logger=_RUNNER_LOGGER):
        runner.run()

    all_text = " ".join(r.getMessage() for r in caplog.records if r.levelno == logging.WARNING)
    assert _DUPLICATE_ID in all_text, (
        f"Warning must name the duplicate event_id '{_DUPLICATE_ID}'. Got: {all_text!r}"
    )


def test_unique_event_ids_produce_no_warning(caplog: pytest.LogCaptureFixture) -> None:
    """When each entity emits a uniquely-scoped event_id, no warning is logged."""
    state = _state(entities={"A": _entity("A"), "B": _entity("B")})
    runner = ScenarioRunner(
        initial_state=state,
        scheduled_inputs=[],
        modules=[_UniqueIdModule()],
        n_steps=1,
    )
    with caplog.at_level(logging.WARNING, logger=_RUNNER_LOGGER):
        runner.run()

    warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert not warnings, f"Expected no warnings but got: {[r.message for r in warnings]}"


def test_no_entities_produces_no_warning(caplog: pytest.LogCaptureFixture) -> None:
    """A step with no entities and no inputs produces no warnings."""
    runner = ScenarioRunner(
        initial_state=_state(entities={}),
        scheduled_inputs=[],
        modules=[_FixedIdModule()],
        n_steps=1,
    )
    with caplog.at_level(logging.WARNING, logger=_RUNNER_LOGGER):
        runner.run()

    warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert not warnings


def test_simulation_continues_after_duplicate_warning(caplog: pytest.LogCaptureFixture) -> None:
    """The simulation must not raise an exception on duplicate event_ids — warning only."""
    state = _state(entities={"A": _entity("A"), "B": _entity("B")})
    runner = ScenarioRunner(
        initial_state=state,
        scheduled_inputs=[],
        modules=[_FixedIdModule()],
        n_steps=3,
    )
    with caplog.at_level(logging.WARNING, logger=_RUNNER_LOGGER):
        history = runner.run()

    assert len(history) == 4  # 3 steps + initial state — no exception raised


def test_duplicate_warning_fires_once_per_duplicate(caplog: pytest.LogCaptureFixture) -> None:
    """Each duplicate pair generates exactly one warning per step."""
    state = _state(entities={"A": _entity("A"), "B": _entity("B")})
    runner = ScenarioRunner(
        initial_state=state,
        scheduled_inputs=[],
        modules=[_FixedIdModule()],
        n_steps=1,
    )
    with caplog.at_level(logging.WARNING, logger=_RUNNER_LOGGER):
        runner.run()

    duplicate_warnings = [
        r for r in caplog.records
        if r.levelno == logging.WARNING and "Duplicate event_id" in r.message
    ]
    assert len(duplicate_warnings) == 1, (
        f"Expected exactly 1 warning for one duplicate pair, got {len(duplicate_warnings)}"
    )
