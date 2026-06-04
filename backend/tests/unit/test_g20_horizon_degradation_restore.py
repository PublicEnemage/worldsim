"""Unit tests for G20: horizon degradation envelope + fidelity artifact + restore endpoint.

Issues covered: #151 (_steps_projected horizon metadata), #154 (write_fidelity_artifact),
#155 (POST /scenarios/restore).

No database required — all tests exercise pure logic: schema shapes, serialization
behaviour, artifact writing, and restore endpoint logic via mocked asyncpg connections.

Coverage:
  STATE_DATA_ENVELOPE_VERSION = "3"  (quantity_serde)
    1.  STATE_DATA_ENVELOPE_VERSION is exactly "3".
    2.  Version string is a digit string, not an integer.

  _serialize_state / _steps_projected  (snapshot_repository)
    3.  step=0 → _steps_projected == 0 in serialized envelope.
    4.  step=3 → _steps_projected == 3 in serialized envelope.
    5.  _steps_projected is an int in the serialized dict.
    6.  _steps_projected is present alongside _modules_active and _envelope_version.

  write_snapshot — _steps_projected passed through
    7.  write_snapshot(step=2) stores _steps_projected=2 in the JSON written to DB.
    8.  write_snapshot(step=0) stores _steps_projected=0 in the JSON written to DB.

  IA1_CANONICAL_PHRASE horizon degradation extension  (quantity_serde)
    9.  IA1_CANONICAL_PHRASE contains "Horizon degradation schedule".
    10. IA1_CANONICAL_PHRASE contains "_steps_projected".
    11. IA1_CANONICAL_PHRASE contains "Tier 5".
    12. IA1_DISCLOSURE in greece fixtures equals IA1_CANONICAL_PHRASE exactly.

  write_fidelity_artifact  (fidelity_report)
    13. Artifact file is created at the correct path pattern.
    14. Artifact JSON is valid and includes required top-level keys.
    15. overall is "PASS" when all thresholds pass.
    16. overall is "FAIL" when any threshold fails.
    17. deferred_thresholds appear in results with passed=None.
    18. results list includes one entry per threshold.
    19. engine_version defaults to "0.3.0".
    20. engine_version can be overridden.
    21. commit_sha is a non-empty string.
    22. run_date is a valid YYYY-MM-DD date string.
    23. Artifact filename follows {case_id}-{date}-{sha8}.json pattern.

  ScenarioRestoreRequest / ScenarioRestoreResponse  (schemas)
    24. ScenarioRestoreRequest has tombstone_id field.
    25. ScenarioRestoreResponse has scenario_id, name, status, restored_from_tombstone_id.
    26. ScenarioRestoreResponse.status is always "pending" in a real restore.

  restore_scenario endpoint logic  (api/scenarios)
    27. 404 raised when tombstone_id not found.
    28. Version match passes; restored scenario returned with status="pending".
    29. Name conflict → restored name is "{original} (restored)".
    30. No name conflict → restored name equals original name.
    31. Version mismatch raises 409.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.schemas import ScenarioRestoreRequest, ScenarioRestoreResponse
from app.simulation.repositories.quantity_serde import (
    IA1_CANONICAL_PHRASE,
    STATE_DATA_ENVELOPE_VERSION,
)
from app.simulation.repositories.snapshot_repository import (
    ScenarioSnapshotRepository,
    _serialize_state,
)
from tests.backtesting.fidelity_report import write_fidelity_artifact
from tests.fixtures.greece_2010_2012_actuals import IA1_DISCLOSURE

# ---------------------------------------------------------------------------
# Helpers shared across tests
# ---------------------------------------------------------------------------


def _make_minimal_state() -> object:
    """Return a SimulationState with one entity and one attribute."""
    from app.simulation.engine.models import (  # noqa: PLC0415
        ResolutionConfig,
        ScenarioConfig,
        SimulationEntity,
        SimulationState,
    )
    from app.simulation.engine.quantity import Quantity, VariableType  # noqa: PLC0415

    qty = Quantity(
        value=Decimal("-0.054"),
        unit="ratio",
        variable_type=VariableType.RATIO,
        confidence_tier=2,
    )
    entity = SimulationEntity(
        id="GRC",
        entity_type="country",
        attributes={"gdp_growth": qty},
        metadata={},
    )
    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    end = datetime(2016, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    return SimulationState(
        timestep=ts,
        resolution=ResolutionConfig(),
        entities={"GRC": entity},
        relationships=[],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="test-id",
            name="Test",
            description="",
            start_date=ts,
            end_date=end,
        ),
    )


# ---------------------------------------------------------------------------
# STATE_DATA_ENVELOPE_VERSION = "3"
# ---------------------------------------------------------------------------


def test_state_data_envelope_version_is_three() -> None:
    """Test 1: STATE_DATA_ENVELOPE_VERSION must be exactly '3'."""
    assert STATE_DATA_ENVELOPE_VERSION == "3"


def test_state_data_envelope_version_is_string() -> None:
    """Test 2: version is a str digit, not an int."""
    assert isinstance(STATE_DATA_ENVELOPE_VERSION, str)


# ---------------------------------------------------------------------------
# _serialize_state / _steps_projected
# ---------------------------------------------------------------------------


def test_serialize_state_step0_has_steps_projected_zero() -> None:
    """Test 3: step=0 → _steps_projected == 0."""
    state = _make_minimal_state()
    result = _serialize_state(state, [], steps_projected=0)  # type: ignore[arg-type]
    assert result["_steps_projected"] == 0


def test_serialize_state_step3_has_steps_projected_three() -> None:
    """Test 4: step=3 → _steps_projected == 3."""
    state = _make_minimal_state()
    result = _serialize_state(state, [], steps_projected=3)  # type: ignore[arg-type]
    assert result["_steps_projected"] == 3


def test_serialize_state_steps_projected_is_int() -> None:
    """Test 5: _steps_projected value is an int in the serialized dict."""
    state = _make_minimal_state()
    result = _serialize_state(state, [], steps_projected=2)  # type: ignore[arg-type]
    assert isinstance(result["_steps_projected"], int)


def test_serialize_state_has_all_envelope_keys() -> None:
    """Test 6: _steps_projected is present alongside _modules_active and _envelope_version."""
    state = _make_minimal_state()
    result = _serialize_state(state, ["MacroeconomicModule"], steps_projected=1)  # type: ignore[arg-type]
    assert "_envelope_version" in result
    assert "_modules_active" in result
    assert "_steps_projected" in result
    assert result["_envelope_version"] == "3"
    assert result["_modules_active"] == ["MacroeconomicModule"]
    assert result["_steps_projected"] == 1


# ---------------------------------------------------------------------------
# write_snapshot — _steps_projected passthrough
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_write_snapshot_step2_sets_steps_projected_2() -> None:
    """Test 7: write_snapshot(step=2) stores _steps_projected=2 in JSON."""
    conn = MagicMock()
    conn.execute = AsyncMock(return_value="INSERT 1")

    state = _make_minimal_state()
    repo = ScenarioSnapshotRepository()
    ts = datetime(2012, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    await repo.write_snapshot(conn, "s-1", 2, ts, state)  # type: ignore[arg-type]

    state_data_arg = conn.execute.call_args.args[5]
    parsed = json.loads(state_data_arg)
    assert parsed["_steps_projected"] == 2


@pytest.mark.asyncio
async def test_write_snapshot_step0_sets_steps_projected_0() -> None:
    """Test 8: write_snapshot(step=0) stores _steps_projected=0 in JSON."""
    conn = MagicMock()
    conn.execute = AsyncMock(return_value="INSERT 1")

    state = _make_minimal_state()
    repo = ScenarioSnapshotRepository()
    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    await repo.write_snapshot(conn, "s-1", 0, ts, state)  # type: ignore[arg-type]

    parsed = json.loads(conn.execute.call_args.args[5])
    assert parsed["_steps_projected"] == 0


# ---------------------------------------------------------------------------
# IA1_CANONICAL_PHRASE horizon degradation extension
# ---------------------------------------------------------------------------


def test_ia1_canonical_phrase_contains_horizon_degradation() -> None:
    """Test 9: IA1_CANONICAL_PHRASE contains 'Horizon degradation schedule'."""
    assert "Horizon degradation schedule" in IA1_CANONICAL_PHRASE


def test_ia1_canonical_phrase_contains_steps_projected() -> None:
    """Test 10: IA1_CANONICAL_PHRASE references _steps_projected field."""
    assert "_steps_projected" in IA1_CANONICAL_PHRASE


def test_ia1_canonical_phrase_contains_tier_5_cap() -> None:
    """Test 11: IA1_CANONICAL_PHRASE references Tier 5 cap."""
    assert "Tier 5" in IA1_CANONICAL_PHRASE


def test_ia1_disclosure_matches_canonical_phrase_exactly() -> None:
    """Test 12: IA1_DISCLOSURE in greece fixtures equals IA1_CANONICAL_PHRASE exactly."""
    assert IA1_DISCLOSURE == IA1_CANONICAL_PHRASE


# ---------------------------------------------------------------------------
# write_fidelity_artifact
# ---------------------------------------------------------------------------


def _run_write_artifact(
    case_id: str = "test_case",
    thresholds: dict[str, bool] | None = None,
    deferred: dict[str, str] | None = None,
    engine_version: str = "0.3.0",
    reports_dir: Path | None = None,
) -> tuple[Path, dict]:
    """Helper: run write_fidelity_artifact, return (path, parsed_json)."""
    if thresholds is None:
        thresholds = {"threshold_a": True, "threshold_b": True}

    with patch(
        "tests.backtesting.fidelity_report._resolve_commit_sha",
        return_value="abc1234567890",
    ):
        if reports_dir is not None:
            with patch(
                "tests.backtesting.fidelity_report.Path.__new__",
                side_effect=lambda cls, *a, **kw: Path(*a, **kw),
            ):
                artifact_path = write_fidelity_artifact(
                    case_id=case_id,
                    thresholds_met=thresholds,
                    engine_version=engine_version,
                    deferred_thresholds=deferred,
                )
        else:
            artifact_path = write_fidelity_artifact(
                case_id=case_id,
                thresholds_met=thresholds,
                engine_version=engine_version,
                deferred_thresholds=deferred,
            )
    return artifact_path, json.loads(artifact_path.read_text())


def test_write_fidelity_artifact_creates_file() -> None:
    """Test 13: artifact file is created at the expected path."""
    with patch(
        "tests.backtesting.fidelity_report._resolve_commit_sha",
        return_value="deadbeef12345678",
    ):
        path = write_fidelity_artifact(
            case_id="greece_test",
            thresholds_met={"t1": True},
        )
    assert path.exists()
    assert path.suffix == ".json"
    path.unlink(missing_ok=True)


def test_write_fidelity_artifact_has_required_keys() -> None:
    """Test 14: artifact JSON includes all required top-level keys."""
    with patch(
        "tests.backtesting.fidelity_report._resolve_commit_sha",
        return_value="abc12345",
    ):
        path = write_fidelity_artifact(
            case_id="test_keys",
            thresholds_met={"t1": True},
        )
    data = json.loads(path.read_text())
    path.unlink(missing_ok=True)
    required_keys = {
        "case_id", "run_date", "commit_sha", "engine_version",
        "thresholds", "results", "overall",
    }
    assert required_keys.issubset(data.keys())


def test_write_fidelity_artifact_overall_pass_when_all_pass() -> None:
    """Test 15: overall is 'PASS' when all thresholds are True."""
    with patch(
        "tests.backtesting.fidelity_report._resolve_commit_sha",
        return_value="abc12345",
    ):
        path = write_fidelity_artifact(
            case_id="test_pass",
            thresholds_met={"t1": True, "t2": True},
        )
    data = json.loads(path.read_text())
    path.unlink(missing_ok=True)
    assert data["overall"] == "PASS"


def test_write_fidelity_artifact_overall_fail_when_any_fails() -> None:
    """Test 16: overall is 'FAIL' when any threshold is False."""
    with patch(
        "tests.backtesting.fidelity_report._resolve_commit_sha",
        return_value="abc12345",
    ):
        path = write_fidelity_artifact(
            case_id="test_fail",
            thresholds_met={"t1": True, "t2": False},
        )
    data = json.loads(path.read_text())
    path.unlink(missing_ok=True)
    assert data["overall"] == "FAIL"


def test_write_fidelity_artifact_deferred_thresholds_in_results() -> None:
    """Test 17: deferred thresholds appear in results with passed=None."""
    with patch(
        "tests.backtesting.fidelity_report._resolve_commit_sha",
        return_value="abc12345",
    ):
        path = write_fidelity_artifact(
            case_id="test_deferred",
            thresholds_met={"t1": True},
            deferred_thresholds={"deferred_t": "FAIL — no module (Issue #87)"},
        )
    data = json.loads(path.read_text())
    path.unlink(missing_ok=True)
    deferred_results = [r for r in data["results"] if r["threshold_id"] == "deferred_t"]
    assert len(deferred_results) == 1
    assert deferred_results[0]["passed"] is None
    assert "DEFERRED" in deferred_results[0]["note"]


def test_write_fidelity_artifact_results_count_matches_thresholds() -> None:
    """Test 18: results list has one entry per threshold key."""
    thresholds = {"a": True, "b": False, "c": True}
    with patch(
        "tests.backtesting.fidelity_report._resolve_commit_sha",
        return_value="abc12345",
    ):
        path = write_fidelity_artifact(
            case_id="test_count",
            thresholds_met=thresholds,
        )
    data = json.loads(path.read_text())
    path.unlink(missing_ok=True)
    blocking_results = [r for r in data["results"] if r["passed"] is not None]
    assert len(blocking_results) == len(thresholds)


def test_write_fidelity_artifact_default_engine_version() -> None:
    """Test 19: engine_version defaults to '0.3.0'."""
    with patch(
        "tests.backtesting.fidelity_report._resolve_commit_sha",
        return_value="abc12345",
    ):
        path = write_fidelity_artifact(
            case_id="test_ver_default",
            thresholds_met={"t1": True},
        )
    data = json.loads(path.read_text())
    path.unlink(missing_ok=True)
    assert data["engine_version"] == "0.3.0"


def test_write_fidelity_artifact_custom_engine_version() -> None:
    """Test 20: engine_version can be overridden."""
    with patch(
        "tests.backtesting.fidelity_report._resolve_commit_sha",
        return_value="abc12345",
    ):
        path = write_fidelity_artifact(
            case_id="test_ver_custom",
            thresholds_met={"t1": True},
            engine_version="1.2.3",
        )
    data = json.loads(path.read_text())
    path.unlink(missing_ok=True)
    assert data["engine_version"] == "1.2.3"


def test_write_fidelity_artifact_commit_sha_non_empty() -> None:
    """Test 21: commit_sha is a non-empty string."""
    with patch(
        "tests.backtesting.fidelity_report._resolve_commit_sha",
        return_value="abcdef1234567890",
    ):
        path = write_fidelity_artifact(
            case_id="test_sha",
            thresholds_met={"t1": True},
        )
    data = json.loads(path.read_text())
    path.unlink(missing_ok=True)
    assert isinstance(data["commit_sha"], str)
    assert len(data["commit_sha"]) > 0


def test_write_fidelity_artifact_run_date_format() -> None:
    """Test 22: run_date is a valid YYYY-MM-DD date string."""
    with patch(
        "tests.backtesting.fidelity_report._resolve_commit_sha",
        return_value="abc12345",
    ):
        path = write_fidelity_artifact(
            case_id="test_date",
            thresholds_met={"t1": True},
        )
    data = json.loads(path.read_text())
    path.unlink(missing_ok=True)
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", data["run_date"])


def test_write_fidelity_artifact_filename_pattern() -> None:
    """Test 23: filename follows {case_id}-{date}-{sha8}.json pattern."""
    with patch(
        "tests.backtesting.fidelity_report._resolve_commit_sha",
        return_value="deadbeef12345678",
    ):
        path = write_fidelity_artifact(
            case_id="greece_2010_2015",
            thresholds_met={"t1": True},
        )
    path.unlink(missing_ok=True)
    assert path.stem.startswith("greece_2010_2015-")
    parts = path.stem.split("-")
    assert len(parts) >= 3
    sha8_part = parts[-1]
    assert sha8_part == "deadbeef"


# ---------------------------------------------------------------------------
# ScenarioRestoreRequest / ScenarioRestoreResponse schemas
# ---------------------------------------------------------------------------


def test_restore_request_has_tombstone_id_field() -> None:
    """Test 24: ScenarioRestoreRequest has tombstone_id field."""
    req = ScenarioRestoreRequest(tombstone_id="abc-123")
    assert req.tombstone_id == "abc-123"


def test_restore_response_has_all_fields() -> None:
    """Test 25: ScenarioRestoreResponse has the four required fields."""
    resp = ScenarioRestoreResponse(
        scenario_id="new-id",
        name="Greece (restored)",
        status="pending",
        restored_from_tombstone_id="old-id",
    )
    assert resp.scenario_id == "new-id"
    assert resp.name == "Greece (restored)"
    assert resp.status == "pending"
    assert resp.restored_from_tombstone_id == "old-id"


def test_restore_response_status_is_pending() -> None:
    """Test 26: status value in a valid restore response is 'pending'."""
    resp = ScenarioRestoreResponse(
        scenario_id="x",
        name="y",
        status="pending",
        restored_from_tombstone_id="z",
    )
    assert resp.status == "pending"


# ---------------------------------------------------------------------------
# restore_scenario endpoint logic
# ---------------------------------------------------------------------------


def _make_tombstone_row(
    *,
    name: str = "Greece 2010",
    engine_version: str = "0.3.0",
    git_commit_hash: str | None = None,
) -> dict:
    return {
        "scenario_id": "tombstone-id-1",
        "name": name,
        "configuration": json.dumps({
            "n_steps": 3, "entities": ["GRC"],
            "timestep_label": "annual", "initial_attributes": {},
        }),
        "scheduled_inputs": json.dumps([]),
        "engine_version": engine_version,
        "git_commit_hash": git_commit_hash,
    }


@pytest.mark.asyncio
async def test_restore_scenario_404_when_tombstone_not_found() -> None:
    """Test 27: 404 raised when tombstone_id not found."""
    from fastapi import HTTPException  # noqa: PLC0415

    from app.api.scenarios import restore_scenario  # noqa: PLC0415

    conn = MagicMock()
    conn.fetchrow = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await restore_scenario(ScenarioRestoreRequest(tombstone_id="missing-id"), conn)

    assert exc_info.value.status_code == 404
    assert "missing-id" in exc_info.value.detail


@pytest.mark.asyncio
async def test_restore_scenario_returns_pending_scenario() -> None:
    """Test 28: successful restore returns ScenarioRestoreResponse with status='pending'."""
    from app.api.scenarios import _ENGINE_VERSION, restore_scenario  # noqa: PLC0415

    conn = MagicMock()
    tombstone = _make_tombstone_row(engine_version=_ENGINE_VERSION)
    conn.fetchrow = AsyncMock(return_value=tombstone)
    conn.fetchval = AsyncMock(return_value=None)  # no name conflict
    conn.execute = AsyncMock(return_value="INSERT 1")

    class _FakeTx:
        async def __aenter__(self) -> _FakeTx:
            return self

        async def __aexit__(self, *args: object) -> None:
            pass

    conn.transaction = MagicMock(return_value=_FakeTx())

    result = await restore_scenario(ScenarioRestoreRequest(tombstone_id="tombstone-id-1"), conn)

    assert isinstance(result, ScenarioRestoreResponse)
    assert result.status == "pending"
    assert result.restored_from_tombstone_id == "tombstone-id-1"
    assert result.name == "Greece 2010"


@pytest.mark.asyncio
async def test_restore_scenario_name_conflict_appends_restored() -> None:
    """Test 29: when original name is taken, restored name is '{original} (restored)'."""
    from app.api.scenarios import _ENGINE_VERSION, restore_scenario  # noqa: PLC0415

    conn = MagicMock()
    tombstone = _make_tombstone_row(name="Greece 2010", engine_version=_ENGINE_VERSION)
    conn.fetchrow = AsyncMock(return_value=tombstone)
    conn.fetchval = AsyncMock(return_value=1)  # name conflict exists
    conn.execute = AsyncMock(return_value="INSERT 1")

    class _FakeTx:
        async def __aenter__(self) -> _FakeTx:
            return self

        async def __aexit__(self, *args: object) -> None:
            pass

    conn.transaction = MagicMock(return_value=_FakeTx())

    result = await restore_scenario(ScenarioRestoreRequest(tombstone_id="tombstone-id-1"), conn)

    assert result.name == "Greece 2010 (restored)"


@pytest.mark.asyncio
async def test_restore_scenario_no_conflict_uses_original_name() -> None:
    """Test 30: when original name is not taken, restored name equals original."""
    from app.api.scenarios import _ENGINE_VERSION, restore_scenario  # noqa: PLC0415

    conn = MagicMock()
    tombstone = _make_tombstone_row(name="Unique Name", engine_version=_ENGINE_VERSION)
    conn.fetchrow = AsyncMock(return_value=tombstone)
    conn.fetchval = AsyncMock(return_value=None)  # no conflict
    conn.execute = AsyncMock(return_value="INSERT 1")

    class _FakeTx:
        async def __aenter__(self) -> _FakeTx:
            return self

        async def __aexit__(self, *args: object) -> None:
            pass

    conn.transaction = MagicMock(return_value=_FakeTx())

    result = await restore_scenario(ScenarioRestoreRequest(tombstone_id="tombstone-id-1"), conn)

    assert result.name == "Unique Name"


@pytest.mark.asyncio
async def test_restore_scenario_version_mismatch_raises_409() -> None:
    """Test 31: version mismatch raises HTTPException 409."""
    from fastapi import HTTPException  # noqa: PLC0415

    from app.api.scenarios import restore_scenario  # noqa: PLC0415

    conn = MagicMock()
    tombstone = _make_tombstone_row(engine_version="0.1.0")  # mismatched version
    conn.fetchrow = AsyncMock(return_value=tombstone)

    with pytest.raises(HTTPException) as exc_info:
        await restore_scenario(ScenarioRestoreRequest(tombstone_id="tombstone-id-1"), conn)

    assert exc_info.value.status_code == 409
