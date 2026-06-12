---
name: process-redesign-phaseB-sprint-entry
type: sprint-entry
phase: Phase B — Business PO Acceptance Protocol
status: COMPLETE — Phase B outputs endorsed 2026-06-12 (PR #902)
authored-by: PM Agent (derived from deliberation document, 2026-06-08, and Phase A outputs)
authored-date: 2026-06-12
el-endorsement-required: true
prerequisite: Phase A exit artifact endorsed — docs/process/sprint-plans/process-redesign-phaseA-exit.md
deliberation-source: docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md §Phase B
phaseA-inputs:
  - CLAUDE.md §Agent Execution Lifecycle (Step 5 — Validate)
  - CLAUDE.md §Agent Execution Lifecycle — When Verify or Validate fails
  - CLAUDE.md §Agent Execution Lifecycle — Layer 3 Quality Gate
  - docs/process/intent-template.md
gates-phases:
  - Phase C — Sprint Cadence Formalization
  - Phase D — Session Boundary Discipline
---

# Phase B Sprint Entry — Business PO Acceptance Protocol

**Status:** COMPLETE — EL endorsement recorded 2026-06-12 (PR #902)
**Date authored:** 2026-06-12
**Opened:** Phase A EL endorsement confirmed 2026-06-12
**Deliberation source:** `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md §Phase B`

---

## Why Phase B Exists

Phase A defined the execution lifecycle — including the Validate step (Step 5) and the sprint
exit gate (Business PO acceptance). Phase B authors the acceptance protocol that gives the
Business PO concrete verification criteria for each work type.

Without Phase B, the Business PO Validate step is defined but under-specified:
- What does the Business PO actually do in a frontend feature Validate step? Open the app and
  look at it? Click through a specific user journey? Observe a specific metric?
- What does "confirmed the analytical intent is satisfied" mean for a backend capability — what
  API calls, what fixture scenarios, what specific field values?
- What is the exception path when the Business PO rejects? The rejection artifact is specified in
  Phase A, but the protocol for triggering and resolving it needs further specification.

Phase B produces the specificity that makes the Validate step repeatable rather than improvised.

---

## Entry Invariants

This sprint does not open until:

1. **Phase A EL endorsement is complete.** The execution lifecycle (Phase A output) is the
   prerequisite — the acceptance protocol references the Validate step's inputs and the rejection
   artifact format. Phase B cannot author a meaningful acceptance protocol without an accepted
   lifecycle to reference.

2. **All Phase A primary outputs are confirmed accessible:**
   - `CLAUDE.md §Agent Execution Lifecycle` (Validate step, rejection artifact, Layer 3 gate)
   - `docs/process/intent-template.md`

3. **Mandatory reading before session opens:**
   - `docs/process/sprint-plans/process-redesign-phaseA-exit.md` — Phase A summary
   - `CLAUDE.md §Agent Execution Lifecycle` — the Phase B acceptance protocol references this
   - `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md §Phase B`
   - `SESSION_STATE.md`, `CLAUDE.md`, `docs/process/agents.md` — standard session protocol

---

## What Phase B Delivers

### Primary Output — Business PO Acceptance Protocol

A formal specification of what Business PO acceptance looks like for each work type, what
constitutes a passing validation, and what the exception path is when acceptance is rejected.

**The four work types from CLAUDE.md §Agent Execution Lifecycle — Step 5, requiring per-type
verification specification:**

1. **Frontend feature:** How does the Business PO confirm the named persona reaches the
   observable state within the time ceiling? What specific user journey steps? What fixture
   scenario? What viewport? What constitutes evidence (screenshot, Playwright recording,
   specific UI element observed)?

2. **Backend capability:** What API calls, fixture scenarios, and field values constitute
   evidence of analytical intent satisfied? Who executes the API calls — the Business PO or
   the implementing agent in the Business PO's presence?

3. **Documentation:** How does the Business PO confirm navigability in under five minutes?
   Starting from which entry point? What constitutes "found the key finding"?

4. **Analytics:** How does the Business PO confirm the output changes what the persona can
   argue? What is the standard for "naming the specific argument"?

### Secondary Output — Exception Path Specification

Per PI Agent Finding 3 in the Phase A deliberation: a rejected sprint must produce a written
rejection artifact naming the defect, the remediation scope, and the re-acceptance date before
any work in the next sprint group begins. Phase B specifies the protocol for:
- When the Business PO triggers a rejection (what threshold, what evidence)
- What the rejection artifact must contain (beyond the Phase A format — work-type specific content)
- What the re-acceptance process looks like (who verifies, what confirms resolution)

---

## Participating Agents

| Agent | Phase B role |
|---|---|
| **Business PO** | Authors acceptance verification criteria per work type; defines what "validated" means as a repeatable protocol, not a judgment call |
| **PI Agent** | Co-authors the exception path; confirms enforcement language has teeth; produces the Phase B exit artifact enforcement review |
| **PM Agent** | Orchestrates the work sequence; produces the Phase B exit artifact |
| **QA Lead** | Consulted on test-type-specific verification (what makes a backend acceptance test repeatable and honest) |

---

## Work Sequence Within Phase B

```
Step 1 — Business PO: per-work-type verification specification
    Produces: Acceptance verification criteria for frontend, backend, documentation, analytics work types
    Canonical location: docs/process/acceptance-protocol.md
    Prerequisite for: Step 2

Step 2 — PI Agent: exception path specification + enforcement review
    Produces: Exception path specification (rejection trigger, artifact requirements, re-acceptance)
              Enforcement review (does the protocol have teeth, or is it aspirational?)
    Canonical location: Appended to docs/process/acceptance-protocol.md
    Prerequisite for: Step 3

Step 3 — PM Agent: Phase B exit artifact + Phase C sprint entry filed
    Produces: Phase B exit artifact (docs/process/sprint-plans/process-redesign-phaseB-exit.md)
              Phase C sprint entry (docs/process/sprint-plans/process-redesign-phaseC-sprint-entry.md)
    Prerequisite for: Phase C opens

Step 4 — EL endorsement
    Produces: Signed endorsement in Phase B exit artifact
    Prerequisite for: Phase C sprint entry may be opened
```

---

## Output Artifact Canonical Locations

| Artifact | Canonical location | Authored by |
|---|---|---|
| Business PO acceptance protocol | `docs/process/acceptance-protocol.md` | Business PO (Steps 1–2) |
| Exception path specification | Appended to `docs/process/acceptance-protocol.md` | PI Agent (Step 2) |
| Phase B exit artifact | `docs/process/sprint-plans/process-redesign-phaseB-exit.md` | PM Agent |
| Phase C sprint entry | `docs/process/sprint-plans/process-redesign-phaseC-sprint-entry.md` | PM Agent |

---

## Exit Gate

Phase B closes when:
1. `docs/process/acceptance-protocol.md` is filed with per-work-type verification criteria
2. PI Agent confirms enforcement language is adequate (obligation, not aspiration)
3. EL endorses Phase B outputs
4. Phase C sprint entry document is filed
5. SESSION_STATE.md updated
6. Any deferred items explicitly listed with rationale

---

*This document is filed as Phase A exit gate condition 4. Phase B opens when the EL endorses Phase A.*
