---
name: m19-g2c-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G2 Phase C — Battle-Testing Scenario Runs
status: Filed — awaiting intent documents, CM advisory (#1549–#1552, #1554), and EL approval
authored-by: PM Agent
authored-date: 2026-07-03
el-approved: false
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19, G2 Phase C: Battle-Testing Scenario Runs

**Status:** Filed — awaiting intent documents, CM advisory for new-country scenarios, and EL approval before implementation begins
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
| Sprint number | 4 (G2 Phase C) |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md` |
| Exit checklist issue | #1535 |
| Sprint groups in scope | G2 Phase C (#1547, #1548, #1549, #1550, #1551, #1552, #1554) |
| Wave coordination tier | Standard — G2C concurrent with G3 (Wave 2 entry) if G3 begins; disjoint file areas |
| Concurrent groups at entry | 1 of 5 max — G2C only; G3 sprint entry not yet filed; G1/G2A/G2B complete |
| Cross-group dependencies | G2C depends on G2A harness: SATISFIED — `sprint/m19-g2` contains `backend/app/harness/mode3_harness.py` (PR #1568, 2026-07-02) |

### Wave kickoff coordination fields (NM-071; sprint-planning-sop.md §Wave Kickoff Coordination Check)

**Groups active at G2C entry (Wave 2 transition):**

| Group | Primary implementation domain | Shared-file write scope |
|---|---|---|
| G2C (#1547–#1552, #1554) | Backend only (`backend/tests/backtesting/`, `backend/tests/fixtures/`) | `SESSION_STATE.md` at exit only |
| G3 (#1543, #1536, #1537) | Backend (`backend/app/simulation/banding_engine.py`, `backend/app/schemas.py`) + Frontend (`frontend/src/components/TrajectoryView.tsx`) | `SESSION_STATE.md` at exit only |

**Cross-group dependency graph:**
- G2C has no dependency on G3.
- G3 has no dependency on G2C (G3 is blocked by G2B calibration data — SATISFIED; G3 is not blocked by G2C).
- G2C and G3 have fully disjoint file areas — no merge conflicts anticipated if concurrent.

**Coordination tier rationale:** Standard (concurrent G2C + G3 if G3 enters). G2C writes only to `backend/tests/` paths; G3 writes to `backend/app/simulation/`, `backend/app/schemas.py`, and `frontend/src/components/`. Zero overlap. Shared-state updates deferred to sprint exits via PM Agent coordination lane.

**Scope lock precondition (NM-081):** Confirmed CLEAR — see Section 3.0.

### Integration PR determination (G2D contingency)

Per the sprint group isolation protocol, the integration PR (`sprint/m19-g2` → `release/m19`) fires at the close of the *final* G2 phase. G2D (Iceland, #1553) is currently blocked by the capital controls gap (#1532), which is an open EL decision (SESSION_STATE.md §Open EL Decisions: "ARCH-014 PENDING_NUMBER — EL decision needed on whether to scope ADR authorship in M19 Wave 2 or defer to M20").

**Contingency rule for this sprint entry:**
- If EL determines G2D defers to M20 before or at G2C exit: **G2C is the final G2 phase**. The integration PR fires at G2C PI Agent exit confirmation.
- If EL scopes G2D within M19 Wave 2: **G2C is not the final G2 phase**. The integration PR is deferred to G2D exit.

PI Agent must confirm the G2D determination with the EL before filing the G2C exit document. If the determination is not on record at G2C exit, PI Agent must obtain an EL ruling before proceeding with or deferring the integration PR.

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for this sprint.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` cut from `main` at milestone kickoff 2026-07-02 at commit 1bf1ecc
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` (verified at M19 sprint plan filing 2026-07-02; covers `sprint/m*` as well)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m19-sprint-plan.md` EL-approved 2026-07-02

### 2.2 — ADR prerequisite gate

G2 Phase C has no ADR prerequisite. See Section 4 for reasoning. N/A check:

- [x] All groups with `BLOCKED_ADR` status in the sprint plan have their required ADR accepted — G2C carries no `BLOCKED_ADR` status (N/A)

**ADR prerequisite status:**

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G2 Phase C | None | N/A | CLEAR |

**Chief Methodologist advisory — pre-PR-open condition for new-country scenarios:**

The sprint plan states: "Sri Lanka (#1549), Pakistan (#1550), Turkey (#1551), Egypt (#1552), Ghana (#1554) are new cases — Chief Methodologist advises on data sourcing before sprint entries filed."

**Status of CM advisory at G2C entry filing:** *Not yet on record.* The sprint plan's intended sequencing was for CM advisory to precede this entry. EL approval of this entry is conditional on:
1. The CM advisory for all five new-country scenarios being on record (issue comments on each of #1549–#1552 and #1554), OR
2. An EL determination that CM advisory is a pre-PR-open condition (not pre-entry) for G2C, given that Greece (#1547) and Argentina (#1548) have lower data risk and can unblock early implementation.

For Greece (#1547) and Argentina (#1548): these extend existing scenarios with established data source precedents. CM advisory is LOW risk. Feature PRs for these two countries may open once EL approval is recorded, without a separate CM advisory.

For Sri Lanka (#1549), Pakistan (#1550), Turkey (#1551), Egypt (#1552), Ghana (#1554): CM advisory must be on record on each issue before the implementing agent opens the corresponding feature PR. This is the NM-084 spirit applied to G2C: observable artifact on the issue before the PR opens, not after.

**Pre-PR-open checklist (implementing agent, per-country for new cases):**

| Country | Issue | CM advisory on issue? | Feature PR may open? |
|---|---|---|---|
| Greece 2010–15 | #1547 | N/A — extends existing fixture | Yes — PR #1597 merged |
| Argentina 2001 | #1548 | N/A — extends existing fixture | Yes — PR #1598 merged |
| Sri Lanka 2022–23 | #1549 | Advisory on record 2026-07-03 — unblocked | Yes |
| Pakistan 2022–23 | #1550 | Advisory on record 2026-07-03 — unblocked | Yes |
| Turkey 2018–19 | #1551 | Advisory on record 2026-07-03 — unblocked | Yes |
| Egypt 2016 | #1552 | Advisory on record 2026-07-03 — unblocked | Yes — MonetaryVolumeInput deserializer fix required first |
| Ghana 2022–23 | #1554 | Advisory on record 2026-07-03 — unblocked | Yes — verify GHA entity; MonetaryVolumeInput optional (absence-of-input fallback accepted) |

*Implementing agent must check the CM advisory column before opening each PR. Do not open a feature PR for a new-country scenario until the CM advisory comment is on the corresponding issue. This is an enforcement obligation, not advisory.*

### 2.3 — Intent document gate

G2 Phase C is **not** an infrastructure sprint. The battle-testing scenario runs produce harness output reports — qualitative analytics artifacts reviewed by the Business PO, the Chief Methodologist, and Demo 8 reviewers for model fidelity evidence. These are analytics deliverables that constitute user-facing evidence of the model's cross-country breadth. Intent documents are required per `docs/process/agent-execution-lifecycle.md Step 1`.

- [ ] Intent document filed for every user-facing deliverable in this sprint — **NOT YET — BLOCKING**

**Intent document status:**

A single combined intent document covering all seven G2C scenarios is appropriate given the shared acceptance criteria structure (all scenarios use the same harness API, the same run classification logic, and the same output format gates). Per-country data sourcing specifications are included as appendices within the combined document.

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| G2C battle-testing scenario runs (#1547–#1552, #1554) — combined | N/A | `docs/process/intents/M19-G2C-2026-07-03-battle-testing-scenario-runs.md` | **No — BLOCKING** |

*Intent document must be filed and the path above must exist before EL approval is granted.*

### 2.4 — QA test authorship gate

- [ ] QA test file authored for every user-facing deliverable in this sprint — **NOT YET — BLOCKING**

**QA test status:**

A single combined test file is appropriate, with one test function per country scenario. Each function asserts: (a) harness run completes without error, (b) output structure matches the configured format, (c) `known_limitations` block is present, (d) run type is correctly classified (`TYPE_B` for counter-factual scenarios; `TYPE_A_B` for scenarios with both replay and counter-factual components).

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| G2C battle-testing runs (#1547–#1552, #1554) — combined | `docs/process/intents/M19-G2C-2026-07-03-battle-testing-scenario-runs.md` | `backend/tests/backtesting/test_m19_g2c_scenario_runs.py` | **No — BLOCKING** |

*NM-078 compliance: test file placed at `backend/tests/backtesting/` (CI-discoverable path).*
*NM-056 rule: NO `pytest.skip()` or soft-skip patterns. Tests fail RED (missing fixture function) until each scenario's fixture is implemented.*

**CI ordering note (NM-085 application):**

G2C will have seven feature PRs landing sequentially on `sprint/m19-g2`. Unlike G2B, G2C scenarios are NOT CI-gated calibration fixtures — the `backtesting` mark coverage is informational for G2C. If the combined test file includes tests for all seven scenarios from the start, earlier PRs will produce transient `NameError` / `ImportError` failures on the not-yet-implemented scenario functions. Two mitigations (implementing agent chooses one):
1. Author the combined test file with per-function stubs returning `pytest.skip("pending: <country>")` until the scenario PR lands — **exception to NM-056 permitted only for G2C cross-scenario stubs, not for the primary scenario under test in each PR**
2. Author the test file with only Greece and Argentina functions initially; add remaining country functions in each country's feature PR (additive approach — no stubs needed)

The implementing agent must document which approach is taken at G2C test file authorship. Option 2 is preferred as it avoids the NM-056 tension.

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation (NM-081; sprint-planning-sop.md §Scope lock precondition)

- [x] All ADR decisions affecting this sprint's scope are EL-approved and merged to `release/m19`

G2C has no ADR dependency. The harness infrastructure (G2A, PR #1568) and calibration fixtures (G2B, PRs #1576–#1577) are both on `sprint/m19-g2`. No predecessor ADR scope decision can produce scope drift for G2C. **CLEAR.**

**Scope uncertainty:** None affecting implementation scope. The fidelity tier achievable per country (DIRECTION_ONLY vs MAGNITUDE_MATCH vs STRUCTURAL_ONLY) is a Chief Methodologist determination made before each country's feature PR opens — this does not change the sprint scope (all seven issues remain in scope regardless of fidelity tier outcome).

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1547 | Greece 2010–15 primary surplus programme counter-factual — Type B | G2 Phase C | Medium — extends existing fixture; lower data risk |
| #1548 | Argentina 2001 convertibility exit counter-factual — Type B | G2 Phase C | Medium — extends existing fixture; lower data risk |
| #1549 | Sri Lanka 2022–23 Coffin Corner — Type A+B | G2 Phase C | Medium — new country; CM advisory required |
| #1550 | Pakistan 2022–23 IMF programme survival — Type B | G2 Phase C | Medium — new country; CM advisory required |
| #1551 | Turkey 2018–19 Backside of Power Curve — Type B | G2 Phase C | Medium — new country; CM advisory required |
| #1552 | Egypt 2016 devaluation and subsidy reform — Type B | G2 Phase C | Medium — new country; CM advisory required |
| #1554 | Ghana 2022–23 IMF programme — Type A+B | G2 Phase C | Medium — new country; CM advisory required |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Horizon | Rationale for exclusion |
|---|---|---|---|
| #1553 | Iceland 2008–11 orthodox vs heterodox — Type A+B | G2 Phase D | Blocked by #1532 (capital controls gap); ARCH-014 pending EL scope decision |
| #1543 | ADR-007 Bayesian posterior layer | G3 Wave 2 | Separate sprint group; not dependent on G2C |
| #1536 | ADR-007 meaninglessness threshold | G3 Wave 2 | Separate sprint group |
| #1537 | BandResult visible fields | G3 Wave 2 | Separate sprint group |
| #1528 | PSP driver arc + auditability panel | G4 Wave 2–3 | Separate sprint group |
| #1529 | CI label precision fix | G4 Wave 2–3 | Separate sprint group |

---

## Section 4 — ADR Prerequisite Summary

G2 Phase C does not require a new ADR or an amendment to any existing ADR.

**Reasoning:** G2C scenario runs use the established harness API (`run_harness`, `FidelityTier`, `RunType`) and existing REST API contracts. Each scenario is a `build_XXX_scenario()` function + `run_harness()` call, identical in structure to G2B. The Type A/B run classification and `known_limitations` block design are already implemented in `app.harness.mode3_harness` (G2A). Country-specific data sourcing choices are a Chief Methodologist data quality determination, not an architectural decision. The `CAPITAL_CONTROLS` emergency instrument limitation (#1532) is flagged via the harness `known_limitations` block — it does not require a G2C ADR.

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G2 Phase C | None | N/A | Conditional — once intent document (§2.3), QA tests (§2.4), EL approval, and CM advisory for each new-country scenario (§2.2) are in place |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-03
**Sweep period:** Since G2B entry (2026-07-02) — two NM entries filed during G2B (NM-084, NM-085)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| NM-084: CM sign-off obtained after feature PRs opened; ordering enforcement absent | Process gap — pre-merge CM review | Yes — filed during G2B exit 2026-07-02 | NM-084 |
| NM-085: Co-dependent fixture PRs produce transient cross-test failure; pattern undocumented | Process gap — co-dependent fixture CI ordering | Yes — filed during G2B exit 2026-07-02 | NM-085 |
| NM-084 process improvement not yet codified in `sprint-planning-sop.md §Pre-Merge CM Review` | Process gap — process improvement lagging | Anticipatory — noted here; PI Agent to assess whether a new NM entry is required or the NM-084 entry covers this | Pending |

**NM-084 codification gap — anticipatory note:**
NM-084 called for codification in `docs/process/sprint-planning-sop.md §Pre-Merge CM Review` before G2C sprint entry. That codification has not yet occurred. G2C handles the NM-084 spirit via the explicit pre-PR-open CM advisory table in §2.2. However, the process improvement is structural — it should live in the SOP, not only in this sprint entry. PI Agent must assess whether the codification gap warrants a new NM entry or is captured within NM-084 scope, before EL approval of this entry.

*Prior NM applicability review in Section 6.5.*

---

## Section 6 — Sprint Group Isolation (M18 onward)

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m19-g2` |
| Branch status | **Already exists** — cut at G2A entry (2026-07-02); G2A (PR #1568), G2B SEN (PR #1576), G2B ZMB (PR #1577) all merged |
| Cut from | `release/m19` (original cut 2026-07-02) |
| Sprint journal issue | TBD — PM Agent creates at EL approval |

**Branch lifecycle note (from G2A sprint entry §6.1):** `sprint/m19-g2` serves all G2 phases (A, B, C, D). It is not re-cut here. G2C feature branches are cut from the current tip of `sprint/m19-g2`. Feature PRs target `sprint/m19-g2`.

**Feature branch cut commands for G2C implementing agent:**

```bash
# Greece (first — no CM advisory prerequisite)
git checkout -b feat/m19-g2c-greece-counterfactual sprint/m19-g2

# Argentina (no CM advisory prerequisite)
git checkout -b feat/m19-g2c-argentina-counterfactual sprint/m19-g2

# Each new-country case — ONLY after CM advisory is on record on the corresponding issue
git checkout -b feat/m19-g2c-sri-lanka-coffin-corner sprint/m19-g2
git checkout -b feat/m19-g2c-pakistan-programme sprint/m19-g2
git checkout -b feat/m19-g2c-turkey-backside sprint/m19-g2
git checkout -b feat/m19-g2c-egypt-devaluation sprint/m19-g2
git checkout -b feat/m19-g2c-ghana-imf-programme sprint/m19-g2
```

*Always verify `git branch` confirms the correct branch before committing (NM-079).*

### 6.2 — File-conflict risk assessment

G2C writes only new test and fixture files on the sprint sub-branch. No shared state files or DS-owned files are touched during implementation.

| File | Lane required | Trigger |
|---|---|---|
| `backend/tests/fixtures/greece_scenario.py` (new) | Sprint sub-branch — no coordination needed | — |
| `backend/tests/fixtures/argentina_scenario.py` (new) | Sprint sub-branch — no coordination needed | — |
| `backend/tests/fixtures/sri_lanka_scenario.py` (new) | Sprint sub-branch — no coordination needed | — |
| `backend/tests/fixtures/pakistan_scenario.py` (new) | Sprint sub-branch — no coordination needed | — |
| `backend/tests/fixtures/turkey_scenario.py` (new) | Sprint sub-branch — no coordination needed | — |
| `backend/tests/fixtures/egypt_scenario.py` (new) | Sprint sub-branch — no coordination needed | — |
| `backend/tests/fixtures/ghana_scenario.py` (new) | Sprint sub-branch — no coordination needed | — |
| `backend/tests/backtesting/test_m19_g2c_scenario_runs.py` (new — QA file) | Sprint sub-branch — no coordination needed | — |
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update only |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | Only if NM identified during implementation |

*If the implementing agent introduces a scenario results cache directory (e.g., `backend/tests/backtesting/results/`), a `.gitignore` update is required — see §6.3a.*

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

G2C introduces no changes to `.github/workflows/`, `.githooks/`, or `.gitignore`. Scenario fixture files write to `backend/tests/fixtures/` (already tracked). Harness output routes to stdout or user-specified paths.

#### 6.3a — New output paths declaration (NM-069 process improvement)

The harness produces output to stdout or user-specified file paths. If the implementing agent introduces a results cache directory for G2C scenario outputs (e.g., `backend/tests/backtesting/results/`), a `.gitignore` update is required in the same PR that introduces the directory. Assess at implementation time.

- [x] No new output directories anticipated — harness output routes to stdout or user-specified paths
- [ ] If a results cache directory is introduced: `.gitignore` update required in the same PR

### 6.4 — Cross-group dependency declaration

- [x] G2C has a SATISFIED intra-sprint dependency on G2A

**G2A dependency (SATISFIED):**
G2C depends on `app.harness.mode3_harness` produced by G2A (#1546). This module is on `sprint/m19-g2` (PR #1568, merged 2026-07-02). All G2C scenario fixture functions import `run_harness`, `FidelityTier`, and `RunType` — these imports are GREEN as of this entry filing.

**No dependency on G2B calibration data:**
G2C scenario runs are battle-testing runs, not Bayesian posterior inputs. The G2B SEN and ZMB calibration data is consumed by G3 (#1543), not by G2C. G2C does not require G2B's output — only G2A's harness.

**No cross-group dependency on G3:**
G2C and G3 are independent and may run concurrently. G3 does not depend on G2C outputs.

### 6.5 — Prior NM verification (NM-068 process improvement)

**NM verification sweep date:** 2026-07-03
**Sweep period:** All NM entries through NM-085

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-075 | Git worktrees allocated per sprint group | Yes — implementing agent must use dedicated worktree for `sprint/m19-g2` G2C feature branches. Worktree path convention: `.claude/worktrees/sprint-m19-g2c` |
| NM-076 | Before any testid rename, grep full E2E corpus for old testid | N/A — G2C is backend-only; no testids introduced or renamed |
| NM-077 | `gh pr create` must specify `--head <branch>` explicitly | Yes — implementing agent must pass `--head feat/m19-g2c-<country>` when opening each PR |
| NM-078 | Milestone test files must be in CI-discoverable path (`backend/tests/backtesting/`) | Yes — combined test file at `backend/tests/backtesting/test_m19_g2c_scenario_runs.py` per §2.4 |
| NM-079 | Confirm active branch before committing | Yes — implementing agent must verify `git branch` before every commit on the worktree |
| NM-080 | No direct commits to `release/m19` | Yes — all G2C work targets `sprint/m19-g2` via feature branches |
| NM-081 | Sprint branch must not be cut before predecessor ADR scope finalized | N/A — G2C has no ADR dependency; `sprint/m19-g2` already exists from G2A entry |
| NM-082 | CI band fill geometry error (UI-specific) | N/A — G2C is backend-only |
| NM-083 | Demo-spec ↔ component-contract integration gap (UI-specific) | N/A — G2C is backend-only |
| NM-084 | CM sign-off must be on record before feature PRs are opened (or merged) for fixture-producing groups | Yes — applied via pre-PR-open CM advisory table in §2.2. Codification in `sprint-planning-sop.md §Pre-Merge CM Review` is pending — see §5 near-miss note. G2C applies the NM-084 spirit even though G2C runs are not CI-gated calibration fixtures |
| NM-085 | Co-dependent fixture sprint entries must include CI ordering statement for `backtesting` non-required check | Assessed — G2C scenario runs are NOT CI-gated (`@pytest.mark.backtesting` is informational for G2C). The combined test file approach (§2.4) means earlier PRs may produce transient failures on not-yet-implemented country functions. This is addressed via the two-option mitigation documented in §2.4. See §2.4 CI ordering note for full treatment |

---

## EL Approval Record

*EL reviews this entry document before any implementation PR opens. Approval is recorded here
or as a comment on the exit checklist issue #1535.*

**EL approval:** APPROVED — 2026-07-03

**Pre-approval conditions:**

1. `[x]` Intent document filed at `docs/process/intents/M19-G2C-2026-07-03-battle-testing-scenario-runs.md`
2. `[x]` QA test file authored at `backend/tests/backtesting/test_m19_g2c_scenario_runs.py`
3. `[x]` CM advisory status — **Option (b) selected:** CM advisory is a pre-PR-open condition (not a pre-entry condition). Greece (#1547) and Argentina (#1548) may proceed to implementation immediately. PRs for new-country scenarios (#1549, #1550, #1551, #1552, #1554) must not open until CM advisory is on record per §2.2.
4. `[x]` NM-084 codification gap — proceed with entry. Gap is documented in §5; codification in `sprint-planning-sop.md §Pre-Merge CM Review` is deferred to end-of-G2 SOP sweep, not blocking G2C start.

> G2C sprint entry approved. Greece and Argentina counter-factual Type B runs may begin. New-country feature PRs are gated on CM advisory (§2.2). Integration PR deferred per ARCH-014 contingency rule (§1.5).
> — @PublicEnemage (2026-07-03)
