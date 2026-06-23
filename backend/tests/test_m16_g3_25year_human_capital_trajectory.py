"""QA tests for M16-G3: 25-year human capital depletion trajectory (#274).

QA Lead — authored from intent document at:
  docs/process/intents/M16-G3-2026-06-23-25year-human-capital-trajectory.md

CM review satisfied 2026-06-23 — AC-CM-1/AC-CM-2/AC-CM-3 confirmed.
These tests define "done" for G3 backend work. All AC tests will fail (or be
skipped pending DB) until the Chief Engineer Agent delivers the implementation.
An implementation PR must not be merged until every test below passes in CI.

NM-056 rule (soft-skip prevention): NO test uses pytest.skip() conditionally
except on DATABASE_URL absence for integration tests. No test.skip() patterns.
A test that cannot yet run returns without asserting — it does not skip.

AC coverage:
  AC-1  ScenarioConfigSchema accepts projection_steps field (Pydantic, no DB)
  AC-2  projection_steps=0 → ValidationError (Pydantic, no DB)
  AC-3  projection_steps=101 → ValidationError (Pydantic, no DB)
  AC-4  projection_steps absent → n_steps governs; ZMB 8-step non-regression (schema)
  AC-5  WebScenarioRunner applies adaptive_resolution=False when projection_steps > 8
  AC-6  Indicator bounds: poverty_headcount_ratio ∈ [0.0, 1.0] across 100 steps (DB)
  AC-7  Trajectory endpoint: exactly 100 step objects + quarterly spacing (DB)
  AC-8  api_contracts.yml documents projection_steps (filesystem, no DB)

CE Assessment enforcement:
  Decision 1 — adaptive_resolution override: enforced by AC-5
  Decision 2 — projection_steps on ScenarioConfigSchema: enforced by AC-1–AC-4, AC-8
  Decision 3 — CM pre-condition: SATISFIED 2026-06-23 (cm-review-gate in intent frontmatter)
  Decision 4 — dry-run obligation: enforced by AC-6 (indicator bounds in CI) + AC-7 (step count)

CM review findings (2026-06-23 — #274):
  - Only poverty_headcount_ratio has registered elasticities in DemographicModule
  - Three cohort curves: Q1 informal (SEN:CHT:1-25-54-INFORMAL), Q1 agriculture
    (SEN:CHT:1-25-54-AGRICULTURE), Q2 informal (SEN:CHT:2-25-54-INFORMAL)
  - MDA-HD-POVERTY-Q1 floor (≥ 0.40) applies directly to 100-step projection
  - Entity attribute store must clamp VariableType.RATIO to [0.0, 1.0];
    DemographicModule does not clamp internally (CE Assessment Decision 4 dry-run required)
  - No MDA-HD-POVERTY-Q2 floor registered; Q2 curve does not trigger milestone sentence

SEN fixture note (CE Assessment Decision 3):
  Integration tests use a synthetic SEN fixture — NOT ZMB values transposed.
  SEN entity seeded in source_registry via migration 2b821063ef81 (M15-G4).
  Synthetic indicator values are Tier 3 per DATA_STANDARDS.md §Confidence Tier.
"""
from __future__ import annotations

import os
import pathlib
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Any

import httpx
import pytest
import pytest_asyncio

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

_DATABASE_URL = os.environ.get("DATABASE_URL", "")


def _require_db() -> None:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping M16-G3 integration test")


pytestmark = pytest.mark.integration

# ---------------------------------------------------------------------------
# Payload helpers
# ---------------------------------------------------------------------------

_SYNTHETIC_SEN_ATTRIBUTES: dict[str, Any] = {
    "SEN": {
        "poverty_headcount_ratio": {
            "value": "0.38",
            "unit": "ratio",
            "variable_type": "ratio",
            "measurement_framework": "human_development",
            "confidence_tier": 3,
            "is_synthetic": True,
            "synthetic_basis": (
                "Estimated from West African regional distribution "
                "(SSA T3 synthetic — World Bank PovcalNet regional aggregate 2022). "
                "Tier 3 per DATA_STANDARDS.md §Confidence Tier System."
            ),
        },
        "reserve_coverage_months": {
            "value": "2.8",
            "unit": "months",
            "variable_type": "stock",
            "measurement_framework": "financial",
            "confidence_tier": 3,
            "is_synthetic": True,
            "synthetic_basis": (
                "Estimated from IMF WEO Sub-Saharan Africa regional data 2022. "
                "Tier 3 per DATA_STANDARDS.md §Confidence Tier System."
            ),
        },
    }
}


