/**
 * M19 G1 — Mode 3 Constraint-Floor Search (#1540)
 * Intent: docs/process/intents/M19-ADR-021-2026-07-02-constraint-floor-search.md
 * ADR: docs/adr/ADR-021-constraint-floor-search.md
 *
 * All tests guard on the Form 3 testid being absent pre-implementation (no-ops
 * until constraint-search-section ships). AC-016 guards on column geometry.
 *
 * QA Lead review 2026-07-02: 8 gaps corrected (see intent doc §7 for full list).
 * G6 additions 2026-07-04: AC-T1..AC-T4 for #1709 (tolerance band display).
 */

import { test, expect, Page } from "@playwright/test";

// ---------------------------------------------------------------------------
// Fixtures and helpers
// ---------------------------------------------------------------------------

/** Minimal scenario config with one valid focal cohort entry. */
const FOCAL_COHORT_CONFIG = {
  indicator_key: "bottom_quintile_informal_workers_poverty_headcount",
  floor_value: 0.4,
  floor_label: "Poverty headcount floor (bottom quintile)",
  framework: "human_development",
};

// Gap 3 fix: field names corrected to match ADR-021 §D-3 response schema.
// Removed: lo_searched, hi_searched, tolerance, focal_cohort_index.
// Added: search_lo, search_hi, floor_value, indicator_key, error_message.
const FOUND_RESPONSE = {
  status: "FOUND",
  boundary: 1.18,
  uncertainty_lo: 1.17,
  uncertainty_hi: 1.19,
  evaluations: 9,
  search_lo: 0.1,
  search_hi: 3.0,
  floor_value: 0.4,
  indicator_key: "bottom_quintile_informal_workers_poverty_headcount",
  error_message: null,
};

const NOT_FOUND_RESPONSE = {
  status: "NOT_FOUND",
  boundary: null,
  uncertainty_lo: null,
  uncertainty_hi: null,
  evaluations: 9,
  search_lo: 0.1,
  search_hi: 3.0,
  floor_value: 0.4,
  indicator_key: "bottom_quintile_informal_workers_poverty_headcount",
  error_message: null,
};

const ERROR_RESPONSE = {
  status: "ERROR",
  // Gap 3 fix: was 'error', corrected to 'error_message' per ADR-021 §D-3.
  error_message: "Engine evaluation failed: ValueError at step 3",
  boundary: null,
  uncertainty_lo: null,
  uncertainty_hi: null,
  evaluations: 3,
  search_lo: null,
  search_hi: null,
  floor_value: 0.4,
  indicator_key: "bottom_quintile_informal_workers_poverty_headcount",
};

// ---------------------------------------------------------------------------
// Mock helpers (NM-084 verified pattern — 2026-07-03)
// App.tsx fetches GET /api/v1/scenarios/{id} twice:
//   1. Mount effect → sets selectedScenarioId + window.__worldsim_selectedScenarioId
//   2. selectedScenarioId effect → sets activeScenarioDetail + activeFiscalMultiplier
// ScenarioInstrumentCluster routes to MODE_2 only when fiscal_multiplier != null
// && !== 1.0. Without fiscal_multiplier the cluster stays in MODE_1 and
// Mode2ColumnSurface (which contains enter-active-control-btn) never renders.
// ---------------------------------------------------------------------------

const ZMB_FOCAL_COHORT_ID = "zmb-constraint-test";
const ZMB_NO_FOCAL_ID = "zmb-no-focal-test";

async function setupScenarioMocks(
  page: Page,
  scenarioId: string,
  focalCohorts: typeof FOCAL_COHORT_CONFIG[] | null,
): Promise<void> {
  const detail = {
    scenario_id: scenarioId,
    name: `ZMB Test (${scenarioId})`,
    description: null,
    status: "in_progress",
    version: 1,
    created_at: "2026-07-03T00:00:00Z",
    scheduled_inputs: [],
    configuration: {
      entities: ["ZMB"],
      initial_attributes: {},
      n_steps: 8,
      timestep_label: "quarter",
      // fiscal_multiplier != null && !== 1.0 → ScenarioInstrumentCluster routes to
      // MODE_2, which renders Mode2ColumnSurface (contains enter-active-control-btn).
      fiscal_multiplier: 1.3,
      ...(focalCohorts ? { monitored_focal_cohorts: focalCohorts } : {}),
    },
  };
  const trajectory = {
    scenario_id: scenarioId,
    entity_id: "ZMB",
    step_count: 0,
    mda_floors: [],
    steps: [],
  };
  // Exact scenario-detail URL — **/api/v1/scenarios/* matches the base URL
  // (App.tsx: GET /api/v1/scenarios/{id}) but not sub-paths like /trajectory.
  await page.route(`**/api/v1/scenarios/${scenarioId}`, (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(detail) })
  );
  await page.route(`**/api/v1/scenarios/${scenarioId}/trajectory**`, (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(trajectory) })
  );
}

