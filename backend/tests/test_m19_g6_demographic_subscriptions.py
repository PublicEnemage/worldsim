"""QA tests for #1657: DemographicModule dead subscription strings + elasticity rows.

RED-before-implementation tests (flip GREEN when #1657 impl PR merges):
  - test_subscribed_events_no_dead_bare_strings: currently "imf_program_acceptance"
    and "emergency_declaration" (bare) are in _SUBSCRIBED_EVENTS — should NOT be.
  - test_subscribed_events_has_prefixed_imf_string: "emergency_policy_imf_program_acceptance"
    not yet in _SUBSCRIBED_EVENTS (it is the bare string instead).
  - test_subscribed_events_has_prefixed_emergency_declaration_string: same for emergency.
  - test_imf_program_acceptance_triggers_q1_informal_delta: no elasticity row + dead string.
  - test_imf_program_acceptance_triggers_q2_informal_delta: same.
  - test_emergency_declaration_triggers_q1_informal_delta: same.
  - test_emergency_declaration_triggers_q2_informal_delta: same.

GREEN before implementation (value / type guards; will remain GREEN after):
  - test_imf_program_acceptance_delta_is_positive
  - test_emergency_declaration_delta_is_positive

CM cert: issue #1657 comment 2026-07-04 — values certified by Chief Methodologist.
NM-084 gate satisfied.
"""
from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from app.simulation.modules.demographic.cohort import (
    AgeBand,
    CohortSpec,
    EmploymentSector,
    IncomeQuintile,
)
from app.simulation.modules.demographic.module import DemographicModule

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_state(entity_id: str, prior_events: list) -> object:
    from app.simulation.engine.models import (
        ResolutionConfig,
        ScenarioConfig,
        SimulationEntity,
        SimulationState,
    )

    ts = datetime(2020, 1, 1, tzinfo=UTC)
    return SimulationState(
        timestep=ts,
        resolution=ResolutionConfig(),
        entities={
            entity_id: SimulationEntity(
                id=entity_id,
                entity_type="country",
                attributes={},
                metadata={},
            )
        },
        relationships=[],
        events=prior_events,
        scenario_config=ScenarioConfig(
            scenario_id="test-1657",
            name="Test #1657",
            description="",
            start_date=ts,
            end_date=ts,
        ),
    )


def _emergency_policy_event(
    entity_id: str, instrument_value: str, magnitude: float = 1.0
) -> object:
    """Build an emergency policy Event as EmergencyPolicyInput.to_events() would emit it.

    event_type = f"emergency_policy_{instrument_value}"
    affected_attributes = {instrument_value: Quantity(magnitude)}
    """
    from app.simulation.engine.models import Event, MeasurementFramework
    from app.simulation.engine.quantity import Quantity, VariableType

    ts = datetime(2020, 1, 1, tzinfo=UTC)
    delta = Quantity(
        value=Decimal(str(magnitude)),
        unit="dimensionless",
        variable_type=VariableType.DIMENSIONLESS,
        measurement_framework=MeasurementFramework.GOVERNANCE,
        confidence_tier=1,
    )
    return Event(
        event_id=f"test-{instrument_value}-event",
        source_entity_id=entity_id,
        event_type=f"emergency_policy_{instrument_value}",
        affected_attributes={instrument_value: delta},
        propagation_rules=[],
        timestep_originated=ts,
        framework=MeasurementFramework.GOVERNANCE,
    )


def _run_module(entity_id: str, event: object) -> list:
    state = _make_state(entity_id, [event])
    module = DemographicModule(cohort_resolution_entity_ids=[entity_id])
    entity = state.entities[entity_id]
    ts = datetime(2020, 4, 1, tzinfo=UTC)
    return module.compute(entity, state, ts)


def _delta_for_cohort(events: list, entity_id: str, cohort_spec: CohortSpec) -> Decimal | None:
    """Return the poverty_headcount_ratio delta for the given cohort, or None."""
    target_id = cohort_spec.entity_id(entity_id)
    for event in events:
        if event.metadata.get("target_entity_id") == target_id:
            qty = event.affected_attributes.get("poverty_headcount_ratio")
            if qty is not None:
                return qty.value
    return None


