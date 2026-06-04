"""
Matrix computation engine — ADR-009 (Simulation Engine Computation Model).

Implements event propagation using NumPy dense matrix operations. Runs
ALONGSIDE the iterative engine (propagation.py) for the parallel-run phase
mandated by ADR-009 §Decision 1. Public API is a drop-in mirror of propagate().

Mathematical formulation (ADR-009 §Engine Computation Model):
  Weight matrix W (N×N float64):
    W[target_idx, source_idx] = relationship.weight for edges of the
    rule's relationship_type. Zero for all absent edges.

  Source entity receives the full unattenuated delta via _accumulate
  (Decimal arithmetic, identical to iterative engine).

  Per-hop propagation (carry starts at source delta, shape N×n_attrs):
    LINEAR:    carry = a * W @ carry.  Always accumulated.
    THRESHOLD: carry = a * W @ carry.  Rows with max |delta| < threshold
               are zeroed and excluded from accumulation and next hop.
    CASCADE:   carry = (1/a) * W @ carry.  Ceiling-clipped per column
               at ceiling × |base_values| before accumulation.

  Decimal↔float64 boundary (ADR-009 §Decision 5): delta values cross
  float64 for matrix operations only; return via Decimal(str(float_value)).
  Propagation weights and attenuation factors are dimensionless float64
  throughout.

Semantic notes — documented divergence from iterative engine:
  THRESHOLD: The iterative engine checks the threshold per edge
    (each relationship independently). The matrix engine checks threshold
    on the summed per-entity contribution. Results diverge when multiple
    frontier entities converge on the same target with mixed above/below-
    threshold contributions. Single-path and single-source graphs produce
    identical output within ADR-009 §Decision 2 tolerance.
  CASCADE:   The iterative engine applies the ceiling cap before accumulating
    each individual path. The matrix engine applies the ceiling after summing
    converging paths. Results diverge on graphs with multiple frontier
    entities converging at the same target. Single-path graphs are identical.

Both divergences are confined to multi-path converging scenarios. The
equivalence harness (test_equivalence_harness.py) uses single-source,
single-path graphs where both engines are mathematically identical.
"""
from __future__ import annotations

import logging
from decimal import Decimal

import numpy as np
import numpy.typing as npt

from app.simulation.engine.models import (
    Event,
    PropagationMode,
    SimulationState,
)
from app.simulation.engine.propagation import _accumulate, _build_next_state
from app.simulation.engine.quantity import Quantity

_log = logging.getLogger(__name__)

_DeltaAccumulator = dict[str, dict[str, Quantity]]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def propagate_matrix(state: SimulationState, events: list[Event]) -> SimulationState:
    """Apply events to State[T] via matrix operations, return State[T+1].

    Drop-in mirror of propagation.propagate(). Both functions run in CI during
    the ADR-009 §Decision 1 parallel phase. Output must match propagate()
    within ADR-009 §Decision 2 tolerance (1e-10 on every Quantity.value)
    for the equivalence gate to pass.

    Args:
        state: Current simulation state (State[T]). Treated as read-only.
        events: Events produced by simulation modules this timestep.

    Returns:
        New SimulationState (State[T+1]) with all event deltas applied and
        State[T+1].events set to the current step's events (one-step lag).
    """
    entity_ids: list[str] = list(state.entities.keys())
    entity_idx: dict[str, int] = {eid: i for i, eid in enumerate(entity_ids)}
    N = len(entity_ids)

    accumulator: _DeltaAccumulator = {}

    for event in events:
        _apply_event_matrix(state, event, accumulator, entity_ids, entity_idx, N)

    return _build_next_state(state, accumulator, events)


# ---------------------------------------------------------------------------
# Private — event application
# ---------------------------------------------------------------------------


