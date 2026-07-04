---
name: M19-G5-view-model-retrofit
type: implementation-intent
adr: "N/A — code architecture refactor; no user-visible design decision; no ADR required"
issues: "#1522"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-03
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m19-g5-sprint-entry.md
---

# Implementation Intent: G5 — View Model Layer Retrofit (Zone 1 Extraction) (#1522)

## 1. Source Issue and Architecture Authority

**Issue:** #1522 — View model layer retrofit — extract composition logic from Zone 1 instrument
components
**ADR prerequisite:** None — code architecture refactor; no UX contract change; no ADR required.
**Authored by:** PM Agent
**Date:** 2026-07-03
**Implementing agent:** Frontend Architect Agent

**Background (G5 scheduling rationale):**
#1522 was originally M20+. It is pulled into G5 because #1524 (trackwheel zoom) requires
`visibleStepRange` plumbing that is cleaner to build with extracted pure functions in a
dedicated module. Without the extraction, `visibleStepRange` would thread through a 1338-line
component with no co-located ownership. The G5 scope is a focused extraction — not the full
`buildTrajectoryRenderModel` architectural vision — deliberately sized to unblock #1524 without
introducing refactor risk ahead of Demo 8.

**G5 scope (focused extraction only):**
1. Create `frontend/src/components/trajectoryViewModel.ts` — the new home for pure functions
   currently in `TrajectoryView.tsx`
2. `TrajectoryView.tsx` re-exports all moved functions — existing test imports unchanged
3. `mergeTrajectories` gains optional `visibleStepRange?: [number, number]` param to slice
   steps before merging — the bridge that #1524 uses for zoom state
4. New pure utility `sliceToStepRange` for post-merge filtering in `CompositeChartSVG`

**Explicitly deferred (not G5):**
- `buildTrajectoryRenderModel()` full typed render model
- `ciRibbonModel.ts` CI band geometry extraction
- Secondary components (MDAAlertPanelZone1B, PMMWidgetZone1C, FourFrameworkZone1D)

---

## 2. Scope — Single Deliverable

**What changes:**

| File | Change |
|---|---|
| `frontend/src/components/trajectoryViewModel.ts` | NEW — exports `computeYDomain`, `computeDivergenceFill`, `getConfidenceBadgeVisible`, `mergeTrajectories`, `sliceToStepRange`, and their dependent types (`MergedStepDatum`) |
| `frontend/src/components/TrajectoryView.tsx` | MODIFIED — imports above from `trajectoryViewModel.ts`; re-exports them under the same names; passes optional `visibleStepRange` to `mergeTrajectories` in `mergedData` useMemo |

**What does NOT change:**
- Any exported function signature (except `mergeTrajectories` which gains an optional third param
  — backward compatible; all existing call sites omit the param and continue to work)
- Any test file (existing tests import from `TrajectoryView` via re-export; no import path change)
- Any backend code
- `CompositeChartSVG` internal step-index logic (receives `visibleStepRange` prop in G5 only as
  a pass-through for #1524; does not use it internally until #1524 lands)

---

## 3. Acceptance Criteria

**AC-1 — trajectoryViewModel.ts exists with correct exports**
`frontend/src/components/trajectoryViewModel.ts` exists and exports:
- `computeYDomain(values: number[]): [number, number]`
- `computeDivergenceFill(active: number | null, baseline: number | null): boolean`
- `getConfidenceBadgeVisible(confidenceTier: number): boolean`
- `mergeTrajectories(active, baseline, visibleStepRange?): MergedStepDatum[]`
- `sliceToStepRange(data: MergedStepDatum[], range: [number, number]): MergedStepDatum[]`
- `MergedStepDatum` type (re-exported for consumers)

**Observable state:** `import { computeYDomain } from "../trajectoryViewModel"` resolves
without TypeScript error.

**AC-2 — TrajectoryView.tsx re-exports are present**
`TrajectoryView.tsx` still exports `computeYDomain`, `computeDivergenceFill`,
`getConfidenceBadgeVisible`, `mergeTrajectories` by name (via re-export from
`trajectoryViewModel.ts`). Existing test import `from "../TrajectoryView"` still resolves.

**Observable state:** `TrajectoryView.test.ts` passes without any import path change.

**AC-3 — All existing pure-function unit tests pass unchanged**
`TrajectoryView.test.ts` tests for `computeDivergenceFill`, `getConfidenceBadgeVisible`,
`computeYDomain`, `FRAMEWORKS`, `CONNECT_NULLS` all pass. No test modification required.

**Observable state:** `npm run test` exits 0; `TrajectoryView.test.ts` shows all green.

**AC-4 — mergeTrajectories visibleStepRange filtering**
When `visibleStepRange: [3, 7]` is passed as the third argument to `mergeTrajectories`,
the returned `MergedStepDatum[]` contains only steps with `step_index` in [3, 7] inclusive.
When `visibleStepRange` is undefined (or null), all steps are returned (existing behavior).

**Observable state:** Unit test in `trajectoryViewModel.test.ts`:
```
mergeTrajectories(trajectory10steps, null, [3, 7]).map(d => d.step_index) === [3, 4, 5, 6, 7]
mergeTrajectories(trajectory10steps, null, undefined).length === 10
```

**AC-5 — sliceToStepRange pure function**
`sliceToStepRange(data, [3, 7])` returns only items where `step_index >= 3 && step_index <= 7`.
Empty array input returns empty array. Range `[0, Infinity]` returns all items.

**Observable state:** Unit test in `trajectoryViewModel.test.ts`.

**AC-6 — No behavior regression in TrajectoryView**
Recharts path and composite SVG path render identically before and after the extraction
(no visual change). `yDomain` continues to rescale from `mergedData`.

**Observable state:** Existing E2E tests that observe Zone 1A pass without change.

---

## 4. File-Level Change Plan

| File | Change type | Detail |
|---|---|---|
| `frontend/src/components/trajectoryViewModel.ts` | NEW | All pure functions + `MergedStepDatum` type |
| `frontend/src/components/TrajectoryView.tsx` | MODIFIED — imports + re-exports | Remove function bodies; add `export { ... } from "./trajectoryViewModel"`; update `mergedData` useMemo to pass `visibleStepRange` |
| `frontend/src/components/__tests__/trajectoryViewModel.test.ts` | NEW | AC-4 and AC-5 unit tests; verifies extraction did not alter function behavior |

---

## 5. QA Notes (NM-086 compliance)

No new API mock routes introduced. No `api_contracts.yml` verification required.

`trajectoryViewModel.test.ts` covers AC-4 and AC-5 with pure-function unit tests (no React
component mounting required). Existing `TrajectoryView.test.ts` covers AC-3 via re-export.

**NM-086 check:** No new E2E mock routes. No api_contracts.yml cross-check needed.

---

## 6. Implementation Sequence Note

#1522 must merge before any #1524 implementation PR opens. The `visibleStepRange` parameter
added to `mergeTrajectories` in AC-4 is the interface that #1524 uses. If both issues are
implemented in the same session, the implementing agent must verify #1522 is green on CI
before opening the #1524 PR.
