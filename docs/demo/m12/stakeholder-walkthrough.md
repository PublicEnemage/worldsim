# WorldSim Stakeholder Demonstration — Presenter Guide (v0.12.0 / Milestone 12)

> UX Designer Agent — Journey: Stakeholder demonstration walkthrough.
> Grounded in `docs/ux/north-star.md` §Resolved Design Questions and
> `docs/ux/user-journeys.md`. Read both documents before adapting this guide.
> Narration voice standard: `docs/ux/standards.md §16` (NARRATION-RULING-1,
> EL ruling 2026-06-02). Each Section 2 step uses the three-layer structure
> verbatim: **Umbrella → Facts → Synthesis**. No step may be narrated as a
> fact barrage. M8 walkthrough (`docs/demo/m8/stakeholder-walkthrough.md`)
> is the reference voice standard.
>
> **Version:** v0.12.0 — Milestone 12 (External Sector, Mode 3 Active Control)
> **Supersedes:** `docs/demo/stakeholder-walkthrough.md` (v0.10.0)
> **Scenario:** Jordan + Egypt, Strait of Hormuz, 2024–2031 — eight steps
>
> Target audience for the demo: non-technical stakeholders and domain experts.
> Not developers. Not data scientists.
>
> Total runtime: 22 minutes plus Q&A.

---

## Presenter Briefing — Read Before the Room Fills

### What Is New in Milestone 12

This demo represents the most significant capability advance since the project
began. Four things are live for the first time:

1. **External Sector Module** — Import dependency, commodity shock transmission,
   reserve burn-rate under supply disruption, current account deterioration.
   The Hormuz scenario is the first demo in which the shock mechanism is
   modelled explicitly, not assumed.

2. **Mode 3 Active Control** — The minister can now steer, not just observe.
   From any step, the minister's team adjusts a policy lever — fiscal multiplier,
   central bank intervention rate, debt rescheduling terms — and the simulation
   branches to show the consequence. The tool does not recommend. It shows
   what the choice produces.

3. **All four composite scores live simultaneously** — Financial, Human
   Development, Ecological, Governance. This is the first demo in WorldSim
   history where all four axes of the Multi-Framework Overview render with
   live data. No axis is null. No axis is dashed.

4. **Two-country simultaneous modelling** — Jordan and Egypt face the same
   external shock and produce entirely different failure mechanisms. The
   divergence between the two is the analytical argument.

### Who Is in the Room

Assume a mixed audience. The technical sophistication varies and does not
matter. What matters is that everyone in the room understands power asymmetry
in consequential negotiations and has a stake in correcting it.

The likely profiles:

- **Domain economists and policy analysts** — comfortable with fiscal
  multipliers, import dependency ratios, and reserve adequacy thresholds.
  They will push hardest on methodology. If convinced, they become the most
  valuable advocates.

- **Programme directors and ministry officials** — understand the negotiating
  context intuitively. They need to see a tool that fits into the workflow they
  already have. For them, speed and specificity are the test.

- **Potential funders or institutional partners** — evaluating whether this
  project is worth supporting. They need the mission to be clear, the technical
  implementation to appear credible, and a confident sense of what makes this
  different from everything that already exists.

The presentation serves all three simultaneously. The live application serves
the policy analysts. The backtesting argument serves the economists. The North
Star closing serves the funders. Keep all three in view throughout.

### What They Need to Leave Believing

Three things, in priority order:

1. **The capability gap is real and consequential.** Finance ministries in
   vulnerable countries lack the analytical infrastructure that sophisticated
   institutional actors bring to the table. This is structural, not
   incidental. WorldSim is a direct response to that structural condition.

2. **The model is disciplined, not aspirational.** Backtesting against five
   historical crises with documented fidelity thresholds and explicit blind spot
   disclosure is evidence of methodological seriousness. The model knows what
   it does not know.

3. **What you are watching is already running on a production engine.** The
   Milestone 12 demo runs on the matrix computation engine validated in
   Phase 2 A/B testing. This is not a prototype advancing toward production
   readiness. This is working software.

### Narration Voice — Pre-Session Checklist (NARRATION-RULING-1)

Before presenting Section 2, verify each step's narration satisfies:

- [ ] **Umbrella present** — one to two sentences that orient before any facts.
  Ask: "Does the audience know *why* they are looking at this before I name
  any number?"
