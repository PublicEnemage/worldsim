# WorldSim UX Architecture — First Principles Review

> Author: UX Design Thinking Agent
> Date: 2026-05-18
> Scope: First-principles review of the current UX architecture against the
>        three-mode flight simulator product vision. This document supersedes
>        the M8 panel synthesis (docs/ux/design-thinking/m8-critique-panel-synthesis.md)
>        on any points where they conflict.
> Engineering Lead directive: treat the three-mode architecture as authoritative
>        and evaluate whether existing documents are correct, not whether they
>        are internally consistent.
>
> Documents read (in order): CLAUDE.md, north-star.md, user-journeys.md,
>   information-hierarchy.md, ADR-005-human-cost-ledger.md,
>   docs/demo/m8/stakeholder-walkthrough.md,
>   docs/ux/design-thinking/m8-interaction-model-critique.md,
>   docs/ux/design-thinking/m8-critique-panel-synthesis.md
>
> **Reader Orientation:** This document is the *derivation* of ADR-008, not a separate
> standard. It derives the five governing premises and the Case A / Case B terminology
> used throughout ADR-008. Read this document when you need to understand *why* ADR-008
> was written the way it was. **ADR-008 (`docs/adr/ADR-008-ux-architecture.md`) is the
> canonical authority** — its Renewal Triggers and Decisions govern what a developer may
> and may not change. When a change you are making is governed by both documents, check
> ADR-008's Renewal Triggers first. (DOC-LEGIBILITY-AUDIT-001, Gap 3, 2026-06-03)

---

## Orientation

This document does not optimize the current UX. It evaluates whether the
current UX architecture can survive the product WorldSim is becoming. The
product is a flight simulator for national policy. That analogy is
architectural — the Engineering Lead has stated this explicitly. A flight
simulator has three interaction modes: Replay, Simulation, and Active Control.
WorldSim must support all three.

The current UX was designed for Mode 1 (Replay). It performs Mode 1
adequately. Mode 3 (Active Control) is coming. The question is whether the
current architecture can be extended to accommodate Mode 3 without rebuilding
or whether it requires a rethink now.

The answer is: it requires a rethink now. The reasoning follows.

---

## Question 1 — Does the current UX architecture survive Mode 3?

### What Mode 3 requires

Mode 3 is the IMF negotiator at the table. Not reviewing a completed
programme. Not constructing a hypothetical in advance. Actively steering
in the moment: applying a policy input — say, a 2% spending cut at step 3
— and reading the trajectory response immediately across all live measurement
frameworks.

This interaction model has four inviolable requirements. They are
inviolable because they follow from what the user is doing, not from design
preference:

**R1 — Primary instruments must be always visible.** The user cannot open
a drawer to read their altimeter during a stall. In WorldSim terms: the
programme trajectory view, PMM indicator, and four-framework composite scores
must be visible at all times, without opening the entity drawer. Not because
it is a nice design goal. Because the user is applying control inputs and
needs to see the instrument response. An instrument the user must navigate
to see is not a primary instrument. It is a secondary instrument with
aspirations.

**R2 — The feedback loop must be spatially immediate.** The pilot applies
input with the yoke; the attitude indicator responds in the same physical
space. The user applies a spending cut control input; the trajectory view
must update in the same viewport region. If the control input is in one
part of the screen and the instrument response is in another, the feedback
loop is severed. The user cannot read the effect of their input.

**R3 — The temporal frame must be primary.** Mode 3 is active steering
across a programme horizon. The primary frame is temporal — what is
happening at this step, what will happen at the next, what has the
trajectory been. Geographic frame is secondary: it provides context about
where the effects are distributed, but it cannot serve as the primary
instrument surface. The pilot does not fly by watching the view out the
windshield; they fly by watching the instruments.

**R4 — Pilot input and exogenous shock must be visually distinguishable.**
A 2% spending cut applied by the user is a deliberate policy choice. A snap
election injected as an exogenous shock is an event the user is testing
against. Both change the trajectory. Only one is under the pilot's control.
The instrument must distinguish between these — in aviation terms, between
yoke deflection and wind shear.

### Audit of the current architecture against Mode 3 requirements

**The choropleth map as primary Zone 1 surface — actively obstructs Mode 3.**

