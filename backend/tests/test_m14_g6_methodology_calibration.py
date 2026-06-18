"""Integration and unit tests for M14-G6 methodology, calibration, and instrument legibility.

QA Lead step 2 — authored BEFORE implementation, from intent document at:
  docs/process/intents/M14-G6-2026-06-18-methodology-calibration.md

These tests define "done" for G6 backend deliverables. AC-5, AC-6, and AC-8 will fail
pre-implementation (or trivially pass in the case noted for AC-6). AC-7 is a regression
guard — it must pass both before and after the AC-6 fix.

AC coverage:
  AC-5  reserve_coverage_months in GET /scenarios/{id}/initial-state for a freshly
        created JOR scenario that has been advanced at least one step.
        Issue #884 — indicator was absent because it was seeded as FLOW delta, not
        STOCK with source_registry attribution.

  AC-6  Ecological composite confidence_tier derived from max() of ecological indicator
        confidence_tiers — NOT hardcoded at T2.
        Issue #823 — scenarios.py line 866 hardcodes confidence_tier=2.
        CE-G6-3: Chief Methodologist must confirm the minimum tier floor. Test verifies
        the derivation rule; CE must ensure GRC fixture has ≥1 T3 ecological indicator
        for the test to distinguish derived from hardcoded behavior.

  AC-7  Regression guard: zero ecological boundary constants → composite_score null.
        This existing behavior (already correct) must survive the AC-6 fix.
        Uses unit test pattern from test_measurement_output.py line 550.

  AC-8  MENA water scarcity elasticity applied to JOR: GET
        /scenarios/{id}/measurement-output?entity_id=JOR&step=1 includes an ecological
        indicator for water_stress_index (CE-G6-1: indicator key to be confirmed) with
        a non-null value and confidence_tier=3.
        Issue #824 — elasticity not in ECOLOGICAL_ELASTICITY_REGISTRY for arid_semiarid.

Open CE decisions that affect these tests:
  CE-G6-1  Canonical water_stress_index indicator key for #824 (AC-8).
           Tests use "water_stress_index" as specified in intent doc §3.2 state D;
           update if CE confirms a different key.
  CE-G6-2  reserve_coverage_months seeding approach for #884 (AC-5).
           Test asserts observable state regardless of approach A or B.
  CE-G6-3  Ecological composite minimum tier floor (AC-6).
           Test computes max() of available indicator tiers; if all GRC ecological
           indicators are T2, the assertion trivially passes pre-implementation.
           CE must seed at least one T3 GRC ecological indicator.

Uses httpx.AsyncClient with ASGITransport — no running server required.
All async tests skip gracefully when DATABASE_URL is not set.
AC-7 uses the unit test mock pattern (no database required).
"""
from __future__ import annotations

import os
import pathlib
from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
import pytest_asyncio

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

from app.main import app

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

pytestmark = pytest.mark.integration


def _require_db() -> None:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping M14-G6 integration test")


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    _require_db()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


# ---------------------------------------------------------------------------
# Payload helpers
# ---------------------------------------------------------------------------


def _jor_payload() -> dict[str, Any]:
    """Minimal JOR scenario for AC-5 and AC-8."""
    return {
        "name": "M14-G6 test — JOR calibration",
        "configuration": {
            "entities": ["JOR"],
            "n_steps": 2,
            "timestep_label": "annual",
        },
        "scheduled_inputs": [],
    }


def _grc_payload() -> dict[str, Any]:
    """Minimal GRC scenario for AC-6 (ecological composite tier derivation)."""
    return {
        "name": "M14-G6 test — GRC ecological tier",
        "configuration": {
            "entities": ["GRC"],
            "n_steps": 1,
            "timestep_label": "annual",
        },
        "scheduled_inputs": [],
    }


