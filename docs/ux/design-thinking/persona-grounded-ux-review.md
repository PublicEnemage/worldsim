# Persona-Grounded UX Review

> Date: 2026-05-21
> Scope: Re-evaluate the M8 Case B verdict and five governing premises against
>        the five named personas now that docs/ux/personas.md exists.
> Input documents: docs/ux/personas.md, docs/ux/design-thinking/m8-interaction-model-critique.md,
>        docs/ux/design-thinking/m8-critique-panel-synthesis.md,
>        docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md
> Issue: #387
>
> Three sequential activations. All three outputs recorded here.
> Engineering Lead review required before findings inform Issue #363.

---

## Activation 1 — UX Design Thinking Agent

*Re-evaluate the Case B verdict and five governing premises against the five
named personas. The critique reasoned from an abstract canonical user; this
review uses specific people with specific institutional contexts and historical
marquee cases as the test.*

---

### Q1 — Does Case B serve each persona's primary entry state and primary marquee case?

Work through each of the five personas individually, using their primary
marquee case as the acceptance test.

---

**Persona 1 — Lucas Ferreira (Programme Analyst)**

Lucas's primary entry states are Investigative and Preparatory. His primary
marquee case is the Greece 2010 multiplier sensitivity analysis: run three
scenario variants at fiscal multiplier 0.5, 1.0, and 2.0; produce differentiated
threshold-crossing maps; identify which income cohort crosses which floor at
which step.

Case B holds for Lucas without strain.

The trajectory view (the primary instrument under Case B) is precisely his
output format — he reads IMF fan charts and programme projection tables as
a professional. Multiple framework composite scores on a shared step axis,
with scenario bands showing multiplier sensitivity, is immediately legible
to him. The comparison view showing two or three simultaneous trajectories
is the comparison sensitivity analysis he performs manually today. Case B's
instrument cluster gives Lucas what no IMF tool currently gives him: the
human cost trajectory plotted alongside the financial trajectory, with MDA
floors showing where each multiplier value crosses into critical territory.

The one place Case B strains for Lucas: he needs confidence tiers displayed
per indicator, and he needs a methodology path accessible within one click of
any output. Case B's architecture (instruments primary, context navigable)
does not say anything about methodology accessibility — it prioritizes the
instrument cluster for reactive users like Eleni. For Lucas in Evaluative or
Investigative mode, the methodology path must also be a first-class element
of the primary viewport, not buried in Zone 3. Case B doesn't conflict with
this requirement, but it doesn't address it either.

**Verdict for Lucas:** Case B holds. No structural tension. One gap: the
architecture must specify that methodology path accessibility is a Zone 1 or
Zone 2 requirement, not only a Zone 3 deliberate-navigation feature.

---

**Persona 2 — Eleni Papadimitriou (Finance Ministry Negotiator)**

Eleni's primary entry states are Preparatory and Reactive. Her primary
marquee case is the February 2012 second memorandum: identify which specific
conditionality terms drive CRITICAL threshold crossings, build the counter-
proposal, enter the comparison view. In the room: retrieve a specific MDA
alert in under 90 seconds without navigation.

Case B was designed around Eleni. The first-principles document derives its
four inviolable Mode 3 requirements (R1–R4) from a user whose failure mode is
"primary instrument in a drawer is not a primary instrument." That failure mode
is Eleni's failure mode, stated verbatim in her persona.

Case B holds completely for Eleni.

Instruments always visible without navigation = direct architectural solution
to her active negotiation failure mode. The primary viewport as instrument
cluster = the tablet open in the negotiation room shows the relevant alert
without her needing to tap, open, or navigate. The step axis as shared frame =
she can cite "at step 2" and point to the same moment across the MDA panel,
the trajectory view, and the PMM widget simultaneously.

The one place Case B strains for Eleni: the comparison view. Eleni needs the
delta alert panel — which CRITICAL thresholds fire in the primary scenario
but not the counter-proposal — to be visible without constructing both
scenarios from scratch. The first-principles document was less thorough on
Mode 2 comparison than on Mode 3 active control. For Eleni in Preparatory
mode, the most time-pressure-sensitive moment is not Mode 3 steering but Mode 2
scenario comparison: she has 3 hours, she needs to build two scenarios, and the
comparison view must surface the delta without requiring her to navigate into
the entity drawer for each scenario separately.

**Verdict for Eleni:** Case B holds fully. One gap carried forward: Mode 2
comparison surface (the delta alert panel and fiscal equivalence demonstration)
needs to be specified with the same rigor as Mode 3 instrument placement.

---

**Persona 3 — Andreas Stefanidis (Political Advisor)**

Andreas's primary entry states are Reactive and Preparatory. His primary
marquee case is the Cyprus bail-in 48-hour window, March 2013: run Mode 1
Replay of Argentina 2001 and Iceland 2008; extract governance and social
legitimacy trajectories; build the political argument for the parliament vote.

Case B strains significantly for Andreas. Not because the architecture is
wrong, but because it was designed for a different cognitive task than his.

