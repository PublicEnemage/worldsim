# Engine Baseline Benchmarks — Milestone 10

**Issue:** #514  
**Author:** Chief Engineer Agent  
**Date:** 2026-05-31  
**Script:** `backend/scripts/benchmark_phase1.py`  
**Purpose:** Phase 1 baseline measurements of the iterative engine on target hardware, required before authoring ADR-009.

---

## Hardware Under Test

| Field | Dev Machine | ProBook |
|---|---|---|
| Role | High-end reference | Constrained / accessible |
| OS | macOS 26.0.1 (arm64) | Windows 11 (10.0.26200) |
| CPU | Apple M1 Pro (ARM) | Intel Core i5-8265U @ 1.60 GHz |
| Physical cores | 10 | 4 |
| Logical processors | 10 | 8 |
| RAM | — (system) | 8.0 GiB |
| Python | 3.13.11 (Anaconda) | 3.13.11 (CPython/MSC) |
| Benchmark date | 2026-05-31 | 2026-05-31 |

> The ProBook represents the lowest-specification machine on which WorldSim must run acceptably — an Intel i5-8265U laptop with 8 GiB RAM. The equity principle in CLAUDE.md §Guiding Principles requires that performance work target this hardware, not the dev machine.

---

## Methodology

| Parameter | Value |
|---|---|
| Warmup runs (discarded) | 3 |
| Timing runs per configuration | 10 |
| MC steps per run | 10 |
| Timing function | `time.perf_counter()` |
| Memory function | `tracemalloc.get_traced_memory()` peak |
| Scenario construction | In-memory — no database, no network |
| Shock type | Fiscal shock: GDP growth rate −3 pp, unemployment +2 pp, primary surplus −1 pp |
| Propagation | `relationship_type="trade"`, `attenuation_factor=0.4`, `max_hops=2` |

All scenarios use Greece-like entity attributes (GDP growth −5.7%, unemployment 17.8%, debt/GDP 146%). The entity set is synthetic — the measurement methodology is calibrated to the same helpers used in the unit test suite.

---

## Benchmark 1 — Per-Step Computation Cost

Single `propagate()` call with one shock event, no relationships (propagation cost excluded).

| Entities | Dev Machine (ms) | ProBook (ms) | Ratio |
|---|---|---|---|
| 1 | 0.0034 | 0.0074 | 2.2× |
| 10 | 0.0070 | 0.0149 | 2.1× |
| 100 | 0.046 | 0.0895 | 1.9× |

**Scaling characteristic:** Near-linear with entity count on both machines. 100-entity cost ≈ 13–14× the 1-entity cost (expected: O(n) with constant per-entity processing).

**Headroom assessment:** At 0.09 ms per step for 100 entities on the ProBook, the engine can sustain approximately 11,000 steps per second at this scale. A 15-year simulation at annual resolution (15 steps) completes in well under 2 ms of compute on constrained hardware.

---

## Benchmark 2 — Propagation Scaling

Single `propagate()` call, shock on the first entity, relationships active.

| Config | Entities | Relationships | Dev Machine (ms) | ProBook (ms) | Ratio |
|---|---|---|---|---|---|
| Sparse-small | 1 | 5 | 0.0032 | 0.0068 | 2.1× |
| Moderate | 10 | 50 | 0.1177 | 0.2422 | 2.1× |
| Dense-small | 10 | 200 | 1.6446 | 3.2108 | 2.0× |
| Sparse-large | 100 | 1000 | 0.6816 | 1.1467 | 1.7× |

**Key observation — edge density dominates over raw edge count:**

The dense-small configuration (10 entities / 200 relationships = 20 edges/entity) is significantly slower than the sparse-large configuration (100 entities / 1,000 relationships = 10 edges/entity), despite having fewer total edges. On the dev machine: 1.64 ms vs 0.68 ms. On the ProBook: 3.21 ms vs 1.15 ms.

This indicates the propagation traversal cost is sensitive to local edge density (edges per source entity) rather than total graph size. The current implementation's BFS/DFS hop traversal re-examines edges from the shock source at each hop; a densely connected source multiplies that cost superlinearly.

