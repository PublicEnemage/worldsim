---
name: M19-G3-meaninglessness-threshold
type: implementation-intent
adr: ADR-007 Amendment 1 (ARCH-016) §6 Implementation Clause
issues: "#1536"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-03
implementing-agent: Computation Engine Agent
sprint-entry: docs/process/sprint-plans/m19-g3-sprint-entry.md
---

# Implementation Intent: G3 — Meaninglessness Threshold (#1536)

## 1. Source Issue and Architecture Authority

**Issue:** #1536 — feat(banding): ADR-007 meaninglessness threshold — suppress T5 indicators at step 7+ producing [0,1] bands
**ADR prerequisite:** ADR-007 Amendment 1 (ARCH-016) §6 Implementation Clause — ACCEPTED 2026-07-03
**Authored by:** PM Agent
**Date:** 2026-07-03
**Implementing agent:** Computation Engine Agent

**Architecture authority:**
ADR-007 Amendment 1 appends an implementation clause to Section 6. Section 6's three conditions
are unchanged. This clause specifies how `compute_band()` detects Condition 1 and what it returns.
Condition 2 (CI spans MDA floor) and Condition 3 (comparison group < 3 countries) are out of scope.

**Dependency on #1537:**
This PR sets `is_meaningless=True` and `band_method="SUPPRESSED_MEANINGLESS"` — fields added by G3 #1537.
#1537 must merge to `sprint/m19-g3` before this PR opens, or both PRs must coordinate field additions.
If #1537 has not merged, include the field declarations here and coordinate with the #1537 agent.

---

## 2. Implementation Specification

**File:** `backend/app/simulation/banding_engine.py` — `compute_band()` function

### 2.1 — Detection Logic

After clipping raw CI to natural bounds, add this check before returning the normal BandResult:

```python
if clipped_lower and clipped_upper:
    ci_width = ci_upper_clipped - ci_lower_clipped
    natural_width = Decimal(str(natural_upper)) - Decimal(str(natural_lower))
    if ci_width == natural_width:
        return BandResult(
            ci_lower=None,
            ci_upper=None,
            ci_coverage=None,
            is_pre_calibration=None,
            clipped_lower=False,
            clipped_upper=False,
            band_method="SUPPRESSED_MEANINGLESS",
            is_meaningless=True,
            suppressed_reason=(
                f"CI spans full natural range "
                f"[{natural_lower}, {natural_upper}] — Condition 1"
            ),
        )
```

The check must occur **after** natural-bound clipping and **before** the normal BandResult return.
The `Decimal` comparison is exact — both bounds have already been clipped to natural limits.
Do not use float comparison here. `natural_upper` and `natural_lower` come from the existing
framework natural bounds mapping — do not hardcode [0, 1].

### 2.2 — When This Fires

For financial and human_development frameworks (natural range [0.0, 1.0]):

| Tier | Step | half_width | Fires for composite ∈ [0.4, 0.8]? |
|---|---|---|---|
| T5 | ≥ 7 | 1.50 | Yes — both bounds clip; CI = [0,1] |
| T4 | ≥ 7 | 1.00 | Only for composite = 0.5 exactly |
| T3 | ≥ 7 | 0.75 | No |

### 2.3 — What Does Not Change

- Conditions 2 and 3 are not implemented here
- Existing callers receiving `ci_lower=None` are already null-safe (M18)
- The new fields are additive with defaults; callers that do not read them are unaffected

---

## 3. Observable Application State

- T5, step 7, score 0.5: `compute_band()` returns `is_meaningless=True`, `ci_lower=None`, `band_method="SUPPRESSED_MEANINGLESS"`
- T3, step 7, score 0.5: `compute_band()` returns `is_meaningless=False` with normal bounds
- Existing banding_engine test suite remains green

---

## 4. Acceptance Criteria

| ID | Criterion | Type |
|---|---|---|
| AC-01 | T5, step 7, score 0.5: `is_meaningless=True`, `ci_lower=None`, `ci_upper=None` | Unit test |
| AC-02 | T5, step 7, score 0.5: `band_method == "SUPPRESSED_MEANINGLESS"` | Unit test |
| AC-03 | T5, step 7, score 0.5: `suppressed_reason` contains the framework natural range bounds | Unit test |
| AC-04 | T3, step 7, score 0.5: `is_meaningless=False` with normal ci_lower/ci_upper | Unit test |
| AC-05 | T5, step 6 (step < 7): suppression does NOT fire | Unit test |
| AC-06 | Only one bound clipping (not both): suppression does NOT fire | Unit test |
| AC-07 | Existing banding_engine tests remain green | CI gate |
| AC-08 | `compute_band()` check uses `Decimal` comparison, not float | Code review |

---

## 5. Process Gates

**CM pre-merge gate (NM-084):** N/A — deterministic detection clause, not calibration methodology.
CM review required for #1543, not #1536.

---

## 6. Business PO Acceptance Conditions

| Condition | Verification |
|---|---|
| Suppression fires for T5 at step 7+ in typical range | AC-01, AC-02, AC-03 |
| Suppression does not fire for T3 or T5 steps < 7 | AC-04, AC-05 |
| Partial-clip cases do not trigger suppression | AC-06 |
| Existing tests remain green | AC-07 |
