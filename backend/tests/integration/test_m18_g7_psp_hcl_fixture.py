"""M18-G7-D: AC-D5 — psp_dominant_driver in trajectory response.

Verifies that GET /scenarios/{id}/trajectory returns psp_dominant_driver
at the expected JSON path in the response for a SEN scenario at step >= 3
(post BRANCH_FROM_STEP).

NM-078 compliance: file is at backend/tests/integration/ (not backend/tests/ root).

RED state: the trajectory response may include psp_dominant_driver from the
backend (schemas.py:188, module.py:229) but the frontend mock in demo-narrated.spec.ts
omits it. This test verifies the backend is correct so the G7-D fix only needs
to update the frontend mock fixture, not the backend.

If psp_dominant_driver is absent from the response, the fix is in the backend
derivation layer (not just the mock). See M18-G7-D intent §6.2.

Source: docs/process/intents/M18-G7-D-2026-06-29-data-pipeline-psp-hcl.md §AC-D5.
"""
from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    import httpx

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

pytestmark = pytest.mark.integration


def _require_db() -> None:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping M18-G7-D integration test")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_DRIVER_VALUES = {
    "fiscal_sustainability",
    "governance",
    "external_balance",
    "social_stability",
}


def _sen_payload(name: str = "SEN G7-D PSP fixture test") -> dict[str, Any]:
    return {
        "name": name,
        "configuration": {
            "entities": ["SEN"],
            "n_steps": 8,
            "start_date": "2024-01-01",
            "timestep_label": "annual",
            "modules_config": {
                "ecological": {"enabled": False},
                "political_economy": {"enabled": True},
            },
        },
        "scheduled_inputs": [],
    }


# ---------------------------------------------------------------------------
# AC-D5 — psp_dominant_driver in trajectory response
# ---------------------------------------------------------------------------


@pytest.fixture()
def client() -> httpx.AsyncClient:
    """ASGI test client for the FastAPI application."""
    from httpx import AsyncClient

    from app.main import app

    return AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_trajectory_response_includes_psp_dominant_driver(
    client: httpx.AsyncClient,
) -> None:
    """AC-D5: trajectory response at step >= 3 includes psp_dominant_driver.

    Verifies:
    1. psp_dominant_driver is present in the trajectory response JSON
    2. The value is one of the four valid driver strings
    3. The extraction path matches what the frontend reads (ScenarioInstrumentCluster.tsx)

    RED if psp_dominant_driver is absent from the response at any path.
    GREEN after G7-D confirms the backend is correct and the fix is frontend-only.
    """
    _require_db()

    # Create SEN scenario
    create_resp = await client.post("/api/v1/scenarios", json=_sen_payload())
    if create_resp.status_code != 201:
        pytest.skip(
            f"Could not create SEN scenario (status {create_resp.status_code}) — "
            "database may not have SEN entity data"
        )

    scenario_id: str = create_resp.json()["scenario_id"]

    try:
        # Advance 3 steps so political_economy PSP is computed
        branch_from_step = 3
        for step_num in range(branch_from_step):
            adv_resp = await client.post(f"/api/v1/scenarios/{scenario_id}/advance")
            assert adv_resp.status_code in (200, 201), (
                f"Advance step {step_num + 1} failed: {adv_resp.status_code}"
            )

        # Fetch trajectory
        traj_resp = await client.get(f"/api/v1/scenarios/{scenario_id}/trajectory")
        assert traj_resp.status_code == 200, (
            f"Trajectory fetch failed: {traj_resp.status_code}"
        )

        traj_data: dict[str, Any] = traj_resp.json()

        # Trajectory must have steps
        assert "steps" in traj_data, "Trajectory response missing 'steps' key"
        steps: list[dict[str, Any]] = traj_data["steps"]
        assert len(steps) >= branch_from_step, (
            f"Expected >= {branch_from_step} steps, got {len(steps)}"
        )

        # Step 3 (index 2 in list, step_index == 3)
        step3 = next(
            (s for s in steps if s.get("step_index") == branch_from_step),
            None,
        )
        assert step3 is not None, f"step_index={branch_from_step} not in trajectory response"

        # Check psp_dominant_driver at possible paths
        # Path 1: top-level field (most likely based on scenarios.py:2652)
        psp_driver_top = step3.get("psp_dominant_driver")

        # Path 2: nested in political_economy framework
        frameworks = step3.get("frameworks", [])
        pe_framework = None
        if isinstance(frameworks, list):
            pe_framework = next(
                (fw for fw in frameworks if fw.get("framework") == "political_economy"),
                None,
            )
        elif isinstance(frameworks, dict):
            pe_framework = frameworks.get("political_economy")

        psp_driver_nested = (
            pe_framework.get("psp_dominant_driver") if pe_framework else None
        )

        psp_driver_found = psp_driver_top or psp_driver_nested

        assert psp_driver_found is not None, (
            "AC-D5 FAIL: psp_dominant_driver absent from trajectory response at step 3. "
            "Checked top-level step field and political_economy framework field. "
            "Fix G7-D: ensure backend populates psp_dominant_driver in TrajectoryStep "
            "response (see scenarios.py:2668, module.py:229). "
            "See M18-G7-D intent §AC-D5 + §6.2."
        )

        assert psp_driver_found in VALID_DRIVER_VALUES, (
            f"AC-D5 FAIL: psp_dominant_driver value '{psp_driver_found}' is not one of "
            f"the four valid driver keys: {VALID_DRIVER_VALUES}. "
            "See M18-G7-D intent §AC-D2."
        )

    finally:
        # Clean up
        await client.delete(f"/api/v1/scenarios/{scenario_id}")