**Implication for ADR-009:** Worst-case scenarios (small graphs with high local connectivity) are more expensive than large sparse graphs. The engine scales well with entity count when the graph is sparse; optimization work should target the dense-neighborhood traversal path.

---

## Benchmark 3 — Monte Carlo Ensemble Throughput

Sequential `ScenarioRunner.run()` calls, 1 entity, 10 steps per run, one fiscal shock per step.

| Ensemble size | Dev Machine total (s) | Dev Machine per run (ms) | ProBook total (s) | ProBook per run (ms) | Ratio |
|---|---|---|---|---|---|
| 100 runs | 0.007 | 0.075 | 0.019 | 0.195 | 2.6× |
| 1000 runs | 0.074 | 0.074 | 0.174 | 0.174 | 2.4× |

**Throughput headline:**

| Hardware | Runs per second (1-entity, 10-step scenario) |
|---|---|
| Dev machine (M1 Pro) | ~13,500 runs/s |
| ProBook (i5-8265U) | ~5,750 runs/s |

**Scaling characteristic:** Per-run cost is stable across ensemble sizes on both machines — no per-ensemble overhead accumulation. 1,000 runs cost approximately the same per run as 100 runs, confirming the runner has no growing state between iterations.

**Headroom assessment:** A 1,000-run Monte Carlo ensemble on the ProBook completes in 174 ms. A 10,000-run ensemble projects to ~1.74 s. These are well within interactive latency budgets for the Mode 2 scenario exploration workflow.

---

## Benchmark 4 — Peak Memory Usage

| Scenario | Dev Machine (MiB) | ProBook (MiB) |
|---|---|---|
| 100 entities / 1,000 relationships — single step | 0.108 | 0.108 |
| 1,000 Monte Carlo runs — 1 entity | 0.030 | 0.030 |

Memory footprint is **identical** across both machines, as expected — `tracemalloc` measures Python heap allocations, which are architecture-independent at this scale.

**Assessment:** Memory usage is negligible at current scale. The 100-entity / 1,000-relationship single-step peak (0.108 MiB) leaves ample headroom under the 8 GiB ProBook RAM and the 7 GiB GitHub Actions runner RAM. Memory is not a near-term constraint and need not be a primary consideration in ADR-009.

---

## Cross-Machine Performance Ratio

The ProBook runs consistently **2.0–2.6× slower** than the M1 Pro dev machine across all benchmarks. This ratio is stable across workload types (per-step, propagation, Monte Carlo) and consistent with the hardware differential: a 2015-era Intel i5-8265U mobile processor at 1.60 GHz base vs a 2021 Apple M1 Pro with high-efficiency ARM cores and shared memory bandwidth.

The ratio is favorable for the equitable build mission: the engine is fast enough on constrained hardware that no benchmark result presents a blocking constraint for ADR-009 design decisions.

---

## Findings for ADR-009

These measurements establish the following facts for the engine computation model decision:

1. **The iterative engine is not the bottleneck at current scenario scale.** Per-step costs of 0.09 ms (100 entities, ProBook) and MC throughput of 5,750 runs/second are well inside interactive budget for Mode 2 scenario exploration.

2. **Edge density, not entity count, is the propagation cost driver.** A dense-neighborhood graph (10 entities / 200 relationships) costs 3× more than a sparse large graph (100 entities / 1,000 relationships). ADR-009 must model this; optimizing for entity count alone would miss the actual scaling axis.

3. **Memory is not a near-term constraint.** The current implementation uses < 0.2 MiB even at the largest benchmark configuration. Memory architecture is not a decision driver for ADR-009.

4. **The engine scales linearly with entity count when the graph is sparse.** This is the expected operating regime for national-level simulations (tens to low hundreds of entities, moderate connectivity). The iterative engine is the correct computation model for this regime.

5. **Performance on constrained hardware is acceptable for the current milestone scope.** No result on the ProBook suggests that engine redesign is urgently needed for M10 deliverables. ADR-009 should treat the sparse-matrix / vectorized approach as a performance ceiling investigation, not an immediate necessity.

---

## Reproduction

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run all four benchmark suites
python scripts/benchmark_phase1.py

# Save JSON output to a file
python scripts/benchmark_phase1.py --out bench-results.json
```

No database, network, or external services required. Runs on macOS, Linux, and Windows.
