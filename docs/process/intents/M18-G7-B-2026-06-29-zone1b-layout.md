---
name: M18-G7-B-zone1b-layout
type: implementation-intent
issues:
  - "#1460 — DEMO-131: Zone 3 expanded panel content not visible in viewport"
  - "#1462 — DEMO-133: DistributionalComparisonSummary below Zone 1C fold"
  - "#1470 — DEMO-141: TERMINAL alert above comparison summary (headline hierarchy inversion)"
  - "DEMO-149 (no GitHub issue) — PSP section clipped by governance horizon disclosure text"
status: Filed — ADR-008 Amendment 2 accepted (2026-06-29); all gates CLEAR
authored-by: Frontend Architect Agent
authored-date: 2026-06-29
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m18-g7-sprint-entry.md
adr-reference: "ADR-008 Amendment 2 — Zone 1B minimum height and comparison-session DOM order (accepted 2026-06-29)"
governing-adrs:
  - "ADR-008 Decision 5 — MDA Alert Panel Specification (Zone 1B)"
  - "ADR-008 Amendment 2 — Zone 1B min height (160px) + comparison-session DOM order"
root-cause-reference: docs/demo/m18/reviews/2026-06-29-g7-root-cause-analysis.md
release-branch: release/m18
bpo-acceptance-required: "No — bug fix restoring spec-correct behaviour"
customer-agent-l3-required: "No — layout/visibility fix, not a new capability"
---

# Implementation Intent: M18-G7-B — Zone 1B Layout Fix

> **Pre-implementation prerequisites (all required before implementation PR opens):**
> - [x] G7-0 root cause analysis filed and EL-approved (2026-06-29)
> - [x] ADR-008 Amendment 2 accepted by EL (2026-06-29) — specifies minimum height and DOM ordering
> - [ ] QA tests authored and committed (red) before implementation code

---

## 0. Implementation Constraints

*Authority: G7-0 root cause analysis §Root Cause 2 + ADR-008 Amendment 2 (accepted 2026-06-29).*

1. **DOM order for comparison sessions: distributional first.** In comparison sessions (two scenarios active), `DistributionalComparisonSummary` renders as the first child of the Zone 1B container, before `MDAAlertPanelZone1B`'s alert rows and `CohortImpactSection`. This is a conditional — single-scenario sessions retain the existing ordering (alerts first).

2. **Minimum height: 160px for DistributionalComparisonSummary.** The `DistributionalComparisonSummary` element must have a CSS `minHeight` of at least 160px in comparison sessions. This prevents the flex container from shrinking the summary below its six content elements at 1440×900.

3. **Zone 3 expanded panel: scrollIntoView after open.** When `panelOpen` transitions to `true`, call `scrollIntoView({ block: 'nearest' })` on the expanded panel content container after the render cycle. The expanded panel container must have `overflowY: 'auto'` if its content height can exceed Zone 1B allocation.

4. **DEMO-149 — governance horizon disclosure fix.** The governance horizon note in the PSP section currently renders as full text, expanding the section height and clipping the PSP value. Fix: convert the governance horizon disclosure to a tooltip (`title` attribute or hover popover) or reduce the text to a single line with an expandable affordance. The PSP value must be visible without scroll or expansion at 1440×900.

5. **No change to Zone 1B position in the instrument cluster.** Zone 1B boundaries (Decision 2), alert severity ordering within Zone 1B, and single-scenario Zone 1B behaviour are all unchanged. This intent only specifies comparison-session conditionals.

---

## 1. Source

**Issues:** #1460 (DEMO-131), #1462 (DEMO-133), #1470 (DEMO-141), DEMO-149

**Root cause document:** `docs/demo/m18/reviews/2026-06-29-g7-root-cause-analysis.md §Root Cause 2`

**Governing ADR:** ADR-008 Amendment 2 (Zone 1B minimum height + DOM ordering — accepted 2026-06-29).

