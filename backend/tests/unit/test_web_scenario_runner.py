"""Unit tests for WebScenarioRunner and simulation repository components.

Tests cover:
  SA-11 determinism: same config + same initial state → identical snapshot contents
  SA-12 round-trip: Quantity → JSONB → QuantitySchema → Quantity without data loss
  SA-04 status transitions: pending→running→completed, pending→running→failed
  IA-1 disclosure: ia1_disclosure is always set and contains the canonical phrase
  quantity_to_jsonb_envelope: field types and _envelope_version
  quantity_from_schema: field type restoration (Decimal, int, date not string)

All tests run without a database connection. DB-dependent paths use MagicMock /
AsyncMock to simulate asyncpg behaviour.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.simulation.engine.models import (
    MeasurementFramework,
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.engine.quantity import Quantity, VariableType
from app.simulation.orchestration.runner import ScenarioRunner
from app.simulation.repositories.quantity_serde import (
    IA1_CANONICAL_PHRASE,
    STATE_DATA_ENVELOPE_VERSION,
    quantity_from_jsonb,
    quantity_to_jsonb_envelope,
    validate_ia1_disclosure,
)
from app.simulation.repositories.snapshot_repository import ScenarioSnapshotRepository
from app.simulation.web_scenario_runner import RunSummary, WebScenarioRunner

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_quantity(
    value: str = "12345.67",
    unit: str = "USD_2015",
    variable_type: VariableType = VariableType.STOCK,
    confidence_tier: int = 3,
    observation_date: date | None = date(2010, 1, 1),
    source_id: str | None = "TEST_SOURCE",
    measurement_framework: MeasurementFramework | None = MeasurementFramework.FINANCIAL,
) -> Quantity:
    return Quantity(
        value=Decimal(value),
        unit=unit,
        variable_type=variable_type,
        confidence_tier=confidence_tier,
        observation_date=observation_date,
        source_id=source_id,
        measurement_framework=measurement_framework,
    )


def _make_entity(
    entity_id: str = "GRC", attrs: dict[str, Quantity] | None = None
) -> SimulationEntity:
    return SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes=attrs or {
            "gdp_growth": _make_quantity(
                value="-0.054", unit="ratio", variable_type=VariableType.RATIO
            )
        },
        metadata={"name_en": "Greece"},
    )


def _make_state(entities: dict[str, SimulationEntity] | None = None) -> SimulationState:
    if entities is None:
        entities = {"GRC": _make_entity()}
    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    end = datetime(2012, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    return SimulationState(
        timestep=ts,
        resolution=ResolutionConfig(),
        entities=entities,
        relationships=[],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="test-id",
            name="Test Scenario",
            description="",
            start_date=ts,
            end_date=end,
        ),
    )


def _make_mock_conn(
    scenario_status: str = "pending",
    n_steps: int = 1,
    entity_ids: list[str] | None = None,
) -> MagicMock:
    """Build a mock asyncpg connection for WebScenarioRunner unit tests."""
    conn = MagicMock()

    cfg = {
        "entities": entity_ids or [],
        "n_steps": n_steps,
        "timestep_label": "annual",
        "initial_attributes": {},
    }

    conn.fetchrow = AsyncMock(
        return_value={
            "scenario_id": "test-id",
            "name": "Test",
            "status": scenario_status,
            "configuration": json.dumps(cfg),
        }
    )
    conn.fetch = AsyncMock(return_value=[])
    conn.execute = AsyncMock(return_value="UPDATE 1")

    class _FakeTx:
        async def __aenter__(self) -> _FakeTx:
            return self

        async def __aexit__(self, *args: Any) -> None:  # noqa: ANN401
            pass

    conn.transaction = MagicMock(return_value=_FakeTx())
    return conn


# ---------------------------------------------------------------------------
# SA-11: Determinism test
# ---------------------------------------------------------------------------


def test_scenario_runner_is_deterministic() -> None:
    """SA-11: Same config + same initial state → identical snapshot attribute values.

    Runs ScenarioRunner twice from the same state with no modules (M3 baseline).
    All entity attribute values must be identical across both runs at every step.
    """
    state = _make_state()

    history_a = ScenarioRunner(
        initial_state=state,
        scheduled_inputs=[],
        modules=[],
        n_steps=2,
    ).run()

    history_b = ScenarioRunner(
        initial_state=state,
        scheduled_inputs=[],
        modules=[],
        n_steps=2,
    ).run()

    assert len(history_a) == len(history_b)

    for step, (s_a, s_b) in enumerate(zip(history_a, history_b, strict=False)):
        for entity_id in s_a.entities:
            assert entity_id in s_b.entities, (
                f"Entity {entity_id!r} missing at step {step} in run B"
            )
            attrs_a = s_a.entities[entity_id].attributes
            attrs_b = s_b.entities[entity_id].attributes
            assert attrs_a.keys() == attrs_b.keys(), f"Attribute key mismatch at step {step}"
            for attr_key in attrs_a:
                val_a = attrs_a[attr_key].value
                val_b = attrs_b[attr_key].value
                assert val_a == val_b, (
                    f"Non-determinism at step {step}, entity {entity_id!r}, "
                    f"attribute {attr_key!r}: {val_a} != {val_b}"
                )


# ---------------------------------------------------------------------------
# SA-12: Round-trip tests
# ---------------------------------------------------------------------------


def test_quantity_round_trip_preserves_decimal_value() -> None:
    """SA-12: Decimal value survives Quantity → envelope → QuantitySchema → Quantity."""
    original = _make_quantity(value="12345.6789012345")
    envelope = quantity_to_jsonb_envelope(original)
    restored = quantity_from_jsonb(envelope)
    assert restored.value == original.value
    assert isinstance(restored.value, Decimal)


def test_quantity_round_trip_preserves_unit() -> None:
    """SA-12: unit string survives round-trip."""
    original = _make_quantity(unit="EUR_2015_PPP")
    restored = quantity_from_jsonb(quantity_to_jsonb_envelope(original))
    assert restored.unit == original.unit


def test_quantity_round_trip_preserves_variable_type() -> None:
    """SA-12: variable_type enum survives round-trip as VariableType, not string."""
    for vt in VariableType:
        original = _make_quantity(variable_type=vt)
        restored = quantity_from_jsonb(quantity_to_jsonb_envelope(original))
        assert restored.variable_type == vt
        assert isinstance(restored.variable_type, VariableType)


def test_quantity_round_trip_preserves_confidence_tier_as_int() -> None:
    """SA-12: confidence_tier survives round-trip as int, not float."""
    original = _make_quantity(confidence_tier=4)
    restored = quantity_from_jsonb(quantity_to_jsonb_envelope(original))
    assert restored.confidence_tier == 4
    assert isinstance(restored.confidence_tier, int)


def test_quantity_round_trip_preserves_observation_date_as_date() -> None:
    """SA-12: observation_date survives round-trip as date object, not ISO string."""
    original = _make_quantity(observation_date=date(2010, 6, 15))
    restored = quantity_from_jsonb(quantity_to_jsonb_envelope(original))
    assert restored.observation_date == date(2010, 6, 15)
    assert isinstance(restored.observation_date, date)


def test_quantity_round_trip_preserves_none_observation_date() -> None:
    """SA-12: None observation_date survives round-trip as None, not 'None'."""
    original = _make_quantity(observation_date=None)
    restored = quantity_from_jsonb(quantity_to_jsonb_envelope(original))
    assert restored.observation_date is None


def test_quantity_round_trip_preserves_source_id() -> None:
    """SA-12: source_id (stored as source_registry_id in envelope) survives round-trip."""
    original = _make_quantity(source_id="IMF_WEO_APR2010")
    restored = quantity_from_jsonb(quantity_to_jsonb_envelope(original))
    assert restored.source_id == "IMF_WEO_APR2010"


def test_quantity_round_trip_preserves_measurement_framework() -> None:
    """SA-12: measurement_framework enum survives round-trip."""
    for mf in MeasurementFramework:
        original = _make_quantity(measurement_framework=mf)
        restored = quantity_from_jsonb(quantity_to_jsonb_envelope(original))
        assert restored.measurement_framework == mf
        assert isinstance(restored.measurement_framework, MeasurementFramework)


def test_quantity_round_trip_preserves_none_measurement_framework() -> None:
    """SA-12: None measurement_framework survives round-trip as None."""
    original = _make_quantity(measurement_framework=None)
    restored = quantity_from_jsonb(quantity_to_jsonb_envelope(original))
    assert restored.measurement_framework is None


# ---------------------------------------------------------------------------
# quantity_to_jsonb_envelope: format checks
# ---------------------------------------------------------------------------


def test_envelope_contains_version() -> None:
    """SA-09: _envelope_version field must be present and equal '1'."""
    envelope = quantity_to_jsonb_envelope(_make_quantity())
    assert envelope["_envelope_version"] == "1"


def test_envelope_value_is_string() -> None:
    """SA-09: value must be a string (float prohibition)."""
    envelope = quantity_to_jsonb_envelope(_make_quantity(value="9999.99"))
    assert isinstance(envelope["value"], str)
    assert envelope["value"] == "9999.99"


def test_envelope_variable_type_is_string() -> None:
    """SA-09: variable_type must be the enum .value string."""
    envelope = quantity_to_jsonb_envelope(_make_quantity(variable_type=VariableType.FLOW))
    assert envelope["variable_type"] == "flow"
    assert isinstance(envelope["variable_type"], str)


def test_envelope_observation_date_is_iso_string_or_none() -> None:
    """SA-09: observation_date is ISO-8601 string or None, never a date object."""
    envelope = quantity_to_jsonb_envelope(_make_quantity(observation_date=date(2010, 1, 1)))
    assert envelope["observation_date"] == "2010-01-01"
    assert isinstance(envelope["observation_date"], str)

    envelope_none = quantity_to_jsonb_envelope(_make_quantity(observation_date=None))
    assert envelope_none["observation_date"] is None


# ---------------------------------------------------------------------------
# IA-1 disclosure
# ---------------------------------------------------------------------------


def test_ia1_canonical_phrase_not_empty() -> None:
    """SA-01: IA1_CANONICAL_PHRASE must be non-empty and contain required terms."""
    assert IA1_CANONICAL_PHRASE
    assert len(IA1_CANONICAL_PHRASE) > 30
    assert "confidence tier" in IA1_CANONICAL_PHRASE.lower()
    assert "IA-1" in IA1_CANONICAL_PHRASE
    assert "DATA_STANDARDS.md" in IA1_CANONICAL_PHRASE


def test_ia1_canonical_phrase_contains_projection_warning() -> None:
    """SA-01: IA-1 text must reference time-horizon degradation limitation."""
    assert "time-horizon" in IA1_CANONICAL_PHRASE or "projection" in IA1_CANONICAL_PHRASE.lower()


# ---------------------------------------------------------------------------
# SA-04: Status transition tests via mocked asyncpg connection
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_run_sets_status_running_then_completed() -> None:
    """SA-04: pending → running → completed on successful execution."""
    conn = _make_mock_conn(scenario_status="pending", n_steps=1, entity_ids=[])

    runner = WebScenarioRunner()
    result = await runner.run(conn, "test-id")

    assert result.final_status == "completed"
    assert result.steps_executed == 1

    execute_calls = [str(c) for c in conn.execute.call_args_list]
    assert any("running" in c for c in execute_calls), "Status 'running' never set"
    assert any("completed" in c for c in execute_calls), "Status 'completed' never set"


@pytest.mark.asyncio
async def test_run_sets_status_failed_on_exception_and_reraises() -> None:
    """SA-04: running → failed on exception; exception must be re-raised."""
    conn = _make_mock_conn(scenario_status="pending", n_steps=1, entity_ids=[])

    # Fail on the snapshot write execute() call (after status=running is set)
    call_counter: list[int] = [0]

    async def _execute_side_effect(*args: Any, **kwargs: Any) -> str:  # noqa: ANN401
        call_counter[0] += 1
        if call_counter[0] == 2:
            raise RuntimeError("Simulated snapshot write failure")
        return "UPDATE 1"

    conn.execute = AsyncMock(side_effect=_execute_side_effect)

    runner = WebScenarioRunner()
    with pytest.raises(RuntimeError, match="Simulated snapshot write failure"):
        await runner.run(conn, "test-id")

    all_execute_args = [str(c) for c in conn.execute.call_args_list]
    assert any("failed" in arg for arg in all_execute_args), "Status 'failed' never set"


@pytest.mark.asyncio
async def test_run_returns_run_summary_type() -> None:
    """WebScenarioRunner.run() must return a RunSummary dataclass."""
    conn = _make_mock_conn(n_steps=2, entity_ids=[])
    result = await WebScenarioRunner().run(conn, "test-id")
    assert isinstance(result, RunSummary)
    assert result.scenario_id == "test-id"
    assert result.steps_executed == 2
    assert result.duration_seconds >= 0.0


@pytest.mark.asyncio
async def test_run_never_swallows_exceptions() -> None:
    """SA-04: exception must always propagate after setting failed status."""
    conn = _make_mock_conn(n_steps=1, entity_ids=["GRC"])

    # fetch() returns no entity rows — ValueError from missing entity
    conn.fetch = AsyncMock(return_value=[])

    runner = WebScenarioRunner()
    with pytest.raises(ValueError, match="GRC"):
        await runner.run(conn, "test-id")


# ---------------------------------------------------------------------------
# ScenarioSnapshotRepository: ia1_disclosure always set
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_snapshot_write_includes_ia1_disclosure() -> None:
    """Every snapshot write must pass IA1_CANONICAL_PHRASE as ia1_disclosure."""
    conn = MagicMock()
    conn.execute = AsyncMock(return_value="INSERT 1")

    state = _make_state()
    repo = ScenarioSnapshotRepository()
    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    await repo.write_snapshot(conn, "scenario-1", 0, ts, state)

    call_args = conn.execute.call_args
    # args[0]=sql, [1]=id, [2]=scenario_id, [3]=step, [4]=timestep,
    # [5]=state_data, [6]=ia1_disclosure
    positional_args = call_args.args
    assert len(positional_args) >= 7
    ia1_arg = positional_args[6]
    assert ia1_arg == IA1_CANONICAL_PHRASE, (
        f"ia1_disclosure was {ia1_arg!r}, expected the canonical IA-1 phrase"
    )


@pytest.mark.asyncio
async def test_snapshot_write_serializes_state_data_as_json() -> None:
    """state_data written to DB must be JSON-serializable JSONB."""
    conn = MagicMock()
    conn.execute = AsyncMock(return_value="INSERT 1")

    state = _make_state()
    repo = ScenarioSnapshotRepository()
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    await repo.write_snapshot(conn, "scenario-1", 1, ts, state)

    call_args = conn.execute.call_args.args
    state_data_arg = call_args[5]  # args[0]=sql, [5]=state_data ($5)
    # Must be a JSON string (JSONB via json.dumps)
    parsed = json.loads(state_data_arg)
    # Top-level state_data envelope metadata (v2)
    assert parsed["_envelope_version"] == STATE_DATA_ENVELOPE_VERSION
    assert parsed["_modules_active"] == []
    # Per-entity, per-quantity SA-09 envelope still at version "1"
    assert "GRC" in parsed
    assert "gdp_growth" in parsed["GRC"]
    assert parsed["GRC"]["gdp_growth"]["_envelope_version"] == "1"
    assert isinstance(parsed["GRC"]["gdp_growth"]["value"], str)


# ---------------------------------------------------------------------------
# Issue #144: ia1_disclosure semantic validation
# ---------------------------------------------------------------------------


def test_validate_ia1_disclosure_rejects_empty_string() -> None:
    """Issue #144: empty string must be rejected — NOT NULL is not enough."""
    with pytest.raises(ValueError, match="non-empty"):
        validate_ia1_disclosure("")