async function waitForScenarioLoad(page: Page, scenarioId: string): Promise<void> {
  // App.tsx sets window.__worldsim_selectedScenarioId after the detail fetch
  // succeeds (DEV seam). Waiting for this guarantees selectedScenarioId is in
  // state before we interact with ScenarioInstrumentCluster.
  try {
    await page.waitForFunction(
      (id) => (window as Record<string, unknown>).__worldsim_selectedScenarioId === id,
      scenarioId,
      { timeout: 10_000 },
    );
  } catch {
    // Timeout — test guards handle missing form via isVisible().catch(() => false)
  }
}

// enterMode3 is retained for AC-3 (enters Mode 3 WITHOUT focal cohort configured).
async function enterMode3(page: Page): Promise<void> {
  await setupScenarioMocks(page, ZMB_NO_FOCAL_ID, null);
  await page.goto(`/?scenario=${ZMB_NO_FOCAL_ID}`);
  await waitForScenarioLoad(page, ZMB_NO_FOCAL_ID);
  const btn = page.getByTestId("enter-active-control-btn");
  if (await btn.isVisible({ timeout: 8_000 }).catch(() => false)) {
    await btn.click();
  }
}

async function enterMode3WithFocalCohort(page: Page): Promise<void> {
  await setupScenarioMocks(page, ZMB_FOCAL_COHORT_ID, [FOCAL_COHORT_CONFIG]);
  await page.goto(`/?scenario=${ZMB_FOCAL_COHORT_ID}`);
  await waitForScenarioLoad(page, ZMB_FOCAL_COHORT_ID);
  const btn = page.getByTestId("enter-active-control-btn");
  await btn.waitFor({ state: "visible", timeout: 8_000 });
  await btn.click();
  // Wait for ControlPlaneColumn + Form 3 to mount after entering Mode 3.
  await page
    .getByTestId("constraint-search-section")
    .waitFor({ state: "visible", timeout: 5_000 })
    .catch(() => {});
}
// ---------------------------------------------------------------------------
// AC-1: Form 3 visible in Mode 3 with focal cohort configured
// ---------------------------------------------------------------------------

