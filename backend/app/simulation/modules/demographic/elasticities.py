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
    """

    event_type: str
    cohort_spec: CohortSpec
    attribute_key: str
    elasticity: Decimal
    source: str
    source_registry_id: str
    confidence_tier: int


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
]
