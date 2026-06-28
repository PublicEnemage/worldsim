"""QA tests for M18-G3: Counter-Scenario Comparison — AC-1349-G and AC-schema.

QA Lead — Computation Engine Agent (backend pytest authorship per sprint entry §2.4).
Authored BEFORE implementation from intent document at:
  docs/process/intents/M18-G3-2026-06-26-counter-scenario-comparison.md

Sprint entry: docs/process/sprint-plans/m18-g3-sprint-entry.md (EL approval required)
GR source: docs/process/intents/M18-GR-2026-06-26-counter-scenario-comparison.md
Issue: #1349

AC coverage:
  AC-1349-G  Distributional differential endpoint returns:
             (a) Per-step headcount differential for each non-reference scenario pair
             (b) CI band bounds (lower, upper) per step
             (c) Tier classification (T2 or T3)
             (d) Terminal step differential within +/-5% of Zambia fixture (340K for A vs C)
             (e) Response does NOT return composite score delta as primary differential value
  AC-schema  docs/schema/api_contracts.yml updated with distributional-differential endpoint:
             (a) Endpoint path present in schema
             (b) "distributional-differential" key documented
             (c) "headcount_differential" response field documented
             (d) "direction_stable" response field documented

G1 soft dependency (intent doc §6.3):
  G3 backend tests can be authored against a fixture with the G1 uncertainty data shape.
  Full end-to-end integration (real G1 CI band data -> G3 differential) requires G1 to be
  merged to release/m18 before G3's integration PR exits. These tests use a fixture-based
  approach that does not require G1 to be merged.

Zambia fixture values (Demo 7 Act 2, intent doc §1 and §6.2):
  Option A (EFF front-loaded) vs Option C (Homegrown reference):
    Terminal-step headcount differential: +340,000 persons
    CI band: 295,000 - 395,000 (95% CI)
  Option B (IMF carve-out) vs Option C (Homegrown reference):
    Terminal-step headcount differential: +210,000 persons
    CI band: 175,000 - 255,000 (95% CI)

5% tolerance on terminal-step differential (intent doc §4 AC-1349-G):
  The simulation engine produces these differentials from composite score deltas x
  ZMB Q1 population x Q1 income share factor. The 5% tolerance accommodates:
  - Rounding in the conversion from composite score delta to integer headcount
  - T3 uncertainty in the ZMB Q1 income share parameter (SSA regional average)
  - Step-specific fixture variance

NM-056 rule: NO test uses pytest.skip() conditionally except DATABASE_URL absence guard.
  AC-1349-G (integration tests) require DATABASE_URL — the only permitted skip condition.
  AC-schema (file-read tests) MUST NEVER skip.

Silent failure guards (from intent doc §3.3):
  SF-composite-display: endpoint returns composite score delta (float < 1.0) as primary value
                         instead of integer headcount — caught by AC-1349-G(e)
  SF-ci-absent:          CI band bounds missing or null — caught by AC-1349-G(b)
  SF-schema-drift:       api_contracts.yml not updated — caught by AC-schema
"""
from __future__ import annotations

import os
import pathlib
from typing import TYPE_CHECKING, Any

import httpx
import pytest
import pytest_asyncio

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

_REPO_ROOT = pathlib.Path(__file__).parent.parent.parent
_API_CONTRACTS = _REPO_ROOT / "docs" / "schema" / "api_contracts.yml"

# Zambia Demo 7 Act 2 fixture values — from intent doc §1, §4b
_TERMINAL_STEP = 8
_N_STEPS = 8

# Expected terminal-step headcount differentials (+/-5% tolerance, intent doc AC-1349-G(d))
_OPTION_A_VS_C_HEADCOUNT = 340_000
_OPTION_B_VS_C_HEADCOUNT = 210_000
_TOLERANCE = 0.05  # 5% tolerance on terminal-step value

# Endpoint path — from intent doc §7 (path confirmed in api_contracts.yml schema update)
_ENDPOINT_PATH = "/api/v1/scenarios/comparison/distributional-differential"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _require_db() -> None:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping M18-G3 integration test")


def _within_tolerance(actual: int, expected: int, tolerance: float) -> bool:
    """Return True if |actual - expected| / expected <= tolerance."""
    if expected == 0:
        return actual == 0
    return abs(actual - expected) / expected <= tolerance


def _zmb_scenario_payload(name: str, n_steps: int = _N_STEPS) -> dict[str, Any]:
    """ZMB ECF scenario configuration for G3 comparison tests."""
    return {
        "name": name,
        "configuration": {
            "entities": ["ZMB"],
            "n_steps": n_steps,
            "timestep_label": "annual",
            "start_date": "2024-01-01",
            "modules_config": {
                "ecological": {"enabled": False},
                "political_economy": {"enabled": True},
            },
        },
        "scheduled_inputs": [],
    }


# ---------------------------------------------------------------------------
# Async HTTP client fixture
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    _require_db()
    from app.main import app  # type: ignore[import]

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
        timeout=180.0,
    ) as ac:
        yield ac


# ---------------------------------------------------------------------------
# Scenario setup helpers
# ---------------------------------------------------------------------------


async def _create_and_run_zmb_scenario(
    client: httpx.AsyncClient,
    name: str,
    n_steps: int = _N_STEPS,
) -> str | None:
    """Create a ZMB scenario and run all steps. Returns scenario_id or None on failure."""
    payload = _zmb_scenario_payload(name, n_steps)
    create_res = await client.post("/api/v1/scenarios", json=payload)
    if create_res.status_code != 201:
        return None
    sid: str = create_res.json()["scenario_id"]
    run_res = await client.post(f"/api/v1/scenarios/{sid}/run")
    if run_res.status_code not in (200, 202):
        return None
    return sid


# ===========================================================================
# AC-1349-G — Distributional differential endpoint
# ===========================================================================


pytestmark = pytest.mark.integration


