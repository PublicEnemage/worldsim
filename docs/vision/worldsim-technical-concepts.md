# WorldSim: Technical Concepts and Architectural Reasoning

*Synthesized from the project's technical conversations, April–May 2026*
*Companion to `docs/vision/worldsim-founding-document.md`*

---

## Preface

The founding document explains why WorldSim exists. This document explains how it works and why it works that way.

The founding document was written to preserve the vision before it compressed into bullet points. This document is written for the same reason, applied to the technical layer: the reasoning behind the architecture, the mental models that produced the design choices, and the concepts that are easy to forget between sessions but essential to understand before making decisions that depend on them.

It is written for three readers: the Engineering Lead who needs to remember what was decided and why; the future collaborator who needs to understand the architecture deeply enough to contribute with judgment; and the future agent who needs context that no ADR or GitHub issue fully captures.

Where the founding document covers the problem space and the vision, this document covers the technical reasoning. Both are needed. Neither is sufficient alone.

---

## Concept 1: The Two-Graph Architecture

### The Mental Model That Came First — And Why It Was Almost Right

The Engineering Lead's initial mental model of the simulation was a tree — specifically something resembling a binary search tree where each node can have one-to-many children. Value flows up the parent-child relationship; resources and spending flow down. A nation at the root; regions, sectors, and demographic cohorts as descending branches. The higher the node, the more aggregate its scope.

This mental model is approximately correct — and precisely wrong in one critical respect.

The parent-child hierarchy exists exactly as described. `SimulationEntity` carries a `parent_id` field. The six resolution levels (nation → region → sector → demographic cohort → institution → individual archetype) map directly to the tree structure. Higher nodes represent aggregate scope. This part of the model is right.

What the tree model gets wrong is the propagation medium. In the tree model, effects travel through parent-child edges — up from children to parents, down from parents to children. This seems intuitive. It is incorrect.

Effects in WorldSim do not travel through the parent-child hierarchy at all. They travel through a completely separate structure: the **relationship graph**.

### The Two Graphs

`SimulationState` contains two distinct structural layers:

**Graph 1 — The Identity Hierarchy (the tree):**
The `parent_id` relationships. This is the administrative scope structure. It tells you what each entity *is* — Greece is a nation, Attica is a region within Greece, the manufacturing sector is a sector within Attica, the bottom income quintile is a demographic cohort within the manufacturing sector. This structure represents identity and scope. It is how you navigate the hierarchy. It is not how effects propagate.

**Graph 2 — The Relationship Graph (the propagation medium):**
`SimulationState.relationships` — a list of `Relationship` objects, each carrying `source_id`, `target_id`, `relationship_type` (trade, debt, alliance, currency union), and `weight`. These relationships do not follow the parent-child tree. Greece has a trade relationship with Germany. GRC and DEU are peers at Level 1 — neither is the parent of the other. A currency union creates edges between countries at the same hierarchical level. A debt relationship between Greece and the IMF creates an edge to an institution that isn't in the administrative hierarchy at all.

When an event fires at an entity, `PropagationRules` specify which event types travel along which relationship edge types, with what attenuation factor, to what maximum depth. A fiscal contraction event at GRC propagates to DEU because there is a `trade` relationship edge between them with a specific weight — not because Germany is Greece's parent in some administrative hierarchy.

### Why This Matters

The practical implication: **the identity hierarchy is the map; the relationship graph is the road network.** Knowing that Attica is a region within Greece tells you what Attica is. It tells you nothing about how a currency crisis in Turkey propagates to Greek exports. For that, you need the relationship graph — the typed, weighted edges that encode the actual economic and political dependencies.

The directional intuition — resources flow down, value flows up — is not wrong. It describes a common pattern in how propagation rules are configured for many scenarios. A national government's fiscal policy creates events that propagate downward through the hierarchy to affected sectors and cohorts. Economic stress in sectors generates events that propagate upward to national indicators. But this directionality is an emergent property of the relationship configuration, not a structural property of the graph. The architecture supports any propagation direction along any typed edge.

### The Rollup Gap

There is currently no automatic rollup. Each entity computes its own state from the events it receives. A nation's GDP growth indicator is computed by the MacroeconomicModule from that entity's own attributes and received events — not by summing GDP figures from its child regions.

When subnational resolution (Level 2) is activated in future milestones, explicit aggregation events will need to flow from regions to their parent nation for the national aggregate to reflect regional dynamics. The `parent_id` field is the structural marker a future aggregation module would use. The rollup logic itself must be built — it is not automatic.

---

## Concept 2: The Simulation Engine — Event-Driven, Step-Based, Immutable

### How the Engine Computes

At each timestep, the engine operates on `State[T]` and produces `State[T+1]`. Nothing mutates in place. The propagation engine collects all deltas into a `_DeltaAccumulator` and constructs the new state in a single pass.

The computation sequence at each step:

1. **Control inputs are translated to events.** Exogenous inputs (a scheduled fiscal consolidation, a monetary rate change) are converted to `Event` objects by the input orchestration layer.

2. **Modules run per entity.** Each `SimulationModule` implements `compute(entity, state, timestep) → List[Event]`. It receives the full `SimulationState` (so it can observe other entities), but its outputs are events tagged to a specific `source_entity_id`. The module sees everything but only directly affects its own entity.

3. **Events propagate along the relationship graph.** `PropagationRules` specify which event types travel along which edge types, with what attenuation. A fiscal contraction event hops along trade edges, attenuating by `attenuation_factor × edge.weight` at each hop, up to `max_hops` depth.

4. **Deltas accumulate.** The `_DeltaAccumulator` collects all deltas in one flat pass — no ordering dependency between entities.

5. **State is reconstructed.** `_build_next_state` applies deltas. STOCK indicators receive replacement values (`new_absolute_value = old_value + elasticity_delta`). FLOW, RATIO, and DIMENSIONLESS indicators receive additive deltas. The STOCK/FLOW distinction is critical and has a documented failure mode: emitting the raw elasticity delta instead of the absolute replacement value corrupts all subsequent computations for that indicator.

### The STOCK/FLOW Contract

This contract deserves special attention because its violation produced the most consequential bug of M8 — the EcologicalModule STOCK delta path error.

**STOCK indicators** represent accumulated states — they replace their prior value. `co2_concentration_ppm` is a STOCK: at step 3, it has an absolute value (say, 391 ppm). The module emits a new absolute value, not a delta. If the module incorrectly emits the raw elasticity delta (~0.08) instead of the new absolute value (391.08), the propagation engine replaces 391 ppm with 0.08 ppm — corrupting every subsequent CO2 boundary proximity computation.

**FLOW indicators** represent rates — they add to the running total. GDP growth rate is a FLOW: each module's contribution adds to the accumulating flow for that step.

The contract is simple to state and easy to violate under time pressure. Every simulation module that handles STOCK indicators must have explicit unit tests for the delta path before the module ships. This is an M10 exit gate.

### Why Step-Based Rather Than Continuous

The flight simulator analogy suggests continuous real-time feedback. WorldSim is step-based. This is a deliberate choice, not a technical limitation.

