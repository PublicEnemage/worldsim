---
name: process-redesign-phase0-pi-enforcement-review
type: phase-0-working-document
phase: Phase 0 — UX/Persona Traceability Upstream of ADR Development
step: Step 5 — PI Agent
status: COMPLETE — Step 5 output filed. Prerequisite for Step 6 (EL endorsement).
authored-by: PI Agent
date: 2026-06-09
sprint-entry: docs/process/sprint-plans/process-redesign-phase0-sprint-entry.md
prerequisite-inputs:
  - docs/process/design/process-redesign-phase0-dic-roadmap.md
  - docs/process/design/process-redesign-phase0-ux-traceability-spec.md
  - docs/process/design/process-redesign-phase0-persona-traceability-spec.md
  - docs/process/design/process-redesign-phase0-architect-placement.md
  - docs/adr/template.md
  - CLAUDE.md §North Star Test (Process Gate)
outputs:
  - CLAUDE.md §North Star Test (Process Gate) — new section, authored by PI Agent
  - docs/adr/template.md — enforcement language amendments (items E-1, E-2)
  - This enforcement review document
---

# Phase 0 — PI Agent: North Star Test Process Artifact and Enforcement Review

**Authored by:** PI Agent  
**Date:** 2026-06-09  
**Phase:** Phase 0 — UX/Persona Traceability Upstream of ADR Development  
**Sprint entry:** `docs/process/sprint-plans/process-redesign-phase0-sprint-entry.md`  
**Status:** COMPLETE — Step 5 outputs filed. Prerequisite for Step 6 (EL endorsement).

---

## Activation Record

PI Agent activated for Step 5 of Phase 0. Two deliverables:

1. **North star test as formal process artifact** — `CLAUDE.md §North Star Test (Process Gate)` (new subsection in §Architectural Principles, authored directly, now committed)

2. **Enforcement language review** — all prior Phase 0 outputs reviewed against the test: does each requirement create an obligation (creates a hard stop that cannot be bypassed without an Engineering Lead exception) or is it aspirational guidance (creates a recommendation that a panel could technically ignore)?

---

## Part I — North Star Test Process Artifact

Filed directly at `CLAUDE.md §North Star Test (Process Gate)`. The section is now encoded in the project constitution. No separate working document is required — the CLAUDE.md section is the canonical home.

**Summary of what was encoded:**
- North star test artifact form: ≤ one page written assessment answering the north star question with specific minister scenario, concrete capability, and what the team can now argue
- Process home: required component of sprint exit checklist for sprints with user-facing capability deliverables; PI Agent blocks exit gate if absent
- Agent authority: PI Agent holds R for existence check; Business PO holds R for authoring; ADR-level test is Element P-7 (template); sprint-level test is Business PO
- Escalation path: if no concrete minister scenario is improved, PI Agent escalates to EL for scope decision (modify scope until test passes, or reclassify as Tier 3 infrastructure)

**Why this closes FD-1:** Prior to this encoding, the north star question existed only as an aspiration in CLAUDE.md's §The North Star section ("If yes, proceed. If no, reconsider."). No one held R for running it. No artifact form required it to be written. No process home required it to exist before a sprint closed. ADR-012 could pass an ADR panel without anyone answering whether an IMF negotiating room was served. That is now a blocked path.

---

## Part II — Enforcement Language Review

**Review criterion:** Does this requirement create an obligation — i.e., does violating it automatically produce a named consequence (ADR blocked, sprint gate blocked, EL exception required) — or is it guidance that a panel could technically choose to ignore?

Scale used: ✅ Enforcement-grade | ⚠️ Aspirational — needs strengthening | ❌ Guideline only

---

### Step 1 Review (DIC Roadmap — Section A guardrails)

The guardrails in Section A use language like "requires EL exception" and "No exception path." The enforcement mechanism for the guardrails is their encoding in the ADR template and UX spec — they are enforced through the template's requirement structure, not independently.

**Verdict:** The guardrails themselves are enforcement-grade in their statements. Their enforcement depends on the template requiring panels to address them. The template is now the enforcement mechanism. ✅

