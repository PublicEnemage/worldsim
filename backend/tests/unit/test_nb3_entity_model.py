"""Unit tests for ADR-001 Amendment 2 — CohortProfile and AttributeType.

Covers: AttributeType enum (Issue #30), CohortProfile dataclass (Issue #28),
cohort_profiles field on SimulationEntity, JSONB round-trip via quantity_serde,
Greece M12 seed fixture (EU-SILC 2010, Tier 2).
"""
from decimal import Decimal

import pytest

from app.simulation.engine.models import CohortProfile, SimulationEntity
from app.simulation.engine.quantity import AttributeType, Quantity, VariableType
from app.simulation.repositories.quantity_serde import (
    cohort_profile_from_jsonb,
    cohort_profile_to_jsonb,
    quantity_from_jsonb,
    quantity_to_jsonb_envelope,
)

# ---------------------------------------------------------------------------
# AttributeType enum
# ---------------------------------------------------------------------------


class TestAttributeType:
    def test_all_four_values_present(self) -> None:
        values = {at.value for at in AttributeType}
        assert values == {"stock", "flow", "structural_index", "rate"}

    def test_str_enum_construction(self) -> None:
        assert AttributeType("rate") is AttributeType.RATE
        assert AttributeType("stock") is AttributeType.STOCK
        assert AttributeType("flow") is AttributeType.FLOW
        assert AttributeType("structural_index") is AttributeType.STRUCTURAL_INDEX

    def test_unknown_value_raises(self) -> None:
        with pytest.raises(ValueError):
            AttributeType("unknown")


# ---------------------------------------------------------------------------
# Quantity.attribute_type and stock_flow_identity fields
# ---------------------------------------------------------------------------


class TestQuantityAmendment2Fields:
    def test_attribute_type_defaults_none(self) -> None:
        q = Quantity(value=Decimal("1"), unit="ratio", variable_type=VariableType.RATIO)
        assert q.attribute_type is None

    def test_stock_flow_identity_defaults_false(self) -> None:
        q = Quantity(value=Decimal("1"), unit="ratio", variable_type=VariableType.RATIO)
        assert q.stock_flow_identity is False

    def test_attribute_type_set(self) -> None:
        q = Quantity(
            value=Decimal("0.18"),
            unit="dimensionless",
            variable_type=VariableType.RATIO,
            attribute_type=AttributeType.RATE,
        )
        assert q.attribute_type is AttributeType.RATE

    def test_stock_flow_identity_set(self) -> None:
        q = Quantity(
            value=Decimal("100"),
            unit="USD_millions_current",
            variable_type=VariableType.STOCK,
            stock_flow_identity=True,
        )
        assert q.stock_flow_identity is True


# ---------------------------------------------------------------------------
# Quantity JSONB envelope — attribute_type and stock_flow_identity
# ---------------------------------------------------------------------------


class TestQuantityEnvelopeAmendment2:
    def test_attribute_type_omitted_when_none(self) -> None:
        q = Quantity(value=Decimal("1"), unit="ratio", variable_type=VariableType.RATIO)
        envelope = quantity_to_jsonb_envelope(q)
        assert "attribute_type" not in envelope

    def test_stock_flow_identity_omitted_when_false(self) -> None:
        q = Quantity(value=Decimal("1"), unit="ratio", variable_type=VariableType.RATIO)
        envelope = quantity_to_jsonb_envelope(q)
        assert "stock_flow_identity" not in envelope

    def test_attribute_type_serialised_when_set(self) -> None:
        q = Quantity(
            value=Decimal("0.201"),
            unit="dimensionless",
            variable_type=VariableType.RATIO,
            attribute_type=AttributeType.RATE,
        )
        envelope = quantity_to_jsonb_envelope(q)
        assert envelope["attribute_type"] == "rate"

    def test_stock_flow_identity_serialised_when_true(self) -> None:
        q = Quantity(
            value=Decimal("100"),
            unit="USD_millions_current",
            variable_type=VariableType.STOCK,
            stock_flow_identity=True,
        )
        envelope = quantity_to_jsonb_envelope(q)
        assert envelope["stock_flow_identity"] is True

    def test_attribute_type_round_trips(self) -> None:
        q = Quantity(
            value=Decimal("0.065"),
            unit="dimensionless",
            variable_type=VariableType.RATIO,
            confidence_tier=2,
            attribute_type=AttributeType.RATE,
        )
        restored = quantity_from_jsonb(quantity_to_jsonb_envelope(q))
        assert restored.attribute_type is AttributeType.RATE

    def test_stock_flow_identity_round_trips(self) -> None:
        q = Quantity(
            value=Decimal("500"),
            unit="USD_millions_current",
            variable_type=VariableType.STOCK,
            stock_flow_identity=True,
        )
        restored = quantity_from_jsonb(quantity_to_jsonb_envelope(q))
        assert restored.stock_flow_identity is True

    def test_unknown_attribute_type_in_jsonb_silently_none(self) -> None:
        envelope = {
            "_envelope_version": "1",
            "value": "1.0",
            "unit": "dimensionless",
            "variable_type": "ratio",
            "confidence_tier": 1,
            "attribute_type": "FUTURE_UNKNOWN_TYPE",
        }
        q = quantity_from_jsonb(envelope)
        assert q.attribute_type is None


