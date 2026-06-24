---
name: M16-G9-compare-threshold-crossing-markers
type: implementation-intent
issues: "#97"
status: Filed — QA tests required before implementation PR opens
authored-by: PM Agent (pre-implementation spec; Chief Engineer Agent takes implementation authority at Step 3)
authored-date: 2026-06-24
implementing-agent: Chief Engineer Agent
sprint-entry: "docs/process/sprint-plans/m16-g9-sprint-entry.md — EL Approved 2026-06-24"
adr-reference: "None — additive field extension within existing /compare endpoint scope; Architect consultation CLEAR (sprint entry §2.2)"
release-branch: release/m16
sequencing: "After G2 merges to release/m16 — API contract must be stable before extension; G2 extends backend data contracts and must land before /compare is modified to avoid contract drift"
---

# Implementation Intent: M16-G9 — Threshold-Crossing Markers in Compare Output (#97)

> **G9 capacity-allowing.** Not Demo 6 critical path. If capacity is exhausted before G8 is
> scheduled, this issue carries to M17.
> Implementation does not begin until: (1) G2 merges to `release/m16`; (2) this intent document
> is committed to `release/m16`; (3) the implementing agent reads `docs/schema/api_contracts.yml`
> to confirm the exact compare endpoint path and current response shape; (4) QA tests are authored
> from this document's ACs.
> **Backend pre-push lint gate mandatory:** `cd backend && ruff check . && mypy app/` — exits 0
> before any push modifying `backend/`.

---

## 1. Source Authority

**Issue:** #97 — arch(api): threshold-crossing markers in compare output
**Sprint entry:** `docs/process/sprint-plans/m16-g9-sprint-entry.md` — EL Approved 2026-06-24
**ADR gate:** None — additive field extension within existing `/compare` endpoint pattern
**Schema reference (mandatory pre-implementation read):** `docs/schema/api_contracts.yml` —
confirm compare endpoint path, request shape, and current response shape before writing
any implementation code (CLAUDE.md §Schema registry mandate)
**Date authored:** 2026-06-24
**Authored by:** PM Agent (pre-implementation spec)
**Implementing agent:** Chief Engineer Agent

---

## 2. Persona Trace Elements Targeted

**P-1 — Personas served:**
**Persona 2 — Finance Ministry Negotiator** (Aicha Mbaye archetype, `docs/ux/personas.md §Persona 2`).
The compare API enables multi-scenario comparison in the frontend — which scenario avoids the
threshold crossing at step 4? Without `threshold_crossings` in the compare response, a frontend
view that marks threshold-crossing steps across compared scenarios would require a separate
per-scenario endpoint call for each entity, degrading performance and creating data consistency
risk. Adding `threshold_crossings` to the compare response makes this information available in
a single call, enabling a future frontend sprint to render threshold-crossing markers in the
comparison view without additional backend round-trips.

