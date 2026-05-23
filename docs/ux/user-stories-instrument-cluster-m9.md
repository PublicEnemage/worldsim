# User Stories — M9 Instrument Cluster

> **Owned by:** Business Product Owner Agent (R), UX Designer Agent (C)
> **Authored:** 2026-05-23 — Issue #441
> **Status:** Awaiting three UX Designer rulings (marked [UX-RULING]) before stories are
> fully testable. All other criteria are final. EL decision on US-GAP-001 resolved:
> M10 gap (Issue #451 filed 2026-05-23).
>
> **Consumers:**
> - **QA Lead** — writes acceptance tests from the Given/When/Then criteria before
>   implementation begins. This is the independent quality gate.
> - **Frontend Architect** — implements to these stories as the user-value specification
>   that governs tradeoff decisions. When an implementation choice conflicts with a story,
>   the story governs — not implementation convenience.
>
> **Source documents read:**
> `docs/ux/personas.md`, `docs/ux/user-journeys.md`, `docs/ux/north-star.md`,
> `docs/ux/information-hierarchy.md`, `docs/frontend/fa-brief-m9-instrument-cluster.md`
>
> **Agents consulted:** UX Designer Agent (three rulings requested), UX Design Thinking Agent
> (gap coverage check)

---

## How to Read These Stories

Each story uses the project standard format:

**As** [named persona] in [mode / entry state],
**I need** [specific observable capability],
**so that** [goal — traced to the north-star cognitive task for the active mode].

Acceptance criteria use Given/When/Then format. Each criterion is independently testable
without requiring interpretation of the story context. Test method is noted per criterion:

- `[Playwright]` — automated E2E assertion
- `[Vitest]` — unit or component test
- `[RTL]` — React Testing Library component test
- `[pytest]` — backend / fixture validation
- `[Manual]` — human verification gate (MV-NNN from FA brief)

**[UX-RULING]** marks criteria with open placeholders awaiting UX Designer confirmation.
These stories are otherwise complete — QA can write all other criteria immediately.

**[EL-DECISION]** marks a gap finding requiring Engineering Lead scope decision before
a story can be written.

All 29 stories are M9 required. None are deferred.

---

## Story Groups

| Group | Instrument / Capability | Stories |
|---|---|---|
| 1 | Zone 1 Completeness — all four instruments without scroll | US-001, US-002 |
| 2 | Trajectory View (1A) — curves, step axis, mode behavior | US-003 – US-012 |
| 3 | MDA Alert Panel (1B) — threshold crossings, severity, attribution | US-013 – US-018 |
| 4 | PMM Widget (1C) — margin, direction, mode-specific label | US-019, US-020 |
| 5 | Four-Framework Current Position (1D) — numeric readout | US-021, US-022 |
| 6 | Atomicity — single render cycle | US-023, US-024 |
| 7 | Persistent Header — entity selector, mode indicator | US-025, US-026 |
| 8 | Control Plane Reserved Zone — empty in Mode 1/2, populated in Mode 3 | US-027, US-028 |
| 9 | Performance — render time on CI throttled profile | US-029 |
| — | Gap finding — Andreas Mode 1 pattern recognition | US-GAP-001 |

---

## Group 1 — Zone 1 Completeness

### US-001 — All four Zone 1 instruments visible at tablet minimum (1024×768)

**As** Eleni Papadimitriou in Mode 2 Preparatory entry state,
**I need** all four Zone 1 instruments (trajectory view, MDA alert panel, PMM widget,
four-framework current position) visible without scrolling at 1024×768,
**so that** I can complete the threshold-safe path construction task — the Mode 2 primary
cognitive task — without navigating away from the primary viewport.

**Acceptance criteria:**
- Given SCENARIO_RUNNING in Mode 2, when rendered at 1024×768, then the trajectory view
  (1A), MDA alert panel (1B), PMM widget (1C), and four-framework current position (1D)
  are all present in the DOM with computed height > 0, without any scroll interaction
  [Playwright — AC-001]
- Given rendered at 1024×768, then trajectory view computed width ≥ 480px [Playwright — AC-003]
- Given rendered at 1024×768, then the right co-primary column is 240px wide; none of 1B,
  1C, 1D overflow their container [Playwright]
- Given rendered at 1024×768, then each of 1B, 1C, 1D has `offsetTop + offsetHeight ≤`
  usable viewport height (~680px) — none are below the fold [Playwright]

**Journey anchor:** Journey A Step 3b; Journey B Step 3
**Cognitive task:** Mode 2: threshold-safe path construction
**M9 gate:** Required

---

### US-002 — All four Zone 1 instruments visible at desktop minimum (1280×800)

**As** Eleni Papadimitriou in Mode 2 Preparatory entry state,
**I need** all four Zone 1 instruments visible without scrolling at 1280×800,
**so that** I can complete the threshold-safe path construction task at the most common
working viewport without navigating away from the primary viewport.

**Acceptance criteria:**
- Given SCENARIO_RUNNING in Mode 2, when rendered at 1280×800, then all four Zone 1
  instruments are present with computed height > 0, without scroll [Playwright — AC-002]
- Given rendered at 1280×800, then trajectory view computed width ≥ 580px [Playwright — AC-004]
- Given rendered at 1280×800, then trajectory view computed height ≥ 300px [Playwright — AC-005]
- Given rendered at 1280×800, then control plane zone computed width = 280px [Playwright — AC-014]

**Journey anchor:** Journey A Step 3b
**Cognitive task:** Mode 2: threshold-safe path construction
**M9 gate:** Required

---

## Group 2 — Trajectory View (1A)

### US-003 — Four framework curves on a shared step axis

**As** Eleni Papadimitriou in Mode 2 Preparatory entry state,
**I need** the trajectory view to show four composite score curves (financial, human
development, ecological, governance) simultaneously on a single shared step axis,
**so that** I can identify at a glance which framework is deteriorating, at which step, and
whether it is approaching an MDA floor — without switching tabs or toggling frameworks.

**Acceptance criteria:**
- Given a scenario with all four frameworks computed, when the trajectory view renders, then
  four distinct `<Line>` components are present in the SVG, one per framework, all sharing
  the same x-axis domain [Playwright — assert four curve elements present simultaneously]
- Given the trajectory view renders at any supported viewport, then all four curves are
  visible without a tab action or framework toggle [Playwright — assert no click required
  before all four curves are visible]
- Given a scenario advanced to step N, then all four curves share the same x-domain (steps
  1 through N); no curve uses a different x-axis range [Vitest — unit test shared axis]

**Journey anchor:** Journey A Step 3b
**Cognitive task:** Mode 2: threshold-safe path construction
**M9 gate:** Required

---

### US-004 — MDA floor lines overlaid as threshold reference

**As** Lucas Ferreira in Mode 2 Preparatory entry state,
**I need** the MDA floor for each framework rendered as a horizontal dashed threshold line
overlaid on the trajectory view,
**so that** I can see at a glance how close any composite score is to its Minimum Descent
Altitude without opening a separate panel or inspecting numerical values.

**Acceptance criteria:**
- Given a scenario where MDA floors are defined for at least one framework, when the trajectory
  view renders, then a horizontal dashed `<ReferenceLine>` element is present at the floor
  y-value for each framework that has a defined floor [Vitest — assert ReferenceLine present
  at floor y-value per framework]
- Given a composite score curve that crosses the MDA floor between step N and step N+1, then
  the floor line is positioned at the floor y-value and the curve visibly crosses it in that
  interval [Playwright — screenshot assertion: curve element crosses ReferenceLine element]

**Journey anchor:** Journey A Step 3b; Journey A Step 4
**Cognitive task:** Mode 2: threshold-safe path construction
**M9 gate:** Required

---

### US-005 — Mode 1 step axis: three-line annotation for historical orientation

**As** Aicha Mbaye in Mode 1 SCENARIO_PRELOADED (demonstrative entry state),
**I need** each SIGNIFICANT step on the trajectory view step axis to show three lines —
step index, calendar date, and event label — without any interaction,
**so that** I can orient within 20 seconds which historical events correspond to which
trajectory inflections, without an economist interpreting the quantitative values for me.

**Acceptance criteria:**
- Given a Mode 1 scenario fixture where at least one step has `step_significance = "SIGNIFICANT"`,
  when the trajectory view renders, then for each SIGNIFICANT step the tick contains exactly
  three text nodes: step index, `effective_from` formatted as a human-readable date, and
  `step_event_label` text — in that order top to bottom [Playwright — AC-011; assert three
  text nodes per SIGNIFICANT tick]
- Given a SIGNIFICANT step's `step_event_label`, then it is ≤ 8 words AND ≤ 32 characters;
  the fixture schema validation rejects violations before they reach the UI [pytest — AC-012;
  runs on every PR as a CI gate]
- Given a Mode 1 step that is not SIGNIFICANT, then its tick contains exactly two text nodes
  (step index and date) — no event label row [Playwright — assert two text nodes on
  non-SIGNIFICANT ticks]
- Given the three-line tick renders at 1024×768 viewport with 480px trajectory view width
  on a six-step Greece fixture, then no tick label truncates mid-word [Playwright — AC-011
  extension; screenshot assertion — FA-C5 resolution]

**Journey anchor:** Journey D Step 1
**Cognitive task:** Mode 1: trajectory reconstruction AND historical pattern recognition
**M9 gate:** Required

---

### US-006 — Mode 2 step axis: projected calendar dates

**As** Eleni Papadimitriou in Mode 2 Preparatory entry state,
**I need** the trajectory view step axis to show the projected calendar date for each step,
**so that** I can translate step indices ("step 3 crosses the floor") into programme-year
language ("year 2 of the programme") that I can use in briefings and when citing findings
under Troika scrutiny.

**Acceptance criteria:**
- Given a Mode 2 scenario, when the trajectory view renders, then each step tick label
  contains a projected calendar date alongside the step index [Playwright — assert date
  text node present per tick in Mode 2]
- Given a Mode 2 scenario, then step tick labels do not contain event label text — event
  labels are Mode 1 only [Playwright — assert exactly two text nodes per tick in Mode 2]

**Journey anchor:** Journey A Step 3b
**Cognitive task:** Mode 2: threshold-safe path construction
**M9 gate:** Required

---

### US-007 — Mode 3: baseline ghost curves appear automatically on first control input

**As** Eleni Papadimitriou in Mode 3 Active Control (Journey C Step 2),
**I need** the baseline trajectory curves to appear automatically as ghost lines (50% opacity,
1px stroke) when I apply my first control input — without any toggle or additional interaction,
**so that** I can see immediately how the proposed term diverges from my prepared baseline at
the exact moment I need that comparison, without taking any action that delays the negotiation.

**Acceptance criteria:**
- Given Mode 3 is active and no control input has been applied, when the trajectory view
  renders, then no ghost curve elements are present — only the four active trajectory curves
  [Vitest — assert no baseline curve elements before first control input is applied]
- Given the first control input is applied and computation completes, then four baseline ghost
  `<Line>` components (50% opacity, 1px stroke) are automatically rendered alongside the four
  active `<Line>` components (100% opacity, 2px stroke) — total: eight Line components in the
  ComposedChart [Playwright — AC-009 partial; assert eight Line components after first input]
- Given ghost curves are rendered, then the baseline `<Line>` components have `opacity={0.5}`
  and `strokeWidth={1}`; active `<Line>` components have `opacity={1}` and `strokeWidth={2}`
  [Vitest — assert style props]
- Given all eight `<Line>` components are rendered, then every one has `connectNulls={false}`
  [Vitest — AC-015 extension to Mode 3 ghost curves]

**Journey anchor:** Journey C Step 2; Journey B Step 5
**Cognitive task:** Mode 3: real-time steering within human cost constraints
**M9 gate:** Required

---

### US-008 — Mode 3: divergence fill marks where paths separate

**As** Eleni Papadimitriou in Mode 3 Active Control (Journey C Step 2),
**I need** a divergence fill region to appear automatically between the baseline and active
curves where they separate by more than a threshold delta,
**so that** I can see at a glance which steps are affected by the proposed modification
without visually comparing two overlaid curves — in a negotiation room there is no time for
that comparison.

**Acceptance criteria:**
- Given Mode 3 with baseline and active trajectories where |active − baseline| > 0.01 at
  step N, when the trajectory view renders, then a filled `<Area>` region is present between
  the two curves at step N [Vitest — AC-010 inverse; assert Area present when delta > 0.01]
- Given trajectories where |active − baseline| ≤ 0.01 at every step, then no `<Area>` fill
  is rendered [Vitest — AC-010; assert no Area element when delta ≤ 0.01 at all steps]
- Given a divergence fill renders, then it uses 5–10% opacity [Vitest — assert fill-opacity
  style prop is in range [0.05, 0.10]]

**Journey anchor:** Journey C Step 2
**Cognitive task:** Mode 3: real-time steering within human cost constraints
**M9 gate:** Required

---

### US-009 — Mode 3: policy and shock markers visually distinct

**As** Eleni Papadimitriou in Mode 3 Active Control (Journey C Step 4),
**I need** policy input markers (blue) and scenario shock markers (orange vertical lines
across all curves) to be visually distinct from each other and from the trajectory curves,
**so that** I can immediately identify whether a trajectory inflection was caused by my policy
input or by an exogenous shock — this distinction is what I cite when the Troika disputes
the cause of a threshold crossing.

**Acceptance criteria:**
- Given a control input applied at step N, when the trajectory view renders, then a blue
  marker element is present at the step N x-position on the shared axis [Playwright — assert
  blue-treated marker element at step N]
- Given a scenario shock injected at step M, then an orange vertical line spans the full
  chart height at step M [Playwright — assert orange full-height vertical element at step M]
- Given both a policy input at step N and a shock at step M (N ≠ M), then the blue and
  orange markers are visually distinguishable by color treatment; CVD validation (MV-001)
  must be completed before this story ships [Manual — MV-001]

**Journey anchor:** Journey C Step 4
**Cognitive task:** Mode 3: real-time steering within human cost constraints
**M9 gate:** Required

---

### US-010 — Null composite score renders as curve gap, not zero

**As** Lucas Ferreira in Mode 2 Preparatory entry state,
**I need** a null composite score at any step to render as a visible gap in the corresponding
trajectory curve,
**so that** I cannot misread a data-absent step as a zero-value outcome and build a
negotiating argument on a false reading — a Tier 5 governance null is not a zero governance
score and must not look like one.

**Acceptance criteria:**
- Given a scenario fixture where the governance composite score is `null` at step 3, when the
  trajectory view renders, then no data-point element is rendered on the governance curve at
  step 3; the curve has a visible gap [Vitest — AC-015; assert no rendered element at null
  step position; all four `<Line>` components have `connectNulls={false}`]
- Given a curve gap at step 3 due to a null value, then the governance curve renders as two
  distinct segments (steps 1–2 and steps 4–N) with no interpolation through the null step
  [Vitest — assert two distinct curve segments; no connected path through step 3]

**Journey anchor:** Journey A Step 3b
**Cognitive task:** Mode 2: threshold-safe path construction
**M9 gate:** Required

---

### US-011 — Step transitions animated 200–300ms ease-in-out

**As** Aicha Mbaye in Mode 1 SCENARIO_PRELOADED (demonstrative entry state),
**I need** the trajectory view curves to animate smoothly when the scenario advances from
one step to the next,
**so that** I can observe the deformation of the four-framework shape across historical steps —
the change itself is the visual argument; if I only see the result, I lose the narrative.

**Acceptance criteria:**
- Given the scenario advances from step N to step N+1, then the ComposedChart applies a
  CSS transition of 200–300ms ease-in-out to the curve update [Playwright — assert
  transition-duration CSS property on chart element is in range [200ms, 300ms]]
- Given `prefers-reduced-motion: reduce` is set, then the step transition animation is
  suppressed — no transition-duration applied [Playwright — emulate prefers-reduced-motion;
  assert transition-duration is 0ms or unset]

**Journey anchor:** Journey D Step 1
**Cognitive task:** Mode 1: trajectory reconstruction
**M9 gate:** Required

---

### US-012 — Tier 4/5 curves show exploratory confidence badge

**As** Lucas Ferreira in Mode 2 Preparatory entry state,
**I need** trajectory curves with Tier 4 or Tier 5 composite confidence to display an "(exp)"
label adjacent to their most recent data point in the chart body,
**so that** I can see at a glance that a framework curve carries exploratory confidence before
I decide whether to cite it in a staff report — a Tier 5 breach requires an epistemic caveat
that Tier 1 does not.

**Acceptance criteria:**
- Given a scenario where the governance framework has Tier 4 or Tier 5 composite confidence,
  when the trajectory view renders, then a `<text>` element containing "(exp)" is present in
  the SVG, adjacent to the rightmost data point on the governance curve [Playwright — AC-013]
- Given a framework with Tier 1, 2, or 3 confidence, then no "(exp)" label is rendered on
  that curve [Playwright — assert absence of "(exp)" text adjacent to Tier 1–3 curves]

**Journey anchor:** Journey A Step 5
**Cognitive task:** Mode 2: threshold-safe path construction
**M9 gate:** Required

---

## Group 3 — MDA Alert Panel (1B)

### US-013 — Top 1–3 alerts visible without scrolling

**As** Eleni Papadimitriou in Mode 2 Preparatory entry state (Journey A Step 4),
**I need** the top 1–3 MDA alerts visible without scrolling at all supported viewports,
**so that** I can determine within 5 seconds whether any threshold has been crossed at the
current step — this is the pass/fail scan that determines whether I have an argument.

**Acceptance criteria:**
- Given a scenario with ≥ 3 alerts of mixed severity, when rendered at 1024×768, then the
  top 3 alerts (ordered by severity: TERMINAL > CRITICAL > WARNING) each have
  `offsetTop + offsetHeight ≤` usable viewport height (~680px) — no scroll required to
  see the third alert [Playwright]
- Given rendered at 1024×768 with 240px right column, then each alert row renders in compact
  three-line format: Line 1 (severity pill + severity abbreviation ["WARN"/"CRIT"/"TERM"] +
  framework abbreviation ["FIN"/"HDI"/"ECO"/"GOV"]), Line 2 (indicator display name ≤ 22
  characters with ellipsis if truncated), Line 3 ("Step N • [cohort ≤ 10 characters]")
  [Playwright — assert three line elements per alert row at 1024×768]
- Given rendered at 1280×800 with 400px right column, then each alert row renders in
  full-density format with all four fields untruncated on separate lines [Playwright —
  assert untruncated text at 1280×800]

**Journey anchor:** Journey A Step 4; Journey B Step 3
**Cognitive task:** Mode 2: threshold-safe path construction; Mode 3: real-time steering
**M9 gate:** Required

---

### US-014 — Severity ordering: TERMINAL before CRITICAL before WARNING

**As** Eleni Papadimitriou in Mode 2 Reactive entry state,
**I need** alerts ordered by severity (TERMINAL first, CRITICAL second, WARNING third)
regardless of the order they fired or the framework they belong to,
**so that** I see the most critical finding first in the 5-second scan — never scroll past
a WARNING to find the CRITICAL that constitutes my argument.

**Acceptance criteria:**
- Given a scenario with alerts of mixed severity across frameworks, when the alert panel
  renders, then TERMINAL-severity alerts appear before CRITICAL, and CRITICAL before
  WARNING, in DOM order top to bottom [Vitest — unit test sort function; assert sort
  order of alert objects before render]
- Given two alerts of the same severity level, then within the severity group, alerts are
  ordered by step_index ascending (earlier step first) [Vitest — unit test secondary
  sort by step_index]

**Journey anchor:** Journey A Step 4; Journey B Step 3
**Cognitive task:** Mode 2: threshold-safe path construction
**M9 gate:** Required

---

### US-015 — Framework source visible per alert without expanding

**As** Eleni Papadimitriou in Mode 2 Preparatory entry state,
**I need** the framework source (FIN / HDI / ECO / GOV) visible in each alert row without
opening a framework tab or expanding the row,
**so that** I know immediately which analytical dimension produced the alert and whether it
falls in a domain where I have confidence strong enough to cite.

**Acceptance criteria:**
- Given an alert from the human_development framework, when the panel renders at 1024×768,
  then the alert row compact Line 1 contains the text "HDI" [Playwright — assert "HDI" in
  Line 1 of a human_development alert at 1024×768]
- Given an alert from the ecological framework at 1024×768, then Line 1 contains "ECO"
  [Playwright]
- Given any alert at 1280×800, then the framework source is visible in the full-density row
  without any expand or tab action [Playwright — assert framework source text visible without
  click at 1280×800]

**Journey anchor:** Journey A Step 4
**Cognitive task:** Mode 2: threshold-safe path construction
**M9 gate:** Required

---

### US-016 — Mode 1 alert language is declarative historical fact

**As** Andreas Stefanidis in Mode 1 Retrospective entry state,
**I need** MDA alert text to use declarative historical tense,
**so that** I can read the alerts as evidence about what actually happened — not as warnings
about something I need to prevent — and translate findings directly into political narrative
without an economist re-interpreting them for me.

**Acceptance criteria:**
- Given a Mode 1 scenario where an indicator crossed its floor at step 3, when the alert
  panel renders, then the alert row text uses the Mode 1 historical tense pattern
  [Playwright — assert [UX-RULING-1: exact observable string for Mode 1 alert tense]]
- Given a Mode 1 alert row, then the text does not contain advisory-language strings
  [Playwright — assert absence of [UX-RULING-1: advisory language strings to exclude
  from Mode 1 alert text]]
- Given Mode 2, then alert text uses the Mode 2 projected-warning pattern [Playwright —
  assert [UX-RULING-1: Mode 2 observable string]]
- Given Mode 3, then alert text uses the Mode 3 live-update pattern [Playwright —
  assert [UX-RULING-1: Mode 3 observable string]]

**Journey anchor:** Journey D Step 2
**Cognitive task:** Mode 1: historical pattern recognition
**M9 gate:** Required
**[UX-RULING-1]:** Exact observable alert text strings per mode required from UX Designer
before QA can write these assertions. See §Open Rulings.

---

### US-017 — Mode 3 causal attribution: which input caused which crossing

**As** Eleni Papadimitriou in Mode 3 Active Control (Journey C Step 3),
**I need** each MDA alert row to show "Caused by: [description]" when the crossing was
produced by a specific control input,
**so that** I can cite verbatim in the negotiation which specific proposed term caused which
threshold crossing — this attribution is the negotiating instrument, not context.

**Acceptance criteria:**
- Given Mode 3 and a control input applied at step 1 caused an alert at step 2, when the
  alert panel renders, then the alert row contains text beginning with "Caused by:" followed
  by a description of the control input [Playwright — assert "Caused by:" substring present
  in Mode 3 alert row]
- Given a shock injected at step 2 is the sole cause of an alert, then the attribution reads
  "Caused by: [shock type]" [Playwright — assert shock type description in attribution]
- Given multiple inputs contributed to an alert, then the attribution reads "Caused by:
  Multiple inputs (see trajectory view)" [Playwright — assert exact string "Multiple inputs"
  when multi-cause alert]
