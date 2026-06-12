---
name: process-redesign-phaseD-sprint-entry
type: sprint-entry
phase: Phase D — Session Boundary Discipline
status: Filed — awaiting Phase C EL endorsement before opening
authored-by: PM Agent (derived from deliberation document, 2026-06-08, and Phase C outputs)
authored-date: 2026-06-12
el-endorsement-required: true
prerequisite: Phase C exit artifact endorsed — docs/process/sprint-plans/process-redesign-phaseC-exit.md
deliberation-source: docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md §Phase D
phaseC-inputs:
  - docs/process/sprint-plans/templates/sprint-entry-template.md (sprint entry artifact form)
  - docs/process/sprint-plans/templates/sprint-exit-template.md (sprint exit artifact form)
  - docs/process/sprint-planning-sop.md §Sprint Entry Gate (entry gate conditions)
  - docs/process/sprint-planning-sop.md §Sprint Exit Gate (exit gate conditions)
  - docs/process/agents.md §PM Agent — Sprint Boundary Obligations
  - docs/process/agents.md §Process Integrity Agent — Sprint Boundary Enforcement
gates-phases: []
---

# Phase D Sprint Entry — Session Boundary Discipline

**Status:** Filed — awaiting Phase C EL endorsement
**Date authored:** 2026-06-12
**Opens when:** EL endorses Phase C exit artifact (`docs/process/sprint-plans/process-redesign-phaseC-exit.md §Part VII`)
**Deliberation source:** `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md §Phase D`

---

## Why Phase D Exists

Phase A defined the execution lifecycle. Phase B defined the Business PO acceptance protocol.
Phase C encoded the sprint boundary templates and conditions. Phase D is the final phase:
it codifies the entry and exit invariants as architectural commitments in CLAUDE.md — the
project's permanent constitution.

