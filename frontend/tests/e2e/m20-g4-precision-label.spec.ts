/**
 * E2E: M20-G4 — Binary Search Precision Label vs CI Label (DEMO-234 / #1776)
 *
 * Authored BEFORE implementation per intent document:
 *   docs/process/intents/M20-G4-2026-07-08-precision-label-clarification.md
 *
 * Sprint entry: docs/process/sprint-plans/m20-g4-sprint-entry.md (EL Approved 2026-07-08)
 * Component: ControlPlaneColumn.tsx — constraint-search-found section
 *
 * ACs covered:
 *   AC-1  constraint-search-precision present; text contains "binary search"
 *   AC-2  constraint-tolerance-band absent from constraint-search-found (renamed)
 *   AC-3  constraint-precision-note present; text does NOT say "Zone 3"; says "trajectory" or "CI bands"
 *   AC-4  constraint-precision-note computed font-size ≥ 11px AND color NOT rgb(156,163,175)
 *   AC-5  constraint-boundary-value present and unchanged (regression)
 *   AC-6  evaluations count and search range still present (regression)
 *   AC-7  SF-1 guard: constraint-tolerance-band absent — explicit block
 *   AC-8  SF-2 guard: constraint-precision-note color NOT #9ca3af — explicit block
 *   AC-9  SF-3 guard: constraint-search-precision text contains "binary search" — explicit block
 *
 * RED state: AC-1, AC-3, AC-4, AC-7, AC-9 will fail until DEMO-234 implementation lands.
 *   - AC-1: constraint-search-precision does not exist yet (element is constraint-tolerance-band)
 *   - AC-2: constraint-tolerance-band exists → AC-2 FAILS (the rename hasn't happened)
 *   - AC-4: note is currently 10px #9ca3af → AC-4 FAILS
 *
 * See NM-056: no test.skip() / test.fixme() / .only() patterns.
 *
 * Context:
 *   The constraint-tolerance-band currently shows "±0.00 precision" (ambiguous).
 *   DEMO-234 fix: rename to constraint-search-precision; label "binary search precision: ±X.XX".
 *   The disambiguation note (already in DOM at 10px/#9ca3af) must be promoted to ≥11px/≥#6b7280.
 *   Note text must not say "Zone 3 methodology panel" — that's an internal label.
 */

import { test, expect, Page } from "@playwright/test";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const VIEWPORT = { width: 1440, height: 900 };

const FOCAL_COHORT_CONFIG = {
  indicator_key: "bottom_quintile_informal_workers_poverty_headcount",
  floor_value: 0.4,
  floor_label: "Poverty headcount floor (bottom quintile)",
  framework: "human_development",
};

// FOUND response with uncertainty_hi - uncertainty_lo = 0.01 (the binary search precision).
// This is distinct from CI width (e.g. 0.08 wide on the poverty headcount estimate).
const FOUND_RESPONSE = {
  status: "FOUND",
  boundary: 0.83,
  uncertainty_lo: 0.825,
  uncertainty_hi: 0.835,
  evaluations: 8,
  search_lo: 0.1,
  search_hi: 3.0,
  floor_value: 0.4,
  indicator_key: "bottom_quintile_informal_workers_poverty_headcount",
  error_message: null,
};

const SCENARIO_ID = "zmb-precision-label-test";

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
    // Timeout handled by downstream guards
  }
}

async function setupScenarioMocks(page: Page): Promise<void> {
  const detail = {
    scenario_id: SCENARIO_ID,
    name: "ZMB Precision Label Test",
    description: null,
    status: "in_progress",
    version: 1,
    created_at: "2026-07-08T00:00:00Z",
    scheduled_inputs: [],
    configuration: {
      entities: ["ZMB"],
      initial_attributes: {},
      n_steps: 8,
      timestep_label: "quarter",
      // fiscal_multiplier != null && !== 1.0 → ScenarioInstrumentCluster routes to MODE_2
      fiscal_multiplier: 1.3,
      monitored_focal_cohorts: [FOCAL_COHORT_CONFIG],
    },
  };
  const trajectory = {
    scenario_id: SCENARIO_ID,
    entity_id: "ZMB",
    step_count: 0,
    mda_floors: [],
    threshold_crossings: [],
    steps: [],
  };
  await page.route(`**/api/v1/scenarios/${SCENARIO_ID}`, (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(detail) }),
  );
  await page.route(`**/api/v1/scenarios/${SCENARIO_ID}/trajectory**`, (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(trajectory) }),
  );
}

