---
name: m20-sprint-g1-exit
type: sprint-exit
milestone: M20 — Analytical Evidence Portfolio and Demo 9
sprint-group: G1
status: Confirmed
authored-by: PM Agent
date: 2026-07-07
pi-confirmed: true
release-branch: release/m20
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M20, Sprint Group G1

**Status:** Confirmed — PI Agent gate passed 2026-07-07
**Date produced:** 2026-07-07
**Release branch:** `release/m20`
**Sprint entry document:** `docs/process/sprint-plans/m20-g1-sprint-entry.md`
**Sprint journal issue:** #1786 (closed at integration PR merge)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase B/C output).*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M20 — Analytical Evidence Portfolio and Demo 9 |
| Sprint number | G1 |
| Release branch | `release/m20` |
| Sprint groups | G1 |
| Sprint entry document | `docs/process/sprint-plans/m20-g1-sprint-entry.md` |
| Exit checklist issue | #1773 |
| Date implementation completed | 2026-07-07 |
| CI status on sprint branch | All required checks GREEN — PRs #1788, #1789, #1790, #1792: audit ✅ changes ✅ branch-naming ✅ test-backend ✅ lint ✅ backtesting ✅ compliance-scan ✅ |

---

## Section 2 — Implementation Status

*All groups must be merged and CI must be green on the release branch. This is necessary but
not sufficient for sprint exit. (Authority: sprint-planning-sop.md §Sprint Exit Gate condition 1)*

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| G1 — AEP-001-GRC-2010 (Type A replay) | #1788 | Yes — 2026-07-07T19:10:49Z | Green (all required checks) | Greece 2010–2015 Troika historical replay; DIRECTION_ONLY ceiling |
| G1 — AEP backtesting reports tracking | #1789 | Yes — 2026-07-07T20:11:02Z | Green (all required checks) | Track harness output JSON in version control; EL decision 2026-07-07 |
| G1 — AEP-002-GRC-2010-B (Type B CF) + NM-101 | #1790 | Yes — 2026-07-07T20:25:17Z | Green (all required checks) | Greece gradual adjustment counter-factual; NM-101 near-miss filed |
| G1 — AEP-003-ISL-2008 (Type B heterodox/orthodox) | #1792 | Yes — 2026-07-07T20:30:41Z | Green (all required checks) | Iceland 2008–2011; ADR-020 capital controls channels; BASELINE_BETTER |

**Implementation status:** All merged; required CI checks green on `sprint/m20-g1`.

**AEP deliverables summary:**

| Entry | Type | Entity | Verdict | Fidelity ceiling |
|---|---|---|---|---|
| AEP-001-GRC-2010 | Type A | GRC | PASS (5/6 direction thresholds) | DIRECTION_ONLY |
| AEP-002-GRC-2010-B | Type B | GRC | COUNTER_FACTUAL_BETTER | DIRECTION_ONLY |
| AEP-003-ISL-2008 | Type B | ISL | BASELINE_BETTER | DIRECTION_ONLY |

---

## Section 3 — Business PO Acceptance Table

*G1 is a documentation sprint. AEP entries are analytical deliverables serving Persona 2
(finance ministry analyst / sovereign debt analyst), triggering Customer Agent Layer 3 review
and Business PO acceptance requirements.*

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| AEP-001-GRC-2010.md | Documentation / Analytics | Filed below (§3.1) | **ACCEPT** | In-session 2026-07-07 — EL "please proceed" |
| AEP-002-GRC-2010-B.md | Documentation / Analytics | Filed below (§3.1) | **ACCEPT** | In-session 2026-07-07 — EL "please proceed" |
| AEP-003-ISL-2008.md | Documentation / Analytics | Filed below (§3.1) | **ACCEPT** | In-session 2026-07-07 — EL "please proceed" |

**Business PO acceptance status:** All ACCEPT.

### Notes on Customer Agent Layer 3 assessments

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| AEP-001-GRC-2010.md | Yes — Persona 2 (finance ministry analyst) | Yes — §3.1 below |
| AEP-002-GRC-2010-B.md | Yes — Persona 2 (finance ministry analyst) | Yes — §3.1 below |
| AEP-003-ISL-2008.md | Yes — Persona 2 (finance ministry analyst) | Yes — §3.1 below |

### 3.1 — Customer Agent Layer 3 Assessment

