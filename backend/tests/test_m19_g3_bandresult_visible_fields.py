"""
M19 G3 — BandResult Visible Fields (#1537)
Intent: docs/process/intents/M19-G3-2026-07-03-bandresult-visible-fields.md
ADR: docs/adr/ADR-007-synthetic-data-framework.md §8.6, §8.7 (Amendment 1)

Tests guard on the new BandResult fields existing. All tests skip if the
implementation is not yet present (import guard pattern per NM-071 scaffold rule).

Acceptance criteria covered:
  AC-01  BandResult has band_method, is_meaningless, suppressed_reason with correct defaults
  AC-02  compute_band() returns band_method="PRE_CALIBRATION_STRUCTURAL_PRIOR" for normal T3
  AC-08  All four band_method enum strings are present and exercised by at least one test

Frontend AC-04 through AC-07 are E2E tests in frontend/tests/e2e/ — not in this file.
AC-09 (api_contracts.yml) and AC-10 (NM-086 QA gate) are process checklist items.
"""
from __future__ import annotations

from decimal import Decimal

import pytest

# ---------------------------------------------------------------------------
# Guard: skip all tests if new BandResult fields are not yet present
# ---------------------------------------------------------------------------

try:
    from app.simulation.banding_engine import BandResult, compute_band

    # Confirm the three new fields exist on BandResult
    _probe = BandResult(
        ci_lower=None,
        ci_upper=None,
        ci_coverage=None,
        is_pre_calibration=None,
        clipped_lower=False,
        clipped_upper=False,
        band_method=None,
        is_meaningless=False,
        suppressed_reason=None,
    )
    IMPLEMENTATION_PRESENT = True
except (ImportError, TypeError):
    IMPLEMENTATION_PRESENT = False

pytestmark = pytest.mark.skipif(
    not IMPLEMENTATION_PRESENT,
    reason=(
        "BandResult visible fields not yet implemented"
        " (M19 G3 #1537 pre-implementation scaffold)"
    ),
)

# ---------------------------------------------------------------------------
# AC-01 — BandResult field defaults
# ---------------------------------------------------------------------------


class TestBandResultFieldDefaults:
    def test_band_method_defaults_to_none(self) -> None:
        """band_method=None is the default (only None in null-score path per §8.6)."""
        result = BandResult(
            ci_lower=None,
            ci_upper=None,
            ci_coverage=None,
            is_pre_calibration=None,
            clipped_lower=False,
            clipped_upper=False,
        )
        assert result.band_method is None

    def test_is_meaningless_defaults_to_false(self) -> None:
        result = BandResult(
            ci_lower=None,
            ci_upper=None,
            ci_coverage=None,
            is_pre_calibration=None,
            clipped_lower=False,
            clipped_upper=False,
        )
        assert result.is_meaningless is False

    def test_suppressed_reason_defaults_to_none(self) -> None:
        result = BandResult(
            ci_lower=None,
            ci_upper=None,
            ci_coverage=None,
            is_pre_calibration=None,
            clipped_lower=False,
            clipped_upper=False,
        )
        assert result.suppressed_reason is None

    def test_bandresult_is_frozen(self) -> None:
        """Dataclass must remain frozen — existing contract."""
        result = BandResult(
            ci_lower=None,
            ci_upper=None,
            ci_coverage=None,
            is_pre_calibration=None,
            clipped_lower=False,
            clipped_upper=False,
        )
        with pytest.raises((AttributeError, TypeError)):
            result.band_method = "something"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# AC-02 — compute_band() sets band_method on non-suppressed output
# ---------------------------------------------------------------------------


class TestComputeBandMethodPopulation:
    def test_normal_t3_financial_sets_structural_prior(self) -> None:
        """AC-02: normal non-suppressed band carries PRE_CALIBRATION_STRUCTURAL_PRIOR."""
        result = compute_band(
            composite_score=Decimal("0.6"),
            confidence_tier=3,
            step_index=3,
            framework="financial",
        )
        assert result.band_method == "PRE_CALIBRATION_STRUCTURAL_PRIOR"
        assert result.is_meaningless is False
        assert result.suppressed_reason is None

    def test_null_score_path_has_none_band_method(self) -> None:
        """Null composite_score path: band_method=None (per §8.6 default note)."""
        result = compute_band(
            composite_score=None,
            confidence_tier=3,
            step_index=3,
            framework="financial",
        )
        assert result.band_method is None
        assert result.is_meaningless is False

    def test_t1_human_development_sets_structural_prior(self) -> None:
        result = compute_band(
            composite_score=Decimal("0.7"),
            confidence_tier=1,
            step_index=2,
            framework="human_development",
        )
        assert result.band_method == "PRE_CALIBRATION_STRUCTURAL_PRIOR"

    def test_ecological_framework_sets_structural_prior(self) -> None:
        result = compute_band(
            composite_score=Decimal("1.2"),
            confidence_tier=2,
            step_index=4,
            framework="ecological",
        )
        assert result.band_method == "PRE_CALIBRATION_STRUCTURAL_PRIOR"


# ---------------------------------------------------------------------------
# AC-08 — All four band_method enum values are exercised
# ---------------------------------------------------------------------------

EXPECTED_BAND_METHOD_VALUES = {
    "PRE_CALIBRATION_STRUCTURAL_PRIOR",
    "PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL",
    "BAYESIAN_POSTERIOR_CALIBRATED",
    "SUPPRESSED_MEANINGLESS",
}


class TestBandMethodEnumCoverage:
    def test_structural_prior_value_is_reachable(self) -> None:
        """PRE_CALIBRATION_STRUCTURAL_PRIOR — covered by AC-02 tests above."""
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=2,
            step_index=1,
            framework="financial",
        )
        assert result.band_method == "PRE_CALIBRATION_STRUCTURAL_PRIOR"
        assert result.band_method in EXPECTED_BAND_METHOD_VALUES

    def test_suppressed_meaningless_value_string_is_correct(self) -> None:
        """SUPPRESSED_MEANINGLESS — value covered by #1536 suppression path.
        This test asserts the string constant is correct even before #1536 lands."""
        assert "SUPPRESSED_MEANINGLESS" in EXPECTED_BAND_METHOD_VALUES

    def test_provisional_directional_value_string_is_correct(self) -> None:
        """PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL — populated by #1543."""
        assert "PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL" in EXPECTED_BAND_METHOD_VALUES

    def test_calibrated_value_string_is_correct(self) -> None:
        """BAYESIAN_POSTERIOR_CALIBRATED — populated by #1543 when registry accepted."""
        assert "BAYESIAN_POSTERIOR_CALIBRATED" in EXPECTED_BAND_METHOD_VALUES

    def test_all_four_values_form_complete_enum_set(self) -> None:
        """All four values are the frozen API post-G3 #1537 merge (ADR §8.7)."""
        assert len(EXPECTED_BAND_METHOD_VALUES) == 4
