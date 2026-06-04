"""
STOCK/FLOW delta path contract tests — Issue #374.

apply_delta() is the single boundary where VariableType semantics are
enforced. Misclassification between STOCK and FLOW produces silent
accumulation errors that are only visible after several simulation steps.
These tests are required before any simulation module with STOCK variables
ships (DATA_STANDARDS.md §STOCK/FLOW delta path gate).

Contract under test (SimulationEntity.apply_delta):
  STOCK       — replaces existing value unconditionally (delta is absolute level)
  FLOW        — adds delta to existing; initialises from delta if absent
  RATIO       — same additive semantics as FLOW
  DIMENSIONLESS — same additive semantics as FLOW
  confidence_tier — max(existing, delta) on accumulation (lower-of-two-quality rule)
"""
from __future__ import annotations

from decimal import Decimal

import pytest

from app.simulation.engine.models import MeasurementFramework, SimulationEntity
from app.simulation.engine.quantity import Quantity, VariableType

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _entity(attrs: dict[str, tuple[Decimal, VariableType]] | None = None) -> SimulationEntity:
    """Return a minimal country entity with optional pre-seeded attributes."""
    attribute_map: dict[str, Quantity] = {}
    for key, (val, vtype) in (attrs or {}).items():
        attribute_map[key] = Quantity(
            value=val,
            unit="dimensionless",
            variable_type=vtype,
            measurement_framework=MeasurementFramework.FINANCIAL,
            confidence_tier=1,
        )
    return SimulationEntity(
        id="TST",
        entity_type="country",
        attributes=attribute_map,
        metadata={},
    )


def _qty(
    value: float,
    variable_type: VariableType,
    confidence_tier: int = 1,
) -> Quantity:
    return Quantity(
        value=Decimal(str(value)),
        unit="dimensionless",
        variable_type=variable_type,
        measurement_framework=MeasurementFramework.FINANCIAL,
        confidence_tier=confidence_tier,
    )


# ---------------------------------------------------------------------------
# STOCK semantics — replacement
# ---------------------------------------------------------------------------


def test_stock_replaces_existing_value() -> None:
    entity = _entity({"debt_outstanding": (Decimal("500"), VariableType.STOCK)})
    entity.apply_delta("debt_outstanding", _qty(600.0, VariableType.STOCK))
    result = entity.get_attribute_value("debt_outstanding")
    assert result == Decimal("600")


def test_stock_replaces_with_lower_value() -> None:
    entity = _entity({"debt_outstanding": (Decimal("500"), VariableType.STOCK)})
    entity.apply_delta("debt_outstanding", _qty(100.0, VariableType.STOCK))
    assert entity.get_attribute_value("debt_outstanding") == Decimal("100")


def test_stock_initialises_absent_attribute() -> None:
    entity = _entity()
    entity.apply_delta("reserves", _qty(8.5, VariableType.STOCK))
    assert entity.get_attribute_value("reserves") == Decimal("8.5")


def test_stock_second_delta_replaces_first() -> None:
    """Two STOCK deltas on the same key: last one wins, no accumulation."""
    entity = _entity()
    entity.apply_delta("reserves", _qty(10.0, VariableType.STOCK))
    entity.apply_delta("reserves", _qty(20.0, VariableType.STOCK))
    assert entity.get_attribute_value("reserves") == Decimal("20")


# ---------------------------------------------------------------------------
# FLOW semantics — additive accumulation
# ---------------------------------------------------------------------------


def test_flow_accumulates_on_existing() -> None:
    entity = _entity({"gdp_growth": (Decimal("0.03"), VariableType.FLOW)})
    entity.apply_delta("gdp_growth", _qty(-0.05, VariableType.FLOW))
    result = entity.get_attribute_value("gdp_growth")
    assert result == Decimal("0.03") + Decimal("-0.05")


def test_flow_initialises_absent_attribute() -> None:
    entity = _entity()
    entity.apply_delta("gdp_growth", _qty(0.02, VariableType.FLOW))
    assert entity.get_attribute_value("gdp_growth") == Decimal("0.02")


def test_flow_multiple_deltas_accumulate() -> None:
    entity = _entity()
    entity.apply_delta("exports", _qty(10.0, VariableType.FLOW))
    entity.apply_delta("exports", _qty(5.0, VariableType.FLOW))
    entity.apply_delta("exports", _qty(-3.0, VariableType.FLOW))
    assert entity.get_attribute_value("exports") == Decimal("12")


