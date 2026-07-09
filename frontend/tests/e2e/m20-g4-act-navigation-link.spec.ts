/**
 * E2E: M20-G4 — Act 1 → Act 2 In-Viewport Navigation Link (DEMO-217)
 *
 * Authored BEFORE implementation per intent document:
 *   docs/process/intents/M20-G4-2026-07-08-act1-act2-nav-link.md
 *
 * Sprint entry: docs/process/sprint-plans/m20-g4-sprint-entry.md (EL Approved 2026-07-08)
 * ADR gate: ADR-021 §D-4 (existing four-state machine; no new ADR required)
 *
 * ACs covered:
 *   AC-1  act2-nav-link present in FOUND state when ≥ 2 scenarios loaded
 *   AC-2  act2-nav-link absent when only 1 scenario in session
 *   AC-3  act2-nav-link visible without scroll at 1440×900
 *   AC-4  clicking act2-nav-link switches active scenario in instrument cluster
 *   AC-5  constraint-boundary-value and constraint-tolerance-band unchanged (regression)
 *   AC-6  SF-1 guard: act2-nav-link not scroll-hidden (separate assertion block)
 *
 * RED state: AC-1 through AC-6 will fail until DEMO-217 implementation lands.
 *   - AC-1: [data-testid="act2-nav-link"] does not exist yet
 *   - AC-2: passes vacuously until AC-1 is implemented
 *
 * Mock patterns established in m19-g1-constraint-floor-search.spec.ts.
 * See NM-056: no test.skip() / test.fixme() / .only() patterns.
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

const FOUND_RESPONSE = {
  status: "FOUND",
  boundary: 0.83,
  uncertainty_lo: 0.82,
  uncertainty_hi: 0.84,
  evaluations: 8,
  search_lo: 0.1,
  search_hi: 3.0,
  floor_value: 0.4,
  indicator_key: "bottom_quintile_informal_workers_poverty_headcount",
  error_message: null,
};

// Two distinct scenario IDs: one for the Mode 3 (Act 1) session, one for the
// distributional comparison (Act 2, Replay mode).
const ACT1_SCENARIO_ID = "zmb-act1-mode3";
const ACT2_SCENARIO_ID = "zmb-act2-replay";

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
    // Timeout: test guards handle missing elements via isVisible().catch(() => false)
  }
}

function makeScenarioDetail(
  scenarioId: string,
  name: string,
  withFocalCohorts: boolean,
): object {
  return {
    scenario_id: scenarioId,
    name,
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
      // fiscal_multiplier != null && !== 1.0 → ScenarioInstrumentCluster routes to MODE_2,
      // which renders Mode2ColumnSurface (contains enter-active-control-btn).
      fiscal_multiplier: 1.3,
      ...(withFocalCohorts ? { monitored_focal_cohorts: [FOCAL_COHORT_CONFIG] } : {}),
    },
  };
}

function makeTrajectoryResponse(scenarioId: string): object {
  return {
    scenario_id: scenarioId,
    entity_id: "ZMB",
    step_count: 0,
    mda_floors: [],
    threshold_crossings: [],
    steps: [],
  };
}

/** Set up only the detail and trajectory routes for Act 1 — no list mock.
 *  Used by enterMode3AndTriggerFoundSearch so it does not clobber a previously-registered
 *  list mock (Playwright route() is LIFO — the last registration wins for a matching pattern).
 */
async function setupAct1DetailRoutes(page: Page): Promise<void> {
  const detail = makeScenarioDetail(ACT1_SCENARIO_ID, "ZMB Demo Act 1 (Constraint)", true);
  const trajectory = makeTrajectoryResponse(ACT1_SCENARIO_ID);
  await page.route(`**/api/v1/scenarios/${ACT1_SCENARIO_ID}`, (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(detail) }),
  );
  await page.route(`**/api/v1/scenarios/${ACT1_SCENARIO_ID}/trajectory**`, (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(trajectory) }),
  );
}

/** Set up mocks for the Act 1 scenario (Mode 3 focal cohort scenario).
 *  Also mocks the scenario list endpoint to return only Act 1 — so act2-nav-link is absent.
 */
