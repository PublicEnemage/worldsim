# Milestone MILESTONE_NUMBER Exit Checklist — MILESTONE_NAME

**This Issue must be the last one closed before Milestone MILESTONE_NUMBER closes.**
Every checkbox must be checked. No exceptions without documented rationale added
as a comment on this Issue.

---

## Milestone Scope Verification

- [ ] All Issues assigned to Milestone MILESTONE_NUMBER are either closed or explicitly
      deferred to Milestone MILESTONE_NUMBER+1 with a comment on this Issue documenting
      the deferral rationale.
- [ ] No Issues are in an ambiguous state (open, assigned to this milestone, with no
      activity in the last two weeks) without an explanation.

---

## Compliance

- [ ] Full compliance scan run against all new Milestone MILESTONE_NUMBER code and
      recorded in `docs/compliance/scan-registry.md` with a Milestone-exit trigger entry.
- [ ] Scan registry entry references this Issue by number.
- [ ] All **Critical** findings are either remediated (PR merged) or carry an approved
      exception with full audit trail (rationale, risk acknowledgment, approver,
      review date).
- [ ] All **Major** findings are either remediated or carry an approved exception with
      review dates documented and approver on record.
- [ ] All **Minor** findings have open GitHub Issues with appropriate compliance labels.
      Deferred Minor findings have target resolution dates set.
- [ ] No exception review dates have passed without renewal or resolution.
- [ ] No deferred findings are past their target dates without updated rationale.
- [ ] CF-001-F01 Engineering Lead architectural decision on `Dict[str, float]` vs
      `Decimal` at the simulation state store level is documented before any simulation
      module writes monetary arithmetic against the attributes dict.

---

## Standards

- [ ] All new simulation modules introduced in Milestone MILESTONE_NUMBER have
      corresponding ADRs in `docs/adr/` with Accepted status.
- [ ] All ADRs introduced in Milestone MILESTONE_NUMBER have at least one Mermaid
      diagram in `docs/architecture/` of the appropriate type.
- [ ] All diagrams are current with the actual implementation. No interface changes
      were merged without a corresponding diagram update in the same commit.
- [ ] CI lint job is passing (`ruff check`, `mypy`). No lint suppression comments
      (`# noqa`, `# type: ignore`) were added without a comment explaining why.
- [ ] CI compliance-scan job is passing (or all `COMPLIANCE-WARN` outputs have been
      reviewed and either accepted or converted to compliance finding Issues).
- [ ] All new Python files follow the naming conventions in `CODING_STANDARDS.md`.
- [ ] All new commit messages follow Conventional Commits format.

---

## Testing

- [ ] Unit test coverage is acceptable for all new Milestone MILESTONE_NUMBER code.
      Every public method has at least one happy-path test, one error-condition test,
      and one boundary-value test.
- [ ] Backtesting suite is passing, or the empty suite is explicitly documented as
      acceptable at this milestone with a comment on this Issue explaining why.
- [ ] Human cost ledger outputs are tested explicitly where applicable — not just
      checking that fields are non-null, but that they respond correctly to the inputs
      that drive them.
- [ ] No test is testing internal implementation details rather than the public contract.

---

## Governance

- [ ] All admin bypass merges during Milestone MILESTONE_NUMBER (merges without
      required reviews) have corresponding audit trail Issues with the single-principal
      limitation disclosure verbatim as required by `CLAUDE.md § Governance`.
- [ ] All Issues with the `review:periodic` label have been reviewed if their review
      date has passed during this milestone.
- [ ] The compliance scan registry (`docs/compliance/scan-registry.md`) is current.
      The Milestone-exit scan entry for Milestone MILESTONE_NUMBER exists before this
      checklist is closed.

---

## Standards License Audit

For each ADR active in this milestone, the Engineering Lead confirms its
license status before the milestone closes. An ADR whose license status is
not CURRENT at milestone close requires documented rationale.

- [ ] ADR-001 (Simulation Core Data Model) — license status confirmed CURRENT,
      OR rationale documented below for why milestone closes with UNDER-REVIEW.
- [ ] ADR-002 (Input Orchestration Layer) — license status confirmed CURRENT,
      OR rationale documented below for why milestone closes with UNDER-REVIEW.
- [ ] All ADRs introduced during Milestone MILESTONE_NUMBER — license status
      confirmed CURRENT at the standards version in effect at milestone close.
- [ ] No UNDER-REVIEW ADR has a dependent ADR that reached Accepted status
      during this milestone (the dependency rule was not violated).
- [ ] If any UNDER-REVIEW ADR exists at milestone close: a GitHub Issue is open
      documenting the standards update required for renewal, with a target
      resolution date no later than the midpoint of Milestone MILESTONE_NUMBER+1.

**UNDER-REVIEW rationale** (complete if any ADR is not CURRENT at close):

> *(Engineering Lead documents here why closure proceeds without renewal,
> including the specific standards amendment pending, the open Issue tracking
> it, and the risk assessment for proceeding with UNDER-REVIEW status.)*

---

## Engineering Lead Sign-off

- [ ] Socratic Agent TEST session completed on Milestone MILESTONE_NUMBER architecture.
      The session confirmed genuine understanding, not just familiarity.
- [ ] Engineering Lead can explain the core architectural decisions introduced in
      Milestone MILESTONE_NUMBER without consulting the code — including what contracts
      they enforce and what would break if a constraint were removed.
- [ ] Milestone MILESTONE_NUMBER scope is complete per the definition in `CLAUDE.md`.
      If scope was reduced, the reduction is documented as a comment on this Issue with
      rationale.
- [ ] The next milestone's creation ceremony has been initiated (or this is the final
      milestone).
