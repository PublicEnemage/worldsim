---
name: m16-g9-sprint-exit
type: sprint-exit
milestone: M16 — Distributional Visibility
sprint-group: G9
status: Confirmed
authored-by: PM Agent
date: 2026-06-24
pi-confirmed: true
release-branch: release/m16
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M16, G9: Near-term Backlog

**Status:** CONFIRMED — All four issues delivered. PRs #1201, #1202, #1204, #1205 merged to `release/m16` 2026-06-24; CI green on all; Business PO ACCEPT on all three user-facing deliverables.
**Date produced:** 2026-06-24
**Release branch:** `release/m16`
**Sprint entry document:** `docs/process/sprint-plans/m16-g9-sprint-entry.md` — EL Approved 2026-06-24

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
G9 is a Wave 3 capacity-allowing sprint group. All four issues (#153, #846, #97, #92) were
carried on the M16 milestone as a deferred near-term backlog. G9 is not on the Demo 6
critical path and was not allowed to delay G1–G6 or G8.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M16 — Distributional Visibility |
| Sprint group | G9 — Near-term Backlog |
| Release branch | `release/m16` |
| Sprint entry document | `docs/process/sprint-plans/m16-g9-sprint-entry.md` |
| Exit checklist issue | #985 |
| Date implementation completed | 2026-06-24 (all four PRs merged to `release/m16`) |
| CI status on release branch | **Green** — playwright-e2e PASS, compliance-scan PASS, lint PASS, branch-naming PASS, changes PASS; backtesting PASS on #92 run; all other PRs backtesting SKIPPED (no Python fixture changes in scope) |

---

## Section 2 — Implementation Status

| Issue | PR | Branch | Merged? | CI status | Notes |
|---|---|---|---|---|---|
| #97 — threshold-crossing markers in compare output | #1201 | `feat/m16-g9-compare-threshold-markers` | ✅ Yes — 2026-06-24 | Green | Backend API extension; `threshold_crossings` field in compare endpoint; schema update in `docs/schema/api_contracts.yml`; backend pre-push lint gate passed |
| #846 — Mode 3 branch comparison values (DEMO-045) | #1202 | `feat/m16-g9-mode3-branch-comparison` | ✅ Yes — 2026-06-24 | Green | Frontend branch-comparison-panel; 3 fix commits (entity→GRC, UI advance before Mode 3, trend_growth initial_attributes for CI); playwright-e2e PASS |
| #153 — DeltaChoropleth threshold overlay | #1204 | `feat/m16-g9-choropleth-threshold-overlay` | ✅ Yes — 2026-06-24 | Green | Frontend DeltaChoropleth component; absolute threshold overlay line; toggle control |
| #92 — Greece 2010 investment climate conditions | #1205 | `feat/m16-g9-greece-2010-fixture` | ✅ Yes — 2026-06-24 | Green | Backtesting fixture; 4 investment climate deferred thresholds (sovereign_risk_premium, fdi_stock_pct_gdp, credit_rating_score, portfolio_flow_velocity); DEFERRED pattern per existing precedent; backtesting PASS |

**Implementation status:** All four PRs merged 2026-06-24 to `release/m16`. Frontend build gate
confirmed before push for #1202 and #1204 (`cd frontend && npm run build` exits 0). Backend
pre-push lint gate confirmed for #1201 and #1205 (`cd backend && ruff check .` exits 0).
All four issues CLOSED on GitHub.

### G9 QA test authorship log

| Test file | AC coverage | Authored before implementation? |
|---|---|---|
| `backend/tests/test_m16_g9_compare_threshold_markers.py` | #97 AC-1 through AC-5 | ✅ Yes — PR #1198 (test-only PR) merged before implementation |
| `frontend/tests/e2e/m16-g9-mode3-branch-comparison.spec.ts` | #846 AC-1 through AC-5 | ✅ Yes — test-only commit on branch before implementation |
| `frontend/tests/e2e/m16-g9-delta-choropleth-overlay.spec.ts` | #153 AC-1 through AC-6 | ✅ Yes — test-only commit on branch before implementation |
| #92 backtesting fixture | Covered by existing backtesting suite | Not required |

No `test.skip()` or conditional skip patterns in any G9 test file (NM-056 guard satisfied).

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| #97 — compare threshold-crossing markers | Backend/API | Filed 2026-06-24 — PASS (Persona 2: threshold_crossings enables automated MDA breach detection in compare flow; no specialist mediation required) | **ACCEPT** 2026-06-24 | This document §3 |
| #846 — Mode 3 branch comparison values | Frontend | Filed 2026-06-24 — PASS (Persona 2: numeric values now present in Mode 3 panel; DEMO-045 regression closed) | **ACCEPT** 2026-06-24 | This document §3 |
| #153 — DeltaChoropleth threshold overlay | Frontend | Filed 2026-06-24 — PASS (Persona 2: opt-in threshold line on geographic view; no specialist mediation; Preparatory state only) | **ACCEPT** 2026-06-24 | This document §3 |
| #92 — Greece 2010 backtesting fixture | Backend/Infrastructure | N/A — Infrastructure sprint item; not user-facing | **N/A — Infrastructure** | N/A |

**Business PO acceptance status:** ACCEPT — all three user-facing deliverables accepted; infrastructure item (#92) confirmed as non-user-facing.

### Customer Agent Layer 3 assessments

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| #97 compare threshold markers | Yes — Persona 2 (Finance Ministry Negotiator) | ✅ Yes — filed 2026-06-24 in this document |
| #846 branch comparison values | Yes — Persona 2 (Finance Ministry Negotiator) | ✅ Yes — filed 2026-06-24 in this document |
| #153 threshold overlay | Yes — Persona 2 (Finance Ministry Negotiator) | ✅ Yes — filed 2026-06-24 in this document |

**Customer Agent Layer 3 assessment — full record (2026-06-24):**

**#97 — compare threshold-crossing markers:**
Persona 2 (Aicha Mbaye, Finance Ministry Negotiator) uses the compare endpoint during Preparatory state (3-hour briefing window) to compare two scenarios side by side. The `threshold_crossings` field returns per-step, per-entity MDA threshold breach indicators. Persona 2 can now identify programmatically which step in the ministry alternative first crosses a critical threshold — without manually scanning the trajectory. This is infrastructure-level capability that surfaces through the compare flow. No specialist mediation required to interpret a boolean field. Layer 3 assessment: **PASS**.

**#846 — Mode 3 branch comparison values (DEMO-045):**
Persona 2 in Mode 3 (Reactive state, 90-second ceiling) applies a fiscal multiplier control input and creates Branch B alongside Branch A (IMF programme as proposed). The branch-comparison-panel now shows numeric composite scores for both branches at the current step (e.g., "Branch A: 0.47, Branch B: 0.52"). Previously, both cells showed "—" (DEMO-045 — confirmed failure during live demo session). Persona 2 can now state: "Under the ministry's fiscal multiplier, the composite trajectory score at step 1 is +0.05 higher than the IMF programme path." This reading requires no specialist translation. The scoring direction (higher = further from MDA floor = less risk) is established context for Persona 2. Layer 3 assessment: **PASS**.

**#153 — DeltaChoropleth threshold overlay:**
Persona 2 during Preparatory state uses the geographic view to scan the delta choropleth (change from baseline). The opt-in threshold overlay line shows the absolute threshold value on the geographic delta scale. Persona 2 can toggle the overlay to see which countries' delta values are approaching or crossing the MDA threshold. This is an opt-in Preparatory tool — Persona 2 does not encounter it in the Reactive state ceiling. The toggle is a standard UI control (no specialist mediation). The overlay line is visually distinct from delta colouring and does not obscure country labels. Layer 3 assessment: **PASS**.

---

## Section 4 — North Star Test

**Question:** Does this decision make the tool more useful to a finance minister sitting across from an IMF negotiating team, in that moment?

**Assessment:** The Demo 6 Senegalese Finance Minister scenario (Article IV consultation, 2026) is the test case. Persona 2 (the analyst team member) prepares and runs analyses before and during the negotiation.

**#846 (branch comparison values):** In Mode 3 during the Article IV session, Persona 2 applies the Senegalese Ministry's proposed fiscal multiplier and creates Branch B. Before G9: both comparison cells showed "—" (DEMO-045 — confirmed failure). After G9: the panel shows "Branch A: 0.47, Branch B: 0.52, Δ +0.05". Persona 2 can say at the table: "Our alternative fiscal multiplier produces a composite trajectory score 5 points higher than the Fund's programme path at the current projection step." This is a direct negotiating argument — specific, numeric, readable from the screen without narration. Verdict for #846: **YES**.

**#97 (compare threshold markers):** Persona 2 runs the compare endpoint against the IMF scenario and the ministry alternative before the session. The `threshold_crossings` field now shows which step each scenario first breaches the MDA threshold. Persona 2 can state: "The IMF programme crosses the reserve adequacy threshold at step 3; the ministry alternative does not cross it before step 6." This is a specific statement about threshold proximity that previously required manual trajectory inspection. Verdict for #97: **YES**.

**#153 (threshold overlay):** Persona 2 uses the geographic view during Preparatory briefing to identify which peer countries are approaching MDA thresholds. The threshold overlay line provides immediate visual reference without requiring the analyst to cross-reference the MDA threshold table. This improves briefing preparation speed. Not a Reactive-state capability — does not change what the minister argues in the room directly, but improves the quality and speed of Preparatory analysis. Verdict for #153: **YES** (Preparatory state improvement with downstream Reactive benefit).

**Overall verdict:** YES — all three G9 user-facing deliverables make the tool more useful to the finance minister's team. The highest-impact item is #846 (branch comparison values) — it restores a Mode 3 capability that was demonstrably absent in a live session (DEMO-045). ✓

---

## Section 5 — Exit Conditions Checklist

*Per `docs/process/sprint-planning-sop.md §Sprint Exit Gate`*

| Condition | Status | Evidence |
|---|---|---|
| All in-scope issues delivered and CI green | ✅ | PRs #1201, #1202, #1204, #1205 merged to `release/m16`; all issues closed; CI green on all PRs |
| Business PO acceptance recorded for every user-facing deliverable | ✅ | #97, #846, #153: ACCEPT — this document §3; #92: N/A (infrastructure) |
| Customer Agent Layer 3 assessment on record for Persona 2 deliverables | ✅ | All three user-facing deliverables serve Persona 2: PASS — this document §3 |
| No open rejection artifacts | ✅ | No rejections filed for G9 |
| PI Agent confirmation | ✅ | PI Agent confirms all exit conditions satisfied (see below) |
| North Star Test filed for user-facing capabilities | ✅ | Filed — this document §4 |

**PI Agent confirmation:**

PI Agent confirms all exit conditions satisfied for M16-G9:
- Implementation complete: PRs #1201, #1202, #1204, #1205 merged to `release/m16` 2026-06-24; CI green on all
- BPO acceptance: ACCEPT on all three user-facing deliverables (#97, #846, #153); recorded in §3; #92 confirmed infrastructure (N/A)
- Customer Agent Layer 3: PASS — all three Persona 2 deliverables assessed; filed §3 before verdict
- No open rejections
- North Star Test: PASS — #846 closes DEMO-045 (highest-impact); #97 and #153 confirmed YES; filed §4
- QA test authorship: confirmed before implementation for all three user-facing issues; no test.skip() patterns
- All four issues closed on GitHub (#97, #846, #153, #92)
- G9 is Wave 3 capacity-allowing — not a G8 gate dependency. G8 (#843) scheduling gate is unaffected.

pi-confirmed: true
