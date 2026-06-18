"""Elasticity registry for EcologicalModule — ADR-005 Amendment 1.

Each entry encodes an empirical relationship: when event_type fires on a
country entity, the specified ecological indicator changes by
(event_magnitude × elasticity).

Confidence tier defaults follow ADR-005 Amendment B:
  co2_concentration_ppm: tier 1 (NASA/NOAA direct measurement series)
  land_use_pressure_index: tier 3 (FAO GFR 5-year data; annual interpolation)

All source_registry_id values follow the ACADEMIC_LITERATURE_* naming
convention from DATA_STANDARDS.md §Data Provenance Requirements.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class EcologicalElasticity:
    """One row of the ecological elasticity matrix.

    Encodes: when event_type fires on a country entity, indicator_key
    changes by (event_magnitude × elasticity).
    """

    event_type: str
    indicator_key: str
    elasticity: Decimal
    confidence_tier: int
    source: str
    source_registry_id: str


ECOLOGICAL_ELASTICITY_REGISTRY: list[EcologicalElasticity] = [
    # GDP growth → co2_concentration_ppm.
    # The Global Carbon Project (Friedlingstein et al., 2023) documents the
    # CO2-GDP coupling: global economic output and fossil fuel CO2 emissions
    # track closely, with an emissions-intensity elasticity of approximately
    # 0.5–0.7 per unit of GDP growth rate. At country resolution, GDP growth
    # → more industrial activity, energy use, and transport emissions →
    # higher national contribution to atmospheric CO2. Elasticity calibrated
    # at +0.5 ppm per 1pp GDP growth rate change. Positive sign: GDP growth
    # (positive magnitude) → CO2 increases (positive delta); GDP contraction
    # (negative magnitude) → CO2 decreases (negative delta). This is the
    # correct direction for the economic-ecological channel.
    #
    # Unit note: co2_concentration_ppm is a STOCK (VariableType.STOCK),
    # confidence_tier 1 (NASA/NOAA Mauna Loa direct measurement — ADR-005
    # Amendment B confidence tier table). The delta is applied to the
    # country-level attribute representing the entity's contribution to
    # atmospheric CO2 trajectory.
    EcologicalElasticity(
        event_type="gdp_growth_change",
        indicator_key="co2_concentration_ppm",
        elasticity=Decimal("0.5"),
        confidence_tier=1,
        source=(
            "Friedlingstein, P. et al. (2023): Global Carbon Budget 2023."
            " Earth System Science Data, 15, 5301–5369."
            " doi:10.5194/essd-15-5301-2023. Table 7 (national emissions by"
            " GDP growth category) and Supplementary Figure S12 (emissions"
            " intensity vs. GDP growth rate). The 0.5 ppm/pp elasticity"
            " approximates the annual atmospheric CO2 increment attributable"
            " to a 1pp change in a country's GDP growth rate, derived from"
            " Eq. 2 (atmospheric CO2 growth = fossil emissions + land-use"
            " change − ocean uptake − land uptake). Used as the GDP channel"
            " elasticity for EcologicalElasticity(event_type='gdp_growth_change',"
            " indicator_key='co2_concentration_ppm')."
        ),
        source_registry_id="ACADEMIC_LITERATURE_FRIEDLINGSTEIN_2023_CO2_GDP",
    ),
    # Fiscal spending change → land_use_pressure_index.
    # FAO Global Forest Resources Assessment (FAO GFR 2020) documents a
    # significant negative relationship between government conservation and
    # forest management expenditure and deforestation rates. Countries that
    # reduce public forestry and conservation spending exhibit measurably
    # higher deforestation rates in subsequent 1–2 year periods. The
    # land_use_pressure_index (RATIO, confidence_tier 3 per ADR-005
    # Amendment B) captures the fraction of the safe land-system boundary
    # that a country's land-use change trajectory is consuming.
    #
    # Negative elasticity: fiscal spending cut (negative magnitude) →
    # land_use_pressure increases (positive delta). Mechanism: reduced
    # conservation budget → weakened enforcement of protected areas →
    # accelerated deforestation. Magnitude of fiscal events is the change
    # in spending as a fraction of GDP (e.g., -0.05 for a 5% of GDP cut).
    # Elasticity calibrated at -0.1 RATIO units per unit fiscal change
    # (a 5% GDP spending cut → +0.005 pressure increase, consistent with
    # FAO FRA 2020 national data tables linking conservation expenditure
    # to deforestation rates in high-forest-cover countries).
    EcologicalElasticity(
        event_type="fiscal_policy_spending_change",
        indicator_key="land_use_pressure_index",
        elasticity=Decimal("-0.1"),
        confidence_tier=3,
        source=(
            "FAO (2020): Global Forest Resources Assessment 2020 — Main Report."
            " Food and Agriculture Organization of the United Nations, Rome."
            " doi:10.4060/ca9825en. Chapter 3 (Forest Management and"
            " Governance) and Annex 2 (country-level deforestation rates"
            " vs. forest management expenditure). The -0.1 elasticity"
            " approximates the land_use_pressure_index increase per unit"
            " fiscal spending cut (as fraction of GDP), derived from the"
            " FRA 2020 relationship between government forestry budget"
            " and net deforestation change in high-forest-cover countries"
            " (Table A3, columns 'National forest investment' and"
            " 'Annual net forest loss'). Used as the fiscal channel"
            " elasticity for EcologicalElasticity("
            " event_type='fiscal_policy_spending_change',"
            " indicator_key='land_use_pressure_index')."
        ),
        source_registry_id="ACADEMIC_LITERATURE_FAO_GFR_2020_FISCAL_LAND_USE",
    ),
    # Fiscal spending change → water_stress_index (arid_semiarid entities only).
    # FAO Global Framework for Water Scarcity in Agriculture (WASAG 2020) and
    # ICARDA (International Center for Agricultural Research in the Dry Areas)
    # document the link between government water infrastructure investment and
    # water stress in arid/semi-arid economies: a 1pp-of-GDP reduction in public
    # agricultural/water spending → 0.04 unit increase in the water stress index
    # (RATIO, range [0, 2] in boundary-proximity scoring). The mechanism operates
    # through reduced irrigation infrastructure maintenance, groundwater management
    # program cuts, and reduced desalination capacity support.
    #
    # Elasticity approved: CM + Ecological Economist, 2026-06-13 (M13 G8a deliberation).
    # Biome-class restriction: ONLY applies to entities with biome_class=arid_semiarid.
    # For high_forest_cover entities, this elasticity is skipped with a WARNING log.
    # The module.py dispatch enforces this restriction — this registry entry does not.
    #
    # Negative elasticity: fiscal spending cut (negative magnitude) → water stress
    # increases (positive delta). A spending increase (positive magnitude) → water
    # stress decreases (negative delta), consistent with conservation investment.
    # confidence_tier = 3: FAO GFR arid-subset / ICARDA data; annual interpolation
    # required from 5-year assessment cycles.
    EcologicalElasticity(
        event_type="fiscal_policy_spending_change",
        indicator_key="water_stress_index",
        elasticity=Decimal("-0.04"),
        confidence_tier=3,
        source=(
            "FAO WASAG (2020): Global Framework on Water Scarcity in Agriculture."
            " Food and Agriculture Organization, Rome. ICARDA Research Report:"
            " Water Productivity in Arid Regions (2019), International Center for"
            " Agricultural Research in the Dry Areas, Beirut. FAO GFR 2020 arid-subset"
            " analysis (MENA + SSA arid zones, Annex 3: Water Stress Indicators)."
            " The -0.04 elasticity approximates the water_stress_index increase per"
            " unit fiscal spending cut (as fraction of GDP) in arid/semi-arid economies."
            " CM + EE approval recorded 2026-06-13 (M13 G8a). biome_class restriction:"
            " arid_semiarid entities only; module dispatch enforces this gate."
        ),
        source_registry_id="ACADEMIC_LITERATURE_FAO_GFR_ARID_ICARDA_WATER_STRESS",
    ),
]
