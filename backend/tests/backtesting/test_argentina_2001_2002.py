"""Argentina 2001–2002 backtesting test — Issue #192.

This is the second backtesting case alongside Greece 2010–2012.
It validates DIRECTION_ONLY fidelity thresholds for the Argentina
currency and sovereign debt crisis.

Fidelity gate: GDP contraction predicted at both simulation steps.
  Step 1 (2001): fiscal austerity shock (Zero Deficit Plan) → GDP contracts.
  Step 2 (2002): lagged macro effect of step 1 fiscal shock → deeper contraction.

The GDP direction check is structurally correct regardless of magnitude
calibration: a large pro-cyclical fiscal cut in a depressed economy must
produce negative GDP growth per the MacroeconomicModule regime logic.

Test skips gracefully when DATABASE_URL is not set. The ARG entity must
exist in simulation_entities — the natural_earth_loader seed must run
before this test in CI (Argentina ISO 3166-1 alpha-3 = "ARG").

Thresholds registered in backtesting_thresholds as case_id='ARGENTINA_2001_2002'
(migration c7e2a9f4d1b8).
"""
from __future__ import annotations

import os
from decimal import Decimal
from typing import TYPE_CHECKING, Any

import httpx
import pytest
import pytest_asyncio

from tests.backtesting.fidelity_report import (
    _extract_gdp_value,
    format_fidelity_report,
)
from tests.fixtures.argentina_2001_2002_actuals import (
    ACTUALS,
    IA1_DISCLOSURE,
    PARAMETER_CALIBRATION_DISCLOSURE,
)
from tests.fixtures.argentina_2001_2002_scenario import build_argentina_scenario

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

from app.main import app

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

pytestmark = [pytest.mark.backtesting, pytest.mark.asyncio(loop_scope="session")]


def _require_db() -> None:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping Argentina backtesting test")


@pytest_asyncio.fixture(loop_scope="session")
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


async def _create_and_run_scenario(
    client: httpx.AsyncClient,
) -> tuple[str, list[dict[str, Any]]]:
    """Create, run, and fetch snapshots for the Argentina scenario.

    Returns (scenario_id, snapshots_list).
    Raises AssertionError if any HTTP step fails.
    """
    scenario_req = build_argentina_scenario()
    create_resp = await client.post(
        "/api/v1/scenarios",
        json=scenario_req.model_dump(mode="json"),
    )
    assert create_resp.status_code == 201, (
        f"Scenario creation failed: {create_resp.status_code} {create_resp.text}"
    )
    scenario_id: str = create_resp.json()["scenario_id"]

    run_resp = await client.post(f"/api/v1/scenarios/{scenario_id}/run")
    assert run_resp.status_code == 200, (
        f"Scenario run failed: {run_resp.status_code} {run_resp.text}"
    )
    assert run_resp.json()["final_status"] == "completed"

    snap_resp = await client.get(f"/api/v1/scenarios/{scenario_id}/snapshots")
    assert snap_resp.status_code == 200, (
        f"Snapshots fetch failed: {snap_resp.status_code} {snap_resp.text}"
    )
    snapshots: list[dict[str, Any]] = snap_resp.json()

    return scenario_id, snapshots


# ---------------------------------------------------------------------------
# Primary backtesting test
# ---------------------------------------------------------------------------


