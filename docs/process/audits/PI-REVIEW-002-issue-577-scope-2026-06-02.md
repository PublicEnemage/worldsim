# PI-REVIEW-002 — Issue #577 Scope Assessment: [Phase-3-TBD] Stories

**Date:** 2026-06-02
**Reviewed by:** Process Integrity Agent
**Activation:** `Process Integrity Agent: REVIEW — Issue #577 scope`
**Scope:** Four [Phase-3-TBD] stories from `docs/ux/user-stories-public-advocacy-m10.md`
(Issue #576): US-039, US-042, US-043, US-048. Architectural classification and DIC panel
composition recommendations as input to Issue #577 DIC panel activation.

---

## Required Reading Completed

Before this document was drafted, the following were read in full in order:

1. `CLAUDE.md` — Project constitution; UX Architectural Commitments; Platform Principle; No False Precision; three interaction modes
2. `docs/architecture/simulation-framework.md` — Three modes, failure architecture, simulation engine structure, key use cases
3. `docs/ux/information-hierarchy.md` — Zone hierarchy; disclosure zones; COMPARE_VIEW conditional; Control Plane Reserved Zone
4. `docs/ux/user-stories-public-advocacy-m10.md` — All 19 stories; full text of US-039, US-042, US-043, US-048; Panel Decisions 1–4
5. `docs/process/agents.md` — PI Agent REVIEW activation; DIC roster; Architecture Review Facilitator; Council Orchestrator
6. `docs/process/agent-raci.md` — File ownership; RACI matrix; decision-type grounding

**File authority verified:** PI Agent holds R on `docs/process/audits/` by working agreement
(process audit trail ownership). No other agent holds R on this directory. Required
Consultant (C): EL (informed of findings). This document does not require EL pre-approval to
create — it is a research artifact, not an architectural decision.

---

## Assessment Frame

The four [Phase-3-TBD] stories were classified by the PO Agent (Issue #576, Panel Decision 1)
as having "no current architectural path." This review applies a finer classification to each,
using the four categories posed in the activation prompt:

| Category | Definition |
|---|---|
| **New simulation mode** | Requires a fourth interaction mode with its own cognitive task definition, instrument layout, and mode indicator label. High architectural cost. Requires ADR. |
| **Extension of existing mode** | Adds capability within Mode 1, 2, or 3 without requiring a new mode state or cognitive task. Moderate cost. May require ADR amendment. |
| **New Zone 2 surface** | A new rendering component in the secondary (one-click) disclosure zone. Does not require a new mode. May require backend API extension. |
| **Standalone tool** | An export path, report generator, or data entry form that operates on existing simulation output without altering the instrument cluster. Lowest architectural cost. |

Three additional questions applied per story:

1. **Platform Principle test:** Does the story require a scenario-specific branch or is it
   a data/rendering concern that works across all scenarios?
2. **No False Precision test:** Does the story's acceptance criteria preserve epistemic
   disclosure (confidence tiers, uncertainty, synthetic provenance) or does it suppress it?
3. **Milestone placement:** Based on mode and architectural scope, which milestone is the
   correct home?

---

## Story Assessments

### F-001 — US-039: Real-Time Parameter Change (Mode 3)

**Story:** As James Ochieng in Mode 3 Active Control, change a fiscal consolidation parameter
in real time without creating a new scenario.

**Classification:** Extension of existing Mode 3

**Basis:**

Mode 3 (Active Control) is an existing, architecturally defined mode. The control plane
reserved zone is already sized at 280px and allocated in the M9 layout (US-027, US-028).
US-039 requires populating the control plane with a fiscal consolidation instrument form —
this is exactly the use case the reserved zone was sized to serve.

No new mode is required. No new zone is required. The capability is an implementation
of the control plane's intended purpose, not a structural extension of the platform.

**What does not exist yet:**

1. **Control plane form content** — The control plane is reserved but empty in Mode 1 and
   Mode 2 (by design). In Mode 3, it is currently unimplemented. US-039 requires
   implementing one concrete instrument: a fiscal consolidation parameter input.

2. **Mid-scenario parameter recomputation path** — The engine currently accepts inputs at
   scenario creation. Whether the engine can accept a parameter change mid-scenario (without
   creating a new scenario object) and recompute from a branch point is not documented.
   This is the critical architectural unknown. Two paths exist:
   - *Branch-and-recompute:* The engine holds the baseline state snapshot and runs a new
     computation from it with the modified parameter. This is the intended Mode 3 behavior
     (US-007: ghost baseline curves appear at first control input). The question is whether
     this is already supported or requires new engine plumbing.
   - *New scenario creation under the hood:* The frontend creates a new scenario implicitly,
     copies baseline state, and advances it. This would technically satisfy the acceptance
     criteria but is an implementation smell — the user should not feel a scenario creation
     boundary.

3. **Journey map gap** — The story's journey anchor reads "Journey F (Mode 3 extension, not
   yet in current journey map)." Journey F in `docs/ux/user-journeys.md` covers Mode 2
   only (Legislative Brief). A Mode 3 journey is not in scope for M10. This is not a
   finding about the story — it is a scoping signal: US-039 has no journey to anchor to
   until Mode 3 is mapped.

**Platform Principle test:** Passes. Fiscal consolidation parameter input is a data concern.
Any scenario with a fiscal instrument can use the control plane form. No scenario-specific
branch required.

**No False Precision test:** Passes. US-039 acceptance criteria carry through the ghost
baseline / divergence fill contract from US-007 and US-008. Epistemic contrast between
baseline and modified trajectory is preserved.

**Milestone placement:** M12 — "Active Control and External Sector." Mode 3 implementation
is the M12 core deliverable per the roadmap. US-039 requires Mode 3 to exist as a buildable
surface before the control plane can be populated. Building the control plane form in M10 or
M11 without Mode 3 instrumentation is premature.

**Exception path:** If the DIC panel finds that a simplified Mode 2 variant of parameter
change (creating a new scenario implicitly, with the new scenario shown in COMPARE_VIEW)
serves James's hearing use case adequately, that variant could be scoped as an M11 Near-Term-Gap.
The distinction is: does the parliamentary economist need real-time (<10s) in-session recomputation
(Mode 3 behavior), or does he need quick alternate scenario creation (Mode 2 behavior)?
This is a UX question, not an engine question.

**Panel required:** Architecture Review (TARGETED — Mode 3 control plane implementation
scope). Members: Architect Agent (R — scope decision), Chief Engineer (C — branch-and-recompute
engine capability), Frontend Architect (C — control plane form implementation path), UX
Designer (C — Mode 3 journey mapping requirement). DIC domain council not required for
the scope classification; DIC members may be consulted if the exception path (Mode 2
variant) is evaluated for adequacy for the parliamentary economist persona.

---

### F-002 — US-042: Observed-Actuals Input Overlay

**Story:** As Abena Osei, input observed actual spending values and have them overlaid on the
committed programme baseline trajectory in the instrument cluster.

**Classification:** New Zone 2 surface (data entry) + Zone 1 overlay (rendering) —
**NOT a new simulation mode**

**Basis:**

The story note correctly identifies three candidate approaches. This review assesses them:

**Option A — Mode 1 Extension:**

Mode 1 replays historical scenarios from configured fixtures. Observed actuals are genuinely
historical — the Ghana ECF ran; the spending happened. However, Mode 1 as currently
implemented requires a pre-baked fixture. There is no user-facing data entry path.

Extending Mode 1 to support live observed-actuals entry would require:
- A new data entry form in Zone 2 (or a modal) for per-step actual value input
- Fixture creation on the fly from user-entered data (bypassing the normal fixture pipeline)
- The resulting "historical" scenario would have unusual provenance (user-entered, not a
  registered source)

Assessment: Mode 1 extension is architecturally possible but epistemically awkward. The
Confidence Tier System requires source attribution. User-entered observed actuals are Tier 3
at best (primary source: the civil society monitor's records) but the provenance is not
registry-registered. This path requires the Data Quality Agent's input on whether user-entered
programme actuals can be handled within the existing tier framework.

**Option B — Mode 4:**

A new interaction mode with its own cognitive task ("accountability tracking — verifying
observed outcomes against committed baselines"). This is the highest architectural cost option.
Mode 4 would require:
- ADR (cannot be added without one)
- Cognitive task definition
- Mode indicator label
- Instrument layout specification
- Journey map entry

Assessment: Mode 4 is not warranted for this use case. The accountability tracking task
is not structurally different enough from Mode 2 + observed-actuals overlay to justify a
new mode. Mode 4 risks fragmenting the three-mode architecture that the entire instrument
cluster is designed around. This option is rejected on architectural grounds alone.

**Option C — Post-processing overlay (recommended):**

The committed programme baseline trajectory is produced by Mode 2 (Scenario A). The observed
actuals are external data entered by the user after the scenario is complete. The overlay
renders them as a distinct data series on the trajectory view without feeding them into the
simulation engine.

This is architecturally correct for a fundamental epistemic reason: **observed actuals are
not simulation outputs.** Feeding them into the engine as if they were simulated values would
conflate two epistemically distinct quantities — the model's prediction and the government's
reported expenditure. The No False Precision principle prohibits this conflation.

The post-processing overlay approach requires:
- A data entry form in Zone 2 (or a persistent panel below Zone 1) for per-step actual value
  input — the user enters step N → actual spending value pairs
- A new data series rendering on the trajectory view (Zone 1) showing observed actuals as
  distinct data points (e.g., filled circles rather than a curve, with a distinct color and
  a clear legend entry: "Observed actuals — SEND Ghana records")
- MDA alert comparison logic: the alert panel must evaluate the observed-actuals series against
  the MDA thresholds and show which thresholds are crossed in the actuals that are not in
  the simulation — this is an extension of the compare-view alert panel logic, not new logic
- Confidence tier for the actuals series: Tier 3 (primary source, user-entered) — displayed
  explicitly in the legend and in any alert that fires against the actuals series

**Platform Principle test:** Passes. The data entry form and overlay rendering work for any
Mode 2 scenario with spending indicators. No scenario-specific logic required.

**No False Precision test:** Passes if implemented as overlay. The actuals series carries
its own confidence tier and provenance label. The simulation curve and actuals series are
visually distinct. The alert panel distinguishes which alerts fire on simulation vs. actuals.

**Fails if implemented as Mode 1 extension or Mode 4.** Either path risks treating
user-entered actuals as equivalent to simulation outputs — a precision claim the data
cannot support.

**Milestone placement:** M11. The overlay rendering is architecturally self-contained.
It does not require Mode 3. It extends Mode 2's SCENARIO_COMPLETE state with a new data
entry path and a new trajectory series. M11 is the Political Economy milestone with no demo
commitment — appropriate for a focused architectural extension.

**Data schema question (for Data Architect):** Observed actuals must be persisted if the
session is closed and reopened. Options: (a) store as a JSONB array in the scenarios table
alongside the baseline scenario; (b) store in a new `observed_actuals` table with a
foreign key to `scenarios.id` and per-step rows. Option (b) is more normalized and
queryable; option (a) is simpler. DA must rule before implementation begins.

**Panel required:** Architecture Review (TARGETED — observed-actuals overlay implementation
approach). Members: Architect Agent (R), Data Architect (C — schema for actuals
persistence), Chief Methodologist (C — epistemic honesty of overlay: confidence tier
for user-entered data, provenance disclosure), Development Economist (C — accountability
use case validity: does this overlay serve Abena's reporting workflow?), Customer Agent
(C — Abena's actual document formats for programme monitoring data).

---

### F-003 — US-043: Community-Audience Output Layer

**Classification:** Standalone rendering/export tool — **NOT a new mode or zone**

**Basis:**

US-043 requires a community-audience rendering of the trajectory comparison as a PDF report
in plain language. The simulation engine produces no new output for this story. The
instrument cluster layout is unchanged. The MDA alert panel is unchanged. What changes is
a rendering path: the existing comparison output is transformed into a community-readable
format.

This is architecturally equivalent to a report generator: take the existing simulation
output data (trajectory, alert panel findings) and produce a document in a different
register. Two sub-components:

1. **Plain-language vocabulary mapping layer** — Translates technical outputs into
   community-readable language. Per indicator × severity combination: what does "HDI
   composite crossed WARNING at step 2" mean for people in plain language? This requires
   a maintained vocabulary mapping (similar to `INDICATOR_DISPLAY_NAMES` in the frontend,
   but extended to consequence language and keyed to severity).

2. **PDF/document format rendering** — Server-side or client-side document generation
   from the vocabulary-mapped output. A4 format, two-column, screen-readable.

**CRITICAL FINDING — No False Precision risk:**

The story's acceptance criteria state:

> "the output document contains no technical notation: no 'composite_score', no
> 'confidence_tier N', no 'MDA', no 'Tier N' strings as primary content"

The phrase "as primary content" is ambiguous. Read strictly, it prohibits these strings
from appearing as the lead finding — acceptable. Read loosely, it could be interpreted
as stripping epistemic disclosure from the community report entirely.

**The No False Precision principle is absolute.** CLAUDE.md states: "Uncertainty is
quantified and displayed, not hidden. The model's blindspots are documented and visible."
A community report that strips confidence tier disclosure entirely would violate this
principle. A government-funded programme monitor reading a WorldSim-generated report that
does not disclose that a key indicator is a synthetic estimate (Tier 4) would be misled
about the strength of the evidence.

The community-audience vocabulary mapping must include plain-language equivalents of
epistemic disclosure:
- Tier 1–2: "Based on official government statistics" (no special marking needed)
- Tier 3: "Based on a model estimate from comparable countries"
- Tier 4: "This is an estimated figure — independent verification recommended"
- Tier 5: "Insufficient data — the model could not compute this reliably"

The acceptance criteria must be tightened: "no technical notation as primary content"
must be accompanied by "plain-language epistemic disclosure present for all Tier 3+
indicators." This is a required correction before implementation begins.

**Platform Principle test:** Passes. The vocabulary mapping works for any scenario.
No scenario-specific branches in the report generator.

**Sequencing dependency:** US-043 is not independent of US-042. The community report
(US-043) is most valuable when it covers the commitment gap — the comparison between
what was promised (Scenario A) and what was observed (observed actuals overlay from
US-042). Without US-042, US-043 can only report on the Mode 2 comparison between two
configured scenarios, which is a weaker accountability claim (it shows what would happen
at different spending levels, not what actually happened). Implementing US-043 before
US-042 is possible but delivers reduced value for Persona 8's primary use case.

**Milestone placement:** M11 (with or after US-042). Can be scoped as a standalone
deliverable if US-042 is out of scope, but the dependency should be documented in
the tracking issue.

**Panel required:** Architecture Review (TARGETED — community output rendering approach,
No False Precision correction). Members: Architect Agent (R — rendering approach),
Chief Methodologist (C — No False Precision: plain-language disclosure standard),
Development Economist (C — accountability report format requirements), Customer Agent
(C — SEND Ghana's actual publication formats and community audience reading level),
Community Resilience Agent (C — community legibility: does this output reach
programme beneficiaries in a usable form?). UX Designer (C — export path placement
in the compare view layout).

---

### F-004 — US-048: X-Ray Structural Dependency Visualization

**Classification:** New Zone 2 surface + backend API extension — **NOT a new simulation mode**

**Basis:**

US-048 requires a directed graph visualization showing the multi-hop causal path from a
policy input through the simulation's event-propagation graph to an outcome indicator.
The story note correctly identifies that this lives in Zone 2 (one-click access from Zone 1),
with no Premise 1 or Premise 2 conflict.

The architectural requirements are:

**Backend (new):**

The simulation engine uses an event-propagation relationship graph internally. This graph
is not currently surfaced to the frontend — it is execution infrastructure, not output.
US-048 requires a new API endpoint that traverses this graph in reverse from a selected
indicator at a selected step and returns the causal provenance chain.

Two traversal strategies:
- *At-runtime traversal:* The trajectory endpoint already knows, for each step, which
  propagation events fired. The causal chain for a given indicator at a given step can be
  reconstructed by walking the relationship graph backward from that indicator. This
  requires O(depth × branching_factor) traversal per request — acceptable if depth is
  bounded (the 4-hop minimum in US-048 suggests the use case is shallow chains, not the
  full graph).
- *Stored provenance:* The engine annotates each state update at each step with its causal
  chain at computation time. This is more expensive to compute and store but produces instant
  retrieval. Appropriate if the causal graph is used frequently across many sessions.

Chief Engineer must rule on the engine's ability to support runtime traversal, and whether
the relationship graph's current data structure is query-efficient in reverse.

**Frontend (new):**

A directed graph rendering component in Zone 2. Requirements from US-048 acceptance criteria:
- Directed nodes representing the causal chain
- 4-node minimum: price floor → farm gate price → farm income → food expenditure → child
  malnutrition (note: this is 5 nodes for 4 hops)
- **Bidirectional Zone 1/Zone 2 coupling:** When a node in the X-ray graph is selected,
  the trajectory view in Zone 1 highlights the corresponding indicator curve. This is novel
  — it requires a shared state atom that both the Zone 1 trajectory view and the Zone 2
  X-ray panel subscribe to. The Zustand atom pattern from US-023/US-024 can support this,
  but the implementation must ensure Zone 1 does not re-render unnecessarily when a Zone 2
  node is selected.

**Platform Principle test:** Passes. The causal graph traversal API is scenario-agnostic —
it works for any indicator in any scenario where the relationship graph is populated. The
4-hop agricultural income chain is one instance of a general capability.

**No False Precision test:** Significant risk to flag. The X-ray visualization implies
that the displayed causal chain is *the* causal chain — that X causes Y definitively.
In the simulation, causality is encoded as elasticity relationships (e.g., gdp_growth_change
→ rule_of_law_percentile at -0.08 per unit). These are modeled relationships, not empirically
established cause-and-effect. The Chief Methodologist must rule on the epistemic disclosure
required alongside the X-ray visualization:
- Each edge in the graph should carry its elasticity value and source (e.g., "Bermeo 2016
  — democratic backsliding coefficient")
- A disclosure at the panel header: "This path represents the simulation model's causal
  assumptions, not empirically established causation"
- Edges derived from synthetic data must carry Tier notation consistent with ADR-007

**Milestone placement:** M11 or M12. Two considerations:
1. The backend provenance API requires Chief Engineer involvement (potentially blocked
   on the ADR-009 engine computation model).
2. The Zone 2 directed graph rendering component is frontend work that could begin
   independently of the backend if the API contract is specified first.
3. If the Chief Engineer confirms runtime traversal is feasible without ADR-009 resolution,
   M11 is plausible. If ADR-009 is a prerequisite, M12 is more likely.

**Panel required:** Architecture Review (TARGETED — X-ray provenance API and Zone 2
graph rendering). Members: Architect Agent (R — API contract for provenance endpoint),
Chief Engineer (C — graph traversal feasibility and engine data structure), Frontend
Architect (C — directed graph component and Zone 1/2 bidirectional coupling),
Chief Methodologist (C — No False Precision: causal disclosure standard for edges and
panel header), Development Economist (C — is the 4-hop minimum adequate for agricultural
income transmission chains in the scenarios we intend to support?).

---

## Cross-Cutting Findings

### F-005 — US-043 No False Precision Violation Risk

**Severity:** High — requires correction before implementation begins

The phrase "no technical notation as primary content" in US-043's acceptance criteria is
ambiguous in a way that could produce a community report that strips epistemic disclosure
entirely. This is a potential No False Precision violation and must be corrected in the
acceptance criteria before any implementation work begins.

**Required correction:**

The acceptance criterion:
> "the output document contains no technical notation: no 'composite_score', no
> 'confidence_tier N', no 'MDA', no 'Tier N' strings as primary content"

Must be accompanied by an additional criterion:
> "For any indicator with confidence_tier ≥ 3, the community report contains a
> plain-language epistemic disclosure consistent with the vocabulary mapping standard:
> Tier 3 → 'Based on a model estimate from comparable countries'; Tier 4 → 'This is an
> estimated figure — independent verification recommended'; Tier 5 → 'Insufficient data —
> the model could not compute this reliably'"

**Owner of correction:** PO Agent (R on user stories), Chief Methodologist (C — the
vocabulary mapping standard is CM's domain).

This finding should be registered with the PO Agent before Issue #577's DIC panel
activation. The correction does not block DIC panel activation — it should be incorporated
into the DIC brief as a pre-decided constraint.

### F-006 — US-042 and US-043 Sequencing Dependency

**Severity:** Medium

US-043 (community-audience output) delivers its highest value when it covers the commitment
gap between committed programme spending (Mode 2 Scenario A) and observed actuals (US-042
overlay). Without US-042, US-043 can only compare two Mode 2 configured scenarios — a
weaker accountability claim than what Persona 8's primary use case requires.

The tracking issues for US-042 and US-043 should document this dependency explicitly.
The DIC panel should assess whether:
1. US-043 without US-042 is useful enough to implement first (serving the mode-2-vs-mode-2
   comparison without the actuals overlay), or
2. US-042 is a hard prerequisite for US-043 and they should be scoped as a single deliverable.

**No process action required** — this is a planning input for the DIC panel, not an error.

### F-007 — US-039 Milestone Mis-Scope Risk

**Severity:** Medium

US-039 is tagged [Phase-3-TBD] without a milestone assignment. The story is anchored to
"Journey F (Mode 3 extension, not yet in current journey map)." Mode 3 Active Control is the
M12 core deliverable. If US-039 is scoped into M10 or M11 without the Mode 3 journey and
instrument cluster fully specified, it will be implemented without adequate context and will
likely require rework when Mode 3 arrives.

The DIC panel should explicitly confirm the milestone placement as M12 before any
implementation tracking issue is filed for US-039.

**Exception path acknowledged:** If the DIC panel concludes that a simplified Mode 2 variant
(quick alternate scenario creation) is adequate for James Ochieng's committee hearing
use case, that variant could be scoped into M11 as a [Near-Term-Gap] rather than [Phase-3-TBD].
The distinction requires UX Designer ruling on whether Mode 2 quick-create satisfies the
"parliamentary tempo" constraint in the story's north-star sentence.

### F-008 — Panel Architecture Clarification

**Severity:** Low (process clarity)

The story notes for US-042 and US-048 call for "DIC panel scope assessment." The DIC
(Domain Intelligence Council) is the domain intelligence panel — economists, political analysts,
ecologists — whose purpose is to surface competing human values and domain accuracy constraints.

For Issue #577, the primary questions are architectural (which implementation approach,
which milestone, which API contract) — not domain accuracy questions. The correct panel
type for US-039, US-042, US-043, US-048 is:

> `Architecture Review: TARGETED — [story ID]: [capability description]`

with DIC domain members consulted (C) where domain accuracy is load-bearing:
- US-042: Development Economist (accountability use case), Chief Methodologist (overlay
  epistemic honesty), Customer Agent (civil society monitor workflow)
- US-043: Chief Methodologist (No False Precision), Development Economist (report content),
  Customer Agent (community legibility), Community Resilience (beneficiary reach)
- US-048: Chief Methodologist (causal attribution disclosure), Development Economist
  (agricultural income chain depth)
- US-039: No DIC domain members required unless the Mode 2 exception path is evaluated

The Architecture Review Facilitator (not the Council Orchestrator) is the correct
activation for Issue #577. The Council Orchestrator's ORCHESTRATE mode is appropriate when
"competing interests" across frameworks must be made explicit — Issue #577 is an architectural
scoping question, not a values tradeoff.

---

## Summary Table

| Story | Classification | Zone | Mode | Milestone | Panel type | No False Precision risk |
|---|---|---|---|---|---|---|
| US-039 | Extension of Mode 3 | Zone 1 (control plane) | Mode 3 | M12 (M11 if Mode 2 variant confirmed) | Architecture Review (TARGETED) | None identified |
| US-042 | New Zone 2 surface + Zone 1 overlay | Zone 1 (overlay) + Zone 2 (data entry) | Mode 2 (extended) | M11 | Architecture Review (TARGETED) | Medium — user-entered actuals confidence tier must be disclosed |
| US-043 | Standalone rendering/export tool | No zone (export path) | None (output of any mode) | M11 (with or after US-042) | Architecture Review (TARGETED) | **HIGH — epistemic disclosure stripping risk; correction required** |
| US-048 | New Zone 2 surface + backend API | Zone 2 (graph) + Zone 1 coupling | Mode 1 (initially) | M11 or M12 (Chief Engineer gates) | Architecture Review (TARGETED) | Medium — causal attribution disclosure required per edge |

---

## Recommended Actions

**Before Issue #577 DIC panel activation:**

1. PO Agent corrects US-043 acceptance criteria to add plain-language epistemic disclosure
   requirement per F-005. Chief Methodologist drafts the vocabulary mapping standard.

2. EL confirms or revises the milestone placement for US-039 (M12 vs. M11 Mode 2 variant).

3. The activation for Issue #577 should be:
   `Architecture Review: TARGETED — Issue #577: [Phase-3-TBD] public advocacy story scope`
   Not `Council Orchestrator: ORCHESTRATE` — the questions are architectural, not values-tradeoff.

**Panel composition for Issue #577:**

| Member | Role | Stories |
|---|---|---|
| Architect Agent | R (scope decision) | US-039, US-042, US-043, US-048 |
| Chief Engineer | C | US-039 (branch-and-recompute), US-048 (graph traversal) |
| Frontend Architect | C | US-039 (control plane), US-048 (Zone 2 graph component + Zone 1/2 coupling) |
| Data Architect | C | US-042 (schema for observed actuals persistence) |
| Chief Methodologist | C | US-042 (user-entered tier), US-043 (disclosure vocabulary), US-048 (causal attribution) |
| Development Economist | C | US-042 (accountability use case), US-043 (report content), US-048 (chain depth) |
| Customer Agent | C | US-042 (Abena's workflow), US-043 (community legibility) |
| Community Resilience | C | US-043 (beneficiary reach) |
| UX Designer | C | US-039 (Mode 3 journey gap), US-043 (export path placement) |
| Engineering Lead | A (decision authority) | All — final milestone and scope decisions |

---

*This document is a process audit artifact. It does not constitute an architectural decision.
All recommendations require Architecture Review panel validation and EL acceptance before
any implementation begins.*
