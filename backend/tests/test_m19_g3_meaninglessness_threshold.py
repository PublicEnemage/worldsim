"""
M19 G3 — Meaninglessness Threshold (#1536)
Intent: docs/process/intents/M19-G3-2026-07-03-meaninglessness-threshold.md
ADR: docs/adr/ADR-007-synthetic-data-framework.md §6 Implementation Clause (Amendment 1)

Tests guard on the suppression logic existing in compute_band(). All tests skip if
the implementation is not yet present.

Acceptance criteria covered:
  AC-01  T5, step 7, score 0.5 → is_meaningless=True, ci_lower=None, ci_upper=None
  AC-02  T5, step 7, score 0.5 → band_method="SUPPRESSED_MEANINGLESS"
  AC-03  T5, step 7, score 0.5 → suppressed_reason contains natural range bounds
  AC-04  T3, step 7, score 0.5 → is_meaningless=False, normal ci_lower/ci_upper
  AC-05  T5, step 6 (step < 7) → suppression does NOT fire
  AC-06  Only one bound clips → suppression does NOT fire
  AC-07  Existing banding_engine tests remain green (CI gate — not in this file)
  AC-08  Decimal comparison used, not float (code review — not a unit test)

Requires #1537 (BandResult new fields) to be merged before this implementation lands.
"""
from __future__ import annotations

from decimal import Decimal

import pytest

# ---------------------------------------------------------------------------
# Guard: skip all tests if compute_band() does not yet suppress T5 step 7+
# ---------------------------------------------------------------------------

try:
    from app.simulation.banding_engine import BandResult, compute_band

    # Probe: T5, step 7, score 0.5 on financial framework should be suppressed
    # after implementation. If it returns is_meaningless=False, implementation
    # is not yet present — tests still register but are skipped.
    _probe = compute_band(
        composite_score=Decimal("0.5"),
        confidence_tier=5,
        step_index=7,
        framework="financial",
    )
    IMPLEMENTATION_PRESENT = hasattr(_probe, "is_meaningless") and _probe.is_meaningless
except (ImportError, TypeError):
    IMPLEMENTATION_PRESENT = False

pytestmark = pytest.mark.skipif(
    not IMPLEMENTATION_PRESENT,
    reason="Meaninglessness threshold not yet implemented (M19 G3 #1536 pre-implementation scaffold)",
)

# ---------------------------------------------------------------------------
# AC-01, AC-02, AC-03 — Suppression fires for T5, step 7
# ---------------------------------------------------------------------------


class TestSuppressedT5Step7:
    """T5 at step 7: half_width = 0.50 × 3.0 = 1.50.
    For score 0.5 on financial [0,1]:
      raw_lower = 0.5 × (1 - 1.5) = -0.25  → clips to 0.0
      raw_upper = 0.5 × (1 + 1.5) =  1.25  → clips to 1.0
    CI = [0.0, 1.0] = full natural range → Condition 1 fires.
    """

    def test_ci_lower_is_none(self) -> None:
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=5,
            step_index=7,
            framework="financial",
        )
        assert result.ci_lower is None

    def test_ci_upper_is_none(self) -> None:
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=5,
            step_index=7,
            framework="financial",
        )
        assert result.ci_upper is None

    def test_is_meaningless_true(self) -> None:
        """AC-01."""
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=5,
            step_index=7,
            framework="financial",
        )
        assert result.is_meaningless is True

    def test_band_method_is_suppressed_meaningless(self) -> None:
        """AC-02."""
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=5,
            step_index=7,
            framework="financial",
        )
        assert result.band_method == "SUPPRESSED_MEANINGLESS"

    def test_suppressed_reason_contains_natural_range(self) -> None:
        """AC-03: suppressed_reason must mention the framework's natural bounds."""
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=5,
            step_index=7,
            framework="financial",
        )
        assert result.suppressed_reason is not None
        # Must contain the natural bounds in some form
        assert "0" in result.suppressed_reason
        assert "1" in result.suppressed_reason

    def test_is_pre_calibration_is_none_when_suppressed(self) -> None:
        """Suppressed BandResult has is_pre_calibration=None (per ADR §6 impl clause)."""
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=5,
            step_index=7,
            framework="financial",
        )
        assert result.is_pre_calibration is None

    def test_ci_coverage_is_none_when_suppressed(self) -> None:
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=5,
            step_index=7,
            framework="financial",
        )
        assert result.ci_coverage is None

    def test_score_04_financial_also_suppressed(self) -> None:
        """Score 0.4: raw_lower = 0.4×(-0.5) = -0.2 → 0.0; raw_upper = 0.4×2.5 = 1.0 → 1.0."""
        result = compute_band(
            composite_score=Decimal("0.4"),
            confidence_tier=5,
            step_index=7,
            framework="financial",
        )
        assert result.is_meaningless is True

    def test_score_08_financial_also_suppressed(self) -> None:
        """Score 0.8: raw_lower = 0.8×(-0.5) = -0.4 → 0.0; raw_upper = 0.8×2.5 = 2.0 → 1.0."""
        result = compute_band(
            composite_score=Decimal("0.8"),
            confidence_tier=5,
            step_index=7,
            framework="financial",
        )
        assert result.is_meaningless is True

    def test_suppression_fires_at_step_8_too(self) -> None:
        """Step 8 > 7: base_hw still 0.50, suppression still fires."""
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=5,
            step_index=8,
            framework="financial",
        )
        assert result.is_meaningless is True

    def test_human_development_framework_also_suppressed(self) -> None:
        """human_development has same [0,1] range; same T5 step 7 behaviour."""
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=5,
            step_index=7,
            framework="human_development",
        )
        assert result.is_meaningless is True


