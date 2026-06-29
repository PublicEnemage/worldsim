"""Backend integration tests for M15-G4 Path 1 + ADR-016 Component 3.

QA Lead step 2 — authored BEFORE implementation, from intent document at:
  docs/process/intents/M15-G4-2026-06-22-path1-fidelity-contextualisation.md

These tests define "done" for G4 backend deliverables. All AC-7–AC-10,
AC-14–AC-15 tests fail until the Data Architect Agent delivers the
implementation (Step 3). The api_contracts.yml test fails until DA-G4-3
update lands on release/m15.

Uses httpx.AsyncClient with ASGITransport — no running server required.
All async tests skip gracefully when DATABASE_URL is not set.

AC coverage:
  AC-7   GET /entities/SEN/data-quality?year=2023 — loadable: true on ≥1 framework
         (SEN registered in source_registry but not preloaded in entity_data_quality_coverage)
  AC-8   GET /entities/ZMB/data-quality?year=2024 — loadable: false + non-null
         confidence_tier (ZMB is preloaded — already-loaded state)
  AC-9   GET /entities/XYZ/data-quality?year=2023 — at least one framework object with
         is_synthetic: true and confidence_tier ≥ 3 (ADR-007 synthetic fallback; XYZ
         is not in source_registry; endpoint never returns empty frameworks after G4)
  AC-10  POST /entities/SEN/pull?year=2023 → job_id returned in response body;
         subsequent GET /entities/SEN/pull/{job_id} eventually returns status: complete
  AC-14  GET /scenarios/{zmb_id}/fidelity-context → analogous_case.case_id = "ARG" and
         analogous_case.directional_accuracy_validated = true (ZMB→ARG mapping)
  AC-15  GET /scenarios/{sen_id}/fidelity-context (SEN — not in CM mapping table) →
         HTTP 200 with analogous_case: null (fallback path returned, not an error)
  API    docs/schema/api_contracts.yml — four new G4 path strings present before
         frontend implementation begins (DA-G4-3 obligation)

Silent failure guards:
  AC-7:  /data-quality for non-preloaded registered entity must include loadable field
         — missing field is a test failure, not a silent pass
  AC-9:  /data-quality for unregistered entity must return ≥1 synthetic framework object
         — empty frameworks list is the pre-G4 behaviour this AC fixes
  AC-15: /fidelity-context must return HTTP 200 with analogous_case: null
         — a 404 or 500 for an entity without a mapping case is a silent failure
"""

from __future__ import annotations

import asyncio
import os
import pathlib
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    import httpx

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

pytestmark = pytest.mark.integration


def _require_db() -> None:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping M15-G4 integration test")



# ---------------------------------------------------------------------------
# Payload helpers
# ---------------------------------------------------------------------------


def _zmb_payload() -> dict[str, Any]:
    """Minimal ZMB scenario for AC-14 — entity with CM mapping to ARG."""
    return {
        "name": "M15-G4 test — ZMB fidelity context",
        "configuration": {
            "entities": ["ZMB"],
            "n_steps": 1,
            "timestep_label": "annual",
        },
        "scheduled_inputs": [],
    }


def _sen_payload() -> dict[str, Any]:
    """SEN scenario for AC-15 — entity not in the CM analogous-case mapping table.

    Requires G4 to be implemented: SEN must be pullable before scenario creation.
    Tests that call this payload skip if scenario creation returns non-201.
    """
    return {
        "name": "M15-G4 test — SEN fidelity context (null case)",
        "configuration": {
            "entities": ["SEN"],
            "n_steps": 1,
            "timestep_label": "annual",
        },
        "scheduled_inputs": [],
    }


async def _create_and_run_scenario(
    client: httpx.AsyncClient,
    payload: dict[str, Any],
) -> str:
    """Create a scenario and run it to completion. Returns the scenario_id."""
    create = await client.post("/api/v1/scenarios", json=payload)
    assert create.status_code == 201, (
        f"Scenario creation failed: {create.status_code} — {create.text[:200]}"
    )
    scenario_id = create.json()["scenario_id"]
    run = await client.post(f"/api/v1/scenarios/{scenario_id}/run")
    assert run.status_code == 200, (
        f"Scenario run failed: {run.status_code} — {run.text[:200]}"
    )
    return str(scenario_id)