# ---------------------------------------------------------------------------
# RATIO semantics — same additive semantics as FLOW
# ---------------------------------------------------------------------------


def test_ratio_accumulates_on_existing() -> None:
    entity = _entity({"debt_gdp_ratio": (Decimal("1.2"), VariableType.RATIO)})
    entity.apply_delta("debt_gdp_ratio", _qty(0.1, VariableType.RATIO))
    assert entity.get_attribute_value("debt_gdp_ratio") == Decimal("1.3")


def test_ratio_initialises_absent_attribute() -> None:
    entity = _entity()
    entity.apply_delta("debt_gdp_ratio", _qty(0.8, VariableType.RATIO))
    assert entity.get_attribute_value("debt_gdp_ratio") == Decimal("0.8")


# ---------------------------------------------------------------------------
# DIMENSIONLESS semantics — same additive semantics as FLOW
# ---------------------------------------------------------------------------


def test_dimensionless_accumulates_on_existing() -> None:
    entity = _entity({"democratic_quality_score": (Decimal("0.72"), VariableType.DIMENSIONLESS)})
    entity.apply_delta("democratic_quality_score", _qty(-0.05, VariableType.DIMENSIONLESS))
    result = entity.get_attribute_value("democratic_quality_score")
    assert result == pytest.approx(Decimal("0.67"), abs=Decimal("0.000001"))


def test_dimensionless_initialises_absent_attribute() -> None:
    entity = _entity()
    entity.apply_delta("rule_of_law_percentile", _qty(45.0, VariableType.DIMENSIONLESS))
    assert entity.get_attribute_value("rule_of_law_percentile") == Decimal("45")


# ---------------------------------------------------------------------------
# Confidence tier — lower-of-two-quality rule (max of tier numbers)
# ---------------------------------------------------------------------------


def test_confidence_tier_uses_max_on_accumulation() -> None:
    """Lower-of-two-quality rule: result confidence_tier = max(existing, delta)."""
    entity = _entity()
    # Seed with tier-1 (highest quality)
    entity.attributes["gdp_growth"] = Quantity(
        value=Decimal("0.03"),
        unit="dimensionless",
        variable_type=VariableType.FLOW,
        measurement_framework=MeasurementFramework.FINANCIAL,
        confidence_tier=1,
    )
    # Accumulate a tier-3 delta (lower quality)
    delta = Quantity(
        value=Decimal("-0.01"),
        unit="dimensionless",
        variable_type=VariableType.FLOW,
        measurement_framework=MeasurementFramework.FINANCIAL,
        confidence_tier=3,
    )
    entity.apply_delta("gdp_growth", delta)
    assert entity.attributes["gdp_growth"].confidence_tier == 3


def test_confidence_tier_unchanged_when_delta_is_higher_quality() -> None:
    """If delta tier < existing tier, result keeps the lower quality (higher number)."""
    entity = _entity()
    entity.attributes["gdp_growth"] = Quantity(
        value=Decimal("0.03"),
        unit="dimensionless",
        variable_type=VariableType.FLOW,
        measurement_framework=MeasurementFramework.FINANCIAL,
        confidence_tier=4,
    )
    delta = Quantity(
        value=Decimal("0.01"),
        unit="dimensionless",
        variable_type=VariableType.FLOW,
        measurement_framework=MeasurementFramework.FINANCIAL,
        confidence_tier=1,
    )
    entity.apply_delta("gdp_growth", delta)
    assert entity.attributes["gdp_growth"].confidence_tier == 4


def test_stock_replacement_takes_delta_confidence_tier() -> None:
    """STOCK replace: result tier comes from the delta, not the prior value."""
    entity = _entity()
    entity.attributes["reserves"] = Quantity(
        value=Decimal("10"),
        unit="dimensionless",
        variable_type=VariableType.STOCK,
        measurement_framework=MeasurementFramework.FINANCIAL,
        confidence_tier=1,
    )
    delta = Quantity(
        value=Decimal("15"),
        unit="dimensionless",
        variable_type=VariableType.STOCK,
        measurement_framework=MeasurementFramework.FINANCIAL,
        confidence_tier=3,
    )
    entity.apply_delta("reserves", delta)
    assert entity.attributes["reserves"].confidence_tier == 3
