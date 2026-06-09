---
name: process-redesign-phase0-ux-traceability-spec
type: phase-0-working-document
phase: Phase 0 — UX/Persona Traceability Upstream of ADR Development
step: Step 2 — UX Designer
status: COMPLETE — Step 2 output filed. Prerequisite for Step 3 (Business PO).
authored-by: UX Designer
date: 2026-06-09
sprint-entry: docs/process/sprint-plans/process-redesign-phase0-sprint-entry.md
prerequisite-input: docs/process/design/process-redesign-phase0-dic-roadmap.md
feeds-into: Step 3 (Business PO), Step 4 (Architect — encodes into ADR template)
canonical-destination: New §Persona and UX Traceability section in ADR template (Architect determines placement in Step 4)
---

# Phase 0 — UX Designer: UX Traceability Specification

**Authored by:** UX Designer  
**Date:** 2026-06-09  
**Phase:** Phase 0 — UX/Persona Traceability Upstream of ADR Development  
**Sprint entry:** `docs/process/sprint-plans/process-redesign-phase0-sprint-entry.md`  
**Status:** COMPLETE — Step 2 output filed. Prerequisite for Step 3 (Business PO) and Step 4 (Architect).

---

## Activation Record

UX Designer activated for Step 2 of Phase 0. This specification derives UX traceability requirements grounded in the DIC guardrails produced in Step 1. It does not derive requirements independently — the guardrails are the upstream authority.

**Mandatory reading confirmed before producing output:**
- `docs/ux/north-star.md` — read in full (canonical user, primary cognitive tasks by mode, three-mode structure)
- `docs/ux/user-journeys.md` — read in full (Journeys A through H, journey dependency map)
- `docs/ux/information-hierarchy.md` — read in full (three disclosure zones, M8/M9 hierarchy decisions)
- `docs/process/design/process-redesign-phase0-dic-roadmap.md` — read in full (20 binding guardrails, 8-item gap list, Section C cross-cutting requirements)
- `docs/vision/worldsim-founding-document.md` — read in full (per sprint entry invariant 3)
- `docs/process/sprint-plans/process-redesign-phase0-sprint-entry.md` — read in full

**XD-1 tension handling:** The founding document / UX north star persona conflict (Persona 5 minister vs. Persona 2 specialist as primary user) is *held open* in this document. Where the two personas produce different UX implications, both are named. Resolution is Step 3 (Business PO) responsibility. This document must not pre-empt that resolution by defaulting to either persona.

---

## What This Specification Covers

This specification answers three questions that the Architect will encode into the ADR template:

1. **Which ADR types require UX Designer on the authorship panel?**
2. **What must a UX implication statement contain?**
3. **What constitutes adequate UX review?**

It also produces:
- A set of hard UX invariants (derived from DIC guardrails) that override information hierarchy decisions
- A resolution to Tension 1 (cognitive load vs. methodological completeness), which the DIC Roadmap identified as the UX Designer's specific obligation
- A set of XD-1 observations (minister vs. specialist persona divergences at the UX level) for the Business PO's conflict resolution ruling in Step 3

---

## Part I — ADR Type Classification: Which ADRs Require UX Designer Panel Membership

Three tiers. Tier assignment is made at ADR initiation, before the panel is assembled. Misassignment is a process violation equivalent to the authorship gap that produced ADR-012's missing HCL acceptance criterion.

---

### Tier 1 — UX Designer on authorship panel (required)

These ADR types require the UX Designer as a named panel member who reviews the draft, proposes or approves the UX implication statement, and holds sign-off before the ADR moves to acceptance vote.

An ADR belongs in Tier 1 if it satisfies **any** of the following conditions:

| Condition | Examples | Rationale |
|---|---|---|
| Introduces a new surface in Zone 1 (primary viewport, no interaction required) | New Zone 1 instrument, new persistent header element, new primary viewport layout division | Zone 1 is the canonical user's primary scan surface in all three modes; changes require UX authority sign-off |
| Modifies zone assignment of an existing element (moves from Zone 2 to Zone 1, or Zone 1 to Zone 2, or any zone demotion/promotion) | Moving MDA alert panel, trajectory view, radar chart to a different disclosure zone | Zone assignment encodes cognitive task priority; reassignment without UX authority is a hierarchy violation |
| Introduces a new visual treatment for severity, uncertainty, or confidence tier at any zone | New badge style for confidence tiers, new color system for alert severity, new disclosure pattern for Tier 3 data | Visual treatment for epistemic state is a UX architectural decision, not an implementation detail |
| Modifies MDA alert panel placement, visible count, scroll behavior, or severity display | Changing alert ordering, changing TERMINAL vs. CRITICAL visual distinction, introducing filtered alert views | IA-1 and IA-4 guardrails require UX authority on all alert panel modifications — TERMINAL severity is irreversibility signal, not a styling choice |
| Introduces or removes a Mode (Mode 1, 2, 3 or future modes) | Mode 3 introduction, Mode 4 architectural specification | Mode boundaries define the primary cognitive task served; each mode has a primary task that all instrument layout serves |
| Introduces or modifies an entry state (Investigative, Reactive, Preparatory, Demonstrative, Evaluative, Retrospective) | New entry state for Phase 3 accountability monitoring, modification to Reactive vs. Preparatory state boundary detection | Entry states determine the time constraint regime under which a capability must be operable (DE-4 guardrail) |
| Introduces a new interaction pattern as the primary access path for a user-facing capability | New drawer type, new modal, new scroll-required access path for a Zone 1 instrument | Information hierarchy governs — a new interaction pattern may demote an instrument without a zone change on paper |
| Modifies the control plane zone in Mode 3 | Changes to policy instruments form, scenario shocks form, control plane zone sizing | Control plane zone is reserved per Governing Premise 5; modifications require UX authority verification that trajectory view primacy is maintained |
| Introduces a new display pathway for human cost ledger indicators | New HCL output format, new composite display for human development framework | DE-1 guardrail supersedes information hierarchy; HCL parity is a per-ADR obligation that must be certified by UX authority |

**Tier 1 is not waiveable by the Architect.** An Architect determination that a Tier 1 ADR does not need UX Designer panel membership requires Engineering Lead exception and must be documented in the ADR.

---

### Tier 2 — Persona trace required; UX Designer review of trace (not full panel membership)

These ADR types introduce capabilities that reach user-facing output through existing display surfaces — the display surface itself is unchanged; the content it shows is new. The UX Designer does not hold authorship authority on the ADR, but reviews and signs off on the persona trace before the ADR moves to acceptance vote.

An ADR belongs in Tier 2 if it satisfies **any** of the following conditions:

| Condition | Examples | Rationale |
|---|---|---|
| Introduces a new indicator, composite score, or capability that will be shown in an existing Zone 1 or Zone 2 surface | New fiscal multiplier sensitivity output displayed in existing FrameworkPanel, new cohort disaggregation data in existing alert row | The surface is unchanged; the content is new. Persona trace must specify which journey step this serves, in which entry state, at which time ceiling. UX Designer verifies the trace is complete before acceptance. |
| Introduces or modifies a schema field whose value appears in a user-facing surface | Column rename that changes an indicator display name, new JSONB field that appears in a Zone 2 table | Display name is a UX concern even when it is encoded as data; a field rename without UX review can silently change what the canonical user reads |
| Extends an existing analytical module with new outputs visible to the user | ExternalSectorModule new reserve drawdown indicator, MacroeconomicModule new multiplier sensitivity map | Mission-relevant content additions require persona trace review to verify entry state coverage and cohort naming |
| Introduces backtesting or historical data fixtures that serve a specific user journey | Historical fixture for Persona 3 (political advisor) comparable-case analysis | Journey dependency map must be updated; UX Designer verifies fixture serves the named journey step |

**Tier 2 review deliverable:** A named UX Designer sign-off in the ADR's review section confirming that the persona trace (a) names entry state and time ceiling, (b) names the income cohort served (where applicable), and (c) names the user journey step addressed. This sign-off is a precondition for the ADR acceptance vote.

---

### Tier 3 — Indirect connection waiver; UX Designer notified but no review required

These ADR types have no direct or first-order UX connection. The UX Designer is notified when the ADR is accepted — not because review is required, but because the forward trace obligation must be tracked.

An ADR belongs in Tier 3 if it satisfies **all** of the following conditions:

1. The ADR's primary subject is infrastructure, computation, or data architecture with no direct user-facing output (examples: computation engine internal algorithms, database schema changes with no user-facing field mapping, event propagation internal wiring)
2. The connection to a user-facing capability is ≥2 levels of indirection (the ADR enables an engine, which enables a capability, which enables a display — not the ADR enables a display)
3. The Architect documents in the ADR: (a) the downstream capability this infrastructure will eventually enable, and (b) the Tier 1 or Tier 2 ADR that will handle display implications when that capability is built

**Tier 3 waiver is granted by the Architect with UX Designer notification, not with UX Designer approval.** If the UX Designer identifies that a claimed Tier 3 ADR has a first-order UX implication that the Architect missed, the UX Designer may escalate to the Engineering Lead. The Architect's initial classification is not final if UX Designer flags a misclassification.

**IA-5 signal latency note:** Even Tier 3 infrastructure ADRs must include a "signal latency impact" statement covering TERMINAL alert update latency (IA-5 guardrail). This is the one guardrail that applies regardless of tier. The UX Designer is not in the authorship panel for Tier 3 ADRs, but the latency impact statement is an architectural requirement that the Architect must satisfy.

---

## Part II — UX Implication Statement: Required Contents

A UX implication statement is a section in the ADR that the UX Designer either authors (Tier 1) or reviews and approves (Tier 2). It is not an optional summary — it is a named acceptance gate. An ADR whose UX implication statement is incomplete or absent cannot receive a "ACCEPTED" status.

### Required contents for Tier 1 UX implication statements

A complete Tier 1 UX implication statement contains all seven of the following elements:

---

**Element 1 — Zone assignment and hierarchy certification**

States:
- Which zone(s) are affected by this ADR (Zone 1, Zone 2, Zone 3, or new element)
- Whether any existing element changes zone assignment as a result of this ADR
- Whether the proposed zone assignment is consistent with `information-hierarchy.md` as of the ADR authorship date; if not, identifies the conflict and documents the resolution authority

*Format:* "This ADR places [element] in Zone [N]. [Previous zone if reassigned.] This assignment is consistent with `information-hierarchy.md` §[section] / This assignment conflicts with `information-hierarchy.md` §[section] because [reason]; resolution: [ruling or EL exception reference]."

---

**Element 2 — Primary cognitive task alignment**

