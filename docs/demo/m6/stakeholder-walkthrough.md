# WorldSim Stakeholder Demonstration — Presenter Guide

> UX Designer Agent — Journey: Stakeholder demonstration walkthrough.
> Grounded in `docs/ux/north-star.md` §Resolved Design Questions and
> `docs/ux/user-journeys.md`. Read both documents before adapting this guide.
>
> Target audience for the demo: non-technical stakeholders and domain experts.
> Not developers. Not data scientists.
>
> Total runtime: 20 minutes plus Q&A.

---

## Presenter Briefing — Read Before the Room Fills

### Who Is in the Room

Assume a mixed audience. The technical sophistication varies and does not matter.
What matters is that everyone in the room understands power asymmetry in
consequential negotiations and has a stake in correcting it.

The likely profiles:

- **Domain economists and policy analysts** — comfortable with fiscal multipliers,
  debt sustainability, and conditionality frameworks. They will engage on the
  methodology. They are the ones who will push back hardest and, if convinced,
  become the most valuable advocates.

- **Programme directors and ministry officials** — understand the negotiating
  context intuitively. They need to see a tool that fits into the workflow they
  already have, not a new discipline to learn. For them, speed and clarity are
  the test.

- **Potential funders or institutional partners** — evaluating whether this project
  is worth supporting. They need to understand the mission, see evidence that the
  technical implementation is credible, and leave with a clear sense of what
  makes this different from existing tools.

The presentation serves all three audiences simultaneously. The live application
sequence serves the policy analysts. The backtesting argument serves the
economists. The North Star closing serves the funders. Keep all three in view.

### What They Need to Leave Believing

Three things, in priority order:

1. **The capability gap is real and consequential.** Finance ministries in
   vulnerable countries currently lack the analytical infrastructure that
   sophisticated institutional actors bring to the table. This is not a
   complaint — it is a structural condition that affects negotiating outcomes.
   WorldSim is a direct response to that gap.

2. **The model is disciplined, not aspirational.** Backtesting against five
   historical crises with documented fidelity thresholds and explicit blind
   spot disclosure is evidence of methodological seriousness. The model knows
   what it does not know. That is a harder standard to meet than simply
   producing plausible-looking outputs.

3. **The roadmap is coherent and sequenced correctly.** What exists today is
   working software, not a prototype. What comes next (uncertainty
   visualization, ecological and governance composite scores) follows directly
   from the epistemic commitments already made. The trajectory is legible.

### Honest Disclosure Required

Do not oversell the current state. The following are honest statements that
must be available if questions arise:

- The simulation produces distributions, not predictions. Uncertainty bands
  are currently pre-calibration — meaning they reflect a reasonable range
  of model outcomes, not empirically calibrated confidence intervals. This
  is disclosed in the interface and in the methodology documentation.

- The ecological and governance composite scores are currently null in
  scenario outputs. The modules exist (GovernanceModule ships in M6) but
  the axes are not yet integrated into the radar chart display. These are
  live scores in M8.

- Fidelity thresholds at this milestone are DIRECTION_ONLY for all five
  backtesting cases. The model gets the direction right. Magnitude
  calibration is the next validation layer.

- The canonical user is a finance ministry counterpart in a negotiation.
  The tool is not designed for real-time trading, surveillance, or any
  use case involving financial advantage over the actors it is designed
  to assist.

If any of these disclosures become a problem in the room, they are not problems
with the tool — they are evidence that the tool's epistemic honesty is working.

---

## Section 1 — The Problem (3 minutes)

### What the Presenter Says

