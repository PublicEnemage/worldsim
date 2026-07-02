---
name: m19-g2b-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G2 Phase B — SEN + ZMB Calibration Fixtures
status: EL-approved 2026-07-02
authored-by: PM Agent
authored-date: 2026-07-02
el-approved: 2026-07-02
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19, G2 Phase B: SEN + ZMB Calibration Fixtures

**Status:** EL-approved 2026-07-02 — implementation may begin
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
| Sprint number | 3 (G2 Phase B) |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md` |
| Exit checklist issue | #1535 |
| Sprint groups in scope | G2 Phase B (#1541, #1542) |
| Wave coordination tier | Standard — G1 and G2B concurrent; disjoint file areas |
| Concurrent groups at entry | 2 of 5 max — G1 (entry filed, EL approval pending); G2B (this entry) |
| Cross-group dependencies | G2B depends on G2A (harness): SATISFIED — PR #1568 merged to sprint/m19-g2 on 2026-07-02 |

### Wave kickoff coordination fields (NM-071; sprint-planning-sop.md §Wave Kickoff Coordination Check)

**Groups active at G2B entry (Wave 1):**

| Group | Primary implementation domain | Shared-file write scope |
|---|---|---|
| G1 (#1540) | Frontend (`ControlPlaneColumn.tsx`) + Backend (constraint-floor endpoint, `backend/app/simulation/`) | `SESSION_STATE.md` at exit only |
| G2B (#1541, #1542) | Backend only (`backend/tests/backtesting/`, `backend/tests/fixtures/`) | `SESSION_STATE.md` at exit only |

**Cross-group dependency graph:**
- G1 has no dependency on G2B.
- G2B has no dependency on G1.
- G2B has an intra-group dependency on G2A (harness): SATISFIED — `sprint/m19-g2` now contains `backend/app/harness/mode3_harness.py`.

**Coordination tier rationale:** Standard (2 concurrent groups). G1 and G2B have fully disjoint file areas. G1 writes frontend components and backend simulation engine; G2B writes only test and fixture files. No merge conflicts anticipated. Shared-state updates deferred to sprint exit via PM Agent coordination lane.

**Scope lock precondition (NM-081):** Confirmed CLEAR — see Section 3.0.

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for this sprint.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` cut from `main` at milestone kickoff 2026-07-02 at commit 1bf1ecc
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` (verified at M19 sprint plan filing 2026-07-02; covers `sprint/m*` as well)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m19-sprint-plan.md` EL-approved 2026-07-02

### 2.2 — ADR prerequisite gate

G2 Phase B has no ADR prerequisite. See Section 4 for reasoning. N/A check:

- [x] All groups with `BLOCKED_ADR` status in the sprint plan have their required ADR accepted — G2B carries no `BLOCKED_ADR` status (N/A)

**ADR prerequisite status:**

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G2 Phase B | None | N/A | CLEAR |

**Chief Methodologist consultation — pre-merge condition (not pre-entry):**
Per `docs/process/sprint-plans/m19-sprint-plan.md §Wave 1`: "Chief Methodologist sign-off on fidelity thresholds before fixtures enter CI." This is a required review before each fixture's feature PR merges to `sprint/m19-g2` — not before the sprint entry is approved. G2B implementation may begin without the consultation record; feature PRs may not merge without it. The Computation Engine Agent must activate the Chief Methodologist before opening the SEN and ZMB PRs.

### 2.3 — Intent document gate

G2 Phase B is **not** an infrastructure sprint. SEN and ZMB calibration fixtures are user-facing analytics artifacts: they constitute the empirical calibration base that grounds CI intervals displayed to finance ministry analysts in Demos and in production (ADR-007 Bayesian posterior gate, G3). Intent documents are required.

- [x] Intent document filed for every user-facing deliverable in this sprint

