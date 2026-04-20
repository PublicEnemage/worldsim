"""
Quantity type system — SCR-001, ADR-001 Amendment 1.

Every physical and economic measurement in the simulation is a Quantity.
Never raw float, never raw Decimal without a unit and provenance.

The VariableType enum determines propagation semantics:
  STOCK  — level at a point in time; absolute replacement on apply_delta
  FLOW   — change over a period; additive accumulation
  RATIO  — dimensionless fraction derived from other quantities; additive
  DIMENSIONLESS — index/score with no natural unit; module-defined update rule

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
    """

    value: Decimal
    unit: str
    variable_type: VariableType
    measurement_framework: MeasurementFramework | None = None
    observation_date: date | None = None
    source_id: str | None = None
    confidence_tier: int = 1


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
