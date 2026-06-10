"""EcologicalModule — ADR-005 Amendment 1, expanded at M8 (Amendment 3 Decision M8-6).

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

M8 expansion (ADR-005 Amendment 3 Decision M8-6) — stock-path proximity indicators:
  planetary_boundary_co2_proximity — min(co2_concentration_ppm / 350, 2.0)
    Confidence tier 2: max(source_tier=1, boundary_tier=2). Boundary effective
    from 2009-09-24 (Rockström 2009, Nature). Temporal guard: not computed if
    simulation timestep precedes effective_from.
  planetary_boundary_land_use_proximity — min(land_use_pressure_index, 2.0)
    No division by 0.25 — land_use_pressure_index is already boundary-relative
    (double-normalization prevention, ADR-005 Amendment 3 Decision M8-6).
    Confidence tier 3: max(source_tier=3, boundary_tier=2). Boundary effective
    from 2023-09-13 (Richardson 2023, Science Advances).

Proximity computation reads entity.attributes (accumulated stock values), not
state.events (deltas). Delta computation continues to read state.events. Both
paths run independently and are merged into a single event per step.

Implicit dependency: subscribes to gdp_growth_change which only fires when
MacroeconomicModule is active. If MacroeconomicModule is absent, GDP-mediated
ecological effects are silently absent. Enforcement tracked in Issue #211 (M7).
"""
from __future__ import annotations

import logging
from datetime import UTC, datetime
from decimal import Decimal

from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
    SimulationEntity,
    SimulationModule,
    SimulationState,
)
from app.simulation.engine.quantity import Quantity, VariableType
from app.simulation.modules.ecological.elasticities import ECOLOGICAL_ELASTICITY_REGISTRY

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

# ---------------------------------------------------------------------------
# M8 boundary proximity constants — ADR-005 Amendment 3 Decision M8-6
# ---------------------------------------------------------------------------

# Hardcoded boundary values matching simulation_reference_constants seed (migration b3c5d7e9f1a2).
# Used for proximity computation in the simulation engine (sync context).
# The DB query in scenarios.py validates temporal availability at read time.
_BOUNDARY_CONSTANT_VALUES: dict[str, Decimal] = {
    "ECOLOGICAL_CO2_PLANETARY_BOUNDARY_PPM": Decimal("350"),
    "ECOLOGICAL_LAND_USE_PLANETARY_BOUNDARY_RATIO": Decimal("0.25"),
}

# effective_from dates matching the simulation_reference_constants table rows.
_BOUNDARY_CONSTANT_EFFECTIVE_FROM: dict[str, datetime] = {
    "ECOLOGICAL_CO2_PLANETARY_BOUNDARY_PPM": datetime(2009, 9, 24, tzinfo=UTC),
    "ECOLOGICAL_LAND_USE_PLANETARY_BOUNDARY_RATIO": datetime(2023, 9, 13, tzinfo=UTC),
}

# Maps base indicator key →
#   (constant_id, is_pre_normalized, output_key, confidence_tier, retroactive)
# is_pre_normalized=True: formula is min(v, 2.0) — indicator already boundary-relative.
# is_pre_normalized=False: formula is min(v / boundary_value, 2.0).
# confidence_tier = max(source_indicator_tier, boundary_constant_tier=2) per ADR-001 Amendment 1.
# retroactive=True: boundary may be applied to simulation timesteps before effective_from.
#   Rationale: the CO2 350 ppm boundary is a physical threshold derived from pre-industrial
#   concentrations — it predates its scientific publication (Rockström 2009). Retroactive
#   backtesting against historical data is analytically valid.
# retroactive=False: boundary is not applicable before effective_from.
#   Rationale: the Richardson 2023 land-use boundary reflects new methodology not available
#   for pre-2023 analysis.
_PROXIMITY_INDICATOR_CONFIG: dict[str, tuple[str, bool, str, int, bool]] = {
    "co2_concentration_ppm": (
        "ECOLOGICAL_CO2_PLANETARY_BOUNDARY_PPM",
        False,   # absolute-scale ppm — divide by 350
        "planetary_boundary_co2_proximity",
        2,       # max(source=1, boundary=2) = 2
        True,    # retroactive: physical threshold, valid for pre-2009 backtesting
    ),
    "land_use_pressure_index": (
        "ECOLOGICAL_LAND_USE_PLANETARY_BOUNDARY_RATIO",
        True,    # already boundary-relative ratio — no division (ADR M8-6: no double-normalization)
        "planetary_boundary_land_use_proximity",
        3,       # max(source=3, boundary=2) = 3
        False,   # not retroactive: Richardson 2023 methodology, not valid for pre-2023 analysis
    ),
}


