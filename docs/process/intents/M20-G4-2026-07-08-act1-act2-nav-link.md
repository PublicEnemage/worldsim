---
name: M20-G4-act1-act2-nav-link
type: implementation-intent
adr: N/A — enhancement to existing Mode 3 constraint-floor result display (ADR-021 §D-4)
issues: "DEMO-217"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-08
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m20-g4-sprint-entry.md
---

# Implementation Intent: G4 — Act 1 → Act 2 In-Viewport Navigation Link (DEMO-217)

## 1. Source Issue and Architecture Authority

**Finding:** DEMO-217 CRITICAL — Demo 8 audience simulation Step 6c (Eleni, Persona 2) and
confirmed at Demo 8 stakeholder review Q7.

**Problem:** The constraint-floor result (Act 1 — Mode 3 Active Control, scenario
"ZMB Demo 8 Act1") and the distributional comparison (Act 2 — Replay mode, scenario
"ZMB Demo 8 OptionC") live in separate scenario views. Navigation between them required
38 seconds with a rehearsed path. Cold navigation (without pre-configured scenarios) is
not achievable. The two primary findings of Demo 9 must not require a 38-second manual
scenario switch under session conditions.

**Architecture authority:** ADR-021 §D-4 governs the four-state constraint-floor search
result display (`PENDING | FOUND | NOT_FOUND | ERROR`). The FOUND state (`data-testid=
"constraint-search-found"`) is the display location for the new navigation element. No
new ADR is required — this is a UX addition to an existing result state, not an
architectural decision. The implementing agent must not alter the four-state machine or
the `constraint-search-result` / `constraint-search-pending` / `constraint-search-not-found`
/ `constraint-search-error` display contract.

**Authored by:** PM Agent  
**Date:** 2026-07-08  
**Implementing agent:** Frontend Architect Agent

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Persona 2 (Eleni Papadimitriou, Ministry of Finance analyst) — raised DEMO-217
in Step 6c and confirmed at stakeholder Q7: "Thirty-eight seconds from the constraint
result to the distributional comparison. I rehearsed this path before the session. In the
room, without preparation, this path takes longer." Eleni is the primary presenter in a
programme review session.

Secondary: Persona 1 (Lucas Ferreira, IMF Senior Economist) — the audience. If the
presenter cannot navigate fluently from the constraint result to the distributional
consequence, the argument loses analytical coherence under time pressure.