- [ ] **Facts read from instrument** — the specific indicator, value, and step
  exactly as visible on screen.
- [ ] **Synthesis present** — one to two sentences connecting the reading to
  the minister's decision. Ask: "Would a ministry official know what to *do*
  with this information?"

If any step has no umbrella and leads directly with a number, rewrite it.
If any step has no synthesis and ends on a fact, rewrite it.

---

## Section 1 — The Problem (3 minutes)

### What the Presenter Says

> When the IMF or World Bank walks into a negotiation, they bring an
> institution. They have programme economists who have modelled this exact
> country for years. They have historical precedent databases. They have
> scenario analysis capacity built up over decades, refined by hundreds of
> programme outcomes. They have seen this before, or something close enough
> to it that the pattern recognition is there.
>
> The finance ministry on the other side of the table is starting from a
> different position. Their team is smaller. Their analytical infrastructure
> is thinner. They may have excellent economists — but those economists are
> also managing a budget process, a parliamentary reporting requirement, and
> three other crises at the same time. The asymmetry is not in intent. It is
> in infrastructure.
>
> What that asymmetry produces, in practice, is a gap in the quality of
> scenario analysis available to each party. The IMF team can model what
> happens to the fiscal path if growth comes in 1.5 points below projection,
> or if import prices sustain at 30 percent above baseline. The ministry team
> is more likely to be working from the IMF's own model outputs, evaluated
> against their own economic judgment. That judgment is often good. But it
> is not the same as running the analysis yourself against your own
> assumptions about what the shock will do.
>
> WorldSim is an attempt to close that gap. Not to give the ministry team
> the same institution — that is not possible in a software tool. But to give
> them the same quality of scenario analysis: historical pattern recognition,
> human cost consequence modelling, distributional outputs rather than point
> estimates. Analytical capability that currently costs what sophisticated
> institutional infrastructure costs, made available as open-source software
> that runs on a laptop.

### What This Establishes

This framing — capability analysis, not alarm — follows directly from
north-star.md §Resolved Design Question 3. The human cost ledger is what
the path does to the people the ministry serves. It is an asset in the
negotiation, not a constraint on the ministry's own choices.

Do not use warning language here. Do not say "dangerous" or "alarming" or
"crisis." The human cost ledger shows consequences. The finance minister reads
those consequences as evidence. Evidence is power.

---

## Section 2 — Live Application (8 minutes)

### Setup

The application should be running and the map loaded before the session starts.
Do not demo a loading screen.

Run `./scripts/demo.sh --run` to launch the stack and follow this guide
manually. The scenario may be pre-created or created live — the creation step
is narrated but brief.

The presentation sequence follows the screenshot brief:
`docs/demo/m12/screenshot-brief.md`.

Do **not** narrate the choropleth as the analytical argument. The choropleth
is context. Zone 1A (trajectory view) is the instrument.

---

### Step 1 — The Map Loads

**What the audience sees:** A world map. Countries rendered as polygons. A
color gradient over the Middle East and North Africa region. The scenario
panel is visible on the left.

**UMBRELLA — What the presenter says:**

> The opening view is context, not the argument. What you are about to see
> is the same regardless of the country, the crisis type, or the year. This
> is a platform — one analytical framework, different ingredients.
>
> We are starting in the Middle East because the scenario we are modelling
> today involves a commodity shock transmitted through one of the most
> consequential maritime chokepoints on earth. But the instrument cluster you
> will be reading in a moment would look the same for a fiscal consolidation
> in a landlocked African economy.

**Cognitive purpose:** Establish the platform principle early. The audience
should understand from the first sentence that they are seeing a general
analytical capability, not a bespoke Middle East tool.

---

### Step 2 — Load the Jordan + Egypt Hormuz Scenario

**What the audience sees:** The presenter selects or creates the Jordan–Egypt
Hormuz scenario. Both JOR and EGY appear in the entity panel. The scenario
selector shows step 1 of 8. The step label reads 2024.

**UMBRELLA — What the presenter says:**

