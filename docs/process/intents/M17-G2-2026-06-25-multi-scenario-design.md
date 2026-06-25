---
name: M17-G2-multi-scenario-design
type: design-intent
issue: "#394"
status: Filed — Phase 1 and Phase 2 design artifact deliverable; Phase 3 implementation intent is a separate artifact filed before Phase 3 sprint entry
authored-by: PM Agent
authored-date: 2026-06-25
design-agents:
  - UX Designer Agent (Artifact 1 — UX journeys + zone layout for N>2)
  - Customer Agent (Artifact 2 — persona minimum viable story)
  - Architect Agent (Artifact 3 — ARCH-REVIEW-007 N>2 assessment)
sprint-note: >
  Design-first, three-phase group. Phase 1 (design) and Phase 2 (architecture) produce
  design artifacts only — no implementation PR, no sprint entry required for either phase.
  Phase 3 (implementation) requires a separate sprint entry document and a separate
  implementation-intent document filed before any implementation PR opens. Phase 3 may
  carry to M18. Phase 3 implementation PR gate: #1249 (Zone 1A curve identifiability)
  must be merged before Phase 3 implementation PR opens.
adr-reference: >
  ARCH-REVIEW-007 (binding constraint — COMPARE_VIEW N≤2/fixture) must be revisited
  with Phase 1 UX journeys in hand. Phase 2 determines: ADR-017 amendment, new ADR,
  or architecture review note on #394. ADR determination is Phase 2 output (Artifact 3).
release-branch: release/m17
---

# Design Intent: M17-G2 — Multi-Scenario Comparison Design Sprint

> **Design-first sprint — Phases 1 and 2 produce design artifacts, not implementation code.**
> No sprint entry is required for Phase 1 or Phase 2. The "observable state" for this
> document is the design artifacts themselves meeting specific completeness criteria —
> verifiable by any agent reading the filed documents without knowledge of any implementation.
>
> **Phase 3 implementation** requires a separate implementation-intent document (to be filed
> before Phase 3 sprint entry) and a separate sprint entry document. The Phase 3
> implementation intent is authored from the Phase 1 UX journeys and the Phase 2
> architecture determination — not from this document alone.
>
> **Adapted from the standard intent template:** §3 describes design artifact deliverable
> states; §4 describes completion criteria reviewable by BPO and Architect; §7 states
> that the QA test authorship obligation applies to Phase 3 (not Phase 1 or 2). All
> other sections follow the standard template. Authority:
> `docs/process/sprint-plans/m17-sprint-plan.md §G2`.

---

## 1. Source

**Issue:** #394 — platform: multi-scenario comparison (>2 scenarios) — Kenya budget planning
marquee case requires lifting two-scenario limit

**Journey reference:**
- Journey A Step 3 [Near-Term-Gap] (Preparatory — Persona 1): Comparing three programme
  options before a negotiating session; current tool supports exactly N=2
- Journey B Step 3 [Near-Term-Gap] (Reactive — Persona 5): Identifying which restructuring
  option is least damaging to Q1 at the table; current tool cannot surface a three-way comparison
  on the primary viewport

**Status at authorship:** Issue #394 open; G2 authorized as M17 Wave 2 parallel design track
per `docs/process/sprint-plans/m17-sprint-plan.md §Sprint Groups`; Wave 1 exit gate confirmed
2026-06-25

**Authored by:** PM Agent
**Date:** 2026-06-25

**Design phase authority:**
- `docs/process/sprint-plans/m17-sprint-plan.md §G2 Phase sequencing detail` — three
  journeys, three personas, BPO accepts Phase 1 before Phase 2 begins
- `docs/process/sprint-plans/m17-sprint-plan.md §Four-Agent Consultation Summary` —
  Design Thinking cognitive task analysis, UX Designer journey specification,
  Customer Agent MVS, Architect ARCH-REVIEW-007 assessment
- ARCH-REVIEW-007 (`docs/architecture/reviews/ARCH-REVIEW-007-milestone15.md §Binding
  decisions`) — N≤2/fixture in COMPARE_VIEW is the current architectural constraint;
  N>2 deferred explicitly to a future architecture decision with UX evidence
- `docs/ux/information-hierarchy.md` — Zone 1A/1B/1D cognitive task contracts
- `docs/ux/north-star.md` — Mode-specific primary cognitive task (Mode 2: threshold-safe
  path construction; Mode 3: real-time steering)
- `docs/ux/personas.md §Persona 1, §Persona 3, §Persona 5` — Lucas (Persona 1),
  Andreas (Persona 3), Aicha (Persona 5)

**Producing agents:**
- **Artifact 1:** UX Designer Agent — UX journey wireframes + zone layout specification
  for N=2/3/5 comparison
- **Artifact 2:** Customer Agent — Persona minimum viable story (Lucas / Aicha / Andreas)
  for Demo 7 Act 2 Zambia three-scenario scenario
