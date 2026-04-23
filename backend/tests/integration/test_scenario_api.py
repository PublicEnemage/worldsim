"""Integration tests for scenario API endpoints — ADR-004 Decision 1.

Uses httpx.AsyncClient with ASGITransport — no running server required.
All tests skip gracefully when DATABASE_URL is not set.

Tests cover:
  POST   /api/v1/scenarios        — create, validation failures
  GET    /api/v1/scenarios        — list returns newest first
  GET    /api/v1/scenarios/{id}   — detail includes configuration and inputs
  DELETE /api/v1/scenarios/{id}   — delete cascades, returns 204
"""
from __future__ import annotations

import os
import uuid
from typing import TYPE_CHECKING, Any

import httpx
import pytest
import pytest_asyncio

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

from app.main import app

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

pytestmark = pytest.mark.integration


def _require_db() -> None:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping scenario API integration test")


# ---------------------------------------------------------------------------
# Client fixture
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    _require_db()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _minimal_payload(name: str = "Test scenario", n_steps: int = 2) -> dict[str, Any]:
    return {
        "name": name,
        "configuration": {
            "entities": ["GRC"],
            "n_steps": n_steps,
            "timestep_label": "annual",
        },
        "scheduled_inputs": [],
    }


# ---------------------------------------------------------------------------
# POST /scenarios — happy path
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_scenario_returns_201(client: httpx.AsyncClient) -> None:
    resp = await client.post("/api/v1/scenarios", json=_minimal_payload())
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "pending"
    assert data["version"] == 1
    assert "scenario_id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_scenario_name_preserved(client: httpx.AsyncClient) -> None:
    resp = await client.post(
        "/api/v1/scenarios", json=_minimal_payload(name="Greece austerity 2010")
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Greece austerity 2010"


@pytest.mark.asyncio
async def test_create_scenario_with_scheduled_inputs(client: httpx.AsyncClient) -> None:
    payload = _minimal_payload(n_steps=3)
    payload["scheduled_inputs"] = [
        {
            "step": 0,
            "input_type": "EmergencyPolicyInput",
            "input_data": {"instrument": "IMF_PROGRAM_ACCEPTANCE"},
        }
    ]
    resp = await client.post("/api/v1/scenarios", json=payload)
    assert resp.status_code == 201


# ---------------------------------------------------------------------------
# POST /scenarios — validation failures
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_scenario_empty_name_returns_422(client: httpx.AsyncClient) -> None:
    resp = await client.post("/api/v1/scenarios", json=_minimal_payload(name=""))
    assert resp.status_code == 422
    assert "name" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_create_scenario_n_steps_zero_returns_422(client: httpx.AsyncClient) -> None:
    payload = _minimal_payload()
    payload["configuration"]["n_steps"] = 0
    resp = await client.post("/api/v1/scenarios", json=payload)
    assert resp.status_code == 422
    assert "n_steps" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_create_scenario_n_steps_101_returns_422(client: httpx.AsyncClient) -> None:
    payload = _minimal_payload()
    payload["configuration"]["n_steps"] = 101
    resp = await client.post("/api/v1/scenarios", json=payload)
    assert resp.status_code == 422
    assert "n_steps" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_create_scenario_out_of_range_step_returns_422(
    client: httpx.AsyncClient,
) -> None:
    payload = _minimal_payload(n_steps=2)
    payload["scheduled_inputs"] = [
        {"step": 5, "input_type": "FiscalPolicyInput", "input_data": {}}
    ]
    resp = await client.post("/api/v1/scenarios", json=payload)
    assert resp.status_code == 422
    assert "step" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_create_scenario_missing_entity_returns_422(
    client: httpx.AsyncClient,
) -> None:
    payload = _minimal_payload()
    payload["configuration"]["entities"] = ["NOTANENTITY_XYZ"]
    resp = await client.post("/api/v1/scenarios", json=payload)
    assert resp.status_code == 422
    assert "NOTANENTITY_XYZ" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# GET /scenarios
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_scenarios_returns_list(client: httpx.AsyncClient) -> None:
    resp = await client.get("/api/v1/scenarios")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_list_scenarios_newest_first(client: httpx.AsyncClient) -> None:
    suffix = uuid.uuid4().hex[:6]
    await client.post("/api/v1/scenarios", json=_minimal_payload(name=f"first-{suffix}"))
    await client.post("/api/v1/scenarios", json=_minimal_payload(name=f"second-{suffix}"))
    resp = await client.get("/api/v1/scenarios")
    assert resp.status_code == 200
    names = [s["name"] for s in resp.json() if suffix in s["name"]]
    assert names[0] == f"second-{suffix}"
    assert names[1] == f"first-{suffix}"


# ---------------------------------------------------------------------------
# GET /scenarios/{scenario_id}
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_scenario_returns_detail(client: httpx.AsyncClient) -> None:
    create = await client.post("/api/v1/scenarios", json=_minimal_payload())
    assert create.status_code == 201
    scenario_id = create.json()["scenario_id"]

    resp = await client.get(f"/api/v1/scenarios/{scenario_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["scenario_id"] == scenario_id
    assert "configuration" in data
    assert data["configuration"]["n_steps"] == 2
    assert isinstance(data["scheduled_inputs"], list)


@pytest.mark.asyncio
async def test_get_scenario_includes_scheduled_inputs(client: httpx.AsyncClient) -> None:
    payload = _minimal_payload(n_steps=3)
    payload["scheduled_inputs"] = [
        {
            "step": 1,
            "input_type": "FiscalPolicyInput",
            "input_data": {"instrument": "SPENDING_CHANGE", "value": "-0.05"},
        }
    ]
    create = await client.post("/api/v1/scenarios", json=payload)
    scenario_id = create.json()["scenario_id"]

    resp = await client.get(f"/api/v1/scenarios/{scenario_id}")
    assert resp.status_code == 200
    inputs = resp.json()["scheduled_inputs"]
    assert len(inputs) == 1
    assert inputs[0]["step"] == 1
    assert inputs[0]["input_type"] == "FiscalPolicyInput"


@pytest.mark.asyncio
async def test_get_scenario_not_found_returns_404(client: httpx.AsyncClient) -> None:
    resp = await client.get(f"/api/v1/scenarios/{uuid.uuid4()}")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /scenarios/{scenario_id}
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_delete_scenario_returns_204(client: httpx.AsyncClient) -> None:
    create = await client.post("/api/v1/scenarios", json=_minimal_payload())
    scenario_id = create.json()["scenario_id"]

    resp = await client.delete(f"/api/v1/scenarios/{scenario_id}")
    assert resp.status_code == 204
    assert resp.content == b""


@pytest.mark.asyncio
async def test_delete_scenario_removes_from_list(client: httpx.AsyncClient) -> None:
    suffix = uuid.uuid4().hex[:6]
    create = await client.post(
        "/api/v1/scenarios", json=_minimal_payload(name=f"to-delete-{suffix}")
    )
    scenario_id = create.json()["scenario_id"]
    await client.delete(f"/api/v1/scenarios/{scenario_id}")

    resp = await client.get("/api/v1/scenarios")
    ids = [s["scenario_id"] for s in resp.json()]
    assert scenario_id not in ids


@pytest.mark.asyncio
async def test_delete_scenario_not_found_returns_404(client: httpx.AsyncClient) -> None:
    resp = await client.delete(f"/api/v1/scenarios/{uuid.uuid4()}")
    assert resp.status_code == 404
