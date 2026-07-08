# The WorldSim Parameter Computation Manifesto

*By Imran Yousuf, Engineering Lead*
*2026-07-08*

---

## The Problem with Borrowed Numbers

WorldSim's engine currently runs on borrowed constants.

When we model what happens to Greek GDP under a Troika austerity programme, we use a fiscal multiplier drawn from Ilzetzki, Mendoza, and Végh (2013): approximately 0.3–0.4 on impact for advanced economies under fixed exchange rates. When we model Zambia's commodity-driven fiscal cycle, we use a range from the same paper's developing-country estimates, adjusted by Céspedes and Velasco (2012). When we trace how a spending cut propagates to Q1 poverty headcount, we use an elasticity calibrated by Fosu (2011) on a Sub-Saharan Africa cross-country panel from 1990 to 2010.

These are good papers. The estimates are defensible. The methodology documentation in our `docs/evidence/analytical-framework.md` and `docs/evidence/TEMPLATE.md` is explicit about which literature source supports which claim, under what conditions, and at what confidence tier.

But there is something epistemically wrong with how we use them. When we borrow a constant from external research and embed it in our engine, we accept it as a black box. We did not run the identification strategy. We did not validate the estimate against our specific entities and scenario periods. When our AEP entries show directional failures, we cannot distinguish between "our multiplier is wrong for this entity" and "the literature's multiplier was wrong for this case." We have accepted someone else's estimate without the ability to audit it or improve it.

This is not a criticism of the literature. It is a description of our own epistemic condition. And it is a condition that is inconsistent with what WorldSim is supposed to be.

WorldSim exists to give a finance ministry the same quality of analytical capability that sophisticated institutions currently reserve for themselves. The IMF does not borrow parameters from external research and insert them as fixed inputs. The IMF estimates its multipliers from its own proprietary models, its own data infrastructure, and its own estimation procedures — procedures the finance ministry across the table cannot inspect, challenge, or reproduce. The asymmetry this tool is designed to correct is not only about who has access to the tool. It is about who has standing to interrogate the numbers inside it.

We cannot credibly claim to be leveling the analytical playing field while running an engine whose parameters are themselves unauditable.

This manifesto is a declaration of what we are going to do about that.

---

## What We Mean by Computing a Parameter

A parameter is WorldSim's own computation if and only if four conditions hold:

**Declared procedure.** The statistical method is written down in a WorldSim methodology document — not just the estimator family, but the identification strategy, the timing restrictions or instruments, the software environment, and the data series codes. A procedure that cannot be written down is not a procedure — it is an assertion.

**Traceable inputs.** Every data input is named, publicly available, and registered in the WorldSim source registry with vintage dates. A computation derived from data that a third party cannot retrieve and verify is not our computation. It is an internal estimate of unknown provenance. This is not a bureaucratic requirement. It is the condition that makes the computation useful to the finance ministry we are trying to serve — because she can open the same sources we used, run the same procedure, and tell us we are wrong.

**Quantified uncertainty.** The output includes a standard error, credible interval, or declared uncertainty range with its basis. A point estimate without uncertainty inherits none of the epistemic standing that estimation is supposed to provide. It is the same kind of claim a borrowed constant makes — a number without a distribution. When uncertainty is so large the output is directionally ambiguous, we do not publish a wide band. We publish a Structural Absence Declaration. That is more honest than a number that cannot support any claim.

**Independent reproducibility.** A technically competent researcher with access to public data and our methodology document should be able to run our procedure and obtain a result within our declared uncertainty bounds. If she cannot, we have not computed anything — we have asserted something in the syntax of computation.

These four conditions define the boundary. A computation that satisfies them is WorldSim's own, regardless of whether it is better or worse than the literature estimate it might replace. A computation that fails any one of them is not ours, regardless of how sophisticated the internal process that produced it was.

There is a middle category worth naming. Some researchers publish fully reproducible estimates with declared procedures, open data, and replication packages. These are not borrowed in the problematic sense — the provenance is auditable. But they are not WorldSim's own computation either. We will call these *externally-supplied computations* and treat them differently from both borrowed constants and WorldSim-computed values: provisionally adopted, with an explicit adoption rationale and full replication package reference in the ELASTICITY_REGISTRY, but subject to the same community review pathway as any contributed estimate.

