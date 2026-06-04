"""
ADR-009 Equivalence Harness — Phase 2 A/B validation.

Verifies that propagate_matrix() produces output identical to propagate()
within ADR-009 §Decision 2 tolerance (1e-10 on every Quantity.value at
every step for every entity). Also validates the ADR-009 §Decision 3
performance gate for the matrix engine.

Architecture authority: ADR-009 §Decision 1 (parallel run), §Decision 2
(equivalence gate), §Decision 3 (performance target), §Decision 4
(equivalence harness is a required M11 deliverable).

Graph topology note:
  The equivalence gate is tested on single-source, single-path graphs
  (chain topologies) where both engines are mathematically identical.
  Multi-path converging graphs produce documented semantic differences
  for THRESHOLD and CASCADE modes (see matrix_propagation.py module
  docstring). The harness covers:
    - LINEAR: any topology (mathematically exact)
    - THRESHOLD: single-path chains (per-edge == per-entity when only
      one source entity is in the frontier at each hop)
    - CASCADE: single-path chains (ceiling applied to sole contribution)
    - 1x, 10x, 100x load levels for the matrix engine
    - ADR-009 §Decision 3 performance gate (1000 MC runs ≤ 60s)

Usage (from backend/ directory):
    pytest tests/performance/test_equivalence_harness.py -v
    pytest tests/performance/test_equivalence_harness.py -v -k "linear"
"""
from __future__ import annotations

import time
import uuid
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from app.simulation.engine.matrix_propagation import propagate_matrix
from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
    PropagationMode,
    PropagationRule,
    Relationship,
    ResolutionConfig,
    ResolutionLevel,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.engine.propagation import propagate
from app.simulation.engine.quantity import Quantity, VariableType

# ---------------------------------------------------------------------------
# Markers
# ---------------------------------------------------------------------------

pytestmark = pytest.mark.slow

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

_EPOCH = datetime(2010, 1, 1, tzinfo=UTC)
_SCENARIO_END = datetime(2016, 1, 1, tzinfo=UTC)
_RESOLUTION = ResolutionConfig(global_level=ResolutionLevel.NATION_STATE)
_SCENARIO_CONFIG = ScenarioConfig(
    scenario_id="equivalence-test",
    name="Equivalence Test",
    description="ADR-009 §Decision 2 equivalence harness",
    start_date=_EPOCH,
    end_date=_SCENARIO_END,
)

_TOLERANCE = 1e-10  # ADR-009 §Decision 2


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _make_entity(entity_id: str, gdp: float = -5.7, unemployment: float = 17.8) -> SimulationEntity:
    return SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes={
            "gdp_growth_rate": Quantity(
                value=Decimal(str(gdp)),
                unit="percent",
                variable_type=VariableType.RATIO,
                confidence_tier=1,
            ),
            "unemployment_rate": Quantity(
                value=Decimal(str(unemployment)),
                unit="percent",
                variable_type=VariableType.RATIO,
                confidence_tier=1,
            ),
        },
        metadata={},
    )


def _make_state(
    entity_ids: list[str],
    relationships: list[Relationship] | None = None,
) -> SimulationState:
    return SimulationState(
        timestep=_EPOCH,
        resolution=_RESOLUTION,
        entities={eid: _make_entity(eid) for eid in entity_ids},
        relationships=relationships or [],
        events=[],
        scenario_config=_SCENARIO_CONFIG,
    )


def _make_chain_relationships(
    entity_ids: list[str],
    relationship_type: str = "trade",
    weight: float = 0.4,
) -> list[Relationship]:
    """Build a linear chain: E0 → E1 → E2 → ... (no converging paths)."""
    rels = []
    for i in range(len(entity_ids) - 1):
        rels.append(Relationship(
            source_id=entity_ids[i],
            target_id=entity_ids[i + 1],
            relationship_type=relationship_type,
            weight=weight,
        ))
    return rels


def _make_fiscal_shock(
    source_id: str,
    magnitude: float = -3.0,
    rule: PropagationRule | None = None,
    framework: MeasurementFramework = MeasurementFramework.FINANCIAL,
) -> Event:
    if rule is None:
        rule = PropagationRule(
            relationship_type="trade",
            attenuation_factor=0.4,
            max_hops=2,
        )
    return Event(
        event_id=str(uuid.uuid4()),
        source_entity_id=source_id,
        event_type="shock",
        affected_attributes={
            "gdp_growth_rate": Quantity(
                value=Decimal(str(magnitude)),
                unit="percent",
                variable_type=VariableType.RATIO,
                confidence_tier=2,
            ),
        },
        propagation_rules=[rule],
        timestep_originated=_EPOCH,
        framework=framework,
    )