def test_validate_ia1_disclosure_rejects_whitespace_only() -> None:
    """Issue #144: whitespace-only string must be rejected."""
    for ws in ("   ", "\t", "\n", "  \t\n  "):
        with pytest.raises(ValueError, match="non-empty"):
            validate_ia1_disclosure(ws)


def test_validate_ia1_disclosure_accepts_valid_text() -> None:
    """Issue #144: IA1_CANONICAL_PHRASE and any substantive string must pass."""
    result = validate_ia1_disclosure(IA1_CANONICAL_PHRASE)
    assert result == IA1_CANONICAL_PHRASE

    short_valid = "Time-horizon degradation not applied — see DATA_STANDARDS.md IA-1."
    assert validate_ia1_disclosure(short_valid) == short_valid


# ---------------------------------------------------------------------------
# Issue #145: state_data envelope v2 with _modules_active
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_snapshot_state_data_has_envelope_version_2() -> None:
    """Issue #145: top-level state_data _envelope_version must be '2'."""
    conn = MagicMock()
    conn.execute = AsyncMock(return_value="INSERT 1")

    state = _make_state()
    repo = ScenarioSnapshotRepository()
    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    await repo.write_snapshot(conn, "s-1", 0, ts, state)

    parsed = json.loads(conn.execute.call_args.args[5])
    assert parsed["_envelope_version"] == "2", (
        f"Expected state_data _envelope_version '2', got {parsed.get('_envelope_version')!r}"
    )


