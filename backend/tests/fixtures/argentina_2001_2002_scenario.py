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

  2003–2004: Kirchner recovery — GDP rebounded strongly (8.8% in 2003, 9.0% in 2004)
             under heterodox policies: debt restructuring, export tax revenue, peso
             undervaluation, and suppression of utility tariffs.

Simulation structure:
  build_argentina_scenario(): n_steps=2 (annual); step 1 = 2001, step 2 = 2002.
    Backtesting fixture. Initial state reflects Argentina's 2000 baseline.

  build_argentina_demo_scenario(): n_steps=4 (annual: 2001→2004).
    Demo 3 variant. Extends the base with EcologicalModule, GovernanceModule,
    step_metadata event labels, recovery-phase steps, and an emergency_declaration
    at step 2 (state of siege, December 19 2001 — concurrent with sovereign default).
    The emergency_declaration drives democratic_quality_score below the 0.70 MDA
    floor at step 3, producing a governance WARNING during the Kirchner recovery
    period (Issue #553, #615).

Scheduled inputs:
  Step 1: IMF program acceptance (Blindaje) + fiscal spending cut (Zero Deficit Plan)
  Step 2: Default declaration
  Step 3 (demo only): Recovery — no active shock; ROUTINE step
  Step 4 (demo only): Consolidation — no active shock; ROUTINE step

Initial state sources:
  gdp_growth        — IMF WEO April 2001 (2000 outturn: -0.8%)
  unemployment_rate — INDEC EPH October 2000 wave (14.7%)

References: Issue #192; Issue #553; ARCH-REVIEW-004 second-case recommendation.
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


def build_argentina_demo_scenario() -> ScenarioCreateRequest:
    """Build the Argentina 2001–2002 Demo 3 scenario with all four Zone 1 axes live.

    Extends build_argentina_scenario() with:
      - n_steps=4 (crisis arc through 2004 recovery)
      - modules_config enabling EcologicalModule and GovernanceModule
      - co2_concentration_ppm initial seed (369.5 ppm — NOAA Mauna Loa 2000 mean)
      - rule_of_law_percentile initial seed (33.2 — WGI Rule of Law ARG 2000)
      - democratic_quality_score initial seed (0.71 — V-Dem LDI ARG 2000)
      - step_metadata with SIGNIFICANT labels for crisis steps 1–3
      - emergency_declaration at step 2 (state of siege, December 19 2001)

    Composite score status (M10):
      Ecological      — live (boundary proximity; CO2 active)
      Governance      — live (normalized_absolute; LDI + rule of law percentile)
      Financial       — null (single-entity guard, Issue #193)
      Human Dev       — null (single-entity guard, Issue #193)

    Step arc:
      Step 1 (2001): Zero Deficit Plan + IMF Blindaje (SIGNIFICANT)
      Step 2 (2002): Default declaration / Peso devaluation (SIGNIFICANT)
      Step 3 (2003): Kirchner recovery begins (SIGNIFICANT)
      Step 4 (2004): Growth consolidation (ROUTINE)

    References: Issue #553 (Demo 3); build_greece_demo_scenario() (pattern reference).
    """
    base = build_argentina_scenario()

    # NOAA Mauna Loa Observatory 2000 annual mean: 369.5 ppm (confidence_tier=1).
    initial_co2_concentration = QuantitySchema(
        value="369.5",
        unit="ppm",
        variable_type="stock",
        confidence_tier=1,
        observation_date=date(2000, 1, 1),
        source_registry_id="NOAA_MLO_2000",
        measurement_framework="ecological",
    )

    # World Bank WGI 2000 — Rule of Law Percentile Rank for Argentina: 33.2.
    # Argentina's rule of law stood at the 33rd percentile in 2000, already under
    # stress from institutional gridlock and provincial fiscal crises.
    # Confidence tier 2 (official multilateral statistics, annual survey).
    initial_rule_of_law = QuantitySchema(
        value="33.2",
        unit="percentile_0_100",
        variable_type="stock",
        confidence_tier=2,
        observation_date=date(2000, 1, 1),
        source_registry_id="WB_WGI_ARG_2000_RULE_OF_LAW",
        measurement_framework="governance",
    )

    # V-Dem v13 Liberal Democracy Index for Argentina 2000: 0.71.
    # Argentina was a functioning democracy pre-crisis. The LDI will decline
    # through steps 1–2 under emergency conditions (state of siege, five
    # presidents in ten days, social unrest).
    # Confidence tier 3 (expert-coded survey).
    initial_democratic_quality = QuantitySchema(
        value="0.71",
        unit="ratio_0_1",
        variable_type="stock",
        confidence_tier=3,
        observation_date=date(2000, 1, 1),
        source_registry_id="VDEM_V13_ARG_2000_LDI",
        measurement_framework="governance",
    )

    updated_arg_attrs = {
        **base.configuration.initial_attributes.get("ARG", {}),
        "co2_concentration_ppm": initial_co2_concentration,
        "rule_of_law_percentile": initial_rule_of_law,
        "democratic_quality_score": initial_democratic_quality,
    }

    # step_metadata: 1-based string keys → significance + label.
    # Steps 1, 2, and 3 are SIGNIFICANT (major crisis events and recovery onset).
    # Step 4 (2004 consolidation) is ROUTINE.
    # Labels are truncated to ≤32 chars per the trajectory endpoint contract.
    step_metadata = {
        "1": {"significance": "SIGNIFICANT", "label": "Zero Deficit Plan / Blindaje"},
        "2": {"significance": "SIGNIFICANT", "label": "Default / Peso devaluation"},
        "3": {"significance": "SIGNIFICANT", "label": "Kirchner recovery begins"},
    }

    demo_config = base.configuration.model_copy(
        update={
            "n_steps": 4,
            "start_date": date(2000, 1, 1),
            "modules_config": {
                "ecological": {"enabled": True},
                "governance": {"enabled": True},
            },
            "initial_attributes": {"ARG": updated_arg_attrs},
            "step_metadata": step_metadata,
        }
    )

    # Add emergency_declaration at step 2: Argentina's state of siege was declared
    # December 19, 2001 — the same step as the sovereign default. GovernanceModule
    # applies a one-step lag, so this event is processed at step 3. The elasticity
    # is -0.05 on democratic_quality_score (Bermeo 2016). Starting at 0.715 after
    # the imf_program_acceptance effect (+0.005 at step 2), the score drops to
    # 0.665 at step 3 — below the MDA-GOV-DEMOCRACY-FLOOR threshold of 0.70.
    # MDA WARNING fires at step 3 (the Kirchner recovery), showing that governance
    # damage persists even as the economy begins to recover.
    demo_scheduled_inputs = list(base.scheduled_inputs) + [
        ScheduledInputSchema(
            step=2,
            input_type="EmergencyPolicyInput",
            input_data={
                "instrument": "emergency_declaration",
                "target_entity": "ARG",
                "expected_duration": 1,
            },
        ),
    ]

    return base.model_copy(update={
        "name": "Argentina 2001-2002 Demo 3 — Crisis Arc and Kirchner Recovery",
        "description": (
            "Demo 3 scenario (Issue #553). "
            "EcologicalModule and GovernanceModule enabled — all four framework axes live. "
            "Crisis arc: Zero Deficit Plan (2001) → sovereign default + state of siege (2002) → "
            "Kirchner recovery (2003–2004). "
            "Governance composite uses normalized_absolute strategy "
            "(WGI/V-Dem; ADR-005 Amendment 4). "
            "MDA-GOV-DEMOCRACY-FLOOR breached at step 3: emergency_declaration (step 2) "
            "drives democratic_quality_score to 0.665 via GovernanceModule one-step lag. "
            "Financial and human_development composites are null "
            "(percentile rank requires ≥2 entities, Issue #193). "
            "Initial state: IMF WEO April 2001 + INDEC EPH October 2000 "
            "+ NOAA MLO 2000 (co2_concentration_ppm=369.5) "
            "+ WB WGI 2000 (rule_of_law_percentile=33.2) "
            "+ V-Dem v13 (democratic_quality_score=0.71)."
        ),
        "configuration": demo_config,
        "scheduled_inputs": demo_scheduled_inputs,
    })
