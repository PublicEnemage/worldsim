"""Tests for G8a reversibility classification — Issue #271.

Covers:
1. ReversibilityClassification enum values and string representation
2. REVERSIBILITY_REGISTRY: required indicators present with correct classification
3. Quantity carries the reversibility field (default None; can be set)
4. Round-trip: Quantity → quantity_to_jsonb_envelope → QuantitySchema.from_jsonb
   → quantity_from_schema preserves reversibility exactly
5. Unknown reversibility value in JSONB envelope is silently dropped (defensive)
"""
from __future__ import annotations

from decimal import Decimal

from app.schemas import QuantitySchema
from app.simulation.engine.quantity import Quantity, ReversibilityClassification, VariableType
from app.simulation.engine.reversibility import REVERSIBILITY_REGISTRY
from app.simulation.repositories.quantity_serde import (
    quantity_from_schema,
    quantity_to_jsonb_envelope,
)

RC = ReversibilityClassification


class TestReversibilityClassificationEnum:
    def test_values_are_correct_strings(self) -> None:
        assert RC.RECOVERABLE.value == "recoverable"
        assert RC.DELAYED_RECOVERY.value == "delayed_recovery"
        assert RC.IRREVERSIBLE.value == "irreversible"

    def test_is_str_enum(self) -> None:
        assert isinstance(RC.RECOVERABLE, str)
        assert RC.IRREVERSIBLE == "irreversible"

    def test_round_trip_from_string(self) -> None:
        for member in RC:
            assert RC(member.value) is member


class TestReversibilityRegistry:
    """Required indicator presence and classification correctness."""

    def test_irreversible_mortality(self) -> None:
        assert REVERSIBILITY_REGISTRY["maternal_mortality_ratio"] is RC.IRREVERSIBLE
        assert REVERSIBILITY_REGISTRY["child_mortality_rate"] is RC.IRREVERSIBLE

    def test_irreversible_schooling(self) -> None:
        assert REVERSIBILITY_REGISTRY["school_enrollment_rate"] is RC.IRREVERSIBLE
        assert REVERSIBILITY_REGISTRY["primary_school_completion_rate"] is RC.IRREVERSIBLE

    def test_irreversible_emigration(self) -> None:
        assert REVERSIBILITY_REGISTRY["skilled_emigration_rate"] is RC.IRREVERSIBLE
        assert REVERSIBILITY_REGISTRY["net_migration_skilled"] is RC.IRREVERSIBLE

    def test_irreversible_ecosystem(self) -> None:
        assert REVERSIBILITY_REGISTRY["ecosystem_degradation_index"] is RC.IRREVERSIBLE

    def test_delayed_recovery_community(self) -> None:
        assert REVERSIBILITY_REGISTRY["community_social_capital_index"] is RC.DELAYED_RECOVERY

    def test_delayed_recovery_land_use(self) -> None:
        assert REVERSIBILITY_REGISTRY["land_use_pressure_index"] is RC.DELAYED_RECOVERY

    def test_delayed_recovery_food(self) -> None:
        assert REVERSIBILITY_REGISTRY["food_insecurity_rate"] is RC.DELAYED_RECOVERY

    def test_recoverable_financial_indicators(self) -> None:
        for key in (
            "reserve_coverage_months",
            "gdp_growth_rate",
            "unemployment_rate",
            "fiscal_balance_pct_gdp",
            "debt_gdp_ratio",
            "inflation_rate",
            "current_account_balance_pct_gdp",
        ):
            assert REVERSIBILITY_REGISTRY[key] is RC.RECOVERABLE, (
                f"Expected RECOVERABLE for {key}"
            )

    def test_all_values_are_classification_members(self) -> None:
        for key, val in REVERSIBILITY_REGISTRY.items():
            assert isinstance(val, RC), (
                f"Registry entry {key!r} has unexpected type {type(val)}"
            )

    def test_registry_has_minimum_coverage(self) -> None:
        assert len(REVERSIBILITY_REGISTRY) >= 15, (
            f"Registry has only {len(REVERSIBILITY_REGISTRY)} entries — "
            "expected at least 15 (G8a minimum coverage)"
        )


