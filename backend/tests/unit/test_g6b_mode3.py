"""
G6b — Mode 3 Active Control unit tests (Issue #753).

Tests:
  - BranchRequest/BranchResponse schema validation
  - RebranchRequest schema validation
  - MDAAlert.recovery_horizon_years field propagation through mda_checker
  - alerts_to_events_snapshot stores recovery_horizon_years
  - alerts_from_events_snapshot restores recovery_horizon_years
  - _validate_branch_step_range (branch_from_step >= 0)
"""
from __future__ import annotations

from datetime import UTC

import pytest
from pydantic import ValidationError

from app.schemas import (
    BranchRequest,
    BranchResponse,
    MDAAlert,
    MDASeverity,
    MDAThresholdRecord,
    RebranchRequest,
)
from app.simulation.mda_checker import (
    MDAChecker,
    alerts_from_events_snapshot,
    alerts_to_events_snapshot,
)

# ---------------------------------------------------------------------------
# 1. BranchRequest schema validation
# ---------------------------------------------------------------------------


def test_branch_request_accepts_valid() -> None:
    req = BranchRequest(fiscal_multiplier=1.5, branch_from_step=3)
    assert req.fiscal_multiplier == pytest.approx(1.5)
    assert req.branch_from_step == 3


def test_branch_request_fiscal_multiplier_floor() -> None:
    with pytest.raises(ValidationError):
        BranchRequest(fiscal_multiplier=0.05, branch_from_step=0)


def test_branch_request_fiscal_multiplier_ceiling() -> None:
    with pytest.raises(ValidationError):
        BranchRequest(fiscal_multiplier=3.5, branch_from_step=0)


def test_branch_request_step_must_be_non_negative() -> None:
    with pytest.raises(ValidationError):
        BranchRequest(fiscal_multiplier=1.0, branch_from_step=-1)


def test_branch_response_fields() -> None:
    resp = BranchResponse(
        branch_scenario_id="abc-123",
        branch_from_step=4,
        n_steps=8,
    )
    assert resp.branch_scenario_id == "abc-123"
    assert resp.branch_from_step == 4
    assert resp.n_steps == 8


# ---------------------------------------------------------------------------
# 2. RebranchRequest schema validation
# ---------------------------------------------------------------------------


def test_rebranch_request_accepts_valid() -> None:
    req = RebranchRequest(fiscal_multiplier=0.8, from_step=2)
    assert req.fiscal_multiplier == pytest.approx(0.8)
    assert req.from_step == 2


def test_rebranch_request_from_step_non_negative() -> None:
    with pytest.raises(ValidationError):
        RebranchRequest(fiscal_multiplier=1.0, from_step=-1)


# ---------------------------------------------------------------------------
# 3. MDAAlert.recovery_horizon_years — field exists and defaults to None
# ---------------------------------------------------------------------------


def test_mda_alert_recovery_horizon_default_none() -> None:
    alert = MDAAlert(
        mda_id="m1",
        entity_id="GRC",
        indicator_key="reserve_coverage_months",
        indicator_name="Reserve Coverage Months",
        severity=MDASeverity.WARNING,
        floor_value="3.0",
        current_value="3.5",
        approach_pct_remaining="0.05",
        consecutive_breach_steps=0,
    )
    assert alert.recovery_horizon_years is None


def test_mda_alert_recovery_horizon_set() -> None:
    alert = MDAAlert(
        mda_id="m1",
        entity_id="GRC",
        indicator_key="reserve_coverage_months",
        indicator_name="Reserve Coverage Months",
        severity=MDASeverity.WARNING,
        floor_value="3.0",
        current_value="3.5",
        approach_pct_remaining="0.05",
        consecutive_breach_steps=0,
        recovery_horizon_years=5,
    )
    assert alert.recovery_horizon_years == 5


# ---------------------------------------------------------------------------
# 4. MDAChecker propagates recovery_horizon_years from threshold
# ---------------------------------------------------------------------------


def _make_threshold(
    *,
    recovery_horizon_years: int | None = None,
    indicator_value: str = "2.5",
    floor_value: str = "3.0",
) -> MDAThresholdRecord:
    return MDAThresholdRecord(
        mda_id="mda-reserve",
        indicator_key="reserve_coverage_months",
        entity_scope="all",
        measurement_framework="financial",
        floor_value=floor_value,
        floor_unit="months",
        approach_pct="0.1",
        comparison_operator="lte",
        severity_at_breach="CRITICAL",
        description="Minimum reserve coverage",
        historical_basis="IMF 2010",
        recovery_horizon_years=recovery_horizon_years,
        irreversibility_note=(
            "Recoverable with IMF support" if recovery_horizon_years else "Irreversible"
        ),
    )


