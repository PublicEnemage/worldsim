# REJECT-001 — Grounding Strip Missing Source Citations (AC-3 Fail)

**Date:** 2026-06-17
**Sprint group:** M14 G4 — ADR-016 Frontend
**Rejection author:** Business PO
**Step:** Step 5 (Validate)
**Resolution status:** Resolved — PR #1018 merged 2026-06-17; BPO re-validate PASS (intent doc §9); G4 sprint exit confirmed

---

## Source Intent Document

- **ADR reference:** ADR-016 — Scenario Grounding Architecture
- **Intent document path:** `docs/process/intents/M14-G4-2026-06-17-adr016-frontend.md`

---

## Which Acceptance Criterion Failed

**AC-3** — Grounding strip opens within 3s with at least one source citation.

> *Intent document §4 AC-3: "within 3 seconds `[data-testid="grounding-strip"]` is visible and contains at least one text node that includes a non-empty source institution name (e.g., 'CBJ', 'IMF BOP', 'World Bank')"*

---

## What the Observable Application State Actually Showed vs. What the Intent Specified

**Intent specification (§3.2 Secondary state A):**
> "Within 3 seconds of the click, the element contains at least one indicator row where a source citation is non-empty. The row format is: `[display_name]: [value] [unit]   [Source · Vintage · T{N}]`"

**Actual observed state (BPO Validate, 2026-06-17):**
```
FinancialGDP growth rate: 0.025 ratio · T2Trend growth rate: 0.03 ratio · T3Reserve coverage: 7.1 months · T2Human DevelopmentTotal population: 10101694 persons · T3Unemployment rate: 0.178 ratio · T2
```

The Grounding strip renders value and tier label only. Source institution (e.g., "CBJ") and vintage (e.g., "2023-Q4") are absent from every row. The P-6 negotiating leverage is not delivered: Persona 2 cannot cite "CBJ · 2023-Q4" from the strip.

**API verified:** `GET /api/v1/scenarios/68b31277-346e-45dc-9e1e-91e877f6b9fa/initial-state` returns `"source": "CBJ"` and `"vintage": "2023-Q4"` for `reserve_coverage_months`. Data is present at the API boundary.

---

## Gap Location: Intent or Implementation?

**Implementation gap** — the intent document correctly specifies the requirement (source institution names must appear). The implementation has a field name mismatch:

- The `/initial-state` API contract (`docs/schema/api_contracts.yml`) specifies field names **`source`** and **`vintage`** on each indicator object.
- `GroundingIndicator` in `frontend/src/types.ts` declares **`source_institution`** and **`data_vintage`** — the field names used by the *separate* `/data-quality` endpoint.
- `GroundingStrip.tsx` reads `ind.source_institution` and `ind.data_vintage`, both of which are `undefined` when the API response uses `source` and `vintage`.
- Result: `citation = ""` for every row; only the tier label is rendered.

**Why Step 4 Verify did not catch this:** The AC-3 E2E test for `[data-testid="grounding-strip"]` used a generic fallback regex `/[·•]\s*\S/` to detect "a citation-like token," which matched `· T2` (the tier label). The test did not assert that "CBJ" or "IMF" was present by string match before the regex fallback. Step 4 self-verification noted "CBJ citation present ✅" based on the E2E test result — the test passed but the assertion was too weak to detect the field name gap.

**Underlying root cause:** Intent document §7 (Test Authorship Obligation) specified the observable state correctly but did not identify the exact API field names the component must read. The QA test covered the cited intent description but relied on a regex that matched the tier separator (`·`) rather than the institution name.

---

## Required Review — Data Architect Agent

This defect involves an API contract field name discrepancy (`source`/`vintage` vs. `source_institution`/`data_vintage`). The Data Architect Agent holds R on `docs/schema/api_contracts.yml` and must review the following before the remediation fix is merged:

1. **Confirm the authoritative field names** for the `/initial-state` IndicatorObject are `source` and `vintage` (as specified in `api_contracts.yml §GET /scenarios/{id}/initial-state`).
2. **Confirm no schema drift** exists between the API contract and the actual backend serialisation in `backend/app/routers/scenarios.py` (or the initial-state endpoint file) — i.e., the endpoint actually serialises `source` and `vintage`, not `source_institution`/`data_vintage`.
3. **Confirm the `/data-quality` endpoint correctly uses `source_institution`/`data_vintage`** (as defined in `api_contracts.yml §GET /entities/{entity_id}/data-quality`) — these are the correct field names for that endpoint's `DataQualityFramework` object.
4. **If any contract update is required**, Data Architect updates `api_contracts.yml` in the same commit as the frontend fix.

Data Architect activation prompt: `Data Architect: REVIEW — G4 REJECT-001 field name discrepancy. /initial-state IndicatorObject uses source/vintage in contract; frontend GroundingIndicator type used source_institution/data_vintage. Confirm contract authority and verify no backend serialisation drift.`

*EL request: 2026-06-17 — Data Architect must be looped into this defect before remediation merge.*

---

## Remediation Scope

**What must change:**

1. **`frontend/src/types.ts` — `GroundingIndicator` interface:** Rename `source_institution` → `source` and `data_vintage` → `vintage` to match the `/initial-state` API contract field names.

2. **`frontend/src/components/GroundingStrip.tsx` — `IndicatorRow` component:** Update `ind.source_institution` → `ind.source` and `ind.data_vintage` → `ind.vintage`.

3. **`frontend/tests/e2e/m14-g4-adr016-frontend.spec.ts` — AC-3 test:** Remove or demote the generic regex fallback. The test must assert that the strip text includes at least one of "CBJ", "IMF", "World Bank", "V-Dem", "DOS" by string match — not only by regex character class. The generic regex was the mechanism that hid the field name gap from Step 4.

4. **Intent document `§8` update:** Note the field name gap and add a cross-reference to `api_contracts.yml §initial-state` confirming `source`/`vintage` are the authoritative field names for the `GroundingIndicator` type.

**Which step the implementing agent returns to:** Step 1 (Intent authorship re-examination for the field name contract gap) then Step 3 (code fix) then Step 4 (self-verify with string assertion, not regex) then Step 5 (BPO re-validate).

---

## Re-Acceptance Condition

BPO re-validates: with JOR scenario `68b31277-346e-45dc-9e1e-91e877f6b9fa` loaded and Grounding strip open, the strip text contains the string "CBJ" and "2023-Q4" (or equivalent source + vintage text). Both must be present by direct string assertion — not only by tier separator detection.

---

## Sprint Exit Block

This sprint group (G4) cannot close and no subsequent sprint group (G5+) may begin until:
- [x] The field name fix is applied (types.ts + GroundingStrip.tsx) — PR #1018 merged 2026-06-17
- [x] The AC-3 E2E test is strengthened (string assertion over regex fallback) — PR #1018; route mock + named-string assertion
- [x] BPO re-validates and issues ACCEPT — intent doc §9 BPO ACCEPT 2026-06-17

---

*Filed: 2026-06-17 by Business PO at Step 5 Validate. Near-miss: NM-045 (PI Agent to confirm). Implementing agent returns to Step 1 per CLAUDE.md §Agent Execution Lifecycle — When Verify or Validate Fails.*