The analytical use cases — backtesting historical scenarios, modelling programme paths, constructing threshold-safe alternative proposals — operate on annual or monthly timesteps. A finance ministry analyst evaluating an IMF programme doesn't need sub-second feedback; they need reliable, well-documented outputs at the step resolution that matches the programme's review cadence.

The adaptive temporal resolution architecture addresses the cases where finer resolution matters: a currency crisis or bank run operates on hourly or daily timescales. The design allows switching to daily resolution within a sub-system when a crisis threshold is detected, while the rest of the simulation continues at monthly resolution. This is not yet implemented, but the architecture accommodates it.

---

## Concept 3: The Iterative Engine and Why Its Replacement Requires Deliberate Care

### What the Iterative Engine Does Well

The current simulation engine is iterative: modules run sequentially, events propagate through the relationship graph hop by hop, and the log trail is narrative. Any output value can be traced back to its contributing events, modules, and propagation paths by reading the log. A developer with no special tooling can answer "why is Greece's unemployment indicator 0.003 higher than expected at step 4" by following the log sequence.

This debuggability is not incidental. It is a property of sequential execution that disappears when you move to matrix computation. The iterative engine is transparent by nature.

The iterative engine also has a hard equity commitment built into it: it runs on a four-core laptop, within the GitHub Actions free-tier runner constraints (2-core, 7GB RAM). Every performance decision has been made against these constraints. Computational efficiency is an accessibility requirement — a tool that only runs on institutional hardware does not serve a Jordanian finance ministry analyst.

### Why the Matrix Engine Is Coming

Two related pressures drive the matrix engine investigation:

**Performance at scale.** The entity template library (Concept 6) introduces specialized domain entities — transport fuel, food systems, electricity — that run alongside nation-level entities. A multi-country Hormuz closure scenario with twelve countries, each with transport fuel, food system, and electricity entities, plus bilateral trade relationship edges between them, is a fundamentally different computational problem than the current Greece single-entity scenario. The iterative engine's performance degrades roughly linearly with entity and edge count. Matrix computation is inherently parallelizable and scales more favorably.

**The NOAA insight.** The Engineering Lead's background working with ensemble meteorological forecast data from NOAA — packed binary formats from supercomputers producing wind forecasts — produced the intuition that matrix arithmetic operations on the simulation's state tensors could provide order-of-magnitude performance improvement. The patterns from ensemble weather computation map to the WorldSim simulation's structure: many entities computed simultaneously, propagation rules as transformation matrices, state updates as matrix operations.

### The Swiss Watch Principle

The transition from iterative to matrix engine must be handled with the discipline of a watchmaker replacing a gear in a Swiss movement — not by feel, not on autopilot.

The simulation engine is the load-bearing substrate of everything WorldSim does. The UX work, the persona work, the ADRs, the stakeholder demos — all of it rests on an engine that produces correct outputs reliably and efficiently. Changing the engine is not a feature addition. It is a structural intervention in the thing everything else depends on.

The Swiss watchmaker doesn't replace a gear by feel. They understand the complete movement first, they test the replacement gear in isolation, they measure the impact on every connected component, and they validate the complete movement against the original specification before declaring the replacement complete.

For WorldSim, this means:

**Phase 1 — Understand the movement:** Comprehensive baseline benchmarks of the current iterative engine on target hardware before any matrix code is written. Not on development machines. On the 4-core laptop and the GitHub Actions free-tier runner. What does one step computation cost at 1 entity? 10? 100? What does propagation cost as relationship edges increase?

**Phase 2 — Test the gear in isolation:** The matrix engine runs in parallel with the iterative engine on identical scenarios, producing identical outputs, before any migration. Output equivalence verified to Decimal precision (the float prohibition applies to both engines). Performance measured on identical hardware.

**Phase 3 — Validate the complete movement:** The full backtesting suite passes identically on both engines. The stress test suite establishes the high-water mark — what does the system do at 100x load? At 1000x? Where are the bottlenecks?

The iterative engine is not retired until Phase 2 equivalence is confirmed. This constraint is non-negotiable.

### The Interpretability Problem

There is a deeper issue with the matrix engine that the performance framing obscures: opacity.

With the iterative engine, debugging is narrative. You follow the story. With the matrix engine, the computation is a transformation: `S(t) × M → S(t+1)`. The output is correct or it isn't, but "why" doesn't have a readable log trail. The answer is somewhere in the tensor operations — but finding it requires tooling that doesn't exist yet.

This is the interpretability problem applied to computation rather than to model outputs. WorldSim already has strong model-output interpretability — confidence tiers, honest-null states, documented blindspots. The matrix engine needs the same discipline applied to the computation substrate itself.

Three capabilities are required before the matrix engine can be considered production-ready:

**Contribution tracing:** Given a specific entity, indicator, step, and output value — decompose the output into its contributing inputs. Which relationship edges contributed what proportion? Which module transformation contributed what delta? This is the matrix equivalent of reading the iterative engine log trace.

**Transformation visualization:** A human-readable representation of the transformation applied at each step — not raw tensor values, but a structured display showing which entities were affected, by how much, through which relationship paths.

**Computation anomaly detection:** Statistical anomaly detection on transformation outputs — values that exceed theoretical bounds, deltas implausibly large relative to prior state, propagation patterns that suggest a relationship graph configuration error. Critically: computation anomaly flags must be in a separate alert channel from MDA threshold alerts. A computation anomaly means something went wrong in the engine. An MDA alert means the simulation found something meaningful. Conflating them destroys the credibility of both.

**The matrix engine is not production-ready until the interpretability tooling is production-ready.** An engine you cannot probe is an engine you cannot trust.

### The Milestone Sequencing

The matrix engine work was initially planned for M10 alongside the stakeholder demo. It was deliberately moved to M11. The reason is a product thinking principle, not a technical one.

A stakeholder demo tells one coherent story. The M10 demo should say: "WorldSim works — here is what it can show you." Introducing a matrix engine investigation into the same demo cycle produces a second story: "Here is what we built, and here is why the thing we built needs to be replaced." That second story undermines the first. Stakeholders cannot absorb a before/after when they haven't yet internalized the before.

M11 is the investigation milestone, with no demo. M12 is the transformation milestone — where the production matrix engine ships alongside the external sector module, and the Hormuz closure scenario for Jordan demonstrates the democratization mission made concrete.

---

## Concept 4: The Causal Meta-Map

### The Bangladesh Case

The clearest illustration of the causal meta-map gap is the Bangladesh fuel shortage cascade.

A fuel shortage in Bangladesh does not remain a fuel shortage. It cascades: fuel → electricity generation → telecommunications towers → mobile financial services → remittance flows. Each step in the cascade is a cross-sector dependency — fuel and electricity are different sectors, electricity and telecommunications are different sectors, telecommunications and financial services are different sectors.

WorldSim's current architecture can model each of these sectors individually. It can model the fuel shock. It can model the electricity generation impact. But it cannot automatically model the cascade — because the cascade requires knowing that telecommunications towers depend on diesel generators, which depend on fuel supply, and that mobile financial services depend on telecommunications infrastructure.

