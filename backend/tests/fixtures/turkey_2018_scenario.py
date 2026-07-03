"""Turkey 2018–19 lira crisis — Backside of the Power Curve scenario fixture.

Historical context:
  Turkey 2018–19 is the cleanest available real-world example of the
  Backside of the Power Curve failure mode in monetary policy.

  Timeline modeled (4 quarterly steps):
    2018 Q4 (Step 1): CBRT emergency rate hike to 24% (from 17.75%).
      The hike was 625 basis points in one step (September 2018) following
      the August 2018 currency crisis (TRY hit 7.24/USD). The hike initially
      stabilised the lira but left Turkey on the wrong side of the power curve:
      the rate was unsustainably high given the economy's structural inflation
      and the political context.

    2019 Q1 (Step 2): Hold. CBRT maintains 24% despite political pressure.
      President Erdoğan publicly demanded rate cuts throughout Q1 2019,
      calling for "logical rates". CBRT held through Q1 under Governor Çetinkaya.

    2019 Q3 (Step 3): First rate cut −425 bps (24% → 19.75%).
      Governor Çetinkaya was fired in July 2019 (first central bank governor
      dismissed mid-term in modern Turkey). New governor Murat Uysal immediately
      cut rates. This fired the Backside of the Power Curve and Hypoxia modes.

    2019 Q4 (Step 4): Second rate cut −425 bps (19.75% → 14%).
      Inflation remained above 8% throughout this period (12.3% in December 2019).
      Rate cuts with sticky inflation deepened the TRY depreciation trajectory.

Failure modes:
  - Backside of the Power Curve: standard monetary transmission inverted —
    rate cuts intended to stimulate growth instead accelerated TRY depreciation
    and imported inflation, shrinking the real economy
  - Hypoxia: CB independence compromised by executive pressure, impairing
    the institution's capacity to make rate decisions on monetary grounds

Counter-factual: maintain 24% rate (CB independence path).
  Steps 3–4: no rate cuts. GovernanceModule institutional_capacity_index
  is not degraded by the Hypoxia trigger since CB remains independent.

Simulation structure:
  build_turkey_scenario(): n_steps=4, quarterly. Actual rate-cut path.
  build_turkey_counterfactual_scenario(): n_steps=4, quarterly. Rate hold path.

Initial state sources (mid-2018, pre-crisis):
  gdp_growth         — IMF WEO April 2018 (TUR 2018 est: 4.2%)
  unemployment_rate  — TUIK Household Labour Force Survey H1 2018 (10.2%)
  sovereign_risk_premium — JP Morgan EMBI+ TUR August 2018 pre-hike (~320 bps)
  fdi_stock_pct_gdp  — UNCTAD WIR 2018 (TUR: ~18.8%)
  portfolio_flow_velocity — CBRT BOP 2018 H1 (outflow ~-0.04)
  credit_rating_score — Fitch BB- end-2018. 21-notch linear: BB- = 26.
  reserve_coverage_months — CBRT 2018 H1: ~4.5 months
  inflation_rate     — TUIK CPI August 2018: 17.9%

References: Issue #1551; CM advisory 2026-07-03.
"""
from __future__ import annotations

from datetime import date

from app.schemas import (
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScheduledInputSchema,
)