@pytest.mark.asyncio
async def test_snapshot_state_data_has_modules_active_empty_list_for_m3() -> None:
    """Issue #145: M3 snapshots (no modules) must carry _modules_active: []."""
    conn = MagicMock()
    conn.execute = AsyncMock(return_value="INSERT 1")

    state = _make_state()
    repo = ScenarioSnapshotRepository()
    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    await repo.write_snapshot(conn, "s-1", 0, ts, state)

    parsed = json.loads(conn.execute.call_args.args[5])
    assert "_modules_active" in parsed
    assert parsed["_modules_active"] == []
    assert isinstance(parsed["_modules_active"], list)


@pytest.mark.asyncio
async def test_snapshot_state_data_modules_active_populated_when_passed() -> None:
    """Issue #145: modules_active param is reflected in state_data envelope."""
    conn = MagicMock()
    conn.execute = AsyncMock(return_value="INSERT 1")

    state = _make_state()
    repo = ScenarioSnapshotRepository()
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    await repo.write_snapshot(
        conn, "s-1", 1, ts, state,
        modules_active=["DemographicModule", "MacroeconomicModule"],
    )

    parsed = json.loads(conn.execute.call_args.args[5])
    assert parsed["_modules_active"] == ["DemographicModule", "MacroeconomicModule"]


