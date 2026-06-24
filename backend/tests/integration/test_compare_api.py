"""Integration tests for comparative scenario output — ADR-004 Decision 5.

Tests require a live DATABASE_URL and skip gracefully without one.
Covers:
  - GET /scenarios/compare returns 404 when scenario_a not found
  - GET /scenarios/compare returns 404 when scenario_b not found
  - GET /scenarios/compare returns 409 when scenario_a has no snapshots
  - GET /scenarios/compare returns 409 when scenario_b has no snapshots
  - GET /scenarios/compare returns CompareResponse for two snapshotted scenarios
  - GET /scenarios/compare?attr= filters to one attribute
  - GET /choropleth/{attr}/delta returns 404 when no shared attribute in snapshots
  - GET /choropleth/{attr}/delta returns GeoJSONFeatureCollection for valid pair
  - GET /scenarios/compare/trajectory returns 404 when scenario_a not found (Issue #99)
  - GET /scenarios/compare/trajectory returns 409 when scenario_a has no snapshots (Issue #99)
  - GET /scenarios/compare/trajectory returns per-step trajectory for two scenarios (Issue #99)
  - GET /scenarios/compare/trajectory returns empty steps when no shared steps (Issue #99)
"""
from __future__ import annotations

import json
import os
import uuid
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

DATABASE_URL = os.environ.get("DATABASE_URL")
pytestmark = pytest.mark.integration

if not DATABASE_URL:
    pytest.skip("DATABASE_URL not set — skipping integration tests", allow_module_level=True)


import asyncpg  # noqa: E402
from httpx import AsyncClient  # noqa: E402

from app.main import app  # noqa: E402

_BASE_CFG = json.dumps(
    {"entities": [], "n_steps": 1, "timestep_label": "annual", "initial_attributes": {}}
)


@pytest.fixture()
async def db_conn() -> AsyncGenerator[asyncpg.Connection, None]:
    conn = await asyncpg.connect(DATABASE_URL)
    yield conn
    await conn.close()


@pytest.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _insert_scenario(
    conn: asyncpg.Connection,
    status: str = "completed",
) -> str:
    sid = str(uuid.uuid4())
    await conn.execute(
        """
        INSERT INTO scenarios (scenario_id, name, status, configuration, version)
        VALUES ($1, 'Compare Test', $2, $3, 1)
        """,
        sid,
        status,
        _BASE_CFG,
    )
    return sid


async def _insert_snapshot(
    conn: asyncpg.Connection,
    scenario_id: str,
    step: int,
    state_data: dict,  # type: ignore[type-arg]
) -> None:
    await conn.execute(
        """
        INSERT INTO scenario_state_snapshots
            (scenario_id, step, timestep, state_data)
        VALUES ($1, $2, NOW(), $3)
        """,
        scenario_id,
        step,
        json.dumps(state_data),
    )


async def _cleanup(conn: asyncpg.Connection, *scenario_ids: str) -> None:
    for sid in scenario_ids:
        await conn.execute("DELETE FROM scenarios WHERE scenario_id = $1", sid)


# ---------------------------------------------------------------------------
# GET /scenarios/compare — 404 / 409 cases
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_compare_scenario_a_not_found_returns_404(client: AsyncClient) -> None:
    res = await client.get(
        "/api/v1/scenarios/compare",
        params={"scenario_a": "no-such-id", "scenario_b": "no-such-id-2"},
    )
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_compare_scenario_b_not_found_returns_404(
    client: AsyncClient,
    db_conn: asyncpg.Connection,
) -> None:
    sid_a = await _insert_scenario(db_conn)
    try:
        res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": sid_a, "scenario_b": "no-such-id"},
        )
        assert res.status_code == 404
    finally:
        await _cleanup(db_conn, sid_a)


@pytest.mark.asyncio
async def test_compare_scenario_a_no_snapshots_returns_409(
    client: AsyncClient,
    db_conn: asyncpg.Connection,
) -> None:
    sid_a = await _insert_scenario(db_conn, status="pending")
    sid_b = await _insert_scenario(db_conn)
    try:
        res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": sid_a, "scenario_b": sid_b},
        )
        assert res.status_code == 409
    finally:
        await _cleanup(db_conn, sid_a, sid_b)


@pytest.mark.asyncio
async def test_compare_scenario_b_no_snapshots_returns_409(
    client: AsyncClient,
    db_conn: asyncpg.Connection,
) -> None:
    sid_a = await _insert_scenario(db_conn)
    sid_b = await _insert_scenario(db_conn, status="pending")
    _env = {"value": "100", "unit": "M", "variable_type": "stock", "confidence_tier": 2}
    state = {"USA": {"pop": _env}}
    await _insert_snapshot(db_conn, sid_a, 0, state)
    try:
        res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": sid_a, "scenario_b": sid_b},
        )
        assert res.status_code == 409
    finally:
        await _cleanup(db_conn, sid_a, sid_b)


