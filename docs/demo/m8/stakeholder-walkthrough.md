# WorldSim Stakeholder Demonstration — Presenter Guide (v0.8.0 / Milestone 8)

> UX Designer Agent — Journey: Stakeholder demonstration walkthrough.
> Grounded in `docs/ux/north-star.md` §Resolved Design Questions and
> `docs/ux/user-journeys.md`. Read both documents before adapting this guide.
>
> **Version:** v0.8.0 — Milestone 8 (Ecological and Governance Frameworks)
> **Supersedes:** `docs/demo/m6/stakeholder-walkthrough.md` (v0.6.0)
> **Scenario:** Greece 2010–2015 IMF programme — six steps
>
> Target audience for the demo: non-technical stakeholders and domain experts.
> Not developers. Not data scientists.
>
> Total runtime: 20 minutes plus Q&A.

---

## Presenter Briefing — Read Before the Room Fills

### What Is New in Milestone 8

This demo represents a qualitative advance over the M6 baseline. Three things
are live for the first time:

1. **Ecological composite score** — CO2 planetary boundary proximity,
   boundary-normalized against 350 ppm (Rockström 2009). The ecological radar
   axis is no longer null. Greece's carbon trajectory is now a first-class
   measurement output.

2. **Governance honest null** — The governance axis renders a dashed hollow
   dot labeled "Governance — in validation." This is an explicit methodology
   choice: the composite score does not yet meet the five promotion criteria,
   so the tool does not display zero. Zero would imply governance failure.
   Null means the composite is not yet computed. The distinction is the point.

3. **Six-step scenario (2010–2015)** — The Greece scenario now covers the
   full six-year programme, including the 2015 capital controls. The thesis
   frame is Step 5 (2014): financial indicators show partial GDP recovery
   while human development remains at crisis depth. This asymmetry is the
   WorldSim argument.

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
   working software at v0.8.0, not a prototype. Ecological composite scores
   are live. Governance renders honest null rather than fabricated data. What
   comes next follows directly from the epistemic commitments already made.

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
Do not demo a loading screen. The scenario does not need to be pre-created —
the creation step is part of the demonstration.

Run `./scripts/demo.sh --run` to launch the stack and the Playwright walkthrough,
or `./scripts/demo.sh` to start the stack and follow the guide manually.

The sequence below is precise. Follow it exactly. Each step has a specific
cognitive purpose for the audience.

---

### Step 1 — The Map Loads

**What the audience sees:** A world map. Countries rendered as polygons. A
color gradient indicating a simulation attribute. The interface is familiar —
it looks like every geopolitical visualization tool they have seen.

**What the presenter says:**

> This is the baseline view. Each country shows a simulation attribute across
> entities. Click any country to open its analysis panel. What makes this
> different from a data visualization tool will become clear in a moment.

**Key M8 note:** The attribute selector switches to `gdp_growth` after Step 1
completes, so the choropleth shows simulation output rather than seed data.

**Cognitive purpose:** Orient. Establish that this is an interactive, not a
static display. Avoid spending time here — the map is familiar territory and
earns nothing on its own.

---

### Step 2 — Create the Greece 2010–2015 M8 Demo Scenario

**What the audience sees:** The scenario creation panel. Presenter enters
"Greece 2010-2015 M8 Demo" and creates it. The scenario appears in the scenario
list. The presenter selects it as the primary.

**What the presenter says:**

> We are modelling Greece's 2010–2015 IMF programme — six years of fiscal
> conditionality. The programme conditions are the inputs. The simulation
> produces the consequences. Each step here is one year.
>
> The reason we are starting with a historical case is important — we know what
> happened. The backtesting discipline, which we will return to, is how we
> validate that the simulation captures real causal dynamics.

**Cognitive purpose:** Establish that scenarios are structured, not arbitrary.
Conditionality terms are the inputs. The simulation produces the consequences.

---

### Step 3 — Advance Through Six Steps

**What the audience sees:** The presenter clicks Next Step six times. The step
counter increments: 1/6 → 2/6 → 3/6 → 4/6 → 5/6 → 6/6. The choropleth
updates at each step.

**What the presenter says:**

> Each step is one year. Watch Greece shift in the choropleth as the fiscal
> contraction accumulates across steps. What the choropleth shows is the central
> simulation value — the full analysis is in the entity panel.

**Cognitive purpose:** Show time progression. Establish that the simulation
runs sequentially through a programme horizon. Make the step counter legible
to the audience.

---

### Step 4 — Click Greece — Drawer Opens (Step 4, Year 2013)

**What the audience sees:** The EntityDetailDrawer slides open. This step is
specifically chosen for Step 4 (2013) — the year of the third memorandum and
the primary surplus conditionality target.

**What the presenter says:**

> This panel is the primary analytical surface. Step 4 is 2013 — the year the
> programme required Greece to achieve a primary surplus for the first time.
> What the simulation shows is not whether the surplus was achieved, but what
> else happened in the same year. Watch the indicators below.

**Pause. Let them read the MDA alert panel first.**

