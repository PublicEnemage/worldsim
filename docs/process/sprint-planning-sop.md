---
name: sprint-planning-sop
type: process-sop
owner: PM Agent
status: Active
first-applied: M12
last-revised: 2026-06-27
revision-authority: NM-072 — upstream gate clause for pre-wave design packages
---

# Sprint Planning SOP

**Owner:** PM Agent (R)  
**Accountable:** Engineering Lead (A)  
**Required Consultants:** Business Product Owner, Frontend Architect, Computation Engine Agent, Architect, DevSecOps Agent  
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

### 3. Computation Engine Agent — Backend dependency sequencing

`Computation Engine Agent: REVIEW — sprint dependency chain for [milestone name]`

**Ask:** Review the proposed backend issue groupings for dependency correctness. Are there hidden performance or schema dependencies between groups that affect sequencing? Is the critical path correctly identified?

**Output informs:** Wave 2 and Wave 3 sequencing; any group split or merge recommendations on the backend side.

### 4. DevSecOps Agent — Infrastructure and dependency review

`DevSecOps Agent: REVIEW — sprint dependency and output-path assessment for [milestone name]`

**Ask:** For each proposed sprint group: (1) Does the group introduce a new Python or npm dependency? If yes, confirm CVE status and license. (2) Does the group introduce a new test framework or output directory? If yes, confirm `.gitignore` coverage is planned for the same PR. (3) Does the group change CI/CD configuration? If yes, confirm the change is compatible with the Equitable Build Process hardware targets.

**Output informs:** Sprint entry template "Prior NM applicability check" field for infrastructure-class groups; any group flagged `NEEDS_GITIGNORE_UPDATE` or `DEPENDENCY_CVE_REVIEW` is noted before EL approves.

### 5. Architect — ADR prerequisites

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

**UX Designer sign-off session practice for Tier 1 ADRs:** For Tier 1 ADRs, the preferred
practice is to obtain the UX Designer sign-off in a separate EL-triggered session after the
ADR is committed as `Proposed`. This eliminates authoring-context bleed — the reviewing agent
reads the ADR cold, without the authoring session's reasoning in its context window, producing
a genuinely independent assessment. Same-session sign-offs are permitted for Tier 2 and Tier 3
ADRs but must be declared `Same session as ADR authorship — acknowledged` in the sign-off block,
and are subject to additional EL scrutiny on the governing document citations. A same-session
Tier 1 sign-off without this declaration is non-compliant (NM-042; CLAUDE.md §UX Designer
sign-off — structured attestation required).

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

## Pre-Wave Design Package Gate

*Authority: NM-072 process improvement (2026-06-27). Changes to this section require PM Agent authorship and EL endorsement.*

A pre-wave design package is a structured set of design artifacts produced before implementation waves begin, where one artifact serves as an **EL scope gate** — a document that the EL must approve before a downstream ADR may be authored and before any implementation sprint entry may be filed.