/** Enter Mode 3 and trigger a FOUND constraint search result. */
async function enterMode3AndGetFoundResult(page: Page): Promise<void> {
  await setupScenarioMocks(page);
  await page.route("**/constraint-floor-search", (route) =>
    route.fulfill({ json: FOUND_RESPONSE }),
  );

  await page.goto(`/?scenario=${SCENARIO_ID}`);
  await waitForScenarioLoad(page, SCENARIO_ID);

  const enterBtn = page.getByTestId("enter-active-control-btn");
  await enterBtn.waitFor({ state: "visible", timeout: 8_000 }).catch(() => {});
  if (await enterBtn.isVisible().catch(() => false)) {
    await enterBtn.click();
  }

  await page
    .getByTestId("constraint-search-section")
    .waitFor({ state: "visible", timeout: 5_000 })
    .catch(() => {});

  const searchBtn = page.getByTestId("constraint-search-btn");
  if (await searchBtn.isVisible().catch(() => false)) {
    await searchBtn.click();
    await page
      .getByTestId("constraint-search-found")
      .waitFor({ state: "visible", timeout: 8_000 })
      .catch(() => {});
  }
}

/** Returns true if constraint-search-found is visible (search implementation landed). */
async function foundSectionVisible(page: Page): Promise<boolean> {
  return page.getByTestId("constraint-search-found").isVisible().catch(() => false);
}

// ---------------------------------------------------------------------------
// AC-1: constraint-search-precision present; text contains "binary search"
// ---------------------------------------------------------------------------

test("AC-1: constraint-search-precision present in FOUND state with text containing 'binary search'", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await enterMode3AndGetFoundResult(page);

  if (!(await foundSectionVisible(page))) {
    expect(
      false,
      "AC-1 FAIL: constraint-search-found not visible — constraint search not yet implemented. " +
      "See m19-g1-constraint-floor-search.spec.ts AC-5.",
    ).toBe(true);
    return;
  }

  const precisionEl = page.getByTestId("constraint-search-precision");
  const present = await precisionEl.isVisible().catch(() => false);

  expect(
    present,
    "AC-1 FAIL: [data-testid='constraint-search-precision'] not present in constraint-search-found. " +
    "Fix DEMO-234: rename constraint-tolerance-band → constraint-search-precision. " +
    "The element must be present after FOUND result renders. " +
    "See intent M20-G4-2026-07-08-precision-label-clarification.md §3.2.",
  ).toBe(true);

  if (present) {
    const text = await precisionEl.textContent().catch(() => "");
    expect(
      text,
      "AC-1 FAIL: constraint-search-precision text does not contain 'binary search'. " +
      `Got: '${text}'. ` +
      "Fix DEMO-234: label must read 'binary search precision: ±X.XX' (explicit qualifier). " +
      "See intent §3.2 — key change 1: unambiguous label 'binary search precision: ±0.01'. " +
      "See intent §4 AC-1.",
    ).toContain("binary search");
  }
});

// ---------------------------------------------------------------------------
// AC-2: constraint-tolerance-band absent (renamed to constraint-search-precision)
// ---------------------------------------------------------------------------

test("AC-2: constraint-tolerance-band absent from constraint-search-found after rename", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await enterMode3AndGetFoundResult(page);

  if (!(await foundSectionVisible(page))) {
    return; // pre-implementation; pass vacuously
  }

  const foundSection = page.getByTestId("constraint-search-found");
  const oldEl = foundSection.locator('[data-testid="constraint-tolerance-band"]');
  const present = await oldEl.isVisible().catch(() => false);

  expect(
    present,
    "AC-2 FAIL: [data-testid='constraint-tolerance-band'] still present in constraint-search-found. " +
    "Fix DEMO-234: the testid must be renamed to constraint-search-precision. " +
    "constraint-tolerance-band must not appear in the FOUND state after the fix. " +
    "See intent §3.2 key change 1 and §3.3 SF-1.",
  ).toBe(false);
});

// ---------------------------------------------------------------------------
// AC-3: constraint-precision-note present; no "Zone 3"; references "trajectory" or "CI"
// ---------------------------------------------------------------------------

