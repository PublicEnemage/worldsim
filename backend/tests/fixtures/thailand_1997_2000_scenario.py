"""Thailand 1997–2000 Asian financial crisis — scenario configuration fixture.

Historical context:
  Thailand's 1997 crisis was the epicentre of the Asian financial contagion
  that spread to South Korea, Indonesia, Malaysia, and beyond. Its roots lay in
  a decade of fixed exchange rate policy (THB pegged to a USD-dominated basket),
  which attracted large capital inflows and encouraged USD-denominated borrowing
  by Thai corporates and financial institutions. By 1996, Thailand's current
  account deficit reached 8% of GDP and its financial sector was heavily exposed
  to a collapsing property bubble.

  July 2, 1997 — Peg abandonment: After exhausting USD 28bn of reserves
  defending the peg against speculative attacks (most notably from macro hedge
  funds), the Bank of Thailand announced a managed float of the baht. The baht
  immediately lost approximately 15–20% of its value against the USD, with
  further depreciation to 56 THB/USD by January 1998 (from 26 THB/USD at peg).
  Capital controls were imposed on offshore baht lending markets.

  August 1997 — IMF program acceptance: Thailand agreed to a USD 17.2bn
  IMF-led bailout package (IMF USD 4bn + bilateral contributions from Japan,
  Singapore, Malaysia, and others). The program required fiscal adjustment
  (initial target: surplus of 1% of GDP), high interest rates to defend the
  float, and financial sector restructuring (56 finance companies suspended,
  ultimately 58 closed). The conditionality proved pro-cyclical: austerity
  deepened the recession even as the currency continued to depreciate.

  1998 — Cascade and deepening: The 1998 contraction (-10.5%) reflected:
  corporate balance-sheet recession (USD-denominated debt became unpayable
  after baht depreciation), banking system stress (non-performing loans
  reached ~47% of total loans by 1999), demand collapse, and regional
  contagion amplifying all channels simultaneously.

Simulation structure:
  n_steps=2 (annual); step 1 = 1997, step 2 = 1998.
  Initial state reflects Thailand's early-1997 deteriorating conditions
  (property bubble deflating, capital flow reversal underway, before the
  July 2 peg abandonment).

  Note on initial GDP seed: IMF WEO April 1998 tracking data for Thailand
  showed GDP already trending negative in H1 1997 as the property and
  financial sector stress became acute. The initial gdp_growth of -1.0%
  represents this pre-abandonment deterioration trajectory. The full-year
  1997 outturn of -1.4% (IMF WEO October 1998) includes the July crisis impact.

Scheduled inputs:
  Step 1 (1997): Currency peg abandonment (capital controls on offshore
                 baht market) + fiscal tightening (pre-program austerity)
  Step 2 (1998): IMF program acceptance (August 1997 USD 17.2bn package,
                 processed at step 2 per one-step lag design)

  Note on mechanism: the fiscal tightening at step 1 is processed by
  MacroeconomicModule at step 2 (one-step lag), generating a large negative
  gdp_growth_change delta that drives the 1998 contraction. The IMF program
  acceptance at step 2 also appears in the step 2 event queue.

Initial state sources:
  gdp_growth        — IMF WEO April 1998, early-1997 tracking estimate (-1.0%
                      annualised, pre-abandonment; full-year outturn -1.4%)
  unemployment_rate — World Bank WDI 1997 vintage (ILO-modelled, 1.5%)

References: Issue #141.

CASCADE dynamics note:
  Thailand 1997 exemplifies the herding and contagion CASCADE failure mode:
  speculative currency attack (coordinated market action) → peg abandonment →
  banking system stress → corporate balance-sheet recession → regional contagion
  (Korea, Indonesia, Malaysia). The M6 simulation captures the macro-fiscal
  channel but not the contagion dynamics. Full cascade validation is deferred
  to Issue #29 (CASCADE propagation mode).
"""
from __future__ import annotations

from datetime import date

from app.schemas import (
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScheduledInputSchema,
)