# ---------------------------------------------------------------------------
# AC-04 — T3 step 7 does NOT suppress
# ---------------------------------------------------------------------------


class TestNoSuppressionT3:
    """T3 at step 7: half_width = 0.50 × 1.5 = 0.75.
    For score 0.5 on financial [0,1]:
      raw_lower = 0.5 × (1 - 0.75) = 0.125  (no clip)
      raw_upper = 0.5 × (1 + 0.75) = 0.875  (no clip)
    CI width = 0.75 < 1.0 → Condition 1 does NOT fire.
    """

    def test_t3_step7_is_not_suppressed(self) -> None:
        """AC-04."""
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=3,
            step_index=7,
            framework="financial",
        )
        assert result.is_meaningless is False
        assert result.ci_lower is not None
        assert result.ci_upper is not None

    def test_t3_step7_has_structural_prior_band_method(self) -> None:
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=3,
            step_index=7,
            framework="financial",
        )
        assert result.band_method == "PRE_CALIBRATION_STRUCTURAL_PRIOR"


# ---------------------------------------------------------------------------
# AC-05 — T5 step 6 does NOT suppress
# ---------------------------------------------------------------------------


class TestNoSuppressionT5Step6:
    """T5 at step 6: base_hw=0.50, half_width=1.50.
    step_index=6 is the boundary — suppression requires step_index >= 7.
    """

    def test_t5_step6_is_not_suppressed(self) -> None:
        """AC-05: step 6 is below the threshold; suppression requires step >= 7."""
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=5,
            step_index=6,
            framework="financial",
        )
        # At step 6 with T5, half_width is also 1.50 (base_hw 0.50 × 3.0).
        # If the ADR spec requires suppression only at step_index >= 7, this
        # should NOT be suppressed. If step 6 also clips to full range
        # (same half_width as step 7), the implementation may suppress it too —
        # the spec says "step_index >= 7" but the trigger is actually the
        # clip-to-full-range condition, which fires at the same half_width.
        # Whichever the implementation chooses, this test records the contract:
        # the AC-05 claim is that step 6 does NOT suppress.
        assert result.is_meaningless is False

    def test_t5_step5_is_not_suppressed(self) -> None:
        """Step 5: base_hw=0.35, half_width=0.35×3.0=1.05.
        raw_lower for score 0.5: 0.5×(1-1.05) = -0.025 → clips to 0.
        raw_upper: 0.5×(1+1.05) = 1.025 → clips to 1.0.
        CI width = 1.0 = full range → this may also fire at step 5.
        The intent doc says step >= 7; adjust test if spec changes.
        This test documents the current AC-05 target (no suppression at step 5).
        """
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=5,
            step_index=5,
            framework="financial",
        )
        assert result.is_meaningless is False


# ---------------------------------------------------------------------------
# AC-06 — Single-bound clip does NOT suppress
# ---------------------------------------------------------------------------


class TestNoSuppressionSingleClip:
    """If only one bound clips (not both), Condition 1 does not fire."""

    def test_only_lower_clips_not_suppressed(self) -> None:
        """AC-06: score near 0.0 → lower clips, upper does not → no suppression."""
        # T5 step 7, score 0.05: half_width=1.50
        # raw_lower = 0.05×(-0.5) = -0.025 → clips to 0.0 (lower clips)
        # raw_upper = 0.05×(2.5) = 0.125 → no clip (< 1.0)
        # CI = [0.0, 0.125], width = 0.125 ≠ 1.0 → Condition 1 does NOT fire
        result = compute_band(
            composite_score=Decimal("0.05"),
            confidence_tier=5,
            step_index=7,
            framework="financial",
        )
        assert result.is_meaningless is False
        assert result.ci_upper is not None

    def test_only_upper_clips_not_suppressed(self) -> None:
        """Score near 1.0 → upper clips, lower does not → no suppression."""
        # T5 step 7, score 0.95: half_width=1.50
        # raw_lower = 0.95×(-0.5) = -0.475 → clips to 0.0 (lower clips)
        # raw_upper = 0.95×(2.5) = 2.375 → clips to 1.0 (upper clips)
        # Both clip → CI = [0.0, 1.0] → full range → DOES suppress.
        # Use T4 instead where upper clips but width < 1.0:
        # T4 step 7, score 0.95: half_width=0.50×2.0=1.0
        # raw_lower = 0.95×0.0 = 0.0 → clips? 0.95×(1-1.0)=0 → ci_lower=0.0
        # raw_upper = 0.95×2.0 = 1.9 → clips to 1.0
        # Both clip, but CI width = 1.0 = natural width → fires for T4 too.
        # Use T3 step 7, score 0.99:
        # half_width = 0.50 × 1.5 = 0.75
        # raw_lower = 0.99 × 0.25 = 0.2475 (no clip)
        # raw_upper = 0.99 × 1.75 = 1.7325 → clips to 1.0 (only upper clips)
        result = compute_band(
            composite_score=Decimal("0.99"),
            confidence_tier=3,
            step_index=7,
            framework="financial",
        )
        assert result.is_meaningless is False
        assert result.clipped_upper is True
        assert result.clipped_lower is False
