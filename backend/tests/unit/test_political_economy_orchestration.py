"""Unit tests for political economy orchestration extensions.

Covers:
  Issue #96  — InputSource.CONDITIONALITY + constraining_actor_id + constraint_mechanism
  Issue #93  — implementation_capacity scaling via get_events()
  Issue #157 — CompoundStateCondition AND/OR logic with recursive nesting

All tests are pure-Python unit tests with no database or HTTP layer dependency.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import datetime
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
from app.simulation.orchestration.inputs import (
    ComparisonOperator,
    CompoundStateCondition,
    FiscalInstrument,
    FiscalPolicyInput,
    InputSource,
    LogicalOperator,
    StateCondition,
)

_BASE_DATE = datetime(2010, 1, 1)
_EPOCH = datetime(2010, 1, 1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _q(value: float) -> Quantity:
    return Quantity(
        value=Decimal(str(value)),
        unit="ratio",
        variable_type=VariableType.RATIO,
        measurement_framework=MeasurementFramework.FINANCIAL,
        confidence_tier=2,
    )


def _state_with(entity_id: str, **attrs: float) -> SimulationState:
    entity = SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes={k: _q(v) for k, v in attrs.items()},
        metadata={},
    )
    return SimulationState(
        timestep=_EPOCH,
        resolution=ResolutionConfig(),
        entities={entity_id: entity},
        relationships=[],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="test",
            name="Test",
            description="",
            start_date=_EPOCH,
            end_date=datetime(2020, 1, 1),
        ),
    )


def _fiscal(value: str = "-0.08", capacity: str = "1.0") -> FiscalPolicyInput:
    return FiscalPolicyInput(
        target_entity="GRC",
        instrument=FiscalInstrument.SPENDING_CHANGE,
        sector="government",
        value=Decimal(value),
        duration_years=1,
        implementation_capacity=Decimal(capacity),
    )


# ---------------------------------------------------------------------------
# Issue #96 — InputSource.CONDITIONALITY + constraining fields
# ---------------------------------------------------------------------------


class TestCondionalityInputSource:
    def test_conditionality_value_in_enum(self) -> None:
        assert InputSource.CONDITIONALITY.value == "conditionality"

    def test_conditionality_is_distinct_from_scenario_script(self) -> None:
        assert InputSource.CONDITIONALITY != InputSource.SCENARIO_SCRIPT

    def test_constraining_actor_id_default_empty(self) -> None:
        inp = _fiscal()
        assert inp.constraining_actor_id == ""

    def test_constraint_mechanism_default_empty(self) -> None:
        inp = _fiscal()
        assert inp.constraint_mechanism == ""

    def test_conditionality_fields_settable(self) -> None:
        inp = FiscalPolicyInput(
            target_entity="GRC",
            instrument=FiscalInstrument.SPENDING_CHANGE,
            sector="government",
            value=Decimal("-0.08"),
            duration_years=1,
            source=InputSource.CONDITIONALITY,
            constraining_actor_id="IMF",
            constraint_mechanism="ELA_WITHDRAWAL_THREAT",
        )
        assert inp.source == InputSource.CONDITIONALITY
        assert inp.constraining_actor_id == "IMF"
        assert inp.constraint_mechanism == "ELA_WITHDRAWAL_THREAT"

    def test_conditionality_audit_trail_distinguishable(self) -> None:
        """CONDITIONALITY source is distinguishable from SCENARIO_SCRIPT in audit."""
        free_choice = FiscalPolicyInput(
            target_entity="GRC",
            instrument=FiscalInstrument.SPENDING_CHANGE,
            sector="government",
            value=Decimal("-0.08"),
            duration_years=1,
            source=InputSource.SCENARIO_SCRIPT,
        )
        coerced = FiscalPolicyInput(
            target_entity="GRC",
            instrument=FiscalInstrument.SPENDING_CHANGE,
            sector="government",
            value=Decimal("-0.08"),
            duration_years=1,
            source=InputSource.CONDITIONALITY,
            constraining_actor_id="IMF",
            constraint_mechanism="DISBURSEMENT_SUSPENSION",
        )
        assert free_choice.source != coerced.source
        assert coerced.constraining_actor_id == "IMF"


# ---------------------------------------------------------------------------
# Issue #93 — implementation_capacity scaling via get_events()
# ---------------------------------------------------------------------------


class TestImplementationCapacityScaling:
    def test_default_capacity_is_one(self) -> None:
        inp = _fiscal()
        assert inp.implementation_capacity == Decimal("1.0")

    def test_get_events_full_capacity_unchanged(self) -> None:
        """implementation_capacity=1.0 → get_events() returns unscaled events."""
        inp = _fiscal(value="-0.08", capacity="1.0")
        raw = inp.to_events(_BASE_DATE)
        scaled = inp.get_events(_BASE_DATE)
        assert len(raw) == len(scaled)
        for r, s in zip(raw, scaled, strict=True):
            for k in r.affected_attributes:
                assert r.affected_attributes[k].value == s.affected_attributes[k].value

    def test_get_events_half_capacity_halves_magnitude(self) -> None:
        """implementation_capacity=0.5 → event magnitudes halved."""
        inp = _fiscal(value="-0.08", capacity="0.5")
        raw = inp.to_events(_BASE_DATE)
        scaled = inp.get_events(_BASE_DATE)
        assert len(raw) == len(scaled)
        for r, s in zip(raw, scaled, strict=True):
            for k in r.affected_attributes:
                assert s.affected_attributes[k].value == r.affected_attributes[k].value * Decimal("0.5")

    def test_get_events_zero_capacity_zeroes_magnitude(self) -> None:
        """implementation_capacity=0.0 → all event attribute values are zero."""
        inp = _fiscal(value="-0.08", capacity="0.0")
        scaled = inp.get_events(_BASE_DATE)
        for evt in scaled:
            for q in evt.affected_attributes.values():
                assert q.value == Decimal("0")

    def test_get_events_preserves_event_structure(self) -> None:
        """Scaling must not change event_type, source_entity_id, or metadata."""
        inp = _fiscal(value="-0.08", capacity="0.75")
        raw = inp.to_events(_BASE_DATE)
        scaled = inp.get_events(_BASE_DATE)
        for r, s in zip(raw, scaled, strict=True):
            assert r.event_type == s.event_type
            assert r.source_entity_id == s.source_entity_id
            assert r.framework == s.framework

    def test_get_events_preserves_confidence_tier(self) -> None:
        """Scaling must not change the confidence_tier of attribute Quantities."""
        inp = _fiscal(value="-0.08", capacity="0.5")
        raw = inp.to_events(_BASE_DATE)
        scaled = inp.get_events(_BASE_DATE)
        for r, s in zip(raw, scaled, strict=True):
            for k in r.affected_attributes:
                assert (r.affected_attributes[k].confidence_tier ==
                        s.affected_attributes[k].confidence_tier)

    def test_to_events_unaffected_by_capacity(self) -> None:
        """to_events() must not apply scaling — raw output is always unscaled."""
        inp = _fiscal(value="-0.10", capacity="0.3")
        raw = inp.to_events(_BASE_DATE)
        # The raw events should contain the full -0.10 magnitude
        for evt in raw:
            for q in evt.affected_attributes.values():
                assert abs(q.value) == Decimal("0.10")


# ---------------------------------------------------------------------------
# Issue #157 — CompoundStateCondition AND/OR logic
# ---------------------------------------------------------------------------


class TestCompoundStateCondition:
    def _cond(
        self, entity_id: str, attr: str, op: ComparisonOperator, threshold: float
    ) -> StateCondition:
        return StateCondition(
            entity_id=entity_id,
            attribute=attr,
            operator=op,
            threshold=threshold,
        )

    def test_and_both_met(self) -> None:
        """AND: both conditions met → is_met returns True."""
        state = _state_with("GRC", reserves=2.0, outflow=0.20)
        compound = CompoundStateCondition(
            operator=LogicalOperator.AND,
            conditions=[
                self._cond("GRC", "reserves", ComparisonOperator.LT, 3.0),
                self._cond("GRC", "outflow", ComparisonOperator.GT, 0.15),
            ],
        )
        assert compound.is_met(state) is True

    def test_and_first_not_met(self) -> None:
        """AND: first condition not met → is_met returns False (short-circuit)."""
        state = _state_with("GRC", reserves=5.0, outflow=0.20)
        compound = CompoundStateCondition(
            operator=LogicalOperator.AND,
            conditions=[
                self._cond("GRC", "reserves", ComparisonOperator.LT, 3.0),  # 5.0 < 3.0 → False
                self._cond("GRC", "outflow", ComparisonOperator.GT, 0.15),
            ],
        )
        assert compound.is_met(state) is False

    def test_and_second_not_met(self) -> None:
        """AND: second condition not met → is_met returns False."""
        state = _state_with("GRC", reserves=2.0, outflow=0.10)
        compound = CompoundStateCondition(
            operator=LogicalOperator.AND,
            conditions=[
                self._cond("GRC", "reserves", ComparisonOperator.LT, 3.0),
                self._cond("GRC", "outflow", ComparisonOperator.GT, 0.15),  # 0.10 > 0.15 → False
            ],
        )
        assert compound.is_met(state) is False

    def test_or_first_met(self) -> None:
        """OR: first condition met → is_met returns True (short-circuit)."""
        state = _state_with("GRC", confidence=0.25, bank_holiday=0.0)
        compound = CompoundStateCondition(
            operator=LogicalOperator.OR,
            conditions=[
                self._cond("GRC", "confidence", ComparisonOperator.LT, 0.30),  # True
                self._cond("GRC", "bank_holiday", ComparisonOperator.GT, 0.50),  # False
            ],
        )
        assert compound.is_met(state) is True

    def test_or_second_met(self) -> None:
        """OR: only second condition met → is_met returns True."""
        state = _state_with("GRC", confidence=0.50, bank_holiday=0.70)
        compound = CompoundStateCondition(
            operator=LogicalOperator.OR,
            conditions=[
                self._cond("GRC", "confidence", ComparisonOperator.LT, 0.30),  # False
                self._cond("GRC", "bank_holiday", ComparisonOperator.GT, 0.50),  # True
            ],
        )
        assert compound.is_met(state) is True

    def test_or_none_met(self) -> None:
        """OR: no conditions met → is_met returns False."""
        state = _state_with("GRC", confidence=0.60, bank_holiday=0.30)
        compound = CompoundStateCondition(
            operator=LogicalOperator.OR,
            conditions=[
                self._cond("GRC", "confidence", ComparisonOperator.LT, 0.30),
                self._cond("GRC", "bank_holiday", ComparisonOperator.GT, 0.50),
            ],
        )
        assert compound.is_met(state) is False

    def test_empty_conditions_returns_false(self) -> None:
        """Empty conditions list is conservative — returns False."""
        state = _state_with("GRC", gdp_growth=-0.05)
        compound = CompoundStateCondition(
            operator=LogicalOperator.AND,
            conditions=[],
        )
        assert compound.is_met(state) is False

    def test_nested_compound_conditions(self) -> None:
        """Nested AND within OR evaluates recursively."""
        state = _state_with("GRC", reserves=2.0, outflow=0.20, gdp_growth=-0.10)
        # (reserves < 3 AND outflow > 0.15) OR (gdp_growth < -0.05)
        inner_and = CompoundStateCondition(
            operator=LogicalOperator.AND,
            conditions=[
                self._cond("GRC", "reserves", ComparisonOperator.LT, 3.0),
                self._cond("GRC", "outflow", ComparisonOperator.GT, 0.15),
            ],
        )
        outer_or = CompoundStateCondition(
            operator=LogicalOperator.OR,
            conditions=[
                inner_and,
                self._cond("GRC", "gdp_growth", ComparisonOperator.LT, -0.05),
            ],
        )
        assert outer_or.is_met(state) is True

    def test_nested_and_fails_when_inner_condition_not_met(self) -> None:
        """Nested compound: inner AND fails → outer AND fails."""
        state = _state_with("GRC", reserves=5.0, outflow=0.20, deficit=0.10)
        # (reserves < 3 AND outflow > 0.15) AND deficit > 0.05
        inner_and = CompoundStateCondition(
            operator=LogicalOperator.AND,
            conditions=[
                self._cond("GRC", "reserves", ComparisonOperator.LT, 3.0),  # False
                self._cond("GRC", "outflow", ComparisonOperator.GT, 0.15),
            ],
        )
        outer_and = CompoundStateCondition(
            operator=LogicalOperator.AND,
            conditions=[
                inner_and,
                self._cond("GRC", "deficit", ComparisonOperator.GT, 0.05),
            ],
        )
        assert outer_and.is_met(state) is False

    def test_state_condition_backward_compatible(self) -> None:
        """Existing StateCondition.is_met() still works — no regression."""
        state = _state_with("GRC", gdp_growth=-0.05)
        cond = self._cond("GRC", "gdp_growth", ComparisonOperator.LT, 0.0)
        assert cond.is_met(state) is True

    def test_logical_operator_enum_values(self) -> None:
        assert LogicalOperator.AND.value == "and"
        assert LogicalOperator.OR.value == "or"
