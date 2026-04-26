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
    # Fiscal spending cuts raise poverty headcount for Q1 informal workers.
    # Lustig (2017) estimates a ~15pp poverty rate response per 1pp spending cut
    # for the bottom quintile in emerging-market fiscal consolidation episodes.
    CohortElasticity(
        event_type="fiscal_spending_change",
        cohort_spec=CohortSpec(
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
        ),
        attribute_key="poverty_headcount_ratio",
        elasticity=Decimal("-0.15"),
        source=(
            "Lustig (2017): The Impact of Fiscal Policy on Inequality and Poverty"
            " in Latin America. IMF Working Paper WP/17/55."
        ),
        source_registry_id="ACADEMIC_LITERATURE_LUSTIG_2017_FISCAL_POVERTY",
        confidence_tier=3,
    ),
    # Q2 informal workers face smaller but significant poverty exposure.
    # Ball et al. (2013) document distributional effects of consolidation across
    # 17 OECD countries: Q2 effect roughly 2/3 of Q1 effect.
    CohortElasticity(
        event_type="fiscal_spending_change",
        cohort_spec=CohortSpec(
            IncomeQuintile.Q2,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
        ),
        attribute_key="poverty_headcount_ratio",
        elasticity=Decimal("-0.10"),
        source=(
            "Ball, Furceri, Leigh, Loungani (2013): The Distributional Effects"
            " of Fiscal Consolidation. IMF Working Paper WP/13/151."
        ),
        source_registry_id="ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION",
        confidence_tier=3,
    ),
    # Agricultural sector Q1 cohorts: subsistence exposure amplifies poverty
    # response to fiscal cuts that reduce rural subsidies and extension services.
    # IMF (2014) finds agricultural cohort poverty response ~80% of informal rate.
    CohortElasticity(
        event_type="fiscal_spending_change",
        cohort_spec=CohortSpec(
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.AGRICULTURE,
        ),
        attribute_key="poverty_headcount_ratio",
        elasticity=Decimal("-0.12"),
        source=(
            "IMF (2014): Fiscal Policy and Income Inequality."
            " IMF Policy Paper, January 2014."
        ),
        source_registry_id="ACADEMIC_LITERATURE_IMF_2014_FISCAL_INEQUALITY",
        confidence_tier=3,
    ),
]