- Given Mode 1 or Mode 2, then no "Caused by:" text is present in any alert row [Playwright —
  assert "Caused by:" string absent outside Mode 3]

**Journey anchor:** Journey C Step 3
**Cognitive task:** Mode 3: real-time steering within human cost constraints
**M9 gate:** Required

---

### US-018 — Mode 3 alert panel updates in real time after control input

**As** Eleni Papadimitriou in Mode 3 Active Control,
**I need** the MDA alert panel to update within 10 seconds of applying a control input,
**so that** I can see the alert consequence of the proposed term while the negotiation
is still in progress — not after the discussion has moved on.

**Acceptance criteria:**
- Given Mode 3, when a control input is applied and computation completes, then the alert
  panel DOM reflects the new alert state within 10 seconds of the user clicking "Apply
  policy input" [Playwright — measure elapsed time from button click to alert panel DOM
  update; assert ≤ 10 seconds]
- Given computation is in progress (`computation_state = "computing"`), then the alert
  panel shows a loading indicator rather than stale data from the prior step [Playwright —
  assert loading state element renders during computing state]

**Journey anchor:** Journey C Step 2; Journey B Step 5
**Cognitive task:** Mode 3: real-time steering within human cost constraints
**M9 gate:** Required

---

## Group 4 — PMM Widget (1C)