> These are the Minimum Descent Altitude alerts. In aviation, an MDA is the
> floor below which an aircraft cannot safely descend given the terrain.
> In this simulation, MDAs are human cost floors — levels below which
> consequences become irreversible, or where standard policy frameworks no
> longer provide protection.
>
> What you are reading is not a warning about the model's uncertainty. It is
> a finding about where this path takes the population.

**Cognitive purpose:** Introduce the primary visual element. The alert is the
first thing the canonical user reads. It must be the first thing the audience
hears explained. The 2013 step anchors the narration to a historical fact the
domain economists in the room will recognize.

---

### Step 5 — MDA Alerts and Thesis Frame (Step 5, Year 2014)

**What the audience sees:** The presenter navigates to Step 5 (2014). The
EntityDetailDrawer shows the asymmetric radar: financial axis extending from
the Step 3 nadir, human development axis still near maximum compression.

**What the presenter says:**

> Step 5 is 2014. In the historical record, Greece's GDP grew 0.7 percent —
> a financial recovery. But unemployment was still 26.5 percent.
>
> Look at the radar: the financial axis is extending as the model registers
> partial recovery. The human development axis remains near its most depressed
> point. This asymmetry is the WorldSim argument in a single image.
>
> Financial recovery and human recovery are not the same event. No
> single-axis measurement tool can show you both simultaneously.

**Call out a specific MDA alert:**

> Read this alert as a piece of evidence: the indicator, the step at which
> the threshold was crossed, the severity level, and the affected cohort.
> That sentence is specific enough to cite in a negotiation. A finding you
> can cite is a finding you can use.

**Cognitive purpose:** The thesis frame is the M8 centrepiece. The asymmetric
radar is not a secondary detail — it is the argument. The MDA alert grounds
the radar in a specific, nameable consequence. Together they produce the
negotiating posture: "Under this path, these thresholds were crossed. Here
is the evidence."

---

### Step 6 — Radar Chart (Ecological Live, Governance Honest Null)

**What the audience sees:** The presenter scrolls to the Multi-Framework
Overview radar chart in the drawer. Three axes are live with data; one axis
(Governance) renders as a dashed hollow dot.

**What the presenter says:**

> Four axes: financial, human development, ecological, governance. Financial
> and human development are live — those are the two contracted axes you saw
> in the thesis frame.
>
> Ecological is now live as of Milestone 8: CO2 planetary boundary proximity,
> boundary-normalized against 350 ppm. A value above 1.0 means the boundary
> is exceeded. This is a first-class measurement output — ecological
> consequences are no longer a footnote.
>
> Governance shows as a dashed axis, labeled 'Governance — in validation.'
> It renders honest null — not zero. Zero would imply governance failure.
> Null means the composite score is not yet computed to the standard required
> for publication. The four-axis architecture is here. The fourth axis will
> show composite scores when the promotion criteria are met at Milestone 9.

**Cognitive purpose:** Introduce the multi-framework measurement principle.
The ecological live score and the governance honest null are both M8 claims —
one about capability, one about epistemic integrity. Both need to land as
deliberate choices, not gaps.

---

### Step 7 — Compare Mode

**What the audience sees:** The presenter creates a second scenario and
activates compare mode. The DeltaChoropleth shows where the two paths diverge
geographically.

**What the presenter says:**

> This is the counter-proposal function. Once you have identified which terms
> produce threshold crossings, you model an alternative — the same fiscal
> outcome, achieved differently. The DeltaChoropleth shows where the two
> scenarios diverge.
>
> The argument becomes: this path crosses the threshold. This alternative
> achieves the same primary fiscal objective and does not. Here is the
> evidence for both.

**Cognitive purpose:** Complete the preparation journey. The tool is not only
a diagnostic — it produces the counter-proposal as an analytical output. That
is what closes the capability gap in a live negotiation.

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
> each milestone extending what can be seen.

### Milestone 6 and Milestone 7 — Foundation (Complete)

> Milestones 6 and 7 established the technical foundation: compliance
> framework clean, legibility baseline measured and documented, the backtesting
> suite covering five historical cases. These were not features — they were
> discipline. A simulation that produces outputs without a clean bill of
> methodological health is a tool that cannot be trusted in the setting it
> is designed for.

### Milestone 8 — Ecological and Governance Frameworks (Complete — Current Version)

> Milestone 8 delivers what you have seen in this demonstration: the ecological
> composite score live for the first time (CO2 planetary boundary proximity,
> Rockström 2009 reference), the governance axis rendering honest null rather
> than fabricated zero, and the Greece scenario extended to 2015 — six steps
> covering the full programme duration including capital controls.
>
> The four-axis radar chart is now a substantive instrument, not a placeholder.
> Three axes carry live composite scores. The fourth will follow when its
> promotion criteria are met.

### Milestone 9 — Standards Foundation (Next)

> Milestone 9 formalizes the Governance Module promotion path: five promotion
> criteria, currently unmet, targeted for M9 delivery. The milestone also
> covers the canonical unit registry, field-level data certification, WGI
> source documentation, and the beginning of the methodology publication
> preparation. When governance meets its promotion criteria, the fourth radar
> axis moves from dashed null to a live composite score.

### Milestone 10 and Beyond