This is the causal meta-map gap: the simulation lacks an explicit representation of cross-sector dependencies that would allow cascade dynamics to propagate automatically through the relationship graph.

### What the Causal Meta-Map Is

The causal meta-map is a structured registry of cross-sector dependencies — a document (and eventually a data structure) that says: "The telecommunications sector depends on the electricity sector for X% of its operational capacity. The financial services sector depends on the telecommunications sector for Y% of its transaction processing. These dependencies have the following transmission characteristics at the following timescales."

Without this map, each cascade must be manually encoded as explicit relationship edges and propagation rules for each scenario. With the map, the simulation engine can automatically derive the relevant edges and propagation rules for any scenario involving the mapped sectors.

ARCH-REVIEW-005 (the causal meta-map review) is the formal architectural process for designing this component. It was gated on the Domain Intelligence Council blind interview — the council members needed to be consulted before the architecture was committed to, because the dependency structure between sectors is a domain knowledge question, not an engineering question.

### The Relationship to the Entity Template Library

The causal meta-map and the entity template library are deeply connected. Entity templates specify not just a domain entity's internal structure but its typed relationship edges to other entity types. The transport fuel template knows it has a fiscal relationship edge to the nation entity, a consumption relationship edge to demographic cohort entities, and a supply chain relationship edge to the electricity template (when present).

The causal meta-map is the knowledge base from which those relationship edge specifications are derived. The entity template library is the operational implementation of the causal meta-map — making the dependency structure computable rather than merely documented.

---

## Concept 5: The Multi-Currency Measurement Framework

### Why No Master Conversion Rate

The most consequential architectural decision in WorldSim's design is stated simply: **there is no master conversion rate between the measurement frameworks.**

Economic analysis almost always ends in a single unit. Everything gets translated into money. When you translate child malnutrition into a GDP impact, you are making a claim about what child malnutrition is worth in monetary terms. That claim involves assumptions about future earnings capacity, discount rates, and whose valuation of childhood health outcomes is used as the denominator. Those assumptions are never neutral. In the context of a sovereign debt negotiation, they are almost always made by the people with the most analytical power and the greatest incentive to value human outcomes at the rate that supports their preferred programme design.

WorldSim produces outputs simultaneously in four accounting units: financial metrics, human development units (the Sen capability approach and HDI dimensions), ecological units (planetary boundary proximity and natural capital depletion), and governance units (institutional quality, political freedom, rule of law).

The radar chart visualizes this: a four-dimensional deformation of a shape where any dimension can deteriorate independently of the others. A country's financial indicators can be improving while its human development indicators continue to deteriorate. This is not a contradiction to be resolved by applying a weighting scheme. It is the central analytical finding — the finding the finance ministry negotiator most needs and is least likely to be shown by the counterparty's models.

The Greece 2010–2015 scenario makes this concrete: at step 5 (2014), GDP growth turned marginally positive for the first time since the programme began. By the IMF's primary headline metric, the programme was working. By the human development metric — unemployment at 26.5%, child poverty elevated, life expectancy declining — the recovery had not begun. "Financial recovery is not the same as recovery" is not a slogan. It is a finding made visible by simultaneous multi-framework display.

### User-Defined Weighting and MDA Alerts

User-defined weighting is supported — a user can assign different weights to different frameworks for their analytical context. But MDA threshold alerts fire regardless of user weighting when any dimension crosses below a critical floor.

This is the key governance principle: no aggregate score can hide a catastrophic failure in a single dimension. A weighted average that masks a threshold crossing is not an analytical tool — it is a mechanism for producing comfortable falsehoods. The MDA system exists to prevent this.

### The Honest-Null Principle

When a measurement framework is not yet certified for production use, the correct display is not zero and not suppression. Zero implies governance failure. Suppression implies governance is not being tracked. The honest-null is a visually distinct state — the governance axis at M8 renders as a dashed hollow dot labeled "Governance — in validation" — that communicates: we are tracking this, it is not yet ready, and here is why.

The `RadarAxisDatum.composite_score: number | null` type contract enforces this: `computeFinalScore(null) → null`, and Recharts skips the polygon vertex entirely rather than interpolating to zero. The visual gap in the radar chart polygon is itself information — it says "this dimension is absent, not zero."

---

## Concept 6: The Entity Template Library and the Resolution Spectrum

### The Coarse-to-Fine Insight

WorldSim currently operates at the coarse end of a resolution spectrum. Nation-level entities, aggregate indicators, annual or monthly timesteps. This is the right starting point — the analytical value at this resolution is real, the equity requirement is met, and the backtesting fixtures validate correctly.

But the resolution is not fixed. It is a dial.

The entity template library is the mechanism for moving up the resolution spectrum selectively — not everywhere simultaneously, but where the analytical question demands it. A Kenya fuel scenario that needs to capture the kerosene → household cooking fuel → food expenditure → child malnutrition transmission chain needs higher resolution in the household consumption entity. The nation-level financial indicators can stay coarse.

### What an Entity Template Is

A domain-specific simulation entity template is a pre-configured entity type with:
- A structural model (what the entity represents, its internal computation, its typed relationship edges to other entity types)
- Calibrated parameters derived from cross-country empirical data
- Known transmission pathways (how shocks propagate through this entity to adjacent systems)
- Documented limitations (where the structural assumptions break by country context)
- Confidence tier assignments per parameter (per the synthetic data framework)

The structural properties of a template are largely invariant across countries — the physics of fuel consumption, the economics of storage, the transmission mechanism from pump price to food price. The parameters vary by country context. A transport fuel template instantiated for Jordan has different modal split parameters than the same template instantiated for Kenya — but the same structural model, the same relationship edge types, the same transmission pathways.

### The Decomposition Criterion

A template decomposition — splitting a coarse aggregate entity into finer-grained sub-entities — is justified when the variability spread justifies the further decomposition. If disaggregating transport fuel into petrol, diesel, and kerosene produces meaningfully different policy conclusions than treating them as a single aggregate, the decomposition is justified. If the three sub-entities produce essentially the same finding as the aggregate, the decomposition costs compute without adding analytical value.

The Chief Methodologist owns this criterion. It is a statistical question about whether disaggregation reduces or preserves uncertainty in the finding that matters for the canonical user's decision. A decomposition that improves the simulation's theoretical completeness but does not change the policy finding is not worth the computational cost.

### The Founding Template Candidates

Three domain entities cover the most common cascade pathways in the sovereign governance failure cases and appear simultaneously in the most important global south use cases:

**Transport fuel** — pump price → transport cost → food price → household purchasing power → public legitimacy. Relationship edges: fiscal (fuel tax revenue to nation entity), consumption (household fuel expenditure to demographic cohort entities), supply chain (import dependency to external sector). The Kenya fuel case is the clearest illustration of why this template matters.

**Food systems** — staple food availability, price, and import dependency. The natural companion to transport fuel, given the transport cost → food price transmission. The Sudan and Yemen cases are the clearest illustrations.

**Electricity** — generation, distribution, and household access. Similar structure to transport fuel — import dependency, pricing regulation, household consumption elasticity. The Bangladesh cascade case is the clearest illustration.

