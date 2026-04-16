"""
Unit tests for the Input Orchestration Layer — ADR-002.

Covers:
- ScenarioRunner advances state correctly across multiple timesteps
- Each ControlInput subclass translates correctly to Events
- Audit records are created for every injected input
- ContingentInputs fire when conditions are met and respect cooldown
- Scenario replay from audit log produces identical event sequences
"""

from __future__ import annotations

import dataclasses
from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
    PropagationRule,
    Relationship,
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationModule,
    SimulationState,
)
from app.simulation.orchestration import (
    AuditLog,
    ComparisonOperator,
    ContingentInput,
    EmergencyInstrument,
    EmergencyPolicyInput,
    FiscalInstrument,
    FiscalPolicyInput,
    InputSource,
    MonetaryInstrument,
    MonetaryPolicyInput,
    ScenarioRunner,
    StateCondition,
    StructuralInstrument,
    StructuralPolicyInput,
    TradeInstrument,
    TradePolicyInput,
)

# ---------------------------------------------------------------------------
# Shared fixtures / helpers
# ---------------------------------------------------------------------------

_BASE_DATE = datetime(2025, 1, 1)
_STEP_DELTA = timedelta(days=365)


def _entity(entity_id: str, **attributes: float) -> SimulationEntity:
    return SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes=dict(attributes),
        metadata={},
    )


def _scenario(scenario_id: str = "TEST") -> ScenarioConfig:
    return ScenarioConfig(
        scenario_id=scenario_id,
        name="Test Scenario",
        description="Unit test scenario",
        start_date=_BASE_DATE,
        end_date=_BASE_DATE + timedelta(days=3650),
    )


def _state(
    entities: dict[str, SimulationEntity] | None = None,
    relationships: list[Relationship] | None = None,
    scenario_id: str = "TEST",
) -> SimulationState:
    return SimulationState(
        timestep=_BASE_DATE,
        resolution=ResolutionConfig(),
        entities=entities or {},
        relationships=relationships or [],
        events=[],
        scenario_config=_scenario(scenario_id),
    )


def _monetary_input(
    target: str = "USA",
    instrument: MonetaryInstrument = MonetaryInstrument.POLICY_RATE,
    value: Decimal = Decimal("0.005"),
) -> MonetaryPolicyInput:
    return MonetaryPolicyInput(
        target_entity=target,
        instrument=instrument,
        value=value,
        actor_id="test_actor",
        actor_role="central_bank",
        effective_date=_BASE_DATE,
        justification="test",
        timestamp=_BASE_DATE,
    )


def _fiscal_input(
    target: str = "USA",
    sector: str = "",
    value: Decimal = Decimal("0.01"),
) -> FiscalPolicyInput:
    return FiscalPolicyInput(
        target_entity=target,
        instrument=FiscalInstrument.SPENDING_CHANGE,
        sector=sector,
        value=value,
        actor_id="test_actor",
        actor_role="finance_minister",
        effective_date=_BASE_DATE,
        justification="test",
        timestamp=_BASE_DATE,
    )


def _trade_input(
    source: str = "USA",
    target: str = "CHN",
    value: Decimal = Decimal("0.25"),
    retaliation: bool = False,
) -> TradePolicyInput:
    return TradePolicyInput(
        target_entity=target,
        source_entity=source,
        instrument=TradeInstrument.TARIFF_RATE,
        affected_sector="goods",
        value=value,
        retaliation_modeled=retaliation,
        actor_id="test_actor",
        actor_role="trade_minister",
        effective_date=_BASE_DATE,
        justification="test",
        timestamp=_BASE_DATE,
    )


def _emergency_input(
    target: str = "GRC",
    magnitude: float = 1.0,
) -> EmergencyPolicyInput:
    return EmergencyPolicyInput(
        target_entity=target,
        instrument=EmergencyInstrument.CAPITAL_CONTROLS,
        parameters={"magnitude": magnitude},
        expected_duration=3,
        actor_id="test_actor",
        actor_role="finance_minister",
        effective_date=_BASE_DATE,
        justification="test",
        timestamp=_BASE_DATE,
    )