- **Artifact 3:** Architect Agent — ARCH-REVIEW-007 N>2 architecture assessment + ADR
  determination

---

## 2. Persona Trace Elements Targeted

### Primary persona — Aicha Mbaye (Persona 5 — Finance Minister / Senior Ministry Official)

**P-1 — Persona served:**
Persona 5 — Finance Ministry Senior Official (Finance Minister or Deputy). Aicha must read
the comparison result within 90 seconds — without the presenter's narration and without prior
analytical preparation. She needs one clear answer: which option is least damaging to the
bottom quintile? Multi-scenario comparison is not a UX luxury for Aicha — it is a negotiating
necessity when three IMF conditionality packages are on the table simultaneously.

**P-2 — Entry state:**
Reactive. Aicha is at the table. Creditor side has proposed three programme options with
different conditionality structures. She has less than 90 seconds to form and state a
distributional preference. The comparison must be legible at glance level — option
identification without terminal labels or annotation is an acceptable failure.

**P-3 — Journey reference:**
Journey B Step 3 [Near-Term-Gap GA-B3]: Reactive defence of distributional output.
Aicha must read the bottom-quintile comparison across scenarios — which option crosses
the poverty headcount CRITICAL threshold, which does not — from the primary viewport at
the current step. Current tool supports N=2; Aicha's use case requires N=3.

**P-4 — Time/interaction ceiling:**
90 seconds; zero drawer interactions required. The three-scenario comparison must deliver
Aicha's question — "which option is least harmful to Q1?" — from primary viewport
observation alone. Aicha does not operate the tool at the table.

**P-6 — Negotiating leverage delivered (Persona 5 analogue):**
The design document specifies the argument. After Phase 3 implementation: "Under Option C,
the bottom income quintile avoids the poverty headcount CRITICAL threshold for the first
four programme quarters. Options A and B both cross the threshold at step 2. You can see
this on the screen." Aicha can state this from the primary viewport within 90 seconds,
without the analyst who built the scenario being required to narrate.

**P-7 — North star capability delivered:**
After Phase 3 implementation derived from this design, Aicha in the Reactive entry state
can identify the least-damaging restructuring option for Q1 by reading the primary viewport —
from a three-scenario Zone 1A trajectory display and a per-scenario Zone 1B threshold
crossing summary — within 90 seconds and without specialist narration. The comparison
capability that was previously limited to N=2 now supports the Zambia Demo 7 Act 2
three-restructuring-option scenario that represents Aicha's canonical use case.

---

### Secondary persona — Lucas Ferreira (Persona 1 — IMF Programme Analyst)

**P-1:** Lucas uses the three-scenario comparison to reproduce and challenge programme
alternatives presented by creditor-side analysts. His credibility gate: can he show
that Option B produces a worse Q1 poverty trajectory than Option A in the first four
steps — from simulation data accessible to both sides of the table — without requiring
the creditor side to have access to his modelling environment?

**P-4 — Time/interaction ceiling:**
No fixed ceiling for Preparatory entry state. Lucas builds the comparison during
preparation; the constraint is that the comparison must be fully set up (all three
scenarios loaded, Zone 1A rendering N=3) within a single preparation session.

**P-7:** After Phase 3 implementation, Lucas can load three restructuring scenarios for
the same entity, place them in comparison mode, and cite the specific step at which each
scenario's Q1 poverty headcount trajectory diverges — using the Zone 1A trajectory display
and Zone 1B per-scenario threshold crossing summary. The comparison is reproducible: the
same three-scenario setup produces the same display from the same data inputs, allowing
Lucas to share the comparison state with the creditor-side analyst for validation.

---

### Tertiary persona — Andreas Petrakis (Persona 3 — Political Advisor)

**P-1:** Andreas uses the Zone 1D PSP comparison across three scenarios to identify which
option has the highest programme survival probability — to build a political feasibility
brief before the negotiating session. PSP comparison across N=2 is currently possible;
N=3 extends this to the full restructuring option set.

**P-7:** After Phase 3 implementation, Andreas can read a per-scenario PSP value in Zone
1D for all three active scenarios simultaneously. "Option A: 62% / Option B: 44% / Option
C: 51% — Option A has highest survival probability." The design must make this comparison
readable without Andreas performing arithmetic or navigating between scenario views.

---

## 3. Design Artifact Deliverable State

> *G2 Phases 1 and 2 produce design documents, not application code. The observable states
> below are the design documents themselves. The test for each: can the Business PO (Phase 1)
> or Architect (Phase 2) assess this artifact by reading the file — without consulting the
> authoring agent, reading the simulation engine code, or referencing this intent document
> for clarification?*

### 3.1 Primary deliverable state — Phase 1

Both design artifacts exist as committed files at
`docs/ux/design-thinking/multi-scenario-comparison/`:

1. `ux-journeys-n3.md` — UX Designer Agent
2. `persona-mvs-n3.md` — Customer Agent

