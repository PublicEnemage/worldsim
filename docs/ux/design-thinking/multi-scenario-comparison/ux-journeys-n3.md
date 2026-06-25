# UX Journeys — Multi-Scenario Comparison (N=3)

> **Artifact 1 of G2 Phase 1 design sprint**
> **Authored by:** UX Designer Agent
> **Date:** 2026-06-25
> **Issue:** #394 — feat: multi-scenario comparison (>2 scenarios)
> **Authority:** `docs/process/intents/M17-G2-2026-06-25-multi-scenario-design.md §3.1`
> **Governing documents:** `docs/ux/information-hierarchy.md`, `docs/ux/north-star.md`,
> `docs/ux/personas.md §Persona 1, §Persona 3, §Persona 5`,
> `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md`

---

## Purpose

This document specifies the three journeys required for the N=3 multi-scenario comparison
capability (Issue #394). It is the primary design input for G2 Phase 2 architecture assessment
(Artifact 3) and the G2 Phase 3 implementation-intent document. The design is grounded in the
Demo 7 Act 2 scenario: Zambia (ZMB) — three IMF restructuring options compared simultaneously.

**Three scenarios (Demo 7 Act 2 — ZMB):**

| Label | Name | Conditionality character |
|---|---|---|
| Option A | Extended Fund Facility — Front-Loaded | Aggressive primary surplus target; front-loaded spending cuts; minimal social protection carve-out |
| Option B | EFF with Social Protection Carve-Out | Same surplus target; phased cuts; explicit Q1 expenditure floor through step 4 |
| Option C | Homegrown Programme — Gradual Adjustment | 2% lower primary surplus target; 12-month delayed implementation; maintains social expenditure |

---

## Journey 1 — Scenario Setup

**Cognitive task:** Transition from N=2 comparison (existing capability) to N=3 comparison
without navigating away from the instrument cluster.

### Entry State

The analyst has loaded Option A and Option B into Mode 2 COMPARE_VIEW using the existing
"Compare against..." mechanism in Zone 2. The primary viewport shows two scenario curves in
Zone 1A. The Zone 2 scenario browser shows both loaded scenarios and the "×" (close comparison)
control.

### Step Sequence (minimum required — three steps)

**Step 1 — Trigger "Add third scenario"**

From the existing N=2 COMPARE_VIEW state, an "Add third scenario" button appears below the
"×" close comparison control in the Zone 2 scenario browser. This button is visible only when
`comparisonScenarios.length === 2` and the current entity has at least one additional scenario.
The button is labeled "Add third scenario" (not "Add comparison" — specificity matters for Aicha's
analyst, who must set this up before Aicha reads it).

The user clicks "Add third scenario." The inline fixture list expands within Zone 2, listing
available scenarios for the same entity (ZMB). Scenarios already in the comparison are
shown as disabled with a checkmark indicator ("already in comparison").

**Step 2 — Select the third scenario**

The analyst selects "Option C — Homegrown Programme" from the inline list. The list closes.
Zone 2 now shows three scenario rows (Option A, Option B, Option C) with:
- The active/primary scenario indicated by a solid left-border (Option A — the "baseline")
- Comparison scenario indicators for Option B and Option C

**Step 3 — Zone 1A updates to N=3 rendering**

Zone 1A re-renders with three scenario curves using the N=3 differentiation scheme (see
Journey 2). Zone 1B updates to show per-scenario threshold crossing rows (see Journey 3).
Zone 1D updates to show three PSP values. No navigation away from the primary viewport
occurs at any step.

**Exit state:** Three scenarios active. Zone 1A shows N=3 curves. Zone 1B shows per-scenario
threshold crossings. Zone 1D shows per-scenario PSP. The analyst is in N=3 COMPARE_VIEW.

### Maximum N supported

**N=3 confirmed.** N=5 is the design target (the differentiation scheme below scales to N=5).
N>5 is explicitly deferred — at N>5, Zone 1A enters legibility-limit notice mode consistent
with the existing N>4 entity legibility limit (per ARCH-REVIEW-007 §Q3 decision).

### Zone 1D entity attribution with three active scenarios

When three scenarios are active (all for the same entity, ZMB), Zone 1D's entity attribution
header reads: "ZMB — Zambia (3 scenarios)." The four-framework current position values shown
in Zone 1D are those of the **primary scenario** (Option A, the baseline). A scenario selector
within Zone 1D allows the analyst to switch the Zone 1D readout to any of the three scenarios
for deeper framework inspection. The per-scenario PSP is shown separately below the four
framework values (see Journey 2, Zone 1D PSP).

---

## Journey 2 — Primary Viewport in Comparison Mode

**Cognitive task:** Read which of three scenario trajectories is diverging from the others
at the current step, and which is at risk of crossing an MDA threshold.

### Zone 1A — N=3 Differentiation Scheme

**The problem:** Three composite score trajectories for the same entity (ZMB) must be
simultaneously legible at 1280×800 (Demo 7 presentation) and at 768px (tablet legibility,
DEMO6-026/043 constraint). A color-only differentiation fails accessibility. A line-style-only
differentiation fails at small viewports (line style is too fine at 768px). The solution
is a **triple-channel** differentiation strategy.

#### Triple-channel strategy (committed design decision)

| Scenario | Color | Line style | Stroke width | Terminal label |
|---|---|---|---|---|
| Option A (baseline) | Steel Blue `#2563EB` | Solid | 2px | "A" |
| Option B | Amber Orange `#D97706` | Dashed `8 2` | 2px | "B" |
| Option C | Forest Green `#16A34A` | Dotted `2 4` | 2px | "C" |

**Why these colors:**
- Steel Blue, Amber Orange, Forest Green are distinguishable by the three most common
  color vision deficiencies (deuteranopia, protanopia, tritanopia) when combined with
  line-style differentiation. They do not overlap with the four framework colors
  (`#2271B3` financial, `#1A8FA0` ecological, `#D4841A` human_development, `#7B50A8`
  governance) — though Steel Blue and the financial blue are in the same hue family,
  the saturation difference and the line-style channel prevent confusion.
- Line-style differentiation (solid / dashed / dotted) provides the primary
  accessibility fallback — it distinguishes the three scenarios without color.
- Terminal endpoint labels ("A", "B", "C") provide the primary identification anchor
  at the end of the step window; no hover required.

**Legibility at 1280×800:** At 1280×800, the Zone 1A trajectory view occupies approximately
580×300px. Three curves with distinct color and line-style differentiation are legible within
this area. Terminal endpoint labels positioned with dynamic y-offset (per ARCH-REVIEW-007 Open
Question (d) decision) ensure labels do not overlap at convergence points.

**Legibility at 768px:** At 768×1024 (tablet), the Zone 1A view narrows to approximately
480×240px. At this viewport, terminal endpoint labels must be at least 9px font. The dashed
and dotted line styles are legible at 2px stroke on retina and 2x displays, but may merge
on standard-DPI tablets. Color differentiation becomes the primary channel at small viewports.
The triple-channel strategy is therefore **additive**: color at all viewports; line-style on
retina/2x; label on all viewports. No single channel alone guarantees legibility — the
combination does.

**Scaling to N=5:** The design scales to N=5 with the following extension:
- Option D: Purple `#7C3AED`, `strokeDasharray="12 4"` (long dash), terminal label "D"
- Option E: Rose `#E11D48`, `strokeDasharray="2 2 8 2"` (dash-dot), terminal label "E"

At N=5, the Zone 1A view approaches the legibility ceiling. The same legibility-limit notice
mechanism used at N>4 entities applies at N>5 scenarios — the notice reads: "5 scenarios
displayed. Add or remove scenarios in the comparison panel." N=5 is confirmed within the
legibility boundary; N>5 triggers the notice.

#### MDA floor lines in N=3 comparison mode

In N=3 scenario comparison, the MDA floor lines are drawn **once** (per framework / per
indicator) regardless of how many scenarios are active. The floor is a property of the entity
and the indicator, not of the scenario. The MDA floor line style is a horizontal dashed gray
`#6B7280` at 1px stroke — visually distinct from all three scenario curve styles.

#### Relationship to #1249 (N=2 curve identifiability fix)

The N=3 differentiation scheme builds on the N=2 fix from #1249 (Zone 1A curve identifiability,
DEMO6-014). The N=2 fix establishes terminal endpoint labels and line-style differentiation
for two scenarios. The N=3 scheme extends this framework with a third color/line-style slot.
G2 Phase 3 implementation PR should not open until #1249 is merged — the N=2 fix is the stable
base that N=3 builds on, not a concurrent development.

