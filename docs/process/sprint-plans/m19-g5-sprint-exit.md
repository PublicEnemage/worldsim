---
name: m19-g5-sprint-exit
type: sprint-exit
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G5 — Demo 8 Display Fidelity + Zone 1 View Model
status: Confirmed
authored-by: PI Agent
date: 2026-07-03
pi-confirmed: true
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M19, G5: Demo 8 Display Fidelity + Zone 1 View Model

**Status:** Confirmed — all exit conditions satisfied (BPO ACCEPT 2026-07-03)
**Date produced:** 2026-07-03
**Release branch:** `release/m19`
**Sprint entry document:** `docs/process/sprint-plans/m19-g5-sprint-entry.md` — EL-approved 2026-07-03 (PR #1663)
**Sprint journal issue:** #1660
**Exit checklist issue:** #1535

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase C complete, updated 2026-07-03).
G5 delivers Demo 8 display fidelity fixes: Zone 1A y-axis tight scoping (#1629), Zone 1D per-framework
delta annotations implementing ADR-017 §Zone 1D Integration required companion (#1630), api_contracts.yml
schema gap fix (#1632), and seven NM process codification items (Phase A). Phase C also delivered in G5:
view model layer retrofit (#1522, trajectoryViewModel.ts extraction) and Zone 1A trackwheel zoom (#1524,
desktop scroll wheel, EL-reduced scope). BPO ACCEPT for all four user-facing deliverables (#1629, #1630,
#1522, #1524). Integration PR #1684 `sprint/m19-g5 → release/m19` opened 2026-07-03.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| Sprint group | G5 — Demo 8 Display Fidelity + Zone 1 View Model |
| Release branch | `release/m19` |
| Sprint sub-branch | `sprint/m19-g5` |
| Sprint entry document | `docs/process/sprint-plans/m19-g5-sprint-entry.md` |
| Exit checklist issue | #1535 |
| Sprint journal issue | #1660 |
| Date implementation completed | 2026-07-03 (Phase C) |
| CI status on sprint branch | Green — all required sprint-branch-ci-gate checks passing on all Phase B PRs (#1666–#1669) and Phase C PRs (#1679, #1681). playwright-e2e check FAILURE is pre-existing known behavior — requires live Docker Compose stack; not a required check; does not block merge. |

---

## Section 2 — Implementation Status

*All implementation PRs merged to sprint/m19-g5. Required checks: `audit`, `changes`,
`branch-naming`, `session-state-size-check`, `test-backend`, `lint`, `compliance-scan`.*

### Phase A — NM Process Codification (complete at sprint entry)

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| NM codification (#1650–#1656) | #1658 | Yes | Green | NM-084/085/086/089/092/093/094 improvements to sprint-planning-sop.md, CODING_STANDARDS.md, sprint-group-isolation.md |

### Phase B — Demo 8 Display Fidelity and Schema Gap

| Group | PRs | Merged? | CI status | Notes |
|---|---|---|---|---|
| QA tests (#1629, #1630) | #1666 | Yes | Green | Tests authored before implementation; RED state at merge (functions not yet exported) |
| Schema fix (#1632) | #1667 | Yes | Green | api_contracts.yml: band_method, is_meaningless, suppressed_reason |
| Zone 1A y-axis tight scoping (#1629) | #1668 | Yes | Green (required checks) | computeYDomain excludes MDA floor in comparison mode; floor line suppressed when comparisonDataMin - floor > 0.10 |
| Zone 1D delta annotations (#1630) | #1669 | Yes | Green (required checks) | formatDelta, getDeltaColor exported; baseline_trajectory from Zustand store; Mode 3 only |

### Phase C — Zone 1 View Model (delivered in G5)

| Group | PRs | Merged? | CI status | Notes |
|---|---|---|---|---|
| View model layer retrofit (#1522) | #1679 | Yes | Green (required checks) | trajectoryViewModel.ts: MergedStepDatum, computeYDomain, computeDivergenceFill, getConfidenceBadgeVisible, mergeTrajectories (visibleStepRange param), sliceToStepRange. 33 unit tests GREEN. |
| Zone 1A trackwheel zoom (#1524) | #1681 | Yes | Green (required checks) | visibleStepRange state + non-passive wheel listener + double-click reset + data-visible-step-min/max. Desktop trackwheel only (EL scope decision 2026-07-03). |

**Implementation status:** All Phase A, B, and C implementation merged; CI green on all required checks.

### Scope change note — #1630

The sprint entry described #1630 as BLOCKED_UX_PANEL (per-framework lines in Zone 1A requiring
Architect + UX Designer panel review and potential ADR amendment). During this session, the
Architect finding resolved the scope change:

> ADR-017 §Zone 1D Integration (Mode 3) already mandated per-framework delta annotations as a
> "required companion" to the composite-only Zone 1A encoding. This companion was never
> implemented. The correct remedy for #1630 (Demo 8 narration implying per-framework lines in
> Zone 1A) is to implement the mandated Zone 1D annotations — not to add lines to Zone 1A
> (which would conflict with ADR-017's composite-only Zone 1A contract).

BLOCKED_UX_PANEL was cleared: the implementation path is fully backed by ADR-017 with no new
ADR required. The #1630 intent was updated accordingly (see `docs/process/intents/M19-G5-2026-07-03-zone1d-delta-annotations.md`). Demo narration in `demo-narrated.spec.ts` updated to reference Zone 1D correctly.

---

## Section 3 — Business PO Acceptance Table

*User-facing deliverables: #1629, #1630, #1522, #1524. Phase A (NM codification) and #1632 (schema fix)
are process/infrastructure — no BPO acceptance required.*

| Deliverable | Work type | Customer Agent L3 | BPO verdict | Verdict artifact |
|---|---|---|---|---|
| #1629 — Zone 1A y-axis tight scoping | Frontend | N/A — display fidelity fix; no new Persona 2/3/5 capability introduced | **ACCEPT** | #1629#issuecomment-4879773995 |
| #1630 — Zone 1D delta annotations (Mode 3) | Frontend | N/A — ADR-017 required companion; no new Persona 2/3/5 capability introduced; Mode 3 north star foundation | **ACCEPT** | #1630#issuecomment-4879774027 |
| #1522 — View model layer retrofit | Frontend infrastructure | N/A — pure architectural extraction; no user-visible change; seam prerequisite for #1524 | **ACCEPT** | #1522#issuecomment-4880120492 |
| #1524 — Zone 1A trackwheel zoom (desktop) | Frontend | N/A — Demo 8 analyst navigation capability; Mode 3 north star instrument; no new Persona 2/3/5 live data capability | **ACCEPT** | #1524#issuecomment-4880121152 |

**Business PO acceptance status: All ACCEPT — gate cleared 2026-07-03 (Phase C updated).**

### Customer Agent L3 sequencing note

Neither #1629 nor #1630 introduces a new capability for Personas 2, 3, or 5 as defined in
`docs/ux/personas.md`. #1629 is a display fidelity fix (y-axis domain calculation correction).
#1630 implements a required companion mandated by ADR-017 for Mode 3 active control — Mode 3
is the north star but is not yet serving live Persona 2/3/5 users. CA L3 assessment is not
a precondition for the BPO verdict on these deliverables.

---

## Section 4 — Open Rejections

No REJECT verdicts issued in G5 (Phase A, B, or Phase C-deferred). No rejection artifacts filed.

**No open rejections. Section 5 gated only on BPO acceptance (Section 3).**

---

## Section 5 — North Star Test

*Required for user-facing deliverables per CLAUDE.md §North Star Test (Process Gate).
BPO holds R for authoring. PI Agent confirms existence and specificity before exit gate passes.*

**Scenario:** Demo 8 Act 2 — Zambia three-scenario comparison. A Zambian ministry analyst is
preparing to present the Zone 1A comparison chart in a restructuring negotiation session. The
chart shows three programme variants (baseline, moderate reform, aggressive reform). Before
#1629, all three curves visually collapsed to a single band because the MDA floor value (0.40)
anchored the y-scale far below the tightly clustered scenario scores (~0.54–0.63). The analyst
could not use the chart to distinguish the scenarios without explaining the y-axis scaling
problem to the counterparty.

**Capability delivered (#1629):** After the fix, the y-axis is tight-scoped to the actual
data range in comparison mode. The three ZMB scenario curves are visually separated —
each curve is distinguishable at a glance. The MDA floor annotation is suppressed when it
would distort the scale, appearing only when the floor is within 10pp of the data cluster.
The analyst can hand the chart to a counterparty and the comparison is immediately legible.

**Capability delivered (#1630):** In Mode 3 (active control), each framework row in Zone 1D
now shows the per-framework delta from baseline at the current step: e.g.
`Financial: 0.71 (+0.04 vs baseline)`. The delta is color-coded (green = improvement, amber
= regression, gray = neutral). The analyst can see which framework dimensions are driving the
composite improvement — not just the aggregate score — without leaving the instrument cluster.

**What changed at the table:** The ministry analyst can now use Zone 1A comparisons in direct
presentations without pre-explaining y-axis scaling artifacts. Zone 1D now fulfills its
ADR-017 mandate as a per-framework breakdown companion — showing *which* dimensions improved
under the proposed programme, not just the composite. These are two distinct legibility
improvements that together make the Demo 8 narrative coherent.

**North star test assessment:** Confirmed by BPO 2026-07-03 alongside ACCEPT verdicts for
#1629 and #1630. Assessment stands as written.

---

## Section 6 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist:**

- [x] All Phase B implementation PRs merged; CI green on required checks (Section 2)
- [x] All Phase C implementation PRs merged; CI green on required checks — #1679 (#1522), #1681 (#1524) (Section 2)
- [x] Phase C QA tests + intent docs filed before implementation (PRs #1675, #1676)
- [x] BPO ACCEPT verdict filed for #1629 — #1629#issuecomment-4879773995 (2026-07-03)
- [x] BPO ACCEPT verdict filed for #1630 — #1630#issuecomment-4879774027 (2026-07-03)
- [x] BPO ACCEPT verdict filed for #1522 — #1522#issuecomment-4880120492 (2026-07-03)
- [x] BPO ACCEPT verdict filed for #1524 — #1524#issuecomment-4880121152 (2026-07-03)
- [x] CA L3 assessment — not required (no deliverable serves new Persona 2/3/5 live capability; see Section 3)
- [x] No open rejection artifacts from G5 (Section 4)
- [x] No near-miss entries required (no rejections in G5)
- [x] North star test artifact confirmed by BPO (Section 5) — #1524 north star trace recorded in BPO ACCEPT comment
- [x] NM-094 test-file check: `git diff release/m19...sprint/m19-g5 -- '*.spec.ts' '*.test.ts'` confirms new test files present for every Phase B deliverable (#1629, #1630) and Phase C deliverables (#1522, #1524)

**PI Agent sprint exit verdict:** Confirmed — all exit conditions satisfied.

**PI Agent confirmation:**

> G5 exit conditions are fully satisfied. All Phase A, B, and C implementation PRs are merged
> and CI is green on all required sprint-branch-ci-gate checks. BPO ACCEPT verdicts for all
> four user-facing deliverables (#1629, #1630, #1522, #1524) are on record (2026-07-03).
> CA L3 assessment is not required — no deliverable introduces new capability for live
> Personas 2, 3, or 5. No rejection artifacts were filed in G5. The north star test is
> confirmed by the BPO for #1629 + #1630 (Section 5) and for #1524 (BPO ACCEPT comment).
> NM-094 test-file check passed — test files exist for all Phase B and Phase C deliverables.
> Integration PR #1684 `sprint/m19-g5 → release/m19` opened 2026-07-03.
>
> G5 is confirmed (updated: Phase C complete 2026-07-03).

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G5 of M19. It supersedes any informal exit
notation in SESSION_STATE.md for this sprint. Filed at
`docs/process/sprint-plans/m19-g5-sprint-exit.md`.

*The PI Agent confirmation in Section 6 is the gate. The sprint closes when the PI Agent's
verdict is "Confirmed." The integration PR (sprint/m19-g5 → release/m19) may not open until
the PI Agent verdict is "Confirmed."*
