# ADR-014: Alert Panel (Zone 1B) — Master-Detail Layout

> **Reader Orientation:** This ADR governs the Zone 1B layout architecture for M13 forward.
> Read it before: modifying `MDAAlertPanelZone1B.tsx`, changing `AlertDetailPanel` placement,
> adjusting Zone 1B height allocation in `InstrumentCluster.tsx`, or adding sub-zone content
> to the alert panel. G7 (#852) implementation is gated on this ADR's acceptance.

## Tier Classification

**Tier:** 1

**Justification:**
This ADR modifies Zone 1B — a co-primary instrument in Zone 1 (no interaction required).
It changes the layout architecture of the alert panel's detail surface, directly affecting
the visible-without-scroll guarantee that Zone 1 instruments must satisfy per
`docs/ux/information-hierarchy.md §Zone 1`. A detail panel rendered below the fold
in Zone 1B is a Zone 1 integrity failure — the instrument has demoted its own co-primary
status by requiring scroll to complete the primary read task.

**Sections required by tier:**

| Section | Required? |
|---|---|
| Persona Trace (7-element) | Required |
| UX Implication Statement (7-element) | Required — UX Designer sign-off |
| Forward Trace Statement | Not applicable |
| Silent Failure Mode | Required |
| Asymmetry Assessment | Not applicable (layout ADR — no analytical capability) |
| North Star Test | Required |
| Mission Impact Statement | Required |

---

## Status

`Proposed`

---

## Validity Context

> *Fill in when the ADR is accepted. Leave blank at Proposed.*

**Standards Version:** 2026-06-12
**Valid Until:** M14 close, or when Zone 1B height allocation changes, or when AlertDetailPanel content scope expands beyond current fields
**License Status:** `PROPOSED`

**Panel:**
- Architect Agent (R — authorship, component interface contracts, layout architecture)
- Frontend Architect Agent (C — React component structure, viewport behavior, layout mechanics)
- UX Designer Agent (C — UX implication statement; sign-off required before acceptance vote)
- Engineering Lead (A — accountable on all ADR decisions)

**Renewal Triggers:**
- Zone 1B height allocation in `InstrumentCluster.tsx` changes by more than 10%
- AlertDetailPanel content scope expands (new fields added beyond sparkline, snapshot, causal attribution)
- A new alert severity level (e.g., ADVISORY) is added below WARNING
- Zone 1B is split between Mode 2 and Mode 3 into separate components
- The master panel's "top N" display count changes from 3

---

## Date

2026-06-12

---

## Context

### Background

Zone 1B is the MDA Alert Panel, designated a co-primary instrument in Zone 1. The Zone 1
contract from `docs/ux/information-hierarchy.md` is: top 1–3 alerts visible without scrolling
at all supported viewports; the user must be able to complete the primary cognitive task from
Zone 1 alone.

The current implementation (`MDAAlertPanelZone1B.tsx`) renders the sorted alert list and then
appends `AlertDetailPanel` below the list in a stacked layout. When 3 alerts fill the visible
area and the user selects one, the detail panel renders below the fold of Zone 1B's container
and requires scroll to read. The component's own comment documents this: *"Scroll into view on
mount — Zone 1B is ~135px tall so the detail panel renders below the fold when 3 alerts already
fill the visible area (#814)."*

This stacked layout breaks the Zone 1 contract. The alert detail (sparkline, current vs. floor,
consecutive breach count) is the evidence Persona 2 needs to formulate the argument at Journey B
Step 4 — it is not Zone 2 content. Pushing it below the fold converts Zone 1B from a
zero-interaction instrument into a one-scroll instrument, which is the definition of Zone 2.

IR findings DEMO-042 (scrollable unsorted list) and DEMO-043 (detail below fold) documented
this as a Zone 1 legibility defect at the M12 demo cycle. Issue #852 specifies the fix:
master-detail pattern.

### Problem Framing

In Journey B Step 3 (Reactive entry state, 90-second total ceiling, 5-second read ceiling per
the journey spec), Persona 2 selects the top CRITICAL or TERMINAL alert to read its detail.
Under the current stacked layout, the `AlertDetailPanel` renders below the 3 alert rows that
already fill Zone 1B's visible area. Reading the detail requires a scroll that Journey B Step 3
does not budget. Persona 2 can see that a threshold was crossed — she cannot see the evidence
(breach count, approach to floor, sparkline) within the 5-second window.

The consequence at a negotiating table: she can say "there is a CRITICAL breach" but not
"this threshold has been breached for N consecutive steps at X% below floor." The second
statement is the negotiating instrument. The first is a status report.

---

## Decision

Zone 1B adopts a master-detail layout. The outer container is split into two fixed-height
sub-zones stacked vertically, always simultaneously visible, with no reflow on selection.

### Layout Architecture

**Zone 1B outer container:**
```
display: flex
flex-direction: column
height: 100%          (fills Zone 1B allocation from InstrumentCluster)
overflow: hidden      (sub-zones manage their own scroll independently)
```

**Zone 1B-master (alert list sub-zone):**
```
flex: 0 0 auto        (fixed height — does not shrink or grow)
height: ~60% of Zone 1B allocation (implementation: pixel or percentage — verified at all viewports)
overflow-y: auto      (only if alerts exceed visible space; top 1-3 visible without scroll)
```

The master sub-zone renders the severity-sorted alert rows (TERMINAL → CRITICAL → WARNING,
then ascending step_index within severity). Top 3 rows visible at minimum desktop viewport
(1280×800) without scroll. "+N more" indicator renders below the visible rows in the master
sub-zone (scrollable — not a Zone 1 requirement).

**Zone 1B-detail (alert detail sub-zone):**
```
flex: 1               (fills remaining Zone 1B height)
overflow-y: auto
```

The detail sub-zone is **always rendered**. When no alert is selected, it shows a placeholder:
`"Select an alert to view details."` in `color: #aaa; font-size: 11px; font-style: italic`.
When an alert is selected (`focusedAlertMdaId` is non-null), it renders `AlertDetailPanel`
for the selected alert. `AlertDetailPanel` is **removed from its current inline position**
below the master list and relocated exclusively into Zone 1B-detail.

### Component Interface Changes

`MDAAlertPanelZone1B` outer `div` style:
- Before: `overflowY: "auto"; height: "100%"`
- After: `display: "flex"; flexDirection: "column"; height: "100%"; overflow: "hidden"`

New inner `div` for Zone 1B-master:
- `data-testid="zone-1b-master"`
- `style={{ flex: "0 0 auto", overflowY: "auto" }}`
- Height: `60%` of Zone 1B allocation (confirmed as fitting ≥3 compact rows or ≥2 full-density rows at 1280×800)

New inner `div` for Zone 1B-detail:
- `data-testid="zone-1b-detail"`
- `style={{ flex: 1, overflowY: "auto", borderTop: "1px solid #eee" }}`
- Renders `AlertDetailPanel` or placeholder

`AlertDetailPanel` scroll-into-view `useEffect` (line 162–163 of current implementation)
is removed — detail panel no longer needs to scroll into view because it is always in view.

### Invariants

1. Zone 1B-master height does not change when an alert is selected — no reflow.
2. Zone 1B-detail is always visible in the Zone 1B bounds — no scroll required to reach it.
3. Top TERMINAL and CRITICAL alert rows remain visible in Zone 1B-master without scroll at
   1440×900, 1280×800, and 1024×768.
4. The alert row click behavior (select / deselect toggle) is unchanged.
5. Compact (240px) and full-density (400px+) row formats within Zone 1B-master are unchanged.
6. `+N more` indicator remains in Zone 1B-master below visible rows — it is inside the
   master's scrollable area, not a separate element.

### Viewport Verification Requirement

Before the G7 implementation PR is marked ready for review, the implementing agent must
confirm the following at all three viewports using a live application observation (Playwright
or screen recording):
- At 1440×900: Zone 1B-master shows ≥3 alert rows; Zone 1B-detail shows detail or placeholder
  without scroll; total Zone 1B height does not change when alert is selected or deselected.
- At 1280×800: same as 1440×900.
- At 1024×768 (compact mode): Zone 1B-master shows ≥2 compact rows; Zone 1B-detail visible.

---

## Persona and UX Traceability

### [Tier 1] Persona Trace

**P-1 — Persona identification:**
Primary: Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou archetype).
Secondary: Persona 3 — Political Advisor (Andreas Stefanidis archetype) — also operates in
reactive state at negotiating table and has the same 5-second ceiling for alert detail.

**P-2 — Entry state:**
Reactive entry state (90-second total ceiling, negotiation room context). Journey B Step 3
establishes a 5-second ceiling for the alert read — severity, indicator name, and breach
evidence must all be readable within 5 seconds of the alert being selected, without scroll.

**P-3 — Journey reference:**
- Journey B Step 3 — "Scan: read the top MDA alert" — 5-second ceiling for severity,
  indicator, step, cohort. This ADR extends the 5-second ceiling to also cover the detail
  pane (sparkline, current vs. floor, consecutive breach count) — the detail is the evidence
  that converts a status read into a negotiating argument.
- Journey B Step 4 — "Cite: formulate the argument" — the detail evidence (consecutive breach
  count, approach pct, sparkline direction) is the raw material for the citation.
- Journey C Step 3 — MDA alert panel fires with causal attribution. The detail pane shows
  "Caused by: [policy input]" when in Mode 3.
- Closes DEMO-042 and DEMO-043 (IR findings from M12 demo cycle).

**P-4 — Time or interaction ceiling:**
Alert detail visible within 5 seconds of selecting the alert row, at 1440×900, without scroll.
(Journey B Step 3 sets the 5-second ceiling for the full alert read including detail.)
One click to select an alert → detail immediately visible in Zone 1B-detail. Zero additional
interactions required.

**P-5 — Income cohort served:**
Zone 1B MDA alerts are cohort-tagged (the `cohort` field on `Zone1BAlert`). The master layout
change does not affect cohort disaggregation — cohort is displayed in the alert row (compact:
truncated; full-density: full). Per-cohort income quintile breakdown (bottom two quintiles,
pensioners 65+, etc.) is Zone 2 content — accessible via FrameworkPanel after the alert scan.
This ADR does not extend or constrain cohort coverage.

**P-6 — Negotiating leverage statement:**
After this layout change, Persona 2 can make the following specific argument within the
5-second reactive window:
> "The CRITICAL alert for reserve coverage has been active for 3 consecutive steps. Current
> value is 2.1 months below the CRITICAL floor. At the current draw rate, the trajectory
> breaches the irreversible floor at step 5. This is not a one-period anomaly — it is a
> structural drawdown. The proposed adjustment timeline does not account for this."

Under the stacked layout, this argument requires a scroll to reach the consecutive breach count
and sparkline. Under the master-detail layout, it is readable in the fixed detail pane
immediately on alert selection.

**P-7 — North star test answer:**
A Zambian finance minister's lead analyst is in a live debt restructuring session. Reserve
coverage has crossed the CRITICAL threshold. She clicks the top CRITICAL alert in Zone 1B.
Under the current stacked layout, the `AlertDetailPanel` renders below the three alert rows
already visible — she must scroll to read the consecutive breach count and sparkline. In a
90-second reactive window with IMF counterparts watching the screen, that scroll is not
available. She can see "CRITICAL — reserve coverage" and say it crossed a threshold. She
cannot say for how many steps it has been below floor, or show the trajectory direction.

Under the master-detail layout: she clicks the alert, the detail pane is immediately visible
in the fixed lower zone without any scroll. She reads: "3 consecutive steps below CRITICAL
floor, approach 18% remaining, sparkline showing continued decline." She says at the table:
"This threshold has been below floor for three consecutive steps — under your proposed
timeline, it reaches irreversible territory at step 5. We need a different adjustment path."

The IMF team's analysts have this same information in their monitoring tools without a
legibility constraint. This ADR closes the UI legibility gap that was the only reason
Persona 2 could not access evidence that was already present in the data.

---

### [Tier 1] UX Implication Statement

**UX-1 — Zone assignment and hierarchy certification:**
This ADR places the alert detail surface in Zone 1B (co-primary, no interaction required to
reach). The detail surface currently occupies Zone 1B-overflow (requires scroll — effectively
Zone 2 positioning despite Zone 1 data). This ADR restores the detail surface to its intended
Zone 1 position by assigning it a fixed sub-zone within the Zone 1B allocation.
Assignment is consistent with `information-hierarchy.md §1B` requirement: "top 1–3 alerts
visible without scrolling." The detail sub-zone is a logical extension of this requirement —
alert detail is evidence that belongs with the alert row, not downstream of it.

**UX-2 — Primary cognitive task alignment:**
- Mode 1 (trajectory reconstruction): alert detail shows historical breach evidence — sparkline
  over historical steps, consecutive breach count at the step where threshold was crossed.
  Supports the reconstruction task without navigating away from Zone 1.
- Mode 2 (threshold-safe path construction): alert detail shows projected threshold approach —
  approach_pct_remaining and sparkline direction confirm whether the projected path crosses.
  The negotiation-defensibility label (Tier 3: "cite with caveat") is visible in the detail
  pane for Mode 2 without additional interaction.
- Mode 3 (real-time steering within human cost constraints): alert detail fires with causal
  attribution in the fixed detail pane. The analyst steers, observes alert row change, clicks
  to confirm detail — all within Zone 1B without reflow. Supports fast-cycle iteration.

**UX-3 — Entry state coverage (falsifiable acceptance criteria):**
In Reactive entry state (Persona 2, Journey B Step 3): with the Greece 2012 fixture loaded
at step 4 in a live application at 1440×900, click the top CRITICAL alert row. Acceptance
criterion: `data-testid="zone-1b-detail"` is visible within the Zone 1B container bounds
(no scroll), contains `data-testid="alert-detail-panel"` within 500ms of click, and
`data-testid="zone-1b-master"` retains its height (no reflow). Verifiable by Playwright
bounding-box assertion.

**UX-4 — HCL parity certification:**
This ADR modifies layout only — it does not affect data output, indicator weights, or
the display of human cost ledger outputs relative to financial indicators. HCL parity
is maintained. No EL exception required.

**UX-5 — Uncertainty display specification:**
The negotiation-defensibility label from `getNegotiationLabel(confidence_tier)` is inherited
unchanged and displayed in the alert detail sub-zone (currently rendered in the inline detail
panel; relocated to Zone 1B-detail). For Tier 3 (`confidence_tier === 3`): label reads
"Moderate confidence — cite with caveat." The word "synthetic" does not appear in Zone 1B —
the full synthetic data disclosure (including "SYNTHETIC_COMPARABLE" provenance) is a Zone 3
surface in the methodology notes. This is an acknowledged limitation: Zone 1B communicates
confidence level (tier number → label) but not data source provenance. Tier 4: "Early estimate —
confirm before citing." No Structural Absence Declaration display in Zone 1B (Zone 3 surface).

**UX-6 — Irreversibility signal integrity certification:**
TERMINAL alerts use `SEVERITY_COLOR.TERMINAL = "#7f0000"` (dark red fill, `#fff0f0`
background). CRITICAL use `SEVERITY_COLOR.CRITICAL = "#cc0000"`. These are distinct by color
and background — no implementation discretion. Severity colors are exported constants; any
change requires updating `SEVERITY_COLOR` in `MDAAlertPanelZone1B.tsx`, which is a named
violation of this ADR.

At 1440×900 with a fixture containing ≥2 TERMINAL and ≥1 CRITICAL alerts loaded at step 4:
both TERMINAL rows and the CRITICAL row must be visible in `data-testid="zone-1b-master"`
without scroll. Acceptance criterion (CI-testable): Playwright test with Greece 2012 fixture
at step 4; assert that all rows with `data-severity="TERMINAL"` and `data-severity="CRITICAL"`
have bounding boxes within the vertical bounds of `data-testid="zone-1b-master"`.

**UX-7 — User journey coverage:**
- Journey B Step 3 — alert read ceiling extended to include detail pane. Closes the
  below-fold defect flagged in DEMO-042 (scrollable list) and DEMO-043 (detail below fold).
- Journey B Step 4 — argument citation supported within reactive window; no scroll to
  access consecutive breach count and sparkline.
- Journey C Step 3 — causal attribution visible in Zone 1B-detail (Mode 3) without scroll.
- Journey D Step 2 — MDA alert panel as threshold orientation: detail pane confirms which
  specific threshold was crossed and by how much.
- No `[Near-Term-Gap]` items from user-journeys.md are closed by this ADR. This is a
  legibility correction on an already-specified surface, not a capability extension.

**UX Designer sign-off:**
This sign-off is a precondition for the acceptance vote. An ADR with an unchecked UX Designer
sign-off cannot proceed to acceptance vote and cannot be given `Accepted` status.

`[ ]` UX Designer: UX implication statement elements 1–7 confirmed complete. [Date]

---

## Silent Failure Mode

**Silent failure 1 — detail pane height collapses to zero:**
If Zone 1B-detail `flex: 1` receives a computed height of 0px (e.g., Zone 1B-master expands
to fill 100% of Zone 1B via a CSS specificity override), the detail placeholder and detail
panel are both rendered but invisible. No error is thrown. The user sees only the alert list
and a blank space below it — indistinguishable from the old behavior.
Detection: Playwright assertion that `data-testid="zone-1b-detail"` has `clientHeight > 0`
at all three reference viewports with the reference fixture loaded.

**Silent failure 2 — alert selection clears silently after scenario advance:**
If `focusedAlertMdaId` is held in local state and the scenario advances (resetting the store),
the focused alert ID may no longer match any alert in the new step's `mda_alerts`. Zone 1B-detail
would revert to the placeholder without user action — appears as if the alert was deselected.
Detection: set `focusedAlertMdaId` to a known alert ID, advance the scenario, confirm that
Zone 1B-detail shows placeholder (expected) and that no stale detail content is displayed
(stale detail would be indistinguishable from a real alert match and would show wrong data).
Note: the `onSelectAlert` callback propagating to the parent state mitigates this — the parent
should clear `focusedAlertMdaId` on step advance.

---

## North Star Test

A finance minister's analyst is in a sovereign debt negotiation session. Zone 1B shows a
TERMINAL alert for reserve coverage. She selects the alert to read the evidence. Under the
stacked layout, the evidence (sparkline, breach count, approach pct) is below the fold —
unreachable in the 5-second reactive window without scroll. Under the master-detail layout,
the evidence is immediately visible in the fixed detail pane below the alert list.

The argument she gains access to within the 5-second window:
> "This indicator has been below the CRITICAL floor for 3 consecutive steps. The sparkline
> shows continued decline. At approach 18% remaining, the irreversible floor is 5 steps
> away at current draw rate. Your timeline adds 3 steps before the adjustment activates —
> that overshoots. We need an earlier trigger."

This argument was analytically available in the data before this ADR. The only reason it
was not accessible in the reactive window was an implementation choice (stacked layout) that
caused detail to render outside the visible area. The master-detail layout is not a capability
improvement — it is a legibility correction that restores access to already-present analytical
content within the time constraint that the negotiation context imposes.

---

## Mission Impact Statement

This ADR closes DEMO-042 and DEMO-043 (IR findings from M12 demo cycle) — Zone 1B legibility
defects that degrade the reactive-state read experience at demonstration viewports. These findings
directly map to the M13 objective: "instrument legibility improvements — Demo findings DEMO-059–064
resolved" (per CLAUDE.md §Milestone 13). Zone 1B legibility is one dimension of instrument
credibility, which is the M13 theme.

The direct impact on the finance ministry side of a sovereign debt negotiation is: the analyst
can access threshold-crossing evidence (breach count, sparkline, approach pct) within the
5-second reactive read window without scroll. This converts Zone 1B from a threshold-crossing
signal into a threshold-crossing evidence instrument — the difference between alerting to a
problem and equipping the ministry team to argue the magnitude of that problem at the table.

---

## Alternatives Considered

### Alternative 1: Increase Zone 1B allocation height to accommodate stacked layout

The `InstrumentCluster.tsx` allocation for Zone 1B could be increased so the stacked layout
(alert rows + detail below) fits within the visible area. Rejected: Zone 1B increasing means
Zone 1A (trajectory view) or Zone 1C (PMM widget) decreasing. Both are co-primary instruments
with their own visibility requirements. Trading legibility in one primary instrument for
legibility in another does not resolve the underlying architectural issue — it displaces it.

### Alternative 2: Popover or tooltip for alert detail

Alert detail could appear as a positioned popover on alert row click. Rejected: the UX
Architecture First Principles (`docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md`)
and UX governing premise 2 establish that primary Zone 1 information must not be hidden behind
hover or overlay interactions. A popover is an overlay — it can be obscured by other elements
and does not provide the stable, always-visible guarantee that Zone 1B-detail requires.

### Alternative 3: Separate navigator or tab for alert detail

Alert detail could be placed in Zone 2 — accessible via one click from Zone 1B into a
FrameworkPanel tab. Rejected: alert detail (sparkline, breach count, approach pct) is the
primary evidence that makes Zone 1B a co-primary instrument rather than a notification list.
Demotion to Zone 2 demotes Zone 1B itself. Journey B Step 3's 5-second ceiling would require
a tab navigation that the ceiling does not budget.

### Alternative 4: Show only top 1–2 alerts (fewer rows, more space for detail)

Reduce visible alert rows from 3 to 1–2, freeing vertical space for inline detail. Rejected:
`information-hierarchy.md §1B` specifies "top 1–3 alerts visible without scrolling." Reducing
to 1–2 visible rows when 3 alerts are active degrades the Zone 1B scanning surface — the
analyst may miss the second TERMINAL alert. The master-detail allocation (60% master / 40%
detail) preserves the 3-row visibility while adding the fixed detail zone.

---

## Consequences

### Positive

- Alert detail accessible within the 5-second reactive window (Journey B Step 3) without scroll.
- No reflow when an alert is selected — Zone 1B-master height is invariant.
- Zone 1B-detail always visible — the detail zone is a stable, predictable surface in the layout.
- Closes DEMO-042 and DEMO-043 IR findings.
- `AlertDetailPanel`'s scroll-into-view `useEffect` (current workaround for below-fold rendering)
  is removed — component becomes simpler.

### Negative

- Zone 1B-detail occupies ~40% of Zone 1B height even when no alert is selected — the placeholder
  text fills this zone. This reduces Zone 1B-master's visible row count from its theoretical
  maximum (if the full height were allocated to the master list).
- At very narrow Zone 1B heights (< 120px), Zone 1B-detail may be too small to show the full
  sparkline without its own scroll. This is a height allocation concern for the InstrumentCluster
  and is flagged as a renewal trigger.

### Known Limitations

- The alert detail does not show per-cohort income breakdown within Zone 1B. The `cohort` field
  (e.g., "bottom_two_quintiles") is displayed as text in the alert row and detail header, but
  the full cohort breakdown (multiple cohorts, income quintile disaggregation) remains Zone 2
  content accessible via FrameworkPanel. This limitation affects Persona 5 (Cohort Impact
  Analyst) more than Persona 2 — the primary persona served by this ADR.
- Zone 1B-detail confidence tier display uses the negotiation label only, not the full
  synthetic data provenance. A Tier 3 SYNTHETIC_COMPARABLE alert shows "Moderate confidence —
  cite with caveat" — the word "synthetic" does not appear in Zone 1B. Users seeking the full
  provenance disclosure must access Zone 3 methodology notes.

---

## Diagram

`docs/architecture/ADR-014-alert-panel-component-diagram.mmd`

---

*ADR-014 authored 2026-06-12. Tier 1. Phase 0 encoded. Implements ARCH-008.
Gates: G7 (#852) — implementation may not begin until this ADR is Accepted and UX Designer
sign-off is on record. Template version: 2026-06-09.*
