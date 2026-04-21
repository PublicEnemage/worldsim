"""Integration tests for FastAPI country endpoints — ADR-003 Decision 2.

Uses httpx.AsyncClient with ASGITransport — no running server required.
All tests skip gracefully when DATABASE_URL is not set.

Tests cover:
  GET /api/v1/health               — status ok, db connected
  GET /api/v1/countries            — list returns entity_id and name
  GET /api/v1/countries/{id}       — detail includes attributes with str values
  GET /api/v1/countries/{id}/geometry — GeoJSON Feature with valid geometry
  GET /api/v1/countries/{id}/attributes — attributes-only endpoint
  GET /api/v1/choropleth/{attr}    — FeatureCollection with attribute_value as str
  GET /api/v1/attributes/available — returns available attribute keys
"""
from __future__ import annotations

import os
from typing import Any

import pytest
import pytest_asyncio

from app.main import app

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

pytestmark = pytest.mark.integration


def _require_db() -> None:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping API integration test")


# ---------------------------------------------------------------------------
# Client fixture
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture()
async def client() -> Any:
    """httpx AsyncClient with ASGITransport pointing at the FastAPI app.

    Requires DATABASE_URL. The lifespan context manager initialises the
    asyncpg pool on startup and closes it on teardown.
    """
    _require_db()
    try:
        import httpx
    except ImportError:
        pytest.skip("httpx not installed")

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


# ---------------------------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_health_returns_ok(client: Any) -> None:
    response = await client.get("/api/v1/health/")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"] == "0.2.0"
    assert body["db"] == "connected"


# ---------------------------------------------------------------------------
# Countries list endpoint
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_countries_list_returns_summaries(client: Any) -> None:
    response = await client.get("/api/v1/countries")
    assert response.status_code == 200
    countries = response.json()
    assert isinstance(countries, list)
    if countries:
        first = countries[0]
        assert "entity_id" in first
        assert "name" in first
        assert "entity_type" in first


@pytest.mark.asyncio
async def test_countries_list_no_geometry_field(client: Any) -> None:
    response = await client.get("/api/v1/countries")
    assert response.status_code == 200
    for country in response.json():
        assert "geometry" not in country, "list endpoint must not include geometry"


@pytest.mark.asyncio
async def test_countries_list_no_attributes_field(client: Any) -> None:
    response = await client.get("/api/v1/countries")
    assert response.status_code == 200
    for country in response.json():
        assert "attributes" not in country, "list endpoint must not include attributes"


# ---------------------------------------------------------------------------
# Country detail endpoint
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_country_detail_usa(client: Any) -> None:
    response = await client.get("/api/v1/countries/USA")
    if response.status_code == 404:
        pytest.skip("USA not in database — run NE loader first")
    assert response.status_code == 200
    body = response.json()
    assert body["entity_id"] == "USA"
    assert "attributes" in body
    assert "metadata" in body


@pytest.mark.asyncio
async def test_country_detail_attributes_value_is_str(client: Any) -> None:
    response = await client.get("/api/v1/countries/USA")
    if response.status_code == 404:
        pytest.skip("USA not in database — run NE loader first")
    assert response.status_code == 200
    attrs = response.json().get("attributes", {})
    for key, qty in attrs.items():
        assert isinstance(qty["value"], str), (
            f"attributes.{key}.value must be str, got {type(qty['value'])}: {qty['value']!r}"
        )


@pytest.mark.asyncio
async def test_country_detail_not_found(client: Any) -> None:
    response = await client.get("/api/v1/countries/ZZZZZZ")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Geometry endpoint
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_country_geometry_is_geojson_feature(client: Any) -> None:
    response = await client.get("/api/v1/countries/DEU/geometry")
    if response.status_code == 404:
        pytest.skip("DEU not in database — run NE loader first")
    assert response.status_code == 200
    body = response.json()
    assert body["type"] == "Feature"
    assert "geometry" in body
    assert "properties" in body
    assert body["geometry"]["type"] in (
        "MultiPolygon", "Polygon", "GeometryCollection"
    )


@pytest.mark.asyncio
async def test_country_geometry_has_no_attributes(client: Any) -> None:
    response = await client.get("/api/v1/countries/DEU/geometry")
    if response.status_code == 404:
        pytest.skip("DEU not in database — run NE loader first")
    assert response.status_code == 200
    props = response.json()["properties"]
    assert "attributes" not in props


# ---------------------------------------------------------------------------
# Attributes-only endpoint
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_country_attributes_only(client: Any) -> None:
    response = await client.get("/api/v1/countries/BRA/attributes")
    if response.status_code == 404:
        pytest.skip("BRA not in database — run NE loader first")
    assert response.status_code == 200
    attrs = response.json()
    assert isinstance(attrs, dict)
    for key, qty in attrs.items():
        assert isinstance(qty["value"], str), (
            f"{key}.value must be str — float prohibition violated"
        )


# ---------------------------------------------------------------------------
# Choropleth endpoint
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_choropleth_returns_feature_collection(client: Any) -> None:
    response = await client.get("/api/v1/choropleth/gdp_usd_millions")
    if response.status_code == 404:
        pytest.skip("gdp_usd_millions not in database — run NE loader first")
    assert response.status_code == 200
    body = response.json()
    assert body["type"] == "FeatureCollection"
    assert isinstance(body["features"], list)


@pytest.mark.asyncio
async def test_choropleth_attribute_value_is_str(client: Any) -> None:
    response = await client.get("/api/v1/choropleth/gdp_usd_millions")
    if response.status_code == 404:
        pytest.skip("gdp_usd_millions not in database — run NE loader first")
    assert response.status_code == 200
    for feature in response.json()["features"]:
        props = feature["properties"]
        assert isinstance(props["attribute_value"], str), (
            f"choropleth attribute_value must be str for {props.get('entity_id')}, "
            f"got {type(props['attribute_value'])}"
        )


@pytest.mark.asyncio
async def test_choropleth_features_have_geometry(client: Any) -> None:
    response = await client.get("/api/v1/choropleth/gdp_usd_millions")
    if response.status_code == 404:
        pytest.skip("gdp_usd_millions not in database — run NE loader first")
    assert response.status_code == 200
    for feature in response.json()["features"]:
        assert feature["geometry"] is not None
        assert "type" in feature["geometry"]


@pytest.mark.asyncio
async def test_choropleth_territorial_note_fields_present(client: Any) -> None:
    response = await client.get("/api/v1/choropleth/gdp_usd_millions")
    if response.status_code == 404:
        pytest.skip("gdp_usd_millions not in database — run NE loader first")
    assert response.status_code == 200
    for feature in response.json()["features"]:
        props = feature["properties"]
        assert "has_territorial_note" in props
        assert isinstance(props["has_territorial_note"], bool)


@pytest.mark.asyncio
async def test_choropleth_unknown_attribute_returns_404(client: Any) -> None:
    response = await client.get("/api/v1/choropleth/does_not_exist_xyz")
    assert response.status_code == 404
    assert "does_not_exist_xyz" in response.json()["detail"]


# ---------------------------------------------------------------------------
# Available attributes endpoint
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_available_attributes_returns_list(client: Any) -> None:
    response = await client.get("/api/v1/attributes/available")
    assert response.status_code == 200
    attrs = response.json()
    assert isinstance(attrs, list)
    if attrs:
        first = attrs[0]
        assert "attribute_key" in first
        assert "unit" in first
        assert "variable_type" in first
