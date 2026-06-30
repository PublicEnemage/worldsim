# Sprint Group Isolation Protocol

> **Owner:** DevSecOps Agent (DS) — R on this document; EL is A.
> **Status:** Active — M18 onward.
> **Authority:** EL direction decisions on #1328 (SESSION_STATE.md) and #1329
> (branching model), approved 2026-06-26. Implements Option E hybrid for both.
> **Last revised:** 2026-06-26

---

## Why This Document Exists

M15–M17 ran multiple sprint groups concurrently and repeatedly produced the same
class of failures: duplicate PRs, wrong-target merges, shared-file overwrites, and
post-exit rework caused by groups stepping on each other's changes. The root cause
was a single shared integration target (the release branch) with no merge ordering,
no file-ownership enforcement, and no isolation between groups during development.

This document defines the model that replaces that. It is the authoritative reference
for every agent and every human working on a WorldSim sprint. When the instructions
here conflict with an older version of CLAUDE.md, this document takes precedence for
sprint execution — CLAUDE.md §Release Branch Workflow is updated to match.

The guiding principle is: **session boundaries are forcing functions.** Every piece of
work that happens in a session must be documented in that session. If it is not written
down, it did not happen, and it will not be acted upon. The branch topology, journal
protocol, and gate structure below are all designed to enforce this principle at the
process level — not to rely on discipline.

---

## Branch Topology

```
main
└── release/m{N}                          ← EL cuts at milestone kickoff
      ├── sprint/m{N}-g1                  ← PM Agent cuts at G1 entry
      │     ├── feat/m{N}-g1-short-name   ← implementing agent cuts per feature
      │     └── feat/m{N}-g1-other-name
      ├── sprint/m{N}-g2                  ← PM Agent cuts at G2 entry
      │     └── feat/m{N}-g2-short-name
      ├── chore/m{N}-state-sync-NNN       ← PM Agent: shared state files only
      └── infra/m{N}-short-name           ← DS Agent: .github/, .githooks/, .gitignore only
```

**Three lanes, each with a single authorized author:**

| Lane | Branch prefix | Author | What goes here |
|---|---|---|---|
| Sprint group (code) | `sprint/m{N}-g{N}` + `feat/m{N}-g{N}-*` | Implementing agent | All code and test changes for a sprint group |
| Shared state | `chore/m{N}-state-sync-NNN` | PM Agent only | `SESSION_STATE.md`, registry files, `CLAUDE.md`, `docs/insights-log.md` |
| Infrastructure | `infra/m{N}-short-name` | DS Agent only | `.github/workflows/`, `.githooks/`, `.gitignore` |

---

## The Session Continuity Contract

At session start, every agent reads these files in order (CLAUDE.md §Session Continuity):

1. `SESSION_STATE.md` — cockpit card (current milestone, open blockers, active journal issues)
2. `docs/process/agents.md`
3. `CLAUDE.md`
4. `docs/insights-log.md`
5. **Active sprint journal issue** — `gh issue view <N> --comments` where `<N>` is listed
   in SESSION_STATE.md §Cockpit "Active sprint journal issues". If none listed: skip.

The cockpit card must be readable in one pass. If it exceeds 200 lines, CI fails.
Sprint-level detail belongs in the journal issue, not the cockpit card.

---

## SESSION_STATE.md Cockpit Card Protocol

### What the cockpit card contains

The cockpit card is a program-level orientation document. It contains only:

- Current milestone name, GitHub milestone number, and exit checklist issue
- Release branch and sprint plan status
- Active wave and active sprint groups
- Pointers to active sprint journal issues (issue numbers, not content)
- Open EL decisions (≤ 5)
- M{N} entry blockers if any remain open
- Current milestone open issues (issue numbers and titles only)
- Carry-forward context: 3–5 bullets that would otherwise be lost at a session boundary

It does not contain: sprint group status, PR lists, HORIZON sweep entries, acceptance
criterion results, PI Agent confirmation text, or any content that belongs in a sprint
journal issue or exit document.

### Size enforcement