For Persona 2, the downstream capability is: the comparison argument
("Scenario B avoids the threshold crossing at step 4 that Scenario A triggers — two steps later
and it is still above the MDA floor") is computable from one API response.

**P-2 — Entry state:**
Preparatory (3-hour briefing window). Multi-scenario comparison is a Preparatory-state activity —
Persona 2 sets up scenarios and reviews comparison outputs before the negotiating session.
The `threshold_crossings` field is infrastructure for Preparatory analysis and for future frontend
comparison views.

**P-3 — Journey reference:**
Journey A (Preparatory briefing) — scenario comparison before the consultation session.
Persona 2 runs two scenarios (IMF proposal vs. ministry alternative) and uses the compare
endpoint response to identify where threshold crossings diverge between paths.

**P-4 — Time/interaction ceiling:**
Backend API infrastructure — no direct interaction ceiling in this sprint. Preparatory tool.
The 90-second ceiling will apply when a frontend view consuming this field is implemented.

**P-7 — North star capability delivered:**
The compare API returns `threshold_crossings` per entity per step, enabling a future frontend
sprint to mark threshold-crossing steps in a comparison view without additional backend calls.
The Zambia finance ministry analyst obtains threshold-crossing information for two compared
scenarios in a single `/compare` API response — the data is available; its visual expression
is a future sprint deliverable.

---

## 3. Observable Application State

*All states verifiable by calling the API directly (curl, Playwright network intercept, or pytest
integration test). No source code reading, no CI report reference.*

*Note: The implementing agent must verify the exact compare endpoint path and query parameter
names from `docs/schema/api_contracts.yml` before authoring any test. This document uses
`/compare?scenario_a={id_a}&scenario_b={id_b}` as a placeholder — the canonical path is
`api_contracts.yml`-authoritative.*

### 3.1 Primary observable state

`GET /compare?scenario_a={zmb_ecf_id}&scenario_b={zmb_alt_id}` returns HTTP 200.

The response body for each entity-step entry includes a `threshold_crossings` field. The field
is a list. Each entry in the list has two keys:
- `threshold_name` (string): identifies the MDA threshold (e.g., `"poverty_headcount_q1_floor"`)
- `crossed` (boolean): `true` if this threshold was crossed at this step

For the ZMB ECF scenario at the step where poverty_headcount_ratio Q1 crosses the MDA floor
(step 2, per G2 implementation): `threshold_crossings` contains at least one entry with
`crossed: true` and a non-empty `threshold_name` string.

### 3.2 Secondary observable states

**State A — JOR ECF threshold crossings:**
`GET /compare?scenario_a={jor_ecf_id}&scenario_b={jor_alt_id}` returns HTTP 200.
At the JOR threshold-crossing step (implementing agent confirms step number from G2 implementation
and `docs/schema/api_contracts.yml`): `threshold_crossings` contains at least one entry with
`crossed: true`.

**State B — No crossings → empty list (not null, not absent):**
For a step where no MDA threshold is crossed in either compared scenario:
`threshold_crossings` is an empty list `[]`. The field is present in the response body — it is
not absent, not `null`. The response is HTTP 200.

**State C — api_contracts.yml updated in same commit:**
`docs/schema/api_contracts.yml` contains `threshold_crossings` as a documented field in the
compare response schema definition. The field documentation includes type (array), entry shape
(`threshold_name`: string, `crossed`: boolean), and behavior when empty (empty array, not null).
This update is committed in the same PR as the backend implementation.

**State D — Existing compare fields unchanged:**
The compare response for existing fields (`delta`, `baseline`, `distribution` from G4 if
present) is unchanged. No existing field is renamed, removed, or has its type altered. The
`threshold_crossings` addition is purely additive.

### 3.3 Silent failure detection

**Silent failure 1 — Field present but always empty:**
`threshold_crossings` is always `[]` regardless of whether thresholds were crossed — the field
exists in the schema but the backend never populates it (the query returns no MDA threshold data).
Detection: AC-2 asserts that the ZMB ECF response at the crossing step contains a non-empty list.

**Silent failure 2 — Field absent from response:**
The response body omits `threshold_crossings` entirely (field not serialized). Detection:
AC-1 asserts field presence — `"threshold_crossings" in response_data` for each step entry.

**Silent failure 3 — Crossing reported at wrong step:**
The backend reports a crossing at step N+1 or N-1 rather than the actual crossing step.
Detection: AC-2 asserts the crossing entry at the correct step index, not an adjacent step.

**Silent failure 4 — api_contracts.yml not updated:**
The backend ships but the schema file is not updated — schema drift compliance violation.
Detection: AC-5 checks for `threshold_crossings` in `api_contracts.yml`. If the implementing
agent updates the backend but not the schema file, AC-5 fails.

---

## 4. Acceptance Criteria

*Each criterion verifiable by calling the running API or reading the schema file.
Test file: `backend/tests/test_m16_g9_compare_threshold_markers.py`*

*Before authoring tests: verify the exact compare endpoint path from `docs/schema/api_contracts.yml`.
Replace the placeholder path below with the canonical path.*

**AC-1 (threshold_crossings field present in compare response):**
`GET /compare?scenario_a={zmb_ecf_id}&scenario_b={zmb_alt_id}` returns HTTP 200.
For each entity-step entry in the response body, `"threshold_crossings"` is a key in the entry.
The value is a list (may be empty `[]` for steps with no crossings). The field is not absent;
it is not `null`.

**AC-2 (threshold_crossings populated at crossing step for ZMB):**
For the ZMB ECF scenario at step 2 (the step where poverty_headcount_ratio Q1 crosses the MDA
floor per G2 implementation — implementing agent confirms step number from G2 test assertions):
The entry's `threshold_crossings` list is non-empty. At least one entry has `"crossed": true`.
That entry has a non-empty string value for `"threshold_name"`.
*(Validates that the backend reads MDA configuration and compares against it, not just returning
empty lists for all steps.)*

**AC-3 (threshold_crossings populated for JOR ECF at crossing step):**
For the JOR ECF scenario at the relevant threshold-crossing step (implementing agent confirms from
G2 implementation and `docs/schema/api_contracts.yml`):
`threshold_crossings` is a non-empty list with at least one entry having `"crossed": true`.

**AC-4 (empty list for step with no crossings — not null, not absent):**
For the ZMB ECF scenario at step 0 (initial state, no thresholds crossed):
`threshold_crossings` value is `[]` (empty list). The key is present. The response is HTTP 200.

**AC-5 (api_contracts.yml updated in same PR):**
`docs/schema/api_contracts.yml` content includes the string `"threshold_crossings"` within the
compare response schema definition. The schema entry documents: type as array, entry shape
(`threshold_name` string, `crossed` boolean), and empty-list behavior. This file change is
committed in the same PR as the backend implementation — not a follow-up PR.

**AC-6 (existing compare fields unchanged — non-regression):**
`GET /compare?...` response body for existing fields (`delta`, `baseline`; and `distribution`
if present from G4) is unchanged in type, name, and nullability contract. The
`threshold_crossings` addition is verified additive-only: the pre-existing fields' values for
the ZMB ECF scenario at each step are numerically identical before and after the PR.

---

## 4b. Visual Spec (before/after)

*Backend API response — no frontend display component in G9 scope.*

### AC-1/AC-2 — Compare response shape

**AC-1/AC-2 (before — no threshold_crossings field):**
```
GET /compare?scenario_a={zmb_ecf_id}&scenario_b={zmb_alt_id}
Response body (simplified, ZMB step 2 entry):
{
  "entity": "ZMB",
  "step": 2,
  "delta": -0.04,
  "baseline": 0.51
  /* "threshold_crossings" key is ABSENT */
}
```

**AC-1 (after — field present, empty at non-crossing step):**
```
GET /compare?...
Response body (step 0, no crossings):
{
  "entity": "ZMB",
  "step": 0,
  "delta": 0.00,
  "baseline": 0.58,
  "threshold_crossings": []    ← field PRESENT, empty list
}
```

**AC-2 (after — field populated at crossing step):**
```
GET /compare?...
Response body (step 2, threshold crossed):
{
  "entity": "ZMB",
  "step": 2,
  "delta": -0.04,
  "baseline": 0.51,
  "threshold_crossings": [
    {
      "threshold_name": "poverty_headcount_q1_floor",
      "crossed": true
    }
  ]
}
```

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` **No** — with conditions.

`threshold_crossings` is a backend API field. Its user-facing expression is a future frontend
sprint deliverable (threshold-crossing markers in a comparison view). This intent delivers the
API contract only. The kryptonite constraint applies to the eventual frontend rendering and will
be assessed again when the frontend comparison view consuming this field is implemented.

Backend API infrastructure that enables a future self-interpreting frontend display does not
itself introduce kryptonite risk. The `threshold_name` and `crossed` boolean are interpretable
without specialist translation by a developer implementing the frontend view — this is the
primary audience for the API field.

---

## 6. Out of Scope

| Scope item | Rationale for exclusion |
|---|---|
| Frontend display of threshold_crossings (markers in Zone 1A or comparison views) | #97 delivers the API field only. Frontend rendering of threshold-crossing markers is a separate sprint. |
| MDA alert integration or alert escalation from threshold crossings | The `threshold_crossings` field is informational only. MDA alert generation (tier escalation) is handled by the existing MDA alert system — not this PR. |
| Cohort-level threshold crossings in compare response | This field covers indicator-level MDA thresholds. Cohort-specific threshold crossings would require a separate field design extending G2's cohort data contract. |
| N > 2 entity pairwise comparison | The existing compare endpoint covers pairwise comparison. N > 2 is a separate API design. |
| Full compare API redesign | #97 is an additive field only. A comprehensive compare API overhaul is separate. |
| G2 endpoints or component files | #97 modifies the compare endpoint only. Must not touch G2-delivered endpoints or frontend component files. |

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any implementation PR is opened against `release/m16` for #97
**Test file:** `backend/tests/test_m16_g9_compare_threshold_markers.py`
**Acceptance criteria covered:** AC-1 through AC-6

**Pre-implementation read requirement:** The test author and implementing agent must read
`docs/schema/api_contracts.yml` before authoring any test or writing any implementation code —
the exact compare endpoint path and current response shape are `api_contracts.yml`-authoritative.

**Pre-push gate (mandatory):**
`cd backend && ruff check . && mypy app/` — exits 0 before any push modifying `backend/`.
`docs/schema/api_contracts.yml` must be updated in the same commit as the backend implementation.

**Sequencing note:** Implementation may not begin until G2 merges to `release/m16`.
Tests must be authored from this document before implementation code is written.

**Soft-skip guard (NM-056 follow-up):** No `test.skip()` or conditional skip patterns.
Integration tests requiring a live database must fail explicitly (not skip) when DATABASE_URL is
absent.

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-6 authored and filed. 2026-06-24

---

*Intent document authority: `docs/process/intent-template.md` (version 2026-06-17).
Sprint entry: `docs/process/sprint-plans/m16-g9-sprint-entry.md` (EL Approved 2026-06-24).
ADR authority: None (#97 additive field extension in existing endpoint boundary).
Schema authority: `docs/schema/api_contracts.yml` — mandatory pre-implementation read.
Implementing agent: Chief Engineer Agent.
G9 capacity gate: Carry to M17 if capacity is exhausted before G8 is scheduled.*
