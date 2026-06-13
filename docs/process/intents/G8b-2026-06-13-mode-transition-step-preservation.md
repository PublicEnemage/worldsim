---
name: G8b-mode-transition-step-preservation
type: implementation-intent
adr: N/A — design on record in PR #390 Gap 5
issue: "#393"
status: Filed
authored-by: Frontend Architect Agent
authored-date: 2026-06-13
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m13-g8-sprint-entry.md
---

# Implementation Intent: G8b — Mode 1→2 Step Position Preservation (#393)

## 1. Source ADR

**ADR:** N/A — no new ADR required. Mode transition design is on record in
`docs/ux/design-thinking/worldsim-ux-architecture-first-principles-depth.md §Gap 5`.
**Status at time of authorship:** Gap 5 design accepted (PR #390, merged). G8 sprint entry EL-approved 2026-06-13.
**Authored by:** Frontend Architect Agent
**Date:** 2026-06-13
**Implementing agent:** Frontend Architect Agent

**Design authority:**
- `docs/ux/design-thinking/worldsim-ux-architecture-first-principles-depth.md §Gap 5 — Mode Transition Design`
- Issue #393 acceptance criteria
- G8 sprint entry §2.3 observable application state requirements

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou archetype).
Secondary: Persona 1 — Programme Analyst (Lucas Ferreira archetype).
Both are named in the Sri Lanka 2022 marquee case (`docs/ux/personas.md §Secondary Case C`).

**P-2 — Entry state:**
Preparatory entry state — the analyst is building a multi-mode case within a single session.
The Sri Lanka marquee case pattern: analyst has replayed the external shock sequence in Mode 1
(identifying the crisis entry point at step N where cumulative shocks cross the reserves MDA
floor), and needs to transition to Mode 2 to test alternative policy responses *from that exact
step* without re-loading the entity configuration or losing the step context.

**P-3 — Journey reference:**
Within-session cross-mode transition — between Journey A (Preparation) and Journey B (Active
Negotiation). The Sri Lanka case requires a complete Mode 1 → Mode 2 transition inside a single
Journey A preparation session. The mode transition step is a prerequisite for Journey B Step 3
(cite the finding) when the finding originates from a Mode 2 simulation branched from a Mode 1
crisis entry point.

**P-4 — Time/interaction ceiling:**
The Mode 1 → Mode 2 transition (tap mode selector → read modal → confirm → instruments update)
must complete in under 30 seconds with no manual context reconstruction. "Context reconstruction"
means: the analyst must not re-enter entity identifiers, re-select a step, or re-configure the
scenario after the transition. If any re-entry is required, the time ceiling is broken regardless
of raw UI latency.

**P-6 — Negotiating leverage delivered:**
N/A — this implementation delivers workflow continuity, not a new analytical output. The
negotiating leverage is downstream: a Mode 2 simulation branched from the Mode 1 crisis step
produces the "what if we had acted at step N?" counterfactual that Mode 1 alone cannot produce.
That counterfactual is the argument. This implementation removes the barrier to producing it
in a single session.

**P-7 — North star capability delivered:**
The Colombo finance ministry analyst can replay the five-shock convergence in Mode 1 to identify
step 3 as the crisis entry point (reserves MDA breach), then transition to Mode 2 from that
exact step to simulate alternative policy responses — without restarting, without re-entering
the Sri Lanka entity configuration, and without losing the step-3 context that defines the
counterfactual. The Mode 2 simulation begins at step 3, not at step 0.

---

## 3. Observable Application State

### 3.1 Primary observable state

With the Hormuz fixture (JOR+EGY scenario, any scenario reaching ≥ step 3) loaded in Mode 1
and advanced to step 3 in the live application at 1440×900: when the user taps the "Simulation"
mode label in the mode selector header and confirms the transition modal,
`data-testid="mode-indicator"` shows `data-mode="MODE_2"` (rendering "Simulation") AND
`data-testid="current-step-display"` shows the value `3` — not `0` and not `1`.

The `current-step-display` element is a new required addition to the ScenarioControls or
instrument cluster header; it must carry `data-testid="current-step-display"` and render the
current step index as its text content. This makes the step position directly observable by
an external test without reading store state.

### 3.2 Secondary observable states

