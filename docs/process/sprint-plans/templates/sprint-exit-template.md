---
name: {milestone-slug}-sprint-{N}-exit
type: sprint-exit
milestone: M{N} — {milestone name}
sprint-group: {G1/G2/... or "all groups"}
status: In-progress
authored-by: PM Agent
date: {YYYY-MM-DD}
pi-confirmed: false
release-branch: release/m{N}
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — {Milestone Name}, Sprint {N}

**Status:** In-progress — awaiting PI Agent confirmation
**Date produced:** {YYYY-MM-DD}
**Release branch:** `release/m{N}`
**Sprint entry document:** `docs/process/sprint-plans/{milestone-slug}-sprint-{N}-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase B/C output).
Changes to this template require PM Agent authorship and EL endorsement.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M{N} — {milestone name} |
| Sprint number | {N} |
| Release branch | `release/m{N}` |
| Sprint groups | {G1, G2, G3, …} |
| Sprint entry document | `docs/process/sprint-plans/{milestone-slug}-sprint-{N}-entry.md` |
| Exit checklist issue | #{exit-checklist-issue-number} |
| Date implementation completed | {YYYY-MM-DD} |
| CI status on release branch | {Green / Red — BLOCKING} |

---

## Section 2 — Implementation Status

*All groups must be merged and CI must be green on the release branch. This is necessary but
not sufficient for sprint exit. (Authority: sprint-planning-sop.md §Sprint Exit Gate condition 1)*

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| {G1 — description} | #{PR-number} | {Yes / No — BLOCKING} | {Green / Red — BLOCKING} | |
| {G2 — description} | #{PR-number} | {Yes / No — BLOCKING} | {Green / Red — BLOCKING} | |

**Implementation status:** {All merged, CI green / BLOCKED — see above}

---

## Section 3 — Business PO Acceptance Table

*One row per user-facing deliverable. Business PO verdict (ACCEPT or REJECT) must be filed
and on record before the sprint exit gate passes.
(Authority: sprint-planning-sop.md §Sprint Exit Gate condition 2;
docs/process/acceptance-protocol.md §Part 1)*

*If no user-facing deliverables (infrastructure sprint): "Infrastructure sprint — Business PO
acceptance not required. Proceed to Section 5."*

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| {deliverable 1} | {Frontend / Backend / Documentation / Analytics} | {Filed at: path} | {ACCEPT / REJECT / Pending} | {path or "Pending"} |
| {deliverable 2} | {Frontend / Backend / Documentation / Analytics} | {Filed at: path or N/A — non-Persona-2/3/5} | {ACCEPT / REJECT / Pending} | {path or "Pending"} |

**Business PO acceptance status:** {All ACCEPT / Open rejections — see Section 4 / Pending}

### Notes on Customer Agent Layer 3 assessments

*For deliverables serving Personas 2, 3, or 5: the Customer Agent Layer 3 assessment is a
precondition for the Business PO verdict — not a follow-up. The Business PO does not execute
the Validate step before the Layer 3 assessment is on record.*

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| {deliverable 1} | {Yes / No} | {Yes / N/A — non-Persona-2/3/5} |
| {deliverable 2} | {Yes / No} | {Yes / N/A — non-Persona-2/3/5} |

---

## Section 4 — Open Rejections

*Any REJECT verdicts from Section 3 and their resolution status. A sprint with an unresolved
rejection artifact does not exit.*

*If no rejections: "No open rejections. Proceed to Section 5."*

| Rejection artifact | Deliverable | Defect named | Remediation scope | Resolution status |
|---|---|---|---|---|
| `docs/process/rejections/REJECT-NNN-YYYY-MM-DD-{desc}.md` | {deliverable} | {acceptance criterion that failed} | {return to Step 1 / Step 3 — specify} | {Re-accepted / EL exception recorded / Blocking} |

**Near-miss entries required for each rejection:**

| Rejection | Near-miss entry | NM number |
|---|---|---|
| REJECT-NNN | {filed / not yet filed — BLOCKING} | {NM-NNN} |

---

## Section 5 — PI Agent Sprint Exit Confirmation

*PI Agent reviews all exit conditions and confirms they are satisfied before the sprint exit
checklist issue is closed. PI Agent does not produce the verdicts — PI Agent confirms they
exist and are complete.*

**Exit conditions checklist (PI Agent):**

- [ ] All implementation groups merged; CI green on release branch (Section 2)
- [ ] Business PO ACCEPT verdict filed for each user-facing deliverable, or EL exception on record (Section 3)
- [ ] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed before Business PO verdict (Section 3)
- [ ] No open rejection artifacts (Section 4)
- [ ] Near-miss entry filed for each rejection in this sprint (Section 4)

**PI Agent sprint exit verdict:** {Confirmed — all exit conditions satisfied / BLOCKED — see above}

**PI Agent confirmation:**

> {PI Agent confirmation statement — to be filled at confirmation time.
> If blocked: name the specific condition that is unsatisfied and what must change.}

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for sprint {N} of M{N}. It supersedes any informal
exit notation in SESSION_STATE.md for this sprint. It is filed at
`docs/process/sprint-plans/{milestone-slug}-sprint-{N}-exit.md`.

*The PI Agent confirmation in Section 5 is the gate. The sprint closes when the PI Agent's
verdict is "Confirmed." No subsequent sprint group begins until this verdict is recorded.*