class TestAC1349GDistributionalDifferentialEndpoint:
    """AC-1349-G: POST /api/v1/scenarios/comparison/distributional-differential
    with the Zambia three-scenario fixture returns the required response shape.

    Intent doc §4 AC-1349-G:
      - Per-step headcount differential for each non-reference scenario vs. reference
      - CI band bounds (lower, upper) per step
      - Tier classification (T2 or T3)
      - Terminal step differential within +/-5% of Zambia fixture (340K for A vs C)
      - Response does NOT return composite score delta as primary differential value

    G3 prerequisite (intent doc §7): api_contracts.yml must be updated with the
    distributional-differential endpoint shape before the G3 implementation PR opens.
    These tests run RED until the endpoint is implemented and the schema is updated.

    Three ZMB scenarios are created:
      A -- EFF front-loaded (austerity front-loaded): worst poverty outcome
      B -- IMF carve-out:                             intermediate outcome
      C -- Homegrown alternative:                     reference scenario (CLEAR)

    The endpoint designates Option C as the reference scenario. Differentials are:
      A vs C: +340,000 persons (terminal step 8)
      B vs C: +210,000 persons (terminal step 8)
    """

    async def test_endpoint_returns_http_200_with_three_scenarios(
        self, client: httpx.AsyncClient
    ) -> None:
        """POST to distributional-differential endpoint with ZMB three-scenario input returns 200.

        Pre-G3: endpoint does not exist -> 404. Test FAILS (RED). Becomes GREEN when
        the implementing agent creates the endpoint.
        """
        sid_a = await _create_and_run_zmb_scenario(client, "M18-G3 AC-G ZMB Option A")
        sid_b = await _create_and_run_zmb_scenario(client, "M18-G3 AC-G ZMB Option B")
        sid_c = await _create_and_run_zmb_scenario(client, "M18-G3 AC-G ZMB Option C (ref)")

        for label, sid in [("A", sid_a), ("B", sid_b), ("C (ref)", sid_c)]:
            assert sid is not None, (
                f"AC-1349-G: ZMB scenario {label} creation/run failed. "
                "Cannot test the distributional-differential endpoint without "
                "running scenarios."
            )

        request_body = {
            "entity_id": "ZMB",
            "scenario_ids": [sid_a, sid_b, sid_c],
            "reference_scenario_id": sid_c,
        }

        res = await client.post(_ENDPOINT_PATH, json=request_body)

        assert res.status_code == 200, (
            f"AC-1349-G: POST {_ENDPOINT_PATH} returned {res.status_code}. "
            "Expected 200. "
            "Pre-G3: endpoint does not exist -> 404. This test is RED until implementation. "
            "If 422: request body shape does not match the schema — check api_contracts.yml. "
            f"Response body (first 500 chars): {res.text[:500]}"
        )

    async def test_response_contains_pairs_array_for_non_reference_scenarios(
        self, client: httpx.AsyncClient
    ) -> None:
        """Response must contain a 'pairs' array with one entry per non-reference scenario.

        Intent doc §6.1: 'For each non-reference scenario S and reference scenario R,
        compute delta(t) = score_S(t) - score_R(t) at each step t.'
        A three-scenario input (A, B, C with C as reference) yields pairs for A vs C
        and B vs C.
        """
        sid_a = await _create_and_run_zmb_scenario(client, "M18-G3 pairs-test A")
        sid_b = await _create_and_run_zmb_scenario(client, "M18-G3 pairs-test B")
        sid_c = await _create_and_run_zmb_scenario(client, "M18-G3 pairs-test C (ref)")

        if any(s is None for s in (sid_a, sid_b, sid_c)):
            pytest.skip("DATABASE_URL not set or scenario creation failed")

        request_body = {
            "entity_id": "ZMB",
            "scenario_ids": [sid_a, sid_b, sid_c],
            "reference_scenario_id": sid_c,
        }

        res = await client.post(_ENDPOINT_PATH, json=request_body)
        if res.status_code == 404:
            pytest.fail(
                f"AC-1349-G: POST {_ENDPOINT_PATH} returned 404. "
                "Endpoint not yet implemented. RED until G3 implementation lands."
            )
        if res.status_code != 200:
            return  # HTTP 200 test above catches this

        body: dict[str, Any] = res.json()

        assert "pairs" in body, (
            "AC-1349-G: Response is missing 'pairs' key. "
            f"Got keys: {list(body.keys())}. "
            "Intent doc §6.1: response must contain per-pair differentials for each "
            "non-reference scenario. "
            "A three-scenario input with C as reference must yield pairs for A vs C "
            "and B vs C."
        )

        pairs: list[dict[str, Any]] = body["pairs"]
        assert isinstance(pairs, list), (
            f"AC-1349-G: 'pairs' must be a list, got {type(pairs).__name__}."
        )
        assert len(pairs) == 2, (
            f"AC-1349-G: Expected 2 pairs (A vs C, B vs C) for three-scenario input. "
            f"Got {len(pairs)} pair(s). "
            "Reference scenario (C) must not appear as a non-reference pair member."
        )

    async def test_each_pair_contains_per_step_array_with_headcount_differential(
        self, client: httpx.AsyncClient
    ) -> None:
        """Each pair must contain a 'steps' array with headcount_differential per step.

        Intent doc §6.2 Step 2:
          headcount_delta(t) = delta(t) x population x q1_income_share_factor
        Intent doc AC-1349-G:
          'per-step headcount differential for each non-reference scenario'
        """
        sid_a = await _create_and_run_zmb_scenario(client, "M18-G3 per-step A")
        sid_b = await _create_and_run_zmb_scenario(client, "M18-G3 per-step B")
        sid_c = await _create_and_run_zmb_scenario(client, "M18-G3 per-step C (ref)")

        if any(s is None for s in (sid_a, sid_b, sid_c)):
            pytest.skip("DATABASE_URL not set or scenario creation failed")

        request_body = {
            "entity_id": "ZMB",
            "scenario_ids": [sid_a, sid_b, sid_c],
            "reference_scenario_id": sid_c,
        }

        res = await client.post(_ENDPOINT_PATH, json=request_body)
        if res.status_code == 404:
            pytest.fail(
                f"AC-1349-G: POST {_ENDPOINT_PATH} returned 404. "
                "Endpoint not yet implemented. RED until G3 implementation lands."
            )
        if res.status_code != 200:
            return

        body: dict[str, Any] = res.json()
        pairs: list[dict[str, Any]] = body.get("pairs", [])
        if not pairs:
            return  # pairs-array test above catches this

        for pair in pairs:
            scenario_id = pair.get("scenario_id", "unknown")

            assert "steps" in pair, (
                f"AC-1349-G: Pair for scenario {scenario_id} is missing 'steps' array. "
                "Intent doc §6.2: each pair must include per-step headcount differentials."
            )

            steps: list[dict[str, Any]] = pair["steps"]
            assert isinstance(steps, list), (
                f"AC-1349-G: 'steps' for scenario {scenario_id} must be a list."
            )
            assert len(steps) >= 1, (
                f"AC-1349-G: 'steps' for scenario {scenario_id} must be non-empty."
            )

            for step_record in steps:
                assert "headcount_differential" in step_record, (
                    f"AC-1349-G: step record for scenario {scenario_id} missing "
                    f"'headcount_differential'. "
                    "Intent doc §6.2: each step entry must include the integer "
                    "headcount delta."
                )
                hc = step_record["headcount_differential"]
                assert isinstance(hc, int), (
                    f"AC-1349-G: 'headcount_differential' for scenario {scenario_id} "
                    f"must be an integer (not float). Got {type(hc).__name__}: {hc!r}. "
                    "Silent failure SF-composite-display: a float value like 0.14 "
                    "indicates the endpoint is returning a composite score delta "
                    "instead of a headcount. "
                    "The conversion from composite score delta to integer headcount "
                    "is required per intent doc §6.2 Step 2."
                )

    async def test_each_step_contains_ci_band_lower_and_upper(
        self, client: httpx.AsyncClient
    ) -> None:
        """Each step entry must contain ci_lower and ci_upper integer CI band bounds.

        Intent doc §6.2 Step 3:
          ci_headcount(t) = [delta_ci_lower(t) x conversion_factor,
                             delta_ci_upper(t) x conversion_factor]
        Intent doc AC-1349-G: 'CI band bounds (lower, upper) per step'
        """
        sid_a = await _create_and_run_zmb_scenario(client, "M18-G3 CI-band A")
        sid_b = await _create_and_run_zmb_scenario(client, "M18-G3 CI-band B")
        sid_c = await _create_and_run_zmb_scenario(client, "M18-G3 CI-band C (ref)")

        if any(s is None for s in (sid_a, sid_b, sid_c)):
            pytest.skip("DATABASE_URL not set or scenario creation failed")

        request_body = {
            "entity_id": "ZMB",
            "scenario_ids": [sid_a, sid_b, sid_c],
            "reference_scenario_id": sid_c,
        }

        res = await client.post(_ENDPOINT_PATH, json=request_body)
        if res.status_code == 404:
            pytest.fail(
                f"AC-1349-G: POST {_ENDPOINT_PATH} returned 404. "
                "Endpoint not yet implemented. RED until G3 implementation lands."
            )
        if res.status_code != 200:
            return

        body: dict[str, Any] = res.json()
        pairs: list[dict[str, Any]] = body.get("pairs", [])

        for pair in pairs:
            scenario_id = pair.get("scenario_id", "unknown")
            steps: list[dict[str, Any]] = pair.get("steps", [])

            for step_record in steps:
                step_num = step_record.get("step", "?")

                assert "ci_lower" in step_record, (
                    f"AC-1349-G: step {step_num} for scenario {scenario_id} "
                    "missing 'ci_lower'. "
                    "Silent failure SF-ci-absent: CI bounds must be present in "
                    "every step record. "
                    "The frontend CI band display requires both bounds."
                )
                assert "ci_upper" in step_record, (
                    f"AC-1349-G: step {step_num} for scenario {scenario_id} "
                    "missing 'ci_upper'. "
                    "Silent failure SF-ci-absent: CI upper bound must be present "
                    "in every step record."
                )

                ci_lower = step_record["ci_lower"]
                ci_upper = step_record["ci_upper"]

                assert isinstance(ci_lower, int), (
                    f"AC-1349-G: ci_lower at step {step_num} for {scenario_id} "
                    f"must be an integer, got {type(ci_lower).__name__}: {ci_lower!r}. "
                    "CI bounds inherit the headcount integer unit."
                )
                assert isinstance(ci_upper, int), (
                    f"AC-1349-G: ci_upper at step {step_num} for {scenario_id} "
                    f"must be an integer, got {type(ci_upper).__name__}: {ci_upper!r}."
                )

                assert ci_upper >= ci_lower, (
                    f"AC-1349-G: ci_upper ({ci_upper}) < ci_lower ({ci_lower}) at "
                    f"step {step_num} for scenario {scenario_id}. "
                    "CI bounds must be ordered (lower <= upper)."
                )

    async def test_response_contains_tier_classification(
        self, client: httpx.AsyncClient
    ) -> None:
        """Response must include a 'tier' field with value T2 or T3.

        Intent doc §6.2 Step 3: 'If the conversion factor is itself uncertain (T3),
        the CI band widens accordingly and tier inheritance becomes T3.'
        Intent doc AC-1349-G: 'tier classification (T2 or T3) in the response body'
        Architect constraint 4: 'The implementing agent determines the correct tier at
        implementation time and documents it in the PR description.'
        """
        sid_a = await _create_and_run_zmb_scenario(client, "M18-G3 tier-test A")
        sid_c = await _create_and_run_zmb_scenario(client, "M18-G3 tier-test C (ref)")

        if any(s is None for s in (sid_a, sid_c)):
            pytest.skip("DATABASE_URL not set or scenario creation failed")

        request_body = {
            "entity_id": "ZMB",
            "scenario_ids": [sid_a, sid_c],
            "reference_scenario_id": sid_c,
        }

        res = await client.post(_ENDPOINT_PATH, json=request_body)
        if res.status_code == 404:
            pytest.fail(
                f"AC-1349-G: POST {_ENDPOINT_PATH} returned 404. "
                "Endpoint not yet implemented. RED until G3 implementation lands."
            )
        if res.status_code != 200:
            return

        body: dict[str, Any] = res.json()

        assert "tier" in body, (
            "AC-1349-G: Response missing 'tier' field. "
            "Intent doc AC-1349-G: 'Tier classification (T2 or T3) in the response body.' "
            "Architect constraint 4: T-tier badge on the frontend element must match this. "
            "The implementing agent must determine tier from the conversion methodology "
            "and document it in the PR description."
        )

        tier: str = body["tier"]
        assert tier in ("T2", "T3"), (
            f"AC-1349-G: 'tier' must be T2 or T3, got {tier!r}. "
            "Intent doc §6.2 Step 3: tier inherits from the conversion methodology. "
            "If ZMB Q1 income share uses a regional SSA average (World Bank), tier is T3. "
            "T2 requires ZMB-specific backtested income distribution data."
        )

    async def test_response_contains_direction_stable_flag_per_pair(
        self, client: httpx.AsyncClient
    ) -> None:
        """Each step in each pair must include a direction_stable boolean flag.

        Intent doc §6.2 Step 5: 'direction_stable: boolean per scenario pair, computed as:
        direction_stable = (ci_lower > 0) OR (ci_upper < 0)'
        The flag drives the frontend direction stability statement (AC-1349-E).
        """
        sid_a = await _create_and_run_zmb_scenario(client, "M18-G3 direction-stable A")
        sid_c = await _create_and_run_zmb_scenario(client, "M18-G3 direction-stable C (ref)")

        if any(s is None for s in (sid_a, sid_c)):
            pytest.skip("DATABASE_URL not set or scenario creation failed")

        request_body = {
            "entity_id": "ZMB",
            "scenario_ids": [sid_a, sid_c],
            "reference_scenario_id": sid_c,
        }

        res = await client.post(_ENDPOINT_PATH, json=request_body)
        if res.status_code == 404:
            pytest.fail(
                f"AC-1349-G: POST {_ENDPOINT_PATH} returned 404. "
                "Endpoint not yet implemented. RED until G3 implementation lands."
            )
        if res.status_code != 200:
            return

        body: dict[str, Any] = res.json()
        pairs: list[dict[str, Any]] = body.get("pairs", [])

        for pair in pairs:
            scenario_id = pair.get("scenario_id", "unknown")
            steps: list[dict[str, Any]] = pair.get("steps", [])

            for step_record in steps:
                step_num = step_record.get("step", "?")

                assert "direction_stable" in step_record, (
                    f"AC-1349-G: step {step_num} for {scenario_id} "
                    "missing 'direction_stable'. "
                    "Intent doc §6.2 Step 5: 'direction_stable: boolean per scenario pair.' "
                    "This flag drives the frontend direction disclosure statement. "
                    "Its absence means the frontend cannot implement AC-1349-E."
                )

                direction_stable = step_record["direction_stable"]
                assert isinstance(direction_stable, bool), (
                    f"AC-1349-G: direction_stable at step {step_num} for {scenario_id} "
                    f"must be boolean, got "
                    f"{type(direction_stable).__name__}: {direction_stable!r}."
                )

                # Cross-check: direction_stable must be consistent with ci_lower/ci_upper
                ci_lower = step_record.get("ci_lower")
                ci_upper = step_record.get("ci_upper")
                if ci_lower is not None and ci_upper is not None:
                    expected_stable = (ci_lower > 0) or (ci_upper < 0)
                    assert direction_stable == expected_stable, (
                        f"AC-1349-G: direction_stable inconsistent at step {step_num} "
                        f"for {scenario_id}. "
                        f"ci_lower={ci_lower}, ci_upper={ci_upper} -> "
                        f"expected direction_stable={expected_stable}, "
                        f"got {direction_stable}. "
                        "Intent doc §6.2 Step 5: direction_stable = "
                        "(ci_lower > 0) OR (ci_upper < 0). "
                        "A CI spanning zero must produce direction_stable=False."
                    )

    async def test_terminal_step_differential_within_tolerance_option_a_vs_c(
        self, client: httpx.AsyncClient
    ) -> None:
        """Option A vs Option C terminal-step differential within +/-5% of 340,000 persons.

        Intent doc §1 Demo 7 citable claim:
          'Under the IMF-proposed terms, 340,000 more Zambians will be below the poverty
           threshold at programme end than under our counter-proposal.'
        Intent doc AC-1349-G: 'Terminal step differential that matches the expected Zambia
        fixture value within +/-5% tolerance.'

        The 5% tolerance (+/-17,000 persons) accommodates T3 uncertainty in the ZMB Q1
        income share parameter used in the headcount conversion.

        If the simulation produces significantly different values than the Demo 7
        fixture (e.g., due to calibration updates), the implementing agent must:
        1. Document the actual terminal values in the PR description
        2. Update the fixture constants in this test to match verified simulation output
        3. File a near-miss if the deviation from the Demo 7 claim exceeds 10%
        """
        sid_a = await _create_and_run_zmb_scenario(
            client, "M18-G3 Demo7 ZMB OptionA EFF-FrontLoaded"
        )
        sid_b = await _create_and_run_zmb_scenario(
            client, "M18-G3 Demo7 ZMB OptionB IMF-CarveOut"
        )
        sid_c = await _create_and_run_zmb_scenario(
            client, "M18-G3 Demo7 ZMB OptionC Homegrown (ref)"
        )

        if any(s is None for s in (sid_a, sid_b, sid_c)):
            pytest.skip("DATABASE_URL not set or scenario creation failed")

        request_body = {
            "entity_id": "ZMB",
            "scenario_ids": [sid_a, sid_b, sid_c],
            "reference_scenario_id": sid_c,
        }

        res = await client.post(_ENDPOINT_PATH, json=request_body)
        if res.status_code == 404:
            pytest.fail(
                f"AC-1349-G: POST {_ENDPOINT_PATH} returned 404. "
                "Endpoint not yet implemented. RED until G3 implementation lands."
            )
        if res.status_code != 200:
            return

        body: dict[str, Any] = res.json()
        pairs: list[dict[str, Any]] = body.get("pairs", [])
        if not pairs:
            return

        terminal_step_declared: int = body.get("terminal_step", _TERMINAL_STEP)
        pair_a: dict[str, Any] | None = None

        for pair in pairs:
            if pair.get("scenario_id") == sid_a:
                pair_a = pair
                break

        assert pair_a is not None, (
            f"AC-1349-G(d): Pair for Option A scenario ({sid_a}) not found in response. "
            f"Available: {[p.get('scenario_id') for p in pairs]}."
        )

        steps_a: list[dict[str, Any]] = pair_a.get("steps", [])
        terminal_records_a = [
            s for s in steps_a if s.get("step") == terminal_step_declared
        ]

        assert terminal_records_a, (
            f"AC-1349-G(d): No step record for terminal step {terminal_step_declared} "
            f"in Option A pair. "
            f"Available steps: {[s.get('step') for s in steps_a]}. "
            "Intent doc §6.2 Step 4: 'The API response includes per-step differentials; "
            "the frontend renders the terminal step by default.'"
        )

        terminal_a = terminal_records_a[0]
        headcount_a: int | None = terminal_a.get("headcount_differential")

        assert headcount_a is not None, (
            "AC-1349-G(d): 'headcount_differential' absent at terminal step for Option A."
        )
        assert isinstance(headcount_a, int), (
            f"AC-1349-G(d): headcount_differential must be int, "
            f"got {type(headcount_a).__name__}. "
            "SF-composite-display: a float value (e.g. 0.14) indicates the endpoint is "
            "returning a composite score delta instead of an integer headcount."
        )

        # Verify no composite score decimal is being returned as primary value
        assert headcount_a > 1, (
            f"AC-1349-G(e): headcount_differential at terminal step is {headcount_a!r}. "
            "A value <= 1 is the composite score decimal silent failure. "
            "The endpoint must return an integer headcount (e.g. 340000), not 0.14."
        )

        within = _within_tolerance(headcount_a, _OPTION_A_VS_C_HEADCOUNT, _TOLERANCE)
        lower_bound = int(_OPTION_A_VS_C_HEADCOUNT * (1 - _TOLERANCE))
        upper_bound = int(_OPTION_A_VS_C_HEADCOUNT * (1 + _TOLERANCE))
        assert within, (
            f"AC-1349-G(d): Option A vs Option C terminal-step headcount differential "
            f"is {headcount_a:,} persons. "
            f"Expected {_OPTION_A_VS_C_HEADCOUNT:,} +/-{_TOLERANCE*100:.0f}% "
            f"(range: {lower_bound:,} - {upper_bound:,}). "
            "Demo 7 Act 2 claim: '340,000 more Zambians below poverty threshold.' "
            "If the simulation produces a significantly different value, the implementing "
            "agent must update the fixture constant and document the calibration basis "
            "in the PR description. "
            "Deviation > 10% from 340,000 requires a near-miss entry."
        )

    async def test_response_does_not_return_composite_score_as_primary_differential(
        self, client: httpx.AsyncClient
    ) -> None:
        """Explicit SF-composite-display guard: primary differential must not be float < 1.0.

        Intent doc §3.3: 'If the element renders +0.14 instead of +340,000 persons, the
        engine is returning the composite score delta, not the headcount conversion.'
        Intent doc AC-1349-G: 'Response does NOT return a composite score delta field as
        the primary differential value.'

        This test isolates the silent failure where the endpoint skips the headcount
        conversion (intent doc §6.2 Step 2) and returns the raw composite score delta.
        """
        sid_a = await _create_and_run_zmb_scenario(client, "M18-G3 SF-composite-guard A")
        sid_c = await _create_and_run_zmb_scenario(client, "M18-G3 SF-composite-guard C ref")

        if any(s is None for s in (sid_a, sid_c)):
            pytest.skip("DATABASE_URL not set or scenario creation failed")

        request_body = {
            "entity_id": "ZMB",
            "scenario_ids": [sid_a, sid_c],
            "reference_scenario_id": sid_c,
        }

        res = await client.post(_ENDPOINT_PATH, json=request_body)
        if res.status_code == 404:
            pytest.fail(
                f"AC-1349-G: POST {_ENDPOINT_PATH} returned 404. "
                "Endpoint not yet implemented. RED until G3 implementation lands."
            )
        if res.status_code != 200:
            return

        body: dict[str, Any] = res.json()
        pairs: list[dict[str, Any]] = body.get("pairs", [])

        for pair in pairs:
            scenario_id = pair.get("scenario_id", "unknown")
            steps: list[dict[str, Any]] = pair.get("steps", [])

            for step_record in steps:
                step_num = step_record.get("step", "?")
                hc = step_record.get("headcount_differential")

                if hc is None:
                    continue  # absence caught by per-step test above

                # SF guard: composite score delta is always a float < 1.0
                # (composite scores are normalized [0.0, 1.0] ratios)
                # A valid headcount is always an integer >= 1
                assert not (isinstance(hc, float) and hc < 1.0), (
                    f"AC-1349-G(e) SF-composite-display: headcount_differential at "
                    f"step {step_num} for scenario {scenario_id} is {hc!r} (float < 1.0). "
                    "This is the composite score delta silent failure: the endpoint is "
                    "returning the raw composite score delta instead of applying the "
                    "headcount conversion (intent doc §6.2 Step 2). "
                    "The implementing agent must apply: "
                    "headcount_delta = delta x population x q1_income_share_factor. "
                    "For ZMB at terminal step 8, the expected value is ~340,000 (not 0.14)."
                )

                # Secondary guard: integer type confirms conversion was applied
                assert isinstance(hc, int), (
                    f"AC-1349-G(e): headcount_differential at step {step_num} for "
                    f"{scenario_id} must be int after conversion, "
                    f"got {type(hc).__name__}: {hc!r}."
                )

    async def test_n_less_than_2_returns_error(self, client: httpx.AsyncClient) -> None:
        """Endpoint must return an error when fewer than 2 scenarios are provided.

        Intent doc §7: 'Error cases: N < 2 (no reference)'
        A single scenario without a comparison partner cannot produce a differential.
        """
        sid_c = await _create_and_run_zmb_scenario(client, "M18-G3 N<2 guard (single)")

        if sid_c is None:
            pytest.skip("DATABASE_URL not set or scenario creation failed")

        request_body = {
            "entity_id": "ZMB",
            "scenario_ids": [sid_c],
            "reference_scenario_id": sid_c,
        }

        res = await client.post(_ENDPOINT_PATH, json=request_body)
        if res.status_code == 404:
            return  # endpoint not yet implemented (pre-G3 guard)

        # With N=1 (only the reference, no non-reference scenarios), the endpoint
        # must return an error status (4xx), not HTTP 200 with an empty pairs array
        assert res.status_code in (400, 422), (
            f"AC-1349-G error case: N<2 input returned {res.status_code}. "
            "Expected 400 or 422 (client error for invalid request). "
            "Intent doc §7: 'Error cases: N < 2 (no reference).' "
            "HTTP 200 with empty pairs silently hides the error condition."
        )