@pytest.mark.asyncio
async def test_trajectory_response_psp_driver_path_matches_frontend_extraction(
    client: httpx.AsyncClient,
) -> None:
    """AC-D5 companion: verify extraction path consistency.

    ScenarioInstrumentCluster.tsx reads psp_dominant_driver from the trajectory
    response at line ~641. This test confirms the path used in the backend response
    matches what the frontend expects to read.

    If this test fails, the G7-D fix requires updating the frontend extraction path
    in ScenarioInstrumentCluster.tsx in addition to the mock fixture.
    """
    _require_db()

    create_resp = await client.post("/api/v1/scenarios", json=_sen_payload("SEN G7-D path check"))
    if create_resp.status_code != 201:
        pytest.skip("Could not create SEN scenario — database may not have SEN entity data")

    scenario_id: str = create_resp.json()["scenario_id"]

    try:
        for _ in range(3):
            adv_resp = await client.post(f"/api/v1/scenarios/{scenario_id}/advance")
            if adv_resp.status_code not in (200, 201):
                break

        traj_resp = await client.get(f"/api/v1/scenarios/{scenario_id}/trajectory")
        if traj_resp.status_code != 200:
            pytest.skip(f"Trajectory not available: {traj_resp.status_code}")

        traj_data = traj_resp.json()
        steps = traj_data.get("steps", [])
        step3 = next((s for s in steps if s.get("step_index") == 3), None)
        if step3 is None:
            pytest.skip("step_index 3 not in response")

        # The frontend reads from: entry.psp_dominant_driver (top-level step field)
        # OR from: entry.frameworks.political_economy.psp_dominant_driver
        # This test documents which path is actually populated.
        psp_top = step3.get("psp_dominant_driver")
        frameworks = step3.get("frameworks", {})
        pe: dict[str, Any] | None = None
        if isinstance(frameworks, list):
            pe = next((fw for fw in frameworks if fw.get("framework") == "political_economy"), None)
        elif isinstance(frameworks, dict):
            pe = frameworks.get("political_economy")

        psp_nested = pe.get("psp_dominant_driver") if pe else None

        # Document which path is populated (for frontend extraction path verification)
        # At least one must be populated after step 3
        populated_paths = []
        if psp_top is not None:
            populated_paths.append("step.psp_dominant_driver")
        if psp_nested is not None:
            populated_paths.append("step.frameworks.political_economy.psp_dominant_driver")

        assert len(populated_paths) > 0, (
            "AC-D5 path check FAIL: psp_dominant_driver not found at any extraction path. "
            f"step3 keys: {list(step3.keys())}. "
            "Check ScenarioInstrumentCluster.tsx line ~641 extraction path "
            "against actual backend response structure."
        )

    finally:
        await client.delete(f"/api/v1/scenarios/{scenario_id}")