def _structural_input(
    target: str = "BRA",
    sector: str = "energy",
    magnitude: float = 1.0,
) -> StructuralPolicyInput:
    return StructuralPolicyInput(
        target_entity=target,
        instrument=StructuralInstrument.PRIVATIZATION,
        affected_sector=sector,
        parameters={"magnitude": magnitude},
        implementation_years=3,
        actor_id="test_actor",
        actor_role="president",
        effective_date=_BASE_DATE,
        justification="test",
        timestamp=_BASE_DATE,
    )


class _NoOpModule(SimulationModule):
    """Module that returns no events — used to verify advance_timestep runs."""

    def compute(
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime,
    ) -> list[Event]:
        return []

    def get_subscribed_events(self) -> list[str]:
        return []


class _ConstantDeltaModule(SimulationModule):
    """Module that adds a fixed delta to one attribute on every entity."""

    def __init__(self, attribute: str, delta: float) -> None:
        self._attribute = attribute
        self._delta = delta

    def compute(
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime,
    ) -> list[Event]:
        return [
            Event(
                event_id=f"module-{entity.id}-{timestep.isoformat()}",
                source_entity_id=entity.id,
                event_type="module_delta",
                affected_attributes={self._attribute: self._delta},
                propagation_rules=[],
                timestep_originated=timestep,
            )
        ]

    def get_subscribed_events(self) -> list[str]:
        return []


# ---------------------------------------------------------------------------
# ScenarioRunner: basic advancement
# ---------------------------------------------------------------------------


class TestScenarioRunnerAdvances:
    def test_run_returns_state_history_of_correct_length(self) -> None:
        runner = ScenarioRunner(
            initial_state=_state(entities={"USA": _entity("USA", gdp_growth=0.02)}),
            scheduled_inputs=[],
            modules=[],
            n_steps=3,
        )
        history = runner.run()
        assert len(history) == 4  # initial + 3 steps

    def test_run_index_zero_is_initial_state(self) -> None:
        initial = _state(entities={"USA": _entity("USA", gdp_growth=0.02)})
        runner = ScenarioRunner(
            initial_state=initial,
            scheduled_inputs=[],
            modules=[],
            n_steps=1,
        )
        history = runner.run()
        assert history[0] is initial

    def test_run_advances_timestep_by_delta_each_step(self) -> None:
        delta = timedelta(days=365)
        runner = ScenarioRunner(
            initial_state=_state(),
            scheduled_inputs=[],
            modules=[],
            n_steps=3,
            timestep_delta=delta,
        )
        history = runner.run()
        assert history[1].timestep == _BASE_DATE + delta
        assert history[2].timestep == _BASE_DATE + 2 * delta
        assert history[3].timestep == _BASE_DATE + 3 * delta

    def test_module_deltas_accumulate_across_steps(self) -> None:
        runner = ScenarioRunner(
            initial_state=_state(entities={"USA": _entity("USA", counter=0.0)}),
            scheduled_inputs=[],
            modules=[_ConstantDeltaModule("counter", 1.0)],
            n_steps=3,
        )
        history = runner.run()
        assert history[3].entities["USA"].get_attribute("counter") == pytest.approx(3.0)

    def test_scheduled_input_fires_at_correct_step(self) -> None:
        tariff = _trade_input()
        runner = ScenarioRunner(
            initial_state=_state(
                entities={"USA": _entity("USA"), "CHN": _entity("CHN")}
            ),
            scheduled_inputs=[(2, tariff)],
            modules=[],
            n_steps=3,
        )
        history = runner.run()
        # Step 2 fires the tariff; USA receives trade_tariff_rate delta
        val_step1 = history[1].entities["USA"].get_attribute("trade_tariff_rate_goods")
        val_step2 = history[2].entities["USA"].get_attribute("trade_tariff_rate_goods")
        assert val_step1 == pytest.approx(0.0)
        assert val_step2 == pytest.approx(0.25)

    def test_no_steps_returns_only_initial_state(self) -> None:
        runner = ScenarioRunner(
            initial_state=_state(),
            scheduled_inputs=[],
            modules=[],
            n_steps=0,
        )
        history = runner.run()
        assert len(history) == 1

    def test_state_immutability_across_steps(self) -> None:
        initial = _state(entities={"USA": _entity("USA", gdp_growth=0.02)})
        runner = ScenarioRunner(
            initial_state=initial,
            scheduled_inputs=[],
            modules=[_ConstantDeltaModule("gdp_growth", 0.01)],
            n_steps=5,
        )
        runner.run()
        # Original state must be unchanged
        assert initial.entities["USA"].get_attribute("gdp_growth") == pytest.approx(
            0.02
        )


