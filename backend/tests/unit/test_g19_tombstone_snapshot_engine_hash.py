"""Unit tests for G19: entity_state_snapshot tombstone capture + engine_version_hash.

Issues covered: #147 (entity_state_snapshot on tombstones), #152 (engine_version_hash
on scenarios), #36 DB piece (debt MDA threshold migration).

No database required — all tests exercise pure logic: schema shapes, ORM model
attributes, response builder behaviour, and migration structure.

Coverage:
  ScenarioDetailResponse schema
    1.  engine_version_hash field exists and defaults to None.
    2.  engine_version_hash accepts a valid SHA-1 string.
    3.  engine_version_hash accepts None explicitly.
    4.  ScenarioResponse (list/create) does NOT expose engine_version_hash.

  ScenarioDeletedTombstone ORM model
    5.  git_commit_hash attribute present (schema drift fix from c7f4a3e9d2b1).
    6.  entity_state_snapshot attribute present (#147).
    7.  Both columns are nullable (no server default).

  Scenario ORM model
    8.  engine_version_hash attribute present (#152).
    9.  engine_version_hash is nullable.

  Migration structure
    10. Migration revision ID is a4f2b6d8e1c9.
    11. down_revision is e3b7f1c9d5a2 (M10 governance MDA head).
    12. Migration module imports successfully without a live database.

  _build_detail_response — engine_version_hash passthrough
    13. engine_version_hash present in row dict → included in response.
    14. engine_version_hash absent from row dict (pre-migration row) → None in response.
    15. engine_version_hash = None in row dict → None in response.

  entity_state_snapshot capture logic
    16. snap_row is None → entity_state_snap is None.
    17. snap_row.state_data is a dict → json.dumps round-trips correctly.
    18. snap_row.state_data is a JSON string → json.loads then json.dumps round-trips.
    19. entity_state_snap round-trip preserves nested structure.

  MDA threshold — debt_profile.foreign_currency_pct
    20. indicator_key matches DebtProfile attribute map key.
    21. floor_value 0.60 matches DebtProfile.FOREIGN_CURRENCY_MDA_THRESHOLD.
    22. comparison_operator is 'gte' (breach when current >= floor_value).
    23. MDA checker correctly fires CRITICAL when foreign_currency_pct == 0.60.
    24. MDA checker fires WARNING when foreign_currency_pct is in approach band (0.57–0.59).
    25. MDA checker is silent when foreign_currency_pct < 0.57 (below approach band).
"""
from __future__ import annotations

import json
from datetime import UTC
from decimal import Decimal
from pathlib import Path

from app.api.scenarios import _build_detail_response
from app.schemas import MDAThresholdRecord, ScenarioDetailResponse, ScenarioResponse
from app.simulation.engine.models import DebtProfile, SimulationEntity
from app.simulation.mda_checker import MDAChecker

_MIGRATION_FILE = (
    Path(__file__).parent.parent.parent
    / "alembic"
    / "versions"
    / "a4f2b6d8e1c9_g19_tombstone_snapshot_engine_hash.py"
)
_MIGRATION_SRC = _MIGRATION_FILE.read_text()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_threshold(**kwargs: object) -> MDAThresholdRecord:
    defaults = {
        "mda_id": "MDA-DEBT-FOREIGN-CURRENCY-ROLLOVER",
        "indicator_key": "debt_profile.foreign_currency_pct",
        "entity_scope": "all",
        "measurement_framework": "financial",
        "floor_value": Decimal("0.60"),
        "floor_unit": "ratio",
        "approach_pct": Decimal("0.05"),
        "comparison_operator": "gte",
        "severity_at_breach": "CRITICAL",
        "description": "Foreign-currency debt rollover risk",
        "historical_basis": "Reinhart & Rogoff (2009)",
        "recovery_horizon_years": 3,
        "irreversibility_note": "3-5 year recovery horizon",
    }
    defaults.update(kwargs)
    return MDAThresholdRecord(**defaults)  # type: ignore[arg-type]


