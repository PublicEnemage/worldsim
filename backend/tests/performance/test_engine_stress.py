"""
Simulation engine stress test suite — Issue #406, Phase 3.

Establishes the high-water mark for the iterative engine and provides the
scaffold for the Phase 2 A/B comparison once the matrix engine is implemented.

Architecture authority: ADR-009 §Decision 3 (performance target), §Decision 2
(equivalence gate tolerance). Phase 1 baseline benchmarks:
docs/architecture/performance/phase1-iterative-baseline.md

Load levels (per Issue #406):
  1x   — current production scenario: Greece 2010–2015, 1 entity, 6 steps
  10x  — 10 entities, 10 steps, all frameworks, full relationship graph
  100x — 100 entities, 20 steps, all frameworks, dense relationship graph
  1000x— 500 entities, 30 steps (capped at 5000 entity-steps for CI equity)

Usage (from backend/ directory):
    pytest tests/performance/test_engine_stress.py -v
    pytest tests/performance/test_engine_stress.py -v --tb=short -k "1x"

These tests are marked `slow` and excluded from the default test run. They are
intended to be run:
  (a) before any matrix engine integration (to record the iterative baseline)
  (b) after matrix engine integration (Phase 2 A/B comparison)

CI integration: stress tests run in a separate workflow job, not in the standard
unit/integration job. Results are committed to docs/architecture/performance/.

Equitable build: all load levels must complete on the GitHub Actions free-tier
runner (2-core, 7 GiB RAM, Ubuntu). The 1000x scenario is capped at 500 entities
× 30 steps = 15,000 entity-steps to avoid OOM on 7 GiB RAM. The cap is documented
in the high-water mark table below.
"""
from __future__ import annotations

import time
import tracemalloc
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
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
# Shared fixtures — deterministic timestamps, no I/O
# ---------------------------------------------------------------------------

_EPOCH = datetime(2010, 1, 1, tzinfo=UTC)
_SCENARIO_END = datetime(2016, 1, 1, tzinfo=UTC)
_RESOLUTION = ResolutionConfig(global_level=ResolutionLevel.NATION_STATE)
_SCENARIO_CONFIG = ScenarioConfig(
    scenario_id="stress-test",
    name="Stress Test",
    description="Iterative engine stress test — Issue #406",
    start_date=_EPOCH,
    end_date=_SCENARIO_END,
)


# ---------------------------------------------------------------------------
# Scenario factories
# ---------------------------------------------------------------------------


def _make_entity(entity_id: str, gdp: float = -5.7, unemployment: float = 17.8) -> SimulationEntity:
    """Greece-like entity attributes."""
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
            "primary_surplus_pct_gdp": Quantity(
                value=Decimal("-8.5"),
                unit="percent_gdp",
                variable_type=VariableType.RATIO,
                confidence_tier=1,
            ),
        },
        metadata={},
    )


def _make_propagation_rule() -> PropagationRule:
    return PropagationRule(
        relationship_type="trade",
        attenuation_factor=0.4,
        max_hops=2,
    )


def _make_fiscal_shock(entity_id: str, magnitude: float = -3.0) -> Event:
    """Fiscal contraction event."""
    return Event(
        event_id=str(uuid.uuid4()),
        source_entity_id=entity_id,
        event_type="shock",
        affected_attributes={
            "gdp_growth_rate": Quantity(
                value=Decimal(str(magnitude)),
                unit="percent",
                variable_type=VariableType.RATIO,
                confidence_tier=2,
            ),
        },
        propagation_rules=[_make_propagation_rule()],
        timestep_originated=_EPOCH,
        framework=MeasurementFramework.FINANCIAL,
    )


def _make_trade_relationship(source: str, target: str, weight: float = 0.4) -> Relationship:
    return Relationship(
        source_id=source,
        target_id=target,
        relationship_type="trade",
        weight=weight,
    )


def _build_state(
    n_entities: int,
    n_relationships: int,
) -> SimulationState:
    """Build a simulation state with n_entities and n_relationships."""
    entities = {f"E{i:04d}": _make_entity(f"E{i:04d}") for i in range(n_entities)}
    # Distribute relationships round-robin across entities
    relationships = []
    for i in range(n_relationships):
        src = f"E{i % n_entities:04d}"
        tgt = f"E{(i + 1) % n_entities:04d}"
        if src != tgt:
            relationships.append(_make_trade_relationship(src, tgt))
    return SimulationState(
        timestep=_EPOCH,
        resolution=_RESOLUTION,
        entities=entities,
        relationships=relationships,
        events=[],
        scenario_config=_SCENARIO_CONFIG,
    )


# ---------------------------------------------------------------------------
# Timing harness
# ---------------------------------------------------------------------------


