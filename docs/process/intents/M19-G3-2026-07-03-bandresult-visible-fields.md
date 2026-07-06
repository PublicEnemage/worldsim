---
name: M19-G3-bandresult-visible-fields
type: implementation-intent
adr: ADR-007 Amendment 1 (ARCH-016) §8.6, §8.7
issues: "#1537"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-03
implementing-agent: Computation Engine Agent (backend schema + API); Frontend Architect Agent (CI label component)
sprint-entry: docs/process/sprint-plans/m19-g3-sprint-entry.md
---

# Implementation Intent: G3 — BandResult Visible Fields (#1537)

## 1. Source Issue and Architecture Authority

**Issue:** #1537 — feat(banding): BandResult visible fields — expose `band_method` and `is_meaningless` to frontend; update CI label display contract
**ADR prerequisite:** ADR-007 Amendment 1 (ARCH-016) — ACCEPTED 2026-07-03 — see `docs/adr/reviews/ADR-007-amendment-1-panel-review.md §EL Acceptance`
**Authored by:** PM Agent
**Date:** 2026-07-03
**Implementing agents:** Computation Engine Agent (BandResult schema + API serialisation); Frontend Architect Agent (CI label component)

**Architecture authority:**
ADR-007 Amendment 1 §8.6 (BandResult field additions) and §8.7 (display contract). `BandResult`
in `backend/app/simulation/banding_engine.py` gains three new fields. The API response for
`TrajectoryFrameworkPoint` gains `band_method`. The CI label component gains conditional rendering
per the four-state display contract below. Label text strings are delegated to G4 #1529 — G3 does
not hardcode label text.

**G4 coordination gate (§6.4 sprint entry):**
`band_method` enum values are frozen API from the moment this PR merges (ADR-007 §8.7 UX Concern 1).
G4 #1529 may not open its implementation PR until G3 #1537 is merged and the four enum values are
confirmed in the merged code. PM Agent notifies G4 when this PR merges.

---

## 2. BandResult Schema Changes

**File:** `backend/app/simulation/banding_engine.py`

Three new fields added to the `BandResult` frozen dataclass (additive — existing callers unaffected):

```python
@dataclass(frozen=True)
class BandResult:
    # Existing fields (unchanged):
    ci_lower: str | None
    ci_upper: str | None
    ci_coverage: float | None
    is_pre_calibration: bool | None
    clipped_lower: bool
    clipped_upper: bool
    # New fields (G3 #1537):
    band_method: str | None = None
    is_meaningless: bool = False
    suppressed_reason: str | None = None
```

**`band_method` enum values (frozen API — do not rename post-merge):**

| Value | When used |
|---|---|
| `"PRE_CALIBRATION_STRUCTURAL_PRIOR"` | No backtesting evidence; pure prior multipliers |
| `"PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL"` | ≥1 DIRECTION_ONLY case; no MAGNITUDE_MATCH |
| `"BAYESIAN_POSTERIOR_CALIBRATED"` | ≥1 MAGNITUDE_MATCH case; posterior multipliers accepted |
| `"SUPPRESSED_MEANINGLESS"` | §6 Condition 1 fires (meaninglessness threshold) |

G3 introduces all four values in the dataclass and API. G3 populates only the pure-prior state
(`"PRE_CALIBRATION_STRUCTURAL_PRIOR"`) in this PR — provisional and calibrated states are populated
by G3 #1543; suppressed state is populated by G3 #1536. However, all four values must be present
in the codebase and covered by at least one test in this PR because the API contract is frozen at
merge time.

