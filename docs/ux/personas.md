# WorldSim User Personas

> Owned by the UX Designer Agent and Council Orchestrator.
> Every UX decision, Frontend Architect brief, and stakeholder
> demonstration must be evaluated against the personas and marquee
> cases in this document before it is accepted as complete.
>
> This is the most important design document produced since CLAUDE.md.
> Do not modify without Engineering Lead sign-off.
>
> First draft completed: 2026-05-20 (Issue #362).
> Engineering Lead review required before canonical status.

---

## Section 1 — Five Formal Personas

---

### Persona 1 — The Programme Analyst

**Identity**

Lucas Ferreira. Country Economist, IMF Fiscal Affairs Department, seconded
to a European country desk. 34 years old. PhD in economics from a European
university; 9 years at the IMF, the last 4 as a country desk economist.
Worked on Greece, Portugal, and Angola programmes. Currently building the
Article IV consultation for a mid-size European economy facing early-stage
fiscal stress. He is not a WorldSim skeptic — he is cautious. He has spent
his career defending quantitative outputs in rooms that look for holes.

**Domain Expertise Profile**

Deep: macroeconomic modeling, debt sustainability analysis, fiscal multiplier
calibration, cross-country regression analysis, IMF-style programme design.
Edge: distributional and cohort-level human impact below the macro aggregate;
ecological constraints; political feasibility modeling. Lucas knows that
poverty rates increase when GDP falls, but his current tools do not show him
which income quintile crosses a critical threshold at which fiscal multiplier
value, at which step. That gap is the reason he is interested in WorldSim.

**Mental Model at Session Entry**

"A good analytical tool shows me what my current model is missing, in a form
I can defend." Lucas expects to disagree with specific model assumptions and
wants to be able to inspect and challenge them. He is not looking for a
black box with better output — he is looking for a transparent framework
that surfaces distributional and human cost signals his current tools do not
produce. He trusts outputs that carry explicit confidence tiers. He distrusts
outputs that carry no uncertainty quantification.

**Entry State and Frame of Mind**

Primary states: **Investigative** (exploring the tool's methodology and
coverage before committing analytical time) and **Preparatory** (building
the human cost evidence base before programme design lock-in).

Most demanding state: Preparatory. When Lucas is two weeks from a programme
design deadline, he needs specific outputs — specific indicator threshold
crossings at specific multiplier sensitivities — that he can include in
his staff report. Time is constrained; the output must be citable and
reproducible.

Least demanding state: Retrospective. Running Greece 2010-2015 against
the tool to validate calibration. He has time, the outcome is known, and
the exercise is about building trust.

**Primary Task**

Identify the human cost threshold crossings that are sensitive to fiscal
multiplier assumptions before programme design lock-in. Specifically: at
which multiplier value do human development indicators begin crossing MDA
floors? Which cohorts bear the earliest and most severe impact? Does the
proposed conditionality package produce avoidable threshold crossings at
multiplier values within the range of peer-reviewed literature?

**Trust Threshold**

Lucas will not cite an output in a staff report until three conditions are
met: (1) the methodology is documented and accessible from within the tool;
(2) the confidence tier for every cited indicator is explicitly displayed;
(3) he can reproduce the output from the same inputs. A single opaque
calculation breaks trust irreparably. The tool must also be defensible under
IMF peer review — methodological documentation must be citable.

**Preferred Information Format**

Numerical tables with confidence intervals; trajectory charts with scenario
bands; comparative output between multiplier-sensitivity scenarios. He reads
charts for orientation and tables for precision. He is comfortable with
statistical notation. He dislikes narrative explanations in the primary
display — they belong in methodology documentation, not the instrument cluster.

**Failure Mode**

Lucas closes the tool and never returns if: (1) it produces results that
diverge significantly from established consensus without a transparent
explanation of why; (2) confidence tiers are absent or aggregated to a
session level rather than displayed per indicator; (3) the methodology
documentation is inaccessible or incomplete. He will not defend opaque
outputs in front of an IMF review board.

---

### Persona 2 — The Finance Ministry Negotiator

**Identity**

Eleni Papadimitriou. Deputy Director of Debt Management, Hellenic Ministry
of Finance. 47 years old. Economics and law degree from a Greek university;
20 years in the Greek public sector, the last 8 in debt management. She
sat across from Troika negotiators in 2012 and 2015. She knows what it
feels like to need a specific number in under 90 seconds and not have it.
She uses the tool in two modes: desk preparation the night before, and
tablet retrieval in the room.

**Domain Expertise Profile**

Deep: fiscal policy and budget management, sovereign debt markets,
negotiation dynamics, programme conditionality design, political constraints
on policy implementation. Edge: econometric modeling methods; confidence
tier interpretation; ecological or governance framework details. Eleni is
not a modeler — she is a practitioner. She knows debt sustainability
arithmetic better than most PhD economists. She does not know, and does not
need to know, how the simulation engine propagates events.

**Mental Model at Session Entry**

"A good analytical tool gives me an argument I can make in the next 5 minutes."
Eleni is not exploring. She has a question that arrived from outside — from
a draft conditionality package, from a press release, from a ministry briefing.
The tool must produce the answer to that specific question with enough
specificity to be citable and enough confidence to survive scrutiny. She is
not evaluating the tool's methodology; she is using it to build a position.

**Entry State and Frame of Mind**

Primary states: **Preparatory** (desk work, evening before a session) and
**Reactive** (morning of, or in the room itself).

Most demanding state: Reactive in the active negotiation room. The tablet
is open. People are talking. The clock is running. She needs to navigate to
a specific threshold crossing — indicator name, step index, cohort — in
under 90 seconds. Any friction (loading states, navigation requirements,
drawer opening) is a failure.

Second-most demanding: Preparatory when the conditionality document just
arrived. She has 3 hours before she needs to brief the minister. She must
identify which terms cross which thresholds, build the counter-proposal,
and structure the argument. This is Journey A from user-journeys.md.

**Primary Task**

In the room: retrieve a specific threshold crossing (indicator, step, cohort,
severity) that can be cited as evidence against a specific conditionality
term. Before the room: identify which conditionality terms drive threshold
crossings, build the counter-scenario, confirm the counter-proposal reduces
or delays crossing severity.

**Trust Threshold**

Two conditions: (1) the confidence tier of the cited indicator must be visible
and defensible under Troika scrutiny — she will be asked "how do you know
this?" and "is that from a pre-calibration model?" She needs an honest answer,
not a deflection; (2) the output must be specific enough to cite — "poverty
headcount crosses critical threshold at step 2 under proposed terms" is
citable. "Human development outcomes deteriorate" is not. The IA1_CANONICAL_PHRASE
about pre-calibration epistemic bands must be framed in a way she can use
proactively rather than defensively.

**Preferred Information Format**

Alerts. Named indicators. Specific cohort data. Step-level precision.
Short sentences. No jargon in the primary display. The MDA alert panel is
her primary surface — severity, indicator name, step index, cohort.
Everything else is secondary context. She does not read methodology notes
during a session; she reads them when building trust before a session.

**Failure Mode**

Eleni closes the tool permanently if: (1) the primary instrument requires
navigation to access during active negotiation — a primary instrument in a
drawer is not a primary instrument; (2) the output takes more than 90 seconds
to produce under active negotiation conditions; (3) the tool cannot tell her
which specific conditionality term drove the threshold crossing (generic
deterioration signals do not support specific challenges).

---

### Persona 3 — The Political Advisor

**Identity**

Andreas Stefanidis. Senior Policy Advisor to a Finance Minister. 43 years
old. Political science degree; 8 years as a political journalist; 6 years
in senior advisory roles. No formal economics training. Deep intuition for
political narrative, social legitimacy, and the 18-month horizon in which
political decisions either survive or collapse. He is the person in the room
who translates "the model shows a 3.2% GDP contraction" into "we will lose
the next election if we sign this."

**Domain Expertise Profile**

Deep: political feasibility assessment, public legitimacy dynamics, social
cohesion signals, media framing, electoral mathematics, coalition survival.
Edge: macroeconomic modeling mechanics; confidence tier interpretation;
any quantitative framework at the indicator level. Andreas is the opposite
of Lucas — he cares deeply about outcomes and very little about methodology.
He trusts the tool if the political advisor or ministry economist he respects
trusts it.

**Mental Model at Session Entry**

"A good tool tells me whether this decision will survive 18 months politically."
Andreas is not asking about GDP. He is asking about public legitimacy, social
cohesion, and the political sustainability of the proposed adjustment path.
He needs human cost findings translated into political narrative: "3 CRITICAL
threshold crossings mean that the bottom quintile loses [X] in real terms by
year 2" is material he can use. "Human development composite score: 0.54"
is not.

**Entry State and Frame of Mind**

Primary states: **Reactive** (crisis decision in the next 48 hours) and
**Preparatory** (building the political brief before the minister meets
with Troika).

Most demanding: Reactive in a crisis decision window. The Cyprus bail-in
decision (March 2013) is the canonical case. A decision must be made within
48 hours. Andreas needs to know: does historical precedent suggest this type
of decision produces irreversible social legitimacy damage? At what point does
the governance indicator collapse? He needs Mode 1 (Replay) — not scenario
construction but historical pattern recognition.

Secondary most demanding: When briefing the minister on a conditionality
package. Andreas needs to translate the Finance Ministry Negotiator's
quantitative findings into a 3-slide brief the minister can consume in
5 minutes.

**Primary Task**

Translate the simulation's quantitative threshold crossings into a political
narrative: which cohorts are most affected, what is the social legitimacy
trajectory, and does the historical record show comparable cases where this
type of adjustment produced irreversible political damage? The bridge between
the Finance Ministry Negotiator's analytical output (indicator, step, cohort)
and the Institutional Decision-Maker's 5-minute brief.

**Trust Threshold**

Social dynamics and governance outputs are Andreas's primary signals — but
he cannot assess their quality directly. He trusts outputs when: (1) the
minister's existing economic advisor (Persona 1 or 2 equivalent) trusts
the underlying model; (2) the human cost findings match his own political
intuitions about what historical cases produced; (3) the language is plain
enough to translate directly into a briefing without technical processing.
He distrusts any output labeled "preliminary" or "exploratory" without
understanding what that means in practice.

**Preferred Information Format**

Headlines and percentages tied to specific population groups. Before/after
comparisons framed as "under this path, the bottom income quintile loses
approximately X% of real consumption by year 2." Traffic light indicators
(red/amber/green) for framework status. Not radar charts, not trajectory
curves without annotation. The governance indicator — social legitimacy and
social cohesion signals in particular — must produce narrative-ready outputs,
not just composite scores.

**Failure Mode**

Andreas stops consulting the tool if: (1) the governance and social dynamics
outputs are null or unavailable — if the tool cannot say anything about
political feasibility, it is not useful for his role; (2) the primary display
requires interpretation by an economist to understand — if he needs to ask
Lucas what the number means, the tool has failed his use case; (3) the
historical precedent pattern is absent — without Mode 1 replay of comparable
cases, he cannot build the political argument.

---

### Persona 4 — The Academic Researcher

**Identity**

Dr. Amara Diallo. Senior Research Fellow, Overseas Development Institute.
38 years old. PhD from the London School of Economics; dissertation on
fiscal multiplier heterogeneity in Sub-Saharan Africa. 10 years of
post-doctoral research; published in top field journals; regular contributor
to IMF research output. She evaluates analytical tools with the same
methodological rigor she brings to her own research. She is WorldSim's
most demanding epistemic critic and most valuable future ally.

**Domain Expertise Profile**

Deep: econometric methods, causal identification, heterogeneous treatment
effects, cross-country regression, distributional analysis, programme
evaluation. Edge: systems dynamics modeling, feedback graph architecture,
confidence tier systems (WorldSim's specific implementation). Amara's
edge is not the underlying economics — it is this specific tool's
implementation. She will read the methodology documentation before trusting
any output.

**Mental Model at Session Entry**

"A good analytical tool makes its assumptions explicit and its results
reproducible." Amara enters WorldSim as an evaluator before she enters as
a user. She reads CLAUDE.md, the founding document, and the ADRs before
she runs a simulation. She wants to understand what the model claims,
what it does not claim, and where its documented blindspots are. She is
not hostile — she is rigorous.

**Entry State and Frame of Mind**

Primary states: **Evaluative** (assessing WorldSim as a research platform
for potential citation or endorsement), **Retrospective** (running
historical cases to validate calibration against known outcomes), and
**Investigative** (exploring a specific research question using WorldSim
as an analytical instrument).

Most demanding: Evaluative. Amara will run the same backtesting case
multiple times with different parameter assumptions to test whether the
tool's outputs are sensitive to assumption choices in ways that the
methodology documentation does not disclose. She will try to break it.
If it survives her evaluation session, it has earned academic credibility.

**Primary Task**

Validate whether WorldSim's model specifications align with published
literature. Specifically: (1) do the simulation's fiscal multiplier
assumptions fall within the range of peer-reviewed estimates?; (2) does
the human development propagation chain match established empirical
relationships?; (3) does the backtesting output — the divergence between
predicted and observed trajectories — match the documented calibration
claims? Produce a reproducible result that can be cited or challenged.

**Trust Threshold**

Three non-negotiable requirements: (1) full methodology documentation
accessible from within the tool — not a link to a GitHub repository but
an in-session path to the ADR that governs each model component; (2)
confidence tiers displayed per indicator with sub-tier labels (SYNTHETIC_COMPARABLE
vs. SYNTHETIC_MODEL); (3) the backtesting divergence metric must be
accessible — she needs to know not just the predicted path but how far it
deviated from the observed path in historical cases. A tool that validates
itself without transparent calibration documentation has no standing in
peer-reviewed discourse.

**Preferred Information Format**

Methodology documentation first; numerical output second; charts for
orientation only. She will export raw data for analysis in her own tools.
Confidence intervals, sample sizes, comparison group composition, holdout
validation results. She wants the data behind the visualization, not just
the visualization. The IA1_CANONICAL_PHRASE about pre-calibration limits
is not a caveat to her — it is a calibration claim she will test.

**Failure Mode**

Amara abandons WorldSim as a research tool if: (1) the methodology
documentation cannot be accessed from within the tool or is incomplete;
(2) the model makes implicit assumptions without disclosing them — hidden
structural priors that produce the results without acknowledgment; (3) the
backtesting infrastructure cannot be run with user-specified historical data,
constraining her to pre-defined fixtures. She will publish a critique if
she believes the tool's credibility claims exceed its methodological
transparency.

---

### Persona 5 — The Institutional Decision-Maker

**Identity**

Aicha Mbaye. Finance Minister, Republic of Senegal. 56 years old. PhD in
economics from Paris; 15 years in academia followed by senior roles in
the WAEMU (West African Economic and Monetary Union) and the African
Development Bank; 3 years as Finance Minister. She commands the room
without needing to. She has sat on the IMF Executive Board as Senegal's
alternate governor. She does not use analytical tools directly — she
consumes demonstrations and briefs. She is the decision the tool's findings
are ultimately informing.

**Domain Expertise Profile**

Deep: macroeconomic policy, regional monetary frameworks, sovereign debt
diplomacy, political economy of programme conditionality, African development
finance. Edge: technical modeling details, simulation methodology, confidence
tiers, any quantitative framework below the aggregate level. Aicha's
expertise is at the strategic level — she knows what a fiscal multiplier
is, but she does not need to know how WorldSim implements one to make
a decision based on its output.

**Mental Model at Session Entry**

"A good tool gives me one clear answer and the confidence that the answer
is right." Aicha does not have 20 minutes to explore a simulation. She
has 5 minutes, possibly in a car, possibly between two other meetings.
The demonstration she is consuming must surface the key finding in the
first 30 seconds and provide the evidence in the next 2 minutes. Everything
else is noise.

**Entry State and Frame of Mind**

Primary state: **Demonstrative** — she is being shown the tool by someone
who prepared the analysis. She is not the analyst; she is the audience.
Secondary state: **Reactive** in crisis — when the IMF has just released
a statement about Senegal's programme performance, or when a regional
peer has defaulted, and she needs to know what the simulation suggests
about her own country's current position. In this state she is not being
shown anything — she is asking a direct question and needs a direct answer.

Most demanding: Reactive. She has asked a specific question: "Are we at
risk of the same thing that just happened to Ghana?" She needs an answer
in 3 minutes. Everything in the tool must serve that 3-minute window.

**Primary Task**

Receive a demonstration that surfaces the key finding — which frameworks
are deteriorating, which thresholds are at risk, what the instrument cluster
shows about the country's current trajectory — in under 5 minutes, without
requiring technical interpretation. Form a judgment: is this analysis
trustworthy, and does it change my position?

**Trust Threshold**

Institutional rather than methodological: (1) who is showing me this, and
do I trust their analytical judgment?; (2) is the institution credible —
has WorldSim been used by peers I respect?; (3) does the output match my
prior knowledge of the situation? If the simulation shows something she
knows to be wrong about her own country's fiscal position, she will distrust
everything else it shows. First demonstration must be calibrated against a
case she knows well.

**Preferred Information Format**

Three formats and no others: (1) traffic light status per framework —
red/amber/green without a number; (2) one-sentence finding per framework:
"Human development indicators show deterioration since step 2. Three
indicators have crossed warning thresholds."; (3) the single most important
chart, annotated in plain language. She does not read tables; she does
not interpret trajectory curves without annotation; she does not process
confidence tier numbers. The instrument cluster demonstration must be
optimized for non-technical consumption or it fails this use case entirely.

**Failure Mode**

Aicha terminates the demonstration and does not revisit the tool if:
(1) the first screen requires explanation before she can read it — any
technical label without a plain-language equivalent is a failure; (2) the
primary finding requires more than 5 minutes to reach; (3) the tool's
output is hedged to the point of providing no directional signal — "results
are uncertain and dependent on assumptions" without a central recommendation
is not useful for a decision. She needs the tool to take a position and
declare its confidence honestly, not retreat behind methodology.

---

## Section 2 — Entry State Taxonomy

Six entry states. Each maps to a distinct cognitive mode, opening screen
requirement, and failure condition. Personas experience different subsets.

| Entry State | Definition | What must appear in the first 60 seconds | Failure if wrong |
|---|---|---|---|
| **Investigative** | Exploring a question with no fixed deadline. Time-rich, agenda-open. | Entity selector visible; scenario list accessible; methodology documentation path clear; no loading placeholder as default state. | The tool appears inert or requires setup before the first useful output is visible. The user leaves before forming a question. |
| **Reactive** | Responding to an event that has already occurred. Question defined externally; time compressed. | The most recent completed scenario loads with its alert summary visible without navigation. MDA alert panel is the first surface. | The tool opens to a configuration screen or an empty canvas. The user cannot reach the alert summary without performing setup they do not have time for. |
| **Preparatory** | A known event is upcoming (negotiation, board meeting, crisis decision). Building the evidence base before it. | A clear path to scenario configuration from the landing state. A completed scenario opens directly to its summary output. | The scenario configuration workflow is buried or requires more than 3 steps to reach. The evidence assembly takes longer than the available preparation window. |
| **Demonstrative** | Showing the tool to an audience. Performance context; the analyst is not the audience; the audience is a decision-maker. | The instrument cluster is visible on the opening screen. The primary finding is legible without navigation. No setup required to reach the demonstration state. | The opening screen is a configuration view, empty canvas, or table of contents. The demonstrator must narrate what is about to appear before anything appears. |
| **Evaluative** | Assessing the tool's credibility and methodology. Meta-level exploration. Not consuming output — inspecting how the output is produced. | A direct path from any output to its methodology source. Confidence tier displayed per indicator. Backtesting output accessible. | The methodology is behind a link or a separate documentation site. The tool's claims about its own accuracy cannot be tested from within the session. |
| **Retrospective** | Running a historical case with known outcome to calibrate understanding or test tool accuracy. The outcome is known; the exercise is epistemic. | Mode 1 (Replay) is accessible from the landing state. Historical fixture data is loadable without custom configuration. The step counter makes the historical timeline legible. | Mode 1 requires the same setup as Mode 2. The user cannot distinguish a historical replay from a forward scenario. Historical calibration is treated as a scenario, not a replay. |

### Entry State × Persona Matrix

Frequency indicators: **P** = primary entry state for this persona;
**S** = secondary entry state; **O** = occasional; **—** = not typical.

| Entry State | Persona 1: Programme Analyst | Persona 2: Ministry Negotiator | Persona 3: Political Advisor | Persona 4: Academic Researcher | Persona 5: Decision-Maker |
|---|---|---|---|---|---|
| Investigative | S | O | O | P | — |
| Reactive | O | P | P | — | S |
| Preparatory | P | P | S | O | — |
| Demonstrative | — | O | S | O | P |
| Evaluative | S | — | — | P | — |
| Retrospective | S | O | — | P | — |

### Most Demanding Entry State per Persona

| Persona | Most demanding entry state | Why |
|---|---|---|
| 1 — Programme Analyst | Preparatory | Programme design deadline: specific output required on a fixed timeline |
| 2 — Ministry Negotiator | Reactive (in the room) | 90-second retrieval window; primary instruments must be immediately accessible |
| 3 — Political Advisor | Reactive (crisis window) | 48-hour decision horizon; historical precedent pattern is the primary need |
| 4 — Academic Researcher | Evaluative | Tool must survive methodological scrutiny; any opacity breaks trust permanently |
| 5 — Decision-Maker | Reactive | 3-minute answer window; no tolerance for navigation or technical interpretation |

---

## Section 3 — Primary Marquee Cases

One per persona. Historically grounded. Seven elements each: the room,
what they had, what they lacked, the decision made, the consequence, the
WorldSim intervention, and the exit criteria (the acceptance test).

---

### Primary Case 1 — The Multiplier Assumption

**Persona:** 1 — The Programme Analyst

**The room:** IMF Fiscal Affairs Department, Washington DC, May 2010. The
Greece programme team is finalizing the fiscal adjustment path. The programme
requires approximately 10% of GDP in fiscal consolidation over three years —
the largest such adjustment in OECD history at the time. The fiscal multiplier
assumption embedded in the model is 0.5, consistent with IMF standard practice
at the time. The assumption will be defended publicly as the consensus estimate.

**What they had:** IMF debt sustainability analysis; GDP growth projections
based on the 0.5 multiplier; aggregate poverty and unemployment projections;
the programme conditionality document. All standard outputs, all at the
aggregate level.

**What they lacked:** A sensitivity analysis showing what happens to human
development threshold crossings at multiplier values of 1.0, 1.5, and 2.0.
The Blanchard-Leigh literature establishing the true multiplier was 1.5–2.0
was three years away. But the uncertainty was not unknown — it was simply
not surfaced in the programme design. No tool existed to show that at
multiplier = 1.5, poverty headcount crosses a critical threshold at step 2,
not step 4. The human cost sensitivity to the multiplier assumption was
unmodeled.

**The decision made:** 10% of GDP fiscal consolidation over three years,
programme approved in May 2010.

**The consequence:** GDP contracted 25% over five years — roughly double the
initial projection. Youth unemployment reached 60%. Poverty headcount tripled.
The programme required two restructuring episodes (2012, 2015). In 2013,
Blanchard and Leigh published their IMF Working Paper establishing the fiscal
multiplier was 1.5–2.0, not 0.5. The human cost of the underestimated
multiplier was paid by the bottom income quintiles in the years between the
programme design and the methodological correction.

**The WorldSim intervention:** Lucas runs three scenario variants, each
identical except for the fiscal multiplier assumption: 0.5 (IMF consensus),
1.0 (literature lower bound), and 2.0 (Blanchard-Leigh upper bound). The
comparison view shows differentiated threshold-crossing maps. At multiplier
= 0.5: no CRITICAL MDA alerts in the first two steps. At multiplier = 1.5:
poverty headcount crosses WARNING at step 1, CRITICAL at step 2. At multiplier
= 2.0: poverty headcount crosses CRITICAL at step 1; health system capacity
crosses WARNING at step 2. The sensitivity map is the finding. Lucas now
has a quantified human cost argument for the programme design meeting: the
multiplier assumption is carrying a hidden human cost bet, and the tool
surfaces what that bet is worth.

**Exit criteria (acceptance test):** "Does the simulation produce differentiated
MDA alert maps for fiscal multiplier values of 0.5, 1.0, and 2.0 applied to
the same fiscal adjustment path? Does the comparison view identify which
human development indicators cross CRITICAL thresholds, at which step, and
for which income cohort, at each multiplier value? Are confidence tiers
displayed per indicator?"

---

### Primary Case 2 — The Second Memorandum

**Persona:** 2 — The Finance Ministry Negotiator

**The room:** Athens, late evening, February 2012. The Troika (IMF/ECB/EC)
has circulated a draft conditionality package for the second Greek memorandum.
Greece needs a second bailout to avoid default on March 20th debt payments.
The package includes minimum wage cuts of 22%, eighth-round pension reductions,
public sector dismissals, and an accelerated privatization schedule. Eleni
and her team have until morning to identify which specific terms cross
human cost thresholds — and to build a counter-proposal for the negotiating
session beginning at 9am.

**What they had:** The Troika's draft conditionality document; their own
fiscal staff estimates; partial social data from ELSTAT (Greek statistical
office); political guidance from the cabinet about which terms were politically
survivable.

**What they lacked:** A quantified threshold-crossing analysis showing which
specific conditionality terms drive CRITICAL human development alerts, at
which step, and for which cohorts. Without this analysis, the challenge to
any specific term is an assertion: "this will hurt people." The Troika's
counter-assertion — "adjustment is necessary for programme sustainability"
— carries more analytical apparatus. The asymmetry is not about values.
It is about which side has the quantified evidence.

**The decision made:** Greece accepted the package largely as presented.
Minimum wage was cut; pensions were reduced. Some modifications were achieved
on implementation timelines.

**The consequence:** Social indicators deteriorated sharply in 2012-2013.
The "internal devaluation" path produced distributional consequences that
subsequent analysis showed were concentrated in the bottom two income quintiles
and in pensioners above 65 — precisely the cohorts most dependent on public
transfers. The argument for protecting specific expenditure lines was never
made with the specificity needed to succeed.

**The WorldSim intervention:** Eleni runs two scenarios — the full Troika
package and her counter-proposal (same fiscal consolidation target, different
instrument mix: postpone minimum wage cut by 12 months; protect basic pension
floor; accelerate privatization in year 3 rather than year 1). The comparison
view shows that the full Troika package produces CRITICAL MDA alert on poverty
headcount at step 2 (bottom income quintile) and WARNING on health system
capacity at step 3. Her counter-proposal delays the poverty crossing to step 3
and avoids the health alert entirely. The delta is the negotiating position.
She has now built the case for a specific term modification: not "this is
harsh" but "this specific term, applied this way, crosses this threshold for
this cohort at this step."

**Exit criteria (acceptance test):** "Does the comparison view show differentiated
MDA alert timing for the two scenarios, with specific indicator, step, and
cohort data? Can the user identify the minimum modification to the conditionality
package that avoids a CRITICAL threshold crossing — i.e., does the simulation
surface which specific term is driving the alert? Is the navigation path from
the opening screen to the comparison view completable in under 5 minutes?"

---

### Primary Case 3 — The 48-Hour Window

**Persona:** 3 — The Political Advisor

**The room:** Nicosia, March 15-17, 2013. The Troika has proposed a levy
on Cypriot bank deposits as a condition of the €10B bailout — including
a haircut on insured deposits below the European deposit guarantee threshold
of €100,000. This was unprecedented in Eurozone history. President
Anastasiades's political team has approximately 48 hours before the parliament
vote. The question on the table is not the economics — the economics are clear.
The question is whether this decision destroys social legitimacy irreversibly,
and what the historical record shows about comparable decisions.

**What they had:** The Troika memorandum; their own political instincts;
knowledge of the Cypriot banking sector's dependence on Russian deposits;
awareness of the Iceland 2008 case and the Argentine 2001 deposit freeze
as partial comparables.

**What they lacked:** A structured Mode 1 replay of what happened to
governance and social legitimacy indicators in comparable cases — specifically,
at what step did legitimacy collapse become irreversible? Argentina 2001:
how quickly did social cohesion deteriorate after the corralito? Iceland 2008:
what distinguished the governance trajectory from Argentina's? The political
team needed a pattern recognition tool, not a forward scenario — they needed
to know what history says about this type of decision.

**The decision made:** The Cypriot parliament rejected the deposit levy 36-0,
with the government abstaining. A modified bailout was eventually adopted:
accounts above €100,000 were haircut; the bank guarantee for insured depositors
was honored. Capital controls lasted two years.

**The consequence:** The rejection of the original levy was widely credited
with preserving the basic social contract (the deposit guarantee) that Cyprus
required to remain economically functional. The alternative — implementing
the haircut on insured deposits — would have destroyed public trust in the
banking system across the Eurozone, with potential for bank runs far beyond
Cyprus.

**The WorldSim intervention:** Andreas runs Mode 1 (Replay) on the Argentina
2001 corralito. The simulation shows: social cohesion indicator collapses
at step 1 (deposit freeze announcement); governance indicator crosses CRITICAL
at step 2 (five-president period); the legitimacy cascade produces a TERMINAL
alert on political stability at step 3. He then runs Iceland 2008: governance
indicators decline at step 1 but stabilize by step 3; social cohesion
deteriorates but does not cross CRITICAL. The distinguishing factor:
Iceland's deposit guarantee was honored for domestic depositors; Argentina's
was not. Andreas now has a historical pattern: breach the deposit guarantee
→ legitimacy collapse (Argentina); honor it → governance cost but recovery
possible (Iceland). This is the political argument for the parliament vote.

**Exit criteria (acceptance test):** "Does Mode 1 (Replay) produce a
governance and social dynamics trajectory for Argentina 2001 showing
social cohesion and political stability threshold crossings with step-level
precision? Does the comparison view between Argentina and Iceland show
a legible divergence in governance trajectory following the deposit guarantee
decision? Are the social dynamics and governance indicators producing
non-null, non-placeholder outputs for these historical cases?"

---

### Primary Case 4 — The Backtesting Audit

**Persona:** 4 — The Academic Researcher

**The room:** Oxford, January 2014. Blanchard and Leigh's 2013 IMF Working
Paper ("Growth Forecast Errors and Fiscal Multipliers") has established that
IMF programme forecasts systematically underestimated the negative multiplier
effect of fiscal consolidation during 2010-2012. The IMF has acknowledged
the finding. A research fellow at ODI — Amara — is evaluating whether
WorldSim's backtesting infrastructure can reproduce the Blanchard-Leigh
finding, and whether the tool's multiplier specification is calibrated to
the updated literature. This is a tool evaluation, not a policy question.
The outcome of the case is already known. The exercise tests whether
WorldSim's output diverges from that outcome, and by how much.

**What they had:** Published Greek national accounts data 2010-2013
(GDP, unemployment, poverty headcount); the original IMF programme
projections for each indicator; Blanchard-Leigh's multiplier estimates;
IMF Working Paper data appendix.

**What they lacked:** A structured backtesting framework that would take
the Greece 2010 programme inputs, run the simulation, compare the projected
trajectory to the observed trajectory, and quantify the divergence. The
comparison between "what the model predicted" and "what actually happened"
is the primary signal for model improvement. Without accessible backtesting
output, the tool cannot earn academic credibility.

**The decision made:** (Prospective) If the backtesting divergence at
multiplier = 0.5 is substantial and the divergence at multiplier = 1.5 is
small, WorldSim's multiplier specification has been validated against an
independent dataset and the tool can be cited in peer-reviewed work.
If not, the specific calibration gap is documented for correction.

**The consequence:** (Prospective) A peer-reviewed citation that WorldSim's
backtesting results are consistent with the Blanchard-Leigh finding provides
the external academic validation that gives the tool credibility with
institutional users. Without this validation, the tool remains a private
analytical instrument.

**The WorldSim intervention:** Amara runs the Greece 2010-2012 simulation
with three multiplier values (0.5, 1.0, 1.5). She downloads the backtesting
divergence table for each run: predicted GDP path vs. observed GDP path,
step by step. At multiplier = 0.5, the model overpredicts GDP by 18% by
step 3 (consistent with the IMF's actual forecasting error). At multiplier
= 1.5, the model is within 8% of observed GDP at step 3. The poverty
headcount trajectory at multiplier = 1.5 is within 12% of ELSTAT's published
figures. The calibration report is specific, quantified, and citable.
Amara can write: "WorldSim's backtesting infrastructure reproduces the
Blanchard-Leigh multiplier sensitivity finding within ±12% on the GDP path
and ±15% on the poverty headcount trajectory for the 2010-2012 period."

**Exit criteria (acceptance test):** "Does the backtesting infrastructure
produce a divergence table comparing predicted to observed trajectories for
specified historical indicators, with confidence tiers for each comparison?
Does the simulation output at fiscal multiplier = 1.5 match the observed
GDP path for Greece 2010-2012 within a stated margin? Can the backtesting
result be exported in a format suitable for academic citation (including
methodology source, confidence tier, and comparison group documentation)?"

---

### Primary Case 5 — The Board Demonstration

**Persona:** 5 — The Institutional Decision-Maker

**The room:** IMF Headquarters, Washington DC, June 2015. An extended
Executive Board session on the Greek programme. The programme is in its
fifth year. The financial metrics show partial recovery in aggregate fiscal
terms. The human development metrics show sustained deterioration. Several
executive directors representing developing-country constituencies are
considering their vote — continuation vs. abstention. One of them has
5 minutes before the session resumes after a break.

**What they had:** An 80-page IMF staff report; a one-page summary from
their constituency office; general awareness that the programme had been
controversial; intuition that the human cost had been substantial.

**What they lacked:** A concise, non-technical visualization of whether the
programme was producing the outcomes it claimed — specifically, whether the
financial recovery was being purchased at proportionate or disproportionate
human cost. The 80-page staff report answers the financial question. It does
not answer the four-framework question.

**The decision made:** The Board continued the programme. The subsequent
Greek referendum (July 5, 2015) rejected the conditionality 61-39. Capital
controls were imposed the following week.

**The consequence:** The programme continuation set the stage for the
July referendum, which produced capital controls and a near-exit from the
euro. Whether a different Board vote would have produced a different
outcome is counterfactual — but the Board's view of the programme's
human cost trajectory was not fully informed by the distributional evidence
available.

**The WorldSim intervention:** A 5-minute demonstration using the Greece
2010-2015 six-step fixture (already built in M8). Three screens: (1) The
instrument cluster at step 6 (2015). Radar chart: financial framework
recovered partially (score 0.61), human development severely deteriorated
(score 0.27), governance declining (score 0.38), ecological not material
for this case. The asymmetry is visible without explanation — one axis up,
three axes down. (2) MDA alert summary: 4 CRITICAL threshold crossings.
First breach at step 2 (2012). Indicators: poverty headcount (bottom
quintile), health system capacity, youth employment, pension adequacy.
(3) PMM: declining throughout the programme horizon. The instrument cluster
tells the story in 90 seconds. The executive director can ask one question:
"Is the financial recovery purchasing the human cost, or was the human cost
the price of the financial recovery? Were there alternative paths?"

**Exit criteria (acceptance test):** "Does the four-framework radar chart
show the asymmetry between financial recovery and human development
deterioration in a way that is legible to a non-economist within 30 seconds?
Are the CRITICAL MDA alerts visible without opening a drawer or navigating
away from the primary viewport? Is the instrument cluster state at step 6
(2015) accessible from the landing screen without requiring scenario setup?
Can the demonstration be completed within 5 minutes by someone who has not
prepared a scenario in advance?"

---

## Section 4 — Secondary Marquee Cases

One per structural challenge. Globally distributed. Seven elements per case,
plus an eighth: the structural gap verdict.

---

### Secondary Case A — Political Economy as Binding Constraint

**Country/Year:** Argentina, December 2001 — the corralito and sovereign default

**Persona archetype:** Finance Ministry Negotiator (Persona 2) and Political
Advisor (Persona 3)

**The room:** Buenos Aires, December 1-10, 2001. After three years of
recession under the currency board arrangement (peso/dollar parity), the
De la Rúa government implements the corralito — a freeze on bank withdrawals
— on December 1st. Five presidents in ten days follow. Argentina defaults
on $100 billion in sovereign debt on December 24th, the largest default in
history at the time.

**What they had:** Standard macroeconomic adjustment programme; currency board
defence with IMF backing; political stability assumptions that were violated
before the programme could run.

**What they lacked:** A model that treats political economy collapse as a
binding constraint rather than an exogenous shock to be absorbed by the
programme. The programme failed not because the macroeconomics were wrong
but because the political system disintegrated before the adjustment could
occur. No standard IMF-style model captures this because it is not a
macroeconomic variable — it is a governance and social legitimacy threshold.

**The decision made:** The corralito was implemented. The consequences were
irreversible.

**The consequence:** GDP contracted 11% in 2002. Poverty headcount rose
from 25% to 57% in 12 months. The currency board collapsed; the peso
devalued 70%. The political legitimacy collapse preceded and caused the
economic collapse.

**The WorldSim intervention:** The simulation surfaces what the political
team needed — the governance indicator trajectory that the standard model
does not produce. The Social Dynamics agent models the political legitimacy
cascade from a deposit freeze. The question the tool must answer: "At what
governance threshold does the programme become politically unimplementable,
independent of whether it is economically sound?"

**Structural gap verdict:** This case exposes the limit of the current
governance modeling. GovernanceModule (M9 scope) carries social legitimacy
as an indicator — but social legitimacy as a threshold that makes other
policy instruments unavailable (not just deteriorating alongside them) is
a Political Economy constraint that the M11 political feasibility modeling
scope must address. The current architecture surfaces the governance signal;
it does not model governance collapse as a binding constraint on the
programme's other instruments. **Near-term partial (M9/M10): GovernanceModule
surfaces the signal. Full solution: M11 Political Economy module (Issue TBD).**

---

### Secondary Case B — Inflation-Driven Human Development Shock

**Country/Year:** Egypt, November 2016 — IMF programme and exchange rate float

**Persona archetype:** Finance Ministry Negotiator (Persona 2)

**The room:** Cairo, November 2016. Egypt signs a $12B IMF programme contingent
on floating the Egyptian pound. The pound had been maintained at an overvalued
peg for years. On November 3rd, the Central Bank floats the pound; it
immediately loses 50% of its dollar value. CPI inflation reaches 33% by
mid-2017. The human development impact is immediate: real wages fall, food
prices spike, poverty headcount rises rapidly in a country where 60% of
spending for lower-income households is on food.

**What they had:** Debt sustainability analysis showing the fiscal adjustment
path; exchange rate competitiveness analysis; aggregate macroeconomic
projections.

**What they lacked:** A tool that propagates the exchange rate shock through
the inflation channel to the human development trajectory. The sequence is
not complex: depreciation → higher import prices → consumer price inflation
→ real wage decline → poverty headcount increase. But the programme's
macroeconomic models treated these as separate analysis tracks. The human
cost of the exchange rate policy choice — which cohorts bear it, at what
speed, at what severity — was not modeled in the programme design.

**The decision made:** The float was implemented on the programme timeline.

**The consequence:** The fiscal programme succeeded in macroeconomic terms.
Inflation peaked at 33% and declined. External competitiveness improved.
The human development cost was concentrated in the first 18 months
post-float and fell disproportionately on urban lower-income households
dependent on food imports.

**The WorldSim intervention:** The simulation must propagate: `ExchangeRatePolicyInput`
→ import price increase → CPI change → real wage trajectory → poverty
headcount MDA alert. The current architecture handles this as an event-driven
chain; what is needed is the explicit implementation of the exchange rate
→ inflation transmission as a validated propagation relationship.

**Structural gap verdict:** **M10/M11 engineering problem.** The platform
principle holds — this is not an "Egypt mode," it is the exchange rate
→ inflation → human development propagation chain that is currently
unimplemented but architecturally within scope. The ControlInput taxonomy
includes `MonetaryPolicyInput` and the propagation engine supports
multi-hop chains. The missing piece is: (1) explicit exchange rate module
with calibrated depreciation-inflation pass-through coefficients, and
(2) CPI → real wage → poverty headcount as a validated propagation chain.
ADR required at implementation.

---

### Secondary Case C — Contagion and Regional Linkage

**Country/Year:** Sri Lanka, March-April 2022 — multi-shock convergence
and sovereign default

**Persona archetype:** Finance Ministry Negotiator (Persona 2) and
Programme Analyst (Persona 1)

**The room:** Colombo, early 2022. Sri Lanka is simultaneously absorbing
five shocks that have been building for three years: (1) 2019 Easter
Sunday bombings destroyed tourism (18% of GDP); (2) COVID-19 further
collapsed tourism; (3) 2021 ban on chemical fertilizers produced an
agricultural shock that halved rice yields; (4) Russia-Ukraine war in
February 2022 spiked oil prices in an economy 97% dependent on imported
energy; (5) a 2019 tax cut had depleted foreign reserves. By March 2022
Sri Lanka had fewer than 2 weeks of fuel reserves. Default followed
in April.

**What they had:** Individual sector analyses for each shock; IMF Article
IV reports noting fiscal deterioration; external debt analytics.

**What they lacked:** A tool that shows what happens when five moderate
shocks converge simultaneously. Each shock individually may not have been
crisis-triggering. Their simultaneous occurrence was. The simulation must
model cross-shock propagation — the interaction between the agriculture
shock, the energy price shock, and the reserves depletion is not additive;
it is multiplicative. When foreign reserves drop below a threshold, the
country loses the ability to respond to any single shock regardless of
its own merits.

**The decision made:** Sri Lanka sought IMF assistance in April 2022 after
defaulting. IMF programme signed in March 2023.

**The consequence:** Severe economic contraction; import restrictions that
forced hospitals to cancel surgeries for lack of supplies; fuel queues
lasting days; political collapse (President Rajapaksa fled in July 2022).
The human development impact was acute and concentrated on lower-income
households.

**The WorldSim intervention:** The primary question the tool must answer
is: at what point did the cumulative effect of these five shocks become
crisis-triggering, and which shock was the final constraint? This is the
Coffin Corner failure mode from the simulation framework — multiple constraints
binding simultaneously. The reserves depletion below minimum threshold
is the hard MDA floor; the tool must show when the cumulative shock path
crosses it.

**Structural gap verdict:** **M10 engineering problem.** The Coffin Corner
failure mode is architecturally specified in the simulation framework.
The multi-entity propagation graph handles cross-country contagion. The
within-country multi-shock convergence — where simultaneous shocks from
different domains (agriculture, energy, fiscal) interact — requires
the event accumulation system to handle multi-source shocks at the same
step without treating them as sequential. The `_DeltaAccumulator` collects
deltas before state construction; the question is whether the interaction
effects between simultaneous shocks are modeled (second-order propagation)
or just additive (first-order accumulation). Second-order is the correct
behavior for crisis convergence; current implementation is additive.
Issue for M10 scoping.

---

### Secondary Case D — Geopolitical Constraint on Programme Design

**Country/Year:** Ukraine, March 2015 — IMF programme under active conflict

**Persona archetype:** Programme Analyst (Persona 1)

**The room:** Washington DC and Kyiv, early 2015. Russia's annexation of
Crimea occurred in March 2014. Armed conflict in eastern Ukraine began in
April 2014. The IMF approves a $17.5B Extended Fund Facility for Ukraine
in March 2015. The programme requires fiscal consolidation, energy price
reform, and central bank independence — standard conditions. But the
programme entity (Ukraine) does not have full sovereignty over its own
territory. Military spending cannot be cut because there is an active war.
Eastern industrial regions are outside Kyiv's economic control. The IMF
programme model assumes the Ukrainian government can implement the programme.
This assumption is only partially true.

**What they had:** Ukraine's constitutional territory as the programme entity;
fiscal accounts for the government-controlled regions; IMF standard programme
framework.

**What they lacked:** A simulation framework that could model partial
sovereignty — that approximately 7% of the country's GDP was in territories
outside government control, that this constrained the fiscal adjustment
instruments available, and that the security spending floor was non-negotiable.
Standard IMF programme models assume the programme entity controls its own
instruments. When sovereignty is contested, this assumption fails.

**The decision made:** The programme was implemented on the basis of full
Ukraine as the entity. The eastern industrial capacity was simply excluded
from the fiscal model.

**The consequence:** The programme required multiple restructurings. Ukraine's
recovery was slower than projected, partly because the fiscal adjustment
was being implemented over a smaller revenue base than the programme assumed.
The human development impact was disproportionately felt in government-
controlled areas that bore the full adjustment while being partly severed
from their industrial base.

**The WorldSim intervention:** The current simulation architecture models
one entity per sovereign state. The tool cannot model partial sovereignty —
it cannot represent that one entity (Kyiv's fiscal authority) controls a
subset of the nominal entity's capacity. This is a fundamental architectural
constraint, not a data gap.

**Structural gap verdict:** **M11/M12 long-horizon design problem.** This
case exposes that the `SimulationEntity` model with a single `parent_id`
hierarchy cannot represent contested sovereignty without a schema extension.
Partial sovereignty modeling requires either: (a) splitting the entity into
government-controlled and contested-territory sub-entities with different
ControlInput capacity profiles; or (b) a "sovereignty constraint" parameter
that reduces the effective range of certain ControlInputs below their nominal
values. Both require explicit schema changes (ADR extension). This is
disclosed as a known limitation. The tool should document: "The simulation
assumes the programme entity has full implementation capacity over its
nominal territory. Where sovereignty is contested, the effective ControlInput
range may be narrower than modeled." **This is a fundamental constraint
requiring explicit disclosure, not an engineering fix.**

---

### Secondary Case E — Information Asymmetry and Data Infrastructure Gap

**Country/Year:** Zambia, November 2020 — first African COVID-era default

**Persona archetype:** Finance Ministry Negotiator (Persona 2) in the role
of the Zambian ministry analyst — the primary beneficiary side of the
democratization mission

**The room:** Lusaka, October-November 2020. Zambia misses a Eurobond
coupon payment of $42.5M in November 2020, becoming the first African
country to default in the COVID era. The default follows years of debt
accumulation, a significant portion of which is with Chinese bilateral
creditors. The terms of those bilateral loans are not publicly available.
The Zambian ministry team has incomplete information about their own
sovereign debt stock — specifically, the actual terms and conditions of
Chinese bilateral lending, which may include collateral provisions and
cross-default clauses that were not disclosed at the time of signing.

**What they had:** Published Eurobond terms; World Bank and IMF lending
data; their own ministry's fiscal accounts; limited sub-national poverty data.

**What they lacked:** Three compounding gaps that represent the three-layer
asymmetry: (1) **Data availability**: Chinese bilateral lending terms were
not publicly available; sub-national poverty data was 3 years old; key
fiscal indicators were available with 18-month delay. (2) **Data quality**:
GDP figures revised by 7-12% post-publication; poverty estimates from
different sources diverged by 15+ percentage points; debt data in the
ministry's own records did not match IIF (Institute of International Finance)
estimates. (3) **Institutional capacity**: the Zambian Ministry of Finance had
approximately 12 economists across all analytical functions; the IMF programme
team had 30 country economists working on Zambia alone; Chinese creditors
had institutional knowledge of the loan terms that the ministry no longer
had access to.

**The decision made:** Zambia requested debt restructuring. The process was
complicated by the opacity of the Chinese bilateral terms and took three
years to complete (first restructuring agreement reached in June 2023).

**The consequence:** Three years of debt limbo, during which Zambia could
not access capital markets and had to manage severe fiscal constraints.
The human development impact was concentrated in copper belt urban areas
and rural smallholder farming communities.

**The WorldSim intervention and synthetic data application:** This case is
the operational test of the democratization mission.

For Layer 1 (data availability — Chinese bilateral loan terms): Missing
because the data is MNAR — China does not publish bilateral lending terms.
The absence is itself a governance/political signal. WorldSim applies
**Method E (Structural Absence Declaration)**: `synthetic_method: "STRUCTURAL_ABSENCE"`,
`absence_reason: "Chinese bilateral lending terms are not publicly available.
Missingness is MNAR — the absence is a governance signal. Generating a
synthetic estimate would mask this signal. To enable this indicator, official
disclosure of bilateral terms is required."` The tool is honest about what
it cannot know.

For Layer 2 (data quality — revised GDP, divergent poverty estimates): Most
Zambian macroeconomic indicators are Tier 2-3. For indicators where
Sub-Saharan Africa comparables are available (≥10 comparable countries:
Zimbabwe, Tanzania, Mozambique, DRC, Malawi, Uganda, Angola, Senegal, Côte
d'Ivoire, Ethiopia), **Method A (Hierarchical Bayesian)** can be applied.
The comparison group produces Tier 3 SYNTHETIC_COMPARABLE estimates with
the mandatory per-indicator badge and comparison group exposure.

For Layer 3 (institutional capacity — 12 analysts vs. 30 counterparts):
This is not a data gap that synthetic data solves. It is a UX and
accessibility requirement. The tool must be operable by an analyst without
specialized econometric training. Help text, plain-language explanations
of confidence tiers, and progressive disclosure of methodology are required.
This is a design discipline problem, not an engine problem.

**Structural gap verdict:** **Addresses all three asymmetry layers.**
Layer 1: Structural Absence Declaration — correct output, implements in
M9/M10 with ADR-007. Layer 2: Synthetic data framework (ADR-007) is the
active solution; Sub-Saharan Africa comparison group registry needed
before Method A deployment. Layer 3: UX accessibility is a fundamental
ongoing design discipline; no single engineering fix, but a persistent
evaluation criterion for every design decision. This case must be the
primary design evaluation test for any new UX feature: can a Zambian
Ministry of Finance analyst with 12 economists and thin, delayed data
extract actionable intelligence from this feature? **Partially addressable
(M9 ADR-007; M10 comparison group registry). Institutional capacity gap
is a fundamental constraint requiring ongoing UX discipline, not a
software fix.**

---

## Section 5 — Tertiary Use Cases

Three cases, each framed as an ingredient specification — what data inputs
and simulation architecture capabilities this use case requires, not what
module it needs. The platform principle applies throughout.

---

### TC-1 — Trade Policy Shock: US Tariffs on Canadian Steel

**Scenario:** The Trump administration imposes 25% tariffs on Canadian steel
and aluminum, March 2018. Canada retaliates with equivalent tariffs on
US goods. The bilateral trade dispute creates immediate uncertainty for
Canadian steel-producing regions.

**Actor:** Senior Economist, Trade Policy Division, Global Affairs Canada.
Preparatory entry state. Has been asked to produce an evidence base for
the government's response strategy within 2 weeks.

**Question:** What is the projected employment and GDP impact on Canadian
steel-producing regions (Ontario, Quebec) over 3 years under three scenarios:
(a) tariff maintained without retaliation, (b) tariff with Canadian
retaliation as implemented, (c) negotiated exemption (actual outcome,
June 2018). Which policy response most effectively limits regional employment
impact?

**Simulation architecture required (ingredient specification):**
- Two entities: United States and Canada, connected by a bilateral trade
  relationship edge typed `TRADE`, with `weight` proportional to bilateral
  steel/aluminum trade volume (~$16B annually at baseline)
- The tariff shock is a `TradePolicyInput` applied to the bilateral
  relationship — a tariff rate change that modifies the effective `weight`
  of the trade relationship and flows through the Canada entity's export
  revenue trajectory
- Attenuation from the Canada entity to sub-national entities (Ontario,
  Quebec as child entities in the hierarchy) routed through the
  `parent_id` relationship
- Employment in manufacturing as a human development indicator
  propagating from the trade revenue shock through the GDP trajectory
- The comparison view requires three concurrent scenarios across the
  same step axis

**Current gap:** Multi-entity bilateral trade propagation with sub-national
attenuation is within the architecture's scope in principle. What is
needed: a two-entity fixture with a typed trade relationship edge and
confirmed propagation routing from national entity to sub-national child
entities. The MDA threshold for regional unemployment would need to be
configured in the fixture.

**Democratization dimension:** Canada is not a primary vulnerable actor
in the WorldSim sense, but this case demonstrates the tool's value for
any government facing asymmetric trade pressure from a dominant trading
partner. The underlying architecture — bilateral shock propagation with
sub-national attenuation — is the same capability needed for a Bolivian
analyst modeling the impact of Brazilian import quotas on highland
agricultural communities.

**Exit criteria:** "Does a 25% tariff shock on the Canada-US trade
relationship edge produce differentiated employment trajectory alerts
by sub-national entity over 3 steps, with confidence bands? Does the
comparison view support three concurrent scenario trajectories on a
shared step axis?"

---

### TC-2 — Geopolitical Contagion: Strait of Hormuz Closure

**Scenario:** A credible threat of Strait of Hormuz closure by Iran,
prompted by escalating US-Iran tensions. Jordan imports 97% of its energy
needs through the Gulf. Even a 60-day closure would exhaust Jordan's fuel
reserves and trigger severe import cost and fiscal consequences.

**Actor:** Senior Economist, Macro-Fiscal Analysis Unit, Jordan Ministry
of Finance. Reactive/Preparatory entry state. The analyst has received
an early warning briefing from the Central Bank and has been asked to
assess the fiscal impact and identify the emergency expenditure buffer
needed to prevent the most severe human development threshold crossings.

**Question:** What is the fiscal impact of a 60-day Hormuz closure on
the Jordanian economy? Which human development MDA thresholds are at risk?
What emergency expenditure buffer would be needed to prevent CRITICAL
threshold crossings in health and poverty indicators? What is the earliest
step at which the reserve adequacy MDA floor is breached?

**Simulation architecture required (ingredient specification):**
- Jordan as the primary simulation entity
- Oil price spike as an `EmergencyPolicyInput` — a global exogenous shock
  injected at step 0 with a specified duration (6 steps = 60 days at
  weekly resolution, or 2 steps at monthly resolution)
- The shock propagates through: energy import cost → fiscal deficit
  (Jordan's energy subsidy bill rises) → public expenditure capacity
  → health and social transfer human development indicators
- Reserve adequacy as a hard MDA floor: when reserves drop below
  X weeks of import cover, CRITICAL alert fires
- Synthetic data application: Jordan has reasonable data quality for
  Middle East comparables (Tier 2-3 for most macro indicators). Scenario
  bands for the oil shock transmission magnitude require Method A
  (Bayesian) from comparable import-dependent economies (Lebanon,
  Tunisia, Morocco, Egypt, Jordan's own 2008 oil shock — this is
  a Mode 1 calibration data point)
- Mode 1 calibration: Jordan 2008 oil price spike as a historical
  fixture to validate the shock transmission chain before running
  the forward scenario

**Current gap:** The oil price → energy import cost → fiscal deficit
→ human development chain requires: (a) Jordan energy sector data
seeding (IEA, Jordanian Ministry of Energy); (b) the energy import
dependency as a structural parameter of the Jordan entity (97% energy
import dependency); (c) the oil price transmission coefficient as a
calibrated propagation parameter. All are data and calibration requirements,
not architectural requirements. The propagation engine handles multi-hop
chains; what is needed is the specific implementation of this chain with
Jordan calibration data.

**Democratization dimension:** This is the canonical case for the
democratization mission. A Jordanian Finance Ministry analyst faces a
geopolitical shock manufactured by actors (US-Iran dynamics) entirely
outside Jordan's control or influence. The tool gives that analyst the
same quality of impact analysis that the US Treasury, the IMF Middle
East department, and sovereign wealth funds watching Jordan's credit risk
can already perform independently. This is the asymmetry the tool corrects.

**Exit criteria:** "Does an oil price exogenous shock injected at step 0
produce a differentiated human development alert trajectory for Jordan's
fiscal and health indicators over 6 steps? Does the simulation surface
the emergency expenditure buffer amount that would prevent the most severe
CRITICAL threshold crossings? Are the synthetic data scenario bands
(optimistic/realistic/pessimistic) for the shock transmission labeled
as inference uncertainty distinct from model uncertainty?"

---

### TC-3 — Annual Budget Planning: Kenya

**Scenario:** Kenya Finance Ministry annual budget planning for FY2025/26.
The Ministry is evaluating three fiscal paths: (a) baseline, no net
consolidation; (b) moderate consolidation, 2% of GDP over 3 years; (c)
IMF-recommended path per the 2023 programme, 3.5% of GDP. Kenya's 2023
IMF programme (ECF/EFF) provides a documented conditionality baseline
for comparison. Kenya has IMF and World Bank programme history and
relatively good data quality for Sub-Saharan Africa (World Bank WDI,
KNBS data, KIPPRA analysis).

**Actor:** Senior Economist, Budget Policy Department, Ministry of National
Treasury and Planning, Kenya. Preparatory entry state. Has 3 weeks before
the inter-ministerial budget consultation. Needs to identify which
consolidation path produces the most favorable trade-off between fiscal
sustainability and human development outcomes.

**Question:** Under each fiscal path, which human development indicators
are most at risk? What is the distributional impact by income quintile?
Does the moderate consolidation path avoid CRITICAL threshold crossings
that the IMF-recommended path triggers? What is the minimum-cost fiscal
path that keeps all indicators above WARNING level over the 3-step horizon?

**Simulation architecture required (ingredient specification):**
- Kenya as the simulation entity with real data seeded from: IMF Article
  IV (2023), WDI Kenya country page, KNBS Continuous Household Survey,
  Kenya Revenue Authority outturn data
- Three scenarios as concurrent Mode 2 comparisons (requires 3-way
  comparison mode or 2+1 branching comparison; see current gap below)
- Fiscal consolidation as `FiscalPolicyInput` applied at different
  magnitudes over 3 annual steps per scenario
- Confidence tiers reflecting Kenya data quality: macro fiscal indicators
  Tier 1-2 (WDI and IMF); subnational poverty estimates Tier 2-3;
  governance indicators may require Method A Bayesian from East Africa
  comparables (Uganda, Tanzania, Rwanda, Ethiopia, Ethiopia constitute
  a viable comparison group for most indicators)
- Synthetic data application for governance indicators: `technocratic_independence`
  and `social_cohesion` may require Method A from East Africa comparables;
  mandatory per-indicator synthetic badge; comparison group exposure
  within one click
- The 3-scenario comparison must surface differentiated MDA alert timing
  per scenario, not just composite score comparison

**Current gap:** Mode 2 comparison mode at M9 is designed for two-scenario
comparison. A 3-scenario comparison (baseline vs. moderate vs. IMF-recommended)
may require either running three pairwise comparisons or a multi-scenario
comparison mode that is not yet scoped. The exit criteria must be evaluated
against whatever comparison mode is available — if 2-way only, the Kenya
case requires two comparison sessions (baseline vs. moderate; moderate vs.
IMF-recommended) rather than one 3-way view.

**Democratization dimension:** A Kenya Finance Ministry analyst building
an independent assessment of the IMF-recommended conditionality path —
evaluating whether 3.5% consolidation is the minimum-cost path or whether
2% achieves an acceptable human development outcome — is the operational
definition of what WorldSim is for. The analyst is not rejecting the IMF;
they are engaging with the IMF from an informed position about their own
country's thresholds. This is the finance minister sitting across the
table with the same quality of analysis as the team across from them.

**Exit criteria:** "Does the 3-scenario comparison (or equivalent pairwise
comparison) show differentiated human development threshold crossings,
with specific indicator, step, and cohort data per scenario? Can the
Kenya analyst identify the minimum-cost fiscal path that avoids CRITICAL
thresholds within a 20-minute session? Are confidence tiers and synthetic
data flags displayed per indicator, with the East Africa comparison group
accessible within one click?"

---

## Section 6 — Product Scope Statement

WorldSim is an open-source geopolitical-economic simulation platform that
gives governments, central banks, and finance ministries the scenario analysis
capacity previously available only to the most sophisticated sovereign wealth
funds and financial institutions. The platform models national economies
as event-driven feedback graphs — not calculators but simulators — across
four simultaneous measurement frameworks: financial, human development,
ecological, and governance. It operates in three modes: Mode 1 (historical
replay and calibration), Mode 2 (scenario construction and path comparison),
and Mode 3 (active control with real-time policy feedback). Its primary and
hardest use case is sovereign debt negotiation support for programme countries:
a finance ministry analyst preparing a negotiating position against an IMF
conditionality package must be able to identify specific human cost threshold
crossings — with indicator, step, cohort, and severity specificity — in
under 90 seconds, using the instrument cluster alone, without opening a
drawer or navigating away from the primary viewport. The tool's secondary use
cases are equally within scope: trade policy impact analysis, budget planning
scenario comparison, geopolitical risk assessment, and historical calibration
for academic validation. Its most ambitious edge cases are data-poor
environments — Zambia, Chad, Sri Lanka, Jordan — where the synthetic data
framework (ADR-007) enables honest scenario construction from inference
rather than observation, with mandatory per-indicator disclosure of what was
measured versus what was inferred. In every case, the tool treats the human
cost ledger as a primary output with equal visual weight to financial
indicators, declares its own limitations explicitly, and is optimized for
the hardware and analytical capacity that resource-constrained finance
ministries actually have — not for the well-resourced institutions already
well-served by existing tools.