> When the IMF or World Bank walks into a negotiation, they bring an institution.
> They have programme economists who have modelled this exact country for years.
> They have historical precedent databases. They have scenario analysis capacity
> built up over decades, refined by hundreds of programme outcomes. They have
> seen this before, or something close enough to it that the pattern recognition
> is there.
>
> The finance ministry on the other side of the table is starting from a
> different position. Their team is smaller. Their analytical infrastructure is
> thinner. They may have excellent economists — but those economists are also
> managing a budget process, a parliamentary reporting requirement, and three
> other crises at the same time. The asymmetry is not in intent. It is in
> infrastructure.
>
> What that asymmetry produces, in practice, is a gap in the quality of
> scenario analysis available to each party. The IMF team can model what
> happens to the fiscal path if growth comes in 1.5 points below projection.
> The ministry team is more likely to be working from the IMF's own model
> outputs, evaluated against their own economic judgment. That judgment is
> often good. But it is not the same as running the analysis yourself against
> your own assumptions.
>
> WorldSim is an attempt to close that gap. Not to give the ministry team the
> same institution — that is not possible in a software tool. But to give them
> the same quality of scenario analysis: historical pattern recognition,
> human cost consequence modeling, distributional outputs rather than point
> estimates. Analytical capability that currently costs what sophisticated
> institutional infrastructure costs, made available as open-source software
> that runs on a laptop.

### What This Establishes

This framing — capability analysis, not alarm — follows directly from
north-star.md §Resolved Design Question 3. The human cost ledger is what
the path does to the people the ministry serves. It is an asset in the
negotiation, not a constraint on the ministry's own choices.

Do not use warning language here. Do not say "dangerous" or "alarming" or
"crisis." The human cost ledger shows consequences. The finance minister
reads those consequences as evidence. Evidence is power.

---

## Section 2 — Live Application (5 minutes)

### Setup

The application should be running and the map loaded before the session starts.
Do not demo a loading screen. The Greece 2010 backtesting scenario should be
pre-created so that the "create scenario" step is demonstrating the interface,
not waiting on a database write.

The sequence below is precise. Follow it exactly. Each step has a specific
cognitive purpose for the audience.

---

### Step 1 — The Map Loads

**What the audience sees:** A world map. Countries rendered as polygons. A
color gradient indicating an attribute value. The interface is familiar —
it looks like every geopolitical visualization tool they have seen.

**What the presenter says:**

> This is the application's baseline view. The choropleth shows a simulation
> attribute across entities — in this case, GDP growth rate from the most
> recent completed scenario step. Each country is colored by its simulated
> value. Click any country to open its analysis panel.
>
> What makes this different from a data visualization tool will become clear
> in a moment.

**Cognitive purpose:** Orient. Establish that this is an interactive, not a
static display. Avoid spending time here — the map is familiar territory and
earns nothing on its own.

---

### Step 2 — Create the Greece 2010 Scenario

**What the audience sees:** The scenario creation panel. Presenter selects
entity "GRC", sets n_steps to 3, and confirms. The scenario appears in the
scenario list with status "pending."

**What the presenter says:**

> We're going to model Greece's 2010–2012 fiscal adjustment programme. This is
> a historical case — we know what happened. In the simulation, we'll inject
> the IMF programme conditions as scheduled inputs: the fiscal tightening, the
> emergency declarations, the structural conditionality. Then we advance the
> scenario step by step and observe what the model produces.
>
> The reason we're starting with a historical case rather than a hypothetical
> is important. It's the point of the backtesting discipline, which we'll come
> back to.

**Cognitive purpose:** Establish that scenarios are structured, not arbitrary.
Conditionality terms are the inputs. The simulation produces the consequences.
The causal arrow is explicit.

---

### Step 3 — Advance to Step 3

**What the audience sees:** The presenter clicks the Advance button three times
(or uses the run button for the full scenario). The step counter increments:
Step 1 / 3 → Step 2 / 3 → Step 3 / 3. The choropleth updates at each step.
Greece shifts color.

**What the presenter says:**

> Each step here is one year. We're advancing through 2010, 2011, 2012 — the
> three years of the initial programme. At each step, the simulation applies
> the scheduled inputs and propagates their effects through the model's
> relationship graph. You can see Greece shift in the choropleth as the
> fiscal contraction accumulates across steps.
>
> What the choropleth is showing is the point estimate — the central value of
> the distribution. The full picture is in the entity panel.

**Cognitive purpose:** Show time progression. Establish that the simulation
runs sequentially through a programme horizon, not all at once. The choropleth
update makes the progression visible.

---

### Step 4 — Click Greece, Drawer Opens

**What the audience sees:** The EntityDetailDrawer slides open. The panel
shows Greece's simulation state at Step 3. The MDA alert panel is at the top.
Below it, the radar chart. Below that, framework-specific indicators with
confidence tiers.