**Secondary state A — entity configuration carry-forward:**
After the Mode 1→2 transition described in 3.1 (same session, same scenario), the scenario
identity header (`data-testid="scenario-identity-header"`) still displays the JOR and EGY
entity identifiers. No re-entry prompt for entity configuration appears. The entity set visible
before and after the transition is identical.

**Secondary state B — confirmation modal content specificity:**
When the user taps the "Simulation" mode label while in Mode 1, a modal appears
(`data-testid="mode-transition-modal"`) whose text content contains the literal substring
"step position" AND "entity configuration" as named preserved elements. The modal is not a
generic unsaved-changes warning — it must name the specific items that are preserved and the
specific item that changes.

**Secondary state C — cancel leaves Mode 1 unchanged:**
When the modal is shown and the user taps `data-testid="mode-transition-modal-cancel"`,
`data-testid="mode-indicator"` still shows `data-mode="MODE_1"` AND
`data-testid="current-step-display"` still shows the step value from before the modal appeared.

### 3.3 Silent failure detection

**SF-1 (step reset on transition):** If the implementation calls `setScenario` (which resets
`current_step: 0`) instead of `useScenarioStepStore.setState({ mode: "MODE_2" })` during the
transition, the step resets silently to 0. The mode indicator shows "Simulation" correctly, but
the instruments display Step 0 data. Detection: immediately after transition confirmation,
`data-testid="current-step-display"` shows `0` instead of the pre-transition step value N.
This is the primary silent failure — the mode change appears successful while the mission
capability (branching from crisis step) is broken.

**SF-2 (modal skipped):** If the mode transition fires without showing the modal (e.g., a click
handler directly sets mode without the confirmation step), the user never receives explicit
disclosure that the step is preserved. The instruments may be correct, but the UX contract
(Gap 5: "single modal confirmation") is violated. Detection: in a Playwright test, tap the
"Simulation" label and assert `data-testid="mode-transition-modal"` is visible before any
assertion about the mode indicator changing.

**SF-3 (entity config lost):** If the mode transition triggers a scenario reload that clears
the entity configuration, the entity identifiers disappear from the scenario identity header
and an entity selection prompt appears. Detection: after transition, assert
`data-testid="scenario-identity-header"` contains the original entity ISO codes without any
intervening re-entry prompt.

---

## 4. Acceptance Criteria

**AC-1 (primary — step preservation):**
With the Hormuz fixture (or equivalent fixture with ≥3 steps) loaded in Mode 1, when the
fixture is advanced to step 3, the mode selector "Simulation" label is tapped, and the
confirmation modal is accepted via `data-testid="mode-transition-modal-confirm"`, then
`data-testid="mode-indicator"` has `data-mode="MODE_2"` AND `data-testid="current-step-display"`
contains the text `3`.

**AC-2 (entity carry-forward):**
After the Mode 1→2 transition in AC-1, `data-testid="scenario-identity-header"` contains
the text "JOR" and "EGY" (or the relevant fixture entity identifiers) without any entity
selection modal or configuration prompt appearing between transition confirmation and the
assertion.

**AC-3 (modal content — named preserved items):**
With any fixture in Mode 1 with current_step ≥ 1, when the "Simulation" mode label in the
mode selector is tapped, `data-testid="mode-transition-modal"` is visible and its text content
contains both "step position" and "entity configuration".

**AC-4 (modal cancel — state unchanged):**
With the Hormuz fixture in Mode 1 at step 3, when the mode transition modal is shown and
`data-testid="mode-transition-modal-cancel"` is clicked, then `data-testid="mode-indicator"`
has `data-mode="MODE_1"` AND `data-testid="current-step-display"` shows `3`.

**AC-5 (SF-1 — step reset detection):**
In a Playwright test, immediately after confirming the Mode 1→2 transition modal with the
fixture at step 3, assert `data-testid="current-step-display"` does NOT contain `0`. This
explicit negative assertion catches the silent-failure scenario where `setScenario` (which
resets step) is called instead of the mode-only state update path.

**AC-6 (SF-2 — modal always shown before mode change):**
With any fixture in Mode 1, when the "Simulation" mode label is tapped, assert
`data-testid="mode-transition-modal"` is visible BEFORE `data-testid="mode-indicator"`
changes from `data-mode="MODE_1"`. The modal must precede the mode change, not follow it.

