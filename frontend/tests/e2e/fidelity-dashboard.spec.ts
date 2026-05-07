/**
 * E2E: FidelityDashboard renders correctly — Issue #206.
 *
 * Verifies the backtesting fidelity dashboard:
 *   1. The "Fidelity" toggle button is present in the header.
 *   2. Clicking it opens the dashboard panel.
 *   3. All five backtesting cases are rendered.
 *   4. The Argentina step 2 MAGNITUDE gate is highlighted.
 *   5. The two structural gaps are shown as documented limitations.
 *   6. The ADR-006 Monte Carlo upgrade trigger status is visible.
 *   7. The dashboard closes when the toggle is clicked again.
 *   8. Opening Scenarios closes Fidelity (panels are mutually exclusive).
 *
 * Does NOT require a running backend — the dashboard is a static
 * methodology transparency display. Tests run against the Vite dev server.
 */
import { test, expect } from "@playwright/test";

test.describe("FidelityDashboard", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    // Wait for React to mount — the test seam confirms full hydration.
    await page.waitForFunction(
      () =>
        typeof (window as Record<string, unknown>).__worldsim_selectEntity ===
        "function",
      { timeout: 10_000 },
    );
  });

  test("Fidelity toggle button is present in header", async ({ page }) => {
    await expect(page.getByTestId("fidelity-toggle")).toBeVisible();
    await expect(page.getByTestId("fidelity-toggle")).toContainText("Fidelity");
  });

  test("clicking Fidelity opens dashboard panel", async ({ page }) => {
    await expect(page.getByTestId("fidelity-dashboard")).not.toBeVisible();
    await page.getByTestId("fidelity-toggle").click();
    await expect(page.getByTestId("fidelity-dashboard")).toBeVisible();
  });

  test("all five backtesting cases are rendered", async ({ page }) => {
    await page.getByTestId("fidelity-toggle").click();
    const dashboard = page.getByTestId("fidelity-dashboard");
    await expect(dashboard).toBeVisible();

    // Each case row is identified by entity ID
    await expect(page.getByTestId("fidelity-case-GRC")).toBeVisible();
    await expect(page.getByTestId("fidelity-case-ARG")).toBeVisible();
    await expect(page.getByTestId("fidelity-case-LBN")).toBeVisible();
    await expect(page.getByTestId("fidelity-case-THA")).toBeVisible();
    await expect(page.getByTestId("fidelity-case-ECU")).toBeVisible();
  });

  test("DIRECTION_ONLY 5/5 summary badge is shown", async ({ page }) => {
    await page.getByTestId("fidelity-toggle").click();
    await expect(page.getByText("DIRECTION_ONLY: 5/5 cases ✓")).toBeVisible();
  });

  test("Argentina step 2 MAGNITUDE result is highlighted", async ({ page }) => {
    await page.getByTestId("fidelity-toggle").click();
    const argCase = page.getByTestId("fidelity-case-ARG");
    await expect(argCase).toBeVisible();
    // The MAGNITUDE badge and first-result callout
    await expect(argCase.getByText("MAGNITUDE ✓")).toBeVisible();
    await expect(
      argCase.getByText("FIRST MAGNITUDE-VALIDATED RESULT", { exact: true }),
    ).toBeVisible();
    // The actual numbers
    await expect(argCase.getByText(/−10\.55%/)).toBeVisible();
    await expect(argCase.getByText(/3\.2%/)).toBeVisible();
  });

  test("structural gaps are shown as documented limitations not failures", async ({
    page,
  }) => {
    await page.getByTestId("fidelity-toggle").click();
    // ARG step 1 gap
    const argGap = page.getByTestId("structural-gap-ARG-1");
    await expect(argGap).toBeVisible();
    await expect(argGap.getByText(/Issue #222/)).toBeVisible();

    // GRC steps 2-3 gap
    const grcGap = page.getByTestId("structural-gap-GRC-2–3");
    await expect(grcGap).toBeVisible();
    await expect(grcGap.getByText(/Issue #221/)).toBeVisible();

    // Section heading frames them as limitations, not failures
    await expect(
      page.getByText("Documented Structural Gaps — Deferred to M7"),
    ).toBeVisible();
  });

  test("ADR-006 Monte Carlo upgrade trigger status is shown", async ({ page }) => {
    await page.getByTestId("fidelity-toggle").click();
    await expect(
      page.getByText(/ADR-006 Monte Carlo upgrade trigger/),
    ).toBeVisible();
    await expect(page.getByText(/1 of 2 required MAGNITUDE cases/)).toBeVisible();
  });

  test("clicking Fidelity again closes the dashboard", async ({ page }) => {
    await page.getByTestId("fidelity-toggle").click();
    await expect(page.getByTestId("fidelity-dashboard")).toBeVisible();
    await page.getByTestId("fidelity-toggle").click();
    await expect(page.getByTestId("fidelity-dashboard")).not.toBeVisible();
  });

  test("opening Scenarios closes Fidelity panel", async ({ page }) => {
    await page.getByTestId("fidelity-toggle").click();
    await expect(page.getByTestId("fidelity-dashboard")).toBeVisible();

    // Opening Scenarios should close Fidelity
    await page.getByRole("button", { name: /Scenarios/ }).click();
    await expect(page.getByTestId("fidelity-dashboard")).not.toBeVisible();
    // Scenario panel is now open (the section title is visible)
    await expect(page.getByText("Scenarios", { exact: false }).first()).toBeVisible();
  });
});