async def test_argentina_2001_2002_direction_only_fidelity(
    client: httpx.AsyncClient,
) -> None:
    """Argentina 2001–2002 DIRECTION_ONLY fidelity gate — Issue #192.

    Thresholds checked:
      - gdp_growth at steps 1 and 2 must be negative (contraction predicted).
        ACTUALS show -4.4% (2001) and -10.9% (2002). The simulation must predict
        contraction, not growth. This is DIRECTION_ONLY — magnitude not evaluated.

    Mechanism: the Zero Deficit Plan spending cut (-6.5% of GDP) injected at step 1
    propagates through MacroeconomicModule at step 2 (one-step lag), generating a
    large negative gdp_growth_change event. The initial gdp_growth of -0.8% ensures
    step 1 is also already negative before the lag resolves.

    KNOWN LIMITATION: magnitude calibration not yet implemented. DISTRIBUTION_COMBINED
    thresholds require calibrated uncertainty bands; deferred per
    PARAMETER_CALIBRATION_DISCLOSURE.
    """
    scenario_id, snapshots = await _create_and_run_scenario(client)

    try:
        snapshots_by_step = {s["step"]: s for s in snapshots}
        thresholds_met: dict[str, bool] = {}

        # DIRECTION_ONLY: gdp_growth must be negative at steps 1 and 2
        for step_num in [1, 2]:
            snap = snapshots_by_step.get(step_num)
            key = f"gdp_growth_step{step_num}_negative"
            if snap is None:
                thresholds_met[key] = False
            else:
                val = _extract_gdp_value(snap, entity_id="ARG")
                thresholds_met[key] = val is not None and val < Decimal("0")

        report = format_fidelity_report(
            scenario_name="Argentina 2001-2002 Currency and Debt Crisis Backtesting Fixture",
            actuals=ACTUALS,
            snapshots=snapshots,
            thresholds_met=thresholds_met,
            ia1_disclosure=IA1_DISCLOSURE,
            parameter_calibration_disclosure=PARAMETER_CALIBRATION_DISCLOSURE,
            entity_id="ARG",
        )
        print(f"\n{report}")

        failed = [name for name, passed in thresholds_met.items() if not passed]
        assert not failed, (
            f"Backtesting DIRECTION_ONLY thresholds FAILED: {failed}\n"
            f"See fidelity report above.\n"
            f"{IA1_DISCLOSURE}\n"
            f"{PARAMETER_CALIBRATION_DISCLOSURE}"
        )

    finally:
        await client.delete(f"/api/v1/scenarios/{scenario_id}")


# ---------------------------------------------------------------------------
# Supplementary backtesting tests
# ---------------------------------------------------------------------------


async def test_argentina_scenario_creates_correct_number_of_snapshots(
    client: httpx.AsyncClient,
) -> None:
    """Argentina scenario with n_steps=2 must produce 3 snapshots (steps 0–2)."""
    scenario_id, snapshots = await _create_and_run_scenario(client)
    try:
        assert len(snapshots) == 3, (
            f"Expected 3 snapshots (steps 0–2) for n_steps=2, got {len(snapshots)}"
        )
        step_nums = sorted(s["step"] for s in snapshots)
        assert step_nums == [0, 1, 2]
    finally:
        await client.delete(f"/api/v1/scenarios/{scenario_id}")


async def test_argentina_snapshot_state_data_includes_gdp_growth(
    client: httpx.AsyncClient,
) -> None:
    """Every ARG snapshot must include gdp_growth in SA-09 envelope format."""
    scenario_id, snapshots = await _create_and_run_scenario(client)
    try:
        for snap in snapshots:
            step = snap["step"]
            arg = snap["state_data"].get("ARG", {})
            assert "gdp_growth" in arg, (
                f"gdp_growth missing from ARG at step {step}"
            )
            envelope = arg["gdp_growth"]
            assert envelope.get("_envelope_version") == "1", (
                f"SA-09 _envelope_version missing at step {step}"
            )
            assert isinstance(envelope.get("value"), str), (
                f"gdp_growth.value is not a string at step {step} (float prohibition)"
            )
    finally:
        await client.delete(f"/api/v1/scenarios/{scenario_id}")


async def test_argentina_run_sets_status_completed(
    client: httpx.AsyncClient,
) -> None:
    """After a successful run, scenario status must be 'completed'."""
    scenario_id, _ = await _create_and_run_scenario(client)
    try:
        detail = await client.get(f"/api/v1/scenarios/{scenario_id}")
        assert detail.json()["status"] == "completed"
    finally:
        await client.delete(f"/api/v1/scenarios/{scenario_id}")
