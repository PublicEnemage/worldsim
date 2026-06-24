---
name: M16-G9-mode3-branch-comparison-values
type: implementation-intent
issues: "#846"
status: Filed — QA tests required before implementation PR opens
authored-by: PM Agent (pre-implementation spec; Frontend Architect Agent takes implementation authority at Step 3)
authored-date: 2026-06-24
implementing-agent: Frontend Architect Agent
sprint-entry: "docs/process/sprint-plans/m16-g9-sprint-entry.md — EL Approved 2026-06-24"
adr-reference: "None — within existing Mode 3 branch management architecture; no new mode-level ADR required (sprint entry §2.2)"
release-branch: release/m16
sequencing: "After G1 merges to release/m16 — DEMO-045 finding may be in the same primary viewport component tree modified by G1; G1 must land first to avoid conflicts"
---

# Implementation Intent: M16-G9 — Mode 3 Branch Comparison Values (#846)

> **G9 capacity-allowing.** Not Demo 6 critical path. If capacity is exhausted before G8 is
> scheduled, this issue carries to M17.
> DEMO-045 finding: branch comparison values were absent in Mode 3 during a live demo session.
> Implementation does not begin until: (1) G1 merges to `release/m16`; (2) this intent document
> is committed to `release/m16`; (3) QA tests are authored from this document's ACs.

---

## 1. Source Authority

**Issue:** #846 — ux: DEMO-045 — Mode 3 branch comparison values absent
**Sprint entry:** `docs/process/sprint-plans/m16-g9-sprint-entry.md` — EL Approved 2026-06-24
**ADR gate:** None — within existing Mode 3 branch management architecture
**Finding:** DEMO-045 — in a live demo session, the Mode 3 branch comparison panel rendered with
empty/absent values instead of numeric comparison values at each step. The panel was present;
the values were missing.
**Date authored:** 2026-06-24
**Authored by:** PM Agent (pre-implementation spec)
**Implementing agent:** Frontend Architect Agent

---

## 2. Persona Trace Elements Targeted

