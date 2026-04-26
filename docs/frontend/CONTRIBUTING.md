# Frontend Contribution Guide

> WorldSim frontend contribution standards, owned by the UI/Frontend
> Architect Agent. Backend contribution guide is at `docs/CONTRIBUTING.md`.
> Read this document before opening any PR that touches `frontend/`.

---

## Prerequisites

Before contributing to the frontend, you must understand:

1. `docs/frontend/component-architecture.md` — the component tree and each
   component's responsibility boundary.
2. `docs/frontend/state-ownership.md` — which state lives where and why,
   including the `currentStep` resolution contract.
3. `docs/frontend/design-decisions.md` — the decisions already made and the
   reasoning behind them. Do not re-litigate DD-001 through DD-010 without
   reading their rationale first.
4. `docs/frontend/ui-state-machine.md` — the correctness invariants that
   Playwright tests must enforce.

---

## Stack

| Tool | Version | Purpose |
|---|---|---|
| React | 19 | UI library |
| TypeScript | ~6.0 | Type safety |
| Vite | 8 | Build tool and dev server |
| MapLibre GL | 5 | Map rendering (WebGL) |
| Recharts | 3 | Radar chart |
| ESLint | 9 | Linting |

No CSS framework. No state management library. No test runner yet
(Vitest + Playwright are M5 deliverables — see testing-standards.md).

---

## Development Workflow

```bash
# From repo root
docker compose up frontend   # dev server at http://localhost:3000

# or directly
cd frontend
npm install
npm run dev

# Type check
npm run build   # tsc + vite build; 0 errors required before any commit

# Lint
npm run lint    # ESLint; 0 errors required
```

All PRs must pass `npm run build` and `npm run lint` with zero errors.

---

## TypeScript Requirements

- **Strict mode is on.** Do not add `@ts-ignore` or `as unknown as T` casts
  without a comment explaining why the type system cannot express the invariant.
- All component props must be typed with an explicit `interface Props { ... }`.
  Do not use inline object types for props.
- All API response shapes must be declared in `frontend/src/types.ts`.
  Do not define response types inline in components.
- Use `string` for Decimal values coming from the API (e.g. `composite_score`,
  `attribute_value`). Convert to `number` only at the display layer using
  `parseFloat()`. Never use `as number` on a Decimal string.

---

## Component Standards

See `component-standards.md` for full detail. Key rules:

- **Each component file exports exactly one default component.** Internal
  sub-components (e.g. `TierBadge`, `IndicatorRow`, `CohortBlock`) may be
  co-located in the same file if they are not used outside it.
- **New components must use CSS modules** (not inline styles). Inline styles
  are legacy M4 tech debt. From M5 onward, new components import a `.module.css`
  file. Do not extend the inline style surface.
- **Do not add state to a component** if that state must be shared with a
  sibling or ancestor. Add it to the nearest common ancestor (usually App.tsx
  until the M5 decomposition is in place).
- **Custom hooks** live in `frontend/src/hooks/`. A hook file must start with
  `use` and export exactly one hook as a named export.

---

## State Management Rules

- Do not add a state management library without a UI/Frontend Architect Agent
  design decision (documented in `design-decisions.md`). The criteria for
  adopting a store are defined in DD-005.
- Do not use React Context for application state in M4-M5. Context is acceptable
  only for dependency injection of stable values (e.g. a theme or config object
  that never changes after mount).
- State that affects the choropleth or the drawer must live in App.tsx.
  Local UI state (loading spinners, error messages, form inputs) lives in the
  component that owns it.

---

## Map (MapLibre) Rules

- All MapLibre event listeners that call a React prop or state value must use
  a stable ref (see DD-003 in design-decisions.md). Do not capture props
  directly in event listener closures.
- Map instances must be initialised in an empty-deps `useEffect` and cleaned up
  with `map.remove()` in the effect's return function.
- Data loading (source + layer add/remove) must be a separate `useEffect` from
  map initialisation. It runs on the data dependencies, not on mount.
- Never call `map.addLayer()` before `map.isStyleLoaded()`. Use the
  `map.once("load", ...)` guard pattern.

---

## Async Data Fetching Rules

- All `useEffect` hooks that perform async operations must use the `cancelled`
  flag pattern to prevent stale state updates.
- `fetch` errors must be caught and surfaced in component state. Do not
  swallow errors silently.
- Never parse `attribute_value` strings as numbers in JavaScript.
  MapLibre paint expressions use `["to-number", ...]` — keep numeric conversion
  in MapLibre, not in component code.

---

## No-Browser-State Policy

Do not persist application state in `sessionStorage` or `indexedDB` without
explicit design review. The only permitted browser storage is:

| Key | Owner | Justification |
|---|---|---|
| `worldsim.frameworkWeights` | EntityDetailDrawer | User preference; session-independent |

URL-based state (scenario in query params, entity in hash) is a M6+ feature.

---

## PR Checklist

Before opening a frontend PR:

- [ ] `npm run build` passes with 0 errors
- [ ] `npm run lint` passes with 0 errors
- [ ] `docs/frontend/` updated if component tree, state, or data flow changed
- [ ] New components use CSS modules (not inline styles)
- [ ] Any new state in App.tsx has its entry added to `state-ownership.md`
- [ ] Any new API endpoint consumption added to `data-flow.md`
- [ ] Any new design decision documented in `design-decisions.md`
- [ ] Playwright test added or updated if a UI flow is new or changed
  (required from M5 onward — no new feature ships without a Playwright test)
- [ ] GitHub Issue referenced in PR description with `Closes #N`
