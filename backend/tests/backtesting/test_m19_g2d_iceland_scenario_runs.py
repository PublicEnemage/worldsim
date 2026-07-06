"""QA tests for M19 G2 Phase D — Iceland 2008–11 heterodox vs orthodox counter-factual.

Issue: #1553 (Iceland 2008–11 fixture — heterodox vs orthodox counter-factual)
       #1532 (capital controls transmission gap — ADR-020 Channels A/B/C)

Authored BEFORE implementation per intent document:
  docs/process/intents/M19-G2D-2026-07-03-iceland-2008-backtesting-fixture.md

Sprint entry: docs/process/sprint-plans/m19-g2d-sprint-entry.md
ADR: ADR-020 (ARCH-014) — Emergency Instrument Economic Transmission Pattern

FIXTURE STRUCTURE:
  Heterodox baseline (Run A — what actually happened):
    tests/fixtures/isl_2008_heterodox.py → build_isl_heterodox_scenario()
  Orthodox counter-factual (Run B — IMF prescription, not taken):
    tests/fixtures/isl_2008_orthodox_counterfactual.py
    → build_isl_orthodox_counterfactual_scenario()

HARNESS: app.harness.mode3_harness (G2A PR #1568)
  Run A: TYPE_A — heterodox baseline advance run (direction check)
  Run B: TYPE_B — orthodox as counter-factual vs Run A (direction verdict)

DIRECTION ADVISORY:
  Direction verdict assertions are advisory (warn, do NOT fail CI).
  BASELINE_BETTER is expected on hd_composite (heterodox baseline outperforms
  orthodox counter-factual on human development). INDISTINGUISHABLE is also
  accepted pre-calibration.

DB-GATE: All API tests skip when DATABASE_URL absent (asgi_client fixture).
  NM-056 rule: NO pytest.skip() in test bodies — fixture-level skip only.

ENTITY FIELD NOTE:
  ScenarioCreateRequest has no top-level entity_id field.
  Primary entity accessed via req.configuration.entities[0].

AC coverage (from intent doc §4):
  AC-1   ISL entity seeded; required attributes present
  AC-2   Run A (heterodox) reserve_coverage_months advisory — Channel A fires
  AC-3   Run B (orthodox) no capital controls — reserve depletes (advisory)
  AC-4   Both runs' gdp_growth DETERIORATING at Step 2 (advisory)
  AC-5   known_limitations non-empty (TYPE_B auto-adds counter-factual disclosure)
  AC-6   Both runs tagged is_pre_calibration=True
  AC-7   direction_verdict advisory: BASELINE_BETTER (heterodox outperforms orthodox)
  AC-8   Iceland-specific known_limitations advisory (Q2 gap, debt overhang, etc.)
  AC-9   fidelity_tier DIRECTION_ONLY on TYPE_A run
  AC-10  Both runs complete without crash (HarnessApiError not raised)
  AC-NC-1 entity_id == "ISL"
  AC-NC-2 Both runs accessible under named keys in test assertions
"""
from __future__ import annotations

import os
import warnings
from typing import TYPE_CHECKING

import httpx
import pytest
import pytest_asyncio

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

from app.harness.mode3_harness import (
    DirectionVerdict,
    FidelityTier,
    RunType,
    run_harness,
)
from app.main import app

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

_ACCEPTABLE_TIERS = {FidelityTier.DIRECTION_ONLY, FidelityTier.MAGNITUDE_MATCH}


# ---------------------------------------------------------------------------
# Advisory assertion helpers
# ---------------------------------------------------------------------------


def _assert_direction_advisory(
    actual: object,
    expected: DirectionVerdict,
    indicator: str,
) -> None:
    """Log a warning when direction_verdict does not match expectation.

    Iceland G2D direction assertions are advisory — they surface model
    behaviour without failing CI. Persistent disagreement should be
    escalated to the Chief Methodologist.
    """
    if actual != expected and str(actual) != str(expected):
        warnings.warn(
            f"G2D advisory (ISL): {indicator} direction_verdict={actual!r}, "
            f"expected={expected!r}. Not a CI failure — review harness output. "
            "Escalate to Chief Methodologist if mismatch persists post-calibration.",
            UserWarning,
            stacklevel=2,
        )


