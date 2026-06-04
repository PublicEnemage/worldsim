"""Tests for G18 batch — Issue #89 (n_runs schema), #31 (multi-step duration),
#33 (CapitalFlowInput, DFICommitmentInput, ActorType), #36 (DebtProfile).
"""
from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from app.schemas import ScenarioConfigSchema
from app.simulation.engine.models import DebtProfile, SimulationEntity
from app.simulation.engine.quantity import Quantity, VariableType
from app.simulation.orchestration.inputs import (
    ActorType,
    CapitalFlowInput,
    CapitalFlowType,
    DFICommitmentInput,
    DFIInstrumentType,
    FiscalInstrument,
    FiscalPolicyInput,
    InputSource,
)
from app.simulation.orchestration.runner import (
    ScenarioRunner,
    _expand_multi_period_inputs,
    _period_scale,
)

_TS = datetime(2010, 1, 1, tzinfo=UTC)


# ---------------------------------------------------------------------------
# Issue #89 — n_runs on ScenarioConfigSchema
# ---------------------------------------------------------------------------


def test_scenario_config_schema_n_runs_default() -> None:
    cfg = ScenarioConfigSchema(entities=["GRC"], n_steps=3)
    assert cfg.n_runs == 1


def test_scenario_config_schema_n_runs_explicit() -> None:
    cfg = ScenarioConfigSchema(entities=["GRC"], n_steps=3, n_runs=100)
    assert cfg.n_runs == 100


def test_scenario_config_schema_n_runs_roundtrip() -> None:
    cfg = ScenarioConfigSchema(entities=["GRC"], n_steps=3, n_runs=50)
    data = cfg.model_dump()
    restored = ScenarioConfigSchema(**data)
    assert restored.n_runs == 50


# ---------------------------------------------------------------------------
# Issue #36 — DebtProfile dataclass and SimulationEntity integration
# ---------------------------------------------------------------------------


def _make_entity(entity_id: str = "GRC", **attrs: Decimal) -> SimulationEntity:
    quantities = {
        k: Quantity(value=v, unit="ratio", variable_type=VariableType.RATIO, confidence_tier=2)
        for k, v in attrs.items()
    }
    return SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes=quantities,
        metadata={},
    )


def test_debt_profile_basic_fields() -> None:
    dp = DebtProfile(
        total_pct_gdp=Decimal("0.85"),
        foreign_currency_pct=Decimal("0.35"),
        short_term_pct=Decimal("0.15"),
        domestic_holder_pct=Decimal("0.60"),
        multilateral_pct=Decimal("0.12"),
        interest_service_pct_revenue=Decimal("0.18"),
    )
    assert dp.total_pct_gdp == Decimal("0.85")
    assert dp.foreign_currency_pct == Decimal("0.35")
    assert not dp.is_elevated_rollover_risk()


def test_debt_profile_elevated_rollover_risk() -> None:
    dp = DebtProfile(
        total_pct_gdp=Decimal("0.70"),
        foreign_currency_pct=Decimal("0.70"),
        short_term_pct=Decimal("0.20"),
        domestic_holder_pct=Decimal("0.10"),
        multilateral_pct=Decimal("0.05"),
        interest_service_pct_revenue=Decimal("0.25"),
    )
    assert dp.is_elevated_rollover_risk()


def test_debt_profile_threshold_boundary() -> None:
    dp_below = DebtProfile(
        total_pct_gdp=Decimal("0.80"),
        foreign_currency_pct=Decimal("0.60"),
        short_term_pct=Decimal("0.10"),
        domestic_holder_pct=Decimal("0.40"),
        multilateral_pct=Decimal("0.10"),
        interest_service_pct_revenue=Decimal("0.15"),
    )
    # Exactly 0.60 is not > 0.60
    assert not dp_below.is_elevated_rollover_risk()


def test_simulation_entity_debt_profile_none_by_default() -> None:
    entity = _make_entity("GRC")
    assert entity.debt_profile is None


def test_simulation_entity_get_attribute_debt_profile_key() -> None:
    dp = DebtProfile(
        total_pct_gdp=Decimal("0.85"),
        foreign_currency_pct=Decimal("0.45"),
        short_term_pct=Decimal("0.12"),
        domestic_holder_pct=Decimal("0.55"),
        multilateral_pct=Decimal("0.08"),
        interest_service_pct_revenue=Decimal("0.20"),
    )
    entity = _make_entity("GRC")
    object.__setattr__(entity, "debt_profile", dp)

    qty = entity.get_attribute("debt_profile.foreign_currency_pct")
    assert qty is not None
    assert qty.value == Decimal("0.45")


def test_simulation_entity_get_attribute_value_debt_profile() -> None:
    dp = DebtProfile(
        total_pct_gdp=Decimal("1.20"),
        foreign_currency_pct=Decimal("0.65"),
        short_term_pct=Decimal("0.18"),
        domestic_holder_pct=Decimal("0.30"),
        multilateral_pct=Decimal("0.15"),
        interest_service_pct_revenue=Decimal("0.30"),
    )
    entity = _make_entity("GRC")
    object.__setattr__(entity, "debt_profile", dp)

    val = entity.get_attribute_value("debt_profile.foreign_currency_pct")
    assert val == Decimal("0.65")


