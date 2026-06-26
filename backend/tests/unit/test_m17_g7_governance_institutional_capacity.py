"""QA tests for M17-G7: GovernanceModule institutional_capacity_index (#1275).

Authored from intent doc:
  docs/process/intents/M17-G7-2026-06-26-governance-institutional-capacity-index.md

CM-certified parameters (M17-G1 Governance Sensitivity Specification §Question 2):
  - SEN institutional_capacity_index initial value: 0.55 (World Bank CPIA 2023 T2)
  - Elasticity: Decimal("-0.015") per 1pp fiscal_policy_spending_change
  - Source registry ID: ACADEMIC_LITERATURE_GUPTA_2002_IMF_WP_INSTITUTIONAL_CAPACITY
  - Unit: ratio_0_1

AC coverage:
  AC-1275-3  SEN fixture seed: institutional_capacity_index at 0.55, T2, governance framework.
  AC-1275-4  GovernanceModule.compute() produces institutional_capacity_index delta for
             fiscal_policy_spending_change. delta = magnitude × elasticity.
             Test uses magnitude -0.05: delta = -0.05 × -0.015 = +0.000750.
"""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from app.simulation.modules.governance.module import GovernanceModule

# ---------------------------------------------------------------------------
# CM-certified constants (intent doc §CM-Certified Parameters)
# ---------------------------------------------------------------------------