### US-019 — PMM visible without scroll; value, direction, and mode-specific label

**As** Aicha Mbaye in Mode 1 SCENARIO_PRELOADED (demonstrative entry state, Journey D Step 3),
**I need** the PMM widget to be visible without scroll and show a numeric value, a direction
indicator showing whether margin is growing or shrinking, and the mode-specific label,
**so that** the driver can orient me in one sentence without requiring prior WorldSim
knowledge or any interaction on my part.

**Acceptance criteria:**
- Given Mode 1, when the instrument cluster renders, then the PMM widget is present with
  `offsetTop + offsetHeight ≤` usable viewport height (no scroll required), shows a numeric
  value, a direction indicator element (arrow or equivalent trend symbol), and the exact
  label text "Policy Maneuver Margin — historical" [Playwright — assert PMM visible without
  scroll; assert exact label text match]
- Given Mode 2, then the PMM label reads exactly "Policy Maneuver Margin — projected"
  [Playwright — assert Mode 2 label]
- Given Mode 3, then the PMM label reads exactly "Policy Maneuver Margin — current"
  [Playwright — assert Mode 3 label]
- Given Mode 3 and a control input has been applied and computed, then the direction
  indicator element updates to reflect the new margin direction [Playwright — assert
  direction indicator element state changes after control input computation completes]