The choropleth occupies approximately 75% of the primary viewport. It
answers one question: "what is the value of a selected attribute across
geographic entities right now?" In Mode 3, the user is not asking that
question. They are asking: "how did the trajectory respond to the control
input I just applied, across all four frameworks?" The choropleth has no
answer to that question. Worse, it occupies the viewport that Mode 3
requires for primary instruments.

A choropleth during active control is the equivalent of placing a satellite
view of the terrain in Zone 1 of a cockpit and moving the altimeter to a
drawer. The terrain view is context. Valuable context. But context that
belongs in a secondary panel, not in the primary viewport that the pilot
consults to avoid dying.

The choropleth is not the problem. Its location is the problem.

**The entity drawer as the container for primary instruments — actively
obstructs Mode 3.**

The current architecture places the primary instruments — radar chart, MDA
alert panel, PMM widget — inside the EntityDetailDrawer. The EntityDetailDrawer
opens when the user clicks an entity on the choropleth. It occupies
approximately 25% of the viewport when open.

In Mode 3, this architecture fails at R1 and R2 simultaneously. The user
cannot maintain situational awareness of their primary instruments while
looking at the map — they have to open a drawer and navigate away from the
control surface to read the instruments. And even when the drawer is open,
it occupies a narrow 25% panel rather than the viewport space required to
display trajectory data legibly.

The drawer paradigm is appropriate for detail (indicator breakdown, cohort
data, methodology notes). It is not appropriate for primary instruments.
A primary instrument in a drawer is not a primary instrument.

**The step advance button as the primary temporal interaction — obstructs
Mode 3 as an interaction model; neutral as an engine mechanism.**

In Mode 1, the step advance button is correct: the user runs through a
completed programme sequentially. In Mode 3, a one-way sequential advance
button is the wrong interaction model. The user needs to apply a control
input at a specific step and see the trajectory response across the remaining
programme horizon — not click through steps one at a time.

The underlying engine mechanism (advancing steps, computing propagation) is
not the problem. The interaction model (button that advances one step, no
direct control input surface, no real-time trajectory response) is the
problem. The engine can be reused; the interaction model requires replacement.

**The DeltaChoropleth in compare mode — obstructs Mode 3 compare.**

Mode 3 comparison is not "compare two pre-built scenarios." It is "compare
this trajectory with my current control inputs vs. the baseline without
them." That is a temporal divergence question on a shared step axis —
two trajectory curves on the same instrument display. The DeltaChoropleth
is a geographic divergence answer to a temporal divergence question. It
cannot serve Mode 3 comparison even with conditional logic.

**What is compatible with Mode 3:**

- The MDA threshold system architecture (threshold values, consecutive-step
  logic, severity enum, framework source) — correct design, wrong location
  in the UI
- The four-framework measurement model (ADR-005) — correct; the measurement
  architecture does not change
- The PMM indicator concept — correct instrument; current Zone 1C placement
  is wrong (in the drawer) but the instrument itself is right
- The zone architecture for progressive disclosure within the instrument
  panel — correct; Zone 1/2/3 applies to the instrument cluster, not to the
  primary viewport

### Verdict

**The current UX architecture does not survive Mode 3 intact.** It requires
fundamental restructuring before Mode 3 can be introduced. The restructuring
is not a component replacement — it is a viewport architecture change. The
primary viewport must show instruments, not context. The entity drawer is
the wrong paradigm for primary instruments.

Modification would not be sufficient. Adding a trajectory view to Zone 1B
in the drawer (the M8 panel synthesis recommendation) would give the user
a trajectory view in a 25% panel beneath the MDA alerts, with the choropleth
still occupying 75% of the viewport. This is not the instrument cluster
architecture Mode 3 requires. It is more instruments in the wrong place.

---

## Question 2 — What are WorldSim's primary flight instruments?

Aviation's primary flight instruments are defined by one criterion: the pilot
cannot fly safely without them being always visible and always current.
The criterion for WorldSim's primary instruments is the same: the canonical
user cannot maintain situational awareness during Mode 3 without them being
always visible and immediately responsive to control inputs.

These are WorldSim's primary flight instruments:

---

**Instrument 1 — Programme Trajectory View**
*The attitude indicator and heading indicator combined.*

What it shows: the four-framework composite scores plotted on a shared step
axis across the full programme horizon. Each framework is a distinct curve.
MDA threshold lines are overlaid on each curve's axis. The user reads the
curves as trajectory — where the programme has been, where it is now, where
it is heading.

