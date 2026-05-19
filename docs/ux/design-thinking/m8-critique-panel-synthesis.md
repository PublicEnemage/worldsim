# M8 Interaction Model Critique — Panel Synthesis

> Date: 2026-05-18
> Scope: Cross-panel synthesis of three independent agent reviews of the M8
>        interaction model critique produced by the UX Design Thinking Agent
> Panel composition: UX Designer Agent (frame owner), Development Economist
>        (DIC policy workflow perspective), Chief Methodologist (DIC epistemics)
> Input document: docs/ux/design-thinking/m8-interaction-model-critique.md
> Also reviewed: CLAUDE.md, north-star.md, user-journeys.md,
>        information-hierarchy.md, frontend-m8-brief.md

---

## Purpose

The UX Design Thinking Agent produced a formal critique of the M8 interaction
model (PR #355). Three independent agents were subsequently asked to evaluate
the same material without access to each other's responses. This document
synthesizes the panel's output into a structured record of:

1. Cross-cutting concerns raised independently by two or more panel members
2. Direct disagreements requiring Engineering Lead decision
3. Premises the panel would revise or reject
4. Premises the panel unanimously confirms

Independence was maintained: no agent saw any other agent's response before
answering. The UX Designer Agent reviewed the critique's four questions as the
frame owner. The Development Economist reviewed the critique's three questions
from the policy workflow and canonical user perspective. The Chief Methodologist
reviewed the three questions with a focus on epistemic integrity.

---

## Panel Positions — UX Designer Agent

**Role:** Frame owner; sole authority over information-hierarchy.md,
north-star.md, user-journeys.md.

**Q1 — Does the current UI support the canonical user's mental model?**

Concurred with the critique's diagnosis as substantially correct. Specific
concessions:

- Choropleth: confirmed zero temporal signal for the single-entity case;
  the spatial instrument framing is architecturally accurate.
- Journey A: conceded the "Navigate completed scenario as a time series" step
  is genuinely absent from user-journeys.md, not merely implicit. Filed this
  as a real gap.
- Zone 2B Step Timeline: conceded its current depth is too low given its
  analytical importance.

Defended without revision:

- "Threshold alarm detection" as the primary cognitive task framing. The UX
  Designer's position: alerts already encode step_index; the primary task
  does not require the trajectory view to be Zone 1 first for alarm detection
  to function correctly. The framing captures the decision-moment output even
  if it understates the preparation path.
- The progressive disclosure zone structure. The zone framework itself is
  sound; what needs revision is which instruments occupy which zones, not
  the zone architecture.

**Q2 — Radar chart: fix it, demote it, or replace it?**

Accepted (B) in principle with a sequencing condition:

- Conceded the radar chart's placement at Zone 1B was premature; a trajectory
  view is the right Zone 1B instrument.
- Condition: Zone 1B should be designated as reserved for the trajectory view
  (recorded in information-hierarchy.md) but not actively populated until the
  trajectory view is built to the minimum viable specification. During the
  interim, the radar chart should remain at Zone 1C or high Zone 2A — visible
  without scroll.
- This preserves the multi-framework orientation value of the radar without
  blocking the trajectory view's eventual Zone 1B placement.

**Q3 — Comparison mode**

Accepted the diagnosis for single-entity scenarios as correct. Two additions:

- Input delta visibility: comparison mode should surface not only the output
  delta (which alerts fire in one path but not the other) but also the input
  delta (what parameters differed between the two scenario paths). Without
  this, the specialist cannot reconstruct why the paths diverge.
- Silent mode-switching legibility risk: conditional Zone 1 switching between
  DeltaChoropleth and divergence timeline must be legible to the user — not
  a silent layout change. The mode switch should be announced and navigable.

---

## Panel Positions — Development Economist

**Role:** DIC policy workflow perspective; speaks to IMF negotiation context,
Article IV document conventions, canonical user real-world information diet.

**Q1 — Does the current UI support the canonical user's mental model?**

Confirmed the critique's diagnosis as correct and added that it understates the
severity of one point. The step advance as a "production model not an analysis
model" is the core issue — and it maps directly to how IMF Article IV documents
are structured: projection tables, fan charts, debt-to-GDP trajectories over a
programme horizon. The canonical user reads temporal instruments professionally.
Presenting WorldSim as a one-way clock rather than a navigable time series is
the deepest mismatch with their daily analytical workflow.

Preserved the MDA alert panel without revision: in active negotiation, the
five-second recall surface is correctly designed. The panel argued that the
alert panel and the trajectory view are complementary instruments — the timeline
is the preparation surface, the alert panel is the negotiation-room surface —
and both must be Zone 1 elements for the full workflow.

**Q2 — Radar chart: fix it, demote it, or replace it?**

The change should be made. The radar chart earns Zone 2, not Zone 1. The panel
position was stated without the UX Designer's sequencing condition — the
Development Economist's view is that the trajectory view is already the correct
Zone 1B instrument at the architectural level, and information-hierarchy.md
should document it that way now regardless of implementation timeline.

Sequencing note shared with UX Designer: the radar chart should remain visible
without scroll until the trajectory view is built to its minimum viable
specification — step annotations, MDA threshold lines, uncertainty bands, and
distinct framework plot lines. The point is not to hide the radar but to
correctly classify the trajectory view as the primary instrument in the
documentation now, so implementation decisions are made against the right target.

**Q3 — Comparison mode**

Accepted the single-entity DeltaChoropleth diagnosis as correct. Two additions:

- Delta panel severity trajectory: the delta alert panel should not display
  alerts as binary fire/no-fire. The panel must express severity trajectory —
  whether the threshold is crossed by a narrow or deep margin, and whether that
  margin is widening or narrowing. A binary delta panel understates the
  analytical argument.

- Fiscal equivalence gap (independent of Design Thinking Agent critique):
  comparison mode must surface that the counter-proposal achieves the same
  fiscal objective as the primary scenario, not merely that it produces fewer
  threshold crossings. Without fiscal equivalence demonstration, the specialist
  cannot use the comparison output to counter the IMF's position that the
  alternative is fiscally irresponsible. This gap was not identified in the
  Design Thinking Agent's critique and is raised here as an additive finding.

---

## Panel Positions — Chief Methodologist

**Role:** DIC epistemics; speaks to statistical integrity, uncertainty
quantification, disclosure obligations, and model limitation transparency.

**Pre-question analysis — Epistemic risks of the timeline view:**

The Chief Methodologist flagged risks introduced by making the trajectory view
Zone 1B that the Design Thinking Agent did not address and that must be resolved
as preconditions, not afterthoughts:

1. **Trajectory implication without validation.** A line chart with positive
   slope implies upward trend. WorldSim's propagation engine does not model
   interpolation between steps — intermediate values are not computed, they are
   presented as if linear. Users will read trajectory from the slope; the slope
   geometry is not validated. This is an epistemic representation risk.

2. **Slope magnitude not validated by DIRECTION_ONLY thresholds.** The Greece
   fixture uses DIRECTION_ONLY validation for several indicators (including
   step 5 GDP direction). DIRECTION_ONLY validates the sign of change, not the
   magnitude. A timeline displaying a steep positive slope when the validation
   constraint only ensures the sign is positive creates a misleading visual
   representation — the slope is drawn from a value not known to be accurate.

3. **Cross-framework absolute position comparison unsupported.** If multiple
   framework composite scores are plotted on a shared axis, users will visually
   compare the absolute positions of the lines. The composite scores across
   frameworks are not on a common scale; their absolute positions are not
   comparable. The visual representation implies comparability the architecture
   does not support.

4. **Governance null on timeline is absent line, not zero line.** The governance
   composite score is null in M8. On a radar chart, null is represented as a
   dashed hollow dot — a correctly designed "not yet measured" indicator. On a
   timeline, null must be represented as an absent line, not a zero line or a
   gap that could be read as a measurement of zero. A zero line for a null value
   implies the measurement was taken and the result was zero. This is a
   representation requirement the Design Thinking Agent did not address and that
   must be specified before the timeline view is implemented.

5. **MacroeconomicModule recovery blind spot.** The engine has no endogenous
   recovery mechanism. At step 5 in the Greece scenario, the historical record
   shows GDP growth returning to positive (+0.007%); the engine produces -0.434%.
   A timeline view will display a declining financial composite score line at step
   5, where historical data shows recovery. For the thesis frame (financial
   recovery as the divergence from human development), the timeline would display
   the wrong argument. The radar chart at the current step does not expose this
   as clearly because the viewer cannot construct the step 4–5 slope from it.

**Q1 — Does the current UI support the canonical user's mental model?**

Partially correct diagnosis. Refined formulation: "threshold detection
decontextualized from trajectory" — not "wrong as primary task, but incomplete
as primary task framing." The MDA alert panel is the correct output of the
workflow; the issue is that the workflow's preparation phase, which produces
the input to alert evaluation, has no primary visual surface in the current UI.
The canonical task is not simply detecting thresholds but constructing the
trajectory argument that contextualizes each threshold crossing.

**Q2 — Radar chart: fix it, demote it, or replace it?**

Conditionally supportable as (B). The four pre-question disclosures are
preconditions, not afterthoughts. The trajectory view cannot occupy Zone 1B
and present a correct epistemic posture without all four disclosures embedded
in the visualization specification — not as footnotes but as mandatory
non-suppressible elements. A trajectory view that lacks these disclosures
introduces more epistemic risk than the current radar chart does.

Sequencing position: the disclosure framework must be designed before the
trajectory view is implemented, not after.

**Q3 — Comparison mode**

Accepted the DeltaChoropleth diagnosis as correct for single-entity scenarios.
Architecture: delta alert panel as Zone 1A (the conclusion); trajectory
divergence view as Zone 1B (the evidence). The conclusion should be visible
first; the trajectory view supports the conclusion with the full quantitative
argument.

Fiscal equivalence gap (independently identified): the comparison mode must
demonstrate that the alternative scenario achieves the same fiscal target, or
articulate which fiscal targets it relaxes and by how much. Without this, the
specialist cannot use WorldSim output to counter a fiscal irresponsibility
objection. This is a canonical negotiation workflow gap independent of the
visualization surface choice.

---

## Cross-Cutting Concerns — Raised by Two or More Panel Members Independently

The following concerns were raised by two or more panel members without
coordination. Items raised by all three are marked (×3).

### 1 — Temporal mismatch diagnosis is substantially correct (×3)

All three panel members independently confirmed the Design Thinking Agent's
diagnosis that the choropleth is a spatial instrument misapplied to a temporal
problem. No panel member challenged this finding. The UX Designer was the most
qualified to reject it and did not.

### 2 — Journey A is missing the "Navigate completed scenario" step (×2)

UX Designer and Development Economist independently confirmed this as a genuine
gap in user-journeys.md, not an implicit step. The canonical user's workflow
splits into two distinct phases: running the simulation forward (production) and
reviewing the completed simulation as a navigable time series (analysis). The
current journeys document has only the first.

### 3 — Timeline view should be Zone 1B primary analytical surface (×3)

All three panel members accepted the trajectory view as the correct Zone 1B
instrument, with conditions varying by agent (UX Designer: reservation pending
implementation; Development Economist: document it now; Chief Methodologist:
requires epistemic disclosures as preconditions). No panel member argued the
radar chart should remain Zone 1B once the trajectory view exists.

### 4 — DeltaChoropleth is wrong for single-entity scenarios (×3)

All three panel members independently confirmed this. For single-entity
scenarios, the DeltaChoropleth has no geographic variation to display. It is
the correct instrument for multi-entity scenarios. The Zone 1 surface in compare
mode should be conditional on scenario structure.

### 5 — Delta alert panel as Zone 1A in compare mode (×3)

All three panel members endorsed the delta alert panel — MDA alerts that fire
in one scenario path but not the other — as a Zone 1A element in comparison
mode. This is the primary output: which threshold crossings are avoided and at
which steps.

### 6 — Radar chart should not be removed (×3)

All three panel members explicitly or implicitly rejected removing the radar
chart. The multi-framework orientation value is real and not recoverable from
a timeline view alone. The panel's consensus is: demotion to Zone 1C or high
Zone 2A, not removal.

### 7 — Radar chart should not be moved until trajectory view meets a minimum viable spec (×2)

UX Designer and Development Economist independently specified that the radar
chart should remain visible without scroll until the trajectory view is built
to at least: step annotations, MDA threshold lines overlaid on the trajectory,
uncertainty bands, and distinct framework plot lines. Moving the radar before
the trajectory view meets this standard would degrade the user experience.

### 8 — Three minimum requirements for the trajectory view (×3)

All three panel members independently specified the same three minimum
requirements, in the same order of importance: (1) step annotations for
significant historical events; (2) MDA threshold lines on the trajectory
axis so crossings are visible as the line descends through the floor; and
(3) uncertainty bands implementing the ADR-006 distribution schedule visually.
These are preconditions for the view to function as a structured reasoning
tool rather than a line chart.

### 9 — Fiscal equivalence gap in comparison mode (×2)

Development Economist and Chief Methodologist independently identified a
requirement not in the Design Thinking Agent's critique: comparison mode must
demonstrate that the alternative scenario achieves the same fiscal objective as
the primary scenario, or explicitly state which fiscal targets it relaxes. Without
this, the comparison output cannot be used to counter a fiscal irresponsibility
objection — the canonical counter-argument in an IMF negotiation. This is an
additive finding not traceable to the input critique.

---

## Direct Disagreements Requiring Engineering Lead Decision

### Decision 1 — Primary Cognitive Task framing revision in north-star.md

**The question:** Should north-star.md §Primary Cognitive Task be revised, and
if so, to what formulation?

| Agent | Position |
|---|---|
| UX Design Thinking Agent (input) | Full reframe required: "trajectory threshold detection" replaces "threshold alarm detection" as the primary task |
| UX Designer Agent (frame owner) | Extend, do not replace: "threshold alarm detection" remains correct as the decision-moment output; the critique's framing adds trajectory preparation but does not invalidate the current framing |
| Development Economist | Reframe in spirit: the temporal preparation phase is the primary analytical task; alarm detection is the output of that task, not the task itself |
| Chief Methodologist | Neither: the better formulation is "threshold detection decontextualized from trajectory" — the current framing is incomplete, not wrong; improved by adding the trajectory preparation phase rather than replacing the detection output framing |

**What is load-bearing:** All downstream hierarchy changes — Zone 1 instrument
ordering, trajectory view placement, radar chart position — are defensible
under any of these formulations. The formulation choice in north-star.md
determines which framing future contributors work from. An EL decision is
required because the frame owner (UX Designer) and the critique author
(Design Thinking Agent) disagree, and the two DIC members each offered a
third formulation.

**Engineering Lead options:**
- A: Adopt Design Thinking Agent's formulation — "trajectory threshold detection"
- B: Adopt UX Designer's extension — keep "threshold alarm detection" and add
  explicit documentation of the preparation phase as a distinct prior step
- C: Adopt Chief Methodologist's formulation — "threshold detection
  contextualized by trajectory" (additive framing, not replacement)
- D: Draft a new formulation incorporating all three inputs

### Decision 2 — Radar chart final Zone assignment

**The question:** What zone does the radar chart occupy once the trajectory view
is built?

| Agent | Position |
|---|---|
| UX Designer Agent | Zone 1C or high Zone 2A — visible without scroll, immediately available |
| Development Economist | Zone 2 — earns demotion to secondary zone once trajectory view reaches minimum viable spec |
| Chief Methodologist | No explicit zone specified; supports trajectory view at Zone 1B; implicitly places radar below |

**What is load-bearing:** Information-hierarchy.md §Zone 1 must specify the
radar chart's final position. The UX Designer's condition (visible without
scroll) and the Development Economist's condition (Zone 2) are substantively
different layout choices that affect how much screen real estate the trajectory
view receives.

**Engineering Lead options:**
- A: Zone 1C (visible immediately below the trajectory view, no scroll required)
- B: Zone 2A (requires one scroll unit; trajectory view fills Zone 1)
- C: Conditional — Zone 1C during transition period, Zone 2A after trajectory
  view is validated in usability testing

### Decision 3 — Zone 1B designation: document now vs. populate when built

**The question:** Should information-hierarchy.md designate Zone 1B as the
trajectory view's reserved position now, with the radar chart at Zone 1C as
an interim state? Or should Zone 1B remain unassigned until the trajectory view
is built?

| Agent | Position |
|---|---|
| UX Designer Agent | Designate Zone 1B as reserved for trajectory view now; radar at Zone 1C interim |
| Development Economist | Document Zone 1B as trajectory view's position now, regardless of implementation timeline |
| Design Thinking Agent (input) | Zone 1B is the trajectory view's correct position — implies immediate designation |

**What is load-bearing:** Whether the hierarchy document reflects the intended
architecture (trajectory view at Zone 1B) or the current implementation
(radar chart de facto at 1B). Documenting the intended architecture now
creates a clear implementation target; deferring avoids describing a state
that does not yet exist.

---

## Premises the Panel Would Revise or Reject

### P1 — MDA alert panel is the primary visual element (north-star.md)

**Current premise:** The MDA alert panel is the primary visual element.

**Panel verdict:** Revise. All three panel members agree the alert panel is
the correct threshold alarm output, but it is not the primary visual element
for the preparation phase of the canonical workflow. The trajectory view is
the primary preparation surface. The alert panel is the conclusion surface.
North-star.md's description should clarify this sequencing rather than treating
the alert panel as the single primary element.

**Dissent:** None. All three agents accepted this revision.

### P2 — DeltaChoropleth is unconditionally Zone 1 in compare mode (information-hierarchy.md §COMPARE_VIEW)

**Current premise:** The DeltaChoropleth is always the Zone 1 visualization
surface in comparison mode.

**Panel verdict:** Reject for single-entity scenarios. All three panel members
agreed that the conditional Zone 1 rule is correct: DeltaChoropleth for
multi-entity; scenario-path divergence timeline for single-entity. The
unconditional assignment should be replaced with a scenario-structure-conditional
rule.

**Dissent:** None.

### P3 — The radar chart's current Zone 1B position is final (information-hierarchy.md)

**Current premise:** Radar chart at Zone 1B is the established primary
visualization position in Zone 1.

**Panel verdict:** Revise. All three panel members agree the trajectory view
is the correct Zone 1B instrument and the radar chart should be demoted (to
Zone 1C or Zone 2, per EL Decision 2). Zone 1B for the radar chart was
appropriate when the trajectory view did not exist as a design concept; it
is no longer the correct assignment.

**Dissent:** None on the direction. Zone 1B is wrong for the radar chart
once the trajectory view exists. Disagreement is only on where the radar lands
(Decision 2 above).

### P4 — Step advance is both the simulation control and the analytical navigation (user-journeys.md)

**Current premise:** The step advance workflow serves both the simulation run
(forward progression) and the analyst's review (inspecting individual steps).

**Panel verdict:** Revise. UX Designer and Development Economist independently
confirmed that sequential forward progression is a simulation production model,
not an analysis model. The journeys document should split "Advance" and
"Navigate" into distinct steps with distinct information needs.

**Dissent:** None from the two agents who addressed this. Chief Methodologist
did not directly address user-journeys.md step structure.

---

## Premises the Panel Unanimously Confirms

### C1 — The multi-framework measurement principle is architecturally correct

The radar chart's existence is justified by the multi-framework measurement
principle (financial, human development, ecological, governance simultaneously).
No panel member recommended removing this instrument or the principle it serves.
The debate is about zone placement, not about whether the instrument belongs.

### C2 — The MDA alert panel is correctly designed for its function

All three panel members confirmed the MDA alert panel is the right instrument
for the threshold alarm output — binary threshold status per indicator at the
current step, with step_index encoded in each alert. The alert panel is not
the problem; its position as the described "primary visual element" is the
framing problem.

### C3 — The choropleth is appropriate for multi-entity scenarios

No panel member recommended removing the choropleth or replacing it as the
Zone 1 surface for multi-entity scenarios. The critique is scope-specific:
the choropleth is misapplied in the single-entity canonical case. It is
appropriate when geographic variation exists.

### C4 — The trajectory view requires three minimum features to function as a structured reasoning tool

All three panel members converged on the same three minimum requirements:
(1) step annotations; (2) MDA threshold lines overlaid on the trajectory axis;
(3) uncertainty bands implementing ADR-006. A trajectory view without these
is a line chart, not a structured reasoning tool, and should not be placed
at Zone 1B until it meets this specification.

### C5 — The fiscal equivalence gap must be addressed in comparison mode

Development Economist and Chief Methodologist identified this independently;
the UX Designer's zone-specific additions (input delta visibility, mode-switch
legibility) do not contradict it. The panel's consensus, by non-contradiction,
is that comparison mode must demonstrate fiscal equivalence or explicitly
quantify which fiscal targets the alternative relaxes. This is a canonical
negotiation workflow requirement.

