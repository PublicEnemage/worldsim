"""Unit tests for Greece 2010–2012 backtesting fixtures.

Tests run without a database connection. Covers:
  - GreeceActuals field values match documented historical data
  - FidelityThresholds are set correctly
  - build_greece_scenario() returns a valid ScenarioCreateRequest
  - All Quantity values in the fixture are strings (float prohibition)
  - IA1_DISCLOSURE is non-empty and matches canonical phrase
  - PARAMETER_CALIBRATION_DISCLOSURE is non-empty
  - fidelity_report.format_fidelity_report() returns a non-empty string
    containing the required disclosure sections
"""
from __future__ import annotations

from decimal import Decimal

import pytest

from tests.backtesting.fidelity_report import (
    _extract_gdp_value,
    _extract_unemployment_value,
    format_fidelity_report,
)
from tests.fixtures.greece_2010_2012_actuals import (
    ACTUALS,
    IA1_DISCLOSURE,
    PARAMETER_CALIBRATION_DISCLOSURE,
    THRESHOLDS,
)
from tests.fixtures.greece_2010_scenario import build_greece_scenario

# ---------------------------------------------------------------------------
# GreeceActuals
# ---------------------------------------------------------------------------


def test_actuals_gdp_2010_matches_imf_weo() -> None:
    """GDP growth 2010: IMF WEO Apr 2013 outturn -5.4%."""
    assert ACTUALS.gdp_growth_2010 == Decimal("-0.054")
    assert isinstance(ACTUALS.gdp_growth_2010, Decimal)


def test_actuals_gdp_2011_matches_imf_weo() -> None:
    """GDP growth 2011: IMF WEO Apr 2013 outturn -8.9%."""
    assert ACTUALS.gdp_growth_2011 == Decimal("-0.089")
    assert isinstance(ACTUALS.gdp_growth_2011, Decimal)


def test_actuals_gdp_2012_matches_imf_weo() -> None:
    """GDP growth 2012: IMF WEO Apr 2013 outturn -6.6%."""
    assert ACTUALS.gdp_growth_2012 == Decimal("-0.066")
    assert isinstance(ACTUALS.gdp_growth_2012, Decimal)


def test_actuals_unemployment_2010() -> None:
    """Eurostat LFS Q1 2010 — 12.7% (updated from IMF WEO in Issue #149)."""
    assert ACTUALS.unemployment_rate_2010 == Decimal("0.127")


def test_actuals_unemployment_2011() -> None:
    """Eurostat LFS Q1 2011 — 14.9%."""
    assert ACTUALS.unemployment_rate_2011 == Decimal("0.149")


def test_actuals_unemployment_2012() -> None:
    """Eurostat LFS Q1 2012 — 24.5%."""
    assert ACTUALS.unemployment_rate_2012 == Decimal("0.245")


def test_actuals_unemployment_2013() -> None:
    """Eurostat LFS Q1 2013 — 27.5% (step 3 extrapolation within fixture window)."""
    assert ACTUALS.unemployment_rate_2013 == Decimal("0.275")


def test_actuals_all_gdp_values_are_negative() -> None:
    """All historical GDP growth rates for 2010–2012 are negative (contraction)."""
    assert ACTUALS.gdp_growth_2010 < Decimal("0")
    assert ACTUALS.gdp_growth_2011 < Decimal("0")
    assert ACTUALS.gdp_growth_2012 < Decimal("0")


def test_actuals_unemployment_rises_2010_to_2013() -> None:
    """Historical unemployment rose monotonically 2010→2011→2012→2013 (Eurostat LFS Q1)."""
    assert ACTUALS.unemployment_rate_2010 < ACTUALS.unemployment_rate_2011
    assert ACTUALS.unemployment_rate_2011 < ACTUALS.unemployment_rate_2012
    assert ACTUALS.unemployment_rate_2012 < ACTUALS.unemployment_rate_2013


def test_actuals_is_frozen_dataclass() -> None:
    """GreeceActuals is immutable (frozen=True)."""
    with pytest.raises(AttributeError):
        ACTUALS.gdp_growth_2010 = Decimal("0")  # type: ignore[misc]


