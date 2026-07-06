"""Iceland 2008–11 heterodox baseline — capital controls + bank nationalisation.

Historical context:
  Iceland's October 2008 banking collapse was the largest relative to GDP in
  modern history. Faced with banking sector liabilities ~10× GDP, Iceland
  rejected the orthodox IMF prescription and instead imposed capital controls,
  nationalised the failed banks (separating foreign creditors from domestic
  depositors), and introduced household debt relief via krona-indexed mortgage
  writedowns.

  The heterodox path produced a faster recovery than IMF-programme peers
  (Ireland, Greece, Portugal) with lower unemployment persistence and faster
  poverty headcount recovery — at the cost of foreign creditor haircuts and
  temporary capital account isolation.

  This is the heterodox BASELINE — what actually happened. The orthodox
  counter-factual (what IMF prescription would have produced) is in
  isl_2008_orthodox_counterfactual.py.

Classification: Pre-calibration structural test.
  Output interpreted as "what does the engine's current structural model
  show?" — not a calibrated prediction. ADR-020 channels must be active
  for Channel A (reserve protection), Channel B (credit contraction GDP),
  and Channel C (Q1 PHC impact) to fire.

Timeline modeled (4 annual steps):
  Step 1 (Oct 2008): Capital controls imposed; banking sector nationalised.
  Step 2 (2009): Household debt relief (REGULATORY_CHANGE); modest fiscal
    adjustment (-2% GDP, far below orthodox austerity prescription).
  Step 3 (2010): Recovery trajectory; controls maintained.
  Step 4 (2011): Continued recovery; export-led growth via krona devaluation.

Initial state (October 2008 baseline — pre-controls-imposition):
  reserve_coverage_months         — Central Bank of Iceland: ~3.5 months
  gdp_growth                      — Statistics Iceland: ~-3% at crisis onset
  q1_poverty_headcount_ratio      — Eurostat SILC: ~8% (pre-crisis low)
  capital_account_outflow_velocity — Tier 2 estimate: severe capital flight ~2
  banking_sector_leverage_ratio   — CBI Annual Report 2008: ~10× GDP
  political_legitimacy_index      — WVS / PEM: 0.72 (democratic mandate)

References: Issue #1553; ADR-020 (ARCH-014); calibration-basis.md §Capital Controls.
"""
from __future__ import annotations

from datetime import date

from app.schemas import (
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScheduledInputSchema,
)

# ---------------------------------------------------------------------------
# Shared ISL October 2008 baseline attributes (identical for both scenarios)
# ---------------------------------------------------------------------------

_ISL_START_DATE = date(2008, 10, 1)


def _isl_baseline_attributes() -> dict[str, QuantitySchema]:
    """Return ISL October 2008 initial state attributes.

    Shared by both heterodox baseline and orthodox counter-factual.
    Data tiers: see calibration-basis.md §Capital Controls (CM advisory 2026-07-03).
    """
    return {
        # Central Bank of Iceland Annual Report 2008: ~3.5 months gross import cover
        # at October 2008 capital controls imposition. Declining from 8.3 months
        # (end-2007) due to accelerating capital outflows.
        "reserve_coverage_months": QuantitySchema(
            value="3.5",
            unit="months",
            variable_type="stock",
            attribute_type="stock",
            confidence_tier=1,
            observation_date=_ISL_START_DATE,
            source_registry_id="CENTRAL_BANK_ICELAND_ANNUAL_2008",
            measurement_framework="financial",
        ),

        # Statistics Iceland / IMF WEO: Iceland 2008 full-year GDP -6.6%;
        # Q4 2008 annualised at crisis onset ~-3% (acute phase entry point).
        "gdp_growth": QuantitySchema(
            value="-0.03",
            unit="ratio",
            variable_type="ratio",
            attribute_type="rate",
            confidence_tier=1,
            observation_date=_ISL_START_DATE,
            source_registry_id="STATISTICS_ICELAND_GDP_2008Q4",
            measurement_framework="financial",
        ),

        # Eurostat EU-SILC ISL 2008: Iceland pre-crisis poverty rate ~8%
        # at 60% median income threshold. Q1 informal proxy (ADR-020 Channel C
        # targets Q1 informal PHC; ISL Q1 is small relative to peer economies).
        "q1_poverty_headcount_ratio": QuantitySchema(
            value="0.08",
            unit="ratio",
            variable_type="ratio",
            attribute_type="rate",
            confidence_tier=2,
            observation_date=_ISL_START_DATE,
            source_registry_id="EUROSTAT_SILC_ISL_2008",
            measurement_framework="human_development",
        ),

        # Tier 2 estimate: Iceland 2008 capital flight velocity.
        # FX reserves fell from €4.0bn (Sep 2008) to €1.5bn (Oct 2008) in weeks
        # before controls imposed — approximately 2 months of reserve coverage
        # equivalent per annual step at the acute crisis rate.
        # Required for ADR-020 Channel A: reserve_delta = outflow_velocity * ε * severity * impl_cap
        "capital_account_outflow_velocity": QuantitySchema(
            value="2.0",
            unit="months_per_step",
            variable_type="flow",
            attribute_type="flow",
            confidence_tier=2,
            observation_date=_ISL_START_DATE,
            source_registry_id="CBI_BOP_ISL_2008Q3Q4_OUTFLOW_ESTIMATE",
            measurement_framework="financial",
        ),

        # Central Bank of Iceland 2008: banking sector total assets ~€100bn
        # against GDP ~€12bn → leverage ratio ~8-10×. Rounded to 10.0 for
        # structural severity representation.
        "banking_sector_leverage_ratio": QuantitySchema(
            value="10.0",
            unit="ratio",
            variable_type="ratio",
            attribute_type="structural_index",
            confidence_tier=1,
            observation_date=_ISL_START_DATE,
            source_registry_id="CENTRAL_BANK_ICELAND_ANNUAL_2008",
            measurement_framework="financial",
        ),

        # WVS / PoliticalEconomyModule default: Iceland had strong democratic
        # mandate for the heterodox path. October 2008 public sentiment strongly
        # opposed bank bailout at taxpayer expense (post-Icesave dispute).
        "political_legitimacy_index": QuantitySchema(
            value="0.72",
            unit="index_0_1",
            variable_type="ratio",
            attribute_type="structural_index",
            confidence_tier=2,
            observation_date=_ISL_START_DATE,
            source_registry_id="WVS_ISL_2005_POLITICAL_TRUST",
            measurement_framework="governance",
        ),
    }