def build_turkey_scenario() -> ScenarioCreateRequest:
    """Build Turkey 2018–19 actual rate-cut baseline (Backside of Power Curve).

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    4 quarterly steps: 2018 Q4 → 2019 Q1 → 2019 Q3 → 2019 Q4.
    Step 1: emergency hike +6.25pp to 24%. Steps 3–4: rate cuts under pressure.
    """
    initial_gdp_growth = QuantitySchema(
        value="0.042",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2018, 4, 1),
        source_registry_id="IMF_WEO_APR2018_TUR",
        measurement_framework="financial",
    )

    initial_unemployment_rate = QuantitySchema(
        value="0.102",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2018, 6, 30),
        source_registry_id="TUIK_HLFS_TUR_2018H1",
        measurement_framework="human_development",
    )

    # CBRT: reserve coverage mid-2018 ~4.5 months (gross)
    initial_reserve_coverage_months = QuantitySchema(
        value="4.5",
        unit="months",
        variable_type="stock",
        attribute_type="stock",
        confidence_tier=2,
        observation_date=date(2018, 6, 30),
        source_registry_id="CBRT_RESERVES_TUR_2018H1",
        measurement_framework="financial",
    )

    # JP Morgan EMBI+ TUR August 2018 pre-emergency-hike: ~320 bps
    initial_sovereign_risk_premium = QuantitySchema(
        value="0.032",
        unit="ratio",
        variable_type="ratio",
        attribute_type="rate",
        confidence_tier=2,
        observation_date=date(2018, 8, 31),
        source_registry_id="JPMORGAN_EMBI_TUR_2018Q3",
        measurement_framework="financial",
    )

    # UNCTAD WIR 2018 — TUR inward FDI stock / GDP: ~18.8%
    initial_fdi_stock_pct_gdp = QuantitySchema(
        value="0.188",
        unit="ratio",
        variable_type="stock",
        attribute_type="stock",
        confidence_tier=2,
        observation_date=date(2018, 1, 1),
        source_registry_id="UNCTAD_WIR_TUR_2018",
        measurement_framework="financial",
    )

    # CBRT BOP 2018 H1: significant portfolio outflow (~-4% GDP)
    initial_portfolio_flow_velocity = QuantitySchema(
        value="-0.040",
        unit="ratio",
        variable_type="ratio",
        attribute_type="flow",
        confidence_tier=2,
        observation_date=date(2018, 6, 30),
        source_registry_id="CBRT_BOP_TUR_2018H1",
        measurement_framework="financial",
    )

    # Fitch BB- end-2018 (downgraded from BB in August 2018). 21-notch scale: BB- = 26.
    initial_credit_rating_score = QuantitySchema(
        value="26.0",
        unit="index_0_100",
        variable_type="stock",
        attribute_type="structural_index",
        confidence_tier=1,
        observation_date=date(2018, 12, 31),
        source_registry_id="FITCH_SOVEREIGN_RATINGS_TUR_2018",
        measurement_framework="financial",
    )

    # TUIK CPI August 2018: 17.9% YoY (peaked at this point)
    initial_inflation_rate = QuantitySchema(
        value="0.179",
        unit="ratio",
        variable_type="ratio",
        attribute_type="rate",
        confidence_tier=1,
        observation_date=date(2018, 8, 31),
        source_registry_id="TUIK_CPI_TUR_AUG2018",
        measurement_framework="financial",
    )

    return ScenarioCreateRequest(
        name="Turkey 2018-19 Lira Crisis — Backside of Power Curve Baseline",
        description=(
            "Backtesting fixture for Issue #1551. "
            "Turkey 2018–19: emergency rate hike to 24% (Step 1) → hold (Step 2) "
            "→ rate cuts under political pressure after CB governor fired (Steps 3–4). "
            "Backside of Power Curve: rate cuts with 8–12% inflation deepen TRY depreciation. "
            "Hypoxia: institutional_capacity_index degraded by CB independence compromise. "
            "Type B primary indicator: fin_composite. "
            "Initial state: IMF WEO April 2018 + TUIK HLFS 2018H1 + CBRT data."
        ),
        configuration=ScenarioConfigSchema(
            entities=["TUR"],
            n_steps=4,
            timestep_label="quarterly",
            start_date=date(2018, 9, 1),
            step_metadata={
                "1": {"significance": "SIGNIFICANT", "label": "Emergency hike to 24%"},
                "2": {"significance": "SIGNIFICANT", "label": "Hold under pressure"},
                "3": {"significance": "SIGNIFICANT", "label": "First cut / governor fired"},
                "4": {"significance": "SIGNIFICANT", "label": "Second cut / Hypoxia deepens"},
            },
            initial_attributes={
                "TUR": {
                    "gdp_growth": initial_gdp_growth,
                    "unemployment_rate": initial_unemployment_rate,
                    "reserve_coverage_months": initial_reserve_coverage_months,
                    "sovereign_risk_premium": initial_sovereign_risk_premium,
                    "fdi_stock_pct_gdp": initial_fdi_stock_pct_gdp,
                    "portfolio_flow_velocity": initial_portfolio_flow_velocity,
                    "credit_rating_score": initial_credit_rating_score,
                    "inflation_rate": initial_inflation_rate,
                },
            },
        ),
        scheduled_inputs=[
            # Step 1 (2018 Q4): Emergency CBRT hike +625 bps from 17.75% → 24%.
            ScheduledInputSchema(
                step=1,
                input_type="MonetaryRateInput",
                input_data={
                    "instrument": "policy_rate",
                    "target_entity": "TUR",
                    "value": "0.0625",
                    "duration_periods": 2,
                },
            ),

            # Step 2 (2019 Q1): Hold. No new inputs — CBRT maintains 24%.

            # Step 3 (2019 Q3): First rate cut −425 bps (24% → 19.75%).
            # Governor Çetinkaya fired; new governor Uysal immediately cuts.
            ScheduledInputSchema(
                step=3,
                input_type="MonetaryRateInput",
                input_data={
                    "instrument": "policy_rate",
                    "target_entity": "TUR",
                    "value": "-0.0425",
                    "duration_periods": 1,
                },
            ),

            # Step 4 (2019 Q4): Second cut −425 bps (19.75% → 14%).
            ScheduledInputSchema(
                step=4,
                input_type="MonetaryRateInput",
                input_data={
                    "instrument": "policy_rate",
                    "target_entity": "TUR",
                    "value": "-0.0425",
                    "duration_periods": 1,
                },
            ),
        ],
    )


