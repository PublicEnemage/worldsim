"""Unit tests for GET /scenarios/compare step-alignment validation — Issue #150.

Covers:
  - step provided, both scenarios have it → CompareResponse with correct steps
  - step provided, scenario_a missing it → 404 identifying scenario_a
  - step provided, scenario_b missing it → 404 identifying scenario_b
  - step omitted → final-snapshot behavior (step_a/step_b from DB)

All tests run without a database connection using AsyncMock.
"""
from __future__ import annotations

import json
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from app.api.scenarios import compare_scenarios

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_SCENARIO_ROW_A = {"scenario_id": "aaa"}
_SCENARIO_ROW_B = {"scenario_id": "bbb"}

_STATE = {
    "GRC": {
        "gdp": {
            "_envelope_version": "1",
            "value": "200",
            "unit": "USD",
            "variable_type": "monetary",
            "confidence_tier": 2,
            "observation_date": None,
            "source_registry_id": None,
            "measurement_framework": None,
        }
    }
}


def _snap(step: int) -> dict:  # type: ignore[type-arg]
    return {"step": step, "state_data": json.dumps(_STATE)}


def _make_conn(
    fetchrow_effects: list,  # type: ignore[type-arg]
    fetch_a: list,  # type: ignore[type-arg]
    fetch_b: list,  # type: ignore[type-arg]
) -> AsyncMock:
    """Build a mock DB connection.

    `fetchrow_effects` — side-effects for existence-check calls (2 entries).
    `fetch_a` — rows returned for scenario_a all-snapshots fetch.
    `fetch_b` — rows returned for scenario_b all-snapshots fetch.
    """
    conn = AsyncMock()
    conn.fetchrow = AsyncMock(side_effect=list(fetchrow_effects))
    # The endpoint calls conn.fetch twice in order: scenario_a then scenario_b
    conn.fetch = AsyncMock(side_effect=[fetch_a, fetch_b])
    return conn


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_step_provided_both_present_returns_compare_response() -> None:
    conn = _make_conn(
        fetchrow_effects=[_SCENARIO_ROW_A, _SCENARIO_ROW_B],
        fetch_a=[_snap(3)],
        fetch_b=[_snap(3)],
    )
    result = await compare_scenarios(conn=conn, scenario_a="aaa", scenario_b="bbb", step=3)
    assert result.scenario_a_id == "aaa"
    assert result.scenario_b_id == "bbb"
    assert result.step_a == 3
    assert result.step_b == 3
    # Flat list — check entity_id present in at least one record
    entity_ids = {r.entity_id for r in result.deltas}
    assert "GRC" in entity_ids


@pytest.mark.asyncio
async def test_step_provided_scenario_a_missing_returns_404() -> None:
    # scenario_a has step 0 only (not step 5)
    conn = _make_conn(
        fetchrow_effects=[_SCENARIO_ROW_A, _SCENARIO_ROW_B],
        fetch_a=[_snap(0)],
        fetch_b=[_snap(5)],
    )
    with pytest.raises(HTTPException) as exc_info:
        await compare_scenarios(conn=conn, scenario_a="aaa", scenario_b="bbb", step=5)
    assert exc_info.value.status_code == 404
    assert "aaa" in exc_info.value.detail
    assert "5" in exc_info.value.detail


@pytest.mark.asyncio
async def test_step_provided_scenario_b_missing_returns_404() -> None:
    # scenario_b has step 0 only (not step 5)
    conn = _make_conn(
        fetchrow_effects=[_SCENARIO_ROW_A, _SCENARIO_ROW_B],
        fetch_a=[_snap(5)],
        fetch_b=[_snap(0)],
    )
    with pytest.raises(HTTPException) as exc_info:
        await compare_scenarios(conn=conn, scenario_a="aaa", scenario_b="bbb", step=5)
    assert exc_info.value.status_code == 404
    assert "bbb" in exc_info.value.detail
    assert "5" in exc_info.value.detail


@pytest.mark.asyncio
async def test_no_step_uses_final_snapshots() -> None:
    conn = _make_conn(
        fetchrow_effects=[_SCENARIO_ROW_A, _SCENARIO_ROW_B],
        fetch_a=[_snap(8), _snap(10)],  # max = 10
        fetch_b=[_snap(6), _snap(8)],   # max = 8
    )
    result = await compare_scenarios(conn=conn, scenario_a="aaa", scenario_b="bbb")
    assert result.step_a == 10
    assert result.step_b == 8
    assert result.scenario_a_id == "aaa"
    assert result.scenario_b_id == "bbb"