def _sen_100_step_payload() -> dict[str, Any]:
    """SEN scenario for 100-step quarterly projection.

    Uses n_steps=8 (programme length) with projection_steps=100 to extend the
    horizon per CE Assessment Decision 2. timestep_label=quarterly per the Demo 6
    intent (100 quarterly steps = 25 years).

    Fires gdp_growth_change at step 1 to activate the DemographicModule elasticity path
    and produce poverty_headcount_ratio deltas for the bounds test.

    Synthetic SEN fixture per CE Assessment Decision 3 — not ZMB values transposed.
    """
    return {
        "name": "M16-G3 test — SEN 100-step 25-year projection",
        "configuration": {
            "entities": ["SEN"],
            "n_steps": 8,
            "projection_steps": 100,
            "timestep_label": "quarterly",
            "start_date": "2024-01-01",
            "initial_attributes": _SYNTHETIC_SEN_ATTRIBUTES,
            "modules_config": {
                "ecological": {"enabled": False},
                "political_economy": {"enabled": False},
            },
        },
        "scheduled_inputs": [
            {
                "step": 1,
                "input_type": "gdp_growth_change",
                "input_data": {"magnitude": "-0.04"},
            }
        ],
    }


def _zmb_default_payload() -> dict[str, Any]:
    """ZMB 8-step scenario without projection_steps — non-regression (AC-4, AC-7)."""
    return {
        "name": "M16-G3 test — ZMB 8-step non-regression",
        "configuration": {
            "entities": ["ZMB"],
            "n_steps": 8,
            "timestep_label": "annual",
        },
        "scheduled_inputs": [],
    }


# ---------------------------------------------------------------------------
# Module-level async client fixture for AC-6 and AC-7 integration tests
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    _require_db()
    from app.main import app

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
        timeout=120.0,
    ) as ac:
        yield ac


# ---------------------------------------------------------------------------
# AC-1 — ScenarioConfigSchema accepts projection_steps field (no DB)
# ---------------------------------------------------------------------------


class TestAC1ProjectionStepsFieldAccepted:
    """AC-1: ScenarioConfigSchema must accept an optional projection_steps field.

    CE Assessment Decision 2: 'Add projection_steps: int | None to SimulationRequest.
    Default None → programme-length behaviour unchanged.'
    """

    def test_projection_steps_100_accepted(self) -> None:
        from pydantic import ValidationError

        try:
            from app.schemas import ScenarioConfigSchema
        except ImportError:
            pytest.fail("app.schemas.ScenarioConfigSchema could not be imported.")

        try:
            config = ScenarioConfigSchema(
                entities=["SEN"],
                n_steps=8,
                projection_steps=100,
                timestep_label="quarterly",
            )
        except (ValidationError, TypeError) as exc:
            pytest.fail(
                f"ScenarioConfigSchema rejected projection_steps=100: {exc}\n"
                "AC-1: projection_steps must be a valid optional field (CE Assessment Decision 2)."
            )
        assert config.projection_steps == 100

    def test_projection_steps_defaults_to_none(self) -> None:
        try:
            from app.schemas import ScenarioConfigSchema
        except ImportError:
            pytest.fail("app.schemas.ScenarioConfigSchema could not be imported.")
        from pydantic import ValidationError

        try:
            config = ScenarioConfigSchema(entities=["ZMB"], n_steps=8, timestep_label="annual")
        except (ValidationError, TypeError) as exc:
            pytest.fail(
                f"ScenarioConfigSchema rejected payload without projection_steps: {exc}\n"
                "Non-regression: projection_steps must be optional."
            )
        assert getattr(config, "projection_steps", "ABSENT") is None, (
            "projection_steps must default to None when absent. "
            "CE Assessment Decision 2: 'default None → programme-length behaviour unchanged.'"
        )