# ---------------------------------------------------------------------------
# MonetaryPolicyInput translation
# ---------------------------------------------------------------------------


class TestMonetaryPolicyInputToEvents:
    def test_produces_single_event(self) -> None:
        inp = _monetary_input()
        events = inp.to_events(_BASE_DATE)
        assert len(events) == 1

    def test_event_source_is_target_entity(self) -> None:
        events = _monetary_input(target="BOL").to_events(_BASE_DATE)
        assert events[0].source_entity_id == "BOL"

    def test_event_type_matches_instrument(self) -> None:
        inp = MonetaryPolicyInput(
            target_entity="USA",
            instrument=MonetaryInstrument.RESERVE_REQUIREMENT,
            value=Decimal("0.02"),
            effective_date=_BASE_DATE,
            timestamp=_BASE_DATE,
        )
        events = inp.to_events(_BASE_DATE)
        assert events[0].event_type == "monetary_policy_reserve_requirement"

    def test_affected_attributes_contains_instrument_value(self) -> None:
        inp = _monetary_input(
            instrument=MonetaryInstrument.POLICY_RATE, value=Decimal("0.005")
        )
        events = inp.to_events(_BASE_DATE)
        assert "policy_rate" in events[0].affected_attributes
        assert events[0].affected_attributes["policy_rate"] == pytest.approx(0.005)

    def test_event_framework_is_financial(self) -> None:
        events = _monetary_input().to_events(_BASE_DATE)
        assert events[0].framework == MeasurementFramework.FINANCIAL

    def test_event_id_contains_input_id(self) -> None:
        inp = _monetary_input()
        events = inp.to_events(_BASE_DATE)
        assert inp.input_id in events[0].event_id

    def test_propagation_rules_passed_through(self) -> None:
        rule = PropagationRule(relationship_type="debt", attenuation_factor=0.5)
        inp = _monetary_input()
        inp = dataclasses.replace(inp, propagation_rules=[rule])
        events = inp.to_events(_BASE_DATE)
        assert events[0].propagation_rules == [rule]

    def test_negative_value_produces_negative_delta(self) -> None:
        inp = _monetary_input(value=Decimal("-0.005"))
        events = inp.to_events(_BASE_DATE)
        assert events[0].affected_attributes["policy_rate"] == pytest.approx(-0.005)


# ---------------------------------------------------------------------------
# FiscalPolicyInput translation
# ---------------------------------------------------------------------------


class TestFiscalPolicyInputToEvents:
    def test_sector_qualified_key_when_sector_specified(self) -> None:
        events = _fiscal_input(sector="health").to_events(_BASE_DATE)
        assert "fiscal_spending_change_health" in events[0].affected_attributes

    def test_economy_wide_key_when_no_sector(self) -> None:
        events = _fiscal_input(sector="").to_events(_BASE_DATE)
        assert "fiscal_spending_change" in events[0].affected_attributes

    def test_event_type_matches_instrument(self) -> None:
        inp = FiscalPolicyInput(
            target_entity="GRC",
            instrument=FiscalInstrument.TAX_RATE_CHANGE,
            sector="",
            value=Decimal("0.02"),
            effective_date=_BASE_DATE,
            timestamp=_BASE_DATE,
        )
        events = inp.to_events(_BASE_DATE)
        assert events[0].event_type == "fiscal_policy_tax_rate_change"

    def test_event_framework_is_financial(self) -> None:
        events = _fiscal_input().to_events(_BASE_DATE)
        assert events[0].framework == MeasurementFramework.FINANCIAL

    def test_produces_single_event(self) -> None:
        assert len(_fiscal_input().to_events(_BASE_DATE)) == 1

    def test_value_in_affected_attributes(self) -> None:
        events = _fiscal_input(value=Decimal("0.05")).to_events(_BASE_DATE)
        val = next(iter(events[0].affected_attributes.values()))
        assert val == pytest.approx(0.05)


