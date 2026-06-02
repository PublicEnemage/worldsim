"""Unit tests for PMM (Policy Maneuver Margin) computation — Issue #496.

Covers:
  - _pmm_indicator_margin: lte thresholds (lower-bound, breach when too low)
  - _pmm_indicator_margin: gte thresholds (upper-bound, breach when too high)
  - _pmm_indicator_margin: degenerate approach_pct=0
  - _pmm_indicator_margin: clamping to [0, 1]
  - _compute_pmm_for_step: no indicators matched → None
  - _compute_pmm_for_step: single threshold in approach zone → correct margin
  - _compute_pmm_for_step: min-of-margins (most constrained dimension)
  - _compute_pmm_for_step: direction tracking across steps
  - _compute_pmm_for_step: cohort-scoped thresholds skipped
  - _compute_pmm_for_step: entity-scoped threshold matches exact entity
"""
from __future__ import annotations

from decimal import Decimal

from app.api.scenarios import _compute_pmm_for_step, _pmm_indicator_margin
from app.schemas import QuantitySchema

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _qty(value: str, framework: str = "financial") -> QuantitySchema:
    return QuantitySchema(
        value=value,
        unit="dimensionless",
        variable_type="ratio",
        confidence_tier=3,
        measurement_framework=framework,
    )


def _threshold(
    indicator_key: str,
    floor_value: str,
    approach_pct: str,
    comparison_operator: str = "lte",
    entity_scope: str = "all",
) -> dict[str, object]:
    return {
        "indicator_key": indicator_key,
        "entity_scope": entity_scope,
        "floor_value": floor_value,
        "approach_pct": approach_pct,
        "comparison_operator": comparison_operator,
    }


# ---------------------------------------------------------------------------
# _pmm_indicator_margin — lte (lower-bound)
# ---------------------------------------------------------------------------


class TestPmmIndicatorMarginLte:
    def test_at_floor_returns_zero(self) -> None:
        # reserve_coverage_months = 2.5 at floor 2.5
        m = _pmm_indicator_margin(Decimal("2.5"), Decimal("2.5"), Decimal("0.20"), "lte")
        assert m == Decimal("0")

    def test_below_floor_returns_zero(self) -> None:
        m = _pmm_indicator_margin(Decimal("2.0"), Decimal("2.5"), Decimal("0.20"), "lte")
        assert m == Decimal("0")

    def test_at_outer_edge_of_approach_zone_returns_one(self) -> None:
        # floor=2.5, approach_pct=0.20 → outer edge = 2.5 * 1.20 = 3.0
        m = _pmm_indicator_margin(Decimal("3.0"), Decimal("2.5"), Decimal("0.20"), "lte")
        assert m == Decimal("1")

    def test_above_approach_zone_capped_at_one(self) -> None:
        m = _pmm_indicator_margin(Decimal("5.0"), Decimal("2.5"), Decimal("0.20"), "lte")
        assert m == Decimal("1")

    def test_midpoint_of_approach_zone_returns_half(self) -> None:
        # floor=2.5, span=0.5 → midpoint = 2.75
        m = _pmm_indicator_margin(Decimal("2.75"), Decimal("2.5"), Decimal("0.20"), "lte")
        assert m == Decimal("0.5")

    def test_just_above_floor_near_zero(self) -> None:
        m = _pmm_indicator_margin(Decimal("2.51"), Decimal("2.5"), Decimal("0.20"), "lte")
        assert Decimal("0") < m < Decimal("0.1")


# ---------------------------------------------------------------------------
# _pmm_indicator_margin — gte (upper-bound)
# ---------------------------------------------------------------------------


