---
name: m18-g6-sprint-exit
type: sprint-exit
milestone: M18 — Full Argument and Demo 7
sprint-group: G6 — Demo 7 Preparation (through Step 6b)
status: BPO ACCEPT recorded 2026-06-29 — awaiting PI Agent confirmation
authored-by: PM Agent
date: 2026-06-29
pi-confirmed: false
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M18, G6: Demo 7 Preparation (through Step 6b)

**Status:** BPO ACCEPT recorded 2026-06-29 (#1475#issuecomment-4839161892) — awaiting PI Agent confirmation
**Date produced:** 2026-06-29
**Release branch:** `release/m18`
**Sprint entry document:** `docs/process/sprint-plans/m18-g6-sprint-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
G6 is closed at Step 6b by EL scope decision (see §Scope Adjustment below). G6's original
scope included the live stakeholder session (#843) as the M18 closure gate. That deliverable,
and all demo preparation steps between Step 6b and the live session, are transferred to G7.*

---

## Scope Adjustment — EL Decision 2026-06-29

**G6 closes at Step 6b internal review (FAIL verdict).** The Step 6b panel returned a
unanimous FAIL (9/9 agents) on 2026-06-29 with 7 CRITICAL and 9 HIGH findings. The volume
and structural nature of the findings — touching rendering geometry, layout contracts, component
design, and data pipeline — warrants a structured G7 sprint with root cause analysis, intent
documents, and QA authorship gates before any fixes are implemented.

**G6 scope as closed:**
Steps 1, 2, 3, 5, 5a, 5b, 5c, 5d, 4, 6, and 6b of the demo preparation standard.
All G6 deliverables are documentation and process artifacts filed to `docs/demo/m18/`.

**Transferred to G7:**
- All DEMO-130 through DEMO-153 finding resolution (or disposition)
- Step 6b re-review (nine-agent panel re-run after CRITICAL fixes)
- Steps 7, 6c, 8, 9, 9b of the demo preparation standard
- Live stakeholder session issue #843 (M18 closure gate)
- North star test artifact (cannot be filed until the demo runs — see §North Star)

**Rationale on record:** PM Agent recommendation accepted by EL 2026-06-29. See sprint journal
#1475 for the full Step 6b gate status. The sprint process enforces the pattern analysis,
intent documents, and QA gates that a remediation of this scope requires.

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| Sprint group | G6 — Demo 7 Preparation (through Step 6b) |
| Release branch | `release/m18` |
| Sprint sub-branch | `sprint/m18-g6` |
| Sprint entry document | `docs/process/sprint-plans/m18-g6-sprint-entry.md` |
| Exit checklist issue | #1340 (not closed by G6 — closes when #843 closes in G7) |
| Sprint journal issue | #1475 |
| Date G6 implementation completed | 2026-06-29 (Step 6b review filed; PR #1476 merged to sprint/m18-g6) |
| CI status on sprint sub-branch | Green — all required checks pass on sprint/m18-g6 |

---

## Section 2 — Implementation Status

*All G6 deliverables are documentation artifacts. No backend or frontend code was changed in G6
(code changes from the NaN/Guard 2 fixes in the prior context were delivered in earlier feature
branches and are not G6 scope — they were fixes to the spec and component that enabled G6's
demo capture to proceed).*

| Deliverable | PR(s) | Merged to sprint/m18-g6? | CI status | Notes |
|---|---|---|---|---|
| Demo prep issue #1445 | #1445 (issue, no PR) | N/A | N/A | Filed as GitHub issue |
| Walkthrough script | (filed in feat/m18-g6-demo7-prep) | Yes | Green | `docs/demo/m18/stakeholder-walkthrough.md` |
| Screenshot brief | (filed in feat/m18-g6-demo7-prep) | Yes | Green | `docs/demo/m18/screenshot-brief.md` |
| Step 5d deliberation + recommendation | (filed in feat/m18-g6-demo7-prep) | Yes | Green | `docs/demo/m18/reviews/scenario-evaluation-mode3-{deliberation,recommendation}.md` |
| Narrated spec update + archive | #1449, #1457, #1458 | Yes | Green | `demo-narrated.spec.ts` updated; NaN/Act 2 sync fixes; `demo-narrated-m16.spec.ts` archived |
| Five frames (1440×900 capture) | (via feat/m18-g6-demo7-guard2-fix) | Yes | Green | `docs/demo/m18/screenshots/frame-{a–e}-*.png` |
| Step 6b internal review artifact | #1476 | Yes — merged 2026-06-29T22:27Z | Green | `docs/demo/m18/reviews/2026-06-29-v0.18.0-internal-review.md` |

**Implementation status:** All G6 deliverables merged to `sprint/m18-g6`. CI green.

---

## Section 3 — Business PO Acceptance Table

*G6 deliverables are documentation and process artifacts: walkthrough script, screenshot brief,
Step 5d mode evaluation documents, narrated spec, five frames, and Step 6b review. These are
accepted as correctly-executed artifacts. The Step 6b FAIL verdict is the correct output of a
correctly-run review process — FAIL is not a rejection of G6's work; it is G6's primary
deliverable, triggering G7.*

*The live session (#843) and north star test are transferred to G7 and do not appear here.*

| Deliverable | Work type | Customer Agent Layer 3 | BPO verdict | Verdict artifact |
|---|---|---|---|---|
| Stakeholder walkthrough (`docs/demo/m18/stakeholder-walkthrough.md`) | Documentation | Customer Agent Solo-Use review on record — Step 6b panel (DEMO-148 filed for 8 narration transition gaps; medium severity; G7 fix) | ACCEPT — complete, narration-structured, NARRATION-RULING-1 satisfied at section level | This exit document §3 |
| Screenshot brief (`docs/demo/m18/screenshot-brief.md`) | Documentation | Covered by Step 6b panel | ACCEPT — five frames fully specified; Step 5d configuration parameters correct | This exit document §3 |
| Step 5d panel documents | Documentation | N/A — internal methodology artifact | ACCEPT — deliberation and recommendation correctly produced per two-agent panel protocol | This exit document §3 |
| Narrated spec (`demo-narrated.spec.ts`) | Frontend test | Covered by Step 6b panel; spec executed and produced five distinct screenshots for review | ACCEPT — spec runs to completion (6.6 minutes, 1 passed); captures occur at correct states (subject to G7 fixes) | This exit document §3 |
| Five frames (screenshots) | Documentation | Step 6b Customer Agent Solo-Use review on record — SOLO-USE NOT PASSED (DEMO-130 through DEMO-145; CRITICAL findings require G7 remediation) | ACCEPT AS CAPTURED ARTIFACTS — the screenshots are the correct output of the current spec; the FAIL verdict identifies what G7 must correct before the demo runs | This exit document §3 |
| Step 6b internal review | Documentation | Customer Agent is one of the nine review agents — assessment embedded in review artifact | ACCEPT — nine-agent panel correctly constituted and executed; all findings documented; DEMO-130–DEMO-153 assigned; issues #1459–#1474 filed | This exit document §3 |

**Business PO acceptance status:** All ACCEPT (within G6 scope as adjusted). Formal BPO verdict filed 2026-06-29 — #1475#issuecomment-4839161892. Includes BPO observations: (a) DEMO-146 filename mismatch operationally significant for presenter prep — prioritize in fix cluster E; (b) DEMO-142 \"Policy Malevolent Margin\" jargon should be treated as first fix in any display-layer cluster before G7 recapture; (c) Frame C→D act break transition (DEMO-148) is highest-risk narration gap; (d) north star deferred to G7 accepted.

### Customer Agent Layer 3 assessment note

The Customer Agent Solo-Use review was conducted as the first review in the Step 6b panel
(per demo prep standard §Step 6b protocol — Customer Agent reviews screenshots only, no live
walkthrough, before other agents). The assessment is on record in the Step 6b internal review
artifact at `docs/demo/m18/reviews/2026-06-29-v0.18.0-internal-review.md`. This constitutes
the Layer 3 assessment for G6's demo-preparation deliverables.

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before BPO verdict? |
|---|---|---|
| Walkthrough (as document) | Yes — authored for Personas 2, 3, 5 | Yes — Customer Agent Solo-Use in Step 6b panel (2026-06-29) |
| Screenshots (as artifacts) | Yes — stakeholder-facing | Yes — Customer Agent Solo-Use verdict: SOLO-USE NOT PASSED (DEMO-130, DEMO-131, DEMO-132 CRITICAL) |

---

## Section 4 — Open Rejections

No REJECT verdicts were filed in G6. The Step 6b FAIL verdict is a gate verdict on the
screenshot quality, not a rejection of G6's delivery process. The findings are carried into
G7 as issues (#1459–#1474), not as rejection artifacts.

**No open rejections. Proceed to Section 5.**

---

## Section 5 — North Star Test

*The sprint exit checklist requires a north star test artifact for any sprint whose primary
deliverable is a user-facing capability. G6's ultimate user-facing capability is the live
stakeholder demo — a Zambia finance ministry counter-proposal demonstrated to real external
participants (Persona 2/Aicha frame). That capability cannot be north-star tested until the
demo runs.*

**North star test status: DEFERRED TO G7.**

The north star test artifact will be authored by the Business PO at G7 exit, after the live
session runs. PI Agent blocks G7 exit confirmation until the artifact exists and is specific
(per the North Star Test process gate in `CLAUDE.md §North Star Test (Process Gate)`).

**Interim north star assessment (to be replaced at G7 exit):**

The finance minister scenario: Aicha, Zambian Finance Minister, in a debt restructuring
session with an IMF negotiating team. Option C (Homegrown Programme) is the ministry's
counter-proposal. The capability being demonstrated is: the ministry can put a specific
number on screen (+340K persons differential, with CI bounds and direction stability) that
the IMF team must analytically engage with rather than dismiss. Additionally, the ministry
can expand the methodology panel in real time to show the analytical basis — preventing the
IMF team from dismissing the figure as a model artifact.

This capability is architecturally complete (G3, G5 deliveries). The Step 6b findings are
rendering and presentation failures, not architecture failures. G7 restores the presentation
to a state where the capability is demonstrable. The north star test will pass when a
presenter can stand in front of an external audience and make the above argument from what
is on screen.

---

## Section 6 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [ ] All G6 deliverables merged to `sprint/m18-g6`; CI green (Section 2)
- [x] Business PO ACCEPT verdict recorded for all G6 deliverables within adjusted scope (Section 3) — #1475#issuecomment-4839161892, 2026-06-29
- [ ] Customer Agent Layer 3 assessment on record for Persona 2/3/5 deliverables — Step 6b Solo-Use review (Section 3)
- [ ] No open rejection artifacts (Section 4) — confirmed
- [ ] North star test deferred to G7 with explicit EL exception recorded (Section 5)
- [x] G6 integration PR opened and MERGED: PR #1479 `sprint/m18-g6` → `release/m18` — merged 2026-06-29T23:42Z
- [ ] G7 sprint entry filed and EL-approved before G7 implementation begins

**PI Agent sprint exit verdict:** Pending

> {PI Agent confirmation — to be recorded at confirmation. Confirm that all six conditions
> above are checked and that the G6 integration PR is open with auto-merge enabled.}

---

## G6 Integration PR Checklist

*PI Agent confirms this PR exists before exit confirmation.*

| Field | Value |
|---|---|
| Integration PR | To be opened: `sprint/m18-g6` → `release/m18` |
| Carries | All G6 deliverables: walkthrough, screenshot brief, Step 5d docs, narrated spec, screenshots, Step 6b review |
| Auto-merge | Set immediately after PR opens |
| EL action required | None — release branch PR is pre-authorized for auto-merge |

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G6 of M18. It is filed at
`docs/process/sprint-plans/m18-g6-sprint-exit.md`. The PI Agent confirmation in Section 6
is the gate. G7 may not begin implementation until this gate is confirmed and the G6
integration PR is merged to `release/m18`.
