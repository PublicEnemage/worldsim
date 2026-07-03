"""Sri Lanka 2021–2023 Coffin Corner crisis — scenario configuration fixture.

Historical context:
  Sri Lanka's 2022 crisis is the most complete real-world instance of all six
  WorldSim failure modes firing simultaneously:

  - The Spin: accelerating debt spiral from pandemic revenue collapse + defence
    spending commitments + tax cuts (2019 Sirisena → 2020 Rajapaksa)
  - Coffin Corner: policy options narrowed by simultaneous foreign reserve
    depletion, loss of Eurobond market access, and agricultural shock
  - Hypoxia: the organic fertiliser mandate (May 2021) was imposed under
    institutional delusion — projected export benefits contradicted available
    agronomy evidence; IMF engagement refused until reserves were critical
  - Backside of Power Curve: currency defence depleted reserves faster than
    the trade deficit compressed; the harder the CBSL defended the peg,
    the faster the reserve floor approached
  - Get-There-Itis: 26 months of warning signs (worsening EMBI spread,
    falling reserves, food price inflation) passed before IMF accepted
  - CB Cloud: the population experienced food shortages and fuel queues
    12–18 months before the government acknowledged the liquidity crisis

  Timeline modeled (5 annual steps):
    2019: Baseline (pre-tax-cut, pre-pandemic). GDP ~2.3%, reserves ~5 months.
    2020 (Step 1): Pandemic shock — revenue collapse, no IMF engagement.
    2021 (Step 2): Organic fertiliser ban — REGULATORY_CHANGE. Agricultural shock.
    2022a (Step 3): Reserve defence (EXCHANGE_RATE_INTERVENTION) + fuel subsidy
                    continuation (SPENDING_CHANGE).
    2022b (Step 4): DEBT_MORATORIUM (April 2022) + DEFAULT_DECLARATION.
    2023 (Step 5): IMF SBA acceptance (USD 3bn, 48-month programme).

Simulation structure:
  build_sri_lanka_scenario(): n_steps=5, annual. Historical baseline.
    Initial state: 2019 (pre-crisis). Steps 1–5 reproduce the crisis arc.

  build_sri_lanka_counterfactual_scenario(): n_steps=5, annual.
    Counter-factual: fertiliser ban reversed at step 2 (no agricultural shock);
    IMF programme accepted one step earlier at step 3 instead of step 5.
    Reserve trajectory and Q1 poverty headcount are the primary Type B signals.

Initial state sources (2019 baseline):
  gdp_growth             — IMF WEO April 2020 (LKA 2019 outturn: 2.3%)
  unemployment_rate      — Department of Census & Statistics LFS 2019 (4.8%)
  sovereign_risk_premium — JP Morgan EMBI+ LKA end-2019 (~90 bps)
  fdi_stock_pct_gdp      — UNCTAD World Investment Report 2020 (LKA: ~7.3%)
  portfolio_flow_velocity — CBSL Annual Report 2019 (modest outflow ~-0.003)
  credit_rating_score    — S&P B+ end-2019, 21-notch scale index ~29
  reserve_coverage_months — CBSL Annual Report 2019 (~5.0 months)

References: Issue #1549; CM advisory 2026-07-03.
"""
from __future__ import annotations

from datetime import date

from app.schemas import (
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScheduledInputSchema,
)


