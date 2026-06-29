# DevSecOps Infra Review — Sprint Group Execution Health Audit
**Type:** sprint-health (ad-hoc)
**Date:** 2026-06-29
**Milestone:** M18 — Full Argument and Demo 7
**Authored by:** DevSecOps Agent (DS)
**Triggered by:** EL request — post-G6-Step-6b analysis of all M18 sprint group terminal session activity for branching anomalies, cross-contamination, and timing failures
**Sources:** git reflog (full M18 period 2026-06-26–2026-06-29), branch graph, integration commit diffs, near-miss registry, session JSONL analysis (10 largest session files from 62 total M18-era sessions)

---

## Scope

All M18 sprint groups G1–G6 active 2026-06-26 through 2026-06-29. Analysis covers:
- Branch switches and HEAD movements (git reflog full replay)
- Cross-group file contamination events
- Integration PR conflict resolution commits
- Sprint branch cut timing relative to predecessor merges
- CI gate failures and what escaped them
- Session JSONL terminal output for direct evidence of wrong-branch commits, stash leaks, and unrecovered errors

---

## Part 1 — Documented Incidents (Confirmed Against Git Evidence)

All six NM entries from M18 G1–G5 were confirmed against the git record and session logs. Severity and scope assessments below reflect DS review, not NM filing dates.

| NM | Date | Sprint groups | Event | Detected by |
|---|---|---|---|---|
| NM-073 | Jun 27 | G3 | `sprint-branch-ci-gate` had no `playwright-e2e` requirement; PR #1395 (G3 test authorship) auto-merged while E2E still `pending` | EL observation |
| NM-074 | Jun 27 | G3 / infra | `branch-naming` check added to `sprint-branch-ci-gate` Ruleset before the `branch-naming.yml` workflow trigger was extended to cover `sprint/m*` targets; PR #1398 hung indefinitely | EL observation |
| NM-075 | Jun 27 | G1 / G2 / G3 | 18+ concurrent Claude Code sessions sharing one main git working tree; 30+ HEAD switches in ~2 hours; G2 PSP implementation overwritten at least 3×; QA test file deleted from working tree | DS investigation |
| NM-076 | Jun 28 | G4 → G2-era | ADR-019 D-3 testid renames not cross-checked against E2E corpus; 5 test files broken in `sprint/m18-g4` including G2-era `demo-trajectory-mode3.spec.ts` AC-1; three failures detected post-merge | Post-merge CI run 28332341391 |
| NM-077 | Jun 28 | G4 / shared state | `gh pr create` inferred head branch from shell CWD (`chore/m18-state-sync-022`) instead of worktree branch; PR #1428 opened as wrong branch against `sprint/m18-g4`; auto-merge already set when error was detected | Manual inspection |
| NM-078 | Jun 28 | G3 → G4 → G5 | 17 milestone test files in `backend/tests/` root excluded from CI since M14 by directory-based discovery; G3 `distributional-differential` endpoint had wrong column names (`step_index`/`state` vs actual `step`/`state_data`); bug survived G3, G4, G5 integration PRs undetected | Demo 7 narrated spec Guard 2 |

**NM-075 reflog evidence** — HEAD movements in main working tree, Jun 27 21:41–22:13 EDT:
```
21:41  feat/m18-g1-ci-bands         →  feat/m18-g2-psp-decomposition
21:42  feat/m18-g3-test-authorship  →  chore/m18-state-sync-012     (+ reset HEAD~1)
21:42  chore/m18-state-sync-012     →  feat/m18-g2-psp-decomposition  →  release/m18
21:49  feat/m18-g2-psp-impl         →  feat/m18-g3-intent-document   ← cross-group exit mid-G2
22:00  chore/m18-state-sync-012     →  infra/m18-sprint-branch-gate  →  release/m18
22:11  feat/m18-g2-psp-impl         →  release/m18  →  infra/m18-branch-naming-sprint
22:13  feat/m18-g1-ci-bands         →  feat/m18-g2-psp-decomposition ← cherry-pick recovery
22:13  cherry-pick: feat(m18-g2): implement PSP driver decomposition
```

---

## Part 2 — Undocumented Findings

### Finding A — G1 CI Bands Implementation Committed to G3 Branch
**Severity: High** | **NM status: Not filed**

