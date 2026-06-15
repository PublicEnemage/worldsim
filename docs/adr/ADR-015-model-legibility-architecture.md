---
name: ADR-015-model-legibility-architecture
type: architecture-decision-record
version: Proposed
phase0-encoded: true
authored: 2026-06-15
---

# ADR-015: Model Legibility Architecture — Evidence Thread Architecture

## Tier Classification

**Tier:** 1

**Justification:** This ADR introduces modifications to multiple Zone 1 surfaces — Zone 1B (alert panel basis threads), Zone 1C (PMM interpretation anchor), Zone 1D (basis annotations on all four framework scores, addition of programme_survival_probability as fifth row) — and a new assumption surface positioned between the identity header (Zone 0) and the instrument cluster (Zone 1). Every change directly modifies the zero-interaction primary viewport reading experience for Persona 2 in the Reactive entry state.

**Sections required by tier:**

| Section | Tier 1 | Required here |
|---|---|---|
| Persona Trace (7-element) | Required | Yes |
| UX Implication Statement (7-element) | Required — UX Designer sign-off | Yes |
| Forward Trace Statement | Not applicable | Not applicable |
| Silent Failure Mode | Required | Yes |
| Asymmetry Assessment | Required (analytical capability) | Yes |
| North Star Test | Required | Yes |
| Mission Impact Statement | Required | Yes |

---

## Status

`Proposed`

---

## Validity Context

**Standards Version:** 2026-06-15 (CLAUDE.md revision date; CODING_STANDARDS.md current at this date)  
**Valid Until:** M15 kickoff, or any PR that modifies Zone 1D row structure, the assumption surface, or the cross-examination mode  
**License Status:** `PROPOSED` — awaiting EL resolution of 6 pre-implementation decisions (listed in §Decisions Required)

**Panel:**
- Architect Agent (R — author)
- UX Designer Agent (R — sign-off, required precondition for acceptance vote)
- Frontend Architect Agent (C — implementation scope review)
- Chief Methodologist (C — PMM interpretation anchor, confidence tier display specification, ia1_disclosure placement)
- Development Economist (C — Human Cost Ledger and income cohort visibility)
- Business PO (C — north star test authorship, validate step)
- Engineering Lead (A — accountable; resolves 6 pre-implementation decisions before acceptance)

**Renewal Triggers:**
- Any change to Zone 1D row structure that adds or removes a framework row
- Any change to the confidence tier system or tier display labels (DATA_STANDARDS.md revision)
- Any M15 capability that modifies how the cross-examination mode behaves
- Introduction of the Mode 3 control plane that displaces the assumption surface position

---

## Date

2026-06-15

---

## Context

### Background

WorldSim's primary mission is to give a finance minister the same quality of scenario analysis that sophisticated financial and institutional actors have — particularly in a negotiating room where she faces counterparties with vastly greater analytical staff. The instrument cluster (Zone 1) delivers trajectory signals, MDA alerts, PMM, and four-framework scores. Each of these outputs is computed by a model with calibrated (or pre-calibration) relationships, sourced from specific data tiers, and shaped by a set of model assumptions. None of this reasoning is co-visible with the output in the current UI.

