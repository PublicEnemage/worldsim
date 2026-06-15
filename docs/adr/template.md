---
name: adr-template
type: template
version: 2026-06-09
phase0-encoded: true
canonical-authority: This template is the canonical ADR authorship reference from Phase 0 onward.
prerequisite-sources:
  - docs/process/design/process-redesign-phase0-ux-traceability-spec.md
  - docs/process/design/process-redesign-phase0-persona-traceability-spec.md
  - docs/ux/personas.md §Persona Conflict Resolution
---

# ADR Template — WorldSim

> **How to use this template:**  
> Copy this file to `docs/adr/ADR-NNN-short-name.md`. Replace all `[bracketed placeholders]`
> with actual content. Delete sections that are marked as not applicable for your tier.
> The tier classification section (below) determines which sections are required.
> Before filling in any section, read `docs/ux/personas.md §Persona Conflict Resolution`
> to understand the persona priority hierarchy that governs when persona requirements conflict.
>
> **Tier reclassification rule:** Deleting sections that the template marks as required for
> your tier — on the basis that you have reclassified the ADR to a lower tier — requires
> Architect sign-off recorded in the ADR before those sections are removed. Do not delete
> required sections without that sign-off. Misclassification to avoid traceability requirements
> is a process violation.

---

# ADR-NNN: [Title]

## Tier Classification

**Tier:** [1 / 2 / 3]

**Justification:**  
[One sentence explaining why this ADR belongs in this tier. Tier 1: introduces or modifies a Zone 1 surface, entry state, mode, or visual treatment for severity/uncertainty/confidence. Tier 2: introduces a new capability or indicator that uses existing display surfaces. Tier 3: infrastructure with ≥2 levels of indirection from any user-facing output.]

**Sections required by tier:**

| Section | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Persona Trace (7-element) | Required | Elements P-1–P-5, P-6 if Persona 2 | Not required |
| UX Implication Statement (7-element) | Required — UX Designer sign-off | UX Designer trace review | Not required |
| Forward Trace Statement | Not applicable | Not applicable | Required |
| Silent Failure Mode | Required | Required | Required |
| Asymmetry Assessment | Required if analytical capability | Required if analytical capability | Not applicable |
| North Star Test | Required | Recommended | Not required |
| Mission Impact Statement | Required | Required | Not required |

---

## Status

`Proposed` | `Accepted` | `Deprecated` | `Superseded by ADR-NNN`

---

## Validity Context

> *Fill in when the ADR is accepted. Leave blank at Proposed.*

**Standards Version:** [YYYY-MM-DD of CLAUDE.md / CODING_STANDARDS.md used at authorship]  
**Valid Until:** [Milestone or condition under which this ADR must be reviewed]  
**License Status:** `PROPOSED → ACCEPTED` on [date]

**Panel:**
- [Agent name] ([R/A/C/I] — [brief role description])
- [Agent name] ([R/A/C/I] — [brief role description])
- Engineering Lead (A — accountable on all ADR decisions)

**Renewal Triggers:**  
[List conditions under which this ADR must transition ACCEPTED → UNDER-REVIEW.]

---

## Date

[YYYY-MM-DD]

---

## Context

### Background

[What problem is this ADR solving? What constraints exist? Why is this decision necessary now? Include relevant external context — which user journey step(s) make this decision necessary, which milestone gap(s) this addresses, what would happen if no decision were made.]

### Problem Framing

[Name the persona and the specific moment where the absence of this capability produces a failure. Example: "In Journey B Step 3 (Reactive state), Persona 2 cannot identify which specific conditionality term causes the threshold crossing — she can see that a crossing occurred but not which term drove it. This means she can produce a finding but not a negotiating position."]

---

## Decision

[What did we decide? State it precisely enough that an implementation agent can build to this spec without asking clarifying questions. Include interface contracts, schema changes, and display specifications here — not in a separate document.]

---

## Persona and UX Traceability

> *This section is required for Tier 1 and Tier 2 ADRs. The appropriate subsection below is determined by tier. Delete the subsections that do not apply to your tier.*  
> *Authority: `docs/process/design/process-redesign-phase0-ux-traceability-spec.md` and `docs/process/design/process-redesign-phase0-persona-traceability-spec.md`*  
> *Persona conflict resolution: `docs/ux/personas.md §Persona Conflict Resolution`*