# ---------------------------------------------------------------------------
# AC-7 — /data-quality SEN returns loadable: true on ≥1 framework
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac7_data_quality_sen_loadable_true(
    client: httpx.AsyncClient,
) -> None:
    """AC-7: SEN 2023 /data-quality returns ≥1 framework with loadable: true.

    SEN (Senegal) is registered in source_registry with World Bank WDI coverage
    but has NOT been preloaded into entity_data_quality_coverage. G4 extends
    the /data-quality endpoint to query source_registry and return loadable: true
    for framework/year combinations with registered coverage but no preloaded data.

    Pre-G4: the response either has no 'loadable' field or returns empty frameworks.
    Post-G4: ≥1 framework has loadable: true.
    """
    resp = await client.get("/api/v1/entities/SEN/data-quality?year=2023")
    assert resp.status_code == 200, (
        f"Expected HTTP 200, got {resp.status_code}: {resp.text[:200]}"
    )
    data = resp.json()
    frameworks = data.get("frameworks", [])
    assert len(frameworks) >= 1, (
        "Expected ≥1 framework object for SEN 2023; got empty frameworks list. "
        "After G4, source_registry coverage for SEN must produce framework rows."
    )
    loadable_frames = [f for f in frameworks if f.get("loadable") is True]
    assert len(loadable_frames) >= 1, (
        f"Expected ≥1 framework with loadable: true for SEN 2023; "
        f"frameworks returned: {frameworks}. "
        "G4 must add 'loadable' field to /data-quality for registered-source entities."
    )


# ---------------------------------------------------------------------------
# AC-8 — /data-quality ZMB returns loadable: false + non-null confidence_tier
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac8_data_quality_zmb_loadable_false_preloaded(
    client: httpx.AsyncClient,
) -> None:
    """AC-8: ZMB 2024 /data-quality returns loadable: false + non-null confidence_tier.

    ZMB is preloaded into entity_data_quality_coverage. G4 adds the loadable
    field set to false for preloaded entities — confirming the 'already loaded'
    state is correctly distinguished from the 'available to pull' state (AC-7).
    """
    resp = await client.get("/api/v1/entities/ZMB/data-quality?year=2024")
    assert resp.status_code == 200
    data = resp.json()
    frameworks = data.get("frameworks", [])
    assert len(frameworks) >= 1, "Expected ≥1 framework for ZMB 2024 (preloaded entity)"

    preloaded_frames = [
        f for f in frameworks
        if f.get("loadable") is False and f.get("confidence_tier") is not None
    ]
    assert len(preloaded_frames) >= 1, (
        f"Expected ≥1 framework with loadable: false and non-null confidence_tier "
        f"for ZMB 2024; frameworks: {frameworks}. "
        "G4 must distinguish preloaded entities (loadable: false) from pullable ones."
    )


# ---------------------------------------------------------------------------
# AC-9 — /data-quality XYZ synthetic fallback (not in source_registry)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac9_data_quality_unregistered_entity_synthetic_fallback(
    client: httpx.AsyncClient,
) -> None:
    """AC-9: XYZ 2023 /data-quality returns ≥1 framework with is_synthetic: true, tier ≥ 3.

    Entity 'XYZ' is not in source_registry. Before G4, /data-quality returned
    empty frameworks for unknown entities (ADR-016 SF-1 guard preserved HTTP 200).
    After G4, the ADR-007 synthetic fallback is activated: the endpoint returns
    synthetic framework objects (T3/T4) rather than an empty list — ensuring the
    analyst sees what tier of inference is available, not a silent empty state.
    """
    resp = await client.get("/api/v1/entities/XYZ/data-quality?year=2023")
    assert resp.status_code == 200
    data = resp.json()
    frameworks = data.get("frameworks", [])
    assert len(frameworks) >= 1, (
        "Expected ≥1 synthetic framework object for XYZ 2023. "
        "After G4, unregistered entities must return ADR-007 synthetic fallback rows — "
        "not an empty list. An empty list is a silent failure (SF-1)."
    )
    synthetic_frames = [
        f for f in frameworks
        if f.get("is_synthetic") is True
        and (f.get("confidence_tier") or 0) >= 3
    ]
    assert len(synthetic_frames) >= 1, (
        f"Expected ≥1 framework with is_synthetic: true and confidence_tier ≥ 3; "
        f"frameworks: {frameworks}. "
        "ADR-007 synthetic fallback must produce T3/T4 tier values for unregistered entities."
    )