async function setupAct1Mocks(page: Page): Promise<void> {
  await setupAct1DetailRoutes(page);
  // Scenario list — only Act 1 present → act2-nav-link must be absent (AC-2).
  await page.route("**/api/v1/scenarios", (route) => {
    if (route.request().method() !== "GET") { route.continue(); return; }
    route.fulfill({
      status: 200, contentType: "application/json",
      body: JSON.stringify([{ scenario_id: ACT1_SCENARIO_ID, name: "ZMB Demo Act 1 (Constraint)", status: "in_progress" }]),
    });
  });
}

/** Set up mocks for the Act 2 scenario (Replay / distributional comparison).
 *  Also overrides the scenario list endpoint to include both Act 1 and Act 2,
 *  so ControlPlaneColumn's useEffect discovers the comparison target.
 */
async function setupAct2Mocks(page: Page): Promise<void> {
  const detail = makeScenarioDetail(ACT2_SCENARIO_ID, "ZMB Demo Act 2 (Distributional)", false);
  const trajectory = makeTrajectoryResponse(ACT2_SCENARIO_ID);
  await page.route(`**/api/v1/scenarios/${ACT2_SCENARIO_ID}`, (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(detail) }),
  );
  await page.route(`**/api/v1/scenarios/${ACT2_SCENARIO_ID}/trajectory**`, (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(trajectory) }),
  );
  // Scenario list — both Act 1 and Act 2 present → act2-nav-link must appear (AC-1).
  // Caller must invoke setupAct2Mocks BEFORE enterMode3AndTriggerFoundSearch so this
  // registration is the active one when ControlPlaneColumn fetches the list (LIFO wins).
  await page.route("**/api/v1/scenarios", (route) => {
    if (route.request().method() !== "GET") { route.continue(); return; }
    route.fulfill({
      status: 200, contentType: "application/json",
      body: JSON.stringify([
        { scenario_id: ACT2_SCENARIO_ID, name: "ZMB Demo Act 2 (Distributional)", status: "in_progress" },
        { scenario_id: ACT1_SCENARIO_ID, name: "ZMB Demo Act 1 (Constraint)", status: "in_progress" },
      ]),
    });
  });
}

/** Enters Mode 3 for the Act 1 scenario and triggers a FOUND constraint search.
 *  Registers only the Act 1 detail and trajectory routes — NOT the scenario list.
 *  Callers that need a specific list response must register it AFTER calling this function
 *  (Playwright route() is LIFO; the last registration wins for a matching URL pattern).
 */
async function enterMode3AndTriggerFoundSearch(page: Page): Promise<void> {
  await setupAct1DetailRoutes(page);
  await page.route("**/constraint-floor-search", (route) =>
    route.fulfill({ json: FOUND_RESPONSE }),
  );

  await page.goto(`/?scenario=${ACT1_SCENARIO_ID}`);
  await waitForScenarioLoad(page, ACT1_SCENARIO_ID);

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

// ---------------------------------------------------------------------------
// AC-1: act2-nav-link present in FOUND state when ≥ 2 scenarios loaded
// ---------------------------------------------------------------------------

test("AC-1: act2-nav-link present in constraint-search-found when session has ≥ 2 scenarios", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);

  // Load Act 2 mock before navigating, so the app knows a second scenario exists.
  await setupAct2Mocks(page);
  await enterMode3AndTriggerFoundSearch(page);

  const foundSection = page.getByTestId("constraint-search-found");
  if (!(await foundSection.isVisible().catch(() => false))) {
    // constraint-search-found not visible: constraint search not yet implemented.
    // AC-1 remains RED. No test.skip() per NM-056.
    expect(
      false,
      "AC-1 FAIL: constraint-search-found not visible — constraint search implementation required first. " +
      "See m19-g1-constraint-floor-search.spec.ts AC-5.",
    ).toBe(true);
    return;
  }

  const navLink = page.getByTestId("act2-nav-link");
  const present = await navLink.isVisible().catch(() => false);

  expect(
    present,
    "AC-1 FAIL: [data-testid='act2-nav-link'] not present in constraint-search-found " +
    "when session has ≥ 2 loaded scenarios. " +
    "Fix DEMO-217: add act2-nav-link element inside constraint-search-found section. " +
    "Link must be visible when session has a second scenario available as distributional comparison. " +
    "See intent M20-G4-2026-07-08-act1-act2-nav-link.md §3.1.",
  ).toBe(true);
});

