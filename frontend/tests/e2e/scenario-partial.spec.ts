/**
 * E2E: partial advance → drawer shows output at current step, then updates on next advance.
 *
 * Verifies that the drawer renders measurement output after step 1 (not placeholder),
 * and that advancing to step 2 causes the drawer to auto-refresh to step 2 data without
 * closing and reopening.
 */
import { test, expect } from "@playwright/test";

test("partial advance → drawer shows output at step 1, updates to step 2", async ({
  page,
}) => {
  const scenarioName = `E2E-Partial-${Date.now()}`;

  await page.goto("/");

  await page.waitForFunction(
    () =>
      typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
    { timeout: 10_000 },
  );

  // Create and select the scenario.
  await page.getByRole("button", { name: /Scenarios/ }).click();
  await page.locator('input[placeholder="Scenario name"]').fill(scenarioName);
  await page.locator(".scenario-btn--create").click();

  const scenarioRow = page.locator(".scenario-row").filter({ hasText: scenarioName });
  await expect(scenarioRow).toBeVisible({ timeout: 15_000 });
  await scenarioRow.getByTitle("Select as primary scenario").click();

  await page.getByRole("button", { name: /Scenarios/ }).click();

  const nextStepBtn = page.getByRole("button", { name: /Next Step/ });

  // ── Advance to step 1 ────────────────────────────────────────────────────────

  await nextStepBtn.click();
  await expect(page.getByText("Step 1 / 3")).toBeVisible({ timeout: 15_000 });

  // Open entity drawer — must show measurement output at step 1, not the placeholder.
  await page.evaluate(() => {
    (window as Record<string, (id: string) => void>).__worldsim_selectEntity("GRC");
  });

  await expect(page.getByLabel("Close drawer")).toBeVisible({ timeout: 15_000 });
  await expect(page.getByText("Greece")).toBeVisible({ timeout: 15_000 });
  await expect(page.getByText("Multi-Framework Overview")).toBeVisible({ timeout: 15_000 });

  // Subtitle shows the step index once data has loaded.
  await expect(page.getByText(/· step 1/)).toBeVisible({ timeout: 15_000 });

  await expect(
    page.getByText("Advance the scenario at least one step to view measurement output."),
  ).not.toBeVisible();

  // ── Advance to step 2 — drawer must auto-update ──────────────────────────────

  await nextStepBtn.click();
  await expect(page.getByText("Step 2 / 3")).toBeVisible({ timeout: 15_000 });

  // Drawer refreshes automatically when currentStep changes — no need to reopen.
  await expect(page.getByText(/· step 2/)).toBeVisible({ timeout: 15_000 });
});
