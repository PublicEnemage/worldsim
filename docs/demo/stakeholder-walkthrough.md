# WorldSim Stakeholder Demonstration — Presenter Guide (v0.10.0 / Milestone 10)

> UX Designer Agent — Journey: Stakeholder demonstration walkthrough.
> Grounded in `docs/ux/north-star.md` §Resolved Design Questions and
> `docs/ux/information-hierarchy.md`. Read both documents before adapting this guide.
>
> **Version:** v0.10.0 — Milestone 10 (Engine Integrity and Instrument Delivery)
> **Supersedes:** `docs/demo/m8/stakeholder-walkthrough.md` (v0.8.0)
> **Scenario:** Argentina 2001–2004 sovereign default and Kirchner recovery — four steps
>
> Target audience for the demo: non-technical stakeholders and domain experts.
> Not developers. Not data scientists.
>
> Total runtime: 20 minutes plus Q&A.

---

## Presenter Briefing — Read Before the Room Fills

### What Is New in Milestone 10

Three things are live for the first time:

1. **GovernanceModule promoted — all four axes live.** The governance composite
   score meets all five ADR-005 promotion criteria. Zone 1D now renders four real
   numbers. The dashed "in validation" treatment is gone. The fourth axis is no
   longer a placeholder — it is a live measurement output derived from WGI Rule
   of Law and V-Dem Liberal Democracy Index data.

2. **PMM live computation.** Policy Manoeuvre Margin — the margin between the
   current trajectory and the nearest MDA threshold — is computed from the
   simulation state at each step. Zone 1C shows a directional signal: whether
   the fiscal path is widening or narrowing the available policy space.

3. **Argentina 2001–2002 — the second country fixture.** Demo 3 runs Argentina's
   sovereign default, convertibility collapse, and Kirchner recovery. This is
   a structurally distinct crisis mechanism from Greece (external conditionality
   vs domestic convertibility collapse). The same engine runs both. That is the
   Platform Principle — one analytical framework, different ingredients.

**Architecture change from M8:** Zone 1A (Trajectory View) is now the primary
analytical surface, not the EntityDetailDrawer radar chart. The instrument cluster
shows all four frameworks simultaneously in the primary viewport. The choropleth
(Zone 2A) is geographic context only — it is not the demo's thesis visualization.

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

### What They Need to Leave Believing

Three things, in priority order:

1. **The capability gap is real and consequential.** Finance ministries in
   vulnerable countries currently lack the analytical infrastructure that
   sophisticated institutional actors bring to the table. This is not a
   complaint — it is a structural condition that affects negotiating outcomes.
   WorldSim is a direct response to that gap.

2. **The model is disciplined, not aspirational.** Backtesting against five
   historical crises with documented fidelity thresholds and explicit blind
   spot disclosure is evidence of methodological seriousness. Argentina 2002
   is the first MAGNITUDE-validated result — the model produces a contraction
   of −10.55% against the historical −10.9%, a 3.2% deviation. That is not
   a coincidence. That is calibration evidence.

3. **The roadmap is coherent and sequenced correctly.** What exists today is
   working software at v0.10.0, not a prototype. All four analytical frameworks
   are live. The second country fixture demonstrates the Platform Principle.
   What comes next follows directly from the backtesting evidence.

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
the creation step happens in the Playwright walkthrough.

Run `./scripts/demo.sh --run` to launch the stack and the Playwright walkthrough,
or `./scripts/demo.sh` to start the stack and follow the guide manually.

The sequence below is precise. Follow it exactly. Each step has a specific
cognitive purpose for the audience.

**Primary surface:** The Zone 1 instrument cluster on the left side of the
primary viewport — four instruments always visible. This is where the demo
argument lives. The map is geographic context.

---

### Step 1 — The Map Loads

**What the audience sees:** A world map as geographic context. Countries visible
as reference polygons. On the left: the Zone 1 instrument cluster — trajectory
view, MDA alert panel, PMM widget, four-framework current position.

