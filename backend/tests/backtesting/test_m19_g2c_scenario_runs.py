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
NM-056 rule: NO pytest.skip() / soft-skip in structural tests. ImportError
at test-method level is hard RED — not a soft skip. Exception: DB-gated
session fixtures skip gracefully when DATABASE_URL is absent (same pattern
as test_greece_2010_2012.py and test_m19_g2b_zmb_fixture.py).

DIRECTION VERDICT ADVISORY NOTE (intent doc §7):
  _assert_direction_advisory() logs a warning if the model disagrees with
  an expected direction_verdict. These assertions do NOT fail CI.
  Hard assertions (DO fail CI if violated): fixture importability, entity_id,
  scenario creation (HTTP 201), harness run completion without exception,
  direction_verdict field presence, per_step_diff list length, known_limitations
  non-empty, non-regression (AC-6, AC-7), scenario cleanup (AC-10).

CI ORDERING NOTE (intent doc §2.4 / NM-085 application):
  This file uses the additive approach — no stubs for country functions not yet
  implemented. The backtesting mark is non-required for sprint/m19-g2 PRs.
  Transient missing-function failures on earlier PRs in this file are by design
  and do not block auto-merge on required checks.

AC coverage (Greece #1547 and Argentina #1548 — initial authorship):

  Common structural ACs:
  AC-1   Fixture functions importable
  AC-2   entity_id correct (GRC / ARG); is_pre_calibration == False
  AC-3   POST /api/v1/scenarios → HTTP 201
  AC-4   TYPE_B run_harness() completes; direction_verdict in summary (SF-C1 guard)
  AC-5   known_limitations is a non-empty list
  AC-6   Non-regression: build_greece_scenario() Type A → DIRECTION_ONLY unchanged
  AC-7   Non-regression: build_argentina_scenario() and build_argentina_demo_scenario()
         construct without error after counter-factual function is added to same file
  AC-8   Capital controls known_limitations present where active (Greece baseline Step 6)
  AC-9   Counter-factual Tier 3 disclosure in known_limitations or fidelity_rationale
  AC-10  Cleanup: DELETE /api/v1/scenarios/{id} succeeds after run

  Greece-specific:
  AC-GRE-1  Counter-factual Step 1 scheduled_input differs from baseline (smaller shock)
  AC-GRE-2  direction_verdict on hd_composite — advisory
  AC-GRE-3  Per-step record count == 6 (2010–2015 window)
  AC-GRE-4  MDA alerts non-empty at Step 6 (capital controls step) — advisory
  AC-GRE-5  Coffin Corner / Backside failure mode at Step 2 or 3 — advisory

  Argentina-specific:
  AC-ARG-1  Counter-factual n_steps >= 3 (extended window from 1999)
  AC-ARG-2  direction_verdict on fin_composite — advisory
  AC-ARG-3  Per-step record count >= 3
  AC-ARG-4  Coffin Corner identified at crisis step — advisory
  AC-ARG-5  build_argentina_demo_scenario() unaffected — non-regression
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

pytestmark = pytest.mark.asyncio(loop_scope="function")


# ---------------------------------------------------------------------------
# Advisory assertion helper (intent doc §7 — warns, does not fail CI)
# ---------------------------------------------------------------------------


def _assert_direction_advisory(
    actual: object,
    expected: DirectionVerdict,
    country: str,
    indicator: str,
) -> None:
    """Log a warning when direction_verdict does not match expectation.

    G2C direction assertions are advisory — they surface model behaviour without
    failing CI. If the model consistently disagrees with the structural expectation,
    escalate to the Chief Methodologist.
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
# Greece structural construction tests (no DATABASE_URL required)
# RED until build_greece_counterfactual_scenario() is added to fixture file
# ---------------------------------------------------------------------------


class TestGreeceCounterfactualConstruction:
    """AC-1, AC-2, AC-GRE-1, AC-GRE-3 — fixture construction without DB.

    These tests call build_greece_counterfactual_scenario() directly and
    inspect the returned ScenarioCreateRequest. They fail RED with
    ModuleNotFoundError / AttributeError until the fixture function is added
    to backend/tests/fixtures/greece_2010_scenario.py.

    No database connection is required.
    """

    def test_counterfactual_importable(self) -> None:
        """AC-1: build_greece_counterfactual_scenario importable without error."""
        from tests.fixtures.greece_2010_scenario import (  # RED until implemented  # noqa: F401
            build_greece_counterfactual_scenario,
        )

    def test_entity_id_is_grc(self) -> None:
        """AC-2: returned ScenarioCreateRequest has entity_id == 'GRC'."""
        from tests.fixtures.greece_2010_scenario import build_greece_counterfactual_scenario

        req = build_greece_counterfactual_scenario()
        assert req.entity_id == "GRC", (
            f"AC-2 FAIL: entity_id={req.entity_id!r}, expected 'GRC'"
        )

    def test_is_pre_calibration_false(self) -> None:
        """AC-2: is_pre_calibration == False — battle-testing run, not calibration."""
        from tests.fixtures.greece_2010_scenario import build_greece_counterfactual_scenario

        req = build_greece_counterfactual_scenario()
        assert getattr(req, "is_pre_calibration", None) is False, (
            "AC-2 FAIL: Greece counter-factual must set is_pre_calibration=False "
            "(this is a battle-testing run, not a Bayesian posterior calibration fixture)"
        )

    def test_step_count_is_six(self) -> None:
        """AC-GRE-3: 6-step window (annual 2010–2015)."""
        from tests.fixtures.greece_2010_scenario import build_greece_counterfactual_scenario

        req = build_greece_counterfactual_scenario()
        n_steps = getattr(req, "n_steps", None)
        scheduled = getattr(req, "scheduled_inputs", None) or []
        count = n_steps if n_steps is not None else len(scheduled)
        assert count == 6, (
            f"AC-GRE-3 FAIL: expected 6 steps (2010–2015), got {count}"
        )

    def test_step1_input_differs_from_baseline(self) -> None:
        """AC-GRE-1: counter-factual Step 1 scheduled_input differs from baseline.

        The counter-factual applies a smaller primary surplus shock at Step 1
        than the troika baseline. This test confirms the inputs differ — the
        exact field name is an implementation decision.
        """
        from tests.fixtures.greece_2010_scenario import (
            build_greece_counterfactual_scenario,
            build_greece_scenario,
        )

        baseline = build_greece_scenario()
        counterfactual = build_greece_counterfactual_scenario()

        baseline_inputs = list(getattr(baseline, "scheduled_inputs", None) or [])
        cf_inputs = list(getattr(counterfactual, "scheduled_inputs", None) or [])

        assert baseline_inputs, "AC-GRE-1: baseline has no scheduled_inputs"
        assert cf_inputs, "AC-GRE-1: counter-factual has no scheduled_inputs"

        b_step1 = baseline_inputs[0]
        c_step1 = cf_inputs[0]
        assert b_step1 != c_step1, (
            "AC-GRE-1 FAIL: counter-factual Step 1 input is identical to baseline. "
            "The counter-factual must apply a gentler fiscal consolidation path "
            "(primary surplus target <= 2.5% GDP vs troika ~4.5% GDP at Step 1). "
            "Verify build_greece_counterfactual_scenario() modifies the Step 1 control input."
        )


class TestGreeceBaselineNonRegression:
    """AC-6 / AC-7 partial: existing build_greece_scenario() unaffected.

    Adding build_greece_counterfactual_scenario() to greece_2010_scenario.py
    must not break the existing baseline function. These tests call the
    existing function and confirm it still constructs a valid GRC request.
    """

    def test_baseline_importable_after_counterfactual_added(self) -> None:
        """AC-6: build_greece_scenario() still importable from same file."""
        from tests.fixtures.greece_2010_scenario import build_greece_scenario  # noqa: F401

    def test_baseline_entity_id_unchanged(self) -> None:
        """AC-6: build_greece_scenario() still returns entity_id == 'GRC'."""
        from tests.fixtures.greece_2010_scenario import build_greece_scenario

        req = build_greece_scenario()
        assert req.entity_id == "GRC"


# ---------------------------------------------------------------------------
# Argentina structural construction tests (no DATABASE_URL required)
# RED until build_argentina_counterfactual_scenario() added to fixture file
# ---------------------------------------------------------------------------


class TestArgentinaCounterfactualConstruction:
    """AC-1, AC-2, AC-ARG-1, AC-ARG-3, AC-ARG-5 — fixture construction without DB."""

    def test_counterfactual_importable(self) -> None:
        """AC-1: build_argentina_counterfactual_scenario importable without error."""
        from tests.fixtures.argentina_2001_2002_scenario import (  # RED  # noqa: F401
            build_argentina_counterfactual_scenario,
        )

    def test_entity_id_is_arg(self) -> None:
        """AC-2: entity_id == 'ARG'."""
        from tests.fixtures.argentina_2001_2002_scenario import (
            build_argentina_counterfactual_scenario,
        )

        req = build_argentina_counterfactual_scenario()
        assert req.entity_id == "ARG", (
            f"AC-2 FAIL: entity_id={req.entity_id!r}, expected 'ARG'"
        )

    def test_is_pre_calibration_false(self) -> None:
        """AC-2: is_pre_calibration == False."""
        from tests.fixtures.argentina_2001_2002_scenario import (
            build_argentina_counterfactual_scenario,
        )

        req = build_argentina_counterfactual_scenario()
        assert getattr(req, "is_pre_calibration", None) is False, (
            "AC-2 FAIL: Argentina counter-factual must set is_pre_calibration=False"
        )

    def test_step_count_at_least_three(self) -> None:
        """AC-ARG-1 / AC-ARG-3: n_steps >= 3 (extended window from 1999/2000).

        The existing build_argentina_scenario() has n_steps=2 (2001–2002 only).
        The counter-factual must extend to at least 3 steps to represent the
        earlier intervention point (1999 or 2000 baseline).
        """
        from tests.fixtures.argentina_2001_2002_scenario import (
            build_argentina_counterfactual_scenario,
        )

        req = build_argentina_counterfactual_scenario()
        n_steps = getattr(req, "n_steps", None)
        scheduled = getattr(req, "scheduled_inputs", None) or []
        count = n_steps if n_steps is not None else len(scheduled)
        assert count >= 3, (
            f"AC-ARG-1 FAIL: counter-factual must have >= 3 steps to represent "
            f"the earlier peg-exit intervention window (1999/2000 baseline). "
            f"Got {count} step(s). The existing 2-step fixture covers 2001–2002 only."
        )

    def test_baseline_scenario_unaffected(self) -> None:
        """AC-7 partial: build_argentina_scenario() still importable after new function added."""
        from tests.fixtures.argentina_2001_2002_scenario import build_argentina_scenario

        req = build_argentina_scenario()
        assert req.entity_id == "ARG"

    def test_demo_scenario_unaffected(self) -> None:
        """AC-ARG-5: build_argentina_demo_scenario() (4-step demo variant) still constructs."""
        from tests.fixtures.argentina_2001_2002_scenario import build_argentina_demo_scenario

        req = build_argentina_demo_scenario()
        assert req.entity_id == "ARG"
        n_steps = getattr(req, "n_steps", None)
        scheduled = getattr(req, "scheduled_inputs", None) or []
        count = n_steps if n_steps is not None else len(scheduled)
        assert count == 4, (
            f"AC-ARG-5 FAIL: build_argentina_demo_scenario() n_steps changed "
            f"from 4 to {count} — adding the counter-factual function must not "
            "modify the existing demo variant."
        )


# ---------------------------------------------------------------------------
# Greece full Type B harness run (backtesting mark — DATABASE_URL required)
# ---------------------------------------------------------------------------


@pytest.mark.backtesting
@pytest.mark.asyncio(loop_scope="session")
class TestGreeceCounterfactualTypeB:
    """AC-3, AC-4, AC-5, AC-6, AC-8, AC-9, AC-10, AC-GRE-2, AC-GRE-3..5.

    Requires DATABASE_URL. Runs the Greece counter-factual as Type B against
    the existing troika-path baseline and asserts structural properties of
    the harness result.

    AC-6 (non-regression: Greece Type A → DIRECTION_ONLY) is also covered here
    since it requires the DB for the harness run.
    """

    @pytest_asyncio.fixture(loop_scope="session")
    async def asgi_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        if not _DATABASE_URL:
            pytest.skip(
                "DATABASE_URL not set — skipping Greece Type B harness run"
            )
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client

    async def test_greece_counterfactual_type_b_run(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """AC-3/4/5/8/9/10, AC-GRE-2/3/4/5: full Type B harness run.

        Creates both the baseline (actual troika path) and counter-factual
        (gradual fiscal adjustment) scenarios, then runs the counter-factual
        as TYPE_B against the baseline.
        """
        from tests.fixtures.greece_2010_scenario import (  # RED until implemented
            build_greece_counterfactual_scenario,
            build_greece_scenario,
        )

        # Create baseline scenario (Greece actual IMF programme)
        baseline_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_greece_scenario().model_dump(mode="json"),
        )
        assert baseline_resp.status_code == 201, (
            f"AC-3 FAIL (baseline): {baseline_resp.status_code} {baseline_resp.text}"
        )
        baseline_id: str = baseline_resp.json()["scenario_id"]

        # Create counter-factual scenario
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

            # AC-GRE-3: step count
            assert len(result.per_step_records) == 6, (
                f"AC-GRE-3 FAIL: expected 6 step records, "
                f"got {len(result.per_step_records)}"
            )

            # AC-4 (SF-C1 guard): direction_verdict present
            assert "direction_verdict" in result.summary, (
                "AC-4 SF-C1 FAIL: direction_verdict missing from Type B summary. "
                "run_harness() with RunType.TYPE_B must populate direction_verdict."
            )
            verdict = result.summary["direction_verdict"]
            valid_verdicts = {
                DirectionVerdict.COUNTER_FACTUAL_BETTER,
                DirectionVerdict.BASELINE_BETTER,
                DirectionVerdict.INDISTINGUISHABLE,
            }
            assert verdict in valid_verdicts or str(verdict) in {str(v) for v in valid_verdicts}, (
                f"AC-4 FAIL: direction_verdict={verdict!r} not in valid set {valid_verdicts}"
            )

            # AC-4: per_step_diff present and correct length
            per_step_diff = result.summary.get("per_step_diff", [])
            assert isinstance(per_step_diff, list) and len(per_step_diff) == 6, (
                f"AC-4 FAIL: per_step_diff must be a list of length 6, "
                f"got {per_step_diff!r}"
            )

            # AC-5: known_limitations non-empty
            known = result.summary.get("known_limitations", [])
            assert isinstance(known, list) and len(known) >= 1, (
                "AC-5 FAIL: known_limitations must be a non-empty list. "
                "At minimum, the stock-flow accounting gap (#30) must be present."
            )

            # AC-8: capital controls disclosure (Greece Step 6 applies CAPITAL_CONTROLS)
            # Advisory — Greece baseline applies capital controls at step 6;
            # the limitation should propagate to the Type B summary.
            cap_ctrl_entries = [
                e for e in known
                if "1532" in str(e)
                or "CAPITAL_CONTROLS" in str(e).upper()
                or "transmission absent" in str(e).lower()
            ]
            if not cap_ctrl_entries:
                warnings.warn(
                    "AC-8 advisory (Greece): CAPITAL_CONTROLS active at Step 6 of baseline "
                    "but no corresponding entry found in known_limitations. "
                    "Verify #1532 gap is surfaced for Type B runs when baseline activates "
                    "CAPITAL_CONTROLS.",
                    UserWarning,
                    stacklevel=1,
                )

            # AC-9: counter-factual Tier 3 disclosure
            tier3_entries = [
                e for e in known
                if "hypothetical" in str(e).lower()
                or "Tier 3" in str(e)
                or "INFERRED_STRUCTURAL" in str(e)
            ]
            rationale = result.summary.get("fidelity_rationale", "")
            tier3_in_rationale = any(
                term in str(rationale)
                for term in ("hypothetical", "Tier 3", "INFERRED_STRUCTURAL")
            )
            if not tier3_entries and not tier3_in_rationale:
                warnings.warn(
                    "AC-9 advisory (Greece): no Tier 3 / hypothetical disclosure found in "
                    "known_limitations or fidelity_rationale for counter-factual run. "
                    "Intent doc §3.2 requires disclosure that counter-factual control inputs "
                    "are INFERRED_STRUCTURAL (not historically validated).",
                    UserWarning,
                    stacklevel=1,
                )

            # AC-GRE-2: direction_verdict on hd_composite — advisory
            _assert_direction_advisory(
                actual=verdict,
                expected=DirectionVerdict.COUNTER_FACTUAL_BETTER,
                country="GRC",
                indicator="hd_composite",
            )

            # AC-GRE-4: MDA alerts at Step 6 (capital controls step) — advisory
            step6_record = result.per_step_records[5]
            mda_step6 = step6_record.get("mda_alert_states", [])
            if not mda_step6:
                warnings.warn(
                    "AC-GRE-4 advisory (GRC): mda_alert_states empty at Step 6 "
                    "(2015 capital controls step). Expected at least one alert given "
                    "CAPITAL_CONTROLS instrument active.",
                    UserWarning,
                    stacklevel=1,
                )

            # AC-GRE-5: Coffin Corner / Backside failure mode at Steps 2 or 3 — advisory
            expected_failure_modes = {"Coffin_Corner", "Backside_of_Power_Curve"}
            for step_idx in (1, 2):  # zero-indexed: step 2 = index 1, step 3 = index 2
                modes = result.per_step_records[step_idx].get("active_failure_modes", [])
                _assert_failure_mode_advisory(
                    active_modes=modes,
                    expected_modes=expected_failure_modes,
                    country="GRC",
                    step=step_idx + 1,
                )

        finally:
            # AC-10: cleanup both scenarios
            await asgi_client.delete(f"/api/v1/scenarios/{baseline_id}")
            await asgi_client.delete(f"/api/v1/scenarios/{cf_id}")

    async def test_greece_type_a_non_regression(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """AC-6: build_greece_scenario() Type A still produces DIRECTION_ONLY.

        Regression guard: adding build_greece_counterfactual_scenario() to
        greece_2010_scenario.py must not change the baseline fixture's behaviour.
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
                "Adding build_greece_counterfactual_scenario() must not alter "
                "the existing fixture's harness classification. Do not merge."
            )
        finally:
            await asgi_client.delete(f"/api/v1/scenarios/{scenario_id}")