# ---------------------------------------------------------------------------
# TradePolicyInput translation
# ---------------------------------------------------------------------------


class TestTradePolicyInputToEvents:
    def test_no_retaliation_produces_one_event(self) -> None:
        events = _trade_input(retaliation=False).to_events(_BASE_DATE)
        assert len(events) == 1

    def test_retaliation_produces_two_events(self) -> None:
        events = _trade_input(retaliation=True).to_events(_BASE_DATE)
        assert len(events) == 2

    def test_primary_event_source_is_source_entity(self) -> None:
        events = _trade_input(source="USA", target="CHN").to_events(_BASE_DATE)
        assert events[0].source_entity_id == "USA"

    def test_retaliation_event_source_is_target_entity(self) -> None:
        events = _trade_input(source="USA", target="CHN", retaliation=True).to_events(
            _BASE_DATE
        )
        assert events[1].source_entity_id == "CHN"

    def test_retaliation_event_has_negated_value(self) -> None:
        events = _trade_input(value=Decimal("0.25"), retaliation=True).to_events(
            _BASE_DATE
        )
        primary_val = events[0].affected_attributes["trade_tariff_rate_goods"]
        retaliation_val = events[1].affected_attributes["trade_tariff_rate_goods"]
        assert retaliation_val == pytest.approx(-primary_val)

    def test_sector_qualified_attribute_key(self) -> None:
        events = _trade_input().to_events(_BASE_DATE)
        assert "trade_tariff_rate_goods" in events[0].affected_attributes

    def test_no_sector_produces_unqualified_key(self) -> None:
        inp = TradePolicyInput(
            target_entity="CHN",
            source_entity="USA",
            instrument=TradeInstrument.SANCTIONS,
            affected_sector="",
            value=Decimal("1.0"),
            effective_date=_BASE_DATE,
            timestamp=_BASE_DATE,
        )
        events = inp.to_events(_BASE_DATE)
        assert "trade_sanctions" in events[0].affected_attributes

    def test_event_framework_is_financial(self) -> None:
        events = _trade_input().to_events(_BASE_DATE)
        assert events[0].framework == MeasurementFramework.FINANCIAL


# ---------------------------------------------------------------------------
# EmergencyPolicyInput translation
# ---------------------------------------------------------------------------


class TestEmergencyPolicyInputToEvents:
    def test_produces_single_event(self) -> None:
        assert len(_emergency_input().to_events(_BASE_DATE)) == 1

    def test_event_type_matches_instrument(self) -> None:
        events = _emergency_input().to_events(_BASE_DATE)
        assert events[0].event_type == "emergency_policy_capital_controls"

    def test_magnitude_from_parameters(self) -> None:
        events = _emergency_input(magnitude=0.5).to_events(_BASE_DATE)
        assert events[0].affected_attributes["capital_controls"] == pytest.approx(0.5)

    def test_default_magnitude_is_one(self) -> None:
        inp = EmergencyPolicyInput(
            target_entity="GRC",
            instrument=EmergencyInstrument.BANK_HOLIDAY,
            parameters={},
            effective_date=_BASE_DATE,
            timestamp=_BASE_DATE,
        )
        events = inp.to_events(_BASE_DATE)
        assert events[0].affected_attributes["bank_holiday"] == pytest.approx(1.0)

    def test_event_framework_is_governance(self) -> None:
        events = _emergency_input().to_events(_BASE_DATE)
        assert events[0].framework == MeasurementFramework.GOVERNANCE


# ---------------------------------------------------------------------------
# StructuralPolicyInput translation
# ---------------------------------------------------------------------------