- Given the PMM widget renders in any mode, then the label does not contain the string
  "coffin_corner_index" or any other raw database field name [Playwright — assert raw
  field name strings absent from PMM label]

**Journey anchor:** Journey D Step 3
**Cognitive task:** Mode 1: trajectory reconstruction AND historical pattern recognition
**M9 gate:** Required

---

### US-020 — PMM has dedicated visual identity, not a FrameworkPanel row

**As** any user in any mode,
**I need** the PMM widget to be a distinct component separate from the FrameworkPanel rows,
**so that** the Policy Maneuver Margin is immediately identifiable as a primary instrument —
not a secondary indicator buried in a panel — which is the precondition for Aicha orienting
in one sentence.

**Acceptance criteria:**
- Given the instrument cluster renders, then the PMM widget element is not a descendant of
  any FrameworkPanel component in the DOM tree [Vitest — assert PMM not rendered inside
  FrameworkPanel DOM subtree]
- Given the instrument cluster renders at 1024×768, then the PMM widget occupies the
  middle vertical slot of the right column (between 1B bottom edge and 1D top edge), with
  computed height ≈ 25% of right column height (~160px at 1024×768) [Playwright — assert
  PMM offsetTop > 1B bottom and PMM bottom < 1D top]

**Journey anchor:** Journey D Step 3
**Cognitive task:** All modes — prerequisite for PMM legibility
**M9 gate:** Required