> The Strait of Hormuz handles approximately 20 percent of global oil trade
> and a significant share of Gulf food supply. In this scenario, beginning
> in 2024, disruption to that transit has produced a sustained commodity
> shock: fuel import costs elevated for Jordan, food import costs elevated
> for Egypt.
>
> What makes this a useful scenario to model is not the geopolitics — it is
> the structural difference between the two countries. Jordan depends on fuel
> imports heavily. Egypt depends on food imports heavily. The same external
> shock lands differently on two different import dependency structures.
>
> This is the two-country argument. Watch what happens to each country's
> trajectory as the same shock accumulates.

**FACTS:**

> Step 1, 2024. Jordan: fuel import dependency 0.42 — meaning 42 percent
> of domestic fuel consumption is imported. Reserve coverage: 7.1 months.
> Egypt: food import dependency 0.35. Democratic quality score: 0.07 on the
> V-Dem Liberal Democracy Index — already below the governance floor from the
> first step.

**SYNTHESIS:**

> The scenario does not begin with a crisis. It begins after the disruption
> is already underway. Both finance ministries are already inside the event.
> The question is which pathways are still available and at what cost.

**Cognitive purpose:** Establish the two-country analytical frame before the
first step advances. The audience needs to understand the structural asymmetry
between JOR and EGY before they can read the divergence.

---

### Step 3 — Advance Through the Arc (Steps 1 to 3)

**What the audience sees:** The presenter advances to step 3 (2026). The
trajectory view in Zone 1A shows both entity curves moving. The step label
reads 3/8, 2026.

**UMBRELLA — What the presenter says:**

> Before we stop and read any specific number, watch the shape of what is
> happening. Two countries, one shock, two very different trajectories.

**FACTS:**

> By step 3, Jordan's reserve coverage has moved from 7.1 months at step 1
> to 5.0 months. Egypt's democratic quality score — already at 0.07 at step
> 1 — has begun a further decline toward the 0.03 range as the government's
> emergency fiscal response activates.

**SYNTHESIS:**

> Jordan's stress is accumulating on the reserve axis: the fuel shock is
> burning through import capacity faster than the reserve buffer can absorb.
> Egypt's stress is accumulating on the governance axis: the emergency
> measures required to manage the food shock are the mechanism that deepens
> the governance deficit.
>
> Two failure modes, same precipitating event. That is the analytical
> argument for two-country simultaneous modelling.

**Pause. Let the trajectory view settle.**

**Cognitive purpose:** Orient the audience to the divergence pattern before
the thesis frame lands. The shape of the divergence should be visually
readable before the specific values are named.

---

### Step 4 — The Thesis Frame (Step 3, 2026 — Divergence)

**What the audience sees:** Zone 1A trajectory view at step 3, showing JOR
reserve curve declining and EGY governance curve in sustained breach. Zone 1B
MDA alert panel visible.

This is the presentation sequence's thesis frame — it is shown first in the
screenshot brief's C → A → B → D → E sequence.

**UMBRELLA — What the presenter says:**

> This is the frame that makes the tool's argument most legible. Step 3, 2026.
> Jordan's finance ministry is watching its reserve runway compress. Egypt's
> finance ministry is managing a country in which the governance indicators
> have been in breach from before the first step arrived.

**FACTS:**

> Zone 1A: Jordan reserve coverage 5.0 months, declining at approximately
> 1.2 months per step. The CRITICAL floor is 2.5 months — Jordan is three
> steps from it at current burn rate.
>
> Egypt democratic quality score: 0.07 at step 1, moving toward 0.03 by step 4
> as the emergency declaration activates. The governance floor is 0.70. Egypt
> is not approaching the floor — it is operating at one-tenth of the floor value.

**Pause. Let them read Zone 1B.**

> Zone 1B shows the MDA alert panel. Egypt's governance alert is CRITICAL and
> has been from step 1. That is not a step 3 finding — it is a pre-existing
> condition that the Hormuz disruption is deepening.
>
> Jordan's reserve alert is escalating toward CRITICAL, but has not reached it
> yet at step 3. That is the window the tool is illuminating.

**SYNTHESIS:**

> The two alert states on that panel represent two entirely different policy
> problems. Jordan's ministry needs to extend the reserve runway — that is a
> question about what intervention is available before step 5. Egypt's ministry
> is operating in governance breach; the Hormuz shock is compounding an
> existing structural condition, not creating a new one.
>
> A single-country model would show you one of these. The instrument cluster
> shows you both, on the same step axis, with the same analytical discipline.

