# CM + Chief Economist Joint Deliberation — WorldSim Parameter Computation: Structured Input for the EL Manifesto

> **Commissioned by:** Engineering Lead, 2026-07-08
> **Authors:** Chief Methodologist (CM) — Q1, Q2, Q3; Chief Economist (ChE) — Q4, Q5; cross-review: each section reviewed by the other author before filing
> **Purpose:** Structured input for the EL's Parameter Computation Manifesto. This document is not the manifesto. It is the deliberative input the EL requested.
> **Status:** FILED — awaiting EL review and manifesto authorship
> **File authority note:** Filed at `docs/evidence/` under EL commission. Distinct from AEP entries. Normal AEA file authority covers AEP entries and the analytical framework; this is an EL-directed methodology input document outside the AEP production sequence.

---

## Authorship Note — The Chief Economist

The Chief Economist does not appear in the current agent roster (`docs/process/agents.md`). This commission introduces the agent. The Chief Economist speaks for:

- **Macroeconomic theory and empirical method** — beyond the CM's statistical scope, the Chief Economist holds the theoretical models (Mundell-Fleming, DSGE, New Keynesian) and the empirical traditions that give parameter estimates their meaning within a system
- **The political economy of parameter estimation** — who produces economic knowledge, under what institutional constraints, with what incentives, and why two credentialed economists looking at the same data can reach different estimates without either being wrong
- **Community governance of analytical frameworks** — how competing estimates are adjudicated in open-source scientific communities; how methodology drifts when governance is absent
- **Structural limitations of the computation vision** — what cannot be computed from public data for deep architectural reasons, not merely what is technically difficult

The Chief Economist does not duplicate the Development Economist's role (human development impacts), the Political Economist's role (domestic political feasibility), or the Computation Engine Agent's role (computational performance). The distinction from the Chief Methodologist is this: the CM asks "is this procedure statistically valid?" The Chief Economist asks "what does it mean for this procedure to produce knowledge that a finance ministry can act on, and who has standing to contest the result?"

**EL decision required:** Whether to formally register the Chief Economist in `docs/process/agents.md`. The agent has been activated in at least one prior session (M19 headless battle-testing deliberation, 2026-07-02, per `docs/insights-log.md`) but has no formal profile, activation pattern, or working agreement in the roster. This commission is the first deliberation that defines what the agent speaks for — the formal registration remains an EL decision.

---

## Q1 — What does it mean for WorldSim to compute a parameter rather than borrow one?

**CM leads. Chief Economist cross-review in §Q1 CE Review below.**

### The distinction

A **borrowed parameter** is a constant taken from the published literature and inserted into the WorldSim engine as a fixed input. Example: WorldSim currently uses the Ilzetzki, Mendoza, and Végh (2013) fiscal multiplier range for EURO-AREA scenarios. The value (impact multiplier ≈ 0.3–0.4 for advanced economies under fixed exchange rates) was estimated by external researchers using their data, their methods, and their identification strategy. WorldSim adopted it. WorldSim did not test whether it holds for the specific entities, periods, or structural contexts of any particular AEP entry. When results diverge from historical actuals, we cannot distinguish between "our multiplier is wrong" and "IMV13's multiplier was wrong for this case" — we have borrowed a black box.

A **computed parameter** is one WorldSim derives itself, from declared public data, using a declared statistical procedure, producing a point estimate with quantified uncertainty, traceable from inputs to output, and independently reproducible. The computation is WorldSim's institutional claim: this is our best estimate of this parameter, derived this way, under these assumptions, with this uncertainty. We own it.

### The four conditions of ownership

A computation is WorldSim's own if and only if all four conditions hold:

1. **Declared procedure:** The statistical method is written down — the estimator family, identification strategy, any instrument or timing restriction used, and the software implementation — in a WorldSim methodology document. "We applied OLS" is not a declared procedure. "We applied a Blanchard-Perotti (2002) SVAR with two-variable quarterly system on cyclically-adjusted primary balance and real GDP, using the Q3 2005 – Q4 2019 window, with seasonal dummies, on IMF GFS quarterly series GFS-CAB, cross-referenced against WEO series" is a declared procedure.

2. **Traceable inputs:** Every data input to the procedure is named (source, series code, vintage date, URL or repository path), publicly available, and referenced in the WorldSim source registry. An estimate derived from data that cannot be retrieved and verified by a third party is not a WorldSim computation — it is an internal estimate of unknown provenance.

3. **Quantified uncertainty:** The output includes a standard error, credible interval, or declared uncertainty range with its basis (bootstrap, analytical, Bayesian posterior). A point estimate without uncertainty is epistemically identical to a borrowed constant — it makes the same precision claim the literature makes and inherits none of the validation that justifies that claim. If the uncertainty is too large to report honestly, the correct output is a Structural Absence Declaration, not a false precision.

4. **Independent reproducibility:** A technically competent third party — say, a World Bank economist who has read the methodology document and accessed the public data — can rerun the procedure and obtain a result within the declared uncertainty bounds. Reproducibility is not a nice-to-have; it is what separates a scientific computation from an assertion.

### The gray zone: meta-analysis

