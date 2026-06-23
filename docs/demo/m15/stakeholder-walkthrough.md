# WorldSim Stakeholder Demonstration — Presenter Guide (v0.15.0 / Milestone 15)

> PM Agent — Demo 6 walkthrough. Produced for M15-G5 sprint (Issue #1055 / G8 gate prep).
> Grounded in `docs/ux/north-star.md`, `docs/ux/information-hierarchy.md`,
> and `docs/process/demo-preparation-standard.md`.
> Screenshot brief: `docs/demo/m15/screenshot-brief.md` (to be produced at G8)
>
> **Version:** v0.15.0 — Milestone 15 (Human Cost Architecture)
> **Supersedes:** `docs/demo/m14/stakeholder-walkthrough.md` (v0.14.0)
> **Scenario:** Zambia 2024, IMF Extended Credit Facility program review — six steps
>
> Target audience: non-technical stakeholders, domain economists, potential funders,
> ministry officials. Not developers.
>
> Total runtime: 20 minutes plus Q&A.

---

## Presenter Briefing — Read Before the Room Fills

### What Is New in Milestone 15

Three things are live for the first time in Demo 6:

1. **Zone 1B Layer 3 trajectory sentence** — Zone 1B no longer shows only the number,
   the floor, and the defensibility label. It now states the conclusion directly: "Reserve
   coverage has fallen 2.1 months below the CRITICAL threshold. At current draw rate, full
   depletion occurs in 4 steps." The instrument tells you what to do with the reading, not
   just what the gauge shows. This is the Layer 3 output the M14 trust architecture was
   built to receive. The sentence ships in M15.

2. **Zone 1A information architecture** — The primary viewport now presents the instrument
   cluster with a redesigned information hierarchy (ADR-017). The trajectory view, alert
   panel, PMM widget, and four-framework overview are structured so the highest-signal
   output is the first thing the analyst's eye lands on. Entry-state data and simulation
   outputs are visually distinguished at the layout level — not just by label.

3. **Path 1: Approved source network** — At scenario creation, the platform now queries the
   approved source registry to offer pre-populated initial state inputs from IMF WEO, World
   Bank WDI, and regional data providers. The Grounding strip's source citations are now
   system-verified against the approved source list, not just human-entered.

**Architecture change from M14:** Demo 6 delivers the Layer 3 sentence that Demo 5 
announced as forthcoming. Zone 1B now states the conclusion the M14 walkthrough said the 
analyst had to narrate manually. The demonstration's thesis is the same — challenge-response 
at the IMF ECF review table — but the tool now speaks the answer, not just displays the data.

**Methodology documentation:** The full WorldSim methodology — every model relationship,
calibration assumption, and documented limitation — is published and auditable at
`docs/onboarding/methodology-overview.md`. Reference it directly if asked about how
confidence tiers are assigned or how the simulation engine was validated.

### EL Scenario Design Decisions (Recorded 2026-06-19, carried from M14)

| Decision | Value |
|---|---|
| Entity | ZMB only (single entity) |
| Challenge moment | Reserve coverage data challenged by creditor → analyst responds with Grounding strip citation at zero interaction |
| Reserve coverage starting value | 3.8 months (IMF WEO Apr 2024, T2) — 0.8 months above the 3.0-month WARNING threshold; 1.3 months above the 2.5-month CRITICAL floor |
| Layer 3 sentence live | Zone 1B trajectory sentence ships in M15 — present in Demo 6 |

### Who Is in the Room

Assume a mixed audience. Domain economists, programme directors, ministry officials,
potential funders or institutional partners. The technical sophistication varies and
does not matter. What matters is that everyone in the room understands power asymmetry
in consequential negotiations and has a stake in correcting it.

The likely test they are running: "Is this specific enough to be useful at the table,
or is it another tool that requires specialist mediation to interpret?"

Demo 6 answers that question in the first two minutes — and the instrument now answers
it without the presenter having to narrate the conclusion.

### What They Need to Leave Believing

Three things, in priority order:

1. **The challenge-response moment is real.** When a creditor team challenges a
   reserve figure, the ministry team's ability to cite the source without pausing,
   without opening a drawer, without calling a specialist — that changes the character
   of the conversation. The Grounding strip is the mechanism. Demo 6 shows it working.

2. **The model is honest about what it knows and what it inferred.** ZMB ecological
   and governance data are synthetic extrapolations (T4). The tool labels them "Synthetic
   extrapolation" in Zone 1B. It does not hide the inference — it names it. That is
   the No False Precision principle in practice, and it is what gives the T2 data
   its credibility by contrast.

3. **The trust architecture extends to the full trajectory, not just the entry state.**
   The evidence thread traces from data source through assumptions to output. By step 5,
   Zone 1B states the conclusion directly. The creditor cannot challenge the chain, only
   the numbers — and the chain answers the challenge. The instrument answers it too.

---

## Section 1 — The Room (3 minutes)

### What the Presenter Says

> There is a room where this happens.
>
> On one side of the table: a creditor team. They have institutional memory that spans
> decades of programme design in this country. They have proprietary models. They have
> a dataset the ministry team cannot access before the meeting. They have twenty analysts
> behind them who have modelled this exact trajectory for six months.
>
> On the other side: a finance ministry. Three economists. Public data. And a question
> they will be asked in thirty minutes that they have twelve seconds to answer.
>
> The question is: "Where does your 3.8 months reserve figure come from?"
>
> Not: "Is your number right?" That is a negotiation about methodology. The question
> is the simpler one: "What is your source?" And the ministry team's answer to that
> question — how fast they can give it, how specific it is, whether it names the
> institution, the tier, and the date — determines whether the challenge lands or
> bounces.
>
> Today we are going to show you what that moment looks like when the ministry team
> has the right tool.

### What This Establishes

The problem is not analytical sophistication — it is access to traceable, defensible
evidence at the table, at the moment the challenge arrives. The trust architecture
is the response to a specific, concrete negotiating vulnerability.

Do not use warning language. Frame every capability as analytical standing in a
negotiation, not alarm about a crisis.

---

## Section 2 — Live Application (8 minutes)

### Presentation Order

Screenshots are presented in thesis-first order: C → A → B → D → E.
See `docs/demo/m15/screenshot-brief.md` for the five-frame brief and capture specs
(produced at G8 with live application screenshots).

The narrated Playwright walkthrough in `demo-narrated.spec.ts` captures frames in
step order (A → B → C → D → E) because that is the simulation's temporal order.
The presentation order inverts the opening: lead with the thesis frame (C), then
pull back to show the setup.

### Setup

Application should be running before the room fills. Run `./scripts/demo.sh` to
start the stack. The scenario creation happens in the Playwright walkthrough; for
live presentation, pre-create the Zambia scenario using the API or the UI creation
panel.

**Primary surface:** Zone 1 instrument cluster — trajectory view (1A), alert panel
(1B), PMM widget (1C), four-framework + PSP (1D). This is where the demo argument
lives. Do NOT narrate the choropleth as the analytical instrument (UX-RULING-4).

---

### Step 1 — Frame A: The Grounding Strip at Scenario Load (Step 1, 2024)

**What the audience sees:** ZMB at step 1. Four composite scores live. The Grounding
strip in the scenario parameters area shows: financial T2 (IMF WEO Apr 2024), human
development T2 (World Bank WDI 2023), ecological T4 (Synthetic extrapolation),
governance T4 (Synthetic extrapolation). Zone 1A shows the reserve trajectory.
Zone 1D shows the four-framework scores, each with an L0 tier annotation always
visible: Financial T2 (IMF WEO Apr 2024).

**Important: The Grounding strip shows entry-state data only.** These are the
initial values at scenario creation — fixed provenance, not simulation outputs. The
Grounding strip does not update as the simulation advances. When the scenario reaches
step 3 and reserve coverage has moved to 2.9 months, the Grounding strip continues
to show 3.8 months, because 3.8 months is the entry-state citation the tool is
preserving: where the analyst started, and what source they can cite at the table.

**What the presenter says:**

> Zambia, 2024. The IMF program is accepted. Before the simulation runs a single step —
> before any output has been computed — the Grounding strip is visible.
>
> Every initial number in this scenario has three fields in that strip: the source
> institution, the confidence tier, and the observation date.
>
> Reserve coverage: 3.8 months. IMF World Economic Outlook, April 2024. Tier two.
>
> That is on the screen. No drawer to open. No panel to navigate. It is the first
> thing the analyst sees when the scenario loads.
>
> Notice Zone 1D — the four-framework panel. Each framework score shows its tier
> annotation directly: T2 for the financial dimension, citing the IMF World Economic
> Outlook. That annotation is always visible at zero interaction.
>
> The trust architecture is not a footnote. It is structural.

**Cognitive purpose:** Show that the provenance is present before the analysis, not
discoverable after. The Grounding strip is the mechanism that makes the challenge-
response moment possible.

**Key narration note (UX-RULING-4):** Do NOT say "watch Zambia shift on the map."
The choropleth is geographic context. Say "Zone 1A shows..." or "the trajectory view
shows..." The instruments carry the argument.

---

### Step 2 — Frame C: The Citation at the Table (THESIS FRAME) (Step 3, 2026)

**What the audience sees:** Step 3. Year 2026. The food price shock has compounded
across two steps. Reserve coverage is now 2.9 months — in the WARNING zone (below the
3.0-month threshold, approaching the 2.5-month CRITICAL floor). Zone 1B persistent-detail
shows: indicator name ("Reserve Coverage (months)"), current value (2.9), floor (2.500),
negotiation-defensibility label ("Moderate confidence — cite with caveat"), percentage
distance above floor ("16.3% above floor at step 3"), and the Layer 3 trajectory sentence.
The Grounding strip is simultaneously visible, showing the entry-state 3.8-month value
with its source citation (IMF WEO Apr 2024, T2).

**Two distinct values are visible simultaneously — both correct:**
- **Grounding strip, 3.8 months:** The entry-state reserve coverage at scenario creation,
  sourced from IMF WEO Apr 2024. This is the provenance citation that answers "where does
  your 3.8 figure come from?" The Grounding strip preserves this value unchanged as the
  simulation advances — it is entry-state data, not a simulation output.
- **Zone 1B, 2.9 months:** The computed reserve coverage at step 3 (2026), after two
  steps of food price shock drawdown. This is the current simulated state.

These are not competing numbers — they are two points on the same trajectory. The presenter
must distinguish them explicitly in narration. See revised script below.

**Presenter timing note (DEMO-100):** Section 1 narration must be fully delivered before
Frame C appears on screen. Do not project Frame C while narrating "The Room." Keep the
display on the title slide until the final sentence of Section 1 — "Today we are going
to show you what that moment looks like when the ministry team has the right tool" — then
advance to Frame C.

**What the presenter says:**

> Step three. Year 2026. Two years into the programme. The food price shock has
> compounded. Reserve coverage is in the WARNING zone.
>
> This is the moment. The creditor says: "Where does your 3.8 months figure come from?
> We have a different number in our model."
>
> The analyst points to the Grounding strip — still open, never closed.
>
> Reserve coverage: 3.8 months. IMF World Economic Outlook, April 2024. Tier two.
>
> No drawer. No specialist. Under ten seconds.
>
> One more thing to note: the source is the IMF's own publication — the World Economic
> Outlook is an IMF document. The creditor is challenging a figure from their own
> institution's dataset. That changes the character of the conversation.

**PAUSE — let them read Zone 1B and the Grounding strip simultaneously.**

> Zone 1B — the alert panel — shows: Reserve Coverage (months). Current value: 2.9
> months. Floor: 2.5 months. The negotiation-defensibility label: Moderate confidence
> — cite with caveat.
>
> One thing to name explicitly: two reserve numbers are on screen at once. The Grounding
> strip shows 3.8 months — that is the entry-state value at programme creation, sourced
> from IMF WEO April 2024. The Grounding strip preserves that citation unchanged
> throughout the simulation, because that is the number the creditor challenged. Zone 1B
> shows 2.9 months — that is the current simulated state at step three, after two years
> of food price shock. They are not in conflict. They are two points on the same
> trajectory: where we started, and where we are.
>
> The indicator name is readable — not a database field. The floor is named. The
> direction of risk is clear: 16.3% above the CRITICAL floor, in the WARNING zone,
> moving down.
>
> Now look at Zone 1B again. The instrument does not just show you the gauge. In M15,
> it tells you what to do with the reading. The trajectory sentence is there: "Reserve
> coverage is declining. At this draw rate, the CRITICAL floor is reached within one step."
>
> In aviation, the instrument tells you what to do with the reading, not just what the
> gauge shows. That sentence is what M15 delivers.

**Cognitive purpose:** Land the thesis. The challenge-response moment is resolved
before the audience has time to ask whether it would be. The simultaneous visibility
of Zone 1B and the Grounding strip is the key composition.

---

### Step 3 — Frame B: Zone 1B in Detail (Step 3 continued)

**What the presenter says:**

> Let me name what you are seeing in that alert slot, because it is specific by design.
>
> In M12, that slot showed a tier badge and a raw threshold value. In M14, it showed
> four things: the indicator name in plain language, the negotiation-defensibility label,
> the current value against the floor, and the percentage distance.
>
> In M15, it shows five things — the fifth is the trajectory sentence. The sentence
> states the conclusion the analyst used to have to narrate. "Reserve coverage is
> declining. At this draw rate, the CRITICAL floor is reached within one step."
>
> That sentence is specific enough to put in a briefing note. The ministry team does
> not need to do additional calculation. The instrument has already done it.
>
> What the ministry team can argue from what is on screen today: reserve coverage is in
> the WARNING zone, the CRITICAL floor is 2.5 months, the trajectory is downward, and
> the tool states that CRITICAL is one step away. That is what it means to move from
> a tool that displays data to a tool that builds analytical standing.

---

### Step 4 — Frame D: Political Feasibility in the Same View (Step 3, 2026)

**What the audience sees:** Step 3. Zone 1D showing four composites plus PSP
(`programme_survival_probability`). Zone 1B showing the reserve WARNING alert with
Layer 3 trajectory sentence. Zone 1A showing the full arc from step 1.
The Grounding strip is now closed so Zone 1D is unobstructed.

**What the presenter says:**

> Step three. Year 2026. Reserve coverage is in the WARNING zone — 2.9 months,
> 0.4 months above the 2.5-month CRITICAL floor. Zone 1B tells us: CRITICAL is one step
> away. That is not the presenter's analysis of the screen — it is what the instrument states.
>
> Look at Zone 1D — the four-framework overview. There is a fifth readout: programme
> survival probability.
>
> This is a capability that came live in M14. The political economy module is asking a
> question the four composites cannot answer: given the fiscal pressure this government
> is under, what is the probability that the programme's conditionality terms can actually
> be implemented? Not whether the programme is approved. Whether the government can deliver
> what the approval requires.
>
> The value you are seeing is approximately 0.65. In plain terms: at this level of
> fiscal pressure and governance quality, the model assesses the programme's
> conditionality terms as carrying meaningful political execution risk — not a breakdown,
> but an active constraint running alongside the financial one. A programme with high
> reserve stress and moderate political execution risk is a programme under compounding
> pressure on two dimensions simultaneously.
>
> Reserve stress and programme viability are related but distinct constraints. The
> financial composite measures what the trajectory does to financial sustainability.
> The PSP measures whether the political system can execute the path. Both are visible
> in the same instrument cluster, at the same step, in the same moment the minister is
> looking at the screen.

**Cognitive purpose:** Introduce the political economy capability as a distinct
analytical dimension — not a modifier of the financial analysis, but a parallel
question the financial analysis cannot answer alone.

**Key narration note on PSP:** "The model is asking whether the programme's
conditionality terms are achievable given the fiscal pressure the country is under.
That is not a political prediction. It is a quantified constraint estimate based on
the political economy module's assessment of implementation capacity."

**Key narration note on alert status at step 3:** Zone 1B shows WARNING (not CRITICAL)
at step 3. Reserve = 2.9 months; CRITICAL floor = 2.5 months; WARNING zone = below 3.0.
The trajectory sentence states that CRITICAL is one step away. Do not narrate CRITICAL
as the current state until the audience reaches step 4 (year 2027).

---

### Step 5 — Frame E: The Evidence Thread Complete (Step 5, 2028)

**What the audience sees:** Step 5. Full Zone 1 instrument cluster. Zone 1A shows
the complete reserve arc from step 0 through step 5. Zone 1B shows the current alert
state with Layer 3 trajectory sentence. Zone 1D shows all composites plus PSP at step 5.
The Grounding strip or assumption surface is visible, confirming the source chain.

**What the presenter says:**

> Step five. Year 2028. Five annual steps from the scenario entry.
>
> Every number on this screen has a named source. Every input that drove the output
> is visible in the assumption surface — the L1 basis statement shows the inputs with
> their tier annotations. The confidence tier on every indicator tells you whether it
> came from measured data or a model estimate, and the methodology for that assignment
> is published and auditable by anyone. If you want to read it: it is at
> `docs/onboarding/methodology-overview.md` in the public repository.
>
> I want to name something explicitly about the ecological and governance data you are
> seeing in the Grounding strip: they are T4 — Synthetic extrapolation. That label is
> in the right column of the strip — it is on the screen, not in a footnote. This is
> not an apology. This is the No False Precision principle in practice. For a country
> where ecological and governance data are thin, the tool tells you what it knows from
> measured data and what it inferred from SADC comparable economies. The T2 data stands
> out by contrast — it is not inflated to cover the T4 gaps.
>
> You will notice the ecological module is not producing alerts in Zone 1B today. I have
> configured the scenario that way deliberately — a CO2 planetary boundary alert that
> fires from the opening step would push the reserve signal out of the primary alert slot.
> The reserve is the thesis indicator for this demonstration. In a full deployment,
> ecological alerts would appear in Zone 1B with the same T4 label visible in the
> alert text.
>
> What the ministry team has at the table, at step five, is a traceable chain: from
> data source through assumptions to output. Zone 1B states the conclusion. The Grounding
> strip preserves the entry-state citation throughout. The creditor can challenge the
> number. They cannot challenge the chain. The chain is documented, sourced, and on screen.
>
> That is what this demonstration is about.

**Cognitive purpose:** Close the live application section on the evidence chain as an
institutional asset, not just a data display. The kryptonite framing: the ministry
team with three economists can defend every number without specialist mediation, and the
instrument states the conclusion they used to have to narrate.

---

## Section 3 — Backtesting Credibility (4 minutes)

### The Epistemic Problem

> In 2013, Blanchard and Leigh published a paper that became one of the more
> uncomfortable self-assessments any major institution has produced. The IMF's programme
> designs during the 2010–2012 European austerity period used fiscal multipliers around
> 0.5. The empirical evidence showed actual multipliers were roughly 1.5 — three times
> higher. Programmes produced significantly more damage than their models predicted.
>
> This is not a criticism of the IMF. It is an illustration of the same epistemic
> problem this tool addresses: model assumptions embedded in consequential decisions
> are not visible to the parties most affected by those decisions. The ministry sitting
> across the table did not have a mechanism to interrogate the multiplier assumption.
>
> WorldSim is a direct response to that gap. But it is a response with its own
> validation obligations.

### The Five Cases

> WorldSim has been validated against five historical crisis cases — each representing
> a distinct crisis mechanism:
>
> **Greece 2010–2012** — fiscal consolidation under external conditionality. The
> model correctly predicts contraction at each step. DIRECTION_ONLY.
>
> **Argentina 2001–2002** — sovereign default and convertibility peg collapse.
> The first MAGNITUDE-validated result: simulated GDP contraction of −10.55% against
> the historical −10.9% — a 3.2% deviation. The same engine runs Zambia.
>
> **Lebanon 2019–2020** — compound crisis cascade. The model correctly predicts
> contraction at both steps. DIRECTION_ONLY.
>
> **Thailand 1997–2000** — externally induced currency attack producing domestic
> balance-sheet deterioration. DIRECTION_ONLY.
>
> **Ecuador 1999–2000** — banking collapse and dollarization. The recovery case —
> the fidelity threshold is "do not predict deeper contraction than the first step."
> The model passes.
>
> Honest disclosure for Demo 6: Zambia is not yet a backtested case. The reserve
> coverage trajectory in this scenario is a simulation output under the configured
> initial attributes and scheduled inputs — not a calibrated prediction of Zambia's
> actual trajectory. The engine that produced this output has been validated on five
> distinct crisis mechanisms. Zambia adds a sixth crisis type when backtesting is run
> against historical data. That work is M16 scope.

### What DIRECTION_ONLY Means

> The current fidelity threshold type is DIRECTION_ONLY: does the model get the sign
> right? The model passes on all five cases. A model that randomly produced outputs
> would pass roughly 50% of binary sign tests. Consistent directional accuracy across
> five distinct crisis mechanisms is evidence of real causal capture.
>
> Magnitude calibration — DISTRIBUTION_COMBINED thresholds — is the next validation
> layer. Argentina 2002 is the first step. We are not claiming it before we have evidence.

---

## Section 4 — What Is Being Built (3 minutes)

> The roadmap is best understood as expanding the trust architecture — each milestone
> extending what the ministry team can defend at the table.

### Milestones 1 through 14 — Foundation (Complete)

> The first fourteen milestones established the analytical infrastructure: the
> simulation engine, all four measurement frameworks live, political economy module,
> Zone 1B persistent-detail, instrument legibility at the 90-second threshold, the
> Grounding strip provenance layer, and the evidence thread. These were not features —
> they were discipline. The Layer 3 trajectory sentence delivered in M15 is only
> credible because the measurement and provenance underneath it have been validated.

### Milestone 15 — Human Cost Architecture (Current)

> Milestone 15 delivers what you have seen in this demonstration:
>
> **The Layer 3 trajectory sentence:** Zone 1B now states the conclusion, not just the
> data. "Reserve coverage is declining. At this draw rate, the CRITICAL floor is reached
> within one step." The instrument speaks the answer the M14 architecture was built to
> deliver.
>
> **Zone 1A information architecture:** ADR-017 reorganises the primary viewport so the
> highest-signal output is the first thing the analyst sees. Entry-state data and
> simulation outputs are visually distinguished at the layout level.
>
> **Path 1 approved source network:** At scenario creation, the platform queries the
> approved source registry. Grounding strip citations are now system-verified, not
> human-entered.
>
> What you are seeing in this demonstration is not a prototype. It is working software
> at v0.15.0, validated against five historical crisis mechanisms, with a published
> methodology that anyone can inspect and challenge — published at
> `docs/onboarding/methodology-overview.md`.

### What Comes Next (M16 and Beyond)

> Three capabilities that Demo 6 was designed not to claim:
>
> **Counter-proposal branch with trust arc:** Mode 3 Active Control combined with the
> evidence thread. A ministry team that can test alternative conditionality structures
> and show the traceable chain for each branch.
>
> **Zambia backtesting:** Running the ZMB ECF history against the engine to validate
> directional accuracy. The sixth crisis mechanism in the validated case set.
>
> **Cross-examination of composite decomposition:** ADR-015 Component 4 — the analyst
> can ask "what drove this composite score?" and the engine surfaces the contributing
> components with their source citations. The challenge-response moment extended to
> composite outputs, not just initial state inputs.

---

## Section 5 — Q&A Preparation

### "Where does your 3.8 months figure come from?"

> IMF World Economic Outlook, April 2024. Tier two — meaning the data was sourced from
> a primary institutional data provider under a peer-reviewed methodology. That citation
> is on the Grounding strip in the scenario header — it has been on the screen since
> before the simulation started. The confidence tier methodology is published in the
> WorldSim methodology documentation at `docs/onboarding/methodology-overview.md`;
> anyone can audit how we assigned Tier 2 to this figure.

*(This is the Demo 6 thesis question — the answer should take under ten seconds and
the presenter should not need to look anything up.)*

### "What does 'Synthetic extrapolation' mean in Zone 1B?"

> It means the indicator was estimated using statistical inference from comparable
> economies — in Zambia's case, SADC regional distributions and historical patterns —
> because the direct measurement data is thin or delayed. The tool labels this "T4 —
> Synthetic extrapolation" rather than hiding it behind a plausible-looking number.
>
> The No False Precision principle: when uncertainty is large enough to matter, the
> tool says so. The T4 label next to ecological and governance indicators makes the
> T2 labels on financial indicators more credible, not less — the distinction is real
> and visible.

### "What is programme survival probability and who sets it?"

> The political economy module computes a probability estimate based on the model's
> assessment of implementation capacity under the current fiscal trajectory. It
> incorporates the political feasibility of conditionality delivery given reserve
> stress, governance quality, and democratic legitimacy dynamics.
>
> It is not an IMF view. It is not a political prediction. It is the model's
> quantified estimate of a constraint — the same way reserve coverage months is
> the model's quantified estimate of a financial constraint. Both carry a confidence
> tier. The PSP calibration is ongoing — this is disclosed in Zone 1B when PSP
> appears in an alert.

### "Why not use existing IMF tools?"

> The IMF's analytical tools are built for the IMF's analytical tasks. The capability
> gap is not that the IMF's tools are bad — it is that they belong to the IMF.
>
> When a finance ministry uses the IMF's projections as its primary analytical input,
> it is evaluating conditionality terms against the model that produced those terms.
> That is a structural problem regardless of model quality. The ministry needs
> analytical infrastructure that runs on its own assumptions — so it can interrogate
> what the IMF is showing, not just receive it.
>
> The Grounding strip is not competing with IMF methodology. It is giving the ministry
> a mechanism to cite the same sources the IMF is using, from the ministry's own tool.

### "Who is this for?"

> The primary user is a debt restructuring specialist or senior economist at a finance
> ministry in a developing or emerging market economy — specifically one that encounters
> IMF or World Bank programmes as a negotiating counterpart. They have graduate-level
> economics training. They are not data scientists. They need to reach an analytically
> defensible conclusion in under 90 seconds, under cognitive load, in a room where
> they are the only one without a hundred analysts behind them.
>
> This tool is not for sovereign wealth fund analysis, trading strategy, sanctions
> design, or any use case in which the analytical advantage runs against vulnerable
> actors rather than toward them.

### "What does it cost to run?"

> The software is open source and free. Infrastructure: a PostgreSQL database and a
> Python runtime — available on commodity cloud hardware at negligible cost for a
> single ministry's analytical load. The application is designed to run on a machine
> with 8GB RAM. No paid APIs, no licensed datasets, no proprietary services.
>
> All data sources in the simulation and backtesting are open-licensed: IMF WEO, World
> Bank WDI, Natural Earth boundary data, NOAA Mauna Loa, V-Dem. The methodology
> documentation is published under the same license as the software — open access at
> `docs/onboarding/methodology-overview.md`.

---

## Section 6 — Honest Disclosures (Available If Asked)

These statements must be available if questions arise. Frame them as evidence that
the tool's epistemic honesty is working. Do not proactively volunteer unless a
direct question requires it.

- **Zambia is not a backtested case.** Reserve coverage trajectory is scenario output
  under configured initial attributes and scheduled inputs — not a calibrated prediction.
  Zambia ECF backtesting is M16 scope.

- **Ecological and governance data are T4 (synthetic extrapolation).** The tool
  labels this visibly in Zone 1B. Sourced from SADC regional distributions. Disclosed,
  not hidden.

- **PSP calibration is ongoing.** The political economy module's political feasibility
  calibration is active work. The PSP output carries a confidence tier consistent with
  the module's current validation status. Disclosed in Zone 1B when PSP appears.

- **Distributions are pre-calibration.** Uncertainty bands reflect a reasonable range
  of model outcomes, not empirically calibrated confidence intervals. Disclosed in UI.

- **No Mode 3 in Demo 6.** The counter-proposal capability (Mode 3 + evidence thread)
  is M16 scope. The control plane zone is visible in the UI but not the primary
  demonstration surface today.

- **This tool is not for financial advantage or surveillance.** The canonical user is
  a finance ministry counterpart in a negotiation. The tool does not assist in executing
  financial attacks, identifying vulnerabilities in adversaries, or any use case that
  amplifies power asymmetries against vulnerable actors.

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
| Section 1 | The room — the challenge-response framing | 3 min |
| Section 2 | Live application (five frames, Steps 1–5) | 8 min |
| Section 3 | Backtesting credibility | 4 min |
| Section 4 | What is being built (M15 + M16 horizon) | 3 min |
| Section 7 | North Star closing | 1 min |
| Q&A | See prepared responses above | Remaining time |

Total structured content: 19 minutes. Leave at least 10 minutes for Q&A.
Domain economists will engage most seriously on methodology — do not compress it.

---

## Screenshot Reference (M15 Demo 6 Frames)

Captured to `docs/demo/m15/screenshots/` via `demo-narrated.spec.ts` at G8.
Current files are preliminary placeholders — G8 replaces them with live application
screenshots showing Layer 3 trajectory sentence and ADR-017 Zone 1A layout.

| Presentation order | File | Step | Zone 1 focus | Caption |
|---|---|---|---|---|
| 1 — THESIS | `frame-c.png` | 3 / 6 | Zone 1B WARNING + Layer 3 sentence + Grounding strip entry-state | Reserve coverage challenge-response at step 3 (2026). Grounding strip shows entry-state 3.8 months (T2 · IMF WEO Apr 2024). Zone 1B shows Layer 3 trajectory sentence. |
| 2 | `frame-a.png` | 1 / 6 | Zone 1D L0 annotation + Grounding strip entry-state | Zambia at program entry: source, tier, date visible before analysis begins |
| 3 | `frame-b.png` | 3 / 6 | Zone 1B Layer 3 persistent-detail | Self-interpreting reserve WARNING alert with trajectory sentence: current 2.9 / floor 2.5 / direction statement |
| 4 | `frame-d.png` | 3 / 6 | Zone 1D: PSP alongside four composites | Programme survival probability live — financial and political constraints on same instrument |
| 5 | `frame-e.png` | 5 / 6 | Full instrument cluster: complete arc | Five-step trajectory, all sources named, evidence thread and Layer 3 output complete |