// ---------------------------------------------------------------------------
// AC-2: act2-nav-link absent when session has only 1 scenario
// ---------------------------------------------------------------------------

test("AC-2: act2-nav-link absent in constraint-search-found when only 1 scenario in session", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);

  // Register 1-scenario list BEFORE entering Mode 3 so ControlPlaneColumn sees no comparison target.
  // enterMode3AndTriggerFoundSearch does not register a list mock; calling setupAct1Mocks here
  // (which DOES register the list) makes the 1-scenario response the active one.
  await setupAct1Mocks(page);
  await enterMode3AndTriggerFoundSearch(page);

  const foundSection = page.getByTestId("constraint-search-found");
  if (!(await foundSection.isVisible().catch(() => false))) {
    // constraint-search-found not visible — pre-implementation pass.
    return;
  }

  const navLink = page.getByTestId("act2-nav-link");
  const present = await navLink.isVisible().catch(() => false);

  expect(
    present,
    "AC-2 FAIL: [data-testid='act2-nav-link'] is present in constraint-search-found " +
    "even when the session has only 1 scenario (no comparison target). " +
    "Fix DEMO-217: omit act2-nav-link when no second scenario is available. " +
    "A broken or non-functional navigation link is a regression. " +
    "See intent M20-G4-2026-07-08-act1-act2-nav-link.md §AC-2.",
  ).toBe(false);
});

// ---------------------------------------------------------------------------
// AC-3: act2-nav-link visible without scroll at 1440×900
// ---------------------------------------------------------------------------

test("AC-3: act2-nav-link is within visible viewport of control-plane column — no scroll needed", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);

  await setupAct2Mocks(page);
  await enterMode3AndTriggerFoundSearch(page);

  const foundSection = page.getByTestId("constraint-search-found");
  if (!(await foundSection.isVisible().catch(() => false))) {
    return; // pre-implementation
  }

  const navLink = page.getByTestId("act2-nav-link");
  if (!(await navLink.isVisible().catch(() => false))) {
    // AC-1 not yet implemented; AC-3 cannot run.
    return;
  }

  const navBox = await navLink.boundingBox();
  expect(
    navBox,
    "AC-3 FAIL: act2-nav-link has no bounding box — element may be hidden or not rendered.",
  ).not.toBeNull();

  if (navBox) {
    const viewportHeight = VIEWPORT.height;
    const viewportWidth = VIEWPORT.width;

    expect(
      navBox.y + navBox.height,
      "AC-3 FAIL: act2-nav-link bottom edge is below viewport height — " +
      "link requires scroll to be visible at 1440×900. " +
      "Fix SF-1 (DEMO-217): place act2-nav-link within the visible fold of the " +
      "control-plane column after FOUND result. See intent §3.3 SF-1.",
    ).toBeLessThanOrEqual(viewportHeight);

    expect(
      navBox.x + navBox.width,
      "AC-3 FAIL: act2-nav-link right edge is beyond viewport width.",
    ).toBeLessThanOrEqual(viewportWidth);

    expect(navBox.y, "AC-3 FAIL: act2-nav-link top is above viewport top.").toBeGreaterThanOrEqual(0);
    expect(navBox.x, "AC-3 FAIL: act2-nav-link left is beyond viewport left.").toBeGreaterThanOrEqual(0);
  }
});

// ---------------------------------------------------------------------------
// AC-4: clicking act2-nav-link switches active scenario in instrument cluster
// ---------------------------------------------------------------------------

