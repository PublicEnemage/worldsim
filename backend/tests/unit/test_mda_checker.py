"""Unit tests for MDAChecker — ADR-005 Decision 3.

Coverage:
  1. No alert when indicator value is safely above floor and approach threshold.
  2. WARNING fires when within approach_pct of floor (above floor).
  3. CRITICAL fires on first step at or below floor.
  4. TERMINAL fires when prior snapshot also had a breach for the same pair.
  5. Entity scope 'all' treated as '*' (matches all entity IDs).
  6. fnmatch glob pattern restricts to matching entity IDs only.
  7. Missing indicator on entity is silently skipped (no alert).
  8. Multiple thresholds produce one alert per triggered (entity, threshold) pair.
  9. alerts_to_events_snapshot encodes event_id deterministically.
  10. alerts_from_events_snapshot reconstructs MDAAlert list from stored events.
  11. alerts_from_events_snapshot entity_id filter narrows results.
  12. MDAThresholdRecord coerces Decimal floor_value and approach_pct to str.
  13. _build_prior_counts ignores non-mda_breach event types.
  14. approach_pct_remaining is negative (4 d.p.) when value is below floor.
  15. TERMINAL consecutive_breach_steps increments beyond 2 using prior count.
"""
from __future__ import annotations

from datetime import timezone
from decimal import Decimal

from app.schemas import MDAAlert, MDASeverity, MDAThresholdRecord
from app.simulation.mda_checker import (
    MDAChecker,
    _build_prior_counts,
    alerts_from_events_snapshot,
    alerts_to_events_snapshot,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _threshold(
    mda_id: str = "MDA-TEST",
    indicator_key: str = "reserve_coverage_months",
    entity_scope: str = "all",
    floor_value: str = "2.5",
    approach_pct: str = "0.20",
    measurement_framework: str = "financial",
) -> MDAThresholdRecord:
    return MDAThresholdRecord(
        mda_id=mda_id,
        indicator_key=indicator_key,
        entity_scope=entity_scope,
        measurement_framework=measurement_framework,
        floor_value=floor_value,
        floor_unit="months",
        approach_pct=approach_pct,
        severity_at_breach="CRITICAL",
        description="Test threshold.",
        historical_basis="Unit test.",
        recovery_horizon_years=None,
        irreversibility_note="Test irreversibility note.",
    )


def _state_with_entity(
    entity_id: str = "GRC",
    attrs: dict[str, Decimal] | None = None,
) -> object:
    """Build a minimal SimulationState-like object for MDAChecker.check()."""
    from datetime import datetime

    from app.simulation.engine.models import (
        ResolutionConfig,
        ScenarioConfig,
        SimulationEntity,
        SimulationState,
    )
    from app.simulation.engine.quantity import Quantity, VariableType

    attr_map = {}
    for key, val in (attrs or {}).items():
        attr_map[key] = Quantity(
            value=val,
            unit="months",
            variable_type=VariableType.STOCK,
            measurement_framework=None,
            confidence_tier=3,
        )

    entity = SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes=attr_map,
        metadata={},
    )
    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    return SimulationState(
        timestep=ts,
        resolution=ResolutionConfig(),
        entities={entity_id: entity},
        relationships=[],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="test-sid",
            name="Test",
            description="",
            start_date=ts,
            end_date=ts,
        ),
    )


# ---------------------------------------------------------------------------
# Test: no alert when safely above floor
# ---------------------------------------------------------------------------


def test_no_alert_when_safely_above_floor() -> None:
    state = _state_with_entity("GRC", {"reserve_coverage_months": Decimal("4.0")})
    threshold = _threshold(floor_value="2.5", approach_pct="0.20")
    alerts = MDAChecker().check(state, [], [threshold])
    assert alerts == []


# ---------------------------------------------------------------------------
# Test: WARNING when within approach_pct of floor but above it
# ---------------------------------------------------------------------------


