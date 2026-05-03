"""BacktestingThreshold evaluation logic — Issue #194 (ADR-006 Decision 11).

Three threshold types correspond to the `threshold_type` column in
`backtesting_thresholds`.  All arithmetic uses Decimal to avoid float drift.

  DIRECTION_ONLY:
    The simulated value's sign must match expected_direction ('negative' /
    'positive').  No magnitude assertion.  ci_coverage = NULL in the DB.

  MAGNITUDE:
    |simulated_value - expected_value| ≤ |expected_value| × tolerance_pct
    ci_coverage = NULL in the DB.

  DISTRIBUTION_COMBINED (ADR-006 Decision 11):
    Both conditions must hold:
      1. |sim_mean - expected_value| ≤ |expected_value| × tolerance_pct
      2. expected_value falls within [sim_ci_lower, sim_ci_upper]

    ci_coverage stored in the DB (e.g. 0.80) is a CONTRACT with the caller:
    the CI bounds supplied must correspond to that coverage fraction.
    Prevents a wide distribution centred on the right mean from passing when
    the historical actual falls in an extreme tail.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Literal

ThresholdType = Literal["DIRECTION_ONLY", "MAGNITUDE", "DISTRIBUTION_COMBINED"]

VALID_THRESHOLD_TYPES: frozenset[str] = frozenset({
    "DIRECTION_ONLY",
    "MAGNITUDE",
    "DISTRIBUTION_COMBINED",
})


def evaluate_direction_only(
    simulated_value: Decimal,
    expected_direction: str,
) -> bool:
    """True iff simulated_value's sign matches expected_direction."""
    if expected_direction == "negative":
        return simulated_value < Decimal("0")
    if expected_direction == "positive":
        return simulated_value > Decimal("0")
    raise ValueError(
        f"Unknown expected_direction: {expected_direction!r}. "
        "Must be 'negative' or 'positive'."
    )


def evaluate_magnitude(
    simulated_value: Decimal,
    expected_value: Decimal,
    tolerance_pct: Decimal,
) -> bool:
    """True iff |simulated_value - expected_value| ≤ |expected_value| × tolerance_pct."""
    allowance = abs(expected_value) * tolerance_pct
    return abs(simulated_value - expected_value) <= allowance


def evaluate_distribution_combined(
    sim_mean: Decimal,
    sim_ci_lower: Decimal,
    sim_ci_upper: Decimal,
    expected_value: Decimal,
    tolerance_pct: Decimal,
) -> bool:
    """True iff both distribution pass conditions hold.

    Condition 1: mean within ±tolerance_pct of expected_value (MAGNITUDE check).
    Condition 2: expected_value falls within [sim_ci_lower, sim_ci_upper].

    The caller is responsible for supplying CI bounds at the coverage fraction
    recorded in backtesting_thresholds.ci_coverage (e.g. the 80% CI bounds
    when ci_coverage = 0.80).
    """
    mean_ok = evaluate_magnitude(sim_mean, expected_value, tolerance_pct)
    ci_ok = sim_ci_lower <= expected_value <= sim_ci_upper
    return mean_ok and ci_ok
