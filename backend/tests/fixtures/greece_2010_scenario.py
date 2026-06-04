"""Greece 2010–2015 IMF Program — scenario configuration fixture.

Defines the scenario configuration for the Greece 2010–2015 backtesting run
as a Python object. This fixture is consumed by the backtesting test in
tests/backtesting/test_greece_2010_2012.py.

Also exports build_greece_demo_scenario() for the M8 end-of-milestone demo
(Issue #269), which enables EcologicalModule via modules_config.

Design follows ADR-004 Decision 3. The ControlInput sequence approximates
the documented historical program:
  - Step 1 (2010): IMF program acceptance + fiscal spending cuts
  - Step 2 (2011): Second austerity package + deficit target
  - Step 3 (2012): Continued fiscal consolidation (third memorandum preparation)
  - Step 4 (2013): Primary surplus conditionality + fiscal adjustment
  - Step 5 (2014): Privatisation programme (ESM conditionality)
  - Step 6 (2015): Capital controls imposed 26 June 2015

ControlInput types are restricted to those implemented in
WebScenarioRunner._deserialize_control_input(). Instrument enum values must
match the ControlInput dataclass definitions in orchestration/inputs.py.

All Quantity values are strings per DATA_STANDARDS.md float prohibition.

Initial state sources — Issue #149:
  IMF_WEO_APR2010   — IMF World Economic Outlook April 2010, gdp_growth
  EUROSTAT_LFS_2010 — Eurostat Labour Force Survey Q1 2010, unemployment_rate
  WDI_2010          — World Bank World Development Indicators 2010 vintage
                      (published Dec 2011), health_expenditure_pct_gdp and
                      net_enrollment_secondary
"""
from __future__ import annotations

from datetime import date

from app.schemas import (
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScheduledInputSchema,
)


