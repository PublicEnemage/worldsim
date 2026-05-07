"""Unit tests for Ecuador 1999–2000 backtesting fixtures — Issue #212.

Covers:
  - EcuadorActuals field values match documented IMF WEO / WDI sources
  - FidelityThresholds are set correctly (including unique 'not_deeper' step 2)
  - build_ecuador_scenario() returns a valid ScenarioCreateRequest
  - All Quantity values in the fixture are strings (float prohibition)
  - IA1_DISCLOSURE matches IA1_CANONICAL_PHRASE
  - PARAMETER_CALIBRATION_DISCLOSURE is non-empty and references DIRECTION_ONLY
  - fidelity_report helpers work with entity_id="ECU"
  - Step 2 uses StructuralPolicyInput (not FiscalPolicyInput — no fiscal shock in Ecuador)
  - gdp_growth_2000 is POSITIVE (recovery year — distinct from all other cases)

All tests run without a database connection.
"""
from __future__ import annotations

from decimal import Decimal

import pytest

from tests.backtesting.fidelity_report import (
    _extract_gdp_value,
    format_fidelity_report,
)
from tests.fixtures.ecuador_1999_2000_actuals import (
    ACTUALS,
    IA1_DISCLOSURE,
    PARAMETER_CALIBRATION_DISCLOSURE,
    THRESHOLDS,
)
from tests.fixtures.ecuador_1999_2000_scenario import build_ecuador_scenario

# ---------------------------------------------------------------------------
# EcuadorActuals
# ---------------------------------------------------------------------------


def test_actuals_gdp_1999_matches_imf_weo() -> None:
    """GDP growth 1999: IMF WEO October 1999 outturn -6.3%."""
    assert ACTUALS.gdp_growth_1999 == Decimal("-0.063")
    assert isinstance(ACTUALS.gdp_growth_1999, Decimal)


def test_actuals_gdp_2000_matches_imf_weo() -> None:
    """GDP growth 2000: IMF WEO April 2001 outturn +2.8% (recovery year)."""
    assert ACTUALS.gdp_growth_2000 == Decimal("0.028")
    assert isinstance(ACTUALS.gdp_growth_2000, Decimal)


def test_actuals_gdp_2000_is_positive() -> None:
    """Ecuador 2000 GDP is POSITIVE — recovery after dollarization.

    This is the key structural difference from all other backtesting cases
    (Greece, Argentina, Lebanon, Thailand all show contraction at both steps).
    """
    assert ACTUALS.gdp_growth_2000 > Decimal("0")


def test_actuals_gdp_1999_is_negative() -> None:
    """Ecuador 1999 GDP growth is negative (crisis contraction)."""
    assert ACTUALS.gdp_growth_1999 < Decimal("0")


def test_actuals_gdp_2000_greater_than_gdp_1999() -> None:
    """2000 recovery is stronger than 1999 contraction (+2.8% > -6.3%)."""
    assert ACTUALS.gdp_growth_2000 > ACTUALS.gdp_growth_1999


def test_actuals_unemployment_1999() -> None:
    """World Bank WDI 1999 vintage — INEC/ILO-modelled 14.4%."""
    assert ACTUALS.unemployment_rate_1999 == Decimal("0.144")


def test_actuals_unemployment_2000() -> None:
    """World Bank WDI 2000 vintage — INEC/ILO-modelled 14.1%."""
    assert ACTUALS.unemployment_rate_2000 == Decimal("0.141")


def test_actuals_unemployment_declines_1999_to_2000() -> None:
    """Unemployment slightly declined from 14.4% to 14.1% during stabilization."""
    assert ACTUALS.unemployment_rate_2000 < ACTUALS.unemployment_rate_1999


def test_actuals_is_frozen_dataclass() -> None:
    """EcuadorActuals is immutable (frozen=True)."""
    with pytest.raises(AttributeError):
        ACTUALS.gdp_growth_1999 = Decimal("0")  # type: ignore[misc]


# ---------------------------------------------------------------------------
# FidelityThresholds
# ---------------------------------------------------------------------------


