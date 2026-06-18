---
name: m14-g6-sprint-entry
type: sprint-entry
milestone: M14 — Methodology Publication and External Validation
sprint-group: G6
status: Filed — awaiting EL approval
authored-by: PM Agent
authored-date: 2026-06-18
el-approved: false
release-branch: release/m14
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M14, G6: Methodology, Calibration, and Instrument Legibility

**Status:** Filed — awaiting EL approval before implementation begins
**Date authored:** 2026-06-18
**Release branch:** `release/m14`
**Sprint plan:** `docs/process/sprint-plans/m14-sprint-plan.md` (EL Approved 2026-06-16)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G6 is the methodology and calibration parallel group. It carries no ADR prerequisite
and no sequencing dependency on G3/G4/G5 — it may proceed in parallel. Issues addressed:
#22 (uncertainty quantification disclosure layer), #884 (reserve_coverage_months initial-state
surfacing), #885 (Exploratory tier label misclassification), #823 (ecological composite
denominator), #824 (MENA arid-economy water scarcity elasticity), #950 (Zone 1A Y axis label),
plus the PMM interpretation anchor (Chief Methodologist G5 parallel deliverable).*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M14 — Methodology Publication and External Validation |
| GitHub Milestone | #15 |
| Sprint group | G6 — Methodology, Calibration, and Instrument Legibility |
| Release branch | `release/m14` |
| Sprint plan document | `docs/process/sprint-plans/m14-sprint-plan.md` |
| Exit checklist issue | #968 |
| Sprint groups in scope | G6 only |
| ADR gate | None — no ADR required per sprint plan |
| Sequencing | Parallel — no dependency on G3/G4/G5 completion |
| Implementing agents | Data Architect Agent (DA-G6-1: indicator key for #824; DA-G6-2: seeding architecture for #884; api_contracts.yml authority); Chief Engineer Agent (backend implementation of #823, #824, #884 after DA decisions); Frontend Architect Agent (#885, #950); Chief Methodologist Agent (#22, PMM anchor, CM-G6-1: ecological tier floor) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G6.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m14` cut from `main` 2026-06-16
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed 2026-06-16 (Ruleset ID 17751852 with 6 required checks: `changes`,
  `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m14-sprint-plan.md`
  `el-approved: 2026-06-16`

### 2.2 — ADR prerequisite gate

G6 requires no ADR. All items are standalone fixes, calibration updates, and documentation
deliverables within existing architectural boundaries:

- **#885** (Zone 1B negotiation label): modifies `getNegotiationLabel()` in `MDAAlertPanelZone1B.tsx`
  — presentation-only, within ADR-014 (Zone 1B persistent-detail) boundaries
- **#950** (Zone 1A Y axis): adds `label` prop to `<YAxis>` in `TrajectoryView.tsx` — no
  architectural change
- **#884** (reserve_coverage_months): adds display-name entry and/or source-registry attribution
  to ensure the indicator appears in `/initial-state` for JOR/EGY/ZMB entities — within ADR-016
  (Scenario Grounding) boundaries
- **#823** (ecological composite): corrects the `_boundary_proximity_strategy` denominator and
  `confidence_tier` derivation — within ADR-005 (ecological module) boundaries
- **#824** (MENA calibration): adds water scarcity elasticity entry to `ECOLOGICAL_ELASTICITY_REGISTRY`
  — within ADR-005 boundaries; Chief Methodologist + Ecological Economist already approved (2026-06-13)
- **#22** (confidence tier methodology): documentation deliverable — no architectural change
- **PMM anchor**: documentation deliverable — no architectural change

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G6 (all deliverables) | N/A | N/A | **CLEAR** |

- [x] No ADR required for any G6 deliverable.

### 2.3 — Intent document gate

*An intent document must be filed before any G6 implementation PR opens.
(Authority: CLAUDE.md §Agent Execution Lifecycle Step 1)*

- [x] Intent document filed for G6 deliverables — filed 2026-06-18 in same session as this entry

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| Zone 1B negotiation label fix (#885) | ADR-014 §Zone 1B presentation | `docs/process/intents/M14-G6-2026-06-18-methodology-calibration.md` | ✅ Filed 2026-06-18 |
| Zone 1A Y axis label (#950) | N/A | (same intent document) | ✅ Filed 2026-06-18 |
| reserve_coverage_months initial-state (#884) | ADR-016 §initial-state | (same intent document) | ✅ Filed 2026-06-18 |
| Ecological composite fix (#823) | ADR-005 §ecological | (same intent document) | ✅ Filed 2026-06-18 |
| MENA water scarcity calibration (#824) | ADR-005 Amendment (CM+EE approved 2026-06-13) | (same intent document) | ✅ Filed 2026-06-18 |
| Confidence tier methodology doc (#22) | N/A | (same intent document) | ✅ Filed 2026-06-18 |
| PMM interpretation anchor | ADR-015 §Component 1 (placeholder) | (same intent document) | ✅ Filed 2026-06-18 |

**Intent document completeness gate:** The QA Lead must be able to write Playwright E2E tests
(frontend) and pytest tests (backend) from every acceptance criterion without reading implementation
source code. For G6 specifically:

- **Zone 1B label tests** (#885): route-mock the trajectory/MDA response to inject T4/T5
  confidence tiers; assert exact string content of `[data-testid="alert-negotiation-label"]`
  (or equivalent). NM-045 rule applies: string assertions, not structural regex.
- **Zone 1A Y axis test** (#950): load any completed scenario at 1280×900; assert Zone 1A
  chart contains a visible Y axis label element with non-empty text.
- **Backend tests** (#884, #823, #824): pytest + httpx against the real test database; the
  implementing agent specifies exact fixture scenarios in the intent document.
- **Documentation tests** (#22, PMM anchor): Business PO validates via 5-minute navigation test —
  these do not require automated tests.

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before implementation
code is written. (Authority: CLAUDE.md §Agent Execution Lifecycle Step 2)*

- [x] QA test files authored before any implementation PR is opened — **FILED 2026-06-18**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| Zone 1B label fix (#885) | `docs/process/intents/M14-G6-2026-06-18-methodology-calibration.md` | `frontend/tests/e2e/m14-g6-methodology-calibration.spec.ts` | ✅ Yes — authored 2026-06-18 before implementation PR (guard pattern; NM-045 rule applied; AC-1/AC-2/AC-3/AC-4 covered) |
| Zone 1A Y axis (#950) | (same intent document) | (same test file) | ✅ Yes — authored 2026-06-18 before implementation PR |
| Backend fixes (#884, #823, #824) | (same intent document) | `backend/tests/test_m14_g6_methodology_calibration.py` | ✅ Yes — authored 2026-06-18 before implementation PR; AC-5/AC-6/AC-7/AC-8 + AC-9 partial file-existence check |
| Documentation (#22, PMM anchor) | (same intent document) | BPO 5-min navigation test at Step 5 | No automated test; BPO validates at Validate step (AC-9 full) |

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Implementing agent |
|---|---|---|---|
| #885 | Zone 1B negotiation label — "Exploratory" misclassification (T4/T5) | immediate | Frontend Architect Agent |
| #950 | Zone 1A Y axis label absent | immediate | Frontend Architect Agent |
| #884 | reserve_coverage_months not appearing in /initial-state for JOR/EGY/ZMB | immediate | Chief Engineer Agent |
| #823 | Ecological composite denominator fix (CM-approved constraints) | immediate | Chief Engineer Agent |
| #824 | MENA arid-economy water scarcity elasticity −0.04 (CM+EE approved) | immediate | Chief Engineer Agent |
| #22 (M14 scope only) | Confidence tier disclosure layer — methodology documentation | immediate | Chief Methodologist Agent |
| PMM anchor | PMM interpretation anchor — Chief Methodologist deliverable (G5 out-of-scope) | immediate | Chief Methodologist Agent |

### 3.2 — Items explicitly out of scope

| Item | Rationale for exclusion |
|---|---|
| #22 — full distributional bands (CI intervals) | Deferred to M16 per sprint plan HORIZON note. M14 scope is methodology documentation only (how tiers are assigned), not Monte Carlo CI computation. |
| PMM calibration completion | The interpretation anchor documents the pre-calibration status and methodology. Full calibration completion and ADR-007 authorship are post-M14. The `[T3 composite · pre-cal]` placeholder in Zone 1C remains until calibration is complete. |
| Ecological directionality schema fix (Option B for G5) | M15 scope per EL Decision 2 (2026-06-16). G5 implements static Option A mapping. |
| Water stress indicator seeding for all entities beyond GRC/JOR/EGY/ZMB | M14 entity scope is ADR-016 §EL Decision 1: GRC, JOR, EGY, ZMB. Other entities receive no new ecological calibration in G6. |
| Zone 1A redesign (#845) | G6c scope — design-only; Phases 2–4 in M15/M16. G6 delivers only the Y axis label fix (#950), not any layout change. |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G6 (all deliverables) | N/A | N/A | **After EL approval of this entry document** |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-18
**Sweep period:** G5 sprint entry approval (2026-06-17) through G6 sprint entry filing (2026-06-18)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified in this period. G5 implementation (Step 3) is in progress (PR #1030 merged). NM-045 and NM-046 were filed in G5 sprint entry. | N/A | N/A | N/A |

---

## EL Approval Record

**EL approval:** Pending

> {EL approval statement — to be filled at approval time}
> — @PublicEnemage ({date})
