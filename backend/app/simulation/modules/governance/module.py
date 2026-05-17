"""GovernanceModule — ADR-005 Decision 6.

Subscribes to macro, fiscal, and political events on country entities and
applies the governance elasticity matrix to produce governance indicator
Quantity-delta Events with framework=MeasurementFramework.GOVERNANCE.

One-step lag design: reads state.events (prior step). Governance effects of
GDP contractions, fiscal cuts, IMF programs, and emergency declarations appear
with a structural delay, consistent with annual indicator update cycles.

Implicit dependency: subscribes to gdp_growth_change which only fires when
MacroeconomicModule is active. If MacroeconomicModule is absent, GDP-mediated
governance effects are silently absent. Enforcement tracked in Issue #211 (M7).
"""
from __future__ import annotations

import logging
from decimal import Decimal
from typing import TYPE_CHECKING

from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
    SimulationEntity,
    SimulationModule,
    SimulationState,
)
from app.simulation.engine.quantity import Quantity, VariableType
from app.simulation.modules.governance.elasticities import GOVERNANCE_ELASTICITY_REGISTRY

if TYPE_CHECKING:
    from datetime import datetime

_log = logging.getLogger(__name__)

# Canonical unit strings per DATA_STANDARDS.md §Canonical Unit Registry (Gap 1).
# Sources: WGI RL.EST → percentile_0_100; V-Dem LDI → ratio_0_1 (0–1 scale);
# TI CPI → percentile_0_100; RSF index → index; derived composite → index.
# Any future governance indicator not listed here falls back to "dimensionless"
# (genuinely dimensionless, not a placeholder — document the rationale if used).
_INDICATOR_UNITS: dict[str, str] = {
    "rule_of_law_percentile": "percentile_0_100",
    "democratic_quality_score": "ratio_0_1",
    "corruption_perception_index": "percentile_0_100",
    "press_freedom_index": "index",
    "technocratic_independence": "index",
}
_DEFAULT_GOVERNANCE_UNIT = "dimensionless"

_SUBSCRIBED_EVENTS = frozenset({
    "gdp_growth_change",
    "fiscal_policy_spending_change",
    "imf_program_acceptance",
    "emergency_declaration",
})


class GovernanceModule(SimulationModule):
    """Translates country-level events into governance indicator deltas.

    M6 minimum viable scope: rule_of_law_percentile and democratic_quality_score.
    Full indicator set (press_freedom_index, corruption_perception_index,
    technocratic_independence) added in subsequent milestones as elasticity
    registry entries and backtesting data are available.
    """

    def compute(
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime,
    ) -> list[Event]:
        if entity.entity_type != "country":
            return []

        prior_events = [
            e for e in state.events
            if e.source_entity_id == entity.id and e.event_type in _SUBSCRIBED_EVENTS
        ]
        if not prior_events:
            _log.debug(
                "%s: no subscribed events for entity_id=%r at timestep=%r — returning []",
                type(self).__name__,
                entity.id,
                timestep,
            )
            return []

        # Accumulate deltas per indicator across all prior events.
        indicator_deltas: dict[str, Decimal] = {}
        indicator_tiers: dict[str, int] = {}

        for event in prior_events:
            magnitude = _extract_magnitude(event)
            if magnitude is None:
                continue
            event_tier = _event_confidence_tier(event)
            for row in GOVERNANCE_ELASTICITY_REGISTRY:
                if row.event_type != event.event_type:
                    continue
                delta = (magnitude * row.elasticity).quantize(Decimal("0.000001"))
                key = row.indicator_key
                indicator_deltas[key] = indicator_deltas.get(key, Decimal("0")) + delta
                indicator_tiers[key] = max(
                    indicator_tiers.get(key, row.confidence_tier),
                    event_tier,
                )

        if not indicator_deltas:
            return []

        affected_attributes = {
            key: Quantity(
                value=delta,
                unit=_INDICATOR_UNITS.get(key, _DEFAULT_GOVERNANCE_UNIT),
                variable_type=VariableType.DIMENSIONLESS,
                measurement_framework=MeasurementFramework.GOVERNANCE,
                confidence_tier=indicator_tiers[key],
            )
            for key, delta in indicator_deltas.items()
        }

        return [Event(
            event_id=f"gov-{entity.id}-{timestep.isoformat()}",
            source_entity_id=entity.id,
            event_type="governance_indicator_update",
            affected_attributes=affected_attributes,
            propagation_rules=[],
            timestep_originated=timestep,
            framework=MeasurementFramework.GOVERNANCE,
            metadata={"entity_id": entity.id},
        )]

    def get_subscribed_events(self) -> list[str]:
        return list(_SUBSCRIBED_EVENTS)


def _extract_magnitude(event: Event) -> Decimal | None:
    """Return the primary scalar magnitude from an event's affected_attributes."""
    if not event.affected_attributes:
        return None
    qty = event.affected_attributes.get(event.event_type)
    if qty is None:
        qty = next(iter(event.affected_attributes.values()))
    return qty.value


def _event_confidence_tier(event: Event) -> int:
    """Return the max confidence_tier across an event's affected_attributes."""
    if not event.affected_attributes:
        return 2
    return max(q.confidence_tier for q in event.affected_attributes.values())