**What the presenter says:**

> This is the baseline view. The map provides geographic context — you can see
> where any country sits relative to its neighbours, and in a multi-entity
> scenario you can see how the analysis distributes across a region. The
> analytical instrument is the panel on the left: four instruments, always
> visible, updated with each simulation step.

**Cognitive purpose:** Orient. Establish that the primary analytical surface is
the instrument cluster, not the map. The map is a navigation aid, not the
thesis visualization.

**Key M10 note:** Do NOT narrate "watch Argentina shift in the choropleth" —
that was the M8 narration. Per UX-RULING-4, the choropleth is geographic
context. The trajectory view (Zone 1A) is now the instrument.

---

### Step 2 — Create the Argentina Demo 3 Scenario

**What the audience sees:** The scenario creation panel. The Playwright
walkthrough selects the pre-created Argentina Demo 3 scenario and activates it.
The Zone 1 instruments load with Argentina data.

**What the presenter says:**

> We are modelling Argentina's 2001 to 2002 sovereign default — four years.
> The Zero Deficit Plan: a pro-cyclical spending cut of 6.5 percent of GDP,
> imposed in July 2001. The IMF Blindaje programme. Then the default itself —
> declared in December 2001, 81.8 billion US dollars, the largest in history
> at the time. Then the Kirchner recovery.
>
> The crisis conditions are the scheduled inputs. The simulation produces the
> consequences. Each step is one year.

**Cognitive purpose:** Establish that scenarios are structured, not arbitrary.
The historical events — the programme conditions, the default, the emergency
declaration — are the inputs. What the simulation does with them is the output.

---

### Step 3 — Advance Through Four Steps

**What the audience sees:** The presenter clicks Next Step four times. The step
counter increments: 1/4 → 2/4 → 3/4 → 4/4. Zone 1A updates at each step.

**What the presenter says:**

> Each step is one year. Watch the trajectory view as the crisis arc unfolds.
> The step labels come from the historical event record: Zero Deficit Plan,
> Default, Kirchner recovery, Growth consolidation.

**Cognitive purpose:** Show time progression. Establish the four-step arc from
crisis entry to recovery. The Zone 1A trajectory curves tell the story across
steps without requiring the audience to open any additional panel.

---

### Step 4 — Step 3 — The Thesis Frame

**What the audience sees:** At Step 3 (2003 — Kirchner recovery begins), the
Zone 1A trajectory shows the financial curve rising from its step 2 trough
while the governance curve remains flat near the breach floor.

**What the presenter says:**

> Step 3 is 2003. The Kirchner recovery is beginning. Look at the trajectory view.
>
> The financial curve — the dashed line — is rising. GDP is recovering. The
> heterodox policies are working on the headline number.
>
> Now look at the governance curve. It is flat. Still in the breach zone.
>
> The emergency declaration from December 2001 — the state of siege that ran
> concurrent with the default — drove democratic quality below the analytical
> threshold. That institutional damage does not repair itself as fast as GDP
> recovers.
>
> Financial recovery and institutional recovery are not the same event. No
> single-axis measurement tool can show you both simultaneously. This one does.

**PAUSE — let them look at Zone 1B.**

---

### Step 5 — Zone 1B — MDA Alert: Governance WARNING

**What the audience sees:** Zone 1B (MDA Alert Panel) shows a governance WARNING
alert: democratic quality score at 0.665, below the MDA-GOV-DEMOCRACY-FLOOR
threshold of 0.70. Step 3. Governance framework.

**What the presenter says:**

> This is a Minimum Descent Altitude alert. In aviation, the MDA is the floor
> below which an aircraft cannot safely descend given the terrain. In this
> simulation, MDAs are analytical floors — levels below which consequences
> become structural rather than correctable.
>
> Read this alert as a sentence: democratic quality score has dropped to 0.665 —
> below the threshold of 0.70 — at step 3, under the governance framework.
>
> That sentence is specific enough to cite in a negotiation. You are not
> saying "things look bad." You are citing a finding with an indicator, a
> threshold, a step, and a framework. That is the difference between intuition
> and analytical standing.

