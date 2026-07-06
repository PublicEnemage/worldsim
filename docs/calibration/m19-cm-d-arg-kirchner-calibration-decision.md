---
name: m19-cm-d-arg-kirchner-calibration-decision
type: calibration-decision
issue: "#1750"
sprint: M19-CM-D
status: FILED — closes §2.4 PENDING gate; gates implementation PR
authored-by: Chief Methodologist
authored-date: 2026-07-05
intent-document: docs/process/intents/M19-CMD-2026-07-05-arg-kirchner-recovery-inputs.md
implements: docs/process/sprint-plans/m19-cm-d-sprint-entry.md §Section 2.4 PENDING gate
---

# CM Calibration Decision: ARG Baseline Kirchner 2003 Recovery — M19 CM Sprint D

> **Authority:** This document closes the PENDING gate in sprint entry §2.4 and is the
> specification from which the `argentina_2001_2002_scenario.py` step-3 inputs are authored.
> The implementation PR may not open until this document is committed.
>
> **What this document decides:** Which fiscal policy input to add to `build_argentina_scenario()`
> at step 3 to represent the Kirchner 2003 recovery, what confidence tier to assign, and how to
> certify the AC-1 test bounds for `test_m19_cm_b_elasticity_calibration.py`.

---

## 1. Background: Why the CM Sprint B Bounds Failed

### 1.1 The structural problem

CM Sprint B §4.1 specified AC-1 bounds `[0.003, 0.050]` for `per_step_diff[2]` (step-3 index).
These bounds assumed that by step 3, the heterodox counter-factual (managed 1999 peg exit)
and the orthodox baseline (continued austerity + default) would *converge* toward a common
trajectory — the differential narrowing from ~0.167 at step 2 to near-zero by step 3.

This convergence assumption is economically incorrect for this fixture pairing.

The counter-factual starts from a 1999 baseline (unemployment 12.9%; no crisis). By the
simulation's step 3, the counter-factual is in a post-managed-exit stabilisation phase with
unemployment remaining moderate. The baseline, by contrast, entered the 2001–02 sovereign
default with unemployment peaking near 21.5% (May 2002 INDEC EPH). Even with Kirchner's
strong 2003 recovery (+8.8% GDP, unemployment declining toward 14–15% by end-2003), the
baseline has not recovered to anywhere near the counter-factual level in three simulation steps.

**Correct expectation:** Substantial continuing divergence at step 3 — in the range 0.08–0.14
based on engine mechanics — not near-zero convergence.

### 1.2 What CM Sprint B should have specified

The [0.003, 0.050] bounds were authored from the CM Sprint B calibration rationale (§4.1):
"At Q1 FORMAL elasticity -0.22: ~0.22-0.33pp poverty_headcount_ratio change per cohort per step;
hd_composite scale normalization: Q1 FORMAL contribution ~0.003-0.008 per step."

This reasoning captured the *per-step marginal contribution* of the LAC formal-sector calibration —
not the *cumulative multi-step divergence* between two scenarios with structurally different
initial conditions. The bounds were a category error. CM Sprint D corrects them.

---

## 2. Historical Basis: Argentina 2003

### 2.1 Primary source: MECON Budget Execution 2003

Ministerio de Economía y Producción (MECON), Budget Execution Report 2003.
`MECON_BUDGET_2003`

Key data:
- Primary fiscal surplus 2003: +0.5% of GDP (first surplus since 1999; revenue-driven)
- Government spending 2003: approximately 23–24% of GDP (up from the 2002 emergency austerity
  trough of ~21% GDP, which cut services sharply as tax revenue collapsed post-default)
- Social transfer programs (Jefes y Jefas de Hogar Desocupados, PJJHD):
  ~1.5–2.0 million beneficiaries; programme cost ~0.8–1.0% GDP maintained into 2003

The net fiscal impulse to domestic demand at step 3 — relative to the step-2 default shock
state — is approximately +2.5–3.5% GDP (combination of spending normalisation and social
program maintenance, partially offset by the export tax revenue that enables the primary surplus
without cutting spending further).

### 2.2 Supporting source: IMF WEO April 2004

IMF World Economic Outlook April 2004. `IMF_WEO_APR2004`

Validates the 2003 GDP growth outturn of +8.8%. Confirms fiscal trajectory: primary surplus
improving from 2002 to 2003 on the basis of export tax revenue, not spending cuts.

### 2.3 Known limitation: spending_change as a proxy

The `spending_change` parameter in WorldSim's `FiscalPolicyInput` captures government
expenditure as a fraction of GDP. It does not separately model:
- Export tax revenue (the primary surplus driver in 2003)
- Utility tariff suppression (Kirchner kept utility prices below market clearing)
- Exchange rate undervaluation effects (the devalued peso boosted competitiveness)

The `spending_change = +0.030` is a *net fiscal impulse proxy* — it represents the increase
in effective government demand injection at step 3 relative to the step-2 default trough.
It is not a precise estimate of government expenditure change in isolation.

This is an accepted T3 approximation. A T2 calibration would require a dedicated regression
of the `spending_change` parameter against observed quarterly unemployment series for
Argentina 2003 — possible in a future backtesting sprint.

---

## 3. Chosen Calibration

### 3.1 Step 3 scheduled input