Without Phase D, the sprint entry and exit gates live in the SOP and in agents.md, but
they are not in the constitution that every agent reads at session start. An agent reading
only CLAUDE.md at session initialization would see the PR merge gate ("must stop all git
operations after opening a PR") and the pre-push lint gate ("mandatory before any git push
touching Python files") as hard stops — but would not see the sprint entry gate ("may not
authorize implementation to begin without the entry template complete and EL-approved") with
the same architectural weight.

Phase D closes that gap: the session boundary invariants enter CLAUDE.md §Session Continuity
with the same enforcement language as the PR merge gate and the pre-push lint gate.

---

## Entry Invariants

This sprint does not open until:

1. **Phase C EL endorsement is complete.** The sprint templates, PM Agent obligations, and
   PI Agent obligations (Phase C outputs) are the referents that Phase D will cite in CLAUDE.md.
   Phase D cannot produce correct constitutional language without the Phase C artifacts being
   final and endorsed.

2. **All Phase C primary outputs are confirmed accessible:**
   - `docs/process/sprint-plans/templates/sprint-entry-template.md`
   - `docs/process/sprint-plans/templates/sprint-exit-template.md`
   - `docs/process/sprint-planning-sop.md §Sprint Entry Gate`
   - `docs/process/sprint-planning-sop.md §Sprint Exit Gate`
   - `docs/process/agents.md §PM Agent — Sprint Boundary Obligations`
   - `docs/process/agents.md §Process Integrity Agent — Sprint Boundary Enforcement`

3. **Mandatory reading before session opens:**
   - `docs/process/sprint-plans/process-redesign-phaseC-exit.md` — Phase C summary
   - `docs/process/sprint-planning-sop.md` — the SOP Phase D will reference
   - `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md §Phase D`
   - `SESSION_STATE.md`, `CLAUDE.md`, `docs/process/agents.md` — standard session protocol

---

## What Phase D Delivers

### Primary Output — CLAUDE.md §Session Continuity Amendment

An amendment to `CLAUDE.md §Session Continuity` adding a subsection
`§Entry and Exit Invariants`. The subsection must carry the same enforcement weight as
existing architectural gates — not as advisory guidance, but as hard stops.

**Content requirements for the amendment:**

1. **Sprint entry invariant (architectural statement):**
   - Named obligation: "The PM Agent may not authorize implementation to begin without the
     sprint entry template filed and EL-approved."
   - Enforcement mechanism: if a sprint begins implementation without a filed entry document,
     PI Agent files a near-miss in the same session — not after the sprint closes.
   - Reference: `docs/process/sprint-planning-sop.md §Sprint Entry Gate`
   - Template reference: `docs/process/sprint-plans/templates/sprint-entry-template.md`

2. **Sprint exit invariant (architectural statement):**
   - Named obligation: "A sprint does not close when issues are closed and CI is green. A
     sprint closes when Business PO acceptance is recorded for every user-facing deliverable
     and PI Agent confirms all exit conditions are satisfied."
   - Enforcement mechanism: PI Agent blocks exit confirmation until all exit conditions in the
     sprint exit template are satisfied.
   - Reference: `docs/process/sprint-planning-sop.md §Sprint Exit Gate`
   - Template reference: `docs/process/sprint-plans/templates/sprint-exit-template.md`

3. **"If it isn't written down, it doesn't exist" principle:**
   An intent document that exists in an agent's session context but has not been filed at
   `docs/process/intents/` does not satisfy the entry gate. A Business PO verdict delivered
   verbally but not as a filed artifact does not satisfy the exit gate. A sprint entry
   document that exists as a draft but has not been committed and referenced in SESSION_STATE.md
   does not satisfy the entry gate. The gates are satisfied by artifacts, not by knowledge.

The language must be architectural, not aspirational. The deliberation document (§Phase D)
specifies: "The entry and exit invariants must be stated as architecture, not process guidance.
The existing §Architectural Principles section enforces pre-push lint gates and PR merge gates
as hard stops — 'must stop all git operations.' The session boundary invariants should carry
the same enforcement language."

### Secondary Output — Phase D Exit Artifact and SESSION_STATE.md Update

Phase D has no Phase E. It is the terminal phase of the process redesign sequence. The Phase D
exit artifact documents what was produced and the EL endorsement that closes the redesign
sequence. SESSION_STATE.md is updated to mark the process redesign sequence complete.

---

## Participating Agents

| Agent | Phase D role |
|---|---|
| **PI Agent** | Authors CLAUDE.md §Session Continuity amendment; produces Phase D exit artifact enforcement review |
| **PM Agent** | Reviews for practical enforceability in single-principal governance context; produces Phase D exit artifact; confirms sequence is complete |
| **Engineering Lead** | Endorses Phase D outputs; closes the process redesign sequence |

---

## Work Sequence Within Phase D

```
Step 1 — PI Agent: CLAUDE.md §Session Continuity amendment
    Produces: New subsection §Entry and Exit Invariants in CLAUDE.md
    Authority: Deliberation document §Phase D — PI Agent authors this
    Prerequisite for: Step 2

Step 2 — PM Agent: enforceability review
    Produces: Assessment of whether the §Entry and Exit Invariants language creates
              genuine obligations in a single-principal governance context, or whether
              the constraints are circular (the EL who approves the entry is the same
              person who could bypass it). Names any gaps.
    Prerequisite for: Step 3

Step 3 — PM Agent: Phase D exit artifact + sequence closure notation
    Produces: Phase D exit artifact (docs/process/sprint-plans/process-redesign-phaseD-exit.md)
              SESSION_STATE.md update marking process redesign sequence complete
    Prerequisite for: EL endorsement

Step 4 — EL endorsement
    Produces: Signed endorsement in Phase D exit artifact
    Prerequisite for: Process redesign sequence formally closed
```

---

## Output Artifact Canonical Locations

| Artifact | Canonical location | Authored by |
|---|---|---|
| CLAUDE.md amendment | `CLAUDE.md §Session Continuity — §Entry and Exit Invariants` | PI Agent |
| PM Agent enforceability review | Embedded in Phase D exit artifact Part III | PM Agent |
| Phase D exit artifact | `docs/process/sprint-plans/process-redesign-phaseD-exit.md` | PM Agent |

---

## Exit Gate

Phase D closes when:
1. CLAUDE.md §Session Continuity amendment filed with architectural enforcement language
2. PM Agent enforceability review complete and on record
3. EL endorses Phase D outputs
4. SESSION_STATE.md updated to mark process redesign sequence (Phases 0, A, B, C, D) complete
5. Any deferred items explicitly listed with rationale

---

*Phase D is the terminal phase. The process redesign sequence closes when Phase D is endorsed.*