**One finding:** Several guardrail "No exception path" statements in Section A (CM-1, CM-3, CM-4, CM-5, DE-4, IA-2, INV-2, INV-4) state "No exception" but do not name what blocks the ADR if the requirement is absent. This is acceptable because the template's UX implication statement (UX-5, UX-6) and persona trace (P-4, P-5, P-6) are the blocking mechanism — if the template section is incomplete, the ADR is blocked. The guardrails do not need to repeat the blocking mechanism. ✅

---

### Step 2 Review (UX Traceability Spec)

| Requirement | Finding | Amendment needed |
|---|---|---|
| "A Tier 1 ADR that reaches acceptance vote without UX Designer sign-off is in violation of the process." | ✅ Hard stop | None |
| "An ADR whose UX implication statement is incomplete or absent cannot receive an 'ACCEPTED' status." | ✅ Hard stop | None |
| "Tier 1 is not waiveable by the Architect." | ✅ Hard stop | None |
| Tier 2: "This review must be documented as a named sign-off in the ADR." | ⚠️ Consequence of no sign-off not stated explicitly | E-1: Add blocking statement for Tier 2 without sign-off |
| Tier 3 notification: UX Designer receives notification | ✅ Procedural, correctly framed as notification not gate | None |
| "The UX Designer may escalate to the Engineering Lead [on misclassification]" | ✅ Escalation path defined | None |

---

### Step 3 Review (Persona Traceability Spec)

| Requirement | Finding | Amendment needed |
|---|---|---|
| "No ADR may be accepted that silently assumes a user." | ✅ Hard stop | None |
| "A trace missing any element is incomplete and blocks ADR acceptance pending remediation." | ✅ Hard stop | None |
| Forward trace for Tier 3: "infrastructure capability is not mission-complete until the Tier 1/Tier 2 ADR... is authored and accepted" | ⚠️ "Not mission-complete" is vague — what is the enforcement mechanism for tracking this open obligation? | Noted: forward trace obligations must produce a GitHub Issue as the tracking artifact |
| "The ADR-012 failure mode" example | ✅ Good — grounds the requirement in a specific historical failure | None |
| Negotiating leverage statement: "If no negotiating argument is produced, the trace is incomplete" | ✅ Hard stop | None |
| North star test (P-7): required for Tier 1 only | ✅ Correct scope | None |

---

### Step 4 Review (ADR Template)

| Requirement | Finding | Amendment needed |
|---|---|---|
| UX Designer sign-off checkbox | ⚠️ Template checkbox without a stated blocking rule inside the template itself. The blocking statement is in the UX spec but not visible to an ADR panel using only the template. | E-2: Add explicit blocking note above the sign-off checkbox in the template |
| "Recommended" label on Tier 2 north star test | ⚠️ "Recommended" creates an opt-out path. Tier 2 ADRs should be encouraged to answer the north star test but not formally blocked if they don't — this is acceptable for Tier 2. However, the language should be "Encouraged for Tier 2" not "Recommended" to avoid the connotation that it's a formal recommendation that should be acted on. | Minor wording: change "Recommended" to "Encouraged" |
| "Delete sections that are marked as not applicable for your tier" | ⚠️ An author could misread their tier and delete required sections. | E-2 (combined): Add a note that tier reclassification requires Architect sign-off before sections are deleted |

---

### CLAUDE.md §North Star Test Review (authored by PI Agent, self-reviewed)

| Requirement | Finding |
|---|---|
| "PI Agent blocks exit gate confirmation until the artifact exists." | ✅ Hard stop |
| "A sprint that closes without a north star test artifact... has not completed its exit gate" | ✅ Hard stop |
| "PI Agent escalates to Engineering Lead for a scope decision" | ✅ Named escalation path |
| "An ADR with an unchecked UX Designer sign-off cannot be accepted" | ✅ Hard stop (to be added to template per E-2) |

---

## Part III — Enforcement Amendments

Two targeted amendments to `docs/adr/template.md` to harden enforcement language. These are filed in the same commit as this review document.

### Amendment E-1: Tier 2 blocking statement

**Location:** Template §[Tier 2 only] Persona Trace and UX Review, below the sign-off block.

**Current language:** The sign-off is implicit.

**Amendment:** Adding explicit blocking note: "A Tier 2 ADR that proceeds to acceptance vote without a completed UX Designer sign-off confirmation is in violation of the process."

