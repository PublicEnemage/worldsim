---
name: m19-cm-b-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: CM Sprint B — LAC entity family calibration
status: Filed
authored-by: Chief Methodologist / PM Agent
authored-date: 2026-07-03
el-approved: 2026-07-03
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19 CM Sprint B: LAC Elasticity Calibration (#1623 Gap 2)

**Status:** EL-approved 2026-07-03 — implementation entry gate open; §2.4 calibration decision PENDING
**Date authored:** 2026-07-03
**Release branch:** `release/m19`
**Sprint plan:** `docs/process/sprint-plans/m19-sprint-plan.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
Changes to this template require PM Agent authorship and EL endorsement.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| GitHub Milestone | #21 |
| Sprint number | CM Sprint B (Wave 3 concurrent with G5 exit / post-G5) |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md` |
| Exit checklist issue | #1535 |
| Sprint groups in scope | CM Sprint B (calibration-only sprint; no UI or API changes) |
| Wave coordination tier | Standard — G5 integration PR #1684 auto-merge pending; CM Sprint B affects backend only (elasticities.py + tests). No file-area overlap with G5 frontend PRs. |
| Concurrent groups at entry | 1 (CM Sprint B only; #1657 DemographicModule fix may run concurrently — file-area is different: module.py vs elasticities.py — PM Agent monitors for conflict) |
| Cross-group dependencies | CM Sprint A integration PR #1683 merged to `release/m19` (2026-07-03) — entity_families field available. G5 integration PR #1684 pending auto-merge — no overlap. |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for this sprint.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` cut from `main` 2026-07-02 at 1bf1ecc
- [x] **CI trigger verified:** `.github/workflows/ci.yml` triggers on `release/m*` branches
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m19-sprint-plan.md` — EL-approved 2026-07-02

### 2.2 — ADR prerequisite gate

- [x] **N/A — no new ADR required.** CM Sprint B adds calibration constants to the ELASTICITY_REGISTRY
  using the `entity_families` scoping mechanism established in CM Sprint A. The DemographicModule
  architecture is unchanged (ADR-005 Decision 1 remains current).

### 2.3 — Intent document gate

- [x] **Intent document filed:**
  `docs/process/intents/M19-CMB-2026-07-03-lac-elasticity-calibration.md`
  Filed 2026-07-03 by Chief Methodologist.

### 2.4 — CM calibration PENDING gate

- [x] **CLEARED: CM calibration decision document filed.**
  `docs/calibration/m19-cm-b-lac-calibration-decision.md` — filed 2026-07-03.
  Decision: Option (a) FORMAL-only entries; Q1 FORMAL elasticity Decimal("-0.22") T3;
  Q2 FORMAL Decimal("-0.13") T3 (Ball 2013 0.60 scaling); entity_families=frozenset({"ARG","ECU","BOL","PER"});
  MAGNITUDE bounds: lower=0.003, upper=0.050 (ARG Type B, step index 2).

### 2.5 — QA test authorship gate

- [ ] **PENDING: QA test file committed to sprint branch before implementation PR opens.**
  File: `backend/tests/test_m19_cm_b_elasticity_calibration.py`
  Authored RED-before-implementation per §3.3. Must be present on sprint/m19-cm-b when
  the implementation PR targets that branch.
  (NM-094: PI Agent verifies test file presence before exit gate passes.)

### 2.6 — NM-084 CM self-certification gate

- [ ] **PENDING: CM posts methodological certification comment on Issue #1623** before
  implementation PR auto-merge is set. Two-step mechanism:
  - Step 1: CM posts formal certification comment on Issue #1623 certifying chosen constants
    and source quality for Gap 2 LAC calibration.
  - Step 2: PI Agent posts gate comment on the implementation PR confirming CM cert is on record.
  Implementation PR auto-merge must not be set until Step 2 is complete.

---

## Section 3 — Scope Definition

### 3.1 — Issue scope

**Issue:** #1623 — ELASTICITY_REGISTRY non-SSA entity family calibration gap
**Gap covered:** Gap 2 — Latin American and Caribbean (LAC) entity families
**Out of scope:** Gap 3 — South/Southeast Asia (deferred to CM Sprint C); Euro area additional
countries PRT/IRL/CYP (deferred; GRC coverage sufficient for Demo 8)

### 3.2 — Entity families in scope

| Entity ID | Country | Crisis episode covered | Primary fixture |
|---|---|---|---|
| ARG | Argentina | 2001–2002 currency/debt crisis | G2C #1548 counter-factual |
| ECU | Ecuador | 1999–2000 dollarization/banking crisis | backtesting/test_ecuador_1999_2000.py |
| BOL | Bolivia | 1985–90s structural adjustment | No M19 fixture (structural basis only) |
| PER | Peru | 1990–92 structural adjustment (Fujishock) | No M19 fixture (structural basis only) |

BOL and PER are included in `entity_families` frozenset for structural completeness. Their
calibration uses the same LAC literature basis as ARG/ECU. Country-specific backtesting
fixtures for BOL and PER are deferred beyond M19.

### 3.3 — Implementation specification

**Primary deliverable:** Two or more new `CohortElasticity` entries in `ELASTICITY_REGISTRY`
at `backend/app/simulation/modules/demographic/elasticities.py`:

```python
# LAC Q1 FORMAL — primary formal-sector poverty channel in LAC crisis episodes
CohortElasticity(
    event_type="gdp_growth_change",
    cohort_spec=CohortSpec(IncomeQuintile.Q1, AgeBand.AGE_25_54, EmploymentSector.FORMAL),
    attribute_key="poverty_headcount_ratio",
    elasticity=Decimal("TBD"),  # calibration decision doc §3.1
    source="TBD — Lustig (2017) CEQ + Gasparini & Lustig (2011)",
    source_registry_id="ACADEMIC_LITERATURE_LUSTIG_2017_CEQ_LAC_POVERTY",
    confidence_tier=3,
    entity_families=frozenset({"ARG", "ECU", "BOL", "PER"}),
),
# LAC Q2 FORMAL — Ball et al. (2013) scaling of Q1 FORMAL
CohortElasticity(
    event_type="gdp_growth_change",
    cohort_spec=CohortSpec(IncomeQuintile.Q2, AgeBand.AGE_25_54, EmploymentSector.FORMAL),
    attribute_key="poverty_headcount_ratio",
    elasticity=Decimal("TBD"),  # 0.60 × Q1 FORMAL per Ball et al. (2013)
    source="TBD — Ball et al. (2013) scaling",
    source_registry_id="ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION",
    confidence_tier=3,
    entity_families=frozenset({"ARG", "ECU", "BOL", "PER"}),
),
```

Exact values, source strings, and `confidence_tier` are specified in the calibration decision
document. The `ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION` source_registry_id is
already registered. A new `ACADEMIC_LITERATURE_LUSTIG_2017_CEQ_LAC_POVERTY` source registry
ID must be added to `source_registry` before or in the same PR as the implementation.

**No changes to existing entries.** SSA entries (entity_families=None) are unchanged.
GRC entries are unchanged. The non-regression tests verify this.

**No module.py changes.** The entity_families filter was added in CM Sprint A. No further
changes to DemographicModule are required for CM Sprint B.

### 3.4 — QA test structure (to be authored after §2.4 PENDING gate clears)

Following the CM Sprint A test structure at `backend/tests/test_m19_cm_a_elasticity_calibration.py`:

| Test class | Test count (est.) | Status |
|---|---|---|
| `TestAC2LACEntriesPresent` | 4 | RED until implementation |
| `TestAC3LACFormalEntryValues` | 6 | RED until implementation |
| `TestAC3LACDeltaUnitRange` | 3 | RED until implementation |
| `TestAC4NonRegression` | 6 | GREEN (non-regression assertions on all prior entries) |
| `TestAC5CrossContaminationGuard` | 3 | GREEN (SEN/GRC must not receive LAC entries) |
| `TestAC1MagnitudeDivergence` | 3 | `@pytest.mark.backtesting` — forward condition for Demo 8 |

Estimated total: ~25 tests. RED count ~13 (implementation-required). GREEN count ~12
(non-regression + cross-contamination; run before implementation).

---

## Section 4 — Exit Conditions

The sprint exit gate passes when all of the following are satisfied:

1. **Business PO acceptance** recorded as a formal artifact (comment on Issue #1623 or
   dedicated review file) by @PublicEnemage (EL / Business PO).

2. **Customer Agent Layer 3 assessment** on record for CM Sprint B deliverable. CM Sprint B
   serves Persona 2 (finance ministry in programme country) and Persona 5 (researcher) —
   both require Layer 3 assessment.

3. **North star test artifact** filed as part of sprint exit document. The Argentine or
   Bolivian/Peruvian finance ministry analyst scenario must be named specifically.

4. **PI Agent confirmation** that all exit conditions are satisfied, recorded as a gate
   comment on the sprint exit PR.

5. **Integration PR** `sprint/m19-cm-b → release/m19` auto-merged and confirmed.

6. **No open rejection artifacts** from Business PO or Customer Agent Layer 3.

---

## Section 5 — Branch Structure

| Branch | Purpose | Targets |
|---|---|---|
| `sprint/m19-cm-b` | Sprint sub-branch | `release/m19` (via integration PR at exit) |
| `feat/m19-cm-b-sprint-entry` | This document + intent doc | `sprint/m19-cm-b` |
| `feat/m19-cm-b-calibration-decision` | Calibration decision document | `sprint/m19-cm-b` |
| `feat/m19-cm-b-qa-tests` | QA test file (RED) | `sprint/m19-cm-b` |
| `feat/m19-cm-b-impl` | ELASTICITY_REGISTRY implementation | `sprint/m19-cm-b` |
| `feat/m19-cm-b-sprint-exit` | Sprint exit document | `sprint/m19-cm-b` |

---

*Sprint entry authored: Chief Methodologist / PM Agent, 2026-07-03.
EL approval required before §2.4 calibration decision PENDING gate may clear.
Implementation may not begin until §2.4, §2.5, and §2.6 gates are satisfied.*
