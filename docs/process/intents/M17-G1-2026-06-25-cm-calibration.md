---
name: M17-G1-cm-calibration
type: implementation-intent
issues: "#1229, #1248"
status: Step 1 authored — CM calibration decision document must be filed before implementation PR opens
authored-by: Chief Methodologist
authored-date: 2026-06-25
implementing-agent: Chief Methodologist
sprint-entry: "docs/process/sprint-plans/m17-g1-sprint-entry.md — EL Approved 2026-06-25"
adr-reference: "N/A — calibration constant revision within ADR-005 Decision 1 (DemographicModule) and ADR-005 Decision 6 (GovernanceModule)"
release-branch: release/m17
---

# Implementation Intent: M17-G1 — Chief Methodologist Calibration Sprint

> **Calibration sprint — no ADR.** This intent document covers two Wave 1 deliverables:
> (1) DemographicModule ELASTICITY_REGISTRY revision (#1229) and (2) GovernanceModule
> fiscal conditionality transmission specification (#1248). Both are calibration constant
> revisions within the existing module architecture established by ADR-005/ADR-006 — no new
> architectural decision is required.
>
> **Intent gate structure:** This document satisfies Step 1 of the agent execution lifecycle.
> The CM calibration decision document (Step 3 in sprint entry sequencing) is a separate
> artifact that specifies the chosen constants and uncertainty ranges. The intent document is
> filed first and defines what "done" looks like. The calibration decision document is filed
> after research and before the implementation PR opens — it closes the PENDING gate in
> sprint entry Section 2.3.

---

## 1. Source

**Issues:**
- #1229 — feat(simulation): fiscal-to-cohort elasticity calibration — DemographicModule ELASTICITY_REGISTRY revision
- #1248 — feat(simulation): governance sensitivity calibration — GovernanceModule fiscal conditionality transmission

**ADR reference:** N/A — calibration revision within ADR-005 Decision 1 and ADR-005 Decision 6. No new architectural decision required.

**Authored by:** Chief Methodologist
**Date:** 2026-06-25
**Implementing agent:** Chief Methodologist

**Background:** The fiscal spending cut → cohort-level poverty headcount chain currently produces
+0.0015pp Q1 `poverty_headcount_ratio` per step under a -3% GDP fiscal shock (at standard
multiplier 0.5 × elasticity -0.10 in `gdp_growth_change`). This is insufficient to produce a
visible cohort-level poverty trajectory within a realistic 8-step programme window starting from
a T3 Senegal baseline. Two gaps identified at M16-G8 Step 5b: (1) the fiscal multiplier chain
may not capture the full magnitude of poverty effect from a direct social spending cut; (2)
`imf_program_acceptance` is in `_SUBSCRIBED_EVENTS` but has no demographic elasticity entries.
The GovernanceModule similarly shows near-zero governance response to fiscal conditionality events
in the 8-step quarterly window.

---

## 2. Persona Trace Elements Targeted

> *Calibration infrastructure with no new UI element. Forward trace: calibration change →
> FRAME-D milestone sentence fires within the 8-step Demo 6 Senegal window → Persona 2 can
> present an honest, empirically-defensible cohort-level consequence at the negotiating table.*

**P-1 — Persona served:**
Indirectly: **Persona 2 — Finance Ministry Negotiator** (Aicha Mbaye archetype, `docs/ux/personas.md §Persona 2`).
No new UI element is introduced. Forward trace: the calibration enables the Demo 6 FRAME-D
milestone sentence to fire within the 8-step Senegal window — allowing Persona 2 to cite a
visible Q1 informal-sector poverty trajectory as the fiscal consequence argument in a
conditionality negotiation. Without calibrated elasticities, the trajectory is too flat to
constitute a credible demonstration of the human cost of fiscal consolidation.

**P-2 — Entry state:**
N/A — Tier 3 infrastructure. Forward trace: FRAME-D milestone sentence fires in Demo 6 Step 4
narrative (`docs/demo/m16/stakeholder-walkthrough.md` FRAME-D milestone sentence), which is
delivered in the Reactive entry state (90-second negotiating room context, Journey B Step 3).

**P-3 — Journey reference:** N/A — infrastructure tier. Downstream: Journey B Step 3 [Near-Term-Gap].

**P-4 — Time/interaction ceiling:** N/A — infrastructure tier. Downstream ceiling: FRAME-D
milestone sentence must appear within a ≤ 8-step Demo 6 Senegal programme window (quarterly
resolution, T3 Article IV conditionality scenario).

**P-6 — Negotiating leverage delivered (Persona 2):**
N/A at calibration tier. Forward trace: calibrated ELASTICITY_REGISTRY → FRAME-D fires in Demo 6
walkthrough → Persona 2 can state "Q1 informal-sector poverty headcount rose by N percentage
points per programme quarter under -3% GDP fiscal consolidation — this is the cohort-level
consequence of [the conditionality term]." The specific N is certified by the CM calibration
decision document.

**P-7 — North star capability delivered:**
N/A for calibration infrastructure tier. Forward trace: after the ELASTICITY_REGISTRY revision,
the Senegal simulation produces a visible Q1 poverty trajectory response to a fiscal
conditionality shock — enabling the Demo 6 Senegal walkthrough to present an honest quantified
cohort-level consequence rather than a structurally-flat trajectory. The Senegal finance ministry
analyst can cite the direction and order-of-magnitude of poverty increase from IMF Article IV
conditionality terms, in the programme's own quarterly framing.

---

## 3. Observable Application State

> *All states are verifiable by an external observer — a QA reviewer or CI system — using
> only the running application and source files. No source code analysis of implementation
> logic is required to confirm any state below.*

### 3.1 Primary observable state (#1229 — FRAME-D integration test)

`backend/tests/test_m17_g1_frame_d_calibration.py` passes in CI (the `test-backend` required
check is green) when run against the Senegal T3 Article IV conditionality shock scenario:

- SEN entity; `fiscal_policy_spending_change = Decimal("-3.0")` (representing -3% GDP social
  spending cut); quarterly resolution; 8-step programme window
- The test asserts that `poverty_headcount_ratio` for the Q1 informal cohort
  (`IncomeQuintile.Q1`, `EmploymentSector.INFORMAL`) shows a positive delta per step that
  falls within the lower and upper bounds specified in the CM calibration decision document
- Both bounds must be non-zero and the lower bound must exceed +0.0015pp (the pre-calibration
  response) — or the calibration decision document must explicitly defend why the current
  calibration is correct at the CM's confidence tier assessment

**What this confirms:** The ELASTICITY_REGISTRY revision produces a demographically meaningful
poverty response to fiscal conditionality at T3 confidence. The test failing CI is unambiguous
evidence the calibration is unchanged.

**Dependency on calibration decision document:** AC-1 cannot be authored or confirmed until
the CM calibration decision document specifies the certified range. The FRAME-D test is authored
after the calibration decision document is filed (sprint entry sequencing Step 5 — after Step 3).

### 3.2 Secondary observable states

**State A — ELASTICITY_REGISTRY updated entries visible in source:**
After the implementation PR merges, at least one of the following is true in
`backend/app/simulation/modules/demographic/elasticities.py`:
- The `gdp_growth_change` Q1 informal `elasticity` value differs from `Decimal("-0.10")`, OR
- At least one `CohortElasticity` entry with `event_type="fiscal_policy_spending_change"` is
  present in `ELASTICITY_REGISTRY`, OR
- At least one `CohortElasticity` entry with `event_type` matching `imf_program_acceptance`
  is present in `ELASTICITY_REGISTRY`

All updated or new entries must contain a `source` string with a cited reference and a
`source_registry_id` matching the `ACADEMIC_LITERATURE_*` naming convention
(`docs/DATA_STANDARDS.md §Data Provenance Requirements`).

Observable confirmation: `grep -n "fiscal_policy_spending_change\|imf_program_acceptance" backend/app/simulation/modules/demographic/elasticities.py` returns at least one match, OR
the `gdp_growth_change` Q1 informal `elasticity` value in source differs from `Decimal("-0.10")`.

**State B — CM calibration decision document filed:**
`docs/calibration/m17-g1-elasticity-calibration-decision.md` exists in the repository and
contains (readable by `cat` without source code access):
- A section explicitly naming the chosen calibration path (one of: revised GDP channel
  elasticity, new direct fiscal channel entries, new programme-acceptance entries, or a
  defended position that current calibration is correct)
- Updated ELASTICITY_REGISTRY constant values with stated uncertainty ranges
- The FRAME-D acceptance criterion: the Q1 `poverty_headcount_ratio` delta range per step
  (lower bound, upper bound) under the Senegal T3 conditionality shock that AC-1 will assert
- At least two source citations from `docs/data-sources/approved-sources.md`

**State C — CM governance sensitivity specification filed:**
`docs/calibration/m17-g1-governance-sensitivity-specification.md` exists in the repository
and contains a headed section for each of the three open questions in #1248, with an explicit
position statement — not a deferral — in each section:
1. Whether `imf_program_acceptance` has a direct governance transmission pathway distinct from
   the GDP channel (with cited evidence for or against)
2. Whether institutional capacity degradation under austerity has an empirically defensible
   elasticity for the GovernanceModule (with candidate constant if yes, or citation of
   why no relationship is defensible if no)
3. Whether the 8-step quarterly window is sufficient to manifest governance stress, or whether
   governance decline is a longer-horizon signal that the current quarterly resolution cannot
   capture (with timeline estimate if the latter)

### 3.3 Silent failure detection

**Silent failure — FRAME-D test passes but range is set to include pre-calibration response:**
If ELASTICITY_REGISTRY is updated but the FRAME-D test's lower bound is set to ≤ +0.0015pp
per step, the test passes without addressing the calibration gap. Detection: AC-3 requires the
calibration decision document's lower bound to exceed +0.0015pp, or to explicitly defend why
the current calibration is the correct citable position. A calibration decision document that
sets a lower bound of ≤ +0.0015pp without a written defence is incomplete and blocks AC-3.

**Silent failure — governance specification filed but three questions not answered:**
If the governance specification exists but contains "further research needed" without a position
statement for any of the three questions, the Wave 1 exit gate is not satisfied. Detection:
each of the three sections must contain an explicit "CM position: [YES/NO/WORKING-AS-DESIGNED
+ rationale]" line. A section without a position line is incomplete.

---

## 4. Acceptance Criteria

> *All criteria verifiable from source files and CI output without reading implementation
> logic. Test file: `backend/tests/test_m17_g1_frame_d_calibration.py`.*
>
> *AC-1 cannot be authored or confirmed until AC-3 is satisfied. The sequencing is:
> AC-3 (decision document filed) → FRAME-D test authored → AC-1 confirmed in CI.*

**AC-1 (FRAME-D integration test — #1229):**
In `backend/tests/test_m17_g1_frame_d_calibration.py`, running the SEN entity with
`fiscal_policy_spending_change = Decimal("-3.0")` at quarterly resolution, 8-step window,
the test asserts that the `poverty_headcount_ratio` delta for the Q1 informal cohort at step 1
falls within the lower and upper bounds stated in the CM calibration decision document (State B).
The CI `test-backend` check is green on the implementation PR branch.

**AC-2 (ELASTICITY_REGISTRY source change — #1229):**
At least one of the following is present in
`backend/app/simulation/modules/demographic/elasticities.py` after the implementation PR merges:
(a) the `gdp_growth_change` Q1 informal `elasticity` value differs from `Decimal("-0.10")`, OR
(b) at least one `CohortElasticity` with `event_type="fiscal_policy_spending_change"`, OR
(c) at least one `CohortElasticity` with `event_type` matching `imf_program_acceptance`.
All new or updated entries have `source_registry_id` following the `ACADEMIC_LITERATURE_*`
convention and a non-empty `source` string containing a citable reference.

**AC-3 (CM calibration decision document — #1229):**
`docs/calibration/m17-g1-elasticity-calibration-decision.md` exists in the repository on the
implementation PR branch and contains: a named calibration path, at least one updated constant
with uncertainty range, a FRAME-D lower bound > +0.0015pp (or a written defence), and at
least two source citations.

**AC-4 (CM governance sensitivity specification — #1248):**
`docs/calibration/m17-g1-governance-sensitivity-specification.md` exists in the repository
and contains an explicit position statement for each of the three questions in #1248. Each
section must include a "CM position:" line. A specification with a "further research needed"
deferral in place of a position fails this criterion.

**AC-5 (pre-push lint gate — #1229 implementation PR):**
`cd backend && ruff check . && mypy app/` exits 0 on the implementation PR branch. The
FRAME-D test file must pass `mypy` type checking with no new errors introduced.

---

## 4b. Visual Spec (before/after)

N/A — backend only. No UI changes in this sprint group. All acceptance criteria are source
file changes and document artifact verifications confirmable without browser or Playwright.

---

## 5. Kryptonite Constraint Check

*Authority: `docs/process/agent-execution-lifecycle.md §Kryptonite Design Constraint (FD-3)`.*

**Does this implementation's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` **No — with qualification.** The calibration change does not itself require specialist
mediation; it produces a simulation output (Q1 poverty trajectory response) that was previously
too flat to be interpretable. After calibration:
- The FRAME-D milestone sentence fires within the Demo 6 Senegal scenario window — it presents
  a direction and order-of-magnitude of poverty headcount change without requiring the finance
  ministry analyst to interpret calibration constants
- The trajectory output is self-interpreting at the Layer 3 level when read through the demo
  walkthrough framing (`docs/demo/m16/stakeholder-walkthrough.md` Step 4 FRAME-D sentence)

**Asymmetry acknowledged:** The CM calibration decision document contains technical uncertainty
ranges that require methodologist expertise to evaluate. These are methodology-transparency
documentation (open source as strategy) — not user-facing mediation barriers. The user-facing
output (poverty trajectory visible in Zone 1A, FRAME-D milestone sentence in the walkthrough)
is readable without specialist translation within the 90-second Reactive ceiling.

---

## 6. Out of Scope

**GovernanceModule code changes (#1248 Wave 1):** Wave 1 deliverable for #1248 is the
specification document only. GovernanceModule ELASTICITY_REGISTRY code changes are Wave 2
scope — gated on Wave 2 sprint entry. If the CM's three-question assessment concludes that
governance is working-as-designed at the quarterly resolution, no code change is required.

**Multi-scenario comparison (#394):** Wave 2; gated on Wave 1 exit.

**DEMO6 CRITICAL polish (#1249/#1250/#1253/#1239):** Wave 2; gated on Wave 1 exit.

**Any frontend changes:** G1 is exclusively CM research and backend calibration. No frontend
code is modified in this sprint group.

**Non-Senegal backtesting fixture extension:** The FRAME-D test is the Senegal T3 conditionality
fixture only. Other backtesting fixtures (Argentina, Ecuador, Lebanon, Thailand, Greece) are not
in G1 scope unless the CM calibration decision document determines that a cross-entity regression
test is required to validate the new elasticity values without overfitting to the Senegal case.

**Confidence tier upgrade:** The revised ELASTICITY_REGISTRY entries remain Tier 3 (T3).
Upgrading to Tier 2 requires backtesting validation against historical country-level poverty data —
this is M18 or later scope after the calibration is stable.

**`imf_program_acceptance` governance implementation (#1248):** If the CM governance specification
concludes that `imf_program_acceptance` should have a direct governance transmission pathway, the
code implementation of that pathway is Wave 2 scope — the specification document establishes the
position; implementation is a separate Wave 2 issue.

---

## 7. Test Authorship Obligation

> *The FRAME-D test is authored by the Chief Methodologist alongside the calibration code
> change — the CM holds both the calibration research knowledge and the implementation
> responsibility for #1229. The test is authored from the CM calibration decision document,
> not from this intent document — because the specific delta range is determined by the
> calibration research.*

**QA Lead:** Chief Methodologist (CM holds R for both implementation and FRAME-D test authorship
for #1229, per sprint entry Section 2.4. CM-specific calibration knowledge is required to
author a meaningful range assertion — the QA Lead Agent does not hold the necessary domain
knowledge to derive the FRAME-D bounds independently.)

**Test authorship deadline:** Before the ELASTICITY_REGISTRY implementation PR is opened against
`release/m17` — specifically, after the CM calibration decision document is filed (AC-3) and
using that document as the specification for the FRAME-D range bounds.

**Test file location:**
- `backend/tests/test_m17_g1_frame_d_calibration.py` — FRAME-D integration test (#1229)
- No E2E test required — #1248 is a specification document only; #1229 has no UI change

**Acceptance criteria covered by test:** AC-1 (FRAME-D range assertion), AC-2 (ELASTICITY_REGISTRY
entry existence can be asserted in a separate unit test in the same file), AC-5 (lint gate —
confirmed before push, not by the test itself).

**QA Lead acknowledgment:**
`[x]` CM (QA Lead): FRAME-D test for AC-1 authored and filed before implementation PR opens.
      Date: 2026-06-25 — `backend/tests/test_m17_g1_frame_d_calibration.py`; 12 tests;
      ruff + mypy clean; red-before-implementation confirmed (7 fail on pre-revision constants,
      5 pass on calibration-independent invariants).

---

*Intent document authority: `docs/process/intent-template.md` (version 2026-06-17).
Sprint entry: `docs/process/sprint-plans/m17-g1-sprint-entry.md` (EL Approved 2026-06-25).
Implementing agent: Chief Methodologist. No ADR — calibration constant revision within
ADR-005 Decision 1 (DemographicModule) and ADR-005 Decision 6 (GovernanceModule).
Issues in scope: #1229 (Wave 1 code change), #1248 (Wave 1 specification document only).
Wave 2 gated on PI Agent Wave 1 exit confirmation — see sprint entry Section 4 Step 8.*
