/**
 * E2E: Mode 3 Active Control (G6b, Issue #753).
 *
 * Golden path:
 *   1. Create scenario, advance at least one step
 *   2. Enable Mode 3 via toggle
 *   3. Change fiscal multiplier, click Apply Change
 *   4. Recompute badge appears ("Recomputing…") while advance loop runs
 *   5. Badge disappears on completion; branch trajectory curves are visible
 *
 * The test uses data-testid anchors defined in ControlPlane.tsx and
 * ScenarioInstrumentCluster.tsx. It does not assert exact numeric output,
 * only that the UI state transitions correctly (idle → computing → complete).
 */
import { test, expect } from "@playwright/test";

test("Mode 3 — enable, apply control change, recompute completes", async ({ page }) => {
  const scenarioName = `E2E-Mode3-${Date.now()}`;

  await page.goto("/");

  await page.waitForFunction(
    () =>
      typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
    { timeout: 10_000 },
  );

  // Open scenarios panel and create scenario.
  await page.getByRole("button", { name: /Scenarios/ }).click();
  await page.locator('input[placeholder="Scenario name"]').fill(scenarioName);
  await page.locator(".scenario-btn--create").click();

  // Wait for scenario row.
  await page.locator(".scenario-row").filter({ hasText: scenarioName }).waitFor({
    timeout: 10_000,
  });

  // Select the scenario.
  await page.locator(".scenario-row").filter({ hasText: scenarioName }).click();

  // Advance one step so branch_from_step = 0 is valid.
  const advanceBtn = page.getByRole("button", { name: /Advance/ });
  await advanceBtn.waitFor({ timeout: 10_000 });
  await advanceBtn.click();

  // Wait for step indicator to show Step 1.
  await expect(page.locator('[data-testid="step-indicator"]')).toContainText("1", {
    timeout: 15_000,
  });

  // Enable Mode 3.
  await page.locator('[data-testid="mode3-toggle"]').click();

  // ControlPlane should appear.
  await expect(page.locator('[data-testid="zone-control-plane"]')).toBeVisible({
    timeout: 3_000,
  });

  // Move fiscal multiplier to 1.5 (default is 1.0 — drag or set via evaluate).
  // Playwright range input: set value and dispatch input event.
  await page.locator('[data-testid="fiscal-multiplier-slider"]').evaluate(
    (el: HTMLInputElement) => {
      el.value = "1.5";
      el.dispatchEvent(new Event("input", { bubbles: true }));
    },
  );

  // Verify display updated.
  await expect(page.locator('[data-testid="fiscal-multiplier-value"]')).toContainText("1.50");

  // Click Apply Change — triggers branch creation and advance loop.
  await page.locator('[data-testid="apply-control-change"]').click();

  // Recompute badge should appear while computing.
  await expect(page.locator('[data-testid="recompute-badge"]')).toBeVisible({
    timeout: 5_000,
  });
  await expect(page.locator('[data-testid="recompute-badge"]')).toContainText("Recomputing");

  // Wait for badge to disappear — recompute complete.
  await expect(page.locator('[data-testid="recompute-badge"]')).not.toBeVisible({
    timeout: 30_000,
  });

  // Branch anchor annotation should appear (step > 0).
  await expect(page.locator('[data-testid="branch-anchor-label"]')).toBeVisible();
  await expect(page.locator('[data-testid="branch-anchor-label"]')).toContainText("Branched");
});

test("Mode 3 toggle resets to idle when scenario changes", async ({ page }) => {
  const scenarioA = `E2E-Mode3-A-${Date.now()}`;
  const scenarioB = `E2E-Mode3-B-${Date.now()}`;

  await page.goto("/");

  await page.waitForFunction(
    () =>
      typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
    { timeout: 10_000 },
  );

  await page.getByRole("button", { name: /Scenarios/ }).click();

  // Create scenario A.
  await page.locator('input[placeholder="Scenario name"]').fill(scenarioA);
  await page.locator(".scenario-btn--create").click();
  await page.locator(".scenario-row").filter({ hasText: scenarioA }).waitFor({
    timeout: 10_000,
  });

  // Create scenario B.
  await page.locator('input[placeholder="Scenario name"]').fill(scenarioB);
  await page.locator(".scenario-btn--create").click();
  await page.locator(".scenario-row").filter({ hasText: scenarioB }).waitFor({
    timeout: 10_000,
  });

  // Select scenario A, enable Mode 3.
  await page.locator(".scenario-row").filter({ hasText: scenarioA }).click();
  await page.locator('[data-testid="mode3-toggle"]').click();
  await expect(page.locator('[data-testid="zone-control-plane"]')).toBeVisible({
    timeout: 3_000,
  });

  // Select scenario B — Mode 3 should turn off (mode3Active resets in handleSelectScenario).
  await page.locator(".scenario-row").filter({ hasText: scenarioB }).click();
  await expect(page.locator('[data-testid="zone-control-plane"]')).not.toBeVisible({
    timeout: 3_000,
  });
});
