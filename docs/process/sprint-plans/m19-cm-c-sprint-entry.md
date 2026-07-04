---
name: m19-cm-c-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: CM Sprint C — South/Southeast Asia entity family calibration
status: Filed
authored-by: Chief Methodologist / PM Agent
authored-date: 2026-07-04
el-approved: 2026-07-04
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19 CM Sprint C: South/Southeast Asia Elasticity Calibration (#1623 Gap 3)

**Status:** EL-approved 2026-07-04 — implementation entry gate open; §2.4 calibration decision PENDING
**Date authored:** 2026-07-04
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
| Sprint number | CM Sprint C (post-CM-B; no active concurrent groups) |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md` |
| Exit checklist issue | #1535 |
| Sprint journal issue | #1700 |
| Sprint groups in scope | CM Sprint C (calibration-only sprint; no UI or API changes) |
| Wave coordination tier | Standard — no active sprint groups at CM-C entry; no file-area overlap with deferred #1657 (module.py vs elasticities.py) |
| Concurrent groups at entry | 1 (CM Sprint C only; #1657 DemographicModule fix may run concurrently — separate file area: module.py vs elasticities.py) |
| Cross-group dependencies | CM Sprint A (#1683) and CM Sprint B (#1698) integration PRs merged to `release/m19`; `entity_families` field and LAC FORMAL entries available. |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for this sprint.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` cut from `main` 2026-07-02 at 1bf1ecc
- [x] **CI trigger verified:** `.github/workflows/ci.yml` triggers on `release/m*` branches
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m19-sprint-plan.md` — EL-approved 2026-07-02

### 2.2 — ADR prerequisite gate

- [x] **N/A — no new ADR required.** CM Sprint C adds calibration constants to the ELASTICITY_REGISTRY
  using the `entity_families` scoping mechanism established in CM Sprint A. The DemographicModule
  architecture is unchanged (ADR-005 Decision 1 remains current).

### 2.3 — Intent document gate

- [x] **Intent document filed:**
  `docs/process/intents/M19-CMC-2026-07-04-sea-elasticity-calibration.md`
  Filed 2026-07-04 by Chief Methodologist.

### 2.4 — CM calibration PENDING gate

- [ ] **PENDING: CM calibration decision document filed.**
  `docs/calibration/m19-cm-c-sea-calibration-decision.md` — not yet filed.
  This document specifies:
  - Chosen entity families and entity IDs in scope (PAK/LKA/BGD confirmed; additional SEA
    entities such as THA, IDN, PHL subject to CM assessment)
  - Cohort targets (design question from intent §3 — Option a/b/c/d resolved)
  - Point estimate elasticities with uncertainty ranges
  - Confidence tier assignment
  - Source registry IDs (Batini et al. 2012 or equivalent South Asian literature)
  - MAGNITUDE bounds for AC-1 integration test (PAK Type B counter-factual step index TBD)
  The calibration decision document must be committed and referenced in this sprint entry
  (update §2.4 to checked) before QA test authorship may begin and before the implementation
  PR may open.

### 2.5 — QA test authorship gate

- [ ] **PENDING: QA test file committed to sprint branch before implementation PR opens.**
  File: `backend/tests/test_m19_cm_c_elasticity_calibration.py`
  Authored RED-before-implementation per §3.3. Must be present on sprint/m19-cm-c when
  the implementation PR targets that branch.

### 2.6 — NM-084 CM self-certification gate

- [ ] **PENDING: CM posts methodological certification comment on Issue #1623** before
  implementation PR auto-merge is set. Two-step mechanism:
  - Step 1: CM posts formal certification comment on Issue #1623 certifying chosen constants
    and source quality for Gap 3 South/Southeast Asian calibration.
  - Step 2: PI Agent posts gate comment on the implementation PR confirming CM cert is on record.
  Implementation PR auto-merge must not be set until Step 2 is complete.

---

## Section 3 — Scope Definition

### 3.1 — Issue scope

**Issue:** #1623 — ELASTICITY_REGISTRY non-SSA entity family calibration gap
**Gap covered:** Gap 3 — South and Southeast Asian programme countries
**Out of scope:** Additional SEA entities beyond PAK/LKA/BGD (THA, IDN, PHL — subject to
calibration decision; THA has a backtesting fixture from G2C but is not in the priority set
from #1623); Gap 3 entity set is PAK/LKA/BGD per issue spec.

### 3.2 — Entity families in scope

| Entity ID | Country | Crisis episode covered | Primary fixture |
|---|---|---|---|
| PAK | Pakistan | 2022–23 IMF programme (fiscal consolidation + energy subsidy removal) | `backend/tests/fixtures/pakistan_2022_scenario.py` (n_steps=4, biannual) |
| LKA | Sri Lanka | 2022 sovereign default + fuel crisis + IMF Extended Fund Facility | `backend/tests/fixtures/sri_lanka_2022_scenario.py` (n_steps=5, annual) |
| BGD | Bangladesh | Structural completeness; no primary M19 fixture | No M19 fixture (structural basis only) |

BGD is included in `entity_families` frozenset for structural completeness. Bangladesh's
calibration uses the same South Asian literature basis as PAK/LKA. Country-specific
backtesting fixtures for BGD are deferred beyond M19.

### 3.3 — Implementation specification (TBD — pending §2.4 calibration decision)

**Primary deliverable:** One or more new `CohortElasticity` entries in `ELASTICITY_REGISTRY`
at `backend/app/simulation/modules/demographic/elasticities.py`.

Entry structure (exact values TBD in calibration decision):

```python
# South Asian entries — design question (Option a/b/c/d) resolved in calibration decision
CohortElasticity(
    event_type="gdp_growth_change",
    cohort_spec=CohortSpec(IncomeQuintile.Q1, AgeBand.AGE_25_54, EmploymentSector.TBD),
    attribute_key="poverty_headcount_ratio",
    elasticity=Decimal("TBD"),
    source="TBD — Batini, Callegari & Melina (2012) or IMF REO Asia-Pacific equivalent",
    source_registry_id="ACADEMIC_LITERATURE_BATINI_2012_EMERGING_ASIA_MULTIPLIERS",
    confidence_tier=3,
    entity_families=frozenset({"PAK", "LKA", "BGD"}),
),
```

Exact values, sector scope, source strings, and number of entries are specified in the
calibration decision document. `entity_families=frozenset({"PAK","LKA","BGD"})` is
confirmed from #1623 Gap 3 scope. Confidence tier is T3 (cross-country South Asian
inference; T2 upgrade requires country-specific backtesting).

**Key calibration question (§3 intent):** Whether Option (a) FORMAL-only, Option (b)
INFORMAL-only, or mixed coverage is appropriate given PAK/LKA 2022 dual-channel transmission
(energy subsidy removal → formal sector; import compression/fuel shortage → informal sector).
This is the primary open question for the calibration decision.

**No module.py changes.** The entity_families filter was added in CM Sprint A. No further
changes to DemographicModule are required for CM Sprint C.

### 3.4 — QA test structure (to be authored after §2.4 PENDING gate clears)

Following CM Sprint A (`test_m19_cm_a_elasticity_calibration.py`) and CM Sprint B
(`test_m19_cm_b_elasticity_calibration.py`) test structure:

| Test class | Test count (est.) | Status |
|---|---|---|
| `TestAC2SEAEntriesPresent` | 3–4 | RED until implementation |
| `TestAC3SEAEntryValues` | 4–6 | RED until implementation |
| `TestAC3SEADeltaUnitRange` | 2–3 | RED until implementation |
| `TestAC4NonRegression` | 8 (SSA + Channel C + GRC + LAC all unchanged) | GREEN |
| `TestAC5CrossContaminationGuard` | 4 | GREEN (SEN/ZMB/GRC/ARG must not receive SEA entries) |
| `TestAC1MagnitudeDivergence` | 3 | `@pytest.mark.backtesting` — forward condition Demo 8 |

Estimated total: ~25 tests. Non-regression guards cover all prior entries (SSA M17-G1,
ADR-020 Channel C, GRC CM-A, LAC CM-B).

---

## Section 4 — Exit Conditions

The sprint exit gate passes when all of the following are satisfied:

1. **Business PO acceptance** recorded as a formal artifact (comment on Issue #1623 or
   dedicated review file) by @PublicEnemage (EL / Business PO).

2. **Customer Agent Layer 3 assessment** on record for CM Sprint C deliverable. CM Sprint C
   serves Persona 2 (finance ministry in programme country) and Persona 5 (researcher) —
   both require Layer 3 assessment.

3. **North star test artifact** filed as part of sprint exit document. The Pakistani or
   Sri Lankan finance ministry analyst scenario must be named specifically.

4. **PI Agent confirmation** that all exit conditions are satisfied, recorded as a gate
   comment on the sprint exit PR.

5. **Integration PR** `sprint/m19-cm-c → release/m19` auto-merged and confirmed.

6. **No open rejection artifacts** from Business PO or Customer Agent Layer 3.

---

## Section 5 — Branch Structure

| Branch | Purpose | Targets |
|---|---|---|
| `sprint/m19-cm-c` | Sprint sub-branch | `release/m19` (via integration PR at exit) |
| `feat/m19-cm-c-sprint-entry` | This document + intent doc | `sprint/m19-cm-c` |
| `feat/m19-cm-c-calibration-decision` | Calibration decision document | `sprint/m19-cm-c` |
| `feat/m19-cm-c-qa-tests` | QA test file (RED) | `sprint/m19-cm-c` |
| `feat/m19-cm-c-impl` | ELASTICITY_REGISTRY implementation | `sprint/m19-cm-c` |
| `feat/m19-cm-c-sprint-exit` | Sprint exit document | `sprint/m19-cm-c` |

---

*Sprint entry authored: Chief Methodologist / PM Agent, 2026-07-04.
EL approval required before §2.4 calibration decision PENDING gate may clear.
Implementation may not begin until §2.4, §2.5, and §2.6 gates are satisfied.*
