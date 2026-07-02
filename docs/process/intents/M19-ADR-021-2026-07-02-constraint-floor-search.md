---
name: M19-G1-constraint-floor-search
type: implementation-intent
adr: ADR-021 — Mode 3 Constraint-Floor Search
issues: "#1540, #1563, #1564"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-02
implementing-agent: Frontend Architect Agent (Form 3 frontend) + Computation Engine Agent (backend endpoint)
sprint-entry: docs/process/sprint-plans/m19-g1-sprint-entry.md
---

# Implementation Intent: G1 — Mode 3 Constraint-Floor Search (#1540)

## 1. Source ADR

**ADR:** ADR-021 — Mode 3 Constraint-Floor Search
**Status at time of authorship:** Accepted 2026-07-02 (@PublicEnemage).
**Authored by:** PM Agent
**Date:** 2026-07-02
**Implementing agents:** Frontend Architect Agent (Form 3 in `ControlPlaneColumn.tsx`);
Computation Engine Agent (`POST /scenarios/{id}/constraint-floor-search` endpoint and
binary search algorithm in `backend/app/simulation/`)

**Design authority:**
- ADR-021 §D-1 (Form 3 layout and color)
- ADR-021 §D-2 (endpoint contract)
- ADR-021 §D-3 (request/response schema)
- ADR-021 §D-4 (four result states)
- ADR-021 §D-5 (floor source from `monitored_focal_cohorts[0]`)
- ADR-021 §D-6 (relationship to ADR-019)
- ADR-021 §UX Implication Statement UX-1 through UX-7
- Pre-ship conditions: #1563 (AC-016 column visibility assertion), #1564 (MV-001 CVD three-way validation)

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou / Zambian ministry
analyst archetypes). Preparatory entry state: Eleni has completed Steps 1–5 of Journey A
and needs to know the parameter boundary before constructing the counter-proposal scenario.
Reactive entry state: Eleni is in the negotiation room and needs a specific boundary value
to cite within 90 seconds.

Secondary: Persona 5 — Stakeholder Observer (Aicha, World Bank evaluation team) observes
the boundary search as a demonstration of analytical capability at Demo 8.

**P-2 — Entry state:**
Two distinct entry states per ADR-021 §UX Implication Statement UX-3:

*Preparatory state:* All Journey A Steps 1–5 are complete. Eleni transitions from Mode 2
to Mode 3 with no Form 1 or Form 2 inputs applied. She runs the constraint search to
establish the boundary before constructing her counter-proposal in Mode 2 Step 6b.
Time ceiling: 15 seconds to boundary result (30-second HTTP timeout; result expected in
8–15 seconds at free-tier runner speeds).

*Reactive state:* Eleni is in the negotiation session with a tablet. The scenario is
preloaded (SCENARIO_PRELOADED or SCENARIO_COMPLETE). She has previously run a constraint
search during preparation. Time ceiling: 30 seconds to retrieve/cite the result. In the
Reactive state, Form 3 shows the last FOUND result — she is citing, not searching.

**P-3 — Journey reference:**
Journey A Step 6a (Mode 2→Mode 3→Form 3→Mode 2 boundary-establishment sub-workflow,
documented in `docs/ux/user-journeys.md §Journey A Step 6a`, updated 2026-07-02).
Journey B Step 5 (Reactive state — cite the boundary at the table via Mode 3 / control
plane panel).
Journey C Steps 1–4 (Mode 3 entry and Form 3 as complement to Forms 1 and 2).

**P-4 — Time/interaction ceiling:**
Preparatory ceiling: 15 seconds from "Find safe boundary" click to FOUND/NOT_FOUND result.
30-second HTTP timeout is the hard ceiling; if backend exceeds 30s, ERROR state renders.
Reactive ceiling: instantaneous (last result is already visible in Form 3 from preparation).

**P-5 — Data tier requirement:**
Minimum Tier 2 (estimated comparable). At Tier 3 (SYNTHETIC_COMPARABLE), the result
renders with "synthetic" disclosure (per UX-5 in ADR-021). At Tier 4+, the search does
not run and Form 3 shows `data-testid="constraint-search-structural-absence"`.

