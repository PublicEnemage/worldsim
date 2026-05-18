"""Unit tests for MultiFrameworkOutput schemas and GET /measurement-output — Issue #176, #193.

Covers:
  - MultiFrameworkOutput rejects empty ia1_disclosure
  - MultiFrameworkOutput rejects whitespace-only ia1_disclosure
  - FINANCIAL framework groups financial-tagged attributes correctly
  - Untagged attributes (measurement_framework=None) classified as FINANCIAL
  - ECOLOGICAL returns composite_score=None with note field
  - GOVERNANCE returns composite_score=None with note field
  - composite_score is serialized as a string, not a float
  - Single-entity scenario: composite_score=None, single_entity_warning=True (Issue #193)
  - Multi-entity scenario: composite_score non-null, single_entity_warning=False (Issue #193)

All tests run without a database connection using AsyncMock.
ADR-005 Decision 2.
"""
from __future__ import annotations

import json
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from app.api.scenarios import get_measurement_output
from app.schemas import MDAAlert, MDASeverity, MultiFrameworkOutput
from app.simulation.repositories.quantity_serde import IA1_CANONICAL_PHRASE

# ---------------------------------------------------------------------------
# Shared test state_data
# ---------------------------------------------------------------------------

_GRC_FINANCIAL_ATTR = {
    "_envelope_version": "1",
    "value": "-0.054",
    "unit": "dimensionless",
    "variable_type": "ratio",
    "confidence_tier": 1,
    "observation_date": None,
    "source_registry_id": "IMF_WEO_2013",
    "measurement_framework": "financial",
}

_GRC_UNTAGGED_ATTR = {
    "_envelope_version": "1",
    "value": "0.127",
    "unit": "dimensionless",
    "variable_type": "ratio",
    "confidence_tier": 2,
    "observation_date": None,
    "source_registry_id": "EUROSTAT_LFS_2010",
    "measurement_framework": None,
}

_USA_FINANCIAL_ATTR = {
    "_envelope_version": "1",
    "value": "0.023",
    "unit": "dimensionless",
    "variable_type": "ratio",
    "confidence_tier": 1,
    "observation_date": None,
    "source_registry_id": "BEA_NIPA_2013",
    "measurement_framework": "financial",
}

_STATE = {
    "_envelope_version": "2",
    "_modules_active": [],
    "GRC": {
        "gdp_growth": _GRC_FINANCIAL_ATTR,
        "unemployment_rate": _GRC_UNTAGGED_ATTR,
    },
    "USA": {
        "gdp_growth": _USA_FINANCIAL_ATTR,
    },
}


def _snap_row(state: dict | None = None, events_snapshot: list | None = None) -> dict:
    return {
        "scenario_id": "scen-1",
        "step": 1,
        "timestep": "2011-01-01",
        "state_data": json.dumps(state or _STATE),
        "events_snapshot": events_snapshot,  # None for pre-M4 snapshots
    }


def _entity_row(name: str = "Greece") -> dict:
    """Mock row for SELECT metadata FROM simulation_entities (commit b93ac3d format)."""
    return {"metadata": json.dumps({"name_en": name})}


def _make_conn(*side_effects: dict[str, object] | None) -> AsyncMock:
    conn = AsyncMock()
    conn.fetchrow = AsyncMock(side_effect=list(side_effects))
    # conn.fetch is used by _fetch_active_boundary_constants for ecological composite score.
    # Default empty list = no active boundary constants = ecological composite_score None.
    conn.fetch = AsyncMock(return_value=[])
    return conn


# ---------------------------------------------------------------------------
# Schema validation tests — no DB required
# ---------------------------------------------------------------------------


def test_multiframework_output_rejects_empty_ia1_disclosure() -> None:
    with pytest.raises(ValidationError) as exc_info:
        MultiFrameworkOutput(
            entity_id="GRC",
            entity_name="Greece",
            timestep="2011-01-01",
            scenario_id="scen-1",
            step_index=1,
            outputs={},
            ia1_disclosure="",
        )
    assert "ia1_disclosure" in str(exc_info.value)


def test_multiframework_output_rejects_whitespace_ia1_disclosure() -> None:
    with pytest.raises(ValidationError) as exc_info:
        MultiFrameworkOutput(
            entity_id="GRC",
            entity_name="Greece",
            timestep="2011-01-01",
            scenario_id="scen-1",
            step_index=1,
            outputs={},
            ia1_disclosure="   ",
        )
    assert "ia1_disclosure" in str(exc_info.value)


