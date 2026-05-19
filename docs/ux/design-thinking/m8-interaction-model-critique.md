# M8 Interaction Model Critique — UX Design Thinking

> Author: UX Design Thinking Agent
> Date: 2026-05-18
> Scope: Post-M8 design premise audit — interaction model, primary visualization,
>        timeline proposal, comparison mode
> Source documents reviewed: CLAUDE.md, north-star.md, user-journeys.md,
>   information-hierarchy.md, frontend-m8-brief.md,
>   2026-05-18-v0.8.0-stakeholder-review.md, stakeholder-walkthrough.md,
>   all five M8 screenshots

---

## Preamble

This document is a challenge to design premises, not a component specification.
It evaluates whether the foundational assumptions embedded in the current UX
documents are correct, and recommends changes to those assumptions where the
evidence from M8 indicates they are not. Implementation decisions follow from
correct premises; they cannot correct wrong ones.

The four questions below are answered in full. Reasoning is not summarized away.
The ranked premise-change recommendations follow.

---

## Question 1 — Does the current UI support the canonical user's mental model?

The canonical user is a debt restructuring specialist. Their mental model is
temporal and differential: what state was the system in at entry, what state
is it in now, what changed at each step, and what drove those changes? This is
not a snapshot mental model — it is a trajectory mental model. They think in
before/after, in inflection points, in the question "when did this break and
what caused it?"

The current UI does not support that mental model. It frustrates it at three
specific points.

**Friction point 1: the choropleth is a spatial instrument solving a temporal
problem.** The primary visual surface is a world map. Maps answer the question
"what is different between here and there?" The canonical user's question is
"what is different between now and then?" These are not the same question, and
a map cannot answer the second one. When the specialist advances from step 1 to
step 3 to step 5, the map does not change — confirmed by the IR review
(DEMO-001) and visible in the screenshots. The specialist is using a spatial
instrument to track a time series. The instrument is wrong for the task.

This is not a calibration problem. The IR review correctly identifies a
single-entity color scale problem, but the deeper issue is architectural: even
if Greece's color changed visibly with each step, the map would still be showing
her one step's value, not the trajectory. She cannot see "GDP went from -7% to
-3% to +0.7%" from a choropleth — she can only see "at step 5, GDP is in this
color band." The trajectory is invisible regardless of color scale fix.

**Friction point 2: the step advance is a simulation control, not a navigation
tool.** The specialist's temporal mental model requires the ability to move
through time in both directions, to hold two steps in view simultaneously, and
to annotate which step matters for her argument. The current interface presents
step advance as a simulation progression button — a one-way clock. She cannot
go backward without resetting. She cannot see step 2 and step 5 simultaneously.
She cannot mark "this is the inflection point." The step counter confirms
sequential progression but does not make the sequence navigable as data.

**Friction point 3: the drawer is a place, not a timeline.** When the specialist
opens the entity drawer, she sees the state at the current step. The drawer has
no persistent representation of the trajectory — no "this indicator was 85 at
step 1, 72 at step 2, 61 at step 3." The information-hierarchy.md §2B notes
"Step Timeline / Scenario Progress" as a Zone 2 element, but it is described as
a view of key indicator trajectories accessible via scroll or a tab — meaning it
requires deliberate navigation to reach, and its current implementation status
is unclear. In any case, it is secondary to a Zone 1 that does not itself
communicate trajectory.

The north-star.md's primary cognitive task framing — "threshold alarm detection"
— is correct as far as it goes. But it treats threshold detection as if it were
a static scan: is anything in the danger zone right now? The canonical user's
actual task is more specific: at what step did this threshold get crossed, what
was the trajectory leading up to that crossing, and is the crossing deepening
or stabilizing? That is a trajectory question, not a snapshot question.

The current UI answers the snapshot question. The canonical user needs the
trajectory question answered first, and from that answer they derive whether a
threshold has been crossed and when.

**Specific UI frictions visible in the screenshots:**

The five screenshots show an interface that is visually identical across all
frames in the 75% of the screen occupied by the choropleth map. The right-side
drawer changes, but it is narrow — approximately 25% of the viewport — and
densely stacked. The radar chart is present but its axes are not legible. The
MDA alert panel fires the same two alerts at every step visible in the
screenshots (step 1, step 3, step 5). There is no visual representation of
trajectory anywhere in the primary or visible secondary zones.

The step counter in the toolbar header ("Step 1/6", "Step 3/6") is the only
temporal marker in Zone 1. It is a number, not a visualization of trajectory.

---

## Question 2 — The radar chart: fix it, demote it, or replace it?

**Answer: (B) — the radar chart is a secondary visualization and something else
should be primary.**