### C6 — The timeline view creates epistemic representation risks that require mandatory disclosure

Chief Methodologist was the only agent to enumerate the specific risks in
detail, but neither other panel member contradicted the epistemic concern or
argued the disclosures were unnecessary. The four mandatory disclosures —
interpolation not modeled, no forecast implication, magnitude not validated,
cross-framework absolute position not supported — are not contested findings.
They are consensus preconditions for the trajectory view.

---

## Highest-Priority Engineering Lead Decision

**Decision 1 — The north-star.md Primary Cognitive Task formulation — is the
load-bearing decision.**

It is load-bearing because:

- The zone placement of every instrument in information-hierarchy.md follows
  from what the primary cognitive task is stated to be.
- The "threshold alarm detection" framing is currently used to justify the MDA
  alert panel as "the primary visual element" in north-star.md — a statement
  that will be in direct tension with placing the trajectory view at Zone 1B.
- Future contributors and agents will read north-star.md to calibrate their
  implementation decisions. An unrevised north-star.md that still names the
  alert panel as the primary visual element will conflict with an
  information-hierarchy.md that places the trajectory view at Zone 1B.
- This is a three-way disagreement between: (a) the Design Thinking Agent
  (who has no implementation authority but challenged the premise), (b) the
  UX Designer (who has implementation authority and disagrees on the replacement
  formulation), and (c) two DIC members (who each offered distinct third
  formulations).

