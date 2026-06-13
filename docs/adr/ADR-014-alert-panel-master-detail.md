# ADR-014: Alert Panel (Zone 1B) — Persistent Alert Detail with Scan-Only Compact List

> **Reader Orientation:** This ADR governs the Zone 1B layout architecture for M13 forward.
> Read it before: modifying `MDAAlertPanelZone1B.tsx`, adjusting Zone 1B height allocation
> in `InstrumentCluster.tsx`, or adding sub-zone content to the alert panel.
> G7 (#852) implementation is gated on this ADR's acceptance.
>
> **Design provenance:** The layout model in this ADR emerged from a structured design
> deliberation (UX Designer Agent, Design Thinking Agent, Frontend Architect Agent, EL)
> on 2026-06-12. The deliberation stress-tested four alert volume scenarios (1 alert,
> 5 alerts, 10 alerts, Mode 3 in-flight update) and found that a master-detail
> click-to-select model is inappropriate for a reactive 90-second window. The persistent
> detail model was validated against all four scenarios before this ADR was revised.
> See §Alternatives Considered for the full rejection rationale for the master-detail model.

## Tier Classification

**Tier:** 1

**Justification:**
This ADR modifies Zone 1B — a co-primary instrument in Zone 1 (no interaction required).
It changes the layout architecture of the alert panel's detail surface, directly affecting
the visible-without-scroll guarantee and the interaction budget that Zone 1 instruments must
satisfy per `docs/ux/information-hierarchy.md §Zone 1`.

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
**Valid Until:** M14 close, or when Zone 1B height allocation changes by more than 10%, or
when the top-alert ranking rule changes, or when a new severity level is added

**License Status:** `PROPOSED`

**Panel:**
- Architect Agent (R — authorship, component interface contracts, layout architecture)
- Frontend Architect Agent (C — React component structure, viewport behavior, height budget)
- UX Designer Agent (C — UX implication statement; sign-off required before acceptance vote)
- Engineering Lead (A — accountable on all ADR decisions)

**Renewal Triggers:**
- Zone 1B height allocation in `InstrumentCluster.tsx` changes by more than 10%
- Top-alert ranking rule changes (severity ordering or step-index tiebreak)
- A new alert severity level is added (e.g., ADVISORY below WARNING)
- Zone 1B-detail content scope changes (fields added or removed)
- Mode 3 auto-update behavior is modified (e.g., user-selectable lock on detail slot)
- Zone 1B is split between Mode 2 and Mode 3 into separate components

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

The current implementation (`MDAAlertPanelZone1B.tsx`) renders a severity-sorted alert list
then appends `AlertDetailPanel` below it in a stacked layout. When alert rows fill the visible
area and the user selects one, the detail panel renders below the fold and requires scroll.
The component's own comment records this: *"Scroll into view on mount — Zone 1B is ~135px tall
so the detail panel renders below the fold when 3 alerts already fill the visible area (#814)."*

This stacked layout breaks the Zone 1 contract. The alert detail — breach count, current vs.
floor, consecutive steps — is the evidence Persona 2 needs to formulate the negotiating
argument at Journey B Step 4. Pushing it below the fold converts Zone 1B from a zero-interaction
instrument into a one-scroll instrument.

IR findings DEMO-042 and DEMO-043 documented this as a Zone 1 legibility defect at the M12
demo cycle. Issue #852 specifies the fix.

### Problem Framing

In Journey B Step 3 (Reactive entry state, 90-second total ceiling, 5-second read ceiling),
Persona 2 needs to read not only which alert fired but the evidence behind it — breach count,
current vs. floor, consecutive steps — in order to formulate a specific claim at the negotiating
table. Under the stacked layout, this evidence requires scroll. In a negotiation room, that
scroll is not budgeted.

The consequence: she can say "there is a CRITICAL breach" but not "this threshold has been
breached for N consecutive steps at X% below floor." The second statement is the negotiating
instrument. The first is a status report.

The design deliberation (2026-06-12) identified a deeper problem with the proposed master-detail
fix: a click-to-select model imposes the same interaction budget problem in a different form.
If reading evidence requires selecting an alert, the reactive window still has a mandatory
interaction step. The correct solution eliminates the selection step entirely for the most
urgent finding.

---

## Decision

Zone 1B adopts a **persistent-detail + scan-only compact list** layout. The detail for the
highest-severity alert is always visible without any user interaction. The compact list below
it is a scrollable scan surface — informational only, no click targets.

### Design Specification — Visual Mock-ups and Stress-Test Scenarios

The design is specified by its behaviour across four reference scenarios. These mock-ups are
the primary specification for this ADR — implementation must satisfy all four states. The
implementation detail in subsequent subsections (layout architecture, height budget, component
changes) is derived from and must not contradict these scenarios. The acceptance criteria in
UX-3 and UX-6 are anchored to Scenario B (medium volume, 5 alerts).

**Before — current stacked layout (the problem this ADR resolves):**
```
┌──────────────────────────────────────────────┐  ← Zone 1B, overflow:auto
│ ■ TERM  FIN  reserve coverage   Step 3       │
│ ■ CRIT  HDI  poverty headcount  Step 2       │  ← 3 rows fill visible area
│ ■ WARN  GOV  rule of law        Step 4       │
└──────────────────────────────────────────────┘
                                                 ↕ SCROLL REQUIRED — not budgeted
┌──────────────────────────────────────────────┐  ← AlertDetailPanel below fold
│  Reserve Coverage   TERMINAL                 │
│  Current: 1.842  Floor: 3.0  BREACHED        │
│  Consecutive: 2 steps                        │
└──────────────────────────────────────────────┘
```

**Scenario A — Low volume (1 alert):**
```
┌──────────────────────────────────────────────┐  ← Zone 1B (~135–171px total)
│ ■ CRITICAL  poverty headcount  HDI           │  ← detail slot: always visible, zero clicks
│             Step 2 · bottom_quintile         │
│  Current: 0.312    Floor: 0.28               │
│  11% above floor  ·  1 consecutive step      │
│  Moderate confidence — cite with caveat      │
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
│  No other active alerts.                     │  ← compact sub-zone: empty state
└──────────────────────────────────────────────┘
```

**Scenario B — Medium volume (5 alerts: 1 TERMINAL, 2 CRITICAL, 2 WARNING):**
```
┌──────────────────────────────────────────────┐
│ ■ TERMINAL  reserve coverage  FIN            │  ← highest severity; zero clicks to read
│             Step 3 · all cohorts             │
│  Current: 1.842    Floor: 3.0                │
│  BREACHED  ·  2 consecutive steps            │
│  Moderate confidence — cite with caveat      │
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
│  CRIT  HDI  poverty headcount      Stp 2     │  ← scan only; no click target; cursor:default
│  CRIT  ECO  co2 concentration      Stp 3     │
│  +2 more ↕                                   │
└──────────────────────────────────────────────┘
```

**Scenario C — High volume (10 alerts: 2 TERMINAL, 5 CRITICAL, 3 WARNING):**
```
┌──────────────────────────────────────────────┐  ← Zone 1B height invariant regardless of volume
│ ■ TERMINAL  reserve coverage  FIN            │  ← earliest TERMINAL; 4 consecutive steps
│             Step 1 · all cohorts             │
│  Current: 1.842    Floor: 3.0                │
│  BREACHED  ·  4 consecutive steps            │
│  Moderate confidence — cite with caveat      │
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
│  TERM  GOV  sovereign default      Stp 2     │  ← 2nd TERMINAL visible in compact
│  CRIT  HDI  poverty headcount      Stp 2     │
│  +7 more ↕                                   │
└──────────────────────────────────────────────┘
```

*Design property demonstrated by Scenario C:* Zone 1B height is invariant at all alert
volumes. Ten alerts produce the same Zone 1B footprint as one. The compact sub-zone absorbs
additional alerts through scroll, not through layout expansion.

**Scenario D — Mode 3 in-flight auto-update (new TERMINAL fires mid-session):**

*Before — analyst reading existing TERMINAL data:*
```
┌──────────────────────────────────────────────┐
│ ■ TERMINAL  reserve coverage  FIN            │
│             Step 3 · all cohorts             │
│  Current: 1.842    Floor: 3.0                │
│  BREACHED  ·  2 consecutive steps            │
│  Moderate confidence — cite with caveat      │
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
│  CRIT  HDI  poverty headcount      Stp 2     │
│  WARN  GOV  rule of law            Stp 4     │
└──────────────────────────────────────────────┘
```

*After control input — new higher-priority TERMINAL fires at Step 4:*
```
┌──────────────────────────────────────────────┐
│ ■ TERMINAL  sovereign default  GOV  [NEW]    │  ← auto-updated; [NEW] badge persists
│             Step 4 · all cohorts             │
│  Current: 0.08     Floor: 0.10               │
│  BREACHED  ·  0 consecutive steps            │
│  High confidence — cite directly             │
│  Caused by: EmergencyPolicyInput Step 4      │  ← Mode 3 causal attribution
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
│  TERM  FIN  reserve coverage       Stp 1     │  ← previous top alert; demoted to compact
│  CRIT  HDI  poverty headcount      Stp 2     │
│  +1 more ↕                                   │
└──────────────────────────────────────────────┘
```

*After analyst scrolls Zone 1B-compact — [NEW] badge clears:*
```
┌──────────────────────────────────────────────┐
│ ■ TERMINAL  sovereign default  GOV           │  ← [NEW] cleared; layout otherwise unchanged
│             ...                              │
```

*Design properties demonstrated by Scenario D:* (1) No reflow when detail content changes —
Zone 1B height is identical across all three states shown. (2) [NEW] badge persists until the
analyst takes any action within Zone 1B — it is not a flash. (3) There is no ambiguity about
which alert occupies the detail slot — always the highest-severity, earliest-step alert,
regardless of what the analyst was previously reading.

### Layout Architecture

**Zone 1B outer container:**
```
display: flex
flex-direction: column
height: 100%        (fills Zone 1B allocation from InstrumentCluster)
overflow: hidden    (sub-zones manage scroll independently)
```

**Zone 1B-detail (top sub-zone — always shows highest-severity alert):**
```
flex: 0 0 auto      (fixed height — does not shrink or grow)
overflow: hidden    (no internal scroll; content sized to fit)
```

Always rendered. Always shows the detail of the top-ranked alert from `mda_alerts` (ranked
by severity descending, then step_index ascending within severity). No user action required.
When `mda_alerts` is empty, shows: *"No active threshold breaches."*

**Zone 1B-compact (bottom sub-zone — scan surface for remaining alerts):**
```
flex: 1             (fills remaining Zone 1B height)
overflow-y: auto    (scrollable — analyst may scroll to see all remaining alerts)
```

Shows all alerts except the top-ranked one, in the same severity → step_index order. Rows
are informational only: no click handler, no hover state, `cursor: default`. A `+N more ↕`
indicator appears when the list overflows, where `↕` signals the list is scrollable.

### Top-Alert Ranking Rule

The detail slot always shows the alert ranked first by:
1. Severity: TERMINAL (0) → CRITICAL (1) → WARNING (2)
2. Tiebreak: `step_index` ascending — within the same severity, the earliest breach (most
   consecutive steps accrued) ranks first

**Rationale:** The earliest breach within the highest severity has the longest consecutive
breach count and therefore the strongest argument evidence. At the negotiating table, "this
threshold has been breached for 4 consecutive steps" is a stronger claim than "this just fired."

### Detail Slot Content (No Sparkline)

The detail slot shows the following fields for the top-ranked alert:

```
[SEVERITY pill]  [indicator display name]  [FRAMEWORK_ABBREV]
[cohort — if not "all cohorts"]
Current: {current_value}    Floor: {floor_value}
{BREACHED | N% above floor}  ·  {N consecutive step(s)}
{getNegotiationLabel(confidence_tier)}
[Caused by: {causal_attribution}]   ← Mode 3 only, when present
```

The sparkline is **explicitly excluded** from Zone 1B-detail. Rationale: the framework
composite score trajectory is already displayed in Zone 1A (Trajectory View). Duplicating
it in Zone 1B-detail consumes ~56px of height and adds no information beyond what Zone 1A
already provides. Zone 1B's instrument job is the threshold argument (current vs. floor,
breach count) — not trend visualization. The sparkline belongs in Zone 2 (FrameworkPanel),
which is where preparatory-state exploration occurs.

### Height Budget

Without sparkline, Zone 1B-detail content heights:

| Row | Height |
|---|---|
| Header: severity pill + indicator + framework + step | ~22px |
| Subheader: cohort (conditional — omitted for "all cohorts") | ~18px |
| Values row 1: Current / Floor | ~18px |
| Values row 2: BREACHED/approach · consecutive steps | ~18px |
| Confidence label | ~16px |
| Top + bottom padding | ~8px |
| **Total (without cohort subheader)** | **~82px** |
| **Total (with cohort subheader)** | **~100px** |
| Mode 3 causal attribution (conditional) | +16px |

Remaining height for Zone 1B-compact at reference viewports
(Zone 1B height estimated from InstrumentCluster ~45% of column height):

| Viewport | Zone 1B est. | Detail (no cohort) | Compact remaining | Compact rows visible |
|---|---|---|---|---|
| 1024×768 | ~135px | ~82px | ~53px | 2 rows (~24px ea.) + "+N more" |
| 1280×800 | ~153px | ~82px | ~71px | 2–3 rows + "+N more" |
| 1440×900 | ~171px | ~82px | ~89px | 3 rows + "+N more" |

**Viewport verification is mandatory before the G7 PR is marked ready for review.** The
implementing agent must measure the actual Zone 1B computed height at each viewport and
confirm that Zone 1B-detail is fully visible (not clipped) and at least 1 compact row is
visible in Zone 1B-compact. If Zone 1B-detail is clipped at 1024×768, Zone 1B allocation
in `InstrumentCluster.tsx` must increase — that change requires an ADR amendment before
the PR merges.

### Mode 3 Auto-Update and [NEW] Signal

In Mode 3, when a scenario step advances and the new highest-ranked alert differs from the
previous one (different `mda_id`), Zone 1B-detail auto-updates to show the new top alert.
No user action required or available.

When this auto-update occurs, a `[NEW]` badge appears in the header row of Zone 1B-detail:

```
[TERMINAL]  reserve coverage  FIN  [NEW]
```

**[NEW] persistence rule:** The badge persists until the analyst's next interaction within
Zone 1B — any scroll of Zone 1B-compact, or any click within Zone 1B bounds, clears it.
A 200ms animation-only flash is not sufficient: the badge must persist because the analyst
may be composing a verbal argument and glancing at the screen intermittently. A persistent
badge is still visible on the next glance; a flash is not.

**[NEW] does NOT appear** when the alert list updates but the top-ranked alert remains the
same `mda_id` — e.g., when a step advances and the same TERMINAL alert now shows one more
consecutive breach step. That is an update to existing evidence, not a new finding.

### Component Interface Changes

**`MDAAlertPanelZone1B`:**
- Outer container style: `overflowY: "auto"` → `display: "flex"; flexDirection: "column"; height: "100%"; overflow: "hidden"`
- Remove: `focusedAlertMdaId` prop (no user selection)
- Remove: `onSelectAlert` prop
- Remove: inline `AlertDetailPanel` render
- Add: `TopAlertDetail` internal sub-component (renders detail slot content without sparkline)
- Add: `CompactAlertList` internal sub-component (scan-only rows; no click handler)
- Add: `showNewBadge` state (`boolean`) + change-detection logic comparing `mda_alerts[0].mda_id` across renders
- `data-testid="zone-1b-detail"` → rename to `data-testid="zone-1b-top-detail"` for clarity
- `data-testid="zone-1b-compact"` — new testid for compact list sub-zone

**`AlertDetailPanel`:** Retained for use in `EntityDetailDrawer` (the drawer uses it independently of Zone 1B). Remove only from `MDAAlertPanelZone1B`. The scroll-into-view `useEffect` in `AlertDetailPanel` (line 162–163) may be removed from the Zone 1B context since it is no longer rendered there; it is retained in the EntityDetailDrawer usage.

**`InstrumentCluster`:** Remove `focusedAlertMdaId` state and `onSelectAlert` handler that were wired to `MDAAlertPanelZone1B`.

---

## Persona and UX Traceability

### [Tier 1] Persona Trace

**P-1 — Persona identification:**
Primary: Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou archetype).
Secondary: Persona 3 — Political Advisor (Andreas Stefanidis archetype) — also operates in
reactive state and has the same zero-interaction ceiling for alert evidence.