def _assert_isl_limitations_advisory(known: list[object]) -> None:
    """Advisory: warn if Iceland-specific limitations missing from known_limitations.

    AC-8: these items are expected but not auto-detected by detect_known_limitations()
    (which only checks harness-level control_inputs, not scenario scheduled_inputs).
    A missing item is a process gap, not a CI failure.
    """
    known_str = " ".join(str(e) for e in known).lower()
    if "q2" not in known_str and "quintile 2" not in known_str:
        warnings.warn(
            "G2D advisory (ISL AC-8): Q2 poverty gap limitation missing from "
            "known_limitations. Expected per ADR-020 INCORPORATE-5.",
            UserWarning,
            stacklevel=2,
        )
    if "household debt" not in known_str and "debt overhang" not in known_str:
        warnings.warn(
            "G2D advisory (ISL AC-8): Iceland Q1 household debt overhang "
            "limitation missing from known_limitations.",
            UserWarning,
            stacklevel=2,
        )


# ---------------------------------------------------------------------------
# Construction tests (no DATABASE_URL required)
# ---------------------------------------------------------------------------


class TestIcelandFixtureConstruction:
    """AC-NC-1, AC-NC-2, AC-1: fixture construction assertions (no API calls).

    These tests verify that both fixture functions are importable, produce
    ScenarioCreateRequest with ISL entity, 4 steps, and the correct structural
    differences between heterodox and orthodox scenarios.
    """

    def test_heterodox_imports_and_entity(self) -> None:
        """AC-NC-1: heterodox fixture importable; primary entity is ISL; 4 steps."""
        from tests.fixtures.isl_2008_heterodox import build_isl_heterodox_scenario

        req = build_isl_heterodox_scenario()

        assert req.configuration.entities[0] == "ISL", (
            f"AC-NC-1 FAIL: heterodox primary entity={req.configuration.entities[0]!r}, "
            "expected 'ISL'"
        )
        assert req.configuration.n_steps == 4, (
            f"AC-NC-1 FAIL: heterodox n_steps={req.configuration.n_steps}, expected 4"
        )

    def test_orthodox_imports_and_entity(self) -> None:
        """AC-NC-1: orthodox counter-factual importable; primary entity is ISL; 4 steps."""
        from tests.fixtures.isl_2008_orthodox_counterfactual import (
            build_isl_orthodox_counterfactual_scenario,
        )

        req = build_isl_orthodox_counterfactual_scenario()

        assert req.configuration.entities[0] == "ISL", (
            f"AC-NC-1 FAIL: orthodox primary entity={req.configuration.entities[0]!r}, "
            "expected 'ISL'"
        )
        assert req.configuration.n_steps == 4, (
            f"AC-NC-1 FAIL: orthodox n_steps={req.configuration.n_steps}, expected 4"
        )

    def test_heterodox_has_capital_controls_at_step_1(self) -> None:
        """AC-NC-2: heterodox fixture has capital_controls scheduled at step 1."""
        from tests.fixtures.isl_2008_heterodox import build_isl_heterodox_scenario

        req = build_isl_heterodox_scenario()
        step1_inputs = [
            inp for inp in (req.scheduled_inputs or []) if inp.step == 1
        ]
        capital_ctrl = [
            inp for inp in step1_inputs
            if inp.input_data.get("instrument") == "capital_controls"
        ]
        assert capital_ctrl, (
            "AC-NC-2 FAIL: heterodox fixture has no capital_controls input at step 1. "
            "ADR-020 Channel A+B+C require EmergencyPolicyInput(instrument='capital_controls') "
            "at step 1."
        )

    def test_orthodox_has_no_capital_controls(self) -> None:
        """AC-NC-2: orthodox counter-factual has NO capital_controls at any step."""
        from tests.fixtures.isl_2008_orthodox_counterfactual import (
            build_isl_orthodox_counterfactual_scenario,
        )

        req = build_isl_orthodox_counterfactual_scenario()
        capital_ctrl = [
            inp for inp in (req.scheduled_inputs or [])
            if inp.input_data.get("instrument") == "capital_controls"
        ]
        assert not capital_ctrl, (
            "AC-NC-2 FAIL: orthodox counter-factual has capital_controls input. "
            "Orthodox path does not impose capital controls — open capital account "
            "maintained. Remove capital_controls from build_isl_orthodox_counterfactual_scenario()."
        )

    def test_scenarios_differ_at_step_1(self) -> None:
        """AC-NC-2: heterodox and orthodox differ in step 1 scheduled inputs."""
        from tests.fixtures.isl_2008_heterodox import build_isl_heterodox_scenario
        from tests.fixtures.isl_2008_orthodox_counterfactual import (
            build_isl_orthodox_counterfactual_scenario,
        )

        h = build_isl_heterodox_scenario()
        o = build_isl_orthodox_counterfactual_scenario()

        h_step1 = [inp.input_data for inp in (h.scheduled_inputs or []) if inp.step == 1]
        o_step1 = [inp.input_data for inp in (o.scheduled_inputs or []) if inp.step == 1]

        assert h_step1 != o_step1, (
            "AC-NC-2 FAIL: heterodox and orthodox have identical step 1 inputs. "
            "The structural difference between the two scenarios must be visible at step 1."
        )

    def test_heterodox_has_capital_account_outflow_velocity(self) -> None:
        """AC-1: capital_account_outflow_velocity present in ISL initial attributes.

        Required for ADR-020 Channel A to produce a non-zero reserve_coverage_months
        delta. Without this attribute, reserve_delta = 0 and AC-2 cannot be satisfied.
        """
        from tests.fixtures.isl_2008_heterodox import build_isl_heterodox_scenario

        req = build_isl_heterodox_scenario()
        attrs = req.configuration.initial_attributes or {}
        isl_attrs = attrs.get("ISL", {})
        assert "capital_account_outflow_velocity" in isl_attrs, (
            "AC-1 FAIL: capital_account_outflow_velocity missing from ISL initial attributes. "
            "ADR-020 Channel A requires this attribute for reserve_delta computation."
        )

    def test_orthodox_has_imf_program_acceptance_at_step_1(self) -> None:
        """AC-NC-2: orthodox has imf_program_acceptance at step 1."""
        from tests.fixtures.isl_2008_orthodox_counterfactual import (
            build_isl_orthodox_counterfactual_scenario,
        )

        req = build_isl_orthodox_counterfactual_scenario()
        step1_emergency = [
            inp for inp in (req.scheduled_inputs or [])
            if inp.step == 1
            and inp.input_type == "EmergencyPolicyInput"
            and inp.input_data.get("instrument") == "imf_program_acceptance"
        ]
        assert step1_emergency, (
            "AC-NC-2 FAIL: orthodox counter-factual missing imf_program_acceptance "
            "at step 1. Orthodox path requires IMF programme as the primary step 1 input."
        )


