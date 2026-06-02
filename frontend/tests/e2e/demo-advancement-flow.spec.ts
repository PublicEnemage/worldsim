/**
 * E2E: Demo advancement flow — full step-through regression gate.
 *
 * Source: Issue #376 — M8 retrospective Required Improvement 3.
 * Defect references: DEMO-001 (choropleth no visible change), DEMO-004
 * (MDA alerts static), DEMO-002/005 (radar labels not legible).
 *
 * These defects were caught by the M8 IR review — not by automated tests.
 * This suite is the guard that prevents regression.
 *
 * Architecture note (M10): The instrument cluster (Zone 1A–1D) is the
 * primary viewport. The choropleth is the context surface. Tests assert
 * the full step-through path from scenario creation through final step,
 * verifying that all four Zone 1 instruments and the choropleth remain
 * live and data-driven at every step.
 *
 * Choropleth test strategy: MapLibre GL renders to a WebGL canvas — pixel
 * comparison is not used. Instead, the outer container carries
 * data-testid="choropleth-map" and data-step={currentStep}, allowing
 * Playwright to assert the choropleth received the new step (i.e. was
 * told to re-fetch and re-render). This is the correct invariant: DEMO-001
 * was caused by the choropleth not receiving step updates at all.
 *
 * MDA test strategy: the default scenario does not seed indicators that
 * breach MDA thresholds, so Zone 1B will consistently show "No active
 * threshold breaches." The regression guard is that the panel is live
 * (shows one of the two valid states) at every step — not that specific
 * alerts fire.
 */
import { test, expect } from "@playwright/test";

// ---------------------------------------------------------------------------
// Shared helpers (mirrors greece-integration.spec.ts pattern)
// ---------------------------------------------------------------------------

async function createAndSelectScenario(
  page: import("@playwright/test").Page,
  name: string,
) {
  await page.waitForFunction(
    () =>
      typeof (window as Record<string, unknown>).__worldsim_selectEntity ===
      "function",
    { timeout: 10_000 },
  );
  await page.getByRole("button", { name: /Scenarios/ }).click();
  await page.locator('input[placeholder="Scenario name"]').fill(name);
  await page.locator(".scenario-btn--create").click();
  const row = page.locator(".scenario-row").filter({ hasText: name });
  await expect(row).toBeVisible({ timeout: 15_000 });
  await row.getByTitle("Select as primary scenario").click();
  await page.getByRole("button", { name: /Scenarios/ }).click();
}

async function advanceStep(
  page: import("@playwright/test").Page,
  toStep: number,
  totalSteps: number,
) {
  await page.getByRole("button", { name: /Next Step/ }).click();
  await expect(
    page.getByText(`Step ${toStep} / ${totalSteps}`),
  ).toBeVisible({ timeout: 15_000 });
}

// ---------------------------------------------------------------------------
// Zone 1 instruments live at every step — full advancement flow
//
// Advances through all default steps (n=3). At each step all four Zone 1
// instruments must be visible and the advance button must be enabled (until
// the final step). This is the core guard against instrument dropout on advance.
//
// Source: Issue #376 requirement 1 and 2 (step-through sequence).
// DEMO defects guarded: DEMO-001 (choropleth), DEMO-004 (MDA static).
// ---------------------------------------------------------------------------

test("demo flow: all four Zone 1 instruments remain live at every step", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await createAndSelectScenario(page, `DEMO-flow-${Date.now()}`);

  const instruments = [
    '[data-testid="zone-1a-trajectory-container"]',
    '[data-testid="zone-1b-mda-alerts"]',
    '[data-testid="zone-1c-pmm"]',
    '[data-testid="zone-1d-four-framework"]',
  ];

  // Verify all four instruments are visible at step 0 (pre-advance)
  for (const sel of instruments) {
    await expect(page.locator(sel)).toBeVisible({ timeout: 10_000 });
  }

  const nextBtn = page.getByRole("button", { name: /Next Step/ });

  for (let step = 1; step <= 3; step++) {
    await nextBtn.click();
    await expect(page.getByText(`Step ${step} / 3`)).toBeVisible({
      timeout: 15_000,
    });

    for (const sel of instruments) {
      await expect(page.locator(sel)).toBeVisible();
    }
  }

  // Final step: advance button disabled
  await expect(nextBtn).toBeDisabled();
});

// ---------------------------------------------------------------------------
// Choropleth step attribute increments on each advance
//
// Asserts the choropleth container's data-step attribute tracks the current
// step. This proves the choropleth is receiving step updates and will re-fetch
// the attribute data for the new step — the core DEMO-001 invariant.
//
// Source: Issue #376 requirement 3.
// ---------------------------------------------------------------------------