**P-2 — Entry state:**
Reactive entry state (90-second total ceiling, negotiation room context). Journey B Step 3
establishes a 5-second ceiling for the alert read — severity, indicator name, and breach
evidence must all be readable **without any interaction** from the moment the instrument
cluster is visible. This ADR eliminates the selection step that existed in both the stacked
layout (scroll) and the earlier master-detail proposal (click).

**P-3 — Journey reference:**
- Journey B Step 3 — "Scan: read the top MDA alert" — 5-second ceiling for severity,
  indicator, step, cohort. Under this ADR, the ceiling now covers the full breach evidence
  (current vs. floor, consecutive breach count) with zero interactions, not one click.
- Journey B Step 4 — "Cite: formulate the argument" — the breach evidence in Zone 1B-detail
  is the raw material. It is available immediately on drawer open, not after a selection.
- Journey C Step 3 — MDA alert fires with causal attribution in Mode 3. Causal attribution
  appears in Zone 1B-detail for the top alert without any user action.
- Journey D Step 2 — threshold orientation: Zone 1B-detail confirms which specific threshold
  was crossed and by how much, before the analyst has taken any action.
- Closes DEMO-042 and DEMO-043 (IR findings from M12 demo cycle).

**P-4 — Time or interaction ceiling:**
**Zero interactions** to read the top alert's full evidence (severity, indicator, current vs.
floor, consecutive breach count, confidence label) from the moment Zone 1B is visible at the
reference viewport (1440×900). Zero clicks. Zero scrolls. The instrument delivers the argument
evidence automatically to the analyst's eye.