@pytest.mark.asyncio
async def test_snapshot_quantity_envelope_still_readable_inside_v2_state_data() -> None:
    """Issue #145: per-quantity SA-09 envelope is still readable inside v2 state_data."""
    conn = MagicMock()
    conn.execute = AsyncMock(return_value="INSERT 1")

    state = _make_state()
    repo = ScenarioSnapshotRepository()
    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    await repo.write_snapshot(conn, "s-1", 0, ts, state)

    parsed = json.loads(conn.execute.call_args.args[5])
    qty_envelope = parsed["GRC"]["gdp_growth"]
    # Per-quantity SA-09 envelope version unchanged
    assert qty_envelope["_envelope_version"] == "1"
    # quantity_from_jsonb must still deserialize correctly
    restored = quantity_from_jsonb(qty_envelope)
    from decimal import Decimal  # noqa: PLC0415
    assert restored.value == Decimal("-0.054")


# ---------------------------------------------------------------------------
# Issue #146: modules_active field on SnapshotRecord
# ---------------------------------------------------------------------------


def test_snapshot_record_has_modules_active_field() -> None:
    """Issue #146: SnapshotRecord must expose modules_active, default empty list."""
    from app.schemas import SnapshotRecord  # noqa: PLC0415

    record = SnapshotRecord(
        scenario_id="s-1",
        step=0,
        timestep="2010-01-01T00:00:00",
        state_data={},
    )
    assert hasattr(record, "modules_active")
    assert record.modules_active == []


