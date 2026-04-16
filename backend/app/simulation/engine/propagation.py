"""
Event propagation engine — ADR-001.

Implements the graph traversal that applies Events to SimulationState[T]
and produces SimulationState[T+1]. This module owns state transitions.
Simulation modules return Events. The propagation engine applies them.

Architecture contracts (ADR-001):
- State[T] is never mutated. State[T+1] is constructed fresh.
- The source entity always receives the full unattenuated delta.
- Propagation follows PropagationRules hop-by-hop along relationship edges
  of the specified type, attenuating by (attenuation_factor * edge.weight)
  at each hop. Attenuation compounds across hops.
- Deltas accumulate additively: multiple events and multiple propagation
  paths to the same entity are summed before being applied.
- Deltas for entity_ids not present in state.entities are silently dropped.
  A relationship may reference an entity outside the active resolution scope.
"""

from __future__ import annotations

from app.simulation.engine.models import (
    Event,
    PropagationRule,
    SimulationEntity,
    SimulationState,
)

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

# Accumulator maps entity_id -> {attribute_key -> total_delta}
_DeltaAccumulator = dict[str, dict[str, float]]


def propagate(state: SimulationState, events: list[Event]) -> SimulationState:
    """Apply a list of events to State[T] and return State[T+1].

    The engine collects all attribute deltas produced by the events and their
    graph traversals, then applies them in a single pass to construct the next
    state. State[T] is never modified.

    Args:
        state: Current simulation state (State[T]). Treated as read-only.
        events: Events produced by simulation modules this timestep.

    Returns:
        New SimulationState (State[T+1]) with all event deltas applied.
    """
    accumulator: _DeltaAccumulator = {}

    for event in events:
        _apply_event(state, event, accumulator)

    return _build_next_state(state, accumulator)


# ---------------------------------------------------------------------------
# Private — event application
# ---------------------------------------------------------------------------


def _apply_event(
    state: SimulationState,
    event: Event,
    accumulator: _DeltaAccumulator,
) -> None:
    """Collect all deltas for one event into the accumulator.

    The source entity always receives the full unattenuated delta. Each
    PropagationRule then drives a separate graph traversal that attenuates
    and distributes the delta across connected entities.

    Args:
        state: Simulation state used for relationship traversal.
        event: The event to apply and propagate.
        accumulator: Mutable accumulator updated in place.
    """
    _accumulate(accumulator, event.source_entity_id, event.affected_attributes)

    for rule in event.propagation_rules:
        _propagate_rule(
            state,
            event.affected_attributes,
            event.source_entity_id,
            rule,
            accumulator,
        )


def _propagate_rule(
    state: SimulationState,
    base_delta: dict[str, float],
    source_entity_id: str,
    rule: PropagationRule,
    accumulator: _DeltaAccumulator,
) -> None:
    """Traverse the relationship graph for one PropagationRule.

    Processes hops iteratively. The frontier at each hop carries the
    already-attenuated delta from the previous hop, so attenuation compounds:
    a two-hop chain applies (attenuation * weight) twice.

    Multiple frontier entries may reach the same target entity (converging
    paths). Both contributions are accumulated additively — the engine makes
    no attempt to deduplicate paths.

    Args:
        state: Simulation state providing relationship queries.
        base_delta: Full unattenuated delta from the event source.
        source_entity_id: Entity where this propagation begins.
        rule: Controls which edge types to traverse and how to attenuate.
        accumulator: Mutable accumulator updated in place.
    """
    # frontier: (entity_id, delta_carried_from_previous_hop)
    frontier: list[tuple[str, dict[str, float]]] = [(source_entity_id, base_delta)]

    for _ in range(rule.max_hops):
        next_frontier: list[tuple[str, dict[str, float]]] = []

        for entity_id, current_delta in frontier:
            for rel in state.get_relationships_from(entity_id):
                if rel.relationship_type != rule.relationship_type:
                    continue
                attenuated = _attenuate(current_delta, rule.attenuation_factor, rel.weight)
                _accumulate(accumulator, rel.target_id, attenuated)
                next_frontier.append((rel.target_id, attenuated))

        frontier = next_frontier
        if not frontier:
            break


# ---------------------------------------------------------------------------
# Private — delta arithmetic
# ---------------------------------------------------------------------------


def _attenuate(
    delta: dict[str, float],
    attenuation_factor: float,
    relationship_weight: float,
) -> dict[str, float]:
    """Scale a delta by one hop's attenuation.

    The combined scale is attenuation_factor * relationship_weight. For a
    delta of 0.15, attenuation_factor 0.4, and weight 0.30, the result is
    0.15 * 0.4 * 0.30 = 0.018, matching the diagram in ADR-001.

    Args:
        delta: Attribute deltas from the sending entity at this hop.
        attenuation_factor: Rule-level per-hop decay (in [0.0, 1.0]).
        relationship_weight: Edge-level coupling strength (in [0.0, 1.0]).

    Returns:
        New dict with each delta value scaled by attenuation_factor * weight.
    """
    scale = attenuation_factor * relationship_weight
    return {k: v * scale for k, v in delta.items()}


def _accumulate(
    accumulator: _DeltaAccumulator,
    entity_id: str,
    deltas: dict[str, float],
) -> None:
    """Add deltas to the accumulator for one entity.

    Multiple calls for the same entity sum their contributions. This is the
    mechanism by which converging propagation paths accumulate correctly.

    Args:
        accumulator: Mutable accumulator mapping entity_id to attr deltas.
        entity_id: The entity receiving this delta contribution.
        deltas: Attribute key -> delta value to add.
    """
    if entity_id not in accumulator:
        accumulator[entity_id] = {}
    entity_deltas = accumulator[entity_id]
    for key, delta in deltas.items():
        entity_deltas[key] = entity_deltas.get(key, 0.0) + delta


# ---------------------------------------------------------------------------
# Private — state construction
# ---------------------------------------------------------------------------


def _build_next_state(
    state: SimulationState,
    accumulator: _DeltaAccumulator,
) -> SimulationState:
    """Construct State[T+1] by applying accumulated deltas to fresh entity copies.

    Every entity in state.entities receives a new attributes dict. Entities
    with accumulated deltas have those deltas applied via addition. Entities
    with no deltas are copied with their attributes unchanged. Accumulated
    deltas for entity_ids absent from state.entities are dropped.

    Args:
        state: State[T] — read only, never mutated.
        accumulator: All attribute deltas to apply, keyed by entity_id.

    Returns:
        New SimulationState with updated entity attribute values.
    """
    new_entities: dict[str, SimulationEntity] = {}

    for entity_id, entity in state.entities.items():
        new_attrs = dict(entity.attributes)

        if entity_id in accumulator:
            for key, delta in accumulator[entity_id].items():
                new_attrs[key] = new_attrs.get(key, 0.0) + delta

        new_entities[entity_id] = SimulationEntity(
            id=entity.id,
            entity_type=entity.entity_type,
            attributes=new_attrs,
            metadata=entity.metadata,
            parent_id=entity.parent_id,
            geometry=entity.geometry,
        )

    return SimulationState(
        timestep=state.timestep,
        resolution=state.resolution,
        entities=new_entities,
        relationships=state.relationships,
        events=state.events,
        scenario_config=state.scenario_config,
    )