Each artifact is self-contained: a reader who opens the file for the first time can determine
what the three-scenario comparison must show in the primary viewport, and for which persona,
without consulting the authoring agent or reading the simulation engine.

### 3.2 Required content per Phase 1 artifact

**Artifact 1 — UX journeys: `ux-journeys-n3.md`** (UX Designer Agent)

Three journeys mapped in sufficient visual and interaction detail to serve as an
Architecture Review input. Required elements:

**Journey 1 — Scenario Setup:** How does the user create or select three scenarios for
comparison? Required: name the specific UI mechanism (scenario selector extension,
new entry point, Mode 2 branching extension, or other); show the step sequence
from "two scenarios active" to "three scenarios active" with at least three named
interaction steps; state the maximum number of active scenarios supported (N=3 confirmed,
N=5 target, N>5 deferred); specify the Zone 1D behavior when three scenarios are active
(does entity attribution show separately per scenario?).

**Journey 2 — Primary Viewport in Comparison Mode:** Zone 1A with N=3 trajectory sets.
Required: specify the visual differentiation strategy for three trajectories in Zone 1A —
color channel, line-style channel (solid / dashed / dotted), and terminal endpoint label
are the three available channels; the journey must commit to which combination is used
and confirm it is readable at 1280×800 (the Demo 7 presentation viewport) without a
color-blind accessibility failure; confirm the same differentiation strategy scales to
N=5 (target) without becoming unreadable; address the COMPARE_VIEW binding constraint
from ARCH-REVIEW-007 explicitly — does N>2 extend the existing compare-mode overlay
contract, or does it require changes to the composite_score rendering path?

**Journey 2 continued — Zone 1B and Zone 1D in comparison mode:** The journey must
specify whether Zone 1B threshold crossings are displayed per-scenario (Scenario A
crosses at step 2; Scenario B crosses at step 4) or as a merged union (any scenario
that crosses is shown). The journey must specify whether Zone 1D PSP is displayed
per-scenario or as a single PSP for the active scenario only. These are the two
most architecturally consequential UX decisions in the multi-scenario scope.

**Journey 3 — Threshold Comparison:** The comparison interaction when Aicha's question
("which option avoids Q1 poverty headcount CRITICAL?") must be answerable from the
viewport. Required: name the viewport zone(s) where Aicha finds the answer and the
maximum number of visual elements she reads; confirm zero interaction requirement
(she must not be required to navigate between scenario views or open a drawer);
show the concrete display for the Zambia Demo 7 Act 2 scenario — three restructuring
options, step 4, Q1 poverty headcount threshold — as a literal text block (not prose
description) specifying what Zone 1A and Zone 1B show simultaneously.

**Zone layout for N>2 (any journey):** State the viewport constraint at which the N>2
display degrades — what fails at 1280×800, at 1024×768. The Frontend Architect needs
this to assess TrajectoryView N>2 feasibility before Phase 2 architecture assessment.

**Silent failure for Artifact 1:** A journey document that describes the visual strategy
in prose but does not show a literal wireframe or text block for the Zambia Demo 7
Act 2 scenario (three options, step 4, Q1 threshold) does not satisfy Journey 3.
After reading the document, a QA reviewer must be able to complete: "In a ZMB Mode 2
three-scenario comparison at step 4, Zone 1A shows [specific visual treatment] and
Zone 1B shows [specific per-scenario or union content]." If the reviewer cannot complete
this sentence from the document alone, the document is incomplete.

---

**Artifact 2 — Persona MVS: `persona-mvs-n3.md`** (Customer Agent)

Minimum viable story specification per persona, anchored to the Zambia Demo 7 Act 2
scenario. Required elements:

**Lucas (Persona 1) MVS:** The specific comparison argument Lucas can make in the
negotiating session — naming the three scenarios (or Option A/B/C placeholders), the
specific step, the specific indicator, and the specific delta — using only the
primary viewport. The MVS must confirm that the comparison is reproducible: the same
three-scenario setup yields the same display for both sides of the table.

**Aicha (Persona 5) MVS:** The 90-second legibility gate — a literal description of
what Aicha sees when she looks at the primary viewport at step 4 of the Zambia
three-scenario comparison, and the specific statement she can make from that observation.
"The least harmful option is [label]" must be answerable without narration. The MVS
must confirm that the Zone 1A trajectory labels and Zone 1B per-scenario summary
together provide the answer — or name which element is the anchor.

**Andreas (Persona 3) MVS:** The specific PSP comparison statement Andreas can make
from Zone 1D — three scenario labels with three PSP values. Name the Zone 1D display
contract that delivers this and whether it requires a structural change to Zone 1D or
an extension of the existing per-scenario PSP rendering.

**Minimum implementation scope for Demo 7:** A named section titled "Minimum Viable
N=3 Implementation" (or equivalent) that states the minimum feature set required to
support all three personas' MVS at Demo 7 — not "what comparison ideally looks like"
but "what must ship for Demo 7 Act 2 to work without the presenter narrating the
answer for Aicha." The BPO uses this section to assess whether a partial implementation
is sufficient for M17, and what the M18 carry scope is.

