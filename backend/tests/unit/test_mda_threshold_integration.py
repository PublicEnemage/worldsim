"""
MDA threshold integration scenarios — Issue #184.

Deliberately constructed scenarios that verify MDAChecker fires the
correct severity at the correct threshold boundary. Tests are scenario-level
(entity + threshold + checker) rather than unit-level (one method call).

Thresholds used here mirror production thresholds from the Argentina and
Greece fixtures so that backtesting regressions are caught immediately.

Severity contract (MDAChecker docstring):
  WARNING  — within approach_pct of floor, not yet breached
  CRITICAL — breached for exactly one consecutive step
  TERMINAL — breached for two or more consecutive steps

comparison_operator contract:
  "lte" — breach when current ≤ floor_value (lower-bound threshold)
  "gte" — breach when current ≥ floor_value (upper-bound threshold)
"""
from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from app.schemas import MDASeverity, MDAThresholdRecord
from app.simulation.engine.models import (
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.engine.quantity import Quantity, VariableType
from app.simulation.mda_checker import MDAChecker, alerts_to_events_snapshot

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_TS = datetime(2001, 12, 1, tzinfo=UTC)

_DEMOCRACY_FLOOR = MDAThresholdRecord(
    mda_id="MDA-GOV-DEMOCRACY-FLOOR",
    indicator_key="democratic_quality_score",
    entity_scope="all",
    measurement_framework="governance",
    floor_value="0.70",
    floor_unit="ratio_0_1",
    approach_pct="0.10",
    comparison_operator="lte",
    severity_at_breach="CRITICAL",
    description="V-Dem LDI democracy floor — minimum threshold for governance viability.",
    historical_basis="V-Dem dataset, autocratization thresholds.",
    recovery_horizon_years=None,
    irreversibility_note="Democratic backsliding requires years to reverse.",
)

_ECOLOGICAL_BOUNDARY = MDAThresholdRecord(
    mda_id="MDA-ECO-CO2-BOUNDARY",
    indicator_key="co2_proximity_score",
    entity_scope="all",
    measurement_framework="ecological",
    floor_value="1.0",
    floor_unit="ratio",
    approach_pct="0.05",
    comparison_operator="gte",
    severity_at_breach="CRITICAL",
    description="CO2 planetary boundary — breach when normalized proximity ≥ 1.0.",
    historical_basis="NOAA MLO CO2 series, IPCC boundary.",
    recovery_horizon_years=None,
    irreversibility_note="CO2 concentration is effectively irreversible on human timescales.",
)

_DEBT_CEILING = MDAThresholdRecord(
    mda_id="MDA-FIN-DEBT-GDP",
    indicator_key="debt_gdp_ratio",
    entity_scope="all",
    measurement_framework="financial",
    floor_value="1.40",
    floor_unit="ratio",
    approach_pct="0.20",
    comparison_operator="gte",
    severity_at_breach="CRITICAL",
    description="Debt-to-GDP ceiling — breach when ratio ≥ 1.40.",
    historical_basis="Greece 2012 sovereign debt crisis threshold.",
    recovery_horizon_years=None,
    irreversibility_note="",
)


def _state(entity_id: str, attrs: dict[str, Decimal]) -> SimulationState:
    attribute_map: dict[str, Quantity] = {
        key: Quantity(
            value=val,
            unit="dimensionless",
            variable_type=VariableType.DIMENSIONLESS,
            measurement_framework=None,
            confidence_tier=1,
        )
        for key, val in attrs.items()
    }
    entity = SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes=attribute_map,
        metadata={},
    )
    return SimulationState(
        timestep=_TS,
        resolution=ResolutionConfig(),
        entities={entity_id: entity},
        relationships=[],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="test-sid",
            name="Integration test",
            description="",
            start_date=_TS,
            end_date=_TS,
        ),
    )


