"""Elasticity registry for the DemographicModule — ADR-005 Decision 1.

Each entry encodes an empirical relationship: when event_type fires on a
country entity, the specified cohort's attribute_key changes by
(event_magnitude × elasticity).

All source_registry_id values follow the ACADEMIC_LITERATURE_* naming
convention from DATA_STANDARDS.md §Data Provenance Requirements.
Entries are Tier 3 confidence (derived from Tier 1 sources via documented
methodology) until backtesting calibration upgrades them.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.simulation.modules.demographic.cohort import (
    AgeBand,
    CohortSpec,
    EmploymentSector,
    IncomeQuintile,
)


@dataclass(frozen=True)
class CohortElasticity:
    """One row of the elasticity matrix.

    Encodes: when event_type fires on the parent country entity, this cohort's
    attribute_key changes by (event_magnitude * elasticity).

    entity_families: if None, fires on ALL entities (existing SSA behaviour).
    If a frozenset, fires only when the country entity.id is in the set.
    Calibration decision: docs/calibration/m19-cm-a-euro-area-calibration-decision.md §1.2.
    """

    event_type: str
    cohort_spec: CohortSpec
    attribute_key: str
    elasticity: Decimal
    source: str
    source_registry_id: str
    confidence_tier: int
    entity_families: frozenset[str] | None = None


ELASTICITY_REGISTRY: list[CohortElasticity] = [
    # GDP contraction raises poverty headcount for Q1 informal workers.
    # M17-G1 SSA recalibration (Fosu 2011): prior -0.10 was calibrated from
    # Lustig (2017) Latin American episodes. SSA poverty-growth elasticities
    # are 1.5–2× larger than Latin American comparators at equivalent inequality
    # levels (Fosu 2011; Ravallion 2012 comparison basis). Senegal's ECOWAS-
    # regional inequality position (Gini ≈ 0.38) corresponds to Fosu (2011)
    # moderate-inequality SSA mid-range (-0.15 to -0.25); point estimate -0.20.
    # Calibration decision: docs/calibration/m17-g1-elasticity-calibration-decision.md
    # T3 — regionally inferred SSA, not Senegal-specific backtested. T2 upgrade
    # requires Senegal quarterly poverty-growth backtesting (M18 scope).
    CohortElasticity(
        event_type="gdp_growth_change",
        cohort_spec=CohortSpec(
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
        ),
        attribute_key="poverty_headcount_ratio",
        elasticity=Decimal("-0.20"),
        source=(
            "Fosu, A.K. (2011): The Effect of Income Distribution on the"
            " Poverty-Growth Relationship: Empirical Evidence from Sub-Saharan"
            " Africa. Journal of African Economies 20(5): 811-839."
            " DOI: 10.1093/jae/ejr019. SSA mid-range elasticity for moderate-"
            "inequality countries (Gini 0.35-0.40). 2x prior Latin American"
            " calibration (Lustig 2017) per Fosu/Ravallion SSA-vs-LAC finding."
            " M17-G1 recalibration — see calibration decision doc §3.2."
        ),
        source_registry_id="ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH",
        confidence_tier=3,
    ),
    # Q2 informal workers: 2/3 of Q1 effect per Ball et al. (2013) scaling.
    # M17-G1: Ball (2013) 2/3 ratio preserved; absolute base revised with Q1
    # SSA recalibration → 2/3 × 0.20 = 0.133 (prior: 0.067 = 2/3 × 0.10).
    CohortElasticity(
        event_type="gdp_growth_change",
        cohort_spec=CohortSpec(
            IncomeQuintile.Q2,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
        ),
        attribute_key="poverty_headcount_ratio",
        elasticity=Decimal("-0.133"),
        source=(
            "Ball, Furceri, Leigh, Loungani (2013): The Distributional Effects"
            " of Fiscal Consolidation. IMF Working Paper WP/13/151."
            " 2/3 scaling of Q1 informal (between-quintile distribution structure)."
            " Base Q1 revised to SSA calibration (Fosu 2011) in M17-G1;"
            " 2/3 ratio preserved per ADR-006 Decision 10."
        ),
        source_registry_id="ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION",
        confidence_tier=3,
    ),
    # ADR-020 Channel C: credit contraction → Q1 informal poverty headcount.
    # φ = -0.30: Iceland 2008-11 micro-survey basis (calibration-basis.md §Capital Controls).
    # Credit contraction → tighter lending → informal-sector unemployment → PHC increase.
    # Bridge event magnitude is NEGATIVE (credit contraction); elasticity is NEGATIVE →
    # PHC delta is POSITIVE (poverty rises when credit contracts). T3 until ISL backtesting.
    CohortElasticity(
        event_type="credit_contraction_labour_shock",
        cohort_spec=CohortSpec(
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
        ),
        attribute_key="poverty_headcount_ratio",
        elasticity=Decimal("-0.30"),
        source=(
            "Iceland 2008-11 micro-survey: credit contraction → informal employment"
            " → Q1 poverty headcount ratio. ADR-020 Channel C calibration."
            " φ=0.30 point estimate; docs/methodology/calibration-basis.md §Capital Controls."
        ),
        source_registry_id="ACADEMIC_LITERATURE_ICELAND_2008_CREDIT_CONTRACTION_PHC",
        confidence_tier=3,
    ),
    # Agricultural Q1 cohorts: subsistence amplification at 80% of informal rate.
    # M17-G1: IMF (2014) 80% scaling preserved; absolute base revised with Q1
    # SSA recalibration → 0.80 × 0.20 = 0.16 (prior: 0.08 = 0.80 × 0.10).
    CohortElasticity(
        event_type="gdp_growth_change",
        cohort_spec=CohortSpec(
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.AGRICULTURE,
        ),
        attribute_key="poverty_headcount_ratio",
        elasticity=Decimal("-0.16"),
        source=(
            "IMF (2014): Fiscal Policy and Income Inequality."
            " IMF Policy Paper, January 2014. Table 1: SSA LIC fiscal shock"
            " consumption elasticity 1.8-2.5x EMDE baseline."
            " 80% scaling of Q1 informal (subsistence amplification factor)."
            " Base Q1 revised to SSA calibration (Fosu 2011) in M17-G1."
        ),
        source_registry_id="ACADEMIC_LITERATURE_IMF_2014_FISCAL_INEQUALITY",
        confidence_tier=3,
    ),
    # Euro area / GRC: Q1 FORMAL formal-sector poverty-GDP elasticity.
    # M19-CM-A calibration (Blanchard & Leigh 2013 + Eurostat AROPE 2010-2013).
    # Greek AROPE rose 8pp on 26pp GDP decline → aggregate PHC elasticity 0.31/unit.
    # Q1 cohort concentration factor ~2× aggregate (Ball et al. 2013) → 0.62 upper.
    # Dampened to -0.25 for per-step quarterly dynamics (formal-sector UI coverage 50%
    # at crisis depth reduces short-run PHC impact vs annual aggregate).
    # entity_families=frozenset({"GRC"}): fires only on GRC entity; not on SSA entities.
    # Calibration: docs/calibration/m19-cm-a-euro-area-calibration-decision.md §3.1.
    CohortElasticity(
        event_type="gdp_growth_change",
        cohort_spec=CohortSpec(
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
        ),
        attribute_key="poverty_headcount_ratio",
        elasticity=Decimal("-0.25"),
        source=(
            "Blanchard, O. & Leigh, D. (2013): Growth Forecast Errors and Fiscal"
            " Multipliers. IMF Working Paper WP/13/1. Actual fiscal multiplier"
            " 1.3 (range 0.9–1.7) vs assumed 0.5 — validates Euro area crisis"
            " calibration distinct from SSA. Eurostat AROPE Greece 2010–2013:"
            " +8pp poverty on 26pp GDP decline (0.31/unit aggregate)."
            " Q1 formal cohort concentration ~2× aggregate (Ball et al. 2013);"
            " dampened to -0.25 for quarterly per-step dynamics (50% UI coverage)."
            " Uncertainty range: -0.20 to -0.35. M19-CM-A calibration."
        ),
        source_registry_id="ACADEMIC_LITERATURE_BLANCHARD_LEIGH_2013_FISCAL_MULTIPLIERS",
        confidence_tier=2,
        entity_families=frozenset({"GRC"}),
    ),
    # Euro area / GRC: Q2 FORMAL formal-sector poverty-GDP elasticity.
    # Ball et al. (2013) 0.60 scaling of Q1 FORMAL: 0.60 × -0.25 = -0.15.
    # Q2 formal workers have higher UI coverage and employment tenure than Q1,
    # absorbing less impact per unit fiscal adjustment. Uncertainty: -0.12 to -0.20.
    CohortElasticity(
        event_type="gdp_growth_change",
        cohort_spec=CohortSpec(
            IncomeQuintile.Q2,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
        ),
        attribute_key="poverty_headcount_ratio",
        elasticity=Decimal("-0.15"),
        source=(
            "Ball, Furceri, Leigh, Loungani (2013): The Distributional Effects"
            " of Fiscal Consolidation. IMF Working Paper WP/13/151."
            " 0.60 scaling of GRC Q1 FORMAL (Blanchard & Leigh 2013 base):"
            " 0.60 × -0.25 = -0.15. Q2 formal workers have stronger UI coverage"
            " and employment tenure — absorb 0.60× the Q1 per-unit impact."
            " Uncertainty range: -0.12 to -0.20. M19-CM-A calibration."
        ),
        source_registry_id="ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION",
        confidence_tier=2,
        entity_families=frozenset({"GRC"}),
    ),
]