**Silent failure for Artifact 2:** A MVS document that describes persona needs in
general terms without naming the specific display element, step, and indicator for
each persona does not satisfy this requirement. After reading the document, the BPO
must be able to confirm or deny: "Aicha can read which restructuring option avoids Q1
crossing at step 4, from Zone 1A + Zone 1B, without narration, in under 90 seconds."
If the document does not contain enough specificity to make this confirmation, it is
incomplete.

---

### 3.3 Required content — Phase 2 artifact

**Artifact 3 — Architecture assessment: `docs/architecture/reviews/ARCH-REVIEW-007-m17-n3-assessment.md`** (Architect Agent)

Supplemental architecture assessment document to ARCH-REVIEW-007, produced with Phase 1
UX journeys in hand. Required elements:

**ARCH-REVIEW-007 binding constraint revisited:** The current constraint is:
"COMPARE_VIEW N≤2/fixture" — established at Phase 2 review 2026-06-22. The assessment
must state explicitly whether the N>2 UX journey from Artifact 1 is achievable within
the existing Zone 1A composite_score rendering path and compare-mode overlay contract,
or whether structural changes are required to the rendering architecture.

**Three architecture questions addressed (per sprint plan):**
1. Does Zone 1A N>2 require changes to the composite_score rendering path, or only to
   the compare-mode overlay?
2. Does Zone 1B per-scenario threshold crossings require a new backend data structure
   in the compare endpoint, or a frontend composition from the existing `threshold_crossings`
   field (delivered in G9)?
3. Does Zone 1D per-scenario PSP require a new endpoint or a client-side multi-scenario
   store structure?

