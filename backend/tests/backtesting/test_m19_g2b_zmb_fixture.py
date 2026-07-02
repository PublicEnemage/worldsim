"""QA tests for M19 G2 Phase B — ZMB backtesting fixture (#1542).

Authored BEFORE implementation per intent document:
  docs/process/intents/M19-G2B-2026-07-02-zmb-backtesting-fixture.md

Sprint entry: docs/process/sprint-plans/m19-g2b-sprint-entry.md

These tests are RED until the fixture is implemented at:
  backend/tests/fixtures/zmb_scenario.py

The harness imports below are GREEN (app.harness.mode3_harness exists, G2A PR #1568).
The fixture import below is RED until build_zmb_scenario() is implemented.

NM-078 guard: this file is placed at backend/tests/backtesting/ — not at
backend/tests/ root — to ensure CI test discovery includes it.

NM-056 rule: NO pytest.skip() or soft-skip patterns in structural tests.
The top-level fixture import fails RED (ImportError/collection error) until
backend/tests/fixtures/zmb_scenario.py is created with build_zmb_scenario().

DEMO 8 LOAD-BEARING: ZMB is the primary calibration country for Demo 8 Act 2.
The fidelity tier produced by this fixture grounds the CI interval credibility
claim ("empirically grounded" CI bounds) at the stakeholder session. A fidelity
tier below DIRECTION_ONLY means the fixture cannot serve as calibration evidence
and must not merge — see intent doc §5 for escalation path.

AC coverage:
  AC-1   fixture importable; build_zmb_scenario() callable without error
  AC-2   fixture returns ScenarioRequest with entity_id="ZMB", is_pre_calibration=True,
         monitored_focal_cohorts non-empty (Copperbelt cohort required)
  AC-3   POST /api/v1/scenarios returns HTTP 201
  AC-4   run_harness() TYPE_A completes; per_step_records length == 6
  AC-5   fidelity_tier in {DIRECTION_ONLY, MAGNITUDE_MATCH}
  AC-6   fin_composite step 3 < step 1 (copper crash fiscal direction correct)
  AC-7   at least one per_step_record has non-null cohort_poverty_headcount (SF-3 guard)
  AC-8   len(per_step_records) == 6 (SF-1 guard)
  AC-9   known_limitations is a list
  AC-10  scenario cleanup — DELETE succeeds after run
"""
from __future__ import annotations

import os
from typing import TYPE_CHECKING

import httpx
import pytest
import pytest_asyncio

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

# GREEN — harness exists (G2A PR #1568 merged to sprint/m19-g2, 2026-07-02)
from app.harness.mode3_harness import FidelityTier, RunType, run_harness
from app.main import app

# RED — fails ImportError until backend/tests/fixtures/zmb_scenario.py is created.
# This is intentional per NM-056: hard RED, not soft skip.
from tests.fixtures.zmb_scenario import build_zmb_scenario

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

_ACCEPTABLE_TIERS = {FidelityTier.DIRECTION_ONLY, FidelityTier.MAGNITUDE_MATCH}

pytestmark = pytest.mark.asyncio(loop_scope="function")


# ---------------------------------------------------------------------------
# ZMB Type A calibration fixture tests
# ---------------------------------------------------------------------------


