# Data Flow — WorldSim Frontend (M4 Baseline)

> Traces how data moves from API responses through the component tree to
> rendered UI. Updated by the UI/Frontend Architect Agent when new API
> endpoints are consumed or data paths change.

---

## API Surface Consumed by the Frontend

All requests target `http://localhost:8000/api/v1` (hardcoded `API_BASE`).

| Endpoint | Caller | Trigger |
|---|---|---|
| `GET /attributes/available` | AttributeSelector | On mount |
| `GET /scenarios` | ScenarioPanel | On mount; on refresh button |
| `GET /scenarios/{id}` | ScenarioPanel | On "Select" button for primary scenario |
| `GET /scenarios/{id}` | App.tsx `useEffect` | When `selectedScenarioId` changes |
| `POST /scenarios` | ScenarioPanel | Create form submit |
| `POST /scenarios/{id}/advance` | ScenarioControls | "Next Step" button |
| `GET /choropleth/{key}` | ChoroplethMap | On `attributeName`, `scenarioId`, or `currentStep` change |
| `GET /choropleth/{key}/delta` | DeltaChoropleth | On `scenarioAId`, `scenarioBId`, `attributeName` change |
| `GET /scenarios/{id}/measurement-output` | `useMultiFrameworkOutput` | When any of `(scenarioId, entityId, step)` changes |

---

## Flow 1: Baseline Choropleth (no scenario)

```
App renders ChoroplethMap(attributeName, scenarioId=null, currentStep=null)
  → ChoroplethMap useEffect fires
  → GET /choropleth/{attributeName}  (no query params)
  → GeoJSON FeatureCollection returned
  → computeSteps() derives percentile breakpoints from attribute_value strings
  → map.addSource() + map.addLayer() paint the fill
  → Hover popup reads feature.properties.{name, attribute_value, confidence_tier}
```

---

## Flow 2: Scenario Choropleth (scenario active, step advanced)

```
User selects scenario  →  App.handleSelectScenario(id, name, steps)
  setSelectedScenarioId, setSelectedScenarioSteps, setCurrentStep(null)

useEffect([selectedScenarioId]) fires
  →  GET /scenarios/{id}
  →  if status=="completed": setCurrentStep(n_steps)
  →  else: currentStep stays null (no else branch)

User clicks "Next Step"  →  ScenarioControls.advance()
  →  POST /scenarios/{id}/advance
  →  data.step_executed → ScenarioControls.setCurrentStep(N)
  →  onStepChange(N, isComplete)  →  App.setCurrentStep(N)

App re-renders ChoroplethMap(attributeName, scenarioId=id, currentStep=N)
  →  ChoroplethMap useEffect fires (currentStep changed)
  →  GET /choropleth/{attributeName}?scenario_id={id}&step={N}
  →  Snapshot data returned; map repainted with scenario values
```

---

## Flow 3: Entity Detail Drawer

```
User clicks country on map
  →  ChoroplethMap map.on("click") fires
  →  onEntityClickRef.current(entity_id)  →  App.handleEntityClick(entity_id)
  →  App.setSelectedEntityId(entity_id)

App renders EntityDetailDrawer(
  scenarioId, entityId,
  step = currentStep ?? selectedScenarioSteps
)

EntityDetailDrawer calls useMultiFrameworkOutput(scenarioId, entityId, effectiveStep)
  →  GET /scenarios/{id}/measurement-output?step={N}&entity_id={entity_id}
  →  MultiFrameworkOutput returned:
       entity_name, timestep, outputs (financial/human_development/ecological/governance)
       ia1_disclosure

  EntityDetailDrawer derives RadarAxisDatum[] from outputs[fw].composite_score
  RadarChart renders 4-axis radar; unimplemented axes (ecological, governance) show ⊘

  MDAAlertPanel renders all mda_alerts from all frameworks, sorted by severity

  FrameworkPanel renders indicator table for selectedFramework:
    flat QuantitySchema entries → IndicatorRow
    nested cohort-keyed objects → CohortBlock (collapsible)
```

---

## Flow 4: Compare Mode (Delta Choropleth)

```
User checks "Compare scenarios" checkbox  →  App.setCompareMode(true)
User clicks "+ Compare" on a second scenario  →  App.setSecondScenarioId(id)

showDelta = compareMode && selectedScenarioId && secondScenarioId
  →  DeltaChoropleth renders instead of ChoroplethMap

DeltaChoropleth useEffect fires
  →  GET /choropleth/{attributeName}/delta?scenario_a={id}&scenario_b={id2}
  →  Delta GeoJSON returned with attribute_value = str(B - A)
  →  computeDivergingSteps() derives red/white/blue breakpoints
  →  Diverging fill layer painted; popup shows value_a, value_b, delta, direction
```

---

## Async Cancellation Pattern

All async operations use a `cancelled` flag or equivalent:

```typescript
let cancelled = false;
// ... async operation ...
if (cancelled) return;
// cleanup:
return () => { cancelled = true; };
```

This prevents stale data from a superseded request overwriting state after
a new request has already started. Every `useEffect` that does a fetch
follows this pattern. Missing it causes race conditions where a slower
earlier request resolves after a faster later one.

---

## Data Shapes at Key Boundaries

### ChoroplethFeatureProperties (from GeoJSON features)
```typescript
{ entity_id, name, attribute_value: string, // Decimal as string — to-number in MapLibre
  confidence_tier, has_territorial_note, territorial_note }
```
`attribute_value` is always a string. MapLibre paint expressions use
`["to-number", ["get", "attribute_value"]]` — never parse it in JS.

### MultiFrameworkOutput (from measurement-output endpoint)
```typescript
{
  entity_id, entity_name, timestep, scenario_id, step_index,
  outputs: {
    financial:         { composite_score: string|null, indicators, mda_alerts, ... },
    human_development: { composite_score: string|null, indicators, mda_alerts, ... },
    ecological:        { composite_score: null, note: "...", ... },  // always null at M4
    governance:        { composite_score: null, note: "...", ... },  // always null at M4
  },
  ia1_disclosure: string  // always present, never null
}
```

`indicators` entries are either flat `QuantitySchema` or nested
`Record<cohortId, Record<indicatorKey, QuantitySchema>>` for cohort-level data.
`isCohortBlock()` in FrameworkPanel distinguishes the two by checking for
the absence of a `"value"` key at the top level.

---

## Known Data Flow Gaps (M4 → M5)

1. **No real-time updates.** The frontend polls only on user action.
   If a background process modifies a scenario, the UI does not refresh.
   For M4 scope this is acceptable — all scenarios are advanced manually.

2. **No pagination.** `GET /scenarios` returns all scenarios. This will
   become a UI problem as the scenario list grows. Pagination or search
   is M5+ scope.

3. **API_BASE hardcoded.** No environment variable injection. Docker Compose
   works today because both services are on localhost; this breaks in any
   non-localhost deployment. Fix tracked in modularization-strategy.md.

4. **No loading skeleton on choropleth repaint.** The map silently shows
   stale data while a new fetch is in flight. A loading indicator on the
   map overlay is M5 scope.