Case B says: instruments primary, context navigable. Andreas's instruments
are different from Eleni's. Eleni's primary instrument is the MDA alert panel:
severity, indicator, step, cohort — immediately citable. Andreas's primary
instrument is the historical precedent pattern: what happened to governance
indicators in Argentina when the deposit guarantee was breached? At what step
did the legitimacy cascade become irreversible? This is a Mode 1 comparative
narrative question, not a Mode 3 active control question.

The instrument cluster under Case B — trajectory view, MDA panel, PMM, four-
framework current position — serves Andreas partially:

- The trajectory view in Mode 1, showing governance composite score over the
  Argentina 2001 programme steps, is the right surface. It shows the
  legitimacy collapse.
- The MDA alert panel shows governance threshold crossings with step indices.
  This is the right output.

But Case B fails Andreas in three specific ways:

**Gap 1 — Step axis is not calendar-annotated by default.** Andreas needs
the step axis to read "December 2001 — corralito announced" not "Step 1." He
is building a political narrative for a cabinet that thinks in calendar dates
and political events, not simulation steps. The first-principles document's
Premise 3 (step axis as shared frame) is correct architecturally but assumes
the user can navigate from "step N" to "the event at step N." Andreas cannot.
He needs event annotation baked into the primary viewport, not accessible via
Zone 3 deliberate navigation.

**Gap 2 — The instrument cluster is analysis-first, not narrative-first.**
The trajectory view produces a composite score curve. Andreas needs this
translated into political language: "Social cohesion collapsed at Step 1
— within one week of the deposit freeze announcement, comparable to the 2001
Argentine corralito." That translation is not in the instrument. It is in the
Social Dynamics and Political Economist council consultation — but those are
agent consultations, not UX affordances. The Mode 1 instrument cluster needs
a narrative summary layer between the composite score curve and the political
brief Andreas must write.

**Gap 3 — Comparative Mode 1 is not the same as comparative Mode 2.** Andreas
needs to compare two historical cases (Argentina 2001 vs. Iceland 2008) on the
same step axis. This is a Mode 1 multi-entity comparison question: two countries,
two historical trajectories, one governance indicator, legible divergence visible
in the primary viewport. The Case B architecture handles Mode 2 scenario
comparison (same entity, two conditionality paths). It does not explicitly
address Mode 1 multi-case comparison (different entities, same governance
question). These are different analytical structures with different UX
requirements.

**Verdict for Andreas:** Case B's viewport architecture (instruments primary,
context navigable) serves his Reactive entry state. It does not serve his
Preparatory use case (cabinet brief construction) because: (a) step annotations
are required before the instrument cluster is legible to him; (b) narrative
translation from composite score to political language is absent; (c) Mode 1
multi-case comparison is architecturally underspecified. These are gaps
to address in Issue #363, not reasons to reject Case B.

---

**Persona 4 — Dr. Amara Diallo (Academic Researcher)**

Amara's primary entry states are Evaluative, Retrospective, and Investigative.
Her primary marquee case is the backtesting audit: run Greece 2010-2012 at
three multiplier values, download the divergence table, compare to Blanchard-
Leigh estimates.

Case B is neutral for Amara in a way that reveals a gap.

The Case B architecture is designed to serve users who need to act quickly on
instrument readings. Amara is not acting on an instrument reading — she is
inspecting the instrument. Her primary workflow is: read methodology documentation,
run simulation with specified parameters, download the backtesting divergence
table, compare to external reference. None of this is served or blocked by
instruments being primary in the viewport.

The architecture gap is this: for Amara, the methodology path (Zone 3 in the
current information hierarchy) should be a Zone 1 element — always accessible
without deliberate navigation — because her session begins with methodology
inspection, not instrument reading. The current hierarchy places methodology
documentation in Zone 3 ("deliberate navigation"), which is correct for Eleni
(who reads methodology before a session, not during) but wrong for Amara (who
reads methodology as the session's opening act).

Case B does not conflict with this requirement. It simply doesn't address it.
The five governing premises make no claim about where methodology documentation
sits in the zone hierarchy — they address instrument cluster placement, step
axis governance, mode-specific cognitive tasks, and control plane reservation.
A sixth premise is needed for Amara's entry state: **methodology documentation
path is always accessible within one interaction from any instrument output.**
This is not a Zone 3 requirement. It is a Zone 2 requirement that applies
universally when any instrument output is visible.

**Verdict for Amara:** Case B is neutral — neither serves nor obstructs her
primary workflow. The gap is a missing sixth premise about methodology
accessibility. The Evaluative and Retrospective entry states are architecturally
underaddressed in all existing UX documents.

---

**Persona 5 — Aicha Mbaye (Institutional Decision-Maker)**

Aicha's primary entry state is Demonstrative. Her primary marquee case is
the IMF Board demonstration using the Greece 2010-2015 six-step fixture: five
minutes, three screens, non-technical audience, leadership-level decision.

Case B partially serves Aicha, with one significant tension.

The viewport architecture is exactly right for Demonstrative entry state. The
instrument cluster on the primary viewport means the demonstrator does not have
to narrate "let me open this drawer to show you the finding" — the finding is
present. Case B's Premise 2 (instruments always visible without navigation) is
the single most important requirement for a successful demonstration: the
executive director cannot be left watching the demonstrator navigate the tool
while people are waiting.

The significant tension: Case B's instrument cluster is labeled in analyst
language. The trajectory view shows composite scores on a 0-1 axis. The MDA
panel shows "WARNING: poverty_headcount_pct - bottom_quintile — step 2."
Aicha's information format requirements are: traffic lights (red/amber/green
without a number), one-sentence findings, plain-language annotation on the
single most important chart. The instrument cluster under Case B is not
annotated this way by default.

