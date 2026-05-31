"""Phase 1 baseline benchmarks — iterative engine on target hardware.

Issue #514. Chief Engineer Agent.

Measures per-step computation cost, propagation scaling, Monte Carlo ensemble
throughput, and peak memory usage of the current iterative engine. Run on both
target machines before authoring ADR-009. Results feed directly into the
engine-baseline-benchmarks-m10.md document.

No database, no network, no external services required. All scenarios are
constructed in memory using the same helpers as the unit test suite.

Usage:
    cd backend
    python scripts/benchmark_phase1.py [--out PATH]

Options:
    --out PATH   Write JSON summary to PATH (default: prints to stdout only)

Exit codes:
    0 — All benchmarks complete, results printed
    1 — Fatal error during benchmark setup or execution
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import platform
import statistics
import sys
import time
import tracemalloc
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
    PropagationRule,
    Relationship,
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationModule,
    SimulationState,
)
from app.simulation.engine.propagation import propagate
from app.simulation.engine.quantity import Quantity, VariableType
from app.simulation.orchestration.runner import ScenarioRunner

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_WARMUP_RUNS = 3      # discarded to allow JIT / cache warmup
_TIMING_RUNS = 10     # measured runs per single-step benchmark
_MC_STEPS = 10        # steps per Monte Carlo scenario run
_BASE_DATE = datetime(2010, 1, 1)

# ---------------------------------------------------------------------------
# Scenario construction helpers
# ---------------------------------------------------------------------------

def _qty(
    value: float,
    variable_type: VariableType = VariableType.RATIO,
    unit: str = "dimensionless",
    framework: MeasurementFramework = MeasurementFramework.FINANCIAL,
) -> Quantity:
    return Quantity(
        value=Decimal(str(value)),
        unit=unit,
        variable_type=variable_type,
        measurement_framework=framework,
    )


def _entity(entity_id: str) -> SimulationEntity:
    """Construct a single country entity with realistic Greece-like attributes."""
    return SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes={
            "gdp_growth_rate":       _qty(-0.057, VariableType.RATIO),
            "unemployment_rate":     _qty(0.178, VariableType.RATIO),
            "primary_surplus_gdp":   _qty(-0.025, VariableType.RATIO),
            "debt_gdp_ratio":        _qty(1.46, VariableType.RATIO),
            "human_development_idx":  _qty(
                0.853, VariableType.RATIO, framework=MeasurementFramework.HUMAN_DEVELOPMENT
            ),
            "co2_boundary_proximity": _qty(
                0.72, VariableType.RATIO, framework=MeasurementFramework.ECOLOGICAL
            ),
        },
        metadata={"iso3": entity_id},
    )


def _relationship(
    source: str, target: str, rel_type: str = "trade", weight: float = 0.6
) -> Relationship:
    return Relationship(
        source_id=source,
        target_id=target,
        relationship_type=rel_type,
        weight=weight,
    )


def _scenario_config() -> ScenarioConfig:
    return ScenarioConfig(
        scenario_id="BENCH",
        name="Phase 1 Benchmark Scenario",
        description="Engine baseline benchmark — in-memory, no DB",
        start_date=_BASE_DATE,
        end_date=_BASE_DATE + timedelta(days=365 * 15),
    )


def _build_state(n_entities: int, n_relationships: int) -> SimulationState:
    """Build an in-memory SimulationState with n_entities and n_relationships.

    Entity IDs are E000..E{n-1}. Relationships are distributed round-robin
    from each entity to its neighbours so the graph is connected and the
    total edge count matches n_relationships as closely as possible.
    """
    entity_ids = [f"E{i:03d}" for i in range(n_entities)]
    entities = {eid: _entity(eid) for eid in entity_ids}

    relationships: list[Relationship] = []
    if n_entities > 1 and n_relationships > 0:
        # Round-robin: entity i → entity (i+1) % n, cycling until quota reached
        i = 0
        while len(relationships) < n_relationships:
            src = entity_ids[i % n_entities]
            tgt = entity_ids[(i + 1) % n_entities]
            if src != tgt:
                relationships.append(_relationship(src, tgt))
            i += 1

    return SimulationState(
        timestep=_BASE_DATE,
        resolution=ResolutionConfig(),
        entities=entities,
        relationships=relationships,
        events=[],
        scenario_config=_scenario_config(),
    )


def _build_shock_event(source_id: str) -> Event:
    """A fiscal shock event that propagates through trade relationships."""
    return Event(
        event_id="BENCH-SHOCK",
        source_entity_id=source_id,
        event_type="shock",
        timestep_originated=_BASE_DATE,
        framework=MeasurementFramework.FINANCIAL,
        affected_attributes={
            "gdp_growth_rate":     _qty(-0.03, VariableType.FLOW),
            "unemployment_rate":   _qty(0.02,  VariableType.FLOW),
            "primary_surplus_gdp": _qty(-0.01, VariableType.FLOW),
        },
        propagation_rules=[
            PropagationRule(
                relationship_type="trade",
                attenuation_factor=0.4,
                max_hops=2,
            )
        ],
    )


class _ShockModule(SimulationModule):
    """Module that fires a fiscal shock on the first entity every step.

    Only fires for the first entity in the state to avoid duplicate events
    when multiple entities are present (benchmark measures propagation cost,
    not module fan-out).
    """

    def compute(
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime,
    ) -> list[Event]:
        # Fire only on the first entity to produce a single shock per step
        first_id = next(iter(state.entities))
        if entity.id != first_id:
            return []
        return [_build_shock_event(entity.id)]

    def get_subscribed_events(self) -> list[str]:
        return []


# ---------------------------------------------------------------------------
# Timing utilities
# ---------------------------------------------------------------------------

def _time_single_step_ms(state: SimulationState) -> float:
    """Time one propagate() call in milliseconds."""
    events = [_build_shock_event(next(iter(state.entities)))]
    t0 = time.perf_counter()
    propagate(state, events)
    return (time.perf_counter() - t0) * 1_000


def _median_step_time_ms(state: SimulationState) -> dict[str, float]:
    """Run _WARMUP_RUNS + _TIMING_RUNS single steps; return timing statistics."""
    for _ in range(_WARMUP_RUNS):
        _time_single_step_ms(state)

    samples = [_time_single_step_ms(state) for _ in range(_TIMING_RUNS)]
    return {
        "mean_ms":   round(statistics.mean(samples), 4),
        "median_ms": round(statistics.median(samples), 4),
        "stdev_ms":  round(statistics.stdev(samples), 4),
        "min_ms":    round(min(samples), 4),
        "max_ms":    round(max(samples), 4),
        "n_samples": _TIMING_RUNS,
    }


def _time_mc_run_seconds(state: SimulationState, n_runs: int) -> float:
    """Time N sequential ScenarioRunner.run() calls; return total elapsed seconds."""
    runner_kwargs: dict[str, Any] = {
        "scheduled_inputs": [],
        "modules": [_ShockModule()],
        "n_steps": _MC_STEPS,
        "timestep_delta": timedelta(days=365),
    }
    gc.collect()
    t0 = time.perf_counter()
    for _ in range(n_runs):
        ScenarioRunner(initial_state=state, **runner_kwargs).run()
    return time.perf_counter() - t0


# ---------------------------------------------------------------------------
# Memory measurement
# ---------------------------------------------------------------------------

def _peak_memory_mib(state: SimulationState, n_mc_runs: int) -> float:
    """Run n_mc_runs Monte Carlo iterations; return peak RSS in MiB via tracemalloc."""
    tracemalloc.start()
    runner_kwargs: dict[str, Any] = {
        "scheduled_inputs": [],
        "modules": [_ShockModule()],
        "n_steps": _MC_STEPS,
        "timestep_delta": timedelta(days=365),
    }
    for _ in range(n_mc_runs):
        ScenarioRunner(initial_state=state, **runner_kwargs).run()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return round(peak / 1_048_576, 3)  # bytes → MiB


# ---------------------------------------------------------------------------
# Benchmark suites
# ---------------------------------------------------------------------------

def bench_per_step_cost() -> dict[str, Any]:
    """Benchmark 1: per-step computation cost at 1 / 10 / 100 entities."""
    print("\n[1/4] Per-step computation cost", flush=True)
    results: dict[str, Any] = {}
    for n in (1, 10, 100):
        state = _build_state(n_entities=n, n_relationships=0)
        label = f"{n}_entities"
        print(f"      {n} entities ...", end=" ", flush=True)
        results[label] = _median_step_time_ms(state)
        print(f"{results[label]['median_ms']} ms (median)", flush=True)
    return results


def bench_propagation_scaling() -> dict[str, Any]:
    """Benchmark 2: propagation cost as relationship edges scale."""
    print("\n[2/4] Propagation scaling", flush=True)
    configs = [
        (1,   5,    "1e_5r"),
        (10,  50,   "10e_50r"),
        (10,  200,  "10e_200r"),
        (100, 1000, "100e_1000r"),
    ]
    results: dict[str, Any] = {}
    for n_entities, n_rels, label in configs:
        state = _build_state(n_entities=n_entities, n_relationships=n_rels)
        print(f"      {n_entities} entities / {n_rels} relationships ...", end=" ", flush=True)
        results[label] = _median_step_time_ms(state)
        print(f"{results[label]['median_ms']} ms (median)", flush=True)
    return results


def bench_monte_carlo_throughput() -> dict[str, Any]:
    """Benchmark 3: Monte Carlo ensemble throughput on Greece-like 1-entity scenario."""
    print("\n[3/4] Monte Carlo throughput (1 entity, 10 steps/run)", flush=True)
    state = _build_state(n_entities=1, n_relationships=0)
    results: dict[str, Any] = {}

    for n_runs in (100, 1000):
        print(f"      {n_runs} runs ...", end=" ", flush=True)
        elapsed = _time_mc_run_seconds(state, n_runs)
        results[f"{n_runs}_runs"] = {
            "total_elapsed_seconds": round(elapsed, 3),
            "mean_ms_per_run":       round((elapsed / n_runs) * 1_000, 3),
        }
        key = f"{n_runs}_runs"
        print(f"{elapsed:.3f} s total ({results[key]['mean_ms_per_run']} ms/run)", flush=True)

    return results


def bench_memory_usage() -> dict[str, Any]:
    """Benchmark 4: peak tracemalloc memory at scale."""
    print("\n[4/4] Peak memory usage", flush=True)
    results: dict[str, Any] = {}

    # 100 entities / 1000 relationships — single step
    state_large = _build_state(n_entities=100, n_relationships=1000)
    print("      100 entities / 1000 relationships (single step) ...", end=" ", flush=True)
    tracemalloc.start()
    propagate(state_large, [_build_shock_event(next(iter(state_large.entities)))])
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    results["100e_1000r_single_step_mib"] = round(peak / 1_048_576, 3)
    print(f"{results['100e_1000r_single_step_mib']} MiB peak", flush=True)

    # 1000 Monte Carlo runs — 1 entity
    state_mc = _build_state(n_entities=1, n_relationships=0)
    print("      1000 Monte Carlo runs (1 entity) ...", end=" ", flush=True)
    results["1000_mc_runs_mib"] = _peak_memory_mib(state_mc, n_mc_runs=1000)
    print(f"{results['1000_mc_runs_mib']} MiB peak", flush=True)

    return results


# ---------------------------------------------------------------------------
# Hardware fingerprint
# ---------------------------------------------------------------------------

def _hardware_info() -> dict[str, str]:
    info: dict[str, str] = {
        "platform":    platform.platform(),
        "processor":   platform.processor(),
        "python":      sys.version,
        "cpu_count_logical": str(os.cpu_count()),
    }
    # Physical core count — best-effort, not available on all platforms
    try:
        import psutil  # type: ignore[import-untyped]
        info["cpu_count_physical"] = str(psutil.cpu_count(logical=False))
        info["ram_total_gib"] = str(round(psutil.virtual_memory().total / (1024 ** 3), 1))
    except ImportError:
        info["cpu_count_physical"] = "run: wmic cpu get NumberOfCores"
        info["ram_total_gib"] = "run: wmic memorychip get Capacity"
    return info


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", metavar="PATH", help="Write JSON summary to this path")
    args = parser.parse_args()

    print("=" * 60)
    print("WorldSim Phase 1 Baseline Benchmarks — Issue #514")
    print("=" * 60)

    hw = _hardware_info()
    print("\nHardware:")
    for k, v in hw.items():
        print(f"  {k}: {v}")

    results: dict[str, Any] = {
        "benchmark_date":   datetime.now(UTC).isoformat(),
        "hardware":         hw,
        "methodology": {
            "warmup_runs":   _WARMUP_RUNS,
            "timing_runs":   _TIMING_RUNS,
            "mc_steps_per_run": _MC_STEPS,
            "timing_function": "time.perf_counter()",
            "memory_function": "tracemalloc.get_traced_memory() peak",
            "scenario_construction": "in-memory (no database)",
        },
        "benchmarks": {
            "1_per_step_cost":          bench_per_step_cost(),
            "2_propagation_scaling":    bench_propagation_scaling(),
            "3_monte_carlo_throughput": bench_monte_carlo_throughput(),
            "4_memory_usage":           bench_memory_usage(),
        },
    }

    print("\n" + "=" * 60)
    print("Complete. JSON summary:")
    print("=" * 60)
    json_out = json.dumps(results, indent=2)
    print(json_out)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json_out, encoding="utf-8")
        print(f"\nJSON written to: {out_path}")


if __name__ == "__main__":
    main()