**What the presenter says:**

> This panel is the primary analytical surface. What I want to draw your
> attention to first is the top of the panel.

**Pause. Let them read it.**

> These are the Minimum Descent Altitude alerts. The terminology comes from
> aviation: an MDA is the altitude below which an aircraft cannot safely
> descend given the terrain. In this simulation, MDAs are human cost floors —
> levels below which consequences become irreversible, or where standard policy
> frameworks no longer provide protection.
>
> The alert fires when the simulation determines that an indicator has crossed
> one of those floors. What you're reading is not a warning about the model's
> own uncertainty. It is a finding about where the proposed path takes the
> population.

**Cognitive purpose:** Introduce the primary visual element (per north-star.md
§Resolved Design Question 1: MDA alert panel is primary). The alert is the
first thing the canonical user reads. It must be the first thing the audience
hears explained.

---

### Step 5 — Call Out the MDA Alert Panel

**What the audience sees:** The presenter highlights a specific alert —
for example, a CRITICAL severity alert on unemployment or poverty headcount
at step 3.

**What the presenter says:**

> Read this alert as a piece of evidence: "Under this fiscal adjustment path,
> [indicator] crosses the critical threshold at programme year 3. This affects
> primarily [cohort]." That sentence is the analytical finding. It is specific
> enough to cite in a negotiation. It names an indicator, a step, a severity
> level, and a population cohort.
>
> This is what 'capability analysis' means in practice. The finance ministry
> specialist is not being alarmed by the simulation. She is being handed a
> finding that she can use. Her argument at the negotiating table becomes:
> "Under this path, poverty headcount crosses the critical threshold in year
> three. In comparable historical cases — which we can show you — that level
> of deterioration produced programme collapse. Here is the evidence."
>
> The simulation gives her the analytical standing to make that argument
> specifically, not generally.

**Cognitive purpose:** Translate the UI into the use case. The audience
understands negotiating contexts. Connect the visual output to the human
situation it serves.

---

### Step 6 — Radar Chart as Secondary

**What the audience sees:** The presenter scrolls down to the radar chart,
which shows four axes: financial, human development, ecological, governance.

**What the presenter says:**

> Below the alert panel is the radar chart — four axes, one for each
> measurement framework the simulation tracks. Financial indicators: fiscal
> balance, GDP trajectory. Human development: poverty headcount, health system
> capacity. Ecological: currently null — that module ships in Milestone 8.
> Governance: institutional quality indicators, now live as of this milestone.
>
> The radar chart tells you which dimensions are under stress, which supports
> the threshold scan the alert panel just completed. If the financial axis
> shows deterioration but the human development axis is flat, the programme
> may be fiscally painful without being humanly catastrophic. If both collapse
> simultaneously, the analysis changes.
>
> I'll be honest about what is not on the screen yet: the ecological and
> governance axes are showing preliminary values. They will show composite
> scores in M8. What you see now is the architecture for a four-framework
> assessment, with two frameworks producing full composite outputs today.

**Cognitive purpose:** Show the radar chart as the framework overview (per
north-star.md: secondary to the alert panel). Introduce the multi-currency
measurement principle. Be transparent about what is null.

---

### Step 7 — Enter Compare Mode

**What the audience sees:** The presenter opens compare mode and selects a
second scenario — either a pre-created alternative with softer conditionality
terms, or a demonstration of the DeltaChoropleth showing divergence between
the two.

**What the presenter says:**

> This is the counter-proposal function. Once you have identified which terms
> produce threshold crossings, you model an alternative — the same fiscal
> outcome, achieved differently. The DeltaChoropleth shows you, geographically,
> where the two scenarios diverge. The entity drawer in compare mode lets you
> read the divergence at the indicator level.
>
> The argument becomes: "This path crosses the threshold. This alternative
> path achieves the same primary fiscal objective and does not. Here is the
> evidence for both."

**Cognitive purpose:** Complete the preparation journey (per user-journeys.md
Journey A Step 6). The tool is not just a diagnostic — it produces the
counter-proposal as an analytical output.

---

## Section 3 — Backtesting Credibility (5 minutes)

