"""Unit tests for MacroeconomicModule — ADR-006 Decisions 8 and 10.

Coverage:
  1. Non-country entity → empty result.
  2. No prior events → empty result.
  3. Regime detection — standard (growth >= 0).
  4. Regime detection — depressed (-0.03 <= growth < 0).
  5. Regime detection — ZLB (growth < -0.03).
  6. GDP computation — standard multiplier (0.5).
  7. GDP computation — depressed multiplier (1.5).
  8. GDP computation — ZLB multiplier (2.0).
  9. Fiscal balance improves on spending cut.
  10. Fiscal balance improves on tax increase.
  11. Inflation decreases on spending cut.
  12. Inflation increases on tax increase.
  13. gdp_growth_change event emitted with correct affected_attributes key.
  14. gdp_growth_change event has empty propagation_rules (no graph propagation).
  15. regime_change event emitted on standard → depressed transition.
  16. regime_change event emitted on depressed → ZLB transition.
  17. No regime_change event when regime stays the same.
  18. regime_change metadata carries previous/new regime and threshold.
  19. Multiple fiscal events in same step accumulate gdp_delta.
  20. get_subscribed_events returns all expected types.
"""
from __future__ import annotations

from decimal import Decimal
from datetime import datetime, timezone

import pytest

from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.engine.quantity import Quantity, VariableType
from app.simulation.modules.macroeconomic.module import (
    FISCAL_MULTIPLIERS,
    MacroeconomicModule,
    _detect_regime,
)

