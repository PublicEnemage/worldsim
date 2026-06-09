---
name: process-redesign-phase0-persona-traceability-spec
type: phase-0-working-document
phase: Phase 0 — UX/Persona Traceability Upstream of ADR Development
step: Step 3 — Business PO (persona traceability requirements)
status: COMPLETE — Step 3 output filed. Prerequisite for Step 4 (Architect).
authored-by: Business PO
date: 2026-06-09
sprint-entry: docs/process/sprint-plans/process-redesign-phase0-sprint-entry.md
prerequisite-inputs:
  - docs/process/design/process-redesign-phase0-dic-roadmap.md
  - docs/process/design/process-redesign-phase0-ux-traceability-spec.md
feeds-into: Step 4 (Architect — encodes into ADR template alongside UX traceability spec)
canonical-destination: New §Persona and UX Traceability section in ADR template (Architect determines placement in Step 4)
second-output: docs/ux/personas.md §Persona Conflict Resolution (appended directly — Output 2 of Phase 0)
---

# Phase 0 — Business PO: Persona Traceability Specification

**Authored by:** Business PO  
**Date:** 2026-06-09  
**Phase:** Phase 0 — UX/Persona Traceability Upstream of ADR Development  
**Sprint entry:** `docs/process/sprint-plans/process-redesign-phase0-sprint-entry.md`  
**Status:** COMPLETE — Step 3 outputs filed. Prerequisite for Step 4 (Architect).

---

## Activation Record

Business PO activated for Step 3 of Phase 0. This document provides the persona traceability requirements that the Architect will integrate with the UX traceability requirements (Step 2) to produce a unified ADR template section (Step 4). It also references Output 2 of Phase 0 — the persona conflict resolution ruling — which is filed directly in `docs/ux/personas.md §Persona Conflict Resolution`.

**Mandatory reading confirmed before producing output:**
- `docs/ux/personas.md` — read in full (all nine personas, entry state taxonomy, marquee cases, tertiary cases)
- `docs/ux/user-journeys.md` — read in full (Journeys A through H, journey dependency map)
- `docs/process/design/process-redesign-phase0-dic-roadmap.md` — read in full (20 binding guardrails, handoff notes for Step 3)
- `docs/process/design/process-redesign-phase0-ux-traceability-spec.md` — read in full (UX Designer Step 2 output)
- `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md` — XD-1 gap analysis section

**Step 3 delivers two things:**
1. **This document** — persona traceability specification (what a valid persona trace is; which ADRs must name a persona; what ADRs that cannot name a persona must document)
2. **`docs/ux/personas.md §Persona Conflict Resolution`** — the authoritative priority hierarchy ruling on the founding document / UX north star persona conflict (XD-1 gap)

---

## Part I — Which ADRs Must Name a Persona

**The obligation:**

An ADR that introduces or modifies a user-facing capability must name at least one persona the capability serves. "User-facing capability" means: any capability whose output is visible to, accessible by, or acted on by a human user of the tool.