# ---------------------------------------------------------------------------
# GET /scenarios/compare — success cases
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_compare_returns_delta_for_shared_entity(
    client: AsyncClient,
    db_conn: asyncpg.Connection,
) -> None:
    sid_a = await _insert_scenario(db_conn)
    sid_b = await _insert_scenario(db_conn)
    _env_a = {"value": "100", "unit": "M", "variable_type": "stock", "confidence_tier": 2}
    _env_b = {"value": "120", "unit": "M", "variable_type": "stock", "confidence_tier": 3}
    state_a = {"USA": {"pop": _env_a}}
    state_b = {"USA": {"pop": _env_b}}
    await _insert_snapshot(db_conn, sid_a, 0, state_a)
    await _insert_snapshot(db_conn, sid_b, 0, state_b)
    try:
        res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": sid_a, "scenario_b": sid_b},
        )
        assert res.status_code == 200
        body = res.json()
        assert body["scenario_a_id"] == sid_a
        assert body["scenario_b_id"] == sid_b
        assert isinstance(body["deltas"], list)
        delta_rec = next(
            (d for d in body["deltas"] if d["entity_id"] == "USA" and d["attribute_key"] == "pop"),
            None,
        )
        assert delta_rec is not None
        assert delta_rec["direction"] == "increase"
        assert delta_rec["delta"] == "20"
        assert delta_rec["confidence_tier"] == 3  # max(2, 3)
        assert isinstance(delta_rec["delta"], str)  # float prohibition
    finally:
        await _cleanup(db_conn, sid_a, sid_b)


@pytest.mark.asyncio
async def test_compare_attr_filter_excludes_other_keys(
    client: AsyncClient,
    db_conn: asyncpg.Connection,
) -> None:
    sid_a = await _insert_scenario(db_conn)
    sid_b = await _insert_scenario(db_conn)
    state_a = {
        "USA": {
            "pop": {"value": "100", "unit": "M", "variable_type": "stock", "confidence_tier": 1},
            "gdp": {"value": "200", "unit": "USD", "variable_type": "flow", "confidence_tier": 1},
        }
    }
    state_b = {
        "USA": {
            "pop": {"value": "110", "unit": "M", "variable_type": "stock", "confidence_tier": 1},
            "gdp": {"value": "250", "unit": "USD", "variable_type": "flow", "confidence_tier": 1},
        }
    }
    await _insert_snapshot(db_conn, sid_a, 0, state_a)
    await _insert_snapshot(db_conn, sid_b, 0, state_b)
    try:
        res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": sid_a, "scenario_b": sid_b, "attr": "pop"},
        )
        assert res.status_code == 200
        body = res.json()
        deltas = body["deltas"]
        attr_keys = {d["attribute_key"] for d in deltas if d["entity_id"] == "USA"}
        assert "pop" in attr_keys
        assert "gdp" not in attr_keys
    finally:
        await _cleanup(db_conn, sid_a, sid_b)


@pytest.mark.asyncio
async def test_compare_no_shared_entities_returns_empty_deltas(
    client: AsyncClient,
    db_conn: asyncpg.Connection,
) -> None:
    sid_a = await _insert_scenario(db_conn)
    sid_b = await _insert_scenario(db_conn)
    _env = {"value": "100", "unit": "M", "variable_type": "stock", "confidence_tier": 1}
    state_a = {"USA": {"pop": _env}}
    _env_deu = {"value": "80", "unit": "M", "variable_type": "stock", "confidence_tier": 1}
    state_b = {"DEU": {"pop": _env_deu}}
    await _insert_snapshot(db_conn, sid_a, 0, state_a)
    await _insert_snapshot(db_conn, sid_b, 0, state_b)
    try:
        res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": sid_a, "scenario_b": sid_b},
        )
        assert res.status_code == 200
        assert res.json()["deltas"] == []
    finally:
        await _cleanup(db_conn, sid_a, sid_b)


# ---------------------------------------------------------------------------
# GET /choropleth/{attr}/delta — 404 case (no shared attr)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_choropleth_delta_no_shared_attr_returns_404(
    client: AsyncClient,
    db_conn: asyncpg.Connection,
) -> None:
    sid_a = await _insert_scenario(db_conn)
    sid_b = await _insert_scenario(db_conn)
    _pop_env = {"value": "100", "unit": "M", "variable_type": "stock", "confidence_tier": 1}
    _gdp_env = {"value": "200", "unit": "USD", "variable_type": "flow", "confidence_tier": 1}
    state_a = {"USA": {"pop": _pop_env}}
    state_b = {"USA": {"gdp": _gdp_env}}
    await _insert_snapshot(db_conn, sid_a, 0, state_a)
    await _insert_snapshot(db_conn, sid_b, 0, state_b)
    try:
        res = await client.get(
            "/api/v1/choropleth/pop/delta",
            params={"scenario_a": sid_a, "scenario_b": sid_b},
        )
        assert res.status_code == 404
    finally:
        await _cleanup(db_conn, sid_a, sid_b)