WorldSim could compute an inverse-variance weighted average of N published fiscal multiplier estimates, adjusting for regime characteristics. This is technically a computation: declared procedure (inverse-variance weighting), traceable inputs (the published studies), quantifiable uncertainty (heterogeneity estimate from the meta-analytic variance). But it is a computation whose inputs are themselves the outputs of other identification strategies WorldSim did not verify. The CM's position: meta-analytic estimation satisfies the four conditions and is therefore WorldSim's computation. But its epistemic weight is lower than a first-principles country estimate, because the computation's validity depends on the validity of each input study — a dependency WorldSim cannot audit at scale. Meta-analytic estimates should be labeled distinctly in the ELASTICITY_REGISTRY: `method: meta_analysis, studies: [...], n: N, heterogeneity: I²`.

### Where the boundary sits

The boundary is not between "hard" and "easy" computation. It is between **declared and undeclared provenance**. A parameter WorldSim computed poorly — with a weak identification strategy, wide uncertainty, and acknowledged limitations — is still WorldSim's own computation if the four conditions hold. A parameter WorldSim computed well but did not document is not. Computation without documentation is indistinguishable from assertion.

---

## Q2 — What public data sources are required, and what is the identification strategy for fiscal multiplier estimation?

**CM leads. Chief Economist cross-review in §Q2 CE Review below.**

### The fundamental identification problem

Fiscal multipliers cannot be estimated by regressing GDP growth on fiscal expenditure. Governments expand spending during downturns (automatic stabilizers, counter-cyclical policy) and contract it during recoveries — this reverse causation systematically biases OLS estimates toward zero or negative, understating the true multiplier. Every identification strategy is an attempt to isolate variation in fiscal policy that is genuinely exogenous to current economic conditions.

### Public data sources required

| Category | Series | Source | Public access | Coverage notes |
|---|---|---|---|---|
| Government expenditure | Expense, grants, total; cyclically-adjusted primary balance | IMF Government Finance Statistics (GFS) | imf.org/gfs | Quarterly available for advanced economies; annual for most LICs; SSA-LIC coverage at annual only for most countries |
| GDP, output gap | Real GDP, output gap estimate | IMF World Economic Outlook (WEO) / World Bank WDI | imf.org/weo, data.worldbank.org | Standard quality; WEO output gap estimates are model-dependent (OECD HP filter method) |
| Interest rates, monetary policy | Policy rate, 10-year sovereign yield | IMF IFS, World Bank WITS | imf.org/ifs | Coverage varies; LIC markets often thin |
| Exchange rate regime | Classification, exchange rate level | IMF AREAER / Ilzetzki-Reinhart-Rogoff classification | Publicly available via publication | Required for regime-conditional multiplier estimation |
| Trade, current account | Exports, imports, BOP components | IMF IFS / WEO | Standard; quarterly for advanced, annual for LICs |
| Commodity prices | World Bank Pink Sheet commodity price index | data.worldbank.org/commodities | Full public access; monthly; long history | Used for commodity instrument approaches |
| IMF programme history | Programme type, date, conditionality | IMF MONA database | imf.org/mona | Publicly searchable; required for narrative identification in programme-context scenarios |
| Policy documents | IMF Article IV consultation reports, Letter of Intent documents | IMF archives | imf.org/publications | Publicly available; required for narrative identification; not machine-readable |

### Identification strategies — a ranked assessment

**Strategy 1: Narrative identification (Romer-Romer 2010; Guajardo-Leigh-Pescatori 2014)**

Mechanism: Identify fiscal actions documented as motivated by deficit reduction or structural adjustment goals rather than by contemporaneous economic weakness. This isolates fiscal shocks that are exogenous to the current business cycle.

Data required: IMF Article IV reports, Letters of Intent, parliamentary records, budget speeches — all publicly available from IMF archives, national finance ministry websites, and parliamentary databases.

Validity: Strongest identification when applied carefully. The Guajardo et al. (2014) "action-based" dataset is the gold standard for advanced economies in programme contexts — directly relevant to WorldSim's primary use case.

Honest limitation: **Labor-intensive at scale.** Each narrative coding requires reading 5–20 documents per country-year and making judgment calls about motivation. For WorldSim's current 11 AEP entities across 4 calibration families, full narrative coding is a 400–800 hour research commitment. This is not a near-term deliverable under current resource constraints. It is, however, the correct aspiration for EURO-AREA and LATAM-EM programme-context scenarios.

**Strategy 2: SVAR with timing restrictions (Blanchard-Perotti 2002)**

Mechanism: In a structural VAR with government spending, taxes, and GDP, impose the identifying assumption that the government cannot change discretionary fiscal policy within the quarter in response to contemporaneous GDP shocks. Automatic stabilizers are controlled for using the OECD semi-elasticity estimates.

Data required: Quarterly fiscal data (IMF GFS quarterly) + quarterly GDP + OECD or IMF semi-elasticity estimates for automatic stabilizers. All publicly available.

Validity: Well-established for advanced economies with quarterly data. The timing restriction is defensible when the political cycle for fiscal legislation is longer than a quarter — broadly true for parliamentary systems.

Honest limitation: **Fails in IMF programme context.** IMF programme conditionality explicitly ties fiscal measures to within-quarter economic triggers — spending cuts are activated or suspended based on quarterly performance criteria. The Blanchard-Perotti timing restriction fails precisely in the context WorldSim uses most. Additionally, quarterly fiscal data coverage for SSA-LIC and SOUTH-SE-ASIAN entities is thin to non-existent — WorldSim's most important calibration families cannot be served by this strategy in the near term.

**Strategy 3: Bartik-style commodity instruments (cross-country application)**

