---
name: m19-g8-sprint-exit
type: sprint-exit
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G8
status: Confirmed
authored-by: PM Agent
date: 2026-07-04
pi-confirmed: true
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M19, Sprint Group G8

**Status:** Confirmed — PI Agent gate passed 2026-07-04
**Date produced:** 2026-07-04
**Release branch:** `release/m19`
**Sprint entry document:** `docs/process/sprint-plans/m19-g8-sprint-entry.md`
**Sprint journal issue:** #1741 (closed at integration PR merge)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase B/C output).*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| Sprint number | G8 |
| Release branch | `release/m19` |
| Sprint groups | G8 |
| Sprint entry document | `docs/process/sprint-plans/m19-g8-sprint-entry.md` |
| Exit checklist issue | #1535 |
| Date implementation completed | 2026-07-04 |
| CI status on sprint branch | All required checks GREEN — PRs #1744, #1745, #1746: changes ✅ lint ✅ test-backend ✅ compliance-scan ✅ |

---

## Section 2 — Implementation Status

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| G8 — `_classify_direction` primary_indicator fix | #1744 | Yes — 2026-07-04 | Green (required checks) | NM-098 fix; `_COMPOSITE_INDICATOR_FIELDS` routing branch added |
| G8 — CM_A/B/C baseline pre-advance | #1745 | Yes — 2026-07-04 | Green (required checks) | Root cause: TYPE_B tests created baseline but never advanced it before `run_harness`; 7 pre-advance loops added across cm_a/b/c |
| G8 — CM_B ARG baseline n_steps cap | #1746 | Yes — 2026-07-04 | Green (required checks) | ARG baseline n_steps=2 vs CF n_steps=3; loop now uses baseline's own n_steps; step-3 magnitude assertion correctly RED pending CM-D |

**Implementation status:** All merged; required CI checks green on sprint/m19-g8.

**GRC AC-1 live verification:** Workflow dispatch run `28719741291` (2026-07-04, `sprint/m19-g8`,
`force_backtesting=true`) confirmed `TestAC1MagnitudeDivergence` 3/3 PASSED:
- `test_grc_counterfactual_hd_composite_magnitude_at_step_4`: PASSED
- `test_grc_counterfactual_per_step_diff_positive_at_step_4`: PASSED
- `test_grc_counterfactual_direction_verdict_not_advisory_after_implementation`: PASSED

**ARG AC-1 status:** CM_B magnitude tests remain RED pending CM-D (Kirchner 2003 recovery
inputs for ARG baseline step 3). Setup 409 crash eliminated — failures now surface at the
correct magnitude assertion. This is expected per sprint entry §3.2 (Issue #1712 out of scope).

---

## Section 3 — Business PO Acceptance Table

G8 is a **bug-fix sprint** restoring correct primary_indicator semantics in the Mode 3 harness.
The fix is user-facing: without it, all hd_composite divergence measurements returned
INDISTINGUISHABLE regardless of calibrated elasticity values, making Demo 8 Act 2 impossible.

| Deliverable | Work type | Customer Agent Layer 3 | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| `_classify_direction` primary_indicator fix (#1739) | Backend — bug fix | N/A — restores existing spec; no new capability surface | **ACCEPT** | In-session 2026-07-04 |
| GRC AC-1 verified (#1711) | Backend — verification | N/A — verification of existing fixture | **ACCEPT** | Run 28719741291, 3/3 PASSED |
| CM_A/B/C baseline pre-advance (#1745, #1746) | Backend — test fix | N/A — test infrastructure; no Persona 2/3/5 direct exposure | **ACCEPT** | In-session 2026-07-04 |

**Business PO acceptance status:** All ACCEPT.

**North star test:** Filed in sprint entry `m19-g8-sprint-entry.md §BPO Assessment`:

> The Zambia/GRC analyst at a restructuring session asks: "Does a smaller IMF programme
> (0.30 vs 0.48 GDP ratio) produce meaningfully better human development outcomes?"
> After the fix, the harness correctly measures hd_composite divergence (confirmed
> 2026-07-04: per_step_diff[3] within [0.010, 0.20], direction_verdict=COUNTER_FACTUAL_BETTER).
> The analyst can point to a specific measured gap. Without the fix, the harness reports
> zero divergence — the core demonstration is impossible.

**North star test classification:** Tier 2 — bug fix restoring instrument-level measurement
capability. The harness now functions as specified; the Demo 8 Act 2 GRC argument is instrument-visible.

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on sprint branch (Section 2) — PRs #1744, #1745, #1746 all merged; all required checks green
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable (Section 3) — all three deliverables ACCEPT; in-session 2026-07-04
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables — N/A; bug fix restoring existing spec; no new capability surface exposed to end users
- [x] No open rejection artifacts (Section 4)
- [x] Near-miss entry filed for each rejection in this sprint — no rejections; NM-098 filed at sprint entry (root cause of G8 scope)
- [x] North star test artifact on record — filed in sprint entry §BPO Assessment; confirmed by run 28719741291 (3/3 PASSED)
- [x] Issues #1739 and #1711 closed (see below)

**PI Agent sprint exit verdict: Confirmed — all exit conditions satisfied.**

> G8 exit confirmed. Three feature PRs merged to sprint/m19-g8 with all required CI checks
> green. GRC AC-1 verified by workflow dispatch run 28719741291 (2026-07-04):
> `TestAC1MagnitudeDivergence` 3/3 PASSED — per_step_diff[3] within [0.010, 0.20],
> direction_verdict=COUNTER_FACTUAL_BETTER. BPO ACCEPT on record for all three deliverables
> (in-session 2026-07-04). No open rejections. North star test confirmed by live run.
>
> Root cause chain fully resolved: (1) `_classify_direction` now respects primary_indicator
> for composite fields (NM-098 fix, #1744); (2) CM_A/B/C tests now pre-advance the baseline
> before TYPE_B run_harness (#1745, #1746); (3) ARG baseline n_steps mismatch surfaced at
> correct magnitude assertion, not setup crash — CM-D scope confirmed.
>
> ARG AC-1 (#1712) remains RED pending CM-D Kirchner recovery inputs. This is out-of-scope
> for G8 and documented in sprint entry §3.2. Sprint journal #1741 closes at integration
> PR merge.
>
> — PI Agent, 2026-07-04

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G8 of M19. It is filed at
`docs/process/sprint-plans/m19-g8-sprint-exit.md`. Sprint closes when the integration
PR (`sprint/m19-g8` → `release/m19`) merges and CI is green on `release/m19`.
