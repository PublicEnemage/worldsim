"""Unit tests for Thailand 1997–2000 backtesting fixtures — Issue #141.

Covers:
  - ThailandActuals field values match documented IMF WEO / WDI sources
  - FidelityThresholds are set correctly
  - build_thailand_scenario() returns a valid ScenarioCreateRequest
  - All Quantity values in the fixture are strings (float prohibition)
  - IA1_DISCLOSURE matches IA1_CANONICAL_PHRASE
  - PARAMETER_CALIBRATION_DISCLOSURE is non-empty and references DIRECTION_ONLY
  - fidelity_report helpers work with entity_id="THA"

All tests run without a database connection.
"""
from __future__ import annotations

from decimal import Decimal

import pytest

from tests.backtesting.fidelity_report import (
    _extract_gdp_value,
    format_fidelity_report,
)
from tests.fixtures.thailand_1997_2000_actuals import (
    ACTUALS,
    IA1_DISCLOSURE,
    PARAMETER_CALIBRATION_DISCLOSURE,
    THRESHOLDS,
)
from tests.fixtures.thailand_1997_2000_scenario import build_thailand_scenario

# ---------------------------------------------------------------------------
# ThailandActuals
# ---------------------------------------------------------------------------


def test_actuals_gdp_1997_matches_imf_weo() -> None:
    """GDP growth 1997: IMF WEO Oct 1998 outturn -1.4%."""
    assert ACTUALS.gdp_growth_1997 == Decimal("-0.014")
    assert isinstance(ACTUALS.gdp_growth_1997, Decimal)


def test_actuals_gdp_1998_matches_imf_weo() -> None:
    """GDP growth 1998: IMF WEO Apr 1999 outturn -10.5%."""
    assert ACTUALS.gdp_growth_1998 == Decimal("-0.105")
    assert isinstance(ACTUALS.gdp_growth_1998, Decimal)


def test_actuals_unemployment_1997() -> None:
    """World Bank WDI 1997 ILO-modelled — 1.5%."""
    assert ACTUALS.unemployment_rate_1997 == Decimal("0.015")


def test_actuals_unemployment_1998() -> None:
    """World Bank WDI 1998 ILO-modelled — 3.4% (structural undercount noted)."""
    assert ACTUALS.unemployment_rate_1998 == Decimal("0.034")


def test_actuals_both_gdp_values_are_negative() -> None:
    """Both historical GDP growth rates are negative (crisis contraction)."""
    assert ACTUALS.gdp_growth_1997 < Decimal("0")
    assert ACTUALS.gdp_growth_1998 < Decimal("0")


def test_actuals_gdp_1998_deeper_than_1997() -> None:
    """1998 contraction was deeper than 1997 (-10.5% vs -1.4%)."""
    assert ACTUALS.gdp_growth_1998 < ACTUALS.gdp_growth_1997


def test_actuals_unemployment_rises_1997_to_1998() -> None:
    """Unemployment rose from 1.5% to 3.4% during the crisis."""
    assert ACTUALS.unemployment_rate_1997 < ACTUALS.unemployment_rate_1998


def test_actuals_is_frozen_dataclass() -> None:
    """ThailandActuals is immutable (frozen=True)."""
    with pytest.raises(AttributeError):
        ACTUALS.gdp_growth_1997 = Decimal("0")  # type: ignore[misc]


# ---------------------------------------------------------------------------
# FidelityThresholds
# ---------------------------------------------------------------------------


def test_thresholds_gdp_direction_step1_is_true() -> None:
    assert THRESHOLDS.gdp_direction_step1_correct is True


def test_thresholds_gdp_direction_step2_is_true() -> None:
    assert THRESHOLDS.gdp_direction_step2_correct is True


def test_thresholds_is_frozen_dataclass() -> None:
    with pytest.raises(AttributeError):
        THRESHOLDS.gdp_direction_step1_correct = False  # type: ignore[misc]


# ---------------------------------------------------------------------------
# IA1_DISCLOSURE
# ---------------------------------------------------------------------------


def test_ia1_disclosure_matches_canonical_phrase() -> None:
    from app.simulation.repositories.quantity_serde import IA1_CANONICAL_PHRASE
    assert IA1_DISCLOSURE == IA1_CANONICAL_PHRASE


