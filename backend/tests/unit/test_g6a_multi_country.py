"""
G6a — Multi-country scenario backend unit tests (Issue #754, #153).

Tests:
  - _load_relationships: real DB edges loaded; synthetic Tier 4 injected for missing pairs
  - _validate_create_request: entities list 1–5 enforcement
  - _compute_delta threshold_crossed field
  - ScenarioIdentityHeader entityIds → single "Entity:" vs plural "Entities:"
  - DeltaRecord threshold_crossed schema field
"""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.api.scenarios import _compute_delta, _validate_create_request
from app.schemas import DeltaRecord, ScenarioConfigSchema, ScenarioCreateRequest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_config(**kwargs: object) -> ScenarioConfigSchema:
    defaults: dict[str, object] = {
        "entities": ["GRC"],
        "n_steps": 5,
        "timestep_label": "annual",
    }
    defaults.update(kwargs)
    return ScenarioConfigSchema(**defaults)  # type: ignore[arg-type]


def _make_request(entities: list[str]) -> ScenarioCreateRequest:
    return ScenarioCreateRequest(
        name="test",
        configuration=_make_config(entities=entities),
    )


# ---------------------------------------------------------------------------
# 1. _validate_create_request — entity count gate
# ---------------------------------------------------------------------------


def test_validate_accepts_one_entity() -> None:
    _validate_create_request(_make_request(["GRC"]))  # no exception


def test_validate_accepts_five_entities() -> None:
    _validate_create_request(_make_request(["GRC", "DEU", "FRA", "ITA", "ESP"]))


def test_validate_rejects_zero_entities() -> None:
    from fastapi import HTTPException  # noqa: PLC0415
    with pytest.raises(HTTPException) as exc:
        _validate_create_request(_make_request([]))
    assert "1–5" in str(exc.value.detail)


def test_validate_rejects_six_entities() -> None:
    from fastapi import HTTPException  # noqa: PLC0415
    with pytest.raises(HTTPException) as exc:
        _validate_create_request(_make_request(["A", "B", "C", "D", "E", "F"]))
    assert "1–5" in str(exc.value.detail)


# ---------------------------------------------------------------------------
# 2. _compute_delta — threshold_crossed field (Issue #153)
# ---------------------------------------------------------------------------


def test_compute_delta_no_threshold_returns_none() -> None:
    record = _compute_delta("0.85", "0.92", 1, 1)
    assert record.threshold_crossed is None


def test_compute_delta_threshold_not_crossed() -> None:
    record = _compute_delta("0.85", "0.92", 1, 1, threshold_value="0.80")
    assert record.threshold_crossed is False  # both above 0.80


def test_compute_delta_threshold_crossed_upward() -> None:
    record = _compute_delta("0.75", "0.85", 1, 1, threshold_value="0.80")
    assert record.threshold_crossed is True  # crosses 0.80 upward


def test_compute_delta_threshold_crossed_downward() -> None:
    record = _compute_delta("0.85", "0.75", 1, 1, threshold_value="0.80")
    assert record.threshold_crossed is True  # crosses 0.80 downward


def test_compute_delta_threshold_at_boundary_not_crossed() -> None:
    # value_a exactly at threshold — dec_a < thr is False on both sides
    record = _compute_delta("0.80", "0.90", 1, 1, threshold_value="0.80")
    assert record.threshold_crossed is False


def test_compute_delta_threshold_crossed_preserves_direction() -> None:
    record = _compute_delta("0.75", "0.85", 1, 1, threshold_value="0.80")
    assert record.direction == "increase"
    assert record.threshold_crossed is True


# ---------------------------------------------------------------------------
# 3. DeltaRecord schema — threshold_crossed is optional None by default
# ---------------------------------------------------------------------------


def test_delta_record_threshold_crossed_defaults_none() -> None:
    r = DeltaRecord(
        value_a="1.0", value_b="2.0", delta="1.0",
        direction="increase", confidence_tier=1,
    )
    assert r.threshold_crossed is None


def test_delta_record_threshold_crossed_can_be_set() -> None:
    r = DeltaRecord(
        value_a="1.0", value_b="2.0", delta="1.0",
        direction="increase", confidence_tier=1,
        threshold_crossed=True,
    )
    assert r.threshold_crossed is True