Why it is primary: it answers the pilot's orienting question — "where am I
in the space of safe and unsafe outcomes, and in which direction am I
traveling?" A programme where human development is declining while financial
metrics recover is like an aircraft with correct airspeed and wrong altitude.
The trajectory view shows both simultaneously.

What must be true about its responsiveness: when the user applies a control
input (a spending cut, a structural reform), the trajectory curves update to
reflect the new projected path within the current render cycle. Not at the
next step advance. Not after a panel refresh. Immediately. This is the
Mode 3 feedback loop.

Where it must be: always visible without opening the entity drawer, without
scrolling. It occupies the primary viewport — not a panel within a drawer.

---

**Instrument 2 — Policy Maneuver Margin**
*The altimeter.*

What it shows: the remaining degrees of freedom before the corrective
maneuver window closes. Current value, trend direction (improving/
deteriorating), and, when available, the rate of change.

Why it is primary: the altimeter is the instrument that tells the pilot
whether they have time to recover from the current trajectory or whether
the ground is close. PMM serves the same function. A finance minister whose
PMM is declining rapidly has less time to respond to a CRITICAL MDA alert
than one whose PMM is stable. This contextualizes every other instrument
reading. Without it visible, the user cannot assess the urgency of what the
other instruments are showing.

What must be true about its responsiveness: it must update with each step
advance and with each control input application. When a spending cut is
applied, the user must see immediately whether it improves or degrades the
policy maneuver margin — that is the instrument telling them whether they
pulled back on the yoke correctly or made the stall worse.

Where it must be: always visible, adjacent to the trajectory view. Not Zone
1C in the drawer. Not a widget that requires scrolling to see.

---

**Instrument 3 — MDA Alert Panel**
*The ground proximity warning system (GPWS).*

What it shows: threshold crossings by severity, with step index, indicator,
and affected cohort. Fires when a programme trajectory crosses a human cost
floor.

Why it is primary: GPWS does not live alongside the altimeter. It
interrupts the display. It demands attention. MDA CRITICAL and TERMINAL
alerts are not findings to consider alongside other findings — they are
terrain warnings. The design implication: CRITICAL and TERMINAL alerts must
have visual weight that commands attention, not vie for it. The current
design (color + label in a panel) is partially correct. The location (in
the entity drawer) is not.

What must be true about its responsiveness: the alert must fire visibly
when a trajectory crosses a threshold — including when the threshold crossing
occurs as a result of a control input applied in Mode 3. The user applies a
control input; if it causes a threshold crossing at a future step, the alert
fires.

Where it must be: visible without opening the entity drawer. The top-severity
alerts command the primary display.

---

**Instrument 4 — Four-Framework Current Position**
*The airspeed and altitude readouts — current state in each measurement axis.*

What it shows: the current composite score for each framework at the current
step — a single value per framework, always visible. Not the full radar chart
with its polygon — a simpler, always-visible readout of the four numbers.

Why it is primary: the user needs to know their current position in all four
measurement spaces simultaneously. In Mode 3, before applying a control input,
the user reads their current position. After applying it, they read the new
position. This is a four-number scan, not a full radar chart analysis.

The radar chart is appropriate for the deeper profile view (how do the four
axes compare to each other? what is the shape of the current situation?).
But the primary instrument is simpler: four current composite scores,
always visible, immediately updated.

Where it must be: adjacent to the PMM and trajectory view. Part of the
primary instrument cluster.

---

**What is not a primary flight instrument:**

The choropleth map is context — the terrain visible through the windshield.
Important context. The pilot uses terrain awareness. But the pilot does not
fly by looking out the window; they fly by watching their instruments. The
choropleth shows where effects are distributed geographically. It is always
relevant; it is never primary.

The radar chart polygon is a secondary instrument — the attitude and
heading displayed as a spatial relationship rather than as numbers. Valuable
for profile analysis (preparation mode), not for moment-to-moment situational
awareness. It belongs in Zone 2 relative to the four-number current position
readout.

The framework detail panels (Zone 2A) are secondary instruments — the
detailed indicator breakdown behind the composite score. Used in preparation;
not needed during active control.

---

## Question 3 — The control plane UX architecture