This tension is real and structural. The same instrument cluster that serves
Eleni — who reads "poverty_headcount_pct — CRITICAL at step 2 — bottom
quintile" and immediately knows what to do — fails Aicha, who reads the same
text and needs a 30-second explanation. The instruments are correctly positioned
(Premise 1 and Premise 2 hold). Their language register is wrong for Demonstrative
entry state.

This implies a display mode for Demonstrative entry state — not a different
instrument architecture but an annotation layer that:
(1) relabels composite score curves with plain-language framework names and
    directional arrows (Human Development: ↓ since step 2);
(2) converts MDA alert text into one-sentence plain-language findings;
(3) suppresses secondary indicators in the alert panel to show only the
    highest-severity finding;
(4) optionally converts the trajectory view to a traffic light summary for
    the current step position.

This is not a Mode 3 feature. It is a Demonstrative entry state feature —
a presentation mode that overlays plain-language annotation on the
Case B instrument cluster without changing its underlying architecture.

**Verdict for Aicha:** Case B's architecture (viewport and instrument placement)
is right for Demonstrative entry state. The labeling register is wrong.
A presentation layer (annotation overlay for Demonstrative mode) is needed
before the Case B design serves Aicha. This is a specification gap for
Issue #363, not a challenge to Case B.

---

### Q2 — Are any of the five governing premises optimized for one persona at the cost of another?

Evaluating each premise against the full persona set.

---

**Premise 1 — Primary viewport is the instrument cluster; context is navigable**

Serves all five personas. Lucas (Preparatory), Eleni (Reactive/Preparatory),
and Aicha (Demonstrative) all need the instrument cluster on the primary
viewport. Andreas (Reactive — crisis window) needs governance and social
dynamics instruments visible immediately. Amara (Evaluative) is not served
by this premise but is not harmed by it.

No tension. No persona is worse off when instruments are primary.

**Verdict:** Holds for all five. No revision needed.

---

**Premise 2 — Instruments are always visible without drawer, without scroll**

Serves Personas 1, 2, 3, and 5. All four need primary instruments accessible
without navigation in their most demanding entry states.

Strains for Persona 4 (Amara): in Evaluative entry state, the "instrument"
Amara needs always visible is the methodology documentation path, not the
simulation output. For Amara, Premise 2 says "the trajectory view is always
visible" when what she needs is "the ADR governing this instrument is always
accessible within one click of this instrument." This is not a contradiction —
Premise 2 doesn't obstruct her — but the premise optimizes for Eleni's
Reactive entry state while leaving Amara's Evaluative entry state with no
equivalent guarantee.

**Verdict:** Holds for four of five personas. Amara requires a companion
premise about methodology path accessibility. Amara is not harmed by Premise 2,
but she is not served by it. The gap should be named and addressed.

---

**Premise 3 — Step axis is the shared frame for all instruments**

Serves Personas 1 and 2. Lucas and Eleni both think natively in step-indexed
programme time — they work with IMF programme steps, Article IV projection
years, and conditionality timelines. "Step 2 = 2012" is their vocabulary.

Strains for Persona 3 (Andreas): Andreas thinks in calendar dates, political
events, and election horizons. "Step 1" is not political language. The step
axis is architecturally correct, but without mandatory calendar annotation and
event labeling on every instrument that shows the step axis, it is illegible
to Andreas. The step axis does not become legible just because it is shared
— it becomes legible when it is annotated with the political calendar.

Strains for Persona 5 (Aicha): "Step 3" is not legible to a decision-maker
in a 5-minute demonstration unless it is annotated "2012 — second
memorandum." The shared step axis is correct. The annotation is currently
missing.

**This is the most significant persona-level tension in the five premises.**
Premise 3 is correct as an architectural invariant. It is underspecified as a
display requirement. The premise must be extended: the step axis annotation
is not optional — every instrument displaying the step axis must also display
the corresponding calendar date and a one-line event label for significant steps.
This is a label requirement, not an architecture change. But it is the
difference between Premise 3 serving four personas and serving two.

**Verdict:** Holds architecturally for all five. **Requires an extension**:
step axis annotation (calendar date + event label for significant steps) is
mandatory on all instruments that display the step axis. Without this extension,
Premise 3 optimizes for Personas 1 and 2 while leaving Personas 3 and 5
unable to orient themselves.

---

**Premise 4 — Each mode has its own primary cognitive task; the architecture must not privilege any one mode at the cost of making another impossible**

Holds for all five personas in principle. The premise creates the conceptual
space for Mode 1 to have a different cognitive task from Mode 3 — which is
the correct claim.