def test_multiframework_output_accepts_canonical_ia1_disclosure() -> None:
    obj = MultiFrameworkOutput(
        entity_id="GRC",
        entity_name="Greece",
        timestep="2011-01-01",
        scenario_id="scen-1",
        step_index=1,
        outputs={},
        ia1_disclosure=IA1_CANONICAL_PHRASE,
    )
    assert obj.ia1_disclosure == IA1_CANONICAL_PHRASE


def test_mda_severity_enum_values() -> None:
    assert MDASeverity.WARNING == "WARNING"
    assert MDASeverity.CRITICAL == "CRITICAL"
    assert MDASeverity.TERMINAL == "TERMINAL"


def test_mda_alert_decimal_fields_are_strings() -> None:
    alert = MDAAlert(
        mda_id="MDA-001",
        entity_id="GRC",
        indicator_key="poverty_headcount_ratio",
        severity=MDASeverity.CRITICAL,
        floor_value="0.25",
        current_value="0.31",
        approach_pct_remaining="-0.24",
        consecutive_breach_steps=1,
    )
    assert isinstance(alert.floor_value, str)
    assert isinstance(alert.current_value, str)
    assert isinstance(alert.approach_pct_remaining, str)


# ---------------------------------------------------------------------------
# Endpoint unit tests — DB mocked with AsyncMock
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_financial_framework_groups_financial_tagged_attributes() -> None:
    conn = _make_conn(
        {"scenario_id": "scen-1"},  # scenario exists
        _snap_row(),                 # snapshot at step 1
        _entity_row(),               # entity name lookup
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    financial = result.outputs["financial"]
    assert "gdp_growth" in financial.indicators
    assert financial.indicators["gdp_growth"].value == "-0.054"
    assert financial.indicators["gdp_growth"].measurement_framework == "financial"


@pytest.mark.asyncio
async def test_untagged_attributes_classified_as_financial() -> None:
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(),
        _entity_row(),
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    financial = result.outputs["financial"]
    # unemployment_rate has measurement_framework=None — must appear in FINANCIAL
    assert "unemployment_rate" in financial.indicators
    assert financial.indicators["unemployment_rate"].measurement_framework is None


@pytest.mark.asyncio
async def test_ecological_returns_null_composite_score_with_note() -> None:
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(),
        _entity_row(),
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    ecological = result.outputs["ecological"]
    # No proximity indicators in _STATE, no active boundary constants → composite None.
    assert ecological.composite_score is None
    assert ecological.note is not None
    # ADR-005 Amendment 3 Decision M8-1: mandatory note references boundary proximity formula.
    assert "boundary" in ecological.note
    assert "Composite range: [0.0, 2.0]" in ecological.note


@pytest.mark.asyncio
async def test_governance_returns_null_composite_score_with_note() -> None:
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(),
        _entity_row(),
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    governance = result.outputs["governance"]
    assert governance.composite_score is None
    assert governance.note is not None
    assert "not yet implemented" in governance.note


@pytest.mark.asyncio
async def test_composite_score_is_string_not_float() -> None:
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(),
        _entity_row(),
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    financial = result.outputs["financial"]
    assert financial.composite_score is not None
    assert isinstance(financial.composite_score, str)
    # Must parse to a Decimal — no float contamination
    score = Decimal(financial.composite_score)
    assert Decimal("0") <= score <= Decimal("1")


@pytest.mark.asyncio
async def test_all_four_frameworks_present_in_response() -> None:
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(),
        _entity_row(),
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    assert set(result.outputs.keys()) == {
        "financial", "human_development", "ecological", "governance"
    }


@pytest.mark.asyncio
async def test_ia1_disclosure_is_canonical_phrase() -> None:
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(),
        _entity_row(),
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    assert result.ia1_disclosure == IA1_CANONICAL_PHRASE


@pytest.mark.asyncio
async def test_missing_scenario_returns_404() -> None:
    from fastapi import HTTPException

    conn = _make_conn(None)  # scenario not found
    with pytest.raises(HTTPException) as exc_info:
        await get_measurement_output(
            scenario_id="bad-id", entity_id="GRC", step=1, conn=conn
        )
    assert exc_info.value.status_code == 404
    assert "bad-id" in exc_info.value.detail


@pytest.mark.asyncio
async def test_missing_snapshot_returns_404() -> None:
    from fastapi import HTTPException

    conn = _make_conn(
        {"scenario_id": "scen-1"},  # scenario exists
        None,                        # no snapshot at this step
    )
    with pytest.raises(HTTPException) as exc_info:
        await get_measurement_output(
            scenario_id="scen-1", entity_id="GRC", step=99, conn=conn
        )
    assert exc_info.value.status_code == 404
    assert "99" in exc_info.value.detail


@pytest.mark.asyncio
async def test_entity_name_falls_back_to_entity_id_when_not_in_db() -> None:
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(),
        None,  # entity not in simulation_entities
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    assert result.entity_name == "GRC"


# ---------------------------------------------------------------------------
# Single-entity composite score warning — Issue #193
# ---------------------------------------------------------------------------

_SINGLE_ENTITY_STATE = {
    "_envelope_version": "2",
    "_modules_active": [],
    "GRC": {
        "gdp_growth": _GRC_FINANCIAL_ATTR,
        "unemployment_rate": _GRC_UNTAGGED_ATTR,
    },
}


@pytest.mark.asyncio
async def test_single_entity_composite_score_is_null() -> None:
    """Single-entity: financial and human_development composite_score must be None.

    Ecological is exempt from the single-entity guard (ADR-005 Amendment 3 Decision M8-2)
    and is tested separately in test_ecological_exempt_from_single_entity_guard.
    """
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(state=_SINGLE_ENTITY_STATE),
        _entity_row(),
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    assert result.outputs["financial"].composite_score is None
    assert result.outputs["human_development"].composite_score is None


@pytest.mark.asyncio
async def test_single_entity_warning_is_true() -> None:
    """Single-entity snapshot: single_entity_warning must be True."""
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(state=_SINGLE_ENTITY_STATE),
        _entity_row(),
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    assert result.single_entity_warning is True


@pytest.mark.asyncio
async def test_single_entity_note_on_implemented_frameworks() -> None:
    """Single-entity: implemented frameworks carry the single-entity note."""
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(state=_SINGLE_ENTITY_STATE),
        _entity_row(),
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    financial_note = result.outputs["financial"].note
    assert financial_note is not None
    assert "not meaningful" in financial_note
    assert "single-entity" in financial_note


@pytest.mark.asyncio
async def test_single_entity_unimplemented_frameworks_keep_their_note() -> None:
    """Single-entity: ecological gets the mandatory ADR-005 Amendment B note;
    governance (still unimplemented) keeps the 'not yet implemented' note."""
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(state=_SINGLE_ENTITY_STATE),
        _entity_row(),
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    # ADR-005 Amendment 3 Decision M8-1: ecological always gets the mandatory boundary note.
    assert "boundary" in result.outputs["ecological"].note
    assert "Composite range: [0.0, 2.0]" in result.outputs["ecological"].note
    # Governance module still unimplemented (deferred to M9 — Decision M8-4).
    assert "not yet implemented" in result.outputs["governance"].note


@pytest.mark.asyncio
async def test_multi_entity_single_entity_warning_is_false() -> None:
    """Multi-entity snapshot: single_entity_warning must be False."""
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(),   # _STATE has GRC + USA
        _entity_row(),
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    assert result.single_entity_warning is False


# ---------------------------------------------------------------------------
# Framework Promotion Protocol CI enforcement — CODING_STANDARDS.md §Framework Promotion Protocol
# ---------------------------------------------------------------------------


def test_governance_is_in_unimplemented_frameworks() -> None:
    """CI enforcement: governance composite scores must be None while 'governance'
    is in _UNIMPLEMENTED_FRAMEWORKS.

    This test is the explicit, testable precondition for promotion. It will
    PASS as long as governance is unimplemented (correct) and must be REMOVED
    (not just disabled) when the companion integration test that satisfies
    promotion criterion 5 is written and passes.

    CODING_STANDARDS.md §Framework Promotion Protocol promotion criterion 5:
    'The act of satisfying the companion integration test is the explicit,
    testable precondition for the API surface change.'
    """
    from app.api.scenarios import _UNIMPLEMENTED_FRAMEWORKS
    assert "governance" in _UNIMPLEMENTED_FRAMEWORKS, (
        "governance was removed from _UNIMPLEMENTED_FRAMEWORKS without satisfying "
        "all five promotion criteria in CODING_STANDARDS.md §Framework Promotion Protocol. "
        "Remove this test only after the companion integration test passes."
    )


@pytest.mark.asyncio
async def test_governance_composite_score_is_none_when_unimplemented() -> None:
    """Governance composite_score must be None while governance is in _UNIMPLEMENTED_FRAMEWORKS.

    Companion to test_governance_is_in_unimplemented_frameworks. If governance
    is promoted, both this test and the guard test above must be updated together.
    """
    from app.api.scenarios import _UNIMPLEMENTED_FRAMEWORKS
    if "governance" not in _UNIMPLEMENTED_FRAMEWORKS:
        pytest.skip("governance has been promoted — update this test")

    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(),
        _entity_row(),
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    assert result.outputs["governance"].composite_score is None, (
        "governance composite_score must be None while governance is unimplemented"
    )


@pytest.mark.asyncio
async def test_multi_entity_composite_score_is_not_null() -> None:
    """Multi-entity snapshot: financial composite_score must be a non-null string."""
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(),   # _STATE has GRC + USA
        _entity_row(),
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    assert result.outputs["financial"].composite_score is not None
    assert isinstance(result.outputs["financial"].composite_score, str)


# ---------------------------------------------------------------------------
# ADR-005 Amendment 3 — strategy dispatch and ecological exemption
# ---------------------------------------------------------------------------

_ECOLOGICAL_ATTR = {
    "_envelope_version": "1",
    "value": "1.2",
    "unit": "ratio_0_1",
    "variable_type": "stock",
    "confidence_tier": 2,
    "observation_date": None,
    "source_registry_id": "ECO_TEST",
    "measurement_framework": "ecological",
}

_SINGLE_ENTITY_ECO_STATE = {
    "_envelope_version": "2",
    "_modules_active": [],
    "GRC": {
        "planetary_boundary_co2_proximity": _ECOLOGICAL_ATTR,
    },
}


def test_ecological_exempt_frameworks_constant_exists() -> None:
    """_SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS must exist and include ecological."""
    from app.api.scenarios import _SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS
    assert "ecological" in _SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS


@pytest.mark.asyncio
async def test_ecological_exempt_from_single_entity_guard() -> None:
    """Single-entity snapshot: ecological composite_score is computed (not suppressed).

    ADR-005 Amendment 3 Decision M8-2 — boundary proximity is physically meaningful
    for a single entity. With active boundary constants (mocked), composite is non-null.
    """
    boundary_row = {"constant_id": "ECOLOGICAL_CO2_PLANETARY_BOUNDARY_PPM", "value": "350"}
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(state=_SINGLE_ENTITY_ECO_STATE),
        _entity_row(),
    )
    # Override fetch to return an active boundary constant.
    conn.fetch = AsyncMock(return_value=[boundary_row])

    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    assert result.single_entity_warning is True
    # Financial and human_development are still suppressed.
    assert result.outputs["financial"].composite_score is None
    assert result.outputs["human_development"].composite_score is None
    # Ecological is exempt — composite_score computed from proximity value 1.2 → min(1.2, 2.0).
    eco = result.outputs["ecological"]
    assert eco.composite_score is not None
    from decimal import Decimal
    score = Decimal(eco.composite_score)
    assert score == Decimal("1.2000")