---

### [Tier 1 only] Persona Trace

> *Complete all seven elements. A trace missing any element is incomplete and blocks ADR acceptance pending remediation.*

**P-1 — Persona identification:**  
[Persona name and number from `docs/ux/personas.md`. Example: "Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou archetype)". Multiple personas: name the primary first.]

**P-2 — Entry state:**  
[Canonical entry state(s): Investigative / Reactive / Preparatory / Demonstrative / Evaluative / Retrospective. Include time ceiling. Example: "Reactive entry state (90-second total ceiling, negotiation room context)."]

**P-3 — Journey reference:**  
[Canonical notation: "Journey [Letter] Step [Number][Subpart]". Example: "Journey B Step 3 (Scan: read the top MDA alert in under 30 seconds)." If closing a gap: "Closes Journey F Step 7 [Near-Term-Gap] — downloadable tabular output."]

**P-4 — Time or interaction ceiling:**  
[Maximum time or interaction count for the named entry state. Use canonical values from `user-journeys.md` wherever possible. Example: "Alert must be visible without any interaction within 5 seconds of the EntityDetailDrawer opening (Journey B Step 3)."]

**P-5 — Income cohort served (where applicable):**  
[From canonical list: bottom two income quintiles / pensioners 65+ / youth 18–35 tradable sector / children 0–5. If aggregate only: "This capability produces aggregate output only. Per-cohort breakdown path: [specified/deferred]."]

**P-6 — Negotiating leverage statement (required if tracing to Persona 2):**  
["After accessing this capability, Persona 2 can make the following specific argument: [statement naming indicator + step + cohort + severity or direction, speakable at a negotiating table]."]

**P-7 — North star test answer (Tier 1 only):**  
[One paragraph. "Does this decision make the tool more useful to a finance minister sitting across from an IMF negotiating team, in that moment?" Answer with a specific scenario, a named country if possible, what the minister or her specialist can now do that they could not before, and whether this closes an asymmetry gap (per `docs/process/design/process-redesign-phase0-dic-roadmap.md §Section B`).]

---

### [Tier 1 only] UX Implication Statement

> *Complete all seven elements. UX Designer sign-off is required before ADR acceptance vote.*  
> *Authority: `docs/process/design/process-redesign-phase0-ux-traceability-spec.md`*

**UX-1 — Zone assignment and hierarchy certification:**  
["This ADR places [element] in Zone [N]. [Previous zone if reassigned.] This assignment is consistent with `information-hierarchy.md` §[section] / This assignment conflicts with §[section] because [reason]; resolution: [ruling or EL exception reference]."]

**UX-2 — Primary cognitive task alignment:**  
["This capability primarily serves Mode [N]'s primary cognitive task ([task name]). In Mode [M], it [serves/does not serve] the primary task because [reason]." Mode tasks: Mode 1 = trajectory reconstruction; Mode 2 = threshold-safe path construction; Mode 3 = real-time steering within human cost constraints.]

**UX-3 — Entry state coverage (falsifiable acceptance criteria):**  
[For each named entry state, a specific falsifiable acceptance criterion verifiable by observation in the live application. Format: "In [entry state] (Persona [N], Journey [X] Step [Y]): user can reach [specific output] in [time/interaction ceiling]. Acceptance criterion: [specific observable application state — NOT 'CI passes']."]

**UX-4 — HCL parity certification:**  
[Two valid states: (a) "This ADR does not affect HCL visual weight relative to financial indicators. HCL parity is maintained." (b) "This ADR affects [specific aspect]. Effect: [description]. Engineering Lead exception required: [reference]." No third state — the UX Designer must actively verify, not assume.]

**UX-5 — Uncertainty display specification:**  
[Name: (a) what confidence tier information is displayed, (b) where it appears, (c) what it shows for Tier 3 SYNTHETIC_COMPARABLE — the word "synthetic" must appear verbatim, (d) what it shows for Tier 4, (e) what the Structural Absence Declaration shows. "Per the standard" is not a specification.]