**P-5 — Income cohort served:**
Zone 1B MDA alerts are cohort-tagged. The cohort field is displayed as a subheader in
Zone 1B-detail when it is not "all cohorts" — the analyst can immediately see which cohort
is affected without any additional interaction. Per-cohort income quintile breakdown
(bottom two quintiles, pensioners 65+, etc.) remains Zone 2 content; this ADR does not
extend or constrain cohort coverage beyond the existing `cohort` field.

**P-6 — Negotiating leverage statement:**
After this layout change, Persona 2 can make the following specific argument at the moment
she opens the instrument cluster, with zero interactions:
> "The TERMINAL alert for reserve coverage has been active for 4 consecutive steps.
> Current value is 1.842 months against a floor of 3.0 — fully breached. Under your proposed
> adjustment timeline, this has already crossed the irreversible threshold. This is not a
> one-period anomaly; it is a structural drawdown that predates this negotiation session."

Previously this argument required a scroll (stacked layout) or a click (master-detail
proposal). Under this ADR it requires neither.

**P-7 — North star test answer:**
A Zambian finance minister's lead analyst opens the WorldSim instrument cluster during a
live debt restructuring session. The IMF team has just proposed an adjustment timeline. Zone 1B
shows a TERMINAL alert for reserve coverage. Without touching the screen, the analyst reads:
"TERMINAL — reserve coverage — FIN — Step 1 — Current: 1.842 / Floor: 3.0 — BREACHED —
4 consecutive steps — Moderate confidence, cite with caveat."