# ---------------------------------------------------------------------------
# FidelityThresholds
# ---------------------------------------------------------------------------


def test_thresholds_gdp_direction_correct_is_true() -> None:
    assert THRESHOLDS.gdp_direction_correct is True


def test_thresholds_unemployment_direction_step0_to_step3_is_true() -> None:
    """Threshold renamed from unemployment_direction_correct — Issue #149."""
    assert THRESHOLDS.unemployment_direction_step0_to_step3 is True


def test_thresholds_is_frozen_dataclass() -> None:
    with pytest.raises(AttributeError):
        THRESHOLDS.gdp_direction_correct = False  # type: ignore[misc]


# ---------------------------------------------------------------------------
# IA1_DISCLOSURE
# ---------------------------------------------------------------------------


def test_ia1_disclosure_is_non_empty() -> None:
    assert IA1_DISCLOSURE
    assert len(IA1_DISCLOSURE) > 30


def test_ia1_disclosure_matches_canonical_phrase() -> None:
    """Must match IA1_CANONICAL_PHRASE from quantity_serde exactly."""
    from app.simulation.repositories.quantity_serde import IA1_CANONICAL_PHRASE

    assert IA1_DISCLOSURE == IA1_CANONICAL_PHRASE


def test_ia1_disclosure_contains_required_terms() -> None:
    assert "confidence tier" in IA1_DISCLOSURE.lower()
    assert "DATA_STANDARDS.md" in IA1_DISCLOSURE
    assert "IA-1" in IA1_DISCLOSURE


# ---------------------------------------------------------------------------
# PARAMETER_CALIBRATION_DISCLOSURE
# ---------------------------------------------------------------------------


def test_parameter_calibration_disclosure_is_non_empty() -> None:
    assert PARAMETER_CALIBRATION_DISCLOSURE
    assert len(PARAMETER_CALIBRATION_DISCLOSURE) > 30


def test_parameter_calibration_disclosure_references_issue_44() -> None:
    assert "Issue #44" in PARAMETER_CALIBRATION_DISCLOSURE


def test_parameter_calibration_disclosure_references_direction_only() -> None:
    assert "DIRECTION_ONLY" in PARAMETER_CALIBRATION_DISCLOSURE


# ---------------------------------------------------------------------------
# build_greece_scenario()
# ---------------------------------------------------------------------------


def test_build_greece_scenario_returns_scenario_create_request() -> None:
    from app.schemas import ScenarioCreateRequest

    scenario = build_greece_scenario()
    assert isinstance(scenario, ScenarioCreateRequest)


def test_build_greece_scenario_name_is_correct() -> None:
    scenario = build_greece_scenario()
    assert "Greece" in scenario.name
    assert "2010" in scenario.name


def test_build_greece_scenario_has_grc_entity() -> None:
    scenario = build_greece_scenario()
    assert "GRC" in scenario.configuration.entities


def test_build_greece_scenario_n_steps_is_3() -> None:
    scenario = build_greece_scenario()
    assert scenario.configuration.n_steps == 3


def test_build_greece_scenario_timestep_label_is_annual() -> None:
    scenario = build_greece_scenario()
    assert scenario.configuration.timestep_label == "annual"


def test_build_greece_scenario_has_scheduled_inputs() -> None:
    scenario = build_greece_scenario()
    assert len(scenario.scheduled_inputs) >= 1


def test_build_greece_scenario_all_quantity_values_are_strings() -> None:
    """Float prohibition: all QuantitySchema.value fields must be strings."""
    scenario = build_greece_scenario()
    for entity_id, attrs in scenario.configuration.initial_attributes.items():
        for attr_key, qty in attrs.items():
            assert isinstance(qty.value, str), (
                f"Float prohibition violated: {entity_id}.{attr_key}.value "
                f"is {type(qty.value).__name__}, expected str"
            )


