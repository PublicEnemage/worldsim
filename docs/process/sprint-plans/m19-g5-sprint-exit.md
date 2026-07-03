---
name: m19-g5-sprint-exit
type: sprint-exit
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G5 — Demo 8 Display Fidelity + Zone 1 View Model
status: In-progress
authored-by: PI Agent
date: 2026-07-03
pi-confirmed: false
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M19, G5: Demo 8 Display Fidelity + Zone 1 View Model

**Status:** In-progress — awaiting BPO acceptance verdicts for user-facing deliverables
**Date produced:** 2026-07-03
**Release branch:** `release/m19`
**Sprint entry document:** `docs/process/sprint-plans/m19-g5-sprint-entry.md` — EL-approved 2026-07-03 (PR #1663)
**Sprint journal issue:** #1660
**Exit checklist issue:** #1535

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase C output).
G5 delivers Demo 8 display fidelity fixes: Zone 1A y-axis tight scoping for three-scenario ZMB
comparison (#1629), Zone 1D per-framework delta annotations implementing ADR-017 §Zone 1D
Integration required companion (#1630), api_contracts.yml schema gap fix (#1632), and seven
NM process codification items (Phase A). Phase C (#1522, #1524) deferred to next sprint group
— capacity consumed by Demo 8 display work and UX panel resolution.*

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
| Date implementation completed | 2026-07-03 |
| CI status on sprint branch | Green — all required sprint-branch-ci-gate checks passing on all Phase B PRs (#1666, #1667, #1668, #1669). playwright-e2e check FAILURE on #1668/#1669 is pre-existing known behavior — requires live Docker Compose stack not available in standard CI. Not a required check; does not block merge. |

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

### Phase C — Zone 1 View Model (deferred)

| Group | PRs | Status | Notes |
|---|---|---|---|
| View model layer retrofit (#1522) | None | Deferred — no capacity remaining after Phase B + UX panel resolution | To be scoped for G6 or later; no implementation PR opened in G5 |
| Zone 1A interaction layer (#1524) | None | Deferred — same reason | To be scoped for G6 or later; no implementation PR opened in G5 |

**Implementation status:** All in-scope implementation merged, CI green on required checks.
Phase C deferred to next sprint group per capacity-conditional rule in sprint entry §3.1.

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

*User-facing deliverables: #1629 and #1630. Phase A (NM codification) and #1632 (schema fix)
are process/infrastructure — no BPO acceptance required.*

| Deliverable | Work type | Customer Agent L3 | BPO verdict | Verdict artifact |
|---|---|---|---|---|
| #1629 — Zone 1A y-axis tight scoping | Frontend | N/A — display fidelity fix; no new Persona 2/3/5 capability introduced | **Pending — EL/BPO to record** | Pending |
| #1630 — Zone 1D delta annotations (Mode 3) | Frontend | N/A — ADR-017 required companion; no new Persona 2/3/5 capability introduced; Mode 3 north star foundation | **Pending — EL/BPO to record** | Pending |

**Business PO acceptance status: PENDING — gate not yet cleared.**

### BPO acceptance prompt

EL / Business PO: please review the two user-facing deliverables and record an ACCEPT or
REJECT verdict on each by posting a comment on this issue (#1660) or on the individual GitHub
issues (#1629, #1630). Reference the acceptance criteria in the intent documents:

- `docs/process/intents/M19-G5-2026-07-03-zmb-yaxis-tight-scoping.md` (AC-1 through AC-4)
- `docs/process/intents/M19-G5-2026-07-03-zone1d-delta-annotations.md` (AC-1 through AC-5)

For verification, the E2E tests encode the acceptance criteria:
- `frontend/tests/e2e/m19-g5-zmb-yaxis-tight-scoping.spec.ts`
- `frontend/tests/e2e/m19-g5-zone1d-delta-annotations.spec.ts`

Once both verdicts are on record, update Section 3 above and proceed to Section 5.

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

**North star test assessment:** Authored by PI Agent pending BPO endorsement. BPO to confirm
or revise this assessment at verdict time.

---

## Section 6 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist:**

- [x] All Phase B implementation PRs merged; CI green on required checks (Section 2)
- [x] Phase C items correctly deferred per capacity-conditional rule in sprint entry §3.1 (Section 2)
- [ ] BPO ACCEPT verdict filed for #1629 (Section 3) — **PENDING**
- [ ] BPO ACCEPT verdict filed for #1630 (Section 3) — **PENDING**
- [x] CA L3 assessment — not required (neither deliverable serves new Persona 2/3/5 capability; see Section 3)
- [x] No open rejection artifacts from G5 (Section 4)
- [x] No near-miss entries required (no rejections in G5)
- [ ] North star test artifact endorsed by BPO — **PENDING** (draft in Section 5)
- [ ] PI Agent NM-094 test-file check before integration PR — `git diff release/m19...sprint/m19-g5 | grep -E "test_|\.spec\.ts"` — **not yet run; runs at integration PR time**

**PI Agent sprint exit verdict:** BLOCKED — awaiting BPO ACCEPT verdicts for #1629 and #1630.

**PI Agent confirmation:**

> G5 implementation is complete and all CI gates are clear on required checks. Phase C is
> correctly deferred per the sprint entry capacity-conditional rule. No rejection artifacts
> were filed. The north star test draft is on record in Section 5 and awaits BPO endorsement.
>
> This sprint exit document will be updated to "Confirmed" once the EL/BPO records ACCEPT
> verdicts for #1629 and #1630. After confirmation, NM-094 test-file check runs and the
> integration PR (sprint/m19-g5 → release/m19) may open.

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G5 of M19. It supersedes any informal exit
notation in SESSION_STATE.md for this sprint. Filed at
`docs/process/sprint-plans/m19-g5-sprint-exit.md`.

*The PI Agent confirmation in Section 6 is the gate. The sprint closes when the PI Agent's
verdict is "Confirmed." The integration PR (sprint/m19-g5 → release/m19) may not open until
the PI Agent verdict is "Confirmed."*