**UX-6 — Irreversibility signal integrity certification:**  
[For ADRs touching Zone 1, alert panel, or severity display: certify that TERMINAL alerts remain visually distinct from CRITICAL with no implementation discretion, and that TERMINAL + CRITICAL alerts are visible without scroll at 1280×800 desktop and 1024×768 tablet. Include a CI-testable acceptance criterion naming the scenario and alert count.]

**UX-7 — User journey coverage:**  
[Named journeys and steps from `user-journeys.md` served or modified. For each: what the user can now do that was previously unavailable or impeded. If closing a `[Near-Term-Gap]` or `[Phase-3-TBD]` item, reference it explicitly.]

**UX Designer sign-off:**  
This sign-off is a precondition for the acceptance vote. An ADR with an incomplete sign-off
block cannot proceed to acceptance vote and cannot be given `Accepted` status. All four
fields below are required — a checkbox without the structured attestation is non-compliant.

**Reviewing agent:** [UX Designer Agent]  
**Session context:** [One of: `Separate session, EL-triggered YYYY-MM-DD` | `Same session as ADR authorship — acknowledged`]  
**Governing documents reviewed:** [Named sections required — e.g., `information-hierarchy.md §1B`, `north-star.md §Primary Cognitive Tasks`. Generic references ("governing premises") do not satisfy this field.]  
**Concerns found:** [N — listed below with each concern on its own line | `None`]  

`[ ]` UX Designer sign-off. [Date]

---

### [Tier 2 only] Persona Trace and UX Review

> *Complete elements P-1 through P-5 and P-6 (if Persona 2). UX Designer reviews and confirms.*

**P-1 — Persona identification:** [Name and number]

**P-2 — Entry state:** [Entry state + time ceiling]

**P-3 — Journey reference:** [Journey Letter + Step Number]

**P-4 — Time or interaction ceiling:** [Maximum time or interaction count]

**P-5 — Income cohort served:** [Cohort from canonical list, or aggregate-only acknowledgment]

**P-6 — Negotiating leverage statement** *(if Persona 2):*  
["After accessing this capability, Persona 2 can make the following specific argument: [statement]."]

**UX Designer review:**  
A Tier 2 ADR that proceeds to acceptance vote without a completed UX Designer sign-off
confirmation is in violation of the process. PI Agent holds R for blocking the vote if
sign-off is absent. All four fields below are required.

**Reviewing agent:** [UX Designer Agent]  
**Session context:** [One of: `Separate session, EL-triggered YYYY-MM-DD` | `Same session as ADR authorship — acknowledged`]  
**Governing documents reviewed:** [Named sections — e.g., `north-star.md §Primary Cognitive Tasks`, `user-journeys.md §Journey B`. Generic references do not satisfy this field.]  
**Concerns found:** [N — listed below | `None`]  

`[ ]` UX Designer: Elements P-1–P-5 (and P-6 if applicable) confirmed present and adequate. [Date]  
Or: "UX Designer review: persona trace incomplete. Missing: [elements]. Blocked from acceptance until remediated."

---

### [Tier 3 only] Forward Trace Statement

> *Required for all Tier 3 infrastructure ADRs. The forward trace obligation is tracked at ADR acceptance and remains open until the named Tier 1 or Tier 2 ADR is authored.*

"This ADR does not directly serve a named persona. It enables [capability description], which will serve [Persona N in entry state X, Journey Y Step Z]. The Tier 1/Tier 2 ADR for that capability is [ADR-N / TBD]."

If TBD: note this as an open obligation and create a GitHub Issue to track it. The infrastructure
capability is not mission-complete until the Tier 1/Tier 2 ADR for the downstream user-facing
capability is authored and accepted. Reference the GitHub Issue number in this section so the
obligation is tracked beyond the ADR document itself.

---

## Silent Failure Mode

> *Required for all tiers. Every ADR must specify what this capability produces when it appears to be functioning but the underlying data, propagation channel, or computation is absent or broken. This is the DEMO4-001 class of failure.*  
> *Authority: DIC Roadmap Section C, C-1.*

[What does this capability show when it appears correct but the underlying [data source / event channel / computation / database connection] is absent or disconnected? Examples: "Shows placeholder value 0 rather than no-data indicator," "Shows stale step data without indicating staleness," "Emits no events without surfacing an error — appears to advance but produces no downstream output." Name the detection mechanism: how would a QA reviewer identify this failure mode?]