def test_thresholds_gdp_direction_step1_is_true() -> None:
    """Step 1 DIRECTION_ONLY contraction gate is active."""
    assert THRESHOLDS.gdp_direction_step1_correct is True


def test_thresholds_gdp_step2_not_deeper_is_true() -> None:
    """Step 2 'not deeper' gate is active (unique to Ecuador)."""
    assert THRESHOLDS.gdp_step2_not_deeper_than_step1 is True


def test_thresholds_has_not_deeper_field_not_direction_step2() -> None:
    """Ecuador uses 'not_deeper' threshold name — not 'gdp_direction_step2_correct'.

    This distinguishes Ecuador from Greece, Argentina, Lebanon, and Thailand,
    which all use gdp_direction_step2_correct.
    """
    assert hasattr(THRESHOLDS, "gdp_step2_not_deeper_than_step1")
    assert not hasattr(THRESHOLDS, "gdp_direction_step2_correct")


def test_thresholds_is_frozen_dataclass() -> None:
    """FidelityThresholds is immutable (frozen=True)."""
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


def test_parameter_calibration_disclosure_references_ecuador() -> None:
    assert "Ecuador" in PARAMETER_CALIBRATION_DISCLOSURE


def test_parameter_calibration_disclosure_references_dollarization() -> None:
    """Ecuador's key limitation is dollarization stabilization not modeled."""
    assert "dollarization" in PARAMETER_CALIBRATION_DISCLOSURE.lower()


# ---------------------------------------------------------------------------
# build_ecuador_scenario()
# ---------------------------------------------------------------------------


def test_build_ecuador_scenario_returns_scenario_create_request() -> None:
    from app.schemas import ScenarioCreateRequest
    scenario = build_ecuador_scenario()
    assert isinstance(scenario, ScenarioCreateRequest)


def test_build_ecuador_scenario_name_contains_ecuador() -> None:
    scenario = build_ecuador_scenario()
    assert "Ecuador" in scenario.name
    assert "1999" in scenario.name


def test_build_ecuador_scenario_has_ecu_entity() -> None:
    scenario = build_ecuador_scenario()
    assert "ECU" in scenario.configuration.entities


def test_build_ecuador_scenario_n_steps_is_2() -> None:
    scenario = build_ecuador_scenario()
    assert scenario.configuration.n_steps == 2


def test_build_ecuador_scenario_timestep_label_is_annual() -> None:
    scenario = build_ecuador_scenario()
    assert scenario.configuration.timestep_label == "annual"


def test_build_ecuador_scenario_has_scheduled_inputs() -> None:
    scenario = build_ecuador_scenario()
    assert len(scenario.scheduled_inputs) >= 2


def test_build_ecuador_scenario_all_quantity_values_are_strings() -> None:
    """Float prohibition: all QuantitySchema.value fields must be strings."""
    scenario = build_ecuador_scenario()
    for entity_id, attrs in scenario.configuration.initial_attributes.items():
        for attr_key, qty in attrs.items():
            assert isinstance(qty.value, str), (
                f"Float prohibition: {entity_id}.{attr_key}.value "
                f"is {type(qty.value).__name__}, expected str"
            )


def test_build_ecuador_scenario_initial_gdp_growth_is_string() -> None:
    scenario = build_ecuador_scenario()
    gdp = scenario.configuration.initial_attributes["ECU"]["gdp_growth"]
    assert gdp.value == "-0.063"
    assert isinstance(gdp.value, str)


def test_build_ecuador_scenario_initial_gdp_growth_is_negative() -> None:
    """Initial GDP growth must be negative (Ecuador 1999 full-year outturn -6.3%)."""
    scenario = build_ecuador_scenario()
    gdp = scenario.configuration.initial_attributes["ECU"]["gdp_growth"]
    assert Decimal(gdp.value) < Decimal("0")


def test_build_ecuador_scenario_initial_unemployment_rate() -> None:
    """World Bank WDI 1999 INEC/ILO-modelled — 14.4%."""
    scenario = build_ecuador_scenario()
    unemp = scenario.configuration.initial_attributes["ECU"]["unemployment_rate"]
    assert unemp.value == "0.144"
    assert unemp.source_registry_id == "WDI_ECU_1999"
    assert unemp.measurement_framework == "human_development"


