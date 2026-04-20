"""
Unit tests for the Quantity type system — SCR-001, ADR-001 Amendment 1.

Tests cover: VariableType enum, Quantity dataclass field contract,
MonetaryValue subclass, propagate_confidence lower-of-two rule,
and the CM-1 / IA-1 documentation requirements captured in docstrings.
"""
from decimal import Decimal

import pytest

from app.simulation.engine.quantity import (
    MonetaryValue,
    Quantity,
    VariableType,
    propagate_confidence,
)

# ---------------------------------------------------------------------------
# VariableType
# ---------------------------------------------------------------------------


class TestVariableType:
    def test_all_four_types_present(self) -> None:
        values = {vt.value for vt in VariableType}
        assert values == {"stock", "flow", "ratio", "dimensionless"}

    def test_stock_is_distinct_from_flow(self) -> None:
        assert VariableType.STOCK != VariableType.FLOW

    def test_ratio_is_distinct_from_dimensionless(self) -> None:
        assert VariableType.RATIO != VariableType.DIMENSIONLESS

    def test_enum_values_are_strings(self) -> None:
        for vt in VariableType:
            assert isinstance(vt.value, str)


# ---------------------------------------------------------------------------
# Quantity — construction and field contract
# ---------------------------------------------------------------------------


class TestQuantityConstruction:
    def test_minimal_quantity_with_required_fields(self) -> None:
        q = Quantity(
            value=Decimal("1.46"),
            unit="dimensionless",
            variable_type=VariableType.RATIO,
        )
        assert q.value == Decimal("1.46")
        assert q.unit == "dimensionless"
        assert q.variable_type == VariableType.RATIO

    def test_optional_fields_default_to_none_or_one(self) -> None:
        q = Quantity(
            value=Decimal("44e9"),
            unit="USD_2015",
            variable_type=VariableType.FLOW,
        )
        assert q.measurement_framework is None
        assert q.observation_date is None
        assert q.source_id is None
        assert q.confidence_tier == 1

    def test_confidence_tier_can_be_set_explicitly(self) -> None:
        q = Quantity(
            value=Decimal("0.5"),
            unit="dimensionless",
            variable_type=VariableType.RATIO,
            confidence_tier=3,
        )
        assert q.confidence_tier == 3

    def test_all_five_confidence_tiers_accepted(self) -> None:
        for tier in range(1, 6):
            q = Quantity(
                value=Decimal("1"),
                unit="dimensionless",
                variable_type=VariableType.DIMENSIONLESS,
                confidence_tier=tier,
            )
            assert q.confidence_tier == tier

    def test_value_is_decimal_not_float(self) -> None:
        q = Quantity(
            value=Decimal("0.082"),
            unit="dimensionless",
            variable_type=VariableType.RATIO,
        )
        assert isinstance(q.value, Decimal)

    def test_negative_value_accepted(self) -> None:
        q = Quantity(
            value=Decimal("-0.05"),
            unit="dimensionless",
            variable_type=VariableType.FLOW,
        )
        assert q.value == Decimal("-0.05")

    def test_zero_value_accepted(self) -> None:
        q = Quantity(
            value=Decimal("0"),
            unit="dimensionless",
            variable_type=VariableType.STOCK,
        )
        assert q.value == Decimal("0")

    def test_kw_only_construction(self) -> None:
        # kw_only=True means positional arguments are not accepted
        with pytest.raises(TypeError):
            Quantity(Decimal("1.0"), "dimensionless", VariableType.RATIO)  # type: ignore[call-arg]

    def test_equality_is_value_based(self) -> None:
        q1 = Quantity(value=Decimal("1.0"), unit="USD_2015", variable_type=VariableType.FLOW)
        q2 = Quantity(value=Decimal("1.0"), unit="USD_2015", variable_type=VariableType.FLOW)
        assert q1 == q2

    def test_different_values_not_equal(self) -> None:
        q1 = Quantity(value=Decimal("1.0"), unit="USD_2015", variable_type=VariableType.FLOW)
        q2 = Quantity(value=Decimal("2.0"), unit="USD_2015", variable_type=VariableType.FLOW)
        assert q1 != q2

    def test_different_variable_types_not_equal(self) -> None:
        q1 = Quantity(value=Decimal("1.0"), unit="USD_2015", variable_type=VariableType.FLOW)
        q2 = Quantity(value=Decimal("1.0"), unit="USD_2015", variable_type=VariableType.STOCK)
        assert q1 != q2


