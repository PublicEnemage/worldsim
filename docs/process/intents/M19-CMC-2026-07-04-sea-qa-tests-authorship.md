---
name: M19-CMC-sea-qa-tests-authorship
type: test-authorship-intent
sprint: M19-CM-C
status: Filed
authored-by: Chief Methodologist
authored-date: 2026-07-04
calibration-decision: docs/calibration/m19-cm-c-sea-calibration-decision.md
implements: docs/process/sprint-plans/m19-cm-c-sprint-entry.md §Section 2.5
---

# Test Authorship Intent: M19 CM Sprint C QA Tests

> **Authority:** This document maps the CM calibration decision to the specific test
> assertions in `backend/tests/test_m19_cm_c_elasticity_calibration.py`. It is the
> test specification from which the implementation can be verified RED-before-GREEN.
> Closing §2.5: QA test file authored from this specification, committed to sprint branch
> before the implementation PR opens.

---

## 1. Test file location

`backend/tests/test_m19_cm_c_elasticity_calibration.py`

Follows the structure of:
- `backend/tests/test_m19_cm_a_elasticity_calibration.py` (CM Sprint A, GRC)
- `backend/tests/test_m19_cm_b_elasticity_calibration.py` (CM Sprint B, LAC)

---

## 2. Calibration constants mapped to assertions

| Constant | Value | Test(s) |
|---|---|---|
| SEA Q1 FORMAL elasticity | `Decimal("-0.17")` | `TestAC3SEAFormalEntryValues.test_sea_q1_formal_elasticity_value` |
| SEA Q2 FORMAL elasticity | `Decimal("-0.10")` | `TestAC3SEAFormalEntryValues.test_sea_q2_formal_elasticity_value` |
| Confidence tier (both) | `3` (T3) | `TestAC3SEAFormalEntryValues.test_sea_q1_formal_confidence_tier` |
| entity_families | `frozenset({"PAK","LKA","BGD"})` | `TestAC3SEAFormalEntryValues.test_sea_entries_entity_families_covers_all_three` |
| Q1 source ID | `ACADEMIC_LITERATURE_ILZETZKI_2013_FISCAL_MULTIPLIERS` | `TestAC3SEAFormalEntryValues.test_sea_q1_formal_source_registry_id` |
| Q2 source ID | `ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION` | `TestAC3SEAFormalEntryValues.test_sea_q2_formal_source_registry_id` |
| Q1 per-step delta (−0.015 shock) | `∈ [0.001, 0.004]` | `TestAC3SEADeltaUnitRange.test_sea_q1_formal_delta_within_range` |
| Q2 per-step delta (−0.015 shock) | `∈ [0.001, 0.003]` | `TestAC3SEADeltaUnitRange.test_sea_q2_formal_delta_within_range` |
| PAK Type B hd_composite step 2 | `∈ [0.002, 0.035]` | `TestAC1MagnitudeDivergence.test_pak_hd_composite_divergence_within_magnitude_bounds` |

---

## 3. RED/GREEN status before implementation

| Test class | RED before implementation | GREEN before implementation |
|---|---|---|
| `TestAC2SEAEntriesPresent` | 3 of 4 (presence checks) | 1 (entity_families field exists — CM Sprint A) |
| `TestAC3SEAFormalEntryValues` | All 6 | — |
| `TestAC3SEADeltaUnitRange` | All 3 | — |
| `TestAC4NonRegression` | — | All 9 (guards on prior entries) |
| `TestAC5CrossContaminationGuard` | — | All 4 (no SEA entries yet → no contamination) |
| `TestAC1MagnitudeDivergence` | 3 (DATABASE_URL gated) | — |

Estimated total: ~29 tests. Non-backtesting count: 26 (GREEN/RED unit tests). Backtesting: 3.

---

## 4. Non-regression scope

`TestAC4NonRegression` covers all CM Sprint B state entries (8 total) plus source IDs:

| Non-regression target | Expected value | Source |
|---|---|---|
| SSA Q1 INFORMAL | `-0.20` | Fosu 2011 (M17-G1) |
| SSA Q2 INFORMAL | `-0.133` | Ball 2013 scaling (M17-G1) |
| SSA Q1 AGRICULTURE | `-0.16` | IMF 2014 (M17-G1) |
| Channel C | `-0.30` | Iceland 2008 (ADR-020) |
| GRC Q1 FORMAL | `-0.25` | Blanchard & Leigh 2013 (CM Sprint A) |
| GRC Q2 FORMAL | `-0.15` | Ball 2013 scaling (CM Sprint A) |
| LAC Q1 FORMAL | `-0.22` | Lustig 2014 CEQ (CM Sprint B) |
| LAC Q2 FORMAL | `-0.13` | Ball 2013 scaling (CM Sprint B) |

Source IDs set (7 total — adds Lustig 2014 + Gasparini-Lustig 2011 from CM Sprint B).

---

## 5. Cross-contamination guard entities

`TestAC5CrossContaminationGuard` checks that elasticities `{"-0.17", "-0.10"}` do not appear
in any entity_families frozenset containing: `SEN`, `ZMB`, `GRC`, `ARG`.

---

## 6. Backtesting fixture reference

`TestAC1MagnitudeDivergence` uses:
- `backend/tests/fixtures/pakistan_2022_scenario.py`
- Functions: `build_pakistan_scenario()`, `build_pakistan_counterfactual_scenario()`
- Entity: `"PAK"`, `n_steps=4` (biannual; step index 2 = H2 2023)
- DATABASE_URL guard: NM-056 skip at fixture level only

---

*Test authorship intent authority: sprint entry §2.5 gate.
Sprint entry: `docs/process/sprint-plans/m19-cm-c-sprint-entry.md` (EL-approved 2026-07-04).
Author: Chief Methodologist. Date: 2026-07-04.*