**Demo 7 anchor:** Act 2 (Zambia three-scenario comparison). Zone 1B must show `DistributionalComparisonSummary` fully visible as the first element the analyst reads upon entering comparison mode — this is the primary human cost argument of Act 2 ("342,700 more people above the poverty floor under Option C").

---

## 2. Persona Trace (abbreviated — layout fix)

**Personas affected:** Persona 1 (Lucas, Programme Analyst — reads distributional differential in Act 2); Persona 2 (Eleni, Finance Ministry Negotiator — cites differential value at table); Persona 5 (Aicha, Finance Minister — reads Zone 1B summary during demo observation).

**Capability before fix:** `DistributionalComparisonSummary` is below the Zone 1C fold at 1440×900. The analyst cannot read the primary human cost finding without scrolling. The Zone 3 expanded methodology panel content is not visible even after clicking the expand toggle.

**Capability after fix:** `DistributionalComparisonSummary` is the first element visible in Zone 1B in comparison mode. All six content elements are visible without scroll. Zone 3 methodology panel scrolls into view on expansion.

---

## 3. Observable Application State

### 3.1 Primary observable state

**In comparison session (ZMB three-scenario) at 1440×900:**

`[data-testid="distributional-comparison-summary"]` has a bounding box with `bottom ≤ 900` (fully within viewport) and `height ≥ 160`. The element is the first child of the Zone 1B flex container in the DOM. MDA alert rows render below it.

### 3.2 Secondary observable states

**State A — Zone 3 panel expansion visible:**
After clicking `[data-testid="zone3-methodology-toggle"]`, the expanded panel content (`[data-testid="zone3-methodology-panel"]`) has a bounding box with `bottom ≤ 900` (fully or at least partially within viewport — scroll is acceptable but content must be reachable).

**State B — Single-scenario session unaffected:**
In a single-scenario (SEN Mode 3) session, Zone 1B renders in the original order: alerts first (`[data-testid="mda-alert-list"]`), `CohortImpactSection` below. `DistributionalComparisonSummary` is absent (not a comparison session). No regressions to existing single-scenario Zone 1B layout.

**State C — DEMO-149 PSP value visible:**
In Act 2 frames at 1440×900, `[data-testid="psp-value"]` (or equivalent) is visible without scroll. The governance horizon disclosure text does not expand the PSP section to the point of clipping the PSP numeric value.

### 3.3 Silent failure detection

**Silent failure — DOM ordering regression in single-scenario session:**
`DistributionalComparisonSummary` appears above alert rows in a single-scenario session. Observable: `distributional-comparison-summary` present before `mda-alert-list` in DOM when no comparison is active.

**Silent failure — minHeight not applied:**
`distributional-comparison-summary` rendered height < 160px in comparison session at 1440×900. Observable via bounding box check.

**Silent failure — Zone 3 panel still not scrolling into view:**
After toggle click, `zone3-methodology-panel` bounding box bottom > 900 (below fold). Observable via viewport containment check after toggle.

---

## 4. Acceptance Criteria

**AC-B1 (E2E — distributional summary in viewport at 1440×900):**
At viewport 1440×900 in comparison session with two ZMB scenarios loaded, `[data-testid="distributional-comparison-summary"]` has `boundingClientRect().bottom ≤ 900` and `boundingClientRect().height ≥ 160`. All six content elements (headcount number, CI bounds, 95% CI marker, direction-stability, T3 badge, reference label) are within the bounding box — verified by checking each child element's `bottom ≤ 900`.
*Source: §3.1 + ADR-008 Amendment 2 §Zone 1B minimum height*

**AC-B2 (E2E — distributional summary renders first in comparison session):**
In comparison session DOM, `distributional-comparison-summary` appears before `[data-testid="mda-alert-list"]` as a sibling element (or ancestor/child). The `compareDocumentPosition` of `distributional-comparison-summary` relative to `mda-alert-list` returns `DOCUMENT_POSITION_FOLLOWING` (i.e., summary is before alerts in the DOM).
*Source: §3.1 + ADR-008 Amendment 2 §Zone 1B DOM ordering*

