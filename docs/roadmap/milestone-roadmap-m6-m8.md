# Milestone Roadmap — M6 through M8

> Extracted from CLAUDE.md at M4 exit (2026-04-26). Updated at M7 exit
> (2026-05-10) to correct M7 theme and cascade M8/M9. CLAUDE.md carries the
> current milestone inline; this file carries the committed scope for
> M6 through M9. GitHub Milestones carry the live issue lists.

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

## Milestone 9 — Methodology Publication and External Validation

**Core deliverable:** The simulation's methodology is publicly documented
and validated by at least one external domain reviewer.

**Scope:**
- Methodology paper: full documentation of every model relationship,
  every assumption, every calibration decision, and every known limitation
- External domain review: at least one development economist or sovereign
  debt specialist reviews the methodology and signs off on the human
  development framework implementation
- `docs/POLICY.md` updated to reflect all methodology positions taken
  through M8, with the external reviewer's name and affiliation
- Technical Steering Committee formation initiated (first institutional
  user engagement sought)
- Public launch preparation: README, CONTRIBUTING.md, and POLICY.md
  written for external contributors, not just internal agents

**Dependencies:** Milestones 5–8 (methodology cannot be published before
the core modules are implemented and validated); external reviewer
recruited no later than M8 midpoint