**Recommendation:** An EL decision on the formulation should precede any
changes to information-hierarchy.md. The zone hierarchy changes are not
controversial — all panel members accept them. But they should be grounded in
a north-star.md that is internally consistent, not one that contains a vestigial
"alert panel is primary" statement inherited from a pre-trajectory-view era.

The decision is not urgent in the sense of blocking M8 closure — M8 is feature-
complete and these are M9+ design changes. But it should be made before the
trajectory view is scoped for implementation, because the formulation determines
what the trajectory view is the primary instrument for.

---

## Additive Findings Not in the Input Critique

The following findings emerged from panel review and were not present in the
Design Thinking Agent's critique:

| Finding | Source | Priority |
|---|---|---|
| Fiscal equivalence gap — comparison mode must demonstrate alternative achieves same fiscal objective | Development Economist + Chief Methodologist (independent) | High — canon negotiation workflow gap |
| Input delta visibility — comparison mode should surface what parameters differed, not only what outputs differed | UX Designer | Medium — without this, divergence cause is not visible |
| Silent mode-switch legibility risk — conditional Zone 1 switch between DeltaChoropleth and divergence timeline must be announced, not silent | UX Designer | Medium — silent layout changes undermine orientation |
| Governance null on timeline — must be absent line, not zero line; zero implies measurement, null implies absence of measurement | Chief Methodologist | High — representation integrity; zero line would be a false epistemic claim |
| Delta panel severity trajectory — binary fire/no-fire is insufficient; margin depth and trajectory direction required | Development Economist | Medium — binary panel understates negotiation argument |
| MacroeconomicModule step 5 recovery blind spot visible on timeline — engine produces declining financial line where historical shows recovery; timeline makes this more visible than radar | Chief Methodologist | High — thesis frame integrity; timeline would display wrong slope at the thesis step |

---

## Appendix — Input Documents

| Document | Role |
|---|---|
| docs/ux/design-thinking/m8-interaction-model-critique.md | Input critique (UX Design Thinking Agent, PR #355) |
| docs/ux/north-star.md | Primary cognitive task definition |
| docs/ux/information-hierarchy.md | Zone structure and instrument assignments |
| docs/ux/user-journeys.md | Canonical user workflow documentation |
| docs/frontend/frontend-m8-brief.md | M8 component specification |
| docs/demo/m8/reviews/2026-05-18-v0.8.0-stakeholder-review.md | IR Agent review (nine findings, DEMO-001–009) |
| docs/demo/m8/stakeholder-walkthrough.md | M8 presenter guide (PR #351) |