**Cognitive purpose:** The thesis frame is the M12 centrepiece. The divergence
between JOR reserve stress and EGY governance stress is the argument for
multi-entity simultaneous modelling. It must land as a deliberate analytical
point, not a data display.

---

### Step 5 — Reserve CRITICAL Floor (Step 5, 2028)

**What the audience sees:** Zone 1A at step 5 (2028). JOR reserve coverage
has reached the CRITICAL alert threshold. Zone 1B shows a CRITICAL breach for
Jordan with consecutive breach count.

**UMBRELLA — What the presenter says:**

> Step 5 is 2028. This is the point where Jordan's reserve buffer reaches
> the critical floor — the threshold below which standard policy frameworks
> no longer provide protection, and where the options available to the
> ministry change structurally.

**FACTS:**

> Reserve coverage: 2.5 months. The CRITICAL floor is set at the IMF's
> minimum adequate reserve benchmark — below this level, the ministry's
> capacity to manage currency volatility, service import obligations, and
> maintain monetary credibility simultaneously is materially constrained.
>
> Zone 1B CRITICAL alert: reserve_coverage_months, step 5, first CRITICAL
> breach. The alert reads the finding, not a prediction.

**SYNTHESIS:**

> Read this alert as a sentence the finance minister can take into a cabinet
> meeting: "As of 2028, under the current trajectory, Jordan's reserve
> coverage reaches the critical threshold. This is the step at which the
> margin for negotiation narrows sharply."
>
> A finding you can cite is a finding you can use. The alert is specific
> enough for a technical briefing. It is also legible to a cabinet minister
> who has not read the methodology.

**Cognitive purpose:** The MDA alert is the primary instrument output for
this scenario. It must be read as a negotiating asset — specific, nameable,
and citable — not as a danger warning. The framing should be capability
analysis throughout.

---

### Step 6 — Mode 3 Active Control (Branch from Step 3, 2026)

**What the audience sees:** The Mode 3 control panel is active. The fiscal
multiplier lever is adjusted to 1.3, representing a GCC emergency fiscal
injection equivalent to a 30-percent increase in effective fiscal capacity.
Branch anchor is set at step 3. Zone 1A shows two trajectories: the baseline
Jordan reserve arc and the Mode 3 branch arc.

This is the emotional peak of the demonstration. Present it as a question
being answered in real time.

**UMBRELLA — What the presenter says:**

> Until this step, the tool has been reading the trajectory. This step is
> different. A finance ministry does not only read a trajectory — it steers.
>
> Here is the minister's question: if GCC partners provide emergency fiscal
> support equivalent to a 30-percent increase in Jordan's effective fiscal
> capacity, does that buy sufficient reserve runway to avoid the critical
> floor at step 5?
>
> The minister's team does not have weeks to model this. They may have the
> length of a phone call.

**FACTS:**

> Mode 3 active. Fiscal multiplier set to 1.3. Branch anchored at step 3,
> 2026. The simulation recomputes from the branch point forward. Zone 1A now
> shows both trajectories simultaneously — the baseline arc and the Mode 3
> branch arc — on the same step axis.

**SYNTHESIS:**

> What you are reading is the consequence of the intervention, not a
> recommendation. The tool does not tell the minister whether to accept the
> GCC offer. It shows what the fiscal injection produces under the current
> model dynamics: where the reserve curve lands at step 5, and whether the
> critical floor is cleared.
>
> Whether that consequence is sufficient is the minister's decision. That
> decision is better made with this analysis than without it.
>
> This is the counter-proposal function. The analytical capability that was
> previously available only to well-resourced institutional actors — running
> your own model, against your own assumptions, in the room — is what Mode 3
> delivers.

**Cognitive purpose:** Mode 3 is the north star the entire instrument
architecture has been designed toward. It must land as the answer to the
capability gap framed in Section 1: the ministry team can now run the analysis
themselves, against their own assumptions, with the same analytical discipline
their counterparts bring.

Do not oversell the branch result. If the Mode 3 trajectory clears the
critical floor, read the result factually. If it does not fully clear the
floor, that is equally important information — the minister learns the
intervention is insufficient at these parameters before going back to the
GCC with a counter-proposal.

---

### Step 7 — All Four Axes Live (Step 5, 2028 — Capability Claim)