def test_build_greece_scenario_initial_gdp_growth_is_string() -> None:
    scenario = build_greece_scenario()
    gdp = scenario.configuration.initial_attributes["GRC"]["gdp_growth"]
    assert gdp.value == "-0.054"
    assert isinstance(gdp.value, str)


def test_build_greece_scenario_has_four_initial_attributes() -> None:
    """Initial state must have 4 attributes after Issue #149 WDI seed."""
    scenario = build_greece_scenario()
    grc_attrs = scenario.configuration.initial_attributes["GRC"]
    assert len(grc_attrs) == 4
    expected_keys = {
        "gdp_growth",
        "unemployment_rate",
        "health_expenditure_pct_gdp",
        "net_enrollment_secondary",
    }
    assert set(grc_attrs.keys()) == expected_keys


def test_build_greece_scenario_initial_unemployment_rate() -> None:
    """Eurostat LFS Q1 2010 — 12.7% (Issue #149)."""
    scenario = build_greece_scenario()
    unemp = scenario.configuration.initial_attributes["GRC"]["unemployment_rate"]
    assert unemp.value == "0.127"
    assert unemp.source_registry_id == "EUROSTAT_LFS_2010"
    assert unemp.measurement_framework == "human_development"
    assert unemp.confidence_tier == 2


def test_build_greece_scenario_initial_health_expenditure() -> None:
    """World Bank WDI 2010 — 9.5% of GDP (Issue #149)."""
    scenario = build_greece_scenario()
    health = scenario.configuration.initial_attributes["GRC"]["health_expenditure_pct_gdp"]
    assert health.value == "0.095"
    assert health.source_registry_id == "WDI_2010"
    assert health.measurement_framework == "human_development"
    assert health.confidence_tier == 2


def test_build_greece_scenario_initial_net_enrollment_secondary() -> None:
    """World Bank WDI 2010 — 99.1% net enrollment (Issue #149)."""
    scenario = build_greece_scenario()
    enroll = scenario.configuration.initial_attributes["GRC"]["net_enrollment_secondary"]
    assert enroll.value == "0.991"
    assert enroll.source_registry_id == "WDI_2010"
    assert enroll.measurement_framework == "human_development"
    assert enroll.confidence_tier == 2


def test_build_greece_scenario_human_dev_attributes_use_human_development_framework() -> None:
    """All three WDI-seeded attributes must use measurement_framework=human_development."""
    scenario = build_greece_scenario()
    grc = scenario.configuration.initial_attributes["GRC"]
    for key in ("unemployment_rate", "health_expenditure_pct_gdp", "net_enrollment_secondary"):
        assert grc[key].measurement_framework == "human_development", (
            f"{key}.measurement_framework must be 'human_development'"
        )


def test_build_greece_scenario_scheduled_inputs_have_valid_steps() -> None:
    """All scheduled input steps must be within [0, n_steps - 1]."""
    scenario = build_greece_scenario()
    n = scenario.configuration.n_steps
    for si in scenario.scheduled_inputs:
        assert 0 <= si.step <= n, (
            f"Scheduled input step {si.step} outside valid range [0, {n}]"
        )


def test_build_greece_scenario_input_types_are_known() -> None:
    """All scheduled input types must be recognized by _deserialize_control_input."""
    known_types = {
        "FiscalPolicyInput",
        "EmergencyPolicyInput",
        "TradePolicyInput",
        "MonetaryRateInput",
        "StructuralPolicyInput",
    }
    scenario = build_greece_scenario()
    for si in scenario.scheduled_inputs:
        assert si.input_type in known_types, (
            f"Unknown input_type: {si.input_type!r}. "
            f"WebScenarioRunner cannot deserialize this type."
        )


def test_build_greece_scenario_scheduled_input_values_are_strings() -> None:
    """Float prohibition extends to scheduled input value fields."""
    scenario = build_greece_scenario()
    for si in scenario.scheduled_inputs:
        if "value" in si.input_data:
            assert isinstance(si.input_data["value"], str), (
                f"Float prohibition: scheduled_input step={si.step} "
                f"value is {type(si.input_data['value']).__name__}, expected str"
            )