---

## Group 5 — Four-Framework Current Position (1D)

### US-021 — All four framework scores visible simultaneously without tabs

**As** Eleni Papadimitriou in any mode, SCENARIO_RUNNING state,
**I need** all four composite score values (financial, human development, ecological,
governance) visible simultaneously as numbers with human-readable labels, without tabs,
toggles, or navigation,
**so that** I can scan the current step's full framework picture in a single glance — a
multi-framework argument collapses if any axis requires interaction to reveal.

**Acceptance criteria:**
- Given SCENARIO_RUNNING at any step in any mode, when the 1D panel renders, then exactly
  four framework value elements are present in the DOM simultaneously, each labeled with
  "Financial", "Human Development", "Ecological", "Governance" [Playwright — assert four
  labeled value elements present without any tab or toggle interaction]
- Given the four framework labels render, then none use raw database field names
  ("financial", "human_development", "ecological", "governance" as display labels are not
  acceptable) [Playwright — assert human-readable label strings present]

**Journey anchor:** Journey A Step 3b; Journey B Step 3
**Cognitive task:** Mode 2: threshold-safe path construction
**M9 gate:** Required

---

### US-022 — Null score visually distinct from zero score

**As** Lucas Ferreira in Mode 2 Preparatory entry state,
**I need** a null governance composite score to be visually distinct from a zero-value score
in the four-framework current position panel,
**so that** I cannot build a negotiating argument based on a false reading that mistakes
"data absent" for "governance at zero" — these are categorically different states and a
Tier 5 null is not evidence of zero governance health.

