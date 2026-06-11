"""Integration tests — branch snapshot copy integrity (NM-036).

NM-036 root cause: POST /scenarios/{id}/branch INSERT omitted the ia1_disclosure
NOT NULL column, causing a database constraint violation on any branch creation.
Fix merged in PR #794. These tests verify the fix holds and provide a regression
gate for any future NOT NULL column additions.

Process improvement 2 from docs/process/near-miss-registry.md NM-036:
  (a) create scenario
  (b) advance ≥1 step
  (c) call branch endpoint
  (d) confirm branch snapshot rows are complete (ia1_disclosure included)

Test strategy: ia1_disclosure is not exposed in the snapshot list API response,
so we verify completeness indirectly:
  - Branch returns 201 (INSERT succeeded — any NOT NULL violation returns 500)
  - Branch has the expected snapshot count (branch_from_step + 1)
  - Branch can be advanced (snapshots are readable and complete enough to run)
"""
from __future__ import annotations

import os
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
        pytest.skip("DATABASE_URL not set — skipping branch snapshot integrity integration test")


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    _require_db()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


def _minimal_payload(name: str = "Branch integrity test", n_steps: int = 3) -> dict[str, Any]:
    return {
        "name": name,
        "configuration": {
            "entities": [],
            "n_steps": n_steps,
            "timestep_label": "annual",
        },
        "scheduled_inputs": [],
    }


def _branch_payload(branch_from_step: int, fiscal_multiplier: float = 1.0) -> dict[str, Any]:
    return {
        "branch_from_step": branch_from_step,
        "fiscal_multiplier": fiscal_multiplier,
    }


def _rebranch_payload(from_step: int, fiscal_multiplier: float = 1.1) -> dict[str, Any]:
    return {
        "from_step": from_step,
        "fiscal_multiplier": fiscal_multiplier,
    }


# ---------------------------------------------------------------------------
# Branch endpoint — NM-036 regression gate
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_branch_returns_201_after_run(client: httpx.AsyncClient) -> None:
    """Branch endpoint must return 201 — confirms ia1_disclosure INSERT succeeds."""
    create = await client.post("/api/v1/scenarios", json=_minimal_payload(n_steps=3))
    assert create.status_code == 201
    scenario_id = create.json()["scenario_id"]

    run = await client.post(f"/api/v1/scenarios/{scenario_id}/run")
    assert run.status_code == 200
    assert run.json()["steps_executed"] == 3

    branch = await client.post(
        f"/api/v1/scenarios/{scenario_id}/branch",
        json=_branch_payload(branch_from_step=1),
    )
    assert branch.status_code == 201
    data = branch.json()
    assert data["branch_from_step"] == 1
    assert "branch_scenario_id" in data


@pytest.mark.asyncio
async def test_branch_snapshot_count_matches_branch_from_step(client: httpx.AsyncClient) -> None:
    """Branch copies snapshots 0..branch_from_step inclusive — count = branch_from_step + 1."""
    create = await client.post("/api/v1/scenarios", json=_minimal_payload(n_steps=3))
    assert create.status_code == 201
    scenario_id = create.json()["scenario_id"]

    await client.post(f"/api/v1/scenarios/{scenario_id}/run")

    branch_from_step = 2
    branch = await client.post(
        f"/api/v1/scenarios/{scenario_id}/branch",
        json=_branch_payload(branch_from_step=branch_from_step),
    )
    assert branch.status_code == 201
    branch_id = branch.json()["branch_scenario_id"]

    snapshots = await client.get(f"/api/v1/scenarios/{branch_id}/snapshots")
    assert snapshots.status_code == 200
    rows = snapshots.json()
    assert len(rows) == branch_from_step + 1, (
        f"Expected {branch_from_step + 1} snapshots in branch "
        f"(steps 0..{branch_from_step}), got {len(rows)}"
    )
    steps_present = {r["step"] for r in rows}
    assert steps_present == set(range(branch_from_step + 1))


