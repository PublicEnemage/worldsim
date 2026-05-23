# Design Decisions — WorldSim Frontend (M4 Baseline)

> Records the significant design choices made during M2-M4 frontend development,
> with rationale and the alternatives that were considered. This is the institutional
> memory for the frontend layer. Updated by the UI/Frontend Architect Agent when
> consequential decisions are made.

---

## DD-001: Map as Hero Element

**Decision:** The MapLibre GL map occupies the full main content area. All
other UI is header, panel overlay, or drawer overlay on top of the map.

**Rationale:** CLAUDE.md states explicitly: "The map is not decorative. It is
the primary interface." The choropleth is the first thing users see; the scenario
controls and entity detail are secondary. This hierarchy is reflected in the DOM
structure — `<main>` is the map container; ScenarioPanel and EntityDetailDrawer
are `position: absolute` overlays.

**Alternatives considered:** Dashboard layout with map as one of several panels.
Rejected: reduces map to a supplementary element rather than the primary interface.

---

## DD-002: MapLibre Instance Managed Imperatively via useRef

**Decision:** The MapLibre map is initialised once in an empty-deps `useEffect`,
stored in `mapRef`, and updated imperatively (remove/re-add source+layers).
It is not modelled as React state.

**Rationale:** MapLibre GL does not follow React's declarative model. Its
internal rendering pipeline is WebGL and is not compatible with reconciliation.
Trying to treat it as a declarative component (react-map-gl style) adds an
abstraction layer that makes it harder to control MapLibre features directly.

**Alternative considered:** `react-map-gl` or `react-maplibre-gl` wrappers.
Rejected for M2: adds dependency complexity and indirection for unclear benefit
given the controlled scope. May revisit at M6 if map complexity grows.

**Consequence:** Map event listeners (mousemove, click) are registered inside the
data-load effect. When the effect re-runs (on attributeName or step change), old
listeners must be cleaned up. The current approach removes the entire source+layer
and re-adds them, which implicitly removes the old listeners. The `onEntityClickRef`
stable-ref pattern avoids stale closures without recreating listeners on every render.

---

## DD-003: onEntityClickRef — Stable Ref for Map Event Callbacks

**Decision:** `ChoroplethMap` stores `onEntityClick` in a `useRef` that is kept
current on every render. Map click listeners capture the ref, not the prop directly.

**Rationale:** MapLibre event listeners are registered imperatively and are not
re-registered on every React render. If the listener captured the prop value at
registration time, it would form a stale closure. The ref solves this without
recreating listeners.

**This pattern is required** for any map event listener that calls a React prop
or state value. Do not pass callbacks directly to MapLibre event handlers.

---

## DD-004: currentStep / selectedScenarioSteps Dual-State Pattern

