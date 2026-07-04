---
name: M19-G6-found-tolerance-band
type: implementation-intent
adr: ADR-021 §D-4 State 2 (FOUND state display)
issues: "#1709"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-04
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m19-g6-sprint-entry.md
---

# Implementation Intent: G6 — FOUND State Tolerance Band Display (#1709)

## 1. Source Issue and Architecture Authority

**Issue:** #1709 — FOUND state: tolerance band (±0.01) not displayed alongside constraint-floor boundary value
**ADR authority:** ADR-021 §D-4 State 2 — FOUND state display requirements
**Authored by:** PM Agent
**Date:** 2026-07-04
**Implementing agent:** Frontend Architect Agent

**Background:**
The constraint-floor search FOUND state currently renders the boundary value and the
precision band in the same `<div data-testid="constraint-boundary-value">` element:

```
fiscal multiplier ≥ 0.83 (±0.01)
```

Customer Agent Layer 3 assessment on #1540 (G1 exit, 2026-07-03) flagged that the
tolerance band visibility was "an unverified assumption" at G1 exit — there is no
separate `data-testid` on the tolerance portion, so no E2E assertion can target it
independently of the boundary value. This is the gap.

**Terminology clarification:** The issue description refers to a `tolerance` response
field. In practice, `tolerance` is a **request** parameter (convergence threshold,
default 0.01). The response contains `uncertainty_lo` and `uncertainty_hi` — the last
unsafe and first safe values from the binary search. The precision band width is
`uncertainty_hi - uncertainty_lo`, which is ≤ `tolerance` by definition when FOUND.
The intent uses "precision band" to describe `(uncertainty_hi - uncertainty_lo)`, and
"tolerance" as the label shown to users (consistent with current display language).

---

## 2. Scope

**What changes:**

**Deliverable A — Extract tolerance band into a separate, testable element**

`frontend/src/components/ControlPlaneColumn.tsx` — in the FOUND state block
(currently ~line 814–866):

Remove `(±{...})` from `data-testid="constraint-boundary-value"` and add a new
`<div data-testid="constraint-tolerance-band">` below it.

**Before (current):**
```tsx
<div
  data-testid="constraint-boundary-value"
  style={{ fontSize: 14, fontWeight: 700, color: TEAL, ... }}
>
  fiscal multiplier ≥ {searchResult.boundary?.toFixed(2)} (±{
    ((searchResult.uncertainty_hi ?? 0) - (searchResult.uncertainty_lo ?? 0)).toFixed(2)
  })
</div>
```

**After:**
```tsx
<div
  data-testid="constraint-boundary-value"
  style={{ fontSize: 14, fontWeight: 700, color: TEAL, ... }}
>
  fiscal multiplier ≥ {searchResult.boundary?.toFixed(2)}
</div>
<div
  data-testid="constraint-tolerance-band"
  style={{ fontSize: 11, color: "#6b7280", marginTop: 1 }}
>
  ±{((searchResult.uncertainty_hi ?? 0) - (searchResult.uncertainty_lo ?? 0)).toFixed(2)} precision
</div>
```

The precision band is rendered on its own line, smaller font (11px), muted gray
(`#6b7280`), immediately below the boundary value. This satisfies "visually distinct
from the boundary value" per #1709 acceptance criterion 2 — it is a separate labeled
element, not an inline suffix.

**What does NOT change:**
- The boundary value computation — `searchResult.boundary` is unchanged
- The precision band computation — still `uncertainty_hi - uncertainty_lo`
- The metadata line below (evaluations · search range) — unchanged
- The disclosure block (synthetic tier warnings) — unchanged
- All other search states (PENDING, NOT_FOUND, ERROR) — unchanged
- Any backend code

---

## 3. Acceptance Criteria

**AC-1 — Tolerance band element visible in FOUND state (primary)**

When the constraint-floor search result is FOUND, the element
`data-testid="constraint-tolerance-band"` is present in the DOM and visible in the
control plane column.

**Observable state:** `page.locator('[data-testid="constraint-tolerance-band"]').isVisible()` returns true in FOUND state.