The reasoning follows from the analysis in Question 1 and from what the radar
chart does and does not do.

The radar chart encodes a cross-framework comparison at a single moment in
time. It answers: "How does this entity's composite score on financial,
human development, ecological, and governance frameworks compare to each other
right now?" This is a genuinely important question — it is the multi-currency
measurement principle that is one of WorldSim's core architectural commitments.
The radar chart is the right instrument for answering it.

But it is not the right instrument for answering the primary cognitive task
(threshold detection over a programme timeline), and it is not the instrument
that makes the WorldSim thesis self-evident. The thesis — as stated explicitly
in the stakeholder walkthrough — is: "Financial recovery and human recovery are
not the same event." This is a claim about two trajectories diverging over time.
A radar chart shows the current cross-framework profile at one step. To make
the divergence claim visible, the presenter must direct the audience's attention
to two axes and explain that one has moved and the other has not, and that this
represents temporal divergence. That cognitive work is being done by the
narrator, not by the visualization.

The Engineering Lead's observation that "the radar chart is losing relevance"
and the tool "feels like functionality quilted together" is a design coherence
diagnosis, not a feature-count complaint. The radar chart was introduced as
the primary multi-framework visualization in M6, when two axes were null. Now
at M8, three axes carry live data and the four-axis architecture is substantive.
But the more substantive the radar becomes, the more its structural limitation
is exposed: it shows one moment, the canonical user needs a sequence of moments.

The argument for making the radar primary (option A) rests on its role as "the
visual argument that a country's situation cannot be understood through one lens"
(information-hierarchy.md §1B). This argument is correct and important. The
radar does communicate multi-framework measurement in a way that nothing else
currently in the UI does. Demoting it risks losing this — which is why (C)
replacement is wrong. The multi-framework argument needs a visual form.

The argument against making the radar primary is that its primary visual claim
(the four-framework profile) answers a different question from the user's
primary cognitive task (threshold detection over a trajectory). Placing the
radar in Zone 1B above the framework panels means the user's eye lands on
"here is the current multi-framework profile" before it lands on "here is
whether any threshold has been crossed and when." For the canonical user in
an active negotiation, that ordering is wrong.

The correct placement is: radar chart as the thumbnail view in Zone 1 (present
for at-a-glance multi-framework orientation) with the trajectory view as the
primary Zone 1 analytical surface. The radar chart's value is orientation, not
argument. The argument is in the trajectory.

This requires a change to information-hierarchy.md §1B, which currently treats
the radar as "secondary primary weight" in Zone 1 and specifies it as the
visualization of "the visual argument that a country's situation cannot be
understood through one lens." That framing is right about the radar's value but
wrong about where it should sit in the hierarchy relative to a trajectory view.

---

## Question 3 — The timeline view proposal

**Evaluation:** The timeline view would make the WorldSim thesis more
self-evident than the current radar chart. It would not make it self-evident
without additional design work. What would be lost is recoverable.

The WorldSim thesis — financial recovery is not human development recovery —
is a claim about temporal divergence between two measurement frameworks. A
timeline view that plots multiple framework composite scores on a shared step
axis, with each framework as a distinct plot line, would make this divergence
directly visible: one line rises between step 4 and step 5, another line
remains flat. The audience does not need the narrator to explain that the axes
are moving differently — they can see the lines diverging.

This maps directly to the canonical user's mental model. A debt restructuring
specialist thinks in time series. They read IMF programme review documents
that contain tables of annual projections. They compare actual vs. projected
outcomes. They identify inflection points. A timeline graph with a step axis
is the most natural representation of programme-duration dynamics they
encounter in their daily work. The IMF's own Article IV documents show
GDP paths, fiscal balance trajectories, and debt-to-GDP projections as line
charts over time. WorldSim's timeline view would be immediately legible to
this user without any explanation.

The specific design proposal — multiple frameworks superimposed on a shared
step axis, each with its own plot line style and color — is sound in principle
but has one critical requirement: the vertical axis for each framework must be
independently scaled, or normalized to a common reference, or the crossing
pattern must be made explicit. If all frameworks share a 0–1 scale, the
relative positions of the lines convey both individual performance and
cross-framework comparison. If they do not share a scale, the display must
make clear that the absolute positions are not comparable — only the slopes
and crossing patterns are meaningful.

**What the timeline view would gain over the radar chart for the thesis:**

The radar shows the asymmetry as a shape deformation at a single step: one
axis long, another short. To understand that this deformation represents
temporal divergence, the viewer must (a) register the shape, (b) compare it
to a prior step's shape they saw earlier and must now recall, and (c) interpret
the difference as divergence over time. This is three cognitive steps, the
second of which requires memory of a prior state. The timeline view compresses
this to one step: the lines are visibly diverging.

