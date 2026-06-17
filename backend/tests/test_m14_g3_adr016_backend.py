"""Integration tests for M14-G3 ADR-016 backend endpoints.

QA Lead step 2 — authored BEFORE implementation, from intent document at:
  docs/process/intents/M14-G3-2026-06-17-adr016-backend.md

These tests define "done" for G3. All AC-1–AC-8 tests will fail until
the Chief Engineer Agent delivers the implementation (Step 3). AC-9 fails
until the Data Architect Agent updates api_contracts.yml.

Uses httpx.AsyncClient with ASGITransport — no running server required.
All async tests skip gracefully when DATABASE_URL is not set.

AC coverage:
  AC-1  GET /entities/JOR/data-quality?year=2024 — financial framework present (T1–T5)
  AC-2  GET /entities/ZMB/data-quality?year=2024 — is_synthetic flag + non-empty synthetic_basis
  AC-3  GET /entities/GRC/data-quality?year=2010 — financial confidence_tier ≤ 2
  AC-4  GET /entities/{e}/data-quality?year=2024 for {GRC,JOR,EGY,ZMB} — all return 200
  AC-5  GET /entities/XXX/data-quality?year=2024 — 200 + empty frameworks list (SF-1 guard)
  AC-6  GET /scenarios/{jor_id}/initial-state — ≥1 indicator with display_name + confidence_tier
  AC-7  GET /scenarios/{jor_id}/initial-state — reserve_coverage_months with source + vintage
  AC-8  GET /scenarios/{id}/initial-state for no-registry scenario — 200 + empty frameworks (SF-2)
  AC-9  docs/schema/api_contracts.yml — both new path strings present (DA RACI obligation)
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

from app.main import app

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

pytestmark = pytest.mark.integration


def _require_db() -> None:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping M14-G3 ADR-016 integration test")


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
    """Minimal JOR scenario for AC-6 and AC-7 — entity with source-registry entries."""
    return {
        "name": "M14-G3 test — JOR initial state",
        "configuration": {
            "entities": ["JOR"],
            "n_steps": 1,
            "timestep_label": "annual",
        },
        "scheduled_inputs": [],
    }


def _no_registry_payload() -> dict[str, Any]:
    """Scenario with no entity data — simulates a pre-G3 scenario (SF-2 guard, AC-8).

    entities=[] means the step-0 snapshot contains no entity indicator data.
    The /initial-state endpoint must return 200 with empty frameworks, not 404.
    """
    return {
        "name": "M14-G3 test — no source registry association",
        "configuration": {
            "entities": [],
            "n_steps": 1,
            "timestep_label": "annual",
        },
        "scheduled_inputs": [],
    }


async def _create_and_run_scenario(
    client: httpx.AsyncClient,
    payload: dict[str, Any],
) -> str:
    """Create a scenario and run it to completion. Returns the scenario_id string."""
    create = await client.post("/api/v1/scenarios", json=payload)
    assert create.status_code == 201
    scenario_id = create.json()["scenario_id"]
    run = await client.post(f"/api/v1/scenarios/{scenario_id}/run")
    assert run.status_code == 200
    return str(scenario_id)


# ---------------------------------------------------------------------------
# AC-1 — /data-quality JOR financial framework present
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac1_data_quality_jor_financial_present(
    client: httpx.AsyncClient,
) -> None:
    """AC-1: JOR 2024 /data-quality returns 200 with a financial framework entry (T1–T5)."""
    resp = await client.get("/api/v1/entities/JOR/data-quality?year=2024")
    assert resp.status_code == 200
    data = resp.json()
    financial = [f for f in data["frameworks"] if f["framework"] == "financial"]
    assert len(financial) >= 1, (
        "Expected at least one financial framework entry for JOR 2024"
    )
    tier = financial[0]["confidence_tier"]
    assert 1 <= tier <= 5, f"confidence_tier {tier} not in valid range 1–5"


# ---------------------------------------------------------------------------
# AC-2 — /data-quality ZMB synthetic flag present
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac2_data_quality_zmb_synthetic_flag_present(
    client: httpx.AsyncClient,
) -> None:
    """AC-2: ZMB 2024 /data-quality has ≥1 synthetic entry with non-empty synthetic_basis."""
    resp = await client.get("/api/v1/entities/ZMB/data-quality?year=2024")
    assert resp.status_code == 200
    synthetic = [
        f for f in resp.json()["frameworks"] if f.get("is_synthetic") is True
    ]
    assert len(synthetic) >= 1, (
        "ZMB 2024 must have at least one synthetic framework entry"
    )
    synthetic_basis = synthetic[0].get("synthetic_basis")
    assert synthetic_basis, (
        "synthetic_basis must be a non-empty string when is_synthetic is true"
    )


# ---------------------------------------------------------------------------
# AC-3 — /data-quality GRC financial at T2 or better
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac3_data_quality_grc_financial_t2_or_better(
    client: httpx.AsyncClient,
) -> None:
    """AC-3: GRC 2010 financial confidence_tier must be ≤ 2 (IMF/World Bank observed data)."""
    resp = await client.get("/api/v1/entities/GRC/data-quality?year=2010")
    assert resp.status_code == 200
    financial = [
        f for f in resp.json()["frameworks"] if f["framework"] == "financial"
    ]
    assert len(financial) >= 1, "Expected financial framework entry for GRC 2010"
    tier = financial[0]["confidence_tier"]
    assert tier <= 2, (
        f"GRC 2010 financial must be T1 or T2 (observed IMF/WB data), got T{tier}"
    )


# ---------------------------------------------------------------------------
# AC-4 — /data-quality all four entities return 200
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac4_data_quality_all_four_entities_return_200(
    client: httpx.AsyncClient,
) -> None:
    """AC-4: GRC, JOR, EGY, ZMB all return HTTP 200 for year=2024; empty frameworks is OK."""
    for entity_id in ("GRC", "JOR", "EGY", "ZMB"):
        resp = await client.get(
            f"/api/v1/entities/{entity_id}/data-quality?year=2024"
        )
        assert resp.status_code == 200, (
            f"Expected 200 for {entity_id}/data-quality?year=2024, got {resp.status_code}"
        )
        data = resp.json()
        assert data["entity_id"] == entity_id
        assert data["year"] == 2024
        assert isinstance(data["frameworks"], list), (
            f"{entity_id}: frameworks must be a list (empty OK; 404/500 not acceptable)"
        )


# ---------------------------------------------------------------------------
# AC-5 — /data-quality unsupported entity returns empty frameworks, not 404 (SF-1)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac5_data_quality_unsupported_entity_empty_frameworks(
    client: httpx.AsyncClient,
) -> None:
    """AC-5 (SF-1): entity not in source registry → 200 + empty frameworks list, not 404."""
    resp = await client.get("/api/v1/entities/XXX/data-quality?year=2024")
    assert resp.status_code == 200, (
        f"Unsupported entity must return 200 with empty frameworks, got {resp.status_code} (SF-1)"
    )
    data = resp.json()
    assert data["entity_id"] == "XXX"
    assert data["year"] == 2024
    assert data["frameworks"] == [], (
        "frameworks must be [] for entity not in source registry — "
        "not 404, not entries with null source_institution"
    )


# ---------------------------------------------------------------------------
# AC-6 — /initial-state JOR scenario returns indicator with display_name + confidence_tier
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac6_initial_state_jor_indicator_present(
    client: httpx.AsyncClient,
) -> None:
    """AC-6: completed JOR /initial-state has ≥1 indicator with display_name + confidence_tier."""
    scenario_id = await _create_and_run_scenario(client, _jor_payload())
    resp = await client.get(f"/api/v1/scenarios/{scenario_id}/initial-state")
    assert resp.status_code == 200
    data = resp.json()
    assert data["entity_id"] == "JOR"
    frameworks = data["frameworks"]
    assert isinstance(frameworks, dict) and frameworks, (
        "frameworks must be a non-empty dict for a completed JOR scenario"
    )
    for fw_key, fw_val in frameworks.items():
        indicators = fw_val.get("indicators", [])
        assert indicators, (
            f"framework '{fw_key}' must contain at least one indicator"
        )
        for ind in indicators:
            assert ind.get("display_name"), (
                f"indicator '{ind.get('name')}' must have non-null display_name"
            )
            tier = ind.get("confidence_tier")
            assert tier is not None and 1 <= tier <= 5, (
                f"indicator '{ind.get('name')}' confidence_tier must be 1–5, got {tier}"
            )


# ---------------------------------------------------------------------------
# AC-7 — /initial-state reserve_coverage_months with non-null source and vintage
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac7_initial_state_reserve_coverage_months_cited(
    client: httpx.AsyncClient,
) -> None:
    """AC-7: JOR /initial-state has reserve_coverage_months with non-null source and vintage."""
    scenario_id = await _create_and_run_scenario(client, _jor_payload())
    resp = await client.get(f"/api/v1/scenarios/{scenario_id}/initial-state")
    assert resp.status_code == 200
    financial = resp.json()["frameworks"].get("financial", {})
    reserve = [
        i for i in financial.get("indicators", [])
        if i.get("name") == "reserve_coverage_months"
    ]
    assert reserve, (
        "frameworks['financial']['indicators'] must contain reserve_coverage_months — "
        "this is the Persona 2 north star indicator for input challenge response"
    )
    ind = reserve[0]
    assert ind.get("source"), (
        "reserve_coverage_months must have non-null source (e.g. 'IMF BOP') — "
        "required for Persona 2 to cite at the negotiating table"
    )
    assert ind.get("vintage"), (
        "reserve_coverage_months must have non-null vintage (e.g. '2024-Q1') — "
        "required for source attribution in the G4 Grounding strip"
    )


# ---------------------------------------------------------------------------
# AC-8 — /initial-state no source-registry data returns empty frameworks, not 404 (SF-2)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ac8_initial_state_no_registry_data_empty_frameworks(
    client: httpx.AsyncClient,
) -> None:
    """AC-8 (SF-2): scenario with no source-registry entity data → 200 + empty frameworks {}."""
    scenario_id = await _create_and_run_scenario(client, _no_registry_payload())
    resp = await client.get(f"/api/v1/scenarios/{scenario_id}/initial-state")
    assert resp.status_code == 200, (
        f"Pre-G3 scenario must return 200, not {resp.status_code} (SF-2 guard)"
    )
    assert resp.json()["frameworks"] == {}, (
        "frameworks must be {} (empty dict) for scenario with no source-registry data — "
        "empty is not the same as a missing key; the endpoint must return the key"
    )


# ---------------------------------------------------------------------------
# AC-9 — api_contracts.yml contains both endpoint path strings (DA RACI)
# ---------------------------------------------------------------------------


def test_ac9_api_contracts_yml_contains_both_endpoint_paths() -> None:
    """AC-9: api_contracts.yml has path entries for both new endpoints (Data Architect RACI)."""
    contracts_path = (
        pathlib.Path(__file__).parents[2] / "docs" / "schema" / "api_contracts.yml"
    )
    assert contracts_path.exists(), (
        f"api_contracts.yml not found at expected path {contracts_path}"
    )
    content = contracts_path.read_text()
    assert "/entities/{entity_id}/data-quality" in content, (
        "api_contracts.yml missing /data-quality endpoint — "
        "Data Architect must add it in the G3 PR (RACI obligation)"
    )
    assert "/scenarios/{scenario_id}/initial-state" in content, (
        "api_contracts.yml missing /initial-state endpoint — "
        "Data Architect must add it in the G3 PR (RACI obligation)"
    )
