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
> Public advocacy personas (6–8, Persona 4V) added: 2026-06-02 (Issue #575, panel-authorized).

---

## Section 1 — Formal Personas

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

### Persona 6 — The Investigative Journalist

*Public advocacy persona, Issue #575. Panel-authorized addition.*

**Identity**

Farida Haidari. Senior Correspondent, Economic and Financial Desk, Dawn, Karachi.
36 years old. BA in Journalism from University of Karachi; MSc in International
Political Economy from SOAS, University of London. Eight years covering Pakistan's
macroeconomic beat — IMF programme negotiations, sovereign debt management,
agricultural shocks, industrial contraction. She is not an economist. She reads
economic evidence with the precision of someone trained to find the buried fact,
not the headline claim. In August 2022, one-third of Pakistan submerged under
catastrophic flooding while the country was simultaneously under IMF programme
pressure requiring energy subsidy removal. She covered the human cost story. She
believes the causal chain between IMF conditionality, flood displacement, and food
security collapse was never quantified and published — not because the evidence
did not exist, but because no tool assembled it.

**Domain Expertise Profile**

Deep: financial and economic journalism, investigative data analysis, public records
navigation, interview methodology for technical subjects, synthesis under deadline.
Moderate: reading IMF Article IV documents and fiscal frameworks; understanding of
balance sheets, debt sustainability arithmetic, and programme conditionality. Edge:
econometric methodology, confidence tier systems, simulation architecture,
multi-framework composite scoring. She does not know what a fiscal multiplier is
at the mathematical level. She knows what it means for the families she interviews.

**Mental Model at Session Entry**

"A good tool gives me a specific, defensible claim I can put in a sentence." Farida
enters with a hypothesis, not a question. She knows what she is looking for — a
threshold crossing, a specific cohort, a specific step — that the official
programme narrative did not surface. She needs the tool to confirm or refute the
hypothesis with enough specificity to be publishable. "Human development
deteriorated" is not publishable. "The bottom income quintile in flood-affected
Sindh crossed a food security warning threshold at step 1 under combined shock
conditions, while the programme modeled the flood and subsidy removal as
independent shocks" is publishable.

**Entry State and Frame of Mind**

Primary state: **Investigative** — on a story, pursuing a specific hypothesis
within a 3-week investigative window before publication deadline.
Secondary state: **Reactive** — breaking-news mode when the IMF releases a country
statement or a new programme review triggers a deadline.

Most demanding: Investigative on a 3-week deadline. Farida will spend at most two
hours with WorldSim to extract the specific claim. If the tool cannot surface a
specific, citable finding in that session, it does not appear in the story and she
does not return for the next one.

Critical Layer 3 constraint: Farida has no specialist to mediate. She uses the tool
directly. If the instrument cluster requires economist-level interpretation to
produce a publishable claim, the tool has failed the journalism use case entirely.
The MDA alert summary must produce a sentence she can quote without requiring her
to understand how the simulation engine propagates events.

**Primary Task**

Identify the specific threshold crossing — indicator, step, income cohort, severity
— attributable to a combination of shocks, documented with enough precision to be
cited in a published article. The claim must be: (a) falsifiable and attributed to
a citable source (source registry ID visible); (b) specific enough to name the
cohort and the step; (c) defensible under editorial fact-checking; (d) distinct
from aggregate macroeconomic claims already on the public record.

**Trust Threshold**

Two non-negotiable conditions: (1) the source for every cited indicator must be
visible and citable at the indicator level — she needs the source registry ID to
include in her article's methodology note; (2) the finding must be specific enough
to be operationally distinct from what is already in the public domain — generic
deterioration signals are not publishable. Additionally: (3) the plain-language
alert must not claim more than the data supports. A Tier 3 synthetic estimate
stated as certain is a story about WorldSim's methodology problems, not about the
scenario.

**Preferred Information Format**

One specific claim, in plain language, with: indicator name, step index, cohort,
severity, and source citation. She will quote this as a sentence in the article.
She will not quote a chart. The MDA alert panel is her primary surface, provided
each alert states its claim in plain language rather than composite score notation.
She does not need to understand the radar chart; she needs the alert to tell her
what happened to whom at which step.

**Failure Mode**

Farida does not return to WorldSim if: (1) the instrument cluster requires an
economist to interpret — she will not cite an output she cannot explain; (2) the
plain-language MDA alert is absent or uses technical notation ("HDI indicator
below MDA floor") without a plain-language equivalent; (3) source attribution is
not visible at the indicator level — without a citable source, the finding cannot
be published; (4) the session produces only aggregate findings already on the
public record, adding no specific claim she can cite uniquely.

---

### Persona 7 — The Parliamentary Economist

*Public advocacy persona, Issue #575. Panel-authorized addition.*
*Political Economist validation: Kenya Parliamentary Budget Office established under
Public Finance Management Act 2012 — confirmed. Finance and National Planning
Committee — confirmed. EFF programme 7th review timeline — plausible. The persona
correctly notes that PBO economists typically review Treasury submissions rather
than run independent models; WorldSim's value here is enabling the independent
modelling that is within the PBO's mandate but constrained by available tools.*

**Identity**

James Ochieng. Senior Economist, Parliamentary Budget Office, Republic of Kenya.
41 years old. MSc in Economics from University of Nairobi; 7 years as a Treasury
analyst; 5 years at the PBO since its establishment under the Public Finance
Management Act 2012. His institutional mandate is to provide the National
Assembly's Finance and National Planning Committee with independent fiscal
analysis — analysis produced outside the Treasury and outside the IMF programme
team. He is not adversarial; he is institutionally required to be independent.
He has testified before the Finance Committee on Kenya's 2023 EFF programme four
times. He is preparing for the fifth hearing in 72 hours.

**Domain Expertise Profile**

Deep: fiscal policy and budget analysis, public expenditure tracking, programme
conditionality assessment, parliamentary procedure and evidence standards.
Moderate: econometric methods — can read regression output, understands confidence
intervals, does not independently build structural models. Edge: simulation
architecture, synthetic data methodology, multi-framework composite scoring.
James knows the Kenya fiscal data better than almost anyone outside the Treasury.
He knows which numbers in the IMF's programme projections are contested and why.

**Mental Model at Session Entry**

"A good tool gives me the independent estimate the Treasury won't produce." James
is not adversarial to the IMF or the Treasury — he is institutionally required to
be independent of both. He needs WorldSim to produce the same fiscal sustainability
and human cost analysis the Treasury is presenting, so the Finance Committee can
hear an independent verification or challenge. If the simulation agrees with the
Treasury's projections, the committee hearing will say so. If it diverges, the
committee needs to know where, why, and at which step.

**Entry State and Frame of Mind**

Primary state: **Preparatory** — 72 hours before a committee hearing; building the
independent evidence base.
Secondary state: **Reactive** — emergency session, often following IMF press
releases or mid-programme review announcements.
Occasional: **Evaluative** — assessing WorldSim's methodology before citing it in
Hansard for the first time. **Retrospective** — running Kenya's 2011 IMF programme
as a historical calibration before relying on the tool for current-programme analysis.

Most demanding: Preparatory with a 72-hour deadline. James has three days to run
the independent scenario, compare it to the Treasury's projections, identify
divergences, and produce a 4-page committee brief that a Finance Committee member
without specialist training can follow. Time is fixed; quality cannot be cut.

Critical constraint: James's brief will be cited in Hansard — the official
parliamentary record. A finding later demonstrated to be wrong has institutional
consequences beyond a single session. His trust threshold is accordingly high:
the simulation must carry explicit confidence tiers, transparent methodology, and
a clear statement of what is modeled versus what is assumed.

**Primary Task**

Produce an independent assessment of Kenya's 3.5% GDP fiscal consolidation path
under the 2023 EFF programme. Specifically: (1) does the simulation confirm or
challenge the Treasury/IMF GDP growth projection at each step?; (2) which human
development indicators cross WARNING or CRITICAL thresholds under the programme
path that the official projections do not flag?; (3) does an alternative 2%
consolidation path avoid those threshold crossings while maintaining fiscal
sustainability above the MDA floor? The committee brief must name the specific
terms and steps where the two paths diverge.

**Trust Threshold**

Parliamentary evidence standards: (1) methodology must be transparent enough to
withstand a Treasury rebuttal in committee — James needs to explain, in plain
language, how WorldSim reached its finding; (2) confidence tiers must be visible
per indicator — a Tier 2 finding is defensible in committee; a Tier 3 synthetic
estimate requires explicit qualification; (3) the output must be reproducible
within the committee hearing day — if a committee member requests a re-run with
different assumptions, he must be able to do it. Non-reproducible outputs cannot
be cited in Hansard.

**Preferred Information Format**

4-page committee brief format: executive summary (1 page, no jargon, three key
findings); threshold crossing table (indicator, step, severity, scenario
comparison); methodology note (confidence tiers, data sources, model limitations
disclosed). He will produce this brief from WorldSim's tabular output. Trajectory
charts are useful for orientation. He needs the underlying data in downloadable
form for independent formatting.

**Failure Mode**

James cannot use WorldSim for committee testimony if: (1) the methodology is not
accessible from within the tool — he needs to be able to cite the ADR governing
the fiscal multiplier specification, not just state "the model shows X"; (2)
confidence tiers are aggregated or unavailable at the indicator level — "the model
is pre-calibration" without specifying which indicators carry which tier is
insufficient for parliamentary evidence; (3) the simulation cannot be re-run with
user-specified parameters in real time — if he cannot change the consolidation rate
and observe the effect, the tool is a black box that Hansard cannot cite.

---

### Persona 8 — The Civil Society Monitor

*Public advocacy persona, Issue #575. Panel-authorized addition.*
*Political Economist validation: SEND Ghana is a real organization (Social
Enterprise Development Foundation of West Africa, Accra). Ghana ECF programme
($3B, May 2023) confirmed. Social protection floor commitment in Ghana ECF is a
real programme feature — SEND Ghana has published monitoring reports on it. The
1.2% GDP floor is used as a plausible approximation; the actual programme uses
absolute spending floors in specific categories. Persona validated.*
*Customer Agent finding: integrated observed-actuals input (entering real-world
step data alongside projected trajectory) is not a current platform capability.
This is flagged in the Primary Task section and reflected in the Failure Mode.*

**Identity**

Abena Osei. Programme Economist, SEND Ghana (Social Enterprise Development
Foundation of West Africa), Accra. 33 years old. BSc in Economics from University
of Ghana, Legon; MSc in Development Economics from the Institute of Social
Studies, The Hague. 6 years at SEND Ghana, the last two focused on tracking
Ghana's IMF programme commitments against reported outcomes. She is not the
government; she is not the IMF. She is the civil society actor whose institutional
role is to hold both accountable to what was promised. She tracks the gap between
the programme's stated human development commitments and what field monitoring
shows.

**Domain Expertise Profile**

Deep: programme monitoring and evaluation, participatory data collection,
community-level impact assessment, public finance tracking, civil society
advocacy. Moderate: macroeconomic analysis — reads programme documents, fiscal
frameworks, and MDA definitions; moderate quantitative skills. Edge: simulation
architecture, synthetic data methodology. Abena knows what the programme
committed to. She has the baseline data. She needs to track whether the trajectory
is matching the commitment.

**Mental Model at Session Entry**

"A good tool shows me where the gap is between what was promised and what is
happening." Abena entered Ghana's IMF programme monitoring cycle in 2022. She
knows what the programme's baseline scenario claimed. She needs WorldSim to
reproduce that baseline and compare it to observed outcomes — step by step — so
she can identify which commitments are being honored and which are diverging.

**Entry State and Frame of Mind**

Primary state: **Retrospective** — accountability tracking sub-mode. The committed
baseline is known (the programme's own projections); the exercise is verification
of whether observed actuals match it. This is distinct from historical calibration
(where the outcome is fully known): here the trajectory is still emerging, but
the reference path is fixed.
Secondary state: **Investigative** — when following up on a specific government or
IMF claim about programme outcomes.

Most demanding: Retrospective in accountability mode with a publication deadline.
Ghana's December 2022 IMF programme included explicit social protection floor
commitments. Six months in, field monitoring shows spending below the floor. Abena
has 30 days to present this finding to Parliament, the IMF Ghana Mission Chief,
and community organizations in northern Ghana. The evidence must be specific enough
to require a specific response — not a generic acknowledgment.

**Primary Task**

Reproduce the Ghana 2022-2023 IMF programme's committed baseline trajectory for
social protection spending and healthcare floor commitments. Compare the baseline
to observed quarterly expenditure data. Identify the steps at which committed
expenditure levels are not being met. Produce a quarterly monitoring brief that
names the specific commitments not honored and the human development indicators
most at risk.

Current platform limitation (Customer Agent finding, Issue #575 panel): WorldSim
can reproduce the programme baseline as a forward scenario. It does not currently
support entering observed actuals as step-level inputs for divergence calculation
within the tool. Abena's accountability tracking requires this capability. Until
it exists, she manually compares the simulation's step-level projected output to
her observed data — possible but not integrated. This gap is a primary engineering
requirement for the civil society monitoring use case. Filed for roadmap
consideration.

**Trust Threshold**

Community accountability standards: (1) findings must be tied to specific,
verifiable commitments — the simulation generates the counterfactual baseline, but
the accountability finding is the gap between that baseline and observed data;
(2) the monitoring brief must be legible to a community leader in northern Ghana
without a university education — plain language is not a preference, it is an
institutional obligation; (3) where the simulation introduces uncertainty, that
uncertainty must be disclosed. She will not present a synthetic inference as a
programme commitment.

**Preferred Information Format**

Two-layer output: (1) technical layer (her own analysis) — trajectory chart
showing programme baseline against observed actuals, with divergence markers;
confidence tiers per indicator; source attribution; (2) community layer (the
monitoring brief) — plain-language summary per commitment: on-track or diverging,
and what that means in terms of specific services (school meals, health clinic
visits, cash transfer amounts). Both layers must be produceable from a single
session.

**Failure Mode**

Abena cannot use WorldSim for accountability monitoring if: (1) the platform
cannot integrate observed actuals alongside simulated projections — the core
accountability function requires comparing what was promised to what happened
(structural gap flagged above; roadmap item); (2) the output cannot be translated
into plain language for community audiences — expert-only output is institutionally
unusable; (3) the baseline scenario cannot be reproduced from the programme's own
committed inputs — if the simulation's baseline does not match the programme's
stated commitment, the comparison is invalid.

---

### Persona 4 Variant — The Personal-Connection Researcher

*Variant of Persona 4 (The Academic Researcher). Same 8-dimension format.
EL-authorized addition (Issue #575). Differentiated by: lived proximity to the
subject; personal stake in findings' accuracy; higher tolerance for tool limitations
combined with sharper challenge of findings that contradict direct observation.*
*Development Economist validation: Vidarbha cotton farmer suicide crisis is
extensively documented — NSSO Agricultural Household Survey (2013, 2019),
M.S. Swaminathan Commission reports (2004–2006), AGMARK price series (Wardha
district), EPW literature (Mishra 2008, Nagaraj et al. 2014). CDS
Thiruvananthapuram and JNU are real institutions with active agrarian economics
programmes. The causal chain (AGMARK cotton price → farm gate revenue → household
debt service → food expenditure reduction) is established in the literature.
Historical grounding confirmed.*

**Identity**

Dr. Priya Krishnaswamy. Research Associate, Centre for Development Studies,
Thiruvananthapuram, Kerala. 32 years old. PhD in Agricultural Economics from
Jawaharlal Nehru University; dissertation on the political economy of agricultural
subsidies and farmer indebtedness in Vidarbha, Maharashtra. Her father is a cotton
farmer in Wardha district — one of the districts with the highest farmer suicide
rates in India's farm crisis period (2004–2015). She studies the academic
literature on agrarian distress with the knowledge that the farm in the literature
is her family's farm. She uses WorldSim because she wants to know whether the
simulation's output about agricultural market reform and income volatility matches
what she has observed directly — and when it does not, she wants to know exactly
which assumption produced the divergence.

**Domain Expertise Profile**

Deep: agricultural economics, political economy of rural markets, farmer
indebtedness and credit access, rural poverty measurement, agrarian distress
indicators. Moderate: macroeconomic modeling, simulation methodology, confidence
tier systems. Edge: simulation architecture, governance module outputs, financial
composite scoring. Her edge is not the economics — it is this specific tool's
implementation of agricultural income transmission chains, which she will verify
against her own field data and her dissertation dataset.

**Mental Model at Session Entry**

"A good tool tells me whether its model matches what I've observed — and if not,
shows me exactly where the divergence is." Priya is both evaluator and engaged
user. She enters with more tolerance for limitation than Amara (Persona 4) — she
knows real-world complexity cannot be fully modeled. But she is harder to convince
when a finding contradicts her direct observation. If WorldSim shows agricultural
market deregulation has a neutral effect on cotton farm income in step 2, and her
dissertation data shows income declined 32% in comparable districts in the same
period, she wants to see the specific model assumption that produces the discrepancy
— not a confidence tier disclaimer.

**Entry State and Frame of Mind**

Primary states: **Investigative** (pursuing a research question using WorldSim as
one instrument in a multi-method analysis), **Retrospective** (running historical
cases to compare simulation output to field data she collected directly), and
**Evaluative** (assessing whether WorldSim's agrarian distress modeling is
sufficiently calibrated to be cited in an agricultural economics journal).

Most demanding: Retrospective with personal-observation verification. When the
simulation diverges from what she observed in Wardha district — not what the
literature says, but what she personally documented — she needs the model to show
its work at the specific variable level where the divergence occurs. This is the
most demanding trust test: the user knows more than the model about one specific
data point, and the model must acknowledge that.

**Primary Task**

Use WorldSim to model the income and food security trajectory for smallholder
cotton farmers in Vidarbha during India's 2020-2021 farm law reform period.
Specifically: (1) does the simulation's output for agricultural income volatility
under market deregulation match the pattern documented in her field data?;
(2) does the human development propagation chain — from farm income decline to
household food security to child nutrition — match established agricultural
economics literature on Vidarbha?; (3) produce a backtesting comparison between
the simulation's trajectory and the NSSO Agricultural Household Survey data that
she can include in a journal submission.

**Trust Threshold**

Three conditions, in priority order: (1) the simulation's output must be
falsifiable against her own data — a discrepancy is acceptable if the tool shows
exactly which assumption produces it; (2) confidence tiers must be displayed at
sub-indicator level, distinguishing SYNTHETIC_COMPARABLE (regional agricultural
data available) from OBSERVED (actual AGMARK cotton price series); (3) the
backtesting divergence metric must be downloadable in a format suitable for a
journal data appendix — the format matters for peer review. Additionally: when
the simulation conflicts with her direct observation, the tool must not claim the
simulation is more accurate than her fieldwork. Her dissertation dataset (47
households, Wardha district, 2015) is Tier 2-3 for those households and Tier 4
for regional inference. The simulation's comparable-economy estimate is Tier 3.
They are roughly comparable in credibility. The tool must reflect this.

**Preferred Information Format**

Methodology documentation first; numerical output second; charts for orientation
only. She will export raw trajectory data to R for independent analysis. She reads
confidence tier displays carefully and will challenge a synthetic estimate that
appears to carry more precision than the underlying comparison group justifies.
The divergence table (simulation prediction vs. observed outcome) is her primary
analytical artifact.

**Failure Mode**

Priya disengages from WorldSim as a research instrument if: (1) the model produces
output that conflicts with her direct observation without showing the specific
assumption driving the divergence — she cannot include an unexplained discrepancy
in a journal submission; (2) the agricultural income transmission chain is
unimplemented or modeled as a simple GDP multiplier rather than a structured
propagation from farm gate price to household income to food security — if the
causal mechanism is absent, the tool is not useful for her research question;
(3) the backtesting output cannot be exported in a citeable format — the journal
data appendix requirement is non-negotiable.

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
| **Retrospective** | Running a known reference path against actual or observed trajectories. Two sub-modes: (a) Historical calibration — the outcome is fully known; the exercise tests model accuracy against history. (b) Accountability tracking — a prior projection or committed programme baseline is known; the exercise verifies whether observed actuals track the reference path. In both sub-modes, the reference path is known; the exercise is verification. The outcome may be fully known (calibration) or still emerging (accountability). | Mode 1 (Replay) is accessible from the landing state. Historical fixture data is loadable without custom configuration. The step counter makes the historical timeline legible. For accountability tracking: a prior scenario's projected output is accessible for step-by-step comparison alongside observed actuals. (Note: integrated observed-actuals input is a forward capability; manual comparison is currently required.) | Mode 1 requires the same setup as Mode 2. The user cannot distinguish a historical replay from a forward scenario. For accountability tracking: the baseline scenario cannot be reproduced from programme inputs, or the tool conflates simulation uncertainty with programme commitment uncertainty. |

### Entry State × Persona Matrix

Frequency indicators: **P** = primary entry state for this persona;
**S** = secondary entry state; **O** = occasional; **—** = not typical.

| Entry State | P1: Programme Analyst | P2: Ministry Negotiator | P3: Political Advisor | P4: Academic Researcher | P5: Decision-Maker | P6: Journalist | P7: Parliamentary Economist | P8: Civil Society Monitor | P4V: Personal-Connection Researcher |
|---|---|---|---|---|---|---|---|---|---|
| Investigative | S | O | O | P | — | P | O | S | P |
| Reactive | O | P | P | — | S | S | S | — | — |
| Preparatory | P | P | S | O | — | — | P | — | O |
| Demonstrative | — | O | S | O | P | — | — | — | — |
| Evaluative | S | — | — | P | — | — | S | — | P |
| Retrospective | S | O | — | P | — | — | O | P | P |

### Most Demanding Entry State per Persona

| Persona | Most demanding entry state | Why |
|---|---|---|
| 1 — Programme Analyst | Preparatory | Programme design deadline: specific output required on a fixed timeline |
| 2 — Ministry Negotiator | Reactive (in the room) | 90-second retrieval window; primary instruments must be immediately accessible |
| 3 — Political Advisor | Reactive (crisis window) | 48-hour decision horizon; historical precedent pattern is the primary need |
| 4 — Academic Researcher | Evaluative | Tool must survive methodological scrutiny; any opacity breaks trust permanently |
| 5 — Decision-Maker | Reactive | 3-minute answer window; no tolerance for navigation or technical interpretation |
| 6 — Investigative Journalist | Investigative | 2-hour session cap; publishable specific claim required; no specialist mediation; plain-language output is mandatory |
| 7 — Parliamentary Economist | Preparatory | 72-hour deadline; findings cited in Hansard; reproducible within the committee hearing day |
| 8 — Civil Society Monitor | Retrospective (accountability) | 30-day publication cycle; community-audience legibility required; platform capability gap for integrated actuals input |
| 4V — Personal-Connection Researcher | Retrospective | Personal-observation verification: when simulation diverges from direct field data, the specific assumption must be visible |

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

### Primary Case 6 — The Flood and the Programme

**Persona:** 6 — The Investigative Journalist

**The room:** Dawn newsroom, Karachi, October 2022. Farida has returned from a
two-week reporting trip to Sindh province, where she interviewed flood-displaced
families subsisting on government relief food distribution. Pakistan's catastrophic
2022 monsoon floods — the most destructive in the country's recorded history —
submerged one-third of the country between July and September. Simultaneously,
Pakistan was under IMF pressure to remove energy subsidies as a condition of the
7th EFF review. Subsidies were removed in June 2022, one month before the floods
began. The IMF programme's targeted subsidy scheme was designed to protect the
bottom quintile from the subsidy removal; it was not designed for a simultaneous
30% agricultural income loss from flood displacement.

**What they had:** IMF 7th EFF review documents; HIES 2018-19 household data;
NDMA flood damage assessments; reporting from field visits with displaced families;
existing public analysis treating the flood and the subsidy removal as separate
events.

**What they lacked:** A tool that models what happens to a specific income cohort
when a fiscal shock (energy price increase) and a physical displacement shock
(agricultural income loss from flood) operate simultaneously rather than
sequentially. The IMF programme's bottom-quintile protection assumption held under
subsidy removal alone. It was not evaluated under the combined shock. No published
analysis had quantified the combined effect on a specific cohort at a specific step.

**The decision made:** (Prospective) If the simulation confirms that the combined
shock drives a CRITICAL food security threshold crossing at step 1 for the bottom
income quintile, Farida has the publishable claim: "The IMF programme's bottom
quintile protection assumption failed under combined shock conditions — a finding
the programme design did not surface."

**The consequence:** HIES data released in 2023 showed poverty headcount in
flood-affected districts rose sharply in 2022-23. If WorldSim's combined-shock
scenario predicted this crossing before the data was released, the tool
demonstrated prospective value for economic journalism. If the data was already
available, the tool provided the specific causal mechanism — the interaction of
two shocks on one cohort at one step — that explained what the aggregate data showed.

**The WorldSim intervention:** Farida runs two scenarios: (a) IMF programme +
energy subsidy removal only; (b) IMF programme + energy subsidy removal +
agricultural income displacement shock (30% agricultural capacity reduction for
flood-affected districts, 2 steps). The comparison view shows: scenario (a) —
no CRITICAL food security alert in the first 2 steps (consistent with programme
design). Scenario (b) — CRITICAL food security alert for bottom income quintile
at step 1; CRITICAL poverty headcount at step 2. The plain-language MDA alert
reads: "Food security for Pakistan's lowest-income households crossed a critical
threshold at step 1 under combined shock conditions. Under programme-only
conditions, this threshold was not breached in the same period." That is the
sentence that goes into the article.

**Exit criteria (acceptance test):** "Can a user with no specialist economics
training navigate from the landing screen to a plain-language MDA alert summary
within 30 minutes? Does the comparison view produce a differentiated
threshold-crossing finding between the combined-shock scenario and the
programme-only scenario, with cohort specificity (bottom income quintile) and step
precision? Is the source registry ID for each cited indicator visible and
accessible without navigating away from the instrument cluster? Is the
plain-language MDA alert legible to a non-economist journalist without requiring
specialist interpretation?"

---

### Primary Case 7 — The Committee Brief

**Persona:** 7 — The Parliamentary Economist

**The room:** Parliamentary Budget Office, Nairobi, March 2023. The National
Assembly Finance and National Planning Committee is hearing evidence on the 7th
review of Kenya's IMF EFF programme. The Treasury has presented its mid-programme
assessment showing the fiscal path is on track. James has 72 hours to produce an
independent assessment — specifically, whether the 3.5% GDP consolidation path
is producing human development threshold crossings that the official projections
do not flag.

**What they had:** IMF 7th EFF review documents; Kenya Treasury fiscal framework
presentation; KNBS data through Q3 2022; Kenya's Medium-Term Budget Strategy
Statement; World Bank WDI Kenya page; the PBO's own prior brief from the 4th
review hearing.

**What they lacked:** A quantified, indicator-specific threshold-crossing analysis
showing how the 3.5% path compares to a 2% alternative on human development
outcomes. The Treasury's presentation treated human development in aggregate terms
("poverty reduction is on track"). The Finance Committee minority report from the
previous hearing had recommended slowing the consolidation pace — but was unable
to name the specific threshold, indicator, step, and cohort that a slower path
would protect. The minority report stated a concern; it did not state a finding.

**The decision made:** (Historical) The Finance Committee published a minority
report recommending re-examination of the consolidation pace, citing human
development risks in healthcare and education spending. The minority report cited
insufficient quantified evidence — the exact gap WorldSim addresses.

**The consequence:** The minority report had limited impact because it lacked
indicator-specific threshold-crossing evidence. "We believe the consolidation is
too fast" without naming the specific threshold, cohort, and step cannot survive a
Treasury rebuttal that cites its own programme projections. Step-level threshold
evidence with indicator specificity would have produced a more defensible brief.

**The WorldSim intervention:** James runs two scenarios: (a) 3.5% GDP
consolidation per IMF EFF; (b) 2% alternative. The comparison shows: at 3.5%,
education spending crosses WARNING at step 2 (below UNESCO per-student expenditure
floor); healthcare capacity crosses WARNING at step 3. At 2%, neither threshold is
crossed within the 4-step programme horizon. The committee brief states: "The
programme path triggers two WARNING threshold crossings — education spending at
step 2 and healthcare capacity at step 3 — that the 2% alternative path avoids
within the programme horizon." This is the finding the minority report needed.

**Exit criteria (acceptance test):** "Does the comparison view identify specific
human development threshold crossings at the programme-recommended consolidation
rate that are avoided at the 2% alternative, with indicator name, step index, and
severity? Is the simulation reproducible with a different consolidation rate within
the committee hearing day (same-session parameter change)? Is the methodology
documentation accessible from within the tool and citable by ADR reference without
navigating to an external site? Can a 4-page committee brief be drafted from the
tool's tabular output within 2 hours?"

---

### Primary Case 8 — The Accountability Gap

**Persona:** 8 — The Civil Society Monitor

**The room:** SEND Ghana offices, Accra, July 2023. Ghana signed its IMF ECF
programme in May 2023 — $3B over three years — following the 2022 debt default
and restructuring process. The programme included explicit social protection floor
commitments: government spending on social protection would not fall below a
defined floor during the programme period. Six months in, Abena's team has
obtained Treasury quarterly expenditure data showing social protection spending
below the committed floor. She needs to present this finding to the National
Assembly Finance Committee, the IMF Ghana Mission Chief, and community
organizations in northern Ghana within 30 days.

**What they had:** Ghana's IMF ECF programme document (May 2023); Treasury
quarterly expenditure reports; SEND Ghana field monitoring data from community-
level cash transfer disbursements; prior SEND Ghana analyses of Ghana's LEAP
programme performance going back to 2012.

**What they lacked:** A tool that could reproduce the programme's committed
trajectory — what social protection spending should look like at each step under
the programme floor — and compare it to the observed trajectory with indicator-
level specificity. Without the committed baseline, the finding is: "spending is
below commitment." With the committed baseline and a divergence simulation: "at
observed spending levels, the social protection floor is breached, and this breach
predicts child nutrition crossing a threshold the programme commitment was
specifically designed to prevent."

**The decision made:** (Prospective) If SEND Ghana presents a specific,
step-level divergence finding — not a general shortfall but an indicator-specific
threshold crossing attributable to the spending floor breach — the IMF Mission
Chief cannot respond with "the programme is broadly on track" without addressing
the specific finding. A specific claim requires a specific response. A generic
concern does not.

**The consequence:** Ghana's LEAP programme has consistently underperformed
stated targets since 2012. Each shortfall has been documented and generally
acknowledged without specific corrective action, partly because documentation
has been in aggregate terms easy to counter with aggregate assurances. Indicator-
specific, step-level threshold evidence creates accountability where aggregate
evidence does not. This case is the civil society monitor's core thesis: specific
claims produce specific responses.

**The WorldSim intervention:** Abena reproduces the Ghana ECF baseline scenario
using the programme's committed inputs. The simulation produces the projected
trajectory for social protection spending, poverty headcount, and child nutrition
at committed spending levels. She manually compares step-level projected values to
her observed Treasury data (current platform limitation: this comparison is
external to the tool). The divergence at step 1: observed spending is 0.3
percentage points of GDP below the committed floor. Running a second scenario with
the corrected (lower) spending input shows child malnutrition crossing WARNING at
step 2 and approaching CRITICAL at step 4 if the shortfall continues. The
accountability brief states: "The social protection floor shortfall is projected to
drive child malnutrition above warning threshold by step 2 — the specific outcome
the programme commitment was designed to prevent."

**Exit criteria (acceptance test):** "Can the tool reproduce a committed programme
baseline from programme document inputs? Can the user run a second scenario with
observed (lower) spending and compare the divergence from the committed baseline?
Does the divergence comparison identify specific indicator threshold crossings at
the observed spending level that are avoided at the committed level? Is the
plain-language summary legible to a community organization audience? Note: this
acceptance test is partially forward-looking — integrated observed-actuals input
is a roadmap item; the current acceptance criterion is met if the two-scenario
comparison (committed vs. observed spending level) produces the required divergence
output."

---

### Persona 4V Marquee Case — The Wardha Divergence

*Backtesting stress test for WorldSim's agricultural income transmission chain.
Development Economist validates: the causal mechanism (AGMARK cotton price →
farm gate revenue → household debt service → food expenditure reduction) is
established in the literature (Nagaraj et al. 2014, JNU Agrarian Research Group;
Mishra 2008, EPW). NSSO Agricultural Household Survey 2013 and 2019 provide the
comparison dataset. Historical grounding confirmed.*

**Persona:** 4 Variant — The Personal-Connection Researcher

**The room:** CDS Thiruvananthapuram, March 2022. India's three farm laws were
repealed in November 2021 following a 13-month farmers' protest. Priya is writing
a journal article on whether the farm laws' projected deregulation effects would
have matched the income and food security trajectory that Vidarbha cotton farmers
actually experienced during the protest period (November 2020 – November 2021).
She wants to use WorldSim to model the projected trajectory and compare it to her
field data.

**What they had:** NSSO Agricultural Household Survey 2013 and 2019 data; AGMARK
historical cotton price series for Wardha district 2015-2021; her own dissertation
field survey (47 households, Wardha district, 2015); published literature on
agricultural income volatility in Maharashtra.

**What they lacked:** A simulation framework modeling the specific transmission
chain: cotton AGMARK price → farm gate revenue → debt service capacity → household
food expenditure reduction, under market deregulation conditions. Standard
macroeconomic models do not capture this chain at the household level. The farm
law scenario requires a policy input (removal of MSP price floor guarantee)
propagating through the agricultural income chain to human development indicators.

**The decision made:** (Prospective) If the simulation's projected trajectory under
market deregulation matches the income and food security pattern in her field data,
WorldSim has validated its agricultural transmission chain for this use case. If
it diverges, the specific assumption causing the divergence becomes the journal
article's finding: "WorldSim's model underestimates [X] because [Y] assumption
does not capture [Z] mechanism."

**The consequence:** Either outcome is valuable: confirmation validates the tool for
agricultural economics research; divergence identifies a calibration gap that the
tool's documentation should disclose. The exercise is adversarial review as
epistemic contribution — the same discipline that makes backtesting the primary
signal for model improvement.

**The WorldSim intervention:** Priya runs the India agricultural scenario with farm
law deregulation as the policy input — removal of the MSP price floor modeled as
a price floor removal affecting cotton farm gate revenue for 2 steps. The
simulation produces: projected cotton farm income trajectory; household food
expenditure; child nutrition indicator. She downloads the trajectory and compares
it to her Wardha field data: simulation predicts 18% income decline at step 1;
her 2021 field follow-up shows 23% decline. Divergence: 5 percentage points. The
tool discloses the assumption: "Wardha district-specific data not available;
estimate derived from Maharashtra agricultural comparables." The confidence tier
system shows the simulation estimate is Tier 3 (SYNTHETIC_COMPARABLE). Her field
data for those 47 households is Tier 2 for those households, Tier 4 for regional
inference. They are roughly comparable in credibility for this data point. Priya
accepts the divergence as within the plausible range for district-level vs.
regional estimation. She cites the simulation with the appropriate qualification
in the journal data appendix.

**Exit criteria (acceptance test):** "Does the simulation model an agricultural
price floor removal and propagate it through farm income to food security human
development indicators with step-level output? Does the backtesting divergence
table show predicted vs. observed income trajectory for cotton farmers, with the
specific comparison group disclosed? Can the trajectory data be exported in a
format suitable for a journal data appendix? When the user has district-level
field data that diverges from the simulation's regional estimate by 5 percentage
points, does the tool correctly disclose the comparison group and confidence tier
such that the divergence is interpretable rather than opaque?"

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

---

## Section 7 — Persona Conflict Resolution

> **Authored by:** Business PO  
> **Date:** 2026-06-09  
> **Phase 0 context:** Output 2 of Phase 0 — closes gap XD-1 (founding document north star figure vs. UX north star canonical user conflict, unreconciled)  
> **Status:** Authoritative ruling — applies at ADR authorship time and at sprint review time  
> **Cross-references:** `docs/process/design/process-redesign-phase0-persona-traceability-spec.md`, `docs/ux/north-star.md §The Canonical User`

### The Conflict Being Resolved

The founding document's north star test names "a finance minister of a small, vulnerable country sitting across from an IMF negotiating team" as the reference figure. This is **Persona 5** — Aicha Mbaye, IMF Executive Board Member / Institutional Decision-Maker.

The UX north star names "a debt restructuring specialist at a finance ministry" as the canonical user. This is **Persona 2** — Eleni Papadimitriou, Deputy Director, Ministry of Finance, Finance Ministry Negotiator.

When ADR authorship panels, UX design decisions, and sprint reviews face a choice where serving one persona well means serving the other less well, the question has been resolved differently in different sessions — whichever persona was more convenient for the capability being built. Gap XD-1 names this as a root cause of inconsistent design direction.

This section is the authoritative resolution. It governs any future decision where the two personas' requirements conflict.

---

### The Resolution

#### The personas play different roles in the tool's mission — they are not design competitors

Persona 5 (finance minister) is the **mission beneficiary and north star validation reference**. She is not the operational user of the tool. She benefits when Persona 2 can use the tool effectively on her behalf. The founding document's north star test — "does this make the tool more useful to that person in that moment?" — uses Persona 5 as the evaluation frame, not as the design subject.

Persona 2 (specialist) is the **primary design subject**. She operates the tool. She is in the negotiation room with a tablet. She prepared the analysis the night before. She is citing the finding. The instrument cluster, the information hierarchy, the time constraints, and the alert specificity are all designed for her operational requirements.

This distinction resolves most apparent conflicts before they become genuine design choices: capabilities designed for Persona 2's operational needs automatically serve Persona 5's mission needs through Persona 2's work.

#### When genuine conflict exists: the priority hierarchy

Genuine persona conflict occurs at specific design choices where Persona 2's operational requirement and Persona 5's orientation or trust requirement cannot both be satisfied simultaneously. The three classes of genuine conflict are:

**Class A — Alert panel information density:** Persona 2 needs full citation-quality specificity (indicator, step, cohort, severity, causal attribution). Persona 5 needs a signal-level read (severity direction, plain-language implication) without cognitive overload in a 5-minute demonstration context.

**Ruling on Class A:** Persona 2's citation-quality requirements govern alert panel design. Persona 5's orientation requirement is satisfied by the severity label and indicator name being legible at a glance — which Persona 2's design already requires. The alert panel carries the full information Persona 2 needs; a cold reader (Persona 5) can orient from severity and indicator name alone without processing the full row. No sacrifice of Persona 2's requirements is warranted.

**Class B — Zone 1 primary viewport display:** Persona 2 needs the primary viewport to support her most demanding active-query task in Reactive state. Persona 5 needs to orient to Zone 1 within 60 seconds without prior tool training (Journey D cold-reader requirement).

**Ruling on Class B:** Persona 2's operational requirements govern Zone 1 layout and instrument content. A floor constraint applies: every Zone 1 element must carry a self-describing label and visual treatment that allows a cold observer to read it correctly with one explanatory sentence from a driver. This floor is not a Persona 5 concession at Persona 2's expense — it is a legibility standard that serves both. A Zone 1 element that requires prior training to interpret has also failed Persona 2's criterion for communicating findings to counterparties who were not briefed. The floor and the operational requirement are not in conflict.

**Class C — Uncertainty disclosure format and depth:** Persona 5 in a demonstrative context needs compressed disclosure that fits within a one-sentence finding without triggering confusion. Persona 2 needs sufficient disclosure depth to cite with epistemic precision. (Full resolution in UX Designer Step 2 Tension 1 ruling: confidence tier parenthetical — "(Tier 2 — World Bank WDI)" — satisfies both within the one-sentence finding format.)

**Ruling on Class C:** The Step 2 parenthetical format is adopted as the standard for uncertainty disclosure in compressed contexts. For Tier 3 data, the word "synthetic" must appear verbatim in the parenthetical regardless of which persona is the primary audience. Persona 5's comfort with the disclosure is not a reason to omit or soften it.

#### The north star test reference

The founding document's north star test continues to use Persona 5 as the evaluation reference:

> "Does this decision make the tool more useful to a finance minister sitting across from an IMF negotiating team, in that moment?"

This is the test applied in the Phase 0 exit artifact's north star validation question, in sprint review sign-offs, and in ADR acceptance (Element P-7 of the persona trace). Persona 5 is the north star test reference. Persona 2 is the primary design subject. These are two distinct roles, and both are required.

An ADR or sprint deliverable that serves Persona 2 well (operational, fast, citation-complete) but cannot pass the Persona 5 north star test ("does this help the minister?") has identified a capability that may be technically correct but mission-misaligned. The converse is also true: a deliverable that passes the Persona 5 test aspirationally but is inoperable for Persona 2 in Reactive state has built for the wrong subject.

---

### Priority Summary Table

| Decision domain | Governs | Hard floor |
|---|---|---|
| Zone 1 layout and instrument content | Persona 2 (operational requirements in Reactive state) | Zone 1 elements self-describing to cold reader in ≤1 sentence per instrument |
| Alert panel information density and specificity | Persona 2 (citation-quality requirements) | Severity label and indicator name legible at a glance without full row processing |
| Information hierarchy zone assignments | Persona 2 via `information-hierarchy.md` | HCL equal visual weight invariant (supersedes both personas — Engineering Lead exception required to modify) |
| Uncertainty disclosure format | Parenthetical format satisfies both — no conflict | "Synthetic" verbatim for Tier 3 data regardless of persona |
| Mode 3 and control plane | Persona 2 exclusively — Persona 5 has no Mode 3 journey | Not applicable |
| North star test reference | Persona 5 — the mission evaluation frame | North star test must be answered for every Tier 1 ADR (Element P-7) |

---

### What This Ruling Does Not Resolve

This ruling does not establish precedence for all nine personas in all conflict scenarios. It resolves the specific XD-1 conflict: founding document north star (Persona 5) vs. UX canonical user (Persona 2). Conflicts involving other persona pairs (e.g., Persona 3 political advisor vs. Persona 2 for Mode 1 comparative case surface; Persona 6 journalist vs. Persona 2 for plain-language alert text) are not addressed here and are left to the relevant ADR authorship panels, informed by the general principle that the tool's primary operational context is sovereign debt negotiation support and persona pairs should be resolved in that direction when in doubt.

---

### Amendment Record

| Date | Amendment | Authority |
|---|---|---|
| 2026-06-09 | Initial ruling — Phase 0 Output 2, closes gap XD-1 | Business PO (Phase 0) |
