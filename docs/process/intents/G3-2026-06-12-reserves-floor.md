---
name: G3-reserves-floor
type: intent
sprint-group: G3
issues: "#799"
milestone: M13
authored-by: Chief Engineer Agent
authored-date: 2026-06-12
implementing-agent: Chief Engineer Agent
adr-reference: None — engine correctness fix with architectural note
---

# Implementation Intent: G3 — Reserves Non-Negativity Floor

## 1. Source ADR

**ADR:** None — this is a simulation integrity fix. An architectural note is embedded
in the implementation explaining the constraint registry design.
**Status at time of authorship:** N/A
**Authored by:** Chief Engineer Agent
**Date:** 2026-06-12
**Implementing agent:** Chief Engineer Agent

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:** All personas — this is a simulation integrity fix. A negative
reserve value is analytically incorrect and would undermine the credibility of any
analytical output citing reserve coverage.

**P-2 — Entry state:** N/A — engine fix, not a user-visible feature.

**P-3 — Journey step:** N/A

**P-4 — Time/interaction ceiling:** N/A

**P-6 — Negotiating leverage delivered:** N/A — correctness prerequisite.

**P-7 — North star capability delivered:** After this fix, the reserve coverage metric
never shows a physically impossible negative value — a finance ministry analyst citing
"JOR reserves at 0.0 months" in a cabinet meeting will not have the credibility undermined
by a negative value appearing in any exported output or screenshot.

---

## 3. Observable Application State

### 3.1 Primary observable state

After running the Hormuz scenario 8 steps (JOR entity), `reserve_coverage_months` at
step 7 is exactly `0.0` (floored), not a negative value. The value returned by
GET /api/v1/scenarios/{id}/trajectory, in the JOR entity's steps[6].frameworks["financial"]
composite score chain, reflects a scenario where reserves cannot go below zero.

Directly observable: the engine state snapshot for JOR at step 7 shows
`reserve_coverage_months` ≥ 0.0 (verified via `GET /api/v1/scenarios/{id}/snapshot?step=7&entity_id=JOR`).

### 3.2 Secondary observable states

**Secondary 1:** All existing backtesting fixtures (Greece 2010, Argentina 2001) still
pass — `cd backend && python -m pytest tests/backtesting/ -v` exits 0.

**Secondary 2:** All unit tests still pass — `cd backend && python -m pytest tests/unit/ -v`
exits 0.

### 3.3 Silent failure detection

Silent failure: The floor is applied but only to a display formatter (client-side clamping),
not to the engine state. Distinguishing characteristic: `GET .../snapshot?step=7&entity_id=JOR`
returns a negative `reserve_coverage_months` value in state_data even though the trajectory
shows 0.0. After fix: snapshot state_data shows ≥ 0.0.

---

## 4. Acceptance Criteria

**AC-1:** After running the Hormuz scenario (JOR+EGY, 8 steps), the engine state snapshot
for JOR at step 7 has `reserve_coverage_months` ≥ 0.0 in the state_data JSONB field.
(Verified by unit test against `_build_next_state` with a mock accumulator that produces
a negative reserve delta.)

**AC-2:** A new unit test `test_reserve_coverage_months_floor_at_zero` passes: given an
entity with `reserve_coverage_months = 0.5` and a FLOW delta of `-2.0`, after `_build_next_state`,
the attribute value is `0.0` (not `-1.5`).

**AC-3:** `cd backend && python -m pytest tests/backtesting/ -v` exits 0 with the floor active.

**AC-4:** `cd backend && python -m pytest tests/unit/ -v` exits 0 with the floor active.

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for
Persona 2 to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` No — this is a correctness fix. The observable state (reserve value ≥ 0) is a
physical constraint, not an analytical output requiring interpretation.

---

## 6. Out of Scope

- General domain constraint system for all simulation attributes (full registry design
  is deferred; this fix applies the floor only to known non-negative stock/flow attributes).
- Percentage ceiling (≤ 1.0) for ratio attributes — separate issue.
- Display-layer changes: `_format_months()` client-side clamping in the demo script is
  retained as a defensive display guard but is no longer the primary correctness mechanism.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before G3 implementation PR is opened
**Test file location:** `backend/tests/unit/test_g3_reserves_floor.py` (new file)
**Relevant ADR acceptance criteria:** AC-1 through AC-4

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-4 authored and filed. 2026-06-12
