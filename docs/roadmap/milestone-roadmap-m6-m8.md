> **Archived:** This document covers the M6–M8 roadmap and is preserved as a historical record.
> The current roadmap (M9–M13) is at `docs/roadmap/worldsim-roadmap.md`.
> Last updated: 2026-05-22

# Milestone Roadmap — M6 through M13

> Extracted from CLAUDE.md at M4 exit (2026-04-26). Updated at M7 exit
> (2026-05-10) to correct M7 theme and expand to M9–M13 sequence.
> CLAUDE.md carries the current milestone inline; this file carries the
> committed scope. GitHub Milestones carry the live issue lists.
>
> M9–M13 sequence approved 2026-05-11. Old M9 (Methodology Publication)
> renumbered to M13 to make room for four intermediate milestones that
> absorb ~77 issues that had accumulated without milestone assignment.

---

## Milestone 6 — Backtesting Coverage Expansion

**Core deliverable:** Backtesting suite covers at least five historical cases
with documented fidelity thresholds per case.

**Scope:**
- Five historical cases minimum: Greece 2010–2012 (existing),
  Argentina 2001–2002, Thailand 1997, Lebanon 2019–2020, and one
  additional case chosen by Engineering Lead at M6 start
- MAGNITUDE_WITHIN_20PCT threshold enforced in CI for all five cases
- Backtesting fidelity dashboard visible in the UI (pass/fail per case,
  per module, per indicator)
- Ecological Module initial implementation (climate forcing integration
  from pre-computed ERA5 reanalysis data)
- Governance Module initial implementation (institutional quality indices,
  press freedom, policy-reality divergence)

**Dependencies:** Milestone 5 (Macroeconomic Module must exist before
multi-module backtesting is meaningful), ADR-005 ecological/governance
framework implementations

---

## Milestone 7 — Technical Foundation *(Complete — v0.7.0)*

**Core deliverable:** Resolve P0 deferred technical debt before Ecological
and Governance Modules require a clean foundation.

