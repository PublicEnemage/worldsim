# State Ownership Map — WorldSim Frontend (M4 Baseline)

> Documents which component owns which state, why it lives there, and
> the contracts governing state transitions. Updated by the UI/Frontend
> Architect Agent when state is added, moved, or the transition contracts change.

---

## App.tsx — Cross-Component State

All state that must be visible to more than one component lives here.

| State variable | Type | Initial | Owner rationale |
|---|---|---|---|
| `attributeName` | `string` | `"population_total"` | ChoroplethMap and AttributeSelector both need it |
| `selectedScenarioId` | `string \| null` | `null` | ScenarioControls, ChoroplethMap, EntityDetailDrawer, ScenarioPanel all depend on it |
| `selectedScenarioName` | `string \| null` | `null` | Header display; set alongside `selectedScenarioId` |
| `selectedScenarioSteps` | `number` | `3` | Needed for ScenarioControls `totalSteps` and the `?? selectedScenarioSteps` fallback |
| `currentStep` | `number \| null` | `null` | Drives choropleth step query param and EntityDetailDrawer's step prop |
| `compareMode` | `boolean` | `false` | Controls ChoroplethMap vs. DeltaChoropleth branch |
| `secondScenarioId` | `string \| null` | `null` | DeltaChoropleth and ScenarioPanel selection highlight |
| `panelOpen` | `boolean` | `false` | ScenarioPanel visibility |
| `selectedEntityId` | `string \| null` | `null` | EntityDetailDrawer visibility and identity |

---

## currentStep Resolution Contract

This is the most nuanced state in the application. Its behavior must be
understood precisely to avoid the class of bugs that consumed M4 debugging time.

### Sources that write `currentStep`

1. **`handleSelectScenario`** — always resets to `null` when a new scenario
   is selected. This clears stale step state from a previous scenario.

2. **`handleStepChange(step, _)`** — called by ScenarioControls after each
   successful advance. Always sets `currentStep = step`. Never resets to null
   on completion — the drawer must continue showing data at the final step.

3. **`useEffect([selectedScenarioId])`** — fires when `selectedScenarioId`
   changes. Fetches scenario detail. If `status === "completed"`, sets
   `currentStep = n_steps`. This handles the case where a user selects a
   scenario that was completed in a prior session — ScenarioControls will
   not emit `onStepChange` for a pre-completed scenario.
   **Critical**: this effect has NO `else` branch. The `null` reset is
   exclusively owned by `handleSelectScenario`. Adding an else branch that
   resets `currentStep = null` would race with `handleStepChange` and
   re-introduce the M4 EntityDetailDrawer placeholder bug.

### The `?? selectedScenarioSteps` fallback

`EntityDetailDrawer` receives `step={currentStep ?? selectedScenarioSteps}`.

This fallback fires only when `currentStep` is null — which occurs between
`handleSelectScenario` (sets null) and either the first `handleStepChange`
call or the `useEffect` status check resolving. In this narrow window, the
drawer is not visible (it requires `selectedEntityId` which is also cleared
by `handleSelectScenario`). The fallback exists as a correctness guarantee:
if the drawer somehow opens before `currentStep` resolves, it uses `n_steps`
(the scenario's total steps) rather than passing `null` to the hook, which
would produce a placeholder message.

---

## ScenarioControls — Local UI State

| State variable | Type | Initial | Purpose |
|---|---|---|---|
| `currentStep` | `number` | `0` | Displayed as "Step N / Total". **This is a display counter, not the authoritative step.** The authoritative step is `currentStep` in App.tsx. |
| `isComplete` | `boolean` | `false` | Disables the advance button |
| `loading` | `boolean` | `false` | Shows "Advancing…" and disables button during in-flight request |
| `error` | `string \| null` | `null` | Shows inline error message |

ScenarioControls owns its own display counter because it is the only
component that cares about "what step are we on for the purpose of the
advance button." It does not re-initialize from props when a completed
scenario is re-selected — that is intentional. When a user selects a
pre-completed scenario, ScenarioControls shows "Step 0 / N" while the
advance button is disabled. The EntityDetailDrawer shows data at `n_steps`
because App.tsx's `useEffect` resolved `currentStep` independently.

**Anti-pattern to avoid**: do not add a `useEffect` in ScenarioControls
that watches any prop that changes on each step advance (e.g. `initialStep`).
This pattern was tried and reverted during M4: it caused the display counter
to reset on every advance because `initialStep` is a new value after each
`handleStepChange` call.

---

## EntityDetailDrawer — Local State

| State variable | Type | Initial | Purpose |
|---|---|---|---|
| `weights` | `FrameworkWeights` | `loadWeights()` from localStorage | Framework visual emphasis; persisted across sessions |
| `selectedFramework` | `string` | `"financial"` | Which FrameworkPanel tab is visible |
| `lastStepRef` | `useRef<number \| null>` | `null` | Belt-and-suspenders guard — tracks last non-null step so data is not lost if `step` prop becomes null |

The `data`, `loading`, and `error` states live in `useMultiFrameworkOutput`
and are not surfaced directly in EntityDetailDrawer's state.

---

## ScenarioPanel — Local State

| State variable | Type | Purpose |
|---|---|---|
| `scenarios` | `ScenarioResponse[]` | The fetched scenario list |
| `listError` | `string \| null` | List fetch error |
| `createName` | `string` | Controlled input for new scenario name |
| `creating` | `boolean` | In-flight create request |
| `createSuccess` | `string \| null` | Success message after create |
| `createError` | `string \| null` | Create error message |

Receives `selectedScenarioId` and `secondScenarioId` from App for
visual highlighting only — never writes back to App's scenario IDs.

---

## ChoroplethMap — Local State

| State variable | Type | Purpose |
|---|---|---|
| `error` | `string \| null` | Displayed as a centered overlay if fetch fails |

The MapLibre instance is managed via `mapRef` (not state). The choropleth
data is applied imperatively via `map.addSource` / `map.addLayer` — not via
React state or props.

`onEntityClickRef` is a stable ref pointing to the current `onEntityClick`
prop. This prevents recreating MapLibre event listeners on prop changes
(the listener captures the ref, not the prop value directly).

---

## useMultiFrameworkOutput — Hook-owned Async State

| State variable | Type | Purpose |
|---|---|---|
| `data` | `MultiFrameworkOutput \| null` | Fetched measurement output |
| `loading` | `boolean` | True while fetch is in-flight |
| `error` | `string \| null` | Fetch error message |

Re-fetches on any change to the `(scenarioId, entityId, step)` triple.
When any of the three keys is null/undefined, immediately returns
`{data: null, loading: false, error: null}` without fetching.
Uses the `cancelled` flag pattern for safe async cleanup.

---

## localStorage

One key is written by the frontend:

| Key | Value | Owner |
|---|---|---|
| `worldsim.frameworkWeights` | JSON `FrameworkWeights` | EntityDetailDrawer |

No other browser storage is used. Session and scenario IDs are not persisted —
refreshing the page returns to the default state (no scenario selected).
