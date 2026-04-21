"""Unit tests for API Pydantic schemas — ADR-003 Decision 2.

Key invariants tested:
  - QuantitySchema.value is always str, never float
  - Decimal inputs are preserved exactly as strings
  - confidence_tier is int in range 1–5
  - observation_date serializes to ISO format string
  - GeoJSON schemas enforce correct type literals
"""
from __future__ import annotations

import json
from datetime import date

import pytest

from app.schemas import (
    CountryDetail,
    CountrySummary,
    GeoJSONFeature,
    GeoJSONFeatureCollection,
    HealthResponse,
    QuantitySchema,
)

# ---------------------------------------------------------------------------
# QuantitySchema — float prohibition
# ---------------------------------------------------------------------------


def test_quantity_value_is_str() -> None:
    qty = QuantitySchema(
        value="44000000000",
        unit="USD_millions_current",
        variable_type="flow",
        confidence_tier=3,
    )
    assert isinstance(qty.value, str)
    assert qty.value == "44000000000"


def test_quantity_value_not_float_in_json() -> None:
    qty = QuantitySchema(
        value="44000000000",
        unit="USD_millions_current",
        variable_type="flow",
        confidence_tier=3,
    )
    payload = json.loads(qty.model_dump_json())
    assert isinstance(payload["value"], str), (
        f"value must be str in JSON output, got {type(payload['value'])}: {payload['value']!r}"
    )


def test_quantity_decimal_string_preserves_precision() -> None:
    large_decimal = "9999999999999999.123456789"
    qty = QuantitySchema(
        value=large_decimal,
        unit="dimensionless",
        variable_type="dimensionless",
        confidence_tier=1,
    )
    assert qty.value == large_decimal


def test_quantity_from_jsonb_str_decimal() -> None:
    data = {
        "value": "1234.56",
        "unit": "USD_millions_current",
        "variable_type": "flow",
        "confidence_tier": 2,
        "observation_date": "2023-01-01",
        "source_registry_id": "WB_WDI_2024",
    }
    qty = QuantitySchema.from_jsonb(data)
    assert qty.value == "1234.56"
    assert isinstance(qty.value, str)


def test_quantity_from_jsonb_int_value_converts_to_str() -> None:
    data = {
        "value": 42,
        "unit": "dimensionless",
        "variable_type": "dimensionless",
        "confidence_tier": 3,
    }
    qty = QuantitySchema.from_jsonb(data)
    assert isinstance(qty.value, str)
    assert qty.value == "42"


def test_quantity_from_jsonb_float_value_converts_to_str() -> None:
    data = {
        "value": 3.14,
        "unit": "dimensionless",
        "variable_type": "dimensionless",
        "confidence_tier": 3,
    }
    qty = QuantitySchema.from_jsonb(data)
    assert isinstance(qty.value, str)
    # str(Decimal(str(3.14))) = "3.14"
    assert "." in qty.value


# ---------------------------------------------------------------------------
# QuantitySchema — confidence_tier
# ---------------------------------------------------------------------------


def test_confidence_tier_is_int() -> None:
    qty = QuantitySchema(
        value="100",
        unit="persons",
        variable_type="stock",
        confidence_tier=3,
    )
    assert isinstance(qty.confidence_tier, int)
    assert qty.confidence_tier == 3


@pytest.mark.parametrize("tier", [1, 2, 3, 4, 5])
def test_confidence_tier_valid_range(tier: int) -> None:
    qty = QuantitySchema(
        value="0",
        unit="dimensionless",
        variable_type="dimensionless",
        confidence_tier=tier,
    )
    assert qty.confidence_tier == tier


# ---------------------------------------------------------------------------
# QuantitySchema — observation_date serialization
# ---------------------------------------------------------------------------


def test_observation_date_none_allowed() -> None:
    qty = QuantitySchema(
        value="0",
        unit="dimensionless",
        variable_type="dimensionless",
        confidence_tier=5,
        observation_date=None,
    )
    assert qty.observation_date is None
    payload = json.loads(qty.model_dump_json())
    assert payload["observation_date"] is None


def test_observation_date_serializes_to_iso_string() -> None:
    qty = QuantitySchema(
        value="0",
        unit="dimensionless",
        variable_type="dimensionless",
        confidence_tier=1,
        observation_date=date(2024, 1, 1),
    )
    payload = json.loads(qty.model_dump_json())
    assert payload["observation_date"] == "2024-01-01"


def test_quantity_from_jsonb_observation_date_parsed() -> None:
    data = {
        "value": "5.0",
        "unit": "dimensionless",
        "variable_type": "dimensionless",
        "confidence_tier": 3,
        "observation_date": "2024-01-01",
    }
    qty = QuantitySchema.from_jsonb(data)
    assert qty.observation_date == date(2024, 1, 1)


def test_quantity_from_jsonb_invalid_date_falls_back_to_none() -> None:
    data = {
        "value": "5.0",
        "unit": "dimensionless",
        "variable_type": "dimensionless",
        "confidence_tier": 3,
        "observation_date": "not-a-date",
    }
    qty = QuantitySchema.from_jsonb(data)
    assert qty.observation_date is None


# ---------------------------------------------------------------------------
# CountrySummary
# ---------------------------------------------------------------------------


def test_country_summary_fields() -> None:
    summary = CountrySummary(
        entity_id="GRC",
        entity_type="country",
        name="Greece",
        iso_a2="GR",
        iso_a3="GRC",
    )
    assert summary.entity_id == "GRC"
    assert summary.name == "Greece"


# ---------------------------------------------------------------------------
# CountryDetail
# ---------------------------------------------------------------------------


def test_country_detail_attributes_are_quantity_schemas() -> None:
    detail = CountryDetail(
        entity_id="GRC",
        entity_type="country",
        name="Greece",
        iso_a2="GR",
        iso_a3="GRC",
        metadata={"note": "test"},
        attributes={
            "gdp_usd_millions": QuantitySchema(
                value="184000",
                unit="USD_millions_current",
                variable_type="flow",
                confidence_tier=3,
            )
        },
    )
    assert isinstance(detail.attributes["gdp_usd_millions"], QuantitySchema)
    assert detail.attributes["gdp_usd_millions"].value == "184000"


# ---------------------------------------------------------------------------
# GeoJSON schemas
# ---------------------------------------------------------------------------


def test_geojson_feature_type_literal() -> None:
    feature = GeoJSONFeature(
        geometry={"type": "MultiPolygon", "coordinates": []},
        properties={"entity_id": "GRC"},
    )
    assert feature.type == "Feature"


def test_geojson_feature_collection_type_literal() -> None:
    fc = GeoJSONFeatureCollection(features=[])
    assert fc.type == "FeatureCollection"
    assert fc.features == []


def test_geojson_feature_collection_serializes_cleanly() -> None:
    fc = GeoJSONFeatureCollection(
        features=[
            GeoJSONFeature(
                geometry={"type": "MultiPolygon", "coordinates": []},
                properties={"entity_id": "GRC", "attribute_value": "184000"},
            )
        ]
    )
    payload = json.loads(fc.model_dump_json())
    assert payload["type"] == "FeatureCollection"
    assert len(payload["features"]) == 1
    assert payload["features"][0]["properties"]["attribute_value"] == "184000"


# ---------------------------------------------------------------------------
# HealthResponse
# ---------------------------------------------------------------------------


def test_health_response_structure() -> None:
    hr = HealthResponse(status="ok", version="0.2.0", db="connected")
    assert hr.status == "ok"
    assert hr.db == "connected"
