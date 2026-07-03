---
name: m19-g2d-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G2 Phase D — Iceland 2008–11 Heterodox vs Orthodox Counter-Factual
status: Filed — awaiting EL approval
authored-by: PM Agent
authored-date: 2026-07-03
el-approved: false
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19, G2 Phase D: Iceland 2008–11 Backtesting Fixture

**Status:** Filed 2026-07-03 — awaiting EL approval before implementation begins
**Date authored:** 2026-07-03
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
| Sprint number | 5 (G2 Phase D — final G2 phase) |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md` |
| Exit checklist issue | #1535 |
| Sprint groups in scope | G2 Phase D (#1553) |
| Wave coordination tier | Standard — G2D is the only active implementation group at entry |
| Concurrent groups at entry | 1 of 5 max — G2D only; G3 integration merged 2026-07-03; G4 coordination gate cleared but not yet entered |
| Cross-group dependencies | None — G2D depends only on ADR-020 (ACCEPTED 2026-07-03) and `sprint/m19-g2` (existing) |

### Wave kickoff coordination fields

**Groups active at G2D entry (Wave 2):**

| Group | Primary implementation domain | Shared-file write scope |
|---|---|---|
| G2D (#1553) | Backend only (`backend/tests/backtesting/`, `backend/tests/fixtures/`, `backend/app/simulation/`) | `SESSION_STATE.md` at exit; `emergency-instrument-transmission-table.md` (CE audit); `docs/methodology/calibration-basis.md` (CM deliverable) |

**Coordination tier rationale:** Standard (1 active group). G4 is not yet entered — no concurrent file conflicts. G2D's file scope is backend test and fixture files plus simulation engine changes (ADR-020 channel implementation). Shared-state updates via PM Agent coordination lane at exit.

**Scope lock precondition (NM-081):** CLEAR — ADR-020 (ARCH-014) accepted 2026-07-03. No pending architectural decisions affect G2D scope.

---

## Section 1.5 — Integration PR Clause

G2D is the **final phase of the G2 wave.** At G2D exit, the PM Agent fires the integration PR:

```
sprint/m19-g2 → release/m19
```

This PR carries the cumulative G2 wave work: G2A (harness), G2B (SEN/ZMB fixtures),
G2C (7-country battle-testing suite), and G2D (Iceland heterodox/orthodox counter-factual).
The integration PR must not be opened until the PI Agent confirms all G2D exit conditions
are satisfied. Auto-merge is set immediately on PR open.

Authority: G2C sprint entry §1.5 (deferred integration PR clause); G2C sprint exit §1
(EL ruling: integration PR defers to G2D exit).

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for this sprint.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` cut from `main` at milestone kickoff 2026-07-02 at commit 1bf1ecc
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` (verified at M19 sprint plan filing 2026-07-02; covers `sprint/m*` as well)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m19-sprint-plan.md` EL-approved 2026-07-02

### 2.2 — ADR prerequisite gate