def test_simulation_entity_get_attribute_unknown_key_returns_none() -> None:
    entity = _make_entity("GRC")
    assert entity.get_attribute("debt_profile.nonexistent") is None
    assert entity.get_attribute("nonexistent_attribute") is None


def test_simulation_entity_debt_profile_key_without_profile_returns_none() -> None:
    entity = _make_entity("GRC")
    # No debt_profile set — should return None, not raise
    assert entity.get_attribute("debt_profile.foreign_currency_pct") is None


# ---------------------------------------------------------------------------
# Issue #31 — duration_periods and decay_function on ControlInput base
# ---------------------------------------------------------------------------


def test_control_input_duration_periods_default() -> None:
    inp = FiscalPolicyInput(
        target_entity="GRC",
        instrument=FiscalInstrument.SPENDING_CHANGE,
        value=Decimal("-0.05"),
    )
    assert inp.duration_periods == 1
    assert inp.decay_function == "constant"


def test_control_input_duration_periods_explicit() -> None:
    inp = FiscalPolicyInput(
        target_entity="GRC",
        instrument=FiscalInstrument.SPENDING_CHANGE,
        value=Decimal("-0.05"),
        duration_periods=3,
        decay_function="linear_decay",
    )
    assert inp.duration_periods == 3
    assert inp.decay_function == "linear_decay"


def test_period_scale_constant() -> None:
    for p in range(1, 6):
        assert _period_scale("constant", p, 5) == pytest.approx(1.0)


def test_period_scale_linear_decay() -> None:
    # period=1: scale=1.0; period=2: scale=0.8; period=3: scale=0.6, etc.
    assert _period_scale("linear_decay", 1, 5) == pytest.approx(1.0)
    assert _period_scale("linear_decay", 2, 5) == pytest.approx(0.8)
    assert _period_scale("linear_decay", 3, 5) == pytest.approx(0.6)
    assert _period_scale("linear_decay", 5, 5) == pytest.approx(0.2)


def test_period_scale_exponential_decay() -> None:
    assert _period_scale("exponential_decay", 1, 5) == pytest.approx(1.0)
    assert _period_scale("exponential_decay", 2, 5) == pytest.approx(0.5)
    assert _period_scale("exponential_decay", 3, 5) == pytest.approx(0.25)


def test_expand_multi_period_inputs_single_period() -> None:
    inp = FiscalPolicyInput(
        target_entity="GRC",
        instrument=FiscalInstrument.SPENDING_CHANGE,
        value=Decimal("-0.05"),
        duration_periods=1,
    )
    expanded = _expand_multi_period_inputs([(1, inp)], n_steps=5)
    assert len(expanded) == 1
    assert expanded[0] == (1, inp)


def test_expand_multi_period_inputs_three_periods() -> None:
    inp = FiscalPolicyInput(
        target_entity="GRC",
        instrument=FiscalInstrument.SPENDING_CHANGE,
        value=Decimal("-0.05"),
        duration_periods=3,
        decay_function="constant",
    )
    expanded = _expand_multi_period_inputs([(1, inp)], n_steps=5)
    # Original + 2 continuations
    assert len(expanded) == 3
    steps = sorted(s for s, _ in expanded)
    assert steps == [1, 2, 3]


def test_expand_multi_period_inputs_clamps_to_n_steps() -> None:
    inp = FiscalPolicyInput(
        target_entity="GRC",
        instrument=FiscalInstrument.SPENDING_CHANGE,
        value=Decimal("-0.05"),
        duration_periods=10,
        decay_function="constant",
    )
    expanded = _expand_multi_period_inputs([(1, inp)], n_steps=3)
    # Only steps 1, 2, 3 — step 4+ is clamped
    steps = sorted(s for s, _ in expanded)
    assert steps == [1, 2, 3]


def test_expand_multi_period_inputs_linear_decay_scales_capacity() -> None:
    inp = FiscalPolicyInput(
        target_entity="GRC",
        instrument=FiscalInstrument.SPENDING_CHANGE,
        value=Decimal("-0.05"),
        duration_periods=3,
        decay_function="linear_decay",
        implementation_capacity=Decimal("1.0"),
    )
    expanded = _expand_multi_period_inputs([(1, inp)], n_steps=5)
    by_step = dict(expanded)

    # Period 2 scale = 1 - 1/3 ≈ 0.667
    assert float(by_step[2].implementation_capacity) == pytest.approx(0.6667, abs=1e-4)
    # Period 3 scale = 1 - 2/3 ≈ 0.333
    assert float(by_step[3].implementation_capacity) == pytest.approx(0.3333, abs=1e-4)


