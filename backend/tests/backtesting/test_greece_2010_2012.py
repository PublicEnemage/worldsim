"""Greece 2010–2012 backtesting test — ADR-004 Decision 3, Issue #112.

This is the primary fidelity gate for Milestone 3. It creates and runs the
Greece 2010–2012 IMF program scenario, retrieves the simulation snapshots, and
evaluates DIRECTION_ONLY fidelity thresholds against the historical actuals.

A failure here is a build failure. The first time this test passes in CI is
the Milestone 3 exit gate for the backtesting criterion (Issue #61).

Test skips gracefully when DATABASE_URL is not set. The GRC entity must exist
in simulation_entities — the natural_earth_loader seed must run before this
test in CI.

Known Limitations (printed in CI output on every run):
  IA-1: confidence tiers on projected attributes are inherited from historical
    input tiers without time-horizon degradation.
  Calibration: parameter calibration tier system not yet implemented (Issue #44).
    Thresholds are DIRECTION_ONLY — magnitude accuracy is not asserted.
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
    _extract_unemployment_value,
    format_fidelity_report,
)
from tests.fixtures.greece_2010_2012_actuals import (
    ACTUALS,
    IA1_DISCLOSURE,
    PARAMETER_CALIBRATION_DISCLOSURE,
)
from tests.fixtures.greece_2010_scenario import build_greece_scenario

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

from app.main import app

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

pytestmark = [pytest.mark.backtesting, pytest.mark.asyncio(loop_scope="session")]


def _require_db() -> None:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping Greece backtesting test")


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
    """Create, run, and fetch snapshots for the Greece scenario.

    Returns (scenario_id, snapshots_list).
    Raises AssertionError if any HTTP step fails.
    """
    scenario_req = build_greece_scenario()
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


async def test_greece_2010_2012_direction_only_fidelity(
    client: httpx.AsyncClient,
) -> None:
    """Greece 2010–2012 DIRECTION_ONLY fidelity gate — ADR-004 Decision 3.

    Thresholds checked:
      - gdp_growth at steps 1, 2, 3 must be negative (contraction predicted).
        Rationale: ACTUALS show -5.4%, -8.9%, -6.6%. Simulation must predict
        contraction, not growth. This is a DIRECTION_ONLY check — the
        simulation need not match the magnitude.
      - unemployment_rate at step 3 must exceed step 1 value if attribute
        exists in the simulation output (DIRECTION_ONLY: rising unemployment).

    KNOWN LIMITATION: Parameter calibration tier system not yet implemented
    (Issue #44). Magnitude accuracy is not evaluated in M3.
    """
    scenario_id, snapshots = await _create_and_run_scenario(client)

    try:
        snapshots_by_step = {s["step"]: s for s in snapshots}

        thresholds_met: dict[str, bool] = {}

        # DIRECTION_ONLY: gdp_growth must be negative at steps 1, 2, 3
        for step_num in [1, 2, 3]:
            snap = snapshots_by_step.get(step_num)
            key = f"gdp_growth_step{step_num}_negative"
            if snap is None:
                thresholds_met[key] = False
            else:
                val = _extract_gdp_value(snap)
                thresholds_met[key] = val is not None and val < Decimal("0")

        # DIRECTION_ONLY: unemployment rising (step 3 > step 1) if attribute present
        unemp_step1 = _extract_unemployment_value(snapshots_by_step.get(1, {}))
        unemp_step3 = _extract_unemployment_value(snapshots_by_step.get(3, {}))
        if unemp_step1 is not None and unemp_step3 is not None:
            thresholds_met["unemployment_rising_step1_to_step3"] = unemp_step3 > unemp_step1

        # Print fidelity report to stdout (appears in CI logs on every run)
        report = format_fidelity_report(
            scenario_name="Greece 2010-2012 IMF Program Backtesting Fixture",
            actuals=ACTUALS,
            snapshots=snapshots,
            thresholds_met=thresholds_met,
            ia1_disclosure=IA1_DISCLOSURE,
            parameter_calibration_disclosure=PARAMETER_CALIBRATION_DISCLOSURE,
        )
        print(f"\n{report}")

        # Assert all thresholds pass
        failed = [name for name, passed in thresholds_met.items() if not passed]
        assert not failed, (
            f"Backtesting DIRECTION_ONLY thresholds FAILED: {failed}\n"
            f"See fidelity report above.\n"
            f"{IA1_DISCLOSURE}\n"
            f"{PARAMETER_CALIBRATION_DISCLOSURE}"
        )

    finally:
        # Clean up regardless of pass/fail
        await client.delete(f"/api/v1/scenarios/{scenario_id}")


# ---------------------------------------------------------------------------
# Supplementary backtesting tests
# ---------------------------------------------------------------------------


async def test_greece_scenario_creates_correct_number_of_snapshots(
    client: httpx.AsyncClient,
) -> None:
    """Greece scenario with n_steps=3 must produce 4 snapshots (steps 0–3)."""
    scenario_id, snapshots = await _create_and_run_scenario(client)
    try:
        assert len(snapshots) == 4, (
            f"Expected 4 snapshots (steps 0–3) for n_steps=3, got {len(snapshots)}"
        )
        step_nums = sorted(s["step"] for s in snapshots)
        assert step_nums == [0, 1, 2, 3]
    finally:
        await client.delete(f"/api/v1/scenarios/{scenario_id}")


async def test_greece_snapshot_state_data_includes_gdp_growth(
    client: httpx.AsyncClient,
) -> None:
    """Every GRC snapshot must include gdp_growth in SA-09 envelope format."""
    scenario_id, snapshots = await _create_and_run_scenario(client)
    try:
        for snap in snapshots:
            step = snap["step"]
            grc = snap["state_data"].get("GRC", {})
            assert "gdp_growth" in grc, (
                f"gdp_growth missing from GRC at step {step}"
            )
            envelope = grc["gdp_growth"]
            assert envelope.get("_envelope_version") == "1", (
                f"SA-09 _envelope_version missing at step {step}"
            )
            assert isinstance(envelope.get("value"), str), (
                f"gdp_growth.value is not a string at step {step} (float prohibition)"
            )
    finally:
        await client.delete(f"/api/v1/scenarios/{scenario_id}")


async def test_greece_run_sets_status_completed(
    client: httpx.AsyncClient,
) -> None:
    """After a successful run, scenario status must be 'completed'."""
    scenario_id, _ = await _create_and_run_scenario(client)
    try:
        detail = await client.get(f"/api/v1/scenarios/{scenario_id}")
        assert detail.json()["status"] == "completed"
    finally:
        await client.delete(f"/api/v1/scenarios/{scenario_id}")
