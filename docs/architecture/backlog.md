# Architecture Decision Record Backlog

> This file is the single source of truth for ADR number assignment.
> No ADR number may be used in any issue title, document, or code comment
> before it appears in this table with status ASSIGNED.
> Last updated: 2026-07-02 (ARCH-016 added)

## Process

When an architectural question requiring an ADR is identified:
1. File a GitHub issue describing the architectural question — no ADR number in the title
2. Add the issue to this backlog with status PENDING_NUMBER
3. At the next PM Agent HORIZON sweep, the backlog is reviewed for priority against all pending ADRs
4. Before any ADR is drafted, the Architect Agent claims the next available number from this table, marks it ASSIGNED, and begins drafting
5. Only then does the ADR number appear in the issue title and document

## Panel Composition Rule

Before naming the review panel for any ADR, the Architect Agent must consult
`docs/process/agent-raci.md`. Any agent listed as R (Responsible) or C (Consulted)
for the decision type in the RACI chart must either be included in the panel or have
their exclusion explicitly documented with rationale.

**The implementing agent is always required in the ADR panel regardless of panel size.**

Minimum panel by ADR type:

| ADR type | Required panel members |
|---|---|
| Frontend architecture | Architect Agent (author), Frontend Architect Agent, UX Designer Agent, Engineering Lead |
| Simulation engine | Architect Agent (author), Computation Engine Agent, Chief Methodologist, Engineering Lead |
| Data standards | Architect Agent (author), Chief Methodologist, Development Economist, Engineering Lead |
| UX design | Architect Agent (author), UX Designer Agent, Frontend Architect Agent, Engineering Lead |
| Cross-cutting | Architect Agent (author), relevant domain DIC members per RACI, Engineering Lead |

The Architect Agent authors the ADR — they are not a reviewer. The Engineering Lead is
accountable on all ADRs — their sign-off is always required.

## Prerequisite Clause Rule

Any entry whose Notes field contains a prerequisite clause ("Do not author until [condition]")
must have a corresponding GitHub issue filed for that prerequisite before the milestone begins
in which the prerequisite must be completed. The issue is the accountability mechanism; the
Notes clause is a reminder, not a tracker.

At M10 kickoff: verify that ARCH-003's prerequisite (Phase 1 baseline benchmarks) has a
corresponding GitHub issue milestoned to M10. If none exists, file one immediately as part
of the kickoff gate (per MILESTONE_RUNBOOK.md §Kickoff Gate).

Root cause: NM-020 — Phase 1 baseline benchmarks were listed as an ARCH-003 Notes prerequisite
for three milestones without ever being converted to a tracked work item.

## Priority Review

The PM Agent HORIZON sweep must include a backlog review before any ADR activation:
- Are there PENDING_NUMBER entries that should be prioritized over newer requests?
- Does any PENDING entry block another issue or milestone more urgently than the proposed ADR?
- Is the proposed ADR's empirical evidence available, or should it remain PENDING until it is?

Recency bias is explicitly countered by this review. A new architectural question raised in
the current session does not automatically take priority over an older pending entry.

## ADR Registry

