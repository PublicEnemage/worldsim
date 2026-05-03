"""Unit tests for backtesting threshold evaluation logic — Issue #194.

Coverage:
  1.  VALID_THRESHOLD_TYPES contains all three required types.
  2.  evaluate_direction_only: negative direction + negative value → True.
  3.  evaluate_direction_only: negative direction + positive value → False.
  4.  evaluate_direction_only: negative direction + zero value → False.
  5.  evaluate_direction_only: positive direction + positive value → True.
  6.  evaluate_direction_only: positive direction + negative value → False.
  7.  evaluate_direction_only: unknown direction raises ValueError.
  8.  evaluate_magnitude: value within tolerance → True.
  9.  evaluate_magnitude: value at exact tolerance boundary → True.
  10. evaluate_magnitude: value beyond tolerance → False.
  11. evaluate_magnitude: zero expected_value, non-zero simulated → False.
  12. evaluate_magnitude: zero expected_value, zero simulated → True.
  13. evaluate_distribution_combined: both conditions pass → True.
  14. evaluate_distribution_combined: mean ok, actual outside CI → False.
  15. evaluate_distribution_combined: actual in CI, mean not ok → False.
  16. evaluate_distribution_combined: both fail → False.
  17. evaluate_distribution_combined: actual at exact CI lower bound → True.
  18. evaluate_distribution_combined: actual at exact CI upper bound → True.
  19. All evaluation functions accept Decimal inputs (no float leakage).
  20. evaluate_magnitude: Decimal arithmetic used (result is not float).
"""
from __future__ import annotations

from decimal import Decimal

import pytest

from app.simulation.backtesting.threshold_types import (
    VALID_THRESHOLD_TYPES,
    evaluate_direction_only,
    evaluate_distribution_combined,
    evaluate_magnitude,
)

# ---------------------------------------------------------------------------
# VALID_THRESHOLD_TYPES
# ---------------------------------------------------------------------------


def test_valid_threshold_types_contains_direction_only() -> None:
    assert "DIRECTION_ONLY" in VALID_THRESHOLD_TYPES


def test_valid_threshold_types_contains_magnitude() -> None:
    assert "MAGNITUDE" in VALID_THRESHOLD_TYPES


def test_valid_threshold_types_contains_distribution_combined() -> None:
    assert "DISTRIBUTION_COMBINED" in VALID_THRESHOLD_TYPES


def test_valid_threshold_types_has_exactly_three_entries() -> None:
    assert len(VALID_THRESHOLD_TYPES) == 3


# ---------------------------------------------------------------------------
# evaluate_direction_only
# ---------------------------------------------------------------------------


def test_direction_only_negative_with_negative_value() -> None:
    assert evaluate_direction_only(Decimal("-0.05"), "negative") is True


def test_direction_only_negative_with_positive_value() -> None:
    assert evaluate_direction_only(Decimal("0.05"), "negative") is False


def test_direction_only_negative_with_zero_value() -> None:
    assert evaluate_direction_only(Decimal("0"), "negative") is False


def test_direction_only_positive_with_positive_value() -> None:
    assert evaluate_direction_only(Decimal("0.02"), "positive") is True


def test_direction_only_positive_with_negative_value() -> None:
    assert evaluate_direction_only(Decimal("-0.01"), "positive") is False


def test_direction_only_unknown_direction_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Unknown expected_direction"):
        evaluate_direction_only(Decimal("-0.05"), "sideways")


def test_direction_only_positive_with_zero_value() -> None:
    assert evaluate_direction_only(Decimal("0"), "positive") is False


# ---------------------------------------------------------------------------
# evaluate_magnitude
# ---------------------------------------------------------------------------


def test_magnitude_within_tolerance() -> None:
    # actual = -0.054, simulated = -0.050, tolerance = 20%
    # allowance = 0.054 × 0.20 = 0.0108; |delta| = 0.004 ≤ 0.0108
    assert evaluate_magnitude(
        Decimal("-0.050"), Decimal("-0.054"), Decimal("0.20")
    ) is True


def test_magnitude_at_exact_tolerance_boundary() -> None:
    # actual = -0.100, simulated = -0.080, tolerance = 20%
    # allowance = 0.100 × 0.20 = 0.020; |delta| = 0.020 = boundary
    assert evaluate_magnitude(
        Decimal("-0.080"), Decimal("-0.100"), Decimal("0.20")
    ) is True


def test_magnitude_beyond_tolerance() -> None:
    # actual = -0.054, simulated = -0.020, tolerance = 20%
    # allowance = 0.054 × 0.20 = 0.0108; |delta| = 0.034 > 0.0108
    assert evaluate_magnitude(
        Decimal("-0.020"), Decimal("-0.054"), Decimal("0.20")
    ) is False


