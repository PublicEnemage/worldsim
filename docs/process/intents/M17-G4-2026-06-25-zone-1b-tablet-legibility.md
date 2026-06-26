---
name: M17-G4-zone-1b-tablet-legibility
type: implementation-intent
issues: "#1250"
status: Step 1 authored — QA tests may be authored; implementation begins after #1253 merges
authored-by: Frontend Architect Agent
authored-date: 2026-06-25
implementing-agent: Frontend Engineer
sprint-entry: "docs/process/sprint-plans/m17-g4-sprint-entry.md — EL Approved 2026-06-25"
ux-visual-spec: "docs/ux/specs/m17-g4-1250-zone-1b-tablet-legibility.md"
adr-reference: "N/A — responsive tuning within ADR-017 Zone 1B boundary; no architectural decision required"
release-branch: release/m17
---

# Implementation Intent: M17-G4 — Zone 1B Tablet Legibility at 768px (#1250)

> **UX visual spec governs.** All observable state requirements are derived from
> `docs/ux/specs/m17-g4-1250-zone-1b-tablet-legibility.md`.
>
> **FA implementation sequence:** #1250 is the 3rd issue in FA sequence
> (#1249 → #1253 → #1250 → #1239). Implementation PR opens after #1253 merges.
>
> **G3 coordination gate (sprint entry §2.5 and §1):** #1250 must merge to
> `release/m17` before the G3 Phase 3 implementation PR opens. G3 and #1250
> both touch Zone 1B layout and cannot be in-flight concurrently.

---

## 1. Source

**Issue:** #1250 — ux(zone-1b): DEMO6-026/043 tablet legibility at 768px

**Root cause:** `CohortImpactSection` in `MDAAlertPanelZone1B.tsx` uses hardcoded
inline font sizes (row: 10px, severity badge: 9px, tier badge: 8px, sublabel: 7px)
with no responsive breakpoint. At 768px viewport width, these sizes are unreadable
at demo viewing distance.

`useViewportBreakpoint()` (in `InstrumentCluster.tsx`) returns 1024 for all viewports
< 1280px, including 768px. `CohortImpactSection` does not currently consume this hook.

**The fix:** Import `useViewportBreakpoint` into `CohortImpactSection` (or use a
local `useIsNarrow` hook as specified in `docs/ux/specs/m17-g4-1250-zone-1b-tablet-legibility.md §7`).
Apply increased font sizes when breakpoint is 1024 (viewport < 1280px), including 768px.

**Scope constraint:** Font size changes only, in `CohortImpactSection` only.
No layout structure changes. No changes at 1280×800 or wider viewports.

---

## 2. Required Font Size Changes

Per `docs/ux/specs/m17-g4-1250-zone-1b-tablet-legibility.md §3`:

| Element | Current (all viewports) | After (at ≤ 1023px) | After (at ≥ 1280px) |
|---|---|---|---|
| Row container | 10px | **11px** | 10px (unchanged) |
| Severity badge | 9px | **10px** | 9px (unchanged) |
| Tier badge (`cohort-tier-badge-*`) | 8px | **10px** | 8px (unchanged) |
| Tier sublabel (`confidence-tier-badge-sublabel`) | 7px | **9px** | 7px (unchanged) |

---

## 3. Persona Trace Elements Targeted

**P-1 — Persona served:** **Persona 2 — Aicha Mbaye (Finance Ministry Negotiator)**
(`docs/ux/personas.md §Persona 2`). Zone 1B CohortImpactSection is the distributional
consequence record. Aicha reads cohort crossing rows to identify which population groups
are breaching MDA floors — and cites this data in a conditionality negotiation. At 768px
(tablet), 7–9px font sizes are unreadable.

**P-4 — Time/interaction ceiling:** 90 seconds (Reactive). Zone 1B must be readable
at glance level at all supported viewport widths, including 768px.

**P-7 — North star capability delivered:**
After this fix, a finance ministry analyst reading Zone 1B cohort crossing data on a
tablet (768px) can read the tier badge, severity label, and sublabel without zooming.
This is the tablet-legibility condition required for Demo 7 presentations on shared
display hardware.

---

## 4. Observable Application State

### 4.1 Primary observable states

**At 768px viewport (Playwright page.setViewportSize({ width: 768, height: 1024 })):**

For a scenario where Zone 1B shows cohort crossing rows:
- `data-testid="cohort-tier-badge-{indicator_key}"` has computed font size ≥ 10px
- `data-testid="confidence-tier-badge-sublabel"` has computed font size ≥ 9px

**At 1280×800 viewport (regression guard):**
- `data-testid="cohort-tier-badge-{indicator_key}"` has computed font size ≥ 8px (unchanged)
- `data-testid="confidence-tier-badge-sublabel"` has computed font size ≥ 7px (unchanged)

### 4.2 Silent failure detection

**Silent failure — breakpoint logic inverted:**
If the `is768` condition is accidentally inverted (applying small fonts at 768px and large
fonts at 1280px), the 768px test fails with "font size < 10px" and the 1280px regression
test fails with "font size > 8px." Both assertions catch the inversion.

**Silent failure — hook not triggered at Playwright viewport:**
If `useViewportBreakpoint` (or `useIsNarrow`) is not reactive to `page.setViewportSize`
in the Playwright test environment, the font size never updates. The implementing agent
must verify that the hook fires in the Playwright environment during Step 4 Verify.
If not reactive, the implementation must use `window.innerWidth` directly in an initial
state computation rather than a resize event listener.

---

## 5. Acceptance Criteria

**AC-1250-1 (tier badge legibility at 768px):**
At 768px viewport width, for a scenario where Zone 1B displays a cohort crossing row,
the element at `data-testid="cohort-tier-badge-{indicator_key}"` has computed CSS
`font-size` ≥ 10px.

**AC-1250-2 (sublabel legibility at 768px):**
At 768px viewport width, the element at `data-testid="confidence-tier-badge-sublabel"`
has computed CSS `font-size` ≥ 9px.

**AC-1250-3 (regression — 1280×800 layout unaffected):**
At 1280×800 viewport, `data-testid="cohort-tier-badge-{indicator_key}"` has computed
CSS `font-size` ≥ 8px and ≤ 9px (confirming unchanged from current 8px, not increased).
`data-testid="confidence-tier-badge-sublabel"` has computed CSS `font-size` ≥ 7px and ≤ 8px.

---

## 6. Kryptonite Constraint Check

`[x]` **No specialist mediation required.** Increasing font size does not change the
semantic content of Zone 1B — only its legibility. Persona 2 reads the same crossing
information at larger scale. No new cognitive demand introduced.

---

## 7. Out of Scope

**Zone 1B layout structure changes at 768px:** The flex layout, badge positioning, and
row structure are unchanged. No reflow of cohort rows.

**Zone 1B overflow at 768px:** Zone 1B overflow and allocation are G3 Phase 3 scope.
#1250 does NOT address Zone 1B overflow at 768px — only font sizes.

**InstrumentCluster layout at 768px:** The InstrumentCluster uses breakpoints 1024/1280/1440.
Adding a 768px breakpoint to InstrumentCluster is NOT in scope. #1250 only changes font
sizes within `CohortImpactSection`.

---

## 8. Test Authorship Obligation

**Test file:** `frontend/tests/e2e/m17-g4-demo6-critical-polish.spec.ts` — `#1250` describe block

**Implementation completeness check (Step 4 Verify):**
- Confirm `useIsNarrow()` or equivalent hook is reactive to `page.setViewportSize(768, ...)` in Playwright
- Confirm computed font size of `cohort-tier-badge-{indicator_key}` at 768px reports ≥ 10px
- Confirm no change at 1280×800

**No soft-skip patterns** (NM-056 guard): All ACs must be hard-fail assertions.
