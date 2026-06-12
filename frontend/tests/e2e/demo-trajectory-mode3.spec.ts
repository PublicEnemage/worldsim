/**
 * E2E: G2 — DEMO trajectory and comparison display tests.
 *
 * Tests for DEMO-059 (PMM scale note), DEMO-062 (Zone 1D entity label),
 * DEMO-063 (inline entity labels), DEMO-064 (Mode 3 comparison readout).
 *
 * Source intent: docs/process/intents/DEMO-059-062-063-064-2026-06-12-trajectory.md
 *
 * AC-1 (DEMO-064): Mode 3 comparison readout with labeled baseline/branch values.
 * AC-2 (DEMO-059): PMM scale note element visible in Zone 1C.
 * AC-3 (DEMO-063): Entity labels (JOR, EGY) visible in trajectory chart area.
 * AC-4 (DEMO-062): Zone 1D shows primary-entity label in multi-entity scenario.
 */
import { test, expect } from "@playwright/test";

const API_BASE = "http://localhost:8000/api/v1";

// ---------------------------------------------------------------------------
// Helpers
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

// ---------------------------------------------------------------------------
// G2/AC-2 — PMM scale note (DEMO-059)
//
// After any scenario is selected, Zone 1C PMM widget must show a scale
// reference element (data-testid="pmm-scale-note") that is visible.
// The scale note must be readable without presenter mediation.
// ---------------------------------------------------------------------------

test("G2/AC-2: PMM widget shows pmm-scale-note element", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await createAndSelectScenario(page, `G2-pmm-scale-${Date.now()}`);

  const pmmWidget = page.locator('[data-testid="zone-1c-pmm"]');
  await expect(pmmWidget).toBeVisible({ timeout: 10_000 });

  const scaleNote = page.locator('[data-testid="pmm-scale-note"]');
  await expect(scaleNote).toBeVisible({ timeout: 5_000 });

  // Note must be non-empty
  const text = await scaleNote.textContent();
  expect(text?.trim().length).toBeGreaterThan(0);
});

// ---------------------------------------------------------------------------
// G2/AC-1 — Mode 3 comparison readout (DEMO-064)
//
// After a Mode 3 branch recompute completes, a comparison readout
// (data-testid="mode3-comparison-readout") must be visible showing labeled
// baseline and branch values for a financial indicator.
// ---------------------------------------------------------------------------

test("G2/AC-1: Mode 3 comparison readout visible after branch recompute", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  await page.waitForFunction(
    () =>
      typeof (window as Record<string, unknown>).__worldsim_selectEntity ===
      "function",
    { timeout: 10_000 },
  );

  await page.getByRole("button", { name: /Scenarios/ }).click();
  const scenarioName = `G2-mode3-readout-${Date.now()}`;
  await page.locator('input[placeholder="Scenario name"]').fill(scenarioName);
  await page.locator(".scenario-btn--create").click();
  const row = page.locator(".scenario-row").filter({ hasText: scenarioName });
  await expect(row).toBeVisible({ timeout: 15_000 });
  await row.getByTitle("Select as primary scenario").click();

  // Advance one step so branching is valid.
  const advanceBtn = page.getByRole("button", { name: /Next Step/ });
  await advanceBtn.waitFor({ timeout: 10_000 });
  await advanceBtn.click();
  await expect(page.getByText("Step 1 / 3")).toBeVisible({ timeout: 15_000 });

  // Close Scenarios panel before enabling Mode 3.
  await page.getByRole("button", { name: /Scenarios/ }).click();

  // Enable Mode 3.
  await page.locator('[data-testid="mode3-toggle"]').click();
  await expect(page.locator('[data-testid="apply-control-change"]')).toBeVisible({
    timeout: 3_000,
  });

  // Set fiscal multiplier to 1.30.
  await page.locator('[data-testid="fiscal-multiplier-slider"]').evaluate(
    (el: HTMLInputElement) => {
      const setter = Object.getOwnPropertyDescriptor(
        window.HTMLInputElement.prototype,
        "value",
      )!.set!;
      setter.call(el, "1.30");
      el.dispatchEvent(new Event("input", { bubbles: true }));
    },
  );
  await expect(
    page.locator('[data-testid="fiscal-multiplier-value"]'),
  ).toContainText("1.30", { timeout: 2_000 });

  // Apply control change — triggers branch recompute.
  await page.locator('[data-testid="apply-control-change"]').click();

  // Wait for recompute to complete (badge disappears).
  await expect(page.locator('[data-testid="recompute-badge"]')).toBeVisible({
    timeout: 5_000,
  });
  await expect(page.locator('[data-testid="recompute-badge"]')).not.toBeVisible({
    timeout: 60_000,
  });

  // Mode 3 comparison readout must now be visible.
  const readout = page.locator('[data-testid="mode3-comparison-readout"]');
  await expect(readout).toBeVisible({ timeout: 5_000 });

  // Both baseline and branch value elements must be present.
  await expect(page.locator('[data-testid="mode3-baseline-value"]')).toBeVisible();
  await expect(page.locator('[data-testid="mode3-branch-value"]')).toBeVisible();
});