# ---------------------------------------------------------------------------
# AC-2 — projection_steps=0 → ValidationError (no DB)
# ---------------------------------------------------------------------------


class TestAC2ProjectionStepsLowerBound:
    """AC-2: projection_steps=0 must be rejected. Valid range: 1–100."""

    def test_projection_steps_zero_rejected(self) -> None:
        try:
            from app.schemas import ScenarioConfigSchema
        except ImportError:
            pytest.fail("app.schemas.ScenarioConfigSchema could not be imported.")
        from pydantic import ValidationError

        with pytest.raises(ValidationError, match=r"projection_steps"):
            ScenarioConfigSchema(
                entities=["SEN"], n_steps=8, projection_steps=0, timestep_label="quarterly"
            )

    def test_projection_steps_negative_rejected(self) -> None:
        try:
            from app.schemas import ScenarioConfigSchema
        except ImportError:
            pytest.fail("app.schemas.ScenarioConfigSchema could not be imported.")
        from pydantic import ValidationError

        with pytest.raises(ValidationError, match=r"projection_steps"):
            ScenarioConfigSchema(
                entities=["SEN"], n_steps=8, projection_steps=-1, timestep_label="quarterly"
            )


# ---------------------------------------------------------------------------
# AC-3 — projection_steps=101 → ValidationError (no DB)
# ---------------------------------------------------------------------------


class TestAC3ProjectionStepsUpperBound:
    """AC-3: projection_steps > 100 must be rejected. Valid range: 1–100."""

    def test_projection_steps_101_rejected(self) -> None:
        try:
            from app.schemas import ScenarioConfigSchema
        except ImportError:
            pytest.fail("app.schemas.ScenarioConfigSchema could not be imported.")
        from pydantic import ValidationError

        with pytest.raises(ValidationError, match=r"projection_steps"):
            ScenarioConfigSchema(
                entities=["SEN"], n_steps=8, projection_steps=101, timestep_label="quarterly"
            )

    def test_projection_steps_max_boundary_accepted(self) -> None:
        try:
            from app.schemas import ScenarioConfigSchema
        except ImportError:
            pytest.fail("app.schemas.ScenarioConfigSchema could not be imported.")
        from pydantic import ValidationError

        try:
            config = ScenarioConfigSchema(
                entities=["SEN"], n_steps=8, projection_steps=100, timestep_label="quarterly"
            )
        except (ValidationError, TypeError) as exc:
            pytest.fail(f"projection_steps=100 (max boundary) rejected: {exc}")
        assert config.projection_steps == 100

    def test_projection_steps_min_boundary_accepted(self) -> None:
        try:
            from app.schemas import ScenarioConfigSchema
        except ImportError:
            pytest.fail("app.schemas.ScenarioConfigSchema could not be imported.")
        from pydantic import ValidationError

        try:
            config = ScenarioConfigSchema(
                entities=["SEN"], n_steps=8, projection_steps=1, timestep_label="quarterly"
            )
        except (ValidationError, TypeError) as exc:
            pytest.fail(f"projection_steps=1 (min boundary) rejected: {exc}")
        assert config.projection_steps == 1


# ---------------------------------------------------------------------------
# AC-4 — Non-regression: projection_steps absent → n_steps governs (no DB)
# ---------------------------------------------------------------------------


class TestAC4NonRegression:
    """AC-4: When projection_steps is absent, existing schema behaviour is unchanged."""

    def test_existing_payload_shape_unchanged(self) -> None:
        try:
            from app.schemas import ScenarioConfigSchema
        except ImportError:
            pytest.fail("app.schemas.ScenarioConfigSchema could not be imported.")
        from pydantic import ValidationError

        try:
            config = ScenarioConfigSchema(entities=["ZMB"], n_steps=8, timestep_label="annual")
        except (ValidationError, TypeError) as exc:
            pytest.fail(
                f"Existing ZMB 8-step payload rejected after G3 schema change: {exc}\n"
                "Non-regression: existing payloads must work without projection_steps."
            )
        assert config.n_steps == 8
        assert getattr(config, "projection_steps", None) is None


# ---------------------------------------------------------------------------
# AC-5 — adaptive_resolution=False applied when projection_steps > 8 (unit)
# ---------------------------------------------------------------------------


