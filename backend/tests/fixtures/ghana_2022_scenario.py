"""Ghana 2022–23 Eurobond default and IMF programme — scenario fixture.

Historical context:
  Ghana's 2022–23 crisis is a canonical Coffin Corner / CB Cloud case:
  the country lost Eurobond market access before the IMF programme was
  secured, leaving a single viable exit path. The Domestic Debt Exchange
  Programme (DDEP) imposed haircuts on domestic small bondholders while
  the external financial picture stabilised — CB Cloud in its clearest form.

  Ghana was used as the Demo 7 Act 2 regional comparator for the Zambia
  three-scenario comparison. This fixture makes that comparator headlessly
  reproducible and adds a standalone Type A backtesting gate.

  Timeline modeled (4 biannual steps):
    2022 H1 (Step 1): Eurobond DEBT_MORATORIUM declared. FX intervention
      CEASES (cessation modeled as absence of input — no active intervention
      at Step 1, per CM advisory 2026-07-03: cessation = absence of action).
    2022 H2 (Step 2): IMF ECF programme accepted (USD 3bn). Domestic Debt
      Exchange Programme (DDEP) — modeled as FiscalPolicyInput(DEBT_ISSUANCE)
      with negative value (net reduction in domestic debt service).
      Fiscal consolidation begins: FiscalPolicyInput(SPENDING_CHANGE).
    2023 H1 (Step 3): ECF fiscal consolidation terms continue.
    2023 H2 (Step 4): Consolidation phase; reserve recovery trajectory.

  Failure modes:
    - Coffin Corner: Eurobond market access lost before IMF programme secured
    - CB Cloud: small domestic bondholders see haircuts while external creditors
      see balance sheet improvement; Q1 poverty headcount rises through
      programme period despite currency stabilisation

  Demo 7 connection: Ghana comparator used in Act 2 ZMB three-scenario
  comparison. "+342K Q1 poverty headcount under IMF terms vs +80K under
  Zambia counter-proposal" used Ghana 2023 as regional benchmark.

Simulation structure:
  build_ghana_scenario(): n_steps=4, biannual. Historical IMF ECF terms.
  build_ghana_counterfactual_scenario(): n_steps=4, biannual.
    Ghanaian government's proposed terms: domestic debt restructuring
    exempting small bondholders, slower fiscal adjustment.
    implementation_capacity=0.85 (more feasible conditionality).

  Type A fidelity target (two simultaneous directions — CB Cloud test):
    - reserve_coverage_months: improves direction at Step 3/4 (post-programme)
    - q1_poverty_headcount_ratio: continues deteriorating through programme period

  Type B counter-factual question: do Ghanaian proposed terms produce lower
  Q1 poverty headcount at the cost of slower reserve recovery?

Initial state sources (2021 baseline, pre-Eurobond access loss):
  gdp_growth             — IMF WEO April 2022 (GHA 2021 outturn: 5.4%)
  unemployment_rate      — Ghana Statistical Service LFS 2021 (13.8%)
  reserve_coverage_months — Bank of Ghana Annual Report 2021 (~3.7 months)
  sovereign_risk_premium — JP Morgan EMBI+ GHA end-2021 (~700 bps)
  fdi_stock_pct_gdp      — UNCTAD WIR 2022 (GHA: ~14.7%)
  portfolio_flow_velocity — BoG BOP 2021 (outflow ~-0.015)
  credit_rating_score    — S&P CCC+ December 2021. 21-notch: CCC+ = 16.
  q1_poverty_headcount_ratio — GSS GLSS 2021-22: ~23.4%

NOTE: GHA entity may or may not be seeded from Demo 7 setup. The test
checks that the fixture creates a valid scenario (HTTP 201 on POST) and
uses only fixture-supplied initial attributes. If GHA already has entity
attributes in the DB, the fixture's initial_attributes will supplement
or override them per the engine's entity attribute merge rules.

References: Issue #1554; CM advisory 2026-07-03.
"""
from __future__ import annotations

from datetime import date

from app.schemas import (
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScheduledInputSchema,
)