But the premise does not go far enough. The persona document reveals that
within Mode 1, different personas have different primary cognitive tasks:

- Eleni in Mode 1: trajectory reconstruction — at what step did the threshold
  cross and what produced it?
- Andreas in Mode 1: historical pattern recognition — what does the comparable
  case show about political survivability?
- Amara in Mode 1: backtesting validation — how far does the predicted trajectory
  diverge from the observed trajectory?
- Aicha in Mode 1 (Demonstrative): legible narration of a completed historical
  case without technical interpretation.

These are four different Mode 1 tasks. The first-principles document defined
Mode 1's primary cognitive task as "trajectory reconstruction" — which is
correct for Eleni but incomplete as a statement of what Mode 1 must serve.

**Verdict:** Holds architecturally. Requires extension: Premise 4 should
acknowledge that within each mode, personas have different primary cognitive
tasks, and the Mode 1 instrument cluster must be designed to support at minimum
Eleni's (trajectory reconstruction) and Andreas's (historical pattern recognition)
tasks without requiring them to share the same cognitive path.

---

**Premise 5 — Control plane zone reserved before it is built**

Neutral for Personas 3, 4, and 5. None of them are Mode 3 users.
Serves Personas 1 and 2. Does not harm any persona.

**Verdict:** Holds for all five. No revision needed.

---

### Q3 — Does the instrument cluster serve all five personas, or primarily one? What does that imply for Mode 1 and Mode 2 instrument design?

The instrument cluster as specified in the first-principles document was
derived from Mode 3 requirements. The four primary flight instruments (trajectory
view, PMM, MDA alert panel, four-framework current position) are all designed
from the Mode 3 question: "what does a pilot need always visible during active
control?" The answer is correct for Mode 3. The question imposes a bias.

The persona review shows the instrument cluster serves three of five personas
well, one partially, and one not directly:

- Lucas (Persona 1): well-served. The trajectory view with scenario bands is
  his primary output format.
- Eleni (Persona 2): well-served. The instrument cluster was designed around
  her failure mode.
- Andreas (Persona 3): partially served. The instruments are in the right
  location. Their content (composite scores, severity labels, step indices)
  requires annotation and narrative translation before they are useful to him.
- Amara (Persona 4): not directly served. The instrument cluster is not her
  primary workflow surface. She needs the methodology layer, not the
  instrument layer, to be her primary viewport.
- Aicha (Persona 5): partially served. The viewport architecture is correct.
  The language register is wrong.

**What this implies for Mode 1 instrument design:**

Mode 1 (Replay) is the primary mode for Personas 3, 4, and the Retrospective
entry state of Persona 1. The first-principles document addressed Mode 1 the
least thoroughly — it derived the instrument cluster from Mode 3 and assumed
Mode 1 would be served by the same instruments in a read-only configuration.

The persona review shows this assumption is partially wrong:

1. **Andreas in Mode 1 needs event annotation as a first-class instrument
   feature, not a Zone 3 detail.** The step counter showing "Step 1 / 6" is
   not sufficient. Mode 1's step axis must display the historical calendar event
   at each step by default — not as an opt-in label but as a mandatory
   component of the step axis display in Mode 1.

2. **Amara in Mode 1 needs the backtesting divergence view as a Zone 1 or Zone
   2 instrument, not a Zone 3 data export.** The divergence table (predicted
   vs. observed, step by step, with confidence tiers) is Amara's primary output
   in Mode 1 Retrospective entry state. Under the current hierarchy, this output
   is buried. For Amara, the backtesting divergence view must be promoted to
   Zone 2 at minimum — accessible in one interaction from any Mode 1 instrument
   reading.

3. **Mode 1 multi-case comparison** (Andreas comparing Argentina 2001 and
   Iceland 2008 governance trajectories on the same step axis) is architecturally
   unspecified. Mode 2 comparison is single-entity, two-scenario. Mode 1 multi-
   case comparison is multi-entity, single scenario, comparing historical
   trajectories. This is a distinct analytical structure that requires a distinct
   comparison surface specification. Issue #363 should address it.

**What this implies for Mode 2 instrument design:**

Mode 2 (Simulation) is the primary mode for Personas 1 and 2 in Preparatory
entry state. The first-principles document addressed the Mode 2 comparison
surface (delta alert panel, fiscal equivalence gap) but did not specify the
Mode 2 scenario construction workflow.

For Lucas in Mode 2: the scenario configuration surface must expose the fiscal
multiplier as a top-level configurable parameter — not buried in a settings
panel. He needs to run three scenarios with one parameter changed between them.
The workflow must support this without rebuilding the scenario from scratch
each time.

For Eleni in Mode 2: the scenario configuration must be completable in under
5 minutes for a practitioner who is not a simulation expert. The conditionality
terms she is modeling (minimum wage cut, pension reduction, privatization
timeline) must be representable as ControlInput parameters without requiring
her to understand the underlying simulation engine.

Neither Lucas's nor Eleni's Mode 2 workflow is explicitly specified in the
first-principles document. Issue #363 must address the Mode 2 scenario
construction workflow alongside the Mode 2 comparison surface.

