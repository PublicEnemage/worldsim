---
name: m19-cm-d-sprint-exit
type: sprint-exit
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: CM Sprint D — ARG baseline Kirchner recovery inputs + bounds recalibration
status: Confirmed
authored-by: PI Agent
authored-date: 2026-07-05
release-branch: release/m19
sprint-entry: docs/process/sprint-plans/m19-cm-d-sprint-entry.md
---

# Sprint Exit — M19 CM Sprint D: ARG Baseline Kirchner Recovery Inputs

**Status:** Confirmed — PI Agent exit gate PASS
**Date confirmed:** 2026-07-05
**Release branch:** `release/m19`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
A sprint closes when all exit conditions in the entry §4 are satisfied and confirmed by
the PI Agent — not when CI is green and issues are closed.*

---

## Exit Conditions Checklist

### 1 — Business PO acceptance

- [x] **ACCEPT** — recorded 2026-07-05
  Issue #1750 comment: https://github.com/PublicEnemage/worldsim/issues/1750#issuecomment-4887265239
  Business PO: @PublicEnemage (EL)
  Deliverable accepted: ARG fixture extended to n_steps=3 (Kirchner 2003 `spending_change=+0.030`);
  AC-1 bounds certified `[0.10135, 0.40540]` from empirical CI run (`per_step_diff[2]=0.2027`)

### 2 — Customer Agent Layer 3 assessment

- [x] **PASS** — recorded 2026-07-05
  Issue #1750 comment: https://github.com/PublicEnemage/worldsim/issues/1750#issuecomment-4887265845
  Personas assessed: Persona 2 (Finance ministry), Persona 3 (Negotiating team), Persona 5 (Researcher)
  Verdict: PASS. Capability serves stated personas with appropriate confidence documentation.
  No kryptonite concerns. No user-facing regression. T3 confidence tier correctly declared.

### 3 — No open rejection artifacts

- [x] **Confirmed** — no rejection artifacts were filed for CM Sprint D deliverables.
  CM Sprint B §4.1 bounds rejection `[0.003, 0.050]` was a prior-sprint artifact, not a
  CM-D rejection. CM-D delivered the replacement certified bounds `[0.10135, 0.40540]`.

### 4 — North star test artifact

- [x] **Filed** — BPO acceptance comment (exit condition 1 above) contains the north star test artifact.
  Finance minister scenario named: Bolivian finance ministry analyst team preparing for a
  debt restructuring preparation session, evaluating whether the heterodox Kirchner 2003
  programme entry produced meaningfully different human development outcomes than continued
  IMF austerity conditioning through 2003.
  Concrete capability: ARG harness now measures `hd_composite` divergence at step 3 between
  baseline (continued austerity) and counter-factual (Kirchner heterodox entry). Certified
  bounds confirm the divergence is instrument-visible with T3 confidence. `per_step_diff[2] = 0.2027`.
  Without CM-D, step-3 divergence = 0 — the Demo 8 Act 2 ARG claim is unmeasurable.
  North star verdict: **PASS** (BPO attestation on record).

### 5 — PI Agent confirmation (this document)

- [x] All exit conditions 1–4 satisfied as of 2026-07-05
- [x] NM-084 §2.4 two-step gate satisfied — CM APPROVED comment on #1750 posted 2026-07-05
  before implementation PR opened (commit b632d61 filed intent+calibration decision; then
  42df495 opened implementation — correct ordering)
- [x] NM-094 test file presence check satisfied — `test_m19_cm_b_elasticity_calibration.py`
  present on `sprint/m19-cm-d` (inherited from `release/m19`)
- [x] NM-097 DATABASE_URL gate satisfied — `@pytest.mark.backtesting` guard present;
  CI ran backtesting job with `force_backtesting=true` via workflow_dispatch; observed
  `per_step_diff[2] = 0.2027` surfaced via `warnings.warn()` diagnostic in CI log