**Exit criteria (all met at 2026-05-10 exit):**
- Defensive Programming standards codified in CODING_STANDARDS.md (Issue #224)
- `[SIM-INTEGRITY]` WARNING added: dropped delta for unknown entity, STOCK
  conflict accumulation (Issue #243); duplicate event_id across module outputs
  (Issue #223)
- DEBUG log added: all four modules log when `prior_events` is empty
  (Issues #244, #245)
- `computeSteps()` collapsed-quantile fix for ordinal choropleth attributes
  (Issue #82)
- HCL deferred thresholds reported in CI output without blocking gate
  (Issue #87)
- Compliance scan SCAN-021 clean: 0 violations, 16 warnings (all pre-accepted)
- Module Capability Registry updated to M6-complete state
- Milestone roadmap corrected (this file)

**Dependencies:** Milestone 6 complete.

---

## Milestone 8 — Ecological and Governance Frameworks

**Core deliverable:** Ecological and governance composite scores become
non-null. The radar chart shows all four dimensions with real data.

**Scope:**
- Ecological Module complete: planetary boundary proximity, agricultural
  stress, water stress by watershed, natural capital depletion rate
- Governance Module complete: Institutional Cognitive Integrity Index,
  policy-reality divergence tracking, ghost flight detection
- All four radar chart axes showing real composite scores for any
  scenario with sufficient data
- Coffin Corner indicator implemented: Policy Maneuver Margin composite
  tracking remaining degrees of freedom
- MDA threshold system extended to ecological and governance indicators

**Dependencies:** Milestone 7 (clean foundation required before extending
module complexity), ADR-005 Decisions 5 and 6 (ecological and governance
module contracts — reviewed at M8 entry)

---

## Milestone 9 — Standards Foundation

**Core deliverable:** Canonical unit registry, field-level data certification,
and legibility framework established. Methodological integrity gaps from
STD-REVIEW-004 and ARCH-REVIEW-005 resolved before M10 engine work begins.

**Scope:**
- Canonical unit registry: replace `unit="dimensionless"` placeholders
  with registered physical units (Issues #255, #256 gate)
- Field-level certification chain: `source_registry.admission_status` field
  per approved-sources.md; mandatory data admission tests (Issue #253)
- WGI territorial conventions documented in DATA_STANDARDS.md (Issue #43 area)
- Legibility baseline audit: all user-visible text meets analyst-comprehension
  bar (Issue #255)
- North Star legibility section added to CLAUDE.md (Issue #256)
- Standards Review STD-REVIEW-004 gaps closed (Issues #255–#257)
- Domain Intelligence Council blind stakeholder interviews completed (#235)
- M7 orphan issues triaged and closed or formally re-scoped

**Pre-implementation gates:** Issues #255, #256, #257, #235 must be resolved
before M9 implementation begins.

**Dependencies:** Milestone 8 (M9 standards work assumes M8 ecological and
governance indicators are live — the unit registry must cover real indicators).

---

## Milestone 10 — Engine Integrity and Backtesting

**Core deliverable:** Mean-reversion channels operational, Ecuador backtesting
case added, sparse matrix propagation foundation in place, interpretability
tooling suite available to contributors.

**Scope:**
- Mean-reversion channel (`trend_growth` seeded attribute, Issue #221)
- Ecuador as second Monte Carlo scenario case
- ADR-007 sparse matrix propagation implementation
- Interpretability tooling: propagation trace, equivalence harness, matrix
  visualizer, sparse profiler (Issue #216)
- Engine version gap Issue #139 formally resolved (ADR entry or closed)
- Decimal↔float precision boundary tests hardened

**Dependencies:** Milestone 9 (unit registry and data certification must be
clean before new backtesting cases are added).

---

## Milestone 11 — Political Economy and Conditionality

**Core deliverable:** IMF conditionality modeling, political feasibility
constraints, and elite capture dynamics available for scenario analysis.
Debt sustainability module extended for multi-creditor scenarios.

**Scope:**
- Political Module: electoral calendar, coalition stability, legitimacy cascade
- IMF conditionality impact modeling: policy-space constraint propagation
- Elite capture indicators: concentration of institutional authority,
  dissent tolerance, policy-reality divergence
- Debt sustainability extension: multi-creditor, cross-default triggers
- Fiscal Module: political feasibility constraint on spending paths

**Dependencies:** Milestone 10 (engine integrity work must be complete
before political economy feedback loops are added to the propagation graph).

---

## Milestone 12 — Analyst Tooling and External Sector

**Core deliverable:** Trade and external sector module live; analyst tooling
(propagation trace, export, comparison) polished; governance and branch
protection established.

**Scope:**
- Trade Module: current account, trade balance, terms of trade dynamics
- External sector: capital flows, FDI, remittance channel
- Analyst tooling: scenario comparison, data export, backtesting dashboard
  improvements
- Governance: branch protection on `main`, second governance account (#3, #6)
- Scenario comparison view: side-by-side multi-scenario radar

**Dependencies:** Milestone 11 (political economy channels feed external
sector dynamics — trade policy is a political decision).

---

## Milestone 13 — Methodology Publication and External Validation

**Core deliverable:** The simulation's methodology is publicly documented
and validated by at least one external domain reviewer.

**Scope:**
- Methodology paper: full documentation of every model relationship,
  every assumption, every calibration decision, and every known limitation
- External domain review: at least one development economist or sovereign
  debt specialist reviews the methodology and signs off on the human
  development framework implementation
- `docs/POLICY.md` updated to reflect all methodology positions taken
  through M12, with the external reviewer's name and affiliation
- Technical Steering Committee formation initiated (first institutional
  user engagement sought)
- Public launch preparation: README, CONTRIBUTING.md, and POLICY.md
  written for external contributors, not just internal agents

**Dependencies:** Milestones 5–12 (methodology cannot be published before
the core modules are implemented and validated); external reviewer
recruited no later than M12 midpoint
