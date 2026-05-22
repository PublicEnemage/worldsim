# UX North Star

> Owned by the UX Designer Agent. This document is the authoritative source
> for who we are building for, what they are trying to do, and what the
> experience must make possible. All frontend decisions are evaluated against
> it. Last updated: 2026-05-21 (EL Decisions 1/2/3 — per-mode cognitive tasks,
> viewport architecture, comparison mode conditional; closes Issue #365).

---

## Canonical User

A debt restructuring specialist at a finance ministry. They are working
alongside IMF staff on a program design — not as a passive recipient of
conditionality terms, but as a counterpart who needs to understand the
structural implications of what is being proposed and where the proposed
path becomes politically and humanly unsustainable.

They have a graduate-level economics background. They are not a data
scientist. They do not have time to learn a new analytical tool from
scratch during an active negotiation. They need to get to the relevant
signal in minutes, not hours.

They are operating under cognitive load. There are people in the room,
a document on the table, and a clock running. The tool must work for
them in that context, not in a calm research environment.

Five personas — from finance ministry specialist to academic economist to
institutional decision-maker — provide concrete instantiations of this
canonical user across roles, entry states, and scenarios:
`docs/ux/personas.md`.

---

## Primary Use Case

Understanding whether a proposed fiscal adjustment path crosses human
cost thresholds that would make the program politically and socially
unsustainable — and being able to articulate specifically which
indicators cross which thresholds, at what point in the program
timeline, and for which population cohorts.

The output of this use case is not a chart. It is a defensible argument
in a negotiation: "This path produces these human consequences by year
three, which in comparable historical cases produced political
instability that caused program collapse. Here is the evidence."

The tool exists to give the finance ministry the same analytical
standing as the institution sitting across the table.

---

## Resolved Design Questions

These questions were open at M4 close. The answers are binding UX
constraints for all M5 distribution visualization work and for M6
frontend decisions.

### 1. Primary Cognitive Tasks by Mode

**Question:** What is the user's primary cognitive task at the tool — and
does it vary across the three interaction modes (Replay, Simulation,
Active Control)?

**Answer: Yes — per-mode cognitive tasks, not a single universal formulation.**

The M4-era answer ("threshold alarm detection") correctly identified a
central user task but applied it uniformly across contexts where the
cognitive task differs. EL Decision 1 (Issue #364) supersedes it. The
three-mode per-task formulation was validated against all thirteen
marquee acceptance cases across primary, secondary, and tertiary tiers.

**Mode 1 (Replay) — Trajectory reconstruction AND historical pattern recognition**

Both tasks are valid primary cognitive tasks within Mode 1; both must be
served by the instrument cluster. The academic economist (Persona 4) needs
trajectory reconstruction: does the simulation reproduce what actually
happened? The political advisor (Persona 3) needs historical pattern
recognition: did the trajectory follow a recognizable pre-collapse pattern?
These are distinct tasks with a shared instrument. The step axis annotation
requirement — calendar dates and event labels on SIGNIFICANT steps — is the
precondition for serving both tasks. Without it, the step axis serves the
finance ministry specialist while remaining opaque to the political advisor
and the institutional decision-maker.

**Mode 2 (Simulation) — Threshold-safe path construction**

The preparation task: which policy path achieves the required fiscal outcome
while keeping all four framework indicators above their Minimum Descent
Altitudes? The user is not passively scanning for alarms — she is
constructing a defensible path. The comparison surface (divergence timeline
for single-entity scenarios) shows which path crosses fewer thresholds, not
just whether a specific path crosses one.

**Mode 3 (Active Control) — Real-time steering within human cost constraints**

Active negotiation: proposed terms applied as control inputs in real time,
trajectory effects propagate and update the instrument cluster. The live A/B
comparison — baseline ghost curves at 50% opacity versus active trajectory —
makes the effect of each proposed term immediately legible. The MDA alert
panel causal attribution ("caused by: −2% spending cut applied at step 3")
is the negotiating instrument: it distinguishes threshold crossings caused by
the proposed policy from those caused by the underlying scenario trajectory.

**Design implication (EL Decisions 1 and 2):**

The primary viewport is the instrument cluster. The trajectory view (four
composite score curves on a shared step axis) is the primary Zone 1 instrument
— the frame that makes all three per-mode cognitive tasks legible. The MDA
alert panel and PMM widget are co-primary Zone 1 elements within the instrument
cluster. The entity selector is a persistent header element, visible without
navigation in all three modes.

The choropleth is a navigable context surface, not a primary viewport element.
The EntityDetailDrawer is demoted to detail and methodology surface — primary
instruments are in the instrument cluster viewport, not inside the drawer.

The M4-era design implication — "the MDA alert panel is the primary visual
element; the radar chart is secondary" — correctly identified the alert panel's
primacy but placed it inside the drawer. The alert panel occupies Zone 1 of the
instrument cluster viewport directly. Distribution bands on individual indicators
must remain legible as proximity-to-threshold information — the ADR-006 composite
alert rule (ci_lower < floor AND mean ≤ 1.5 × floor) operationalizes this.

Full hierarchy specification: `docs/ux/information-hierarchy.md`.

---

### 2. Preparation, Active Negotiation, and Historical Analysis

**Question:** Does the user's relationship to the tool differ across the three
interaction modes — and how does this map to real-world usage contexts?

**Answer: Yes — the cognitive task and information hierarchy both differ
across modes. The instrument architecture and underlying analytical standard
do not.**

**Three modes, three contexts:**

*Mode 2 (Simulation) — Preparation: building the case*

The specialist is at her desk the night before. She has time to explore.
Primary cognitive task: threshold-safe path construction — which consolidation
path keeps all four framework indicators above their MDAs? Every panel is
relevant: full distribution bands, cohort breakdown, the comparison divergence
timeline between the proposed path and the counter-proposal. The trajectory
view shows where the proposed path fails; the divergence timeline confirms
the counter-proposal avoids it.

*Mode 3 (Active Control) — Active negotiation: steering in real time*

The specialist is in the room, tablet open. The IMF proposes a modified
term. She applies it as a control input. The trajectory updates: live A/B
comparison shows the effect of the proposed term against the baseline she
built the previous night. The MDA alert panel causal attribution confirms
whether the proposed term is what causes the threshold crossing. She is not
re-exploring — she is navigating the terrain she already mapped, with
the proposed modification injected directly.

*Mode 1 (Replay) — Historical analysis: trajectory reconstruction*

The academic economist or political advisor examines how a trajectory actually
unfolded. Primary cognitive tasks: trajectory reconstruction (does the model
reproduce what happened?) and historical pattern recognition (did the
trajectory follow a recognizable pre-crisis pattern?). The demonstrative
entry state — Aicha Mbaye oriented in 60 seconds without driving the tool —
is also a Mode 1 context: a pre-loaded, completed historical fixture navigated
by someone other than the driver.

**What stays the same across all three modes:**

The instrument cluster is always the primary viewport. The step axis is always
the shared coordinate system. The four-framework measurement is always
simultaneous — no framework is hidden while another is examined. The underlying
analytical standard — defensible argument, quantified uncertainty,
pre-calibration disclosure — does not change between modes.

**Design implication:**

Progressive disclosure achieves all three modes without separate screens.
The instrument cluster serves all three cognitive tasks when the correct mode
is active. The mode indicator — always visible in the primary viewport header —
tells both the user and any observer which cognitive task is active. The top
1–3 MDA alerts must be readable without scrolling at all supported viewports.

Journeys for each mode: `docs/ux/user-journeys.md`.

---

### 3. Professional Framing of the Human Cost Ledger

**Question:** Does the canonical user experience the human cost
indicators as warning signals (adversarial: "this crosses a floor"),
as evidence (neutral: "this is what the data shows"), or as capability
analysis (aligned: "this is what this path does to the people your
ministry serves")?

**Answer: Capability analysis framing is primary.**

The finance ministry official serves her population. The human cost
ledger shows what a proposed fiscal adjustment path does to the people
she is mandated to defend. This is not a warning against her own
choices — she is the defending party, not the party whose behavior
is being constrained. An MDA CRITICAL alert is analytical output
that supports her negotiating position, not an alarm against her
proposed policy.

The CLAUDE.md "Defense, not offense" principle is the architectural
expression of this. The tool builds situational awareness and
defensive capability for vulnerable actors. Capability analysis
framing makes the human cost ledger an asset, not a constraint.

**Design implication for M5 alert text and M6 visual language:**

MDA alert language should be declarative: "poverty headcount crosses
CRITICAL threshold at step 3" is a finding. "WARNING: poverty headcount
approaching dangerous level" is an alarm. The first is a piece of
evidence the specialist can cite; the second creates anxiety about the
analysis rather than confidence in it.

Visual weight remains high — threshold crossings are the most important
output and must be visually prominent. But color coding (WARNING /
CRITICAL / TERMINAL) is for triage, not for alarm. The language of the
alert panel should make the user feel analytically equipped, not
cautioned.

---

## Distribution Visualization Acceptance Criteria

These three criteria define the observable outcomes for M5 distribution
rendering. They become the second Playwright suite (Phases 3–4 per
ADR-006 Decision 12) once distribution visualization components are
implemented. Each criterion is derived from the primary cognitive task
(threshold alarm detection) and the capability analysis framing.

**Criterion 1 — Distribution alert fires before the mean crosses the floor**

> Given a scenario advanced to a horizon where an indicator's 80% CI lower
> bound is below its MDA floor and the point estimate is within 1.5× the
> floor, when the user opens the entity drawer, then the MDA alert panel
> shows the indicator with an alert labeled as distribution-source, and this
> alert is visually distinguishable from a point-estimate alert — even if no
> point-estimate alert has fired.

This criterion operationalizes the primary cognitive task at the
distribution layer. The system warns the user that the distribution
places material probability mass below the floor before the central
estimate confirms it.

**Criterion 2 — Pre-calibration disclosure is non-suppressible**

> Given any scenario at any step with distribution bands visible, when the
> entity drawer shows measurement output, then the ia1_disclosure text is
> visible and contains the word "pre-calibration," and no user interaction
> (weight adjustment, framework tab change, or scroll to top of drawer) makes
> it disappear from the rendered DOM.

This criterion enforces the "No False Precision" principle at the UI
layer. The specialist's negotiating argument must rest on correctly-labeled
uncertainty. She cannot present pre-calibration bands as calibrated
confidence intervals without disclosure.

**Criterion 3 — Band width is proportional to projection horizon**

> Given scenario A advanced 1 step and scenario B advanced 3 steps, when the
> user views the same indicator in both scenarios with uncertainty bands
> visible, then the rendered band for scenario B is visually wider than for
> scenario A, and each band display shows the declared coverage level (80%)
> and the is_pre_calibration flag.

This criterion validates that the ADR-006 Decision 1 band schedule (±10%
at 1 year, ±35% at 3–5 years) is correctly rendered. The specialist must
be able to see that uncertainty grows with projection horizon — a property
she needs to understand to present the argument correctly when the IMF
challenges her year-3 projections.
