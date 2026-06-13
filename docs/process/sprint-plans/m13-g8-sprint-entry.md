---
name: m13-g8-sprint-entry
type: sprint-entry
milestone: M13 — Political Economy and Instrument Credibility
sprint-group: G8 (G8a + G8b)
status: EL-approved — implementation may begin
authored-by: PM Agent
authored-date: 2026-06-13
el-approved: 2026-06-13
release-branch: release/m13
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M13, G8: Standards, Methodology, Calibration and Mode Transition UX

**Status:** EL-approved 2026-06-13 — implementation may begin
**Date authored:** 2026-06-13
**Release branch:** `release/m13`
**Sprint plan:** `docs/process/sprint-plans/m13-sprint-plan.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This document gates G8 (both sub-groups). G8 was not in the original M13 sprint waves;
it was identified and scoped at the M13 midpoint HORIZON sweep (2026-06-13) following
completion of G1–G7. The HORIZON sweep is the formal mechanism for near-term backlog
promotion to an active sprint group per `docs/process/sprint-planning-sop.md`.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M13 — Political Economy and Instrument Credibility |
| GitHub Milestone | #9 |
| Sprint number | 2 (mid-milestone — HORIZON sweep promotion) |
| Release branch | `release/m13` |
| Sprint plan document | `docs/process/sprint-plans/m13-sprint-plan.md` |
| Exit checklist issue | #264 |
| Sprint groups in scope | G8a (standards/methodology/calibration), G8b (UX) |
| Sub-group parallelism | G8a and G8b may run in parallel — no shared files |
| HORIZON sweep date | 2026-06-13 |
| Triage authority | PM Agent TRIAGE assessment 2026-06-13 |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G8.
An unchecked invariant blocks the relevant sub-group from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m13` cut from `main` 2026-06-12 (verified in M13 Sprint 1 entry; confirmed current)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at M13 kickoff (NM-035 fix, pre-existing)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m13-sprint-plan.md` approved 2026-06-12

### 2.2 — ADR prerequisite gate

Neither G8a nor G8b requires a new ADR. G8a issues are standards, documentation, and
calibration work — none cross the ADR threshold (no new module boundary, no new data
model, no new measurement framework). G8b (#393) is a UX fix whose mode transition design
is already on record in PR #390 Gap 5; the step-position carry-forward and entity-config
preservation are implementation of a specified design, not a new architectural decision.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G8a | None | N/A | **CLEAR** |
| G8b | None | N/A | **CLEAR** |

- [x] Neither sub-group has an ADR prerequisite. Both gates are CLEAR.

### 2.3 — Intent document gate

**G8a — Infrastructure sprint exception applies (EL direction, 2026-06-13).**

G8a deliverables are standards updates, documentation residuals, calibration data changes,
and a schema-level output field addition (#271 metadata tag). No G8a deliverable introduces
a new user-visible UX element or changes existing UX behaviour. The #271 reversibility
classification metadata field is an API-level output addition; its surface presentation
(display in simulation output) is a follow-on concern gated by the MDA calibration work
deferred to M14. On this basis the EL has directed that the infrastructure sprint exception
applies to G8a in full — intent documents are not required for G8a issues.

*Note on #271 scope boundary:* The infrastructure sprint exception is specific to the
metadata-tag-only scope. If any G8a implementation produces a new user-visible label,
alert text, or indicator display in the running application, that element is out of G8a
scope and must be tracked in a separate G9 issue with a full Phase A lifecycle.

- [x] G8a: Infrastructure sprint exception applied — intent documents not required.
- [ ] G8b: Intent document required before implementation PR opens — **BLOCKING G8b IMPLEMENTATION**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| G8a — #45, #27 R1–R3, #271, #823, #824 | N/A (infrastructure exception) | N/A | N/A — exception applies |
| G8b — Mode 1→2 step preservation (#393) | N/A (no ADR required) | `docs/process/intents/G8b-2026-06-13-mode-transition-step-preservation.md` | No — must file before G8b PR opens |

**G8b intent document minimum content:**

The intent document for #393 must derive its acceptance criteria from the mode transition
design specified in PR #390 Gap 5 and the Sri Lanka 2022 marquee case. Required observable
application states:

1. **Step position preservation:** Advance Mode 1 to step N; trigger Mode 1→2 transition;
   confirm the Mode 2 simulation begins at step N (not at step 0 or step 1).
2. **Entity configuration carry-forward:** Transition from Mode 1 with JOR+EGY configuration;
   confirm Mode 2 session has the same entity set and relationship graph without re-entry.
3. **Confirmation modal content:** Transition modal must name what is preserved ("current step
   position and entity configuration") and what changes ("replay history is not editable in
   simulation mode"). Text must be specific — not a generic "unsaved changes will be lost"
   pattern.
4. **Sri Lanka marquee case execution:** A Mode 1 replay → Mode 2 simulation transition at
   step N must be executable in a single session without manual context reconstruction.

### 2.4 — QA test authorship gate

**G8a — Infrastructure sprint exception applies.** QA test authorship gate waived for all
G8a deliverables. Backend calibration changes (#823, #824) must include regression tests
confirming existing backtesting fixtures still pass after the change — these are correctness
guards, not new user-facing capability tests, and may be authored in the same PR as the
implementation.

**G8b — Full Phase A lifecycle.** QA tests must be authored from the G8b intent document's
observable application states before the implementation PR opens.

- [x] G8a: QA test authorship gate waived (infrastructure exception); regression guard tests shipped in implementation PR.
- [ ] G8b: QA test file authored before implementation PR opens — **BLOCKING G8b IMPLEMENTATION**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| G8a — calibration changes (#823, #824) | N/A | Regression assertions in existing backtesting test suite — authored in implementation PR | Exception applies — concurrent authorship permitted |
| G8b — Mode 1→2 preservation (#393) | `docs/process/intents/G8b-2026-06-13-mode-transition-step-preservation.md` | `frontend/tests/e2e/mode-transition.spec.ts` (or equivalent) | No — must be authored after intent document, before implementation PR opens |

**Required G8b test coverage (from observable application states above):**

- Playwright: advance Mode 1 to step 3 on the Hormuz fixture; trigger Mode 1→2 transition
  (accept confirmation modal); assert `data-testid="mode-indicator"` shows Mode 2 and the
  step counter shows step 3 (not step 0 or step 1)
- Playwright: after Mode 1→2 transition, assert entity configuration panel or scenario header
  still shows JOR and EGY entity identifiers — no re-entry prompt
- Playwright: transition modal content check — assert modal text contains "step position" and
  "entity configuration" as described elements (or equivalent named observable text)
- Playwright: assert Mode 1→2 transition completes without page reload or full state reset

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Group | Priority | Scope notes |
|---|---|---|---|---|
| #45 | standards: human development indicator standards and HCL effect size | G8a | near-term | Add HCL output field standards (5 fields), effect size thresholds, 4 test requirements to `CODING_STANDARDS.md`; cross-reference in `DATA_STANDARDS.md` |
| #27 (R1) | docs(calibration): add TARIFF_ATTENUATION/TARIFF_MAX_HOPS to calibration doc | G8a | near-term | Add Propagation Rules section to `docs/methodology/calibration-basis.md` with PLACEHOLDER declaration and calibration methodology for `attenuation_factor = 0.6`, `max_hops = 2` |
| #27 (R2) | docs(calibration): demo scenario docstring references calibration doc | G8a | near-term | Update `backend/scripts/demo_scenario.py` line 229 docstring to reference `docs/methodology/calibration-basis.md` |
| #27 (R3) | docs(calibration): ADR-001 calibration status note | G8a | near-term | Add single-sentence note to current ADR-001 milestone review entry referencing `docs/methodology/calibration-basis.md`; issue #44 as forward-calibration vehicle |
| #271 | feat(simulation): reversibility classification metadata tag on output indicators | G8a | near-term | **Scope-limited:** Add `reversibility` field (`recoverable` / `delayed_recovery` / `irreversible`) to simulation output indicators; classified indicators specified in issue (school enrollment, maternal/child mortality, skilled emigration, community social capital, ecosystem stocks crossing tipping points); no MDA recalibration; no display-layer changes |
| #823 | arch(methodology): ecological composite fixed denominator | G8a | near-term | Fix denominator at scenario initialisation; hold indicator set constant for full scenario run; disclose absent indicators separately; Chief Methodologist sign-off required before implementation PR merges |
| #824 | fix(engine): MENA arid-economy elasticity calibration for land_use_pressure_index | G8a | near-term | Biome-specific elasticity from FAO GFR arid-country subset; update `ECOLOGICAL_ELASTICITY_REGISTRY`; Chief Methodologist + Ecological Economist sign-off required before implementation PR merges |
| #393 | ux(mode-transition): Mode 1→2 step position preservation | G8b | near-term | Step position and entity config carry-forward; confirmation modal with explicit preservation disclosure; Sri Lanka 2022 marquee case execution |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Disposition | Rationale |
|---|---|---|---|
| #22 | Uncertainty quantification | Deferred to M14 | Major ADR-gated architectural undertaking; M14 primary deliverable candidate |
| #35 | Dynamic relationship weight updating | Deferred to M14 | ADR required; significant engine change; not aligned with M13 focus |
| #102 | Distributional scenario comparison | Deferred to M14 | Hard dependency on #22 |
| #274 | 25-year human capital trajectory | Deferred to M14 | Hard dependency on #271 full implementation + backtesting validation |
| #394 | Multi-scenario comparison (>2 scenarios) | Deferred to M14 | ADR required; architecture change |
| #837 | Configuration-driven demo scripts | Deferred to M14 | Developer tooling; no demo cycle in M13; M14 Demo 5 prep work |
| #271 MDA recalibration | MDA threshold recalibration for irreversible indicators | Deferred to M14 | Named follow-on: M14 near-term after reversibility metadata field is in production |

**#271 scope boundary on record:** The MDA calibration piece — calibrating thresholds
differently for indicators classified as irreversible — is explicitly a named M14 follow-on.
The G8a implementation must not touch MDA threshold values, MDA alert logic, or any
display-layer representation of reversibility. The reversibility field is a schema-level
addition to simulation output. A G8a implementation that modifies MDA thresholds or
introduces a user-visible reversibility label is out of G8a scope; any such change must
be extracted to a separate PR gated by a new sprint entry.

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G8a | None | N/A | Yes — after EL approves this entry document |
| G8b | None | N/A | Yes — after EL approves this entry document AND intent document + QA tests are filed |

**Implementation sequencing:**

**G8a sequence** (all items may proceed concurrently within G8a):
1. EL approves this entry document
2. Implementation PRs open for G8a items (no intent document gate; no QA test authorship gate)
3. For #823 and #824: domain agent sign-off (Chief Methodologist for both; Ecological Economist
   for #824) is a mandatory AC — implementation PR may not be merged without sign-off on record
4. For #27 residuals: close issue #27 via `Closes #27` in the G8a PR description once R1–R3
   are all committed in the same PR or confirmed complete across multiple PRs

