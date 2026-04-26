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