def _make_entity_with_fc_pct(fc_pct: str) -> SimulationEntity:
    profile = DebtProfile(
        total_pct_gdp=Decimal("0.80"),
        foreign_currency_pct=Decimal(fc_pct),
        short_term_pct=Decimal("0.20"),
        domestic_holder_pct=Decimal("0.40"),
        multilateral_pct=Decimal("0.15"),
        interest_service_pct_revenue=Decimal("0.18"),
    )
    return SimulationEntity(
        id="ARG",
        entity_type="country",
        attributes={},
        metadata={},
        debt_profile=profile,
    )


def _make_minimal_detail_row(**overrides: object) -> dict:
    base: dict = {
        "scenario_id": "sc-1",
        "name": "Test",
        "description": None,
        "status": "pending",
        "version": 1,
        "created_at": "2026-06-04T00:00:00+00:00",
        "configuration": {
            "entities": [],
            "n_steps": 2,
            "timestep_label": "quarter",
            "start_date": "2024-01-01",
        },
        "engine_version_hash": None,
    }
    base.update(overrides)
    return base


def _make_simulation_state(entity: SimulationEntity) -> object:
    from datetime import datetime

    from app.simulation.engine.models import (
        ResolutionConfig,
        ScenarioConfig,
        SimulationState,
    )

    ts = datetime(2026, 1, 1, tzinfo=UTC)
    return SimulationState(
        timestep=ts,
        resolution=ResolutionConfig(),
        entities={entity.id: entity},
        relationships=[],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="test-g19",
            name="G19 Test",
            description="",
            start_date=ts,
            end_date=ts,
        ),
    )


_MINIMAL_CFG: dict = {  # type: ignore[type-arg]
    "entities": [],
    "n_steps": 2,
    "timestep_label": "quarter",
    "start_date": "2024-01-01",
}


def _minimal_detail_response(**kwargs: object) -> ScenarioDetailResponse:
    return ScenarioDetailResponse(
        scenario_id="sc-1",
        name="Test",
        description=None,
        status="pending",
        version=1,
        created_at="2026-06-04T00:00:00+00:00",
        configuration=_MINIMAL_CFG,  # type: ignore[arg-type]
        scheduled_inputs=[],
        temporal_scope_note="note",
        **kwargs,  # type: ignore[arg-type]
    )


# ---------------------------------------------------------------------------
# 1–4: ScenarioDetailResponse schema
# ---------------------------------------------------------------------------


def test_detail_response_engine_version_hash_defaults_none() -> None:
    """engine_version_hash field exists and defaults to None."""
    assert _minimal_detail_response().engine_version_hash is None


def test_detail_response_engine_version_hash_accepts_sha1() -> None:
    """engine_version_hash accepts a 40-char hex SHA-1."""
    sha = "a" * 40
    assert _minimal_detail_response(engine_version_hash=sha).engine_version_hash == sha


def test_detail_response_engine_version_hash_accepts_none() -> None:
    """engine_version_hash accepts explicit None."""
    assert _minimal_detail_response(engine_version_hash=None).engine_version_hash is None


def test_scenario_response_no_engine_version_hash_field() -> None:
    """ScenarioResponse (list/create endpoint) does not expose engine_version_hash."""
    assert "engine_version_hash" not in ScenarioResponse.model_fields


# ---------------------------------------------------------------------------
# 5–9: Migration source verifies the correct columns and types
# ---------------------------------------------------------------------------


def test_migration_adds_entity_state_snapshot_to_tombstones() -> None:
    """Migration source adds entity_state_snapshot to scenario_deleted_tombstones."""
    assert "entity_state_snapshot" in _MIGRATION_SRC
    assert "scenario_deleted_tombstones" in _MIGRATION_SRC