@pytest.mark.asyncio
async def test_three_branch_dispatch_ecological_uses_boundary_strategy(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Ecological framework must use the boundary proximity strategy, not percentile rank."""
    import logging
    boundary_row = {"constant_id": "ECOLOGICAL_CO2_PLANETARY_BOUNDARY_PPM", "value": "350"}
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(state=_SINGLE_ENTITY_ECO_STATE),
        _entity_row(),
    )
    conn.fetch = AsyncMock(return_value=[boundary_row])

    with caplog.at_level(logging.WARNING, logger="app.api.scenarios"):
        result = await get_measurement_output(
            scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
        )

    # No [SIM-INTEGRITY] warning for ecological — it has a registered strategy.
    sim_warnings = [r for r in caplog.records if "[SIM-INTEGRITY]" in r.message]
    assert not any("ecological" in w.message for w in sim_warnings)
    assert result.outputs["ecological"].composite_score is not None


@pytest.mark.asyncio
async def test_ecological_composite_null_when_no_active_boundary_constants(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Ecological composite_score is None when no boundary constants are active.

    conn.fetch returns [] (no constants seeded) — _boundary_proximity_strategy
    cannot validate temporal availability and emits [SIM-INTEGRITY] WARNING per indicator.
    """
    import logging
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(state=_SINGLE_ENTITY_ECO_STATE),
        _entity_row(),
    )
    conn.fetch = AsyncMock(return_value=[])  # no active constants

    with caplog.at_level(logging.WARNING, logger="app.api.scenarios"):
        result = await get_measurement_output(
            scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
        )

    assert result.outputs["ecological"].composite_score is None


def test_multiframework_output_default_single_entity_warning_is_false() -> None:
    """single_entity_warning defaults to False so existing callers without it stay valid."""
    obj = MultiFrameworkOutput(
        entity_id="GRC",
        entity_name="Greece",
        timestep="2011-01-01",
        scenario_id="scen-1",
        step_index=1,
        outputs={},
        ia1_disclosure=IA1_CANONICAL_PHRASE,
    )
    assert obj.single_entity_warning is False