### Zone 1B — Per-Scenario Threshold Crossing Display (committed)

**Decision: Per-scenario (option (a)).**

Rationale: Aicha's 90-second question is "which option avoids Q1 CRITICAL?" This question
requires scenario attribution — she must be able to identify Option C as the safe option by
reading Zone 1B. A union display (all crossings merged without per-scenario grouping) would
require her to parse the scenario label from each row independently, which is two cognitive
steps. Per-scenario display groups all crossings under their scenario header, reducing the
read to a single scan.

**Per-scenario Zone 1B layout (N=3 comparison mode):**

```
Zone 1B | Threshold crossings — ZMB Mode 2, Step 4
─────────────────────────────────────────────────────────────────
▶ Option A [■ solid blue]
  CRITICAL  Q1 Poverty headcount — crossed step 2
  WARNING   Health system capacity — crossed step 3

▶ Option B [▪ dashed orange]
  CRITICAL  Q1 Poverty headcount — crossed step 3
  WARNING   School enrollment rate — crossed step 3

▶ Option C [● dotted green]
  [no crossings through step 8]
─────────────────────────────────────────────────────────────────
MDA alert count: 4 (Option A: 2 · Option B: 2 · Option C: 0)
```

Each scenario header includes its color-coded indicator (the same color dot/dash/square used
in Zone 1A). Crossing rows show: severity, indicator name (human-readable), and step of first
crossing. The scenario with no crossings shows an explicit "[no crossings through step N]"
line — not a blank — to distinguish "no crossings" from "not yet computed."

