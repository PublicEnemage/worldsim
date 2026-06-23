---
name: process-redesign-phaseC-sprint-entry
type: sprint-entry
phase: Phase C — Sprint Cadence Formalization
status: Filed — awaiting Phase B EL endorsement before opening
authored-by: PM Agent (derived from deliberation document, 2026-06-08, and Phase B outputs)
authored-date: 2026-06-12
el-endorsement-required: true
prerequisite: Phase B exit artifact endorsed — docs/process/sprint-plans/process-redesign-phaseB-exit.md
deliberation-source: docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md §Phase C
phaseB-inputs:
  - docs/process/acceptance-protocol.md (Business PO acceptance protocol — per-type criteria and exception path)
  - docs/process/sprint-planning-sop.md §Sprint Exit Gate (Business PO acceptance attestation requirement)
  - docs/process/agent-execution-lifecycle.md (five-step lifecycle — Steps 1 and 5 are the sprint boundary reference points)
gates-phases:
  - Phase D — Session Boundary Discipline
---

# Phase C Sprint Entry — Sprint Cadence Formalization

**Status:** Filed — awaiting Phase B EL endorsement
**Date authored:** 2026-06-12
**Opens when:** EL endorses Phase B exit artifact (`docs/process/sprint-plans/process-redesign-phaseB-exit.md §Part VII`)
**Deliberation source:** `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md §Phase C`

---

## Why Phase C Exists

Phase A defined the execution lifecycle — what each implementation step is and what gates each
transition. Phase B defined the Business PO acceptance protocol — what validation looks like
for each work type and what the exception path is. Phase C encodes the sprint boundary: when
those steps run relative to sprint entry and exit, and what must exist at each boundary.

Without Phase C, sprint entry and exit remain informally bounded:
- Sprint entry: implementation begins when issues exist and a sprint plan is drafted — but
  there is no document template that makes the entry conditions explicit and checkable
- Sprint exit: the sprint-planning-sop.md §Sprint Exit Gate now names the conditions, but
  the exit conditions are not yet in a template that an implementing agent can follow at
  every sprint without reading the SOP each time

Phase C produces the templates and PM Agent role language that make the sprint boundaries
consistent across sprints — not dependent on re-reading the SOP, but encoded in artifacts
that are filed at each sprint's start and close.

---

## Entry Invariants

This sprint does not open until:

1. **Phase B EL endorsement is complete.** The acceptance protocol (Phase B output) is the
   prerequisite — the sprint exit template references the Business PO acceptance attestation
   and the acceptance protocol defines what that attestation contains. Phase C cannot produce
   a meaningful exit template without an accepted acceptance protocol to reference.

2. **All Phase B primary outputs are confirmed accessible:**
   - `docs/process/acceptance-protocol.md`
   - `docs/process/sprint-planning-sop.md §Sprint Exit Gate`

3. **Mandatory reading before session opens:**
   - `docs/process/sprint-plans/process-redesign-phaseB-exit.md` — Phase B summary
   - `docs/process/acceptance-protocol.md` — the sprint exit template references this
   - `docs/process/sprint-planning-sop.md` — the SOP this phase amends
   - `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md §Phase C`
   - `SESSION_STATE.md`, `CLAUDE.md`, `docs/process/agents.md` — standard session protocol

---

## What Phase C Delivers

### Primary Output — Sprint Entry and Exit Document Templates

**Sprint entry template** (`docs/process/sprint-plans/templates/sprint-entry-template.md`):

A structured template that any PM Agent session fills out at sprint kickoff to confirm the
sprint is properly bounded before implementation begins. Required sections:

1. Sprint identification (milestone, sprint group, issue list, release branch)
2. Entry invariants checklist:
   - [ ] ADR accepted for each group requiring an ADR (per sprint-planning-sop.md §Grouping Criteria #5)
   - [ ] Intent document filed for each user-facing deliverable (per docs/process/agent-execution-lifecycle.md Step 1)
   - [ ] QA tests authored for each user-facing deliverable (per docs/process/agent-execution-lifecycle.md Step 2)
   - [ ] CI trigger verified on release branch (per sprint-planning-sop.md §Relationship to Release Branch)
3. Scope declaration: the issues in this sprint; any issues explicitly out of scope with rationale
4. ADR prerequisite table: which groups are BLOCKED_ADR and what ADR must be accepted first
5. Near-miss sweep: any process gaps identified since the previous sprint close

**Sprint exit template** (`docs/process/sprint-plans/templates/sprint-exit-template.md`):

A structured template that PM Agent fills out at sprint close to confirm all exit conditions
are satisfied. Required sections:

1. Sprint identification and date
2. Implementation status: all groups merged; CI green on release branch
3. Business PO acceptance table: one row per user-facing deliverable, with verdict (ACCEPT/REJECT),
   verdict artifact location, and Customer Agent Layer 3 assessment reference
4. Open rejections: any REJECT verdicts and their resolution status (re-accepted, EL exception,
   or blocking)
5. PI Agent sprint exit confirmation: PI Agent confirms all conditions are satisfied

The sprint exit template is filed at `docs/process/sprint-plans/{milestone-slug}-sprint-{N}-exit.md`
alongside the sprint plan.

### Secondary Output — PM Agent Role Amendment

An amendment to `docs/process/agents.md §PM Agent` adding:

- The PM Agent's obligation at sprint entry: fill out the sprint entry template before any
  implementation PR is opened. A sprint that opens without a sprint entry template is a process
  deviation — the PM Agent may not authorize implementation to begin without the entry template
  complete and EL-approved.
- The PM Agent's obligation at sprint exit: fill out the sprint exit template, confirm Business
  PO acceptance is on record for all user-facing deliverables, and route to PI Agent for sprint
  exit confirmation.

### Tertiary Output — PI Agent Role Amendment

An amendment to `docs/process/agents.md §Process Integrity Agent` adding:

- The PI Agent's obligation when a sprint opens without a complete entry document: file a
  near-miss entry immediately. A sprint that begins implementation without a sprint entry
  template is a process gap — the near-miss is filed whether or not implementation ultimately
  succeeds.
- The PI Agent's role in the sprint exit gate: confirm all exit conditions in the sprint exit
  template are satisfied before the sprint exit checklist issue is closed.

### Quaternary Output — Sprint Planning SOP Amendment (sprint entry section)

An amendment to `docs/process/sprint-planning-sop.md` adding a §Sprint Entry Gate section
that mirrors the §Sprint Exit Gate added in Phase B. The sprint entry gate specifies what must
be true before implementation begins — the intent document, the QA test file, the ADR — so
that the sprint has both a defined entry and a defined exit.

---

## Participating Agents

| Agent | Phase C role |
|---|---|
| **PM Agent** | Authors sprint entry and exit templates; authors PM Agent role amendment; orchestrates; produces Phase C exit artifact |
| **PI Agent** | Authors PI Agent role amendment; confirms enforcement language has teeth; produces Phase C exit artifact enforcement review |
| **QA Lead** | Consulted on sprint entry template — specifically, the test authorship entry invariant (does the entry template format make it easy to confirm tests exist before implementation?) |

---

## Work Sequence Within Phase C

```
Step 1 — PM Agent: sprint entry and exit document templates
    Produces: docs/process/sprint-plans/templates/sprint-entry-template.md
              docs/process/sprint-plans/templates/sprint-exit-template.md
    Prerequisite for: Step 2

Step 2 — PM Agent + PI Agent: role amendments
    Produces: Amendment to docs/process/agents.md §PM Agent (sprint boundary obligations)
              Amendment to docs/process/agents.md §Process Integrity Agent (sprint entry near-miss obligation)
              Amendment to docs/process/sprint-planning-sop.md §Sprint Entry Gate
    Prerequisite for: Step 3

Step 3 — PM Agent: Phase C exit artifact + Phase D sprint entry filed
    Produces: Phase C exit artifact (docs/process/sprint-plans/process-redesign-phaseC-exit.md)
              Phase D sprint entry (docs/process/sprint-plans/process-redesign-phaseD-sprint-entry.md)
    Prerequisite for: Phase D opens

Step 4 — EL endorsement
    Produces: Signed endorsement in Phase C exit artifact
    Prerequisite for: Phase D sprint entry may be opened
```

---

## Output Artifact Canonical Locations

| Artifact | Canonical location | Authored by |
|---|---|---|
| Sprint entry template | `docs/process/sprint-plans/templates/sprint-entry-template.md` | PM Agent |
| Sprint exit template | `docs/process/sprint-plans/templates/sprint-exit-template.md` | PM Agent |
| PM Agent role amendment | Appended to `docs/process/agents.md §PM Agent` | PM Agent |
| PI Agent role amendment | Appended to `docs/process/agents.md §Process Integrity Agent` | PI Agent |
| Sprint Entry Gate SOP amendment | `docs/process/sprint-planning-sop.md §Sprint Entry Gate` | PM Agent |
| Phase C exit artifact | `docs/process/sprint-plans/process-redesign-phaseC-exit.md` | PM Agent |
| Phase D sprint entry | `docs/process/sprint-plans/process-redesign-phaseD-sprint-entry.md` | PM Agent |

---

## Exit Gate

Phase C closes when:
1. Sprint entry and exit templates are filed at canonical locations
2. PM Agent and PI Agent role amendments are filed in agents.md
3. Sprint Entry Gate section added to sprint-planning-sop.md
4. PI Agent confirms enforcement language is adequate (obligation, not aspiration)
5. EL endorses Phase C outputs
6. Phase D sprint entry document is filed
7. SESSION_STATE.md updated
8. Any deferred items explicitly listed with rationale

---

*This document is filed as Phase B exit gate condition 4. Phase C opens when the EL endorses Phase B.*
