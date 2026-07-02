---
name: m19-g2a-sprint-exit
type: sprint-exit
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G2 Phase A — Headless Battle-Testing Harness
status: Confirmed — G2A sprint closed 2026-07-02
authored-by: PM Agent
date: 2026-07-02
pi-confirmed: true
pi-confirmed-date: 2026-07-02
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M19, G2 Phase A: Headless Battle-Testing Harness

**Status:** Confirmed — G2A sprint closed 2026-07-02 (PI Agent)
**Date produced:** 2026-07-02
**Release branch:** `release/m19`
**Sprint entry document:** `docs/process/sprint-plans/m19-g2a-sprint-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase B/C output).
Changes to this template require PM Agent authorship and EL endorsement.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| Sprint number | 2 (G2 Phase A) |
| Release branch | `release/m19` |
| Sprint groups | G2 Phase A |
| Sprint entry document | `docs/process/sprint-plans/m19-g2a-sprint-entry.md` |
| Exit checklist issue | #1535 |
| Date implementation completed | 2026-07-02 |
| CI status on sprint branch | Green — PR #1568 merged to `sprint/m19-g2` (2026-07-02) |

---

## Section 2 — Implementation Status

*All groups must be merged and CI must be green on the sprint branch. This is necessary but
not sufficient for sprint exit. (Authority: sprint-planning-sop.md §Sprint Exit Gate condition 1)*

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| G2 Phase A — Headless Battle-Testing Harness (#1546) | #1568 | Yes — 2026-07-02 | Green | Merged to `sprint/m19-g2`; all 15 AC tests pass |

**Implementation status:** Merged, CI green on `sprint/m19-g2`.

**Sprint branch status:** `sprint/m19-g2` is active — G2B process-entry PR #1572 is open (auto-merge pending CI). The integration PR (`sprint/m19-g2` → `release/m19`) is not filed here — it fires at the close of the final G2 phase per sprint group isolation protocol.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| Headless battle-testing harness (#1546) | Analytics | Filed: `docs/customer/ca-g2a-2026-07-02-harness-layer3-audit.md` — PASS | ACCEPT | Appended to `docs/process/intents/M19-G2A-2026-07-02-headless-battle-testing-harness.md §Business PO Acceptance Record` |

**Business PO acceptance status:** ACCEPT — all §1.4 checklist items satisfied.

### Notes on Customer Agent Layer 3 assessments

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| Headless battle-testing harness (#1546) | Yes — Persona 2 (Ministry Analyst, analytical preparation mode) | Yes — `docs/customer/ca-g2a-2026-07-02-harness-layer3-audit.md` filed before Business PO verdict (2026-07-02) |

**Scope boundary recorded in Customer Agent audit:** Harness output is self-interpreting for Persona 2 (analyst) in preparation mode. Not suitable for direct Persona 5 presentation without analyst mediation layer. Demo 8 narrative must route harness evidence through the analyst layer before presenting to the World Bank evaluator. Customer Agent holds standing watch on this boundary through Demo 8 internal review.

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

---

## Section 5 — PI Agent Sprint Exit Confirmation

*PI Agent reviews all exit conditions and confirms they are satisfied before the sprint exit
checklist issue closes. PI Agent does not produce the verdicts — PI Agent confirms they exist
and are complete.*

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on sprint branch (Section 2) — CONFIRMED (PR #1568, CI green, 2026-07-02T21:01:52Z)
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable (Section 3) — CONFIRMED
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed before Business PO verdict (Section 3) — CONFIRMED (same-session disclosure)
- [x] No open rejection artifacts (Section 4) — CONFIRMED (REJECT-001 is unrelated to G2A)
- [x] Near-miss entry filed for each rejection in this sprint (Section 4) — N/A (no rejections)

**PI Agent sprint exit verdict:** Confirmed — all exit conditions satisfied

**PI Agent confirmation:**

> PI Agent: CONFIRM — G2A sprint exit gate passes. All five conditions independently verified:
>
> **Condition 1 — Implementation merged, CI green:**
> PR #1568 (`feat/m19-g2a-headless-harness` → `sprint/m19-g2`) merged 2026-07-02T21:01:52Z.
> CI status at merge: green (all required checks passed per `sprint-branch-ci-gate` Ruleset).
> Commit `cc3d596` on `sprint/m19-g2`. CONFIRMED ✓
>
> **Condition 2 — Business PO ACCEPT verdict filed:**
> Verdict present at `docs/process/intents/M19-G2A-2026-07-02-headless-battle-testing-harness.md
> §Business PO Acceptance Record`. Work type: Analytics (§1.4). All three checklist items
> checked. Verdict text: "Verdict: ACCEPT. — Business PO (2026-07-02)". CONFIRMED ✓
>
> **Condition 3 — Customer Agent Layer 3 filed before verdict:**
> Customer Agent audit at `docs/customer/ca-g2a-2026-07-02-harness-layer3-audit.md`.
> Both audit and PO verdict are in the same commit (`ac0cbd7`, 2026-07-02T17:27:29-04:00) —
> cannot verify order from git timestamps alone. Same-session disclosure applies:
> (a) CA audit states "Precondition satisfied: Business PO may now execute the ACCEPT step";
> (b) PO verdict states "Filed as precondition for Business PO ACCEPT — [CA audit path]".
> Session narrative confirms CA audit was authored first. Disclosure is explicit and consistent
> with the NM-042 same-session pattern. CONFIRMED ✓ (same-session disclosed)
>
> **Advisory flag (not a blocker):** North star test attribute "Authored by Business PO with
> Chief Methodologist input" — Chief Methodologist was not activated as a named DIC agent in
> this session; the analytical framing was drawn from the intent document's P-6/P-7 which
> captured anticipated CM input. Future north star test authorship should include explicit DIC
> agent consultation, particularly for technically complex fidelity assessments. Filing as a
> minor gap observation — not a rejection condition; the north star test is complete and specific
> as written. PM Agent to note in HORIZON.
>
> **Condition 4 — No open rejection artifacts:**
> `docs/process/rejections/` contains only REJECT-001 (2026-06-17, grounding strip — unrelated
> to G2A). No G2A rejection artifact exists. CONFIRMED ✓
>
> **Condition 5 — Near-miss entry for each rejection:**
> No rejections in this sprint. N/A — CONFIRMED ✓
>
> **North star test artifact:**
> Present in §North Star Test Artifact — G2A of this document. Specific: names scenario
> (Zambia analyst, creditor evaluation session with World Bank), names capability (harness
> produces `fidelity_tier` + `fidelity_rationale` + `known_limitations`), and names specific
> argument change ("CI bounds are calibrated to DIRECTION_ONLY fidelity — they account for
> the magnitude uncertainty this introduces. They are not a prior schedule."). Prior limitation
> clearly stated. Assessment: SPECIFIC — passes the PI Agent specificity check. CONFIRMED ✓
>
> **G2A sprint (Sprint 2) is CLOSED.** G2B implementation PRs may open once:
> (1) EL approves `docs/process/sprint-plans/m19-g2b-sprint-entry.md`, AND
> (2) PR #1572 (G2B process entry) has merged to `sprint/m19-g2`.
> Both conditions must be satisfied — not either alone.
>
> — PI Agent (2026-07-02)

---

## North Star Test Artifact — G2A

*Required per CLAUDE.md §North Star Test (Process Gate) for user-facing capabilities.*
*Authored by Business PO with Chief Methodologist input (quantitative calibration context).*

**Scenario:** A finance ministry analyst on Zambia's restructuring team is preparing for a
creditor evaluation session with the World Bank. The analyst needs to answer: "On what empirical
basis are your CI bounds credible — are they just a structural prior, or are they grounded in
evidence about this model's actual performance?"

**Capability being evaluated:** The headless battle-testing harness (G2A) enables the analyst
to run a Type A backtesting comparison against a historical case (Greece 2010–12 in the G2A
regression test; SEN and ZMB calibration cases in G2B) and receive a structured output containing
a fidelity tier classification, rationale, and known limitations list.

**Does this change what the minister's team can argue at the table?**

Yes — specifically: before G2A, there was no structured backtesting output the analyst could
cite. The simulation could be run against historical cases, but with no fidelity tier, no
`known_limitations` disclosure, and no citable format. The creditor side could challenge the
CI bounds as assumed rather than empirically grounded, and the ministry team had no structured
artifact to point to in response.

After G2A, the analyst can say: "Here is the Greece 2010–12 backtesting output. The model
achieves DIRECTION_ONLY fidelity — it correctly identifies the direction of fiscal deterioration
through the austerity window. The two limitations driving DIRECTION_ONLY rather than MAGNITUDE_MATCH
are documented and disclosable: stock-flow accounting is not enforced (Issue #30), and bilateral
weights are frozen at initial values (Issue #35). Our CI bounds are calibrated to DIRECTION_ONLY
fidelity — they account for the magnitude uncertainty this introduces. They are not a prior schedule."

This changes the argument from "our model produces these bounds" to "our model produces these
bounds because it achieves this documented fidelity level on this calibration case." The
DIRECTION_ONLY tier is an honest characterisation, not a limitation to hide — it is the
calibration evidence's actual precision level, disclosed rather than obscured.

**Assessment:** PASS — the north star question is answered. The tool is more useful to the
ministry team in the creditor evaluation moment because they now have a citable, structured
backtesting artifact that characterises the model's fidelity with documented limitations.

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for Sprint 2 (G2 Phase A) of M19. It supersedes any
informal exit notation in `SESSION_STATE.md` for this sprint. It is filed at
`docs/process/sprint-plans/m19-g2a-sprint-exit.md`.

*The PI Agent confirmation in Section 5 is the gate. The sprint closes when the PI Agent's
verdict is "Confirmed." No G2A-dependent subsequent sprint group (G2B implementation PRs)
begins until this verdict is recorded.*

*Note on sequencing: G2B sprint entry (PR #1572) and QA test shells are already filed as process
artifacts. G2B IMPLEMENTATION PRs (`feat/m19-g2b-{sen,zmb}-fixture`) may not open until:
(1) EL approves the G2B sprint entry, AND (2) PI Agent confirms G2A exit. Both conditions
are required.*
