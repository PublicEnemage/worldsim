---
name: M14-G6c-zone-1a-design-thinking
type: implementation-intent
issue: "#845 — Zone 1A information architecture — multi-dimensional encoding"
status: Filed
authored-by: UX Designer Agent
authored-date: 2026-06-18
implementing-agent: UX Designer Agent
sprint-entry: "N/A — design-only; no sprint entry required per sprint plan §G6c"
---

# Implementation Intent: M14-G6c — Zone 1A Phase 1 Design Thinking

> **Design-only deliverable.** No implementation PR opens from this group.
> No QA Lead test authorship obligation. The "observable application state"
> for G6c is the design document itself meeting specific completeness criteria
> — verifiable by any agent reading the file without knowledge of Zone 1A's
> implementation. The Architecture Review Facilitator confirms Phase 2
> readiness at M15 kickoff.

---

## 1. Source Issue and Design Authority

**Issue:** #845 — Zone 1A information architecture — multi-dimensional encoding (framework × entity × branch × mode)
**Phase:** Phase 1 — UX Design Thinking Document
**ADR:** None — Phase 3 ADR is M15 scope; this document gates that ADR
**Status at time of authorship:** Issue open; Phase 1 authorized as M14 parallel track (EL directive 2026-06-16)
**Authored by:** UX Designer Agent
**Date:** 2026-06-18
**Implementing agent:** UX Designer Agent

**Governing documents read (mandatory before authoring):**
- `docs/ux/north-star.md §Primary Cognitive Tasks by Mode`
- `docs/ux/information-hierarchy.md §Dashboard View Hierarchy`
- `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md §Question 1`
- `CLAUDE.md §UX Architectural Commitments` (commitments 1–5)
- `docs/ux/user-journeys.md §Journey B` (Reactive entry state)
- `docs/ux/personas.md §Persona 2` (Finance Ministry Negotiator)

**Design authority constraints:**
- UX architectural commitment #4: "Each mode has its own primary cognitive task."
  Zone 1A's design must be derived from per-mode cognitive tasks, not retrofitted to all three.
- UX architectural commitment #3: "The step axis is the shared frame for all instruments."
  Any Zone 1A redesign concept must preserve the shared step axis.
- Platform Principle (`CLAUDE.md §The Platform Principle`): The instrument is situation-agnostic.
  Zone 1A must not become entity-specific or scenario-specific in its design contract.
- Issue #845 EL directive 2026-06-15: DEMO-044 framing (curve endpoint labels as fix) is
  explicitly rejected. The design must not entrench the current multi-line encoding as permanent.

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou / Aicha Diallo archetype).
The design thinking document derives Zone 1A's cognitive task from what Persona 2 must be able to
read and argue from Zone 1A alone — not from what Zone 1A currently displays.

Secondary consideration: Persona 3 — Institutional Decision-Maker (multi-entity comparative
analysis), who drives the multi-dimensional encoding problem (N entities × M branches). The design
must name how Zone 1A serves Persona 3 in Mode 1 comparative analysis without making Zone 1A
illegible for Persona 2.

**P-2 — Entry state:**
- **Reactive** (primary design constraint): Persona 2 is at the negotiating table. A trajectory
  number is challenged. She looks at Zone 1A. The design must answer: what single question can
  she confirm from Zone 1A in 90 seconds, in each mode?
- **Preparatory**: Persona 2 prepares her briefing. Mode 2 simulation — what does Zone 1A tell
  her about whether the constructed path crosses a threshold?
- **Comparative** (Persona 3 consideration): Mode 1 replay — two entities, two branches. Zone 1A
  is being asked to carry 4 frameworks × N entities × M branches simultaneously.

**P-3 — Journey reference:**
- Journey B Step 3 [Near-Term-Gap]: Persona 2 defends challenged output. Zone 1A must answer
  "what was the trajectory?" within the 90-second Reactive ceiling.
- Journey A Step 2 [Preparatory]: Persona 2 checks trajectory shape before the session. Zone 1A
  must answer "is the threshold-safe path visible?" within 5-minute Preparatory ceiling.
