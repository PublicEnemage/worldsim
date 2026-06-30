---
name: M18-G7-D-data-pipeline-psp-hcl
type: implementation-intent
issues:
  - "#1461 — DEMO-132: psp-driver-row absent in all five demo frames"
  - "#1472 — DEMO-143: Human Cost Ledger bottom quintile em dash (missing indicator value)"
  - "DEMO-150 — Ecological framework shows em dash instead of 'Not modelled'"
status: Filed — no ADR gate; all gates CLEAR
authored-by: Frontend Architect Agent
authored-date: 2026-06-29
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m18-g7-sprint-entry.md
adr-reference: "None — mock fixture + display label fixes; no ADR impact"
root-cause-reference: docs/demo/m18/reviews/2026-06-29-g7-root-cause-analysis.md
release-branch: release/m18
bpo-acceptance-required: "No — data pipeline fixes restoring existing feature functionality"
customer-agent-l3-required: "No — fixes to existing G2 (psp-driver-row) and G3 (HCL) capabilities"
---

# Implementation Intent: M18-G7-D — Data Pipeline Fix (PSP Driver + HCL + Ecological)

> **Pre-implementation prerequisites (all required before implementation PR opens):**
> - [x] G7-0 root cause analysis filed and EL-approved (2026-06-29)
> - [x] No ADR gate (bug fixes in mock fixture and display bindings)
> - [ ] QA tests authored and committed (red) before implementation code

---

## 0. Implementation Constraints

*Authority: G7-0 root cause analysis §Root Cause 4.*

1. **PSP mock fix is in `demo-narrated.spec.ts`, not in production code.** The backend implementation is correct (`schemas.py:188`, `module.py:229`, `scenarios.py:2668`). The mock fixture in `makeAct1BaselineMock` and `makeAct1BranchMock` omits `psp_dominant_driver`. The fix is to add this field to the mock at all steps ≥ `BRANCH_FROM_STEP`.

2. **Verify `ScenarioInstrumentCluster` extraction path before adding mock field.** Root cause analysis §Root Cause 4 notes: "check whether `ScenarioInstrumentCluster`'s extraction path at line 641 matches the actual API response shape." The backend populates `psp_dominant_driver` from event metadata (see `scenarios.py:2652`). Verify the frontend reads from `entry.psp_dominant_driver` at the correct JSON path. If the path is wrong in the frontend, fix both the extraction path and the mock.

3. **DEMO-143 (HCL bottom quintile) — verify root cause before fixing.** The root cause analysis identifies two possible causes: (a) mock doesn't include `bottom_quintile_informal_workers_poverty_headcount` in `initial_attributes`; (b) backend fails to derive the cohort-level indicator from `poverty_headcount_ratio`. Determine which is the actual cause before writing the fix. Add the indicator to the fixture only if the backend derivation is working; fix the backend derivation if it isn't.

4. **DEMO-150 (Ecological "Not modelled") is a display fix only.** The ecological module is explicitly disabled in both SEN and ZMB scenario configurations. The fix is to render "Not modelled" instead of `—` when the ecological framework is disabled. This is a one-line display change — it does NOT enable the ecological module or add any ecological computation.

5. **NM-078 compliance — backend test file location.** Any new backend test files must be at `backend/tests/integration/`, not `backend/tests/` root. See `docs/process/near-miss-registry.md §NM-078`.

---

## 1. Source

**Issues:** #1461 (DEMO-132), #1472 (DEMO-143), DEMO-150

**Root cause document:** `docs/demo/m18/reviews/2026-06-29-g7-root-cause-analysis.md §Root Cause 4`