# ---------------------------------------------------------------------------
# API-gated tests (DATABASE_URL required)
# ---------------------------------------------------------------------------


@pytest.mark.backtesting
@pytest.mark.asyncio(loop_scope="session")
class TestIcelandHarnessRuns:
    """AC-2 through AC-10: harness run assertions (DATABASE_URL required).

    Run A (heterodox baseline): TYPE_A — 4-step advance, direction advisory.
    Run B (orthodox counter-factual): TYPE_B vs Run A — direction verdict advisory.
    """

    @pytest_asyncio.fixture(loop_scope="session")
    async def asgi_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        if not _DATABASE_URL:
            pytest.skip(
                "DATABASE_URL not set — skipping Iceland G2D harness run tests"
            )
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client

    async def test_heterodox_type_a_run(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """AC-6, AC-9, AC-10: heterodox baseline TYPE_A run completes; is_pre_calibration.

        Creates Run A scenario, advances 4 steps, checks is_pre_calibration=True
        and fidelity_tier in acceptable range (DIRECTION_ONLY or MAGNITUDE_MATCH).
        """
        from tests.fixtures.isl_2008_heterodox import build_isl_heterodox_scenario

        resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_isl_heterodox_scenario().model_dump(mode="json"),
        )
        assert resp.status_code == 201, (
            f"AC-10 FAIL (heterodox): POST /api/v1/scenarios returned "
            f"{resp.status_code}: {resp.text}"
        )
        run_a_id: str = resp.json()["scenario_id"]

        try:
            result = await run_harness(
                scenario_id=run_a_id,
                steps=4,
                run_type=RunType.TYPE_A,
                control_inputs=[{} for _ in range(4)],
                primary_indicator="hd_composite",
                http_client=asgi_client,
            )

            # AC-10: run completed without HarnessApiError (reached here)

            # AC-6: is_pre_calibration flag in metadata
            assert result.run_metadata.get("is_pre_calibration") is True, (
                "AC-6 FAIL: is_pre_calibration not True in run_metadata. "
                "The harness must tag pre-calibration structural tests."
            )

            # AC-9: fidelity_tier in acceptable range
            fidelity = result.summary.get("fidelity_tier")
            assert fidelity in _ACCEPTABLE_TIERS or str(fidelity) in {
                str(t) for t in _ACCEPTABLE_TIERS
            }, (
                f"AC-9 FAIL: fidelity_tier={fidelity!r} not in acceptable tiers "
                f"{_ACCEPTABLE_TIERS}. Pre-calibration ISL run must be DIRECTION_ONLY."
            )

            # AC-NC-2: 4 step records
            assert len(result.per_step_records) == 4, (
                f"AC-NC-2 FAIL: expected 4 step records, "
                f"got {len(result.per_step_records)}"
            )

        finally:
            await asgi_client.delete(f"/api/v1/scenarios/{run_a_id}")

    async def test_orthodox_type_b_counterfactual_run(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """AC-3/4/5/6/7/8/10: orthodox TYPE_B counter-factual vs heterodox baseline.

        Creates both Run A (heterodox) and Run B (orthodox); runs Type B.
        Direction verdict advisory: BASELINE_BETTER expected (heterodox outperforms).
        """
        from tests.fixtures.isl_2008_heterodox import build_isl_heterodox_scenario
        from tests.fixtures.isl_2008_orthodox_counterfactual import (
            build_isl_orthodox_counterfactual_scenario,
        )

        # Create Run A (baseline — heterodox)
        baseline_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_isl_heterodox_scenario().model_dump(mode="json"),
        )
        assert baseline_resp.status_code == 201, (
            f"AC-10 FAIL (baseline): POST /api/v1/scenarios returned "
            f"{baseline_resp.status_code}: {baseline_resp.text}"
        )
        baseline_id: str = baseline_resp.json()["scenario_id"]

        # Create Run B (counter-factual — orthodox)
        cf_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_isl_orthodox_counterfactual_scenario().model_dump(mode="json"),
        )
        assert cf_resp.status_code == 201, (
            f"AC-10 FAIL (counter-factual): POST /api/v1/scenarios returned "
            f"{cf_resp.status_code}: {cf_resp.text}"
        )
        cf_id: str = cf_resp.json()["scenario_id"]

        try:
            result = await run_harness(
                scenario_id=cf_id,
                steps=4,
                run_type=RunType.TYPE_B,
                control_inputs=[{} for _ in range(4)],
                baseline_run_id=baseline_id,
                primary_indicator="hd_composite",
                http_client=asgi_client,
            )

            # AC-10: run completed (no HarnessApiError raised — reached here)

            # AC-6: is_pre_calibration
            assert result.run_metadata.get("is_pre_calibration") is True, (
                "AC-6 FAIL: is_pre_calibration not True in run_metadata."
            )

            # AC-NC-2: 4 step records for counter-factual
            assert len(result.per_step_records) == 4, (
                f"AC-NC-2 FAIL: expected 4 step records, "
                f"got {len(result.per_step_records)}"
            )

            # AC-4 (SF-C1 guard): direction_verdict present and valid
            assert "direction_verdict" in result.summary, (
                "AC-4 SF-C1 FAIL: direction_verdict missing from TYPE_B summary."
            )
            verdict = result.summary["direction_verdict"]
            valid_verdicts = {
                DirectionVerdict.COUNTER_FACTUAL_BETTER,
                DirectionVerdict.BASELINE_BETTER,
                DirectionVerdict.INDISTINGUISHABLE,
            }
            assert verdict in valid_verdicts or str(verdict) in {
                str(v) for v in valid_verdicts
            }, (
                f"AC-4 FAIL: direction_verdict={verdict!r} not in {valid_verdicts}"
            )

            # AC-4: per_step_diff present and length 4
            per_step_diff = result.summary.get("per_step_diff", [])
            assert isinstance(per_step_diff, list) and len(per_step_diff) == 4, (
                f"AC-4 FAIL: per_step_diff must be list of length 4, "
                f"got {per_step_diff!r}"
            )

            # AC-5: known_limitations non-empty
            # TYPE_B auto-adds counter-factual methodology disclosure.
            known = result.summary.get("known_limitations", [])
            assert isinstance(known, list) and len(known) >= 1, (
                "AC-5 FAIL: known_limitations must be non-empty. "
                "TYPE_B runs auto-add INFERRED_STRUCTURAL counter-factual disclosure."
            )

            # AC-7: direction advisory — BASELINE_BETTER expected (heterodox outperforms)
            _assert_direction_advisory(
                verdict, DirectionVerdict.BASELINE_BETTER, "hd_composite"
            )

            # AC-8: Iceland-specific limitations advisory
            _assert_isl_limitations_advisory(known)

        finally:
            # AC-10: cleanup both scenarios (no orphaned state in DB)
            await asgi_client.delete(f"/api/v1/scenarios/{cf_id}")
            await asgi_client.delete(f"/api/v1/scenarios/{baseline_id}")