class TestAC5AdaptiveResolutionOverride:
    """AC-5: WebScenarioRunner must reference adaptive_resolution explicitly.

    CE Assessment Decision 1: 'The simulation engine must accept an
    adaptive_resolution: false flag when projection_steps > 8. This flag must
    be an explicit parameter, not inferred via a constant.'

    Behavioral verification (wall-time) is confirmed by the CE Assessment Decision 4
    dry-run at Step 4 Verify. CI cannot enforce a 60-second ceiling reliably on shared
    runners; the dry-run on target hardware is the binding gate.
    """

    def test_adaptive_resolution_flag_present_in_runner_source(self) -> None:
        """WebScenarioRunner source must reference 'adaptive_resolution'."""
        import inspect

        try:
            from app.simulation.web_scenario_runner import WebScenarioRunner
        except ImportError:
            pytest.fail(
                "app.simulation.web_scenario_runner.WebScenarioRunner could not be imported."
            )
        source = inspect.getsource(WebScenarioRunner)
        assert "adaptive_resolution" in source, (
            "WebScenarioRunner source code must reference 'adaptive_resolution'. "
            "CE Assessment Decision 1: the flag must be explicit — not a silent constant."
        )

    def test_web_scenario_runner_is_callable(self) -> None:
        try:
            from app.simulation.web_scenario_runner import WebScenarioRunner
        except ImportError:
            pytest.fail("WebScenarioRunner could not be imported.")
        assert callable(WebScenarioRunner)


# ---------------------------------------------------------------------------
# AC-6 — Indicator bounds: poverty_headcount_ratio ∈ [0.0, 1.0] (DB)
# ---------------------------------------------------------------------------


class TestAC6IndicatorBounds:
    """AC-6: poverty_headcount_ratio must remain in [0.0, 1.0] across all 100 steps.

    CM review finding (2026-06-23): the DemographicModule does not clamp internally;
    the entity attribute store must clamp VariableType.RATIO values. This test
    catches any unbounded decay function (silent failure 2 in the intent document).

    CE Assessment Decision 4: wall time and indicator bounds confirmed in Step 4 Verify
    dry-run on 4-core hardware. This test confirms the bounds condition in CI.
    """

    async def test_100_step_run_steps_executed(self, client: httpx.AsyncClient) -> None:
        payload = _sen_100_step_payload()
        create_res = await client.post("/api/v1/scenarios", json=payload)
        assert create_res.status_code == 201, (
            f"POST /scenarios with projection_steps=100 returned {create_res.status_code}. "
            f"Body: {create_res.text[:500]}"
        )
        scenario_id = create_res.json()["scenario_id"]

        run_res = await client.post(f"/api/v1/scenarios/{scenario_id}/run")
        assert run_res.status_code == 200, (
            f"Run returned {run_res.status_code}. Body: {run_res.text[:500]}"
        )
        assert run_res.json()["steps_executed"] == 100, (
            f"steps_executed was {run_res.json()['steps_executed']}, expected 100. "
            "SF-1: if projection_steps is silently capped, steps_executed equals n_steps (8)."
        )

    async def test_poverty_headcount_ratio_bounded_across_100_steps(
        self, client: httpx.AsyncClient
    ) -> None:
        """poverty_headcount_ratio ∈ [0.0, 1.0] at all 100 steps.

        The gdp_growth_change at step 1 triggers the elasticity path — without a
        triggering event, the indicator never changes and the bounds check would be trivial.
        """
        payload = _sen_100_step_payload()
        create_res = await client.post("/api/v1/scenarios", json=payload)
        assert create_res.status_code == 201
        scenario_id = create_res.json()["scenario_id"]

        await client.post(f"/api/v1/scenarios/{scenario_id}/run")

        snapshots_res = await client.get(f"/api/v1/scenarios/{scenario_id}/snapshots")
        assert snapshots_res.status_code == 200
        snapshots = snapshots_res.json()
        assert len(snapshots) == 100, (
            f"Expected 100 snapshots, got {len(snapshots)}."
        )

        out_of_bounds: list[dict[str, Any]] = []
        for snap in snapshots:
            step_index = snap.get("step_index", "unknown")
            for cohort_id, cohort_attrs in snap.get("attributes", {}).items():
                if "poverty_headcount_ratio" not in cohort_attrs:
                    continue
                raw = cohort_attrs["poverty_headcount_ratio"]
                value_str = raw.get("value") if isinstance(raw, dict) else str(raw)
                try:
                    value = Decimal(str(value_str))
                except Exception:  # noqa: BLE001
                    out_of_bounds.append({
                        "step": step_index, "cohort": cohort_id,
                        "value": value_str, "reason": "unparseable",
                    })
                    continue
                if value < Decimal("0.0") or value > Decimal("1.0"):
                    out_of_bounds.append({
                        "step": step_index, "cohort": cohort_id,
                        "value": str(value), "reason": "outside [0.0, 1.0]",
                    })

        assert not out_of_bounds, (
            f"poverty_headcount_ratio outside [0.0, 1.0] at {len(out_of_bounds)} step(s): "
            f"{out_of_bounds[:5]}\n"
            "CE Assessment Decision 4: any value outside [0.0, 1.0] → Step 4 Verify FAIL. "
            "Silent failure 2: unbounded DemographicModule decay function."
        )


