"""Argentina 2001–2002 currency and debt crisis — scenario configuration fixture.

Historical context:
  Argentina's convertibility system (ARS pegged 1:1 to USD since 1991) came under
  sustained pressure from a 1999 recession, chronic current account deficits, and
  a rising external debt burden. Key events modeled:

  2001: Zero Deficit Plan (Plan Déficit Cero, July 2001) — Finance Minister Cavallo
        imposed strict pro-cyclical fiscal adjustment, cutting federal spending ~6.5%
        of GDP. The IMF Blindaje (USD 39.7bn, December 2000) was extended and
        augmented (USD 8bn, June 2001) but failed to restore market confidence.

  2002: Sovereign default (declared December 2001 — USD 81.8bn, the largest default
        in history at the time). Pesification and devaluation (January 2002) ended
        the convertibility era.

Simulation structure:
  n_steps=2 (annual); step 1 = 2001, step 2 = 2002.
  Initial state reflects Argentina's 2000 economic baseline (recession onset).

Scheduled inputs:
  Step 1: IMF program acceptance (Blindaje) + fiscal spending cut (Zero Deficit Plan)
  Step 2: Default declaration

Initial state sources:
  gdp_growth        — IMF WEO April 2001 (2000 outturn: -0.8%)
  unemployment_rate — INDEC EPH October 2000 wave (14.7%)

References: Issue #192; ARCH-REVIEW-004 second-case recommendation.
"""
from __future__ import annotations

from datetime import date

from app.schemas import (
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScheduledInputSchema,
)


def build_argentina_scenario() -> ScenarioCreateRequest:
    """Build the Argentina 2001–2002 backtesting scenario configuration.

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    The scenario runs 2 steps (annual: 2001→2002→2003 projection window)
    starting from Argentina's 2000 economic conditions.

    Scheduled inputs represent the two dominant policy shocks:
      Step 1: IMF Blindaje continuation + Zero Deficit Plan spending cut
      Step 2: Sovereign default declaration

    Initial state attributes:
      gdp_growth        = -0.8%  (IMF WEO April 2001, 2000 outturn)
      unemployment_rate = 14.7% (INDEC EPH October 2000 wave)
    """
    # IMF WEO April 2001 — Argentina 2000 real GDP growth outturn: -0.79%
    initial_gdp_growth = QuantitySchema(
        value="-0.008",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2001, 4, 1),
        source_registry_id="IMF_WEO_APR2001",
        measurement_framework="financial",
    )

    # INDEC EPH October 2000 semi-annual wave — 14.7% unemployment
    initial_unemployment_rate = QuantitySchema(
        value="0.147",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2001, 1, 1),
        source_registry_id="INDEC_EPH_2000",
        measurement_framework="human_development",
    )

    return ScenarioCreateRequest(
        name="Argentina 2001-2002 Currency and Debt Crisis Backtesting Fixture",
        description=(
            "Backtesting fixture for Issue #192. "
            "Reproduces the Argentina 2001–2002 sovereign default and convertibility "
            "collapse to validate DIRECTION_ONLY GDP contraction thresholds. "
            "Initial state: IMF WEO April 2001 + INDEC EPH October 2000."
        ),
        configuration=ScenarioConfigSchema(
            entities=["ARG"],
            n_steps=2,
            timestep_label="annual",
            initial_attributes={
                "ARG": {
                    "gdp_growth": initial_gdp_growth,
                    "unemployment_rate": initial_unemployment_rate,
                },
            },
        ),
        scheduled_inputs=[
            # Step 1 (2001): IMF Blindaje — extended credit facility, augmented June 2001.
            # Program size ~16% of GDP (USD 39.7bn on ~USD 250bn GDP).
            ScheduledInputSchema(
                step=1,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "imf_program_acceptance",
                    "target_entity": "ARG",
                    "expected_duration": 2,
                    "program_size_gdp_ratio": "0.16",
                },
            ),
            # Step 1 (2001): Zero Deficit Plan — pro-cyclical spending cut ~6.5% of GDP.
            # Announced July 2001 under Finance Minister Domingo Cavallo.
            ScheduledInputSchema(
                step=1,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "ARG",
                    "sector": "government",
                    "value": "-0.065",
                    "duration_years": 1,
                },
            ),
            # Step 2 (2002): Default declaration — December 2001, USD 81.8bn.
            # Largest sovereign default in history at the time.
            ScheduledInputSchema(
                step=2,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "default_declaration",
                    "target_entity": "ARG",
                    "expected_duration": 1,
                },
            ),
        ],
    )
