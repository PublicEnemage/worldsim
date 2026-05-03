/**
 * E2E: create → advance to completion → click entity → drawer shows measurement output.
 *
 * This is the canonical regression test for the M4 EntityDetailDrawer placeholder bug:
 * after advancing all steps, clicking a country must show data, never the placeholder.
 */
import { test, expect } from "@playwright/test";

test("create → advance to completion → entity drawer shows measurement output", async ({
  page,
}) => {
  const scenarioName = `E2E-Advance-${Date.now()}`;

  await page.goto("/");

  // Wait for app to mount and test seam to be available.
  await page.waitForFunction(
    () =>
      typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
    { timeout: 10_000 },
  );

  // Open scenarios panel.
  await page.getByRole("button", { name: /Scenarios/ }).click();

  // Create scenario.
  await page.locator('input[placeholder="Scenario name"]').fill(scenarioName);
  await page.locator(".scenario-btn--create").click();

  // Wait for the scenario row to appear in the list (implies create succeeded and list refreshed).
  const scenarioRow = page.locator(".scenario-row").filter({ hasText: scenarioName });
  await expect(scenarioRow).toBeVisible({ timeout: 15_000 });

  // Select as primary scenario.
  await scenarioRow.getByTitle("Select as primary scenario").click();

  // Close panel.
  await page.getByRole("button", { name: /Scenarios/ }).click();

  // Advance all 3 steps, waiting for each to complete before clicking next.
  const nextStepBtn = page.getByRole("button", { name: /Next Step/ });

  await nextStepBtn.click();
  await expect(page.getByText("Step 1 / 3")).toBeVisible({ timeout: 15_000 });

  await nextStepBtn.click();
  await expect(page.getByText("Step 2 / 3")).toBeVisible({ timeout: 15_000 });

  await nextStepBtn.click();
  await expect(page.getByText("Step 3 / 3")).toBeVisible({ timeout: 15_000 });
  await expect(page.getByText(/Complete/)).toBeVisible({ timeout: 10_000 });

  // Advance button must be disabled after completion.
  await expect(nextStepBtn).toBeDisabled();

  // Trigger entity selection via test seam (avoids clicking WebGL canvas).
  await page.evaluate(() => {
    (window as Record<string, (id: string) => void>).__worldsim_selectEntity("GRC");
  });

  // Drawer must show measurement output — not the placeholder.
  await expect(page.getByLabel("Close drawer")).toBeVisible({ timeout: 15_000 });
  await expect(page.getByText("Greece")).toBeVisible({ timeout: 15_000 });
  await expect(page.getByText("Multi-Framework Overview")).toBeVisible({ timeout: 15_000 });

  // The placeholder text must NOT appear.
  await expect(
    page.getByText("Advance the scenario at least one step to view measurement output."),
  ).not.toBeVisible();
});
