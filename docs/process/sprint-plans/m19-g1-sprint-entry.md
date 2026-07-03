---
name: m19-g1-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G1
status: EL-Approved
authored-by: PM Agent
authored-date: 2026-07-02
el-approved: 2026-07-02
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19, G1

**Status:** Filed — awaiting EL approval before implementation begins
**Date authored:** 2026-07-02
**Release branch:** `release/m19`
**Sprint plan:** `docs/process/sprint-plans/m19-sprint-plan.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
Changes to this template require PM Agent authorship and EL endorsement.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| GitHub Milestone | #21 |
| Sprint number | G1 |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md` |
| Exit checklist issue | #1535 |
| Sprint groups in scope | G1 |
| Wave coordination tier | Standard — G1 and G2 run in parallel with no shared file areas |
| Concurrent groups at entry | 1 of 5 max (G1 only; G2 sprint entry not yet filed) |
| Cross-group dependencies | None — G1 file areas (`ControlPlaneColumn.tsx`, `backend/app/api/scenarios.py`, `backend/app/simulation/`) do not overlap with G2 (`backend/scripts/` harness) |

---

## Section 2 — Entry Invariants Checklist

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` cut from `main` 2026-07-02 at 1bf1ecc
- [x] **CI trigger verified:** `.github/workflows/ci.yml` line 7 — `pull_request: branches: [main, 'release/m*', 'sprint/m*']` — covers both `release/m19` and `sprint/m19-g1`
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m19-sprint-plan.md` — `el-approved: 2026-07-02` (#1535 comment)

### 2.2 — ADR prerequisite gate

- [x] All groups with `BLOCKED_ADR` status in the sprint plan have their required ADR accepted

**ADR prerequisite status:**

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G1 | ADR-021 | **Accepted 2026-07-02** (EL: @PublicEnemage) | **CLEAR** |

ADR-021 was the sole ADR blocking G1. Accepted 2026-07-02. UX Designer sign-off on record (separate EL-triggered session, NM-042 compliant, 3 concerns resolved). UX Designer concern remediations reviewed and cleared by second UX Designer session 2026-07-02.

### 2.3 — Intent document gate

- [x] Intent document filed for every user-facing deliverable in this sprint

**Intent document status:**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| Mode 3 constraint-floor search (Form 3 + endpoint) | ADR-021 | `docs/process/intents/M19-ADR-021-2026-07-02-constraint-floor-search.md` | **Yes** |

### 2.4 — QA test authorship gate

- [x] QA test file authored for every user-facing deliverable in this sprint

**QA test status:**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| Form 3 frontend (AC-1–7, AC-11, AC-12, AC-016) | `docs/process/intents/M19-ADR-021-2026-07-02-constraint-floor-search.md` | `frontend/tests/e2e/m19-g1-constraint-floor-search.spec.ts` | **Yes — 2026-07-02** |
| Backend endpoint + binary search (AC-8–10) | same | `backend/tests/test_m19_g1_constraint_floor_search.py` | **Yes — 2026-07-02** |

All tests guard on implementation being present (no-op against pre-implementation codebase).

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation

- [x] All ADR decisions affecting this sprint's scope are EL-approved and merged to `release/m19`

ADR-021 accepted 2026-07-02 and merged to `release/m19`. All six ADR-021 decisions (D-1 through D-6) are locked. No open EL decisions affecting G1 scope.

**Scope uncertainty:** None.

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1540 | Mode 3 constraint-floor search | G1 | High — Demo 8 Act 1 |
| #1563 | AC-016: Form 3 column visibility CI assertion | G1 (pre-ship condition — same PR as #1540) | Pre-ship |
| #1564 | MV-001 three-way CVD validation (blue/orange/teal) | G1 (pre-ship condition — same PR as #1540) | Pre-ship |

Notes on #1563 and #1564: These are pre-ship conditions from the UX Designer sign-off on
ADR-021. They must be resolved in the same G1 PR as the Form 3 implementation — not
separate follow-on PRs. #1563 is satisfied when AC-016 in the test file passes. #1564 is
satisfied when the MV-001 CVD validation result is documented in the G1 PR description.

### 3.2 — Issues explicitly out of scope

| Issue | Title | Horizon | Rationale for exclusion |
|---|---|---|---|
| #1541 | SEN backtesting fixture | G2B Wave 1 | Separate sprint group; no shared file areas with G1 |
| #1542 | ZMB backtesting fixture | G2B Wave 1 | Same |
| #1543 | ADR-007 Bayesian posterior layer | G3 Wave 2 | Depends on G2B calibration data |
| #1536 | ADR-007 meaninglessness threshold | G3 Wave 2 | Same |
| #1537 | BandResult visible fields | G3 Wave 2 | Same |
| #1528 | PSP driver arc + auditability panel | G4 Wave 2–3 | Deferred to Wave 2 |
| #1529 | CI label precision fix | G4 Wave 2–3 | Same |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G1 | ADR-021 | **Accepted 2026-07-02** | **Yes** |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-02
**Sweep period:** Since M18 close (2026-07-02) — same day; no sprint has closed in this period

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new near-miss findings identified at G1 entry. Pre-wave near-miss sweep not required (pre-wave items are direct fixes, not sprint groups). | N/A | N/A | N/A |

---

## Section 6 — Sprint Group Isolation (M18 onward)

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m19-g1` |
| Cut from | `release/m19` |
| Sprint journal issue | TBD — PM Agent creates at EL approval |

**PM Agent sprint sub-branch cut command (execute after EL approval):**
```bash
git checkout -b sprint/m19-g1 release/m19 && git push -u origin sprint/m19-g1
```

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified during G1 |
| `docs/compliance/scan-registry.md` | PM Agent coordination lane | M19 compliance scan (post-G1) |
| `frontend/src/components/ControlPlaneColumn.tsx` | Sprint sub-branch | Form 3 implementation |
| `backend/app/api/scenarios.py` | Sprint sub-branch | New endpoint |
| `backend/app/simulation/` (new module) | Sprint sub-branch | Binary search algorithm |
| `backend/app/schemas.py` | Sprint sub-branch | Request/response schema |
| `frontend/tests/e2e/m19-g1-constraint-floor-search.spec.ts` | Sprint sub-branch | Already authored |
| `backend/tests/test_m19_g1_constraint_floor_search.py` | Sprint sub-branch | Already authored |
| `docs/ux/user-journeys.md` | PM Agent coordination lane (if further journey updates needed) | If G1 implementation reveals journey gaps |

**G1 does not overlap with G2:** G2 operates in `backend/scripts/` or `backend/app/harness/`; G1 in `backend/app/api/scenarios.py` and `backend/app/simulation/`. No merge conflicts anticipated.

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required for G1 base implementation

**Exception:** If MV-001 CVD validation (#1564) determines teal `#0d9488` must change to
an alternative value, `ControlPlaneColumn.tsx` color tokens will be updated in the G1 PR.
This is a code file change, not a DS-owned file change.

#### 6.3a — New output paths declaration

- [x] No new output directories — `backend/app/simulation/` is an existing directory; new module files are tracked by git

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies

G1 does not depend on G2, G3, or G4 outputs. G3 (Bayesian posterior, #1543) will later
add empirically grounded CI to the constraint-floor boundary result — but that is G3's
scope, not G1's. G1 ships search precision (±0.01) only.

### 6.5 — Prior NM verification

**NM verification sweep date:** 2026-07-02
**Sweep period:** Since M18 close

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-076 | Before any testid rename, grep the full E2E corpus for the old testid | N/A — G1 introduces new testids, does not rename existing ones |
| NM-075 | git worktrees must be allocated per sprint group | Yes — `sprint/m19-g1` sub-branch isolates G1 from other groups |
| NM-042 | UX Designer sign-off requires 4-field NM-042 attestation; same-session review must be disclosed | Yes — ADR-021 sign-off is NM-042 compliant (separate EL-triggered session) |

---

## EL Approval Record

*EL reviews this entry document before the sprint sub-branch is cut or any implementation PR opens.*

**EL approval:** 2026-07-02

> All five entry conditions satisfied. ADR-021 accepted. QA test scaffold filed and QA Lead-reviewed (PR #1569, 8 gaps corrected). Sprint sub-branch `sprint/m19-g1` is now authorized to cut.
> — @PublicEnemage (2026-07-02)
