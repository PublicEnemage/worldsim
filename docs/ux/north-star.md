# UX North Star

> Owned by the UX Designer Agent. This document is the authoritative source
> for who we are building for, what they are trying to do, and what the
> experience must make possible. All frontend decisions are evaluated against
> it. Last updated: 2026-05-02 (open questions resolved; user journeys in
> `docs/ux/user-journeys.md`).

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

### 1. Primary Cognitive Task

**Question:** When the user scans a scenario output showing distributions
across multiple indicators, what is her primary cognitive task — threshold
alarm detection, trajectory tracking, or cross-scenario comparison?

**Answer: Threshold alarm detection.**

The canonical user's purpose at the tool is to determine whether a
proposed fiscal adjustment path crosses human cost thresholds. This is
a binary question: has any indicator crossed a floor, or is any
indicator's distribution at material risk of crossing one?

Trajectory tracking (where is this heading?) and cross-scenario
comparison (how does A differ from B?) are both present in the
workflow, but they are activated *after* the threshold scan. The user
first asks: is anything in the danger zone? Only then does she ask:
when does it get there, and would an alternative path avoid it?

**Design implication for M5 distribution visualization:**

The MDA alert panel is the primary visual element. The radar chart is
secondary (it shows which dimensions are under stress, supporting the
threshold scan). The delta choropleth is tertiary (activated only after
the user has identified what to compare).

Distribution bands on individual indicators must be legible as
proximity-to-threshold information — not statistical detail. The
ADR-006 composite alert rule (ci_lower < floor AND mean ≤ 1.5 × floor)
directly operationalizes this task: it fires when the distribution
places material probability mass below the floor, before the mean
has crossed. The alert must be the first thing the user reads.

---

### 2. Preparation Mode vs. Active Negotiation Mode

**Question:** Does the user's relationship to the tool differ between a
preparation session (the night before) and an active negotiation session
(tablet open on the table, 90 seconds to respond)?

**Answer: Yes — the information hierarchy differs; the underlying
data requirement and primary cognitive task do not.**

**What changes:**

In preparation mode, the specialist is building the argument. She has
time to explore. She needs the full distribution, the cohort breakdown,
the ability to advance step by step and observe where thresholds are
crossed, and the ability to compare proposals. Every panel is relevant.
The four-framework radar chart, MDA severity progression, and cohort-level
indicator tables are all primary surfaces.

In active negotiation mode, the specialist is citing the argument
she already built. She needs one thing in seconds: the threshold
crossing she identified the night before — indicator, step, severity,
cohort. She is not re-running the analysis. She is reading a conclusion
that must be immediately visible.

**What stays the same:**

The primary cognitive task is identical: threshold alarm detection.
The MDA alert panel is the primary entry point in both modes — in
preparation it is the scanning surface; in negotiation it is the
recall surface. The underlying analytical standard — defensible
argument, quantified uncertainty, pre-calibration disclosure — does
not change between modes.

**Design implication for M6:**

Progressive disclosure achieves both modes without separate screens.
The alert panel surfaces the headline finding (severity + indicator +
step + top affected cohort) in the negotiation-mode scan. Clicking
through opens the full preparation-mode detail. The M6 information
hierarchy decision should ensure the top 1–3 MDA alerts are readable
without scrolling in any viewport likely to be used at a negotiating
table.

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