# ---------------------------------------------------------------------------
# CohortProfile dataclass
# ---------------------------------------------------------------------------


class TestCohortProfile:
    def test_construct_with_attributes(self) -> None:
        profile = CohortProfile(
            attributes={
                "poverty_headcount": Quantity(
                    value=Decimal("0.201"),
                    unit="dimensionless",
                    variable_type=VariableType.RATIO,
                    attribute_type=AttributeType.RATE,
                    confidence_tier=2,
                )
            }
        )
        assert "poverty_headcount" in profile.attributes
        assert profile.attributes["poverty_headcount"].value == Decimal("0.201")

    def test_empty_attributes_allowed(self) -> None:
        profile = CohortProfile(attributes={})
        assert profile.attributes == {}


# ---------------------------------------------------------------------------
# CohortProfile JSONB serde
# ---------------------------------------------------------------------------


class TestCohortProfileSerde:
    def _q1_profile(self) -> CohortProfile:
        return CohortProfile(
            attributes={
                "poverty_headcount": Quantity(
                    value=Decimal("0.201"),
                    unit="dimensionless",
                    variable_type=VariableType.RATIO,
                    attribute_type=AttributeType.RATE,
                    confidence_tier=2,
                    source_id="EU_SILC_2010_GRC",
                ),
                "unemployment_rate": Quantity(
                    value=Decimal("0.18"),
                    unit="dimensionless",
                    variable_type=VariableType.RATIO,
                    attribute_type=AttributeType.RATE,
                    confidence_tier=2,
                    source_id="EU_SILC_2010_GRC",
                ),
            }
        )

    def test_to_jsonb_produces_attribute_envelopes(self) -> None:
        serialised = cohort_profile_to_jsonb(self._q1_profile())
        assert "poverty_headcount" in serialised
        assert "unemployment_rate" in serialised
        assert serialised["poverty_headcount"]["value"] == "0.201"
        assert serialised["unemployment_rate"]["value"] == "0.18"

    def test_round_trip_preserves_value(self) -> None:
        original = self._q1_profile()
        serialised = cohort_profile_to_jsonb(original)
        restored = cohort_profile_from_jsonb(serialised)
        assert restored.attributes["poverty_headcount"].value == Decimal("0.201")
        assert restored.attributes["unemployment_rate"].value == Decimal("0.18")

    def test_round_trip_preserves_confidence_tier(self) -> None:
        restored = cohort_profile_from_jsonb(cohort_profile_to_jsonb(self._q1_profile()))
        assert restored.attributes["poverty_headcount"].confidence_tier == 2

    def test_round_trip_preserves_attribute_type(self) -> None:
        restored = cohort_profile_from_jsonb(cohort_profile_to_jsonb(self._q1_profile()))
        assert restored.attributes["poverty_headcount"].attribute_type is AttributeType.RATE

    def test_malformed_envelope_silently_skipped(self) -> None:
        data = {
            "poverty_headcount": {"value": "0.201", "unit": "dimensionless"},
            "broken_key": "not_a_dict",
        }
        restored = cohort_profile_from_jsonb(data)
        assert "broken_key" not in restored.attributes


# ---------------------------------------------------------------------------
# SimulationEntity.cohort_profiles field
# ---------------------------------------------------------------------------


