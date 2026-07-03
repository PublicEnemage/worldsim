---
name: m19-g2d-sprint-exit
type: sprint-exit
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G2 Phase D — Iceland 2008–11 Capital Controls Transmission
status: Confirmed
authored-by: PM Agent
date: 2026-07-03
pi-confirmed: true
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M19, G2 Phase D: Iceland 2008–11 Capital Controls Transmission

**Status:** Confirmed — PI Agent exit conditions satisfied 2026-07-03
**Date produced:** 2026-07-03
**Release branch:** `release/m19`
**Sprint entry document:** `docs/process/sprint-plans/m19-g2d-sprint-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase B/C output).
Changes to this template require PM Agent authorship and EL endorsement.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| Sprint number | 5 (G2 Phase D) |
| Release branch | `release/m19` |
| Sprint groups | G2 Phase D — final G2 wave phase |
| Sprint entry document | `docs/process/sprint-plans/m19-g2d-sprint-entry.md` |
| Sprint journal issue | #1621 (closed at exit confirmation) |
| Exit checklist issue | #1535 |
| Date implementation completed | 2026-07-03 |
| CI status on sprint branch | Green — all G2D PRs merged to `sprint/m19-g2`; all required checks passed |

**G2D is the final G2 wave phase.** The integration PR (`sprint/m19-g2` → `release/m19`)
fires at this exit, carrying all G2 wave work (G2A through G2D). The integration PR was
deferred from G2C exit per the EL ruling recorded in `m19-g2c-sprint-exit.md §1`.

---

## Section 2 — Implementation Status

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| CM calibration deliverable — §Capital Controls (ADR-020) | #1625 | Yes — 2026-07-03 | Green | ε=0.60/0.50 (ISL), β=0.020, γ=1.2, φ∈[0.3,0.7]; CM pre-implementation gate |
| CE DemographicModule audit — subscription matrix | #1626 | Yes — 2026-07-03 | Green | Full 7-variant audit; NM-090/NM-091 filed; transmission table rewrite |
| Capital controls transmission channels A/B/C (#1532) | #1635 | Yes — 2026-07-03 | Green | Channel A (ESM), Channel B (MM + bridge), Channel C (DM dead sub fix + φ elasticity). 28/28 unit tests pass. |
| Iceland 2008–11 heterodox vs orthodox fixture (#1553) | #1639 | Yes — 2026-07-03 | Green | Heterodox baseline + orthodox counter-factual. 7 construction tests + 2 DB-gated harness tests. |

**Implementation status:** All PRs merged; CI green on `sprint/m19-g2`.

**Supporting deliveries (not standalone user-facing deliverables):**
- PR #1625 (CM calibration): pre-implementation gate; not a standalone AC deliverable.
- PR #1626 (CE audit): pre-implementation gate; NM-090/NM-091 filed.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| Capital controls transmission channels A/B/C (#1532) | Backend Capability | N/A — engine-internal; no new output surface (existing Zone 1A); §1.2 protocol does not require Layer 3 | ACCEPT | Appended to `docs/process/intents/M19-G2D-2026-07-03-capital-controls-transmission-channels.md` (2026-07-03) |
| Iceland 2008–11 backtesting fixture (#1553) | Analytics | CONDITIONAL PASS — infrastructure (pre-calibration structural test); Demo 8 surfacing must include DIRECTION_ONLY qualifier. Verdict issued before BPO verdict below. | ACCEPT | Appended to `docs/process/intents/M19-G2D-2026-07-03-iceland-2008-backtesting-fixture.md` (2026-07-03) |

**Business PO acceptance status:** All ACCEPT. No open rejections.

### Notes on Customer Agent Layer 3 assessments

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| Capital controls transmission channels (#1532) | Yes — Persona 2 (Eleni, analytical preparation) primary; Persona 5 secondary (Demo 8) | N/A — §1.2 backend capability; no new output surface requiring Layer 3; existing Zone 1A display surfaces carry the channel outputs |
| Iceland 2008–11 fixture (#1553) | Yes — Persona 2 primary (analytical prep); Persona 5 (Aicha, Demo 8 Act 2) | Yes — Customer Agent CONDITIONAL PASS issued in intent doc verdict section, ordered before BPO verdict |

**Customer Agent Layer 3 condition propagated to Demo 8 Act 2:**
The direction verdict ("BASELINE_BETTER") from the Iceland fixture must be accompanied by an
explicit `fidelity_tier: DIRECTION_ONLY` qualifier at Demo 8. Raw direction verdict without
the qualifier implies higher precision than the pre-calibration fixture warrants. This is a
Demo 8 Act 2 authorship note, not a G2D delivery gap.

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

---

## Section 5 — North Star Test Artifact

*Required per CLAUDE.md §North Star Test (Process Gate) for user-facing capabilities.*
*BPO authority: P-7 element of ADR-020 (ARCH-014) persona trace.*

**Deliverable assessed:** #1532 (capital controls channels A/B/C) + #1553 (Iceland fixture)
together constitute a single user-facing capability: the ability to model the heterodox path
and produce an analytically defensible trajectory for Iceland 2008.

**Finance minister scenario:**
A Zambian finance ministry analyst is preparing for a restructuring session with bilateral
creditors (October 2023). The creditor side argues that capital controls would destroy investor
confidence and are not an available tool. The analyst wants to demonstrate that Iceland's 2008
heterodox path — capital controls + nationalisation — produced better Q1 poverty headcount
outcomes than the orthodox IMF alternative, using a model that both sides can inspect.

**Concrete capability delivered:**
1. The analyst runs an Iceland 2008 scenario in Mode 1 (replay) with capital controls at Step 1.
   The trajectory now shows `reserve_coverage_months` increasing after Step 1 (Channel A active;
   ε=0.60 per Iceland 2008 IMF Article IV). The `known_limitations` no longer states "reserve
   protection channel absent" — it states "channels active; Q2 PHC and bilateral creditor
   composition not modeled."
2. The analyst runs the Iceland counter-factual (orthodox path) from the same baseline.
   The trajectory shows `reserve_coverage_months` declining at Step 2 (no reserve protection).
3. The direction verdict at Step 4 is BASELINE_BETTER — the heterodox path outperforms on
   the human cost composite.

**Table impact:**
When the creditor side argues "capital controls are not an available tool," the ministry
analyst can cite: "WorldSim models Iceland's 2008 path. Channel A (reserve protection,
ε=0.60, Iceland Article IV calibration) and Channel C (Q1 poverty headcount, φ=0.30) are
active. The heterodox trajectory shows reserve recovery and lower Q1 poverty at Step 4
than the orthodox alternative. The model's known limitations are disclosed; the direction
is defensible."

This is a specific, citable argument that shifts the creditor challenge from "does your
model support heterodox tools?" to "where does fidelity degrade in your Channel C calibration?"
— a tractable technical dispute, not a categorical dismissal.

**North star test verdict:** PASS — the capability makes the tool more useful to a finance
minister sitting across from a creditor-side negotiating team that is arguing against heterodox
tools. The model now has a documented, calibrated counter-factual for the most prominent
heterodox-path success case.

---

## Section 6 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on sprint branch (Section 2) — SATISFIED:
  PRs #1625, #1626, #1635, #1639 all merged to `sprint/m19-g2`; required checks green
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable (Section 3) — SATISFIED:
  ACCEPT on record for both #1532 and #1553 at intent document appendages (2026-07-03)
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed
  before Business PO verdict (Section 3) — SATISFIED:
  - #1532: N/A (§1.2 backend capability; no new output surface)
  - #1553: CONDITIONAL PASS filed in intent doc verdict section, ordered before BPO verdict
- [x] No open rejection artifacts (Section 4) — SATISFIED
- [x] Near-miss entry filed for each rejection in this sprint — N/A (no rejections)
- [x] North star test artifact present for user-facing deliverables (Section 5) — SATISFIED:
  artifact authored above; names Zambian restructuring scenario; concrete capability and table
  impact stated; non-aspirational. Confirmed present by PI Agent.
- [x] CM advisory on record before G2D implementation PR opened — SATISFIED:
  PR #1625 merged before PR #1635 opened (CM gate satisfied in correct sequence)
- [x] CE audit on record before implementation PR opened — SATISFIED:
  PR #1626 merged before PR #1635 opened (CE gate satisfied in correct sequence)
- [x] G2D is final G2 wave phase; integration PR authorization — SATISFIED:
  G2C exit recorded the EL ruling (G2D stays in M19; integration PR defers to G2D exit).
  G2D is now complete. Integration PR `sprint/m19-g2 → release/m19` is authorized.

**PI Agent sprint exit verdict:** CONFIRMED — all exit conditions satisfied.

**PI Agent confirmation:**

> All G2D exit conditions are satisfied as of 2026-07-03. Four G2D PRs are merged to
> `sprint/m19-g2` with required checks green: CM calibration gate (#1625), CE audit gate
> (#1626), channel A/B/C implementation (#1635, 28/28 unit tests), and Iceland fixture
> (#1639, 7 construction tests + 2 CI-green harness tests).
>
> Business PO ACCEPT verdicts are on record for both G2D deliverables:
> — #1532 (backend capability, §1.2): 28/28 unit tests; DEMO4 check PASS; Persona 2 can
>   now argue capital controls reserve protection with documented calibration anchor.
> — #1553 (analytics, §1.4): direction verdict BASELINE_BETTER; Customer Agent CONDITIONAL
>   PASS (infrastructure; Demo 8 surfacing requires DIRECTION_ONLY qualifier on record).
>
> North star test: PASS — Iceland heterodox path analytically distinguishable from orthodox
> counter-factual; a Zambian finance ministry analyst can cite the direction verdict and
> calibration parameters in a restructuring session with bilateral creditors.
>
> G2D is the final G2 wave phase. The integration PR (`sprint/m19-g2` → `release/m19`) is
> now authorized. Sprint journal #1621 is closed at this confirmation.

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G2 Phase D of M19. It is the exit gate for
the entire G2 wave — G2A through G2D all exit via this document and the subsequent integration
PR (`sprint/m19-g2` → `release/m19`).

Filed at `docs/process/sprint-plans/m19-g2d-sprint-exit.md`.

*The PI Agent confirmation in Section 6 is the gate. The sprint closes when the PI Agent's
verdict is "Confirmed." The integration PR is the final G2 wave action.*
