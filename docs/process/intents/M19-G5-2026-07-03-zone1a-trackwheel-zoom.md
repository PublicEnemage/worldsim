---
name: M19-G5-zone1a-trackwheel-zoom
type: implementation-intent
adr: "N/A — interaction gesture within existing Zone 1A viewport contract; no ADR required (confirmed: NM-086 E2E mock check — no new routes)"
issues: "#1524"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-03
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m19-g5-sprint-entry.md
prerequisite: "#1522 must be merged before this PR opens"
---

# Implementation Intent: G5 — Zone 1A Trackwheel Zoom (Desktop, Reduced Scope) (#1524)

## 1. Source Issue and Architecture Authority

**Issue:** #1524 — Zone 1A TrajectoryView: pinch-zoom, thumbwheel zoom, and pan on trajectory plot
**ADR prerequisite:** None — interaction gesture within existing Zone 1A viewport contract;
no new rendering contract; no ADR required.
**Authored by:** PM Agent
**Date:** 2026-07-03
**Implementing agent:** Frontend Architect Agent

**G5 scope (reduced from original issue):**
Desktop mouse trackwheel (scroll wheel) zoom in/out on Zone 1A trajectory step axis only.
Mobile pinch-zoom, mobile pan, and click-drag pan are deferred (EL decision 2026-07-03 comment
on #1524). Sparse tick strategy at high zoom is deferred — ticks may crowd at maximum zoom;
acceptable for G5.

**Why this matters:**
When trajectory composite scores cluster in a narrow band (e.g., ZMB financial 0.51–0.56,
governance ~0.51), a 20-step full-range view shows scores as a near-flat line. Trackwheel zoom
lets an analyst narrow to steps 3–8 where divergence is visible and defensible at a negotiating
table. This is the core Demo 8 / Mode 3 analyst workflow when inspecting the per-step delta.

**Prerequisite:** #1522 must be merged first. The `visibleStepRange` state slot in
`TrajectoryView` and the `mergeTrajectories(active, baseline, visibleStepRange)` interface
are provided by #1522.

**Browser technical note:**
React's synthetic `onWheel` fires passively in modern browsers (Chrome 51+) — `preventDefault()`
inside it does not stop page scroll. A non-passive native `addEventListener('wheel', handler,
{ passive: false })` on the container ref is required. This is a known constraint; the pattern
is safe and does not require a third-party library.

---

## 2. Scope — Single Deliverable

**What changes:**

| File | Change |
|---|---|
| `frontend/src/components/TrajectoryView.tsx` | MODIFIED — adds `visibleStepRange` state, non-passive wheel listener via `useEffect`, double-click reset handler; passes `visibleStepRange` to `mergeTrajectories` (recharts path) and to `CompositeChartSVG` as new optional prop |
| `frontend/src/components/TrajectoryView.tsx` (`CompositeChartSVG`) | MODIFIED — accepts optional `visibleStepRange?: [number, number] \| null` prop; when non-null, filters `stepIndices` and trajectory steps to the visible range before building path geometry |

**What does NOT change:**
- `computeYDomain` — rescales automatically because `mergedData` is already sliced via #1522
- Any backend code or API contract
- Touch event handling (zero touch events registered)
- `FourFrameworkZone1D`, `PMMWidgetZone1C`, `MDAAlertPanelZone1B` — not in scope

---

## 3. Acceptance Criteria

**AC-1 — Scroll wheel zooms the step axis**
When the mouse cursor is positioned over Zone 1A and the user scrolls the mouse wheel downward
(wheel `deltaY > 0`), the visible step range narrows by approximately 20% per scroll event,
centered on the midpoint of the current visible range. The y-axis rescales to composite scores
visible in the new step slice. Curves that were previously overlapping (< 5px separation)
become visually separated.

**Observable state:** `data-testid="zone-1a-trajectory"` container receives `data-visible-step-min`
and `data-visible-step-max` attributes reflecting the current visible range. After one downward
scroll starting from full 20-step range, the range narrows (e.g., steps [3, 17] instead of
[1, 20]).

**AC-2 — Scroll wheel zoom out restores range**
When the cursor is over Zone 1A and the user scrolls upward (`deltaY < 0`), the visible range
widens up to the full trajectory range. Scrolling beyond full range is a no-op (clamped).

**Observable state:** After scrolling fully out, `data-visible-step-min` and
`data-visible-step-max` match the full trajectory `[minStep, maxStep]`.

**AC-3 — Page does not scroll while hovering Zone 1A**
The `wheel` event listener on the Zone 1A container calls `event.preventDefault()` on every
wheel event that occurs while the cursor is over the Zone 1A container. The outer page scroll
position does not change while the user is scrolling within Zone 1A.

**Observable state:** A Playwright test that scrolls the wheel over `[data-testid="zone-1a-trajectory"]`
observes `window.scrollY` unchanged. The listener is registered with `{ passive: false }`.

**AC-4 — Double-click resets to full range**
When the user double-clicks anywhere within Zone 1A, `visibleStepRange` resets to `null` and
the full trajectory range is restored.

**Observable state:** After zooming in, a double-click on `[data-testid="zone-1a-trajectory"]`
results in `data-visible-step-min` and `data-visible-step-max` returning to the full range.

**AC-5 — No touch events registered**
`TrajectoryView` registers no `touchstart`, `touchmove`, `touchend`, or `pointerdown` handlers.
Mobile browsers scrolling over Zone 1A are unaffected — the page scrolls normally.

**Observable state:** Static check — `frontend/tests/e2e/m19-g5-zone1a-trackwheel-zoom.spec.ts`
uses `page.evaluate` to verify no touch event listener is registered on the Zone 1A container.

**AC-6 — CompositeChartSVG respects visibleStepRange**
When `visibleStepRange` is non-null, `CompositeChartSVG` filters `stepIndices` to the visible
range. Terminal labels, MDA floor line, and comparison scenario curves all reflect the zoomed
step window. The y-domain recomputes from the visible step scores only.

**Observable state:** In comparison mode with `visibleStepRange: [3, 8]`, the SVG contains
path geometry only for steps 3–8. Terminal labels appear at step 8 (not step 20).

---

## 4. File-Level Change Plan

| File | Change type | Detail |
|---|---|---|
| `frontend/src/components/TrajectoryView.tsx` | MODIFIED | `useState<[number, number] \| null>(null)` for `visibleStepRange`; `useRef` for container; `useEffect` with non-passive wheel listener + dblclick reset; pass `visibleStepRange` to `mergeTrajectories` and `CompositeChartSVG` |
| `frontend/src/components/TrajectoryView.tsx` (`CompositeChartSVG`) | MODIFIED | New `visibleStepRange?: [number, number] \| null` prop; filter `stepIndices` when non-null; recompute y-domain from filtered composite scores |
| `frontend/tests/e2e/m19-g5-zone1a-trackwheel-zoom.spec.ts` | NEW | E2E tests covering AC-1 through AC-5; guard pattern if backend unavailable |

---

## 5. Zoom Geometry Specification

The zoom computation on each wheel event:

```
const ZOOM_FACTOR = 0.20;  // 20% range reduction per tick (downward scroll)
const [lo, hi] = current visibleStepRange ?? [minStep, maxStep]
const center = Math.round((lo + hi) / 2)
const halfRange = Math.round((hi - lo) / 2)

if (deltaY > 0) {  // zoom in
  const newHalf = Math.max(1, Math.round(halfRange * (1 - ZOOM_FACTOR)))
  setVisibleStepRange([
    Math.max(minStep, center - newHalf),
    Math.min(maxStep, center + newHalf),
  ])
} else {  // zoom out
  const newHalf = Math.round(halfRange / (1 - ZOOM_FACTOR))
  const newLo = Math.max(minStep, center - newHalf)
  const newHi = Math.min(maxStep, center + newHalf)
  if (newLo === minStep && newHi === maxStep) {
    setVisibleStepRange(null)  // fully zoomed out → reset
  } else {
    setVisibleStepRange([newLo, newHi])
  }
}
```

Center is the midpoint of the current range (not the cursor position). Cursor-centered zoom
is deferred — it requires mapping pixel position to step index, which increases complexity.
Midpoint-centered zoom is correct and sufficient for G5.

---

## 6. QA Notes (NM-086 compliance)

No new API mock routes introduced. No `api_contracts.yml` verification required.

The E2E test file uses the guard pattern: if `__worldsim_setMode` or the trajectory window
seam is unavailable (backend offline), tests return early without failing assertions. This
matches the pattern established in `m19-g5-zmb-yaxis-tight-scoping.spec.ts`.

**NM-086 check:** No new E2E mock routes. No api_contracts.yml cross-check needed.

---

## 7. data-attribute contract (testid observability)

`TrajectoryView`'s outer `div` gains two new `data-` attributes when `visibleStepRange` is non-null:
- `data-visible-step-min="{lo}"` — current visible range lower bound (step index)
- `data-visible-step-max="{hi}"` — current visible range upper bound (step index)

When `visibleStepRange` is null (full range), these attributes are absent. AC-1 and AC-2 use
these attributes to assert zoom state without inspecting internal React state.