**Cognitive purpose:** Introduce the MDA alert as citeable evidence. The format
matters: indicator / severity / step / framework. A ministry official who can
cite a specific threshold crossing has changed the character of the conversation.

---

### Step 6 — Zone 1D — Four-Framework Current Position

**What the audience sees:** Zone 1D shows all four framework rows. Ecological
and governance are live composite scores. Financial and human development show
a null treatment — not zero, but explicitly disclosed as deferred.

**What the presenter says:**

> Four axes: financial, human development, ecological, governance. At Milestone 10,
> all four are in the instrument cluster.
>
> Ecological composite: 1.07 — Argentina is 7 percent beyond the CO2 planetary
> boundary. The reference point is 1.0. Above 1.0 means the boundary is exceeded.
>
> Governance composite: 0.665 — below the MDA floor. The composite is derived from
> World Bank Governance Indicators and V-Dem Liberal Democracy Index data. This is
> not an estimate — it is a measurement strategy applied to certified source data.
>
> Financial and human development composites show as deferred. The percentile-rank
> scoring strategy requires at least two entities for a meaningful comparison.
> When you add a second country to this analysis, those composites activate.
> The limitation is disclosed in the interface. The indicators — GDP growth,
> unemployment — are live.

**Cognitive purpose:** Introduce the four-framework measurement principle. The
ecological and governance live scores and the honest null treatment for financial
and HD are all deliberate choices — each needs to land as methodology, not gap.

---

### Step 7 — Step 4 — Recovery Without Restoration

**What the audience sees:** The presenter advances to Step 4 (2004 — growth
consolidation). Zone 1A shows the full four-step arc. GDP growing at +9%.
Governance composite healing slowly — not yet at full recovery.

**What the presenter says:**

> Step 4 is 2004. GDP growing at plus 9 percent. The Kirchner recovery is entrenched.
>
> Now look at the trajectory arc as a whole: four steps, all four frameworks.
> The financial arc has recovered. The governance arc is healing — but slowly.
> Institutional recovery lags financial recovery, sometimes by years.
>
> And this is the platform principle made concrete: the same engine, the same
> instruments, the same analytical discipline that modelled Greece in 2010 to 2015
> now models Argentina from 2001 to 2004. Different crisis arc, different geopolitical
> context, same tool. A finance minister in any country facing programme conditionality
> can use this. The inputs change. The analytical framework does not.

**Cognitive purpose:** Close the live demo on the Platform Principle. This is the
most important claim for potential adopters — the tool is not built for one country
or one crisis type. It generalizes.

---

## Section 3 — Backtesting Credibility (5 minutes)

### The IMF Multiplier Error

> In 2013, Olivier Blanchard and Daniel Leigh published a paper that became one of
> the more uncomfortable self-assessments any major institution has produced.
>
> The paper examined the fiscal multipliers the IMF had been using in its programme
> designs during the 2010–2012 European austerity period. A fiscal multiplier is the
> relationship between a unit of government spending cuts and the resulting change in
> output. If the multiplier is 0.5, cutting spending by 1 percentage point of GDP
> reduces GDP by half a point. The IMF's programme forecasts were built on multipliers
> around that range.
>
> The empirical evidence showed that the actual multipliers in the European austerity
> cases were roughly 1.5 — three times what the programmes had assumed. A one-point
> spending cut was contracting GDP by one and a half points, not half a point. The
> programmes produced significantly more economic damage than their models predicted,
> which required further fiscal tightening to hit primary balance targets, which
> contracted GDP further, in a compounding cycle.
>
> This is not a criticism of the IMF. It is an illustration of the epistemic problem:
> model assumptions embedded in consequential decisions are not always visible to the
> parties most affected by those decisions. The finance ministry sitting across the
> table did not have a mechanism to interrogate the multiplier assumption. The IMF
> was using a model that turned out to be systematically wrong in a predictable
> direction, and no counterpart had the tools to surface that.