**`is_meaningless` default:** `False` — set to `True` only when §6 Condition 1 fires (implemented in #1536).
**`suppressed_reason` default:** `None` — set by #1536 when suppression fires.

---

## 3. API Surface

**File:** `backend/app/schemas.py` (or equivalent response model)

`TrajectoryFrameworkPoint` (or the per-step response structure) must include:
- `band_method: str | None` — new field
- `is_meaningless: bool` — new field
- `suppressed_reason: str | None` — new field
- `is_pre_calibration: bool | None` — already present (M18); confirm it remains

`docs/schema/api_contracts.yml` must be updated in the same PR to reflect these additions.
NM-086 gate: E2E mock helpers for these fields must be verified against `api_contracts.yml`
before the implementation PR opens.

---

## 4. Display Contract — Four-State Table

*This table is the acceptance criterion for UX Designer Concern 3. It specifies what the CI
label component must render for each `band_method` state. Label text strings are G4 #1529's
concern; structural rendering obligations are G3's concern.*

| State | `band_method` | `is_pre_calibration` | CI band slot | Calibration status element |
|---|---|---|---|---|
| Pure prior | `"PRE_CALIBRATION_STRUCTURAL_PRIOR"` | `True` | CI bounds rendered normally | `data-testid="ci-calibration-status"` present; text delegated to G4 |
| Provisional | `"PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL"` | `True` | CI bounds rendered normally | `data-testid="ci-calibration-status"` present and **non-empty** (text delegated to G4; Demo 8 requires this element to be visible) |
| Calibrated | `"BAYESIAN_POSTERIOR_CALIBRATED"` | `False` | CI bounds rendered normally | `data-testid="ci-calibration-status"` present; text delegated to G4 |
| Suppressed | `"SUPPRESSED_MEANINGLESS"` | `None` | CI bounds **hidden**; slot shows exactly: `"Data range too wide for confidence interval"` | No calibration status element rendered |

**Demo 8 obligation (provisional state):** `"PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL"` is the
state Aicha encounters in Demo 8 Act 2. The `ci-calibration-status` element must be present and
non-empty or the north star test (ADR §8.10) conditional PASS becomes a FAIL. G4 #1529 provides
the text; G3 provides the element.

**Suppressed CI slot placeholder (UX Designer Concern 2):** The exact string is
`"Data range too wide for confidence interval"` — do not truncate or paraphrase.

---

## 5. Observable Application State

The implementation is complete when all of the following are true simultaneously:

**Backend state:**
- `BandResult` has three new fields with correct defaults
- `compute_band()` sets `band_method="PRE_CALIBRATION_STRUCTURAL_PRIOR"` on all non-suppressed returns
- API response for `GET /scenarios/{id}/trajectory` includes `band_method`, `is_meaningless`, `suppressed_reason` per framework point

**Frontend state:**
- CI label component reads `band_method` and `is_meaningless` from the API response
- `data-testid="ci-calibration-status"` element is present for all non-suppressed states
- Suppressed state hides CI bounds and shows "Data range too wide for confidence interval"

---

## 6. Acceptance Criteria

| ID | Criterion | Type |
|---|---|---|
| AC-01 | `BandResult` has `band_method`, `is_meaningless`, `suppressed_reason` fields with correct defaults | Unit test |
| AC-02 | `compute_band()` returns `band_method="PRE_CALIBRATION_STRUCTURAL_PRIOR"` for a normal T3 indicator | Unit test |
| AC-03 | API response for `/trajectory` includes `band_method` and `is_meaningless` per framework point | Integration test |
| AC-04 | CI label component renders `data-testid="ci-calibration-status"` for STRUCTURAL_PRIOR state | E2E / component test |
| AC-05 | CI label component renders `data-testid="ci-calibration-status"` (non-empty) for PROVISIONAL_DIRECTIONAL state | E2E / component test |
| AC-06 | CI label component renders `data-testid="ci-calibration-status"` for CALIBRATED state | E2E / component test |
| AC-07 | When `is_meaningless=True`, CI bounds are hidden and "Data range too wide for confidence interval" is shown | E2E / component test |
| AC-08 | All four `band_method` enum strings are present in the codebase and covered by at least one test | Unit test |
| AC-09 | `docs/schema/api_contracts.yml` updated to reflect new fields | Schema review |
| AC-10 | E2E mock helpers for new fields verified against `api_contracts.yml` (NM-086) | QA Lead checklist |

**NM-086 QA gate:** "Mock helpers verified against `docs/schema/api_contracts.yml §[trajectory endpoint]`?" must be confirmed before the implementation PR opens.

---

## 7. Process Gates

**CM pre-merge review gate (NM-084):** N/A — this issue is schema/API/frontend work, not
calibration methodology. CM review is not required for #1537.

**G4 coordination:** `band_method` enum values are not settled until this PR is merged.
G4 #1529 reads enum values from merged code, not from this intent document.

**UX Designer acceptance:** The display contract table in Section 4 must be reviewed by UX
Designer before the frontend PR merges. UX Designer posts ACCEPT on the issue before
auto-merge is set on the frontend portion.

---

## 8. Business PO Acceptance Conditions

| Condition | Verification |
|---|---|
| All four `band_method` states have defined UI treatment | AC-04 through AC-07 pass |
| Suppressed state shows exact placeholder text | AC-07 asserts exact string |
| Provisional state element is non-empty (Demo 8 readiness) | AC-05 asserts non-empty |
| G4 coordination gate satisfied | G4 #1529 PR opens only after this PR merges |