She says at the table: "This threshold has been fully breached for four consecutive steps —
your proposed timeline would add three more steps before any adjustment. By that point we
are 7 steps into an irreversible drawdown. We need the trigger at Step 3, not Step 6."

The IMF team's analysts have this same evidence in their proprietary monitoring tools without
a legibility constraint. The only reason the Zambian analyst did not have immediate access to
it was an implementation choice — the stacked layout rendering the detail below the fold.
This ADR closes a pure legibility asymmetry: the data was already present; only the layout
was wrong. After this change, the ministry team reads the same evidence in the same timeframe
as the creditor side.

---

### [Tier 1] UX Implication Statement

**UX-1 — Zone assignment and hierarchy certification:**
This ADR places the alert detail surface in Zone 1B-detail (co-primary, no interaction
required). The alert detail currently occupies Zone 1B-overflow (requires scroll — Zone 2
positioning despite Zone 1 content). The compact alert list for remaining alerts is also
placed in Zone 1B — it is a scan surface, not a drill-down surface. Both sub-zones are
within the Zone 1B allocation. The compact list's scroll capability does not demote it to
Zone 2 — it is a supplementary scan surface within the primary instrument, not a separate
navigation destination. Assignment is consistent with `information-hierarchy.md §1B`.

**UX-2 — Primary cognitive task alignment:**
- Mode 1 (trajectory reconstruction): Zone 1B-detail shows historical breach evidence at
  the loaded step — consecutive breach count and current vs. floor at the historical crossing
  point. Reconstruction task is served without navigating away from Zone 1.
