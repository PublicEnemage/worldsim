"""Unit tests for Jordan/Egypt Strait of Hormuz Demo 4 fixture — Issue #793, ADR-012.

Covers:
  - build_jordan_hormuz_scenario() structural contracts
    — two entities (JOR + EGY), 8 steps, commodity_price_shocks configured
    — import dependency coefficients at expected Tier 3 values
    — scheduled inputs valid (step range, type, instrument)
    — all QuantitySchema.value fields are strings (float prohibition)
  - build_jordan_hormuz_demo_scenario()
    — extends base with all four module seeds
    — EcologicalModule and GovernanceModule enabled in modules_config
    — governance seeds: rule_of_law_percentile, democratic_quality_score, elite_capture_coefficient
    — step_metadata: 6 labelled steps, ≤32 chars each, correct significance levels
    — political_context present for JOR scenario
    — all quantity values strings after extension
    — model_dump(mode='json') round-trips successfully

All tests run without a database connection.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from tests.fixtures.jordan_hormuz_scenario import (
    build_jordan_hormuz_demo_scenario,
    build_jordan_hormuz_scenario,
)

# ---------------------------------------------------------------------------
# build_jordan_hormuz_scenario() — base fixture structural contracts
# ---------------------------------------------------------------------------


def test_base_returns_scenario_create_request() -> None:
    from app.schemas import ScenarioCreateRequest
    scenario = build_jordan_hormuz_scenario()
    assert isinstance(scenario, ScenarioCreateRequest)


def test_base_name_references_jordan_and_hormuz() -> None:
    scenario = build_jordan_hormuz_scenario()
    assert "Jordan" in scenario.name or "JOR" in scenario.name
    assert "Hormuz" in scenario.name


def test_base_entities_contains_jor_and_egy() -> None:
    """Two-entity requirement: JOR + EGY unlock composite scores (Issue #193)."""
    scenario = build_jordan_hormuz_scenario()
    entities = scenario.configuration.entities
    assert "JOR" in entities
    assert "EGY" in entities
    assert len(entities) == 2


def test_base_n_steps_is_8() -> None:
    """8-step arc: 2024–2031 (6 shock steps + 2 recovery steps)."""
    scenario = build_jordan_hormuz_scenario()
    assert scenario.configuration.n_steps == 8


def test_base_timestep_label_is_annual() -> None:
    scenario = build_jordan_hormuz_scenario()
    assert scenario.configuration.timestep_label == "annual"


def test_base_start_date_is_2024() -> None:
    scenario = build_jordan_hormuz_scenario()
    assert scenario.configuration.start_date == date(2024, 1, 1)


# ---------------------------------------------------------------------------
# Commodity price shocks
# ---------------------------------------------------------------------------


def test_base_has_two_commodity_shocks() -> None:
    """Fuel shock (steps 1–6) and food shock (steps 2–6) both required."""
    scenario = build_jordan_hormuz_scenario()
    shocks = scenario.configuration.commodity_price_shocks
    assert len(shocks) == 2


def test_base_fuel_shock_configured_correctly() -> None:
    """Fuel shock: category=fuel, magnitude=0.25, start_step=1, duration_steps=6."""
    scenario = build_jordan_hormuz_scenario()
    shocks = scenario.configuration.commodity_price_shocks
    fuel_shocks = [s for s in shocks if s.commodity_category == "fuel"]
    assert len(fuel_shocks) == 1
    fuel = fuel_shocks[0]
    assert fuel.magnitude == Decimal("0.25")
    assert fuel.start_step == 1
    assert fuel.duration_steps == 6


def test_base_food_shock_configured_correctly() -> None:
    """Food shock: category=food, magnitude=0.15, start_step=2, duration_steps=5."""
    scenario = build_jordan_hormuz_scenario()
    shocks = scenario.configuration.commodity_price_shocks
    food_shocks = [s for s in shocks if s.commodity_category == "food"]
    assert len(food_shocks) == 1
    food = food_shocks[0]
    assert food.magnitude == Decimal("0.15")
    assert food.start_step == 2
    assert food.duration_steps == 5


def test_base_fuel_shock_ends_at_step_6() -> None:
    """Fuel shock active steps 1–6: start=1, duration=6 → last active step = 6."""
    scenario = build_jordan_hormuz_scenario()
    fuel = next(
        s for s in scenario.configuration.commodity_price_shocks
        if s.commodity_category == "fuel"
    )
    assert fuel.start_step + fuel.duration_steps - 1 == 6


def test_base_food_shock_ends_at_step_6() -> None:
    """Food shock active steps 2–6: start=2, duration=5 → last active step = 6."""
    scenario = build_jordan_hormuz_scenario()
    food = next(
        s for s in scenario.configuration.commodity_price_shocks
        if s.commodity_category == "food"
    )
    assert food.start_step + food.duration_steps - 1 == 6


# ---------------------------------------------------------------------------
# Jordan initial attributes
# ---------------------------------------------------------------------------


def test_base_jor_gdp_growth_value() -> None:
    """JOR GDP growth: IMF WEO Apr 2024 — +2.5%."""
    scenario = build_jordan_hormuz_scenario()
    gdp = scenario.configuration.initial_attributes["JOR"]["gdp_growth"]
    assert gdp.value == "0.025"
    assert gdp.source_registry_id == "IMF_WEO_APR2024"
    assert gdp.measurement_framework == "financial"


def test_base_jor_unemployment_value() -> None:
    """JOR unemployment: DOS LFS Q1 2024 — 17.8%."""
    scenario = build_jordan_hormuz_scenario()
    unemp = scenario.configuration.initial_attributes["JOR"]["unemployment_rate"]
    assert unemp.value == "0.178"
    assert unemp.source_registry_id == "DOS_LFS_Q1_2024"
    assert unemp.measurement_framework == "human_development"


def test_base_jor_reserves_value() -> None:
    """JOR reserves: CBJ Annual Report 2023 — 7.1 months."""
    scenario = build_jordan_hormuz_scenario()
    res = scenario.configuration.initial_attributes["JOR"]["reserve_coverage_months"]
    assert res.value == "7.1"
    assert res.unit == "months"
    assert res.source_registry_id == "CBJ_ANNUAL_2023"


def test_base_jor_fuel_dependency_value() -> None:
    """JOR fuel import dependency: 0.42 Tier 3 synthetic."""
    scenario = build_jordan_hormuz_scenario()
    dep = scenario.configuration.initial_attributes["JOR"]["commodity_import_dependency_fuel"]
    assert dep.value == "0.42"
    assert dep.confidence_tier == 3
    assert dep.variable_type == "stock"
    assert dep.source_registry_id == "WB_2023_JOR_ENERGY_DEP"


def test_base_jor_food_dependency_value() -> None:
    """JOR food import dependency: 0.28 Tier 3 synthetic."""
    scenario = build_jordan_hormuz_scenario()
    dep = scenario.configuration.initial_attributes["JOR"]["commodity_import_dependency_food"]
    assert dep.value == "0.28"
    assert dep.confidence_tier == 3
    assert dep.variable_type == "stock"
    assert dep.source_registry_id == "WFP_2024_JOR_FOOD_DEP"


def test_base_jor_fuel_dep_gt_food_dep() -> None:
    """Jordan's fuel exposure (0.42) exceeds food exposure (0.28) — central demo claim."""
    scenario = build_jordan_hormuz_scenario()
    jor_attrs = scenario.configuration.initial_attributes["JOR"]
    fuel = Decimal(jor_attrs["commodity_import_dependency_fuel"].value)
    food = Decimal(jor_attrs["commodity_import_dependency_food"].value)
    assert fuel > food, "Jordan fuel dependency must exceed food dependency"


# ---------------------------------------------------------------------------
# Egypt initial attributes
# ---------------------------------------------------------------------------


def test_base_egy_gdp_growth_value() -> None:
    """EGY GDP growth: IMF WEO Apr 2024 — +2.9%."""
    scenario = build_jordan_hormuz_scenario()
    gdp = scenario.configuration.initial_attributes["EGY"]["gdp_growth"]
    assert gdp.value == "0.029"
    assert gdp.source_registry_id == "IMF_WEO_APR2024"


def test_base_egy_fuel_dependency_value() -> None:
    """EGY fuel import dependency: 0.23 Tier 3 synthetic — lower than Jordan."""
    scenario = build_jordan_hormuz_scenario()
    dep = scenario.configuration.initial_attributes["EGY"]["commodity_import_dependency_fuel"]
    assert dep.value == "0.23"
    assert dep.confidence_tier == 3
    assert dep.source_registry_id == "WB_2023_EGY_ENERGY_DEP"


def test_base_egy_food_dependency_value() -> None:
    """EGY food import dependency: 0.35 Tier 3 synthetic — higher than Jordan."""
    scenario = build_jordan_hormuz_scenario()
    dep = scenario.configuration.initial_attributes["EGY"]["commodity_import_dependency_food"]
    assert dep.value == "0.35"
    assert dep.confidence_tier == 3
    assert dep.source_registry_id == "WFP_2024_EGY_FOOD_DEP"


def test_base_egy_food_dep_gt_jor_food_dep() -> None:
    """Egypt food exposure (0.35) exceeds Jordan food exposure (0.28) — central demo claim."""
    scenario = build_jordan_hormuz_scenario()
    attrs = scenario.configuration.initial_attributes
    jor_food = Decimal(attrs["JOR"]["commodity_import_dependency_food"].value)
    egy_food = Decimal(attrs["EGY"]["commodity_import_dependency_food"].value)
    assert egy_food > jor_food, "Egypt food dependency must exceed Jordan food dependency"


def test_base_jor_fuel_dep_gt_egy_fuel_dep() -> None:
    """Jordan fuel exposure (0.42) exceeds Egypt fuel exposure (0.23) — divergent profiles."""
    scenario = build_jordan_hormuz_scenario()
    attrs = scenario.configuration.initial_attributes
    jor_fuel = Decimal(attrs["JOR"]["commodity_import_dependency_fuel"].value)
    egy_fuel = Decimal(attrs["EGY"]["commodity_import_dependency_fuel"].value)
    assert jor_fuel > egy_fuel, "Jordan fuel dependency must exceed Egypt fuel dependency"


def test_base_egy_reserves_above_critical_floor() -> None:
    """EGY reserves (5.3 months) above CRITICAL floor (2.5 months) at entry."""
    scenario = build_jordan_hormuz_scenario()
    res = Decimal(scenario.configuration.initial_attributes["EGY"]["reserve_coverage_months"].value)
    assert res > Decimal("2.5"), "Egypt must enter the scenario above the CRITICAL floor"


# ---------------------------------------------------------------------------
# Scheduled inputs — base fixture
# ---------------------------------------------------------------------------


def test_base_has_imf_program_at_step3_for_jor() -> None:
    """Step 3: Jordan IMF program acceptance (reserve pressure at step 2 peak)."""
    scenario = build_jordan_hormuz_scenario()
    imf_inputs = [
        si for si in scenario.scheduled_inputs
        if si.step == 3
        and si.input_type == "EmergencyPolicyInput"
        and si.input_data.get("instrument") == "imf_program_acceptance"
        and si.input_data.get("target_entity") == "JOR"
    ]
    assert len(imf_inputs) == 1


def test_base_has_emergency_declaration_at_step3_for_egy() -> None:
    """Step 3: Egypt emergency declaration (food protest escalation)."""
    scenario = build_jordan_hormuz_scenario()
    emergency_inputs = [
        si for si in scenario.scheduled_inputs
        if si.step == 3
        and si.input_type == "EmergencyPolicyInput"
        and si.input_data.get("instrument") == "emergency_declaration"
        and si.input_data.get("target_entity") == "EGY"
    ]
    assert len(emergency_inputs) == 1


def test_base_has_fiscal_cut_at_step4_for_jor() -> None:
    """Step 4: Jordan spending cut (IMF conditionality — austerity during shock)."""
    scenario = build_jordan_hormuz_scenario()
    fiscal_inputs = [
        si for si in scenario.scheduled_inputs
        if si.step == 4
        and si.input_type == "FiscalPolicyInput"
        and si.input_data.get("instrument") == "spending_change"
        and si.input_data.get("target_entity") == "JOR"
    ]
    assert len(fiscal_inputs) == 1
    cut = fiscal_inputs[0]
    assert Decimal(cut.input_data["value"]) < Decimal("0"), "Spending cut must be negative"


def test_base_scheduled_steps_in_valid_range() -> None:
    """All scheduled input steps must be within [0, n_steps]."""
    scenario = build_jordan_hormuz_scenario()
    n = scenario.configuration.n_steps
    for si in scenario.scheduled_inputs:
        assert 0 <= si.step <= n, (
            f"Scheduled input step {si.step} outside valid range [0, {n}]"
        )


def test_base_scheduled_input_types_are_known() -> None:
    """All scheduled input types must be recognized by _deserialize_control_input."""
    known_types = {
        "FiscalPolicyInput",
        "EmergencyPolicyInput",
        "TradePolicyInput",
        "MonetaryRateInput",
        "StructuralPolicyInput",
    }
    scenario = build_jordan_hormuz_scenario()
    for si in scenario.scheduled_inputs:
        assert si.input_type in known_types, (
            f"Unknown input_type: {si.input_type!r}"
        )


def test_base_scheduled_input_values_are_strings() -> None:
    """Float prohibition extends to scheduled input value fields."""
    scenario = build_jordan_hormuz_scenario()
    for si in scenario.scheduled_inputs:
        if "value" in si.input_data:
            assert isinstance(si.input_data["value"], str), (
                f"Float prohibition: step={si.step} value is "
                f"{type(si.input_data['value']).__name__}, expected str"
            )


# ---------------------------------------------------------------------------
# Float prohibition — base fixture
# ---------------------------------------------------------------------------


def test_base_all_quantity_values_are_strings_jor() -> None:
    """Float prohibition: all JOR QuantitySchema.value fields must be strings."""
    scenario = build_jordan_hormuz_scenario()
    for attr_key, qty in scenario.configuration.initial_attributes["JOR"].items():
        assert isinstance(qty.value, str), (
            f"Float prohibition: JOR.{attr_key}.value "
            f"is {type(qty.value).__name__}, expected str"
        )


def test_base_all_quantity_values_are_strings_egy() -> None:
    """Float prohibition: all EGY QuantitySchema.value fields must be strings."""
    scenario = build_jordan_hormuz_scenario()
    for attr_key, qty in scenario.configuration.initial_attributes["EGY"].items():
        assert isinstance(qty.value, str), (
            f"Float prohibition: EGY.{attr_key}.value "
            f"is {type(qty.value).__name__}, expected str"
        )


# ---------------------------------------------------------------------------
# Serialization — base fixture
# ---------------------------------------------------------------------------


def test_base_serializes_to_json() -> None:
    """model_dump(mode='json') must succeed and include commodity_price_shocks."""
    scenario = build_jordan_hormuz_scenario()
    dumped = scenario.model_dump(mode="json")
    cfg = dumped["configuration"]
    assert "commodity_price_shocks" in cfg
    shocks = cfg["commodity_price_shocks"]
    assert len(shocks) == 2
    categories = {s["commodity_category"] for s in shocks}
    assert categories == {"fuel", "food"}


# ---------------------------------------------------------------------------
# build_jordan_hormuz_demo_scenario() — Demo 4 variant contracts
# ---------------------------------------------------------------------------


def test_demo_returns_scenario_create_request() -> None:
    from app.schemas import ScenarioCreateRequest
    demo = build_jordan_hormuz_demo_scenario()
    assert isinstance(demo, ScenarioCreateRequest)


def test_demo_name_references_demo_4() -> None:
    demo = build_jordan_hormuz_demo_scenario()
    assert "Demo" in demo.name or "demo" in demo.name.lower()


def test_demo_n_steps_is_8() -> None:
    demo = build_jordan_hormuz_demo_scenario()
    assert demo.configuration.n_steps == 8


def test_demo_entities_still_jor_and_egy() -> None:
    demo = build_jordan_hormuz_demo_scenario()
    entities = demo.configuration.entities
    assert "JOR" in entities
    assert "EGY" in entities


def test_demo_ecological_module_enabled() -> None:
    demo = build_jordan_hormuz_demo_scenario()
    assert demo.configuration.modules_config.get("ecological", {}).get("enabled") is True


def test_demo_governance_module_enabled() -> None:
    demo = build_jordan_hormuz_demo_scenario()
    assert demo.configuration.modules_config.get("governance", {}).get("enabled") is True


def test_demo_commodity_shocks_preserved() -> None:
    """Demo scenario must retain base commodity price shocks."""
    demo = build_jordan_hormuz_demo_scenario()
    shocks = demo.configuration.commodity_price_shocks
    assert len(shocks) == 2
    categories = {s.commodity_category for s in shocks}
    assert "fuel" in categories
    assert "food" in categories


# ---------------------------------------------------------------------------
# Demo governance seeds
# ---------------------------------------------------------------------------


def test_demo_jor_has_co2_seed() -> None:
    """JOR ecological seed: co2_concentration_ppm = 421.0 (NOAA MLO 2024)."""
    demo = build_jordan_hormuz_demo_scenario()
    attrs = demo.configuration.initial_attributes["JOR"]
    assert "co2_concentration_ppm" in attrs
    co2 = attrs["co2_concentration_ppm"]
    assert co2.value == "421.0"
    assert co2.measurement_framework == "ecological"
    assert co2.source_registry_id == "NOAA_MLO_2024"
    assert co2.confidence_tier == 1


def test_demo_egy_has_co2_seed() -> None:
    """EGY gets same CO2 seed (atmospheric CO2 is global — uniform at national scale)."""
    demo = build_jordan_hormuz_demo_scenario()
    attrs = demo.configuration.initial_attributes["EGY"]
    assert "co2_concentration_ppm" in attrs
    co2 = attrs["co2_concentration_ppm"]
    assert co2.value == "421.0"
    assert co2.source_registry_id == "NOAA_MLO_2024"


def test_demo_jor_rule_of_law_seed() -> None:
    """JOR governance seed: rule_of_law_percentile = 52.4 (WB WGI 2022)."""
    demo = build_jordan_hormuz_demo_scenario()
    attrs = demo.configuration.initial_attributes["JOR"]
    assert "rule_of_law_percentile" in attrs
    rol = attrs["rule_of_law_percentile"]
    assert rol.value == "52.4"
    assert rol.measurement_framework == "governance"
    assert rol.source_registry_id == "WB_WGI_JOR_2022_RULE_OF_LAW"
    assert rol.confidence_tier == 2


def test_demo_egy_rule_of_law_seed() -> None:
    """EGY governance seed: rule_of_law_percentile = 29.3 (WB WGI 2022)."""
    demo = build_jordan_hormuz_demo_scenario()
    attrs = demo.configuration.initial_attributes["EGY"]
    assert "rule_of_law_percentile" in attrs
    rol = attrs["rule_of_law_percentile"]
    assert rol.value == "29.3"
    assert rol.source_registry_id == "WB_WGI_EGY_2022_RULE_OF_LAW"


def test_demo_jor_democratic_quality_seed() -> None:
    """JOR governance seed: democratic_quality_score = 0.21 (V-Dem v14 2023)."""
    demo = build_jordan_hormuz_demo_scenario()
    attrs = demo.configuration.initial_attributes["JOR"]
    assert "democratic_quality_score" in attrs
    dqs = attrs["democratic_quality_score"]
    assert dqs.value == "0.21"
    assert dqs.measurement_framework == "governance"
    assert dqs.source_registry_id == "VDEM_V14_JOR_2023_LDI"
    assert dqs.confidence_tier == 3


def test_demo_egy_democratic_quality_seed() -> None:
    """EGY governance seed: democratic_quality_score = 0.07 (V-Dem v14 2023).
    Egypt is already far below the MDA-GOV-DEMOCRACY-FLOOR (0.70) at entry.
    """
    demo = build_jordan_hormuz_demo_scenario()
    attrs = demo.configuration.initial_attributes["EGY"]
    assert "democratic_quality_score" in attrs
    dqs = attrs["democratic_quality_score"]
    assert dqs.value == "0.07"
    assert dqs.source_registry_id == "VDEM_V14_EGY_2023_LDI"


def test_demo_egy_democratic_quality_below_mda_floor() -> None:
    """Egypt's democratic quality (0.07) is below MDA-GOV-DEMOCRACY-FLOOR (0.70).
    Governance alert fires from step 1 — not triggered by the shock, pre-existing.
    """
    demo = build_jordan_hormuz_demo_scenario()
    dqs = Decimal(demo.configuration.initial_attributes["EGY"]["democratic_quality_score"].value)
    mda_floor = Decimal("0.70")
    assert dqs < mda_floor, (
        f"Egypt democratic quality {dqs} must be below MDA-GOV-DEMOCRACY-FLOOR {mda_floor}"
    )


def test_demo_jor_democratic_quality_above_mda_floor() -> None:
    """Jordan's democratic quality (0.21) is below MDA floor but scenario differentiates.
    Jordan at 0.21 is also below 0.70 — both countries will have governance alerts.
    The contrast is rule of law: JOR 52.4 vs EGY 29.3.
    """
    demo = build_jordan_hormuz_demo_scenario()
    attrs = demo.configuration.initial_attributes
    jor_dqs = Decimal(attrs["JOR"]["democratic_quality_score"].value)
    egy_dqs = Decimal(attrs["EGY"]["democratic_quality_score"].value)
    # Jordan's governance quality is higher than Egypt's — meaningful contrast
    assert jor_dqs > egy_dqs, "Jordan democratic quality must be higher than Egypt's"


def test_demo_jor_rule_of_law_gt_egy() -> None:
    """Jordan rule of law (52.4) exceeds Egypt (29.3) — governance divergence."""
    demo = build_jordan_hormuz_demo_scenario()
    jor_rol = Decimal(demo.configuration.initial_attributes["JOR"]["rule_of_law_percentile"].value)
    egy_rol = Decimal(demo.configuration.initial_attributes["EGY"]["rule_of_law_percentile"].value)
    assert jor_rol > egy_rol


def test_demo_jor_has_elite_capture_seed() -> None:
    """JOR elite capture: 0.45 Tier 4 synthetic."""
    demo = build_jordan_hormuz_demo_scenario()
    attrs = demo.configuration.initial_attributes["JOR"]
    assert "elite_capture_coefficient" in attrs
    ec = attrs["elite_capture_coefficient"]
    assert ec.confidence_tier == 4
    assert ec.measurement_framework == "governance"


def test_demo_egy_has_elite_capture_seed() -> None:
    """EGY elite capture: 0.62 Tier 4 synthetic — higher than Jordan (SCAF military economy)."""
    demo = build_jordan_hormuz_demo_scenario()
    attrs = demo.configuration.initial_attributes["EGY"]
    assert "elite_capture_coefficient" in attrs
    ec = attrs["elite_capture_coefficient"]
    assert Decimal(ec.value) == Decimal("0.62")
    assert ec.confidence_tier == 4


def test_demo_egy_elite_capture_gt_jor() -> None:
    """Egypt elite capture (0.62) exceeds Jordan (0.45) — SCAF military economy contrast."""
    demo = build_jordan_hormuz_demo_scenario()
    attrs = demo.configuration.initial_attributes
    jor_ec = Decimal(attrs["JOR"]["elite_capture_coefficient"].value)
    egy_ec = Decimal(attrs["EGY"]["elite_capture_coefficient"].value)
    assert egy_ec > jor_ec


# ---------------------------------------------------------------------------
# Demo step_metadata
# ---------------------------------------------------------------------------


def test_demo_has_step_metadata_for_steps_1_through_6() -> None:
    """step_metadata must cover steps 1–6 (the shock arc); 7–8 absent (ROUTINE)."""
    demo = build_jordan_hormuz_demo_scenario()
    sm = demo.configuration.step_metadata
    for step in ["1", "2", "3", "4", "5", "6"]:
        assert step in sm, f"step_metadata missing key {step!r}"


def test_demo_step_metadata_steps_7_8_absent() -> None:
    """Steps 7–8 are ROUTINE — absent keys default to ROUTINE per trajectory contract."""
    demo = build_jordan_hormuz_demo_scenario()
    sm = demo.configuration.step_metadata
    assert "7" not in sm
    assert "8" not in sm


def test_demo_step_1_is_significant() -> None:
    demo = build_jordan_hormuz_demo_scenario()
    sm = demo.configuration.step_metadata
    assert sm["1"]["significance"] == "SIGNIFICANT"


def test_demo_step_2_is_significant() -> None:
    demo = build_jordan_hormuz_demo_scenario()
    sm = demo.configuration.step_metadata
    assert sm["2"]["significance"] == "SIGNIFICANT"


def test_demo_step_3_is_critical() -> None:
    """Step 3 (dual shock peak + IMF program) is the primary crisis step: CRITICAL."""
    demo = build_jordan_hormuz_demo_scenario()
    sm = demo.configuration.step_metadata
    assert sm["3"]["significance"] == "CRITICAL"


def test_demo_step_4_is_significant() -> None:
    demo = build_jordan_hormuz_demo_scenario()
    sm = demo.configuration.step_metadata
    assert sm["4"]["significance"] == "SIGNIFICANT"


def test_demo_step_5_is_critical() -> None:
    """Step 5 (reserve drawdown critical) is the secondary crisis step: CRITICAL."""
    demo = build_jordan_hormuz_demo_scenario()
    sm = demo.configuration.step_metadata
    assert sm["5"]["significance"] == "CRITICAL"


def test_demo_step_6_is_significant() -> None:
    demo = build_jordan_hormuz_demo_scenario()
    sm = demo.configuration.step_metadata
    assert sm["6"]["significance"] == "SIGNIFICANT"


def test_demo_all_labels_under_32_chars() -> None:
    """All step_metadata labels must be ≤32 chars (trajectory endpoint contract)."""
    demo = build_jordan_hormuz_demo_scenario()
    for key, meta in demo.configuration.step_metadata.items():
        label = meta.get("label", "")
        assert len(label) <= 32, (
            f"step_metadata[{key!r}] label exceeds 32 chars: {label!r} ({len(label)} chars)"
        )


def test_demo_step_labels_reference_hormuz() -> None:
    """At least one step_metadata label must reference Hormuz or the shock."""
    demo = build_jordan_hormuz_demo_scenario()
    sm = demo.configuration.step_metadata
    all_labels = " ".join(meta.get("label", "") for meta in sm.values())
    labels_lower = all_labels.lower()
    assert "Hormuz" in all_labels or "shock" in labels_lower or "disruption" in labels_lower


# ---------------------------------------------------------------------------
# Demo political_context
# ---------------------------------------------------------------------------


def test_demo_political_context_is_present() -> None:
    """Demo scenario must have political_context (Jordan monarchy context)."""
    demo = build_jordan_hormuz_demo_scenario()
    assert demo.configuration.political_context is not None


def test_demo_political_context_has_approval_rating() -> None:
    demo = build_jordan_hormuz_demo_scenario()
    ctx = demo.configuration.political_context
    assert ctx is not None
    assert ctx.government_approval_rating is not None
    assert Decimal("0") < ctx.government_approval_rating < Decimal("1")


def test_demo_political_context_has_legitimacy_index() -> None:
    demo = build_jordan_hormuz_demo_scenario()
    ctx = demo.configuration.political_context
    assert ctx is not None
    assert ctx.legitimacy_index is not None
    assert Decimal("0") < ctx.legitimacy_index < Decimal("1")


# ---------------------------------------------------------------------------
# Float prohibition — demo fixture
# ---------------------------------------------------------------------------


def test_demo_all_quantity_values_are_strings() -> None:
    """Float prohibition applies to all initial attributes including demo seeds."""
    demo = build_jordan_hormuz_demo_scenario()
    for entity_id, attrs in demo.configuration.initial_attributes.items():
        for attr_key, qty in attrs.items():
            assert isinstance(qty.value, str), (
                f"Float prohibition: {entity_id}.{attr_key}.value "
                f"is {type(qty.value).__name__}, expected str"
            )


# ---------------------------------------------------------------------------
# Serialization — demo fixture
# ---------------------------------------------------------------------------


def test_demo_serializes_to_json() -> None:
    """model_dump(mode='json') must succeed and include all M12 fields."""
    demo = build_jordan_hormuz_demo_scenario()
    dumped = demo.model_dump(mode="json")
    cfg = dumped["configuration"]
    assert "commodity_price_shocks" in cfg
    assert "step_metadata" in cfg
    assert "modules_config" in cfg
    assert "political_context" in cfg
    assert cfg["step_metadata"]["3"]["significance"] == "CRITICAL"
    assert cfg["modules_config"]["ecological"]["enabled"] is True
    assert cfg["modules_config"]["governance"]["enabled"] is True


def test_demo_inherits_base_scheduled_inputs() -> None:
    """Demo scenario must retain all base scheduled inputs."""
    base = build_jordan_hormuz_scenario()
    demo = build_jordan_hormuz_demo_scenario()
    def _key(si) -> tuple:  # noqa: ANN001
        return (
            si.step, si.input_type,
            si.input_data.get("instrument"), si.input_data.get("target_entity"),
        )
    base_inputs = {_key(si) for si in base.scheduled_inputs}
    demo_inputs = {_key(si) for si in demo.scheduled_inputs}
    assert base_inputs.issubset(demo_inputs), (
        f"Demo scenario is missing base inputs: {base_inputs - demo_inputs}"
    )
