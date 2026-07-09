/**
 * E2E: M20-G4 — WARNING Badge Alongside CLEAR in Zone 1B (DEMO-233 / #1775)
 *
 * Authored BEFORE implementation per intent document:
 *   docs/process/intents/M20-G4-2026-07-08-warning-clear-badge.md
 *
 * Sprint entry: docs/process/sprint-plans/m20-g4-sprint-entry.md (EL Approved 2026-07-08)
 * Component: CohortImpactSection in MDAAlertPanelZone1B.tsx
 *
 * ACs covered:
 *   AC-1  WARNING badge present when CLEAR + narrow margin (< 5% above floor)
 *   AC-2  WARNING badge absent when CLEAR + comfortable margin (≥ 5% above floor)
 *   AC-3  WARNING badge absent when CRITICAL (below floor)
 *   AC-4  CLEAR badge unchanged when narrow margin (WARNING is additive)
 *   AC-5  Boundary case: exactly 5% above floor → WARNING absent (< not ≤)
 *   AC-6  SF-1 guard: 3% above floor → WARNING present (separate block)
 *   AC-7  SF-2 guard: 10% above floor → WARNING absent (separate block)
 *   AC-8  SF-3 guard: CRITICAL state → WARNING absent (separate block)
 *
 * RED state: AC-1, AC-4, AC-6 will fail until DEMO-233 implementation lands.
 *   - AC-1: [data-testid="focal-warning-badge"] does not exist yet
 *   - AC-2, AC-3, AC-5, AC-7, AC-8: pass vacuously (absent = pass)
 *
 * See NM-056: no test.skip() / test.fixme() / .only() patterns.
 *
 * Margin computation: above_floor_pct = (numValue - floor_value) / floor_value
 * WARNING threshold: above_floor_pct < 0.05 (strict less-than; not less-than-or-equal)
 */

import { test, expect, Page } from "@playwright/test";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const VIEWPORT = { width: 1440, height: 900 };

// The focal cohort indicator and floor values used across all tests.
// floor_value = 0.400
// narrow margin (< 5%): numValue = 0.400 * 1.03 = 0.412 → above_floor_pct = 0.03 → WARNING
// comfortable margin (≥ 5%): numValue = 0.400 * 1.10 = 0.440 → above_floor_pct = 0.10 → no WARNING
// exactly 5%: numValue = 0.400 * 1.05 = 0.420 → above_floor_pct = 0.05 → no WARNING (< not ≤)
// CRITICAL (below floor): numValue = 0.400 * 0.97 = 0.388 → CRITICAL → no WARNING
const FLOOR_VALUE = 0.4;
const VALUE_NARROW = FLOOR_VALUE * 1.03;     // 0.412: 3% above floor → WARNING
const VALUE_COMFORTABLE = FLOOR_VALUE * 1.10; // 0.440: 10% above floor → no WARNING
const VALUE_EXACT_5PCT = FLOOR_VALUE * 1.05;  // 0.420: exactly 5% → no WARNING (< not ≤)
const VALUE_CRITICAL = FLOOR_VALUE * 0.97;    // 0.388: below floor → CRITICAL

const INDICATOR_KEY = "bottom_quintile_informal_workers_poverty_headcount";
const FOCAL_COHORT_CONFIG = {
  indicator_key: INDICATOR_KEY,
  floor_value: FLOOR_VALUE,
  floor_label: "Recovery floor",
  framework: "human_development",
};

const SCENARIO_ID = "zmb-warning-badge-test";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function waitForScenarioLoad(page: Page, scenarioId: string): Promise<void> {
  try {
    await page.waitForFunction(
      (id) => (window as Record<string, unknown>).__worldsim_selectedScenarioId === id,
      scenarioId,
      { timeout: 10_000 },
    );
  } catch {
    // Timeout handled by downstream isVisible().catch(() => false) guards
  }
}

/** Build a single-step trajectory mock with the given indicator value. */
function makeTrajectoryWithFocalValue(scenarioId: string, indicatorValue: number): object {
  const valStr = indicatorValue.toFixed(3);
  return {
    scenario_id: scenarioId,
    entity_id: "ZMB",
    step_count: 1,
    mda_floors: [],
    threshold_crossings: [],
    steps: [
      {
        step_index: 1,
        effective_from: "2024-01-01T00:00:00Z",
        step_event_label: null,
        step_significance: "ROUTINE",
        frameworks: [
          {
            framework: "human_development",
            composite_score: "0.500",
            confidence_tier: 3,
            ci_lower: null,
            ci_upper: null,
            scoring_basis: "percentile_rank",
            indicators: {
              [INDICATOR_KEY]: {
                value: valStr,
                unit: "ratio",
                variable_type: "STOCK",
                confidence_tier: 3,
              },
            },
            mda_alerts: [],
            has_below_floor_indicator: indicatorValue <= FLOOR_VALUE,
            note: null,
          },
          {
            framework: "financial",
            composite_score: "0.500",
            confidence_tier: 3,
            ci_lower: null,
            ci_upper: null,
            scoring_basis: "percentile_rank",
            indicators: {},
            mda_alerts: [],
            has_below_floor_indicator: false,
            note: null,
          },
        ],
      },
    ],
  };
}