| Entry | GitHub Issue | Title | Filed | Status | ADR # | Milestone | Notes |
|---|---|---|---|---|---|---|---|
| ARCH-001 | #508 | Synthetic data framework | 2026-05-19 | ACCEPTED — ADR-007 | 7 | M9 | CM consultation PR #373; accepted 2026-05-23; panel review `docs/adr/reviews/ADR-007-panel-review.md` |
| ARCH-002 | #397 | UX architecture — instrument cluster, viewport, interaction model | 2026-05-21 | ACCEPTED — ADR-008 | 8 | M9 | Accepted 2026-05-22. Panel: UX Designer (conditional ✓), Frontend Architect (conditional ✓), Chief Methodologist (conditional ✓), Engineering Lead (accepted ✓). FA brief required before implementation. |
| ARCH-003 | #217 | Simulation engine computation model — iterative vs. matrix | 2026-04-xx | ACCEPTED — ADR-009 | 9 | M11 | Phase 1 benchmarks complete (#514, 2026-05-31). Accepted 2026-06-03. Panel: CE (conditional ✓), CM (conditional ✓), EL (accepted ✓). Panel review: `docs/adr/reviews/ADR-009-panel-review.md`. |
| ARCH-004 | #366 | Trajectory view as primary instrument | 2026-05-21 | ACCEPTED — ADR-010 | 10 | M9 | Accepted 2026-05-22. Panel: FA (conditional ✓), UX Designer (conditional ✓), CM (conditional ✓), Engineering Lead (accepted ✓). 4 INCORPORATE items applied and approved. FA brief required before implementation. |
| ARCH-005 | #40 | Non-linear propagation architecture — THRESHOLD and CASCADE modes | 2026-06-04 | ACCEPTED — ADR-011 | 11 | M11 | Closes #40 and #29. Accepted 2026-06-04. Panel: CE (accepted ✓), CM (accepted ✓), SD (accepted ✓), EL (accepted ✓). A/B validation report: `docs/backtesting/cascade-validation-report.md`. Panel review: `docs/adr/reviews/ADR-011-panel-review.md`. |
| ARCH-006 | #751 + #752 | External sector module — new module boundary (G5: BilateralTradeShock + CommodityPriceShock) | 2026-06-05 | ACCEPTED — ADR-012 | 12 | M12 | Panel: Architect Agent (author), CE (C), CM (C), Development Economist (C), EL (accepted ✓ 2026-06-05). G5 PR #773 merged to release/m12 2026-06-05. |
| ARCH-007 | #792 | Political economy module — new module boundary (G9: conditionality, political feasibility, elite capture) | 2026-06-05 | ACCEPTED — ADR-013 — EL accepted 2026-06-12 (PR #916) | 13 | M13 | G6 (#392) now unblocked. Pre-G6 condition: `docs/methodology/calibration-basis.md` political economy section required before G6 begins (Chief Methodologist conditional). Panel review: `docs/adr/reviews/ADR-013-panel-review.md`. |
| ARCH-008 | #908 | Alert panel (Zone 1B) master-detail UX architecture | 2026-06-12 | ACCEPTED — ADR-014 — EL accepted 2026-06-12 (PR #926) | 14 | M13 | Required before #852 implementation. Panel: Architect Agent (author), Frontend Architect Agent (C), UX Designer Agent (sign-off ✓ 2026-06-12), EL (accepted ✓ 2026-06-12). Persistent-detail + scan-only compact list. G7 (#852) now unblocked — sprint entry document required before implementation. |
| ARCH-009 | TBD | Model legibility architecture — Evidence Thread Architecture (Zone 1 basis threads, assumption surface, cross-examination mode) | 2026-06-15 | ACCEPTED — ADR-015 | 15 | M14 | Evidence: live UI audit 2026-06-15 (`docs/demo/m14/reviews/2026-06-15-ux-legibility-audit-minister-exercise.md`). EL decisions recorded 2026-06-16 (all 6 pre-implementation decisions resolved). M14 scope: Components 1, 2, 3; Component 4 deferred to M15. Panel: Architect Agent (author), UX Designer Agent (sign-off ✓), Frontend Architect Agent (C), Chief Methodologist (C), Development Economist (C), Business PO (C), Engineering Lead (A — accepted 2026-06-16). |
| ARCH-010 | TBD | Scenario Grounding Architecture — pre-creation data quality preview, scenario grounding strip (initial state + source + vintage), Fidelity panel contextualisation, parameter persistence | 2026-06-15 | ACCEPTED — ADR-016 — EL accepted 2026-06-16 | 16 | M14 | Evidence: live UI input confidence audit 2026-06-15 (`docs/demo/m14/reviews/2026-06-15-ux-input-confidence-audit-minister-exercise.md`). Gap taxonomy IC-1 through IC-7. M14 Wave 1 complete — ADR-016 Accepted 2026-06-16; ADR-015 Wave 2 implementation now unblocked. Entity scope: GRC/JOR/EGY/ZMB. Component 3 (Fidelity contextualisation) deferred to M15. IC-6 deferred to M15 with header label mitigation. |
| ARCH-011 | #845 | Zone 1A information architecture — multi-dimensional encoding across framework × entity × branch × mode; primary cognitive task per mode (Personas 1/2/5); cohort disaggregation path | 2026-06-20 | ACCEPTED — ADR-017 | 17 | M15 | Evidence: Phase 1 design thinking doc `docs/ux/design-thinking/zone-1a-information-architecture.md` (M14 G6c, PR #1033). Tier 1 ADR — UX Designer independent sign-off (NM-042 compliant, same-session acknowledged). Accepted 2026-06-22. Panel: Architect Agent (author), UX Designer (sign-off ✓ 2026-06-22), Frontend Architect (C), Business PO (C), Customer Agent (Layer 3), Chief Methodologist (C), EL (A — accepted ✓ 2026-06-22). Architecture Review: ARCH-REVIEW-007-milestone15.md. |
| ARCH-012 | #1252 | Zone 1B proportional allocation — explicit sub-zone A/B split replacing flex negotiation; MDA alert panel guaranteed minimum; CohortImpactSection internal scroll | 2026-06-25 | ACCEPTED — ADR-018 | 18 | M17 | G3 Phase 2. Path B determination: overflow contract + multi-occupant allocation. Accepted 2026-06-25. Panel: Architect Agent (author), Frontend Architect Agent (C), UX Designer Agent (sign-off ✓ Tier 2), EL (A — accepted ✓ 2026-06-25). Supersedes PR #1235 temporary minHeight:80px guarantee. |
| ARCH-013 | #1360 | Control Plane Column — Mode 2 and Mode 3 implementation: column content by mode, blue/orange cross-layer visual system, shock type taxonomy, history list contracts, sizing constraints, mode transition behavior | 2026-06-26 | ACCEPTED — ADR-019 | 19 | M18 | Accepted 2026-07-02 (PR #1354 merged to release/m18). UX Designer sign-off filed 2026-06-27 (EL-triggered separate session, NM-042 compliant). Panel: Architect Agent (author), UX Designer Agent (independent sign-off ✓), Frontend Architect Agent (C), Business PO (C), Customer Agent (C), EL (A — accepted ✓). Valid Until: M19 entry if Mode 3 scope expands beyond ADR-019 contracts — see ARCH-015. |
| ARCH-014 | #1532 | Emergency instrument economic transmission pattern — capital controls ExternalSectorModule (reserve protection) + MacroeconomicModule (credit contraction) channels; DemographicModule dead subscription bug | 2026-07-02 | PROPOSED — ADR-020 (panel review open 2026-07-03) | 20 | M19 | Discovered at M19 pre-wave. Capital controls currently produce only political legitimacy erosion; reserve protection and credit contraction channels absent. DemographicModule subscribes to wrong event string (capital_controls_imposition vs emergency_policy_capital_controls). ADR establishes the emergency instrument economic transmission pattern for all EmergencyInstrument variants. CM calibration required (Iceland 2008, Malaysia 1998 anchors). Blocks G2D: Iceland (#1553). Panel: Architect Agent (author), CE (C), CM (C — calibration), Development Economist (C), Geopolitical Analyst (C), UX Designer (Tier 2 trace review), EL (A). ADR authored 2026-07-03; panel activation open; G2D entry files after ADR accepted. |
| ARCH-015 | #1540 | Mode 3 constraint-floor search — interaction model (user specifies floor, instrument finds parameter boundary); backend binary search algorithm; result display contract (boundary found / no boundary / boundary uncertainty) | 2026-07-02 | ACCEPTED — ADR-021 — EL accepted 2026-07-02 | 21 | M19 | UX Designer sign-off ✓ 2026-07-02 (separate EL-triggered session, NM-042 compliant, 3 concerns resolved). Concern 3 closed in user-journeys.md; Concerns 1 and 2 tracked as #1564 (CVD gate) and #1563 (AC-016) — pre-ship conditions for G1. G1 sprint entry now open. |
| ARCH-016 | #1543 | ADR-007 amendment — Bayesian posterior layer for CI band calibration from SEN/ZMB backtesting outcomes (Section 8, new); meaninglessness threshold implementation (Section 6, existing design now implemented); is_pre_calibration transition protocol | 2026-07-02 | ASSIGNED | 7 (amendment) | M19 | Amends ADR-007 (not a new ADR number). Section 8 (posterior calibration method): fit coverage multipliers to SEN/ZMB empirical backtesting outcomes; gate condition for is_pre_calibration=False transition (MAGNITUDE_WITHIN_20PCT). Section 6 (meaninglessness threshold): suppress T5 indicators at step 7+ producing [0,1] bands. Panel: Architect Agent (author), CM (C — posterior calibration method), CE (C — implementation), UX Designer (C — is_pre_calibration display contract for #1537), EL (A). Coord issues: #1536 (meaninglessness threshold), #1537 (BandResult visible fields). G3 implementation PRs BLOCKED_ADR until amendment accepted. |