**P-6 — Negotiating leverage delivered:**
The Zambian finance ministry analyst can state "fiscal multiplier ≥ 1.18" at the IMF
table — the same boundary precision that the IMF's internal sovereign risk models can
produce. The ministry did not need a proprietary DSGE model or Bloomberg terminal.
The boundary is derived from the same simulation engine, the same calibration data, and
the same uncertainty framework. The asymmetry this closes: sophisticated creditor teams
can compute safe operating parameter ranges in minutes; this was not available to the
ministry side without WorldSim.

**P-7 — North star capability delivered:**
At Demo 8 Act 1: Eleni enters "0.40" (poverty headcount floor, bottom quintile) into
`monitored_focal_cohorts` config, clicks "Find safe boundary," and within 15 seconds
Form 3 shows "fiscal multiplier ≥ 1.18 (±0.01) | 9 evaluations | [0.1, 3.0] searched."
She cites this number directly to the IMF representative. The representative, who knows
from internal models that the safe boundary is approximately 1.15–1.20, is working from
the same number. The analytical asymmetry is closed for this moment.

---

## 3. Observable Application State

### 3.1 Primary observable state — Form 3 in ControlPlaneColumn

In Mode 3 (`data-testid="mode-3-active"` present on the instrument cluster), with
`monitored_focal_cohorts` configured and containing at least one entry with a valid
`floor_value`, the `ControlPlaneColumn` renders three form sections:

1. Form 1 (POLICY INSTRUMENTS, blue header — ADR-019 §D-3)
2. Form 2 (SCENARIO SHOCKS, orange header — ADR-019 §D-3)
3. Form 3 (CONSTRAINT SEARCH, teal header `#0d9488` — ADR-021 §D-1)

Form 3 contains:
- `data-testid="constraint-search-section"` (the section container)
- `data-testid="constraint-floor-label"` — text: the indicator key and floor value from
  `monitored_focal_cohorts[0]`, e.g., "bottom_quintile_informal_workers_poverty_headcount ≥ 0.40"
- `data-testid="constraint-floor-value"` — numeric: the floor value (e.g., "0.40")
- `data-testid="constraint-search-btn"` — button: "Find safe boundary"

When `monitored_focal_cohorts` is empty or not configured, Form 3 renders
`data-testid="constraint-search-unavailable"` instead of the search button.

### 3.2 Post-search observable states

After "Find safe boundary" is clicked, `data-testid="constraint-search-result"` is
always present and contains one of four states:

**PENDING:** `data-testid="constraint-search-pending"` — spinner visible; button disabled.

**FOUND:** `data-testid="constraint-search-found"` present.
- `data-testid="constraint-boundary-value"` — text: "fiscal multiplier ≥ 1.18 (±0.01)"
- Supporting line: "{N} evaluations · [{lo}, {hi}] searched"
- If Tier 3 synthetic: additional line containing the word "synthetic"

**NOT_FOUND:** `data-testid="constraint-search-not-found"` present.
- Message: no boundary found within the search range

**ERROR:** `data-testid="constraint-search-error"` present.
- Message: search failed; retry suggested; includes the error reason if available

### 3.3 Silent failure detection

**SF-1 (blank result on ERROR):** Backend returns `status: "ERROR"` but frontend renders
nothing in `constraint-search-result`. Detection: after clicking "Find safe boundary"
with a misconfigured focal cohort (no `floor_value`), assert that
`data-testid="constraint-search-result"` renders one of the four states — not a blank.

**SF-2 (incorrect boundary on partial evaluation):** Backend swallows an exception on one
internal binary search step and returns a boundary derived from partial results.
Detection: in the backend unit test, assert that if `run_trajectory` raises `ValueError`
on any evaluation, the endpoint returns `status: "ERROR"` — not a `status: "FOUND"` with
a boundary.

