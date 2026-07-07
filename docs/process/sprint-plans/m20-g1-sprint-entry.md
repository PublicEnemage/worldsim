---
name: m20-sprint-g1-entry
type: sprint-entry
milestone: M20 — Analytical Evidence Portfolio and Demo 9
sprint-group: G1
status: Filed
authored-by: PM Agent
authored-date: 2026-07-07
el-approved: true
release-branch: release/m20
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M20 G1 — AEP EURO-AREA Entries

**Status:** EL-approved — implementation authorised  
**Date authored:** 2026-07-07  
**Release branch:** `release/m20`  
**Sprint plan:** `docs/process/sprint-plans/m20-sprint-plan.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M20 — Analytical Evidence Portfolio and Demo 9 |
| GitHub Milestone | #22 |
| Sprint number | G1 |
| Release branch | `release/m20` |
| Sprint plan document | `docs/process/sprint-plans/m20-sprint-plan.md` |
| Exit checklist issue | #1773 |
| Sprint groups in scope | G1 |
| Wave coordination tier | Standard — no engineering dependencies, no concurrent implementation PRs |
| Concurrent groups at entry | 0 — G4 not yet started |
| Cross-group dependencies | None — G1 AEA documentation is independent of G4 engineering |

---

## Section 2 — Entry Invariants Checklist

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m20` cut from main `5fadd00` on 2026-07-07
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*`
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m20-sprint-plan.md` EL-approved in session 2026-07-07 (scope decomposition approval recorded in session)

### 2.2 — ADR prerequisite gate

**N/A — AEA documentation sprint.** G1 deliverables are AEP evidence entries authored in `docs/evidence/`. No new ADRs are required. The governing methodological documents (analytical-framework.md, coverage-audit.md, TEMPLATE.md) are already accepted and on `release/m20`.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G1 | None | N/A | CLEAR |

### 2.3 — Intent document gate

**Documentation sprint — AEP entries are authorship artifacts, not code deliverables.** The coverage audit (`docs/evidence/coverage-audit.md §Family 2 — EURO-AREA`) serves as the functional intent specification for each entry: it identifies which scenarios to run, what calibration family applies, what fidelity ceiling is achievable, and what the entry should document. No separate `docs/process/intents/` files are required.

| Deliverable | Coverage audit reference | Intent specification | Gate |
|---|---|---|---|
| AEP-001-GRC-2010.md | `§Family 2 (b)/(c) — EUR-1` | coverage-audit.md §Family 2 + analytical-framework.md §2 Family 2 | CLEAR |
| AEP-002-GRC-2010-B.md | `§Family 2 (c) — EUR-1 Type B` | As above; temporal blindfold protocol applies | CLEAR |
| AEP-003-ISL-2008.md | `§Family 2 (c) — EUR-2` | coverage-audit.md §Family 2 + ADR-020 capital controls channel | CLEAR |

### 2.4 — QA test authorship gate

**Documentation sprint — no code test files.** AEP entries are reviewed against TEMPLATE.md structural compliance (9 sections present) and analytical-framework.md epistemic bounds (fidelity tier correctly declared). EL review is the quality gate. No backend or frontend test files are produced by this sprint group.

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation

- [x] All ADR decisions affecting this sprint's scope are EL-approved and merged to `release/m20`

**Scope uncertainty:** None. AEP-001 through AEP-003 are fully determined by existing fixtures, the EURO-AREA calibration family, and the accepted analytical framework.

### 3.1 — Issues in scope

G1 deliverables are tracked under the sprint journal issue and sprint plan, not individual GitHub issues. Parent tracking: #1773 (M20 Exit Checklist). Sprint journal: #1786.

| Deliverable | Sprint journal issue | Priority |
|---|---|---|
| AEP-001-GRC-2010.md (Type A replay) | #1786 | Immediate |
| AEP-002-GRC-2010-B.md (Type B counter-factual) | #1786 | Immediate |
| AEP-003-ISL-2008.md (Type B heterodox vs orthodox) | #1786 | Immediate |

### 3.2 — Issues explicitly out of scope

| Item | Horizon | Rationale |
|---|---|---|
| AEP-004–009 (SSA-LIC + LATAM-EM) | G2 | Separate sprint group; begins after G1 exits |
| AEP-010–011 (SOUTH-SE-ASIAN) | G3 | Begins after G2 exits |
| DEMO-217, DEMO-233, DEMO-234, NM-099/test fix | G4 | Engineering sprint; independent of G1 AEA work |
| Live constraint-floor search | M21 | Deferred per scope decomposition 2026-07-07 |
| DEMO-235 (#1777) | M21 | Deferred per scope decomposition 2026-07-07 |
| ADR-008 renewal (SCAN-029 carry-forward) | M20 (not G1) | Not blocked on G1; assign to Architect Agent |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G1 | None | N/A | Yes |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-07  
**Sweep period:** Since M19 close (2026-07-06)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| Session ended mid-task with uncommitted agents.md/CLAUDE.md edits; PR #1779 omitted them | Near-miss | Yes — filed this session | NM-100 |

**NM-100 process improvements apply to this sprint (see §6.5).**

---

## Section 6 — Sprint Group Isolation (M18 onward)

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m20-g1` |
| Cut from | `release/m20` |
| Sprint journal issue | #1786 |

**PM Agent sprint sub-branch cut command:**
```bash
git checkout -b sprint/m20-g1 release/m20 && git push -u origin sprint/m20-g1
```

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/evidence/AEP-001-GRC-2010.md` | Sprint sub-branch (AEA file authority) | AEP-001 authorship |
| `docs/evidence/AEP-002-GRC-2010-B.md` | Sprint sub-branch (AEA file authority) | AEP-002 authorship |
| `docs/evidence/AEP-003-ISL-2008.md` | Sprint sub-branch (AEA file authority) | AEP-003 authorship |

No shared state files or DS-owned files require direct writes from the sprint feature branch.

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

#### 6.3a — New output paths declaration

- [x] No new output directories — all generated paths are already covered by `.gitignore`

`docs/evidence/` writes are documentation files (not generated artifacts). The existing reports directory (`backend/tests/backtesting/reports/`) already has `.gitignore` coverage. No changes needed.

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies

G1 (AEA documentation) is independent of G4 (engineering). G1 does not require G4 output, and G4 does not require G1 output. Both may proceed in parallel.

### 6.5 — Prior NM verification

**NM verification sweep date:** 2026-07-07  
**Sweep period:** Since M19 close (2026-07-06)

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-100 | Before opening any multi-file PR: run `git diff HEAD --name-only` and verify every file named in the PR description appears in the output | Yes — pre-PR diff check will be run before the G1 integration PR opens |
| NM-100 | `gh pr view <N> --json files` is authoritative about what a merged PR contained — session summary is not | Yes — will verify integration PR contents via `gh pr view` after merge if any doubt arises |

---

## EL Approval Record

**EL approval:** Confirmed in session

> "we can begin."  
> — @PublicEnemage (2026-07-07)