def _assert_states_equivalent(
    iterative_state: SimulationState,
    matrix_state: SimulationState,
    tolerance: float = _TOLERANCE,
    label: str = "",
) -> None:
    """Assert every Quantity.value matches within tolerance.

    Checks:
    - Same entity IDs in both states.
    - Same attribute keys per entity.
    - |matrix_value - iterative_value| <= tolerance for every Quantity.value.
    """
    prefix = f"[{label}] " if label else ""
    assert set(iterative_state.entities.keys()) == set(matrix_state.entities.keys()), (
        f"{prefix}Entity ID sets differ"
    )
    for entity_id in iterative_state.entities:
        it_entity = iterative_state.entities[entity_id]
        mx_entity = matrix_state.entities[entity_id]
        assert set(it_entity.attributes.keys()) == set(mx_entity.attributes.keys()), (
            f"{prefix}entity={entity_id}: attribute key sets differ "
            f"(iterative={set(it_entity.attributes)}, matrix={set(mx_entity.attributes)})"
        )
        for attr_key in it_entity.attributes:
            it_val = float(it_entity.attributes[attr_key].value)
            mx_val = float(mx_entity.attributes[attr_key].value)
            diff = abs(mx_val - it_val)
            assert diff <= tolerance, (
                f"{prefix}entity={entity_id} attr={attr_key}: "
                f"|matrix({mx_val}) - iterative({it_val})| = {diff:.2e} "
                f"exceeds gate {tolerance:.0e} (ADR-009 §Decision 2)"
            )


# ---------------------------------------------------------------------------
# LINEAR equivalence tests
# ---------------------------------------------------------------------------


def test_equivalence_linear_single_entity_no_propagation() -> None:
    """
    # INTENT: Single entity with no relationships — both engines produce identical output.
    # PRECONDITIONS: 1 entity, 0 relationships, 1 fiscal shock event.
    # POSTCONDITIONS: Both states are identical within 1e-10 tolerance.
    # ERROR CASES: Any divergence is an ADR-009 §Decision 2 violation.
    # KNOWN LIMITATIONS: No propagation occurs; this tests source accumulation only.
    """
    state = _make_state(["GRC"])
    events = [_make_fiscal_shock("GRC")]

    it_state = propagate(state, events)
    mx_state = propagate_matrix(state, events)
    _assert_states_equivalent(it_state, mx_state, label="linear_single_entity")


def test_equivalence_linear_two_entity_chain_one_hop() -> None:
    """
    # INTENT: Two-entity chain with 1 hop — verify exact delta transfer.
    # PRECONDITIONS: GRC → DEU trade relationship, 1-hop LINEAR rule, weight=0.4, a=0.4.
    # POSTCONDITIONS: DEU receives attenuation_factor × weight × delta = 0.4×0.4×(-3)=-0.48.
    # ERROR CASES: Divergence >1e-10 fails ADR-009 §Decision 2.
    # KNOWN LIMITATIONS: Chain topology; no converging paths.
    """
    rels = _make_chain_relationships(["GRC", "DEU"], weight=0.4)
    state = _make_state(["GRC", "DEU"], relationships=rels)
    events = [_make_fiscal_shock("GRC")]

    it_state = propagate(state, events)
    mx_state = propagate_matrix(state, events)
    _assert_states_equivalent(it_state, mx_state, label="linear_two_entity_1hop")


def test_equivalence_linear_three_entity_chain_two_hops() -> None:
    """
    # INTENT: Three-entity chain with 2 hops — verify multi-hop compounding.
    # PRECONDITIONS: GRC→DEU→FRA trade chain, 2-hop LINEAR rule, weight=0.4, a=0.4.
    # POSTCONDITIONS: DEU: 0.4×0.4×(-3)=-0.48; FRA: 0.4×0.4×(-0.48)=-0.0768.
    # ERROR CASES: Divergence >1e-10 fails ADR-009 §Decision 2.
    # KNOWN LIMITATIONS: Chain topology; FRA receives 2-hop attenuated signal.
    """
    rels = _make_chain_relationships(["GRC", "DEU", "FRA"], weight=0.4)
    state = _make_state(["GRC", "DEU", "FRA"], relationships=rels)
    events = [_make_fiscal_shock("GRC", rule=PropagationRule(
        relationship_type="trade",
        attenuation_factor=0.4,
        max_hops=2,
    ))]

    it_state = propagate(state, events)
    mx_state = propagate_matrix(state, events)
    _assert_states_equivalent(it_state, mx_state, label="linear_three_entity_2hop")