class TestPmmIndicatorMarginGte:
    def test_at_floor_returns_zero(self) -> None:
        # debt_gdp_ratio = 1.20 at floor 1.20
        m = _pmm_indicator_margin(Decimal("1.20"), Decimal("1.20"), Decimal("0.10"), "gte")
        assert m == Decimal("0")

    def test_above_floor_returns_zero(self) -> None:
        m = _pmm_indicator_margin(Decimal("1.50"), Decimal("1.20"), Decimal("0.10"), "gte")
        assert m == Decimal("0")

    def test_at_outer_edge_of_approach_zone_returns_one(self) -> None:
        # floor=1.20, approach_pct=0.10 → outer edge = 1.20 * (1-0.10) = 1.08
        m = _pmm_indicator_margin(Decimal("1.08"), Decimal("1.20"), Decimal("0.10"), "gte")
        assert m == Decimal("1")

    def test_below_approach_zone_capped_at_one(self) -> None:
        m = _pmm_indicator_margin(Decimal("0.50"), Decimal("1.20"), Decimal("0.10"), "gte")
        assert m == Decimal("1")

    def test_midpoint_of_approach_zone_returns_half(self) -> None:
        # floor=1.20, span=0.12 → midpoint = 1.14
        m = _pmm_indicator_margin(Decimal("1.14"), Decimal("1.20"), Decimal("0.10"), "gte")
        assert m == Decimal("0.5")

    def test_ecological_proximity_at_boundary_zero(self) -> None:
        # planetary_boundary_co2_proximity = 1.0 at floor 1.0
        m = _pmm_indicator_margin(Decimal("1.0"), Decimal("1.0"), Decimal("0.10"), "gte")
        assert m == Decimal("0")

    def test_ecological_proximity_well_below_boundary_one(self) -> None:
        m = _pmm_indicator_margin(Decimal("0.5"), Decimal("1.0"), Decimal("0.10"), "gte")
        assert m == Decimal("1")


# ---------------------------------------------------------------------------
# _pmm_indicator_margin — degenerate (approach_pct = 0)
# ---------------------------------------------------------------------------


class TestPmmIndicatorMarginDegenerate:
    def test_lte_at_floor_returns_zero(self) -> None:
        m = _pmm_indicator_margin(Decimal("2.5"), Decimal("2.5"), Decimal("0"), "lte")
        assert m == Decimal("0")

    def test_lte_above_floor_returns_one(self) -> None:
        m = _pmm_indicator_margin(Decimal("3.0"), Decimal("2.5"), Decimal("0"), "lte")
        assert m == Decimal("1")

    def test_gte_at_floor_returns_zero(self) -> None:
        m = _pmm_indicator_margin(Decimal("1.2"), Decimal("1.2"), Decimal("0"), "gte")
        assert m == Decimal("0")

    def test_gte_below_floor_returns_one(self) -> None:
        m = _pmm_indicator_margin(Decimal("1.0"), Decimal("1.2"), Decimal("0"), "gte")
        assert m == Decimal("1")


# ---------------------------------------------------------------------------
# _compute_pmm_for_step
# ---------------------------------------------------------------------------


