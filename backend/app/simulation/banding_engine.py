"""BandingEngine — 80% CI computation for trajectory framework points.

Authority: DATA_STANDARDS.md §Band Schedule and Tier Multipliers,
           §BandingEngine Is the Sole Source, §Attribute Boundary Classification.
Intent doc: docs/process/intents/M18-G1-2026-06-26-ci-bands-zone-1a.md §3.
Issue: #1254.

Band schedule:
  step_index 1     → base half-width 0.10
  step_index 2     → base half-width 0.20
  step_index 3–5   → base half-width 0.35
  step_index > 5   → base half-width 0.50

Tier multipliers:
  T1 → 1.0 | T2 → 1.2 | T3 → 1.5 | T4 → 2.0 | T5 → 3.0

half_width = base_half_width × tier_multiplier
ci_lower   = max(natural_lower, composite_score × (1 - half_width))
ci_upper   = min(natural_upper, composite_score × (1 + half_width))
ci_coverage = 0.80 throughout M18
is_pre_calibration = True throughout M18 (MAGNITUDE_WITHIN_20PCT not yet confirmed)

Governance framework: composite_score is null throughout M18 → no band produced.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

# ---------------------------------------------------------------------------
# Framework natural boundaries (DATA_STANDARDS.md §Attribute Boundary Classification)
# ---------------------------------------------------------------------------

_FRAMEWORK_BOUNDS: dict[str, tuple[Decimal, Decimal]] = {
    "financial":        (Decimal("0.0"), Decimal("1.0")),
    "human_development": (Decimal("0.0"), Decimal("1.0")),
    "ecological":       (Decimal("0.0"), Decimal("2.0")),
    # governance: composite_score = null throughout M18 → compute_band returns null band
}

# ---------------------------------------------------------------------------
# Band schedule (horizon → base half-width)
# ---------------------------------------------------------------------------

def _base_half_width(step_index: int) -> Decimal:
    if step_index == 1:
        return Decimal("0.10")
    if step_index == 2:
        return Decimal("0.20")
    if step_index <= 5:
        return Decimal("0.35")
    return Decimal("0.50")


# ---------------------------------------------------------------------------
# Tier multipliers
# ---------------------------------------------------------------------------

_TIER_MULTIPLIERS: dict[int, Decimal] = {
    1: Decimal("1.0"),
    2: Decimal("1.2"),
    3: Decimal("1.5"),
    4: Decimal("2.0"),
    5: Decimal("3.0"),
}


def _tier_multiplier(confidence_tier: int) -> Decimal:
    return _TIER_MULTIPLIERS.get(confidence_tier, Decimal("1.0"))


# ---------------------------------------------------------------------------
# BandResult dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BandResult:
    """Output of compute_band for a single framework point."""

    ci_lower: str | None            # Decimal-as-string; None when composite_score is None
    ci_upper: str | None            # Decimal-as-string; None when composite_score is None
    ci_coverage: float | None       # 0.80 or None
    is_pre_calibration: bool | None # True or None
    clipped_lower: bool                # True if max(natural_lower, raw_lower) fired
    clipped_upper: bool                # True if min(natural_upper, raw_upper) fired


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compute_band(
    composite_score: Decimal | None,
    confidence_tier: int,
    step_index: int,
    framework: str,
) -> BandResult:
    """Compute the 80% CI band for a single TrajectoryFrameworkPoint.

    Returns a BandResult with all fields None when composite_score is None
    (governance framework throughout M18, or any framework where the score
    could not be computed).
    """
    if composite_score is None:
        return BandResult(
            ci_lower=None,
            ci_upper=None,
            ci_coverage=None,
            is_pre_calibration=None,
            clipped_lower=False,
            clipped_upper=False,
        )

    if framework not in _FRAMEWORK_BOUNDS:
        # Unknown framework (e.g. governance with null score never reaches here,
        # but a future framework without bounds should produce a null band).
        return BandResult(
            ci_lower=None,
            ci_upper=None,
            ci_coverage=None,
            is_pre_calibration=None,
            clipped_lower=False,
            clipped_upper=False,
        )

    natural_lower, natural_upper = _FRAMEWORK_BOUNDS[framework]

    base_hw = _base_half_width(step_index)
    multiplier = _tier_multiplier(confidence_tier)
    half_width = base_hw * multiplier

    raw_lower = composite_score * (Decimal("1") - half_width)
    raw_upper = composite_score * (Decimal("1") + half_width)

    ci_lower = max(natural_lower, raw_lower)
    ci_upper = min(natural_upper, raw_upper)

    clipped_lower = ci_lower > raw_lower
    clipped_upper = ci_upper < raw_upper

    # Quantize to 4 decimal places (consistent with composite_score precision)
    quantizer = Decimal("0.0001")
    ci_lower_str = str(ci_lower.quantize(quantizer, rounding=ROUND_HALF_UP))
    ci_upper_str = str(ci_upper.quantize(quantizer, rounding=ROUND_HALF_UP))

    return BandResult(
        ci_lower=ci_lower_str,
        ci_upper=ci_upper_str,
        ci_coverage=0.80,
        is_pre_calibration=True,
        clipped_lower=clipped_lower,
        clipped_upper=clipped_upper,
    )