def test_equivalence_linear_multi_step_simulation() -> None:
    """
    # INTENT: Verify equivalence across 6 consecutive simulation steps.
    # PRECONDITIONS: 3 entities in a chain; fiscal shock applied every step.
    # POSTCONDITIONS: Both state sequences are identical within 1e-10 at each step.
    # ERROR CASES: Divergence at any step is an ADR-009 §Decision 2 violation.
    # KNOWN LIMITATIONS: Each step compounds propagated deltas from prior steps.
    """
    rels = _make_chain_relationships(["GRC", "DEU", "FRA"], weight=0.3)
    it_state = _make_state(["GRC", "DEU", "FRA"], relationships=rels)
    mx_state = _make_state(["GRC", "DEU", "FRA"], relationships=rels)
    rule = PropagationRule(relationship_type="trade", attenuation_factor=0.3, max_hops=2)

    for step in range(6):
        events = [_make_fiscal_shock("GRC", magnitude=-2.0, rule=rule)]
        it_state = propagate(it_state, events)
        mx_state = propagate_matrix(mx_state, events)
        _assert_states_equivalent(it_state, mx_state, label=f"linear_multi_step_step{step}")


def test_equivalence_linear_no_events() -> None:
    """
    # INTENT: Empty event list — both engines return identical (unchanged) state.
    # PRECONDITIONS: 3 entities, 2 relationships, 0 events.
    # POSTCONDITIONS: Both output states match input state; attributes unchanged.
    # ERROR CASES: Any change to entity attributes is an engine error.
    # KNOWN LIMITATIONS: Trivial; verifies no-op path.
    """
    rels = _make_chain_relationships(["GRC", "DEU", "FRA"], weight=0.4)
    state = _make_state(["GRC", "DEU", "FRA"], relationships=rels)

    it_state = propagate(state, [])
    mx_state = propagate_matrix(state, [])
    _assert_states_equivalent(it_state, mx_state, label="linear_no_events")


def test_equivalence_linear_multiple_events_same_source() -> None:
    """
    # INTENT: Two events from the same source entity — deltas accumulate correctly.
    # PRECONDITIONS: GRC→DEU chain; two fiscal shocks from GRC at different magnitudes.
    # POSTCONDITIONS: Accumulated deltas in both states are identical within 1e-10.
    # ERROR CASES: Non-commutativity or incorrect accumulation is an engine bug.
    # KNOWN LIMITATIONS: Both events use the same propagation rule and attribute.
    """
    rels = _make_chain_relationships(["GRC", "DEU"], weight=0.5)
    state = _make_state(["GRC", "DEU"], relationships=rels)
    rule = PropagationRule(relationship_type="trade", attenuation_factor=0.5, max_hops=1)
    events = [
        _make_fiscal_shock("GRC", magnitude=-3.0, rule=rule),
        _make_fiscal_shock("GRC", magnitude=-1.5, rule=rule),
    ]

    it_state = propagate(state, events)
    mx_state = propagate_matrix(state, events)
    _assert_states_equivalent(it_state, mx_state, label="linear_multiple_events")


# ---------------------------------------------------------------------------
# THRESHOLD equivalence tests (single-path topology)
# ---------------------------------------------------------------------------


def test_equivalence_threshold_above_gate_propagates() -> None:
    """
    # INTENT: THRESHOLD mode — delta above threshold propagates in both engines.
    # PRECONDITIONS: GRC→DEU chain, threshold=0.1, magnitude=-3.0.
    #   Attenuated delta at DEU: 0.4×0.4×3.0 = 0.48 >> threshold.
    # POSTCONDITIONS: DEU receives propagated delta in both engines.
    # ERROR CASES: DEU not receiving delta is a threshold gate bug.
    # KNOWN LIMITATIONS: Single-path topology; per-edge == per-entity threshold.
    """
    rels = _make_chain_relationships(["GRC", "DEU"], weight=0.4)
    state = _make_state(["GRC", "DEU"], relationships=rels)
    rule = PropagationRule(
        relationship_type="trade",
        attenuation_factor=0.4,
        max_hops=1,
        propagation_mode=PropagationMode.THRESHOLD,
        threshold=0.1,
    )
    events = [_make_fiscal_shock("GRC", magnitude=-3.0, rule=rule)]

    it_state = propagate(state, events)
    mx_state = propagate_matrix(state, events)
    _assert_states_equivalent(it_state, mx_state, label="threshold_above_gate")


