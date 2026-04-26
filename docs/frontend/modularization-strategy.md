# Modularization Strategy — WorldSim Frontend

> Describes the current App.tsx-centric structure, the planned decomposition
> for M5, and the longer-term modularization trajectory. Owned by the
> UI/Frontend Architect Agent.

---

## Current Structure (M4 Baseline)

The frontend is a **monolithic single-file orchestrator** (`App.tsx`) that owns
all cross-component state and wires 8 leaf components together via props and
callbacks.

```
App.tsx                    — 145 lines; 9 state variables; 4 handlers; 1 effect
  ├─ AttributeSelector     — 47 lines; self-contained; 1 API call
  ├─ ScenarioPanel         — 199 lines; self-contained; 2 API calls
  ├─ ScenarioControls      — 77 lines; self-contained; 1 API call
  ├─ ChoroplethMap         — 203 lines; MapLibre; 1 API call
  ├─ DeltaChoropleth       — 235 lines; MapLibre; 1 API call
  └─ EntityDetailDrawer    — 262 lines; 2 local states; delegates to hook
       ├─ RadarChart        — 247 lines; Recharts; 0 API calls
       ├─ MDAAlertPanel     — 110 lines; pure display; 0 API calls
       └─ FrameworkPanel    — 179 lines; 1 local state; 0 API calls

Hooks:
  useMultiFrameworkOutput  — 65 lines; 1 API call; cancellation pattern

Types:
  types.ts                 — 146 lines; all API response shapes
```

**What works well:**
- Clear component boundaries with well-defined prop interfaces
- Single source of truth for all cross-component state
- No prop drilling beyond two levels (App → leaf)
- Each component is independently understandable

**What needs to change for M5:**
- App.tsx will become unwieldy as M5 adds distribution visualization state,
  uncertainty toggle state, and Macroeconomic Module controls
- `API_BASE` is hardcoded in six files — environment variable injection needed
- No CSS module structure — inline styles are not scalable
- No test infrastructure — must be added before M5 feature work begins

---

## M5 Decomposition Plan

M5 adds: distribution outputs, uncertainty bounds visualization, Macroeconomic
Module indicators, and Playwright test infrastructure. These additions require
targeted decomposition before they make App.tsx unmanageable.

### Phase 1: Infrastructure (before M5 feature work)

**1a. Test infrastructure**
Install Vitest, @testing-library/react, MSW, Playwright. Configure CI to run
both Vitest and Playwright. Write the three required Playwright flows before any
M5 feature work begins.

**1b. Environment variable injection**
Replace hardcoded `const API_BASE = "..."` in all 6 files with a single source:
```typescript
// frontend/src/config.ts
export const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api/v1";
```
All components import from `config.ts`. The Vite build can inject `VITE_API_BASE`
from Docker Compose environment. This unblocks non-localhost deployments.

**1c. CSS module migration for new components**
Do not migrate existing inline-styled components. Any M5 component that is new
or significantly rewritten uses CSS modules. This creates a migration path by
progressive replacement rather than a big-bang rewrite.

### Phase 2: State Decomposition

M5 will add at minimum:
- Uncertainty display toggle (show/hide confidence bounds)
- Distribution visualization options (histogram, percentile bands)
- Macroeconomic Module indicator panel state

These are candidates for a `ScenarioViewContext`:

```typescript
// Wraps: ChoroplethMap, ScenarioControls, EntityDetailDrawer, and their toolbar
interface ScenarioViewState {
  selectedScenarioId: string | null;
  selectedScenarioName: string | null;
  selectedScenarioSteps: number;
  currentStep: number | null;
  selectedEntityId: string | null;
  uncertaintyVisible: boolean;
  distributionMode: "point" | "interval" | "histogram";
}
```

App.tsx retains: `attributeName`, `compareMode`, `secondScenarioId`, `panelOpen`.
These are map-layer and panel-visibility concerns that span beyond the scenario view.

**Decision criteria:** Introduce `ScenarioViewContext` only when any of these
is true:
- A new M5 component needs scenario view state and would require passing it
  through more than one intermediate parent
- Two sibling components both need write access to the same piece of state
- ScenarioViewState grows beyond 10 variables

If none of these trigger in M5, keep all state in App.tsx and document
why in design-decisions.md.

### Phase 3: Component Extraction

As the EntityDetailDrawer grows (it will — distribution outputs add
visualization components), extract:

```
EntityDetailDrawer (coordinator only)
  ├─ EntityHeader               — entity name, timestep, close button
  ├─ FrameworkOverview          — radar chart + weight sliders
  │    └─ RadarChart            — (existing)
  ├─ MDAAlertPanel              — (existing)
  └─ FrameworkDetailPanel       — framework tabs + indicator tables
       ├─ DistributionPanel     — NEW (M5) — confidence bounds visualization
       └─ FrameworkPanel        — (existing, renamed IndicatorTable)
```

This extraction is not a M5 requirement — it is the planned shape for when
EntityDetailDrawer grows past ~350 lines. Trigger: EntityDetailDrawer exceeds
350 lines or contains more than 3 distinct visual sections.

---

## Longer-Term Modularization (M6-M7)

### Multi-Entity View (M6)

The current architecture assumes one primary entity in the drawer at a time.
When the Ecological Module activates, users will want to compare two countries
side-by-side. This requires:
- A drawer that can show two entity columns (or a new full-page entity comparison view)
- URL-based state so entity comparison links can be shared

Design decision deferred to M6 entry. Do not pre-architect for this in M5.

### Attribute Configuration Panel (M6)

The ScenarioPanel create form hardcodes GRC/3-steps. A real configuration panel
will need:
- Entity multi-select (search + checkbox)
- Step count input with validation
- Module configuration toggles (DemographicModule, MacroeconomicModule)
- Initial attribute overrides

This is substantial new UI. It will be a separate panel or modal, not an
extension of the current create form. Design at M5 exit, implement in M6.

### URL-Based State (M6)

Persisting `selectedScenarioId`, `selectedEntityId`, `currentStep` in the URL
query string allows shareable links and browser-back navigation. Requires adding
a router (React Router or TanStack Router). Decision deferred to M6.

---

## What Is Explicitly Not Being Refactored

- **The Map is not becoming a React component.** MapLibre stays imperative.
  The `useRef` + `useEffect` pattern is the correct abstraction.
- **Recharts is not being replaced.** The radar chart works. Replace only if
  a capability gap requires it.
- **CSS-in-JS libraries are not being adopted.** CSS modules are the path.
- **The overall architecture of App.tsx as orchestrator is not changing in M5.**
  Context extraction is contingent on the triggers above being met.