**Intent document status:**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| SEN backtesting fixture (#1541) | N/A | `docs/process/intents/M19-G2B-2026-07-02-sen-backtesting-fixture.md` | Yes — filed 2026-07-02 |
| ZMB backtesting fixture (#1542) | N/A | `docs/process/intents/M19-G2B-2026-07-02-zmb-backtesting-fixture.md` | Yes — filed 2026-07-02 |

### 2.4 — QA test authorship gate

- [x] QA test file authored for every user-facing deliverable in this sprint

**QA test status:**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| SEN backtesting fixture (#1541) | `docs/process/intents/M19-G2B-2026-07-02-sen-backtesting-fixture.md` | `backend/tests/backtesting/test_m19_g2b_sen_fixture.py` | Yes — filed 2026-07-02 |
| ZMB backtesting fixture (#1542) | `docs/process/intents/M19-G2B-2026-07-02-zmb-backtesting-fixture.md` | `backend/tests/backtesting/test_m19_g2b_zmb_fixture.py` | Yes — filed 2026-07-02 |

*NM-078 compliance: test files placed at `backend/tests/backtesting/` — CI-discoverable path.*
*NM-056 rule: NO pytest.skip() or soft-skip patterns in the structural test bodies. Tests fail RED (ImportError on fixture module) until fixture functions are implemented.*

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation (NM-081; sprint-planning-sop.md §Scope lock precondition)

- [x] All ADR decisions affecting this sprint's scope are EL-approved and merged to `release/m19`

G2B has no ADR dependency. The harness infrastructure it depends on is now on `sprint/m19-g2` (PR #1568 merged 2026-07-02). The Chief Methodologist fidelity threshold consultation is a pre-merge condition (§2.2), not a scope lock precondition — fixture structure is fully specified in the intent docs regardless of which fidelity tier the CM endorses. **CLEAR.**

**Scope uncertainty:** None at entry. The exact fidelity tier assertion in each fixture (`DIRECTION_ONLY` vs `MAGNITUDE_MATCH`) is determined by the Chief Methodologist review before each feature PR merges. The QA test files gate on `fidelity_tier in {DIRECTION_ONLY, MAGNITUDE_MATCH}` (floor-based assertion) to remain valid across both outcomes.

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1541 | SEN backtesting fixture (Senegal) — Type A harness run + CI gate | G2 Phase B | High — Bayesian posterior gate (#1543) |
| #1542 | ZMB backtesting fixture (Zambia) — Type A harness run + CI gate | G2 Phase B | High — Bayesian posterior gate (#1543) + Demo 8 Act 2 credibility |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Horizon | Rationale for exclusion |
|---|---|---|---|
| #1543 | ADR-007 Bayesian posterior layer | G3 Wave 2 | Blocked by G2B; requires SEN+ZMB fidelity data on `sprint/m19-g2` first |
| #1547 | Greece 2010–15 counter-factual Type B | G2C | Depends on G2A harness; separate sprint entry |
| #1548–1552, #1554 | Remaining Phase C scenarios | G2C | Depend on G2A harness; separate sprint entries |
| #1553 | Iceland 2008–11 | G2D | Blocked by #1532 (capital controls gap) |
| #1540 | Mode 3 constraint-floor search | G1 | Separate sprint group |

---

## Section 4 — ADR Prerequisite Summary

G2 Phase B does not require a new ADR or an amendment to any existing ADR.

**Reasoning:** G2B introduces two calibration fixtures using the harness produced by G2A. The fixture structure — a `build_XXX_scenario()` function + `run_harness()` call + fidelity tier assertion — is pure test/fixture infrastructure that calls the existing harness API. No new simulation engine capabilities, endpoints, or architectural decisions are introduced. The fidelity tier classification logic is already in `app.harness.mode3_harness` (G2A). The Chief Methodologist consultation (§2.2) governs the threshold value decision, which is a data quality question, not an architectural question.

ADR-007 Bayesian posterior amendments are authored in G3 after SEN and ZMB fidelity data is available to calibrate the posterior.

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G2 Phase B | None | N/A | Yes — once intent documents (§2.3) and QA tests (§2.4) are filed and EL approval is recorded |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-02
**Sweep period:** Since G2A entry (2026-07-02) — same-day filing; all NM entries through NM-083 in scope.

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| Conftest global session skip prevented G2A unit tests from running without DATABASE_URL; fixed by yielding without pool instead of skipping | process gap — conftest design | No — fixed in G2A PR #1568 without requiring a new NM entry (NM-078 root cause covered; this is a variant) | N/A (resolved in-session) |
| No new process gaps identified for G2B scope since G2A entry | N/A | N/A | N/A |

*Prior NM applicability review in Section 6.5.*

---

## Section 6 — Sprint Group Isolation (M18 onward)

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m19-g2` |
| Branch status | **Already exists** — cut at G2A entry (2026-07-02); G2A harness PR #1568 merged |
| Cut from | `release/m19` (original cut) |
| Sprint journal issue | TBD — PM Agent creates at EL approval |

**Branch lifecycle note (from G2A sprint entry §6.1):** `sprint/m19-g2` serves all G2 phases (A, B, C, D). It is not re-cut here. G2B feature branches are cut from the current tip of `sprint/m19-g2` (which now includes the harness module). The integration PR (`sprint/m19-g2` → `release/m19`) is filed only at the close of the final G2 phase, after PI Agent exit confirmation.

**Feature branch cut commands for G2B implementing agent:**
```bash
# SEN fixture
git checkout -b feat/m19-g2b-sen-fixture sprint/m19-g2

# ZMB fixture (sequential after SEN — or parallel with separate feature branches)
git checkout -b feat/m19-g2b-zmb-fixture sprint/m19-g2
```

### 6.2 — File-conflict risk assessment

G2B writes only new test and fixture files. No shared state files or DS-owned files are touched during implementation.

| File | Lane required | Trigger |
|---|---|---|
| `backend/tests/fixtures/sen_scenario.py` (new) | Sprint sub-branch — no coordination needed | — |
| `backend/tests/fixtures/zmb_scenario.py` (new) | Sprint sub-branch — no coordination needed | — |
| `backend/tests/backtesting/test_m19_g2b_sen_fixture.py` (new — QA shell filed) | Sprint sub-branch — no coordination needed | — |
| `backend/tests/backtesting/test_m19_g2b_zmb_fixture.py` (new — QA shell filed) | Sprint sub-branch — no coordination needed | — |
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update only |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | Only if NM identified during implementation |

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

G2B introduces no changes to `.github/workflows/`, `.githooks/`, or `.gitignore`. Fixture files write to repository-tracked `backend/tests/fixtures/` (already tracked).

#### 6.3a — New output paths declaration (NM-069 process improvement)

- [x] No new output directories — fixture and test files write to existing tracked paths; `.gitignore` unchanged

### 6.4 — Cross-group dependency declaration

- [x] G2B has a SATISFIED intra-sprint dependency on G2A

**G2A dependency (SATISFIED):**
G2B depends on `app.harness.mode3_harness` module produced by G2A (#1546). This module is now on `sprint/m19-g2` (PR #1568, merged 2026-07-02). The QA test files import `run_harness`, `FidelityTier`, and `RunType` from `app.harness.mode3_harness` — these imports are GREEN as of this sprint entry filing. The only RED imports in the QA files are the fixture functions (`build_sen_scenario`, `build_zmb_scenario`) which are implemented in G2B itself.

**No cross-group dependency on G1:** G2B is independent of G1.

### 6.5 — Prior NM verification (NM-068 process improvement)

**NM verification sweep date:** 2026-07-02
**Sweep period:** All NM entries through NM-083

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-075 | Git worktrees allocated per sprint group | Yes — implementing agent must use dedicated worktree for `sprint/m19-g2` G2B feature branches |
| NM-076 | Before any testid rename, grep full E2E corpus for old testid | N/A — G2B is backend-only; no testids introduced or renamed |
| NM-077 | `gh pr create` must specify `--head <branch>` explicitly | Yes — implementing agent must pass `--head feat/m19-g2b-{sen,zmb}-fixture` when opening PRs |
| NM-078 | Milestone test files must be in CI-discoverable path (`backend/tests/backtesting/`) | Yes — test files placed at `backend/tests/backtesting/` per §2.4 |
| NM-079 | Confirm active branch before committing | Yes — implementing agent must verify `git branch` before every commit on the worktree |
| NM-080 | No direct commits to `release/m19` | Yes — all G2B work targets `sprint/m19-g2` via feature branches |
| NM-081 | Sprint branch must not be cut before predecessor ADR scope finalized | N/A — G2B has no ADR dependency; `sprint/m19-g2` already exists |
| NM-082 | CI band fill geometry error (UI-specific) | N/A — G2B is backend-only |
| NM-083 | Demo-spec ↔ component-contract integration gap (UI-specific) | N/A — G2B is backend-only |

---

## EL Approval Record

*EL reviews this entry document before any implementation PR opens. Approval is recorded here
or as a comment on the exit checklist issue #1535.*

**EL approval:** Approved 2026-07-02

> G2 Phase B sprint entry approved. All five entry conditions confirmed: release branch
> exists and CI trigger verified; sprint plan EL-approved; no ADR prerequisite (Chief
> Methodologist consultation is a pre-merge condition on each fixture PR, not a pre-entry
> gate); intent documents filed at `docs/process/intents/M19-G2B-2026-07-02-sen-backtesting-fixture.md`
> and `docs/process/intents/M19-G2B-2026-07-02-zmb-backtesting-fixture.md`; QA test
> shells authored at `backend/tests/backtesting/test_m19_g2b_sen_fixture.py` and
> `backend/tests/backtesting/test_m19_g2b_zmb_fixture.py` before implementation begins.
> G2A dependency SATISFIED (PR #1568 merged to `sprint/m19-g2` 2026-07-02).
> `sprint/m19-g2` already exists — G2B feature branches may be cut from its current tip.
> — @PublicEnemage (2026-07-02)