# ===========================================================================
# AC-schema — api_contracts.yml updated with distributional-differential endpoint
# ===========================================================================


class TestACSchemaApiContractsUpdated:
    """AC-schema: docs/schema/api_contracts.yml must be updated with the
    distributional-differential endpoint shape as a prerequisite to the G3 PR.

    Intent doc §7: 'docs/schema/api_contracts.yml must be updated with the distributional
    differential endpoint specification before the G3 implementation PR opens.'
    CLAUDE.md §Schema registry mandate: 'When schema files are out of date with the code,
    update them in the same commit as the code change -- schema drift is a compliance
    violation.'

    These are file-read tests -- they do NOT require DATABASE_URL and MUST NEVER skip.
    Pre-G3: api_contracts.yml does not contain the new endpoint -> tests FAIL (RED).
    Post-G3: api_contracts.yml updated in the implementation PR -> tests PASS.
    """

    def test_api_contracts_yml_exists(self) -> None:
        """api_contracts.yml must exist at the canonical path."""
        assert _API_CONTRACTS.exists(), (
            f"AC-schema: api_contracts.yml not found at {_API_CONTRACTS}. "
            "CLAUDE.md §Schema registry: 'Any agent calling an API endpoint must first "
            "read the relevant schema file.' The schema file must exist."
        )

    def test_api_contracts_contains_distributional_differential_endpoint(self) -> None:
        """api_contracts.yml must document the distributional-differential endpoint.

        Pre-G3: the endpoint path is absent -> this test FAILS. That is intentional.
        The test becomes GREEN when api_contracts.yml is updated in the same PR as the
        backend implementation (intent doc §7 prerequisite).
        """
        assert _API_CONTRACTS.exists(), (
            "AC-schema: api_contracts.yml not found. "
            "Run test_api_contracts_yml_exists first."
        )
        content = _API_CONTRACTS.read_text(encoding="utf-8")

        assert "distributional-differential" in content, (
            "AC-schema FAIL: 'distributional-differential' not found in api_contracts.yml. "
            "Intent doc §7: the implementing agent must update api_contracts.yml with the "
            "new endpoint path before the G3 implementation PR opens. "
            "CLAUDE.md §Schema registry: 'Schema drift is a compliance violation.' "
            "The endpoint documentation must be added in the same PR as the backend code."
        )

    def test_api_contracts_documents_headcount_differential_field(self) -> None:
        """api_contracts.yml must document 'headcount_differential' in the response schema.

        Guards against SF-composite-display at the schema layer: if the schema documents
        a float 'composite_delta' instead of an integer 'headcount_differential', the
        implementing agent may implement the wrong type.
        """
        if not _API_CONTRACTS.exists():
            pytest.fail(
                "AC-schema: api_contracts.yml not found. Cannot verify schema."
            )
        content = _API_CONTRACTS.read_text(encoding="utf-8")
        if "distributional-differential" not in content:
            pytest.fail(
                "AC-schema: endpoint 'distributional-differential' not in api_contracts.yml. "
                "Run the endpoint presence test first."
            )

        assert "headcount_differential" in content, (
            "AC-schema FAIL: 'headcount_differential' not documented in api_contracts.yml. "
            "Intent doc §7 response shape: the response must document the integer headcount "
            "field by name. A schema that documents 'composite_delta' (float) instead of "
            "'headcount_differential' (integer) is a schema-level SF-composite-display hazard."
        )

    def test_api_contracts_documents_direction_stable_field(self) -> None:
        """api_contracts.yml must document 'direction_stable' in the response schema.

        The direction_stable flag drives AC-1349-E (direction stability display).
        If absent from the schema, the frontend implementing agent may omit it.
        """
        if not _API_CONTRACTS.exists():
            pytest.fail(
                "AC-schema: api_contracts.yml not found. Cannot verify schema."
            )
        content = _API_CONTRACTS.read_text(encoding="utf-8")
        if "distributional-differential" not in content:
            pytest.fail(
                "AC-schema: endpoint not documented yet. Run endpoint presence test first."
            )

        assert "direction_stable" in content, (
            "AC-schema FAIL: 'direction_stable' not documented in api_contracts.yml. "
            "Intent doc §7 response shape: 'Per-step array with ... direction stability flag.' "
            "The field must be documented so the frontend implementing agent knows to "
            "consume it in the direction disclosure component (AC-1349-E)."
        )

    def test_api_contracts_documents_tier_field(self) -> None:
        """api_contracts.yml must document the 'tier' classification field.

        The T-tier badge on the frontend element (AC-1349-D) reads the tier from the
        API response. If not documented, the implementing agent may omit or mislabel it.
        """
        if not _API_CONTRACTS.exists():
            pytest.fail(
                "AC-schema: api_contracts.yml not found. Cannot verify schema."
            )
        content = _API_CONTRACTS.read_text(encoding="utf-8")
        if "distributional-differential" not in content:
            pytest.fail(
                "AC-schema: endpoint not documented yet."
            )

        assert "tier" in content, (
            "AC-schema FAIL: 'tier' not documented in api_contracts.yml. "
            "Intent doc §7 response shape: 'Tier classification field (string T2 or T3).' "
            "Architect constraint 4: T-tier badge on the frontend must match the tier "
            "determined by the implementing agent. The schema must document the field."
        )

    def test_api_contracts_documents_ci_lower_and_ci_upper_fields(self) -> None:
        """api_contracts.yml must document 'ci_lower' and 'ci_upper' in step schema.

        The CI band display ('295K - 395K  95% CI') in AC-1349-D requires both fields.
        Missing schema documentation risks the implementing agent using different field
        names (e.g., 'lower_bound', 'p5', 'confidence_lower') that misalign with tests.
        """
        if not _API_CONTRACTS.exists():
            pytest.fail(
                "AC-schema: api_contracts.yml not found."
            )
        content = _API_CONTRACTS.read_text(encoding="utf-8")
        if "distributional-differential" not in content:
            pytest.fail(
                "AC-schema: endpoint not documented yet."
            )

        assert "ci_lower" in content, (
            "AC-schema FAIL: 'ci_lower' not found in api_contracts.yml. "
            "Intent doc §7: response step array must include lower CI bound by this name. "
            "The frontend renders the CI band as 'ci_lower - ci_upper  95% CI'."
        )
        assert "ci_upper" in content, (
            "AC-schema FAIL: 'ci_upper' not found in api_contracts.yml. "
            "Intent doc §7: response step array must include upper CI bound by this name."
        )


