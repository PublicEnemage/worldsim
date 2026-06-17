---
name: m14-g1-sprint-exit
type: sprint-exit
milestone: M14 — Methodology Publication and External Validation
sprint-group: G1
status: Complete
authored-by: PM Agent
date: 2026-06-17
pi-confirmed: true
release-branch: release/m14
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M14, G1 (Prerequisite Bug Fixes)

**Status:** Complete — PI Agent confirmation recorded
**Date produced:** 2026-06-17
**Release branch:** `release/m14`
**Sprint entry document:** `docs/process/sprint-plans/m14-g1-sprint-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase B/C output).*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M14 — Methodology Publication and External Validation |
| Sprint number | G1 |
| Release branch | `release/m14` |
| Sprint groups | G1 |
| Sprint entry document | `docs/process/sprint-plans/m14-g1-sprint-entry.md` |
| Exit checklist issue | #968 |
| Date implementation completed | 2026-06-17 |
| CI status on release branch | Green |

---

## Section 2 — Implementation Status

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| G1 — #961 entity selector, #962 step counter, #963 choropleth labels | #1006 | Yes | Green | `release/m14`; all 6 required checks pass |

**Implementation status:** All merged, CI green

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| #961 entity selector (GRC/JOR/EGY/ZMB) | Frontend | Filed — intent doc §9 (N/A — form affordance, not indicator output) | ACCEPT | `docs/process/intents/M14-G1-2026-06-16-prerequisite-bugs.md §9` |
| #962 step counter URL-load fix | Frontend | Filed — intent doc §9 (PASS — "Step 3 / 3 — Complete" self-interpreting) | ACCEPT | `docs/process/intents/M14-G1-2026-06-16-prerequisite-bugs.md §9` |
| #963 choropleth human-readable labels | Frontend | Filed — intent doc §9 (PASS — "Reserve Coverage (months)" interpretable by Persona 2 without mediation; threshold Layer 3 carried by Zone 1B ADR-014) | ACCEPT | `docs/process/intents/M14-G1-2026-06-16-prerequisite-bugs.md §9` |

**Business PO acceptance status:** All ACCEPT — 2026-06-17

### Notes on Customer Agent Layer 3 assessments

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| #961 entity selector | Yes (Persona 2 primary) | Yes — filed in intent doc §9 before BPO verdict |
| #962 step counter | Yes (Persona 2 primary) | Yes — filed in intent doc §9 before BPO verdict |
| #963 choropleth labels | Yes (Persona 2 primary) | Yes — filed in intent doc §9 before BPO verdict |

**BPO validation method:** Playwright at 1440×900 (4 probes via `tests/e2e/bpo-validate-g1.spec.ts`, run 2026-06-17 — all pass). Natural entry state navigation; no developer shortcuts.

**BPO observations:**
- BPO-1: entity selector visible with GRC/JOR/EGY/ZMB in 1977ms (P-4 90s ceiling met) ✅
- BPO-2: ZMB selection → `configuration.entities[0]==="ZMB"` in API (SF-1 absent) ✅
- BPO-3: URL-loaded completed scenario "Step 3 / 3 — Complete" in 1002ms, stable after 1s (SF-2 absent) ✅
- BPO-4: choropleth attribute selector — 6 options, no underscore in any label portion (SF-3 absent); `reserve_coverage_months` AC-7 confirmed at Step 4 Verify ✅

**North star check (P-7):** The Zambian finance ministry analyst can open WorldSim, select ZMB, create a scenario, and see ZMB-calibrated outputs — not Greece's. The step counter correctly positions the analyst in the scenario timeline. Choropleth labels are human-readable. These fixes are the prerequisite for Demo 5 with real external participants representing non-GRC entities. P-7 PASS.

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on release branch — PR #1006 merged to `release/m14`; all 6 required checks pass
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable — three ACCEPT verdicts on record in intent doc §9; filed 2026-06-17
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed before Business PO verdict — Layer 3 assessment filed in intent doc §9 prior to BPO verdict
- [x] No open rejection artifacts — confirmed; no REJECT artifacts exist for G1
- [x] Near-miss entry for each rejection — no rejections in G1; no near-miss obligation from rejections

**Pre-existing issue found during Step 4 Verify:** Bug #1007 (`recompute-badge` not visible after `apply-control-change`) was discovered during G1 Step 4 and filed as a pre-existing defect. It is not a G1 rejection — it predates G1 and is filed for G2 or follow-on scope. PI Agent confirms this is not a G1 exit blocker.

**PI Agent sprint exit verdict:** Confirmed — all exit conditions satisfied

**PI Agent confirmation:**

> G1 sprint exit conditions are satisfied as of 2026-06-17. Implementation (PR #1006) is merged
> to `release/m14` with CI green. Business PO ACCEPT verdict is filed for all three G1
> deliverables (#961, #962, #963) with Customer Agent Layer 3 assessment on record prior to each
> verdict. No rejection artifacts exist. Issues #961, #962, #963 are closed. Pre-existing bug #1007
> is filed and not a G1 exit blocker.
>
> G1 is closed.

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G1 of M14. It supersedes any informal exit
notation in SESSION_STATE.md for this sprint. Filed at
`docs/process/sprint-plans/m14-g1-sprint-exit.md`.