def build_greece_scenario() -> ScenarioCreateRequest:
    """Build the Greece 2010–2015 backtesting scenario configuration.

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    The scenario runs 6 steps (annual: 2010→2011→2012→2013→2014→2015→2016
    projection window) starting from Greece's 2010 initial economic conditions.

    Scheduled inputs represent the IMF/EU program conditionality:
      Step 1: IMF program acceptance (May 2010) + primary spending cuts
      Step 2: Second austerity package (June 2011) + deficit target
      Step 3: Third memorandum fiscal consolidation (2012)
      Step 4: Primary surplus target + fiscal adjustment (2013)
      Step 5: ESM privatisation programme (2014)
      Step 6: Capital controls (26 June 2015)

    Initial state attributes — Issue #149 (WDI human development seed):
      gdp_growth              — IMF WEO April 2010, -5.4% outturn
      unemployment_rate       — Eurostat LFS Q1 2010, 12.7%
      health_expenditure_pct_gdp — World Bank WDI 2010, 9.5% of GDP
      net_enrollment_secondary   — World Bank WDI 2010, 99.1%

    References: ADR-004 Decision 3; Issue #112; Issue #149; Issue #316.
    """
    initial_gdp_growth = QuantitySchema(
        value="-0.054",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=3,
        observation_date=date(2010, 4, 1),
        source_registry_id="IMF_WEO_APR2010",
        measurement_framework="financial",
    )

    # Eurostat LFS Q1 2010 — 12.7%; confidence_tier=2 (calibrated from
    # official national statistics). vintage_date = Q2 2010 release.
    initial_unemployment_rate = QuantitySchema(
        value="0.127",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2010, 7, 1),
        source_registry_id="EUROSTAT_LFS_2010",
        measurement_framework="human_development",
    )

    # World Bank WDI 2010 (published Dec 2011) — 9.5% of GDP
    initial_health_expenditure = QuantitySchema(
        value="0.095",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2011, 12, 1),
        source_registry_id="WDI_2010",
        measurement_framework="human_development",
    )

    # World Bank WDI 2010 (published Dec 2011) — 99.1% net enrollment
    initial_net_enrollment_secondary = QuantitySchema(
        value="0.991",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2011, 12, 1),
        source_registry_id="WDI_2010",
        measurement_framework="human_development",
    )

    # IMF Country Report 10/110 (May 2010) — Greece's effective import coverage
    # at programme entry was approximately 2.0 months (central government
    # liquidity position, pre-first-disbursement).  Below the MDA-FIN-RESERVES
    # CRITICAL floor (2.5 months), producing a persistent CRITICAL alert from
    # step 1 onward throughout the programme window.
    initial_reserve_coverage_months = QuantitySchema(
        value="2.0",
        unit="months",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2010, 5, 1),
        source_registry_id="IMF_CR10_110",
        measurement_framework="financial",
    )

    # Mean-reversion channel seed (ADR-006 Amendment 1 — Issue #221).
    # Greece long-run potential growth: approximately 2% — the pre-crisis
    # estimate that survived debt restructuring per Blanchard-Leigh (2013)
    # "Growth Forecast Errors and Fiscal Multipliers" (IMF WP/13/1).
    # Confidence tier 3: model estimate derived from academic literature.
    initial_trend_growth = QuantitySchema(
        value="0.02",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=3,
        observation_date=date(2010, 1, 1),
        source_registry_id="ACADEMIC_LITERATURE_BLANCHARD_LEIGH_2013",
        measurement_framework="financial",
    )

    return ScenarioCreateRequest(
        name="Greece 2010-2015 IMF Program Backtesting Fixture",
        description=(
            "Backtesting fixture for ADR-004 Decision 3, Issue #112, Issue #316. "
            "Reproduces the Greece 2010–2015 sovereign debt crisis, IMF/EU program "
            "conditionality, and capital controls episode to validate DIRECTION_ONLY "
            "fidelity thresholds across the full stabilization period. "
            "Initial state: IMF WEO April 2010 + Eurostat LFS 2010 + WDI 2010 "
            "+ IMF CR10/110 (reserve_coverage_months)."
        ),
        configuration=ScenarioConfigSchema(
            entities=["GRC"],
            n_steps=6,
            timestep_label="annual",
            start_date=date(2010, 1, 1),
            # step_metadata: all 6 steps are SIGNIFICANT — every year in the Greece
            # 2010–2015 arc has a named programme event. Labels ≤32 chars AND ≤8 words
            # per DATA_STANDARDS.md §Scenario Fixture Step Annotation (Issue #395).
            step_metadata={
                "1": {"significance": "SIGNIFICANT", "label": "First Memorandum / IMF SBA"},
                "2": {"significance": "SIGNIFICANT", "label": "Second Memorandum / MTFS"},
                "3": {"significance": "SIGNIFICANT", "label": "Third Memorandum / PSI"},
                "4": {"significance": "SIGNIFICANT", "label": "Primary Surplus Achieved"},
                "5": {"significance": "SIGNIFICANT", "label": "Privatisation / Snap Elections"},
                "6": {"significance": "CRITICAL", "label": "Capital Controls / Referendum"},
            },
            initial_attributes={
                "GRC": {
                    "gdp_growth": initial_gdp_growth,
                    "unemployment_rate": initial_unemployment_rate,
                    "health_expenditure_pct_gdp": initial_health_expenditure,
                    "net_enrollment_secondary": initial_net_enrollment_secondary,
                    "reserve_coverage_months": initial_reserve_coverage_months,
                    "trend_growth": initial_trend_growth,
                },
            },
        ),
        scheduled_inputs=[
            # Step 1 (2010): IMF program acceptance — €110bn ESM/IMF program, May 2010
            ScheduledInputSchema(
                step=1,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "imf_program_acceptance",
                    "target_entity": "GRC",
                    "expected_duration": 3,
                    "program_size_gdp_ratio": "0.48",
                },
            ),
            # Step 1 (2010): Fiscal spending cuts — 2010 Memorandum primary cuts
            ScheduledInputSchema(
                step=1,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "GRC",
                    "sector": "government",
                    "value": "-0.08",
                    "duration_years": 1,
                },
            ),
            # Step 2 (2011): Second austerity package — June 2011 Medium-Term Fiscal Strategy
            ScheduledInputSchema(
                step=2,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "GRC",
                    "sector": "government",
                    "value": "-0.05",
                    "duration_years": 1,
                },
            ),
            # Step 2 (2011): Deficit target — Medium-Term Fiscal Strategy 2011–2015
            ScheduledInputSchema(
                step=2,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "deficit_target",
                    "target_entity": "GRC",
                    "sector": "",
                    "value": "-0.03",
                    "duration_years": 4,
                },
            ),
            # Step 3 (2012): Third memorandum fiscal consolidation
            ScheduledInputSchema(
                step=3,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "GRC",
                    "sector": "government",
                    "value": "-0.04",
                    "duration_years": 1,
                },
            ),
            # Step 4 (2013): Primary surplus conditionality — +1.5% GDP achieved
            ScheduledInputSchema(
                step=4,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "GRC",
                    "sector": "government",
                    "value": "-0.02",
                    "duration_years": 1,
                },
            ),
            ScheduledInputSchema(
                step=4,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "deficit_target",
                    "target_entity": "GRC",
                    "sector": "",
                    "value": "0.015",
                    "duration_years": 2,
                },
            ),
            # Step 5 (2014): ESM privatisation programme conditionality
            ScheduledInputSchema(
                step=5,
                input_type="StructuralPolicyInput",
                input_data={
                    "instrument": "privatization",
                    "target_entity": "GRC",
                    "affected_sector": "public_assets",
                    "implementation_years": 3,
                },
            ),
            # Step 6 (2015): Capital controls — imposed 26 June 2015 by Greek government
            ScheduledInputSchema(
                step=6,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "capital_controls",
                    "target_entity": "GRC",
                    "expected_duration": 2,
                },
            ),
        ],
    )


