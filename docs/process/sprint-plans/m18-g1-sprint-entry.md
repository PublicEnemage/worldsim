---
name: m18-g1-sprint-entry
type: sprint-entry
milestone: M18 — Full Argument and Demo 7
sprint-group: G1
status: EL-approved 2026-06-26 — intent document filed 2026-06-26; UX/UI mockups, panel review, and QA tests required before implementation PR opens
authored-by: PM Agent
authored-date: 2026-06-26
el-approved: 2026-06-26
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M18, G1: CI Bands on Zone 1A

**Status:** EL-approved 2026-06-26 — intent document filed 2026-06-26; UX/UI mockups, panel review, and QA tests required before implementation PR opens
**Date authored:** 2026-06-26
**Release branch:** `release/m18`
**Sprint plan:** `docs/process/sprint-plans/m18-sprint-plan.md` (EL-approved 2026-06-26, PR #1364)
**Sprint journal issue:** #1367

*EL-approved. Implementation PR may not open until intent document, UX/UI mockups, panel review, and QA tests are complete (§2.3 and §2.4).*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| GitHub Milestone | #19 (API: milestone 19) |
| Sprint group | G1 — CI Bands on Zone 1A (Wave 1) |
| Release branch | `release/m18` |
| Sprint sub-branch | `sprint/m18-g1` |
| Sprint plan document | `docs/process/sprint-plans/m18-sprint-plan.md` |
| Exit checklist issue | #1340 |
| Sprint journal issue | #1367 |
| Sprint groups in scope | G1 only |
| Wave coordination tier | **Standard** — 2 concurrent groups (G1 + G2); well within 5-group ceiling |
| Concurrent groups at entry | 2 of 5 max (G1 + G2 opening simultaneously) |
| Cross-group dependencies | None — G1 (TrajectoryView.tsx / banding engine) and G2 (Zone 1D / PSP module) touch distinct file areas; no merge ordering constraint |

---

## Section 2 — Entry Invariants Checklist

*All items must be confirmed before any G1 implementation PR opens.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m18` cut from `main` 2026-06-26 (commit 8cffc86 after sync PR #1366 merged)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` and `sprint/m*` — confirmed 2026-06-26. 6 required checks: `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m18-sprint-plan.md` EL-approved 2026-06-26 (PR #1364 merged)

### 2.2 — ADR prerequisite gate

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G1 — #1254 (CI bands, Zone 1A) | ADR-007 (synthetic data / CI band methodology) | **ACCEPTED** 2026-05-23 | **CLEAR** |
| G1 — #1254 (Zone 1A visual encoding) | ADR-017 (Zone 1A information architecture) | **ACCEPTED** 2026-06-22 | **CLEAR** |

- [x] All ADR prerequisites accepted. Gate: **CLEAR**.

ADR-007 provides the methodology authority for CI band computation (confidence interval derivation, tier assignment for bands). ADR-017 provides the visual encoding authority for how bands render on Zone 1A trajectories (§Decision table: framework × branch × mode encoding). CI ribbons are a new visual channel within the existing Zone 1A encoding framework — no new ADR required.

### 2.3 — Intent document gate

G1 is UX/UI-impacting (new visual element on Zone 1A trajectories). An intent document is required before the implementation PR opens.

- [ ] Intent document filed: `docs/process/intents/M18-G1-2026-06-26-ci-bands-zone-1a.md` — **required before implementation PR opens**

The intent document must specify:
- CI band visual treatment: ribbon opacity, color, width, and whether interaction (tooltip on hover) is in scope
- Data contract: what fields the backend produces (`uncertainty_lower`, `uncertainty_upper` per step per framework, or equivalent) and which `docs/schema/` files must be updated
- Observable application state: "The CI band is visible on the Zone 1A trajectory at 1280×800 for the Zambia baseline scenario, with lower/upper bounds rendered as a semi-transparent ribbon around the composite score line. Band width reflects the confidence tier of the underlying data."
- Acceptance criteria the QA Lead can assert from without reading implementation code

**UX/UI design artifact gate (SOP §Sprint Entry Gate — UX/UI):**

CI bands are a new visual pattern on Zone 1A (not merely a color change — new geometry). A UX mockup is required before the implementation PR opens. A UI mockup specifying opacity, color palette reference, and interaction state is required because this introduces a new visual element type on the primary instrument.

- [ ] UX mockup filed and referenced from intent document — **required before implementation PR opens**
- [ ] UI mockup filed (new visual element: band opacity, color, interaction states) — **required before implementation PR opens**
- [ ] UX/UI panel review complete (5 agents: UX Designer, Design Thinking, Customer Agent, Frontend Architect, Business PO) — **required before implementation PR opens**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #1254 — CI bands on Zone 1A | ADR-007 + ADR-017 | `docs/process/intents/M18-G1-2026-06-26-ci-bands-zone-1a.md` | **Yes — filed 2026-06-26** |

### 2.4 — QA test authorship gate

- [ ] QA test file authored from intent document acceptance criteria before implementation code is written — **required before implementation PR opens**

Expected test file: `frontend/tests/e2e/m18-g1-ci-bands.spec.ts`

The test must assert: CI band ribbon is visible on Zone 1A at the specified breakpoints; band opacity and color match the UI mockup spec; the band updates when a different scenario branch is selected; the band is absent when uncertainty data is unavailable (graceful degradation).

A backend integration test is also required: `backend/tests/test_m18_g1_ci_bands.py` asserting that the uncertainty output endpoint returns lower/upper bounds per step for the Zambia baseline scenario within the ADR-007 tier structure.

| Deliverable | Test file path | Authored before implementation? |
|---|---|---|
| #1254 — CI bands (frontend) | `frontend/tests/e2e/m18-g1-ci-bands.spec.ts` | No — required before implementation PR opens |
| #1254 — CI bands (backend) | `backend/tests/test_m18_g1_ci_bands.py` | No — required before implementation PR opens |

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state |
|---|---|---|---|
| #1254 | ux(zone-1a): CI bands on Zone 1A trajectory curves — ADR-007 implementation | High — Demo 7 Act 2 epistemic foundation | CI band ribbon visible on Zone 1A trajectory curves for Zambia baseline scenario at 1280×800. Backend produces lower/upper uncertainty bounds per step per framework, consistent with ADR-007 confidence tier assignments. The Demo 7 Act 2 claim ("confidence band on the 340,000 vs. 80,000 differential") is computable from backend data and visually grounded on screen. |

### 3.2 — Issues explicitly out of scope

| Issue | Rationale for exclusion |
|---|---|
| #1255 — PSP decomposition | G2 — Wave 1 parallel group; separate file area |
| #1349 — Counter-scenario comparison | G3 — Wave 2; requires GR close and Architect determination |
| #1217 / control plane | G4 — Wave 2; requires ADR-019 |
| Any Zone 1B, 1C, or 1D changes | G1 scope is Zone 1A and the backend uncertainty output only |
| Uncertainty quantification for non-Zone-1A surfaces | Deferred — ADR-007 full implementation is Zone 1A first |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G1 — #1254 | ADR-007 + ADR-017 | Both ACCEPTED | Yes — after EL approves this entry; intent document, UX/UI mockups, panel review, and QA tests must exist before implementation PR opens |

**Implementation sequencing for G1:**

1. EL approves this entry document
2. UX Designer produces UX mockup + UI mockup for CI band visual treatment
3. UX/UI panel review (5 agents) — ACCEPT required
4. ✅ Frontend Architect Agent files intent document `docs/process/intents/M18-G1-2026-06-26-ci-bands-zone-1a.md` — **done 2026-06-26**; panel-approved UX/UI mockup to be referenced when complete
5. QA Lead authors `frontend/tests/e2e/m18-g1-ci-bands.spec.ts` and `backend/tests/test_m18_g1_ci_bands.py` from intent document acceptance criteria (red before implementation)
6. Implementing agent opens feature branch `feat/m18-g1-ci-bands` from `sprint/m18-g1`
7. Implementation: backend uncertainty output extension + frontend Zone 1A CI ribbon rendering
8. Schema files updated in same PR (`docs/schema/api_contracts.yml`, `docs/schema/simulation_state.yml`)
9. Pre-push gate: `cd backend && ruff check . && mypy app/`; `cd frontend && npm run build` — both exit 0
10. PR targeting `sprint/m18-g1`; set auto-merge
11. Integration PR `sprint/m18-g1` → `release/m18` after feature PR merges; PI Agent gate comment required
12. BPO acceptance and Customer Agent Layer 3 at sprint exit

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-26
**Sweep period:** M17 exit ceremony (2026-06-26) through M18 G1 sprint entry filing (2026-06-26)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified. All M17 NM entries (NM-066 through NM-071) were resolved before M18 kickoff and are confirmed resolved. M18 entry blockers all cleared. | N/A | N/A | N/A |

---

## Section 6 — Sprint Group Isolation

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m18-g1` |
| Cut from | `release/m18` at commit 8cffc86 (2026-06-26) |
| Sprint journal issue | #1367 |

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `frontend/src/components/TrajectoryView.tsx` | Sprint sub-branch | CI band ribbon rendering |
| `frontend/src/stores/` (uncertainty data shape) | Sprint sub-branch | New uncertainty fields |
| `backend/app/simulation/` (banding engine) | Sprint sub-branch | Uncertainty output extension |
| `docs/schema/api_contracts.yml` | Sprint sub-branch (same PR as implementation) | New uncertainty response fields |
| `docs/schema/simulation_state.yml` | Sprint sub-branch (same PR as implementation) | New uncertainty quantity fields |
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified |
| `docs/compliance/scan-registry.md` | PM Agent coordination lane | If compliance scan produced |

G1 does not write to `InstrumentCluster.tsx` structurally — CI bands are passed as props to TrajectoryView. If any InstrumentCluster change is needed, PM Agent must assess G2 conflict risk before opening that PR.

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required. All G1 writes are to implementation code, test files, and schema files.

#### 6.3a — New output paths declaration

- [x] No new output directories introduced by G1. `backend/test-results/` and `frontend/test-results/` are already covered by `.gitignore` (PR #1346).

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies. G1 (Zone 1A / banding engine) and G2 (Zone 1D / PSP module) touch distinct file areas. G1 need not wait for G2 and G2 need not wait for G1.

### 6.5 — Prior NM verification

**NM verification sweep date:** 2026-06-26
**Sweep period:** M17 exit through M18 G1 sprint entry

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-069 | New output directories covered by `.gitignore` in same PR | Yes — `backend/test-results/` and `frontend/test-results/` already in `.gitignore`; §6.3a confirmed |
| NM-070 | Pre-push hook enforcing ruff + mypy + npm build | Yes — `.githooks/pre-push` active; step 9 of §4 implementation sequencing requires both gates exit 0 |
| NM-071 | Wave concurrency ceiling check at wave kickoff | Yes — 2 concurrent groups (G1 + G2) = Standard tier; recorded in §1 |
| NM-068 | Prior NM verification field in sprint entry | Yes — this section (§6.5) |

---

## EL Approval Record

**EL approval:** 2026-06-26

> G1 sprint entry approved. ADR prerequisites confirmed (ADR-007 and ADR-017 both ACCEPTED). Sprint sub-branch `sprint/m18-g1` is live. Implementation PR may not open until: intent document filed at `docs/process/intents/M18-G1-2026-06-26-ci-bands-zone-1a.md`, UX mockup and UI mockup complete, 5-agent panel review ACCEPT recorded, and QA tests authored (red before implementation).
> — @PublicEnemage (2026-06-26)
