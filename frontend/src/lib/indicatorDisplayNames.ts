// Indicator display name registry — frontend/src/lib/indicatorDisplayNames.ts
// Issue #317, ADR-005 Area 3: all indicator keys map to human-readable display
// names. No raw key is visible in any UI surface. Extension contract: add a new
// entry in the relevant framework block; no other file requires a change.

const INDICATOR_DISPLAY_NAMES: Record<string, Record<string, string>> = {
  financial: {
    gdp_growth: "GDP Growth",
    fiscal_balance_pct_gdp: "Fiscal Balance (% GDP)",
    inflation_rate: "Inflation Rate",
    unemployment_rate: "Unemployment Rate",
    reserve_coverage_months: "Reserve Coverage (months)",
    health_expenditure_pct_gdp: "Health Expenditure (% GDP)",
    net_enrollment_secondary: "Secondary School Enrollment",
    debt_gdp_ratio: "Debt-to-GDP Ratio",
    current_account_balance: "Current Account Balance",
    exchange_rate: "Exchange Rate",
    interest_rate: "Interest Rate",
    tax_revenue_pct_gdp: "Tax Revenue (% GDP)",
    export_growth: "Export Growth",
    import_growth: "Import Growth",
    foreign_reserves: "Foreign Reserves",
    credit_growth: "Credit Growth",
  },
  human_development: {
    bottom_quintile_consumption_capacity: "Bottom Quintile Consumption",
    poverty_headcount_ratio: "Poverty Headcount Ratio",
    gini_coefficient: "Gini Coefficient",
    life_expectancy: "Life Expectancy",
    infant_mortality_rate: "Infant Mortality Rate",
    maternal_mortality_rate: "Maternal Mortality Rate",
    literacy_rate: "Literacy Rate",
    school_enrollment_primary: "Primary School Enrollment",
    school_enrollment_secondary: "Secondary School Enrollment",
    net_enrollment_secondary: "Secondary Net Enrollment Rate",
    food_security_index: "Food Security Index",
    undernourishment_rate: "Undernourishment Rate",
    human_development_index: "Human Development Index",
    income_share_q1: "Income Share — Bottom Quintile",
    income_share_q5: "Income Share — Top Quintile",
    access_to_healthcare: "Access to Healthcare",
    access_to_clean_water: "Access to Clean Water",
    sanitation_coverage: "Sanitation Coverage",
  },
  ecological: {
    co2_concentration_ppm: "CO₂ Concentration (ppm)",
    land_use_pressure_index: "Land Use Pressure Index",
    planetary_boundary_co2_proximity: "CO₂ Boundary Proximity",
    planetary_boundary_land_use_proximity: "Land Use Boundary Proximity",
    deforestation_rate: "Deforestation Rate",
    biodiversity_loss_index: "Biodiversity Loss Index",
    freshwater_withdrawal_pct: "Freshwater Withdrawal (%)",
    ocean_acidification_index: "Ocean Acidification Index",
    nitrogen_cycle_loading: "Nitrogen Cycle Loading",
    phosphorus_cycle_loading: "Phosphorus Cycle Loading",
    aerosol_optical_depth: "Aerosol Optical Depth",
    stratospheric_ozone_depletion: "Ozone Depletion",
    chemical_pollution_index: "Chemical Pollution Index",
    novel_entities_index: "Novel Entities Index",
  },
  governance: {
    rule_of_law_percentile: "Rule of Law (percentile)",
    democratic_quality_score: "Democratic Quality Score",
    government_effectiveness: "Government Effectiveness",
    regulatory_quality: "Regulatory Quality",
    control_of_corruption: "Control of Corruption",
    voice_and_accountability: "Voice and Accountability",
    political_stability: "Political Stability",
    press_freedom_index: "Press Freedom Index",
    judicial_independence: "Judicial Independence",
    transparency_index: "Transparency Index",
  },
};

function formatFallback(key: string): string {
  return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function getIndicatorDisplayName(framework: string, key: string): string {
  return INDICATOR_DISPLAY_NAMES[framework]?.[key] ?? formatFallback(key);
}

/** Framework-agnostic lookup — returns the first matching display name across all
 *  framework blocks, falling back to title-cased key. Used by surfaces that have
 *  the attribute key but not the framework (e.g. AttributeSelector). */
export function getIndicatorDisplayNameAny(key: string): string {
  for (const block of Object.values(INDICATOR_DISPLAY_NAMES)) {
    if (key in block) return block[key];
  }
  return formatFallback(key);
}

/**
 * 24-character abbreviation set for compact Zone 1B alert rows (ADR-015 §Component 1).
 * Names that already fit within 24 chars use their full display name.
 * Keys not present fall back to truncateIndicatorName(getIndicatorDisplayNameAny(key), 24).
 */
const INDICATOR_ABBREV_24: Record<string, string> = {
  reserve_coverage_months:              "Reserve Coverage",
  debt_gdp_ratio:                       "Debt-to-GDP Ratio",
  poverty_headcount_ratio:              "Poverty Headcount Ratio",
  food_insecurity_rate:                 "Food Insecurity Rate",
  health_index:                         "Health Index",
  planetary_boundary_co2_proximity:     "CO₂ Boundary Proximity",
  planetary_boundary_land_use_proximity:"Land Use Boundary Prox.",
  programme_survival_probability:       "Prog. Survival Prob.",
  unemployment_rate:                    "Unemployment Rate",
  bottom_quintile_consumption_capacity: "Bottom Quintile Consump.",
  fiscal_balance_pct_gdp:               "Fiscal Balance % GDP",
  inflation_rate:                       "Inflation Rate",
  current_account_balance:              "Current Account Balance",
  gdp_growth:                           "GDP Growth",
};

/**
 * Returns the 24-char compact abbreviation for Zone 1B rows.
 * Prefers the INDICATOR_ABBREV_24 registry; falls back to a standard truncation.
 */
export function getIndicatorAbbreviation(key: string, maxChars = 24): string {
  if (key in INDICATOR_ABBREV_24) return INDICATOR_ABBREV_24[key];
  const full = getIndicatorDisplayNameAny(key);
  if (full.length <= maxChars) return full;
  return full.slice(0, maxChars - 1) + "…";
}