---

## Asymmetry Assessment

> *Required for analytical capability ADRs (Tier 1 and Tier 2 ADRs that introduce new measurement, computation, or scenario analysis capabilities). Not required for display-only or infrastructure ADRs.*  
> *Authority: DIC Roadmap guardrail INV-1.*

[One paragraph: "Well-resourced actors with [Bloomberg / sovereign wealth fund models / IMF proprietary tools / creditor syndicate analytics] can currently [describe the capability]. WorldSim's proposed ADR-N [closes / partially closes / does not address] this gap by [description]. The remaining gap after this ADR is [description]." If no comparable capability exists in sophisticated actor tooling, document that explicitly — this is an acceptable finding.]

---

## North Star Test

> *Required for Tier 1 ADRs. Encouraged for Tier 2 (not a blocking gate for Tier 2 acceptance, but absence should be explained). Authority: DIC Roadmap Section C, C-3; CLAUDE.md §North Star Test (Process Gate).*

[One paragraph answering: "Does this decision make the tool more useful to a finance minister sitting across from an IMF negotiating team, in that moment?" Name a specific scenario. Name what the minister or her specialist can now do. Name whether this closes an asymmetry gap.]

---

## Mission Impact Statement

> *Required for all ADRs requiring panel review (Tier 1 and Tier 2).*  
> *Authority: DIC Roadmap guardrail INV-5.*

[One paragraph: "This ADR closes [capability gap], ranked as [priority N] in the asymmetry-closing impact list (`docs/process/design/process-redesign-phase0-dic-roadmap.md §Section B`). The direct impact on the finance ministry side of a sovereign debt negotiation is [statement]. Technical completeness without this mission relevance assessment is insufficient for acceptance."]

---

## Minimum Data Tier

> *Required for Tier 1 and Tier 2 analytical capability ADRs.*  
> *Authority: DIC Roadmap guardrail INV-3.*

[Minimum data tier at which this capability produces actionable output: Tier [N]. For users in Tier 3–4 environments, the synthetic data inference pathway is [defined: describe it / undefined: acknowledge as accessibility gap]. If undefined: "This is a capability accessibility gap — the target user population operates in a Tier 3–4 data environment. This must be addressed before this capability is considered mission-complete for those users."]

---

## Alternatives Considered

### Alternative 1: [Name]

[Description. Why it was rejected. What it would have cost or risked. An ADR that considers only one option has not established that the decision is sound.]

### Alternative 2: [Name]

[...]

---

## Consequences

### Positive

[What does this decision enable or improve? Reference specific journey steps, persona needs, or capability gaps closed.]

### Negative

[What does this decision constrain or cost? What technical debt does it create? Be honest. An ADR that lists no negative consequences has not been completed honestly. Reference any known limitations in generational horizon coverage (IA-3), capability accessibility at low data tiers (INV-3), or cohort disaggregation gaps (DE-5) that this ADR does not address.]

### Known Limitations

[Any model limitation, variable not captured, or domain where this capability's fidelity is known to be weak. These must be documented and made visible to users. Reference `docs/ux/personas.md` cases that this limitation affects.]

---

## Diagram

[Reference to the Mermaid diagram in `docs/architecture/`. Example: `docs/architecture/ADR-NNN-component-diagram.mmd`. Every ADR gets at least one diagram per CODING_STANDARDS.md §Diagram Standards.]

---

## Backtesting Validation Anchor

> *Required for ADRs introducing a new composite score, composite indicator, or novel measurement methodology. See CODING_STANDARDS.md §Backtesting Validation Anchor.*

[Historical case(s) this capability must be validated against before the milestone closes. Format: "This capability must be validated against [case name, year] — the simulation should produce [expected output] when applied to that case's known trajectory. A failure to match indicates model miscalibration, not an edge case."]

---

*Template version: 2026-06-09. Phase 0 encoded. For questions about tier classification, see `docs/process/design/process-redesign-phase0-ux-traceability-spec.md`. For persona conflict resolution, see `docs/ux/personas.md §Persona Conflict Resolution`.*
