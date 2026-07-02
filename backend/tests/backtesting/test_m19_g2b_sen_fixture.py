"""QA tests for M19 G2 Phase B — SEN backtesting fixture (#1541).

Authored BEFORE implementation per intent document:
  docs/process/intents/M19-G2B-2026-07-02-sen-backtesting-fixture.md

Sprint entry: docs/process/sprint-plans/m19-g2b-sprint-entry.md

These tests are RED until the fixture is implemented at:
  backend/tests/fixtures/sen_scenario.py

The harness imports below are GREEN (app.harness.mode3_harness exists, G2A PR #1568).
The fixture import below is RED until build_sen_scenario() is implemented.

NM-078 guard: this file is placed at backend/tests/backtesting/ — not at
backend/tests/ root — to ensure CI test discovery includes it.

NM-056 rule: NO pytest.skip() or soft-skip patterns in structural tests.
The top-level fixture import fails RED (ImportError/collection error) until
backend/tests/fixtures/sen_scenario.py is created with build_sen_scenario().

AC coverage:
  AC-1   fixture importable; build_sen_scenario() callable without error
  AC-2   fixture returns ScenarioRequest with entity_id="SEN", is_pre_calibration=True
  AC-3   POST /api/v1/scenarios returns HTTP 201
  AC-4   run_harness() TYPE_A completes; per_step_records length == 6
  AC-5   fidelity_tier in {DIRECTION_ONLY, MAGNITUDE_MATCH}
  AC-6   fin_composite step 3 < step 1 (commodity shock direction correct)
  AC-7   len(per_step_records) == 6 (SF-1 guard)
  AC-8   known_limitations is a list
  AC-9   scenario cleanup — DELETE succeeds after run
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

# RED — fails ImportError until backend/tests/fixtures/sen_scenario.py is created.
# This is intentional per NM-056: hard RED, not soft skip.
from tests.fixtures.sen_scenario import build_sen_scenario

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

_ACCEPTABLE_TIERS = {FidelityTier.DIRECTION_ONLY, FidelityTier.MAGNITUDE_MATCH}

pytestmark = pytest.mark.asyncio(loop_scope="function")


# ---------------------------------------------------------------------------
# SEN Type A calibration fixture tests
# ---------------------------------------------------------------------------


@pytest.mark.backtesting
@pytest.mark.asyncio(loop_scope="session")
class TestSENTypeARegressionFidelity:
    """AC-1 through AC-9: SEN 2014–2019 Type A harness run validation.

    Requires DATABASE_URL — tests skip gracefully in environments without a DB.
    All assertions are direction-only or structural (no magnitude matching).
    Chief Methodologist review required before this fixture merges to sprint/m19-g2.
    """

    @pytest_asyncio.fixture(loop_scope="session")
    async def asgi_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        if not _DATABASE_URL:
            pytest.skip("DATABASE_URL not set — skipping SEN Type A harness calibration")
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client

    async def test_sen_fixture_importable_and_returns_valid_request(self) -> None:
        """AC-1 + AC-2: fixture callable; entity_id == "SEN"."""
        scenario_req = build_sen_scenario()
        assert scenario_req.entity_id == "SEN", (
            "AC-2 FAIL: build_sen_scenario() must return entity_id='SEN'"
        )
        assert getattr(scenario_req, "is_pre_calibration", None) is True, (
            "AC-2 FAIL: SEN calibration fixture must set is_pre_calibration=True"
        )

    async def test_sen_type_a_produces_acceptable_fidelity(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """AC-3 through AC-9: full harness run; fidelity + direction assertions.

        Covers: scenario creation (AC-3), harness run completion (AC-4), fidelity tier
        floor (AC-5), fin_composite direction (AC-6), step count (AC-7),
        known_limitations type (AC-8), cleanup (AC-9).

        Chief Methodologist must review fidelity_tier output before this fixture
        is accepted as CI calibration evidence. Tier below DIRECTION_ONLY is a hard
        failure — do not merge without CM escalation (see intent doc §5).
        """
        scenario_req = build_sen_scenario()
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

            # AC-7 (SF-1 guard)
            assert len(result.per_step_records) == 6, (
                f"AC-7 SF-1 FAIL: expected 6 step records, got "
                f"{len(result.per_step_records)}"
            )

            # AC-5 — fidelity tier floor
            actual_tier = result.summary.get("fidelity_tier")
            assert actual_tier in _ACCEPTABLE_TIERS, (
                f"AC-5 FAIL: SEN 2014–2019 Type A fidelity tier {actual_tier!r} "
                f"is below the acceptable floor {_ACCEPTABLE_TIERS}. "
                "Chief Methodologist review required — do not merge this fixture."
            )

            # AC-6 — fiscal direction: step 3 (2016 trough) < step 1 (2014 baseline)
            fin_step1 = result.per_step_records[0].get("fin_composite")
            fin_step3 = result.per_step_records[2].get("fin_composite")
            if fin_step1 is not None and fin_step3 is not None:
                assert fin_step3 < fin_step1, (
                    f"AC-6 FAIL: fin_composite at step 3 ({fin_step3}) is not less "
                    f"than at step 1 ({fin_step1}). "
                    "The commodity price shock (2015–16) should produce fiscal deterioration."
                )

            # AC-8 — known_limitations is a list
            known = result.summary.get("known_limitations")
            assert isinstance(known, list), (
                f"AC-8 FAIL: known_limitations must be a list, got {type(known)!r}"
            )

        finally:
            # AC-9 — cleanup
            await asgi_client.delete(f"/api/v1/scenarios/{scenario_id}")