The M14 live external demo (#843) is the first time WorldSim will be used in the presence of real external participants. These participants will challenge the outputs. The minister's analyst will need to answer from the screen. The current architecture does not support this.

**Evidence base:** Live UI audit conducted 2026-06-15, documented in full at `docs/demo/m14/reviews/2026-06-15-ux-legibility-audit-minister-exercise.md`. Screenshots taken of the live application at localhost:5173 with two scenarios: Jordan/Egypt 2024 Hormuz Demo 4 (completed, Mode 2, Fiscal ×1.3) and Greece 2010-2015 M8 Demo (completed, Mode 1). The audit table identifies 21 questions a first-time user would ask and classifies which can and cannot be answered from the screen alone. Twelve of the twenty-one questions cannot be answered.

**DIC consultations on record in the audit document:**
- Chief Methodologist: CHALLENGE — confidence tier conflates data quality and model calibration; PMM is undefendable without interpretation anchor; ia1_disclosure must be zone-zero
- Development Economist: CHALLENGE — Human Development composite is useless at the decision level; Human Cost Ledger is largely blank and "-0.25 T4" is unreadable; "Irreversible" label without timeframe/population/cause is alarming but not informative
- Political Economist: CHALLENGE — programme_survival_probability is not visible anywhere in Zone 1; the most mission-critical political economy output is invisible from the primary reading experience
- Geopolitical Analyst: CHALLENGE — every primary number must be reachable from challenge to evidence in two interactions; current architecture requires 6 steps; this fails under negotiating room time pressure
- Council Orchestrator: VALIDATE — current tool lets minister read it but not defend it; proposed framework passes north star test if L0 thread always visible, L1 reachable in one interaction, cross-examination single-action activatable, political economy in Zone 1

**Pre-existing structural gap:** The information hierarchy (Zone 1 → Zone 2 → Zone 3) organizes content by interaction depth — how many clicks. The Evidence Thread Architecture introduces a second axis: reasoning depth — how many causal steps from output to basis. These are orthogonal. Currently high visual primacy = shallow reasoning depth visible. The gap between "can be read" and "can be defended" is a structural consequence of optimizing only for the first axis.

### Problem Framing

Persona 2 (the finance ministry negotiator — Eleni/Aicha archetype) is in Journey B Step 3: Reactive entry state. The IMF analyst across the table says: "Your reserve coverage estimate is overstated — the fiscal multiplier assumption is weak for this context." Persona 2's specialist looks at the screen. She can see: "Financial 0.81" and a TERMINAL alert with "Current 2.000 / Floor 2.500." She cannot see: what data produced this, whether the underlying model relationship is calibrated, what the fiscal multiplier was, or where the methodology basis can be found. She has 90 seconds to respond. The current screen gives her no response material beyond "the number is there."

The specific mission failure: the asymmetry that WorldSim is designed to correct (sophisticated analytical staff on the creditor side, limited staff on the ministry side) is not corrected if the tool produces outputs the ministry team cannot defend. The outputs must be *traversable from challenge to basis* under the time constraints of the negotiating room. This traversal is currently unavailable.

---

## Decision

WorldSim will implement the Evidence Thread Architecture across Zone 1 surfaces, consisting of four components. All four are specified at decision level here; implementation specification is in the intent document authored at Step 1 of the agent execution lifecycle.

### Component 1 — Basis Threads on Zone 1 Primary Outputs (L0 / L1 / L2)

Every primary numeric output in Zone 1 carries a persistent, always-visible one-line annotation (L0) that answers: what produced this, and at what confidence? One interaction reveals the basis statement (L1). Existing Zone 3 documentation (entity drawer → framework panels → methodology notes) serves as L2 and is reachable from the L1 basis statement.

**Zone 1D — Four-Framework Current Position:**  
Each framework row displays a compact annotation beneath the score value. The annotation shows: data tier, indicator count, primary source, and pre-calibration status if applicable.

Current form: `Financial  0.81`  
L0 annotated form: `Financial  0.81 [T2 · 4 indicators · IMF/Central Bank 2024]`

For pre-calibration outputs: `[T3 · pre-cal]` — the abbreviation "pre-cal" is always shown when the scenario has ia1_disclosure = True and the output is from an uncalibrated model relationship.

**Zone 1C — PMM Widget:**  
The PMM requires a Chief Methodologist-authored interpretation anchor before L0 annotation can be specified (Decision 3 in §Decisions Required). Once that anchor is provided, the L0 annotation will include the neutral point, the constraint threshold, and whether the output is pre-calibration. Placeholder: `[T3 composite · pre-cal]`.

**Zone 1B — Compact Alert Rows:**  
Current compact rows truncate mid-indicator name ("Reserve Coverage ..."). The compact row format will be redesigned to display the full indicator name within the allocated column width, using a defined 24-character abbreviation set rather than mid-word truncation. This is not a layout change — it is a display specification for the text rendering within the existing compact slot.

**Human Cost Ledger strip:**  
Each ledger row will show the unit of the value and the tier meaning in parentheses. Current: `-0.25  T4`. Proposed: `-0.25 (capability index) [T4 · model estimate]`. "T4" expands to "model estimate" in all human-facing text; "Tier 4" expands to "early estimate — confirm before citing." The raw tier code must not appear without expansion.

### Component 2 — The Assumption Surface

A persistent one-line strip positioned between the ScenarioIdentityHeader (Zone 0) and the InstrumentCluster (Zone 1) that shows the model inputs most explanatory of the current trajectory shape. Visible whenever a scenario has been advanced beyond step 0. Content is computed from the scenario's sensitivity attribution (existing backend capability) and surfaces the 3–4 highest-sensitivity inputs in a comma-separated, human-readable form.

**Display format:**
`Fiscal ×1.30 · Political economy: enabled · Conditionality: standard · Data: 2024-Q1 vintage`

This is not a configuration widget. It is a read-only display. No click target. No popover on hover in the default state. The purpose is to answer "what assumptions shaped this?" with zero interaction.

**Conditional visibility:** If the scenario's political economy module is not enabled, "Political economy: enabled" is absent. If no fiscal multiplier override is present, the fiscal multiplier is absent (the default value is displayed only when it differs from the model's default). The strip width must accommodate its content without truncation at 1280px minimum viewport width.

### Component 3 — Programme Survival Probability in Zone 1D

When the political economy module is enabled for a scenario, `programme_survival_probability` appears as a fifth row in Zone 1D, labeled "Political Feasibility." This is the most mission-direct political economy output and must not require opening the entity drawer to access.

**Display format:**  
`Political Feasibility  [probability as percentage] [confidence tier]`

Example: `Political Feasibility  59% [T3 · political economy module]`

**Visibility rule:** Row appears only when political economy module is enabled (ADR-013). Row is suppressed entirely (not shown as a dash) when the module is not enabled, to avoid the "what is Political Feasibility?" question from users in scenarios where it is not computed.