**ADR determination:** Explicit answer to one of three options:
(a) N>2 requires structural changes to Zone 1A architecture — ARCH-012 (or ARCH-013
    depending on #1252 outcome) must be authored and accepted before Phase 3
    implementation PR opens
(b) N>2 is a straightforward compare-mode extension within the existing component
    boundary — architecture review note on #394 sufficient; no new ADR required;
    Phase 3 sprint entry may proceed
(c) Mixed — Zone 1A extension is within boundary (no ADR) but Zone 1B or Zone 1D
    changes require an ADR; specify which sub-component triggers the ADR requirement

**Phase 3 implementation preconditions:** A named section "Phase 3 Implementation
Gate" listing the conditions that must be met before the Phase 3 sprint entry is
filed — including: #1249 (Zone 1A curve identifiability) merged; any required ADR
accepted; BPO acceptance of Phase 1 artifacts confirmed.

**Silent failure for Artifact 3:** An assessment that states "N>2 is more complex"
without committing to one of the three ADR determination options is incomplete. The
assessment must give the Architect's explicit recommendation: option (a), (b), or (c)
above. A recommendation that defers to "further study" is not an acceptable output.

---

## 4. Acceptance Criteria

> *Each criterion is reviewable by the BPO (Phase 1) or Architect (Phase 2) without
> reading any implementation code. An artifact that satisfies the AC can be assessed
> from the document alone. Phase 1 ACs are BPO acceptance criteria; Phase 2 AC is
> Architect acceptance criteria.*

### Phase 1 — Artifact 1 (`ux-journeys-n3.md`)

**AC-1 (Journey 1 — scenario setup mechanism named):**
`ux-journeys-n3.md` contains a Journey 1 section naming the specific UI mechanism by
which a user moves from two active scenarios to three active scenarios — whether by
extending the scenario selector, adding a "branch" action in Mode 2, or another named
mechanism. The step sequence (minimum three steps) is shown. The maximum supported N
is stated (N=3 confirmed, N=5 target). The Zone 1D entity attribution behavior with
three active scenarios is specified — either per-scenario or shared.

**AC-2 (Journey 2 — Zone 1A three-scenario differentiation strategy committed):**
`ux-journeys-n3.md` Journey 2 names the exact combination of visual channels used to
differentiate three trajectories in Zone 1A: which color palette is used for three
scenarios (naming specific colors, not "distinct colors"), whether line style
differentiation (solid / dashed / dotted) is added, and whether terminal endpoint
labels are added — with the reasoning for each choice. The document confirms the chosen
strategy is readable at 1280×800 in the Demo 7 presentation context. The document
confirms the same strategy scales to N=5 without a collapse in visual legibility.
A single color-only differentiation strategy that fails at 1280×800 presentation scale
does not satisfy this criterion.

**AC-3 (Journey 2 — Zone 1B per-scenario vs. union decision committed):**
Journey 2 explicitly commits to one of two Zone 1B display contracts for three-scenario
comparison:
(a) Per-scenario: threshold crossings are grouped by scenario label, so a crossing
    present in Scenario B but not A or C is attributed to Scenario B only
(b) Union: threshold crossings from any scenario are shown as a combined list, with
    scenario attribution via label

The rationale for the chosen option must reference the reading-order requirement
(Aicha reads the Zone 1B content to identify which scenario triggered a Q1 crossing —
the display must make scenario attribution unambiguous within her 90-second ceiling).
A document that describes both options without committing to one does not satisfy AC-3.

**AC-4 (Journey 2 — Zone 1D per-scenario PSP decision committed):**
Journey 2 explicitly commits to one of two Zone 1D PSP display contracts for
three-scenario comparison:
(a) Per-scenario: three PSP values displayed simultaneously with scenario labels
(b) Active-scenario only: PSP shown for whichever scenario is currently focused
    or hovered, with a mechanism to switch

The rationale must reference Andreas's use case — he needs to compare PSP across all
three scenarios without switching views. A single active-scenario display (option b)
must show how Andreas can complete his PSP comparison without holding all three values
in memory simultaneously.

**AC-5 (Journey 3 — Aicha's question answered without narration):**
Journey 3 contains a literal text block or annotated wireframe showing what Aicha sees
in the primary viewport at step 4 of the ZMB Mode 2 three-scenario comparison, with Q1
poverty headcount trajectory active. The block must show Zone 1A content and Zone 1B
content simultaneously (as they appear on screen together, not separately). From this
block, a reviewer must be able to confirm: "Aicha can identify which scenario avoids
Q1 CRITICAL crossing at step 4 without narration." A prose description of the display
does not satisfy AC-5.

Example of what does NOT satisfy AC-5:
> "Zone 1A will show three clearly differentiated trajectories so Aicha can identify
> which option is least harmful."

Example of what satisfies AC-5 (illustrative, not prescriptive — the actual content
is a design decision for the UX Designer):
```
Zone 1A | Step 4 | ZMB Mode 2 — Restructuring Comparison
───────────────────────────────────────────────────────────
  ╭──── Option C ⬤ (solid blue) — Q1 composite: 0.72 [above floor]
  │──── Option A ◆ (dashed red) — Q1 composite: 0.58 [below floor]
  ╰──── Option B ▲ (dotted orange) — Q1 composite: 0.51 [below floor]

Zone 1B | Threshold crossings at step 4:
  CRITICAL  Option A — Q1 Poverty headcount — crossed at step 2
  CRITICAL  Option B — Q1 Poverty headcount — crossed at step 3
  [Option C — no Q1 crossing through step 8]
```

**AC-6 (COMPARE_VIEW architectural position stated):**
`ux-journeys-n3.md` contains an explicit architectural position statement — not a
recommendation to the Architect, but the UX Designer's assessment of whether the
proposed Zone 1A N>2 differentiation strategy (from AC-2) operates within the existing
COMPARE_VIEW compare-mode overlay contract (no structural rendering change required)
or requires changes to how the composite_score rendering path processes multiple
scenario curves. The UX Designer's position does not determine the architectural
conclusion — that is Artifact 3 — but the Architect cannot produce a complete Phase 2
assessment without the UX Designer's view on whether their design requires a new
rendering mechanism or extends the existing one. A journey document that says "this
is an architecture question" without providing the UX position fails AC-6.

---

### Phase 1 — Artifact 2 (`persona-mvs-n3.md`)

**AC-7 (Lucas MVS — specific comparison argument named):**
`persona-mvs-n3.md` contains a Lucas (Persona 1) section that names the specific
comparison argument Lucas can make in the negotiating session from a three-scenario
ZMB comparison: citing the specific step number, the specific indicator (poverty
headcount, school enrollment rate, or other — the MVS must choose), and the direction
of divergence between the three options. "Lucas can compare three options" does not
satisfy AC-7. "At step 4, Option C's Q1 poverty headcount trajectory is 0.14pp higher
than Option A and 0.21pp higher than Option B" is the specificity level required.

**AC-8 (Aicha MVS — 90-second legibility gate confirmed):**
The Aicha section confirms: (a) which display element is Aicha's primary anchor for
identifying the least-harmful option — Zone 1A terminal labels, Zone 1B crossing
summary, or other — naming it specifically; (b) that the answer is available from the
primary viewport at step 4 without Aicha navigating between views; (c) a literal
statement of what Aicha says after reading the display — not a template but a concrete
sentence citing the option name or label she reads on screen. "Aicha can identify the
best option within 90 seconds" does not satisfy AC-8.

**AC-9 (Andreas MVS — per-scenario PSP comparison stated):**
The Andreas section states: the three PSP values Aicha's team can read for the Zambia
Demo 7 Act 2 three-scenario comparison at a specific step (the step where PSP divergence
is most pronounced, named by the Customer Agent from the simulation engine's expected
output range for ZMB conditionality scenarios); the Zone 1D display mechanism that
delivers this (per-scenario PSP values simultaneously visible, or a mechanism for
sequence); and the political statement Andreas can make from these values — a literal
sentence, not a template.

**AC-10 (Minimum viable N=3 implementation scope named):**
`persona-mvs-n3.md` contains a section titled "Minimum Viable N=3 Implementation for
Demo 7 Act 2" (or equivalent) that names the minimum feature set required for all three
personas' MVS to be satisfied at Demo 7. Specifically: (a) which zones must support N=3
comparison (Zone 1A required / Zone 1B required / Zone 1D required or optional), (b)
whether the scenario setup journey from AC-1 is required or whether a pre-configured
three-scenario fixture is sufficient for Demo 7, and (c) what is explicitly deferred
to M18 (e.g., N=4 and N=5 support; Mode 3 multi-scenario branching; full scenario
setup UI as opposed to a fixed fixture). The BPO uses this section to determine whether
a partial Phase 3 implementation closes M17 with BPO acceptance.

---

### Phase 2 — Artifact 3 (`ARCH-REVIEW-007-m17-n3-assessment.md`)

**AC-11 (ARCH-REVIEW-007 constraint explicitly revisited):**
`docs/architecture/reviews/ARCH-REVIEW-007-m17-n3-assessment.md` contains a section
titled "N>2 Assessment Against ARCH-REVIEW-007 Binding Constraint" (or equivalent)
that quotes the original binding constraint ("COMPARE_VIEW N≤2/fixture") and states
whether the UX journey in Artifact 1 operates within that constraint or requires it
to be revised. The assessment must be specific: does Zone 1A N>2 operate within
the existing compare-mode overlay rendering path, or does it require changes to
`composite_score` aggregation, curve assignment logic, or TrajectoryView component
state that were not contemplated by ARCH-REVIEW-007?

**AC-12 (ADR determination committed — one of three options):**
The assessment commits to one of three options per §3.3 above: (a) new ADR required
before Phase 3 PR opens, (b) architecture review note on #394 is sufficient, or (c)
mixed. The option chosen is stated explicitly as an "ADR Determination" header entry.
A recommendation that defers to "pending further discussion" or "requires EL input
before determination" without a Architect-authored provisional position is incomplete.
The Architect's provisional position must be present even if EL review changes it.

**AC-13 (Phase 3 implementation gate checklist present):**
The assessment includes a section titled "Phase 3 Implementation Gate" listing the
conditions that must be confirmed before the Phase 3 sprint entry is filed: (1) #1249
merged; (2) BPO acceptance of Artifacts 1 and 2 on record; (3) any required ADR from
AC-12 accepted; (4) any Zone 1B or Zone 1D backend data structure changes clarified
(from Q2 and Q3 assessment in §3.3). The list is exhaustive — an unchecked item in
this gate prevents the Phase 3 sprint entry from being filed.

---

## 4b. Visual Spec (before/after)

**AC-5 — Journey 3: what Aicha's viewport must look like**

The visual spec requirement is inverted for a design-intent: the UX Designer must produce
the before/after spec in Artifact 1. This section establishes what the UX Designer must
include in the Artifact 1 spec.

**Before (current N=2, Zone 1A):**
```
Zone 1A | Step 4 | ZMB Mode 2 — current two-scenario comparison
───────────────────────────────────────────────────────────────
  ╭──── Scenario A ⬤ (solid) — composite: 0.58
  ╰──── Scenario B ◆ (ghost) — composite: 0.51

Zone 1B | Threshold crossings:
  CRITICAL  Q1 Poverty headcount — crossed at step 2
  (scenario attribution: Scenario A; Scenario B not shown separately)
```

The "before" is the current implementation. The UX Designer's `ux-journeys-n3.md`
Journey 3 must show the N=3 equivalent that makes scenario attribution unambiguous
for Aicha's question — as a literal text block, not prose description.
The design may differ from the illustrative N=3 example in §4 AC-5 — what matters
is that it is literal, scenario-attributed, and answerable without narration.

**After (N=3, Zone 1A and Zone 1B, as specified by UX Designer):**
To be produced in `ux-journeys-n3.md` Journey 3. The spec must include:
- Viewport: 1280×800 (Demo 7 presentation context)
- Zone: Zone 1A and Zone 1B (both, as they appear on screen simultaneously)
- `data-testid` anchors for Zone 1A scenario curves (e.g.,
  `data-testid="zone1a-curve-scenario-{id}"`) and Zone 1B per-scenario rows
  (e.g., `data-testid="zone1b-threshold-row-scenario-{id}"`) — so that the Phase 3
  implementation-intent QA Lead can author Playwright tests from Artifact 1 without
  reading frontend source code
- The specific N=3 scenario labels as they appear on screen (not database IDs)

---

## 5. Kryptonite Constraint Check

**Does the design document's primary observable state require specialist mediation for
Persona 5 to act on it in the Reactive entry state (90-second ceiling)?**

`[ ]` Applied to Artifact 1 — UX journeys:

The kryptonite constraint is the primary design discipline for Journey 3. The design
must specify a three-scenario comparison that Aicha — who is at the table, not
operating the tool — can read without an analyst narrating the answer. Any design
that requires:
- Opening a drawer to see per-scenario Zone 1B threshold crossings
- Hovering over Zone 1A curves to read scenario labels
- Navigating between scenario views in Zone 1D to compare PSP values
fails the kryptonite constraint for Aicha's 90-second Reactive ceiling.

The UX Designer must confirm in `ux-journeys-n3.md` §Kryptonite Check (or equivalent
section) that the Zone 1A + Zone 1B composite visible at the primary viewport at step 4
answers Aicha's question — "which option is least harmful to Q1?" — without any of the
above interactions. If the design requires any of these, the UX Designer must either
revise the design or document the asymmetry gap and route to EL for a scope decision.

`[ ]` Applied to Artifact 2 — Persona MVS:

The Customer Agent's MVS assessment (AC-8) is the Layer 3 quality gate for Artifact 1.
If the Customer Agent's assessment concludes that Aicha's MVS cannot be satisfied within
the Reactive ceiling at N=3 — that the comparison is inherently too information-dense
for 90 seconds without narration — that is a design finding that triggers either:
(a) UX redesign of Journey 3 to meet the ceiling, or
(b) A scoped-down MVS that identifies the minimum N=3 display that is legible
    within 90 seconds and defers richer comparison to Mode 3 (which has a longer
    ceiling).

The Customer Agent names explicitly in `persona-mvs-n3.md` which option applies and why.
"Multi-scenario comparison is complex" is not a kryptonite assessment.

`[ ]` Applied to Artifact 3 — Architecture assessment:

Artifact 3 is an internal architecture document — its audience is the Phase 3
implementing agent and the EL, not Aicha. The kryptonite constraint does not apply
to Artifact 3 directly. However: if the architecture determination from AC-12 requires
a data contract that cannot be met by the existing compare endpoint within the Phase 3
timeline, the Architect must note the constraint and route to the BPO for a scope
decision on Phase 3 MVS vs. full N>2 implementation.

---

## 6. Out of Scope

**Phase 3 implementation code:** No frontend or backend code changes are produced in
G2 Phase 1 or Phase 2. An agent reading this intent document and opening a feature PR
has exceeded scope. Phase 3 has its own sprint entry gate.

**N>3 support (N=4, N=5 target) as Phase 3 scope:** The Minimum Viable N=3
Implementation for Demo 7 Act 2 is the Phase 3 delivery target for M17 (if
implementation completes). N=4 and N=5 support is the extended target but is explicitly
deferred to M18 if Phase 3 carries there. Artifact 1 must confirm the design scales
to N=5 — but Phase 3 implementation does not need to deliver N=5 in M17.

**Mode 3 multi-scenario branching (active control):** Mode 3 branching across three
independent control trajectories is out of scope for #394. The current issue is
Mode 1 and Mode 2 N>2 comparison. Mode 3 branching extension is M19+ scope.

**ADR authorship (Phase 2 is an assessment, not an ADR):** Artifact 3 is an architecture
assessment note. It may conclude that a new ADR (ARCH-012 or ARCH-013) is required —
but Artifact 3 does not author that ADR. The ADR authorship is a separate Phase 3
prerequisite sprint group activity, triggered by AC-12 option (a).

**Zone 1B proportional allocation (#1252 / G3):** The Zone 1B layout when both the MDA
alert panel and the cohort impact section are populated is G3 scope. If the G2 UX
journey specifies a Zone 1B per-scenario display contract that conflicts with the G3
proportional allocation brief, the UX Designer notes the conflict in Artifact 1 and
routes to EL for resolution before Phase 3 sprint entry. G2 does not resolve G3 scope.

**DEMO6 CRITICAL polish (#1249, #1250, #1253):** G4 scope. G2 Journey 3 Zone 1A
wireframe should be designed knowing that #1249 (Zone 1A curve identifiability for N=2)
will be merged before G2 Phase 3 implementation begins — but G2 does not specify or
implement the N=2 fix. The UX Designer notes in Journey 2 whether the N=3 differentiation
strategy from AC-2 builds on the N=2 fix from #1249 or is independent of it.

**G3 Zone 1B ADR authorship:** G2 UX journey may feed into G3 because the per-scenario
Zone 1B display contract in Journey 2 affects the Zone 1B layout question. If it does,
Artifact 1 explicitly notes the G3 dependency and what the G3 UX brief must resolve
before G2 Phase 3 implementation can proceed. G2 does not own G3 scope.

**Scenario setup UI implementation:** The Journey 1 UI mechanism (how a user creates a
third scenario) may reveal scope that exceeds M17 Phase 3 capacity. The MVS in Artifact 2
AC-10 determines whether a pre-configured three-scenario fixture is sufficient for
Demo 7 Act 2 or whether the full scenario setup journey must be implemented. If a fixture
is sufficient for Demo 7, the scenario setup UI is M18 scope.

---

## 7. Review Obligation

> *G2 Phases 1 and 2 are design-only. No QA Lead test authorship step applies to Phase 1
> or Phase 2 artifacts. QA test authorship is a Phase 3 obligation, triggered at Phase 3
> sprint entry and governed by the Phase 3 implementation-intent document. The review
> obligation for Phase 1 and Phase 2 is described below.*

### Phase 1 review — Business Product Owner

**Reviewer:** Business Product Owner
**Scope:** Confirm AC-1 through AC-10 are satisfied — that both Phase 1 artifacts contain
the specific content required and that the minimum viable N=3 story (AC-10) is coherent
and consistent with the BPO's Demo 7 prioritization position (see `docs/process/sprint-plans/m17-sprint-plan.md §Business Product Owner — Demo 7 value prioritization`).

**Specific BPO review questions:**
1. Does Journey 3 (AC-5) show a display that Aicha can read without narration within 90
   seconds, or does the design require the presenter to point at trajectories?
2. Is the Minimum Viable N=3 Implementation scope (AC-10) achievable in Phase 3 if
   Phase 3 begins immediately after #1249 merges — or is Phase 3 M18 scope?
3. Is the MVS for Aicha (AC-8) consistent with the BPO's northstar framing: "The Zambia
   three-scenario comparison is Demo 7 Act 2. Aicha must read it without narration."?

**Review deadline:** Before Phase 2 begins (before Artifact 3 is authored). The Architect
cannot produce a complete Phase 2 assessment without BPO acceptance of Phase 1.

**BPO acknowledgment:**
`[ ]` Business PO: AC-1 through AC-10 satisfied. Minimum N=3 Implementation scope
      reviewed and confirmed. Phase 2 may begin. [Date]

---

### Phase 2 review — Architect

**Reviewer:** Architect Agent
**Scope:** Confirm AC-11 through AC-13 are satisfied — that Artifact 3 provides an
explicit ARCH-REVIEW-007 revisitation, a committed ADR determination, and a Phase 3
implementation gate checklist.

**Specific Architect review questions:**
1. Does AC-11 provide enough architectural specificity for the Phase 3 implementing
   agent to understand the component boundary before beginning implementation?
2. If option (a) is chosen in AC-12 (new ADR required): is an expedited ADR panel
   feasible before G2 Phase 3 sprint entry? Or does this push Phase 3 to M18?
3. Does AC-13 name all blocking conditions — are there additional Zone 1B or Zone 1D
   data contract dependencies not captured?

**Review deadline:** Before Phase 3 sprint entry is filed.

**Architect acknowledgment:**
`[ ]` Architect: AC-11 through AC-13 satisfied. ADR determination recorded.
      Phase 3 implementation gate confirmed. [Date]

---

### Phase 3 obligations (deferred)

**QA Lead:** QA Lead Agent (Frontend for E2E; CM or backend for any API changes)
**Test authorship deadline:** Before Phase 3 implementation PR opens — governed by the
Phase 3 implementation-intent document, not this document
**Test file location (anticipated):** `frontend/tests/e2e/m17-g2-multi-scenario.spec.ts`
**Note:** Phase 3 ACs and test file are specified in the Phase 3 implementation-intent
document, which is authored after Phase 1/2 design artifacts are accepted. That document
derives its ACs from the specific zone layouts and `data-testid` anchors committed in
Artifact 1 — particularly the Zone 1A scenario curve selectors and Zone 1B per-scenario
row selectors required by AC-5 (§4b).

---

### Document locations

- `docs/ux/design-thinking/multi-scenario-comparison/ux-journeys-n3.md` — Artifact 1 (UX Designer)
- `docs/ux/design-thinking/multi-scenario-comparison/persona-mvs-n3.md` — Artifact 2 (Customer Agent)
- `docs/architecture/reviews/ARCH-REVIEW-007-m17-n3-assessment.md` — Artifact 3 (Architect)

---

*Design intent version: 2026-06-25. Issue #394 authorized as M17 G2 Wave 2 parallel design
track per `docs/process/sprint-plans/m17-sprint-plan.md §Sprint Groups`. No sprint entry
required for Phase 1 or Phase 2. Phase 3 requires a separate sprint entry document and a
separate implementation-intent document — filed when BPO acceptance of Phase 1/2 is on record
and all Phase 3 gate conditions in AC-13 are satisfied. Authoring authority: PM Agent (this
document); UX Designer Agent (Artifact 1); Customer Agent (Artifact 2); Architect Agent
(Artifact 3). BPO review of Phase 1 required before Phase 2 begins. Phase 3 implementation
gate: #1249 merged; BPO acceptance of Artifacts 1 and 2 confirmed; ADR determination from
Artifact 3 resolved. Full lifecycle authority: `docs/process/agent-execution-lifecycle.md`.*