**AC-7 (current-step-display testid present):**
In any loaded scenario state, `data-testid="current-step-display"` is present in the DOM and
contains the current step index as its text content (matching `useScenarioStepStore`'s
`current_step`). This testid is a new required addition to the implementation and must be
present for all AC assertions above to be testable.

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` No — the observable state is interpretable by Persona 2 without an analyst translating it.

Rationale: The confirmation modal and mode selector are direct UI affordances. The modal names
what is preserved ("step position and entity configuration") and what changes ("replay history
is not editable in simulation mode") in plain language. No analyst is required to interpret the
step counter value or the mode label. The Kryptonite test: the ministry-side analyst reads the
modal, confirms, and proceeds — the creditor-side workflow is identical. No mediation asymmetry.

---

## 6. Out of Scope

The following are explicitly outside this implementation:

**Mode 2 → Mode 3 transition:** Gap 5 specifies this transition as well, but #393 is scoped to
Mode 1 → Mode 2 only (Sri Lanka marquee case). Mode 2 → Mode 3 is handled by the existing
`mode3Active` toggle mechanism and is not changed by this implementation.

**Mode 3 → Mode 1 transition:** Out of scope for #393. Gap 5 design applies; follow-on issue
required if this transition currently loses applied control inputs without logging them.

**New backend endpoint or scenario branching:** This implementation is frontend-only. The step
position preservation operates via `useScenarioStepStore.setState({ mode: "MODE_2" })` — it
does not create a new scenario in the database. A Mode 2 simulation from step N reuses the
existing scenario_id; the trajectory from step 0 to N is already computed. No new API call is
required for the mode transition itself.

**Mode selector for scenarios in initial state (step 0):** If `current_step === 0` (scenario
not yet advanced), the Mode 1→2 transition may omit the modal (no unsaved state) and transition
directly. This edge case is not the Sri Lanka marquee case and may be handled as a simple mode
toggle. The modal and step preservation requirements apply when `current_step > 0`.

**Fiscal multiplier integration:** The existing `fiscalMultiplier` prop–driven mode derivation
in `ScenarioInstrumentCluster.tsx` must remain unchanged. The new mode selector triggers mode
transitions through an independent path. Regression requirement: after this implementation,
the fiscal multiplier changing from 1.0 to 1.30 must still change the mode to MODE_2 exactly
as before.

---

## 7. Implementation Specification

### 7.1 New `setMode` store action

Add to `useScenarioStepStore` (`frontend/src/store/scenarioStepStore.ts`):

```typescript
setMode: (mode: "MODE_1" | "MODE_2" | "MODE_3") => void;
```

Implementation: `setMode: (mode) => set({ mode })` — sets mode only; does not reset
`current_step`, `trajectory`, `scenario_id`, or any other state. This is the only
action that may be used for explicit mode transitions. The existing `setScenario` call path
(which resets `current_step: 0`) must not be invoked during a mode-selector-driven transition.

### 7.2 ModeIndicator → ModeSelector

Transform `frontend/src/components/ModeIndicator.tsx` into an interactive mode selector:
- Three clickable labels: "Replay" | "Simulation" | "Active Control"
- `data-testid="mode-selector-label-MODE_1"`, `data-testid="mode-selector-label-MODE_2"`,
  `data-testid="mode-selector-label-MODE_3"` on each label
- Active mode label has a distinct visual treatment (filled background, not just a border)
- Inactive mode labels are tappable. Active mode label tap is a no-op.
- When an inactive label is tapped: check if `current_step > 0`; if yes, show confirmation
  modal. If no (step 0), call `setMode` directly (no modal required — no state would be lost).
- `data-testid="mode-indicator"` remains on the outer container for backward compatibility
  with existing tests. `data-mode={mode}` attribute also retained.

### 7.3 Mode transition modal component

New component: `ModeTransitionModal` in `frontend/src/components/ModeTransitionModal.tsx`.

Props:
- `targetMode: "MODE_1" | "MODE_2" | "MODE_3"`
- `currentStep: number`
- `onConfirm: () => void`
- `onCancel: () => void`

`data-testid="mode-transition-modal"` on the modal container.
`data-testid="mode-transition-modal-confirm"` on the confirm button.
`data-testid="mode-transition-modal-cancel"` on the cancel button.

Modal body text (Mode 1 → Mode 2): single confirmation message that contains the exact
phrases "step position" and "entity configuration" as named preserved items, and states that
replay history (event annotation layer) will not be active in simulation mode.

Example (implementation may vary wording but must contain named items):
> "Switching to Simulation mode. Your current step position (step {currentStep}) and entity
> configuration are preserved. Replay event annotations will not be shown in Simulation mode."

Confirm button label: "Switch to Simulation"
Cancel button label: "Stay in Replay"

The modal is not full-screen. It is a non-blocking dialog positioned near the mode selector.
No backdrop or page scroll lock — consistent with Gap 5 "single non-modal confirmation" pattern.

### 7.4 `current-step-display` testid

Add `data-testid="current-step-display"` to the step counter display in
`frontend/src/components/ScenarioControls.tsx`:

```tsx
<span data-testid="current-step-display" style={{ fontWeight: 600 }}>
  Step {currentStep} / {totalSteps}
  {isComplete && " — Complete"}