**G8b sequence** (serial — intent document must precede implementation):
1. EL approves this entry document
2. Implementing agent authors intent document at
   `docs/process/intents/G8b-2026-06-13-mode-transition-step-preservation.md`
3. QA Lead authors test file before implementation PR opens
4. Implementation PR opens targeting `release/m13`
5. Verify step (Step 4): implementing agent confirms observable application states from the
   intent document are present in the running application
6. Business PO Step 5 Validate: execute Sri Lanka 2022 marquee case entry
   (Mode 1 replay → Mode 2 simulation in a single session, no context reconstruction)

**G8a and G8b may run in parallel.** G8a and G8b have no shared files; no merge conflict
risk. G8a PRs need not wait for G8b to complete, and vice versa.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-13
**Sweep period:** Since G7 sprint exit filed (2026-06-13, same session)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| #27 open on GitHub despite G4 (PR #915) marking it MERGED — PR did not use `Closes #27` syntax; two ACs (demo docstring, ADR-001 note) and one document gap (TARIFF_ATTENUATION missing from calibration doc) were not satisfied at G4 close | near-miss candidate | Flagged to PI Agent — judgment call: does an issue remaining open because `Closes #` syntax was omitted constitute a near-miss, or is this a documentation process gap? | Pending PI Agent determination |

