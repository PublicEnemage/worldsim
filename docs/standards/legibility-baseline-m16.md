# Legibility Baseline — Milestone 16 Exit

**Date:** 2026-06-23
**Milestone:** M16 — Distributional Visibility (in progress)
**Purpose:** Record Tier 1 legibility metrics against the M16 codebase before the milestone closes.
Establishes thresholds and current values for the four Tier 1 metrics per Issue #259
(CTO legibility metrics dashboard).
**Tool versions:** radon 6.x; Python 3.13; measured against `backend/app/` excluding `__init__.py`.
**Prior baseline:** `docs/standards/legibility-baseline-m7.md` (M7 exit — v0.7.0).

---

## Tier 1 Threshold Table

| Metric | Green | Yellow | Red | M16 measured value | Status |
|---|---|---|---|---|---|
| Mean cognitive complexity (radon cc) | ≤ 5.0 | 5.1 – 10.0 | > 10.0 | 3.33 | ✅ Green |
| p90 function length (lines) | ≤ 50 | 51 – 100 | > 100 | 76 | 🟡 Yellow |
| Silent-failure surface (bare unlogged returns) | ≤ 30 | 31 – 50 | > 50 | 50 | 🟡 Yellow |
| Test-to-implementation ratio (lines) | ≥ 2.0 | 1.5 – 1.99 | < 1.5 | 2.32 | ✅ Green |

**Measurement date:** 2026-06-23 (M16 active, pre-G1/G2/G3 implementation commits).

---

## Category 1 — Cognitive Complexity (radon cc)

**Scope:** 338 blocks analyzed across `backend/app/`.
**Overall average:** A (3.33) — within green band; marginal increase from M7 baseline (3.29).

### Grade distribution

| Grade | Complexity range | Count | Percentage |
|---|---|---|---|
| A | 1–5 | 284 | 84.0% |
| B | 6–10 | 34 | 10.1% |
| C | 11–15 | 18 | 5.3% |
| D | 16–24 | 2 | 0.6% |

### Top-10 highest complexity blocks

| Score | Grade | Block | File |
|---|---|---|---|
| 24 | D | `get_scenario_initial_state` (F) | `api/scenarios.py` |
| 20 | C | `choropleth_delta` (F) | `api/countries.py` |
| 20 | C | `trace_propagation` (F) | `simulation/propagation.py` |
| 17 | C | `profile_propagation` (F) | `simulation/propagation.py` |
| 16 | C | `_build_attributes` (F) | `db/seed/natural_earth_loader.py` |
| 15 | C | `_reconstruct_state_from_snapshot` (F) | `api/scenarios.py` |
| 15 | C | `PoliticalEconomyModule` (C) | `simulation/modules/political_economy/module.py` |
| 14 | C | `_apply_event_matrix` (F) | `simulation/propagation.py` |
| 12 | C | `_deserialize_control_input` (F) | `api/scenarios.py` |
| 12 | C | `_build_next_state` (F) | `simulation/orchestration/runner.py` |

**Observations:**
- D-grade count: 2 (`get_scenario_initial_state` at 24; same block flagged since M7). The D-count
  has grown from 1 (M7) to 2 (M16). `PoliticalEconomyModule` is a new C-grade addition since M7
  reflecting the M14 political economy module implementation.
- C-grade blocks: 18 (up from 10 at M7). Growth is proportionate to codebase expansion;
  does not indicate architectural deterioration but warrants monitoring.
- The four core simulation modules (`macroeconomic`, `demographic`, `ecological`, `governance`)
  remain at B-grade average — the shared elasticity-registry loop pattern is established and stable.

**M17 target:** Reduce D-grade blocks from 2 to 0 by refactoring `get_scenario_initial_state`
(complexity 24). This was the target at M8 and has not been executed. File as technical debt
issue if not addressed at M17 sprint entry.

---

## Category 2 — Function Length Distribution

**Method:** AST-based measurement using `ast.FunctionDef.end_lineno - lineno + 1` across
all `backend/app/**/*.py` files.

| Statistic | Value |
|---|---|
| Function count | 207 |
| Median | 19 lines |
| p90 | 76 lines |
| p95 | 98 lines |
| Maximum | 229 lines |

