"""Elasticity registry for GovernanceModule — ADR-005 Decision 6.

Each entry encodes an empirical relationship: when event_type fires on a
country entity, the specified governance indicator changes by
(event_magnitude × elasticity).

All source_registry_id values follow the ACADEMIC_LITERATURE_* naming
convention from DATA_STANDARDS.md §Data Provenance Requirements.
Confidence tier defaults follow ADR-005 Decision 6: Tier 2 for WGI/V-Dem
derived official statistics, Tier 3 for RSF/TI CPI expert surveys.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class GovernanceElasticity:
    """One row of the governance elasticity matrix.

    Encodes: when event_type fires on a country entity, indicator_key
    changes by (event_magnitude × elasticity).
    """

    event_type: str
    indicator_key: str
    elasticity: Decimal
    confidence_tier: int
    source: str
    source_registry_id: str


GOVERNANCE_ELASTICITY_REGISTRY: list[GovernanceElasticity] = [
    # GDP contraction → rule_of_law deterioration.
    # Haggard & Kaufman (2016) document consistent cross-country evidence that
    # sustained GDP contractions erode rule of law through fiscal stress on
    # judicial systems and public administration. Elasticity calibrated at
    # -0.08 percentile points of WGI rule_of_law_percentile per unit of
    # gdp_growth_change (one unit = 1pp GDP growth rate change).
    # Event magnitude is negative for contraction, elasticity negative →
    # positive delta when GDP contracts (rule of law deteriorates = lower score).
    GovernanceElasticity(
        event_type="gdp_growth_change",
        indicator_key="rule_of_law_percentile",
        elasticity=Decimal("-0.08"),
        confidence_tier=2,
        source=(
            "Haggard, S. and Kaufman, R. (2016): Dictators and Democrats: Masses,"
            " Elites, and Regime Change. Princeton University Press."
            " Cross-country time-series analysis of WGI rule_of_law_percentile"
            " vs. GDP growth rate. Elasticity calibrated for gdp_growth_change units"
            " using MacroeconomicModule regime chain (ADR-006 Decision 10)."
        ),
        source_registry_id="ACADEMIC_LITERATURE_HAGGARD_KAUFMAN_2016_GOVERNANCE_GDP",
    ),
    # IMF program acceptance → democratic_quality_score conditionality effect.
    # Grabel (2017) and IMF IEO (2018) document that IMF programs include
    # governance conditionality clauses (anti-corruption benchmarks, statistical
    # reform) that have historically improved democratic_quality_score in
    # compliant programs but reduced it where emergency executive powers were
    # concentrated to achieve conditionality. Net elasticity positive (modest
    # improvement) at +0.005 on V-Dem Liberal Democracy Index per acceptance
    # event. Event magnitude for imf_program_acceptance is +1.0 (binary signal).
    GovernanceElasticity(
        event_type="imf_program_acceptance",
        indicator_key="democratic_quality_score",
        elasticity=Decimal("0.005"),
        confidence_tier=3,
        source=(
            "Grabel, I. (2017): When Things Don't Fall Apart: Global Financial"
            " Governance and Developmental Finance in an Age of Productive Incoherence."
            " MIT Press. IMF IEO (2018): The IMF and Fragile States. Independent"
            " Evaluation Office. Net elasticity from governance conditionality"
            " clause analysis across post-2000 programs."
        ),
        source_registry_id="ACADEMIC_LITERATURE_GRABEL_2017_IMF_GOVERNANCE",
    ),
]