def test_ia1_disclosure_is_non_empty() -> None:
    assert IA1_DISCLOSURE
    assert len(IA1_DISCLOSURE) > 30


# ---------------------------------------------------------------------------
# PARAMETER_CALIBRATION_DISCLOSURE
# ---------------------------------------------------------------------------


def test_parameter_calibration_disclosure_is_non_empty() -> None:
    assert PARAMETER_CALIBRATION_DISCLOSURE
    assert len(PARAMETER_CALIBRATION_DISCLOSURE) > 30


def test_parameter_calibration_disclosure_references_direction_only() -> None:
    assert "DIRECTION_ONLY" in PARAMETER_CALIBRATION_DISCLOSURE


def test_parameter_calibration_disclosure_references_thailand() -> None:
    assert "Thailand" in PARAMETER_CALIBRATION_DISCLOSURE


# ---------------------------------------------------------------------------
# build_thailand_scenario()
# ---------------------------------------------------------------------------


def test_build_thailand_scenario_returns_scenario_create_request() -> None:
    from app.schemas import ScenarioCreateRequest
    scenario = build_thailand_scenario()
    assert isinstance(scenario, ScenarioCreateRequest)


def test_build_thailand_scenario_name_contains_thailand() -> None:
    scenario = build_thailand_scenario()
    assert "Thailand" in scenario.name
    assert "1997" in scenario.name


def test_build_thailand_scenario_has_tha_entity() -> None:
    scenario = build_thailand_scenario()
    assert "THA" in scenario.configuration.entities


def test_build_thailand_scenario_n_steps_is_2() -> None:
    scenario = build_thailand_scenario()
    assert scenario.configuration.n_steps == 2


def test_build_thailand_scenario_timestep_label_is_annual() -> None:
    scenario = build_thailand_scenario()
    assert scenario.configuration.timestep_label == "annual"


def test_build_thailand_scenario_has_scheduled_inputs() -> None:
    scenario = build_thailand_scenario()
    assert len(scenario.scheduled_inputs) >= 2


def test_build_thailand_scenario_all_quantity_values_are_strings() -> None:
    """Float prohibition: all QuantitySchema.value fields must be strings."""
    scenario = build_thailand_scenario()
    for entity_id, attrs in scenario.configuration.initial_attributes.items():
        for attr_key, qty in attrs.items():
            assert isinstance(qty.value, str), (
                f"Float prohibition: {entity_id}.{attr_key}.value "
                f"is {type(qty.value).__name__}, expected str"
            )


def test_build_thailand_scenario_initial_gdp_growth_is_string() -> None:
    scenario = build_thailand_scenario()
    gdp = scenario.configuration.initial_attributes["THA"]["gdp_growth"]
    assert gdp.value == "-0.010"
    assert isinstance(gdp.value, str)


def test_build_thailand_scenario_initial_gdp_growth_is_negative() -> None:
    """Initial GDP growth must be negative (early-1997 Thai deterioration)."""
    scenario = build_thailand_scenario()
    gdp = scenario.configuration.initial_attributes["THA"]["gdp_growth"]
    assert Decimal(gdp.value) < Decimal("0")


def test_build_thailand_scenario_initial_unemployment_rate() -> None:
    """World Bank WDI 1997 ILO-modelled — 1.5%."""
    scenario = build_thailand_scenario()
    unemp = scenario.configuration.initial_attributes["THA"]["unemployment_rate"]
    assert unemp.value == "0.015"
    assert unemp.source_registry_id == "WDI_THA_1997"
    assert unemp.measurement_framework == "human_development"


def test_build_thailand_scenario_has_capital_controls_at_step1() -> None:
    """Step 1 must include a capital controls EmergencyPolicyInput (peg abandonment)."""
    scenario = build_thailand_scenario()
    emergency_step1 = [
        si for si in scenario.scheduled_inputs
        if si.input_type == "EmergencyPolicyInput" and si.step == 1
    ]
    assert len(emergency_step1) >= 1
    instruments = {si.input_data["instrument"] for si in emergency_step1}
    assert "capital_controls" in instruments


