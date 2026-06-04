# ADR-008: UX Architecture — Instrument Cluster, Viewport, and Interaction Model

## Status
Accepted

## Validity Context

**Standards Version:** 2026-05-22
**Valid Until:** Milestone 11.5 — Usability Validation and Experience Audit
**License Status:** ACCEPTED — 2026-05-22

**M11 exit review:** 2026-06-04 (SCAN-025). No renewal triggers fired during Milestone 11. No frontend components modified in M11. PoliticalEconomyModule outputs (`legitimacy_index`, `programme_survival_probability`, `elite_capture_divergence`) are engine outputs — their Zone placement is specified in the M11 political economy user stories (Issue #681, PR #713) as Zone 2; no Zone 1 instrument layout changes required. `_steps_projected` envelope field is backend-only. No mode transition, Zone boundary, simultaneous-update contract, or confidence tier visual changes. License renewed to Milestone 11.5. M11.5 usability audit may surface Zone 1 layout findings that trigger a renewal — evaluate at M11.5 exit.

**M10 exit review:** 2026-06-02 (SCAN-024). No renewal triggers fired during Milestone
10. All four Zone 1 instruments implemented per ADR-008 spec — implementation of the
spec is not a trigger. Zone boundaries unchanged. `step_event_label` fix (Issue #395)
standardised fixture content format; the field name, type, and schema contract are
unchanged — not a trigger. Column width responsive fix (Issue #647) is an implementation
detail within the existing ADR-008 layout contract. Simultaneous instrument update
contract (AC-006 RTL test confirms all Zone 1 instruments update in a single render
cycle) remains in force and unchanged. No mode transition, A/B comparison, blue/orange
color, confidence tier visual, or methodology access model changes. License Status
confirmed ACCEPTED. License renewed through Milestone 11 — Engine Investigation and
Political Economy. M11 political economy module will introduce new conditionality
instruments; any control plane or mode 3 changes must be evaluated against ADR-008
renewal triggers at M11 exit. Next scheduled review at Milestone 11 close.

**Panel (accepted):**
- UX Designer Agent (C — UX frame and component decisions)
- Frontend Architect Agent (C — implementing agent, required per panel composition rule)
- Chief Methodologist (C — confidence tier visual system, epistemic obligations)
- Engineering Lead (A — accountable on all ADR decisions)

**Renewal Triggers** — any of the following fires the CURRENT → UNDER-REVIEW transition:
- Viewport zone definitions changed (Zone 1 / 2 / 3 boundaries)
- Control plane zone sizing revised or its reserved position moved
- Step axis annotation schema fields (`effective_from`, `step_event_label`,
  `step_significance`) renamed, typed differently, or removed
- Live A/B comparison invocation model changed (currently: automatic on first
  control input — any change to this contract triggers renewal)
- Blue/orange color assignment changed (currently: blue = policy input, orange =
  exogenous shock — cross-layer consistency is a hard contract)
- Confidence tier visual differentiation rules changed (solid/dashed/opacity
  thresholds, tier badge interactivity)
- Mode transition design changed (explicit user action requirement, single modal
  confirmation rule)
- Simultaneous instrument update contract changed (currently: all Zone 1
  instruments update in a single render cycle)
- Methodology documentation access model changed (currently: one interaction
  from any instrument output)

## Date
2026-05-22

## Context

### Background

ADR-001 through ADR-006 established the simulation data model, engine, and
measurement infrastructure through Milestone 8. These ADRs define what the
simulation computes. This ADR defines how the simulation presents its output
to the user across all three interaction modes.

At M8, the WorldSim frontend architecture positions the geographic context view
(choropleth) as the primary viewport. The primary instruments — the MDA alert
panel, radar chart, and PMM widget — live inside the EntityDetailDrawer, a
panel approximately 25% of viewport width that the user must open to see them.
This is an inversion: the context (where effects are distributed) occupies the
primary viewport while the instruments (whether the programme is safe) are in
the drawer.

### The Case B Finding

The UX Design Thinking Agent critique (PR #355, 2026-05-18) diagnosed this
inversion and produced a Case B verdict: *Case B means the architecture requires
rethinking before implementation begins, not incremental patching after.* (Case A
would mean incremental improvement is sufficient. Case B requires a principled
restart. The Case A / Case B terminology originates in
`docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md` — read
that document for the full derivation; this ADR is the canonical authority derived
from it. DOC-LEGIBILITY-AUDIT-001, Gap 2, 2026-06-03.)

The first-principles review (PR #390,
`docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md`)
derived five governing premises from Mode 3 requirements, validated them against
all five personas, and identified four specific Mode 3 requirements (R1–R4)
that the M8 architecture fails:

**R1 — Primary instruments must be always visible.** The user cannot open a
drawer to read their altimeter during a stall. MDA alerts, PMM, and trajectory
must be visible without opening the EntityDetailDrawer.

**R2 — The feedback loop must be spatially immediate.** Control input is applied
in one viewport region; trajectory response must update in the same region.

**R3 — The temporal frame must be primary.** Mode 3 is active steering across
a programme horizon. The trajectory view — not the choropleth — is the primary
frame.

**R4 — Pilot input and exogenous shock must be visually distinguishable.**
A policy decision and a scenario shock both change the trajectory. Only one is
under the pilot's control. The visual system must make this distinction
scannable without reading alert text.

### The Three EL Decisions

Engineering Lead decisions recorded on Issue #364 (2026-05-21):

**EL Decision 1 — Per-mode cognitive tasks (supersedes M4-era single formulation):**
Mode 1: trajectory reconstruction AND historical pattern recognition.
Mode 2: threshold-safe path construction.
Mode 3: real-time steering within human cost constraints.
All 13 marquee cases validated.

**EL Decision 2 — Viewport architecture:**
Primary viewport is the instrument cluster. EntityDetailDrawer demoted to
detail and methodology surface. Entity selector is a persistent header element.

**EL Decision 3 — Comparison mode conditional (extended to Mode 3):**
Single-entity Mode 2 → divergence timeline.
Multi-entity Mode 2 → DeltaChoropleth.
Mode 3 → automatic live A/B (no COMPARE_VIEW entered; instrument cluster
trajectory view always shows baseline ghost curves once first control input
is applied).

### Six Specification Gaps Closed Before This ADR

The persona-grounded review (PR #388) and first-principles depth document
(PR #390, `docs/ux/design-thinking/worldsim-ux-architecture-first-principles-depth.md`)
closed six specification gaps to Frontend Architect precision before this ADR
was drafted. The gaps are not architectural failures — they are preconditions
for this ADR to be implementable:

- **Gap 1A:** Mode 3 walkthrough (Eleni February 2012) — 10-component requirement table
- **Gap 1B:** Mode 1 step axis annotation — three mandatory fixture fields and rendering spec
- **Gap 2:** Three structural breaks in the flight simulator analogy — with derived qualifications
- **Gap 3:** Blue/orange cross-layer visual system — policy inputs vs. exogenous shocks
- **Gap 4:** Live A/B comparison — automatic invocation, visual design, preconditions
- **Gap 5:** Mode transition design — persistent vs. mode-specific instruments; transition states

### Governing Premises

The following six premises govern all decisions in this ADR. They are not
preferences — they are the architectural load-bearing claims of the Case B verdict.
A proposed change that conflicts with any premise requires Engineering Lead
decision with recorded rationale in `docs/frontend/design-decisions.md`.

**Premise 1 — The primary viewport is the instrument cluster. Geographic context
is always accessible but never primary.**

**Premise 2 — Primary instruments are always visible without opening a drawer,
without scrolling, at any supported viewport. Confidence tier is a primary
instrument attribute — displayed on the instrument face, not in Zone 3. A Tier 4
instrument does not visually resemble a Tier 1 instrument.**

**Premise 3 — The step axis is the shared frame for all instruments. In Mode 1,
the step axis displays calendar date and event label on every step marker —
this is mandatory, not optional. All instruments that display the step axis
update simultaneously when a step is navigated or a computation completes.**

**Premise 4 — The primary cognitive task differs by mode and by persona within
each mode. The architecture must not collapse the Mode 1 cognitive task to
trajectory reconstruction alone — Mode 1 must support both trajectory
reconstruction (Eleni) and historical pattern recognition (Andreas) without
requiring them to share the same cognitive path.**

**Premise 5 — The control plane is a persistent layout zone, adjacent to the
primary instrument cluster, reserved in the layout architecture before it is
built. The zone must accommodate at minimum: a policy input form, an exogenous
shock injection form, and an applied inputs/shocks history list.**

**Premise 6 — Methodology documentation is accessible within one interaction of
any instrument output. Confidence tier badges are interactive: tapping any badge
opens the methodology note for that indicator.**

### Open Issues at ADR Authoring

- **Issue #366** — Trajectory view ADR (ADR-010). Blocks M9 Frontend Architect
  brief. This ADR commits to the trajectory view as Zone 1A and specifies its
  requirements; ADR-010 will go deeper on the trajectory view component
  architecture (data streaming, rendering performance, step axis state management).
- **Issue #397** — This ADR (ADR-008). Closed 2026-05-22 — panel review complete,
  EL accepted. See `docs/adr/reviews/ADR-008-panel-review.md`.

---

## Decision

### Decision 1 — Instrument Cluster as Primary Viewport

The instrument cluster is the primary viewport for all three interaction modes.
The choropleth (geographic context view) is navigable from the primary viewport
but is never the primary surface.

**What this replaces:** The M8 layout where the choropleth occupies the full
primary viewport and instruments are inside the EntityDetailDrawer.

**What "primary viewport" means operationally:**

At any supported viewport size (desktop 1280×800 minimum, tablet 1024×768
minimum), the instrument cluster occupies the dominant visual area — the region
the user sees without any navigation, scroll, or interaction after landing. The
choropleth is accessible via a navigation affordance (tab, panel toggle, or
secondary viewport zone) but does not occupy this dominant area.

**Implementation constraint:** The entity selector, mode indicator, and all
Zone 1 instruments (Decisions 3–7) must be within the primary viewport at the
minimum supported viewport sizes without any navigation. A layout that places
any Zone 1 instrument below the fold at 1024×768 is not compliant with this
decision.

---

### Decision 2 — Zone Assignments for All Instruments

The three-zone disclosure model (Zone 1 / Zone 2 / Zone 3) from
`docs/ux/information-hierarchy.md` is the binding hierarchy. Assignments are
as follows.

**Persistent Header (above all zones, always visible):**
- Mode indicator (see Decision 3)
- Entity selector (see Decision 3)

**Zone 1 — Primary (no interaction required):**
- 1A: Trajectory view (see Decision 4) — highest weight, primary instrument
- 1B: MDA alert panel (see Decision 5) — co-primary
- 1C: PMM widget (see Decision 6) — co-primary
- 1D: Four-framework current position (see Decision 7) — co-primary

**Zone 2 — Secondary (one scroll or one click):**
- 2A: Radar chart (moved from Zone 1 by EL Decision 2)
- 2B: Framework panels (financial, human_development, ecological, governance)
- 2C: Distribution bands (M5 forward)

**Zone 3 — Tertiary (deliberate navigation):**
- 3A: Methodology notes and mandatory disclosures (ia1_disclosure, ecological note)
- 3B: Raw indicator tables
- 3C: Backtesting fidelity dashboard

**EntityDetailDrawer:** Demoted by EL Decision 2 to a detail and methodology
surface. No primary instrument lives inside the drawer. The drawer contains Zone
2 and Zone 3 content (indicator detail, cohort breakdowns, methodology notes) and
is accessible from the choropleth or from instrument interactions that require
per-indicator context. Primary instruments must not be relocated to the drawer
without an Engineering Lead decision recorded in `docs/frontend/design-decisions.md`.

**What moves from M8:** The radar chart moves from Zone 1 to Zone 2A. The MDA
alert panel moves from inside the EntityDetailDrawer to Zone 1B in the instrument
cluster viewport. The PMM widget moves from inside the drawer to Zone 1C.

---

### Decision 3 — Persistent Header Elements

Two elements are positioned above all disclosure zones and must be visible in
all three modes, at all supported viewport sizes, without any navigation or
interaction:

**Mode Indicator:** A persistent label in the primary viewport header that reads:

```
MODE 1 — REPLAY  |  MODE 2 — SIMULATION  |  MODE 3 — ACTIVE CONTROL
```

The three labels function as a mode selector — the user taps a label to switch
to that mode. Mode transitions are explicit user actions (see Decision 15); no
instrument interaction causes a mode transition as a side effect.

**Entity Selector:** Shows the current primary entity name. In single-entity
scenarios, displays the entity name. In multi-entity scenarios, renders as a
toggle (two entities) or dropdown (three or more entities) that allows switching
the primary entity without navigating away from the instrument cluster.

Entity switch must update all four Zone 1 instruments atomically — not one at a
time, not with separate loading states per instrument. The atomicity requirement
from Decision 14 applies.

The entity selector is not inside the EntityDetailDrawer. It is not accessible
only after interacting with the choropleth. It is a persistent viewport element.

---

### Decision 4 — Trajectory View Specification (Zone 1A)

The trajectory view is the primary Zone 1A instrument. It is positioned in the
primary viewport — not inside the EntityDetailDrawer, not behind a tab or
navigation action.

**Core requirements:**
- Four composite score curves (financial, human development, ecological, governance)
  visible simultaneously on a single shared step axis
- MDA floor lines overlaid as horizontal dashed threshold lines on each framework curve
- Step transitions animated 200–300ms ease-in-out
- Trajectory view occupies the primary viewport at all supported viewport sizes
  without requiring navigation

**Mode-specific behavior:**

*Mode 1 (Replay):*
- Historical trajectory curves, fixed (no ghost curves)
- Step axis annotation layer active: calendar date and event label on every step
  marker per Decision 11 requirements
- Multi-case comparison: two sets of historical curves on the same step axis,
  aligned by programme step (key decision event as Step 1), not by calendar date

*Mode 2 (Simulation):*
- Projected trajectory curves; scenario label on curves
- Step axis displays step indices and projected calendar dates; no event labels
  (forward scenario — no historical events to annotate)

*Mode 3 (Active Control):*
- Observation mode before first control input: single trajectory set (baseline),
  no ghost curves
- After first control input applied: baseline curves (ghost) at 50% opacity,
  1px stroke; active curves at 100% opacity, 2px stroke — simultaneously, without
  any additional user action (see Decision 9)
- Divergence fill region: where active and baseline curves separate, the area
  between them is filled with semi-transparent shading in the active curve's
  framework color (5–10% opacity); appears immediately on computation complete
- Policy inflection markers (blue filled circle) on the specific curve(s) the
  input affects; orange vertical line across all curves for exogenous shocks
  (see Decision 12)
- MDA floor lines overlaid on both baseline and active curves

**Shared step axis state contract:** All instruments in the instrument cluster
subscribe to the same step state. When the user advances a step or a computation
completes, the trajectory view must update in the same render cycle as the MDA
alert panel, PMM widget, and four-framework current position (see Decision 14).

---

### Decision 5 — MDA Alert Panel Specification (Zone 1B)

The MDA alert panel is a Zone 1B co-primary instrument positioned in the primary
viewport — not inside the EntityDetailDrawer.

**Requirements:**
- Top 1–3 alerts visible without scrolling at all supported viewports
- Each alert row must display without expansion: severity (color + label),
  indicator name, step index, top affected cohort
- Severity ordering: TERMINAL before CRITICAL before WARNING
- Framework source visible per alert row without requiring a framework tab to open
- Alert entries are interactive: tapping an alert expands to show the trajectory
  view for that indicator at that step — not the entity drawer
- The mechanism for showing the indicator trajectory detail must keep the trajectory
  view (Zone 1A) visible — a full-screen overlay occluding the instrument cluster
  is not acceptable. The specific rendering mechanism (inline expansion, sidebar,
  coordinated trajectory view update) is a Frontend Architect brief decision.

**Mode-specific behavior:**

*Mode 1 — Alert tense is historical:* Alerts are facts about what happened.
Language: "[indicator] crossed [severity] threshold at step N."

*Mode 2 — Alert tense is projected:* Alerts are warnings about what will happen
if the scenario continues. Language: "[indicator] is projected to cross [severity]
threshold at step N."

*Mode 3 — Alert tense is live:* Alerts fire in real time as control inputs
propagate. Causal attribution is required per alert:

```
CRITICAL — poverty_headcount — bottom_quintile — step 3
Caused by: −2% spending cut applied at step 3
```
or
```
WARNING — social_cohesion — all_cohorts — step 3
Caused by: Scenario shock — snap election, step 3
```
or
```
WARNING — social_cohesion — all_cohorts — step 3
Caused by: Multiple inputs (see trajectory view)
```

The causal attribution is the negotiating instrument. "This path crosses the
threshold because of the consolidation trajectory" is a categorically different
negotiating claim from "this path crosses the threshold because an exogenous
shock overwhelmed the policy framework."

**Confidence tier → negotiation-defensibility label (required in Mode 2 and 3):**

| Tiers | Displayed label |
|---|---|
| 1–2 | "High confidence — cite directly" |
| 3 | "Moderate confidence — cite with caveat" |
| 4–5 | "Exploratory — do not cite" |

Raw tier numbers are not displayed in the alert panel. The negotiation-defensibility
label is the user-facing translation of the tier system.

---

### Decision 6 — PMM Widget Specification (Zone 1C)

The Policy Maneuver Margin widget is a Zone 1C co-primary instrument with its
own dedicated visual identity — not a row in a FrameworkPanel, not a subtitle
under another element.

**Requirements:**
- Visible without scrolling at minimum supported viewport
- Direction indicator (arrow or trend line) showing whether margin is growing or
  shrinking since the last step
- Label legible to a non-specialist: "Policy Maneuver Margin" is acceptable;
  "coffin_corner_index" is not
- Null value must be rendered as "—" (instrument in validation), not as zero

**Mode-specific header label:**

| Mode | PMM widget header label |
|---|---|
| Mode 1 (Replay) | "Policy Maneuver Margin — historical" |
| Mode 2 (Simulation) | "Policy Maneuver Margin — projected" |
| Mode 3 (Active Control) | "Policy Maneuver Margin — current" |

In Mode 3, the trend arrow updates after each control input computation — not
after each user interaction, but after the computation resolves. During computation
the widget shows a pending update state (greyed out). In Mode 1, the trend arrow
reflects the historical trajectory and does not change in response to user action.

---

### Decision 7 — Four-Framework Current Position Specification (Zone 1D)

The four-framework current position is a Zone 1D co-primary instrument: a
quick-read number readout of the four composite scores at the current step.

**Requirements:**
- All four values visible simultaneously — no tabs, no toggles
- Human-readable framework labels: "Financial", "Human Development", "Ecological",
  "Governance"
- Current step value shown as a number per framework
- Null axes visually distinct from zero-value axes: a null governance score
  (instrument in validation) must not render identically to a governance score
  of 0.0; a "—" label and dashed border differentiate them
- Updates atomically when a step advances or a control input computation completes
  (see Decision 14)

---

### Decision 8 — Radar Chart and Framework Panels (Zone 2A and 2B)

**Radar Chart (Zone 2A):**

The radar chart moves from Zone 1 (M8 position) to Zone 2A by EL Decision 2.
The four-framework current position (Zone 1D) provides the Zone 1 quick-read;
the radar chart provides the spatial depth and deformation view behind it.

Requirements:
- All four axes visible simultaneously — no tabs, no toggles
- Axis labels human-readable: "Financial", "Human Development", "Ecological",
  "Governance"
- Each axis shows the composite score value alongside the visual position
- Step-to-step transitions animated 200–300ms ease-in-out
- Null axes visually distinct from zero-value axes (same rule as Zone 1D)
- Accessible via one scroll or one tab action from Zone 1; does not require
  opening a separate drawer or navigating away from the instrument cluster

**Framework Panels (Zone 2B):**

- Indicator display names human-readable (e.g., `rule_of_law_percentile` →
  "Rule of Law (global percentile)")
- Confidence tier visible per indicator row without expanding
- In Mode 3, confidence tier badges are interactive: tapping a badge opens the
  methodology note for that indicator (satisfies Premise 6 / Decision 16)
- Cohort breakdown visible by expanding an indicator row — one click, not a
  separate navigation

---

### Decision 9 — Comparison Mode Conditional (EL Decision 3)

The comparison surface is context-dependent. The conditional rule applies across
all three modes.

**Mode 2 — Single-entity scenarios:**
COMPARE_VIEW Zone 1: Divergence timeline — two scenario trajectory curves
(proposed path and counter-proposal) on the shared step axis. Delta alert panel
shows which MDA alerts fire in the primary scenario but not the comparison
scenario (step-level severity delta, not binary fire/no-fire).

COMPARE_VIEW Zone 1 header — Fiscal equivalence header: a single-line calculation
visible without navigation: "Counter-proposal achieves X% of 5-year primary
surplus target." This is visible in the comparison view header, not in Zone 3.

DeltaChoropleth is not the Zone 1 surface for single-entity Mode 2 comparisons.

**Mode 2 — Multi-entity scenarios:**
COMPARE_VIEW Zone 1: DeltaChoropleth — geographic divergence between scenarios,
color-coded by direction and magnitude.

**Mode 3 — Active Control:**
No COMPARE_VIEW state is entered. The instrument cluster's trajectory view always
shows baseline ghost curves (50% opacity) alongside active trajectory curves
(100% opacity) from the moment the first control input is applied. The comparison
is automatic — not invoked. See Decision 10 for the full live A/B specification.

DeltaChoropleth has no role in Mode 3 comparisons. Mode 3 comparison is always
temporal (baseline trajectory vs. live modified trajectory), never geographic.

**Comparison prompt on second scenario completion (Mode 2):** When a second
scenario computation completes, the interface prompts automatically: "Both
scenarios are complete. View comparison?" with a single-action confirmation.
This prompt is not required for user-initiated compare actions.

---

### Decision 10 — Mode 3 Live A/B Comparison

**Invocation model:** The live A/B comparison is automatic — not invoked by
the user. No "enable comparison" button, no "show baseline" toggle.

Before any control input is applied: trajectory view shows a single trajectory
set (observation mode). No ghost curves. No comparison state.

After the user applies the first control input: the baseline trajectory is
preserved as ghost curves. The active trajectory updates to reflect the control
input. The user sees both simultaneously — no additional action required.

When multiple control inputs are applied: the active trajectory accumulates all
control inputs. The baseline does not change — it is always "the trajectory
before any control inputs." The comparison always answers: "What is the total
effect of all my control inputs?"

**Preconditions for live A/B comparison:**
1. A completed baseline scenario (at least one step computed before the first
   control input)
2. At least one applied control input
3. Shared step axis between baseline and active (same scenario, two states)

**Visual specification:**

| Element | Specification |
|---|---|
| Baseline curves (ghost) | Same color as active curve per framework; 50% opacity; 1px stroke; fully interactive (hover/tap shows baseline value) |
| Active curves | 100% opacity; 2px stroke; the "current trajectory" as modified by all applied control inputs and injected shocks |
| Divergence fill | Area between baseline and active curves filled with semi-transparent shading in the active curve's framework color (5–10% opacity); appears immediately when divergence exists; disappears if trajectories re-converge |
| MDA floor lines | Overlaid on both baseline and active curves as horizontal dashed threshold lines |

---

### Decision 11 — Mode 1 Step Axis Annotation

In Mode 1, the step axis is the primary legibility bridge between the simulation's
coordinate system (steps) and the users' coordinate system (calendar dates,
political events). Without this annotation, the step axis serves the Finance
Ministry Negotiator (Persona 2) while remaining opaque to the Political Advisor
(Persona 3) and the Institutional Decision-Maker (Persona 5).

**Three mandatory fields on every Mode 1 step marker:**

| Field | Type | When required | Source |
|---|---|---|---|
| Step index | Integer label (e.g., "Step 1") | Always | Step counter |
| Calendar date | `MMM YYYY` (e.g., "Dec 2001") | Always | Scenario fixture `effective_from` field |
| Event label | String, ≤ 8 words, plain language | Required on SIGNIFICANT steps; omitted on ROUTINE steps | Scenario fixture `step_event_label` field |

**Fixture schema requirements (binding for all Mode 1 scenarios):**

Every Mode 1 scenario fixture must include the following fields per step:

| Field | Type | Required | Notes |
|---|---|---|---|
| `effective_from` | ISO 8601 date | Always mandatory | Source for calendar date display |
| `step_event_label` | string, ≤ 8 words | Mandatory for SIGNIFICANT steps; null permitted for ROUTINE | Cannot be absent for any SIGNIFICANT step |
| `step_significance` | enum: `SIGNIFICANT` \| `ROUTINE` | Always mandatory | SIGNIFICANT = three-field display; ROUTINE = step index + date only |

A Mode 1 fixture with any SIGNIFICANT step missing `step_event_label` is
incomplete and must not pass CI. This is a fixture completeness gate, enforced
at fixture creation time via schema validation — not at render time.

**Rendering requirements:**

*Standard viewport (≥ 1024px):* All three fields visible on every step marker.
Event label omitted for ROUTINE steps.

*Narrow viewport (< 768px):* Step index and calendar date visible. Event label
truncates to a tooltip accessible via tap/hover.

*Step marker click behavior:* Clicking any step marker navigates all instruments
in the cluster to that step simultaneously — in a single render cycle (see
Decision 14). Every instrument updates at once; sequential updates violate the
shared step axis invariant.

**In Mode 2 and Mode 3:** The step axis displays step indices and projected
calendar dates. Event labels are not displayed — forward scenarios have no
historical events to annotate.

**Multi-case Mode 1 comparison alignment:** When two historical entities are
compared in Mode 1 (e.g., Argentina 2001 and Iceland 2008), step axis alignment
is by programme step (key decision event as Step 1 for each entity), not by
calendar date. The `step_significance = SIGNIFICANT` key event is the alignment
anchor for each entity.

---

### Decision 12 — Blue/Orange Cross-Layer Visual System

In Mode 3, policy inputs (deliberate user decisions) and exogenous shocks
(environmental events the user is testing against) both change the trajectory.
Their visual distinction must be scannable by the user without reading alert text.

**Blue = policy input. Orange = exogenous shock.**

This assignment is a cross-layer contract. The colors are not used for any other
purpose in the UI. A user who has learned the distinction at the control plane
can scan the trajectory view and alert panel and immediately identify the cause
of any trajectory change.

**Layer 1 — Control Plane:**

Policy instruments form: blue icon, blue "Apply policy input" confirm button,
blue entries in "Applied inputs" history list.

Scenario shocks form: orange icon, orange "Inject scenario shock" confirm button,
orange entries in "Injected shocks" history list.

Shock type taxonomy: `ElectionShock`, `CurrencyAttack`, `CreditorDefection`,
`GeopoliticalShock`, `NaturalDisaster`, `ContagionShock`.

The policy instruments form and scenario shocks form must be visible simultaneously
in Mode 3 — the visual separation is an epistemic requirement, not a layout
preference. The control plane zone must be sized to accommodate both without scroll
(see Decision 15).

**Layer 2 — Trajectory View:**

Policy inflection markers: filled blue circle at the step where input was applied,
on the specific curve(s) the input affects; short inline label (e.g., "−2%
spending cut"); click shows ControlInput parameters in tooltip.

Shock event markers: orange vertical line at the step where shock was injected,
extending across all four framework curves; orange label at top of line (e.g.,
"SHOCK: Snap election, step 3"); click shows shock type and parameters in tooltip.

When both a policy input and a shock occur at the same step: both markers appear
simultaneously and must not merge — the blue dot on affected curves and the orange
vertical line across all curves are visually distinct even when co-located.

**Layer 3 — MDA Alert Panel:**

Causal attribution per alert per Decision 5. The prefix "Caused by:" followed by
either the policy input description (plain language) or the shock type must appear
in every Mode 3 alert for which causation is attributable.

**What must not happen:** Any violation of cross-layer color consistency —
blue used for shocks, orange used for policy inputs, or either color repurposed
for a different UI element in the same viewport zone.

**Accessibility:** Color is not the only distinguishing element — the shape
difference (filled circle for policy inputs; vertical line for shocks) must
also be consistent across all three layers, ensuring legibility for users with
color vision deficiencies.

---

### Decision 13 — Confidence Tier Visual Differentiation

A Tier 4 (SYNTHETIC_MODEL) instrument that looks visually identical to a Tier 1
(MEASURED_OFFICIAL) instrument violates Premise 2. The epistemic standing of the
instrument must be present on the instrument face — not only in Zone 3 methodology
documentation.

**Trajectory view curve treatment by tier:**

| Tier | Curve treatment |
|---|---|
| Tier 1–2 (MEASURED or REPORTED) | Solid curve, 100% opacity, no uncertainty band |
| Tier 3 (SYNTHETIC_COMPARABLE) | Solid curve, 75% opacity, uncertainty band (width ADR-007-gated — see note) |
| Tier 4–5 (SYNTHETIC_MODEL / STRUCTURAL_ABSENCE) | Dashed curve, 60% opacity, uncertainty band (width ADR-007-gated — see note), confidence badge adjacent to curve label |

**Uncertainty band widths (Tier 3-5):** Uncertainty band at width defined in
ADR-007 (synthetic data framework) — Tier 3-5 band rendering is gated on ADR-007
acceptance. Until ADR-007 is accepted, the visual differentiation (75% opacity
solid / 60% opacity dashed / confidence badge) is implemented; band width rendering
is deferred.

**MDA alert behavior by tier:**

| Tier | Alert behavior |
|---|---|
| Tier 1–2 | Full severity fires (WARNING / CRITICAL / TERMINAL) |
| Tier 3 | Full severity fires, plus "(moderate confidence)" qualifier on alert text |
| Tier 4–5 | WARNING-only regardless of computed severity, plus "(exploratory — do not cite)" badge. No CRITICAL or TERMINAL alerts from Tier 4–5 data. |

The WARNING-only rule for Tier 4-5 does not mean the crossing is less severe —
it means the epistemic standing of the data does not support a CRITICAL or TERMINAL
claim with the confidence those labels carry. The severity labels carry an implicit
confidence claim about the data quality underlying the crossing. A CRITICAL alert
from Tier 1-2 data is a different kind of statement than a CRITICAL alert from
SYNTHETIC_MODEL data. The former can be cited in a negotiation; the latter cannot.
The severity label system must remain honest about this distinction.

**Tier 4–5 instruments are not suppressed.** The governance signal, even as an
exploratory estimate, is never moved to Zone 3 or hidden. Suppression would
violate the human cost ledger principle (CLAUDE.md §Guiding Principles). The
visual differentiation communicates epistemic quality without hiding the signal.

**Confidence tier badges (Zone 2B, Framework Panels):** Badges are interactive
in Mode 2 and Mode 3 — tapping any badge opens the methodology note for that
indicator (confidence tier justification, source data vintage, comparison group
if synthetic). This satisfies Premise 6 and Decision 16.

---

### Decision 14 — Simultaneous Instrument Update Contract

All Zone 1 instruments (trajectory view, MDA alert panel, PMM widget,
four-framework current position) subscribe to the same state update signal. A
single computation-complete event triggers all four instrument updates in one
render cycle — not four sequential update events.

**Trigger events that must produce a single-render-cycle update:**
- User advances a step (Mode 1, Mode 2)
- A control input computation resolves (Mode 3)
- The user switches the primary entity (multi-entity scenarios)
- The user navigates to a different step via step marker click

**Partial update violation:** A state where the trajectory view shows the new
step while the MDA alert panel still shows the previous step is a violation of
the shared step axis invariant (Premise 3). The Frontend Architect must ensure
that no combination of loading states, async resolution order, or React render
batching produces this state.

**Computation state during Mode 3 control input propagation:**
- Input registration: immediate (within one render cycle). The control input
  appears in the "Applied inputs" history list before computation begins.
- Computation acknowledgment: affected trajectory curves show "computing" state
  (e.g., subtle pulse animation). PMM widget and four-framework current position
  show "pending update" state. MDA alert panel shows "updating alerts" state.
- Computation complete: all affected instruments update simultaneously in a
  single render cycle.

---

### Decision 15 — Mode Transition Design

**Transitions are explicit user actions.** The user cannot accidentally transition
to a different mode by interacting with an instrument. Tapping a trajectory curve,
expanding an alert, or navigating a step does not cause a mode transition. The
three labels in the mode indicator (Decision 3) are the only transition triggers.

**Single modal confirmation rule:** If a mode transition would discard unsaved
work (e.g., Mode 3 session with applied control inputs), a single-sentence
confirmation is required: "Your Mode 3 session has N applied control inputs.
Leave Mode 3?"

This is the only modal confirmation in the entire interaction model. All other
actions are non-modal.

**Transition states:**

*Mode 1 → Mode 2:*
- Scenario configuration surface populates the control plane zone
- Event annotation layer on step axis deactivates
- PMM header label changes to "projected"
- Historical session state preserved in session history

*Mode 2 → Mode 3:*
- Control plane zone populates with policy input and scenario shock forms
- PMM header label changes to "current"
- Live A/B comparison state initializes (observation mode — single trajectory
  set, no ghost curves — until first control input is applied)
- Unsaved Mode 2 scenario parameters preserved

*Mode 3 → Mode 1:*
- Control plane zone returns to empty reserved state
- Event annotation layer activates on step axis
- PMM header label changes to "historical"
- All applied control inputs from the Mode 3 session preserved in session
  history log (not silently discarded)

**Instruments that persist unchanged across all three modes:**
- Trajectory view (what changes: annotation layer, ghost curves, Mode 3 markers)
- MDA alert panel (what changes: alert tense, causal attribution)
- Four-framework current position (what changes: which step is "current")
- Step axis as shared coordinate system (what changes: annotation layer)

**Instruments that are mode-specific:**
- Control plane forms (Mode 3 only; zone empty in Mode 1, scenario config in Mode 2)
- Event annotation layer on step axis (Mode 1 only)
- PMM widget header label (mode-specific text per Decision 6)
- Delta alert panel structure (Mode 2: named scenario comparison;
  Mode 3: baseline vs. active — structurally different, same Zone 1B position)

---

### Decision 16 — Methodology Documentation Accessibility (Premise 6)

Methodology documentation must be accessible within one interaction of any
instrument output. This closes the gap the original five premises left for the
Evaluative and Retrospective entry states (Amara Diallo, Persona 4 — Academic
Researcher).

**Implementation:**
- Confidence tier badges in Zone 2B are interactive: one tap opens the methodology
  note for that indicator (confidence tier justification, source data vintage,
  comparison group if synthetic estimate)
- The methodology note must open in-place (expandable panel or inline drawer)
  without navigating away from the instrument cluster
- Zone 3 contains the full methodology text (ia1_disclosure, ecological note,
  model limitation documentation) — accessible via one deliberate navigation
  action ("ⓘ Methodology notes" expandable link or equivalent)

**What must not happen:** A methodology note that requires more than one
interaction from within the instrument cluster to access. If the path is
Zone 1 instrument → Zone 3 methodology note without a Zone 2 intermediate
step accessible in one action, the accessibility contract is violated.

---

### Decision 17 — Control Plane Reserved Zone (Premise 5)

A dedicated screen zone is reserved in the primary viewport layout for the Mode 3
control plane from M9 onward. The zone is reserved before Mode 3 is built — not
retrofitted when Mode 3 arrives.

**Location:** A persistent zone adjacent to the trajectory view in the primary
viewport. In Mode 1 and Mode 2, this zone holds no content and is not hidden or
collapsed — it is reserved (visible as whitespace). In Mode 3, it is populated
with the control plane.

**Minimum Mode 3 zone content (used to size the zone from M9):**

The reserved zone must accommodate simultaneously, without requiring scroll to
see either form:
- Policy instruments form: control input type selector, parameter field(s),
  step selector, "Apply policy input" button, applied inputs history list
  (blue visual treatment throughout)
- Scenario shocks form: step selector, shock type selector from taxonomy,
  "Inject scenario shock" button, injected shocks history list (orange visual
  treatment throughout)

Both forms must be visible simultaneously. The visual separation between policy
inputs (blue) and exogenous shocks (orange) is an epistemic requirement (Decision
12) — not a layout preference.

**Sizing constraint:** The control plane zone must not reduce the trajectory view
below a minimum legible width at the desktop minimum viewport (1280×800). The
trajectory view (Zone 1A) is the primary instrument. The control plane zone is
adjacent but secondary. If the zone sizes create a conflict, the trajectory view
wins. The Frontend Architect must specify the minimum trajectory view width at
1280×800 in the M9 implementation brief and confirm the control plane zone is
sized within that constraint.

---

## Alternatives Considered

### Alternative 1: Case A — Incremental Enhancement of M8 Architecture

**Description:** Keep the choropleth as primary viewport, expand the
EntityDetailDrawer, and improve instrument visibility within it. Move the MDA
alert panel to the top of the drawer. Make the drawer wider (35% instead of 25%).
Defer the viewport inversion to Mode 3 introduction.

**Why rejected:** The EntityDetailDrawer's fundamental constraint is that it
requires user action to open. Mode 3 requires instruments to be always visible
without navigation (R1). An always-visible drawer is no longer a drawer — it is
a split viewport. The "incremental" path terminates at the same architectural
destination as Case B, but with the additional cost of M9 frontend work built on
the wrong substrate that must be replaced at Mode 3 introduction. The UX Design
Thinking Agent first-principles review (PR #390) made this case explicitly.
Deferring the viewport inversion creates a larger M10 migration, not a smaller M9
scope.

### Alternative 2: Case C — Full Rebuild Without Control Plane Reservation

**Description:** Execute the viewport inversion (instrument cluster as primary
viewport) but do not reserve the control plane zone until Mode 3 design is
complete. Place the control plane reservation when its dimensions are known.

**Why rejected:** The control plane zone sizing depends on simultaneously
accommodating both the policy instruments form and the scenario shocks form
without scroll. At Mode 3 introduction, if the control plane zone is retrofitted,
it will compete with the trajectory view (Zone 1A) for viewport real estate.
A trajectory view compressed below minimum legible width at 1024×768 would
violate Premise 2. Reserving the zone from M9, when the layout is flexible,
costs nothing. Retrofitting it at Mode 3 entry costs trajectory view legibility.
Premise 5 closes this risk at the earliest possible moment.

### Alternative 3: DeltaChoropleth as Universal Comparison Surface

**Description:** Use the DeltaChoropleth as the primary Zone 1 comparison surface
for both single-entity and multi-entity Mode 2 scenarios, and for Mode 3.

**Why rejected:** The DeltaChoropleth answers "which entities diverge and in which
direction?" This is the correct primary question only for multi-entity Mode 2
scenarios. For single-entity Mode 2 scenarios, both scenarios model the same
entity — geographic divergence is not the primary question; step-level threshold
crossing timing is. For Mode 3, comparison is always temporal (baseline trajectory
vs. live modified trajectory), never geographic. A DeltaChoropleth in Mode 3
would answer the wrong question entirely. EL Decision 3 established the
conditional rule explicitly for this reason.

### Alternative 4: User-Invoked A/B Comparison in Mode 3

**Description:** Require the user to explicitly invoke the live A/B comparison
in Mode 3 (e.g., a "Show baseline" toggle, or a "Compare" button) rather than
making it automatic on first control input.

**Why rejected:** In Mode 3, "baseline vs. active" is the cognitive task — it is
not an optional view. Making it user-invoked would require an action at the
moment when cognitive load is highest: after applying a control input during an
active negotiation. The user has just proposed a modification to the Troika's
terms. The immediate question is: "What did that change?" A toggle that must be
found and activated before that question can be answered is a failure of the Mode
3 interaction model. The gap analysis (Gap 4,
`docs/ux/design-thinking/worldsim-ux-architecture-first-principles-depth.md`)
established the automatic invocation model for this reason.

### Alternative 5: Per-Mode Separate Instrument Clusters

**Description:** Design three separate instrument cluster layouts — one per mode
— that are activated and deactivated on mode transition.

**Why rejected:** Four instruments persist unchanged across all three modes with
only their content changing (trajectory view, MDA alert panel, four-framework
current position, step axis). Three-instrument-cluster architectures would
require maintaining three separate component trees for instruments that are
structurally identical across modes. The mode-specific differences (annotation
layer in Mode 1, ghost curves in Mode 3, mode-specific PMM label) are parametric
variations of the same components — not structurally different components. The
single instrument cluster with mode-specific parameterization is architecturally
simpler and satisfies all five personas across all three modes.

---

## Consequences

### Positive

**Mode 3 is possible.** The Case B verdict holds: the M8 architecture cannot
accommodate Mode 3 without an inversion of the primary viewport. This ADR executes
that inversion at M9 and makes Mode 3 a consequence of the existing architecture
rather than a structural retrofit.

**All five personas are served.** The trajectory view with mandatory Mode 1 step
annotation (Decision 11) enables both trajectory reconstruction (Personas 1 and 2)
and historical pattern recognition (Personas 3 and 5) within the same instrument
cluster. The Evaluative entry state (Persona 4) gains the one-interaction
methodology access guarantee (Decision 16). The Demonstrative entry state (Persona
5) gains the step-annotated Mode 1 opening screen readable by a cold observer
in 20 seconds.

**The confidence tier system is visible on the instrument face.** Tier 4 instruments
are not suppressed (human cost ledger principle) and do not look identical to Tier
1 instruments (No False Precision principle). Both obligations are met simultaneously.

**The causal attribution system makes the negotiation argument traceable.**
"This crossing is caused by the consolidation trajectory" and "this crossing is
caused by the exogenous shock" are categorically different negotiating claims that
the blue/orange system makes scannable without reading alert text.

**Step annotation closes the legibility gap for non-analyst users.** Without the
Mode 1 step annotation, the shared step axis serves Lucas and Eleni while remaining
opaque to Andreas and Aicha. With it, the same instrument cluster serves all four
Mode 1 personas.

### Negative

**The M8 EntityDetailDrawer layout must be replaced.** The radar chart, MDA alert
panel, and PMM widget are currently inside the drawer. Moving them to the primary
viewport is a non-trivial frontend refactor. Existing frontend implementation code
that assumes a drawer-first layout must be restructured.

**The control plane reserved zone increases layout complexity at M9** even though
it is empty in Mode 1 and Mode 2. A reserved-but-empty zone requires explicit
layout discipline to maintain — there will be pressure to use it for other content
before Mode 3 arrives.

**The simultaneous instrument update contract (Decision 14) constrains the state
management architecture.** A four-instrument atomic update on computation complete
requires a state management approach that guarantees render batching across all
four components. React 18 automatic batching reduces the implementation burden
but does not eliminate it; the Frontend Architect must confirm the atomicity
contract is satisfied under async resolution patterns.

**The Mode 1 step annotation fixture requirement (Decision 11) creates a CI gate**
that will fail existing fixtures that do not include `step_event_label` on SIGNIFICANT
steps. The Greece fixture must be audited and completed before this gate is active.

**Radar chart demotion from Zone 1 to Zone 2** is a visually significant change
that existing demo materials and documentation reference as Zone 1. All screenshots,
walkthroughs, and documentation referencing the M8 radar chart position must be
updated before M10 Demo 3.

### Open Risks

**Tablet performance at 1024×768 with all four Zone 1 instruments visible
simultaneously:** The trajectory view (four animated curves), MDA alert panel
(potentially live-updating in Mode 3), PMM widget, and four-framework position
must all be visible without scroll at 1024×768. The Frontend Architect must validate
at M9 implementation entry that the component layout satisfies the viewport
constraint on the target hardware (8GB RAM, 4-core laptop per equitable build
requirement).

**Control plane zone sizing conflict:** The reserved zone must accommodate two
forms simultaneously without reducing the trajectory view below minimum legible
width. The sizing specification ("visible without scroll" for both forms
simultaneously) was derived from the Gap 3 epistemic requirement — the forms must
be visually separated. If hardware constraints at 1024×768 force a conflict,
the trajectory view wins and the control plane zone requires a scroll affordance
for one form. This is a Mode 3 implementation decision; the M9 reservation must
document the minimum zone width so the conflict is evaluated at M10 rather than
discovered at Mode 3 introduction. The EL ruling on FA-C3 (2026-05-22) specifies
Option A: stacked forms, ~280px reserved zone. "Simultaneously visible" means both
form headers visible without scroll, not all form fields.

**Zone 1 co-primary spatial arrangement:** The relative positions of Zone 1B (MDA
alert panel), 1C (PMM widget), and 1D (four-framework current position) with respect
to each other and to Zone 1A (trajectory view) are a Frontend Architect brief
requirement. The brief must demonstrate simultaneous scannability of all Zone 1
elements at 1024×768 and document MDA alert panel primacy among co-primary
instruments (severity ordering: TERMINAL > CRITICAL > WARNING governs arrangement,
not framework ordering).

---

## Diagram

Viewport zone architecture: `docs/architecture/ADR-008-viewport-zones.mmd`

The diagram shows the relationship between the primary viewport (instrument
cluster), the persistent header (mode indicator, entity selector), Zone 1/2/3
disclosure levels, the control plane reserved zone, the navigable geographic
context, and the EntityDetailDrawer. The control plane zone's three modal states
(empty in Mode 1, scenario configuration in Mode 2, policy instruments and scenario
shocks forms in Mode 3) are shown as mode-conditional content within a persistent
layout zone.