The M18 GD design package (Control Plane Column, #1354) is the canonical instance of this pattern.

### Phase sequencing invariant — upstream gate

When a design package includes an EL scope gate artifact, the following invariant applies:

**The EL scope gate artifact may not be submitted for EL review until all prerequisite design artifacts are filed and their content is stable.**

Submitting the scope gate artifact before its prerequisite artifacts exist forces the EL to make scope decisions without complete information. When the prerequisite artifacts subsequently arrive with divergent information, the scope decisions must be revised — producing stale downstream artifacts that must be corrected, course-correction near-misses, and an ADR author who receives inconsistent inputs. This is the root cause of NM-072: Artifact 5 (EL scope gate) was submitted and approved before Artifacts 2 and 4 were complete, causing GrowthShock to be absent from the panel deliberation and Artifact 4 to be drafted against an information hierarchy that had not yet been corrected.

**PM Agent obligation:** The sprint entry document for every design package must record, in its phase sequencing section:
- Which artifacts are prerequisites to the EL scope gate artifact
- An explicit statement that the scope gate artifact will not be submitted for EL review until those prerequisites are filed and on record

This is a scheduling commitment made at sprint entry, not a retrospective note. If the PM Agent cannot confirm at sprint entry which artifacts are prerequisites to the scope gate, the design package scope is not sufficiently defined to begin.

### Downstream gate

Once the EL approves the scope gate artifact, the downstream sequence is:
1. ADR authorship begins — the ADR author receives a complete, consistent scope specification
2. Implementation sprint entry may be filed only after the ADR is accepted

These gates are strictly sequential. The PM Agent does not file the implementation sprint entry before ADR acceptance, even if EL scope gate approval has been received.

### Near-miss obligation

If the scope gate artifact is submitted to the EL before all prerequisite design artifacts are on record — for any reason, including time pressure or parallel-phase authorship — the PI Agent files a near-miss in the same session, not after the design package closes. The near-miss must identify:
1. Which prerequisite artifacts were absent when the scope gate was submitted
2. Which scope decisions were made without complete information
3. Which downstream artifacts were produced against the incomplete scope
4. What course correction was required before ADR authorship began

A design package that exits without a near-miss for a sequencing inversion is not clean — it has an unrecorded process deviation.

---

## Wave Kickoff Coordination Check

*Authority: NM-071 process improvement (2026-06-26). Changes to this section require PM Agent authorship and EL endorsement.*

The wave kickoff coordination check is a PM Agent obligation executed before any sprint group in a new wave opens an implementation PR. It is distinct from the sprint entry gate (which is per-group) — this check is per-wave and asks whether the groups running concurrently are at a coordination tier where the PM Agent can reliably manage shared-file conflicts, cross-group dependencies, and PI Agent gate obligations alongside normal HORIZON sweep duties.

The check produces a coordination tier assignment recorded in every sprint entry document for the wave.

### Wave kickoff coordination fields

PM Agent records these fields in each sprint group's entry document (Section 1 — Sprint Identification):

1. **Groups in this wave** — list all sprint groups opening in the same wave, their primary implementation domains, and their shared-file write scope (`SESSION_STATE.md`, registry files, `CLAUDE.md`, DS-owned files). Use the file-conflict risk assessment (sprint entry §6.2) for each group to construct this list.

2. **Cross-group dependency graph** — for each group, list any upstream group whose merged output is required before this group can begin implementation. Any group with an upstream dependency must have the dependency merge sequence documented before implementation begins — the downstream group may not open its integration PR until the upstream group's integration PR has merged to the release branch.

3. **Coordination tier** — PM Agent determines the tier based on the count of groups actively running concurrently (not groups in the wave plan, but groups with open implementation PRs):

| Concurrent groups | Tier | Required coordination protocol |
|---|---|---|
| 1–2 | **Standard** | Groups write to shared files in their own PRs; conflicts are recoverable at merge time. No additional coordination required beyond normal sprint entry. |
| 3–4 | **Recommended coordination** | PM Agent coordination lane is recommended for shared-state files (`SESSION_STATE.md`, registry files). Groups flag shared-file changes in their exit PR description. PM Agent reviews exit PRs before PI Agent gate comment. |
| 5 | **Required coordination** | PM Agent coordination lane is mandatory for all shared-state files. Sprint group sub-branches mandatory (per `docs/process/sprint-group-isolation.md`). No group may open an integration PR without PM Agent clearance. |

**Hard ceiling: 5 concurrent groups per wave maximum.**

If 5 groups are already actively running (implementation PRs open), no new group may open an implementation PR until at least one exits (integration PR merges to release branch). Exceeding this ceiling without explicit EL direction is a process deviation. The PM Agent is responsible for enforcing this ceiling — EL is accountable and may revise the ceiling after M18 experience.

### Wave kickoff sequence

1. PM Agent reviews all groups planned for the wave before any group opens an implementation PR.
2. PM Agent determines the coordination tier for the wave.
3. PM Agent records the tier and the dependency merge sequence in each group's sprint entry document (Section 1).
4. EL approves the sprint entry documents (which now include the coordination tier).
5. Implementation PRs may open once sprint entry documents are EL-approved.

### When a new group joins mid-wave

If a group not originally in the wave plan is added mid-wave:
1. PM Agent re-runs the wave coordination check counting all currently open implementation PRs.
2. If the new group's addition would push the concurrent count above 5, the group holds at sprint entry until a running group exits.
3. The new group's entry document records the coordination tier at the time of its entry — not the tier from original wave planning.

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
   `docs/process/intents/M{N}-{G-suffix-or-ADR-NNN}-{YYYY-MM-DD}-{short-name}.md` before the implementation PR
   opens. The intent document completeness gate: the QA Lead can write a test from it without
   reading implementation code. (Authority: docs/process/agent-execution-lifecycle.md Step 1)

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

### UX/UI Design Artifact Gate

*Authority: M17-G6 sprint entry (2026-06-26). This gate applies to all sprint groups containing
deliverables classified as UX/UI-impacting. Changes to this section require PI Agent review and
EL endorsement.*

#### Classification trigger

A deliverable is **UX/UI-impacting** if it introduces or modifies: any visible component, any
layout region, any instrument boundary, any interaction pattern, or any data presentation in
the primary viewport. Documentation-only changes, backend-only changes, and test-only changes
are not UX/UI-impacting. The PM Agent records the classification in the sprint entry document.
The UX Designer may override a non-impacting classification before the sprint entry is
EL-approved.

#### Minimum artifact — UX mockups

Every UX/UI-impacting deliverable requires a **UX mockup** before the implementation PR opens.
The UX mockup is a minimum viable artifact: a rough sketch, ASCII layout diagram, annotated
screenshot, or wireframe sufficient for the panel to evaluate placement and information
hierarchy. The mockup is filed with or referenced from the intent document.

#### Conditional artifact — UI mockups

When a deliverable introduces a **new component, new layout zone, or new interaction pattern**
(not a modification of an existing element), a **UI mockup** is required in addition to the UX
mockup. A UI mockup specifies exact visual treatment: dimensions, color palette reference,
typography scale, and interaction states. The UI mockup is authored by the UX Designer and the
Frontend Architect jointly, and filed before the panel review.

#### Panel composition

UX/UI panel reviews require exactly five agents:

| Agent | Role in review |
|---|---|
| UX Designer | Lead reviewer — placement, information hierarchy, UX Architectural Commitment compliance |
| Design Thinking Agent | Evaluates against `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md` |
| Customer Agent | Confirms the deliverable does not introduce kryptonite for Personas 2, 3, or 5 |
| Frontend Architect | Confirms technical feasibility and component boundary compliance |
| Business PO | Confirms the north star test can be answered for the deliverable |

#### Panel review format

Each panel agent posts a review as a GitHub comment on the feature issue (not the PR), tagging
`@PM Agent`. The comment must include: (1) agent name and role, (2) governing document sections
reviewed, (3) any concerns or REJECT condition, and (4) a final verdict: ACCEPT or REJECT. The
PM Agent records the panel verdict in the sprint exit document.

#### Binding specification rule

The intent document for a UX/UI-impacting deliverable must reference the panel-approved mockup
by filename or GitHub comment link before the implementation PR opens. An implementation PR that
opens against an intent document with no panel-approved mockup reference is a process deviation.
The implementing agent verifies this reference exists before opening the PR.

#### Panel review fail condition

If any panel agent issues a REJECT verdict:

- The REJECT blocks Business PO acceptance — the Business PO may not issue an ACCEPT while any
  unresolved REJECT from a panel agent is outstanding.
- The PI Agent blocks the architecture phase of any downstream deliverable that depends on
  this deliverable.
- The implementing agent must address the REJECT condition and request re-review from the
  rejecting agent before the implementation PR opens.
- A near-miss entry is filed in `docs/process/near-miss-registry.md` if implementation began
  before the panel review was complete.

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