def _make_state_with_reserve(value: str) -> object:
    from datetime import datetime

    from app.schemas import QuantitySchema
    from app.simulation.engine.models import (  # type: ignore[import]
        ResolutionConfig,
        ScenarioConfig,
        SimulationEntity,
        SimulationState,
    )
    from app.simulation.repositories.quantity_serde import (
        quantity_from_schema,  # type: ignore[import]
    )

    entity = SimulationEntity(
        id="GRC",
        entity_type="country",
        attributes={
            "reserve_coverage_months": quantity_from_schema(
                QuantitySchema(
                    value=value,
                    unit="months",
                    variable_type="stock",
                    confidence_tier=2,
                    measurement_framework="financial",
                )
            )
        },
        metadata={},
    )
    return SimulationState(
        timestep=datetime(2010, 1, 1, tzinfo=UTC),
        resolution=ResolutionConfig(),
        entities={"GRC": entity},
        relationships=[],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="test",
            name="test",
            description="",
            start_date=datetime(2010, 1, 1, tzinfo=UTC),
            end_date=datetime(2010, 1, 1, tzinfo=UTC),
        ),
    )


def test_mda_checker_propagates_recovery_horizon_years() -> None:
    state = _make_state_with_reserve("2.5")  # breaches lte 3.0
    threshold = _make_threshold(recovery_horizon_years=3)
    checker = MDAChecker()
    alerts = checker.check(state, [], [threshold])
    assert len(alerts) == 1
    assert alerts[0].recovery_horizon_years == 3


def test_mda_checker_propagates_none_recovery_horizon() -> None:
    state = _make_state_with_reserve("2.5")
    threshold = _make_threshold(recovery_horizon_years=None)
    checker = MDAChecker()
    alerts = checker.check(state, [], [threshold])
    assert len(alerts) == 1
    assert alerts[0].recovery_horizon_years is None


# ---------------------------------------------------------------------------
# 5. alerts_to_events_snapshot stores recovery_horizon_years
# ---------------------------------------------------------------------------


def _make_alert(*, recovery_horizon_years: int | None = None) -> MDAAlert:
    return MDAAlert(
        mda_id="m1",
        entity_id="GRC",
        indicator_key="reserve_coverage_months",
        indicator_name="Reserve Coverage Months",
        severity=MDASeverity.CRITICAL,
        floor_value="3.0",
        current_value="2.5",
        approach_pct_remaining="-0.05",
        consecutive_breach_steps=1,
        recovery_horizon_years=recovery_horizon_years,
    )


def test_alerts_to_snapshot_stores_recovery_horizon() -> None:
    alert = _make_alert(recovery_horizon_years=7)
    events = alerts_to_events_snapshot([alert], step_index=2)
    assert len(events) == 1
    assert events[0]["recovery_horizon_years"] == 7


def test_alerts_to_snapshot_stores_none_recovery_horizon() -> None:
    alert = _make_alert(recovery_horizon_years=None)
    events = alerts_to_events_snapshot([alert], step_index=1)
    assert events[0]["recovery_horizon_years"] is None


# ---------------------------------------------------------------------------
# 6. alerts_from_events_snapshot restores recovery_horizon_years
# ---------------------------------------------------------------------------


def test_alerts_from_snapshot_restores_recovery_horizon() -> None:
    snapshot = [
        {
            "event_type": "mda_breach",
            "mda_id": "m1",
            "entity_id": "GRC",
            "indicator_key": "reserve_coverage_months",
            "indicator_name": "Reserve Coverage Months",
            "severity": "CRITICAL",
            "floor_value": "3.0",
            "current_value": "2.5",
            "approach_pct_remaining": "-0.05",
            "consecutive_breach_steps": 1,
            "recovery_horizon_years": 4,
        }
    ]
    alerts = alerts_from_events_snapshot(snapshot)
    assert len(alerts) == 1
    assert alerts[0].recovery_horizon_years == 4


def test_alerts_from_snapshot_handles_missing_recovery_horizon() -> None:
    """Pre-G6b snapshots lack recovery_horizon_years — must default to None."""
    snapshot = [
        {
            "event_type": "mda_breach",
            "mda_id": "m1",
            "entity_id": "GRC",
            "indicator_key": "reserve_coverage_months",
            "indicator_name": "Reserve Coverage Months",
            "severity": "WARNING",
            "floor_value": "3.0",
            "current_value": "3.2",
            "approach_pct_remaining": "0.02",
            "consecutive_breach_steps": 0,
        }
    ]
    alerts = alerts_from_events_snapshot(snapshot)
    assert len(alerts) == 1
    assert alerts[0].recovery_horizon_years is None


def test_alerts_roundtrip_recovery_horizon() -> None:
    """Roundtrip: MDAAlert → events_snapshot → MDAAlert preserves recovery_horizon_years."""
    original = _make_alert(recovery_horizon_years=12)
    events = alerts_to_events_snapshot([original], step_index=3)
    restored = alerts_from_events_snapshot(events)
    assert len(restored) == 1
    assert restored[0].recovery_horizon_years == 12