**Sweep finding detail:**
Issue #27 was listed as closed in the G4 sprint group status (`SESSION_STATE.md` line 77)
but remained OPEN on GitHub at the time of the HORIZON sweep inspection (2026-06-13). Inspection
of PR #915 diff confirmed two original ACs (AC-3: demo scenario docstring; AC-4: ADR-001 note)
and one document gap (TARIFF_ATTENUATION / TARIFF_MAX_HOPS absent from the calibration
document's Propagation Rules section) were not satisfied. The PR's own test plan checked
only AC-2 (≥3 named parameters), not the full original AC set. The issue was carried as
"DONE" in session state without verifying GitHub closure.

PM Agent assessment: this is the same pattern as the AC-verification gap that drove Phase A
of the Process Redesign Sequence — an issue marked done in session state without confirming
all ACs against the original specification. Whether this rises to a near-miss (systemic process
gap) or a known execution gap is the PI Agent's determination to make.

---

## EL Approval Record

**EL approval:** 2026-06-13

> G8 sprint entry approved. G8a (standards/methodology/calibration) and G8b (mode transition
> UX) may proceed. G8a implementation PRs may open immediately — infrastructure sprint
> exception applies, no intent documents required. G8b implementation is blocked until the
> intent document is filed at `docs/process/intents/G8b-2026-06-13-mode-transition-step-preservation.md`
> and QA tests are authored. #271 scope is metadata tag only — no MDA recalibration.
> Domain agent sign-offs (#823: Chief Methodologist; #824: Chief Methodologist + Ecological
> Economist) are mandatory before those PRs merge.
> — @PublicEnemage (2026-06-13)
