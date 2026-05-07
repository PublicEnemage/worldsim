"""Lebanon 2019–2020 backtesting test — Issue #207.

This is the fourth backtesting case alongside Greece 2010–2012, Argentina
2001–2002, and Thailand 1997–2000. It validates DIRECTION_ONLY fidelity
thresholds for the Lebanon financial collapse crisis.

Fidelity gate: GDP contraction predicted at both simulation steps.
  Step 1 (2019): Bank deposit freeze (capital controls) seeds a fiscal
    spending collapse at step 1. Initial gdp_growth is already negative
    (-2.0%), so step 1 is negative without requiring MacroeconomicModule
    to fire (one-step lag design).
  Step 2 (2020): MacroeconomicModule processes the step 1 fiscal spending
    cut (-10% of GDP) under the depressed regime (multiplier 1.5), generating
    a large negative gdp_growth_change delta. Step 2 GDP is deeply negative.

The GDP direction check is structurally correct regardless of magnitude
calibration: an acute banking system crisis forcing fiscal collapse in an
already-contracting economy must produce negative GDP growth per the
MacroeconomicModule regime logic.

CASCADE dynamics forward reference:
  Lebanon 2019–2020 exemplifies the CASCADE propagation failure mode
  (CLAUDE.md §Failure Mode Architecture): banking system insolvency →
  currency peg collapse → real economy contraction → social fabric breakdown.
  Each domain's failure accelerated the others in a reinforcing cascade.
  The M6 simulation captures the macro-fiscal channel but not the full
  cross-domain cascade. Once the CASCADE propagation mode is implemented
  (Issue #29), Lebanon 2019–2020 is the primary candidate for validating
  that the cascade multiplier correctly amplifies the individual-domain
  effects modeled here. This test should be extended at that point to
  include cascade-specific fidelity thresholds.

Test skips gracefully when DATABASE_URL is not set. The LBN entity must
exist in simulation_entities — the natural_earth_loader seed must run
before this test in CI (Lebanon ISO 3166-1 alpha-3 = "LBN").

Thresholds registered in backtesting_thresholds as case_id='LEBANON_2019_2020'
(migration d4b8f3a2e7c1).
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
from tests.fixtures.lebanon_2019_2020_actuals import (
    ACTUALS,
    IA1_DISCLOSURE,
    PARAMETER_CALIBRATION_DISCLOSURE,
)
from tests.fixtures.lebanon_2019_2020_scenario import build_lebanon_scenario

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

from app.main import app

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

pytestmark = [pytest.mark.backtesting, pytest.mark.asyncio(loop_scope="session")]


def _require_db() -> None:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping Lebanon backtesting test")


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
    """Create, run, and fetch snapshots for the Lebanon scenario.

    Returns (scenario_id, snapshots_list).
    Raises AssertionError if any HTTP step fails.
    """
    scenario_req = build_lebanon_scenario()
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


async def test_lebanon_2019_2020_direction_only_fidelity(
    client: httpx.AsyncClient,
) -> None:
    """Lebanon 2019–2020 DIRECTION_ONLY fidelity gate — Issue #207.

    Thresholds checked:
      - gdp_growth at steps 1 and 2 must be negative (contraction predicted).
        ACTUALS show -6.9% (2019) and -21.4% (2020). The simulation must predict
        contraction, not growth. This is DIRECTION_ONLY — magnitude not evaluated.

    Mechanism:
      Step 1: initial gdp_growth seeded at -2.0% (already negative). The bank
        deposit freeze (capital controls) and fiscal spending cut (-10% of GDP)
        fire at step 1. Due to the one-step lag, MacroeconomicModule does not
        yet process these — step 1 shows the negative initial seed.
      Step 2: MacroeconomicModule processes the step 1 fiscal cut (-10% of GDP)
        under the depressed regime (multiplier 1.5), generating a large negative
        gdp_growth_change delta. Step 2 GDP is deeply negative.

    KNOWN LIMITATION: magnitude calibration not yet implemented. DISTRIBUTION_COMBINED
    thresholds require calibrated uncertainty bands; deferred per
    PARAMETER_CALIBRATION_DISCLOSURE. Lebanon's cascade dynamics are partially
    modeled — see CASCADE forward reference in module docstring.
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
                val = _extract_gdp_value(snap, entity_id="LBN")
                thresholds_met[key] = val is not None and val < Decimal("0")

        report = format_fidelity_report(
            scenario_name="Lebanon 2019-2020 Financial Collapse Backtesting Fixture",
            actuals=ACTUALS,
            snapshots=snapshots,
            thresholds_met=thresholds_met,
            ia1_disclosure=IA1_DISCLOSURE,
            parameter_calibration_disclosure=PARAMETER_CALIBRATION_DISCLOSURE,
            entity_id="LBN",
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


async def test_lebanon_scenario_creates_correct_number_of_snapshots(
    client: httpx.AsyncClient,
) -> None:
    """Lebanon scenario with n_steps=2 must produce 3 snapshots (steps 0–2)."""
    scenario_id, snapshots = await _create_and_run_scenario(client)
    try:
        assert len(snapshots) == 3, (
            f"Expected 3 snapshots (steps 0–2) for n_steps=2, got {len(snapshots)}"
        )
        step_nums = sorted(s["step"] for s in snapshots)
        assert step_nums == [0, 1, 2]
    finally:
        await client.delete(f"/api/v1/scenarios/{scenario_id}")


async def test_lebanon_snapshot_state_data_includes_gdp_growth(
    client: httpx.AsyncClient,
) -> None:
    """Every LBN snapshot must include gdp_growth in SA-09 envelope format."""
    scenario_id, snapshots = await _create_and_run_scenario(client)
    try:
        for snap in snapshots:
            step = snap["step"]
            lbn = snap["state_data"].get("LBN", {})
            assert "gdp_growth" in lbn, (
                f"gdp_growth missing from LBN at step {step}"
            )
            envelope = lbn["gdp_growth"]
            assert envelope.get("_envelope_version") == "1", (
                f"SA-09 _envelope_version missing at step {step}"
            )
            assert isinstance(envelope.get("value"), str), (
                f"gdp_growth.value is not a string at step {step} (float prohibition)"
            )
    finally:
        await client.delete(f"/api/v1/scenarios/{scenario_id}")


async def test_lebanon_run_sets_status_completed(
    client: httpx.AsyncClient,
) -> None:
    """After a successful run, scenario status must be 'completed'."""
    scenario_id, _ = await _create_and_run_scenario(client)
    try:
        detail = await client.get(f"/api/v1/scenarios/{scenario_id}")
        assert detail.json()["status"] == "completed"
    finally:
        await client.delete(f"/api/v1/scenarios/{scenario_id}")
