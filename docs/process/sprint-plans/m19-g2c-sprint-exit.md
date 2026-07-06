---
name: m19-g2c-sprint-exit
type: sprint-exit
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G2 Phase C — Battle-Testing Scenario Runs
status: Confirmed
authored-by: PM Agent
date: 2026-07-03
pi-confirmed: true
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M19, G2 Phase C: Battle-Testing Scenario Runs

**Status:** Confirmed — PI Agent exit conditions satisfied 2026-07-03
**Date produced:** 2026-07-03
**Release branch:** `release/m19`
**Sprint entry document:** `docs/process/sprint-plans/m19-g2c-sprint-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase B/C output).
Changes to this template require PM Agent authorship and EL endorsement.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| Sprint number | 4 (G2 Phase C) |
| Release branch | `release/m19` |
| Sprint groups | G2 Phase C |
| Sprint entry document | `docs/process/sprint-plans/m19-g2c-sprint-entry.md` |
| Sprint journal issue | #1589 (closed at exit confirmation) |
| Exit checklist issue | #1535 |
| Date implementation completed | 2026-07-03 |
| CI status on sprint branch | Green — all G2C PRs merged to `sprint/m19-g2`; all required checks passed |

**EL ruling on G2D/ARCH-014 (recorded at G2C exit):**

Per sprint entry §1.5 contingency rule: EL has ruled G2D (Iceland, #1553) stays in M19 Wave 2. G2C is therefore **not the final G2 phase**. The integration PR (`sprint/m19-g2` → `release/m19`) is **deferred to G2D exit**. This ruling is recorded in the sprint journal (#1589) and here as an exit condition artifact.

---

## Section 2 — Implementation Status

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| CM advisory table update — sprint entry §2.2 | #1602 | Yes — 2026-07-03 | Green | Merged to `sprint/m19-g2`; updates §2.2 advisory status for all five new-country scenarios |
| MonetaryVolumeInput deserializer fix | #1603 | Yes — 2026-07-03 | Green | Prerequisite for Egypt and Sri Lanka fixtures; ruff I001 fix included |
| Greece counter-factual Type B (#1547) | #1597 | Yes — 2026-07-03 | Green | Merged to `sprint/m19-g2`; extends `greece_2010_scenario.py` |
| Argentina counter-factual Type B (#1548) | #1598 | Yes — 2026-07-03 | Green | Merged to `sprint/m19-g2`; extends `argentina_2001_2002_scenario.py` |
| Sri Lanka Coffin Corner Type A+B (#1549) | #1605 | Yes — 2026-07-03 | Green | New fixture + TestSriLankaTypeAB (3 tests) |
| Pakistan IMF programme Type B (#1550) | #1606 | Yes — 2026-07-03 | Green | New fixture + TestPakistanTypeB (2 tests) |
| Turkey Backside of Power Curve Type B (#1551) | #1607 | Yes — 2026-07-03 | Green | New fixture + TestTurkeyTypeB (2 tests) |
| Egypt devaluation Type B (#1552) | #1608 | Yes — 2026-07-03 | Green | New fixture + TestEgyptTypeB (2 tests; direction not hardcoded per CM advisory) |
| Ghana IMF programme Type A+B (#1554) | #1611 | Yes — 2026-07-03 | Green | New fixture + TestGhanaTypeAB (3 tests; ruff E501 fix included) |

**Implementation status:** All PRs merged; CI green on `sprint/m19-g2`. Total test count in `backend/tests/backtesting/test_m19_g2c_scenario_runs.py`: 18 tests. All skip without `DATABASE_URL` (NM-056 compliant). Additive approach selected (intent §7) — no skip stubs required.

**Supporting delivery (not a standalone deliverable):** PR #1603 (MonetaryVolumeInput deserializer fix) was a prerequisite unblocking Egypt and Sri Lanka. It is a backend capability fix, not a user-facing deliverable, and does not require a separate Business PO verdict.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| G2C battle-testing scenario runs — all seven (#1547–#1552, #1554) | Analytics | PASS — filed in same comment, ordered before verdict | ACCEPT | Sprint journal #1589 comment (2026-07-03) |

**Business PO acceptance status:** ACCEPT. No open rejections.

### Notes on Customer Agent Layer 3 assessments

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| G2C battle-testing scenario runs | Yes — Persona 2 (Ministry Analyst, analytical preparation mode); Persona 5 secondary (Demo 8) | Yes — Customer Agent AUDIT block in sprint journal #1589 comment, ordered immediately before Business PO verdict in same artifact; temporal sequence within the artifact satisfies the precondition requirement |

**Customer Agent Layer 3 condition (must propagate to Demo 8 Act 2 narrative):**
Raw `per_step_diff` Decimal values must not be presented to Persona 5 (Aicha, World Bank evaluation team) at Demo 8 without narrative interpretation. G2C harness output is appropriate for Persona 2 preparation; Demo 8 narrative layer translates to Persona 5 — this is a Demo 8 Act 2 authorship note, not a G2C delivery gap.

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on sprint branch (Section 2) — SATISFIED: PRs #1597, #1598, #1602, #1603, #1605, #1606, #1607, #1608, #1611 all merged to `sprint/m19-g2`; required checks green
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable (Section 3) — SATISFIED: ACCEPT on record at sprint journal #1589 (2026-07-03), covering all seven G2C issues
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed before Business PO verdict (Section 3) — SATISFIED: Customer Agent AUDIT block in sprint journal #1589 comment, ordered before verdict; temporal sequence within the combined artifact satisfies the precondition
- [x] No open rejection artifacts (Section 4) — SATISFIED
- [x] Near-miss entry filed for each rejection in this sprint — N/A (no rejections)
- [x] North star test artifact present for user-facing deliverables — SATISFIED: north star test artifact embedded in sprint journal #1589 Business PO comment (2026-07-03); names the finance minister scenario (Zambia, IMF restructuring session), the concrete capability (seven-country cross-structural breadth argument), and the table impact (shifts creditor challenge from "is this generalizable?" to "where does fidelity degrade?"). Specific, not aspirational. Confirmed present by PI Agent.
- [x] CM advisory on record before each new-country feature PR opened — SATISFIED: all five CM advisories on record on corresponding issues before PRs opened (confirmed by sprint journal #1589 CM advisory gate update comment, 2026-07-03)
- [x] EL ruling on G2D/ARCH-014 obtained — SATISFIED: G2D stays in M19; integration PR deferred to G2D exit (Section 1)

**PI Agent sprint exit verdict:** CONFIRMED — all exit conditions satisfied.

**PI Agent confirmation:**

> All G2C exit conditions are satisfied as of 2026-07-03. Seven scenario fixture PRs are merged
> to `sprint/m19-g2` with required checks green. The MonetaryVolumeInput deserializer fix (PR
> #1603) unblocked Egypt and Sri Lanka without requiring a separate acceptance gate. Business PO
> ACCEPT verdict is on record at sprint journal #1589 covering all seven G2C issues (#1547,
> #1548, #1549, #1550, #1551, #1552, #1554). Customer Agent Layer 3 PASS is filed and ordered
> before the Business PO verdict in the same comment. North star test artifact is specific and
> present. CM advisory gate was observed for all five new-country scenarios.
>
> EL ruling recorded: G2D (Iceland, #1553) stays in M19 Wave 2. The integration PR
> (`sprint/m19-g2` → `release/m19`) is deferred to G2D exit. G2C closes without an integration
> PR. The G2D sprint entry may now be filed once ADR-020 (ARCH-014, capital controls economic
> transmission gap) authorship and acceptance is complete.
>
> One quality observation is routed to PM Agent (not a rejection criterion): the implementing
> agent used descriptive function naming (`build_sri_lanka_scenario()`, etc.) rather than the
> ISO alpha-3 naming in the intent document appendices (`build_lka_scenario()`, etc.). Entity
> IDs within ScenarioCreateRequest are all correct (AC-NC-3 satisfied). PM Agent to assess
> whether a fixture naming cleanup issue is warranted.
>
> Sprint journal #1589 is closed at this exit confirmation.
>
> — PI Agent (in-session, 2026-07-03)

---

## Section 6 — North Star Test Artifact

*Required per CLAUDE.md §North Star Test (Process Gate). Authored by Business PO; confirmed
present and specific by PI Agent. Source: sprint journal #1589 Business PO comment (2026-07-03).*

**Finance minister scenario:** Zambia Ministry of Finance analyst team, 2026. The Zambian
finance minister's team is preparing for a debt restructuring session with the IMF and the
Official Creditor Committee. A creditor technical advisor has challenged the WorldSim analysis
on Zambia's risk trajectory: "Your CI bounds are too wide to be actionable — how do we know
this model is calibrated to anything?" The ministry team needs to answer this challenge
credibly, without conceding the CI width argument.

**Concrete capability evaluated:** G2C provides the ministry team a specific, citable
counter-argument: WorldSim has been validated against seven sovereign crisis cases spanning
four continents. Sri Lanka (Coffin Corner, all six failure modes simultaneously), Ghana (CB
Cloud — Demo 7 regional comparator now headlessly reproducible), Greece (fiscal multiplier
inversion), Argentina (convertibility exit), Turkey (Backside of the Power Curve under
unorthodox monetary policy), Egypt (a programme that succeeded — confirming the model is not
tuned only to crises), and Pakistan (Get-There-Itis programme suspension). The `known_limitations`
blocks tell the ministry team exactly where structural gaps attenuate confidence.

**Table impact:** After G2C, the ministry team's response to the creditor challenge shifts
from "we tested this against two Sub-Saharan commodity economies" to "we tested against seven
cases on four continents; the challenge is no longer whether the model is generalizable — it
is which structural case exhibits the model's fidelity boundary, and the `known_limitations`
block tells you that per-case." This is a more productive conversation that the ministry team
can drive, not absorb.

**PI Agent specificity confirmation:** The north star test names the finance minister scenario
(Zambia, IMF restructuring session), the concrete capability (seven-country empirical breadth
argument with known_limitations as the boundary disclosure), and the table impact (shifts burden
of specificity to creditor team). Test is specific, not aspirational. Confirmed present.

---

## Section 7 — G2D Entry Gate

**G2D pre-conditions (now unblocked by EL ruling):**

| Condition | Status |
|---|---|
| EL ruling on G2D scope | SATISFIED — G2D stays in M19 (EL ruling 2026-07-03) |
| ADR-020 authorship (ARCH-014 — capital controls economic transmission gap) | REQUIRED before G2D sprint entry — Architect Agent must be activated |
| ADR-020 panel review and acceptance | REQUIRED before G2D sprint entry |
| G2D sprint entry document filed and EL-approved | REQUIRED before any G2D implementation PR opens |

*PM Agent must activate the Architect Agent for ADR-020 before filing the G2D sprint entry.
G2D implementation may not begin without an accepted ADR-020 and an EL-approved sprint entry.*

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for Sprint 4 (G2 Phase C) of M19. It supersedes any
informal exit notation in `SESSION_STATE.md` for this sprint. It is filed at
`docs/process/sprint-plans/m19-g2c-sprint-exit.md`.

*The PI Agent confirmation in Section 5 is the gate. The sprint closes when the PI Agent's
verdict is "Confirmed" — recorded above, 2026-07-03.*

*The integration PR (`sprint/m19-g2` → `release/m19`) is deferred to G2D exit per the EL
ruling recorded in Section 1. G2C exit does not trigger an integration PR.*
