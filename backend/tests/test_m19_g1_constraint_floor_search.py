"""
M19 G1 — Mode 3 Constraint-Floor Search (#1540)
Intent: docs/process/intents/M19-ADR-021-2026-07-02-constraint-floor-search.md
ADR: docs/adr/ADR-021-constraint-floor-search.md

All tests guard on the endpoint existing. They will be skipped (ImportError /
missing route) if the implementation is not yet present. AC-8, AC-9, AC-10
cover the backend binary search algorithm and endpoint contract.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


# ---------------------------------------------------------------------------
# Guard: skip all tests if the constraint-floor-search module is not yet present
# ---------------------------------------------------------------------------

try:
    from app.simulation.constraint_floor_search import binary_search  # type: ignore
    from app.schemas import ConstraintFloorSearchRequest, ConstraintFloorSearchResponse  # type: ignore
    IMPLEMENTATION_PRESENT = True
except ImportError:
    IMPLEMENTATION_PRESENT = False

pytestmark = pytest.mark.skipif(
    not IMPLEMENTATION_PRESENT,
    reason="Constraint-floor search not yet implemented (M19 G1 pre-implementation scaffold)",
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def focal_cohort_config():
    """Minimal valid focal cohort entry for constraint search."""
    return {
        "indicator_key": "bottom_quintile_informal_workers_poverty_headcount",
        "floor_value": 0.4,
        "floor_label": "Poverty headcount floor (bottom quintile)",
        "framework": "human_development",
        "recovery_horizon_years": 10,
    }


@pytest.fixture
def scenario_fixture(focal_cohort_config):
    """Minimal scenario object with one monitored focal cohort."""
    scenario = MagicMock()
    scenario.id = "test-scenario-001"
    scenario.configuration = {
        "monitored_focal_cohorts": [focal_cohort_config],
        "n_steps": 5,
        "entities": ["ZMB"],
    }
    return scenario


# ---------------------------------------------------------------------------
# AC-8: Binary search converges to correct boundary
# ---------------------------------------------------------------------------

def test_ac8_binary_search_converges_to_correct_boundary(
    scenario_fixture, focal_cohort_config
):
    """
    AC-8: binary_search() on a fixture scenario where fiscal_multiplier=1.18
    causes the focal cohort to just cross the floor returns boundary in [1.17, 1.19]
    within 12 evaluations.
    """
    evaluation_count = [0]

    def mock_run_trajectory(scenario, fiscal_multiplier):
        """
        Simulates a trajectory that crosses the floor at fiscal_multiplier < 1.18.
        Returns True (crosses floor) if multiplier < 1.18, False if >= 1.18.
        """
        evaluation_count[0] += 1
        return fiscal_multiplier < 1.18

    result = binary_search(
        scenario=scenario_fixture,
        focal_cohort=focal_cohort_config,
        lo=0.1,
        hi=3.0,
        tolerance=0.01,
        run_trajectory_fn=mock_run_trajectory,
    )

    assert result["status"] == "FOUND"
    boundary = result["boundary"]
    assert 1.17 <= boundary <= 1.19, (
        f"Expected boundary in [1.17, 1.19], got {boundary}"
    )
    assert evaluation_count[0] <= 12, (
        f"Expected ≤ 12 evaluations, used {evaluation_count[0]}"
    )


# ---------------------------------------------------------------------------
# AC-9: Endpoint returns ERROR when run_trajectory raises — SF-2 guard
# ---------------------------------------------------------------------------

def test_ac9_endpoint_returns_error_on_trajectory_exception(
    scenario_fixture, focal_cohort_config
):
    """
    AC-9 (SF-2): If run_trajectory raises ValueError on any binary search evaluation,
    binary_search() returns status='ERROR' — not status='FOUND' with a partial boundary.
    """
    call_count = [0]

    def raising_run_trajectory(scenario, fiscal_multiplier):
        call_count[0] += 1
        if call_count[0] >= 3:
            raise ValueError("Engine evaluation failed at step 3")
        return fiscal_multiplier < 1.18

    result = binary_search(
        scenario=scenario_fixture,
        focal_cohort=focal_cohort_config,
        lo=0.1,
        hi=3.0,
        tolerance=0.01,
        run_trajectory_fn=raising_run_trajectory,
    )

    assert result["status"] == "ERROR", (
        f"Expected ERROR status on trajectory exception, got {result['status']}"
    )
    assert result.get("boundary") is None, (
        "ERROR response must not include a boundary value"
    )


# ---------------------------------------------------------------------------
# AC-10: POST to unknown scenario returns 404
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_ac10_unknown_scenario_returns_404(async_client):
    """
    AC-10: POST /api/v1/scenarios/nonexistent-id/constraint-floor-search
    returns HTTP 404 with a JSON error body.
    """
    response = await async_client.post(
        "/api/v1/scenarios/nonexistent-id/constraint-floor-search",
        json={
            "focal_cohort_index": 0,
            "lo": 0.1,
            "hi": 3.0,
            "tolerance": 0.01,
        },
    )
    assert response.status_code == 404
    body = response.json()
    assert "detail" in body or "error" in body, (
        "404 response must contain a JSON error detail"
    )


# ---------------------------------------------------------------------------
# Schema validation guard (imports only — no logic)
# ---------------------------------------------------------------------------

def test_request_schema_valid():
    """Smoke test: ConstraintFloorSearchRequest accepts valid input."""
    req = ConstraintFloorSearchRequest(
        focal_cohort_index=0,
        lo=0.1,
        hi=3.0,
        tolerance=0.01,
    )
    assert req.focal_cohort_index == 0
    assert req.lo == pytest.approx(0.1)
    assert req.hi == pytest.approx(3.0)
    assert req.tolerance == pytest.approx(0.01)


def test_response_schema_found_valid():
    """Smoke test: ConstraintFloorSearchResponse FOUND state is constructable."""
    resp = ConstraintFloorSearchResponse(
        status="FOUND",
        boundary=1.18,
        uncertainty_lo=1.17,
        uncertainty_hi=1.19,
        evaluations=9,
        lo_searched=0.1,
        hi_searched=3.0,
        tolerance=0.01,
        focal_cohort_index=0,
    )
    assert resp.status == "FOUND"
    assert resp.boundary == pytest.approx(1.18)