---

### Summary of Activation 1 Findings

The Case B verdict holds for all five personas at the architectural level.
It requires four specification extensions that the first-principles document
did not address because it reasoned from Mode 3 alone:

1. **Methodology path as Zone 2 mandatory** (serves Persona 4 — Amara in
   Evaluative/Retrospective entry state). Methodology documentation path
   accessible within one interaction of any instrument output.

2. **Step axis annotation as mandatory on all instruments** (serves Personas
   3 and 5 — Andreas and Aicha). Calendar date + event label for significant
   steps is not optional in Mode 1 or Mode 2; it is the precondition for the
   step axis being legible to non-analyst personas.

3. **Presentation layer for Demonstrative entry state** (serves Persona 5 —
   Aicha). Plain-language annotation overlay on the instrument cluster for
   Demonstrative entry state; does not change the underlying instrument
   architecture.

4. **Mode 1 multi-case comparison and backtesting divergence view** (serves
   Personas 3 and 4 — Andreas and Amara). Distinct analytical structure from
   Mode 2 comparison; requires separate specification.

The single most significant tension found: **Premise 3 (step axis as shared
frame) optimizes for Personas 1 and 2 while leaving Personas 3 and 5 unable
to orient themselves without step annotation.** This is not a rejection of
Premise 3 — it is a specification gap that, if left unaddressed, will produce
a Mode 1 instrument cluster that is legible to Lucas and Eleni and opaque to
Andreas and Aicha.

---

## Activation 2 — Development Economist

*Evaluating the proposed instrument cluster from the perspective of Persona 2
(Eleni Papadimitriou) in her February 2012 marquee case.*

---

### What is Eleni's burning question at session entry?

It is not "is there a threshold crossing?" She knows there probably is — she
has read the conditionality document. It is not "how severe is the overall
human development trajectory?" That is Lucas's framing.

Eleni's burning question is specific: **"Which term in this package is the one
I can actually challenge, and what does the alternative look like?"**

The February 2012 conditionality package contains multiple terms simultaneously.
Her strategic question is not about the aggregate human cost — it is about
which specific lever, if removed or modified, produces the largest reduction
in threshold crossing severity without losing fiscal credibility. She is
looking for the negotiating surface, not the economic headline.

This distinction matters for the instrument cluster design. The trajectory view
shows the aggregate financial and human development composite scores over six
steps. The MDA alert panel shows which indicators crossed which floors at
which steps. Neither of these directly answers "which conditionality term
drove this crossing?" — both tell her what happened, not what caused it.

To answer her burning question, she needs the comparison view: the primary
scenario (full Troika package) and her counter-proposal (same fiscal target,
modified instrument mix) on the same trajectory view, with the delta alert
panel showing which CRITICAL crossings are present in one and absent in the
other. The comparison view is the instrument that surfaces the negotiating
surface.

This is the first design implication from Eleni's marquee case: **the comparison
view is not a secondary instrument for Eleni in Preparatory mode — it is her
primary workflow destination.** The trajectory view with a single scenario is
her orientation surface. The comparison view is her evidence surface.

---

### Does the proposed instrument cluster surface her burning question within 60 seconds?

No. Not in her most demanding moment (Preparatory — 3 hours to brief the
minister, conditionality document just arrived).

The proposed instrument cluster in a single-scenario view shows:
1. Trajectory view: composite scores over the 6-step programme horizon
2. MDA alert panel: which indicators crossed floors, at which step, for which
   cohort
3. PMM widget: remaining degrees of freedom
4. Four-framework current position: composite scores at current step

This surfaces the wrong question first. The instrument cluster answers:
"What is happening to this country's trajectory under these conditions?"
Eleni's burning question is: "Which condition is doing this to the trajectory,
and what is the alternative?" These are not the same.

Within 60 seconds of opening the tool with a completed comparison scenario,
the instrument cluster does surface her answer — because the delta alert panel
shows which crossings fire in primary but not counter-proposal. But 60 seconds
assumes the comparison scenario is already built and loaded. If she is entering
in Preparatory state with a new conditionality document, she needs to build two
scenarios first. The scenario construction workflow is not part of the 60-second
clock — it is the preparation work that must be completable before the 60-second
clock starts.

**The UX implication:** The instrument cluster design is correct for the
active negotiation moment (Reactive entry state). It partially serves the
preparation moment (Preparatory entry state) but does not make the scenario
construction workflow that precedes it frictionless. Issue #363 must address
the preparation workflow, not only the retrieval workflow.

---

### What would frustrate Eleni specifically?

Three specific friction points, in order of severity:

**Friction 1 — The comparison view is not the default destination after
scenario completion.** After running two scenarios (primary and counter-
proposal), Eleni expects the comparison view to be the immediate next surface.
If completing a second scenario drops her back to a single-scenario instrument
cluster rather than opening the comparison view automatically, she has to
navigate to the comparison. In a 3-hour preparation window, this navigation
is tolerable. In an active negotiation, it is not. The comparison view must
be accessible in one action from any state in which two scenarios are complete.