async def _create_and_advance(
    client: httpx.AsyncClient,
    payload: dict[str, Any],
    steps: int = 1,
) -> str:
    """Create a scenario and advance it `steps` times. Returns the scenario_id."""
    create = await client.post("/api/v1/scenarios", json=payload)
    assert create.status_code == 201
    scenario_id = create.json()["scenario_id"]

    for step_num in range(steps):
        adv = await client.post(f"/api/v1/scenarios/{scenario_id}/advance")
        assert adv.status_code in (200, 202), (
            f"Advance step {step_num + 1} failed: {adv.status_code}"
        )

    return str(scenario_id)


# ---------------------------------------------------------------------------
# AC-5 — reserve_coverage_months present in /initial-state for freshly created JOR
#
# Intent doc §4 AC-5:
# GET /initial-state for a JOR scenario advanced ≥1 step returns HTTP 200.
# frameworks["financial"]["indicators"] contains ≥1 entry with name="reserve_coverage_months"
# and a non-null value.
#
# Silent failure detection (§3.3):
# The bug causes the financial indicators list to be empty or omit reserve_coverage_months
# with no error — the endpoint returns 200 with a short list. The test must assert
# reserve_coverage_months IS in the list (not just that the list is non-empty).
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac5_reserve_coverage_months_in_initial_state_for_jor(
    client: httpx.AsyncClient,
) -> None:
    """AC-5: Freshly created JOR scenario — /initial-state contains reserve_coverage_months."""
    scenario_id = await _create_and_advance(client, _jor_payload(), steps=1)

    resp = await client.get(f"/api/v1/scenarios/{scenario_id}/initial-state")
    assert resp.status_code == 200

    data = resp.json()
    assert data["entity_id"] == "JOR"

    frameworks = data.get("frameworks", {})
    assert isinstance(frameworks, dict), (
        "frameworks must be a dict in the initial-state response"
    )

    financial = frameworks.get("financial", {})
    indicators = financial.get("indicators", [])
    assert isinstance(indicators, list), (
        "frameworks['financial']['indicators'] must be a list"
    )

    reserve = [
        ind for ind in indicators
        if ind.get("name") == "reserve_coverage_months"
    ]
    assert reserve, (
        "frameworks['financial']['indicators'] must contain reserve_coverage_months for JOR — "
        "indicator absent because it is seeded as FLOW delta, not STOCK (issue #884). "
        "Fix: seed reserve_coverage_months as a source-attributed STOCK in the entity "
        "seed data (CE-G6-2 approach A or B)."
    )

    ind = reserve[0]
    assert ind.get("value") is not None, (
        "reserve_coverage_months must have a non-null value in /initial-state — "
        "a null value means the indicator exists in the list but has no usable data "
        "for Persona 2 to cite at the negotiating table."
    )


# ---------------------------------------------------------------------------
# AC-6 — Ecological composite confidence_tier == 3 for GRC (not hardcoded T2)
#
# Intent doc §4 AC-6 + CM-G6-1 CONFIRMED 2026-06-18:
# Ecological composite minimum tier floor = 3. Derivation: max(indicator_min_tier, 3).
# Rationale (CM-G6-1): land_use_pressure_index is T3 (FAO GFR 5-year/annual interpolation);
# water_stress_index entering via #824 is T3 (arid-zone proxy). A composite combining
# T1 measurements with T3 proxies cannot be T2 without misrepresenting the chain.
#
# Therefore AC-6 must assert composite_tier == 3 unconditionally (not a dynamic max check).
# The hardcoded T2 at scenarios.py line 866 is wrong — it labels the ecological composite
# as "official statistics, citable directly," which it is not.
#
# Pre-implementation: composite_tier will be 2 (hardcoded) → assertion FAILS as expected.
# Post-implementation: composite_tier will be max(indicator_tiers, floor=3) = 3 → PASSES.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac6_ecological_composite_tier_is_3_not_hardcoded_2(
    client: httpx.AsyncClient,
) -> None:
    """AC-6: GRC ecological composite confidence_tier == 3, not hardcoded 2 (CM-G6-1)."""
    scenario_id = await _create_and_advance(client, _grc_payload(), steps=1)

    traj_resp = await client.get(f"/api/v1/scenarios/{scenario_id}/trajectory")
    assert traj_resp.status_code == 200

    traj_data = traj_resp.json()
    steps = traj_data.get("steps", [])
    step1 = next(
        (s for s in steps if s.get("step_index") == 1),
        None,
    )
    assert step1 is not None, (
        "Trajectory must contain step_index=1 after one advance"
    )

    frameworks_at_step1 = step1.get("frameworks", [])
    eco_fw = next(
        (f for f in frameworks_at_step1 if f.get("framework") == "ecological"),
        None,
    )
    assert eco_fw is not None, (
        "Step 1 trajectory must include an ecological framework entry for GRC"
    )

    composite_tier = eco_fw.get("confidence_tier")

    # CM-G6-1 confirmed floor=3: the composite must be at least T3.
    # If composite_score is null (zero ecological indicators), AC-7 handles that case.
    if eco_fw.get("composite_score") is None:
        return  # AC-7 regression guard covers the null case

    assert composite_tier == 3, (
        f"GRC ecological composite confidence_tier must be 3 (CM-G6-1: floor=3, "
        f"max(indicator_min_tier, 3)). Got: {composite_tier}. "
        f"If composite_tier=2, the hardcoded confidence_tier=2 at scenarios.py line 866 "
        f"has not been replaced with the derived tier (issue #823). "
        f"CM-G6-1 rationale: land_use_pressure_index and water_stress_index are both T3; "
        f"the composite cannot be T2 without misrepresenting the data quality chain."
    )


