# Information Hierarchy — WorldSim Dashboard

> Last significant revision: 2026-06-26
> Updated against: GD Artifact 2 (#1354) — Control Plane Reserved Zone expanded: Mode 1 confirmed; Mode 2 column content designed for first time (closes GA-02); Mode 3 specification consolidated and shock taxonomy extended with GrowthShock; mode transition behavior specified; CVD color values documented
> Previous version context: 2026-06-06 — NB-7 (Mode 1 COMPARE_VIEW spec; closes Issue #451)

> Owned by the UX Designer Agent. This document defines the visual weight
> and disclosure depth of every element on the WorldSim dashboard. It is
> the reference for all Frontend Architect decisions about layout, ordering,
> and progressive disclosure. When a proposed component placement conflicts
> with this hierarchy, this document governs — not implementation convenience.
>
> Last updated: 2026-06-06 (NB-7 — Mode 1 COMPARE_VIEW spec completed; entry point
> resolved to inline fixture picker in Zone 2 scenario browser; single-call API design
> decision documented; US-049 Persona 3 user story added; closes Issue #451).

---

## Governing Principle

The information hierarchy exists to serve the primary cognitive task of the
active mode: trajectory reconstruction and historical pattern recognition
(Mode 1), threshold-safe path construction (Mode 2), or real-time steering
within human cost constraints (Mode 3). Per-mode cognitive tasks are
established in `north-star.md §Primary Cognitive Tasks by Mode`.

Every hierarchy decision is evaluated against this question:

> Does this placement allow the user to complete the primary cognitive task
> of the active mode within the time constraints of that mode — under
> 30 seconds in Mode 3, under 5 minutes in Mode 2 preparation, without
> navigating away from the primary viewport in any mode?

Elements that serve the active mode's primary task directly occupy primary
position. Elements that support it once the initial question is answered
occupy secondary position. Elements that require exploration occupy tertiary
position — accessible, but not competing with the primary scan.

**Foundational rule (EL Decision 2):** The primary viewport is the instrument
cluster. The choropleth is a navigable context surface. The EntityDetailDrawer
is a detail and methodology surface. No primary instrument lives inside the
drawer or requires choropleth interaction to reach.

---

## The Three Disclosure Zones

### Zone 1 — Primary (no interaction required)

Visible on page load or on drawer open, without scrolling, at any viewport
likely to be used in a negotiation room (desktop 1280×800 minimum,
tablet 1024×768 minimum). Occupies the upper portion of each view.

**The user must be able to complete the primary cognitive task from Zone 1
alone.** If the answer to "has anything crossed a threshold?" requires
leaving Zone 1, the hierarchy is wrong.

### Zone 2 — Secondary (one scroll or one click)

Visible after a single scroll or a single expand/tab action. Provides the
evidence behind the Zone 1 signal: indicator detail, confidence tier,
cohort breakdown, trajectory values. This is the preparation-mode surface.

### Zone 3 — Tertiary (deliberate navigation)

Requires two or more interactions: a click to expand, then a scroll, or
a tab change then a read. Contains methodology disclosures, raw indicator
tables, historical comparison data, and model limitation documentation.
In negotiation mode, Zone 3 content is never needed. In preparation mode,
it supports the argument-building phase but is never the first stop.

---

## Dashboard View Hierarchy (SCENARIO_VIEW / SCENARIO_COMPLETE)

### Persistent Header — Entity Selector

Above all zones, always visible regardless of mode, drawer state, or interaction
state. This element does not belong to any zone — it is always present.

In a single-entity scenario, shows the entity name. In a multi-entity scenario,
shows a selector that allows the user to switch entity without navigating away
from the instrument cluster. The entity selector is never inside a drawer, never
behind a navigation action.

Requirements:
- Visible and functional in Mode 1, Mode 2, and Mode 3 without any scroll or
  navigation action
- In multi-entity scenarios, the selector must list all entities in the scenario
  with their current-step composite score visible per entity
- Entity switch must update all four Zone 1 instruments atomically — not one at
  a time, not with separate loading states per instrument

---

### Zone 1 — Primary

**1A — Trajectory View** *(highest weight — primary instrument)*

Four composite score curves (financial, human development, ecological, governance)
on a shared step axis. This is the primary Zone 1 instrument. It makes
multi-framework trajectory comparison legible at a glance in all three modes.

The trajectory view is positioned in the primary viewport — not inside the
EntityDetailDrawer, not behind a tab or navigation action.

Requirements:
- Four framework curves visible simultaneously on a single shared step axis
- Shared step axis with mode-specific annotation:
  - Mode 1: step index + calendar date + event label for SIGNIFICANT steps
    (mandatory fixture fields: `effective_from`, `step_event_label`,
    `step_significance`; see Gap 1B, PR #390)
  - Mode 2: step index + projected calendar date
  - Mode 3: step index + projected calendar date; baseline ghost curves
    (50% opacity, 1px stroke) appear automatically when the first control
    input is applied
- MDA floor lines overlaid as horizontal dashed threshold lines on each curve
- Mode 3 live A/B: baseline curves (50% opacity, 1px) and active curves
  (100% opacity, 2px) simultaneously; divergence fill region (5–10% opacity)
  where they separate — automatic, no user action required to invoke
- Policy inflection markers (blue) and shock event markers (orange vertical
  line across all curves) per Gap 3 cross-layer visual system (PR #390)
- Step transitions animated 200–300ms ease-in-out
- Trajectory view occupies the primary viewport at all supported viewport
  sizes (desktop 1280×800 minimum, tablet 1024×768 minimum) without requiring
  any navigation

**1B — MDA Alert Panel** *(co-primary)*

Threshold crossing alerts from the trajectory computation. Positioned within
the primary viewport (instrument cluster) — not inside the EntityDetailDrawer.
In Mode 3, alerts fire in real time as control inputs propagate.

Requirements:
- Top 1–3 alerts visible without scrolling at all supported viewports
- Each alert row: severity (color + label), indicator name, step index, top
  affected cohort — all readable without expanding
- Severity ordering: TERMINAL before CRITICAL before WARNING
- Framework source visible per alert (financial / human_development /
  ecological / governance) without requiring a framework tab to open
- Mode 3 causal attribution per alert: "Caused by: [policy input description]"
  or "Caused by: [shock type]" or "Caused by: Multiple inputs (see trajectory
  view)" — this attribution is the negotiating instrument
- Alert tense is mode-dependent: historical fact (Mode 1), projected warning
  (Mode 2), live update (Mode 3)

**1C — PMM Widget** *(co-primary)*

The Policy Maneuver Margin: remaining degrees of policy freedom before the
corrective maneuver window closes.

Requirements:
- Dedicated visual treatment: not a row in FrameworkPanel, not a subtitle
  under another element — a distinct widget with its own visual identity
- Direction indicator (arrow or trend line) showing whether margin is growing
  or shrinking since the last step
- Mode-specific header label: "Policy Maneuver Margin — historical" (Mode 1),
  "Policy Maneuver Margin — projected" (Mode 2), "Policy Maneuver Margin —
  current" (Mode 3); in Mode 3, the trend arrow updates after each control
  input computation
- Visible without scrolling at minimum supported viewport
- Label legible to a non-specialist: "Policy Maneuver Margin" acceptable;
  "coffin_corner_index" is not

**1D — Four-Framework Current Position** *(co-primary)*

The four composite score values at the current step — a quick-read number
readout serving as the flight instrument analog to an altimeter cluster.

Requirements:
- All four values visible simultaneously — no tabs, no toggles
- Human-readable framework labels: "Financial", "Human Development",
  "Ecological", "Governance"
- Current step value shown as a number per framework
- Null axes visually distinct from zero-value axes (distinct treatment, e.g.,
  dashed border, "—" label) — a null governance score and a zero governance
  score are categorically different
- Updates atomically when a step advances or a control input is applied

---

### Zone 2 — Secondary

**2A — Radar Chart**

The four-dimensional deformation view: composite scores for all four frameworks
plotted on a radar axis at the current step. Provides the visual argument that
a country's situation cannot be understood through one lens. Moved from Zone 1
to Zone 2 by EL Decision 2 — the four-framework current position readout (1D)
provides the Zone 1 quick-read; the radar chart provides the Zone 2 visual depth.

Requirements:
- All four axes visible simultaneously — no tabs, no toggles, no "click to
  see ecological"
- Axis labels human-readable: "Financial", "Human Development", "Ecological",
  "Governance"
- Each axis shows the composite score value alongside the visual position
- Step-to-step transitions animated 200–300ms ease-in-out so the user sees
  the deformation happen, not just the result
- Null axes visually distinct from zero-value axes — a partially-filled chart
  with null axes showing as zero is not acceptable
- Accessible via one scroll or one tab action from Zone 1; does not require
  opening a separate drawer or navigating away from the instrument cluster

**2B — Framework Panels** (financial, human_development, ecological, governance)

The four FrameworkPanel tabs contain the indicator detail behind each radar
axis. The user reaches 2B after Zone 1 has confirmed which framework is under
stress — she then opens the relevant tab to examine specific indicators,
confidence tiers, and cohort breakdowns.

Requirements:
- Indicator display names human-readable: `rule_of_law_percentile` → "Rule of
  Law (global percentile)", `co2_concentration_ppm` → "CO2 Contribution (ppm)"
- Confidence tier visible per indicator row without expanding — argument quality
  signal the specialist needs to cite; in Mode 3, confidence tier badges are
  interactive (tapping opens the methodology note for that indicator)
- Cohort breakdown (income quintile, age band) visible within Zone 2 by
  expanding an indicator row — one click, not a separate navigation

**2C — Distribution Bands** (M5 forward)

Uncertainty bands on individual indicators. Visible in Zone 2 after the alert
panel has confirmed which indicators to examine. The band width is the evidence
behind the distribution-source alert.

---

### Zone 3 — Tertiary

**3A — Methodology Notes and Mandatory Disclosures**

All methodology disclosures — ia1_disclosure, the ecological normalization
methodology note, the data source citations — belong in Zone 3. They must
be present (ADR-005 Amendment B mandates the ecological note; ADR-006
Decision 13 mandates ia1_disclosure) but must not compete with Zone 1 or
Zone 2 content for visual attention.

Implementation: collapsed info panel accessible via an (i) icon or
"Methodology notes" expandable link. The collapsed state shows only a
one-line indicator that disclosures are available ("ⓘ Methodology notes
— expand for data limitations and model uncertainty disclosure"). The
expanded state shows the full text.

This is the resolution of UX Gap 2 identified in the M8 demo review: the
mandatory ecological note currently renders inline with the composite score.
It is ADR-compliant at Zone 3 — the note is present and accessible — while
no longer occupying Zone 1 attention.

**3B — Raw Indicator Tables**

Full attribute dumps, source registry IDs, data provenance. For
methodology reviewers and contributor workflows, not for the canonical user
during preparation or negotiation.

**3C — Backtesting Fidelity Dashboard**

The per-case pass/fail fidelity view. Used by analysts calibrating the
model and by methodology reviewers, not by the canonical user in the IMF
negotiation context.

---

## BASELINE_VIEW Hierarchy (no scenario selected)

Zone 1: Scenario list with name, status, entity, and creation date — sorted
by most recently modified. The specialist must be able to identify and select
the correct scenario within 10 seconds (Journey B, Step 1).

Zone 2: Scenario creation entry point. Accessible from Zone 1 without
navigating away.

Zone 3: System status, data source registry, configuration.

---

## COMPARE_VIEW Hierarchy

The comparison surface is context-dependent. EL Decision 3 (Issue #364)
establishes a conditional rule across all three modes.

**Mode 1 — Replay (comparable-case comparison):** *(spec complete — NB-7, closes Issue #451)*

The primary cognitive task in Mode 1 comparison is pattern recognition: does
the current historical trajectory match a recognizable structural precursor?
Persona 3 (Andreas Stefanidis, political advisor) needs to place two historical
trajectories on the same step axis and identify where they diverge — and where
they do not.

**Zone 1:**

Two historical entity trajectory curves on the shared step axis, aligned by
`step_index` from the API response (ADR-010 Decision 11; FA brief §UD-R2 tick
format). The rendering rules:

- **Baseline curve** (primary fixture): solid line, 100% opacity, 2px stroke.
  Values drawn from `steps[].baseline_value` in the `TrajectoryCompareResponse`.
- **Comparison curve** (secondary fixture): ghost curve, 50% opacity,
  `strokeDasharray="4 2"`, 1px stroke. Values drawn from
  `steps[].compare_value` in the `TrajectoryCompareResponse`.
- Step axis uses `steps[].step_index` as the shared alignment axis. Calendar
  dates (`steps[].timestep`) appear as step axis annotations for SIGNIFICANT
  steps, consistent with Mode 1 single-trajectory rendering.
- MDA floor lines overlaid as horizontal dashed threshold lines on both curves.
- Divergence fill region (5–10% opacity) between baseline and comparison curves
  where they separate — rendered automatically when both curves are present.

**Zone 1A — Delta MDA Alert Panel:**

When COMPARE_VIEW is active in Mode 1, the MDA alert panel shows a delta view:
which alerts fire in the primary fixture but not the comparison fixture (and vice
versa). Alert rows that fire in both are shown once, with a "both" indicator.
Alert rows that are fixture-specific carry a label: "primary only" or "comparison
only." This is the structural pattern signal — if the same alert fires in both
fixtures at the same step, the pattern is robust; if it fires only in the primary,
the structural condition is not shared.

**Zone 2 — Inline Fixture Picker (entry point):**

The entry point for Mode 1 COMPARE_VIEW is a "Compare against…" button in the
Zone 2 scenario / fixture browser. This button is visible whenever the active
mode is Mode 1 and a fixture is loaded. Selecting it does not open a modal —
it expands an inline list of available scenarios and fixtures within the Zone 2
panel. The user selects the second fixture from this inline list. Selecting a
fixture sets `compare_scenario_id` and enters COMPARE_VIEW. No navigation away
from the instrument cluster is required.

Exit: an "×" (close comparison) control within the Zone 2 panel clears
`compare_scenario_id` and returns to single-trajectory Mode 1 view.

**Zone 3:** Methodology disclosures for both fixtures.

**API design decision (resolved NB-5, closes Issue #451):**

The Mode 1 comparison uses a **single API call**, not two separate trajectory
fetches:

```
GET /api/v1/scenarios/compare?include_trajectory=true&scenario_id=A&compare_scenario_id=B
```

This returns a `TrajectoryCompareResponse` with a `steps` array of
`TrajectoryCompareStep` objects, each providing:
`step_index, timestep, entity_id, attribute_key, baseline_value, compare_value,
delta, baseline_tier, compare_tier`.

**Rationale for single call over dual call:** Both trajectories share the same
step alignment logic. A single call guarantees that `step_index` values are
aligned server-side before the response is returned — eliminating the client-side
alignment problem that would arise if two separate trajectory calls returned
different step ranges or different `timestep` values for the same conceptual step.
The `delta` field is also computed server-side, removing the need for client-side
subtraction and the rounding risk associated with it. The dual-call pattern was
explicitly considered and rejected during NB-5 implementation (PR #784).

**DeltaChoropleth:** The DeltaChoropleth has no role in Mode 1 comparisons.
Mode 1 comparison is always temporal — two historical trajectories on the same
step axis — not geographic.

**User story (US-049):**

```
US-049: Political advisor compares Greece 2010 trajectory against Argentina 2001 precursor
Actor: Andreas Stefanidis — Political Advisor
Mode: Mode 1 (Replay)
Entry state: Greece 2010-2012 fixture loaded, step 0 visible, single-trajectory view

Given the Greece 2010-2012 historical fixture is loaded in Mode 1 and the Zone 2
  scenario browser is visible
When Andreas clicks "Compare against…" in the Zone 2 fixture browser, the inline
  fixture list expands, and he selects "Argentina 2001-2002"
Then (a) the trajectory view renders two curves — solid for Greece (baseline),
  ghost (50% opacity, strokeDasharray="4 2") for Argentina (comparison);
  (b) the step axis aligns both curves by step_index with calendar date annotations
  for significant steps on each fixture;
  (c) the Zone 1A delta MDA alert panel shows which alerts are "primary only"
  (Greece), "comparison only" (Argentina), or "both";
  (d) the divergence fill region appears between the curves at steps where
  composite scores diverge;
  (e) the Zone 2 panel shows an "×" control to exit COMPARE_VIEW
Tag: [Playwright]
```

**Mode 2 — Single-entity scenarios:**

Zone 1: Divergence timeline — two scenario trajectory curves (proposed path
and counter-proposal) on the shared step axis. The primary question is "at
which step does path A diverge from path B, and which thresholds does path A
cross that B avoids?" The delta alert panel shows which MDA alerts fire in
the primary scenario but not the comparison scenario (or vice versa).

Zone 2: Side-by-side indicator tables for the two scenarios, used in
preparation mode to build the detailed counter-proposal argument.

Zone 3: Methodology disclosures for both scenarios.

The DeltaChoropleth is not the Zone 1 surface for single-entity Mode 2
comparisons — geographic divergence is not the primary question when both
scenarios model the same entity.

**Mode 2 — Multi-entity scenarios:**

Zone 1: DeltaChoropleth — geographic divergence between scenarios, color-coded
by direction and magnitude. The primary question in multi-entity compare mode
is "which entities diverge and in which direction?" and the answer must be
visible immediately.

Zone 2: Entity detail for the entity of interest in the primary scenario —
MDA alerts showing which alerts fire in the primary but not the comparison.

Zone 3: Side-by-side indicator tables for the entities of interest.

**Mode 3 — Active Control:**

The Mode 3 live A/B comparison is automatic — not invoked. No COMPARE_VIEW
state is entered. The instrument cluster's trajectory view always shows
baseline ghost curves (50% opacity) alongside active trajectory curves (100%
opacity) from the moment the first control input is applied. See Zone 1 / 1A
requirements for the visual specification.

The DeltaChoropleth has no role in Mode 3 comparisons. The comparison in
active control is always temporal (baseline trajectory vs. live modified
trajectory), not geographic.

### Zone 1A — Confidence Display

**Binding ruling (DP-1, 2026-06-06):** The confidence band displayed in Zone 1A
is derived from `uncertainty_range_pct` on the composite Quantity. Rendering rules:

| `uncertainty_range_pct` | Band rendered | Label |
|---|---|---|
| ≤ 5 % (Tier 1) | Full opacity confidence band | High confidence |
| ≤ 15 % (Tier 2) | Full opacity confidence band | Moderate confidence |
| ≤ 30 % (Tier 3) | Reduced opacity confidence band | Research estimate |
| ≤ 50 % (Tier 4) | Reduced opacity confidence band | Model estimate |
| `None` (Tier 5) | **No confidence band rendered** | Directional only — uncertainty not quantified |

When `uncertainty_range_pct = None`:
- No confidence band is rendered.
- The trajectory line is rendered with `strokeDasharray="8 3"` (dashed).
- The label "Directional only — uncertainty not quantified" appears in Zone 1A.
- The trajectory remains visible (not hidden) — directional information is preserved.

---

## Control Plane Reserved Zone

> Revised: 2026-06-27 — Course corrected per NM-072: restored to maximalist
> platform target state. Mode 2 read-only specification is confirmed correct target
> architecture (not an M18 scope compromise). Mode 3 shock taxonomy restored to
> all 7 types including GrowthShock. M18 delivery scope constraints removed —
> this document records platform target state only. M18 delivery scope and G4
> implementation scope are in Artifact 5 (#1359) and ADR-019.

A dedicated screen zone is reserved in the primary viewport layout for the control
plane from M9 onward. This zone is reserved before Mode 3 is built — not retrofitted
when Mode 3 arrives (CLAUDE.md Governing Premise 5). The zone is 280px wide
(`gridColumn: 3` in `InstrumentCluster`), rendered at all three supported breakpoints
(1024, 1280, 1440), and never collapsed or hidden in any mode.

---

### Mode 1 (Replay) — Reserved, Empty

The 280px column contains no interactive content in Mode 1. A subdued watermark
label — "Control plane (Mode 3)" — is rendered in the lower-left of the column
using `color: rgba(0,0,0,0.25)`, `fontSize: 11`, `fontFamily: monospace`, no
pointer events. This is the final Mode 1 state; no additional content is specified.

**Testable constraint:** No element inside the control plane zone has `tabIndex`,
`onClick`, `onChange`, or any interactive attribute in Mode 1. The watermark font
size (11px) must not exceed the smallest text in Zone 1 instruments.

---

### Mode 2 (Simulation) — Read-Only Summary + Mode 3 Activation

> **Platform architecture ruling — UX Designer, GD Artifact 5 panel 2026-06-26.**
> Mode 2 column 3 is a read-only scenario summary surface with a single
> mode-transition affordance. This is the correct target architecture for Mode 2,
> not a scope compromise: Mode 2's cognitive task is threshold-safe path
> construction, which requires undistracted trajectory reading. Editable parameters
> in column 3 would undermine that task. No editable configuration surface is
> specified for Mode 2 column 3 at any milestone.

The Mode 2 column carries two elements only: a read-only summary of the loaded
scenario, and a single control to enter Mode 3. No editable fields. No sliders.
No Apply button.

**Component:** `Mode2ColumnSurface` — a separate component from `ControlPlane`.
The two-component architecture is an EL-mandated condition (Decision 1 panel
condition 3): `Mode2ColumnSurface` and `ControlPlane` must not be implemented
as conditional rendering inside a single component. This constraint exists to
enable lazy mounting of `ControlPlane` independently of Mode 2 content (Issue
#1217 render optimization — EX-001 decision 3).

**Visual treatment:** Subdued — the column in Mode 2 should visually signal
"this zone becomes active in Mode 3," not present itself as a live instrument.
Use `color: rgba(0,0,0,0.45)` for summary text labels (slightly lighter than
body text but not as subdued as the Mode 1 watermark). The "Enter Active Control"
button is the single element with full-weight styling.

---

**Element 1 — Active scenario summary (read-only)**

Four lines, plain text, no interaction:

- **Scenario name** — the name of the currently loaded and completed scenario
- **Entity** — ISO 3166-1 alpha-3 code + entity display name
- **Calibration vintage** — the data vintage used (e.g., "2023 WB WDI")
- **Run horizon** — "Steps 1–N (YYYY–YYYY)" using the scenario's `start_year`
  and computed step count

All four fields sourced from `activeScenarioDetail` — no additional fetch
required. If any field is unavailable, render "—" (em dash) for that line.

`data-testid="mode2-scenario-summary"`

---

**Element 2 — "Enter Active Control" affordance**

A single button positioned below the scenario summary.

Button label: **"Enter Active Control"** (not "Enter Mode 3" — EL condition 1).
Rationale: "Mode 3" is an internal label; "Active Control" is the instrument
cluster mode indicator label that Eleni already reads (US-026). Using the same
language removes a translation step.

Button treatment: subdued by default to signal the weight of the action —
`background: #0284c7` (sky-700), `color: #fff`, `opacity: 0.75`. Not disabled,
not grayed out — but visually restrained relative to the full-brightness Mode 3
Apply button.

**Caution text** below the button (12px, `color: rgba(0,0,0,0.45)`):
"Mode 3 branching cannot be undone from this view — return to Mode 2 resets
the active branch."

`data-testid="enter-active-control"`

---

**Testable constraints for Mode 2 column:**
- No `<input>`, `<select>`, or `<textarea>` element within `Mode2ColumnSurface`
- Exactly one button element present (`enter-active-control`)
- All four summary fields present in DOM (may display "—" if data unavailable)
- Column width remains 280px (same as Mode 1 and Mode 3)

---

### Mode 3 (Active Control) — Two-Form Control Plane

The 280px column is populated with two independent forms: the policy instruments form
(blue) and the scenario shocks form (orange). Both form headers must be visible
simultaneously without scroll within the column. Content within each form may scroll
independently if the history list grows.

**Column header:** "ACTIVE CONTROL" — `fontWeight: 700`, `fontSize: 11`,
`letterSpacing: 0.5`, `color: #0284c7` (the primary Mode 3 blue). Positioned at
the top of the column, above both forms.

---

#### Policy Instruments Form (blue visual treatment)

**Form section header:** "POLICY INSTRUMENTS" — `fontWeight: 700`, `fontSize: 10`,
`letterSpacing: 0.5`, `color: #0284c7`. Section has `borderLeft: 3px solid #0284c7`.

**Controls:**

1. **Control input type selector** (dropdown/select)
   - Label: "Input type"
   - Available types: `FiscalMultiplier`, `LegitimacyConstraint`
   - Display names: "Fiscal Multiplier", "Legitimacy Constraint"
   - Selecting a type updates the parameter field(s) shown below
   - `data-testid="policy-input-type-selector"`

2. **Parameter field** (slider, updates based on selected type)
   - FiscalMultiplier: range 0.1–3.0, step 0.05, display `{value.toFixed(2)}×`
   - LegitimacyConstraint: range 0.0–1.0, step 0.05, display `{Math.round(value * 100)}%`
   - `data-testid="policy-param-slider"`

3. **Step selector** (dropdown or number input)
   - Label: "Apply at step"
   - Range: 1 through current max computed step
   - Default: current step
   - Distinct from Mode 2's "branch from step" slider — this selects the step
     at which the policy input takes effect, not the recompute anchor
   - `data-testid="policy-step-selector"`

4. **"Apply policy input" button**
   - Background: `#0284c7`, color: `#fff`
   - Disabled state: `background: #bae6fd` (sky-200), label "Computing…"
   - `data-testid="apply-policy-input"`

5. **Applied inputs history list** (scrollable within policy section)
   - Appears below the Apply button after the first application
   - Each entry: `step N — [InputType]: [value]` — e.g., "Step 1 — Fiscal Multiplier: 0.75×"
   - Max visible without scroll: 2 entries; scrollable after
   - `data-testid="policy-inputs-history"`
   - Empty state: no list element rendered (not an empty list placeholder)

---

#### Scenario Shocks Form (orange visual treatment)

**Form section header:** "SCENARIO SHOCKS" — `fontWeight: 700`, `fontSize: 10`,
`letterSpacing: 0.5`, `color: #ea580c` (the primary Mode 3 orange). Section has
`borderLeft: 3px solid #ea580c`.

**Controls:**

1. **Step selector**
   - Label: "Inject at step"
   - Range: 1 through current max computed step
   - Default: next step after current
   - `data-testid="shock-step-selector"`

2. **Shock type selector** (dropdown/select)
   - Label: "Shock type"
   - `data-testid="shock-type-selector"`
   - Available types (display name — internal enum):

   | Display name | Enum value |
   |---|---|
   | Election / Political Transition | `ElectionShock` |
   | Currency Crisis | `CurrencyAttack` |
   | Creditor Defection | `CreditorDefection` |
   | Geopolitical Shock | `GeopoliticalShock` |
   | Natural Disaster | `NaturalDisaster` |
   | Financial Contagion | `ContagionShock` |
   | GDP / Growth Scenario | `GrowthShock` |

   Seven types — the complete platform shock taxonomy. Parameter schemas for
   each type are specified in ADR-019. Type-specific parameter fields (magnitude,
   duration, distribution parameters) are ADR-019 scope — not specified here.

3. **"Inject scenario shock" button**
   - Background: `#ea580c`, color: `#fff`
   - Disabled state: `background: #fed7aa` (orange-200), label "Computing…"
   - `data-testid="inject-scenario-shock"`

5. **Injected shocks history list** (scrollable within shock section)
   - Each entry: `step N — [ShockType] [magnitude if applicable]` — e.g.,
     "Step 2 — GDP Growth Shock: +8%"
   - Max visible without scroll: 2 entries; scrollable after
   - `data-testid="shock-history"`
   - Empty state: no list element rendered

---

### Simultaneous Visibility Requirement

Both the "POLICY INSTRUMENTS" section header and the "SCENARIO SHOCKS" section
header must be visible simultaneously without scroll within the 280px column. This
is the US-028 acceptance criterion and an epistemic requirement: Eleni must be able
to see at a glance that both action categories are available without scrolling.

**Sizing at 1280×800:** The instrument cluster height at 1280 is constrained by the
chart height (320px) plus header elements. The two form section headers require
approximately 28px each (10px font, padding, border). Both headers are visible
at 56px combined — easily within any realistic column height. The 280px column
width is confirmed sufficient for the two-form layout at all three breakpoints.

**The trajectory view width takes priority.** At 1280×800 the trajectory is 580px.
If future additions to the column require width beyond 280px, the trajectory view
minimum (580px) must not be violated. The 280px + 400px co-primary + 580px
trajectory = 1260px total, within the 1280px minimum viewport width.

---

### CVD (Colour Vision Deficiency) Color Specification

The blue/orange distinction is an epistemic requirement. It must hold for users with
deuteranopia (red-green CVD, the most common form) and protanopia.

| Role | Hex | Name | Use |
|---|---|---|---|
| Policy (blue) | `#0284c7` | Sky-700 | Policy form header, border, Apply button, trajectory inflection markers |
| Shock (orange) | `#ea580c` | Orange-600 | Shock form header, border, Inject button, trajectory shock markers |

These two values are safe under deuteranopia and protanopia simulations: they differ
in hue (blue vs. orange/yellow region) and in luminance (sky-700 is darker than
orange-600 at 100% opacity), providing both hue and luminance discrimination channels.

**MV-001 validation is a hard gate.** Manual CVD validation using a simulation tool
(e.g., Sim Daltonism, Coblis) must be completed and documented before any Mode 3
control plane component ships. The validation must confirm that both section headers
and their respective form elements are distinguishable from each other under
deuteranopia and protanopia simulation at all supported viewports. The MV-001 gate
applies to both trajectory markers and alert panel treatment as well.

**Purple is deprecated for control plane elements.** The current `#8b5cf6` purple
in `ControlPlane.tsx` does not satisfy the blue/orange requirement and must be
replaced in all Mode 3 control plane styling.

---

### Mode 2 → Mode 3 Transition (Column Behavior)

The transition is triggered by the "Enter Active Control" button in `Mode2ColumnSurface`.

When the user clicks "Enter Active Control":

1. The `mode` state transitions to `"MODE_3"`.
2. `Mode2ColumnSurface` unmounts (or hides — two-component architecture per EL
   Decision 1 condition 3 means these are separate mounted components, not a
   conditional render within one component).
3. `ControlPlane` mounts into the column slot — lazy mounting is intentional
   (Issue #1217, EX-001 Decision 3): `ControlPlane` is not in the DOM until
   Mode 3 is entered, avoiding its render cost during Mode 1 and Mode 2.
4. The Mode 3 "ACTIVE CONTROL" header and both forms render.
5. The transition must complete in under 3 seconds (Journey C Step 1 critical
   constraint). No animation is specified — simple mount/unmount.

The trajectory view must not reflow during the transition — the column width
(280px) is identical in both modes and does not change on mount/unmount.

**State preservation:** The scenario's completed trajectory becomes the Mode 3
baseline at the moment Mode 3 is entered. The baseline is locked — no Mode 2
parameter adjustments are possible once Mode 3 is active. (In M18, Mode 2 column
3 has no editable fields; this constraint is architectural rather than enforced
by hiding controls.)

---

### Sizing Constraint (All Modes)

The control plane zone must not reduce the trajectory view below its minimum legible
width at the desktop minimum viewport (1280×800). Rule: trajectory view wins if zone
sizes conflict. The current 280px column leaves 580px for the trajectory view at
1280px viewport — above the minimum legible width. This constraint must be verified
at ADR-019 acceptance if any column width change is proposed.

## M8 Hierarchy Decisions

These decisions are binding for M8 implementation and must not be overridden
by implementation convenience.

| Decision | Ruling | Rationale |
|---|---|---|
| All four radar axes must appear simultaneously | No tabs, no toggles | The four-framework argument collapses if any axis requires interaction to reveal |
| Null axes must be visually distinct from zero-value axes | Distinct treatment (e.g., dashed outline, "—" label) | A zero governance score and a null governance score are categorically different; conflating them is a precision error |
| Policy Maneuver Margin is Zone 1, not a FrameworkPanel row | Dedicated widget, not a table row | It is the primary instrument for Coffin Corner detection — burying it in a panel defeats the purpose |
| Methodology notes are Zone 3 | Collapsed by default, accessible via (i) | Mandatory ADR-005/006 compliance satisfied without competing with threshold alarm detection |
| Indicator display names are human-readable | Display name mapping layer in frontend | Demo and negotiation-room legibility; internal keys are implementation detail |
| Radar chart step transitions are animated | 200–300ms ease-in-out | The deformation across steps is the visual argument; it must be observable, not just the result |
| MDA alert framework source visible in Zone 1 | Shown per alert row without expanding | At M8, ecological and governance alerts fire for the first time; the specialist must know which framework without opening a tab |

---

## M9 Hierarchy Decisions

These decisions supersede or extend M8 decisions where they conflict. EL Decision
numbers refer to decisions recorded on Issue #364.

| Decision | Ruling | Rationale |
|---|---|---|
| Trajectory view is Zone 1, not Zone 2 (EL Decision 2) | Trajectory view in primary viewport; not in drawer or behind tab | The primary cognitive task across all three modes requires multi-framework trajectory comparison as the first read — it cannot be behind a click |
| Radar chart moves from Zone 1 to Zone 2 (EL Decision 2) | Accessible via one scroll or tab; not on initial view | Zone 1 four-framework current position (1D) provides the quick-read; the radar chart provides the spatial depth behind it — it is Zone 2 evidence, not a Zone 1 scan surface |
| EntityDetailDrawer demoted to detail/methodology surface (EL Decision 2) | No primary instrument lives inside the drawer | Primary instruments are in the instrument cluster viewport. The drawer provides indicator detail, cohort breakdowns, and methodology notes — it is the Zone 2/3 expansion surface |
| Entity selector is a persistent header element (EL Decision 2) | Always visible, never inside a drawer or behind navigation | In multi-entity scenarios, the user must be able to switch entity without leaving the primary viewport — a flight simulator cannot require navigating away to switch which aircraft is on instruments |
| COMPARE_VIEW Zone 1 is mode-and-context-conditional (EL Decision 3) | Single-entity Mode 2 → divergence timeline; multi-entity Mode 2 → DeltaChoropleth; Mode 3 → automatic live A/B (no COMPARE_VIEW entered) | The primary comparison question differs: multi-entity asks "where do these entities diverge?"; single-entity asks "at which step does path A cross a threshold B avoids?"; Mode 3 comparison is always temporal, never geographic |
| DeltaChoropleth deprecated for single-entity and Mode 3 (EL Decision 3) | DeltaChoropleth used only in multi-entity Mode 2 | Geographic divergence is not the primary question in single-entity comparison or in Mode 3 active control; using it in these contexts answers the wrong question |
| Control plane zone reserved from M9 onward (Premise 5, PR #390) | Empty reserved zone in Mode 1 and Mode 2; populated in Mode 3 | A zone retrofitted at Mode 3 introduction will be undersized; a zone sized from M9 will accommodate both policy instrument and scenario shock forms simultaneously |
| Mode 3 live A/B is automatic, not invoked (EL Decision 3, Gap 4) | Ghost baseline curves appear at first applied control input; no toggle required | In Mode 3, "baseline vs. active" is always the comparison frame — it is not an optional view; making it user-invoked would require an action at the moment when cognitive load is highest |

---

## What Belongs in Which Document

| Question | Document |
|---|---|
| Who is the user and what are they trying to do? | `north-star.md` |
| What does the user do step by step? | `user-journeys.md` |
| Where does each element appear and at what depth? | This document |
| How is a specific component implemented? | `docs/frontend/` architecture documents |
| What design decision was made and why? | `docs/frontend/design-decisions.md` |

Hierarchy decisions (this document) govern layout and depth. Implementation
decisions (design-decisions.md) govern how the layout is built. When they
conflict, hierarchy governs — the implementation must adapt to the hierarchy,
not the reverse.
