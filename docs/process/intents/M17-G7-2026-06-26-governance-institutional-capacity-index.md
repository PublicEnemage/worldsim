---
name: M17-G7-2026-06-26-governance-institutional-capacity-index
type: intent
issue: "#1275"
sprint: M17-G7
status: FILED 2026-06-26
authored-by: PM Agent
authored-date: 2026-06-26
cm-specification: docs/calibration/m17-g1-governance-sensitivity-specification.md §Question 2
---

# Intent: M17-G7 — GovernanceModule Institutional Capacity Index (#1275)

> Authority: CM Governance Sensitivity Specification §Question 2 (M17-G1 deliverable, filed
> 2026-06-25). All parameter values in this document are CM-specified; no implementing agent
> may deviate from them without CM sign-off.

---

## Deliverable Summary

Two co-gated backend changes in a single PR:

1. **Seed `institutional_capacity_index` for SEN** — World Bank CPIA 2023 normalized value
2. **Add GovernanceElasticity entry** — `fiscal_policy_spending_change` → `institutional_capacity_index`

Both must be in the same PR. An elasticity entry without the seeded indicator is a process
deviation (NM-class failure mode per issue #1275 body).

---

## Acceptance Criteria

### AC-1275-1 — Source registry: Gupta 2002 seeded

**Given** the migration runs  
**Then** `source_registry` contains a row with
`source_id = 'ACADEMIC_LITERATURE_GUPTA_2002_IMF_WP_INSTITUTIONAL_CAPACITY'`

### AC-1275-2 — GovernanceElasticity entry present with CM-certified values

**Given** the `GOVERNANCE_ELASTICITY_REGISTRY` in
`app/simulation/modules/governance/elasticities.py`  
**Then** it contains exactly one entry with:
- `event_type = "fiscal_policy_spending_change"`
- `indicator_key = "institutional_capacity_index"`
- `elasticity = Decimal("-0.015")`
- `confidence_tier = 3`
- `source_registry_id = "ACADEMIC_LITERATURE_GUPTA_2002_IMF_WP_INSTITUTIONAL_CAPACITY"`

### AC-1275-3 — `institutional_capacity_index` seeded in SEN backtesting fixture

**Given** `_SYNTHETIC_SEN_ATTRIBUTES` in the relevant backtesting fixture (at minimum the
governance integration test)  
**Then** it contains an `institutional_capacity_index` entry with:
- `value = "0.55"` (World Bank CPIA 2023 SEN score 3.3/6 normalized)
- `confidence_tier = 2`
- `measurement_framework = "governance"`

### AC-1275-4 — GovernanceModule responds to `fiscal_policy_spending_change` → `institutional_capacity_index`

**Given** a SEN simulation entity with `institutional_capacity_index = 0.55`  
**And** a `fiscal_policy_spending_change` event with magnitude `Decimal("-0.05")`  
**When** `GovernanceModule.compute()` runs on the next step (one-step lag design)  
**Then** the returned events include a `governance_indicator_update` event with:
- `affected_attributes["institutional_capacity_index"].value == Decimal("-0.05") * Decimal("-0.015")`
  = `Decimal("0.000750")`
- `affected_attributes["institutional_capacity_index"].measurement_framework == GOVERNANCE`

### AC-1275-R — Regression: existing elasticity entries unaffected

**Given** the existing three entries in `GOVERNANCE_ELASTICITY_REGISTRY`
(`gdp_growth_change → rule_of_law_percentile`, `emergency_policy_imf_program_acceptance →
democratic_quality_score`, `emergency_policy_emergency_declaration → democratic_quality_score`)  
**Then** their parameter values are unchanged after the new entry is added.

### AC-1275-5 — `institutional_capacity_index` unit registered in GovernanceModule

**Given** `_INDICATOR_UNITS` dict in `app/simulation/modules/governance/module.py`  
**Then** it contains `"institutional_capacity_index": "ratio_0_1"` (CPIA normalized [0, 1])

---

## CM-Certified Parameters

| Parameter | Value | Authority |
|---|---|---|
| SEN `institutional_capacity_index` initial value | `"0.55"` | World Bank CPIA 2023, score 3.3/6 normalized |
| SEN confidence tier | `2` | World Bank published score |
| Elasticity (`fiscal_policy_spending_change` → `institutional_capacity_index`) | `Decimal("-0.015")` | Gupta et al. 2002, Table 3, scaled to quarterly [0,1] |
| Elasticity confidence tier | `3` | SSA regional inference — T3 per DATA_STANDARDS.md |
| Source registry ID | `ACADEMIC_LITERATURE_GUPTA_2002_IMF_WP_INSTITUTIONAL_CAPACITY` | |
| Unit | `ratio_0_1` | CPIA normalized [0, 1] |

**Elasticity derivation:** Gupta et al. (2002, IMF WP/02/77) Table 3 — institutional
capacity under fiscal adjustment in SSA LICs. Point estimate −0.015 per 1pp fiscal
spending change, scaled to quarterly resolution and 0–1 index range (from normalized
CPIA score). T3: cross-country SSA panel; entity-specific upgrade to T2 requires
Senegal-specific time-series validation (deferred).

---

## Files to Modify

| File | Change |
|---|---|
| `backend/app/simulation/modules/governance/elasticities.py` | Add fourth `GovernanceElasticity` entry |
| `backend/app/simulation/modules/governance/module.py` | Add `"institutional_capacity_index": "ratio_0_1"` to `_INDICATOR_UNITS` |
| `backend/alembic/versions/{new_rev}_m17_g7_gupta_2002_governance_capacity_seed.py` | New migration: Gupta 2002 source_registry + SEN governance entity_data_quality_coverage |
| `backend/tests/unit/test_governance_module.py` | AC-1275-4 integration test (fiscal_policy_spending_change → institutional_capacity_index delta) |

**New test file (AC-1275-2/3/4):** `backend/tests/unit/test_m17_g7_governance_institutional_capacity.py`

---

## Pre-push Gate

`cd backend && ruff check . && mypy app/` — mandatory before any `git push` touching Python files.

---

## Silent Failure Mode

If `institutional_capacity_index` is not seeded in `initial_attributes`, the GovernanceModule
elasticity entry is present but produces no output — governance composite appears unaffected
by fiscal austerity. This is the same failure mode documented in issue #1275. The QA test
(AC-1275-4) detects this: if the indicator is absent, the elasticity fires but the delta has
nothing to accumulate against in `entity.attributes`, so the returned events list may be
empty or contain a zero-value delta.
