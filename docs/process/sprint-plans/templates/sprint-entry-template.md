---
name: {milestone-slug}-sprint-{N}-entry
type: sprint-entry
milestone: M{N} — {milestone name}
sprint-group: {G1/G2/... or "all groups" for full-milestone plans}
status: Filed
authored-by: PM Agent
authored-date: {YYYY-MM-DD}
el-approved: false
release-branch: release/m{N}
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — {Milestone Name}, Sprint {N}

**Status:** Filed — awaiting EL approval before implementation begins
**Date authored:** {YYYY-MM-DD}
**Release branch:** `release/m{N}`
**Sprint plan:** `docs/process/sprint-plans/{milestone-slug}-sprint-plan.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
Changes to this template require PM Agent authorship and EL endorsement.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M{N} — {milestone name} |
| GitHub Milestone | #{github-milestone-number} |
| Sprint number | {N} |
| Release branch | `release/m{N}` |
| Sprint plan document | `docs/process/sprint-plans/{milestone-slug}-sprint-plan.md` |
| Exit checklist issue | #{exit-checklist-issue-number} |
| Sprint groups in scope | {G1, G2, G3, …} |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for this sprint.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [ ] **Release branch exists:** `release/m{N}` cut from `main` at milestone kickoff
- [ ] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*`
  (Root: NM-035 — M12 ran 7 groups without CI triggering because this check did not exist)
- [ ] **Sprint plan EL-approved:** `docs/process/sprint-plans/{milestone-slug}-sprint-plan.md`
  has `el-approved` date in frontmatter, or EL approval recorded on exit checklist issue

### 2.2 — ADR prerequisite gate

*For each sprint group that requires an ADR (per sprint plan §ADR Prerequisites), the ADR
must be accepted before the group's implementation PR merges. If no groups require a new ADR,
check "N/A" and note below.*

- [ ] All groups with `BLOCKED_ADR` status in the sprint plan have their required ADR accepted, or the ADR is explicitly listed as in-progress with a named target acceptance date

**ADR prerequisite status:**

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| {G1} | {ADR-NNN or N/A} | {Accepted / In-progress / N/A} | {CLEAR / BLOCKED_ADR} |
| {G2} | {ADR-NNN or N/A} | {Accepted / In-progress / N/A} | {CLEAR / BLOCKED_ADR} |

### 2.3 — Intent document gate

*For each user-facing deliverable in this sprint, an intent document must be filed at
`docs/process/intents/M{N}-{G-suffix-or-ADR-NNN}-{YYYY-MM-DD}-{short-name}.md` before implementation begins.
(Authority: docs/process/agent-execution-lifecycle.md Step 1)*

- [ ] Intent document filed for every user-facing deliverable in this sprint

**Intent document status:**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| {deliverable 1} | {ADR-NNN} | `docs/process/intents/{path}` | {Yes / No — BLOCKING} |
| {deliverable 2} | {ADR-NNN} | `docs/process/intents/{path}` | {Yes / No — BLOCKING} |

*If no user-facing deliverables are in this sprint (infrastructure only), note "Infrastructure sprint — no user-facing deliverables — intent documents not required."*

### 2.4 — QA test authorship gate

*For each user-facing deliverable, QA tests must be authored from the intent document's
acceptance criteria BEFORE implementation code is written.
(Authority: docs/process/agent-execution-lifecycle.md Step 2)*

- [ ] QA test file authored for every user-facing deliverable in this sprint

**QA test status:**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| {deliverable 1} | `docs/process/intents/{path}` | `frontend/tests/e2e/m{N}-g{N}-{short-name}.spec.ts` or `backend/tests/test_m{N}_g{N}_{short_name}.py` | {Yes / No — BLOCKING} |
| {deliverable 2} | `docs/process/intents/{path}` | `frontend/tests/e2e/m{N}-g{N}-{short-name}.spec.ts` or `backend/tests/test_m{N}_g{N}_{short_name}.py` | {Yes / No — BLOCKING} |

*If infrastructure sprint: "Infrastructure sprint — no user-facing deliverables — test authorship gate not required for these groups."*

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

*All issues assigned to this sprint, with group assignment.*

| Issue | Title | Group | Priority |
|---|---|---|---|
| #{number} | {title} | {G1} | {immediate / near-term} |
| #{number} | {title} | {G2} | {immediate / near-term} |

### 3.2 — Issues explicitly out of scope

*Issues on the milestone board that are NOT in this sprint, with rationale.*

| Issue | Title | Horizon | Rationale for exclusion |
|---|---|---|---|
| #{number} | {title} | {near-term} | {Deferred to next sprint — dependency on G3 output} |

