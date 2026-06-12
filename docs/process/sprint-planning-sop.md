---
name: sprint-planning-sop
type: process-sop
owner: PM Agent
status: Active
first-applied: M12
---

# Sprint Planning SOP

**Owner:** PM Agent (R)  
**Accountable:** Engineering Lead (A)  
**Required Consultants:** Business Product Owner, Frontend Architect, Chief Engineer, Architect  
**Activation:** `PM Agent: SPRINT — [milestone]`

---

## Purpose

Produces a sprint plan document at milestone kickoff that organizes all milestone issues into implementation groups optimized for shared file areas, PR atomicity, dependency sequencing, and test co-location. The sprint plan is the primary implementation guide for the milestone — it replaces ad-hoc group decisions and makes the sequencing rationale permanent and auditable.

Sprint planning is a process the PM Agent owns. It is not a solo exercise — PM consults domain agents before producing a plan, and EL approves before work begins.

---

## Trigger Conditions

Sprint planning is triggered at **milestone kickoff**, immediately after:

1. The HORIZON sweep (scope-completeness check) confirms all deliverables are tracked
2. All roadmap deliverables have linked GitHub issues (Scope Linkage Requirement, NM-019)
3. The milestone exit checklist issue is filed

Sprint planning may be re-triggered mid-milestone if:
- More than 30% of the milestone's issues are re-scoped or added after kickoff
- A major architectural decision (ADR acceptance) materially changes the implementation sequence
- EL requests a re-plan

---

## Input Documents

| Input | Where to find it |
|---|---|
| Milestone issue board | GitHub milestone — current milestone |
| Roadmap deliverables | `docs/roadmap/worldsim-roadmap.md §Milestone by Milestone` |
| HORIZON sweep output | `SESSION_STATE.md §Open Issues — M{N}` |
| File ownership table | `docs/process/agent-raci.md §File Ownership` |
| ADR backlog | `docs/architecture/backlog.md` |
| Current architecture | Relevant ADRs in `docs/adr/` |

---

## Consultation Sequence

PM Agent runs four consultations before producing a draft plan. Consultations are issue-scoped — not open-ended requests for opinion.

### 1. Business Product Owner — Value prioritization

`Business Product Owner: PRIORITIZE — [milestone name]`

**Ask:** Given the milestone issue board, which groups of issues are the highest user-value priority? Which issues, if delayed to the end, would most damage the canonical user's experience if a milestone-close scope cut were needed?

**Output informs:** Group sequencing within each wave. High-value groups go in earlier waves where possible.

### 2. Frontend Architect — File area grouping

`Frontend Architect: REVIEW — sprint grouping for [milestone name]`

**Ask:** Review the proposed frontend issue groupings for file area overlap. Are there issues being placed in separate groups that would produce merge conflicts or shared component churn? Are there issues in the same group that touch incompatible file areas and should be split?

**Output informs:** G1/G2/G3 groupings and which frontend features share TrajectoryView, App.tsx, or zone components.

### 3. Chief Engineer — Backend dependency sequencing

`Chief Engineer: REVIEW — sprint dependency chain for [milestone name]`

**Ask:** Review the proposed backend issue groupings for dependency correctness. Are there hidden performance or schema dependencies between groups that affect sequencing? Is the critical path correctly identified?

**Output informs:** Wave 2 and Wave 3 sequencing; any group split or merge recommendations on the backend side.

### 4. Architect — ADR prerequisites

`Architect: REVIEW — ADR prerequisites for [milestone name]`

**Ask:** For each group in the proposed sprint plan, is there an ADR that must be authored and accepted before implementation begins? Identify any group whose implementation would violate the "no significant feature without an ADR" rule if it proceeded without a new or amended ADR.

**Output informs:** ADR prerequisite section of the sprint plan. Any group with an unresolved ADR prerequisite is flagged as `BLOCKED_ADR` until the ADR is accepted.

---

## Grouping Criteria

When producing groups, apply these criteria in order:

1. **Same file area first.** Issues touching the same primary files go in the same group unless a dependency conflict prevents it. This minimizes merge friction and keeps PR scope coherent.

2. **Tests ship with the code.** No group produces a PR with implementation but no tests. No group produces a "test-only" follow-up PR. Tests are part of the group, not a cleanup task.

3. **Playwright E2E assertions ship in the same PR as the feature they gate.** A feature whose acceptance criteria includes a UI assertion must have that assertion written before the PR merges.

4. **Dependencies determine waves.** A group that depends on another goes in a later wave. A group with no dependencies goes in Wave 1 (parallel).

5. **ADR prerequisites are surfaced explicitly.** Any group requiring an ADR or ADR amendment is marked. The ADR must be accepted before the group's implementation PR merges — not before the group begins, but before it closes.

6. **Group size.** A group should be implementable and reviewable in a single PR. If a group grows to more than ~800 lines of diff, consider splitting it at a natural boundary (e.g., G6a backend / G6b frontend). The split must maintain clean ordering — G6a merges before G6b begins.

---

## Sprint Plan Document Format