/** Set up scenario detail and trajectory mocks for the given indicator value. */
async function setupFocalScenarioMocks(page: Page, indicatorValue: number): Promise<void> {
  const detail = {
    scenario_id: SCENARIO_ID,
    name: `ZMB Warning Badge Test (${indicatorValue.toFixed(3)})`,
    description: null,
    status: "completed",
    version: 1,
    created_at: "2026-07-08T00:00:00Z",
    scheduled_inputs: [],
    configuration: {
      entities: ["ZMB"],
      initial_attributes: {},
      n_steps: 1,
      timestep_label: "quarter",
      // fiscal_multiplier != null && !== 1.0 → routes to MODE_2
      fiscal_multiplier: 1.3,
      monitored_focal_cohorts: [FOCAL_COHORT_CONFIG],
    },
  };
  const trajectory = makeTrajectoryWithFocalValue(SCENARIO_ID, indicatorValue);

  await page.route(`**/api/v1/scenarios/${SCENARIO_ID}`, (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(detail) }),
  );
  await page.route(`**/api/v1/scenarios/${SCENARIO_ID}/trajectory**`, (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(trajectory) }),
  );
}

/** Navigate to the scenario and advance to step 1 to surface Zone 1B focal row. */
async function loadScenarioAtStep1(page: Page): Promise<void> {
  await page.goto(`/?scenario=${SCENARIO_ID}`);
  await waitForScenarioLoad(page, SCENARIO_ID);
  // Advance once so the step 1 indicators are rendered in Zone 1B.
  // Guard: only click if the button is enabled — a completed scenario with n_steps=1
  // loads at step 1 directly (setCurrentStep(n_steps)), leaving Next Step disabled.
  const nextBtn = page.getByRole("button", { name: /Next Step/ });
  const nextVisible = await nextBtn.isVisible({ timeout: 5_000 }).catch(() => false);
  if (nextVisible && !(await nextBtn.isDisabled().catch(() => false))) {
    await nextBtn.click();
    await page.waitForTimeout(600);
  }
  await page.waitForTimeout(500);
}

/** Return the focal-cohort-row locator for the test scenario. */
function focalCohortRow(page: Page) {
  return page.locator('[data-testid="focal-cohort-row"]');
}

// ---------------------------------------------------------------------------
// AC-1: WARNING badge present when CLEAR + narrow margin (3% above floor)
// ---------------------------------------------------------------------------

test("AC-1: focal-warning-badge present when indicator is 3% above floor (narrow margin < 5%)", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await setupFocalScenarioMocks(page, VALUE_NARROW);
  await loadScenarioAtStep1(page);

  const row = focalCohortRow(page);
  if (!(await row.isVisible().catch(() => false))) {
    // focal-cohort-row not yet implemented (G7-C gate). Cannot assert warning badge.
    // AC-1 remains RED. No test.skip() per NM-056.
    expect(
      false,
      "AC-1 FAIL: [data-testid='focal-cohort-row'] not visible — " +
      "focal row implementation required before warning badge. " +
      "Ensure monitored_focal_cohorts renders focal-cohort-row in Zone 1B.",
    ).toBe(true);
    return;
  }

  const warningBadge = row.locator('[data-testid="focal-warning-badge"]');
  const present = await warningBadge.isVisible().catch(() => false);

  expect(
    present,
    "AC-1 FAIL: [data-testid='focal-warning-badge'] not present in focal-cohort-row " +
    `when indicator value ${VALUE_NARROW.toFixed(3)} is 3% above floor ${FLOOR_VALUE}. ` +
    "above_floor_pct = 0.03 < 0.05 → WARNING badge must be shown. " +
    "Fix DEMO-233: add focal-warning-badge to focal row when (numValue - floor_value) / floor_value < 0.05 " +
    "and state is CLEAR. See intent M20-G4-2026-07-08-warning-clear-badge.md §3.2.",
  ).toBe(true);

  if (present) {
    const text = await warningBadge.textContent().catch(() => "");
    expect(
      text,
      "AC-1 FAIL: focal-warning-badge text is not 'WARNING'. Got: " + text,
    ).toContain("WARNING");
  }
});