# ---------------------------------------------------------------------------
# 4. _load_relationships — relationship loading logic
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_load_relationships_single_entity_returns_empty() -> None:
    from app.simulation.repositories.state_repository import _load_relationships  # noqa: PLC0415
    conn = AsyncMock()
    result = await _load_relationships(conn, ["GRC"])
    assert result == []
    conn.fetch.assert_not_called()


@pytest.mark.asyncio
async def test_load_relationships_real_edges_loaded() -> None:
    from app.simulation.repositories.state_repository import _load_relationships  # noqa: PLC0415

    mock_row = {
        "source_id": "GRC",
        "target_id": "DEU",
        "relationship_type": "trade",
        "weight": 0.6,
        "attributes": "{}",
    }
    conn = AsyncMock()
    conn.fetch = AsyncMock(return_value=[mock_row])

    result = await _load_relationships(conn, ["GRC", "DEU"])

    real = [r for r in result if not r.attributes.get("synthetic")]
    assert len(real) == 1
    assert real[0].source_id == "GRC"
    assert real[0].target_id == "DEU"
    assert real[0].weight == pytest.approx(0.6)


@pytest.mark.asyncio
async def test_load_relationships_synthetic_injected_for_missing_pair() -> None:
    from app.simulation.repositories.state_repository import _load_relationships  # noqa: PLC0415

    conn = AsyncMock()
    conn.fetch = AsyncMock(return_value=[])  # no real edges

    result = await _load_relationships(conn, ["GRC", "DEU"])

    synthetic = [r for r in result if r.attributes.get("synthetic")]
    # Both directions: GRC→DEU and DEU→GRC
    assert len(synthetic) == 2
    pairs = {(r.source_id, r.target_id) for r in synthetic}
    assert ("GRC", "DEU") in pairs
    assert ("DEU", "GRC") in pairs


@pytest.mark.asyncio
async def test_load_relationships_synthetic_confidence_tier_4() -> None:
    from app.simulation.repositories.state_repository import _load_relationships  # noqa: PLC0415

    conn = AsyncMock()
    conn.fetch = AsyncMock(return_value=[])

    result = await _load_relationships(conn, ["GRC", "DEU"])

    for rel in result:
        assert rel.attributes.get("confidence_tier") == 4


@pytest.mark.asyncio
async def test_load_relationships_real_pair_not_duplicated_by_synthetic() -> None:
    from app.simulation.repositories.state_repository import _load_relationships  # noqa: PLC0415

    mock_row = {
        "source_id": "GRC",
        "target_id": "DEU",
        "relationship_type": "trade",
        "weight": 0.5,
        "attributes": "{}",
    }
    conn = AsyncMock()
    conn.fetch = AsyncMock(return_value=[mock_row])

    result = await _load_relationships(conn, ["GRC", "DEU"])

    # Real GRC→DEU exists — no synthetic for that direction
    grc_deu = [r for r in result if r.source_id == "GRC" and r.target_id == "DEU"]
    assert len(grc_deu) == 1
    assert not grc_deu[0].attributes.get("synthetic")

    # Reverse DEU→GRC has no real edge — synthetic injected
    deu_grc = [r for r in result if r.source_id == "DEU" and r.target_id == "GRC"]
    assert len(deu_grc) == 1
    assert deu_grc[0].attributes.get("synthetic")


@pytest.mark.asyncio
async def test_load_relationships_three_entities_all_pairs_covered() -> None:
    from app.simulation.repositories.state_repository import _load_relationships  # noqa: PLC0415

    conn = AsyncMock()
    conn.fetch = AsyncMock(return_value=[])

    result = await _load_relationships(conn, ["A", "B", "C"])

    # 3 entities → 3×2=6 ordered pairs, all synthetic
    assert len(result) == 6
    pairs = {(r.source_id, r.target_id) for r in result}
    assert ("A", "B") in pairs
    assert ("B", "A") in pairs
    assert ("A", "C") in pairs
    assert ("C", "A") in pairs
    assert ("B", "C") in pairs
    assert ("C", "B") in pairs
