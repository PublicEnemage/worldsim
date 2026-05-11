# Legibility Baseline — Milestone 7 Exit

**Date:** 2026-05-11
**Milestone:** M7 — Technical Foundation (Complete — v0.7.0)
**Purpose:** Establish quantitative legibility baseline before M8 implementation opens. Metrics recaptured at each milestone exit per Issue #257 (blind audit) and Issue #259 (legibility dashboard).
**Tool versions:** radon 6.x; Python 3.10; measured against `backend/app/` excluding `__init__.py` and generated files.

---

## Category 1 — Cognitive Complexity (radon cc)

**Scope:** 245 blocks analyzed across `backend/app/`.
**Overall average:** A (3.29) — healthy baseline; mean complexity is well within maintainable range.

### Grade distribution

| Grade | Complexity range | Count | Percentage |
|---|---|---|---|
| A | 1–5 | 213 | 86.9% |
| B | 6–10 | 21 | 8.6% |
| C | 11–15 | 10 | 4.1% |
| D | 16–24 | 1 | 0.4% |

### Top-10 highest complexity blocks

| Score | Grade | Block | File |
|---|---|---|---|
| 24 | D | `get_measurement_output` (F) | `api/scenarios.py:878` |
| 20 | C | `choropleth_delta` (F) | `api/countries.py:434` |
| 19 | C | `compare_scenarios` (F) | `api/scenarios.py:380` |
| 17 | C | `WebScenarioRunner.run_single_step` (M) | `simulation/web_scenario_runner.py:185` |
| 16 | C | `_build_attributes` (F) | `db/seed/natural_earth_loader.py:75` |
| 15 | C | `MacroeconomicModule.compute` (M) | `simulation/modules/macroeconomic/module.py:84` |
| 12 | C | `DemographicModule.compute` (M) | `simulation/modules/demographic/module.py:49` |
| 12 | C | `EcologicalModule.compute` (M) | `simulation/modules/ecological/module.py:76` |
| 12 | C | `GovernanceModule.compute` (M) | `simulation/modules/governance/module.py:53` |
| 12 | C | `_choropleth_from_snapshot` (F) | `api/countries.py:328` |

