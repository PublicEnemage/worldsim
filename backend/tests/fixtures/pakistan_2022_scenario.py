"""Pakistan 2022–23 IMF programme survival — scenario configuration fixture.

Historical context:
  Pakistan's 23rd IMF engagement (EFF/SBA 2022–23) demonstrates the
  PoliticalEconomyModule's core stress test: repeated programme suspensions
  driven by political infeasibility of conditionality implementation.

  Pakistan's fiscal and balance-of-payments crisis of 2022:
    - Forex reserves fell to ~$4.5bn (less than 3 weeks import cover) by
      January 2023 — lowest in 9 years.
    - Fuel and electricity subsidies removed under political pressure in
      April 2022, then partially reinstated by new government.
    - IMF programme suspended twice in 2022 due to subsidy reinstatement
      and missed fiscal targets before the July 2023 SBA replaced the EFF.
    - PM Imran Khan removed April 2022; interim government inherited crisis.
    - Implementation capacity estimated at 0.6 (major conditions missed
      in 2022, recovered partially under Dar/Ishaq Dar FY23).

  Failure modes: Get-There-Itis (repeated programme failures without
  systemic change), Hypoxia (political interference in CB and finance
  ministry decisions on fuel subsidies).

Simulation structure:
  build_pakistan_scenario(): n_steps=4, biannual (2022 H1 → 2023 H2).
    Front-loaded conditionality — actual IMF programme path.
    Initial state: Pakistan FY2022 baseline (pre-August 2022 floods).

  build_pakistan_counterfactual_scenario(): n_steps=4, biannual.
    Phased conditionality — 25% fuel subsidy removal per step.
    implementation_capacity=0.85 per step (more feasible each step).
    Counter-factual question: does phased delivery produce better
    programme_survival_probability and lower Q1 poverty headcount impact?

Initial state sources (2022 H1 baseline):
  gdp_growth        — IMF WEO April 2022 (PAK FY2022 est: 5.97%)
  unemployment_rate — PBS Labour Force Survey 2021-22 (~6.0%)
  sovereign_risk_premium — JP Morgan EMBI+ PAK March 2022 (~450 bps)
  reserve_coverage_months — State Bank of Pakistan March 2022 (~1.9 months)
  fdi_stock_pct_gdp — UNCTAD WIR 2022 (PAK: ~9.1%)
  portfolio_flow_velocity — SBP BOP 2022 H1 (net outflow ~-0.02)
  credit_rating_score — S&P CCC+ March 2022, 21-notch scale: ~11

References: Issue #1550; CM advisory 2026-07-03.
"""
from __future__ import annotations

from datetime import date

from app.schemas import (
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScheduledInputSchema,
)


