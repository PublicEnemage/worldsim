---
name: m19-cm-d-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: CM Sprint D — ARG baseline Kirchner recovery inputs + bounds recalibration
status: Filed — awaiting EL approval
authored-by: PM Agent
authored-date: 2026-07-05
el-approved: pending
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19 CM Sprint D: ARG Baseline Kirchner Recovery Inputs

**Status:** Filed — awaiting EL approval before implementation begins
**Date authored:** 2026-07-05
**Release branch:** `release/m19`
**Sprint plan:** `docs/process/sprint-plans/m19-sprint-plan.md`
**BPO evaluation:** see §BPO Assessment below

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| GitHub Milestone | #21 |
| Sprint number | CM Sprint D (Wave 6 — post-G8; final M19 Demo 8 Act 2 condition) |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md` |
| Exit checklist issue | #1535 |
| Sprint groups in scope | CM Sprint D (calibration-only; backend fixture + test bounds only) |
| Wave coordination tier | Standard — no concurrent active sprint groups at entry |
| Concurrent groups at entry | 0 of 5 max — G1–G8 + CM-A/B/C all integrated |
| Cross-group dependencies | G8 integration PR #1748 merged 2026-07-04 — `_classify_direction` primary_indicator fix live on `release/m19`. CM-D depends on that fix being present. |

---

## Section 2 — Entry Invariants Checklist

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` — current; G8 + CM-A/B/C all integrated (PR #1748 merged 2026-07-04)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` triggers on `release/m*` and `sprint/m*` branches
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m19-sprint-plan.md` — EL-approved 2026-07-02

### 2.2 — ADR prerequisite gate

- [x] **N/A — no new ADR required.** CM Sprint D extends the ARG baseline fixture and recalibrates
  existing CM Sprint B bounds. No interface change, no new ELASTICITY_REGISTRY structure, no API change.
  The `entity_families` scoping mechanism (CM Sprint A), the `_classify_direction` routing
  (G8), and the TYPE_B harness pre-advance pattern (G8) are all in place on `release/m19`.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| CM-D | None — fixture extension + bounds recalibration | N/A | CLEAR |

### 2.3 — Intent document gate

- [ ] **PENDING — intent document to be filed before implementation PR opens.**
  Path: `docs/process/intents/M19-CMD-2026-07-05-arg-kirchner-recovery-inputs.md`
  
  The intent document must specify:
  - Kirchner 2003 recovery inputs: fiscal parameter names, proposed values, historical sourcing citations
  - Confidence tier classification for the new step-3 inputs
  - Rationale for input selection (which engine channels these activate)
  - Pre-implementation CM Agent sign-off line (see §2.4)

  **Gate rule:** Implementation PR may not open until this document is filed and CM Agent has
  signed off on the calibration decision (§2.4). If EL approves this entry before the intent
  document is filed, the implementation gate is still blocked until §2.3 + §2.4 are cleared.

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| ARG fixture step-3 Kirchner recovery inputs + bounds recalibration | N/A (calibration extension) | `docs/process/intents/M19-CMD-2026-07-05-arg-kirchner-recovery-inputs.md` | **PENDING — BLOCKING** |

### 2.4 — CM calibration decision gate

- [ ] **PENDING — CM Agent calibration decision document to be filed before implementation PR opens.**
  Path: `docs/calibration/m19-cm-d-arg-kirchner-calibration-decision.md`

  The calibration decision document must record:
  - CM Agent activation and consultation
  - Kirchner 2003 historical inputs: sources, values, confidence tier (expected T3)
  - Extended fixture empirical run results: actual `per_step_diff[2]` with recovery inputs
  - Certified bounds: `lower = observed × 0.5`, `upper = observed × 2.0` (T3 formula)
  - CM sign-off: explicit "APPROVED" comment on #1750

  **Gate rule:** Implementation PR (`feat/m19-cm-d-impl` or similar) may not open until this
  document is filed and the CM Agent has posted an APPROVED comment on #1750.

  *Precedent: CM Sprint B §2.4 required calibration decision before implementation PR.*

### 2.5 — QA test authorship gate

- [x] **SATISFIED — test file exists and is RED for the correct reason.**
  File: `backend/tests/test_m19_cm_b_elasticity_calibration.py`
  Test: `TestAC1MagnitudeDivergence::test_arg_hd_composite_divergence_within_magnitude_bounds`

  The test currently fails with `per_step_diff[2]=Decimal('0') outside [0.003, 0.050]`.
  This is the correct RED-before-implementation state: the fixture has no step-3 BL data,
  so `hd_composite=None` → diff=0. The implementation PR will:
  1. Extend the fixture (add Kirchner inputs at step 3)
  2. Update the assertion bounds to CM-certified values

  The test was authored before the CM-D implementation (it predates CM-D by design —
  CM Sprint B authored it; CM-D delivers the inputs that make it pass).

  **NM-094 check:** PI Agent verifies the test file is present on `sprint/m19-cm-d` before
  the exit gate passes. It is present (inherited from `release/m19`).

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation

- [x] All ADR decisions affecting this sprint's scope are EL-approved and merged to `release/m19`

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1750 | fix(backtesting): ARG baseline Kirchner 2003 recovery inputs — step 3 fixture design and bounds recalibration | CM-D | **Immediate — Demo 8 Act 2 blocker; final open condition** |
| #1712 | Demo 8 Act 2 verification: ARG AC-1 live harness run | CM-D | **Immediate — close after #1750 delivers and live run passes** |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Horizon | Rationale for exclusion |
|---|---|---|---|
| #1544 | Demo 8 — live stakeholder session | Milestone exit | Separate milestone exit gate; requires all Demo 8 conditions CLEARED first |
| #1535 | M19 Exit Checklist | Milestone exit | Opened after Demo 8 (#1544) completes |

### 3.3 — Design pre-decision (CM consultation 2026-07-04)

The G8 sprint contained a CM Agent consultation on the ARG AC-1 architecture. Decision on record:

- **Option A selected:** Extend `build_argentina_scenario()` to `n_steps=3`
- **Rationale:** 2001–2003 window captures Argentina's full crisis-and-recovery arc. The
  CM-approved counter-factual already has `n_steps=3` (heterodox path through 2003 Kirchner
  entry). A 2-step baseline creates an artificial asymmetry where baseline ends at the default
  trough and the counter-factual continues into the recovery window.
- **Engine behaviour (empirical, 2026-07-04):** BL step 3 without inputs stays flat at
  `hd_composite=0.3723` — the post-default trough. The engine correctly produces no recovery
  without explicit fiscal inputs.
- **Divergence at step 3 without inputs:** `0.2027` — outside `[0.003, 0.050]`.
  The CM-D task is to add recovery inputs that produce **convergence** at step 3, reducing
  the divergence to within certified bounds.

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| CM-D | None — calibration extension | N/A | Yes (pending EL approval + §2.3/§2.4 gates) |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-05
**Sweep period:** Since G8 close (2026-07-04)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified since G8 close | N/A | N/A | N/A |

**Prior NM applicability (§6.5):**
- NM-084 (CM sign-off ordering gap): CM sign-off on #1750 must be recorded BEFORE the
  implementation PR opens — not while CI runs, not after PR is merged.
- NM-085 (co-dependent fixture CI sequencing): fixture extension and bounds update are in
  the same PR. No sequencing risk.
- NM-094 (test file presence check): `test_m19_cm_b_elasticity_calibration.py` is present
  on `sprint/m19-cm-d` (inherited from `release/m19`). PI Agent verifies at exit gate.
- NM-097 (CM test skip guard): The ARG AC-1 test will pass only against a live DATABASE_URL.
  CI will skip via existing `@pytest.mark.backtesting` guard. Dispatch with
  `force_backtesting=true` required for exit gate verification.

---

## Section 6 — Sprint Group Isolation

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m19-cm-d` |
| Cut from | `release/m19` |
| Sprint journal issue | #1751 |

Sprint sub-branch already cut: `git checkout -b sprint/m19-cm-d release/m19` (2026-07-05).

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `backend/tests/fixtures/argentina_2001_scenario.py` | Sprint sub-branch | Kirchner recovery inputs at step 3 |
| `backend/tests/test_m19_cm_b_elasticity_calibration.py` | Sprint sub-branch | Bounds recalibration |
| `docs/calibration/m19-cm-d-arg-kirchner-calibration-decision.md` | Sprint sub-branch | CM calibration decision artifact |

No overlap with any other planned sprint. All writes are backend fixture and test files.

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

#### 6.3a — New output paths declaration

- [x] No new output directories — all generated paths already covered by `.gitignore`

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies at entry. CM-D requires G8 integration (#1748) to be
  present on `release/m19` — SATISFIED (merged 2026-07-04).

### 6.5 — Prior NM verification

**NM verification sweep date:** 2026-07-05

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-084 | CM sign-off must be recorded on the issue BEFORE implementation PR opens | Yes — §2.4 gate blocks implementation PR until CM sign-off on #1750 |
| NM-085 | Co-dependent fixture CI sequencing awareness | N/A — fixture + test update are in the same single PR (no sequencing risk) |
| NM-094 | PI Agent verifies test file presence on sprint branch before exit gate | Yes — test file present on sprint/m19-cm-d (inherited from release/m19) |
| NM-097 | CM backtesting tests require DATABASE_URL; skip guard checks env var only | Yes — exit gate verification requires `force_backtesting=true` dispatch; documented in §5 |
| NM-098 | Parameters accepted by a function must be used or explicitly documented as reserved | N/A — G8 delivered the fix; CM-D consumes the corrected `_classify_direction` |

---

## BPO Assessment (2026-07-05)

**Verdict: PROCEED — M19 scope; HIGH priority; final Demo 8 Act 2 condition**

**Demo 8 impact (BLOCKER):** CM-D delivers the last open Demo 8 Act 2 condition. GRC and PAK
AC-1 are CLEARED. ARG AC-1 (#1712) remains OPEN and blocks Demo 8 Act 2. Without CM-D, the
Demo 8 narrative cannot demonstrate the three-country empirical calibration result.

**North star test:** A Bolivian finance ministry analyst, reviewing Argentina's 2001–2003
trajectory at a debt restructuring session, asks: "Did the heterodox Kirchner path produce
meaningfully different human development outcomes than continuing the IMF austerity path?"
The ARG fixture answers this. After CM-D delivers the step-3 recovery inputs, the harness
correctly measures `hd_composite` divergence between the baseline (continued austerity at
2003 pace) and the counter-factual (Kirchner heterodox programme entry), confirming the
calibrated difference is instrument-visible with empirically certified bounds. The analyst can
point to a specific measured gap with T3 confidence tier sourcing. Without CM-D, the harness
reports zero divergence at step 3 — the Demo 8 Act 2 claim is unmeasurable.

**Priority:** HIGH. CM-D is the final M19 blocker before Demo 8.

---

## EL Approval Record

**EL approval:** pending

> {EL approval statement}
> — @PublicEnemage ({date})
