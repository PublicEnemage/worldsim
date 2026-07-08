---
name: M20-G4-precision-label-clarification
type: implementation-intent
adr: N/A — label clarification in existing constraint-floor result display (ADR-021 §D-4)
issues: "#1776, DEMO-234"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-08
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m20-g4-sprint-entry.md
---

# Implementation Intent: G4 — Binary Search Precision Label vs CI Label (#1776 / DEMO-234)

## 1. Source Issue and Architecture Authority

**Finding:** DEMO-234 High — Demo 8 Step 9 (Lucas Oliveira, Persona 1). Stakeholder Q1:
"Is the ±0.01 the same as the CI width?"

**Problem:** The constraint-floor result FOUND state displays:
- `constraint-boundary-value`: "fiscal multiplier ≥ 0.83"
- `constraint-tolerance-band`: "±0.00 precision" (derived from `uncertainty_hi - uncertainty_lo`)
- A gray note (10px, color #9ca3af): "This is the binary search precision, not a statistical
  confidence interval. Empirical CI bounds visible in the Zone 3 methodology panel."

The note already exists (added in prior implementation), but it is insufficiently prominent
and too small to read without deliberate attention at 1440×900. Lucas — an IMF Senior
Economist fluent in uncertainty quantification — immediately asked whether the ±0.01 is
the CI width. The gray note below the tolerance band did not prevent the question.

**Root cause:** Two distinct quantities are presented without adequate visual separation
and labeling:
1. **Binary search precision interval** — `[uncertainty_lo, uncertainty_hi]` — the range
   where the boundary lies (width ≤ `tolerance`, hardcoded 0.01). This is an algorithmic
   property, not a statistical estimate.
2. **Empirical CI on the indicator** — from the BandingEngine (e.g. 0.08 width on poverty
   headcount). This is the distributional uncertainty. Currently shown only in Zone 3.

The fix: make the label on `constraint-tolerance-band` unambiguous ("binary search
precision" not just "precision"), and make the CI-vs-precision distinction visible at
a glance without requiring the user to read a 10px note.

**Architecture authority:** `ControlPlaneColumn.tsx`, `constraint-search-found` section
(lines 816–871). No new ADR required — label and display enhancement within existing
four-state machine. The `SearchResult` type interface (lines 96–103) is not changed;
no new fields are added. If the CI width is shown inline, it is computed from existing
trajectory state (already available in `useScenarioStepStore`), not from a new API field.

**Authored by:** PM Agent  
**Date:** 2026-07-08  
**Implementing agent:** Frontend Architect Agent

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Persona 1 (Lucas Ferreira, IMF Senior Economist) — raised DEMO-234. Lucas
understands confidence intervals as statistical objects. Seeing "±0.01" next to a
boundary in a context that also has a CI raises an immediate "which one is this?"
question. He needs the distinction to be obvious, not buried in a footnote.

Secondary: Persona 2 (Eleni, Ministry of Finance analyst) — will cite the constraint
result in programme review submissions. If the ±0.01 could be mistaken for a statistical
CI, the citation is immediately challengeable by a technical reviewer.

**P-2 — Entry state:**
Mode 3 Active Control. Constraint-floor search FOUND. `constraint-search-found` is
visible. Lucas is reading the result, preparing to cite "0.83 ± 0.01" in a technical
note. He has not opened the Zone 3 methodology panel.

**P-3 — Journey step:**
Programme Review / Analytical Scrutiny. Lucas is verifying the precision claim before
the team uses the result in a negotiation argument. He needs to confirm ±0.01 is the
search precision, not the uncertainty on the poverty headcount estimate.

**P-4 — Time/interaction ceiling:**
Zero additional interaction — the distinction must be clear on first view of the FOUND
result. Opening Zone 3 to read the CI is not acceptable during live scrutiny. The
constraint result panel itself must carry the distinction.

**P-6 — Negotiating leverage delivered:**
Lucas can cite "boundary at 0.83, binary search precision ±0.01; the distributional CI
on poverty headcount is 0.08 wide (see trajectory panel)" in a technical note without
a colleague immediately asking "what does ±0.01 mean?"

**P-7 — North star capability delivered:**
A numerically literate IMF counterpart reviewing the constraint-floor result cannot
conflate binary search precision with distributional uncertainty — because the result
panel labels them distinctly without requiring the user to click into a methodology
panel to resolve the ambiguity.

---

## 3. Observable Application State

### 3.1 — Current state (to be changed)

```
data-testid="constraint-search-found"
  ├── "Safe boundary found:"
  ├── data-testid="constraint-boundary-value"     "fiscal multiplier ≥ 0.83"
  ├── data-testid="constraint-tolerance-band"     "±0.00 precision"
  ├── (evaluations + range line)
  └── (gray 10px note — insufficiently visible)
```

### 3.2 — Target state (after fix)

```
data-testid="constraint-search-found"
  ├── "Safe boundary found:"
  ├── data-testid="constraint-boundary-value"      "fiscal multiplier ≥ 0.83"
  ├── data-testid="constraint-search-precision"    "binary search precision: ±0.01"
  └── data-testid="constraint-precision-note"      "Not a statistical CI — see CI bands
                                                    in trajectory view"
      (or equivalent; see §4b)
```

**Key changes:**
1. `constraint-tolerance-band` is renamed `constraint-search-precision` and relabeled
   "binary search precision: ±X.XX" (explicit qualifier, not just "±X.XX precision").
2. The disambiguation note is promoted in visual hierarchy — it is readable at standard
   viewing distance at 1440×900 (≥ 11px, color ≥ #6b7280, not #9ca3af).
3. The note text references "trajectory view" or "CI bands" as the location of the
   distributional uncertainty — not "Zone 3 methodology panel" (an internal label Persona 1
   does not use).

**Note on CI display:** Showing the CI width inline (e.g. "poverty headcount CI: 0.08 wide")
is a SHOULD, not a MUST for this deliverable. If the implementing agent can derive the
relevant CI width from `useScenarioStepStore` trajectory state without a new API call,
it should be shown. If the computation is non-trivial, the note pointing to the trajectory
CI bands is sufficient for AC-3.

### 3.3 — Silent failure detection

**SF-1 (old testid still in place — test gap):** `constraint-tolerance-band` still
exists in the DOM under the old name. Detection: assert `constraint-tolerance-band`
is absent from `constraint-search-found` after the fix; assert `constraint-search-precision`
is present.

**SF-2 (note still 10px / #9ca3af — not promoted):** The disambiguation note was
promoted to ≥ 11px and ≥ #6b7280 color but reverted or not changed. Detection: assert
`constraint-precision-note` computed style `font-size ≥ 11px` and `color !== "#9ca3af"`.

**SF-3 (label still just "precision" without "binary search"):** The label text reads
"±0.01 precision" without the "binary search" qualifier. Detection: assert
`constraint-search-precision` text content contains "binary search".

---

## 4. Acceptance Criteria

**AC-1 (new testid — label present with correct qualifier):**
When `constraint-search-found` is visible, `data-testid="constraint-search-precision"`
is present and its text content contains the string `"binary search"`.

**AC-2 (old testid absent — renamed):**
`data-testid="constraint-tolerance-band"` is absent from `constraint-search-found`.
(Renamed to `constraint-search-precision`.)

**AC-3 (disambiguation note present and promoted):**
`data-testid="constraint-precision-note"` is present within `constraint-search-found`.
Its text content does NOT say "Zone 3 methodology panel" (internal label); it says
"trajectory view" or "CI bands" or equivalent user-facing language.

**AC-4 (note visual prominence — readable):**
The computed `font-size` of `constraint-precision-note` is ≥ 11px AND the computed
`color` is NOT `"rgb(156, 163, 175)"` (the old #9ca3af). The note is readable at
standard viewing distance without deliberate examination.

**AC-5 (boundary value unchanged — regression):**
`data-testid="constraint-boundary-value"` is present and unchanged (shows boundary
value in same format as before the fix).

**AC-6 (FOUND state otherwise unchanged — regression):**
The evaluations count and search range display are still present in `constraint-search-found`
after the label changes.

**AC-7 (SF-1 guard — old testid absent):**
Assert `data-testid="constraint-tolerance-band"` does NOT exist within
`constraint-search-found`.

**AC-8 (SF-2 guard — note color promoted):**
Assert `constraint-precision-note` computed color is NOT `#9ca3af` / `rgb(156, 163, 175)`.

**AC-9 (SF-3 guard — "binary search" in label):**
Assert `constraint-search-precision` text content contains the exact string `"binary search"`.

---

## 4b. Visual Spec (before/after)

**FOUND state (before):**
```
Viewport: 1440×900 | control-plane column | Mode 3 Active Control

✓ Safe boundary found:
fiscal multiplier ≥ 0.83          [constraint-boundary-value]
±0.00 precision                    [constraint-tolerance-band]  ← ambiguous
8 evaluations · [0.1, 3.0] searched
This is the binary search precision, not a statistical      ← 10px #9ca3af, invisible
confidence interval. Empirical CI bounds visible in
the Zone 3 methodology panel.
```

**FOUND state (after):**
```
Viewport: 1440×900 | control-plane column | Mode 3 Active Control

✓ Safe boundary found:
fiscal multiplier ≥ 0.83           [constraint-boundary-value]
binary search precision: ±0.01     [constraint-search-precision]  ← explicit qualifier
8 evaluations · [0.1, 3.0] searched
Not a statistical CI —             [constraint-precision-note]    ← ≥11px, ≥#6b7280
see CI bands in trajectory view
```

If CI width is available from trajectory state (SHOULD):
```
✓ Safe boundary found:
fiscal multiplier ≥ 0.83
binary search precision: ±0.01
Distributional CI (poverty headcount): 0.08 wide               ← OPTIONAL
8 evaluations · [0.1, 3.0] searched
Not a statistical CI — see CI bands in trajectory view
```

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for
Persona 1 to resolve the ambiguity in the Reactive entry state (zero interaction)?**

`[x]` No — "binary search precision: ±0.01" is self-describing to a numerically literate
audience. "Not a statistical CI — see CI bands in trajectory view" tells Lucas exactly
where to find the distributional uncertainty. No tooltip, no Zone 3 click, no specialist
explanation required.

**Rationale:** Persona 1 is an IMF Senior Economist. "Binary search precision" is a
term he understands. The note tells him where the CI is, which is what he needs to
complete his verification. Zero mediation required.

---

## 6. Out of Scope

- **CI width inline display:** If the implementing agent cannot derive CI width cleanly
  from existing store state, omitting the inline CI display is acceptable (AC-3 note is
  sufficient). Fetching a new API endpoint to display CI width is out of scope.
- **Tooltip on `constraint-search-precision`:** A tooltip explaining binary search
  precision is a future enhancement, not required for this deliverable. The label
  "binary search precision" is sufficient.
- **NOT_FOUND / ERROR state changes:** Unchanged.
- **Backend changes:** No backend changes required.
- **Renaming the `tolerance` field in the request body:** The API contract uses `tolerance`
  as the request parameter — unchanged. Only the display label changes.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent  
**Test authorship deadline:** Before any G4 implementation PR opens on `sprint/m20-g4`  
**Test file location:** `frontend/tests/e2e/m20-g4-precision-label.spec.ts`

**Required test coverage (Playwright E2E):**

- **AC-1:** Trigger FOUND result; assert `constraint-search-precision` present; assert
  text contains `"binary search"`.
- **AC-2:** Trigger FOUND result; assert `constraint-tolerance-band` absent from
  `constraint-search-found`.
- **AC-3:** Assert `constraint-precision-note` present; assert text does NOT contain
  `"Zone 3"` and DOES contain a user-facing reference to CI location.
- **AC-4:** Assert `constraint-precision-note` computed `font-size` ≥ 11px and color
  NOT `"rgb(156, 163, 175)"`.
- **AC-5 (regression):** Assert `constraint-boundary-value` present and unchanged.
- **AC-6 (regression):** Assert evaluations count and search range display still present.
- **AC-7 (SF-1 guard):** Assert `constraint-tolerance-band` absent. Write as a separate
  assertion block, not as a by-product of AC-2.
- **AC-8 (SF-2 guard):** Assert `constraint-precision-note` color promoted. Separate block.
- **AC-9 (SF-3 guard):** Assert `constraint-search-precision` text contains `"binary search"`.
  Separate block.

**QA Lead acknowledgment:**
`[ ]` QA Lead: Tests for AC-1 through AC-9 authored and filed before first implementation PR.

---

*Intent document version: 2026-07-08. Sprint entry: `docs/process/sprint-plans/m20-g4-sprint-entry.md`.
See `docs/process/agent-execution-lifecycle.md` for the five-step lifecycle this document gates.*