**P-1 — Personas served:**
**Persona 2 — Finance Ministry Negotiator** (Aicha Mbaye archetype, `docs/ux/personas.md §Persona 2`).
Mode 3 (Active Control) is the primary interaction mode for the G8 live demo (#843). In Mode 3,
Persona 2 applies control inputs (fiscal policy, monetary policy parameters) and creates branches
(alternative policy paths at different control input settings). The branch comparison panel is the
instrument through which Persona 2 reads the divergence between policy paths — "Branch B keeps
the composite score above the MDA floor at step 4; Branch A does not."

Without numeric comparison values, the branch comparison capability is non-functional: branches
exist but cannot be evaluated against each other. This eliminates the primary Mode 3 analytical
argument — the one Demo 6 depends on.

**P-2 — Entry state:**
**Reactive** (90-second ceiling). In Mode 3, Persona 2 applies a control input and immediately
checks the branch comparison to assess the effect. The comparison values must be present without
additional interaction after a step is advanced or a branch is created.

**P-3 — Journey reference:**
Mode 3 Active Control session (Demo 6 context, Zambia ECF + JOR two-entity scenario). After
applying a fiscal multiplier control input and advancing a step, Persona 2 reads the branch
comparison to state the argument at the negotiating table.

**P-4 — Time/interaction ceiling:**
**Zero additional interaction.** After a branch is created or a step is advanced, comparison values
must appear in the panel without an additional click, hover, or scroll. 90-second Reactive ceiling.

**P-6 — Negotiating leverage delivered (Persona 2):**
Persona 2 in Mode 3 with Branch A (IMF programme as proposed) and Branch B (Zambia ministry
proposal with fiscal_multiplier=1.30) can read from the branch comparison panel at step 4:
"Branch B shows a composite score 0.08 higher than Branch A — the modified programme improves
our aggregate position by step 4 relative to the IMF baseline."
This argument is speakable at the negotiating table and requires only reading the branch
comparison panel — no specialist translation of absent values.

**P-7 — North star capability delivered:**
A Mode 3 session with 2 branches configured shows non-null numeric comparison values in the
branch comparison panel at every step. The DEMO-045 silent absence of values is resolved. The
Zambia finance ministry analyst can state the branch divergence argument with cited numeric
values from the panel.

---

## 3. Observable Application State

*All states verifiable by an external observer using only the running application at 1280×800.
No source code reading, no CI report reference.*

### 3.1 Primary observable state

At 1280×800 in **Mode 3** with 2 or more branches configured, advanced to step 1:

`data-testid="branch-comparison-panel"` is visible in the viewport without scroll.

For each branch in the panel: `data-testid="branch-value-{branchIndex}"` (where `branchIndex`
is 0, 1, ... for each branch in creation order) contains a non-empty text string that includes
at least one numeric digit (parseable as a float). The value is not "—", not an empty string,
not "loading...", not "N/A" — it is a numeric comparison value for that branch at the current
step.

### 3.2 Secondary observable states

**State A — Values update on step advance:**
At 1280×800 in Mode 3 with 2 branches at step 1:
After advancing to step 2, at least one of `data-testid="branch-value-0"` or
`data-testid="branch-value-1"` changes its text content from the step 1 value. Both values
remain non-empty numeric strings at step 2. Values are not cached from step 0 or step 1.

**State B — Mode 1 non-regression (panel absent):**
At 1280×800 in Mode 1 with the ZMB ECF scenario loaded:
`data-testid="branch-comparison-panel"` is absent from the DOM. Branch comparison is a Mode 3
capability only.

**State C — Mode 2 non-regression (panel absent):**
At 1280×800 in Mode 2 with the ZMB ECF scenario loaded:
`data-testid="branch-comparison-panel"` is absent from the DOM.

### 3.3 Silent failure detection

**Silent failure 1 — Panel present, values empty (DEMO-045 condition):**
The panel renders but all value cells contain empty strings, "—", or null renderings. This is the
exact DEMO-045 failure mode. Detection: AC-1 explicitly asserts that `branch-value-{branchIndex}`
text content contains at least one digit — an empty string or "—" fails the assertion.

**Silent failure 2 — Panel requires a second interaction to reveal values:**
The panel is present but values are in a collapsed/hover state. Detection: AC-1 asserts values
are visible without any interaction after advancing to step 1 — no click, no hover required.

**Silent failure 3 — Values cached from step 0 and do not update:**
Values are present but static — the same across all steps. Detection: AC-2 asserts that at least
one branch value cell changes text between step 1 and step 2.

---

## 4. Acceptance Criteria

*Each criterion verifiable by an external observer. Test file:
`frontend/tests/e2e/m16-g9-mode3-branch-comparison.spec.ts`*

**AC-1 (primary — values present in Mode 3 at step 1):**
At 1280×800 in **Mode 3**, with 2 branches configured and the scenario advanced to step 1:
`data-testid="branch-comparison-panel"` is visible (non-zero bounding box, not `display:none`).
`data-testid="branch-value-0"` and `data-testid="branch-value-1"` both exist in the DOM and each
contains text matching `/\d/` (at least one digit). Neither contains "—", "", "N/A", or
"loading".
*(Regression of DEMO-045: previously both cells contained empty/null values.)*

**AC-2 (values update on step advance):**
Continuing from AC-1 state (step 1): after advancing to step 2, the text content of at least one
of `data-testid="branch-value-0"` or `data-testid="branch-value-1"` differs from its step-1
value. Both remain non-empty numeric strings at step 2.

**AC-3 (Mode 1 non-regression — panel absent):**
At 1280×800 in **Mode 1** with the ZMB ECF scenario loaded:
`data-testid="branch-comparison-panel"` is absent from the DOM. The primary viewport (Zone 1A,
Zone 1B, Zone 1D) renders without any branch comparison panel element present.

**AC-4 (Mode 2 non-regression — panel absent):**
At 1280×800 in **Mode 2** with the ZMB ECF scenario loaded:
`data-testid="branch-comparison-panel"` is absent from the DOM. Mode 2 instrument cluster
renders without any branch comparison panel element present.

**AC-5 (panel shows exactly the configured branch count):**
At 1280×800 in Mode 3 with exactly 2 branches configured:
`data-testid="branch-value-0"` and `data-testid="branch-value-1"` are present. No additional
`data-testid="branch-value-2"` or higher index exists in the DOM (no phantom branches rendered).

---

## 4b. Visual Spec (before/after)

### AC-1 — Mode 3 branch comparison panel values

**AC-1 (before — DEMO-045 failure state):**
```
Viewport: 1280×800 | Mode 3 | data-testid="branch-comparison-panel"

Branch comparison panel at step 1, 2 branches configured:
┌─────────────────────────────────────────────────────────┐
│ BRANCH COMPARISON                                        │
│ ─────────────────────────────────────────────────────── │
│ Branch A:  [   ]   ← data-testid="branch-value-0"      │
│                        ^^^^ DEMO-045: empty / absent    │
│ Branch B:  [   ]   ← data-testid="branch-value-1"      │
│                        ^^^^ DEMO-045: empty / absent    │
└─────────────────────────────────────────────────────────┘
Both value cells empty. Persona 2 cannot read branch comparison.
```

**AC-1 (after — DEMO-045 resolved):**
```
Viewport: 1280×800 | Mode 3 | data-testid="branch-comparison-panel"

Branch comparison panel at step 1, 2 branches configured:
┌─────────────────────────────────────────────────────────┐
│ BRANCH COMPARISON                                        │
│ ─────────────────────────────────────────────────────── │
│ Branch A:  [ 0.47 ]  ← data-testid="branch-value-0"   │
│                           ✓ numeric, non-empty          │
│ Branch B:  [ 0.52 ]  ← data-testid="branch-value-1"   │
│                           ✓ numeric, non-empty          │
└─────────────────────────────────────────────────────────┘
Both value cells contain non-empty numeric text.
Persona 2 can read: "Branch B (0.52) is higher than Branch A (0.47)."
Values update when advancing steps (AC-2).
```

### AC-3/AC-4 — Mode 1 and Mode 2 non-regression

**AC-3/AC-4 (Mode 1 and Mode 2 — panel absent):**
```
Viewport: 1280×800 | Mode 1 or Mode 2 | primary viewport

Primary viewport instruments visible (Zone 1A, Zone 1B, Zone 1D).
data-testid="branch-comparison-panel" is NOT present in the DOM.
No ghost element, no empty panel, no collapsed panel — element is absent entirely.
```

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` **No** — the branch comparison panel shows numeric values that a finance analyst reads
and compares directly. "Branch B: 0.52" vs. "Branch A: 0.47" — the higher composite score
(further from the MDA floor) is interpretable without specialist translation by Persona 2, who
has domain familiarity with composite indices from Mode 3 preparatory sessions.

This intent resolves the DEMO-045 absent-values finding only. No new interpretive complexity is
introduced — the fix restores values that should always have been present.

Named asymmetry gap (accepted): a well-resourced analytical team can derive full per-framework
branch divergence for multiple branches simultaneously. WorldSim provides the aggregate composite
branch comparison value in the panel. Per-framework breakdown is available via Zone 1D (one zone
navigation). This residual gap is accepted.

---

## 6. Out of Scope

| Scope item | Rationale for exclusion |
|---|---|
| Branch management UI (renaming, deleting, reordering branches) | #846 is scoped to the absent comparison value display only. Branch management architecture is separate. |
| Per-framework comparison breakdown in the branch panel | The panel shows aggregate composite values. Per-framework breakdown is Zone 1D scope. |
| Branch comparison panel layout redesign | This intent fixes the absent values within the existing panel layout. Layout redesign is separate. |
| Branch comparison for N > 2 branches | Scope is the 2-branch case (DEMO-045 context). N > 2 branches is a separate design. |
| G1 component files (Zone 1A Phase 4, Zone 1D delta annotations) | #846 modifies the branch comparison panel component only. Must not touch G1-delivered component files. |

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any implementation PR is opened against `release/m16` for #846
**Test file:** `frontend/tests/e2e/m16-g9-mode3-branch-comparison.spec.ts`
**Acceptance criteria covered:** AC-1 through AC-5

**Sequencing note:** Implementation may not begin until G1 merges to `release/m16`.
Tests must be authored from this document before implementation code is written.

**Soft-skip guard (NM-056 follow-up):** No `test.skip()` or conditional skip patterns.

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-5 authored and filed. 2026-06-24

---

*Intent document authority: `docs/process/intent-template.md` (version 2026-06-17).
Sprint entry: `docs/process/sprint-plans/m16-g9-sprint-entry.md` (EL Approved 2026-06-24).
Finding authority: DEMO-045 (Mode 3 branch comparison values absent during live demo session).
Implementing agent: Frontend Architect Agent.
G9 capacity gate: Carry to M17 if capacity is exhausted before G8 is scheduled.*
