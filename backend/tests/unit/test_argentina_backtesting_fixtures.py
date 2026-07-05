"""Unit tests for Argentina 2001–2002 backtesting fixtures — Issues #192, #553.

Covers:
  - ArgentinaActuals field values match documented IMF WEO / INDEC EPH data
  - FidelityThresholds are set correctly
  - build_argentina_scenario() returns a valid ScenarioCreateRequest
  - All Quantity values in the fixture are strings (float prohibition)
  - IA1_DISCLOSURE matches IA1_CANONICAL_PHRASE
  - PARAMETER_CALIBRATION_DISCLOSURE is non-empty
  - fidelity_report helpers work with entity_id="ARG"
  - build_argentina_demo_scenario() — Demo 3 (Issue #553):
      n_steps=4, ecological/governance seeds, step_metadata event labels

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
from tests.fixtures.argentina_2001_2002_scenario import (
    build_argentina_demo_scenario,
    build_argentina_scenario,
)

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


def test_build_argentina_scenario_n_steps_is_3() -> None:
    scenario = build_argentina_scenario()
    assert scenario.configuration.n_steps == 3


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


# ---------------------------------------------------------------------------
# build_argentina_demo_scenario() — Issue #553 Demo 3
# ---------------------------------------------------------------------------


def test_build_argentina_demo_scenario_returns_scenario_create_request() -> None:
    from app.schemas import ScenarioCreateRequest
    demo = build_argentina_demo_scenario()
    assert isinstance(demo, ScenarioCreateRequest)


def test_build_argentina_demo_scenario_name_references_demo() -> None:
    demo = build_argentina_demo_scenario()
    assert "Demo" in demo.name or "demo" in demo.name.lower() or "Argentina" in demo.name


def test_build_argentina_demo_scenario_n_steps_is_4() -> None:
    """Demo arc covers 4 annual steps (2001–2004)."""
    demo = build_argentina_demo_scenario()
    assert demo.configuration.n_steps == 4


def test_build_argentina_demo_scenario_has_arg_entity() -> None:
    demo = build_argentina_demo_scenario()
    assert "ARG" in demo.configuration.entities


def test_build_argentina_demo_scenario_start_date_is_2000() -> None:
    from datetime import date
    demo = build_argentina_demo_scenario()
    assert demo.configuration.start_date == date(2000, 1, 1)


def test_build_argentina_demo_scenario_ecological_module_enabled() -> None:
    demo = build_argentina_demo_scenario()
    assert demo.configuration.modules_config.get("ecological", {}).get("enabled") is True


def test_build_argentina_demo_scenario_governance_module_enabled() -> None:
    demo = build_argentina_demo_scenario()
    assert demo.configuration.modules_config.get("governance", {}).get("enabled") is True


def test_build_argentina_demo_scenario_has_co2_seed() -> None:
    """Ecological seed: co2_concentration_ppm = 369.5 (NOAA MLO 2000)."""
    demo = build_argentina_demo_scenario()
    attrs = demo.configuration.initial_attributes["ARG"]
    assert "co2_concentration_ppm" in attrs
    co2 = attrs["co2_concentration_ppm"]
    assert co2.value == "369.5"
    assert co2.measurement_framework == "ecological"
    assert co2.source_registry_id == "NOAA_MLO_2000"


def test_build_argentina_demo_scenario_has_rule_of_law_seed() -> None:
    """Governance seed: rule_of_law_percentile = 33.2 (WGI ARG 2000)."""
    demo = build_argentina_demo_scenario()
    attrs = demo.configuration.initial_attributes["ARG"]
    assert "rule_of_law_percentile" in attrs
    rol = attrs["rule_of_law_percentile"]
    assert rol.value == "33.2"
    assert rol.measurement_framework == "governance"
    assert rol.source_registry_id == "WB_WGI_ARG_2000_RULE_OF_LAW"


def test_build_argentina_demo_scenario_has_democratic_quality_seed() -> None:
    """Governance seed: democratic_quality_score = 0.71 (V-Dem LDI ARG 2000)."""
    demo = build_argentina_demo_scenario()
    attrs = demo.configuration.initial_attributes["ARG"]
    assert "democratic_quality_score" in attrs
    dqs = attrs["democratic_quality_score"]
    assert dqs.value == "0.71"
    assert dqs.measurement_framework == "governance"
    assert dqs.source_registry_id == "VDEM_V13_ARG_2000_LDI"


def test_build_argentina_demo_scenario_has_step_metadata() -> None:
    """step_metadata must contain entries for steps 1, 2, and 3."""
    demo = build_argentina_demo_scenario()
    sm = demo.configuration.step_metadata
    assert "1" in sm
    assert "2" in sm
    assert "3" in sm


def test_build_argentina_demo_scenario_step1_is_significant() -> None:
    demo = build_argentina_demo_scenario()
    sm = demo.configuration.step_metadata
    assert sm["1"]["significance"] == "SIGNIFICANT"
    assert len(sm["1"]["label"]) <= 32


def test_build_argentina_demo_scenario_step2_is_significant() -> None:
    demo = build_argentina_demo_scenario()
    sm = demo.configuration.step_metadata
    assert sm["2"]["significance"] == "SIGNIFICANT"
    assert len(sm["2"]["label"]) <= 32


def test_build_argentina_demo_scenario_step3_is_significant() -> None:
    demo = build_argentina_demo_scenario()
    sm = demo.configuration.step_metadata
    assert sm["3"]["significance"] == "SIGNIFICANT"
    assert "Kirchner" in sm["3"]["label"]


def test_build_argentina_demo_scenario_all_labels_under_32_chars() -> None:
    """All step_metadata labels must be ≤32 chars (trajectory endpoint contract)."""
    demo = build_argentina_demo_scenario()
    for key, meta in demo.configuration.step_metadata.items():
        label = meta.get("label", "")
        assert len(label) <= 32, (
            f"step_metadata[{key!r}] label exceeds 32 chars: {label!r} ({len(label)} chars)"
        )


def test_build_argentina_demo_scenario_inherits_base_scheduled_inputs() -> None:
    """Demo scenario must retain the base backtesting scheduled inputs."""
    base = build_argentina_scenario()
    demo = build_argentina_demo_scenario()
    base_steps = {(si.step, si.input_type) for si in base.scheduled_inputs}
    demo_steps = {(si.step, si.input_type) for si in demo.scheduled_inputs}
    assert base_steps.issubset(demo_steps), (
        f"Demo scenario is missing base inputs: {base_steps - demo_steps}"
    )


def test_build_argentina_demo_scenario_all_quantity_values_are_strings() -> None:
    """Float prohibition applies to all initial attributes including demo seeds."""
    demo = build_argentina_demo_scenario()
    for entity_id, attrs in demo.configuration.initial_attributes.items():
        for attr_key, qty in attrs.items():
            assert isinstance(qty.value, str), (
                f"Float prohibition: {entity_id}.{attr_key}.value "
                f"is {type(qty.value).__name__}, expected str"
            )


def test_build_argentina_demo_scenario_serializes_to_json() -> None:
    """model_dump(mode='json') must succeed — step_metadata must round-trip."""
    demo = build_argentina_demo_scenario()
    dumped = demo.model_dump(mode="json")
    cfg = dumped["configuration"]
    assert "step_metadata" in cfg
    assert cfg["step_metadata"]["1"]["significance"] == "SIGNIFICANT"


def test_build_argentina_demo_scenario_has_emergency_declaration_at_step2() -> None:
    """Demo scenario must include emergency_declaration at step 2 (state of siege,
    December 19 2001 — concurrent with sovereign default).

    This is the instrument that drives democratic_quality_score below the 0.70
    MDA-GOV-DEMOCRACY-FLOOR at step 3 via GovernanceModule one-step lag (#615).
    """
    demo = build_argentina_demo_scenario()
    emergency_at_step2 = [
        si for si in demo.scheduled_inputs
        if si.step == 2
        and si.input_type == "EmergencyPolicyInput"
        and si.input_data.get("instrument") == "emergency_declaration"
    ]
    assert len(emergency_at_step2) == 1, (
        "Demo scenario must have exactly one emergency_declaration at step 2 "
        f"(found {len(emergency_at_step2)})"
    )


def test_build_argentina_demo_scenario_emergency_declaration_step_in_range() -> None:
    """emergency_declaration step must be within [0, n_steps]."""
    demo = build_argentina_demo_scenario()
    n = demo.configuration.n_steps
    for si in demo.scheduled_inputs:
        assert 0 <= si.step <= n, (
            f"Scheduled input step {si.step} outside valid range [0, {n}]"
        )


def test_build_argentina_demo_scenario_governance_mda_breach_math() -> None:
    """Verify democratic_quality_score drops below 0.70 at step 3.

    GovernanceModule one-step lag applies elasticities from the prior step:
      Step 2 reads step 1: imf_program_acceptance × +0.005 = +0.005
        → score: 0.71 + 0.005 = 0.715 (above 0.70 — no breach)
      Step 3 reads step 2: emergency_declaration × -0.05 = -0.05
        → score: 0.715 - 0.05 = 0.665 ≤ 0.70 — MDA WARNING fires

    This test encodes the expected score trajectory as a regression gate.
    If the elasticity values or initial seed change, this test will catch it.
    """
    from decimal import Decimal

    from app.simulation.modules.governance.elasticities import GOVERNANCE_ELASTICITY_REGISTRY

    initial_dqs = Decimal("0.71")
    mda_floor = Decimal("0.70")

    imf_elasticity = next(
        r.elasticity for r in GOVERNANCE_ELASTICITY_REGISTRY
        if r.event_type == "emergency_policy_imf_program_acceptance"
        and r.indicator_key == "democratic_quality_score"
    )
    emergency_elasticity = next(
        r.elasticity for r in GOVERNANCE_ELASTICITY_REGISTRY
        if r.event_type == "emergency_policy_emergency_declaration"
        and r.indicator_key == "democratic_quality_score"
    )

    # Step 2 effect: imf_program_acceptance fires at step 1 → processed at step 2
    score_after_step2 = initial_dqs + (Decimal("1") * imf_elasticity)
    assert score_after_step2 > mda_floor, (
        f"Score after step 2 ({score_after_step2}) must be above MDA floor — "
        "breach should not fire until step 3"
    )

    # Step 3 effect: emergency_declaration fires at step 2 → processed at step 3
    score_after_step3 = score_after_step2 + (Decimal("1") * emergency_elasticity)
    assert score_after_step3 <= mda_floor, (
        f"Score after step 3 ({score_after_step3}) must be ≤ MDA floor {mda_floor} — "
        "MDA-GOV-DEMOCRACY-FLOOR WARNING must fire at step 3"
    )
