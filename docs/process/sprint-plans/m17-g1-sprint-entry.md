---
name: m17-g1-sprint-entry
type: sprint-entry
milestone: M17 — Calibration and Comparative Infrastructure
sprint-group: G1
status: EL Approved 2026-06-25 — CM may begin research; implementation PR requires calibration decision document + FRAME-D test first
authored-by: PM Agent
authored-date: 2026-06-25
el-approved: 2026-06-25
release-branch: release/m17
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M17, G1: Chief Methodologist Calibration Sprint

**Status:** EL Approved 2026-06-25 — Wave 1 begins
**Date authored:** 2026-06-25
**Release branch:** `release/m17`
**Sprint plan:** `docs/process/sprint-plans/m17-sprint-plan.md` (EL Approved 2026-06-25)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G1 — the Wave 1 hard entry gate for M17. No Wave 2 implementation
sprint entry may open until G1 exits with Wave 1 exit gate confirmed by PI Agent.
No G1 implementation PR may open until this entry document is EL-approved.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M17 — Calibration and Comparative Infrastructure |
| GitHub Milestone | #18 |
| Sprint group | G1 — CM Calibration Sprint (Wave 1) |
| Release branch | `release/m17` |
| Sprint plan document | `docs/process/sprint-plans/m17-sprint-plan.md` |
| Exit checklist issue | #982 |
| Sprint groups in scope | G1 only |
| ADR gate | N/A — calibration research; no new architectural decision required |
| Implementing agent | Chief Methodologist |
| Wave | Wave 1 (**hard entry gate** — no Wave 2 implementation sprint entry may open until G1 exits) |
| CM activation recorded | ✅ #1229 activated 2026-06-25; #1248 activated 2026-06-25 |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any G1 implementation PR (ELASTICITY_REGISTRY code change) opens.
CM research and deliberation work may proceed after EL approval of this document.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m17` cut from `main` 2026-06-25 (commit d806957)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at M17 kickoff 2026-06-25. Ruleset ID 17751852 with 6 required checks:
  `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
  KI-005 permanent fix (`do_not_enforce_on_create: true`) applied 2026-06-20 — no Ruleset
  workaround required.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m17-sprint-plan.md`
  `el-approved: 2026-06-25` (recorded 2026-06-25, PR #1264 merged)

### 2.2 — ADR prerequisite gate

G1 is a calibration research sprint. The ELASTICITY_REGISTRY update is a constant revision
within the existing DemographicModule architecture — no new architectural decision is required.
The governance sensitivity specification is a CM-authored document; if implementation proceeds
in Wave 2, the Architect will determine at that point whether an ADR amendment is required.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G1 — #1229 (ELASTICITY_REGISTRY calibration) | N/A — constant revision within existing module | N/A | **CLEAR** |
| G1 — #1248 (governance sensitivity specification) | N/A — specification document; Wave 2 implementation may require ADR assessment | N/A | **CLEAR** |

- [x] No ADR prerequisites for G1. Gate: **CLEAR**.

### 2.3 — Intent document gate

G1 is a calibration sprint with two deliverables:

**#1229 — Fiscal-to-cohort elasticity calibration (code change):** The CM calibration decision
document serves as the intent equivalent. It must be filed before the implementation PR (the
ELASTICITY_REGISTRY code change) opens. The document must specify: the chosen calibration path
with citations, updated ELASTICITY_REGISTRY constants with uncertainty ranges, and the FRAME-D
acceptance criterion (Q1 `poverty_headcount_ratio` delta range per step under Senegal T3
conditionality shock). Observable application state: the FRAME-D backend integration test passes
in CI.

**#1248 — Governance sensitivity calibration (specification document):** The CM-authored
governance sensitivity specification is both the deliverable and the intent equivalent. It must
be filed before any Wave 2 implementation work on governance calibration opens. No code change
is required in Wave 1 for #1248.

- [ ] CM calibration decision document filed before #1229 implementation PR opens (gate: PENDING — document authored during G1 work; this entry records the precondition)
- [x] #1248 governance sensitivity specification: document-only deliverable for Wave 1; intent gate not applicable to specification documents

| Deliverable | ADR reference | Intent document equivalent | Gate |
|---|---|---|---|
| #1229 — ELASTICITY_REGISTRY calibration | N/A | CM calibration decision document (to be filed by CM before implementation PR) | PENDING — filed during G1 work |
| #1248 — Governance sensitivity specification | N/A | The specification document IS the deliverable — no separate intent document | CLEAR — document-only deliverable |

### 2.4 — QA test authorship gate

**#1229 — FRAME-D integration test:**

The QA artifact for the ELASTICITY_REGISTRY change is a backend integration test that asserts:
Q1 `poverty_headcount_ratio` delta per step is within the CM-certified range under the
Senegal T3 Article IV conditionality shock (100-step quarterly resolution, SEN scenario).
The test must be authored from the CM calibration decision document and must pass in CI before
the implementation PR merges.

File: `backend/tests/test_m17_g1_frame_d_calibration.py` (or equivalent path determined by CM)

- [ ] FRAME-D integration test authored before implementation PR merges (gate: PENDING — test authored by CM alongside calibration code change)

**#1248 — Governance sensitivity specification:**

Specification document only. No QA test is required at Wave 1. If implementation proceeds in
Wave 2, a backend integration test for governance transmission will be specified in the Wave 2
sprint entry.

- [x] #1248: specification-only deliverable at Wave 1; QA test gate not applicable

| Deliverable | Test file path | Gate |
|---|---|---|
| #1229 — ELASTICITY_REGISTRY calibration | `backend/tests/test_m17_g1_frame_d_calibration.py` | PENDING — authored by CM before implementation PR merges |
| #1248 — Governance sensitivity specification | N/A — specification only at Wave 1 | CLEAR |

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state |
|---|---|---|---|
| #1229 | feat(simulation): fiscal-to-cohort elasticity calibration — DemographicModule ELASTICITY_REGISTRY revision | immediate / Wave 1 entry gate | FRAME-D integration test passes in CI: Q1 `poverty_headcount_ratio` delta per step is within CM-certified range under Senegal T3 Article IV conditionality shock. CM calibration decision document on record with citations. Three possible outcomes are all valid — the exit gate closes on a written, citable decision with updated constants, not on any specific calibration result. |
| #1248 | feat(simulation): governance sensitivity calibration — GovernanceModule fiscal conditionality transmission | immediate / Wave 1 | CM-authored governance sensitivity specification document on record: recommended constants with source citations, position on whether implementation proceeds in M17 Wave 2 or M18, specification of minimum step window for visible governance divergence. |

### 3.2 — Issues explicitly out of scope

G1 scope is bounded to the two CM calibration deliverables. The following are explicitly excluded:

| Issue / scope | Rationale for exclusion |
|---|---|
| #394 — Multi-scenario comparison (G2) | Wave 2; implementation gated on Wave 1 exit + design phases complete |
| #1249/#1250/#1253 — DEMO6 CRITICAL polish (G4) | Wave 2; implementation gated on Wave 1 exit + UX visual specs |
| #1252 — Zone 1B proportional allocation (G3) | Wave 2; implementation gated on Wave 1 exit + ADR |
| #1220/#1214 — infrastructure fixes (G5) | Wave 2; capacity-allowing after Wave 1 exit |
| #1251 — adaptive y-axis extension audit (G5) | Wave 2; capacity-allowing |
| Any frontend changes | G1 is CM research and backend calibration only |
| GovernanceModule implementation (#1248) | Wave 1 deliverable for #1248 is specification only; implementation is Wave 2 scope |

G1 is complete when: FRAME-D integration test passes in CI with CM-certified constants; CM calibration decision document is on record for #1229; CM governance sensitivity specification is on record for #1248. Business PO acceptance and Customer Agent Layer 3 assessment are not required for G1 (calibration research sprint — no new user-visible capability; simulation outputs change but no new UI element is delivered).

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G1 — #1229 (ELASTICITY_REGISTRY calibration) | None | N/A | Yes — after EL approves this entry document and CM calibration decision document is filed |
| G1 — #1248 (governance sensitivity specification) | None | N/A | Yes (specification work) — specification is the Wave 1 deliverable; code implementation not in G1 scope |

**Implementation sequencing for G1:**

1. EL approves this entry document
2. CM conducts research: investigates three calibration paths for #1229; addresses three governance questions for #1248
3. CM authors calibration decision document for #1229 — citable conclusion with updated ELASTICITY_REGISTRY constants and FRAME-D acceptance criterion
4. CM authors governance sensitivity specification for #1248 — recommended constants, implementation timeline position, step-window analysis
5. CM authors FRAME-D integration test (`backend/tests/test_m17_g1_frame_d_calibration.py`) from the calibration decision document
6. CM opens implementation PR targeting `release/m17` with branch `feat/m17-g1-elasticity-calibration`: updates ELASTICITY_REGISTRY constants, adds FRAME-D integration test
7. CI passes: FRAME-D test passes; `ruff check .` and `mypy app/` pass (pre-push lint gate)
8. PI Agent confirms Wave 1 exit gate: FRAME-D test confirmed, calibration decision document on record, governance sensitivity specification on record
9. G1 sprint exit document filed; Wave 1 exit confirmed

**Wave 2 gate dependency:** No Wave 2 implementation sprint entry may open until PI Agent confirms the Wave 1 exit gate at step 8.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-25
**Sweep period:** M16 exit ceremony (2026-06-25) through M17 G1 sprint entry filing (2026-06-25)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified in the sweep period. M16 exit ceremony and M17 kickoff completed in the same session without deviations from SOP. All insights log entries 8–12 dispositioned at HORIZON sweep 2026-06-25. CM activation on #1229 and #1248 confirmed before sprint entry filing (meeting the §G1 Additional Requirement in the sprint plan). | N/A | N/A | N/A |

---

## EL Approval Record

**EL approval:** 2026-06-25

> G1 sprint entry approved. Structural gates confirmed clear: release/m17 cut, CI trigger verified, sprint plan EL-approved. ADR gates clear for both issues (calibration constant revisions within existing module architecture — no new ADR required). CM activation confirmed on #1229 and #1248 before filing. Calibration decision document and FRAME-D integration test must be filed and passing before the ELASTICITY_REGISTRY implementation PR opens — these remain blocking conditions for the code change. Governance sensitivity specification (#1248) is the Wave 1 document deliverable; implementation carries to Wave 2. Wave 2 implementation sprint entries may not open until PI Agent confirms the Wave 1 exit gate (FRAME-D pass + calibration decision document on record + governance specification on record).
> — @PublicEnemage (2026-06-25)
