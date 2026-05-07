"""Thailand 1997–2000 backtesting test — Issue #141.

This is the third backtesting case alongside Greece 2010–2012, Argentina
2001–2002, and Lebanon 2019–2020. It validates DIRECTION_ONLY fidelity
thresholds for the Thailand Asian financial crisis.

Fidelity gate: GDP contraction predicted at both simulation steps.
  Step 1 (1997): Currency peg abandonment (capital controls) and fiscal
    tightening fire at step 1. Initial gdp_growth is already negative
    (-1.0%), so step 1 is negative without requiring MacroeconomicModule
    to fire (one-step lag design).
  Step 2 (1998): MacroeconomicModule processes the step 1 fiscal spending
    cut (-6% of GDP) under the depressed regime (multiplier 1.5), generating
    a large negative gdp_growth_change delta. Step 2 GDP is deeply negative.

The GDP direction check is structurally correct regardless of magnitude
calibration: currency peg collapse + pro-cyclical fiscal austerity in a
deteriorating economy must produce negative GDP growth per the
MacroeconomicModule regime logic.

CASCADE dynamics and contagion forward reference:
  Thailand 1997–2000 exemplifies two reinforcing CASCADE propagation failure
  modes (CLAUDE.md §Failure Mode Architecture):

  1. Herding / speculative contagion: coordinated speculative attacks on the
     baht (and later on regional currencies) were self-fulfilling — each
     successful attack increased the probability of the next, creating a
     cascade of currency crises across the Asian Tigers (Thailand → Malaysia
     → Indonesia → South Korea). This herding dynamic is not modeled in M6.

  2. Balance-sheet cascade: baht depreciation made USD-denominated corporate
     debt unpayable, generating non-performing loans → banking system stress
     → credit contraction → demand collapse. This within-country cascade
     amplified the external shock. The M6 simulation captures the macro-fiscal
     channel (fiscal austerity → GDP contraction via MacroeconomicModule) but
     not the balance-sheet cascade.

  Once the CASCADE propagation mode is implemented (Issue #29), Thailand
  1997–2000 is a primary candidate for validating that:
    (a) speculative contagion dynamics amplify GDP contraction beyond the
        isolated-country estimate modeled here.
    (b) the balance-sheet cascade multiplier is captured when corporate sector
        attributes (debt_service_ratio, non_performing_loan_rate) are seeded.
  This test should be extended at that point to include cascade-specific
  thresholds comparing isolated-country vs. contagion-adjusted outcomes.

Test skips gracefully when DATABASE_URL is not set. The THA entity must
exist in simulation_entities — the natural_earth_loader seed must run
before this test in CI (Thailand ISO 3166-1 alpha-3 = "THA").

Thresholds registered in backtesting_thresholds as case_id='THAILAND_1997_2000'
(migration e1c9d7f5b3a2).
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
from tests.fixtures.thailand_1997_2000_actuals import (
    ACTUALS,
    IA1_DISCLOSURE,
    PARAMETER_CALIBRATION_DISCLOSURE,
)
from tests.fixtures.thailand_1997_2000_scenario import build_thailand_scenario

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

from app.main import app

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

pytestmark = [pytest.mark.backtesting, pytest.mark.asyncio(loop_scope="session")]


def _require_db() -> None:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping Thailand backtesting test")


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
    """Create, run, and fetch snapshots for the Thailand scenario.

    Returns (scenario_id, snapshots_list).
    Raises AssertionError if any HTTP step fails.
    """
    scenario_req = build_thailand_scenario()
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


async def test_thailand_1997_2000_direction_only_fidelity(
    client: httpx.AsyncClient,
) -> None:
    """Thailand 1997–2000 DIRECTION_ONLY fidelity gate — Issue #141.

    Thresholds checked:
      - gdp_growth at steps 1 and 2 must be negative (contraction predicted).
        ACTUALS show -1.4% (1997) and -10.5% (1998). The simulation must predict
        contraction, not growth. This is DIRECTION_ONLY — magnitude not evaluated.

    Mechanism:
      Step 1: initial gdp_growth seeded at -1.0% (already negative). Capital
        controls and fiscal tightening (-6% of GDP) fire at step 1. Due to the
        one-step lag, MacroeconomicModule does not yet process these — step 1
        shows the negative initial seed.
      Step 2: MacroeconomicModule processes the step 1 fiscal cut (-6% of GDP)
        under the depressed regime (multiplier 1.5), generating a large negative
        gdp_growth_change delta. Step 2 GDP is deeply negative.

    KNOWN LIMITATION: magnitude calibration not yet implemented. DISTRIBUTION_COMBINED
    thresholds require calibrated uncertainty bands; deferred per
    PARAMETER_CALIBRATION_DISCLOSURE. Thailand's cascade and contagion dynamics
    are partially modeled — see CASCADE forward reference in module docstring.
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
                val = _extract_gdp_value(snap, entity_id="THA")
                thresholds_met[key] = val is not None and val < Decimal("0")

        report = format_fidelity_report(
            scenario_name="Thailand 1997-2000 Asian Financial Crisis Backtesting Fixture",
            actuals=ACTUALS,
            snapshots=snapshots,
            thresholds_met=thresholds_met,
            ia1_disclosure=IA1_DISCLOSURE,
            parameter_calibration_disclosure=PARAMETER_CALIBRATION_DISCLOSURE,
            entity_id="THA",
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


async def test_thailand_scenario_creates_correct_number_of_snapshots(
    client: httpx.AsyncClient,
) -> None:
    """Thailand scenario with n_steps=2 must produce 3 snapshots (steps 0–2)."""
    scenario_id, snapshots = await _create_and_run_scenario(client)
    try:
        assert len(snapshots) == 3, (
            f"Expected 3 snapshots (steps 0–2) for n_steps=2, got {len(snapshots)}"
        )
        step_nums = sorted(s["step"] for s in snapshots)
        assert step_nums == [0, 1, 2]
    finally:
        await client.delete(f"/api/v1/scenarios/{scenario_id}")


async def test_thailand_snapshot_state_data_includes_gdp_growth(
    client: httpx.AsyncClient,
) -> None:
    """Every THA snapshot must include gdp_growth in SA-09 envelope format."""
    scenario_id, snapshots = await _create_and_run_scenario(client)
    try:
        for snap in snapshots:
            step = snap["step"]
            tha = snap["state_data"].get("THA", {})
            assert "gdp_growth" in tha, (
                f"gdp_growth missing from THA at step {step}"
            )
            envelope = tha["gdp_growth"]
            assert envelope.get("_envelope_version") == "1", (
                f"SA-09 _envelope_version missing at step {step}"
            )
            assert isinstance(envelope.get("value"), str), (
                f"gdp_growth.value is not a string at step {step} (float prohibition)"
            )
    finally:
        await client.delete(f"/api/v1/scenarios/{scenario_id}")


async def test_thailand_run_sets_status_completed(
    client: httpx.AsyncClient,
) -> None:
    """After a successful run, scenario status must be 'completed'."""
    scenario_id, _ = await _create_and_run_scenario(client)
    try:
        detail = await client.get(f"/api/v1/scenarios/{scenario_id}")
        assert detail.json()["status"] == "completed"
    finally:
        await client.delete(f"/api/v1/scenarios/{scenario_id}")
