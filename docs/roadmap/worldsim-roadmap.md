# WorldSim Roadmap

> Last significant revision: 2026-06-16
> Next mandatory review: Milestone 14 close
> Updated against: M14 milestone planning panel deliberation 2026-06-16 — M15/M16/M17/M18 defined; demo arc extended through Demo 7; issue allocation confirmed across all four milestones; scope gaps closed (#986 cohort disaggregation, #987 political risk surface, #988 Goodhart's Law, #989 onboarding docs, #990 accessibility validation)
> Canonical location: `docs/roadmap/worldsim-roadmap.md`

*Note: This document was not updated at M10, M11, M11.5, or M12 close — a gap against the "Roadmap Currency" policy. Updates at those closes are now reflected in the registry and narrative sections.*

*This document is directionally committed, not contractually precise. When scope changes materially, this document is updated with a dated rationale note — not silently overwritten. The change history is the accountability mechanism.*

---

## Milestone Registry (Issue #412)

**This table is the single source of truth for milestone number, canonical title, and core deliverable.** GitHub milestone titles must match the Title column exactly. When a milestone is renamed, update this table and the GitHub milestone title in the same operation — not as a follow-up. Drift between this table and GitHub is a compliance finding.

| Milestone | Canonical Title | Core Deliverable | Status |
|---|---|---|---|
| M0 | Foundation | Simulation engine core, data architecture, PostGIS | Complete |
| M1 | Simulation Core | Event propagation, control inputs, entity model | Complete |
| M2 | Geospatial Foundation | MapLibre frontend, choropleth, territorial validation | Complete |
| M3 | Scenario Engine | Multi-step scenarios, snapshots, API, comparative output | Complete |
| M4 | Human Cost Ledger | DemographicModule, cohort tracking, human development axis | Complete |
| M5 | Calibration and Uncertainty | MacroeconomicModule, banding engine, confidence tiers | Complete |
| M6 | Backtesting Coverage Expansion | Greece fixture, Argentina fixture, fidelity framework | Complete |
| M7 | Technical Foundation | EcologicalModule, GovernanceModule, MDA system | Complete |
| M8 | Ecological and Governance Frameworks | Instrument cluster design, four-framework UX | Complete |
| M9 | Standards Foundation | Standards framework, compliance scan, UX architecture | Complete |
| M10 | Engine Integrity and Instrument Delivery | TrajectoryView, PMM, MDA alerts, matrix investigation groundwork | Complete |
| M11 | Engine Investigation and Political Economy | ADR-009, sparse matrix PoC, Phase 2 A/B validation, PoliticalEconomyModule | Complete |
| M11.5 | Usability Validation and Experience Audit | Priority A usability sessions; universal finding; M12 scope filed | Complete |
| M12 | Active Control and External Sector | Matrix engine production, ExternalSectorModule (ADR-012), Mode 3, Demo 4 | Complete |
| M13 | Political Economy and Instrument Credibility | ADR-013, political economy integration, ADR-014 alert panel UX, instrument legibility, mode transition UX, Process Redesign Phases 0–D | Complete |
| M14 | Trust Architecture and Instrument Credibility | ADR-016 Grounding strip (source provenance), ADR-015 Evidence thread (Zone 1B credibility), PSP in Zone 1D, methodology foundation docs, Demo 5 | Current |
| M15 | Human Cost Architecture | Zone 1A information architecture (ADR), cohort disaggregation design, political risk surface design, approved-source query (Path 1), accessibility validation | Planned |
| M16 | Distributional Visibility | Demo 6: cohort-level distributional output, 25-year human capital trajectory, uncertainty quantification as bands, ecological transmission, Path 2 data upload | Planned |
| M17 | Multi-Scenario Infrastructure | Multi-scenario comparison infrastructure (>2 scenarios), dynamic relationship weights, stock vs. flow at scale, entity template library design | Planned |
| M18 | Comparative Analysis and Full Argument | Demo 7: multi-scenario comparison with distributional overlay, uncertainty bands, full counter-scenario argument at the negotiating table | Planned |

---

## Where We Are

WorldSim v0.12.1+ is released. Fourteen milestones of foundational and delivery work are complete. The simulation engine runs multi-country scenarios with matrix computation. The external sector module enables bilateral trade shocks and commodity price cascades. Mode 3 Active Control lets a finance ministry analyst branch from any simulation step, apply policy instruments, and compare the resulting trajectory against the baseline in real time. All four measurement framework axes are live. The political economy module makes programme survival probability and conditionality dynamics analytically visible. The alert panel (Zone 1B) delivers threshold breach evidence in persistent-detail without interaction. Five historical backtesting cases are validated (Greece, Argentina, Lebanon, Thailand, Ecuador). Demo 4 — a Jordan/Egypt Strait of Hormuz closure scenario — has been presented to stakeholders.

M13 is complete. M14 is the transition from institutional readiness to public availability. The methodology publication makes every model relationship, calibration assumption, and known limitation inspectable. External validation by domain experts outside the project provides independent credibility. The live external demo (#843) is the M14 closure gate — the moment the democratization mission becomes operational rather than aspirational.

The three questions that drove M13 — political feasibility, conditionality design, and medium-term horizon — are now answerable. M14 asks: can we make that answer credible to the world?

M15–M18 are defined and issued-scoped as of 2026-06-16. The roadmap through M18 is directionally committed. The demo arc (Demo 5 through Demo 7) defines the progressive capability story the tool tells to the world across those four milestones.

---

## The Demo Arc

WorldSim follows a two-milestone demo cadence. Each demo tells one coherent story. Stakeholders are not asked to absorb a progress report — they are shown what the tool is at that moment.

**Demo 3 — Milestone 10: WorldSim works.**

The instrument cluster is redesigned. All four measurement framework axes are live with real data. The simulation runs a second country beyond Greece. The tool looks right, works across frameworks, and is credible as an analytical instrument.

A finance ministry analyst can open WorldSim, load the Greece 2010–2015 scenario, and see — without opening a drawer, without navigating away from the primary screen — where the human cost thresholds were crossed, which framework deteriorated first, and how the trajectory across all four dimensions simultaneously diverges from the financial recovery narrative.

**Demo 4 — Milestone 12: WorldSim serves its users.**

The matrix computation engine is in production. The simulation runs multi-country scenarios at scale. A Jordanian finance ministry analyst runs a Strait of Hormuz closure scenario and sees what it means for Jordan's fuel access, food price inflation, and public legitimacy — on a standard laptop, in real time.

The story is the democratization mission made concrete. The tool that showed Greece in Demo 3 now serves the user it was built for — in a scenario no institution has previously given them the analytical tools to navigate.

**Demo 5 — Milestone 14: WorldSim can be trusted.**

The trust architecture is live. A Zambian finance ministry analyst responds to an input challenge at the negotiating table. "Where does that reserve figure come from?" She opens the grounding strip: World Bank WDI, 2023 vintage, Tier 2. "How was the drawdown calculated?" She opens the evidence thread: the methodology is documented, inspectable, and cited. The creditor side cannot challenge the data provenance — because the provenance is on screen.

The story is epistemic credibility. The tool that served the Jordanian analyst in Demo 4 can now be defended under scrutiny — by a minister's team with three economists, against a creditor side with one hundred.

**Demo 6 — Milestone 16: WorldSim shows who bears the cost.**

The human cost ledger is visible. A Senegalese Finance Minister walks into an Article IV consultation. Her team has run the proposed conditionality scenario overnight. On screen: the bottom quintile crosses the poverty threshold at step 2. The 25-year human capital trajectory shows a generation of teachers and doctors leaving the public sector by step 6. The programme survival probability drops to 38% at step 3 — the political feasibility model says the programme collapses before it achieves its fiscal target.

The story is distributional evidence. The argument the ministry team can make is no longer "this is bad in general" — it is "this is bad specifically, for this cohort, at this step, and we have the numbers."

**Demo 7 — Milestone 18: WorldSim shows it didn't have to be this way.**

The counter-scenario comparison is live. A Zambian restructuring team loads three scenarios simultaneously: IMF proposed terms, Zambian counter-proposal, Ghana 2023 restructuring as a regional comparator. The instrument cluster shows overlaid trajectories with uncertainty bands. Under proposed terms: 340,000 additional people below the poverty threshold. Under the counter-proposal: 80,000. The ministry's counter-proposal is now an argument with a specific number differential, a confidence band, and a historical precedent.

The story is the complete analytical stack at the negotiating table: inputs cited, methodology transparent, human cost visible, alternatives compared. The minister's team has parity.

---

## Scope Linkage Requirement

Each milestone entry in this document must enumerate its blocking deliverables
explicitly — not just narratively — and link to the tracking GitHub issue once
filed. A deliverable named here without a linked issue is a visible scope gap.

Format for each blocking deliverable within a milestone entry:
```
- [Deliverable name] → Issue #NNN (horizon:immediate)
```

If the issue has not yet been filed, the entry reads:
```
- [Deliverable name] → UNTRACKED (file issue before kickoff begins)
```

This requirement exists because roadmap.md is designated as the canonical
milestone scope reference in CLAUDE.md. A canonical reference that does not
link to tracked work cannot be audited. The linkage makes the roadmap a diff
surface: any milestone entry with UNTRACKED items is an open kickoff gate.
(NM-019)

---

## Milestone by Milestone

### Milestone 9 — Standards Foundation *(complete)*

**Core deliverable:** A complete UX design foundation and instrument cluster specification that gates all M9–M10 implementation work.

**What ships:**
- Instrument cluster redesign specification — trajectory view as primary Zone 1 instrument, MDA alerts always visible, entity selector as persistent header, EntityDetailDrawer demoted to detail/methodology surface
- Five formal user personas with historical marquee cases as acceptance tests
- Agent working agreements (15 agents) and RACI chart
- Synthetic data framework — Chief Methodologist consultation complete, ADR-007 forthcoming
- GovernanceModule promotion path — five promotion criteria defined, target M9 close
- UX architecture ADRs (ADR-008 and ADR-010) through governed process
- Document referencing convention — revision headers on living documents, ADR as stable reference point
- Architecture Backlog process — pre-ADR queue to prevent numbering conflicts

**Demo:** None. M9 is the design foundation that makes the M10 demo possible.

**Canonical user primarily served:** Lucas Ferreira (Programme Analyst) and Eleni Papadimitriou (Finance Ministry Negotiator) — the two personas whose Mode 1 and Mode 3 requirements drive the instrument cluster specification.

**What M9 does not do:** M9 does not implement the instrument cluster redesign. It specifies, governs, and gates it. Implementation is M10.

---

### Milestone 10 — Engine Integrity and Instrument Delivery

**Core deliverable:** The instrument cluster redesign implemented, all four radar axes live with real data, and a second country backtesting fixture. The tool that Demo 3 will show.

**What ships:**
- Instrument cluster implementation — trajectory view as Zone 1 primary, MDA alerts always visible without navigation, step axis annotated with calendar dates and event labels → Issues #495, #496, #497, #498, #499, #500 (horizon:immediate)
- GovernanceModule promoted — governance axis live with real data; five ADR-005 Amendment 4 promotion criteria → Issue #556 (horizon:immediate) [filed 2026-05-30; blocking prerequisite: #523 IB+DQ agent definitions]
- PMM (Policy Manoeuvre Margin) live computation → Issue #496 (horizon:immediate)
- Second country backtesting fixture — Argentina 2000–2002 (confirmed 2026-05-30) → Issue #553 (horizon:immediate) [CM data availability check is blocking prerequisite before implementation]
- Mean-reversion channel → Issue #221 (M11) [EL decision 2026-05-30: M11 deferral accepted. Greece MAGNITUDE fidelity gap at stabilisation cases is acknowledged. Demo 3 proceeds without the mean-reversion channel. Deferred to M11 where engine integrity is the milestone theme and MacroeconomicModule fidelity work is in scope alongside ADR-009.]
- Phase 1 baseline benchmarks — iterative engine on target hardware (4-core/8GB laptop AND GitHub Actions free-tier runner) → Issue #514 (horizon:immediate) [moved from M11 to M10 per NM-020, 2026-05-25; prerequisite for ADR-009 authoring in M11; Chief Engineer activation required]
- step_event_label mandatory field on all Mode 1 fixtures → Issue #395 (horizon:immediate)
- Playwright demo advancement test and legibility assertions → Issues #376, #377 (horizon:immediate)
- Confidence tier standards (SA-02) — prerequisite for M11 uncertainty quantification → Issue #43 (horizon:immediate)

**Demo:** Demo 3 at M10 close. All four frameworks live. Second country live. Instrument cluster redesigned.

**Canonical user primarily served:** Aicha Mbaye (Institutional Decision-Maker) in Demonstrative entry state — the M10 demo is the first time WorldSim is shown in its complete form.

**What M10 does not do:** M10 does not introduce the matrix computation engine. No matrix code ships in M10. M10 does not model political economy constraints on programme design — that is M11 scope.

---

### Milestone 11 — Engine Investigation and Political Economy *(no demo)*

**Primary objective:** A complete empirical understanding of the simulation engine's performance characteristics and a validated proof-of-concept matrix engine running in parallel with the iterative engine. M11 closes when the matrix engine investigation track is complete — the political economy module does not block M11 closure.

**Stretch goal:** Political economy module — political feasibility constraints, conditionality modelling, elite capture dynamics, coalition stability. Ships in M11 if the primary objective is complete with milestone capacity remaining. If not started in M11, carries to M12.

**Rationale (EL decision 2026-06-03):** Both tracks were originally listed as co-equal M11 deliverables. The PM Agent flagged the risk that both cannot realistically ship in the same milestone alongside ADR-009 authoring, which is itself time-intensive research work. The sparse matrix investigation is the foundational architectural decision; the political economy module is additive domain coverage. When scope must be reduced, reduce analytical sophistication before reducing architectural integrity.

**What ships — Primary (M11 exit gate):**

*Matrix engine investigation (Chief Engineer owned):*
- Phase 1 baseline benchmarks — [moved to M10, Issue #514 (horizon:immediate), per NM-020 2026-05-25; ADR-009 authoring depends on M10 benchmark results before matrix investigation begins]
- ADR-009 authored and accepted — after Phase 1 results, before any matrix code written
- Sparse matrix proof-of-concept — matrix engine running alongside iterative engine. Not a replacement.
- Phase 2 A/B validation — output equivalence to Decimal precision, performance comparison on identical hardware, full backtesting suite passing identically on both engines
- Matrix interpretability tooling — contribution tracing, transformation visualization, computation anomaly detection (separate alert channel from MDA threshold system)
- Phase 3 stress test suite — load levels 1x through 1000x on target hardware. Permanent test infrastructure artifact.

**What ships — Stretch goal (ships if primary is complete):**

*Political economy module:*
- Political feasibility constraints as scenario inputs
- Conditionality modelling — IMF terms as structured scenario inputs
- Elite capture dynamics
- Coalition stability as a simulation state variable

**Demo:** None. M11 is the investigation milestone. ADR-009 is the most consequential architectural decision the project will make — it deserves a milestone without a demo clock running.

**Canonical user primarily served:** The Chief Engineer and Architect Agent — M11 is primarily an internal architectural milestone whose outputs enable M12.

**What M11 does not do:** M11 does not migrate the production engine. The iterative engine remains in production at M11 close. The matrix engine is a validated proof-of-concept, not a replacement. Production migration is M12. M11 does not guarantee political economy module delivery — that delivery depends on capacity remaining after the primary objective is complete.

---

### Milestone 12 — Transformation and External Sector

**Core deliverable:** The matrix computation engine in production, the external sector module enabling multi-country trade and geopolitical scenarios, and the democratization use case made concrete for a global south finance ministry analyst.

**What ships:**

*Matrix engine migration:*
- Production migration — iterative engine retired after Phase 2 equivalence confirmed across full backtesting suite → Issue #749 (horizon:immediate)
- Cloud compute path scoped — infrastructure design documented, pricing model proposed for high-resolution institutional use cases → Issue #750 (horizon:immediate)

*External sector module:*
- Bilateral trade shock as standard scheduled input type — enables Canadian steel tariff scenarios and similar trade policy cases → Issue #751 (horizon:immediate)
- Commodity price shock as global parameter propagating through relationship graph — enables Hormuz closure, multi-country cascade scenarios → Issue #752 (horizon:immediate)
- Multi-scenario comparison lifted beyond two-scenario limit — enables Kenya budget planning with three competing proposals → Issue #394 (horizon:near-term)

*Mode 3 active control:*
- Policy instrument inputs with live trajectory response and automatic A/B comparison → Issue #753 (horizon:immediate)
- Multi-country scenario configuration → Issue #754 (horizon:immediate)

*UX prerequisites (from M11.5 exit findings — added 2026-06-05):*
- Persistent scenario identity header → Issue #744 (horizon:immediate)
- Interactive alert panel with drill-in → Issue #745 (horizon:immediate)
- Mode 2 fiscal multiplier parameter input → Issue #746 (horizon:immediate)
- Zone 1 cohort disaggregation → Issue #747 (horizon:immediate)

**Demo:** Demo 4 at M12 close. A Jordanian finance ministry analyst runs a Strait of Hormuz closure scenario on a standard laptop. The democratization mission made concrete. → Issue #755 (horizon:immediate)

**Canonical user primarily served:** Persona 2 (Finance Ministry Negotiator) in Mode 3 active control — in a global south context rather than European.

**What M12 does not do:** M12 does not introduce the entity template library. Transport fuel, food system, and electricity templates are M13+ scope.

---

### Milestone 13 — Political Economy and Instrument Credibility *(complete)*

**Core deliverable:** The political economy module makes programme feasibility constraints and conditionality design analytically visible. Instrument legibility makes the tool credible in a live negotiation room without a technical presenter.

**What ships:**
- ADR-013 — political economy module boundary definition; panel composition and acceptance gate
- Political economy module — conditionality modelling as structured scenario inputs, elite capture dynamics, programme survival probability (political feasibility constraints)
- Alert panel UX (Zone 1B) — master-detail layout; ADR required before implementation; EL decision 2026-06-11: Frontend architecture review + UX Designer + Design Thinking agent input required → Issue #852
- Instrument legibility improvements — DEMO-059–064 resolved; Demo 5 readiness
- Process Redesign Phase A deliverables (parallel track)

**Demo:** None (M13). Demo 5 at M14.

**Canonical user primarily served:** Persona 2 (Finance Ministry Negotiator) in a live negotiation context — the three analytical gaps identified in Demo 4 close such that "Can this government actually deliver this programme?" becomes answerable at the table.

**What M13 does not do:** M13 does not publish the methodology publicly. External validation and TSC formation are M14 scope. M13 does not deliver a live external demo — that gates M14 closure (#843).

---

### Milestone 14 — Trust Architecture and Instrument Credibility *(current)*

**Core deliverable:** WorldSim is ready for institutional adoption. The methodology is published, externally validated, and inspectable by anyone.

**Demo 5 story:** *"The minister's team can now defend their inputs and trace the output reasoning to a published methodology."*

**What ships:**
- ADR-016 implementation — entity selector, data quality preview, grounding strip (source-cited initial state) → G3/G4 (no standalone issue; tracked in sprint plan)
- ADR-015 implementation — evidence thread, L0 basis annotations, L1 basis statement, L2 evidence chain → G5 (no standalone issue; tracked in sprint plan)
- Prerequisite bug fixes — entity selector (#961), step counter (#962), choropleth labels (#963) → Issue #961, #962, #963 (horizon:immediate)
- Calibration and methodology — reserve_coverage_months (#884), Exploratory tier (#885), ecological composite (#823), MENA calibration (#824), Zone 1A Y axis (#950), confidence tier disclosure (#22 — disclosure layer only; full distributional bands → M16) → Issues #884, #885, #823, #824, #950, #22 (horizon:immediate)
- TSC formation → Issue #3 (horizon:immediate)
- Branch protection restoration → Issue #6 (horizon:immediate)
- Goodhart's Law mitigation design — TSC monitoring framework for parameterization gaming risk → Issue #988 (horizon:immediate)
- Onboarding documentation for global south finance ministry analysts → Issue #989 (horizon:immediate)
- Zone 1A Phase 1 design thinking (G6c) — UX Designer document gating M15 architecture review → Issue #845 Phase 1 (horizon:immediate)
- Path 2 design groundwork (G6b) — field mapping UX, USER_SUPPLIED provenance spec, data isolation sketch → Issue #976 design artifacts (horizon:immediate)
- Live stakeholder demo with real external participants — M14 closure gate → Issue #843 (horizon:immediate)

**Demo:** Demo 5 at M14 close.

**Canonical user primarily served:** Persona 2 (Finance Ministry Negotiator) in Reactive entry state — the trust architecture makes her inputs defensible at the table.

**What M14 does not do:** M14 does not surface cohort disaggregation on the primary viewport (M15 design, M16 implementation). M14 does not ship full distributional uncertainty bands (M16). M14 does not enable multi-scenario comparison (M17/M18).

---

### Milestone 15 — Human Cost Architecture *(planned)*

**Core deliverable:** The design and architectural foundation that makes Demo 6 possible. No demo at M15 close — M15 builds what M16 shows.

**What ships:**
- Zone 1A information architecture — Phase 2 (ARCH-REVIEW with DIC) and Phase 3 (ADR) gating M16 distributional implementation → Issue #845 Phases 2–3 (horizon:immediate)
- Cohort disaggregation design — specifies how bottom-quintile threshold crossings surface in the primary viewport; may be subsumed into Zone 1A ADR → Issue #986 (horizon:immediate)
- Political risk summary surface design — plain-language legitimacy dynamics for Persona 3; design and any required ADR → Issue #987 (horizon:immediate)
- Path 1 — user-directed query from approved source network at scenario creation → Issue #975 (horizon:immediate)
- Information access architecture (RBAC design) — prerequisite for Path 2 data isolation → Issue #53 (horizon:immediate)
- Zone 1A Y axis and Mode 3 branch comparison values → Issues #950 (if not completed in M14 G6), #846 (horizon:near-term)
- Threshold-crossing markers in comparative output → Issue #97 (horizon:near-term)
- Absolute threshold overlay on DeltaChoropleth → Issue #153 (horizon:near-term)
- Greece backtesting expansion (investment climate initial conditions) → Issue #92 (horizon:near-term)
- Config-driven demo scripts → Issue #837 (horizon:near-term)
- CTO legibility metrics dashboard → Issue #259 (horizon:near-term)
- Mode 3 hardware validation (MV-002) → Issue #569 (horizon:near-term)
- Solo-use review protocol → Issue #951 (horizon:near-term)
- Accessibility validation on target hardware (8GB/4-core) → Issue #990 (horizon:near-term)

**Demo:** None (M15). Demo 6 at M16.

**Canonical user primarily served:** Persona 4 (Academic Researcher, Amara Diallo) and Persona 2 — M15 is the methodology depth and data access milestone that serves both.

**What M15 does not do:** M15 does not implement cohort disaggregation or distributional output (M16). M15 does not implement Path 2 proprietary data upload (requires Issue #53 design decisions from M15 before M16 implementation can begin).

---

### Milestone 16 — Distributional Visibility *(planned)*

**Core deliverable:** The human cost ledger is operationally visible. A finance minister can cite which cohort bears the cost, at which step, with what confidence, against a 25-year horizon. Demo 6 shows this.

**Demo 6 story:** *"Here is who bears the cost — specifically, this cohort, at this step, for this long."*

**What ships:**
- Cohort disaggregation on primary surface — bottom-quintile threshold crossings visible in primary viewport within 90-second retrieval ceiling → Issue #986 (horizon:immediate)
- Political risk summary surface for Persona 3 — programme survival probability and legitimacy trajectory in plain language → Issue #987 (horizon:immediate)
- Distributional scenario comparison — variance and percentile ranges by cohort → Issue #102 (horizon:immediate)
- 25-year human capital depletion trajectory → Issue #274 (horizon:immediate)
- Calibrated ecological-to-financial transmission — resource curse → fiscal capacity chain → Issue #275 (horizon:immediate)
- Uncertainty quantification — full distributional output as scenario bands (builds on ADR-015 evidence thread) → Issue #22 full implementation (horizon:immediate)
- Dynamic relationship weight updating → Issue #35 (horizon:near-term)
- Stock vs. flow variable distinction in entity attribute model → Issue #30 (horizon:near-term)
- Path 2 — ministry-owned proprietary data upload with field mapping (implementation; depends on Issue #53 from M15) → Issue #976 (horizon:near-term)

**Demo:** Demo 6 at M16 close. Senegalese Finance Minister scenario. The human cost argument becomes specific.

**Canonical user primarily served:** Persona 5 (Institutional Decision-Maker, Aicha Mbaye) and Persona 2 — the distributional evidence is what Aicha presents to her cabinet and what Eleni cites at the table.

**What M16 does not do:** M16 does not enable comparison of more than two scenarios simultaneously (M17). M16 does not deliver the entity template library.

---

### Milestone 17 — Multi-Scenario Infrastructure *(planned)*

**Core deliverable:** The comparison infrastructure that makes Demo 7 possible. No demo at M17 close.

**What ships:**
- Multi-scenario comparison (>2 scenarios) — Kenya budget planning use case → Issue #394 (horizon:immediate)
- Entity template library — initial templates (transport fuel, food systems) → Issue #407 (horizon:near-term)
- Data marketplace design — curated dataset registry → Issue #5 (horizon:near-term)
- Advanced geocoded dataset integration → Issue #4 (horizon:near-term)

**Demo:** None (M17). Demo 7 at M18.

**Canonical user primarily served:** Persona 7 (Parliamentary Economist, James Ochieng) — the multi-scenario comparison enables the independent fiscal analysis his PBO mandate requires.

---

### Milestone 18 — Comparative Analysis and Full Argument *(planned)*

**Core deliverable:** The complete analytical stack at the negotiating table. A finance ministry team can load three scenarios, show who bears the cost under each, compare the distributional outcomes, and cite the counter-proposal with a specific number differential.

**Demo 7 story:** *"Here is what we proposed instead — side by side, with error bars, with human cost consequences."*

**What ships:**
- Multi-scenario comparison with distributional overlay — three+ scenarios, overlaid trajectories with uncertainty bands → builds on Issue #394
- Counter-scenario comparison showing distributional differences under each pathway
- Path 2 full implementation — ministry-owned proprietary data integrated into multi-scenario comparison
- Entity template library operational — additional countries navigable in comparison

**Demo:** Demo 7 at M18 close. Zambian restructuring team scenario. The ministry team has negotiating parity.

**Canonical user primarily served:** Persona 2 (Finance Ministry Negotiator) and Persona 5 (Institutional Decision-Maker) — the moment the tool's full promise is operationally real.

---

## The Long-Term Direction

**The resolution spectrum.** The simulation currently operates at the coarse end of a resolution spectrum — nation-level entities, aggregate indicators. The entity template library is the mechanism for moving up the spectrum selectively, where the variability spread justifies the further decomposition. Transport fuel, food systems, and electricity are the founding template candidates. Each addition improves simulation fidelity for scenarios where that system's dynamics matter — without affecting scenarios where it doesn't. See Issue #407 for the full architectural specification.

**The two-path infrastructure model.** The equity commitment — WorldSim runs on a four-core laptop — applies permanently to the core use case. High-resolution template scenarios with many specialized entities across multiple countries are served by an on-demand cloud compute path. Both paths run the same computation model. The infrastructure path is an operational choice, not an architectural one.

**Continuous improvement without forced migration.** New entity templates ship when calibrated and validated. New countries are added to the source registry as data becomes available. New backtesting fixtures are contributed by the community of practice. The flywheel operates through this continuous improvement path rather than version-gated feature releases.

---

## Roadmap Currency

This document is updated at every milestone close — as part of the exit ceremony, not as a separate activity. It will never be more than one milestone cycle out of date.

**Updates are triggered by:**
- Milestone close (mandatory review — scope confirmed or updated with dated rationale)
- A significant scope decision that materially changes a future milestone's shape
- A new marquee case or real-world event that reshapes the tool's priorities
- An ADR acceptance that changes the sequencing of future work

When an update is made, the revision header changes and a dated note is added explaining what changed and why. Between updates, the document is stable and can be relied upon as an accurate representation of the project's direction at the time of last revision.

**This roadmap is not a delivery contract.** It is a directional commitment with honest uncertainty. When reality diverges from the roadmap, the document is updated to reflect reality — not defended against it.

The one commitment that does not change regardless of scope: the tool is built for the quinoa farmer in Bolivia who will never know it exists, but whose government may make better decisions because it does.