### The IMF Multiplier Error

> In 2013, Olivier Blanchard and Daniel Leigh — the IMF's chief economist and
> a senior economist in the Research Department — published a paper that became
> one of the more uncomfortable self-assessments any major institution has
> produced.
>
> The paper examined the fiscal multipliers the IMF had been using in its
> programme designs during the 2010–2012 European austerity period. A fiscal
> multiplier is the relationship between a unit of government spending cuts and
> the resulting change in output. If the multiplier is 0.5, cutting spending
> by 1 percentage point of GDP reduces GDP by half a point. The IMF's programme
> forecasts were built on multipliers around that range.
>
> The empirical evidence, once Blanchard and Leigh examined it, showed that
> the actual multipliers in the European austerity cases were roughly 1.5 —
> three times what the programmes had assumed. A one-point spending cut was
> contracting GDP by one and a half points, not half a point. The programmes
> produced significantly more economic damage than their models predicted,
> which required further fiscal tightening to hit primary balance targets,
> which contracted GDP further, in a compounding cycle.
>
> This is not a criticism of the IMF. It is an illustration of the epistemic
> problem: model assumptions embedded in consequential decisions are not
> always visible to the parties most affected by those decisions. The finance
> ministry sitting across the table did not have a mechanism to interrogate
> the multiplier assumption and produce its own analysis. The IMF was using a
> model that turned out to be systematically wrong in a predictable direction,
> and no counterpart had the tools to surface that.
>
> Backtesting discipline is one response to that problem. You run your model
> against historical cases where the outcomes are known. You measure the gap
> between what your model produces and what actually happened. You document
> where the model is right, where it is wrong, and why. You ship that
> documentation alongside your outputs.

### The Five Cases

> WorldSim has been validated against five historical crisis cases. Each one
> was selected because it represents a distinct crisis mechanism — not the same
> failure mode five times.
>
> **Greece 2010–2012** — a fiscal consolidation programme under external
> conditionality. GDP contracted for three consecutive years. The simulation
> correctly predicts contraction at each step and the direction of unemployment
> movement.
>
> **Argentina 2001–2002** — sovereign default and currency crisis following
> a convertibility peg. A different mechanism from Greece: the binding constraint
> was not fiscal space but monetary credibility. The simulation captures the
> contractionary dynamics.
>
> **Lebanon 2019–2020** — a compound crisis: a banking system collapse that
> became a currency crisis that became a sovereign debt crisis, with the
> Beirut port explosion as a compounding shock in year two. Lebanon is the
> cascade case — multiple systems failing simultaneously and interacting. The
> simulation correctly predicts contraction at both steps.
>
> **Thailand 1997–2000** — the Asian financial crisis. An externally triggered
> currency speculative attack that produced domestic balance-sheet deterioration.
> The mechanism is different from all three prior cases: externally induced
> contagion, not domestically generated stress. The simulation captures
> contraction in both crisis years.
>
> **Ecuador 1999–2000** — the dollarization case. Ecuador entered a banking
> collapse and hyperinflation in 1999, then replaced its national currency with
> the US dollar in January 2000. GDP contracted -6.3% in 1999 and recovered
> +2.8% in 2000. This is the first case with a recovery at step two — it tests
> whether the simulation can distinguish stabilization dynamics from continued
> deterioration. The fidelity threshold for step two is not 'predict
> contraction' but 'do not predict deeper contraction than step one.' The model
> passes. The recovery itself is a documented blind spot: dollarization
> stabilization and oil price recovery are not yet modeled.

### What DIRECTION_ONLY Means in Plain Language

> The current fidelity threshold type is called DIRECTION_ONLY. In plain
> language: the model is being tested on whether it gets the sign right.
> Did GDP go down or up? Did unemployment rise or fall? It is a binary test.
>
> The model passes DIRECTION_ONLY on all five cases. That is a meaningful
> result — a model that randomly produced outputs would pass roughly 50% of
> binary sign tests. Consistent directional accuracy across five distinct
> crisis mechanisms and ten sign checks is evidence that the model is capturing
> real causal dynamics.
>
> What DIRECTION_ONLY does not validate is magnitude. The model may predict
> -1.5% GDP when the historical outturn was -6.3%. Both pass DIRECTION_ONLY.
> Magnitude calibration — DISTRIBUTION_COMBINED thresholds — is the next
> validation layer. We are working toward it. We are not claiming it yet.
>
> This is the discipline: document what the model has been shown to get right.
> Document what has not been validated. Ship both.