class TestQuantityReversibilityField:
    def _make_qty(
        self,
        reversibility: RC | None = None,
    ) -> Quantity:
        return Quantity(
            value=Decimal("1.0"),
            unit="dimensionless",
            variable_type=VariableType.DIMENSIONLESS,
            confidence_tier=2,
            reversibility=reversibility,
        )

    def test_default_is_none(self) -> None:
        qty = self._make_qty()
        assert qty.reversibility is None

    def test_can_set_irreversible(self) -> None:
        qty = self._make_qty(RC.IRREVERSIBLE)
        assert qty.reversibility is RC.IRREVERSIBLE

    def test_can_set_delayed_recovery(self) -> None:
        qty = self._make_qty(RC.DELAYED_RECOVERY)
        assert qty.reversibility is RC.DELAYED_RECOVERY

    def test_can_set_recoverable(self) -> None:
        qty = self._make_qty(RC.RECOVERABLE)
        assert qty.reversibility is RC.RECOVERABLE


class TestReversibilityRoundTrip:
    """Round-trip: quantity_to_jsonb_envelope → from_jsonb → quantity_from_schema."""

    def _round_trip(self, qty: Quantity) -> Quantity:
        envelope = quantity_to_jsonb_envelope(qty)
        schema = QuantitySchema.from_jsonb(envelope)
        return quantity_from_schema(schema)

    def test_irreversible_survives_round_trip(self) -> None:
        qty = Quantity(
            value=Decimal("0.42"),
            unit="dimensionless",
            variable_type=VariableType.DIMENSIONLESS,
            confidence_tier=3,
            reversibility=RC.IRREVERSIBLE,
        )
        assert self._round_trip(qty).reversibility is RC.IRREVERSIBLE

    def test_delayed_recovery_survives_round_trip(self) -> None:
        qty = Quantity(
            value=Decimal("0.7"),
            unit="dimensionless",
            variable_type=VariableType.DIMENSIONLESS,
            confidence_tier=2,
            reversibility=RC.DELAYED_RECOVERY,
        )
        assert self._round_trip(qty).reversibility is RC.DELAYED_RECOVERY

    def test_recoverable_survives_round_trip(self) -> None:
        qty = Quantity(
            value=Decimal("3.5"),
            unit="months",
            variable_type=VariableType.RATIO,
            confidence_tier=1,
            reversibility=RC.RECOVERABLE,
        )
        assert self._round_trip(qty).reversibility is RC.RECOVERABLE

    def test_none_reversibility_survives_round_trip(self) -> None:
        qty = Quantity(
            value=Decimal("100"),
            unit="USD_2015",
            variable_type=VariableType.STOCK,
            confidence_tier=1,
        )
        assert self._round_trip(qty).reversibility is None

    def test_envelope_omits_key_when_none(self) -> None:
        qty = Quantity(
            value=Decimal("1"),
            unit="dimensionless",
            variable_type=VariableType.DIMENSIONLESS,
            confidence_tier=1,
        )
        envelope = quantity_to_jsonb_envelope(qty)
        assert "reversibility" not in envelope

    def test_envelope_includes_key_when_set(self) -> None:
        qty = Quantity(
            value=Decimal("1"),
            unit="dimensionless",
            variable_type=VariableType.DIMENSIONLESS,
            confidence_tier=1,
            reversibility=RC.IRREVERSIBLE,
        )
        envelope = quantity_to_jsonb_envelope(qty)
        assert envelope["reversibility"] == "irreversible"

    def test_unknown_reversibility_value_in_jsonb_is_silently_dropped(self) -> None:
        """Defensive: unknown enum value in JSONB must not raise; reversibility → None."""
        qty = Quantity(
            value=Decimal("1"),
            unit="dimensionless",
            variable_type=VariableType.DIMENSIONLESS,
            confidence_tier=1,
            reversibility=RC.RECOVERABLE,
        )
        envelope = quantity_to_jsonb_envelope(qty)
        envelope["reversibility"] = "semi_reversible_unknown"
        schema = QuantitySchema.from_jsonb(envelope)
        result = quantity_from_schema(schema)
        assert result.reversibility is None
