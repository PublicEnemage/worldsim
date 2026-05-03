"""Unit tests for Argentina 2001–2002 backtesting fixtures — Issue #192.

Covers:
  - ArgentinaActuals field values match documented IMF WEO / INDEC EPH data
  - FidelityThresholds are set correctly
  - build_argentina_scenario() returns a valid ScenarioCreateRequest
  - All Quantity values in the fixture are strings (float prohibition)
  - IA1_DISCLOSURE matches IA1_CANONICAL_PHRASE
  - PARAMETER_CALIBRATION_DISCLOSURE is non-empty
  - fidelity_report helpers work with entity_id="ARG"

All tests run without a database connection.
"""
from __future__ import annotations

from decimal import Decimal

import pytest

from tests.backtesting.fidelity_report import (
    _extract_gdp_value,
    format_fidelity_report,
)
from tests.fixtures.argentina_2001_2002_actuals import (
    ACTUALS,
    IA1_DISCLOSURE,
    PARAMETER_CALIBRATION_DISCLOSURE,
    THRESHOLDS,
)
from tests.fixtures.argentina_2001_2002_scenario import build_argentina_scenario

# ---------------------------------------------------------------------------
# ArgentinaActuals
# ---------------------------------------------------------------------------


def test_actuals_gdp_2001_matches_imf_weo() -> None:
    """GDP growth 2001: IMF WEO Apr 2002 outturn -4.4%."""
    assert ACTUALS.gdp_growth_2001 == Decimal("-0.044")
    assert isinstance(ACTUALS.gdp_growth_2001, Decimal)


def test_actuals_gdp_2002_matches_imf_weo() -> None:
    """GDP growth 2002: IMF WEO Apr 2003 outturn -10.9%."""
    assert ACTUALS.gdp_growth_2002 == Decimal("-0.109")
    assert isinstance(ACTUALS.gdp_growth_2002, Decimal)


def test_actuals_unemployment_2001() -> None:
    """INDEC EPH May 2001 — 16.4%."""
    assert ACTUALS.unemployment_rate_2001 == Decimal("0.164")


def test_actuals_unemployment_2002() -> None:
    """INDEC EPH May 2002 — 21.5%."""
    assert ACTUALS.unemployment_rate_2002 == Decimal("0.215")


def test_actuals_both_gdp_values_are_negative() -> None:
    """Both historical GDP growth rates are negative (crisis contraction)."""
    assert ACTUALS.gdp_growth_2001 < Decimal("0")
    assert ACTUALS.gdp_growth_2002 < Decimal("0")


def test_actuals_gdp_2002_deeper_than_2001() -> None:
    """2002 contraction was deeper than 2001 (-10.9% vs -4.4%)."""
    assert ACTUALS.gdp_growth_2002 < ACTUALS.gdp_growth_2001


def test_actuals_unemployment_rises_2001_to_2002() -> None:
    """Unemployment rose from 16.4% to 21.5% during the crisis."""
    assert ACTUALS.unemployment_rate_2001 < ACTUALS.unemployment_rate_2002


def test_actuals_is_frozen_dataclass() -> None:
    """ArgentinaActuals is immutable (frozen=True)."""
    with pytest.raises(AttributeError):
        ACTUALS.gdp_growth_2001 = Decimal("0")  # type: ignore[misc]


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


# ---------------------------------------------------------------------------
# build_argentina_scenario()
# ---------------------------------------------------------------------------


def test_build_argentina_scenario_returns_scenario_create_request() -> None:
    from app.schemas import ScenarioCreateRequest
    scenario = build_argentina_scenario()
    assert isinstance(scenario, ScenarioCreateRequest)


def test_build_argentina_scenario_name_contains_argentina() -> None:
    scenario = build_argentina_scenario()
    assert "Argentina" in scenario.name
    assert "2001" in scenario.name


def test_build_argentina_scenario_has_arg_entity() -> None:
    scenario = build_argentina_scenario()
    assert "ARG" in scenario.configuration.entities


def test_build_argentina_scenario_n_steps_is_2() -> None:
    scenario = build_argentina_scenario()
    assert scenario.configuration.n_steps == 2


def test_build_argentina_scenario_timestep_label_is_annual() -> None:
    scenario = build_argentina_scenario()
    assert scenario.configuration.timestep_label == "annual"


def test_build_argentina_scenario_has_scheduled_inputs() -> None:
    scenario = build_argentina_scenario()
    assert len(scenario.scheduled_inputs) >= 2


def test_build_argentina_scenario_all_quantity_values_are_strings() -> None:
    """Float prohibition: all QuantitySchema.value fields must be strings."""
    scenario = build_argentina_scenario()
    for entity_id, attrs in scenario.configuration.initial_attributes.items():
        for attr_key, qty in attrs.items():
            assert isinstance(qty.value, str), (
                f"Float prohibition: {entity_id}.{attr_key}.value "
                f"is {type(qty.value).__name__}, expected str"
            )


def test_build_argentina_scenario_initial_gdp_growth_is_string() -> None:
    scenario = build_argentina_scenario()
    gdp = scenario.configuration.initial_attributes["ARG"]["gdp_growth"]
    assert gdp.value == "-0.008"
    assert isinstance(gdp.value, str)


