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
`docs/process/intents/ADR-NNN-YYYY-MM-DD-short-name.md` before implementation begins.
(Authority: CLAUDE.md §Agent Execution Lifecycle Step 1)*

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
(Authority: CLAUDE.md §Agent Execution Lifecycle Step 2)*

- [ ] QA test file authored for every user-facing deliverable in this sprint

**QA test status:**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| {deliverable 1} | `docs/process/intents/{path}` | `{backend or frontend test path}` | {Yes / No — BLOCKING} |
| {deliverable 2} | `docs/process/intents/{path}` | `{backend or frontend test path}` | {Yes / No — BLOCKING} |

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

## EL Approval Record

*EL reviews this entry document before any implementation PR opens. Approval is recorded here
or as a comment on the exit checklist issue #{exit-checklist-issue-number}.*

**EL approval:** Pending

> {EL approval statement — to be filled at approval time}
> — @PublicEnemage ({date})