---

## What We Are Doing Now, and Why It Is Defensible

We are not there yet. This declaration would be dishonest if it implied otherwise.

For most calibration families, WorldSim currently cannot implement narrative identification — the strongest available strategy for fiscal multiplier estimation in programme-context scenarios. Narrative identification requires reading 5–20 policy documents per country-year and coding fiscal actions by motivation. For our current eleven AEP entities across four calibration families, full narrative coding is a commitment measured in hundreds of hours of careful research work. We do not have that capacity now.

What we are doing now:

For **EURO-AREA** entities with quarterly data, we will implement Blanchard-Perotti (2002) SVAR with timing restrictions, as the near-term feasible approach, while working toward narrative identification as the long-term standard.

For **LATAM-EM and SSA-LIC** commodity-dependent entities, we will implement Bartik-style commodity instruments interacted with country export exposure, using World Bank Pink Sheet price data and UN COMTRADE exposure estimates — all publicly available.

For **SOUTH-SE-ASIAN** programme-context entities, we will implement annual SVAR where quarterly data permits, with narrative coding for IMF MONA-documented programme episodes where feasible.

Narrative identification is the highest identification standard we know how to apply for the scenarios this tool runs most often. We are not applying it yet for most calibration families. Bartik instruments and B-P SVAR are defensible interim approaches with known limitations that we are committing to document explicitly. This is honest progress reporting, not a credibility gap. We will say, in every AEP entry that uses an interim approach, which approach was used and why the long-term standard has not yet been applied.

The honest limitation all interim approaches share: the parameters we compute will be reduced-form estimates, not structural parameters. This distinction is not technical. It has direct consequences for how our outputs should be read.

A reduced-form fiscal multiplier estimates the historical correlation between fiscal actions and GDP outcomes, conditional on the identification strategy's assumptions. It is not a deep structural parameter that is stable across policy regimes. Blanchard and Leigh established in 2013 that the IMF's pre-crisis multiplier estimates — themselves estimated from defensible historical data using accepted methods — were systematically wrong during the 2010–2011 European austerity precisely because the regime had shifted. The monetary offset disappeared. Confidence effects spiked. Partner countries consolidated simultaneously.

WorldSim will face the same problem. A reduced-form multiplier estimated from 2000–2009 Greek quarterly data is a correct characterization of that period's fiscal dynamics. It is not a correct characterization of the 2010–2015 Troika period, during which every structural assumption the estimation procedure relied on had changed. This is not a failure of our computation. It is the correct description of what reduced-form estimation can and cannot do.

We commit to surfacing this explicitly. When WorldSim runs a scenario that involves a fundamental regime shift — IMF programme entry, default declaration, currency crisis, zero lower bound on monetary policy — the fiscal multiplier becomes the most uncertain input in the model. Outputs in these scenarios will carry elevated uncertainty flags at the multiplier-dependent indicators, with explicit notation that the estimation period and the deployment context may differ structurally.

---

## What We Will Not Compute, and Why

Not everything can be computed from public data. Some things cannot be computed from public data in principle, not just in practice. We are drawing a hard line, because the alternative — treating every parameter as "computation planned, funding and methodology pending" — would mislead both the community that uses this tool and the team that builds it.

**Behaviorally determined parameters are permanently outside the computation framework.**

Political feasibility scores. Elite capture elasticities. Social cohesion indices. Confidence effects that turn into sudden stops when a government changes. Currency crisis dynamics triggered not by fundamentals but by self-fulfilling beliefs about what other actors will do.

These are not parameters in the sense of stable structural relationships that can be estimated from historical data and applied forward. They are emergent properties of specific political configurations, individual actor decisions, and social dynamics that do not aggregate into a coefficient. A governance composite calibrated on twenty years of ICRG and WGI data captures something real about historical patterns. It does not capture the parameter that will determine whether the current finance minister's credibility survives the programme's first performance review.