def build_ghana_scenario() -> ScenarioCreateRequest:
    """Build Ghana 2022–23 historical IMF ECF terms baseline.

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    4 biannual steps. Type A (historical baseline) and Type B (counter-factual).
    """
    initial_gdp_growth = QuantitySchema(
        value="0.054",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2022, 4, 1),
        source_registry_id="IMF_WEO_APR2022_GHA",
        measurement_framework="financial",
    )

    initial_unemployment_rate = QuantitySchema(
        value="0.138",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2021, 1, 1),
        source_registry_id="GSS_LFS_GHA_2021",
        measurement_framework="human_development",
    )

    # Bank of Ghana Annual Report 2021: ~3.7 months gross import cover
    initial_reserve_coverage_months = QuantitySchema(
        value="3.7",
        unit="months",
        variable_type="stock",
        attribute_type="stock",
        confidence_tier=1,
        observation_date=date(2021, 12, 31),
        source_registry_id="BOG_ANNUAL_GHA_2021",
        measurement_framework="financial",
    )

    # JP Morgan EMBI+ GHA end-2021: ~700 bps (Eurobond access already stressed)
    initial_sovereign_risk_premium = QuantitySchema(
        value="0.070",
        unit="ratio",
        variable_type="ratio",
        attribute_type="rate",
        confidence_tier=2,
        observation_date=date(2021, 12, 31),
        source_registry_id="JPMORGAN_EMBI_GHA_2021Q4",
        measurement_framework="financial",
    )

    # UNCTAD WIR 2022 — GHA inward FDI stock / GDP: ~14.7%
    initial_fdi_stock_pct_gdp = QuantitySchema(
        value="0.147",
        unit="ratio",
        variable_type="stock",
        attribute_type="stock",
        confidence_tier=2,
        observation_date=date(2021, 1, 1),
        source_registry_id="UNCTAD_WIR_GHA_2021",
        measurement_framework="financial",
    )

    # BoG BOP 2021: net portfolio outflow (~-1.5% GDP)
    initial_portfolio_flow_velocity = QuantitySchema(
        value="-0.015",
        unit="ratio",
        variable_type="ratio",
        attribute_type="flow",
        confidence_tier=2,
        observation_date=date(2021, 1, 1),
        source_registry_id="BOG_BOP_GHA_2021",
        measurement_framework="financial",
    )

    # S&P CCC+ December 2021 (downgraded from B- in 2021). 21-notch: CCC+ = 16.
    initial_credit_rating_score = QuantitySchema(
        value="16.0",
        unit="index_0_100",
        variable_type="stock",
        attribute_type="structural_index",
        confidence_tier=1,
        observation_date=date(2021, 12, 31),
        source_registry_id="SP_SOVEREIGN_RATINGS_GHA_2021",
        measurement_framework="financial",
    )

    # GSS GLSS 2021-22: national poverty line ~23.4% headcount
    initial_q1_poverty_headcount = QuantitySchema(
        value="0.234",
        unit="ratio",
        variable_type="ratio",
        attribute_type="rate",
        confidence_tier=2,
        observation_date=date(2021, 1, 1),
        source_registry_id="GSS_GLSS_GHA_2021",
        measurement_framework="human_development",
    )

    return ScenarioCreateRequest(
        name="Ghana 2022-23 IMF ECF Programme — Historical Baseline",
        description=(
            "Backtesting fixture for Issue #1554. "
            "Ghana 2022–23: Eurobond debt moratorium (Step 1) → IMF ECF acceptance + "
            "DDEP domestic restructuring (Step 2) → fiscal consolidation (Steps 3–4). "
            "Coffin Corner: Eurobond access lost before programme secured. "
            "CB Cloud: small bondholders bear DDEP haircut; Q1 poverty headcount rises "
            "through programme despite currency stabilisation. "
            "Demo 7 Act 2 regional comparator for ZMB three-scenario comparison. "
            "Type A: reserve improvement AND Q1 PHC deterioration simultaneous (CB Cloud). "
            "Initial state: IMF WEO April 2022 + GSS LFS 2021 + BoG 2021."
        ),
        configuration=ScenarioConfigSchema(
            entities=["GHA"],
            n_steps=4,
            timestep_label="biannual",
            start_date=date(2021, 1, 1),
            step_metadata={
                "1": {"significance": "SIGNIFICANT", "label": "Eurobond moratorium"},
                "2": {"significance": "SIGNIFICANT", "label": "IMF ECF / DDEP restructuring"},
                "3": {"significance": "SIGNIFICANT", "label": "ECF consolidation"},
                "4": {"significance": "ROUTINE", "label": "Reserve recovery"},
            },
            initial_attributes={
                "GHA": {
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
            # Step 1 (2022 H1): Eurobond debt moratorium.
            # FX intervention CEASED — cessation modeled as ABSENCE of MonetaryVolumeInput
            # (per CM advisory: cessation = no active intervention, not a new shock).
            ScheduledInputSchema(
                step=1,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "debt_moratorium",
                    "target_entity": "GHA",
                    "expected_duration": 1,
                },
            ),

            # Step 2 (2022 H2 / 2023 H1): IMF ECF acceptance + DDEP domestic restructuring.
            # DDEP: modeled as negative DEBT_ISSUANCE (net reduction in domestic debt service).
            # Fiscal consolidation begins (ECF conditionality).
            ScheduledInputSchema(
                step=2,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "imf_program_acceptance",
                    "target_entity": "GHA",
                    "expected_duration": 4,
                    "program_size_gdp_ratio": "0.09",
                    "source": "conditionality",
                    "constraining_actor_id": "IMF",
                },
            ),
            ScheduledInputSchema(
                step=2,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "debt_issuance",
                    "target_entity": "GHA",
                    "sector": "",
                    "value": "-0.06",
                    "duration_years": 1,
                },
            ),
            ScheduledInputSchema(
                step=2,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "GHA",
                    "sector": "government",
                    "value": "-0.03",
                    "duration_years": 2,
                },
            ),

            # Step 3 (2023 H1): ECF fiscal consolidation continues.
            ScheduledInputSchema(
                step=3,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "GHA",
                    "sector": "government",
                    "value": "-0.015",
                    "duration_years": 1,
                },
            ),

            # Step 4 (2023 H2): Continued consolidation; reserve recovery expected.
            ScheduledInputSchema(
                step=4,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "GHA",
                    "sector": "government",
                    "value": "-0.01",
                    "duration_years": 1,
                },
            ),
        ],
    )