**Friction 2 — The delta alert panel shows binary fire/no-fire without
severity trajectory.** "Poverty headcount CRITICAL in primary, absent in
counter-proposal" is a good signal. What she also needs: "The poverty headcount
crossing in the primary scenario is at a margin of X percentage points below
the MDA floor; in the counter-proposal, the margin does not reach the floor."
The depth of the crossing matters for the argument — a near-miss on a
CRITICAL threshold in the counter-proposal is a weaker argument than a
scenario that stays clearly above the floor. Binary alert delta understates
the evidence.

**Friction 3 — Confidence tier labels in the primary display without
translation.** If the MDA alert panel shows "CRITICAL — poverty_headcount_pct
— Tier 2 (REPORTED)" alongside "WARNING — governance_composite — Tier 4
(SYNTHETIC_MODEL)," Eleni cannot immediately distinguish which alert she can
defend under Troika scrutiny (Tier 2 = defensible) from which she cannot
(Tier 4 = exploratory, will be challenged). The confidence tier must be
translated into a negotiation-defensibility label, not displayed as a raw
tier number. Suggested: "High confidence — cite directly" (Tiers 1-2),
"Moderate confidence — cite with caveat" (Tier 3), "Exploratory — do not
cite" (Tiers 4-5). This translation lives in the UI, not in the data model.

---

### What does a successful 20-minute session look like for Eleni?

She enters in Preparatory state with the Troika conditionality document open
on her desk. She has previously configured the Greece entity and knows the
scenario configuration workflow.

Minutes 0-3: She opens WorldSim. The landing state shows her two previously
saved scenarios: "Troika_Feb2012_Full" and a baseline. She selects
"Troika_Feb2012_Full," confirms it is complete at step 6. She navigates to
scenario configuration, duplicates the scenario, modifies it: postpones minimum
wage cut by 12 months, protects basic pension floor at current level. She
names it "Counter_Feb2012_ModA." Runs to step 6.

Minutes 3-12: She selects both scenarios and enters the comparison view.
The delta alert panel is Zone 1A: "CRITICAL — poverty_headcount — bottom
quintile — fires at step 2 in primary; absent in counter-proposal."
"WARNING — health_system_capacity — step 3 — present in primary; present
in counter-proposal at step 4." She reads the fiscal equivalence line:
"Counter-proposal achieves same 5-year fiscal consolidation target as primary
at 99.3% equivalence. Primary surplus target met 1 quarter later." She now
has the core of her argument.

Minutes 12-20: She navigates to the trajectory divergence view. She can see
the human development composite score in the primary scenario descending
through the MDA floor at step 2 and remaining below it through step 6. In
the counter-proposal, the score descends toward the floor but does not cross.
The slope of descent is annotated: the slope between steps 1-2 in the primary
is steeper than in the counter-proposal. She screenshots this view. She opens
the cohort breakdown for the poverty_headcount indicator: bottom quintile, age
25-65, primarily formal sector employees. She has the cohort for her argument.

Exit: She carries out: one delta alert panel screenshot, one trajectory
divergence view showing the floor crossing avoided, the cohort identification
(bottom quintile, formal sector), the fiscal equivalence figure (99.3%),
and the specific modification that drove the change (minimum wage cut
postponed). This is her evidence. The argument is: "This specific term, applied
this way, crosses this threshold for this cohort at step 2. A 12-month
postponement of the cut avoids the crossing entirely, at 99.3% fiscal
equivalence."

This is the acceptance test for Eleni's marquee case: can she construct this
argument and carry this evidence in under 20 minutes?

---

### Implication for Issue #363 from Activation 2

The Mode 2 scenario construction workflow is the preparation infrastructure
without which the instrument cluster cannot serve Eleni's Preparatory entry
state. Issue #363 must specify:

1. Scenario duplication with single-parameter modification (minimum viable
   preparation workflow for generating a counter-proposal from the primary
   scenario)
2. Automatic transition to comparison view after a second scenario completes
3. Delta alert panel with severity margin, not binary fire/no-fire
4. Fiscal equivalence demonstration in the comparison view header
5. Confidence tier translation to negotiation-defensibility labels

These are five design requirements for Mode 2 preparation that the
first-principles document did not specify because it derived the instrument
cluster from Mode 3. Mode 2 preparation is Eleni's most time-sensitive use
case; it must be specified with the same rigor as Mode 3 active control.

---

## Activation 3 — Political Economist

*Evaluating the instrument design from the perspective of Persona 3 (Andreas
Stefanidis, the Political Advisor) in Preparatory entry state.*

---

### What does Andreas need from WorldSim?

Andreas has a cabinet meeting tomorrow morning. He needs to brief the Prime
Minister on whether to accept the current conditionality terms, and he needs
to be able to answer a journalist who will ask: "How many people will actually
suffer under this programme, and did the government have any alternative?"

These are not analytical questions. They are political questions that require
an analytical foundation. Andreas cannot answer them from the instrument
cluster directly. He needs the instrument cluster to produce ingredients that
he can assemble into a political argument. The assembly is his job — the
ingredients are WorldSim's job.

What Andreas specifically needs:

**1. Historical precedent pattern, not forward scenario.** His most powerful
argument is not "the simulation predicts this will happen" — prediction claims
are immediately challenged in political rooms. His most powerful argument is
"this has happened before, and this is what happened then." Mode 1 (Replay) of
Argentina 2001 and Iceland 2008 is his primary analytical instrument. He does
not need Mode 2 or Mode 3 for his marquee case. He needs Mode 1 to surface a
governance and social legitimacy trajectory in plain language.

**2. A narrative-ready governance trajectory.** Not "governance composite score:
0.43 at step 2, declining to 0.31 by step 4." Instead: "Political legitimacy
collapsed within 6 weeks of the deposit freeze announcement, comparable to
the Argentine corralito. Public trust in the banking system fell to its lowest
recorded level. Three governments fell in succession." This is what the Social
Dynamics and Governance indicators are meant to surface — but they surface
them as composite scores and MDA alerts, not as narrative summaries.

**3. Comparable case contrast.** Andreas needs the Iceland comparison not as
a second Mode 1 scenario run separately, but as a comparative answer to a
single question: "Why did Iceland survive what Argentina could not?" The
instrument cluster shows two Mode 1 trajectories. Andreas needs the
comparative narrative to be visible without him constructing it from two
separate trajectory views.

**4. Political survivability signal, not economic signal.** "The programme
is expected to reduce GDP by 25% over 5 years" is an economic signal. Andreas
can use it, but he needs it translated: "A 25% GDP contraction over 5 years
has no democratic precedent in the Eurozone. No government has survived
implementing such an adjustment and been re-elected." The translation from
economic trajectory to political survivability is the output Andreas is
looking for. WorldSim does not currently produce it. The Political Economist
DIC agent can narrate it in a consultation — but it is not a UX affordance
in the instrument cluster.

---

### Is there a path from the instrument cluster to the narrative Andreas needs?

Partially. The path exists but requires manual cognitive steps that Andreas
cannot reliably perform.

The existing path: Run Mode 1 (Argentina 2001). Open governance indicator in
Zone 2. Read social cohesion composite score trajectory. Run Mode 1 (Iceland
2008). Compare trajectories. Notice governance score diverges at step 2.
Infer that Iceland's decision to honor the deposit guarantee correlates with
a different trajectory. Translate composite score divergence into political
narrative.

