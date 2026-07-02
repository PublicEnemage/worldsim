---
name: m19-g2a-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G2 Phase A — Headless Battle-Testing Harness
status: EL-approved 2026-07-02
authored-by: PM Agent
authored-date: 2026-07-02
el-approved: 2026-07-02
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19, G2 Phase A: Headless Battle-Testing Harness

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
| Sprint number | 2 (G2 Phase A) |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md` |
| Exit checklist issue | #1535 |
| Sprint groups in scope | G2 Phase A (#1546) |
| Wave coordination tier | Standard — 2 groups active concurrently in Wave 1 (G1 and G2A); no shared implementation file areas |
| Concurrent groups at entry | 1 of 5 max — G1 sprint entry filed simultaneously; no G1 implementation PR open at time of G2A filing |
| Cross-group dependencies | None — G2A is parallel to G1; see §6.4 for G2B intra-group dependency |

### Wave kickoff coordination fields (NM-071; sprint-planning-sop.md §Wave Kickoff Coordination Check)

**Groups in this wave (Wave 1, concurrent implementation PRs expected):**

| Group | Primary implementation domain | Shared-file write scope |
|---|---|---|
| G1 (#1540) | Frontend (`ControlPlaneColumn.tsx`) + Backend (constraint-floor endpoint, `backend/app/simulation/`) | `SESSION_STATE.md` at exit only |
| G2 Phase A (#1546) | Backend only (`backend/tests/backtesting/` or `backend/app/harness/`) | `SESSION_STATE.md` at exit only |

**Cross-group dependency graph:**
- G1 has no dependency on G2A.
- G2A has no dependency on G1.
- G2B (#1541, #1542) depends on G2A: no G2B feature PR may open on `sprint/m19-g2` until the G2A harness PR merges to `sprint/m19-g2`. This ordering constraint is enforced at G2B sprint entry.

**Coordination tier rationale:** Standard (2 concurrent groups). G1 and G2A have fully disjoint file areas — G1 writes to `frontend/src/components/ControlPlaneColumn.tsx` and `backend/app/simulation/`; G2A writes to `backend/tests/backtesting/` and/or `backend/app/harness/`. No merge conflicts anticipated. Shared-state file writes (`SESSION_STATE.md`) are deferred to sprint exit and routed through the PM Agent coordination lane at that time.

**Scope lock precondition (NM-081):** Confirmed CLEAR — see Section 3.0.

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for this sprint.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` cut from `main` at milestone kickoff 2026-07-02 at commit 1bf1ecc
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` (verified at M19 sprint plan filing 2026-07-02; covers `sprint/m*` as well)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m19-sprint-plan.md` EL-approved 2026-07-02 (frontmatter date and #1535 comment)

### 2.2 — ADR prerequisite gate

G2 Phase A has no ADR prerequisite. See Section 4 for the full reasoning. N/A check:

- [x] All groups with `BLOCKED_ADR` status in the sprint plan have their required ADR accepted — G2A carries no `BLOCKED_ADR` status (N/A)

**ADR prerequisite status:**

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G2 Phase A | None | N/A | CLEAR |

### 2.3 — Intent document gate

G2 Phase A is **not** an infrastructure sprint. The harness produces user-facing outputs — ASCII/CSV/JSON/Markdown battle-testing reports consumed by finance ministry analysts reviewing backtesting evidence before and at Demo 8. These are analytics outputs and constitute a "backend capability" under `docs/process/sprint-planning-sop.md §Sprint Entry Gate` condition 4. An intent document is required.

- [x] Intent document filed for every user-facing deliverable in this sprint

**Intent document status:**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| Headless battle-testing harness (#1546) | N/A | `docs/process/intents/M19-G2A-2026-07-02-headless-battle-testing-harness.md` | Yes — filed 2026-07-02 |

### 2.4 — QA test authorship gate

- [x] QA test file authored for every user-facing deliverable in this sprint

**QA test status:**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| Headless battle-testing harness (#1546) | `docs/process/intents/M19-G2A-2026-07-02-headless-battle-testing-harness.md` | `backend/tests/backtesting/test_m19_g2a_headless_harness.py` | Yes — filed 2026-07-02 |

*NM-078 compliance: test file placed at `backend/tests/backtesting/` (not `backend/tests/` root). Confirmed: `backend/pytest.ini` does not restrict testpaths — pytest discovers all `test_*.py` files under `backend/`, so `backend/tests/backtesting/` is covered.*

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation (NM-081; sprint-planning-sop.md §Scope lock precondition)

- [x] All ADR decisions affecting this sprint's scope are EL-approved and merged to `release/m19`

G2A has no ADR dependency. The harness architecture is fully specified in issue #1546 (run modes, output formats, `known_limitations` block, Type A/B classification, Type B differential summary fields). No predecessor ADR scope decision can produce scope drift for G2A. **CLEAR.**

**Scope uncertainty:** None.

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1546 | Headless battle-testing harness — configurable output format, Type A/B run classification, per-run `known_limitations` | G2 Phase A | High — prerequisite for G2B, G2C, G2D |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Horizon | Rationale for exclusion |
|---|---|---|---|
| #1541 | SEN backtesting fixture | G2 Phase B | Depends on G2A harness; separate sprint entry filed after G2A PR merges to `sprint/m19-g2` |
| #1542 | ZMB backtesting fixture | G2 Phase B | Same — dependent on G2A |
| #1547 | Greece 2010–15 counter-factual Type B | G2 Phase C | Depends on G2A harness; separate sprint entry |
| #1548 | Argentina 2001 counter-factual Type B | G2 Phase C | Same |
| #1549 | Sri Lanka 2022–23 Type A+B | G2 Phase C | Same |
| #1550 | Pakistan 2022–23 Type B | G2 Phase C | Same |
| #1551 | Turkey 2018–19 Type B | G2 Phase C | Same |
| #1552 | Egypt 2016 Type B | G2 Phase C | Same |
| #1554 | Ghana 2022–23 Type A+B | G2 Phase C | Same |
| #1553 | Iceland 2008–11 Type A+B | G2 Phase D | Blocked by #1532 (capital controls gap); separate sprint entry when #1532 resolved |
| #1540 | Mode 3 constraint-floor search | G1 | Different sprint group; parallel to G2A on `sprint/m19-g1` |
| #1532 | Capital controls transmission gap | Pre-wave / known gap | G2A must flag #1532 in the `known_limitations` block when `EmergencyInstrument.CAPITAL_CONTROLS` is used; the fix itself is out of G2A scope |

---

## Section 4 — ADR Prerequisite Summary

G2 Phase A does not require a new ADR or an amendment to any existing ADR.

**Reasoning:** The harness calls existing REST API endpoints (`POST /scenarios/{id}/advance`, `GET /scenarios/{id}/snapshots`, `GET /scenarios/{id}/measurement-output`) whose contracts are governed by existing ADRs and `docs/schema/api_contracts.yml`. No new endpoints are introduced. The Type A / Type B run classification formalises the existing conceptual distinction between backtesting and counter-factual runs — it is not a new framework-level architectural decision requiring an ADR panel. The four output format modes (ASCII/CSV/JSON/Markdown) are presentation-layer choices in a reporting utility, equivalent in scope to a CLI formatter. The `known_limitations` block surfaces pre-existing module capability registry gaps (Issues #30, #35, #1532) — it does not introduce new capability commitments.

The Chief Methodologist consultation on SEN/ZMB calibration fidelity thresholds applies at **G2B** sprint entry (after the harness is running and can produce fidelity tier outputs), not at G2A.

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G2 Phase A | None | N/A | Yes — once intent document (§2.3) and QA tests (§2.4) are filed and EL approval is recorded |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-02
**Sweep period:** Since M18 close (2026-07-02) — same-day as G2A filing; all NM entries through NM-083 from M18 sprint group activity are in scope.

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified for G2A scope since M18 close | N/A | N/A | N/A |

*Prior NM applicability review in Section 6.5.*

---

## Section 6 — Sprint Group Isolation (M18 onward)

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m19-g2` |
| Cut from | `release/m19` |
| Sprint journal issue | TBD — PM Agent creates at EL approval |

**PM Agent sprint sub-branch cut command:**
```bash
git checkout -b sprint/m19-g2 release/m19 && git push -u origin sprint/m19-g2
```

*Branch lifecycle note: The `sprint/m19-g2` sub-branch serves all G2 phases (A, B, C, D). It is cut once here at G2A entry. G2B, G2C, and G2D sprint entries will reference this same branch. Phase B feature PRs must not open until Phase A's harness PR has merged to `sprint/m19-g2`. The integration PR (`sprint/m19-g2` → `release/m19`) is filed at the close of the final G2 phase, after PI Agent exit confirmation for that phase.*

### 6.2 — File-conflict risk assessment

G2A writes only to new backend files. No shared state files or DS-owned files are touched during implementation.

| File | Lane required | Trigger |
|---|---|---|
| `backend/tests/backtesting/mode3_harness.py` (new) | Sprint sub-branch — no coordination needed | — |
| `backend/tests/backtesting/test_m19_g2a_headless_harness.py` (new) | Sprint sub-branch — no coordination needed | — |
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update only — not during implementation |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | Only if NM identified during implementation |

*If the implementing agent opts for a module path (`backend/app/harness/`) instead of `backend/tests/backtesting/` for the non-test harness source, all writes remain on the sprint sub-branch with no coordination needed. Module path decision is left to the implementing agent per issue #1546 guidance.*

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

G2A introduces no changes to `.github/workflows/`, `.githooks/`, or `.gitignore`. The harness writes to stdout or user-specified paths — no new tracked output directories are introduced.

#### 6.3a — New output paths declaration (NM-069 process improvement)

The harness produces output to stdout or user-specified file paths; it does not write to any repository-tracked directory. If a Phase C or Phase D scenario run in a later sprint needs a results cache directory (e.g., `backend/tests/backtesting/results/`), a `.gitignore` update will be required at that sprint entry. G2A itself introduces no such directory.

- [x] No new output directories — harness output routes to stdout or user-specified paths; `.gitignore` unchanged

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies — G2A is fully parallel to G1

G2A and G1 have no shared implementation file areas and no sequential dependency. The only relationship is demo narrative sequencing (G1 produces constraint-floor capability for Demo 8 Act 1; G2C/D battle-testing evidence provides M19 calibration context) — this is not an implementation dependency.

**Intra-group G2B dependency (not a cross-group dependency — same sprint branch):**
G2B (#1541, #1542) depends on G2A. The SEN and ZMB calibration fixtures use the harness script produced by G2A. G2B feature branches must not be cut from `sprint/m19-g2` until the G2A harness PR has merged to `sprint/m19-g2`. This ordering constraint is enforced at G2B sprint entry — not here.

### 6.5 — Prior NM verification (NM-068 process improvement)

**NM verification sweep date:** 2026-07-02
**Sweep period:** All NM entries through NM-083

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-075 | Git worktrees allocated per sprint group (`git worktree add /tmp/<name> <branch>`) to prevent branch switches overwriting in-progress work | Yes — sprint sub-branch `sprint/m19-g2` is isolated; implementing agent must use a dedicated worktree per NM-075 guidance |
| NM-076 | Before any testid rename, grep full E2E corpus for old testid; update in same PR | N/A — G2A is backend-only; no testids introduced or renamed |
| NM-077 | `gh pr create` must specify `--head <branch>` explicitly; CWD-based inference is unreliable when operating from a worktree | Yes — implementing agent must pass `--head feat/m19-g2a-headless-harness` (or equivalent) when opening the implementation PR |
| NM-078 | Milestone test files must be in the CI-discoverable path; files at `backend/tests/` root are silently excluded | Yes — test file path specified as `backend/tests/backtesting/test_m19_g2a_headless_harness.py` in §2.4; implementing agent must confirm `pytest.ini` discovery covers this path before committing |
| NM-079 | Confirm active branch before committing; wrong-branch commits not detected by any process gate | Yes — implementing agent must verify `git branch` before every commit on the worktree |
| NM-080 | No direct commits to `release/m19`; all changes via feature branches and PRs | Yes — all G2A work targets `sprint/m19-g2` via feature branches |
| NM-081 | Sprint branch must not be cut before predecessor ADR scope is finalized on `release/m{N}` | N/A — G2A has no ADR dependency; scope lock CLEAR per §3.0 |
| NM-082 | CI band fill geometry error shipped with tests green (UI-specific) | N/A — G2A is backend-only; no UI components introduced |
| NM-083 | Demo-spec ↔ component-contract integration gap (UI-specific) | N/A — G2A is backend-only; no component contracts |

---

## EL Approval Record

*EL reviews this entry document before any implementation PR opens. Approval is recorded here
or as a comment on the exit checklist issue #1535.*

**EL approval:** Approved 2026-07-02

> G2 Phase A sprint entry approved. All five entry conditions confirmed: release branch
> exists and CI trigger verified; sprint plan EL-approved; no ADR prerequisite; intent
> document filed at `docs/process/intents/M19-G2A-2026-07-02-headless-battle-testing-harness.md`;
> QA tests authored at `backend/tests/backtesting/test_m19_g2a_headless_harness.py` before
> implementation begins. Coordination tier Standard is correct — G2A and G1 have disjoint
> file areas. `sprint/m19-g2` branch may be cut from `release/m19` and implementation PRs
> may open.
> — @PublicEnemage (2026-07-02)
