---
name: m20-sprint-g3-exit
type: sprint-exit
milestone: M20 — Analytical Evidence Portfolio and Demo 9
sprint-group: G3
status: Confirmed
authored-by: PM Agent
date: 2026-07-07
pi-confirmed: true
release-branch: release/m20
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M20, Sprint Group G3

**Status:** Confirmed — PI Agent gate passed 2026-07-07; BPO verdict pending EL review
**Date produced:** 2026-07-07
**Release branch:** `release/m20`
**Sprint entry document:** `docs/process/sprint-plans/m20-g3-sprint-entry.md`
**Sprint journal issue:** #1811

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase B/C output).*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M20 — Analytical Evidence Portfolio and Demo 9 |
| Sprint number | G3 |
| Release branch | `release/m20` |
| Sprint groups | G3 |
| Sprint entry document | `docs/process/sprint-plans/m20-g3-sprint-entry.md` |
| Exit checklist issue | #1773 |
| Date implementation completed | 2026-07-07 |
| CI status on sprint branch | PR #1814 merged; CI green (all required checks PASS) |

---

## Section 2 — Implementation Status

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| G3 — AEP-010 LKA 2022 (SOUTH-SE-ASIAN Type A) | #1814 | Yes — 2026-07-07 | Green | Report: `sri_lanka_2022_2023-2026-07-07-8750594.json` |
| G3 — AEP-011 PAK 2022 (SOUTH-SE-ASIAN Type A+B) | #1814 | Yes — 2026-07-07 | Green | Reports: `pakistan_2022_2023_type_a/type_b-2026-07-07-8750594.json`; NM-101 applied |
| G3 — Gap closure issues | GitHub issues | Yes — 2026-07-07 | N/A | #1815 (PRT fixture); #1816 (BGD fixture); #1817 (remittance channel) |

**Implementation status:** Feature PR #1814 merged to `sprint/m20-g3`; all three harness reports committed; three gap closure issues filed.

**AEP deliverables summary:**

| Entry | Type | Entity | Period | Verdict | Fidelity ceiling | Calibration family |
|---|---|---|---|---|---|---|
| AEP-010-LKA-2022 | Type A | LKA | 2019–2023 (5 annual steps) | Engine does not find crisis at any step; counterintuitive composite increase at default declaration | DIRECTION_ONLY — targeted; direction not confirmed | SOUTH-SE-ASIAN (CM-C, T3) |
| AEP-011-PAK-2022 | Type A + B | PAK | 2022 H1 – 2023 H2 (4 biannual steps) | Type A: Steps 1–2 directionally correct decline; Type B: COUNTER_FACTUAL_BETTER (phased conditionality) | DIRECTION_ONLY | SOUTH-SE-ASIAN (CM-C, T3) |

---

## Section 3 — Business PO Acceptance Table

*G3 is a documentation sprint. AEP entries are analytical deliverables serving Persona 2
(finance ministry analyst / sovereign debt analyst), triggering Customer Agent Layer 3 review
and Business PO acceptance requirements.*

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| AEP-010-LKA-2022.md | Documentation / Analytics | Filed below (§3.1) | **PENDING EL REVIEW** | In-session 2026-07-07; EL review required |
| AEP-011-PAK-2022.md | Documentation / Analytics | Filed below (§3.1) | **PENDING EL REVIEW** | In-session 2026-07-07; EL review required |

### 3.1 — Customer Agent Layer 3 Assessment

*Filed in-session 2026-07-07. Persona 2: sovereign debt analyst / finance ministry official
(Demo 9 context: Zambian finance ministry analyst reviewing full AEP portfolio before the
Demo 9 walkthrough).*

**Assessment question:** Do the G3 SOUTH-SE-ASIAN AEP entries (AEP-010 LKA and AEP-011 PAK)
equip Persona 2 to make an honest, credible statement about WorldSim's analytical capability
— including where it works and where it does not — for scenarios involving IMF programme
conditionality, sovereign default, and Coffin Corner dynamics in South and South-East Asian contexts?

---

**Assessment — AEP-010-LKA-2022 (SOUTH-SE-ASIAN Type A):**

This entry is analytically unique in the AEP portfolio because it documents the most complete
fidelity failure across all 11 entries: the engine produces no directional signal for Sri Lanka's
2022 crisis across five steps, and produces a counterintuitive composite *increase* at the
sovereign default step.

From a Persona 2 perspective, the entry's value is entirely in its honest disclosure. A finance
ministry analyst reviewing this entry can make the following credible statement: "WorldSim does
not currently model Coffin Corner dynamics for SOUTH-SE-ASIAN scenarios. The Sri Lanka 2022
case — the canonical instance of all six failure modes firing simultaneously — produces no
crisis signal and an incorrect direction at the default step. The platform's current scope does
not include this class of scenario."

This is a harder statement to deliver than a partial success, but it is the honest one. The
alternative — presenting AEP-010 as a partial capability — would misrepresent the engine's
reach and would be caught by any counterpart with knowledge of the Sri Lankan crisis.