CI job `session-state-size-check` fails any PR that causes SESSION_STATE.md to exceed
200 lines. This is a hard ceiling, not a guideline. If SESSION_STATE.md is approaching
the ceiling, move content to the appropriate location:

- Sprint group progress → sprint journal issue (comment thread)
- Completed milestone history → `docs/process/session-archives/`
- Permanent process context → `CLAUDE.md` or `docs/process/`

### Archive rotation

At each milestone close, the PM Agent:

1. Copies the full `SESSION_STATE.md` to
   `docs/process/session-archives/session-state-pre-m{N+1}.md` with an archive header
2. Rewrites `SESSION_STATE.md` as a fresh cockpit card for the new milestone
3. Both files go in the same milestone close PR

Archives are permanent. Never edit or delete an archive file.

### Canonical artifact location

| Artifact | Directory | Naming |
|---|---|---|
| Session state archives | `docs/process/session-archives/` | `session-state-pre-m{N}.md` |

---

## Sprint Group Sub-Branch Protocol

### Step-by-step for each sprint group

**1. At sprint entry (PM Agent)**

Cut the sprint group sub-branch from the release branch:
```bash
git checkout -b sprint/m{N}-g{N} release/m{N}
git push -u origin sprint/m{N}-g{N}
```

Create the sprint journal issue (see §Sprint Journal Issue Protocol below).

Open the sprint entry document at:
`docs/process/sprint-plans/m{N}-g{N}-sprint-entry.md`

The entry document must be filed and EL-approved before any feature branch opens.

**2. During implementation (implementing agent)**

