# WorldSim Roadmap

> Last significant revision: 2026-05-30
> Next mandatory review: Milestone 10 close
> Updated against: M10 kickoff gate — Argentina 2000–2002 confirmed as second country fixture; Phase 1 benchmarks moved to M10 per NM-020; GovernanceModule #556 filed; scope linkage issue numbers added; #221 conflict flagged pending EL decision
> Canonical location: `docs/roadmap/worldsim-roadmap.md`

*This document is directionally committed, not contractually precise. When scope changes materially, this document is updated with a dated rationale note — not silently overwritten. The change history is the accountability mechanism.*

---

## Where We Are

WorldSim v0.8.0 is released. Eight milestones of foundational work are complete: the simulation engine, the data architecture, the backtesting infrastructure, the four-framework measurement system (financial, human development, ecological, governance), the Greece 2010–2015 and Argentina 2001–2002 backtesting fixtures, the multi-agent development team, the governance and compliance framework, and the UX design foundation.

The tool is not yet ready for consequential use. The instrument cluster is being redesigned. The governance module is in validation. The simulation runs one country at a time. The canonical users have been formally defined but the tool has not yet been evaluated against their real-world use cases.

Milestone 9 is the transition from foundational infrastructure to a tool that looks right, works across all four frameworks, and has been evaluated against the historical cases that define its value proposition.

---

## The Demo Arc

WorldSim follows a two-milestone demo cadence. Each demo tells one coherent story. Stakeholders are not asked to absorb a progress report — they are shown what the tool is at that moment.

**Demo 3 — Milestone 10: WorldSim works.**

The instrument cluster is redesigned. All four measurement framework axes are live with real data. The simulation runs a second country beyond Greece. The tool looks right, works across frameworks, and is credible as an analytical instrument.

A finance ministry analyst can open WorldSim, load the Greece 2010–2015 scenario, and see — without opening a drawer, without navigating away from the primary screen — where the human cost thresholds were crossed, which framework deteriorated first, and how the trajectory across all four dimensions simultaneously diverges from the financial recovery narrative.

**Demo 4 — Milestone 12: WorldSim serves its users.**

The matrix computation engine is in production. The simulation runs multi-country scenarios at scale. A Jordanian finance ministry analyst runs a Strait of Hormuz closure scenario and sees what it means for Jordan's fuel access, food price inflation, and public legitimacy — on a standard laptop, in real time.

The story is the democratization mission made concrete. The tool that showed Greece in Demo 3 now serves the user it was built for — in a scenario no institution has previously given them the analytical tools to navigate.

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

### Milestone 9 — Standards Foundation *(current)*

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
- Mean-reversion channel → Issue #221 [**EL DECISION PENDING** — roadmap previously stated "hard constraint, cannot be deferred past M10"; issue moved to M11 per 2026-05-30 board split; EL must either re-milestone #221 to M10 or confirm M11 deferral and remove this constraint]
- Phase 1 baseline benchmarks — iterative engine on target hardware (4-core/8GB laptop AND GitHub Actions free-tier runner) → Issue #514 (horizon:immediate) [moved from M11 to M10 per NM-020, 2026-05-25; prerequisite for ADR-009 authoring in M11; Chief Engineer activation required]
- step_event_label mandatory field on all Mode 1 fixtures → Issue #395 (horizon:immediate)
- Playwright demo advancement test and legibility assertions → Issues #376, #377 (horizon:immediate)
- Confidence tier standards (SA-02) — prerequisite for M11 uncertainty quantification → Issue #43 (horizon:immediate)

**Demo:** Demo 3 at M10 close. All four frameworks live. Second country live. Instrument cluster redesigned.

**Canonical user primarily served:** Aicha Mbaye (Institutional Decision-Maker) in Demonstrative entry state — the M10 demo is the first time WorldSim is shown in its complete form.

**What M10 does not do:** M10 does not introduce the matrix computation engine. No matrix code ships in M10. M10 does not model political economy constraints on programme design — that is M11 scope.

---

### Milestone 11 — Engine Investigation and Political Economy *(no demo)*