class TestStructuralPolicyInputToEvents:
    def test_produces_single_event(self) -> None:
        assert len(_structural_input().to_events(_BASE_DATE)) == 1

    def test_event_type_matches_instrument(self) -> None:
        events = _structural_input().to_events(_BASE_DATE)
        assert events[0].event_type == "structural_policy_privatization"

    def test_magnitude_from_parameters(self) -> None:
        events = _structural_input(magnitude=2.0).to_events(_BASE_DATE)
        assert events[0].affected_attributes["privatization"] == pytest.approx(2.0)

    def test_event_framework_is_governance(self) -> None:
        events = _structural_input().to_events(_BASE_DATE)
        assert events[0].framework == MeasurementFramework.GOVERNANCE

    def test_event_source_is_target_entity(self) -> None:
        events = _structural_input(target="ARG").to_events(_BASE_DATE)
        assert events[0].source_entity_id == "ARG"


# ---------------------------------------------------------------------------
# Audit log
# ---------------------------------------------------------------------------


class TestAuditLog:
    def test_inject_creates_audit_record(self) -> None:
        log = AuditLog()
        runner = ScenarioRunner(
            initial_state=_state(entities={"USA": _entity("USA")}),
            scheduled_inputs=[(1, _monetary_input())],
            modules=[],
            n_steps=1,
            audit_log=log,
        )
        runner.run()
        assert len(log) == 1

    def test_audit_record_has_correct_input_type(self) -> None:
        log = AuditLog()
        runner = ScenarioRunner(
            initial_state=_state(entities={"USA": _entity("USA")}),
            scheduled_inputs=[(1, _monetary_input())],
            modules=[],
            n_steps=1,
            audit_log=log,
        )
        runner.run()
        assert log.records[0].input_type == "MonetaryPolicyInput"

    def test_audit_record_captures_actor_fields(self) -> None:
        log = AuditLog()
        inp = _monetary_input()
        runner = ScenarioRunner(
            initial_state=_state(entities={"USA": _entity("USA")}),
            scheduled_inputs=[(1, inp)],
            modules=[],
            n_steps=1,
            audit_log=log,
        )
        runner.run()
        record = log.records[0]
        assert record.actor_id == "test_actor"
        assert record.actor_role == "central_bank"

    def test_audit_record_lists_translated_event_ids(self) -> None:
        log = AuditLog()
        inp = _monetary_input()
        runner = ScenarioRunner(
            initial_state=_state(entities={"USA": _entity("USA")}),
            scheduled_inputs=[(1, inp)],
            modules=[],
            n_steps=1,
            audit_log=log,
        )
        runner.run()
        record = log.records[0]
        assert len(record.translated_events) == 1
        assert inp.input_id in record.translated_events[0]

    def test_multiple_inputs_produce_multiple_records(self) -> None:
        log = AuditLog()
        runner = ScenarioRunner(
            initial_state=_state(entities={"USA": _entity("USA")}),
            scheduled_inputs=[(1, _monetary_input()), (2, _fiscal_input())],
            modules=[],
            n_steps=2,
            audit_log=log,
        )
        runner.run()
        assert len(log) == 2

    def test_get_records_for_session_filters_correctly(self) -> None:
        log = AuditLog()
        runner = ScenarioRunner(
            initial_state=_state(entities={"USA": _entity("USA")}),
            scheduled_inputs=[(1, _monetary_input())],
            modules=[],
            n_steps=1,
            audit_log=log,
            session_id="session-abc",
        )
        runner.run()
        assert len(log.get_records_for_session("session-abc")) == 1
        assert len(log.get_records_for_session("other-session")) == 0

    def test_audit_record_scenario_id_matches_state(self) -> None:
        log = AuditLog()
        runner = ScenarioRunner(
            initial_state=_state(
                entities={"USA": _entity("USA")}, scenario_id="TARIFF-2025"
            ),
            scheduled_inputs=[(1, _monetary_input())],
            modules=[],
            n_steps=1,
            audit_log=log,
        )
        runner.run()
        assert log.records[0].scenario_id == "TARIFF-2025"

    def test_raw_input_contains_target_entity(self) -> None:
        log = AuditLog()
        runner = ScenarioRunner(
            initial_state=_state(entities={"USA": _entity("USA")}),
            scheduled_inputs=[(1, _monetary_input(target="USA"))],
            modules=[],
            n_steps=1,
            audit_log=log,
        )
        runner.run()
        assert log.records[0].raw_input["target_entity"] == "USA"