### Why Backtesting Discipline Matters

> Every analytical tool used in consequential decisions should be held to
> backtesting discipline. The IMF's multiplier error was not a failure of
> intent — it was a failure to run their model against historical outcomes
> with sufficient rigor before embedding it in programme design. The lesson
> is not that the IMF was wrong. The lesson is that any model, used without
> systematic comparison to historical evidence, will accumulate hidden error.
>
> For a tool designed to give finance ministries analytical standing in
> negotiations, epistemic honesty is not optional. A ministry official who
> cites a finding from this simulation in a negotiation is staking their
> credibility on it. The tool must be able to tell her what it has and has
> not been shown to do.

---

## Section 4 — What Is Being Built (5 minutes)

> The roadmap is best understood as a sequence of expanding analytical capability —
> each milestone extending what can be seen, not filling in what was missing.

### Milestone 7 — Uncertainty Visualization

> The simulation currently produces distributions with pre-calibration bands.
> The bands are visible in the interface but not yet calibrated against
> historical variance. Milestone 7 delivers the uncertainty visualization that
> makes those bands meaningful: band widths proportional to projection horizon,
> alert source distinction between distribution-triggered and point-estimate-
> triggered findings, and the non-suppressible pre-calibration disclosure
> integrated into the alert language.
>
> What this changes in practice: a finance ministry specialist will be able to
> say not just "the central estimate shows a year-3 breach" but "the
> distribution places 80% probability mass below the threshold at year 3, even
> accounting for model uncertainty." That is a materially stronger finding.

### Milestone 8 — Ecological and Governance Composite Scores

> The radar chart currently has four axes. Two produce full composite outputs
> today: financial and human development. Two are emerging: ecological and
> governance.
>
> Milestone 8 completes all four. The ecological module will surface planetary
> boundary proximity, natural capital depletion, and agricultural stress indices
> — dimensions that are systematically absent from IMF programme analysis but
> that directly affect the long-term sustainability of fiscal consolidation
> paths. A programme that achieves primary balance by reducing agricultural
> investment in a climate-stressed agricultural economy is producing a different
> risk profile than one that achieves the same balance through administrative
> efficiency gains.
>
> The governance module — which ships its first indicators this milestone —
> will surface rule-of-law degradation and democratic quality erosion as
> programme consequences. These are not peripheral concerns. An adjustment
> programme that stabilizes fiscal accounts while undermining institutional
> quality is producing a different trajectory than a programme that preserves
> both. The four-axis radar chart makes that comparison visible.
>
> Also in Milestone 8: the causal meta-map — a visualization of the causal
> relationships the simulation is modeling, so that any user (or reviewer)
> can inspect the assumption embedded in every output. The model's theory of
> the world is not hidden in source code. It is displayed alongside the output.

### Milestone 9 — Methodology Publication and External Validation

> The final piece of the current roadmap is methodology publication and the
> formation of a Technical Steering Committee. Every assumption the simulation
> makes — every elasticity, every multiplier, every threshold value — will be
> published with source citations and open to external challenge. Domain experts
> in sovereign debt, ecological economics, and governance will review the
> methodology and contribute to calibration.
>
> This is what 'open source as strategy' means in practice. The tool's
> credibility does not rest on the authority of its producers. It rests on
> the transparency of its methodology and the quality of its backtesting
> evidence. Anyone can inspect, challenge, and improve the assumptions.
> That is the standard the tool is designed to meet.

---

## Section 5 — The North Star (1 minute)

