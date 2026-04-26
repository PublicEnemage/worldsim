# Component Architecture — WorldSim Frontend (M4 Baseline)

> Authoritative reference for the M4 component tree as it exists in
> `frontend/src/`. Updated by the UI/Frontend Architect Agent whenever
> components are added, removed, or structurally reorganized.

---

## Component Tree

```
App (frontend/src/App.tsx)
├── AttributeSelector
├── ScenarioPanel  (conditional — panelOpen)
├── ScenarioControls  (conditional — selectedScenarioId)
├── ChoroplethMap  (exclusive with DeltaChoropleth)
│   └── [MapLibre GL instance — not a React component]
├── DeltaChoropleth  (exclusive with ChoroplethMap, compareMode only)
│   └── [MapLibre GL instance — not a React component]
└── EntityDetailDrawer  (conditional — selectedEntityId && selectedScenarioId)
    ├── RadarChart
    │   └── [Recharts RechartsRadarChart]
    ├── MDAAlertPanel
    └── FrameworkPanel  (one active at a time, toggled by tab)
        └── CohortBlock  (conditional — nested cohort indicator groups)
```

**Custom hooks:**
- `useMultiFrameworkOutput` — used exclusively by EntityDetailDrawer

---

## Component Responsibilities

### App.tsx
The single root orchestrator. Owns all cross-component state. Coordinates:
- Which attribute the choropleth renders
- Which scenario is active (primary and comparison)
- How far that scenario has been advanced (`currentStep`)
- Which entity the drawer is showing
- Whether compare mode is on

App.tsx does not render domain UI — it wires children together and owns
the state that must flow between them.

### AttributeSelector
Fetches `GET /attributes/available` on mount. Renders a `<select>` of
all attribute keys present in the seeded entity set. Fires `onChange`
with the selected key. No local state beyond loading/error.

### ScenarioPanel
Renders the scenario management overlay (displayed when `panelOpen` is
true). Two sections: scenario list and create-new-scenario form.
- Fetches `GET /scenarios` on mount and on refresh button.
- On "Select": fetches `GET /scenarios/{id}` to get `n_steps`, then
  calls `onSelectScenario(id, name, n_steps)` on App.
- On "+ Compare": calls `onSelectSecondScenario(id)` directly.
- The create form POSTs to `POST /scenarios` with a hardcoded GRC/3-step
  configuration — the only scenario template available in M4.
- Owns its own list/create state; receives selected IDs from App for
  visual highlighting only.

### ScenarioControls
Renders the "Step N / Total — Complete" indicator and "Next Step" button.
- Calls `POST /scenarios/{id}/advance` on each click.
- Owns internal `currentStep` / `isComplete` / `loading` state — these
  are local UI state for the advance UI, not the authoritative step counter.
- Fires `onStepChange(step, isComplete)` to App after each successful advance.
- Does not know about the drawer or the choropleth.

### ChoroplethMap
MapLibre GL choropleth over all countries for one attribute.
- Initialises the MapLibre instance once (empty-deps useEffect).
- Re-fetches and repaints on any change to `attributeName`, `scenarioId`,
  or `currentStep`. When both `scenarioId` and `currentStep` are non-null,
  passes them as query params to `GET /choropleth/{key}`.
- Uses `onEntityClickRef` (stable ref pattern) to fire `onEntityClick`
  without recreating map event listeners on prop changes.
- Shows a hover popup via `maplibregl.Popup`.

### DeltaChoropleth
MapLibre GL diverging-color choropleth showing delta between two scenarios.
- Fetches `GET /choropleth/{key}/delta?scenario_a=…&scenario_b=…`.
- Same map lifecycle pattern as ChoroplethMap (init once, data reload on deps).
- No entity-click support — delta mode is read-only.
- Renders a built-in legend (decrease / unchanged / increase) as an
  absolutely-positioned overlay div.

### EntityDetailDrawer
Full-height panel overlaid on the right side of the map. Shows multi-framework
measurement output for one entity at one step.
- Uses `useMultiFrameworkOutput` hook for data fetching.
- `effectiveStep`: tracks the last non-null step via `useRef` so the drawer
  keeps showing data after scenario completion even if `step` prop becomes null
  from a hypothetical future reset. In M4, `step` is always non-null when the
  drawer is open (ensured by `currentStep ?? selectedScenarioSteps` in App.tsx),
  so this ref guard is a belt-and-suspenders defence.
- Framework weights stored in `localStorage` under `worldsim.frameworkWeights`.
  Defaults to `{financial:1, human_development:1, ecological:1, governance:1}`.
  Loaded once on mount; persisted on every weights change.
- Contains three sub-sections: RadarChart, MDAAlertPanel, FrameworkPanel tabs.

### RadarChart
Recharts `RechartsRadarChart` displaying the four-axis framework profile.
- Receives `RadarAxisDatum[]` and `FrameworkWeights` from EntityDetailDrawer.
- Custom SVG `<text>` tick (CustomTick) renders axis labels with breach badge
  and grays unimplemented frameworks with ⊘.
- Custom dot (CustomDot) renders red for critical breach, gray for unimplemented.
- Weights are applied to `final_score` as visual-only scaling. MDA alert badges
  fire unconditionally regardless of weights.
- Toggle shows weight sliders (0–2×, step 0.1). Reset button restores all to 1.
- Ecological and governance axes are always `is_implemented=false` at M4
  (composite_score is null).

### MDAAlertPanel
Sorted list of MDA threshold breaches across all frameworks.
- Sorts by severity: TERMINAL → CRITICAL → WARNING.
- Each alert shows: severity badge, mda_id, indicator_key, current value,
  floor value, distance-to-floor percentage, consecutive breach steps.
- Renders cohort entity_id for cohort-level breaches.

### FrameworkPanel
Collapsible indicator table for one measurement framework.
- Toggles open/closed with a header button.
- Renders `composite_score` as percentile rank or "not implemented".
- `isCohortBlock` distinguishes flat QuantitySchema entries from nested
  cohort-grouped entries. Cohort blocks are rendered as collapsible
  `CohortBlock` sub-rows.

### CohortBlock
Collapsible table row group for one cohort entity's indicators within
a FrameworkPanel. Toggled by clicking the cohort header row.

---

## Key Architectural Constraints

- **No router.** Single-page, single view. No URL-based navigation.
- **No state management library.** All cross-component state lives in App.tsx
  via `useState`. Props flow downward; callbacks flow upward.
- **No test framework installed.** Zero automated frontend tests at M4 close.
  Playwright test suite is a hard gate for M5 exit.
- **MapLibre instances are imperative.** They are not React components.
  They are managed via `useRef` and lifecycle effects.
- **API_BASE is hardcoded** in every file as `http://localhost:8000/api/v1`.
  This is an acknowledged tech debt item; environment variable injection
  is deferred to M5.
- **Inline styles throughout.** Intentional for M4 velocity. CSS module or
  Tailwind migration is tracked in modularization-strategy.md.
