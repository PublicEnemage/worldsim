# Frontend Testing Standards — WorldSim Frontend

> Defines the required test coverage, tools, and standards for the frontend
> layer. Owned by the UI/Frontend Architect Agent. Applies from M5 onward.
>
> **Current state at M4 close: zero automated frontend tests.**
> The Playwright suite is a hard gate for M5 exit — no M5 work ships without it.
> See CLAUDE.md §Milestone Retrospective Process for the M4 radar chart incident
> that made this a hard gate.

---

## Test Framework Stack (M5 Target)

| Tool | Purpose |
|---|---|
| **Vitest** | Unit and component tests |
| **@testing-library/react** | Component rendering and interaction |
| **Playwright** | End-to-end browser tests against the full stack |
| **MSW (Mock Service Worker)** | API mocking for unit/component tests |

None of these are installed at M4 close. Installation and configuration is
the first M5 frontend task before any feature work begins.

---

## Test Categories

### 1. Unit Tests (Vitest + Testing Library)

Target: pure functions, custom hooks, and stateless components.

**Required coverage targets (M5):**
- `useMultiFrameworkOutput`: test loading state, success, error, and
  cancellation (stale-response prevention).
- `computeSteps()` in ChoroplethMap: test empty features, uniform values,
  varied distributions.
- `computeDivergingSteps()` in DeltaChoropleth: test all-positive, all-negative,
  mixed, empty.
- `isCohortBlock()` in FrameworkPanel: test QuantitySchema shape and cohort block shape.
- `loadWeights()` in EntityDetailDrawer: test missing key, invalid JSON, partial object.
- RadarChart weight application: test that `final_score` is bounded to [0,1].

**Files that need unit tests:**
```
frontend/src/hooks/useMultiFrameworkOutput.ts
frontend/src/components/ChoroplethMap.tsx    (computeSteps)
frontend/src/components/DeltaChoropleth.tsx  (computeDivergingSteps)
frontend/src/components/FrameworkPanel.tsx   (isCohortBlock)
frontend/src/components/EntityDetailDrawer.tsx (loadWeights)
```

### 2. Component Tests (Vitest + Testing Library + MSW)

Target: individual components in isolation with mocked API.

**Required for M5:**
- `MDAAlertPanel`: renders sorted by severity; handles empty list.
- `ScenarioControls`: advance button disables on complete; error message shown.
- `FrameworkPanel`: collapse/expand works; cohort block renders nested indicators.
- `AttributeSelector`: renders loading/error/select states; fires `onChange`.

### 3. End-to-End Tests (Playwright)

Target: full user flows against the running Docker Compose stack.

**Required before M5 exit — hard gate from M4 retrospective:**

```gherkin
Scenario: Create, advance, and view entity drawer
  Given the application is open
  When the user creates a scenario named "M5-Test"
  And opens the Scenarios panel
  And selects "M5-Test" as the primary scenario
  And clicks "Next Step" three times
  Then the step indicator shows "Step 3 / 3 — Complete"
  When the user clicks on Greece on the map
  Then the EntityDetailDrawer opens
  And shows "Greece" in the header
  And shows measurement output (not the placeholder message)
  And the radar chart is visible

Scenario: Re-select a completed scenario shows drawer immediately
  Given a completed scenario "M5-Test" exists
  When the user selects it from the panel
  And clicks on Greece
  Then the EntityDetailDrawer shows measurement output
  Without requiring any advance clicks

Scenario: Partial advance shows drawer at current step
  Given a scenario "Partial" with 3 steps
  When the user advances it one step
  And clicks on Greece
  Then the drawer shows measurement output at step 1
  When the user advances it a second step
  Then the drawer updates to show step 2 data
```

These three flows are the minimum. Additional flows for compare mode and
delta choropleth are required before those features are modified in M5.

---

## Coverage Requirements

| Test category | M5 minimum | M6 target |
|---|---|---|
| Unit — pure functions | 80% line coverage | 90% |
| Component — isolated | 60% component coverage | 80% |
| Playwright — E2E | 3 flows (above) | 8 flows (all primary UX paths) |

Coverage is measured by Vitest's built-in coverage reporter (c8/v8).
Playwright coverage is flow-count, not line coverage.

---

## Testing Rules

- **Never mock the API in Playwright tests.** Playwright tests run against the
  real Docker Compose stack. API mocking defeats the purpose of E2E tests.
- **Do mock the API in Vitest component tests** using MSW. Component tests must
  not make real network requests.