Mechanism: Use exogenous variation in world commodity prices interacted with country-level commodity export exposure as an instrument for export revenue, fiscal revenue, and ultimately fiscal spending. Fiscal spending that responds to commodity windfalls (or collapses) is instrumented by world price movements that a single country cannot affect.

Data required: World Bank Pink Sheet commodity prices (public, monthly), IMF commodity trade data, country-level commodity export shares (UN COMTRADE, public). All publicly available.

Validity: Defensible for commodity-dependent economies in LATAM-EM (ARG, ECU, BOL, PER) and SSA-LIC (ZMB copper, GHA cocoa/gold, SEN phosphate/groundnuts). The instrument has a well-established literature base (Céspedes-Velasco 2012 in the WorldSim ELASTICITY_REGISTRY uses this logic). Cross-entity application is valid within calibration families.

Honest limitation: **Not applicable to import-dependent or service economies.** The instrument loses force for countries where fiscal revenue is decoupled from commodity export prices (GRC, PRT, LKA manufacturing and services). Coverage is also uneven — some commodity exposure data is IMF-reported; some requires COMTRADE processing.

**Strategy 4: Local projection IV (Jordà 2005 + valid instrument)**

Mechanism: Estimate impulse response functions of GDP to fiscal shocks using local projections (direct regressions of GDP at horizon h on fiscal shocks at time 0), instrumented by one of the above strategies. Produces horizon-specific multipliers rather than the impact multiplier alone.

Data required: Same as SVAR + valid instrument from Strategy 1 or 3.

Validity: Increasingly the empirical standard (Ramey 2016 review). More flexible than VAR; better at capturing non-linear dynamics. Combines cleanly with the Bartik instrument for commodity-dependent entities.

Honest limitation: Requires a valid instrument from Strategy 1 or 3 — it is an estimator, not an identification strategy. Produces wider confidence intervals than VAR because each horizon regression is independent. For short annual panels (SSA-LIC), the local projection may run out of degrees of freedom past 3-4 year horizons.

### Summary of identification strategy recommendation

| Calibration family | Recommended primary strategy | Fallback | Near-term feasibility |
|---|---|---|---|
| EURO-AREA | Narrative (Guajardo et al.) | B-P SVAR | Medium — narrative coding required; GRC viable near-term |
| LATAM-EM | Bartik commodity + local projection | Narrative where feasible | Medium — commodity exposure data available |
| SSA-LIC | Bartik commodity + local projection | Annual B-P SVAR where quarterly data exists | Low-to-medium — data coverage limits annual-frequency application |
| SOUTH-SE-ASIAN | Annual B-P SVAR (limited) | Narrative for PAK/LKA IMF programme periods | Low — thin quarterly data; narrative requires IMFMONA coding |

### Honest limitations of all strategies

1. **Multipliers are not structural parameters.** They are reduced-form estimates that change when the policy regime changes. The Blanchard-Leigh (2013) finding — that IMF multiplier estimates during 2010–2011 European austerity were systematically too low because they used pre-crisis panel estimates during a structural break — is the definitive warning. Computing a multiplier from 2000–2019 panel data and applying it to a 2022 crisis scenario carries the same risk. WorldSim's computed multiplier from public data will be a reduced-form historical average. It is not valid as a structural prediction for unprecedented regime shifts.

2. **Small-sample precision is an illusion.** For SSA-LIC entities with 5–8 annual observations in any given programme period, the standard errors on a SVAR or local projection estimate will be very large. A computed estimate with wide uncertainty from 6 data points is honest. Presenting it with the same confidence as an IMV13 meta-estimate based on 50+ country-years is not. WorldSim's computation must acknowledge that for data-poor contexts, the computed uncertainty will be so large that the output may only defensibly be a Structural Absence Declaration.

3. **Fiscal data reliability in LICs is a known problem.** IMF GFS data for SSA-LIC often reflects official reported figures that diverge from IMF-estimated actuals during programme negotiations. The data WorldSim would compute from is the data that the IMF's own economists do not fully trust. Computations from this data inherit that reliability limitation.

---

## Q3 — What is the validation standard?

**CM leads. Chief Economist cross-review in §Q3 CE Review below.**

### What validation is not

Consistency with published literature is not a validation standard — it is a plausibility check. A WorldSim computation that reproduces the IMV13 estimate within its confidence interval has confirmed coherence, not validity. Calibration to the existing literature just means the computation agrees with what WorldSim currently borrows. The purpose of computing our own estimate is to have a check on the literature for the specific entity and context — if the computation always agrees with the literature, the computation adds no information.

### The four validation tests

**Test 1 — Directional backtesting**

For each AEP entry that uses a WorldSim-computed multiplier, compare the harness output direction against historical actuals under the DIRECTION_ONLY fidelity tier. A computed multiplier that fails directional backtesting at a higher rate than the borrowed literature estimate for the same scenario is a validation failure. The benchmark is the current borrowed estimate, not an absolute accuracy standard.

*What failure looks like:* WorldSim computes a multiplier of −0.15 for a LATAM-EM open economy (negative: fiscal expansion contracts GDP via crowding out, consistent with Ilzetzki et al. LAC range). The AEP entry using this computed multiplier shows GDP rising when the historical record shows GDP falling — directional failure. If the borrowed literature estimate would have produced the correct direction, the computation has underperformed its benchmark. This requires a gap brief before the computed estimate can be retained in the ELASTICITY_REGISTRY.

**Test 2 — Uncertainty ordering**

