---
name: M15-G3-cohort-disaggregation-political-risk-design
type: implementation-intent
issues: "#986 — cohort disaggregation on primary surface; #987 — political risk summary surface (Persona 3)"
status: Filed
authored-by: UX Designer Agent
authored-date: 2026-06-21
implementing-agent: UX Designer Agent
sprint-entry: "N/A — design-only; no sprint entry required per m15-sprint-plan.md §G3 and §Sprint Entry Gate Exceptions"
---

# Implementation Intent: M15-G3 — Cohort Disaggregation and Political Risk Summary Design

> **Design-only deliverable.** No implementation PR opens from this group.
> No QA Lead test authorship obligation. The "observable application state"
> for G3 is the design documents themselves meeting specific completeness criteria —
> verifiable by any agent reading the files without knowledge of any implementation.
> Architecture Review Facilitator and Chief Methodologist confirm readiness before
> any M16 G-group implementation sprint entry is filed.

---

## 1. Source Issues and Design Authority

**Issue A:** #986 — feat(ux): cohort disaggregation on primary surface
**Issue B:** #987 — feat(ux): political risk summary surface — plain-language legitimacy dynamics for Persona 3 in primary viewport
**Phase:** Design-only (M15); implementation is M16 scope for both issues
**ADR prerequisite:** None for G3 itself — but the cohort disaggregation design must explicitly address whether its placement depends on ADR-017 (Zone 1A Phase 3, #845). The issue body of #986 states: "The design for cohort disaggregation may be subsumed into the Zone 1A ADR (#845 Phase 3) if cohort data belongs in Zone 1A." AC-5 requires the design document to resolve this question explicitly.
**Status at time of authorship:** Both issues open; G3 authorized as M15 parallel track per `docs/process/sprint-plans/m15-sprint-plan.md §Sprint Groups`
**Authored by:** UX Designer Agent
**Date:** 2026-06-21
**Implementing agent:** UX Designer Agent

**Governing documents read (mandatory before authoring):**
- `docs/ux/north-star.md §Primary Cognitive Tasks by Mode`
- `docs/ux/information-hierarchy.md §Dashboard View Hierarchy`
- `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md §Question 1`
- `CLAUDE.md §UX Architectural Commitments` (commitments 1–5)
- `docs/ux/user-journeys.md §Journey A, §Journey B`
- `docs/ux/personas.md §Persona 2, §Persona 3`
- `docs/ux/design-thinking/zone-1a-information-architecture.md` (M14 G6c Phase 1 — Zone 1A encoding contract and information allocation table)

**Design authority constraints:**
- UX architectural commitment #2: "Instruments are always visible; context is navigable." Cohort disaggregation and political risk summary must appear on the primary surface without a drawer.
- UX architectural commitment #4: "Each mode has its own primary cognitive task." Both design documents must specify mode-specific display contracts — a single unified contract that ignores modes does not satisfy this constraint.
- Platform Principle (`CLAUDE.md §The Platform Principle`): Both instruments must work for any country (Bolivia, Zambia, Greece, Jordan) without structural modification. The design must not embed country-specific cohort definitions.
- Zone 1A Phase 1 interplay: `zone-1a-information-architecture.md §Information Allocation` names what each zone is responsible for. Both design documents must confirm that the proposed placement is non-conflicting with those zone responsibilities — or explicitly propose a revision to the allocation that feeds into ADR-017.

---

## 2. Persona Trace Elements Targeted

### Issue #986 — Cohort Disaggregation

**P-1 — Persona served:**
Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou / Aicha Diallo archetype).
Secondary: Persona 5 — Civil Society / NGO Policy Analyst (distributional impact analysis).
Origin: M11.5 Session 3 (2026-06-04-persona-2-003) FINDING-03 (HIGH severity): "No cohort disaggregation visible — CONCLUDED answer was ~80% historical knowledge, not tool output." G3 design closes this gap. The engine's DemographicModule produces cohort-level data; that data is invisible at the instrument level.

**P-2 — Entry state:**
Reactive (primary design constraint): Persona 2 is at the negotiating table. A counterparty challenges distributional claims — "Which cohort is most affected and when?" Persona 2 must read the answer from the primary viewport within 90 seconds without opening a drawer.

**P-3 — Journey reference:**
- Journey B Step 3 [Near-Term-Gap] (Reactive): Persona 2 defends challenged distributional output. "The bottom quintile crosses the poverty headcount threshold at step 2" must be readable on-screen at step 2, not reconstructed from domain knowledge.
- Journey A Step 2 (Preparatory): Persona 2 checks whether the bottom quintile crosses a threshold in any simulated step before the negotiating session.