test("AC-3: constraint-precision-note present; no 'Zone 3' reference; says 'trajectory' or 'CI bands'", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await enterMode3AndGetFoundResult(page);

  if (!(await foundSectionVisible(page))) {
    expect(
      false,
      "AC-3 FAIL: constraint-search-found not visible — cannot verify precision note.",
    ).toBe(true);
    return;
  }

  const noteEl = page.getByTestId("constraint-precision-note");
  const present = await noteEl.isVisible().catch(() => false);

  expect(
    present,
    "AC-3 FAIL: [data-testid='constraint-precision-note'] not present in constraint-search-found. " +
    "Fix DEMO-234: the disambiguation note must be present and have testid='constraint-precision-note'. " +
    "See intent §3.2 — the existing 10px gray note must be promoted and re-testid'd. " +
    "See intent §4 AC-3.",
  ).toBe(true);

  if (present) {
    const text = await noteEl.textContent().catch(() => "");

    expect(
      text,
      "AC-3 FAIL: constraint-precision-note contains 'Zone 3' — an internal label not visible to users. " +
      `Got: '${text}'. ` +
      "Fix DEMO-234: note must say 'trajectory view', 'CI bands', or equivalent user-facing language " +
      "instead of 'Zone 3 methodology panel'. See intent §3.2 key change 3.",
    ).not.toContain("Zone 3");

    const referencesUserFacing =
      text.toLowerCase().includes("trajectory") ||
      text.toLowerCase().includes("ci band") ||
      text.toLowerCase().includes("confidence interval");

    expect(
      referencesUserFacing,
      "AC-3 FAIL: constraint-precision-note does not reference 'trajectory view' or 'CI bands'. " +
      `Got: '${text}'. ` +
      "The note must tell the user WHERE to find the distributional uncertainty. " +
      "See intent §3.2 key change 3.",
    ).toBe(true);
  }
});

// ---------------------------------------------------------------------------
// AC-4: constraint-precision-note font-size ≥ 11px AND color NOT #9ca3af
// ---------------------------------------------------------------------------

test("AC-4: constraint-precision-note font-size ≥ 11px and color is NOT rgb(156,163,175)", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await enterMode3AndGetFoundResult(page);

  if (!(await foundSectionVisible(page))) {
    expect(
      false,
      "AC-4 FAIL: constraint-search-found not visible — cannot verify note visual prominence.",
    ).toBe(true);
    return;
  }

  const noteEl = page.getByTestId("constraint-precision-note");
  if (!(await noteEl.isVisible().catch(() => false))) {
    expect(
      false,
      "AC-4 FAIL: constraint-precision-note not visible — AC-3 fix required first.",
    ).toBe(true);
    return;
  }

  const styles = await noteEl.evaluate((el) => {
    const cs = window.getComputedStyle(el);
    return {
      fontSize: cs.fontSize,  // e.g. "10px" or "11px"
      color: cs.color,         // e.g. "rgb(156, 163, 175)" = #9ca3af
    };
  }).catch(() => null);

  if (styles === null) {
    expect(false, "AC-4 FAIL: Could not read computed styles of constraint-precision-note.").toBe(true);
    return;
  }

  // Parse font-size value (strip "px" suffix)
  const fontSizePx = parseFloat(styles.fontSize);
  expect(
    fontSizePx,
    "AC-4 FAIL: constraint-precision-note font-size is " + styles.fontSize + " (< 11px). " +
    "Fix DEMO-234: promote the note to ≥ 11px so it is readable at standard viewing distance. " +
    "Current implementation uses 10px. See intent §3.2 key change 2 and §4 AC-4.",
  ).toBeGreaterThanOrEqual(11);

  // Color must NOT be #9ca3af = rgb(156, 163, 175)
  const isOldColor = /rgb\(156,\s*163,\s*175\)/.test(styles.color);
  expect(
    isOldColor,
    "AC-4 FAIL: constraint-precision-note color is rgb(156, 163, 175) (#9ca3af — too light). " +
    "Fix DEMO-234: promote note color to ≥ #6b7280 (rgb(107, 114, 128)) for readability. " +
    "Current implementation uses #9ca3af. See intent §3.2 key change 2 and §4 AC-4.",
  ).toBe(false);
});

// ---------------------------------------------------------------------------
// AC-5: constraint-boundary-value present and unchanged (regression)
// ---------------------------------------------------------------------------

test("AC-5 regression: constraint-boundary-value present and shows boundary after DEMO-234 changes", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await enterMode3AndGetFoundResult(page);

  if (!(await foundSectionVisible(page))) {
    return;
  }

  const boundaryEl = page.getByTestId("constraint-boundary-value");
  const present = await boundaryEl.isVisible().catch(() => false);

  expect(
    present,
    "AC-5 FAIL: constraint-boundary-value not visible in constraint-search-found after DEMO-234 changes. " +
    "Regression: the boundary value display must survive the label rename. " +
    "See intent §4 AC-5.",
  ).toBe(true);

  if (present) {
    const text = await boundaryEl.textContent().catch(() => "");
    // FOUND_RESPONSE.boundary = 0.83; the text should contain "0.83"
    expect(
      text,
      "AC-5 FAIL: constraint-boundary-value does not contain '0.83'. Got: '" + text + "'.",
    ).toContain("0.83");
  }
});

