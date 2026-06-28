---
name: m18-g5-sprint-exit
type: sprint-exit
milestone: M18 — Full Argument and Demo 7
sprint-group: G5 — Demo 7 Readiness
status: Confirmed
authored-by: PI Agent
date: 2026-06-28
pi-confirmed: true
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M18, G5: Demo 7 Readiness

**Status:** Confirmed — all exit conditions satisfied
**Date produced:** 2026-06-28
**Release branch:** `release/m18`
**Sprint entry document:** `docs/process/sprint-plans/m18-g5-sprint-entry.md` — EL-approved 2026-06-28 (PR #1436)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
G5 delivers the Zone 3 auditability panel on `DistributionalComparisonSummary` (#1422 — G3 CA
condition: Lucas, Persona 1, can open an expand/collapse methodology panel from Zone 1B and
defend the 340,000 headcount figure under IMF analytical scrutiny without leaving the primary
viewport). Also: #1238 (Frame A TTS narration fix) closed with no code change — all 4 ACs
already satisfied in main branch at sprint entry. NM-076 testid rename crosscheck rule landed
in `docs/CODING_STANDARDS.md`. Enhancement issue #1441 filed for two non-blocking Layer 3
forward notes (extraction path entity_id interpolation; CI factor percentage labels).*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| Sprint group | G5 — Demo 7 Readiness (Wave 3) |
| Release branch | `release/m18` |
| Sprint sub-branch | `sprint/m18-g5` |
| Sprint entry document | `docs/process/sprint-plans/m18-g5-sprint-entry.md` |
| Exit checklist issue | #1340 |
| Sprint journal issue | #1435 |
| Date implementation completed | 2026-06-28 |
| CI status on implementation PR | Green — all required checks SUCCESS (PR #1439) |

---

## Section 2 — Implementation Status

| Group | PRs | Merged? | CI status | Notes |
|---|---|---|---|---|
| G5 — intent doc (#1422) | #1437 | Yes | Green | Intent document filed before implementation |
| G5 — QA tests (#1422) | #1438 | Yes | Green | Tests authored before implementation (NM-056 + NM-076 compliant) |
| G5 — Zone 3 panel (#1422) | #1439 | Yes | Green | All 9 CI checks SUCCESS: audit, changes, branch-naming, session-state-size-check, test-backend, lint, playwright-e2e, compliance-scan, backtesting (SKIPPED — no backtesting files changed) |
| G5 — #1238 narration fix | (no PR) | N/A | N/A | No code change required — ACs already met; issue closed directly |

**Implementation status:** All merged, CI green on PR #1439.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 | BPO verdict | Verdict artifact |
|---|---|---|---|---|
| #1422 Zone 3 auditability panel | Frontend + Backend | PASS — #1435#issuecomment-4827654535 | ACCEPT | #1422#issuecomment-4827639990 + #1435#issuecomment-4827640635 |
| #1238 TTS narration fix | Documentation (no code change) | N/A — no new user-facing output | ACCEPT (no code change; ACs met) | #1435 sprint journal (narration fix closed directly) |

**Business PO acceptance status:** All ACCEPT.

### Customer Agent Layer 3 sequencing note

The intent document explicitly required Customer Agent L3 assessment for this sprint
(`customer-agent-l3-required: "Yes — Persona 1 (Lucas) at sprint exit"`). The BPO
filed a conditional ACCEPT noting "Pending: CA L3 assessment (Persona 1/2)" — treating
L3 as a precondition not yet cleared. The CA L3 assessment was then filed (PASS), clearing
the condition. PI Agent confirms this sequencing satisfies the lifecycle requirement: the
BPO verdict was conditional on L3, not final before L3 was filed.

| Deliverable | Serves Persona 2/3/5? | L3 filed before final verdict? |
|---|---|---|
| #1422 Zone 3 auditability panel | Yes (Persona 2 — Eleni, 90-second gate; Persona 5 — Aicha, kryptonite gate; explicit Persona 1 requirement per intent doc) | Yes — BPO conditional ACCEPT held open pending L3; L3 PASS cleared it |
| #1238 TTS narration fix | N/A — no new user-facing output | N/A |

---

## Section 4 — Open Rejections

No REJECT verdicts issued in G5. No rejection artifacts filed.

*Note: REJECT-001 (M14 G4, grounding strip citations, 2026-06-17) is from a prior milestone
sprint group and does not block G5 exit.*

**No open rejections. Section 5 unblocked.**

---

## Section 5 — North Star Test

*Required for user-facing deliverables per CLAUDE.md §North Star Test (Process Gate).*

**Scenario:** IMF analytical team challenges the 340,000 poverty headcount figure during the
Demo 7 live external session (#843), Act 2 — Zambia three-scenario comparison.

**Capability delivered:** Lucas Ferreira (Persona 1, Programme Analyst, Preparatory entry
state) clicks "▶ Methodology" adjacent to the T3 badge in the Zone 1B sticky panel. In
one click, without leaving the primary viewport, he reads: the ZMB Q1 population used
(3,894,625, UN WPP 2024, 20% Q1 fraction), the CI band derivation (±13–16%, T3 placeholder,
ADR-007 forward trace, factor citations), the extraction path (Q1 CHT cohort mean with main
entity fallback), and the T3 rationale (ECOWAS regional comparables, not calibrated
country-level income share data).

**What changed at the table:** Before G5, the T3 badge was an epistemic signal with no
substantive backing accessible from the viewport — Lucas could note "T3 uncertainty" but
could not name the methodology in the room without external documentation. After G5, Lucas
can name the full methodology chain in response to a direct challenge, closing the gap between
"the tool says 340,000" and "here is the methodology you can audit."

**North star test:** PASS. Authored by Business PO, confirmed by PI Agent.

---

## Section 6 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist:**

- [x] All implementation PRs merged; CI green on implementation PR (Section 2)
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable, with L3 sequencing confirmed (Section 3)
- [x] Customer Agent Layer 3 assessment on record, filed before BPO final verdict cleared (Section 3 — sequencing note)
- [x] No open rejection artifacts from G5 (Section 4)
- [x] No near-miss entries required (no rejections in G5)
- [x] North star test artifact on record for user-facing deliverable (Section 5)
- [x] Enhancement issue #1441 filed for non-blocking L3 forward notes (extraction path entity_id interpolation; CI factor percentage labels)

**PI Agent sprint exit verdict:** Confirmed — all exit conditions satisfied.

**PI Agent confirmation:**

> G5 exit conditions are fully satisfied. PR #1439 CI is green across all required checks.
> Business PO ACCEPT is on record for #1422 (the sole user-facing deliverable). Customer
> Agent L3 PASS is on record; the BPO-conditional-then-L3 sequencing is documented and
> compliant. No rejection artifacts were filed in G5. The north star test is on record in
> the BPO validation and confirmed here. Enhancement issue #1441 captures the two
> non-blocking L3 forward notes for a future sprint. #1238 required no code change and
> was correctly closed by verifying ACs against the existing main branch.
>
> G5 is closed. Integration PR (sprint/m18-g5 → release/m18) may now open.

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G5 of M18. It supersedes any informal exit
notation in SESSION_STATE.md for this sprint. Filed at
`docs/process/sprint-plans/m18-g5-sprint-exit.md`.

*The PI Agent confirmation in Section 6 is the gate. Sprint G5 is closed as of 2026-06-28.*