**ADR-008 amendment required:** Adding a fifth row to Zone 1D changes the instrument cluster layout. This must be reviewed against ADR-008 (UX Architecture — instrument cluster layout) before implementation. The EL must confirm whether a formal ADR-008 amendment is required or whether this falls within the existing "expanding Zone 1D is permitted" clause. Decision 4 in §Decisions Required.

### Component 4 — Cross-Examination Mode

A single-action mode (keyboard shortcut `?` or persistent "Defend" button in the header, adjacent to the mode selector) that transforms the primary viewport to expose the evidence chain behind all Zone 1 primary outputs.

**When active, the mode:**
- Expands all Zone 1B alerts to full-detail form (indicator name, floor basis, source statement — inline, not in drawer)
- Expands all Zone 1D scores to show the 3–4 component indicators beneath each composite (inline expansion, not a navigation event)
- Shows the PMM interpretation anchor alongside the PMM value (Chief Methodologist-authored text defining what 0.5, 1.0, and 1.5 mean in policy language)
- Shows programme_survival_probability inline if political economy is enabled and it is not already visible (Component 3 makes it persistent; this mode confirms it in context)

**Design constraints:**
- Cross-examination mode does not change the layout architecture. It adds the L1 basis layer inline by expanding existing elements
- Mode must be toggleable. When toggled off, Zone 1 returns to its default compact form
- Mode must not be activatable in Mode 3 (real-time steering), where cognitive load of the primary read must be protected. The "Defend" button is suppressed or disabled when Mode 3 is active
- The toggle state must be visually unambiguous — a persistent indicator (e.g., header background tint or badge) is required so the user knows they are in cross-examination mode

### Pre-Implementation Decisions Required from EL

These decisions must be recorded as EL verdicts in this document before the ADR can move from Proposed to Accepted and before a sprint entry document can be filed.

**Decision 1 — Step counter bug.** The header shows "Step 0 / 8" when the scenario status is "Complete (8 steps)" and the trajectory chart shows all 8 steps. This is a prerequisite fix. The legibility work assumes the user can trust that the step counter reflects the step being read. If the step counter is wrong, every basis annotation (which step does this apply to?) is undermined. Scope: diagnose the ScenarioIdentityHeader / ScenarioStepStore interaction for completed scenarios loaded via URL param. Fix before any ADR-015 legibility work begins.

**Decision 2 — Ecological directionality convention.** The Ecological framework exhibits apparent directional inconsistency between scenarios (Greece Ecological = 1.11 → TERMINAL; Hormuz Ecological = 0.60 → TERMINAL via different breach mechanism). Before the Zone 1D Ecological basis annotation can be specified, the EL must commit to one of: (a) a single consistent directional convention with explicit directional annotation on every Ecological curve ("↑ = approaching breach"), or (b) a schema-level distinction between the composite score computation for "proximity above boundary" versus "proximity below boundary" scenarios. The annotation at L0 cannot be authored until the directionality is fixed.

**Decision 3 — PMM interpretation anchor (Chief Methodologist commitment).** The PMM Widget L0 annotation requires Chief Methodologist-authored text defining the neutral point, the constraint threshold, and the policy interpretation of the scale. This is a methodology commitment, not a frontend label. The Chief Methodologist must record the anchor text as a filed artifact before the PMM annotation can be implemented. If the PMM cannot be given an interpretation anchor because the model relationship is not sufficiently calibrated, the PMM must carry a pre-calibration disclosure that is more prominent than the current "↓ lower = more constrained."

**Decision 4 — Political Feasibility as Zone 1D fifth row (ADR-008 relationship).** Adding a fifth row to Zone 1D requires the EL to confirm the architectural path: ADR-008 amendment required, ADR-008 amendment not required (the change is within existing authority), or the row is placed in Zone 2 for M14 with Zone 1 placement deferred to a subsequent ADR.

**Decision 5 — Cross-examination surface scope for M14.** The live demo (#843) forces the question: which components of the Evidence Thread Architecture are required for a Demo 5 participant to be able to defend challenged outputs? The EL must scope M14: (a) all four components ship before Demo 5, (b) only Components 1 and 2 (basis threads and assumption surface) ship for M14 with cross-examination mode deferred, or (c) only the assumption surface (Component 2) ships for M14.

**Decision 6 — Landing orientation scope.** The bare landing state (world map + "Gdp Usd Millions (USD_millions_cur▼)") is a trust problem prior to model legibility. For Demo 5 with real external participants, this is a demo-critical risk. The EL must decide: (a) landing orientation is in M14 scope as a prerequisite for Demo 5, (b) landing orientation is deferred to M15 and Demo 5 participants are pre-briefed, or (c) the raw DB field name in the choropleth header is fixed as a separate bug (not an ADR-015 scope item) and landing orientation is deferred.

---

## Persona and UX Traceability

### Persona Trace

**P-1 — Persona identification:**  
Primary: Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou / Aicha Diallo archetype). The negotiator is in the room where sovereign decisions are made; she uses WorldSim to construct and defend an analytical position against a better-staffed counterpart. Secondary: Persona 1 — IMF Programme Analyst (Lucas Ferreira archetype), who uses the same interface to scrutinize the ministry's analysis for weaknesses. This ADR primarily serves Persona 2 but must not degrade Persona 1's read speed.