Computed multiplier confidence intervals must be wider for lower data quality contexts and narrower for higher data quality contexts. Specifically:

- A T3 computed estimate (SSA-LIC annual panel) must have wider CI than a T2 computed estimate (EURO-AREA quarterly panel with narrative coding)
- A T2 computed estimate must have wider CI than the ADR-007 CALIBRATED_CI tier (Bayesian posterior with direct country data)
- Any computed estimate with narrower CI than the corresponding CALIBRATED_CI tier is a validation failure — it is claiming more precision than the data quality supports

This test is unusual: it tests whether the computation is *appropriately uncertain*, not whether it is accurate. Overconfident outputs are a category of validation failure, not a style preference.

**Test 3 — Within-family cross-entity consistency**

Two entities in the same calibration family (e.g., SEN and ZMB, both SSA-LIC) whose computed multiplier estimates diverge significantly from each other — more than what can be explained by structural differences (exchange rate regime, trade openness, financial depth) — require explanation. Either the divergence reflects a real structural difference that the computation has captured (good) or an artifact of the thin-data estimation (bad). A computed multiplier that is 3× larger for GHA than for SEN, without a documented structural explanation, is a consistency failure.

**Test 4 — Regime plausibility**

The computed multiplier must produce economically coherent scenario trajectories across the WorldSim scenario library. Specifically: under fixed exchange rates, fiscal multipliers should be larger than under flexible exchange rates (Mundell-Fleming prediction). Under high-debt regimes, multipliers should be smaller or zero due to confidence and crowding-out effects (Ilzetzki et al. finding). A computed multiplier that inverts these relationships must document why — either the structural context genuinely differs, or the computation has failed.

### What constitutes a failed validation

A WorldSim-computed multiplier fails validation if any of the following conditions hold:

1. **Directional backtesting failure:** AEP entries using the computed estimate show higher DIRECTION_ONLY FAIL rates than entries using the corresponding literature range for the same calibration family
2. **Overconfidence:** The computed CI is narrower than what the data quality supports by the uncertainty ordering test
3. **Within-family inconsistency:** Significant unexplained divergence between computed estimates for structurally comparable entities in the same calibration family
4. **Regime incoherence:** The computed estimate inverts the Mundell-Fleming or Ilzetzki et al. regime predictions without structural justification
5. **Non-reproducibility:** A technically competent third party cannot reproduce the estimate within declared uncertainty bounds from the declared inputs and procedure

A failed validation does not mean the computation is discarded. It means: (a) the gap brief is filed by the CM per the Backtesting Eureka obligation; (b) the estimate is retained in ELASTICITY_REGISTRY with a VALIDATION_STATUS: FAILED tag and the specific failure mode recorded; (c) the AEP entries using this estimate carry explicit notation of the failed validation in §6 (Fidelity Assessment); and (d) the estimate is treated as experimental until a revised procedure passes validation.

### Validation is not a one-time event

A computed multiplier that passes validation at the time of computation can fail later as new historical data becomes available. The AEP's backtesting framework is the ongoing validation mechanism — each new AEP entry that covers a period or entity served by a computed estimate is a fresh validation test. The CM is responsible for flagging when a new entry's directional backtesting outcome degrades the computed estimate's validation status.

---

## Chief Economist's Cross-Review of Q1–Q3

**ChE reviews CM's work before filing.**

Q1 is correct and the four-condition framework is precise. One addition: the CM's framing treats computation as a binary status (WorldSim's own vs. borrowed). The Chief Economist adds a middle category the EL should be aware of: **externally-supplied computation** — a computation WorldSim did not perform but whose procedure is fully declared and independently reproducible (e.g., a World Bank researcher publishes a fully reproducible fiscal multiplier estimate for ZMB using a declared SVAR, with replication package on GitHub). This is not borrowed in the problematic sense (no declared procedure) but it is also not WorldSim's own computation (we didn't run it). The manifesto should address this category: what is WorldSim's epistemic relationship to externally-supplied computations with full replication packages? The CM's four conditions probably treat this as "borrowed but well-documented." The Chief Economist believes it deserves a distinct status — provisionally adopted, with a declared adoption rationale — because it changes the community contribution dynamics (see Q4).

On Q2: The CM's ranked assessment of identification strategies is honest and the limitations are correctly stated. The Chief Economist adds one structural limitation the CM omitted: **publication bias in the fiscal multiplier literature.** The published studies WorldSim is computing from or comparing against are not a random sample of all fiscal episodes — they are the episodes that produced clean enough results to be published. Crisis episodes with ambiguous or contradictory outcomes are systematically underrepresented. WorldSim's computed estimates from public data will face the same selection problem if the public data itself reflects only the episodes where data was reliably reported (i.e., not the worst crises). The manifesto should acknowledge that the available public data is biased toward better-functioning contexts, and WorldSim's computation inherits that bias.

On Q3: The four validation tests are well-specified. The Chief Economist endorses the framing that failed validation is a finding, not a failure to be hidden. One tension: Test 1 (directional backtesting) compares the computed estimate against the borrowed estimate as benchmark. This creates a perverse incentive: if the borrowed estimate is well-calibrated for the historical period but wrong for future regimes, a computed estimate that diverges from the literature to capture a structural change would "fail" Test 1. The manifesto should be clear that Test 1 is a relative test, not an absolute one — and that a computed estimate that outperforms the literature on out-of-sample periods is a more significant finding than one that matches the literature in-sample.