**What the audience sees:** Zone 1D Multi-Framework Overview at step 5. All
four composite scores render with live data: Financial (reserve stress),
Human Development (bottom-quintile consumption under commodity price elevation),
Ecological (CO2 accumulation, independent of the Hormuz crisis), Governance
(EGY far below floor; JOR stable).

**UMBRELLA — What the presenter says:**

> The final frame closes on what is actually being claimed at this milestone.
> Not as a feature list — as a measurement architecture.

**FACTS:**

> Zone 1D shows all four composite scores simultaneously at step 5. Financial:
> reserve-linked divergence between Jordan and Egypt is the primary driver.
> Human Development: the bottom-quintile consumption capacity indicator —
> the primary human cost ledger signal — shows the commodity price transmission
> reaching the most vulnerable income cohort. Ecological: CO2 accumulation
> continues its trajectory independent of the Hormuz crisis — global carbon
> dynamics are not paused by a regional commodity shock. Governance: Egypt
> far below the floor from step 1; Jordan stable on governance while under
> financial pressure.
>
> No axis is null. No axis is dashed. All four frameworks are live and
> concurrent.

**SYNTHESIS:**

> This is the first time in WorldSim's demonstration history that all four
> analytical frameworks have appeared simultaneously with live data. The
> measurement architecture that has been under development across twelve
> milestones is now operationally complete for a canonical scenario.
>
> The same engine that validated Greece's 2010 austerity and Argentina's 2001
> default is modelling Jordan and Egypt in 2024 under a commodity price shock.
> The crisis is different. The geopolitical context is different. The
> measurement framework and the analytical discipline are identical. That is
> the platform principle in production.

**Cognitive purpose:** The four-axis completion is the M12 milestone claim.
It should land as a capability milestone, not a feature demonstration. The
audience should leave understanding that the measurement architecture is now
complete, and that what comes next is additional scenario depth, not
additional framework construction.

---

## Section 3 — Backtesting Credibility (5 minutes)

### The IMF Multiplier Error

> In 2013, Olivier Blanchard and Daniel Leigh — the IMF's chief economist and
> a senior Research Department economist — published a paper that became one
> of the more uncomfortable self-assessments any major institution has
> produced.
>
> The paper examined the fiscal multipliers the IMF had been using in its
> programme designs during the 2010–2012 European austerity period. A fiscal
> multiplier is the relationship between a unit of government spending cuts
> and the resulting change in output. The IMF's programme forecasts were built
> on multipliers around 0.5.
>
> The empirical evidence showed that the actual multipliers in the European
> austerity cases were roughly 1.5 — three times what the programmes had
> assumed. A one-point spending cut was contracting GDP by one and a half
> points. The programmes produced significantly more economic damage than
> their models predicted, which required further fiscal tightening to hit
> primary balance targets, which contracted GDP further, in a compounding cycle.
>
> This is not a criticism of the IMF. It is an illustration of the epistemic
> problem: model assumptions embedded in consequential decisions are not always
> visible to the parties most affected by those decisions. The finance ministry
> on the other side of the table did not have a mechanism to interrogate the
> multiplier assumption and produce its own analysis.
>
> Backtesting discipline is one response to that problem. You run your model
> against historical cases where the outcomes are known. You measure the gap
> between what your model produces and what actually happened. You document
> where the model is right, where it is wrong, and why. You ship that
> documentation alongside your outputs.

### The Five Cases

> WorldSim has been validated against five historical crisis cases. Each
> represents a distinct crisis mechanism.
>
> **Greece 2010–2012** — fiscal consolidation under external conditionality.
> GDP contracted for three consecutive years. The simulation correctly predicts
> contraction at each step and the direction of unemployment movement.
>
> **Argentina 2001–2002** — sovereign default and currency crisis following a
> convertibility peg. The simulation captures the contractionary dynamics.
> Argentina is also the first case where the simulation has reached MAGNITUDE
> calibration on year-one contraction — not just direction, but scale.
>
> **Lebanon 2019–2020** — a compound crisis: banking system collapse, currency
> crisis, sovereign debt crisis, and the Beirut port explosion as a compounding
> shock. Lebanon is the cascade case. The simulation correctly predicts
> contraction at both steps.
>
> **Thailand 1997–2000** — the Asian financial crisis. An externally triggered
> currency speculative attack that produced domestic balance-sheet deterioration.
> The simulation captures contraction in both crisis years.
>
> **Ecuador 1999–2000** — the dollarization case. Ecuador entered a banking
> collapse and hyperinflation in 1999, then replaced its national currency with
> the US dollar in January 2000. GDP contracted -6.3% in 1999 and recovered
> +2.8% in 2000. This is the recovery case — it tests whether the simulation
> can distinguish stabilization dynamics from continued deterioration. The
> model passes the directional test. The dollarization mechanism itself is a
> documented blind spot.

