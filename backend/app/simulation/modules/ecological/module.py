"""EcologicalModule — ADR-005 Amendment 1.

Subscribes to macro, fiscal, and emergency events on country entities and
applies the ecological elasticity matrix to produce ecological indicator
Quantity-delta Events with framework=MeasurementFramework.ECOLOGICAL.

One-step lag design: reads state.events (prior step). Ecological effects of
GDP changes and fiscal spending cuts appear with a structural delay, consistent
with annual indicator measurement cycles (NASA/NOAA Mauna Loa CO2 series,
FAO Global Forest Resources Assessment 5-year cycle).

Indicators produced at M6 minimum viable scope:
  co2_concentration_ppm — STOCK (VariableType.STOCK); confidence_tier 1
    (NASA/NOAA direct measurement). Tracks country contribution to
    atmospheric CO2 trajectory via GDP-emissions coupling.
  land_use_pressure_index — RATIO (VariableType.RATIO); confidence_tier 3
    (FAO GFR 5-year data, annual interpolation required). Tracks the fraction
    of the safe land-system boundary consumed by the entity's land-use change
    trajectory.

ADR-005 Amendment B mandatory note: the ecological composite score in
MultiFrameworkOutput uses cross-entity percentile rank at M6 scope.
Planetary boundary absolute normalization is methodologically preferred and
is deferred to M8. This note appears on every ecological FrameworkOutput
via scenarios.py — it is not this module's responsibility to set it.

Implicit dependency: subscribes to gdp_growth_change which only fires when
MacroeconomicModule is active. If MacroeconomicModule is absent, GDP-mediated
ecological effects are silently absent. Enforcement tracked in Issue #211 (M7).
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
from app.simulation.modules.ecological.elasticities import ECOLOGICAL_ELASTICITY_REGISTRY

if TYPE_CHECKING:
    from datetime import datetime

_log = logging.getLogger(__name__)

_SUBSCRIBED_EVENTS = frozenset({
    "gdp_growth_change",
    "fiscal_policy_spending_change",
    "emergency_declaration",
})

# variable_type per ADR-005 Amendment B and approved-sources.md:
#   co2_concentration_ppm — STOCK (level at a point in time)
#   land_use_pressure_index — RATIO (fraction of boundary threshold)
_INDICATOR_VARIABLE_TYPES: dict[str, VariableType] = {
    "co2_concentration_ppm": VariableType.STOCK,
    "land_use_pressure_index": VariableType.RATIO,
}

# Canonical unit strings per DATA_STANDARDS.md §Canonical Unit Registry (Gap 1).
# co2_concentration_ppm: atmospheric concentration in parts per million.
# land_use_pressure_index: fraction of planetary boundary threshold consumed (0–1).
# Default "ratio_0_1" applies to any future ecological indicator not yet listed here.
_INDICATOR_UNITS: dict[str, str] = {
    "co2_concentration_ppm": "ppm",
    "land_use_pressure_index": "ratio_0_1",
}
_DEFAULT_ECOLOGICAL_UNIT = "ratio_0_1"


class EcologicalModule(SimulationModule):
    """Translates country-level events into ecological indicator deltas.

    M6 minimum viable scope: co2_concentration_ppm and land_use_pressure_index.
    Full planetary boundary indicator set (planetary_boundary_proximity,
    co2_trajectory, deforestation_rate) added at M8 alongside boundary-normalized
    composite score methodology (ADR-005 Amendment 1 §Amendment B M8 obligation).
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
            for row in ECOLOGICAL_ELASTICITY_REGISTRY:
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
                unit=_INDICATOR_UNITS.get(key, _DEFAULT_ECOLOGICAL_UNIT),
                variable_type=_INDICATOR_VARIABLE_TYPES.get(key, VariableType.RATIO),
                measurement_framework=MeasurementFramework.ECOLOGICAL,
                confidence_tier=indicator_tiers[key],
            )
            for key, delta in indicator_deltas.items()
        }

        return [Event(
            event_id=f"eco-{entity.id}-{timestep.isoformat()}",
            source_entity_id=entity.id,
            event_type="ecological_indicator_update",
            affected_attributes=affected_attributes,
            propagation_rules=[],
            timestep_originated=timestep,
            framework=MeasurementFramework.ECOLOGICAL,
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