def _apply_event_matrix(
    state: SimulationState,
    event: Event,
    accumulator: _DeltaAccumulator,
    entity_ids: list[str],
    entity_idx: dict[str, int],
    N: int,
) -> None:
    """Apply one event to the accumulator via matrix propagation.

    Source entity receives the full unattenuated delta identically to
    the iterative engine (_accumulate called directly). Each propagation
    rule drives one matrix traversal over relationship edges.

    Args:
        state: Simulation state (read-only).
        event: Event to apply.
        accumulator: Mutable accumulator updated in place.
        entity_ids: Ordered entity IDs matching matrix row/column indices.
        entity_idx: entity_id → matrix index map.
        N: Number of entities (matrix dimension).
    """
    # Source entity always gets the full unattenuated delta — Decimal arithmetic,
    # identical to iterative engine (ADR-001 §source entity contract).
    _accumulate(accumulator, event.source_entity_id, event.affected_attributes)

    if not event.propagation_rules or N == 0:
        return

    source_idx = entity_idx.get(event.source_entity_id)
    if source_idx is None:
        _log.warning(
            "[SIM-INTEGRITY] Matrix engine: source entity %r not in state.entities "
            "— propagation rules skipped.",
            event.source_entity_id,
        )
        return

    attr_keys: list[str] = list(event.affected_attributes.keys())
    attr_quantities: list[Quantity] = [event.affected_attributes[k] for k in attr_keys]
    n_attrs = len(attr_keys)
    if n_attrs == 0:
        return

    # base_values: (n_attrs,) float64 — original source delta values.
    # Retained throughout for CASCADE ceiling reference (ADR-009 §Decision 5).
    base_values: npt.NDArray[np.float64] = np.array(
        [float(q.value) for q in attr_quantities], dtype=np.float64
    )

    for rule in event.propagation_rules:
        W: npt.NDArray[np.float64] = _build_weight_matrix(
            state, entity_idx, N, rule.relationship_type
        )
        if not np.any(W != 0.0):
            continue

        # carry: (N, n_attrs) float64 — delta at each entity for each attribute.
        # Starts non-zero only at source_idx.
        carry: npt.NDArray[np.float64] = np.zeros((N, n_attrs), dtype=np.float64)
        carry[source_idx, :] = base_values

        safe_a = rule.attenuation_factor if rule.attenuation_factor > 0.0 else 1.0

        for _ in range(rule.max_hops):
            if rule.propagation_mode == PropagationMode.CASCADE:
                carry = _matrix_cascade_hop(
                    carry, W, safe_a, rule.ceiling, base_values
                )
            elif rule.propagation_mode == PropagationMode.THRESHOLD:
                carry = _matrix_threshold_hop(
                    carry, W, rule.attenuation_factor, rule.threshold
                )
            else:  # LINEAR (default)
                carry = _matrix_linear_hop(carry, W, rule.attenuation_factor)

            _accumulate_matrix_carry(
                accumulator, carry, entity_ids, attr_keys, attr_quantities
            )

            if not np.any(carry != 0.0):
                break


# ---------------------------------------------------------------------------
# Private — matrix construction
# ---------------------------------------------------------------------------


def _build_weight_matrix(
    state: SimulationState,
    entity_idx: dict[str, int],
    N: int,
    relationship_type: str,
) -> npt.NDArray[np.float64]:
    """Build the N×N float64 weight matrix for one relationship type.

    W[target_idx, source_idx] = relationship.weight for all relationships
    of the specified type present in state.relationships. All other entries
    are zero.

    Relationships referencing entity IDs absent from entity_idx are silently
    dropped (mirrors iterative engine's dropped-delta warning behaviour; the
    relationship scope mismatch is logged upstream).

    Args:
        state: Simulation state providing relationship list.
        entity_idx: entity_id → matrix index map.
        N: Matrix dimension (number of entities).
        relationship_type: Only relationships of this type are included.

    Returns:
        (N, N) float64 NumPy array.
    """
    W = np.zeros((N, N), dtype=np.float64)
    for rel in state.relationships:
        if rel.relationship_type != relationship_type:
            continue
        src_i = entity_idx.get(rel.source_id)
        tgt_i = entity_idx.get(rel.target_id)
        if src_i is None or tgt_i is None:
            continue
        W[tgt_i, src_i] = rel.weight
    return W


# ---------------------------------------------------------------------------
# Private — per-hop propagation modes
# ---------------------------------------------------------------------------


def _matrix_linear_hop(
    carry: npt.NDArray[np.float64],
    W: npt.NDArray[np.float64],
    attenuation_factor: float,
) -> npt.NDArray[np.float64]:
    """Apply one LINEAR propagation hop.

    carry_next = attenuation_factor × W @ carry

    Equivalent to iterative _attenuate() applied to every (entity, attribute)
    pair simultaneously. Mathematically exact — no semantic difference from
    the iterative engine on any graph topology.

    Args:
        carry: (N, n_attrs) current delta matrix.
        W: (N, N) weight matrix.
        attenuation_factor: Per-hop decay in [0.0, 1.0].

    Returns:
        (N, n_attrs) delta matrix after one LINEAR hop.
    """
    result: npt.NDArray[np.float64] = attenuation_factor * (W @ carry)
    return result


