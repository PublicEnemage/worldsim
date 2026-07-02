---
name: m18-g7-sprint-exit
type: sprint-exit
milestone: M18 — Full Argument and Demo 7
sprint-group: G7 — Demo 7 Continuation
status: In-progress — awaiting PI Agent confirmation
authored-by: PM Agent
date: 2026-07-01
pi-confirmed: false
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M18, G7: Demo 7 Continuation

**Status:** In-progress — awaiting PI Agent confirmation
**Date produced:** 2026-07-01
**Release branch:** `release/m18`
**Sprint entry document:** `docs/process/sprint-plans/m18-g7-sprint-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate`.
G7 was the Demo 7 continuation sprint. It carried all 24 Step 6b findings (DEMO-130 through
DEMO-160) from the G6 internal review, executed root cause analysis, authored intent documents
and QA-first test suites across five fix clusters (A–E), remediated all CRITICAL and HIGH
findings, advanced through Step 6b v3 (PASS) and Step 7 IR review (PASS), addressed all
four IR-required findings, and produced run 13 as the final demo-ready screenshot set.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| Sprint group | G7 — Demo 7 Continuation |
| Release branch | `release/m18` |
| Sprint entry document | `docs/process/sprint-plans/m18-g7-sprint-entry.md` (EL-approved 2026-06-29) |
| Exit checklist issue | #1340 (M18 closure gate — closes when #843 closes) |
| Sprint journal issue | #1475 |
| Date implementation completed | 2026-07-01 |
| CI status on sprint branch | Green — all 21 PRs to `sprint/m18-g7` passed all required checks |

---

## Section 2 — Implementation Status

All implementation groups are merged to `sprint/m18-g7` with CI green.

| PR | Merged | Title | Cluster |
|---|---|---|---|
| #1497 | 2026-06-30 | G7-0 root cause analysis | Process |
| #1498 | 2026-06-30 | G7-0b — ADR-008 Amend 2, ADR-010 Amend 2, NM-083 | Process / ADR |
| #1499 | 2026-06-30 | G7 intent documents — five fix cluster intents (A–E) | Process |
| #1500 | 2026-06-30 | QA-first assertions — AC-A1/A2, AC-B1–B5, AC-C1–C5, AC-D1–D5 (red) | QA |
| #1501 | 2026-06-30 | Cluster E QA-first assertions — AC-E1 through AC-E7 (red) | QA |
| #1502 | 2026-06-30 | Cluster E — capture sequence, narration, and label fixes (AC-E1–E7 green) | E |
| #1503 | 2026-06-30 | M18-G7-A — CI band geometry fix (additive formula, yDomain, opacity) | A |
| #1504 | 2026-06-30 | M18-G7-B — Zone 1B layout: distributional summary first, PSP visible | B |
| #1505 | 2026-06-30 | AC-C1–C5 — CohortImpactSection monitored-row state | C |
| #1506 | 2026-06-30 | M18-G7-D — data pipeline fixes (PSP driver, HCL, ecological) | D |
| #1507 | 2026-06-30 | Hotfix — 4 CI failures on sprint/m18-g7 | Hotfix |
| #1508 | 2026-06-30 | Hotfix 2 — AC-B1/B5/C2/P1 four CI failures | Hotfix |
| #1509 | 2026-07-01 | AC-B5 — trajectory mock unblocks measurement-output useEffect guard | Fix |
| #1510 | 2026-07-01 | Step 6 screenshot recapture — all 5 frames (run 9) | Step 6 |
| #1515 | 2026-07-01 | Step 6b v2 nine-agent internal review — FAIL (2 CRITICAL) | Step 6b v2 |
| #1516 | 2026-07-01 | DEMO-156 Zone 1B focal row + DEMO-157 PSP driver root-cause fixes | D / C |
| #1517 | 2026-07-01 | Scroll Zone 1B cohort-impact before Frame C capture (DEMO-156) | E |
| #1518 | 2026-07-01 | Step 6b v3 nine-agent review — PASS (DEMO-156 + DEMO-157 resolved) | Step 6b v3 |
| #1519 | 2026-07-01 | Step 7 Independent Review — PASS (0 CRITICAL, 2 HIGH, 2 MEDIUM, 1 LOW) | Step 7 |
| #1520 | 2026-07-01 | IR-M18-001 + IR-M18-003 walkthrough edits | Step 7 follow-up |
| #1521 | 2026-07-01 | DEMO-158 — generic choropleth centering DEV seams | Step 7 follow-up |
| #1523 | 2026-07-01 | Remove stale Mode 2 narration + DEMO-160 Screenshot Reference fix | Step 7 follow-up |

**Implementation status:** All 21 PRs merged; CI green on `sprint/m18-g7`.

### Final screenshot evidence (run 13, 2026-07-01)

| Frame | File | MD5 | Bytes |
|---|---|---|---|
| A | `frame-a-the-instrument.png` | `841123e0cb982746d0a2d6f97a4ace5f` | 195,207 |
| B | `frame-b-uncertainty-envelope.png` | `e8ef1edc563283745eaee7648b9df1df` | 195,126 |
| C | `frame-c-act1-finding.png` | `d36a9ff9a0456b5bcc3cf2319b0533a3` | 193,864 |
| D | `frame-d-counter-proposal.png` | `b889e24999920b2a0761b94b9dea8114` | 147,382 |
| E | `frame-e-analytical-defence.png` | `ef5ae6cdd825ae950d169b393deb191d` | 166,275 |

