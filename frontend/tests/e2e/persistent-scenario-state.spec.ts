/**
 * E2E: IR-003 — Persistent scenario state and demonstrative entry (Issue #497).
 *
 * Tests two complementary entry paths:
 *   1. localStorage persistence — selecting a scenario writes to localStorage;
 *      reloading the page restores the instrument cluster without user action.
 *   2. URL ?scenario= param — navigating to /?scenario={id} selects that
 *      scenario and renders the instrument cluster without user action.
 *
 * Both paths satisfy the entry state requirements from the IR-003 finding:
 *   - Demonstrative entry (Persona 5 — Aicha): cluster visible on load.
 *   - Reactive entry (Persona 2 — Eleni): last completed scenario auto-loads.
 *
 * Source: Issue #497 — persistent scenario state + demonstrative entry.
 */
import { test, expect } from "@playwright/test";

const LAST_SCENARIO_KEY = "worldsim_last_scenario";

async function waitForAppReady(page: import("@playwright/test").Page) {
  await page.waitForFunction(
    () =>
      typeof (window as Record<string, unknown>).__worldsim_selectEntity ===
      "function",
    { timeout: 10_000 },
  );
}

async function createAndSelectScenario(
  page: import("@playwright/test").Page,
  name: string,
): Promise<void> {
  await waitForAppReady(page);
  await page.getByRole("button", { name: /Scenarios/ }).click();
  await page.locator('input[placeholder="Scenario name"]').fill(name);
  await page.locator(".scenario-btn--create").click();
  const row = page.locator(".scenario-row").filter({ hasText: name });
  await expect(row).toBeVisible({ timeout: 15_000 });
  await row.getByTitle("Select as primary scenario").click();
  await page.getByRole("button", { name: /Scenarios/ }).click();
}

// ---------------------------------------------------------------------------
// localStorage persistence: selecting a scenario writes to localStorage
// ---------------------------------------------------------------------------

test("IR-003: selecting a scenario writes ID to localStorage", async ({ page }) => {
  await page.goto("/");
  const name = `IR003-storage-${Date.now()}`;
  await createAndSelectScenario(page, name);

  // Instrument cluster must be visible after selection
  await expect(
    page.locator('[data-testid="zone-1d-four-framework"]'),
  ).toBeVisible({ timeout: 10_000 });

  // localStorage must have the scenario ID stored
  const stored = await page.evaluate((key) => {
    return localStorage.getItem(key);
  }, LAST_SCENARIO_KEY);
  expect(stored).not.toBeNull();

  const parsed = JSON.parse(stored!) as { id: string; name: string; totalSteps: number };
  expect(parsed.id).toBeTruthy();
  expect(parsed.name).toBe(name);
  expect(parsed.totalSteps).toBeGreaterThan(0);
});

// ---------------------------------------------------------------------------
// localStorage restore: reloading the page restores the instrument cluster
// ---------------------------------------------------------------------------

test("IR-003: reloading page restores instrument cluster from localStorage", async ({
  page,
}) => {
  await page.goto("/");
  const name = `IR003-reload-${Date.now()}`;
  await createAndSelectScenario(page, name);

  // Cluster must be visible after selection
  await expect(
    page.locator('[data-testid="zone-1d-four-framework"]'),
  ).toBeVisible({ timeout: 10_000 });

  // Reload — no user interaction, cluster must reappear automatically
  await page.reload();
  await waitForAppReady(page);

  // Cluster must be visible without opening Scenarios panel or selecting anything
  await expect(
    page.locator('[data-testid="zone-1d-four-framework"]'),
  ).toBeVisible({ timeout: 15_000 });

  // The restored scenario name should appear in the header
  await expect(page.locator("header")).toContainText(name, { timeout: 5_000 });
});

// ---------------------------------------------------------------------------
// URL param: ?scenario={id} loads cluster without user action
// ---------------------------------------------------------------------------

test("IR-003: ?scenario= URL param selects scenario on load", async ({ page }) => {
  // First: create a scenario via the UI to get a real ID
  await page.goto("/");
  const name = `IR003-url-${Date.now()}`;
  await createAndSelectScenario(page, name);

  await expect(
    page.locator('[data-testid="zone-1d-four-framework"]'),
  ).toBeVisible({ timeout: 10_000 });

  // Extract the stored scenario ID from localStorage
  const stored = await page.evaluate((key) => {
    return localStorage.getItem(key);
  }, LAST_SCENARIO_KEY);
  expect(stored).not.toBeNull();
  const { id } = JSON.parse(stored!) as { id: string };

  // Navigate to the app with a fresh context (clear localStorage) but pass the
  // scenario ID via URL param — cluster must appear without user setup
  await page.evaluate((key) => localStorage.removeItem(key), LAST_SCENARIO_KEY);
  await page.goto(`/?scenario=${encodeURIComponent(id)}`);
  await waitForAppReady(page);

  // Cluster must appear automatically from URL param alone
  await expect(
    page.locator('[data-testid="zone-1d-four-framework"]'),
  ).toBeVisible({ timeout: 15_000 });
});

// ---------------------------------------------------------------------------
// URL param takes precedence over localStorage when both are present
// ---------------------------------------------------------------------------

test("IR-003: URL ?scenario= takes precedence over localStorage", async ({ page }) => {
  // Create two scenarios
  await page.goto("/");
  const nameA = `IR003-urlA-${Date.now()}`;
  await createAndSelectScenario(page, nameA);
  await expect(
    page.locator('[data-testid="zone-1d-four-framework"]'),
  ).toBeVisible({ timeout: 10_000 });

  // Scenario A is now in localStorage
  const storedA = await page.evaluate((key) => localStorage.getItem(key), LAST_SCENARIO_KEY);
  const { id: idA } = JSON.parse(storedA!) as { id: string };

  // Open panel and create scenario B, but do NOT select it — localStorage stays as A
  await page.getByRole("button", { name: /Scenarios/ }).click();
  const nameB = `IR003-urlB-${Date.now()}`;
  await page.locator('input[placeholder="Scenario name"]').fill(nameB);
  await page.locator(".scenario-btn--create").click();
  const rowB = page.locator(".scenario-row").filter({ hasText: nameB });
  await expect(rowB).toBeVisible({ timeout: 15_000 });

  // Get scenario B's ID from localStorage after — need to select it briefly
  await rowB.getByTitle("Select as primary scenario").click();
  await page.getByRole("button", { name: /Scenarios/ }).click();
  const storedB = await page.evaluate((key) => localStorage.getItem(key), LAST_SCENARIO_KEY);
  const { id: idB } = JSON.parse(storedB!) as { id: string };
  expect(idA).not.toBe(idB);

  // Restore localStorage to scenario A — simulates returning user
  await page.evaluate(
    ([key, val]) => localStorage.setItem(key!, val!),
    [LAST_SCENARIO_KEY, storedA!],
  );

  // Navigate with ?scenario=idB — URL param should win
  await page.goto(`/?scenario=${encodeURIComponent(idB)}`);
  await waitForAppReady(page);

  await expect(
    page.locator('[data-testid="zone-1d-four-framework"]'),
  ).toBeVisible({ timeout: 15_000 });

  // The scenario name shown in the header must be B, not A
  await expect(page.locator("header")).toContainText(nameB, { timeout: 5_000 });
  const headerText = await page.locator("header").textContent();
  expect(headerText).not.toContain(nameA);
});
