"""
M19 G3 — Bayesian Posterior Layer (#1543)
Intent: docs/process/intents/M19-G3-2026-07-03-bayesian-posterior.md
ADR: docs/adr/ADR-007-synthetic-data-framework.md §8.2–§8.5, §8.8 (Amendment 1)

Pre-implementation scaffold. All tests skip unless the implementation is present.

Acceptance criteria covered:
  AC-01  Synthetic MAGNITUDE_MATCH run → FidelityTier.MAGNITUDE_MATCH
  AC-02  Synthetic DIRECTION_ONLY run → FidelityTier.DIRECTION_ONLY
  AC-03  Catastrophic outlier (>5× hist) blocks MAGNITUDE_MATCH
  AC-04  < 5 valid pairs → DIRECTION_ONLY regardless of coverage
  AC-05  compute_correction_factor(Decimal("0.03")) → EVIDENCE_INSUFFICIENT
  AC-06  compute_correction_factor(Decimal("0.60")) → kappa ∈ [0.5, 2.0]
  AC-07  set_calibration_multipliers() overrides compute_band() multiplier
  AC-08  docs/backtesting/calibration-registry.md exists with CAL-001 entry
  AC-09  SEN registry entry has affected_indicators_excluded field
  AC-10  No code path returns is_pre_calibration=False without accepted registry
  AC-11  CM pre-merge gate (process — not a unit test; documented below)

CM pre-merge review gate (NM-084): CE activates CM after implementation is
complete → CM posts sign-off on #1543 → PI Agent posts gate comment → CE sets
auto-merge. Auto-merge must NOT be set without PI Agent gate comment.
"""
from __future__ import annotations

import os
from decimal import Decimal
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Guard: skip all tests if the calibration module is not yet present
# ---------------------------------------------------------------------------

try:
    from app.harness.mode3_harness import FidelityTier, _classify_fidelity

    # CalibrationStore components may live in banding_engine or calibration.py
    try:
        from app.simulation.calibration import compute_correction_factor
    except ImportError:
        from app.simulation.banding_engine import (
            compute_correction_factor,  # type: ignore[no-redef]
        )

    from app.simulation.banding_engine import (
        compute_band,
        get_tier_multiplier,
        set_calibration_multipliers,
    )

    # Probe: MAGNITUDE_MATCH must be a member of FidelityTier
    _ = FidelityTier.MAGNITUDE_MATCH
    # Probe: function must accept per_step_records with hist_value key (CE Condition A)
    _probe_records = [
        {"model_value": Decimal("0.5"), "hist_value": Decimal("0.5")}
    ] * 5
    _probe_result = _classify_fidelity(_probe_records)
    IMPLEMENTATION_PRESENT = True
except (ImportError, AttributeError, TypeError):
    IMPLEMENTATION_PRESENT = False