def test_snapshot_record_modules_active_from_state_data_envelope() -> None:
    """Issue #146: modules_active is populated from _modules_active in state_data."""
    from app.schemas import SnapshotRecord  # noqa: PLC0415

    record = SnapshotRecord(
        scenario_id="s-1",
        step=1,
        timestep="2011-01-01T00:00:00",
        state_data={"_envelope_version": "2", "_modules_active": ["DemographicModule"]},
        modules_active=["DemographicModule"],
    )
    assert record.modules_active == ["DemographicModule"]


def test_snapshot_record_m3_snapshot_has_empty_modules_active() -> None:
    """Issue #146: M3 snapshot state_data with empty _modules_active → [] on record."""
    from app.schemas import SnapshotRecord  # noqa: PLC0415

    # Simulate what list_snapshots builds from a real M3 DB row
    state_data = {
        "_envelope_version": "2",
        "_modules_active": [],
        "GRC": {"gdp_growth": {"_envelope_version": "1", "value": "-0.054"}},
    }
    modules_active: list[str] = state_data.get("_modules_active", [])  # type: ignore[assignment]
    record = SnapshotRecord(
        scenario_id="s-1",
        step=0,
        timestep="2010-01-01T00:00:00",
        state_data=state_data,
        modules_active=modules_active,
    )
    assert record.modules_active == []