---

## Section 4 — ADR Prerequisite Summary

*Explicit table of which groups require which ADRs, per sprint-planning-sop.md §Grouping Criteria #5.*

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| {G1} | {ADR-NNN or N/A} | {Accepted / In-progress} | {Yes / No — awaiting ADR acceptance} |
| {G2} | None | N/A | Yes |

*Groups marked "No" under "Implementation may begin?" are BLOCKED_ADR. Their feature PRs must not open until the required ADR is accepted.*

---

## Section 5 — Near-Miss Sweep

*Any process gaps identified since the previous sprint closed. Each finding is a REGISTER call
to the PI Agent — PM Agent does not write registry entries directly.*

**Near-miss sweep date:** {YYYY-MM-DD}
**Sweep period:** Since {previous sprint close date}

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| {description or "None"} | {near-miss / known-issue / N/A} | {Yes / N/A} | {NM-NNN or N/A} |

*If no findings: "No process gaps identified in the sweep period."*

---

## Section 6 — Sprint Group Isolation (M18 onward)

*Required for every sprint group under the sprint group isolation protocol.
Authority: `docs/process/sprint-group-isolation.md`.*

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m{N}-g{N}` |
| Cut from | `release/m{N}` |
| Sprint journal issue | #{TBD — PM Agent creates at entry} |

**PM Agent sprint sub-branch cut command:**
```bash
git checkout -b sprint/m{N}-g{N} release/m{N} && git push -u origin sprint/m{N}-g{N}
```

### 6.2 — File-conflict risk assessment

*List every shared state file or DS-owned file this group will need to write.
Shared state files route through the PM Agent coordination lane.
DS-owned files route through the DS infra lane.
Never write to these files directly from a feature branch.*

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified |
| `docs/compliance/scan-registry.md` | PM Agent coordination lane | If compliance scan produced |
| {any DS-owned file} | DS infra lane | {describe the needed change} |
| {code/test files} | Sprint sub-branch (no coordination needed) | — |

*If this sprint group writes no shared state files and requires no DS-owned file changes,
write: "No shared-file conflicts anticipated. All writes are to code and test files."*

### 6.3 — Infrastructure dependency declaration

*Does this sprint group's implementation require a change to a DS-owned file
(`.github/workflows/`, `.githooks/`, `.gitignore`)?*

- [ ] No DS-owned file changes required
- [ ] Yes — DS infra lane required (activate: `DevSecOps Agent: CONFIGURE — [description]`)

**If yes, describe the required change and which DS deliverable must merge before
implementation can begin:**

> {description or "N/A"}

#### 6.3a — New output paths declaration (NM-069 process improvement)

*Does this sprint group's implementation generate any new output directories not currently
covered by `.gitignore`? (Examples: new test artifact paths, benchmark output directories,
report directories.)*

- [ ] No new output directories — all generated paths are already covered by `.gitignore`
- [ ] Yes — `.gitignore` update required (see below)

**If yes, list each new output directory and confirm it will be added to `.gitignore` in the
same implementation PR (or as a DS infra lane PR that merges before the generating code):**

| New output path | Already in `.gitignore`? | Action |
|---|---|---|
| {e.g. `backend/reports/`} | {Yes / No} | {None / Add to .gitignore in same PR / DS infra lane PR} |

*If no new output paths: "No new output directories introduced by this sprint group."*

### 6.4 — Cross-group dependency declaration

*Does this sprint group depend on the output of another active sprint group?*

- [ ] No cross-group dependencies
- [ ] Yes — dependency declared below

**If yes, state the upstream group, what output is required, and the merge ordering constraint:**

> {e.g. "G2 depends on G1: requires ELASTICITY_REGISTRY changes from G1's sprint branch
> to be on release/m{N} before G2's sprint/m{N}-g2 sub-branch is cut."}

### 6.5 — Prior NM verification (NM-068 process improvement)

*For each near-miss entry filed since the previous sprint closed, confirm whether the
process improvement it mandated has been applied to this sprint's execution.*

**NM verification sweep date:** {YYYY-MM-DD}
**Sweep period:** Since {previous sprint close date}

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| {NM-NNN} | {brief description of required process change} | {Yes / N/A — does not apply to this group} |

*If no NM entries are open with applicable process improvements: "No applicable NM process
improvements identified since previous sprint close."*

---

## EL Approval Record

*EL reviews this entry document before any implementation PR opens. Approval is recorded here
or as a comment on the exit checklist issue #{exit-checklist-issue-number}.*

**EL approval:** Pending

> {EL approval statement — to be filled at approval time}
> — @PublicEnemage ({date})
