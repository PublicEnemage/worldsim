"""Iceland 2008–11 orthodox counter-factual — IMF prescription (not taken).

Historical context:
  Iceland rejected IMF-orthodox conditionality in October 2008. The orthodox
  path would have required: bank bailout via sovereign debt assumption (taking
  on ~80% GDP of banking sector liabilities), deep fiscal austerity, and
  maintaining an open capital account to preserve creditor interests.

  This counter-factual models what the IMF-orthodox prescription would have
  produced, given Iceland's 2008 starting position. The Orthodox path was NOT
  taken. Outputs should be interpreted as INFERRED_STRUCTURAL (Tier 3) — the
  alternative path was not historically executed.

  Counter-factual question: does the heterodox baseline (isl_2008_heterodox.py)
  produce better human development outcomes than the orthodox path would have?

  Expected structural direction: BASELINE_BETTER — the heterodox path (capital
  controls + nationalisation + household debt relief) produces lower Q1 poverty
  headcount and faster GDP recovery than the orthodox path (austerity + open
  capital account + bank bailout via sovereign debt assumption).

Classification: Pre-calibration structural test, TYPE_B counter-factual.
  INFERRED_STRUCTURAL (Tier 3) — the alternative path was not historically
  executed. Persistent direction disagreement should be escalated to CM.

Timeline modeled (4 annual steps — same window as heterodox baseline):
  Step 1 (Oct 2008): IMF programme acceptance (full conditionality);
    deep fiscal austerity (-8% GDP); no capital controls imposed.
  Steps 2–4 (2009–2011): Continued austerity (tapering); sovereign debt
    service burden for banking sector bailout; open capital account maintained.

References: Issue #1553; ADR-020 (ARCH-014); calibration-basis.md §Capital Controls.
"""
from __future__ import annotations

from app.schemas import (
    ScenarioCreateRequest,
    ScheduledInputSchema,
)
from tests.fixtures.isl_2008_heterodox import build_isl_heterodox_scenario


def build_isl_orthodox_counterfactual_scenario() -> ScenarioCreateRequest:
    """Build Iceland 2008–11 orthodox counter-factual scenario.

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    4 annual steps. TYPE_B counter-factual against the heterodox baseline.

    Same ISL October 2008 initial state as the heterodox baseline.
    Structural differences:
    - Step 1: IMF programme acceptance (full conditionality, HIGH tier)
    - Step 1: Deep fiscal austerity (-8% GDP) — far above Iceland's actual -2%
    - Steps 2–4: Continued fiscal contraction (tapering IMF conditionality)
    - No capital controls imposed — open capital account maintained
    - No banking sector nationalisation — implicit sovereign bailout assumed

    Known limitations for this counter-factual:
    - Sovereign debt assumption for banking bailout not directly modeled —
      DFICommitmentInput not yet supported in web_scenario_runner. The fiscal
      cost is approximated through fiscal deterioration dynamics.
    - Q2 poverty gap: Channel C targets Q1 informal only (ADR-020 INCORPORATE-5).
    - Iceland Q1 household debt overhang: actual recovery slower than model
      shows (dollarised mortgage debt burden not captured by current modules).
    - Dollarised corporate debt amplification not modeled (ADR-020 §Known Limitations).
    - Bilateral creditor composition (UK/Netherlands Icesave dispute) not modeled.
    """
    base = build_isl_heterodox_scenario()

    return base.model_copy(update={
        "name": "Iceland 2008–11 Orthodox Counter-Factual — IMF Programme (Not Taken)",
        "description": (
            "TYPE_B counter-factual for Issue #1553. "
            "Orthodox IMF prescription (NOT actually taken). "
            "Step 1: IMF programme acceptance (HIGH conditionality) + deep fiscal austerity "
            "(-8% GDP — consistent with standard IMF conditionality circa 2008). "
            "Steps 2-4: Continued fiscal contraction (-4%/-2%/-1% GDP). "
            "No capital controls imposed — open capital account maintained. "
            "No bank nationalisation — sovereign bailout assumed (not explicitly modeled). "
            "INFERRED_STRUCTURAL (Tier 3): this path was not historically executed. "
            "Expected verdict: BASELINE_BETTER (heterodox baseline outperforms this path "
            "on human development indicators at Step 4). "
            "pre_calibration_structural_test: true."
        ),
        "scheduled_inputs": [
            # Step 1 (Oct 2008): IMF programme acceptance — full conditionality.
            # HIGH conditionality tier: consistent with orthodox prescription.
            # implementation_capacity=0.65: conditionality is politically costly;
            # lower feasibility than heterodox path.
            ScheduledInputSchema(
                step=1,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "imf_program_acceptance",
                    "target_entity": "ISL",
                    "expected_duration": 4,
                    "program_size_gdp_ratio": "0.20",
                    "source": "conditionality",
                    "constraining_actor_id": "IMF",
                    "implementation_capacity": "0.65",
                },
            ),

            # Step 1 (Oct 2008): Deep fiscal austerity — -8% GDP.
            # Orthodox prescription circa 2008 (consistent with Greece 2010 troika
            # conditionality of -4.5% GDP primary surplus; Iceland banking bailout
            # would add ~3.5% additional fiscal pressure → total -8%).
            # Targeting: broad fiscal adjustment (no social protection floor).
            ScheduledInputSchema(
                step=1,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "ISL",
                    "sector": "government",
                    "value": "-0.08",
                    "duration_years": 1,
                },
            ),

            # Step 2 (2009): Continued austerity — tapering to -4% GDP.
            # Year 2 of standard IMF conditionality sequence.
            ScheduledInputSchema(
                step=2,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "ISL",
                    "sector": "government",
                    "value": "-0.04",
                    "duration_years": 1,
                },
            ),

            # Step 3 (2010): Austerity tapering — -2% GDP.
            ScheduledInputSchema(
                step=3,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "ISL",
                    "sector": "government",
                    "value": "-0.02",
                    "duration_years": 1,
                },
            ),

            # Step 4 (2011): Final consolidation — -1% GDP.
            ScheduledInputSchema(
                step=4,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "ISL",
                    "sector": "government",
                    "value": "-0.01",
                    "duration_years": 1,
                },
            ),
        ],
    })