@pytest.mark.asyncio
async def test_branch_can_be_advanced_after_creation(client: httpx.AsyncClient) -> None:
    """Branch snapshots are complete enough to advance — confirms ia1_disclosure is readable."""
    create = await client.post("/api/v1/scenarios", json=_minimal_payload(n_steps=3))
    assert create.status_code == 201
    scenario_id = create.json()["scenario_id"]

    await client.post(f"/api/v1/scenarios/{scenario_id}/run")

    branch = await client.post(
        f"/api/v1/scenarios/{scenario_id}/branch",
        json=_branch_payload(branch_from_step=1),
    )
    assert branch.status_code == 201
    branch_id = branch.json()["branch_scenario_id"]

    advance = await client.post(f"/api/v1/scenarios/{branch_id}/advance")
    assert advance.status_code == 200
    data = advance.json()
    assert data["step_executed"] == 2


@pytest.mark.asyncio
async def test_branch_at_step_zero_has_one_snapshot(client: httpx.AsyncClient) -> None:
    """Branch at step 0 produces exactly one snapshot (the initial state)."""
    create = await client.post("/api/v1/scenarios", json=_minimal_payload(n_steps=2))
    assert create.status_code == 201
    scenario_id = create.json()["scenario_id"]

    await client.post(f"/api/v1/scenarios/{scenario_id}/run")

    branch = await client.post(
        f"/api/v1/scenarios/{scenario_id}/branch",
        json=_branch_payload(branch_from_step=0),
    )
    assert branch.status_code == 201
    branch_id = branch.json()["branch_scenario_id"]

    snapshots = await client.get(f"/api/v1/scenarios/{branch_id}/snapshots")
    assert snapshots.status_code == 200
    assert len(snapshots.json()) == 1


# ---------------------------------------------------------------------------
# Branch error cases
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_branch_returns_404_for_nonexistent_scenario(client: httpx.AsyncClient) -> None:
    import uuid
    resp = await client.post(
        f"/api/v1/scenarios/{uuid.uuid4()}/branch",
        json=_branch_payload(branch_from_step=0),
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_branch_returns_404_when_no_snapshot_at_step(client: httpx.AsyncClient) -> None:
    """Cannot branch from a step that has no snapshot (scenario not yet advanced that far)."""
    create = await client.post("/api/v1/scenarios", json=_minimal_payload(n_steps=3))
    assert create.status_code == 201
    scenario_id = create.json()["scenario_id"]

    # Do NOT run — no snapshots exist
    resp = await client.post(
        f"/api/v1/scenarios/{scenario_id}/branch",
        json=_branch_payload(branch_from_step=1),
    )
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Rebranch endpoint — end-to-end completeness
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_rebranch_resets_to_from_step_and_can_advance(client: httpx.AsyncClient) -> None:
    """Rebranch deletes forward snapshots and allows re-advance from from_step."""
    create = await client.post("/api/v1/scenarios", json=_minimal_payload(n_steps=3))
    assert create.status_code == 201
    scenario_id = create.json()["scenario_id"]

    await client.post(f"/api/v1/scenarios/{scenario_id}/run")

    # Create branch with 2 snapshots (steps 0, 1)
    branch = await client.post(
        f"/api/v1/scenarios/{scenario_id}/branch",
        json=_branch_payload(branch_from_step=1),
    )
    assert branch.status_code == 201
    branch_id = branch.json()["branch_scenario_id"]

    # Advance branch to step 2
    adv = await client.post(f"/api/v1/scenarios/{branch_id}/advance")
    assert adv.status_code == 200

    # Rebranch from step 1 — truncates step 2 onward, resets to pending
    rebranch = await client.post(
        f"/api/v1/scenarios/{branch_id}/rebranch",
        json=_rebranch_payload(from_step=1),
    )
    assert rebranch.status_code == 200
    assert rebranch.json()["branch_from_step"] == 1

    # Snapshot count back to 2 after rebranch
    snapshots = await client.get(f"/api/v1/scenarios/{branch_id}/snapshots")
    assert snapshots.status_code == 200
    assert len(snapshots.json()) == 2

    # Can advance again from step 1
    adv2 = await client.post(f"/api/v1/scenarios/{branch_id}/advance")
    assert adv2.status_code == 200
    assert adv2.json()["step_executed"] == 2