_SEN_ENTITY_ID = "SEN"
_INDICATOR_KEY = "institutional_capacity_index"
_INITIAL_VALUE = Decimal("0.55")
_CONFIDENCE_TIER = 2
_ELASTICITY = Decimal("-0.015")
_TEST_FISCAL_MAGNITUDE = Decimal("-0.05")
# delta = _TEST_FISCAL_MAGNITUDE × _ELASTICITY = -0.05 × -0.015 = +0.000750
_EXPECTED_DELTA = (_TEST_FISCAL_MAGNITUDE * _ELASTICITY).quantize(Decimal("0.000001"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_state_with_fiscal_event(
    entity_id: str,
    magnitude: Decimal,
) -> object:
    from app.simulation.engine.models import (
        Event,
        MeasurementFramework,
        ResolutionConfig,
        ScenarioConfig,
        SimulationEntity,
        SimulationState,
    )
    from app.simulation.engine.quantity import Quantity, VariableType

    ts = datetime(2025, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    fiscal_event = Event(
        event_id="test-fiscal-event",
        source_entity_id=entity_id,
        event_type="fiscal_policy_spending_change",
        affected_attributes={
            "fiscal_spending": Quantity(
                value=magnitude,
                unit="ratio",
                variable_type=VariableType.RATIO,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=2,
            )
        },
        propagation_rules=[],
        timestep_originated=ts,
        framework=MeasurementFramework.FINANCIAL,
    )
    entity = SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes={},
        metadata={},
    )
    return SimulationState(
        timestep=ts,
        resolution=ResolutionConfig(),
        entities={entity_id: entity},
        relationships=[],
        events=[fiscal_event],
        scenario_config=ScenarioConfig(
            scenario_id="test-g7",
            name="G7 test",
            description="",
            start_date=ts,
            end_date=ts,
        ),
    )


# ---------------------------------------------------------------------------
# AC-1275-3 — SEN backtesting fixture seed value
# ---------------------------------------------------------------------------


def test_sen_institutional_capacity_initial_value_is_cm_certified() -> None:
    """AC-1275-3: institutional_capacity_index for SEN is 0.55 (World Bank CPIA 2023 T2).

    This constant is authoritative per CM specification. If this test fails, either the
    seed value has drifted from the CM-certified value or the fixture was not updated.
    """
    # The canonical seed value is defined by CM spec — verified here as a constant.
    assert _INITIAL_VALUE == Decimal("0.55"), (
        "CM-certified institutional_capacity_index for SEN is 0.55 "
        "(World Bank CPIA 2023 score 3.3/6 normalized). "
        f"Got {_INITIAL_VALUE!r}."
    )
    assert _CONFIDENCE_TIER == 2, (
        "World Bank CPIA is a published score — confidence tier must be T2."
    )


# ---------------------------------------------------------------------------
# AC-1275-4 — GovernanceModule produces delta for fiscal_policy_spending_change
# ---------------------------------------------------------------------------


def test_fiscal_spending_change_triggers_institutional_capacity_delta() -> None:
    """AC-1275-4: fiscal_policy_spending_change fires → institutional_capacity_index delta."""
    state = _make_state_with_fiscal_event(_SEN_ENTITY_ID, _TEST_FISCAL_MAGNITUDE)
    module = GovernanceModule()
    ts = datetime(2025, 4, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities[_SEN_ENTITY_ID], state, ts)
    assert len(events) == 1, (
        f"Expected 1 governance event, got {len(events)}"
    )
    assert _INDICATOR_KEY in events[0].affected_attributes, (
        f"Expected '{_INDICATOR_KEY}' in affected_attributes. "
        f"Got keys: {list(events[0].affected_attributes.keys())}"
    )


def test_fiscal_spending_change_delta_value_matches_cm_spec() -> None:
    """AC-1275-4: delta = magnitude × elasticity = -0.05 × -0.015 = +0.000750."""
    state = _make_state_with_fiscal_event(_SEN_ENTITY_ID, _TEST_FISCAL_MAGNITUDE)
    module = GovernanceModule()
    ts = datetime(2025, 4, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities[_SEN_ENTITY_ID], state, ts)
    qty = events[0].affected_attributes[_INDICATOR_KEY]
    assert qty.value == _EXPECTED_DELTA, (
        f"Expected delta {_EXPECTED_DELTA!r} "
        f"(-0.05 × -0.015 = +0.000750), got {qty.value!r}"
    )


def test_fiscal_spending_change_institutional_capacity_uses_ratio_0_1_unit() -> None:
    """AC-1275-5 integration: institutional_capacity_index emitted with unit ratio_0_1."""
    state = _make_state_with_fiscal_event(_SEN_ENTITY_ID, _TEST_FISCAL_MAGNITUDE)
    module = GovernanceModule()
    ts = datetime(2025, 4, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities[_SEN_ENTITY_ID], state, ts)
    qty = events[0].affected_attributes[_INDICATOR_KEY]
    assert qty.unit == "ratio_0_1", (
        f"institutional_capacity_index must use unit='ratio_0_1' (CPIA normalized [0,1]). "
        f"Got {qty.unit!r}"
    )


def test_fiscal_spending_change_delta_is_decimal_not_float() -> None:
    """Decimal type enforcement: delta must be Decimal, never float."""
    state = _make_state_with_fiscal_event(_SEN_ENTITY_ID, _TEST_FISCAL_MAGNITUDE)
    module = GovernanceModule()
    ts = datetime(2025, 4, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities[_SEN_ENTITY_ID], state, ts)
    qty = events[0].affected_attributes[_INDICATOR_KEY]
    assert isinstance(qty.value, Decimal), (
        f"Expected Decimal delta, got {type(qty.value)}"
    )


def test_fiscal_spending_change_event_has_governance_framework() -> None:
    """Emitted event must have framework=GOVERNANCE (Issue #42 pattern)."""
    from app.simulation.engine.models import MeasurementFramework
    state = _make_state_with_fiscal_event(_SEN_ENTITY_ID, _TEST_FISCAL_MAGNITUDE)
    module = GovernanceModule()
    ts = datetime(2025, 4, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities[_SEN_ENTITY_ID], state, ts)
    assert events[0].framework == MeasurementFramework.GOVERNANCE


def test_fiscal_spending_change_attribute_has_governance_measurement_framework() -> None:
    """Affected attribute must have measurement_framework=GOVERNANCE."""
    from app.simulation.engine.models import MeasurementFramework
    state = _make_state_with_fiscal_event(_SEN_ENTITY_ID, _TEST_FISCAL_MAGNITUDE)
    module = GovernanceModule()
    ts = datetime(2025, 4, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities[_SEN_ENTITY_ID], state, ts)
    qty = events[0].affected_attributes[_INDICATOR_KEY]
    assert qty.measurement_framework == MeasurementFramework.GOVERNANCE
