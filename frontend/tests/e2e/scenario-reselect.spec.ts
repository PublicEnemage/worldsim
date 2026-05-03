/**
 * E2E: re-select a completed scenario → entity drawer shows output immediately.
 *
 * Regression test for the `currentStep ?? selectedScenarioSteps` fallback documented
 * in state-ownership.md.  When a user selects scenario A (completed), then selects
 * scenario B, then re-selects A, currentStep resets to null and the useEffect must
 * set it back to n_steps.  Even before that resolves, the ?? fallback must prevent
 * the placeholder from appearing.
 */
import { test, expect } from "@playwright/test";

test("re-select completed scenario → drawer shows output without advance clicks", async ({
  page,
}) => {
  const ts = Date.now();
  const nameA = `E2E-Reselect-A-${ts}`;
  const nameB = `E2E-Reselect-B-${ts}`;

  await page.goto("/");

  await page.waitForFunction(
    () =>
      typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
    { timeout: 10_000 },
  );

  // ── Create and complete scenario A ──────────────────────────────────────────

  await page.getByRole("button", { name: /Scenarios/ }).click();

  await page.locator('input[placeholder="Scenario name"]').fill(nameA);
  await page.locator(".scenario-btn--create").click();

  const rowA = page.locator(".scenario-row").filter({ hasText: nameA });
  await expect(rowA).toBeVisible({ timeout: 15_000 });
  await rowA.getByTitle("Select as primary scenario").click();

  await page.getByRole("button", { name: /Scenarios/ }).click();

  const nextStepBtn = page.getByRole("button", { name: /Next Step/ });
  for (let step = 1; step <= 3; step++) {
    await nextStepBtn.click();
    await expect(page.getByText(`Step ${step} / 3`)).toBeVisible({ timeout: 15_000 });
  }
  await expect(page.getByText(/Complete/)).toBeVisible();

  // ── Create scenario B and select it ─────────────────────────────────────────

  await page.getByRole("button", { name: /Scenarios/ }).click();

  await page.locator('input[placeholder="Scenario name"]').fill(nameB);
  await page.locator(".scenario-btn--create").click();

  const rowB = page.locator(".scenario-row").filter({ hasText: nameB });
  await expect(rowB).toBeVisible({ timeout: 15_000 });
  await rowB.getByTitle("Select as primary scenario").click();

  // ── Re-select scenario A ─────────────────────────────────────────────────────
  // This changes selectedScenarioId → useEffect fires → sets currentStep = n_steps
  // (because A is completed).  The ?? fallback also guards if the fetch hasn't
  // resolved yet.

  await expect(rowA).toBeVisible();
  await rowA.getByTitle("Select as primary scenario").click();

  await page.getByRole("button", { name: /Scenarios/ }).click();

  // Trigger entity selection immediately — before the useEffect status-check resolves.
  // The ?? fallback (currentStep ?? selectedScenarioSteps) must provide step 3.
  await page.evaluate(() => {
    (window as Record<string, (id: string) => void>).__worldsim_selectEntity("GRC");
  });

  await expect(page.getByLabel("Close drawer")).toBeVisible({ timeout: 15_000 });
  await expect(page.getByText("Greece")).toBeVisible({ timeout: 15_000 });
  await expect(page.getByText("Multi-Framework Overview")).toBeVisible({ timeout: 15_000 });

  await expect(
    page.getByText("Advance the scenario at least one step to view measurement output."),
  ).not.toBeVisible();
});