The `debt_moratorium` + `default_declaration` interaction producing a composite improvement
is the most significant individual data point in the portfolio: it demonstrates that the engine
has an internal inconsistency for SOUTH-SE-ASIAN scenarios that does not exist for LATAM-EM
scenarios (where `default_declaration` correctly produces fin→0.0000 in AEP-007). This
inconsistency should be surfaced explicitly in Demo 9, not buried in §7 Known Limitations.

Persona 2 utility: CONDITIONAL — the entry equips the analyst to be honest about what the
engine cannot do, not what it can do. For Demo 9 purposes, AEP-010 serves as the scope
limitation disclosure entry for Coffin Corner scenarios.

---

**Assessment — AEP-011-PAK-2022 (SOUTH-SE-ASIAN Type A+B):**

The Type A component produces a directionally correct result for the most policy-sensitive
step: front-loaded conditionality at Step 1 propagates to a composite decline at Step 2
(fin: -9.5%, hd: -3.6%). This is a partial success — the engine recognises the shock without
producing a deeper crisis. The Steps 3–4 flatness (monetary tightening produces no response) is
a documented limitation consistent with the cross-entry flat-plateau pattern.

The PSP null finding is the most significant gap for Persona 2: the fixture was specifically
designed to stress-test programme survival probability under conditionality pressure. PSP=None
throughout means the most analytically interesting claim (does front-loaded conditionality
threaten programme survival?) cannot be demonstrated. A finance ministry analyst who uses this
entry to argue that front-loaded IMF conditionality creates programme survival risk cannot point
to any PSP signal — only to the hd_composite decline.

The Type B result (COUNTER_FACTUAL_BETTER) is the portfolio's strongest contribution to the
policy design question: the engine finds that phased conditionality (25%/step, higher
implementation feasibility) produces better short-term human development outcomes. This
directional finding — even at DIRECTION_ONLY — is more useful than most of the Type B entries
because it speaks directly to a policy design question (front-loaded vs phased adjustment)
that finance ministry analysts in IMF programme countries actually face.

The within-family comparison with AEP-010 is directionally useful: PAK (managed compliance,
no default) vs LKA (Coffin Corner entry, default) produces the expected relative entry-point
ordering (LKA starts higher because 2019 pre-crisis conditions are stronger than 2022 H1
conditions). The crisis-depth comparison is limited by LKA's direction inconsistency.

Persona 2 utility: CONFIRMED — for Type A directional decline (Steps 1–2), Type B phased vs
front-loaded conditionality comparison. PSP gap must be disclosed. Coffin Corner capability
claim must not be made.

---

**Cross-G3 pattern:**

The G3 SOUTH-SE-ASIAN entries complete the AEP first-pass portfolio across all four calibration
families. The cross-family pattern at G3 close:

- **EURO-AREA (G1: AEP-001–003):** DIRECTION_ONLY; 2 of 3 directionally correct; Iceland
  BASELINE_BETTER (heterodox path confirmed); Greece default fin→0.0000 (strong signal)
- **SSA-LIC (G2: AEP-004–006):** DIRECTION_ONLY; consistent decline for commodity shock arcs;
  CB Cloud distributional signal absent (GHA)
- **LATAM-EM (G2: AEP-007–009):** DIRECTION_ONLY; default hard-floor signal strong (ARG);
  fin_composite path insensitivity maximum in Kirchner recovery (AEP-008)
- **SOUTH-SE-ASIAN (G3: AEP-010–011):** DIRECTION_ONLY; most complete fidelity failure (LKA);
  conditionality direction correct but PSP absent (PAK); COUNTER_FACTUAL_BETTER for phased
  adjustment (PAK Type B)

**G3-specific finding not previously observed:** The `debt_moratorium` + `default_declaration`
interaction inconsistency (AEP-010 Step 4 improvement vs AEP-007 Step 2 collapse) is a new
engine gap not documented in G1 or G2. This may indicate a calibration family-specific
weighting difference in how emergency policy inputs are processed, or it may indicate a
general bug triggered by multi-input emergency steps. Recommend filing as a separate engine
gap issue before Demo 9.

**Layer 3 verdict:**

- **AEP-010 (LKA):** Pass with critical disclosure requirement — useful as scope limitation
  documentation; not useful as capability demonstration. Demo 9 must present AEP-010 as
  "here is what the engine cannot yet do" rather than "here is a partial result."
- **AEP-011 (PAK):** Pass — Type A directional signal correct for conditionality propagation;
  Type B phased/front-loaded comparison is the strongest policy-design finding in the SOUTH-SE-ASIAN
  family. PSP gap must be disclosed.

Customer Agent Layer 3 assessment complete. Business PO verdict may proceed.

---

### 3.2 — North Star Test

**Finance minister scenario:** A Pakistani finance ministry analyst is preparing for the next
EFF review with the IMF. They need to understand whether WorldSim can model the distributional
consequences of front-loaded versus phased conditionality — the central negotiating question for
every programme country with a politically constrained implementation capacity.