**AC-2 — Tolerance band contains numeric precision value**

The tolerance band element contains a non-empty numeric string in the format `±N.NN precision` where `N.NN` is the result of `(uncertainty_hi - uncertainty_lo).toFixed(2)`.

**Observable state:** `page.locator('[data-testid="constraint-tolerance-band"]').textContent()` matches `/^±\d+\.\d{2} precision$/`.

**AC-3 — Tolerance band absent in non-FOUND states**

`data-testid="constraint-tolerance-band"` is absent from the DOM when the search
result is null, PENDING, NOT_FOUND, or ERROR.

**Observable state:** The testid element is not present when `searchResult` is null or has any status other than `"FOUND"`.

**AC-4 — Boundary value unmodified (non-regression)**

`data-testid="constraint-boundary-value"` still exists and still displays the boundary
number. After the change, the element's text content must match
`/fiscal multiplier ≥ \d+\.\d{2}$/` — it must NOT contain the `(±...)` suffix (which
moves to the tolerance band element).

**Observable state:** `constraint-boundary-value` text content no longer includes `(±`. The element still passes the existing AC-5 assertion.

**AC-5 — Visual distinction**

The tolerance band element is rendered as a separate line below the boundary value.
Confirmed by the `margin-top: 1` and block-level display of the tolerance band div.

---

## 4. File-Level Change Plan

| File | Change | Why |
|---|---|---|
| `frontend/src/components/ControlPlaneColumn.tsx` | Remove `(±...)` from `constraint-boundary-value` div; add `constraint-tolerance-band` div below | Deliverable A |
| `frontend/tests/e2e/m19-g1-constraint-floor.spec.ts` | Add AC-1/AC-2/AC-3 assertions on `constraint-tolerance-band` | QA gate |

**No new file required.** The E2E assertions are an addition to the existing
`m19-g1-constraint-floor.spec.ts` spec, which already sets up the FOUND state fixture.

**Implementing agent must first:**
1. Read `frontend/tests/e2e/m19-g1-constraint-floor.spec.ts` to locate the existing
   AC-5 assertion on `constraint-boundary-value` and confirm the FOUND-state test
   fixture setup
2. Verify the mock response used by the E2E spec includes `uncertainty_lo` and
   `uncertainty_hi` fields (NM-086 compliance — verify against `api_contracts.yml §constraint-floor-search response` before modifying the mock if needed)
3. Confirm that removing `(±...)` from `constraint-boundary-value` does not break
   the existing AC-5 text assertion — if AC-5 asserts the full string including `(±...)`,
   update AC-5 in the same PR

---

## 5. QA Notes (NM-086 compliance)

This deliverable introduces no new API calls and no new mock routes. The E2E spec
already mocks the `/constraint-floor-search` endpoint. The mock must include
`uncertainty_lo` and `uncertainty_hi` fields in the FOUND response — verify these
are present before adding assertions. If the mock uses a hardcoded object without
these fields, add them as part of this PR (e.g., `uncertainty_lo: 0.82`,
`uncertainty_hi: 0.83`).

**NM-086 check:** The constraint-floor endpoint mock shape must match
`api_contracts.yml §constraint-floor-search response` exactly. Verify before
modifying the mock.

---

## 6. Visual Spec (before / after)

**Before:**
```
Safe boundary found:
fiscal multiplier ≥ 0.83 (±0.01)         ← one element, boundary + tolerance fused
7 evaluations · [0.1, 3.0] searched
This is the binary search precision...
```

**After:**
```
Safe boundary found:
fiscal multiplier ≥ 0.83                  ← constraint-boundary-value (bold, teal, 14px)
±0.01 precision                           ← constraint-tolerance-band (muted, 11px)
7 evaluations · [0.1, 3.0] searched
This is the binary search precision...
```

The tolerance band is clearly separated from the boundary value. A user skimming the
panel can identify the boundary (bold teal) and the precision (smaller, gray)
independently. A Demo 8 audience member can see "0.83" as the actionable number and
"±0.01" as the precision qualifier without them visually competing.
