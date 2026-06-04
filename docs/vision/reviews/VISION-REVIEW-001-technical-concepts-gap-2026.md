# VISION-REVIEW-001: Technical Concepts Gap Analysis

**Date:** 2026-06-03
**Issue:** #577 — DIC technical concept review (Phase 3 of the Vision-to-Architecture Bridge)
**Parent Epic:** #574

**Panel:** Geopolitical Analyst, Development Economist, Political Economist,
Chief Methodologist, Intergenerational Advocate

**Input documents reviewed by each agent:**
- `docs/vision/worldsim-intellectual-foundations-2026-05-31.md`
- `docs/vision/worldsim-founding-document-recommendations-2026-05-31.md`
- `docs/ux/personas.md` (as extended by PR #592 — Personas 6, 7, 8, 4V)
- `docs/ux/user-journeys.md` (as extended by PR #600 — public advocacy journeys)
- `[Phase-3-TBD]` tagged user stories from #576
- `docs/vision/worldsim-technical-concepts.md` (18 concepts, version 1.0)

---

## Panel Task

For each agent: identify which ideas in the intellectual foundations and extended
user journeys have concrete architectural implications not captured in the 18 existing
technical concepts. Name the gap. Name the concept. Explain the technical implication —
what would need to be built, changed, or constrained.

Findings format: **Gap name → Concept name → Technical implication → Affected existing
concepts (if any) → New concept required (yes/no)**

---

## Agent Findings — Geopolitical Analyst

*Domain: Coercive dynamics, debt leverage, negotiating tactics*

### Finding GA-001: The Tactical Context of Each Instrument Is Implicit

**Gap:** The intellectual foundations (Part Five: The Art of the Deal) describes how
each WorldSim instrument directly counters a specific negotiating tactic — MDA
thresholds counter anchoring, PMM counters leverage exploitation, Mode 2 pre-run
counters manufactured urgency. This mapping is precise and architecturally meaningful.
It is nowhere in the 18 technical concepts.

**Why it matters technically:** If the tactical context of each instrument is not
codified, two problems arise:
1. Instrument designers optimize for analytical completeness rather than tactical
   readiness — a different design constraint.
2. The acceptance criteria for each instrument cannot include the most important
   test: does the finance ministry analyst, using this instrument in a live
   negotiation, have what she needs to resist the specific tactic it was designed
   to counter?

**Technical implication:** A new technical concept is required that names the
Counter-Negotiation Architecture as a design principle — not a feature, but an
architectural constraint on how instruments are specified, tested, and documented.
Each instrument's specification must include its "counter" assignment and the tactical
scenario against which it is acceptance-tested.

**Affected existing concepts:** Concept 8 (UX Architecture), Concept 5
(Multi-Currency Measurement Framework)

**New concept required: Yes — Counter-Negotiation Architecture**

### Finding GA-002: The GPR Network Has No Cross-Case Query Architecture

**Gap:** The GPR Network theory of change (Part Seven) describes how a distributed
network of WorldSim deployments produces a "point cloud" that makes structural
patterns visible across countries. One WorldSim deployment produces a cross-section.
The network produces the three-dimensional map.

Concept 14 (Distributed Simulation Ecosystem) describes federation and data sharing.
It does not specify that the backtesting library must support cross-case structural
queries — that is, queries that answer "does the Greek fiscal multiplier anomaly
appear in the Argentine, Lebanese, and Thai backtesting record?" Cross-case inference
is different from per-country backtesting. The architecture required to support it
is different.

**Technical implication:** The backtesting library must be designed from the outset
with cross-case structural inference as a first-class query type, not a future
add-on. This requires a data model that normalizes across countries at the indicator
and relationship level — not just a collection of per-country time-series.

**Affected existing concepts:** Concept 14 (Distributed Simulation Ecosystem)

**New concept required: Yes — Cross-Case Structural Inference (as extension of Concept 14)**

---

## Agent Findings — Development Economist

*Domain: Human cost ledger, capability approach, distributional effects*

### Finding DE-001: Dependency Chain Visualization Is a New Data Layer

**Gap:** The intellectual foundations describe navigable multi-hop structural
dependency maps (Part Seven: The Dependency Chain Map) — the Moroccan property
chain, the Indian farmer suicide chain. These maps connect treaty structures,
financial policy decisions, and human consequences across time and across actors.

The X-ray view (US-048, Concept 4 — Causal Meta-Map) shows the simulation's
internal propagation graph: how events at one node propagate to adjacent nodes
within the simulation. That is not the same as a dependency chain visualization.
A dependency chain map requires data about legal/treaty structures, historical
policy decisions, and their documented human consequences — data that currently
has no place in the WorldSim data architecture.

**Technical implication:** A dependency chain visualization requires:
1. A new data layer for legal/treaty/policy decision records (distinct from
   simulation attributes)
2. A rendering mode for navigable multi-hop chains (distinct from the X-ray graph)
3. A provenance model for historical causal claims (distinct from simulation output)

**Assessment:** This is a significant architectural undertaking outside M11 scope.
The X-ray view (US-048) partially addresses the internal simulation propagation
structure. The full dependency chain map is a future milestone scope item.

**New concept required: No — defer to M12+ roadmap discussion. File as issue.**

### Finding DE-002: Lagged Consequence Architecture Has No Cross-Module Contract

**Gap:** Concept 13 (HealthBurdenModule and Lagged Health Consequences) establishes
lagged consequences as a pattern. The intellectual foundations extend this pattern
beyond health — to educational attainment across generations, to the children of
the Indian farmers. There is no cross-module contract that specifies how lagged
consequences are represented, communicated, and surfaced in the instrument cluster
across all modules that model them.

**Technical implication:** A cross-module lagged consequence contract is needed
before additional modules implement lagged indicators. Without it, each module
implements lags differently (different time horizons, different uncertainty bands,
different UI treatment). The Human Cost Ledger instrument cluster must handle
lagged consequences consistently regardless of which module produced them.

**Assessment:** This is a documentation gap in an existing concept (Concept 13),
not a new concept. The lagged consequence pattern should be generalized and
moved to a cross-module contract. Existing concept amendment, not a new concept.

**New concept required: No — Concept 13 amendment**

### Finding DE-003: Public Accountability Is Architecturally Distinct

**Gap:** The Phase-3-TBD user stories (observed-actuals overlay, community-audience
output layer, structural dependency visualization) are individually specified. But
they collectively constitute a distinct architectural layer — the public accountability
layer — that has no unified concept in the technical document.

The public accountability layer serves Personas 6, 7, 8, and 4V. It has distinct
requirements from the primary instrument layer (which serves Personas 1–5):
- Plain-language rendering (not just technical output)
- Export pipeline (not just on-screen display)
- Actuals comparison (not just simulation projection)
- Community-audience legibility (not just analyst legibility)

**Technical implication:** Without naming this as a distinct architectural layer,
each Phase-3 feature is designed in isolation, potentially with inconsistent
rendering contracts, data models, and accessibility baselines.

**New concept required: Yes — Public Accountability Architecture**

---

## Agent Findings — Political Economist

*Domain: Governance, political feasibility, structural dynamics*

### Finding PE-001: The Known Adversary Constraint Is Unencoded

**Gap:** Part Four of the intellectual foundations (Wallerstein's World Systems
Theory) names a specific challenge to WorldSim: the system will resist. As the
tool closes analytical gaps, new mechanisms will emerge to re-raise the bar. This
is not paranoia — it is a structural prediction grounded in world systems theory.

The Known Adversary Design Principle — that WorldSim must be designed with structural
resistance in mind — has implications for the methodology publication strategy, the
open-source licensing, and the governance framework. If the tool can be captured by
the parties it is designed to counter (by being made proprietary, by having its
methodology challenged by institutional authority, by being marginalized as an
"academic exercise"), the theory of change fails.

**Technical implication:** This is primarily a governance and security concern, not
a simulation architecture concern. The relevant architectural expressions are already
encoded: open-source licensing (Guiding Principles), dual-use protection framework
(POLICY.md), TSC gaming-detection mandate (Concept added in G7). A new technical
concept is not required — but the dual-use framework documentation should reference
the Wallerstein structural resistance argument explicitly.

**New concept required: No — governance/policy domain, not a technical concept**

### Finding PE-002: Political Feasibility Constraints Have No Formal Representation

**Gap:** The political economy module (M11 stretch goal) models political feasibility
constraints and conditionality. There is no technical concept that describes how
political feasibility constraints are represented in the simulation data model — as
a constraint on policy instrument parameters, as a separate module output, or as
a framework-level indicator.

**Technical implication:** This is the primary open architectural question for the
political economy module. It needs to be answered before any political economy module
implementation begins. However, this is the subject of ADR-009 (simulation engine
computation model), which is the M11 primary objective. The answer will emerge from
that work. Premature specification risks constraining ADR-009.

**New concept required: No — defer to ADR-009 process**

---

## Agent Findings — Chief Methodologist

*Domain: Statistical integrity, uncertainty quantification*

### Finding CM-001: Instrument Coherence Has No Formal Technical Specification

**Gap:** Part Six of the intellectual foundations names "Instrument Coherence" as
a design principle — specifically "The Reverse-Triangulation Principle": when
instruments contradict each other, the contradiction is the signal. A financial
recovery indicator that contradicts a human development deterioration indicator
does not resolve by choosing which to trust — it requires surfacing the
inconsistency for human judgment.

This principle is stated in the intellectual foundations as a design rationale. It
does not appear as a technical concept in `worldsim-technical-concepts.md`. Its
absence is consequential: without a formal specification, cross-framework
inconsistency detection is either not implemented, or implemented ad-hoc by
individual module developers.

**Technical implication:** Two concrete requirements follow from Instrument Coherence:

1. The instrument cluster must detect and surface cross-framework contradictions —
   specifically, cases where one framework shows improvement while another shows
   deterioration above a threshold. This requires a cross-framework comparison
   computation.

2. Instrument Coherence as a manipulation detection mechanism requires that selective
   manipulation of any single framework output is made visible by its inconsistency
   with the others. This is an integrity property of the instrument cluster that
   must be specified, not assumed.

**Affected existing concepts:** Concept 5 (Multi-Currency Measurement Framework),
Concept 8 (UX Architecture)

**New concept required: Yes — Instrument Coherence (The Reverse-Triangulation Principle)**

### Finding CM-002: Cross-Case Structural Inference Requires a Different Normalization

**Gap:** Confirming GA-002: per-country backtesting uses country-specific baselines.
Cross-case structural inference requires normalized comparisons across countries —
comparable elasticity estimates, comparable indicator scales, comparable time horizons.
The current backtesting architecture (Concept 3 — Iterative Engine) is silent on
cross-country normalization.

**Technical implication:** Cross-case queries need a normalization layer that does
not currently exist. This is an extension of GA-002 — the cross-case inference
concept must specify the normalization approach.

**New concept required: Yes — confirms GA-002, same concept**

---

## Agent Findings — Intergenerational Advocate

*Domain: Future generations, irreversible thresholds*

### Finding IA-001: Public Accountability Architecture Serves the Generational Timeline

**Gap:** Confirming DE-003. The intergenerational dimension adds one specific
requirement: the public accountability layer must be able to surface lagged
consequences across long time horizons in a format accessible to non-specialist
users. The children of the Indian farmers need to see the causal chain — not
just the outcome. The intergenerational accountability use case is specifically
for users who are living with the consequences of decisions made before they
had any representation in the negotiation.

**Technical implication:** The community-audience rendering mode (US-043) must
be capable of rendering lagged consequence chains — not just current-step
indicators. This extends the export pipeline requirement beyond a snapshot
report to a trajectory-aware report.

**New concept required: No — this is an additional requirement on the Public
Accountability Architecture concept (confirms DE-003)**

### Finding IA-002: The Instrument Coherence Principle Protects Against Intergenerational Harm

**Gap:** Confirming CM-001. Adding one dimension: cross-framework inconsistency
detection is particularly important for intergenerational consequences. Financial
recovery in the short term while human development deteriorates has intergenerational
consequences that extend beyond the simulation window. The instrument coherence
principle is not just a manipulation detection mechanism — it is also an
early-warning system for decisions with irreversible intergenerational consequences.

**Technical implication:** The cross-framework contradiction detection must be
sensitive to time-horizon asymmetry — financial indicators often resolve in years,
human development indicators in decades. The inconsistency threshold for
short-term-financial / long-term-human-development divergence may need to be
different from same-horizon divergences.

**New concept required: No — additional specification requirement on the Instrument
Coherence concept (confirms CM-001)**

---

## Synthesis: Proposed New Concepts

| Concept | Surfaced by | Technical requirement |
|---|---|---|
| Counter-Negotiation Architecture | Geopolitical Analyst (GA-001) | Each instrument's specification includes its tactical counter assignment and acceptance criteria |
| Instrument Coherence | Chief Methodologist (CM-001), confirmed by IA-002 | Cross-framework contradiction detection; reverse-triangulation as integrity property |
| Public Accountability Architecture | Development Economist (DE-003), confirmed by IA-001 | Plain-language rendering pipeline, export pipeline, actuals comparison layer as unified architectural layer |
| Cross-Case Structural Inference | Geopolitical Analyst (GA-002), confirmed by CM-002 | Normalized cross-country query layer in backtesting library |

**Deferred:**
- Dependency Chain Visualization (DE-001) — outside M11 scope; requires new data layer for legal/treaty records
- Known Adversary Design Principle (PE-001) — governance domain; existing dual-use framework applies
- Political Feasibility Constraints (PE-002) — ADR-009 scope; premature specification risks constraining that work
- Lagged Consequence Cross-Module Contract (DE-002) — Concept 13 amendment, not a new concept

---

## EL Decision Record

*See comment on Issue #577 for the full EL decision.*

**Decision:** Accept all four proposed new concepts. Defer the five items listed above.

**Concepts accepted for addition to `docs/vision/worldsim-technical-concepts.md`:**
- Concept 19: Counter-Negotiation Architecture
- Concept 20: Instrument Coherence — The Reverse-Triangulation Principle
- Concept 21: Public Accountability Architecture
- Concept 22: Cross-Case Structural Inference and the GPR Network

**Deferred:**
- Dependency Chain Visualization → file as future milestone scope issue
- Lagged Consequence Cross-Module Contract → Concept 13 amendment pending HealthBurdenModule M12 expansion
- Known Adversary Design Principle → no new concept required; POLICY.md reference to Wallerstein sufficient
- Political Feasibility Constraints → ADR-009 will produce the architectural answer; no concept required before that

**EL decision date:** 2026-06-03

---

*Panel review closed: 2026-06-03*
*Artifact committed: closes Issue #577*
*Parent epic: closes Issue #574 (all children #575, #576, #577 now resolved)*