def _prior_breach_events(
    mda_id: str,
    entity_id: str,
    consecutive_steps: int = 1,
) -> list[dict[str, Any]]:
    """Build the events_snapshot format that encodes a prior breach."""
    return [
        {
            "event_type": "mda_breach",
            "event_id": f"{mda_id}--{entity_id}--0",
            "mda_id": mda_id,
            "entity_id": entity_id,
            "consecutive_breach_steps": consecutive_steps,
        }
    ]


# ---------------------------------------------------------------------------
# Democracy floor — lte threshold
# ---------------------------------------------------------------------------


def test_democracy_floor_safe_zone_produces_no_alert() -> None:
    state = _state("ARG", {"democratic_quality_score": Decimal("0.90")})
    alerts = MDAChecker().check(state, [], [_DEMOCRACY_FLOOR])
    assert alerts == []


def test_democracy_floor_approach_zone_produces_warning() -> None:
    # floor=0.70, approach_pct=0.10 → warning when value ≤ 0.70 * 1.10 = 0.77
    state = _state("ARG", {"democratic_quality_score": Decimal("0.73")})
    alerts = MDAChecker().check(state, [], [_DEMOCRACY_FLOOR])
    assert len(alerts) == 1
    assert alerts[0].severity == MDASeverity.WARNING
    assert alerts[0].mda_id == "MDA-GOV-DEMOCRACY-FLOOR"


def test_democracy_floor_breach_produces_critical() -> None:
    state = _state("ARG", {"democratic_quality_score": Decimal("0.665")})
    alerts = MDAChecker().check(state, [], [_DEMOCRACY_FLOOR])
    assert len(alerts) == 1
    assert alerts[0].severity == MDASeverity.CRITICAL
    assert alerts[0].entity_id == "ARG"


def test_democracy_floor_second_consecutive_breach_produces_terminal() -> None:
    state = _state("ARG", {"democratic_quality_score": Decimal("0.65")})
    prior = _prior_breach_events("MDA-GOV-DEMOCRACY-FLOOR", "ARG", consecutive_steps=1)
    alerts = MDAChecker().check(state, prior, [_DEMOCRACY_FLOOR])
    assert len(alerts) == 1
    assert alerts[0].severity == MDASeverity.TERMINAL
    assert alerts[0].consecutive_breach_steps == 2


def test_democracy_floor_boundary_exact_value_is_breach() -> None:
    """exact floor value triggers CRITICAL, not WARNING (≤ semantics)."""
    state = _state("ARG", {"democratic_quality_score": Decimal("0.70")})
    alerts = MDAChecker().check(state, [], [_DEMOCRACY_FLOOR])
    assert len(alerts) == 1
    assert alerts[0].severity == MDASeverity.CRITICAL


# ---------------------------------------------------------------------------
# Ecological boundary — gte threshold
# ---------------------------------------------------------------------------


def test_ecological_boundary_safe_zone_produces_no_alert() -> None:
    state = _state("GRC", {"co2_proximity_score": Decimal("0.90")})
    alerts = MDAChecker().check(state, [], [_ECOLOGICAL_BOUNDARY])
    assert alerts == []


def test_ecological_boundary_breach_produces_critical() -> None:
    # Argentina Argentina seed: 369.5 ppm → proximity ≈ 1.056 (above 1.0 boundary)
    state = _state("ARG", {"co2_proximity_score": Decimal("1.056")})
    alerts = MDAChecker().check(state, [], [_ECOLOGICAL_BOUNDARY])
    assert len(alerts) == 1
    assert alerts[0].severity == MDASeverity.CRITICAL
    assert alerts[0].mda_id == "MDA-ECO-CO2-BOUNDARY"


def test_ecological_boundary_approach_produces_warning() -> None:
    # floor=1.0, approach_pct=0.05 → warning when value ≥ 1.0 * (1 - 0.05) = 0.95
    state = _state("ARG", {"co2_proximity_score": Decimal("0.97")})
    alerts = MDAChecker().check(state, [], [_ECOLOGICAL_BOUNDARY])
    assert len(alerts) == 1
    assert alerts[0].severity == MDASeverity.WARNING


