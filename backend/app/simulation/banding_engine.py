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
# CalibrationStore — Bayesian posterior multiplier overrides (ADR-007 §8.2–§8.5)
# ---------------------------------------------------------------------------

_CALIBRATION_MULTIPLIERS: dict[int, Decimal] = {}


def set_calibration_multipliers(multipliers: dict[int, Decimal]) -> None:
    """Override active tier multipliers for calibrated posteriors.

    Tests call set_calibration_multipliers({}) in tearDown to restore defaults.
    Production registry entries set overrides after MAGNITUDE_MATCH + co-sign gate.
    """
    global _CALIBRATION_MULTIPLIERS
    _CALIBRATION_MULTIPLIERS = dict(multipliers)


def get_tier_multiplier(tier: int) -> Decimal:
    """Return active multiplier for tier: calibrated override if set, else structural prior."""
    if tier in _CALIBRATION_MULTIPLIERS:
        return _CALIBRATION_MULTIPLIERS[tier]
    return _TIER_MULTIPLIERS.get(tier, Decimal("1.0"))


# ---------------------------------------------------------------------------
# Correction factor (ADR-007 §8.4)
# ---------------------------------------------------------------------------

_C_TARGET = Decimal("0.80")
_CLAMP_MIN = Decimal("0.5")
_CLAMP_MAX = Decimal("2.0")
_C_MAG_FLOOR = Decimal("0.05")


def compute_correction_factor(c_mag: Decimal) -> tuple[Decimal, str]:
    """Compute κ = clamp(sqrt(C_target / max(C_mag, 0.05)), 0.5, 2.0).

    Returns (Decimal("1.0"), "EVIDENCE_INSUFFICIENT") when c_mag < C_MAG_FLOOR.
    """
    if c_mag < _C_MAG_FLOOR:
        return Decimal("1.0"), "EVIDENCE_INSUFFICIENT"
    raw_kappa = (_C_TARGET / max(c_mag, _C_MAG_FLOOR)).sqrt()
    kappa = max(_CLAMP_MIN, min(_CLAMP_MAX, raw_kappa))
    return kappa, "OK"


# ---------------------------------------------------------------------------
# BandResult dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BandResult:
    """Output of compute_band for a single framework point."""

    ci_lower: str | None            # Decimal-as-string; None when suppressed or null score
    ci_upper: str | None            # Decimal-as-string; None when suppressed or null score
    ci_coverage: float | None       # 0.80 or None
    is_pre_calibration: bool | None # True or None (None when suppressed)
    clipped_lower: bool             # True if max(natural_lower, raw_lower) fired
    clipped_upper: bool             # True if min(natural_upper, raw_upper) fired
    # Visible fields added M19 G3 #1537 — all defaulted for backwards compatibility
    band_method: str | None = None  # frozen enum; None only on null-score path
    is_meaningless: bool = False    # True when CI suppressed (full natural range)
    suppressed_reason: str | None = None  # human-readable suppression reason


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
            band_method=None,
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
            band_method=None,
        )

    natural_lower, natural_upper = _FRAMEWORK_BOUNDS[framework]

    base_hw = _base_half_width(step_index)
    multiplier = get_tier_multiplier(confidence_tier)
    half_width = base_hw * multiplier

    raw_lower = composite_score * (Decimal("1") - half_width)
    raw_upper = composite_score * (Decimal("1") + half_width)

    ci_lower = max(natural_lower, raw_lower)
    ci_upper = min(natural_upper, raw_upper)

    clipped_lower = ci_lower > raw_lower
    clipped_upper = ci_upper < raw_upper

    # ADR-007 §6 Implementation Clause (Amendment 1): meaninglessness threshold.
    # When the CI equals the full natural range at step >= 7, suppress. Use
    # equality on the clipped values rather than the clipped_* flags because
    # raw_upper can equal natural_upper exactly (e.g. score=0.4 × 2.5 = 1.0),
    # which leaves clipped_upper=False while the CI still spans [0, 1].
    if (
        step_index >= 7
        and ci_lower == natural_lower
        and ci_upper == natural_upper
    ):
        return BandResult(
            ci_lower=None,
            ci_upper=None,
            ci_coverage=None,
            is_pre_calibration=None,
            clipped_lower=True,
            clipped_upper=True,
            band_method="SUPPRESSED_MEANINGLESS",
            is_meaningless=True,
            suppressed_reason=(
                f"CI spans full natural range [{natural_lower}, {natural_upper}]"
                f" at step {step_index} T{confidence_tier} — directionally meaningless"
            ),
        )

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
        band_method="PRE_CALIBRATION_STRUCTURAL_PRIOR",
    )