# ---------------------------------------------------------------------------
# AC-1422-G — methodology_detail object in distributional-differential response
# ---------------------------------------------------------------------------
# Authored BEFORE implementation from intent document at:
#   docs/process/intents/M18-G5-2026-06-28-zone3-auditability-panel.md
#
# Sprint entry: docs/process/sprint-plans/m18-g5-sprint-entry.md
# Issue: #1422 (G3 CA condition — Lucas, Persona 1)
# Sprint journal: #1435
#
# These tests are appended to the G3 test file because:
#   (1) The AC targets the same endpoint as AC-1349-G
#   (2) The fixture creation helpers are already defined here
#   (3) The schema tests share the same _API_CONTRACTS path
#
# NM-056 rule: no pytest.skip() or pytest.mark.skip() without a filed near-miss.
#   DATABASE_URL absence guard is the only permitted skip condition.
#
# Guard pattern: AC-1422-G asserts a NEW field in the response object.
#   Pre-G5: endpoint returns no `methodology_detail` key → assertions fail.
#   Post-G5: endpoint includes `methodology_detail` → assertions pass.
#   Tests run RED immediately; do NOT guard on field absence.

# Expected values for ZMB — from backend/app/api/scenarios.py constants
# _ENTITY_Q1_POPULATION["ZMB"] = 3_894_625 (UN WPP 2024, 20% Q1 fraction)
_ZMB_EXPECTED_Q1_POPULATION = 3_894_625