The control plane is where the user applies policy inputs and introduces
exogenous shocks. These are the product's interactive core in Mode 3. The
design of the control plane must follow from the feedback loop requirement
(R2): control input and instrument response must be spatially co-located.

**Where the control plane lives:**

The control plane occupies a persistent zone adjacent to the primary
instrument cluster. Not a modal. Not a slide-out panel. Not a configuration
view accessible via a settings screen. The yoke is in front of the pilot
because the pilot needs to see the instruments while using the yoke. The
control plane must be visible while the instruments are visible.

This means the control plane competes for viewport space with the instrument
cluster. The design consequence: the instrument cluster must be compact
enough that the primary instruments remain legible when the control plane
is visible. This is a layout constraint, not a feature choice. It rules
out a layout where the instrument cluster fills the full viewport and the
control plane appears as an overlay.

**The feedback loop design:**

Three states, visually distinguishable:

1. *Input pending:* The user has entered a control input (e.g., -2% spending
   at step 3) but has not applied it. The instrument cluster shows the
   trajectory without the input. The pending input is visible in the control
   plane with a visual treatment indicating "not yet applied."

2. *Input applied — computing:* The user has applied the input. The engine
   is computing the trajectory response. The instrument cluster shows a
   computing state on the affected trajectory curves — not a blank, not an
   error, but a "trajectory updating" indicator. This is brief (seconds) but
   must be legible. The user must know the input was registered.

3. *Trajectory updated:* The instrument cluster shows the new trajectory.
   The control plane records the applied input with its step index. The
   feedback loop is complete.

The signal that the input was registered is the trajectory update — the
instrument showing the new path is the confirmation. There is no separate
"input accepted" indicator. The altimeter moving when you pull back on the
yoke is the confirmation that the yoke input was registered.

**Distinguishing policy inputs from exogenous shocks:**

A policy input is a deliberate control action. The user chose it. The
trajectory change resulting from it is the consequence of the user's decision.

An exogenous shock is an injected event: snap election, currency crisis,
creditor defection, geopolitical shock. The user is testing the scenario
against an event they did not choose. The trajectory change resulting from
it is the consequence of an external force the user is evaluating.

The UI must preserve this distinction at three levels:

*Control plane:* The control input form and the exogenous shock injection
form are visually distinct. They are not in the same list. Policy inputs
appear under "Policy instruments." Exogenous shocks appear under "Scenario
shocks." The separation is not cosmetic — it reflects the epistemic
distinction between what the pilot controls and what the environment does
to the pilot.