def test_scenario_runner_multi_step_injection() -> None:
    """Integration: multi-period input fires at three steps in run()."""
    from datetime import UTC, datetime

    from app.simulation.engine.models import (
        ResolutionConfig,
        ResolutionLevel,
        ScenarioConfig,
        SimulationState,
    )

    entities = {
        "GRC": SimulationEntity(
            id="GRC",
            entity_type="country",
            attributes={
                "gdp_growth_rate": Quantity(
                    value=Decimal("-3.0"),
                    unit="percent",
                    variable_type=VariableType.RATIO,
                    confidence_tier=1,
                )
            },
            metadata={},
        )
    }
    ts = datetime(2010, 1, 1, tzinfo=UTC)
    state = SimulationState(
        timestep=ts,
        resolution=ResolutionConfig(global_level=ResolutionLevel.NATION_STATE),
        entities=entities,
        relationships=[],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="test-g18",
            name="G18 Test",
            description="",
            start_date=ts,
            end_date=datetime(2016, 1, 1, tzinfo=UTC),
        ),
    )

    fiscal_inp = FiscalPolicyInput(
        target_entity="GRC",
        instrument=FiscalInstrument.SPENDING_CHANGE,
        value=Decimal("0.01"),
        duration_periods=3,
        decay_function="constant",
    )

    runner = ScenarioRunner(
        initial_state=state,
        scheduled_inputs=[(1, fiscal_inp)],
        modules=[],
        n_steps=5,
    )
    history = runner.run()
    # 5 steps + initial = 6 states
    assert len(history) == 6
    # At step 3, the continuation should have fired — GDP still updated
    # (just verify no exception and expected history length)
    assert history[3].timestep.year == 2013


# ---------------------------------------------------------------------------
# Issue #33 — ActorType, CapitalFlowInput, DFICommitmentInput
# ---------------------------------------------------------------------------


def test_actor_type_enum_values() -> None:
    assert ActorType.PRIVATE_INVESTOR.value == "private_investor"
    assert ActorType.DFI.value == "dfi"
    assert ActorType.SOVEREIGN_INVESTOR.value == "sovereign_investor"
    assert ActorType.GOVERNMENT.value == "government"
    assert ActorType.CENTRAL_BANK.value == "central_bank"


def test_capital_flow_input_defaults() -> None:
    inp = CapitalFlowInput(target_entity="ARG")
    assert inp.flow_type == CapitalFlowType.FDI
    assert inp.volume == Decimal("0")
    assert inp.duration_periods == 1
    assert inp.actor_type is None


def test_capital_flow_input_to_events_fdi() -> None:
    inp = CapitalFlowInput(
        target_entity="ARG",
        flow_type=CapitalFlowType.FDI,
        volume=Decimal("0.03"),
        actor_type=ActorType.PRIVATE_INVESTOR,
    )
    events = inp.to_events(_TS)
    assert len(events) == 1
    evt = events[0]
    assert evt.source_entity_id == "ARG"
    assert "fdi_stock" in evt.affected_attributes
    assert evt.affected_attributes["fdi_stock"].value == Decimal("0.03")
    assert evt.event_type == "capital_flow_fdi"


def test_capital_flow_input_to_events_portfolio() -> None:
    inp = CapitalFlowInput(
        target_entity="GRC",
        flow_type=CapitalFlowType.PORTFOLIO_INVESTMENT,
        volume=Decimal("-0.05"),
    )
    events = inp.to_events(_TS)
    assert events[0].affected_attributes["portfolio_flows"].value == Decimal("-0.05")
    assert events[0].event_type == "capital_flow_portfolio_investment"


def test_capital_flow_input_to_events_sovereign_debt() -> None:
    inp = CapitalFlowInput(
        target_entity="GRC",
        flow_type=CapitalFlowType.SOVEREIGN_DEBT,
        volume=Decimal("0.10"),
    )
    events = inp.to_events(_TS)
    assert "reserve_adequacy" in events[0].affected_attributes


def test_dfi_commitment_input_defaults() -> None:
    inp = DFICommitmentInput(target_entity="ETH")
    assert inp.instrument == DFIInstrumentType.GUARANTEE
    assert inp.volume == Decimal("0")
    assert inp.dfi_actor == ""


def test_dfi_commitment_input_to_events() -> None:
    inp = DFICommitmentInput(
        target_entity="ETH",
        instrument=DFIInstrumentType.CONCESSIONAL_LOAN,
        volume=Decimal("0.02"),
        dfi_actor="AfDB",
        actor_type=ActorType.DFI,
        actor_id="AfDB",
    )
    events = inp.to_events(_TS)
    assert len(events) == 1
    evt = events[0]
    assert evt.source_entity_id == "ETH"
    assert "fdi_stock" in evt.affected_attributes
    assert evt.affected_attributes["fdi_stock"].value == Decimal("0.02")
    assert evt.event_type == "dfi_commitment_concessional_loan"
    assert evt.metadata["dfi_actor"] == "AfDB"


def test_control_input_actor_type_field() -> None:
    inp = CapitalFlowInput(
        target_entity="GRC",
        volume=Decimal("0.01"),
        actor_type=ActorType.SOVEREIGN_INVESTOR,
        source=InputSource.SCENARIO_SCRIPT,
    )
    assert inp.actor_type == ActorType.SOVEREIGN_INVESTOR
