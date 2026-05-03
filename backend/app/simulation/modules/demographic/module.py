"""DemographicModule — ADR-005 Decision 1.

Subscribes to fiscal and policy events on country entities and applies
the elasticity matrix to generate Quantity-delta Events targeting the
affected cohort child entities.

The module reacts to events from the *previous* timestep (state.events),
which is the correct one-step lag: demographic effects of fiscal policy
changes appear with a structural delay in real economies.
"""
from __future__ import annotations

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
from app.simulation.modules.demographic.elasticities import ELASTICITY_REGISTRY

if TYPE_CHECKING:
    from datetime import datetime

_SUBSCRIBED_EVENTS = frozenset({
    "gdp_growth_change",
    "imf_program_acceptance",
    "capital_controls_imposition",
    "emergency_declaration",
})


class DemographicModule(SimulationModule):
    """Translates country-level policy events into cohort attribute deltas."""

    def __init__(
        self,
        cohort_resolution_entity_ids: list[str] | None = None,
    ) -> None:
        self._active_ids: frozenset[str] = frozenset(cohort_resolution_entity_ids or [])

    def compute(
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime,
    ) -> list[Event]:
        if entity.entity_type != "country":
            return []
        if self._active_ids and entity.id not in self._active_ids:
            return []

        prior_events = [
            e for e in state.events
            if e.source_entity_id == entity.id and e.event_type in _SUBSCRIBED_EVENTS
        ]
        if not prior_events:
            return []

        result: list[Event] = []
        for event in prior_events:
            magnitude = _extract_magnitude(event)
            if magnitude is None:
                continue
            for row in ELASTICITY_REGISTRY:
                if row.event_type != event.event_type:
                    continue
                delta = (magnitude * row.elasticity).quantize(Decimal("0.000001"))
                qty = Quantity(
                    value=delta,
                    unit="dimensionless",
                    variable_type=VariableType.RATIO,
                    measurement_framework=MeasurementFramework.HUMAN_DEVELOPMENT,
                    confidence_tier=row.confidence_tier,
                )
                cohort_id = row.cohort_spec.entity_id(entity.id)
                result.append(Event(
                    event_id=(
                        f"demo-{entity.id}-{cohort_id}"
                        f"-{row.attribute_key}-{timestep.isoformat()}"
                    ),
                    source_entity_id=entity.id,
                    event_type="demographic_cohort_delta",
                    affected_attributes={row.attribute_key: qty},
                    propagation_rules=[],
                    timestep_originated=timestep,
                    framework=MeasurementFramework.HUMAN_DEVELOPMENT,
                    metadata={"target_entity_id": cohort_id},
                ))
        return result

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
