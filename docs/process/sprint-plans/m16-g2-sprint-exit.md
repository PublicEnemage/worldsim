---
name: m16-g2-sprint-exit
type: sprint-exit
milestone: M16 — Distributional Visibility
sprint-group: G2
status: Confirmed
authored-by: PI Agent
date: 2026-06-24
pi-confirmed: true
release-branch: release/m16
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M16, G2: Distributional Visibility on Primary Surface

**Status:** Confirmed — all exit conditions satisfied
**Date produced:** 2026-06-24
**Release branch:** `release/m16`
**Sprint entry document:** `docs/process/sprint-plans/m16-g2-sprint-entry.md` — EL Approved 2026-06-23
**Intent document:** `docs/process/intents/M16-G2-2026-06-23-distributional-surface.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
G2 is a user-facing frontend sprint serving Persona 2 (finance ministry negotiator) and
Persona 3 (political advisor). All four exit gate conditions apply: Business PO acceptance,
Customer Agent Layer 3 assessment, no open rejections, and PI Agent confirmation.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M16 — Distributional Visibility |
| Sprint group | G2 — Distributional Visibility on Primary Surface |
| Release branch | `release/m16` |
| Sprint entry document | `docs/process/sprint-plans/m16-g2-sprint-entry.md` |
| Intent document | `docs/process/intents/M16-G2-2026-06-23-distributional-surface.md` |
| Exit checklist issue | #985 |
| Date implementation completed | 2026-06-24 (PR #1173 merged to `release/m16`) |
| CI status on release branch | **Green** — 209/209 E2E tests passing, including all 14 G2 ACs |

---

## Section 2 — Implementation Status

| Issue | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| #986 — Cohort disaggregation on primary surface (Zone 1B) | #1173 | ✅ Yes — 2026-06-24 | Green (209/209) | Frontend Architect Agent |
| #987 — Political risk summary surface (Zone 1D) | #1173 | ✅ Yes — 2026-06-24 | Green (209/209) | Same PR as #986; co-gated per FA brief DD-016 |
| #1163 — PSP threshold anchor / absolute PSP legibility | #1173 | ✅ Closed — 2026-06-24 | N/A (no separate implementation) | Resolved by #987 severity-labeled display; closed as consequence of #987 merge per entry §3.1 |

**Implementation status:** All three issues resolved via single PR (#1173) per entry document
§4 sequencing (co-gated implementation). CI green on `release/m16` post-merge confirmed:
209/209 Playwright E2E tests, including all 14 G2 ACs (AC-1 through AC-14). Pre-push build gate
(`cd frontend && npm run build` — exits 0) confirmed before push.

**QA test authorship:** PR #1170 (merged to `release/m16` prior to #1173) filed both
`frontend/tests/e2e/m16-g2-distributional-surface.spec.ts` (AC-1–AC-14) and updated
`frontend/tests/e2e/m16-g1-zone-1a-phase4-composite.spec.ts` for the 4 retired G1 testids
(`zone-1d-political-feasibility`, `psp-delta`, `psp-layer3-sentence`, `psp-delta-sentence`).
QA-before-implementation gate satisfied.

**Pre-push gate compliance:** `cd frontend && npm run build` — exits 0, 0 TypeScript errors.
Confirmed at Step 4 Verify (Frontend Architect, 2026-06-24).

**AC-4 root cause and fix (NM-056 pattern):** CI run 1 failed on AC-4 (empty-state text
mismatch). Root cause: `CohortImpactSection` used `mode === "MODE_1"` from the Zustand store
to select label tense. In-progress scenarios without a non-default fiscal multiplier have
`mode = "MODE_1"` in the store, causing "HISTORICAL" text on in-progress scenarios. Fix:
replaced store-mode logic with `isCompleted?: boolean` prop driven by
`activeScenarioDetail.status === "completed"`. The prop correctly signals scenario completion
status independent of fiscal multiplier mode. CI run 2: 209/209 passing.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| #986 — Cohort disaggregation on primary surface (Zone 1B) | Frontend | Filed 2026-06-24 — PASS (no blocking conditions) | **ACCEPT** 2026-06-24 | `docs/process/intents/M16-G2-2026-06-23-distributional-surface.md §9` |
| #987 — Political risk summary surface (Zone 1D) | Frontend | Filed 2026-06-24 — PASS (no blocking conditions) | **ACCEPT** 2026-06-24 | `docs/process/intents/M16-G2-2026-06-23-distributional-surface.md §9` |
| #1163 — PSP threshold legibility | Closed by #987 | N/A (resolved by #987 implementation) | **ACCEPT** 2026-06-24 | (same §9 — criterion (c) confirmed satisfied) |

**Business PO acceptance status:** All ACCEPT — all three deliverables accepted in intent
document §9 per their co-gated delivery structure.

### Customer Agent Layer 3 assessments

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| #986 — Cohort disaggregation (Zone 1B) | Yes — Persona 2 (finance ministry negotiator) | ✅ Yes — filed 2026-06-24 before BPO verdict |
| #987 — Political risk summary (Zone 1D) | Yes — Persona 3 (political advisor) | ✅ Yes — filed 2026-06-24 before BPO verdict |
| #1163 — PSP threshold legibility | Yes — Persona 3 (political advisor) | ✅ Yes — assessed within #987 Layer 3 assessment |

**Layer 3 verdict (Customer Agent, 2026-06-24): PASS — both Persona 2 and Persona 3**

Named conditions and disposition:

| # | Condition | Persona | Disposition |
|---|---|---|---|
| None | No blocking conditions | — | No open conditions at exit |

All Layer 3 conditions were classified as non-blocking by the Customer Agent (no conditions
issued). Both Persona 2 (cohort argument) and Persona 3 (political risk read) pass at L0 with
zero interaction beyond scenario load.

### North star test artifact

*Required for user-facing deliverables per CLAUDE.md §North Star Test (Process Gate).*

**North star test:** Filed in intent document §9 (Business PO narrative, 2026-06-24).

*"The Senegalese finance ministry analyst with ZMB ECF loaded in Mode 2 at step 3 can now tell
the delegating Minister: 'The bottom income quintile has crossed the poverty headcount threshold
at step 2 — that is a CRITICAL cohort impact finding. Programme survival is also CRITICAL at 38%
and falling — comparable ECF programmes at this level have shown abandonment within 3 steps.'
Both facts are readable from the primary viewport in under 15 seconds, without opening any drawer
or consulting any specialist. The Zone 1D political risk section and the Zone 1B cohort impact
section together constitute the distributional visibility argument that Demo 6 will anchor."*

PI Agent confirms this is specific — names scenario (ZMB ECF Mode 2), step number, two distinct
arguments (cohort crossing + PSP level), time ceiling (15 seconds), and the Demo 6 forward
connection. North star test artifact: **SATISFIES** the gate condition.

---

## Section 4 — Open Rejections

No open rejections. No REJECT verdicts were issued for any G2 deliverable.

**Near-miss entries required for each rejection:** N/A — no rejections.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] **All implementation groups merged; CI green on release branch (Section 2)**
  PR #1173 merged 2026-06-24 to `release/m16`. CI green post-merge confirmed: 209/209
  Playwright E2E tests passing including all 14 G2 ACs. Pre-push build gate satisfied at Step 4
  Verify (0 TypeScript errors). QA test authorship pre-dated implementation (PR #1170 merged
  before #1173).

- [x] **Business PO ACCEPT verdict filed for each user-facing deliverable, or EL exception on record (Section 3)**
  #986 and #987 both ACCEPT — verdict filed in intent document §9, 2026-06-24. #1163 accepted
  as a consequence of #987 per entry document §3.1. Verdict artifact exists in the repository.

- [x] **Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed before Business PO verdict (Section 3)**
  Layer 3 assessment filed 2026-06-24 before BPO verdict was rendered. PASS for both Persona 2
  (#986 cohort argument) and Persona 3 (#987 political risk read + #1163 PSP legibility). No
  blocking conditions issued.

- [x] **No open rejection artifacts (Section 4)**
  No rejections in G2. Zero REJECT verdicts on record.

- [x] **Near-miss entry filed for each rejection in this sprint (Section 4)**
  N/A — no rejections in G2. No near-miss entries required on this basis.

- [x] **North star test artifact on record for user-facing deliverables**
  Filed in intent document §9. Specific — names ZMB ECF Mode 2 scenario, step 3, two distinct
  arguments (bottom quintile cohort crossing + PSP CRITICAL at 38%), 15-second time ceiling,
  Demo 6 forward connection. PI Agent confirms: specific, not aspirational. Gate satisfied.

**PI Agent sprint exit verdict: CONFIRMED — all exit conditions satisfied**

**PI Agent confirmation:**

> G2 sprint exit conditions are satisfied as of 2026-06-24. All three deliverables (#986, #987,
> #1163) are resolved via PR #1173 merged to `release/m16`. CI is green (209/209 E2E tests, all
> 14 G2 ACs passing). Business PO ACCEPT verdicts are on record in intent document §9. Customer
> Agent Layer 3 PASS is on record for both Persona 2 and Persona 3 — no blocking conditions.
> No rejection artifacts exist. The north star test artifact in §9 is specific and satisfies the
> gate. G2 is closed.
>
> G3 gate effect: G3 (25-year human capital trajectory, #988) is a parallel sprint that does not
> depend on G2 BPO acceptance. However, G8 (live stakeholder demo #843 — M16 exit gate) may not
> open until G1, G2, and G3 are all BPO-accepted. G2 BPO acceptance clears G2's portion of the
> G8 gate. G3 BPO acceptance remains outstanding.
>
> AC-4 root cause note: The `mode === "MODE_1"` → `isCompleted` prop refactor is recorded in
> Section 2 above. This is not near-miss worthy (caught by CI before merge, not a shipped
> regression) but is documented for institutional memory — the Zustand store mode field is
> fiscal-multiplier-driven, not completion-status-driven, and these must not be conflated.
>
> — PI Agent, 2026-06-24

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for M16-G2. It supersedes any informal exit notation
in `SESSION_STATE.md` for this sprint. It is filed at
`docs/process/sprint-plans/m16-g2-sprint-exit.md`.

The PI Agent confirmation in Section 5 is the gate. G2 is closed as of 2026-06-24.