def build_thailand_scenario() -> ScenarioCreateRequest:
    """Build the Thailand 1997–2000 backtesting scenario configuration.

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    The scenario runs 2 steps (annual: 1997→1998→1999 projection window)
    starting from Thailand's early-1997 deteriorating economic conditions.

    Scheduled inputs represent the dominant crisis events:
      Step 1: Peg abandonment (capital controls) + fiscal tightening
      Step 2: IMF program acceptance (USD 17.2bn, August 1997)

    Initial state attributes:
      gdp_growth        = -1.0%  (IMF WEO April 1998, early-1997 tracking)
      unemployment_rate =  1.5%  (World Bank WDI 1997 vintage, ILO-modelled)
    """
    # IMF WEO April 1998 — Thailand early-1997 annualised growth tracking: -1.0%
    # (pre-peg-abandonment; full-year 1997 outturn -1.4% reflects July crisis)
    initial_gdp_growth = QuantitySchema(
        value="-0.010",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=3,
        observation_date=date(1998, 4, 1),
        source_registry_id="IMF_WEO_APR1998",
        measurement_framework="financial",
    )

    # World Bank WDI 1997 vintage — ILO-modelled unemployment estimate: 1.5%
    # (structurally low due to agricultural sector absorption of displaced workers)
    initial_unemployment_rate = QuantitySchema(
        value="0.015",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(1998, 1, 1),
        source_registry_id="WDI_THA_1997",
        measurement_framework="human_development",
    )

    return ScenarioCreateRequest(
        name="Thailand 1997-2000 Asian Financial Crisis Backtesting Fixture",
        description=(
            "Backtesting fixture for Issue #141. "
            "Reproduces the Thailand 1997–2000 Asian financial crisis — currency "
            "peg abandonment, fiscal tightening, and IMF program acceptance — to "
            "validate DIRECTION_ONLY GDP contraction thresholds. "
            "Initial state: IMF WEO April 1998 early-1997 tracking + WDI 1997. "
            "CASCADE contagion dynamics (regional spillover to Korea, Indonesia, "
            "Malaysia) partially modeled; full cascade validation deferred to Issue #29."
        ),
        configuration=ScenarioConfigSchema(
            entities=["THA"],
            n_steps=2,
            timestep_label="annual",
            initial_attributes={
                "THA": {
                    "gdp_growth": initial_gdp_growth,
                    "unemployment_rate": initial_unemployment_rate,
                },
            },
        ),
        scheduled_inputs=[
            # Step 1 (1997): Currency peg abandonment — Bank of Thailand floated
            # the baht on July 2, 1997, after exhausting USD 28bn of reserves
            # defending the peg against speculative attacks. Capital controls were
            # simultaneously imposed on the offshore baht lending market.
            # Instrument: CAPITAL_CONTROLS (EmergencyInstrument) — models the
            # capital flow restrictions accompanying the float.
            ScheduledInputSchema(
                step=1,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "capital_controls",
                    "target_entity": "THA",
                    "expected_duration": 1,
                },
            ),
            # Step 1 (1997): Fiscal tightening — Thailand began pro-cyclical
            # fiscal adjustment before the IMF program was formally agreed.
            # Pre-program target: primary surplus of 1% of GDP (later revised
            # to 3% surplus under IMF conditionality). Modeled as a spending cut
            # of -6% of GDP representing the combined pre-program and program-year
            # fiscal adjustment.
            ScheduledInputSchema(
                step=1,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "THA",
                    "sector": "government",
                    "value": "-0.06",
                    "duration_years": 1,
                },
            ),
            # Step 2 (1998): IMF program acceptance — Thailand agreed to a
            # USD 17.2bn multilateral bailout (IMF USD 4bn; balance from Japan,
            # Singapore, Malaysia, World Bank, ADB) in August 1997. Program
            # conditionality included high interest rates, fiscal austerity,
            # and closure of insolvent finance companies (56 suspended; 58 closed).
            # Per one-step lag design, the step 1 fiscal shock is processed at
            # step 2 by MacroeconomicModule; the IMF acceptance event is also
            # present in the step 2 prior-events queue.
            ScheduledInputSchema(
                step=2,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "imf_program_acceptance",
                    "target_entity": "THA",
                    "expected_duration": 3,
                    "program_size_gdp_ratio": "0.22",
                },
            ),
        ],
    )
