"""QA tests for M19 G2 Phase C — Battle-Testing Scenario Runs.

Issues: #1547 (Greece), #1548 (Argentina), #1549 (Sri Lanka),
        #1550 (Pakistan), #1551 (Turkey), #1552 (Egypt), #1554 (Ghana)

Authored BEFORE implementation per intent document:
  docs/process/intents/M19-G2C-2026-07-03-battle-testing-scenario-runs.md

Sprint entry: docs/process/sprint-plans/m19-g2c-sprint-entry.md

ADDITIVE STRUCTURE (intent doc §7, additive approach):
  This file ships with Greece (#1547) and Argentina (#1548) test functions only.
  Test classes for new-country scenarios are added in each country's feature PR:
    Sri Lanka (#1549) — added in feat/m19-g2c-sri-lanka-coffin-corner
    Pakistan (#1550)  — added in feat/m19-g2c-pakistan-programme
    Turkey (#1551)    — added in feat/m19-g2c-turkey-backside
    Egypt (#1552)     — added in feat/m19-g2c-egypt-devaluation
    Ghana (#1554)     — added in feat/m19-g2c-ghana-imf-programme
  No skip stubs — fixture imports inside test methods fail RED (NM-056).

HARNESS IMPORTS are GREEN (app.harness.mode3_harness — G2A PR #1568).
FIXTURE IMPORTS are inside test methods — RED (ModuleNotFoundError) until each
country's fixture file is created.

NM-078 guard: file at backend/tests/backtesting/ — CI-discoverable path.

NM-056 rule: NO pytest.skip() / soft-skip in test bodies.
  Fixture imports are inside test methods and fail RED when unimplemented.
  All tests are DB-gated via the `asgi_client` session fixture which calls
  pytest.skip() in its setup when DATABASE_URL is absent. This is the only
  permitted skip path (fixture-level, not test-body-level). This matches
  the pattern established in test_m19_g2b_zmb_fixture.py.

CI ORDERING NOTE (intent doc §2.4 / NM-085 application):
  The backtesting mark is non-required for sprint/m19-g2 PRs.
  Transient missing-function failures on earlier PRs in this file are by
  design and do not block auto-merge on required checks.

ENTITY FIELD NOTE:
  ScenarioCreateRequest has no top-level entity_id field. The primary entity
  is accessed as req.configuration.entities[0]. All entity assertions use this
  path. The n_steps is at req.configuration.n_steps.

DIRECTION VERDICT ADVISORY NOTE (intent doc §7):
  _assert_direction_advisory() logs a warning if the model disagrees with
  an expected direction_verdict. These assertions do NOT fail CI.
  Hard assertions (DO fail CI if violated): fixture importability (RED),
  entity check, scenario creation (HTTP 201), harness run completion,
  direction_verdict field presence, per_step_diff list length,
  known_limitations non-empty, non-regression, scenario cleanup (AC-10).

AC coverage (Greece #1547 and Argentina #1548 — initial authorship):

  Common structural ACs (all folded into DB-gated test methods):
  AC-1   Fixture functions importable
  AC-2   entity == GRC / ARG  (req.configuration.entities[0])
  AC-3   POST /api/v1/scenarios → HTTP 201
  AC-4   TYPE_B run_harness() completes; direction_verdict in summary; per_step_diff
  AC-5   known_limitations is a non-empty list
  AC-6   Non-regression: Greece Type A → DIRECTION_ONLY unchanged
  AC-7   Non-regression: build_argentina_scenario() and build_argentina_demo_scenario()
         still construct after counterfactual function added to same file
  AC-8   Capital controls known_limitations present (Greece baseline Step 6) — advisory
  AC-9   Counter-factual Tier 3 disclosure in known_limitations — advisory
  AC-10  Cleanup: DELETE /api/v1/scenarios/{id} succeeds

  Greece-specific:
  AC-GRE-1  Counter-factual Step 1 scheduled_input differs from baseline
  AC-GRE-2  direction_verdict on hd_composite — advisory
  AC-GRE-3  n_steps == 6 and per_step_records == 6
  AC-GRE-4  MDA alerts non-empty at Step 6 — advisory
  AC-GRE-5  Coffin Corner / Backside failure mode at Step 2 or 3 — advisory

  Argentina-specific:
  AC-ARG-1  Counter-factual n_steps >= 3
  AC-ARG-2  direction_verdict on fin_composite — advisory
  AC-ARG-3  Per-step record count >= 3
  AC-ARG-4  Coffin Corner at crisis step — advisory
  AC-ARG-5  build_argentina_demo_scenario() unaffected — 4 steps, non-regression
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

# GREEN — harness exists (G2A PR #1568 merged to sprint/m19-g2, 2026-07-02)
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
# Advisory assertion helpers (intent doc §7 — warn, do NOT fail CI)
# ---------------------------------------------------------------------------


def _assert_direction_advisory(
    actual: object,
    expected: DirectionVerdict,
    country: str,
    indicator: str,
) -> None:
    """Log a warning when direction_verdict does not match expectation.

    G2C direction assertions are advisory — they surface model behaviour without
    failing CI. Persistent disagreement should be escalated to the Chief
    Methodologist.
    """
    if actual != expected and str(actual) != str(expected):
        warnings.warn(
            f"G2C advisory ({country}): {indicator} direction_verdict={actual!r}, "
            f"expected={expected!r}. Not a CI failure — review harness output. "
            "Escalate to Chief Methodologist if mismatch persists.",
            UserWarning,
            stacklevel=2,
        )


def _assert_failure_mode_advisory(
    active_modes: list[object],
    expected_modes: set[str],
    country: str,
    step: int,
) -> None:
    """Log a warning when no expected failure mode is active at a given step."""
    active_strs = {str(m) for m in active_modes}
    if not active_strs.intersection(expected_modes):
        warnings.warn(
            f"G2C advisory ({country}): none of {expected_modes} found in "
            f"active_failure_modes at step {step}. active={active_strs!r}. "
            "Not a CI failure — review harness output.",
            UserWarning,
            stacklevel=2,
        )


# ---------------------------------------------------------------------------
# Greece counter-factual tests (backtesting mark — DATABASE_URL required)
# All methods SKIP when DATABASE_URL absent (asgi_client fixture gate).
# All fixture imports are inside method bodies — RED until implemented.
# ---------------------------------------------------------------------------


@pytest.mark.backtesting
@pytest.mark.asyncio(loop_scope="session")
class TestGreeceCounterfactualTypeB:
    """AC-1 through AC-10, AC-GRE-1 through AC-GRE-5, AC-6 non-regression.

    Requires DATABASE_URL. All tests skip gracefully in CI without a database.
    """

    @pytest_asyncio.fixture(loop_scope="session")
    async def asgi_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        if not _DATABASE_URL:
            pytest.skip(
                "DATABASE_URL not set — skipping Greece counter-factual Type B tests"
            )
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client

    async def test_counterfactual_construction(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """AC-1, AC-2, AC-GRE-1, AC-GRE-3: fixture construction checks (no API calls).

        Imports build_greece_counterfactual_scenario() — RED (ModuleNotFoundError)
        until backend/tests/fixtures/greece_2010_scenario.py exports this function.
        """
        from tests.fixtures.greece_2010_scenario import (  # RED until implemented
            build_greece_counterfactual_scenario,
            build_greece_scenario,
        )

        # AC-1: importable (reached here means it is)

        cf = build_greece_counterfactual_scenario()
        baseline = build_greece_scenario()

        # AC-2: primary entity is GRC
        assert cf.configuration.entities[0] == "GRC", (
            f"AC-2 FAIL: counter-factual primary entity="
            f"{cf.configuration.entities[0]!r}, expected 'GRC'"
        )

        # AC-GRE-3: 6-step window (2010–2015)
        assert cf.configuration.n_steps == 6, (
            f"AC-GRE-3 FAIL: n_steps={cf.configuration.n_steps}, expected 6"
        )

        # AC-GRE-1: Step 1 scheduled_input differs from baseline (smaller shock)
        cf_inputs = list(cf.scheduled_inputs or [])
        b_inputs = list(baseline.scheduled_inputs or [])
        assert cf_inputs, "AC-GRE-1: counter-factual has no scheduled_inputs"
        assert b_inputs, "AC-GRE-1: baseline has no scheduled_inputs"
        assert cf_inputs[0] != b_inputs[0], (
            "AC-GRE-1 FAIL: counter-factual Step 1 input is identical to baseline. "
            "Must apply a gentler fiscal consolidation (<=2.5% GDP primary surplus "
            "vs troika ~4.5% GDP). Verify build_greece_counterfactual_scenario() "
            "modifies the Step 1 control input."
        )

    async def test_baseline_non_regression_construction(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """AC-6 partial: build_greece_scenario() still returns valid GRC request.

        Adding build_greece_counterfactual_scenario() to greece_2010_scenario.py
        must not alter the existing baseline fixture.
        """
        from tests.fixtures.greece_2010_scenario import build_greece_scenario

        req = build_greece_scenario()
        assert req.configuration.entities[0] == "GRC", (
            f"AC-6 non-regression FAIL: build_greece_scenario() primary entity "
            f"changed to {req.configuration.entities[0]!r}"
        )
        assert req.configuration.n_steps == 6, (
            f"AC-6 non-regression FAIL: build_greece_scenario() n_steps changed "
            f"to {req.configuration.n_steps}"
        )

    async def test_counterfactual_type_b_run(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """AC-3, AC-4, AC-5, AC-8, AC-9, AC-10, AC-GRE-2/4/5: full Type B harness run.

        Creates baseline (actual troika path) and counter-factual (gradual fiscal
        adjustment), runs the counter-factual as TYPE_B against the baseline.
        """
        from tests.fixtures.greece_2010_scenario import (  # RED until implemented
            build_greece_counterfactual_scenario,
            build_greece_scenario,
        )

        baseline_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_greece_scenario().model_dump(mode="json"),
        )
        assert baseline_resp.status_code == 201, (
            f"AC-3 FAIL (baseline): {baseline_resp.status_code} {baseline_resp.text}"
        )
        baseline_id: str = baseline_resp.json()["scenario_id"]

        cf_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_greece_counterfactual_scenario().model_dump(mode="json"),
        )
        assert cf_resp.status_code == 201, (
            f"AC-3 FAIL (counter-factual): {cf_resp.status_code} {cf_resp.text}"
        )
        cf_id: str = cf_resp.json()["scenario_id"]

        try:
            result = await run_harness(
                scenario_id=cf_id,
                steps=6,
                run_type=RunType.TYPE_B,
                control_inputs=[{} for _ in range(6)],
                baseline_run_id=baseline_id,
                primary_indicator="hd_composite",
                http_client=asgi_client,
            )

            # AC-GRE-3: step records
            assert len(result.per_step_records) == 6, (
                f"AC-GRE-3 FAIL: expected 6 step records, "
                f"got {len(result.per_step_records)}"
            )

            # AC-4 (SF-C1 guard): direction_verdict present and valid
            assert "direction_verdict" in result.summary, (
                "AC-4 SF-C1 FAIL: direction_verdict missing from Type B summary."
            )
            verdict = result.summary["direction_verdict"]
            valid_verdicts = {
                DirectionVerdict.COUNTER_FACTUAL_BETTER,
                DirectionVerdict.BASELINE_BETTER,
                DirectionVerdict.INDISTINGUISHABLE,
            }
            assert verdict in valid_verdicts or str(verdict) in {str(v) for v in valid_verdicts}, (
                f"AC-4 FAIL: direction_verdict={verdict!r} not in {valid_verdicts}"
            )

            # AC-4: per_step_diff present and length 6
            per_step_diff = result.summary.get("per_step_diff", [])
            assert isinstance(per_step_diff, list) and len(per_step_diff) == 6, (
                f"AC-4 FAIL: per_step_diff must be list of length 6, got {per_step_diff!r}"
            )

            # AC-5: known_limitations non-empty
            known = result.summary.get("known_limitations", [])
            assert isinstance(known, list) and len(known) >= 1, (
                "AC-5 FAIL: known_limitations must be a non-empty list."
            )

            # AC-8: capital controls disclosure — advisory
            cap_ctrl_found = any(
                "1532" in str(e) or "CAPITAL_CONTROLS" in str(e).upper()
                or "transmission absent" in str(e).lower()
                for e in known
            )
            if not cap_ctrl_found:
                warnings.warn(
                    "AC-8 advisory (GRC): CAPITAL_CONTROLS active at Step 6 of baseline "
                    "but no corresponding entry in known_limitations. "
                    "Verify #1532 gap is surfaced for Type B runs.",
                    UserWarning,
                    stacklevel=1,
                )

            # AC-9: Tier 3 / hypothetical disclosure — advisory
            tier3_found = any(
                term in str(e)
                for e in known
                for term in ("hypothetical", "Tier 3", "INFERRED_STRUCTURAL")
            ) or any(
                term in str(result.summary.get("fidelity_rationale", ""))
                for term in ("hypothetical", "Tier 3", "INFERRED_STRUCTURAL")
            )
            if not tier3_found:
                warnings.warn(
                    "AC-9 advisory (GRC): no Tier 3 / hypothetical disclosure found. "
                    "Counter-factual control inputs are INFERRED_STRUCTURAL — "
                    "intent doc §3.2 requires this to be disclosed.",
                    UserWarning,
                    stacklevel=1,
                )

            # AC-GRE-2: direction_verdict — advisory
            _assert_direction_advisory(
                actual=verdict,
                expected=DirectionVerdict.COUNTER_FACTUAL_BETTER,
                country="GRC",
                indicator="hd_composite",
            )

            # AC-GRE-4: MDA alerts at Step 6 (capital controls step) — advisory
            step6 = result.per_step_records[5]
            if not step6.get("mda_alert_states"):
                warnings.warn(
                    "AC-GRE-4 advisory (GRC): mda_alert_states empty at Step 6 "
                    "(2015 capital controls step).",
                    UserWarning,
                    stacklevel=1,
                )

            # AC-GRE-5: Coffin Corner / Backside at Steps 2 or 3 — advisory
            expected_modes = {"Coffin_Corner", "Backside_of_Power_Curve"}
            for idx in (1, 2):
                modes = result.per_step_records[idx].get("active_failure_modes", [])
                _assert_failure_mode_advisory(modes, expected_modes, "GRC", idx + 1)

        finally:
            # AC-10: cleanup
            await asgi_client.delete(f"/api/v1/scenarios/{baseline_id}")
            await asgi_client.delete(f"/api/v1/scenarios/{cf_id}")

    async def test_greece_type_a_non_regression(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """AC-6: Greece Type A still produces DIRECTION_ONLY after counter-factual added.

        If this test fails, the counter-factual addition has broken the existing
        fixture — do not merge.
        """
        from tests.fixtures.greece_2010_scenario import build_greece_scenario

        create_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_greece_scenario().model_dump(mode="json"),
        )
        assert create_resp.status_code == 201, (
            f"AC-6 non-regression: scenario creation failed: "
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
            actual_tier = result.summary.get("fidelity_tier")
            assert actual_tier == FidelityTier.DIRECTION_ONLY, (
                f"AC-6 NON-REGRESSION FAIL: Greece 2010–15 Type A fidelity_tier "
                f"changed from DIRECTION_ONLY to {actual_tier!r}. "
                "Do not merge — the counter-factual addition altered the baseline."
            )
        finally:
            await asgi_client.delete(f"/api/v1/scenarios/{scenario_id}")


# ---------------------------------------------------------------------------
# Argentina counter-factual tests (backtesting mark — DATABASE_URL required)
# ---------------------------------------------------------------------------


@pytest.mark.backtesting
@pytest.mark.asyncio(loop_scope="session")
class TestArgentinaCounterfactualTypeB:
    """AC-1 through AC-5, AC-7, AC-9, AC-10, AC-ARG-1 through AC-ARG-5.

    Requires DATABASE_URL. All tests skip gracefully in CI without a database.
    """

    @pytest_asyncio.fixture(loop_scope="session")
    async def asgi_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        if not _DATABASE_URL:
            pytest.skip(
                "DATABASE_URL not set — skipping Argentina counter-factual Type B tests"
            )
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client

    async def test_counterfactual_construction(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """AC-1, AC-2, AC-ARG-1, AC-ARG-5: fixture construction checks (no API calls).

        RED until build_argentina_counterfactual_scenario() is added to
        backend/tests/fixtures/argentina_2001_2002_scenario.py.
        """
        from tests.fixtures.argentina_2001_2002_scenario import (  # RED until implemented
            build_argentina_counterfactual_scenario,
            build_argentina_demo_scenario,
            build_argentina_scenario,
        )

        cf = build_argentina_counterfactual_scenario()

        # AC-2: primary entity is ARG
        assert cf.configuration.entities[0] == "ARG", (
            f"AC-2 FAIL: counter-factual primary entity="
            f"{cf.configuration.entities[0]!r}, expected 'ARG'"
        )

        # AC-ARG-1: extended window — n_steps >= 3
        assert cf.configuration.n_steps >= 3, (
            f"AC-ARG-1 FAIL: n_steps={cf.configuration.n_steps} < 3. "
            "The counter-factual must extend to at least 3 steps to represent "
            "the earlier peg-exit intervention (1999/2000 baseline)."
        )

        # AC-7 partial / AC-ARG-5: existing fixtures unaffected
        baseline = build_argentina_scenario()
        assert baseline.configuration.entities[0] == "ARG", (
            "AC-7 FAIL: build_argentina_scenario() primary entity changed"
        )

        demo = build_argentina_demo_scenario()
        assert demo.configuration.entities[0] == "ARG", (
            "AC-ARG-5 FAIL: build_argentina_demo_scenario() primary entity changed"
        )
        assert demo.configuration.n_steps == 4, (
            f"AC-ARG-5 FAIL: build_argentina_demo_scenario() n_steps changed "
            f"from 4 to {demo.configuration.n_steps}. "
            "Adding the counter-factual function must not modify the demo variant."
        )

    async def test_counterfactual_type_b_run(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """AC-3, AC-4, AC-5, AC-9, AC-10, AC-ARG-2/3/4: full Type B harness run."""
        from tests.fixtures.argentina_2001_2002_scenario import (  # RED until implemented
            build_argentina_counterfactual_scenario,
            build_argentina_scenario,
        )

        cf_req = build_argentina_counterfactual_scenario()
        cf_n_steps = cf_req.configuration.n_steps

        baseline_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_argentina_scenario().model_dump(mode="json"),
        )
        assert baseline_resp.status_code == 201, (
            f"AC-3 FAIL (baseline): {baseline_resp.status_code} {baseline_resp.text}"
        )
        baseline_id: str = baseline_resp.json()["scenario_id"]

        cf_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=cf_req.model_dump(mode="json"),
        )
        assert cf_resp.status_code == 201, (
            f"AC-3 FAIL (counter-factual): {cf_resp.status_code} {cf_resp.text}"
        )
        cf_id: str = cf_resp.json()["scenario_id"]

        try:
            result = await run_harness(
                scenario_id=cf_id,
                steps=cf_n_steps,
                run_type=RunType.TYPE_B,
                control_inputs=[{} for _ in range(cf_n_steps)],
                baseline_run_id=baseline_id,
                primary_indicator="fin_composite",
                http_client=asgi_client,
            )

            # AC-ARG-3: step records >= 3
            assert len(result.per_step_records) >= 3, (
                f"AC-ARG-3 FAIL: expected >= 3 step records, "
                f"got {len(result.per_step_records)}"
            )

            # AC-4: direction_verdict present and valid
            assert "direction_verdict" in result.summary, (
                "AC-4 SF-C1 FAIL: direction_verdict missing from Argentina Type B summary."
            )
            verdict = result.summary["direction_verdict"]
            valid_verdicts = {
                DirectionVerdict.COUNTER_FACTUAL_BETTER,
                DirectionVerdict.BASELINE_BETTER,
                DirectionVerdict.INDISTINGUISHABLE,
            }
            assert verdict in valid_verdicts or str(verdict) in {str(v) for v in valid_verdicts}, (
                f"AC-4 FAIL: direction_verdict={verdict!r} not in {valid_verdicts}"
            )

            # AC-4: per_step_diff length matches cf_n_steps
            per_step_diff = result.summary.get("per_step_diff", [])
            assert isinstance(per_step_diff, list) and len(per_step_diff) == cf_n_steps, (
                f"AC-4 FAIL: per_step_diff length {len(per_step_diff)} != {cf_n_steps}"
            )

            # AC-5: known_limitations non-empty
            known = result.summary.get("known_limitations", [])
            assert isinstance(known, list) and len(known) >= 1, (
                "AC-5 FAIL: known_limitations must be a non-empty list."
            )

            # AC-9: Tier 3 disclosure — advisory
            tier3_found = any(
                term in str(e)
                for e in known
                for term in ("hypothetical", "Tier 3", "INFERRED_STRUCTURAL")
            ) or any(
                term in str(result.summary.get("fidelity_rationale", ""))
                for term in ("hypothetical", "Tier 3", "INFERRED_STRUCTURAL")
            )
            if not tier3_found:
                warnings.warn(
                    "AC-9 advisory (ARG): no Tier 3 / hypothetical disclosure found. "
                    "Counter-factual peg-exit timing is INFERRED_STRUCTURAL.",
                    UserWarning,
                    stacklevel=1,
                )

            # AC-ARG-2: direction_verdict — advisory
            _assert_direction_advisory(
                actual=verdict,
                expected=DirectionVerdict.COUNTER_FACTUAL_BETTER,
                country="ARG",
                indicator="fin_composite",
            )

            # AC-ARG-4: Coffin Corner at any step — advisory
            coffin_found = any(
                any("Coffin_Corner" in str(m) for m in rec.get("active_failure_modes", []))
                for rec in result.per_step_records
            )
            if not coffin_found:
                warnings.warn(
                    "AC-ARG-4 advisory (ARG): Coffin_Corner not found across any step. "
                    "Argentina 2001 convertibility collapse is a canonical Coffin Corner case.",
                    UserWarning,
                    stacklevel=1,
                )

        finally:
            # AC-10: cleanup
            await asgi_client.delete(f"/api/v1/scenarios/{baseline_id}")
            await asgi_client.delete(f"/api/v1/scenarios/{cf_id}")


# ---------------------------------------------------------------------------
# New-country scenario tests — ADDITIVE, added in each country's feature PR
# ---------------------------------------------------------------------------


@pytest.mark.backtesting
@pytest.mark.asyncio(loop_scope="session")
class TestSriLankaTypeAB:
    """AC-1..5, AC-9, AC-10, AC-NC-2 (advisory), AC-NC-3, AC-LKA-1..4.

    Type A: does the engine predict DIRECTION_ONLY on reserve depletion and
    Q1 poverty headcount increase during the 2021–2022 crisis arc?
    Type B: counter-factual (no fertiliser ban, earlier IMF) — direction verdict.

    Requires DATABASE_URL. Skips gracefully when absent.
    """

    @pytest_asyncio.fixture(loop_scope="session")
    async def asgi_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        if not _DATABASE_URL:
            pytest.skip("DATABASE_URL not set — skipping Sri Lanka Type A+B tests")
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client

    async def test_construction(self, asgi_client: httpx.AsyncClient) -> None:
        """AC-1, AC-2, AC-LKA-1: fixture importable; entity=LKA; counter-factual differs."""
        from tests.fixtures.sri_lanka_2022_scenario import (  # RED until implemented
            build_sri_lanka_counterfactual_scenario,
            build_sri_lanka_scenario,
        )

        baseline = build_sri_lanka_scenario()
        cf = build_sri_lanka_counterfactual_scenario()

        # AC-2: entity
        assert baseline.configuration.entities[0] == "LKA"
        assert cf.configuration.entities[0] == "LKA"

        # AC-NC-3: n_steps == 5
        assert baseline.configuration.n_steps == 5, (
            f"AC-NC-3 FAIL: n_steps={baseline.configuration.n_steps}, expected 5"
        )
        assert cf.configuration.n_steps == 5

        # AC-LKA-1: counter-factual Step 2 has NO REGULATORY_CHANGE (fertiliser ban omitted)
        cf_step2_inputs = [
            s for s in (cf.scheduled_inputs or []) if s.step == 2
        ]
        regulatory_at_step2 = any(
            s.input_data.get("instrument") == "regulatory_change"
            for s in cf_step2_inputs
        )
        assert not regulatory_at_step2, (
            "AC-LKA-1 FAIL: counter-factual Step 2 still has REGULATORY_CHANGE. "
            "The fertiliser ban must be absent from the counter-factual."
        )

    async def test_type_a_run(self, asgi_client: httpx.AsyncClient) -> None:
        """AC-3, AC-4 (TYPE_A), AC-5, AC-10, AC-LKA-2: Type A historical run."""
        from tests.fixtures.sri_lanka_2022_scenario import (
            build_sri_lanka_scenario,
        )

        resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_sri_lanka_scenario().model_dump(mode="json"),
        )
        assert resp.status_code == 201, f"AC-3 FAIL: {resp.status_code} {resp.text}"
        scenario_id: str = resp.json()["scenario_id"]

        try:
            result = await run_harness(
                scenario_id=scenario_id,
                steps=5,
                run_type=RunType.TYPE_A,
                control_inputs=[{} for _ in range(5)],
                http_client=asgi_client,
            )
            # AC-LKA-2: fidelity tier is DIRECTION_ONLY (reserve floor is stock-flow #30)
            actual_tier = result.summary.get("fidelity_tier")
            assert actual_tier in _ACCEPTABLE_TIERS or str(actual_tier) in {
                str(t) for t in _ACCEPTABLE_TIERS
            }, (
                f"AC-LKA-2 FAIL: fidelity_tier={actual_tier!r} — "
                "Sri Lanka Type A requires at minimum DIRECTION_ONLY."
            )
            assert len(result.per_step_records) == 5
        finally:
            await asgi_client.delete(f"/api/v1/scenarios/{scenario_id}")

    async def test_type_b_run(self, asgi_client: httpx.AsyncClient) -> None:
        """AC-3, AC-4, AC-5, AC-9, AC-10, AC-LKA-3/4: Type B counter-factual run."""
        from tests.fixtures.sri_lanka_2022_scenario import (
            build_sri_lanka_counterfactual_scenario,
            build_sri_lanka_scenario,
        )

        baseline_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_sri_lanka_scenario().model_dump(mode="json"),
        )
        assert baseline_resp.status_code == 201, (
            f"AC-3 FAIL (baseline): {baseline_resp.status_code}"
        )
        baseline_id: str = baseline_resp.json()["scenario_id"]

        cf_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_sri_lanka_counterfactual_scenario().model_dump(mode="json"),
        )
        assert cf_resp.status_code == 201, (
            f"AC-3 FAIL (cf): {cf_resp.status_code}"
        )
        cf_id: str = cf_resp.json()["scenario_id"]

        try:
            result = await run_harness(
                scenario_id=cf_id,
                steps=5,
                run_type=RunType.TYPE_B,
                control_inputs=[{} for _ in range(5)],
                baseline_run_id=baseline_id,
                primary_indicator="fin_composite",
                http_client=asgi_client,
            )

            assert len(result.per_step_records) == 5
            assert "direction_verdict" in result.summary, "AC-4: direction_verdict missing"
            verdict = result.summary["direction_verdict"]
            valid_verdicts = {
                DirectionVerdict.COUNTER_FACTUAL_BETTER,
                DirectionVerdict.BASELINE_BETTER,
                DirectionVerdict.INDISTINGUISHABLE,
            }
            assert verdict in valid_verdicts or str(verdict) in {
                str(v) for v in valid_verdicts
            }

            per_step_diff = result.summary.get("per_step_diff", [])
            assert isinstance(per_step_diff, list) and len(per_step_diff) == 5

            # AC-5: known_limitations non-empty
            known = result.summary.get("known_limitations", [])
            assert isinstance(known, list) and len(known) >= 1, "AC-5 FAIL"

            # AC-9: Tier 3 disclosure — advisory
            tier3_found = any(
                term in str(e)
                for e in known
                for term in ("Tier 3", "INFERRED_STRUCTURAL", "hypothetical")
            )
            if not tier3_found:
                warnings.warn(
                    "AC-9 advisory (LKA): no Tier 3 disclosure in known_limitations.",
                    UserWarning, stacklevel=1,
                )

            # AC-LKA-3: direction advisory (expected COUNTER_FACTUAL_BETTER)
            _assert_direction_advisory(
                actual=verdict,
                expected=DirectionVerdict.COUNTER_FACTUAL_BETTER,
                country="LKA",
                indicator="fin_composite",
            )

            # AC-LKA-4: all-six failure modes advisory (at least one per crisis step)
            all_modes = {
                str(m)
                for rec in result.per_step_records
                for m in rec.get("active_failure_modes", [])
            }
            expected_modes = {
                "The_Spin", "Coffin_Corner", "Hypoxia",
                "Backside_of_Power_Curve", "Get_There_Itis", "CB_Cloud",
            }
            missing = expected_modes - all_modes
            if missing:
                warnings.warn(
                    f"AC-LKA-4 advisory (LKA): failure modes not detected: {missing}. "
                    "Sri Lanka 2022 is the canonical all-six-modes case.",
                    UserWarning, stacklevel=1,
                )
        finally:
            await asgi_client.delete(f"/api/v1/scenarios/{baseline_id}")
            await asgi_client.delete(f"/api/v1/scenarios/{cf_id}")


# Pakistan (#1550) — TestPakistanTypeB
# ----------------------------------------
# ACs: AC-1..5, AC-9, AC-10, AC-NC-2 (advisory), AC-NC-3, AC-PAK-1..3
# Run: Type B
# Primary indicator: fin_composite
# Advisory: direction_verdict COUNTER_FACTUAL_BETTER
# Add in: feat/m19-g2c-pakistan-programme (after CM advisory on #1550)


# Turkey (#1551) — TestTurkeyTypeB
# ----------------------------------------
# ACs: AC-1..5, AC-9, AC-10, AC-NC-2 (advisory), AC-NC-3, AC-TUR-1..3
# Run: Type B
# Primary indicator: fin_composite
# Advisory: direction_verdict COUNTER_FACTUAL_BETTER
# Add in: feat/m19-g2c-turkey-backside (after CM advisory on #1551)


# Egypt (#1552) — TestEgyptTypeB
# ----------------------------------------
# ACs: AC-1..5, AC-9, AC-10, AC-NC-2 (advisory), AC-NC-3, AC-EGY-1..3
# Run: Type B
# DIRECTION INVERSION NOTE: Egypt 2016 is not a WorldSim failure-mode case.
#   direction_verdict may be BASELINE_BETTER — the advisory assertion must NOT
#   hardcode COUNTER_FACTUAL_BETTER. Log whichever verdict the model produces.
# Add in: feat/m19-g2c-egypt-devaluation (after CM advisory on #1552)


# Ghana (#1554) — TestGhanaTypeAB
# ----------------------------------------
# ACs: AC-1..5, AC-9, AC-10, AC-NC-2 (advisory), AC-NC-3, AC-GHA-1..4
# Run: Type A+B (baseline = 2020–2023 actual crisis; counter-factual = earlier IMF 2021)
# Primary indicator: fin_composite
# Advisory: direction_verdict COUNTER_FACTUAL_BETTER
# Add in: feat/m19-g2c-ghana-imf-programme (after CM advisory on #1554)