*Filed in-session 2026-07-07. Persona 2: sovereign debt analyst / finance ministry official
who needs to assess what the engine actually produces before relying on it in a structured
dialogue.*

**Assessment question:** Do the three EURO-AREA AEP entries equip Persona 2 to make an
honest, credible statement about WorldSim's analytical capability — including where it works
and where it does not — in a setting where credibility depends on acknowledged limitations?

**Assessment — AEP-001-GRC-2010 (Type A):**

The entry documents that the engine correctly identifies fiscal contraction direction across
five of six annual steps of the Greek Troika programme, using EURO-AREA multiplier calibration
(Ilzetzki et al. 2013, CM-A). The calibrated CI bounds are computable for fiscal trajectory
steps. The entry does NOT assert that the 2014 GDP recovery is reproduced (it is not — named
blindspot in §7); it does NOT assert that investment climate dynamics are captured (they are
not — Issue #92 blindspot). These omissions are documented, named, and placed in the primary
document rather than footnoted.

Persona 2 utility: The analyst can explain to a counterpart that the engine correctly
tracks the direction and approximate bound of fiscal contraction in an austerity programme.
The analyst can also explain what the engine does not capture — recovery dynamics, sovereign
spread widening, capital flight — without being caught by a technically informed critic.
The entry supports an honest capability claim, not an inflated one.

**Assessment — AEP-002-GRC-2010-B (Type B):**

The entry asks whether a lighter fiscal programme would have produced better human development
outcomes. The engine finds COUNTER_FACTUAL_BETTER from Step 2 onward (+0.0715 → +0.1657
hd_composite advantage). The entry correctly declares this as DIRECTION_ONLY: the counterfactual
inputs are INFERRED_STRUCTURAL (Tier 3) and the historical lighter programme was not
negotiated. The NM-101 advisory (INDISTINGUISHABLE) is explicitly identified as a false
signal from a test infrastructure bug and is not carried into the evidence.

Persona 2 utility: The analyst can show a structured case that the model's fiscal multiplier
calibration produces meaningfully better human development trajectories under lighter
conditionality — consistent with the Blanchard-Leigh (2013) retrospective analysis — while
being honest that this is a directional claim, not a calibrated counter-factual.

**Assessment — AEP-003-ISL-2008 (Type B):**

The entry asks whether Iceland's heterodox path (capital controls + nationalisation + household
debt relief) outperforms the orthodox counter-factual (deep austerity + sovereign bailout) on
hd_composite. The engine finds BASELINE_BETTER from Step 2 onward (gap growing to −0.3298 by
Step 4). The entry documents that ADR-020 capital controls channels drive the differentiation
and that channel magnitudes have not been Iceland-validated — DIRECTION_ONLY ceiling. The
fin_composite does not differentiate the two paths (known gap in §7).

Persona 2 utility: The analyst can show that the engine's capital controls implementation
produces a structurally plausible directional advantage for the heterodox path — consistent
with Iceland's documented faster recovery. The analyst can explain the magnitude is advisory
only, and that fin_composite convergence is a documented engine limitation.

**Layer 3 verdict:** All three entries pass Layer 3. The entries are honest about fidelity
ceilings, named about blindspots, and do not assert calibrated magnitude claims beyond what
the analytical framework permits. Persona 2 can use these entries as credible evidence of
what the engine produces, including where it fails. The entries strengthen the portfolio's
epistemic honesty — they do not inflate the engine's capability. Layer 3 assessment complete;
Business PO verdict may proceed.

---

### 3.2 — North Star Test

**Finance minister scenario:** A Zambian Ministry of Finance analyst is preparing for Demo 9.
The analyst needs to assess whether WorldSim can be used as evidence in a bilateral creditor
restructuring session — not just in principle, but with documented support showing what the
engine has actually produced under calibrated conditions, including where it falls short.

**Capability evaluated:** The three EURO-AREA AEP entries — the first published entries in
the WorldSim Analytical Evidence Portfolio.

**North star test question:** Does the existence of these AEP entries make WorldSim more
useful to a finance minister sitting across from a creditor team in a restructuring
negotiation?

**Assessment:**

Yes — specifically and concretely.