---

## Q4 — What is the community contribution pathway?

**Chief Economist leads. CM cross-review in §Q4 CM Review below.**

### The problem this pathway must solve

The multiplier embedded in WorldSim's ELASTICITY_REGISTRY affects the analytical conclusions available to every finance ministry that uses the tool. A Zambian Ministry of Finance economist who knows that the fiscal multiplier for ZMB's copper-dependent open economy in a programme context is meaningfully different from WorldSim's SSA-LIC family estimate has a legitimate claim to be heard — not as a courtesy, but because she holds domain knowledge that WorldSim does not have. The community contribution pathway is the mechanism that converts local expertise into improved methodology without compromising epistemic standards.

A pathway that is too open (accept any estimate from any contributor without review) destroys the engine's methodological integrity. A pathway that is too closed (only WorldSim team estimates accepted) defeats the mission — the tool is supposed to draw on the intelligence of its users, not merely serve them.

### The submission protocol

A contributing economist submits a parameter contribution by opening a GitHub issue using a `parameter-contribution` template (to be created). The template requires:

1. **Parameter identification:** The specific ELASTICITY_REGISTRY entry being contested or supplemented (registry key, current value, current source)
2. **Proposed estimate:** Point estimate or range, with declared uncertainty (standard error or bounds), and scope conditions (which entities, which periods, which structural contexts the estimate applies to)
3. **Data source:** Named public data sources used (source, series, vintage, access path). Proprietary data that cannot be verified by a third party cannot be the sole basis for a contribution.
4. **Identification strategy:** Which of the approaches documented in Q2 was used, or an alternative with declared assumptions. "Expert judgment" is not an identification strategy for this pathway — it is a consultation that informs a future CM computation, not a contribution in itself.
5. **Scope of disagreement:** Does the contributor believe the current estimate is wrong in direction, wrong in magnitude, or valid for different structural contexts than where WorldSim applies it? These three types of disagreement have different implications for the review.

### The review protocol

**Stage 1 — Methodological validity (CM)**

The Chief Methodologist reviews the submission for: (a) whether the identification strategy is valid, (b) whether the uncertainty quantification is honest, and (c) whether the data sources satisfy WorldSim's data quality standards (DAT-STANDARDS.md). The CM's review is pass/fail with required explanations for any failure. A submission that fails Stage 1 is returned to the contributor with a written explanation — not rejected without explanation.

The CM's independence requirement (normally requiring separate session activation per NM-042) applies here. A contribution that arrives in the same session as a CM VALIDATE call should have Stage 1 deferred to a separate CM session. This is a process overhead the pathway must accommodate.

**Stage 2 — Domain plausibility (DIC consultation)**

If Stage 1 passes, the PM Agent activates the relevant DIC member(s) — Development Economist for poverty/human development parameters; Political Economist for governance elasticities; Ecological Economist for environmental cost parameters; Geopolitical Analyst for contagion and external shock parameters. The DIC member reviews whether the proposed estimate produces economically coherent scenario trajectories for the contributing entity and context.

DIC consultation is advisory, not binding. The DIC member records their assessment (consistent with domain knowledge / plausible but outside my expertise / inconsistent with what I know about this context). A DIC member who flags the contribution as domain-inconsistent must be specific — "the proposed multiplier of 0.9 for ZMB is inconsistent with the copper-dependency literature" not "this seems wrong."

**Stage 3 — Adoption decision (EL or delegated panel)**

If Stage 1 and Stage 2 both produce favorable assessments, the adoption decision is made by the Engineering Lead (if the parameter change affects multiple calibration families or alters a widely-used estimate) or delegated to a panel of CM + PM + relevant DIC member (if the change is narrow-scope — one entity, one period).

Possible outcomes:
- **Full adoption:** The contributed estimate replaces or supplements the existing estimate in the ELASTICITY_REGISTRY for the declared scope
- **Conditional adoption:** The estimate is adopted as an alternative for the contributed scope, and the existing estimate is retained for other contexts. AEP entries must declare which estimate they use.
- **Provisional adoption (experimental):** The estimate is flagged as experimental in the ELASTICITY_REGISTRY, pending an AEP entry that tests it against historical actuals. Full adoption requires that the test entry achieves at minimum DIRECTION_ONLY PASS.
- **Non-adoption with record:** The estimate does not meet adoption criteria, but the contribution and the review process are permanently recorded in the ELASTICITY_REGISTRY as a contested-and-reviewed entry. A future contributor who encounters the same question can see what was previously proposed and why it was not adopted.

### The versioning requirement

Every ELASTICITY_REGISTRY entry must include a version history. When an estimate is superseded:
- Prior estimate is retained with version number, source, adoption date, and deprecation rationale
- New estimate enters as the active version with source, adoption date, and review record reference
- AEP entries that used the prior estimate carry a notation: "Uses ELASTICITY_REGISTRY [key] v[N] — see v[N+1] for updated estimate adopted [date]"

This versioning is not optional. An ELASTICITY_REGISTRY that silently overwrites estimates without retaining prior versions is an audit trail violation — future analysts consulting AEP entries will be unable to determine what estimate those entries were actually computed with.

### What prevents drift without deliberation

The primary protection is structural: the ELASTICITY_REGISTRY is a source-controlled file. Changes to it require a commit, a PR, a reviewer (at minimum CM), and a recorded rationale. This structural gate cannot be bypassed by any agent acting within the declared process. A parameter change adopted without a CM-reviewed PR is a process violation of the same severity as implementing a feature without an ADR.

