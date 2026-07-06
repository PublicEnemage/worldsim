---
name: m19-g2b-sprint-exit
type: sprint-exit
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G2 Phase B — SEN + ZMB Calibration Fixtures
status: Confirmed
authored-by: PM Agent
date: 2026-07-02
pi-confirmed: true
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M19, G2 Phase B: SEN + ZMB Calibration Fixtures

**Status:** Confirmed — PI Agent exit conditions satisfied 2026-07-02
**Date produced:** 2026-07-02
**Release branch:** `release/m19`
**Sprint entry document:** `docs/process/sprint-plans/m19-g2b-sprint-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase B/C output).
Changes to this template require PM Agent authorship and EL endorsement.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| Sprint number | 3 (G2 Phase B) |
| Release branch | `release/m19` |
| Sprint groups | G2 Phase B |
| Sprint entry document | `docs/process/sprint-plans/m19-g2b-sprint-entry.md` |
| Exit checklist issue | #1535 |
| Date implementation completed | 2026-07-02 |
| CI status on sprint branch | Green — PRs #1576 and #1577 merged to `sprint/m19-g2` (2026-07-02); all required checks passed for both PRs |

---

## Section 2 — Implementation Status

*All groups must be merged and CI must be green on the sprint branch. This is necessary but
not sufficient for sprint exit. (Authority: sprint-planning-sop.md §Sprint Exit Gate condition 1)*

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| SEN backtesting fixture (#1541) | #1576 | Yes — 2026-07-02 | Green (required checks) | Merged to `sprint/m19-g2`; backtesting check non-required; SEN test PASSED; ZMB test transiently failed (sequencing — see note) |
| ZMB backtesting fixture + focal cohort PHC (#1542) | #1577 | Yes — 2026-07-02 | Green (all checks including backtesting) | Merged to `sprint/m19-g2`; all checks green |

**Implementation status:** Both PRs merged; all required checks green on sprint branch.

**CI sequencing note:** PR #1576 (SEN) showed a transient backtesting failure: the ZMB test shell
(already on `sprint/m19-g2` from PR #1572) ran against the merge commit before `zmb_scenario.py`
was present. `backtesting` is not a required check for sprint branch PRs — auto-merge fired on
required checks only. By the time PR #1577 merged (34 seconds later), `zmb_scenario.py` was on
the sprint branch and the full suite is coherent. The SEN test PASSED on #1576; the ZMB test
PASSED on #1577. No test integrity concern. See pending near-miss assessment below.

**Sprint branch status:** `sprint/m19-g2` is active — G2C and G2D phases remain outstanding.
The integration PR (`sprint/m19-g2` → `release/m19`) is not filed here — it fires at the close
of the final G2 phase per sprint group isolation protocol.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| SEN backtesting fixture (#1541) | Analytics | N/A — Tier 3 infrastructure; does not directly serve Persona 2/3/5 in this sprint | ACCEPT | Issue #1541 comment (2026-07-02) |
| ZMB backtesting fixture (#1542) | Analytics | PASS with condition — Issue #1542 comment (2026-07-02); filed before verdict | ACCEPT | Issue #1542 comment (2026-07-02) |

**Business PO acceptance status:** All ACCEPT. No open rejections.

### Notes on Customer Agent Layer 3 assessments

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| SEN backtesting fixture (#1541) | No — Tier 3 infrastructure (forward trace: G3 Bayesian posterior calibration diversity) | N/A |
| ZMB backtesting fixture (#1542) | Yes — Persona 2 (Aicha, Zambian government analyst; Demo 8 Act 2 primary calibration country) | Yes — Issue #1542 CM and Customer Agent assessment recorded before Business PO verdict (same session, 2026-07-02) |

**Customer Agent condition on ZMB (must propagate to Demo 8 materials):**
Cohort poverty headcount is non-null (SF-3 passed) but reflects a fixed initial seed across all
steps — the DemographicModule is not enabled. Demo 8 Act 2 presenter must use CM-prescribed
framing: "CI intervals grounded in DIRECTION_ONLY fidelity on the ZMB 2014–2019 fiscal channel;
cohort poverty headcount non-null but flat pending DemographicModule integration in G3."
The "+342K cohort effect" narrative is preserved as a model scenario output; it is not presented
as empirically calibrated at G2B.

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

---

## Section 5 — PI Agent Sprint Exit Confirmation

*PI Agent reviews all exit conditions and confirms they are satisfied before the sprint exit
checklist issue is closed. PI Agent does not produce the verdicts — PI Agent confirms they
exist and are complete.*

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on sprint branch (Section 2) — SATISFIED: PRs #1576 and #1577 merged to `sprint/m19-g2` 2026-07-02; all required checks green on both PRs
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable (Section 3) — SATISFIED: ACCEPT on record for both #1541 and #1542 (Issue comments, 2026-07-02)
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed before Business PO verdict (Section 3) — SATISFIED: ZMB Customer Agent assessment filed in same session before BPO verdict; SEN is Tier 3 (N/A)
- [x] No open rejection artifacts (Section 4) — SATISFIED
- [x] Near-miss entry filed for each rejection in this sprint — N/A (no rejections)
- [x] North star test artifact present for user-facing deliverables — SATISFIED: ZMB north star test (PARTIAL PASS) embedded in Section 6 below; SEN is Tier 3 (not required at sprint level)
- [x] CM sign-off on record before fixture PRs merged — SATISFIED: CM sign-offs recorded on Issues #1541 and #1542 (2026-07-02). Note: sign-offs were recorded after PRs were opened (the intent doc requires sign-off "before the feature PR is opened"; PRs opened before CM consultation completed — see pending near-miss assessment in Section 7)

**PI Agent sprint exit verdict:** CONFIRMED — all exit conditions satisfied.

**PI Agent confirmation:**

> All G2B exit conditions are satisfied as of 2026-07-02. Both SEN (#1541) and ZMB (#1542)
> fixture PRs are merged to `sprint/m19-g2` with required checks green. Business PO ACCEPT
> verdicts are on record for both deliverables. Customer Agent Layer 3 assessment for ZMB
> (Persona 2, Aicha) is on record and was filed before the Business PO verdict. No rejection
> artifacts. North star test artifact for ZMB (PARTIAL PASS) is present in Section 6.
>
> One process deviation is noted and referred for near-miss assessment (Section 7): CM sign-off
> was obtained after the feature PRs were opened, not before (as required by the intent document).
> The `backtesting` check is non-required for sprint branch PRs, so auto-merge could have
> fired before CM sign-off was recorded. In practice, both PRs merged within 35 minutes of
> the CM sign-off; the deviation did not compromise fixture integrity. The near-miss entry is
> required to capture the process gap — the intent doc ordering requirement exists precisely
> to prevent this sequence.
>
> The CI sequencing transient failure on #1576 (ZMB test without zmb_scenario.py) is a
> sequencing artifact, not a test integrity issue. Both fixture tests passed on their respective
> PRs. The pattern warrants documenting as a process consideration for G2C onward (Section 7).
>
> — PI Agent (in-session, 2026-07-02)

---

## Section 6 — North Star Test Artifact

*Required per CLAUDE.md §North Star Test (Process Gate) for user-facing capabilities.
Authored by Business PO; embedded here per CLAUDE.md ("part of the exit artifact, not a
separate document"). PI Agent confirms presence and specificity — not authorship.*

### SEN fixture (#1541) — Tier 3 (Infrastructure)

Sprint-level north star test not required. Forward trace: SEN diversifies the calibration
evidence base to Sub-Saharan commodity-shock economies, which is necessary for the ADR-007
Bayesian posterior layer (G3 #1543) to have cross-regional credibility. Downstream capability
that will eventually pass the north star test: a finance ministry analyst can cite backtesting
evidence from their own region, not only from European sovereign debt crises.

### ZMB fixture (#1542) — Tier 1 (User-facing, Demo 8 primary)

**North star test verdict: PARTIAL PASS**

*Scenario:* Aicha (Zambian government analyst) is at the IMF restructuring table. The IMF
team challenges the CI intervals on the WorldSim trajectory: "These bounds are model outputs —
how do we know they aren't just parametric uncertainty with no empirical grounding?" Aicha
opens the sourcing panel: "We ran this same engine against the actual 2014–2019 Zambia copper
crash. It correctly identified the direction and approximate zone of fiscal deterioration across
all six years — the fiscal composite declined from baseline through the copper trough and into
the eurobond period. The trajectory direction is empirically validated."

*What this capability enables:* The ZMB fixture allows Demo 8 to state "direction empirically
validated against ZMB 2014–2019 outturn" rather than "model output with uncertainty
quantification only." This changes the argument from "our model produces these bounds" to "our
model produces these bounds because it achieves documented DIRECTION_ONLY fidelity on this
calibration case." The IMF team cannot dismiss the CI intervals as purely synthetic.

*What remains for G3:* The magnitude claim — "CI intervals calibrated to match historical
variance" — requires the ADR-007 Bayesian posterior layer (#1543). The PARTIAL PASS reflects
that G2B delivers the directional evidence; G3 delivers the magnitude calibration. Demo 8 Act 2
must use CM-prescribed framing throughout.

*PI Agent specificity confirmation:* The north star test names the finance minister scenario
(Aicha, Zambia, IMF restructuring table), the concrete capability (citable directional
backtesting output), and whether the capability changes what the team can argue
(yes — directional claim now defensible; magnitude claim deferred to G3). Test is specific,
not aspirational. Confirmed present.

---

## Section 7 — Near-Miss Referrals

*Process deviations identified during G2B implementation that require PI Agent near-miss
assessment. The PI Agent refers these to the near-miss registry — the PI Agent does not
resolve them.*

### NM referral 1 — CM sign-off obtained after feature PRs were opened

**What happened:** Both G2B feature PRs (#1576 SEN, #1577 ZMB) were opened before the Chief
Methodologist sign-off was recorded on the corresponding issues. The intent document for both
fixtures states "The CM sign-off is recorded as a comment on Issue before the feature PR is
opened" (ZMB intent §5; SEN intent §5). The PRs opened first; the CM consultation and sign-off
followed.

**What was at risk:** Auto-merge was set on both PRs. If the required CI checks had passed before
the CM sign-off was recorded, the fixtures could have merged without any CM review. In practice,
the CM sign-off was recorded while CI was running and both PRs merged within 35 minutes of the
sign-offs. The `backtesting` check failure on #1576 (non-required) slowed nothing. But the
ordering protection failed.

**What caught it:** The EL noticed the ordering deviation and the CM consultation was activated
in-session before CI completed. The system worked because the EL was attentive — not because
the process enforced the ordering.

**Process improvement required:** The pre-merge CM sign-off requirement needs a process
mechanism that enforces ordering, not just documents it. Options: (a) require a manual GitHub
required-status-check or PR label that the implementing agent must set after recording the CM
sign-off; (b) add a PI Agent gate comment obligation before auto-merge is set (similar to the
integration PR gate). The near-miss entry should evaluate these options.

*PI Agent: file NM entry in `docs/process/near-miss-registry.md` before G2C begins.*

### NM referral 2 — Co-dependent fixture sequencing produces transient backtesting failure

**What happened:** PR #1576 (SEN fixture) ran the full `backtesting` test suite, which
includes the ZMB test shell (already on `sprint/m19-g2` from #1572). The ZMB test failed
(`ModuleNotFoundError: No module named 'tests.fixtures.zmb_scenario'`) because `zmb_scenario.py`
was not yet on the sprint branch. `backtesting` is non-required, so auto-merge fired anyway.

**What was at risk:** If `backtesting` were a required check, the SEN PR would have been blocked
indefinitely (circular dependency: SEN needs ZMB to pass; ZMB needs to land first; neither can
land first under required checks). The current design correctly makes `backtesting` non-required
for sprint branch PRs — but this is an implicit assumption, not a documented design decision.

**Process improvement required:** For G2C onward (multiple co-dependent fixture PRs in the same
sprint), the sprint entry should explicitly state the CI ordering expectation and confirm that
`backtesting` is non-required for the sprint sub-branch. Document the pattern.

*PI Agent: file NM entry in `docs/process/near-miss-registry.md` before G2C begins.*

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for Sprint 3 (G2 Phase B) of M19. It supersedes any
informal exit notation in `SESSION_STATE.md` for this sprint. It is filed at
`docs/process/sprint-plans/m19-g2b-sprint-exit.md`.

*The PI Agent confirmation in Section 5 is the gate. The sprint closes when the PI Agent's
verdict is "Confirmed" — recorded above, 2026-07-02.*

*The integration PR (`sprint/m19-g2` → `release/m19`) is deferred to the close of the final
G2 phase (G2C or G2D, whichever is last), per sprint group isolation protocol. G2B exit does
not trigger an integration PR.*