def build_turkey_counterfactual_scenario() -> ScenarioCreateRequest:
    """Build Turkey counter-factual: CB independence path (rate hold at 24%).

    Counter-factual question: does maintaining the 24% rate (CB independence
    path) produce meaningfully better exchange rate stability and reserve
    protection than the actual rate-cut sequence?

    At what step does the rate-cut path enter regime-dependent deterioration?

    Structural differences from baseline:
    - Steps 3–4: NO rate cuts (hold at 24%)
    - GovernanceModule: no CB governor removal; institutional_capacity_index
      not degraded (no Hypoxia trigger in counter-factual)

    AC-TUR-1: Steps 3 and 4 have no MonetaryRateInput scheduled inputs.
    """
    base = build_turkey_scenario()

    return base.model_copy(update={
        "name": "Turkey 2018-19 Counter-Factual — CB Independence Path (Rate Hold at 24%)",
        "description": (
            "Counter-factual for Issue #1551. "
            "CBRT holds 24% rate through Steps 3–4 (CB independence maintained). "
            "No Hypoxia trigger: institutional_capacity_index not degraded. "
            "Type B primary indicator: fin_composite. "
            "Direction advisory: COUNTER_FACTUAL_BETTER on reserve protection. "
            "Known limitation: INFERRED_STRUCTURAL (Tier 3)."
        ),
        "scheduled_inputs": [
            # Step 1: same emergency hike to 24%
            ScheduledInputSchema(
                step=1,
                input_type="MonetaryRateInput",
                input_data={
                    "instrument": "policy_rate",
                    "target_entity": "TUR",
                    "value": "0.0625",
                    "duration_periods": 4,
                },
            ),
            # Steps 2–4: hold — no rate cut inputs. Counter-factual ends here.
            # The CB independence path means no step 3 or step 4 rate change inputs.
        ],
    })