**Acceptance criteria:**
- Given the governance composite score is `null` at the current step, when the 1D panel
  renders, then the governance value element displays "—" (em dash) — not "0", not "0.00",
  not blank [Playwright — assert text content of governance value element equals "—" when
  score is null]
- Given the governance composite score is exactly `0.00` at the current step, then the
  governance value element displays a numeric value (e.g., "0.00") — not "—" [Playwright —
  assert numeric text present when score is 0; assert "—" absent]
- Given a null score, then the governance value element carries a visually distinct CSS
  treatment distinguishing it from numeric values in peripheral vision [Playwright —
  assert [UX-RULING-2: exact CSS class or DOM attribute for null vs. zero distinction]]

**Journey anchor:** Journey A Step 3b
**Cognitive task:** Mode 2: threshold-safe path construction
**M9 gate:** Required
**[UX-RULING-2]:** Exact CSS treatment (class name, attribute, or property) for null vs.
zero distinction required from UX Designer before QA can write the third criterion.
See §Open Rulings.

---

## Group 6 — Atomicity

### US-023 — All Zone 1 instruments update in one render cycle on step advance

**As** Eleni Papadimitriou in Mode 2 Preparatory entry state (Journey A Step 3a),
**I need** all four Zone 1 instruments to update atomically when a step advances — in a
single React render cycle — not one at a time with separate loading states per instrument,
**so that** I never see a partially-updated instrument cluster that could cause me to draw
a false conclusion mid-scan at the step that matters most.

**Acceptance criteria:**
- Given SCENARIO_RUNNING, when the step-advance action is wrapped in a React Testing Library
  `act()` call, then before `act()` resolves, all four Zone 1 instrument DOM nodes reflect
  the new `current_step` value — no additional `act()` call is required [RTL — AC-006]
- Given the step advance action fires, then the Zustand store is updated via a single
  `set()` call carrying `current_step`, `trajectory`, and updated state — never via multiple
  `set()` calls in sequence [Vitest — unit test Zustand update pattern; assert exactly one
  `set()` call executes on step advance]

**Journey anchor:** Journey A Step 3a
**Cognitive task:** Mode 2: threshold-safe path construction
**M9 gate:** Required

---

### US-024 — Mode 3 computation completes atomically with trajectory data

**As** Eleni Papadimitriou in Mode 3 Active Control,
**I need** the `complete` computation state and the new trajectory data to arrive in the
instruments simultaneously — never a flash where `computation_state` reads "complete" but
trajectory data is still stale,
**so that** I read the consequence of the proposed term once, correctly — a stale read
followed by an update would cause me to cite the wrong finding at the wrong moment.

**Acceptance criteria:**
- Given Mode 3, when a control input computation completes, then the Zustand `set()` call
  transitions `computation_state` to `"complete"` and delivers the new `trajectory` in the
  same `set()` call — `complete` is never set without accompanying trajectory data [Vitest —
  assert `computation_state: "complete"` and `trajectory: newData` are always set together;
  assert no intermediate state where `complete` is set and `trajectory` is stale]
- Given the `complete` state is set, then all four Zone 1 instruments render with the new
  trajectory data in the same React render cycle [RTL — assert no stale-data render
  between `computing` and `complete` states]

**Journey anchor:** Journey C Step 2
**Cognitive task:** Mode 3: real-time steering within human cost constraints
**M9 gate:** Required

---

## Group 7 — Persistent Header

### US-025 — Entity selector always visible without scroll or navigation

**As** a finance ministry specialist in any mode with a multi-entity scenario,
**I need** the entity selector to be visible and functional in the persistent header at all
times — no scroll, no navigation action, no drawer interaction required,
**so that** I can switch which entity is on instruments without leaving the primary viewport —
a flight simulator cannot require navigating away to switch which aircraft is on instruments.

**Acceptance criteria:**
- Given a multi-entity scenario in any mode, when the instrument cluster renders, then the
  entity selector element has computed `offsetTop < 80px` — it is in the persistent header
  above all zone content [Playwright — assert entity selector offsetTop]
