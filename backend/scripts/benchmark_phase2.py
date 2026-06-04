"""
Phase 2 A/B benchmark — ADR-009 Simulation Engine Computation Model.

Runs the iterative engine (propagation.py) and matrix engine
(matrix_propagation.py) side-by-side across all Phase 1 load levels
and reports wall time, peak memory, and per-step throughput for both.
Outputs a Markdown table to stdout and optionally to a report file.

Authority: ADR-009 §Decision 1 (parallel run), §Decision 3 (performance
target), §Decision 4 (Phase 2 A/B report is a required M11 deliverable).

Usage (from backend/ directory):
    python scripts/benchmark_phase2.py
    python scripts/benchmark_phase2.py --output docs/architecture/performance/phase2-ab-report.md

Load levels match Phase 1 (benchmark_phase1.py) exactly for direct comparison:
  1x:    1 entity,   6 steps,    0 relationships  (Greece 2010-2012 production)
  10x:   10 entities, 10 steps,  50 relationships
  100x:  100 entities, 20 steps, 500 relationships
  1000x: 500 entities, 30 steps, 1000 relationships  (CI equity cap)
  spike: 50 entities,  10 steps, 200 relationships, all-entity shock
  adr009: 1 entity,  15 steps,  0 relationships, 1000 MC runs (§Decision 3 gate)
"""
from __future__ import annotations

import argparse
import sys
import time
import tracemalloc
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

