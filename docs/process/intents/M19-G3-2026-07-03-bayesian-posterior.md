---
name: M19-G3-bayesian-posterior
type: implementation-intent
adr: ADR-007 Amendment 1 (ARCH-016) §8.2–§8.5, §8.8
issues: "#1543"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-03
implementing-agent: Computation Engine Agent
sprint-entry: docs/process/sprint-plans/m19-g3-sprint-entry.md
---

# Implementation Intent: G3 — ADR-007 Bayesian Posterior Layer (#1543)

## 1. Source Issue and Architecture Authority

**Issue:** #1543 — feat(banding): ADR-007 Bayesian posterior layer — fit CI coverage multipliers to SEN/ZMB outcomes; is_pre_calibration=False gate
**ADR prerequisite:** ADR-007 Amendment 1 (ARCH-016) §8.2–§8.5, §8.8 — ACCEPTED 2026-07-03
**Authored by:** PM Agent
**Date:** 2026-07-03
**Implementing agent:** Computation Engine Agent

**Architecture authority:**
ADR-007 Amendment 1 Section 8. This PR implements: (1) MAGNITUDE_MATCH gate in
`_classify_fidelity()`, (2) coverage measurement and correction factor, (3) CalibrationStore
module-level dict with test override, and (4) calibration registry bootstrap (SEN entry,
DIRECTION_ONLY/EVIDENCE_INSUFFICIENT). The actual posterior multiplier update (when
MAGNITUDE_MATCH is eventually achieved) is a separate calibration registry event — not part
of this PR. `is_pre_calibration` remains `True` after this PR (SEN achieves DIRECTION_ONLY,
not MAGNITUDE_MATCH).

**CM pre-merge review gate (NM-084):**
CM must sign off on issue #1543 before auto-merge is set. Protocol: CE activates CM after
implementation → CM reviews MAGNITUDE_MATCH gate logic and correction factor formula →
CM posts sign-off on the issue → PI Agent posts gate comment on the PR → CE sets auto-merge.
Auto-merge must not be set before PI Agent gate comment.

---

## 2. Component 1 — MAGNITUDE_MATCH Gate in `_classify_fidelity()`

**File:** `backend/app/harness/mode3_harness.py`

### 2.1 — Interface Extension (CE Condition A)

`_classify_fidelity()` currently receives `per_step_records: list[dict]` with model output.
MAGNITUDE_MATCH requires historical reference values.

**Preferred resolution (Option 1):** Extend `per_step_records` dicts with a `"hist_value"` key.
When no historical value exists for a step, `"hist_value": None`. Confirm feasibility by reading
`run_harness()` and the `per_step_records` construction site before implementing.

**Fallback (Option 2):** Add `hist_values: dict[int, Decimal] | None = None` parameter to
`_classify_fidelity()`. Use only if Option 1 is not feasible. Document the choice in the PR
description. If Option 2 is chosen, activate CM for a 30-minute consultation (interface change).

### 2.2 — MAGNITUDE_MATCH Gate Logic (ADR §8.3)

```python
def _classify_fidelity(per_step_records: list[dict]) -> FidelityTier:
    # ... existing directional classification ...

    # MAGNITUDE_MATCH gate
    valid_pairs = [
        (r["model_value"], r["hist_value"])
        for r in per_step_records
        if r.get("hist_value") is not None and r.get("model_value") is not None
    ]
    if len(valid_pairs) < 5:
        return FidelityTier.DIRECTION_ONLY

    within_20pct = sum(
        1 for model_i, hist_i in valid_pairs
        if abs(model_i - hist_i) / max(abs(hist_i), Decimal("0.01")) <= Decimal("0.20")
    )
    coverage_frac = Decimal(within_20pct) / Decimal(len(valid_pairs))

    has_catastrophic = any(
        abs(model_i - hist_i) > 5 * abs(hist_i)
        for model_i, hist_i in valid_pairs
        if abs(hist_i) > Decimal("0.001")
    )
    if has_catastrophic:
        return FidelityTier.DIRECTION_ONLY

    if coverage_frac >= Decimal("0.50"):
        return FidelityTier.MAGNITUDE_MATCH
    return FidelityTier.DIRECTION_ONLY
```