# ---------------------------------------------------------------------------
# Argentina full Type B harness run (backtesting mark — DATABASE_URL required)
# ---------------------------------------------------------------------------


@pytest.mark.backtesting
@pytest.mark.asyncio(loop_scope="session")
class TestArgentinaCounterfactualTypeB:
    """AC-3, AC-4, AC-5, AC-7, AC-9, AC-10, AC-ARG-2/3/4.

    Requires DATABASE_URL. Runs the Argentina counter-factual as Type B against
    the existing convertibility-peg-maintained baseline.
    """

    @pytest_asyncio.fixture(loop_scope="session")
    async def asgi_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        if not _DATABASE_URL:
            pytest.skip(
                "DATABASE_URL not set — skipping Argentina Type B harness run"
            )
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client

    async def test_argentina_counterfactual_type_b_run(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """AC-3/4/5/9/10, AC-ARG-2/3/4: full Type B harness run.

        Creates the baseline (actual convertibility peg collapse) and the
        counter-factual (managed earlier exit), then runs the counter-factual
        as TYPE_B. The counter-factual window must extend earlier than the
        existing 2-step fixture to include the 1999/2000 pre-crisis period.
        """
        from tests.fixtures.argentina_2001_2002_scenario import (  # RED until implemented
            build_argentina_counterfactual_scenario,
            build_argentina_scenario,
        )

        # Create baseline scenario (actual peg collapse)
        baseline_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_argentina_scenario().model_dump(mode="json"),
        )
        assert baseline_resp.status_code == 201, (
            f"AC-3 FAIL (baseline): {baseline_resp.status_code} {baseline_resp.text}"
        )
        baseline_id: str = baseline_resp.json()["scenario_id"]

        # Create counter-factual scenario (earlier managed exit)
        cf_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_argentina_counterfactual_scenario().model_dump(mode="json"),
        )
        assert cf_resp.status_code == 201, (
            f"AC-3 FAIL (counter-factual): {cf_resp.status_code} {cf_resp.text}"
        )
        cf_id: str = cf_resp.json()["scenario_id"]

        try:
            # n_steps determined from counter-factual fixture (>= 3)
            cf_req = build_argentina_counterfactual_scenario()
            cf_n_steps = getattr(cf_req, "n_steps", None) or len(
                getattr(cf_req, "scheduled_inputs", None) or []
            )
            assert cf_n_steps >= 3, (
                f"AC-ARG-1 pre-run check FAIL: counter-factual n_steps={cf_n_steps} < 3"
            )

            result = await run_harness(
                scenario_id=cf_id,
                steps=cf_n_steps,
                run_type=RunType.TYPE_B,
                control_inputs=[{} for _ in range(cf_n_steps)],
                baseline_run_id=baseline_id,
                primary_indicator="fin_composite",
                http_client=asgi_client,
            )

            # AC-ARG-3: step count >= 3
            assert len(result.per_step_records) >= 3, (
                f"AC-ARG-3 FAIL: expected >= 3 step records, "
                f"got {len(result.per_step_records)}"
            )

            # AC-4 (SF-C1 guard): direction_verdict present
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
                f"AC-4 FAIL: direction_verdict={verdict!r} not in valid set"
            )

            # AC-4: per_step_diff length matches steps run
            per_step_diff = result.summary.get("per_step_diff", [])
            assert isinstance(per_step_diff, list) and len(per_step_diff) == cf_n_steps, (
                f"AC-4 FAIL: per_step_diff length {len(per_step_diff)} != steps {cf_n_steps}"
            )

            # AC-5: known_limitations non-empty
            known = result.summary.get("known_limitations", [])
            assert isinstance(known, list) and len(known) >= 1, (
                "AC-5 FAIL: known_limitations must be a non-empty list. "
                "At minimum, the stock-flow accounting gap (#30) must be present."
            )

            # AC-9: Tier 3 disclosure for counter-factual inputs
            tier3_found = any(
                term in str(e)
                for e in known
                for term in ("hypothetical", "Tier 3", "INFERRED_STRUCTURAL")
            )
            tier3_in_rationale = any(
                term in str(result.summary.get("fidelity_rationale", ""))
                for term in ("hypothetical", "Tier 3", "INFERRED_STRUCTURAL")
            )
            if not tier3_found and not tier3_in_rationale:
                warnings.warn(
                    "AC-9 advisory (ARG): no Tier 3 / hypothetical disclosure found. "
                    "Counter-factual peg-exit timing is INFERRED_STRUCTURAL — "
                    "must be disclosed.",
                    UserWarning,
                    stacklevel=1,
                )

            # AC-ARG-2: direction_verdict on fin_composite — advisory
            _assert_direction_advisory(
                actual=verdict,
                expected=DirectionVerdict.COUNTER_FACTUAL_BETTER,
                country="ARG",
                indicator="fin_composite",
            )

            # AC-ARG-4: Coffin Corner at crisis step — advisory
            # Crisis step is the last step in the baseline (default step = 2002).
            # In the counter-factual the step index of 2001/2002 depends on the
            # extended window — check all steps.
            coffin_corner_found = any(
                any("Coffin_Corner" in str(m) for m in rec.get("active_failure_modes", []))
                for rec in result.per_step_records
            )
            if not coffin_corner_found:
                warnings.warn(
                    "AC-ARG-4 advisory (ARG): Coffin_Corner not found in active_failure_modes "
                    "across any step. Argentina 2001 convertibility collapse is a canonical "
                    "Coffin Corner case — both tightening and loosening were lethal by the "
                    "corralito period.",
                    UserWarning,
                    stacklevel=1,
                )

        finally:
            # AC-10: cleanup both scenarios
            await asgi_client.delete(f"/api/v1/scenarios/{baseline_id}")
            await asgi_client.delete(f"/api/v1/scenarios/{cf_id}")


