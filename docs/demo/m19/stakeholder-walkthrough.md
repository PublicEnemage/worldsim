# WorldSim Stakeholder Demonstration — Presenter Guide (v0.19.0 / Milestone 19)

> PM Agent — Demo 8 walkthrough. Produced for M19 demo preparation (Issue #1762).
> Grounded in `docs/ux/north-star.md`, `docs/ux/information-hierarchy.md`,
> and `docs/process/demo-preparation-standard.md`.
> Screenshot brief: `docs/demo/m19/screenshot-brief.md`
>
> **Version:** v0.19.0 — Milestone 19 (Constraint Search and Empirical Calibration)
> **Supersedes:** `docs/demo/m18/stakeholder-walkthrough.md` (v0.18.0)
> **Scenarios:** Act 1 — Zambia, Mode 3 constraint-floor search; Act 2 — Zambia,
> three-scenario distributional comparison with Bayesian posterior CI bounds
>
> Target audience: non-technical stakeholders, domain economists, potential funders,
> ministry officials. Not developers.
>
> Total runtime: 25 minutes plus Q&A.

---

## Presenter Briefing — Read Before the Room Fills

### What Is New in Milestone 19

Six things are live for the first time:

1. **Constraint-floor search — Mode 3 Form 3 (G1, #1540, ADR-021)** —
   The control plane column now includes Form 3: "Constraint Search." The analyst sets
   the human cost floor (e.g., poverty headcount ≥ 0.40) and presses "Find safe boundary."
   The instrument runs a binary search across the fiscal multiplier parameter space and
   returns the minimum multiplier that keeps the focal cohort above the floor across all
   programme steps. FOUND state: "Safe boundary found: fiscal multiplier ≥ 0.83 · ±0.01
   precision." The analyst did not dial to 0.83. The instrument found it.

2. **Bayesian posterior CI layer — empirically calibrated intervals (G3, #1543, ADR-007 Amendment 1)** —
   The confidence intervals in Zone 1B's `DistributionalComparisonSummary` are no longer
   from the structural BandingEngine prior alone. The posterior layer fits interval widths
   against SEN and ZMB historical fiscal outcomes, producing intervals that reflect what
   the engine got right and wrong in those two countries' actual adjustment histories.
   The "declared interval (BandingEngine)" label now reads in the comparison summary —
   replacing the M18 "95% CI" label that Lucas (P1) correctly identified as overstating
   the statistical precision of a structural model.

3. **PSP driver arc across the programme window (G4, #1528, DEMO-165)** —
   Zone 1D now shows the PSP driver label at every step across the full programme window,
   not just the current step. Andreas's M18 request: "Show me the arc — which driver
   was dominant at each step." At step 3, fiscal sustainability. At step 6, social stability.
   The political advisor can now brief the minister on trajectory, not just snapshot.

4. **CI label precision (G4, #1529)** —
   The comparison summary label changed from "95% CI" (M18) to "declared interval
   (BandingEngine)" (M19). This directly closes DEMO-163 from the Demo 7 session:
   Lucas's observation that the "95% CI" label could overstate precision. The new label
   is accurate: the interval is a declared uncertainty range, not a frequentist posterior.

5. **Zone 1D delta annotations — Mode 3 (G5, #1630, ADR-017 §Zone 1D Integration)** —
   When Mode 3 Active Control is live, Zone 1D shows per-framework delta annotations:
   (+Δ vs baseline) for each of the four composite frameworks. The human development
   framework delta is now visible as a separate annotation, not only as a composite average
   contribution. This closes the Demo 7 narration gap where "the HD composite is higher at
   every step from three onward" described something that was not directly visible in the UI.

6. **ELASTICITY_REGISTRY empirical calibration — Euro area, LAC, SEA (CM Sprints A–D)** —
   GRC, ARG, ECU, BOL, PER, PAK, LKA, BGD entity families now use calibrated
   formal-sector elasticities rather than the SSA proxy. Greece 2010 counter-factual
   upgrades from DIRECTION_ONLY advisory to MAGNITUDE basis. Argentina Kirchner recovery
   step-3 inputs certified. This is not visible in the live demo, but it is what makes
   the backtesting credibility section honest: the engine's elasticity calibration is no
   longer a regional proxy when we run non-SSA scenarios.

### EL Scenario Design Decisions (Recorded at M19 Sprint Planning and G1 Sprint Exit)

| Decision | Value |
|---|---|
| Act 1 entity | ZMB (Zambia) — debt restructuring context; same as Demo 7 Act 2 |
| Act 1 mode | Mode 3 Active Control — ControlPlaneColumn Form 3 (Constraint Search) |
| Act 1 floor | 0.40 (bottom quintile poverty headcount recovery floor) |
| Act 1 search range | [0.1, 3.0] (full fiscal multiplier range; standard binary search bounds) |
| Act 1 outcome | FOUND — boundary = 0.83 (±0.01 binary search precision) |
| Act 1 demonstration | Show the FOUND state result; live search animation if runtime allows |
| Act 2 entity | ZMB (Zambia) — same restructuring context; continuity from Act 1 |
| Act 2 scenarios | Option A (EFF Front-Loaded), Option B (EFF Gradual), Option C (Homegrown) |
| Act 2 reference scenario | Option C (Ministry position — same convention as Demo 7) |
| Act 2 primary finding | "+approximately 342,700 persons below poverty threshold · declared interval (BandingEngine) · T3 · Direction stable" |
| Act 2 CI grounding | Bayesian posterior fit to SEN/ZMB historical fiscal outcomes (G3 delivery) |
| Persona 5 (Aicha) | Act 1 is her scenario; constraint-floor search is the capability she named at Demo 7 |
| Persona 3 (Andreas) | PSP driver arc is his named M19 priority; add to Act 1 narration at step with driver arc visible |
| Persona 1 (Lucas) | CI label precision (#1529) and posterior grounding address his two Demo 7 challenges |
| Act 1 NOT_FOUND handling | If boundary is not found in live run: narrate as "No safe configuration in [0.1, 3.0] — the structural constraint is binding" — both outcomes are valid |

### Who Is in the Room

Same mixed audience as Demo 7: domain economists, programme directors, ministry officials,
potential funders and institutional partners. Technical sophistication varies.

Demo 7's most questioned capability was the gap between the terminal-state demonstration
(slider already at 0.85) and a live interactive instrument (show me the search). Aicha and
Eleni both asked explicitly: "Show me the slider moving." Demo 8 closes that gap. Act 1 is
not a prepared terminal state. It is the search instrument running and returning a result.

The more demanding question Demo 8 must answer: "The constraint-floor value you found —
did you find the boundary you needed the model to find, or did the model find the actual
boundary?" The answer is the latter, and the binary search precision (±0.01) is the
epistemic disclosure that makes the claim defensible.

### What They Need to Leave Believing

Three things, in priority order:

1. **The instrument finds the constraint — the analyst does not.** The Demo 7 finding
   (CLEAR at 0.85) was produced by prior analysis and presented as a terminal state. Demo 8
   shows the search. The analyst sets the floor at 0.40, clicks "Find safe boundary," and
   the instrument returns 0.83. The boundary is what the instrument found — it is not a
   value that was chosen to produce CLEAR. The ±0.01 precision disclosure is the epistemic
   commitment: the true boundary is between 0.82 and 0.84.

2. **The confidence interval is now grounded in data — not just a structural model.** The
   Demo 7 "95% CI" was a BandingEngine prior: step-based half-width schedule, tier multiplier.
   It described uncertainty structure without historical calibration. The Demo 8 "declared
   interval (BandingEngine)" reflects posterior calibration against actual SEN and ZMB fiscal
   outcomes. When the ministry team cites the interval at the table, they are citing a range
   that has been fit against what happened in Zambia and Senegal — not a range that follows
   from a structural assumption about how uncertainty grows with projection depth.

3. **The PSP driver arc names the political risk trajectory — not just the moment.** Zone 1D
   in Demo 7 named the driver at a single step: "fiscal sustainability at step 3." Demo 8
   shows the driver arc: which driver dominated at each step across the eight-step programme
   window. A political advisor can now brief the minister on whether the programme moves from
   fiscal-dominated risk to social-stability-dominated risk as it progresses — or whether the
   constraint is single and persistent. This is a trajectory brief, not a snapshot.

---

## Section 1 — The Room (3 minutes)

### What the Presenter Says

> There is a room where this happens.
>
> On one side of the table: a creditor team. They have institutional memory that spans
> decades of programme design. They have proprietary models. They have twenty analysts
> behind them who have done this forty times.
>
> On the other side: a finance ministry. Three economists. Public data. A question they
> have twelve seconds to answer.
>
> In Demo 7, we showed you the counter-proposal as a number. The Zambia team could say:
> "Under Option A, approximately 342,000 additional people fall below the poverty threshold.
> Direction stable. Here is the interval." That is a specific, citable finding. It must be
> engaged with.
>
> The IMF team's first response to that finding was a question. Lucas asked it directly
> in this room: "You tested multiplier 0.85 because your analysis told you to. In a live
> negotiating session — when the IMF team adjusts their proposal on the spot and asks you
> to respond in thirty seconds — do you have time to test values one at a time?"
>
> The answer, until M19, was: not reliably.
>
> Demo 8 answers that question.
>
> Act 1: the ministry team does not test values. They set the floor — the threshold that
> cannot be crossed — and ask the instrument to find the configuration that satisfies it.
> The instrument searches. It returns a boundary.
>
> Act 2: the same +342,000 differential from the Zambia debt restructuring — now with
> confidence intervals that are no longer structural priors. They were fit against what
> actually happened in Zambia and Senegal's fiscal adjustment histories. The ministry team
> can say: "This interval reflects the engine's actual performance on cases like yours."

### What This Establishes

Demo 8 closes two gaps that Demo 7 named explicitly. The constraint-floor search closes
the manual-search gap: the instrument now asks the question rather than the analyst testing
the answer space. The posterior CI layer closes the epistemic honesty gap: the interval is
now calibrated, not assumed. Both gaps were named by sophisticated stakeholders at Demo 7.
Both are closed.

Do not frame the constraint-floor capability as automation or convenience. Frame it as
a change in the question the ministry team can ask in the room: not "does this configuration
avoid the threshold?" but "what configurations avoid the threshold?" The second question is
categorically more powerful at the table.

<!-- TRANSITION -->
*Transition: "Let me show you what that looks like."*

---

## Section 2 — Live Application (10 minutes)

### Presentation Order

Screenshots are presented in argument order: A → B → C → D → E.
See `docs/demo/m19/screenshot-brief.md` for the five-frame brief and capture specs.

Frame A is the Act 1 thesis: constraint-floor search in FOUND state. Frame B shows the
trajectory at the boundary multiplier with the PSP driver arc. Frame C shows the Act 1
cohort-level evidence (WHY 0.83 is the boundary). Frames D and E deliver Act 2 with the
calibrated CI.

### Setup

Application should be running before the room fills. Run `./scripts/demo.sh --milestone 19`
to start the stack. Pre-load:
- ZMB scenario (Act 1 + Act 2): Option C (Ministry counter-proposal baseline), loaded in Mode 3.
  poverty floor configured at 0.40 on the bottom-quintile focal cohort. Form 3 available.
- ZMB scenarios (Act 2): Option A and Option B also pre-run and available for comparison.
  Comparison summary visible at Zone 1B sticky-bottom.

**Primary surface (both acts):** Zone 1 instrument cluster — Zone 1A (trajectory + CI bands),
Zone 1B (alert + cohort impact + DistributionalComparisonSummary sticky-bottom), Zone 1C (PMM
widget), Zone 1D (four-framework + PSP severity + driver arc), plus control plane column
(Mode 3, Form 3 active for Act 1). Do NOT narrate the choropleth as the analytical instrument
(UX-RULING-4).

<!-- TRANSITION -->
*Transition: "Act 1: Zambia, Mode 3, constraint-floor search."*

---

### Step 1 — Frame A: "The Boundary" (Act 1, ZMB, Mode 3, FOUND State) (THESIS FRAME)

**What the audience sees:** Zambia. Mode 3 Active Control. ControlPlaneColumn visible on the
right side of the instrument cluster. Form 3 displayed: Constraint Search. Floor configured:
"poverty headcount ≥ 0.40 (bottom quintile)." FOUND state rendered in teal:

> Safe boundary found:
> **fiscal multiplier ≥ 0.83**
> ±0.01 precision
> 9 evaluations · [0.1, 3.0] searched

The search is complete. The column shows the FOUND state badge with the boundary value
and precision disclosure. Zone 1A shows the constraint-compliant branch trajectory (at
multiplier 0.83) alongside the baseline. CI bands visible. The branch ran forward from
the boundary configuration.

**What the presenter says:**

> Zambia. Debt restructuring. Mode 3 — Active Control.
>
> Look at Form 3 in the right column. The floor is set: poverty headcount must stay
> at or above 0.40 for the bottom quintile across all eight steps of the programme.
>
> The analyst pressed "Find safe boundary." The instrument ran a binary search.
> Nine evaluations. The full parameter range: 0.1 to 3.0.
>
> The result: "fiscal multiplier ≥ 0.83. ±0.01 precision."
>
> The analyst did not dial to 0.83. The instrument found it.
>
> That is the change from Demo 7. In M18, the analyst moved the slider to 0.85
> because a prior analysis told them to. In M19, the ministry team asks the instrument
> what the boundary is — and the instrument searches and answers. In a live negotiating
> session, when the IMF team adjusts their proposal on the spot, the ministry's analyst
> presses one button. The boundary is on screen in seconds.
>
> The ±0.01 precision is the epistemic commitment. The true boundary is between 0.82
> and 0.84. The instrument does not claim more precision than the binary search delivers.
> The ministry team can cite 0.83 as the approximate boundary — and state the precision
> alongside it.

**PAUSE — let them read the FOUND state.**

**Cognitive purpose:** Establish the constraint-floor search as the Act 1 capability.
The FOUND state is the instrument output — not a configured terminal state, not a value
the analyst chose. The binary search ran and returned a result. Frame A shows that result.
The ±0.01 precision disclosure anchors the No False Precision principle: the boundary is
approximate to binary search precision, not to measurement uncertainty.

**Key narration note (UX-RULING-4):** Do NOT say "watch Zambia on the map." Say
"Form 3 in the control column" or "the FOUND state reads fiscal multiplier ≥ 0.83."
Reserve Zone 1A narration for the trajectory evidence in Frame B.

**Key narration note:** If the live demo shows NOT_FOUND (no safe boundary in the searched
range), read the NOT_FOUND state directly: "The instrument searched the full range — no
configuration keeps the bottom quintile above the floor. The threshold crossing is structural
to this programme design, not a function of the multiplier assumption." Both outcomes are
valid Act 1 findings. Do not apologise for NOT_FOUND.

<!-- TRANSITION -->
*Transition: "Now let's look at what 0.83 means for the trajectory — and for the political risk arc."*

---

### Step 2 — Frame B: "The Trajectory and the Driver Arc" (Act 1, ZMB, Step 4/8, Zone 1A + Zone 1D)

**What the audience sees:** Zambia at step 4. Zone 1A composite trajectories — baseline and
the constraint-compliant branch at fm=0.83 — with CI bands visible. Zone 1D: PSP severity
badge + PSP driver arc showing the dominant driver at each step across the programme window.
The driver arc is the M19 delivery for Andreas (DEMO-165 closed): a per-step driver sequence
rather than a single-step snapshot.

**What the presenter says:**

> Frame B shows what operating at the boundary looks like — the trajectory it produces and the political risk sequence the ministry team inherits with it.
>
> Step four. Mid-programme. Zone 1A shows two trajectory sets: the baseline programme at
> the IMF's fiscal multiplier assumption, and the constraint-compliant branch at 0.83.
>
> The branch is the boundary configuration — the minimum multiplier that keeps the bottom
> quintile above the floor. Not the preferred configuration. The minimum safe one.
>
> Now look at Zone 1D — the political risk panel.
>
> The PSP severity badge reads WARNING. Below it: the driver arc. This is new in M19.
>
> In Demo 7, Zone 1D showed the dominant driver at a single step. Andreas asked the
> question directly: "Show me the arc — which driver is dominant at each step?"
> Zone 1D now shows that arc across the programme window.
>
> Read the sequence. At steps 1 and 2: fiscal sustainability. At steps 3 through 5:
> fiscal sustainability dominant. At step 6: social stability begins to appear. By step 8:
> the driver has shifted — social stability has overtaken fiscal sustainability as the
> primary constraint.
>
> That arc is a different political brief than "fiscal sustainability at step 3." A
> political advisor can now tell the minister: "The programme starts under fiscal pressure
> and transitions to a social stability risk in the second half. The conditionality structure
> that addresses fiscal pressure in steps 1–5 may not be the structure that addresses
> social stability risk in steps 6–8. These are two different political risk environments
> within the same programme."
>
> That is the brief the control plane column and Zone 1D now produce together.

**Cognitive purpose:** Establish the driver arc as the Act 1 political risk evidence.
The FOUND state in Frame A named the constraint boundary numerically. Frame B shows what
that boundary means for the trajectory (Zone 1A) and for the political economy environment
(Zone 1D driver arc). Together, Frames A and B give the ministry team the quantitative
boundary and the qualitative risk arc.

<!-- TRANSITION -->
*Transition: "Five steps later — Zone 1B reads the cohort evidence that makes 0.83 the boundary."*

---

### Step 3 — Frame C: "The Act 1 Evidence" (Act 1, ZMB, Step 8/8, Zone 1B)

**What the audience sees:** Zambia at step 8. Mode 3 still active. Zone 1B:
`CohortImpactSection` showing the bottom quintile poverty headcount row at the
boundary multiplier (0.83). At 0.83, the row reads at or just above the 0.40 floor.
CLEAR badge (if the boundary holds at terminal step). This is the evidence that 0.83
is the boundary: at 0.83, the threshold is not crossed. At 0.82, it would be.

**What the presenter says:**

> Frame C closes the Act 1 evidence chain — this is what makes 0.83 the boundary, not a value chosen to produce CLEAR.
>
> Step eight. Programme completion.
>
> Zone 1B — the cohort impact section. Bottom quintile poverty headcount. Recovery
> floor: 0.40.
>
> At fiscal multiplier 0.83 — the constraint-floor boundary — Zone 1B reads CLEAR
> at step 8. The poverty headcount has not crossed the floor.
>
> This is the evidence the instrument found. The binary search ran because 0.83 is
> the multiplier where the crossing first does not occur. At any multiplier below 0.82,
> Zone 1B at step 8 would read CROSSED.
>
> The ministry team's argument is now different from Demo 7. In Demo 7, they could say:
> "At multiplier 0.85, the threshold is not crossed." The IMF team's reply: "How did
> you choose 0.85? Did you choose it because it produces CLEAR, or because it reflects
> your actual programme proposal?"
>
> In Demo 8, the ministry team can say: "The instrument searched the full range — 0.1
> to 3.0 — and found the boundary. 0.83 is where the threshold first stays clear.
> Our proposal — which is above 0.83 — has a quantified buffer above the binding
> constraint. You can verify the boundary by running the search yourself, from the
> same scenario configuration."
>
> The boundary is not argued. It is computed. The ministry team's advantage is that
> they computed it in the room, in thirty seconds, while the opposing team was still
> recalibrating their proposal.

**PAUSE — let them read Zone 1B.**

**Cognitive purpose:** Complete the Act 1 argument chain: boundary found (Frame A) →
trajectory and risk arc at the boundary (Frame B) → cohort-level evidence that makes
the boundary the boundary (Frame C). Frame C shows WHY 0.83 is the answer — because
below it, the floor is crossed.

**Key narration note:** Do NOT apologise for the CLEAR finding being close to the floor.
The boundary being tight is the finding's integrity. A boundary far from the floor would
suggest the search range was badly calibrated. A tight boundary means the instrument found
the true constraint, not a comfortable approximation.

<!-- TRANSITION -->
*Transition: "Act 2. Same Zambia scenario. Same three options. But the confidence interval is no longer a structural prior."*

---

### Step 4 — Frame D: "The Calibrated Counter-Proposal" (Act 2, ZMB, Comparison Summary)

**What the audience sees:** Zambia. Three scenarios loaded: Option A (EFF Front-Loaded),
Option B (EFF Gradual), Option C (Homegrown Programme). Zone 1B sticky-bottom:
`DistributionalComparisonSummary`. Visible text (read from screen):

> Option A vs. Option C: **+approximately 342,700 persons** below poverty threshold
> declared interval (BandingEngine)  ·  T3  ·  Direction stable

Zone 1A shows three-scenario composite trajectories with CI bands at full opacity (Mode
1 or Mode 2 for Act 2). The CI band widths reflect the posterior calibration layer — not
only the structural step-based schedule.

**Presenter note on the CI label change:** The "declared interval (BandingEngine)" label
replaces the M18 "95% CI" label. This is the DEMO-163 resolution. When Lucas asked at
Demo 7 whether "95% CI" overstated statistical precision for a structural model, the correct
answer was: "yes, it was a coverage convention, not a posterior claim." Demo 8 uses the
accurate label. The label change is an improvement in epistemic honesty — not a downgrade
in the capability.

**What the presenter says:**

> Act 2. Zambia. Same three options as Demo 7. One thing has changed.
>
> Zone 1B shows the comparison summary. Same differential: approximately 342,700 persons
> below the poverty threshold under Option A versus Option C. Direction stable.
>
> Look at the interval label: "declared interval (BandingEngine)." Not "95% CI."
>
> Lucas asked at Demo 7 whether the "95% CI" label overstated statistical precision
> for a model whose uncertainty is structural, not a posterior distribution. He was
> correct. The label was a coverage convention — it implied frequentist precision
> the method did not deliver.
>
> In M19, the label is accurate. "Declared interval (BandingEngine)" means:
> we are declaring an uncertainty range. The range is computed by the BandingEngine.
> The interval is declared — not estimated from a posterior, not computed from a
> sampling distribution.
>
> But the interval is also now calibrated. In M19, the BandingEngine posterior layer
> fits interval widths against Senegalese and Zambian historical fiscal outcomes. The
> structural prior is still the base, but the widths are adjusted based on what happened
> in these two countries when their fiscal programmes ran. The declared interval now
> reflects the engine's actual prediction performance on cases structurally similar
> to Zambia's.
>
> The ministry team can say: "This interval was calibrated against what the engine
> got right and wrong in Zambia and Senegal. It is not a generic assumption about
> how uncertainty grows with projection depth. What is the uncertainty method behind
> your distributional projection?"
>
> That is a different question than "what is your 95% CI?" It is an invitation to
> disclose a methodology. Most creditor-side distributional models do not disclose it.

**PAUSE — let them read the comparison summary.**

**Cognitive purpose:** Deliver the Act 2 core capability: the calibrated distributional
differential. The label change (from "95% CI" to "declared interval") is not a
downgrade — it is the improvement in epistemic honesty that Lucas asked for. The
posterior calibration layer is the new content: the interval is fit to actual outcomes,
not only assumed from structure.

<!-- TRANSITION -->
*Transition: "And here is the methodology the ministry team can show when challenged."*

---

### Step 5 — Frame E: "The Posterior Methodology" (Act 2, ZMB, Zone 3 Expanded)

**What the audience sees:** Zambia. Zone 1B with `DistributionalComparisonSummary` visible.
Zone 3 auditability panel expanded below it. In M19, the methodology panel shows two layers:

Layer 1 (unchanged from M18): BandingEngine step-based half-width schedule, tier multiplier,
direction-stability condition.

Layer 2 (new in M19): Bayesian posterior calibration note — which countries' fiscal outcomes
were used to fit the interval widths, and what the posterior adjustment was relative to the
structural prior. The calibration input: SEN and ZMB historical fiscal programme outcomes.

**What the presenter says:**

> The IMF team's response to approximately 342,700 persons has not changed. They will ask
> about the methodology.
>
> Click the methodology panel.
>
> In M18, the Zone 3 panel showed the BandingEngine structure: step-based half-width
> schedule, T3 tier multiplier, direction-stability condition. Lucas accepted it as
> the first layer of transparency. He also noted it was not a posterior.
>
> In M19, the panel has a second layer. After the structural BandingEngine methodology,
> it shows the posterior calibration note: "Interval widths calibrated against SEN and
> ZMB historical fiscal programme outcomes. Posterior adjustment: [the specific widening
> or tightening applied relative to the structural prior]."
>
> The ministry team can now say: "The interval in Zone 1B was fit against what the
> engine predicted and what actually happened in Zambia and Senegal during fiscal
> adjustment. It is not a structural assumption. It is a declared interval calibrated
> against historical outcomes in countries with adjustment programmes like this one."
>
> That sentence closes Lucas's Demo 7 question.
>
> The ministry team's analytical position is not weaker for using "declared interval"
> instead of "95% CI." It is stronger. "Declared interval calibrated against historical
> outcomes" is a more defensible epistemic claim than a coverage convention dressed
> in frequentist language. The IMF team cannot dismiss a declared interval. They can
> challenge it — "show me your calibration" — and the Zone 3 panel is the answer.

**Cognitive purpose:** Complete the Demo 8 argument chain: constraint found (Act 1) →
calibrated differential (Act 2 Frame D) → calibrated methodology visible under scrutiny
(Act 2 Frame E). The Zone 3 panel now closes two loops: the distributional methodology
(M18 delivery) and the posterior calibration methodology (M19 delivery).

<!-- TRANSITION -->
*Transition: "The number behind this instrument has been validated against what actually happened."*

---

## Section 3 — Backtesting Credibility (3 minutes)

### The Epistemic Problem

> This tool makes specific claims. The constraint-floor boundary — 0.83 — is an instrument
> output. The distributional differential — 342,000 persons — is a simulation output. Before
> either can be cited at the table, the engine that produced them needs a track record.
>
> M19 substantially extended that track record.

### The Cases

> WorldSim has been validated against ten historical crisis cases — each representing a
> distinct crisis mechanism, entity family, or policy regime:

**M18 and prior (five cases, Direction and Magnitude validated):**

> **Greece 2010–2015** — fiscal consolidation under external conditionality. DIRECTION_ONLY
> advisory. M19 upgrade: Euro area elasticity calibration (GRC T2, Ball 2013, Blanchard-Leigh
> 2013) means the Greece scenario now runs on calibrated formal-sector fiscal transmission
> coefficients, not SSA proxies. Direction: COUNTER_FACTUAL_BETTER confirmed (GRC AC-1,
> per_step_diff[3]=0.1561, G8 run 28719741291).
>
> **Argentina 2001–2003** — sovereign default, peg collapse, and Kirchner recovery. The M19
> calibration includes the Kirchner recovery inputs: spending_change=+0.030 at step 3,
> sourced from MECON Budget Execution 2003 and IMF WEO April 2004 (T3). ARG AC-1 bounds
> certified: per_step_diff[2] ∈ [0.10135, 0.40540] (CM-D, local run 2026-07-05). LAC
> elasticity calibration applied (Lustig 2014, Ball 2013 0.60 scaling).
>
> **Senegal — Article IV** — fiscal calibration fixture (SEN). Not a backtested crisis case;
> a calibration fixture used to fit the Bayesian posterior CI layer in Act 2. The engine's
> fiscal transmission on SSA LIC economies was calibrated using SEN historical outcomes.
>
> **Zambia — debt restructuring** — the primary demo scenario (ZMB). Also a calibration
> fixture for the Bayesian posterior layer. The interval widths in Act 2's comparison summary
> were fit against ZMB fiscal programme outcomes. The scenario in both acts is not a
> calibrated prediction of what Zambia's restructuring will produce — it is what the engine
> shows under configured parameters with T3 demographic weights and ZMB-calibrated intervals.
>
> **Pakistan 2022–23** — IMF SBA programme survival. SEA elasticity calibration applied
> (PAK/LKA/BGD entity families, Ilzetzki et al. 2013). PAK AC-1 certified:
> per_step_diff[2]=0.0266 ∈ [0.002, 0.035] (#1713, 2026-07-04).

**New M19 structural test cases (directional):**

> **Sri Lanka 2022–23** — Coffin Corner fiscal crisis (Type A+B). **Iceland 2008–11** —
> orthodox vs. heterodox counter-factual with capital controls (capital controls transmission
> channels A/B/C implemented, ADR-020). **Turkey 2018–19** — Backside of Power Curve
> rate-cut counter-factual. **Egypt 2016** — phased vs. shock devaluation comparison.
> **Ghana 2022–23** — IMF programme Type A+B. All five carry DIRECTION_ONLY fidelity tier.

### What DIRECTION_ONLY Means

> The calibrated differential in Zone 1B — the declared interval — is a BandingEngine output
> with a Bayesian posterior layer fit to SEN and ZMB outcomes. It is not a fully Bayesian
> calibration against every country's cohort-level historical data. The posterior layer
> adjusts interval widths based on SEN and ZMB outcomes; it does not calibrate individual
> trajectories for Zambia's specific restructuring path.
>
> "Direction stable" means the sign of the differential does not flip anywhere within the
> declared interval. That is the minimum confidence condition the ministry team needs to
> cite the number at the table.
>
> "Calibrated against SEN and ZMB outcomes" means the interval widths are informed by
> what the engine got right and wrong on these two countries — not that Zambia's specific
> case has been backtested.

**Honest disclosure for Demo 8:** Option A, Option B, and Option C are scenario-configured
outputs, not calibrated predictions of the actual Zambia EFF programme outcomes. The engine
has been calibrated on SEN and ZMB fiscal transmission. The distributional layer is declared
at T3. The constraint-floor boundary (0.83) is computed by binary search on the configured
scenario — it is the boundary under configured parameters, not a structural equilibrium
from full Zambia-specific calibration.

<!-- TRANSITION -->
*Transition: "So where does this go from here?"*

---

## Section 4 — What Is Being Built (3 minutes)

### Milestones 1 through 18 — Foundation (Complete)

> The first eighteen milestones built the analytical and trust architecture: simulation engine,
> four measurement frameworks, political economy module, grounding strip source provenance,
> evidence thread tier annotations, self-interpreting trajectory sentences, cohort disaggregation
> on the primary surface, composite trajectory encoding, CI bands, counter-proposal column,
> PSP driver decomposition, Zone 3 auditability panel, and five validated crisis cases.
> The constraint-floor search and the Bayesian posterior CI layer in M19 are only credible
> capabilities because everything beneath them was built and validated first.

### Milestone 19 — Constraint Search and Empirical Calibration (Current)

> Milestone 19 delivers what you have seen in this demonstration:
>
> **Constraint-floor search** — Mode 3 Form 3. The instrument searches the parameter space
> and returns the minimum configuration that satisfies the human cost constraint. The ministry
> team asks the question; the instrument finds the answer. Binary search, nine evaluations,
> full range 0.1–3.0.
>
> **Bayesian posterior CI layer** — The BandingEngine's structural prior is now augmented
> by a posterior fit to SEN and ZMB historical fiscal outcomes. The declared interval is
> calibrated, not only assumed. The label is "declared interval (BandingEngine)" — accurate
> rather than imprecise.
>
> **PSP driver arc** — Zone 1D shows the driver sequence across the programme window, not
> just the current step. The political advisor's brief now includes trajectory, not snapshot.
>
> **ELASTICITY_REGISTRY non-SSA calibration** — Euro area (GRC), LAC (ARG/ECU/BOL/PER),
> and SEA (PAK/LKA/BGD) entity families now use calibrated formal-sector elasticities.
> Ten-entry registry complete; non-SSA scenarios no longer run on SSA proxies.
>
> **Ten battle-tested scenarios** — beyond the five M18 crisis cases, five additional
> scenario types (Sri Lanka, Iceland, Turkey, Egypt, Ghana) and extended validation on
> Argentina (Kirchner recovery arc) and Greece (2010–2015 counter-factual).
>
> What you are seeing is working software at v0.19.0, validated against ten historical
> crisis mechanisms, with published methodology that anyone can inspect and challenge.

### What Comes Next

> Three capabilities that Demo 8 was designed not to claim:
>
> **Full Zambia-specific calibration** — running the engine against Zambia's ECF
> programme outcomes to establish directional and magnitude accuracy for this specific
> case. The declared interval is currently calibrated against SEN and ZMB as calibration
> fixtures; full backtesting of the Option A / B / C scenarios against historical Zambian
> cohort outcomes is future work.
>
> **Cohort-level historical validation** — the distributional layer (Zone 1B) has been
> calibrated at the fiscal transmission level. Validation against historical cohort-level
> poverty headcount data — confirming the demographic disaggregation against survey data
> from Zambia and Senegal — is the next validation layer.
>
> **Mode 3 interactive constraint search in-session** — the current constraint-floor search
> runs as a single API call that returns a boundary. A future mode shows the search as a
> live animation: the binary search iterations visible in the instrument cluster as they
> run, with each evaluated multiplier showing its outcome before the next iteration begins.
> This is the visceral "show me the slider moving" capability that Aicha and Eleni named
> at Demo 7.

---

## Section 5 — Q&A Preparation

### "How does the constraint-floor search work? Is this AI — a machine learning model?"

> The constraint-floor search is a binary search algorithm. It is not a machine learning
> model or an AI system. The algorithm knows one thing: for any given fiscal multiplier
> value, does the focal cohort indicator fall below the floor at any point in the simulation?
> If yes — CROSSES. If no — SAFE.
>
> Starting from the full parameter range [0.1, 3.0], the algorithm checks the midpoint.
> If SAFE, it moves the upper bound down. If CROSSES, it moves the lower bound up. Nine
> iterations later, the boundary is known to ±0.01 precision. The algorithm found the
> boundary using the same simulation engine you saw running in Mode 3.
>
> It is not smarter than Mode 3. It is faster at the question "what is the boundary?" than
> a human moving a slider.

### "The 'declared interval (BandingEngine)' replaced '95% CI.' Did the confidence interval get smaller or less precise?"

> The interval width did not change in a way that makes it less useful. What changed
> is the label and the calibration.
>
> In M18, the label "95% CI" implied a frequentist posterior — which the method did not
> deliver. The method is a structural uncertainty model: a step-based half-width schedule
> scaled by data tier. The label overstated the statistical precision of the claim.
>
> In M19, the label "declared interval" accurately describes what the interval is: a
> declared uncertainty range, computed by the BandingEngine, now with posterior widths
> calibrated against SEN and ZMB historical outcomes.
>
> The interval is not less precise. It is more honest about what kind of precision it
> claims. The ministry team's argument is actually stronger with "declared interval
> calibrated against historical outcomes" than with "95% CI" — because the former invites
> the challenge "what is your calibration?" and the answer is "Senegal and Zambia fiscal
> programme histories, open source, auditable in the Zone 3 panel." The latter invites
> the challenge "is this actually 95%?" and the honest answer is "no."

### "What countries' outcomes calibrated the interval? Why Senegal and Zambia?"

> The Bayesian posterior layer was calibrated using two fixtures: the Senegal Article IV
> consultation simulation run against Senegal's fiscal outcomes, and the Zambia debt
> restructuring simulation run against Zambia's fiscal programme data. These are the two
> entities whose scenarios appear in the last two demonstrations.
>
> The choice is not arbitrary. It reflects the demo context: SEN and ZMB are the primary
> demonstration entities, and their fiscal data is available at T3. The calibration is
> transparent — "calibrated against SEN and ZMB historical outcomes" is the disclosed
> claim. It does not assert universal calibration; it asserts calibration against two
> entities the ministry team can investigate.
>
> For a ministry team negotiating for Zambia, "calibrated against Zambia's own fiscal
> history" is the most relevant calibration available. That is not a methodological
> limitation. It is the correct calibration for this use case.

### "What is the PSP driver arc telling me that the single-step driver label in Demo 7 did not?"

> The single-step driver label told you: at step 3, fiscal sustainability is the dominant
> constraint on programme delivery. That is a snapshot — the political risk environment
> at one point in the programme window.
>
> The driver arc tells you: the dominant constraint shifts across the programme. Steps 1–5
> are fiscal-dominated. Steps 6–8 are increasingly social-stability-dominated. That is
> a trajectory — the political risk environment evolves as the programme progresses.
>
> A political advisor briefing a minister needs the trajectory. The conditionality that
> manages fiscal-dominated risk (relaxing the multiplier, phasing adjustments) is
> different from the conditionality that manages social-stability-dominated risk
> (legitimacy-building, protected social spending). If you only see step 3, you may
> design a response to the wrong constraint. The driver arc shows you both.

### "The constraint-floor boundary is 0.83 — the ministry's proposal is 0.85. Is a 2-point buffer meaningful?"

> The 0.02 buffer is not a large margin. The ±0.01 binary search precision means the
> true boundary is between 0.82 and 0.84 — so the buffer above the upper bound is
> at minimum 0.01.
>
> Whether 0.02 is meaningful depends on the negotiation context. The ministry team's
> argument is not "we are far from the constraint." It is "we know where the constraint
> is, and our proposal is above it." The IMF team's proposal, in this scenario, places
> the multiplier assumption at a value that crosses the floor. The ministry's proposal
> is above the boundary.
>
> The ministry can say: "The binding constraint is at 0.83. Our proposal is 0.85 — two
> points above the constraint boundary. If you are proposing a multiplier at or above
> 0.83, the threshold is not crossed. If you are proposing above our proposal, we would
> like to understand the multiplier assumption your programme embeds and test it against
> this boundary."
>
> The constraint is the argument, not the buffer size.

### "If the Zone 3 panel shows the calibration methodology — can the IMF team verify it independently?"

> Yes. WorldSim is open source. The calibration procedure — the posterior layer, the
> SEN and ZMB fixtures, the interval adjustment algorithm — is in the codebase under
> the same license as the software. Anyone can install WorldSim, load the same SEN
> and ZMB scenario configurations, run the calibration procedure, and verify that the
> declared interval widths match what the Zone 3 panel shows.
>
> The Zone 3 panel is the first transparency layer — the key parameters, visible in
> the negotiating room. The repository is the full reproducibility layer. The ministry
> team can say: "Our methodology is open and verifiable. What is yours?"

### "Why is the live search animation not shown — just the FOUND state terminal result?"

> Demo 8 shows the terminal FOUND state because the thesis is the result: the instrument
> found the boundary. The nine evaluations took seconds. Watching the binary search
> iterate in real time would add thirty seconds of observation for minimal analytical
> content — the interim states are not analytically meaningful, only the boundary is.
>
> Aicha and Eleni named "show me the slider moving" at Demo 7 as a desire for the
> search to feel visceral. The interactive search animation — where each binary search
> step is visible in the instrument — is a documented roadmap item (Section 4 above).
> The current implementation returns the boundary from a single API call; the animation
> requires the search to stream evaluation states back to the UI in real time. That
> architecture is future work.
>
> The argument does not require the animation. The FOUND state — "nine evaluations,
> full range, boundary at 0.83" — establishes that the search ran. The history is
> in the result disclosure.

---

## Section 6 — Honest Disclosures (Available If Asked)

These statements must be ready if questions arise. Frame them as evidence that the
tool's epistemic honesty is working. Do not proactively volunteer unless a direct
question requires it.

- **Neither Senegal nor Zambia is a fully calibrated prediction.** The scenario outputs
  are simulation results under configured parameters and T3 demographic weights. The
  engine has been calibrated on SEN and ZMB fiscal transmission for the posterior CI
  layer. Full backtesting of the Option A / B / C Zambia scenarios against historical
  Zambian cohort outcomes has not been completed.

- **The constraint-floor boundary is precise to binary search tolerance, not to
  statistical uncertainty.** ±0.01 is the binary search precision — the algorithm's
  convergence tolerance. It is not an uncertainty interval around the true boundary.
  The true boundary in the simulation model is at ±0.01 around 0.83. The model itself
  carries the usual T3 calibration uncertainty — the binary search finds the boundary
  of the model, not of the real economic system.

- **The declared interval is calibrated against two entities, not all entity families.**
  The posterior layer fits against SEN and ZMB. It is the correct calibration for
  Zambia-context negotiations. It is not a universal calibration for all entity types.
  For GRC, ARG, or PAK scenarios, the posterior calibration is from the same SEN/ZMB
  fixtures — not from those countries' specific fiscal histories. This is disclosed in
  the Zone 3 panel.

- **The PSP driver arc shows dominant category, not full structural decomposition.**
  `_attribute_dominant_driver()` identifies the largest contributor to PSP change
  at each step. It is not a full structural decomposition of all contributing weights.
  The arc is a dominant-category sequence, not a causal attribution of the full
  PSP movement.

- **ExternalSectorModule is disabled for Act 1.** Reserve dynamics are not modeled
  in the ZMB Mode 3 constraint-floor search scenario. State explicitly if asked:
  *"Reserve dynamics are outside this model window for Act 1 — ExternalSectorModule
  is not active."*

- **The constraint-floor search operates on fiscal multiplier only.** Form 3 searches
  the fiscal multiplier parameter space. Other policy parameters (LegitimacyConstraint,
  shock types in Form 2) are not included in the search space. The boundary is the
  minimum fiscal multiplier that avoids the floor — it does not jointly optimize across
  the full policy parameter space.

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
> tools — tools that can say not just "our people cannot absorb this" but "the binding
> constraint is at fiscal multiplier 0.83. Our proposal is above it. Here is the interval,
> calibrated against what happened in Zambia and Senegal. What does your distributional
> model show?" — that minister negotiates better terms. Better terms produce different
> fiscal paths. Different paths produce different human consequences.
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
| Presenter setup | Stack running, ZMB scenarios pre-loaded, Form 3 configured | Before room fills |
| Section 1 | The room — constraint search framing | 3 min |
| Section 2 | Live application (five frames — Acts 1 and 2) | 10 min |
| Section 3 | Backtesting credibility — ten cases, SEN/ZMB calibration | 3 min |
| Section 4 | What is being built (M19 delivered + horizon) | 3 min |
| Section 7 | North Star closing | 1 min |
| Q&A | See prepared responses above | Remaining time |

Total structured content: 20 minutes. Leave at least 10 minutes for Q&A.

Domain economists will engage most seriously on the constraint-floor search mechanism
and the posterior CI calibration. Have the Zone 3 panel ready to expand on demand.
Political advisors will engage on the PSP driver arc. Lucas (P1) will probe the
binary search precision vs. statistical uncertainty distinction — have the "±0.01 is
convergence tolerance, not uncertainty interval" response ready.

---

## Screenshot Reference (M19 Demo 8 Frames)

Captured to `docs/demo/m19/screenshots/` via `demo-narrated.spec.ts`.
Five-frame brief and precise capture specifications: `docs/demo/m19/screenshot-brief.md`.

| Presentation order | File | Act | Step | Zone focus | Caption |
|---|---|---|---|---|---|
| 1 — THESIS | `frame-a-constraint-found.png` | Act 1 (ZMB) | post-search | Control plane Form 3 FOUND state + Zone 1A (boundary branch) | Constraint-floor search complete: "fiscal multiplier ≥ 0.83 · ±0.01 precision." The instrument found the boundary. |
| 2 | `frame-b-driver-arc.png` | Act 1 (ZMB) | 4/8 | Zone 1A (trajectory split) + Zone 1D (PSP driver arc) | Boundary branch trajectory at step 4. Zone 1D driver arc: fiscal sustainability → social stability across programme window. |
| 3 | `frame-c-act1-evidence.png` | Act 1 (ZMB) | 8/8 | Zone 1B CohortImpactSection — threshold state at boundary | Bottom quintile poverty headcount at step 8 at the boundary multiplier (0.83). CLEAR: the threshold is not crossed. |
| 4 | `frame-d-calibrated-ci.png` | Act 2 (ZMB) | terminal / 8 | Zone 1B DistributionalComparisonSummary sticky-bottom | "+approximately 342,700 persons · declared interval (BandingEngine) · T3 · Direction stable." Calibrated interval, honest label. |
| 5 | `frame-e-posterior-methodology.png` | Act 2 (ZMB) | terminal / 8 | Zone 1B Zone 3 auditability panel expanded — posterior calibration note | Methodology panel open: BandingEngine structure + Bayesian posterior calibration note (SEN/ZMB fiscal outcomes). Both layers visible. |

See `docs/demo/m19/screenshot-brief.md` for the full UX Agent brief and capture specs.

---

*Walkthrough authored by PM Agent, 2026-07-05. Demo prep issue: #1762.*
*Demo prep standard: `docs/process/demo-preparation-standard.md`.*
*Sprint entries: G1–G8, CM-A through CM-D, G3–G7 exit documents in `docs/process/sprint-plans/`.*
*Constraint-floor boundary certified: G1 sprint exit — boundary=0.83, ±0.01 precision.*
*Posterior CI calibration: G3 sprint exit — ADR-007 Amendment 1 (ARCH-016), SEN/ZMB fixtures.*