> I want to close with the reason this project exists, stated as plainly as
> possible.
>
> There is a quinoa farmer in Bolivia who will never know this tool exists.
> He does not have internet access reliable enough to open a web application.
> He does not speak the language the interface is written in. He has no idea
> what an IMF programme is, or what a fiscal multiplier means, or why it
> matters.
>
> His government might know. If his government has a finance minister with
> better analytical tools, that minister can negotiate better terms. Better
> terms produce different fiscal paths. Different fiscal paths produce
> different human consequences.
>
> The quinoa farmer lives at the end of that chain. Every decision we make
> about this tool — what to build first, what to be honest about, what not
> to oversell — we make as if he is watching. Not because he is. But because
> that framing is the right discipline.
>
> Build it as if he does.

---

## Section 6 — Q&A Preparation

### "Why not use existing IMF tools? They already have analytical infrastructure."

> The IMF's analytical tools are built for the IMF's analytical tasks. They
> are excellent at what they are designed to do. The capability gap we are
> addressing is not that the IMF's tools are bad — it is that they belong to
> the IMF.
>
> When a finance ministry uses the IMF's projections as its primary analytical
> input, it is evaluating conditionality terms against the model that produced
> those terms. That is a structural problem regardless of the quality of the
> model. The ministry needs its own analytical infrastructure — one that runs
> on its own assumptions and surfaces its own findings, which it can then
> compare to what the IMF is showing.
>
> This tool does not compete with IMF methodology. It gives the ministry team
> a mechanism to interrogate it.

### "How do you validate the model?"

> Backtesting against historical cases with documented fidelity thresholds.
> Five crisis cases covering five distinct crisis mechanisms. Explicit
> separation between what has been validated (DIRECTION_ONLY: the sign of
> directional change) and what has not (magnitude calibration). Documented
> blind spots for each case — the things the model did not capture and why.
>
> The validation architecture is transparent by design. Every fidelity
> threshold is registered in the database with its source citation. Every
> backtesting test is in the public repository and runs in CI — a failure
> is a build failure. The methodology will be published with source citations
> and submitted to external domain expert review at Milestone 9.
>
> What we cannot claim: that the model is calibrated to produce
> quantitatively accurate magnitude estimates. That is the next validation
> layer. We are working toward it and will not claim it before we have evidence.

### "Who is this for?"

> The primary user is a debt restructuring specialist at a finance ministry
> in a developing or emerging market economy — specifically, one that
> encounters IMF or World Bank programmes as negotiating counterparts rather
> than as programme designers. They have graduate-level economics training.
> They are not data scientists. They need to reach an analytically defensible
> conclusion in minutes, not hours, under cognitive load.
>
> Secondary users: independent economists and civil society analysts who
> want to evaluate programme conditionality against human cost consequences
> that official programme documents do not surface. Third: journalists and
> accountability institutions who need an accessible mechanism to interrogate
> what a proposed programme actually does to a population.
>
> What this tool is not for: sovereign wealth fund analysis, trading strategy,
> sanctions design, or any use case in which the analytical advantage runs
> against vulnerable actors rather than toward them.

### "What does it cost to run?"

> The software is open source and free to use. The infrastructure requirements
> are a PostgreSQL database and a Python runtime — both available on commodity
> cloud hardware at negligible cost for a single ministry's analytical load.
> The application is designed to run on a machine with 8GB of RAM. It does not
> require paid APIs, licensed datasets, or proprietary services.
>
> All data sources used in the simulation and backtesting are open-licensed:
> IMF World Economic Outlook, World Bank World Development Indicators, Natural
> Earth boundary data. The methodology documentation will be available under
> the same license as the software.
>
> The Equitable Build Process principle embedded in the project's architecture
> documents is not incidental. A tool designed to level the playing field for
> resource-constrained actors must not reproduce the resource asymmetry it is
> designed to counter in its own infrastructure requirements.

---

## Timing Reference

| Section | Content | Time |
|---|---|---|
| Presenter setup | Map loaded, Greece scenario pre-created | Before room fills |
| Section 1 | Problem framing | 3 min |
| Section 2 | Live application sequence (7 steps) | 5 min |
| Section 3 | Backtesting credibility | 5 min |
| Section 4 | Roadmap | 5 min |
| Section 5 | North Star closing | 1 min |
| Q&A | See prepared responses above | Remaining time |

Total structured content: 19 minutes. Leave at least 10 minutes for Q&A.
The Q&A is where domain economists will engage most seriously — do not compress it.
