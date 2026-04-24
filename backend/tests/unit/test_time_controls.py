"""Unit tests for time acceleration controls — ADR-004 Decision 4.

Tests run without a database connection. Covers:
  - AdvanceResponse schema validation
  - StepSummary dataclass construction
  - run_single_step raises ValueError on completed scenario
  - Choropleth step-without-scenario_id returns 422 (via FastAPI routing)
"""
from __future__ import annotations

import pytest

from app.schemas import AdvanceResponse
from app.simulation.web_scenario_runner import StepSummary  # noqa: TCH001

# ---------------------------------------------------------------------------
# AdvanceResponse schema
# ---------------------------------------------------------------------------


def test_advance_response_valid() -> None:
    r = AdvanceResponse(
        scenario_id="abc",
        step_executed=1,
        steps_remaining=2,
        final_status="running",
        is_complete=False,
    )
    assert r.scenario_id == "abc"
    assert r.step_executed == 1
    assert r.steps_remaining == 2
    assert r.final_status == "running"
    assert r.is_complete is False


def test_advance_response_complete() -> None:
    r = AdvanceResponse(
        scenario_id="xyz",
        step_executed=3,
        steps_remaining=0,
        final_status="completed",
        is_complete=True,
    )
    assert r.is_complete is True
    assert r.steps_remaining == 0
    assert r.final_status == "completed"


def test_advance_response_serialises_to_dict() -> None:
    r = AdvanceResponse(
        scenario_id="s1",
        step_executed=2,
        steps_remaining=1,
        final_status="running",
        is_complete=False,
    )
    d = r.model_dump()
    assert d["scenario_id"] == "s1"
    assert d["step_executed"] == 2
    assert d["is_complete"] is False


# ---------------------------------------------------------------------------
# StepSummary dataclass
# ---------------------------------------------------------------------------


def test_step_summary_running() -> None:
    s = StepSummary(
        scenario_id="s1",
        step_executed=1,
        steps_remaining=2,
        final_status="running",
        is_complete=False,
    )
    assert s.step_executed == 1
    assert s.is_complete is False


def test_step_summary_complete() -> None:
    s = StepSummary(
        scenario_id="s1",
        step_executed=3,
        steps_remaining=0,
        final_status="completed",
        is_complete=True,
    )
    assert s.steps_remaining == 0
    assert s.is_complete is True


# ---------------------------------------------------------------------------
# run_single_step raises ValueError on completed scenario (mocked conn)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_run_single_step_raises_on_completed() -> None:
    """run_single_step raises ValueError when scenario status is 'completed'."""
    from unittest.mock import AsyncMock, MagicMock

    from app.simulation.web_scenario_runner import WebScenarioRunner

    conn = MagicMock()
    conn.fetchrow = AsyncMock(
        return_value={
            "scenario_id": "s1",
            "name": "Test",
            "status": "completed",
            "configuration": (
                '{"entities": ["GRC"], "n_steps": 3, '
                '"timestep_label": "annual", "initial_attributes": {}}'
            ),
        }
    )

    with pytest.raises(ValueError, match="already completed"):
        await WebScenarioRunner().run_single_step(conn, "s1")


@pytest.mark.asyncio
async def test_run_single_step_raises_on_not_found() -> None:
    """run_single_step raises ValueError when scenario does not exist."""
    from unittest.mock import AsyncMock, MagicMock

    from app.simulation.web_scenario_runner import WebScenarioRunner

    conn = MagicMock()
    conn.fetchrow = AsyncMock(return_value=None)

    with pytest.raises(ValueError, match="not found"):
        await WebScenarioRunner().run_single_step(conn, "nonexistent")


# ---------------------------------------------------------------------------
# Choropleth 422 when only step provided without scenario_id
# ---------------------------------------------------------------------------


def test_choropleth_step_without_scenario_id_is_422() -> None:
    """Providing step without scenario_id must return 422 from the FastAPI route.

    This test validates the validation logic directly on the choropleth function
    signature without going through TestClient (which requires a running DB).
    """
    import asyncio
    from unittest.mock import MagicMock

    from fastapi import HTTPException

    from app.api.countries import choropleth

    conn = MagicMock()

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(choropleth(attribute_key="gdp_growth", conn=conn, scenario_id=None, step=5))

    assert exc_info.value.status_code == 422


def test_choropleth_scenario_id_without_step_is_422() -> None:
    """Providing scenario_id without step must return 422 from the FastAPI route."""
    import asyncio
    from unittest.mock import MagicMock

    from fastapi import HTTPException

    from app.api.countries import choropleth

    conn = MagicMock()

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            choropleth(attribute_key="gdp_growth", conn=conn, scenario_id="s1", step=None)
        )

    assert exc_info.value.status_code == 422