DIRECTION_ONLY is the necessary precondition for MAGNITUDE_MATCH — run the directional check first.

---

## 3. Component 2 — Coverage Measurement and Correction Factor (ADR §8.2, §8.4)

**File:** `backend/app/simulation/banding_engine.py` or `backend/app/simulation/calibration.py`

```python
C_TARGET = Decimal("0.80")
CLAMP_MIN = Decimal("0.5")
CLAMP_MAX = Decimal("2.0")
C_MAG_FLOOR = Decimal("0.05")

def compute_magnitude_coverage(per_step_records: list[dict]) -> Decimal:
    pairs = [
        r for r in per_step_records
        if r.get("hist_value") is not None
        and r.get("ci_lower") is not None
        and r.get("ci_upper") is not None
    ]
    if not pairs:
        return Decimal("0")
    covered = sum(
        1 for r in pairs
        if Decimal(r["ci_lower"]) <= r["hist_value"] <= Decimal(r["ci_upper"])
    )
    return Decimal(covered) / Decimal(len(pairs))

def compute_correction_factor(c_mag: Decimal) -> tuple[Decimal, str]:
    if c_mag < C_MAG_FLOOR:
        return Decimal("1.0"), "EVIDENCE_INSUFFICIENT"
    raw_kappa = (C_TARGET / c_mag).sqrt()
    kappa = max(CLAMP_MIN, min(CLAMP_MAX, raw_kappa))
    return kappa, "OK"
```

---

## 4. Component 3 — CalibrationStore (CE Condition B)

**File:** `backend/app/simulation/banding_engine.py`

```python
_CALIBRATION_MULTIPLIERS: dict[int, Decimal] = {}

def set_calibration_multipliers(multipliers: dict[int, Decimal]) -> None:
    global _CALIBRATION_MULTIPLIERS
    _CALIBRATION_MULTIPLIERS = dict(multipliers)

def get_tier_multiplier(tier: int) -> Decimal:
    if tier in _CALIBRATION_MULTIPLIERS:
        return _CALIBRATION_MULTIPLIERS[tier]
    return STRUCTURAL_PRIOR_MULTIPLIERS[tier]
```

`compute_band()` calls `get_tier_multiplier(tier)` instead of reading from `TIER_MULTIPLIERS` directly.
Tests call `set_calibration_multipliers({3: Decimal("1.8")})` in setUp and `set_calibration_multipliers({})` in tearDown.

---

## 5. Calibration Registry Bootstrap

**File:** `docs/backtesting/calibration-registry.md` (create if absent; append-only thereafter)

The SEN case must be recorded as the first entry. SEN achieves DIRECTION_ONLY — no MAGNITUDE_MATCH —
so the structural prior is retained and `is_pre_calibration` remains `True`.

```markdown
## Entry CAL-001

| Field | Value |
|---|---|
| Case ID | SEN-2014-2019 |
| Fidelity tier achieved | DIRECTION_ONLY |
| Empirical C_mag (T3) | [computed from run — expected < 0.05] |
| Empirical C_dir (T3) | [computed from run] |
| Correction factor (T3) | EVIDENCE_INSUFFICIENT (C_mag < 0.05) |
| Posterior multiplier (T3) | N/A — structural prior retained |
| Provisional κ_prov (T3) | [computed from C_dir] |
| Calibration date | 2026-07-03 |
| Status | PROVISIONAL — DIRECTION_ONLY only; structural prior retained |
| affected_indicators_excluded | [external_sector_balance, export_volume] (CommodityShockConfig direction mismatch — #1541) |
| Architect sign-off | Pending |
| CM sign-off | Pending |
```

`affected_indicators_excluded` is required on every entry (empty list `[]` when no limitations).

---

## 6. Silent Failure Tests (ADR §8.8)

