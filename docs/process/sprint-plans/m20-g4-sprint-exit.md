---
name: m20-sprint-g4-exit
type: sprint-exit
milestone: M20 — Analytical Evidence Portfolio and Demo 9
sprint-group: G4
status: PI-confirmed
authored-by: PM Agent
date: 2026-07-09
pi-confirmed: true
release-branch: release/m20
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M20 G4 — DEMO Maintenance and Test Fix

**Status:** PI-confirmed — all exit conditions satisfied
**Date produced:** 2026-07-09
**Release branch:** `release/m20`
**Sprint entry document:** `docs/process/sprint-plans/m20-g4-sprint-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate`.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M20 — Analytical Evidence Portfolio and Demo 9 |
| Sprint number | G4 |
| Release branch | `release/m20` |
| Sprint groups | G4 |
| Sprint entry document | `docs/process/sprint-plans/m20-g4-sprint-entry.md` |
| Exit checklist issue | #1773 |
| Sprint journal issue | #1834 |
| Date implementation completed | 2026-07-09 (integration PR #1845 merged 02:57 UTC) |
| CI status on release branch | Green |

---

## Section 2 — Implementation Status

| Group | Integration PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| G4 — DEMO maintenance + test fix | #1845 | Yes — 2026-07-09 | Green | 5 feature PRs (#1840–#1844) + fix PRs (#1846, #1848, #1849, #1850) merged to sprint branch before integration |

**Implementation status:** All merged, CI green.

**Note — fix PRs after integration PR opened:** PRs #1848 (PSP `isAttached` API), #1849 (disabled-button guard), #1850 (FP narrowMargin fix) were opened against `sprint/m20-g4` after #1845 was opened, resolving CI failures found during integration review. PR #1846 (CM-A + CM-C pool ordering fix) similarly. All four fix PRs merged to sprint branch before #1845 finally passed CI on `release/m20`. NM-102 filed for the four-root-cause pattern. This does not affect sprint exit validity — all deliverables are confirmed green on the release branch.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| DEMO-217 — Act 1 → Act 2 in-viewport nav link | Frontend | PASS — filed in-session 2026-07-09 | **ACCEPT (unconditional)** | `docs/process/sprint-plans/m20-g4-sprint-exit.md §BPO Verdicts` |
| DEMO-233 (#1775) — WARNING badge alongside CLEAR | Frontend | PASS — filed in-session 2026-07-09 | **ACCEPT (unconditional)** | `docs/process/sprint-plans/m20-g4-sprint-exit.md §BPO Verdicts` |
| DEMO-234 (#1776) — Precision label vs CI label | Frontend | PASS (strong) — filed in-session 2026-07-09 | **ACCEPT (unconditional)** | `docs/process/sprint-plans/m20-g4-sprint-exit.md §BPO Verdicts` |
| #1759 / NM-099 — asgi_client pool ordering fix | Test infrastructure | N/A — not Persona 2/3/5 | **ACCEPT (unconditional)** | `docs/process/sprint-plans/m20-g4-sprint-exit.md §BPO Verdicts` |
| #1791 / NM-101 — G2C Type B baseline pre-run | Test logic | N/A — not Persona 2/3/5 | **ACCEPT (unconditional)** | `docs/process/sprint-plans/m20-g4-sprint-exit.md §BPO Verdicts` |

**Business PO acceptance status:** All five deliverables ACCEPT (unconditional).

### BPO Verdicts

**DEMO-217 — ACCEPT (unconditional)**
The in-viewport navigation link ("View distributional comparison →") is present in the `constraint-search-found` state, visible without scrolling at 1440×900, and navigates Persona 2 directly from the Act 1 boundary result to the Act 2 distributional comparison in one click. The 38-second navigation gap identified at Demo 8 Q7 is closed. All 6 E2E ACs pass CI green.

*North Star test:* The Zambian finance ministry analyst completing a constraint-floor search can immediately navigate to the distributional consequence of operating near that boundary — one click, no scenario-list navigation. The capability changes what she can demonstrate in a restructuring briefing: not just "this is the floor" but "this is what living near it does to headcount poverty," without losing the thread.

**DEMO-233 (#1775) — ACCEPT (unconditional)**
The WARNING badge appears alongside CLEAR in Zone 1B when the focal indicator value is within 5% of the MDA floor. The production narrowMargin comparison uses `Math.round(pct * 10000) / 10000` to avoid IEEE 754 accumulation — compliant with CODING_STANDARDS §Monetary Arithmetic. The exact-boundary case (value = floor × 1.05) correctly produces no WARNING badge (`< 0.05` strict). All 8 E2E ACs pass CI green.

*North Star test:* "Can I see both CLEAR and a WARNING if the margin is narrow?" (Stakeholder Q2) is now answered by the display itself. The analyst can read "CLEAR | WARNING — reserve coverage 0.420 / floor 0.400" and state the position to the negotiating table without further computation.

**DEMO-234 (#1776) — ACCEPT (unconditional)**
The tolerance band is labelled "binary search precision: ±0.01" with an inline note "Not a statistical CI — see CI bands in trajectory view." The pre-existing "±0.00 precision" label that prompted Lucas's Q1 confusion is replaced. The two quantities (search stopping criterion vs distributional uncertainty) are visually distinct and self-interpreting without tooltip or documentation reference. All 9 E2E ACs pass CI green.

**#1759 / NM-099 — ACCEPT (unconditional)**
`pytest -m backtesting -k test_m19_cm_b` passes in isolation. The asgi_client pool ordering dependency is resolved in CM-B, CM-A, and CM-C fixtures. NM-102 documents the incomplete initial fix (CM-A/CM-C missed in #1841, corrected in #1846).

**#1791 / NM-101 — ACCEPT (unconditional)**
All 7 Type B test methods in `test_m19_g2c_scenario_runs.py` pre-run the baseline scenario before passing its ID as `baseline_run_id`. Direction verdicts are now real (GRC: COUNTER_FACTUAL_BETTER confirmed). AEP authorship integrity restored: G2C Type B advisory output is now reliable for AEP evidence entries.

### Layer 3 assessment notes

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| DEMO-217 | Yes — Persona 2 (navigation workflow) | Yes — filed in-session before BPO verdict |
| DEMO-233 | Yes — Persona 2, Persona 5 (Aicha in-session Q2) | Yes — filed in-session before BPO verdict |
| DEMO-234 | Yes — Persona 2 (Lucas analytical scrutiny) | Yes — filed in-session before BPO verdict |
| #1759 / NM-099 | No — test infrastructure | N/A |
| #1791 / NM-101 | No — test logic | N/A |

**Customer Agent finding (DEMO-233 future gap):** WARNING badge carries no inline sub-label quantifying "< 5% above floor." Persona 5 cold-reader context would benefit from a tooltip. Not a Layer 3 blocking gap for Persona 2; filed as future enhancement for M21 instrument polish backlog alongside #1777.

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on release branch (Section 2) — #1845 merged 2026-07-09, CI green
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable, or EL exception on record (Section 3) — all five ACCEPT (unconditional)
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed before Business PO verdict (Section 3) — DEMO-217, DEMO-233, DEMO-234 all Layer 3 PASS; filed in-session before BPO verdicts
- [x] No open rejection artifacts (Section 4) — confirmed
- [x] Near-miss entry filed for each rejection in this sprint (Section 4) — no rejections; NM-102 filed for four-root-cause CI failure pattern (PR #1851, auto-merge set)

**PI Agent sprint exit verdict:** Confirmed — all exit conditions satisfied.

**PI Agent confirmation:**

> All five G4 exit conditions are satisfied. Implementation is green on `release/m20` (#1845 merged 2026-07-09). Business PO ACCEPT on record for all five deliverables. Customer Agent Layer 3 PASS for all three Persona 2/3/5 deliverables (DEMO-217, DEMO-233, DEMO-234), filed before BPO verdicts. No open rejection artifacts. NM-102 filed for the cascading CI failure pattern. G4 sprint is confirmed closed.
>
> Issues to close: #1759, #1775, #1776, #1791. DEMO-217 has no standalone issue number — tracked via sprint entry and this exit document.
>
> — PI Agent (2026-07-09)

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G4 of M20. It supersedes any informal exit notation in SESSION_STATE.md for this sprint. Filed at `docs/process/sprint-plans/m20-g4-sprint-exit.md`.