### What the Fidelity Thresholds Mean in Plain Language

> The current primary fidelity threshold type is called DIRECTION_ONLY. In
> plain language: the model is being tested on whether it gets the sign right.
> Did GDP go down or up? Did unemployment rise or fall? A model that randomly
> produced outputs would pass roughly half of binary sign tests. Consistent
> directional accuracy across five distinct crisis mechanisms is evidence that
> the model is capturing real causal dynamics.
>
> What DIRECTION_ONLY does not validate is magnitude. Argentina year one is
> now at MAGNITUDE calibration. The remaining cases are not. We are not
> claiming they are.
>
> This is the discipline: document what the model has been shown to get right.
> Document what has not been validated. Ship both.

### Why This Matters for the Demonstration You Just Saw

> The Jordan–Egypt Hormuz scenario runs on the same engine that produced those
> five validated cases. The backtesting discipline does not guarantee the
> Hormuz scenario is accurate — it demonstrates that the engine has been
> subjected to systematic empirical scrutiny and that its failure modes are
> documented.
>
> A ministry official who cites a finding from this simulation in a negotiation
> is staking their credibility on it. The tool must be able to tell her what
> it has and has not been shown to do.

---

## Section 4 — What Is Being Built (4 minutes)

> The roadmap is best understood as a sequence of expanding analytical
> capability — each milestone extending what can be seen and acted on.
>
> Milestones 1 through 12 are complete. The platform today runs a validated
> computation engine, models two-country simultaneous scenarios with live
> commodity shock transmission through the External Sector Module, renders
> all four measurement frameworks simultaneously, and gives the ministry team
> a live steering interface through Mode 3 Active Control.
>
> Milestone 13 is next: the Political Economy Module. Conditionality
> modelling, political feasibility constraints, elite capture dynamics.
> The analytical gap we are closing in M13 is between what the model
> predicts and what is actually feasible to implement given the political
> economy of the country in question. A fiscal path that is technically
> sound but politically impossible is not a useful output. M13 addresses
> that.
>
> Beyond M13: resolution spectrum expansion, multi-region cascade modelling,
> and the formal backtesting data partnership programme — opening the
> validation layer to external domain reviewers with historical data authority
> we do not have ourselves.
>
> The sequencing is deliberate. Measurement architecture first. Steering
> capability second. Political feasibility modelling third. Each layer builds
> on validated foundations.

---

## Section 5 — Q&A Preparation

### Questions to Expect

**"How accurate is this? Can I rely on these numbers?"**

> The backtesting section answers this directly: the model passes DIRECTION_ONLY
> on five distinct crisis mechanisms. Argentina year one is at MAGNITUDE
> calibration. The remainder are directionally validated. We are not claiming
> predictive precision. We are claiming structured analytical rigour — the
> same rigour we apply to any model used in consequential decisions, applied
> to our own. The documentation of what we have and have not validated is
> shipped with every output.

**"How is this different from IMF or World Bank models?"**

> Two differences that matter. First, it is open source — anyone can inspect,
> challenge, and improve the methodology. The transparency that gives the tool
> credibility is structural, not a marketing claim. Second, it is designed to
> be run by the ministry team, not only by the external counterpart. The
> epistemic gap we are closing is not about having better numbers — it is
> about who runs the analysis and against whose assumptions.

**"What about Egypt's governance score — was that 0.07 from the start?"**

> Yes. Egypt's democratic quality score in this scenario is seeded at 0.07 —
> the V-Dem Liberal Democracy Index value for Egypt in 2023. That is not a
> model artifact or a calibration choice; it is the actual historical datum.
> The governance alert that fires from step 1 is correct. The Hormuz
> disruption did not cause Egypt's governance deficit — it is deepening a
> pre-existing condition.

**"Could Mode 3 be used to model adversarial scenarios?"**

