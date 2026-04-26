# UI State Machine — WorldSim Frontend (M4 Baseline)

> Describes the discrete states the application can be in and the events
> that transition between them. Intended to make cross-component state
> interactions explicit so regressions can be reasoned about and tested.
> Updated by the UI/Frontend Architect Agent when new states or transitions
> are added.

---

## Application-Level States

The application has two orthogonal state dimensions that compose:
the **Scenario Context** and the **View Mode**.

### Scenario Context States

```
IDLE
  → (user selects a scenario) → SCENARIO_SELECTED
  → (useEffect status check resolves to "completed") → SCENARIO_PRELOADED

SCENARIO_SELECTED  (currentStep = null)
  → (advance: step N emitted) → SCENARIO_RUNNING
  → (status check → "completed") → SCENARIO_PRELOADED

SCENARIO_RUNNING  (currentStep = N, 1 ≤ N < n_steps)
  → (advance: isComplete = true) → SCENARIO_COMPLETE

SCENARIO_PRELOADED  (currentStep = n_steps, status was "completed" before session)
  [visually identical to SCENARIO_COMPLETE; difference is how currentStep arrived]

SCENARIO_COMPLETE  (currentStep = n_steps)
  → (user selects a different scenario) → SCENARIO_SELECTED
```

Invariant: `currentStep` is null only in IDLE or SCENARIO_SELECTED (pre-resolve).
Once any step has been advanced or the status check resolves, `currentStep`
is a non-null integer for the lifetime of the session.

### View Mode States

```
BASELINE_VIEW  (no scenario selected)
  → Choropleth shows seeded attribute values (no scenario_id/step params)

SCENARIO_VIEW  (scenario selected, compareMode = false)
  → ChoroplethMap shows scenario snapshot values when currentStep is set
  → Falls back to seeded values while currentStep is null (step not yet known)

COMPARE_VIEW  (compareMode = true, both scenario IDs set)
  → DeltaChoropleth replaces ChoroplethMap
  → EntityDetailDrawer is still accessible in compare mode (primary scenario)

DELTA_INCOMPLETE  (compareMode = true, secondScenarioId = null)
  → ChoroplethMap still shown; compare mode checkbox is checked but non-functional
  → Waiting for user to select a second scenario
```

---

## Entity Drawer States

The drawer is an overlay within the scenario view. It has its own state:

```
DRAWER_CLOSED  (selectedEntityId = null)
  → (user clicks country, scenarioId set) → DRAWER_LOADING

DRAWER_LOADING  (loading = true in useMultiFrameworkOutput)
  → (fetch resolves) → DRAWER_DATA
  → (fetch fails, effectiveStep null) → DRAWER_PLACEHOLDER
  → (fetch fails, effectiveStep set) → DRAWER_ERROR

DRAWER_DATA  (data non-null)
  → (user closes drawer) → DRAWER_CLOSED
  → (user advances scenario) → DRAWER_LOADING  (step changed, re-fetch)
  → (user changes scenario) → DRAWER_CLOSED  (selectedEntityId reset)
  → (user clicks different entity) → DRAWER_LOADING

DRAWER_PLACEHOLDER  (effectiveStep = null)
  Shows: "Advance the scenario at least one step to view measurement output."
  This state should not be reachable in M4 because:
    (a) EntityDetailDrawer requires selectedEntityId && selectedScenarioId
    (b) selectedEntityId is cleared by handleSelectScenario (which also clears currentStep)
    (c) step = currentStep ?? selectedScenarioSteps ensures step is never null
  If this state appears, it indicates a state initialization regression.

DRAWER_ERROR  (effectiveStep set, fetch failed)
  Shows: "Error: {error message}"
```

The M4 EntityDetailDrawer placeholder bug was a DRAWER_PLACEHOLDER state
reached when it should have been DRAWER_LOADING. Root cause: the `useEffect`
watching `selectedScenarioId` had an else branch that reset `currentStep = null`
after `handleStepChange` had already set it, causing `effectiveStep` to be null
when the drawer opened.

---

## ScenarioControls Display States

These are local to ScenarioControls and do not affect App.tsx state:

```
IDLE  (currentStep=0, isComplete=false, loading=false)
  → (advance click) → ADVANCING

ADVANCING  (loading=true)
  → (success) → STEPPED (isComplete=false) | COMPLETE (isComplete=true)
  → (failure) → ERROR

STEPPED  (currentStep=N, N < totalSteps)
  → (advance click) → ADVANCING

COMPLETE  (currentStep=totalSteps, isComplete=true)
  [terminal — advance button disabled]

ERROR  (error non-null)
  → (advance click) → ADVANCING  (error is cleared on retry)
```

---

## Transition Event Glossary

| Event | Trigger | State changes |
|---|---|---|
| `selectScenario(id, name, steps)` | ScenarioPanel "Select" | `selectedScenarioId`, `selectedScenarioName`, `selectedScenarioSteps` set; `currentStep=null`; `selectedEntityId=null` |
| `statusCheckResolved(n_steps)` | `useEffect` fetch completes, status=="completed" | `currentStep = n_steps` |
| `advanceStep(step, isComplete)` | ScenarioControls `onStepChange` | `currentStep = step` |
| `clickEntity(entityId)` | ChoroplethMap `onEntityClick` | `selectedEntityId = entityId` |
| `closeDrawer()` | EntityDetailDrawer close button | `selectedEntityId = null` |
| `changeAttribute(key)` | AttributeSelector `onChange` | `attributeName = key` |
| `toggleCompare(bool)` | Compare checkbox `onChange` | `compareMode = bool` |
| `selectSecondScenario(id)` | ScenarioPanel "+ Compare" | `secondScenarioId = id` |
| `togglePanel()` | Scenarios button | `panelOpen = !panelOpen` |

---

## Correctness Invariants

These invariants must hold. A Playwright test that violates any of them
indicates a state management regression:

1. **EntityDetailDrawer is never visible with `step = null`.**
   `currentStep ?? selectedScenarioSteps` ensures step is always a number.

2. **Selecting a new scenario always clears the entity drawer.**
   `handleSelectScenario` calls `setSelectedEntityId(null)`.

3. **`currentStep` is never reset to null by the status-check `useEffect`.**
   The effect has no else branch. Only `handleSelectScenario` resets to null.

4. **Advancing a completed scenario is a no-op.**
   ScenarioControls.advance() guards on `isComplete || loading`.

5. **DeltaChoropleth only renders when both scenario IDs are set.**
   `showDelta = compareMode && selectedScenarioId !== null && secondScenarioId !== null`.

6. **Framework weight changes never suppress MDA alerts.**
   MDA alert display is driven by `output.mda_alerts`, independent of weights.
   Weights only scale `final_score` for visual fill — they do not filter alerts.
