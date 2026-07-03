"""Egypt 2016 IMF SBA — devaluation sequencing and subsidy reform fixture.

Historical context:
  Egypt's 2016 IMF SBA (USD 12bn, 3 years) required two linked actions:
  a 48% EGP devaluation in one step and a phased energy subsidy removal.
  The programme ultimately succeeded — GDP growth recovered to 5% by 2018,
  reserves rebuilt to 8 months import cover by 2017.

  This makes Egypt distinct from other G2C cases: it is NOT a WorldSim
  failure-mode case. The 2016 IMF programme broadly achieved its objectives
  over the 4-step window. The fixture tests whether the engine correctly
  captures the DemographicModule CB Cloud signal (bottom quintile bore
  the cost before the financial stabilisation benefit reached them) even
  in a case where the aggregate economic outcome was positive.

  **Direction inversion note:** The counter-factual (phased devaluation)
  may produce BASELINE_BETTER or INDISTINGUISHABLE on fin_composite rather
  than COUNTER_FACTUAL_BETTER. The actual shock devaluation was more
  effective for reserves and FX stabilisation than phased adjustment would
  have been. The test must NOT hardcode an expected direction.

  Timeline modeled (4 biannual steps):
    2016 H1 (Step 1): 48% EGP devaluation (November 2016 — treating biannual
                      as event-based, not calendar midpoint). IMF SBA begins.
                      Energy subsidy round 1 removal.
    2016 H2 (Step 2): Energy subsidy round 2 removal.
    2017 H1 (Step 3): Energy subsidy round 3 removal.
    2017 H2 (Step 4): No new major shock. Reserve recovery begins.

  Failure modes: CB Cloud (Q1 poverty headcount rose through 2016–2018 while
  reserves improved), Hypoxia (subsidy reform sequencing made with incomplete
  picture of bottom-quintile food expenditure share).

Entity: EGY — already seeded from ADR-016 grounding strip work (M14).
Verify 2015 baseline attributes against the seeded entity before testing.

Simulation structure:
  build_egypt_scenario(): n_steps=4, biannual. Historical shock devaluation.
  build_egypt_counterfactual_scenario(): n_steps=4, biannual. Phased devaluation
    (-12% per step × 4), same cumulative -48% target.

Counter-factual question: does phased devaluation produce materially lower
Q1 poverty headcount impact, holding the same cumulative adjustment target?

Initial state sources (2015 baseline, pre-devaluation):
  gdp_growth         — IMF WEO April 2016 (EGY FY2015 outturn: 4.4%)
  unemployment_rate  — CAPMAS Labour Market Survey Q4 2015 (~12.0%)
  reserve_coverage_months — CBE Monthly Statistics November 2015 (~3.4 months)
  sovereign_risk_premium — JP Morgan EMBI+ EGY October 2016 pre-IMF (~350 bps)
  fdi_stock_pct_gdp  — UNCTAD WIR 2016 (EGY: ~19.5%)
  portfolio_flow_velocity — CBE BOP 2015 (outflow ~-0.012)
  credit_rating_score — S&P B- December 2015. 21-notch: B- = 24.
  q1_poverty_headcount_ratio — CAPMAS Household Income/Expenditure Survey 2015: 27.8%

References: Issue #1552; CM advisory 2026-07-03.
"""
from __future__ import annotations

from datetime import date

from app.schemas import (
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScheduledInputSchema,
)