### The Five Cases

> WorldSim has been validated against five historical crisis cases. Each one was
> selected because it represents a distinct crisis mechanism.
>
> **Greece 2010–2012** — fiscal consolidation under external conditionality. GDP
> contracted for three consecutive years. The simulation correctly predicts
> contraction at each step.
>
> **Argentina 2001–2002** — sovereign default and convertibility peg collapse.
> A different mechanism from Greece: the binding constraint was monetary credibility,
> not fiscal space. The simulation captures the contractionary dynamics. And for
> Argentina 2002, the model is validated not just on direction but on magnitude:
> simulated GDP contraction of −10.55% against the historical −10.9% — a deviation
> of 3.2 percent. That is the first MAGNITUDE-validated result in WorldSim.
>
> **Lebanon 2019–2020** — a compound crisis: banking collapse, currency crisis,
> sovereign debt crisis, and the Beirut port explosion in year two. The cascade
> case. The simulation correctly predicts contraction at both steps.
>
> **Thailand 1997–2000** — externally triggered currency speculative attack producing
> domestic balance-sheet deterioration. The mechanism is different from all three
> prior cases: externally induced contagion, not domestically generated stress.
>
> **Ecuador 1999–2000** — banking collapse and dollarization. The first case with
> a recovery at step two. The fidelity threshold is "do not predict deeper contraction
> than step one" — not "predict contraction." The model passes. The recovery itself
> is a documented blind spot: dollarization stabilization is not yet modeled.

### What DIRECTION_ONLY Means

> The current fidelity threshold type is called DIRECTION_ONLY. In plain language:
> the model is being tested on whether it gets the sign right. Did GDP go down or up?
> Did unemployment rise or fall? It is a binary test.
>
> The model passes DIRECTION_ONLY on all five cases across ten sign checks. A model
> that randomly produced outputs would pass roughly 50% of binary sign tests.
> Consistent directional accuracy across five distinct crisis mechanisms is evidence
> that the model is capturing real causal dynamics.
>
> Magnitude calibration — DISTRIBUTION_COMBINED thresholds — is the next validation
> layer. Argentina 2002 is the first step toward it. We are working toward it. We
> are not claiming it before we have evidence.
>
> This is the discipline: document what the model has been shown to get right.
> Document what has not been validated. Ship both.

---

## Section 4 — What Is Being Built (5 minutes)

> The roadmap is best understood as a sequence of expanding analytical capability —
> each milestone extending what can be seen and trusted.

### Milestones 6 through 9 — Foundation (Complete)

> The first four milestones established the technical and methodological foundation:
> compliance framework clean, legibility baseline measured and documented, the
> backtesting suite covering five historical cases, the ecological composite score
> live, the governance module meeting its promotion criteria. These were not features —
> they were discipline. A simulation that produces outputs without a clean bill of
> methodological health is a tool that cannot be trusted in the setting it is designed
> for.

### Milestone 10 — Engine Integrity and Instrument Delivery (Complete — Current Version)

> Milestone 10 delivers what you have seen in this demonstration: all four Zone 1
> axes live with real data, GovernanceModule promoted from null placeholder to a live
> composite score, PMM live computation, and the Argentina second country fixture.
>
> The instrument cluster is now substantive across all four frameworks. For the first
> time, the demo shows four live curves on a shared step axis, an MDA alert that fires
> and is specific enough to cite, a PMM that gives a directional signal, and a
> four-framework readout with real numbers for ecological and governance.
>
> The Platform Principle is demonstrated in practice, not just claimed: same engine,
> different inputs, second country, same analytical discipline.

### Milestone 11 — Engine Investigation and Political Economy (Next)