# ---------------------------------------------------------------------------
# ContingentInput: condition evaluation and cooldown
# ---------------------------------------------------------------------------


class TestStateCondition:
    def test_lt_condition_true_when_below_threshold(self) -> None:
        state = _state(entities={"GRC": _entity("GRC", reserves=2.0)})
        cond = StateCondition(
            entity_id="GRC",
            attribute="reserves",
            operator=ComparisonOperator.LT,
            threshold=3.0,
        )
        assert cond.is_met(state) is True

    def test_lt_condition_false_when_above_threshold(self) -> None:
        state = _state(entities={"GRC": _entity("GRC", reserves=4.0)})
        cond = StateCondition(
            entity_id="GRC",
            attribute="reserves",
            operator=ComparisonOperator.LT,
            threshold=3.0,
        )
        assert cond.is_met(state) is False

    def test_gt_condition(self) -> None:
        state = _state(entities={"USA": _entity("USA", debt_gdp=1.30)})
        cond = StateCondition(
            entity_id="USA",
            attribute="debt_gdp",
            operator=ComparisonOperator.GT,
            threshold=1.20,
        )
        assert cond.is_met(state) is True

    def test_gte_condition_true_at_threshold(self) -> None:
        state = _state(entities={"BOL": _entity("BOL", inflation=0.10)})
        cond = StateCondition(
            entity_id="BOL",
            attribute="inflation",
            operator=ComparisonOperator.GTE,
            threshold=0.10,
        )
        assert cond.is_met(state) is True

    def test_eq_condition(self) -> None:
        state = _state(entities={"ARG": _entity("ARG", crisis_flag=1.0)})
        cond = StateCondition(
            entity_id="ARG",
            attribute="crisis_flag",
            operator=ComparisonOperator.EQ,
            threshold=1.0,
        )
        assert cond.is_met(state) is True

    def test_absent_entity_returns_false(self) -> None:
        state = _state(entities={})
        cond = StateCondition(
            entity_id="MISSING",
            attribute="reserves",
            operator=ComparisonOperator.LT,
            threshold=3.0,
        )
        assert cond.is_met(state) is False

    def test_absent_attribute_uses_default_zero(self) -> None:
        # default for missing attribute is 0.0; LT 1.0 is true
        state = _state(entities={"GRC": _entity("GRC")})
        cond = StateCondition(
            entity_id="GRC",
            attribute="reserves",
            operator=ComparisonOperator.LT,
            threshold=1.0,
        )
        assert cond.is_met(state) is True


