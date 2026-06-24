---
name: m16-g3-sprint-exit
type: sprint-exit
milestone: M16 — Distributional Visibility
sprint-group: G3
status: Confirmed
authored-by: PI Agent
date: 2026-06-24
pi-confirmed: true
release-branch: release/m16
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M16, G3: 25-Year Human Capital Depletion Trajectory

**Status:** Confirmed — all exit conditions satisfied
**Date produced:** 2026-06-24
**Release branch:** `release/m16`
**Sprint entry document:** `docs/process/sprint-plans/m16-g3-sprint-entry.md` — EL Approved 2026-06-23
**Intent document:** `docs/process/intents/M16-G3-2026-06-23-25year-human-capital-trajectory.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
G3 is a backend + frontend sprint serving Persona 2 (finance ministry negotiator) and Persona 5
(Finance Minister). All five exit gate conditions apply: implementation merged, Business PO
acceptance, Customer Agent Layer 3 assessment, no open rejections, and PI Agent confirmation.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M16 — Distributional Visibility |
| Sprint group | G3 — 25-Year Human Capital Depletion Trajectory |
| Release branch | `release/m16` |
| Sprint entry document | `docs/process/sprint-plans/m16-g3-sprint-entry.md` |
| Intent document | `docs/process/intents/M16-G3-2026-06-23-25year-human-capital-trajectory.md` |
| Exit checklist issue | #985 |
| Date implementation completed | 2026-06-24 (PR #1172 merged to `release/m16`) |
| CI status on release branch | **Green** — all required checks pass (test-backend PASS, playwright-e2e PASS, lint PASS, compliance-scan PASS, branch-naming PASS, backtesting SKIP) |

---

## Section 2 — Implementation Status

| Issue | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| #274 — 25-year human capital depletion trajectory (backend + frontend) | #1172 | ✅ Yes — 2026-06-24 | Green — all required checks PASS | Chief Engineer Agent (backend); Frontend Architect Agent (frontend) |
| Process artifacts — intent doc §8/§9, SESSION_STATE.md | #1175 | ✅ Yes — 2026-06-24 | Green — doc-only, no code checks triggered | BPO ACCEPT record + Customer Agent Layer 3 assessment |

**Implementation status:** PR #1172 merged 2026-06-24. CI green on `release/m16` post-merge
confirmed: all 19 ACs passing (AC-1 through AC-8 in test-backend; AC-F1 through AC-F8 and
AC-CM-1 through AC-CM-3 in playwright-e2e). Pre-push gate (`cd backend && ruff check . &&
mypy app/` and `cd frontend && npm run build`) confirmed before push.

**QA test authorship:** `backend/tests/test_m16_g3_25year_human_capital_trajectory.py` and
`frontend/tests/e2e/m16-g3-25year-human-capital-trajectory.spec.ts` both authored and merged
in PR #1169 before implementation PR #1172 opened. QA-before-implementation gate satisfied.
No soft-skip patterns present (NM-056 guard — confirmed at test authorship review).

**CE Assessment Decision 4 dry-run:** AC-6 (indicator bounds) and AC-F8 (performance ceiling)
both confirmed by CI. `poverty_headcount_ratio` clamped to [0.0, 1.0] by `_ATTRIBUTE_UNIT_INTERVAL`
frozenset in `backend/app/simulation/engine/propagation.py:70–72`. CE Assessment Decision 4
bounds requirement satisfied structurally and confirmed by test-backend PASS.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| #274 — 25-year human capital depletion trajectory | Backend + Frontend | Filed 2026-06-24 — CONDITIONAL PASS (CA-1/CA-2/CA-3 noted, none blocking) | **ACCEPT** 2026-06-24 | `docs/process/intents/M16-G3-2026-06-23-25year-human-capital-trajectory.md §9` |

**Business PO acceptance status:** ACCEPT — #274 accepted in intent document §9.

### Customer Agent Layer 3 assessments

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| #274 — 25-year human capital trajectory | Yes — Persona 2 (finance ministry negotiator) and Persona 5 (Finance Minister) | ✅ Yes — filed 2026-06-24 in intent doc §9 before BPO verdict was rendered |

**Layer 3 verdict (Customer Agent, 2026-06-24): CONDITIONAL PASS**

Three conditions identified, none blocking G3 sprint exit:

| # | Condition | Persona affected | GitHub issue | Disposition |
|---|---|---|---|---|
| CA-1 | `[step N]` reference in milestone sentence is technical noise for Persona 5; year anchor sufficient | Persona 5 | #1177 | Pre-demo polish — required before Demo 6 (#843) |
| CA-2 | `T3` badge text not self-interpreting at L0; hover tooltip provides context but not visible without interaction | Persona 5 | #1178 | Pre-demo polish — required before Demo 6 (#843) |
| CA-3 | Q2 curve silence unexplained on-screen; no MDA-HD-POVERTY-Q2 floor is registered (correct) but asymmetry not labeled | Persona 5 | #1179 | Pre-demo polish — required before Demo 6 (#843) |

The primary L0 output (milestone sentence) is Layer 3 compliant for Persona 2 in Preparatory
state. All three CA conditions concern Persona 5 first-encounter legibility — none prevent the
Demo 6 argument from being completeable by the ministry analyst team. They must be resolved
before Demo 6 (#843) runs with real external participants.

### North star test artifact

*Required for user-facing deliverables per CLAUDE.md §North Star Test (Process Gate).*

**North star test:** Filed in intent document §9 (Business PO narrative, 2026-06-24).

*"Senegalese finance ministry analyst, 15 minutes before Article IV consultation. IMF
conditionality document proposes a 36-month austerity programme. The analyst loads the SEN
scenario with `projection_steps=100` in Mode 1. The milestone sentence reads: 'by 2030 [step
20], bottom quintile informal workers poverty headcount crosses the recovery floor — at this
level, capability restoration takes a decade or more.' The minister's team can now argue: 'The
proposed programme conditions drive the bottom quintile into a capability-loss zone that persists
ten-plus years beyond the programme window.' Before G3, the simulation showed only
programme-length consequences (8 steps ≈ 2 years). G3 extends visibility to 100 quarterly
steps (25 years), making the intergenerational consequence citeable at the table."*

PI Agent confirms this is specific — names the scenario (SEN, `projection_steps=100`, Mode 1),
the consultation context (Article IV, 36-month conditionality), the exact argument now available
("ten-plus years beyond the programme window"), and what changed versus pre-G3. North star test
artifact: **SATISFIES** the gate condition.

---

## Section 4 — Open Rejections

No open rejections. No REJECT verdicts were issued for any G3 deliverable.

**Near-miss entries required for each rejection:** N/A — no rejections.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] **All implementation groups merged; CI green on release branch (Section 2)**
  PR #1172 merged 2026-06-24 to `release/m16`. CI green confirmed: test-backend PASS,
  playwright-e2e PASS, lint PASS, compliance-scan PASS, branch-naming PASS, backtesting SKIP
  (no fixture changes). All 19 ACs confirmed passing. Pre-push gates satisfied at implementation.
  QA test authorship pre-dated implementation per Sprint Entry §2.4. Process artifact PR #1175
  also merged 2026-06-24.

- [x] **Business PO ACCEPT verdict filed for each user-facing deliverable, or EL exception on record (Section 3)**
  #274 ACCEPT — verdict filed in intent document §9, 2026-06-24. BPO ACCEPT comment also posted
  on GitHub issue #274 (comment 4784986059). Verdict artifact exists in the repository.

- [x] **Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed before Business PO verdict (Section 3)**
  Layer 3 assessment filed 2026-06-24 before BPO verdict was rendered. CONDITIONAL PASS —
  three pre-demo conditions (CA-1/CA-2/CA-3) filed as GitHub issues #1177, #1178, #1179.
  None are blocking for sprint exit. All three must be resolved before Demo 6 (#843). The
  milestone sentence is Layer 3 compliant for Persona 2; Persona 5 legibility improvements
  are tracked.

- [x] **No open rejection artifacts (Section 4)**
  No rejections in G3. Zero REJECT verdicts on record.

- [x] **Near-miss entry filed for each rejection in this sprint (Section 4)**
  N/A — no rejections in G3. No near-miss entries required on this basis.

- [x] **North star test artifact on record for user-facing deliverables**
  Filed in intent document §9. Specific — names SEN scenario with `projection_steps=100`,
  Article IV context, the exact argument now available ("ten-plus years beyond the programme
  window"), and what changed versus pre-G3 (8-step limitation removed, 25-year horizon enabled).
  PI Agent confirms: specific, not aspirational. Gate satisfied.

**PI Agent sprint exit verdict: CONFIRMED — all exit conditions satisfied**

**PI Agent confirmation:**

> G3 sprint exit conditions are satisfied as of 2026-06-24. Issue #274 (25-year human capital
> depletion trajectory) is resolved via PR #1172 merged to `release/m16`. CI is green — all 19
> ACs confirmed passing (test-backend + playwright-e2e both PASS). Business PO ACCEPT verdict
> is on record in intent document §9 (2026-06-24) and as an issue comment on #274. Customer
> Agent Layer 3 CONDITIONAL PASS is on record — three pre-demo polish conditions (CA-1/CA-2/CA-3)
> filed as #1177, #1178, #1179 for tracking. None are blocking for G3 exit; all must be resolved
> before Demo 6 (#843) per the BPO verdict. No rejection artifacts exist. The north star test
> artifact in §9 is specific and satisfies the gate.
>
> CE Assessment (sprint entry §2.5) fully satisfied: Decision 1 (adaptive resolution override —
> implemented via `advance_months=3` for quarterly cadence, effectively disabling daily-resolution
> switching; `adaptive_resolution` variable explicitly present in source for AC-5 source inspection);
> Decision 2 (`projection_steps` on existing endpoint — implemented); Decision 3 (CM review on #274
> — filed and finalized 2026-06-23); Decision 4 (dry-run bounds check — confirmed by CI via AC-6
> bounds test and `_ATTRIBUTE_UNIT_INTERVAL` clamping in propagation engine).
>
> G3 is closed.
>
> G8 gate effect: both G2 (BPO ACCEPT 2026-06-24) and G3 (BPO ACCEPT 2026-06-24) are now
> accepted. G1 was accepted 2026-06-23. The G8 gate (#843 — live stakeholder demo, M16 exit gate)
> requires G1, G2, and G3 all BPO-accepted. That condition is now satisfied. G8 may proceed when
> the EL authorizes demo preparation. Pre-demo items #1177, #1178, #1179 (from G3 CA assessment)
> and #1162 (from G1 CA assessment) must all be resolved before the live session runs.
>
> — PI Agent, 2026-06-24

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for M16-G3. It supersedes any informal exit notation
in `SESSION_STATE.md` for this sprint. It is filed at
`docs/process/sprint-plans/m16-g3-sprint-exit.md`.

The PI Agent confirmation in Section 5 is the gate. G3 is closed as of 2026-06-24.
