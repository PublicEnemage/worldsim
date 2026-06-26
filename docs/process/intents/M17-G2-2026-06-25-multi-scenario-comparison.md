---
name: M17-G2-multi-scenario-comparison-phase3
type: implementation-intent
issue: "#394"
status: Filed — Phase 3 implementation intent; authored from Phase 1/2 design artifacts
authored-by: PM Agent
authored-date: 2026-06-25
phase: Phase 3 — Implementation
design-artifacts:
  - "docs/ux/design-thinking/multi-scenario-comparison/ux-journeys-n3.md (Artifact 1)"
  - "docs/ux/design-thinking/multi-scenario-comparison/persona-mvs-n3.md (Artifact 2)"
  - "docs/architecture/reviews/ARCH-REVIEW-007-m17-n3-assessment.md (Artifact 3)"
implementing-agents:
  - Frontend Agent (TrajectoryView.tsx — Zone 1A + Zone 1B + Zone 1D)
  - QA Lead Agent (frontend/tests/e2e/m17-g2-multi-scenario-comparison.spec.ts)
sprint-entry: "docs/process/sprint-plans/m17-g2-sprint-entry.md"
bpo-acceptance: "#394#issuecomment-4803977557 — 2026-06-25"
architect-determination: "#394#issuecomment-4804024195 — option (b); no new ADR"
release-branch: release/m17
hard-gate: "#1249 (Zone 1A curve identifiability) must be merged before implementation PR opens"
---

# Implementation Intent: M17-G2 Phase 3 — Multi-Scenario Comparison (N>2)

> **Derived from Phase 1/2 design artifacts.** This document specifies what the
> implementing agent builds in Phase 3 and what the QA Lead tests. The design
> decisions (triple-channel differentiation, per-scenario Zone 1B, per-scenario
> PSP) are settled in Artifacts 1–3 — this document records them as implementation
> obligations and derives testable acceptance criteria from them.
>
> **Hard gate:** This Phase 3 implementation PR must not open until #1249
> (Zone 1A curve identifiability fix, DEMO6-014) is merged to `release/m17`.
> The N=3 differentiation scheme builds on the N=2 terminal label + line-style
> base from #1249.
>
> **ADR gate:** CLEAR — Architect determination option (b); architecture review
> note on #394 is sufficient. No new ADR required before this PR opens.

---

## 1. Source

**Issue:** #394 — feat: multi-scenario comparison (>2 scenarios)