@dataclass
class StressResult:
    load_level: str
    n_entities: int
    n_steps: int
    n_relationships: int
    wall_time_s: float
    peak_memory_mib: float
    steps_per_second: float


def _run_stress(
    load_level: str,
    n_entities: int,
    n_steps: int,
    n_relationships: int,
) -> StressResult:
    state = _build_state(n_entities, n_relationships)
    events = [_make_fiscal_shock(f"E{i:04d}") for i in range(min(n_entities, 5))]

    tracemalloc.start()
    t0 = time.perf_counter()
    for _ in range(n_steps):
        state = propagate(state, events)
    wall_time_s = time.perf_counter() - t0
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return StressResult(
        load_level=load_level,
        n_entities=n_entities,
        n_steps=n_steps,
        n_relationships=n_relationships,
        wall_time_s=wall_time_s,
        peak_memory_mib=peak_bytes / (1024 * 1024),
        steps_per_second=n_steps / wall_time_s if wall_time_s > 0 else float("inf"),
    )


def _print_result(r: StressResult) -> None:
    print(
        f"\n[{r.load_level}] {r.n_entities} entities × {r.n_steps} steps × "
        f"{r.n_relationships} relationships"
    )
    print(f"  Wall time:       {r.wall_time_s * 1000:.1f} ms")
    print(f"  Peak memory:     {r.peak_memory_mib:.3f} MiB")
    print(f"  Steps/second:    {r.steps_per_second:.0f}")


# ---------------------------------------------------------------------------
# Load level 1x — current production scenario
# ---------------------------------------------------------------------------


def test_stress_1x_iterative() -> None:
    """
    # INTENT: Stress test load level 1x — production scenario baseline.
    # PRECONDITIONS: Iterative engine is importable; Greece-like attributes are valid.
    # POSTCONDITIONS: Wall time is recorded; result is printed for Phase 2 comparison.
    # ERROR CASES: Any propagation error or OOM is a test failure.
    # KNOWN LIMITATIONS: 1x load is trivially small; this test documents the floor,
    #   not a meaningful bottleneck. Phase 2 will run the same test on the matrix engine.
    """
    result = _run_stress(
        load_level="1x",
        n_entities=1,
        n_steps=6,
        n_relationships=0,
    )
    _print_result(result)
    # 1x must complete in under 1 second on any target hardware
    assert result.wall_time_s < 1.0, f"1x wall time {result.wall_time_s:.3f}s exceeded 1s gate"


# ---------------------------------------------------------------------------
# Load level 10x
# ---------------------------------------------------------------------------


def test_stress_10x_iterative() -> None:
    """
    # INTENT: Stress test load level 10x — 10 entities, moderate graph.
    # PRECONDITIONS: 10 entities and 50 relationships are constructable.
    # POSTCONDITIONS: Wall time recorded; serves as Phase 2 A/B comparison point.
    # ERROR CASES: OOM or propagation error is a test failure.
    # KNOWN LIMITATIONS: Relationship graph is synthetic (round-robin), not
    #   calibrated to a real scenario topology.
    """
    result = _run_stress(
        load_level="10x",
        n_entities=10,
        n_steps=10,
        n_relationships=50,
    )
    _print_result(result)
    # 10x must complete in under 10 seconds on CI runner
    assert result.wall_time_s < 10.0, f"10x wall time {result.wall_time_s:.3f}s exceeded 10s gate"


# ---------------------------------------------------------------------------
# Load level 100x
# ---------------------------------------------------------------------------


def test_stress_100x_iterative() -> None:
    """
    # INTENT: Stress test load level 100x — 100 entities, dense graph.
    # PRECONDITIONS: 100 entities and 500 relationships are constructable in memory.
    # POSTCONDITIONS: High-water mark for entity count documented.
    # ERROR CASES: OOM (expected to remain well under 7 GiB); propagation errors.
    # KNOWN LIMITATIONS: Dense round-robin graph may not reflect real-world
    #   sparse topology. Edge density dominates propagation cost (Phase 1 finding).
    """
    result = _run_stress(
        load_level="100x",
        n_entities=100,
        n_steps=20,
        n_relationships=500,
    )
    _print_result(result)
    # 100x must complete in under 120 seconds on CI runner
    assert result.wall_time_s < 120.0, (
        f"100x wall time {result.wall_time_s:.3f}s exceeded 120s gate"
    )


# ---------------------------------------------------------------------------
# Load level 1000x (capped at 500 entities × 30 steps for CI equity)
# ---------------------------------------------------------------------------


