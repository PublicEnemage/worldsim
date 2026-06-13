"""
Quantity type system — SCR-001, ADR-001 Amendment 1; AttributeType ADR-001 Amendment 2;
ReversibilityClassification Issue #271 (G8a, M13).

Every physical and economic measurement in the simulation is a Quantity.
Never raw float, never raw Decimal without a unit and provenance.

The VariableType enum determines propagation semantics:
  STOCK  — level at a point in time; absolute replacement on apply_delta
  FLOW   — change over a period; additive accumulation
  RATIO  — dimensionless fraction derived from other quantities; additive
  DIMENSIONLESS — index/score with no natural unit; module-defined update rule

AttributeType (Amendment 2, Issue #30) is a complementary economic-semantic tag:
  STOCK           — natural capital stock, debt stock, FX reserves (accumulated level)
  FLOW            — GDP, exports, deficit (change per period)
  STRUCTURAL_INDEX — governance quality, political stability (index, no natural unit)
  RATE            — rates per period (inflation rate, unemployment rate)

ReversibilityClassification (Issue #271) indicates whether damage from a shock heals:
  RECOVERABLE      — heals within 1–5 years with policy intervention
  DELAYED_RECOVERY — partial recovery over 5–15 years; sustained investment required
  IRREVERSIBLE     — does not recover within policy-relevant time horizons (< 25 years)

AttributeType and VariableType are complementary: VariableType drives propagation
behaviour; AttributeType annotates economic meaning for MDA classification and
ecological stock-depletion accounting. AttributeType is optional — None when the
economic class has not been determined.

confidence_tier propagation uses the lower-of-two rule — a deliberately
conservative policy approximation, not a statistical formula.

See CODING_STANDARDS.md § Monetary and Quantity Standards and
DATA_STANDARDS.md § Confidence Tier Propagation for full specification.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import date
    from decimal import Decimal

    from app.simulation.engine.models import MeasurementFramework


class AttributeType(str, Enum):
    """Economic-semantic classification of simulation attributes (ADR-001 Amendment 2, Issue #30).

    Complements VariableType, which drives propagation behaviour. AttributeType
    annotates the economic meaning for MDA classification, ecological stock-depletion
    accounting, and stock-flow identity validation.

    Use AttributeType.STOCK for accumulated levels (forest cover, debt stock, FX reserves).
    Use AttributeType.FLOW for per-period changes (GDP, exports, fiscal deficit).
    Use AttributeType.STRUCTURAL_INDEX for quality/governance indexes with no natural unit.
    Use AttributeType.RATE for rates per period (unemployment rate, inflation rate).
    """

    STOCK = "stock"
    """Accumulated level at a point in time. Natural capital stocks, debt outstanding,
    FX reserves. Stocks can be depleted below irreversible MDA thresholds."""

    FLOW = "flow"
    """Change or production over a period. GDP, exports, government spending.
    Flows drive stock updates via the stock-flow identity when stock_flow_identity=True."""

    STRUCTURAL_INDEX = "structural_index"
    """Quality index or composite score with no natural unit. Political stability,
    governance effectiveness, V-Dem indicators. Cannot be summed across entities."""

    RATE = "rate"
    """Rate per unit time. Unemployment rate, inflation rate, GDP growth rate.
    Expressed as a fraction (0.0–1.0) or annualised percentage."""


class VariableType(Enum):
    """Classification of simulation state variables by temporal semantics.

    The propagation engine uses this to determine whether a delta replaces
    the current value (STOCK) or accumulates on top of it (FLOW, RATIO,
    DIMENSIONLESS). Misclassification produces silent accumulation errors
    that are difficult to detect in multi-step simulations.
    """

    STOCK = "stock"
    """Level at a point in time. Examples: foreign exchange reserves, debt
    outstanding, population. Propagation: inherits previous period value if
    no event changes it; apply_delta replaces the current value."""

    FLOW = "flow"
    """Change over a period. Examples: GDP, exports, fiscal deficit.
    Propagation: accumulates additively within a timestep."""

    RATIO = "ratio"
    """Dimensionless fraction derived from other quantities.
    Examples: debt/GDP, inflation rate, reserve coverage months.
    Propagation: accumulates additively within a timestep."""

    DIMENSIONLESS = "dimensionless"
    """Index or score with no natural unit — not a ratio of two commensurable
    quantities. Examples: HDI, Freedom House score, V-Dem indicators,
    capability indexes (HCL outputs). Update rule defined by the owning module.
    Propagation: accumulates additively within a timestep.

    DIMENSIONLESS includes all index and score variables regardless of their
    conceptual richness. The classification describes storage behavior, not
    the significance of the variable. A capability index (HDI dimension, child
    mortality rate) is DIMENSIONLESS by this taxonomy and also a primary output
    with equal display weight to financial indicators — the classification does
    not diminish this."""

    PROBABILITY = "probability"
    """Probability value in [0.0, 1.0]. Replaces the current attribute value
    each step (same propagation semantics as STOCK — absolute replacement, not
    additive accumulation). Used for programme_survival_probability and similar
    point-in-time probability estimates (ADR-013)."""


class ReversibilityClassification(str, Enum):
    """Classification of whether damage represented by a simulation indicator heals.

    Distinguishes indicators where the damage caused by a shock recovers with
    economic stabilisation from indicators where the damage forecloses future
    options regardless of subsequent recovery.

    Source: Domain Intelligence Council blind interview (2026-05-11), Issue #271.
    Three of nine DIC members raised the absence of this classification
    independently. See docs/methodology/calibration-basis.md for the full
    rationale and REVERSIBILITY_REGISTRY in reversibility.py for the
    indicator-level assignments.

    The classification is a property of the indicator type, not of the shock
    magnitude. A recoverable indicator may still cause severe harm; the
    classification only addresses whether that harm persists after stabilisation.
    """

    RECOVERABLE = "recoverable"
    """Damage heals with economic stabilisation and appropriate policy intervention.
    Typical recovery horizon: 1–5 years. Examples: fiscal balance, FX reserves,
    GDP growth rate, unemployment rate (structural unemployment excluded)."""

    DELAYED_RECOVERY = "delayed_recovery"
    """Partial or slow recovery is possible but requires sustained investment and
    time well beyond the typical programme window. Typical recovery horizon: 5–15 years.
    Examples: community social capital networks, land-use pressure below tipping point."""

    IRREVERSIBLE = "irreversible"
    """Damage does not recover within policy-relevant time horizons (< 25 years)
    regardless of subsequent economic performance. Examples: mortality, permanent
    emigration of skilled workers, schooling gaps in children who did not complete
    a grade level, ecosystem stocks that crossed a tipping point."""


@dataclass(kw_only=True)
class Quantity:
    """A typed, attributed measurement carrying value, unit, and provenance.

    kw_only=True is required to allow MonetaryValue to add fields without
    Python dataclass inheritance ordering errors (see ARCH-3 in SCR-001).

    Attributes:
        value: The numerical amount. Always Decimal, never float.
        unit: Canonical unit string (e.g. 'USD_2015', 'dimensionless', 'km2').
            Use the string constants defined in DATA_STANDARDS.md.
        variable_type: STOCK, FLOW, RATIO, or DIMENSIONLESS. Required.
            The propagation engine uses this to apply deltas correctly.
        measurement_framework: Which accounting dimension this belongs to.
            None for quantities that cross frameworks (e.g. population).
        observation_date: Date of the underlying observation. None for
            synthetic or computed quantities without a historical anchor.
        source_id: Source registry identifier. None for derived quantities
            before the source tracking system is operational (Milestone 2+).
        confidence_tier: Data quality tier 1–5. See DATA_STANDARDS.md §
            Data Quality Tier System. Defaults to 1 (highest confidence).
            Must be set explicitly at ingestion — do not rely on the default
            for ingested data (ingestion pipeline requirement, SCR-001).
        attribute_type: Economic-semantic classification (ADR-001 Amendment 2,
            Issue #30). None when not yet classified. See AttributeType for values.
        stock_flow_identity: When True, the engine validates that the stock
            value satisfies stock[t+1] = stock[t] + net_flow[t], surfaced as a
            warning in Milestone 1. Only meaningful for STOCK attributes.
    """

    value: Decimal
    unit: str
    variable_type: VariableType
    measurement_framework: MeasurementFramework | None = None
    observation_date: date | None = None
    source_id: str | None = None
    confidence_tier: int = 1
    attribute_type: AttributeType | None = None
    stock_flow_identity: bool = False
    reversibility: ReversibilityClassification | None = None


@dataclass(kw_only=True)
class MonetaryValue(Quantity):
    """A Quantity that is specifically a monetary amount.

    Inherits from Quantity: value, unit, variable_type, measurement_framework,
    observation_date, source_id, confidence_tier.

    The inherited 'value' field is the monetary amount (replaces the former
    standalone 'amount' field from the pre-SCR-001 MonetaryValue definition).
    The inherited 'unit' field carries the canonical storage unit (USD_2015)
    or the source currency unit before conversion at ingestion time.

    'currency_code' is the ISO 4217 source currency — redundant with 'unit'
    for canonical values but required at ingestion before conversion so the
    pipeline can construct the correct Unit.

    See DATA_STANDARDS.md § Currency and Monetary Value Standards.
    """

    currency_code: str = ""       # ISO 4217, e.g. "USD", "EUR", "GHS"
    price_basis: str = ""         # "nominal", "constant", "ppp"
    exchange_rate_type: str = ""  # "official", "parallel", "ppp", "fixed"


def propagate_confidence(*quantities: Quantity) -> int:
    """Return the confidence tier for a value derived from the given inputs.

    Implements the lower-of-two rule: the output tier is the maximum of all
    input tier numbers (higher number = lower confidence quality; the output
    inherits the least reliable input's tier).

    The lower-of-two rule is a deliberately conservative policy approximation,
    not a statistical formula. It systematically overstates uncertainty when
    inputs are independent and mutually corroborating. This is the intended
    behavior: in a tool informing sovereign policy decisions, overstatement of
    uncertainty is the preferred failure mode over understatement.
    Code comments and documentation must not describe this rule as a statistical
    derivation. Where genuine statistical propagation of probability distributions
    is required (e.g., Monte Carlo uncertainty quantification), use the appropriate
    statistical method instead — this rule governs the confidence_tier integer
    field only.

    Known Limitation: This rule does not account for projection horizon.
    A 30-year forward projection derived from a Tier 1 historical observation
    retains Tier 1 confidence under this rule, which overstates reliability for
    long-horizon projections. Time-horizon confidence degradation (automatic tier
    downgrade based on projection distance from observation_date) is required
    Milestone 3 scope, to be implemented when the scenario engine first produces
    forward projections at scale. Until that implementation, modules producing
    forward projections must include in their output metadata the note:
    'Confidence tier does not account for projection horizon.'

    Args:
        *quantities: One or more Quantity inputs to a derived computation.

    Returns:
        The maximum confidence_tier across all inputs (highest tier number =
        lowest confidence quality — the conservative output inherits the least
        reliable input).
    """
    return max(q.confidence_tier for q in quantities)