**SF-3 (Form 3 absent when focal cohort configured):** `monitored_focal_cohorts` contains
a valid entry but `constraint-search-section` does not render in Mode 3. Detection:
assert `constraint-search-section` is present in the DOM when `monitored_focal_cohorts`
has a valid entry and the app is in Mode 3.

---

## 4. Acceptance Criteria

**AC-1 (Form 3 visible in Mode 3 with focal cohort configured):**
In Mode 3 with `monitored_focal_cohorts[0].floor_value` set, `data-testid="constraint-search-section"` is present in the DOM.

**AC-2 (Form 3 absent from Mode 1 and Mode 2):**
In Mode 1 and Mode 2, `data-testid="constraint-search-section"` is not present in the DOM.

**AC-3 (constraint-search-unavailable when no focal cohort):**
In Mode 3 with `monitored_focal_cohorts` empty, `data-testid="constraint-search-unavailable"` is present and `data-testid="constraint-search-btn"` is absent.

**AC-4 (PENDING state while search runs):**
After clicking `constraint-search-btn`, `data-testid="constraint-search-pending"` is
present and `constraint-search-btn` is disabled before the response returns.

**AC-5 (FOUND state with boundary value):**
When the backend binary search converges (mock: `status: "FOUND"`, `boundary: 1.18`,
`uncertainty_lo: 1.17`, `uncertainty_hi: 1.19`, `evaluations: 9`),
`data-testid="constraint-search-found"` is present and `data-testid="constraint-boundary-value"` text contains "1.18".

**AC-6 (NOT_FOUND state):**
When backend returns `status: "NOT_FOUND"`, `data-testid="constraint-search-not-found"` is present and `data-testid="constraint-search-found"` is absent.

**AC-7 (ERROR state — SF-1 guard):**
When backend returns `status: "ERROR"`, `data-testid="constraint-search-error"` is present and `data-testid="constraint-search-result"` contains visible text (not blank).

**AC-8 (backend binary search converges to correct boundary):**
Backend unit test: `binary_search(scenario, focal_cohort, lo=0.1, hi=3.0, tol=0.01)` on
a fixture scenario where `fiscal_multiplier=1.18` causes the focal cohort to just cross
the floor value returns a `boundary` value in `[1.17, 1.19]` within 12 evaluations.

**AC-9 (backend raises on partial evaluation failure — SF-2 guard):**
Backend unit test: if `run_trajectory` raises `ValueError` during any binary search
evaluation, the endpoint response has `status: "ERROR"` — not `status: "FOUND"`.

**AC-10 (endpoint POST /scenarios/{id}/constraint-floor-search returns 404 for unknown scenario):**
`POST /scenarios/nonexistent-id/constraint-floor-search` returns HTTP 404 with a JSON
error body.

**AC-11 (synthetic disclosure — Tier 3):**
When the focal cohort indicator is Tier 3 (SYNTHETIC_COMPARABLE) and status is FOUND,
the result area contains the word "synthetic" visible to the user.

**AC-12 (structural absence — Tier 4+):**
When the focal cohort indicator is Tier 4 or Structural Absence, `data-testid="constraint-search-structural-absence"` is present and `constraint-search-btn` is absent.

