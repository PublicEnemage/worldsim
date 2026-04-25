"""Unit tests for GET /scenarios/compare step-alignment validation — Issue #150.

Covers:
  - step provided, both scenarios have it → CompareResponse with correct steps
  - step provided, scenario_a missing it → 404 identifying scenario_a
  - step provided, scenario_b missing it → 404 identifying scenario_b
  - step omitted → existing final-snapshot behavior (step_a/step_b from DB)

All tests run without a database connection using AsyncMock.
"""
from __future__ import annotations

import json
from unittest.mock import AsyncMock

import pytest

from app.api.scenarios import compare_scenarios
from fastapi import HTTPException

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


def _snap(step: int) -> dict:
    return {"step": step, "state_data": json.dumps(_STATE)}


def _make_conn(*side_effects) -> AsyncMock:
    conn = AsyncMock()
    conn.fetchrow = AsyncMock(side_effect=list(side_effects))
    return conn


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_step_provided_both_present_returns_compare_response() -> None:
    conn = _make_conn(
        _SCENARIO_ROW_A,  # existence check scenario_a
        _SCENARIO_ROW_B,  # existence check scenario_b
        _snap(3),          # snapshot at step=3 for scenario_a
        _snap(3),          # snapshot at step=3 for scenario_b
    )
    result = await compare_scenarios(conn=conn, scenario_a="aaa", scenario_b="bbb", step=3)
    assert result.scenario_a_id == "aaa"
    assert result.scenario_b_id == "bbb"
    assert result.step_a == 3
    assert result.step_b == 3
    assert "GRC" in result.deltas


@pytest.mark.asyncio
async def test_step_provided_scenario_a_missing_returns_404() -> None:
    conn = _make_conn(
        _SCENARIO_ROW_A,
        _SCENARIO_ROW_B,
        None,  # scenario_a has no snapshot at step=5
    )
    with pytest.raises(HTTPException) as exc_info:
        await compare_scenarios(conn=conn, scenario_a="aaa", scenario_b="bbb", step=5)
    assert exc_info.value.status_code == 404
    assert "aaa" in exc_info.value.detail
    assert "5" in exc_info.value.detail


@pytest.mark.asyncio
async def test_step_provided_scenario_b_missing_returns_404() -> None:
    conn = _make_conn(
        _SCENARIO_ROW_A,
        _SCENARIO_ROW_B,
        _snap(5),  # scenario_a has step=5
        None,       # scenario_b has no snapshot at step=5
    )
    with pytest.raises(HTTPException) as exc_info:
        await compare_scenarios(conn=conn, scenario_a="aaa", scenario_b="bbb", step=5)
    assert exc_info.value.status_code == 404
    assert "bbb" in exc_info.value.detail
    assert "5" in exc_info.value.detail


@pytest.mark.asyncio
async def test_no_step_uses_final_snapshots() -> None:
    conn = _make_conn(
        _SCENARIO_ROW_A,
        _SCENARIO_ROW_B,
        _snap(10),  # final snapshot for scenario_a (step 10)
        _snap(8),   # final snapshot for scenario_b (step 8)
    )
    result = await compare_scenarios(conn=conn, scenario_a="aaa", scenario_b="bbb")
    assert result.step_a == 10
    assert result.step_b == 8
    assert result.scenario_a_id == "aaa"
    assert result.scenario_b_id == "bbb"