def build_sri_lanka_scenario() -> ScenarioCreateRequest:
    """Build the Sri Lanka 2021–2023 Coffin Corner historical baseline.

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    5 annual steps from 2019 initial state through 2023 IMF SBA.
    All six WorldSim failure modes fire across steps 2–4.
    """
    initial_gdp_growth = QuantitySchema(
        value="0.023",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2020, 4, 1),
        source_registry_id="IMF_WEO_APR2020_LKA",
        measurement_framework="financial",
    )

    initial_unemployment_rate = QuantitySchema(
        value="0.048",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2019, 1, 1),
        source_registry_id="DCS_LFS_LKA_2019",
        measurement_framework="human_development",
    )

    # CBSL: reserves at 5.0 months import cover end-2019 (pre-crisis)
    initial_reserve_coverage_months = QuantitySchema(
        value="5.0",
        unit="months",
        variable_type="stock",
        attribute_type="stock",
        confidence_tier=1,
        observation_date=date(2019, 12, 31),
        source_registry_id="CBSL_ANNUAL_LKA_2019",
        measurement_framework="financial",
    )

    # JP Morgan EMBI+ LKA end-2019: ~90 bps (pre-Eurobond access loss)
    initial_sovereign_risk_premium = QuantitySchema(
        value="0.009",
        unit="ratio",
        variable_type="ratio",
        attribute_type="rate",
        confidence_tier=2,
        observation_date=date(2019, 12, 31),
        source_registry_id="JPMORGAN_EMBI_LKA_2019",
        measurement_framework="financial",
    )

    # UNCTAD WIR 2020 — LKA inward FDI stock / GDP: ~7.3%
    initial_fdi_stock_pct_gdp = QuantitySchema(
        value="0.073",
        unit="ratio",
        variable_type="stock",
        attribute_type="stock",
        confidence_tier=2,
        observation_date=date(2019, 1, 1),
        source_registry_id="UNCTAD_WIR_LKA_2019",
        measurement_framework="financial",
    )

    # CBSL BOP 2019 — modest net portfolio outflow (~-0.3% GDP)
    initial_portfolio_flow_velocity = QuantitySchema(
        value="-0.003",
        unit="ratio",
        variable_type="ratio",
        attribute_type="flow",
        confidence_tier=2,
        observation_date=date(2019, 1, 1),
        source_registry_id="CBSL_BOP_LKA_2019",
        measurement_framework="financial",
    )

    # S&P B+ end-2019. 21-notch linear 0–100 scale: B+ = 29.
    initial_credit_rating_score = QuantitySchema(
        value="29.0",
        unit="index_0_100",
        variable_type="stock",
        attribute_type="structural_index",
        confidence_tier=1,
        observation_date=date(2019, 12, 31),
        source_registry_id="SP_SOVEREIGN_RATINGS_LKA_2019",
        measurement_framework="financial",
    )

    return ScenarioCreateRequest(
        name="Sri Lanka 2021-2023 Coffin Corner — All-Six-Failure-Modes Baseline",
        description=(
            "Backtesting fixture for Issue #1549. "
            "Historical arc: pandemic revenue collapse (2020) → organic fertiliser ban (2021) "
            "→ reserve defence and fuel subsidy continuation (2022a) "
            "→ debt moratorium and default (2022b) → IMF SBA (2023). "
            "All six WorldSim failure modes active across steps 2–4. "
            "Type A fidelity target: DIRECTION_ONLY on reserve depletion and Q1 poverty headcount. "
            "Initial state: IMF WEO April 2020 + DCS LFS 2019 + CBSL 2019."
        ),
        configuration=ScenarioConfigSchema(
            entities=["LKA"],
            n_steps=5,
            timestep_label="annual",
            start_date=date(2019, 1, 1),
            step_metadata={
                "1": {"significance": "SIGNIFICANT", "label": "Pandemic shock / revenue collapse"},
                "2": {"significance": "SIGNIFICANT", "label": "Organic fertiliser ban"},
                "3": {"significance": "SIGNIFICANT", "label": "Reserve defence / fuel subsidy"},
                "4": {"significance": "SIGNIFICANT", "label": "Debt moratorium / default"},
                "5": {"significance": "SIGNIFICANT", "label": "IMF SBA acceptance"},
            },
            initial_attributes={
                "LKA": {
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
            # Step 1 (2020): No active policy shock; pandemic is an exogenous GDP shock
            # modeled through the initial GDP growth being negative in 2020.
            # No scheduled_inputs at step 1 — endogenous propagation from initial state.

            # Step 2 (2021): Organic fertiliser mandate — REGULATORY_CHANGE.
            # PM Rajapaksa banned synthetic fertilisers overnight (April 2021).
            # Agricultural output collapsed ~40% in short-season crops (rice, tea).
            # This fires Hypoxia (institutional delusion) and begins Coffin Corner narrowing.
            ScheduledInputSchema(
                step=2,
                input_type="StructuralPolicyInput",
                input_data={
                    "instrument": "regulatory_change",
                    "target_entity": "LKA",
                    "affected_sector": "agriculture",
                    "implementation_years": 1,
                },
            ),

            # Step 3 (2022a): CBSL FX intervention defending LKR peg (Backside of Power Curve).
            # Reserves depleted by ~$2.5bn defending the 200 LKR/USD rate.
            # Fuel subsidies maintained despite forex constraint (Get-There-Itis).
            ScheduledInputSchema(
                step=3,
                input_type="MonetaryVolumeInput",
                input_data={
                    "instrument": "exchange_rate_intervention",
                    "target_entity": "LKA",
                    "value": "-0.15",
                    "unit": "ratio",
                    "currency_code": "LKR",
                    "price_basis": "nominal",
                    "exchange_rate_type": "official",
                },
            ),
            ScheduledInputSchema(
                step=3,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "LKA",
                    "sector": "government",
                    "value": "0.015",
                    "duration_years": 1,
                },
            ),

            # Step 4 (2022b): Debt moratorium (April 2022, USD 7.1bn suspended)
            # then formal default declaration (May 2022, first-ever default).
            ScheduledInputSchema(
                step=4,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "debt_moratorium",
                    "target_entity": "LKA",
                    "expected_duration": 1,
                },
            ),
            ScheduledInputSchema(
                step=4,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "default_declaration",
                    "target_entity": "LKA",
                    "expected_duration": 1,
                },
            ),

            # Step 5 (2023): IMF SBA — USD 3bn, 48-month programme (approved March 2023).
            ScheduledInputSchema(
                step=5,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "imf_program_acceptance",
                    "target_entity": "LKA",
                    "expected_duration": 4,
                    "program_size_gdp_ratio": "0.09",
                },
            ),
        ],
    )


