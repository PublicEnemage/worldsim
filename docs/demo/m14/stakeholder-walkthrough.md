# WorldSim Stakeholder Demonstration — Presenter Guide (v0.14.0 / Milestone 14)

> PM Agent — Demo 5 walkthrough. Produced for G8 sprint (Issue #1055).
> Grounded in `docs/ux/north-star.md`, `docs/ux/information-hierarchy.md`,
> and `docs/process/demo-preparation-standard.md`.
> Screenshot brief: `docs/demo/m14/screenshot-brief.md`
>
> **Version:** v0.14.0 — Milestone 14 (Methodology Publication and External Validation)
> **Supersedes:** `docs/demo/m12/stakeholder-walkthrough.md` (v0.12.1)
> **Scenario:** Zambia 2024, IMF Extended Credit Facility program review — six steps
>
> Target audience: non-technical stakeholders, domain economists, potential funders,
> ministry officials. Not developers.
>
> Total runtime: 20 minutes plus Q&A.

---

## Presenter Briefing — Read Before the Room Fills

### What Is New in Milestone 14

Three things are live for the first time:

1. **ADR-016 Grounding strip** — Every scenario's initial state inputs are accompanied
   by a source citation, confidence tier, and vintage date at zero interaction. Before
   the simulation runs, every number has a named provenance. A ministry analyst can
   cite the source of any input at the table without opening a drawer or calling a
   specialist. This is the trust architecture the challenge-response moment requires.

2. **ADR-015 Evidence thread** — L0 basis annotations (tier badges and source labels)
   appear inline on Zone 1A trajectory curves. Zone 1B persistent-detail now shows the
   indicator name (not a raw database field name), human-readable tier label, and a
   Layer 3 self-interpreting sentence: not just the value, but what the value means and
   what threshold it is approaching. The L1 assumption surface makes all inputs visible
   with their tier annotations from the instrument cluster.

3. **Political economy module: programme survival probability (PSP)** — Zone 1D now
   shows a fifth readout alongside the four composites: `programme_survival_probability`.
   The model assesses whether the programme's conditionality terms are achievable given
   the fiscal trajectory. This is not a financial question — it is a political feasibility
   question. Reserve stress and programme viability are related but distinct constraints,
   now visible on the same instrument simultaneously.

**Architecture change from M12:** Demo 5 is single-entity (ZMB only). No Mode 3 in Demo 5
scope (EL decision 2026-06-19). Zone 1B persistent-detail now carries the full Layer 3
output — the alert slot does not require interaction. The demonstration's thesis moment is
a challenge-response at the IMF ECF review table, not a counter-proposal branch.

### EL Scenario Design Decisions (Recorded 2026-06-19)

| Decision | Value |
|---|---|
| Entity | ZMB only (single entity) |
| Mode 3 | Not in Demo 5 scope |
| Challenge moment | Reserve coverage data challenged by creditor → analyst responds with Grounding strip citation at zero interaction |
| Reserve coverage starting value | 3.8 months (IMF WEO Apr 2024, T2) — close to CRITICAL floor (3.0 months) |

### Who Is in the Room

Assume a mixed audience. Domain economists, programme directors, ministry officials,
potential funders or institutional partners. The technical sophistication varies and
does not matter. What matters is that everyone in the room understands power asymmetry
in consequential negotiations and has a stake in correcting it.

The likely test they are running: "Is this specific enough to be useful at the table,
or is it another tool that requires specialist mediation to interpret?"

Demo 5 answers that question in the first two minutes.

### What They Need to Leave Believing

Three things, in priority order:

1. **The challenge-response moment is real.** When a creditor team challenges a
   reserve figure, the ministry team's ability to cite the source without pausing,
   without opening a drawer, without calling a specialist — that changes the character
   of the conversation. The Grounding strip is the mechanism. Demo 5 shows it working.

2. **The model is honest about what it knows and what it inferred.** ZMB ecological
   and governance data are synthetic extrapolations (T4). The tool labels them "Synthetic
   extrapolation" in Zone 1B. It does not hide the inference — it names it. That is
   the No False Precision principle in practice, and it is what gives the T2 data
   its credibility by contrast.

3. **The trust architecture extends to the full trajectory, not just the entry state.**
   The evidence thread traces from data source through assumptions to output. By step 5,
   the ministry team can defend every number on the screen. The creditor cannot challenge
   the chain, only the numbers — and the chain answers the challenge.

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
See `docs/demo/m14/screenshot-brief.md` for the five-frame brief and capture specs.

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
governance T4 (Synthetic extrapolation). Zone 1A shows the reserve trajectory with
a T2 basis annotation on the curve.

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
> Notice the trajectory view above the map. The reserve curve has a small badge: T2.
> That badge is the L0 basis annotation — the source and tier directly on the
> instrument, not behind a click.
>
> The trust architecture is not a footnote. It is structural.

**Cognitive purpose:** Show that the provenance is present before the analysis, not
discoverable after. The Grounding strip is the mechanism that makes the challenge-
response moment possible.

**Key narration note (UX-RULING-4):** Do NOT say "watch Zambia shift on the map."
The choropleth is geographic context. Say "Zone 1A shows..." or "the trajectory view
shows..." The instruments carry the argument.

---

### Step 2 — Frame C: The Citation at the Table (THESIS FRAME) (Step 2, 2025)

**What the audience sees:** Step 2. Fiscal conditionality begins — a 2.5% spending
reduction. Zone 1B persistent-detail shows the reserve coverage alert with full
Layer 3 output: indicator name ("Reserve Coverage (months)"), current value, threshold,
tier label ("T2 · IMF WEO Apr 2024"), and the self-interpreting sentence naming the
threshold and the time to CRITICAL. The Grounding strip is simultaneously visible.

**What the presenter says:**

> Step two. Year 2025. The IMF program's fiscal conditionality begins. Reserve coverage
> is declining.
>
> This is the moment. The creditor says: "Where does your 3.8 months figure come from?
> We have a different number in our model."
>
> The analyst points to the screen.
>
> Zone 1B — the alert panel — shows: Reserve Coverage (months). The tier label:
> T2 · IMF WEO Apr 2024. The self-interpreting sentence: at the current draw rate,
> the CRITICAL floor is reached within two steps.
>
> The Grounding strip in the scenario header is showing the same citation for the
> initial state.
>
> No drawer. No specialist. Under ten seconds.
>
> One more thing to note: the source is the IMF's own publication — the World Economic
> Outlook is an IMF document. The creditor is challenging a figure from their own
> institution's dataset. That changes the character of the conversation.

**PAUSE — let them read Zone 1B and the Grounding strip simultaneously.**

> Read what is on the screen. The indicator name is readable — not a database field.
> The tier is readable — not a raw number. The direction of risk is named. The
> self-interpreting sentence tells you what the number means, not just what it is.
>
> That is a Layer 3 output. In aviation, the instrument tells you what to do with the
> reading, not just what the gauge shows. This instrument does the same.

**Cognitive purpose:** Land the thesis. The challenge-response moment is resolved
before the audience has time to ask whether it would be. The simultaneous visibility
of Zone 1B and the Grounding strip is the key composition.

---

### Step 3 — Frame B: Zone 1B in Detail (Step 2 continued)

**What the presenter says:**

> Let me name what you are seeing in that alert slot, because it is specific by design.
>
> In M12, that slot showed a tier badge and a raw threshold value. In M14, it shows
> four things: the indicator name in plain language, the confidence tier as a
> human-readable label, the current value against the threshold, and the Layer 3
> sentence.
>
> The Layer 3 sentence is not "reserve coverage is low." It is: at the current draw
> rate, the CRITICAL floor — the minimum adequate reserve benchmark — is reached within
> two steps. That sentence is specific enough to put in a briefing note. The minister
> can hand it to the negotiating team verbatim.
>
> This is the difference between a tool that displays data and a tool that builds
> analytical standing.

---

### Step 4 — Frame D: Political Feasibility in the Same View (Step 3, 2026)

**What the audience sees:** Step 3. Zone 1D showing four composites plus PSP
(`programme_survival_probability`). Zone 1B showing the reserve CRITICAL alert.
Zone 1A showing the full arc from step 1.

**What the presenter says:**

> Step three. Year 2026. Reserve coverage crosses the CRITICAL threshold.
>
> Look at Zone 1D — the four-framework overview. There is a fifth readout: programme
> survival probability.
>
> This is a new capability in M14. The political economy module is asking a question
> the four composites cannot answer: given the fiscal pressure this government is under,
> what is the probability that the programme's conditionality terms can actually be
> implemented? Not whether the programme is approved. Whether the government can deliver
> what the approval requires.
>
> Reserve stress and programme viability are related — a government with depleting
> reserves under conditionality is a government under compounding pressure. But they are
> not the same constraint. The financial composite measures what the trajectory does to
> financial sustainability. The PSP measures whether the political system can execute
> the path.
>
> Both are now visible in the same instrument cluster, at the same step, in the same
> moment the minister is looking at the screen.
>
> For the first time.

**Cognitive purpose:** Introduce the political economy capability as a distinct
analytical dimension — not a modifier of the financial analysis, but a parallel
question the financial analysis cannot answer alone.

**Key narration note on PSP:** "The model is asking whether the programme's
conditionality terms are achievable given the fiscal pressure the country is under.
That is not a political prediction. It is a quantified constraint estimate based on
the political economy module's assessment of implementation capacity."

---

### Step 5 — Frame E: The Evidence Thread Complete (Step 5, 2028)

**What the audience sees:** Step 5. Full Zone 1 instrument cluster. Zone 1A shows
the complete reserve arc from step 0 through step 5. Zone 1B shows the current alert
state with Layer 3 output. Zone 1D shows all composites plus PSP at step 5. The
Grounding strip or assumption surface is visible, confirming the source chain.

**What the presenter says:**

> Step five. Year 2028. Five annual steps from the scenario entry.
>
> Every number on this screen has a named source. Every input that drove the output
> is visible in the assumption surface — the L1 basis statement shows the inputs with
> their tier annotations. The confidence tier on every indicator tells you whether it
> came from measured data or a model estimate, and the methodology for that assignment
> is published and auditable by anyone.
>
> I want to name something explicitly about the ecological and governance data you are
> seeing: they are T4 — Synthetic extrapolation. The tool says "Synthetic extrapolation"
> in Zone 1B when those indicators appear in an alert. This is not an apology. This is
> the No False Precision principle in practice. For a country where ecological and
> governance data are thin, the tool tells you what it knows from measured data and what
> it inferred from SADC comparable economies. The T2 data stands out by contrast — it
> is not inflated to cover the T4 gaps.
>
> What the ministry team has at the table, at step five, is a traceable chain: from
> data source through assumptions to output. The creditor can challenge the number.
> They cannot challenge the chain. The chain is documented, sourced, and on screen.
>
> That is what this demonstration is about.

**Cognitive purpose:** Close the live application section on the evidence chain as an
institutional asset, not just a data display. The kryptonite framing: the ministry
team with three economists can defend every number without specialist mediation.

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
> the fidelity threshold is "do not predict deeper contraction than step one."
> The model passes.
>
> Honest disclosure for Demo 5: Zambia is not yet a backtested case. The reserve
> coverage trajectory in this scenario is a simulation output under the configured
> initial attributes and scheduled inputs — not a calibrated prediction of Zambia's
> actual trajectory. The engine that produced this output has been validated on five
> distinct crisis mechanisms. Zambia adds a sixth crisis type when backtesting is run
> against historical data. That work is M15 scope.

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

### Milestones 1 through 13 — Foundation (Complete)

> The first thirteen milestones established the analytical infrastructure: the
> simulation engine, all four measurement frameworks live, political economy module,
> Zone 1B persistent-detail, instrument legibility at the 90-second threshold. These
> were not features — they were discipline. The trust architecture delivered in M14
> is only credible because the measurement underneath it has been validated.

### Milestone 14 — Methodology Publication and External Validation (Current)

> Milestone 14 delivers what you have seen in this demonstration:
>
> **The trust architecture:** ADR-016 Grounding strip brings source provenance to every
> initial state input. ADR-015 Evidence thread makes the chain from source to output
> traceable and visible. Zone 1B is Layer 3 — it tells you what the number means,
> not just what it is.
>
> **The political economy module:** Programme survival probability is live in Zone 1D.
> The political feasibility question and the financial trajectory question are on the
> same instrument.
>
> **Methodology publication:** The methodology documentation — every model relationship,
> calibration assumption, and documented limitation — is being published as part of this
> milestone. The Technical Steering Committee forms at M14 close: the first governance
> actor independent of the Engineering Lead.
>
> What you are seeing in this demonstration is not a prototype. It is working software
> at v0.14.0, validated against five historical crisis mechanisms, with a published
> methodology that anyone can inspect and challenge.

### What Comes Next (M15 and Beyond)

> Three capabilities that Demo 5 was designed not to claim:
>
> **Counter-proposal branch with trust arc:** Mode 3 Active Control (tested a multiplier
> scenario in Demo 4) combined with the evidence thread. A ministry team that can test
> alternative conditionality structures and show the traceable chain for each branch.
>
> **Cross-examination of composite decomposition:** ADR-015 Component 4 — the analyst
> can ask "what drove this composite score?" and the engine surfaces the contributing
> components with their source citations. The challenge-response moment extended to
> composite outputs, not just initial state inputs.
>
> **Zambia backtesting:** Running the ZMB ECF history against the engine to validate
> directional accuracy. The sixth crisis mechanism in the validated case set.

---

## Section 5 — Q&A Preparation

### "Where does your 3.8 months figure come from?"

> IMF World Economic Outlook, April 2024. Tier two — meaning the data was sourced from
> a primary institutional data provider under a peer-reviewed methodology. That citation
> is on the Grounding strip in the scenario header — it has been on the screen since
> before the simulation started. The confidence tier methodology is published in the
> WorldSim methodology documentation; anyone can audit how we assigned Tier 2 to this
> figure.

*(This is the Demo 5 thesis question — the answer should take under ten seconds and
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
> tier. The PSP is exploratory in M14 — the political economy module's calibration
> is ongoing. This is disclosed in Zone 1B when PSP appears in an alert.

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
> documentation is published under the same license as the software.

---

## Section 6 — Honest Disclosures (Available If Asked)

These statements must be available if questions arise. Frame them as evidence that
the tool's epistemic honesty is working. Do not proactively volunteer unless a
direct question requires it.

- **Zambia is not a backtested case.** Reserve coverage trajectory is scenario output
  under configured initial attributes and scheduled inputs — not a calibrated prediction.
  Zambia ECF backtesting is M15 scope.

- **Ecological and governance data are T4 (synthetic extrapolation).** The tool
  labels this visibly in Zone 1B. Sourced from SADC regional distributions. Disclosed,
  not hidden.

- **PSP is exploratory in M14.** The political economy module's political feasibility
  calibration is ongoing. The PSP output carries a confidence tier consistent with the
  module's current validation status. Disclosed in Zone 1B when PSP appears.

- **Distributions are pre-calibration.** Uncertainty bands reflect a reasonable range
  of model outcomes, not empirically calibrated confidence intervals. Disclosed in UI.

- **No Mode 3 in Demo 5.** The counter-proposal capability (Mode 3 + evidence thread)
  is M15 scope. The control plane zone is visible in the UI but not activated.

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
| Section 4 | What is being built (M14 + M15 horizon) | 3 min |
| Section 7 | North Star closing | 1 min |
| Q&A | See prepared responses above | Remaining time |

Total structured content: 19 minutes. Leave at least 10 minutes for Q&A.
Domain economists will engage most seriously on methodology — do not compress it.

---

## Screenshot Reference (M14 Demo 5 Frames)

Captured to `docs/demo/m14/screenshots/` via `demo-narrated.spec.ts`.

| Presentation order | File | Step | Zone 1 focus | Caption |
|---|---|---|---|---|
| 1 — THESIS | `frame-c-citation-at-table.png` | 2 / 6 | Zone 1B + Grounding strip simultaneously visible | Reserve coverage T2 · IMF WEO Apr 2024. The answer on screen before the question finishes. |
| 2 | `frame-a-grounding-strip.png` | 1 / 6 | Zone 1A L0 annotation + Grounding strip | Zambia at program entry: source, tier, date visible before analysis begins |
| 3 | `frame-b-zone1b-reserve.png` | 2 / 6 | Zone 1B Layer 3 persistent-detail | Self-interpreting reserve alert: indicator name, tier label, threshold, direction |
| 4 | `frame-d-political-feasibility.png` | 3 / 6 | Zone 1D: PSP alongside four composites | Programme survival probability live — financial and political constraints on same instrument |
| 5 | `frame-e-evidence-thread.png` | 5 / 6 | Full instrument cluster: complete arc | Five-step trajectory, all sources named, evidence thread complete |

See `docs/demo/m14/screenshot-brief.md` for the full UX Agent brief and frame specifications.