</span>
```

The value rendered is the `currentStep` local state, which is kept in sync with
`useScenarioStepStore.current_step` via the `ScenarioInstrumentCluster` sync `useEffect`
(line 260–265 in current file). After the mode transition, `current_step` in the store is
unchanged; `ScenarioControls` reflects it on next render.

### 7.5 Regression guard: fiscal multiplier mode derivation unchanged

The existing mode derivation in `ScenarioInstrumentCluster.tsx` (lines 244–255):
```typescript
const mode = mode3Active ? "MODE_3"
  : fiscalMultiplier != null && fiscalMultiplier !== 1.0 ? "MODE_2"
  : "MODE_1";
// ...
useScenarioStepStore.setState({ mode });
```
must not be altered. The ModeSelector's `setMode` calls must not conflict with this path.
If the user is in Mode 2 via `setMode` AND the fiscal multiplier is also ≠ 1.0, the
derived mode from the `useEffect` takes precedence (because it fires on the same render
cycle as fiscal multiplier changes). This is acceptable: fiscal multiplier control is a
stronger signal than the mode selector for Mode 2 state.

---

## 8. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any implementation PR is opened
**Test file location:** `frontend/tests/e2e/mode-transition.spec.ts` (Playwright E2E)
**Unit test location:** `frontend/src/components/__tests__/mode-selector.test.ts` (RTL unit)
**Relevant acceptance criteria:** AC-1 through AC-7 (Section 4 above)

**Required test coverage:**

- **E2E (Playwright):** Advance Hormuz fixture to step 3 in Mode 1; tap "Simulation" mode
  selector label; assert modal visible with "step position" and "entity configuration" text;
  confirm; assert `mode-indicator` `data-mode="MODE_2"`; assert `current-step-display` shows `3`.
- **E2E (Playwright):** Same fixture at step 3; show modal; tap cancel; assert `mode-indicator`
  `data-mode="MODE_1"`; assert `current-step-display` shows `3`.
- **E2E (Playwright):** After Mode 1→2 transition, assert `scenario-identity-header` still
  contains entity identifiers (JOR + EGY) without re-entry prompt.
- **E2E (Playwright):** Tap "Simulation" label; assert modal is visible BEFORE `mode-indicator`
  attribute changes. (SF-2 guard)
- **E2E (Playwright):** After transition confirm, assert `current-step-display` does NOT show `0`.
  (SF-1 guard — explicit negative assertion)
- **Unit (RTL):** `getModeLabel` still returns correct values for all three modes.
- **Unit (RTL):** `ModeSelector` with `current_step=0` — tapping inactive label calls `setMode`
  directly without showing modal.
- **Unit (RTL):** `ModeSelector` with `current_step=3` — tapping inactive label shows
  `ModeTransitionModal` before mode changes.

**QA Lead acknowledgment:**
`[ ]` QA Lead: Tests for AC-1 through AC-7 authored and filed. [Date]

---

*Intent document version: 2026-06-13. Design authority: PR #390 Gap 5. G8 sprint entry EL-approved
2026-06-13. No ADR required — implementation satisfies a specified UX design, not a new
architectural decision. Implementing agent: Frontend Architect Agent. Kryptonite constraint:
PASS — modal and mode selector interpretable without specialist mediation. Sri Lanka 2022 marquee
case BPO Validate criterion: Mode 1 replay at step N → Mode 2 simulation in single session
without manual context reconstruction. See CLAUDE.md §Agent Execution Lifecycle for full
five-step lifecycle this document gates.*