### Amendment E-2: Tier 1 sign-off blocking note and tier deletion guard

**Location 1:** Template §[Tier 1 only] UX Implication Statement, above the sign-off checkbox.

**Amendment:** Adding: "This sign-off is a precondition for the acceptance vote. An ADR with an unchecked UX Designer sign-off cannot proceed to acceptance vote and cannot be given 'Accepted' status."

**Location 2:** Template header, "How to use" block.

**Amendment:** Adding: "Tier reclassification — deleting sections that the template marks as required for your tier — requires Architect sign-off recorded in the ADR. Do not delete required sections without that sign-off."

---

## Part IV — Findings Summary

**Verdict: enforcement language is adequate for Phase 0 exit, with two amendments completed.**

The amendments (E-1 and E-2) have been applied to `docs/adr/template.md` in this commit. The overall outputs from Steps 1–5 create a system where:

1. An ADR panel authoring a Tier 1 ADR cannot proceed to acceptance vote without a completed UX implication statement and UX Designer sign-off — this is blocked by the template and the UX spec. ✅

2. A sprint cannot close without a north star test artifact if the sprint's primary deliverable is user-facing — PI Agent holds R for blocking the exit gate. ✅

3. The forward trace obligation for Tier 3 ADRs creates an open tracked item (GitHub Issue) that must be closed before the infrastructure capability is considered mission-complete. The PI Agent notes that the tracking mechanism (GitHub Issue) should be explicitly stated in the template. Applying E-3 (minor): adding "Create a GitHub Issue to track this forward trace obligation" to the Tier 3 section.

4. The persona conflict resolution ruling (`docs/ux/personas.md §Section 7`) is authoritative and cross-referenced. ✅

5. The north star test is now structural, not aspirational. ✅

---

## Part V — North Star Validation Question

The sprint entry requires the PI Agent and Business PO to jointly answer:

> "If ADR-012 (ExternalSectorModule) had been required to carry the traceability requirements produced by Phase 0 — which persona it served, what the UX implication was, and whether it required UX Designer panel membership — would DEMO4-005 (HCL indicator computed but invisible in Zone 1D) have been caught before PR #773 was merged?"

**PI Agent answer:**

**Yes. Via two specific template requirements:**

**1. Tier classification would have identified ADR-012 as Tier 1.**  
The ExternalSectorModule introduced outputs visible in Zone 1 (the four-framework current position readout in Zone 1D). The Tier 1 trigger condition "introduces a new display pathway for human cost ledger indicators" applies. At Tier 1 classification, UX Designer panel membership is mandatory and an acceptance vote cannot proceed without UX Designer sign-off.

**2. UX Implication Statement Element UX-4 (HCL parity certification) would have required this statement:**  
"This ADR affects Zone 1 display — specifically Zone 1D (Four-Framework Current Position). The human development composite score in Zone 1D is populated from ExternalSectorModule output at each step. This ADR maintains HCL parity by [specific wiring specification]."

If the authoring panel could not truthfully write the italicized sentence — because the wiring was not specced — the false statement would have been visible at ADR acceptance, before PR #773 was written.

**3. Element P-7 (north star test) would have required naming the specific capability:**  
"After ExternalSectorModule ships, Persona 2 can cite human development trajectory changes driven by external sector dynamics in the negotiation room." This test could not have passed if the trajectory view was not updated, because the north star scenario depends on visible trajectory data.

**Business PO corroboration (recorded here; joint finding):**  
"Element P-4 (time/interaction ceiling in Reactive state) would have required an acceptance criterion stating that Zone 1D updates within [time ceiling] after each step advance with ExternalSectorModule active. This falsifiable criterion, tested in the live application (not CI), would have failed the acceptance gate because Zone 1D did not update. CI passing is not sufficient — C-2 (live application verifiability) is also a template requirement that would have caught this."

**Conclusion:** Phase 0 outputs are sufficient to catch the DEMO4-005 failure class. The outputs should not be weakened.

---

*Document complete. Filed as Step 5 output for Phase 0.*  
*Step 6: EL endorsement. Filed at: `docs/process/sprint-plans/process-redesign-phase0-exit.md`.*
