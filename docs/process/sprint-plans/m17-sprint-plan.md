---
name: m17-sprint-plan
type: sprint-plan
milestone: M17 — Calibration and Comparative Infrastructure
status: Pending EL Approval
authored-by: PM Agent
authored-date: 2026-06-25
amended: 2026-06-25 — issue audit complete; G2 restructured to put UX/Design Thinking/Customer Agent upstream of architecture per EL direction; six issues disposition-resolved; sprint plan v2
el-approved:
consulted-agents:
  - Chief Methodologist (Wave 1 calibration scope and uncertainty; exit gate specification)
  - Business Product Owner (Demo 7 value prioritization; scope cut order; #394 Demo 7 narrative)
  - Design Thinking Agent (multi-scenario cognitive task analysis; #394 use-case grounding)
  - UX Designer (multi-scenario experience journeys; zone layout for N>2; Mode 1/2/3 comparison model)
  - Customer Agent (multi-scenario persona assessment — Personas 1, 5; Demo 7 Act 2 minimum viable story)
  - Architect (ADR prerequisites; ARCH-REVIEW-007 N≤2 constraint — assessed only after UX design settled)
  - Frontend Architect (Wave 2 frontend sequencing; TrajectoryView N>2 conflict risk — downstream of UX)
sop-reference: docs/process/sprint-planning-sop.md
---

# M17 Sprint Plan — Calibration and Comparative Infrastructure

**Status:** Pending EL Approval — implementation may NOT begin until this plan is EL-approved and a sprint entry document is filed per group
**Release branch:** `release/m17` (cut from `main` at commit d806957, 2026-06-25)
**Exit checklist issue:** #982 (renamed 2026-06-25 — "M17 Exit Checklist — blocks milestone closure")
**Primary objective:** Make Demo 7 analytically defensible. Two-wave structure: Wave 1 (CM calibration sprint) is the hard prerequisite for Wave 2. Wave 2 is anchored by UX-grounded multi-scenario design (#394) and DEMO6 CRITICAL polish. No live demo at M17 close — Demo 7 is at M18.

**M17 exit gate:** PI Agent exit gate confirmation, with BPO acceptance for all Wave 2 user-facing deliverables and Customer Agent Layer 3 for Personas 1, 2, 3, 5. #982 closes last.

**M17 thesis:** The FRAME-D gap is not a demo polish problem — it is a calibration problem. The multi-scenario capability (#394) is not primarily an architecture problem — it is a user experience and use-case problem that architecture must serve. M17 resolves both in the correct sequence.

---

## Kickoff Prerequisites (Status at Sprint Plan Filing)

| Step | Status | Notes |
|---|---|---|
| 1. EL merges `release/m16` → `main` (admin bypass) | ✅ DONE 2026-06-25 | PR #1259 merged |
| 2. PM Agent cuts `release/m17` from `main` | ✅ DONE 2026-06-25 | `release/m17` cut at commit d806957 |
| 3. PM Agent authors `m17-sprint-plan.md` | ✅ THIS DOCUMENT | Filed 2026-06-25; EL approval pending |
| 4. EL approves sprint plan | ⬜ PENDING | Required before any sprint entry is filed |
| 5. #982 renamed "M17 Exit Checklist" | ✅ DONE 2026-06-25 | GitHub milestone 18 |
| 6. CI trigger verified | ✅ CLEAR | `.github/workflows/ci.yml` covers `release/m*` |

---

## HORIZON Scope-Completeness Check (Step 6)

Full open issue audit completed 2026-06-25. All open GitHub issues accounted for.

### Roadmap deliverables — linkage audit

| Roadmap deliverable | Issue | Wave | Status |
|---|---|---|---|
| Fiscal-to-cohort elasticity calibration — ELASTICITY_REGISTRY revision | #1229 | Wave 1 | ✅ Tracked; CM-owned; milestone corrected to M17 2026-06-25 |
| Governance sensitivity calibration — fiscal conditionality transmission | #1248 | Wave 1 | ✅ Tracked; CM-owned |
| Multi-scenario comparison (>2 scenarios) | #394 | Wave 2 | ✅ Tracked; design sprint first (see G2 below) |
| DEMO6-014: Zone 1A curve identifiability | #1249 | Wave 2 | ✅ Tracked; DEMO6 CRITICAL |
| DEMO6-026/043: Zone 1B tablet legibility (768px) | #1250 | Wave 2 | ✅ Tracked; DEMO6 CRITICAL |
| DEMO6-040: PSP historical precedent anchor in Zone 1D | #1253 | Wave 2 | ✅ Tracked; DEMO6 CRITICAL |
| Adaptive y-axis extension audit | #1251 | Wave 2 | ✅ Tracked |
| Zone 1B proportional allocation (ADR required) | #1252 | Wave 2 | ✅ Tracked; ADR gate |
| DEMO6-010: Zone 1B distance label semantically inverted | #1239 | Wave 2 | ✅ Tracked; UI bug; milestone assigned to M17 2026-06-25 |
| fix(e2e): G3 spec AC-F1–AC-F7 soft-skip — NM-061 upstream | #1220 | Wave 2 | ✅ Tracked; test infrastructure bug; milestone assigned to M17 2026-06-25 |
| observability: startup WARNING when simulation_entities empty | #1214 | Wave 2 | ✅ Tracked; NM-060 upstream; milestone assigned to M17 2026-06-25 |

**Deferred to M18 (not M17 scope):**

| Issue | Title | Disposition | Rationale |
|---|---|---|---|
| #843 | Demo 7 — live stakeholder demo | **M18** — milestone updated 2026-06-25; title corrected | Demo 7 requires Mode 3 (M18 north star); #843 is the live session tracking issue |
| #1238 | DEMO6-009 Frame A narration contradiction | **M18** — milestone updated 2026-06-25 | Demo script narration fix; Demo 7 prep work; no UI change required |
| #1059 | HCL narration into five-frame demo structure | **M18** — milestone updated 2026-06-25 | Demo 7 prep; filed from DEMO5-006; M18 pre-demo work |
| #1217 | Mode 3 render optimization | **M18** — milestone updated 2026-06-25 | Mode 3 is M18 north star; EX-001 exception provides coverage through Demo 7 (50.5ms MV-002 PASS) |
| #1254 | Zone 1A CI bands (ADR-007 scope) | **M18** — already assigned | Architecture decision required; #394 infrastructure is prerequisite |
| #1255 | PSP driver decomposition | **M18** — already assigned | Demo 7 capability; no M17 prerequisite work required |
| #1256 | Path 2 full implementation | **M18** — already assigned | AC-001 override scope; M19+ viable option |

**Closed at audit:**

| Issue | Title | Disposition |
|---|---|---|
| #1225 | Demo M16 stakeholder demo preparation | **CLOSED 2026-06-25** — all Steps 1–6c complete; live session tracked in #843 (now M18) |

**Parking Lot (no M17 action required):**

| Issue | Title | Note |
|---|---|---|
| #3 | Governance — single-principal separation of duties | Parking Lot milestone; trigger: second governance account |
| #6 | Governance — branch protection restoration | Parking Lot; dependent on #3 Stage 2 |
| #30 | Stock vs. flow variable distinction | Parking Lot; complexity addition |
| #35 | Dynamic relationship weight updating | Parking Lot; complexity addition |
| #214 | HealthBurdenModule — DALY framework | Long-horizon; no milestone |
| #278 | Technocratic class emigration research | Long-horizon; no milestone |
| #407 | Simulation resolution spectrum | Long-horizon; no milestone |

### ADR backlog review

| ARCH entry | Status | Action |
|---|---|---|
| ARCH-001 through ARCH-011 | All ACCEPTED or ASSIGNED | No action needed |
| #1252 Zone 1B proportional allocation | No ARCH entry | Architect determines at G3 sprint entry: ADR-017 amendment (ARCH-011 extension) or new ADR (ARCH-012). The temporary `minHeight: 80px` guarantee (PR #1235) must not be treated as accepted architecture. |
| #394 multi-scenario (N>2) | No ARCH entry; ARCH-REVIEW-007 constraint in scope | Architect assesses **only after** UX journeys and use stories are produced in G2 Phase 1. ARCH-REVIEW-007 §COMPARE_VIEW constraint is binding until revisited with design evidence. May trigger ARCH-012 or ARCH-013 depending on #1252 outcome. |

---

## Four-Agent Consultation Summary

### Chief Methodologist — Wave 1 calibration scope

Wave 1 is genuine research work with three possible outcomes. The CM must determine: (1) whether `fiscal_policy_spending_change` should have direct elasticity entries bypassing the GDP multiplier chain; (2) whether the GDP multiplier should be larger for social spending cuts specifically; (3) whether the current T3 calibration is accurate and the demo argument should remain structural rather than claiming step-level crossing precision. All three are valid conclusions — the Wave 1 exit is not contingent on a particular answer, only on a written, citable decision with updated ELASTICITY_REGISTRY constants.

Governance sensitivity (#1248): CM review must address whether institutional capacity degradation under austerity is captured in the governance composite, whether `imf_program_acceptance` has a direct governance transmission channel, and whether the 8-step quarterly window is sufficient to manifest governance divergence. A specification document is the required output; implementation may follow in Wave 2 if the timeframe extends. The specification does not block the Wave 1 fiscal calibration exit gate.

**Wave 1 exit gate (hard):** FRAME-D milestone sentence fires within the 8-step Demo 6 window on the Senegal Article IV scenario after the ELASTICITY_REGISTRY change. A backend integration test in CI asserts this within the CM-certified range. Governance sensitivity specification on record.

### Business Product Owner — Demo 7 value prioritization

M17's output is analytical credibility and demo-readiness — not capability additions per se. Wave 1 makes the fiscal-to-cohort argument defensible. Wave 2 makes the demo presentable. The scope cut order if capacity is constrained:

1. Never cut Wave 1 — the milestone premise is calibration
2. Never cut DEMO6 CRITICAL (#1249/#1250/#1253) — live demo legibility failures are disqualifying
3. Never cut #394 design sprint (G2 Phase 1) — without use-case grounding, architecture is speculative
4. Cut #394 implementation to M18 if design sprint reveals scope complexity — design in M17, build in M18
5. Cut #1252 (Zone 1B ADR) if capacity requires — `minHeight: 80px` holds through Demo 7
6. Cut #1251 (y-axis audit) if needed — no demo dependency

**On #394 and Demo 7:** The Zambia three-scenario comparison is Demo 7 Act 2. The Design Thinking and UX phase must ask: what is the minimum viable three-scenario story that Aicha (Persona 5) can read without narration? Not "what features does comparison need" but "what does the analyst need to be able to argue at the table?" That question comes before any architecture discussion.

### Design Thinking Agent — Multi-scenario cognitive task analysis

Multi-scenario comparison is fundamentally different from single-scenario analysis. In Mode 1 (Replay), the user reconstructs what happened — one country, one trajectory. In Mode 2 (Simulation), the user constructs a threshold-safe path — one scenario, steering. In Mode 3 (Active Control), the user branches and compares — this is where multi-scenario comparison is most analytically alive. But #394 must also serve Mode 1 and Mode 2 use cases.

The cognitive task for Demo 7 Act 2 (Zambia restructuring, three scenarios): the analyst has three restructuring options from creditor negotiations. They need to answer — at the table, without the presenter's narration — which option keeps Q1 poverty headcount above the recovery floor for the longest window? Which option produces the worst governance degradation? Which option crosses any MDA floor?

This is a comparison of threshold-crossing profiles, not trajectory aesthetics. The minimum viable comparison story is: for each scenario, which thresholds are crossed, at which step, by which cohort. Zone 1B and Zone 1D are where the comparison lives — Zone 1A shows the trajectory story. The design question is whether three scenario trajectories on Zone 1A become unreadable, and whether Zone 1B and 1D can show per-scenario differentiation without collapsing.

Use stories to investigate before architecture: (a) Three-scenario Zone 1A: can the analyst identify which scenario keeps the human development trajectory highest, without terminal labels? (b) Three-scenario Zone 1B: can the analyst see which scenarios trigger Q1 threshold crossings and at what step? (c) Three-scenario Mode 3: does the concept of "apply instrument to scenario A" still work when two other scenarios are visible?

### UX Designer — Multi-scenario experience journeys

Three experience journeys must be mapped before architecture is assessed:

**Journey 1 — Scenario Setup:** How does the user create or select three scenarios for comparison? Is this a new entry point, an extension of the current scenario selector, or a Mode 2 branching extension? What happens in Zone 1D (entity attribution) when three scenarios are active?

**Journey 2 — Primary Viewport in Comparison Mode:** Zone 1A with three trajectory sets. N>2 creates immediate curve identifiability risk — the DEMO6-014 fix (#1249) for two-scenario comparison will not be sufficient for three. Color + line-style + terminal-label differentiation for three scenarios must be specified before any frontend architecture is discussed.

**Journey 3 — Threshold Comparison:** Zone 1B and Zone 1D in comparison mode. The MDA alert panel surfaces threshold breaches — do breaches appear per-scenario or as a union across scenarios? The PSP surface in Zone 1D — does it show PSP for each scenario or a delta? These are UX decisions that determine the data contract, which determines the API architecture.

None of these can be answered by architecture alone. The UX journeys produce the wireframes that the Frontend Architect scopes and the Architect uses to assess ADR requirements.

### Customer Agent — Persona assessment for multi-scenario comparison

**Lucas Ferreira (Persona 1 — Programme Analyst):** Needs three-scenario comparison to reproduce and challenge IMF programme alternatives. His credibility gate: can he show the audience that option B has a worse Q1 trajectory than option A in a specific step window, from data accessible to both sides of the table? Not a UX luxury — a negotiating necessity.

**Aicha Mbaye (Persona 5 — Finance Minister):** Needs to read the comparison result within 90 seconds — not author it. She needs one clear answer: which option is least damaging to the bottom quintile? The comparison must be legible at glance level. Over-engineering the N>2 rendering risks losing her.

**Andreas Petrakis (Persona 3 — Political Advisor):** PSP comparison across scenarios. Which option has the highest programme survival probability? This is Zone 1D in comparison mode — a legitimate use case for #394 that must be addressed in the UX journey, not assumed.

**Minimum viable story for M17 design sprint:** The personas' needs reveal that the minimum viable multi-scenario is: (a) Side-by-side Zone 1A trajectories with labeled scenario differentiation; (b) Per-scenario Zone 1B threshold crossing summary (not a merged union); (c) Per-scenario PSP value in Zone 1D. Everything else — scenario interaction in Mode 3, full N≥4 support, cross-scenario Zone 1D delta — is enhancement beyond the Demo 7 minimum.

### Architect — ADR prerequisites (downstream of UX)

The ARCH-REVIEW-007 binding constraint (`COMPARE_VIEW N≤2/fixture`) was written before the UX journeys for multi-scenario existed. The constraint exists because the Zone 1A rendering architecture was not designed for N>2 differentiation. The UX Designer's Zone 1A journey (Journey 2 above) will surface whether a simple extension of the existing curve encoding suffices or whether a structural change to the compare rendering architecture is required.

**Assess at G2 Phase 2 (after UX journeys are accepted):**
- Does Zone 1A N>2 require changes to the composite_score rendering path, or only to the compare-mode overlay?
- Does Zone 1B per-scenario threshold crossings require a new backend data structure in the compare endpoint, or a frontend composition from the existing `threshold_crossings` field (#97 delivered in G9)?
- Does Zone 1D per-scenario PSP require a new endpoint or a client-side multi-scenario store structure?

**ADR determination:** If N>2 requires structural changes to Zone 1A composite encoding architecture, ARCH-REVIEW-007 must be reopened and the new architectural decision filed as ARCH-012 (or ARCH-013 if #1252 takes ARCH-012). If N>2 is a straightforward compare-mode extension within the existing component boundary, an architecture review note on #394 may suffice.

### Frontend Architect — Wave 2 sequencing (downstream of UX)

TrajectoryView is the most complex component in the frontend. N>2 scenario rendering will require changes to Zone 1A curve rendering. If #1249 (Zone 1A curve identifiability for N=2) is merged before G2 Phase 3 implementation begins, the N>2 implementation builds on a more legible Zone 1A base. If #1249 is merged concurrently with G2 implementation, the two will conflict on Zone 1A curve rendering.

**Recommended Wave 2 frontend sequencing:**
1. DEMO6 CRITICAL: #1249 (Zone 1A curve identifiability) → #1253 (Zone 1D PSP precedent) → #1250 (Zone 1B tablet legibility) — these must be sequential within G4; PRs cannot be in parallel on the same zone
2. UI bug: #1239 (Zone 1B inverted floor label) — small fix, can be alongside G4
3. #1251 (y-axis audit) — no zone conflicts; can run alongside G4 or G3
4. #1252 (Zone 1B ADR) — after ADR accepted; after #1250 merged to avoid Zone 1B conflicts
5. #394 (multi-scenario) — last; builds on stable Zone 1A (#1249) and Zone 1B (#1250/#1252) base

---

## Sprint Groups

| Group | Issues | Phase | Wave | Description |
|---|---|---|---|---|
| G1 — CM Calibration Sprint | #1229, #1248 | Single phase | Wave 1 (**entry gate**) | Fiscal-to-cohort ELASTICITY_REGISTRY revision (#1229, CM-owned); governance sensitivity specification (#1248, CM-owned). Hard gate — no other G-group sprint entry may open until G1 exits. |
| G2 — Multi-Scenario Design Sprint | #394 | Phase 1: Design (no sprint entry required); Phase 2: Architecture; Phase 3: Implementation sprint entry | Wave 2 | Design Thinking + UX Designer + Customer Agent → user journeys and use stories first; then Architect assessment of ARCH-REVIEW-007; then sprint entry for implementation. Design may complete in M17; implementation may carry to M18 depending on design complexity. |
| G3 — Zone 1B Architecture | #1252 | Implementation (ADR-gated) | Wave 2 | Formal proportional allocation between MDAAlertPanelZone1B and CohortImpactSection. ADR required before implementation (ADR-017 amendment or new ADR). `minHeight: 80px` temporary guarantee active. Can run parallel with G4 once ADR is accepted. |
| G4 — DEMO6 CRITICAL Polish | #1249, #1250, #1253, #1239 | Sequential PRs within single sprint entry | Wave 2 | Four issues: DEMO6-014 curve identifiability (#1249 — CRITICAL), DEMO6-026/043 tablet legibility (#1250 — CRITICAL), DEMO6-040 PSP precedent anchor (#1253 — CRITICAL), DEMO6-010 inverted floor label (#1239 — UI bug). FA-recommended sequence: #1249 → #1253 → #1250 → #1239. All four required before live Demo 7 session is scheduled. |
| G5 — Infrastructure Fixes | #1220, #1214, #1251 | Implementation | Wave 2 (capacity-allowing after G4) | Test infrastructure bug (#1220 — NM-061 upstream, G3 spec soft-skip); observability fix (#1214 — NM-060 upstream, startup WARNING); adaptive y-axis audit (#1251 — `computeYDomain()` extension). None are demo critical-path. |

### Issue-to-group full mapping

| Issue | Group | Wave | Priority |
|---|---|---|---|
| #982 | — (gate) | — | M17 exit checklist |
| #1229 | G1 | Wave 1 | **Entry gate** |
| #1248 | G1 | Wave 1 | **Entry gate** |
| #394 | G2 | Wave 2 | High — Demo 7 Act 2 |
| #1252 | G3 | Wave 2 | Medium — ADR-gated |
| #1249 | G4 | Wave 2 | **DEMO6 CRITICAL** |
| #1250 | G4 | Wave 2 | **DEMO6 CRITICAL** |
| #1253 | G4 | Wave 2 | **DEMO6 CRITICAL** |
| #1239 | G4 | Wave 2 | Bug |
| #1220 | G5 | Wave 2 | Bug / infrastructure |
| #1214 | G5 | Wave 2 | Infrastructure |
| #1251 | G5 | Wave 2 | Capacity-allowing |

### G2 Phase sequencing detail

```
G2 Phase 1 (no sprint entry required — design work):
  Design Thinking Agent: cognitive task analysis for N>2 comparison
  UX Designer: Journey 1/2/3 wireframes + zone layout for N>2
  Customer Agent: persona minimum viable story (Lucas/Aicha/Andreas)
        │
        ↓ BPO accepts Phase 1 output (use stories + journeys)
        │
G2 Phase 2 (no sprint entry required — architecture):
  Architect: ARCH-REVIEW-007 revisitation with UX in hand
  Frontend Architect: component scope, TrajectoryView N>2 feasibility
        │
        ↓ Architect concludes: ARCH-REVIEW-007 amendment or new ADR (if needed)
        │
G2 Phase 3 (sprint entry required — implementation):
  QA tests authored before implementation PR opens
  Implementation — must start after #1249 (Zone 1A identifiability) is merged
```

### Wave 2 sequencing diagram

```
Wave 1: G1 (CM calibration — FRAME-D exit gate) ──────────────────────────────────────────┐
                                                                                           │
                                            ↓ Wave 1 exit confirmed                       │
                                                                                           │
G2 Phase 1 (design — parallel with G4/G5 design phases) ──────────────────────────────────┤
  ↓                                                                                        │
G2 Phase 2 (architecture — after Phase 1 accepted) ───────────────────────────────────────┤
  ↓                                                                                        │
G4 (#1249 → #1253 → #1250 → #1239 — sequential PRs) ─────────────────────────────────────┤
                                                                                           ├─► G8 (M18 Demo 7)
G3 (#1252 — after ADR accepted; after #1250 merged) ──────────────────────────────────────┤
                                                                                           │
G5 (#1220, #1214, #1251 — capacity-allowing) ─────────────────────────────────────────────┤
                                                                                           │
G2 Phase 3 (#394 implementation — after #1249 merged; after Phase 2 architecture) ────────┘
  (may carry to M18 if design/architecture phase reveals scope complexity)
```

---

## Wave 1 Exit Gate (Binding)

**Wave 2 may not begin until all three conditions are satisfied:**

1. DemographicModule ELASTICITY_REGISTRY updated with CM-certified constants for the fiscal-to-cohort poverty transmission channel, with a written calibration decision documenting the chosen path and citing specific sources
2. FRAME-D test confirmed: backend integration test passes in CI asserting that Q1 `poverty_headcount_ratio` delta per step is within the CM-certified range under the Senegal T3 conditionality shock (100-step quarterly, SEN Article IV scenario)
3. Governance sensitivity calibration specification on record: CM-authored document specifying recommended constants for GovernanceModule fiscal conditionality transmission; implementation may carry to Wave 2, specification must exist before Wave 2 begins

PI Agent confirms all three at Wave 1 exit. G1 sprint exit document must record explicit confirmation.

---

## Exit Conditions

M17 closes when all of the following are satisfied:

1. **Wave 1 exit gate** confirmed by PI Agent (G1 sprint exit document)
2. **Business PO acceptance** for all user-facing Wave 2 deliverables: #394 (if implementation completes), #1249, #1250, #1253, #1239
3. **Customer Agent Layer 3 assessment** for capabilities serving Personas 1, 2, 3, or 5
4. **North star test artifact** for #394 (if implementation completes) and DEMO6 CRITICAL polish: a Senegalese Finance Minister's team can see three-scenario comparison and identify the binding constraint without presenter narration, at 1280×800 and 768px
5. **M16 retrospective testing improvements** addressed: calibration integration test (G1 exit); visual distinguishability assertion extension (#1251 scope); Zone 1B overflow regression (#1252 scope); demo script testid discipline (#1220/#1249 scope)
6. **PI Agent exit gate confirmation** recorded in the M17 sprint exit document
7. **#982** (M17 Exit Checklist) closed

**If G2 Phase 3 implementation carries to M18:** M17 closes with G2 design and architecture complete, implementation deferred. The design and architecture artifacts (journeys, wireframes, use stories, ADR decision) are the M17 G2 deliverable. BPO and Customer Agent assess the design artifacts, not the implementation. PI Agent notes the carry in the exit document.

---

## Sprint Entry Gate Requirements

Per `docs/process/sprint-planning-sop.md §Sprint Entry Gate`, implementation may not begin on any sprint group until:

1. This sprint plan is EL-approved
2. **Wave 1 exit gate confirmed before any Wave 2 implementation sprint entry is filed**
3. A sprint entry document filed at `docs/process/sprint-plans/m17-{group}-sprint-entry.md` per template
4. Entry document committed and referenced in `SESSION_STATE.md`

**G1 additional requirement:** CM explicitly activated on #1229 and #1248 before G1 sprint entry is filed. The sprint entry must record the CM activation.

**G2 Phase 1 exception:** No sprint entry required for Phase 1 (design work only). Phase 1 produces design artifacts — use stories, UX journeys, wireframes — which are committed to `docs/ux/` or `docs/process/intents/` and BPO-reviewed. Phase 2 (architecture) also requires no sprint entry — it produces an architecture review and ADR decision. Only Phase 3 (implementation) requires a sprint entry document.

**G2 Phase 3 gate:** #1249 must be merged before G2 Phase 3 implementation PR opens. Zone 1A N>2 rendering must not begin on a Zone 1A codebase that has not passed the DEMO6-014 identifiability fix.

**G3 gate:** ADR accepted before implementation PR opens.

---

## M17 Kickoff Sequence

1. ✅ EL merges `release/m16` → `main` — DONE 2026-06-25 (PR #1259)
2. ✅ PM Agent cuts `release/m17` from `main` — DONE 2026-06-25 at commit d806957
3. ✅ CI trigger verified — `.github/workflows/ci.yml` covers `release/m*`
4. ✅ #982 renamed "M17 Exit Checklist" — DONE 2026-06-25
5. ✅ Issue audit complete — all open issues accounted for; #1229 assigned to M17; #843 moved to M18; #1225 closed; six issues milestoned — DONE 2026-06-25
6. ✅ This sprint plan filed — DONE 2026-06-25 (v2)
7. ⬜ EL approves sprint plan
8. ⬜ CM activated on #1229 and #1248 — immediately after EL approval
9. ⬜ G1 sprint entry filed and EL-approved — Wave 1 begins
10. ⬜ Wave 1 exit gate confirmed by PI Agent
11. ⬜ G2 Phase 1 (design sprint) begins — Design Thinking + UX Designer + Customer Agent; may run concurrently with Wave 1 G1 work if EL chooses (design work is not blocked by calibration)
12. ⬜ G4 DEMO6 CRITICAL sprint entry — first Wave 2 implementation group after Wave 1 exits