def build_pakistan_scenario() -> ScenarioCreateRequest:
    """Build Pakistan 2022–23 front-loaded IMF conditionality baseline.

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    4 biannual steps from 2022 H1 through 2023 H2.
    Fuel subsidy removed fully in Step 1 (IMF conditionality); implementation_capacity=0.6.
    """
    initial_gdp_growth = QuantitySchema(
        value="0.0597",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2022, 4, 1),
        source_registry_id="IMF_WEO_APR2022_PAK",
        measurement_framework="financial",
    )

    initial_unemployment_rate = QuantitySchema(
        value="0.060",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2022, 1, 1),
        source_registry_id="PBS_LFS_PAK_2022",
        measurement_framework="human_development",
    )

    # SBP reserves March 2022: ~$11.3bn on ~$70bn GDP → ~1.9 months import cover
    initial_reserve_coverage_months = QuantitySchema(
        value="1.9",
        unit="months",
        variable_type="stock",
        attribute_type="stock",
        confidence_tier=1,
        observation_date=date(2022, 3, 31),
        source_registry_id="SBP_RESERVES_PAK_2022Q1",
        measurement_framework="financial",
    )

    # JP Morgan EMBI+ PAK March 2022: ~450 bps (pre-political crisis peak)
    initial_sovereign_risk_premium = QuantitySchema(
        value="0.045",
        unit="ratio",
        variable_type="ratio",
        attribute_type="rate",
        confidence_tier=2,
        observation_date=date(2022, 3, 31),
        source_registry_id="JPMORGAN_EMBI_PAK_2022Q1",
        measurement_framework="financial",
    )

    # UNCTAD WIR 2022 — PAK inward FDI stock / GDP: ~9.1%
    initial_fdi_stock_pct_gdp = QuantitySchema(
        value="0.091",
        unit="ratio",
        variable_type="stock",
        attribute_type="stock",
        confidence_tier=2,
        observation_date=date(2022, 1, 1),
        source_registry_id="UNCTAD_WIR_PAK_2022",
        measurement_framework="financial",
    )

    # SBP BOP 2022 H1: net portfolio outflow ~-2% GDP
    initial_portfolio_flow_velocity = QuantitySchema(
        value="-0.020",
        unit="ratio",
        variable_type="ratio",
        attribute_type="flow",
        confidence_tier=2,
        observation_date=date(2022, 1, 1),
        source_registry_id="SBP_BOP_PAK_2022H1",
        measurement_framework="financial",
    )

    # S&P CCC+ March 2022 (downgraded from B-). 21-notch linear: CCC+ = 11.
    initial_credit_rating_score = QuantitySchema(
        value="11.0",
        unit="index_0_100",
        variable_type="stock",
        attribute_type="structural_index",
        confidence_tier=1,
        observation_date=date(2022, 3, 31),
        source_registry_id="SP_SOVEREIGN_RATINGS_PAK_2022Q1",
        measurement_framework="financial",
    )

    return ScenarioCreateRequest(
        name="Pakistan 2022-23 IMF Programme — Front-Loaded Conditionality Baseline",
        description=(
            "Backtesting fixture for Issue #1550. "
            "Pakistan 23rd IMF engagement: front-loaded conditionality with full fuel "
            "subsidy removal at Step 1. implementation_capacity=0.6 (political feasibility). "
            "InputSource.CONDITIONALITY at Step 1. Get-There-Itis and Hypoxia failure modes. "
            "Type B primary indicator: fin_composite. "
            "Initial state: IMF WEO April 2022 + PBS LFS 2022 + SBP data."
        ),
        configuration=ScenarioConfigSchema(
            entities=["PAK"],
            n_steps=4,
            timestep_label="biannual",
            start_date=date(2022, 1, 1),
            step_metadata={
                "1": {"significance": "SIGNIFICANT", "label": "Fuel subsidy removal / EFF"},
                "2": {"significance": "SIGNIFICANT", "label": "Energy reform / floods"},
                "3": {"significance": "SIGNIFICANT", "label": "Monetary tightening"},
                "4": {"significance": "ROUTINE", "label": "SBA stabilisation"},
            },
            initial_attributes={
                "PAK": {
                    "gdp_growth": initial_gdp_growth,
                    "unemployment_rate": initial_unemployment_rate,
                    "reserve_coverage_months": initial_reserve_coverage_months,
                    "sovereign_risk_premium": initial_sovereign_risk_premium,
                    "fdi_stock_pct_gdp": initial_fdi_stock_pct_gdp,
                    "portfolio_flow_velocity": initial_portfolio_flow_velocity,
                    "credit_rating_score": initial_credit_rating_score,
                },
            },
        ),
        scheduled_inputs=[
            # Step 1 (2022 H1): Fuel subsidy removal under IMF EFF conditionality.
            # Full subsidy removal (100%) — front-loaded. Implementation capacity 0.6:
            # government partially implemented then reversed under political pressure.
            ScheduledInputSchema(
                step=1,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "PAK",
                    "sector": "government",
                    "value": "-0.035",
                    "duration_years": 1,
                    "source": "conditionality",
                    "implementation_capacity": "0.6",
                    "constraining_actor_id": "IMF",
                },
            ),

            # Step 2 (2022 H2): Energy pricing structural reform + August 2022 floods shock.
            ScheduledInputSchema(
                step=2,
                input_type="StructuralPolicyInput",
                input_data={
                    "instrument": "regulatory_change",
                    "target_entity": "PAK",
                    "affected_sector": "energy",
                    "implementation_years": 2,
                },
            ),

            # Step 3 (2023 H1): SBP policy rate tightening (+3pp from ~15% → 18%).
            ScheduledInputSchema(
                step=3,
                input_type="MonetaryRateInput",
                input_data={
                    "instrument": "policy_rate",
                    "target_entity": "PAK",
                    "value": "0.030",
                    "duration_periods": 2,
                },
            ),

            # Step 4 (2023 H2): SBP policy rate hold under IMF SBA; no new inputs.
        ],
    )