def _matrix_threshold_hop(
    carry: npt.NDArray[np.float64],
    W: npt.NDArray[np.float64],
    attenuation_factor: float,
    threshold: float,
) -> npt.NDArray[np.float64]:
    """Apply one THRESHOLD propagation hop.

    Applies LINEAR attenuation then zeroes out rows (entities) where the
    maximum |delta| across all attributes is below the threshold. Only
    above-threshold rows are returned for accumulation and further propagation.

    Semantic note: threshold is checked on the summed per-entity contribution
    (not per edge as in the iterative engine). Results may differ on converging
    graphs — see module docstring.

    Args:
        carry: (N, n_attrs) current delta matrix.
        W: (N, N) weight matrix.
        attenuation_factor: Per-hop decay in [0.0, 1.0].
        threshold: Minimum max |delta| across attributes to pass threshold gate.

    Returns:
        (N, n_attrs) delta matrix with below-threshold rows zeroed.
    """
    next_carry: npt.NDArray[np.float64] = attenuation_factor * (W @ carry)
    if threshold > 0.0:
        max_abs: npt.NDArray[np.float64] = np.max(np.abs(next_carry), axis=1)
        mask = max_abs >= threshold
        next_carry = next_carry * mask[:, np.newaxis]
    return next_carry


def _matrix_cascade_hop(
    carry: npt.NDArray[np.float64],
    W: npt.NDArray[np.float64],
    attenuation_factor: float,
    ceiling: float,
    base_values: npt.NDArray[np.float64],
) -> npt.NDArray[np.float64]:
    """Apply one CASCADE propagation hop.

    Amplifies by (1/attenuation_factor) × W, then ceiling-clips each
    entity's per-attribute delta at ceiling × |base_values[attr]|.

    Semantic note: ceiling is applied after summing converging paths.
    Single-path graphs match the iterative engine exactly — see module
    docstring for converging-path divergence.

    Args:
        carry: (N, n_attrs) current delta matrix.
        W: (N, N) weight matrix.
        attenuation_factor: Per-hop scale; inverted for CASCADE (must be > 0).
        ceiling: Maximum amplification factor relative to |base_values|.
        base_values: (n_attrs,) original source delta values for ceiling ref.

    Returns:
        (N, n_attrs) delta matrix after one CASCADE hop with ceiling applied.
    """
    scale = 1.0 / attenuation_factor
    next_carry: npt.NDArray[np.float64] = scale * (W @ carry)

    # Ceiling caps per attribute: caps[k] = ceiling * |base_values[k]|
    # Broadcast shape: (1, n_attrs) over (N, n_attrs)
    caps: npt.NDArray[np.float64] = np.abs(base_values) * ceiling
    nonzero_caps: npt.NDArray[np.bool_] = caps > 0.0
    if np.any(nonzero_caps):
        clipped: npt.NDArray[np.float64] = np.clip(
            next_carry, -caps[np.newaxis, :], caps[np.newaxis, :]
        )
        next_carry = np.where(nonzero_caps[np.newaxis, :], clipped, next_carry)
    return next_carry


# ---------------------------------------------------------------------------
# Private — float → Decimal accumulation
# ---------------------------------------------------------------------------


def _accumulate_matrix_carry(
    accumulator: _DeltaAccumulator,
    carry: npt.NDArray[np.float64],
    entity_ids: list[str],
    attr_keys: list[str],
    attr_quantities: list[Quantity],
) -> None:
    """Convert a carry matrix to Decimal Quantities and accumulate.

    For each entity row with any non-zero delta, converts float64 values to
    Decimal via Decimal(str(v)) per ADR-009 §Decision 5, then calls
    _accumulate with the resulting Quantity dict. Exactly-zero rows are
    skipped without allocating Quantity objects.

    Args:
        accumulator: Mutable delta accumulator (entity_id → attr → Quantity).
        carry: (N, n_attrs) float64 propagated delta matrix.
        entity_ids: entity_id at each row index.
        attr_keys: Attribute key at each column index.
        attr_quantities: Reference Quantity for unit/type/tier metadata.
    """
    for j, eid in enumerate(entity_ids):
        row = carry[j, :]
        if not np.any(row != 0.0):
            continue
        deltas: dict[str, Quantity] = {}
        for a_idx, (k, q) in enumerate(zip(attr_keys, attr_quantities, strict=False)):
            v = float(row[a_idx])
            if v == 0.0:
                continue
            deltas[k] = Quantity(
                value=Decimal(str(v)),
                unit=q.unit,
                variable_type=q.variable_type,
                measurement_framework=q.measurement_framework,
                observation_date=q.observation_date,
                source_id=q.source_id,
                confidence_tier=q.confidence_tier,
            )
        if deltas:
            _accumulate(accumulator, eid, deltas)
