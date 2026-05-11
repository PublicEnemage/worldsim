# Blind Code Legibility Audit — M7 Baseline — 2026-05-11

## Audit Conditions

**Date:** 2026-05-11
**Milestone:** M7 — Technical Foundation (Complete — v0.7.0)
**Gate:** Issue #257 — M7 baseline establishment
**Auditor:** Fresh Claude instance with no WorldSim session history, no access to ADRs, design documents, or implementation context. Persona: intermediate Python developer (3 years experience), competent in async Python, dataclasses, and type annotations; general familiarity with simulation systems and web APIs.
**Prompt:** docs/process/blind-code-audit-prompt.md (seven questions per function, synthesis at end)
**Functions audited (5):** Nominated per Issue #257 specification.

---

## Function 1 — `_accumulate` (`backend/app/simulation/engine/propagation.py:207`)

**Q1 — What it does:** Merges a dictionary of attribute deltas into a running accumulator keyed by entity, summing numeric values when the same attribute key appears more than once, and taking the worse (higher-numbered) confidence tier of the two contributions.

**Q2 — Parameters:**
- `accumulator`: mutable dict-of-dicts mapping entity_id → attr_name → Quantity. **Certain** — mutation pattern unambiguous.
- `entity_id`: string identifier for the entity receiving deltas. **Certain** — used as direct dict key.
- `deltas`: mapping from attribute name to Quantity delta. **Certain** — iterated directly.

**Q3 — Silent failures:**
- **Docstring-code contradiction:** docstring states "the accumulated tier is the minimum of all contributing tiers" but the code uses `max()`. One of these is wrong silently.
- **Unit mismatch silently discarded:** if `delta.unit` differs from `existing.unit`, `delta.unit` is dropped; the merged Quantity keeps `existing.unit` with no warning. Same for `variable_type`, `measurement_framework`, `observation_date`, `source_id`.

**Q4 — Lookup dependencies:**
- `_DeltaAccumulator` type alias (inferred from usage but not confirmed)
- Why STOCK collision warns but FLOW/RATIO do not (asymmetry unexplained from this file alone)
- `propagate_confidence()` — referenced in docstring as authoritative for tier rule

**Q5 — Bug hiding place:** The `max()` vs. `min()` discrepancy on `confidence_tier`. The docstring says "minimum," the code says `max`. A caller reading the docstring gets the opposite behavior from what the code implements.

**Q6 — Single improvement:** Fix the docstring to match the code. The phrase "the accumulated tier is the minimum of all contributing tiers" directly contradicts `max(existing.confidence_tier, delta.confidence_tier)`.

**Q7 — Score: 7/10** — The function body is clean and readable, but the docstring-code contradiction on the central policy rule means the intended behavior cannot be determined from this file alone.

---

## Function 2 — `_reconstruct_state_from_snapshot` (`backend/app/simulation/web_scenario_runner.py:668`)

**Q1 — What it does:** Given a snapshot's serialized state dictionary, fetches entity metadata from the database, deserializes each entity's attribute values, and assembles a SimulationState object that can be used as if it were a live engine state.

**Q2 — Parameters:**
- `conn`: live async database connection. **Certain.**
- `scenario_id`: string scenario identifier. **Certain** — passed directly into ScenarioConfig.
- `scenario_name`: human-readable scenario name. **Certain.**
- `state_data`: deserialized JSON blob mapping entity IDs to attribute envelopes. **Inferred** — type annotation `dict[str, Any]` gives no structural information.
- `timestep`: point in time this snapshot represents. **Certain** — used as both `start_date` and `end_date`.

**Q3 — Silent failures:**
- `contextlib.suppress(ValueError, KeyError)` around `quantity_from_jsonb` silently drops any attribute that fails to deserialize. Resulting entity has fewer attributes than original with no log, no counter, no caller notification.
- Entities in `state_data` with no matching row in `simulation_entities` are silently skipped (`continue`).
- `start_date=timestep, end_date=timestep` — both dates are the same value; if the consumer uses these as a range, it gets a zero-duration scenario with no indication.
- `relationships=[]` and `events=[]` — empty fields in returned state; whether this represents data loss is unknown from this code.

**Q4 — Lookup dependencies:**
- `SA-09 envelope format` — referenced in docstring; needed to understand what `quantity_from_jsonb` expects
- `ResolutionConfig()` — default-constructed with no arguments; unknown what defaults this sets
- Why imports are deferred inside the function body (unusual pattern suggesting circular imports)