States which mode's primary cognitive task this ADR serves:
- Mode 1: trajectory reconstruction and historical pattern recognition
- Mode 2: threshold-safe path construction
- Mode 3: real-time steering within human cost constraints
- Multi-mode (names each mode and how the capability serves each mode's task differently)

*Format:* "This capability primarily serves Mode [N]'s primary cognitive task ([task name]). In Mode [M], it [serves/does not serve] the primary cognitive task because [reason]."

---

**Element 3 — Entry state coverage**

Names each entry state in which the capability must be operable, and specifies the maximum time or interaction ceiling for each (per DE-4 guardrail). Uses the canonical entry state taxonomy from `personas.md`: Investigative, Reactive, Preparatory, Demonstrative, Evaluative, Retrospective.

Required for every entry state explicitly served by the capability:

*Format:* "In [entry state] (Persona [N], Journey [X] Step [Y]): user can reach [specific output] in [maximum time / interaction count]. Acceptance criterion: [specific, falsifiable statement verifiable by observation in the live application, not CI]."

The time ceiling values are not invented by this specification — they come from the user journeys:
- Reactive entry state (Journey B): primary scan must complete in under 90 seconds; Step 1 (locate scenario) must complete under 10 seconds; Step 3 (read top MDA alert) must complete in under 30 seconds from drawer open
- Demonstrative entry state (Journey D): cold-reader orientation must be completable in 60 seconds with one explanatory sentence per instrument
- Mode 3 control input propagation (Journey C): control input → instrument cluster update in under 10 seconds; mode switch in under 3 seconds

Any entry state not explicitly named in Element 3 is treated as not served. If the capability is claimed to serve a persona in an entry state but no time ceiling is specified, the UX implication statement is incomplete.

---

**Element 4 — Human cost ledger parity certification (DE-1 guardrail)**

States explicitly whether this ADR maintains human cost ledger equal visual weight to financial indicators in the primary viewport. This element is required for **all** Tier 1 ADRs that touch Zone 1 layout, instrument weighting, trajectory display, or information hierarchy.

Two valid states:
- "This ADR does not affect HCL visual weight relative to financial indicators. HCL parity is maintained."
- "This ADR affects [specific aspect of HCL display]. The effect is [description]. Engineering Lead exception required: [reference to exception record]."

There is no third state. "HCL is unaffected by implication" is not a valid statement — the UX Designer must actively verify, not assume.

---

**Element 5 — Uncertainty display specification (CM-1 guardrail)**

Required for all Tier 1 ADRs introducing a new display surface or modifying an existing display surface's content.

Must name:
- What confidence tier information is displayed (tier badge, tier label, full tier name, or tier number)
- Where it appears relative to the indicator value (adjacent, parenthetical, tooltip, dedicated row)
- What it shows specifically for Tier 3 data (synthetic comparable) — the word "synthetic" must appear in the specification of what Tier 3 shows; "Tier 3" alone is not sufficient
- What it shows for Tier 4 data (structural extrapolation) — must be visually distinct from Tier 3
- What the Structural Absence Declaration shows when uncertainty is too large to be directionally informative (CM-5 guardrail — see Part IV below)

*Note:* "Per the standard" is not a specification. The standard is a reference. The ADR must specify the format for this capability's output specifically.

---

**Element 6 — Irreversibility signal integrity certification (IA-1, IA-4 guardrails)**

Required for all Tier 1 ADRs that touch Zone 1 display, alert panel, or severity display.

Must certify:
- Whether this ADR affects TERMINAL alert visual treatment
- Whether TERMINAL remains visually distinct from CRITICAL with no implementation discretion (IA-1)
- Whether TERMINAL and CRITICAL alerts remain visible without scroll at minimum supported viewport (1280×800 desktop, 1024×768 tablet) under a representative high-alert-count scenario (IA-4)

The acceptance criterion for this element must be CI-testable and application-observable: "Under scenario [X] producing [N] active alerts at severities [Y], all TERMINAL and CRITICAL alerts are visible without scroll at viewport [dimensions]. This criterion is verified by [specific test or observation protocol]."

---

**Element 7 — User journey coverage**

Names the specific user journeys and steps from `user-journeys.md` that this ADR serves or modifies, using the canonical notation (Journey A Step 3b, Journey B Step 3, etc.).

For each named journey-step:
- What the user can now do that they could not do before (or what was impeded and is now resolved)
- Whether the journey-step's information need (as documented in `user-journeys.md`) is now satisfied by this ADR

Journey steps marked as `[Near-Term-Gap]` or `[Phase-3-TBD]` in `user-journeys.md` are candidates for this element when an ADR proposes to close them.

---

### Required contents for Tier 2 UX implication statements (persona trace review)

A Tier 2 ADR does not require a full UX implication statement. The UX Designer reviews and signs off on the persona trace section already in the ADR. The review confirms presence of:

1. Entry state named (DE-4)
2. Time or interaction ceiling for the named entry state (DE-4)
3. Income cohort named, where the capability affects distributional outputs (DE-2) — see Part III for the valid cohort list
4. Negotiating leverage statement for any trace to Persona 2 (INV-4): "After accessing this capability, Persona 2 can make the following specific argument: [statement]"
5. Uncertainty behavior for Tier 3 data in the named entry state (CM-3)

The UX Designer's sign-off text in the ADR: "UX Designer review complete. Persona trace elements [1–5] confirmed present and adequate. [Date. UX Designer.]"

If any of the five elements is absent or inadequate, the UX Designer's sign-off reads: "UX Designer review: persona trace incomplete. Missing: [element(s)]. ADR blocked from acceptance until remediated."

---

## Part III — Adequate UX Review: Definition

Adequate UX review is not synonymous with UX Designer approval. It is defined per tier:

**Tier 1:** Adequate review means the UX Designer has:
1. Read the full ADR draft
2. Authored or co-authored the seven-element UX implication statement
3. Confirmed all seven elements are complete
4. Signed off with date before the ADR moves to acceptance vote

A Tier 1 ADR that reaches acceptance vote without UX Designer sign-off is in violation of the process. The PI Agent holds R for blocking the vote if sign-off is absent.

**Tier 2:** Adequate review means the UX Designer has:
1. Read the persona trace section of the ADR
2. Confirmed the five review elements are present
3. Signed off with a named confirmation or a specific remediation request

**Tier 3:** Adequate review means the UX Designer has received notification that the ADR was accepted, and the forward trace obligation (identifying the Tier 1 or Tier 2 ADR that will handle display implications) has been recorded. No sign-off is required for Tier 3 acceptance.

**Review timing rule:** UX Designer sign-off is a prerequisite for ADR acceptance, not a post-acceptance formality. An ADR submitted for acceptance vote without completing the applicable review tier is automatically blocked. This is the process gate mechanism that would have prevented ADR-012 from being accepted without specifying HCL Zone 1D visibility as an acceptance criterion.

---

## Part IV — Hard UX Invariants

These constraints are derived directly from DIC guardrails and override any information hierarchy decision in `information-hierarchy.md`. They cannot be resolved by UX Designer authority alone — they require Engineering Lead exception if any ruling would violate them.

**Invariant UX-H1: HCL equal visual weight in Zone 1 is non-negotiable without EL exception**

Source: DE-1 guardrail  
Statement: In the primary viewport, without navigation, the human development trajectory must occupy equal visual real estate to the financial trajectory. Any ADR that would change this balance — for any mode, any entry state, any display configuration — requires an Engineering Lead exception with documented rationale. The UX Designer cannot grant this exception. "Temporary," "mode-specific," or "conditionally demoted" formulations do not reduce the exception requirement.  
Detection: Any Tier 1 UX implication statement that produces a "this ADR affects HCL visual weight" response in Element 4 triggers the exception requirement automatically.

**Invariant UX-H2: TERMINAL alert severity is irreversibility signal, not styling preference**

Source: IA-1 guardrail  
Statement: TERMINAL alerts must be visually distinguishable from CRITICAL alerts at all supported viewports with no implementation discretion. "Visually distinguishable" means: a user with no prior tool knowledge, looking at the alert panel, cannot confuse a TERMINAL alert for a CRITICAL alert or vice versa. The distinction must be encoded as a named acceptance criterion with a CI-testable expression, not as an instruction to the implementer.  
Detection: Any Tier 1 ADR touching the alert panel that does not include Element 6 with a CI-testable TERMINAL distinction criterion is incomplete.

**Invariant UX-H3: TERMINAL and CRITICAL alerts visible without scroll at minimum viewport**

Source: IA-4 guardrail  
Statement: Under any scenario state with ≥1 TERMINAL or CRITICAL alert, all such alerts must be visible at viewport 1280×800 (desktop) and 1024×768 (tablet) without scroll. No scroll-to-reveal is acceptable for TERMINAL or CRITICAL severity. This is not a soft constraint — it is a threshold-crossing that produces the "have not read the TERMINAL alert" failure mode in Reactive state.  
Detection: Any Tier 1 ADR modifying alert count, panel height, scroll behavior, or visible row count must include a scenario-specific CI test verifying this invariant.

**Invariant UX-H4: Zone 1 primary cognitive task servability is mode-invariant**

Source: information-hierarchy.md §Governing Principle  
Statement: Zone 1 must always enable the user to complete the primary cognitive task of the active mode without navigating away from the primary viewport. For Mode 1: "has any threshold been crossed?" For Mode 2: "at which step does the proposed path cross a threshold?" For Mode 3: "what does this control input do to the human cost threshold, in real time?" A Zone 1 configuration that forces navigation to answer any of these questions is a hierarchy violation regardless of layout convenience.  
Detection: Element 2 (cognitive task alignment) in Tier 1 UX implication statements verifies this invariant per ADR.

**These four invariants are listed in priority order.** If an ADR creates a conflict between UX-H1 and UX-H3, UX-H1 governs. If it creates a conflict between UX-H3 and UX-H4, UX-H3 governs (an alert that cannot be seen is a failed irreversibility signal, which is a mission violation). In all cases, the conflict must be surfaced in the ADR, not silently resolved.

---

## Part V — Tension 1 Resolution: Cognitive Load vs. Methodological Completeness

The DIC Roadmap (Part II, Tension 1) identified this as the UX Designer's specific obligation to resolve. The Chief Methodologist's CM-2 requirement (uncertainty disclosure in Persona 5's 5-minute window) and Persona 5's preference for "three formats and no others: traffic light, one-sentence finding, single annotated chart" are in genuine tension. This section is the UX Designer's ruling.

### The tension stated precisely

Persona 5 (Aicha Mbaye, IMF Executive Board Member) fails her use case when the first screen requires explanation before she can read it. Her format preference is maximally compressed — a traffic light reading plus one citable sentence plus one chart. The Chief Methodologist requires that uncertainty tier be visible in that same 5-minute window, because a finding Persona 5 cites as authoritative that is later shown to be Tier 3 will destroy the tool's credibility in exactly the institutional context where it most needs to build it.

The tension is real. Resolving it by choosing one side produces either epistemic dishonesty (Persona 5 cites findings without tier disclosure) or unusability (Persona 5's window is too narrow for a full uncertainty display).

### Ruling

**The resolution is a parenthetical tier indicator within the one-sentence finding format.** The format is:

> "[Finding in plain language] [(Tier N — label)]"

Examples:
- "Financial system is under HIGH stress (Tier 2 — World Bank WDI)"
- "Poverty headcount crosses CRITICAL threshold in year 3 (Tier 3 — synthetic comparable)"
- "Healthcare capacity shows WARNING-level deterioration (Tier 1 — IMF Article IV)"

**Two requirements this ruling generates:**

1. The parenthetical must appear inline with the finding, not in a footnote, tooltip, or Zone 3 disclosure. The purpose of disclosure is that the user reads it; a disclosure that requires interaction is not a disclosure for Persona 5 in the Demonstrative entry state.

2. For Tier 3 data, the label must use the word "synthetic" verbatim — not "estimated," not "projected," not "modeled." "Synthetic comparable" communicates that the data was inferred from similar economies, not measured in this economy. "Tier 3" alone does not communicate this to a cold reader. Persona 5 in a 5-minute orientation does not know the tier system; she does know the difference between measured and inferred.

**Scope of this ruling:**
This ruling governs the one-sentence finding format displayed in Demonstrative and Evaluative entry states. It does not govern the full FrameworkPanel indicator display or Zone 2 analysis surfaces — those have their own display conventions. This ruling answers: "when the one-sentence summary is all the user sees, what does uncertainty disclosure look like?"

**What this ruling does not resolve:**
The ruling specifies format, not placement. Element 5 of the UX implication statement requires ADRs to specify where the parenthetical appears relative to the indicator value. "Parenthetical in the one-sentence finding" is the pattern; the specific rendering implementation is the ADR's responsibility.

**XD-1 note for Step 3:** Persona 5's 5-minute window and Persona 2's 90-second window have different display requirements for the same disclosure. Persona 2 in Reactive state reads the tier indicator as "can I cite this finding?" — she needs the tier number and the label. Persona 5 in Demonstrative state reads the tier indicator as "should I trust this signal?" — she needs the word "synthetic" if the data is inferred, and nothing special if it is measured. The format above serves both: the tier number serves Persona 2's citation need; the label serves Persona 5's trust calibration. This is a convergence that Step 3 can rely on — the ruling does not require persona conflict resolution to resolve Tension 1.

---

## Part VI — XD-1 Observations for Step 3

The XD-1 gap is the founding document / UX north star persona conflict: the founding document's north star figure is a finance minister (Persona 5), while the UX north star's canonical user is a debt restructuring specialist (Persona 2). This section records where these two personas produce different UX implications, to inform the Business PO's conflict resolution ruling in Step 3.

**This section does not resolve the conflict.** It maps the landscape the Business PO must rule on.

---

### Divergence Point 1 — Alert panel information density

| Dimension | Persona 2 (Specialist) | Persona 5 (Minister) |
|---|---|---|
| Primary use | Citation — "poverty headcount crosses CRITICAL at step 2 for bottom quintile" | Signal — "this trajectory is dangerous" |
| Ideal alert specificity | Indicator, step, cohort, confidence tier, causal attribution | Severity, direction, what to do |
| Tolerated cognitive load | HIGH — she needs all four fields to make the argument | LOW — she has 5 minutes; a full indicator row may be too much to absorb |
| Consequence of under-specification | Cannot make the argument; loses the negotiation point | May act on a finding she cannot explain |
| Consequence of over-specification | None — she reads what she needs | May disengage from the tool in the Demonstrative entry state |

**UX implication for ADRs touching alert panel:** ADRs that modify alert row content face a structural choice between Persona 2's citation completeness and Persona 5's cognitive economy. Without the Business PO's conflict resolution ruling, this ADR faces the same hidden assumption that produced DEMO4-005 — whichever persona the implementer pictures governs implicitly.

---

### Divergence Point 2 — Preparation time assumptions

| Dimension | Persona 2 (Specialist) | Persona 5 (Minister) |
|---|---|---|
| Primary journey | Journey A (Preparation, 20-40 minutes) → Journey B (Negotiation, 90 seconds) | Journey D (Demonstrative, 60 seconds as observer) |
| First exposure to output | Prepared — she built the scenario | Cold — she is reading an instrument cluster for the first time |
| Path to insight | Navigate to drawer → read framework panel → extract alert with step and cohort | Observe Zone 1 → read one alert row → orient |
| Design implication | Zone 2 surfaces must be rich; Journey B depends on Journey A's preparation | Journey D's cold-reader orientation requirement imposes a self-describing Zone 1 constraint |

**UX implication for ADRs introducing Zone 1 capabilities:** Zone 1 elements must satisfy both the prepared Persona 2 reading for precision and the cold-observer Persona 5 reading for orientation. These are not mutually exclusive — they impose different labeling requirements. An element that is precise but requires prior tool knowledge to parse fails Persona 5. An element that is self-describing but loses precision fails Persona 2. ADRs must specify how their Zone 1 element satisfies both; they cannot assume one persona's reading.

---

### Divergence Point 3 — Progressive disclosure tolerance

| Dimension | Persona 2 (Specialist) | Persona 5 (Minister) |
|---|---|---|
| Will she use Zone 2? | Yes — cohort breakdown, confidence tier, trajectory values are all essential | Unlikely in Demonstrative state — she observes what the driver shows |
| Will she use Zone 3? | Sometimes — methodology notes for citation (Journey F Step 5 / H Step 1) | No |
| Disclosure patience | HIGH — she will spend 40 minutes in preparation | LOW — she has 5 minutes |

**UX implication for ADRs introducing methodology disclosures:** Zone 3 placement for methodology disclosures (M8 Decision, `information-hierarchy.md` §M8 Hierarchy Decisions) serves Persona 2's citation need and does not harm Persona 5's journey, because Persona 5 never reaches Zone 3. This is a point of convergence, not divergence — Zone 3 methodology disclosure is the correct tier for both personas.

---

### Divergence Point 4 — Mode 3 access

| Dimension | Persona 2 (Specialist) | Persona 5 (Minister) |
|---|---|---|
| Mode 3 use? | Yes — Journey B Step 5 (real-time control), Journey C (primary Mode 3 journey) | No — Persona 5 observes; she does not drive the simulation |
| Control plane legibility | Must be operable in under 60 seconds for first control input | Not applicable |

**UX implication for ADRs touching Mode 3 / control plane:** Mode 3 and control plane ADRs are Persona 2-primary. Persona 5 has no Mode 3 journey. ADRs in this space should trace to Persona 2 without conflict — the XD-1 tension does not apply to Mode 3 capabilities.

---

### Summary for Step 3

The Business PO's conflict resolution ruling (Output 2, gap XD-1) must address Divergence Points 1 and 2 directly — these are where the two personas impose different requirements on the same ADR's design decisions. Divergence Point 3 is a resolved convergence. Divergence Point 4 is persona-separated (Mode 3 is Persona 2 territory).

The ruling the Business PO must produce: when an ADR touches alert panel content or Zone 1 display, and Persona 2's citation specificity conflicts with Persona 5's cognitive economy, which persona's requirement governs? The DIC guardrails constrain the ruling space (DE-1 protects HCL parity regardless of persona priority; IA-4 protects alert visibility regardless), but within those constraints, the Business PO must establish a stated hierarchy.

---

## Part VII — Journey Dependency Obligations

When an ADR's UX implication statement references a specific journey step from `user-journeys.md`, the following obligations are triggered:

1. **Journey dependency map must be updated** if the ADR modifies a step's information need, time constraint, or decision point. The update belongs in the same PR as the ADR.

2. **`[Near-Term-Gap]` or `[Phase-3-TBD]` journey steps** that an ADR proposes to close must have their status updated in `user-journeys.md` when the ADR is accepted — not when the implementation is merged, but when the ADR decision is made. The ADR is the architectural commitment; the journey document records that the gap is now being addressed.

3. **New journey steps** introduced by an ADR (a new capability that creates a new step in an existing journey, or a new journey for a capability not yet represented) must be drafted by the UX Designer in the same cycle as the ADR's UX implication statement — not as a post-implementation update. A journey step that is written after implementation has effectively been written around the implementation's constraints rather than the user's needs.

---

## Part VIII — Application to the Validation Question

The Phase 0 sprint entry's validation question asks: "If ADR-012 (ExternalSectorModule) had been required to carry the Phase 0 traceability requirements, would DEMO4-005 (HCL indicator computed but invisible in Zone 1D) have been caught before PR #773 was merged?"

From the UX Designer's perspective, the answer is yes, via two specific elements of this specification:

**Element 4 (HCL parity certification) would have required the following statement in ADR-012's UX implication statement:**  
"This ADR affects Zone 1 display — specifically Zone 1D (Four-Framework Current Position). This ADR does not affect HCL visual weight relative to financial indicators. HCL parity is maintained."

If the authoring panel could not truthfully write the second sentence — because the human development indicator was computed but not wired to Zone 1D — the false statement would have surfaced the gap before the ADR was accepted, not after PR #773 merged.

**Element 3 (Entry state coverage) would have required an acceptance criterion of the form:**  
"In Reactive entry state (Persona 2, Journey B Step 3): user can read the human development composite score in Zone 1D without navigation in under 5 seconds. Acceptance criterion: Human development composite score is visible in Zone 1D when ExternalSectorModule is active, with value derived from the module's output."

A falsifiable acceptance criterion naming Zone 1D specifically would have failed in CI or application testing the moment the wiring was absent.

This confirms that Invariant UX-H1 and Element 4 are the specific additions that would have caught DEMO4-005. The PI Agent's review in Step 5 should verify that these two elements are stated with sufficient enforcement specificity (not merely present as guidelines) to satisfy the validation question.

---

## Handoff Notes for Step 3 — Business PO

Step 3 must engage directly with:

1. **Divergence Points 1 and 2** from Part VI — these are the specific UX-level manifestations of the XD-1 gap that require a priority hierarchy ruling. The Business PO cannot resolve XD-1 in the abstract; the ruling must be specific enough to determine which persona governs in a Tier 1 ADR touching alert panel content density.

2. **The three-entry-state complexity** (Reactive, Preparatory, Demonstrative) — the personas diverge most at the extremes (Reactive state Persona 2, Demonstrative state Persona 5). The resolution ruling should specify whether Reactive state requirements govern when they conflict with Demonstrative state requirements, or vice versa. The UX Designer's read: Reactive state is the harder constraint (90 seconds vs. 60 seconds, and the 90-second constraint is mission-critical in the negotiating room). But this is a view to inform the Business PO, not a ruling.

3. **INV-4 (negotiating leverage statement)** — the Business PO's persona traceability specification should incorporate the format the Investment Agent requires. The UX implication statement (Tier 2 review, Item 4) references this requirement; the Business PO gives it its canonical definition.

4. **DE-2 (income cohort naming)** — the Business PO must establish the valid cohort list as a formal persona traceability requirement. The Development Economist's list is: bottom two income quintiles; pensioners 65+; youth 18-35 tradable; children 0-5. The Business PO confirms whether this list is complete or requires amendment.

---

*Document complete. Filed as Step 2 output for Phase 0 — UX/Persona Traceability Upstream of ADR Development.*  
*Prerequisite for Step 3 (Business PO) and Step 4 (Architect).*