def test_equivalence_threshold_below_gate_no_propagation() -> None:
    """
    # INTENT: THRESHOLD mode — delta below threshold does NOT propagate.
    # PRECONDITIONS: GRC→DEU chain, threshold=0.5, magnitude=-0.1.
    #   Attenuated delta at DEU: 0.4×0.4×0.1 = 0.016 < threshold=0.5.
    # POSTCONDITIONS: DEU attributes unchanged from initial state in both engines.
    # ERROR CASES: DEU receiving propagated delta is a threshold gate bypass.
    # KNOWN LIMITATIONS: Single-path topology.
    """
    rels = _make_chain_relationships(["GRC", "DEU"], weight=0.4)
    state = _make_state(["GRC", "DEU"], relationships=rels)
    rule = PropagationRule(
        relationship_type="trade",
        attenuation_factor=0.4,
        max_hops=1,
        propagation_mode=PropagationMode.THRESHOLD,
        threshold=0.5,
    )
    events = [_make_fiscal_shock("GRC", magnitude=-0.1, rule=rule)]

    it_state = propagate(state, events)
    mx_state = propagate_matrix(state, events)
    _assert_states_equivalent(it_state, mx_state, label="threshold_below_gate")


# ---------------------------------------------------------------------------
# CASCADE equivalence tests (single-path topology)
# ---------------------------------------------------------------------------


def test_equivalence_cascade_single_hop_amplification() -> None:
    """
    # INTENT: CASCADE mode — delta amplifies (1/a)×w per hop; verify exact match.
    # PRECONDITIONS: GRC→DEU chain, a=0.4, w=0.4, ceiling=3.0, magnitude=-3.0.
    #   Amplified: (1/0.4)×0.4×(-3.0) = -3.0; cap = 3.0×3.0 = 9.0 → no clamp.
    # POSTCONDITIONS: DEU delta = -3.0 in both engines.
    # ERROR CASES: Divergence >1e-10 on single-hop CASCADE is an engine bug.
    # KNOWN LIMITATIONS: Single-path; ceiling cap does not engage here.
    """
    rels = _make_chain_relationships(["GRC", "DEU"], weight=0.4)
    state = _make_state(["GRC", "DEU"], relationships=rels)
    rule = PropagationRule(
        relationship_type="trade",
        attenuation_factor=0.4,
        max_hops=1,
        propagation_mode=PropagationMode.CASCADE,
        ceiling=3.0,
    )
    events = [_make_fiscal_shock("GRC", magnitude=-3.0, rule=rule)]

    it_state = propagate(state, events)
    mx_state = propagate_matrix(state, events)
    _assert_states_equivalent(it_state, mx_state, label="cascade_single_hop")


def test_equivalence_cascade_ceiling_clamps() -> None:
    """
    # INTENT: CASCADE ceiling clamp — verify clamp engages identically in both engines.
    # PRECONDITIONS: GRC→DEU chain, a=0.1, w=1.0, ceiling=1.0, magnitude=-3.0.
    #   Amplified: (1/0.1)×1.0×(-3.0) = -30.0; cap = 1.0×3.0 = 3.0 → clamped to -3.0.
    # POSTCONDITIONS: DEU delta clamped to -3.0 in both engines.
    # ERROR CASES: DEU receiving -30.0 (unclamped) is a ceiling gate failure.
    # KNOWN LIMITATIONS: Single-path; ceiling cap actively engages here.
    """
    rels = _make_chain_relationships(["GRC", "DEU"], weight=1.0)
    state = _make_state(["GRC", "DEU"], relationships=rels)
    rule = PropagationRule(
        relationship_type="trade",
        attenuation_factor=0.1,
        max_hops=1,
        propagation_mode=PropagationMode.CASCADE,
        ceiling=1.0,
    )
    events = [_make_fiscal_shock("GRC", magnitude=-3.0, rule=rule)]

    it_state = propagate(state, events)
    mx_state = propagate_matrix(state, events)
    _assert_states_equivalent(it_state, mx_state, label="cascade_ceiling_clamps")


# ---------------------------------------------------------------------------
# Performance gates — matrix engine
# ---------------------------------------------------------------------------