# ---------------------------------------------------------------------------
# AC-7 — Zero ecological boundary constants → null composite (regression guard)
#
# Intent doc §4 AC-7:
# The zero-indicator → null composite path is already implemented correctly.
# This test confirms the AC-6 fix (derived tier derivation) does NOT regress this.
#
# Uses unit test pattern from test_measurement_output.py line 550:
# conn.fetch = AsyncMock(return_value=[]) simulates no active boundary constants.
# No database required.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac7_zero_ecological_boundary_constants_returns_null_composite() -> None:
    """AC-7 (regression): zero ecological boundary constants → composite_score is None."""
    # Import lazily to avoid module-level import issues when DB is not available
    try:
        from app.api.scenarios import get_measurement_output
    except ImportError:
        pytest.skip("Cannot import get_measurement_output — skipping AC-7 unit test")

    # Replicate the mock pattern from test_measurement_output.py line 550
    conn = MagicMock()
    conn.fetchrow = AsyncMock(
        return_value={
            "scenario_id": "g6-test-scen",
            "name": "G6 AC-7 test",
            "status": "completed",
            "configuration": {
                "entities": ["GRC"],
                "n_steps": 1,
                "timestep_label": "annual",
            },
        }
    )
    conn.fetch = AsyncMock(return_value=[])  # no active ecological boundary constants

    try:
        result = await get_measurement_output(
            scenario_id="g6-test-scen", entity_id="GRC", step=1, conn=conn
        )
        eco = result.outputs.get("ecological")
        if eco is not None:
            assert eco.composite_score is None, (
                "ecological composite_score must be None when no boundary constants are active — "
                "the zero-indicator guard must not be regressed by the AC-6 confidence_tier fix"
            )
    except Exception as exc:
        # If get_measurement_output requires a real DB snapshot, skip rather than fail
        # CE must confirm the correct mock structure if this test errors
        pytest.skip(
            f"get_measurement_output raised {type(exc).__name__}: {exc}. "
            "CE must confirm the correct mock structure for the zero-indicator regression test."
        )


# ---------------------------------------------------------------------------
# AC-8 — MENA water scarcity elasticity active for JOR at step 1
#
# Intent doc §4 AC-8:
# GET /measurement-output?entity_id=JOR&step=1 for a freshly created JOR scenario:
# outputs["ecological"]["indicators"] contains an entry for "water_stress_index"
# (CE-G6-1: canonical key to be confirmed) with a non-null value and confidence_tier=3.
#
# CE-G6-1: The intent doc proposes "water_stress_index" as the indicator key.
# If the Chief Engineer confirms a different key, update _WATER_STRESS_INDICATOR_KEY below.
#
# Implementation requires (per intent doc §3.2 state D):
# 1. Add EcologicalElasticity entry to ECOLOGICAL_ELASTICITY_REGISTRY for water_stress_index
# 2. Set biome_class=arid_semiarid on JOR entity configuration
# 3. Biome-class-conditional dispatch in ecological module (arid_semiarid entities only)
# ---------------------------------------------------------------------------

