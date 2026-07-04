---
name: m19-g6-sprint-exit
type: sprint-exit
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G6 — Demo 8 Clearance
status: Confirmed
authored-by: PI Agent
date: 2026-07-04
pi-confirmed: true
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M19, G6: Demo 8 Clearance

**Status:** Confirmed — all exit conditions satisfied (BPO ACCEPT 2026-07-04)
**Date produced:** 2026-07-04
**Release branch:** `release/m19`
**Sprint entry document:** `docs/process/sprint-plans/m19-g6-sprint-entry.md` — EL-approved 2026-07-04 (PR #1717)
**Sprint journal issue:** #1716
**Exit checklist issue:** #1535

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase C complete, updated 2026-07-03).
G6 delivers Demo 8 clearance: FOUND state tolerance band display (#1709), AC-12 structural absence
timing fix (#1710), DemographicModule dead subscription fix + emergency policy elasticities (#1657),
scenarioId crash guard in MDAAlertPanelZone1B (#1456), and focal cohort floor Pydantic validation
(#1538). All 5 issues closed; all implementation PRs merged to sprint/m19-g6.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| Sprint group | G6 — Demo 8 Clearance |
| Release branch | `release/m19` |
| Sprint sub-branch | `sprint/m19-g6` |
| Sprint entry document | `docs/process/sprint-plans/m19-g6-sprint-entry.md` |
| Exit checklist issue | #1535 |
| Sprint journal issue | #1716 |
| Date implementation completed | 2026-07-04 |
| CI status on sprint branch | Green — all required sprint-branch-ci-gate checks passing on all PRs (#1718–#1722). playwright-e2e not required on sprint sub-branches (sprint-branch-ci-gate Ruleset). |

---

## Section 2 — Implementation Status

*All implementation PRs merged to sprint/m19-g6. Required checks: `audit`, `changes`,
`branch-naming`, `session-state-size-check`, `test-backend`, `lint`, `compliance-scan`.*

| Issue | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| QA tests — #1709 tolerance band | #1718 | Yes | Green | AC-T1..AC-T4 added to m19-g1-constraint-floor-search.spec.ts; AC-12 timing bugs fixed; AC-5 updated for split |
| #1709 — FOUND state tolerance band display | #1720 | Yes | Green | `constraint-tolerance-band` div extracted from FOUND state; `uncertainty_hi - uncertainty_lo` precision; AC-T1..AC-T4 GREEN |
| #1710 — AC-12 structural absence fix | #1721 | Yes | Green | Skip guard removed; `btn.waitFor({state:"visible"})` + `expect(sad).toBeVisible({timeout:5000})`; `__structural_absence__` confirmed as correct sentinel |
| #1657 — DM subscriptions + elasticities | #1722 | Yes | Green | `_SUBSCRIBED_EVENTS` corrected; 4 elasticity rows added (Q1/Q2 INFORMAL, T3); ADR-020 Decision 3 audit completion recorded; transmission table updated |
| #1456 — MDAAlertPanelZone1B crash guard | Prior to G6 (commit b8cb37b, 2026-07-02) | Yes | Green | Already implemented; issue closed retroactively |
| #1538 — Focal cohort floor validation | Prior to G6 (commit cd28853, 2026-07-02) | Yes | Green | Already implemented; issue closed retroactively |

**Implementation status:** All 5 issues closed; all implementation merged; CI green on all required checks.

---

## Section 3 — Business PO Acceptance Table

*User-facing deliverables: #1709. #1710 (test correction), #1657 (engine fix), #1456 (crash guard),
#1538 (schema enforcement) are implementation/infrastructure — no BPO acceptance required.*

| Deliverable | Work type | Customer Agent L3 | BPO verdict | Verdict artifact |
|---|---|---|---|---|
| #1709 — FOUND state tolerance band display | Frontend (UX output) | N/A — tolerance band displays precision from existing FOUND response; no new Persona 2/3/5 raw data capability | **ACCEPT** | See BPO verdict below |

**Business PO acceptance — #1709:**

> The tolerance band element (`±N.NN precision`) completes the FOUND state information contract.
> A ministry analyst can now read both the boundary value AND its precision interval in a single
> glance without mental arithmetic on uncertainty_hi/lo. This is the correct surface for this
> information per `information-hierarchy.md §1B` (actionable uncertainty on primary outputs).
> ACCEPT.
> — Business PO (2026-07-04)

**Business PO acceptance status: ACCEPT — gate cleared 2026-07-04.**

---

## Section 4 — Open Rejections

No open rejections. No REJECT artifacts filed during G6.

---

## Section 5 — North Star Test

**Deliverable requiring north star test:** #1709 (user-facing FOUND state update)

**Finance minister scenario:** A Zambian finance ministry analyst is using WorldSim Mode 3
constraint-floor search in preparation for an IMF restructuring session. The search returns
FOUND with boundary 1.18. Previously, the FOUND state showed `1.18 (±0.02)` embedded in the
boundary value — the analyst could not distinguish "1.18 is the boundary" from "1.18 ± 0.02
is the boundary range."

**Capability evaluated:** After #1709, the FOUND state shows `fiscal multiplier ≥ 1.18`
(boundary) and `±0.02 precision` as a separate element. The analyst immediately understands:
the threshold is 1.18, with ±0.02 uncertainty. She can communicate this to the IMF team as:
"our constraint-floor analysis shows a fiscal multiplier of 1.18 is required, with ±0.02
calibration uncertainty."

**Does this change what the minister's team can argue at the table?** Yes — separating the
boundary from its uncertainty band is not cosmetic. An analyst who cannot distinguish precision
interval from threshold value may misquote the boundary to the IMF team or underestimate the
margin for negotiation. The ±0.02 band is actionable: it tells the team that a multiplier of
1.16 is within the uncertainty bound, which may open a negotiating path.

**North star test verdict: PASS** — the capability changes what the analyst can precisely
communicate at the restructuring table.

---

## Section 6 — Near-Miss and Process Notes

| NM | Description | Severity | Filed? |
|---|---|---|---|
| NM-095 | #1657 QA tests authored in impl PR; RED state observed only in session context, not by CI | Low | Yes — near-miss-registry.md appended 2026-07-04 |

NM-095 does not block sprint exit per PI Agent judgment: tests are correctly authored with
RED-before semantics, CM cert is on record, and 9/9 tests pass GREEN.

---

## Section 7 — PI Agent Confirmation

**PI Agent gate review:**

| Exit condition | Status |
|---|---|
| Business PO acceptance on file for all user-facing deliverables | ✅ ACCEPT on #1709 |
| Customer Agent L3 assessment (Persona 2/3/5) | ✅ N/A — #1709 does not introduce new capability for Personas 2/3/5; tolerance band displays existing FOUND response field |
| No open rejection artifacts | ✅ None |
| All implementation PRs merged to sprint/m19-g6 | ✅ PRs #1718–#1722 merged; #1456/#1538 pre-G6 commits confirmed |
| Test file presence on sprint branch | ✅ `test_m19_g6_demographic_subscriptions.py` present in sprint/m19-g6 (merged via #1722) |
| North star test on file for user-facing deliverable | ✅ #1709 above — PASS verdict |
| NM-095 review | ✅ Low severity; does not block exit; codification improvement recorded |
| Integration PR ready | ✅ sprint/m19-g6 → release/m19 may open |

**PI Agent confirmation: All G6 exit conditions satisfied. Integration PR authorized.**

Sprint journal issue #1716 may be closed.

— PI Agent (2026-07-04)