class TestSimulationEntityCohortProfiles:
    def test_cohort_profiles_defaults_none(self) -> None:
        entity = SimulationEntity(
            id="GRC",
            entity_type="country",
            attributes={},
            metadata={"name_en": "Greece"},
        )
        assert entity.cohort_profiles is None

    def test_cohort_profiles_accepted(self) -> None:
        q1 = CohortProfile(
            attributes={
                "poverty_headcount": Quantity(
                    value=Decimal("0.201"),
                    unit="dimensionless",
                    variable_type=VariableType.RATIO,
                    attribute_type=AttributeType.RATE,
                    confidence_tier=2,
                )
            }
        )
        entity = SimulationEntity(
            id="GRC",
            entity_type="country",
            attributes={},
            metadata={"name_en": "Greece"},
            cohort_profiles={"Q1": q1},
        )
        assert entity.cohort_profiles is not None
        assert "Q1" in entity.cohort_profiles


# ---------------------------------------------------------------------------
# Greece M12 seed fixture — EU-SILC 2010, Tier 2
# ---------------------------------------------------------------------------


class TestGreeceM12CohortSeed:
    """Canonical seed fixture: EU-SILC 2010 Greece income-quintile distributional data."""

    def _build_grc_entity(self) -> SimulationEntity:
        q1 = CohortProfile(
            attributes={
                "poverty_headcount": Quantity(
                    value=Decimal("0.201"),
                    unit="dimensionless",
                    variable_type=VariableType.RATIO,
                    attribute_type=AttributeType.RATE,
                    confidence_tier=2,
                    source_id="EU_SILC_2010_GRC",
                ),
                "unemployment_rate": Quantity(
                    value=Decimal("0.18"),
                    unit="dimensionless",
                    variable_type=VariableType.RATIO,
                    attribute_type=AttributeType.RATE,
                    confidence_tier=2,
                    source_id="EU_SILC_2010_GRC",
                ),
            }
        )
        q5 = CohortProfile(
            attributes={
                "poverty_headcount": Quantity(
                    value=Decimal("0.065"),
                    unit="dimensionless",
                    variable_type=VariableType.RATIO,
                    attribute_type=AttributeType.RATE,
                    confidence_tier=2,
                    source_id="EU_SILC_2010_GRC",
                ),
            }
        )
        return SimulationEntity(
            id="GRC",
            entity_type="country",
            attributes={},
            metadata={"name_en": "Greece"},
            cohort_profiles={"Q1": q1, "Q5": q5},
        )

    def test_q1_poverty_headcount_value(self) -> None:
        entity = self._build_grc_entity()
        assert entity.cohort_profiles is not None
        q1_ph = entity.cohort_profiles["Q1"].attributes["poverty_headcount"]
        assert q1_ph.value == pytest.approx(Decimal("0.201"))

    def test_q1_poverty_headcount_confidence_tier(self) -> None:
        entity = self._build_grc_entity()
        assert entity.cohort_profiles is not None
        assert entity.cohort_profiles["Q1"].attributes["poverty_headcount"].confidence_tier == 2

    def test_q5_poverty_headcount_value(self) -> None:
        entity = self._build_grc_entity()
        assert entity.cohort_profiles is not None
        q5_ph = entity.cohort_profiles["Q5"].attributes["poverty_headcount"]
        assert q5_ph.value == pytest.approx(Decimal("0.065"))

    def test_q1_unemployment_rate_value(self) -> None:
        entity = self._build_grc_entity()
        assert entity.cohort_profiles is not None
        q1_ur = entity.cohort_profiles["Q1"].attributes["unemployment_rate"]
        assert q1_ur.value == pytest.approx(Decimal("0.18"))

    def test_q1_poverty_headcount_is_rate(self) -> None:
        entity = self._build_grc_entity()
        assert entity.cohort_profiles is not None
        q1_ph = entity.cohort_profiles["Q1"].attributes["poverty_headcount"]
        assert q1_ph.attribute_type is AttributeType.RATE

    def test_distributional_inequality_q1_greater_than_q5(self) -> None:
        entity = self._build_grc_entity()
        assert entity.cohort_profiles is not None
        q1_ph = entity.cohort_profiles["Q1"].attributes["poverty_headcount"].value
        q5_ph = entity.cohort_profiles["Q5"].attributes["poverty_headcount"].value
        assert q1_ph > q5_ph

    def test_cohort_profile_jsonb_round_trip(self) -> None:
        entity = self._build_grc_entity()
        assert entity.cohort_profiles is not None
        q1_serialised = cohort_profile_to_jsonb(entity.cohort_profiles["Q1"])
        q1_restored = cohort_profile_from_jsonb(q1_serialised)
        assert q1_restored.attributes["poverty_headcount"].value == Decimal("0.201")
        assert q1_restored.attributes["poverty_headcount"].confidence_tier == 2
        assert q1_restored.attributes["poverty_headcount"].attribute_type is AttributeType.RATE