- Given the entity selector is visible, then it lists all entities in the scenario and shows
  each entity's current-step composite score per entity [Playwright — assert entity count in
  selector matches scenario entity count; assert composite score text per entity entry]
- Given the user selects a different entity, then all four Zone 1 instruments update atomically
  to reflect the newly selected entity [RTL — wrap entity select in `act()`; assert all four
  Zone 1 instruments reflect new entity within the same `act()` resolution]
- Given any mode or any drawer state, then the entity selector has computed height > 0 and
  is not `display: none` [Playwright — assert entity selector visible regardless of mode
  and drawer state]

**Journey anchor:** Journey A Step 1; Journey B Step 1
**Cognitive task:** All modes
**M9 gate:** Required

---

### US-026 — Mode indicator always visible in persistent header

**As** Aicha Mbaye in Mode 1 SCENARIO_PRELOADED (demonstrative entry state, Journey D Step 1),
**I need** the mode indicator to be visible in the persistent header without any interaction,
**so that** within 20 seconds I can confirm I am watching a historical replay — not a
prediction — and contextualize everything else I read in the instrument cluster accordingly.

**Acceptance criteria:**
- Given Mode 1, when the instrument cluster renders, then the persistent header contains
  the mode indicator with exact text [UX-RULING-3: Mode 1 label string] [Playwright —
  assert mode indicator text exact match]
- Given Mode 2, then the mode indicator shows [UX-RULING-3: Mode 2 label string]
  [Playwright]
- Given Mode 3, then the mode indicator shows [UX-RULING-3: Mode 3 label string]
  [Playwright]
- Given a mode change, then the mode indicator text updates within the same render cycle as
  the mode state change [RTL — assert indicator text within `act()` on mode change]

**Journey anchor:** Journey D Step 1
**Cognitive task:** Mode 1: trajectory reconstruction AND historical pattern recognition
**M9 gate:** Required
**[UX-RULING-3]:** Exact mode indicator label strings for all three modes required from
UX Designer before QA can write these assertions. See §Open Rulings.

---

## Group 8 — Control Plane Reserved Zone

### US-027 — Control plane zone reserved and empty in Mode 1 and Mode 2

**As** Eleni Papadimitriou in Mode 1 or Mode 2,
**I need** the 280px control plane zone to be present in the layout as reserved space —
not collapsed, not hidden, not filled with other content,
**so that** when Mode 3 arrives, the layout is already sized correctly and my instrument
cluster is not re-reflowed at the worst possible moment (active negotiation).

**Acceptance criteria:**
- Given Mode 1 or Mode 2, when the instrument cluster renders, then a DOM element
  representing the control plane zone has computed width = 280px and is present in the
  layout — not `display: none`, not collapsed to 0px [Playwright — AC-014 Mode 1/2
  variant; assert control plane element width = 280px in both modes]
- Given Mode 1 or Mode 2, then the control plane zone contains no interactive elements
  (no form fields, no buttons, no clickable controls) [Playwright — assert no interactive
  child elements within control plane zone in Mode 1/2]
- Given the control plane zone renders in Mode 1/2, then any placeholder label has
  subdued styling that does not compete with Zone 1 instruments — font rendering must
  not be more visually prominent than the smallest text in Zone 1 [Playwright — assert
  any text in control plane zone in Mode 1/2 uses subdued color; no font-size exceeding
  Zone 1 minimum label size]

**Journey anchor:** CLAUDE.md §Governing Premise 5; information-hierarchy.md
§Control Plane Reserved Zone
**Cognitive task:** Future Mode 3 prerequisite — protects all three mode cognitive tasks
**M9 gate:** Required

---

### US-028 — Mode 3 control plane: both form headers visible without scroll

**As** Eleni Papadimitriou in Mode 3 Active Control (Journey C Steps 2 and 4),
**I need** both the policy instruments form and the scenario shocks form to be visible
simultaneously in the control plane zone — both form headers visible without scroll —
**so that** I can apply a control input and inject a shock in the same session step without
scrolling within the control plane, which would take my eyes off the trajectory view at the
moment I need it most.

**Acceptance criteria:**
- Given Mode 3 is active, when the control plane zone renders, then both form headers —
  one for policy instruments (blue visual treatment) and one for scenario shocks (orange
  visual treatment) — are visible without scroll within the 280px zone [Playwright —
  assert both form header elements have `offsetTop + offsetHeight ≤` control plane
  zone height without scroll interaction]
- Given the policy instruments form header uses blue treatment and the scenario shocks
  form header uses orange treatment, then the two form headers are visually distinguishable
  by color; CVD validation (MV-001) must be completed before this story ships [Manual —
  MV-001]
- Given Mode 3 with ≥ 1 applied control input, then an applied inputs history list element
  is present within the policy instruments form area [Playwright — assert history list
  element present in policy form section]
- Given Mode 3 with ≥ 1 injected shock, then an injected shocks history list element is
  present within the scenario shocks form area [Playwright — assert history list element
  present in shock form section]

**Journey anchor:** Journey C Steps 2 and 4
**Cognitive task:** Mode 3: real-time steering within human cost constraints
**M9 gate:** Required

---

## Group 9 — Performance

### US-029 — Trajectory view renders within 100ms on CI throttled profile

**As** a finance ministry analyst using WorldSim on a four-core laptop,
**I need** the trajectory view to render and respond within 100ms on a CI 4× throttled
profile,
**so that** the instrument cluster is responsive at the hardware accessible to resource-
constrained ministries — this tool must work on the hardware they actually have, not only
on well-resourced institutional machines.