**Phase 3 implementing from:**
- BPO ACCEPT 2026-06-25 (#394#issuecomment-4803977557)
- Architect Phase 2 assessment 2026-06-25 (#394#issuecomment-4804024195)
- Sprint entry EL approval: pending §2.3 + §2.4 (this document + QA test)

**Authored by:** PM Agent
**Date:** 2026-06-25

---

## 2. Persona Trace

**Primary persona — Aicha Mbaye (Persona 5 — Finance Minister)**

- **Entry state:** Reactive — at the negotiating table; 90-second reading ceiling
- **Question to answer:** Which restructuring option avoids Q1 poverty headcount CRITICAL crossing?
- **Answer location:** Zone 1A terminal label "C" at 0.72 (above MDA floor 0.60) + Zone 1B "Option C: [no crossings through step 8]"
- **North star test (Artifact 2 §AC-8):** Aicha states "Option C — the Homegrown Programme — does not cross the poverty threshold. The other two options both breach it in the first year. Our position at the table is Option C." — from primary viewport observation alone, in under 90 seconds.

**Secondary persona — Lucas Ferreira (Persona 1 — IMF Programme Analyst)**

- Zone 1A three-curve display with per-step Q1 poverty headcount divergence visible
- Lucas can cite: "At step 4, Option C's Q1 poverty headcount trajectory is 0.14 units higher than Option A"

**Tertiary persona — Andreas Petrakis (Persona 3 — Political Advisor)**

- Zone 1D per-scenario PSP: Option A: 58%, Option B: 67%, Option C: 74% — simultaneously visible
- Andreas states: "Option A has the lowest programme survival probability at 58%"

---

## 3. What the Implementing Agent Builds

Three changes to `frontend/src/components/TrajectoryView.tsx` (component-boundary only;
no backend change in Phase 3 — see Architect assessment §Q2):

### 3.1 — `SCENARIO_COMPARISON_PALETTE` constant

Add a constant for N=3 (scalable to N=5) scenario slots:

```typescript
const SCENARIO_COMPARISON_PALETTE = [
  { color: '#2563EB', strokeDasharray: 'none', label: 'A' },   // Steel Blue, solid
  { color: '#D97706', strokeDasharray: '8 2',  label: 'B' },   // Amber Orange, dashed
  { color: '#16A34A', strokeDasharray: '2 4',  label: 'C' },   // Forest Green, dotted
  { color: '#7C3AED', strokeDasharray: '12 4', label: 'D' },   // Purple, long-dash (N=5)
  { color: '#E11D48', strokeDasharray: '2 2 8 2', label: 'E' },// Rose, dash-dot (N=5)
] as const;
```

### 3.2 — Prop extension: `comparisonScenarios?: ScenarioComparisonConfig[]`

Replace `comparisonMode: boolean` with `comparisonScenarios?: ScenarioComparisonConfig[]`.
A non-empty array activates comparison rendering. Each config carries:
- `scenarioId: string` — matched to trajectory data key
- `label: string` — display label ("A", "B", "C")
- `paletteIndex: number` — index into `SCENARIO_COMPARISON_PALETTE`

Backwards compatibility: the current call site using `comparisonMode={true}` becomes
`comparisonScenarios={[{scenarioId: compareScenarioId, label: 'B', paletteIndex: 1}]}`.
The old `comparisonMode` prop is removed — there is one internal call site.

### 3.3 — Zone 1B per-scenario threshold crossings

When `comparisonScenarios` is non-empty, Zone 1B renders per-scenario grouped rows
instead of a flat union list:

```
▶ Option A  [■ solid blue]
  CRITICAL  Q1 Poverty headcount — crossed step 2
  WARNING   Health system capacity — crossed step 3

▶ Option B  [▪ dashed orange]
  CRITICAL  Q1 Poverty headcount — crossed step 3

▶ Option C  [● dotted green]
  [no crossings through step 8]
```

Data source: N parallel trajectory fetches (one per active scenario), each using the
existing `threshold_crossings` field. Client-side composition — no new endpoint.
The MDA alert panel `minHeight: 80px` guarantee is not violated — per-scenario rows
are in a bounded `overflow-y: auto` container below the alert panel.

### 3.4 — Zone 1D per-scenario PSP

When `comparisonScenarios` is non-empty, the Zone 1D PSP row expands to one line per
scenario from `political_economy.indicators.programme_survival_probability` in each
trajectory response. All three values are simultaneously visible without interaction.

---

## 4. Observable Application State

> *Each state is verifiable by QA without reading implementation source code.*

**S1 — N=3 Zone 1A render**
At step 4 with three scenarios active, the primary viewport shows three SVG path
elements in Zone 1A: one solid blue (#2563EB), one dashed orange (#D97706), one
dotted green (#16A34A). Each has a terminal endpoint label ("A", "B", "C") adjacent
to the rightmost data point. The MDA floor horizontal dashed-gray line is present
(from #1249, preserved).

**S2 — Zone 1B per-scenario grouping**
Zone 1B shows three scenario header rows (Option A, Option B, Option C). Under
Option A: two crossing rows (CRITICAL Q1 Poverty headcount at step 2; WARNING
Health system capacity at step 3). Under Option B: two crossing rows. Under
Option C: "[no crossings through step 8]" — a distinct element, not a blank.

**S3 — Zone 1D PSP simultaneity**
Zone 1D shows three PSP value rows: "Option A — 58%", "Option B — 67%",
"Option C — 74%". All three are visible without interaction.

**S4 — MDA alert panel integrity**
The Zone 1B MDA alert panel retains its `minHeight: 80px` allocation when per-scenario
crossing rows are populated. Per-scenario rows scroll within a bounded container
rather than compressing the alert panel.

**S5 — Zone 2 "Add third scenario" entry point**
From N=2 COMPARE_VIEW, a button "Add third scenario" is visible in Zone 2.
Clicking it displays an inline list of available scenarios for the same entity.
After selection, Zone 1A, Zone 1B, and Zone 1D update to N=3 state.

---

## 5. Acceptance Criteria

> *All ACs are assertable by the QA test file without reading component source.
> No soft-skip patterns permitted (NM-056 guard). All assertions are hard-fail.*

### AC-S1 — Scenario setup (Zone 2 → N=3 transition)

Three scenarios can be placed in comparison mode for the same entity (ZMB) via:
- API fixture: pre-configured three-scenario payload injected into compare store, OR
- UI journey: "Add third scenario" button in Zone 2 selects a third scenario

After N=3 is active:
- `[data-testid="zone1a-curve-scenario-option-a"]` exists and is visible
- `[data-testid="zone1a-curve-scenario-option-b"]` exists and is visible
- `[data-testid="zone1a-curve-scenario-option-c"]` exists and is visible
- `[data-testid="zone1b-scenario-header-option-a"]` exists and is visible
- `[data-testid="zone1d-psp-row-scenario-option-a"]` exists and is visible

### AC-A1 — Zone 1A N=3 differentiability

At N=3 at 1280×800, each scenario curve is identifiable:
- `[data-testid="zone1a-terminal-label-scenario-option-a"]` contains text "A"
- `[data-testid="zone1a-terminal-label-scenario-option-b"]` contains text "B"
- `[data-testid="zone1a-terminal-label-scenario-option-c"]` contains text "C"
- `[data-testid="zone1a-mda-floor-line"]` is visible (regression guard from #1249)
- All three curve elements are simultaneously visible (not hidden by overflow)

### AC-B1 — Zone 1B per-scenario rows (not union)

- `[data-testid="zone1b-scenario-header-option-a"]` is visible
- `[data-testid="zone1b-scenario-header-option-b"]` is visible
- `[data-testid="zone1b-scenario-header-option-c"]` is visible
- `[data-testid="zone1b-threshold-row-scenario-option-a"]` contains text "CRITICAL"
- `[data-testid="zone1b-no-crossings-option-c"]` is visible and contains
  text matching /no crossings/i
- MDA alert panel height ≥ 80px (CSS computed height assertion)

### AC-D1 — Zone 1D per-scenario PSP simultaneously visible

- `[data-testid="zone1d-psp-row-scenario-option-a"]` is visible
- `[data-testid="zone1d-psp-row-scenario-option-b"]` is visible
- `[data-testid="zone1d-psp-row-scenario-option-c"]` is visible
- `[data-testid="zone1d-psp-value-option-c"]` contains text matching /74|0\.74/
- All three PSP rows are visible without any click or hover interaction

### AC-P5 — Persona 5 (Aicha) — 90-second legibility gate

At step 4 of the ZMB N=3 comparison with Q1 poverty headcount mock data:
- Zone 1A terminal label "C" is visible (Option C curve identified without hover)
- Zone 1B "Option C" header is visible with `[data-testid="zone1b-no-crossings-option-c"]`
  containing text matching /no crossings/i
- Zone 1B Option A shows CRITICAL crossing text (`zone1b-threshold-row-scenario-option-a`
  contains "CRITICAL")
- No drawer interaction is required to confirm any of the above elements
- Confirmed readable in a 1280×800 viewport: no element is clipped or overflow-hidden

### AC-P1 — Persona 1 (Lucas) — worst Q1 trajectory identification

- The Q1 composite score for Option A at step 4 is lower than Option C at step 4
  (asserted via Zone 1A y-position or aria-label on the terminal endpoint label,
  or via mocked data values visible in Zone 1D current position table)
- `[data-testid="zone1a-curve-scenario-option-a"]` and
  `[data-testid="zone1a-curve-scenario-option-c"]` are both visible and carry
  distinct stroke color/style attributes

### AC-P3 — Persona 3 (Andreas) — per-scenario PSP readable without switching views

- Three PSP value elements visible simultaneously (AC-D1 assertion scope)
- `[data-testid="zone1d-psp-value-option-c"]` value ≥ `[data-testid="zone1d-psp-value-option-a"]`
  (Option C PSP dominates — mocked to 74% vs 58%)
- No view-switch or focus-change event required between reading PSP values

---

## 6. Kryptonite Constraint Check

**Applies to Aicha (Persona 5) — Reactive entry state, 90-second ceiling.**

Prohibited interactions (kryptonite constraint):
- Opening a drawer to see Zone 1B threshold crossings — **PASS:** Zone 1B per-scenario rows are on the primary surface
- Hovering Zone 1A curves to read scenario labels — **PASS:** terminal endpoint labels ("A", "B", "C") are always visible
- Navigating between scenario views to compare PSP — **PASS:** three PSP values shown simultaneously in Zone 1D

**Kryptonite assessment from Artifact 2:** PASS — option (a) — design meets ceiling.

---

## 7. Out of Scope for Phase 3

- **N=4, N=5 scenario support:** SCENARIO_COMPARISON_PALETTE includes palette slots for
  D and E, but Phase 3 tests and UI only assert N=3. N=5 is M18 scope.
- **Scenario setup UI implementation:** Phase 3 may deliver the "Add third scenario" button
  via a pre-configured fixture for Demo 7. Full scenario setup journey (Zone 2 UI) may be
  M18 scope — Artifact 2 AC-10 records this explicitly.
- **Zone 1B proportional allocation:** G3 (#1252) governs the layout contract when MDA
  alert panel and per-scenario crossing rows both populate Zone 1B. G2 Phase 3 defers to
  `minHeight: 80px` + `overflow-y: auto` pending G3.
- **Mode 3 multi-scenario branching:** Out of scope for #394.
- **Backend compare endpoint generalization:** M18 scope (per Architect assessment §Q2).
- **DEMO6 CRITICAL polish (#1249, #1250, #1253):** G4 scope. Phase 3 depends on #1249
  being merged first — it does not implement the N=2 fix.

---

## 8. Review Obligation

**QA Lead:** Frontend Agent (E2E) — test file at
`frontend/tests/e2e/m17-g2-multi-scenario-comparison.spec.ts`

**Test authorship deadline:** Before implementation PR opens (this document filing
plus the test file are the two remaining §2.4 conditions for sprint entry EL approval)

**No soft-skip patterns:** all assertions must be hard-fail per NM-056.
Any test that cannot be hard-asserted before implementation lands uses the
`isVisible().catch(() => false)` guard pattern (returns without failing until
implementation lands, then becomes a hard assertion as per the existing
`m15-g1-layer3-ir-fixes.spec.ts` pattern).

**BPO final acceptance:** After Phase 3 implementation PR merges, BPO acceptance
is triggered by confirming AC-P5 (Aicha's 90-second read) from the running UI.
The BPO may request a screen recording showing the ZMB N=3 comparison at step 4
before issuing formal phase close ACCEPT.

---

*Implementation intent version: 2026-06-25. Phase 3 of G2 — multi-scenario comparison #394.
Derived from Phase 1 (BPO ACCEPT 2026-06-25) and Phase 2 (Architect ADR determination
option (b), 2026-06-25). Implementing agent: Frontend Agent (TrajectoryView.tsx).
QA Lead: Frontend Agent (E2E test file). Sprint entry: m17-g2-sprint-entry.md §2.3.*