def build_pakistan_counterfactual_scenario() -> ScenarioCreateRequest:
    """Build Pakistan counter-factual: phased conditionality, 25% per step.

    Counter-factual question: does phased fuel subsidy removal (25% per step
    over 4 steps) produce better programme_survival_probability and lower
    Q1 poverty headcount impact than front-loaded full removal in Step 1?

    Each step: 25% subsidy removal with implementation_capacity=0.85 (more
    feasible per-step), matching progressive political acceptance capacity.

    AC-PAK-1 check: Step 1 spending_change differs from baseline (0.6×-3.5% full
    vs 0.85×-0.875% phased at first step).
    """
    base = build_pakistan_scenario()

    return base.model_copy(update={
        "name": "Pakistan 2022-23 Counter-Factual — Phased Conditionality (25% per Step)",
        "description": (
            "Counter-factual for Issue #1550. "
            "Fuel subsidy removal phased: 25% per step instead of 100% at Step 1. "
            "implementation_capacity=0.85 per step (higher feasibility per increment). "
            "Type B primary indicator: fin_composite. "
            "Direction advisory: COUNTER_FACTUAL_BETTER on programme survival probability. "
            "Known limitation: INFERRED_STRUCTURAL (Tier 3)."
        ),
        "scheduled_inputs": [
            # Step 1: 25% subsidy removal, implementation_capacity=0.85
            ScheduledInputSchema(
                step=1,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "PAK",
                    "sector": "government",
                    "value": "-0.009",
                    "duration_years": 1,
                    "source": "conditionality",
                    "implementation_capacity": "0.85",
                    "constraining_actor_id": "IMF",
                },
            ),

            # Step 2: 25% more removal + energy reform
            ScheduledInputSchema(
                step=2,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "PAK",
                    "sector": "government",
                    "value": "-0.009",
                    "duration_years": 1,
                    "source": "conditionality",
                    "implementation_capacity": "0.85",
                    "constraining_actor_id": "IMF",
                },
            ),
            ScheduledInputSchema(
                step=2,
                input_type="StructuralPolicyInput",
                input_data={
                    "instrument": "regulatory_change",
                    "target_entity": "PAK",
                    "affected_sector": "energy",
                    "implementation_years": 2,
                },
            ),

            # Step 3: 25% more removal + moderate policy rate tightening (+2pp)
            ScheduledInputSchema(
                step=3,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "PAK",
                    "sector": "government",
                    "value": "-0.009",
                    "duration_years": 1,
                    "source": "conditionality",
                    "implementation_capacity": "0.85",
                    "constraining_actor_id": "IMF",
                },
            ),
            ScheduledInputSchema(
                step=3,
                input_type="MonetaryRateInput",
                input_data={
                    "instrument": "policy_rate",
                    "target_entity": "PAK",
                    "value": "0.020",
                    "duration_periods": 2,
                },
            ),

            # Step 4: Final 25% removal + +1pp rate adjustment
            ScheduledInputSchema(
                step=4,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "PAK",
                    "sector": "government",
                    "value": "-0.009",
                    "duration_years": 1,
                    "source": "conditionality",
                    "implementation_capacity": "0.85",
                    "constraining_actor_id": "IMF",
                },
            ),
            ScheduledInputSchema(
                step=4,
                input_type="MonetaryRateInput",
                input_data={
                    "instrument": "policy_rate",
                    "target_entity": "PAK",
                    "value": "0.010",
                    "duration_periods": 1,
                },
            ),
        ],
    })