**P-2 — Entry state:**  
Reactive entry state (90-second total ceiling, negotiating room context). Persona 2 has a specific number challenged and needs to produce the basis for it before the negotiating momentum shifts. Secondary: Preparatory entry state (Persona 2, prior to the negotiating session — she uses cross-examination mode to pre-stress-test her outputs). Investigative entry state (Persona 1 — auditing the assumptions behind the ministry's scenario).

**P-3 — Journey reference:**  
Journey B Step 3 (Reactive state — scan: identify which alert is most critical and locate its basis). Closes Journey B Step 3 [Near-Term-Gap] — "defend challenged output in under 90 seconds." Extends Journey A Step 4 (Preparatory state — assumption review before the negotiating session). Opens Journey B Step 3a (new sub-step — activate cross-examination mode, read basis statement for challenged number, respond to counterparty).

**P-4 — Time or interaction ceiling:**  
Reactive entry state: basis annotation (L0) visible at zero interaction. Basis statement (L1) reachable in one interaction, total time under 30 seconds from the moment a number is challenged. Cross-examination mode activation: one action (keyboard shortcut or single button press). Full evidence chain (L2, existing Zone 3) reachable in two interactions from any Zone 1 primary output.

**P-5 — Income cohort served:**  
Bottom two income quintiles, pensioners 65+, youth 18–35 tradable sector. These cohorts are the primary subjects of the Human Cost Ledger and the development economist's distributional analysis. The legibility improvements to the Human Cost Ledger strip (unit expansion, tier meaning inline) directly serve the ability to cite bottom-quintile impacts in a negotiating context.

**P-6 — Negotiating leverage statement:**  
After accessing the Evidence Thread Architecture, Persona 2 can make the following specific argument when the reserve coverage finding is challenged: "The reserve coverage breach at step 6 shows 2.0 months current against a 2.5-month floor. This uses IMF BOP data at Tier 2 confidence — citable directly. The model relationship for reserve drawdown under current account deficit is calibrated against the 2001–2002 Argentine case and the 2015–2016 Ghanaian case, as documented in our methodology. The fiscal multiplier assumption that shapes the path to this breach is 1.30, drawn from the Ilzetzki et al. range for middle-income open economies."

This argument is not currently constructable from the primary screen. After ADR-015 implementation, each sentence of this argument is supported by a visible annotation: the tier label (T2 — citable), the interpretation anchor (what the score means), the assumption surface (fiscal ×1.30), and the L1 basis statement (calibration reference). The argument changes from "we believe this" to "here is our documented basis."

**P-7 — North star test answer:**  
The Zambian Finance Ministry's Deputy Minister of Finance is sitting at the table with an IMF mission team conducting a debt sustainability analysis review. The IMF team challenges the ministry's scenario: "Your political economy module shows a 59% programme survival probability, but you've modeled the conditionality schedule at 'standard' — the actual schedule proposed has stricter quarterly targets, which in comparable cases has reduced survival probability by 15–20 percentage points." 

Before ADR-015: the Deputy Minister's analyst looks at the screen and sees Financial 0.81, Governance 0.37. She cannot see the programme_survival_probability, cannot see the conditionality assumption, and cannot trace the confidence basis for the trajectory without leaving the instrument cluster. She has no response material from the screen.

After ADR-015: she sees "Political Feasibility 59% [T3]" in Zone 1D, sees "Conditionality: standard" in the assumption surface, can activate cross-examination mode and see the conditionality input expanded inline alongside the survival probability. She can respond: "The model shows 59% survival probability under standard conditionality. We agree the proposed schedule is more aggressive — we can run the adjusted scenario with the stricter quarterly targets now. The difference will be visible in Programme Feasibility within one step." This changes the dynamic of the negotiation: the ministry's analyst can engage with the challenge analytically rather than deferring to a later session.

This closes the specific asymmetry gap that motivated the political economy module: the IMF side has staff who can model political feasibility in real time; the ministry side now has the same capability visible in the primary viewport.

---

### UX Implication Statement

**UX-1 — Zone assignment and hierarchy certification:**  
This ADR places the following elements in the following zones:
- L0 basis annotations: Zone 1 (always visible, no interaction — consistent with `information-hierarchy.md §Zone 1: Instrument Cluster`)
- Assumption surface strip: positioned between Zone 0 (identity header) and Zone 1 (instrument cluster). This is a new surface that does not appear in the current zone taxonomy. It is architecturally a Zone 0.5 — always visible, no interaction, but lower priority than the identity strip itself. This positioning does not conflict with `information-hierarchy.md` because that document does not preclude a persistent strip between Zone 0 and Zone 1; it specifies that Zone 1 instruments must always be visible, which remains true after this strip is added.
- Programme_survival_probability: Zone 1D (instrument cluster co-primary), visible at zero interaction. This is consistent with Zone 1 assignment for primary-mission outputs per `information-hierarchy.md §Zone 1: Instrument Cluster — definition`.
- Cross-examination expanded state: inline expansion of Zone 1 elements — no zone reassignment. The content is Zone 1 (primary viewport); the mode transformation adds depth without displacing the zone.
- L1 basis statement: one interaction from Zone 1 — this is Zone 2 depth (one interaction, no navigation away from primary viewport). Consistent with `information-hierarchy.md §Zone 2: One Scroll or Click`.

**UX-2 — Primary cognitive task alignment:**  
- Mode 1 (trajectory reconstruction): assumption surface and basis threads support reconstruction by making the inputs and data basis visible alongside the outputs. L0 annotations are additive to the reading experience, not competitive with it.
- Mode 2 (threshold-safe path construction): assumption surface shows the fiscal multiplier and conditionality inputs that shape the path. Programme_survival_probability in Zone 1D adds a fifth axis to the path construction cognitive task — the analyst must find a path that is both threshold-safe *and* politically feasible. This is a Mode 2 cognitive task expansion that is consistent with the Mode 2 north star (threshold-safe path construction, now including political feasibility threshold).
- Mode 3 (real-time steering within human cost constraints): cross-examination mode must be suppressed (or disabled) in Mode 3. The Mode 3 primary cognitive task is real-time steering — additional cognitive load from expanded evidence chains is contraindicated. L0 annotations may remain visible in Mode 3 (they are compact and do not compete with the primary read), but cross-examination mode must not be activatable. Assumption surface is suppressed in Mode 3 (the Mode 3 control plane in Zone 1A may display current control inputs, making the assumption surface redundant).

**UX-3 — Entry state coverage (falsifiable acceptance criteria):**  

*Reactive entry state (Journey B Step 3):*  
"Zone 1D displays a tier annotation below each framework score without any user interaction, using the Jordan/Egypt Hormuz Demo 4 fixture loaded at step 8 at 1440×900. The annotation is legible (minimum 9px rendered font size) and does not overflow the Zone 1D column at 1280px minimum viewport width. Acceptance criterion: Playwright test captures Zone 1D at 1280×900 with Hormuz fixture, asserts that all four framework rows contain a text element matching the pattern `[T{N} · {source_description}]`, and that all four elements are within the visible viewport without scroll."

*Reactive entry state (challenge response, 90-second ceiling):*  
"Persona 2 can activate cross-examination mode and read the basis statement for the challenged TERMINAL Reserve Coverage alert within 30 seconds of the challenge, using only the primary viewport. Acceptance criterion: from the moment the 'Defend' button or '?' shortcut is activated, all Zone 1B alerts expand to full-detail form within 500ms (observable via Playwright waitForSelector on the expanded alert element with timeout 500ms)."

*Preparatory entry state (Journey A Step 4):*  
"The assumption surface strip is visible below the ScenarioIdentityHeader and above the InstrumentCluster in all three modes, using the Hormuz fixture at step 4. Acceptance criterion: Playwright test asserts that a `data-testid='assumption-surface'` element exists in the DOM, is not display:none, and contains text matching the pattern `Fiscal ×{N.NN}` when fiscal multiplier override is non-default."

**UX-4 — HCL parity certification:**  
This ADR does not affect HCL visual weight relative to financial indicators. The Human Cost Ledger strip annotation changes (unit expansion, tier meaning inline) improve the legibility of the HCL without changing its visual weight. HCL parity is maintained. The basis thread annotation format is the same for HCL rows as for financial indicators — no differential treatment.

**UX-5 — Uncertainty display specification:**  
- Tier 1 (real observed data, high quality): annotated `[T1 · {source name}]`. In cross-examination mode: "High confidence — cite directly. Source: {source name}, vintage {year}."
- Tier 2 (official statistics, curated): annotated `[T2 · {source type} {year}]`. In cross-examination mode: "Moderate confidence — cite with caveat. Source: {source type}, vintage {year}. Caveat: official statistics may have publication lag of up to 18 months."
- Tier 3 SYNTHETIC_COMPARABLE: annotated `[T3 · synthetic]`. The word "synthetic" appears verbatim in the annotation. In cross-examination mode: "Early estimate — confirm before citing. Method: synthetic inference from comparable economies. Do not cite as observed data."
- Tier 4 (model estimate): annotated `[T4 · model estimate]`. In cross-examination mode: "Exploratory — do not cite. This value is a model output, not an observed or statistically-inferred estimate."
- Structural Absence Declaration: annotated `[—]` with a "?" hover indicator. In cross-examination mode: "Structural absence — this indicator is not computable for the current entity configuration. This is a documented model limitation, not a data gap."
- Pre-calibration disclosure: when `ia1_disclosure = True`, appended to any annotation: `· pre-cal`. This is always visible at L0, not deferred to Zone 3.

**UX-6 — Irreversibility signal integrity certification:**  
This ADR does not modify the TERMINAL/CRITICAL visual distinction or alert severity display. The basis thread annotations are additive to alert text; they do not alter color, border, or severity-label display. TERMINAL alerts remain visually distinct from CRITICAL with no implementation discretion. The compact alert rows in Zone 1B are the surface changed (full indicator name rather than truncated), not the severity display. Acceptance criterion for irreversibility: using the Greece M8 Demo fixture loaded at step 6 (TERMINAL Reserve Coverage FIN GRC + TERMINAL CO₂ Boundary ECO GRC, two TERMINAL alerts), both alerts are visible in Zone 1B without scroll at 1280×800 desktop and 1024×768 tablet. Playwright test: `page.setViewportSize({width: 1280, height: 800}); assert zone1b contains two elements with text 'TERMINAL' visible in viewport; assert no scroll required`.

**UX-7 — User journey coverage:**  
- Journey B Step 3 [Near-Term-Gap] "defend challenged output in 90 seconds" — closed by cross-examination mode (Component 4) and basis threads (Component 1). After ADR-015: "Zone 1B top detail plus one interaction → basis statement" is the new Journey B Step 3a.
- Journey A Step 4 [Near-Term-Gap] "identify which assumptions shaped the trajectory before the negotiating session" — closed by assumption surface (Component 2). After ADR-015: the assumption surface answers this at zero interaction.
- Journey F Step 7 [Near-Term-Gap] "political feasibility as a traceable output, not a hidden computation" — closed by programme_survival_probability in Zone 1D (Component 3). After ADR-015: programme_survival_probability is Zone 1, visible at zero interaction.

**UX Designer sign-off:**  
This sign-off is a precondition for the acceptance vote.

**Reviewing agent:** UX Designer Agent  
**Session context:** Same session as ADR authorship — acknowledged  
**Governing documents reviewed:** `information-hierarchy.md §Zone 1: Instrument Cluster`, `information-hierarchy.md §Zone 2: One Scroll or Click`, `north-star.md §Primary Cognitive Tasks`, `north-star.md §Reactive Entry State Time Ceiling`, `user-journeys.md §Journey B Step 3`, `user-journeys.md §Journey A Step 4`, `worldsim-ux-architecture-first-principles.md §Governing Premise 2 (Instruments Always Visible)`  
**Concerns found:** 4 — listed below.

Concern 1: The assumption surface introduces a new visual strip between Zone 0 and Zone 1. If this strip carries more than one line of text at any viewport width, it compresses the vertical space available for the instrument cluster. The implementation must enforce a single-line, fixed-height constraint (maximum 24px rendered height) on the assumption surface at all viewport widths. If the content overflows this constraint, it must truncate with ellipsis rather than wrapping.

Concern 2: The L0 annotations on Zone 1D scores (e.g., `[T2 · 4 indicators · IMF/Central Bank 2024]`) must not increase the row height of Zone 1D to the point where the four framework rows no longer fit within the Zone 1D allocation without scroll at 1280×800. The annotation must render as a secondary text line within the existing row height, or the row height must be increased without reducing the instrument cluster's visual weight relative to the choropleth map below it. This requires explicit pixel measurement in the implementation.

Concern 3: Cross-examination mode's inline expansion of Zone 1D component indicators must not displace Zone 1B or Zone 1C from the visible viewport when activated. If expansion causes Zone 1B or Zone 1C to scroll off-screen, the mode has violated the "instruments always visible" governing premise. The implementation must demonstrate that at 1280×900, Zone 1B top detail slot and Zone 1C PMM remain visible with cross-examination mode active.

Concern 4: The "Defend" button placement in the header, adjacent to the mode selector, risks visual crowding in the existing header layout. The header already contains: product name, choropleth attribute selector, Compare scenarios checkbox, Scenarios button, Fidelity button, mode selector (three buttons), a Mode 3 button, step counter, and Next Step button. Adding a "Defend" button may require header layout redesign. A keyboard-shortcut-only implementation (`?` activates cross-examination mode, no button) is an acceptable alternative that avoids header crowding if the Frontend Architect Agent determines the button cannot be accommodated without degrading the mode selector's legibility.

`[ ]` UX Designer sign-off. 2026-06-15

---

## Silent Failure Mode

**Component 1 (Basis threads):**  
If the backend fails to return tier information or source attribution for a given indicator, the annotation renders as `[—]` rather than suppressing the row or showing a blank annotation slot. A blank annotation (no `[...]` visible at all) would be indistinguishable from a design choice to not annotate; `[—]` is visually distinct and signals "annotation unavailable" without being alarming. Detection mechanism: QA runs the Hormuz fixture with a mock API response that returns null for confidence_tier on one indicator; asserts that the affected row shows `[—]` annotation rather than the full annotation string or an empty string.

**Component 2 (Assumption surface):**  
If the sensitivity attribution computation fails or returns an empty list, the strip renders the fixed available inputs (fiscal multiplier, mode, entity, data vintage) from the scenario configuration rather than failing silently. If even scenario configuration is unavailable, the strip is suppressed entirely and a `data-testid="assumption-surface-unavailable"` element is present in the DOM for test detectability. A missing assumption surface is preferable to a wrong assumption surface.

**Component 3 (programme_survival_probability):**  
If the political economy module is enabled but the survival probability computation fails, the row shows `Political Feasibility  — [computation error]` rather than being suppressed. Suppression would create the impression the political economy module is not enabled; the explicit error label makes the failure visible. Detection mechanism: QA runs a political economy-enabled scenario with a mocked PE module response returning null; asserts that the fifth row in Zone 1D shows the label "Political Feasibility" and the value "—" with text "[computation error]".

**Component 4 (Cross-examination mode):**  
If an alert in Zone 1B fails to expand (e.g., the L1 basis data is missing from the API response), the alert row in cross-examination mode shows the full indicator name and "Basis: unavailable" rather than silently not expanding. An unexpanded alert in cross-examination mode looks identical to an expanded alert that has no basis data — which is a trust failure. "Basis: unavailable" is a transparent disclosure.

---

## Asymmetry Assessment

Well-resourced actors — IMF mission teams, World Bank economists, sovereign wealth fund analysts, creditor syndicate advisors — have immediate access to the methodology documentation, calibration records, and assumption sets behind any analytical output their tools produce. They can answer a challenge to a number in real time because they have staff who authored the methodology and can retrieve the basis statement from institutional memory. The challenge response is not a navigation task for them — it is a conversation with a colleague in the room.

WorldSim's ministry-side analyst does not have that staff. Her tool must serve the function that the creditor side's institutional memory serves. ADR-015 closes this gap by making the methodology traversable from the output under time pressure. The gap that remains after ADR-015: the L1 basis statement will reference calibration documents that are not yet authored for all model relationships. Until `docs/methodology/calibration-basis.md` is complete (Chief Methodologist M14 deliverable), the basis statement can point to the document but the document may not yet contain all referenced entries. This is a known limitation — the traversal path exists before the destination is complete.

---

## North Star Test

A Zambian Finance Ministry analyst is in a debt restructuring session with IMF staff. The IMF analyst challenges the scenario at step 4: "Your model shows a 41% drop in Governance score by step 4, but you have not explained what drives that — is this an assumption about democratic quality, or is it a model artifact?" 

Before ADR-015: the analyst can see Governance 0.37 in Zone 1D. She cannot see what indicators compose the score, what data tier underlies it, or what assumption shaped its trajectory. She cannot respond analytically.

After ADR-015: she activates cross-examination mode. Governance 0.37 expands inline to show its three component indicators (Democratic Quality Index, Institutional Capacity, Elite Capture Coefficient) with their individual values and tier labels. She can state: "The Governance score decline is driven by the Democratic Quality Index declining from 0.48 to 0.27 between steps 2 and 4 — this is a Tier 3 model estimate based on Freedom House and V-Dem data patterns for comparable economies under conditionality, which we've labeled 'early estimate, confirm before citing.' The elite capture coefficient is 0.31, a T3 synthetic estimate. This is the model's political economy assessment of governance erosion under the proposed conditionality — we can discuss the assumption directly." She has moved from "we assert this" to "here is the basis."

---

## Mission Impact Statement

This ADR closes the gap between WorldSim's ability to *produce* analytical outputs and the ministry's ability to *defend* them. Signal detection is necessary but not sufficient for the mission — a finance minister who can see that a threshold is crossed but cannot explain why cannot use that finding at the table. ADR-015 makes every Zone 1 primary output *traversable* from the challenged number to its basis, within the time and interaction constraints of the negotiating room.

This is ranked as the highest-priority asymmetry-closing capability in M14, above any additional measurement sophistication. A more sophisticated model that the ministry team cannot defend is less useful than a less sophisticated model they can defend completely. The kryptonite constraint is the organizing principle: the ministry team with three economists must be able to respond to a challenge as fast as the creditor side with their institutional staff can make it. This ADR operationalizes that constraint at the Zone 1 surface.

---

## Minimum Data Tier

The Evidence Thread Architecture improves legibility at all data tiers — it makes the tier visible, not the underlying data. At Tier 5 (no direct data — synthetic extrapolation only), the annotation will show `[T5 · synthetic extrapolation]` and cross-examination mode will show "Exploratory only — do not cite. Basis: extrapolation from regional patterns with no country-specific data." This is the most important use case for the architecture: a finance ministry with thin data coverage needs to know *more clearly*, not less, when the model is operating from synthetic inference. The architecture makes this distinction explicit at L0.

Minimum data tier at which this capability produces actionable output: Tier 5 (the annotations and cross-examination mode work regardless of data tier; the actionability of the underlying output is a separate question). No minimum data tier constraint on this ADR.

---

## Alternatives Considered

### Alternative 1 — Documentation-only approach (expand Zone 3 methodology notes)

Improve the methodology documentation in Zone 3 (entity drawer → framework panels → methodology notes) without modifying Zone 1. Cost: the 6-step navigation path remains. This fails the Reactive entry state time ceiling. The path to the methodology exists today; the problem is that it is not traversable under negotiating room time pressure. Adding more content to Zone 3 does not solve the traversal problem.

**Rejected:** Does not satisfy P-4 (time ceiling) or the Geopolitical Analyst's minimum viable trust architecture requirement (two interactions from challenge to evidence).

### Alternative 2 — Dedicated "methodology" panel in Zone 2

Add a collapsible "Methodology" panel to the entity drawer that surfaces calibration records and assumption sets. One click opens it. Cost: the user must navigate from the challenged Zone 1 number to the entity drawer to the methodology panel. This is still a 3-step path from the challenged number (identify alert → open drawer → open methodology panel). It does not serve the Reactive entry state.

**Rejected:** Improves discoverability but does not reach the time ceiling. Also, the methodology panel would need to be scenario-specific (the assumptions for a Greece run differ from a Jordan run), which the entity drawer architecture does not currently support without significant restructuring.

### Alternative 3 — Full methodology sidebar (persistent right panel)

Replace the Zone 1B/1C/1D co-primary cluster with a tabbed panel where one tab is "Instruments" (current Zone 1B/1C/1D) and one tab is "Basis" (methodology, assumptions, confidence). Cost: the instruments are only visible when the "Instruments" tab is active — they are no longer Zone 1 (no interaction). This violates the "instruments always visible" governing premise (UX architectural commitment 2 from CLAUDE.md).

**Rejected:** Violates ADR-008 and the governing UX premises. Instruments must always be visible without any interaction.

### Alternative 4 — Evidence Thread Architecture on Zone 2 (drawers) only

Implement basis threads as hover/click disclosures on Zone 1B, Zone 1C, Zone 1D elements, but do not add L0 annotations (persistent inline text). Basis threads are only revealed on interaction. Cost: at L0, the screen looks identical to today. The minister must know to hover/click to find the basis, which requires prior knowledge of the feature. For a Demo 5 participant who has never seen the tool, the basis is invisible unless they already know to look for it.

**Rejected:** Does not satisfy UX-3 (the Reactive entry state acceptance criterion requires L0 visibility without interaction). The kryptonite constraint requires the basis to be visible by default, not revealed only to users who know to look.

---

## Consequences

### Positive

- Closes Journey B Step 3 [Near-Term-Gap]: minister's analyst can defend a challenged number in under 90 seconds
- Closes Journey A Step 4 [Near-Term-Gap]: model assumptions visible at zero interaction before negotiating session
- Closes Journey F Step 7 [Near-Term-Gap]: programme_survival_probability in Zone 1D
- Operationalizes the kryptonite constraint at the Zone 1 surface
- Makes the confidence tier system user-facing rather than documentation-internal: "T4" becomes "model estimate" at the display surface
- Enables Demo 5 (live external participants) to challenge outputs and receive analytical responses from the screen
- Forces the Chief Methodologist to author the PMM interpretation anchor — a methodology commitment that was previously deferred

### Negative

- Adds visual density to Zone 1D (basis annotations require additional vertical space per row)
- Requires the frontend to receive and render per-indicator tier and source information that is currently available in the API but not consumed by Zone 1 components — additional frontend engineering scope
- Adding a fifth Zone 1D row (programme_survival_probability) is conditional on EL decision regarding ADR-008 relationship — this may block Component 3 if ADR-008 amendment process is lengthy
- Cross-examination mode adds a new interaction state to manage — it must be suppressed in Mode 3, which adds a mode-dependent rendering branch
- The PMM annotation cannot be authored until the Chief Methodologist delivers the interpretation anchor (Decision 3) — Component 1 partial (PMM) is blocked on a non-frontend deliverable

### Known Limitations

- The L1 basis statement will reference `docs/methodology/calibration-basis.md` entries that are not yet complete for all model relationships. The traversal path to the basis exists before the destination is complete. Users who activate cross-examination mode and navigate to an incomplete calibration entry will find a placeholder. This is transparent but unsatisfying.
- The assumption surface shows the 3–4 highest-sensitivity inputs from the backend's sensitivity attribution computation. If this computation is not available for a scenario (e.g., very short scenarios with insufficient step data for attribution), the assumption surface falls back to showing only the hardcoded user-set inputs (fiscal multiplier, mode). The sensitivity attribution path for the full assumption surface requires the backend sensitivity analysis capability to be stable.
- The ecological directionality confusion (Gap ML-2, Decision 2) is not fixed by the L0 annotation alone. The annotation will show the tier and source; it will not resolve the apparent contradiction between the composite score direction and the alert severity direction until the EL resolves the directionality convention decision.

---

## Diagram

`docs/architecture/ADR-015-evidence-thread-architecture.mmd` — to be authored by Architect Agent at intent document filing (Step 1). The diagram must show: Zone 0 (identity header), Zone 0.5 (assumption surface), Zone 1 (instrument cluster with L0 annotations visible), L1 basis expansion (one interaction), and the cross-examination mode transition.

---

## Backtesting Validation Anchor

This ADR does not introduce a new composite score or measurement methodology. It modifies display of existing scores. No backtesting validation anchor is required for the display changes.

The PMM interpretation anchor (Decision 3) will require Chief Methodologist validation of the interpretation text against historical cases where the PMM was computable for known outcomes — but this is a Chief Methodologist pre-acceptance deliverable, not a backtesting requirement on this ADR.

---

*ADR-015 authored 2026-06-15. Phase 0 encoded. Evidence base: `docs/demo/m14/reviews/2026-06-15-ux-legibility-audit-minister-exercise.md`. Backlog entry: ARCH-009. Template version: 2026-06-09.*
