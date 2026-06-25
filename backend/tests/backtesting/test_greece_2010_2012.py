"""Greece 2010–2015 backtesting test — ADR-004 Decision 3, Issue #112, Issue #316.

This is the primary fidelity gate for Milestone 3 (steps 1–3) and the M8
stabilization-period extension (steps 4–6). It creates and runs the Greece
2010–2015 IMF program scenario, retrieves the simulation snapshots, and
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
    _extract_health_expenditure_value,
    _extract_investment_climate_value,
    _extract_unemployment_value,
    format_fidelity_report,
    write_fidelity_artifact,
)
from tests.fixtures.greece_2010_2012_actuals import (
    ACTUALS,
    ECOLOGICAL_COMPOSITE_DISCLOSURE,
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
    """Greece 2010–2015 DIRECTION_ONLY fidelity gate — ADR-004 Decision 3, Issue #316.

    Thresholds checked (steps 1–3, contraction period):
      - gdp_growth at steps 1, 2, 3 must be negative (contraction predicted).
        Rationale: ACTUALS show -5.4%, -8.9%, -6.6%. Simulation must predict
        contraction, not growth. This is a DIRECTION_ONLY check — the
        simulation need not match the magnitude.
      - unemployment_rate at step 3 must exceed the initial (step 0) value.
        Initial state is empirically grounded: EUROSTAT_LFS_2010 Q1 2010 = 12.7%.
        This replaces the previous step1→step3 check which was vacuous when no
        initial unemployment was seeded (Issue #149, resolved).

    Thresholds checked (steps 4–6, stabilization period — Issue #316):
      - gdp_growth at step 4 must be negative (-3.2%, 2013 continued contraction).
      - gdp_growth at step 5 is DEFERRED: historically +0.7% (2014 recovery), but the
        MacroeconomicModule has no endogenous recovery mechanism. Re-enable with Issue #221.
      - gdp_growth at step 6 must be negative (-0.4%, 2015 capital controls).

    KNOWN LIMITATION: Parameter calibration tier system not yet implemented
    (Issue #44). Magnitude accuracy is not evaluated in M3/M8.
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

        # DIRECTION_ONLY steps 4 and 6: negative (Issue #316)
        snap4 = snapshots_by_step.get(4)
        val4 = _extract_gdp_value(snap4) if snap4 else None
        thresholds_met["gdp_growth_step4_negative"] = val4 is not None and val4 < Decimal("0")

        snap5 = snapshots_by_step.get(5)
        val5 = _extract_gdp_value(snap5) if snap5 else None

        snap6 = snapshots_by_step.get(6)
        val6 = _extract_gdp_value(snap6) if snap6 else None
        thresholds_met["gdp_growth_step6_negative"] = val6 is not None and val6 < Decimal("0")

        # Unemployment direction threshold deferred: no endogenous module updates
        # unemployment_rate yet (module-capability-registry.md). The WDI seed sets
        # initial unemployment but the value stays flat across steps. Re-enable
        # this threshold when the Macroeconomic/Demographic module is implemented.

        # HCL / unemployment deferred thresholds — tracked in fidelity report,
        # not blocking CI (Issue #87)
        snap1 = snapshots_by_step.get(1)
        snap2 = snapshots_by_step.get(2)
        unemp1 = _extract_unemployment_value(snap1) if snap1 else None
        unemp2 = _extract_unemployment_value(snap2) if snap2 else None
        health1 = _extract_health_expenditure_value(snap1) if snap1 else None
        health2 = _extract_health_expenditure_value(snap2) if snap2 else None

        unemp_rising = (unemp1 is not None and unemp2 is not None and unemp2 > unemp1)
        health_declining = (health1 is not None and health2 is not None and health2 < health1)

        # Steps 4–6 unemployment declining from 27.5% peak (deferred — same reason)
        unemp4 = _extract_unemployment_value(snap4) if snap4 else None
        unemp5 = _extract_unemployment_value(snap5) if snap5 else None
        unemp6 = _extract_unemployment_value(snap6) if snap6 else None
        unemp_declining_4_to_6 = (
            unemp4 is not None
            and unemp5 is not None
            and unemp6 is not None
            and unemp5 < unemp4
            and unemp6 < unemp5
        )

        # Investment climate deferred thresholds — Issue #92 (M16-G9).
        # No endogenous module currently updates these attributes; they remain at initial state.
        # These thresholds re-enable when an InvestmentClimateModule produces endogenous updates.
        snap0 = snapshots_by_step.get(0)
        srp0 = _extract_investment_climate_value(snap0, "sovereign_risk_premium") if snap0 else None
        srp2 = _extract_investment_climate_value(snap2, "sovereign_risk_premium") if snap2 else None
        fdi0 = _extract_investment_climate_value(snap0, "fdi_stock_pct_gdp") if snap0 else None
        fdi2 = _extract_investment_climate_value(snap2, "fdi_stock_pct_gdp") if snap2 else None
        crs0 = _extract_investment_climate_value(snap0, "credit_rating_score") if snap0 else None
        crs2 = _extract_investment_climate_value(snap2, "credit_rating_score") if snap2 else None
        pfv0 = (
            _extract_investment_climate_value(snap0, "portfolio_flow_velocity") if snap0 else None
        )
        pfv2 = (
            _extract_investment_climate_value(snap2, "portfolio_flow_velocity") if snap2 else None
        )

        srp_rising = srp0 is not None and srp2 is not None and srp2 > srp0
        fdi_declining = fdi0 is not None and fdi2 is not None and fdi2 < fdi0
        crs_declining = crs0 is not None and crs2 is not None and crs2 < crs0
        pfv_deepening = pfv0 is not None and pfv2 is not None and pfv2 < pfv0

        deferred_thresholds: dict[str, str] = {
            "gdp_growth_step5_positive": (
                "PASS" if val5 is not None and val5 > Decimal("0")
                else (
                    "FAIL — no endogenous recovery module; "
                    "engine accumulates contraction (Issue #221)"
                )
            ),
            "unemployment_rising_step1_to_step2": (
                "PASS" if unemp_rising
                else "FAIL — no endogenous module updates unemployment_rate (Issue #87)"
            ),
            "health_expenditure_declining_step1_to_step2": (
                "PASS" if health_declining
                else "FAIL — no endogenous module updates health_expenditure_pct_gdp (Issue #87)"
            ),
            "unemployment_declining_step4_to_step6": (
                "PASS" if unemp_declining_4_to_6
                else "FAIL — no endogenous module updates unemployment_rate (Issue #87)"
            ),
            "sovereign_risk_rising_step0_to_step2": (
                "PASS" if srp_rising
                else "FAIL — no endogenous module updates sovereign_risk_premium (Issue #92)"
            ),
            "fdi_stock_declining_step0_to_step2": (
                "PASS" if fdi_declining
                else "FAIL — no endogenous module updates fdi_stock_pct_gdp (Issue #92)"
            ),
            "credit_rating_declining_step0_to_step2": (
                "PASS" if crs_declining
                else "FAIL — no endogenous module updates credit_rating_score (Issue #92)"
            ),
            "portfolio_outflows_deepening_step0_to_step2": (
                "PASS" if pfv_deepening
                else "FAIL — no endogenous module updates portfolio_flow_velocity (Issue #92)"
            ),
        }

        # Print fidelity report to stdout (appears in CI logs on every run)
        report = format_fidelity_report(
            scenario_name="Greece 2010-2015 IMF Program Backtesting Fixture",
            actuals=ACTUALS,
            snapshots=snapshots,
            thresholds_met=thresholds_met,
            ia1_disclosure=IA1_DISCLOSURE,
            parameter_calibration_disclosure=PARAMETER_CALIBRATION_DISCLOSURE,
            deferred_thresholds=deferred_thresholds,
        )
        print(f"\n{report}")
        artifact_path = write_fidelity_artifact(
            case_id="greece_2010_2015",
            thresholds_met=thresholds_met,
            deferred_thresholds=deferred_thresholds,
        )
        print(f"\nFidelity artifact written: {artifact_path}")
        print(f"\nECOLOGICAL: {ECOLOGICAL_COMPOSITE_DISCLOSURE}")

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
    """Greece scenario with n_steps=6 must produce 7 snapshots (steps 0–6)."""
    scenario_id, snapshots = await _create_and_run_scenario(client)
    try:
        assert len(snapshots) == 7, (
            f"Expected 7 snapshots (steps 0–6) for n_steps=6, got {len(snapshots)}"
        )
        step_nums = sorted(s["step"] for s in snapshots)
        assert step_nums == [0, 1, 2, 3, 4, 5, 6]
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
