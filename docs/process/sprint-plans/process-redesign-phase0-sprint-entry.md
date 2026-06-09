---
name: process-redesign-phase0-sprint-entry
type: sprint-entry
phase: Phase 0 — UX/Persona Traceability Upstream of ADR Development
status: Pending EL endorsement — entry gate not yet open
authored-by: Derived from deliberation document (EL + PI Agent + Business PO + PM Agent, 2026-06-08)
authored-date: 2026-06-08
el-endorsement-required: true
deliberation-source: docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md
gates-phases:
  - Phase A — Agent Execution Lifecycle
  - Phase B — Business PO Acceptance Protocol
  - Phase C — Sprint Cadence Formalization
  - Phase D — Session Boundary Discipline
---

# Phase 0 Sprint Entry — UX/Persona Traceability Upstream of ADR Development

**Status:** Pending EL endorsement  
**Date authored:** 2026-06-08  
**Deliberation source:** `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md`  
**PI Agent note:** This sprint entry document is itself an instance of the artifact that Phase C will formalize into a template. It cannot be opened until EL endorses the sequencing plan. Filing it now satisfies the entry invariant: the written document exists before the session opens.

---

## Why Phase 0 Exists

The process redesign deliberation (2026-06-08) identified that the execution lifecycle (Phases A–D) describes how implementation agents verify and validate their work — but the chain those agents are executing against starts upstream, before any ADR is authored. If the ADR does not carry a documented user need and UX implication, the Verify and Validate steps at the bottom of the chain have a weaker specification to check against.

Phase 0 closes three gaps identified in the deliberation's gap analysis as **highest priority** (the structural root of the Demo 4 failure class):

| Gap | Document | Failure mode if left open |
|---|---|---|
| XD-2 | Both | Mission-to-implementation traceability never required — every Demo 4 recurs |
| XD-1 | Both | Minister vs. specialist conflict unresolved — whichever persona is convenient wins |
| FD-1 | Founding | North star test never formally run — mission-subversive work accepted as done |

Phase 0 is upstream of Phases A–D. Its outputs are prerequisites for Phase A authorship: the execution lifecycle's "Plan" step cannot be written precisely until "reference the approved ADR" means "reference an ADR that already carries a documented user need and UX implication."

---

## Full Authorship Chain (Post-Phase 0)

The complete chain, once Phase 0 is complete and encoded:

```
Founding Document + North Star
(why we exist; the quinoa farmer; the finance minister across the table)
    └─► DIC (guardrails + art of the possible)
         (domain experts translating the mission into analytical requirements)
            └─► User Personas + User Journeys + North Star UX
                 (named humans the mission serves; how they actually move through the tool)
                    └─► Problem framing
                         (named persona, journey step, domain-validated need)
                            └─► ADR authorship
                                 (Architect + UX Designer + BPO + relevant DIC agents)
                                    └─► Intent authorship
                                            └─► Test authorship
                                                    └─► Implementation
                                                            └─► Verify (does output match intent?)
                                                                    └─► Validate (does it serve the mission?)
```

Phase 0 encodes the top four levels of this chain as formal process requirements. Phases A–D encode the bottom five.

---

## Entry Invariants

This sprint does not open until all of the following are satisfied and written:

1. **EL endorsement of the sequencing plan.** The deliberation document (`docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md`) records the deliberation; EL endorsement of the sequencing plan described therein is the gate that opens Phase 0. Endorsement must be documented — a comment on the process redesign tracking issue, or a signed note in SESSION_STATE.md.

2. **This sprint entry document is complete.** Already satisfied by this file's existence.

3. **Mandatory reading before session opens.** Every agent participating in Phase 0 reads the following in full before producing any output:
   - `docs/vision/worldsim-founding-document.md` — the north star at the apex of the chain
   - `docs/ux/north-star.md` — the UX instrument-cluster design authority
   - `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md` — the full gap analysis and sequencing rationale
   - `docs/ux/personas.md` — all five personas; the minister/specialist tension is explicit here
   - `SESSION_STATE.md`, `CLAUDE.md`, `docs/process/agents.md` — standard session protocol