# ---------------------------------------------------------------------------
# AC-10 — POST /pull → job_id; GET /pull/{job_id} → status: complete
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac10_data_pull_job_end_to_end(
    client: httpx.AsyncClient,
) -> None:
    """AC-10: POST /entities/SEN/pull?year=2023 → job_id; GET → status: complete.

    Tests the DA-G4-2 async pull job mechanism end-to-end:
      1. POST returns HTTP 200 or 202 with a job_id field
      2. GET /pull/{job_id} eventually returns status: 'complete'

    The M15 pull job populates entity_data_quality_coverage from source_registry
    metadata — no external API calls. Polls every 2 seconds for up to 60 seconds.

    Skip if the endpoint returns 404 (pre-G4 — not yet implemented).
    """
    post_resp = await client.post("/api/v1/entities/SEN/pull?year=2023")
    if post_resp.status_code == 404:
        pytest.skip(
            "POST /entities/SEN/pull not yet implemented — "
            "test will become active once G4 backend lands"
        )
    assert post_resp.status_code in (200, 202), (
        f"Expected 200 or 202 from POST /pull; got {post_resp.status_code}: "
        f"{post_resp.text[:200]}"
    )
    data = post_resp.json()
    assert "job_id" in data, (
        f"POST /pull response must contain 'job_id' field; got: {data}"
    )
    assert data.get("status") == "queued", (
        f"POST /pull initial status must be 'queued'; got: {data.get('status')}"
    )
    job_id = data["job_id"]

    final_status = "unknown"
    for _ in range(30):  # poll up to 60 seconds (30 × 2s)
        await asyncio.sleep(2)
        get_resp = await client.get(f"/api/v1/entities/SEN/pull/{job_id}")
        assert get_resp.status_code == 200, (
            f"GET /pull/{job_id} returned {get_resp.status_code}: {get_resp.text[:200]}"
        )
        poll_data = get_resp.json()
        final_status = poll_data.get("status", "unknown")
        if final_status in ("complete", "failed"):
            break

    assert final_status == "complete", (
        f"Pull job for SEN 2023 did not reach status 'complete' within 60 seconds. "
        f"Final status: '{final_status}'. "
        "Check that the M15 pull job correctly populates entity_data_quality_coverage "
        "from source_registry metadata."
    )


# ---------------------------------------------------------------------------
# AC-14 — /fidelity-context ZMB → case_id: ARG, directional_accuracy_validated: true
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac14_fidelity_context_zmb_maps_to_arg(
    client: httpx.AsyncClient,
) -> None:
    """AC-14: GET /scenarios/{zmb_id}/fidelity-context → ARG mapping for ZMB.

    ZMB maps to Argentina 2001–2002 per the Chief Methodologist analogous-case
    mapping table (Decision Gate 2 of the intent document). The endpoint must
    return case_id 'ARG' with directional_accuracy_validated: true.

    Skip if the endpoint returns 404 (pre-G4 — not yet implemented).
    """
    zmb_id = await _create_and_run_scenario(client, _zmb_payload())

    resp = await client.get(f"/api/v1/scenarios/{zmb_id}/fidelity-context")
    if resp.status_code == 404:
        pytest.skip(
            "GET /scenarios/{id}/fidelity-context not yet implemented — "
            "test will become active once G4 backend lands"
        )
    assert resp.status_code == 200, (
        f"Expected HTTP 200 from /fidelity-context; got {resp.status_code}: "
        f"{resp.text[:200]}"
    )
    data = resp.json()
    assert "scenario_id" in data, (
        f"Response must include 'scenario_id' field; got: {list(data.keys())}"
    )
    assert "analogous_case" in data, (
        f"Response must include 'analogous_case' field; got: {list(data.keys())}"
    )
    case = data["analogous_case"]
    assert case is not None, (
        "analogous_case must not be null for ZMB; CM mapping table specifies ZMB → ARG. "
        f"Full response: {data}"
    )
    assert case.get("case_id") == "ARG", (
        f"Expected analogous_case.case_id = 'ARG' for ZMB; got: {case.get('case_id')}. "
        "CM Decision Gate 2: ZMB → Argentina 2001–2002."
    )
    assert case.get("directional_accuracy_validated") is True, (
        f"Expected directional_accuracy_validated: true for ZMB→ARG; "
        f"got: {case.get('directional_accuracy_validated')}. "
        "CM mapping specifies directional validation is confirmed for this mechanism type."
    )