**Acceptance criteria:**
- Given a 4× CPU throttle (`page.emulate({cpuThrottling: 4})`), when the trajectory view
  renders initially, then `performance.measure` records ≤ 100ms [Playwright — AC-007]
- Given the same throttle, when the user navigates to the next step, then the step
  navigation transition completes in ≤ 100ms [Playwright — AC-008]
- Given Mode 3 with full component set (8 `<Line>` components + 4 `<Area>` components +
  3 shock-event `<ReferenceLine>` components; MDA floor lines excluded from M9), then the
  full Mode 3 ComposedChart renders within 100ms on the same throttle [Playwright — AC-009]
- Given the CI throttle gate passes, then hardware validation on an actual 8GB/4-core
  laptop must be completed and documented before M9 closes [Manual — MV-002]

**Journey anchor:** CLAUDE.md §Equitable Build Process; ADR-010 Decision 9
**Cognitive task:** All modes — prerequisite for all other stories
**M9 gate:** Required

---

## Gap Finding — US-GAP-001

### Andreas's Mode 1 Historical Pattern Recognition — Comparative Surface Deferred to M10

**EL decision recorded: M10 gap (2026-05-23). Issue #451 filed.**

Pre-EL consultation panel: UX Design Thinking Agent, Business Product Owner Agent, Architect
Agent — three-agent unanimous verdict M10. The gap is narrower than originally stated: the
trajectory view rendering layer is already Mode 1 comparison-ready (ADR-010 Decision 11;
FA brief §UD-R2 tick format). The missing piece is the UX entry point for selecting a second
historical fixture — a Zone 2 / COMPARE_VIEW architecture question, not a Zone 1 instrument
cluster question.

**Persona:** Andreas Stefanidis (Persona 3 — Political Advisor)
**Mode:** Mode 1 Retrospective / Reactive
**Primary task from personas.md:** Translate quantitative threshold crossings into political
narrative; identify whether the trajectory follows a recognizable pre-collapse pattern from
historical precedent.
**Failure mode:** "Historical precedent pattern is absent — without Mode 1 replay of
comparable cases, he cannot build the political argument."

**What the M9 instrument cluster provides for Andreas:**

US-005 (step axis annotations) enables Andreas to read event labels on SIGNIFICANT steps.
US-003 (four curves) shows the trajectory shape he is trying to pattern-match against. US-016
(Mode 1 declarative alert language) gives him findings in political narrative form.

**What M9 does not provide — and why M10 is the correct home:**

Pattern recognition requires mapping the current trajectory against a reference — "does this
look like Cyprus 2013, or Portugal 2011?" The M9 instrument cluster renders one trajectory
correctly. It has no UX surface for selecting a second reference trajectory.

The rendering layer is not the gap: ADR-010 Decision 11 specifies alignment of two historical
entities by programme step; FA brief §UD-R2 specifies the stacked entity date tick format.
The `TrajectoryView` component will render multi-case Mode 1 correctly once given two data
sets. The missing piece is the Zone 2 entry point for selecting the second fixture — a
COMPARE_VIEW architecture question addressed in `information-hierarchy.md §COMPARE_VIEW
Mode 1` (placeholder added 2026-05-23).

**M9 service level for Persona 3:** Partially served. Orientation (step axis annotations,
declarative alert language) is sufficient for M9. Comparable-case comparison — the full
pattern recognition task — is M10 scope.

**M10 deliverables:** See Issue #451 — entry point UX spec, backend endpoint extension,
`comparison_trajectory` prop on `TrajectoryView`, and one user story with QA acceptance
tests written before implementation begins.

---

## Open Rulings

Three acceptance criteria contain placeholders awaiting UX Designer confirmation.
Stories are otherwise final and QA can begin writing all other criteria immediately.

| Ruling | Story | Question |
|---|---|---|
| [UX-RULING-1] | US-016 | Exact observable alert text strings per mode (Mode 1 historical, Mode 2 projected, Mode 3 live); exact advisory language strings to assert absent from Mode 1 rows |
| [UX-RULING-2] | US-022 | Exact CSS class or DOM attribute distinguishing null composite score from zero-value score in the 1D panel |
| [UX-RULING-3] | US-026 | Canonical mode indicator label strings for all three modes |

---

## Story Coverage Matrix

| Instrument | Mode 1 | Mode 2 | Mode 3 | Primary personas served |
|---|---|---|---|---|
| Zone 1 completeness | US-001, US-002 | US-001, US-002 | US-001, US-002 | 2 |
| Trajectory view (1A) | US-005, US-011 | US-003, US-004, US-006, US-010, US-012 | US-007, US-008, US-009 | 1, 2, 3, 4, 5 |
| MDA alert panel (1B) | US-016 | US-013, US-014, US-015 | US-017, US-018 | 1, 2, 3 |
| PMM widget (1C) | US-019, US-020 | US-019, US-020 | US-019, US-020 | 2, 5 |
| Four-framework position (1D) | US-021, US-022 | US-021, US-022 | US-021, US-022 | 1, 2 |
| Atomicity | — | US-023 | US-024 | 2 |
| Persistent header | US-025, US-026 | US-025, US-026 | US-025, US-026 | 2, 5 |
| Control plane zone | US-027 | US-027 | US-028 | 2 |
| Performance | US-029 | US-029 | US-029 | All |

**Total stories: 29 (US-001 through US-029)**
**M9 Required: 29**
**Open UX Designer rulings: 3** (US-016, US-022, US-026 — QA can write all other criteria)
**EL decision resolved: 1** (US-GAP-001 — M10 gap; Issue #451 filed 2026-05-23)