Sprint plan documents live at `docs/process/sprint-plans/{milestone-slug}-sprint-plan.md`.

Required sections:
- Frontmatter: name, type, milestone, status, authored-by, authored-date, el-approved, consulted agents, SOP reference
- Grouping rationale (one paragraph — why groups were formed this way)
- One section per group: why grouped, shared files, tests, acceptance gates, what it gates
- Near-term backlog: issues that are on the milestone but not in any wave
- Dependency map: visual wave structure + critical path identification
- ADR prerequisites: explicit table of which groups require which ADRs

---

## EL Approval Gate

The draft sprint plan is presented to the Engineering Lead before implementation begins. EL reviews:

1. Are the groupings reasonable? (May redirect groupings)
2. Is the sequencing correct? (May change wave assignments)
3. Are there scope items missing from the plan? (Check against roadmap)

EL approval is recorded as a comment on the milestone exit checklist issue, or as the `el-approved` date in the sprint plan frontmatter.

---

## Relationship to Release Branch

The sprint plan and the release branch are created at the same time, at milestone kickoff. The release branch (`release/m{N}`) is the integration target for all feature branches during the milestone. Feature branches open PRs targeting the release branch — not `main`. This allows PM Agent to close groups autonomously once CI is green.

When the sprint plan is approved:
1. PM Agent creates `release/m{N}` from `main`
2. **CI trigger verification (mandatory):** Confirm that `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` (or the specific release branch pattern). If the CI workflow does not cover the new release branch, update it before opening any feature PRs. Root cause: NM-035 — M12 ran 7 groups without CI triggering because this check did not exist.
3. Feature branches are cut from `release/m{N}`
4. Groups are worked in wave order
5. EL does one admin bypass at milestone close: `release/m{N}` → `main`

---

## Updating the Sprint Plan Mid-Milestone

If scope changes materially after kickoff:

- Add or modify a group section with a `**Revised: [date]**` note explaining what changed and why
- Update the wave structure if dependencies change
- Re-run the Architect consultation if an ADR prerequisite is added or removed
- EL must confirm any wave reassignment that changes the critical path

Sprint plan documents are not silently overwritten. Changes are visible through the revision markers and git history.

---

## Sprint Entry Gate

*Authority: Phase C output (2026-06-12).
Changes to this section require PI Agent review and EL endorsement.*

A sprint does not open when issues exist and a sprint plan is drafted. A sprint opens when
the following conditions are all confirmed. Confirmation is recorded in the sprint entry
document at `docs/process/sprint-plans/{milestone-slug}-sprint-{N}-entry.md`.

### Entry Conditions

1. **Sprint entry document filed and EL-approved.** The PM Agent fills out the sprint entry
   template (`docs/process/sprint-plans/templates/sprint-entry-template.md`) and files it at
   the canonical location. The EL approves the entry document before any implementation PR
   opens — either by adding the `el-approved` date in the frontmatter or confirming approval
   on the exit checklist issue. An implementation PR opened before entry document approval is
   a process deviation.

2. **Release branch exists with CI trigger verified.** `release/m{N}` is cut from `main` and
   the `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*`. This check
   is recorded in the entry document Section 2.1. Root cause: NM-035 — M12 ran 7 groups
   without CI triggering because this check did not exist before.

3. **ADR prerequisites clear for groups opening in this sprint.** For each sprint group
   marked `BLOCKED_ADR` in the sprint plan, the required ADR must be accepted before the
   group's implementation PR opens. Groups with unresolved ADR prerequisites do not open.
   This is recorded in the entry document Section 4.

4. **Intent document filed for each user-facing deliverable.** For each deliverable whose
   primary output is user-facing (frontend feature, backend capability, documentation,
   analytics output), an intent document is filed at
   `docs/process/intents/ADR-NNN-YYYY-MM-DD-short-name.md` before the implementation PR
   opens. The intent document completeness gate: the QA Lead can write a test from it without
   reading implementation code. (Authority: CLAUDE.md §Agent Execution Lifecycle Step 1)

5. **QA test file authored for each user-facing deliverable before implementation begins.**
   The QA Lead writes tests from the intent document's acceptance criteria before any
   implementation code is written. The test file is on record before the implementing agent
   begins implementation work on the deliverable. (Authority: CLAUDE.md §Agent Execution
   Lifecycle Step 2)

### Who Confirms the Sprint Entry Gate

| Role | Responsibility at entry |
|---|---|
| PM Agent | Files sprint entry template; confirms all five conditions are satisfied; routes to EL for approval |
| QA Lead Agent | Consulted on the test authorship invariant — confirms tests can be authored from the intent document and that they are authored before implementation |
| PI Agent | Files a near-miss immediately if a sprint begins implementation without a complete entry document |
| Engineering Lead | Approves the sprint entry document before implementation begins |

### What "The Sprint Plan Is Approved" Does Not Substitute For

- An approved sprint plan does not substitute for a filed sprint entry document.
- EL approval of the sprint plan does not substitute for EL approval of the sprint entry document.
- The sprint plan describes what will be built; the sprint entry document confirms the
  preconditions under which building may begin are satisfied.