- **Tests must not depend on order.** Each test must be independently runnable.
- **No `setTimeout` in tests.** Use Playwright's `waitFor` / `waitForSelector`
  or Testing Library's `waitFor`. Fixed-time sleeps are flaky.
- **Test the correctness invariants from `ui-state-machine.md`**, not
  implementation details. Assert on what the user sees, not on internal state.

---

## Anti-Patterns from M4

These patterns led to the M4 radar chart drawer bug. Tests would have caught
them earlier:

1. **Testing the API smoke test after visual failure.** The smoke test was
   written reactively. The rule: write the smoke test before the first
   manual browser test. The test defines the contract; the browser confirms UX.

2. **No test for async state transitions.** The `useEffect` race between
   `handleSelectScenario` (sets `currentStep=null`) and `handleStepChange`
   (sets `currentStep=N`) was invisible because no test covered the transition.
   A Playwright test that: (a) advances all steps, (b) clicks an entity,
   (c) asserts the drawer shows data — would have caught this immediately.

3. **No test for re-selecting a completed scenario.** The second Playwright
   flow above (re-select → drawer shows immediately) was the exact regression.
   It is now a required test.

---

## Phase 3–4: Distribution Visualization Acceptance Criteria (M5 / M6)

Per ADR-006 Decision 12, a second Playwright layer is required once distribution
visualization components are implemented. These three criteria are the binding
acceptance tests, each derived from a user-observable outcome defined in
`docs/ux/north-star.md §Distribution Visualization Acceptance Criteria`.

The Phase 3–4 suite is **not** a blocking gate for M5 exit. It **becomes** a
blocking gate for the first PR that merges distribution rendering to
`EntityDetailDrawer`, `RadarChart`, or `FrameworkPanel`. It must be written
before that PR is opened, not after.

---

### Criterion 1 — Distribution alert fires before the mean crosses the floor

> Given a scenario advanced to a horizon where an indicator's 80% CI lower
> bound is below its MDA floor and the point estimate is within 1.5× the
> floor, when the user opens the entity drawer, then the MDA alert panel
> shows the indicator with an alert labeled as distribution-source, and this
> alert is visually distinguishable from a point-estimate alert — even if no
> point-estimate alert has fired.

**Playwright assertion:** `MDAAlertPanel` renders an element with
`data-alert-source="distribution"` for the indicator. The element is
distinguishable (e.g., different border or label) from a
`data-alert-source="point_estimate"` element. The criterion passes only
if no point-estimate alert has fired for the same indicator at the same step.

---

### Criterion 2 — Pre-calibration disclosure is non-suppressible

> Given any scenario at any step with distribution bands visible, when the
> entity drawer shows measurement output, then the `ia1_disclosure` text is
> visible and contains the word "pre-calibration," and no user interaction
> (weight adjustment, framework tab change, or scroll to top of drawer)
> makes it disappear from the rendered DOM.

**Playwright assertion:** After each interaction sequence, assert
`page.getByText(/pre-calibration/)` is attached to the DOM with
`toBeAttached()`. The test must cover: initial load, framework tab switch,
scroll to top, and (if implemented) weight adjustment toggle.

---

### Criterion 3 — Band width is proportional to projection horizon

> Given scenario A advanced 1 step and scenario B advanced 3 steps, when
> the user views the same indicator in both scenarios with uncertainty bands
> visible, then the rendered band for scenario B is visually wider than for
> scenario A, and each band display shows the declared coverage level (80%)
> and the `is_pre_calibration` flag.

**Playwright assertion:** The rendered band width for the 3-step scenario is
greater than for the 1-step scenario on the same indicator. Use
`data-band-width` attributes or accessible size attributes for reliable
assertion — do not rely on pixel measurement alone. Each band element must
contain text matching `/80%/` and the `is_pre_calibration: true` label.

---

### Implementation Sequencing Requirement

Per ARCH-REVIEW-004 Domain 5 Blindspot 5-D, the required implementation order is:

1. Phase 1–2 Playwright tests (point-estimate UI) — must pass before any M5 distribution rendering begins
2. TypeScript type updates for distribution sibling fields (no rendering change)
3. Distribution rendering components added behind `uncertaintyVisible = false` default
4. Phase 3–4 Playwright tests authored and passing before any distribution rendering PR merges

Reversing steps 3 and 4 produces flaky tests against a richer UI and makes
the Phase 1–2 tests harder to maintain. Step 1 was completed in Issue #190.
