---
name: process-redesign-phaseA-sprint-entry
type: sprint-entry
phase: Phase A — Agent Execution Lifecycle
status: Filed — awaiting Phase 0 EL endorsement before opening
authored-by: Derived from deliberation document (EL + PI Agent + Business PO + PM Agent, 2026-06-08) and Phase 0 outputs (2026-06-09)
authored-date: 2026-06-09
el-endorsement-required: true
prerequisite: Phase 0 exit artifact endorsed — docs/process/sprint-plans/process-redesign-phase0-exit.md
deliberation-source: docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md
phase0-inputs:
  - docs/adr/template.md
  - docs/ux/personas.md §Persona Conflict Resolution
  - CLAUDE.md §North Star Test (Process Gate)
gates-phases:
  - Phase B — Business PO Acceptance Protocol
  - Phase C — Sprint Cadence Formalization
  - Phase D — Session Boundary Discipline
---

# Phase A Sprint Entry — Agent Execution Lifecycle

**Status:** Filed — awaiting Phase 0 EL endorsement  
**Date authored:** 2026-06-09  
**Opens when:** EL endorses Phase 0 exit artifact (`docs/process/sprint-plans/process-redesign-phase0-exit.md §Part VI`)  
**Deliberation source:** `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md`

---

## Why Phase A Exists

Phase 0 encoded the top four levels of the full authorship chain: Founding Document → DIC → User Personas and Journeys → Problem Framing → ADR authorship. Phase A encodes the bottom five: ADR → Intent authorship → Test authorship → Implementation → Verify → Validate.

The DEMO4 failure class had two root causes, not one:
1. ADR-012 did not carry user need, UX implication, or mission traceability → Phase 0 closed this
2. Even if ADR-012 had carried complete traceability, the execution lifecycle had no gate between "ADR accepted" and "PR merged" that required the implementation to produce the observable output the ADR specified → Phase A closes this

Phase A is the mechanism that makes the Phase 0 ADR template requirements operative at implementation time. Without Phase A, an ADR could carry a complete persona trace and UX implication statement, and an implementation could ignore both at merge time, and CI would still pass.

---

## Full Authorship Chain (Phases 0 + A Together)

```
Founding Document + North Star
(why we exist; the quinoa farmer; the finance minister across the table)
    └─► DIC (guardrails + art of the possible)          [Phase 0 — encoded]
         └─► User Personas + User Journeys + North Star UX
              └─► Problem framing                       [Phase 0 — encoded]
                   └─► ADR authorship                  [Phase 0 — encoded via template]
                        (Architect + UX Designer + BPO + DIC agents)
                            └─► Intent authorship       [Phase A — this sprint]
                                     └─► Test authorship
                                              └─► Implementation
                                                       └─► Verify (does output match intent?)
                                                                └─► Validate (does it serve the mission?)
```

The "Plan" step in the execution lifecycle now reads from ADRs that carry Phase 0 traceability requirements. Phase A encodes what the implementing agent does with that ADR.

---

## What Phase A Delivers

### Primary Output — Execution Lifecycle Process Definition

A formal definition of the agent execution lifecycle for feature implementation work. The lifecycle runs from "ADR accepted" to "sprint exit validated." Each step in the lifecycle has:
- A named starting condition
- A named output artifact (what the agent produces at this step)
- A named acceptance criterion for that artifact
- A named agent with R for producing it
- A named gate before the next step can begin

**The five steps Phase A must define:**

1. **Intent authorship** — Deriving the implementation intent from the ADR's traceability requirements. An Intent document names: the ADR this implements; which persona trace and UX implication statement elements it targets; the specific observable application state that constitutes "done"; and the test that will verify that state.

2. **Test authorship** — Writing tests before implementation begins. Tests are derived from the Intent document's observable application state, not from the implementation's interface. "CI passes" is not a test — "Persona 2 can reach the top MDA alert in under 30 seconds from drawer open, confirmed by application-state observation in a Playwright test against a fixture scenario" is a test.

3. **Implementation** — The coding work. An implementation that cannot be verified against the Intent document's acceptance criteria is not complete, regardless of CI status.

4. **Verify** — The implementing agent confirms the observable application state defined in the Intent document is present after implementation. This is a live-application observation, not a CI check. The verify step produces a named verification artifact (e.g., a Playwright test result, a recorded screen observation, or a referenced CI test that observes the live state).

5. **Validate** — The Business PO and/or PI Agent confirms that the implementation serves the mission as stated in the ADR's north star test (Element P-7) and the Intent document. Validation is a user-need confirmation, not a technical review.

### Secondary Output — Rejection Artifact With Teeth