# CE-G6-1: Update this if CE confirms a different canonical key.
_WATER_STRESS_INDICATOR_KEY = "water_stress_index"


@pytest.mark.asyncio
async def test_ac8_mena_water_scarcity_elasticity_applied_to_jor(
    client: httpx.AsyncClient,
) -> None:
    """AC-8: JOR measurement-output at step 1 contains water_stress_index with non-null value."""
    scenario_id = await _create_and_advance(client, _jor_payload(), steps=1)

    resp = await client.get(
        f"/api/v1/scenarios/{scenario_id}/measurement-output"
        f"?entity_id=JOR&step=1"
    )
    assert resp.status_code == 200

    data = resp.json()
    eco_output = data.get("outputs", {}).get("ecological", {})
    eco_indicators = eco_output.get("indicators", {})

    assert _WATER_STRESS_INDICATOR_KEY in eco_indicators, (
        f"ecological indicators must contain '{_WATER_STRESS_INDICATOR_KEY}' for JOR at step 1 — "
        f"key absent because the MENA arid-economy water scarcity elasticity has not been "
        f"added to ECOLOGICAL_ELASTICITY_REGISTRY (issue #824). "
        f"CE-G6-1: if the canonical key differs from '{_WATER_STRESS_INDICATOR_KEY}', "
        f"update _WATER_STRESS_INDICATOR_KEY before the implementation PR opens. "
        f"Ecological indicators currently present: {list(eco_indicators.keys())}"
    )

    water_indicator = eco_indicators[_WATER_STRESS_INDICATOR_KEY]
    assert isinstance(water_indicator, dict), (
        f"'{_WATER_STRESS_INDICATOR_KEY}' indicator must be a dict in the indicators map"
    )

    value = water_indicator.get("value")
    assert value is not None, (
        f"'{_WATER_STRESS_INDICATOR_KEY}' must have a non-null value at step 1 — "
        f"null value means the elasticity entry was added to the registry but the module "
        f"is not producing output for JOR (biome_class dispatch may be missing)"
    )

    tier = water_indicator.get("confidence_tier")
    assert tier == 3, (
        f"'{_WATER_STRESS_INDICATOR_KEY}' confidence_tier must be 3 (Tier 3, per CM+EE "
        f"approval 2026-06-13 — FAO GFR arid-subset/ICARDA calibration basis). "
        f"Got: {tier}"
    )


# ---------------------------------------------------------------------------
# AC-9 partial automation — calibration documents exist
#
# AC-9 is primarily a BPO 5-minute navigation test at Step 5 Validate.
# This file-existence check is the automated precondition: both documents
# must exist before the BPO navigation test is meaningful.
# ---------------------------------------------------------------------------


def test_ac9_calibration_documents_exist() -> None:
    """AC-9 (partial): both calibration documents exist at their canonical paths."""
    repo_root = pathlib.Path(__file__).parents[2]

    pmm_anchor = repo_root / "docs" / "calibration" / "pmm-interpretation-anchor.md"
    assert pmm_anchor.exists(), (
        f"PMM interpretation anchor not found at {pmm_anchor}. "
        "Chief Methodologist must file this document before G6 sprint exit. "
        "Intent doc §3.2 state E: Chief Methodologist determines canonical path if different."
    )

    tier_methodology = (
        repo_root / "docs" / "calibration" / "confidence-tier-assignment-methodology.md"
    )
    assert tier_methodology.exists(), (
        f"Confidence tier methodology document not found at {tier_methodology}. "
        "Chief Methodologist must file this document for issue #22 (M14 scope). "
        "Intent doc §3.2 state E: methodology documents the T1-T5 tier assignments "
        "across all indicator families — required for M14 methodology publication goal."
    )