def build_ghana_counterfactual_scenario() -> ScenarioCreateRequest:
    """Build Ghana counter-factual: Ghanaian proposed terms.

    Counter-factual question: does the Ghanaian government's proposed terms
    (domestic debt restructuring exempting small bondholders, slower fiscal
    adjustment) produce lower Q1 poverty headcount at the cost of slower
    reserve recovery?

    Structural differences from baseline:
    - Step 2: IMF ECF with implementation_capacity=0.85 (more feasible)
    - DDEP exempting small bondholders: approximated as smaller DEBT_ISSUANCE
      reduction (larger domestic bondholders still take haircut; small
      bondholders exempted — smaller net fiscal adjustment)
    - Steps 2–4: spending cuts at 50% of IMF baseline rate

    AC-GHA-1: Step 2 spending_change value differs from baseline (50% of rate).
    """
    base = build_ghana_scenario()

    return base.model_copy(update={
        "name": "Ghana 2022-23 Counter-Factual — Ghanaian Proposed Terms",
        "description": (
            "Counter-factual for Issue #1554. "
            "Ghanaian government's proposed terms: "
            "DDEP exempts small bondholders (smaller DEBT_ISSUANCE reduction); "
            "fiscal adjustment at 50% of IMF baseline rate; "
            "implementation_capacity=0.85 (higher per-step feasibility). "
            "Type B primary indicator: fin_composite. "
            "Direction advisory: COUNTER_FACTUAL_BETTER on Q1 PHC. "
            "Known limitation: INFERRED_STRUCTURAL (Tier 3)."
        ),
        "scheduled_inputs": [
            # Step 1: same Eurobond moratorium
            ScheduledInputSchema(
                step=1,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "debt_moratorium",
                    "target_entity": "GHA",
                    "expected_duration": 1,
                },
            ),

            # Step 2: IMF ECF (modified) + DDEP with small-bondholder exemption
            # implementation_capacity=0.85 (Ghanaian terms more politically feasible)
            ScheduledInputSchema(
                step=2,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "imf_program_acceptance",
                    "target_entity": "GHA",
                    "expected_duration": 4,
                    "program_size_gdp_ratio": "0.09",
                    "source": "conditionality",
                    "constraining_actor_id": "IMF",
                    "implementation_capacity": "0.85",
                },
            ),
            # Smaller DDEP scope (small bondholders exempted — net debt reduction smaller)
            ScheduledInputSchema(
                step=2,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "debt_issuance",
                    "target_entity": "GHA",
                    "sector": "",
                    "value": "-0.035",
                    "duration_years": 1,
                },
            ),
            # 50% of IMF baseline spending cuts
            ScheduledInputSchema(
                step=2,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "GHA",
                    "sector": "government",
                    "value": "-0.015",
                    "duration_years": 2,
                },
            ),

            # Step 3: 50% of IMF baseline consolidation
            ScheduledInputSchema(
                step=3,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "GHA",
                    "sector": "government",
                    "value": "-0.0075",
                    "duration_years": 1,
                },
            ),

            # Step 4: 50% of IMF baseline consolidation
            ScheduledInputSchema(
                step=4,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "GHA",
                    "sector": "government",
                    "value": "-0.005",
                    "duration_years": 1,
                },
            ),
        ],
    })