**Decision:** App.tsx maintains both `currentStep` (the step actually advanced to)
and `selectedScenarioSteps` (the scenario's total steps from its configuration).
EntityDetailDrawer receives `step={currentStep ?? selectedScenarioSteps}`.

**Rationale:** This was the resolution of a multi-iteration debugging process in M4.
The core problem: when a user selects a pre-completed scenario, ScenarioControls
emits no `onStepChange` events (the advance button is disabled). The drawer needs
to show data at `n_steps` immediately. The `useEffect` status check resolves this
for the async path (it sets `currentStep = n_steps`), but there is a window
between scenario selection (which sets `currentStep = null`) and the effect
resolving where the drawer might open. The `?? selectedScenarioSteps` closes this
window without requiring synchronous state.

**Alternatives tried and discarded:**
- `isAlreadyComplete` prop + `key`-based remounting: caused ScenarioControls to
  remount when `isAlreadyComplete` flipped, losing advance-count state.
- `initialStep`/`initialComplete` props + `useEffect([initialStep, initialComplete])`:
  the useEffect fired on every step advance (because `initialStep` changed each time),
  resetting ScenarioControls' internal display counter.
- Watching only `[initialComplete]`: worked but was unnecessary complexity.
- Final resolution: `currentStep ?? selectedScenarioSteps` — simplest possible fix.

**Lesson:** Adding props to children to solve a parent state problem is usually
wrong. Solve it at the level where the state lives (App.tsx).

---

## DD-005: No State Management Library

**Decision:** All state lives in `useState` in App.tsx. No Redux, Zustand,
Jotai, or React Context.

**Rationale:** At M4, the application has nine state variables in App.tsx and
one custom hook. This is well within the range where prop drilling is clear and
maintainable. The added complexity of a store (action types, selectors, provider
wrapping) is not justified by the current state surface.

**Trigger for reconsideration:** When any of the following occurs:
- A state variable must be accessed by components at more than two levels of
  nesting without a natural parent
- Derived state is computed in multiple components from the same source
- Cross-cutting concerns (e.g. global loading, toast notifications) require
  state visible everywhere

This is expected to become relevant at M5 when distribution outputs add UI
state for confidence interval toggles and distribution visualization options.
See modularization-strategy.md.

---

## DD-006: Inline Styles Over CSS Modules or Utility Classes

**Decision:** Component styles are written as inline `style={{...}}` objects
throughout M4.

**Rationale:** M4 was feature-dense. CSS modules or Tailwind would have required
either a build pipeline change (Tailwind) or file-per-component discipline (CSS
modules) that slowed velocity without improving the outcome for M4 scope.
`App.css` handles global layout; component-level styles are inline.

**This is acknowledged tech debt.** See modularization-strategy.md for the
planned migration path. Do not add new components using inline styles from M5
onward — new components must use CSS modules.

---

## DD-007: localStorage for Framework Weights

**Decision:** Framework weights persist via `localStorage['worldsim.frameworkWeights']`
in JSON format.

**Rationale:** Weights are a user preference, not simulation state. They affect
only the visual fill of the radar chart, not data fetching, not MDA alerts.
Persisting them in localStorage means the user's emphasis choices survive page
reloads. The key is prefixed with `worldsim.` to namespace against other
applications sharing the same origin.

**Boundary:** Weights must never affect MDA alert display. This is enforced by
computing `final_score` (weighted) separately from `mda_alerts` (unconditional).
Tests must verify that weight changes do not suppress MDA alert rendering.

---

## DD-008: ScenarioPanel create Form Hardcodes GRC / 3 Steps

**Decision:** The create scenario form creates a GRC (Greece) scenario with
3 annual steps. There is no UI for configuring entities or step count.

**Rationale:** M4 scope was the human cost ledger. Building a full scenario
configuration UI was explicitly deferred. The hardcoded form was the minimum
required to create scenarios for demo and testing purposes.

**M5 scope:** The create form must support at minimum configurable `n_steps`
and entity selection. The M5 Macroeconomic Module will need scenarios with
more steps and potentially multiple entities.

---

## DD-009: FrameworkPanel isCohortBlock Heuristic

**Decision:** `isCohortBlock(value)` determines whether an `indicators` entry
is a flat QuantitySchema or a nested cohort block by checking for the absence
of a `"value"` key at the top level.

**Rationale:** The API returns `indicators` as a heterogeneous object: some keys
map to `QuantitySchema` directly, others map to `Record<cohortId, QuantitySchema>`.
The heuristic works because `QuantitySchema` always has `value` as a required
field. A nested cohort block's outer key maps to an object whose keys are cohort
IDs — not `QuantitySchema` fields.

**Risk:** If a future QuantitySchema variant lacks a `value` field, this heuristic
would misclassify it as a cohort block. The safer fix would be an explicit type
discriminant from the API (e.g. a `_type: "cohort_block"` field). This is tracked
as a known fragility.

---

## DD-011: Null Governance Axis Rendering — Dashed Outline, "—" Score

**See ADR-005 Decision M8-5.** Rendering behavior for null vs. zero axes is fully
specified in ADR-005 Decision M8-5; do not modify this entry without a corresponding
ADR amendment.

**Decision:** When `composite_score === null`, the governance radar axis renders as a
dashed hollow dot with no filled polygon segment. The score displays `"—"`. The axis
label shows `GOVERNANCE_IN_VALIDATION_LABEL` ("Governance — in validation"). The hover
tooltip displays `GOVERNANCE_IN_VALIDATION_TOOLTIP`. When `composite_score === 0.0`, the
axis renders as a normal filled polygon vertex at zero — distinct from null.

**Implementation detail (CSS/SVG):**
- Null dot: `<circle fill="none" stroke="#aaa" strokeWidth={1.5} strokeDasharray="2 2" />`
- `final_score` in `chartData`: `null` for null composite_score (Recharts treats null as
  a polygon gap, no vertex drawn). `0.0` for zero composite_score (vertex at center).
- Tooltip formatter: `composite_score === null` → returns `GOVERNANCE_IN_VALIDATION_TOOLTIP`
  with `"—"` as the name label.
- Both named constants (`GOVERNANCE_IN_VALIDATION_LABEL`, `GOVERNANCE_IN_VALIDATION_TOOLTIP`)
  are exported from `RadarChart.tsx` and tested in `__tests__/RadarChart.test.ts`.

**Why:** ADR-005 M8-5 prohibits zero-value rendering for governance before promotion
criteria are met. Zero implies governance failure; null implies not-yet-measured.
The "—" + dashed treatment is the reference implementation from `information-hierarchy.md §1B`.

---

## DD-012: Shared State Management — Zustand Atom for Zone 1 Instrument Atomicity

**Decision:** All four Zone 1 instruments (`TrajectoryView`, MDA alert panel, PMM widget,
four-framework current position) subscribe to a single Zustand store atom
(`useScenarioStepStore`) scoped to the active scenario session.

**Rationale:** React's `useState` at a top-level component would require prop-drilling the
trajectory and step state through multiple nesting layers to each Zone 1 instrument. Zustand's
hook-based subscription lets each instrument subscribe directly — while still deriving from the
same `set()` call and batching within the same React render cycle.

**Why not `useQuery` per instrument:** Independent `useQuery` hooks cannot guarantee
simultaneous re-renders. Even with a shared React Query cache, two components subscribed to the
same query key may re-render in separate cycles (ADR-010 Decision 4 Alternative 2). The shared
Zustand atom updated in a single `set()` call, combined with React 18 automatic batching, is the
mechanically correct approach for the atomicity requirement (ADR-008 Decision 14, ADR-010 Decision 4).

**Invariant:** `store.advanceStep()` must call Zustand `set()` exactly once, carrying
`current_step`, `trajectory`, and `computation_state` in the same update object. Multiple
`set()` calls in a single step advance are a violation of the atomicity contract and cause
stale-data flashes. AC-006 tests this invariant directly.

**State atom shape (binding):**
```typescript
interface ScenarioStepState {
  scenario_id: string;
  current_step: number;
  step_count: number;
  trajectory: TrajectoryResponse | null;
  baseline_trajectory: TrajectoryResponse | null;
  computation_state: "idle" | "computing" | "complete";
  mode: "MODE_1" | "MODE_2" | "MODE_3";
}
```

**Source:** FA brief §Shared State Architecture (FA-C2 Resolution), 2026-05-22.

---

## DD-013: Divergence Fill — Merged Key `<Area>` Approach

**Decision:** The Mode 3 divergence fill is implemented as a Recharts `<Area>` component whose
data key pair spans both the active and baseline trajectories via a merged data array.
Each step entry has both `{framework}_active` and `{framework}_baseline` fields; the `<Area>`
renders fill between them.

**Rationale:** The alternative (`<defs>` + `<clipPath>`) requires manually generating SVG path
strings, with careful management of clip behavior at re-convergence. The merged-key approach
stays within Recharts' component model — path generation is the library's responsibility, and
fill naturally disappears when the delta collapses to zero. Step-count mismatches (partial active
trajectory) propagate as `null` values in the merged array, which Recharts treats as gaps.

**Proof-of-concept:** `frontend/sandbox/trajectory-divergence-poc.tsx` validates the approach at:
(a) full 8-curve configuration, (b) re-convergence case (fill disappears), (c) step-count
mismatch (partial active trajectory). Referenced in Issue #460 PR.

**Decision function:** `computeDivergenceFill(active, baseline)` returns `true` only when
`|active - baseline| > 0.01` and both values are non-null. The 0.01 threshold prevents visual
noise from floating-point rounding near convergence. AC-010 tests this threshold exactly.

**`connectNulls={false}` mandatory:** All four active `<Line>` and all four baseline ghost
`<Line>` components must have `connectNulls={false}`. This applies to every framework, not
only governance. AC-015 tests this directly.

**Source:** FA brief §Divergence Fill Implementation (FA-R2 Resolution), 2026-05-22.

---

## DD-014: Step Annotation Character Constraint — ≤ 8 Words AND ≤ 32 Characters

**Decision:** The `step_event_label` field on SIGNIFICANT steps is constrained to ≤ 8 words
AND ≤ 32 characters (including spaces). Both constraints are enforced at fixture CI gate time
(pytest), not only at render time.

**Rationale:** The worst-case trajectory viewport width is 480px at 1024×768. With 6 steps,
each step marker has ~80px horizontal space. At 11px font / 6px average char width:
- 8-word constraint alone is insufficient — "Structural adjustment programme second phase
  begins announced" is 8 words but ~54 chars (~324px at 6px/char), requiring 4 lines at 80px.
- 32-character constraint ensures the label wraps into 2 lines at 80px (192px / 80px = 2.4 lines).

Two lines is the design target; three lines is the permitted maximum.

**Render-time safety net:** If a backend-supplied label exceeds 32 characters despite the
fixture CI gate, the custom XAxis tick truncates with "…" at position 31. This prevents layout
overflow without silently hiding data.

**Enforcement:** `pytest tests/fixtures/` schema validator (QA-F6) runs on every PR. Any Mode 1
scenario fixture with a SIGNIFICANT step whose `step_event_label` exceeds 8 words OR 32
characters fails CI.

**Source:** FA brief §Mode 1 Step Axis Annotation (FA-C5 Resolution), 2026-05-22.

---

## DD-015: Control Plane Zone — 280px Stacked Forms (EL Ruling)

**Decision:** The control plane zone is a persistent 280px CSS grid column adjacent to the
instrument cluster, reserved from M9 onward. In Mode 1 and Mode 2 it is empty whitespace. In
Mode 3 it is populated with policy instruments form (blue) and scenario shocks form (orange),
stacked vertically with both form headers visible without scroll.

**Source of authority:** EL ruling 2026-05-22 (FA-C3 disposition in ADR-008 panel review).
"Simultaneously visible" means both form headers visible without scroll, not all form fields.

**Layout impact:** At 1024×768: trajectory view = 480px, co-primary cluster = 240px,
control plane = 280px (total = 1000px, leaving 24px for padding/scrollbars). At 1280×800:
580px + 400px + 280px = 1260px (leaving 20px).

**Implementation:** The 280px column is always rendered. A CSS class `mode-3-active` populates
it with form content. A subtle placeholder label "Control plane (Mode 3)" renders in Mode 1/2:
≤ 11px font, ≤ 30% opacity, non-interactive (UX Designer sign-off, 2026-05-22).

**Why not collapsible:** Collapsing the control plane zone in Mode 1/2 would require expanding
it on Mode 3 entry, which triggers a layout reflow that shifts both the trajectory view and
co-primary cluster widths. A reflow on mode switch violates the instrument layout stability
requirement (ADR-008 Decision 13). The 280px column must be present at all times.

**Source:** FA brief §Control Plane Zone (FA-C3 Resolution), ADR-008 panel review, 2026-05-22.

---

## DD-010: Recharts for Radar Chart Over D3 or SVG-from-Scratch

**Decision:** The radar chart uses Recharts `RechartsRadarChart` with custom
tick and dot components.

**Rationale:** Recharts provides responsive layout (`ResponsiveContainer`),
tooltip, and the polar grid/axis primitives without requiring raw D3 or manual
SVG authoring. The custom tick and dot give full control over breach badges and
unimplemented-axis styling without fighting the library.

**Constraint:** The `PolarAngleAxis` `tick` prop requires a render function
that receives Recharts-internal props (`x`, `y`, `payload`). These props are
not typed precisely by Recharts; the `CustomTick` component accepts `[key: string]: unknown`
to accommodate this. This is a known typing weakness.

**Alternative considered:** D3 radar chart from scratch. More control; far more
code. Recharts is the correct tradeoff at M4 scope.