// ---------------------------------------------------------------------------
// AC-2: WARNING badge absent when CLEAR + comfortable margin (10% above floor)
// ---------------------------------------------------------------------------

test("AC-2: focal-warning-badge absent when indicator is 10% above floor (comfortable margin ≥ 5%)", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await setupFocalScenarioMocks(page, VALUE_COMFORTABLE);
  await loadScenarioAtStep1(page);

  const row = focalCohortRow(page);
  if (!(await row.isVisible().catch(() => false))) {
    return; // focal-cohort-row pre-implementation; pass vacuously
  }

  const warningBadge = row.locator('[data-testid="focal-warning-badge"]');
  const present = await warningBadge.isVisible().catch(() => false);

  expect(
    present,
    "AC-2 FAIL: [data-testid='focal-warning-badge'] is present when indicator value " +
    `${VALUE_COMFORTABLE.toFixed(3)} is 10% above floor ${FLOOR_VALUE}. ` +
    "above_floor_pct = 0.10 ≥ 0.05 → WARNING badge must be absent. " +
    "Fix SF-2: warning badge must only show for narrow margins (< 0.05). " +
    "See intent §3.5 SF-2.",
  ).toBe(false);
});

// ---------------------------------------------------------------------------
// AC-3: WARNING badge absent when CRITICAL (below floor)
// ---------------------------------------------------------------------------

test("AC-3: focal-warning-badge absent when indicator is below floor (CRITICAL state)", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await setupFocalScenarioMocks(page, VALUE_CRITICAL);
  await loadScenarioAtStep1(page);

  const row = focalCohortRow(page);
  if (!(await row.isVisible().catch(() => false))) {
    return;
  }

  const warningBadge = row.locator('[data-testid="focal-warning-badge"]');
  const present = await warningBadge.isVisible().catch(() => false);

  expect(
    present,
    "AC-3 FAIL: [data-testid='focal-warning-badge'] is present when indicator value " +
    `${VALUE_CRITICAL.toFixed(3)} is below floor ${FLOOR_VALUE} (CRITICAL state). ` +
    "The margin-narrowness concept does not apply to sub-floor values. " +
    "Fix SF-3: warning badge must not render when state === 'CRITICAL'. " +
    "See intent §3.5 SF-3.",
  ).toBe(false);
});

// ---------------------------------------------------------------------------
// AC-4: CLEAR badge unchanged when narrow margin (WARNING is additive)
// ---------------------------------------------------------------------------

test("AC-4 regression: focal-badge still shows CLEAR alongside WARNING when margin is narrow", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await setupFocalScenarioMocks(page, VALUE_NARROW);
  await loadScenarioAtStep1(page);

  const row = focalCohortRow(page);
  if (!(await row.isVisible().catch(() => false))) {
    return;
  }

  const clearBadge = row.locator('[data-testid="focal-badge"]');
  const clearVisible = await clearBadge.isVisible().catch(() => false);

  expect(
    clearVisible,
    "AC-4 FAIL: [data-testid='focal-badge'] not visible when indicator is 3% above floor. " +
    "The CLEAR badge must remain present when WARNING is shown alongside it. " +
    "WARNING is additive — it must not replace the CLEAR badge. " +
    "See intent §4 AC-4 and §3.2.",
  ).toBe(true);

  if (clearVisible) {
    const text = await clearBadge.textContent().catch(() => "");
    expect(
      text,
      "AC-4 FAIL: focal-badge text is not 'CLEAR' when indicator is 3% above floor. " +
      "Got: " + text + ". The CLEAR badge must show 'CLEAR' even when WARNING is present alongside it.",
    ).toContain("CLEAR");

    // Badge background must be green #2e7d32 = rgb(46, 125, 50)
    const bgColor = await clearBadge.evaluate(
      (el) => window.getComputedStyle(el).backgroundColor,
    ).catch(() => null);

    if (bgColor !== null) {
      expect(
        bgColor,
        "AC-4 FAIL: focal-badge background is not green #2e7d32 (rgb(46, 125, 50)) when showing CLEAR. " +
        "Got: " + bgColor,
      ).toMatch(/rgb\(46,\s*125,\s*50\)/);
    }
  }
});

// ---------------------------------------------------------------------------
// AC-5: Boundary case — exactly 5% above floor → WARNING absent
// ---------------------------------------------------------------------------