The secondary protection is the contribution record: even non-adopted contributions are retained. A researcher auditing the registry two years from now can see not just what estimates are in use, but what was proposed, reviewed, and declined — and why. This creates an accountability trail that deters silent drift.

### The open question this pathway does not resolve

The pathway above assumes that the identification strategy is the primary basis for adjudication — a better-identified estimate wins, all else equal. But in practice, a Zambian Ministry of Finance economist who says "the multiplier is different here because of X" where X is institutional knowledge (the copper stabilization fund operates differently than the formal fiscal rule suggests; the BCZ behaves differently under programme conditionality than the published IMF assessments indicate) holds a legitimate claim that cannot be fully evaluated by the four-condition framework in Q1. She is not claiming a better statistical identification — she is claiming to know something about the structural context that the published data does not capture.

The pathway as designed handles this case poorly: the CM's Stage 1 review will likely fail the submission if the identification strategy is "I know how the BCZ behaves," even if that knowledge is valid and would improve the estimate. The manifesto must address this gap: is local institutional knowledge a valid input to the ELASTICITY_REGISTRY, and if so, what form does it take and how is it evaluated?

The Chief Economist's position: yes, it should be. The pathway should include a distinct track for **structural context submissions** — not a parameter estimate with an identification strategy, but a documented structural fact about an entity's fiscal context that should modify how the WorldSim procedure is applied. These would be reviewed by the relevant DIC member and the CM jointly (the DIC member assesses structural plausibility; the CM assesses how to translate the structural fact into a parameter adjustment). This track does not currently exist and requires EL decision to create.

---

## Q5 — What are the honest limitations of the computation vision?

**Chief Economist leads. CM cross-review in §Q5 CM Review below.**

### Preamble: permanent vs. contingent limitations

Some parameters cannot currently be computed from public data because of resource constraints or technical gaps — these are **contingent limitations** that may be resolved with investment. Some parameters cannot in principle be computed from public data because of fundamental structural, epistemic, or normative reasons — these are **permanent limitations** that will not be resolved by more data or better methods.

The computation manifesto must distinguish between them. Treating contingent limitations as permanent understates WorldSim's potential. Treating permanent limitations as contingent overpromises and undermines credibility.

### Class 1: Parameters requiring micro-level household data (contingent, but difficult)

**Examples:** Poverty headcount elasticity to GDP growth (Fosu 2011 calibration); consumption quintile shares; distributional consequences of fiscal adjustment by income cohort.

**Why they require micro-data:** These parameters are estimated from household surveys — LSMS, SEDLAC, DHS, national income surveys. The macro relationship (GDP growth → poverty headcount change) is a reduced-form summary of individual-level consumption and income dynamics that can only be recovered from the survey micro-data. The macro aggregates WorldSim accesses (WDI poverty headcount by year) do not contain enough information to identify the elasticity independently.

**Assessment:** Contingent. Household survey data for many WorldSim entities is publicly available (World Bank microdata catalog, SEDLAC). The computation is technically feasible but requires specialized survey econometrics beyond the current engine scope. This is a multi-milestone investment, not a near-term deliverable. Until then: declare the Fosu (2011) source as a **citable literature estimate** rather than borrowing it silently, and document the scope conditions under which it was estimated (SSA cross-country panel, 1990–2010).

### Class 2: Parameters estimated from proprietary or systematically restricted data (contingent in principle, not in practice)

**Examples:** Capital flow sensitivity for LICs (requires BIS locational banking statistics by banking sector, partially restricted); cross-border contagion channels (sudden stop transmission — estimated from SWIFT transaction data, BIS international debt securities data partially public); sovereign spread determinants (requires Bloomberg or Refinitiv data series, not public).

**Assessment:** These parameters have a public-data analog (partial BIS data is public; IMF IFS capital account series exists), but the analog is known to be an imperfect substitute — the public data misses the granularity where the identification strategy requires precision. A computation from the public analog can be declared with an explicit note that it covers only the observable portion of the relevant flow. For spread determinants: the IMF and World Bank publish their own spread decompositions for programme countries; WorldSim can cite these as externally-supplied computations (the middle category the Chief Economist identified in the Q3 review) rather than attempting independent computation.

This class is practically permanent for the current public-data commitment. If the public data axiom (AC-001) is a permanent architectural constraint, sovereign spread estimation from first principles is outside scope, and the manifesto should say so explicitly.

### Class 3: Behaviorally determined parameters with structural breaks (permanent limitation)

**Examples:** Political feasibility scores; elite capture elasticities; social cohesion indices; confidence effect parameters ("sudden stop" in capital flows triggered by political events rather than fundamentals); currency crisis self-fulfilling dynamics.

**Why they cannot be computed from public data:** These parameters are not stable structural relationships. They are emergent properties of specific political configurations, historical path dependencies, individual actor behaviors, and social dynamics that do not aggregate into a stable reduced-form coefficient. A governance composite calibrated on 2000–2020 panel data is not a computation of the "true" governance parameter — it is a behavioral summary of past patterns under past conditions, made by past governments with past institutions.

More fundamentally: for WorldSim's most important use case (a finance minister sitting across from an IMF team), the critical uncertain quantities are precisely the non-quantifiable ones. Will the IMF accept a credible fiscal plan that deviates from programme conditionality? That depends on the negotiating team's personal stances, the G7 political calendar, whether a similar country just failed a programme, and the IMF's internal institutional incentives at that moment. These factors are not computable from public economic data regardless of the identification strategy. They are judgment calls.

