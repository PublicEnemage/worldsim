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
  build_argentina_scenario(): n_steps=3 (annual); step 1 = 2001, step 2 = 2002, step 3 = 2003.
    Backtesting fixture. Initial state reflects Argentina's 2000 baseline.
    Step 3 represents the Kirchner recovery: fiscal normalisation and social program
    expansion (+3.0% GDP spending_change, T3, MECON Budget Execution 2003).

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
  Step 3: Kirchner recovery — fiscal normalisation (+3.0% GDP spending_change)
  Step 3 (demo only, step 4 in demo): Consolidation — no active shock; ROUTINE step

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
    """Build the Argentina 2001–2003 backtesting scenario configuration.

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    The scenario runs 3 steps (annual: 2001→2002→2003) starting from
    Argentina's 2000 economic conditions.

    Scheduled inputs:
      Step 1: IMF Blindaje continuation + Zero Deficit Plan spending cut
      Step 2: Sovereign default declaration
      Step 3: Kirchner recovery — fiscal normalisation and social program expansion
               (+3.0% GDP spending_change; MECON Budget Execution 2003; T3)

    Initial state attributes:
      gdp_growth        = -0.8%  (IMF WEO April 2001, 2000 outturn)
      unemployment_rate = 14.7% (INDEC EPH October 2000 wave)

    CM Sprint D calibration decision: docs/calibration/m19-cm-d-arg-kirchner-calibration-decision.md
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

    # Investment climate state variables — Issue #34, NB-4 (ADR-001 Amendment 2).
    # Argentina 2000 baseline (scenario initial state reflects end-2000 conditions).

    # JP Morgan EMBI+ spread — Argentina December 2000.
    # Argentina's EMBI spread reached ~700-750bps in late 2000 after S&P's
    # negative outlook revision (October 2000). The Blindaje ($39.7bn) in
    # December 2000 temporarily compressed spreads, but pre-Blindaje close
    # was ~750bps. Confidence tier 2: market data, JP Morgan index series.
    initial_sovereign_risk_premium = QuantitySchema(
        value="0.075",
        unit="ratio",
        variable_type="ratio",
        attribute_type="rate",
        confidence_tier=2,
        observation_date=date(2001, 1, 1),
        source_registry_id="JPMORGAN_EMBI_ARG_2000",
        measurement_framework="financial",
    )

    # UNCTAD World Investment Report 2001 — FDI inward stock / GDP for Argentina.
    # Argentina's inward FDI stock was approximately $67bn against GDP of ~$267bn
    # (25.1% ratio) at end-2000. Spain, USA, and France were largest investors.
    # Confidence tier 2: official multilateral statistics, annual vintage.
    initial_fdi_stock_pct_gdp = QuantitySchema(
        value="0.251",
        unit="ratio",
        variable_type="stock",
        attribute_type="stock",
        confidence_tier=2,
        observation_date=date(2001, 1, 1),
        source_registry_id="UNCTAD_FDI_STATS_ARG_2000",
        measurement_framework="financial",
    )

    # INDEC Balance of Payments 2000 — net portfolio investment / GDP.
    # Argentina had significant portfolio outflows in 2000 as investor
    # confidence deteriorated: approximately -$12bn (~-4.5% of GDP).
    # Confidence tier 2: official national statistics.
    initial_portfolio_flow_velocity = QuantitySchema(
        value="-0.045",
        unit="ratio",
        variable_type="ratio",
        attribute_type="flow",
        confidence_tier=2,
        observation_date=date(2001, 1, 1),
        source_registry_id="INDEC_BOP_ARG_2000",
        measurement_framework="financial",
    )

    # S&P sovereign credit rating — Argentina January 2001: BB.
    # Mapped to 0–100 index (AAA=100, D=0) using standard 21-notch linear scale:
    # BB = 38. Argentina had been downgraded steadily through 2000 and was rated
    # BB by S&P at the start of 2001, reflecting sub-investment-grade status.
    # Confidence tier 1: direct observation from rating agency announcement.
    initial_credit_rating_score = QuantitySchema(
        value="38.0",
        unit="index_0_100",
        variable_type="stock",
        attribute_type="structural_index",
        confidence_tier=1,
        observation_date=date(2001, 1, 1),
        source_registry_id="SP_SOVEREIGN_RATINGS_ARG_2001",
        measurement_framework="financial",
    )

    return ScenarioCreateRequest(
        name="Argentina 2001-2002 Currency and Debt Crisis Backtesting Fixture",
        description=(
            "Backtesting fixture for Issue #192. "
            "Reproduces the Argentina 2001–2002 sovereign default and convertibility "
            "collapse to validate DIRECTION_ONLY GDP contraction thresholds. "
            "Initial state: IMF WEO April 2001 + INDEC EPH October 2000 "
            "+ investment climate variables NB-4 (Issue #34)."
        ),
        configuration=ScenarioConfigSchema(
            entities=["ARG"],
            n_steps=3,
            timestep_label="annual",
            initial_attributes={
                "ARG": {
                    "gdp_growth": initial_gdp_growth,
                    "unemployment_rate": initial_unemployment_rate,
                    "sovereign_risk_premium": initial_sovereign_risk_premium,
                    "fdi_stock_pct_gdp": initial_fdi_stock_pct_gdp,
                    "portfolio_flow_velocity": initial_portfolio_flow_velocity,
                    "credit_rating_score": initial_credit_rating_score,
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
            # Step 3 (2003): Kirchner fiscal normalisation and social program expansion.
            # Néstor Kirchner (from May 2003) maintained the PJJHD emergency employment
            # program, normalised government services after the 2002 emergency contraction,
            # and expanded social transfers. Primary fiscal surplus +0.5% GDP — revenue-
            # driven (export taxes ~1.5% GDP); net spending recovery ~+3.0% GDP vs 2002 trough.
            # The IMF Blindaje (step 1, expected_duration=2) expires after step 2 — no IMF
            # conditionality at step 3.
            # Source: MECON Budget Execution 2003 + IMF WEO April 2004. Confidence tier: T3.
            # CM Sprint D calibration decision §3.1.
            ScheduledInputSchema(
                step=3,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "ARG",
                    "sector": "government",
                    "value": "0.030",
                    "duration_years": 1,
                },
            ),
        ],
    )


def build_argentina_counterfactual_scenario() -> ScenarioCreateRequest:
    """Build the Argentina 1999–2001 counter-factual — earlier managed peg exit.

    Counter-factual hypothesis: Argentina exits the convertibility peg in 1999
    under controlled conditions — before the recession deepened and external
    reserves fell critically — rather than maintaining the 1:1 USD peg until
    the disorderly collapse of December 2001.

    Historical basis: Several economists (Mussa 2002, Calvo 2002) argued that
    an earlier controlled devaluation from a position of relative strength
    (mid-1999, reserves ~USD 30bn, EMBI spread ~350bps) would have been
    significantly less contractionary than the eventual corralito/default path.

    Initial state (1999 baseline — before recession deepened):
      gdp_growth        — IMF WEO 1999 outturn: -3.4% (Argentina's recession
                          started with Brazil's January 1999 devaluation)
      unemployment_rate — INDEC EPH October 1998: 12.9%
      sovereign_risk_premium — EMBI+ ARG mid-1999: ~350bps (confidence tier 2)
      fdi_stock_pct_gdp      — UNCTAD 1999: ~$48bn / ~$285bn GDP = 16.8%
      portfolio_flow_velocity — INDEC BOP 1999: moderate outflows ~-2.5% GDP
      credit_rating_score    — S&P BB+ (1999): 41 on 0–100 21-notch scale

    Scheduled inputs (orderly managed exit):
      Step 1 (1999): Modest fiscal adjustment + managed devaluation preparation
      Step 2 (2000): Gradual stabilization path
      Step 3 (2001): Recovery — no active shock; economy stabilises after exit

    The counter-factual does NOT include default_declaration or emergency_declaration.
    No capital controls are imposed. The absence of a corralito is the core
    hypothesis: the peg exit happens before the bank-run dynamic develops.

    n_steps = 3 (satisfies AC-ARG-1: n_steps >= 3).
    Type B comparison: builds a different starting-condition scenario against the
    2001 baseline (build_argentina_scenario(), n_steps=2). The direction_verdict
    advisory expects COUNTER_FACTUAL_BETTER on fin_composite.

    Known limitation (AC-9): counter-factual timing and magnitude are
    INFERRED_STRUCTURAL (Tier 3) — no historical orderly exit was executed.
    Direction verdict is advisory; escalate persistent mismatch to CM.

    References: Issue #1548; M19 G2C sprint entry §3.1;
    intent doc M19-G2C-2026-07-03-battle-testing-scenario-runs.md §Appendix B.
    Mussa (2002) IMF WP/02/187; Calvo (2002) NBER WP/9221.
    """
    # IMF WEO April 1999 — Argentina 1998 real GDP growth outturn: -3.4%
    # (The 1999 recession started in Q1 1999 following Brazil's January devaluation.)
    initial_gdp_growth = QuantitySchema(
        value="-0.034",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(1999, 4, 1),
        source_registry_id="IMF_WEO_APR1999",
        measurement_framework="financial",
    )

    # INDEC EPH October 1998 semi-annual wave — 12.9% unemployment.
    # Unemployment was already elevated going into the 1999 recession;
    # the INDEC October 1998 survey precedes the sharpest contraction.
    initial_unemployment_rate = QuantitySchema(
        value="0.129",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(1998, 10, 1),
        source_registry_id="INDEC_EPH_1998",
        measurement_framework="human_development",
    )

    # JP Morgan EMBI+ spread — Argentina mid-1999.
    # Following Brazil's January 1999 devaluation and contagion, ARG EMBI
    # spread reached ~350bps by mid-1999 before the Blindaje negotiations.
    # Confidence tier 2: JP Morgan index series.
    initial_sovereign_risk_premium = QuantitySchema(
        value="0.035",
        unit="ratio",
        variable_type="ratio",
        attribute_type="rate",
        confidence_tier=2,
        observation_date=date(1999, 6, 1),
        source_registry_id="JPMORGAN_EMBI_ARG_1999",
        measurement_framework="financial",
    )

    # UNCTAD World Investment Report 1999 — FDI inward stock / GDP for Argentina.
    # Inward FDI stock approximately $48bn against GDP of ~$285bn (16.8% ratio).
    # Lower than the 2001 baseline (25.1%) — privatisations peaked in 1997–98.
    # Confidence tier 2: official multilateral statistics.
    initial_fdi_stock_pct_gdp = QuantitySchema(
        value="0.168",
        unit="ratio",
        variable_type="stock",
        attribute_type="stock",
        confidence_tier=2,
        observation_date=date(1999, 1, 1),
        source_registry_id="UNCTAD_FDI_STATS_ARG_1999",
        measurement_framework="financial",
    )

    # INDEC Balance of Payments 1999 — net portfolio investment / GDP.
    # Moderate outflows in 1999 following Brazil devaluation: ~-$7bn (~-2.5% GDP).
    # Less severe than the 2001 baseline (-4.5% GDP) — external position still
    # held in mid-1999 before the reserve drawdown accelerated.
    initial_portfolio_flow_velocity = QuantitySchema(
        value="-0.025",
        unit="ratio",
        variable_type="ratio",
        attribute_type="flow",
        confidence_tier=2,
        observation_date=date(1999, 1, 1),
        source_registry_id="INDEC_BOP_ARG_1999",
        measurement_framework="financial",
    )

    # S&P sovereign credit rating — Argentina 1999: BB+.
    # Argentina maintained BB+ through 1999; downgraded to BB in early 2000.
    # Mapped to 0–100 index (AAA=100, D=0) using 21-notch linear scale: BB+=41.
    # Confidence tier 1: direct observation from rating agency announcement.
    initial_credit_rating_score = QuantitySchema(
        value="41.0",
        unit="index_0_100",
        variable_type="stock",
        attribute_type="structural_index",
        confidence_tier=1,
        observation_date=date(1999, 1, 1),
        source_registry_id="SP_SOVEREIGN_RATINGS_ARG_1999",
        measurement_framework="financial",
    )

    return ScenarioCreateRequest(
        name="Argentina 1999–2001 Counter-Factual — Earlier Managed Peg Exit",
        description=(
            "G2C counter-factual for Issue #1548. "
            "Hypothesis: Argentina exits the convertibility peg in mid-1999 under "
            "controlled conditions — before the corralito and sovereign default of "
            "December 2001. "
            "Initial state: 1999 baseline (recession onset; EMBI ~350bps; reserves intact). "
            "Orderly fiscal path: modest adjustment (Step 1) + gradual stabilisation (Step 2) "
            "+ recovery (Step 3). No default declaration. No capital controls. "
            "Type B comparison against build_argentina_scenario() (2001 crisis path, n_steps=2). "
            "Counter-factual inputs are INFERRED_STRUCTURAL (Tier 3): no historical managed "
            "exit was executed. Direction verdict on fin_composite is advisory. "
            "Sources: IMF WEO 1999; INDEC EPH 1998; UNCTAD 1999; JP Morgan EMBI+ 1999."
        ),
        configuration=ScenarioConfigSchema(
            entities=["ARG"],
            n_steps=3,
            timestep_label="annual",
            start_date=date(1999, 1, 1),
            step_metadata={
                "1": {"significance": "SIGNIFICANT", "label": "Managed peg exit / adjustment"},
                "2": {"significance": "SIGNIFICANT", "label": "Stabilisation phase"},
                "3": {"significance": "ROUTINE", "label": "Recovery consolidation"},
            },
            initial_attributes={
                "ARG": {
                    "gdp_growth": initial_gdp_growth,
                    "unemployment_rate": initial_unemployment_rate,
                    "sovereign_risk_premium": initial_sovereign_risk_premium,
                    "fdi_stock_pct_gdp": initial_fdi_stock_pct_gdp,
                    "portfolio_flow_velocity": initial_portfolio_flow_velocity,
                    "credit_rating_score": initial_credit_rating_score,
                },
            },
        ),
        scheduled_inputs=[
            # Step 1 (1999): Modest fiscal adjustment — supports managed peg exit.
            # A controlled devaluation requires concurrent fiscal tightening to
            # anchor expectations. ~2% GDP spending cut (vs Zero Deficit Plan's 6.5%).
            ScheduledInputSchema(
                step=1,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "ARG",
                    "sector": "government",
                    "value": "-0.020",
                    "duration_years": 1,
                },
            ),
            # Step 1 (1999): Deficit target — medium-term fiscal anchor.
            ScheduledInputSchema(
                step=1,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "deficit_target",
                    "target_entity": "ARG",
                    "sector": "",
                    "value": "-0.030",
                    "duration_years": 3,
                },
            ),
            # Step 2 (2000): Gradual stabilisation — no new shock.
            # Growth stabilises as the new exchange rate supports export
            # competitiveness. Modest fiscal loosening to cushion demand.
            ScheduledInputSchema(
                step=2,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "ARG",
                    "sector": "government",
                    "value": "0.010",
                    "duration_years": 1,
                },
            ),
            # Step 3 (2001): Recovery — no active shock. Economy consolidates.
            # No inputs at Step 3 — counter-factual avoids the Zero Deficit Plan
            # and default spiral entirely.
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