More to the point: for the use case this tool was built for — a finance minister sitting across a table from an IMF team — the most consequential uncertain quantities are exactly these non-computable ones. Will the IMF team accept a fiscally equivalent but differently structured proposal? That depends on the team composition, the G7 political calendar, the recent history of other programmes, the finance minister's personal relationship with the mission chief. None of that is in a public dataset. None of it can be estimated from one.

We will declare Class 3 parameters — behaviorally determined, structurally non-computable — as permanent structural assumptions, not computation targets. Each such parameter in our engine will carry: the assumption being made, the basis for it, the conditions under which it would be wrong, and the name of the DIC member who should be consulted when a scenario makes the assumption load-bearing. This is more honest and more useful than a promised computation that will never arrive.

The classification is revisable. If a methodology emerges that satisfies the four conditions above and produces reproducible estimates of political feasibility from public data, we will reclassify. That is not a ceiling — it is a current honest assessment. But we are not going to pretend the work is tractable in order to avoid the discomfort of the limit.

Two other classes of limitation are contingent rather than permanent, and the manifesto is honest about the difference.

**Distributional and poverty parameters** — poverty headcount elasticities, consumption quintile shares, cohort-level consequences of fiscal adjustment — require household survey microdata that macro public aggregates do not contain. The data often exists (World Bank microdata catalog, SEDLAC) but the computation requires specialized survey econometrics beyond our current engine scope. Until we invest in this capacity, we will declare the Fosu (2011) calibration as a citable literature estimate rather than borrowing it silently, and note the scope conditions under which it was estimated.

**Capital flow and sovereign spread determinants** require data granularity — BIS locational banking statistics by sector, SWIFT transaction-level flows, Bloomberg terminal spreads — that is either proprietary or only partially public. Given our permanent architectural constraint against private data inputs (AC-001), sovereign spread estimation from first principles is outside scope. We will cite the IMF's own published decompositions as externally-supplied computations for these parameters.

---

## How the Community Challenges What We Compute

A parameter that cannot be challenged is not knowledge. It is authority. And we are not in the business of authority.

The Zambian Ministry of Finance economist who knows that the fiscal multiplier for Zambia's copper-dependent open economy under programme conditionality differs from our SSA-LIC family estimate is not obligated to accept our estimate because we computed it. She has a legitimate claim to be heard — not as a courtesy, but because she holds structural knowledge about the BCZ's behavior under conditionality that our GFS quarterly panel cannot recover.

We are building a community contribution pathway. The protocol:

A contributing economist opens a GitHub issue with the `parameter-contribution` template — specifying which ELASTICITY_REGISTRY entry she is contesting, her proposed estimate with declared uncertainty, the public data sources and identification strategy she used, and whether she believes the current estimate is wrong in direction, wrong in magnitude, or valid in a different structural context than where we are applying it.

The Chief Methodologist reviews for methodological validity — whether the identification strategy is sound, whether the uncertainty quantification is honest, whether the data sources meet our standards. The CM's review is batched: contributions accumulate in a staging queue and are reviewed in a single dedicated session per milestone. This preserves the CM's independence requirement while keeping the pathway operational. An out-of-cycle review session requires EL direction, not contributor request.

The relevant DIC member reviews for domain plausibility. The Chief Economist reviews for scope validity — whether the estimation strategy's assumptions hold in the structural context the contributor claims. Both reviews are parallel, not sequential.

An estimate that passes all three reviews goes to an adoption decision: full adoption, conditional adoption (for the contributed scope), provisional adoption pending an AEP validation entry, or non-adoption with full record. Non-adopted contributions are permanently retained. A researcher two years from now should be able to see what was proposed, reviewed, and declined — and why.

The ELASTICITY_REGISTRY is versioned. When an estimate is updated, the prior version is retained with its source, adoption date, and deprecation rationale. No parameter change happens without a CM-reviewed PR and a recorded rationale. This structural gate is the primary protection against drift.

There is a gap in the pathway that we are acknowledging publicly rather than papering over. Our submission protocol requires a declared identification strategy. But some of the most valuable local knowledge is not an identification strategy — it is a structural fact about an entity's institutional context. The BCZ behaves differently under conditionality than the formal fiscal rule suggests. The copper stabilization fund's operational rules create a transmission channel the GFS data does not capture. These structural facts are legitimate inputs to how we apply our estimation procedure. We do not yet have a formal track for them. We are committing to build one.