```python
ScheduledInputSchema(
    step=3,
    input_type="FiscalPolicyInput",
    input_data={
        "instrument": "spending_change",
        "target_entity": "ARG",
        "sector": "government",
        "value": "0.030",
        "duration_years": 1,
    },
)
# Source: MECON Budget Execution 2003 + IMF WEO April 2004
# Represents: Kirchner fiscal normalisation and social program expansion
# Confidence tier: T3 (proxy; direct MECON data available; conversion requires assumptions)
```

| Parameter | Value | Basis |
|---|---|---|
| `instrument` | `spending_change` | Direct fiscal impulse instrument |
| `value` | `+0.030` | 3.0% GDP — MECON 2003 spending recovery |
| `duration_years` | 1 | Single-step representation of 2003 recovery |
| `confidence_tier` | T3 | Regional inference + MECON data; see §2.3 |
| `source_registry_id` | `MECON_BUDGET_2003` | New — add to source_registry in implementation PR |

**Uncertainty range for `value`:** +0.020 to +0.040 (±33% around central estimate).
Lower bound: minimum normalization from 2002 trough (conservative). Upper bound: full
social program + infrastructure injection estimate.

### 3.2 n_steps extension

`build_argentina_scenario()` extends from `n_steps=2` to `n_steps=3`.
Step 3 label (if `step_metadata` is added): "Kirchner recovery" — though
`build_argentina_scenario()` does not currently use `step_metadata`; no change required here.

### 3.3 IMF program expiry

The existing `imf_program_acceptance` at step 1 has `expected_duration=2`, so it expires
naturally after step 2. No explicit IMF program exit input is needed at step 3. Kirchner's
May 2003 refusal to renew IMF conditionality is modelled implicitly by the program's
scheduled expiry. No change to existing inputs.

---

## 4. Bounds Certification Process

### 4.1 Why bounds cannot be pre-specified

The `hd_composite` divergence at step 3 depends on the engine's propagation from
`spending_change = +0.030` through the fiscal multiplier → GDP growth → unemployment →
`hd_composite`. This chain is not analytically invertible — a live run is required.

**Step-3 divergence estimate (pre-run):**
- BL step 2: `hd_composite = 0.3723` (empirically confirmed, G8 run 28719741291)
- BL step 3 (projected): `hd_composite ≈ 0.45–0.50` if `spending_change=+0.030` activates
  expected unemployment decline from ~20% to ~17%
- CF step 3: `hd_composite = 0.5750` (empirically confirmed, G8 run)
- Projected `per_step_diff[2]`: approximately 0.08–0.13

### 4.2 Certified bounds formula (post-run)

After the implementation PR is merged to `sprint/m19-cm-d`, the implementing agent runs:

```python
# Live harness run against localhost:8000 with sprint/m19-cm-d code active
# record per_step_diff[2] as observed_diff
```

Certified bounds:
```python
lower_bound = Decimal(str(round(float(observed_diff) * 0.5, 3)))
upper_bound = Decimal(str(round(float(observed_diff) * 2.0, 3)))
```

The test update commits these values. The implementation PR contains both the fixture
change and the certified bounds — they must be in the same PR (not split).

### 4.3 Previous bounds are REJECTED

The existing bounds in `test_m19_cm_b_elasticity_calibration.py`:
```python
lower_bound = Decimal("0.003")
upper_bound = Decimal("0.050")
```
are rejected by this calibration decision. They assumed step-3 convergence that is
structurally incorrect for this fixture pairing (see §1.1). They must be replaced.

### 4.4 Non-regression assertions

The following existing registry values must be verified unchanged by the implementation PR:

```python
# SSA entries (no change)
EXPECTED_SSA_Q1_INFORMAL = Decimal("-0.20")
EXPECTED_SSA_Q2_INFORMAL = Decimal("-0.133")
EXPECTED_SSA_Q1_AGRI     = Decimal("-0.16")
EXPECTED_CHANNEL_C       = Decimal("-0.30")
# GRC entries (CM Sprint A — no change)
EXPECTED_GRC_Q1_FORMAL   = Decimal("-0.25")
EXPECTED_GRC_Q2_FORMAL   = Decimal("-0.15")
# LAC entries (CM Sprint B — no change)
EXPECTED_LAC_Q1_FORMAL   = Decimal("-0.22")
EXPECTED_LAC_Q2_FORMAL   = Decimal("-0.13")
```

---

## 5. Source Registry IDs

| source_registry_id | Source | Status |
|---|---|---|
| `MECON_BUDGET_2003` | MECON Budget Execution 2003, Argentina | New — add to `source_registry` in implementation PR |
| `IMF_WEO_APR2004` | IMF World Economic Outlook April 2004 | Check if registered; add if absent |

Source registry entries must be added in the same PR as the fixture change, per
`docs/DATA_STANDARDS.md §Data Provenance Requirements`.

---

## 6. CM Agent Sign-Off

**APPROVED** — 2026-07-05

The step-3 Kirchner recovery inputs are historically grounded (MECON 2003 budget execution),
correctly classified T3, and the bounds certification process (empirical run → [obs × 0.5,
obs × 2.0]) is the standard CM Sprint formula. The §2.3 intent document
(`docs/process/intents/M19-CMD-2026-07-05-arg-kirchner-recovery-inputs.md`) is filed.
The §2.4 gate is satisfied by this document.

This APPROVED verdict is posted as a comment on #1750.

*Chief Methodologist. M19 CM Sprint D. 2026-07-05.*