> Milestone 11 addresses what the backtesting evidence tells us to look at next.
>
> The backtesting suite has two documented structural gaps: the one-step lag in
> Argentina's 2001 step (the Zero Deficit Plan fires but the MacroeconomicModule
> processes it with a lag), and the missing mean-reversion channel in Greece
> (GDP only accumulates downward, never receives an endogenous recovery impulse).
> Both require engine-level investigation. ADR-009 will define the computation model.
>
> M11 also introduces the political economy module: conditionality modeling, political
> feasibility scoring, elite capture dynamics. This is what moves the simulation
> from mechanical consequence modeling toward the full analysis a finance ministry
> needs in a live negotiation.
>
> Frame this as expanding capability, not missing features. What exists today is the
> capability that has been validated. What comes next is what the backtesting evidence
> and the epistemic commitments already made require.

---

## Section 5 — Q&A Preparation

### "Why not use existing IMF tools? They already have analytical infrastructure."

> The IMF's analytical tools are built for the IMF's analytical tasks. They are
> excellent at what they are designed to do. The capability gap we are addressing
> is not that the IMF's tools are bad — it is that they belong to the IMF.
>
> When a finance ministry uses the IMF's projections as its primary analytical
> input, it is evaluating conditionality terms against the model that produced
> those terms. That is a structural problem regardless of the quality of the model.
> The ministry needs its own analytical infrastructure — one that runs on its own
> assumptions and surfaces its own findings, which it can then compare to what the
> IMF is showing.
>
> This tool does not compete with IMF methodology. It gives the ministry team
> a mechanism to interrogate it.

### "How do you validate the model?"

> Backtesting against historical cases with documented fidelity thresholds.
> Five crisis cases covering five distinct crisis mechanisms. Explicit separation
> between what has been validated — DIRECTION_ONLY, the sign of directional change —
> and what has not — magnitude calibration. Documented blind spots for each case.
>
> The Argentina 2002 step is also the first MAGNITUDE-validated result: simulated
> GDP contraction of −10.55% against the historical −10.9%. Deviation: 3.2 percent,
> within the validated ±20% band. One case does not make a calibration claim —
> but it is the first evidence that magnitude accuracy is achievable.
>
> The validation architecture is transparent by design. Every fidelity threshold
> is registered in the database with its source citation. Every backtesting test
> is in the public repository and runs in CI — a failure is a build failure.

### "Why are financial and human development composites showing as null?"

> The percentile-rank scoring strategy for financial and human development composite
> scores requires at least two entities for a meaningful comparison — similar to
> how a percentile requires a distribution. A single entity has no peers to rank
> against.
>
> This is not a failure. It is the tool being honest about what composite scores
> mean: a governance composite that uses an absolute scoring strategy (WGI and
> V-Dem normalized to a common scale) can produce a meaningful number for one
> country. A composite that requires peer comparison cannot — not meaningfully, for
> a single entity.
>
> The indicators — GDP growth, unemployment — are live and displaying correctly.
> The composite awaits a second entity. Add Argentina's regional peers, or run a
> comparison scenario with Brazil, and the composites activate.

### "Who is this for?"

> The primary user is a debt restructuring specialist at a finance ministry in a
> developing or emerging market economy — specifically, one that encounters IMF or
> World Bank programmes as negotiating counterparts rather than as programme designers.
> They have graduate-level economics training. They are not data scientists. They
> need to reach an analytically defensible conclusion in minutes, not hours, under
> cognitive load.
>
> Secondary users: independent economists and civil society analysts who want to
> evaluate programme conditionality against human cost consequences that official
> programme documents do not surface. Third: journalists and accountability
> institutions who need an accessible mechanism to interrogate what a proposed
> programme actually does to a population.
>
> What this tool is not for: sovereign wealth fund analysis, trading strategy,
> sanctions design, or any use case in which the analytical advantage runs against
> vulnerable actors rather than toward them.

### "What does it cost to run?"

> The software is open source and free to use. The infrastructure requirements are
> a PostgreSQL database and a Python runtime — both available on commodity cloud
> hardware at negligible cost for a single ministry's analytical load. The application
> is designed to run on a machine with 8GB of RAM. It does not require paid APIs,
> licensed datasets, or proprietary services.
>
> All data sources used in the simulation and backtesting are open-licensed: IMF
> World Economic Outlook, World Bank World Development Indicators, Natural Earth
> boundary data, NOAA Mauna Loa Observatory, V-Dem. The methodology documentation
> will be available under the same license as the software.

