---
name: m19-g1-sprint-exit
type: sprint-exit
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G1
status: Confirmed
authored-by: PM Agent
date: 2026-07-03
pi-confirmed: true
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M19, G1

**Status:** Confirmed — PI Agent exit conditions satisfied
**Date produced:** 2026-07-03
**Release branch:** `release/m19`
**Sprint entry document:** `docs/process/sprint-plans/m19-g1-sprint-entry.md`

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| Sprint number | G1 |
| Release branch | `release/m19` |
| Sprint groups | G1 |
| Sprint entry document | `docs/process/sprint-plans/m19-g1-sprint-entry.md` |
| Exit checklist issue | #1535 |
| Sprint journal issue | #1570 |
| Date implementation completed | 2026-07-03 |
| CI status on sprint branch | Green (run 28630671876 — all required checks pass) |

---

## Section 2 — Implementation Status

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| G1 — Form 3 + constraint-floor search endpoint | #1574 | Yes — 2026-07-03 | Green | Implementation: ControlPlaneColumn Form 3, binary search endpoint, AC-016, MV-001 |
| G1 — E2E mock fixture fix | #1579 | Yes — 2026-07-03 | Green | Fixed 4 bugs in enterMode3WithFocalCohort; playwright-e2e PASSED run 28630671876 |

**Implementation status:** All merged, CI green on `sprint/m19-g1`

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| Mode 3 constraint-floor search (#1540) | Frontend + Backend | CONDITIONAL PASS — filed #1540 comment 2026-07-03 | **ACCEPT** | #1540 comment 2026-07-03 |
| AC-016 column visibility CI assertion (#1563) | Frontend (pre-ship condition) | N/A — infrastructure condition | **ACCEPT** (same PR as #1540) | #1563 close comment |
| MV-001 CVD validation (#1564) | Frontend (pre-ship condition) | N/A — infrastructure condition | **ACCEPT** (same PR as #1540) | #1564 close comment |

**Business PO acceptance status:** All ACCEPT

### North star test artifact (ADR-021 Tier 1 — required)

**Scenario:** Aicha (P5), Zambia 2022 IMF restructuring session.

**Capability:** Constraint-floor search in Mode 3 — returns the minimum fiscal multiplier that keeps the bottom-quintile poverty headcount above the recovery floor.

**Assessment:** With constraint-floor search, Aicha's team can answer: "The binding constraint is 0.83 multiplier. Our proposal (0.85) has a 2-point buffer above the constraint boundary." Previously, the team could only say "our proposal clears the floor" — which the IMF team can rebut with "prove you're not at the boundary." The constraint-floor search lets the ministry name the constraint and show they are above it. This changes what the minister's team can argue at the restructuring table.

**North star test result: PASS**

### Customer Agent Layer 3 — condition tracking

| Deliverable | Serves P2/P3/P5? | L3 filed before verdict? | Conditions |
|---|---|---|---|
| Constraint-floor search (#1540) | Yes — P2 (Lucas), P5 (Aicha) | Yes — #1540 comment 2026-07-03 | 2 Demo 8 conditions (tolerance band display, AC-12 real key) — non-blocking for G1 exit |

**Demo 8 conditions (tracked, non-blocking for G1 exit):**
- [ ] Tolerance band (±0.01) visible in FOUND state UI (verify before Demo 8 Act 1)
- [ ] AC-12 resolved with real structural-absence indicator key before Demo 8

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on sprint branch (Section 2)
  - PR #1574 (implementation) and PR #1579 (E2E fix) both merged to `sprint/m19-g1`
  - CI run 28630671876: all required checks pass (changes, lint, test-backend, compliance-scan, playwright-e2e)
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable (Section 3)
  - #1540 ACCEPT — filed #1540 comment 2026-07-03; north star test artifact embedded
  - #1563 ACCEPT — pre-ship condition satisfied (AC-016 in CI)
  - #1564 ACCEPT — pre-ship condition satisfied (MV-001 CVD verification in PR #1574)
- [x] Customer Agent Layer 3 assessment on record before Business PO verdict (Section 3)
  - CONDITIONAL PASS filed at #1540 comment 2026-07-03
  - Filed before BPO ACCEPT comment (same session, BPO comment follows CA comment)
  - Disclosed: same-session assessment
- [x] No open rejection artifacts (Section 4)
- [x] NM-084 filed — root cause: E2E mock route unverified against api_contracts.yml
  - Process improvement: QA Lead open items requiring FA confirmation are now blocking conditions on intent approval gate
  - Filed in `docs/process/near-miss-registry.md` on `feat/m19-g1-fix-e2e-mock` (commit 0e1bc93), pending coordination lane merge

**PI Agent sprint exit verdict: Confirmed — all exit conditions satisfied**

**PI Agent confirmation:**

> G1 sprint exit conditions are satisfied as of 2026-07-03. All PRs merged to sprint/m19-g1,
> CI green (playwright-e2e passing with AC-016 verified in run 28630671876). Business PO ACCEPT
> on record for all three G1 deliverables. Customer Agent Layer 3 CONDITIONAL PASS filed before
> BPO verdict. No open rejections. NM-084 filed and pending coordination lane merge.
>
> Two Demo 8 conditions from the Customer Agent Layer 3 assessment are tracked in this exit
> document (tolerance band display, AC-12 real indicator key) — these are non-blocking for G1
> exit but are blocking for Demo 8 Act 1 clearance.
>
> Next action: integration PR sprint/m19-g1 → release/m19.
>
> — PI Agent (in-session, 2026-07-03)

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G1 of M19. It supersedes any informal exit
notation in SESSION_STATE.md for this sprint group. It is filed at
`docs/process/sprint-plans/m19-g1-sprint-exit.md`.