A formal specification of what happens when an implementation reaches the Verify step and fails — when the observable application state defined in the Intent document is not present. This is the "rejection artifact with teeth" requirement introduced by the PI Agent in the deliberation (§Step 3).

The rejection artifact must:
- Block sprint exit (not just flag a concern)
- Require the implementing agent to return to the Intent authorship step (not just the implementation step), so the intent is re-examined, not just the code
- Produce a named record of the failure in the near-miss registry (a Verify failure is evidence that the intent-to-implementation chain had a gap)

---

## Entry Invariants

This sprint does not open until all of the following are satisfied:

1. **Phase 0 EL endorsement is complete.** The endorsement must be recorded in `docs/process/sprint-plans/process-redesign-phase0-exit.md §Part VI`. Phase A cannot open on a verbal endorsement.

2. **All Phase 0 primary outputs are confirmed accessible.** The ADR template (`docs/adr/template.md`), the conflict resolution ruling (`docs/ux/personas.md §Section 7`), and the north star test process gate (`CLAUDE.md §North Star Test (Process Gate)`) are all in `release/m12`. Phase A authors cannot design the execution lifecycle without being able to read the upstream requirements it will implement.

3. **Mandatory reading before session opens:**
   - `docs/process/sprint-plans/process-redesign-phase0-exit.md` — Phase 0 summary
   - `docs/adr/template.md` — the Phase A lifecycle executes against ADRs that carry this template's requirements
   - `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md §Phase A` — the deliberation's Phase A reasoning
   - `SESSION_STATE.md`, `CLAUDE.md`, `docs/process/agents.md` — standard session protocol

---

## Participating Agents

| Agent | Phase A role |
|---|---|
| **Architect Agent** | Defines the Intent document format; defines what "observable application state" means as an architectural requirement; ensures the lifecycle is implementable without adding excessive overhead to normal feature work |
| **PI Agent** | Defines the rejection artifact specification; defines the enforcement language for each lifecycle gate; ensures the lifecycle's "does output match intent?" step has teeth |
| **Business PO** | Defines the Validate step; confirms how the north star test flows from ADR Element P-7 into the sprint validation step |
| **PM Agent** | Orchestrates the work sequence within Phase A; produces the Phase A exit artifact |

---

## Work Sequence Within Phase A

```
Step 1 — Architect Agent: define Intent document format + observable application state requirement
    Produces: Intent document template
              Observable application state acceptance criterion format
    Prerequisite for: Steps 2 and 3

Step 2 — PI Agent: define rejection artifact specification + enforcement language
    Produces: Rejection artifact format (what an agent produces when Verify fails)
              Enforcement language for each lifecycle gate
    Prerequisite for: Step 3

Step 3 — Business PO: define Validate step + north star test integration
    Produces: Validate step specification (who runs it, what constitutes passing)
              Integration of ADR Element P-7 into sprint validation
    Prerequisite for: Step 4

Step 4 — Architect Agent: integrate into coherent lifecycle document
    Produces: Agent execution lifecycle definition (complete five-step specification)
              Canonical placement in CLAUDE.md or process docs
    Prerequisite for: Step 5

Step 5 — PI Agent: enforcement review + EL endorsement preparation
    Produces: Enforcement review finding
              Phase A exit artifact
    Prerequisite for: Step 6

Step 6 — EL endorsement
    Produces: Signed endorsement in Phase A exit artifact
    Prerequisite for: Phase B sprint entry document may be opened
```

---

## Output Artifact Canonical Locations

| Artifact | Canonical location | Authored by |
|---|---|---|
| Intent document template | `docs/process/intent-template.md` | Architect Agent |
| Rejection artifact specification | New subsection in CLAUDE.md §Architectural Principles or `docs/process/` | PI Agent |
| Validate step specification | New subsection in CLAUDE.md §Architectural Principles | Business PO |
| Agent execution lifecycle (complete) | New subsection in CLAUDE.md §Architectural Principles | Architect Agent |
| Phase A exit artifact | `docs/process/sprint-plans/process-redesign-phaseA-exit.md` | PM Agent orchestrates; PI Agent confirms |

---

## Exit Gate

Phase A closes when:
1. The agent execution lifecycle (five steps, enforcement gates, rejection artifact) is encoded in CLAUDE.md or a canonical process document
2. PI Agent confirms enforcement language is adequate (obligation, not aspiration)
3. EL endorses Phase A outputs
4. Phase B sprint entry document is filed
5. SESSION_STATE.md updated
6. Any deferred items explicitly listed with rationale

---

*This document is filed as Phase 0 exit gate condition 4. Phase A opens when the EL endorses Phase 0.*