test("AC-5 boundary: focal-warning-badge absent when indicator is exactly 5% above floor", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await setupFocalScenarioMocks(page, VALUE_EXACT_5PCT);
  await loadScenarioAtStep1(page);

  const row = focalCohortRow(page);
  if (!(await row.isVisible().catch(() => false))) {
    return;
  }

  const warningBadge = row.locator('[data-testid="focal-warning-badge"]');
  const present = await warningBadge.isVisible().catch(() => false);

  expect(
    present,
    "AC-5 FAIL: [data-testid='focal-warning-badge'] is present when indicator value " +
    `${VALUE_EXACT_5PCT.toFixed(3)} is exactly 5% above floor ${FLOOR_VALUE}. ` +
    "The threshold is strictly < 0.05 (not ≤ 0.05). " +
    "above_floor_pct === 0.05 → WARNING must be absent. " +
    "Fix DEMO-233: use strict less-than check: (numValue - floor_value) / floor_value < 0.05. " +
    "See intent §4 AC-5.",
  ).toBe(false);
});

// ---------------------------------------------------------------------------
// AC-6 (SF-1 guard): 3% above floor → WARNING present — separate assertion block
// ---------------------------------------------------------------------------

test("AC-6 SF-1 guard: focal-warning-badge present for 3% margin (explicit SF guard)", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await setupFocalScenarioMocks(page, VALUE_NARROW);
  await loadScenarioAtStep1(page);

  const row = focalCohortRow(page);
  if (!(await row.isVisible().catch(() => false))) {
    expect(
      false,
      "AC-6 SF-1 FAIL: focal-cohort-row not visible — " +
      "cannot verify SF-1 (warning badge present for narrow margin). " +
      "focal-cohort-row implementation required first.",
    ).toBe(true);
    return;
  }

  const warningBadge = row.locator('[data-testid="focal-warning-badge"]');
  const present = await warningBadge.isVisible().catch(() => false);

  expect(
    present,
    "AC-6 SF-1 FAIL: [data-testid='focal-warning-badge'] not present " +
    `for indicator value ${VALUE_NARROW.toFixed(3)} (3% above floor). ` +
    "SF-1: narrowness warning must fire for margins < 0.05. " +
    "This is the same assertion as AC-1, written as an explicit SF guard. " +
    "See intent §3.5 SF-1.",
  ).toBe(true);
});

// ---------------------------------------------------------------------------
// AC-7 (SF-2 guard): 10% above floor → WARNING absent — separate assertion block
// ---------------------------------------------------------------------------

test("AC-7 SF-2 guard: focal-warning-badge absent for 10% margin (explicit SF guard)", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await setupFocalScenarioMocks(page, VALUE_COMFORTABLE);
  await loadScenarioAtStep1(page);

  const row = focalCohortRow(page);
  if (!(await row.isVisible().catch(() => false))) {
    return;
  }

  const warningBadge = row.locator('[data-testid="focal-warning-badge"]');
  const present = await warningBadge.isVisible().catch(() => false);

  expect(
    present,
    "AC-7 SF-2 FAIL: [data-testid='focal-warning-badge'] present " +
    `for indicator value ${VALUE_COMFORTABLE.toFixed(3)} (10% above floor). ` +
    "SF-2: narrowness warning must NOT fire for margins ≥ 0.05. " +
    "This is the same assertion as AC-2, written as an explicit SF guard. " +
    "See intent §3.5 SF-2.",
  ).toBe(false);
});

// ---------------------------------------------------------------------------
// AC-8 (SF-3 guard): CRITICAL state → WARNING absent — separate assertion block
// ---------------------------------------------------------------------------

test("AC-8 SF-3 guard: focal-warning-badge absent in CRITICAL state (explicit SF guard)", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await setupFocalScenarioMocks(page, VALUE_CRITICAL);
  await loadScenarioAtStep1(page);

  const row = focalCohortRow(page);
  if (!(await row.isVisible().catch(() => false))) {
    return;
  }

  const warningBadge = row.locator('[data-testid="focal-warning-badge"]');
  const present = await warningBadge.isVisible().catch(() => false);

  expect(
    present,
    "AC-8 SF-3 FAIL: [data-testid='focal-warning-badge'] present in CRITICAL state " +
    `(indicator ${VALUE_CRITICAL.toFixed(3)} < floor ${FLOOR_VALUE}). ` +
    "SF-3: warning badge must not render when state === 'CRITICAL'. " +
    "This is the same assertion as AC-3, written as an explicit SF guard. " +
    "See intent §3.5 SF-3.",
  ).toBe(false);
});