Q1_INFORMAL = CohortSpec(IncomeQuintile.Q1, AgeBand.AGE_25_54, EmploymentSector.INFORMAL)
Q2_INFORMAL = CohortSpec(IncomeQuintile.Q2, AgeBand.AGE_25_54, EmploymentSector.INFORMAL)
ENTITY = "ZMB"


# ---------------------------------------------------------------------------
# AC-S1: Subscription string correctness
# RED before #1657: bare strings "imf_program_acceptance" and
# "emergency_declaration" are present; prefixed strings are absent.
# ---------------------------------------------------------------------------


def test_subscribed_events_has_prefixed_imf_string() -> None:
    """'emergency_policy_imf_program_acceptance' must be in subscribed events.

    RED before #1657: only 'imf_program_acceptance' (bare) is present.
    """
    subscribed = DemographicModule().get_subscribed_events()
    assert "emergency_policy_imf_program_acceptance" in subscribed, (
        "DemographicModule must subscribe to 'emergency_policy_imf_program_acceptance' — "
        "the correct event_type emitted by EmergencyPolicyInput for IMF_PROGRAM_ACCEPTANCE. "
        "Currently the bare string 'imf_program_acceptance' is used, which is a dead subscription."
    )


def test_subscribed_events_has_prefixed_emergency_declaration_string() -> None:
    """'emergency_policy_emergency_declaration' must be in subscribed events.

    RED before #1657: only 'emergency_declaration' (bare) is present.
    """
    subscribed = DemographicModule().get_subscribed_events()
    assert "emergency_policy_emergency_declaration" in subscribed, (
        "DemographicModule must subscribe to 'emergency_policy_emergency_declaration' — "
        "the correct event_type emitted by EmergencyPolicyInput for EMERGENCY_DECLARATION. "
        "Currently the bare string 'emergency_declaration' is used, which is a dead subscription."
    )


def test_subscribed_events_no_dead_bare_strings() -> None:
    """Bare 'imf_program_acceptance' and 'emergency_declaration' must NOT be subscribed.

    RED before #1657: both bare strings are in _SUBSCRIBED_EVENTS.
    """
    subscribed = set(DemographicModule().get_subscribed_events())
    assert "imf_program_acceptance" not in subscribed, (
        "'imf_program_acceptance' is a dead subscription string — "
        "EmergencyPolicyInput emits 'emergency_policy_imf_program_acceptance'. "
        "Remove the bare string and replace with the prefixed form."
    )
    assert "emergency_declaration" not in subscribed, (
        "'emergency_declaration' is a dead subscription string — "
        "EmergencyPolicyInput emits 'emergency_policy_emergency_declaration'. "
        "Remove the bare string and replace with the prefixed form."
    )


# ---------------------------------------------------------------------------
# AC-S2: IMF programme acceptance → Q1/Q2 INFORMAL poverty headcount delta
# CM cert: +0.04 (Q1), +0.02 (Q2); entity_families=None; T3.
# RED before #1657: no elasticity row + dead subscription string.
# ---------------------------------------------------------------------------


def test_imf_program_acceptance_triggers_q1_informal_delta() -> None:
    """emergency_policy_imf_program_acceptance must raise Q1 INFORMAL PHC by 0.04.

    CM cert 2026-07-04 (issue #1657 comment): IMF IEO (2018) mid-range 3–5pp
    Q1 informal PHC increase → +0.04 per acceptance event (magnitude=1.0).
    """
    event = _emergency_policy_event(ENTITY, "imf_program_acceptance")
    events = _run_module(ENTITY, event)
    delta = _delta_for_cohort(events, ENTITY, Q1_INFORMAL)
    assert delta is not None, (
        "No poverty_headcount_ratio delta produced for Q1 INFORMAL on "
        "emergency_policy_imf_program_acceptance. Add the elasticity row (φ=+0.04) "
        "to ELASTICITY_REGISTRY and fix the subscription string."
    )
    assert delta == Decimal("0.04"), (
        f"Expected Q1 INFORMAL delta = +0.04 (CM cert: IMF IEO 2018 mid-range); got {delta}."
    )