For the M8 thesis frame specifically (step 5, financial partial recovery while
human development remains at crisis depth), the timeline view would show
financial line rising between steps 3–5 while the human development line
remains flat or continues falling. This is the argument in its simplest visual
form.

**What would be lost by replacing the radar with a timeline view:**

The radar chart communicates two things the timeline does not: (1) the
multi-framework profile at a single moment, showing how this country's
situation looks across all four dimensions simultaneously; and (2) the
shape of the profile — the radar's polygon shape is a visual fingerprint
that can be compared across countries or scenarios without reference to a
specific axis.

These are real analytical values. The cross-framework snapshot and the
shape fingerprint are not recoverable from a timeline view. A timeline
shows trajectories but not the current multi-framework profile.

The correct response is not to choose one or the other but to establish
which is Zone 1 and which is Zone 2. The timeline view should be the
primary trajectory surface (Zone 1 or high Zone 2). The radar chart
should be the secondary profile surface (lower Zone 1 or Zone 2). The
information hierarchy currently inverts this.

**What the timeline view requires to deliver on its promise:**

Step annotations for significant events — the 2012 second memorandum at step
2, the 2013 primary surplus target at step 4 — so the specialist can anchor
the trajectory to the historical record she knows. MDA threshold lines on the
relevant framework's timeline axis — so the crossing is visible as the line
descends through the floor, not only as an alert in a separate panel. Uncertainty
bands on each line — implementing the ADR-006 distribution schedule visually on
the timeline, so the specialist can see the band widening with projection
horizon. These are not optional features; without them, the timeline view is a
line chart, not a structured reasoning tool.

---

## Question 4 — Comparison mode: what should it look like?

**The DeltaChoropleth is the wrong instrument for single-entity comparison.
The right instrument is a timeline divergence view.**

The DeltaChoropleth answers: "Where in geographic space do these two scenarios
produce different outcomes?" This is a meaningful question when comparing
scenarios across multiple entities — when the analyst wants to see which
regions of a country are affected differently, or which countries in a
multi-country scenario respond differently to two policy paths. For a
single-entity scenario with only Greece, there is no geographic variation to
display. The choropleth shows Greece colored the same in both scenarios because
the delta in the geographic dimension does not exist.

The user-journeys.md §Journey A Step 6 documents the intended comparison
workflow correctly: she creates a second scenario (the counter-proposal), uses
compare mode to visualize divergence, then opens the entity drawer for the
entity of interest to verify that fewer alerts fire. The DeltaChoropleth is
listed as the primary Zone 1 visualization for COMPARE_VIEW in
information-hierarchy.md. For the single-entity case, this Zone 1 surface
is empty of signal.

**The right interaction model for single-entity comparison:**

The canonical user's comparison question is: "How does this alternative path's
trajectory compare to the primary path's trajectory, framework by framework,
step by step?" This is precisely the question the timeline view answers — and
it extends naturally to comparison mode: two sets of lines on the same step
axis, the primary scenario in one visual treatment and the comparison scenario
in another, the divergence between them visible as the gap between two lines.

The alert differential should be a first-class comparison output: which MDA
alerts fire in the primary scenario that do not fire in the comparison, and at
which steps? This is the core negotiating output — "this path crosses the
threshold at step 3; this alternative path does not." It should be visible
without opening the entity drawer.

**The compare mode premise that needs to change:**

The current premise in information-hierarchy.md §COMPARE_VIEW is that the
DeltaChoropleth is always the Zone 1 surface in comparison mode. This is
correct for multi-entity scenarios and wrong for single-entity scenarios.
The premise needs to become: Zone 1 in compare mode is determined by the
scenario structure. For multi-entity scenarios, the DeltaChoropleth is Zone 1.
For single-entity scenarios, the Zone 1 surface is a scenario-path divergence
timeline showing framework trajectories for both scenarios on a shared step
axis. The switch between these two comparison surfaces should be automatic
based on the number of entities in the active scenario.

Beyond the surface switch: the comparison mode should surface a delta alert
panel as Zone 1A — the set of MDA alerts that appear in one scenario but not
the other, framed explicitly as the delta. "These thresholds are crossed under
the primary path and are not crossed under the alternative path." This is
the argument; the visualization supports the argument, not the reverse.

---

## Ranked Premise Change Recommendations

The following changes are ranked by their impact on the canonical user's
ability to complete the primary cognitive task. Each recommendation names
the specific document change required.

---

