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
    # Elasticity calibrated from Lustig (2017) via MacroeconomicModule chain:
    # fiscal spending cut → GDP contraction (regime multiplier 1.5 in recession)
    # → poverty headcount response. Per unit gdp_growth_change: ~0.10 poverty pp
    # per pp GDP contraction for Q1 informal in consolidation episodes.
    CohortElasticity(
        event_type="gdp_growth_change",
        cohort_spec=CohortSpec(
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
        ),
        attribute_key="poverty_headcount_ratio",
        elasticity=Decimal("-0.10"),
        source=(
            "Lustig (2017): The Impact of Fiscal Policy on Inequality and Poverty"
            " in Latin America. IMF Working Paper WP/17/55."
            " Recalibrated for gdp_growth_change units via MacroeconomicModule"
            " recession multiplier (ADR-006 Decision 10)."
        ),
        source_registry_id="ACADEMIC_LITERATURE_LUSTIG_2017_FISCAL_POVERTY",
        confidence_tier=3,
    ),
    # Q2 informal workers: ~2/3 of Q1 effect per Ball et al. (2013).
    CohortElasticity(
        event_type="gdp_growth_change",
        cohort_spec=CohortSpec(
            IncomeQuintile.Q2,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
        ),
        attribute_key="poverty_headcount_ratio",
        elasticity=Decimal("-0.067"),
        source=(
            "Ball, Furceri, Leigh, Loungani (2013): The Distributional Effects"
            " of Fiscal Consolidation. IMF Working Paper WP/13/151."
            " Recalibrated for gdp_growth_change units (ADR-006 Decision 10)."
        ),
        source_registry_id="ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION",
        confidence_tier=3,
    ),
    # Agricultural Q1 cohorts: subsistence amplification ~80% of informal rate.
    CohortElasticity(
        event_type="gdp_growth_change",
        cohort_spec=CohortSpec(
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.AGRICULTURE,
        ),
        attribute_key="poverty_headcount_ratio",
        elasticity=Decimal("-0.08"),
        source=(
            "IMF (2014): Fiscal Policy and Income Inequality."
            " IMF Policy Paper, January 2014."
            " Recalibrated for gdp_growth_change units (ADR-006 Decision 10)."
        ),
        source_registry_id="ACADEMIC_LITERATURE_IMF_2014_FISCAL_INEQUALITY",
        confidence_tier=3,
    ),
]