// ---------------------------------------------------------------------------
// G2/AC-3 — Inline entity labels (DEMO-063)
//
// In a multi-entity scenario (JOR+EGY), the trajectory chart area must
// contain visible text labels showing "JOR" and "EGY" so the audience can
// identify the entities without consulting the legend.
// ---------------------------------------------------------------------------

test("G2/AC-3: Trajectory chart shows JOR and EGY labels in multi-entity scenario", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  await page.waitForFunction(
    () =>
      typeof (window as Record<string, unknown>).__worldsim_selectEntity ===
      "function",
    { timeout: 10_000 },
  );

  // Create a multi-entity scenario via API.
  const scenarioName = `G2-multiEntity-${Date.now()}`;
  const createRes = await page.request.post(`${API_BASE}/scenarios`, {
    data: {
      name: scenarioName,
      description: "G2 multi-entity test",
      configuration: {
        entities: ["JOR", "EGY"],
        n_steps: 3,
        timestep_label: "annual",
        start_date: "2024-01-01",
      },
    },
  });
  expect(createRes.ok()).toBeTruthy();

  // Select the scenario in the UI.
  await page.getByRole("button", { name: /Scenarios/ }).click();
  const row = page.locator(".scenario-row").filter({ hasText: scenarioName });
  await expect(row).toBeVisible({ timeout: 15_000 });
  await row.getByTitle("Select as primary scenario").click();
  await page.getByRole("button", { name: /Scenarios/ }).click();

  // Verify entity labels appear in the chart container.
  const chartContainer = page.locator('[data-testid="zone-1a-trajectory-container"]');
  await expect(chartContainer).toBeVisible({ timeout: 10_000 });

  await expect(chartContainer.getByText("JOR", { exact: true })).toBeVisible({
    timeout: 10_000,
  });
  await expect(chartContainer.getByText("EGY", { exact: true })).toBeVisible({
    timeout: 10_000,
  });

  // Cleanup.
  const scenarioId = (await createRes.json() as { scenario_id: string }).scenario_id;
  await page.request.delete(`${API_BASE}/scenarios/${encodeURIComponent(scenarioId)}`);
});

// ---------------------------------------------------------------------------
// G2/AC-4 — Zone 1D entity label (DEMO-062)
//
// In a multi-entity scenario, Zone 1D must show a primary-entity label
// (data-testid="zone-1d-primary-entity") identifying which entities'
// composite score is displayed.
// ---------------------------------------------------------------------------

test("G2/AC-4: Zone 1D shows zone-1d-primary-entity label in multi-entity scenario", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  await page.waitForFunction(
    () =>
      typeof (window as Record<string, unknown>).__worldsim_selectEntity ===
      "function",
    { timeout: 10_000 },
  );

  // Create a multi-entity scenario via API.
  const scenarioName = `G2-zone1d-${Date.now()}`;
  const createRes = await page.request.post(`${API_BASE}/scenarios`, {
    data: {
      name: scenarioName,
      description: "G2 Zone 1D multi-entity test",
      configuration: {
        entities: ["JOR", "EGY"],
        n_steps: 3,
        timestep_label: "annual",
        start_date: "2024-01-01",
      },
    },
  });
  expect(createRes.ok()).toBeTruthy();

  // Select the scenario.
  await page.getByRole("button", { name: /Scenarios/ }).click();
  const row = page.locator(".scenario-row").filter({ hasText: scenarioName });
  await expect(row).toBeVisible({ timeout: 15_000 });
  await row.getByTitle("Select as primary scenario").click();
  await page.getByRole("button", { name: /Scenarios/ }).click();

  // Zone 1D must be visible.
  const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
  await expect(zone1d).toBeVisible({ timeout: 10_000 });

  // Primary-entity label must be present and visible.
  const entityLabel = page.locator('[data-testid="zone-1d-primary-entity"]');
  await expect(entityLabel).toBeVisible({ timeout: 10_000 });

  // Cleanup.
  const scenarioId = (await createRes.json() as { scenario_id: string }).scenario_id;
  await page.request.delete(`${API_BASE}/scenarios/${encodeURIComponent(scenarioId)}`);
});