def test_build_argentina_scenario_initial_gdp_growth_is_negative() -> None:
    """Initial GDP growth must be negative (2000 Argentine recession)."""
    scenario = build_argentina_scenario()
    gdp = scenario.configuration.initial_attributes["ARG"]["gdp_growth"]
    assert Decimal(gdp.value) < Decimal("0")


def test_build_argentina_scenario_initial_unemployment_rate() -> None:
    """INDEC EPH October 2000 — 14.7%."""
    scenario = build_argentina_scenario()
    unemp = scenario.configuration.initial_attributes["ARG"]["unemployment_rate"]
    assert unemp.value == "0.147"
    assert unemp.source_registry_id == "INDEC_EPH_2000"
    assert unemp.measurement_framework == "human_development"


def test_build_argentina_scenario_has_fiscal_input_at_step1() -> None:
    """Step 1 must include a FiscalPolicyInput (Zero Deficit Plan)."""
    scenario = build_argentina_scenario()
    fiscal_inputs = [
        si for si in scenario.scheduled_inputs
        if si.input_type == "FiscalPolicyInput" and si.step == 1
    ]
    assert len(fiscal_inputs) >= 1
    spending_cut = fiscal_inputs[0]
    assert spending_cut.input_data["instrument"] == "spending_change"
    assert Decimal(spending_cut.input_data["value"]) < Decimal("0")


def test_build_argentina_scenario_has_imf_program_at_step1() -> None:
    """Step 1 must include an IMF program acceptance (Blindaje)."""
    scenario = build_argentina_scenario()
    emergency_inputs = [
        si for si in scenario.scheduled_inputs
        if si.input_type == "EmergencyPolicyInput" and si.step == 1
    ]
    assert len(emergency_inputs) >= 1
    imf = emergency_inputs[0]
    assert imf.input_data["instrument"] == "imf_program_acceptance"


def test_build_argentina_scenario_scheduled_input_values_are_strings() -> None:
    """Float prohibition extends to scheduled input value fields."""
    scenario = build_argentina_scenario()
    for si in scenario.scheduled_inputs:
        if "value" in si.input_data:
            assert isinstance(si.input_data["value"], str), (
                f"Float prohibition: step={si.step} value is "
                f"{type(si.input_data['value']).__name__}, expected str"
            )


def test_build_argentina_scenario_scheduled_steps_in_valid_range() -> None:
    """All scheduled input steps must be within [0, n_steps]."""
    scenario = build_argentina_scenario()
    n = scenario.configuration.n_steps
    for si in scenario.scheduled_inputs:
        assert 0 <= si.step <= n, (
            f"Scheduled input step {si.step} outside valid range [0, {n}]"
        )


def test_build_argentina_scenario_input_types_are_known() -> None:
    """All scheduled input types must be recognized by _deserialize_control_input."""
    known_types = {
        "FiscalPolicyInput",
        "EmergencyPolicyInput",
        "TradePolicyInput",
        "MonetaryRateInput",
        "StructuralPolicyInput",
    }
    scenario = build_argentina_scenario()
    for si in scenario.scheduled_inputs:
        assert si.input_type in known_types, (
            f"Unknown input_type: {si.input_type!r}"
        )


# ---------------------------------------------------------------------------
# fidelity_report helpers with entity_id="ARG"
# ---------------------------------------------------------------------------


def _make_arg_snapshot(gdp_value: str = "-0.044") -> list[dict]:
    envelope = {
        "_envelope_version": "1",
        "value": gdp_value,
        "unit": "ratio",
        "variable_type": "ratio",
        "confidence_tier": 2,
        "observation_date": None,
        "source_registry_id": None,
        "measurement_framework": "financial",
    }
    return [
        {
            "step": s,
            "timestep": f"200{s}-01-01T00:00:00+00:00",
            "state_data": {"ARG": {"gdp_growth": envelope}},
        }
        for s in range(3)
    ]


def test_extract_gdp_value_arg_entity() -> None:
    """_extract_gdp_value must return the ARG value when entity_id='ARG'."""
    snap = {"state_data": {"ARG": {"gdp_growth": {"value": "-0.044"}}}}
    result = _extract_gdp_value(snap, entity_id="ARG")
    assert result == Decimal("-0.044")
    assert isinstance(result, Decimal)


def test_extract_gdp_value_arg_returns_none_for_grc_data() -> None:
    """ARG extraction must return None when only GRC data is present."""
    snap = {"state_data": {"GRC": {"gdp_growth": {"value": "-0.054"}}}}
    result = _extract_gdp_value(snap, entity_id="ARG")
    assert result is None


def test_format_fidelity_report_with_arg_entity() -> None:
    """format_fidelity_report must work with entity_id='ARG'."""
    report = format_fidelity_report(
        scenario_name="Argentina Test",
        actuals=ACTUALS,
        snapshots=_make_arg_snapshot(),
        thresholds_met={"gdp_step1_negative": True, "gdp_step2_negative": True},
        ia1_disclosure=IA1_DISCLOSURE,
        parameter_calibration_disclosure=PARAMETER_CALIBRATION_DISCLOSURE,
        entity_id="ARG",
    )
    assert isinstance(report, str)
    assert len(report) > 100
    assert "Overall: PASS" in report
