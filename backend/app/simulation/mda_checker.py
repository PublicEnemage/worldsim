"""MDAChecker — ADR-005 Decision 3.

Evaluates all registered MDA thresholds against current simulation state after
each timestep advance. Runs unconditionally in WebScenarioRunner — no
configuration option disables it. This implements the CLAUDE.md architectural
requirement: threshold alerts fire regardless of user weighting when any
dimension crosses below a critical floor.

Severity classification (ADR-005 Decision 3):
  WARNING  — value is above floor_value but within approach_pct of it.
             approach_pct_remaining is positive; breach has not occurred.
  CRITICAL — value is at or below floor_value for exactly one consecutive step.
             The floor has been crossed; the intervention window is open.
  TERMINAL — value is at or below floor_value for two or more consecutive steps.
             The simulation flags explicitly: the recovery envelope may be closing.

Entity scope matching uses Python's fnmatch module. Scope 'all' is treated as '*'.

consecutive_breach_steps is derived from the prior snapshot's events_snapshot:
if a matching mda_breach event for the same (mda_id, entity_id) pair appears
in the prior step's events, the count from that event is incremented by one.
TERMINAL fires when consecutive_breach_steps >= 2.
"""
from __future__ import annotations

import fnmatch
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from app.schemas import MDAAlert, MDASeverity, MDAThresholdRecord

if TYPE_CHECKING:
    from app.simulation.engine.models import SimulationState


class MDAChecker:
    """Evaluates all registered MDA thresholds against current simulation state."""

    def check(
        self,
        state: SimulationState,
        prior_breach_events: list[dict[str, Any]],
        thresholds: list[MDAThresholdRecord],
    ) -> list[MDAAlert]:
        """Evaluate all thresholds against current state.

        Args:
            state: Current timestep SimulationState.
            prior_breach_events: MDA breach events from the prior snapshot's
                events_snapshot column. Empty list at step 0 or if no prior
                snapshot exists. Used to count consecutive breach steps.
            thresholds: All registered MDA threshold records from mda_thresholds.

        Returns:
            MDAAlert list — one per (entity, threshold) pair that meets
            WARNING, CRITICAL, or TERMINAL criteria. Empty list when no
            thresholds are triggered.
        """
        prior_counts = _build_prior_counts(prior_breach_events)
        alerts: list[MDAAlert] = []

        for threshold in thresholds:
            scope = "*" if threshold.entity_scope == "all" else threshold.entity_scope
            floor = Decimal(threshold.floor_value)
            approach_pct = Decimal(threshold.approach_pct)

            for entity_id, entity in state.entities.items():
                if not fnmatch.fnmatch(entity_id, scope):
                    continue

                qty = entity.get_attribute(threshold.indicator_key)
                if qty is None:
                    continue

                current = qty.value
                # Positive → above floor (safe). Zero or negative → at/below floor (breach).
                approach_pct_remaining = (current - floor) / floor

                if approach_pct_remaining > approach_pct:
                    continue

                prior_count = prior_counts.get((threshold.mda_id, entity_id), 0)

                if approach_pct_remaining <= Decimal("0"):
                    consecutive = prior_count + 1
                    severity = (
                        MDASeverity.TERMINAL if consecutive >= 2 else MDASeverity.CRITICAL
                    )
                else:
                    consecutive = 0
                    severity = MDASeverity.WARNING

                alerts.append(
                    MDAAlert(
                        mda_id=threshold.mda_id,
                        entity_id=entity_id,
                        indicator_key=threshold.indicator_key,
                        severity=severity,
                        floor_value=str(floor),
                        current_value=str(current),
                        approach_pct_remaining=str(
                            approach_pct_remaining.quantize(Decimal("0.0001"))
                        ),
                        consecutive_breach_steps=consecutive,
                    )
                )

        return alerts


# ---------------------------------------------------------------------------
# Serialization helpers — events_snapshot format
# ---------------------------------------------------------------------------


def alerts_to_events_snapshot(
    alerts: list[MDAAlert],
    step_index: int,
) -> list[dict[str, Any]]:
    """Convert MDAAlert list to the events_snapshot storage format.

    Each alert becomes one dict with event_type='mda_breach'. The event_id
    encodes (mda_id, entity_id, step_index) for deterministic deduplication.

    Args:
        alerts: MDAAlert list from MDAChecker.check().
        step_index: Current simulation step number, used in event_id encoding.

    Returns:
        List of breach event dicts ready to store in events_snapshot JSONB column.
    """
    return [
        {
            "event_type": "mda_breach",
            "event_id": f"mda-{alert.mda_id}-{alert.entity_id}-step{step_index}",
            "mda_id": alert.mda_id,
            "entity_id": alert.entity_id,
            "indicator_key": alert.indicator_key,
            "severity": alert.severity.value,
            "floor_value": alert.floor_value,
            "current_value": alert.current_value,
            "approach_pct_remaining": alert.approach_pct_remaining,
            "consecutive_breach_steps": alert.consecutive_breach_steps,
        }
        for alert in alerts
    ]


def alerts_from_events_snapshot(
    events_snapshot: list[dict[str, Any]],
    entity_id: str | None = None,
    framework: str | None = None,
) -> list[MDAAlert]:
    """Reconstruct MDAAlert list from a stored events_snapshot.

    Args:
        events_snapshot: List of breach event dicts from the JSONB column.
        entity_id: If given, filters to alerts for this entity only.
        framework: Unused here — framework filtering happens in the caller.

    Returns:
        MDAAlert list for the requested entity / all entities.
    """
    alerts: list[MDAAlert] = []
    for evt in events_snapshot:
        if evt.get("event_type") != "mda_breach":
            continue
        if entity_id is not None and evt.get("entity_id") != entity_id:
            continue
        try:
            alerts.append(
                MDAAlert(
                    mda_id=evt["mda_id"],
                    entity_id=evt["entity_id"],
                    indicator_key=evt["indicator_key"],
                    severity=MDASeverity(evt["severity"]),
                    floor_value=evt["floor_value"],
                    current_value=evt["current_value"],
                    approach_pct_remaining=evt["approach_pct_remaining"],
                    consecutive_breach_steps=int(evt["consecutive_breach_steps"]),
                )
            )
        except (KeyError, ValueError):
            continue
    return alerts


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _build_prior_counts(
    prior_breach_events: list[dict[str, Any]],
) -> dict[tuple[str, str], int]:
    """Build (mda_id, entity_id) → consecutive_breach_steps from prior events."""
    counts: dict[tuple[str, str], int] = {}
    for evt in prior_breach_events:
        if evt.get("event_type") != "mda_breach":
            continue
        try:
            key = (str(evt["mda_id"]), str(evt["entity_id"]))
            counts[key] = int(evt.get("consecutive_breach_steps", 1))
        except (KeyError, ValueError):
            continue
    return counts