# Allow running from scripts/ or backend/ directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.simulation.engine.matrix_propagation import propagate_matrix  # noqa: E402
from app.simulation.engine.models import (  # noqa: E402
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
from app.simulation.engine.propagation import propagate  # noqa: E402
from app.simulation.engine.quantity import Quantity, VariableType  # noqa: E402

_EPOCH = datetime(2010, 1, 1, tzinfo=UTC)
_SCENARIO_END = datetime(2016, 1, 1, tzinfo=UTC)
_RESOLUTION = ResolutionConfig(global_level=ResolutionLevel.NATION_STATE)
_SCENARIO_CONFIG = ScenarioConfig(
    scenario_id="benchmark-phase2",
    name="Phase 2 A/B Benchmark",
    description="ADR-009 Phase 2 comparative benchmark — iterative vs matrix",
    start_date=_EPOCH,
    end_date=_SCENARIO_END,
)


# ---------------------------------------------------------------------------
# Scenario factories (match benchmark_phase1.py exactly)
# ---------------------------------------------------------------------------


def _make_entity(entity_id: str) -> SimulationEntity:
    return SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes={
            "gdp_growth_rate": Quantity(
                value=Decimal("-5.7"),
                unit="percent",
                variable_type=VariableType.RATIO,
                confidence_tier=1,
            ),
            "unemployment_rate": Quantity(
                value=Decimal("17.8"),
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


def _build_state(n_entities: int, n_relationships: int) -> SimulationState:
    entities = {f"E{i:04d}": _make_entity(f"E{i:04d}") for i in range(n_entities)}
    rels = []
    for i in range(n_relationships):
        src = f"E{i % n_entities:04d}"
        tgt = f"E{(i + 1) % n_entities:04d}"
        if src != tgt:
            rels.append(Relationship(
                source_id=src,
                target_id=tgt,
                relationship_type="trade",
                weight=0.4,
            ))
    return SimulationState(
        timestep=_EPOCH,
        resolution=_RESOLUTION,
        entities=entities,
        relationships=rels,
        events=[],
        scenario_config=_SCENARIO_CONFIG,
    )


def _make_shock(entity_id: str, magnitude: float = -3.0) -> Event:
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
        propagation_rules=[PropagationRule(
            relationship_type="trade",
            attenuation_factor=0.4,
            max_hops=2,
        )],
        timestep_originated=_EPOCH,
        framework=MeasurementFramework.FINANCIAL,
    )


# ---------------------------------------------------------------------------
# Timing harness
# ---------------------------------------------------------------------------


@dataclass
class BenchResult:
    label: str
    engine: str
    n_entities: int
    n_steps: int
    n_relationships: int
    wall_ms: float
    peak_mib: float
    steps_per_second: float


def _run_bench(
    label: str,
    engine: str,
    n_entities: int,
    n_steps: int,
    n_relationships: int,
    n_shock_sources: int = 5,
) -> BenchResult:
    fn = propagate if engine == "iterative" else propagate_matrix
    state = _build_state(n_entities, n_relationships)
    events = [_make_shock(f"E{i:04d}") for i in range(min(n_entities, n_shock_sources))]

    tracemalloc.start()
    t0 = time.perf_counter()
    for _ in range(n_steps):
        state = fn(state, events)
    wall_s = time.perf_counter() - t0
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return BenchResult(
        label=label,
        engine=engine,
        n_entities=n_entities,
        n_steps=n_steps,
        n_relationships=n_relationships,
        wall_ms=wall_s * 1000,
        peak_mib=peak_bytes / (1024 * 1024),
        steps_per_second=n_steps / wall_s if wall_s > 0 else float("inf"),
    )


def _run_mc_bench(label: str, engine: str, n_runs: int, n_steps: int) -> BenchResult:
    """Run N MC runs of n_steps each; report aggregate wall time."""
    fn = propagate if engine == "iterative" else propagate_matrix
    state_template = _build_state(n_entities=1, n_relationships=0)
    events = [_make_shock("E0000", magnitude=-3.0)]

    t0 = time.perf_counter()
    for _ in range(n_runs):
        state = state_template
        for _ in range(n_steps):
            state = fn(state, events)
    wall_s = time.perf_counter() - t0

    return BenchResult(
        label=label,
        engine=engine,
        n_entities=1,
        n_steps=n_runs * n_steps,
        n_relationships=0,
        wall_ms=wall_s * 1000,
        peak_mib=0.0,
        steps_per_second=(n_runs * n_steps) / wall_s if wall_s > 0 else float("inf"),
    )


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------


def _speedup_label(it_ms: float, mx_ms: float) -> str:
    if it_ms == 0 or mx_ms == 0:
        return "N/A"
    ratio = it_ms / mx_ms
    if ratio >= 1.0:
        return f"{ratio:.2f}× faster"
    return f"{1/ratio:.2f}× slower"


def _generate_report(results: list[tuple[BenchResult, BenchResult]]) -> str:
    lines: list[str] = [
        "# Phase 2 A/B Benchmark Report — ADR-009",
        "",
        f"Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Summary",
        "",
        "Iterative engine (propagation.py) vs matrix engine (matrix_propagation.py).",
        "Load levels match Phase 1 baseline (benchmark_phase1.py) for direct comparison.",
        "ADR-009 §Decision 3 gate: 1000 MC runs ≤ 60s on CI runner (2-core, 7 GiB RAM).",
        "",
        "## Results",
        "",
        "| Load level | Entities | Steps | Rels | Iterative (ms) | Matrix (ms) | "
        "Matrix speedup | Iterative peak MiB | Matrix peak MiB |",
        "|---|---|---|---|---|---|---|---|---|",
    ]

    for it, mx in results:
        speedup = _speedup_label(it.wall_ms, mx.wall_ms)
        lines.append(
            f"| {it.label} | {it.n_entities} | {it.n_steps} | {it.n_relationships} | "
            f"{it.wall_ms:.1f} | {mx.wall_ms:.1f} | {speedup} | "
            f"{it.peak_mib:.2f} | {mx.peak_mib:.2f} |"
        )

    lines += [
        "",
        "## ADR-009 §Decision 3 Gate",
        "",
        "1000 MC runs × 15 steps on Greece-equivalent (1 entity, 0 relationships).",
        "Gate: ≤ 60s on CI runner. Result captured in `adr009_gate` row above.",
        "",
        "## Notes",
        "",
        "- Matrix engine uses NumPy dense matrix operations (numpy==2.1.3).",
        "- Decimal↔float64 boundary: delta values cross float64 for matrix operations;",
        "  return via Decimal(str(float_value)) per ADR-009 §Decision 5.",
        "- Equivalence gate (ADR-009 §Decision 2): |matrix - iterative| ≤ 1e-10",
        "  on every Quantity.value; verified in test_equivalence_harness.py.",
        "- Semantic differences for THRESHOLD (per-edge vs per-entity) and CASCADE",
        "  (pre-accumulation vs post-accumulation ceiling) on converging graphs are",
        "  documented in matrix_propagation.py module docstring.",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 2 A/B benchmark — ADR-009")
    parser.add_argument(
        "--output",
        metavar="PATH",
        help="Write Markdown report to this path (stdout only if omitted)",
    )
    args = parser.parse_args()

    load_levels = [
        ("1x (Greece-equiv)", 1, 6, 0, 1),
        ("10x", 10, 10, 50, 5),
        ("100x", 100, 20, 500, 5),
        ("1000x (capped)", 500, 30, 1000, 5),
    ]

    results: list[tuple[BenchResult, BenchResult]] = []

    for label, n_ent, n_steps, n_rels, n_shock in load_levels:
        print(f"Running {label} ({n_ent} entities × {n_steps} steps × {n_rels} rels) …")
        it = _run_bench(label, "iterative", n_ent, n_steps, n_rels, n_shock)
        mx = _run_bench(label, "matrix", n_ent, n_steps, n_rels, n_shock)
        results.append((it, mx))
        print(f"  iterative: {it.wall_ms:.1f} ms | matrix: {mx.wall_ms:.1f} ms")

    # ADR-009 §Decision 3 gate
    print("Running ADR-009 §Decision 3 gate (1000 MC runs × 15 steps) …")
    it_mc = _run_mc_bench("adr009_gate (1000×15 MC)", "iterative", 1000, 15)
    mx_mc = _run_mc_bench("adr009_gate (1000×15 MC)", "matrix", 1000, 15)
    results.append((it_mc, mx_mc))

    it_gate_s = it_mc.wall_ms / 1000
    mx_gate_s = mx_mc.wall_ms / 1000
    print(f"  iterative: {it_gate_s:.2f}s | matrix: {mx_gate_s:.2f}s")

    gate_status = "PASS" if mx_gate_s < 60.0 else "FAIL"
    print(f"  ADR-009 §Decision 3 gate: {gate_status} (matrix ≤ 60s)")

    report = _generate_report(results)
    print("\n" + report)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report)
        print(f"\nReport written to {out_path}")


if __name__ == "__main__":
    main()