This applies to Tier 1 and Tier 2 ADRs (per the UX traceability specification's tier classification). For Tier 3 (infrastructure) ADRs, a persona name is not required, but a forward trace to the downstream capability — and the persona that downstream capability will serve — is required.

**No ADR may be accepted that silently assumes a user.** Either the user is named, or the ADR explicitly states it does not directly serve a named persona and names the downstream capability that will.

---

### ADRs that must name a persona (Tier 1 and Tier 2)

| ADR subject | Persona tracing obligation | Example of compliance |
|---|---|---|
| New Zone 1 instrument or display surface | Must name persona, entry state, journey step, time ceiling | "Serves Persona 2 in Reactive state (Journey B Step 3); accessible in under 30 seconds from drawer open" |
| New indicator visible to users | Must name persona, entry state, journey step; must name income cohort if indicator touches distributional outputs | "Serves Persona 2 (Journey A Step 5, Preparatory state); bottom income quintile visibility in FrameworkPanel" |
| New mode or entry state | Must name all personas that mode/entry state serves and how; primary cognitive task must be named | "Mode 3 serves Persona 2 in Reactive entry state; primary cognitive task: real-time steering within human cost constraints" |
| New alert type, severity level, or alert panel modification | Must name the persona in the most time-constrained entry state this alert serves; must name what argument the alert enables | "Serves Persona 2 in Reactive state (Journey B Step 3); enables the argument: 'poverty headcount crosses CRITICAL at step 2 for bottom quintile'" |
| New analytical capability (multiplier, attribution, comparison) | Must name persona and negotiating leverage statement (INV-4) | See Part III below |

---

### ADRs that may not name a persona but must document a forward trace (Tier 3)

Infrastructure ADRs that have no direct user-facing output must include a forward trace statement:

> "This ADR does not directly serve a named persona. It enables [capability description], which serves [Persona N in entry state X, Journey Y Step Z]. The Tier 1/Tier 2 ADR for that capability is [ADR-N / TBD]."

If the Tier 1 or Tier 2 ADR for the downstream capability has not yet been authored, the forward trace must state "TBD" and the ADR panel must note this as an open obligation: the Tier 1/Tier 2 ADR must be authored before the infrastructure capability is considered mission-complete.

**The ADR-012 failure mode:** ADR-012 (ExternalSectorModule) was effectively a Tier 1 ADR (it introduced output visible to users) but carried no persona trace. The consequence was DEMO4-005: the human cost ledger indicator was computed but invisible in Zone 1D. A mandatory forward trace would have required naming "serves Persona 2 (Journey A Step 3b); Zone 1D four-framework current position updates with ExternalSectorModule output at each step" — a statement that would have been falsifiable against the Zone 1D acceptance criterion and would have caught the DEMO4-005 class of failure at ADR acceptance.

---

## Part II — What a Valid Persona Trace Looks Like

A persona trace is a structured statement within the ADR that the Business PO reviews before acceptance (Tier 2 ADRs) or co-authors with the panel (Tier 1 ADRs). The following seven elements are required for a complete persona trace. A trace missing any element is incomplete and blocks ADR acceptance pending remediation.

---

### Element P-1 — Persona identification

The trace names the persona by canonical name and number from `docs/ux/personas.md`.

Valid: "Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou archetype)"  
Invalid: "Finance ministry users" / "the primary user" / "analysts"

A persona trace may name multiple personas if the capability genuinely serves more than one. When multiple personas are named, the primary persona (the one whose entry state imposes the most demanding requirement) is identified explicitly.

---

### Element P-2 — Entry state

The trace names the specific entry state(s) from the canonical taxonomy: Investigative, Reactive, Preparatory, Demonstrative, Evaluative, Retrospective.

Valid: "Reactive entry state (90-second time ceiling, negotiation room context)"  
Invalid: "Under time pressure" / "in active use"

When multiple entry states are named, the Reactive entry state acceptance criterion governs if present — it is the hardest constraint (see persona conflict resolution ruling).

---

### Element P-3 — Journey reference

The trace names the specific journey and step from `user-journeys.md` using the canonical notation: "Journey [Letter] Step [Number][Subpart]."

Valid: "Journey B Step 3 (Scan: read the top MDA alert in under 30 seconds)"  
Invalid: "During negotiation" / "when reviewing alerts"

If the capability closes a `[Near-Term-Gap]` or `[Phase-3-TBD]` item in `user-journeys.md`, the trace references that gap notation explicitly: "Closes Journey F Step 7 [Near-Term-Gap] — downloadable tabular output."

---

### Element P-4 — Time or interaction ceiling

The trace states the maximum time or maximum interaction count within which the capability must be accessible in the named entry state. These values are derived from the user journeys and are not invented per-ADR.

**Canonical time ceilings by entry state (from `user-journeys.md`):**
- Reactive — Locate scenario: under 10 seconds
- Reactive — Reach relevant alert from drawer open: under 30 seconds
- Reactive — End-to-end (scenario load → citing finding): under 90 seconds
- Demonstrative — Zone 1 cold-reader orientation: under 60 seconds
- Mode 3 — Mode switch: under 3 seconds
- Mode 3 — Control input → instrument cluster update: under 10 seconds
- Preparatory — Full scenario analysis: 20–40 minutes

When a capability introduces a new access path, the ADR must state the time ceiling for that path and explain how it was determined.

---

### Element P-5 — Income cohort served (where applicable)

For any capability that produces or affects distributional outputs — poverty indicators, income-linked thresholds, cohort-level disaggregation — the trace names the specific income cohort from the canonical list.

**Canonical cohort list (from DE-2 guardrail, confirmed by Business PO):**
- Bottom two income quintiles (primary distributional target; "bottom quintile" alone is insufficient — Q1 and Q2 together)
- Pensioners 65+ (major public transfer recipients; pension system restructuring cases)
- Youth 18–35 in the tradable sector (employment shock, manufacturing, agriculture)
- Children 0–5 (early childhood development indicators; longest-tail intergenerational effects)
- "All cohorts" is acceptable only if the capability genuinely produces output for all four groups simultaneously; it is not acceptable as a shorthand for "we haven't specified which cohort"

Capabilities that produce only aggregate indicators (GDP, aggregate poverty headcount) must include Element P-5 stating: "This capability produces aggregate output only. Per-cohort breakdown path: [specified / deferred to ADR-N / not yet designed]."

---

### Element P-6 — Negotiating leverage statement (required for Persona 2 traces)

Any trace to Persona 2 (Finance Ministry Negotiator) must include a one-paragraph statement naming the specific argument Persona 2 can make in a negotiation as a result of this capability, that she could not make before. This is the INV-4 guardrail as a Business PO-enforced requirement.

*Format:*
> "After accessing this capability, Persona 2 can make the following specific argument: [statement in the form of a declarative sentence Persona 2 would speak at the negotiating table, naming indicator, step, cohort, and severity]."

Valid: "After accessing the multiplier sensitivity map, Persona 2 can state: 'At the programme's assumed fiscal multiplier of 0.5, poverty headcount for the bottom income quintile crosses CRITICAL at step 2. At the empirically validated multiplier of 1.5 (Blanchard-Leigh 2013), this crossing does not occur within the 4-step programme horizon. The multiplier assumption is driving the crossing, not the fiscal consolidation itself.'"

Invalid: "Enables better analysis of fiscal dynamics" / "supports the negotiation" / "improves situational awareness"

The negotiating leverage statement is the Business PO's test that the capability is mission-serving, not merely technically interesting.

---

### Element P-7 — North star test answer (for Tier 1 ADRs only)

Every Tier 1 ADR must include a one-paragraph answer to the founding document's north star test: "Does this decision make the tool more useful to a finance minister sitting across from an IMF negotiating team, in that moment?"

This is C-3 from the DIC Roadmap Section C, now encoded as a Business PO requirement. The answer must:
- Name a specific scenario (a finance minister in a named country/context, not a hypothetical)
- Name what the minister (or her specialist) can now do that they could not before
- Name whether this is a capability the IMF negotiating team's analysts already have (asymmetry assessment tie-in)

The answer may be "this is an infrastructure ADR that indirectly serves the minister through [capability N]." An indirect answer is acceptable; the question must not go unanswered.

---

## Part III — Negotiating Leverage Statement: Full Specification

The negotiating leverage statement (Element P-6) is the Business PO's most important addition to persona traceability. It operationalizes the founding document's mission claim. This section provides fuller guidance for authoring panels.

**The test:** Can the argument be spoken at a negotiating table? If it requires the listener to look up what "multiplier sensitivity coefficient" means, the argument fails the test. The statement should be speakable by Persona 2, not by an economist describing Persona 2's work.

**Subject:** The argument uses first or third person from Persona 2's perspective, not from the developer's perspective. "The simulation shows X" is acceptable; "the module produces output Y" is not.

**Specificity floor:** Indicator + step + cohort + severity or direction. Arguments missing any of these four elements are not specific enough to constitute a negotiating position. "Human development risks are higher under the proposed path" is an observation, not an argument.

**Falsifiability:** The argument must be falsifiable by the tool. If a skeptical IMF counterpart says "your model is wrong," Persona 2 must be able to respond by pointing to a specific indicator, confidence tier, and comparison group. The argument's methodology must be defensible in the room.

**Examples by capability type:**

| Capability | Adequate negotiating leverage statement |
|---|---|
| Reserve drawdown visualization | "Under this trade shock, reserve coverage drops below the 3-month import floor at step 2 — the specific threshold the IMF uses to trigger its own reserve adequacy warnings. The proposed programme design does not account for this drawdown arc." |
| Multiplier sensitivity map | "The programme's projections assume a fiscal multiplier of 0.5. At the IMF's own revised estimate of 1.0-1.5 for programme countries (Blanchard-Leigh 2013), poverty headcount for the bottom quintile crosses CRITICAL at step 2 rather than holding stable. The multiplier assumption is the primary driver of this difference." |
| Conditionality term attribution | "The minimum wage cut applied at step 1 — not the pension reduction — is what pushes poverty headcount across the CRITICAL threshold for the bottom quintile at step 2. Our counter-proposal delays the minimum wage adjustment by one step; the threshold crossing disappears." |
| Cohort disaggregation in Zone 1 | "The aggregate poverty headcount holds below the floor — but the bottom income quintile specifically crosses WARNING at step 2. The aggregate is masking the distributional impact. This is the cohort your programme's social protection floor was designed to protect." |

---

## Part IV — Handoff Summary for Step 4 (Architect)

The Architect's Step 4 task is to integrate the UX traceability requirements (Step 2) and the persona traceability requirements (this document) into a single, coherent ADR template section. The following is a summary of what the Architect receives from the Business PO:

**From this document:**
1. Three-category ADR persona obligation (Tier 1 — must name persona; Tier 2 — persona trace reviewed by BPO; Tier 3 — forward trace required)
2. Seven-element valid persona trace format (P-1 through P-7)
3. Canonical cohort list for Element P-5
4. Negotiating leverage statement specification for Element P-6
5. North star test obligation for Element P-7 (Tier 1 ADRs)
6. Forward trace statement format for Tier 3 ADRs

**From Step 2 (UX traceability spec):**
1. Three-tier ADR classification (Tier 1 UX panel required; Tier 2 persona trace + UX review; Tier 3 indirect waiver)
2. Seven-element UX implication statement (UX-1 through UX-7)
3. Four hard UX invariants
4. Adequate UX review definition per tier

**Integration objective for Step 4:**
The ADR template should contain a single section (e.g., `§Persona and UX Traceability`) that consolidates the persona trace requirements and the UX implication statement into a coherent checklist a panel can complete. The section should not require the panel to read two separate documents — this spec and the UX spec — to know what is required. The Architect synthesizes them.

**On the XD-1 resolution:**
The persona conflict resolution ruling (Output 2) is filed in `docs/ux/personas.md §Persona Conflict Resolution`. The ADR template's persona traceability section should cross-reference this ruling: "When tracing to multiple personas whose requirements conflict, apply the priority hierarchy in `docs/ux/personas.md §Persona Conflict Resolution`."

---

*Document complete. Filed as Step 3 (persona traceability) output for Phase 0.*  
*Output 2 (persona conflict resolution ruling) is filed separately in `docs/ux/personas.md §Persona Conflict Resolution`.*