### Rank 1 — Reframe the primary cognitive task as trajectory detection, not snapshot detection

**Current premise:** north-star.md §Primary Cognitive Task states the
canonical user's primary task is "threshold alarm detection" — a binary
question: has any indicator crossed a floor?

**Why it is wrong:** The canonical user's task is not binary and not a snapshot.
It is temporal: at what step was the threshold crossed, what trajectory produced
that crossing, is the crossing deepening, and which alternative trajectories
avoid it? The current framing produces a UI that is excellent at showing a
current state and weak at showing how that state came to be and where it is going.

**The change:** north-star.md §Primary Cognitive Task should reframe the
primary task as trajectory threshold detection — the task of determining whether
a programme-duration path crosses human cost thresholds, at what step, and
through what trajectory. Threshold alarm detection remains part of the task but
is the output of trajectory analysis, not a replacement for it.

**Document change:** Revise north-star.md §Primary Cognitive Task answer and
its downstream "Design implication" paragraph. The current framing that "the MDA
alert panel is the primary visual element" would become "the programme trajectory
view is the primary visual element; the MDA alert panel is the threshold alarm
output of that view."

---

### Rank 2 — Establish the programme trajectory view as Zone 1 primary; demote the radar chart to Zone 1 secondary

**Current premise:** information-hierarchy.md §Zone 1 places the MDA alert
panel at 1A and the radar chart at 1B ("secondary primary weight"), with the
Step Timeline buried in Zone 2B.

**Why it is wrong:** The timeline view — multiple framework trajectories on a
shared step axis — is the primary instrument for the canonical user's task and
should be Zone 1. The radar chart is a valuable secondary orientation instrument
but answers a different question. Placing it at 1B above the timeline inverts
the hierarchy relative to the task.

**The change:** information-hierarchy.md §Zone 1 should add a new 1B slot for
the programme trajectory view (framework composite scores over the programme
horizon, with MDA threshold lines overlaid) and reassign the radar chart to
a lower 1B or upper 2A position. Zone 2B "Step Timeline / Scenario Progress"
should be promoted to Zone 1B.

**Document change:** Revise information-hierarchy.md §Zone 1 hierarchy to
insert the trajectory view as 1B, reassign radar chart to 1C or 2A, and remove
Zone 2B's "Step Timeline" entry (it is being promoted, not duplicated).

---

### Rank 3 — Make the programme trajectory view the primary comparison surface for single-entity scenarios

**Current premise:** information-hierarchy.md §COMPARE_VIEW states that the
DeltaChoropleth is always Zone 1 in compare mode.

**Why it is wrong:** The DeltaChoropleth is a spatial comparison instrument.
For single-entity scenarios, no spatial comparison exists. Zone 1 in compare
mode is empty of signal for the most common canonical use case (a single
country under a programme).

**The change:** information-hierarchy.md §COMPARE_VIEW should establish a
conditional Zone 1 rule: for multi-entity scenarios, DeltaChoropleth is Zone 1;
for single-entity scenarios, a scenario-path divergence timeline (two scenario
trajectories on a shared step axis) is Zone 1, with a delta alert panel showing
MDA alert differences between scenarios as Zone 1A.

**Document change:** Revise information-hierarchy.md §COMPARE_VIEW to replace
the unconditional DeltaChoropleth Zone 1 assignment with a scenario-structure-
conditional rule.

---

### Rank 4 — Establish the radar chart's function as orientation, not argument

**Current premise:** information-hierarchy.md §1B describes the radar chart as
"the visual argument that a country's situation cannot be understood through one
lens." The stakeholder walkthrough §Step 5 treats the radar asymmetry as "the
WorldSim argument in a single image."

**Why it is incomplete:** The radar chart communicates the current multi-
framework profile but does not make a temporal argument. "Financial recovery
and human recovery are not the same event" is a claim about trajectories over
time, not about a snapshot profile. The radar can support this argument after
it has been established by a trajectory view, but it cannot establish it
independently.

