"""Unit tests for MultiFrameworkOutput schemas and GET /measurement-output — Issue #176.

Covers:
  - MultiFrameworkOutput rejects empty ia1_disclosure
  - MultiFrameworkOutput rejects whitespace-only ia1_disclosure
  - FINANCIAL framework groups financial-tagged attributes correctly
  - Untagged attributes (measurement_framework=None) classified as FINANCIAL
  - ECOLOGICAL returns composite_score=None with note field
  - GOVERNANCE returns composite_score=None with note field
  - composite_score is serialized as a string, not a float

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


def _snap_row(state: dict | None = None) -> dict:
    return {
        "scenario_id": "scen-1",
        "step": 1,
        "timestep": "2011-01-01",
        "state_data": json.dumps(state or _STATE),
    }


def _make_conn(*side_effects: dict[str, object] | None) -> AsyncMock:
    conn = AsyncMock()
    conn.fetchrow = AsyncMock(side_effect=list(side_effects))
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
        {"name": "Greece"},          # entity name lookup
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
        {"name": "Greece"},
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
        {"name": "Greece"},
    )
    result = await get_measurement_output(
        scenario_id="scen-1", entity_id="GRC", step=1, conn=conn
    )
    ecological = result.outputs["ecological"]
    assert ecological.composite_score is None
    assert ecological.note is not None
    assert "not yet implemented" in ecological.note


@pytest.mark.asyncio
async def test_governance_returns_null_composite_score_with_note() -> None:
    conn = _make_conn(
        {"scenario_id": "scen-1"},
        _snap_row(),
        {"name": "Greece"},
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
        {"name": "Greece"},
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
        {"name": "Greece"},
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
        {"name": "Greece"},
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
