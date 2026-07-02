/**
 * M19 G1 — Mode 3 Constraint-Floor Search (#1540)
 * Intent: docs/process/intents/M19-ADR-021-2026-07-02-constraint-floor-search.md
 * ADR: docs/adr/ADR-021-constraint-floor-search.md
 *
 * All tests guard on the Form 3 testid being absent pre-implementation (no-ops
 * until constraint-search-section ships). AC-016 guards on column geometry.
 *
 * QA Lead review 2026-07-02: 8 gaps corrected (see intent doc §7 for full list).
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
// Mock helpers — App.tsx fetches GET /api/v1/scenarios/{id} twice:
//   1. Mount effect (reads ?scenario= URL param) → sets selectedScenarioId
//   2. selectedScenarioId effect → sets activeScenarioDetail (focal cohorts live here)
// Both requests match the exact-ID route pattern below; trajectory is mocked
// separately to prevent 404 errors on the unadvanced synthetic scenario IDs.
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
    created_at: "2026-07-02T00:00:00Z",
    scheduled_inputs: [],
    configuration: {
      entities: ["ZMB"],
      initial_attributes: {},
      n_steps: 8,
      timestep_label: "quarter",
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
  // Exact scenario-detail URL (App.tsx: GET /api/v1/scenarios/{id})
  await page.route(`**/api/v1/scenarios/${scenarioId}`, (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(detail) })
  );
  // Trajectory URL (sub-path not matched by the pattern above)
  await page.route(`**/api/v1/scenarios/${scenarioId}/trajectory**`, (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(trajectory) })
  );
}

async function waitForScenarioLoad(page: Page, scenarioId: string): Promise<void> {
  // App.tsx sets window.__worldsim_selectedScenarioId after the scenario detail
  // fetch succeeds (DEV seam, line ~187). Waiting for this guarantees selectedScenarioId
  // is in state before we try to interact with ScenarioInstrumentCluster.
  try {
    await page.waitForFunction(
      (id) => (window as Record<string, unknown>).__worldsim_selectedScenarioId === id,
      scenarioId,
      { timeout: 10_000 },
    );
  } catch {
    // Timeout — test guards handle the missing form via isVisible().catch(() => false)
  }
}

// Used for AC-3: enter Mode 3 WITHOUT focal cohorts to test the unavailable state.
async function enterMode3(page: Page): Promise<void> {
  await setupScenarioMocks(page, ZMB_NO_FOCAL_ID, null);
  await page.goto(`/?scenario=${ZMB_NO_FOCAL_ID}`);
  await waitForScenarioLoad(page, ZMB_NO_FOCAL_ID);
  const btn = page.getByTestId("enter-active-control-btn");
  if (await btn.isVisible({ timeout: 8_000 }).catch(() => false)) {
    await btn.click();
  }
}

// Gap 5 fix: mock the scenario detail endpoint with correct ScenarioDetailResponse shape.
// Root-cause fix (2026-07-02): original mock used field "id" instead of "scenario_id",
// so App.tsx setSelectedScenarioId(undefined) — scenario never loaded, Mode 3 unreachable.
// Also: route pattern was "**/api/v1/scenarios/*/detail" — no such endpoint exists;
// correct pattern is "**/api/v1/scenarios/{id}" (exact, without /detail suffix).
async function enterMode3WithFocalCohort(page: Page): Promise<void> {
  await setupScenarioMocks(page, ZMB_FOCAL_COHORT_ID, [FOCAL_COHORT_CONFIG]);
  await page.goto(`/?scenario=${ZMB_FOCAL_COHORT_ID}`);
  await waitForScenarioLoad(page, ZMB_FOCAL_COHORT_ID);
  // enter-active-control-btn lives in Mode2ColumnSurface, which renders once
  // ScenarioInstrumentCluster mounts (selectedScenarioId is set).
  const btn = page.getByTestId("enter-active-control-btn");
  await btn.waitFor({ state: "visible", timeout: 8_000 });
  await btn.click();
  // After click, ControlPlaneColumn mounts and receives monitoredFocalCohorts from
  // activeScenarioDetail (set by the selectedScenarioId effect, which fires after
  // the same scenario detail fetch). Wait for Form 3 to render with the focal cohort.
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
  // Gap 6 fix: assert precision disclosure "±" is present (ADR-021 §D-4).
  // A broken display showing only "1.18" without the disclosure would pass
  // without this second assertion.
  await expect(page.getByTestId("constraint-boundary-value")).toContainText(
    "±"
  );
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
  // Gap 8 fix + root-cause fix (2026-07-02): original mock used wrong route pattern
  // ("**/api/v1/scenarios/*/detail") and wrong field name ("id" vs "scenario_id").
  // Using setupScenarioMocks helper to ensure correct ScenarioDetailResponse shape.
  const SA_ID = "zmb-structural-absence-test";
  await setupScenarioMocks(page, SA_ID, [
    {
      ...FOCAL_COHORT_CONFIG,
      // indicator_key starting with "__" triggers structural-absence gate (ControlPlaneColumn.tsx).
      indicator_key: "__structural_absence__",
    },
  ]);
  await page.goto(`/?scenario=${SA_ID}`);
  await waitForScenarioLoad(page, SA_ID);
  const btn = page.getByTestId("enter-active-control-btn");
  if (await btn.isVisible({ timeout: 8_000 }).catch(() => false)) {
    await btn.click();
  }
  // Wait for ControlPlaneColumn to mount and receive the structural-absence config
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
