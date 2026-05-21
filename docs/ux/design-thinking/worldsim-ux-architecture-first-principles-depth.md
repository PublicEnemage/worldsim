# WorldSim UX Architecture — First Principles Depth

> Author: UX Design Thinking Agent (activations: UX Design Thinking Agent,
>         Development Economist, Political Economist — inline below)
> Date: 2026-05-21
> Scope: Closes Issue #363. Depth specification for six gaps in the
>        first-principles review. This document extends
>        docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md
>        — it does not replace it. Read the first-principles review and the
>        persona-grounded review before reading this.
>
> Input documents (read before writing):
>   docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md
>   docs/ux/design-thinking/persona-grounded-ux-review.md
>   docs/ux/personas.md
>   docs/architecture/simulation-framework.md
>   CLAUDE.md

---

## Orientation

The first-principles review produced five governing premises and a Case B verdict.
The persona-grounded review (PR #388) validated the verdict against all five
personas and identified four specification extensions the first-principles document
did not address because it derived the instrument cluster from Mode 3 alone.

This document closes six gaps. The gaps are not architectural failures — the
first-principles review is correct at the premise level. The gaps are specification
absences: places where the premises have been stated but the behavioral requirements
that make them real have not been written down with enough precision for a Frontend
Architect to act.

The governing test throughout: *Is this specific enough that a Frontend Architect
building the component would know exactly what to implement?*

---

## Gap 1A — Mode 3 Walkthrough: Eleni Papadimitriou, February 2012

> Development Economist agent activated for this section.

**What this gap is:** The first-principles document defined Mode 3 requirements
abstractly (R1–R4). The persona-grounded review confirmed that Case B serves Eleni.
Neither document produced a walkthrough concrete enough for component requirements.
This gap closes that.

**Persona context:** Eleni Papadimitriou. Deputy Director, Hellenic Ministry of Finance.
February 2012. The Troika has circulated the second memorandum conditionality package
overnight. She has until 9am to identify the specific terms she can challenge and
build the counter-proposal. At 9am she enters the negotiation session.

This walkthrough covers both the 3-hour Preparatory session the night before and
the Mode 3 active interaction during the negotiation session itself, because Mode 3's
instrument requirements must be traceable to the preparation that made Mode 3 possible.

---

### T=0:00 — Opening the Tool (Preparatory Entry State)

**What Eleni sees:** The landing screen opens with the instrument cluster visible.
Her most recently accessed scenario is pre-loaded — "Greece_Feb2012_Baseline" —
showing the instrument cluster at its last saved step (step 1, January 2012).

The instrument cluster at T=0:00 shows:

- **Trajectory view:** four composite score curves on a shared step axis (6 steps
  = 6 months of the memorandum programme). Step 1 values are current; steps 2–6
  show the projected baseline trajectory.
- **MDA alert panel:** current alerts at step 1. Two WARNING alerts visible.
  No CRITICAL alerts at step 1.
- **PMM widget:** value = 0.67, trend arrow ↓ (declining).
- **Four-framework current position:** Financial 0.58, Human Development 0.71,
  Governance 0.54, Ecological 0.82.

**What she does first:** She does not read any of these values. She opens the
scenario configuration panel. She duplicates "Greece_Feb2012_Baseline" and names
the copy "Counter_Feb2012_ModA."

**Time requirements:**
- Landing state must load in under 3 seconds with the most recent scenario
  pre-loaded
- Scenario duplication must be completable in under 30 seconds (name entry + confirm)

**Component requirements from T=0:00:**

| Requirement | Implementation note |
|---|---|
| Landing screen shows instrument cluster, not a config screen | Pre-load last scenario at session start |
| Scenario duplication in ≤ 2 interactions | Scenario selector → duplicate button |
| Duplication creates exact parameter copy | Not a blank scenario |

---

### T=0:03 — Modifying the Counter-Proposal (Preparatory)

**What she does:** In "Counter_Feb2012_ModA," she modifies three conditionality
terms from the full Troika package:

1. Minimum wage cut: postponed from step 1 to step 2 (12-month delay)
2. Basic pension floor: protected at current level through step 3
3. Privatization timeline: unchanged (accepting as non-negotiable at this meeting)

She enters each modification as a ControlInput:

- `MinimumWagePolicyInput`: delay by 1 step (plain-language: "Delay this policy by
  12 months")
- `SocialTransferInput`: pension floor protection = true, protected through step 3

**Time requirements:** All three modifications completable in under 5 minutes from
a practitioner who knows the conditionality terms but is not a simulation expert.

**Component requirements from T=0:03:**

| Requirement | Implementation note |
|---|---|
| ControlInput fields labeled in plain language | "Delay this policy by [X] months" not "step_offset" |
| Policy input taxonomy visible before entry | Labels grouped: "fiscal adjustment," "social protection," "structural reform" |
| Each ControlInput shows a one-line effect description | Which indicator it primarily affects; visible before entry |

---

### T=0:08 — Running the Counter-Proposal to Step 6

**What she sees during execution:** The trajectory view shows a "computing" state
on the affected curves — the Human Development and Financial curves show a subtle
pulse animation indicating updating. The MDA alert panel shows an "updating alerts"
state. The PMM widget is greyed out during computation.

**What she sees after execution completes:** The counter-proposal scenario
"Counter_Feb2012_ModA" is complete at step 6. All instruments update simultaneously.

**Time requirement:** Execution to step 6 must complete in under 60 seconds.
The "computing" state must be visually explicit — she must know the system is working.

---

### T=0:09 — Entering the Comparison View (Preparatory)

**What triggers it:** Completing the second scenario automatically prompts:
"Both scenarios are complete. View comparison?" with a single-action confirmation.
She confirms. The comparison view opens.

**What she sees in the comparison view:**

*Zone 1A — Delta Alert Panel (primary surface of the comparison view):*

```
COMPARISON: Greece_Feb2012_Baseline vs. Counter_Feb2012_ModA

PRIMARY ONLY:
  CRITICAL — poverty_headcount — bottom_quintile — step 2
             → Delayed to step 4 in counter-proposal
  WARNING  — health_system_capacity — all_cohorts — step 3
             → Absent in counter-proposal

BOTH SCENARIOS:
  WARNING  — unemployment_rate — working_age — step 1

COUNTER-PROPOSAL ONLY:
  (none)
```

The delta panel does not show binary fire/no-fire. It shows:
- The severity in the primary scenario
- Whether the crossing fires in the counter-proposal and at what step if delayed
- The step-level delta: "CRITICAL at step 2 → delayed to step 4 in counter"

This is the negotiating surface. Eleni reads this in 30 seconds and knows:
postponing the minimum wage cut delays the poverty crossing by 2 steps and
eliminates the health system alert entirely.

*Zone 1B — Trajectory Divergence View:*

Two trajectory curves on the same step axis. Primary scenario: darker line. Counter-
proposal: lighter line. Human Development composite score is the primary curve
showing the most dramatic divergence. The MDA floor is overlaid as a horizontal
threshold line. Where the primary crosses below the floor (step 2): red dot marker.
The counter-proposal curve descends toward but does not cross the floor.

*Zone 1C — Fiscal Equivalence Header:*

```
Fiscal equivalence: Counter-proposal achieves 99.3% of 5-year primary surplus target.
Primary surplus target met 1 quarter later under counter-proposal.
```

This is a single-line calculation visible without navigation. It is the financial
credibility claim that makes the human cost argument defensible under Troika scrutiny.

**Component requirements from T=0:09:**

| Requirement | Implementation note |
|---|---|
| Comparison view prompts automatically when second scenario completes | One-action confirmation |
| Delta alert panel is Zone 1A in comparison view | Topmost, always visible |
| Delta shows step-level delta (not binary fire/no-fire) | "Delayed to step N in counter" |
| Fiscal equivalence header in comparison view | Not Zone 3 — must be visible without navigation |
| Trajectory divergence view shows dual curves, shared step axis, MDA floor overlay | MDA floor as horizontal threshold line |

---

### T=0:20 — What Eleni Carries to the 9am Session

From the 20-minute preparatory session, Eleni carries:

1. Delta alert panel: CRITICAL poverty crossing delayed 2 steps
2. Trajectory divergence view: MDA floor crossing avoided
3. Fiscal equivalence figure: 99.3%
4. Cohort identification: bottom quintile, working-age
5. The specific modification: minimum wage postponed 12 months

At 9am, the tablet opens with the comparison view pre-loaded. She reaches the delta
alert panel in under 10 seconds. She does not navigate.

---

### T=9:00 — Active Negotiation (Reactive Entry State)

**What she needs in the negotiation room:** Not Mode 3 steering. Not a scenario
builder. She is not applying new policy inputs in real time — the Troika is
presenting; she is recalling and retrieving.

The correct affordance for Eleni in the negotiation room is instant recall of the
relevant alert without navigation. Specifically:

- MDA alert panel visible on the opening screen without any navigation
- The specific alert she rehearsed (CRITICAL — poverty_headcount — step 2)
  findable in under 90 seconds from cold start
- Tapping any alert in the panel must immediately show the trajectory view for
  that indicator — not open the entity drawer

**Time requirements (Reactive entry state, in-room):**

| Action | Required time |
|---|---|
| Alert panel visible from cold start | 0 navigation — must appear on landing screen |
| Navigate from landing to specific alert detail | ≤ 90 seconds total |
| Navigate from alert detail to indicator trajectory view | ≤ 2 interactions |

**Component requirements from T=9:00:**

| Requirement | Implementation note |
|---|---|
| Alert panel is Zone 1 on the landing screen | Not behind a drawer or a tab |
| Alert entries are interactive | Tapping an alert expands to show trajectory view for that indicator at that step |
| No navigation between instrument cluster surfaces for 90-second retrieval task | All required surfaces accessible via tap within the instrument cluster |

---

### Mode 3 Component Requirement Summary

For a Frontend Architect, the full component requirement set from this walkthrough:

| Component | Must exist | Zone | Modes |
|---|---|---|---|
| Scenario duplication action | Yes | Scenario selector (outside instrument cluster) | 1, 2, 3 |
| ControlInput form with plain-language labels and taxonomy | Yes | Mode 2/3 configuration surface | 2, 3 |
| Comparison view auto-prompt on second scenario completion | Yes | Primary viewport transition | 2, 3 |
| Delta alert panel with step-level severity delta | Yes | Zone 1A (comparison view) | 2, 3 |
| Fiscal equivalence header | Yes | Comparison view header | 2 |
| Trajectory divergence view (dual curves, shared axis, MDA floor overlay) | Yes | Zone 1B (comparison view) | 2, 3 |
| Alert panel interactive (tap → indicator trajectory) | Yes | Zone 1 (single-scenario view) | 1, 2, 3 |
| Landing screen: instrument cluster pre-loaded (last scenario) | Yes | Primary viewport | 1, 2, 3 |
| Execution state: "computing" visual treatment on affected curves | Yes | Trajectory view during computation | 2, 3 |
| Confidence tier → negotiation-defensibility label in alert panel | Yes | MDA alert panel | 2, 3 |

---

## Gap 1B — Mode 1 Annotation Specification for Persona 3 (Andreas Stefanidis)

> Political Economist agent activated for this section.

**What this gap is:** The persona-grounded review found that Premise 3 (step axis
as shared frame) is opaque to Andreas without calendar date and event label
annotation. This gap specifies exactly what must appear on every step marker for
Mode 1 to be legible to a non-analyst user.

**Why this is mandatory, not optional:** Andreas cannot navigate from "Step 1" to
"December 2001 — corralito announced." Aicha cannot follow a 5-minute demonstration
where the x-axis shows "Step 1 / 6" without context. The step annotation is the
bridge between the simulation's coordinate system (steps) and the users' coordinate
system (calendar dates, political events). Without it, Premise 3 serves Personas 1
and 2 only.

---

### Three Mandatory Fields on Every Mode 1 Step Marker

Every step marker on the shared step axis in Mode 1 must display three fields. These
are mandatory — not optional, not behind a settings toggle.

**Field 1 — Step index:** The step number (e.g., "Step 1"). Required for internal
reference and for technical users who navigate by step index (Lucas, Eleni).

**Field 2 — Calendar date:** The calendar date corresponding to the step.
Format: `MMM YYYY` (e.g., "Dec 2001", "Feb 2012"). For daily-resolution scenarios
(adaptive temporal resolution during crisis events), format extends to `DD MMM YYYY`.

The calendar date is sourced from the scenario fixture's `effective_from` field for
the step's initial event — not derived from the step index.

**Field 3 — Event label (for significant steps):** A one-line plain-language label
for steps where a significant historical event occurred or where an MDA alert fires.
Not required for every step — required for every SIGNIFICANT step.

Format constraint: ≤ 8 words, plain language, no economic jargon, no indicator names.

Examples from existing fixtures:
- "Deposit freeze announced" (Argentina, Dec 2001, Step 1)
- "Second memorandum signed" (Greece, Feb 2012, Step 2)
- "Capital controls imposed" (Cyprus, March 2013, Step 1)
- "Currency floated" (Egypt, Nov 2016, Step 1)

---

### Rendering Requirements

**Default rendering at standard viewport (≥ 1024px):**

```
Step 1          Step 2               Step 3
Dec 2001        Jan 2002             Mar 2002
Deposit         Five presidents      Default declared
freeze          period
announced
```

All three fields visible on every step marker. Event label omitted for ROUTINE steps.

**At narrow viewport (< 768px):** Step index and calendar date visible.
Event label truncates to a tooltip accessible via tap/hover.

**Step marker click behavior:** Clicking any step marker navigates all instruments
in the cluster to that step simultaneously — not sequentially. This is the shared
step axis invariant from Premise 3. Every instrument updates in a single render cycle.

**Event label length constraint:** ≤ 8 words. Enforced at fixture creation time
via schema validation, not at render time. A fixture that fails this constraint
must not pass CI.

---

### Fixture Metadata Schema Requirements

Every Mode 1 scenario fixture must include, per step:

| Field | Type | Required | Notes |
|---|---|---|---|
| `effective_from` | ISO 8601 date | Always mandatory | Source for calendar date display |
| `step_event_label` | string, ≤ 8 words | Mandatory for SIGNIFICANT steps; null permitted for ROUTINE | Cannot be absent for any SIGNIFICANT step |
| `step_significance` | enum: `SIGNIFICANT` \| `ROUTINE` | Always mandatory | SIGNIFICANT = full three-field display; ROUTINE = step index + date only |

A Mode 1 fixture with any SIGNIFICANT step missing `step_event_label` is incomplete
and must not be shipped. This is a fixture completeness gate, not a display suggestion.

---

### What This Annotation Enables for Andreas

With full step annotation, the Argentina 2001 Mode 1 replay is legible to Andreas
without explanation:

- "Step 1 / Dec 2001 / Deposit freeze announced" — he immediately knows what event
  this step represents. The governance composite score drop at Step 1 is now connected
  to the corralito.
- "Step 2 / Jan 2002 / Five presidents period" — the governance trajectory becomes
  a political story, not a composite score.
- "Step 3 / Mar 2002 / Default declared" — the TERMINAL alert at Step 3 is now
  legible as the moment Argentina's governance collapse became irreversible.

Compared to Iceland 2008:
- "Step 1 / Oct 2008 / Government takes over banks" — the governance trajectory
  starts to diverge from Argentina at Step 1.
- "Step 3 / Dec 2008 / Emergency laws passed" — governance declines but stabilizes.
- Without annotation, these are two composite score curves. With annotation, they
  are two political stories with a visible fork at the deposit guarantee decision point.

The step annotation is the component that converts Mode 1 from a tool for Lucas
and Eleni into a tool for Andreas and Aicha as well.

---

## Gap 2 — Where the Flight Simulator Analogy Breaks

The flight simulator analogy is architectural. Three places where it breaks
structurally, and what each break means for the five governing premises.

---

### Break 2A — Step-Based vs. Continuous Feedback

**The break:** A real flight simulator produces subsecond continuous feedback —
yoke input → attitude indicator response in the same render cycle. WorldSim
produces step-resolved feedback: a control input triggers a propagation computation
across the step graph. The trajectory view updates when computation completes.
Feedback is not continuous; it is step-resolved with computation latency of seconds
to minutes depending on scenario complexity.

**What "immediate feedback" means in a step-resolution system:**

Immediate feedback in WorldSim has three components — not one:

1. *Input registration is immediate:* within one render cycle, the control input
   appears in the control plane's "applied inputs" list with its step index. The user
   knows the input was received before computation begins.

2. *Computation is visually acknowledged:* affected trajectory curves show a
   "computing" state (e.g., a subtle pulse animation on the curves that will be
   affected). PMM widget and four-framework current position show a "pending update"
   state. The user knows the system is working and which instruments are updating.

3. *Trajectory update is atomic:* when computation completes, all affected instruments
   update simultaneously in a single render cycle — not sequentially, not rolling.
   A partial update where some instruments show new state while others show old
   state is a violation of the shared step axis invariant.

**Premise qualification:** Premise 3 (step axis as shared frame) must make the
atomicity requirement explicit: *"All instruments that display the step axis update
simultaneously when a step is advanced or a computation completes."*

**Frontend Architect requirement:** The trajectory view, MDA alert panel, PMM widget,
and four-framework current position must subscribe to the same state update signal.
A single computation-complete event triggers all four instrument updates in one
render cycle — not four sequential update events.

---

### Break 2B — Multi-Entity vs. Single Aircraft

**The break:** A flight simulator instrument cluster is for one aircraft. Multi-entity
scenarios — two countries linked by a trade relationship (TC-1), regional contagion
(Case C), bilateral conflict (Case D) — do not map cleanly to a single-aircraft
instrument cluster. Which entity's PMM is displayed? Whose trajectory is the primary?

**How the instrument cluster works in multi-entity scenarios:**

The instrument cluster always shows one *primary entity* at a time. In a multi-entity
scenario, the user selects the primary entity — the entity they are analyzing or
steering. The instrument cluster shows that entity's instruments in the primary viewport.

Secondary entities are accessible via:
- The geographic context view (choropleth), always navigable per Premise 1
- The multi-entity comparison surface, Zone 2 — accessible with one interaction

**Multi-entity specific requirements:**

*Entity selector:* A persistent element in the primary viewport header (not in the
entity drawer) that shows the current primary entity and allows switching. In a
2-entity scenario: a toggle. In a 3+ entity scenario: a dropdown. The entity
selector is always visible — it is not buried.

*Contagion signals on primary entity instruments:* When a secondary entity crosses
a threshold that affects the primary entity (e.g., creditor country banking stress
cascades to programme country financing costs), the primary entity's trajectory view
shows an exogenous event annotation at the step where the contagion arrives —
distinct from a shock the user injected (see Gap 3). The user knows the trajectory
change was caused by an external entity, not by their own policy inputs.

*Mode 1 multi-case comparison alignment:* When Andreas compares Argentina 2001 and
Iceland 2008, both are treated as primary entities for the comparison. The trajectory
view shows two sets of curves on the same step axis. The step axis alignment is by
**programme step**, not by calendar date — "Step 1" for Argentina = "the deposit
guarantee decision step" and "Step 1" for Iceland = "the deposit guarantee decision
step." The alignment anchor is the fixture's `step_significance = SIGNIFICANT`
key event, not the calendar date. This is Mode 1-specific alignment logic.

**Premise qualification:** Premise 1 (primary viewport is the instrument cluster)
survives with one explicit qualification for multi-entity scenarios: *"The instrument
cluster always shows one primary entity. Geographic context shows all entities.
Secondary entity instruments are accessible via one interaction."*

---

### Break 2C — Epistemic Qualification vs. Authoritative Instruments

**The break:** A flight simulator's altimeter reads altitude — no confidence tier,
no uncertainty band, no synthetic estimate badge. WorldSim's instruments carry
uncertainty. A Tier 4 (SYNTHETIC_MODEL) governance composite score has fundamentally
different epistemic standing from a Tier 1 (MEASURED_OFFICIAL) GDP estimate.
An instrument that looks identical regardless of its epistemic tier is not honest
about what it knows.

**How confidence tier affects instrument cluster display:**

The instrument cluster does not suppress Tier 4 instruments. Suppression would
violate the human cost ledger principle — the governance signal, even as an
exploratory estimate, is never a footnote. Instead, confidence tier modifies:

*1. Visual weight on trajectory view curves:*

| Tier | Curve treatment |
|---|---|
| Tier 1-2 (MEASURED or REPORTED) | Solid curve, full opacity, no uncertainty band |
| Tier 3 (SYNTHETIC_COMPARABLE) | Solid curve, 75% opacity, narrow uncertainty band visible |
| Tier 4-5 (SYNTHETIC_MODEL / STRUCTURAL_ABSENCE) | Dashed curve, 60% opacity, wide uncertainty band, confidence badge adjacent to curve label |

*2. MDA alert behavior:*

| Tier | Alert behavior |
|---|---|
| Tier 1-2 | Full severity fires (WARNING / CRITICAL / TERMINAL) |
| Tier 3 | Full severity fires, plus "(moderate confidence)" qualifier on alert text |
| Tier 4-5 | WARNING-only regardless of computed severity, plus "(exploratory — do not cite)" badge. No CRITICAL or TERMINAL alerts from Tier 4-5 data. |

*3. Negotiation-defensibility translation in the MDA alert panel (for Eleni):*

Raw tier numbers are not displayed in the alert panel. Instead, a three-level
defensibility label replaces the tier number:

| Tiers | Displayed label |
|---|---|
| 1-2 | "High confidence — cite directly" |
| 3 | "Moderate confidence — cite with caveat" |
| 4-5 | "Exploratory — do not cite" |

Eleni reads this in the negotiation room and immediately knows which alerts
she can cite under Troika scrutiny and which she cannot.

**What must not happen:** A Tier 4 instrument that looks visually identical to
a Tier 1 instrument. The epistemic qualification must be visible on the instrument
face — not only in Zone 3 methodology documentation.

**Premise qualification:** Premise 2 (instruments always visible without navigation)
requires an explicit extension: *"All primary instruments are always visible.
Their confidence tier is visually present on the instrument face. A Tier 4
instrument does not look like a Tier 1 instrument."*

---

## Gap 3 — Exogenous Shock UX Requirements

**What this gap is:** The first-principles document named R4 (pilot input and
exogenous shock must be visually distinguishable) as an inviolable Mode 3 requirement
and sketched the distinction at three layers. This gap specifies exactly how each
layer implements the distinction.

---

### Three Layers of Distinction

**Layer 1 — Control Plane (injection surface)**

Policy inputs appear under **"Policy instruments"** in the control plane.
They represent deliberate decisions the user made. Visual treatment:

- Blue icon (consistent color across all three layers)
- Form with: step selector, parameter fields, "Apply policy input" confirm button
- When applied: appears in "Applied inputs" history list with step index and parameter values

Exogenous shocks appear under **"Scenario shocks"** in the control plane.
They represent external events the user is testing against. Visual treatment:

- Orange icon (consistent color across all three layers)
- Form with: step selector, shock type selector from taxonomy, "Inject scenario shock"
  confirm button
- Shock type taxonomy: `ElectionShock`, `CurrencyAttack`, `CreditorDefection`,
  `GeopoliticalShock`, `NaturalDisaster`, `ContagionShock`
- When injected: appears in "Injected shocks" history list with step index and shock type

The blue/orange visual distinction and the physical separation into two lists are
both required. They are not cosmetic — they reflect the epistemic distinction between
what the pilot controls and what the environment does to the pilot.

---

**Layer 2 — Trajectory View (on the shared step axis)**

Applied policy inputs appear as **policy inflection markers**:

- A small filled circle at the step where the input was applied
- On the specific curve(s) the input affects (not all curves)
- Blue to match the control plane treatment
- Short inline label: e.g., "−2% spending cut"
- Clicking the marker: shows ControlInput parameters in a tooltip

Injected exogenous shocks appear as **shock event markers**:

- A vertical line at the step where the shock was injected
- Extending across **all four framework curves** (because a shock can affect
  multiple frameworks simultaneously)
- Orange to match the control plane treatment
- Orange label at the top of the line: e.g., "SHOCK: Snap election, step 3"
- Clicking the line: shows shock type and parameters in a tooltip

**When both a policy input and a shock occur at the same step:** Both markers
appear. The blue dot on the affected curve(s) and the orange vertical line across
all curves are visually distinct even when co-located. They must not merge.

---

**Layer 3 — MDA Alert Panel (when thresholds are crossed)**

When an MDA threshold crossing results from a policy input:
```
CRITICAL — poverty_headcount — bottom_quintile — step 3
Caused by: −2% spending cut applied at step 3
```

When an MDA threshold crossing results from an exogenous shock:
```
WARNING — social_cohesion — all_cohorts — step 3
Caused by: Scenario shock — snap election, step 3
```

When a threshold crossing cannot be attributed to a single cause:
```
WARNING — social_cohesion — all_cohorts — step 3
Caused by: Multiple inputs (see trajectory view)
```

The causal attribution is the negotiating instrument. "This path crosses the threshold
because of the consolidation trajectory" is a different negotiating claim from
"this path crosses the threshold because an exogenous shock overwhelmed the
policy framework."

---

### Scan Legibility Requirement

In Mode 3, the user must distinguish policy input effects from exogenous shock effects
by visual scan alone — without reading alert text.

The blue/orange system must be consistent across all three layers: control plane,
trajectory view, MDA alert panel. A user who has learned the distinction at the
control plane can scan the trajectory view and alert panel and immediately identify
which trajectory deviations are caused by their own inputs and which are caused by
injected shocks.

**Color consistency is a cross-layer contract, not a per-layer choice.** Blue = policy
input at the control plane, on the trajectory marker, and in the alert causal
attribution. Orange = exogenous shock at the control plane, on the trajectory line,
and in the alert causal attribution. There is no place in the UI where these colors
are used for a different purpose.

---

## Gap 4 — Mode 3 Live A/B Comparison

**What this gap is:** The user applies a control input and wants to see the trajectory
with and without it simultaneously. What does this look like in the instrument cluster?
How does the user invoke it? What is the minimum instrument state required?

The first-principles document established that Mode 3 comparison is always temporal —
two trajectory curves on the same instrument display (baseline vs. active). This gap
specifies the interaction model.

---

### Invocation Model

**The live A/B comparison is automatic — not invoked.**

Before any control input is applied: trajectory view shows a single set of curves —
the baseline trajectory. No comparison state. No ghost curves. The instrument cluster
is in observation mode.

After the user applies the first control input: the baseline trajectory is preserved
as ghost curves. The active trajectory updates to reflect the control input. The user
now sees two sets of curves simultaneously — without any additional action. No
"enable comparison" button. No "show baseline" toggle. The comparison is always on
from the moment of the first applied control input.

This design reflects the Mode 3 cognitive task: the user is steering, and the
comparison between "where I am going" and "where I was going before my input"
is always the primary frame. It is not an optional view; it is the view.

---

### Visual Design of the Live A/B Comparison

**Baseline curves (ghost):**
- Same color as the active curve for each framework
- Lighter weight: thinner stroke (1px vs. 2px), 50% opacity
- Fully interactive: hovering or tapping shows the baseline value at that step

**Active curves:**
- Full weight: normal stroke (2px), 100% opacity
- These are the "current trajectory" — the trajectory as modified by all applied
  control inputs and injected shocks

**Divergence region fill:**
- Where active and baseline curves separate, the area between them is filled with
  a light semi-transparent shading in the active curve's framework color (5-10% opacity)
- The filled region makes the divergence visible at a glance — its visual area
  is proportional to the magnitude of the effect
- The fill appears immediately when any divergence exists; it disappears if the
  active trajectory re-converges with the baseline

**MDA floor lines:**
- Overlaid on both the baseline and active curves as horizontal dashed threshold lines
- The floor line is the reference that makes the crossing visible: if the baseline
  crosses below the MDA floor but the active trajectory does not (because the control
  input prevented the crossing), the floor line is the visual statement of what the
  control input achieved

---

### Minimum Instrument State Required

The live A/B comparison requires exactly three preconditions:

**Precondition 1 — A completed baseline scenario:** The scenario must have been run
to at least one step before the first control input is applied. The baseline requires
at least one step of computed trajectory for the ghost curves to have reference data.

**Precondition 2 — At least one applied control input:** The active trajectory
diverges from the baseline only when a control input has been applied. A session
with no applied control inputs shows only the baseline (observation mode — single
trajectory set, no ghost curves).

**Precondition 3 — Shared step axis between baseline and active:** Both trajectory
sets reference the same step axis. They are not two separate scenario runs; they are
two states of the same scenario's trajectory (pre-input and post-input). The baseline
is frozen when the first control input is applied. The active trajectory updates from
that frozen baseline state, not from the prior active state.

**When multiple control inputs are applied:** The active trajectory accumulates all
control inputs. The baseline does not change — it is always "the trajectory before
any control inputs." The comparison always answers: "What is the total effect of all
my control inputs?" not "What is the effect of my most recent control input?"

To isolate the effect of a single control input, the user examines the trajectory
view at the step where that input was applied (the policy inflection marker location).
A "view single input effect" affordance is not required in M9 scope — the inflection
marker tooltip showing the parameter values is sufficient.

---

## Gap 5 — Mode Transition Design

**What this gap is:** Which instruments persist across all three modes unchanged?
Which are mode-specific? What is the governing principle? How does the UI signal
mode transitions?

---

### Governing Principle: Cognitive Task Continuity

An instrument persists across modes if it serves the cognitive task of every mode.
An instrument is mode-specific if it serves only one mode's cognitive task and would
be misleading or irrelevant in another.

This principle derives from Premise 4: instruments must serve the cognitive task of
the active mode. An instrument designed for Mode 3 active control that is displayed
in Mode 1 without modification may be technically present but cognitively misleading.

---

### Instruments That Persist Unchanged Across All Three Modes

**Trajectory view:** Persists in all three modes. The step axis and four framework
curves are invariant. What changes:
- Mode 1: historical trajectory, event annotation layer active
- Mode 2: projected trajectory, scenario label on curves
- Mode 3: baseline ghost curves + active curves simultaneously

**MDA alert panel:** Persists in all three modes. Severity system (WARNING / CRITICAL
/ TERMINAL) is invariant. What changes:
- Mode 1: alert tense is "historical" — alerts are facts about what happened
- Mode 2: alert tense is "projected" — alerts are warnings about what will happen
  if the scenario continues
- Mode 3: alert tense is "live" — alerts fire when a trajectory update crosses a floor

**Four-framework current position:** Persists in all three modes. The four-number
readout is invariant. What changes: the "current step" the numbers represent
(historical step in Mode 1, constructed step in Mode 2, live step in Mode 3).

**Step axis (as shared coordinate system):** Persists in all three modes. What changes:
the annotation layer (event labels in Mode 1, none in Mode 2/3).

---

### Instruments That Are Mode-Specific

**PMM widget:** Present in all three modes, but with a mode-specific header label
that changes the epistemic framing:

| Mode | PMM widget header label |
|---|---|
| Mode 1 | "Policy Maneuver Margin — historical" |
| Mode 2 | "Policy Maneuver Margin — projected" |
| Mode 3 | "Policy Maneuver Margin — current" |

In Mode 3, the PMM trend arrow (↑ / ↓) updates after each control input computation.
In Mode 1, the trend arrow reflects the historical trajectory — it does not change
in response to user action.

**Control plane:** Mode 3 only. Not present in Mode 1 or Mode 2. In Mode 1, the
control plane zone is empty (reserved but not populated — Premise 5). In Mode 2,
the scenario configuration surface occupies that zone. In Mode 3, the control plane
(Policy instruments + Scenario shocks forms) occupies that zone.

**Event annotation layer on step axis:** Mode 1 only. In Mode 1, the step axis
displays calendar dates and event labels (Gap 1B requirements). In Mode 2 and Mode 3,
the step axis displays step indices and projected calendar dates. Event labels are
not displayed in Mode 2 or Mode 3 because Mode 2/3 are forward scenarios — no
historical events exist to annotate.

**Delta alert panel (comparison surface structure):** Mode 2 comparison and Mode 3
live A/B comparison have the same Zone 1A position but different structures:
- Mode 2: "primary scenario vs. counter-proposal" delta (two named scenarios)
- Mode 3: "baseline vs. active trajectory" delta (no named scenarios — always the
  same implicit comparison)
These are structurally different — Mode 3 does not have named scenarios to compare;
Mode 2 does.

**Mode 1 multi-case comparison surface:** Mode 1 only. Two historical entities on
the same step axis with programme-step alignment (not calendar alignment). This is
a distinct analytical structure from the Mode 2 delta panel or the Mode 3 live A/B.

---

### How the UI Signals Mode Transitions

**Mode indicator:** A persistent label in the primary viewport header reads the
current mode:
```
MODE 1 — REPLAY    |    MODE 2 — SIMULATION    |    MODE 3 — ACTIVE CONTROL
```
The mode indicator is always visible. It is not in a settings panel, not in a
context menu. The three labels function as a mode selector — tapping a label
switches to that mode.

**Mode transitions are explicit user actions, not side effects.** The user cannot
accidentally transition to a different mode by clicking an instrument. Instrument
interactions (tapping an alert, navigating a step) do not cause mode transitions.

**Transition states (what changes and what is preserved):**

*Mode 1 → Mode 2:*
- Historical fixture is replaced by the scenario configuration surface in the
  control plane zone
- Event annotation layer on step axis deactivates
- PMM header label changes to "projected"
- Instrument cluster shows Mode 2 default state (projected curves, no ghost curves)
- Historical session state is preserved in session history

*Mode 2 → Mode 3:*
- Control plane zone activates — the reserved empty zone populates with the
  policy input and scenario shock forms
- PMM header label changes to "current"
- Live A/B comparison state initializes (single trajectory set — observation mode —
  until first control input is applied)
- Any unsaved Mode 2 scenario parameters are preserved

*Mode 3 → Mode 1:*
- Control plane zone clears — returns to empty reserved state
- Event annotation layer activates on step axis
- PMM header label changes to "historical"
- All applied control inputs from the Mode 3 session are preserved in a session
  history log (not lost silently)

**Transition confirmation (when session state would be discarded):** If a mode
transition would discard unsaved work, a single-sentence confirmation is required:
"Your Mode 3 session has 3 applied control inputs. Leave Mode 3?"

This is the only modal confirmation in the entire interaction model. All other
actions are non-modal.

---

## Gap 6 — Stress-Test: Five Governing Premises Against Gaps 2–5 and Persona-Grounded Findings

Taking each of the five governing premises from the first-principles document and
running it through Gaps 2–5 and the persona-grounded review findings. Three verdicts
are possible: (a) survives unchanged, (b) survives with qualification, (c) must be
replaced. No premise requires replacement.

---

### Premise 1 — Primary viewport is the instrument cluster; context is navigable

**Stress tests:**

- Gap 2B (multi-entity): which entity's instruments are primary? → Entity selector
  determines the primary entity. One entity primary at a time. The premise survives.
  The context (choropleth showing all entities) is always navigable. ✓
- Gap 2C (confidence tier): Tier 4 instruments belong in the primary viewport —
  location does not imply quality. Their visual treatment communicates quality. ✓
- Gap 3 (exogenous shocks): shocks are visible on the trajectory view via orange
  vertical lines. The trajectory view is in the primary viewport. ✓
- Gap 5 (mode transitions): primary viewport is always the instrument cluster
  regardless of mode. The control plane zone occupies adjacent space (reserved zone),
  not the primary viewport itself. ✓
- Persona-grounded review (PR #388): Premise 1 holds for all five personas. ✓

**Verdict: Survives unchanged.** No qualification needed.

---

### Premise 2 — Instruments always visible without drawer, without scroll

**Stress tests:**

- Gap 2A (step-based feedback): during computation, instruments show a "computing"
  state but remain visible. Visible-but-updating is still visible. The "computing"
  state does not remove instruments from the viewport. ✓
- Gap 2B (multi-entity): secondary entity instruments require one interaction (entity
  selector). The premise applies to primary instruments of the current entity —
  it does not claim that every entity's instruments are simultaneously visible
  without interaction. ✓
- Gap 2C (confidence tier): Tier 4 instruments must not be in Zone 3. They must be
  visible in the instrument cluster with their tier treatment. This is an extension
  of Premise 2. → **Requires qualification.**
- Persona-grounded review: Premise 2 serves four of five personas. Amara (Evaluative)
  requires a companion requirement about methodology path accessibility — this is a
  new Premise 6 addition, not a modification of Premise 2. ✓

**Verdict: Survives with one qualification:** *"Confidence tier is a primary instrument
attribute, not Zone 3 documentation. All primary instruments display their confidence
tier on the instrument face — Tier 4 instruments do not visually resemble Tier 1
instruments."*

---

### Premise 3 — Step axis is the shared frame for all instruments

**Stress tests:**

- Gap 1B (step annotation): the step axis must display calendar date and event label
  in Mode 1. This is the most significant finding from the persona-grounded review.
  The premise is architecturally correct but underspecified as a display requirement.
  → **Requires mandatory qualification.**
- Gap 2A (step-based feedback): all instruments update simultaneously when a
  computation completes. The "simultaneous" requirement makes Premise 3 a state
  management invariant, not only a visual invariant. → **Requires qualification.**
- Gap 2B (multi-entity Mode 1): the step axis alignment between two historical entities
  uses programme step alignment (key decision event as Step 1), not calendar date
  alignment. This is a Mode 1-specific qualification. → **Requires qualification.**
- Gap 5 (mode transitions): the step axis persists across all three modes. The
  annotation layer changes (event labels in Mode 1, none in Mode 2/3). ✓

**Verdict: Survives with mandatory qualifications:**
- In Mode 1, the step axis displays calendar date and event label on every step
  marker (per Gap 1B schema requirements). This is mandatory — not optional.
- All instruments that display the step axis update simultaneously when a step is
  navigated or a computation completes (single render cycle).
- In Mode 1 multi-case comparison, step axis alignment is by programme step
  (key decision event), not by calendar date.

---

### Premise 4 — Each mode has its own primary cognitive task; the architecture must not privilege any one mode at the cost of making another impossible

**Stress tests:**

- Gap 2B (multi-entity): multi-entity scenarios require Mode 1 multi-case comparison,
  which is distinct from Mode 2 scenario comparison. The premise creates the
  conceptual space for this distinction. ✓
- Gap 5 (mode transitions): mode transitions are explicit user actions — no mode can
  be accidentally entered. This preserves the cognitive task distinction per mode. ✓
- Persona-grounded review: the premise was found insufficient because it defined
  one primary cognitive task per mode when in fact different personas have different
  primary cognitive tasks *within the same mode* (Eleni vs. Andreas in Mode 1).
  → **Requires mandatory extension.**

The first-principles document defined Mode 1's primary cognitive task as "trajectory
reconstruction" — correct for Eleni but incomplete as a statement of what Mode 1
must serve. The persona document reveals four different Mode 1 cognitive tasks
(Eleni: trajectory reconstruction; Andreas: historical pattern recognition; Amara:
backtesting validation; Aicha: legible narration of a completed case). The architecture
must not collapse Mode 1 to trajectory reconstruction alone.

**Verdict: Survives with a mandatory extension:** *"Within each mode, different personas
have different primary cognitive tasks. The Mode 1 instrument cluster must support
both trajectory reconstruction (Eleni) and historical pattern recognition (Andreas)
without requiring them to share the same cognitive path. Mode 1 achieves this via
the trajectory view + mandatory event annotation layer — one instrument serves both
tasks by layering event context on top of the composite score trajectory."*

---

### Premise 5 — Control plane zone reserved before it is built

**Stress tests:**

- Gap 3 (exogenous shocks): the control plane zone must contain both the policy
  input form and the exogenous shock injection form simultaneously. The reserved
  zone must be large enough to accommodate both. → **Requires layout specification.**
- Gap 4 (live A/B comparison): the live A/B comparison is in the trajectory view
  — not in the control plane zone. The control plane zone contains the input surface;
  the trajectory view shows the output. Adjacent but distinct. ✓
- Gap 5 (mode transitions): the control plane zone is empty in Mode 1, occupied
  by scenario configuration in Mode 2, occupied by the control plane in Mode 3.
  The zone's presence is invariant; its content changes. ✓
- Persona-grounded review: Premise 5 is neutral for Personas 3, 4, 5 and serves
  Personas 1 and 2. No tension found. ✓

**Verdict: Survives with a layout specification:** *"The control plane zone must
accommodate, at minimum, when Mode 3 is introduced: a policy input form (2-3
parameter fields + step selector), an exogenous shock injection form (shock type
selector + step selector), and an applied inputs/shocks history list. A zone
reserved without minimum size constraints may be reserved too narrowly for its
actual Mode 3 content."*

---

### New — Premise 6 (from persona-grounded review, Amara)

**Source:** Persona-grounded review, Activation 1, Q2, Premise 2 analysis.
Amara (Evaluative entry state) requires methodology documentation to be accessible
within one interaction of any instrument output. The original five premises do not
address this.

**Stress tests:**

- Gap 2C (confidence tier): confidence tier badges on instrument faces link to
  the methodology documentation for that indicator. If the badge is interactive
  (tap → methodology note), this satisfies Premise 6. ✓
- Gap 5 (mode transitions): methodology documentation is accessible in all three
  modes. Not mode-specific. ✓

**Verdict: New premise required.** The original five premises leave Amara's
Evaluative and Retrospective entry states without an equivalent architectural
guarantee. Premise 6 closes that gap.

---

## Revised Six Governing Premises

The five governing premises from the first-principles document, incorporating all
qualifications from Gap 6 and the persona-grounded review. Premise 6 is new.
These are the premises the Engineering Lead will adopt for all M9 UX decisions.

Any M9 UX proposal that cannot be evaluated against these six premises is premature.

---

**Premise 1 — The primary viewport is the instrument cluster.
Geographic context is always accessible but never primary.**

*Survives unchanged from the first-principles document.*

The choropleth shows where effects are distributed. The instrument cluster shows
whether the programme is safe. In Mode 3, the pilot watches instruments, not
terrain. This premise survives all five personas, all three mode requirements,
multi-entity scenarios, and confidence tier complexity without qualification.
It is the architectural load-bearing claim of the Case B verdict.

---

**Premise 2 — Primary instruments are always visible without opening a drawer,
without scrolling, at any supported viewport. Confidence tier is a primary
instrument attribute — displayed on the instrument face, not in Zone 3.
A Tier 4 instrument does not visually resemble a Tier 1 instrument.**

*Qualified by Gap 2C (confidence tier visual differentiation).*

The original premise specified location (always visible without navigation). The
qualification adds epistemic honesty: visibility without misrepresentation. An
instrument that is visible but communicates false certainty by looking identical
to a higher-confidence instrument is not "visible" in the full sense — it is
present but misleading. The confidence tier visual system (solid/dashed curves,
opacity gradation, tier badges) makes the instrument's epistemic standing a
first-class visual attribute.

---

**Premise 3 — The step axis is the shared frame for all instruments. In Mode 1,
the step axis displays calendar date and event label on every step marker —
this is mandatory, not optional. All instruments that display the step axis
update simultaneously when a step is navigated or a computation completes.**

*Qualified by Gap 1B (Mode 1 step annotation) and Gap 2A (simultaneous updates).*

The original premise specified the step axis as shared. The qualifications add:
(a) in Mode 1, the step axis must be annotated — without calendar dates and event
labels, the step axis is the shared frame for Lucas and Eleni but is illegible to
Andreas and Aicha. The annotation is the difference between Premise 3 serving
two personas and serving four. (b) "Shared" is enforced by simultaneous updates —
instruments that show different states because they updated at different times
violate the shared frame invariant even if they share the same axis structure.

---

**Premise 4 — The primary cognitive task differs by mode and by persona within
each mode. The architecture must not collapse the Mode 1 cognitive task to
trajectory reconstruction alone — Mode 1 must support both trajectory
reconstruction (Eleni) and historical pattern recognition (Andreas) without
requiring them to share the same cognitive path.**

*Extended from the first-principles document's per-mode framing.*

The original premise stated one cognitive task per mode, which was correct as a
structural claim (Mode 1 ≠ Mode 2 ≠ Mode 3) but insufficient as an architectural
specification (within Mode 1, different personas have incompatible cognitive tasks
that the same instrument cluster must serve). The extension does not change the
mode architecture — the trajectory view + mandatory event annotation layer serves
both Eleni (composite score trajectory) and Andreas (annotated political timeline)
by layering event context on top of the trajectory data. Mode 1 does not need
two different instrument clusters; it needs one instrument cluster that is not
stripped of its annotation layer.

---

**Premise 5 — The control plane is a persistent layout zone, adjacent to the
primary instrument cluster, reserved in the layout architecture before it is
built. The zone must accommodate at minimum: a policy input form, an exogenous
shock injection form, and an applied inputs/shocks history list.**

*Extended from the first-principles document's reservation-only framing.*

The original premise reserved the zone. The extension specifies the minimum zone
content at Mode 3 introduction, ensuring the reservation is sized correctly from
M9 onward. A zone reserved without a minimum size constraint may be reserved
too narrowly — the policy input form and exogenous shock injection form are
distinct surfaces that must both be visible simultaneously (per Gap 3: their
visual separation is an epistemic requirement, not a layout preference).

---

**Premise 6 — Methodology documentation is accessible within one interaction
of any instrument output. Confidence tier badges are interactive: tapping any
badge opens the methodology note for that indicator (confidence tier justification,
source data vintage, comparison group if synthetic).**

*New premise. Sourced from persona-grounded review, Amara (Evaluative entry state).*

The original five premises leave the Evaluative and Retrospective entry states
(Amara's primary entry states) without an equivalent architectural guarantee. For
Amara, the methodology layer is not Zone 3 deliberate navigation — it is the
primary surface from which her session begins. Without Premise 6, the instrument
cluster serves Eleni's Reactive entry state and Lucas's Preparatory entry state
while leaving Amara unable to inspect the methodology from within the instrument
cluster. Premise 6 does not conflict with the original five premises — they did
not address it. It closes the gap.

---

## Summary for the Engineering Lead

Six gaps have been closed to Frontend Architect specification precision.

**Gap 1A** provides a step-by-step Mode 3 walkthrough for Eleni's February 2012
session, traceable to a 10-component requirement table. The consequential findings:
scenario duplication with single-parameter modification is the minimum viable
preparation workflow; the comparison view must auto-prompt when a second scenario
completes; the delta alert panel must show step-level severity delta, not binary
fire/no-fire; fiscal equivalence must appear in the comparison view header without
navigation; confidence tiers must be translated to negotiation-defensibility labels
in the alert panel.

**Gap 1B** mandates three fields on every Mode 1 step marker: step index, calendar
date, and event label for significant steps. These are fixture schema requirements
(`effective_from`, `step_event_label`, `step_significance`) — not display preferences.
A Mode 1 fixture without `step_event_label` on SIGNIFICANT steps is incomplete and
must not ship. This requirement closes the most consequential finding from the
persona-grounded review: without it, the step axis serves Lucas and Eleni while
being opaque to Andreas and Aicha.

**Gap 2** identifies three structural breaks in the flight simulator analogy and
derives specific qualifications: step-based feedback requires atomic simultaneous
instrument updates (state management contract); multi-entity scenarios require an
entity selector that is always visible (not in the entity drawer); confidence tier
requires visible differentiation on the instrument face (not only in Zone 3).

**Gap 3** specifies the blue/orange cross-layer visual system for distinguishing
policy inputs from exogenous shocks at the control plane, trajectory view, and MDA
alert panel. Color consistency across all three layers is a hard contract —
it cannot be satisfied by one layer and not the others. The causal attribution in
alert text is the negotiating instrument: the distinction between "caused by policy
input" and "caused by exogenous shock" is the difference between two types of
negotiating claims.

**Gap 4** establishes that Mode 3 live A/B comparison is automatic — any applied
control input creates the A/B split without requiring the user to invoke a
comparison mode. The visual design (ghost baseline curves at 50% opacity, divergence
fill region, shared MDA floor lines) is specified. The minimum preconditions
(completed baseline scenario, at least one applied control input, shared step axis)
are defined.

**Gap 5** identifies which instruments persist unchanged across modes (trajectory
view, MDA alert panel, four-framework position readout, step axis) and which are
mode-specific (control plane, event annotation layer, PMM header label). Mode
transitions are explicit user actions with a persistent mode indicator, no
side-effect transitions, and a single modal confirmation only when unsaved state
would be discarded.

**The revised six governing premises** incorporate all qualifications. The three most
consequential changes from the original five:

1. **Premise 3** now mandates Mode 1 step axis annotation — the precondition for
   the step axis serving Andreas and Aicha as well as Lucas and Eleni. This is the
   single most impactful specification change in this document.

2. **Premise 4** now acknowledges multiple cognitive tasks within Mode 1, preventing
   an implementation that optimizes for trajectory reconstruction alone and produces
   a Mode 1 instrument cluster that is opaque to the Political Advisor and the
   Institutional Decision-Maker.

3. **Premise 6** is new — methodology documentation as Zone 2 mandatory — closing
   the gap the original premises left for the Evaluative and Retrospective entry
   states. Without it, the instrument architecture serves four personas while
   leaving the Academic Researcher without an equivalent architectural guarantee.

Issue #363 is closed by this document.