_TS = datetime(2010, 1, 1, tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_state(
    entity_id: str = "GRC",
    entity_type: str = "country",
    gdp_growth: str = "0",
    prior_events: list[Event] | None = None,
) -> SimulationState:
    entity = SimulationEntity(
        id=entity_id,
        entity_type=entity_type,
        attributes={
            "gdp_growth": Quantity(
                value=Decimal(gdp_growth),
                unit="ratio",
                variable_type=VariableType.RATIO,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=1,
            )
        } if gdp_growth != "missing" else {},
        metadata={},
    )
    return SimulationState(
        timestep=_TS,
        resolution=ResolutionConfig(),
        entities={entity_id: entity},
        relationships=[],
        events=prior_events or [],
        scenario_config=ScenarioConfig(
            scenario_id="test-sid",
            name="Test",
            description="",
            start_date=_TS,
            end_date=_TS,
        ),
    )


def _fiscal_spending_event(
    source_entity_id: str,
    value: str,
) -> Event:
    return Event(
        event_id=f"fiscal-spending-{source_entity_id}",
        source_entity_id=source_entity_id,
        event_type="fiscal_policy_spending_change",
        affected_attributes={
            "fiscal_spending_change": Quantity(
                value=Decimal(value),
                unit="ratio",
                variable_type=VariableType.RATIO,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=1,
            )
        },
        propagation_rules=[],
        timestep_originated=_TS,
        framework=MeasurementFramework.FINANCIAL,
    )


def _fiscal_tax_event(
    source_entity_id: str,
    value: str,
) -> Event:
    return Event(
        event_id=f"fiscal-tax-{source_entity_id}",
        source_entity_id=source_entity_id,
        event_type="fiscal_policy_tax_rate_change",
        affected_attributes={
            "fiscal_tax_rate_change": Quantity(
                value=Decimal(value),
                unit="ratio",
                variable_type=VariableType.RATIO,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=1,
            )
        },
        propagation_rules=[],
        timestep_originated=_TS,
        framework=MeasurementFramework.FINANCIAL,
    )


# ---------------------------------------------------------------------------
# Regime detection
# ---------------------------------------------------------------------------


def test_detect_regime_standard_at_zero() -> None:
    assert _detect_regime(Decimal("0")) == "standard"


def test_detect_regime_standard_positive() -> None:
    assert _detect_regime(Decimal("0.03")) == "standard"


def test_detect_regime_depressed_just_below_zero() -> None:
    assert _detect_regime(Decimal("-0.001")) == "depressed"


def test_detect_regime_depressed_at_lower_boundary() -> None:
    # -0.03 is included in depressed: [-0.03, 0) per ADR-006.
    assert _detect_regime(Decimal("-0.03")) == "depressed"


def test_detect_regime_zlb_just_below_threshold() -> None:
    # Strictly below -0.03 → ZLB.
    assert _detect_regime(Decimal("-0.031")) == "zlb"


def test_detect_regime_zlb_deeply_negative() -> None:
    assert _detect_regime(Decimal("-0.109")) == "zlb"


def test_fiscal_multipliers_have_correct_values() -> None:
    assert FISCAL_MULTIPLIERS["standard"] == Decimal("0.5")
    assert FISCAL_MULTIPLIERS["depressed"] == Decimal("1.5")
    assert FISCAL_MULTIPLIERS["zlb"] == Decimal("2.0")


# ---------------------------------------------------------------------------
# Non-country entity / no events
# ---------------------------------------------------------------------------


def test_non_country_entity_returns_empty() -> None:
    module = MacroeconomicModule()
    state = _make_state(entity_type="cohort")
    entity = state.entities["GRC"]
    assert module.compute(entity, state, _TS) == []


def test_no_prior_events_returns_empty() -> None:
    module = MacroeconomicModule()
    state = _make_state(gdp_growth="-0.054", prior_events=[])
    entity = state.entities["GRC"]
    assert module.compute(entity, state, _TS) == []


def test_unrelated_event_type_ignored() -> None:
    module = MacroeconomicModule()
    event = Event(
        event_id="dummy",
        source_entity_id="GRC",
        event_type="meteor_strike",
        affected_attributes={},
        propagation_rules=[],
        timestep_originated=_TS,
    )
    state = _make_state(prior_events=[event])
    assert module.compute(state.entities["GRC"], state, _TS) == []


# ---------------------------------------------------------------------------
# GDP computation at each regime
# ---------------------------------------------------------------------------


def test_gdp_computation_standard_regime() -> None:
    spending_cut = Decimal("-0.05")
    state = _make_state(
        gdp_growth="0.02",  # standard regime
        prior_events=[_fiscal_spending_event("GRC", str(spending_cut))],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)

    gdp_event = next(e for e in events if e.event_type == "gdp_growth_change")
    gdp_delta = gdp_event.affected_attributes["gdp_growth"].value
    expected = spending_cut * Decimal("0.5")
    assert gdp_delta == expected


def test_gdp_computation_depressed_regime() -> None:
    spending_cut = Decimal("-0.05")
    state = _make_state(
        gdp_growth="-0.01",  # depressed regime
        prior_events=[_fiscal_spending_event("GRC", str(spending_cut))],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)

    gdp_event = next(e for e in events if e.event_type == "gdp_growth_change")
    gdp_delta = gdp_event.affected_attributes["gdp_growth"].value
    expected = spending_cut * Decimal("1.5")
    assert gdp_delta == expected


def test_gdp_computation_zlb_regime() -> None:
    spending_cut = Decimal("-0.05")
    state = _make_state(
        gdp_growth="-0.054",  # ZLB regime
        prior_events=[_fiscal_spending_event("GRC", str(spending_cut))],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)

    gdp_event = next(e for e in events if e.event_type == "gdp_growth_change")
    gdp_delta = gdp_event.affected_attributes["gdp_growth"].value
    expected = spending_cut * Decimal("2.0")
    assert gdp_delta == expected


# ---------------------------------------------------------------------------
# Fiscal balance tracking
# ---------------------------------------------------------------------------


def test_fiscal_balance_improves_on_spending_cut() -> None:
    spending_cut = Decimal("-0.05")
    state = _make_state(
        gdp_growth="-0.054",
        prior_events=[_fiscal_spending_event("GRC", str(spending_cut))],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)

    gdp_event = next(e for e in events if e.event_type == "gdp_growth_change")
    fiscal_delta = gdp_event.affected_attributes["fiscal_balance_pct_gdp"].value
    # Spending cut improves balance: fiscal_delta = -spending_cut = +0.05
    assert fiscal_delta == Decimal("0.05")


def test_fiscal_balance_improves_on_tax_increase() -> None:
    tax_increase = Decimal("0.02")
    state = _make_state(
        gdp_growth="-0.054",
        prior_events=[_fiscal_tax_event("GRC", str(tax_increase))],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)

    gdp_event = next(e for e in events if e.event_type == "gdp_growth_change")
    fiscal_delta = gdp_event.affected_attributes["fiscal_balance_pct_gdp"].value
    assert fiscal_delta == tax_increase


# ---------------------------------------------------------------------------
# Inflation dynamics
# ---------------------------------------------------------------------------


def test_inflation_decreases_on_spending_cut() -> None:
    spending_cut = Decimal("-0.05")
    state = _make_state(
        gdp_growth="-0.054",
        prior_events=[_fiscal_spending_event("GRC", str(spending_cut))],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)

    gdp_event = next(e for e in events if e.event_type == "gdp_growth_change")
    inflation_delta = gdp_event.affected_attributes["inflation_rate"].value
    assert inflation_delta < Decimal("0")


def test_inflation_increases_on_tax_hike() -> None:
    tax_increase = Decimal("0.03")
    state = _make_state(
        gdp_growth="-0.054",
        prior_events=[_fiscal_tax_event("GRC", str(tax_increase))],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)

    gdp_event = next(e for e in events if e.event_type == "gdp_growth_change")
    inflation_delta = gdp_event.affected_attributes["inflation_rate"].value
    assert inflation_delta > Decimal("0")


# ---------------------------------------------------------------------------
# gdp_growth_change event structure
# ---------------------------------------------------------------------------


def test_gdp_growth_change_event_emitted() -> None:
    state = _make_state(
        gdp_growth="0",
        prior_events=[_fiscal_spending_event("GRC", "-0.03")],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)
    event_types = [e.event_type for e in events]
    assert "gdp_growth_change" in event_types


def test_gdp_growth_change_has_gdp_growth_attribute_key() -> None:
    state = _make_state(
        gdp_growth="0",
        prior_events=[_fiscal_spending_event("GRC", "-0.03")],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)
    gdp_event = next(e for e in events if e.event_type == "gdp_growth_change")
    assert "gdp_growth" in gdp_event.affected_attributes


def test_gdp_growth_change_has_empty_propagation_rules() -> None:
    state = _make_state(
        gdp_growth="0",
        prior_events=[_fiscal_spending_event("GRC", "-0.03")],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)
    gdp_event = next(e for e in events if e.event_type == "gdp_growth_change")
    assert gdp_event.propagation_rules == []


def test_gdp_growth_value_is_decimal_not_float() -> None:
    state = _make_state(
        gdp_growth="0",
        prior_events=[_fiscal_spending_event("GRC", "-0.03")],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)
    gdp_event = next(e for e in events if e.event_type == "gdp_growth_change")
    assert isinstance(gdp_event.affected_attributes["gdp_growth"].value, Decimal)


# ---------------------------------------------------------------------------
# regime_change event emission
# ---------------------------------------------------------------------------


def test_regime_change_event_emitted_standard_to_depressed() -> None:
    # GDP starts at 0 (standard). Spending cut of -0.03 * 0.5 = -0.015 → new GDP = -0.015 (depressed).
    state = _make_state(
        gdp_growth="0",
        prior_events=[_fiscal_spending_event("GRC", "-0.03")],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)
    event_types = [e.event_type for e in events]
    assert "regime_change" in event_types


def test_regime_change_event_emitted_depressed_to_zlb() -> None:
    # GDP starts at -0.02 (depressed). Spending cut of -0.02 * 1.5 = -0.03 → new GDP = -0.05 (ZLB).
    state = _make_state(
        gdp_growth="-0.02",
        prior_events=[_fiscal_spending_event("GRC", "-0.02")],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)
    event_types = [e.event_type for e in events]
    assert "regime_change" in event_types


def test_no_regime_change_event_when_regime_stays_same() -> None:
    # GDP starts at -0.054 (ZLB). Small cut → stays in ZLB.
    state = _make_state(
        gdp_growth="-0.054",
        prior_events=[_fiscal_spending_event("GRC", "-0.001")],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)
    event_types = [e.event_type for e in events]
    assert "regime_change" not in event_types


def test_regime_change_metadata_correct() -> None:
    # standard (gdp=0) → depressed after cut
    state = _make_state(
        gdp_growth="0",
        prior_events=[_fiscal_spending_event("GRC", "-0.03")],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)
    regime_event = next(e for e in events if e.event_type == "regime_change")
    assert regime_event.metadata["regime_previous"] == "standard"
    assert regime_event.metadata["regime_new"] == "depressed"
    assert "trigger_value" in regime_event.metadata
    assert "threshold" in regime_event.metadata


def test_regime_change_has_empty_affected_attributes() -> None:
    state = _make_state(
        gdp_growth="0",
        prior_events=[_fiscal_spending_event("GRC", "-0.03")],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)
    regime_event = next(e for e in events if e.event_type == "regime_change")
    assert regime_event.affected_attributes == {}


# ---------------------------------------------------------------------------
# Multiple fiscal events accumulate
# ---------------------------------------------------------------------------


def test_multiple_spending_events_accumulate_gdp_delta() -> None:
    state = _make_state(
        gdp_growth="0.02",
        prior_events=[
            _fiscal_spending_event("GRC", "-0.03"),
            _fiscal_spending_event("GRC", "-0.02"),
        ],
    )
    module = MacroeconomicModule()
    events = module.compute(state.entities["GRC"], state, _TS)
    gdp_event = next(e for e in events if e.event_type == "gdp_growth_change")
    # standard multiplier 0.5; total spending cut = -0.05; gdp_delta = -0.025
    assert gdp_event.affected_attributes["gdp_growth"].value == Decimal("-0.025")


# ---------------------------------------------------------------------------
# get_subscribed_events
# ---------------------------------------------------------------------------


def test_get_subscribed_events_includes_fiscal_spending() -> None:
    module = MacroeconomicModule()
    assert "fiscal_policy_spending_change" in module.get_subscribed_events()


def test_get_subscribed_events_includes_fiscal_tax() -> None:
    module = MacroeconomicModule()
    assert "fiscal_policy_tax_rate_change" in module.get_subscribed_events()


def test_get_subscribed_events_includes_monetary_rate() -> None:
    module = MacroeconomicModule()
    assert "monetary_policy_policy_rate" in module.get_subscribed_events()
