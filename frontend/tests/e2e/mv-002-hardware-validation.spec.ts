/**
 * MV-002 Hardware Validation — @hardware-only
 *
 * Runs AC-009 (Mode 3 full component set render) on real hardware WITHOUT CPU throttle.
 * This test is excluded from CI (playwright.config.ts grep excludes @hardware-only).
 *
 * Run on target hardware:
 *   npx playwright test --grep "@hardware-only"
 *
 * Target hardware: ProBook (Intel i5-8265U, 4 cores, 8 GiB, Windows 11)
 * Pass criterion: renderMs ≤ 100ms
 *
 * After running, post the output (hardware specs + measured renderMs) as a comment
 * on GitHub Issue #550. Record in the G6 validation report:
 *   docs/process/validation/m16-g6-accessibility-validation-report.md
 *
 * Exception context: EX-001 (docs/compliance/exceptions.md) raised the CI throttled
 * threshold to 200ms. The hardware target remains ≤ 100ms — this test is the primary
 * gate for that requirement.
 *
 * Authority: M16-G6 sprint entry §3.1 MV-002 AC-009; EL decision 2026-06-24.
 */
import { test, expect } from "@playwright/test";

test("@hardware-only MV-002 AC-009: Mode 3 full component set render ≤ 100ms on real hardware (no throttle)", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });

  // No CPU throttle — this is the hardware validation run.
  await page.goto("/");

  await page.waitForFunction(
    () =>
      typeof (window as Record<string, unknown>).__worldsim_selectEntity ===
      "function",
    { timeout: 10_000 },
  );

  const scenarioName = "MV-002-hardware";
  await page.getByRole("button", { name: /Scenarios/ }).click();
  await page.locator('input[placeholder="Scenario name"]').fill(scenarioName);
  await page.locator(".scenario-btn--create").click();
  const row = page.locator(".scenario-row").filter({ hasText: scenarioName });
  await expect(row).toBeVisible({ timeout: 10_000 });
  await row.getByTitle("Select as primary scenario").click();
  await page.getByRole("button", { name: /Scenarios/ }).click();

  const mode3Trigger = page.locator('[data-testid="mode3-toggle"]');
  await expect(mode3Trigger).toBeVisible({ timeout: 5_000 });

  await page.evaluate(() => performance.mark("mode3-start"));
  await mode3Trigger.click();
  await page.waitForTimeout(20);
  await page.evaluate(() => {
    performance.mark("mode3-end");
    performance.measure("mode3-render", "mode3-start", "mode3-end");
  });

  const renderMs = await page.evaluate(() => {
    const m = performance.getEntriesByName("mode3-render")[0];
    return m?.duration ?? null;
  });

  console.log(`MV-002 measured renderMs: ${renderMs}ms`);
  console.log(`MV-002 pass criterion: ≤ 100ms`);
  console.log(`MV-002 result: ${renderMs !== null && renderMs <= 100 ? "PASS" : "FAIL"}`);

  expect(renderMs).not.toBeNull();
  expect(renderMs).toBeLessThanOrEqual(100);
});
