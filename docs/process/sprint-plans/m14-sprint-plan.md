---
name: m14-sprint-plan
type: sprint-plan
milestone: M14 — Methodology Publication and External Validation
status: Draft — awaiting EL approval before any implementation PR opens
authored-by: PM Agent
authored-date: 2026-06-16
el-approved: pending
consulted-agents:
  - Business Product Owner (value prioritization and Demo 5 scope)
  - Frontend Architect (component grouping and merge conflict assessment)
  - Chief Engineer (backend dependency sequencing)
  - Architect (ADR prerequisites and wave sequencing)
sop-reference: docs/process/sprint-planning-sop.md
---

# M14 Sprint Plan — Methodology Publication and External Validation

**Status:** Draft — awaiting EL approval before any implementation PR opens
**Release branch:** `release/m14` (cut from `main` 2026-06-16)
**Exit checklist issue:** TBD (filed as part of this kickoff sequence)
**Primary objective:** Methodology publication, external validation by domain experts, live stakeholder demo with real external participants (#843), Technical Steering Committee formation.

**M14 exit gate:** Issue #843 — live stakeholder demo with real external participants. M14 closes when the methodology is published, externally validated, and Demo 5 has been delivered to real external participants.

**Wave structure (EL decision 2026-06-15):**
- **Wave 1 — COMPLETE:** ADR-016 (Scenario Grounding Architecture) authored and Accepted (2026-06-16, PR #967)
- **Wave 2:** ADR-015 (Evidence Thread Architecture) — EL acceptance followed by implementation

---

## Four-Agent Consultation Summary

Before grouping, PM Agent ran four consultations per `docs/process/sprint-planning-sop.md`.

**Business Product Owner (value prioritization):**
The Demo 5 north star (Zambian finance ministry analyst responding to an input challenge at the table) requires two things to be on screen: (1) a source-cited initial state via the Grounding strip (ADR-016), and (2) the ability to create a Zambia scenario from the creation form. Without both, Demo 5 cannot run the north star scenario. The prerequisite bugs (#961 entity hardcoding, #962 step counter, #963 choropleth labels) are the highest-value first items — small scope, high Demo 5 impact. ADR-016 backend and frontend implementation follow, then ADR-015. Methodology items (#22, #884, #885) are methodology publication anchors — they must ship for M14's stated objective, but they are not Demo 5 blockers if the demonstration is structured to show a completed scenario rather than create one in real time.

ADR-015 (Evidence Thread Architecture) is the second half of the trust architecture. It is a Demo 5 enhancer — without it, the minister can verify inputs but cannot traverse output reasoning. The Business PO recommends ADR-015 be accepted by EL and implemented in M14 scope, but acknowledges it can be deferred to M15 if M14 timeline is under pressure. ADR-016 implementation is the Demo 5 minimum; ADR-015 is Demo 5 enriched.

**Frontend Architect (component grouping):**
The three prerequisite bugs (#961, #962, #963) are independent of each other and of ADR-016 frontend implementation — no merge conflict risk between them. Bundle them as a single G1 PR for efficiency.

ADR-016 frontend (entity selector, data quality preview, grounding strip, parameter persistence, IC-6 and IC-4 M14 mitigations) all touch the scenario creation form and the Zone 0/Zone 2 surface area. They should be implemented as one G4 PR to avoid sequential conflicts in `ScenarioCreationPanel.tsx` and the Zone 0 identity strip area. The Grounding strip is a new component and has no existing conflict surface.

ADR-015 frontend (L0 annotations, L1 basis surface, L2 evidence chain) touches Zone 1 instruments — the trajectory view and the MDA alert panel. These are separate component trees from ADR-016's surfaces. No merge conflict with G4 if G4 merges first.

**Chief Engineer (backend dependency sequencing):**
ADR-016 backend requires two new endpoints: `/api/v1/entities/{entity_id}/data-quality` and `/api/v1/scenarios/{scenario_id}/initial-state`. The Data Architect Agent must update `api_contracts.yml` before implementation begins (RACI: DA holds R on that file). The source registry must have entries for GRC, JOR, EGY, ZMB before the data quality preview can return real data. Source registry population is a backend pre-work step, not a feature — assess at sprint entry time whether GRC and JOR/EGY registry entries exist from existing calibration work.

ADR-015 backend has no new endpoint requirements per the current ADR-015 spec — it surfaces existing measurement output data through a new UI layer, relying on existing API endpoints. Chief Engineer confirms no backend sequencing dependency between ADR-016 and ADR-015 backend implementation.

**Architect (ADR prerequisites and wave gate):**
Wave 1 is complete: ADR-016 Accepted 2026-06-16 (PR #967). Wave 2 gate: EL must accept ADR-015 (currently Proposed, PR #959 merged to main 2026-06-15). No new ADR is required for any G1–G4 scope item. ADR-015 acceptance is a documentation action — EL reviews the Proposed ADR, records acceptance (including the six pre-implementation decisions in §Decisions Required), and a PR commits the status change. The same pattern used for ADR-016.

---

## HORIZON Sweep — M14 Scope Completeness

Run against `CLAUDE.md §Milestone 14` and `docs/roadmap/worldsim-roadmap.md §Milestone 14`.

| Roadmap deliverable | Issue | Status |
|---|---|---|
| Methodology publication — complete documentation of every model relationship | #22 (disclosure layer: confidence tier visible per indicator) | Tracked — G6. Note: full distributional bands → M16. |
| External validation by domain experts | #843 (Demo 5) | Tracked — G8 (M14 closure gate) |
| Live stakeholder demo with real external participants | #843 | Tracked — G8 (M14 closure gate) |
| Technical Steering Committee formation | #3, #6 | Tracked — G7 |
| Goodhart's Law mitigation design | #988 | Tracked — G7 (filed 2026-06-16) |
| Onboarding documentation for global south analysts | #989 | Tracked — G7 (filed 2026-06-16) |
| ADR-016 (Scenario Grounding Architecture) | ARCH-010 | ✅ COMPLETE — Accepted 2026-06-16 |
| ADR-015 (Evidence Thread Architecture) | ARCH-009 | Pending EL acceptance — Wave 2 gate |
| Entity selector (IC-1) | #961 | Tracked — G1 |
| Step counter fix (IC display) | #962 | Tracked — G1 |
| Choropleth field name labels (IC-7 related) | #963 | Tracked — G1 |
| reserve_coverage_months surfaced | #884 | Tracked — G6 |
| Exploratory tier misclassification | #885 | Tracked — G6 |
| Ecological composite fix | #823 | Tracked — G6 |
| MENA calibration | #824 | Tracked — G6 |
| Zone 1A Y axis label | #950 | Tracked — G6 |
| Zone 1A Phase 1 design thinking | #845 | Tracked — G6c (design-only; Phases 2–4 in M15/M16) |
| Path 2 design groundwork | #976 (design only) | Tracked — G6b (implementation → M16) |

**Issue disposition — confirmed 2026-06-16 (panel deliberation + EL milestone planning):**

| Issue | Title | Disposition |
|---|---|---|
| #53 | Information access architecture | → M15 ✅ moved |
| #845 | Zone 1A information architecture | Phase 1 (design thinking doc) stays M14 (G6c); Phases 2–4 → M15/M16 |
| #846 | DEMO-045 Mode 3 branch comparison | → M15 ✅ moved |
| #951 | Solo-use review protocol | → M15 ✅ moved |
| #35 | Dynamic relationship weights | → M16 ✅ moved |
| #102 | Distributional comparison | → M16 ✅ moved |
| #274 | 25-year trajectory | → M16 ✅ moved |
| #394 | Multi-scenario >2 | → M17 ✅ moved |
| #837 | Config-driven demo scripts | → M15 ✅ moved |
| #97 | Threshold-crossing markers | → M15 ✅ moved |
| #153 | Absolute threshold overlay | → M15 ✅ moved |
| #92 | Greece backtesting expansion | → M15 ✅ moved |
| #30 | Stock vs. flow variables | → M16 ✅ moved |
| #259 | CTO legibility metrics | → M15 ✅ moved |
| #275 | Ecological-to-financial transmission | → M16 ✅ moved |
| #569 | Mode 3 hardware validation | → M15 ✅ moved |
| #975 | Path 1 approved source query | → M15 ✅ moved |
| #976 | Path 2 proprietary data upload | → M16 ✅ moved (G6b design artifacts remain M14) |
| #988 | Goodhart's Law mitigation | → M14 ✅ filed (G7) |
| #989 | Onboarding documentation | → M14 ✅ filed (G7) |
| #990 | Accessibility validation on target hardware | → M15 ✅ filed |
| #986 | Cohort disaggregation on primary surface | → M15 ✅ filed |
| #987 | Political risk summary surface (Persona 3) | → M15 ✅ filed |

---

## Sprint Groups

| Group | Issues | ADR gate | Wave | Description |
|---|---|---|---|---|
| G1 — Prerequisite bugs | #961, #962, #963 | None | Pre-Wave | Entity selector form fix, step counter, choropleth labels. Single PR. Low-risk, high Demo 5 impact. |
| G2 — ADR-015 acceptance | — | ADR-015 EL review | Wave 2 gate | EL records acceptance of ADR-015 (same pattern as ADR-016). Six pre-implementation decisions in §Decisions Required. EL-action; PM Agent files the acceptance PR. |
| G3 — ADR-016 backend | — | ADR-016 ✅ | Wave 2 | Source registry population (GRC/JOR/EGY/ZMB), `/data-quality` endpoint, `/initial-state` endpoint. Data Architect updates `api_contracts.yml`. Chief Engineer implements. |
| G4 — ADR-016 frontend | — | ADR-016 ✅; G3 partial (API must exist) | Wave 2 | Entity selector + data quality preview (Component 1), Grounding strip (Component 2), parameter persistence (Component 4), choropleth header label (IC-6 mitigation), Fidelity static header (IC-4 M14 mitigation). |
| G5 — ADR-015 implementation | — | ADR-015 Accepted (G2); sprint entry required | Wave 2 | Evidence Thread Architecture: L0 basis annotations, L1 basis statement surface, L2 evidence chain. Gated on G2. |
| G6 — Methodology and calibration | #22, #884, #885, #823, #824, #950 | None | Parallel | Uncertainty quantification, reserve_coverage_months, Exploratory tier fix, ecological composite, MENA calibration, Y axis label. Can proceed in parallel with G3/G4. |
| G7 — Governance | #3, #6, #988, #989 | None | Parallel | TSC formation (#3), branch protection restoration (#6), Goodhart's Law mitigation framework (#988), onboarding documentation for global south analysts (#989). EL-action items for #3/#6/#988; PM Agent leads #989. |
| G6b — Path 2 design groundwork | #976 | None | Parallel | Design-only (no code). Three artifacts: (1) field mapping UX concept for the 5-minute Preparatory ceiling — UX Designer Agent; (2) `USER_SUPPLIED` provenance type specification as a draft ADR-016 amendment — Architect Agent; (3) data isolation model sketch that Issue #53 must satisfy — Data Architect Agent. No sprint entry document required (no implementation). Artifacts filed in `docs/design/path2-data-upload/` before M14 exit. Unblocks M15 Path 2 design-to-implementation transition. Authority: Customer Agent recommendation 2026-06-16. Note: #976 moved to M16 milestone (implementation); G6b design artifacts remain M14 deliverables. |
| G6c — Zone 1A Phase 1 design thinking | #845 | None | Parallel | Design-only (no code). UX Designer Agent authors a design thinking document at `docs/ux/design-thinking/zone-1a-information-architecture.md` specifying Zone 1A's primary cognitive task as a Persona 2 question answerable within the mode's time ceiling, for each of Mode 1, Mode 2, and Mode 3. Must address the combinatorial tension: what information does the analyst need per mode, and what lives elsewhere (Zone 1B, Zone 1D, a comparative view)? No sprint entry required. Document gates Phase 2 (Architecture Review) in M15. Must exist before M14 exit. Phases 2–4 of #845 are M15/M16 scope. Authority: EL directive 2026-06-16. |
| G7 — Governance | #3, #6, #988, #989 | None | Parallel | TSC formation (#3), branch protection restoration (#6), Goodhart's Law mitigation framework (#988), onboarding documentation for global south analysts (#989). EL-action items for #3/#6/#988; PM Agent leads #989. |
| G8 — Demo 5 (#843) | #843 | All preceding groups | Exit gate | Methodology publication artifact, external validator engagement, live stakeholder demo with real external participants, stakeholder review artifact (`docs/demo/m14/reviews/`). M14 closure gate. |

---

## Sprint Sequencing

```
G1 (bugs) ──────────────────────────────────────────────────────┐
                                                                  │
G2 (ADR-015 acceptance) ──► G5 (ADR-015 implementation) ────────┤
                                                                  ├──► G8 (Demo 5 — M14 exit)
G3 (ADR-016 backend) ──► G4 (ADR-016 frontend) ─────────────────┤
                                                                  │
G6 (methodology / calibration) ─────────────────────────────────┤
                                                                  │
G6b (Path 2 design groundwork — design only, no code) ──────────┤
                                                                  │
G6c (Zone 1A Phase 1 design thinking — design only, no code) ───┤
                                                                  │
G7 (governance + onboarding docs) ──────────────────────────────┘
```

No sequential dependency between G1, G2, G3, G6, G6b, G6c, G7 — these can proceed in parallel after EL approval of this sprint plan. G4 is gated on G3 (API endpoints must exist). G5 is gated on G2 (ADR-015 must be Accepted). G6b and G6c produce design artifacts only — no sprint entry document required, no implementation PR opens for either.

---

## Sprint Entry Gate Requirements

Per `docs/process/sprint-planning-sop.md §Sprint Entry Gate`, implementation may not begin on any sprint group until:

1. This sprint plan is EL-approved (record approval as PR comment or commit to this document)
2. A sprint entry document is filed at `docs/process/sprint-plans/m14-{group}-sprint-entry.md` per the template at `docs/process/sprint-plans/templates/sprint-entry-template.md`
3. The entry document is committed and referenced in `SESSION_STATE.md`

G1 (prerequisite bugs) is the lowest-risk group and may proceed with a lightweight sprint entry referencing this plan. G3 and G4 require a full entry document that derives acceptance criteria from ADR-016's observable application states and intent template. G5 requires a full entry document derived from ADR-015's acceptance criteria — filed only after G2 (ADR-015 Accepted).

---

## Exit Conditions

M14 closes when all of the following are satisfied:

1. **Business PO acceptance** recorded for all user-facing G-group deliverables (G1, G3/G4, G5, G6)
2. **Customer Agent Layer 3 assessment** on record for any capability serving Personas 2, 3, or 5
3. **North star test artifact** filed: a Zambian finance ministry analyst (or equivalent Demo 5 scenario) can respond to an input challenge with a source citation from the Grounding strip within 90 seconds
4. **Demo 5 delivered** (#843): live stakeholder demo with real external participants; stakeholder review artifact filed at `docs/demo/m14/reviews/YYYY-MM-DD-vX.X.X-stakeholder-review.md`
5. **PI Agent exit gate confirmation** recorded in the M14 sprint exit document

CI green and issue closure are necessary but not sufficient.

---

*M14 sprint plan authored by PM Agent 2026-06-16. Release branch `release/m14` cut from `main` 2026-06-16. EL approval required before any implementation PR opens against `release/m14`.*