def test_warning_within_approach_pct() -> None:
    # floor=2.5, approach_pct=0.20 → warning fires when value <= 3.0 AND value > 2.5
    # value=2.8 → (2.8-2.5)/2.5 = 0.12 → within 0.20
    state = _state_with_entity("GRC", {"reserve_coverage_months": Decimal("2.8")})
    threshold = _threshold(floor_value="2.5", approach_pct="0.20")
    alerts = MDAChecker().check(state, [], [threshold])
    assert len(alerts) == 1
    alert = alerts[0]
    assert alert.severity == MDASeverity.WARNING
    assert alert.consecutive_breach_steps == 0
    assert Decimal(alert.approach_pct_remaining) > Decimal("0")


# ---------------------------------------------------------------------------
# Test: CRITICAL on first breach (at or below floor)
# ---------------------------------------------------------------------------


def test_critical_on_first_breach() -> None:
    state = _state_with_entity("GRC", {"reserve_coverage_months": Decimal("2.0")})
    threshold = _threshold(floor_value="2.5", approach_pct="0.20")
    alerts = MDAChecker().check(state, [], [threshold])
    assert len(alerts) == 1
    alert = alerts[0]
    assert alert.severity == MDASeverity.CRITICAL
    assert alert.consecutive_breach_steps == 1
    assert Decimal(alert.approach_pct_remaining) < Decimal("0")


# ---------------------------------------------------------------------------
# Test: TERMINAL on consecutive breach (prior events present)
# ---------------------------------------------------------------------------


def test_terminal_on_consecutive_breach() -> None:
    state = _state_with_entity("GRC", {"reserve_coverage_months": Decimal("2.0")})
    threshold = _threshold(mda_id="MDA-FIN-RESERVES", floor_value="2.5", approach_pct="0.20")
    prior_events = [
        {
            "event_type": "mda_breach",
            "mda_id": "MDA-FIN-RESERVES",
            "entity_id": "GRC",
            "consecutive_breach_steps": 1,
        }
    ]
    alerts = MDAChecker().check(state, prior_events, [threshold])
    assert len(alerts) == 1
    alert = alerts[0]
    assert alert.severity == MDASeverity.TERMINAL
    assert alert.consecutive_breach_steps == 2


# ---------------------------------------------------------------------------
# Test: entity scope 'all' treated as '*'
# ---------------------------------------------------------------------------


def test_entity_scope_all_matches_any_entity_id() -> None:
    state = _state_with_entity("THA", {"reserve_coverage_months": Decimal("2.0")})
    threshold = _threshold(entity_scope="all", floor_value="2.5")
    alerts = MDAChecker().check(state, [], [threshold])
    assert len(alerts) == 1
    assert alerts[0].entity_id == "THA"


# ---------------------------------------------------------------------------
# Test: fnmatch glob restricts to matching entity IDs
# ---------------------------------------------------------------------------


def test_glob_scope_filters_non_matching_entities() -> None:
    state = _state_with_entity("GRC", {"poverty_headcount_ratio": Decimal("0.50")})
    # Cohort scope — GRC does not match *:CHT:1-*-*
    threshold = _threshold(
        indicator_key="poverty_headcount_ratio",
        entity_scope="*:CHT:1-*-*",
        floor_value="0.40",
        approach_pct="0.15",
    )
    alerts = MDAChecker().check(state, [], [threshold])
    assert alerts == []


def test_glob_scope_matches_cohort_entity_id() -> None:
    from datetime import datetime

    from app.simulation.engine.models import (
        ResolutionConfig,
        ScenarioConfig,
        SimulationEntity,
        SimulationState,
    )
    from app.simulation.engine.quantity import Quantity, VariableType

    cohort_id = "GRC:CHT:1-25-64-FORMAL"
    qty = Quantity(
        value=Decimal("0.38"),  # below floor=0.40 → CRITICAL
        unit="ratio",
        variable_type=VariableType.RATIO,
        measurement_framework=None,
        confidence_tier=3,
    )
    entity = SimulationEntity(
        id=cohort_id,
        entity_type="cohort",
        attributes={"poverty_headcount_ratio": qty},
        metadata={},
    )
    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    state = SimulationState(
        timestep=ts,
        resolution=ResolutionConfig(),
        entities={cohort_id: entity},
        relationships=[],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="sid", name="t", description="", start_date=ts, end_date=ts,
        ),
    )
    threshold = _threshold(
        indicator_key="poverty_headcount_ratio",
        entity_scope="*:CHT:1-*-*",
        floor_value="0.40",
        approach_pct="0.15",
    )
    alerts = MDAChecker().check(state, [], [threshold])
    assert len(alerts) == 1
    assert alerts[0].entity_id == cohort_id


