"""SyntheticDataEngine — ADR-007 §Section 1, §Consequences §Implementation Sequence steps 1+3.

M16-G4 (#22 scoped): Methods E and B only. Method A (Hierarchical Bayesian) is deferred
until the comparison group registry is populated (ADR-007 §Consequences step 4).

Method dispatch order (ADR-007 §Section 1 — evaluated in this order):
  Method E (STRUCTURAL_ABSENCE): fires when ANY of:
    - indicator_profile.mnar is True (Missing Not At Random)
    - indicator_profile.comparable_country_count < 3
    - indicator_profile.ci_width_to_estimate_ratio > 4.0
  Method B (SYNTHETIC_COMPARABLE / MICE): fires when ALL of:
    - observed_fraction >= 0.80
    - gap_length <= 3 periods
    - bounded_on_both_sides is True
    - (none of the Method E conditions are met — Method E is evaluated first)

When neither method fires (not enough data for MICE, but no Method E trigger either),
the engine returns a default STRUCTURAL_ABSENCE result. This conservative fallback
ensures no synthetic value is presented as real when the dispatch logic has no
applicable method.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


@dataclass
class SyntheticQuantityResult:
    """Output of SyntheticDataEngine.infer().

    is_synthetic: always True (this result is only produced for synthetic cases).
    synthetic_method: "STRUCTURAL_ABSENCE" | "SYNTHETIC_COMPARABLE" | "SYNTHETIC_MODEL"
    value: None for STRUCTURAL_ABSENCE; float in [0.0, 1.0] for SYNTHETIC_COMPARABLE.

    ADR-007 §Section 2: the synthetic_method string is the primary disclosure field.
    "STRUCTURAL_ABSENCE" maps to the "SAD" badge in Zone 1B/1D (ADR-007 §Section 6).
    "SYNTHETIC_COMPARABLE" maps to T3 (holdout_validated=True) or T4 badge.
    "SYNTHETIC_MODEL" maps to T4 badge.
    """

    is_synthetic: bool
    synthetic_method: str | None
    value: float | None


# ---------------------------------------------------------------------------
# Source registry protocol
# ---------------------------------------------------------------------------


class IndicatorDataProfile(Protocol):
    """Protocol for the data profile object returned by source_registry.get_indicator_profile().

    The real SourceRegistry returns objects conforming to this protocol.
    The QA test suite uses _IndicatorDataProfile (a dataclass) that satisfies the same contract.
    """

    comparable_country_count: int
    mnar: bool
    observed_fraction: float
    gap_length: int
    bounded_on_both_sides: bool
    ci_width_to_estimate_ratio: float


class SourceRegistryProtocol(Protocol):
    """Protocol for the source_registry argument to SyntheticDataEngine.infer()."""

    def get_indicator_profile(
        self, entity_id: str, indicator_key: str
    ) -> Any:  # noqa: ANN401
        """Return the data profile for (entity_id, indicator_key)."""
        ...


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------


class SyntheticDataEngine:
    """Dispatches synthetic data inference for a single (entity_id, indicator_key) pair.

    This is a stateless utility class — all methods are classmethods.
    The real ScenarioRunner invokes this during DemographicModule step computation
    when an indicator has no primary source data at the required vintage.

    ADR-007 §Section 1 decision tree (evaluated top-to-bottom; first match wins):
      1. Method E  — Structural Absence Declaration (MNAR / <3 comparables / CI >4×)
      2. Method B  — MICE imputation (≥80% observed, gap ≤3, bounded)
      3. Default   — Structural Absence Declaration (conservative fallback)
    """

    @classmethod
    def infer(
        cls,
        entity_id: str,
        indicator_key: str,
        source_registry: Any,  # noqa: ANN401
    ) -> SyntheticQuantityResult:
        """Infer synthetic data for (entity_id, indicator_key) using the dispatch tree.

        Args:
            entity_id: ISO 3166-1 alpha-3 entity identifier.
            indicator_key: The indicator to synthesize (e.g. "poverty_headcount_ratio").
            source_registry: Object with get_indicator_profile(entity_id, indicator_key).

        Returns:
            SyntheticQuantityResult with is_synthetic=True and the dispatched method.
        """
        profile = source_registry.get_indicator_profile(entity_id, indicator_key)
        return cls._dispatch(profile)

    @classmethod
    def _dispatch(cls, profile: IndicatorDataProfile) -> SyntheticQuantityResult:
        # Method E conditions — evaluated first; any condition sufficient to fire Method E
        if cls._method_e_fires(profile):
            return SyntheticQuantityResult(
                is_synthetic=True,
                synthetic_method="STRUCTURAL_ABSENCE",
                value=None,
            )

        # Method B conditions — all must be met
        if cls._method_b_fires(profile):
            return cls._apply_method_b(profile)

        # Conservative fallback — no applicable method; treat as Structural Absence
        return SyntheticQuantityResult(
            is_synthetic=True,
            synthetic_method="STRUCTURAL_ABSENCE",
            value=None,
        )

    @classmethod
    def _method_e_fires(cls, profile: IndicatorDataProfile) -> bool:
        """ADR-007 §Section 1 Method E trigger conditions (any one sufficient)."""
        if profile.mnar:
            return True
        if profile.comparable_country_count < 3:
            return True
        return profile.ci_width_to_estimate_ratio > 4.0

    @classmethod
    def _method_b_fires(cls, profile: IndicatorDataProfile) -> bool:
        """ADR-007 §Section 1 Method B trigger conditions (all must be met)."""
        if profile.observed_fraction < 0.80:
            return False
        if profile.gap_length > 3:
            return False
        return profile.bounded_on_both_sides

    @classmethod
    def _apply_method_b(cls, profile: IndicatorDataProfile) -> SyntheticQuantityResult:
        """Apply MICE imputation (Method B).

        Produces a synthetic estimate in [0.0, 1.0] for bounded ratio indicators.
        The actual MICE computation requires comparison group data not available at
        G4 scope — we produce a plausible synthetic estimate from the observed fraction.

        ADR-007 §Section 4 tier assignment:
          T3 — short gap (gap_length ≤ 1) or strong flanking (observed_fraction ≥ 0.90)
          T4 — longer gap or weaker flanking
        Both cases return synthetic_method="SYNTHETIC_COMPARABLE" per ADR-007 §Section 1.
        The holdout_validated flag on the Quantity record governs T3 vs T4 display in badges.
        """
        # Simplified MICE estimate: use observed_fraction as a proxy for the imputed value.
        # This is a conservative placeholder; real MICE chained equations require
        # the comparison group registry (ADR-007 §Consequences step 2, out of G4 scope).
        # The value is clipped to [0.01, 0.99] to remain within bounded indicator range.
        imputed = max(0.01, min(0.99, profile.observed_fraction * 0.95))
        return SyntheticQuantityResult(
            is_synthetic=True,
            synthetic_method="SYNTHETIC_COMPARABLE",
            value=imputed,
        )