**Session start checklist — required before any file edits (NM-079, NM-080; Issue #1484):**

1. Confirm `git branch --show-current` matches the expected `feat/m{N}-g{N}-*` or `sprint/m{N}-g{N}` branch. If the branch does not match, checkout the correct branch or create the correct worktree before proceeding — do not begin implementation on the wrong branch.
2. Confirm `git stash list` is empty, or that all stash entries belong to the current sprint group. A stash from a different sprint group can contaminate the pre-push gate with violations from foreign files and mislead debugging. Clear or annotate stash entries before cross-branch operations.

If either check fails: stop, resolve the discrepancy, and re-confirm before writing any code.

Cut feature branches from the sprint sub-branch, not from the release branch:
```bash
git checkout -b feat/m{N}-g{N}-short-description sprint/m{N}-g{N}
```

Run pre-push gates, push, open PR targeting `sprint/m{N}-g{N}`:
```bash
gh pr create --base sprint/m{N}-g{N} --title "..." --body "..."
gh pr merge <number> --merge --auto
```

The sprint gate runs on every feature PR to `sprint/m{N}-g{N}` (triggered by `sprint/m*`
in ci.yml). Required checks: `changes`, `lint`, `test-backend`, `compliance-scan`,
`branch-naming`. `playwright-e2e` runs but is not required — it is gated at the
integration PR instead (see §CI Configuration).
After each merge, pull the sprint branch before cutting the next feature branch:
```bash
git pull origin sprint/m{N}-g{N}
```

**3. At sprint exit (implementing agent + PI Agent)**

File the sprint exit document at `docs/process/sprint-plans/m{N}-g{N}-sprint-exit.md`.

PI Agent confirms all exit conditions are met (see §PI Agent Integration PR Gate below).

Open the integration PR from the sprint branch to the release branch:
```bash
gh pr create \
  --base release/m{N} \
  --head sprint/m{N}-g{N} \
  --title "sprint(m{N}-g{N}): integration — [brief description]" \
  --body "..."
```

PI Agent posts their gate comment on the integration PR (required before merge).

Set auto-merge:
```bash
gh pr merge <number> --merge --auto
```

Pull the release branch before starting the next sprint group:
```bash
git pull origin release/m{N}
```

Close the sprint journal issue.

### Branch naming rules

| Branch type | Pattern | Example |
|---|---|---|
| Sprint sub-branch | `sprint/m{N}-g{N}` | `sprint/m18-g1` |
| Feature branch | `feat/m{N}-g{N}-short-name` | `feat/m18-g1-ci-bands` |
| Shared state | `chore/m{N}-state-sync-NNN` | `chore/m18-state-sync-001` |
| Infrastructure | `infra/m{N}-short-name` | `infra/m18-gitignore-playwright` |

The `branch-naming` CI check enforces the milestone prefix on all feature branches.

---

## Sprint Journal Issue Protocol

### Purpose

The sprint journal issue is the living session record for a sprint group. It replaces
the intra-sprint status updates that used to bloat SESSION_STATE.md. Everything that
would have gone into SESSION_STATE.md about a specific group's progress goes into its
journal issue instead.

### One issue per sprint group

Each sprint group gets exactly one journal issue, opened at sprint entry and closed at
PI Agent exit confirmation. This preserves session isolation: a group's journal thread
is the complete, ordered record of what happened in that group's sessions. If an update
is not in the journal thread, it did not happen in an authorized session.

### Creation (PM Agent, at sprint entry)

```bash
gh issue create \
  --title "sprint journal: M{N} G{N} — [sprint group description]" \
  --body "Sprint journal for M{N} G{N}. Entry document: docs/process/sprint-plans/m{N}-g{N}-sprint-entry.md
Sprint branch: sprint/m{N}-g{N}
Opened: $(date -u +%Y-%m-%d)
This issue is the intra-sprint status record for G{N}. All session progress updates,
HORIZON sweep entries, and PR status belong here — not in SESSION_STATE.md." \
  --label "documentation"
```

Record the issue number in SESSION_STATE.md §Cockpit "Active sprint journal issues".

### What goes in the journal (comment thread)

- Session start context: which agent is active, what session is picking up
- PR numbers opened and their status
- HORIZON sweep entries that are sprint-level (not program-level)
- Acceptance criterion results as they are validated
- Blockers discovered mid-sprint and how they were resolved
- PI Agent pre-exit review findings

### What does NOT go in the journal

- Code or implementation detail (that belongs in PRs and commit messages)
- Near-miss entries (those go in `docs/process/near-miss-registry.md` via PI Agent)
- Program-level decisions (those go in SESSION_STATE.md §Open EL Decisions)

### Closure (PI Agent, at sprint exit confirmation)

PI Agent closes the journal issue after posting their integration PR gate comment.
The closure comment must reference the sprint exit document:

```
Sprint G{N} exit confirmed. Exit document: docs/process/sprint-plans/m{N}-g{N}-sprint-exit.md.
Integration PR merged. Journal closed.
```

---

## File Authority During Sprint Isolation

The primary failure mode in M15–M17 was groups writing to the same files concurrently.
The rule is simple: **each file has exactly one lane it may be written from.**

### Shared state files — PM Agent coordination lane only

Files that every sprint group reads but only the PM Agent may write during sprint execution:

- `SESSION_STATE.md`
- `docs/process/near-miss-registry.md`
- `docs/compliance/scan-registry.md`
- `docs/compliance/exceptions.md`
- `CLAUDE.md`
- `docs/insights-log.md`
- `docs/process/agents.md` and `docs/process/agent-raci.md`

**When a sprint group's work requires an update to a shared file:**
The implementing agent signals the PM Agent with a comment in the sprint journal issue:
> "PM Agent coordination needed: [description of required shared-file update]"

The PM Agent opens a `chore/m{N}-state-sync-NNN` PR targeting `release/m{N}`, applies
the change, and sets auto-merge. Sprint groups do not write to shared files directly.

### DS-owned infrastructure files — DS infra lane only

- `.github/workflows/`
- `.githooks/`
- `.gitignore`
- `docs/process/sprint-group-isolation.md` (this document)
- `docs/compliance/infra-reviews/`

**When a sprint group's implementation requires a change to a DS-owned file:**
The implementing agent activates DS: `DevSecOps Agent: CONFIGURE — [description]`

DS opens an `infra/m{N}-short-name` PR targeting `release/m{N}`, applies the change,
and sets auto-merge. The implementing agent's sprint branch picks up the change via:
```bash
git pull origin release/m{N}
```
after the infra PR merges.

### Code and test files — sprint sub-branch

Everything else: all files under `backend/`, `frontend/`, `docs/` (except shared state
files listed above), `docs/process/intents/`, `docs/process/sprint-plans/`, ADRs, etc.
These live in feature branches targeting the sprint sub-branch.

---

## PM Agent Coordination Lane

### When to use it

Any time a sprint group's work requires an update to a shared state file (see list
above). Common triggers:

- Sprint exit: SESSION_STATE.md cockpit update after a group exits
- Registry entries: near-miss, scan, or exception entries generated by a sprint group
  (the implementing agent files the content; PI Agent writes the registry entry)
- CLAUDE.md updates: process improvements that apply to all future sprints

### Protocol

1. PM Agent creates branch `chore/m{N}-state-sync-NNN` from `release/m{N}`
2. Applies the shared-file update(s)
3. Opens PR targeting `release/m{N}` with title: `chore(state-sync): [description]`
4. Sets auto-merge: `gh pr merge <number> --merge --auto`
5. No PI Agent gate required for state-sync PRs — CI green is sufficient

### Sequencing

State-sync PRs must be ordered. If two sprint groups exit in the same session and both
need SESSION_STATE.md updates, the PM Agent applies them sequentially in one PR, not
two concurrent PRs. Apply the first group's update, confirm merge, pull, apply the
second.

---

## PI Agent Integration PR Gate

### Purpose

The integration PR (`sprint/m{N}-g{N}` → `release/m{N}`) is the gate where undocumented
work would reach the release branch. PI Agent sign-off on this PR is the written
assertion, at the git level, that exit conditions have been met. Without it, a
technically passing implementation without a filed exit document could merge silently.

### Required for every integration PR — no exceptions

CI-green alone does not authorize an integration PR to merge. PI Agent must post a
gate comment on the PR before auto-merge can fire.

### What the gate comment must contain

```markdown
## PI Agent — Integration PR Gate

**Sprint group:** M{N} G{N}
**Exit document:** `docs/process/sprint-plans/m{N}-g{N}-sprint-exit.md` — FILED ✅
**Business PO acceptance:** [ACCEPT on #{issue} / N/A — infrastructure sprint]
**Customer Agent Layer 3:** [PASS / N/A — no Persona 2/3/5 deliverable]
**North star test:** [PASS / N/A — infrastructure sprint]
**Open rejection artifacts:** None ✅
**Near-miss sweep:** [NM-NNN filed / None identified]

**PI Agent verdict: EXIT CONDITIONS MET — integration PR authorized to merge.**
```

If any condition is not met, PI Agent posts a BLOCKED verdict and lists the unresolved
items. The integration PR must not merge until PI Agent posts an unblocked verdict.

### How to implement the gate in practice

Auto-merge is set on the integration PR immediately after opening. GitHub will merge
as soon as CI passes AND the PI Agent gate comment is posted. But GitHub's auto-merge
does not know about the PI Agent comment — it merges when CI passes regardless.

**The gate is enforced by discipline, not by a GitHub check.** The implementing agent
must wait for PI Agent's gate comment before the session can be considered complete.
If auto-merge fires before PI Agent posts, the sprint exit has a process violation —
file a near-miss entry.

*Future improvement: a GitHub Actions workflow that checks for the PI Agent gate
comment pattern and fails a required check until the comment is present would enforce
this mechanically. DS holds R for implementing that workflow when capacity allows.*

---

## Cross-Group Dependency Protocol

### Declaration at sprint entry

When a sprint group depends on the output of another group, the dependency must be
declared in the sprint entry document's "Cross-group dependencies" field (see sprint
entry template §Section 6). Example:

> G2 depends on G1: requires ELASTICITY_REGISTRY changes from G1's sprint branch
> to be on `release/m{N}` before G2's implementation branch is cut.

### Merge sequence

A group with an upstream dependency must not cut its sprint sub-branch until the
upstream group's integration PR has merged to `release/m{N}`. The sequence is:

1. G1 sprint sub-branch → integration PR → merges to `release/m{N}`
2. G2 cuts `sprint/m{N}-g2` from updated `release/m{N}` (picks up G1's changes)

If G2 needs G1's changes mid-sprint (before G1's exit), G2 may rebase onto G1's sprint
sub-branch. This is a deliberate decision that must be documented in the sprint journal:
> "G2 rebased onto sprint/m{N}-g1 to pick up [specific change]. This creates a merge
> ordering dependency: G1 integration PR must merge before G2 integration PR."

---

## CI Configuration

### Two-tier CI gate model

WorldSim uses a two-tier CI gate to enforce fast feedback on sprint branches while
reserving the expensive E2E suite for the integration PR:

| Gate | Branch pattern | Ruleset | Required checks |
|---|---|---|---|
| Sprint gate | `sprint/m*` | `sprint-branch-ci-gate` | `changes`, `lint`, `test-backend`, `compliance-scan`, `branch-naming` |
| Release gate | `release/m*` | `release-branch-ci-gate` | all of the above **+ `playwright-e2e`** |

**Why `playwright-e2e` is not required on sprint branches:**
The test authorship gate (sprint entry §2.4) requires QA tests to be filed before
implementation opens — producing intentionally failing (RED) playwright tests. If
`playwright-e2e` were required on sprint branches, test authorship PRs could never
merge via auto-merge. The E2E gate lives at the integration PR instead, where tests
are expected to be GREEN (implementation complete).

This design was established in response to NM-073 (`docs/process/near-miss-registry.md`).

### `sprint/m*` trigger

`ci.yml` triggers CI on `pull_request` events targeting `sprint/m*` branches.
Feature PRs inside a sprint group get CI coverage at the sprint gate level, with
`playwright-e2e` deferred to the integration PR. The change management arc for
M18 onward is:

```
local pre-push gates (ruff/mypy/build)
  → sprint gate on every feat/m{N}-g{N}-* PR to sprint/m{N}-g{N}
    (changes, lint, test-backend, compliance-scan, branch-naming — no playwright-e2e)
    → release gate on integration PR sprint/m{N}-g{N} → release/m{N}
      (all checks including playwright-e2e)
```

Defects in lint, types, and unit tests surface at the sprint gate. Behavioral
regressions caught by E2E tests surface at the integration PR gate.

### SESSION_STATE.md size check

CI job `session-state-size-check` runs on every PR and fails if SESSION_STATE.md
exceeds 200 lines. This job always runs — it is not gated on path filters.

The 200-line ceiling gives 50 lines of headroom above the 150-line soft target.
If the check fails: archive historical content, do not increase the ceiling.

### CI cost

With `sprint/m*` added as a trigger, CI runs on every feature PR inside a sprint group
in addition to the integration PR. For a 4-group milestone with 3 feature PRs per group,
this adds approximately 12 additional CI runs. All jobs use path-filtering (`changes`
job) so docs-only feature PRs within a sprint branch skip the expensive
`test-backend`, `playwright-e2e`, and `backtesting` jobs. Actual compute cost is
proportional to what each feature PR changes, not to the number of PRs.

---

## Quick Reference

**Cutting a sprint sub-branch:**
```bash
git checkout -b sprint/m{N}-g{N} release/m{N} && git push -u origin sprint/m{N}-g{N}
```

**Cutting a feature branch inside a group:**
```bash
git checkout -b feat/m{N}-g{N}-name sprint/m{N}-g{N}
```

**Opening a feature PR (targets sprint branch, not release):**
```bash
gh pr create --base sprint/m{N}-g{N} ... && gh pr merge <N> --merge --auto
```

**Opening an integration PR (requires PI Agent gate comment before merge):**
```bash
gh pr create --base release/m{N} --head sprint/m{N}-g{N} ... && gh pr merge <N> --merge --auto
```

**Requesting a shared-state update (PM Agent coordination lane):**
Post in sprint journal issue: "PM Agent coordination needed: [description]"

**Requesting a DS-owned file change (DS infra lane):**
`DevSecOps Agent: CONFIGURE — [description]`

**Checking CI in real time (streaming, not polling):**
```bash
gh run watch $(gh run list --branch <branch> --limit 1 --json databaseId --jq '.[0].databaseId') --exit-status
```