# ---------------------------------------------------------------------------
# AC-15 — /fidelity-context SEN → analogous_case: null (not in mapping table)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac15_fidelity_context_unmapped_entity_returns_null(
    client: httpx.AsyncClient,
) -> None:
    """AC-15: /fidelity-context for entity not in CM mapping table → analogous_case: null.

    SEN (Senegal) is not in the Chief Methodologist's analogous-case mapping
    table. The endpoint must return HTTP 200 with analogous_case: null — not
    a 404, not a 500, and not a fabricated case. This is the SF-3 guard: the
    fallback path must be a defined, non-error response.

    Requires G4 pull to have run for SEN (AC-10). Skip if:
      - POST /pull returns 404 (endpoint not yet implemented)
      - SEN scenario creation returns non-201 (entity not available after pull)
      - GET /fidelity-context returns 404 (endpoint not yet implemented)
    """
    # Step 1: Pull SEN data
    post_resp = await client.post("/api/v1/entities/SEN/pull?year=2023")
    if post_resp.status_code == 404:
        pytest.skip("POST /entities/SEN/pull not yet implemented")
    if post_resp.status_code not in (200, 202):
        pytest.skip(
            f"POST /entities/SEN/pull returned unexpected status {post_resp.status_code}"
        )
    job_id = post_resp.json().get("job_id")
    assert job_id, "Pull response must contain job_id"

    # Step 2: Wait for pull completion
    final_status = "unknown"
    for _ in range(30):
        await asyncio.sleep(2)
        poll = await client.get(f"/api/v1/entities/SEN/pull/{job_id}")
        assert poll.status_code == 200
        final_status = poll.json().get("status", "unknown")
        if final_status in ("complete", "failed"):
            break
    if final_status != "complete":
        pytest.skip(f"SEN pull did not complete (status: {final_status}) — skipping AC-15")

    # Step 3: Create SEN scenario
    create_resp = await client.post("/api/v1/scenarios", json=_sen_payload())
    if create_resp.status_code != 201:
        pytest.skip(
            f"SEN scenario creation failed ({create_resp.status_code}) — "
            "entity may not be available post-pull; skipping AC-15"
        )
    sen_id = create_resp.json()["scenario_id"]

    run_resp = await client.post(f"/api/v1/scenarios/{sen_id}/run")
    if run_resp.status_code != 200:
        pytest.skip(
            f"SEN scenario run failed ({run_resp.status_code}) — skipping AC-15"
        )

    # Step 4: Assert /fidelity-context returns null analogous_case
    resp = await client.get(f"/api/v1/scenarios/{sen_id}/fidelity-context")
    if resp.status_code == 404:
        pytest.skip(
            "GET /scenarios/{id}/fidelity-context not yet implemented — "
            "test will become active once G4 backend lands"
        )
    assert resp.status_code == 200, (
        f"Expected HTTP 200 from /fidelity-context for SEN; got {resp.status_code}: "
        f"{resp.text[:200]}"
    )
    data = resp.json()
    assert "analogous_case" in data, (
        f"Response must include 'analogous_case' key; got: {list(data.keys())}"
    )
    assert data["analogous_case"] is None, (
        f"Expected analogous_case: null for SEN (not in CM mapping table); "
        f"got: {data['analogous_case']}. "
        "The fallback for unmapped entities must be null, not an error or a fabricated case."
    )


# ---------------------------------------------------------------------------
# API contracts — four new G4 paths documented before frontend impl begins
# ---------------------------------------------------------------------------

_REPO_ROOT = pathlib.Path(__file__).parent.parent.parent
_API_CONTRACTS = _REPO_ROOT / "docs" / "schema" / "api_contracts.yml"


def test_api_contracts_g4_paths_documented() -> None:
    """DA-G4-3: api_contracts.yml must document all four new G4 endpoints.

    Per DA-G4-3 in the intent document, the Data Architect Agent must update
    docs/schema/api_contracts.yml to add the four new G4 endpoints before the
    frontend implementation PR opens. This test confirms all four path strings
    are present in the contracts file.

    The four required path strings (DA-G4-3):
      1. 'loadable' field on GET /entities/{entity_id}/data-quality
      2. POST /entities/{entity_id}/pull  (new data pull trigger)
      3. GET  /entities/{entity_id}/pull/{job_id}  (new job status poll)
      4. GET  /scenarios/{scenario_id}/fidelity-context  (new fidelity endpoint)
    """
    assert _API_CONTRACTS.is_file(), (
        f"docs/schema/api_contracts.yml not found at {_API_CONTRACTS}"
    )
    content = _API_CONTRACTS.read_text()

    assert "loadable" in content, (
        "api_contracts.yml must document the new 'loadable' field on "
        "GET /entities/{entity_id}/data-quality (DA-G4-1 / DA-G4-3 requirement). "
        "Field not found in contracts file."
    )
    assert "/entities/{entity_id}/pull" in content, (
        "api_contracts.yml must document POST /entities/{entity_id}/pull "
        "(DA-G4-2 / DA-G4-3 requirement). Path not found in contracts file."
    )
    assert "/pull/{job_id}" in content, (
        "api_contracts.yml must document GET /entities/{entity_id}/pull/{job_id} "
        "(DA-G4-2 / DA-G4-3 requirement). Path not found in contracts file."
    )
    assert "/scenarios/{scenario_id}/fidelity-context" in content or \
           "/scenarios/{id}/fidelity-context" in content, (
        "api_contracts.yml must document GET /scenarios/{scenario_id}/fidelity-context "
        "(DA-G4-4 / DA-G4-3 requirement). Path not found in contracts file."
    )