- The design thinking document must name which journey step each mode's Zone 1A question
  corresponds to — not in generic terms, but naming the specific step.

**P-4 — Time/interaction ceiling:**
- Mode 1 (Replay): trajectory reconstruction — Persona 2 must confirm the trajectory shape for a
  single entity within 30 seconds of entering Mode 1. Zero-interaction requirement for primary signal.
- Mode 2 (Simulation): threshold-safe path construction — Persona 2 must see whether the current
  path crosses a threshold within 30 seconds of a scenario advance. The trajectory must update
  synchronously with the step advance.
- Mode 3 (Active Control): real-time steering — Persona 2 must read Zone 1A's trajectory response
  to a control input within 15 seconds. This is the hardest constraint — it determines whether
  Zone 1A can carry the multi-entity encoding at all in Mode 3.

**P-6 — Negotiating leverage delivered** *(Persona 2):*
The design document itself does not deliver negotiating leverage — that is Phase 4 (implementation,
M16). The design document must specify, for each mode, what the Persona 2 negotiating argument
from Zone 1A will be after Phase 4 is complete. This is the north star test for the design
choices made in Phase 1.

**P-7 — North star capability delivered (by Phase 4, through this design):**
After Phase 4 (M16 implementation derived from this design), Persona 2 in the Reactive state can
state: "Zone 1A shows [specific answer to the mode's primary question]." The Phase 1 document
must name this sentence for each mode. Without it, the Architecture Review (Phase 2) has no
criterion to evaluate the proposed design against.

---

## 3. Observable Application State

> G6c is design-only. The observable state is the design document, verifiable by any agent
> reading it. The test for each statement below: can the Architecture Review Facilitator
> confirm it by reading `docs/ux/design-thinking/zone-1a-information-architecture.md`
> without referencing the implementation?

### 3.1 Primary observable state

`docs/ux/design-thinking/zone-1a-information-architecture.md` exists and contains three mode
sections — one for Mode 1, one for Mode 2, one for Mode 3 — each containing:

1. A single named Persona 2 question, formatted as a direct question answerable from Zone 1A
   alone within the mode's time ceiling (e.g., "Has the financial framework trajectory crossed
   the reserve coverage threshold before step 4?"). The question must be specific — not
   "What is the trajectory?" but a question with a binary or bounded answer.
2. The mode's time ceiling (seconds) stated explicitly, matched to `north-star.md §P-4`.
3. An explicit statement of what information the analyst needs from Zone 1A to answer
   that question — naming the dimensions required (frameworks, entities, branches) and
   the minimum dimensionality needed in the single-mode case.

### 3.2 Secondary observable states

**Secondary state A — Combinatorial tension addressed:**
The document contains a section titled "Combinatorial Tension" (or equivalent) that addresses
the multi-dimensional case explicitly: what happens to the primary question's legibility when
N > 1 entities are loaded, or M > 1 branches exist. For each combination that breaks the
primary question's legibility, the document names the breaking point (e.g., "at N=3 entities
and M=2 branches, 24 lines exceed Zone 1A's legibility ceiling") and proposes where the
overflowing information lives — Zone 1B, Zone 1D, a dedicated comparative view, or a
proposed new surface.