# ---------------------------------------------------------------------------
# MonetaryValue — subclass contract
# ---------------------------------------------------------------------------


class TestMonetaryValue:
    def test_monetary_value_is_quantity_subclass(self) -> None:
        mv = MonetaryValue(
            value=Decimal("1.2e9"),
            unit="USD_2015",
            variable_type=VariableType.FLOW,
        )
        assert isinstance(mv, Quantity)

    def test_inherited_fields_accessible(self) -> None:
        mv = MonetaryValue(
            value=Decimal("1.2e9"),
            unit="USD_2015",
            variable_type=VariableType.FLOW,
            confidence_tier=2,
        )
        assert mv.value == Decimal("1.2e9")
        assert mv.unit == "USD_2015"
        assert mv.variable_type == VariableType.FLOW
        assert mv.confidence_tier == 2

    def test_monetary_specific_fields_default_to_empty_string(self) -> None:
        mv = MonetaryValue(
            value=Decimal("5e8"),
            unit="USD_2015",
            variable_type=VariableType.FLOW,
        )
        assert mv.currency_code == ""
        assert mv.price_basis == ""
        assert mv.exchange_rate_type == ""

    def test_monetary_specific_fields_can_be_set(self) -> None:
        mv = MonetaryValue(
            value=Decimal("5e8"),
            unit="USD_2015",
            variable_type=VariableType.FLOW,
            currency_code="GHS",
            price_basis="constant",
            exchange_rate_type="ppp",
        )
        assert mv.currency_code == "GHS"
        assert mv.price_basis == "constant"
        assert mv.exchange_rate_type == "ppp"

    def test_kw_only_construction(self) -> None:
        with pytest.raises(TypeError):
            MonetaryValue(Decimal("1.0"), "USD_2015", VariableType.FLOW)  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# propagate_confidence — lower-of-two rule
# ---------------------------------------------------------------------------


class TestPropagateConfidence:
    def _q(self, tier: int) -> Quantity:
        return Quantity(
            value=Decimal("1"),
            unit="dimensionless",
            variable_type=VariableType.RATIO,
            confidence_tier=tier,
        )

    def test_single_input_returns_its_tier(self) -> None:
        assert propagate_confidence(self._q(2)) == 2

    def test_lower_tier_wins_when_unequal(self) -> None:
        assert propagate_confidence(self._q(1), self._q(4)) == 4

    def test_equal_tiers_return_that_tier(self) -> None:
        assert propagate_confidence(self._q(2), self._q(2)) == 2

    def test_three_inputs_takes_minimum(self) -> None:
        assert propagate_confidence(self._q(1), self._q(3), self._q(2)) == 3

    def test_tier1_and_tier5_returns_5(self) -> None:
        assert propagate_confidence(self._q(1), self._q(5)) == 5

    def test_all_tier5_returns_5(self) -> None:
        inputs = [self._q(5) for _ in range(5)]
        assert propagate_confidence(*inputs) == 5

    def test_returns_int(self) -> None:
        result = propagate_confidence(self._q(2), self._q(3))
        assert isinstance(result, int)

    def test_high_confidence_input_mixed_with_low_confidence(self) -> None:
        # Tier 1 historical data + Tier 4 projection = Tier 4 output
        # This is the IA-1 scenario: a 30-year projection should not
        # appear as Tier 1. The lower-of-two rule correctly captures this
        # for derived computations mixing historical and projected inputs.
        historical = self._q(1)
        projected = self._q(4)
        assert propagate_confidence(historical, projected) == 4

    def test_lower_of_two_bias_is_conservative(self) -> None:
        # The lower-of-two rule overstates uncertainty for independent,
        # mutually corroborating inputs. This is the intended behavior
        # (CM-1 disposition). Two Tier 1 inputs produce Tier 1 output
        # — in this case there is no overstatement.
        assert propagate_confidence(self._q(1), self._q(1)) == 1
        # Two Tier 2 inputs produce Tier 2 — conservative but not wrong.
        assert propagate_confidence(self._q(2), self._q(2)) == 2