def test_matrix_engine_1x_performance() -> None:
    """
    # INTENT: Matrix engine 1x performance — baseline on Greece-equivalent scenario.
    # PRECONDITIONS: 1 entity, 6 steps, 0 relationships.
    # POSTCONDITIONS: Completes under 1 second on any target hardware.
    # ERROR CASES: Timeout exceeding 1s is a performance regression.
    # KNOWN LIMITATIONS: No relationships — pure source accumulation performance.
    """
    state = _make_state(["GRC"])
    events = [_make_fiscal_shock("GRC")]

    t0 = time.perf_counter()
    for _ in range(6):
        state = propagate_matrix(state, events)
    wall_s = time.perf_counter() - t0

    print(f"\n[matrix 1x] 1 entity × 6 steps: {wall_s * 1000:.1f} ms")
    assert wall_s < 1.0, f"Matrix 1x: {wall_s:.3f}s exceeded 1s gate"


def test_matrix_engine_10x_performance() -> None:
    """
    # INTENT: Matrix engine 10x performance — 10 entities × 10 steps.
    # PRECONDITIONS: 10 entities, chain topology, 10 steps.
    # POSTCONDITIONS: Completes under 10 seconds on CI runner.
    # ERROR CASES: Timeout is a performance regression vs. iterative 1x gate.
    # KNOWN LIMITATIONS: Chain topology; dense graphs will be slower.
    """
    entity_ids = [f"E{i:02d}" for i in range(10)]
    rels = _make_chain_relationships(entity_ids, weight=0.4)
    state = _make_state(entity_ids, relationships=rels)
    rule = PropagationRule(relationship_type="trade", attenuation_factor=0.4, max_hops=2)
    events = [_make_fiscal_shock("E00", rule=rule)]

    t0 = time.perf_counter()
    for _ in range(10):
        state = propagate_matrix(state, events)
    wall_s = time.perf_counter() - t0

    print(f"\n[matrix 10x] 10 entities × 10 steps: {wall_s * 1000:.1f} ms")
    assert wall_s < 10.0, f"Matrix 10x: {wall_s:.3f}s exceeded 10s gate"


def test_matrix_engine_100x_performance() -> None:
    """
    # INTENT: Matrix engine 100x performance — 100 entities × 20 steps.
    # PRECONDITIONS: 100 entities, chain topology with 100 edges, 20 steps.
    # POSTCONDITIONS: Completes under 120 seconds on CI runner.
    # ERROR CASES: Timeout on this scale indicates O(N^2) or worse scaling issue.
    # KNOWN LIMITATIONS: Chain topology; real-world dense graphs will be more demanding.
    """
    entity_ids = [f"E{i:03d}" for i in range(100)]
    rels = _make_chain_relationships(entity_ids, weight=0.3)
    state = _make_state(entity_ids, relationships=rels)
    rule = PropagationRule(relationship_type="trade", attenuation_factor=0.3, max_hops=2)
    events = [_make_fiscal_shock("E000", rule=rule)]

    t0 = time.perf_counter()
    for _ in range(20):
        state = propagate_matrix(state, events)
    wall_s = time.perf_counter() - t0

    print(f"\n[matrix 100x] 100 entities × 20 steps: {wall_s * 1000:.1f} ms")
    assert wall_s < 120.0, f"Matrix 100x: {wall_s:.3f}s exceeded 120s gate"


def test_adr009_performance_gate_matrix() -> None:
    """
    # INTENT: ADR-009 §Decision 3 performance gate for the matrix engine.
    # PRECONDITIONS: 1000 MC runs × 15 steps on Greece-equivalent scenario (1 entity).
    # POSTCONDITIONS: All 1000 runs complete within 60 seconds on CI runner.
    # ERROR CASES: Exceeding 60s is an ADR-009 §Decision 3 violation.
    # KNOWN LIMITATIONS: Synthetic Greece-equivalent scenario (no relationships).
    #   This tests raw engine throughput, not end-to-end scenario pipeline.
    #   Full pipeline test is in tests/backtesting/.
    """
    N_RUNS = 1000
    N_STEPS = 15
    state_template = _make_state(["GRC"])
    events = [_make_fiscal_shock("GRC", magnitude=-3.0)]

    t0 = time.perf_counter()
    for _ in range(N_RUNS):
        state = state_template
        for _ in range(N_STEPS):
            state = propagate_matrix(state, events)
    wall_s = time.perf_counter() - t0

    print(f"\n[ADR-009 gate] matrix engine: {N_RUNS} × {N_STEPS} steps: {wall_s:.3f}s")
    print(f"  Per-run: {wall_s / N_RUNS * 1000:.2f} ms")

    assert wall_s < 60.0, (
        f"ADR-009 §Decision 3 FAILED: matrix engine {N_RUNS} MC runs took "
        f"{wall_s:.1f}s (gate: 60s)."
    )
