---
name: M19-G5-zmb-yaxis-tight-scoping
type: implementation-intent
adr: ADR-017 §Zone 1A Encoding Contract (CompositeChartSVG y-domain display contract)
issues: "#1629"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-03
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m19-g5-sprint-entry.md
---

# Implementation Intent: G5 — ZMB Zone 1A Y-axis Tight-Scoping (#1629)

## 1. Source Issue and Architecture Authority

**Issue:** #1629 — Zone 1A ZMB scenario comparison: y-axis not tight-scoped — three curves
visually collapse to single band
**ADR prerequisite:** None — `computeYDomain` fix is within ADR-017 Zone 1A display contract.
**Authored by:** PM Agent
**Date:** 2026-07-03
**Implementing agent:** Frontend Architect Agent

**Root cause (identified at sprint entry, 2026-07-03):**
In `CompositeChartSVG` (`TrajectoryView.tsx`), the `useMemo` block computing `[yMin, yMax]`
(lines ~413–433) includes `getEntityMdaFloor()` values in the `values` array alongside
trajectory composite scores. For the ZMB scenario comparison in Demo 8 Act 2:

- Three scenario PHR composite scores: ~0.540 (Option C), 0.584 (Option B), 0.628 (Option A)
- ZMB MDA floor: ~0.40
- Combined range: [0.40, 0.628] → `computeYDomain` produces [0.35, 0.678] = 0.328 range
- Chart height ~240px → 240px / 0.328 = 732px per unit
- Curve separation between options: 0.044 × 732 ≈ 32px → barely visible speckles

Including the MDA floor anchors the y-scale to a wide range, making curves with 0.04–0.05
data spread visually indistinguishable. This is the "colour speckles" observation in the
original issue.

**Fix strategy:**
In scenario comparison mode (`comparisonScenarios.length > 0`), exclude MDA floor values
from the y-domain computation. The MDA floor is rendered as a fixed horizontal line and
remains visible; it should not anchor the y-scale. Tight-scoping to the trajectory data
range allows curve separation of ≥ 20px at the Demo 8 viewport (1280×800, Zone 1A ~240px
height with ZMB data spread 0.044–0.044–0.044).

Optionally: if the MDA floor is within 0.10 of the tight data range, re-include it so
the "distance from floor" is visually anchored (safety margin 0.10 chosen to avoid
accidentally hiding a near-floor crossing scenario).

---

## 2. Scope — Single Deliverable

**What changes:**
- `frontend/src/components/TrajectoryView.tsx` — `CompositeChartSVG` component, `useMemo`
  y-domain block: conditional exclusion of MDA floor values from `values` when in scenario
  comparison mode

**What does NOT change:**
- `computeYDomain` function signature or behavior (it already tight-scopes correctly)
- MDA floor line rendering (stays as-is; floor line remains visible)
- `recharts` path in `TrajectoryView` (separate rendering path, see §Notes)
- Any backend code

---

## 3. Acceptance Criteria

**AC-1 — Scenario curve visual separation (primary)**
When Zone 1A renders a scenario comparison with 3 ZMB options (PHR composite scores
Option A: 0.628, Option B: 0.584, Option C: 0.540) at viewport 1280×800, each pair of
adjacent scenario curves must have a visible vertical gap of ≥ 15px at the chart render
height of ≈ 240px.

**Observable state:** Three distinct, non-overlapping curves in Zone 1A. No "colour speckle"
band visible in place of three separate lines.

**AC-2 — MDA floor line remains visible**
When the MDA floor value (e.g., 0.40) is within the expanded y-range that would normally
include the floor (i.e., floor value is within 0.10 of the tight data-range minimum), the
floor line remains rendered. When the floor is more than 0.10 below the tight data minimum,
the floor line is not rendered (it is outside the visible y-range).

**Observable state:** In the ZMB Demo 8 comparison (floor ~0.40, data min ~0.540), the MDA
floor line is NOT rendered because 0.540 − 0.40 = 0.14 > 0.10. The chart shows only the
three trajectory curves.

**AC-3 — Single-entity Mode 1/2 unchanged**
In Mode 1 or Mode 2 with a single entity (4 framework lines), the y-domain computation is
unchanged. `computeYDomain` continues to include MDA floors in the domain for single-entity
rendering (where floor proximity to data is typically small and the "distance from floor"
visual anchor is important).

**Observable state:** Existing Playwright screenshots for single-entity Zambia/Senegal
scenarios pass without regression.

**AC-4 — computeYDomain function unchanged**
The `computeYDomain` exported function (line ~80–90 `TrajectoryView.tsx`) has no signature
changes. The fix is in the `CompositeChartSVG` useMemo block's value population, not in
`computeYDomain` itself.

**Observable state:** Importing code that calls `computeYDomain(values)` with the same
arguments produces the same results as before.

---

## 4. File-Level Change Plan

| File | Change | Why |
|---|---|---|
| `frontend/src/components/TrajectoryView.tsx` | `CompositeChartSVG` — modify useMemo y-domain block: do not push `getEntityMdaFloor()` values to `values` array when `comparisonScenarios.length > 0` (or when floor is > 0.10 below tight data min) | Stops floor from anchoring y-scale in comparison mode |
| `frontend/tests/e2e/m19-g5-zmb-yaxis-tight-scoping.spec.ts` | New E2E test for AC-1, AC-2, AC-3 | QA gate |

---

## 5. QA Notes (NM-086 compliance)

This deliverable makes no API calls beyond what existing TrajectoryView tests already cover.
No new mock routes are introduced. `computeYDomain` is already exported and has existing unit
test coverage. E2E test must verify the visual separation via bounding-box measurement (not
screenshot diff) since chart heights are viewport-dependent.

**NM-086 check:** No new E2E mock routes introduced by this fix. No `api_contracts.yml`
verification required.

---

## 6. Notes

The `recharts` path in `TrajectoryView` (used when `useComposite` is false, i.e. for
single-entity Mode 1/2) uses a separate domain computation. That path is not affected by
this fix — it correctly tight-scopes via a different code path (line ~883
`computeYDomain(values)`). The scenario comparison path always uses `CompositeChartSVG`.
