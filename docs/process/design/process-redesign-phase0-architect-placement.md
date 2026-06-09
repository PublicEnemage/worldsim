---
name: process-redesign-phase0-architect-placement
type: phase-0-working-document
phase: Phase 0 — UX/Persona Traceability Upstream of ADR Development
step: Step 4 — Architect Agent
status: COMPLETE — Step 4 output filed. Prerequisite for Step 5 (PI Agent).
authored-by: Architect Agent
date: 2026-06-09
sprint-entry: docs/process/sprint-plans/process-redesign-phase0-sprint-entry.md
prerequisite-inputs:
  - docs/process/design/process-redesign-phase0-dic-roadmap.md
  - docs/process/design/process-redesign-phase0-ux-traceability-spec.md
  - docs/process/design/process-redesign-phase0-persona-traceability-spec.md
  - docs/ux/personas.md §Persona Conflict Resolution
canonical-outputs:
  - docs/adr/template.md
  - docs/CODING_STANDARDS.md §ADR Requirements (reference added)
---

# Phase 0 — Architect Agent: ADR Tiering Specification and Canonical Placement Decision

**Authored by:** Architect Agent  
**Date:** 2026-06-09  
**Phase:** Phase 0 — UX/Persona Traceability Upstream of ADR Development  
**Sprint entry:** `docs/process/sprint-plans/process-redesign-phase0-sprint-entry.md`  
**Status:** COMPLETE — Step 4 outputs filed. Prerequisite for Step 5 (PI Agent).

---

## Canonical Placement Decision

**Question:** Where does the Phase 0 `§Persona and UX Traceability` section live — as a new section in a standalone `docs/adr/template.md`, or as a subsection of `CLAUDE.md §Architectural Principles`?

**Decision: `docs/adr/template.md` (new file, canonical template)**

**Rationale:**

1. **Discovery:** ADR authors work in the `docs/adr/` directory. A template at `docs/adr/template.md` is discovered at the point of use. A subsection in CLAUDE.md is discovered only if the author reads CLAUDE.md before authoring the ADR, which is a session-initialization read, not an authorship-time read.

2. **Size:** CLAUDE.md is already substantial. The Phase 0 traceability requirements add significant length that belongs in a reference document, not in the project constitution. CLAUDE.md should point to the template; the template should contain the requirements.

3. **Coherence:** The template collects all authorship requirements in one place — the tier classification, persona trace, UX implication statement, silent failure mode, asymmetry assessment, north star test, mission impact statement. An author consulting a single template file is better served than one cross-referencing CLAUDE.md + the UX spec + the persona spec.

4. **Precedent:** CODING_STANDARDS.md §Required Sections already showed the basic ADR skeleton in a code block. The canonical template extends this with Phase 0 requirements and supersedes that code block as the authoritative reference.

**Secondary change:** `CODING_STANDARDS.md §ADR Requirements §Required Sections` updated to reference `docs/adr/template.md` and the tier classification requirement. The existing code block in CODING_STANDARDS.md is not removed — it retains the minimal standard sections for quick reference. But the template is canonical.

---

## ADR Tiering Specification: Final Encoding

The three-tier classification integrates the UX Designer's tier boundaries (Step 2) with the Business PO's persona obligation boundaries (Step 3). They are consistent — both use the same three-tier structure — and are encoded in the template as a single unified section.

### Tier 1 — Full panel required

**Classification criteria (any of the following):**
- Introduces or modifies a Zone 1 surface (primary viewport, no interaction required)
- Reassigns an element between zones (Zone 1 → Zone 2, Zone 2 → Zone 1, etc.)
- Introduces a new visual treatment for severity, uncertainty, or confidence tier at any zone
- Modifies MDA alert panel placement, visible count, scroll behavior, or severity display
- Introduces or removes a mode (Mode 1, 2, 3 or future modes)
- Introduces or modifies an entry state (Investigative, Reactive, Preparatory, Demonstrative, Evaluative, Retrospective)
- Introduces a new interaction pattern as the primary access path for a user-facing capability
- Modifies the Mode 3 control plane zone
- Introduces a new display pathway for human cost ledger indicators

**Panel composition:** UX Designer (C or R), Frontend Architect (C), relevant DIC agent(s) per `docs/process/agent-raci.md`, Engineering Lead (A). The UX Designer holds sign-off before acceptance vote.