**AC-016 (Form 3 column visibility — pre-ship, tracked #1563):**
At viewport 1280×800, with Forms 1 and 2 in minimum state (no history entries),
`data-testid="constraint-search-section"` bounding box is fully within
`scrollTop + clientHeight` of the column container. At 1024×768, Form 3 is reachable
within one column-internal scroll from column top.

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation
for Persona 2 to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` No — the observable state is interpretable by Persona 2 without specialist
translation.

Rationale: "fiscal multiplier ≥ 1.18 (±0.01)" is a specific numeric boundary that
Persona 2 can read, state, and cite at the negotiating table without requiring an
economist to interpret it. The "(±0.01)" precision notation is self-describing (search
resolution, not statistical uncertainty — disclosed by the UX per ADR-021 §D-4). The
"9 evaluations" count is supporting metadata, not a required reading for the cite.

The FOUND state's primary output is a number and a direction ("≥"). No mediation required.

---

## 6. Out of Scope (M19 G1)

- **Multi-parameter joint constraint search** (two or more parameters simultaneously) — M20+
- **Multi-cohort joint constraint** (multiple `monitored_focal_cohorts` entries with
  conflicting floors) — M20+; G1 uses `monitored_focal_cohorts[0]` only
- **Streaming progress during binary search** — SSE/chunked response deferred; M19 uses
  synchronous endpoint with PENDING spinner
- **Statistical CI on the boundary** — G3 (ADR-007 Bayesian posterior layer, #1543); M19
  boundary uncertainty is search precision (±0.01), not an empirically grounded CI band
- **Async endpoint / long-polling** — M19 is synchronous; if 30s timeout is insufficient
  at free-tier runner, tolerance relaxed to 0.05 with user note (per ADR-021 §Known
  Limitations)
- **MV-001 CVD three-way validation result** — tracked as #1564; pre-ship condition for
  this PR, not a separate sprint group

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any implementation PR opens for G1
**Test file locations:**
- `frontend/tests/e2e/m19-g1-constraint-floor-search.spec.ts` (Playwright E2E — AC-1 through AC-7, AC-11, AC-12, AC-016)
- `backend/tests/test_m19_g1_constraint_floor_search.py` (pytest — AC-8, AC-9, AC-10)

**Required test coverage:**

- **E2E (Playwright) — AC-1:** Set up Mode 3 fixture with `monitored_focal_cohorts[0]` valid; assert `constraint-search-section` present.
- **E2E (Playwright) — AC-2:** Mode 1 render; assert `constraint-search-section` absent. Mode 2 render; same assertion.
- **E2E (Playwright) — AC-3:** Mode 3, `monitored_focal_cohorts` empty; assert `constraint-search-unavailable` present, `constraint-search-btn` absent.
- **E2E (Playwright) — AC-4:** Click `constraint-search-btn` (intercept and delay the POST); assert `constraint-search-pending` present and button disabled.
- **E2E (Playwright) — AC-5:** Mock POST returning FOUND response; assert `constraint-search-found` present and `constraint-boundary-value` text contains "1.18".
- **E2E (Playwright) — AC-6:** Mock POST returning NOT_FOUND; assert `constraint-search-not-found` present, `constraint-search-found` absent.
- **E2E (Playwright) — AC-7 (SF-1):** Mock POST returning ERROR; assert `constraint-search-error` present with non-empty visible text.
- **E2E (Playwright) — AC-11:** Mock POST returning FOUND + synthetic tier; assert result area text contains "synthetic".
- **E2E (Playwright) — AC-12:** Structural absence tier scenario; assert `constraint-search-structural-absence` present.
- **E2E (Playwright) — AC-016:** At 1280×800 with Forms 1+2 at minimum state, assert `constraint-search-section` bounding box ≤ column `scrollTop + clientHeight`.
- **Backend (pytest) — AC-8:** Call `binary_search()` on fixture scenario; assert returned boundary in `[1.17, 1.19]` within 12 evaluations.
- **Backend (pytest) — AC-9 (SF-2):** Patch `run_trajectory` to raise `ValueError` on third call; assert endpoint response `status == "ERROR"`.
- **Backend (pytest) — AC-10:** POST to `/scenarios/nonexistent-id/constraint-floor-search`; assert 404 response.

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-12 and AC-016 authored and filed. 2026-07-02
- `frontend/tests/e2e/m19-g1-constraint-floor-search.spec.ts` — AC-1 through AC-7, AC-11, AC-12, AC-016 (all guard on `constraint-search-section` testid; no-ops pre-implementation)
- `backend/tests/test_m19_g1_constraint_floor_search.py` — AC-8, AC-9, AC-10 + schema smoke tests (all guard on `IMPLEMENTATION_PRESENT`; no-ops pre-implementation)

---

*Intent document version: 2026-07-02. ADR-021 accepted 2026-07-02. Sprint entry:
`docs/process/sprint-plans/m19-g1-sprint-entry.md`. See
`docs/process/agent-execution-lifecycle.md` for the five-step lifecycle this document
gates.*