These three templates cover the cascade from fuel shortage to household capability loss that appears in virtually every global south sovereign stress scenario.

### Library Governance

A new entity template requires before inclusion: structural documentation, calibration evidence with confidence tier assignments, cross-country validation across a minimum of three country instances, known limitations documentation, and Chief Methodologist review and sign-off.

The template library is a curated, calibrated, validated collection — not an open contribution model. An uncalibrated template produces worse outcomes than a well-calibrated nation-level aggregate. The quality improvement from templates is conditional on calibration quality.

---

## Concept 7: The Two-Path Infrastructure Model

### The Equity Constraint and Its Limits

The equity requirement — WorldSim runs on a four-core laptop — applies permanently to the core analytical use case: a finance ministry analyst running a nation-level scenario at current entity resolution. This is non-negotiable. A tool that requires institutional hardware to run does not serve the Jordanian finance ministry analyst. It recreates the asymmetry it was designed to correct.

But the entity template library creates a genuinely different use case. A twelve-country Hormuz closure scenario with transport fuel, food system, and electricity templates, bilateral trade relationship edges, and commodity price propagation across all entities — this is not a finance ministry analyst use case. It is a regional development bank use case, or a multilateral research team use case. Those institutions have infrastructure access and the budget to pay for on-demand cloud compute when the analytical question justifies it.

### The Two Paths

**Local compute path:** The current engine, on target hardware, serving the core equity use case. Always available. Always free at the point of use. Nation-level entities at current resolution. The scenarios that matter most for the democratization mission.

**Cloud compute path:** On-demand scaling for high-resolution template scenarios. Not free, but priced at cost or subsidized for qualifying institutions (global south finance ministries accessing high-resolution scenarios should not be disadvantaged relative to institutional actors). The analytical capability exists; access is gated by willingness and ability to pay for compute, not by the tool's architecture.

The matrix computation engine is the enabling technology for the cloud scaling path. The matrix formulation is inherently more parallelizable than the iterative engine — horizontal cloud scaling becomes viable at template library depth in a way that the iterative engine's sequential execution cannot support.

Critically: **both paths run the same computation model.** The infrastructure path is an operational choice, not an architectural one. A scenario that runs locally at nation-level resolution and a scenario that runs on cloud compute with entity templates are running the same engine on the same data model. The kitchen is the same; the compute resources change.

### Continuous Improvement Without Forced Migration

The two-path model enables a continuous improvement arc that doesn't require users to upgrade. New entity templates ship when calibrated and validated — they become available to both paths simultaneously. New countries are added to the source registry as data becomes available. New backtesting fixtures are contributed by the community of practice.

A finance ministry analyst using the local compute path with nation-level entities benefits from every new template that gets added — not because they run it themselves, but because the template calibration process generates cross-country parameter data that improves the synthetic data baselines for their own nation-level scenarios.

The flywheel operates at the template library level as well as at the user level.

---

## Concept 8: The UX Architecture — From Case B to Governing Premises

### What Case B Means

After seven milestones, the UX Design Thinking Agent identified a structural problem in the instrument cluster architecture: the tool had been built with the choropleth map as the primary viewport and the instruments (radar chart, MDA alerts, PMM widget) in a side drawer. This is an inversion of the correct relationship.

A choropleth map is geographic context. It tells you which entities are selected and how they compare spatially. It is orientation information.

A trajectory view, an MDA alert panel, and a PMM widget are instruments. They tell you what the simulation is producing and whether it is within safe operating parameters. They are what the canonical user needs to make a decision.

The aviation analogy makes the failure mode legible: instruments belong in the primary viewport, always visible. Context belongs in a navigable secondary surface, accessible but not primary. A cockpit that puts the altimeter in a side drawer and shows a map in the primary viewport is not a cockpit — it is a map application with a drawer for instruments.

Case B is the verdict that the architecture requires a rethink, not an optimization. Case A would have been "the current architecture is approximately correct and needs tuning." Case B means the primary and secondary surfaces are inverted and must be corrected before M9 implementation begins.

### The Three-Mode Architecture

The most important insight from the UX design thinking work is that WorldSim serves three distinct interaction modes with three distinct primary cognitive tasks:

**Mode 1 — Replay:** The user reviews a completed historical scenario, step by step. Two valid primary cognitive tasks:
- Trajectory reconstruction ("what actually happened across all four frameworks?") — serves Lucas Ferreira and Amara Diallo
- Historical pattern recognition ("does this match a pattern I recognize?") — serves Andreas Stefanidis and Aicha Mbaye

**Mode 2 — Simulation:** The user constructs forward projections and compares alternative paths. Primary cognitive task: threshold-safe path construction ("which programme path achieves the fiscal target without crossing any human cost MDA threshold?")

**Mode 3 — Active Control:** The user applies policy inputs in real time and watches the trajectory respond. Primary cognitive task: real-time steering within human cost constraints ("given the current trajectory, what control input at this step keeps us above the floor while moving toward the objective?")

No single primary cognitive task formulation is correct for all three modes. The M4-era "threshold alarm detection" formulation is approximately right for Mode 3 and wrong for Modes 1 and 2. The per-mode formulation serves all five personas across all three modes.

### The Six Governing Premises

The revised six governing premises that govern all M9 UX decisions:

**Premise 1:** The primary viewport is the instrument cluster. Geographic context is always accessible but never primary.

**Premise 2:** Instruments are always visible without deliberate navigation. Confidence tier is a primary instrument attribute — displayed on the instrument face. Tier 4 does not visually resemble Tier 1.

