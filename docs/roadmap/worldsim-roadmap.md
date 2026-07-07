# WorldSim Roadmap

> Last significant revision: 2026-07-06
> Next mandatory review: Milestone 20 close
> Updated against: M19 close — Constraint Search and Empirical Calibration complete; Mode 3 constraint-floor search, SEN/ZMB backtesting, ten real-world battle-testing scenarios, empirically grounded CI intervals (ADR-007 Bayesian layer), PSP driver arc + auditability panel, ELASTICITY_REGISTRY non-SSA calibration (GRC/LAC/SEA + ARG Kirchner), Zone 1A display fidelity and trackwheel zoom, ADR-020 capital controls channels all delivered; Demo 8 simulated stakeholder session north star PASS (constraint-derived boundary, 2026-07-06); M20 now current
> Previous version context: 2026-07-02 — M18 closed; M19 active; Demo 8 at M19 close
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
| M14 | Trust Architecture and Instrument Credibility | ADR-016 Grounding strip (source provenance), ADR-015 Evidence thread (Zone 1B credibility), PSP in Zone 1D, methodology foundation docs, Demo 5 | Complete |
| M15 | Human Cost Architecture | ADR-017 Zone 1A, Layer 3 self-interpreting outputs, Path 1 approved source, cohort/political risk designs, accessibility validation | Complete |
| M16 | Distributional Visibility | Zone 1A Phase 4; cohort disaggregation; political risk summary; 25-year trajectory; ecological-fiscal transmission; uncertainty quantification; Demo 6 prep (Steps 1–6c; DEMO6 findings on record) | Complete |
| M17 | Calibration and Comparative Infrastructure | Wave 1: CM calibration (fiscal-to-cohort elasticity #1229, governance sensitivity #1248, FRAME-D gate); Wave 2: N=3 multi-scenario (#394), DEMO6 CRITICAL polish (#1249/#1250/#1253/#1239), adaptive y-axis (#1251), Zone 1B proportional allocation ADR-018 (#1252), GovernanceModule institutional_capacity_index (#1275) | Complete |
| M18 | Full Argument and Demo 7 | Demo 7 (Senegal Mode 3 + Zambia three-scenario, simulated stakeholder session #843); counter-scenario comparison; CI bands (ADR-007 full implementation); PSP driver decomposition; control plane column (ADR-019); Zone 3 auditability panel | Complete |
| M19 | Constraint Search and Empirical Calibration | Mode 3 constraint-floor search; SEN/ZMB backtesting; 10 battle-testing scenarios; empirically grounded CI intervals (ADR-007 Bayesian layer); PSP driver arc and auditability panel; ELASTICITY_REGISTRY non-SSA calibration (CM Sprints A/B/C/D); Zone 1A display fidelity and interaction layer; ADR-020 capital controls; Demo 8 | Complete |
| M20 | Analytical Evidence Portfolio and Demo 9 | AEP first 11 entries (all four calibration families); Mode 3 instrument polish (DEMO-217, 233, 234); gap closure issues filed; Demo 9 | Current |

---

## Where We Are

WorldSim v0.19.0 is released. Twenty milestones of foundational and delivery work are complete.

M19 is complete. The constraint-floor capability is delivered: the instrument finds configurations that avoid the human cost floor — the ministry team no longer tests one multiplier value at a time. SEN and ZMB backtesting are live; the empirical CI layer (ADR-007 Bayesian posterior across ten real-world cases) gives confidence intervals a grounding the prior structural model could not provide. ELASTICITY_REGISTRY non-SSA calibration closes the MAGNITUDE gap for Greece, Argentina, Pakistan, Sri Lanka, Bangladesh, Bolivia, Ecuador, and Peru. ADR-020 capital controls channels complete the Iceland 2008–11 fixture. Demo 8 simulated stakeholder session (2026-07-06): north star PASS. The boundary is now constraint-derived — the instrument found 0.83, not the presenter.

M19 asks and answers: can the instrument do the search itself — find where the human cost floor is, rather than making the analyst iterate? Yes. At ZMB fiscal multiplier 0.83, the poverty headcount crosses the recovery floor. Below 0.83 it does not. The instrument found that number; the presenter cited it. "The constraint-floor boundary is 0.83. Your proposed programme, which assumes a multiplier above 0.83, embeds the poverty crossing as a structural consequence — not of the adjustment itself." The finding is the instrument's, not the narration's.

M20 is current. The AEA's first commissioned session (M19 exit / M20 kickoff) established the analytical evidence infrastructure: Evidence Entry Template, Analytical Framework, and Coverage Audit. M20 now builds the portfolio itself — 11 entries across all four calibration families, grounding the engine's outputs in a documented, quality-tiered evidence record that finance ministry analysts can cite. Mode 3 instrument polish (DEMO-217, -233, -234) closes as maintenance. Live interactive constraint-floor search — the original M20 primary — defers to M21 to give the AEP the milestone bandwidth it needs.

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

Demo 7 runs in two acts, continuous.

*Act 1 — Senegal, Mode 3:* The Demo 6 scenario is already loaded. Step 2. The analyst activates Mode 3 and asks one question: is there a fiscal instrument configuration that avoids the bottom quintile crossing the 0.40 recovery floor? The tool runs the interrogation. One of two things happens — and both are the answer. Either a configuration exists that prevents the crossing: the counter-proposal is found. Or no configuration within the programme's fiscal envelope prevents the crossing: the conditionality structure itself is the binding constraint. That is the most powerful finding the tool can produce. The ministry's argument is no longer "this is too harsh" — it is "there is no version of this programme, on these terms, that does not cross this threshold."

*Act 2 — Zambia, comparison:* A Zambian restructuring team loads three scenarios simultaneously: IMF proposed terms, Zambian counter-proposal, Ghana 2023 restructuring as a regional comparator. The instrument cluster shows overlaid trajectories with uncertainty bands. Under proposed terms: 340,000 additional people below the poverty threshold. Under the counter-proposal: 80,000. The ministry's counter-proposal is now an argument with a specific number differential, a confidence band, and a historical precedent.

The story is the complete analytical stack at the negotiating table: inputs cited, methodology transparent, human cost visible, alternatives compared, counter-scenario quantified. The minister's team has parity.

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

### Milestone 14 — Trust Architecture and Instrument Credibility *(complete)*

**Core deliverable:** The trust architecture is live. A ministry analyst can defend her inputs and trace the output reasoning to a published methodology.

**Demo 5 story:** *"The figure you are challenging is from your institution's own publication."*

**What shipped:**
- ADR-016 — Scenario Grounding Architecture: entity selector, data quality preview, Grounding strip (source-cited initial state at zero interaction) — G3/G4
- ADR-015 — Evidence Thread Architecture: Zone 1B full indicator names + negotiation-defensibility labels + floor distance; Zone 1D L0 tier annotations; Assumption Surface; Political Feasibility row — G5
- Prerequisite bug fixes — entity selector (#961 closed), step counter (#962 closed), choropleth labels (#963 closed) — G1
- Calibration and methodology: reserve_coverage_months (#884 closed), Exploratory tier (#885 closed), ecological composite denominator (#823 closed), MENA arid-economy calibration (#824 closed), Zone 1A Y axis (#950 closed), confidence tier disclosure layer (#22 partial — full distributional bands → M16)
- Goodhart's Law mitigation design — TSC monitoring framework (#988 closed)
- Onboarding documentation for global south finance ministry analysts (#989 closed)
- Zone 1A Phase 1 design thinking (G6c) — UX Designer document gating M15 architecture review (#845 Phase 1 delivered)
- Path 2 design groundwork (G6b) — field mapping UX, USER_SUPPLIED provenance spec, data isolation sketch (#976 design artifacts delivered)
- Demo 5 delivered 2026-06-20 — Zambia 2024 IMF ECF six-step programme review

**What M14 did not do (explicitly deferred):**
- Layer 3 trajectory sentence in Zone 1B (#1065 → M15) — sentence that says "at the current draw rate, the CRITICAL floor is reached within one step"
- PSP self-interpreting sentence (#1075 → M15) — Zone 1D shows number only; no narrative translation
- Live external demo with real participants (#843 → M15) — simulated session accepted as M14 closure evidence (EL decision 2026-06-20)
- Full distributional uncertainty bands (#22 full → M16)

**Demo:** Demo 5 delivered 2026-06-20 (simulated stakeholder session; real external participants in M15 via #843).

**Canonical user primarily served:** Persona 2 (Finance Ministry Negotiator) in Reactive entry state — the trust architecture makes her inputs defensible at the table.

---

### Milestone 15 — Human Cost Architecture *(complete)*

**Core deliverable:** Layer 3 self-interpreting output at the table, and the architectural foundation for M16 distributional visibility. M15 makes the human cost argument specific enough to cite. Live external engagement deferred to M16 (EL decision 2026-06-23).

**What shipped:**
- ✅ Layer 3 trajectory sentence in Zone 1B (#1065) — "at the current draw rate, the CRITICAL floor is reached within one step"
- ✅ PSP self-interpreting sentence in Zone 1D (#1075) — plain-language translation without economist mediation
- ✅ L0 confidence tier badges on Zone 1A trajectory curves (#1068)
- ✅ Dual reserve value disambiguation in Grounding strip (#1069)
- ✅ Suppress "0 consecutive steps" counter when zero (#1066)
- ✅ Grounding strip date label accuracy (#1083 — "Apr 2024" format)
- ✅ Zone 1A information architecture — ADR-017 accepted; Phase 2 (ARCH-REVIEW-007) + Phase 3 (ADR) complete → #845 Phases 2–3
- ✅ Cohort disaggregation design (#986) — bottom-quintile threshold crossings in primary viewport; ready for M16 implementation
- ✅ Political risk summary surface design (#987) — plain-language legitimacy dynamics for Persona 3; ready for M16 implementation
- ✅ Path 1 — user-directed query from approved source network at scenario creation (#975)
- ✅ Accessibility validation on target hardware (8GB/4-core): VC-1/VC-2/VC-4 PASS; VC-3 CONDITIONAL PASS (#990)
- ✅ PSP historical calibration anchor (Zambia/Ghana ECF) (#1084)
- ✅ Recompute-badge immediate state (#1007); Docker Alembic auto-migration (#1048)
- ✅ CLAUDE.md extraction to child docs (agent-execution-lifecycle.md + milestone-exit-sop.md; 1,082→800 lines) (#1091)
- ✅ AC-001 (private data inputs permanently prohibited) + AC-002 (synthetic substitution permitted with disclosure) architectural constraints established
- ⏭ Live stakeholder demo with real external participants (#843) — deferred to M16 (EL decision 2026-06-23); M16 exit gate
- ⏭ RBAC design (#53) — permanently closed (AC-001)

**Demo:** Demo 5 delivered 2026-06-20 (Zambia 2024 IMF ECF). Demo 6 at M16 with real external participants.

**Canonical user primarily served:** Persona 5 (Aicha Mbaye, Finance Minister) and Persona 2 (Finance Ministry Negotiator) — M15 closes the self-interpreting output gap and establishes the Zone 1A architectural foundation for M16 distributional output.

**What M15 did not do:** M15 did not implement cohort disaggregation or distributional output on the primary surface (M16 implementation). M15 did not run live external participant engagement (deferred to M16).

---

### Milestone 16 — Distributional Visibility *(complete)*

**Core deliverable:** The human cost ledger is operationally visible. A finance minister can cite which cohort bears the cost, at which step, with what confidence, against a 25-year horizon.

**Demo 6 story:** *"Here is who bears the cost — specifically, this cohort, at this step, for this long."*

**What shipped:**
- ✅ Zone 1A implementation (Phase 4) — composite encoding in primary viewport (#845); Zone 1D delta annotations (#1147)
- ✅ Cohort disaggregation on primary surface — CohortImpactSection in Zone 1B; bottom-quintile threshold crossings visible in primary viewport within 90-second retrieval ceiling → Issue #986
- ✅ Political risk summary surface for Persona 3 — PSP severity label (CRITICAL/WARNING/WATCH/STABLE) in Zone 1D; plain-language sentence readable without economist mediation → Issue #987
- ✅ Distributional scenario comparison — variance and percentile ranges by cohort → Issue #102
- ✅ 25-year human capital depletion trajectory → Issue #274
- ✅ Calibrated ecological-to-financial transmission — Zimbabwe 2000 calibration anchor → Issue #275
- ✅ Uncertainty quantification — SyntheticDataEngine + quantity table + Zone 1B tier badges → Issue #22 (partial; AC-F6 Zone 1D deferred)
- ✅ Adaptive y-axis scaling — computeYDomain() for TrajectoryView; resolves IR-001 Zone 1A curve overlap at FIN/GOV separation < 0.05 → PR #1243
- ✅ G9 polish (threshold overlay, Mode 3 branch comparison values, threshold-crossing markers, Greece backtesting)
- ✅ G10 pre-demo polish (entity attribution, SAD badge, T3 badge sublabel, Q2 asymmetry label, milestone sentence year anchor)
- ✅ Demo 6 preparatory work complete — Steps 1–6c delivered: screenshot brief, full walkthrough, narrated specification, five frames captured, internal review, IR review, adaptive y-axis fix, audience simulation (DEMO6-001–049 findings on record), north star finding sentence filed
- ⏭ Live stakeholder demo with real external participants (#843) — deferred to M17/Demo 7 (EL decision 2026-06-25); DEMO6 legibility and calibration gaps addressed holistically alongside Mode 3
- ⏭ Dynamic relationship weight updating (#35) — Parking Lot (EL decision 2026-06-21)
- ⏭ Stock vs. flow variable distinction (#30) — Parking Lot (EL decision 2026-06-21)

**Demo:** Demo 6 preparation complete (Steps 1–6c). Live external session deferred to M17/Demo 7 (EL decision 2026-06-25). Primary finding sentence on record: *"Under this programme, the poorest informal workers in Senegal are six months away from a poverty threshold they would not recover from for a decade — and the government may not have the political capacity to deliver the conditionality either."*

**Canonical user primarily served:** Persona 5 (Aicha Mbaye, Finance Minister) and Persona 2 (Finance Ministry Negotiator) — the distributional evidence is what Aicha's team presents at the Article IV consultation.

**What M16 did not do:** M16 did not run the live external demo (#843 — deferred). M16 did not enable comparison of more than two scenarios simultaneously (M17). M16 did not deliver CI bands on Zone 1A trajectories (ADR-007 scope, M18). M16 did not surface PSP driver decomposition (M18).

---

### Milestone 17 — Calibration and Comparative Infrastructure *(complete)*

**Core deliverable:** A calibrated engine and comparative infrastructure that makes Demo 7 analytically defensible. No demo at M17 close. M17 is the prerequisite milestone — the work here is the condition of possibility for everything Demo 7 claims.

M17 is structured in two waves. **Wave 2 may not begin until Wave 1 produces a calibrated elasticity baseline.** This is a hard gate, not a scheduling preference. Running the multi-scenario infrastructure or the DEMO6 polish work before the calibration is settled would build on a miscalibrated response surface — the Demo 7 Mode 3 interrogation is only analytically meaningful if the fiscal-to-cohort transmission channel reflects the empirically defensible elasticity.

---

**Wave 1 — Chief Methodologist Calibration Sprint** *(M17 entry gate; Wave 2 blocked until Wave 1 exit)*

*Scope uncertainty notice:* The fiscal-to-cohort elasticity calibration (#1229) involves genuine research work. The Chief Methodologist must determine: (1) whether `fiscal_policy_spending_change` should have direct elasticity entries bypassing the GDP multiplier chain; (2) whether the GDP multiplier should be larger for social spending cuts specifically; (3) whether the current T3 calibration accurately represents the uncertainty at that tier or whether the response surface is simply miscalibrated. Candidate sources are already in ELASTICITY_REGISTRY (IMF 2014, Lustig 2017, Ball et al. 2013). The CM review may conclude that one of these possibilities is correct, or it may identify a new calibration approach. **M17 Wave 2 cannot begin until Wave 1 delivers a written calibration decision with the revised elasticity constants and a confirmed test that the FRAME-D milestone sentence fires within an 8-step programme window on the Demo 6 scenario.** If Wave 1 takes longer than estimated, M17 slips rather than Wave 2 beginning on a miscalibrated base.

*Wave 1 exit gate:* The FRAME-D milestone sentence fires within the Demo 6 window after the calibration change. DemographicModule ELASTICITY_REGISTRY updated with CM-certified values. Governance sensitivity specification (see below) is produced even if implementation is Wave 2.

- Fiscal-to-cohort elasticity calibration — DemographicModule ELASTICITY_REGISTRY revision; CM certification required → Issue #1229 (horizon:immediate; CM-owned)
- Governance sensitivity calibration — GovernanceModule response to fiscal conditionality events; institutional capacity degradation under austerity; `imf_program_acceptance` direct governance transmission pathway; whether the 8-step window is sufficient to manifest governance divergence or whether governance stress is a longer-horizon signal → Issue #1248 (horizon:immediate; CM-owned)

---

**Wave 2 — Comparative Infrastructure and DEMO6 Polish** *(begins after Wave 1 exit gate)*

*Scope:* Multi-scenario infrastructure enabling Demo 7 Act 2, plus the DEMO6 CRITICAL and HIGH findings that would visibly undermine Demo 7 if unaddressed, plus the adaptive y-axis pattern extension established in M16.

- Multi-scenario comparison (>2 scenarios) — Kenya budget planning use case; enables Demo 7 Act 2 Zambia three-scenario comparison → Issue #394 (horizon:immediate)
- DEMO6-014: Zone 1A curves visually indistinguishable at presentation scale — terminal endpoint labels or dashed/solid line style differentiation; Human Development curve must be identifiable at a glance without presenter narration → Issue #1249 (horizon:near-term)
- DEMO6-026/043: Zone 1B cohort values not legible at tablet scale — CohortImpactSection current value, floor, and T3 badge must be readable at 768px width without zoom → Issue #1250 (horizon:near-term)
- DEMO6-040: No historical precedent anchor for PSP WARNING in Zone 1D — comparable programme reference accessible from Zone 1D surface; comparable cases at WARNING level with known compliance outcomes; enables Andreas's political brief argument and Lucas's reproducibility threshold → Issue #1253 (horizon:near-term)
- Adaptive y-axis extension — `computeYDomain()` pattern (PR #1243) applied to any additional instrument that exhibits the overlap failure mode identified in IR-001; confirm no other instrument has a fixed-domain chart that would obscure small-range values → Issue #1251 (horizon:near-term)
- Zone 1B proportional allocation — formal split between MDAAlertPanelZone1B and CohortImpactSection; replace `minHeight: 80px` temporary guarantee with a durable proportional design; ADR decision required (ADR-017 amendment or new ADR) → Issue #1252 (horizon:near-term)

*Wave 2 deferred (not M17 scope):*
- Entity template library (#407) — deferred to M19+; not on Demo 7 critical path
- Data marketplace design (#5) — deferred to M19+; not on Demo 7 critical path
- Advanced geocoded dataset integration (#4) — deferred to M19+; not on Demo 7 critical path

---

**Demo:** None (M17). Demo 7 at M18.

**Canonical user primarily served:** Lucas Ferreira (Programme Analyst, Persona 1) and Aicha Mbaye (Finance Minister, Persona 5) — Wave 1 satisfies Lucas's calibration credibility requirement; Wave 2 enables the Mode 3 interrogation and multi-scenario comparison that Aicha's team needs at the table.

**What M17 does not do:** M17 does not run the live external demo (M18). M17 does not deliver CI bands on Zone 1A trajectories — that is ADR-007 scope requiring a separate architecture decision (M18). M17 does not deliver PSP driver decomposition (M18). M17 does not deliver entity templates, data marketplace, or geocoded dataset expansion (M19+).

---

### Milestone 18 — Full Argument and Demo 7 *(planned)*

**Core deliverable:** The complete analytical stack at the negotiating table. A finance ministry team can interrogate whether any available instrument prevents a human cost threshold crossing (Mode 3, Act 1), and can load three scenarios and show distributional differences under each pathway with confidence bands (Act 2). Demo 7 is the live external session that delivers both arguments to real participants.

**Demo 7 story:** *"Here is what we proposed instead — and here is what the conditionality structure does to this cohort under every version of the programme."*

**What ships:**

*Mode 3 interrogation capability for Demo 7 Act 1:*
- Mode 3 instrument search on Demo 6 scenario — M17 calibration is the prerequisite; M18 delivers the demo-ready configuration and the presenter narration for both possible outcomes ("counter-proposal found" and "conditionality structure is the binding constraint")
- The Demo 7 Act 1 argument does not require new engine features — Mode 3 was delivered in M12; M18 delivers the calibrated scenario and narrated demo sequence

*Multi-scenario comparative analysis for Demo 7 Act 2:*
- Multi-scenario comparison with distributional overlay — three+ scenarios, overlaid trajectories with uncertainty bands → builds on M17 Issue #394 infrastructure
- Counter-scenario comparison showing distributional differences under each pathway — the specific number differential (e.g., 340,000 vs. 80,000 people below the poverty threshold) with confidence bands
- Zone 1A CI bands — scenario-band rendering on trajectory curves; ADR-007 scope; architecture decision required before implementation → Issue #1254 (horizon:near-term; DEMO6-015)

*PSP analytical depth for Demo 7:*
- PSP driver decomposition in Zone 1D — dominant signal category visible alongside severity label; enables Andreas's direct political brief without economist mediation → Issue #1255 (horizon:near-term; DEMO6-036)

*Live external session:*
- Demo 7 — live stakeholder session with real external participants; both acts (Senegal Mode 3 + Zambia comparison); M18 exit gate → Issue #843

*Path 2 (capacity-allowing):*
- Path 2 full implementation — ministry-owned proprietary data integrated into multi-scenario comparison; carries from M16 design groundwork → Issue #1256 (horizon:near-term; capacity-allowing)

*Deferred to M19+:*
- Entity template library operational (#407) — not required for Demo 7; deferred
- Data marketplace design (#5) — deferred
- Advanced geocoded dataset integration (#4) — deferred

**Demo:** Demo 7 at M18 close. Two-act live session: Senegal Article IV (Mode 3 interrogation) + Zambia restructuring (three-scenario comparison). The ministry team has negotiating parity.

**Canonical user primarily served:** Persona 5 (Aicha Mbaye, Finance Minister) in Act 1 — the counter-proposal interrogation is her instrument; Persona 2 (Eleni Papadimitriou, Finance Ministry Negotiator) in Act 2 — the distributional comparison with number differentials is what she cites at the table.

**What M18 does not do:** M18 does not deliver entity templates, data marketplace, or geocoded dataset expansion (M19+). M18 does not guarantee Path 2 delivery — that is capacity-allowing, not exit-gating.

---

### Milestone 19 — Constraint Search and Empirical Calibration *(complete)*

**Core deliverable:** The constraint-floor capability and empirically calibrated confidence intervals. The ministry analyst can now ask "what configurations avoid the human cost floor?" rather than testing one at a time. Confidence intervals are grounded in empirical backtesting (Bayesian posterior across ten real-world cases), not just the structural schedule.

**Demo 8 story:** *"The instrument found the boundary — and here is what the numbers say, tested against real outcomes."*

**What ships:**

*Mode 3 constraint-floor search (Act 1):*
- Constraint-floor search capability — instrument finds configurations that avoid a human cost threshold; reverses the Mode 3 query from "is this safe?" to "what configurations are safe?" → Issue #1540 (horizon:immediate) ✅ G1 delivered
- Focal cohort floor Pydantic validation → Issue #1538 (horizon:immediate) ✅ Pre-wave delivered
- scenarioId guard Zone 1B crash fix → Issue #1456 (horizon:immediate)

*Headless battle-testing and empirical calibration (evidence base for Acts 1 and 2):*
- Headless battle-testing harness (Type A/B, configurable output) → Issue #1546 (horizon:immediate) ✅ G2A delivered
- SEN backtesting fixture → Issue #1541 (horizon:immediate) ✅ G2B delivered
- ZMB backtesting fixture → Issue #1542 (horizon:immediate) ✅ G2B delivered
- Greece 2010–15 primary surplus counter-factual (Type B) → Issue #1547 (horizon:immediate) ✅ G2C delivered
- Argentina 2001 peg-abandonment counter-factual (Type B) → Issue #1548 (horizon:immediate) ✅ G2C delivered
- Sri Lanka 2022–23 Coffin Corner (Type A+B) → Issue #1549 (horizon:immediate) ✅ G2C delivered
- Pakistan 2022–23 programme survival (Type B) → Issue #1550 (horizon:immediate) ✅ G2C delivered
- Turkey 2018–19 rate-cut counter-factual (Type B) → Issue #1551 (horizon:immediate) ✅ G2C delivered
- Egypt 2016 devaluation/subsidy reform (Type B) → Issue #1552 (horizon:immediate) ✅ G2C delivered
- Ghana 2022–23 IMF programme (Type A+B) → Issue #1554 (horizon:immediate) ✅ G2C delivered
- Iceland 2008–11 orthodox vs heterodox pre-calibration structural test (Type A+B) → Issue #1553 (horizon:immediate) — G2D active
- Capital controls transmission gap (ExternalSectorModule + MacroeconomicModule channels) → Issue #1532 (horizon:immediate) — G2D active

*Empirically grounded CI intervals (Act 2 confidence bounds):*
- ADR-007 Bayesian posterior layer → Issue #1543 (horizon:immediate) ✅ G3 delivered
- ADR-007 meaninglessness threshold → Issue #1536 (horizon:immediate) ✅ G3 delivered
- BandResult visible fields (is_pre_calibration, clipped_lower/upper) → Issue #1537 (horizon:immediate) ✅ G3 delivered

*PSP analytical depth and CI label polish (Act 2 instrument quality):*
- PSP driver arc across programme window + in-viewport auditability panel (DEMO-165) → Issue #1528 (horizon:immediate) — G4 active
- '95% CI' label precision fix → Issue #1529 (horizon:immediate) — G4 active

*ELASTICITY_REGISTRY empirical calibration — non-SSA entity families (CM parallel track):*
- CM Sprint A: Euro area programme countries (GRC, PRT, IRL, CYP) — Ilzetzki et al. (2013) fiscal multiplier for open economies with fixed exchange rates; GDP-to-unemployment elasticity from OECD Southern European labour market studies; priority: GRC for Greece 2010 counter-factual MAGNITUDE fidelity → Issue #1623 (horizon:immediate; M19 priority)
- CM Sprint B: Latin American emerging markets (ARG, ECU, BOL, PER) — Ilzetzki et al. (2013) Latin American multiplier range; Céspedes & Velasco (2012) commodity price-to-fiscal transmission; priority: ARG for Argentina 2001 counter-factual MAGNITUDE fidelity → Issue #1623 (horizon:immediate; lower priority than Sprint A)
- CM Sprint C: South and Southeast Asian programme countries (PAK, LKA, BGD) — IMF Asia-Pacific Regional Economic Outlook multiplier estimates; Batini et al. (2012) or equivalent; priority: PAK and LKA for 2022–23 live application cases → Issue #1623 (horizon:immediate; lower priority than Sprint A)

*Demo 8 display and presentation quality (Wave 3 / G5 — after G4):*
- Zone 1A ZMB y-axis tight-scoping — `CompositeChartSVG.computeYDomain` fix; three scenario curves currently collapse when data spread ≤ 0.05; Demo 8 Act 2 display risk → Issue #1629 (horizon:immediate)
- Demo 8 narration / Mode 3 HD line alignment — narration implies separately visible HD line in Zone 1A that does not exist; fix is narration correction or per-framework lines (EL decision determines scope) → Issue #1630 (horizon:immediate; separate sprint entry G5)

*Zone 1A instrument quality (Wave 3+ — after G5):*
- View model layer retrofit — extract composition logic from Zone 1 instrument components → Issue #1522 (horizon:immediate)
- Zone 1A TrajectoryView interaction layer — pinch-zoom, thumbwheel zoom, and pan on trajectory plot → Issue #1524 (horizon:immediate)

*Live external session:*
- Demo 8 — live stakeholder session → Issue #1544 (milestone exit gate)

**Demo:** Demo 8 at M19 close. Two-act structure: Act 1 (constraint-floor search — instrument finds the boundary rather than testing one configuration at a time), Act 2 (Zambia three-scenario comparison with CI bounds grounded in empirical backtesting across ten real-world cases).

**Canonical user primarily served:** Persona 5 (Aicha Mbaye, Finance Minister) — Act 1 reverses her analytical task: the boundary comes to her, not the other way around. The Greece 2010 counter-factual (CM Sprint A) directly models the scenario type her counterpart at the IMF negotiating table is most familiar with, raising the credibility floor for all MAGNITUDE-fidelity claims. Persona 2 (Eleni Papadimitriou, Finance Ministry Negotiator) — Act 2 CI bounds are now defensible against "how reliable is this interval?" because they are grounded in fidelity across ten real-world fiscal outcomes.

**What M19 does not do:** M19 does not add entity templates, data marketplace, or geocoded dataset expansion. CM Sprint B (Latin America) and Sprint C (South Asia) were milestoned as M19-conditional — both delivered. The Zone 1A interaction layer (#1522, #1524) was milestoned as M19-conditional — delivered. Live interactive constraint-floor search (real-time boundary update on floor adjustment) was not in scope — M20.

---

### Milestone 20 — Analytical Evidence Portfolio and Demo 9 *(current)*

**Core deliverable:** WorldSim Analytical Evidence Portfolio (AEP) — 11 entries across all four registered calibration families, documenting what the engine actually produces, under what calibration conditions, with what fidelity tier. The evidence infrastructure (TEMPLATE.md, analytical-framework.md, coverage-audit.md) was established at M19 close / M20 kickoff; M20 builds the portfolio itself.

**Demo 9 story:** *"The Zambian finance ministry analyst pulls up AEP-004. The engine found consistent downward direction on human development from the copper crash step onward — the same pattern as Senegal's structural adjustment period (AEP-005). The directional ordering is valid; magnitude comparison is not — the framework says why. She then runs her own scenario and sees where it sits relative to the documented cases."*

**What ships:**

*Analytical Evidence Portfolio (primary):*
- M20-G1 (EURO-AREA family): AEP-001 GRC 2010 Type A, AEP-002 GRC 2010 Type B counter-factual, AEP-003 ISL 2008 heterodox vs orthodox
- M20-G2 (SSA-LIC + LATAM-EM): AEP-004 ZMB 2005, AEP-005 SEN 2000, AEP-006 GHA 2022, AEP-007 ARG 2001 (A+B), AEP-008 ARG 2003 Kirchner recovery, AEP-009 ECU 1999
- M20-G3 (SOUTH-SE-ASIAN + gap issues): AEP-010 LKA 2022, AEP-011 PAK 2022 (A+B); gap closure issues filed (PRT fixture, BGD fixture, remittance channel)

*Instrument polish (maintenance):*
- M20-G4: DEMO-217 (in-viewport navigation link), DEMO-233/#1775 (WARNING alongside CLEAR), DEMO-234/#1776 (precision vs CI label), #1759/NM-099 (asgi_client fix)

*Live external session:*
- Demo 9 — live stakeholder session → M20 exit gate

**Demo:** Demo 9 at M20 close.

**Canonical user primarily served:** Persona 2 (Kaveh Jafari, Finance Ministry Analyst) — the AEP gives him a citable, quality-tiered analytical record that he can present to his minister and to the IMF negotiating team.

**What M20 does not do:** Live interactive constraint-floor search deferred to M21 — it requires a full sprint to implement correctly and should not compress the AEP work. DEMO-235 (PSP multi-scenario comparison) deferred to M21. No new calibration families or entity templates in M20 — gap closure issues are filed but implementation is M21+.

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