> The tool is designed for defensive situational awareness — the asymmetry we
> are correcting runs one direction. The Mode 3 control surface is scoped to
> policy levers that a finance ministry would use: fiscal multiplier, debt
> rescheduling terms, central bank intervention rate. It is not designed to
> model financial attacks or exploit vulnerability identification. The dual-use
> position is documented in `docs/POLICY.md`.

**"When will this be ready for production use?"**

> The tool is operational today for structured scenario analysis and historical
> validation. Mode 3 Active Control is live as of Milestone 12. The limiting
> factor for production deployment in a ministry context is data access — the
> simulation's fidelity is bounded by the quality of country-specific inputs
> available. The synthetic data framework handles data-poor environments with
> documented confidence tiers, but production advisory use requires domain
> partner engagement on data provenance.

---

## Section 6 — Honest Disclosures

These disclosures are not optional. They belong in any substantive discussion
of the tool's current state.

**The ecological composite is CO2-only in Milestone 12.**
The ecological framework currently computes planetary boundary proximity
against CO2 concentration. Land use pressure is in the measurement output but
does not yet drive the composite score. Ecological consequences visible in
Zone 1D are real but incomplete. Full multi-boundary ecological composite is
on the M13 roadmap.

**The commodity shock transmission is directional, not magnitude-calibrated.**
The External Sector Module models fuel and food import shocks through reserve
burn rate and consumption capacity. The directional transmission is validated
through the backtesting suite. The precise magnitude of the reserve drawdown
per shock unit has not been independently calibrated against a historical
commodity crisis case. Do not present reserve level projections as predictions.

**Mode 3 does not recommend.**
The Mode 3 branch shows the consequence of a policy intervention under the
current model dynamics. It does not identify the intervention. It does not
evaluate whether the intervention is politically feasible. Political economy
modelling is Milestone 13.

**Egypt's governance score is a pre-existing condition, not a scenario output.**
This is stated in the Q&A section but warrants emphasis here: the EGY
governance CRITICAL alert from step 1 is the correct modelling of a real
historical state. It is not a bug. It is not a demonstration artifact.

**The simulation is not a prediction engine.**
Outputs are distributions, not point estimates. The step values visible in
the trajectory view are the simulation's central estimate under the input
parameters. Uncertainty bands and confidence tiers are available in the full
analysis panel. Present the central estimate as a scenario output, not a forecast.

---

## Section 7 — The North Star

> A finance minister in a small, vulnerable country is sitting across a table
> from an IMF negotiating team. They have limited time, limited staff, and
> generational consequences riding on the decision they are about to make.
>
> What you watched today is a tool designed to exist in that room. The
> trajectory view is the instrument cluster. The MDA alert is the finding.
> Mode 3 is the counter-proposal function. The multi-framework overview is
> the evidence that financial recovery and human recovery are not the same event.
>
> The tool does not negotiate. It gives the minister's team the analytical
> standing to negotiate from a position of comparable rigour.
>
> A quinoa farmer in Bolivia will never know this tool exists. Build it as
> if he does.

---

## Appendix A — Screenshot Reference

Screenshot files and presentation sequence are in `docs/demo/m12/screenshot-brief.md`.

Presentation sequence: Frame C (divergence thesis) → Frame A (instrument, step 1) → Frame B (escalation, step 2) → Frame D (Mode 3 branch) → Frame E (all four axes, step 5).

Frame file locations: `docs/demo/m12/screenshots/`

---

## Appendix B — Technical Reference for Domain Expert Questions

For questions that go deeper than the main presentation:

- **Computation engine:** Matrix computation engine (ADR-009), validated in
  Phase 2 A/B testing. Performance and equivalence verification documented
  at `docs/architecture/performance/phase2-ab-comparison.md`.
- **External Sector Module:** ADR-012. Import dependency × commodity price
  shock → reserve burn rate and consumption capacity transmission.
- **Planetary boundary thresholds:** CO2 boundary at 350 ppm (Rockström 2009),
  normalised to produce a proximity score where 1.0 = boundary reached. Values
  above 1.0 indicate boundary exceedance.
- **Confidence tier system:** Five-tier classification per `docs/DATA_STANDARDS.md
  §Confidence Tier System`. Synthetic data is always Tier 3 or below. Tier
  visible on each indicator in the entity panel.
- **Backtesting fixture data:** All five cases use open-licensed historical data.
  Fixture files in `backend/tests/backtesting/fixtures/`.