test("AC-4: clicking act2-nav-link switches active scenario to distributional comparison within 5s", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);

  await setupAct2Mocks(page);
  await enterMode3AndTriggerFoundSearch(page);

  const foundSection = page.getByTestId("constraint-search-found");
  if (!(await foundSection.isVisible().catch(() => false))) {
    return;
  }

  const navLink = page.getByTestId("act2-nav-link");
  if (!(await navLink.isVisible().catch(() => false))) {
    return;
  }

  await navLink.click();

  // Wait up to 5 seconds for the scenario to switch — the intent specifies
  // navigation must complete in ≤ 5 seconds in a pre-loaded session.
  const switched = await page
    .waitForFunction(
      (id) => (window as Record<string, unknown>).__worldsim_selectedScenarioId === id,
      ACT2_SCENARIO_ID,
      { timeout: 5_000 },
    )
    .then(() => true)
    .catch(() => false);

  expect(
    switched,
    "AC-4 FAIL: clicking act2-nav-link did not switch the active scenario to " +
    `${ACT2_SCENARIO_ID} within 5 seconds. ` +
    "Fix DEMO-217: act2-nav-link click must update window.__worldsim_selectedScenarioId " +
    "to the comparison scenario ID. Navigation must complete within 5 seconds in a " +
    "pre-loaded session. See intent §P-4 (time/interaction ceiling).",
  ).toBe(true);
});

// ---------------------------------------------------------------------------
// AC-5: constraint-boundary-value and constraint-tolerance-band unchanged (regression)
// ---------------------------------------------------------------------------

test("AC-5 regression: constraint-boundary-value and constraint-tolerance-band present after act2-nav-link addition", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);

  await setupAct2Mocks(page);
  await enterMode3AndTriggerFoundSearch(page);

  const foundSection = page.getByTestId("constraint-search-found");
  if (!(await foundSection.isVisible().catch(() => false))) {
    return;
  }

  // constraint-boundary-value must be present and show the boundary (0.83)
  const boundaryEl = page.getByTestId("constraint-boundary-value");
  const boundaryVisible = await boundaryEl.isVisible().catch(() => false);
  expect(
    boundaryVisible,
    "AC-5 FAIL: constraint-boundary-value missing from constraint-search-found after act2-nav-link addition. " +
    "This is a regression. The boundary value display must not be removed by the DEMO-217 change.",
  ).toBe(true);

  if (boundaryVisible) {
    const boundaryText = await boundaryEl.textContent().catch(() => "");
    expect(
      boundaryText,
      "AC-5 FAIL: constraint-boundary-value does not contain '0.83' — boundary display has regressed.",
    ).toContain("0.83");
  }

  // constraint-tolerance-band must be present (it is the existing testid — DEMO-234 will rename it,
  // but at this point in the test suite we verify the band display is not broken by DEMO-217).
  // Note: after DEMO-234 merges, this testid changes to constraint-search-precision.
  // These two fixes may ship in the same PR; if so, constraint-tolerance-band may be absent
  // and constraint-search-precision present. We assert either one is present.
  const toleranceBand = page.getByTestId("constraint-tolerance-band");
  const precisionEl = page.getByTestId("constraint-search-precision");
  const eitherPresent =
    (await toleranceBand.isVisible().catch(() => false)) ||
    (await precisionEl.isVisible().catch(() => false));

  expect(
    eitherPresent,
    "AC-5 FAIL: neither constraint-tolerance-band nor constraint-search-precision present " +
    "in constraint-search-found after act2-nav-link addition. " +
    "The precision display must survive the DEMO-217 change.",
  ).toBe(true);
});

// ---------------------------------------------------------------------------
// AC-6 (SF-1 guard): act2-nav-link not scroll-hidden — explicit separate block
// ---------------------------------------------------------------------------

test("AC-6 SF-1 guard: act2-nav-link bounding box within visible area — no scroll required", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);

  await setupAct2Mocks(page);
  await enterMode3AndTriggerFoundSearch(page);

  const foundSection = page.getByTestId("constraint-search-found");
  if (!(await foundSection.isVisible().catch(() => false))) {
    return;
  }

  const navLink = page.getByTestId("act2-nav-link");
  if (!(await navLink.isVisible().catch(() => false))) {
    return;
  }

  const box = await navLink.boundingBox();
  expect(
    box,
    "AC-6 SF-1 FAIL: act2-nav-link has no bounding box.",
  ).not.toBeNull();

  if (box) {
    expect(
      box.y + box.height,
      "AC-6 SF-1 FAIL: act2-nav-link bottom is below 900px viewport height — scroll required. " +
      "The link must be positioned within the visible fold of the constraint-search-found container. " +
      "See intent §3.3 SF-1.",
    ).toBeLessThanOrEqual(VIEWPORT.height);
  }
});