**Relationship to G3 (Zone 1B proportional allocation, #1252):**

The N=3 Zone 1B per-scenario display occupies more vertical space than the N=2 display.
When all three scenarios have crossings, the total Zone 1B content height is approximately
3× the single-scenario height. This creates a conflict with the Zone 1B MDA alert panel
minHeight guarantee (current: `minHeight: 80px`). The G3 sprint (Zone 1B proportional
allocation, #1252) must specify the layout contract when both the MDA alert panel and
per-scenario crossing rows populate Zone 1B simultaneously. G2 Phase 3 must not override
the `minHeight: 80px` MDA panel guarantee — if the per-scenario rows would collapse the
alert panel below 80px, they must scroll within a bounded container, not compress the alert panel.
This is a G3 dependency: G2 Phase 3 implementation notes this constraint but defers the
proportional allocation resolution to G3.

### Zone 1D — Per-Scenario PSP (committed)

**Decision: Per-scenario (option (a)) — three PSP values displayed simultaneously.**

Rationale: Andreas (Persona 3) needs to read all three programme survival probabilities
in a single Zone 1D scan. A single active-scenario display (option (b)) would require
him to switch between scenarios, holding three values in memory — a failure condition
for his use case (Persona 3 §Failure Mode: "requires interpretation by an economist").

**Per-scenario PSP layout in Zone 1D (N=3 comparison mode):**

The Zone 1D panel's existing "Programme Survival Probability" row becomes a comparison table
when N=3 comparison is active:

```
Zone 1D | Four-Framework Current Position — ZMB, Step 4

Financial      [Option A: 0.61] [Option B: 0.63] [Option C: 0.57]
Human Dev.     [Option A: 0.48] [Option B: 0.54] [Option C: 0.68]
Ecological     [Option A: 0.72] [Option B: 0.72] [Option C: 0.72]
Governance     [Option A: 0.55] [Option B: 0.58] [Option C: 0.61]

Programme Survival Probability:
  Option A  [■]  58%
  Option B  [▪]  67%
  Option C  [●]  74%
```

The PSP row expands to three lines when N=3 comparison is active. Each line carries the
scenario color indicator and label. The PSP values are the `political_economy.indicators.
programme_survival_probability` output per scenario (per `docs/schema/api_contracts.yml
§DA-G5-4`).

The four-framework composite values at the top of Zone 1D show per-scenario columns when
N=3 is active. This is a table extension of the existing Zone 1D readout — each cell shows
three values (one per scenario). If viewport width does not accommodate a full three-column
table, the four-framework rows collapse to show only the primary scenario's values with an
indicator "(3 scenarios — see comparison)" and the PSP comparison block remains expanded.

---

## Journey 3 — Threshold Comparison (Aicha's 90-second read)

**Cognitive task:** Identify which scenario avoids Q1 poverty headcount CRITICAL crossing
at step 4 without narration, within 90 seconds, from the primary viewport alone.

### Kryptonite check (applied)

The following interactions are prohibited under the kryptonite constraint for Aicha's
Reactive entry state (90-second ceiling):

- ❌ Opening a drawer to see per-scenario Zone 1B threshold crossings
- ❌ Hovering over Zone 1A curves to read scenario labels
- ❌ Navigating between scenario views in Zone 1D to compare PSP values

The Zone 1A + Zone 1B composite visible at the primary viewport at step 4 must answer
Aicha's question — "which option is least harmful to Q1?" — without any of these interactions.

**Confirmation:** The design as specified satisfies the kryptonite constraint. Zone 1A
terminal endpoint labels ("A", "B", "C") identify each curve at glance level without hover.
Zone 1B per-scenario grouping shows Option C's "[no crossings]" status at a glance without
any interaction. Zone 1D PSP three-value block is visible without switching views.

### Literal text block (AC-5 requirement)

The following block shows exactly what Aicha sees at step 4 of the ZMB Mode 2
three-scenario comparison, with Q1 poverty headcount trajectory active. This is
the **normative specification** — the Phase 3 implementation must produce a display
from which a QA reviewer can confirm "Aicha can identify Option C as the least
harmful choice without narration."

#### Viewport: 1280×800 | Zone 1A and Zone 1B as they appear on screen simultaneously

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Zone 1A  |  ZMB — Zambia  |  Mode 2 — Simulation  |  Step 4 of 8              │
│  data-testid="zone-1a-trajectory"                                               │
│                                                                                 │
│  1.0 ┤                                                                          │
│      │                                                              ● C  0.72   │
│  0.8 ┤                                                                          │
│      │  ╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶  (MDA floor 0.60) ╶╶╶╶╶            │
│  0.6 ┤                              ▪ B  0.59                                  │
│      │                    ■ A  0.58                                             │
│  0.4 ┤                                                                          │
│      │                                                                          │
│  0.2 ┤                                                                          │
│      └──────────────────────────────────────────────────────────                │
│        Step 1    Step 2    Step 3    Step 4    Step 5    Step 6                  │
│                                                                                 │
│  ■ Option A (solid blue)  ▪ Option B (dashed orange)  ● Option C (dotted grn)  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│ Zone 1B  |  Threshold Crossings                                                 │
│  data-testid="zone-1b-mda-alerts"                                               │
│                                                                                 │
│  ▶ Option A  [■ solid blue]                                                     │
│    CRITICAL  Q1 Poverty headcount — crossed step 2                              │
│    WARNING   Health system capacity — crossed step 3                            │
│                                                                                 │
│  ▶ Option B  [▪ dashed orange]                                                  │
│    CRITICAL  Q1 Poverty headcount — crossed step 3                              │
│    WARNING   School enrollment rate — crossed step 3                            │
│                                                                                 │
│  ▶ Option C  [● dotted green]                                                   │
│    [no crossings through step 8]                                                │
│                                                                                 │
│  data-testid="zone-1b-threshold-row-scenario-{id}" (per row)                   │
│  data-testid="zone-1b-scenario-header-{id}" (per scenario header)              │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**QA reviewer confirmation:** From this block, a reviewer can confirm: "Aicha can identify
that Option C avoids Q1 poverty headcount crossing through step 8, while Options A and B
both cross CRITICAL (at step 2 and step 3 respectively), by reading Zone 1A (terminal label
'C' at 0.72, above the MDA floor dashed line at 0.60) and Zone 1B (Option C: '[no crossings
through step 8]') from the primary viewport without narration, in under 90 seconds."

### data-testid anchor specification (Phase 3 implementation contract)

These anchors are committed design decisions. Phase 3 implementation must use these exact
`data-testid` values. The QA Lead authors Playwright tests against these anchors.

**Zone 1A scenario curve anchors:**
- `data-testid="zone1a-curve-scenario-{scenarioId}"` — SVG path element per scenario curve
  (e.g., `zone1a-curve-scenario-option-a`, `zone1a-curve-scenario-option-b`)
- `data-testid="zone1a-terminal-label-scenario-{scenarioId}"` — endpoint label per scenario
  (e.g., `zone1a-terminal-label-scenario-option-a`)
- `data-testid="zone1a-mda-floor-line"` — MDA floor horizontal dashed line (existing anchor
  must be preserved from #1249)

**Zone 1B per-scenario row anchors:**
- `data-testid="zone1b-scenario-header-{scenarioId}"` — scenario group header row
- `data-testid="zone1b-threshold-row-scenario-{scenarioId}"` — each threshold crossing row
  within a scenario group (may have multiple rows per scenario)
- `data-testid="zone1b-no-crossings-{scenarioId}"` — the "[no crossings through step N]"
  element when a scenario has no crossings

**Zone 1D PSP anchors:**
- `data-testid="zone1d-psp-row-scenario-{scenarioId}"` — PSP value row per scenario
- `data-testid="zone1d-psp-value-{scenarioId}"` — the numerical PSP value element

---

## Viewport degradation analysis (AC-2 / §3.2 requirement)

**1280×800 (primary presentation):** Full N=3 display as specified above. Zone 1A, Zone 1B
(per-scenario), and Zone 1D (PSP three-value block) are all simultaneously visible. No
content collapse required.

**768px (tablet legibility):** Zone 1A narrows. At 768px, the Zone 1A trajectory view
occupies approximately 480×240px. Three curves are legible with the triple-channel strategy.
Terminal endpoint labels must be at least 9px font (existing Zone 1A label minimum per
DEMO6-026 fix from #1250). Zone 1B per-scenario rows must not collapse — each scenario
header and crossing rows remain visible. Zone 1D PSP block must not drop below its own
Zone 1 requirement.

**Degradation at 768px:** The primary failure mode at 768px is Zone 1B content overflow
when all three scenarios have crossings. The G3 proportional allocation (#1252) must specify
the scrollable container boundary for Zone 1B at 768px. Until G3 is merged, the `minHeight:
80px` MDA panel guarantee plus `overflow-y: auto` on the per-scenario crossing rows is the
minimum acceptable behavior.

**1024×768 (tablet minimum per information-hierarchy.md):** Same constraints as 768px.
No Zone 1 instrument may be hidden at this viewport. If Zone 1D PSP block cannot fit
without scrolling at 1024×768, a condensed single-row PSP summary ("PSP: A:58% B:67% C:74%")
replaces the expanded three-row block.

---

## COMPARE_VIEW architectural position statement (AC-6 requirement)

The UX Designer's assessment of the rendering architecture impact of this design:

**The proposed N=3 differentiation strategy operates within the existing compare-mode overlay
contract.** It does not require changes to the composite_score rendering path.

Reasoning:
1. The Zone 1A curves in N=3 comparison mode are composite score curves — one per scenario
   per step, using the existing `composite_score` field per ARCH-REVIEW-007 Open Question (c)
   decision. The aggregation formula is unchanged.
2. The visual differentiation (color + line-style + terminal label) is applied in the overlay
   layer, not in the core rendering path. The existing `TrajectoryView` already assigns color
   from `ENTITY_PALETTE` and line-style from `comparisonMode` for N=2. N=3 extends this
   by: (a) introducing a `SCENARIO_PALETTE` distinct from `ENTITY_PALETTE`, and (b) expanding
   `comparisonMode: boolean` to `comparisonScenarios?: string[]` (or equivalent) that carries
   the ordered scenario list and their visual assignments.
3. The Recharts multi-line rendering already draws N lines from N datasets — the `entityTrajectories`
   prop demonstrates this for entity-level comparison. Scenario-level comparison uses the same
   rendering path with scenario-keyed data instead of entity-keyed data.
4. **What requires structural change:** The data contract for Zone 1B per-scenario threshold
   crossings may require a new backend data structure (see below). The composite score rendering
   path does not.

**What is uncertain (to be confirmed by Architect in Phase 2):**

The existing `threshold_crossings` field in the compare endpoint (delivered in G9, PR #1201)
was designed for N=2 comparison. Whether it can be extended to per-scenario crossing attribution
for N=3 via client-side composition, or whether a new backend structure is required, is an
architectural question the UX Designer cannot definitively answer. The frontend UX design
assumes per-scenario threshold crossing data is available per scenario — the source of that
data (extended compare endpoint vs. N separate trajectory calls) is a Phase 2 determination.

The UX Designer's position: the frontend rendering of per-scenario Zone 1B rows is within
the existing component boundary. The data contract for those rows may or may not require a
new backend endpoint. This distinction determines whether Phase 3 includes a backend change.

---

## G3 dependency notation (§6 / out of scope boundary)

The G2 N=3 Zone 1B per-scenario display contract creates the following dependency on G3
(Zone 1B proportional allocation, #1252):

- When three scenarios each have 2–3 threshold crossings, Zone 1B may contain 6–9 crossing
  rows plus 3 scenario headers. This content height exceeds the current Zone 1B layout
  assumptions (designed for a single alert panel, not per-scenario grouped rows).
- G3 must resolve: what is the proportional allocation between the MDA alert summary panel
  and the cohort/per-scenario crossing section when both are populated simultaneously?
- G2 Phase 3 cannot finalize the Zone 1B overflow behavior without G3's proportional
  allocation decision. The minimum acceptable G2 Phase 3 behavior: per-scenario crossing
  rows in a bounded scrollable container below the MDA alert panel, `minHeight: 80px`
  on the alert panel guaranteed.
- G3 is not a blocker for G2 Phase 3 implementation *start* — G3 is a blocker for G2 Phase 3
  production readiness in scenarios where Zone 1B is fully populated. The sprint plan FA
  constraint (G2 Phase 3 after #1249; G3 before #394 final) applies.

---

*UX Designer Agent — 2026-06-25. G2 Phase 1 Artifact 1. Issue #394.*
*Reviewed against: `information-hierarchy.md §Zone 1, §COMPARE_VIEW Mode 2 Single-entity`,*
*`north-star.md §Primary Cognitive Tasks by Mode`, `personas.md §Persona 1, §Persona 3, §Persona 5`.*
*Kryptonite check applied and passed. data-testid anchors committed.*