def _compute_proximity_indicators(
    entity: SimulationEntity,
    timestep: datetime,
) -> dict[str, Quantity]:
    """Compute planetary boundary proximity scores from entity stock attributes.

    Reads entity.attributes (accumulated STOCK values), not state.events (deltas).
    Only computes proximity for boundary constants active at simulation timestep.
    Emits [SIM-INTEGRITY] WARNING when base attribute is absent or boundary constant
    is not yet temporally active. ADR-005 Amendment 3 Decision M8-6.
    """
    result: dict[str, Quantity] = {}

    for base_key, (constant_id, is_pre_normalized, output_key, confidence_tier, retroactive) in \
            _PROXIMITY_INDICATOR_CONFIG.items():
        effective_from = _BOUNDARY_CONSTANT_EFFECTIVE_FROM.get(constant_id)
        if effective_from is not None and not retroactive and timestep < effective_from:
            _log.warning(
                "[SIM-INTEGRITY] Boundary constant '%s' not active at timestep=%r "
                "(effective_from=%r) — skipping proximity for '%s'.",
                constant_id,
                timestep,
                effective_from,
                output_key,
            )
            continue

        stock_qty = entity.attributes.get(base_key)
        if stock_qty is None:
            _log.warning(
                "[SIM-INTEGRITY] Base attribute '%s' absent from entity '%s' attributes "
                "— cannot compute '%s'. Proximity requires at least one prior step "
                "with EcologicalModule active.",
                base_key,
                entity.id,
                output_key,
            )
            continue

        try:
            stock_val = Decimal(str(stock_qty.value))
        except Exception:  # noqa: BLE001, S112
            continue

        if is_pre_normalized:
            proximity = max(Decimal("0"), min(stock_val, Decimal("2.0")))
        else:
            boundary_val = _BOUNDARY_CONSTANT_VALUES.get(constant_id, Decimal("1"))
            if boundary_val == Decimal("0"):
                continue
            proximity = max(Decimal("0"), min(stock_val / boundary_val, Decimal("2.0")))

        result[output_key] = Quantity(
            value=proximity.quantize(Decimal("0.000001")),
            unit="ratio_0_1",
            variable_type=VariableType.STOCK,
            measurement_framework=MeasurementFramework.ECOLOGICAL,
            confidence_tier=confidence_tier,
        )

    return result


class EcologicalModule(SimulationModule):
    """Translates country-level events into ecological indicator deltas.

    M6 minimum viable scope: co2_concentration_ppm and land_use_pressure_index.
    Full planetary boundary indicator set (planetary_boundary_proximity,
    co2_trajectory, deforestation_rate) added at M8 alongside boundary-normalized
    composite score methodology (ADR-005 Amendment 1 §Amendment B M8 obligation).
    """

    # INTENT: Produce ecological indicator events for one country entity per step.
    #         Two independent computation paths merged into a single event:
    #         (1) Stock path — planetary boundary proximity from entity.attributes
    #             accumulated stock values (ADR-005 Amendment 3 Decision M8-6).
    #         (2) Delta path — indicator deltas from prior-step events via the
    #             elasticity registry (one-step lag design, M6 scope).
    # PRECONDITIONS: entity is a SimulationEntity with entity_type; state.events
    #                contains the prior timestep's events (one-step lag design);
    #                timestep is the current simulation step.
    # POSTCONDITIONS: Returns a list of Events with framework=ECOLOGICAL and
    #                 event_type='ecological_indicator_update'; returns [] for
    #                 non-country entities or when both paths produce no attributes.
    #                 All Quantity values use Decimal arithmetic. A DEBUG log is
    #                 emitted when prior_events is empty.
    # ERROR CASES: Subscribed events with no matching elasticity registry entry
    #              produce no delta output (silently ignored). Missing stock
    #              attributes or temporally inactive boundary constants produce
    #              [SIM-INTEGRITY] WARNING and skip that proximity indicator.
    # KNOWN LIMITATIONS: Ecological effects are computed via a linear elasticity
    #                    approximation — non-linear threshold effects and
    #                    irreversibility are not modelled. Proximity computation
    #                    requires entity.attributes to be populated from prior steps;
    #                    on the first step with no prior ecological events, proximity
    #                    attributes will be absent.
    def compute(
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime,
    ) -> list[Event]:
        if entity.entity_type != "country":
            return []

        affected_attributes: dict[str, Quantity] = {}

        # Stock path: compute proximity indicators from accumulated entity attributes.
        affected_attributes.update(_compute_proximity_indicators(entity, timestep))

        # Delta path: compute indicator deltas from prior-step subscribed events.
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
        else:
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

            for key, delta in indicator_deltas.items():
                vtype = _INDICATOR_VARIABLE_TYPES.get(key, VariableType.RATIO)
                if vtype == VariableType.STOCK:
                    # STOCK propagation replaces the current value, so the event
                    # must carry the new absolute level (current + elasticity change).
                    current_qty = entity.attributes.get(key)
                    current_val = (
                        Decimal(str(current_qty.value))
                        if current_qty is not None
                        else Decimal("0")
                    )
                    emit_value = current_val + delta
                else:
                    emit_value = delta
                affected_attributes[key] = Quantity(
                    value=emit_value,
                    unit=_INDICATOR_UNITS.get(key, _DEFAULT_ECOLOGICAL_UNIT),
                    variable_type=vtype,
                    measurement_framework=MeasurementFramework.ECOLOGICAL,
                    confidence_tier=indicator_tiers[key],
                )

        if not affected_attributes:
            return []

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