- Mode 2 (threshold-safe path construction): Zone 1B-detail shows projected threshold
  approach at the current step. Negotiation-defensibility label visible without interaction.
  The analyst can confirm which threshold the projected path crosses and how much headroom
  remains.
- Mode 3 (real-time steering within human cost constraints): Zone 1B-detail auto-updates
  when a new highest-severity alert fires. The `[NEW]` badge persists until acknowledged.
  Causal attribution ("Caused by: [input]") appears in the detail slot for the top alert
  without any interaction. The analyst steers, reads the immediate consequence in Zone 1B-detail,
  steers again — tight reactive loop with no interaction required to maintain situational awareness.

**UX-3 — Entry state coverage (falsifiable acceptance criteria):**
In Reactive entry state (Persona 2, Journey B Step 3): with the Greece 2012 fixture loaded
at step 4 in a live application at 1440×900, Zone 1B-detail must be visible and populated
with the top-ranked alert's evidence fields (severity, indicator, current vs. floor, consecutive
breach count, confidence label) **without any user interaction after fixture load**.

Acceptance criterion: Playwright test with Greece 2012 fixture at step 4; immediately after
fixture loads (no clicks), assert that `data-testid="zone-1b-top-detail"` is visible within
Zone 1B bounds, contains `data-testid="detail-indicator-name"` with non-empty text, and
`data-testid="detail-current-value"` with a non-empty numeric value. No click or scroll event
may fire between fixture load and assertion.

