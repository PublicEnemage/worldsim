# Microfrontend Roadmap — WorldSim Frontend

> Records the decision on microfrontend extraction, the rationale, the explicit
> trigger criteria, and the earliest milestone at which extraction could be
> considered. Owned by the UI/Frontend Architect Agent.

---

## Decision: Defer Microfrontend Extraction to No Earlier Than M7

**Date recorded:** 2026-04-26 (M4 exit)
**Status:** Deferred — not under active consideration until M7 entry criteria are met.

---

## What "Microfrontend" Means Here

A microfrontend architecture extracts independently-deployed frontend modules
from the monolith. In WorldSim's context, the candidates would be:

- **Map shell** — the MapLibre choropleth, DeltaChoropleth, and legend overlay
- **Scenario management** — ScenarioPanel, ScenarioControls
- **Entity analysis** — EntityDetailDrawer, RadarChart, FrameworkPanel, MDAAlertPanel
- **Attribute selector** — AttributeSelector (already nearly self-contained)

Each extracted module would be independently built, tested, and potentially
independently deployed. The shell application would compose them at runtime
(via module federation, import maps, or iframe isolation).

---

## Why Not Now (M4/M5/M6)

### The application is not large enough to warrant the overhead.

At M4 close, the frontend is ~1,600 lines across 10 files plus types.
Microfrontend infrastructure — module federation configuration, shared
dependency management, versioning contracts between modules, cross-module
routing — adds complexity that exceeds the complexity of the application itself.

The canonical rule: microfrontends are a solution to organizational scale
problems (multiple teams, independent deploy cycles, ownership boundaries).
WorldSim has one contributor at M4. The architecture does not have the
organizational pressure that microfrontends solve.

### The application does not yet have stable module boundaries.

M5 will add distribution output visualization. M6 will add multi-entity
comparison and URL routing. M7 will add Ecological and Governance framework
UI. Each of these may move components across what today look like natural
module boundaries. Extracting a module before its boundaries are stable
means the extraction will have to be redone.

The right time to extract a module is when you know what it is — when its
interface and responsibilities have been stable across at least two milestones.

### The deployment model does not require it.

The frontend is currently a single Vite build served as a static bundle.
There is no requirement for independent deployment of UI subsections.
The argument for microfrontends rests on operational need; that need does not
yet exist.

---

## M7 Entry Criteria for Reconsideration

The decision must be actively reconsidered at M7 entry if any of the
following conditions are met:

1. **Multiple contributors are working on the frontend simultaneously** and
   experiencing frequent merge conflicts in shared files. If three or more
   people have touched `App.tsx` or `EntityDetailDrawer.tsx` within a single
   milestone, module boundary pressure is real.

2. **The Entity Analysis module (EntityDetailDrawer and its children) has
   grown past 1,500 lines total** across all components in its tree. At that
   scale, independent build and test cycles become valuable.

3. **The deployment architecture has changed** to require independent deploy
   cycles for the map shell vs. the analysis tools (e.g. if a partner
   institution embeds only the map choropleth without the analysis drawer).

4. **Build times have exceeded 90 seconds** for a full production build,
   and code-splitting within the single bundle does not resolve the issue.

If none of these four conditions are met at M7 entry, the decision is
explicitly deferred again to M8, documented with the same criteria check.

---

## Module Federation: The Probable Implementation Path

If extraction is warranted, the implementation would use Vite's module
federation plugin (`@originjs/vite-plugin-federation` or the official
`@module-federation/vite`). This allows:

- Each microfrontend to be independently built as a Vite project
- Runtime composition via federated module imports
- Shared React + ReactDOM to avoid duplicate instances

The alternative (import maps + ESM CDN) is less suitable because WorldSim's
dependencies (MapLibre, Recharts) have non-trivial initialization behavior
that benefits from bundling rather than CDN loading.

**This implementation path is not approved.** It is the likely path if the
extraction decision is made. Formal decision requires a UI/Frontend Architect
Agent design decision entry in `design-decisions.md` with the M7 criteria
assessment.

---

## What This Decision Explicitly Does NOT Defer

The following modularization work proceeds regardless of the microfrontend
decision:

- **CSS module migration** — internal code organization, not deployment boundaries.
- **ScenarioViewContext extraction** — state organization, not module federation.
- **Component extraction within EntityDetailDrawer** — file organization, not
  independent deployment.
- **Test infrastructure** — required before M5 feature work regardless.

Microfrontend extraction is about independent deployment and build isolation.
All internal modularization work (file organization, state decomposition,
component extraction) proceeds on the timeline in `modularization-strategy.md`.