**Core deliverable:** A complete empirical understanding of the simulation engine's performance characteristics, a proof-of-concept matrix engine running in parallel with the iterative engine, and the political economy module that serves the Argentina and Ukraine/Pakistan marquee cases.

**What ships:**

*Matrix engine investigation (Chief Engineer owned):*
- Phase 1 baseline benchmarks — [moved to M10, Issue #514 (horizon:immediate), per NM-020 2026-05-25; ADR-009 authoring depends on M10 benchmark results before matrix investigation begins]
- ADR-009 authored and accepted — after Phase 1 results, before any matrix code written
- Sparse matrix proof-of-concept — matrix engine running alongside iterative engine. Not a replacement.
- Phase 2 A/B validation — output equivalence to Decimal precision, performance comparison on identical hardware, full backtesting suite passing identically on both engines
- Matrix interpretability tooling — contribution tracing, transformation visualization, computation anomaly detection (separate alert channel from MDA threshold system)
- Phase 3 stress test suite — load levels 1x through 1000x on target hardware. Permanent test infrastructure artifact.

*Political economy module:*
- Political feasibility constraints as scenario inputs
- Conditionality modelling — IMF terms as structured scenario inputs
- Elite capture dynamics
- Coalition stability as a simulation state variable

**Demo:** None. M11 is the investigation milestone. ADR-009 is the most consequential architectural decision the project will make — it deserves a milestone without a demo clock running.

**Canonical user primarily served:** The Chief Engineer and Architect Agent — M11 is primarily an internal architectural milestone whose outputs enable M12.

**What M11 does not do:** M11 does not migrate the production engine. The iterative engine remains in production at M11 close. The matrix engine is a validated proof-of-concept, not a replacement. Production migration is M12.

---

### Milestone 12 — Transformation and External Sector

**Core deliverable:** The matrix computation engine in production, the external sector module enabling multi-country trade and geopolitical scenarios, and the democratization use case made concrete for a global south finance ministry analyst.

**What ships:**

*Matrix engine migration:*
- Production migration — iterative engine retired after Phase 2 equivalence confirmed across full backtesting suite
- Cloud compute path scoped — infrastructure design documented, pricing model proposed for high-resolution institutional use cases

*External sector module:*
- Bilateral trade shock as standard scheduled input type — enables Canadian steel tariff scenarios and similar trade policy cases
- Commodity price shock as global parameter propagating through relationship graph — enables Hormuz closure, multi-country cascade scenarios
- Multi-scenario comparison lifted beyond two-scenario limit — enables Kenya budget planning with three competing proposals

*Mode 3 active control:*
- Policy instrument inputs with live trajectory response and automatic A/B comparison
- Multi-country scenario configuration

**Demo:** Demo 4 at M12 close. A Jordanian finance ministry analyst runs a Strait of Hormuz closure scenario on a standard laptop. The democratization mission made concrete.

**Canonical user primarily served:** Persona 2 (Finance Ministry Negotiator) in Mode 3 active control — in a global south context rather than European.

**What M12 does not do:** M12 does not introduce the entity template library. Transport fuel, food system, and electricity templates are M13+ scope.

---

### Milestone 13 — Methodology Publication and Public Launch

**Core deliverable:** WorldSim is ready for institutional adoption. The methodology is published, externally validated, and inspectable by anyone.

**What ships:**
- Methodology publication — complete documentation of every model relationship, calibration assumption, and known limitation
- External validation — methodology reviewed by domain experts outside the project
- Technical Steering Committee formation — first governance actor independent of the Engineering Lead
- Goodhart's Law mitigation design — TSC owns the monitoring and response framework for parameterization gaming risk
- Public launch infrastructure — onboarding path for global south finance ministry analysts, accessibility validation on target hardware

**Demo:** Public launch event. The audience shifts from invited stakeholders to the world.

**Canonical user primarily served:** All five personas — anchored in the quinoa farmer's government. The tool's public availability is the moment the democratization mission becomes operational rather than aspirational.

**What M13 does not do:** M13 does not complete the entity template library. That work begins at M13 and continues beyond it as a permanent capability improvement program.

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