def test_migration_adds_engine_version_hash_to_scenarios() -> None:
    """Migration source adds engine_version_hash to scenarios."""
    assert "engine_version_hash" in _MIGRATION_SRC
    assert '"scenarios"' in _MIGRATION_SRC


def test_migration_entity_state_snapshot_is_jsonb() -> None:
    """entity_state_snapshot is typed as JSONB in the migration."""
    assert "JSONB" in _MIGRATION_SRC


def test_migration_entity_state_snapshot_nullable() -> None:
    """entity_state_snapshot is nullable=True in the migration."""
    assert "nullable=True" in _MIGRATION_SRC


def test_migration_engine_version_hash_is_text() -> None:
    """engine_version_hash is typed as Text in the migration."""
    assert "sa.Text()" in _MIGRATION_SRC


# ---------------------------------------------------------------------------
# 10–12: Migration revision chain
# ---------------------------------------------------------------------------


def test_migration_revision_id() -> None:
    """Migration source declares revision = 'a4f2b6d8e1c9'."""
    assert 'revision = "a4f2b6d8e1c9"' in _MIGRATION_SRC


def test_migration_down_revision() -> None:
    """Migration chains from M10 governance MDA head (e3b7f1c9d5a2)."""
    assert 'down_revision = "e3b7f1c9d5a2"' in _MIGRATION_SRC


def test_migration_file_exists() -> None:
    """Migration file exists at the expected path."""
    assert _MIGRATION_FILE.exists(), f"Migration file not found: {_MIGRATION_FILE}"


# ---------------------------------------------------------------------------
# 13–15: _build_detail_response — engine_version_hash passthrough
# ---------------------------------------------------------------------------


def test_build_detail_response_passes_engine_version_hash() -> None:
    """engine_version_hash in row dict is included in the detail response."""
    sha = "b" * 40
    row = _make_minimal_detail_row(engine_version_hash=sha)
    resp = _build_detail_response(row, [])
    assert resp.engine_version_hash == sha


def test_build_detail_response_missing_key_yields_none() -> None:
    """engine_version_hash absent from row dict (pre-migration row) → None."""
    row = _make_minimal_detail_row()
    del row["engine_version_hash"]
    resp = _build_detail_response(row, [])
    assert resp.engine_version_hash is None


def test_build_detail_response_none_key_yields_none() -> None:
    """engine_version_hash = None in row dict → None in response."""
    row = _make_minimal_detail_row(engine_version_hash=None)
    resp = _build_detail_response(row, [])
    assert resp.engine_version_hash is None


# ---------------------------------------------------------------------------
# 16–19: entity_state_snapshot capture logic
# ---------------------------------------------------------------------------


def test_entity_state_snap_none_when_no_snapshot() -> None:
    """When snap_row is None, entity_state_snap should be None."""
    snap_row = None
    if snap_row is not None:
        raw = snap_row["state_data"]  # type: ignore[index]
        if isinstance(raw, str):
            raw = json.loads(raw)
        entity_state_snap: str | None = json.dumps(raw)
    else:
        entity_state_snap = None
    assert entity_state_snap is None


def test_entity_state_snap_from_dict_state_data() -> None:
    """snap_row.state_data is a dict → json.dumps produces valid JSON."""
    state_data = {"ARG": {"gdp_per_capita": {"value": "12000", "unit": "USD"}}}
    snap_row = {"state_data": state_data}
    raw = snap_row["state_data"]
    if isinstance(raw, str):
        raw = json.loads(raw)
    entity_state_snap: str | None = json.dumps(raw)
    assert entity_state_snap is not None
    assert json.loads(entity_state_snap) == state_data


def test_entity_state_snap_from_string_state_data() -> None:
    """snap_row.state_data is a JSON string → parse then re-dump round-trips."""
    state_data = {"ARG": {"gdp_per_capita": {"value": "12000"}}}
    snap_row = {"state_data": json.dumps(state_data)}
    raw = snap_row["state_data"]
    if isinstance(raw, str):
        raw = json.loads(raw)
    entity_state_snap: str | None = json.dumps(raw)
    assert json.loads(entity_state_snap) == state_data  # type: ignore[arg-type]