Session `1e3802e7` began intending to implement G1 CI bands but worked entirely on `feat/m18-g3-implementation`. Implementation commit `291c5e1` landed on the G3 branch. The error was caught only at commit time when git output showed `[feat/m18-g3-implementation 291c5e1]`. Recovery: cherry-pick to `feat/m18-g1-ci-bands` (produced canonical `c7075c5`) + `git reset HEAD~1 --soft` on the G3 branch.

Reflog corroboration: `2026-06-28 07:11:52 checkout: moving from feat/m18-g1-qa-tests to feat/m18-g3-implementation` — the cross-branch jump happened mid-session, and implementation work continued undetected on the wrong branch.

NM-075 covers the concurrent working-tree interference that created the conditions; the specific wrong-branch commit event for G1 has no standalone NM entry. No process gate caught or could have caught this — the sprint group isolation model specifies branch naming and PR targeting but has no guard that validates the agent's working tree branch against the intended sprint group at session start.

---

### Finding B — Direct Commit to `release/m18`
**Severity: High** | **NM status: Not filed**

Session `74aa9f9a`: while cleaning up stash-leaked files from `feat/m18-gd-artifact5-decision4`, the session drifted onto `release/m18` and committed G3 test files there directly. Session log confirms `gitBranch: "release/m18"` at the moment of the commit. Recovery: `git reset --soft HEAD~1` → stash → checkout correct branch → stash pop → recommit.

A direct commit to `release/m18` bypasses all PR gates, CI required checks, and the sprint group isolation model. The `release-branch-ci-gate` Ruleset blocks merge-via-PR but does not prevent direct push by a user with admin rights. The recovery worked and left no incorrect artifact in `release/m18`. No process guard caught or could have caught this mid-session.

Root cause is the same multi-session working-tree interference as NM-075 but the failure mode is different: NM-075 covers branch switches overwriting in-progress work; this event covers an inadvertent commit to the protected release branch itself.

---

### Finding C — GD Stash + G1 Untracked Files Contaminating G3 Working Tree
**Severity: Medium** | **NM status: Not filed**

Session `74aa9f9a`, while on `feat/m18-g3-test-authorship`:

`git status` showed:
- **Modified (GD stash leak):** `backend/app/api/scenarios.py`, `backend/app/schemas.py`, `docs/schema/api_contracts.yml`, `docs/schema/simulation_state.yml`, `frontend/src/components/FourFrameworkZone1D.tsx`, `ScenarioInstrumentCluster.tsx`, `TrajectoryView.tsx`
- **Untracked (G1 artifacts):** `backend/app/simulation/banding_engine.py`, `backend/tests/test_m18_g1_ci_bands.py`, `frontend/tests/e2e/m18-g1-ci-bands.spec.ts`

The G1 Python files caused `ruff check .` in the pre-push hook to report I001/UP007 violations, blocking the G3 commit until `ruff check . --fix` was run against files that belonged to G1, not G3. Additionally, G3 distributional schema types (`DistributionalDifferentialRequest`) were visible in G1's working tree view, causing `mypy` `attr-defined` errors during G1 debugging.

The pre-push hook correctly blocked the G3 push, but it blocked for the wrong reason (violations in G1 files, not G3 files). An agent that ran `ruff --fix` to unblock without inspecting what was being fixed could have silently modified G1 code during a G3 session.

---

### Finding D — Merge Conflict in `near-miss-registry.md` During State-Sync-012
**Severity: Medium** | **NM status: Not filed**

Verbatim tool output from session `74aa9f9a`:
```
CONFLICT (content): Merge conflict in docs/process/near-miss-registry.md
On branch chore/m18-state-sync-012
Unmerged paths:
  both modified:   docs/process/near-miss-registry.md
```

Multiple concurrent groups were appending to the registry simultaneously (G1 NM entries, DS investigation on G3, infra branch NM-074). A conflict in an append-only file means entries from two groups occupied the same append position. One side's entries were temporarily lost from the merge candidate. The `near-miss-registry.md` is permanent institutional memory; a silently dropped entry is an integrity violation. The conflict was resolved manually in the state-sync branch, but there is no protocol that requires post-resolution verification that all entries from both sides were retained.

---

