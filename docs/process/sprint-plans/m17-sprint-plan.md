---
name: m17-sprint-plan
type: sprint-plan
milestone: M17 — Calibration and Comparative Infrastructure
status: Pending EL Approval
authored-by: PM Agent
authored-date: 2026-06-25
el-approved:
consulted-agents:
  - Chief Methodologist (Wave 1 calibration scope and uncertainty; exit gate specification)
  - Business Product Owner (Demo 7 value prioritization; Wave 2 scope cut order)
  - Architect (ADR prerequisites for #1252 and #394; N>2 constraint in ARCH-REVIEW-007)
  - Frontend Architect (Wave 2 frontend sequencing; TrajectoryView N>2 conflict risk)
sop-reference: docs/process/sprint-planning-sop.md
---

# M17 Sprint Plan — Calibration and Comparative Infrastructure

**Status:** Pending EL Approval — implementation may NOT begin until this plan is EL-approved and a sprint entry document is filed per group
**Release branch:** `release/m17` (cut from `main` at commit d806957, 2026-06-25)
**Exit checklist issue:** #982 (renamed 2026-06-25 — "M17 Exit Checklist — blocks milestone closure")
**Primary objective:** Make Demo 7 analytically defensible. Two-wave structure: Wave 1 (CM calibration sprint) is the hard prerequisite for Wave 2 (DEMO6 CRITICAL polish + comparative infrastructure). No live demo at M17 close — Demo 7 is at M18.

**M17 exit gate:** PI Agent exit gate confirmation, with BPO acceptance for all Wave 2 user-facing deliverables and Customer Agent Layer 3 for Personas 1, 2, 3, 5. #982 closes last. No live demo required for M17 close.

**M17 thesis:** The FRAME-D gap — the milestone sentence that did not fire in the Demo 6 window — is not a demo polish problem. It is a calibration problem. M17 resolves the analytical credibility of the engine before any new capability is built on top of it.

---

## Kickoff Prerequisites (Status at Sprint Plan Filing)

| Step | Status | Notes |
|---|---|---|
| 1. EL merges `release/m16` → `main` (admin bypass) | ✅ DONE 2026-06-25 | PR #1259 merged; `main` at b2a2f09 before HORIZON sweep |
| 2. PM Agent cuts `release/m17` from `main` | ✅ DONE 2026-06-25 | `release/m17` cut from `main` at commit d806957 |
| 3. PM Agent authors `m17-sprint-plan.md` | ✅ THIS DOCUMENT | Filed 2026-06-25; EL approval pending |
| 4. EL approves sprint plan | ⬜ PENDING | Required before any sprint entry is filed |
| 5. #982 renamed "M17 Exit Checklist" | ✅ DONE 2026-06-25 | Confirmed at M16 exit ceremony |
| 6. CI trigger verified | ✅ CLEAR | `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` |

---

## HORIZON Scope-Completeness Check (Step 6)

Run against `CLAUDE.md §Milestone 17` and `docs/roadmap/worldsim-roadmap.md §Milestone 17`.

### Roadmap deliverables — linkage audit

| Roadmap deliverable | Issue | Wave | Status |
|---|---|---|---|
| Fiscal-to-cohort elasticity calibration — ELASTICITY_REGISTRY revision | #1229 | Wave 1 | ✅ Tracked; CM-owned |
| Governance sensitivity calibration — fiscal conditionality transmission | #1248 | Wave 1 | ✅ Tracked; CM-owned |
| Multi-scenario comparison (>2 scenarios) | #394 | Wave 2 | ✅ Tracked |
| DEMO6-014: Zone 1A curve identifiability | #1249 | Wave 2 | ✅ Tracked |
| DEMO6-026/043: Zone 1B tablet legibility (768px) | #1250 | Wave 2 | ✅ Tracked |
| DEMO6-040: PSP historical precedent anchor in Zone 1D | #1253 | Wave 2 | ✅ Tracked |
| Adaptive y-axis extension audit | #1251 | Wave 2 | ✅ Tracked |
| Zone 1B proportional allocation (ADR required) | #1252 | Wave 2 | ✅ Tracked |
| Live stakeholder demo (#843) | #843 | M18 | ✅ Deferred to M17/Demo 7 (EL decision 2026-06-25); Demo 7 at M18 — not M17 close |

**M18-deferred items (not M17 scope):**
- Zone 1A CI bands (ADR-007 scope; architecture decision required) → #1254
- PSP driver decomposition in Zone 1D → #1255
- Path 2 full implementation → #1256 (deferred per AC-001 — see `docs/architecture/constraints.md`)

**Scope gap finding:** No new UNTRACKED items identified at kickoff. All Wave 1 and Wave 2 issues were filed during M16 exit ceremony (PR #1257). DEMO6 HIGH/MEDIUM/LOW findings (outside the four CRITICALs) remain reference material in `docs/demo/m16/reviews/2026-06-25-v0.16.0-audience-simulation.md` — PM Agent will promote specific ones to GitHub if they enter Wave 2 scope planning.

### ADR backlog review

| ARCH entry | Status | Action |
|---|---|---|
| ARCH-001 through ARCH-011 | All ACCEPTED or ASSIGNED | No action needed |
| #1252 Zone 1B proportional allocation | No ARCH entry | Architect must determine at G3 sprint entry whether this requires ADR-017 amendment (ARCH-011 scope extension) or a new ADR. A new ADR would be ARCH-012. The temporary `minHeight: 80px` guarantee (PR #1235) is not an architectural decision — it is an incident response. |
| #394 multi-scenario comparison (N>2) | No ARCH entry | ARCH-REVIEW-007 explicitly constrained COMPARE_VIEW to N≤2 (2026-06-22). Architect must assess whether N>2 comparison requires reopening that constraint — if so, ARCH-012 (or ARCH-013 if #1252 takes ARCH-012). Assess at G2 sprint entry. |

---

## Four-Agent Consultation Summary

### Chief Methodologist — Wave 1 calibration scope

Wave 1 is research work with genuine uncertainty about the outcome. Three possible conclusions exist going in:

1. **Direct elasticity path:** `fiscal_policy_spending_change` should have direct elasticity entries in ELASTICITY_REGISTRY that bypass the GDP multiplier chain — social spending cuts have a documented direct poverty transmission pathway that is faster and larger than the indirect GDP channel.
2. **Multiplier adjustment path:** The GDP multiplier should be larger for social spending cuts specifically — the standard 0.5 Keynesian multiplier understates the poverty impact of cuts to targeted social programmes.
3. **T3 accuracy path:** The current calibration accurately represents the uncertainty at T3. The ~+0.0015pp/step poverty delta is the correct modelled output at Inferred quality. The demo argument should stay at the structural trajectory level ("approaching the threshold") rather than claiming step-level crossing precision that T3 data cannot support.

The CM must produce a written calibration decision — not just an updated ELASTICITY_REGISTRY — that documents which path is correct and why, citing the specific sources. If path 3 is the conclusion, the Wave 1 exit is still complete: the decision that the calibration is accurate is a calibration decision, and the Demo 7 argument is reframed accordingly (structural trajectory without step-crossing claim).

For governance sensitivity (#1248): the CM review must address three sub-questions: (a) whether governance composite scoring accounts for institutional capacity degradation under austerity; (b) whether `imf_program_acceptance` has direct governance transmission distinct from the GDP channel; (c) whether the 8-step quarterly window is long enough to manifest governance divergence or whether governance stress is a longer-horizon signal. The governance review may produce only a specification (recommended elasticity values) if the implementation timeframe extends beyond Wave 1 — it does not block the Wave 1 exit gate if the specification is filed. The fiscal-to-cohort calibration change is the primary gate condition.

**Wave 1 exit gate (hard):** The FRAME-D milestone sentence fires within the 8-step Demo 6 programme window on the Senegal Article IV scenario after the ELASTICITY_REGISTRY change is applied. DemographicModule ELASTICITY_REGISTRY updated with CM-certified constants. The governance calibration specification is on record (implementation may carry to Wave 2). A backend integration test asserts: given the Senegal T3 conditionality shock, Q1 poverty_headcount_ratio delta per step is within the CM-certified range.

### Business Product Owner — Demo 7 value prioritization

M17 has no live demo. Its value is entirely about making Demo 7 defensible. Two elements of Demo 7 are structurally dependent on M17 work:

1. **Demo 7 Act 1 (Senegal Mode 3):** The Mode 3 active control search — "can any fiscal instrument prevent Q1 informal workers crossing 0.40?" — is only analytically meaningful if the fiscal-to-cohort transmission channel is calibrated. An uncalibrated response surface makes the Mode 3 search meaningless. Wave 1 is the prerequisite for Act 1 to be a real question.

2. **Demo 7 Act 2 (Zambia three-scenario):** The three-scenario comparison requires #394 infrastructure. This is the primary Wave 2 deliverable for Demo 7 Act 2. #394 is complex infrastructure work — it requires architecture assessment (N>2 constraint from ARCH-REVIEW-007 revisitation), a full sprint entry, and frontend component changes to TrajectoryView. Do not underscope it.

**DEMO6 CRITICAL polish (#1249/#1250/#1253) is required before the live demo session.** These are not optional improvements — they address audience legibility failures that would make the Demo 7 session ineffective. All three must be resolved before the live session is scheduled in M18.

**Scope cut order if M17 capacity is constrained:**
1. Never cut Wave 1 (the entire milestone premise is the calibration)
2. Never cut #1249/#1250/#1253 (DEMO6 CRITICAL — live demo readiness)
3. Never cut #394 (Demo 7 Act 2 infrastructure)
4. Cut #1251 (adaptive y-axis extension audit) if capacity requires — no demo dependency
5. Cut #1252 (Zone 1B proportional allocation ADR) if capacity requires — `minHeight: 80px` guarantee (PR #1235) provides acceptable temporary protection through Demo 7

### Architect — ADR prerequisites

| Group | ADR required | Coverage | Gate |
|---|---|---|---|
| G1 Wave 1 (#1229, #1248) | None | DemographicModule and GovernanceModule calibration is within existing module boundaries; no new module or architectural pattern introduced | CLEAR |
| G2 Wave 2 (#394 multi-scenario) | ARCH-REVIEW-007 revisitation required | ARCH-REVIEW-007 (2026-06-22) binding decision: `COMPARE_VIEW N≤2/fixture`. If N>2 comparison changes Zone 1A trajectory rendering architecture, this constraint must be formally reopened. Architect assesses at G2 sprint entry — may trigger ARCH-012 or an ARCH-REVIEW-007 amendment. | CONDITIONAL — assess at G2 sprint entry |
| G3 Wave 2 (#1252 Zone 1B allocation) | ADR-017 amendment or new ADR | Zone 1B proportional allocation is an architectural decision, not an implementation detail. The current `flex: "1 1 0"` + `minHeight: 80px` state is an incident-response guarantee, not an accepted architecture. A formal architectural decision is required before a durable implementation. Architect determines scope at G3 sprint entry: ADR-017 amendment (ARCH-011) or new ADR (ARCH-012/ARCH-013). | CONDITIONAL — ADR before implementation |
| G4 Wave 2 (#1249, #1250, #1253 DEMO6 CRITICAL) | None | #1249 is Zone 1A encoding extension (within ADR-017). #1250 is Zone 1B display fix (within ADR-017 disposition (b)). #1253 is Zone 1D documentation extension (within ADR-015). No new architecture required. | CLEAR |
| G5 Wave 2 (#1251 y-axis audit) | None | Extension of `computeYDomain()` pattern established in PR #1243. Within existing component boundaries. No new ADR. | CLEAR |

### Frontend Architect — Wave 2 sequencing

**#394 (multi-scenario comparison) touches TrajectoryView — the most complex frontend component.** N>2 scenario rendering requires Zone 1A changes. If #1249 (curve identifiability — terminal labels or line style) is merged after #394 begins, the implementations will conflict on Zone 1A curve rendering. Recommended sequencing: DEMO6 CRITICAL fixes (#1249/#1250/#1253) first, #394 second. This ensures #394 builds on a stable, legibility-validated Zone 1A base.

**#1252 (Zone 1B proportional allocation) and #1250 (Zone 1B tablet legibility) must not be in the same PR.** Both touch Zone 1B. #1252 changes the structural layout (flex split between MDAAlertPanelZone1B and CohortImpactSection). #1250 changes the content display (current value + floor + T3 badge at 768px). Sequential: #1250 first (simpler, DEMO6 CRITICAL), then #1252 (after ADR decision, structural).

**Wave 2 recommended frontend sequencing:**
1. #1249 (Zone 1A curve identifiability — terminal labels/dashed style)
2. #1253 (Zone 1D PSP historical precedent — documentation + data)
3. #1250 (Zone 1B tablet legibility — display fix)
4. #1251 (y-axis extension audit — `computeYDomain()` extended to other instruments; may identify additional instruments requiring fixes)
5. #1252 (Zone 1B proportional allocation — after ADR accepted)
6. #394 (multi-scenario comparison — after Zone 1A/1B are legibility-stable)

---

## Sprint Groups

| Group | Issues | ADR gate | Wave | Description |
|---|---|---|---|---|
| G1 — CM Calibration Sprint | #1229, #1248 | None | Wave 1 (**entry gate for entire milestone**) | Fiscal-to-cohort elasticity calibration (#1229 — DemographicModule ELASTICITY_REGISTRY; CM-owned); governance sensitivity calibration (#1248 — GovernanceModule fiscal conditionality transmission; CM-owned). No other G-group sprint entry may be filed until G1 exits. |
| G2 — Multi-Scenario Comparison | #394 | ARCH-REVIEW-007 revisitation required | Wave 2 (after G1 exit) | N>2 scenario comparison infrastructure. TrajectoryView N>2 rendering. Backend compare endpoint extension. Architect must assess N>2 constraint from ARCH-REVIEW-007 before sprint entry. Most complex Wave 2 deliverable. Demo 7 Act 2 (Zambia three-scenario) depends on this. |
| G3 — Zone 1B Architecture | #1252 | ADR-017 amendment or new ADR | Wave 2 (after G1 exit; ADR required before implementation) | Formal proportional allocation between MDAAlertPanelZone1B and CohortImpactSection. Replace `minHeight: 80px` temporary guarantee with durable design. ADR decision required at sprint entry — Architect determines whether ADR-017 amendment or new ADR. |
| G4 — DEMO6 CRITICAL Polish | #1249, #1250, #1253 | None | Wave 2 (after G1 exit; before live demo session is scheduled) | Three CRITICAL findings from Demo 6 audience simulation (DEMO6-014/#1249: Zone 1A curve identifiability; DEMO6-026/043/#1250: Zone 1B tablet legibility at 768px; DEMO6-040/#1253: PSP historical precedent anchor in Zone 1D). All three required before Demo 7 session is scheduled. Can be a single sprint group with sequential PRs per FA recommendation. |
| G5 — Adaptive Y-Axis Extension Audit | #1251 | None | Wave 2 (after G1 exit; capacity-allowing after G4) | Audit all instruments for the Zone 1A curve overlap failure mode identified in IR-001. Extend `computeYDomain()` pattern to any instrument with a fixed-domain chart. May identify additional instruments requiring fixes beyond the audit scope. |

### Wave 2 sequencing diagram

```
G1 (CM calibration — Wave 1 entry gate) ──────────────────────────────────────────────────┐
                                                                                           │
                                                  ↓ Wave 1 exit gate: FRAME-D fires        │
                                                                                           │
G4 (DEMO6 CRITICAL — #1249 → #1250 → #1253) ─────────────────────────────────────────────┤
  (sequential within G4 per FA sequencing)                                                  │
                                                                                           ├─► G8 (M18 live demo)
G5 (y-axis audit — #1251 — capacity-allowing) ──────────────────────────────────────────┐ │
                                                                                         ↓ │
G3 (Zone 1B allocation — #1252 — after ADR) ─────────────────────────────────────────┐ │ │
                                                                                      ↓ │ │
G2 (multi-scenario — #394 — after G4 Zone 1A stable) ───────────────────────────────────┘─┘
```

**Critical path:** G1 → [any Wave 2 group may begin]. G4 DEMO6 CRITICAL is highest priority within Wave 2. G2 (#394) is the largest Wave 2 item and must not begin until #1249 (Zone 1A curve identifiability) is merged — the two will conflict on TrajectoryView Zone 1A rendering. G3 (#1252) cannot begin until its ADR is accepted.

---

## Wave 1 Exit Gate (Binding)

**Wave 2 may not begin until all three conditions are satisfied:**

1. DemographicModule ELASTICITY_REGISTRY updated with CM-certified constants for the fiscal-to-cohort poverty transmission channel (`fiscal_policy_spending_change` → Q1/Q2 `poverty_headcount_ratio`), with written calibration decision documenting which of the three calibration paths was taken and why
2. FRAME-D test confirmed: backend integration test asserts that given the Senegal T3 conditionality shock (SEN Article IV scenario, 100-step quarterly, IMF programme acceptance), Q1 `poverty_headcount_ratio` delta per step is within the CM-certified range. Test must pass in CI.
3. Governance sensitivity calibration specification on record: CM-authored document specifying recommended elasticity values for GovernanceModule → `imf_program_acceptance` transmission, institutional capacity degradation under austerity, and the recommended 8-step horizon assessment. Implementation may carry to Wave 2; specification must exist before Wave 2 begins.

PI Agent confirms these three conditions at Wave 1 exit. G1 sprint exit document must contain explicit confirmation of all three.

---

## Exit Conditions

M17 closes when all of the following are satisfied:

1. **Wave 1 exit gate** confirmed: PI Agent verification that all three Wave 1 conditions above are satisfied and recorded in the G1 sprint exit document
2. **Business PO acceptance** recorded for all user-facing Wave 2 deliverables: #394, #1249, #1250, #1253 (G2, G4 user-facing issues). G3 (#1252) and G5 (#1251) may accept Infrastructure Sprint exception from BPO if no user-facing change is produced.
3. **Customer Agent Layer 3 assessment** for any Wave 2 deliverable serving Personas 1, 2, 3, or 5: #394 (multi-scenario — Personas 1, 5), #1249/#1250/#1253 (DEMO6 CRITICAL — all personas)
4. **North star test artifact** filed for #394 and DEMO6 CRITICAL polish: can a Senegalese Finance Minister's team see three-scenario comparison and identify the binding constraint without presenter narration?
5. **M16 retrospective testing improvements** implemented: calibration integration test (post-Wave 1); visual distinguishability assertion extension (post-#1251 audit); Zone 1B overflow regression (post-#1252 implementation); demo script testid discipline audit (post-G4). See SESSION_STATE.md §M16 Exit Ceremony retrospective §3 for the full checklist — these must be checked before M17 close.
6. **PI Agent exit gate confirmation** recorded in the M17 sprint exit document
7. **#982** (M17 Exit Checklist) closed

**What M17 does not do:** No live demo at M17 close. No CI bands on Zone 1A trajectories (#1254 — M18). No PSP driver decomposition (#1255 — M18). No Path 2 (#1256 — M18+).

---

## Sprint Entry Gate Requirements

Per `docs/process/sprint-planning-sop.md §Sprint Entry Gate`, implementation may not begin on any sprint group until:

1. This sprint plan is EL-approved
2. **Wave 1 exit gate is confirmed before any Wave 2 sprint entry is filed** — this is a hard stop, not guidance
3. A sprint entry document is filed at `docs/process/sprint-plans/m17-{group}-sprint-entry.md` per the template
4. The entry document is committed and referenced in `SESSION_STATE.md`

**G1 additional requirements:** CM must be explicitly activated on both #1229 and #1248 before G1 sprint entry is filed. The sprint entry document must include the CM activation record. CM sign-off is not post-implementation review — the CM calibration decision IS the G1 deliverable.

**G2 additional gate:** Architect assessment of N>2 ARCH-REVIEW-007 constraint must be on record before G2 sprint entry is filed. If a new ADR is required, it must be ASSIGNED in the ADR backlog before the sprint entry is filed.

**G3 additional gate:** ADR-017 amendment or new ADR must be ACCEPTED before G3 implementation PR opens. ADR decision may be authored concurrently with G4 work — but G3 implementation is blocked until the ADR is accepted.

---

## M17 Kickoff Sequence

1. ✅ EL merges `release/m16` → `main` — DONE 2026-06-25 (PR #1259)
2. ✅ PM Agent cuts `release/m17` from `main` — DONE 2026-06-25 at commit d806957
3. ✅ CI trigger verified — `.github/workflows/ci.yml` covers `release/m*`
4. ✅ #982 renamed "M17 Exit Checklist" — DONE 2026-06-25
5. ✅ This sprint plan filed — DONE 2026-06-25
6. ⬜ EL approves sprint plan
7. ⬜ CM activated on #1229 and #1248 — immediately after EL approval
8. ⬜ G1 sprint entry filed and EL-approved — CM must be activated first; this is the Wave 1 entry
9. ⬜ G1 Wave 1 work begins — CM calibration sprint; no other G-group begins until G1 exits
10. ⬜ Wave 1 exit gate confirmed by PI Agent
11. ⬜ Wave 2 G-group sprint entries filed (after Wave 1 exit); G4 DEMO6 CRITICAL first priority