**UX-4 — HCL parity certification:**
This ADR modifies layout and interaction model only. It does not affect data output, indicator
weights, or the display of human cost ledger outputs relative to financial indicators. HCL
parity is maintained. No EL exception required.

**UX-5 — Uncertainty display specification:**
The negotiation-defensibility label (`getNegotiationLabel(confidence_tier)`) is displayed in
Zone 1B-detail for the top alert, always visible. For Tier 3 (`confidence_tier === 3`): label
reads "Moderate confidence — cite with caveat." The word "synthetic" does not appear in Zone 1B —
the full synthetic data disclosure (SYNTHETIC_COMPARABLE provenance) is a Zone 3 surface.
For Tier 4: "Early estimate — confirm before citing." No Structural Absence Declaration in
Zone 1B (Zone 3 surface). This is an acknowledged limitation: Zone 1B communicates confidence
level (tier number → label) but not data source provenance. The compact list rows do not
display confidence tier — only the top alert's detail slot does.

**UX-6 — Irreversibility signal integrity certification:**
The top alert in Zone 1B-detail uses the full severity pill (`SEVERITY_COLOR.TERMINAL = "#7f0000"`,
`SEVERITY_COLOR.CRITICAL = "#cc0000"`) — visually distinct with no implementation discretion.
The compact list rows use the severity abbreviation (`TERM`, `CRIT`, `WARN`) in the severity
color but without a pill background, clearly visually subordinate to the detail slot.

TERMINAL and CRITICAL alerts are always surfaced at the top of Zone 1B-detail (auto-ranked).
If both a TERMINAL and a CRITICAL are active, the TERMINAL is always in the detail slot and
the CRITICAL is always in the first compact row. No interaction is required to promote the
TERMINAL to the visible position — it is there by default.

Acceptance criterion (CI-testable): Playwright test with a fixture containing ≥1 TERMINAL
alert; assert that `data-testid="zone-1b-top-detail"` has `data-severity="TERMINAL"` and is
visible within Zone 1B bounds at 1440×900 without any click or scroll events. Verifiable by
bounding-box assertion.

**UX-7 — User journey coverage:**
- Journey B Step 3 — 5-second ceiling now covers full breach evidence with zero interactions.
  Closes DEMO-042 (scrollable list — compact list is scrollable but auto-ranking means the
  top finding is always surfaced without scroll) and DEMO-043 (detail below fold — detail
  is always in Zone 1B-detail sub-zone above the compact list).
- Journey B Step 4 — argument citation available immediately; no interaction required to access
  breach count and threshold comparison.
- Journey C Step 3 — causal attribution appears in Zone 1B-detail for the top alert in Mode 3
  without any user action; `[NEW]` badge signals when the causal finding updates.
- Journey D Step 2 — threshold orientation: Zone 1B-detail provides current vs. floor and
  breach count as the first data the analyst reads upon entering the instrument cluster.
- No `[Near-Term-Gap]` items from user-journeys.md are closed by this ADR. This is a
  legibility correction on an already-specified surface, not a capability extension.

**UX Designer sign-off:**
This sign-off is a precondition for the acceptance vote. An ADR with an unchecked UX Designer
sign-off cannot proceed to acceptance vote and cannot be given `Accepted` status.
The UX Designer participated in the design deliberation of 2026-06-12 and validated the
persistent-detail model against all four stress-test scenarios. Formal sign-off on this
revised ADR text is required before the vote.

`[ ]` UX Designer: UX implication statement elements 1–7 confirmed complete. [Date]

---

## Silent Failure Mode

**Silent failure 1 — Zone 1B-detail height collapses to zero:**
If a CSS specificity override causes Zone 1B-detail to collapse (computed height = 0px),
the detail content is rendered but invisible — no error, no warning. The analyst sees the
compact list filling all of Zone 1B with no visible detail section above it.
Detection: Playwright assertion that `data-testid="zone-1b-top-detail"` has `clientHeight > 0`
immediately after fixture load at all three reference viewports, with no user interactions.