> Mean-reversion channels, magnitude calibration, political economy and
> conditionality modeling, analyst tooling — each building on the validated
> foundation. Milestone 13 targets methodology publication and Technical
> Steering Committee formation: domain experts in sovereign debt, ecological
> economics, and governance reviewing the methodology and contributing to
> calibration.
>
> Frame this as expanding capability, not missing features. The capability
> that exists today is the capability that has been validated. What comes
> next is what the backtesting evidence and the epistemic commitments already
> made require.

---

## Section 5 — Q&A Preparation

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
> is a build failure.
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

### "Why is governance shown as dashed and labeled 'in validation'? Is that a bug?" *(M8-specific)*

> No — it is a deliberate methodology decision. The governance composite score
> has five promotion criteria that must be met before the tool publishes a score:
> source certification, fidelity validation, territorial coverage threshold, blind
> audit score, and domain expert review. All five are currently unmet.
>
> The alternative was to display zero, or to interpolate a value from partial
> data. We chose not to. Zero implies governance failure. An interpolated value
> implies precision we do not have. The dashed axis and the "in validation" label
> tell the user exactly what the tool knows and does not know about this dimension.
>
> That epistemic honesty is not a concession — it is the methodology claim. A
> tool that fabricates data to complete a display is a tool you cannot trust
> with the findings you actually have. The fourth axis will show a composite
> score when it has earned the right to show one.

---

## Section 6 — Honest Disclosures (available if asked)

These statements must be available if questions arise. Do not proactively
volunteer them in the main presentation unless a direct question requires it.
Frame them as evidence that the tool's epistemic honesty is working.

- **Distributions are pre-calibration.** Uncertainty bands reflect a reasonable
  range of model outcomes, not empirically calibrated confidence intervals.
  Disclosed in the interface and in the methodology documentation.

- **Ecological composite score is CO2-only for Greece at M8.** The ecological
  module covers CO2 planetary boundary proximity against the Rockström 2009
  reference (350 ppm). Additional planetary boundary indicators (biodiversity,
  nitrogen, water) are framework scope for future milestones.

- **Governance composite score is null at M8.** Five promotion criteria not yet
  met. The governance axis renders honest null — dashed, labeled "in validation"
  — not zero. Composite score targeted for M9 delivery.

- **GDP step 5 recovery is not reproduced.** The MacroeconomicModule has no
  endogenous recovery mechanism. Historical step 5 shows +0.7% GDP growth
  (partial recovery); the simulation produces a continued contraction at that
  step. This is a documented blind spot tracked in Issue #221
  (mean-reversion channel, M9 scope). The DIRECTION_ONLY fidelity threshold
  for step 5 is deferred pending that fix.

- **PMM Zone 1 widget is a placeholder at M8.** The Policy Maneuver Margin
  indicator renders a null placeholder. Full composite widget is M9 scope.

- **This tool is not for financial advantage or surveillance.** The canonical
  user is a finance ministry counterpart in a negotiation. The tool does not
  assist in executing financial attacks, identifying exploitable vulnerabilities
  in adversaries, or any use case that amplifies power asymmetries against
  vulnerable actors.

---

## Section 7 — The North Star (1 minute)

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

## Timing Reference

| Section | Content | Time |
|---|---|---|
| Presenter setup | Stack running, map loaded | Before room fills |
| Section 1 | Problem framing | 3 min |
| Section 2 | Live application (7 steps) | 5 min |
| Section 3 | Backtesting credibility | 5 min |
| Section 4 | Roadmap | 5 min |
| Section 7 | North Star closing | 1 min |
| Q&A | See prepared responses above | Remaining time |

Total structured content: 19 minutes. Leave at least 10 minutes for Q&A.
The Q&A is where domain economists will engage most seriously — do not compress it.

---

## Screenshot Reference (M8 Demo Frames)

Captured: 2026-05-18. Located in `docs/demo/m8/screenshots/`.

| Presentation order | File | Step | Drawer state | Caption |
|---|---|---|---|---|
| 1 — Thesis | `frame-c-step5-divergence.png` | 5 / 6 | Open — Human Development tab | 2014: financial partial recovery, human development at crisis depth — the asymmetry is the argument |
| 2 — Instrument | `frame-a-step1-instrument.png` | 1 / 6 | Open — default view | Greece at IMF program entry: reserve coverage below the critical floor before the first package lands |
| 3 — Collapse | `frame-b-step3-collapse.png` | 3 / 6 | Open — Financial tab | Three rounds of consolidation produce simultaneous deterioration across all live frameworks |
| 4 — Evidence | `frame-d-step3-evidence.png` | 3 / 6 | Open — MDA panel | Threshold breaches rendered as structured evidence — specific enough to cite across a negotiating table |
| 5 — Planetary | `frame-e-step3-ecological.png` | 3 / 6 | Open — Ecological tab | Milestone 8: planetary boundary proximity tracking live for the first time |

See `docs/demo/m8/screenshot-brief.md` for the full UX Agent brief and frame-by-frame specifications.
See `docs/demo/m8/reviews/2026-05-18-v0.8.0-stakeholder-review.md` for the IR Agent review of these frames.