**AC-B3 (E2E — single-scenario ordering unaffected):**
In single-scenario (SEN Mode 3) session, `mda-alert-list` appears before any non-distributional Zone 1B content. `distributional-comparison-summary` is absent from the DOM (not a comparison session).
*Source: §3.2 State B + ADR-008 Decision 5 §Severity ordering unchanged for single-scenario*

**AC-B4 (E2E — Zone 3 panel content reachable after expand):**
After clicking `[data-testid="zone3-methodology-toggle"]` in comparison session, `[data-testid="zone3-methodology-panel"]` is present in the DOM with non-zero dimensions. At least the top portion of the panel (`boundingClientRect().top < 900`) is within the viewport.
*Source: §3.2 State A + ADR-008 Amendment 2 §Zone 3 expanded panel scrollability*

**AC-B5 (E2E — PSP section not clipped, DEMO-149):**
In Act 2 comparison mode at 1440×900, `[data-testid="psp-value"]` (or equivalent PSP numeric display element) has `boundingClientRect().bottom ≤ 900` and is not occluded by the governance horizon disclosure text. The governance horizon disclosure renders as a single line or tooltip — not a multi-line block pushing the PSP value out of view.
*Source: §0 Constraint 4 + DEMO-149*

---

## 5. Kryptonite Constraint Check

No new kryptonite risk introduced by this fix. The DOM reordering is conditional on comparison sessions — single-scenario sessions are unchanged. Risk of regression: if the comparison-session conditional is implemented incorrectly, single-scenario Zone 1B ordering may be affected. AC-B3 guards against this regression.

---

## 6. Visual Spec (before / after)

**Before (DEMO-133 failure state — comparison session at 1440×900):**
```
Zone 1B (flex column):
  ├── [MDA alert: TERMINAL — bottom_quintile_formal...] ← visible, occupies ~200px
  ├── [CohortImpactSection rows]                         ← visible, occupies ~240px
  └── [DistributionalComparisonSummary]                  ← BELOW FOLD (at y > 900)
```

**After (fixed — comparison session at 1440×900):**
```
Zone 1B (flex column):
  ├── [DistributionalComparisonSummary]  minHeight:160px ← FIRST, FULLY VISIBLE
  │     ├── +342,700 persons
  │     ├── [260,400 – 424,100] 95% CI
  │     ├── Direction: stable improvement
  │     ├── T3 confidence badge
  │     └── vs. Reference: Option A
  ├── [MDA alert: TERMINAL — ...]                        ← below, still visible
  └── [CohortImpactSection rows]                         ← below
```

---

## 7. Out of Scope

- Zone 1B height in single-scenario sessions (unchanged)
- MDA alert severity ordering (unchanged — TERMINAL before CRITICAL before WARNING within alerts)
- Zone 1B to Zone 1C boundary position (unchanged)
- `DistributionalComparisonSummary` visual design beyond minHeight (content layout unchanged)

---

## 8. Test Authorship Obligation

**QA file:** `frontend/tests/e2e/demo-zone1b-layout.spec.ts` (new file)

**Test authorship deadline:** E2E tests authored and committed to `feat/m18-g7-cluster-b` BEFORE implementation code changes. Tests must run red before fix, green after.

| AC | Test type | Playwright check |
|---|---|---|
| AC-B1 | E2E viewport | `distributional-comparison-summary` bounding box fully within 1440×900 |
| AC-B2 | E2E DOM order | `compareDocumentPosition` check: summary before alerts |
| AC-B3 | E2E regression | Single-scenario: alerts first, distributional absent |
| AC-B4 | E2E expansion | Zone 3 panel top < 900 after toggle click |
| AC-B5 | E2E viewport | PSP value visible at 1440×900, not clipped |

**Pre-push gates:** `cd frontend && npm run build` must exit 0.

*Filed: 2026-06-29. Authority: docs/process/agents.md §Frontend Architect Agent.*