- [x] §2.3 intent document filed: `docs/process/intents/M19-CMD-2026-07-05-arg-kirchner-recovery-inputs.md`
- [x] §2.4 calibration decision filed: `docs/calibration/m19-cm-d-arg-kirchner-calibration-decision.md`
- [x] QA test authorship gate (§2.5) satisfied — test predates CM-D (CM Sprint B authorship);
  bounds recalibrated in PR #1755
- [x] Implementation PR #1755 merged to `sprint/m19-cm-d`; CI all-green
  (checks: `changes` ✓, `lint` ✓, `test-backend` ✓, `compliance-scan` ✓)
- [x] Issue #1750 closed

**PI Agent exit gate: PASS.** Sprint exit confirmed. Integration PR may open.

---

## Deliverable Summary

| Artifact | Location | Status |
|---|---|---|
| Intent document | `docs/process/intents/M19-CMD-2026-07-05-arg-kirchner-recovery-inputs.md` | Filed 2026-07-05 |
| Calibration decision | `docs/calibration/m19-cm-d-arg-kirchner-calibration-decision.md` | Filed 2026-07-05 (b632d61) |
| Sprint entry | `docs/process/sprint-plans/m19-cm-d-sprint-entry.md` | EL-approved 2026-07-05 |
| ARG fixture (n_steps=3) | `backend/tests/fixtures/argentina_2001_2002_scenario.py` | PR #1755 merged 2026-07-05 |
| AC-1 certified bounds | `backend/tests/test_m19_cm_b_elasticity_calibration.py` | PR #1755 merged 2026-07-05 |
| Backtesting snapshot test | `backend/tests/backtesting/test_argentina_2001_2002.py` | PR #1755 merged 2026-07-05 |
| ARG fixture unit test | `backend/tests/unit/test_argentina_backtesting_fixtures.py` | PR #1755 merged 2026-07-05 |
| CM certification | Issue #1750 comment (top of issue) | Posted 2026-07-05 |
| BPO acceptance | Issue #1750 comment #4887265239 | Posted 2026-07-05 |
| Customer Agent L3 | Issue #1750 comment #4887265845 | Posted 2026-07-05 |

---

## Forward Conditions

| Condition | Owner | Milestone |
|---|---|---|
| AC-1 harness live run: ARG `hd_composite` divergence at step index 2 ∈ [0.10135, 0.40540] (issue #1712) | CM / EL | Demo 8 Act 2 |
| Demo 8 Act 2 three-country verification (GRC, PAK, ARG all CLEARED) | EL | Demo 8 |

**Issue #1712 note:** The issue title references the old CM Sprint B bounds `[0.003, 0.050]`
(now superseded). Certified bounds from CM-D are `[0.10135, 0.40540]`. The issue body and
Demo 8 Act 2 verification should use the CM-D certified bounds. Issue #1712 closes when
the live DATABASE_URL harness run confirms `per_step_diff[2] ∈ [0.10135, 0.40540]`.

---

## CM Sprint Status After CM Sprint D

| Sprint | Issues | Status |
|---|---|---|
| CM Sprint A | GRC ELASTICITY_REGISTRY Euro area (#1623 Gap 1) | **Complete** — 2026-07-03 |
| CM Sprint B | LAC ELASTICITY_REGISTRY + ARG/GRC AC-1 scaffold (#1623 Gap 2) | **Complete** — 2026-07-04 |
| CM Sprint C | SEA ELASTICITY_REGISTRY PAK/LKA/BGD (#1623 Gap 3) | **Complete** — 2026-07-04 |
| CM Sprint D | ARG fixture n_steps=3 + AC-1 bounds recalibration (#1750) | **Complete** — 2026-07-05 |

All M19 CM sprints complete. ARG AC-1 forward condition is now empirically grounded.
Demo 8 Act 2 live harness verification (issue #1712) is the final remaining condition.

---

*Sprint exit confirmed: PI Agent, 2026-07-05.*
*Integration PR may open: `sprint/m19-cm-d → release/m19`.*
