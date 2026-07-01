# WorldSim Stakeholder Demonstration — Presenter Guide (v0.18.0 / Milestone 18)

> PM Agent — Demo 7 walkthrough. Produced for M18 demo preparation (Issue #1445).
> Grounded in `docs/ux/north-star.md`, `docs/ux/information-hierarchy.md`,
> and `docs/process/demo-preparation-standard.md`.
> Screenshot brief: `docs/demo/m18/screenshot-brief.md`
>
> **Version:** v0.18.0 — Milestone 18 (Full Argument and Demo 7)
> **Supersedes:** `docs/demo/m17/stakeholder-walkthrough.md` (v0.17.0)
> **Scenarios:** Act 1 — Senegal 2024, Mode 3 active control; Act 2 — Zambia, three-scenario
> distributional comparison
>
> Target audience: non-technical stakeholders, domain economists, potential funders,
> ministry officials. Not developers.
>
> Total runtime: 25 minutes plus Q&A.

---

## Presenter Briefing — Read Before the Room Fills

### What Is New in Milestone 18

Five things are live for the first time:

1. **CI bands on Zone 1A trajectory curves (G1, #1254, ADR-007 full implementation)** —
   The composite trajectory lines in Zone 1A now carry semi-transparent confidence ribbons.
   Width reflects a step-based half-width schedule (±10% at step 1, ±20% at step 2,
   ±35% at steps 3–5, ±50% beyond step 5) scaled by the scenario data tier (T3 = 1.5×
   multiplier). In Mode 3, bands render at reduced opacity (5%) to avoid obscuring the
   baseline/branch split. In Mode 1 and Mode 2, full opacity (12%). The uncertainty
   envelope is now visible at primary-viewport level, not disclosed only in documentation.

2. **PSP driver decomposition (G2, #1255)** — Zone 1D now shows the dominant causal driver
   category beneath the PSP severity badge at every step: "Driver: fiscal sustainability,"
   "Driver: governance," "Driver: external balance," or "Driver: social stability." Persona 3
   (Andreas, Political Advisor) can cite the specific constraint — not just the severity label.

3. **Counter-scenario comparison with CI bands (G3, #1349)** — `DistributionalComparisonSummary`
   renders in the sticky-bottom of Zone 1B when two or more scenarios are loaded for the same
   entity. It shows poverty headcount differential between the reference scenario and each
   comparator (e.g., "+approximately 342,700 persons below poverty threshold · 298K–398K · T3 · Direction
   stable"). The counter-proposal exists as a specific number with a confidence interval — not
   a narrative assertion.
   **Note (IR-M18-003):** Actual simulation output: 298K–398K. See Frame D narration for
   correct spoken bounds.

4. **Control plane column — Mode 2 and Mode 3 (G4, #1354, ADR-019)** — The control plane is
   now a column-mounted component occupying a dedicated layout zone. Mode 2 shows
   `Mode2ColumnSurface`: scenario identity (name, entity, calibration vintage, step range)
   and an "Enter Active Control" affordance. Mode 3 shows `ControlPlaneColumn`: Form 1 with
   FiscalMultiplier slider (0.1–3.0, step 0.05) and LegitimacyConstraint input; Form 2 with
   seven shock types. When Form 1 is applied, the counter-trajectory branch appears in Zone 1A
   simultaneously with the baseline — no scroll at 1280×800. Lazy-mount optimization removes
   Recharts render cost in Mode 1 and Mode 2.

5. **Zone 3 auditability panel (G5, #1422)** — `DistributionalComparisonSummary` now carries
   an expand/collapse methodology panel. Persona 1 (Lucas, Analytical Economist) can open the
   panel in Zone 1B and read the methodology behind the differential figure — without leaving
   the primary viewport.

**Architecture change from M16 Demo 6:** Demo 7 runs two acts. Act 1 (Senegal) demonstrates
the active-control instrument: can the finance ministry's team find a fiscal multiplier
configuration that avoids the bottom quintile crossing the 0.40 recovery floor? Act 2 (Zambia)
demonstrates the counter-proposal as a quantified differential: three scenarios loaded, the
comparison summary reads "+approximately 342,700 persons" and a confidence interval. The two acts share a
single instrument cluster — the same Zone 1A / Zone 1B / Zone 1C / Zone 1D architecture
serves both scenarios.

### EL Scenario Design Decisions (Recorded at M18 Sprint Planning)

| Decision | Value |
|---|---|
| Act 1 entity | SEN (Senegal) — Article IV consultation context |
| Act 1 mode | Mode 3 Active Control — ControlPlaneColumn Form 1 |
| Act 1 instrument | FiscalMultiplier slider, range 0.5–2.0 for demo, full range 0.1–3.0 |
| Act 1 question | "Is there a configuration that avoids the bottom quintile crossing the 0.40 floor before step 8?" |
| Act 1 outcome | Both YES and NO are valid findings — the answer is the argument |
| Act 2 entity | ZMB (Zambia) — debt restructuring context |
| Act 2 scenarios | Option A (EFF Front-Loaded, IMF-proposed), Option B (EFF Gradual), Option C (Homegrown Programme, Ministry counter-proposal) |
| Act 2 reference scenario | Option C (last in comparison list — convention for Demo 7) |
| Act 2 primary finding | "+approximately 342,700 persons below poverty threshold · 298K–398K · T3 · Direction stable" |
| Step 5d Mode 3 evaluation | Required before live session — see `docs/demo/m18/reviews/scenario-evaluation-mode3-deliberation.md` |
| ExternalSectorModule disclosure | Required per demo-preparation-standard.md Step 3 if SEN scenario uses ExternalSectorModule in Mode 3 (see §Honest Disclosures) |
| Persona 3 (Andreas) | Included in Step 6c audience simulation — PSP driver label is his primary evaluation frame in Act 1 |
| Persona 1 (Lucas) | Included in Step 6c — Zone 3 auditability panel is his primary evaluation frame in Act 2 |

### Who Is in the Room

Assume a mixed audience. Domain economists, programme directors, ministry officials,
potential funders or institutional partners. Technical sophistication varies.

The test they are running for Demo 7 is more demanding than in prior cycles. Demo 6 showed
the distributional argument. Sophisticated stakeholders will now ask the harder question:
"Can the ministry team produce their own counter-proposal — not just read out the model's
distributional diagnosis, but construct and quantify an alternative?"

Demo 7 answers that question in two acts. Act 1 shows the instrument. Act 2 shows the output.

### What They Need to Leave Believing

Three things, in priority order:

1. **The counter-proposal is now an instrument, not a narrative.** The finance ministry team
   does not say "we think alternative conditionality terms would produce better outcomes." They
   adjust the FiscalMultiplier in Form 1, observe the branch trajectory appear in Zone 1A, and
   say "at multiplier 0.8, the bottom quintile does not cross the recovery floor at step 4 —
   under your proposed multiplier 1.5, it does at step 3." That is not an assertion. That is
   a demonstrable, session-specific finding made live at the table.

2. **The uncertainty envelope is disclosed, not hidden.** The CI bands in Zone 1A are not
   error bars expressing model failure. They are the No False Precision principle rendered
   visually: at step 5 on T3 data, the band is ±35% × 1.5. That is a specific epistemic
   claim about what the simulation can say at this data tier. The ministry team can cite the
   band width; it cannot be dismissed as vague.

3. **The counter-proposal differential is a specific number, not a claim.** "+approximately 342,700 persons
   below the poverty threshold, 298K–398K confidence interval, direction stable" is the Act 2
   finding. Not "our programme is better for Zambian people." A specific number, a confidence
   interval, a direction-stability statement. The IMF team must engage with the number, not
   the claim.

---

## Section 1 — The Room (3 minutes)

### What the Presenter Says

> There is a room where this happens.
>
> On one side of the table: a creditor team. They have institutional memory that spans
> decades of programme design. They have proprietary models and a set of assumptions the
> ministry team has never seen fully written down. They have twenty analysts behind them
> who have done this forty times.
>
> On the other side: a finance ministry. Three economists. Public data. A question they
> have twelve seconds to answer.
>
> In prior demonstrations, we showed you that WorldSim can name which cohort crosses which
> threshold at which step — and that it labels the confidence tier on the demographic weight
> rather than hiding inference behind a plausible number.
>
> Today we show you the next question the ministry team can answer.
>
> The IMF team has just said: "This is the only viable fiscal adjustment path. We have
> modelled the alternatives."
>
> The finance ministry's team needs to say something specific back. Not "we disagree with
> your assumptions." Not "our people cannot absorb this." Something that must be engaged
> with, not dismissed.
>
> Demo 7 shows that instrument. Two acts: Act 1 — the ministry team tests whether any
> configuration of the IMF's own fiscal multiplier assumption avoids the human cost threshold.
> Act 2 — the ministry team presents the counter-proposal as a specific headcount differential
> with a confidence interval the IMF team must answer.
>
> These are not claims. They are demonstrable, citable findings produced from the ministry's
> own analytical infrastructure.

### What This Establishes

The Demo 7 argument is agency, not just visibility. M16 showed the ministry team what was
happening. M18 shows them what they can say back — in the room, in real time, with a number.

Do not frame this as a warning or a protest capability. Frame every capability as analytical
standing in a negotiation. The ministry is not complaining about conditionality. They are
presenting an alternative with a specific differential.

<!-- TRANSITION -->
*Transition: "Let me show you what that looks like in the room."*

---

## Section 2 — Live Application (10 minutes)

### Presentation Order

Screenshots are presented in argument order: A → B → C → D → E.
See `docs/demo/m18/screenshot-brief.md` for the five-frame brief and capture specs.

Frame A is the Act 1 thesis: active control in operation. Frame B shows the epistemic
transparency layer (CI bands + PSP driver). Frame C shows the Act 1 conclusion (Zone 1B
cohort threshold). Frames D and E deliver Act 2.

### Setup

Application should be running before the room fills. Run `./scripts/demo.sh --milestone 18`
to start the stack. Pre-load:
- SEN scenario (Act 1): 100 quarterly steps, 8-step programme window, `start_date="2024-01-01"`.
  Initial poverty headcount (Q1 informal): per Step 5d recommendation.
  Begin in Mode 2 so "Enter Active Control" transition is visible live.
- ZMB scenarios (Act 2): Option A, Option B, Option C — all three loaded and selectable.
  Option C is last (reference convention). Comparison summary visible at Zone 1B bottom.

**Primary surface (both acts):** Zone 1 instrument cluster — Zone 1A (trajectory + CI bands),
Zone 1B (alert + cohort impact + DistributionalComparisonSummary sticky-bottom), Zone 1C (PMM
widget), Zone 1D (four-framework + PSP severity + driver label), plus control plane column
(Mode 3 only, Act 1). Do NOT narrate the choropleth as the analytical instrument (UX-RULING-4).

<!-- TRANSITION -->
*Transition: "The application is live. Act 1: Senegal, active control."*

---

### Step 1 — Frame A: "The Instrument" (Act 1, Mode 3 Active, Form 1 Applied) (THESIS FRAME)

**What the audience sees:** Senegal. Mode 3 active. `ControlPlaneColumn` visible on the right
side of the instrument cluster. Form 1: FiscalMultiplier slider positioned at **0.85**
(Step 5d confirmed: fm=0.85 = 15% multiplier reduction ≈ 1.5pp primary surplus target reduction).
Zone 1A showing the trajectory at programme completion (step 8) — both the baseline and
counter-trajectory branch have been running since step 3, with the branch history visible in
the applied-inputs log in the column. CI bands present on the trajectory (reduced opacity 5%
in Mode 3). The branch anchor label ("Branched from step 3 — baseline locked") visible in the column.
**Note (IR-M18-001):** By step 8, the financial composite has re-converged (delta 0.00). The
trajectory split is most visually evident in Frame B at step 3 (delta +0.04). Direct the
audience to the control column and the "Applied inputs" record as the evidence of the
counter-proposal being live — not to Zone 1A curve separation.

**What the presenter says:**

> Senegal. Programme complete. Mode 3 — Active Control.
>
> Look at the right column. That is Form 1 of the control plane: FiscalMultiplier. The slider
> is at 0.85. The "Applied inputs" record below it reads: "Step 3 — FiscalMultiplier: 0.85."
> That entry is the counter-proposal. It has been running since step 3.
>
> The column and Zone 1A are simultaneously visible. We have not opened a drawer. We have
> not navigated to a separate comparison view. We set the multiplier, pressed Apply, and the
> branch ran forward from step 3 to step 8 — with the control column still open and the
> applied input still on record.
>
> This is what it means to test a counter-proposal in real time. The analyst configures Form 1,
> presses Apply, and the branch runs forward. In Frame B we will see the trajectory split at
> the moment of application — baseline and branch visible simultaneously at step 3.
>
> The question Act 1 is asking: is there a multiplier configuration — between 0.5 and 2.0 —
> that avoids the bottom quintile income index crossing the 0.40 recovery floor before step 8?
>
> We are going to answer it now, on screen, in this room.

**PAUSE — let them read the Form 1 state and the "Applied inputs" record in the column.**

**Cognitive purpose:** Establish the control instrument as the act-1 capability. The audience
needs to see that Form 1 and Zone 1A are simultaneously visible at 1280×800 — the control
input and the trajectory surface are on the same screen, no navigation required. Frame A
shows the terminal state of the counter-proposal run. Frame B (next) shows the trajectory
split at the moment of application. Together they establish the full workflow: configure →
apply → trajectory branches → cohort outcome visible at step 8.

**Key narration note (UX-RULING-4):** Do NOT say "watch Senegal on the map." Say "Form 1 in
the control column" or "the Applied inputs record confirms the branch has been running since
step 3." Reserve "Zone 1A shows the trajectory split" for Frame B where the split is visually
evident (+0.04 delta at step 3). The choropleth anchors geography. The instruments carry the
argument.

<!-- TRANSITION -->
*Transition: "Now let's look at what this means at the moment the policy is applied."*

---

### Step 2 — Frame B: "The Uncertainty Envelope — CI Bands and the PSP Driver" (Act 1, Step 3)

**What the audience sees:** Senegal at step 3. Zone 1A composite trajectories — both baseline
and branch — with CI bands visible as semi-transparent ribbons around each curve (reduced
opacity in Mode 3). **This is the frame where the trajectory split is visually evident:**
header reads "Financial (step 3) Baseline: 0.50  Branch: 0.54  +0.04" — the +0.04 delta
confirms the baseline and branch have diverged at the moment the multiplier is applied.
Zone 1D PSP section: severity badge (WARNING or WATCH depending on current configuration)
plus the `psp-driver-row` below it: "Driver: fiscal sustainability." Zone 1B alert panel
visible.

**What the presenter says:**

> Step three. Q3 2024. Nine months in. This is the moment the counter-proposal takes effect.
>
> Look at Zone 1A. Two sets of curves. The lower set is the baseline — the IMF's proposed
> terms, fiscal multiplier at 1.0. The upper set is the branch: the trajectories under the
> ministry's counter-proposal at 0.85 — fifteen percent below the programme baseline. The
> split is visible right here, at the moment of application.
>
> Both trajectory sets are on screen simultaneously. We pressed Apply in Form 1 and Zone 1A
> updated — the column still open, the slider still visible, the divergence immediate.
>
> Now look at the bands around each curve. The trajectories carry uncertainty ribbons — the semi-transparent fills
> around each set. The band width is not decorative. It is calibrated: at step 3, the
> half-width is ±35% of the composite value, scaled by the data tier. For Senegal's T3
> demographic data, the tier multiplier is 1.5 — so the band is wider than it would be for
> T1 survey data. The uncertainty envelope is specific to what we know and what we inferred.
>
> The ministry team does not have to defend the band as a model weakness. The band is the
> No False Precision principle on screen. "At T3, our step-3 trajectory carries a ±52.5%
> half-width — that is our disclosed uncertainty at this data tier and step depth." That is
> a citable epistemic position. The IMF's own projections also carry uncertainty; this
> instrument is the first to put it on the primary surface.
>
> Now look at Zone 1D — the political risk panel.
>
> The PSP severity badge reads WARNING. Below it: "Driver: fiscal sustainability."
>
> This is the Milestone 18 Zone 1D delivery. In M16, the severity label told the ministry
> team that political execution risk was under constraint. Now it tells them which constraint
> is dominant. "Fiscal sustainability" means the programme's delivery risk is driven primarily
> by fiscal pressure — not governance fragility or social cohesion breakdown. That distinction
> matters: a fiscal-sustainability-driven PSP risk responds to conditionality relaxation in a
> way that a social-stability-driven risk does not.
>
> Persona 3 — the political advisor on the ministry team — can read Zone 1D and give a
> verbal brief without any interaction: "Programme survival risk is in WARNING territory,
> driven by fiscal sustainability. The political system's implementation capacity is under
> fiscal pressure. Relaxing the multiplier assumption addresses the dominant driver."

**Cognitive purpose:** Establish that the confidence bands and the driver label are not
supplementary disclosures but primary-viewport instruments. The uncertainty envelope and
the driver attribution are not behind a drawer — they are on the same surface as the
trajectory at the same step.

<!-- TRANSITION -->
*Transition: "Five steps later — at programme completion, Zone 1B reads the cohort threshold."*

---

### Step 3 — Frame C: "The Act 1 Finding" (Zone 1B, Step 8 Cohort Threshold)

**What the audience sees:** Senegal at step 8. Mode 3 still active (ControlPlaneColumn
still visible). Zone 1B's CohortImpactSection showing the bottom quintile informal worker
poverty headcount row with its current value and the 0.40 recovery floor. The finding is
one of:
- **If crossing avoided:** Current value above 0.40 at step 8 under the applied multiplier.
- **If crossing not avoided:** Current value at or below 0.40 — the threshold is crossed
  regardless of the multiplier tested.

Both are valid Act 1 conclusions. Read whichever the simulation shows.

**What the presenter says:**

> Step eight. Q4 2025. Two years in.
>
> Zone 1B — the cohort impact section. Bottom quintile informal workers. Poverty headcount.
> Recovery floor: 0.40. That 0.40 floor represents approximately 1.2 million informal sector
> workers in Senegal below the poverty threshold — one-fifth of the informal labour force.
>
> The confidence tier moves to exploratory at step 8 — this reflects the BandingEngine's
> step-depth rule: deeper projections carry wider uncertainty. The directional finding
> remains valid.
>
> **[If the threshold is NOT crossed at the tested multiplier:]**
>
> At FiscalMultiplier 0.8, the bottom quintile poverty headcount at step 8 reads [value from
> screen]. The recovery floor is 0.40. The threshold has not been crossed under this multiplier
> configuration.
>
> That is the ministry team's Act 1 finding: under the IMF's proposed multiplier assumptions,
> the crossing happens. Under the alternative calibration — multiplier 0.8 — it does not.
>
> The ministry team can now say at the table: "Your programme design embeds a multiplier
> assumption. Our analysis shows the bottom quintile threshold crossing is a function of that
> assumption, not an inevitable consequence of the adjustment. We tested the range. Here is
> the configuration that avoids it."
>
> That is not a political argument. It is a technical finding made with the IMF team watching
> the instrument cluster.
>
> **[If the threshold IS crossed regardless:]**
>
> At every multiplier configuration between 0.5 and 2.0, the bottom quintile poverty headcount
> crosses the 0.40 recovery floor before step 8. The crossing happens under [value from screen]
> regardless of the fiscal multiplier assumption in the range we tested.
>
> That is also a finding. The ministry team can say: "We tested the range. The threshold
> crossing is not driven by the multiplier assumption — it is structural to the programme
> design. No adjustment to the fiscal multiplier resolves it. The conditionality itself is
> the factor."
>
> That is a more powerful argument than the objection that the model is wrong. The instrument
> shows the structural constraint. The IMF team must respond to that finding.

**PAUSE — let them read Zone 1B.**

**Cognitive purpose:** Establish that both outcomes are analytically valid and that the
instrument's honesty is the demonstration, not a predetermined result. The Act 1 argument
holds regardless of which outcome the simulation produces — the ministry's team now has
a finding rather than an objection.

**Key narration note on outcome acceptance:** Do not apologise for either finding. If the
threshold is crossed under all tested configurations, say so directly: "This is the most
important finding the tool can produce on this question." If avoided, say: "The ministry team
now has the specific configuration to cite."

<!-- TRANSITION -->
*Transition: "We now shift to Zambia, where the Finance Ministry is negotiating debt restructuring with three competing proposals."*

---

### Step 4 — Frame D: "The Counter-Proposal as a Number" (Act 2, Zambia Comparison)

**What the audience sees:** Zambia. Three scenarios loaded: Option A (EFF Front-Loaded,
IMF-proposed), Option B (EFF Gradual), Option C (Homegrown Programme, Ministry counter-
proposal). Zone 1B sticky-bottom: `DistributionalComparisonSummary`. Visible text (read from
screen):

> Option A vs. Option C: **+approximately 342,700 persons** below poverty threshold
> 298K – 398K  ·  95% CI  ·  T3  ·  Direction stable

Zone 1A shows composite trajectories for all three scenarios with CI bands. Zone 1D PSP
comparison may be visible.

**Presenter note:** The breadcrumb bar shows the reference scenario identifier (Option C).
All three options are loaded and can be compared using the entity selector — the audience
does not need to reload; switching scenarios updates Zone 1A and Zone 1B simultaneously.

**What the presenter says:**

> Act 2. Zambia. Debt restructuring — three scenarios loaded simultaneously.
>
> Option A: the IMF's proposed EFF Front-Loaded programme. Option B: an EFF Gradual variant.
> Option C: the Ministry of Finance's homegrown counter-proposal.
>
> Look at Zone 1B — the bottom of the panel.
>
> The comparison summary reads: "Option A vs. Option C: plus approximately 342,700 persons below poverty
> threshold. 298,000 to 398,000. 95% confidence interval. Tier 3. Direction stable."
>
> Three things about that sentence.
>
> First: it is a specific number. Not "Option A produces worse outcomes for the poor." Three
> hundred and forty thousand additional Zambians below the poverty threshold at programme end
> under Option A compared to Option C. That number must be engaged with. It cannot be
> dismissed as a qualitative objection.
>
> Second: it carries a confidence interval. 298,000 to 398,000. The direction is stable
> across the full uncertainty range — meaning regardless of where within the CI band the
> true value lands, the sign does not flip. The ministry team is not claiming precision they
> do not have. They are claiming direction stability at T3. That is a defensible epistemic
> position.
>
> Third: it is T3. The ministry team can say: "Under T3 demographic weights from available
> Zambian population data, the differential is approximately 342,700. What does your distributional model
> show?" That question — "what does your model show?" — changes the structure of the
> conversation. The IMF team cannot dismiss a T3 finding by citing data quality concerns
> without disclosing the tier of their own distributional projections.
>
> The counter-proposal is not an assertion. It is a specific, tiered, directionally stable
> number that the IMF team must answer.

**PAUSE — let them read the comparison summary.**

**Cognitive purpose:** Deliver the Act 2 core capability: the distributional differential
as a self-contained, citable claim. The sentence in Zone 1B is the Demo 7 thesis made
quantitative.

<!-- TRANSITION -->
*Transition: "And here is how the ministry team defends that number when challenged on methodology."*

---

### Step 5 — Frame E: "The Analytical Defence" (Act 2, Zone 3 Methodology Panel Expanded)

**What the audience sees:** Zambia. Zone 1B with `DistributionalComparisonSummary` visible
and the Zone 3 auditability panel expanded below it. The expanded panel shows the methodology
behind the differential: how the poverty headcount differential was computed, the reference
scenario label, the CI methodology note (BandingEngine, step-based half-width, tier
multiplier), and the confidence tier declaration. All visible in Zone 1B without drawer
navigation.

**What the presenter says:**

> One more thing.
>
> The IMF team has just heard the approximately 342,700 figure. Their next question — and they will ask it —
> is: "What is the methodology behind that number? How did you compute the poverty headcount
> differential?"
>
> In prior milestones, answering that question required explaining the methodology verbally,
> or directing the team to a documentation page, or citing a methodology report that was not
> in the room.
>
> Click the methodology disclosure on Zone 1B.
>
> The panel expands. Without opening a drawer. Without navigating away from the primary
> surface. Without scrolling.
>
> The expanded panel shows: how the differential was computed. The reference scenario
> label. The confidence tier. The uncertainty methodology — BandingEngine, step-based
> half-width schedule, T3 tier multiplier of 1.5. The direction-stability condition.
>
> Persona 1 — Lucas, the analytical economist from the IMF — is sitting across the table.
> This is his primary evaluation frame. He needs to verify the methodology before he accepts
> the approximately 342,700 figure. The expanded panel gives him the chain from input to output, readable
> from the primary viewport, while the comparison summary is still visible above it.
>
> The Zone 3 panel closes the analytical defence loop. The ministry team does not have to
> say "trust our methodology." They can say "expand the panel" — and the methodology is on
> screen.

**Cognitive purpose:** Complete the Demo 7 argument chain: instrument (Act 1) → quantified
finding (Act 2 Frame D) → methodology visible under scrutiny (Act 2 Frame E). The Zone 3
panel is not a UI convenience. It is the epistemic completeness of the counter-proposal
argument.

<!-- TRANSITION -->
*Transition: "The question you will ask is: what gives that number authority? The engine that produced it has been validated against historical crisis cases."*

---

## Section 3 — Backtesting Credibility (3 minutes)

### The Epistemic Problem

> This tool makes specific claims. Specific claims require validation.
>
> The number approximately 342,700 is a simulation output. Before it can be cited at the table, the
> engine that produced it needs a track record. That track record is the backtesting suite.

### The Five Cases

> WorldSim has been validated against five historical crisis cases — each representing a
> distinct crisis mechanism:
>
> **Greece 2010–2012** — fiscal consolidation under external conditionality.
> Directional accuracy at each step. DIRECTION_ONLY.
>
> **Argentina 2001–2002** — sovereign default and convertibility peg collapse.
> Simulated GDP contraction of −10.55% against historical −10.9%. 3.2% deviation.
> MAGNITUDE calibrated.
>
> **Lebanon 2019–2020** — compound crisis cascade. Directional accuracy on both steps.
> DIRECTION_ONLY.
>
> **Thailand 1997–2000** — externally induced currency attack producing domestic
> balance-sheet deterioration. DIRECTION_ONLY.
>
> **Ecuador 1999–2000** — banking collapse and dollarization. The recovery case —
> the fidelity threshold is "do not predict deeper contraction than step one." The model passes.
>
> Honest disclosure for Demo 7: Neither Senegal nor Zambia is a backtested case. The
> trajectories in both scenarios are simulation outputs under configured initial attributes
> and scheduled inputs — not calibrated predictions of either country's actual path.
> The cohort distribution layer is not yet backtested against historical cohort data.
> The five validated cases establish that the engine's crisis transmission mechanisms are
> calibrated. The distributional layer is new from M16. The engine that produced these
> outputs has been validated on five distinct crisis mechanisms; the distributional
> differential methodology is declared at T3.

### What DIRECTION_ONLY Means

> The confidence interval in Zone 1B — 298,000 to 398,000 — is a BandingEngine output
> based on a step-based half-width schedule and data tier multipliers. It is not a posterior
> distribution from a fully Bayesian calibration against historical cohort data. That is
> the next validation layer. The current CI band is a declared uncertainty envelope that
> quantifies what we know about our own uncertainty at this tier and step depth. It is
> honest about what it is.
>
> The "Direction stable" declaration means the sign of the differential does not flip
> anywhere within the 298K–398K band. That is the minimum confidence claim the ministry
> team needs to cite the number: the direction is not an artifact of a point estimate.

<!-- TRANSITION -->
*Transition: "So where does this go from here?"*

---

## Section 4 — What Is Being Built (3 minutes)

### Milestones 1 through 17 — Foundation (Complete)

> The first seventeen milestones built the analytical and trust architecture: simulation
> engine, four measurement frameworks, political economy module, grounding strip source
> provenance, evidence thread tier annotations, Layer 3 self-interpreting trajectory
> sentences, cohort disaggregation on the primary surface, composite trajectory encoding,
> Wave 1 calibration (fiscal-to-cohort elasticity, governance sensitivity, FRAME-D milestone
> sentence), Zone 1B proportional allocation, N=3 multi-scenario comparison infrastructure.
> The control plane column, CI bands, and counter-proposal differential in M18 are only
> credible instruments because everything beneath them was built and validated first.

### Milestone 18 — Full Argument (Current)

> Milestone 18 delivers what you have seen in this demonstration:
>
> **Active control column** — Mode 2 and Mode 3 in a column-mounted layout. The ministry
> team adjusts policy parameters and observes the trajectory branch simultaneously, with
> no scroll required at standard laptop display resolution.
>
> **CI bands on Zone 1A** — The uncertainty envelope is visible at the primary instrument
> level. The epistemic position of the simulation is declared on screen, not in a footnote.
>
> **Counter-scenario comparison summary** — The distributional differential between scenarios
> is rendered as a self-contained, citable sentence: number, confidence interval, tier, and
> direction stability — at Zone 1B, visible without interaction once two or more scenarios
> are loaded.
>
> **PSP driver decomposition** — Zone 1D names the dominant constraint driving political
> execution risk, not just its severity. The ministry's political advisor has a specific
> driver to address.
>
> **Zone 3 auditability panel** — The methodology behind the comparison differential is
> visible in the primary viewport under analytical scrutiny, without drawer navigation.
>
> What you are seeing is working software at v0.18.0, validated against five historical
> crisis mechanisms, with published methodology that anyone can inspect and challenge.

### What Comes Next

> Three capabilities that Demo 7 was designed not to claim:
>
> **Empirically calibrated CI intervals** — The BandingEngine's step-based half-width
> schedule is a structural uncertainty model, not a posterior distribution from historical
> calibration. The path from the current structural CI to an empirically grounded Bayesian
> posterior is documented in ADR-007. It is future work, and the current CI is honest about
> what it is.
>
> **Senegal and Zambia backtesting** — Running the engine against these countries' actual
> Article IV and restructuring histories to establish directional accuracy. The distributional
> layer backtesting follows.
>
> **Human cost constraint floors in Mode 3** — Specifying a Zone 1B threshold as a hard
> constraint on the branch search: the tool finds configurations that avoid the crossing, not
> just tests them one at a time. The distributional visibility in M16 and the control plane
> in M18 are the prerequisites for that capability to be meaningful.

---

## Section 5 — Q&A Preparation

### "How do the CI bands translate to a confidence level? 95%?"

> The CI bands in Zone 1A and the 298K–398K interval in Zone 1B are BandingEngine outputs
> — a step-based half-width schedule (±10% at step 1, up to ±50% beyond step 5) scaled by
> the data confidence tier. The "95% CI" label on the comparison summary reflects the coverage
> convention for the declared interval, not a Bayesian posterior from historical calibration.
> The methodology note in the Zone 3 auditability panel states this explicitly.
>
> The claim the ministry team can make: "Under T3 data and our step-based uncertainty model,
> the differential falls between 298,000 and 398,000 across the declared uncertainty range.
> The direction is stable. What uncertainty methodology does your distributional model use?"
>
> The question turns the uncertainty disclosure into a challenge instrument.

### "What is 'Direction stable' and why does it matter?"

> Direction stable means the sign of the differential — positive (Option A worse for poverty)
> or negative (Option A better) — does not change at any point within the 298K–398K band.
> The approximately 342,700 figure is a point estimate within that band. The point estimate could be off.
> But wherever it lands within the declared uncertainty range, Option A produces more poverty
> than Option C. The direction is not an artifact of a point estimate.
>
> That is the minimum confidence condition for the counter-proposal to be citable. The
> ministry team is not claiming the number is exactly approximately 342,700. They are claiming the direction
> is stable, and they are citing a specific range. That is a defensible evidential position.

### "Why does Zone 1A show two trajectory sets in Mode 3? What is the branch?"

> When Form 1 is applied in Mode 3, WorldSim branches the simulation from the configured
> step: the baseline continues on the original conditionality parameters; the branch runs
> forward with the new multiplier. Both trajectories are visible simultaneously in Zone 1A
> because the purpose of Mode 3 is to compare — not to replace the baseline with the
> alternative, but to hold both on the same step axis at the same time.
>
> The branch anchor is labeled in the control column. The step at which the policies diverge
> is visible. The CI bands on both trajectories reflect the same uncertainty envelope — the
> band is a property of the data tier, not of the policy assumption.

### "What is FiscalMultiplier and where does your assumption come from?"

> The fiscal multiplier is the ratio of GDP change to the fiscal impulse — how much economic
> output changes per unit of fiscal consolidation or stimulus. A multiplier of 1.5 means
> one unit of fiscal contraction produces 1.5 units of GDP decline. The IMF's 2010–2012
> European austerity programmes used multipliers around 0.5; empirical analysis showed they
> ran closer to 1.5. The Blanchard-Leigh 2013 paper is the canonical reference.
>
> In Form 1, the slider range is 0.1 to 3.0. The default is the value embedded in the
> programme scenario. The ministry team is not claiming their preferred multiplier is correct;
> they are demonstrating that the threshold crossing is a function of the multiplier assumption,
> and that the IMF's assumption is contestable. That changes the structure of the conversation
> from "is the model right?" to "what is your multiplier assumption, and why?"

### "What is LegitimacyConstraint in Form 1?"

> LegitimacyConstraint in Form 1 adjusts the `legitimacy_index` parameter in the branch
> scenario — the political economy module's measure of democratic legitimacy and government
> mandate strength. A higher legitimacy constraint means the branch scenario starts from a
> stronger political mandate for programme implementation. It is a second policy lever
> alongside the fiscal multiplier: the ministry team can test whether governance-strengthening
> interventions alter the PSP driver label from "fiscal sustainability" to "social stability"
> or "governance" — and whether that changes the trajectory.

### "The approximately 342,700 figure — is that specific to Zambia's actual data?"

> The differential is a simulation output under configured scenario parameters with available
> Zambian population data at T3 tier — UN WPP 2024 and World Bank WDI. It is not a
> calibrated prediction of what will happen if Option A is implemented. It is what the
> simulation shows under those inputs and that configuration. T3 means Inferred or Available
> Aggregate — we have the aggregate data; the cohort disaggregation uses demographic weighting
> from available sources.
>
> The ministry team's argument is: "Under available T3 data and our methodology — which is
> published and auditable in the Zone 3 panel — the differential is approximately 342,700, direction stable.
> What does your distributional model show for this cohort?" That question is valid at T3.
> It does not require T1 survey data to be worth asking.

### "Why two acts — isn't this one tool?"

> Yes. One instrument cluster. One Zone 1A / Zone 1B / Zone 1C / Zone 1D architecture.
> The two acts demonstrate two different workflows on the same platform: Act 1 shows a
> single-entity active control session (the ministry team tests configurations interactively);
> Act 2 shows a multi-scenario comparison session (three pre-run scenarios compared at once).
> These are two analytical modes on the same surface — the same way a cockpit is one
> instrument cluster serving different phases of flight.

### "Who is this for?"

> The primary user is a debt restructuring specialist or senior economist at a finance
> ministry in a developing or emerging market economy. They have graduate-level economics
> training. They are not data scientists. They need to produce a counter-proposal finding
> in under five minutes, under cognitive load, in a room where they are the only party
> without a hundred analysts behind them.
>
> This tool is not for sovereign wealth fund analysis, trading strategy, sanctions design,
> or any use case where the analytical advantage runs against vulnerable actors rather
> than toward them.

### "What does it cost to run?"

> Open source and free. Infrastructure: a PostgreSQL database and a Python runtime.
> Commodity cloud hardware, negligible cost for a single ministry's analytical load.
> Designed to run on 8GB RAM. No paid APIs, no licensed datasets, no proprietary services.
> All data sources are open-licensed: IMF WEO, World Bank WDI, UN WPP, Natural Earth,
> V-Dem, NOAA Mauna Loa. Methodology published under the same license as the software.

---

## Section 6 — Honest Disclosures (Available If Asked)

These statements must be ready if questions arise. Frame them as evidence that the tool's
epistemic honesty is working. Do not proactively volunteer unless a direct question requires it.

- **Neither Senegal nor Zambia is a backtested case.** Trajectories are simulation outputs
  under configured parameters — not calibrated predictions. SEN and ZMB backtesting are
  future milestone scope.

- **CI bands are structural uncertainty, not empirical posteriors.** The BandingEngine
  uses a step-based half-width schedule and data-tier multipliers. It is not a posterior
  distribution from historical calibration. Disclosed in the Zone 3 methodology panel.
  This is the correct epistemic claim at the current validation stage.

- **Cohort disaggregation is not yet backtested against historical cohort data.** The
  aggregate trajectory is validated against five historical crisis mechanisms. The
  distributional layer uses T3 demographic weights and has not been validated against
  historical cohort outcomes. T3 labels are on screen for exactly this reason.

- **PSP driver decomposition is the dominant single category, not a full weight
  decomposition.** `_attribute_dominant_driver()` identifies the largest contributor to
  PSP change at each step. It is not a full structural decomposition of all contributing
  political economy weights. This is disclosed in methodology documentation.

- **Zone 3 auditability panel is explanatory, not a reproducibility package.** The expanded
  panel shows the methodology narrative and key parameters. It is not a full audit trail
  with every parameter value and intermediate calculation. Full reproducibility is via the
  open-source codebase.

- **ExternalSectorModule is disabled for Act 1.** Reserve dynamics are not modeled in the
  Senegal Mode 3 scenario. Reserve path is identical in baseline and branch — no reserve
  indicator appears on screen. State explicitly if asked: *"Reserve dynamics are outside
  this model window for Act 1 — ExternalSectorModule is not active."*

- **Trajectory design disclosure (Step 5d finding).** The Senegal simulation is seeded with
  Natural Earth geographic classification data (population, GDP stock, economic tier).
  Growth dynamics, fiscal transmission, and cohort welfare trajectories are represented by
  calibrated scenario design — the values accepted at G4 sprint exit (fm=0.85,
  BRANCH_FROM_STEP=3). The trajectories are the *designed* representation of what fiscal
  transmission would produce if IMF WEO macroeconomic data were loaded. The CI bands (T3,
  5% opacity) reflect genuine epistemic uncertainty from the data environment. The
  simulation's qualitative argument — that a 15% multiplier reduction improves HD outcomes
  while maintaining fiscal safety — is consistent with the MacroeconomicModule's causal logic
  (net multiplier 0.68, within SSA LIC consensus range 0.5–0.9, Ilzetzki et al. 2013).
  SEN and ZMB backtesting are future milestone scope.

- **This tool is not for financial advantage or surveillance.** The canonical user is a
  finance ministry counterpart in a negotiation. The tool does not assist in executing
  financial attacks, identifying vulnerabilities in adversaries, or any use case that
  amplifies power asymmetries against vulnerable actors.

---

## Section 7 — The North Star (1 minute)

> I want to close with why this project exists.
>
> There is a quinoa farmer in Bolivia who will never know this tool exists. He does not
> have internet access reliable enough to open a web application. He does not speak the
> language the interface is written in. He has no idea what an IMF programme is, or what
> a fiscal multiplier is, or why it matters.
>
> His government might know. If his government has a finance minister with better analytical
> tools — tools that can say not just "our people cannot absorb this" but "at your multiplier
> assumption, approximately 342,700 additional people fall below the poverty threshold, direction stable,
> and here is the alternative configuration that avoids it" — that minister negotiates better
> terms. Better terms produce different fiscal paths. Different paths produce different
> human consequences.
>
> The quinoa farmer lives at the end of that chain. Every decision we make about this tool —
> what to build first, what to be honest about, what not to oversell — we make as if he
> is watching. Not because he is. But because that framing is the right discipline.
>
> Build it as if he does.

---

## Timing Reference

| Section | Content | Time |
|---|---|---|
| Presenter setup | Stack running, SEN + ZMB scenarios pre-loaded | Before room fills |
| Section 1 | The room — the counter-proposal framing | 3 min |
| Section 2 | Live application (five frames — Acts 1 and 2) | 10 min |
| Section 3 | Backtesting credibility | 3 min |
| Section 4 | What is being built (M18 + horizon) | 3 min |
| Section 7 | North Star closing | 1 min |
| Q&A | See prepared responses above | Remaining time |

Total structured content: 20 minutes. Leave at least 10 minutes for Q&A.
Domain economists will engage most seriously on the CI methodology and the BandingEngine
declaration — have the Zone 3 panel ready to expand on demand. Political advisors will
engage on the PSP driver label. Analytical economists (Persona 1) will push on the Zone 3
methodology panel. Do not compress the CI band explanation.

---

## Screenshot Reference (M18 Demo 7 Frames)

Captured to `docs/demo/m18/screenshots/` via `demo-narrated.spec.ts`.
Five-frame brief and precise capture specifications: `docs/demo/m18/screenshot-brief.md`.

| Presentation order | File | Act | Step | Zone focus | Caption |
|---|---|---|---|---|---|
| 1 — THESIS | `frame-a-the-instrument.png` | Act 1 (SEN) | 8 / 8 | Zone 1A (baseline + branch at programme completion) + CI bands + control column | Mode 3 active: FiscalMultiplier applied. Zone 1A shows baseline and counter-trajectory branch at step 8. Trajectory split is most visually evident in Frame B (step 3, +0.04 delta). |
| 2 | `frame-b-uncertainty-envelope.png` | Act 1 (SEN) | 3 / 8 | Zone 1A CI bands + Zone 1D PSP driver label | CI ribbons on trajectory curves at step 3. Zone 1D: "Driver: fiscal sustainability" beneath severity badge. |
| 3 | `frame-c-act1-finding.png` | Act 1 (SEN) | 8 / 8 | Zone 1B CohortImpactSection — cohort threshold state | Bottom quintile informal workers poverty headcount at step 8 vs. 0.40 recovery floor. Finding: threshold crossed or avoided under tested multiplier. |
| 4 | `frame-d-counter-proposal.png` | Act 2 (ZMB) | terminal / 8 | Zone 1B DistributionalComparisonSummary sticky-bottom | "Option A vs. Option C: +approximately 342,700 persons · 298K–398K · T3 · Direction stable." Zone 1A three-scenario trajectories with CI bands. |
| 5 | `frame-e-analytical-defence.png` | Act 2 (ZMB) | terminal / 8 | Zone 1B Zone 3 auditability panel expanded | Methodology panel open below comparison summary. BandingEngine note, tier multiplier, direction-stability condition visible. |

See `docs/demo/m18/screenshot-brief.md` for the full UX Agent brief and capture specs.

---

*Walkthrough authored by PM Agent, 2026-06-28. Demo prep issue: #1445.*
*Demo prep standard: `docs/process/demo-preparation-standard.md`.*
*Sprint entries: G1–G5 exit documents in `docs/process/sprint-plans/`.*