**The change:** information-hierarchy.md §1B should reframe the radar chart's
function as multi-framework orientation (answering "how does this entity's
current profile compare across frameworks?") rather than as the primary thesis
visualization. The "visual argument that a country's situation cannot be
understood through one lens" remains correct — but the argument is made by
showing the trajectory divergence first, with the radar confirming the current
multi-framework profile as supporting evidence.

**Document change:** Revise information-hierarchy.md §1B description paragraph
to reframe radar chart as orientation instrument. Revise stakeholder-walkthrough.md
§Step 5 to anchor the thesis argument in the trajectory view (once it exists)
rather than in the radar asymmetry alone.

---

### Rank 5 — Add a step-navigation model to the user journeys

**Current premise:** user-journeys.md §Journey A Step 3 describes scenario
advance as a sequential forward progression: "She advances the scenario step
by step." Step 3 is labeled "Advance: run through the program horizon."

**Why it is incomplete:** Sequential forward progression is a data production
model, not a data analysis model. After the six steps have been run, the
specialist is not advancing sequentially — she is navigating: going to step 3
to examine the third memorandum, going back to step 1 to compare the baseline,
jumping to step 5 to observe the partial recovery. The journeys document has no
step for "navigate the completed scenario as a time series." This is the gap
between production and analysis.

**The change:** user-journeys.md §Journey A should split "Advance" into two
steps: "Advance: run through the program horizon" (the sequential simulation
execution) and "Navigate: review the completed programme as a time series"
(non-sequential step access to inspect specific moments, compare steps, and
identify trajectory inflection points). The navigation step is where the
programme trajectory view serves the user.

**Document change:** Revise user-journeys.md §Journey A Step 3 to add a
distinct navigation step after the advance sequence, documenting the specialist's
time-series review workflow and the information needs it produces.

---

### Rank 6 — Extend the active negotiation journey to include trajectory recall, not just alert recall

**Current premise:** user-journeys.md §Journey B Step 3 describes the active
negotiation task as: "She reads the MDA alert panel. This is the primary surface."
The journey assumes the specialist needs to recall a specific alert in 5 seconds.

**Why it is incomplete:** In an active negotiation, the specialist may need to
cite not just "this threshold was crossed at step 3" but "here is the trajectory
that produced that crossing — the indicator deteriorated continuously from step 1
through step 3 under these conditions." The trajectory view, if it exists, is
the instrument for this. The current active negotiation journey has no step for
citing the trajectory context of a threshold crossing — only the alert itself.

**The change:** user-journeys.md §Journey B Step 3 should extend the
information need to include the trajectory of the breaching indicator (not
just the alert text), and Journey B should acknowledge that the trajectory view
serves a recall function in active negotiation as well as a preparation function.

**Document change:** Revise user-journeys.md §Journey B Step 3 information
need paragraph to include trajectory context as a negotiation-room need,
not only an alert recall need.

---

## Cross-Document Summary of Changes Required

| Document | Section | Nature of change |
|---|---|---|
| north-star.md | §Primary Cognitive Task | Reframe from snapshot threshold detection to trajectory threshold detection |
| information-hierarchy.md | §Zone 1 | Promote trajectory view to Zone 1B; reassign radar chart to lower position |
| information-hierarchy.md | §COMPARE_VIEW | Conditional Zone 1 based on scenario structure (single vs. multi-entity) |
| information-hierarchy.md | §1B | Reframe radar chart as orientation instrument, not primary thesis visualization |
| user-journeys.md | §Journey A Step 3 | Split advance and navigate into distinct steps |
| user-journeys.md | §Journey B Step 3 | Extend active negotiation information need to trajectory context |

---

## What This Critique Does Not Recommend

This critique does not recommend removing or replacing the radar chart. The
multi-framework measurement principle is architecturally correct and the radar
chart is a legitimate instrument for it. Replacing it would be wrong.

This critique does not recommend removing the choropleth as the baseline view.
For multi-entity scenarios, geographic visualization is appropriate and
valuable. The issue is that the single-entity scenario is the canonical demo
and IMF negotiation use case, and the choropleth's spatial logic is not the
right primary instrument for that case.

This critique does not recommend replacing the MDA alert panel with the
trajectory view. The alert panel is a correct and well-designed output of
threshold analysis. The recommendation is that the trajectory view produces
the input to that analysis, not that it replaces the output.

---

## Relationship to the Engineering Lead's Observation

The Engineering Lead's observation — "functionality quilted together, radar
chart losing relevance" — is a coherence diagnosis. The tool has accumulated
visualization surfaces (choropleth, radar chart, MDA panel, framework tabs,
step counter) without establishing a dominant interaction idiom that unifies
them. Each surface was added for a correct reason. But they do not yet tell
a coherent visual story.

The dominant interaction idiom that would unify them is the programme timeline:
a shared step axis that is the through-line of every analytical surface. The
choropleth shows geographic state at a step. The radar chart shows the
multi-framework profile at a step. The MDA panel shows threshold crossings at
steps. The framework panels show indicator details at a step. If the shared
step axis is visible and navigable as the primary Zone 1 element, all other
surfaces become legible as views into the same underlying temporal data at
different levels of detail. The quilting problem resolves because all surfaces
hang on the same frame.

This is not a new feature. It is the conceptual integration of features that
already exist.