| Test | Assertion |
|---|---|
| Synthetic MAGNITUDE_MATCH | ≥5 within-20% steps → `FidelityTier.MAGNITUDE_MATCH` |
| Synthetic DIRECTION_ONLY | <50% within-20% steps → `FidelityTier.DIRECTION_ONLY` |
| CalibrationStore override | `set_calibration_multipliers({3: Decimal("1.8")})` → `get_tier_multiplier(3) == Decimal("1.8")` |
| EVIDENCE_INSUFFICIENT guard | `compute_correction_factor(Decimal("0.03"))` → `("1.0", "EVIDENCE_INSUFFICIENT")` |
| Catastrophic outlier | One step with `model_i = 10 × hist_i` → DIRECTION_ONLY |
| Minimum pairs guard | Fewer than 5 valid pairs → DIRECTION_ONLY |

---

## 7. Observable Application State

- A synthetic run with ≥5 within-20% steps returns `FidelityTier.MAGNITUDE_MATCH`
- A synthetic run with <50% within-20% steps returns `FidelityTier.DIRECTION_ONLY`
- `set_calibration_multipliers({3: Decimal("1.8")})` causes `compute_band()` to use `1.8` as T3 multiplier
- `docs/backtesting/calibration-registry.md` exists with CAL-001 SEN entry
- `is_pre_calibration=False` is not returned by any code path without an accepted registry entry

---

## 8. Acceptance Criteria

| ID | Criterion | Type |
|---|---|---|
| AC-01 | Synthetic MAGNITUDE_MATCH run → `FidelityTier.MAGNITUDE_MATCH` | Unit test |
| AC-02 | Synthetic DIRECTION_ONLY run → `FidelityTier.DIRECTION_ONLY` | Unit test |
| AC-03 | Catastrophic outlier (>5× hist) blocks MAGNITUDE_MATCH | Unit test |
| AC-04 | < 5 valid pairs → DIRECTION_ONLY regardless of coverage | Unit test |
| AC-05 | `compute_correction_factor(Decimal("0.03"))` → `EVIDENCE_INSUFFICIENT` | Unit test |
| AC-06 | `compute_correction_factor(Decimal("0.60"))` → kappa ∈ [0.5, 2.0] | Unit test |
| AC-07 | `set_calibration_multipliers()` overrides active multipliers in `compute_band()` | Unit test |
| AC-08 | `docs/backtesting/calibration-registry.md` exists with CAL-001 SEN entry | File check |
| AC-09 | SEN registry entry records `affected_indicators_excluded` list | Registry check |
| AC-10 | No code path returns `is_pre_calibration=False` without an accepted registry entry | Code review |
| AC-11 | CM sign-off posted on #1543 before auto-merge is set (NM-084) | Process gate |

---

## 9. Business PO Acceptance Conditions

| Condition | Verification |
|---|---|
| MAGNITUDE_MATCH gate implemented and testable | AC-01 through AC-04 |
| Correction factor formula matches ADR §8.4 | AC-05, AC-06 |
| CalibrationStore pattern allows test isolation | AC-07 |
| Calibration registry exists with SEN entry | AC-08, AC-09 |
| `is_pre_calibration=False` gate not bypassed | AC-10 |
| CM pre-merge review gate satisfied (NM-084) | AC-11 |

---

## 10. North Star Test (Sprint-Level)

*Authored by Business PO per CLAUDE.md §North Star Test (Process Gate).*

**Scenario:** Aicha, the Zambian finance ministry analyst, presents WorldSim CI bands to a
World Bank evaluator at a restructuring session (Demo 8 Act 2).

**Capability being evaluated:** G3 #1543 implements the MAGNITUDE_MATCH gate and CalibrationStore.
SEN and ZMB achieve DIRECTION_ONLY (expected from G2B). The system correctly classifies this and
the CI label surfaces `"PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL"`.

**Does this change what Aicha can argue at the table?**
Yes. Before G3, the challenge "Is this 80% interval calibrated?" has no answer. After G3,
Aicha can say: "The CI is in provisional calibration. Directional fidelity is confirmed from
Senegal and Zambia backtesting. The system classifies these as DIRECTION_ONLY — full magnitude
calibration is not yet available, and the band label says so. The next calibration target is a
MAGNITUDE_MATCH case." This is honest, specific, and defensible.

**Assessment:** PASS (for #1543 scope) — conditional on G3 #1537 (API surface) and G4 #1529
(label text) also landing before Demo 8. PI Agent tracks Demo 8 open condition until all three close.