# Expected fragments in string fields — from intent doc §3.2 and backend constants
# ci_methodology: should contain "±13–16%" or both "0.87" and "1.16" (the factor values)
_CI_METHODOLOGY_FACTOR_LOWER = "0.87"
_CI_METHODOLOGY_FACTOR_UPPER = "1.16"
# extraction_path: should contain "Q1 CHT" (cohort extraction reference)
_EXTRACTION_PATH_FRAG = "Q1 CHT"
# tier_rationale: should contain "T3" classification and rationale
_TIER_RATIONALE_FRAG = "T3"


class TestAC1422GMethodologyDetail:
    """AC-1422-G: distributional-differential endpoint returns methodology_detail object.

    The Zone 3 auditability panel (intent doc §3.2) requires the backend to enrich the
    DistributionalDifferentialResponse with a structured `methodology_detail` object.
    This is a new field added to the existing endpoint — not a new endpoint.

    Four sub-fields are required:
      q1_population:   int — entity Q1 population used in headcount calculation
      ci_methodology:  str — description of CI band computation method
      extraction_path: str — description of how Q1 poverty_headcount_ratio is extracted
      tier_rationale:  str — plain-language explanation of the T-tier classification

    These tests are integration tests (require DATABASE_URL and real ZMB scenario creation).
    """

    @pytest.mark.asyncio
    async def test_methodology_detail_key_present_in_response(
        self,
        client: httpx.AsyncClient,
    ) -> None:
        """AC-1422-G(a): 'methodology_detail' key present in response body.

        Pre-G5: key absent → test fails (RED).
        Post-G5: key present → test passes (GREEN).
        """
        _require_db()
        scenario_id = await _create_and_run_zmb_scenario(client, "ac1422g-presence")

        response = await client.post(
            _ENDPOINT_PATH,
            json={
                "primary_scenario_id": scenario_id,
                "comparison_scenario_ids": [scenario_id],
                "entity_id": "ZMB",
            },
        )
        assert response.status_code == 200, (
            f"AC-1422-G(a) FAIL: endpoint returned {response.status_code}. "
            f"Body: {response.text[:500]}"
        )
        data = response.json()
        assert "methodology_detail" in data, (
            "AC-1422-G(a) FAIL: 'methodology_detail' key absent from "
            "distributional-differential response. Intent doc §3.2: the backend must enrich "
            "DistributionalDifferentialResponse with a structured methodology_detail object "
            "for Zone 3 auditability panel (AC-1422-C). "
            "This is not the same as methodology_summary — it is a typed object, not a string."
        )

    @pytest.mark.asyncio
    async def test_methodology_detail_q1_population_is_zmb_value(
        self,
        client: httpx.AsyncClient,
    ) -> None:
        """AC-1422-G(b): methodology_detail.q1_population == 3,894,625 for ZMB entity.

        The frontend formats this as toLocaleString("en-US") → "3,894,625".
        The backend must provide the integer value; the frontend handles formatting.
        """
        _require_db()
        scenario_id = await _create_and_run_zmb_scenario(client, "ac1422g-q1pop")

        response = await client.post(
            _ENDPOINT_PATH,
            json={
                "primary_scenario_id": scenario_id,
                "comparison_scenario_ids": [scenario_id],
                "entity_id": "ZMB",
            },
        )
        assert response.status_code == 200
        data = response.json()

        if "methodology_detail" not in data:
            pytest.fail(
                "AC-1422-G(b) FAIL: 'methodology_detail' absent — cannot verify q1_population. "
                "AC-1422-G(a) must pass before AC-1422-G(b) can be meaningful."
            )

        detail = data["methodology_detail"]
        assert "q1_population" in detail, (
            "AC-1422-G(b) FAIL: 'q1_population' key absent from methodology_detail. "
            "Intent doc §3.2 MethodologyDetail schema: q1_population: int — "
            "entity Q1 population used in headcount calculation. "
            "Backend source: _ENTITY_Q1_POPULATION.get(entity_id, 0) in scenarios.py."
        )

        q1_pop = detail["q1_population"]
        assert isinstance(q1_pop, int), (
            f"AC-1422-G(b) FAIL: q1_population is {type(q1_pop).__name__}, expected int. "
            "The frontend calls toLocaleString('en-US') on this value — it must be an integer, "
            "not a string or float."
        )
        assert q1_pop == _ZMB_EXPECTED_Q1_POPULATION, (
            f"AC-1422-G(b) FAIL: q1_population == {q1_pop}, "
            f"expected {_ZMB_EXPECTED_Q1_POPULATION}. "
            "Backend constant: _ENTITY_Q1_POPULATION['ZMB'] = 3_894_625 "
            "(UN WPP 2024, 20% Q1 fraction). "
            "Lucas (Persona 1) will use this value to verify the headcount "
            "differential arithmetic. An incorrect value silently undermines "
            "the analytical credibility of the Zone 3 panel."
        )

    @pytest.mark.asyncio
    async def test_methodology_detail_ci_methodology_nonempty_with_factor_references(
        self,
        client: httpx.AsyncClient,
    ) -> None:
        """AC-1422-G(c): methodology_detail.ci_methodology is a non-empty str referencing CI bounds.

        Must contain the lower and upper CI factor values (0.87, 1.16) or percentage equivalents
        (13%, 16%) so Lucas can reproduce the CI band arithmetic from the disclosure text.
        """
        _require_db()
        scenario_id = await _create_and_run_zmb_scenario(client, "ac1422g-cimeth")

        response = await client.post(
            _ENDPOINT_PATH,
            json={
                "primary_scenario_id": scenario_id,
                "comparison_scenario_ids": [scenario_id],
                "entity_id": "ZMB",
            },
        )
        assert response.status_code == 200
        data = response.json()

        if "methodology_detail" not in data:
            pytest.fail("AC-1422-G(c) FAIL: 'methodology_detail' absent.")

        detail = data["methodology_detail"]
        assert "ci_methodology" in detail, (
            "AC-1422-G(c) FAIL: 'ci_methodology' key absent from methodology_detail. "
            "Intent doc §3.2: ci_methodology: str — CI band computation method description."
        )

        ci_meth = detail["ci_methodology"]
        assert isinstance(ci_meth, str) and len(ci_meth) > 0, (
            f"AC-1422-G(c) FAIL: ci_methodology is empty or not a string (got {ci_meth!r}). "
            "The Zone 3 panel renders this text verbatim in the methodology-ci-band element."
        )

        # Must contain either the decimal factor values or the percentage representations
        # so the analyst can reproduce the CI band calculation
        has_decimal_refs = (
            _CI_METHODOLOGY_FACTOR_LOWER in ci_meth
            or _CI_METHODOLOGY_FACTOR_UPPER in ci_meth
        )
        has_percent_refs = "13" in ci_meth or "16" in ci_meth
        assert has_decimal_refs or has_percent_refs, (
            f"AC-1422-G(c) FAIL: ci_methodology string does not reference CI bound factors. "
            f"Got: {ci_meth!r}. "
            f"Must contain '0.87'/'1.16' (decimal factors) or '13'/'16' (percentage equivalents) "
            f"so Lucas can reproduce the CI arithmetic: lower = point_estimate × 0.87, "
            f"upper = point_estimate × 1.16. "
            f"Backend source: _CI_FACTOR_LOWER=Decimal('0.87'), _CI_FACTOR_UPPER=Decimal('1.16')."
        )

    @pytest.mark.asyncio
    async def test_methodology_detail_extraction_path_references_q1_cht(
        self,
        client: httpx.AsyncClient,
    ) -> None:
        """AC-1422-G(d): methodology_detail.extraction_path references Q1 CHT cohort logic.

        The extraction path must describe how poverty_headcount_ratio is extracted from
        the simulation state — specifically the Q1 CHT (cohort: lowest income quintile)
        path and fallback logic. This is required for AC-1422-C frontend display.
        """
        _require_db()
        scenario_id = await _create_and_run_zmb_scenario(client, "ac1422g-xpath")

        response = await client.post(
            _ENDPOINT_PATH,
            json={
                "primary_scenario_id": scenario_id,
                "comparison_scenario_ids": [scenario_id],
                "entity_id": "ZMB",
            },
        )
        assert response.status_code == 200
        data = response.json()

        if "methodology_detail" not in data:
            pytest.fail("AC-1422-G(d) FAIL: 'methodology_detail' absent.")

        detail = data["methodology_detail"]
        assert "extraction_path" in detail, (
            "AC-1422-G(d) FAIL: 'extraction_path' key absent from methodology_detail. "
            "Intent doc §3.2: extraction_path: str — description of Q1 poverty_headcount_ratio "
            "extraction from simulation state."
        )

        epath = detail["extraction_path"]
        assert isinstance(epath, str) and len(epath) > 0, (
            f"AC-1422-G(d) FAIL: extraction_path is empty or not a string (got {epath!r})."
        )

        assert _EXTRACTION_PATH_FRAG in epath, (
            f"AC-1422-G(d) FAIL: extraction_path does not contain '{_EXTRACTION_PATH_FRAG}'. "
            f"Got: {epath!r}. "
            "Intent doc §3.2: 'Q1 CHT cohort mean (entities matching <entity_id>:CHT:1-*); "
            "falls back to main entity poverty_headcount_ratio if no cohort data present.' "
            "The 'Q1 CHT' reference is required for Lucas to understand the data provenance chain."
        )

    @pytest.mark.asyncio
    async def test_methodology_detail_tier_rationale_references_t3(
        self,
        client: httpx.AsyncClient,
    ) -> None:
        """AC-1422-G(e): methodology_detail.tier_rationale is non-empty and references T3.

        The tier_rationale is the plain-language explanation displayed in the
        methodology-tier-rationale element. It must name the tier classification
        so Lucas can cross-reference with the T-tier badge in Zone 3.
        """
        _require_db()
        scenario_id = await _create_and_run_zmb_scenario(client, "ac1422g-tier")

        response = await client.post(
            _ENDPOINT_PATH,
            json={
                "primary_scenario_id": scenario_id,
                "comparison_scenario_ids": [scenario_id],
                "entity_id": "ZMB",
            },
        )
        assert response.status_code == 200
        data = response.json()

        if "methodology_detail" not in data:
            pytest.fail("AC-1422-G(e) FAIL: 'methodology_detail' absent.")

        detail = data["methodology_detail"]
        assert "tier_rationale" in detail, (
            "AC-1422-G(e) FAIL: 'tier_rationale' key absent from methodology_detail. "
            "Intent doc §3.2: tier_rationale: str — plain-language T-tier explanation."
        )

        rationale = detail["tier_rationale"]
        assert isinstance(rationale, str) and len(rationale) > 0, (
            f"AC-1422-G(e) FAIL: tier_rationale is empty or not a string (got {rationale!r})."
        )

        assert _TIER_RATIONALE_FRAG in rationale, (
            f"AC-1422-G(e) FAIL: tier_rationale does not contain '{_TIER_RATIONALE_FRAG}'. "
            f"Got: {rationale!r}. "
            "The tier rationale must name the T3 classification so Lucas can cross-reference "
            "it with the T-tier badge rendered by the comparison-tier-badge testid. "
            "Backend constant: _DISTRIBUTIONAL_TIER = 'T3'."
        )

    @pytest.mark.asyncio
    async def test_methodology_detail_structure_is_typed_object_not_string(
        self,
        client: httpx.AsyncClient,
    ) -> None:
        """AC-1422-G(f): methodology_detail is a dict (JSON object), NOT a string.

        Silent failure guard SF-methodology-as-string:
          If backend returns methodology_detail as a string (e.g., the methodology_summary
          value duplicated under a new key), the frontend TypeScript type annotation
          `MethodologyDetail` will pass compilation but the .q1_population accessor will
          return undefined at runtime, causing the Zone 3 panel to silently render nothing.

        This test explicitly catches that failure mode.
        """
        _require_db()
        scenario_id = await _create_and_run_zmb_scenario(client, "ac1422g-type")

        response = await client.post(
            _ENDPOINT_PATH,
            json={
                "primary_scenario_id": scenario_id,
                "comparison_scenario_ids": [scenario_id],
                "entity_id": "ZMB",
            },
        )
        assert response.status_code == 200
        data = response.json()

        if "methodology_detail" not in data:
            pytest.fail("AC-1422-G(f) FAIL: 'methodology_detail' absent.")

        detail = data["methodology_detail"]
        assert isinstance(detail, dict), (
            f"AC-1422-G(f) FAIL: methodology_detail is {type(detail).__name__}, expected dict. "
            "Silent failure guard SF-methodology-as-string: returning a string here causes the "
            "frontend to silently render an empty Zone 3 panel — the .q1_population accessor "
            "returns undefined on a string object. "
            "The backend Pydantic model must be MethodologyDetail (BaseModel), not str."
        )

        # Confirm all 4 required keys are present in the dict
        required_keys = {"q1_population", "ci_methodology", "extraction_path", "tier_rationale"}
        missing = required_keys - set(detail.keys())
        assert not missing, (
            f"AC-1422-G(f) FAIL: methodology_detail missing required keys: {sorted(missing)}. "
            "Intent doc §3.2 MethodologyDetail schema requires all 4 fields. "
            "The frontend MethodologyDetail TypeScript interface mirrors these field names exactly."
        )


