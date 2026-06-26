---
name: m17-g7-sprint-entry
type: sprint-entry
milestone: M17 — Calibration and Comparative Infrastructure
sprint-group: G7 — GovernanceModule Institutional Capacity Index
status: EL Approved 2026-06-26 — implementation may begin on #1275
authored-by: PM Agent
authored-date: 2026-06-26
el-approved: 2026-06-26
release-branch: release/m17
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M17, G7: GovernanceModule Institutional Capacity Index

**Status:** EL Approved 2026-06-26 — implementation may begin on #1275
**Date authored:** 2026-06-26
**Release branch:** `release/m17`
**Sprint plan:** `docs/process/sprint-plans/m17-sprint-plan.md` (EL Approved 2026-06-25)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G7 covers a single issue (#1275): seeding `institutional_capacity_index` for SEN and adding
the corresponding `fiscal_policy_spending_change` → `institutional_capacity_index`
GovernanceElasticity entry. Two changes co-gated in one PR. Implementation may not begin
until this entry is EL-approved.*

*Sprint classification: backend simulation enhancement with user-visible output in Zone 1D
governance indicators. BPO acceptance is required. Customer Agent Layer 3 assessment is
required (serves Persona 3 — Government Official/Finance Minister context).*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M17 — Calibration and Comparative Infrastructure |
| GitHub Milestone | #18 |
| Sprint group | G7 — GovernanceModule Institutional Capacity Index |
| Release branch | `release/m17` |
| Sprint plan document | `docs/process/sprint-plans/m17-sprint-plan.md` |
| Exit checklist issue | #982 |
| Sprint groups in scope | G7 only |
| Issues in scope | #1275 |
| ADR gate | N/A — elasticity entry addition within existing GovernanceModule architecture (ADR-005); no structural decision |
| Implementing agent | CM Agent (#1275 — elasticity entry is CM-owned parameter; backend implementation) |
| Wave | Wave 2 (Wave 1 exit confirmed 2026-06-25) |
| Demo dependency | Governance indicators visible in Zone 1D; present before Demo 7 live session (#843, M18) |
| Sequencing | G7 may begin after G6 exit confirmation (2026-06-26); no dependency on other Wave 2 groups |

**Issue classification summary:**

| Issue | Title | Classification | BPO acceptance required? |
|---|---|---|---|
| #1275 | feat(simulation): seed SEN institutional_capacity_index + GovernanceElasticity | Backend simulation enhancement — user-visible governance indicator behavior change | Yes — governance composite visible in Zone 1D; serves Persona 3 |

---

## Section 2 — Entry Invariants Checklist

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m17` cut from `main` 2026-06-25 (commit d806957)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at M17 kickoff 2026-06-25.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m17-sprint-plan.md`
  `el-approved: 2026-06-25`
- [x] **Wave 1 exit gate confirmed:** G1 sprint exit at `docs/process/sprint-plans/m17-g1-sprint-exit.md`;
  PI Agent confirmation 2026-06-25

**Structural gates: CLEAR.**

### 2.2 — ADR prerequisite gate

#1275 adds a fourth entry to `GOVERNANCE_ELASTICITY_REGISTRY` in the existing `elasticities.py`
file. The GovernanceModule architecture is governed by ADR-005 Decision 6 (elasticity registry
pattern). No new ADR is required for a registry entry addition within the existing pattern.

**ADR prerequisite status: CLEAR** — no new ADR required.

### 2.3 — Intent document gate

Intent document filed at:
`docs/process/intents/M17-G7-2026-06-26-governance-institutional-capacity-index.md`

Contains: all five acceptance criteria (AC-1275-1 through AC-1275-5 + AC-1275-R), CM-certified
parameter table, files-to-modify list, and silent failure mode description. QA Lead can write
integration tests from this document without reading implementation code.

**Intent document gate: SATISFIED.**

### 2.4 — QA / test gate

Tests required (from intent doc AC coverage):

| AC | Test type | File | Description |
|---|---|---|---|
| AC-1275-2 | Unit | `tests/unit/test_governance_module.py` | GOVERNANCE_ELASTICITY_REGISTRY contains new entry with CM values |
| AC-1275-3 | Unit | `tests/unit/test_m17_g7_governance_institutional_capacity.py` | SEN fixture contains institutional_capacity_index at 0.55 |
| AC-1275-4 | Integration | `tests/unit/test_m17_g7_governance_institutional_capacity.py` | GovernanceModule.compute() produces delta for institutional_capacity_index |
| AC-1275-R | Unit | `tests/unit/test_governance_module.py` | Existing registry entries unchanged |
| AC-1275-5 | Unit | `tests/unit/test_governance_module.py` | _INDICATOR_UNITS contains institutional_capacity_index |

Tests must be authored as a separate commit before the implementation commit (sprint entry
§2.4 gate). The tests will fail until implementation is complete — that is intentional.

**QA gate: SATISFIED** by intent doc acceptance criteria. Tests authored as first commit in the
implementation PR.

### 2.5 — UX / design gate

#1275 has no frontend changes. The governance indicator delta (institutional_capacity_index)
will be reflected in the governance composite score visible in Zone 1D through the existing
GovernanceModule → governance_indicator_update → composite score pathway. No new component,
no layout change, no UX/UI panel review required.

**UX gate: CLEAR** — backend-only change.

---

## Section 3 — Issue-by-Issue Implementation Scope

### #1275 — Seed SEN institutional_capacity_index + GovernanceElasticity

**Files to modify (co-gated — all changes in one PR):**

1. `backend/app/simulation/modules/governance/elasticities.py`
   - Add fourth `GovernanceElasticity` entry per CM spec (AC-1275-2)

2. `backend/app/simulation/modules/governance/module.py`
   - Add `"institutional_capacity_index": "ratio_0_1"` to `_INDICATOR_UNITS` (AC-1275-5)

3. `backend/alembic/versions/{new_rev}_m17_g7_gupta_2002_governance_capacity_seed.py`
   - New migration seeding Gupta 2002 in `source_registry` (AC-1275-1)
   - Migration revision: new head from `a3b5d7f9e2c1` (current head)

4. New test file: `backend/tests/unit/test_m17_g7_governance_institutional_capacity.py`
   - AC-1275-3 (SEN fixture seed value), AC-1275-4 (GovernanceModule delta), AC-1275-R (no regression)

5. Extend `backend/tests/unit/test_governance_module.py`
   - AC-1275-2 (registry entry check), AC-1275-5 (`_INDICATOR_UNITS` check)

**CM-certified parameters (not negotiable without CM sign-off):**
- `institutional_capacity_index` initial value for SEN: `"0.55"` (T2)
- Elasticity: `Decimal("-0.015")` (T3)
- Unit: `"ratio_0_1"` (CPIA normalized [0, 1])
- Source ID: `ACADEMIC_LITERATURE_GUPTA_2002_IMF_WP_INSTITUTIONAL_CAPACITY`

**Pre-push gate:** `cd backend && ruff check . && mypy app/` — mandatory.

**PR target:** `release/m17`

---

## Section 4 — Exit Conditions

G7 exits when:

1. PR merged to `release/m17` with CI green (test-backend + lint passing; backtesting green)
2. All five AC (AC-1275-1 through AC-1275-5 + AC-1275-R) verified in CI
3. Business PO acceptance (ACCEPT verdict) on record for #1275
4. Customer Agent Layer 3 assessment on record (governance indicator serves Persona 3)
5. North star test answered for the sprint: a Senegalese finance ministry analyst using
   WorldSim can now see that IMF-mandated social spending cuts produce institutional capacity
   degradation in the governance composite — not just fiscal stress
6. Issue #1275 closed
7. PI Agent sprint exit confirmation filed

---

*Intent document authority: CM specification (2026-06-25) filed as Wave 2 action item.
Intent document: `docs/process/intents/M17-G7-2026-06-26-governance-institutional-capacity-index.md`.
Implementing agent: CM Agent. Pre-push gate: backend ruff+mypy mandatory.*