def build_egypt_scenario() -> ScenarioCreateRequest:
    """Build Egypt 2016 IMF SBA shock devaluation baseline.

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    4 biannual steps from 2015 baseline (pre-devaluation) through 2017 H2.
    Step 1: 48% EGP devaluation + IMF SBA + energy subsidy removal round 1.
    Steps 2–3: phased energy subsidy removal.

    NOTE: Direction inversion expected. This programme succeeded. The fin_composite
    direction may be BASELINE_BETTER vs the phased counter-factual.
    """
    initial_gdp_growth = QuantitySchema(
        value="0.044",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2016, 4, 1),
        source_registry_id="IMF_WEO_APR2016_EGY",
        measurement_framework="financial",
    )

    initial_unemployment_rate = QuantitySchema(
        value="0.120",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2015, 12, 31),
        source_registry_id="CAPMAS_LMS_EGY_Q42015",
        measurement_framework="human_development",
    )

    # CBE: forex reserves November 2015 at ~3.4 months import cover
    initial_reserve_coverage_months = QuantitySchema(
        value="3.4",
        unit="months",
        variable_type="stock",
        attribute_type="stock",
        confidence_tier=1,
        observation_date=date(2015, 11, 30),
        source_registry_id="CBE_MONTHLY_STATS_EGY_NOV2015",
        measurement_framework="financial",
    )

    # JP Morgan EMBI+ EGY October 2016 (pre-IMF deal): ~350 bps
    initial_sovereign_risk_premium = QuantitySchema(
        value="0.035",
        unit="ratio",
        variable_type="ratio",
        attribute_type="rate",
        confidence_tier=2,
        observation_date=date(2016, 10, 31),
        source_registry_id="JPMORGAN_EMBI_EGY_2016Q3",
        measurement_framework="financial",
    )

    # UNCTAD WIR 2016 — EGY inward FDI stock / GDP: ~19.5%
    initial_fdi_stock_pct_gdp = QuantitySchema(
        value="0.195",
        unit="ratio",
        variable_type="stock",
        attribute_type="stock",
        confidence_tier=2,
        observation_date=date(2015, 1, 1),
        source_registry_id="UNCTAD_WIR_EGY_2015",
        measurement_framework="financial",
    )

    # CBE BOP 2015: modest net portfolio outflow (~-1.2% GDP)
    initial_portfolio_flow_velocity = QuantitySchema(
        value="-0.012",
        unit="ratio",
        variable_type="ratio",
        attribute_type="flow",
        confidence_tier=2,
        observation_date=date(2015, 1, 1),
        source_registry_id="CBE_BOP_EGY_2015",
        measurement_framework="financial",
    )

    # S&P B- December 2015. 21-notch linear: B- = 24.
    initial_credit_rating_score = QuantitySchema(
        value="24.0",
        unit="index_0_100",
        variable_type="stock",
        attribute_type="structural_index",
        confidence_tier=1,
        observation_date=date(2015, 12, 31),
        source_registry_id="SP_SOVEREIGN_RATINGS_EGY_2015",
        measurement_framework="financial",
    )

    # CAPMAS HIECS 2015: Q1 poverty headcount 27.8% (national poverty line)
    initial_q1_poverty_headcount = QuantitySchema(
        value="0.278",
        unit="ratio",
        variable_type="ratio",
        attribute_type="rate",
        confidence_tier=2,
        observation_date=date(2015, 1, 1),
        source_registry_id="CAPMAS_HIECS_EGY_2015",
        measurement_framework="human_development",
    )

    return ScenarioCreateRequest(
        name="Egypt 2016 IMF SBA — Shock Devaluation Baseline",
        description=(
            "Backtesting fixture for Issue #1552. "
            "Egypt 2016 IMF SBA: 48% EGP devaluation in one step (Step 1) "
            "with phased energy subsidy removal across Steps 1–3. "
            "Not a WorldSim failure-mode case — programme achieved objectives. "
            "CB Cloud signal: Q1 poverty headcount rose while reserves improved. "
            "DemographicModule primary test: subsidy removal → food expenditure → Q1 PHC. "
            "Type B primary indicator: fin_composite. "
            "DIRECTION INVERSION: CF (phased) may produce BASELINE_BETTER. "
            "Initial state: IMF WEO April 2016 + CAPMAS 2015 + CBE data."
        ),
        configuration=ScenarioConfigSchema(
            entities=["EGY"],
            n_steps=4,
            timestep_label="biannual",
            start_date=date(2015, 1, 1),
            step_metadata={
                "1": {"significance": "SIGNIFICANT", "label": "48% EGP devaluation / IMF SBA"},
                "2": {"significance": "SIGNIFICANT", "label": "Energy subsidy removal round 2"},
                "3": {"significance": "SIGNIFICANT", "label": "Energy subsidy removal round 3"},
                "4": {"significance": "ROUTINE", "label": "Reserve recovery phase"},
            },
            initial_attributes={
                "EGY": {
                    "gdp_growth": initial_gdp_growth,
                    "unemployment_rate": initial_unemployment_rate,
                    "reserve_coverage_months": initial_reserve_coverage_months,
                    "sovereign_risk_premium": initial_sovereign_risk_premium,
                    "fdi_stock_pct_gdp": initial_fdi_stock_pct_gdp,
                    "portfolio_flow_velocity": initial_portfolio_flow_velocity,
                    "credit_rating_score": initial_credit_rating_score,
                    "q1_poverty_headcount_ratio": initial_q1_poverty_headcount,
                },
            },
        ),
        scheduled_inputs=[
            # Step 1 (2016 H1): IMF SBA + 48% EGP devaluation + energy subsidy round 1.
            ScheduledInputSchema(
                step=1,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "imf_program_acceptance",
                    "target_entity": "EGY",
                    "expected_duration": 3,
                    "program_size_gdp_ratio": "0.12",
                },
            ),
            ScheduledInputSchema(
                step=1,
                input_type="MonetaryVolumeInput",
                input_data={
                    "instrument": "exchange_rate_intervention",
                    "target_entity": "EGY",
                    "value": "-0.48",
                    "unit": "ratio",
                    "currency_code": "EGP",
                    "price_basis": "nominal",
                    "exchange_rate_type": "official",
                },
            ),
            ScheduledInputSchema(
                step=1,
                input_type="StructuralPolicyInput",
                input_data={
                    "instrument": "regulatory_change",
                    "target_entity": "EGY",
                    "affected_sector": "energy",
                    "implementation_years": 1,
                },
            ),

            # Step 2 (2016 H2): Energy subsidy removal round 2.
            ScheduledInputSchema(
                step=2,
                input_type="StructuralPolicyInput",
                input_data={
                    "instrument": "regulatory_change",
                    "target_entity": "EGY",
                    "affected_sector": "energy",
                    "implementation_years": 1,
                },
            ),

            # Step 3 (2017 H1): Energy subsidy removal round 3.
            ScheduledInputSchema(
                step=3,
                input_type="StructuralPolicyInput",
                input_data={
                    "instrument": "regulatory_change",
                    "target_entity": "EGY",
                    "affected_sector": "energy",
                    "implementation_years": 1,
                },
            ),

            # Step 4 (2017 H2): No new inputs — recovery phase.
        ],
    )


