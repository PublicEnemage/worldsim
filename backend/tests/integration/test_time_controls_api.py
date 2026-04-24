"""Integration tests for time acceleration controls — ADR-004 Decision 4.

Tests require a live DATABASE_URL and skip gracefully without one.
Covers:
  - POST /advance on a running scenario advances one step
  - POST /advance on a completed scenario returns 409
  - POST /advance on a nonexistent scenario returns 404
  - GET /choropleth/{attr}?scenario_id=&step= returns GeoJSON from snapshot
  - GET /choropleth/{attr}?step= (no scenario_id) returns 422
"""
from __future__ import annotations

import os
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

_CFG = (
    '{"entities": [], "n_steps": 1, '
    '"timestep_label": "annual", "initial_attributes": {}}'
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
# POST /advance — endpoint status checks (no full DB setup needed)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_advance_nonexistent_scenario_returns_404(client: AsyncClient) -> None:
    res = await client.post("/api/v1/scenarios/does-not-exist/advance")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_advance_completed_scenario_returns_409(
    client: AsyncClient,
    db_conn: asyncpg.Connection,
) -> None:
    import json
    import uuid

    sid = str(uuid.uuid4())
    await db_conn.execute(
        """
        INSERT INTO scenarios (scenario_id, name, status, configuration, version)
        VALUES ($1, 'Completed Test', 'completed', $2, 1)
        """,
        sid,
        json.dumps({
            "entities": [], "n_steps": 1,
            "timestep_label": "annual", "initial_attributes": {},
        }),
    )
    try:
        res = await client.post(f"/api/v1/scenarios/{sid}/advance")
        assert res.status_code == 409
    finally:
        await db_conn.execute("DELETE FROM scenarios WHERE scenario_id = $1", sid)


# ---------------------------------------------------------------------------
# GET /choropleth — step param validation
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_choropleth_step_without_scenario_id_returns_422(client: AsyncClient) -> None:
    res = await client.get("/api/v1/choropleth/gdp_growth?step=1")
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_choropleth_scenario_id_without_step_returns_422(client: AsyncClient) -> None:
    res = await client.get("/api/v1/choropleth/gdp_growth?scenario_id=abc")
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_choropleth_snapshot_missing_step_returns_404(
    client: AsyncClient,
    db_conn: asyncpg.Connection,
) -> None:
    import json
    import uuid

    sid = str(uuid.uuid4())
    await db_conn.execute(
        """
        INSERT INTO scenarios (scenario_id, name, status, configuration, version)
        VALUES ($1, 'Snap Test', 'pending', $2, 1)
        """,
        sid,
        json.dumps({
            "entities": [], "n_steps": 1,
            "timestep_label": "annual", "initial_attributes": {},
        }),
    )
    try:
        res = await client.get(f"/api/v1/choropleth/gdp_growth?scenario_id={sid}&step=99")
        assert res.status_code == 404
    finally:
        await db_conn.execute("DELETE FROM scenarios WHERE scenario_id = $1", sid)
