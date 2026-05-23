/**
 * E2E: M9 Instrument Cluster — Zone-level integration tests (AC-001, AC-002).
 *
 * Type 2 (integration-level) ACs: require all four Zone 1 instruments
 * coexisting simultaneously in App.tsx. Skip annotations removed 2026-05-23 —
 * Issues #460, #461, #462 merged; InstrumentCluster wired into App.tsx via
 * ScenarioInstrumentCluster (PR #490).
 *
 * Setup: creates a minimal scenario via UI so the instrument cluster renders.
 * The cluster appears whenever a scenario is selected (PR #490 App.tsx wiring).
 *
 * Source documents:
 *   docs/frontend/fa-brief-m9-instrument-cluster.md §Named Acceptance Criteria
 *   docs/ux/user-stories-instrument-cluster-m9.md
 *
 * data-testid selectors:
 *   zone-1a-trajectory-container — InstrumentCluster wrapper for TrajectoryView
 *   zone-1b-mda-alerts           — MDAAlertPanelZone1B root
 *   zone-1c-pmm                  — PMMWidgetZone1C root
 *   zone-1d-four-framework       — FourFrameworkZone1D root
 */
import { test, expect } from "@playwright/test";

async function selectScenario(page: import("@playwright/test").Page, name: string) {
  await page.waitForFunction(
    () => typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
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
// AC-001: All four Zone 1 instruments visible without scroll at 1024×768
// Source: US-001; FA brief §Named Acceptance Criteria
// Type 2 — integration-level
// ---------------------------------------------------------------------------

test("AC-001: four Zone 1 instruments visible at 1024×768 without scroll", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");
  await selectScenario(page, `AC-001-${Date.now()}`);

  // All four Zone 1 instruments must be in the viewport without scroll.
  // toBeInViewport() confirms element is within current viewport bounds.
  await expect(
    page.locator('[data-testid="zone-1a-trajectory-container"]'),
  ).toBeInViewport({ timeout: 10_000 });
  await expect(
    page.locator('[data-testid="zone-1b-mda-alerts"]'),
  ).toBeInViewport();
  await expect(
    page.locator('[data-testid="zone-1c-pmm"]'),
  ).toBeInViewport();
  await expect(
    page.locator('[data-testid="zone-1d-four-framework"]'),
  ).toBeInViewport();
});

// ---------------------------------------------------------------------------
// AC-002: All four Zone 1 instruments visible without scroll at 1280×800
// Source: US-002; FA brief §Named Acceptance Criteria
// Type 2 — integration-level
// ---------------------------------------------------------------------------

test("AC-002: four Zone 1 instruments visible at 1280×800 without scroll", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");
  await selectScenario(page, `AC-002-${Date.now()}`);

  await expect(
    page.locator('[data-testid="zone-1a-trajectory-container"]'),
  ).toBeInViewport({ timeout: 10_000 });
  await expect(
    page.locator('[data-testid="zone-1b-mda-alerts"]'),
  ).toBeInViewport();
  await expect(
    page.locator('[data-testid="zone-1c-pmm"]'),
  ).toBeInViewport();
  await expect(
    page.locator('[data-testid="zone-1d-four-framework"]'),
  ).toBeInViewport();
});
