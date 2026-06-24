---
name: m16-g9-sprint-entry
type: sprint-entry
milestone: M16 — Distributional Visibility
sprint-group: G9
status: EL Approved 2026-06-24 — work may begin per sequencing in §4
authored-by: PM Agent
authored-date: 2026-06-24
el-approved: 2026-06-24
release-branch: release/m16
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M16, G9: Near-term Backlog

**Status:** EL Approved 2026-06-24 — work may begin per sequencing in §4
**Date authored:** 2026-06-24
**Release branch:** `release/m16`
**Sprint plan:** `docs/process/sprint-plans/m16-sprint-plan.md` (EL Approved 2026-06-23; amended 2026-06-24 to add G9)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G9 is a Wave 3 capacity-allowing sprint group. All four issues were carried on the M16
milestone as a deferred near-term backlog; this entry formalises them as sprint group G9
per the sprint plan amendment of 2026-06-24. G9 is not on the Demo 6 critical path and
must not be allowed to delay G1–G6 or G8. Carry all four issues to M17 without penalty
if capacity is exhausted before G8 is scheduled.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M16 — Distributional Visibility |
| GitHub Milestone | #17 |
| Sprint group | G9 — Near-term Backlog |
| Release branch | `release/m16` |
| Sprint plan document | `docs/process/sprint-plans/m16-sprint-plan.md` |
| Exit checklist issue | #985 |
| Sprint groups in scope | G9 only |
| ADR gate | None |
| Implementing agents | Frontend Developer (#153, #846); Backend/API Developer (#97); Data Engineer (#92) |
| Wave | Wave 3 — capacity-allowing; parallel with G4/G6; subordinate to G1–G6 and G8 |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any G9 implementation PR is opened.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m16` cut from `main` 2026-06-23 (commit 07c92b8)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at kickoff 2026-06-23 (line 5: `branches: [ main, develop, release/m* ]`;
  line 7: `branches: [ main, release/m* ]`). Ruleset ID 17751852 with 6 required checks:
  `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
  KI-005 permanent fix (`do_not_enforce_on_create: true`) applied 2026-06-20 — no Ruleset
  workaround required.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m16-sprint-plan.md`
  `el-approved: 2026-06-23` (PR #1148); amended 2026-06-24 to add G9.

### 2.2 — ADR prerequisite gate

G9 contains no items requiring a new ADR. All four issues are enhancements or fixtures within
existing component and module boundaries:

- **#153** — adds a visual overlay layer to the existing `DeltaChoropleth` component; the
  choropleth sits in the geographic context zone (Zone 1C / Zone 2), distinct from the Zone 1A
  and Zone 1D surfaces modified in G1/G2. No new zone is introduced; no architectural decision
  beyond the existing component's scope.
- **#846** — restores absent branch comparison values in Mode 3; Mode 3 interaction patterns
  are within the existing mode architecture; no new mode-level architectural decision required.
- **#97** — adds threshold-crossing markers as a new field in the existing compare API response;
  this is an API response extension within the established endpoint's scope; no new endpoint or
  module boundary.
- **#92** — adds a historical backtesting fixture (Greece 2010); fixture additions are explicitly
  excluded from ADR requirements (see sprint plan §ADR Prerequisites Summary).

| Issue | Required ADR | ADR status | Gate |
|---|---|---|---|
| #153 — DeltaChoropleth threshold overlay | None | N/A | **CLEAR** |
| #846 — Mode 3 branch comparison values | None | N/A | **CLEAR** |
| #97 — threshold-crossing markers in compare output | None | N/A | **CLEAR** |
| #92 — Greece 2010 backtesting fixture | None | N/A | **CLEAR** |

- [x] No ADR prerequisites for G9. Gate: **CLEAR**.

### 2.3 — Intent document gate

Three of four G9 issues produce user-facing application state visible to personas in the
running application: #153, #846, and #97. Intent documents are required for these three
before their implementation PRs open. #92 is a backtesting data fixture — not a user-facing
application surface; intent document not required.

**Intent document status:**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #153 — absolute threshold overlay on DeltaChoropleth | N/A | `docs/process/intents/M16-G9-2026-06-24-delta-choropleth-threshold-overlay.md` | ✅ FILED 2026-06-24 |
| #846 — Mode 3 branch comparison values | N/A | `docs/process/intents/M16-G9-2026-06-24-mode3-branch-comparison-values.md` | ✅ FILED 2026-06-24 |
| #97 — threshold-crossing markers in compare output | N/A | `docs/process/intents/M16-G9-2026-06-24-compare-threshold-crossing-markers.md` | ✅ FILED 2026-06-24 |
| #92 — Greece 2010 backtesting fixture | N/A | Infrastructure — not user-facing | Not required |

### 2.4 — QA test authorship gate

QA tests are required for the three user-facing deliverables (#153, #846, #97) and must be
authored from the intent document's acceptance criteria before implementation code is written.
#92 produces no Playwright E2E application state and no new backend API behavior requiring
a test file beyond the backtesting suite's existing fixture-loading coverage.

**QA test status:**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| #153 — DeltaChoropleth overlay | `docs/process/intents/M16-G9-2026-06-24-delta-choropleth-threshold-overlay.md` | `frontend/tests/e2e/m16-g9-delta-choropleth-overlay.spec.ts` | ⬜ NOT YET — **BLOCKING** |
| #846 — Mode 3 branch comparison | `docs/process/intents/M16-G9-2026-06-24-mode3-branch-comparison-values.md` | `frontend/tests/e2e/m16-g9-mode3-branch-comparison.spec.ts` | ⬜ NOT YET — **BLOCKING** |
| #97 — compare threshold-crossing markers | `docs/process/intents/M16-G9-2026-06-24-compare-threshold-crossing-markers.md` | `backend/tests/test_m16_g9_compare_threshold_markers.py` | ⬜ NOT YET — **BLOCKING** |
| #92 — Greece 2010 fixture | N/A | Covered by existing backtesting suite fixture loading | Not required |

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable state (pre-implementation specification) |
|---|---|---|---|
| #153 | feat(frontend): absolute threshold overlay on DeltaChoropleth | near-term / LOW | The `DeltaChoropleth` component renders a configurable absolute threshold overlay line or band (per the threshold values in the active scenario's MDA configuration) visible without opening a drawer or navigating away from the primary viewport. The overlay updates when the scenario or active step changes. Overlay is visually distinct from delta colouring and does not obstruct country labels. Toggling the overlay on/off does not cause a layout shift in adjacent zones. Full spec: `docs/process/intents/M16-G9-2026-06-24-delta-choropleth-threshold-overlay.md`. |
| #846 | ux: DEMO-045 — Mode 3 branch comparison values absent | near-term / LOW | In Mode 3, the branch comparison panel displays non-null comparison values for all configured branches at the current step. The values were previously absent (DEMO-045 finding). Observable state: a Mode 3 session with two or more branches shows numeric comparison values (not empty/placeholder text) for each branch in the comparison panel at every step. Full spec: `docs/process/intents/M16-G9-2026-06-24-mode3-branch-comparison-values.md`. |
| #97 | arch(api): threshold-crossing markers in compare output | near-term / LOW | The compare API endpoint includes a `threshold_crossings` field in its response for each entity-step pair, indicating which MDA thresholds were crossed at that step. The field is present and correctly populated for at least the active backtesting scenarios (Zambia ECF, Jordan ECF). Schema update to `docs/schema/api_contracts.yml` is included in the same PR. Full spec: `docs/process/intents/M16-G9-2026-06-24-compare-threshold-crossing-markers.md`. |
| #92 | arch(backtesting): Greece 2010 investment climate conditions | near-term / LOW | A Greece 2010 backtesting fixture is added to the backtesting suite with investment climate conditions sourced from approved-sources.md Tier 1 or Tier 2 data. The fixture passes the backtesting suite's validation checks. Source provenance is documented in the fixture metadata per `docs/DATA_STANDARDS.md §Backtesting Integrity`. |

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| #845, #1147 — Zone 1A Phase 4 + Zone 1D delta | G1 scope — CLOSED 2026-06-23 |
| #986, #987 — distributional surface | G2 scope — CLOSED 2026-06-24 |
| #274 — 25-year human capital trajectory | G3 scope — CLOSED 2026-06-24 |
| #102, #275, #22 — distributional infrastructure | G4 scope — CLOSED 2026-06-24 |
| #837, #951, #1145, #259 — process + secondary | G5 scope |
| #569 — accessibility + performance validation | G6 scope |
| #3, #6 — governance | G7 scope — EL-action |
| #843 — live stakeholder demo | G8 scope — M16 exit gate |
| #1162, #1177, #1178, #1179, #1184 — pre-demo polish | G10 scope — G8 gate condition; not capacity-allowing |
| Full Greece 2010 multi-module calibration sweep | #92 scope is investment climate conditions only; a complete Greece 2010 macro/fiscal/political calibration is a separate initiative if warranted |
| DeltaChoropleth threshold overlay design variants beyond the intent document specification | #153 scope is the single overlay type specified in the intent document; design variants are future work |
| Mode 3 branch management UI changes beyond comparison value display | #846 scope is the absent comparison value display fix; branch management architecture is separate |
| Full distributional compare API redesign | #97 scope is the `threshold_crossings` field addition only; a comprehensive compare API overhaul is separate |

---

## Section 4 — ADR Prerequisite Summary

| Issue | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| #153 — DeltaChoropleth overlay | None | N/A | **Yes — after EL approves this entry and intent document + test are filed (intent FILED 2026-06-24; test TBD); after G1 merges** |
| #846 — Mode 3 branch comparison | None | N/A | **Yes — after EL approves this entry and intent document + test are filed (intent FILED 2026-06-24; test TBD); after G1 merges** |
| #97 — compare threshold-crossing markers | None | N/A | **Yes — after EL approves this entry and intent document + test are filed (intent FILED 2026-06-24; test TBD); after G2 merges (API contract stability)** |
| #92 — Greece 2010 fixture | None | N/A | **Yes — after EL approves this entry; no intent/test gate** |

**Implementation sequencing for G9:**

1. EL approves this entry document
2. Intent documents and QA tests filed for #153, #846, #97 (intents FILED 2026-06-24; QA tests must be authored before implementation opens)
3. **#92 (backtesting fixture):** May begin immediately after EL approval — no intent or QA test gate. Branch: `feat/m16-g9-greece-2010-fixture`. Merge autonomously after CI passes.
4. **#153 (DeltaChoropleth overlay):** After G1 merges to `release/m16` and after QA test is filed. Branch: `feat/m16-g9-choropleth-threshold-overlay`. Merge autonomously after CI passes.
5. **#846 (Mode 3 branch comparison):** After G1 merges to `release/m16` and after QA test is filed. Branch: `feat/m16-g9-mode3-branch-comparison`. Merge autonomously after CI passes.
6. **#97 (compare API threshold markers):** After G2 merges to `release/m16` and after QA test is filed (API contract must be stable). Branch: `feat/m16-g9-compare-threshold-markers`. Backend pre-push lint gate mandatory: `cd backend && ruff check . && mypy app/`. Schema update to `docs/schema/api_contracts.yml` in the same PR. Merge autonomously after CI passes.
7. All G9 PRs target `release/m16`. Poll CI until all checks are terminal (pass or skipped, none failed), then `gh pr merge <number> --merge`.

**Capacity gate:** If G1–G6 complete and G8 is scheduled with no implementation capacity remaining, carry all incomplete G9 issues to M17 with their intent documents and tests as pre-authored assets. Do not delay G8 for G9 completion.

**G8 gate dependency:** None — G9 completion is not a gate on G8 (#843 live stakeholder demo). G9 items may be in progress, complete, or deferred concurrently with G8 preparation.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-24
**Sweep period:** M16 G7/G5 sprint entry filing (2026-06-23) through G9 sprint entry filing (2026-06-24)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| Near-term backlog existed for one day as a deferred list without a formal sprint group number, sprint entry document, or sequencing dependency declarations. A deferred backlog with no sprint group is a scope tracking gap — issues have milestone assignments but no process home. Promoted to G9 and formalized in this entry. Root cause: sprint plan was authored at kickoff with near-term items explicitly held as a named deferred section; the promotion to a formal group was intentionally deferred until capacity picture clarified. No active implementation was blocked. Severity: LOW — the gap was named and visible, not hidden. | process gap — low severity | PI Agent register call: confirm whether this warrants a NM entry or falls below the NM threshold (named, visible, no blocked work, resolved same day). | TBD — PI Agent determination |

---

## EL Approval Record

**EL approval:** 2026-06-24

> G9 sprint entry approved. Structural gates confirmed clear — release branch exists, CI trigger verified, sprint plan EL-approved (amended 2026-06-24 to add G9). No ADR prerequisites for any G9 issue; gate is clear across the board. Classification accepted: #153, #846, #97 are user-facing and require intent documents and QA tests before their implementation PRs open; #92 (backtesting fixture) is infrastructure and neither gate applies. Sequencing noted and accepted: #92 may begin immediately; #153 and #846 after G1 merges; #97 after G2 merges. Capacity gate accepted: G9 is subordinate to G4 and G6 — all four issues carry to M17 without penalty if capacity is exhausted before G8 is scheduled. G9 is not a G8 gate dependency. Work may begin per §4 sequencing.
> — @PublicEnemage (2026-06-24)