**Assessment:** Permanently outside the computation framework for any honest definition of "computation." The manifesto should not promise to compute these parameters from public data. It should promise to declare them as **structural assumptions** — state the assumption, state its basis (is it literature? historical precedent? mission-derived default?), state the conditions under which it would be wrong, and name the DIC member who should be consulted when a scenario makes this assumption load-bearing.

### Class 4: The fiscal multiplier's own permanent limitation

This is the most important honest limitation, because the fiscal multiplier is the flagship parameter the manifesto is primarily about.

The fiscal multiplier estimable from public data is a **reduced-form parameter** — it summarizes the historical correlation between fiscal actions and GDP outcomes, after controlling for as much simultaneity bias as the identification strategy can address. It is not a **structural parameter** in the Lucas (1976) sense — a deep parameter of preferences, technology, or institutions that is invariant to policy regime changes.

The implication, first stated clearly by Blanchard and Leigh (2013): a reduced-form fiscal multiplier estimated from a panel of normal-times fiscal episodes will be systematically wrong during regime shifts — precisely the episodes WorldSim runs most often. When Greece entered the Troika programme in 2010, the fiscal multiplier shifted because: expectations changed (Ricardian effects), monetary policy hit the zero lower bound (eliminating the usual monetary offset), sovereign risk premia spiked (crowding out via risk spreads rather than interest rates), and trade partner fiscal consolidation was simultaneous (the rest of the Euro area was consolidating at the same time, eliminating the export-growth offset).

WorldSim can compute the pre-crisis GRC reduced-form multiplier from public data. It cannot compute the structural parameter that would have been necessary to correctly forecast the GDP contraction under the Troika programme. That computation would require estimating a full New Keynesian DSGE model with Bayesian likelihood methods — a research programme that is outside scope, requires proprietary data inputs, and would take years to complete for a single entity.

**The honest statement the manifesto must make:** WorldSim will compute reduced-form fiscal multipliers from public data. These computations are valid for understanding the historical range of fiscal policy effects under normal-times regimes. They should not be presented as structural estimates valid for regime-change scenarios. When WorldSim runs a scenario that involves a fundamental regime shift (IMF programme entry, default declaration, currency crisis), the fiscal multiplier becomes the most uncertain input in the model — and the manifesto should commit to surfacing this uncertainty explicitly rather than treating the computed multiplier as if it were stable.

### Summary of honest limitations

| Parameter class | Limitation type | EL manifesto commitment |
|---|---|---|
| Poverty/distributional elasticities | Contingent — micro-data required | Declare Fosu (2011) as citable literature; compute from survey data when available; acknowledge regional estimate applied locally |
| Capital flow/spread determinants | Practically permanent — public-data analog incomplete | Declare as externally-supplied or structural assumption; note coverage gap explicitly |
| Behaviorally determined (governance, confidence) | Permanent — not a stable structural relationship | Declare as structural assumptions; name the DIC member responsible for each; state conditions under which assumption is wrong |
| Fiscal multiplier under regime shift | Permanent reduced-form limitation | Compute reduced-form; declare regime-shift uncertainty explicitly; surface elevated uncertainty in scenario outputs where structural break is indicated |

---

## CM's Cross-Review of Q4–Q5

**CM reviews Chief Economist's work before filing.**

Q4 is structurally correct and the three-stage review protocol is implementable. The CM endorses the submission protocol requirements, particularly the requirement for a declared identification strategy as a minimum for any parameter contribution. The "expert judgment" exclusion is appropriate — expert judgment is a consulting input to a CM computation, not a standalone contribution.

One technical addition: the Stage 1 review should include a **prior consistency check** — does the submitted estimate fall within three standard deviations of the current ELASTICITY_REGISTRY estimate for the same scope? If yes, the review proceeds normally. If no, the CM requires explicit documentation of why the structural context justifies the deviation before Stage 1 can pass. This is not a gate that rejects large deviations — it is a documentation requirement that forces the contributor to articulate the structural argument. An outlier estimate that cannot be justified structurally is more likely a data error or methodological mistake than a genuine finding.