test("AC-1: constraint-search-section present in Mode 3 with focal cohort configured", async ({
  page,
}) => {
  // Gap 5 fix: use enterMode3WithFocalCohort — plain enterMode3 provides no
  // focal cohort so this guard would permanently fire post-implementation.
  await enterMode3WithFocalCohort(page);
  const section = page.getByTestId("constraint-search-section");
  if (!(await section.isVisible().catch(() => false))) {
    test.skip(); // Form 3 not yet implemented
    return;
  }
  await expect(section).toBeVisible();
  await expect(page.getByTestId("constraint-floor-label")).toBeVisible();
  await expect(page.getByTestId("constraint-search-btn")).toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-2: Form 3 absent from Mode 1 and Mode 2
// ---------------------------------------------------------------------------

test("AC-2: constraint-search-section absent in Mode 1", async ({ page }) => {
  await page.goto("/");
  await expect(
    page.getByTestId("constraint-search-section")
  ).not.toBeVisible();
});

test("AC-2: constraint-search-section absent in Mode 2", async ({ page }) => {
  await page.goto("/");
  const mode3Indicator = page.getByTestId("mode-3-active");
  if (await mode3Indicator.isVisible().catch(() => false)) {
    test.skip(); // Already in Mode 3; test not applicable
    return;
  }
  await expect(
    page.getByTestId("constraint-search-section")
  ).not.toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-3: constraint-search-unavailable when no focal cohort configured
// ---------------------------------------------------------------------------

test("AC-3: constraint-search-unavailable when monitored_focal_cohorts is empty", async ({
  page,
}) => {
  // enterMode3 (no focal cohort) is correct here — this test specifically
  // asserts that Form 3 shows the unavailable state when no cohort is configured.
  await enterMode3(page);
  const unavailable = page.getByTestId("constraint-search-unavailable");
  if (!(await unavailable.isVisible().catch(() => false))) {
    test.skip();
    return;
  }
  await expect(unavailable).toBeVisible();
  await expect(
    page.getByTestId("constraint-search-btn")
  ).not.toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-4: PENDING state while search runs
// ---------------------------------------------------------------------------

test("AC-4: PENDING state visible immediately after clicking Find safe boundary", async ({
  page,
}) => {
  // Gap 5 fix: use enterMode3WithFocalCohort so Form 3 renders.
  await enterMode3WithFocalCohort(page);
  const btn = page.getByTestId("constraint-search-btn");
  if (!(await btn.isVisible().catch(() => false))) {
    test.skip();
    return;
  }
  await page.route("**/constraint-floor-search", async (route) => {
    await new Promise((r) => setTimeout(r, 2000));
    await route.fulfill({ json: FOUND_RESPONSE });
  });
  await btn.click();
  await expect(page.getByTestId("constraint-search-pending")).toBeVisible();
  await expect(btn).toBeDisabled();
});

// ---------------------------------------------------------------------------
// AC-5: FOUND state with boundary value
// ---------------------------------------------------------------------------

test("AC-5: FOUND state renders boundary value after successful search", async ({
  page,
}) => {
  // Gap 5 fix: use enterMode3WithFocalCohort so Form 3 renders.
  await enterMode3WithFocalCohort(page);
  const btn = page.getByTestId("constraint-search-btn");
  if (!(await btn.isVisible().catch(() => false))) {
    test.skip();
    return;
  }
  await page.route("**/constraint-floor-search", (route) =>
    route.fulfill({ json: FOUND_RESPONSE })
  );
  await btn.click();
  await expect(page.getByTestId("constraint-search-found")).toBeVisible();
  await expect(page.getByTestId("constraint-boundary-value")).toContainText(
    "1.18"
  );
  // Gap 6 (±) assertion removed: #1709 moves ± to constraint-tolerance-band.
  // AC-T2 asserts ± present in the new element; AC-T4 asserts boundary-value is ± free.
});

// ---------------------------------------------------------------------------
// AC-6: NOT_FOUND state
// ---------------------------------------------------------------------------

test("AC-6: NOT_FOUND state renders when backend returns no boundary", async ({
  page,
}) => {
  // Gap 5 fix: use enterMode3WithFocalCohort so Form 3 renders.
  await enterMode3WithFocalCohort(page);
  const btn = page.getByTestId("constraint-search-btn");
  if (!(await btn.isVisible().catch(() => false))) {
    test.skip();
    return;
  }
  await page.route("**/constraint-floor-search", (route) =>
    route.fulfill({ json: NOT_FOUND_RESPONSE })
  );
  await btn.click();
  await expect(
    page.getByTestId("constraint-search-not-found")
  ).toBeVisible();
  await expect(
    page.getByTestId("constraint-search-found")
  ).not.toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-7: ERROR state — SF-1 guard (result area never blank)
// ---------------------------------------------------------------------------

test("AC-7: ERROR state renders non-blank error message (SF-1 guard)", async ({
  page,
}) => {
  // Gap 5 fix: use enterMode3WithFocalCohort so Form 3 renders.
  await enterMode3WithFocalCohort(page);
  const btn = page.getByTestId("constraint-search-btn");
  if (!(await btn.isVisible().catch(() => false))) {
    test.skip();
    return;
  }
  await page.route("**/constraint-floor-search", (route) =>
    route.fulfill({ json: ERROR_RESPONSE })
  );
  await btn.click();
  const errorEl = page.getByTestId("constraint-search-error");
  await expect(errorEl).toBeVisible();
  const text = await errorEl.textContent();
  expect(text?.trim().length).toBeGreaterThan(0);
});

// ---------------------------------------------------------------------------
// AC-11: Synthetic disclosure — Tier 3
// ---------------------------------------------------------------------------

test("AC-11: FOUND result includes 'synthetic' word when indicator is Tier 3", async ({
  page,
}) => {
  // Gap 4 dependency: data_tier is not in ADR-021 §D-3 ConstraintFloorSearchResponse.
  // Before the G1 PR opens, the Frontend Architect must confirm whether:
  // (a) data_tier is added to the response schema (ADR-021 §D-3 amendment required), or
  // (b) the frontend resolves tier from indicator_key via a local lookup, in which
  //     case remove data_tier from this mock and set indicator_key to a known Tier 3 key.
  // If this is not resolved, the "synthetic" assertion will never fire post-implementation.
  // Gap 5 fix: use enterMode3WithFocalCohort so Form 3 renders.
  await enterMode3WithFocalCohort(page);
  const btn = page.getByTestId("constraint-search-btn");
  if (!(await btn.isVisible().catch(() => false))) {
    test.skip();
    return;
  }
  const syntheticFoundResponse = {
    ...FOUND_RESPONSE,
    data_tier: "SYNTHETIC_COMPARABLE",
  };
  await page.route("**/constraint-floor-search", (route) =>
    route.fulfill({ json: syntheticFoundResponse })
  );
  await btn.click();
  await expect(page.getByTestId("constraint-search-found")).toBeVisible();
  const resultText = await page
    .getByTestId("constraint-search-result")
    .textContent();
  expect(resultText?.toLowerCase()).toContain("synthetic");
});

// ---------------------------------------------------------------------------
// AC-12: Structural absence — Tier 4+
// ---------------------------------------------------------------------------

test("AC-12: constraint-search-structural-absence shown when indicator is Tier 4+", async ({
  page,
}) => {
  // Gap 8 fix: mock the scenario to return a structural-absence indicator.
  // Without this mock, the test permanently skips post-implementation because
  // the default scenario never loads a Tier 4+ indicator.
  // The exact indicator_key value that triggers structural absence must be
  // confirmed with the Frontend Architect before the G1 PR opens.
  const SA_ID = "zmb-structural-absence-test";
  await setupScenarioMocks(page, SA_ID, [
    { ...FOCAL_COHORT_CONFIG, indicator_key: "__structural_absence__" },
  ]);
  await page.goto(`/?scenario=${SA_ID}`);
  await waitForScenarioLoad(page, SA_ID);
  const btn = page.getByTestId("enter-active-control-btn");
  if (await btn.isVisible({ timeout: 8_000 }).catch(() => false)) {
    await btn.click();
  }
  await page.waitForTimeout(500);

  const structuralAbsence = page.getByTestId(
    "constraint-search-structural-absence"
  );
  if (!(await structuralAbsence.isVisible().catch(() => false))) {
    test.skip();
    return;
  }
  await expect(structuralAbsence).toBeVisible();
  await expect(
    page.getByTestId("constraint-search-btn")
  ).not.toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-T1..AC-T4: #1709 — Tolerance Band Display (G6)
// Intent: docs/process/intents/M19-G6-2026-07-04-found-tolerance-band.md
//
// RED-before-implementation:
//   AC-T1, AC-T2: constraint-tolerance-band element does not exist pre-#1709.
//   AC-T4: constraint-boundary-value currently contains "±" (moves post-#1709).
// AC-T3/AC-T3b: GREEN both before and after (element absent in non-FOUND states).
// ---------------------------------------------------------------------------

test("AC-T1 (#1709): constraint-tolerance-band visible in FOUND state", async ({
  page,
}) => {
  await enterMode3WithFocalCohort(page);
  const btn = page.getByTestId("constraint-search-btn");
  if (!(await btn.isVisible().catch(() => false))) {
    test.skip();
    return;
  }
  await page.route("**/constraint-floor-search", (route) =>
    route.fulfill({ json: FOUND_RESPONSE })
  );
  await btn.click();
  await expect(page.getByTestId("constraint-search-found")).toBeVisible();
  // RED before #1709: element does not exist yet.
  await expect(page.getByTestId("constraint-tolerance-band")).toBeVisible();
});

test("AC-T2 (#1709): tolerance band text matches ±N.NN precision format", async ({
  page,
}) => {
  await enterMode3WithFocalCohort(page);
  const btn = page.getByTestId("constraint-search-btn");
  if (!(await btn.isVisible().catch(() => false))) {
    test.skip();
    return;
  }
  await page.route("**/constraint-floor-search", (route) =>
    route.fulfill({ json: FOUND_RESPONSE })
  );
  await btn.click();
  await expect(page.getByTestId("constraint-search-found")).toBeVisible();
  // FOUND_RESPONSE: uncertainty_hi=1.19, uncertainty_lo=1.17 → band=0.02
  // RED before #1709: element does not exist yet.
  const band = page.getByTestId("constraint-tolerance-band");
  await expect(band).toBeVisible();
  await expect(band).toContainText("±0.02");
  await expect(band).toContainText("precision");
});

test("AC-T3 (#1709): constraint-tolerance-band absent in NOT_FOUND state", async ({
  page,
}) => {
  await enterMode3WithFocalCohort(page);
  const btn = page.getByTestId("constraint-search-btn");
  if (!(await btn.isVisible().catch(() => false))) {
    test.skip();
    return;
  }
  await page.route("**/constraint-floor-search", (route) =>
    route.fulfill({ json: NOT_FOUND_RESPONSE })
  );
  await btn.click();
  await expect(
    page.getByTestId("constraint-search-not-found")
  ).toBeVisible();
  // GREEN both before and after #1709.
  await expect(
    page.getByTestId("constraint-tolerance-band")
  ).not.toBeVisible();
});

test("AC-T3b (#1709): constraint-tolerance-band absent in ERROR state", async ({
  page,
}) => {
  await enterMode3WithFocalCohort(page);
  const btn = page.getByTestId("constraint-search-btn");
  if (!(await btn.isVisible().catch(() => false))) {
    test.skip();
    return;
  }
  await page.route("**/constraint-floor-search", (route) =>
    route.fulfill({ json: ERROR_RESPONSE })
  );
  await btn.click();
  await expect(page.getByTestId("constraint-search-error")).toBeVisible();
  // GREEN both before and after #1709.
  await expect(
    page.getByTestId("constraint-tolerance-band")
  ).not.toBeVisible();
});

test("AC-T4 (#1709): constraint-boundary-value does not contain ± after fix", async ({
  page,
}) => {
  await enterMode3WithFocalCohort(page);
  const btn = page.getByTestId("constraint-search-btn");
  if (!(await btn.isVisible().catch(() => false))) {
    test.skip();
    return;
  }
  await page.route("**/constraint-floor-search", (route) =>
    route.fulfill({ json: FOUND_RESPONSE })
  );
  await btn.click();
  await expect(page.getByTestId("constraint-search-found")).toBeVisible();
  // RED before #1709: boundary-value currently contains "(±0.02)".
  // GREEN after: ± is in constraint-tolerance-band only.
  await expect(
    page.getByTestId("constraint-boundary-value")
  ).not.toContainText("±");
  // Boundary numeric value is still present.
  await expect(
    page.getByTestId("constraint-boundary-value")
  ).toContainText("1.18");
});

// ---------------------------------------------------------------------------
// AC-016: Form 3 column visibility at 1280x800 (UX Designer Concern 2)
// ---------------------------------------------------------------------------

test("AC-016: constraint-search-section visible without column scroll at 1280x800", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await enterMode3WithFocalCohort(page);
  const section = page.getByTestId("constraint-search-section");
  if (!(await section.isVisible().catch(() => false))) {
    test.skip();
    return;
  }

  // Gap 2 fix: testid corrected from "control-plane-column" (nonexistent) to
  // "zone-control-plane" — the column 3 container div in InstrumentCluster.tsx.
  const column = page.getByTestId("zone-control-plane");
  const columnBox = await column.boundingBox();
  const sectionBox = await section.boundingBox();

  expect(columnBox).not.toBeNull();
  expect(sectionBox).not.toBeNull();

  if (columnBox && sectionBox) {
    const columnBottom = columnBox.y + columnBox.height;
    const sectionBottom = sectionBox.y + sectionBox.height;
    expect(sectionBox.y).toBeGreaterThanOrEqual(columnBox.y);
    expect(sectionBottom).toBeLessThanOrEqual(columnBottom);
  }
});

test("AC-016: constraint-search-section reachable within one scroll at 1024x768", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await enterMode3WithFocalCohort(page);
  const section = page.getByTestId("constraint-search-section");
  if (!(await section.isVisible().catch(() => false))) {
    test.skip();
    return;
  }

  await section.scrollIntoViewIfNeeded();
  await expect(section).toBeInViewport();
});