**Q5 — Bug hiding place:** The `contextlib.suppress` block. A systematic deserialization failure — schema change, format migration — produces a SimulationState with empty `attributes` dicts and no error. The caller gets a state that looks valid, runs without exception, and produces wrong outputs.

**Q6 — Single improvement:** Replace `contextlib.suppress(ValueError, KeyError)` with an explicit `except` block that logs a `_log.warning` with `entity_id` and `attr_key` before continuing.

**Q7 — Score: 5/10** — Multiple silent skip paths with no logging, deferred imports signal an unexplained constraint, `SA-09` is an opaque external reference, and `start_date == end_date` raises an unanswered question about whether this produces a valid state.

---

## Function 3 — `EcologicalModule.compute` (`backend/app/simulation/modules/ecological/module.py:76`)

**Q1 — What it does:** Filters the current step's events for a given country entity to those matching subscribed types, multiplies each event's magnitude by registered elasticity coefficients, accumulates per-indicator deltas, and emits a single event containing all ecological indicator changes for that entity at that timestep.

**Q2 — Parameters:**
- `entity`: the simulation entity being processed — expected to be a country. **Certain** — explicit type guard.
- `state`: full simulation state; only `state.events` is accessed. **Inferred** — the remaining state fields are unused.
- `timestep`: current simulation timestep. **Certain** — used in logging, event ID, and event fields.

**Q3 — Silent failures:**
- `_extract_magnitude(event)` returning `None` skips the event silently with no log. A misconfigured or malformed event produces no output and no diagnostic.
- `_INDICATOR_VARIABLE_TYPES.get(key, VariableType.RATIO)` defaults to RATIO silently for unknown indicator keys.
- `unit="dimensionless"` hardcoded on every emitted Quantity — if any indicator has a real unit (e.g., ppm, tonnes), that information is permanently discarded here.
- `propagation_rules=[]` — if ecological events are supposed to propagate, this silently terminates the chain.

**Q4 — Lookup dependencies:**
- `_extract_magnitude` — what constitutes a valid vs. None-producing event; what units the return value carries
- `_event_confidence_tier` — logic opaque without reading it
- `ECOLOGICAL_ELASTICITY_REGISTRY` — the elasticity values are the entire analytical core; structure is visible but values are not
- `propagation_rules=[]` — whether this is intentionally terminal or an omission

**Q5 — Bug hiding place:** The `indicator_tiers` accumulation uses `max()` — same docstring-vs-code tension as Function 1. The interaction between the elasticity registry's tier and the event's tier as competing confidence sources is undocumented.

**Q6 — Single improvement:** Add a `_log.debug` call when `_extract_magnitude` returns `None`, naming the `event.event_type` and `entity.id`. A module that produces no output is currently indistinguishable from one that correctly determined there was nothing to update.

**Q7 — Score: 6/10** — Overall structure clear, but two helper functions are black boxes, `unit="dimensionless"` is an unexplained policy decision, `propagation_rules=[]` raises an unanswered question, and the confidence tier logic requires the same external context as Function 1.

---

## Function 4 — `computeSteps` (`frontend/src/.../ChoroplethMap.tsx`)

**Q1 — What it does:** Takes a map of country data and a desired number of color bands, extracts numeric values, sorts them, and returns an array of `steps + 1` quantile boundary points that divide the value distribution evenly — suitable for use as a color scale domain.

**Q2 — Parameters:**
- `choroplethData`: record mapping country codes to attribute summary objects. **Certain** — keys unused, only values matter.
- `steps`: number of equal-frequency buckets. **Certain** — drives quantile calculation directly.

**Q3 — Silent failures:**
- Returns `[]` when all values are non-numeric; caller receives empty array with no indication.
- `Number(a.value)` — locale-formatted strings like `"1,234"` produce `NaN` and are silently filtered, reducing the effective dataset.
- `steps = 0` produces `[sorted[0]]` (single minimum value); behavior is not documented.

**Q4 — Lookup dependencies:**
- `AttributeSummary.value` — whether it can be string, null, or object determines whether `Number()` coercion is safe or a data quality risk
- What the map rendering library expects as the shape of the domain array (whether `steps + 1` values is correct)

**Q5 — Bug hiding place:** The off-by-one between `steps` (the parameter, number of bands) and `steps + 1` (the return length, number of boundaries). Whether the consumer expects `steps` or `steps + 1` values determines whether the color scale is correct or has one missing/duplicate band.