def test_build_thailand_scenario_has_fiscal_input_at_step1() -> None:
    """Step 1 must include a FiscalPolicyInput (fiscal tightening)."""
    scenario = build_thailand_scenario()
    fiscal_inputs = [
        si for si in scenario.scheduled_inputs
        if si.input_type == "FiscalPolicyInput" and si.step == 1
    ]
    assert len(fiscal_inputs) >= 1
    spending_cut = fiscal_inputs[0]
    assert spending_cut.input_data["instrument"] == "spending_change"
    assert Decimal(spending_cut.input_data["value"]) < Decimal("0")


def test_build_thailand_scenario_has_imf_program_at_step2() -> None:
    """Step 2 must include an IMF program acceptance (USD 17.2bn package)."""
    scenario = build_thailand_scenario()
    emergency_step2 = [
        si for si in scenario.scheduled_inputs
        if si.input_type == "EmergencyPolicyInput" and si.step == 2
    ]
    assert len(emergency_step2) >= 1
    instruments = {si.input_data["instrument"] for si in emergency_step2}
    assert "imf_program_acceptance" in instruments


def test_build_thailand_scenario_scheduled_input_values_are_strings() -> None:
    """Float prohibition extends to scheduled input value fields."""
    scenario = build_thailand_scenario()
    for si in scenario.scheduled_inputs:
        if "value" in si.input_data:
            assert isinstance(si.input_data["value"], str), (
                f"Float prohibition: step={si.step} value is "
                f"{type(si.input_data['value']).__name__}, expected str"
            )


def test_build_thailand_scenario_scheduled_steps_in_valid_range() -> None:
    """All scheduled input steps must be within [0, n_steps]."""
    scenario = build_thailand_scenario()
    n = scenario.configuration.n_steps
    for si in scenario.scheduled_inputs:
        assert 0 <= si.step <= n, (
            f"Scheduled input step {si.step} outside valid range [0, {n}]"
        )


def test_build_thailand_scenario_input_types_are_known() -> None:
    """All scheduled input types must be recognized by _deserialize_control_input."""
    known_types = {
        "FiscalPolicyInput",
        "EmergencyPolicyInput",
        "TradePolicyInput",
        "MonetaryRateInput",
        "StructuralPolicyInput",
    }
    scenario = build_thailand_scenario()
    for si in scenario.scheduled_inputs:
        assert si.input_type in known_types, (
            f"Unknown input_type: {si.input_type!r}"
        )


# ---------------------------------------------------------------------------
# fidelity_report helpers with entity_id="THA"
# ---------------------------------------------------------------------------


def _make_tha_snapshot(gdp_value: str = "-0.014") -> list[dict]:
    envelope = {
        "_envelope_version": "1",
        "value": gdp_value,
        "unit": "ratio",
        "variable_type": "ratio",
        "confidence_tier": 3,
        "observation_date": None,
        "source_registry_id": None,
        "measurement_framework": "financial",
    }
    return [
        {
            "step": s,
            "timestep": f"199{7 + s}-01-01T00:00:00+00:00",
            "state_data": {"THA": {"gdp_growth": envelope}},
        }
        for s in range(3)
    ]


def test_extract_gdp_value_tha_entity() -> None:
    """_extract_gdp_value must return the THA value when entity_id='THA'."""
    snap = {"state_data": {"THA": {"gdp_growth": {"value": "-0.014"}}}}
    result = _extract_gdp_value(snap, entity_id="THA")
    assert result == Decimal("-0.014")
    assert isinstance(result, Decimal)


def test_extract_gdp_value_tha_returns_none_for_grc_data() -> None:
    """THA extraction must return None when only GRC data is present."""
    snap = {"state_data": {"GRC": {"gdp_growth": {"value": "-0.054"}}}}
    result = _extract_gdp_value(snap, entity_id="THA")
    assert result is None


def test_format_fidelity_report_with_tha_entity() -> None:
    """format_fidelity_report must work with entity_id='THA'."""
    report = format_fidelity_report(
        scenario_name="Thailand Test",
        actuals=ACTUALS,
        snapshots=_make_tha_snapshot(),
        thresholds_met={"gdp_step1_negative": True, "gdp_step2_negative": True},
        ia1_disclosure=IA1_DISCLOSURE,
        parameter_calibration_disclosure=PARAMETER_CALIBRATION_DISCLOSURE,
        entity_id="THA",
    )
    assert isinstance(report, str)
    assert len(report) > 100
    assert "Overall: PASS" in report