All five MD5 hashes distinct. Frame C ≠ Frame A (DEMO-156 resolved). Frame D choropleth centered on ZMB (DEMO-158 resolved).

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 | BPO verdict | Verdict artifact |
|---|---|---|---|---|
| Demo 7 preparation package — five frames (run 13) + stakeholder walkthrough (IR-revised) | Frontend / Documentation | PASS — `docs/demo/m18/reviews/2026-07-01-v0.18.0-internal-review-v3.md` §Customer Agent Solo-Use | ACCEPT | #1475 (BPO comment, 2026-07-01) |
| Step 7 IR review + finding resolutions (IR-M18-001/002/003) | Documentation / Frontend | N/A — process artifact | ACCEPT | #1475 (BPO comment, 2026-07-01) |
| Step 8 — DEMO-NNN triage complete + stakeholder review placeholder filed | Documentation | N/A — process artifact | ACCEPT | `docs/demo/m18/reviews/PENDING-v0.18.0-stakeholder-review.md` |

**Business PO acceptance status:** All ACCEPT. No open rejections.

### Customer Agent Layer 3 — detail

The Step 6b v3 Customer Agent Solo-Use assessment (in `2026-07-01-v0.18.0-internal-review-v3.md`) constitutes the G7 Layer 3 record:

| Persona | Act | Verdict |
|---|---|---|
| Persona 1 (Lucas, Analytical Economist) | Act 2 — Zone 3 auditability walk | PASS |
| Persona 2 (Aicha, Finance Minister) | Act 1 — CLEAR badge cohort finding | PASS |
| Persona 3 (Andreas, Political Advisor) | Act 1 — PSP driver read | PASS |
| Persona 5 (Aicha, Finance Minister at table) | North star — deferred pending live session #843 | DEFERRED (EL exception) |

---

## Section 4 — Open Rejections

No open rejections. Step 6b v3 returned PASS (9/9 agents). Step 7 IR returned PASS (0 CRITICAL). All four IR-required findings (IR-M18-001/002/003 and DEMO-158) were resolved before G7 exit.

The two accepted IR findings (IR-M18-004 Zone 1B focal row not in Frame A; IR-M18-005 T3 placeholder in Zone 3) were accepted by the IR Agent as design-correct — not rejections.

---

## Section 5 — North Star Test

**Status: DEFERRED — EL exception on record.**

**Authority:** G7 sprint entry §7 (EL-approved 2026-06-29) and G6 exit PI Agent confirmation (#1475, 2026-06-29): "The north star test will be authored at G7 exit after the live session confirms the argument is deliverable as scripted." Inherent necessity — the demo cannot have run at the time the exit document is filed.

**Pre-assessment (BPO, to confirm deferral is not a scope gap):**

*Finance minister scenario:* Aicha (ZMB Finance Minister equivalent), IMF debt restructuring session with three programme proposals on the table. Ministry team has the instrument cluster running on a laptop visible to both sides.

*Act 1 capability evaluated:* The analyst configures FiscalMultiplier at 0.85 in Zone 2 Form 1, presses Apply, and the counter-trajectory branch appears in Zone 1A simultaneously with the baseline. At step 8, Zone 1B reads: "bottom quintile informal workers poverty headcount — 0.450 / floor 0.400 — CLEAR." The ministry team can say: "At your multiplier assumption, the threshold crossing happens. At 0.85 — fifteen percent below the programme baseline and consistent with the Ilzetzki et al. consensus for a constrained open economy — it does not." That is a technical finding, not a political objection.

*Act 2 capability evaluated:* Zone 1B sticky-bottom reads "+342,727 persons below poverty threshold · 298K–398K · T3 · Direction stable." The methodology panel expands in Zone 3 without navigation. The IMF team must engage analytically with the differential — they cannot dismiss it as a model assertion without engaging with the derivation now visible in the same viewport.

*Does this change what the ministry team can argue at the table?* **Yes.** The counter-proposal is no longer a narrative position — it is a quantified differential with a confidence interval, a tier disclosure, and direction stability on record. The IMF team must refute the number or accept it.

**North star pre-assessment verdict: PASSES.** Formal artifact to be filed by Business PO after live session #843 runs and confirms the argument is deliverable as scripted. PI Agent blocks M18 exit gate (#1340) until the formal artifact is filed.

---

## Section 6 — Sprint Exit Artifact Statement

This document is the sprint exit artifact for G7 of M18. It supersedes any informal exit
notation in SESSION_STATE.md for G7. It is filed at
`docs/process/sprint-plans/m18-g7-sprint-exit.md`.

The PI Agent confirmation in Section 7 is the gate. G7 closes when the PI Agent's verdict
is "Confirmed."

---

## Section 7 — PI Agent Sprint Exit Confirmation

*To be completed by PI Agent.*

**Exit conditions checklist (PI Agent):**

- [ ] All implementation groups merged; CI green on `sprint/m18-g7` (Section 2)
- [ ] Business PO ACCEPT verdict filed for each user-facing deliverable (Section 3)
- [ ] Customer Agent Layer 3 on record for Personas 1, 2, 3 (Section 3); Persona 5 north star deferred with EL exception (Section 5)
- [ ] No open rejection artifacts (Section 4)
- [ ] North star deferral EL exception confirmed and pre-assessment on record (Section 5)
- [ ] Integration PR `sprint/m18-g7` → `release/m18` opened and set to auto-merge

**PI Agent sprint exit verdict:** _Pending_

_PM Agent, 2026-07-01. Sprint journal: #1475. Entry doc: `m18-g7-sprint-entry.md`._