def build_egypt_counterfactual_scenario() -> ScenarioCreateRequest:
    """Build Egypt counter-factual: phased devaluation (-12% per step × 4).

    Counter-factual question: does phased devaluation produce materially lower
    Q1 poverty headcount impact than the shock devaluation, holding the same
    cumulative -48% adjustment target?

    DIRECTION INVERSION CAUTION: The actual shock devaluation succeeded for
    financial stabilisation. direction_verdict may be BASELINE_BETTER on
    fin_composite. The test logs whichever verdict the model produces.

    Structural differences from baseline:
    - Steps 1–4: 4 × MonetaryVolumeInput at -12% each (vs single -48% at Step 1)
    - Same energy subsidy schedule
    - Same IMF SBA acceptance at Step 1

    AC-EGY-1: Step 1 MonetaryVolumeInput value differs ("-0.12" vs "-0.48").
    """
    base = build_egypt_scenario()

    return base.model_copy(update={
        "name": "Egypt 2016 Counter-Factual — Phased Devaluation (-12% × 4 Steps)",
        "description": (
            "Counter-factual for Issue #1552. "
            "Phased devaluation: -12% per step over 4 steps (same cumulative -48% target). "
            "DIRECTION INVERSION: direction_verdict may be BASELINE_BETTER — "
            "Egypt 2016 is not a WorldSim failure-mode case. "
            "Type B primary indicator: fin_composite. "
            "Known limitation: INFERRED_STRUCTURAL (Tier 3); "
            "devaluation → import price → Q1 PHC channel tested independently of GDP channel."
        ),
        "scheduled_inputs": [
            # Step 1: IMF SBA + first 12% devaluation + energy subsidy round 1
            ScheduledInputSchema(
                step=1,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "imf_program_acceptance",
                    "target_entity": "EGY",
                    "expected_duration": 3,
                    "program_size_gdp_ratio": "0.12",
                },
            ),
            ScheduledInputSchema(
                step=1,
                input_type="MonetaryVolumeInput",
                input_data={
                    "instrument": "exchange_rate_intervention",
                    "target_entity": "EGY",
                    "value": "-0.12",
                    "unit": "ratio",
                    "currency_code": "EGP",
                    "price_basis": "nominal",
                    "exchange_rate_type": "official",
                },
            ),
            ScheduledInputSchema(
                step=1,
                input_type="StructuralPolicyInput",
                input_data={
                    "instrument": "regulatory_change",
                    "target_entity": "EGY",
                    "affected_sector": "energy",
                    "implementation_years": 1,
                },
            ),

            # Step 2: second 12% devaluation + energy subsidy round 2
            ScheduledInputSchema(
                step=2,
                input_type="MonetaryVolumeInput",
                input_data={
                    "instrument": "exchange_rate_intervention",
                    "target_entity": "EGY",
                    "value": "-0.12",
                    "unit": "ratio",
                    "currency_code": "EGP",
                    "price_basis": "nominal",
                    "exchange_rate_type": "official",
                },
            ),
            ScheduledInputSchema(
                step=2,
                input_type="StructuralPolicyInput",
                input_data={
                    "instrument": "regulatory_change",
                    "target_entity": "EGY",
                    "affected_sector": "energy",
                    "implementation_years": 1,
                },
            ),

            # Step 3: third 12% devaluation + energy subsidy round 3
            ScheduledInputSchema(
                step=3,
                input_type="MonetaryVolumeInput",
                input_data={
                    "instrument": "exchange_rate_intervention",
                    "target_entity": "EGY",
                    "value": "-0.12",
                    "unit": "ratio",
                    "currency_code": "EGP",
                    "price_basis": "nominal",
                    "exchange_rate_type": "official",
                },
            ),
            ScheduledInputSchema(
                step=3,
                input_type="StructuralPolicyInput",
                input_data={
                    "instrument": "regulatory_change",
                    "target_entity": "EGY",
                    "affected_sector": "energy",
                    "implementation_years": 1,
                },
            ),

            # Step 4: fourth 12% devaluation (completes cumulative -48%)
            ScheduledInputSchema(
                step=4,
                input_type="MonetaryVolumeInput",
                input_data={
                    "instrument": "exchange_rate_intervention",
                    "target_entity": "EGY",
                    "value": "-0.12",
                    "unit": "ratio",
                    "currency_code": "EGP",
                    "price_basis": "nominal",
                    "exchange_rate_type": "official",
                },
            ),
        ],
    })