class TestContingentInputFiring:
    def _make_runner(
        self,
        contingents: list[ContingentInput],
        initial_attributes: dict[str, float],
        n_steps: int = 3,
    ) -> ScenarioRunner:
        return ScenarioRunner(
            initial_state=_state(
                entities={"GRC": _entity("GRC", **initial_attributes)}
            ),
            scheduled_inputs=[],
            modules=[],
            n_steps=n_steps,
            contingent_inputs=contingents,
        )

    def test_contingent_fires_when_condition_met(self) -> None:
        cond = StateCondition(
            entity_id="GRC",
            attribute="reserves",
            operator=ComparisonOperator.LT,
            threshold=3.0,
        )
        triggered_input = _emergency_input(target="GRC")
        contingent = ContingentInput(
            condition=cond,
            input=triggered_input,
            cooldown_periods=10,
            documented_rationale="Low reserves trigger capital controls",
            empirical_basis="IMF Article IV 3-month threshold",
        )
        runner = self._make_runner(
            contingents=[contingent],
            initial_attributes={"reserves": 2.0},  # below threshold from step 0
        )
        history = runner.run()
        # capital_controls fires on GRC; it should appear in state after step 1
        val = history[1].entities["GRC"].get_attribute("capital_controls")
        assert val == pytest.approx(1.0)

    def test_contingent_does_not_fire_when_condition_not_met(self) -> None:
        cond = StateCondition(
            entity_id="GRC",
            attribute="reserves",
            operator=ComparisonOperator.LT,
            threshold=3.0,
        )
        contingent = ContingentInput(
            condition=cond,
            input=_emergency_input(target="GRC"),
            cooldown_periods=1,
            documented_rationale="test",
            empirical_basis="test",
        )
        runner = self._make_runner(
            contingents=[contingent],
            initial_attributes={"reserves": 5.0},  # above threshold
        )
        history = runner.run()
        val = history[3].entities["GRC"].get_attribute("capital_controls")
        assert val == pytest.approx(0.0)

    def test_contingent_respects_cooldown_period(self) -> None:
        cond = StateCondition(
            entity_id="GRC",
            attribute="reserves",
            operator=ComparisonOperator.LT,
            threshold=10.0,  # always met — tests cooldown isolation
        )
        contingent = ContingentInput(
            condition=cond,
            input=_emergency_input(target="GRC", magnitude=1.0),
            cooldown_periods=2,
            documented_rationale="test",
            empirical_basis="test",
        )
        runner = self._make_runner(
            contingents=[contingent],
            initial_attributes={"reserves": 1.0},
            n_steps=5,
        )
        history = runner.run()
        # Sequence: fires step 1 (cooldown set→2, decrements→1), skips step 2
        # (decrements→0), fires step 3, skips step 4, fires step 5.
        # Fires: steps 1, 3, 5 → 3 firings → total = 3.0
        val = history[5].entities["GRC"].get_attribute("capital_controls")
        assert val == pytest.approx(3.0)

    def test_contingent_source_set_to_contingent_trigger(self) -> None:
        log = AuditLog()
        cond = StateCondition(
            entity_id="GRC",
            attribute="reserves",
            operator=ComparisonOperator.LT,
            threshold=10.0,
        )
        contingent = ContingentInput(
            condition=cond,
            input=_emergency_input(target="GRC"),
            cooldown_periods=100,
            documented_rationale="test",
            empirical_basis="test",
        )
        runner = ScenarioRunner(
            initial_state=_state(
                entities={"GRC": _entity("GRC", reserves=1.0)}
            ),
            scheduled_inputs=[],
            modules=[],
            n_steps=1,
            contingent_inputs=[contingent],
            audit_log=log,
        )
        runner.run()
        assert log.records[0].source == InputSource.CONTINGENT_TRIGGER


# ---------------------------------------------------------------------------
# Scenario replay
# ---------------------------------------------------------------------------


class TestScenarioReplay:
    def test_replay_from_audit_log_produces_same_event_ids(self) -> None:
        log = AuditLog()
        inp = _monetary_input()
        runner = ScenarioRunner(
            initial_state=_state(entities={"USA": _entity("USA")}),
            scheduled_inputs=[(1, inp)],
            modules=[],
            n_steps=1,
            audit_log=log,
        )
        runner.run()

        # The audit record lists which events were generated
        record = log.records[0]
        expected_event_id = f"{inp.input_id}-monetary-0"
        assert expected_event_id in record.translated_events

    def test_same_inputs_produce_same_final_state(self) -> None:
        def _make_runner() -> ScenarioRunner:
            return ScenarioRunner(
                initial_state=_state(
                    entities={"USA": _entity("USA", gdp_growth=0.02)}
                ),
                scheduled_inputs=[(1, _monetary_input(value=Decimal("0.005")))],
                modules=[],
                n_steps=2,
            )

        history_a = _make_runner().run()
        history_b = _make_runner().run()
        val_a = history_a[2].entities["USA"].get_attribute("policy_rate")
        val_b = history_b[2].entities["USA"].get_attribute("policy_rate")
        assert val_a == pytest.approx(val_b)

    def test_retaliation_events_both_appear_in_translated_events(self) -> None:
        log = AuditLog()
        inp = _trade_input(retaliation=True)
        runner = ScenarioRunner(
            initial_state=_state(
                entities={"USA": _entity("USA"), "CHN": _entity("CHN")}
            ),
            scheduled_inputs=[(1, inp)],
            modules=[],
            n_steps=1,
            audit_log=log,
        )
        runner.run()
        record = log.records[0]
        assert len(record.translated_events) == 2