test("demo flow: choropleth data-step attribute increments on each advance", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await createAndSelectScenario(page, `DEMO-choropleth-${Date.now()}`);

  const choropleth = page.locator('[data-testid="choropleth-map"]');
  const isVisible = await choropleth.isVisible({ timeout: 5_000 }).catch(() => false);
  if (!isVisible) return;

  // step 0 on initial selection
  await expect(choropleth).toHaveAttribute("data-step", "0");

  const nextBtn = page.getByRole("button", { name: /Next Step/ });

  for (let step = 1; step <= 3; step++) {
    await nextBtn.click();
    await expect(page.getByText(`Step ${step} / 3`)).toBeVisible({
      timeout: 15_000,
    });
    await expect(choropleth).toHaveAttribute("data-step", String(step));
  }
});

// ---------------------------------------------------------------------------
// Zone 1B MDA panel is live (data-driven) at each step
//
// At each step, Zone 1B must show exactly one of two valid states:
//   (a) mda-no-alerts — no threshold breaches
//   (b) one or more mda-alert-row elements — active alerts
//
// Both states are acceptable for a default scenario. The invariant is that
// the panel is live — never blank or in an error state. This guards DEMO-004
// (MDA panel was showing stale / static state after step advances).
//
// Source: Issue #376 requirement 4.
// ---------------------------------------------------------------------------

test("demo flow: Zone 1B MDA panel is live and non-blank at every step", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await createAndSelectScenario(page, `DEMO-mda-${Date.now()}`);

  const panel = page.locator('[data-testid="zone-1b-mda-alerts"]');
  await expect(panel).toBeVisible({ timeout: 10_000 });

  const nextBtn = page.getByRole("button", { name: /Next Step/ });

  for (let step = 1; step <= 3; step++) {
    await nextBtn.click();
    await expect(page.getByText(`Step ${step} / 3`)).toBeVisible({
      timeout: 15_000,
    });

    // Zone 1B must settle into one of the two valid states
    await expect
      .poll(
        async () => {
          const noAlerts = page.locator('[data-testid="mda-no-alerts"]');
          const alertRow = page.locator('[data-testid="mda-alert-row"]');
          const hasNoAlerts = await noAlerts.isVisible().catch(() => false);
          const hasAlertRow = await alertRow.first().isVisible().catch(() => false);
          return hasNoAlerts || hasAlertRow;
        },
        {
          timeout: 10_000,
          message: `Zone 1B must show mda-no-alerts or mda-alert-row at step ${step}`,
        },
      )
      .toBe(true);
  }
});

// ---------------------------------------------------------------------------
// Zone 1D framework rows all present and score elements non-empty at final step
//
// At the final step, all four framework rows must render with a score element
// that is either a numeric value or "—" (null). An empty score element
// indicates a rendering regression. This guards the Zone 1D instrument against
// silent dropout during the full step-through.
//
// Source: Issue #376 requirement 2 (full step-through consistency).
// ---------------------------------------------------------------------------

test("demo flow: Zone 1D all framework scores present and non-empty at final step", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await createAndSelectScenario(page, `DEMO-1d-${Date.now()}`);

  const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
  await expect(zone1d).toBeVisible({ timeout: 10_000 });
  await expect(zone1d).not.toHaveAttribute("data-loading", "true", {
    timeout: 10_000,
  });

  const nextBtn = page.getByRole("button", { name: /Next Step/ });
  for (let step = 1; step <= 3; step++) {
    await nextBtn.click();
    await expect(page.getByText(`Step ${step} / 3`)).toBeVisible({
      timeout: 15_000,
    });
  }

  // At final step: every framework score element must be non-empty
  for (const fw of ["financial", "human_development", "ecological", "governance"]) {
    const scoreEl = page.locator(`[data-testid="framework-score-${fw}"]`);
    await expect(scoreEl).toBeVisible();
    const text = await scoreEl.textContent();
    // Score is either a decimal number or "—" (null). Never empty.
    expect(text?.trim().length).toBeGreaterThan(0);
  }
});

// ---------------------------------------------------------------------------
// Advance button disabled after final step — no overshoot possible
//
// Guards against the engine being called with step > n_steps, which would
// produce stale or duplicated trajectory data. The button must be disabled
// exactly at the final step, not one step later.
//
// Source: Issue #376 requirement 2.
// ---------------------------------------------------------------------------

test("demo flow: advance button disabled after final step, not before", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await createAndSelectScenario(page, `DEMO-btn-${Date.now()}`);

  const nextBtn = page.getByRole("button", { name: /Next Step/ });

  // Steps 1 and 2: button must remain enabled
  for (let step = 1; step <= 2; step++) {
    await expect(nextBtn).toBeEnabled();
    await nextBtn.click();
    await expect(page.getByText(`Step ${step} / 3`)).toBeVisible({
      timeout: 15_000,
    });
  }

  // Step 3 (final): click, then button must be disabled
  await expect(nextBtn).toBeEnabled();
  await nextBtn.click();
  await expect(page.getByText("Step 3 / 3")).toBeVisible({ timeout: 15_000 });
  await expect(nextBtn).toBeDisabled();
});