# ---------------------------------------------------------------------------
# Test: missing indicator skipped silently
# ---------------------------------------------------------------------------


def test_missing_indicator_skipped() -> None:
    state = _state_with_entity("GRC", {})  # no attributes at all
    threshold = _threshold(indicator_key="reserve_coverage_months")
    alerts = MDAChecker().check(state, [], [threshold])
    assert alerts == []


# ---------------------------------------------------------------------------
# Test: multiple thresholds produce one alert each
# ---------------------------------------------------------------------------


def test_multiple_thresholds_multiple_alerts() -> None:
    state = _state_with_entity(
        "GRC",
        {
            "reserve_coverage_months": Decimal("2.0"),  # breaches floor=2.5
            "debt_gdp_ratio": Decimal("1.10"),           # breaches floor=1.20
        },
    )
    t1 = _threshold(mda_id="MDA-A", indicator_key="reserve_coverage_months", floor_value="2.5")
    t2 = _threshold(mda_id="MDA-B", indicator_key="debt_gdp_ratio", floor_value="1.20")
    alerts = MDAChecker().check(state, [], [t1, t2])
    assert len(alerts) == 2
    mda_ids = {a.mda_id for a in alerts}
    assert mda_ids == {"MDA-A", "MDA-B"}


# ---------------------------------------------------------------------------
# Test: alerts_to_events_snapshot encodes deterministic event_id
# ---------------------------------------------------------------------------


def test_alerts_to_events_snapshot_event_id() -> None:
    alert = MDAAlert(
        mda_id="MDA-FIN-RESERVES",
        entity_id="GRC",
        indicator_key="reserve_coverage_months",
        severity=MDASeverity.CRITICAL,
        floor_value="2.5",
        current_value="2.0",
        approach_pct_remaining="-0.2000",
        consecutive_breach_steps=1,
    )
    events = alerts_to_events_snapshot([alert], step_index=3)
    assert len(events) == 1
    assert events[0]["event_id"] == "mda-MDA-FIN-RESERVES-GRC-step3"
    assert events[0]["event_type"] == "mda_breach"
    assert events[0]["severity"] == "CRITICAL"


# ---------------------------------------------------------------------------
# Test: alerts_from_events_snapshot reconstructs MDAAlert list
# ---------------------------------------------------------------------------


def test_alerts_from_events_snapshot_round_trip() -> None:
    alert = MDAAlert(
        mda_id="MDA-FIN-RESERVES",
        entity_id="GRC",
        indicator_key="reserve_coverage_months",
        severity=MDASeverity.TERMINAL,
        floor_value="2.5",
        current_value="1.8",
        approach_pct_remaining="-0.2800",
        consecutive_breach_steps=2,
    )
    events = alerts_to_events_snapshot([alert], step_index=5)
    recovered = alerts_from_events_snapshot(events)
    assert len(recovered) == 1
    assert recovered[0].severity == MDASeverity.TERMINAL
    assert recovered[0].consecutive_breach_steps == 2
    assert recovered[0].mda_id == "MDA-FIN-RESERVES"


# ---------------------------------------------------------------------------
# Test: alerts_from_events_snapshot entity_id filter
# ---------------------------------------------------------------------------


