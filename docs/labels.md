# GitHub Label Reference

> Extracted from CLAUDE.md at M4 exit (2026-04-26). CLAUDE.md retains the
> do-not-invent rule and the rejected-label mapping table. This file carries
> the full label definitions, descriptions, and usage guidance.
>
> Use only the labels defined here. Do not invent new labels. If a required
> label is missing, use the closest existing label, add a comment explaining
> which label would be more precise, and note the gap in the PR description.

---

## Workflow / Priority Labels

| Label | Description | When to use |
|---|---|---|
| `horizon:immediate` | Current milestone scope | Work that must complete before current milestone closes |
| `horizon:near-term` | Next 2–3 milestones | Real work, committed timeline, not now |
| `horizon:long-term` | Future, no committed timeline | Architectural vision; no implementation scheduled |

**Choosing between horizon labels:** If the work blocks current milestone
exit criteria → `horizon:immediate`. If it affects design decisions for the
next 2–3 milestones but is not a current blocker → `horizon:near-term`.
If it is important but has no path to implementation in the foreseeable
roadmap → `horizon:long-term`.

---

## Issue Type Labels

| Label | Description | When to use |
|---|---|---|
| `bug` | Something isn't working | Incorrect behaviour, broken output, test failure |
| `enhancement` | New feature or request | New capability, new module, new endpoint |
| `documentation` | Improvements or additions to documentation | CLAUDE.md, ADRs, standards docs, CONTRIBUTING.md, standards reviews |
| `question` | Further information is requested | Design question, clarification needed before implementation can begin |
| `good first issue` | Good for newcomers | Well-scoped, low-risk, does not require deep architecture knowledge |
| `help wanted` | Extra attention is needed | Requires domain expertise, second opinion, or is stalled |

**`bug` vs `enhancement`:** If the code does something it was never supposed
to do, or fails to do something it was explicitly designed to do → `bug`.
If the code works as designed but the design needs to be extended → `enhancement`.

**`documentation` vs `enhancement`:** If the deliverable is a document (ADR,
standards amendment, review, CLAUDE.md update) → `documentation`. If the
deliverable is code + a document (e.g. a new module with an ADR) → `enhancement`.
Do not use `documentation` for issues whose primary deliverable is code.

---

## Compliance Labels

These labels are used exclusively on compliance scan findings. They are not
general-purpose severity labels.

| Label | Description | When to use |
|---|---|---|
| `compliance:critical` | Produces wrong outputs without a visible error signal | Silent correctness failures; data corruption; misleading outputs presented as valid |
| `compliance:major` | Must resolve within current milestone | Compliance deviation that affects the current milestone's exit criteria |
| `compliance:minor` | Address in normal course of development | Style violations, documentation gaps, non-blocking deviations |
| `compliance:exception` | Deviation documented and approved | Self-approved exception per CLAUDE.md §Governance; exception record must exist |
| `compliance:deferred` | Remediation scheduled but not yet started | Known gap with a filed issue and milestone assignment |

**Do not use compliance labels on non-compliance issues.** A bug is not
`compliance:critical` unless it specifically produces a silent incorrect
output that a user cannot detect without reading source code.

---

## Status Labels

| Label | Description | When to use |
|---|---|---|
| `status:known-gap` | Acknowledged deficiency with documented plan to resolve | Architecture limitations accepted in a review (ARCH-REVIEW, STD-REVIEW) with an issue filed |
| `status:parking-lot` | Idea captured, not yet evaluated | Triage outcome: real but not yet assessed for priority or milestone |
| `status:deferred` | Deliberately deferred with documented rationale | Triage outcome: evaluated, assigned to a future milestone, not being worked now |
| `review:periodic` | Must be revisited on a scheduled basis | Items that expire or become stale without re-review (e.g. compliance exceptions, deferred decisions) |