The missing link is the inference step — from "composite score diverges at
step 2" to "this is because Iceland honored the deposit guarantee and Argentina
did not." This inference requires domain knowledge that Andreas has from
political experience and that WorldSim should surface as an event annotation.
Without it, Andreas sees a diverging governance line and must independently
construct the explanation. He can do this — he is a skilled political analyst.
But he should not have to. The historical event annotation that is mandatory
for the step axis (per Activation 1's finding) is exactly the bridge from
composite score to political narrative that Andreas needs. At step 2 of the
Argentina replay: "December 2001 — corralito announced; mass protests begin."
That annotation is the link between the trajectory and the political story.

**The path exists, but it requires two design additions:**
1. Mandatory event annotation on the step axis in Mode 1 (as specified in
   Activation 1)
2. A "narrative context" panel accessible from Mode 1 historical replay —
   a Zone 2 element that surfaces the comparable case's political context
   in 2-3 sentences, sourced from the case fixture's metadata

Neither of these is architecturally novel. The step annotation is a data field.
The narrative context panel is a structured text component. Both require
implementation. Neither requires a new module.

---

### What format does Andreas carry into the cabinet room?

Andreas will construct a one-page political brief. He will not print a
trajectory view chart and hand it to the Prime Minister. He will not read
the MDA alert panel in the cabinet room. He will take the following from
WorldSim:

**Ingredient 1 — The historical precedent statement.** "When Argentina
froze deposits in December 2001, their governance and social cohesion
indicators collapsed within 4 steps (4 weeks). Three governments fell.
When Iceland honored the deposit guarantee for domestic depositors in 2008,
governance declined but recovered within 8 steps. The distinguishing factor:
deposit guarantee integrity."

WorldSim provides the trajectory data that underlies this statement. Andreas
constructs the statement. The tool must surface the trajectory and the event
annotation that connects the data to the political story.

**Ingredient 2 — The political survivability signal.** "Under the proposed
Cypriot deposit levy, the governance trajectory at step 1 mirrors Argentina
2001 within a confidence band of ±15%. The governance indicator crosses WARNING
at step 1 and CRITICAL at step 3. No comparable Eurozone case has recovered
a governance score from CRITICAL within a programme horizon."

WorldSim provides the trajectory, the MDA timing, and the comparable case
comparison. Andreas assembles the survivability claim.

**Ingredient 3 — The alternative outcome.** "Under the modified proposal
(honoring insured deposit guarantee, haircut only on deposits above €100,000),
the governance trajectory at step 1 mirrors Iceland 2008. The governance
indicator declines but does not cross WARNING."

WorldSim provides the counter-scenario trajectory. Andreas delivers the
political conclusion.

---

### Does Case B serve Andreas, frustrate him, or is he simply not the Mode 3 user?

Andreas is not the Mode 3 user. He will never apply a fiscal policy input
and watch the trajectory respond in real time. The Active Control mode was
designed for Eleni. Andreas does not belong there.

Case B does not frustrate Andreas — the architecture of instruments visible
in the primary viewport is correct for his Reactive entry state (48-hour
crisis window). When he enters the tool in crisis mode, he needs the governance
trajectory visible immediately without navigating a drawer. Case B gives him
that.

But Case B does not serve his Preparatory entry state as it currently stands.
The Preparatory workflow for Andreas is: enter Mode 1, select the comparable
historical case, read the governance and social legitimacy trajectory, extract
the political narrative ingredients. This workflow requires:

(a) Mode 1 to be a first-class entry point from the landing screen, not
    a configuration of the same scenario engine that produces Mode 2 and 3
    (Mode 1 should feel like selecting a historical case, not like configuring
    a simulation);

(b) Event annotations on the step axis as mandatory Mode 1 elements;

(c) A narrative context panel as Zone 2 in Mode 1, surfacing the case's
    political context in structured text.

None of these are contradicted by Case B. But none of them are specified by
Case B either. Case B specifies the instrument cluster architecture; it does
not specify the Mode 1 experience. For Andreas, the Mode 1 experience is
his primary use case. Issue #363 must specify it.

---

### What does this imply for how WorldSim serves the Preparatory entry state?

The Preparatory entry state has three distinct workflow structures across the
five personas:

- **Lucas (Preparatory):** Configure scenario parameters, run multiplier
  sensitivity analysis, extract threshold-crossing data for staff report.
  Primary surface: Mode 2 scenario configuration + comparison view.
  Workflow is parameter manipulation and output extraction.

- **Eleni (Preparatory):** Model conditionality package, build counter-
  proposal, enter comparison view, identify delta alert panel output.
  Primary surface: Mode 2 scenario duplication + comparison.
  Workflow is evidence construction under time pressure.

- **Andreas (Preparatory):** Select comparable historical case, extract
  governance and social legitimacy narrative ingredients, construct political
  brief. Primary surface: Mode 1 historical replay + narrative context panel.
  Workflow is pattern recognition and narrative assembly.

These three Preparatory workflows share an entry state but have different
primary surfaces and different cognitive tasks. The UX architecture must
not collapse them into a single "preparation mode" — they require Mode 1 and
Mode 2 to be distinct experiences with distinct default instrument states.

**The architectural implication for Issue #363:** When the user enters in
Preparatory state, the landing screen should surface the question "what are
you preparing for?" — and the answer determines which mode the tool opens in.
Mode 1 (historical case) is the correct default for Andreas; Mode 2 (scenario
construction) is the correct default for Lucas and Eleni. The Preparatory
entry state cannot have a single default mode — it must branch on the
user's preparatory task.

---

### Summary of Activation 3 Findings

Andreas is not served by the current or proposed instrument cluster in his
Preparatory entry state — not because the instruments are wrong but because
the Mode 1 experience is underspecified. Three design requirements for Mode 1
that Issue #363 must address:

1. **Mode 1 as a distinct entry path**, not a configuration of the scenario
   engine. Historical case selection should feel like browsing a library, not
   configuring a simulation.

2. **Event annotation as mandatory Mode 1 step axis element.** Without
   calendar dates and political event labels on each step, the Mode 1 trajectory
   view is opaque to Andreas.

3. **Narrative context panel as Zone 2 in Mode 1.** Structured plain-language
   context for the historical case, surfacing the political conditions at each
   significant step. This is the ingredient that converts trajectory data into
   narrative material Andreas can use.

The Case B verdict is correct for Andreas's Reactive entry state. For his
Preparatory entry state, the Mode 1 experience must be specified to serve
pattern recognition and narrative assembly, not only trajectory reconstruction.
These are different cognitive tasks that require different instrument configurations
within the same Mode 1 framework.

---

## Cross-Activation Synthesis

The single most significant finding from all three activations:

**The first-principles document derived the five governing premises and the
instrument cluster architecture from Mode 3 requirements. Mode 3's primary
user is Eleni (Persona 2). The premises hold for all five personas at the
architectural level, but they require four specification extensions before
they serve the full persona set.**

The most consequential extension — the one that most changes how Issue #363
should be approached — is the **step axis annotation requirement** (Activation 1,
Q2, Premise 3). If the step axis is not annotated with calendar dates and
event labels in Mode 1, the instrument cluster is not legible to Andreas
(who needs the political calendar to orient himself) or Aicha (who needs the
historical context to follow the demonstration). Eleni and Lucas do not need
the annotation because they already know what happened at each step. Andreas
and Aicha do not know, and they cannot interpret a step axis that shows only
"Step 1 / 6."

This means **Issue #363's Gap 1 walkthrough for Persona 2 should be
accompanied by a parallel specification for the Mode 1 instrument cluster**
— one that addresses Andreas's pattern recognition task and Aicha's
demonstration legibility requirement. The Case B verdict holds. What it
needs is a Mode 1 specification that serves the full persona set, not only
the one persona whose cognitive task was the source of the original critique.