**Governing ADR:** None — mock fixture + display binding fixes. The PSP driver-row is a G2 (PR #1401) deliverable; the HCL is a G3 deliverable. Both are confirmed working in production backend. Fixes are to the mock fixture and frontend data binding only.

**Demo 7 anchor:**
- DEMO-132: `psp-driver-row` must be visible in Act 1 frames (Zone 1D). G2 delivered this feature — the mock simply doesn't model the field.
- DEMO-143: HCL bottom quintile must show numeric value (0.450), not `—`, in Act 1 frames.
- DEMO-150: Ecological framework cell must read "Not modelled" — `—` in a live external session looks like a rendering error, not an intentional design decision.

---

## 2. Persona Trace (abbreviated — data fix)

**Personas affected:** Persona 2 (Eleni — reads psp-driver-row and HCL value in Act 1); Persona 5 (Aicha — observes Zone 1D during demo).

**Capability before fix:** Zone 1D psp-driver-row is absent in all five demo frames (DEMO-132 CRITICAL — G2 feature not demonstrable). HCL bottom quintile shows `—` instead of 0.450 (DEMO-143 HIGH). Ecological cell shows `—` (DEMO-150 MEDIUM — looks broken).

**Capability after fix:** Zone 1D shows psp-driver-row with driver label (e.g., "Fiscal sustainability"). HCL shows 0.450 for informal workers. Ecological cell shows "Not modelled" with appropriate styling.

---

## 3. Observable Application State

### 3.1 Primary observable state

**In SEN Mode 3 Act 1, after branch from step 3, at step ≥ 3:**

`[data-testid="psp-driver-row"]` is present and visible within `[data-testid="zone-1d"]`. The row text includes a driver label string (e.g., "Fiscal sustainability", "Governance", "External balance", or "Social stability").

### 3.2 Secondary observable states

**State A — HCL bottom quintile value:**
`[data-testid="hcl-bottom-quintile-poverty"]` (or equivalent HCL indicator element) contains the text "0.450" (or the actual computed value for the step), not "—" or empty string.

**State B — Ecological "Not modelled":**
In Zone 1D or equivalent ecological display area, when `ecological.enabled === false` in scenario config, the ecological cell renders text "Not modelled" (not `—`, not null, not "0.00").

**State C — PSP driver absent before BRANCH_FROM_STEP:**
At steps < 3 (before branch), `psp-driver-row` may be absent or show "—" (driver is only populated after first PSP computation at branch step). This is acceptable — the mock only needs to include the field at steps ≥ BRANCH_FROM_STEP.

### 3.3 Silent failure detection

**Silent failure — psp-driver-row absent despite mock fix:**
Mock includes `psp_dominant_driver` but `psp-driver-row` still absent. Observable: check extraction path in `ScenarioInstrumentCluster.tsx` at line ~641. Possible cause: field is nested differently in the API response than the mock models.

**Silent failure — HCL still shows em dash:**
`poverty_headcount_ratio` is present in `initial_attributes` but backend does not derive `bottom_quintile_informal_workers_poverty_headcount`. If this is the case, fix is in the backend derivation, not the frontend.

---

## 4. Acceptance Criteria

**AC-D1 (E2E — psp-driver-row visible in Act 1 frames):**
In SEN Mode 3 with `makeAct1BranchMock` active at step 3 (BRANCH_FROM_STEP), `[data-testid="psp-driver-row"]` is present in the DOM within `[data-testid="zone-1d"]` (or equivalent Zone 1D container). The element's text content includes one of the four valid DRIVER_LABELS strings: "Fiscal sustainability", "Governance", "External balance", or "Social stability".
*Source: §3.1 + root cause analysis §Root Cause 4 §DEMO-132 §Fix*

**AC-D2 (unit — DRIVER_LABELS mapping exhaustive):**
`FourFrameworkZone1D.tsx` DRIVER_LABELS object includes all four valid `psp_dominant_driver` values as keys: `"fiscal_sustainability"`, `"governance"`, `"external_balance"`, `"social_stability"`. No key is missing. Adding a fifth driver value from the backend does not silently suppress the row — the component must log a warning if `psp_dominant_driver` is non-null but not in DRIVER_LABELS.
*Source: root cause analysis §Root Cause 4 §DEMO-132 — conditional render logic*

**AC-D3 (E2E — HCL bottom quintile shows numeric value):**
In SEN Mode 3 Act 1 at step 3 (baseline or branch), the element rendering the bottom quintile informal workers poverty headcount value does NOT contain "—" or empty string. It contains a decimal number (e.g., "0.450" or similar value ≥ 0.00).
*Source: §3.2 State A + root cause analysis §Root Cause 4 §DEMO-143 §Fix*

**AC-D4 (E2E — ecological "Not modelled"):**
In SEN Mode 3 and ZMB Mode 1/2 scenarios where `ecological.enabled === false`, the ecological framework display cell renders text "Not modelled" (case-insensitive match acceptable). The text "—" does NOT appear for the ecological framework in these scenarios.
*Source: §3.2 State B + DEMO-150 disposition (G7 Cluster D trivial fix)*

**AC-D5 (backend integration — psp_dominant_driver in trajectory response):**
`GET /scenarios/{id}/trajectory` response for the SEN Article IV scenario at step 3 (post-branch) includes `psp_dominant_driver` at the expected path in the response JSON. The value is one of the four valid driver strings. Test uses `backend/tests/integration/test_m18_g7_psp_hcl_fixture.py`.
*Source: §0 Constraint 2 + root cause analysis §Root Cause 4 §DEMO-132 §Fix (extraction path verification)*

---

## 5. Kryptonite Constraint Check

No kryptonite risk from this fix. The psp-driver-row is an existing Zone 1D element (G2 feature). The HCL indicator is an existing Zone 1B element. "Not modelled" is a display string replacement. No new interactions or affordances are introduced.

---

## 6. Backend / Mock Specification

### 6.1 — Mock fix: `makeAct1BaselineMock` and `makeAct1BranchMock`

In `frontend/tests/e2e/demo-narrated.spec.ts`, both mock builders must include `psp_dominant_driver` in the political_economy section of the trajectory response at all steps ≥ `BRANCH_FROM_STEP = 3`:

```typescript
// In makeAct1BaselineMock and makeAct1BranchMock — at each step >= BRANCH_FROM_STEP:
political_economy: {
  indicators: {
    programme_survival_probability: {
      value: "0.58",
      // ... existing fields ...
    }
  },
  psp_dominant_driver: "fiscal_sustainability"  // ADD THIS FIELD
}
```

The exact JSON path must match what `ScenarioInstrumentCluster.tsx` reads at line ~641. Verify the path against the actual backend response structure before setting it in the mock.

### 6.2 — Backend integration check for DEMO-143

Before writing the fix: run `GET /scenarios/{SEN_ID}/trajectory` against the test database and inspect the response for `bottom_quintile_informal_workers_poverty_headcount` at step 3. If the field is present: the fix is to add it to `initial_attributes` in `createSenScenario`. If absent: the fix is in the backend derivation layer (not the mock).

### 6.3 — Ecological "Not modelled" display fix

In the component rendering the ecological framework value (likely `FourFrameworkZone1D.tsx` or a shared framework display component): add a conditional check — when the ecological framework's `enabled` flag is `false` in the scenario config (or when the composite_score is null for all steps), render `"Not modelled"` instead of `"—"`.

---

## 7. Out of Scope

- Enabling the ecological module (backend computation — M19 scope)
- Adding ecological indicator data to SEN or ZMB scenarios (M19 scope)
- Changing the PSP driver decomposition backend logic (already correct)
- Any change to Zone 1D layout, ordering, or visual design beyond the driver label fix

---

## 8. Test Authorship Obligation

**QA files:**
- `frontend/tests/e2e/demo-narrated.spec.ts` — update mock fixtures (AC-D1)
- `backend/tests/integration/test_m18_g7_psp_hcl_fixture.py` — new file (AC-D5)
- `frontend/src/components/FourFrameworkZone1D.test.tsx` — unit test addition for DRIVER_LABELS (AC-D2)

**NM-078 compliance:** Backend test file MUST be at `backend/tests/integration/`, not `backend/tests/` root.

**Test authorship deadline:** All tests authored and committed to `feat/m18-g7-cluster-d` BEFORE implementation code changes.

| AC | Test type | Description |
|---|---|---|
| AC-D1 | E2E (mock) | `psp-driver-row` present after mock fix; driver label text visible |
| AC-D2 | Unit | DRIVER_LABELS has all 4 valid keys; warn on unknown driver |
| AC-D3 | E2E (mock) | HCL bottom quintile non-"—" |
| AC-D4 | E2E (mock) | Ecological "Not modelled" text |
| AC-D5 | Backend pytest | Trajectory response includes `psp_dominant_driver` at correct path |

**Pre-push gates:**
- Backend: `cd backend && source .venv/bin/activate && ruff check . && mypy app/` — both must exit 0
- Frontend: `cd frontend && npm run build` — must exit 0

*Filed: 2026-06-29. Authority: docs/process/agents.md §Frontend Architect Agent.*