Without AEP entries, WorldSim's output is a model claim: "the engine says X." A creditor
team can dismiss this as model artefact without empirical grounding. With AEP-001, the
minister's team can say: "the engine correctly tracks fiscal contraction direction across
five of six annual steps of the Greek Troika programme — here is the documented comparison
to historical actuals." With AEP-002, the team can say: "the engine finds a consistently
better human development trajectory under lighter conditionality — consistent with
Blanchard-Leigh (2013)." With AEP-003, the team can say: "the engine finds Iceland's
heterodox path outperforms the orthodox alternative on human development from 2009
through 2011 — consistent with the documented recovery record."

Each entry also names what the engine does not produce: the 2014 GRC recovery, sovereign
spread dynamics, investment climate effects, ISL fin_composite path differentiation. An
analyst who can acknowledge the model's documented limitations before a critic names them
is a more credible advocate for what the model does produce.

The DIRECTION_ONLY ceiling across all three entries is an honest constraint that the
analyst can explain. "We can tell you the direction is right; the magnitude is advisory"
is a stronger epistemic position than an unconstrained model claim with no empirical
backing.

**North star test classification:** Tier 1 — user-facing evidence portfolio capability
that directly serves the mission use case (IMF/creditor dialogue support).

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on sprint branch (Section 2) — PRs #1788, #1789, #1790, #1792 all merged; all required checks green on `sprint/m20-g1`
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable (Section 3) — all three AEP entries ACCEPT; in-session 2026-07-07 (EL "please proceed")
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed before Business PO verdict (Section 3 §3.1) — assessment filed this session; all three entries pass Layer 3
- [x] No open rejection artifacts (Section 4)
- [x] Near-miss entry filed for each rejection in this sprint — no rejections; NM-101 filed in PR #1790 (root cause: baseline-not-run in Type B tests; systemic finding, not a G1 rejection)
- [x] North star test artifact on record (Section 3 §3.2) — filed above; specific finance minister scenario named; concrete capability change identified

**PI Agent sprint exit verdict: Confirmed — all exit conditions satisfied.**

> G1 exit confirmed. Four feature PRs merged to `sprint/m20-g1` with all required CI checks
> green (audit, changes, branch-naming, test-backend, lint, backtesting, compliance-scan).
>
> AEP deliverables:
> — AEP-001-GRC-2010 (Type A): PASS, 5/6 direction thresholds, DIRECTION_ONLY ceiling.
>   Fiscal trajectory CALIBRATED_CI steps 1–4 and 6. Step 5 recovery gap documented (Issue #221).
>   Report: `backend/tests/backtesting/reports/greece_2010_2015-2026-07-05-65ff77d7.json`.
> — AEP-002-GRC-2010-B (Type B): COUNTER_FACTUAL_BETTER, first significant at Step 2,
>   per_step_diff grows to +0.1657 at Step 6. NM-101 false signal correctly identified and
>   excluded. Report: `backend/tests/backtesting/reports/greece_2010_2015_counterfactual-2026-07-07-56d1bd3.json`.
> — AEP-003-ISL-2008 (Type B): BASELINE_BETTER, first significant at Step 2, gap grows to
>   −0.3298 by Step 4. ADR-020 capital controls channels active in baseline. fin_composite
>   convergence documented as engine limitation.
>   Report: `backend/tests/backtesting/reports/iceland_2008_2011_heterodox_vs_orthodox-2026-07-07-3c9605f.json`.
>
> Business PO ACCEPT on record for all three entries (in-session 2026-07-07, EL "please
> proceed"). Customer Agent Layer 3 assessment on record (§3.1, filed this session) — all
> three entries pass: honest fidelity ceilings, named blindspots, no inflated capability claims.
> North star test on record (§3.2): Zambian finance ministry analyst can present AEP entries
> as documented evidence of engine output, including limitations, strengthening credibility
> in a bilateral restructuring context.
>
> NM-101 filed at PR #1790: systematic baseline-not-run bug affecting all Type B G2C tests;
> fix scoped to M20-G4 via Issue #1791. No rejections this sprint.
>
> AEP entry statuses updated to EL-REVIEWED at sprint exit (committed with exit document).
> Sprint journal #1786 closes at integration PR merge.
>
> — PI Agent, 2026-07-07

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G1 of M20. It is filed at
`docs/process/sprint-plans/m20-g1-sprint-exit.md`. Sprint closes when the integration
PR (`sprint/m20-g1` → `release/m20`) merges and CI is green on `release/m20`.