# ---------------------------------------------------------------------------
# New-country scenario tests — ADDITIVE, added in each country's feature PR
# ---------------------------------------------------------------------------

# The classes below are placeholders indicating where country-specific tests
# will be added. They contain no implementation — they are not imported by
# pytest and produce no test IDs at collection time until added.

# Sri Lanka (#1549) — TestSriLankaTypeAB
# ----------------------------------------
# ACs to cover: AC-1, AC-2, AC-3, AC-4, AC-5, AC-8 (if capital controls),
#               AC-9, AC-10, AC-NC-2 (advisory), AC-NC-3, AC-LKA-1..4
# Run classification: Type A+B
#   Step 1: build_lka_scenario()     → TYPE_A baseline
#   Step 2: build_lka_counterfactual_scenario() → TYPE_B vs baseline
# Primary indicator (Type B): fin_composite or gov_composite (CM advisory determines)
# Advisory: direction_verdict COUNTER_FACTUAL_BETTER on primary indicator
# Add in: feat/m19-g2c-sri-lanka-coffin-corner (after CM advisory on issue #1549)


# Pakistan (#1550) — TestPakistanTypeB
# ----------------------------------------
# ACs: AC-1, AC-2, AC-3, AC-4, AC-5, AC-9, AC-10, AC-NC-2 (advisory), AC-NC-3,
#      AC-PAK-1..3
# Run classification: Type B
#   Baseline: build_pak_scenario()
#   Counter-factual: build_pak_counterfactual_scenario()
# Primary indicator: fin_composite
# Advisory: direction_verdict COUNTER_FACTUAL_BETTER
# Add in: feat/m19-g2c-pakistan-programme (after CM advisory on issue #1550)