On the structural context submission track (the Zambian Ministry economist's institutional knowledge case): the CM endorses the Chief Economist's position that this track should exist, with one condition. Structural context submissions must be translated into a **parameter adjustment with declared direction and magnitude** before they enter the ELASTICITY_REGISTRY — not as narrative text. The CM is responsible for translating the structural fact into a parameter adjustment in consultation with the contributor. If the structural fact cannot be translated into a parameter adjustment with quantified direction and uncertainty, it should be filed as an AEP annotation in the relevant entry, not as an ELASTICITY_REGISTRY modification. The registry requires quantified inputs; annotations accept qualitative structural notes.

On Q5: the CM endorses the four-class taxonomy and the permanent/contingent distinction. One clarification on Class 3 (behaviorally determined parameters): the CM agrees these cannot be computed, but they can be bounded. The governance composite currently uses a parameterized range derived from ICRG and WGI data — both public. WorldSim can compute a distribution over historical governance outcomes for structurally comparable entities to provide uncertainty bounds on the governance parameter, even if the point estimate for a specific entity in a specific political context cannot be computed. The manifesto should distinguish between "parameter cannot be computed" and "parameter cannot be point-estimated" — the distribution over plausible values can often be computed even when the point estimate cannot.

The CM's most important addition on Q5: the manifesto must commit to a **meaninglessness threshold** for each computed parameter. From `docs/DATA_STANDARDS.md` and the synthetic data framework: when uncertainty is so large the output is directionally ambiguous, the correct output is a Structural Absence Declaration, not a wide band. This threshold must be defined per-parameter as part of the computation methodology, not left to case-by-case judgment. A computed fiscal multiplier for an SSA-LIC entity with 5 annual observations may have such wide uncertainty that it cannot reliably distinguish a multiplier of 0.1 from a multiplier of 0.9 — in which case the computed output should trigger a SADeclaration, not a DIRECTION_ONLY claim.

---

## Joint Summary — Three Unresolved Tensions Requiring EL Resolution

### Tension 1: Computation quality vs. resource scope

**CM position:** The narrative identification approach (Romer-Romer; Guajardo et al.) is the correct identification strategy for the programme-context scenarios WorldSim runs most often. It produces the most credible multiplier estimates because it directly addresses the reverse-causality problem by identifying only the exogenous fiscal actions. The manifesto should commit to this approach as the standard.

**Chief Economist position:** Implementing narrative identification for all four calibration families across the current 11 AEP entities requires coding 400–800 documents per country-year, amounting to months of skilled researcher time at the current development pace. This is not a realistic near-term commitment. Committing to narrative identification as the standard, and then delivering Bartik-instrument estimates as the actual implementation, creates a credibility gap worse than honestly committing to the feasible approach.

**The unresolved question:** Should the manifesto commit to the highest-quality identification approach as the long-term standard (with an honest acknowledgment that current deliveries will fall short), or should it commit only to what WorldSim can deliver now (Bartik instruments for commodity-dependent entities; B-P SVAR for entities with quarterly data) while naming narrative identification as a future upgrade? The distinction matters because it changes the citation claims WorldSim makes in AEP entries and public documentation. **EL decision required.**

---

### Tension 2: Community contribution governance vs. CM independence

**Chief Economist position:** The Stage 1 CM review of community contributions is the primary methodological gate. But the CM's independence requirement (per NM-042) creates a slow cycle: each contribution triggers a new CM session, with the associated session startup cost. For a community that produces 10–20 contributions per milestone, this creates a bottleneck that will cause the contribution pathway to be bypassed in practice — contributions will drift in through informal channels (GitHub comments, AEP annotations) rather than the formal pathway, which the pathway exists to prevent.

**CM position:** The independence requirement exists because same-session reviews are structurally compromised — the reviewing agent is exposed to the contributor's framing before forming an independent view. The NM-042 amendment was not a procedural preference; it was a response to a documented failure mode. Relaxing it for community contributions would be a process deviation in precisely the context where the stakes are highest — contributed parameters will be used in analyses that inform real decisions.

**The unresolved question:** Is there a mechanism that preserves CM independence without creating a bottleneck that will cause the pathway to fail in practice? Possible options: (a) a lightweight Stage 0 triage (PM Agent screens for obvious methodological failures; CM independence required only for Stage 1 on submissions that pass triage) — reduces CM calls but doesn't eliminate them; (b) a periodic CM review cycle (monthly or per-milestone) that batches contributions into a single session — preserves independence per submission but introduces lag; (c) a delegated Stage 1 reviewer (a Chief Methodologist-designated reviewer with domain expertise, not the CM agent itself) — but this requires defining who can hold that designation. **EL decision required.** This tension cannot be resolved at the agent level — it requires a governance choice about the independence/efficiency tradeoff.

---

### Tension 3: Where to draw the borrowed/structural assumption line in the current manifesto

**CM position:** Almost all parameters that are currently borrowed from literature could in principle be computed from public data with sufficient investment and methodology development. Declaring any parameter as a "permanent structural assumption" prematurely forecloses future computation. The manifesto should categorize every parameter as "currently borrowed, computation planned" with an honest timeline, rather than creating a permanent structural assumption category that agents and contributors may treat as a ceiling.

**Chief Economist position:** The risk of the CM's framing is that "computation planned" becomes an indefinite deferral with no accountability — the community believes the parameter will be computed, the team knows it won't be, and the gap is never acknowledged. More importantly: for Class 3 parameters (behaviorally determined — governance, confidence effects, political feasibility), the Chief Economist's view is that no additional investment will solve the problem. A governance composite for a specific country at a specific political moment is not computable from public economic data because the causal mechanism runs through institutional arrangements, individual actors, and social dynamics that are not captured in any public dataset at any data quality tier. Calling this "computation planned" misrepresents the nature of the limitation.

**The unresolved question:** Does the manifesto draw a hard line between "can be computed from public data in principle" and "cannot be computed from public data in principle"? The CE argues yes: without a hard line, the manifesto makes implicit promises about parameter computation that mislead users and the community. The CM argues no: the line depends on methodological advances we cannot currently foresee, and drawing it now forecloses options. **EL decision required.** This is ultimately a question about what the manifesto promises and to whom — a mission and governance question, not a statistical one.

---

*CM and Chief Economist attest that each has reviewed the other's sections and that all five questions have received full deliberation. The three tensions identified in this summary are genuine disagreements, not misunderstandings — they require EL resolution, not further agent deliberation.*

*Filed: 2026-07-08 | Branch: `feat/m20-computation-manifesto-input` | EL review flagged in `SESSION_STATE.md`*