**Secondary state B — What lives elsewhere — explicit allocation:**
The document contains an information allocation table or section that names, for each dimension
(framework, entity, branch, mode-specific control input), which Zone owns that dimension and
why. The allocation must be explicit: "Entity trajectory comparison lives in [Zone X] because
[reason derived from that zone's cognitive task]." Implicit allocations ("elsewhere") are not
acceptable — every displaced dimension must have a named home.

**Secondary state C — Phase 2 readiness assertion:**
The document ends with a "Phase 2 Readiness" section that lists the three questions the
Architecture Review Facilitator must be able to answer from this document before the panel
convenes: (1) what is Zone 1A's primary question in each mode, (2) which encoding channels
does the proposed design use to answer it, and (3) what are the design's constraints on M
(branches) and N (entities) before legibility breaks. If the document cannot answer these
three, Phase 2 cannot begin.

### 3.3 Silent failure detection

A design thinking document that describes the problem without proposing a design direction
is a silent failure. The document must contain at least one concrete design direction for
each mode — not a recommendation for further research. "Zone 1A needs a different approach
for Mode 3" is not a design direction. "Zone 1A in Mode 3 shows a single composite trajectory
per entity (framework aggregation), with per-framework detail accessible via Zone 1D at zero
interaction — entities distinguished by position (top/bottom) rather than color" is a design
direction.

Observable distinguisher: the Architecture Review Facilitator can state, after reading the
document, what Zone 1A is proposed to display for a 3-entity Mode 3 scenario. If they cannot
— if the document only describes the problem — the document is incomplete.

---

## 4. Acceptance Criteria

**AC-1 (Mode 1 cognitive question):**
The document contains a section explicitly titled "Mode 1 — Trajectory Reconstruction" (or
equivalent). That section names one Persona 2 question that Zone 1A must answer within 30
seconds of Mode 1 entry, stated as a direct question with a bounded answer.
Observable: the Architecture Review Facilitator can read the question aloud in one sentence.
The question is not "What is the trajectory?" — it names a specific analytical task
(e.g., threshold crossing, framework divergence pattern, recovery point identification).

**AC-2 (Mode 2 cognitive question):**
The document contains a section explicitly titled "Mode 2 — Simulation / Threshold-Safe Path"
(or equivalent). That section names one Persona 2 question that Zone 1A must answer within 30
seconds of a scenario advance in Mode 2, stated as a direct question with a bounded answer.
The question is mode-specific: it is answerable from trajectory data updated at each step advance
and cannot be answered by a static snapshot.

**AC-3 (Mode 3 cognitive question):**
The document contains a section explicitly titled "Mode 3 — Active Control" (or equivalent).
That section names one Persona 2 question that Zone 1A must answer within 15 seconds of a
control input application in Mode 3, stated as a direct question with a bounded answer.
The section explicitly states whether the current multi-line encoding (4 frameworks × N entities
× M branches) is compatible with a 15-second response read or not. If not compatible, the
section names the maximum dimensionality Zone 1A can carry in Mode 3 without exceeding the
time ceiling, and where excess dimensions are allocated.

**AC-4 (Combinatorial tension — breaking-point named):**
The document names at least one (N, M) combination — N entities × M branches — at which the
current Zone 1A encoding breaks legibility, with a brief explanation of why (e.g., "4 frameworks
× 3 entities × 2 branches = 24 same-axis lines; no labeling scheme resolves this"). The
breaking point is specific (named N and M values), not general ("too many lines").

**AC-5 (Information allocation — entity dimension homed):**
The document explicitly names where entity-level trajectory comparison lives when N > 1 —
either in Zone 1A (with a specified encoding change), Zone 1B, Zone 1D, or a named new
surface. "Elsewhere" without a named destination is not acceptable. The named destination
must not conflict with that zone's current cognitive task as defined in
`docs/ux/information-hierarchy.md`.

**AC-6 (Information allocation — branch dimension homed):**
The document explicitly names where Mode 3 branch comparison (baseline vs. control-input path)
lives when M > 1 — either in Zone 1A (with a specified encoding change), or a named destination
with the same non-conflict requirement as AC-5.

**AC-7 (Concrete design direction — at least one per mode):**
For each of the three modes, the document contains at least one concrete design direction
proposal: a specific description of what Zone 1A displays for a named scenario (e.g., "JOR,
Mode 3, 2 branches: Zone 1A shows two lines — composite trajectory per branch, not per
framework — with framework detail in Zone 1D"). The proposal is specific enough that the
Architecture Review Facilitator can assess whether it satisfies the mode's cognitive task
and time ceiling.

**AC-8 (Phase 2 readiness section present):**
The document contains a section explicitly titled "Phase 2 Readiness" (or equivalent) at the
end. That section lists the three questions the Architecture Review Facilitator uses to gate
Phase 2 (listed in §3.2 Secondary state C), and for each, a brief answer pointing to the
document section where the full treatment is found. The section must not say "see above" —
it must name the section heading.

---

## 4b. Visual Spec (before/after)

**AC-7 — Concrete design direction format (example of what is NOT acceptable):**
```
"Zone 1A needs to handle multi-entity scenarios better.
 Further research is required into encoding approaches."
^^^^ No concrete proposal — this does not satisfy AC-7.
^^^^ The Architecture Review panel cannot evaluate this.
```

**AC-7 — Concrete design direction format (example of what IS acceptable):**
```
"Mode 3 (Active Control): Zone 1A displays composite trajectory per entity
 (one line per entity, framework aggregation), with no per-framework color
 channel in Mode 3. Framework detail lives in Zone 1D (current position
 always-visible, no interaction). At N=2 entities: 2 lines on Zone 1A,
 readable. At N=3: 3 lines, still manageable. At N>4: the Facilitator
 is flagged that Zone 1A will not be used as the primary instrument
 for >4-entity scenarios — a dedicated comparative surface is required."
```

---

## 5. Kryptonite Constraint Check

**Does this design document's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` No — the *design document* is a specification authored for the Architecture Review panel,
not a user-facing output. The kryptonite constraint applies to the *Zone 1A design itself*, not
to the intent document.

**Kryptonite constraint on the design itself:**
The design directions proposed in the document must satisfy the kryptonite test: the Zone 1A
display that results from each proposed design direction must be interpretable by Persona 2
without a specialist translating it. Specifically:

- A Mode 3 design direction that requires the analyst to "know which line is which" from color
  alone, across 16 same-colored lines, does NOT satisfy the kryptonite constraint.
- A design direction that requires the analyst to open a tooltip or drawer to understand what
  Zone 1A is showing does NOT satisfy the 15-second Mode 3 ceiling.
- A design direction that aggregates frameworks into a composite and labels each entity by name
  (or by country code with a persistent legend) satisfies the kryptonite test: the ministry
  economist can read "JOR: 0.62 → CRITICAL" without specialist mediation.

The document must confirm, for each proposed design direction, that the resulting display is
interpretable by Persona 2 within the mode's time ceiling without a specialist present.

---

## 6. Out of Scope

**Phase 2 — Architecture Review (M15):**
This document is the input to Phase 2, not Phase 2 itself. The design thinking document does
not constitute an architectural decision. No ARCH-REVIEW artifact is produced in G6c.

**Phase 3 — ADR (M15):**
No ADR is authored in G6c. The ADR number is not assigned until Phase 3 initiation. The design
thinking document must not reference an ADR number or claim ADR authority over any decision.

**Phase 4 — Implementation (M16):**
No code changes, no component modifications, no `frontend/src/` file edits. G6c produces one
Markdown document. Any implementer who reads this intent document and makes code changes is
out of scope.

**Zone 1B, Zone 1C, Zone 1D redesign:**
The design thinking document may propose that certain information be allocated to Zone 1B,
Zone 1C, or Zone 1D — but it may not propose changes to those zones' cognitive tasks or
layouts. The information allocation is about *where the displaced content goes*, not about
redesigning the receiving zones.

**ADR-015 Component 4 (cross-examination mode):**
G6c must not overlap with ADR-015 Component 4 (M15). Component 4 is about the Zone 1D
interactive L1 expansion. G6c is about Zone 1A's encoding contract. These are distinct
surface areas. The design thinking document may reference the eventual Component 4 capability
as a destination for detailed framework evidence, but must not specify its design.

**Axis encoding or rendering changes:**
The document proposes design directions. It does not specify CSS, SVG encoding, axis labels,
or React component structures. Those are Phase 4 (implementation) decisions.

---

## 7. Review Obligation

> G6c is design-only. No QA Lead test authorship applies. The review obligation is:
> the Architecture Review Facilitator confirms at M15 kickoff that the document
> satisfies the Phase 2 prerequisites. This is a document completeness check, not a
> technical review.

**Reviewer:** Architecture Review Facilitator (at M15 Phase 2 kickoff)
**Review deadline:** Before Phase 2 panel convenes in M15
**Document location:** `docs/ux/design-thinking/zone-1a-information-architecture.md`
**Review criteria:** AC-1 through AC-8 (Section 4 above) — the Facilitator confirms each is
satisfied before opening the Phase 2 Architecture Review issue.

**Pre-M14-exit obligation (PM Agent):**
The document must exist and be committed to `release/m14` before the M14 exit ceremony
begins. PM Agent confirms document presence as part of the M14 exit checklist. A missing
document blocks M14 exit — it does not defer to M15.

**PM Agent verification check (at M14 exit):**
`find docs/ux/design-thinking -name "zone-1a-information-architecture.md"` must return the
file. PM Agent runs this check before recording M14 exit. If the file is absent, M14 exit is
blocked until it exists.

**Facilitator acknowledgment:** (to be completed at M15 kickoff)
`[ ]` Architecture Review Facilitator: Phase 2 prerequisites satisfied — AC-1 through AC-8
confirmed in document. Phase 2 panel may be convened. [Date]

---

## Appendix: Zone 1A Background — Why Phase 1 Is Not Trivial

The current Zone 1A encoding contract — time (steps) × composite score × framework (color)
— was designed for one cognitive task: single-entity, single-mode trajectory comparison
across four frameworks.

That contract is now under pressure from four simultaneous dimensions:
- Frameworks: 4 (fixed)
- Entities: N (GRC, JOR, EGY, ZMB in M14; unbounded at scale)
- Branches: M (baseline + Mode 3 control-input branch; multiple what-ifs in future)
- Mode: 3 distinct cognitive tasks, each requiring a different primary question

At the Hormuz scenario scale (2 entities, 2 branches): 4 × 2 × 2 = **16 lines** on one axis.
At a 3-entity, 2-branch scenario: 4 × 3 × 2 = **24 lines**. No labeling scheme makes 24
same-axis lines legible in 15 seconds.

The governing question for Phase 1: **What is the single Persona 2 question Zone 1A must
answer, in each mode, within the mode's time ceiling?** Encoding channels and information
allocation follow from the answer. They cannot be designed before the question is answered.

Phase 1 does not answer the encoding question. It answers the question that comes before
it. The Architecture Review (Phase 2) evaluates whether the proposed design directions for
each mode are architecturally sound. The ADR (Phase 3) makes the binding decision. Phase 4
implements it.

The design thinking document is complete when the Architecture Review Facilitator can read
it and say: "I know what Zone 1A is trying to answer in each mode, I know what it is
proposing to display, and I know where the information that Zone 1A cannot carry is going."
That is the Phase 2 readiness criterion.

---

*Intent document version: 2026-06-18. Issue #845 Phase 1 authorized as M14 parallel track
(EL directive 2026-06-16). No sprint entry document required (design-only; no implementation
PR). Sprint plan authority: `docs/process/sprint-plans/m14-sprint-plan.md §G6c`. Implementing
agent: UX Designer Agent. Document must exist before M14 exit. Architecture Review Facilitator
confirms Phase 2 readiness at M15 kickoff. Full lifecycle authority: `CLAUDE.md §Agent Execution
Lifecycle`. Zone 1A implementation is M16 — this document governs Phase 1 only.*

---

## 8. Step 5 — Business PO Validate

**Date:** 2026-06-18
**Verdict: ACCEPT**

**Documentation Validate criterion applied** (`docs/process/acceptance-protocol.md §Documentation`):
A non-author (Architecture Review Facilitator) can navigate to the key finding from the
document's entry point in under five minutes.

**AC-by-AC confirmation:**

| AC | Status | Evidence |
|---|---|---|
| AC-1 (Mode 1 question) | ✅ PASS | §Mode 1: "At which step did the first MDA threshold crossing occur — and which framework's trajectory crossed first?" — bounded, specific, one sentence |
| AC-2 (Mode 2 question) | ✅ PASS | §Mode 2: "After this step advance, does any framework trajectory project a crossing below its MDA floor in the remaining steps?" — mode-specific (step-updated data required), bounded |
| AC-3 (Mode 3 question + compatibility verdict) | ✅ PASS | §Mode 3: 15-second ceiling stated; explicit incompatibility verdict for N>1; maximum dimensionality named (1 composite line per entity × 2 branches, N≤4) |
| AC-4 (Breaking points named) | ✅ PASS | §Combinatorial Tension: 3 specific breaking points with named (N, M) values (Mode 3 N=2 M=1 → 16 lines; Mode 1/2 N=3 M=1 → 12 lines; COMPARE_VIEW N=2 M=2 → 16 lines) |
| AC-5 (Entity dimension homed) | ✅ PASS | §Information Allocation table: entity comparison → Zone 1A composite per entity + Zone 1D + Zone 2B; non-conflict rationale present |
| AC-6 (Branch dimension homed) | ✅ PASS | §Information Allocation table: M>1 what-if branches → COMPARE_VIEW; non-conflict rationale present |
| AC-7 (Concrete direction per mode) | ✅ PASS | Named scenarios: Mode 1 (JOR+EGY+ZMB, 3 composite lines); Mode 2 (JOR+EGY at step 4, projected floor crossing visible); Mode 3 (JOR+EGY, fiscal_multiplier=1.30 at step 3, 4 lines: baseline+active per entity) |
| AC-8 (Phase 2 Readiness section present) | ✅ PASS | §Phase 2 Readiness answers all three gating questions with named section pointers (not "see above") |

**Layer 3 gate:** Not triggered. G6c produces no user-facing indicator label, alert text, or
confidence tier disclosure.

**North star forward trace (P-7):**
G6c's north star is a forward trace to Phase 4 (M16 implementation). The design document
names the specific Persona 2 argument for each mode that will be available after Phase 4:

- **Mode 3 (the binding constraint):** Zambian finance ministry analyst in live negotiation at
  step 3, JOR+ZMB Mode 3 scenario, fiscal multiplier proposed. Zone 1A shows 4 lines
  (JOR-baseline ghost, JOR-active solid, ZMB-baseline ghost, ZMB-active solid — all composite).
  JOR-active diverges upward from JOR-baseline after step 3. Zone 1D shows Financial: +0.04 vs
  baseline — always visible, no interaction. Argument: "The fiscal multiplier improves the
  programme composite score — specifically the financial framework — relative to the baseline
  path." Readable in 15 seconds without specialist mediation. This argument was previously
  unavailable: the 16-line encoding at N=2+M=2 exceeded the 15-second legibility ceiling and
  no design direction existed for what Zone 1A would display in this scenario.

The Phase 1 document creates the design foundation from which this argument becomes available.
The north star test is forward-looking (M16) — confirmed as a forward trace, not a M14 claim.

**Kryptonite check:** Each proposed design direction contains an explicit kryptonite check
confirming the Zone 1A output will be interpretable by Persona 2 without specialist mediation
within the mode's time ceiling. All three modes pass.

**Navigation test (documentation criterion):** Architecture Review Facilitator reading
the document cold can locate: (1) the primary question per mode (§Mode sections), (2) the
breaking points (§Combinatorial Tension), (3) the information allocation (§Information
Allocation table), (4) the concrete design directions (§Concrete Design Directions), and
(5) the Phase 2 gating answers (§Phase 2 Readiness) — all within 5 minutes from the document
opening. Section headings are explicit; Phase 2 Readiness provides a summary index.

**Sprint exit gate:** AC-1 through AC-8 satisfied. Layer 3 gate not triggered. North star
forward trace present and specific. G6c is COMPLETE. Issue #845 Phase 1 is closed.
PI Agent may confirm sprint exit for G6c. M14 exit ceremony prerequisite (document present in
`release/m14`) is satisfied.
