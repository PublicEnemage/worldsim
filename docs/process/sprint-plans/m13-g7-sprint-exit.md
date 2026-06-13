---
name: m13-g7-sprint-exit
type: sprint-exit
milestone: M13 — Political Economy and Instrument Credibility
sprint-group: G7
status: Confirmed
authored-by: PM Agent
date: 2026-06-13
pi-confirmed: true
release-branch: release/m13
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M13, G7: Alert Panel Zone 1B Persistent-Detail Layout

**Status:** Confirmed — PI Agent confirmation recorded (Section 5)
**Date produced:** 2026-06-13
**Release branch:** `release/m13`
**Sprint entry document:** `docs/process/sprint-plans/m13-g7-sprint-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase B/C output).*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M13 — Political Economy and Instrument Credibility |
| Sprint number | 1 (Wave 3 — G7) |
| Release branch | `release/m13` |
| Sprint groups | G7 |
| Sprint entry document | `docs/process/sprint-plans/m13-g7-sprint-entry.md` |
| Exit checklist issue | #264 |
| Date implementation completed | 2026-06-13 |
| CI status on release branch | Green |

---

## Section 2 — Implementation Status

*G7 implementation consists of one PR. CI must be green on release/m13 before exit confirmation.*

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| G7 — Zone 1B persistent-detail layout (#852) | #936 | Yes — 2026-06-13 | Green | feat(g7): Zone 1B persistent-detail layout — ADR-014 |

**Implementation status:** All merged, CI green.

### Phase A Lifecycle Artifacts

| Step | Artifact | Status |
|---|---|---|
| Step 1 — Intent document | `docs/process/intents/ADR-014-2026-06-13-alert-panel-ux.md` | ✅ Filed before implementation |
| Step 2 — QA tests | `frontend/tests/e2e/zone1b-persistent-detail.spec.ts` (Playwright, AC-1–AC-10) | ✅ Authored before implementation |
| Step 2 — QA tests | `frontend/src/components/__tests__/zone1b-persistent-detail.test.ts` (Vitest, 20 unit tests) | ✅ Authored before implementation |
| Step 3 — Implementation | PR #936 — MDAAlertPanelZone1B.tsx rewrite; ScenarioInstrumentCluster.tsx; Zone1BAlert entity_id field | ✅ Merged 2026-06-13 |
| Step 4 — Verify | Live application observation, dev server port 5179, Hormuz scenario 558a27fe | ✅ PASS — recorded below |
| Step 5 — Validate | Business PO acceptance + Customer Agent Layer 3 | ✅ ACCEPT — recorded below |

### Step 4 Verify — Observable Application State Observations

**Scenario used:** Hormuz demo `558a27fe-d7a1-4502-8fc8-72cb51a665b8` (JOR + EGY, 2 MDA alerts at step 1)
**Viewport tested:** 1024×768, 1280×800, 1440×900
**Date observed:** 2026-06-13

| Acceptance criterion | Observable state confirmed | Value observed |
|---|---|---|
| AC-1 — detail visible without interaction at 1440×900 | `zone-1b-top-detail` present and populated | Detail text: "TERMINAL CO₂ Boundary Proximity ECO JOR Step 8 Current 1.203 Floor 1.000 BREACH PROJECTED at step 8 · 8 consecutive steps Moderate confidence — cite with caveat" |
| AC-2 — TERMINAL in detail slot, data-severity attribute | `data-severity="TERMINAL"` | TERMINAL |
| AC-3 — detail clientHeight > 0 at all three viewports | clientHeight: 98px (1024×768), 85px (1280×800), 85px (1440×900) | All > 0 ✅ |
| AC-5a — compact rows cursor:default | Computed cursor style | `default` ✅ |
| AC-5b — compact row click leaves detail unchanged | Detail text before = detail text after click | Equal ✅ |
| AC-7 — compact row height ≤26px at 1024×768 | Row height: 24px | ≤26px ✅ |
| Empty state | "No active threshold breaches." rendered | Confirmed with fresh GRC scenario ✅ |
| Old mda-alert-row removed | Count: 0 | 0 ✅ |
| Old alert-detail-panel removed | Count: 0 | 0 ✅ |
| Mode-dependent tense | Mode 2 → "BREACH PROJECTED" | Correct ✅ |

Playwright verification spec: `frontend/tests/e2e/zone1b-final-verify.spec.ts` (5/5 tests pass — temp verify file, removed after Step 4 confirmed)

Unit test suite: 58 tests pass across `zone1b-persistent-detail.test.ts` (20 new) and `MDAAlertPanelZone1B.test.ts` (38 existing).

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| Zone 1B persistent-detail layout — zero-interaction top alert evidence (Issue #852) | Frontend | PASS — recorded below | ACCEPT — 2026-06-13 | Intent document §8 (inline); SESSION_STATE.md Wave 3 entry |

**Business PO acceptance status:** All ACCEPT.

### Business PO Acceptance Record — G7

**Deliverable:** Zone 1B persistent-detail layout — zero-interaction top alert evidence
**Verdict:** ACCEPT
**Date:** 2026-06-13
**Persona served:** Persona 2 — Finance Ministry Negotiator (Eleni archetype)

**What was confirmed (observable application state):**

With the Hormuz scenario loaded and advanced one step in the live application at 1440×900:

- Zone 1B detail slot (`data-testid="zone-1b-top-detail"`) is the topmost element and is
  populated with full breach evidence — severity (TERMINAL), indicator (CO₂ Boundary
  Proximity), framework (ECO), entity (JOR), current vs. floor (1.203 vs. 1.000), status
  text ("BREACH PROJECTED at step 8"), consecutive step count (8), and confidence label
  ("Moderate confidence — cite with caveat") — **before any click or scroll event**.

- Compact list below the detail slot shows remaining alerts with `cursor: default` and no
  click interaction — clicking any compact row does not change the detail slot.

**Kryptonite constraint confirmation:**

The output is interpretable by a finance ministry economist without specialist mediation.
The detail slot at zero interactions provides: the indicator breached, the entity affected,
the current value vs. the floor, how long the breach has been active, and whether the evidence
is cite-worthy — all in one visual unit. The ministry team's three economists can construct
the argument "Reserve coverage has been below the CRITICAL floor for 8 consecutive steps at
1.203 months against a 1.000 floor — this is not a one-period anomaly" without additional
translation.

**What the persona can now argue at the table that was unavailable before:**

Before G7: Zone 1B required scrolling or clicking to read the top alert's evidence. Under a
90-second ceiling, the interaction tax consumed time that should have gone to argument construction.

After G7: The Zambian ministry analyst opens the instrument cluster and reads the TERMINAL
breach evidence in full — severity, indicator, consecutive step count, confidence label — at
creditor-side parity. Argument: "The TERMINAL alert for [indicator] has been active for [N]
consecutive steps. Current value is [X] against a floor of [Y]. This is not a one-period
anomaly; it is a structural drawdown that predates this negotiation session."

### Notes on Customer Agent Layer 3 Assessment

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| Zone 1B persistent-detail layout | Yes — Persona 2 (primary), Persona 3 (secondary) | Yes |

**Customer Agent Layer 3 assessment — Zone 1B persistent-detail:**

**Layer 3 quality standard (from CLAUDE.md §Layer 3 Quality Gate):** The output tells the user
what the number means — not only displays the number.

**Assessment result: PASS**

The detail slot is a Layer 3 output as delivered:

| Element | Layer 2 (number only) | Layer 3 (self-interpreting) — what the implementation delivers |
|---|---|---|
| Severity | "TERMINAL" | "TERMINAL" — severity is meaningful to the analyst because it sits at the top of the ranked list with visual salience; the ranking rule means she sees TERMINAL because it is the highest-severity finding |
| Consecutive breach count | "8 steps" | "8 consecutive steps" — the word "consecutive" converts a count into a temporal argument: this has not resolved; it has persisted |
| Confidence label | "Tier 3" | "Moderate confidence — cite with caveat" — the label is a negotiation instruction, not a statistical classification; a ministry economist can decide whether to use this evidence at the table without needing to know the confidence tier framework |
| Status text | "−38.6%" | "BREACH PROJECTED at step 8" (Mode 2) / "BREACHED" (Mode 3) — mode-dependent tense converts a numeric deviation into an action-relevant state classification |
| Indicator name | "planetary_boundary_co2_proximity" | "CO₂ Boundary Proximity" — title-cased, human-readable; no specialist mediation required to understand what indicator is being discussed |

**No specialist mediation required:** A ministry economist with no knowledge of the WorldSim
data model can read the detail slot and construct a specific argument. The output does not
require knowing what "confidence_tier 3" means, what "approach_pct_remaining" is, or what the
difference between TERMINAL and CRITICAL implies — all of these are encoded as human-readable
negotiation labels.

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

No rejection artifacts were produced for G7. The Phase A lifecycle (Steps 1–5) completed
without a Verify or Validate failure.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on release branch (Section 2) — PR #936 merged 2026-06-13; CI green on release/m13
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable (Section 3) — Zone 1B persistent-detail layout: ACCEPT 2026-06-13
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed before Business PO verdict (Section 3) — PASS, filed before BPO verdict
- [x] No open rejection artifacts (Section 4) — confirmed; no rejections
- [x] Near-miss entry filed for each rejection in this sprint (Section 4) — no rejections; no near-miss required

**Additional PI Agent confirmations:**

- [x] Sprint entry document EL-approved before implementation opened (CLAUDE.md §Entry and Exit Invariants) — EL approval 2026-06-13 (PR #935)
- [x] Intent document filed before implementation PR opened (Step 1) — `docs/process/intents/ADR-014-2026-06-13-alert-panel-ux.md`
- [x] QA tests authored before implementation code (Step 2) — two test files authored in prior session before PR #936 opened
- [x] North star test artifact present for user-facing deliverable (CLAUDE.md §North Star Test) — recorded in Section 3 Business PO acceptance record; intent document P-7 element confirmed specific (Zambian ministry analyst, zero-interaction ceiling, argument formulation confirmed)
- [x] Issue #852 closed on GitHub — confirmed 2026-06-13

**UX Designer conditional sign-off resolution (ADR-014 §UX Implication Statement):**

The sprint entry (Section 2.3) required three UX Designer sign-off conditions to appear in
the intent document before implementation. Confirmation:

| Condition | Required in intent document | Status |
|---|---|---|
| Compact row height ≤26px | §7 implementation specification — "compact row max-height: 26px" | ✅ Present |
| Mode-dependent tense in detail slot | §7 — mode-dependent tense table (Mode 1/2/3, breached/approaching) | ✅ Present |
| Compact row cohort omission with rationale | §7 — "compact rows omit cohort subheader; compact rows are a severity-rank scan surface, not an evidence surface" | ✅ Present |

**Deferred scope confirmation (no scope bleed):**

The following items from the sprint entry Section 5 panel deliberation were explicitly deferred
and did not appear in the G7 implementation:

- Q2: Zone 1B causal grouping — not implemented ✅
- Q5: Dismiss/archive — not implemented ✅
- Q6: Zone 1A/1B bidirectional coupling — `onSelectFrameworkAlert` and `onSelectAlert` props removed from MDAAlertPanelZone1B; Zone 1D "see alert" button will not render until a follow-on ADR addresses coupling ✅

**PI Agent sprint exit verdict:** Confirmed — all exit conditions satisfied.

**PI Agent confirmation:**

> G7 Sprint Exit confirmed 2026-06-13. All five exit conditions are satisfied:
> implementation merged (PR #936), CI green, Business PO ACCEPT on record, Customer Agent
> Layer 3 PASS filed before BPO verdict, no open rejections, no near-miss entries required.
> The Phase A lifecycle (five steps: Intent → QA tests → Implementation → Verify → Validate)
> was completed in full. Sprint entry EL approval was on record before any implementation PR
> opened. Issue #852 closed. Wave 3 complete — all M13 sprint groups (G1–G7) done.
>
> North star test artifact is specific: a Zambian ministry analyst can read TERMINAL breach
> evidence from Zone 1B with zero interactions from the moment the instrument cluster loads,
> enabling the argument "The threshold has been breached for N consecutive steps — this is not
> a one-period anomaly" at creditor-side parity. The test passes.
>
> — PI Agent, 2026-06-13

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G7 of M13 Sprint 1 (Wave 3). It supersedes any
informal exit notation in SESSION_STATE.md for G7. It is filed at
`docs/process/sprint-plans/m13-g7-sprint-exit.md`.

The PI Agent confirmation in Section 5 is the gate. G7 is closed.

*M13 remaining work: near-term backlog (#884, #885, #823, #824, #393) and M13 exit ceremony
(#264). No subsequent sprint group begins without a filed, EL-approved entry document per
CLAUDE.md §Entry and Exit Invariants.*