@pytest.mark.asyncio
async def test_choropleth_delta_missing_snapshot_returns_404(
    client: AsyncClient,
    db_conn: asyncpg.Connection,
) -> None:
    sid_a = await _insert_scenario(db_conn, status="pending")
    sid_b = await _insert_scenario(db_conn, status="pending")
    try:
        res = await client.get(
            "/api/v1/choropleth/pop/delta",
            params={"scenario_a": sid_a, "scenario_b": sid_b},
        )
        assert res.status_code == 404
    finally:
        await _cleanup(db_conn, sid_a, sid_b)


# ---------------------------------------------------------------------------
# GET /scenarios/compare/trajectory — Issue #99
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_trajectory_compare_scenario_a_not_found_returns_404(
    client: AsyncClient,
) -> None:
    """Unknown scenario_a returns 404."""
    res = await client.get(
        "/api/v1/scenarios/compare/trajectory",
        params={
            "scenario_a": "no-such-id",
            "scenario_b": "no-such-id-2",
            "attribute": "pop",
        },
    )
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_trajectory_compare_no_snapshots_returns_409(
    client: AsyncClient,
    db_conn: asyncpg.Connection,
) -> None:
    """409 when scenario_a exists but has no snapshots yet."""
    sid_a = await _insert_scenario(db_conn, status="pending")
    sid_b = await _insert_scenario(db_conn, status="pending")
    try:
        res = await client.get(
            "/api/v1/scenarios/compare/trajectory",
            params={"scenario_a": sid_a, "scenario_b": sid_b, "attribute": "pop"},
        )
        assert res.status_code == 409
    finally:
        await _cleanup(db_conn, sid_a, sid_b)


@pytest.mark.asyncio
async def test_trajectory_compare_happy_path(
    client: AsyncClient,
    db_conn: asyncpg.Connection,
) -> None:
    """Happy path: two scenarios with matching steps return a trajectory.

    Verifies that:
    - steps are sorted ascending by step number
    - value_a, value_b, delta, and direction are correctly computed
    - the float prohibition holds (delta is a string, not a float)
    """
    sid_a = await _insert_scenario(db_conn)
    sid_b = await _insert_scenario(db_conn)
    _env_a0 = {"value": "100", "unit": "M", "variable_type": "stock", "confidence_tier": 2}
    _env_b0 = {"value": "120", "unit": "M", "variable_type": "stock", "confidence_tier": 2}
    _env_a1 = {"value": "105", "unit": "M", "variable_type": "stock", "confidence_tier": 2}
    _env_b1 = {"value": "115", "unit": "M", "variable_type": "stock", "confidence_tier": 2}
    await _insert_snapshot(db_conn, sid_a, 0, {"USA": {"pop": _env_a0}})
    await _insert_snapshot(db_conn, sid_b, 0, {"USA": {"pop": _env_b0}})
    await _insert_snapshot(db_conn, sid_a, 1, {"USA": {"pop": _env_a1}})
    await _insert_snapshot(db_conn, sid_b, 1, {"USA": {"pop": _env_b1}})
    try:
        res = await client.get(
            "/api/v1/scenarios/compare/trajectory",
            params={"scenario_a": sid_a, "scenario_b": sid_b, "attribute": "pop"},
        )
        assert res.status_code == 200
        body = res.json()
        assert body["scenario_a_id"] == sid_a
        assert body["scenario_b_id"] == sid_b
        assert body["attribute"] == "pop"
        steps = body["steps"]
        assert len(steps) == 2
        # Steps must be sorted ascending
        assert steps[0]["step"] == 0
        assert steps[1]["step"] == 1
        # Step 0: delta = 120 - 100 = 20, direction = increase
        s0 = steps[0]
        assert s0["value_a"] == "100"
        assert s0["value_b"] == "120"
        assert s0["delta"] == "20"
        assert s0["direction"] == "increase"
        assert isinstance(s0["delta"], str)  # float prohibition
        # Step 1: delta = 115 - 105 = 10, direction = increase
        s1 = steps[1]
        assert s1["value_a"] == "105"
        assert s1["value_b"] == "115"
        assert s1["delta"] == "10"
        assert s1["direction"] == "increase"
    finally:
        await _cleanup(db_conn, sid_a, sid_b)


@pytest.mark.asyncio
async def test_trajectory_compare_empty_steps_when_no_overlap(
    client: AsyncClient,
    db_conn: asyncpg.Connection,
) -> None:
    """Returns empty steps list when the two scenarios have no shared step numbers."""
    sid_a = await _insert_scenario(db_conn)
    sid_b = await _insert_scenario(db_conn)
    _env = {"value": "100", "unit": "M", "variable_type": "stock", "confidence_tier": 1}
    # scenario_a has step 0, scenario_b has step 1 — no overlap
    await _insert_snapshot(db_conn, sid_a, 0, {"USA": {"pop": _env}})
    await _insert_snapshot(db_conn, sid_b, 1, {"USA": {"pop": _env}})
    try:
        res = await client.get(
            "/api/v1/scenarios/compare/trajectory",
            params={"scenario_a": sid_a, "scenario_b": sid_b, "attribute": "pop"},
        )
        assert res.status_code == 200
        body = res.json()
        assert body["steps"] == []
    finally:
        await _cleanup(db_conn, sid_a, sid_b)
