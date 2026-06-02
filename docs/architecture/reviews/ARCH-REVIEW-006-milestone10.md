# ARCH-REVIEW-006: Issue #577 Targeted — [Phase-3-TBD] Story Architectural Scope

**Review type:** Targeted — architectural scope decision for four [Phase-3-TBD] user stories
(US-039, US-042, US-043, US-048) from the public advocacy story set (Issue #576 / #577)
**Scope:** PI-REVIEW-002 classified findings; milestone placement; new Zone 2 surfaces;
branch-and-recompute; post-processing overlay; standalone export; bidirectional Zone 1/2 coupling
**Facilitated by:** Architecture Review Facilitator
**Date:** 2026-06-02
**Status:** Complete — findings below; GitHub Issues enumerated in §Summary Table
**Input document:** `docs/process/audits/PI-REVIEW-002-issue-577-scope-2026-06-02.md`
**Panel:**

| Agent | Role | Scope |
|---|---|---|
| Architect Agent | R — scope decisions | All stories |
| Chief Engineer | C | US-039, US-048 |
| Frontend Architect | C | US-039, US-048 |
| Data Architect | C | US-042 |
| Chief Methodologist | C | US-042, US-043, US-048 |
| Development Economist | C | US-042, US-043, US-048 |
| Customer Agent | C | US-042, US-043 |
| Community Resilience | C | US-043 |
| UX Designer | C | US-039, US-043 |
| Engineering Lead | A — decision authority | All |

---

## Purpose

PI-REVIEW-002 classified the four [Phase-3-TBD] stories from Issue #576 into architectural
categories and identified pre-activation blockers. Both blockers are now resolved: US-043 was
corrected (PR #598) and US-039's M12 milestone placement was confirmed by EL. Issue #577 is
fully unblocked.

This targeted review translates PI-REVIEW-002's classifications into architectural findings.
For each story, the review names the specific unknowns that must be resolved before
implementation can begin, classifies findings by horizon, and produces the GitHub Issue list
that converts findings into tracked commitments.

**This review produces challenges. It does not produce ADR text.** Where a finding exposes
an architectural decision that rises to ADR level, that is noted explicitly.

---

## Story 1: US-039 — Real-Time Parameter Change (Mode 3)

**PI-REVIEW-002 classification:** Mode 3 extension — branch-and-recompute
**Milestone placement:** M12 (EL decision 2026-06-02, Issue #577)
**Horizon:** Long-Term

### Current state

Mode 3 (Active Control) is the north star interaction mode. Its core cognitive task is
real-time steering within human cost constraints. No Mode 3 implementation exists. The
control plane layout zone is reserved (CLAUDE.md §UX Architectural Commitment 5) but not
built. The simulation engine has no concept of a "branch point" — a saved intermediate
state from which a modified parameter set can recompute forward without restarting from
the scenario's initial conditions.

### Challenge from Chief Engineer

The branch-and-recompute capability requires the engine to hold a baseline state snapshot
at the moment the user initiates a parameter change. From that snapshot, the engine must
compute a new forward trajectory using the modified parameters. Two unknowns are
architecturally critical:

1. Can the current engine serialize an intermediate simulation state to a snapshot that is
   sufficient to restart computation? The engine's event-driven feedback graph has
   time-dependent state (accumulated STOCK values, adaptive temporal resolution context,
   triggered failure mode states). All of this must be captured in the snapshot. If the
   engine was not designed with mid-run serialization in mind, this is a significant
   engine refactor, not a feature addition.

2. Does branch-and-recompute require creating a new scenario object, or can it reuse the
   existing scenario? If it creates a new scenario object, the UX must handle the scenario
   multiplicity — two scenarios with different parameter sets, one of which is the "live"
   user modification. This is a different UX model from what Modes 1 and 2 present.

Neither question can be answered without Chief Engineer assessment of the engine's current
serialization capability. This assessment is a prerequisite to any Mode 3 implementation
planning.

**→ Blindspot AR-006-B-001:** Branch-and-recompute architecture undefined. Chief Engineer
assessment required before US-039 enters any implementation milestone.

### Challenge from Frontend Architect

The Mode 3 control plane zone is reserved in layout but has no interaction design. The
branch-and-recompute flow creates a specific UX requirement: after a parameter change,
there is a recompute latency before the updated trajectory appears. During that latency,
the instrument cluster must remain usable (it cannot go blank or show a spinner that blocks
the primary viewport). The interaction model for the recompute loading state has no design.

This is upstream of the Zustand store design for Mode 3 — the store must hold the
"recomputing" state and surface it to the instrument cluster without disrupting the current
trajectory display.

**→ Blindspot AR-006-B-002:** No interaction design for the parameter-change → recompute →
trajectory update flow. UX Designer must produce an interaction spec before Mode 3
implementation planning begins.

### Challenge from UX Designer

US-039 sets an implicit latency expectation: "real-time" implies sub-second or
near-sub-second feedback. If branch-and-recompute takes 2–5 seconds on the hardware target
(4-core laptop, 8GB RAM — CLAUDE.md §Equitable Build Process), the UX must accommodate
a loading state that preserves the control loop feel rather than breaking it. The phrase
"real-time" in the story should be replaced with an explicit latency budget before the
story enters implementation.

The engine performance baseline benchmark (Issue #514, M10 deliverable) is the prerequisite
measurement. Without benchmark data, no latency budget can be set.

**→ Blindspot AR-006-B-003:** Latency budget for parameter-change → recompute undefined.
Issue #514 benchmark results are prerequisite input to M12 Mode 3 planning.
(No new issue — blocked on Issue #514.)

---

## Story 2: US-042 — Observed Actuals Overlay on Trajectory View

**PI-REVIEW-002 classification:** New Zone 1 overlay (post-processing) — not a simulation
mode; observed actuals are NOT fed into the engine
**Milestone placement:** M11 (with CE approval on Zone 1 rendering contract)
**Horizon:** Near-Term

### Current state

The trajectory view (Zone 1) renders simulation output series for a single scenario step
axis. It has no concept of a "data series from external observation." Observed actuals — IMF
Article IV outcomes, World Bank HIPC tracker data, or government self-reported post-program
indicators — are categorically distinct from simulation outputs. The accountability tracking
use case (Journey H, Personas 7/8) requires overlaying these actuals as a distinct visual
series.

The critical architectural constraint from PI-REVIEW-002 F-002: observed actuals must NOT
be routed through the simulation engine. Doing so would conflate categorically distinct
quantities (a simulation projection vs. an observed outcome) and would violate the No False
Precision principle by implying the engine "produced" the observed outcome.

### Challenge from Data Architect

The trajectory view's current rendering contract covers simulation output series only.
Observed actuals require a series classification that answers four questions before any
rendering work begins:

1. **Data model:** Where do observed actuals live in the database? The `sources` table
   holds time-series data from registered sources. Observed actuals are eligible for
   `source_registry` registration — they have a provenance, a data quality tier, and a
   vintage date. But the query path from `source_registry` to the trajectory view endpoint
   is not designed.

2. **Confidence tier assignment:** Observed actuals have their own data quality dimension.
   An IMF Article IV Consultation figure has different reliability than a government
   self-report. The confidence tier system applies. The trajectory view must render the
   tier annotation for each actuals data point, using the same per-indicator provenance
   display that applies to simulation outputs.

3. **Rendering contract:** The actuals series must be visually distinct from simulation
   projection series. Color, line style, and legend treatment must differ. The rendering
   contract must be defined before the component is built.

4. **Sparse data handling:** Observed actuals are not available for every time step in
   the simulation window. The rendering contract must define how gaps are displayed
   (interpolated, null-connected, or broken line) and must not create false continuity
   between sparse observations.

**→ Blindspot AR-006-B-004:** No data model or rendering contract for observed actuals
series. Both are prerequisites for US-042 implementation.

### Challenge from Chief Methodologist

The accountability tracking use case compares simulation projection against observed outcome.
This comparison is analytically meaningful — it reveals whether a policy produced its
projected human development outcomes. But it is vulnerable to confound: many variables
affect outcomes between projection and realization. A direct overlay without confound
disclosure implies that divergence between projection and actuals is fully attributable
to policy choices. That implication is false in most real cases.

The No False Precision principle applies: the UI must not present a comparison that implies
causal attribution the model cannot support. Whether this requires a rendered disclaimer
adjacent to the overlay (implementation detail) or an architectural constraint on what the
actuals overlay endpoint is permitted to return without a confound annotation (API contract)
must be decided before the endpoint is designed.

**→ Blindspot AR-006-B-005:** Confound disclosure requirement unresolved for accountability
tracking overlay. Must be decided before the actuals overlay API contract is written.

### Challenge from Development Economist

The accountability tracking use case exists specifically because governments, civil society,
and affected communities need a mechanism to assess whether promised policy outcomes
materialized. This is one of WorldSim's most analytically significant use cases from a
human cost ledger perspective. The overlay must show human development actuals (HDI
component indicators, capability measures) with the same visual weight as financial actuals.
If the overlay defaults to financial indicators and treats human development actuals as
secondary, the use case fails its primary purpose.

**→ Blindspot AR-006-B-006:** Human cost ledger parity in actuals overlay not guaranteed.
The rendering contract (AR-006-B-004) must explicitly require human development actuals to
receive equal visual weight to financial actuals.

### Constraint from PI-REVIEW-002 (enforced here)

The engine/overlay separation must be enforced at the API layer, not by implementation
convention. The endpoint that injects an actuals series must not route through the simulation
computation path. This is not a guideline — it is an architectural constraint that must
appear in the US-042 API contract spec.

**→ Constraint AR-006-C-001:** Engine/overlay separation is an API contract requirement,
not an implementation-time decision.

---

## Story 3: US-043 — Community Report Export

**PI-REVIEW-002 classification:** Standalone export — post-processing pipeline downstream
of the rendering layer; not a simulation mode
**Milestone placement:** M11
**Horizon:** Near-Term (one Immediate blocker — see AR-006-B-007)

### Current state

WorldSim has no export pipeline. US-043 specifies a community-oriented export format with
plain-language epistemic disclosure replacing technical confidence tier notation. The
No False Precision violation in the original story was corrected via PR #598 (PI-REVIEW-002
F-005): the vocabulary mapping standard (Tier 3 → "Based on a model estimate from comparable
countries"; Tier 4 → "This is an estimated figure — independent verification recommended";
Tier 5 → "Insufficient data — the model could not compute this reliably") is now the
required disclosure mechanism, replacing technical notation rather than omitting it.

### Challenge from Chief Methodologist

The vocabulary mapping standard was described in PI-REVIEW-002 and applied as a correction
to US-043. It does not exist as an authored canonical document. The export pipeline's
conditional disclosure logic — which plain-language string appears adjacent to which
indicator — cannot be implemented until the canonical vocabulary map is defined by CM.

The mapping has three dimensions that CM must specify:
1. The trigger condition (confidence_tier ≥ N)
2. The display string per tier (already drafted in PI-REVIEW-002)
3. The placement rule ("adjacent to each indicator finding" — but what counts as "adjacent"
   in a two-column A4 format? Footnote? Inline qualifier? Sidebar callout?)

Without CM authoring this standard, any implementation is building on an informal draft.
The vocabulary mapping standard is a blocking prerequisite for all US-043 implementation.

**→ Blindspot AR-006-B-007 (IMMEDIATE — blocks M11 implementation):** Vocabulary mapping
standard does not exist as a CM-authored canonical document. Must be authored before any
US-043 implementation work begins.

### Challenge from Community Resilience

The community report format (A4 two-column, screen-readable PDF) specifies an output format
but does not specify the rendering path. Two paths are architecturally distinct:

**Path A — In-app PDF generation:** WorldSim generates the PDF directly. This requires a
PDF rendering dependency (e.g., WeasyPrint, Puppeteer, or similar). It adds a significant
build and runtime dependency, a new test surface, and infrastructure burden that may violate
the Equitable Build Process requirement (CLAUDE.md §Equitable Build Process — test suites
must not require proprietary software to pass; contributors on modest hardware must be able
to run the full test suite).

**Path B — Structured export (HTML/Markdown → user conversion):** WorldSim generates a
structured document that the user renders using local tooling. This eliminates the PDF
dependency but shifts conversion burden to the user. For a community advocacy organization
with limited technical capacity, this may not be acceptable.

The choice is architecturally load-bearing. It drives the dependency list, the test
infrastructure requirements, and the export API contract. It must be decided before
implementation begins.

**→ Blindspot AR-006-B-008:** PDF rendering path unresolved. In-app generation vs.
structured export is an architectural choice with Equitable Build Process implications.
Must be decided as part of US-043 implementation planning.

### Challenge from Customer Agent

The A4 two-column format is specified by SEND Ghana's publication requirements. Other
advocacy personas (Persona 7 — investigative journalists, Persona 4V — frontline
ministry officials) may use different formats. If the export pipeline is implemented
as a single hardcoded format, it will require refactoring when additional formats are
needed.

The export architecture should be designed with pluggable format adapters (A4 PDF,
screen-readable PDF, HTML, Markdown) even if only one format ships in M11. This is not
a feature request — it is an architectural constraint on the pipeline's extensibility.
A pipeline that cannot accommodate a second format without restructuring is a near-term
technical debt commitment.

**→ Blindspot AR-006-B-009:** Export format adapter design absent. The pipeline must
support pluggable formats from the initial design, not require refactoring when a second
format is requested. Combine with AR-006-B-008 in a single architecture decision issue.

### Challenge from UX Designer

Plain-language epistemic disclosure must appear "adjacent" to each Tier 3+ indicator
finding. In a two-column print format, "adjacent" requires a layout model decision:
footnote (numbered reference at bottom of column), inline qualifier (parenthetical
after the indicator value), or sidebar callout (boxed note in the margin). Each choice
requires a different HTML/template structure in the export pipeline. The layout decision
must be input from the CM placement rule (AR-006-B-007) and must appear in the export
template spec before implementation begins.

**→ Blindspot AR-006-B-010:** Epistemic disclosure layout model unspecified. Flows from
CM vocabulary mapping standard (AR-006-B-007) — not independently resolvable.
(No new issue — resolved when AR-006-B-007 is resolved.)

---

## Story 4: US-048 — X-Ray Interactive Graph with Bidirectional Zone 1/2 Coupling

**PI-REVIEW-002 classification:** New Zone 2 surface + new API endpoint (causal graph
exposure) + bidirectional Zone 1/2 coupling
**Milestone placement:** M11 or M12 — depends on Chief Engineer assessment of Zone 1/2
coupling complexity
**Horizon:** Near-Term

### Current state

Zone 2 currently renders geographic context (choropleth). No Zone 2 interactive surface
exists. The trajectory view (Zone 1) has no mechanism to respond to Zone 2 interaction
signals. The simulation engine's propagation graph is a backend construct — there is no
API endpoint that exposes the causal graph as a frontend-renderable structure. The story
requires: (1) a Zone 2 causal graph view, (2) a Zone 2 → Zone 1 highlight signal (node
selection highlights the corresponding trajectory curve), and (3) a Zone 1 → Zone 2
reverse highlight signal (trajectory cursor highlights the corresponding graph node).

### Challenge from Chief Engineer

The Zone 1/2 bidirectional coupling requires a shared state atom that two distinct
frontend zones read and write. The current Zustand store architecture has no such atom.
Adding it requires:

1. Deciding on the atom's schema (what does "node selected in Zone 2" look like as a
   data structure? An indicator key? A framework-indicator pair? A node ID in the
   causal graph?).
2. Ensuring Zone 1 and Zone 2 both subscribe to and write to the same atom without
   creating a circular update loop (Zone 2 writes "selected node" → Zone 1 highlights
   → Zone 1 writes "cursor position" → Zone 2 highlights → infinite loop risk).

The atom schema must be designed before either Zone is modified. It is the shared
contract between two independently developed components.

**→ Blindspot AR-006-B-011:** Zone 1/2 bidirectional coupling Zustand atom undefined.
Schema design is a prerequisite for all US-048 implementation work.

### Challenge from Frontend Architect

Zone 2 currently renders one view type (choropleth). Adding the X-ray graph as a Zone 2
view requires deciding the Zone 2 view model:

**Option A — Switchable Zone 2:** Zone 2 is a switchable multi-view zone; the user
selects "Geographic View" or "X-Ray View" from a control. This maintains Zone 2 as
a single panel with different rendering modes.

**Option B — Separate X-Ray Panel:** The X-ray graph is a separate panel outside
Zone 2. This may require layout restructuring and breaks the "Zone 2 is contextual
navigation" model.

Option A is architecturally consistent with the existing zone model (context is
navigable — CLAUDE.md §UX Architectural Commitment 2). Option B implies a new zone
which requires Engineering Lead sign-off per CLAUDE.md §UX Architectural Commitments.

The view model decision is upstream of all Zone 2 component work.

**→ Blindspot AR-006-B-012:** Zone 2 multi-view architecture undefined. The view model
choice (switchable vs. separate panel) must be made before Zone 2 component work begins.
Option B requires EL sign-off as a new zone addition.

### Challenge from Chief Methodologist

The causal graph exposed by the X-ray view must accurately represent the simulation's
actual propagation structure. This is a simulation output, not a documentation artifact.
If the displayed graph is simplified, aggregated, or stylized relative to the actual
propagation rules, users will draw incorrect conclusions about policy lever effects.

The causal graph API response must include, for each edge:
- The propagation weight (elasticity estimate)
- The confidence tier of that elasticity (literature source quality)
- The direction of the relationship and whether it is bidirectional

Without edge-level confidence annotation, the X-ray view implies equal certainty across
all propagation relationships — a No False Precision violation when elasticities range
from high-quality meta-analyses to rough model estimates.

**→ Blindspot AR-006-B-013:** Causal graph API response must include per-edge confidence
annotation. This is an API contract requirement, not an implementation detail.

### Challenge from Development Economist

The X-ray view's cross-framework edges (e.g., fiscal pressure → education spending →
human capability) represent cross-framework causal claims with varying empirical support.
A direct edge in the X-ray graph implies a modeled causal relationship. Users may
interpret the edge as a well-established empirical relationship when it may be a
modeled assumption with limited literature backing.

The Development Economist position: cross-framework edges in the X-ray view should
carry the same epistemic annotation discipline as simulation outputs. A Tier 4 or Tier 5
edge should render differently from a Tier 1 or Tier 2 edge — not just in the per-edge
confidence annotation but in the visual treatment (edge weight, color, or opacity).

**→ Blindspot AR-006-B-014:** Visual differentiation of cross-framework edge confidence
not designed. Flows from AR-006-B-013 — add to causal graph API design issue scope.

### Challenge from UX Designer

The interaction model for node selection is undesigned. Three dimensions require decisions
before the component is built:

1. **Trigger:** Hover vs. click (hover for transient highlight, click for persistent
   selection — or only click?)
2. **Selection cardinality:** Single node or multi-node selection (multi-node selection
   would highlight multiple trajectory curves simultaneously — useful for comparison
   but complex to implement and read)
3. **Interaction feedback:** Does Zone 1 scroll to the highlighted curve? Does it
   temporarily de-emphasize non-highlighted curves? Does it show a callout?

Each decision affects the Zustand atom schema (AR-006-B-011) and the Zone 1 trajectory
view component. The interaction model spec must be authored before either component
is modified.

**→ Blindspot AR-006-B-015:** X-ray interaction model (trigger, cardinality, feedback)
undesigned. Must be authored as part of AR-006-B-011 resolution.

---

## Cross-Cutting Findings

### Pre-activation status (informational)

Both Issue #577 pre-activation blockers identified by PI-REVIEW-002 are resolved:
- F-005 (US-043 No False Precision): Corrected via PR #598
- US-039 milestone: Confirmed M12 by EL (2026-06-02)

Issue #577 is fully unblocked. The panel composition from PI-REVIEW-002 is the recommended
starting point for DIC activation.

### Zone 2 interaction standard gap

US-048 is the first Zone 2 interactive surface in WorldSim. There is no Zone 2 interaction
design standard — no defined patterns for hover, click, selection, or Zone 1/2 communication.
Before M11 Zone 2 implementation begins on any story, a Zone 2 interaction standard should
be authored (or explicitly scoped into the US-048 interaction design work). Building US-048
without a standard risks establishing an ad-hoc pattern that conflicts with future Zone 2
surfaces.

**→ Blindspot AR-006-B-016:** No Zone 2 interaction design standard. Recommend authoring
one as part of US-048 design work rather than deferring it.

### ADR threshold assessment

None of the four stories individually rises to the ADR threshold. However, two findings
may:

- **Zone 2 multi-view model (AR-006-B-012):** If Option B (separate panel) is chosen,
  this introduces a new zone — a UX architectural change that requires Engineering Lead
  sign-off per CLAUDE.md §UX Architectural Commitments and may warrant an ADR depending
  on scope.
- **Branch-and-recompute (AR-006-B-001):** If the Chief Engineer assessment reveals that
  branch-and-recompute requires a significant engine refactor, the refactor scope may
  warrant an ADR. ADR-009 (simulation engine computation model, M11 deliverable) is
  the likely vehicle.

Neither rises to ADR level today. Both should be re-evaluated when the CE assessments
(AR-006-B-001, AR-006-B-012) are complete.

---

## Summary Table — GitHub Issues to Create

| Blindspot | Story | Horizon | Severity | Issue title (recommended) |
|---|---|---|---|---|
| AR-006-B-001 | US-039 | Long-Term | Blocker | CE assessment: branch-and-recompute from baseline snapshot (US-039 prerequisite) |
| AR-006-B-002 | US-039 | Long-Term | Blocker | Interaction spec: Mode 3 parameter-change → recompute → trajectory update (US-039) |
| AR-006-B-004 | US-042 | Near-Term | Blocker | Data model + rendering contract: observed actuals series (US-042) |
| AR-006-B-005 | US-042 | Near-Term | Major | API contract: confound disclosure requirement for accountability tracking overlay (US-042) |
| AR-006-B-006 | US-042 | Near-Term | Major | Rendering contract: human cost ledger parity in actuals overlay (US-042) |
| AR-006-B-007 | US-043 | **Immediate** | **Blocker** | **CM: author vocabulary mapping standard (prerequisite for US-043)** |
| AR-006-B-008/9 | US-043 | Near-Term | Major | Architecture decision: community report PDF rendering path + format adapter design (US-043) |
| AR-006-B-011 | US-048 | Near-Term | Blocker | Architecture: Zone 1/2 bidirectional coupling Zustand atom schema (US-048 prerequisite) |
| AR-006-B-012 | US-048 | Near-Term | Blocker | Architecture decision: Zone 2 multi-view model (geographic + X-ray) — US-048 |
| AR-006-B-013/14 | US-048 | Near-Term | Major | API design: causal graph exposure endpoint with per-edge confidence annotation (US-048) |
| AR-006-B-016 | US-048 | Near-Term | Minor | Zone 2 interaction design standard (prerequisite for all Zone 2 work) |

**Constraints (no new issue required):**
- **AR-006-C-001 (US-042):** Engine/overlay separation is an API contract requirement —
  include in AR-006-B-004 issue scope.
- **AR-006-B-003 (US-039):** Blocked on Issue #514 (engine benchmarks, M10 deliverable).
- **AR-006-B-010 (US-043):** Resolved when AR-006-B-007 is resolved (no separate issue).
- **AR-006-B-015 (US-048):** Include in AR-006-B-011 issue scope (interaction model spec
  is part of the atom schema design work).

---

## Recommended Next Actions

1. **File the CM vocabulary mapping standard issue immediately** (AR-006-B-007) — it is
   the only Immediate blocker and will gate all US-043 implementation.

2. **File CE assessment issues for US-039 and US-048** (AR-006-B-001, AR-006-B-012) before
   M11 planning begins — these assessments produce the prerequisite inputs for M11 milestone
   scoping decisions.

3. **File remaining Near-Term issues** (AR-006-B-004, AR-006-B-005, AR-006-B-006,
   AR-006-B-008/9, AR-006-B-011, AR-006-B-013/14, AR-006-B-016) as part of Issue #577
   activation — they are the scope decomposition for M11 implementation work.

4. **Assign all eleven issues as children of Issue #577** per the three-level issue
   hierarchy (Epic → Feature Issue → Task Issue).