def test_stress_1000x_iterative() -> None:
    """
    # INTENT: Stress test load level 1000x — maximum entity count on target hardware.
    # PRECONDITIONS: 500 entities and 1000 relationships are constructable.
    # POSTCONDITIONS: First degradation point and bottleneck component identified via
    #   wall time and memory.
    # ERROR CASES: OOM within 7 GiB RAM is the expected failure boundary. If this
    #   test OOMs on the CI runner, document the failure point and reduce n_entities.
    # KNOWN LIMITATIONS: Capped at 500 entities × 30 steps (= 15,000 entity-steps)
    #   to avoid OOM on 7 GiB CI runner. True 1000x (500+ entities × dense graph)
    #   is above the equitable hardware target; this test establishes the practical
    #   ceiling for the iterative engine on target hardware.
    """
    result = _run_stress(
        load_level="1000x (capped)",
        n_entities=500,
        n_steps=30,
        n_relationships=1000,
    )
    _print_result(result)
    # 1000x (capped) must complete without OOM; no hard time gate — document result
    # The wall time is the high-water mark for the iterative engine at scale.
    assert result.peak_memory_mib < 500.0, (
        f"1000x peak memory {result.peak_memory_mib:.1f} MiB exceeded 500 MiB gate"
    )


# ---------------------------------------------------------------------------
# Spike scenario — simultaneous exogenous shock propagation
# ---------------------------------------------------------------------------


def test_stress_spike_scenario_iterative() -> None:
    """
    # INTENT: Stress test spike scenario — simultaneous shocks on all entities.
    # PRECONDITIONS: 50 entities, dense graph (200 relationships).
    # POSTCONDITIONS: Identifies bottleneck under maximum propagation fan-out.
    # ERROR CASES: Propagation error under concurrent shock load.
    # KNOWN LIMITATIONS: Simultaneous shocks on all entities is an adversarial
    #   scenario unlikely in practice; serves as an upper bound on propagation cost.
    """
    n_entities = 50
    state = _build_state(n_entities=n_entities, n_relationships=200)
    # Shock all entities simultaneously
    events = [_make_fiscal_shock(f"E{i:04d}") for i in range(n_entities)]

    tracemalloc.start()
    t0 = time.perf_counter()
    for _ in range(10):
        state = propagate(state, events)
    wall_time_s = time.perf_counter() - t0
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_mib = peak_bytes / (1024 * 1024)
    print(f"\n[spike] {n_entities} entities × 10 steps × 200 relationships × all-entity shock")
    print(f"  Wall time:    {wall_time_s * 1000:.1f} ms")
    print(f"  Peak memory:  {peak_mib:.3f} MiB")
    # Spike must complete in under 30 seconds on CI runner
    assert wall_time_s < 30.0, f"Spike wall time {wall_time_s:.3f}s exceeded 30s gate"


# ---------------------------------------------------------------------------
# ADR-009 performance gate — 1,000 MC runs on Greece-equivalent scenario
# ---------------------------------------------------------------------------


def test_adr009_performance_gate_iterative() -> None:
    """
    # INTENT: Verify the ADR-009 §Decision 3 performance target for the iterative engine.
    # PRECONDITIONS: ScenarioRunner or equivalent MC harness is available.
    # POSTCONDITIONS: 1,000 MC runs on Greece-equivalent scenario complete within 60s.
    # ERROR CASES: Any propagation error is a test failure; timeout is an ADR violation.
    # KNOWN LIMITATIONS: Uses a synthetic Greece-equivalent scenario (1 entity, 15 steps)
    #   rather than the full database-backed Greece 2010-2012 backtesting fixture. The
    #   full fixture test is in tests/backtesting/. This test validates the raw engine
    #   throughput, not the end-to-end scenario pipeline.
    """
    N_RUNS = 1000
    N_STEPS = 15  # Greece 2010-2012 equivalent
    n_entities = 1

    state_template = _build_state(n_entities=n_entities, n_relationships=0)
    events = [_make_fiscal_shock("E0000", magnitude=-3.0)]

    t0 = time.perf_counter()
    for _ in range(N_RUNS):
        state = state_template
        for _ in range(N_STEPS):
            state = propagate(state, events)
    wall_time_s = time.perf_counter() - t0

    print(f"\n[ADR-009 gate] {N_RUNS} × {N_STEPS} steps: {wall_time_s:.3f}s")
    print(f"  Per-run: {wall_time_s / N_RUNS * 1000:.2f} ms")

    # ADR-009 §Decision 3: must complete within 60 seconds on CI runner
    assert wall_time_s < 60.0, (
        f"ADR-009 performance gate FAILED: {N_RUNS} MC runs took {wall_time_s:.1f}s "
        f"(gate: 60s). Matrix engine must match or beat this baseline."
    )
