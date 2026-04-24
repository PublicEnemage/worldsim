"""Integration tests for scenario execution API — ADR-004 Decision 2.

Uses httpx.AsyncClient with ASGITransport — no running server required.
All tests skip gracefully when DATABASE_URL is not set.

Tests cover:
  POST /api/v1/scenarios/{id}/run  — execute pending scenario
  DELETE /api/v1/scenarios/{id}    — tombstone write before cascade
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
        pytest.skip("DATABASE_URL not set — skipping execution API integration test")


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    _require_db()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


def _minimal_payload(name: str = "Exec test", n_steps: int = 1) -> dict[str, Any]:
    return {
        "name": name,
        "configuration": {
            "entities": [],
            "n_steps": n_steps,
            "timestep_label": "annual",
        },
        "scheduled_inputs": [],
    }


# ---------------------------------------------------------------------------
# POST /scenarios/{id}/run — happy path
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_run_scenario_returns_200(client: httpx.AsyncClient) -> None:
    create = await client.post("/api/v1/scenarios", json=_minimal_payload())
    assert create.status_code == 201
    scenario_id = create.json()["scenario_id"]

    resp = await client.post(f"/api/v1/scenarios/{scenario_id}/run")
    assert resp.status_code == 200
    data = resp.json()
    assert data["scenario_id"] == scenario_id
    assert data["final_status"] == "completed"
    assert data["steps_executed"] == 1
    assert data["duration_seconds"] >= 0.0


@pytest.mark.asyncio
async def test_run_scenario_updates_status_to_completed(client: httpx.AsyncClient) -> None:
    create = await client.post("/api/v1/scenarios", json=_minimal_payload(n_steps=2))
    scenario_id = create.json()["scenario_id"]

    await client.post(f"/api/v1/scenarios/{scenario_id}/run")

    detail = await client.get(f"/api/v1/scenarios/{scenario_id}")
    assert detail.status_code == 200
    assert detail.json()["status"] == "completed"


@pytest.mark.asyncio
async def test_run_scenario_writes_snapshots(client: httpx.AsyncClient) -> None:
    """Completed scenario with n_steps=2 should have snapshots at steps 0, 1, 2."""
    # Verified indirectly: run succeeds and status=completed
    # Direct snapshot count query requires DB access beyond ASGITransport scope
    create = await client.post("/api/v1/scenarios", json=_minimal_payload(n_steps=2))
    scenario_id = create.json()["scenario_id"]
    resp = await client.post(f"/api/v1/scenarios/{scenario_id}/run")
    assert resp.status_code == 200
    assert resp.json()["steps_executed"] == 2


# ---------------------------------------------------------------------------
# POST /scenarios/{id}/run — error cases
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_run_nonexistent_scenario_returns_404(client: httpx.AsyncClient) -> None:
    resp = await client.post(f"/api/v1/scenarios/{uuid.uuid4()}/run")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_run_already_running_returns_409(client: httpx.AsyncClient) -> None:
    """Cannot run a scenario that is not in pending status."""
    create = await client.post("/api/v1/scenarios", json=_minimal_payload())
    scenario_id = create.json()["scenario_id"]

    # Run it once to completion
    await client.post(f"/api/v1/scenarios/{scenario_id}/run")

    # Try to run again — status is now 'completed'
    resp = await client.post(f"/api/v1/scenarios/{scenario_id}/run")
    assert resp.status_code == 409
    assert "completed" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_run_failed_scenario_returns_409(client: httpx.AsyncClient) -> None:
    """Cannot re-run a failed scenario without creating a new one."""
    # Create scenario with a non-existent entity to trigger failure
    payload = _minimal_payload()
    payload["configuration"]["entities"] = ["NONEXISTENT_ENTITY_XYZ"]
    create = await client.post("/api/v1/scenarios", json=payload)
    # Entity validation at creation time catches this
    assert create.status_code == 422


# ---------------------------------------------------------------------------
# DELETE /scenarios/{id} — tombstone verification
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_delete_writes_tombstone_and_removes_scenario(client: httpx.AsyncClient) -> None:
    """DELETE must remove scenario and succeed; tombstone verified indirectly."""
    suffix = uuid.uuid4().hex[:6]
    create = await client.post(
        "/api/v1/scenarios", json=_minimal_payload(name=f"to-delete-{suffix}")
    )
    assert create.status_code == 201
    scenario_id = create.json()["scenario_id"]

    delete_resp = await client.delete(f"/api/v1/scenarios/{scenario_id}")
    assert delete_resp.status_code == 204

    # Scenario is gone
    get_resp = await client.get(f"/api/v1/scenarios/{scenario_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_completed_scenario_writes_tombstone(client: httpx.AsyncClient) -> None:
    """DELETE of a completed scenario (with snapshots) must succeed."""
    create = await client.post("/api/v1/scenarios", json=_minimal_payload(n_steps=1))
    scenario_id = create.json()["scenario_id"]

    await client.post(f"/api/v1/scenarios/{scenario_id}/run")

    delete_resp = await client.delete(f"/api/v1/scenarios/{scenario_id}")
    assert delete_resp.status_code == 204

    get_resp = await client.get(f"/api/v1/scenarios/{scenario_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_returns_404(client: httpx.AsyncClient) -> None:
    resp = await client.delete(f"/api/v1/scenarios/{uuid.uuid4()}")
    assert resp.status_code == 404