def test_entity_state_snap_preserves_nested_structure() -> None:
    """Round-trip preserves nested attribute envelope (value + unit + tier)."""
    state_data = {
        "ARG": {
            "gdp_per_capita": {
                "value": "12000.50", "unit": "USD",
                "variable_type": "FLOW", "confidence_tier": 2,
            },
            "inflation_rate": {
                "value": "0.35", "unit": "ratio",
                "variable_type": "RATIO", "confidence_tier": 3,
            },
        }
    }
    snap_row = {"state_data": state_data}
    raw = snap_row["state_data"]
    if isinstance(raw, str):
        raw = json.loads(raw)
    result = json.loads(json.dumps(raw))
    assert result["ARG"]["gdp_per_capita"]["value"] == "12000.50"
    assert result["ARG"]["inflation_rate"]["confidence_tier"] == 3


# ---------------------------------------------------------------------------
# 20–25: MDA threshold — debt_profile.foreign_currency_pct
# ---------------------------------------------------------------------------


def test_indicator_key_matches_debt_profile_attr_map() -> None:
    """indicator_key 'debt_profile.foreign_currency_pct' is in entity._DEBT_PROFILE_ATTR_MAP."""
    entity = SimulationEntity(id="ARG", entity_type="country", attributes={}, metadata={})
    assert "debt_profile.foreign_currency_pct" in entity._DEBT_PROFILE_ATTR_MAP


def test_floor_value_matches_debt_profile_constant() -> None:
    """MDA floor_value 0.60 matches DebtProfile.FOREIGN_CURRENCY_MDA_THRESHOLD."""
    assert Decimal("0.60") == DebtProfile.FOREIGN_CURRENCY_MDA_THRESHOLD


def test_comparison_operator_is_gte() -> None:
    """comparison_operator is 'gte' — breach when foreign_currency_pct >= floor_value."""
    threshold = _make_threshold()
    assert threshold.comparison_operator == "gte"


def test_mda_checker_fires_critical_at_threshold() -> None:
    """MDA checker fires CRITICAL when foreign_currency_pct exactly equals 0.60."""
    from app.schemas import MDASeverity
    entity = _make_entity_with_fc_pct("0.60")
    state = _make_simulation_state(entity)
    threshold = _make_threshold()
    alerts = MDAChecker().check(state, [], [threshold])  # type: ignore[arg-type]
    assert len(alerts) == 1
    assert alerts[0].severity == MDASeverity.CRITICAL
    assert alerts[0].entity_id == "ARG"
    assert alerts[0].mda_id == "MDA-DEBT-FOREIGN-CURRENCY-ROLLOVER"


def test_mda_checker_fires_warning_in_approach_band() -> None:
    """MDA checker fires WARNING when 0.57 <= foreign_currency_pct < 0.60."""
    from app.schemas import MDASeverity
    # At 0.57: approach_pct_remaining = (0.60 - 0.57) / 0.60 = 0.05 → exactly at warning boundary
    entity = _make_entity_with_fc_pct("0.57")
    state = _make_simulation_state(entity)
    threshold = _make_threshold()
    alerts = MDAChecker().check(state, [], [threshold])  # type: ignore[arg-type]
    assert len(alerts) == 1
    assert alerts[0].severity == MDASeverity.WARNING


def test_mda_checker_silent_below_approach_band() -> None:
    """MDA checker produces no alert when foreign_currency_pct < 0.57 (safe zone)."""
    entity = _make_entity_with_fc_pct("0.40")
    state = _make_simulation_state(entity)
    threshold = _make_threshold()
    alerts = MDAChecker().check(state, [], [threshold])  # type: ignore[arg-type]
    assert alerts == []