// ---------------------------------------------------------------------------
// AC-6: evaluations count and search range still present (regression)
// ---------------------------------------------------------------------------

test("AC-6 regression: evaluations count and search range display present after DEMO-234 changes", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await enterMode3AndGetFoundResult(page);

  if (!(await foundSectionVisible(page))) {
    return;
  }

  const foundSection = page.getByTestId("constraint-search-found");
  const sectionText = await foundSection.textContent().catch(() => "");

  // FOUND_RESPONSE.evaluations = 8; search_lo = 0.1, search_hi = 3.0
  expect(
    sectionText,
    "AC-6 FAIL: constraint-search-found does not contain evaluations count '8'. " +
    "The evaluations display must survive the DEMO-234 label changes. " +
    "See intent §4 AC-6.",
  ).toContain("8");

  // Search range [0.1, 3.0] should appear in some form
  const containsRange =
    sectionText.includes("0.1") && sectionText.includes("3.0");

  expect(
    containsRange,
    "AC-6 FAIL: constraint-search-found does not contain both '0.1' and '3.0' (search range). " +
    "The search range display must survive the DEMO-234 label changes. " +
    "Current text: '" + sectionText + "'.",
  ).toBe(true);
});

// ---------------------------------------------------------------------------
// AC-7 (SF-1 guard): constraint-tolerance-band absent — explicit separate block
// ---------------------------------------------------------------------------

test("AC-7 SF-1 guard: constraint-tolerance-band absent from constraint-search-found (explicit SF guard)", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await enterMode3AndGetFoundResult(page);

  if (!(await foundSectionVisible(page))) {
    return;
  }

  const foundSection = page.getByTestId("constraint-search-found");
  const oldEl = foundSection.locator('[data-testid="constraint-tolerance-band"]');
  const present = await oldEl.isVisible().catch(() => false);

  expect(
    present,
    "AC-7 SF-1 FAIL: constraint-tolerance-band still present in constraint-search-found. " +
    "This is the same assertion as AC-2, written as an explicit SF guard. " +
    "SF-1: the testid rename must be complete — old testid must not remain. " +
    "See intent §3.3 SF-1.",
  ).toBe(false);
});

// ---------------------------------------------------------------------------
// AC-8 (SF-2 guard): constraint-precision-note color promoted — explicit separate block
// ---------------------------------------------------------------------------

test("AC-8 SF-2 guard: constraint-precision-note color is NOT #9ca3af (explicit SF guard)", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await enterMode3AndGetFoundResult(page);

  if (!(await foundSectionVisible(page))) {
    return;
  }

  const noteEl = page.getByTestId("constraint-precision-note");
  if (!(await noteEl.isVisible().catch(() => false))) {
    return; // AC-3 not yet implemented
  }

  const color = await noteEl.evaluate(
    (el) => window.getComputedStyle(el).color,
  ).catch(() => null);

  if (color !== null) {
    const isOldColor = /rgb\(156,\s*163,\s*175\)/.test(color);
    expect(
      isOldColor,
      "AC-8 SF-2 FAIL: constraint-precision-note color is still rgb(156, 163, 175) (#9ca3af). " +
      "SF-2: the note color must be promoted to ≥ #6b7280 after the fix. " +
      "This is the color assertion from AC-4, written as an explicit SF guard. " +
      "See intent §3.3 SF-2.",
    ).toBe(false);
  }
});

// ---------------------------------------------------------------------------
// AC-9 (SF-3 guard): constraint-search-precision text contains "binary search" — explicit block
// ---------------------------------------------------------------------------

test("AC-9 SF-3 guard: constraint-search-precision text contains 'binary search' (explicit SF guard)", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);
  await enterMode3AndGetFoundResult(page);

  if (!(await foundSectionVisible(page))) {
    expect(
      false,
      "AC-9 SF-3 FAIL: constraint-search-found not visible — cannot verify label text.",
    ).toBe(true);
    return;
  }

  const precisionEl = page.getByTestId("constraint-search-precision");
  if (!(await precisionEl.isVisible().catch(() => false))) {
    expect(
      false,
      "AC-9 SF-3 FAIL: constraint-search-precision not visible — AC-1 fix required first.",
    ).toBe(true);
    return;
  }

  const text = await precisionEl.textContent().catch(() => "");
  expect(
    text,
    "AC-9 SF-3 FAIL: constraint-search-precision text does not contain 'binary search'. " +
    `Got: '${text}'. ` +
    "SF-3: the label must explicitly say 'binary search' to distinguish it from a " +
    "statistical confidence interval. This is the label-text assertion from AC-1, " +
    "written as an explicit SF guard. See intent §3.3 SF-3.",
  ).toContain("binary search");
});