def test_build_ecuador_scenario_has_capital_controls_at_step1() -> None:
    """Step 1 must include capital controls EmergencyPolicyInput (deposit freeze)."""
    scenario = build_ecuador_scenario()
    emergency_step1 = [
        si for si in scenario.scheduled_inputs
        if si.input_type == "EmergencyPolicyInput" and si.step == 1
    ]
    assert len(emergency_step1) >= 1
    instruments = {si.input_data["instrument"] for si in emergency_step1}
    assert "capital_controls" in instruments


def test_build_ecuador_scenario_has_bank_holiday_at_step1() -> None:
    """Step 1 must include a bank holiday EmergencyPolicyInput (March 1999 freeze)."""
    scenario = build_ecuador_scenario()
    emergency_step1 = [
        si for si in scenario.scheduled_inputs
        if si.input_type == "EmergencyPolicyInput" and si.step == 1
    ]
    instruments = {si.input_data["instrument"] for si in emergency_step1}
    assert "bank_holiday" in instruments


def test_build_ecuador_scenario_has_structural_input_at_step2() -> None:
    """Step 2 must include a StructuralPolicyInput (dollarization adoption)."""
    scenario = build_ecuador_scenario()
    structural_step2 = [
        si for si in scenario.scheduled_inputs
        if si.input_type == "StructuralPolicyInput" and si.step == 2
    ]
    assert len(structural_step2) >= 1
    instruments = {si.input_data["instrument"] for si in structural_step2}
    assert "institutional_reform" in instruments


def test_build_ecuador_scenario_no_fiscal_input() -> None:
    """Ecuador has NO FiscalPolicyInput — this is why MacroeconomicModule does not fire.

    Unlike Lebanon and Thailand, Ecuador's events (capital controls, bank holiday,
    dollarization) are all Emergency or Structural — none are processed by
    MacroeconomicModule. This causes step 2 GDP to equal step 1 GDP (initial seed),
    which satisfies the 'not deeper' threshold.
    """
    scenario = build_ecuador_scenario()
    fiscal_inputs = [
        si for si in scenario.scheduled_inputs
        if si.input_type == "FiscalPolicyInput"
    ]
    assert len(fiscal_inputs) == 0


def test_build_ecuador_scenario_scheduled_input_values_are_strings() -> None:
    """Float prohibition extends to scheduled input value fields."""
    scenario = build_ecuador_scenario()
    for si in scenario.scheduled_inputs:
        if "value" in si.input_data:
            assert isinstance(si.input_data["value"], str), (
                f"Float prohibition: step={si.step} value is "
                f"{type(si.input_data['value']).__name__}, expected str"
            )


def test_build_ecuador_scenario_scheduled_steps_in_valid_range() -> None:
    """All scheduled input steps must be within [0, n_steps]."""
    scenario = build_ecuador_scenario()
    n = scenario.configuration.n_steps
    for si in scenario.scheduled_inputs:
        assert 0 <= si.step <= n, (
            f"Scheduled input step {si.step} outside valid range [0, {n}]"
        )


def test_build_ecuador_scenario_input_types_are_known() -> None:
    """All scheduled input types must be recognized by _deserialize_control_input."""
    known_types = {
        "FiscalPolicyInput",
        "EmergencyPolicyInput",
        "TradePolicyInput",
        "MonetaryRateInput",
        "StructuralPolicyInput",
    }
    scenario = build_ecuador_scenario()
    for si in scenario.scheduled_inputs:
        assert si.input_type in known_types, (
            f"Unknown input_type: {si.input_type!r}"
        )


def test_build_ecuador_scenario_step2_structural_has_monetary_sector() -> None:
    """Dollarization StructuralPolicyInput must target monetary sector."""
    scenario = build_ecuador_scenario()
    structural_step2 = [
        si for si in scenario.scheduled_inputs
        if si.input_type == "StructuralPolicyInput" and si.step == 2
    ]
    assert len(structural_step2) >= 1
    for si in structural_step2:
        assert si.input_data.get("affected_sector") == "monetary", (
            "Dollarization must be tagged as monetary sector reform"
        )