---

## The First Gate

Before any parameter estimate enters the ELASTICITY_REGISTRY as a WorldSim-computed value rather than a literature-borrowed value, a minimum empirical experiment must be run and its results filed.

The experiment is designed for Greece, 2000–2009 estimation period, 2010–2015 holdout. Greece because it has the best data infrastructure of any entity currently in our portfolio, an existing AEP entry against which we can test the holdout, and an independent cross-check available from the ADR-007 Bayesian posterior. The estimation window ends before the Troika programme. This is a hard constraint.

We will run a Blanchard-Perotti SVAR on discretionary fiscal change and real GDP growth, with bootstrap confidence intervals, and use IMF Article IV narrative codes for 2000–2009 as an instrument check. We will compare the computed estimate against the Ilzetzki et al. literature range, note where and why they differ, and then apply the computed multiplier to AEP-001's holdout period.

We expect the holdout test to reveal the Blanchard-Leigh regime-shift problem. The reduced-form multiplier estimated from pre-crisis Greece is expected to underperform during the Troika period, because the structural context changed in ways that reduced-form estimation cannot capture. That is the finding we are designing the experiment to surface. Confirming it is not a failure. It would be a failure to design the experiment so that it cannot reveal this.

The experiment succeeds if: the procedure satisfies all four conditions, the confidence intervals are appropriately wide for a ten-year quarterly panel, the comparison to the literature is filed before any registry entry is made, and — if the holdout fails directionally — a gap brief is on record explaining why. A holdout directional failure with a documented interpretation is a successful learning experiment. A holdout directional failure with no interpretation is a number that does not know why it is wrong.

This experiment is the template. Every subsequent WorldSim computation will have the same structure: a declared estimation period that ends before the holdout period, a holdout test against an AEP entry, a comparison document filed before registry entry, and CM plus Chief Economist sign-off. We will not claim a computed value without this record on file.

---

## What This Means in Practice

Three categories govern every parameter in WorldSim's engine from this point forward.

**Category A — WorldSim-computed.** The four conditions hold. The estimation procedure is declared. The inputs are public and traced. The uncertainty is quantified. The result is reproducible. A holdout test has been run and its results are on file. These parameters carry `method: computed_[procedure]` in the ELASTICITY_REGISTRY, with estimation period, holdout result, and sign-off dates.

**Category B — Citable literature estimate.** The parameter is borrowed from published research, but the borrowing is declared — not embedded silently. The source paper is named, the scope conditions under which it was estimated are documented, the calibration family it applies to is specified, and the confidence tier reflects the fact that we have not independently verified the estimate for our specific entities. These parameters carry `method: literature, source: [citation], scope: [conditions]` in the ELASTICITY_REGISTRY.

**Category C — Structural assumption.** The parameter is permanently outside the computation framework because it is not a stable structural relationship. The assumption being made is stated explicitly. Its basis is documented. The conditions under which it would be wrong are named. The DIC member responsible for flagging when this assumption becomes load-bearing in a scenario is identified. These parameters carry `method: structural_assumption, basis: [source], failure_conditions: [stated]` in the ELASTICITY_REGISTRY.

Every parameter currently in the ELASTICITY_REGISTRY is Category B or C. We will not relabel any parameter as Category A until it has been through the four-condition process and the minimum experiment gate. We are not starting from a clean slate and claiming we already have computed values. We are starting from an honest inventory of what we currently have and building the infrastructure to do better.

The finance minister across the table from the IMF team does not need WorldSim to have perfect parameters. She needs WorldSim to know the difference between what it has verified and what it has borrowed, and to tell her which is which — so that when she puts a number on the table, she knows what she is claiming and what she is not.

That is what this manifesto commits to.

---

*Filed: 2026-07-08*
*Authority: Engineering Lead*
*Governing inputs: `docs/evidence/computation-manifesto-input.md` (CM + Chief Economist joint deliberation)*
*Architectural constraints: `docs/architecture/constraints.md` AC-001, AC-002*
*Agent registration: Chief Economist formally registered `docs/process/agents.md` 2026-07-08*