# ---------------------------------------------------------------------------
# Multiple thresholds simultaneously
# ---------------------------------------------------------------------------


def test_two_thresholds_both_breached_produce_two_alerts() -> None:
    """A single entity breaching both democracy and ecological floors → two alerts."""
    state = _state("ARG", {
        "democratic_quality_score": Decimal("0.65"),  # below 0.70 → CRITICAL
        "co2_proximity_score": Decimal("1.056"),       # above 1.0 → CRITICAL
    })
    alerts = MDAChecker().check(state, [], [_DEMOCRACY_FLOOR, _ECOLOGICAL_BOUNDARY])
    assert len(alerts) == 2
    alert_ids = {a.mda_id for a in alerts}
    assert "MDA-GOV-DEMOCRACY-FLOOR" in alert_ids
    assert "MDA-ECO-CO2-BOUNDARY" in alert_ids
    assert all(a.severity == MDASeverity.CRITICAL for a in alerts)


def test_threshold_does_not_match_absent_indicator() -> None:
    """No alert when the entity has no attribute for the threshold's indicator_key."""
    state = _state("GRC", {"gdp_growth": Decimal("-0.08")})  # no democratic_quality_score
    alerts = MDAChecker().check(state, [], [_DEMOCRACY_FLOOR])
    assert alerts == []


def test_entity_scope_filters_non_matching_entity() -> None:
    """entity_scope='GRC' threshold does not fire for 'ARG'."""
    scoped_threshold = MDAThresholdRecord(
        mda_id="MDA-GRC-ONLY",
        indicator_key="democratic_quality_score",
        entity_scope="GRC",
        measurement_framework="governance",
        floor_value="0.70",
        floor_unit="ratio_0_1",
        approach_pct="0.10",
        comparison_operator="lte",
        severity_at_breach="CRITICAL",
        description="GRC-scoped threshold.",
        historical_basis="",
        recovery_horizon_years=None,
        irreversibility_note="",
    )
    state = _state("ARG", {"democratic_quality_score": Decimal("0.60")})
    alerts = MDAChecker().check(state, [], [scoped_threshold])
    assert alerts == []


# ---------------------------------------------------------------------------
# Debt ceiling — gte threshold (Issue #236 regression guard)
# ---------------------------------------------------------------------------


def test_debt_gdp_ceiling_breach_produces_critical() -> None:
    # Greece 2012: debt/GDP ≈ 1.483 — well above 1.40 ceiling
    state = _state("GRC", {"debt_gdp_ratio": Decimal("1.483")})
    alerts = MDAChecker().check(state, [], [_DEBT_CEILING])
    assert len(alerts) == 1
    assert alerts[0].severity == MDASeverity.CRITICAL


def test_debt_gdp_ceiling_safe_zone() -> None:
    state = _state("GRC", {"debt_gdp_ratio": Decimal("0.90")})
    alerts = MDAChecker().check(state, [], [_DEBT_CEILING])
    assert alerts == []


# ---------------------------------------------------------------------------
# Snapshot round-trip — alerts_to_events_snapshot → prior_breach_events
# ---------------------------------------------------------------------------


def test_snapshot_round_trip_produces_correct_consecutive_count() -> None:
    """alerts_to_events_snapshot output can be fed back as prior_breach_events."""
    state = _state("ARG", {"democratic_quality_score": Decimal("0.65")})

    # Step 1: first breach
    alerts_step1 = MDAChecker().check(state, [], [_DEMOCRACY_FLOOR])
    assert alerts_step1[0].severity == MDASeverity.CRITICAL

    # Serialise to snapshot format
    snapshot = alerts_to_events_snapshot(alerts_step1, step_index=1)

    # Step 2: second breach using step 1 snapshot as prior
    alerts_step2 = MDAChecker().check(state, snapshot, [_DEMOCRACY_FLOOR])
    assert alerts_step2[0].severity == MDASeverity.TERMINAL
    assert alerts_step2[0].consecutive_breach_steps == 2