**Q6 — Single improvement:** Add a one-line comment: `// returns steps+1 boundary values (one per quantile boundary, not one per band)`. The function name says "steps" but the output is boundaries — readers expecting `steps` values will be off by one immediately.

**Q7 — Score: 8/10** — Algorithm readable and math followable; loses points only for undocumented `steps` vs. `steps + 1` semantic, unresolved `AttributeSummary.value` type risk, and zero/one edge cases.

---

## Function 5 — `check_reconstruction_compatibility` (`backend/app/api/scenarios.py:88`)

**Q1 — What it does:** Compares the engine version and git hash recorded when a simulation snapshot was saved against the currently running engine, and raises an HTTP 409 error if they do not match — unless an explicit override flag is set, in which case it logs a warning and proceeds.

**Q2 — Parameters:**
- `tombstone_engine_version`: semantic version string stored at snapshot write time. **Certain.**
- `tombstone_git_commit_hash`: git hash stored in the snapshot, or `None` for pre-migration snapshots. **Certain** — docstring is specific.
- `force_audit_override`: keyword-only boolean that bypasses the 409. **Certain** — name, keyword enforcement, and docstring agree.

**Q3 — Silent failures:** No consequential silent failures. The `force_audit_override` path explicitly logs a WARNING. The only near-silent path: if `_ENGINE_VERSION` is empty or None at import time, a false 409 may fire — but this is a configuration failure, not a logic failure.

**Q4 — Lookup dependencies:**
- `_ENGINE_VERSION` and `_GIT_COMMIT_HASH` — how resolved at import time; whether they can be `None` vs `"unknown"`
- `tombstone` — the concept is undefined in this file; inferred to be a stored snapshot record
- `ADR-004 Decision 1 Amendment` and `SA-11` — referenced but not required to understand the function

**Q5 — Bug hiding place:** The asymmetric `None` check on `both_hashes_known`. The tombstone side checks `is not None`; the live side checks only `!= "unknown"`. If `_GIT_COMMIT_HASH` is `None` (not covered by the "unknown" guard), `both_hashes_known` becomes `True` and `None == real_hash_string` evaluates `False`, triggering a false version mismatch 409 on a valid snapshot.

**Q6 — Single improvement:** Extract `both_hashes_known` into a helper named `_hashes_comparable()` that makes the asymmetry explicit and independently testable.

**Q7 — Score: 8/10** — Well-documented, clear intent, explicit error path; loses points for the asymmetric `None` check requiring careful re-reading, and `tombstone` being undefined in the file.

---

## Synthesis

**Mean score: 6.8/10**
(7 + 5 + 6 + 8 + 8) / 5 = 6.8

**Lowest-scoring function: `_reconstruct_state_from_snapshot` (5/10)**
The combination of deferred imports (unexplained circular import signal), multiple silent skip paths with no logging, an opaque external format reference (SA-09), and a `start_date == end_date` construction of unknown semantic validity makes it impossible to modify safely without reading at least four other files.

**Cross-cutting pattern: Silent discards without diagnostic logging**
Functions 2, 3, and 4 all have paths where data is dropped, skipped, or coerced without any log output or caller notification. In Function 2: `contextlib.suppress` eats deserialization errors; `continue` skips missing entities. In Function 3: `_extract_magnitude` returning `None` has no debug log. In Function 4: `isNaN` filtering and `Number()` coercion silently reduce the dataset. The pattern is uniform: an exceptional condition that changes the output is treated as normal control flow rather than a diagnostic event. A caller in all three cases receives a result that looks valid but reflects less data than was offered.

**Standards escalation:**
"Functions that silently discard input data — via `continue`, `suppress`, `filter`, or a `None`-guard — must emit a `_log.debug` or `_log.warning` call at the discard site that names the discarded item (entity ID, attribute key, event type, or value) and the reason for discarding it."

---

## Issues Filed

| Issue | Title | Rationale |
|---|---|---|
| #279 | `_reconstruct_state_from_snapshot`: replace `contextlib.suppress` with logged except block | Lowest-scoring function; silent drop of deserialization failures is highest-risk finding |
| #280 | `_accumulate` docstring contradiction: "minimum" vs `max()` on confidence_tier | docstring and code contradict each other on the central policy rule |

*Next audit: M8 exit. Auditor must be a fresh instance with no WorldSim history.*
*Prompt: docs/process/blind-code-audit-prompt.md*
*Baseline comparison: docs/standards/legibility-baseline-m7.md*