4. **No prior Phase 0 session outputs are assumed.** This sprint begins in a fresh session. The entry documents above are the only carry-forward context. If a prior Phase 0 session produced partial outputs, those outputs must be filed in their canonical locations before this session opens — otherwise they do not exist.

---

## What Phase 0 Delivers

Three primary outputs (closing gaps XD-2, XD-1, FD-1):

### Output 1 — ADR Traceability Requirements (closes XD-2)

A formal specification of what every ADR must carry before it can be accepted. Closes gap XD-2: "neither document is a formal process gate in the ADR or sprint process."

**Minimum specification per ADR type:**
- ADRs that introduce a new user-facing capability or change how users encounter existing capabilities: requires UX Designer on the authorship panel; must carry a documented UX implication statement before acceptance.
- ADRs that introduce any new analytical capability: must name the persona(s) served and the user journey step addressed. ADRs that cannot name a persona (pure infrastructure) must document that explicitly and carry a forward obligation to trace the enabled capability to a named persona need.
- ADRs for pure infrastructure with only indirect UX connection (≥2 levels of indirection): may waive UX Designer panel membership with Architect documentation of why the connection is sufficiently indirect; must still name the downstream capability that eventually reaches a user.

**Where it lands:** A new `§Persona and UX Traceability` section in the ADR template (canonical location: `docs/adr/template.md` or embedded as a required section in CLAUDE.md §Architectural Principles). The Architect Agent determines the canonical placement and encodes it.

### Output 2 — Persona Conflict Resolution Ruling (closes XD-1)

An authoritative resolution to the founding document / UX north star persona tension. The founding document's north star figure is "a finance minister of a small, vulnerable country" (Persona 5 — Institutional Decision-Maker). The UX north star's canonical user is "a debt restructuring specialist at a finance ministry" (Persona 2 — Finance Ministry Negotiator). When these personas have conflicting design needs, which governs?

**Ruling to be produced:** A stated priority hierarchy for persona conflict resolution in ADR and sprint review contexts. This hierarchy must be grounded in the founding document — not invented fresh.

**Where it lands:** A new subsection in `docs/ux/personas.md §Persona Conflict Resolution` (authored by Business PO). Cross-referenced in the ADR traceability requirements (Output 1) so conflict resolution applies at ADR authorship time, not only at sprint review time.

### Output 3 — North Star Test as a Formal Process Artifact (closes FD-1)

The north star test currently exists as a CLAUDE.md aspiration: "Does this decision make the tool more useful to that person in that moment?" It has no artifact form, no process home, and no agent who holds R for running it. This sprint makes it structural.

**Ruling to be produced:**
- A defined north star test artifact: a short written assessment (≤ one page) answering the north star question for a given decision, naming the finance minister scenario and the concrete capability being evaluated.
- A named process home: the north star test is a required step in the sprint exit artifact for any sprint whose primary deliverable is a user-facing capability.
- A named agent owner: PI Agent holds R for ensuring the north star test artifact exists before a sprint closes; Business PO holds R for authoring it (with input from the DIC agent most relevant to the capability being delivered).

**Where it lands:** A new subsection in CLAUDE.md §Architectural Principles — `§North Star Test (Process Gate)`. Authored by PI Agent, reviewed by Business PO.

### Secondary Outputs (if capacity allows)

The following gaps from the gap analysis are in scope for Phase 0 if primary outputs are complete. If not completed in this sprint, they are explicitly deferred with a documented rationale in the Phase 0 exit artifact:

| Gap | What needs to happen |
|---|---|
| FD-2 | Layer 3 (self-interpreting outputs) assigned a process owner. Candidate: Customer Agent. A CLAUDE.md line naming the owner is sufficient. |
| FD-3 | Kryptonite frame operationalized as a design constraint. A one-paragraph addition to CLAUDE.md §Guiding Principles stating what "on the side of the finance ministry" means when UX tradeoffs are being decided. |
| NS-1 | Persona 2 dominance acknowledged and partially addressed by the conflict resolution ruling (Output 2). Any residual gap documented explicitly. |
| NS-2 | UX north star Mode 3 section updated to reflect delivered capability (Mode 3 shipped in M12, PR #778). UX Designer updates. |

---

## Participating Agents

### Authoring agents (hold R for specific outputs)

| Agent | Output | Consultations required before drafting |
|---|---|---|
| **Council Orchestrator** | ROADMAP activation: domain guardrails + art of the possible | Reads founding document + UX north star in full. Activates four standing DIC agents (see below). |
| **UX Designer** | UX traceability requirements (part of Output 1) | Council Orchestrator ROADMAP output must be complete first — UX traceability requirements must be grounded in the DIC guardrails, not derived independently. |
| **Business PO** | Persona traceability requirements (part of Output 1) + persona conflict resolution ruling (Output 2) | Council Orchestrator ROADMAP output + UX Designer traceability requirements must be complete first. |
| **Architect Agent** | ADR tiering specification (part of Output 1) + canonical placement decision | UX Designer and Business PO outputs must be complete first. Architect determines how all three sub-outputs are encoded in the ADR template. |
| **PI Agent** | North star test as formal process artifact (Output 3) | All other outputs must be complete first. PI Agent also enforces entry invariants and reviews all outputs for enforcement language vs. aspirational guidance. |

### DIC agents (standing Phase 0 participants)

Four DIC agents have standing Phase 0 roles. They are activated via the Council Orchestrator ROADMAP mode and contribute guardrails that the UX Designer and Business PO must not override:

| Agent | Guardrail | Cannot be compromised by UX decisions |
|---|---|---|
| **Development Economist** | Human cost ledger carries equal visual weight to financial indicators — never demoted by UX hierarchy | Demoting HCL to secondary position is a mission violation, regardless of information hierarchy rationale |
| **Chief Methodologist** | Uncertainty must not be suppressed or rendered invisible | Design choices that prioritize clean outputs over honest ones violate "No False Precision" |
| **Intergenerational Advocate** | Irreversible thresholds must never be renderable as ignorable — MDA floors cannot be visually minimized | An MDA floor crossing must read with the same severity as any other TERMINAL alert |
| **Investment Agent** | Art of the possible: what well-resourced actors can see that WorldSim's users cannot | Capability gap framing — what the roadmap should prioritize to close the asymmetry |

Additional DIC agents (Political Economist, Geopolitical Analyst, Ecological Economist, Community Resilience, Social Dynamics) are consulted when Phase 0 outputs touch their specific domain. They do not have standing Phase 0 participation for every decision.

### Review chain

After all authoring outputs are complete:

1. **PI Agent** reviews all outputs for enforcement language. The test: does each requirement create an obligation, or is it aspirational? Requirements must read like CLAUDE.md's existing hard stops ("must stop all git operations," "must exit 0"), not like guidelines.

2. **EL endorses** Phase 0 outputs before Phase A opens. Endorsement is recorded in the Phase 0 exit artifact and in SESSION_STATE.md.

---

## Work Sequence Within Phase 0

The dependency structure within this sprint is linear. No parallel authorship:

```
Step 1 — Council Orchestrator: ROADMAP — [domain guardrails for UX and capability gap priorities]
    Produces: DIC guardrail list (five binding requirements per standing agent)
              Capability gap priority list (art of the possible from Investment Agent + Development Economist)
    Prerequisite for: Steps 2 and 3

Step 2 — UX Designer: derive UX traceability requirements grounded in Step 1 guardrails
    Produces: UX traceability specification (which ADR types require UX Designer on panel;
              what a UX implication statement must contain; what constitutes adequate review)
    Prerequisite for: Step 3

Step 3 — Business PO: derive persona traceability requirements + persona conflict resolution ruling
    Produces: Persona traceability specification (which ADRs must name a persona; what a
              valid persona trace looks like; what ADRs that cannot name a persona must document)
              Persona conflict resolution ruling (priority hierarchy, grounded in founding document)
    Prerequisite for: Step 4

Step 4 — Architect Agent: integrate Steps 1–3 into a coherent ADR tiering specification
    Produces: ADR tiering (three tiers: full UX panel, persona trace only, indirect-connection waiver)
              Canonical placement decision (which file, which section)
              Draft language for the ADR template section
    Prerequisite for: Step 5

Step 5 — PI Agent: author north star test as formal process artifact; review all prior outputs
    Produces: North star test artifact form and process home (CLAUDE.md §North Star Test)
              Review finding: is enforcement language adequate, or aspirational?
    Prerequisite for: Step 6

Step 6 — EL endorsement of all Phase 0 outputs
    Produces: Signed endorsement in Phase 0 exit artifact
    Prerequisite for: Phase A sprint entry document may be opened
```

---

## Output Artifact Canonical Locations

| Artifact | Canonical location | Authored by |
|---|---|---|
| DIC guardrails (Step 1 output) | `docs/process/design/process-redesign-phase0-dic-roadmap.md` | Council Orchestrator (session record) |
| UX traceability requirements | New section in `docs/adr/` ADR template file, or new subsection in CLAUDE.md §ADR Standards | UX Designer (draft); Architect encodes |
| Persona traceability requirements | Same ADR template section as above | Business PO (draft); Architect encodes |
| Persona conflict resolution ruling | `docs/ux/personas.md §Persona Conflict Resolution` | Business PO |
| ADR tiering specification | Same ADR template section (consolidated) | Architect Agent |
| North star test process gate | `CLAUDE.md §North Star Test (Process Gate)` — new subsection in §Architectural Principles | PI Agent |
| Phase 0 exit artifact | `docs/process/sprint-plans/process-redesign-phase0-exit.md` | PM Agent orchestrates; PI Agent confirms |

All artifacts must exist in their canonical locations before the exit gate is evaluated. Artifacts that exist only in session context (not filed to disk) are treated as non-existent per the exit invariant.

---

## Exit Gate

Phase 0 closes when all of the following are satisfied:

1. All primary output artifacts are filed at their canonical locations (see table above).
2. PI Agent confirms that all output language is enforcement-grade, not aspirational.
3. EL has endorsed Phase 0 outputs — recorded in the Phase 0 exit artifact with the endorsement date.
4. Phase A sprint entry document is complete and filed at `docs/process/sprint-plans/process-redesign-phaseA-sprint-entry.md` before Phase A opens.
5. SESSION_STATE.md is updated to reflect Phase 0 complete and Phase A entry document filed.
6. Any secondary outputs (FD-2, FD-3, NS-1, NS-2) that were not completed are explicitly listed in the Phase 0 exit artifact with a documented rationale for deferral.
7. Any near-miss findings generated during Phase 0 are filed in `docs/process/near-miss-registry.md`.

Phase A does not open until all seven conditions above are met. PI Agent holds R for confirming the exit gate. If PI Agent finds the exit artifact incomplete, Phase A is blocked until the deficiency is remediated — not waived.

---

## North Star Validation

Before the exit gate passes, the PI Agent and Business PO must jointly answer the following question and file their answer in the Phase 0 exit artifact:

**If ADR-012 (ExternalSectorModule) had been required to carry the traceability requirements produced by Phase 0 — which persona it served, what the UX implication was, and whether it required UX Designer panel membership — would DEMO4-005 (HCL indicator computed but invisible in Zone 1D) have been caught before PR #773 was merged?**

If the answer is not "yes, before the PR merged," the Phase 0 outputs are not strong enough. The PI Agent should identify which specific requirement, if present, would have caught it — and the outputs must be strengthened until that requirement is present.

The validation question is the same structure as the north star test used to validate the sequencing plan itself (deliberation §Step 1). Phase 0 is held to the same standard it is designing.

---

## What Phase 0 Is Not

**Phase 0 does not implement any new feature or change any existing feature.** It produces written process requirements that govern future ADR authorship. No backend, frontend, or schema files are modified.

**Phase 0 does not redesign the founding document or the UX north star.** It identifies the gaps in those documents (catalogued in the deliberation §Gap Analysis) and closes the three highest-priority process gaps. The remaining gaps (FD-2, FD-3, FD-4, FD-5, NS-2, NS-3, NS-4, NS-5) are deferred and tracked in the Phase 0 exit artifact.

**Phase 0 does not define the execution lifecycle (mechanism 3).** That is Phase A. Phase 0 defines what the "Plan" step of the execution lifecycle reads from — the ADR with its now-required traceability fields.

**Phase 0 does not formalize sprint cadence (mechanism 1) or session boundary discipline (mechanism 4).** Those are Phases C and D. This sprint entry document is a forward-compatible artifact — it follows the spirit of the discipline being designed without waiting for the formal templates that Phase C will produce.