### Finding E — NM-079 and NM-080 Identified in Session But Not Yet Filed
**Severity: Medium** | **NM status: Deferred — pending G7 sprint entry**

Session `543dc2e0` references "NM-079" 37 times as "CI band fill geometry incorrect in `TrajectoryView.tsx` — fills from trajectory to chart ceiling instead of ±half-width envelope; y-axis scales to band, not trajectory values." This is now tracked as DEMO-137 (#1466, open). NM-080 is referenced 4 times with no recoverable title. Both are noted as "to be filed at G7 entry" in the session. Neither exists in the near-miss registry on any branch.

The current near-miss registry (on `origin/release/m18`) ends at NM-078. NM-079 and NM-080 are unfiled with no blocking artifact ensuring they are captured at G7 entry.

---

### Finding F — Local `release/m18` Pointer Stale by 17 Commits
**Severity: High (current-state operational risk)**

Local `release/m18` tip: `92c3bb6` (state-sync-026, ~Jun 28 17:35 EDT).
`origin/release/m18` tip: `636f931` (infra/m18-ci-integration-test-discovery, Jun 28 23:52 EDT).

17 commits missing from local pointer, including the G5 integration (#1443), state-sync-027/028, NM-078 filing, and the CI marker-discovery fix (PR #1453). Any `git merge-base sprint/m18-gX release/m18` or `git log --not release/m18` using the local pointer operates on stale data that excludes G5. The current working branch `feat/m18-g6-exit-and-g7-entry` requires a `git pull origin release/m18` before a G6 integration PR is opened or a G7 sprint branch is cut.

---

### Finding G — Abandoned Local Recovery Branch `feat/m18-g2-psp-decomposition`
**Severity: Low (cleanup)**

Created during NM-075 working tree thrash. Contains cherry-pick `37e50b9` — an alternative G2 PSP implementation that differs from the canonical `b078e7f` in `feat/m18-g2-psp-impl` (which merged via PR #1401). The branch also accumulated a bulk forward merge of `origin/release/m18` during recovery, pulling in GD GA-02 corrections, NM-074 filing, G4 sprint entry docs, and branch-naming infra — giving it a confusingly mixed ancestry. Never pushed to origin; no shared state risk. Existence creates confusion for local git operations and branch archaeology.

---

### Finding H — G3 Sprint Branch Cut Before Predecessor Scope Was Locked; Silent Scope Drift at Integration
**Severity: Medium (process signal for repeat risk)**

`sprint/m18-g3` was cut at PR #1395 merge (Jun 27, ~01:49 EDT), before G1 CI bands, G2 PSP, and all GD design package artifacts had merged to `release/m18`. The G3 → release/m18 integration resolution commit `a19c432` (33 files, Jun 28 07:46 EDT) had to simultaneously bring forward G1, G2, and GD content. Critically: the GD version on `release/m18` had Decisions 4/5/6 EL-approved (ADR-019 scope: all 7 shock types), while `sprint/m18-g3` only knew Decision 3 (6-type taxonomy). G3 implementation proceeded against stale scope for its entire sprint. The integration resolution silently upgraded it to the Decision 4/5/6 scope without G3's awareness. The resolution was functionally correct, but G3's implementation was built on a foundation that shifted under it.

This is the timing window for silent scope drift: sprint branch cut before predecessor scope decisions are locked. The sprint group isolation protocol specifies branch naming and PR targeting but has no rule requiring that scope-bearing ADR decisions be finalized on `release/m18` before a dependent sprint branch is cut.

The same timing issue required dedicated `resolve/` branches for both G1 (`resolve/m18-g1-integration`) and G3 (`resolve/m18-g3-integration`) integrations, with PR #1409 (G1 first attempt) being closed and replaced by PR #1411. Both integrations required manual conflict resolution rather than clean auto-merge.

---

### Finding I — G1 Bugfix Committed Directly to Integration Resolution Branch
**Severity: Low (no functional risk, lineage concern)**

`60806c8 fix(m18-g1): divergence fill invisible via fill=none not fillOpacity=0` was committed directly to `resolve/m18-g1-integration`, not back through `feat/m18-g1-*` → `sprint/m18-g1` → re-integration-PR. The bug was discovered when playwright-e2e failed on the integration PR. Pre-push gates ran on the resolution branch. The fix is correct. But the commit's lineage is in the integration resolution merge commit rather than the G1 sprint branch history, making it invisible in a `git log sprint/m18-g1` audit.

---

### Finding J — State-Sync-027 Submitted as Two PRs (#1440 and #1444) From Same Branch Name
**Severity: Low (pattern recurrence)**

`origin/release/m18` log contains both `5f13b0b` (Merge PR #1440) and `1d0db97` (Merge PR #1444), both from branch `chore/m18-state-sync-027`. The branch accumulated additional commits after PR #1440 merged, requiring a second PR (#1444) for the remainder. This matches the M17 duplicate-PR pattern flagged in NM-067. The split is functionally correct but continues a recurring pattern where a single state sync branch generates two PRs.

---

### Finding K — Non-Conforming Branch Name `docs/m18-g4-sprint-entry`
**Severity: Low (local scratch, no PR opened)**

Reflog shows checkout to `docs/m18-g4-sprint-entry` at Jun 27, 23:15 EDT during G3 implementation activity. Branch name doesn't conform to `feat/m18-{gN}-*`, `chore/m18-*`, or `infra/m18-*` conventions and would fail `branch-naming` CI if a PR were opened. A scratch branch created during the NM-075 thrash period, superseded by the correct `feat/m18-g4-intent-doc` branch.

---

## Part 3 — Cross-Group Contamination Matrix (Confirmed)

| Contaminating source | Contaminated destination | Evidence | Caught how |
|---|---|---|---|
| G3 branch context | G1 implementation | G1 CI bands commit `291c5e1` landed on `feat/m18-g3-implementation`; cherry-pick recovery required | Caught at commit time by agent reading git output — no process gate |
| GD stash (`feat/m18-gd-artifact5-decision4`) | G3 working tree | 7 GD-modified files in `git status` during G3 session | Pre-push hook blocked (wrong files, right gate) |
| G1 untracked files | G3 pre-push gate | `banding_engine.py`, G1 test and spec files caused ruff I001/UP007 in G3 session | Pre-push hook blocked — wrong reason |
| G3 distributional schemas | G1 working tree | `DistributionalDifferentialRequest` visible in `schemas.py` during G1 session; mypy `attr-defined` | Manual observation during G1 debugging |
| G4 ADR-019 D-3 renames | G2-era + M12/M16 E2E tests | `demo-trajectory-mode3.spec.ts` (G2), `mode3-active-control.spec.ts` (M12/M16) broken by G4 testid rename | Post-merge CI (NM-076) |
| State-sync lane | `sprint/m18-g4` via PR #1428 | Wrong-head PR from `chore/m18-state-sync-022` opened against `sprint/m18-g4` with auto-merge set | Manual inspection before auto-merge fired (NM-077) |
| G3 broken endpoint | G4, G5 integration PRs | Column name bug in `distributional-differential` survived all integration CI gates | Demo 7 narrated spec Guard 2 (NM-078) |
| `release/m18` direct commit | G3 test authorship | G3 test files committed to `release/m18`; recovered `git reset --soft HEAD~1` | Caught by agent reading its own git output — no process gate |

---

## Part 4 — Structural Observations

**The sprint group isolation model correctly isolated merge conflicts to integration PR time.** The NM-067 fix (sprint sub-branches) prevented the M17 pattern of shared-state PR overwrites. All G1–G5 integration PRs absorbed their conflicts at integration time, not during sprint execution.

**The model did not prevent in-session working tree interference.** NM-075 captured the G2 overwrite incident. Findings A, B, C, and D are three additional in-session contamination events arising from the same structural gap — multiple sessions sharing one working tree — that are not individually documented in the near-miss registry.

**Every integration PR required a dedicated `resolve/` branch or manual conflict resolution.** G1, G3, and G4 all needed resolve branches or manual merge commits. This is not a failure of the isolation model — it is evidence that the model's conflict surface is at integration time by design. But it also means integration PRs carry higher review burden than expected: each is effectively a cross-group merge review, not just a single-group code review.

**The CI gate stack had two structural gaps that allowed bugs through.** NM-073 (playwright-e2e not required on sprint branches) and NM-078 (CI didn't discover test files in `tests/` root) are both architectural gaps in the test discovery infrastructure. Both have been fixed (sprint-branch-ci-gate now exists; marker-based discovery landed via PR #1453). The fixes are in `origin/release/m18` but not in local `release/m18`.

---

## Part 5 — Immediate Required Actions

| # | Action | Reason | Command |
|---|---|---|---|
| 1 | `git pull origin release/m18` | Local pointer 17 commits stale; required before G6 integration or G7 branch cut | `git pull origin release/m18` |
| 2 | Delete abandoned recovery branch | `feat/m18-g2-psp-decomposition` carries divergent G2 implementation; local confusion risk | `git branch -d feat/m18-g2-psp-decomposition` |
| 3 | Delete scratch branch | `docs/m18-g4-sprint-entry` non-conforming name; never submitted as PR | `git branch -d docs/m18-g4-sprint-entry` |

---

## Part 6 — NM Filings Required

The following events are not covered by any existing NM entry. Each satisfies the NM threshold (process had a gap; a person caught it rather than the process):

| Finding | Proposed NM | Title | Priority |
|---|---|---|---|
| Finding A | NM-079 (or next available) | G1 CI bands committed to G3 feature branch; wrong-branch implementation commit not detected by any process gate | File at G7 sprint entry |
| Finding B | NM-080 (or next available) | Direct commit to `release/m18` by admin-rights session; `release-branch-ci-gate` Ruleset does not cover direct CLI push | File at G7 sprint entry |
| Finding H | NM-081 (or next available) | Sprint branch cut before predecessor ADR scope decisions finalized on `release/m18`; G3 implemented against stale GD scope for entire sprint; silent scope drift resolved at integration | File at G7 sprint entry |

Note: NM-079 and NM-080 are already referenced by number in session `543dc2e0` for other issues (CI band fill geometry; unknown). Actual NM numbers for Findings A, B, H must be the next available slots after NM-078. Verify registry tail before filing.

---

## Part 7 — Process Improvement Recommendations

### P1 — Branch verification at sprint session start (addresses Findings A and B)
Sprint group isolation protocol should require that each implementing session verify its working tree branch matches the expected sprint group at session open, before any file edits. Proposed addition to `docs/process/sprint-group-isolation.md §Worktree Usage`:

> At session start, confirm `git branch --show-current` matches the expected `feat/m18-gN-*` or `sprint/m18-gN` branch before any edits. If the branch does not match, do not proceed — checkout the correct branch or create the worktree before beginning work.

### P2 — Release branch push protection for direct CLI commits (addresses Finding B)
The `release-branch-ci-gate` Ruleset applies to PRs only. Add a GitHub Ruleset push restriction covering `refs/heads/release/m*` that blocks direct CLI pushes for all users including admins, or alternatively add a pre-push hook check that refuses pushes directly to `release/*`. An admin-rights direct commit to a release branch is an audit gap that the current Ruleset cannot close.

### P3 — Sprint branch cut gate: scope lock before cut (addresses Finding H)
Sprint entry template (§ scope section) should require that all in-flight ADR decisions affecting the sprint's scope are EL-approved and merged to `release/m18` before the sprint branch is cut. If a predecessor group's scope decisions are pending, the sprint branch cut must wait or document the known scope uncertainty. Add to `docs/process/sprint-planning-sop.md §Wave Kickoff Coordination Check`.

### P4 — near-miss-registry.md post-merge verification protocol (addresses Finding D)
After resolving any merge conflict in `near-miss-registry.md`, the resolving agent must verify that all NM entries from both sides of the conflict appear in the resolved file before committing. Add to `docs/process/near-miss-registry.md §Instructions for Adding Entries`: "After resolving a merge conflict in this file, count NM entries in both the incoming and current HEAD and verify the resolved file contains all entries from both sides."

### P5 — Stash hygiene before cross-branch operations (addresses Finding C)
Before switching branches, agents should verify `git stash list` is empty or that any stash contents are understood. A stash from a GD branch that survives into a G3 session can contaminate pre-push gate results and mislead debugging. Add as a step to `docs/process/sprint-group-isolation.md §Worktree Usage`.

---

*Filed by DS Agent | Session 2026-06-29 | Supersedes no prior infra review | Next review: M18 exit ceremony or on-demand*