def build_greece_demo_scenario() -> ScenarioCreateRequest:
    """Build the Greece 2010–2015 M10 demo scenario with Ecological and GovernanceModules enabled.

    Extends build_greece_scenario() with:
      - modules_config enabling EcologicalModule (planetary boundary proximity)
        and GovernanceModule (democratic quality + rule of law; ADR-005 Amendment 4)
      - co2_concentration_ppm initial seed (388.0 ppm — Mauna Loa 2010 annual mean)
      - rule_of_law_percentile initial seed (60.0 — WGI Rule of Law GRC 2010)
      - democratic_quality_score initial seed (0.72 — V-Dem LDI GRC 2010)
      - emergency_declaration scheduled input at step 5 (2014 political crisis /
        snap elections) to produce the governance deterioration event at step 6,
        triggering the MDA-GOV-DEMOCRACY-FLOOR alert (Issue #556 Criterion 6)

    Composite score status (M10):
      Ecological      — live (boundary proximity; 1 indicator active: CO2)
      Governance      — live (normalized_absolute; 2 indicators: LDI + RL percentile)
      Financial       — null (single-entity guard, Issue #193)
      Human Dev       — null (single-entity guard, Issue #193)

    References: Issue #269 (M8 demo); Issue #556 (M10 governance promotion);
    ADR-005 Amendments 3 and 4.
    """
    base = build_greece_scenario()

    # NOAA Mauna Loa Observatory 2010 annual mean: 388.0 ppm (confidence_tier=1).
    initial_co2_concentration = QuantitySchema(
        value="388.0",
        unit="ppm",
        variable_type="stock",
        confidence_tier=1,
        observation_date=date(2010, 1, 1),
        source_registry_id="NOAA_MLO_2010",
        measurement_framework="ecological",
    )

    # World Bank WGI 2010 — Rule of Law Percentile Rank for Greece: 60.0.
    # Confidence tier 2 (official multilateral statistics, annual survey).
    # Source: World Bank Worldwide Governance Indicators 2010 vintage.
    initial_rule_of_law = QuantitySchema(
        value="60.0",
        unit="percentile_0_100",
        variable_type="stock",
        confidence_tier=2,
        observation_date=date(2010, 1, 1),
        source_registry_id="WB_WGI_GRC_2010_RULE_OF_LAW",
        measurement_framework="governance",
    )

    # V-Dem v13 Liberal Democracy Index for Greece 2010: 0.72.
    # Confidence tier 3 (expert-coded survey; high credibility but not official stats).
    # Provides the initial seed for the democratic_quality_score stock path.
    initial_democratic_quality = QuantitySchema(
        value="0.72",
        unit="ratio_0_1",
        variable_type="stock",
        confidence_tier=3,
        observation_date=date(2010, 1, 1),
        source_registry_id="VDEM_V13_GRC_2010_LDI",
        measurement_framework="governance",
    )

    updated_grc_attrs = {
        **base.configuration.initial_attributes.get("GRC", {}),
        "co2_concentration_ppm": initial_co2_concentration,
        "rule_of_law_percentile": initial_rule_of_law,
        "democratic_quality_score": initial_democratic_quality,
    }

    demo_config = base.configuration.model_copy(
        update={
            "modules_config": {
                "ecological": {"enabled": True},
                "governance": {"enabled": True},
            },
            "initial_attributes": {"GRC": updated_grc_attrs},
        }
    )

    # emergency_declaration at step 5 (2014 political crisis — snap elections,
    # intensified anti-austerity governance pressure). One-step lag: GovernanceModule
    # reads this as a prior-step event at step 6, reducing democratic_quality_score
    # by 0.05 (elasticity -0.05 × magnitude +1.0). With seed 0.72 and cumulative
    # IMF-acceptance delta +0.005, step-6 score ≈ 0.675 < 0.70 floor →
    # MDA-GOV-DEMOCRACY-FLOOR WARNING fires (Issue #556 Criterion 6).
    emergency_input = ScheduledInputSchema(
        step=5,
        input_type="EmergencyPolicyInput",
        input_data={
            "instrument": "emergency_declaration",
            "target_entity": "GRC",
            "expected_duration": 2,
        },
    )

    demo_scheduled = list(base.scheduled_inputs) + [emergency_input]

    return base.model_copy(update={
        "name": "Greece 2010-2015 M10 Demo — Multi-Framework Measurement",
        "description": (
            "M10 end-of-milestone demo scenario (Issue #556). "
            "EcologicalModule and GovernanceModule enabled — all four framework axes live. "
            "Governance composite uses normalized_absolute strategy "
            "(WGI/V-Dem; ADR-005 Amendment 4). "
            "Financial and human_development composites are null "
            "(percentile rank requires ≥2 entities, Issue #193). "
            "Initial state: IMF WEO April 2010 + Eurostat LFS 2010 + WDI 2010 "
            "+ IMF CR10/110 (reserve_coverage_months) "
            "+ NOAA MLO 2010 (co2_concentration_ppm) "
            "+ WB WGI 2010 (rule_of_law_percentile=60.0) "
            "+ V-Dem v13 (democratic_quality_score=0.72)."
        ),
        "configuration": demo_config,
        "scheduled_inputs": demo_scheduled,
    })