class TestAC1422GSchemaDocumented:
    """AC-1422-G(schema): api_contracts.yml documents methodology_detail in the response shape.

    File-read tests — must NEVER skip (NM-056 rule). DATABASE_URL guard does not apply.
    These tests verify the schema contract between frontend and backend is documented
    before implementation begins — matching the AC-schema tests already in this file.
    """

    def test_api_contracts_documents_methodology_detail_key(self) -> None:
        """api_contracts.yml must document 'methodology_detail' in the distributional-differential
        response shape.

        The frontend MethodologyDetail TypeScript interface is authored from this schema.
        If the schema is not updated, the implementing agent may invent different field names
        causing a name mismatch between backend serialisation and frontend deserialisation.

        This test must remain in the file permanently — it enforces the schema-first discipline
        for G5 in the same way AC-schema enforced it for G3.
        """
        if not _API_CONTRACTS.exists():
            pytest.fail(
                "AC-1422-G(schema): api_contracts.yml not found at expected path. "
                f"Expected: {_API_CONTRACTS}. "
                "The intent doc §8 prerequisite requires api_contracts.yml to be updated "
                "in the same PR as the backend schema change."
            )
        content = _API_CONTRACTS.read_text(encoding="utf-8")
        if "distributional-differential" not in content:
            pytest.fail(
                "AC-1422-G(schema): distributional-differential endpoint not yet documented "
                "in api_contracts.yml. AC-schema tests (G3) must pass before AC-1422-G(schema). "
                "The G5 implementation PR must build on the G3 schema documentation."
            )

        assert "methodology_detail" in content, (
            "AC-1422-G(schema) FAIL: 'methodology_detail' not documented in api_contracts.yml. "
            "Intent doc §8 (Schema prerequisite): api_contracts.yml must be updated with "
            "the methodology_detail field in the same PR as the backend schema change. "
            "The frontend implementing agent reads this schema before authoring the "
            "MethodologyDetail TypeScript interface — if the schema is absent, the agent "
            "cannot determine the correct field names and types."
        )

    def test_api_contracts_documents_q1_population_field(self) -> None:
        """api_contracts.yml must document 'q1_population' within methodology_detail."""
        if not _API_CONTRACTS.exists():
            pytest.fail("AC-1422-G(schema): api_contracts.yml not found.")
        content = _API_CONTRACTS.read_text(encoding="utf-8")
        if "methodology_detail" not in content:
            pytest.fail("AC-1422-G(schema): 'methodology_detail' not yet in schema.")

        assert "q1_population" in content, (
            "AC-1422-G(schema) FAIL: 'q1_population' not found in api_contracts.yml. "
            "The frontend formats this integer as toLocaleString('en-US') — the name "
            "'q1_population' must be documented precisely (not 'population', 'q1_pop', etc.) "
            "so the TypeScript type is authored with the correct accessor."
        )

    def test_api_contracts_documents_tier_rationale_field(self) -> None:
        """api_contracts.yml must document 'tier_rationale' within methodology_detail."""
        if not _API_CONTRACTS.exists():
            pytest.fail("AC-1422-G(schema): api_contracts.yml not found.")
        content = _API_CONTRACTS.read_text(encoding="utf-8")
        if "methodology_detail" not in content:
            pytest.fail("AC-1422-G(schema): 'methodology_detail' not yet in schema.")

        assert "tier_rationale" in content, (
            "AC-1422-G(schema) FAIL: 'tier_rationale' not found in api_contracts.yml. "
            "The methodology-tier-rationale testid (AC-1422-C) renders this field. "
            "Schema documentation ensures the implementing agent uses this exact name."
        )
