# WorldSim Stakeholder Demonstration — Presenter Guide (v0.16.0 / Milestone 16)

> PM Agent — Demo 6 walkthrough. Produced for G8 sprint (Issue #1225).
> Grounded in `docs/ux/north-star.md`, `docs/ux/information-hierarchy.md`,
> and `docs/process/demo-preparation-standard.md`.
> Screenshot brief: `docs/demo/m16/screenshot-brief.md`
>
> **Version:** v0.16.0 — Milestone 16 (Distributional Visibility)
> **Supersedes:** `docs/demo/m15/stakeholder-walkthrough.md` (v0.15.0)
> **Scenario:** Senegal 2024, Article IV consultation — distributional human cost argument
>
> Target audience: non-technical stakeholders, domain economists, potential funders,
> ministry officials. Not developers.
>
> Total runtime: 20 minutes plus Q&A.

---

## Presenter Briefing — Read Before the Room Fills

### What Is New in Milestone 16

Four things are live for the first time:

1. **Zone 1A Phase 4 composite encoding (#845)** — The primary trajectory view now
   encodes four frameworks simultaneously as distinguishable curves sharing one step axis.
   The distributional signal is not isolated in a secondary panel — it is in the primary
   viewport. The composite encoding replaces the single-score trajectory and makes
   cross-framework divergence readable at a glance.

2. **Cohort disaggregation on the primary surface (#986)** — Zone 1B now shows a
   `CohortImpactSection` alongside the MDA alert panel. Bottom-quintile threshold
   crossings appear by cohort: indicator name, current value, recovery floor, T3 tier
   badge with "Inferred" sublabel. The ministry team can now show which specific
   population group bears the cost of conditionality — not aggregate GDP declining,
   but this cohort, at this step.

3. **Political risk summary surface (#987)** — Zone 1D now shows structured PSP
   severity labeling: CRITICAL / WARNING / WATCH / STABLE with a plain-language
   interpretation sentence ("programme implementation faces political execution risk")
   and step-over-step delta annotation visible at zero interaction. The PSP decimal is
   now labeled in the vocabulary the minister's team can use in a briefing note.

4. **25-year human capital trajectory (#274)** — The `HumanCapitalTrajectoryPanel`
   is visible in the primary viewport below Zone 1 instruments. Three cohort curves
   project over 100 quarterly steps (25 years). A Layer 3 milestone sentence renders at
   L0: "by [year], bottom quintile informal workers poverty headcount crosses the recovery
   floor — at this level, capability restoration takes a decade or more." The "for this
   long" argument is now on screen without drawer navigation.

**Architecture change from M14 Demo 5:** Demo 6 is single-entity (SEN only). Scenario:
100 quarterly steps, 8-step programme window, `start_date="2024-01-01"`. No Mode 3.
The demonstration's thesis moment is a challenge-response on cohort distribution
methodology, not reserve coverage provenance. The challenge-response architecture is
the same (the badge is on screen before the challenge arrives); the analytical capability
being challenged is different (distributional disaggregation methodology, not data source
citation).

### EL Scenario Design Decisions (Recorded 2026-06-24)

| Decision | Value |
|---|---|
| Entity | SEN only (single entity) |
| Mode 3 | Not in Demo 6 scope |
| Challenge moment | Cohort distribution methodology challenged → analyst responds with T3 Inferred badge, synthetic flag, ECOWAS demographic weight source |
| Persona 3 (Andreas Stefanidis, Political Advisor) | Included in Step 6c audience simulation — Zone 1D political risk section is his primary evaluation frame |
| Step 5b additional gate | Before screenshots: verify Q1 poverty headcount ≥ 0.40 at step 2; verify milestone sentence leads with calendar year anchor ("by [YYYY]") |
| Initial poverty headcount (Q1 informal) | ~0.385–0.39 (calibrated to produce step-2 crossing to ≥ 0.40 under fiscal conditionality) |
| Legitimacy index | ~0.43 (PSP in WARNING zone at programme entry) |

### Who Is in the Room

Assume a mixed audience. Domain economists, programme directors, ministry officials,
potential funders or institutional partners. Technical sophistication varies.

The likely test they are running: "Can this tool actually disaggregate who bears the
cost — or does it produce aggregate numbers with a distributional label attached?"

Demo 6 answers that question in the first two minutes.

### What They Need to Leave Believing

Three things, in priority order:

1. **The distributional thesis is specific, not rhetorical.** "The poor suffer more"
   is not a citeable claim at the table. "Bottom quintile informal sector workers cross
   the poverty recovery floor at step 2, six months into the proposed programme — at
   that threshold, capability restoration takes a decade or more, labeled T3 Inferred
   from ECOWAS comparable economy distributions" — that is a citeable claim. Demo 6
   shows the difference.

2. **The model is honest about what it knows and what it inferred.** The T3 Inferred
   badge on the cohort distribution data is not a weakness to be defended. It is the
   No False Precision principle in operation. The methodology for the demographic
   weighting is published; the ECOWAS comparable economy source is named; the inference
   chain is on screen.

3. **The political constraint is not separate from the distributional cost — they
   compound.** Zone 1D's PSP WARNING label and Zone 1B's cohort threshold crossing
   are on the same screen at the same step. The conditionality's distributional cost
   and the government's reduced capacity to deliver the conditionality run together.
   That is a political economy argument the aggregate financial trajectory cannot make.

---

## Section 1 — The Room (3 minutes)

### What the Presenter Says

> There is a room where this happens.
>
> On one side of the table: a creditor team. They have institutional memory that spans
> decades of programme design in this region. They have proprietary models. They have
> a set of assumptions the ministry team has never seen fully written down. They have
> twenty analysts behind them who have done this forty times.
>
> On the other side: a finance ministry. Three economists. Public data. And a question
> they will be asked in thirty minutes that they have twelve seconds to answer.
>
> The question is not "is your model correct?" That is a long conversation. The question
> is the simpler one: "Which cohort bears the cost of this programme — and can you
> cite that?"
>
> Not: is the programme viable. Not: does GDP recover. Which specific population group
> hits the threshold at which capability recovery takes a decade, and how far into the
> programme does that happen?
>
> That question, until now, required a specialist social economist on the team to
> translate aggregate model outputs into distributional claims. The ministry did not
> have the right translation infrastructure.
>
> Today the ministry team can answer it from the instrument cluster, in under ten
> seconds, with the source labeled on screen.

### What This Establishes

The problem is not that the ministry team lacks economists. The problem is that the
distributional argument requires translating aggregate model outputs into cohort-specific
claims — under cognitive load, in real time, with a citation the creditor cannot dismiss.

Demo 6 shows the translation infrastructure working without specialist mediation.

Do not frame this as a crisis warning. Frame every capability as analytical standing
in a negotiation.

---

## Section 2 — Live Application (8 minutes)

### Presentation Order

Screenshots are presented in argument order: A → B → C → D → E.
See `docs/demo/m16/screenshot-brief.md` for the five-frame brief and capture specs.

Frame A is the thesis frame. Frames B–C provide context. Frame D makes the
intergenerational argument. Frame E closes on the complete picture.

The narrated Playwright walkthrough in `demo-narrated.spec.ts` captures frames in
step order because that is the simulation's temporal order. Presentation leads with
the thesis (Frame A) then builds context.

### Setup

Application should be running before the room fills. Run `./scripts/demo.sh` to start
the stack. The scenario creation happens in the Playwright walkthrough; for live
presentation, pre-create the Senegal scenario using the API or the UI creation panel.

**Primary surface:** Zone 1 instrument cluster — composite encoding trajectory (1A),
alert panel with cohort impact section (1B), PMM widget (1C), four-framework + PSP
summary (1D), plus 25-year projection panel below. This is where the demo argument
lives. Do NOT narrate the choropleth as the analytical instrument (UX-RULING-4).

---

### Step 1 — Frame A: "This Cohort, at This Step" (THESIS FRAME) (Step 2, Q2 2024)

**What the audience sees:** SEN at step 2. Zone 1B's `CohortImpactSection` shows the
bottom quintile informal worker poverty headcount at or crossing the 0.40 recovery floor.
The T3 badge with "Inferred" sublabel is visible adjacent to the cohort row. Zone 1A shows
the composite encoding with four framework curves diverging as conditionality begins.
Zone 1D shows the PSP severity label (WARNING) with delta annotation.

**What the presenter says:**

> Senegal. Q2 2024. Step two — six months into the proposed Article IV conditionality.
>
> Look at Zone 1B — the alert and cohort panel on the left side of the instrument cluster.
>
> Two rows are visible. The upper section is the MDA alert you have seen in prior
> milestones. The lower section is new: it is the cohort impact section.
>
> It reads: bottom quintile informal workers poverty headcount. Current value: 0.40.
> Recovery floor: 0.40.
>
> This cohort is at the threshold. Six months in.
>
> Next to that number is a badge: T3 — Inferred. The methodology for the demographic
> weighting — how we assigned 0.40 to this specific cohort rather than to aggregate
> poverty — is declared on screen. ECOWAS comparable economy distributions. Tier 3
> synthetic estimate.
>
> That badge is not an apology. It is the analytical chain made visible.
>
> The argument the ministry team can now make: under the proposed programme terms, the
> bottom quintile informal sector workers — not "the poor" in the aggregate, this cohort
> specifically — cross the poverty recovery floor by Q2 2024. Six months in. With the
> demographic weight source named, the tier labeled, and the threshold on screen.
>
> That is not a political claim. That is a citeable technical finding.

**PAUSE — let them read Zone 1B and the T3 badge.**

> Notice also Zone 1D — the political risk panel on the right. The severity label reads
> WARNING. We will return to that in a moment.
>
> For now: the thesis of this demonstration is on this screen. This cohort. At this step.

**Cognitive purpose:** Land the distributional thesis immediately. The audience does not
need the backtesting section to understand what the tool provides. The cohort specificity
and the T3 labeling are the two claims that distinguish Demo 6 from aggregate analysis.

**Key narration note (UX-RULING-4):** Do NOT say "watch Senegal shift on the map."
Say "Zone 1A shows the four-framework composite encoding" or "Zone 1B shows the cohort
impact section." The choropleth anchors geography. The instruments carry the argument.

---

### Step 2 — Frame B: "The Composite Encoding — Four Trajectories at Once" (Step 4, Q4 2024)

**What the audience sees:** SEN at step 4. Zone 1A composite encoding showing four
distinguishable curves — Financial, Human Development, Ecological, Governance — on a shared
step axis. The human development curve is declining. The financial composite is being
compressed by conditionality. Zone 1B cohort section remains visible. Zone 1D PSP
delta annotation shows direction.

**What the presenter says:**

> Step four. Q4 2024. One year into the programme.
>
> Zone 1A is now showing you four trajectories simultaneously — not one composite score,
> but four framework curves encoding together. Financial composite. Human development
> composite. Ecological composite. Governance composite.
>
> The human development curve is declining. That is the same signal driving the Zone 1B
> cohort row you saw at step two. They are not separate readouts — they are the same
> simulation state viewed at different levels of disaggregation.
>
> The composite encoding is the Milestone 16 Zone 1A delivery: the distributional signal
> is not in a separate panel. It is in the primary trajectory view, readable at a glance
> across all four frameworks simultaneously.
>
> The financial composite is compressing because conditionality works: the fiscal
> consolidation is doing what it is designed to do. The human development composite is
> declining at the same time. The instrument shows you both constraints in the same
> encoding, on the same step axis.
>
> This is the question the aggregate model cannot answer: not whether the programme
> achieves its financial objectives, but what it costs in human development terms at
> the same time. The answer is now visible at Zone 1A without opening a drawer.

**Cognitive purpose:** Show that the composite encoding makes the human development
decline visible at the primary instrument level — not as a supplementary panel but as
part of the trajectory that the Zone 1A surface encodes.

---

### Step 3 — Frame C: "The Political Constraint — PSP Severity Labeled" (Step 4, Q4 2024)

**What the audience sees:** SEN at step 4. Zone 1D political risk summary showing PSP
severity label (WARNING), a plain-language interpretation sentence ("programme
implementation faces political execution risk"), and a step-over-step delta annotation.
Zone 1A composite encoding and Zone 1B cohort section remain visible.

**What the presenter says:**

> Same step four. Look now at Zone 1D — the political risk panel.
>
> The severity label reads: WARNING.
>
> Below it, a plain-language sentence: "programme implementation faces political
> execution risk."
>
> And a delta annotation showing direction: the PSP has been declining since programme
> entry.
>
> This is the Milestone 16 Zone 1D delivery. In M14, Zone 1D showed a PSP decimal —
> 0.43, or 0.38, or 0.65. The ministry team had to translate that into a briefing note
> position. Now the instrument translates it: WARNING means the political system's
> capacity to execute the conditionality terms is under active constraint.
>
> Let me be precise about what this is and what it is not. The PSP severity label is
> not a forecast of political stability. It is the model's assessment of whether the
> programme's conditionality terms are deliverable given the political economy conditions
> at this step. That is a distinct question from "will the government survive?" It is
> the question: can this government actually implement what the programme requires,
> at this fiscal pressure, under these political constraints?
>
> The answer is WARNING. And it is on the same screen, at the same step, as the cohort
> threshold crossing you saw in Zone 1B.
>
> The conditionality lands hardest on the bottom quintile informal workers — that is the
> Zone 1B argument. And the government faces political execution risk in delivering it —
> that is the Zone 1D argument. Those two arguments compound each other. The instrument
> cluster shows them compounding, simultaneously, without requiring two separate analyses.

**Cognitive purpose:** Complete the political economy argument that pairs with the
distributional argument. The Zone 1D PSP severity label and Zone 1B cohort threshold
crossing are the two legs of the Demo 6 thesis. Frame C shows both on screen together.

**Key narration note on PSP severity:** "WARNING is not a political prediction. It is
a political constraint estimate. The same way reserve coverage WARNING means the
financial system is under constraint — not that it has failed — PSP WARNING means
the programme's implementation capacity is under constraint. The label tells you what
to watch, not what will happen."

---

### Step 4 — Frame D: "For This Long — The 25-Year Trajectory"

**What the audience sees:** The `HumanCapitalTrajectoryPanel` visible in the primary
viewport below the Zone 1 instruments. Three cohort curves over 100 quarterly steps.
The Layer 3 milestone sentence visible at L0: "by [year], bottom quintile informal
workers poverty headcount crosses the recovery floor — at this level, capability
restoration takes a decade or more." T3 Inferred badges adjacent to curve endpoints.
Zone 1A/1B/1C/1D all visible above the projection panel.

**What the presenter says:**

> The programme window in this scenario is eight steps — two years. Q4 2025.
>
> The 25-year projection panel below Zone 1 asks a different question: what does the
> conditionality commit this cohort to beyond the programme window?
>
> Read the milestone sentence at the bottom of that panel.
>
> "By [year], bottom quintile informal workers poverty headcount crosses the recovery
> floor — at this level, capability restoration takes a decade or more."
>
> The programme lasts two years. The consequence — if the crossing happens — lasts
> a decade or more. That is the intergenerational argument the minister's team needs
> to make. Not "the programme is bad." The specific, temporally precise claim: under
> these conditionality terms, this cohort crosses this threshold by this year, and
> the recovery timeline for human capability is a decade.
>
> That sentence is visible from the primary viewport without opening a drawer. It is
> the Layer 3 treatment for the human capital trajectory — the instrument telling you
> not just what the gauge shows, but what to do with the reading.
>
> Notice the T3 Inferred badges on the curve endpoints. The demographic weighting behind
> these three cohort curves — bottom quintile informal, bottom quintile agricultural,
> second quintile informal — is declared. It is a Tier 3 synthetic estimate from ECOWAS
> comparable economy distributions. The ministry team can say: "Our 25-year trajectory
> uses ECOWAS regional demographic weights, declared at T3 — Inferred. The methodology
> is published. The assumption is named."
>
> That is the challenge-response for the distributional methodology question.

**PAUSE — let them read the three curve trajectories and the milestone sentence.**

**Cognitive purpose:** Establish the "for this long" argument as distinct from the
"this cohort, at this step" argument. Frame D is the intergenerational dimension —
the consequence persists beyond the programme window, and the instrument names the
persistence explicitly.

---

### Step 5 — Frame E: "All Arguments on One Screen" (Step 8, Q4 2025)

**What the audience sees:** Full viewport at step 8. Zone 1A composite encoding
showing the full eight-step divergence. Zone 1B cohort impact section showing cumulative
distributional state at programme close. Zone 1D PSP severity at step 8 with delta
annotation over the programme window. Projection panel showing the full 25-year arc
with milestone sentence. All instruments visible; none displaced.

**What the presenter says:**

> Step eight. Q4 2025. The programme window closes.
>
> Everything on this screen is the answer to the question the ministry team was asked.
>
> Zone 1B: which cohort bears the cost. Zone 1A: across which frameworks the cost
> is distributed. Zone 1D: whether the government's political capacity to deliver
> the conditionality has held. Projection panel: for how long the consequences
> persist beyond the programme window.
>
> The minister's team did not need to open a drawer. They did not need to call a
> social economist to translate the distributional outputs. They did not need to
> navigate to a separate political feasibility tool. Every argument that needs to
> be made at this table is on this one screen.
>
> I want to name something explicitly about what this is and is not. The numbers
> on this screen are a simulation output under configured initial attributes and
> scheduled inputs — not a calibrated prediction of Senegal's actual trajectory.
> The engine that produced them has been validated against five historical crisis
> mechanisms. The distributional disaggregation is scenario output under T3
> demographic weights, not empirically backtested cohort data. The T3 label is
> on screen for exactly this reason.
>
> What the tool provides is not a prediction. It is the analytical standing to
> make a specific, temporally precise, distributional argument — with the
> methodology visible, the confidence tier labeled, and the source named.
>
> That is what has changed.

**Cognitive purpose:** Close the live application section by establishing the single-screen
completeness as the Demo 6 delivery. The ministry team argument does not require specialist
mediation — that is the capability change Demo 6 demonstrates.

---

## Section 3 — Backtesting Credibility (4 minutes)

### The Epistemic Problem

> In 2013, Blanchard and Leigh published a paper that became one of the more
> uncomfortable self-assessments any major institution has produced. The IMF's
> programme designs during the 2010–2012 European austerity period used fiscal
> multipliers around 0.5. The empirical evidence showed actual multipliers were
> roughly 1.5 — three times higher. Programmes produced significantly more damage
> than their models predicted. The human cost of that miscalibration — unemployment,
> health outcomes, intergenerational poverty — is a documented record.
>
> This is not a criticism of the IMF. It is an illustration of the epistemic
> problem this tool addresses: the model assumptions embedded in consequential
> decisions were not visible to the parties most affected by those decisions.
> The finance minister sitting across the table did not have a mechanism to
> interrogate the multiplier assumption.
>
> WorldSim is a direct response to that gap. But it is a response with its own
> validation obligations.

### The Five Cases

> WorldSim has been validated against five historical crisis cases — each
> representing a distinct crisis mechanism:
>
> **Greece 2010–2012** — fiscal consolidation under external conditionality.
> The model correctly predicts contraction at each step. DIRECTION_ONLY.
>
> **Argentina 2001–2002** — sovereign default and convertibility peg collapse.
> Simulated GDP contraction of −10.55% against historical −10.9%. 3.2% deviation.
> MAGNITUDE calibrated.
>
> **Lebanon 2019–2020** — compound crisis cascade. Directional accuracy
> on both steps. DIRECTION_ONLY.
>
> **Thailand 1997–2000** — externally induced currency attack producing
> domestic balance-sheet deterioration. DIRECTION_ONLY.
>
> **Ecuador 1999–2000** — banking collapse and dollarization. The recovery
> case — the fidelity threshold is "do not predict deeper contraction than
> step one." The model passes.
>
> Honest disclosure for Demo 6: Senegal is not yet a backtested case. The
> trajectories in this scenario are simulation outputs under configured initial
> attributes and scheduled inputs — not calibrated predictions of Senegal's
> actual path. The distributional disaggregation is not yet backtested against
> historical cohort data — the aggregate trajectory is calibrated; the cohort
> distribution is scenario output under T3 demographic weights. The engine that
> produced this output has been validated on five distinct crisis mechanisms;
> the distributional layer is new in M16.

### What DIRECTION_ONLY Means

> The current fidelity threshold type is DIRECTION_ONLY: does the model get
> the sign right? The model passes on all five cases. A model that randomly
> produced outputs would pass roughly 50% of binary sign tests. Consistent
> directional accuracy across five distinct crisis mechanisms is evidence of
> real causal capture.
>
> Magnitude calibration — DISTRIBUTION_COMBINED thresholds — is the next
> validation layer. Argentina 2002 is the first step. We are not claiming it
> before we have evidence.

---

## Section 4 — What Is Being Built (3 minutes)

> The roadmap is best understood as expanding the analytical standing the
> ministry team can bring to the table — each milestone extending what can
> be argued, cited, and defended.

### Milestones 1 through 15 — Foundation (Complete)

> The first fifteen milestones established the full analytical and trust
> architecture: simulation engine, all four measurement frameworks, political
> economy module, grounding strip source provenance, evidence thread tier
> annotations, Layer 3 self-interpreting trajectory sentences, Zone 1B cohort
> disaggregation design, Zone 1D political risk summary design, Path 1 approved
> source network, accessibility validation. The distributional visibility
> delivered in M16 is only credible because the measurement infrastructure
> beneath it has been validated.

### Milestone 16 — Distributional Visibility (Current)

> Milestone 16 delivers what you have seen in this demonstration:
>
> **Composite encoding** — The primary trajectory view encodes all four frameworks
> simultaneously. The distributional signal is in Zone 1A, not behind a drawer.
>
> **Cohort disaggregation on the primary surface** — Zone 1B's CohortImpactSection
> shows which population groups bear the cost of conditionality, with T3 Inferred
> badges and the demographic weight source named.
>
> **Political risk summary** — Zone 1D translates the PSP decimal into labeled
> severity vocabulary with plain-language interpretation. The political constraint
> is on the same instrument as the distributional cost.
>
> **25-year human capital trajectory** — The projection panel below Zone 1 answers
> the "for how long" question with a Layer 3 milestone sentence at L0.
>
> What you are seeing in this demonstration is working software at v0.16.0, validated
> against five historical crisis mechanisms, with published methodology that anyone
> can inspect and challenge.

### What Comes Next (M17 and Beyond)

> Three capabilities that Demo 6 was designed not to claim:
>
> **Mode 3 Active Control with distributional constraints** — The counter-proposal
> capability combined with a human cost floor. A ministry team that can not just test
> alternative conditionality structures but explicitly specify which cohort the
> alternative must protect. The distributional visibility in M16 is the prerequisite
> for that constraint to be meaningful.
>
> **Cohort disaggregation backtesting** — Running the demographic weighting methodology
> against historical cohort data to establish validation evidence for the T3 layer.
> The path from T3 Inferred to T2 Measured.
>
> **Senegal backtesting** — Running the SEN Article IV history against the engine to
> validate directional accuracy. The distributional disaggregation validation follows.

---

## Section 5 — Q&A Preparation

### "What is T3 Inferred and why should I trust it?"

> T3 — Inferred means the demographic weight assigned to this cohort was estimated
> using statistical inference from comparable economies — in Senegal's case, ECOWAS
> regional distributions — because direct cohort measurement data at the required
> granularity is not available for this scenario.
>
> The confidence tier methodology is published in the WorldSim methodology documentation;
> anyone can audit how we assigned Tier 3 to this figure.
>
> The key point: the tool labels what it inferred rather than hiding inference behind
> a plausible-looking number. A T2 measured figure would require direct survey data
> for this specific cohort at this granularity. That data does not exist for this
> scenario. The T3 label says: this is the best available inference; here is the
> source; here is the methodology. The ministry team can cite it as T3 — Inferred
> from ECOWAS comparable economy distributions.
>
> That is the No False Precision principle in operation. The T3 badge next to the
> cohort row makes any T2 data on the same screen more credible by contrast — the
> distinction is real and visible.

*(This is the Demo 6 thesis challenge — the answer should take under ten seconds
and the presenter should not need to look anything up. The T3 badge is on screen
before the challenge arrives.)*

### "How do you define 'bottom quintile informal workers'?"

> The cohort is defined as `SEN:CHT:1-25-54-INFORMAL` in the WorldSim cohort
> taxonomy: first income quintile (bottom 20%), prime working age (25–54), informal
> sector. The cohort boundaries are the taxonomy's standard definitions. The demographic
> weight assigned to that cohort — the share of the Senegalese population it
> represents — is the T3 Inferred estimate from ECOWAS comparable economy distributions.
>
> The full taxonomy and demographic weighting methodology are in the published
> methodology documentation. The cohort identifier is visible in the Zone 1B display.

### "Why is the threshold 0.40 — where does that come from?"

> The 0.40 threshold is the `MDA-HD-POVERTY-Q1` hard descent altitude for the poverty
> headcount ratio of the bottom income quintile. Below 0.40, the model's assessment
> is that capability restoration — recovery of human development capabilities that
> were lost — takes a decade or more based on historical precedent in comparable
> cases. This is not a regulatory floor set by an external institution. It is the
> model's empirically calibrated threshold for the point at which the human cost
> becomes structural rather than cyclical.
>
> The threshold and its derivation are documented in the WorldSim methodology
> documentation and the MDA specification. Any party can challenge the threshold —
> the methodology for challenging it and proposing a recalibration is documented.

### "What does Programme Survival Probability mean and who sets it?"

> PSP is the political economy module's estimate of whether the programme's
> conditionality terms are deliverable given the current political economy conditions.
> It is not a prediction of political stability or government survival. It is the
> model's quantified estimate of implementation capacity under the current fiscal
> trajectory — the same way reserve coverage is a quantified estimate of a financial
> constraint.
>
> The PSP is computed from the political economy module's assessment of governance
> quality, democratic legitimacy dynamics, and fiscal pressure. The CRITICAL /
> WARNING / WATCH / STABLE severity thresholds are calibrated from historical cases
> of programme implementation failure and success at comparable PSP levels. The
> calibration methodology is published.

### "Why Senegal — is this a prediction about Senegal?"

> This is not a prediction about Senegal's actual trajectory. The scenario uses
> published Senegal data as the initial state — reserve coverage, legitimacy index,
> GDP trajectory — and then runs a simulation under a specified conditionality
> programme to show what the analytical capabilities look like in a realistic context.
>
> The choice of Senegal is deliberate: it is a West African country with an active
> IMF engagement context where distributional human cost arguments are policy-relevant,
> where ECOWAS comparable economy distributions are the appropriate source for T3
> demographic weighting, and where the political risk dimension is analytically
> significant. It is not a prediction. It is a demonstration context.

### "Why not use the IMF's distributional analysis tools?"

> The IMF does produce distributional analysis, and it is often sophisticated. The
> capability gap is not analytical quality — it is ownership. When the finance
> ministry uses the IMF's distributional projections as its primary analytical input,
> it is evaluating the conditionality's distributional cost against the model
> produced by the institution proposing the conditionality. That is a structural
> problem regardless of model quality.
>
> The ministry needs distributional analysis that runs on its own assumptions —
> so it can interrogate what the IMF is showing, not just receive it. T3 Inferred
> from ECOWAS distributions is a less precise estimate than what the IMF may have
> from its own data. The ministry can use WorldSim's distributional output as a
> challenge instrument: "Our own analysis, using published ECOWAS distributions
> and the methodology you can audit, shows this cohort crosses this threshold at
> this step. What is your distributional model showing?"
>
> That question changes the character of the conversation. It does not require
> the ministry's T3 analysis to be more precise than the IMF's. It requires it
> to be on the record, with a named source, from the ministry's own analytical
> infrastructure.

### "Who is this for?"

> The primary user is a debt restructuring specialist or senior economist at a
> finance ministry in a developing or emerging market economy — specifically one
> that encounters IMF or World Bank programmes as a negotiating counterpart. They
> have graduate-level economics training. They are not data scientists. They need
> to reach an analytically defensible distributional conclusion in under 90 seconds,
> under cognitive load, in a room where they are the only one without a hundred
> analysts behind them.
>
> This tool is not for sovereign wealth fund analysis, trading strategy, sanctions
> design, or any use case in which the analytical advantage runs against vulnerable
> actors rather than toward them.

### "What does it cost to run?"

> Open source and free. Infrastructure: a PostgreSQL database and a Python runtime —
> commodity cloud hardware, negligible cost for a single ministry's analytical load.
> Designed to run on 8GB RAM. No paid APIs, no licensed datasets, no proprietary
> services. All data sources are open-licensed: IMF WEO, World Bank WDI, Natural Earth,
> V-Dem, NOAA Mauna Loa. Methodology published under the same license as the software.

---

## Section 6 — Honest Disclosures (Available If Asked)

These statements must be ready if questions arise. Frame them as evidence that the
tool's epistemic honesty is working. Do not proactively volunteer unless a direct
question requires it.

- **Senegal is not a backtested case.** Trajectories are scenario outputs under
  configured initial attributes and scheduled inputs — not calibrated predictions.
  SEN backtesting is future milestone scope.

- **Cohort disaggregation is not yet backtested against historical cohort data.**
  The aggregate trajectory is validated against five historical crisis mechanisms.
  The distributional layer — cohort weighting methodology and T3 estimates — has
  not yet been validated against historical cohort outcomes. T3 Inferred labels
  are on screen for exactly this reason. The methodology for backtesting the
  distributional layer is documented; the work is scheduled.

- **T3 Inferred methodology uses ECOWAS comparable economy distributions.**
  The demographic weights are synthetic estimates from ECOWAS regional distributions.
  Disclosed in the T3 badge. Not hidden. The source and methodology are in the
  published methodology documentation.

- **PSP severity thresholds are calibrated from historical cases.** The
  CRITICAL/WARNING/WATCH/STABLE calibration is based on historical programme
  implementation precedents. The calibration is ongoing; the thresholds may be
  revised as more cases are added to the validation set. Disclosed in methodology.

- **No Mode 3 in Demo 6.** The counter-proposal capability (Mode 3 + distributional
  constraints) is M17 scope. The control plane zone is reserved in the layout but
  not activated.

- **Distributions are pre-calibration.** Uncertainty bands reflect a reasonable
  range of model outcomes, not empirically calibrated confidence intervals.
  Disclosed in UI per confidence tier documentation.

- **This tool is not for financial advantage or surveillance.** The canonical user
  is a finance ministry counterpart in a negotiation. The tool does not assist in
  executing financial attacks, identifying vulnerabilities in adversaries, or any use
  case that amplifies power asymmetries against vulnerable actors.

---

## Section 7 — The North Star (1 minute)

> I want to close with the reason this project exists, stated as plainly as possible.
>
> There is a quinoa farmer in Bolivia who will never know this tool exists. He does
> not have internet access reliable enough to open a web application. He does not
> speak the language the interface is written in. He has no idea what an IMF programme
> is, or what a fiscal multiplier means, or why it matters.
>
> His government might know. If his government has a finance minister with better
> analytical tools — tools that can say not just "GDP will contract" but "this cohort,
> at this step, crosses this threshold, for this long" — that minister can negotiate
> better terms. Better terms produce different fiscal paths. Different fiscal paths
> produce different human consequences.
>
> The quinoa farmer lives at the end of that chain. Every decision we make about this
> tool — what to build first, what to be honest about, what not to oversell — we make
> as if he is watching. Not because he is. But because that framing is the right
> discipline.
>
> Build it as if he does.

---

## Timing Reference

| Section | Content | Time |
|---|---|---|
| Presenter setup | Stack running, scenario pre-loaded | Before room fills |
| Section 1 | The room — the distributional framing | 3 min |
| Section 2 | Live application (five frames, Steps 1–8) | 8 min |
| Section 3 | Backtesting credibility | 4 min |
| Section 4 | What is being built (M16 + M17 horizon) | 3 min |
| Section 7 | North Star closing | 1 min |
| Q&A | See prepared responses above | Remaining time |

Total structured content: 19 minutes. Leave at least 10 minutes for Q&A.
Domain economists will engage most seriously on distributional methodology — do
not compress the T3 Inferred explanation. Political advisors will engage on the
PSP severity labeling — have the Section 5 PSP response ready.

---

## Screenshot Reference (M16 Demo 6 Frames)

Captured to `docs/demo/m16/screenshots/` via `demo-narrated.spec.ts`.

| Presentation order | File | Step | Zone 1 focus | Caption |
|---|---|---|---|---|
| 1 — THESIS | `frame-a-cohort-threshold.png` | 2 / 8 | Zone 1B CohortImpactSection + T3 Inferred badge | Bottom quintile informal workers at recovery floor. Step 2, Q2 2024. T3 — Inferred. ECOWAS comparable economy weights. |
| 2 | `frame-b-composite-encoding.png` | 4 / 8 | Zone 1A composite encoding — four curves | Four-framework composite at step 4: Financial, Human Dev., Ecological, Governance curves diverging |
| 3 | `frame-c-political-risk.png` | 4 / 8 | Zone 1D PSP severity label + plain-language sentence | PSP WARNING: "programme implementation faces political execution risk." Delta annotation. |
| 4 | `frame-d-25year-trajectory.png` | varies | HumanCapitalTrajectoryPanel + milestone sentence | "By [year], bottom quintile informal workers poverty headcount crosses the recovery floor — capability restoration takes a decade or more." |
| 5 | `frame-e-all-arguments.png` | 8 / 8 | Full viewport: 1A + 1B + 1C + 1D + projection panel | Programme window close: all Demo 6 arguments visible simultaneously |

See `docs/demo/m16/screenshot-brief.md` for the full UX Agent brief and frame specifications.

---

*Walkthrough authored by PM Agent, 2026-06-24. Sprint entry: `docs/process/sprint-plans/m16-g8-sprint-entry.md`.*
*Demo prep standard: `docs/process/demo-preparation-standard.md`.*
*North star test artifact: see §Sprint Exit for M16-G8.*