def test_imf_program_acceptance_triggers_q2_informal_delta() -> None:
    """emergency_policy_imf_program_acceptance must raise Q2 INFORMAL PHC by 0.02.

    CM cert 2026-07-04: Ball et al. (2013) 0.60 scaling of Q1: 0.60 × 0.04 = 0.024 → +0.02.
    """
    event = _emergency_policy_event(ENTITY, "imf_program_acceptance")
    events = _run_module(ENTITY, event)
    delta = _delta_for_cohort(events, ENTITY, Q2_INFORMAL)
    assert delta is not None, (
        "No poverty_headcount_ratio delta for Q2 INFORMAL on "
        "emergency_policy_imf_program_acceptance. Add Q2 INFORMAL elasticity row (φ=+0.02)."
    )
    assert delta == Decimal("0.02"), (
        f"Expected Q2 INFORMAL delta = +0.02 (Ball 2013 0.60 scaling); got {delta}."
    )


def test_imf_program_acceptance_delta_is_positive() -> None:
    """IMF programme acceptance must raise (not lower) Q1 informal poverty headcount.

    Sign guard: conditionality channel raises PHC; negative elasticity would be wrong.
    GREEN both before and after #1657 (verifies sign once row is present).
    """
    event = _emergency_policy_event(ENTITY, "imf_program_acceptance")
    events = _run_module(ENTITY, event)
    delta = _delta_for_cohort(events, ENTITY, Q1_INFORMAL)
    if delta is None:
        pytest.skip("No elasticity row yet — sign guard fires after row is added.")
    assert delta > Decimal("0"), (
        f"IMF programme acceptance must increase Q1 informal PHC (δ > 0); got {delta}."
    )


# ---------------------------------------------------------------------------
# AC-S3: Emergency declaration → Q1/Q2 INFORMAL poverty headcount delta
# CM cert: +0.06 (Q1), +0.04 (Q2); entity_families=None; T3.
# RED before #1657: no elasticity row + dead subscription string.
# ---------------------------------------------------------------------------


def test_emergency_declaration_triggers_q1_informal_delta() -> None:
    """emergency_policy_emergency_declaration must raise Q1 INFORMAL PHC by 0.06.

    CM cert 2026-07-04: ILO (2020) 20–25% informal employment contraction → +0.06
    per declaration (magnitude=1.0). Direct disruption channel, not GDP-mediated.
    """
    event = _emergency_policy_event(ENTITY, "emergency_declaration")
    events = _run_module(ENTITY, event)
    delta = _delta_for_cohort(events, ENTITY, Q1_INFORMAL)
    assert delta is not None, (
        "No poverty_headcount_ratio delta for Q1 INFORMAL on "
        "emergency_policy_emergency_declaration. Add the elasticity row (φ=+0.06) "
        "to ELASTICITY_REGISTRY and fix the subscription string."
    )
    assert delta == Decimal("0.06"), (
        f"Expected Q1 INFORMAL delta = +0.06 (CM cert: ILO 2020); got {delta}."
    )


def test_emergency_declaration_triggers_q2_informal_delta() -> None:
    """emergency_policy_emergency_declaration must raise Q2 INFORMAL PHC by 0.04.

    CM cert 2026-07-04: Ball et al. (2013) 0.60 scaling: 0.60 × 0.06 = 0.036 → +0.04.
    """
    event = _emergency_policy_event(ENTITY, "emergency_declaration")
    events = _run_module(ENTITY, event)
    delta = _delta_for_cohort(events, ENTITY, Q2_INFORMAL)
    assert delta is not None, (
        "No poverty_headcount_ratio delta for Q2 INFORMAL on "
        "emergency_policy_emergency_declaration. Add Q2 INFORMAL elasticity row (φ=+0.04)."
    )
    assert delta == Decimal("0.04"), (
        f"Expected Q2 INFORMAL delta = +0.04 (Ball 2013 0.60 scaling); got {delta}."
    )


def test_emergency_declaration_delta_is_positive() -> None:
    """Emergency declaration must raise (not lower) Q1 informal poverty headcount.

    Sign guard. GREEN both before and after #1657.
    """
    event = _emergency_policy_event(ENTITY, "emergency_declaration")
    events = _run_module(ENTITY, event)
    delta = _delta_for_cohort(events, ENTITY, Q1_INFORMAL)
    if delta is None:
        pytest.skip("No elasticity row yet — sign guard fires after row is added.")
    assert delta > Decimal("0"), (
        f"Emergency declaration must increase Q1 informal PHC (δ > 0); got {delta}."
    )