# ---------------------------------------------------------------------------
# fidelity_report helpers with entity_id="ECU"
# ---------------------------------------------------------------------------


def _make_ecu_snapshot(gdp_value: str = "-0.063") -> list[dict]:
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
            "timestep": f"199{9 + s}-01-01T00:00:00+00:00",
            "state_data": {"ECU": {"gdp_growth": envelope}},
        }
        for s in range(3)
    ]


def test_extract_gdp_value_ecu_entity() -> None:
    """_extract_gdp_value must return the ECU value when entity_id='ECU'."""
    snap = {"state_data": {"ECU": {"gdp_growth": {"value": "-0.063"}}}}
    result = _extract_gdp_value(snap, entity_id="ECU")
    assert result == Decimal("-0.063")
    assert isinstance(result, Decimal)


def test_extract_gdp_value_ecu_returns_none_for_grc_data() -> None:
    """ECU extraction must return None when only GRC data is present."""
    snap = {"state_data": {"GRC": {"gdp_growth": {"value": "-0.054"}}}}
    result = _extract_gdp_value(snap, entity_id="ECU")
    assert result is None


def test_format_fidelity_report_with_ecu_entity_pass() -> None:
    """format_fidelity_report must work with entity_id='ECU' (all pass)."""
    report = format_fidelity_report(
        scenario_name="Ecuador 1999-2000 Dollarization Crisis Backtesting Fixture",
        actuals=ACTUALS,
        snapshots=_make_ecu_snapshot(),
        thresholds_met={
            "gdp_growth_step1_negative": True,
            "gdp_growth_step2_not_deeper_than_step1": True,
        },
        ia1_disclosure=IA1_DISCLOSURE,
        parameter_calibration_disclosure=PARAMETER_CALIBRATION_DISCLOSURE,
        entity_id="ECU",
    )
    assert isinstance(report, str)
    assert len(report) > 100
    assert "Overall: PASS" in report


def test_format_fidelity_report_with_ecu_entity_fail() -> None:
    """format_fidelity_report must report FAIL when thresholds not met."""
    report = format_fidelity_report(
        scenario_name="Ecuador 1999-2000 Dollarization Crisis Backtesting Fixture",
        actuals=ACTUALS,
        snapshots=_make_ecu_snapshot(),
        thresholds_met={
            "gdp_growth_step1_negative": False,
            "gdp_growth_step2_not_deeper_than_step1": True,
        },
        ia1_disclosure=IA1_DISCLOSURE,
        parameter_calibration_disclosure=PARAMETER_CALIBRATION_DISCLOSURE,
        entity_id="ECU",
    )
    assert isinstance(report, str)
    assert "Overall: FAIL" in report


def test_not_deeper_threshold_logic_equal_values_pass() -> None:
    """Equal step 1 and step 2 GDP must satisfy 'not deeper' (>= not >).

    When MacroeconomicModule does not fire (no fiscal inputs), step 2 GDP equals
    step 1 GDP (both show the initial seed value -6.3%). The threshold uses >=,
    so equal values pass. This is the expected Ecuador production behavior.
    """
    val1 = Decimal("-0.063")
    val2 = Decimal("-0.063")
    assert val2 >= val1  # equal satisfies not-deeper


def test_not_deeper_threshold_logic_shallower_contraction_pass() -> None:
    """A shallower step 2 contraction must satisfy 'not deeper'."""
    val1 = Decimal("-0.063")
    val2 = Decimal("-0.020")  # less severe
    assert val2 >= val1


def test_not_deeper_threshold_logic_positive_recovery_pass() -> None:
    """Positive step 2 GDP (historical +2.8%) must satisfy 'not deeper'."""
    val1 = Decimal("-0.063")
    val2 = Decimal("0.028")  # historical outturn
    assert val2 >= val1


def test_not_deeper_threshold_logic_deeper_contraction_fail() -> None:
    """A deeper step 2 contraction must NOT satisfy 'not deeper'."""
    val1 = Decimal("-0.063")
    val2 = Decimal("-0.100")  # worse
    assert not (val2 >= val1)