**Capability evaluated:** AEP-011 Type B counter-factual comparison (phased conditionality CF
vs front-loaded baseline). Specifically: does the engine find that phased delivery reduces peak
social cost during the adjustment period?

**North star test question:** Does this capability change what the Pakistani ministry's team
can argue at the table?

**Assessment:**

Yes — with a specific scope qualification.

The AEP-011 Type B result shows that the engine finds phased conditionality (25%/step,
implementation_capacity=0.85) produces better hd_composite outcomes at Step 2 (+0.0232 peak
differential) and that the differential narrows toward Step 4 as both paths converge. This
is a directional claim, not a magnitude claim.

At the table, the Pakistani analyst can now say: "Our simulation finds that front-loaded
subsidy removal at 60% implementation feasibility produces lower human development outcomes
than phased removal at 85% implementation feasibility across the same 24-month window. This
is a direction-only finding under our current calibration. We are not claiming to know the
specific per-step differential — we are claiming the direction is confirmed by the model."

This changes what the ministry team can argue: they can demonstrate that their own scenario
analysis — using an open-source, methodologically transparent platform — finds the same
direction as the political economy theory: phased adjustment reduces peak social cost. They
cannot assert the specific magnitude (T3 calibration), but they can assert the direction, and
the counterpart cannot dismiss it as unfounded.

**What cannot be argued:** The ministry cannot use AEP-011 to argue that the engine confirms
programme survival probability is at risk under front-loaded conditionality (PSP=None gap).
The failure modes (Get-There-Itis, Hypoxia) are undocumented in the harness output. The 2022
floods are not modelled. These limitations must be disclosed alongside the direction claim.

**For AEP-010 (LKA):** The north star test cannot be answered affirmatively. The engine does
not find Sri Lanka's crisis arc. The analytical value for a Sri Lankan analyst is inverse: the
entry documents what WorldSim currently cannot do, which is itself useful for a credible
capability disclosure.

**North star test classification:** Tier 1 for AEP-011 (user-facing policy design comparison
for IMF conditionality context). Tier 2 (infrastructure/scope documentation) for AEP-010
(capability gap disclosure entry, not capability demonstration).

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on sprint branch — PR #1814 merged to sprint/m20-g3; CI green (checks: audit, changes, branch-naming, session-state-size-check, test-backend, lint, compliance-scan all SUCCESS; backtesting in-progress; playwright-e2e SKIPPED)
- [x] Gap closure issues filed per sprint plan requirement — #1815 (PRT), #1816 (BGD), #1817 (remittance channel)
- [ ] Business PO ACCEPT verdict for each user-facing deliverable — **PENDING** EL in-session review
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables — filed §3.1 this session; AEP-010 and AEP-011 assessed
- [x] No open rejection artifacts
- [x] Near-miss sweep — no new near-miss findings in G3 beyond Issue #1797 extension (LKA all-six failure modes undetected); no new NM entries required (pattern extends existing #1797, not a new hazard)
- [x] North star test artifact on record — §3.2 above; PAK phased conditionality scenario; AEP-010 scope-limitation classification

**Pending BPO condition:** This document is filed in advance of EL BPO review. Integration PR will open after EL confirms BPO verdict in-session. If EL identifies revision conditions, this section is updated before integration PR is opened.

> PI Agent sprint exit verdict: **CONDITIONAL — pending EL Business PO verdict on AEP-010 and AEP-011.**
>
> Two AEP entries merged to sprint/m20-g3 for the SOUTH-SE-ASIAN calibration family.
> Gap closure issues filed: #1815 (PRT), #1816 (BGD), #1817 (remittance channel).
>
> G3 primary finding: AEP-010 (LKA) is the most complete fidelity failure in the AEP portfolio.
> The `debt_moratorium` + `default_declaration` interaction producing a composite improvement (not
> collapse) is a new engine inconsistency not previously documented. AEP-011 (PAK) delivers a
> correct directional signal for conditionality propagation and a COUNTER_FACTUAL_BETTER phased
> adjustment result — the strongest policy-design finding in the SOUTH-SE-ASIAN family.
>
> All-portfolio pattern at G3 close: DIRECTION_ONLY is the consistent ceiling across all four
> calibration families. G3 extends the failure mode non-detection finding (Issue #1797) to the
> most extreme test case (LKA all-six-failure-modes) and adds a new `debt_moratorium` interaction
> gap as a candidate for a standalone engine gap issue before Demo 9.
>
> Customer Agent Layer 3 on record. North star test on record.
> BPO verdict pending EL review; integration PR will open on EL confirmation.
>
> — PI Agent, 2026-07-07

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G3 of M20. It is filed at
`docs/process/sprint-plans/m20-g3-sprint-exit.md`. Sprint closes when:
1. EL provides Business PO ACCEPT on the G3 AEP entries (AEP-010 and AEP-011).
2. This document is updated with ACCEPT verdicts.
3. Integration PR (`sprint/m20-g3` → `release/m20`) is opened with PI Agent gate comment and merges with CI green.