class TestComputePmmForStep:
    def test_no_matching_indicators_returns_none(self) -> None:
        result = _compute_pmm_for_step(
            entity_id="GRC",
            entity_attrs={},
            mda_thresholds=[
                _threshold("reserve_coverage_months", "2.5", "0.20", "lte")
            ],
            prev_pmm=None,
        )
        assert result is None

    def test_no_thresholds_returns_none(self) -> None:
        result = _compute_pmm_for_step(
            entity_id="GRC",
            entity_attrs={"reserve_coverage_months": _qty("4.0")},
            mda_thresholds=[],
            prev_pmm=None,
        )
        assert result is None

    def test_indicator_well_outside_approach_zone_returns_one(self) -> None:
        result = _compute_pmm_for_step(
            entity_id="GRC",
            entity_attrs={"reserve_coverage_months": _qty("10.0")},
            mda_thresholds=[_threshold("reserve_coverage_months", "2.5", "0.20", "lte")],
            prev_pmm=None,
        )
        assert result is not None
        assert Decimal(result.value) == Decimal("1")
        assert result.direction == "flat"

    def test_indicator_in_approach_zone_returns_partial_margin(self) -> None:
        # reserve_coverage_months = 2.75, floor=2.5, approach=0.20 → margin=0.5
        result = _compute_pmm_for_step(
            entity_id="GRC",
            entity_attrs={"reserve_coverage_months": _qty("2.75")},
            mda_thresholds=[_threshold("reserve_coverage_months", "2.5", "0.20", "lte")],
            prev_pmm=None,
        )
        assert result is not None
        assert Decimal(result.value) == Decimal("0.5")

    def test_min_across_thresholds(self) -> None:
        # reserves margin = 1.0 (well above), debt margin = 0 (at breach)
        result = _compute_pmm_for_step(
            entity_id="GRC",
            entity_attrs={
                "reserve_coverage_months": _qty("10.0"),
                "debt_gdp_ratio": _qty("1.20"),  # at floor for gte
            },
            mda_thresholds=[
                _threshold("reserve_coverage_months", "2.5", "0.20", "lte"),
                _threshold("debt_gdp_ratio", "1.20", "0.10", "gte"),
            ],
            prev_pmm=None,
        )
        assert result is not None
        assert Decimal(result.value) == Decimal("0")

    def test_direction_up_when_pmm_improves(self) -> None:
        result = _compute_pmm_for_step(
            entity_id="GRC",
            entity_attrs={"reserve_coverage_months": _qty("10.0")},
            mda_thresholds=[_threshold("reserve_coverage_months", "2.5", "0.20", "lte")],
            prev_pmm=Decimal("0.5"),
        )
        assert result is not None
        assert result.direction == "up"

    def test_direction_down_when_pmm_deteriorates(self) -> None:
        result = _compute_pmm_for_step(
            entity_id="GRC",
            entity_attrs={"reserve_coverage_months": _qty("2.75")},  # margin = 0.5
            mda_thresholds=[_threshold("reserve_coverage_months", "2.5", "0.20", "lte")],
            prev_pmm=Decimal("1.0"),
        )
        assert result is not None
        assert result.direction == "down"

    def test_direction_flat_when_within_threshold(self) -> None:
        # margin = 1.0, prev = 0.995 → delta = 0.005 < threshold 0.01
        result = _compute_pmm_for_step(
            entity_id="GRC",
            entity_attrs={"reserve_coverage_months": _qty("10.0")},
            mda_thresholds=[_threshold("reserve_coverage_months", "2.5", "0.20", "lte")],
            prev_pmm=Decimal("0.995"),
        )
        assert result is not None
        assert result.direction == "flat"

    def test_cohort_scoped_threshold_skipped(self) -> None:
        # Cohort-scoped entity_scope like '*:CHT:*' — not 'all' or exact entity_id
        result = _compute_pmm_for_step(
            entity_id="GRC",
            entity_attrs={"poverty_headcount_ratio": _qty("0.50")},
            mda_thresholds=[
                _threshold(
                    "poverty_headcount_ratio",
                    "0.40",
                    "0.15",
                    "gte",
                    entity_scope="*:CHT:1-*-*",  # cohort scope — skipped
                )
            ],
            prev_pmm=None,
        )
        assert result is None

    def test_entity_scoped_threshold_matches_exact_entity(self) -> None:
        result = _compute_pmm_for_step(
            entity_id="GRC",
            entity_attrs={"reserve_coverage_months": _qty("10.0")},
            mda_thresholds=[
                _threshold(
                    "reserve_coverage_months",
                    "2.5",
                    "0.20",
                    "lte",
                    entity_scope="GRC",  # exact match
                )
            ],
            prev_pmm=None,
        )
        assert result is not None
        assert Decimal(result.value) == Decimal("1")

    def test_entity_scoped_threshold_skipped_for_other_entity(self) -> None:
        result = _compute_pmm_for_step(
            entity_id="GRC",
            entity_attrs={"reserve_coverage_months": _qty("10.0")},
            mda_thresholds=[
                _threshold(
                    "reserve_coverage_months",
                    "2.5",
                    "0.20",
                    "lte",
                    entity_scope="ARG",  # different entity — skipped
                )
            ],
            prev_pmm=None,
        )
        assert result is None

    def test_pmm_value_serialized_as_string(self) -> None:
        result = _compute_pmm_for_step(
            entity_id="GRC",
            entity_attrs={"reserve_coverage_months": _qty("3.0")},
            mda_thresholds=[_threshold("reserve_coverage_months", "2.5", "0.20", "lte")],
            prev_pmm=None,
        )
        assert result is not None
        assert isinstance(result.value, str)
        assert isinstance(result.direction, str)
