---
name: M17-G4-zone-1b-inverted-floor-label
type: implementation-intent
issues: "#1239"
status: Step 1 authored — QA tests may be authored immediately; implementation PR may open once tests are filed
authored-by: Frontend Architect Agent
authored-date: 2026-06-25
implementing-agent: Frontend Engineer
sprint-entry: "docs/process/sprint-plans/m17-g4-sprint-entry.md — EL Approved 2026-06-25"
adr-reference: "N/A — bug fix within ADR-017 Zone 1B boundary; no architectural decision required"
release-branch: release/m17
---

# Implementation Intent: M17-G4 — Zone 1B Inverted Floor Label (#1239)

> **Bug fix — no ADR, no UX visual spec.** The correct label semantics (below floor /
> above floor) are unambiguous from the defect description. The fix is a one-layer mapping
> omission in `ScenarioInstrumentCluster.tsx`. No visual design decision is required.
>
> **Sprint entry gate:** This document satisfies Step 1 of the agent execution lifecycle for
> #1239. QA Lead may author the `#1239` describe block in
> `frontend/tests/e2e/m17-g4-demo6-critical-polish.spec.ts` from this document alone,
> without reading implementation code. Implementation PR may open once both this intent
> document and the QA test are filed.
>
> **FA implementation sequence:** #1239 is the 4th issue in FA-recommended sequence
> (#1249 → #1253 → #1250 → #1239). Sequence applies to implementation ordering — this
> intent document may be filed immediately regardless of sequence position.

---

## 1. Source

**Issue:** #1239 — ux(zone-1b): DEMO6-010 inverted floor label — "above floor" when below

**ADR reference:** N/A — bug fix within ADR-017 Zone 1B boundary. `formatCohortDistance`
(the rendering function) and `CohortThresholdCrossing.breaches_below` (the field) were
both added in M16-G8 commit `6e8f618` but the mapping layer was not completed. This intent
document closes the gap.

**Authored by:** Frontend Architect Agent
**Date:** 2026-06-25
**Implementing agent:** Frontend Engineer

**Root cause (pre-implementation diagnosis):**

`ScenarioInstrumentCluster.tsx` parses raw API cohort threshold crossings into
`CohortThresholdCrossing` objects (lines 523–536). The `breaches_below` field — which
the backend sends as `true` for all current gte thresholds — is absent from both
`RawCohortThresholdCrossing` (the raw-parse interface) and the object literal mapping.
The result: `crossing.breaches_below` is always `undefined` in stored objects.

At the render site (`MDAAlertPanelZone1B.tsx` line 745):

```
formatCohortDistance(crossing.above_floor_pct, crossing.breaches_below !== false, isSad)
```

Since `undefined !== false` evaluates to `true`, `formatCohortDistance` currently renders
"X% below floor" for every cohort crossing — accidentally correct for all current gte
thresholds, but brittle: future lte thresholds (breach when value rises above a ceiling)
would display "X% below floor" incorrectly because `undefined !== false` never resolves to
`false` regardless of the backend value.

**The original DEMO6-010 bug** (before commit `6e8f618`): the render site was hardcoded to
`${crossing.above_floor_pct}% above floor` with no direction check, showing "above floor"
for every crossing regardless of breach direction. The M16-G8 partial fix corrected the
render logic but omitted the mapping layer — making the direction check structurally
unreachable from real API data.

**The fix:** Two changes in `ScenarioInstrumentCluster.tsx`:
1. Add `breaches_below?: boolean` to `RawCohortThresholdCrossing`
2. Add `breaches_below: c.breaches_below` to the `parsedCrossings` mapping

No changes required in `MDAAlertPanelZone1B.tsx` — `formatCohortDistance` is already
correct. No backend changes required — `breaches_below` is already in the API response.

---

## 2. Persona Trace Elements Targeted

> *Zone 1B cohort impact section serves analysts reading distributional floor-crossing
> data. The label "above floor" when the value is actually below the floor creates a
> misread risk at exactly the moment when the floor violation is most consequential.*

**P-1 — Persona served:** **Persona 2 — Finance Ministry Negotiator** (Aicha Mbaye
archetype, `docs/ux/personas.md §Persona 2`). Zone 1B presents the cohort-level threshold
crossing record — the evidence that Q1 informal sector poverty headcount has crossed below
the humanitarian safety floor. An analyst reading "X% above floor" when the crossing
records a below-floor breach receives an inverted signal at the highest-stakes moment in
the demo walkthrough.

Secondary: **Persona 1 — Ministry Analyst** (Lucas Ferreira) who reads Zone 1B crossing
rows to construct the human cost argument.

**P-2 — Entry state:** Reactive — Journey B Step 3 [Near-Term-Gap]. Zone 1B cohort impact
section is visible without interaction at all viewports in the primary instrument cluster.

**P-3 — Journey reference:** Journey B Step 3. The cohort crossing rows are the
distributional-consequence evidence used in the conditionality negotiation.

**P-4 — Time/interaction ceiling:** 90 seconds (Reactive entry state). Zone 1B must be
readable at glance level — the label is a one-line text element inside a cohort row that
the analyst reads without hover or click.

**P-6 — Negotiating leverage delivered (Persona 2):**
The cohort crossing row, with a correct "X% below floor" label, allows Persona 2 to state
the direction of the breach directly: "Q1 informal-sector poverty headcount is 3.5 percent
BELOW the humanitarian safety floor — not approaching it from above." The label direction
is the datum that distinguishes a floor breach from a floor approach.

**P-7 — North star capability delivered:**
After this fix, a Senegal finance ministry analyst reading Zone 1B cohort crossings in
the Demo 6 Senegal scenario can correctly identify that Q1 poverty headcount has breached
BELOW the floor — and cite the direction in a conditionality brief — without having to
correct the tool's output. The label is self-interpreting and semantically correct.

---

## 3. Observable Application State

> *All states are verifiable by an external observer using only the running application —
> no source code reading, no test reports, no implementation knowledge required.*

### 3.1 Primary observable state

Zone 1B cohort impact section, Senegal T3 conditionality scenario (or Greece backtesting
fixture), at any step where a Q1 cohort threshold crossing is displayed:

The text element at `data-testid="cohort-value-poverty_headcount_ratio"` (or the
corresponding `data-testid={`cohort-value-${indicator_key}`}` for any gte-threshold
indicator that has crossed below its MDA floor) reads **"X% below floor"** — where X is
the numeric distance. It does NOT read "X% above floor."

Observable confirmation without source code: load the Senegal T3 scenario (the same
scenario used in the Demo 6 walkthrough, `docs/demo/m16/stakeholder-walkthrough.md`),
step to the frame where Zone 1B shows cohort crossing rows, and read the distance label
in each cohort row. Every row for an indicator whose value is below its MDA floor must
show "below floor."

### 3.2 Secondary observable states

**State A — Approach text for above-floor indicators:**
For a `Zone1BAlert` in the approach state (value above the floor, not yet breached), the
`data-testid="detail-status"` element in `TopAlertDetail` displays "N% above floor at step
N" (Mode 1) or equivalent. This text is produced by `getDetailStatusText` which is not
affected by this fix — confirming the fix is isolated to cohort distance labels.

**State B — Regression guard on the floor-distance numeric display:**
The numeric distance displayed in the cohort row (the "X" in "X% below floor") is the same
value before and after the fix — only the direction label word changes ("above" → "below"
for gte threshold crossings). The numeric magnitude is unaffected.

**State C — Empty cohort section for above-floor steps:**
At any step where no cohort threshold crossings exist (all indicators are above their
respective floors), Zone 1B shows the `data-testid="cohort-empty-state"` element. The fix
must not cause phantom crossing rows to appear for above-floor indicators.

### 3.3 Silent failure detection

**Silent failure — direction check remains unreachable:**
If the mapping fix is applied to `RawCohortThresholdCrossing` but not to the
`parsedCrossings` object literal, or if `breaches_below` is mapped but with an incorrect
default (e.g., `breaches_below: c.breaches_below ?? false` instead of
`breaches_below: c.breaches_below`), then for the current gte-threshold scenarios the
label still shows "below floor" (accidentally correct via `undefined !== false = true`).
The silent failure surfaces only when a future lte threshold is introduced.

**Detection:** AC-1239-R verifies the label against the fixture scenario data that the
backend already sends `breaches_below: true` for. A Playwright test that reads
`cohort-value-{indicator_key}` and asserts "below floor" passes whether or not
`breaches_below` is correctly mapped — BECAUSE of the accidental `undefined !== false`
behavior. The QA Lead must include an **implementation completeness check**: after the
implementation PR is opened, the QA Lead verifies that `RawCohortThresholdCrossing` in
`ScenarioInstrumentCluster.tsx` includes `breaches_below?: boolean` and that the
`parsedCrossings` mapping includes `breaches_below: c.breaches_below`. This is a Step 4
Verify check, not an E2E assertion — it protects the fix from regression in a way the
E2E test cannot.

---

## 4. Acceptance Criteria

> *Criteria are written for the `#1239` describe block in
> `frontend/tests/e2e/m17-g4-demo6-critical-polish.spec.ts`.
> The QA Lead may author all three without reading implementation code.*

**AC-1239-1 (primary — below-floor label):**
In the Senegal T3 conditionality scenario (or Greece backtesting fixture — whichever the
QA Lead can load in the Playwright session), when Zone 1B displays a cohort threshold
crossing row for Q1 `poverty_headcount_ratio` at a step where that indicator's value has
crossed below its MDA floor, the element at
`data-testid="cohort-value-poverty_headcount_ratio"` contains the text "below floor"
and does NOT contain the text "above floor."

**AC-1239-2 (secondary — approach text not affected):**
In the same fixture scenario, when Zone 1B's `TopAlertDetail` area (`data-testid=
"zone-1b-top-detail"`) shows a status line (`data-testid="detail-status"`) for an alert
in the approach state (value above floor, `detail-approach-pct` reads "N% remaining"),
the `detail-status` element contains the text "above floor" (confirming `getDetailStatusText`
is unaffected by the fix and still correctly reports above-floor approach distance).

**AC-1239-R (regression — numeric magnitude unaffected):**
After the fix, the text of `data-testid="cohort-value-poverty_headcount_ratio"` matches
the regex `/^\d+(\.\d+)?% below floor$/` — the numeric prefix (X%) is a positive number,
confirming the floor-distance magnitude is preserved and not negated or zeroed by the fix.

---

## 4b. Visual Spec (before/after)

**AC-1239-1 (before — original DEMO6-010 bug, pre `6e8f618`):**
```
Viewport: 1280×800 | Zone: Zone 1B Cohort Impact | data-testid="cohort-value-poverty_headcount_ratio"
Senegal T3 conditionality scenario · Step 2 · Q1 Informal crossing row

  CRITICAL  Q1 Informal — poverty headcount ratio
            Threshold crossed at step 1 · 3.50% above floor · T3
                                          ^^^^^^^^^^^^^^^^^^^
                                          BUG: value is BELOW floor; label is inverted
```

**AC-1239-1 (after — correct):**
```
Viewport: 1280×800 | Zone: Zone 1B Cohort Impact | data-testid="cohort-value-poverty_headcount_ratio"
Senegal T3 conditionality scenario · Step 2 · Q1 Informal crossing row

  CRITICAL  Q1 Informal — poverty headcount ratio
            Threshold crossed at step 1 · 3.50% below floor · T3
                                          ^^^^^^^^^^^^^^^^^^^
                                          FIXED: "below floor" for gte threshold breach
```

**AC-1239-2 (approach text — unaffected; both before and after):**
```
Viewport: 1280×800 | Zone: Zone 1B Top Detail | data-testid="detail-status"
Greece backtesting fixture · Step where reserves_coverage_months is approaching

  detail-status: "12.3% above floor at step 4"
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                 This text is CORRECT and must remain unchanged — the value IS
                 above floor (approaching); this is not the bug surface.
```

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for
Persona 2 to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` **No.** The floor-distance label is a one-line text element ("3.5% below floor")
in a cohort row. It is self-interpreting: the direction word ("below" vs "above") and
the percentage magnitude are readable without specialist translation. The label appears
inline in Zone 1B without hover, tooltip, or interaction. No mediation is required.

---

## 6. Out of Scope

**lte threshold crossing direction (future):** All current MDA thresholds are gte (breach
when value falls below floor). The fix makes lte threshold direction correct when lte
thresholds are eventually introduced — but lte threshold testing is not in scope for #1239.
The fix is verified against existing gte threshold scenarios only.

**`getDetailStatusText` "above floor" text:** The `detail-status` element shows
"N% above floor at step N" for approaching (above-floor, not-yet-breached) alerts. This is
semantically correct for gte thresholds in the approach state and is NOT part of DEMO6-010.
AC-1239-2 verifies this text remains unchanged — it does not request its modification.

**`formatCohortDistance` unit tests:** Five Vitest unit tests were added in M16-G8 commit
`6e8f618` and remain valid. No new Vitest unit tests are required for this fix — the gap
is in mapping, not in the pure function.

**Backend schema change:** `CohortThresholdCrossing` in `backend/app/schemas.py` already
includes `breaches_below: bool` (added in M16-G8). No backend changes required.

**`above_floor_pct` field rename:** The field is named `above_floor_pct` in both the
backend schema and the API contract but represents the floor-distance magnitude (not
direction) when `breaches_below=True`. Renaming is a schema change beyond G4 scope. The
misleading name is documented here as a known technical debt item — it does not block
the label fix and must NOT be renamed in this PR without a separate schema change process.

**Zone 1B tablet legibility (#1250):** Separate G4 issue with its own UX visual spec
requirement and intent document. The #1239 fix must not introduce any new responsive
layout change that would require coordination with #1250.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent

**Test authorship deadline:** Before the #1239 implementation PR is opened against
`release/m17`. Per FA implementation sequence, #1239 is the last of four G4 issues
— the QA test for #1239 may be authored before #1249/#1253/#1250 are merged, as it
shares the same test file and is an independent describe block.

**Test file location:**
`frontend/tests/e2e/m17-g4-demo6-critical-polish.spec.ts`

The `#1239` describe block is added to the shared G4 E2E file. It is an independent
describe block and does not depend on any other G4 describe block to be present or green.

**Assertions required (from §4 ACs):**

- AC-1239-1: Playwright reads `data-testid="cohort-value-poverty_headcount_ratio"` text
  content; asserts text contains "below floor"; asserts text does NOT contain "above floor"
- AC-1239-2: Playwright reads `data-testid="detail-status"` text content for an
  approach-state alert; asserts text contains "above floor" (confirming no regression to
  `getDetailStatusText`)
- AC-1239-R: Playwright reads `data-testid="cohort-value-poverty_headcount_ratio"` and
  validates against `/^\d+(\.\d+)?% below floor$/` — confirming numeric magnitude is intact

**Implementation completeness check (Step 4 Verify — not an E2E assertion):**
After the implementation PR is opened, the implementing agent and QA Lead confirm:
- `RawCohortThresholdCrossing` in `frontend/src/components/ScenarioInstrumentCluster.tsx`
  includes `breaches_below?: boolean`
- The `parsedCrossings` mapping includes `breaches_below: c.breaches_below`

This check protects the fix from being accidental (the E2E tests pass without it due to
`undefined !== false = true`). It is recorded in the Step 4 Verify verdict before the PR
merges.

**No soft-skip patterns** (NM-056 guard): All three assertions must be hard-fail. No
`test.skip()`, `test.fixme()`, or conditional skips in the #1239 describe block.

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1239-1 through AC-1239-R authored and filed.
      Date: 2026-06-25
      File: `frontend/tests/e2e/m17-g4-demo6-critical-polish.spec.ts` — #1239 describe block

---

*Intent document authority: `docs/process/intent-template.md` (version 2026-06-17).
Sprint entry: `docs/process/sprint-plans/m17-g4-sprint-entry.md` (EL Approved 2026-06-25).
Implementing agent: Frontend Engineer. No ADR — bug fix within ADR-017 Zone 1B boundary.
Issue in scope: #1239 (Zone 1B inverted floor label).
Pre-push gate: `cd frontend && npm run build` — must exit 0 before #1239 implementation
branch is pushed. No backend changes; backend pre-push gate does not apply.*