These are sequential, not parallel. Sprint plan approval is a prerequisite for the entry
document; it does not replace it.

### Infrastructure Sprint Exception

If a sprint's primary deliverables are infrastructure (no user-facing outputs), the PM Agent
declares "infrastructure sprint" in the sprint entry document Section 2. In that case:
- Intent document gate (condition 4) does not apply
- QA test authorship gate (condition 5) does not apply
- Business PO acceptance is not required at exit for those deliverables
- Customer Agent Layer 3 assessment is not required at exit

The PI Agent reviews this declaration at the exit gate. If any declared-infrastructure
deliverable produces user-visible output, it is not infrastructure and the gates apply
retroactively. PI Agent files a near-miss for any infrastructure declaration that was
incorrect.

### Sprint Entry Artifact

The sprint entry artifact is the proof that all entry conditions were confirmed before
implementation began. It is filed at
`docs/process/sprint-plans/{milestone-slug}-sprint-{N}-entry.md`.

Template: `docs/process/sprint-plans/templates/sprint-entry-template.md`

---

## Sprint Exit Gate

*Authority: `docs/process/acceptance-protocol.md` (Phase B output).
Updated 2026-06-12 per Phase B. Changes to this section require PI Agent review and EL endorsement.*

A sprint does not close when all implementation groups are merged and CI is green. A sprint
closes when the following conditions are all satisfied:

### Exit Conditions

1. **All implementation groups are merged to the release branch** with CI green on the release
   branch. This is necessary but not sufficient.

2. **Business PO acceptance is recorded for every user-facing deliverable.** For each sprint
   group whose primary output is a frontend feature, backend capability, documentation, or
   analytics output, the Business PO must have executed the Validate step (Step 5 of the Agent
   Execution Lifecycle) using the per-type verification protocol in
   `docs/process/acceptance-protocol.md`. The Business PO verdict artifact (ACCEPT or REJECT)
   must be filed and on record before the sprint exit gate passes.

3. **No open rejections.** If any Business PO verdict is REJECT, the rejection artifact must be
   resolved — either by re-acceptance (Business PO files re-acceptance verdict) or by EL
   exception (EL appends exception to rejection artifact). A sprint with an unresolved rejection
   artifact does not exit.

4. **Customer Agent Layer 3 assessment on record** for any deliverable serving Personas 2, 3,
   or 5. This is a precondition for the Business PO verdict, but PI Agent confirms it is present
   before signing off the sprint exit.

5. **PI Agent sprint exit confirmation.** PI Agent reviews the exit conditions and confirms all
   are satisfied before the sprint exit checklist issue is closed. PI Agent does not produce the
   verdicts — PI Agent confirms they exist and are complete.

### Who Closes the Sprint Exit Gate

| Role | Responsibility at exit |
|---|---|
| Business PO | Produces ACCEPT/REJECT verdicts for all user-facing deliverables |
| Customer Agent | Produces Layer 3 assessment for Persona 2/3/5 deliverables (before Business PO verdict) |
| PI Agent | Confirms all exit conditions are satisfied; files near-miss for any rejection; blocks exit if any condition is unmet |
| Engineering Lead | Approves EL exceptions for any unresolved rejections; closes the milestone exit checklist issue |

### What "CI Green" Does Not Substitute For

- CI green does not substitute for a Business PO ACCEPT verdict.
- A passing unit test suite does not substitute for the observable application state check.
- A passing Playwright test does not substitute for the Business PO confirming the named persona
  can reach the observable state within the P-4 time ceiling.

These checks are complementary, not substitutable. CI confirms implementation correctness.
Business PO acceptance confirms mission alignment. Both are required before sprint exit.

### Sprint Exit Artifact

The sprint exit artifact is the proof that all exit conditions were satisfied. For process
redesign sprints, see the phase exit document pattern (e.g., `process-redesign-phaseA-exit.md`).
For M{N} milestone sprints, the sprint exit artifact is a sprint exit document filed at
`docs/process/sprint-plans/{milestone-slug}-sprint-{N}-exit.md` using the template at
`docs/process/sprint-plans/templates/sprint-exit-template.md`. The document must include:

- [ ] All implementation groups merged; CI green on release branch
- [ ] Business PO ACCEPT verdict filed for each user-facing deliverable (or EL exception on record)
- [ ] Customer Agent Layer 3 assessment on record for Persona 2/3/5 deliverables
- [ ] No open rejection artifacts
- [ ] PI Agent sprint exit confirmation (Section 5 of the exit template)

The PI Agent reviews this document and records the confirmation in Section 5 before the sprint
exit checklist issue closes. The milestone exit checklist issue comment on GitHub references
the sprint exit document — it does not replace it.

*Updated 2026-06-12 per Phase C: sprint exit is now a standalone filed document, not only an
issue comment. Prior sprints that used issue comments as their sole exit record are
grandfathered; Phase C applies to M13 and subsequent milestones.*