pytestmark = pytest.mark.skipif(
    not IMPLEMENTATION_PRESENT,
    reason=(
        "Bayesian posterior layer not yet implemented"
        " (M19 G3 #1543 pre-implementation scaffold)"
    ),
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_within_records(n: int, model: str = "0.50", hist: str = "0.50") -> list[dict]:
    """Build n records where model is within 20% of hist."""
    return [
        {"model_value": Decimal(model), "hist_value": Decimal(hist)}
        for _ in range(n)
    ]


def _make_outside_records(n: int) -> list[dict]:
    """Build n records where |model - hist| / max(|hist|, 0.01) > 0.20."""
    # model = 0.90, hist = 0.50 → deviation = 0.40/0.50 = 0.80 > 0.20
    return [
        {"model_value": Decimal("0.90"), "hist_value": Decimal("0.50")}
        for _ in range(n)
    ]


# ---------------------------------------------------------------------------
# AC-01 — MAGNITUDE_MATCH when ≥5 pairs all within 20%
# ---------------------------------------------------------------------------


class TestMagnitudeMatchGate:
    def test_all_within_20pct_achieves_magnitude_match(self) -> None:
        """AC-01: 10 pairs, all within 20% → MAGNITUDE_MATCH."""
        records = _make_within_records(10)
        tier, _ = _classify_fidelity(records)
        assert tier == FidelityTier.MAGNITUDE_MATCH

    def test_five_pairs_minimum_achieves_magnitude_match(self) -> None:
        """AC-01: Exactly 5 valid pairs within 20% → MAGNITUDE_MATCH."""
        records = _make_within_records(5)
        tier, _ = _classify_fidelity(records)
        assert tier == FidelityTier.MAGNITUDE_MATCH

    def test_exactly_50pct_within_achieves_magnitude_match(self) -> None:
        """≥50% threshold is inclusive: 5/10 within → MAGNITUDE_MATCH."""
        within = _make_within_records(5)
        outside = _make_outside_records(5)
        records = within + outside
        tier, _ = _classify_fidelity(records)
        assert tier == FidelityTier.MAGNITUDE_MATCH

    def test_boundary_20pct_is_inclusive(self) -> None:
        """Deviation exactly 0.20 satisfies ≤0.20 → counts as within."""
        # hist=0.50, model=0.60 → |0.60-0.50|/0.50 = 0.20 exactly
        records = [
            {"model_value": Decimal("0.60"), "hist_value": Decimal("0.50")}
            for _ in range(6)
        ]
        tier, _ = _classify_fidelity(records)
        assert tier == FidelityTier.MAGNITUDE_MATCH


# ---------------------------------------------------------------------------
# AC-02 — DIRECTION_ONLY when <50% within 20%
# ---------------------------------------------------------------------------


class TestDirectionOnlyGate:
    def test_below_50pct_within_gives_direction_only(self) -> None:
        """AC-02: 4/10 within 20% → DIRECTION_ONLY."""
        within = _make_within_records(4)
        outside = _make_outside_records(6)
        records = within + outside
        tier, _ = _classify_fidelity(records)
        assert tier == FidelityTier.DIRECTION_ONLY

    def test_zero_within_gives_direction_only(self) -> None:
        """0/5 within → DIRECTION_ONLY."""
        records = _make_outside_records(5)
        tier, _ = _classify_fidelity(records)
        assert tier == FidelityTier.DIRECTION_ONLY

    def test_hist_value_none_records_excluded_from_count(self) -> None:
        """Records with hist_value=None are excluded; if <5 valid remain → DIRECTION_ONLY."""
        records = [
            {"model_value": Decimal("0.50"), "hist_value": None}
            for _ in range(10)
        ]
        tier, _ = _classify_fidelity(records)
        # No valid pairs → fewer than 5 → DIRECTION_ONLY
        assert tier == FidelityTier.DIRECTION_ONLY


# ---------------------------------------------------------------------------
# AC-03 — Catastrophic outlier blocks MAGNITUDE_MATCH
# ---------------------------------------------------------------------------


class TestCatastrophicOutlierBlock:
    def test_catastrophic_outlier_blocks_magnitude_match(self) -> None:
        """AC-03: deviation > 5× hist blocks MAGNITUDE_MATCH.

        Check: |model - hist| > 5 × |hist|
        model=4.0, hist=0.5 → deviation=3.5 > 5×0.5=2.5 ✓ (catastrophic)
        Note: model=3.0, hist=0.5 gives deviation exactly 5× (2.5 == 2.5),
        which does NOT trigger the strict > check — use model=4.0 to be clear.
        """
        good = _make_within_records(9)
        catastrophic = {"model_value": Decimal("4.0"), "hist_value": Decimal("0.5")}
        records = good + [catastrophic]
        tier, _ = _classify_fidelity(records)
        assert tier == FidelityTier.DIRECTION_ONLY

    def test_exactly_5x_is_not_catastrophic(self) -> None:
        """Boundary: model = 5 × hist → exactly 5× is NOT catastrophic (> 5× required)."""
        # 9 clean + 1 at exactly 5×
        good = _make_within_records(9)
        exactly_5x = {"model_value": Decimal("2.5"), "hist_value": Decimal("0.5")}
        records = good + [exactly_5x]
        tier, _ = _classify_fidelity(records)
        # With 9/10 within 20% and no true catastrophic → MAGNITUDE_MATCH
        assert tier == FidelityTier.MAGNITUDE_MATCH

    def test_catastrophic_detection_skips_near_zero_hist(self) -> None:
        """hist ≤ 0.001 is excluded from catastrophic check (avoid div-by-near-zero)."""
        good = _make_within_records(9)
        near_zero_hist = {"model_value": Decimal("0.01"), "hist_value": Decimal("0.0001")}
        records = good + [near_zero_hist]
        # near-zero hist excluded from catastrophic check → MAGNITUDE_MATCH should survive
        tier, _ = _classify_fidelity(records)
        assert tier == FidelityTier.MAGNITUDE_MATCH


# ---------------------------------------------------------------------------
# AC-04 — Fewer than 5 valid pairs → DIRECTION_ONLY
# ---------------------------------------------------------------------------


class TestMinimumPairsGuard:
    def test_four_valid_pairs_gives_direction_only(self) -> None:
        """AC-04: 4 valid pairs with all within 20% → still DIRECTION_ONLY (< 5)."""
        records = _make_within_records(4)
        tier, _ = _classify_fidelity(records)
        assert tier == FidelityTier.DIRECTION_ONLY

    def test_zero_valid_pairs_gives_direction_only(self) -> None:
        """0 valid pairs (all hist_value=None) → DIRECTION_ONLY.

        Note: an entirely empty list returns BELOW_THRESHOLD (run never
        produced records). This tests the realistic case where records exist
        but no historical data is available yet (pre-G2B fixture state).
        """
        records = [
            {"model_value": Decimal("0.50"), "hist_value": None}
            for _ in range(5)
        ]
        tier, _ = _classify_fidelity(records)
        assert tier == FidelityTier.DIRECTION_ONLY

    def test_one_valid_pair_gives_direction_only(self) -> None:
        records = _make_within_records(1)
        tier, _ = _classify_fidelity(records)
        assert tier == FidelityTier.DIRECTION_ONLY


# ---------------------------------------------------------------------------
# AC-05 — EVIDENCE_INSUFFICIENT when C_mag < 0.05 (C_MAG_FLOOR)
# ---------------------------------------------------------------------------


class TestEvidenceInsufficientGuard:
    def test_c_mag_below_floor_returns_evidence_insufficient(self) -> None:
        """AC-05: C_mag=0.03 < 0.05 floor → EVIDENCE_INSUFFICIENT."""
        kappa, status = compute_correction_factor(Decimal("0.03"))
        assert status == "EVIDENCE_INSUFFICIENT"
        assert kappa == Decimal("1.0")

    def test_c_mag_zero_returns_evidence_insufficient(self) -> None:
        """C_mag=0.00 → EVIDENCE_INSUFFICIENT."""
        kappa, status = compute_correction_factor(Decimal("0.00"))
        assert status == "EVIDENCE_INSUFFICIENT"

    def test_c_mag_exactly_at_floor_does_not_trigger_insufficient(self) -> None:
        """C_mag=0.05 is exactly at floor — should NOT trigger EVIDENCE_INSUFFICIENT."""
        kappa, status = compute_correction_factor(Decimal("0.05"))
        assert status != "EVIDENCE_INSUFFICIENT"

    def test_c_mag_below_floor_kappa_is_1(self) -> None:
        """Correction factor is 1.0 (no adjustment) when evidence insufficient."""
        kappa, _ = compute_correction_factor(Decimal("0.02"))
        assert kappa == Decimal("1.0")


# ---------------------------------------------------------------------------
# AC-06 — Correction factor kappa ∈ [0.5, 2.0]
# ---------------------------------------------------------------------------


class TestCorrectionFactorClamp:
    def test_c_mag_060_gives_kappa_in_range(self) -> None:
        """AC-06: C_mag=0.60 → kappa ∈ [0.5, 2.0], status=OK.
        κ = sqrt(0.80 / 0.60) = sqrt(1.333) ≈ 1.155
        """
        kappa, status = compute_correction_factor(Decimal("0.60"))
        assert status == "OK"
        assert Decimal("0.5") <= kappa <= Decimal("2.0")

    def test_c_mag_very_small_above_floor_clamps_to_max(self) -> None:
        """C_mag=0.06 (just above floor): κ = sqrt(0.80/0.06) ≈ 3.65 → clamped to 2.0."""
        kappa, status = compute_correction_factor(Decimal("0.06"))
        assert status == "OK"
        assert kappa == Decimal("2.0")

    def test_c_mag_above_target_clamps_to_min(self) -> None:
        """C_mag=0.999 (> C_target=0.80): κ = sqrt(0.80/0.999) ≈ 0.895; > 0.5, no clamp.
        C_mag beyond max possible → test upper end instead.
        """
        # C_mag > 1.0 is not physically achievable but tests clamp floor:
        # κ = sqrt(0.80/1.50) ≈ 0.730 → above CLAMP_MIN=0.5 → not clamped
        kappa, status = compute_correction_factor(Decimal("1.50"))
        assert status == "OK"
        assert Decimal("0.5") <= kappa <= Decimal("2.0")

    def test_correction_factor_formula_matches_adr_84(self) -> None:
        """κ = clamp(sqrt(C_target / max(C_mag, 0.05)), 0.5, 2.0).
        C_mag=0.60, C_target=0.80: expected = sqrt(0.80/0.60) ≈ 1.1547.
        """
        kappa, _ = compute_correction_factor(Decimal("0.60"))
        # Allow rounding tolerance
        expected_approx = (Decimal("0.80") / Decimal("0.60")).sqrt()
        diff = abs(kappa - expected_approx)
        assert diff < Decimal("0.01"), (
            f"κ={kappa} diverges from sqrt(0.80/0.60)={expected_approx} by {diff}"
        )


# ---------------------------------------------------------------------------
# AC-07 — CalibrationStore override propagates to compute_band()
# ---------------------------------------------------------------------------


class TestCalibrationStoreOverride:
    def setup_method(self) -> None:
        set_calibration_multipliers({})

    def teardown_method(self) -> None:
        set_calibration_multipliers({})

    def test_get_tier_multiplier_returns_structural_prior_by_default(self) -> None:
        """With no override, get_tier_multiplier(3) returns structural prior (1.5 for T3)."""
        m = get_tier_multiplier(3)
        assert m == Decimal("1.5")

    def test_set_calibration_multipliers_overrides_tier_3(self) -> None:
        """AC-07: override T3 multiplier → get_tier_multiplier returns overridden value."""
        set_calibration_multipliers({3: Decimal("1.8")})
        m = get_tier_multiplier(3)
        assert m == Decimal("1.8")

    def test_override_propagates_to_compute_band(self) -> None:
        """AC-07: CalibrationStore override used by compute_band().
        T3, step 1 structural prior: half_width = 0.10 × 1.5 = 0.15
        After override to 1.8:       half_width = 0.10 × 1.8 = 0.18
        For score 0.6:
          Original ci_upper = 0.6 × 1.15 = 0.69
          Override ci_upper = 0.6 × 1.18 = 0.708
        """
        baseline = compute_band(
            composite_score=Decimal("0.6"),
            confidence_tier=3,
            step_index=1,
            framework="financial",
        )
        set_calibration_multipliers({3: Decimal("1.8")})
        calibrated = compute_band(
            composite_score=Decimal("0.6"),
            confidence_tier=3,
            step_index=1,
            framework="financial",
        )
        assert baseline.ci_upper != calibrated.ci_upper, (
            "CalibrationStore override did not propagate to compute_band()"
        )

    def test_clear_override_restores_structural_prior(self) -> None:
        """Clearing override restores structural prior."""
        set_calibration_multipliers({3: Decimal("1.8")})
        assert get_tier_multiplier(3) == Decimal("1.8")
        set_calibration_multipliers({})
        assert get_tier_multiplier(3) == Decimal("1.5")

    def test_non_overridden_tier_returns_structural_prior(self) -> None:
        """Override T3 only; T2 and T4 still use structural priors."""
        set_calibration_multipliers({3: Decimal("1.8")})
        assert get_tier_multiplier(2) == Decimal("1.2")
        assert get_tier_multiplier(4) == Decimal("2.0")


# ---------------------------------------------------------------------------
# AC-08 — Calibration registry file exists with CAL-001 SEN entry
# ---------------------------------------------------------------------------


class TestCalibrationRegistryFile:
    def _registry_path(self) -> Path:
        """Locate docs/backtesting/calibration-registry.md from repo root."""
        # Works whether tests are run from backend/ or repo root
        for candidate in [
            Path("docs/backtesting/calibration-registry.md"),
            Path("../docs/backtesting/calibration-registry.md"),
        ]:
            if candidate.exists():
                return candidate
        pytest.fail(
            "docs/backtesting/calibration-registry.md not found relative to cwd "
            f"({os.getcwd()}). Implementation must create this file."
        )

    def test_registry_file_exists(self) -> None:
        """AC-08: calibration-registry.md exists."""
        path = self._registry_path()
        assert path.exists()

    def test_registry_contains_cal_001(self) -> None:
        """AC-08: registry contains a CAL-001 SEN entry."""
        path = self._registry_path()
        content = path.read_text()
        assert "CAL-001" in content, "CAL-001 entry not found in calibration registry"

    def test_registry_contains_sen_case(self) -> None:
        """CAL-001 must reference the SEN-2014-2019 case."""
        path = self._registry_path()
        content = path.read_text()
        assert "SEN" in content or "Senegal" in content, (
            "SEN case not found in calibration registry"
        )

    def test_registry_records_fidelity_tier(self) -> None:
        """CAL-001 must record the fidelity tier achieved (DIRECTION_ONLY)."""
        path = self._registry_path()
        content = path.read_text()
        assert "DIRECTION_ONLY" in content, (
            "Fidelity tier not recorded in calibration registry"
        )


# ---------------------------------------------------------------------------
# AC-09 — SEN registry entry has affected_indicators_excluded field
# ---------------------------------------------------------------------------


class TestRegistryAffectedIndicatorsField:
    def _registry_content(self) -> str:
        for candidate in [
            Path("docs/backtesting/calibration-registry.md"),
            Path("../docs/backtesting/calibration-registry.md"),
        ]:
            if candidate.exists():
                return candidate.read_text()
        pytest.fail("calibration-registry.md not found")

    def test_affected_indicators_excluded_field_present(self) -> None:
        """AC-09: Every CAL entry must have an affected_indicators_excluded field."""
        content = self._registry_content()
        assert "affected_indicators_excluded" in content, (
            "affected_indicators_excluded field missing from calibration registry"
        )

    def test_cal_001_references_external_sector_or_export(self) -> None:
        """CAL-001 SEN entry must document commodity shock direction mismatch exclusions."""
        content = self._registry_content()
        has_external = "external_sector" in content
        has_export = "export_volume" in content
        has_commodity = "commodity" in content.lower()
        assert has_external or has_export or has_commodity, (
            "CAL-001 must document excluded indicators from CommodityShockConfig direction "
            "mismatch (#1541)"
        )


# ---------------------------------------------------------------------------
# AC-10 — is_pre_calibration=False gate: no code path bypasses it
# ---------------------------------------------------------------------------


class TestIsPreCalibrationFalseGate:
    def test_structural_prior_always_returns_is_pre_calibration_true(self) -> None:
        """AC-10: compute_band() with empty CalibrationStore → is_pre_calibration=True."""
        set_calibration_multipliers({})
        for tier in (1, 2, 3, 4, 5):
            result = compute_band(
                composite_score=Decimal("0.5"),
                confidence_tier=tier,
                step_index=3,
                framework="financial",
            )
            assert result.is_pre_calibration is True, (
                f"compute_band(tier={tier}) returned is_pre_calibration=False "
                "without an accepted registry entry — IS_PRE_CALIBRATION=False "
                "gate violation"
            )

    def test_calibration_store_override_does_not_set_is_pre_calibration_false(self) -> None:
        """CalibrationStore multiplier override alone is insufficient to flip the gate.
        is_pre_calibration=False requires MAGNITUDE_MATCH + accepted registry + co-sign.
        """
        set_calibration_multipliers({3: Decimal("1.8")})
        result = compute_band(
            composite_score=Decimal("0.5"),
            confidence_tier=3,
            step_index=3,
            framework="financial",
        )
        # Even with a CalibrationStore override, is_pre_calibration must remain True
        # until MAGNITUDE_MATCH + registry + Architect + CM co-sign is recorded.
        assert result.is_pre_calibration is True, (
            "CalibrationStore override alone must not set is_pre_calibration=False"
        )
        set_calibration_multipliers({})

    def test_no_compute_band_call_returns_false_without_registry_entry(self) -> None:
        """Exhaustive check: all framework × tier × step combos — is_pre_calibration != False."""
        frameworks = ("financial", "human_development", "ecological")
        for framework in frameworks:
            for tier in range(1, 6):
                for step in (1, 3, 6, 7, 10):
                    score = Decimal("0.5") if framework != "ecological" else Decimal("1.0")
                    result = compute_band(
                        composite_score=score,
                        confidence_tier=tier,
                        step_index=step,
                        framework=framework,
                    )
                    # Suppressed results have is_pre_calibration=None — that is fine.
                    # Only False is a gate violation.
                    assert result.is_pre_calibration is not False, (
                        f"compute_band(framework={framework}, tier={tier}, step={step}) "
                        f"returned is_pre_calibration=False without registry entry"
                    )