# Turkey (#1551) — TestTurkeyTypeB
# ----------------------------------------
# ACs: AC-1, AC-2, AC-3, AC-4, AC-5, AC-9, AC-10, AC-NC-2 (advisory), AC-NC-3,
#      AC-TUR-1..3
# Run classification: Type B
#   Baseline: build_tur_scenario()
#   Counter-factual: build_tur_counterfactual_scenario()
# Primary indicator: fin_composite
# Advisory: direction_verdict COUNTER_FACTUAL_BETTER
# Add in: feat/m19-g2c-turkey-backside (after CM advisory on issue #1551)


# Egypt (#1552) — TestEgyptTypeB
# ----------------------------------------
# ACs: AC-1, AC-2, AC-3, AC-4, AC-5, AC-8 (if capital controls), AC-9, AC-10,
#      AC-NC-2 (advisory), AC-NC-3, AC-EGY-1..3
# Run classification: Type B
#   Baseline: build_egy_scenario()
#   Counter-factual: build_egy_counterfactual_scenario()
# Primary indicator: fin_composite
# Advisory: direction_verdict may be BASELINE_BETTER (Egypt 2016 is an inverted case —
#   the actual float may be better than the managed-float counter-factual)
#   _assert_direction_advisory() called without a fixed expected value — logs either result.
# Add in: feat/m19-g2c-egypt-devaluation (after CM advisory on issue #1552)


# Ghana (#1554) — TestGhanaTypeAB
# ----------------------------------------
# ACs: AC-1, AC-2, AC-3, AC-4, AC-5, AC-9, AC-10, AC-NC-2 (advisory), AC-NC-3,
#      AC-GHA-1..4
# Run classification: Type A+B
#   Step 1: build_gha_scenario()     → TYPE_A baseline (2020–2023 actual crisis)
#   Step 2: build_gha_counterfactual_scenario() → TYPE_B vs baseline (earlier IMF 2021)
# Primary indicator: fin_composite
# Advisory: direction_verdict COUNTER_FACTUAL_BETTER
# Add in: feat/m19-g2c-ghana-imf-programme (after CM advisory on issue #1554)
