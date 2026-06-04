"""
EmergencyPolicyInput → GovernanceModule event_type contract — Issue #642.

Root cause of NM-029: EmergencyPolicyInput.to_events() emits
  event_type = "emergency_policy_{instrument.value}"
GovernanceModule._SUBSCRIBED_EVENTS must contain the exact same strings.
25 unit tests passed with wrong synthetic event_type strings because no
test verified the adapter → subscriber contract end-to-end.

These tests cross the boundary: EmergencyPolicyInput produces an Event;
GovernanceModule receives it. The contract is structural — if the string
in to_events() diverges from _SUBSCRIBED_EVENTS, governance effects
silently disappear. This is the highest-severity near-miss class in the
engine: silent wrong result, not a crash.
"""
from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from app.simulation.engine.models import (
    MeasurementFramework,
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.engine.quantity import Quantity, VariableType
from app.simulation.modules.governance.module import _SUBSCRIBED_EVENTS, GovernanceModule
from app.simulation.orchestration.inputs import EmergencyInstrument, EmergencyPolicyInput

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_TIMESTEP = datetime(2001, 12, 19, tzinfo=UTC)


def _input(instrument: EmergencyInstrument) -> EmergencyPolicyInput:
    return EmergencyPolicyInput(
        target_entity="ARG",
        actor_id="test-actor",
        instrument=instrument,
        parameters={},
        expected_duration=1,
    )


def _state_with_events(events: list) -> SimulationState:  # type: ignore[type-arg]
    entity = SimulationEntity(
        id="ARG",
        entity_type="country",
        attributes={
            "democratic_quality_score": Quantity(
                value=Decimal("0.71"),
                unit="ratio_0_1",
                variable_type=VariableType.DIMENSIONLESS,
                measurement_framework=MeasurementFramework.GOVERNANCE,
                confidence_tier=1,
            ),
        },
        metadata={},
    )
    ts = _TIMESTEP
    return SimulationState(
        timestep=ts,
        resolution=ResolutionConfig(),
        entities={"ARG": entity},
        relationships=[],
        events=events,
        scenario_config=ScenarioConfig(
            scenario_id="test-sid",
            name="Test",
            description="",
            start_date=ts,
            end_date=ts,
        ),
    )


# ---------------------------------------------------------------------------
# Contract 1 — event_type strings produced by to_events()
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("instrument,expected_event_type", [
    (
        EmergencyInstrument.EMERGENCY_DECLARATION,
        "emergency_policy_emergency_declaration",
    ),
    (
        EmergencyInstrument.IMF_PROGRAM_ACCEPTANCE,
        "emergency_policy_imf_program_acceptance",
    ),
    (
        EmergencyInstrument.CAPITAL_CONTROLS,
        "emergency_policy_capital_controls",
    ),
])
def test_to_events_produces_correct_event_type(
    instrument: EmergencyInstrument,
    expected_event_type: str,
) -> None:
    """to_events() must produce event_type matching the documented pattern."""
    events = _input(instrument).to_events(_TIMESTEP)
    assert len(events) == 1
    assert events[0].event_type == expected_event_type


# ---------------------------------------------------------------------------
# Contract 2 — event_types in _SUBSCRIBED_EVENTS match what to_events() emits
# ---------------------------------------------------------------------------


def test_emergency_declaration_event_type_is_in_subscribed_events() -> None:
    """The event_type emitted for EMERGENCY_DECLARATION is subscribed by GovernanceModule."""
    events = _input(EmergencyInstrument.EMERGENCY_DECLARATION).to_events(_TIMESTEP)
    assert events[0].event_type in _SUBSCRIBED_EVENTS


def test_imf_program_acceptance_event_type_is_in_subscribed_events() -> None:
    """The event_type emitted for IMF_PROGRAM_ACCEPTANCE is subscribed by GovernanceModule."""
    events = _input(EmergencyInstrument.IMF_PROGRAM_ACCEPTANCE).to_events(_TIMESTEP)
    assert events[0].event_type in _SUBSCRIBED_EVENTS


# ---------------------------------------------------------------------------
# Contract 3 — GovernanceModule processes the event end-to-end
# ---------------------------------------------------------------------------


def test_governance_module_processes_emergency_declaration() -> None:
    """End-to-end: EmergencyPolicyInput event is processed by GovernanceModule.

    GovernanceModule.compute() must return a non-empty list of governance
    events when an emergency_declaration event is present in state.events.
    If the event_type contract breaks, compute() silently returns [].
    """
    emergency_events = _input(EmergencyInstrument.EMERGENCY_DECLARATION).to_events(_TIMESTEP)
    state = _state_with_events(emergency_events)
    entity = state.entities["ARG"]

    result = GovernanceModule().compute(entity, state, _TIMESTEP)

    assert result, (
        "GovernanceModule.compute() returned [] for an emergency_declaration event. "
        "Check that EmergencyPolicyInput.to_events() event_type matches "
        "_SUBSCRIBED_EVENTS in GovernanceModule."
    )


def test_governance_module_processes_imf_program_acceptance() -> None:
    """End-to-end: IMF_PROGRAM_ACCEPTANCE event is processed by GovernanceModule."""
    imf_events = _input(EmergencyInstrument.IMF_PROGRAM_ACCEPTANCE).to_events(_TIMESTEP)
    state = _state_with_events(imf_events)
    entity = state.entities["ARG"]

    result = GovernanceModule().compute(entity, state, _TIMESTEP)

    assert result, (
        "GovernanceModule.compute() returned [] for an imf_program_acceptance event. "
        "Check that EmergencyPolicyInput.to_events() event_type matches "
        "_SUBSCRIBED_EVENTS in GovernanceModule."
    )


def test_governance_module_ignores_unknown_event_type() -> None:
    """GovernanceModule must return [] for events not in _SUBSCRIBED_EVENTS.

    This is the inverse guard: if the subscription filter is broken and
    processes everything, this test will fail.
    """
    emergency_events = _input(EmergencyInstrument.EMERGENCY_DECLARATION).to_events(_TIMESTEP)
    # Corrupt the event_type to simulate the pre-NM-029 bug pattern
    broken_event = emergency_events[0]
    # bare name, not prefixed — simulates the pre-NM-029 bug pattern
    object.__setattr__(broken_event, "event_type", "emergency_declaration")

    state = _state_with_events([broken_event])
    entity = state.entities["ARG"]

    result = GovernanceModule().compute(entity, state, _TIMESTEP)

    assert result == [], (
        "GovernanceModule processed a bare 'emergency_declaration' event_type that is not "
        "in _SUBSCRIBED_EVENTS. The subscription filter is not enforced correctly."
    )


def test_get_subscribed_events_returns_all_emergency_types() -> None:
    """get_subscribed_events() must include all emergency event_types."""
    subscribed = GovernanceModule().get_subscribed_events()
    assert "emergency_policy_emergency_declaration" in subscribed
    assert "emergency_policy_imf_program_acceptance" in subscribed