**Premise 3:** The step axis is the shared frame for all instruments. In Mode 1, calendar date and event label are mandatory on every step marker. A fixture missing `step_event_label` on SIGNIFICANT steps is an incomplete fixture — not a styling gap, a data completeness failure. This premise was the most consequential extension: without calendar annotations, the step axis is legible to Lucas and Eleni (who know what happened at step 3) and opaque to Andreas and Aicha (who don't).

**Premise 4:** Each mode has its own primary cognitive task. Within Mode 1, trajectory reconstruction and historical pattern recognition are both valid primary cognitive tasks and must both be served.

**Premise 5:** The control plane layout zone must be reserved before the control plane is built. The minimum reserved zone content: policy input form, exogenous shock injection form, applied inputs/shocks history list — sized to accommodate all three simultaneously.

**Premise 6 (new):** Methodology documentation is accessible within one interaction of any instrument output. Confidence tier badges are interactive — tapping opens the methodology note. This closes Amara Diallo's Evaluative entry state gap: the Academic Researcher evaluating WorldSim's methodology credibility needs to be able to inspect the methodology from the instrument face, not navigate to a separate documentation section.

---

## Concept 9: The Synthetic Data Framework

### Why Data Poverty Cannot Be a Blocker

WorldSim's value proposition is highest precisely where institutional analytical capacity is lowest — global south finance ministries with thin data infrastructure. But those are also precisely the contexts where the data required to run a meaningful simulation analysis is thinnest.

If WorldSim requires Eurostat-quality data to function, it serves European finance ministries — which already have institutional analytical capacity — and fails the actors it was built for. The democratization mission requires that data poverty not be a blocker.

### The Five-Method Hierarchy

When real data is unavailable or of insufficient quality, WorldSim generates synthetic data using a hierarchy of inference methods:

1. **Bayesian hierarchical models** (Tier 3) — when ten or more comparable countries have sufficient data for a cross-country hierarchical model, with holdout validation. The most statistically sound synthetic method.

2. **MICE imputation** (Tier 3–4) — multiple imputation by chained equations, for bounded short gaps where adjacent-period data exists.

3. **Bootstrap resampling** (Tier 4) — when comparable country data exists but is insufficient for a full Bayesian model. Resamples from the distribution of comparable cases.

4. **Structural extrapolation** (Tier 4) — model-based extrapolation using known structural relationships. Last resort before declaring structural absence.

5. **Structural Absence Declaration** — when data absence is itself a signal (a country has expelled the measuring organization, stopped reporting, or systematically falsified data), generating a synthetic estimate masks the signal. The honest response is a declaration that specifies exactly what data would unblock the estimate.

### The Meaninglessness Threshold

Three conditions, any one of which is sufficient to refuse synthetic estimation:

- The synthetic confidence band width exceeds 4× the point estimate (the band is too wide to be directionally useful)
- The confidence interval straddles an MDA floor (the simulation cannot determine whether the threshold has been crossed)
- Fewer than three comparable countries exist for the inference (the statistical basis is too thin)

When any condition is met, the output is a structured "cannot produce a meaningful estimate" declaration — not a blank, not a wide band, but a specific statement of what data would unblock the estimate.

### MDA Alert Behavior Under Synthetic Data

When an MDA threshold alert would fire based on a synthetic data point, the alert behavior is tiered:

- **Tier 3 synthetic (Bayesian/MICE):** Advisory MDA alert — fires in a secondary alert channel, not the primary instrument cluster
- **Tier 4 synthetic:** Exploratory alert only — does not fire in any production alert channel
- **CI straddles MDA floor (any tier):** "Cannot determine MDA status" — a blue indicator in the primary cluster, because degraded terrain awareness is itself critical information. The user needs to know the instruments are compromised, not that everything is fine.

The last case is the most important: when the simulation cannot determine whether a threshold has been crossed, displaying nothing is worse than displaying the uncertainty. The blue "cannot determine" indicator is the honest-null principle applied to MDA alerts.

### The Anomaly Detection Constraint

Synthetic baseline data can theoretically be used to flag when a country's published official data diverges implausibly from regional comparables — a form of data quality audit. This capability is deliberately constrained:

- Requires Technical Steering Committee sign-off before production deployment
- Opt-in for the user — never automatically enabled
- Permanently excluded from Mode 3 (active control) sessions
- Governance indicators permanently excluded regardless of mode

The constraint on Mode 3 is the critical one: in an active negotiation, a false positive on the ministry's own published data can undermine the primary beneficiary's confidence in their own numbers. A tool built to serve finance ministries cannot undermine them. The asymmetry we are correcting runs one direction. So does the tool.

---

## Concept 10: The Architecture Backlog — Preventing the ADR Numbering Problem

### How the Problem Arose

ADR numbers were being assigned informally — an issue title would say "ADR-007" before any ADR document existed. When the M9 HORIZON sweep revealed that both the synthetic data framework (referenced in CLAUDE.md) and the simulation engine computation model (Issue #217) had claimed ADR-007, the conflict required explicit resolution and renumbering.

The conflict arose because ADR numbers are permanent institutional artifacts — every document that references ADR-007 must be updated when the number changes. An informal numbering system produces this problem inevitably as the project scales.

### The Architecture Backlog

`docs/architecture/backlog.md` is the single source of ADR number assignment. The process:

1. When an architectural question requiring an ADR is identified, file a GitHub issue — no ADR number in the title
2. Add the issue to the backlog with status `PENDING_NUMBER`
3. At the next PM Agent HORIZON sweep, the backlog is reviewed for priority against all pending ADRs — this is the explicit recency bias counter
4. When an ADR is ready to be drafted, the Architect Agent claims the next available number from the backlog, marks it `ASSIGNED`, and begins drafting
5. Only then does the ADR number appear in the issue title and document

The recency bias counter is the most important process element. Without it, a new architectural question raised in the current session naturally gets priority over an older question sitting in the backlog. The HORIZON sweep forces a comparison across the full backlog before any new ADR is activated.

### The Current ADR Registry

| ADR | Title | Status | Milestone |
|---|---|---|---|
| ADR-007 | Synthetic data framework | Consultation complete (PR #373); formal ADR pending | M9 |
| ADR-008 | UX architecture — instrument cluster, viewport, interaction model | Pending governed process (Issue #397) | M9 |
| ADR-009 | Simulation engine computation model — iterative vs. matrix | Pending M11 baseline benchmarks | M11 |
| ADR-010 | Trajectory view as primary instrument | Pending (Issue #366) | M9 |

ADR-009 has a hard constraint: it must not be authored until the Phase 1 baseline benchmarks from the Chief Engineer's performance investigation are complete. Writing ADR-009 before the empirical evidence exists produces a guess with a document number, not an architectural decision.

---

## Concept 11: The GIS and Geocoded Data Layer

### Why Raw Geospatial Data Does Not Enter WorldSim

Issue #4 establishes a principle that sounds technical but has profound implications for the tool's scope and maintainability: **WorldSim consumes pre-processed GIS-derived indicators, not raw geospatial datasets.**

The distinction matters because geospatial data processing is a discipline in itself. Flood risk modeling, terrain-dependent infrastructure vulnerability assessment, high-resolution population distribution analysis, mobile network activity as an economic proxy — these require specialized tools (QGIS, Google Earth Engine, the Python geospatial stack: GeoPandas, Rasterio, GDAL) and specialized expertise. WorldSim is not a GIS tool. It is a simulation platform that can consume GIS outputs.

The pattern is the same as the climate module: WorldSim consumes pre-computed ERA5 time series rather than doing climate science internally. The climate scientists use their tools; WorldSim uses their outputs. The GIS layer follows the same contract.

### What Enters WorldSim's Database

What enters the source registry and the simulation database is structured: a country- or subnational-level indicator value, with a unit, a date, a confidence tier, and a source registry ID. Raw rasters and vector datasets do not enter WorldSim's database.

This is the platform principle applied to data processing: the kitchen doesn't do the farming. Specialized external tools — whether QGIS for flood risk or the World Bank API for economic data — are the ingredient preparation layer. WorldSim is the cooking layer.

### The Dual-Use Flag on Mobile Network Data

Mobile network data (CDR aggregates, mobility indices) deserves special attention. The same data that estimates informal economic activity — tracking movement patterns as a proxy for economic behavior in countries with thin formal economic statistics — can also identify population movement patterns in ways that carry surveillance risk.

Issue #4 explicitly requires Security and Review Agent review before any mobile network data source is integrated. This is the defense-not-offense principle applied at the data ingestion layer, not just at the analytical output layer. A data source that could serve a finance ministry analyst but simultaneously enable population surveillance fails the dual-use test regardless of how useful its economic proxy value might be.

The privacy governance requirement extends this: high-resolution population data requires documented aggregation methodology and minimum cell size even at aggregate level. The protection applies before the data enters WorldSim, not after.

### Why This Matters for the Democratization Mission

A global south finance ministry analyst should not need a GIS specialist on staff to use WorldSim. The pre-processing layer is where GIS expertise is applied — by domain experts who publish their outputs as structured indicators that WorldSim can consume. The analyst uses the outputs, not the processing pipeline.

This also means that improving WorldSim's geospatial capabilities does not require touching the simulation engine. A better flood risk model, a higher-resolution population distribution, a more accurate cellular signal proxy for economic activity — these improvements happen in the pre-processing layer and enter WorldSim through the standard data ingestion pipeline. The kitchen stays the same; the ingredients improve.

### The Candidate Datasets

The motivating dataset candidates from Issue #4 include: flood modeling and terrain-dependent infrastructure vulnerability (relevant for Bangladesh, Pakistan, coastal Caribbean), high-resolution population density (improving demographic cohort spatial precision), and mobile network activity as an economic proxy (particularly valuable in data-poor contexts where formal economic statistics are thin but mobile penetration is high). Each would enter as a structured indicator with a confidence tier reflecting the quality of the geospatial pre-processing.

---

## Concept 12: The Data Marketplace

### Two Distinct Components

Issue #5 establishes the data marketplace concept as two architecturally and governance-distinct components that must be designed and implemented separately.

**Component 1 — Curated External Dataset Registry**

A maintained catalogue of validated external datasets, each with a full `SourceRegistration` record, a quality tier assignment with written rationale, documented known limitations, vintage dating assessment (can this source be used for backtesting?), an ingestion pipeline implementation or specification, and a review cadence (some datasets publish annually, others continuously).

The curated registry is maintained by the WorldSim team. A dataset enters the curated registry by going through the full standards compliance check. This is the high-trust layer — every dataset in the curated registry has been validated against WorldSim's data standards and can be used in production simulations with confidence.

**Component 2 — User-Contributed Dataset Pipeline**

A pathway for community members — researchers, finance ministry analysts, civil society organizations — to contribute datasets that are not yet in the curated registry. User-contributed datasets enter at a lower confidence tier and go through a defined validation and promotion process before they can be used in production simulations.

The promotion criteria are the key governance element: what does a user-contributed dataset need to demonstrate before it earns a higher confidence tier? Source verifiability, methodology documentation, cross-validation against existing sources, community review — these are the criteria that prevent the user-contributed layer from becoming a vector for low-quality or deliberately misleading data.

### Why This Is the Flywheel Made Concrete

The founding document describes the flywheel: the tool makes users better, better users make the tool better. The data marketplace is the mechanism by which users make the tool better in the data dimension.

A Kenyan finance ministry analyst who has proprietary data about Kenya's transport fuel pricing structure — data that isn't in any public registry — can contribute it to the user-contributed pipeline. If it passes the promotion criteria, it improves every future Kenya scenario that uses transport fuel indicators. The analyst's local knowledge becomes a public good for the community of WorldSim users.

### The Governance Tension

The data marketplace introduces a governance tension that doesn't exist in the curated registry: who validates user-contributed data, and what happens when a user-contributed dataset is later found to be inaccurate or deliberately falsified?

The defense-not-offense principle applies here: the marketplace is designed to serve finance ministry analysts who need better data, not to provide a channel for actors who want to introduce biased data into the simulation. The validation and promotion process is the safeguard. The TSC (Technical Steering Committee, M13 scope) is the likely governance body for the promotion criteria.

### The Relationship to the Synthetic Data Framework

The data marketplace and the synthetic data framework are complementary, not competing. The synthetic data framework generates estimates when no real data exists. The data marketplace provides a pathway for real data — contributed by community members — to displace synthetic estimates. A user-contributed dataset that passes the promotion criteria and earns a Tier 2 confidence assignment directly improves the simulation's accuracy for that indicator in that country context, replacing the Tier 3 or Tier 4 synthetic estimate that would otherwise be used.

---

## Concept 13: The HealthBurdenModule and Lagged Health Consequences

### The Signal That Standard Indicators Miss

Issue #214 identifies a systematic gap in the Human Cost Ledger: the current HUMAN_DEVELOPMENT framework tracks poverty headcount and consumption quintile deltas, but these do not surface the lagged, compounding health consequences of austerity that appear 12–36 months after a fiscal shock.

The Greece tuberculosis case is the canonical motivating example. TB incidence increased 17% during the first IMF programme period (ECDC, 2013). The driver was a combination of factors: health budget cuts reduced primary care access, increased homelessness created conditions for TB transmission, and the combination of stress and malnutrition compromised immune function. This signal is invisible to the current Human Cost Ledger output — poverty headcount and consumption quintiles do not capture disease burden.

This is a specific instance of the CB Cloud failure mode: decision-makers see fiscal consolidation from the trailing edge (budget targets met, debt sustainability improving) while the affected population experiences it from the leading edge (deteriorating health system capacity, rising disease burden). WorldSim's multi-framework measurement philosophy requires making the leading-edge signal visible. The HealthBurdenModule is the instrument for that signal.

### The DALY Framework

Disability-Adjusted Life Years (DALYs) are the international standard for measuring disease burden — combining years of life lost to premature death and years of life lived with disability or illness into a single comparable metric. The DALY framework is used by the WHO, IHME (Global Burden of Disease), and major health economics research institutions.

For WorldSim, DALY-based indicators would capture:
- The increase in disease burden from communicable diseases (TB, hepatitis, HIV) that rise with poverty, homelessness, and reduced healthcare access
- The increase in burden from non-communicable diseases (mental health, cardiovascular) that rise with economic stress and reduced healthcare utilization
- The health system capacity deterioration (staff emigration, facility closures, supply chain failures) that compounds the above
- The lagged mortality signal — excess deaths that appear 12–36 months after the fiscal shock, too late to be visible in the programme's review window

### Why the Lag Matters for Negotiation

The 12–36 month lag is the most important property of health burden indicators for the negotiation use case. An IMF programme typically has a 3–5 year programme window with annual review cycles. Health consequences that appear 18 months after programme signing are visible within the programme window — but they appear after the conditionality terms have been signed and the programme is underway.

The HealthBurdenModule, by modeling the lag explicitly, can project when health burden will appear and how severe it will be — before the programme is signed. This is exactly the kind of forward-looking finding that WorldSim is designed to surface in the negotiating room. "This programme path produces a projected 15% increase in TB incidence at month 18" is a citable finding that changes the conversation about health system protection carve-outs in the conditionality package.

### The Relationship to the Multi-Framework Measurement

The HealthBurdenModule extends the HUMAN_DEVELOPMENT framework axis of the radar chart, not the FINANCIAL axis. DALY-based indicators are human development indicators — they belong to the Sen capability framework alongside educational attainment, economic agency, and political participation.

The module is currently deferred to M9 scope (Option A — extend the HUMAN_DEVELOPMENT framework with four new attributes) or M13 (full standalone module). The deferral reflects the epistemic sequencing principle: the module's calibration requires validated data from the backtesting cases, and the backtesting framework needs to be robust before new indicators are added to it. A poorly calibrated HealthBurdenModule would be worse than no module — it would produce false confidence in a domain where the stakes are highest.

---

## Concept 14: The Distributed Simulation Ecosystem

### Beyond the Single Kitchen

The platform principle establishes that WorldSim is one kitchen with interchangeable ingredients. The distributed simulation ecosystem concept extends this further: **the kitchen doesn't have to be owned by one organization, and the ingredients don't have to be produced by one team.**

Consider what the entity template library (Concept 6) implies at scale. A transport fuel template calibrated for East African landlocked country contexts requires deep knowledge of East African fuel logistics — import routes from Mombasa, pipeline vs. road transport dependencies, kerosene vs. diesel consumption splits in rural vs. urban households. The WorldSim team in Canada does not have this knowledge. A transport economics research group at the University of Nairobi does.

The distributed simulation ecosystem concept is: **domain experts from around the world maintain the specialized simulation entities in their domain, and WorldSim's core engine consumes their outputs as ingredients.**

### The Analogy to Package Ecosystems

The closest analogy is a software package ecosystem — npm for JavaScript, PyPI for Python, CRAN for R. A core runtime exists (Node.js, Python, R). Community members publish packages that extend the runtime's capabilities. Users install the packages they need. The runtime doesn't know or care who wrote the packages — it only knows that they conform to the package specification.

For WorldSim, the "packages" are not code libraries but calibrated simulation entities: structured models with documented methodologies, calibrated parameters, confidence tier assignments, validation records, and typed relationship edge specifications. The WorldSim engine doesn't know or care who built the transport fuel template — it only knows that the template conforms to the entity specification and has passed the certification requirements.

### The Networked Expertise Model

The distributed ecosystem enables something the single-team model cannot: genuine global coverage with genuine local expertise.

- A transport economics research group at the University of Nairobi maintains the transport fuel template for East African country contexts
- An agricultural economics institute in São Paulo maintains the food systems template for South American country contexts calibrated against FAOSTAT data and validated against the 2010–2011 food price crisis cascade
- A health systems research group at a South Asian institution maintains the HealthBurdenModule template calibrated against WHO and IHME data
- A climate economics group maintains the ecological stress templates calibrated against IPCC scenarios

Each group has the domain expertise and local data access that the WorldSim core team lacks. WorldSim provides the framework — the engine, the measurement system, the instrument cluster, the certification process. The ecosystem provides the domain depth.

### The Certification Question

A distributed ecosystem requires a certification process that the single-team model does not. When the WorldSim team builds a template, the Chief Methodologist reviews and certifies it. When a community member builds a template, who certifies it?

The certification process for community-contributed templates must answer:
- What methodological standards must the template meet?
- What cross-country validation is required before a template enters the production registry?
- What happens when a certified template is later found to be miscalibrated?
- Who is accountable when a finance ministry analyst makes a decision based on a miscalibrated community template?

The TSC (Technical Steering Committee, M13 scope) is the likely certification body — an independent governance actor with domain expertise drawn from the community of users and contributors. The Chief Methodologist's certification framework for first-party templates is the starting point; the TSC extends and adapts it for community contributions.

### The Equity Dimension

The distributed ecosystem must not reproduce the asymmetry it is designed to counter. If the ecosystem's certification process is so demanding that only well-resourced research institutions can meet it, then community-contributed templates will predominantly come from institutions in well-resourced countries — and the templates will be calibrated for those contexts.

The certification process must be accessible to a research group at a Kenyan university with modest resources. Accessibility of contribution is as important as accessibility of use. This is the equitable build process principle extended to the ecosystem layer.

---

## Concept 15: Uncertainty Quantification — Distributions Not Point Estimates

### The Current State and Why It's Insufficient

Issue #22, identified by the Chief Methodologist in ARCH-REVIEW-001, names a foundational gap: `SimulationEntity.attributes` currently stores bare values and the propagation engine computes deterministic deltas. Every simulation output is a single number with no uncertainty band attached.

This violates the "no false precision" principle at the architectural level. The principle says WorldSim is a structured reasoning tool, not a prediction engine. But an engine that produces point estimates without uncertainty bands is, by construction, presenting its outputs with more confidence than the underlying model warrants. A GDP contraction of -3.2% looks precise. What the simulation actually knows is that the contraction is somewhere between -1.8% and -5.1% given the uncertainty in the input parameters and model relationships. Displaying only -3.2% is a form of dishonesty built into the data model.

### What Uncertainty Quantification Requires

The `Quantity` type system — which already carries `value: Decimal`, `unit`, and `variable_type` — needs to be extended to carry uncertainty representation. The two candidate approaches:

**Confidence intervals:** A lower bound and upper bound representing the X% confidence interval around the central estimate. Simpler to implement, interpretable by non-statisticians, directly displayable as a band on the trajectory view.

**Full distributions:** A probability distribution over possible values (Gaussian, skewed, fat-tailed as appropriate to the indicator). More statistically honest — many macroeconomic outcomes have fat tails that a symmetric confidence interval misrepresents — but harder to display and harder to propagate through the simulation graph.

The propagation challenge is significant: when input parameters have uncertainty bands, those bands must propagate through every module computation and every relationship edge hop, accumulating appropriately. This is computationally non-trivial and is exactly the kind of problem where the matrix computation engine (ADR-009) provides architectural advantages — uncertainty propagation through a matrix transformation is more tractable than uncertainty propagation through sequential module execution.

### Why This Matters for the Negotiation Use Case

A finance ministry negotiator who sees "GDP contraction: -3.2%" has less information than one who sees "GDP contraction: -3.2% (80% CI: -1.8% to -5.1%)." The second presentation honestly represents the model's uncertainty. It also changes the negotiation: the difference between a central estimate of -3.2% and an upper bound of -5.1% may be the difference between a programme that is fiscally survivable and one that produces a debt spiral. Hiding that uncertainty behind a point estimate is the analytical equivalent of the IMF's fiscal multiplier assumption of 0.5 — a false precision that produces overconfident policy choices.

Issue #22 has a hard dependency: M9 must deliver the confidence tier standards (#43) before M10 can implement uncertainty quantification. The confidence tier system establishes which inputs have what level of data quality — that information is the input to the uncertainty band calculation. You cannot quantify output uncertainty without first knowing input uncertainty.

---

## Concept 16: Information Access Architecture — Role-Based Output Visibility

### The Dual-Use Tension Made Operational

Issue #53 surfaces the most operationally difficult consequence of the defense-not-offense principle: WorldSim produces analytical outputs that could be used either to defend a vulnerable country's negotiating position or to identify that country's weaknesses for exploitation. The dual-use problem isn't just theoretical — it becomes concrete the moment the tool is deployed with multiple users.

A finance ministry analyst running a scenario to prepare for IMF negotiations needs to see that scenario's full outputs. An IMF counterpart running the same scenario to prepare their own position does not need to see the ministry's internal scenario configurations. The analytical capability is the same; the access should differ by role and institutional context.

### Two Approaches — Current and Long-Term

**Option A — Scenario tag boundary (current approach):** Scenarios are tagged as public, institutional, or confidential. Output visibility is determined by the tag. This is simple, requires no authentication infrastructure, and is appropriate for the current single-institution deployment model. The limitation: it is manually enforced and provides no cryptographic guarantee.

**Option B — Role-based access control with institutional verification (long-term requirement):** A full RBAC system where output visibility is determined by the authenticated user's role and institutional affiliation. A verified finance ministry analyst sees their own ministry's scenarios and any public scenarios. A verified civil society researcher sees public scenarios and any scenarios they've been explicitly granted access to. An unverified user sees only public scenarios.

The institutional credential verification problem is hard: how do you verify that someone claiming to be a Zambian finance ministry analyst actually is one, without creating a bureaucratic barrier that excludes the very users the tool is designed to serve? This is not a solved problem. The long-term answer likely involves institutional trust relationships (the ministry's IT system verifies its own staff) rather than central WorldSim credential management.

### Why This Is an Architectural Commitment, Not a Feature

Option B requires architectural decisions that must be made before the public deployment infrastructure is built. An access control model retrofitted onto a system built without it produces exactly the kinds of vulnerabilities that undermine the defense-not-offense principle. The ADR for information access architecture must be written before M13 (public launch) — because public launch means the system is accessible to all users, including those who might use it for exploitation.

The scenario tag boundary (Option A) is the correct current approach precisely because it is simple, auditable, and honest about its limitations. The long-term RBAC system (Option B) is the correct eventual approach for a multi-institution deployment. The transition between them requires deliberate architectural planning, not an emergency retrofit.

---

## Concept 17: Mandatory Data Admission Testing

### The Gap Between Certification and Use

Issue #253 identifies a gap in the data pipeline that sits between two existing safeguards. Data currently enters WorldSim after source-level approval (the `source_registry`) and field-level certification (the data quality tier system). Both are documentation-level safeguards — they establish that a data source is approved and that a field is certified. Neither is an automated testing gate.

The gap: a data source can be approved and certified but still produce values that are structurally wrong when actually loaded — truncated time series, wrong units despite correct labeling, values out of the expected range for the indicator, misaligned vintage dates. These failures are not caught by source approval or field certification. They are caught — if at all — when the simulation produces implausible outputs and a developer investigates.

### What Data Admission Testing Requires

A systematic testing gate between data ingestion and simulation use. Every dataset that enters the simulation pipeline must pass a defined set of admission tests before it can be used in a production simulation:

- **Range tests:** Is the value within the theoretically possible range for this indicator? (Unemployment cannot be negative. CO2 concentration cannot be zero. GDP growth rate cannot be -100%.)
- **Temporal consistency tests:** Does the time series have gaps? Are there implausible discontinuities between adjacent periods?
- **Cross-source consistency tests:** Does this value agree within a defined tolerance with values from other approved sources for the same indicator in the same period?
- **Vintage alignment tests:** Is the vintage date consistent with what the source registry declares?
- **Unit consistency tests:** Are the units consistent with the field's declared unit in the schema?

### The Connection to Backtesting Integrity

Data admission testing is the prerequisite for backtesting integrity. The backtesting framework compares simulation outputs against historical actuals. If the historical actuals have passed through data admission testing, the comparison is meaningful. If they haven't, a backtesting "pass" may be comparing a simulation output against a corrupted historical value — producing false confidence in the model's accuracy.

This is why Issue #253 has the relationship it does to the synthetic data framework: a dataset that fails data admission testing is a candidate for synthetic data generation rather than for corrective manual cleaning. The admission test failure is the signal that triggers the synthetic data inference hierarchy — not a reason to manually fix the data and re-run the test.

---

## Concept 18: The Legibility Metrics Dashboard

### Legibility as a Property That Drifts

Issue #259 establishes a principle that applies to the codebase the same way the no-false-precision principle applies to simulation outputs: **legibility is a property that drifts unfavorably as velocity increases, the same way test coverage drifts without enforcement.**

A codebase is legible when a new contributor — specifically the canonical WorldSim new contributor: a Kenyan central banker, a Bolivian agricultural economist, a Lebanese finance ministry official — can read the code and understand what it does. Legibility is not just documentation quality. It includes: consistent naming conventions, clear module boundaries, absence of unexplained magic numbers, test coverage that documents expected behavior, and error messages that explain what went wrong in terms the user can act on.

As development velocity increases, legibility drifts. Shortcuts get taken. Magic numbers appear. Module boundaries blur. Names become inconsistent. This drift is invisible in the moment — it only becomes visible when a new contributor tries to understand the codebase and cannot.

### The CTO Legibility Metrics Dashboard

The dashboard tracks legibility indicators continuously — not as a one-time audit but as an ongoing pulse:

- **Documentation coverage:** What percentage of public functions have docstrings? What percentage of modules have module-level documentation?
- **Naming consistency:** Are indicator names consistent between the backend schema, the API contract, and the frontend display layer? (The `name_en` / `name` incident is the canonical example of what naming inconsistency costs.)
- **Test coverage as documentation:** Are the tests written in a way that documents expected behavior, or do they only assert that code runs without error?
- **Error message quality:** Do error messages explain what went wrong and what to do about it, or do they produce stack traces?
- **Magic number prevalence:** How many unexplained literal values appear in the codebase?

### Why This Is a First-Class Engineering Concern

The equitable build process principle extends to legibility: "code is written as if it will be read by a Kenyan central banker, a Bolivian agricultural economist, and a Lebanese finance ministry official." That principle is aspirational unless it is measured. The legibility metrics dashboard is the measurement mechanism — the instrument that tells the Engineering Lead whether the codebase is drifting away from the standard it has committed to.

Legibility is also a prerequisite for the distributed simulation ecosystem (Concept 14). A community contributor who cannot understand the codebase cannot contribute a calibrated entity template. The certification process for community templates assumes that contributors can read and understand the existing template implementations well enough to follow the pattern. If the codebase is illegible, the ecosystem cannot grow.

---

## Epilogue: What This Document Is Not

This document does not replace the ADRs. The ADRs are the authoritative architectural decisions — immutable once accepted, amended through formal documented processes. This document explains the reasoning that produced those decisions and the mental models that make them legible.

This document does not replace the GitHub issues. The issues are the tracked commitments — what gets built, in what order, gated by what acceptance criteria. This document explains why the work matters.

This document does not replace the founding document. The founding document explains why WorldSim exists, what problem it solves, and who it serves. This document explains how the technical architecture serves that mission.

All three are needed. The soul, the mind, and the body — the founding document, this document, and the code — each tells a different part of the same story.

---

*Document version 1.0 — synthesized May 2026 from the technical conversations of April–May 2026.*
*Canonical location: `docs/vision/worldsim-technical-concepts.md`*
*Companion to: `docs/vision/worldsim-founding-document.md`*
*This document should be updated when major new technical concepts emerge that are not captured in ADRs or GitHub issues.*