def build_sri_lanka_counterfactual_scenario() -> ScenarioCreateRequest:
    """Build the Sri Lanka counter-factual: fertiliser ban reversed, earlier IMF.

    Counter-factual question: if the organic fertiliser ban had been reversed at
    Step 2 (2021), and if the IMF programme had been accepted one step earlier
    (Step 3 = 2022a) before reserves fell to critical levels, what would the
    reserve trajectory and Q1 poverty headcount trajectory have been?

    Structural differences from baseline:
    - Step 2: NO organic fertiliser regulatory_change (ban not imposed)
    - Step 3: IMF_PROGRAM_ACCEPTANCE (earlier engagement) replaces reserve defence
    - Steps 4–5: Fiscal consolidation under IMF; no default

    AC-LKA-1 check: Step 2 counter-factual has no REGULATORY_CHANGE input
    (baseline Step 2 has agricultural shock; counter-factual does not).
    """
    base = build_sri_lanka_scenario()

    return base.model_copy(update={
        "name": "Sri Lanka 2021-2023 Counter-Factual — Earlier IMF, No Fertiliser Ban",
        "description": (
            "Counter-factual for Issue #1549. "
            "Organic fertiliser ban NOT imposed at Step 2 (agricultural channel preserved). "
            "IMF SBA accepted at Step 3 (2022a) before reserve depletion becomes binding. "
            "Type B primary indicator: fin_composite. "
            "Direction verdict advisory: COUNTER_FACTUAL_BETTER on reserve trajectory. "
            "Known limitation: INFERRED_STRUCTURAL (Tier 3) — this policy path was not executed."
        ),
        "scheduled_inputs": [
            # Step 1 (2020): same pandemic shock (no inputs — endogenous propagation)

            # Step 2 (2021): NO fertiliser ban — baseline Step 2 REGULATORY_CHANGE omitted.
            # Counter-factual: government reverses course, keeps chemical fertiliser imports.

            # Step 3 (2022a): Earlier IMF acceptance — before reserve floor is breached.
            # USD 2.5bn (8% GDP) programme negotiated under less severe conditions.
            ScheduledInputSchema(
                step=3,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "imf_program_acceptance",
                    "target_entity": "LKA",
                    "expected_duration": 4,
                    "program_size_gdp_ratio": "0.08",
                },
            ),
            ScheduledInputSchema(
                step=3,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "LKA",
                    "sector": "government",
                    "value": "-0.02",
                    "duration_years": 2,
                },
            ),

            # Step 4 (2022b): IMF programme fiscal consolidation — no default.
            ScheduledInputSchema(
                step=4,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "deficit_target",
                    "target_entity": "LKA",
                    "sector": "",
                    "value": "-0.04",
                    "duration_years": 2,
                },
            ),

            # Step 5 (2023): Recovery consolidation phase — no new shock inputs.
        ],
    })