**Observations:**
- One D-rated function: `get_measurement_output` (complexity 24) in `api/scenarios.py`. This is the multi-framework output builder. ARCH-REVIEW-005 already flagged the composite score dispatch as needing refactoring (Issue #218 input).
- The four module `compute()` methods all grade C (12) with identical structure — this is a known pattern, not an organic complexity signal. The shared elasticity-registry loop is the dominant contributor in all four.
- `compare_scenarios` (C, 19) and `choropleth_delta` (C, 20) are the two API endpoints with the highest complexity and no corresponding unit tests at current coverage levels.

---

## Category 2 — Silent-Failure Surface

**Method:** `grep -rn "^\s*return \[\]\|return None\|return {}"` across `backend/app/`, excluding `__init__.py`, `test_*`, and `*_test.py`.

### Counts

| Pattern | Count | Risk classification |
|---|---|---|
| `return []` | 20 | Mixed — see below |
| `return None` | 12 | Mixed — see below |
| `return {}` | 2 | Low — boundary guard clauses |
| **Total** | **34** | |

### Classification

**Legitimate guard clauses (expected and documented):** 26 of 34

The majority are guard clauses at function entry points that follow the established module pattern:
- Module `compute()` guards: 12 occurrences across 4 modules (entity type check + empty prior_events check). All 8 empty-prior-events returns are logged at DEBUG level per M7 `[SIM-INTEGRITY]` work (Issues #244, #245).
- `_extract_magnitude` returns: 4 occurrences across modules — checks for empty `affected_attributes`. By design; caller is responsible for checking the return value.
- `TerritorialValidator._check_*` returns: 5 occurrences — guard clauses at boundary condition entry, consistent pattern.
- `countries.py:55,59` (`return {}`) — attribute parsing boundary guard.

**Higher-risk silent returns (no logging, caller may not check):** 8 of 34

| Location | Pattern | Risk |
|---|---|---|
| `web_scenario_runner.py:638,653,661` | `return []` | Three consecutive early exits in `_load_prior_breach_events`; no `[SIM-INTEGRITY]` log |
| `web_scenario_runner.py:500,510,518` | `return None` | `_build_*_module` builder functions return `None` when module not configured; callers must check but no assertion enforces this |
| `api/scenarios.py:829,852` | `return None` | `_compute_composite_score` inner logic; `None` propagates silently into the framework output |
| `db/seed/natural_earth_loader.py:97,103,187` | `return None` | Seed loader; lower production risk but no logging on missed paths |

**Total higher-risk silent returns: 8**. Target for M8: reduce to ≤ 4 by adding `[SIM-INTEGRITY]` logging to the three `web_scenario_runner.py` locations and assertion coverage on the module builder `None` returns.

---

## Category 3 — Test-to-Implementation Ratio

**Method:** `wc -l` on implementation files vs. matching test files per module. Total includes all `backend/tests/` files (unit, integration, backtesting).

| Module | Impl lines | Test lines | Ratio |
|---|---|---|---|
| `simulation/engine` | 902 | 1,813 | 2.01 |
| `modules/macroeconomic` | 235 | 540 | 2.30 |
| `modules/demographic` | 277 | 320 | 1.16 |
| `modules/ecological` | 277 | 571 | 2.06 |
| `modules/governance` | 217 | 334 | 1.54 |
| `simulation/orchestration` | 1,332 | 902 | 0.68 |
| `simulation/repositories` | 426 | 666 | 1.56 |
| `api` | 1,678 | 751 | 0.45 |
| `web_scenario_runner` | 735 | 594 | 0.81 |
| `mda_checker` | 220 | 604 | 2.75 |
| **TOTAL** | **8,085** | **14,752** | **1.82** |

**Observations:**
- Overall ratio of 1.82 is healthy — more test lines than implementation lines on aggregate.
- Two modules below 1.0: `api` (0.45) and `orchestration` (0.68). These are the largest modules and the lowest-tested by line count. `api/scenarios.py` contains `get_measurement_output` (complexity D, 24) with no dedicated unit tests at the function level.
- `demographic` module at 1.16 is the lowest among simulation modules — lowest-tested of the four domain modules.
- `mda_checker` at 2.75 is the best-covered module by this metric.

**M8 targets:**
- `api` ratio: improve from 0.45 toward 0.70 by adding unit tests for `get_measurement_output` and `compare_scenarios` as part of M8 implementation work.
- `orchestration` ratio: improve from 0.68 toward 0.90.

---

## Category 4 — Module Docstring and Intent Coverage

**Method:** Manual audit of module-level docstrings for presence of: (1) what the module does, (2) what events it subscribes to, (3) what events it produces, (4) known limitations or deferred scope.

| Module | Has purpose statement | Subscription declared | Output declared | Known limitations noted |
|---|---|---|---|---|
| `simulation/engine/propagation.py` | No module docstring | N/A | N/A | No |
| `simulation/engine/models.py` | No module docstring | N/A | N/A | No |
| `simulation/engine/quantity.py` | Yes | N/A | N/A | Yes (propagate_confidence limitation) |
| `modules/macroeconomic/module.py` | Yes (inline) | Yes (`_SUBSCRIBED_EVENTS`) | Implicit | No |
| `modules/demographic/module.py` | Yes (inline) | Yes (`_SUBSCRIBED_EVENTS`) | Implicit | No |
| `modules/ecological/module.py` | Yes (full docstring) | Yes | Yes | Yes (ADR-005 Amendment B note, M8 obligation) |
| `modules/governance/module.py` | Yes (full docstring) | Yes | Yes | Yes (Issue #211 reference — stale; see ARCH-REVIEW-005) |
| `simulation/web_scenario_runner.py` | No module docstring | N/A | N/A | No |
| `api/scenarios.py` | No module docstring | N/A | N/A | No |
| `simulation/orchestration/runner.py` | No module docstring | N/A | N/A | No |

**Observation:** No module-level docstrings in the four highest-complexity files (`propagation.py`, `models.py`, `web_scenario_runner.py`, `api/scenarios.py`). The ecological and governance modules have the best docstring coverage — this is the pattern to extend to the engine files in M9.

---

## Summary — M7 Baseline Scores

| Category | Metric | M7 value | M8 target |
|---|---|---|---|
| Cognitive complexity | Average grade | A (3.29) | Maintain A; reduce D-grade functions to 0 |
| Cognitive complexity | D-grade blocks | 1 (`get_measurement_output`) | 0 |
| Cognitive complexity | C-grade blocks | 10 | ≤ 8 |
| Silent-failure surface | Total bare returns | 34 | ≤ 34 (hold) |
| Silent-failure surface | Higher-risk unlogged | 8 | ≤ 4 |
| Test coverage | Overall ratio | 1.82 | ≥ 1.82 (hold) |
| Test coverage | Lowest module (`api`) | 0.45 | ≥ 0.60 |
| Intent coverage | Modules with full docstring | 2 of 10 | 4 of 10 |

---

*Captured by PM Agent executing Issue #255. Next recapture at M8 exit.*
*Related: Issue #257 (blind code audit M7 baseline), Issue #259 (legibility dashboard).*