def test_magnitude_zero_expected_nonzero_simulated() -> None:
    # allowance = 0 × 0.20 = 0; any non-zero simulated fails
    assert evaluate_magnitude(
        Decimal("0.001"), Decimal("0"), Decimal("0.20")
    ) is False


def test_magnitude_zero_expected_zero_simulated() -> None:
    assert evaluate_magnitude(
        Decimal("0"), Decimal("0"), Decimal("0.20")
    ) is True


def test_magnitude_result_is_bool_not_decimal() -> None:
    result = evaluate_magnitude(
        Decimal("-0.050"), Decimal("-0.054"), Decimal("0.20")
    )
    assert isinstance(result, bool)


def test_magnitude_handles_large_tolerance() -> None:
    # tolerance = 100%: any value within 100% of expected passes
    assert evaluate_magnitude(
        Decimal("-0.001"), Decimal("-0.054"), Decimal("1.00")
    ) is True


# ---------------------------------------------------------------------------
# evaluate_distribution_combined
# ---------------------------------------------------------------------------


def test_distribution_combined_both_pass() -> None:
    # sim_mean=-0.052, expected=-0.054, tolerance=20%, CI=[-0.065, -0.040]
    assert evaluate_distribution_combined(
        sim_mean=Decimal("-0.052"),
        sim_ci_lower=Decimal("-0.065"),
        sim_ci_upper=Decimal("-0.040"),
        expected_value=Decimal("-0.054"),
        tolerance_pct=Decimal("0.20"),
    ) is True


def test_distribution_combined_mean_ok_actual_outside_ci() -> None:
    # actual = -0.054 is outside CI = [-0.050, -0.010]
    assert evaluate_distribution_combined(
        sim_mean=Decimal("-0.052"),
        sim_ci_lower=Decimal("-0.050"),
        sim_ci_upper=Decimal("-0.010"),
        expected_value=Decimal("-0.054"),
        tolerance_pct=Decimal("0.20"),
    ) is False


def test_distribution_combined_actual_in_ci_mean_not_ok() -> None:
    # mean = -0.020 is far from expected = -0.054 (beyond 20% tolerance)
    assert evaluate_distribution_combined(
        sim_mean=Decimal("-0.020"),
        sim_ci_lower=Decimal("-0.080"),
        sim_ci_upper=Decimal("-0.010"),
        expected_value=Decimal("-0.054"),
        tolerance_pct=Decimal("0.20"),
    ) is False


def test_distribution_combined_both_fail() -> None:
    assert evaluate_distribution_combined(
        sim_mean=Decimal("-0.001"),
        sim_ci_lower=Decimal("-0.005"),
        sim_ci_upper=Decimal("-0.001"),
        expected_value=Decimal("-0.054"),
        tolerance_pct=Decimal("0.20"),
    ) is False


def test_distribution_combined_actual_at_ci_lower_bound() -> None:
    # actual exactly at lower bound is within CI → condition 2 passes
    assert evaluate_distribution_combined(
        sim_mean=Decimal("-0.052"),
        sim_ci_lower=Decimal("-0.054"),
        sim_ci_upper=Decimal("-0.040"),
        expected_value=Decimal("-0.054"),
        tolerance_pct=Decimal("0.20"),
    ) is True


def test_distribution_combined_actual_at_ci_upper_bound() -> None:
    assert evaluate_distribution_combined(
        sim_mean=Decimal("-0.052"),
        sim_ci_lower=Decimal("-0.065"),
        sim_ci_upper=Decimal("-0.054"),
        expected_value=Decimal("-0.054"),
        tolerance_pct=Decimal("0.20"),
    ) is True


def test_distribution_combined_result_is_bool() -> None:
    result = evaluate_distribution_combined(
        sim_mean=Decimal("-0.052"),
        sim_ci_lower=Decimal("-0.065"),
        sim_ci_upper=Decimal("-0.040"),
        expected_value=Decimal("-0.054"),
        tolerance_pct=Decimal("0.20"),
    )
    assert isinstance(result, bool)


def test_distribution_combined_accepts_decimal_inputs() -> None:
    # Verify no TypeError raised when all inputs are Decimal
    result = evaluate_distribution_combined(
        sim_mean=Decimal("-0.089"),
        sim_ci_lower=Decimal("-0.110"),
        sim_ci_upper=Decimal("-0.060"),
        expected_value=Decimal("-0.089"),
        tolerance_pct=Decimal("0.20"),
    )
    assert result is True