# ---------------------------------------------------------------------------
# Heterodox baseline scenario builder
# ---------------------------------------------------------------------------


def build_isl_heterodox_scenario() -> ScenarioCreateRequest:
    """Build Iceland 2008–11 heterodox baseline scenario.

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    4 annual steps. TYPE_A (historical baseline) and TYPE_B comparison target.

    ADR-020 Channel A fires at Step 1: capital controls reduce
    capital_account_outflow_velocity by ε=0.60 fraction → positive
    reserve_coverage_months delta.

    ADR-020 Channel B fires at Step 1: credit contraction β=0.020
    applied to gdp_growth with γ=1.2 amplification.

    ADR-020 Channel C fires at Step 1 via bridge event: Q1 informal
    poverty_headcount_ratio rises (credit contraction → labour shock).
    """
    return ScenarioCreateRequest(
        name="Iceland 2008–11 Heterodox Baseline — Capital Controls + Nationalisation",
        description=(
            "Pre-calibration structural test for Issue #1553. "
            "Iceland October 2008: capital controls imposed (Step 1) to arrest "
            "capital flight; banking sector nationalised (Landsbanki, Glitnir, Kaupthing); "
            "household debt relief via krona-indexed mortgage writedown (Step 2); "
            "modest fiscal adjustment (-2% GDP) — NOT deep austerity. "
            "ADR-020 channels active: Channel A (reserve protection, ε=0.60), "
            "Channel B (credit contraction, β=0.020, γ=1.2), "
            "Channel C (Q1 PHC via bridge event, φ=-0.30). "
            "pre_calibration_structural_test: true. "
            "Fidelity target: DIRECTION_ONLY (pre-M19-calibration). "
            "Initial state: Central Bank of Iceland Annual Report 2008; "
            "Statistics Iceland; Eurostat EU-SILC 2008."
        ),
        configuration=ScenarioConfigSchema(
            entities=["ISL"],
            n_steps=4,
            timestep_label="annual",
            start_date=_ISL_START_DATE,
            step_metadata={
                "1": {
                    "significance": "CRISIS",
                    "label": "Capital controls + bank nationalisation",
                    "year": "2008",
                },
                "2": {
                    "significance": "SIGNIFICANT",
                    "label": "Household debt relief + modest fiscal adjustment",
                    "year": "2009",
                },
                "3": {
                    "significance": "SIGNIFICANT",
                    "label": "Recovery trajectory — controls maintained",
                    "year": "2010",
                },
                "4": {
                    "significance": "ROUTINE",
                    "label": "Export-led recovery — krona devaluation absorbed",
                    "year": "2011",
                },
            },
            initial_attributes={
                "ISL": _isl_baseline_attributes(),
            },
        ),
        scheduled_inputs=[
            # Step 1 (Oct 2008): Capital controls — ADR-020 Channel A+B+C trigger.
            # severity=0.85: acute capital flight environment (near-total account closure).
            # epsilon=0.60: controls arrest 60% of outflow velocity (capital-controls-only
            #   regime per calibration-basis.md §Capital Controls ε_controls_only=0.50–0.60).
            # implementation_capacity=0.75: strong democratic mandate, rapid CB implementation.
            # magnitude=0.85: passed in parameters to produce Event.affected_attributes
            #   {"capital_controls": Quantity(value=0.85)} for Channel A+B extraction.
            ScheduledInputSchema(
                step=1,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "capital_controls",
                    "target_entity": "ISL",
                    "magnitude": "0.85",
                    "epsilon": "0.60",
                    "implementation_capacity": "0.75",
                    "expected_duration": 8,
                },
            ),

            # Step 1 (Oct 2008): Banking sector nationalisation.
            # Emergency instrument — NATIONALIZATION (EmergencyInstrument.NATIONALIZATION).
            # Separates foreign creditors from domestic depositors (Icesave precedent).
            ScheduledInputSchema(
                step=1,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "nationalization",
                    "target_entity": "ISL",
                    "magnitude": "0.90",
                    "implementation_capacity": "0.80",
                    "expected_duration": 1,
                },
            ),

            # Step 2 (2009): Household debt relief — krona-indexed mortgage writedown.
            # REGULATORY_CHANGE: links mortgage payments to CPI cap, reducing real
            # household debt burden for Q1/Q2 income cohorts.
            ScheduledInputSchema(
                step=2,
                input_type="StructuralPolicyInput",
                input_data={
                    "instrument": "regulatory_change",
                    "target_entity": "ISL",
                    "affected_sector": "household_finance",
                    "implementation_years": 2,
                },
            ),

            # Step 2 (2009): Modest fiscal adjustment (-2% GDP).
            # Iceland's actual fiscal response was far below orthodox prescription.
            # Welfare state preserved; adjustment targeted discretionary spending.
            ScheduledInputSchema(
                step=2,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "ISL",
                    "sector": "government",
                    "value": "-0.02",
                    "duration_years": 1,
                },
            ),
        ],
    )