**Silent failure 2 — stale detail after step advance:**
If `mda_alerts` in the store updates after a step advance but the change-detection logic in
`MDAAlertPanelZone1B` fails to re-evaluate the top-ranked alert (e.g., memoisation holding
stale `mda_alerts[0]`), Zone 1B-detail shows evidence from the previous step while the compact
list shows updated alerts from the new step. The detail is internally consistent but stale
relative to the new step — the analyst reads old breach count data while the compact list
shows new alerts. No visual indicator of the mismatch.
Detection: advance the scenario, assert that `data-testid="detail-consecutive"` text value
matches the current step's `consecutive_breach_steps` value for the top-ranked alert in the API
response.

**Silent failure 3 — compact list renders with click handler attached:**
If a refactor accidentally attaches an `onClick` handler to compact list rows, the scan-only
contract is violated — rows become interactive but with undefined behavior (no `onSelectAlert`
handler to call). The analyst may click a compact row expecting promotion and receive no
response, or trigger an unrelated action.
Detection: Playwright test asserts that no compact row (`data-testid="compact-alert-row"`)
has a cursor style other than `default` and that clicking a compact row produces no change
to `data-testid="zone-1b-top-detail"` content.

**Silent failure 4 — [NEW] badge never appears on auto-update:**
If the `showNewBadge` state is not set when the top-ranked alert changes `mda_id` between
renders (e.g., because the comparison uses referential equality on the alerts array rather
than `mda_id` string comparison), the analyst receives no signal that the detail slot updated
in Mode 3. She may read stale evidence without knowing it changed.
Detection: in a Mode 3 test fixture, fire a control input that causes a new highest-severity
alert; assert that `data-testid="detail-new-badge"` is present and visible in Zone 1B-detail
after the step computation completes, before any user interaction.

---

## North Star Test

A finance minister's analyst is in a live debt restructuring session. The instrument cluster
is open. Zone 1B shows a TERMINAL alert for reserve coverage. She has not touched the screen.

She reads, immediately: "TERMINAL — reserve coverage — BREACHED — 4 consecutive steps."

She says: "This has been in breach for four consecutive steps. Your proposed timeline does not
correct for this until Step 6 — two steps after the irreversible floor is crossed. We cannot
accept that timeline."

This argument requires zero interactions. Under the stacked layout it required scroll. Under the
earlier master-detail proposal it required one click. Under this ADR it requires neither. The
layout improvement is not a capability addition — it is the removal of an interaction tax on
evidence that was already present in the data. The ministry team should not be paying an
interaction tax that the creditor side does not pay in their own monitoring tools.

---

## Mission Impact Statement

This ADR closes DEMO-042 and DEMO-043 — Zone 1B legibility defects identified in the M12 IR
review. The direct impact on the finance ministry side of a sovereign debt negotiation is:
the analyst can read the top alert's full threshold argument (breach count, current vs. floor)
the moment she looks at Zone 1B, without any prior interaction. The difference between the
current layout and this one is one step removed from the mission: it is the difference between
an analyst who can cite specific threshold evidence and an analyst who can only report that a
threshold was crossed. The former has a negotiating instrument; the latter has a status update.

Zone 1B legibility is one dimension of instrument credibility — the M13 theme. This ADR
converts Zone 1B from a threshold notification surface into a threshold evidence instrument.

---

## Alternatives Considered

### Alternative 1: Increase Zone 1B allocation to accommodate stacked layout

Increase Zone 1B height in `InstrumentCluster.tsx` so the stacked layout (alert rows +
detail below) fits without scroll. Rejected: Zone 1B increasing means Zone 1A (trajectory
view), Zone 1C (PMM widget), or Zone 1D (four-framework readout) decreasing. All are
co-primary instruments. Trading legibility in one primary instrument for legibility in another
displaces rather than solves the problem.

### Alternative 2: Popover or tooltip for alert detail

Alert detail appears as a positioned popover on alert row click. Rejected: UX governing
premise 2 establishes that primary Zone 1 information must not be behind hover or overlay
interactions. A popover is an overlay — it can be obscured and does not provide the stable,
always-visible guarantee Zone 1B-detail requires.

### Alternative 3: Alert detail in Zone 2 (FrameworkPanel tab)

Alert detail placed in Zone 2, accessible via one click from Zone 1B. Rejected: alert detail
(breach count, current vs. floor) is the primary evidence that makes Zone 1B a co-primary
instrument rather than a notification list. Demotion to Zone 2 demotes Zone 1B itself.
Journey B Step 3's 5-second ceiling does not budget a tab navigation.

### Alternative 4: Master-detail with click-to-promote (ADR-014 original proposal, 2026-06-12)