**Observations:**
- p90 of 76 lines falls in the yellow band (51–100). This means 10% of functions exceed 76 lines.
- The maximum (229 lines) is in `get_scenario_initial_state` — the same D-grade complexity block.
  Reducing this one function would improve both the complexity and length metrics simultaneously.
- Median of 19 lines is healthy. The distribution is right-skewed by a small number of large
  orchestration and API endpoint functions.

**M17 target:** Reduce p90 toward ≤ 60 lines by decomposing the top-5 longest functions
(all above 100 lines) as part of technical debt work.

---

## Category 3 — Silent-Failure Surface

**Method:** `grep -rn "^\s*return \[\]\|return None\|return {}"` across `backend/app/`,
excluding `__init__.py`, `test_*`, and `*_test.py`.

### Count

| Pattern | Count |
|---|---|
| `return []` | 23 |
| `return None` | 25 |
| `return {}` | 2 |
| **Total** | **50** |

**Observations:**
- Total of 50 is at the yellow/red boundary. Significant increase from M7 (34) — growth of 16
  over 9 milestones, proportionate to codebase expansion but warrants classification.
- Legitimate guard clauses (expected and documented) account for approximately 35 of 50.
  The remaining 15 are unclassified at M16 baseline measurement.
- The PoliticalEconomyModule introduced in M14 contributes several `return None` guard clauses
  not yet documented with `[SIM-INTEGRITY]` logging per the M7 standard.

**M17 target:** Classify all 50 returns. Add `[SIM-INTEGRITY]` logging to unlogged high-risk
returns. Reduce total higher-risk unlogged count to ≤ 8 (matching M7 classification target).

---

## Category 4 — Test-to-Implementation Ratio

**Method:** `wc -l` on `backend/app/**/*.py` (implementation) vs `backend/tests/**/*.py` (tests).

| Scope | Lines |
|---|---|
| Implementation (`backend/app/`) | 14,059 |
| Tests (`backend/tests/`) | 32,551 |
| **Ratio** | **2.32** |

**Observations:**
- Overall ratio of 2.32 is in the green band (≥ 2.0). Strong improvement from M7 baseline (1.82).
- The ratio increase reflects M8–M15 investment in backtesting infrastructure and QA test coverage
  per sprint entry requirements (QA test authorship gate).
- Per-module breakdown not reproduced at M16 (full module audit is Tier 2 scope — see below).
  Full module breakdown was last measured at M7 exit; `api/scenarios.py` was the lowest-covered
  module at 0.45 and is expected to remain below the overall ratio.

**M17 target:** Hold ≥ 2.0 overall ratio. Add per-module breakdown to M17 baseline.

---

## Tier 2 and Tier 3 Metrics (Out of Scope for M16)

The following metrics from Issue #259 are semi-automated or qualitative and are not
CI-computable for M16. They are recorded as future work with no current-milestone values.

| Metric | Tier | Status |
|---|---|---|
| Blind audit mean score (external reviewer) | Tier 2 | Future work — requires external reviewer session |
| Assumption documentation rate (module-level docstrings) | Tier 3 | Future work — qualitative audit |

Per M7 baseline, 2 of 10 modules had full docstrings (ecological, governance). This metric
was not re-measured at M16 but is expected to have improved given M8–M15 documentation
requirements. Measure at M17 exit as part of the expanded Tier 2 sweep.

---

## Summary — M16 Baseline Scores

| Category | Metric | M16 value | M17 target |
|---|---|---|---|
| Cognitive complexity | Average grade | A (3.33) | Maintain A |
| Cognitive complexity | D-grade blocks | 2 | 0 |
| Cognitive complexity | C-grade blocks | 18 | ≤ 15 |
| Function length | p90 | 76 lines | ≤ 60 lines |
| Function length | Maximum | 229 lines | ≤ 150 lines |
| Silent-failure surface | Total bare returns | 50 | ≤ 40 (classify + log unlogged) |
| Test coverage | Overall ratio | 2.32 | ≥ 2.0 (hold) |

---

*Captured by Technical Standards Agent executing Issue #259. Next recapture at M17 exit.*
*Related: legibility-baseline-m7.md (M7 reference), Issue #259 (dashboard), Issue #257 (blind audit).*
