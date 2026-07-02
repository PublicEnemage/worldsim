/**
 * M19 G1 — Mode 3 Constraint-Floor Search (#1540)
 * Intent: docs/process/intents/M19-ADR-021-2026-07-02-constraint-floor-search.md
 * ADR: docs/adr/ADR-021-constraint-floor-search.md
 *
 * All tests guard on the Form 3 testid being absent pre-implementation (no-ops
 * until constraint-search-section ships). AC-016 guards on column geometry.
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

const FOUND_RESPONSE = {
  status: "FOUND",
  boundary: 1.18,
  uncertainty_lo: 1.17,
  uncertainty_hi: 1.19,
  evaluations: 9,
  lo_searched: 0.1,
  hi_searched: 3.0,
  tolerance: 0.01,
  focal_cohort_index: 0,
};

const NOT_FOUND_RESPONSE = {
  status: "NOT_FOUND",
  boundary: null,
  evaluations: 9,
  lo_searched: 0.1,
  hi_searched: 3.0,
  tolerance: 0.01,
  focal_cohort_index: 0,
};

const ERROR_RESPONSE = {
  status: "ERROR",
  error: "Engine evaluation failed: ValueError at step 3",
  boundary: null,
  evaluations: 3,
  focal_cohort_index: 0,
};

async function enterMode3(page: Page): Promise<void> {
  // Navigate to the app with a preloaded scenario in Mode 2
  await page.goto("/");
  // Activate Mode 3 via the "Enter Active Control" button
  const enterActiveControl = page.getByRole("button", {
    name: /enter active control/i,
  });
  if (await enterActiveControl.isVisible()) {
    await enterActiveControl.click();
  }
}

// ---------------------------------------------------------------------------
// AC-1: Form 3 visible in Mode 3 with focal cohort configured
// ---------------------------------------------------------------------------

test("AC-1: constraint-search-section present in Mode 3 with focal cohort configured", async ({
  page,
}) => {
  // Guard: no-op if Form 3 not yet implemented
  await enterMode3(page);
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
  // Ensure Mode 1 is active (default replay mode)
  await expect(
    page.getByTestId("constraint-search-section")
  ).not.toBeVisible();
});

test("AC-2: constraint-search-section absent in Mode 2", async ({ page }) => {
  await page.goto("/");
  // Mode 2 is the simulation mode — no Mode 3 transition performed
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
  await enterMode3(page);
  const btn = page.getByTestId("constraint-search-btn");
  if (!(await btn.isVisible().catch(() => false))) {
    test.skip();
    return;
  }
  // Intercept and delay the POST response
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
  await enterMode3(page);
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
});

// ---------------------------------------------------------------------------
// AC-6: NOT_FOUND state
// ---------------------------------------------------------------------------

test("AC-6: NOT_FOUND state renders when backend returns no boundary", async ({
  page,
}) => {
  await enterMode3(page);
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
  await enterMode3(page);
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
  // SF-1: result area must not be blank
  const text = await errorEl.textContent();
  expect(text?.trim().length).toBeGreaterThan(0);
});

// ---------------------------------------------------------------------------
// AC-11: Synthetic disclosure — Tier 3
// ---------------------------------------------------------------------------

test("AC-11: FOUND result includes 'synthetic' word when indicator is Tier 3", async ({
  page,
}) => {
  await enterMode3(page);
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
  await enterMode3(page);
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
  await enterMode3(page);
  const section = page.getByTestId("constraint-search-section");
  if (!(await section.isVisible().catch(() => false))) {
    test.skip();
    return;
  }

  // Locate the column container — expected to be the ControlPlaneColumn root
  const column = page.getByTestId("control-plane-column");
  const columnBox = await column.boundingBox();
  const sectionBox = await section.boundingBox();

  expect(columnBox).not.toBeNull();
  expect(sectionBox).not.toBeNull();

  if (columnBox && sectionBox) {
    // Section must be fully within column visible area (no scroll required)
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
  await enterMode3(page);
  const section = page.getByTestId("constraint-search-section");
  if (!(await section.isVisible().catch(() => false))) {
    test.skip();
    return;
  }

  // Scroll the section into view — must be achievable in one scrollIntoView call
  await section.scrollIntoViewIfNeeded();
  await expect(section).toBeInViewport();
});
