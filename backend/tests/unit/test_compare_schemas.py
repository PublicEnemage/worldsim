"""Unit tests for DeltaRecord and CompareResponse schemas — ADR-004 Decision 5."""
from __future__ import annotations

from decimal import Decimal

import pytest

from app.schemas import CompareResponse, DeltaRecord


class TestDeltaRecord:
    def test_increase_direction(self) -> None:
        r = DeltaRecord(
            value_a="100",
            value_b="150",
            delta="50",
            direction="increase",
            confidence_tier=2,
        )
        assert r.direction == "increase"
        assert r.delta == "50"

    def test_decrease_direction(self) -> None:
        r = DeltaRecord(
            value_a="200",
            value_b="180",
            delta="-20",
            direction="decrease",
            confidence_tier=3,
        )
        assert r.direction == "decrease"
        assert r.delta == "-20"

    def test_unchanged_direction(self) -> None:
        r = DeltaRecord(
            value_a="100",
            value_b="100",
            delta="0",
            direction="unchanged",
            confidence_tier=1,
        )
        assert r.direction == "unchanged"

    def test_confidence_tier_max_rule(self) -> None:
        tier_a = 1
        tier_b = 4
        tier = max(tier_a, tier_b)
        r = DeltaRecord(
            value_a="10",
            value_b="20",
            delta="10",
            direction="increase",
            confidence_tier=tier,
        )
        assert r.confidence_tier == 4

    def test_decimal_string_precision(self) -> None:
        val_a = Decimal("1234567890.123456789")
        val_b = Decimal("2345678901.234567890")
        delta = val_b - val_a
        r = DeltaRecord(
            value_a=str(val_a),
            value_b=str(val_b),
            delta=str(delta),
            direction="increase",
            confidence_tier=2,
        )
        assert Decimal(r.delta) == delta

    def test_negative_delta_str(self) -> None:
        val_a = Decimal("500")
        val_b = Decimal("300")
        delta = val_b - val_a
        r = DeltaRecord(
            value_a=str(val_a),
            value_b=str(val_b),
            delta=str(delta),
            direction="decrease",
            confidence_tier=3,
        )
        assert r.delta == "-200"


class TestCompareResponse:
    def test_round_trip(self) -> None:
        delta = DeltaRecord(
            value_a="100",
            value_b="200",
            delta="100",
            direction="increase",
            confidence_tier=2,
        )
        resp = CompareResponse(
            scenario_a_id="aaa",
            scenario_b_id="bbb",
            step_a=5,
            step_b=5,
            deltas={"USA": {"gdp": delta}},
        )
        assert resp.scenario_a_id == "aaa"
        assert resp.deltas["USA"]["gdp"].direction == "increase"

    def test_empty_deltas(self) -> None:
        resp = CompareResponse(
            scenario_a_id="x",
            scenario_b_id="y",
            step_a=0,
            step_b=0,
            deltas={},
        )
        assert resp.deltas == {}

    def test_serialization_no_float(self) -> None:
        delta = DeltaRecord(
            value_a="999.999",
            value_b="1000.001",
            delta="1.002",
            direction="increase",
            confidence_tier=1,
        )
        resp = CompareResponse(
            scenario_a_id="a",
            scenario_b_id="b",
            step_a=3,
            step_b=4,
            deltas={"DEU": {"inflation_rate": delta}},
        )
        dumped = resp.model_dump(mode="json")
        rec = dumped["deltas"]["DEU"]["inflation_rate"]
        assert isinstance(rec["delta"], str)
        assert isinstance(rec["value_a"], str)
        assert isinstance(rec["value_b"], str)

    @pytest.mark.parametrize("direction", ["increase", "decrease", "unchanged"])
    def test_all_directions_accepted(self, direction: str) -> None:
        r = DeltaRecord(
            value_a="0",
            value_b="0",
            delta="0",
            direction=direction,
            confidence_tier=1,
        )
        assert r.direction == direction