**P-2 — Entry state:**
Mode 3 Active Control is active. The constraint-floor search has completed with FOUND
result. `data-testid="constraint-search-found"` is visible in the control plane.
`data-testid="constraint-boundary-value"` shows the boundary value (e.g. "fiscal
multiplier ≥ 0.83"). Eleni is about to say "the safe boundary is 0.83 — let me show
you what that means for poverty headcount."

**P-3 — Journey step:**
Scenario Exploration / Programme Review journey. Eleni is at the moment of handoff
between Act 1 (constraint result) and Act 2 (distributional consequence) — the analytical
argument requires moving from "we found a safe boundary" to "here is what that boundary
means for the bottom quintile."

**P-4 — Time/interaction ceiling:**
The navigation from FOUND result to distributional comparison must complete in ≤ 5
seconds in a prepared session (pre-loaded scenarios). This is the ceiling that makes
the argument presentable under programme review time pressure. 38 seconds is not
acceptable; 5 seconds is.

**P-6 — Negotiating leverage delivered:**
Eleni can move from "the safe boundary is 0.83" to "this is what it means for 342,700
people in the bottom quintile" in one click, without losing the room to a navigation
pause.

**P-7 — North star capability delivered:**
A Zambian finance ministry analyst presenting to an IMF review session can, from the
constraint-floor result, navigate in one click to the distributional comparison that
shows the human cost of the constraint floor — and the argument remains uninterrupted.
The two halves of the analytical case (boundary found → distributional consequence) are
connected by a single in-viewport action.

---

## 3. Observable Application State

### 3.1 — Navigation link presence

When `data-testid="constraint-search-found"` is visible and at least one other loaded
scenario exists in the session (a scenario in Replay mode or a scenario selectable as
the comparison target), a navigation element is present within the `constraint-search-found`
container:

```
data-testid="constraint-search-found"
  ├── data-testid="constraint-boundary-value"   (existing — unchanged)
  ├── data-testid="constraint-tolerance-band"   (existing — unchanged)
  ├── data-testid="constraint-evaluations"      (existing — unchanged)
  └── data-testid="act2-nav-link"               (NEW — navigation element)
       └── text: "View distributional comparison →" (or equivalent)
```

The `act2-nav-link` element is visible without scrolling when the FOUND result is
displayed. It does not require the user to scroll down in the control plane panel to
find it.

### 3.2 — Navigation behaviour

Clicking `act2-nav-link`:
- Loads or switches to the distributional comparison scenario — either the most recently
  associated comparison scenario, a session-level linked scenario, or a scenario picker
  if no linked scenario is configured
- The implementing agent chooses the lowest-complexity mechanism that satisfies the 5-second
  ceiling in a pre-loaded session (scenarios already in the session's scenario list)
- The active scenario in the instrument cluster changes to the selected distributional
  comparison scenario
- Mode switches to Replay if the target scenario is a Replay scenario

**Design note:** The implementing agent must not require a round-trip to the server to
discover which scenario is the comparison target. If the session has loaded scenarios,
the link mechanism reads from session state. If no comparison scenario is loaded, the
link is either absent (when no other scenarios exist) or opens the scenario panel for
selection.

### 3.3 — Silent failure detection

**SF-1 (link present but requires scroll):** `act2-nav-link` exists in the DOM but is
below the visible fold of the control plane panel. Detection: assert that
`act2-nav-link` is within the visible viewport bounding box of `constraint-search-found`
without scroll.

**SF-2 (link absent when scenarios are loaded):** The session has at least one other
scenario loaded but `act2-nav-link` is not present in `constraint-search-found`.
Detection: assert `act2-nav-link` exists when `constraint-search-found` is present and
session has ≥ 2 scenarios.

**SF-3 (navigation completes but mode does not switch):** The link click loads the
target scenario but Mode 3 remains active instead of switching to Replay. Detection:
assert mode indicator shows Replay (or the target scenario's mode) after navigation.

---

## 4. Acceptance Criteria

**AC-1 (link present in FOUND state with multiple scenarios):**
When `constraint-search-found` is visible and the session has ≥ 2 loaded scenarios,
then `data-testid="act2-nav-link"` is present within `constraint-search-found`.

**AC-2 (link absent when no other scenarios):**
When `constraint-search-found` is visible and the session has exactly 1 loaded scenario
(no comparison target available), then `data-testid="act2-nav-link"` is absent from
`constraint-search-found`. (No broken link; no visible-but-non-functional navigation
element.)

**AC-3 (link visible without scroll):**
When `constraint-search-found` is visible, `act2-nav-link` is within the viewport-visible
area of the control plane column without scrolling.

**AC-4 (navigation completes — scenario switches):**
When `act2-nav-link` is clicked and a comparison scenario is available, the active
scenario in the instrument cluster changes from the Mode 3 scenario to the comparison
scenario. The transition completes within 5 seconds in a pre-loaded session.

**AC-5 (FOUND state unchanged — no regression):**
`data-testid="constraint-boundary-value"`, `data-testid="constraint-tolerance-band"`,
and the evaluations/range display are present and unchanged after the `act2-nav-link`
addition.

**AC-6 (SF-1 guard — not scroll-hidden):**
Assert that the bounding box of `act2-nav-link` does not require scroll within the
`control-plane` panel to be visible at 1440×900 viewport after FOUND result is shown.

---

## 4b. Visual Spec (before/after)

**FOUND state (before):**
```
control-plane (right column, Mode 3)
  CONSTRAINT FLOOR SEARCH
  ────────────────────────
  [Find safe boundary]

  ✓ Safe boundary found:
  fiscal multiplier ≥ 0.83    [constraint-boundary-value]
  ±0.00 precision              [constraint-tolerance-band]
  8 evaluations · [0.1, 3.0] searched
  This is the binary search precision…
```

**FOUND state (after):**
```
control-plane (right column, Mode 3)
  CONSTRAINT FLOOR SEARCH
  ────────────────────────
  [Find safe boundary]

  ✓ Safe boundary found:
  fiscal multiplier ≥ 0.83    [constraint-boundary-value]
  ±0.00 precision              [constraint-tolerance-band]
  8 evaluations · [0.1, 3.0] searched
  This is the binary search precision…

  View distributional comparison →   [act2-nav-link]   ← NEW; in-viewport
```

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for
Persona 2 to act on it in the Reactive entry state (≤ 5 seconds)?**

`[x]` No — "View distributional comparison →" is self-describing. Eleni knows she wants
to show the distributional consequence; the link says exactly that. No specialist
translation required.

**Rationale:** The link text is an action label, not a technical term. The link does not
require the user to understand the underlying scenario architecture (which scenario ID
is the comparison target). The mechanism is: one click, new scenario visible.

---

## 6. Out of Scope

- **Multiple comparison targets:** If the session has more than one potential comparison
  scenario, the implementing agent may show a picker or default to the most recently
  loaded non-Mode-3 scenario. The disambiguation mechanism is the implementing agent's
  call; it must not require > 2 user interactions.
- **Act 1 ↔ Act 2 bidirectional link:** The inverse link (from Act 2 distributional
  comparison back to Act 1 constraint result) is not required by this deliverable.
- **Persistent linked scenario configuration:** A configuration UI for specifying which
  scenario is the "comparison target" is out of scope. Session-level state is sufficient.
- **NOT_FOUND / ERROR state navigation:** The navigation link is only shown in the FOUND
  state. NOT_FOUND and ERROR states are unchanged.
- **Backend changes:** No backend changes required.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent  
**Test authorship deadline:** Before any G4 implementation PR opens on `sprint/m20-g4`  
**Test file location:** `frontend/tests/e2e/m20-g4-act-navigation-link.spec.ts`

**Required test coverage (Playwright E2E):**

- **AC-1:** Set up session with 2 pre-loaded scenarios; trigger constraint-floor search
  to FOUND; assert `act2-nav-link` present in `constraint-search-found`.
- **AC-2:** Set up session with 1 scenario only; trigger FOUND; assert `act2-nav-link`
  absent from `constraint-search-found`.
- **AC-3:** With 2 scenarios and FOUND result, assert `act2-nav-link` bounding box is
  visible (not scroll-hidden) within control-plane column at 1440×900.
- **AC-4:** With 2 scenarios and FOUND result, click `act2-nav-link`; assert active
  scenario changes (scenario name or ID visible in instrument cluster changes to the
  comparison target).
- **AC-5 (regression):** Verify `constraint-boundary-value` and `constraint-tolerance-band`
  present and unchanged after `act2-nav-link` addition.
- **AC-6 (SF-1 guard):** Same as AC-3 — explicit assertion that no scroll is needed.
  Write as a separate assertion block.

**QA Lead acknowledgment:**
`[ ]` QA Lead: Tests for AC-1 through AC-6 authored and filed before first implementation PR.

---

*Intent document version: 2026-07-08. Sprint entry: `docs/process/sprint-plans/m20-g4-sprint-entry.md`.
See `docs/process/agent-execution-lifecycle.md` for the five-step lifecycle this document gates.*