---

## Section 6 — Honest Disclosures (available if asked)

These statements must be available if questions arise. Do not proactively
volunteer them in the main presentation unless a direct question requires it.
Frame them as evidence that the tool's epistemic honesty is working.

- **Distributions are pre-calibration.** Uncertainty bands reflect a reasonable
  range of model outcomes, not empirically calibrated confidence intervals.
  Disclosed in the interface and in the methodology documentation.

- **Ecological composite score is CO2-only.** The ecological module covers CO2
  planetary boundary proximity against the Rockström 2009 reference (350 ppm).
  Additional planetary boundary indicators (biodiversity, nitrogen, water) are
  framework scope for future milestones.

- **Financial and human development composites are null for single-entity scenarios.**
  Percentile-rank scoring requires ≥2 entities. Indicators (gdp_growth,
  unemployment_rate) are live. Disclosed in Zone 1D, not hidden.

- **Financial and HD curves in Zone 1A are dashed (Path A).** The dashed
  treatment indicates normalized-absolute scoring strategy applied without
  peer comparison. Methodology note available in Zone 3.

- **GDP magnitude at step 1 (Argentina 2001) is a documented structural gap.**
  The Zero Deficit Plan fires at step 1 but MacroeconomicModule processes it
  with a one-step lag. Model produces −0.8% vs historical −4.4% (82% deviation).
  Filed as Issue #222, deferred to M11 (engine investigation scope).

- **GovernanceModule mean-reversion dynamics are simplified at M10.** The
  full political economy module (M11) adds conditionality modeling, elite capture,
  and democratic backsliding dynamics. Current governance composite is a
  normalized absolute score, not a full political economy model.

- **This tool is not for financial advantage or surveillance.** The canonical user
  is a finance ministry counterpart in a negotiation. The tool does not assist in
  executing financial attacks, identifying exploitable vulnerabilities in adversaries,
  or any use case that amplifies power asymmetries against vulnerable actors.

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
> analytical tools, that minister can negotiate better terms. Better terms produce
> different fiscal paths. Different fiscal paths produce different human consequences.
>
> The quinoa farmer lives at the end of that chain. Every decision we make about
> this tool — what to build first, what to be honest about, what not to oversell —
> we make as if he is watching. Not because he is. But because that framing is the
> right discipline.
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

## Screenshot Reference (M10 Demo 3 Frames)

Captured: [to be filled after Step 6]. Located in `docs/demo/m10/screenshots/`.

| Presentation order | File | Step | Zone 1 state | Caption |
|---|---|---|---|---|
| 1 — Thesis | `frame-c-step3-divergence.png` | 3 / 4 | Zone 1A: financial ↑, governance flat | Financial recovery begins; governance WARNING still active — the asymmetry is the argument |
| 2 — Instrument | `frame-a-step1-instrument.png` | 1 / 4 | Zone 1 baseline, all instruments loaded | Argentina at programme entry: all four Zone 1 instruments live with crisis-arc initial state |
| 3 — Crisis | `frame-b-step2-crisis.png` | 2 / 4 | Zone 1A: step 2 inflection, MDA alerts | Sovereign default and devaluation — the sharpest inflection; first MAGNITUDE-validated step |
| 4 — Evidence | `frame-d-step3-evidence.png` | 3 / 4 | Zone 1B: governance WARNING full card | Threshold breach rendered as structured evidence — specific enough to cite |
| 5 — Recovery | `frame-e-step4-recovery.png` | 4 / 4 | Zone 1D: all four frameworks, recovery arc | GDP recovering; governance healing slowly — Platform Principle in practice |

See `docs/demo/m10/screenshot-brief.md` for the full UX Agent brief and frame-by-frame specifications.
