# Architecture Decision Record Backlog

> This file is the single source of truth for ADR number assignment.
> No ADR number may be used in any issue title, document, or code comment
> before it appears in this table with status ASSIGNED.
> Last updated: 2026-05-23

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
| Simulation engine | Architect Agent (author), Chief Engineer, Chief Methodologist, Engineering Lead |
| Data standards | Architect Agent (author), Chief Methodologist, Development Economist, Engineering Lead |
| UX design | Architect Agent (author), UX Designer Agent, Frontend Architect Agent, Engineering Lead |
| Cross-cutting | Architect Agent (author), relevant domain DIC members per RACI, Engineering Lead |

The Architect Agent authors the ADR — they are not a reviewer. The Engineering Lead is
accountable on all ADRs — their sign-off is always required.

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
| ARCH-003 | #217 | Simulation engine computation model — iterative vs. matrix | 2026-04-xx | ASSIGNED — ADR-009 | 9 | M11 | Do not author until M11 Phase 1 baseline benchmarks complete |
| ARCH-004 | #366 | Trajectory view as primary instrument | 2026-05-21 | ACCEPTED — ADR-010 | 10 | M9 | Accepted 2026-05-22. Panel: FA (conditional ✓), UX Designer (conditional ✓), CM (conditional ✓), Engineering Lead (accepted ✓). 4 INCORPORATE items applied and approved. FA brief required before implementation. |