Zone 1B split into a fixed master pane (alert list) and a fixed detail pane below it. User
clicks an alert row to populate the detail pane. The detail pane is empty (placeholder) until
a row is selected.

Rejected after design deliberation stress-test (2026-06-12). Two failure modes identified:

*Failure 1 — selection step in the reactive window.* The master-detail model requires a click
to access detail. In a 90-second reactive window at a negotiating table, even one interaction
is a budgeted cost that the creditor side's analysts do not pay. The persistent-detail model
eliminates this cost.

*Failure 2 — auto-override conflict in Mode 3.* When the analyst has clicked to select a
CRITICAL alert (populating the detail pane), and then a new TERMINAL fires, the instrument
faces an unresolvable conflict: override the user's selection (she loses her read) or respect
it (she misses the most urgent alert). Neither option is correct for a real-time steering
instrument. The scan-only compact list eliminates this conflict entirely by removing user
selection from Zone 1B.

### Alternative 5: Persistent detail + click-to-promote compact list

Persistent detail for the top alert, but compact list rows are clickable to promote a
selected alert to the detail slot. Rejected as part of the same stress-test deliberation.
The click-to-promote model reintroduces the Mode 3 auto-override conflict: if the user has
promoted a CRITICAL, does a new TERMINAL override her selection? The scan-only model avoids
this by making Zone 1B's detail slot always system-ranked, never user-ranked. User-driven
alert exploration belongs in Zone 2.

---

## Consequences

### Positive

- Top alert's full breach evidence readable with zero interactions from moment of Zone 1B load.
- Zone 1B height invariant across all alert volumes (1 alert to 10+ alerts).
- No reflow at any alert volume or interaction.
- Mode 3 auto-update with persistent `[NEW]` badge gives the analyst a reliable signal when
  the instrument updates without requiring her to watch for it.
- Compact list is simpler to implement and test than a click-to-promote model — no selection
  state, no toggle logic, no parent state coordination for `focusedAlertMdaId`.
- `AlertDetailPanel`'s scroll-into-view `useEffect` is removed from Zone 1B context (it was
  a workaround for below-fold rendering; no longer needed).

### Negative

- Zone 1B-detail occupies ~82px of fixed height even when no alerts are active — the "No
  active threshold breaches." message fills this space. This is a visual cost when Zone 1B
  is empty. Acceptable: an empty alert panel is a rare condition in a live negotiation scenario,
  and the fixed height ensures the layout never shifts.
- The analyst cannot promote a specific secondary alert to the detail slot from Zone 1B. If she
  needs the full evidence for the 2nd or 3rd alert, she must go to Zone 2. This is an intended
  scope constraint, not an oversight — Zone 1B is the reactive instrument, Zone 2 is the
  exploratory instrument. The constraint should be documented in end-user help text.
- The compact list shows severity + indicator + step only (no current vs. floor values). The
  analyst cannot read the secondary alert's evidence from Zone 1B. Accepted: the compact list
  is a scan surface confirming severity rank, not an evidence surface.

### Known Limitations

- Zone 1B-detail does not show per-cohort income disaggregation. The `cohort` field is displayed
  as a subheader but only for the single affected cohort named in the alert. Full cohort breakdown
  (income quintile distribution across all cohorts) remains Zone 2 content. This limitation
  affects Persona 5 (Cohort Impact Analyst) more than Persona 2.
- Confidence tier display in Zone 1B-detail is a label only ("Moderate confidence — cite with
  caveat"), not a provenance disclosure. The word "synthetic" does not appear. Users requiring
  full provenance must access Zone 3 methodology notes. Acknowledged limitation documented here
  to satisfy the Zone 1B transparency requirement.
- The sparkline is intentionally excluded from Zone 1B-detail. Analysts who need the framework
  trajectory chart find it in Zone 1A (always visible) or Zone 2 FrameworkPanel (one scroll).
  This exclusion is a deliberate height-budget decision, not a capability gap.

---

## Diagram

`docs/architecture/ADR-014-alert-panel-component-diagram.mmd`

---

*ADR-014 revised 2026-06-12. Original authorship 2026-06-12. Tier 1. Phase 0 encoded.
Implements ARCH-008. Design model revised after structured deliberation (UX Designer Agent,
Design Thinking Agent, Frontend Architect Agent, EL) with four-scenario stress test.
Gates: G7 (#852) — implementation may not begin until this ADR is Accepted and UX Designer
sign-off is on record. Template version: 2026-06-09.*
