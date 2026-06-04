"""
Matrix engine interpretability tools — ADR-009 §Decision 4.

Four required tools for M11 delivery:
  1. propagation_trace  — records which entities received deltas and via how many
                          hops, for one propagate_matrix() call.
  2. visualize_weight_matrix — renders an N×N weight matrix as an ASCII table
                          suitable for CI log output and debug inspection.
  3. profile_propagation — reports sparsity, non-zero counts, and per-hop
                          delta magnitude for one propagate_matrix() call.
  4. (equivalence harness — in test_equivalence_harness.py per ADR-009 §Decision 4)

All tools are pure-Python (no I/O, no side effects). They accept the same
inputs as propagate_matrix() plus captured carry snapshots, making them
safe to call in test, CI, and debug contexts without touching the database
or any simulation state.

Usage example:
    from app.simulation.engine.matrix_tools import trace_propagation
    trace = trace_propagation(state, events)
    for hop, entity_id, attrs in trace.hops:
        print(f"hop={hop} entity={entity_id} attrs={attrs}")
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

import numpy as np
import numpy.typing as npt

from app.simulation.engine.matrix_propagation import (
    _build_weight_matrix,
    _matrix_cascade_hop,
    _matrix_linear_hop,
    _matrix_threshold_hop,
)
from app.simulation.engine.models import (
    Event,
    PropagationMode,
    SimulationState,
)
from app.simulation.engine.quantity import Quantity

_DeltaAccumulator = dict[str, dict[str, Quantity]]


# ---------------------------------------------------------------------------
# Tool 1 — Propagation trace
# ---------------------------------------------------------------------------


@dataclass
class HopRecord:
    """One entity-level delta record from one propagation hop."""

    hop: int
    """Hop number (1-indexed). Hop 0 = direct source accumulation."""

    entity_id: str
    """Entity that received this delta."""

    event_id: str
    """Source event."""

    rule_relationship_type: str
    """Relationship type that carried this delta."""

    attr_deltas: dict[str, Decimal]
    """attribute_key → delta value (Decimal) accumulated at this entity."""


@dataclass
class PropagationTrace:
    """Complete trace for one propagate_matrix() call.

    Attributes:
        hops: All hop records produced, in emission order.
        n_events: Number of events processed.
        n_entities: Number of entities in the state.
        n_relationships: Total relationships across all types.
    """

    hops: list[HopRecord] = field(default_factory=list)
    n_events: int = 0
    n_entities: int = 0
    n_relationships: int = 0

    def entities_reached(self) -> set[str]:
        """Return the set of entity IDs that received any non-zero delta."""
        return {r.entity_id for r in self.hops}

    def max_hop_depth(self) -> int:
        """Return the maximum hop depth reached across all events."""
        if not self.hops:
            return 0
        return max(r.hop for r in self.hops)

    def summary(self) -> str:
        """Return a one-line human-readable summary."""
        return (
            f"PropagationTrace: {self.n_events} events, "
            f"{len(self.entities_reached())} entities reached, "
            f"max hop depth {self.max_hop_depth()}"
        )


def trace_propagation(state: SimulationState, events: list[Event]) -> PropagationTrace:
    """Run matrix propagation and record per-hop entity deltas.

    Equivalent to propagate_matrix() but also captures which entity received
    what delta at which hop for each event. The simulation state returned by
    propagate_matrix() is not reproduced here — call propagate_matrix()
    separately if you need the next state alongside the trace.

    Args:
        state: Simulation state (State[T]). Read-only.
        events: Events to trace.

    Returns:
        PropagationTrace with all hop records filled in.
    """
    entity_ids: list[str] = list(state.entities.keys())
    entity_idx: dict[str, int] = {eid: i for i, eid in enumerate(entity_ids)}
    N = len(entity_ids)

    trace = PropagationTrace(
        n_events=len(events),
        n_entities=N,
        n_relationships=len(state.relationships),
    )

    for event in events:
        source_idx = entity_idx.get(event.source_entity_id)
        if source_idx is None:
            continue

        attr_keys = list(event.affected_attributes.keys())
        attr_quantities = [event.affected_attributes[k] for k in attr_keys]
        n_attrs = len(attr_keys)
        if n_attrs == 0:
            continue

        # Hop 0: direct source accumulation
        trace.hops.append(HopRecord(
            hop=0,
            entity_id=event.source_entity_id,
            event_id=event.event_id,
            rule_relationship_type="(direct)",
            attr_deltas={k: q.value for k, q in event.affected_attributes.items()},
        ))

        base_values: npt.NDArray[np.float64] = np.array(
            [float(q.value) for q in attr_quantities], dtype=np.float64
        )

        for rule in event.propagation_rules:
            W: npt.NDArray[np.float64] = _build_weight_matrix(
                state, entity_idx, N, rule.relationship_type
            )
            if not np.any(W != 0.0):
                continue

            carry: npt.NDArray[np.float64] = np.zeros((N, n_attrs), dtype=np.float64)
            carry[source_idx, :] = base_values
            safe_a = rule.attenuation_factor if rule.attenuation_factor > 0.0 else 1.0

            for hop_num in range(1, rule.max_hops + 1):
                if rule.propagation_mode == PropagationMode.CASCADE:
                    carry = _matrix_cascade_hop(
                        carry, W, safe_a, rule.ceiling, base_values
                    )
                elif rule.propagation_mode == PropagationMode.THRESHOLD:
                    carry = _matrix_threshold_hop(
                        carry, W, rule.attenuation_factor, rule.threshold
                    )
                else:
                    carry = _matrix_linear_hop(carry, W, rule.attenuation_factor)

                for j, eid in enumerate(entity_ids):
                    row = carry[j, :]
                    if not np.any(row != 0.0):
                        continue
                    attr_deltas = {
                        attr_keys[a_idx]: Decimal(str(float(row[a_idx])))
                        for a_idx in range(n_attrs)
                        if float(row[a_idx]) != 0.0
                    }
                    if attr_deltas:
                        trace.hops.append(HopRecord(
                            hop=hop_num,
                            entity_id=eid,
                            event_id=event.event_id,
                            rule_relationship_type=rule.relationship_type,
                            attr_deltas=attr_deltas,
                        ))

                if not np.any(carry != 0.0):
                    break

    return trace


# ---------------------------------------------------------------------------
# Tool 2 — Weight matrix visualizer
# ---------------------------------------------------------------------------


def visualize_weight_matrix(
    state: SimulationState,
    relationship_type: str,
    precision: int = 3,
    max_entities: int = 20,
) -> str:
    """Render the weight matrix for one relationship type as an ASCII table.

    Outputs a plain-text matrix where rows are target entities and columns
    are source entities. Non-zero entries show the propagation weight.

    Args:
        state: Simulation state providing entity IDs and relationships.
        relationship_type: The relationship type to visualize.
        precision: Decimal places for weight display.
        max_entities: Truncate at this many entities to keep output readable.

    Returns:
        Multi-line ASCII string suitable for CI log and debug output.
    """
    entity_ids = list(state.entities.keys())[:max_entities]
    N = len(entity_ids)
    entity_idx = {eid: i for i, eid in enumerate(entity_ids)}
    W: npt.NDArray[np.float64] = _build_weight_matrix(state, entity_idx, N, relationship_type)

    n_nonzero = int(np.count_nonzero(W))
    density = n_nonzero / (N * N) if N > 0 else 0.0
    truncated = len(state.entities) > max_entities

    lines: list[str] = [
        f"Weight matrix — relationship_type={relationship_type!r}",
        f"  Entities: {N}{' (truncated)' if truncated else ''} | "
        f"Non-zero edges: {n_nonzero} | Density: {density:.1%}",
        "",
    ]

    if N == 0:
        lines.append("  (no entities)")
        return "\n".join(lines)

    col_w = max(precision + 4, 8)
    id_w = max(len(eid) for eid in entity_ids) + 2

    # Header row
    header = " " * id_w + "".join(f"{eid:>{col_w}}" for eid in entity_ids)
    lines.append(header)
    lines.append(" " * id_w + "-" * (col_w * N))

    # Data rows
    for i, tgt_id in enumerate(entity_ids):
        row_vals = []
        for j in range(N):
            v = W[i, j]
            if v == 0.0:
                row_vals.append(" " * col_w)
            else:
                row_vals.append(f"{v:>{col_w}.{precision}f}")
        lines.append(f"{tgt_id:<{id_w}}" + "".join(row_vals))

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Tool 3 — Sparse profiler
# ---------------------------------------------------------------------------


@dataclass
class PropagationProfile:
    """Sparsity and magnitude profile for one propagate_matrix() call.

    Attributes:
        n_entities: Number of entities in the state.
        n_relationships: Total relationships across all types.
        n_events: Events processed.
        relationship_type_counts: {relationship_type: edge count}.
        per_hop_stats: {hop: {"max_abs": float, "n_nonzero_entities": int}}
    """

    n_entities: int
    n_relationships: int
    n_events: int
    relationship_type_counts: dict[str, int] = field(default_factory=dict)
    per_hop_stats: dict[int, dict[str, float | int]] = field(default_factory=dict)

    def sparsity(self) -> float:
        """Overall edge density (fraction of possible N×N slots that are non-zero)."""
        if self.n_entities == 0:
            return 0.0
        possible = self.n_entities * self.n_entities
        total_edges = sum(self.relationship_type_counts.values())
        return total_edges / possible

    def summary(self) -> str:
        """One-line human-readable summary."""
        return (
            f"PropagationProfile: {self.n_entities} entities, "
            f"{self.n_relationships} relationships, "
            f"sparsity={self.sparsity():.1%}, "
            f"{self.n_events} events"
        )


def profile_propagation(
    state: SimulationState, events: list[Event]
) -> PropagationProfile:
    """Profile the matrix propagation without altering the simulation state.

    Collects sparsity statistics and per-hop delta magnitude data.
    No state mutation; safe to call before or after propagate_matrix().

    Args:
        state: Simulation state (State[T]). Read-only.
        events: Events to profile.

    Returns:
        PropagationProfile with sparsity and per-hop magnitude statistics.
    """
    entity_ids = list(state.entities.keys())
    entity_idx = {eid: i for i, eid in enumerate(entity_ids)}
    N = len(entity_ids)

    # Count relationship types
    rel_type_counts: dict[str, int] = {}
    for rel in state.relationships:
        rel_type_counts[rel.relationship_type] = (
            rel_type_counts.get(rel.relationship_type, 0) + 1
        )

    profile = PropagationProfile(
        n_entities=N,
        n_relationships=len(state.relationships),
        n_events=len(events),
        relationship_type_counts=rel_type_counts,
    )

    for event in events:
        source_idx = entity_idx.get(event.source_entity_id)
        if source_idx is None:
            continue

        attr_keys = list(event.affected_attributes.keys())
        attr_quantities = [event.affected_attributes[k] for k in attr_keys]
        n_attrs = len(attr_keys)
        if n_attrs == 0:
            continue

        base_values: npt.NDArray[np.float64] = np.array(
            [float(q.value) for q in attr_quantities], dtype=np.float64
        )

        for rule in event.propagation_rules:
            W: npt.NDArray[np.float64] = _build_weight_matrix(
                state, entity_idx, N, rule.relationship_type
            )
            if not np.any(W != 0.0):
                continue

            carry: npt.NDArray[np.float64] = np.zeros((N, n_attrs), dtype=np.float64)
            carry[source_idx, :] = base_values
            safe_a = rule.attenuation_factor if rule.attenuation_factor > 0.0 else 1.0

            for hop_num in range(1, rule.max_hops + 1):
                if rule.propagation_mode == PropagationMode.CASCADE:
                    carry = _matrix_cascade_hop(
                        carry, W, safe_a, rule.ceiling, base_values
                    )
                elif rule.propagation_mode == PropagationMode.THRESHOLD:
                    carry = _matrix_threshold_hop(
                        carry, W, rule.attenuation_factor, rule.threshold
                    )
                else:
                    carry = _matrix_linear_hop(carry, W, rule.attenuation_factor)

                max_abs = float(np.max(np.abs(carry))) if carry.size > 0 else 0.0
                n_nonzero = int(np.count_nonzero(np.any(carry != 0.0, axis=1)))

                # Merge stats across events at the same hop depth
                existing = profile.per_hop_stats.get(hop_num)
                if existing is None:
                    profile.per_hop_stats[hop_num] = {
                        "max_abs": max_abs,
                        "n_nonzero_entities": n_nonzero,
                    }
                else:
                    profile.per_hop_stats[hop_num] = {
                        "max_abs": max(float(existing["max_abs"]), max_abs),
                        "n_nonzero_entities": max(
                            int(existing["n_nonzero_entities"]), n_nonzero
                        ),
                    }

                if not np.any(carry != 0.0):
                    break

    return profile