**Requirements at acceptance:**
- 7-element persona trace (P-1 through P-7) complete
- 7-element UX implication statement (UX-1 through UX-7) complete with UX Designer sign-off
- Silent failure mode specified
- Asymmetry assessment (if analytical capability)
- North star test answered
- Mission impact statement

### Tier 2 — Persona trace + UX Designer review

**Classification criteria (any of the following):**
- Introduces a new indicator, composite score, or capability through existing display surfaces
- Introduces or modifies a schema field whose value appears in a user-facing surface
- Extends an existing analytical module with new user-visible outputs
- Introduces historical fixtures serving a specific user journey

**Panel composition:** Standard per `docs/process/agent-raci.md`. UX Designer is not a required panel member but reviews the persona trace before acceptance vote.

**Requirements at acceptance:**
- Elements P-1 through P-5 complete (+ P-6 if Persona 2)
- UX Designer sign-off on persona trace adequacy
- Silent failure mode specified
- Asymmetry assessment (if analytical capability)
- Mission impact statement

### Tier 3 — Indirect connection waiver

**Classification criteria (all of the following must be true):**
- Infrastructure, computation, or data architecture with no direct user-facing output
- UX connection is ≥2 levels of indirection
- Architect has documented the downstream capability and the Tier 1/Tier 2 ADR that will handle display implications

**Panel composition:** Standard per `docs/process/agent-raci.md`. UX Designer is notified at acceptance; no review required.

**Requirements at acceptance:**
- Forward trace statement naming downstream persona and capability
- Signal latency impact statement (IA-5 — always required regardless of tier)
- Tier 3 waiver documented by Architect with UX Designer notification

---

## Integration Notes

The template synthesizes the following requirements from Steps 1–3 into a single coherent structure:

| Requirement | Source | Where in template |
|---|---|---|
| Tier classification | UX spec + Persona spec | §Tier Classification (header section) |
| Persona trace 7 elements | Persona spec P-1 through P-7 | §Persona and UX Traceability (Tier 1 subsection) |
| UX implication statement 7 elements | UX spec UX-1 through UX-7 | §Persona and UX Traceability (Tier 1 subsection) |
| Tier 2 persona trace review | Both specs | §Persona and UX Traceability (Tier 2 subsection) |
| Forward trace format | Persona spec | §Persona and UX Traceability (Tier 3 subsection) |
| Silent failure mode | DIC Roadmap C-1 | §Silent Failure Mode |
| Asymmetry assessment | DIC Roadmap INV-1 | §Asymmetry Assessment |
| North star test | DIC Roadmap C-3 | §North Star Test |
| Mission impact statement | DIC Roadmap INV-5 | §Mission Impact Statement |
| Minimum data tier | DIC Roadmap INV-3 | §Minimum Data Tier |
| HCL parity certification | DIC Roadmap DE-1, UX spec UX-H1 | §UX Implication Statement UX-4 |
| Irreversibility signal integrity | DIC Roadmap IA-1, IA-4 | §UX Implication Statement UX-6 |
| Negotiating leverage statement | DIC Roadmap INV-4 | §Persona Trace P-6 |
| Income cohort naming | DIC Roadmap DE-2 | §Persona Trace P-5 |
| Entry state + time ceiling | DIC Roadmap DE-4 | §Persona Trace P-2 + P-4 |

**The PI Agent (Step 5)** should review the template language for enforcement grade. Specifically:
- Every "required" designation should read as a hard stop, not a recommendation
- The UX Designer sign-off mechanism (checkbox) must be stated as a precondition for acceptance vote, not a post-acceptance formality
- The silent failure mode and forward trace obligations must read as mandatory, not optional

---

## Architect Note on CLAUDE.md Amendment

The sprint plan states that the ADR traceability requirements might land in `CLAUDE.md §Architectural Principles`. The Architect's decision is to place them in `docs/adr/template.md` with a CODING_STANDARDS.md reference. However, CLAUDE.md §Architectural Principles should carry a one-line reference to the template so that anyone reading CLAUDE.md knows the template exists. This amendment is Step 5 (PI Agent) scope — it belongs in the `§North Star Test (Process Gate)` section that the PI Agent will create, which is the natural anchor point for the process-gate language. The Architect does not amend CLAUDE.md here to avoid the Step 5 overlap.

---

*Document complete. Filed as Step 4 output for Phase 0 — UX/Persona Traceability Upstream of ADR Development.*  
*Prerequisite for Step 5 (PI Agent — north star test process artifact and enforcement review).*
