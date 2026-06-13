"""Reversibility classification registry for simulation output indicators.

Every entry maps an attribute_key (the key used in SimulationEntity.attributes)
to a ReversibilityClassification. Modules producing these indicators set
Quantity.reversibility from this registry when constructing output Quantities.

Source: Domain Intelligence Council blind interview (2026-05-11), Issue #271.
Three of nine DIC members raised the absence of this classification independently:
Intergenerational Advocate (Q1), Development Economist (unprompted), Community
Resilience (unprompted).

Scope (G8a, M13): This registry establishes the classification policy. Display-layer
use of the reversibility field and MDA threshold recalibration for irreversible
indicators are deferred to M14.
"""

from app.simulation.engine.quantity import ReversibilityClassification

REVERSIBILITY_REGISTRY: dict[str, ReversibilityClassification] = {
    # --- IRREVERSIBLE ---
    # Mortality: deaths are permanent. Excess mortality above baseline does not
    # recover regardless of subsequent economic improvement.
    "maternal_mortality_ratio": ReversibilityClassification.IRREVERSIBLE,
    "child_mortality_rate": ReversibilityClassification.IRREVERSIBLE,
    "under_five_mortality_rate": ReversibilityClassification.IRREVERSIBLE,
    # School enrollment: a cohort that misses a grade level cannot be returned
    # to the same developmental baseline as peers who remained enrolled.
    "school_enrollment_rate": ReversibilityClassification.IRREVERSIBLE,
    "primary_school_completion_rate": ReversibilityClassification.IRREVERSIBLE,
    # Skilled emigration: human capital stock is permanently reduced when skilled
    # workers emigrate; historical evidence of full return is weak.
    "skilled_emigration_rate": ReversibilityClassification.IRREVERSIBLE,
    "net_migration_skilled": ReversibilityClassification.IRREVERSIBLE,
    # Ecosystem tipping points: ecosystem stocks that cross a tipping point (e.g.
    # severe soil degradation, fishery collapse) do not recover within policy-
    # relevant time horizons. Indicators that approach but have not crossed a
    # tipping point belong in DELAYED_RECOVERY.
    "ecosystem_degradation_index": ReversibilityClassification.IRREVERSIBLE,

    # --- DELAYED_RECOVERY ---
    # Community social capital: networks dissolve faster than they form; recovery
    # requires 5–15 years of sustained community reinvestment.
    "community_social_capital_index": ReversibilityClassification.DELAYED_RECOVERY,
    # Land-use pressure below tipping point: degradation is real but reversible
    # with sustained investment; above tipping point this would be IRREVERSIBLE.
    "land_use_pressure_index": ReversibilityClassification.DELAYED_RECOVERY,
    # Food insecurity: acute insecurity resolves, but child stunting from sustained
    # malnutrition compounds irreversibly; the aggregate indicator is DELAYED_RECOVERY.
    "food_insecurity_rate": ReversibilityClassification.DELAYED_RECOVERY,

    # --- RECOVERABLE ---
    # Financial and macroeconomic indicators recover with appropriate policy
    # intervention. Unemployment has a structural component (DELAYED_RECOVERY for
    # long-duration unemployment), but the aggregate rate is RECOVERABLE.
    "reserve_coverage_months": ReversibilityClassification.RECOVERABLE,
    "gdp_growth_rate": ReversibilityClassification.RECOVERABLE,
    "unemployment_rate": ReversibilityClassification.RECOVERABLE,
    "fiscal_balance_pct_gdp": ReversibilityClassification.RECOVERABLE,
    "debt_gdp_ratio": ReversibilityClassification.RECOVERABLE,
    "inflation_rate": ReversibilityClassification.RECOVERABLE,
    "current_account_balance_pct_gdp": ReversibilityClassification.RECOVERABLE,
    "exchange_rate_volatility": ReversibilityClassification.RECOVERABLE,
    "bottom_quintile_consumption_capacity": ReversibilityClassification.RECOVERABLE,
}