- [x] All groups with `BLOCKED_ADR` status have their required ADR accepted — **CLEARED: ADR-020 (ARCH-014) accepted 2026-07-03 (PR #1619, merged to `release/m19`)**

**ADR prerequisite status:**

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G2D — Iceland fixture (#1553) | ADR-020 (capital controls economic transmission) | **ACCEPTED 2026-07-03** | **CLEARED** |

**Note — pre-implementation PR gates (not sprint entry gates):**
Two additional conditions must be satisfied before the G2D **implementation PR** opens.
These do not block sprint entry or sprint journal issue creation — they block the first
feature branch PR only:

| Gate | Owner | Deliverable | Status |
|---|---|---|---|
| CM calibration deliverable | Chief Methodologist | `docs/methodology/calibration-basis.md §Capital Controls` — ε_controls_only, β=0.020 regression basis, φ validation, Malaysia 1998 cross-validation | PENDING |
| CE DemographicModule audit | Computation Engine Agent | All 10 EmergencyInstrument variants audited; near-miss entries for dead subscriptions; `emergency-instrument-transmission-table.md` updated | PENDING |

Both gates are CM/CE responsibilities. The implementing agent must confirm both are
satisfied before opening the Iceland implementation PR. If either gate is not satisfied
at implementation PR time, the PR must be held until cleared.

### 2.3 — Intent document gate

- [x] Intent document filed for every user-facing deliverable in this sprint

**Intent document status:**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| Iceland 2008–11 heterodox/orthodox fixture (#1553) | ADR-020 | `docs/process/intents/M19-G2D-2026-07-03-iceland-2008-backtesting-fixture.md` | **Yes — filed with this sprint entry** |

### 2.4 — QA test authorship gate

- [ ] QA test file authored for every user-facing deliverable in this sprint

**QA test status:**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| Iceland fixture (#1553) | `docs/process/intents/M19-G2D-2026-07-03-iceland-2008-backtesting-fixture.md` | `backend/tests/test_m19_g2d_iceland_scenario_runs.py` | **No — implementing agent authors before first implementation commit** |

*The test file follows the G2C pattern (`test_m19_g2c_scenario_runs.py`). Tests are
`@pytest.mark.backtesting` and skip without `DATABASE_URL`. Implementing agent authors
the test file before any fixture code is written (agent-execution-lifecycle Step 2).*

---

## Section 2.2 — Chief Methodologist Advisory (G2D new-entity attestation)

G2D introduces a new entity: **ISL (Iceland)**. Per the G2C sprint entry §2.2 CM advisory
process for new-country entries:

**CM advisory required before G2D implementation PR opens:**
- ISL reserve data tier classification (Central Bank of Iceland statistics — expected Tier 1)
- ISL baseline attributes quality tier (banking sector leverage ratio, reserve coverage, GDP, Q1 poverty headcount — all pre-October 2008 baseline)
- Synthetic inference status for any missing attributes
- Calibration notes for ε=0.50 (heterodox fixture, capital-controls-only, ADR-020 INCORPORATE-3)

This advisory is subsumed in the CM calibration deliverable listed in §2.2 above. CM must
confirm ISL data quality before the implementation PR opens.

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation (NM-081)

- [x] All ADR decisions affecting this sprint's scope are EL-approved and merged — **CLEARED: ADR-020 accepted and merged (PR #1619, 2026-07-03)**

**Scope uncertainty:** None. ADR-020 resolves all transmission channel design questions.
The counter-factual methodology (heterodox baseline vs. orthodox counter-factual) is
specified in issue #1553. No pending architectural decisions affect scope.

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1553 | Iceland 2008–11 fixture — heterodox vs orthodox counter-factual | G2D | Immediate — final G2 phase; Demo 8 Act 2 breadth argument |
| #1532 | Capital controls transmission gap | G2D (implementation) | Immediate — closes with G2D implementation PR |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Horizon | Rationale |
|---|---|---|---|
| #1528 | PSP driver arc + auditability panel | G4 | Separate sprint group — not entered yet |
| #1529 | CI label precision fix | G4 | Separate sprint group — coordination gate cleared; G4 entry follows G2D |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G2D (#1553, #1532) | ADR-020 (ARCH-014) | **ACCEPTED 2026-07-03** | **Yes** (subject to CM/CE pre-implementation PR gates) |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-03
**Sweep period:** Since G2C sprint closed (2026-07-03)

| Finding | Category | NM entry | Applicable to G2D? | Applied? |
|---|---|---|---|---|
| NM-087: Agent used `git stash --include-untracked` without authorization | near-miss | NM-087 | Yes — G2D uses the same working tree; stash prohibition applies | Applied: worktree isolation per NM-075 protocol; stash prohibited |
| NM-088: Parallel Claude Code sessions displace branch state | near-miss | NM-088 | Yes — G2D implementing agent must use `git worktree add /tmp/worldsim-g2d sprint/m19-g2` | Applied: worktree allocation required at sprint entry |
| NM-089: Shared-state file changes lost on branch switch before commit | near-miss | NM-089 | Yes — G2D implementation involves shared-state updates (calibration-basis.md, transmission table); these must be committed before any branch switch | Applied: shared-state file writes committed before switching; PM Agent coordination lane for SESSION_STATE.md |

**NM-075 worktree allocation (mandatory per NM-088):**
Implementing agent must allocate a named worktree at sprint entry — not at conflict time:
```bash
git worktree add /tmp/worldsim-g2d sprint/m19-g2
```

---

## Section 6 — Sprint Group Isolation

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m19-g2` |
| Status | **Existing — not recut** (cut at G2A entry; carries G2A + G2B + G2C work) |
| Integration PR | `sprint/m19-g2` → `release/m19` — fires at G2D exit (not at G2D entry) |
| Sprint journal issue | TBD — PM Agent opens after EL approval |

**Note:** `sprint/m19-g2` is the existing G2 wave branch. G2D feature branches target
`sprint/m19-g2`, not `release/m19`. The branch is at commit `7bfa17939` (last G2C merge).
Implementing agent must `git pull origin sprint/m19-g2` before cutting the feature branch.

**Feature branch pattern:**
```bash
git checkout -b feat/m19-g2d-iceland-fixture sprint/m19-g2
```

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified in CE audit findings |
| `docs/architecture/emergency-instrument-transmission-table.md` | CE coordination (update before implementation PR opens) | CE audit findings (Decision 3 gate) |
| `docs/methodology/calibration-basis.md` | CM coordination (update before implementation PR opens) | CM calibration deliverable |
| `backend/app/simulation/` (ExternalSectorModule, MacroeconomicModule, DemographicModule) | Sprint sub-branch — feature PR | ADR-020 channel implementation |
| `backend/tests/test_m19_g2d_iceland_scenario_runs.py` | Sprint sub-branch — feature PR | Test authorship (before implementation) |
| `backend/tests/backtesting/fixtures/isl_*.py` | Sprint sub-branch — feature PR | ISL fixture files |

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

**6.3a — New output paths:** No new output directories introduced.
Iceland fixture follows the G2C fixture pattern — outputs via `mode3_harness.py` to
in-memory `HarnessResult`; no new file output paths.

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies at sprint entry

G2D depends on:
- `sprint/m19-g2` containing `backend/app/harness/mode3_harness.py` (G2A) — **SATISFIED**
- ADR-020 accepted — **SATISFIED**
- CM calibration deliverable and CE audit — **PENDING** (pre-implementation PR gates, not cross-group dependencies)

### 6.5 — Prior NM verification

**NM verification sweep date:** 2026-07-03
**Sweep period:** Since G2C sprint closed (2026-07-03)

| NM entry | Process improvement required | Applied in G2D? |
|---|---|---|
| NM-075 | Worktree allocated per sprint group before implementation begins | **Yes** — worktree allocation command in §6.1 |
| NM-087 | `git stash --include-untracked` prohibited; worktree is the safe alternative | **Yes** — stash prohibition acknowledged; worktree required |
| NM-088 | Parallel Claude Code sessions must each have their own named worktree | **Yes** — worktree allocation required at sprint entry |
| NM-089 | Shared-state file changes committed before branch switch | **Yes** — shared-state writes committed before any branch switch; PM Agent coordination lane enforced |
| NM-084 | CM sign-off obtained before fixture PRs open (not after) | **Yes** — CM advisory/calibration deliverable required before implementation PR opens (§2.2) |
| NM-086 | E2E mock routes verified against `api_contracts.yml` before implementation PR | N/A — G2D is backend-only; no E2E mock routes introduced |

---

## EL Approval Record

*EL reviews this entry document before any implementation PR opens. Approval is recorded here
or as a comment on the exit checklist issue #1535.*

**EL approval:** Pending

> {EL approval statement — to be filled at approval time}
> — @PublicEnemage ({date})