def test_build_greece_scenario_fiscal_inputs_use_spending_change() -> None:
    scenario = build_greece_scenario()
    fiscal_inputs = [
        si for si in scenario.scheduled_inputs if si.input_type == "FiscalPolicyInput"
    ]
    assert len(fiscal_inputs) >= 1
    instruments = {si.input_data.get("instrument") for si in fiscal_inputs}
    known_fiscal = {"spending_change", "tax_rate_change", "deficit_target"}
    unknown = instruments - known_fiscal
    assert not unknown, f"Unknown FiscalInstrument values: {unknown}"


# ---------------------------------------------------------------------------
# fidelity_report.format_fidelity_report()
# ---------------------------------------------------------------------------


def _make_mock_snapshots(gdp_value: str = "-0.054") -> list[dict]:
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
        {"step": s, "timestep": f"200{s}-01-01T00:00:00+00:00",
         "state_data": {"GRC": {"gdp_growth": envelope}}}
        for s in range(4)
    ]


def test_format_fidelity_report_returns_non_empty_string() -> None:
    report = format_fidelity_report(
        scenario_name="Test Scenario",
        actuals=ACTUALS,
        snapshots=_make_mock_snapshots(),
        thresholds_met={"gdp_step1_negative": True},
        ia1_disclosure=IA1_DISCLOSURE,
        parameter_calibration_disclosure=PARAMETER_CALIBRATION_DISCLOSURE,
    )
    assert isinstance(report, str)
    assert len(report) > 100


def test_format_fidelity_report_contains_ia1_disclosure() -> None:
    report = format_fidelity_report(
        scenario_name="Test",
        actuals=ACTUALS,
        snapshots=_make_mock_snapshots(),
        thresholds_met={},
        ia1_disclosure=IA1_DISCLOSURE,
        parameter_calibration_disclosure=PARAMETER_CALIBRATION_DISCLOSURE,
    )
    assert "DATA_STANDARDS.md" in report
    assert "IA-1" in report


def test_format_fidelity_report_contains_parameter_calibration_disclosure() -> None:
    report = format_fidelity_report(
        scenario_name="Test",
        actuals=ACTUALS,
        snapshots=_make_mock_snapshots(),
        thresholds_met={},
        ia1_disclosure=IA1_DISCLOSURE,
        parameter_calibration_disclosure=PARAMETER_CALIBRATION_DISCLOSURE,
    )
    assert "Issue #44" in report
    assert "DIRECTION_ONLY" in report


def test_format_fidelity_report_shows_overall_pass() -> None:
    report = format_fidelity_report(
        scenario_name="Test",
        actuals=ACTUALS,
        snapshots=_make_mock_snapshots(),
        thresholds_met={"t1": True, "t2": True},
        ia1_disclosure=IA1_DISCLOSURE,
        parameter_calibration_disclosure=PARAMETER_CALIBRATION_DISCLOSURE,
    )
    assert "Overall: PASS" in report


def test_format_fidelity_report_shows_overall_fail() -> None:
    report = format_fidelity_report(
        scenario_name="Test",
        actuals=ACTUALS,
        snapshots=_make_mock_snapshots(),
        thresholds_met={"t1": True, "t2": False},
        ia1_disclosure=IA1_DISCLOSURE,
        parameter_calibration_disclosure=PARAMETER_CALIBRATION_DISCLOSURE,
    )
    assert "Overall: FAIL" in report


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def test_extract_gdp_value_returns_decimal() -> None:
    snap = {"state_data": {"GRC": {"gdp_growth": {"value": "-0.054"}}}}
    result = _extract_gdp_value(snap)
    assert result == Decimal("-0.054")
    assert isinstance(result, Decimal)


def test_extract_gdp_value_returns_none_when_missing() -> None:
    assert _extract_gdp_value({}) is None
    assert _extract_gdp_value({"state_data": {}}) is None


def test_extract_unemployment_value_returns_none_when_missing() -> None:
    snap = {"state_data": {"GRC": {"gdp_growth": {"value": "-0.054"}}}}
    assert _extract_unemployment_value(snap) is None