def test_alerts_from_events_snapshot_entity_filter() -> None:
    events = [
        {
            "event_type": "mda_breach",
            "event_id": "mda-MDA-A-GRC-step1",
            "mda_id": "MDA-A",
            "entity_id": "GRC",
            "indicator_key": "reserve_coverage_months",
            "severity": "CRITICAL",
            "floor_value": "2.5",
            "current_value": "2.0",
            "approach_pct_remaining": "-0.2000",
            "consecutive_breach_steps": 1,
        },
        {
            "event_type": "mda_breach",
            "event_id": "mda-MDA-A-THA-step1",
            "mda_id": "MDA-A",
            "entity_id": "THA",
            "indicator_key": "reserve_coverage_months",
            "severity": "CRITICAL",
            "floor_value": "2.5",
            "current_value": "2.1",
            "approach_pct_remaining": "-0.1600",
            "consecutive_breach_steps": 1,
        },
    ]
    grc_only = alerts_from_events_snapshot(events, entity_id="GRC")
    assert len(grc_only) == 1
    assert grc_only[0].entity_id == "GRC"


# ---------------------------------------------------------------------------
# Test: MDAThresholdRecord coerces Decimal floor_value / approach_pct to str
# ---------------------------------------------------------------------------


def test_threshold_record_coerces_numeric_to_str() -> None:
    record = MDAThresholdRecord(
        mda_id="MDA-TEST",
        indicator_key="reserve_coverage_months",
        entity_scope="all",
        measurement_framework="financial",
        floor_value=Decimal("2.5"),   # Decimal input (as asyncpg returns for NUMERIC)
        floor_unit="months",
        approach_pct=Decimal("0.20"),  # Decimal input
        severity_at_breach="CRITICAL",
        description="Test.",
        historical_basis="Test.",
        recovery_horizon_years=None,
        irreversibility_note="Test.",
    )
    assert isinstance(record.floor_value, str)
    assert isinstance(record.approach_pct, str)
    assert record.floor_value == "2.5"
    assert record.approach_pct == "0.20"


# ---------------------------------------------------------------------------
# Test: _build_prior_counts ignores non-mda_breach events
# ---------------------------------------------------------------------------


def test_build_prior_counts_ignores_non_breach_events() -> None:
    events = [
        {"event_type": "policy_change", "mda_id": "MDA-X", "entity_id": "GRC",
         "consecutive_breach_steps": 5},
        {"event_type": "mda_breach", "mda_id": "MDA-FIN-RESERVES", "entity_id": "GRC",
         "consecutive_breach_steps": 1},
    ]
    counts = _build_prior_counts(events)
    assert ("MDA-X", "GRC") not in counts
    assert counts[("MDA-FIN-RESERVES", "GRC")] == 1


# ---------------------------------------------------------------------------
# Test: approach_pct_remaining is negative 4dp when below floor
# ---------------------------------------------------------------------------


def test_approach_pct_remaining_precision_when_breached() -> None:
    state = _state_with_entity("GRC", {"reserve_coverage_months": Decimal("2.0")})
    threshold = _threshold(floor_value="2.5", approach_pct="0.20")
    alerts = MDAChecker().check(state, [], [threshold])
    assert len(alerts) == 1
    # (2.0 - 2.5) / 2.5 = -0.2 → serialized to -0.2000 (4 d.p.)
    assert alerts[0].approach_pct_remaining == "-0.2000"


# ---------------------------------------------------------------------------
# Test: TERMINAL consecutive_breach_steps increments beyond 2 from prior count
# ---------------------------------------------------------------------------


def test_terminal_increments_beyond_two() -> None:
    state = _state_with_entity("GRC", {"reserve_coverage_months": Decimal("2.0")})
    threshold = _threshold(mda_id="MDA-FIN-RESERVES", floor_value="2.5", approach_pct="0.20")
    # Prior step already had consecutive_breach_steps=3
    prior_events = [
        {
            "event_type": "mda_breach",
            "mda_id": "MDA-FIN-RESERVES",
            "entity_id": "GRC",
            "consecutive_breach_steps": 3,
        }
    ]
    alerts = MDAChecker().check(state, prior_events, [threshold])
    assert len(alerts) == 1
    assert alerts[0].severity == MDASeverity.TERMINAL
    assert alerts[0].consecutive_breach_steps == 4