# ---------------------------------------------------------------------------
# AC-7 — Trajectory endpoint: 100 steps + quarterly resolution (DB)
# ---------------------------------------------------------------------------


class TestAC7TrajectoryStepCountAndResolution:
    """AC-7: Trajectory endpoint must return exactly 100 step objects with
    effective_from dates spaced by 3 months (quarterly resolution).

    Observable application state §3.1 (intent document):
      1. Trajectory contains exactly 100 step objects.
      2. All steps have effective_from dates spaced by exactly 3 months
         — CE Assessment Decision 1 (adaptive resolution override) is active.

    Non-regression: ZMB 8-step trajectory is unchanged.
    """

    async def test_trajectory_returns_100_steps(self, client: httpx.AsyncClient) -> None:
        payload = _sen_100_step_payload()
        create_res = await client.post("/api/v1/scenarios", json=payload)
        assert create_res.status_code == 201
        scenario_id = create_res.json()["scenario_id"]

        run_res = await client.post(f"/api/v1/scenarios/{scenario_id}/run")
        assert run_res.status_code == 200

        trajectory_res = await client.get(
            f"/api/v1/scenarios/{scenario_id}/trajectory", params={"entity_id": "SEN"}
        )
        assert trajectory_res.status_code == 200, (
            f"GET /trajectory returned {trajectory_res.status_code}"
        )
        trajectory = trajectory_res.json()
        assert trajectory.get("step_count") == 100, (
            f"step_count was {trajectory.get('step_count')!r}, expected 100. "
            "SF-1: if projection_steps is silently ignored, step_count equals n_steps (8)."
        )
        assert len(trajectory.get("steps", [])) == 100, (
            "steps array length must equal step_count (100)."
        )

    async def test_trajectory_steps_quarterly_spacing(self, client: httpx.AsyncClient) -> None:
        """effective_from dates must be spaced by exactly 3 months (quarterly resolution).

        Observable state §3.1.2: 'All 100 steps have effective_from dates spaced by
        exactly 3 months — no sub-quarterly steps appear.'

        This catches silent failure 1: if adaptive_resolution was not overridden during a
        crisis event, daily steps would appear between quarterly steps.
        """
        payload = _sen_100_step_payload()
        create_res = await client.post("/api/v1/scenarios", json=payload)
        assert create_res.status_code == 201
        scenario_id = create_res.json()["scenario_id"]

        run_res = await client.post(f"/api/v1/scenarios/{scenario_id}/run")
        assert run_res.status_code == 200

        trajectory_res = await client.get(
            f"/api/v1/scenarios/{scenario_id}/trajectory", params={"entity_id": "SEN"}
        )
        assert trajectory_res.status_code == 200
        steps = trajectory_res.json().get("steps", [])
        if len(steps) < 2:
            # Can't verify spacing with fewer than 2 steps — caught by step-count test above.
            return

        spacing_violations: list[str] = []
        for i in range(1, len(steps)):
            prev_from = steps[i - 1].get("effective_from", "")
            curr_from = steps[i].get("effective_from", "")
            if not prev_from or not curr_from:
                continue
            try:
                prev_date = date.fromisoformat(prev_from[:10])
                curr_date = date.fromisoformat(curr_from[:10])
            except ValueError:
                continue
            # Quarterly spacing: same day-of-month, 3 months apart.
            expected_month = (prev_date.month - 1 + 3) % 12 + 1
            expected_year = prev_date.year + ((prev_date.month - 1 + 3) // 12)
            if curr_date.month != expected_month or curr_date.year != expected_year:
                spacing_violations.append(
                    f"Step {i}: {prev_from} → {curr_from} is not a 3-month interval"
                )

        assert not spacing_violations, (
            f"{len(spacing_violations)} non-quarterly interval(s) detected in trajectory: "
            f"{spacing_violations[:5]}\n"
            "CE Assessment Decision 1: adaptive_resolution=False must prevent daily-resolution "
            "steps from appearing in the 100-step trajectory. "
            "Silent failure 1: adaptive resolution not overridden produces sub-quarterly steps."
        )

    async def test_trajectory_non_regression_zmb_8_step(self, client: httpx.AsyncClient) -> None:
        """ADR-017 non-regression: ZMB 8-step trajectory unchanged after G3."""
        payload = _zmb_default_payload()
        create_res = await client.post("/api/v1/scenarios", json=payload)
        assert create_res.status_code == 201
        scenario_id = create_res.json()["scenario_id"]

        run_res = await client.post(f"/api/v1/scenarios/{scenario_id}/run")
        assert run_res.status_code == 200
        zmb_steps = run_res.json()["steps_executed"]
        assert zmb_steps == 8, (
            f"ZMB 8-step non-regression: steps_executed was {zmb_steps}, expected 8."
        )

        trajectory_res = await client.get(
            f"/api/v1/scenarios/{scenario_id}/trajectory", params={"entity_id": "ZMB"}
        )
        assert trajectory_res.status_code == 200
        assert trajectory_res.json().get("step_count") == 8, (
            "ZMB trajectory step_count must remain 8 after G3 (ADR-017 non-regression)."
        )


# ---------------------------------------------------------------------------
# AC-8 — api_contracts.yml documents projection_steps (filesystem, no DB)
# ---------------------------------------------------------------------------

_REPO_ROOT = pathlib.Path(__file__).parent.parent.parent
_API_CONTRACTS = _REPO_ROOT / "docs" / "schema" / "api_contracts.yml"


class TestAC8ApiContractsYamlUpdated:
    """AC-8: docs/schema/api_contracts.yml must document projection_steps.

    Schema drift rule (CLAUDE.md §Schema registry): api_contracts.yml updated
    in the same commit as the backend implementation.
    """

    def test_api_contracts_file_exists(self) -> None:
        assert _API_CONTRACTS.exists(), (
            f"docs/schema/api_contracts.yml not found at {_API_CONTRACTS}."
        )

    def test_projection_steps_documented(self) -> None:
        text = _API_CONTRACTS.read_text(encoding="utf-8")
        assert "projection_steps" in text, (
            "docs/schema/api_contracts.yml does not contain 'projection_steps'. "
            "Schema drift rule: api_contracts.yml must be updated in the same commit "
            "as the implementation."
        )

    def test_projection_steps_near_post_scenarios(self) -> None:
        """projection_steps must appear in the POST /scenarios endpoint context."""
        text = _API_CONTRACTS.read_text(encoding="utf-8")
        if "projection_steps" not in text:
            pytest.fail("projection_steps not found in api_contracts.yml.")

        lines = text.splitlines()
        proj_lines = [i for i, ln in enumerate(lines) if "projection_steps" in ln]
        post_lines = [
            i for i, ln in enumerate(lines)
            if "POST" in ln and "/scenarios" in ln and "scenario_id" not in ln
        ]
        if not post_lines:
            pytest.fail("POST /scenarios entry not found in api_contracts.yml.")

        nearest_post = min(post_lines, key=lambda pl: min(abs(pl - ql) for ql in proj_lines))
        min_distance = min(abs(nearest_post - ql) for ql in proj_lines)
        assert min_distance <= 80, (
            f"projection_steps appears {min_distance} lines from POST /scenarios. "
            "Must be within the endpoint body schema definition."
        )