**P-4 — Time/interaction ceiling:**
90 seconds from the primary viewport, zero drawer interactions. The design must specify the maximum number of visual elements (cohort rows, threshold lines) that remain legible within this constraint at 1440×900.

**P-6 — Negotiating leverage delivered (Persona 2):**
The design document specifies the argument. After M16 implementation: "Under current conditionality terms, the bottom income quintile crosses the poverty headcount CRITICAL threshold at step 2. The middle quintile remains above the WARNING threshold at all steps." Persona 2 can state this from on-screen data within 90 seconds — without a prior briefing from an analyst.

**P-7 — North star capability delivered:**
After M16 implementation derived from this design, Persona 2 in the Reactive state can cite the specific cohort, the specific indicator, the specific threshold severity, and the specific step — from the primary viewport, without specialist mediation and without opening a drawer. That argument was previously unavailable: cohort data existed in the engine but was invisible at the instrument level. The design document must name the specific argument and the exact viewport zone that delivers it.

---

### Issue #987 — Political Risk Summary Surface

**P-1 — Persona served:**
Persona 3 — Senior Policy Advisor (Andreas Stefanidis archetype). No formal economics training. Translates model outputs into political narratives: will this programme survive? When does public legitimacy collapse? What is the political cost in the 18-month window?

The political economy module (ADR-013, M13, #392 closed) is live and ships PSP, legitimacy index, and elite capture divergence. These outputs are currently invisible to Persona 3 without navigating to Zone 1D and interpreting composite scores — a task that requires domain knowledge Andreas does not have.

**P-2 — Entry state:**
Reactive: Persona 3 is in the room. 30-second ceiling. He needs PSP, legitimacy trajectory direction, and a plain-language interpretation — without opening Zone 1D or navigating to a framework composite.
Preparatory: Persona 3 prepares a political risk briefing before the session. Mode 2, constructing a path — does the current simulated trajectory breach the legitimacy fragility threshold?

**P-3 — Journey reference:**
Political feasibility assessment before a negotiating session (Preparatory, Mode 2). Real-time political risk check during active negotiation (Reactive, current step). The design must specify which journey step each mode's display contract corresponds to.

**P-4 — Time/interaction ceiling:**
30 seconds from the primary viewport (Reactive, Persona 3). Zero interaction requirement — PSP as severity-labeled percentage, direction label, and plain-language interpretation must all be simultaneously visible without any click.

**P-6 — Negotiating leverage delivered (Persona 3):**
The design document specifies the argument. After M16 implementation: "Programme survival probability has fallen below the critical threshold at step 3. At this level, historical ECF programmes show abandonment within 3 implementation steps. Legitimacy index is declining, approaching the fragility boundary." Andreas can state this from on-screen data within 30 seconds — with no data economist present to translate it.

**P-7 — North star capability delivered:**
After M16 implementation derived from this design, Persona 3 in the Reactive state can read programme survival probability as a severity-labeled percentage with a plain-language historical analogue — from the primary viewport, without specialist mediation. The ADR-013 political economy module ships data that is currently visible only to specialists navigating Zone 1D; this design makes it visible in Persona 3's idiom. The design document must name the specific argument and the display zone that delivers it.

---

## 3. Observable Application State

> G3 is design-only. The observable states are the design documents themselves, verifiable by
> any agent reading them. The test for each statement below: can the Architecture Review
> Facilitator or Chief Methodologist confirm it by reading the design document without
> referencing implementation code or the simulation engine directly?

### 3.1 Primary observable state

**For #986:**
`docs/ux/design-thinking/cohort-disaggregation-design.md` exists and contains all five of:

1. A named placement decision — which Zone (1A, 1B, 1D, or new surface) owns cohort disaggregation on the primary surface, with a rationale derived from a named section of `docs/ux/information-hierarchy.md`.
2. A cohort scope definition — which cohort dimensions are surfaced in M16 (minimum: income quintile; others named or explicitly deferred with rationale), tied to Persona 2's negotiating argument, not data availability alone.
3. An indicator scope definition — which cohort-level indicators are surfaced, with threshold type for each (MDA-derived or cohort-specific), in sufficient detail for the Chief Methodologist to confirm methodological defensibility.
4. A zero-interaction display format — the exact visual format (literal text block or wireframe, not prose description) visible at the primary viewport with zero user actions, showing cohort name, indicator name, severity, and step.
5. An ADR-017 interplay statement — explicit disposition: either cohort disaggregation is subsumed into ADR-017 (and this document becomes an input to that panel) or it proceeds independently (with a non-conflict statement referencing Zone 1A Phase 1's information allocation table by section name).

**For #987:**
`docs/ux/design-thinking/political-risk-summary-design.md` exists and contains all four of:

1. A named placement decision — which Zone hosts the political risk summary for Persona 3, with rationale and a non-conflict check against Zone 1D's existing political economy composite display.
2. A mode-specific display contract — separate specifications for Mode 1 (Replay, historical trajectory) and Mode 2 (Simulation, step-advance response), naming which political economy indicators appear in each mode and in what format.
3. A plain-language sentence specification — the exact sentence format for a named scenario (ZMB ECF at step 3 with PSP ≈ 0.38), not a template but a literal example.
4. A 30-second legibility check — explicit confirmation that Persona 3 (no formal economics training) can read and act on the named display within 30 seconds without specialist mediation, with a statement of what jargon was eliminated and how.

### 3.2 Secondary observable states

**Secondary state A — Zone cognitive task conflict check:**
`cohort-disaggregation-design.md` explicitly addresses whether the proposed placement degrades any receiving zone's primary cognitive task. "Zone 1B can hold cohort rows" is not sufficient — the document must confirm that adding cohort rows does not crowd the threshold breach alerting function of Zone 1B (if that is the proposed home), or provide an alternative placement rationale if Zone 1B is at capacity.

**Secondary state B — Mode-specific display contract (both documents):**
Both design documents contain explicit per-mode sections. A display specification that does not differentiate Mode 1 (replay — historical fixture, fixed trajectory) from Mode 2 (simulation — step-advance responsive) does not satisfy this state. The mode-specific contract must address at minimum: what changes at each step advance in Mode 2, and what the display shows in a Mode 1 fixture with a known historical outcome.

**Secondary state C — M16 implementation gate section (both documents):**
Each document ends with a section titled "M16 Implementation Gate" (or equivalent) that lists any unresolved dependencies that must be cleared before a M16 sprint entry for that issue can be filed. Dependencies must be named specifically — "ADR-017 must be accepted," "CM must confirm threshold calibration for selected indicators," "Political risk ADR must be accepted (if required per AC-11)," or "None — M16 sprint entry may be filed when G3 design is accepted." "See above" is not an acceptable entry.

### 3.3 Silent failure detection

A design document that describes the problem without specifying the display contract is a silent failure. The observable distinguisher:

For `cohort-disaggregation-design.md`: After reading the document, a QA reviewer can complete the sentence: "In a ZMB ECF Mode 2 scenario at step 2, Zone [N] shows [specific text or row format] for the bottom income quintile." If the reviewer cannot complete the sentence from the document alone — if the document only says "we should surface cohort data clearly" — the document is incomplete.

For `political-risk-summary-design.md`: After reading the document, a QA reviewer can complete the sentence: "In a ZMB ECF Mode 2 scenario at step 3 with PSP=0.38, Zone [N] shows [exact text and severity label]." If the reviewer must read engine code or Zone 1D implementation to complete the sentence, the document is incomplete.

---

## 4. Acceptance Criteria

### #986 — Cohort Disaggregation Design

**AC-1 (Zone placement decision):**
`cohort-disaggregation-design.md` contains a section titled "Zone Placement" (or equivalent) that names which Zone (1A, 1B, 1D, or new surface) hosts cohort disaggregation on the primary surface. The rationale references a named section of `docs/ux/information-hierarchy.md` and names that zone's primary cognitive task. The rationale confirms the proposed placement serves (not conflicts with) that cognitive task. "It makes sense in Zone 1B" without naming the cognitive task is not an acceptable rationale.

**AC-2 (Cohort scope definition):**
The document names which cohort dimensions are surfaced in M16 implementation — minimum: income quintile. For each additional cohort dimension (age cohort, regional cohort, gender cohort): included with rationale, or explicitly deferred with deferral target milestone. The rationale for included cohorts must be tied to Persona 2's negotiating argument (which cohort argument is most mission-critical at the table) rather than data availability.

**AC-3 (Indicator scope definition):**
The document names which cohort-level indicators are surfaced in M16, with:
- At least one poverty or human development indicator (e.g., poverty headcount rate, poverty gap, child malnutrition)
- Threshold type for each: whether the threshold is derived from the MDA architecture (existing floor system) or is a cohort-specific threshold requiring new calibration
- Severity tier schema: how CRITICAL / WARNING / WATCH map to cohort threshold proximity
The Chief Methodologist must be able to confirm methodological defensibility from this section alone, without reading backend indicator code.

**AC-4 (Zero-interaction display format):**
The document shows the exact display format visible in the primary viewport with zero user interaction — as a literal text block or wireframe excerpt, not as prose description. The literal format must name: cohort label (in plain language — not a field key), indicator label (in plain language), threshold severity badge (CRITICAL / WARNING / WATCH), and step reference. Maximum rows visible without scroll at 1440×900 must be stated. Sorted order (by severity, by step, or other) must be stated.

Example of what satisfies AC-4:
```
Zone 1B | Step 2 | ZMB ECF | Mode 2
────────────────────────────────────────────────────
CRITICAL  Bottom quintile — Poverty headcount
          Threshold crossed at step 2
WARNING   Lower-middle quintile — School enrollment rate
          5.8% below 3-year floor projection
[3 cohorts above threshold — not shown]
────────────────────────────────────────────────────
Max 2 rows visible without scroll at 1440×900. Sorted: CRITICAL first.
```

Example of what does NOT satisfy AC-4:
"Zone 1B will display cohort threshold alerts clearly, enabling Persona 2 to see distributional impacts."

**AC-5 (ADR-017 interplay statement):**
The document contains one of the following explicit statements:

(a) "Cohort disaggregation is subsumed into ADR-017. The placement, cohort scope, and display format decisions in this document are inputs to the Zone 1A ADR-017 panel. G3 is complete when this document is accepted by the Architecture Review Facilitator as Phase 2 input material."

(b) "Cohort disaggregation proceeds independently of ADR-017. Placement in [Zone N] does not depend on Zone 1A encoding decisions. Non-conflict with Zone 1A Phase 1 information allocation: [reference to the specific entry in `zone-1a-information-architecture.md §Information Allocation` that names [Zone N] as the home for this category of content]."

A statement that neither commits to (a) nor (b) — that defers the architectural question to M16 — is not acceptable. G3 exists to answer this question so that M16 sprint entry does not require reopening it.

**AC-6 (M16 implementation gate section):**
The document ends with an "M16 Implementation Gate" section. That section lists each dependency that must be cleared before a M16 sprint entry for #986 can be filed, named specifically:
- If ADR-017 acceptance is required: stated explicitly
- If CM threshold calibration for selected indicators is required: stated with CM sign-off condition
- If a new ADR is not required: stated explicitly with rationale
- If no dependencies: "No blocking dependencies — M16 sprint entry may be filed when G3 design documents are accepted by the Architecture Review Facilitator." This is a valid answer but requires an explicit check against ADR-017 dependencies.

---

### #987 — Political Risk Summary Design

**AC-7 (Zone placement decision):**
`political-risk-summary-design.md` contains a section titled "Zone Placement" (or equivalent) naming which Zone hosts the political risk summary for Persona 3. The rationale must address: (a) which zone's cognitive task serves a non-expert political advisor at a 30-second ceiling, and (b) whether the proposed placement conflicts with Zone 1D's existing political economy axis (PSP composite currently shows in Zone 1D). The document must explicitly state whether the political risk summary replaces, extends, or supplements Zone 1D's existing display — it may not leave this ambiguous. A statement of "Zone 1D already has PSP — this design makes it Layer 3" is acceptable if it explains the specific display change; "we will add to Zone 1D" without naming the change is not.

**AC-8 (Mode-specific display contract):**
The document contains a separate section for Mode 1 (Replay) and Mode 2 (Simulation), each specifying:
- Which political economy indicators appear: PSP at minimum; whether legitimacy index and elite capture divergence are included, deferred, or excluded (with rationale for each)
- Format for each indicator: percentage, direction label (declining / stable / improving), plain-language sentence, severity badge — each named explicitly, not collectively described as "clear format"
- Update behaviour in Mode 2: which elements update at each step advance and which are static

A unified display contract that does not distinguish Mode 1 from Mode 2 does not satisfy AC-8.

**AC-9 (Plain-language sentence specification):**
The document shows the exact plain-language sentence format for a named scenario at a named step. The scenario must be specific: ZMB ECF programme at step 3, PSP ≈ 0.38, legitimacy index ≈ 0.42. The sentence must be literal, not a template:

Example of what satisfies AC-9:
```
Zone [N] | Step 3 | ZMB ECF | Mode 2

Programme survival: CRITICAL (38%)
At this level, historical ECF programmes show abandonment within 3 steps.
Legitimacy index: declining — approaching fragility threshold (0.42 of 0.35 floor)
Elite capture divergence: widening — fiscal benefit concentration increasing
```

Example of what does NOT satisfy AC-9:
"The political risk summary will display PSP and legitimacy status in plain language that Persona 3 can understand."

**AC-10 (30-second legibility check):**
The document contains an explicit legibility confirmation: the named display from AC-9 is readable by Persona 3 — a senior policy advisor with no formal economics training — within 30 seconds, without specialist mediation. The check must be substantive: it names at least one piece of jargon or composite score that was removed or translated into plain language in the design, and confirms the resulting display requires no prior knowledge of the political economy module to interpret.

**AC-11 (ADR requirement disposition and M16 implementation gate section):**
The document explicitly answers whether a new ADR is required for the political risk surface — the issue body (#987) flags this as an open question ("design + ADR if required"). The answer must be one of:

(a) "A new ADR is required. The political risk surface introduces a new primary surface zone or modifies the Zone [N] cognitive task contract in a way that requires formal architectural approval. ADR number will be assigned from `docs/architecture/backlog.md` when authorship begins."

(b) "No new ADR is required. The political risk summary is a Layer 3 enhancement to existing Zone [N] content within the accepted display contract of that zone. Implementation in M16 proceeds from this design document and the existing zone's ADR (ADR-NNN)."

The document ends with an "M16 Implementation Gate" section on the same terms as AC-6: named dependencies cleared before M16 sprint entry, including whether PSP historical calibration (#1084, G5) must be complete before the plain-language historical analogue sentence can be implemented.

---

## 4b. Visual Spec (before/after)

**AC-4 — Cohort disaggregation (what is NOT acceptable):**
```
"Zone 1B will surface cohort data in a legible, structured format so that Persona 2
 can understand distributional impacts without specialist mediation."
^^^^ No display contract — this does not satisfy AC-4.
^^^^ A QA reviewer cannot describe what appears on screen from this description.
```

**AC-4 — Cohort disaggregation (what IS acceptable — illustrative, not prescriptive):**
```
Zone 1B | Step 2 | ZMB ECF Mode 2
────────────────────────────────────────────────────────
CRITICAL  Bottom quintile — Poverty headcount
          Threshold crossed at step 2
WARNING   Lower-middle quintile — School enrollment rate
          5.8% below 3-year floor projection
[3 cohorts above threshold — not shown]
────────────────────────────────────────────────────────
2 rows max at 1440×900. Sorted severity-first. No scroll required.
```
The design document may propose a different format — this example is here to show
the specificity required, not to prescribe the design direction.

---

**AC-9 — Political risk summary (what is NOT acceptable):**
```
"The political risk surface will show programme survival probability and a plain-language
 interpretation that Persona 3 can act on within 30 seconds."
^^^^ No literal sentence — this does not satisfy AC-9.
```

**AC-9 — Political risk summary (what IS acceptable — illustrative, not prescriptive):**
```
Zone [N] | Step 3 | ZMB ECF Mode 2 | PSP=0.38, LI=0.42

Programme survival: CRITICAL (38%)
At this level, historical ECF programmes show abandonment within 3 steps.
Legitimacy index: declining — approaching fragility threshold (0.42 / 0.35 floor)
Elite capture divergence: widening — fiscal concentration increasing
```
The design document may propose a different format — this example shows the
specificity required. The exact wording, threshold framing, and historical
analogue phrasing are design decisions G3 must make.

---

## 5. Kryptonite Constraint Check

**Does this design document's primary observable state require specialist mediation for
Persona 2 (or Persona 3) to act on it in the Reactive entry state?**

`[x]` No — the *design documents* are specifications for the Architecture Review panel and
M16 implementing agents, not user-facing outputs. The kryptonite constraint applies to the
designs themselves.

**Kryptonite constraint applied to the design for #986:**
- Any proposed display that requires Persona 2 to know which field key maps to which cohort does NOT satisfy the constraint. `hh_exp_q1` is not a label; "Bottom income quintile" is.
- Any proposed display that requires opening a drawer or navigating to Zone 1D to read cohort detail violates the 90-second zero-interaction ceiling.
- The display format specified in AC-4 must use plain-language cohort labels and severity badges (CRITICAL / WARNING / WATCH) that are self-interpreting. The document must explicitly confirm this for the proposed format.

**Kryptonite constraint applied to the design for #987:**
- Any proposed display that uses "PSP" as the sole label without defining it on-screen for a non-economist does NOT satisfy the constraint.
- Any proposed display that uses "legitimacy index" as a composite score without a plain-language direction label does NOT satisfy the constraint.
- The plain-language sentence in AC-9 is the primary kryptonite test. The document must confirm that the sentence is interpretable by a senior policy advisor — someone who knows "38% survival probability" is alarming but would not know what "composite_score = 0.38 across the political economy framework" means.

---

## 6. Out of Scope

**M16 implementation:**
No code changes. No component modifications. No edits to `frontend/src/`, `backend/`, or any runtime file. G3 produces two Markdown design documents and nothing else. An agent reading this intent document and opening a feature PR has exceeded scope.

**ADR-017 authorship:**
G3 may determine that cohort disaggregation belongs in Zone 1A and should feed into ADR-017 — but G3 does not author or assign ADR-017. The Architecture Review (Phase 2 of #845) is a separate process governed by `docs/architecture/backlog.md`. G3's cohort disaggregation design document is an input to that process if AC-5 disposition (a) is chosen; it is not a substitute for the ADR.

**New ADR authorship (for #987):**
AC-11 requires the political risk design document to state whether a new ADR is required. If the answer is yes, G3 documents the need — it does not assign an ADR number, convene a panel, or draft the ADR. ADR number assignment follows `docs/architecture/backlog.md §Assigning a Number`.

**Cohort-level threshold calibration:**
The design document specifies which cohort indicators and thresholds belong in the M16 display. It does not calibrate thresholds against historical data. Calibration is CM domain work for M16. AC-3 requires the design document to specify the threshold basis in sufficient detail for CM to confirm defensibility — the CM confirmation is the gate, not G3's own calibration.

**PSP calibration anchor (#1084):**
The PSP historical calibration anchor is G5 scope. G3's political risk design (#987) may reference it as a prerequisite for the M16 plain-language historical analogue sentence (named in AC-11) — but G3 does not author or implement the calibration.

**Zone 1B, Zone 1D, or Zone 1A cognitive task redesign:**
Both design documents may propose that content live in one of these zones — but neither document may propose changes to those zones' primary cognitive tasks or existing display contracts beyond what is explicitly noted as a conflict-resolution step. If a conflict is identified, the design document names it and routes it to ADR-017 or the relevant architectural process — it does not unilaterally resolve it.

**#1083 (Grounding strip date label), #1088–#1090 (walkthrough updates):**
These are G5 scope. G3 is not responsible for any G5 issues.

---

## 7. Review Obligation

> G3 is design-only. No QA Lead test authorship applies. Two reviewers are required:
> Chief Methodologist (cohort indicator and threshold scope for #986) and Architecture
> Review Facilitator (M16 readiness gate for both documents).

**Reviewer A — Chief Methodologist**
**Scope:** Confirm that the cohort indicator selection and threshold basis in `cohort-disaggregation-design.md` are methodologically defensible per AC-3. CM acknowledgment is recorded as a comment on the design document or as a comment on GitHub issue #986 before any M16 sprint entry for cohort disaggregation implementation is filed.
**Review deadline:** Before any M16 sprint entry for #986 implementation is filed.

**Reviewer B — Architecture Review Facilitator**
**Scope:** Confirm AC-1 through AC-6 for `cohort-disaggregation-design.md` and AC-7 through AC-11 for `political-risk-summary-design.md`. Both documents must satisfy their criteria before M16 sprint entries for either #986 or #987 implementation are filed. If AC-5 disposition (a) is chosen, the Facilitator routes G3's cohort design document as input to the ADR-017 Phase 2 panel.
**Review deadline:** Before any M16 sprint entry for #986 or #987 implementation is filed.

**Document locations:**
- `docs/ux/design-thinking/cohort-disaggregation-design.md` (for issue #986)
- `docs/ux/design-thinking/political-risk-summary-design.md` (for issue #987)

**Review acknowledgments:** (completed at review time)

`[ ]` Chief Methodologist: Cohort indicator scope and threshold basis in `cohort-disaggregation-design.md` confirmed methodologically defensible (AC-3). M16 sprint entry for #986 may proceed on CM grounds. [Date]

`[ ]` Architecture Review Facilitator: AC-1 through AC-6 satisfied for `cohort-disaggregation-design.md`; AC-7 through AC-11 satisfied for `political-risk-summary-design.md`. M16 sprint entries for #986 and #987 may be filed — ADR-017 and new-ADR dependencies noted as required by the gate sections. [Date]

---

*Intent document version: 2026-06-21. Issues #986 and #987 authorized as M15 G3 parallel track per `docs/process/sprint-plans/m15-sprint-plan.md §Sprint Groups`. No sprint entry document required (design-only; no implementation PR). Implementing agent: UX Designer Agent. Both design documents must exist before M15 exit. Architecture Review Facilitator confirms M16 readiness before any M16 G-group implementation sprint entry is filed for either issue. Full lifecycle authority: `docs/process/agent-execution-lifecycle.md`.*

---

## 8. Step 4 Verify record

**Verifying agent:** UX Designer Agent
**Date:** 2026-06-22
**Method:** QA test suite — `backend/tests/test_m15_g3_cohort_political_risk_design.py` (45 tests, AC-1–AC-11); direct document read by verifying agent

> G3 is design-only. The observable application state is the design documents themselves. The
> verify step confirms: (1) both documents exist at canonical paths, (2) each contains the
> specified content, and (3) QA tests programmatically confirm document completeness criteria.
> CI test-backend: PASS on PR #1109 merge commit (2026-06-22).

**Result: 45/45 QA tests PASS; all AC observable states confirmed**

| AC | Result | Observable state confirmed |
|---|---|---|
| AC-1 | PASS | `cohort-disaggregation-design.md` §Zone Placement names Zone 1B; references `information-hierarchy.md §Zone 1 / 1B`; names cognitive task "threshold crossing alerts"; confirms placement serves (not conflicts) |
| AC-2 | PASS | Income quintile (REQUIRED, M16); under-5 and under-18 age cohort (LIMITED, M16); gender cohort deferred M17 with rationale; subnational deferred M17+ with rationale — all tied to Persona 2 negotiating argument |
| AC-3 | PASS | Three indicators (poverty headcount, school enrollment, child malnutrition); each has cohort dimension, MDA-derived threshold type, severity tier schema; methodological note for CM per indicator |
| AC-4 | PASS | Literal text block present for ZMB ECF Mode 2 step 2; shows severity badge, plain-language cohort label, plain-language indicator label, threshold proximity sentence, tier label, source citation; max rows (2 at 1440×900, 1 at 1024×768) stated; sort order stated |
| AC-5 | PASS | Disposition (b) stated explicitly: "Cohort disaggregation proceeds independently of ADR-017"; references `zone-1a-information-architecture.md §Information Allocation`; explicitly states M16 sprint entry does not require ADR-017 acceptance |
| AC-6 | PASS | "M16 Implementation Gate" section present; 3 named dependencies: CM sign-off, Data Architect DemographicModule confirmation, ARF confirmation; ADR-017 explicitly stated NOT required |
| AC-7 | PASS | `political-risk-summary-design.md` §Zone Placement names Zone 1D; addresses (a) 30-second ceiling for non-expert and (b) non-conflict check with existing Zone 1D political economy display; states SUPPLEMENTS (not replaces) |
| AC-8 | PASS | Mode 1, Mode 2, and Mode 3 sections each specify: indicators (PSP REQUIRED, legitimacy REQUIRED, elite capture OPTIONAL), format per indicator, direction labels, update behaviour, empty state |
| AC-9 | PASS | Literal example present for ZMB ECF step 3, PSP=0.38, legitimacy=0.42, Mode 2; sentence construction rules provided; jargon-eliminated list present |
| AC-10 | PASS | Explicit 28-second read-through for Andreas Stefanidis (Persona 3, no formal economics training); what he can say in the room stated; 4 jargon terms eliminated with plain-language replacements named |
| AC-11 | PASS | Explicit disposition (b): no new ADR required; 4-part rationale; escalation path if ARF disagrees; "M16 Implementation Gate" section with 5 named dependencies including #1084 (conditionally required) |

**Silent failure tests (both documents):**

- Cohort (#986): After reading `cohort-disaggregation-design.md`, a QA reviewer CAN complete: "In a ZMB ECF Mode 2 scenario at step 2, Zone 1B shows a 'COHORT IMPACT' sub-section below MDA alerts with at most 2 rows visible, the first showing 'CRITICAL — Bottom income quintile — Poverty headcount — Threshold crossed at step 2 · was 3.8% above floor'." Completable from the document without reading implementation code. **PASS.**
- Political risk (#987): After reading `political-risk-summary-design.md`, a QA reviewer CAN complete: "In a ZMB ECF Mode 2 scenario at step 3 with PSP=0.38, Zone 1D shows 'Programme survival: CRITICAL (38%) — DECLINING / At this level, historical ECF programmes show abandonment within 3 steps.'" Completable from the document without reading implementation code. **PASS.**

`[x]` Step 4 Verify: COMPLETE — 45/45 QA tests PASS; all 11 ACs confirmed by document read and test suite. 2026-06-22

---

## 9. Step 5 Validate record

**Business PO:** Business PO Agent
**Date:** 2026-06-22
**Method:** Direct read of `docs/ux/design-thinking/cohort-disaggregation-design.md` and `docs/ux/design-thinking/political-risk-summary-design.md` on `release/m15` (merged via PR #1109 2026-06-22); confirmed both documents accessible at canonical paths.

**Customer Agent Layer 3 assessment:**

G3 is a design-only deliverable. The Layer 3 check applies to whether the *designs themselves* specify Layer 3 output — i.e., do the designs describe displays that tell the user what the number means, not just the number?

- **Cohort disaggregation (AC-4 display format):** PASS. The specified display shows severity badge (CRITICAL / WARNING / WATCH) + plain-language cohort label ("Bottom income quintile") + plain-language indicator label ("Poverty headcount") + threshold proximity sentence ("Threshold crossed at step 2 · was 3.8% above floor") + source citation. This is Layer 3: the display tells Persona 2 what crossed, which cohort, how far, when, and from where — without requiring her to interpret a raw number. The display eliminates the field key barrier (`hh_exp_q1` → "Bottom income quintile").

- **Political risk summary (AC-9 sentence specification):** PASS. The specified display shows PSP as "Programme survival: CRITICAL (38%) — DECLINING" (replaces "PSP = 0.38"), historical analogue sentence (replaces a bare probability), legitimacy index with direction and floor proximity (replaces "legitimacy_index = 0.42"), and elite capture with plain-language qualifier. All four jargon-elimination steps are documented and confirmed in the 30-second legibility check. Persona 3 (Andreas, no formal economics training) can read and act on the display within 30 seconds without a data economist present.

**Customer Agent Layer 3 verdict: PASS (both designs specify Layer 3 output)**

**North Star Test:**

*Finance ministry team scenario:* Aicha Diallo (Persona 2 — Zambia Finance Ministry negotiator) and Andreas Stefanidis (Persona 3 — Senior Policy Advisor) are in an IMF ECF restructuring session at step 3. ZMB ECF. Two challenges arrive simultaneously:

- Creditor side: "Your distributional impact claims are not substantiated by the model output."
- Creditor side: "The political economy basis for your programme survival estimate is unclear — 65% of what?"

*Pre-G3 capability (design not yet implemented):* Cohort data exists in the DemographicModule but is invisible at the instrument level — FINDING-03 HIGH (M11.5 Session 3). Aicha must reconstruct the distributional answer from domain knowledge, not tool output. Political risk module outputs (PSP, legitimacy, elite capture) are in Zone 1D as composite scores — Andreas cannot read or act on them without a data economist to translate.

*Post-G3 capability (after M16 implementation from this design):*

1. **Cohort disaggregation (Aicha, Persona 2):** Zone 1B Cohort Impact sub-section shows "CRITICAL — Bottom income quintile — Poverty headcount — Threshold crossed at step 2." Aicha reads this verbatim: "Under current conditionality terms, the bottom income quintile crossed the poverty headcount CRITICAL threshold at step 2. You can see this on the screen." The argument is from instrument output, not domain knowledge. Creditor cannot challenge the source — it is the simulation's output from the agreed data inputs.

2. **Political risk summary (Andreas, Persona 3):** Zone 1D Political Risk sub-section shows "Programme survival: CRITICAL (38%) — DECLINING / At this level, historical ECF programmes show abandonment within 3 steps." Andreas reads this verbatim: "Programme survival is at 38% and declining — that is CRITICAL. At this level, historical ECF programmes show abandonment within 3 steps. You can see this on the screen." No data economist required. The argument names a historical precedent with a specific timeframe.

*Does this design change what the minister's team can argue at the table?*

Yes — materially and for two distinct personas. Both arguments were previously unavailable from instrument output:
- Cohort data existed in the engine but was invisible at the instrument level (FINDING-03 HIGH, unresolved since M11.5)
- PSP existed in Zone 1D but required specialist mediation to translate into a policy argument

After M16 implementation from this design, both arguments are available on the primary viewport, zero interactions, within the persona-specific time ceilings (90 seconds for Aicha, 30 seconds for Andreas).

**Kryptonite Constraint (FD-3):** SATISFIED. Both designs explicitly specify plain-language output that eliminates specialist mediation:
- Cohort: severity badge + plain-language cohort label + threshold proximity sentence (no field keys, no framework composites)
- Political risk: "Programme survival" replaces PSP, percentage replaces composite_score, historical analogue replaces raw probability, direction label replaces step-over-step arithmetic

Both designs were authored with explicit kryptonite checks (§5 of the intent document) and the legibility check for #987 documents the specific jargon eliminated.

**Business PO Validate verdict: ACCEPT**

*M16 gate status:* G3 exit does NOT clear the M16 implementation gates. Before any M16 sprint entry for #986 or #987 is filed, the following remain REQUIRED: (1) Chief Methodologist sign-off on indicator scope and threshold methodology for #986; (2) CM sign-off on PSP severity tiers and 2pp direction threshold for #987; (3) Data Architect confirmation of DemographicModule cohort field availability for GRC/JOR/EGY/ZMB; (4) Architecture Review Facilitator confirmation AC-1–AC-11 satisfied; (5) Frontend Architect Zone 1D layout feasibility check for #987. These are M16 gate conditions, not M15 exit conditions.

`[x]` Step 5 Validate: COMPLETE — Business PO ACCEPT 2026-06-22. Sprint exit document filed at `docs/process/sprint-plans/m15-g3-sprint-exit.md`.