@pytest.mark.backtesting
@pytest.mark.asyncio(loop_scope="session")
class TestZMBTypeARegressionFidelity:
    """AC-1 through AC-10: ZMB 2014–2019 Type A harness run validation.

    Requires DATABASE_URL — tests skip gracefully in environments without a DB.
    ZMB is the Demo 8 primary calibration country. AC-7 (cohort headcount non-null)
    is load-bearing for Demo 8 Act 2 CI credibility — it must pass for the fixture
    to be accepted as calibration evidence (see intent doc §3.2 SF-3).
    Chief Methodologist review required before this fixture merges to sprint/m19-g2.
    """

    @pytest_asyncio.fixture(loop_scope="session")
    async def asgi_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        if not _DATABASE_URL:
            pytest.skip("DATABASE_URL not set — skipping ZMB Type A harness calibration")
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client

    async def test_zmb_fixture_importable_and_returns_valid_request(self) -> None:
        """AC-1 + AC-2: fixture callable; entity_id="ZMB"; Copperbelt cohort configured."""
        scenario_req = build_zmb_scenario()
        assert scenario_req.entity_id == "ZMB", (
            "AC-2 FAIL: build_zmb_scenario() must return entity_id='ZMB'"
        )
        assert getattr(scenario_req, "is_pre_calibration", None) is True, (
            "AC-2 FAIL: ZMB calibration fixture must set is_pre_calibration=True"
        )
        focal_cohorts = getattr(scenario_req, "monitored_focal_cohorts", None)
        assert focal_cohorts, (
            "AC-2 FAIL: ZMB fixture must configure monitored_focal_cohorts "
            "(Copperbelt/Lusaka bottom-quintile cohort required for Demo 8 Act 2 "
            'cohort poverty headcount tracking — the "+342K cohort effect" anchor).'
        )

    async def test_zmb_type_a_produces_acceptable_fidelity(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """AC-3 through AC-10: full harness run; fidelity + direction + cohort assertions.

        Covers: scenario creation (AC-3), harness run completion (AC-4), fidelity tier
        floor (AC-5), fin_composite direction (AC-6), cohort headcount non-null (AC-7,
        SF-3 guard), step count (AC-8), known_limitations type (AC-9), cleanup (AC-10).

        Chief Methodologist must review fidelity_tier output before this fixture is
        accepted as Demo 8 CI calibration evidence. MAGNITUDE_MATCH here strengthens
        the CI interval credibility claim significantly vs DIRECTION_ONLY.
        Tier below DIRECTION_ONLY is a hard failure — escalate to EL (see intent doc §5).
        """
        scenario_req = build_zmb_scenario()
        create_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=scenario_req.model_dump(mode="json"),
        )
        assert create_resp.status_code == 201, (
            f"AC-3 FAIL: Scenario creation failed: "
            f"{create_resp.status_code} {create_resp.text}"
        )
        scenario_id: str = create_resp.json()["scenario_id"]

        try:
            result = await run_harness(
                scenario_id=scenario_id,
                steps=6,
                run_type=RunType.TYPE_A,
                control_inputs=[{} for _ in range(6)],
                http_client=asgi_client,
            )

            # AC-8 (SF-1 guard)
            assert len(result.per_step_records) == 6, (
                f"AC-8 SF-1 FAIL: expected 6 step records, got "
                f"{len(result.per_step_records)}"
            )

            # AC-5 — fidelity tier floor (Demo 8 load-bearing)
            actual_tier = result.summary.get("fidelity_tier")
            assert actual_tier in _ACCEPTABLE_TIERS, (
                f"AC-5 FAIL: ZMB 2014–2019 Type A fidelity tier {actual_tier!r} "
                f"is below the acceptable floor {_ACCEPTABLE_TIERS}. "
                "DEMO 8 LOAD-BEARING: this fixture cannot serve as CI calibration "
                "evidence. Chief Methodologist escalation required — do not merge."
            )

            # AC-6 — fiscal direction: step 3 (2016 copper trough) < step 1 (2014 baseline)
            fin_step1 = result.per_step_records[0].get("fin_composite")
            fin_step3 = result.per_step_records[2].get("fin_composite")
            if fin_step1 is not None and fin_step3 is not None:
                assert fin_step3 < fin_step1, (
                    f"AC-6 FAIL: fin_composite at step 3 ({fin_step3}) is not less "
                    f"than at step 1 ({fin_step1}). "
                    "The copper price crash (2015–16) should produce fiscal deterioration "
                    "by step 3 (2016). Check the ZMB initial state and copper shock transmission."
                )

            # AC-7 — cohort headcount non-null (SF-3 guard — Demo 8 load-bearing)
            cohort_records = [
                r.get("cohort_poverty_headcount")
                for r in result.per_step_records
                if r.get("cohort_poverty_headcount") is not None
            ]
            assert cohort_records, (
                "AC-7 SF-3 FAIL: all per_step_records have null cohort_poverty_headcount. "
                "DEMO 8 LOAD-BEARING: the Copperbelt/Lusaka bottom-quintile cohort must "
                'produce headcount output — this is the "+342K cohort effect" anchor for '
                "Demo 8 Act 2. Check that monitored_focal_cohorts is configured correctly "
                "in build_zmb_scenario()."
            )

            # AC-9 — known_limitations is a list
            known = result.summary.get("known_limitations")
            assert isinstance(known, list), (
                f"AC-9 FAIL: known_limitations must be a list, got {type(known)!r}"
            )

        finally:
            # AC-10 — cleanup
            await asgi_client.delete(f"/api/v1/scenarios/{scenario_id}")