*Trajectory view:* Applied policy inputs appear as trajectory inflection
points marked with a policy annotation (e.g., "−2% spending applied at
step 3"). Injected exogenous shocks appear as event markers with a different
visual treatment (e.g., a vertical line labeled "SHOCK: snap election,
step 3"). Both types of annotation are on the same timeline, but they are
visually distinguishable.

*Alert panel:* When a MDA threshold crossing results from a policy input,
the alert reads differently from a crossing caused by an exogenous shock.
The causal chain matters for the argument: "this path crosses the threshold
because of the consolidation trajectory" is a different negotiating claim
from "this path crosses the threshold because an exogenous shock overwhelmed
the policy framework."

**What happens to comparison mode in Mode 3:**

Mode 2 comparison is between two pre-built scenarios. Mode 3 comparison is
between the current control-input trajectory and a baseline.

These are different. Mode 2 comparison requires the DeltaChoropleth (for
multi-entity) or a divergence timeline (for single-entity) — the panel
synthesis is correct about this. Mode 3 comparison is always a temporal
divergence — two trajectory curves on the same instrument display:
the baseline (trajectory without the control input), and the active
trajectory (trajectory with the control input applied). No choropleth.
No scenario selection. The comparison is live and continuous.

The architectural implication: the trajectory view in Mode 3 must natively
support two concurrent curves — baseline and active. This is not the same
component as the Mode 2 divergence timeline, even if they look similar. The
Mode 3 trajectory comparison is always relative to the baseline; the Mode 2
comparison is between two independently constructed scenarios. The distinction
matters for what the view displays and how the user interacts with it.

---

## Question 4 — The three pending EL decisions in this larger context

### Decision 1 — north-star.md Primary Cognitive Task formulation

**Is this the right question?** Partially. The question as posed assumes a
single primary cognitive task. The flight simulator product vision has three
modes, and each mode has a distinct primary cognitive task:

- Mode 1 (Replay): The primary task is trajectory analysis — understanding
  what the historical programme did, step by step, and what thresholds were
  crossed. Threshold alarm detection is the output of trajectory analysis in
  Mode 1, not the input.

- Mode 2 (Simulation): The primary task is trajectory construction —
  building alternative paths and comparing them against human cost floors.
  The analyst is an architect of scenarios, not a reader of completed ones.

- Mode 3 (Active Control): The primary task is situational awareness — the
  continuous, real-time monitoring of the instrument cluster while applying
  control inputs. This is Endsley Level 2 (comprehension) and Level 3
  (projection) in real time. It requires different UI affordances from both
  Mode 1 and Mode 2.

**If stated as a single-task question, which answer is correct for Mode 3?**
None of the four formulations in the panel synthesis. "Threshold alarm
detection" is correct for the negotiation-room recall moment in Mode 1/2.
"Trajectory threshold detection" is correct for the preparation phase of
Mode 1/2. "Threshold detection decontextualized from trajectory" is a
diagnosis of the current UI, not a prescription. None of these is the
primary task in Mode 3, which is: maintain situational awareness across all
measurement frameworks while applying and evaluating control inputs.

**Should this decision be deferred?** No — it should be reframed. North-star.md
should acknowledge three modes and define the primary cognitive task per mode.
The current "threshold alarm detection" formulation remains correct for Mode 2
active negotiation. It is incomplete as a statement of the primary task for
the product. Resolving it as a single formulation is the wrong question. The
document should be extended, not resolved.

### Decision 2 — Timeline view zone assignment (Zone 1B vs Zone 1C)

**Is this the right question?** No. It is the wrong question entirely.

Zone 1B vs Zone 1C is a zone assignment within the entity drawer. It assumes
the trajectory view lives in the drawer. For Mode 1/2, the panel synthesis
debate between Zone 1B and Zone 1C is real and worth resolving. But for Mode
3, the trajectory view does not live in the drawer at all — it is the primary
viewport surface, outside the drawer, always visible.

Resolving this as a drawer zone assignment decision proceeds from the wrong
premise. Implementing the trajectory view in Zone 1B of the drawer and
shipping it as M9 scope would embed the Mode 3 architecture in the wrong
location. When Mode 3 is introduced, the trajectory view would need to be
relocated from the drawer to the primary viewport — work that could be avoided
by not placing it in the drawer in the first place.

**What is the right question?** What does the primary viewport contain? The
answer to that question determines where the trajectory view lives — and it
is not a zone assignment question, it is a viewport architecture question.

**Should this decision be explicitly deferred?** Yes, with reframing. The
decision that needs to be made is not "which zone does the trajectory view
occupy in the drawer?" but "is the trajectory view a primary viewport element
or a drawer element?" That is the EL decision. Zone 1B vs Zone 1C follows
from it.

### Decision 3 — Comparison mode conditional Zone 1 switch

**Is this the right question?** Yes — and the answer extends further than
the panel synthesis reached.

The comparison mode Zone 1 surface should be:
- Multi-entity, Mode 2: DeltaChoropleth (panel synthesis is correct)
- Single-entity, Mode 2: Divergence timeline on a shared step axis (panel
  synthesis is correct)
- Mode 3 (any entity count): Baseline vs. active trajectory on a shared
  step axis — always temporal, never choropleth (panel synthesis did not
  address Mode 3)

The correct answer to Decision 3 is: Zone 1 in comparison mode is determined
by scenario structure AND mode. The panel synthesis gave the Mode 2 answer
correctly. The Mode 3 answer is: comparison is always temporal in active
control mode, because the user is comparing the effect of a live control
input against the baseline, not comparing two pre-built geographic scenarios.

This decision should be resolved with the Mode 3 case explicitly added,
not deferred.

---

## Question 5 — Rethink or incremental: the case

**Case B — A UX architecture rethink is warranted before M9 implementation
work begins.**

The case for incrementalism would be: the current architecture works for
Modes 1 and 2, Mode 3 is several milestones away, and the cost of a rethink
now outweighs the benefit. The implementation work planned for M9 (trajectory
view, zone restructuring) can proceed without a premise change, and the Mode
3 issues can be addressed when Mode 3 is scoped.

This case fails because of the viewport architecture problem. The planned M9
implementation work would place the trajectory view in Zone 1B of the entity
drawer — a 25% panel beside the choropleth. Once that component is built,
tested, and shipped, it occupies a location. Moving it to the primary viewport
when Mode 3 is introduced is not refactoring; it is rebuilding the layout
from a different premise. The component would be correct; its home would be
wrong, and the home change would require rebuilding the surrounding layout.

The cost of a rethink before M9 is low. These are document changes:
- North-star.md: extend to three modes with per-mode primary cognitive task
- Information-hierarchy.md: reframe the governing principle from "threshold
  alarm detection under cognitive load" (single-task, single-mode) to a
  three-mode instrument architecture
- User-journeys.md: sketch Journey C (Mode 3) as a placeholder, establishing
  that the interaction model must accommodate active control

No code changes are required before M9 begins. The rethink is premisechanges
to three documents. M9 implementation then proceeds against premises that
survive Mode 3 introduction.

The cost of deferring is concrete:
1. The trajectory view is implemented in the drawer (Zone 1B) in M9
2. The choropleth remains in the primary viewport in M9
3. Mode 3 is scoped in M10/M11
4. The viewport architecture change is then required as part of Mode 3 scope
5. The M9 trajectory view component must be relocated and resized — a refactor
   that costs a sprint, plus regression testing, plus potential demo
   disruption

The M8 IR Agent review already documents the cost of premature structural
decisions: DEMO-002 through DEMO-006 are all consequences of the drawer being
too narrow and too dense. That density problem was produced by placing too
many primary instruments in a 25% panel. Adding the trajectory view to that
25% panel without changing the viewport premise repeats the same error at
larger scale.

**The minimum viable rethink — what to change, preserve, and invent:**

*Discard:*

The governing principle that "the primary viewport is the choropleth and the
primary instruments are in the drawer." This is the root premise. The
information-hierarchy.md governing principle ("the information hierarchy exists
to serve threshold alarm detection under cognitive load") survives if re-read
as applying to the instrument cluster, not to the full viewport layout. But
the layout premise — choropleth primary, instruments secondary — must be
discarded.

The entity drawer as the container for primary instruments. The drawer
paradigm is correct for detail. It is wrong for instruments. Primary
instruments are always visible. A primary instrument in a drawer is a
contradiction in terms.

The assumption that "active negotiation mode" is the hardest interaction
scenario the architecture must support. Active control (Mode 3) is harder.
The architecture must be survivable at the harder level.

*Preserve:*

The Zone 1/2/3 progressive disclosure hierarchy — it is correct and should
govern the instrument cluster. Zone 1 of the instrument cluster (always
visible without scroll): primary instruments. Zone 2 (one interaction):
indicator detail, cohort breakdown, confidence tiers. Zone 3 (deliberate
navigation): methodology disclosures, raw tables, backtesting fidelity.

The MDA threshold architecture and severity system — correct and well-designed.
The threshold system does not need to change.

The four-framework measurement model (ADR-005) — the architecture of
composite scores, the boundary proximity normalization, the MDA threshold
system — all correct. This is not a measurement architecture question.

The choropleth itself — as a secondary context surface. Geographic visualization
is valuable. The choropleth is the right instrument for geographic distribution
questions. It does not need to be removed; it needs to be moved.

The radar chart — as a secondary profile instrument. Correct for cross-
framework snapshot comparison. It belongs in Zone 2 of the instrument cluster,
accessible without navigation during preparation, not competing with primary
instruments for Zone 1.

*Invent:*

A primary viewport architecture that places the instrument cluster
(trajectory view + PMM + MDA alerts + four-framework current position) in
the primary viewport. The choropleth moves to a secondary surface — still
accessible, still prominent, but not occupying the 75% primary viewport.

The control plane zone — a persistent layout zone adjacent to the instrument
cluster. This does not need to be built in M9; it needs to be reserved in
the layout architecture so that its introduction in Mode 3 scope does not
require tearing out M9 work.

Journey C — a sketch of the Mode 3 active control journey that establishes
the interaction model at a premise level. Not a detailed user journey with
every step specified. A premise sketch that ensures M9 decisions about the
instrument cluster and the trajectory view are made against the right target.

**The cost of doing this now vs. the cost of doing it at Mode 3 introduction:**

Now: three document changes, estimated two to four hours of writing work.
No code changes. No test changes. M9 implementation begins with correct
premises.

At Mode 3 introduction: one sprint of refactoring, test updates, potential
Playwright suite rework, possible demo disruption, and a conversation
explaining to stakeholders why the layout changed.

The asymmetry is significant. The cost is trivially low now and meaningfully
high later. This is the standard argument for addressing architectural
premises before implementation — and it applies here.

---

## Five Design Premises for M9

These premises govern all M9 UX decisions and remain valid through Mode 3
introduction. Each is one rule followed by why it survives Mode 3.

---

**Premise 1**

*The primary viewport shows instruments; geographic context is always
accessible but never primary.*

The choropleth shows where effects are distributed. The instrument cluster
shows whether the programme is safe. In Mode 3, the pilot watches instruments,
not terrain. This premise survives Mode 3 because it is the premise that
makes Mode 3 possible — an architecture where the primary viewport is
geographic context cannot accommodate active control without a full viewport
restructure.

---

**Premise 2**

*Primary instruments are always visible without opening a drawer, without
scrolling, at any supported viewport.*

The instruments are: programme trajectory view, PMM, MDA alert panel, and
four-framework current position. If any of these requires opening the entity
drawer, it is not a primary instrument — it is a secondary instrument with
a wrong label. This premise survives Mode 3 because Mode 3 is the hard test:
if the instruments are visible during active control without navigation, they
are visible during preparation and negotiation without navigation.

---

**Premise 3**

*The step axis is the shared frame for every instrument. There is no instrument
that does not reference it.*

The choropleth shows a step. The trajectory view shows all steps on the same
axis. The MDA alert references the step it fires. The PMM shows trend since
the last step. Every instrument in the cluster is a view into the same
programme step axis. When the user navigates to a step, every instrument
updates. This premise survives Mode 3 because Mode 3 active control is the
application of inputs at specific steps — the step axis is the coordinate
system of the control interaction.

---

**Premise 4**

*The primary cognitive task differs by mode. The architecture must not
privilege any one mode at the cost of making another mode impossible.*

Mode 1: threshold analysis of a completed programme. Mode 2: trajectory
construction across alternative paths. Mode 3: situational awareness during
active control. North-star.md must define the primary task per mode, not as
a single task that governs all modes. This premise survives Mode 3 because
it is the premise that creates space for Mode 3 — a north-star that defines
only the Mode 1/2 task will produce a UI that is correct for Modes 1/2 and
impossible for Mode 3.

---

**Premise 5**

*The control plane is a persistent layout zone, adjacent to the primary
instrument cluster, reserved in the layout architecture before it is built.*

The control plane does not need to be implemented in M9. It needs to be
reserved. A layout architecture that fills the viewport with the instrument
cluster without reserving space for the control plane will require tearout
when Mode 3 is introduced. A layout architecture that reserves the control
plane zone — even as an empty region — ensures Mode 3 can be introduced
without layout restructuring. This premise survives Mode 3 because it is
the premise that makes Mode 3 a feature addition rather than a layout rebuild.

---

## Summary for the Engineering Lead

This document is self-contained. The four questions answered above lead to a
single conclusion:

The current UX architecture (choropleth as primary viewport, instruments in
a 25% drawer) was designed for Mode 1 and performs Mode 1 adequately. It
actively obstructs Mode 3 because it inverts the instrument/context
relationship: context is primary, instruments are secondary.

The M9 implementation planned under the current architecture — trajectory
view in Zone 1B of the drawer — would deepen this inversion. It adds the
right instrument in the wrong location. When Mode 3 is introduced, that
location must change, at implementation cost.

The minimum viable rethink is three document changes and a reserved layout
zone. It does not require code changes before M9 begins. It requires that
the UX documents governing M9 implementation be updated to reflect the three-
mode architecture before M9 implementation begins.

The five premises above are the specific governance rules for M9 UX proposals.
Any M9 UX proposal that cannot be evaluated against these five premises is
premature.

The highest-priority action is not resolving the pending Decision 1 (Primary
Cognitive Task formulation). That decision is answerable once the three-mode
architecture is acknowledged in north-star.md — because the correct
formulation is "three modes, three primary tasks." The highest-priority action
is updating information-hierarchy.md's governing principle to reflect that the
primary viewport is the instrument cluster, not the choropleth. That change
unblocks everything else.
