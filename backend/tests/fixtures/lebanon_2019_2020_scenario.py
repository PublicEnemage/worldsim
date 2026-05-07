"""Lebanon 2019–2020 financial collapse — scenario configuration fixture.

Historical context:
  Lebanon's financial crisis of 2019–2020 was one of the most severe economic
  collapses in modern history. The crisis had deep structural roots:

  The Banque du Liban (BdL) circular economy — Lebanese commercial banks
  attracted USD dollar deposits with above-market interest rates and placed
  those deposits at BdL, which used them to finance the government's chronic
  fiscal deficit (~10% of GDP annually). By 2019, this Ponzi-like structure
  was exhausted: USD deposit inflows reversed, BdL's net foreign assets
  turned negative, and the banking system became technically insolvent.

  October 2019: Mass protests erupted (the "October 17 revolution") triggered
  by proposed taxes on WhatsApp calls. Prime Minister Saad Hariri resigned
  two weeks later. Banks informally imposed deposit withdrawal restrictions
  (the "bank deposit freeze" — capital controls applied de facto before
  being formalized).

  March 2020: Lebanon formally defaulted on its $1.2bn Eurobond maturity —
  the first Lebanese sovereign default in history. The government announced
  a debt moratorium covering $31bn in Eurobonds.

  August 2020: The Beirut port explosion (August 4, 2020) devastated Lebanon's
  primary import gateway, killed over 200 people, and delivered an additional
  economic shock to an already collapsing economy. Estimated damage: $3.8–4.6bn
  (World Bank), representing approximately 20–25% of 2019 GDP.

Simulation structure:
  n_steps=2 (annual); step 1 = 2019, step 2 = 2020.
  Initial state reflects Lebanon's early-2019 deteriorating baseline
  (pre-October protest onset; fiscal and financial stress already measurable).

  Note on initial GDP seed: IMF WEO tracking data for early-2019 Lebanon
  showed GDP growth already trending negative before the October bank run.
  The initial gdp_growth of -2.0% represents this pre-protest deterioration
  trajectory. The full-year 2019 outturn of -6.9% (IMF WEO April 2020)
  reflects both the pre-protest slowdown and the October crisis impact.

Scheduled inputs:
  Step 1 (2019): Bank deposit freeze (capital controls imposition) +
                 Fiscal spending collapse (government austerity under liquidity crisis)
  Step 2 (2020): Sovereign debt moratorium declaration

  Note on port explosion: The Beirut port explosion (August 2020) is not
  modeled as a separate step-2 fiscal input because in the n_steps=2 annual
  framework, step 2 already captures the compound 2020 crisis including the
  port explosion's economic impact. A three-step variant (Issue #142 pattern)
  would enable modeling the port explosion as a discrete additional shock.

Initial state sources:
  gdp_growth        — IMF WEO April 2020, early-2019 tracking estimate (-2.0%
                      annualised, pre-protest; full-year outturn -6.9%)
  unemployment_rate — World Bank WDI 2019 vintage (ILO-modelled, 11.4%)

References: Issue #207.

CASCADE dynamics note:
  Lebanon exemplifies the CASCADE propagation failure mode: banking system
  insolvency → currency peg collapse → real economy contraction → social
  fabric breakdown. Each domain's failure accelerated the others. The M6
  simulation captures the macro-fiscal channel (steps 1→2 via
  MacroeconomicModule) but not the full cascade. Future validation against
  the CASCADE propagation mode (#29) is tracked in the test file.
"""
from __future__ import annotations

from datetime import date

from app.schemas import (
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScheduledInputSchema,
)


def build_lebanon_scenario() -> ScenarioCreateRequest:
    """Build the Lebanon 2019–2020 backtesting scenario configuration.

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    The scenario runs 2 steps (annual: 2019→2020→2021 projection window)
    starting from Lebanon's early-2019 deteriorating economic conditions.

    Scheduled inputs represent the dominant crisis events:
      Step 1: Bank deposit freeze (capital controls) + fiscal spending collapse
      Step 2: Sovereign debt moratorium (March 2020 Eurobond default)

    Initial state attributes:
      gdp_growth        = -2.0%  (IMF WEO April 2020, early-2019 tracking)
      unemployment_rate = 11.4%  (World Bank WDI 2019 vintage, ILO-modelled)
    """
    # IMF WEO April 2020 — Lebanon early-2019 annualised growth tracking: -2.0%
    # (pre-October protest; full-year 2019 outturn -6.9% reflects crisis onset)
    initial_gdp_growth = QuantitySchema(
        value="-0.020",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=3,
        observation_date=date(2020, 4, 1),
        source_registry_id="IMF_WEO_APR2020",
        measurement_framework="financial",
    )

    # World Bank WDI 2019 vintage — ILO-modelled unemployment estimate: 11.4%
    initial_unemployment_rate = QuantitySchema(
        value="0.114",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2020, 1, 1),
        source_registry_id="WDI_LBN_2019",
        measurement_framework="human_development",
    )

    return ScenarioCreateRequest(
        name="Lebanon 2019-2020 Financial Collapse Backtesting Fixture",
        description=(
            "Backtesting fixture for Issue #207. "
            "Reproduces the Lebanon 2019–2020 financial crisis — bank deposit freeze, "
            "fiscal collapse, and sovereign default — to validate DIRECTION_ONLY GDP "
            "contraction thresholds. "
            "Initial state: IMF WEO April 2020 early-2019 tracking + WDI 2019. "
            "CASCADE dynamics (banking → currency → real economy) partially modeled; "
            "full cascade validation deferred to Issue #29."
        ),
        configuration=ScenarioConfigSchema(
            entities=["LBN"],
            n_steps=2,
            timestep_label="annual",
            initial_attributes={
                "LBN": {
                    "gdp_growth": initial_gdp_growth,
                    "unemployment_rate": initial_unemployment_rate,
                },
            },
        ),
        scheduled_inputs=[
            # Step 1 (2019): Bank deposit freeze — informal capital controls imposed
            # by Lebanese commercial banks from October 2019 onward. Banks restricted
            # USD withdrawals to ~$200-$400/week informally before formal restrictions.
            # Instrument: CAPITAL_CONTROLS (EmergencyInstrument).
            ScheduledInputSchema(
                step=1,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "capital_controls",
                    "target_entity": "LBN",
                    "expected_duration": 2,
                },
            ),
            # Step 1 (2019): Fiscal spending collapse — government expenditure
            # compression under acute USD liquidity shortage. Lebanon's fiscal
            # deficit (~10% of GDP) became unfinanceable as USD inflows reversed.
            # Value: -0.10 (10% of GDP spending reduction — structural fiscal
            # collapse, not discretionary austerity).
            ScheduledInputSchema(
                step=1,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "LBN",
                    "sector": "government",
                    "value": "-0.10",
                    "duration_years": 1,
                },
            ),
            # Step 2 (2020): Sovereign debt moratorium — Lebanon declared default
            # on $1.2bn Eurobond maturity on March 9, 2020 (first sovereign default
            # in Lebanese history). Full Eurobond stock: $31bn (approximately 170%
            # of pre-crisis GDP). The Beirut port explosion (August 4, 2020)
            # compounded the 2020 collapse; modeled within this step's compound shock.
            ScheduledInputSchema(
                step=2,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "debt_moratorium",
                    "target_entity": "LBN",
                    "expected_duration": 1,
                },
            ),
        ],
    )
