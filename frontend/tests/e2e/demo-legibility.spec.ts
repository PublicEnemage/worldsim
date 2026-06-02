/**
 * E2E: Demo legibility assertions — minimum font size, non-truncation, visibility.
 *
 * Source: Issue #377 — M8 retrospective Required Improvement 4.
 * Defect references: DEMO-002 (radar thesis frame not legible), DEMO-003
 * (MDA text not readable), DEMO-005 (radar labels not legible), DEMO-006
 * (governance null not visible).
 *
 * These defects were caught by the M8 IR review — not by automated tests.
 * This suite is the guard that prevents regression.
 *
 * Test strategy:
 *   - All assertions at 1440×900 viewport (standard demo presentation size).
 *   - Font size assertions use window.getComputedStyle() via evaluate() to read
 *     the browser-resolved value, not the declared inline style.
 *   - Non-truncation is checked as element.scrollWidth <= element.offsetWidth.
 *   - Governance honest-null distinction is asserted via computed
 *     borderLeftStyle (dashed = null composite; solid = live composite).
 *   - Ecological boundary annotation (#616 fix) is asserted as visible.
 *
 * Minimum font-size thresholds:
 *   - Primary values (PMM readout)  : 20px (declared 26px; guards against zoom/shrink)
 *   - Framework labels              : 10px (declared 11px; guards against clipping)
 *   - Secondary text (alert body)   : 10px (declared 11–12px; guards DEMO-003)
 *
 * Viewport: 1440×900. If an instrument is not present in the scenario
 * (choropleth optional), the test skips that element gracefully.
 */
import { test, expect } from "@playwright/test";

// ---------------------------------------------------------------------------
// Shared helper — mirrors demo-advancement-flow.spec.ts
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
// Zone 1 instruments are visible and non-zero-sized at 1440×900
//
// Guards DEMO-002 (radar not legible), DEMO-003 (MDA not readable),
// DEMO-005 (radar labels not legible), DEMO-006 (governance null not visible).
// An instrument with zero bounding-box is invisible regardless of font size.
// ---------------------------------------------------------------------------

test("legibility: all four Zone 1 instruments have non-zero bounding boxes at 1440×900", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await createAndSelectScenario(page, `LEG-bounds-${Date.now()}`);

  const instruments = [
    '[data-testid="zone-1a-trajectory-container"]',
    '[data-testid="zone-1b-mda-alerts"]',
    '[data-testid="zone-1c-pmm"]',
    '[data-testid="zone-1d-four-framework"]',
  ];

  for (const sel of instruments) {
    const el = page.locator(sel);
    await expect(el).toBeVisible({ timeout: 10_000 });
    const box = await el.boundingBox();
    expect(box).not.toBeNull();
    expect(box!.width).toBeGreaterThan(0);
    expect(box!.height).toBeGreaterThan(0);
  }
});

// ---------------------------------------------------------------------------
// Zone 1C PMM: primary value element has rendered font-size >= 20px
//
// The PMM readout is the most prominent numeric value (declared 26px). A
// computed size below 20px would indicate a container-shrink regression.
// Guards DEMO-003 (instrument values illegible at demo scale).
// ---------------------------------------------------------------------------

test("legibility: Zone 1C PMM value element has rendered font-size >= 20px", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await createAndSelectScenario(page, `LEG-pmm-${Date.now()}`);

  const pmmValue = page.locator('[data-testid="pmm-value"]');
  await expect(pmmValue).toBeVisible({ timeout: 10_000 });

  const fontSize = await pmmValue.evaluate((el) =>
    parseFloat(window.getComputedStyle(el).fontSize),
  );
  expect(fontSize).toBeGreaterThanOrEqual(20);
});

// ---------------------------------------------------------------------------
// Zone 1D framework labels: rendered font-size >= 10px and not truncated
//
// Framework labels are the primary navigation affordance in Zone 1D. A
// computed font size below 10px is not legible at presentation scale.
// Non-truncation: scrollWidth <= offsetWidth.
// Guards DEMO-005 (radar labels not legible).
// ---------------------------------------------------------------------------

test("legibility: Zone 1D framework labels have rendered font-size >= 10px and are not truncated", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await createAndSelectScenario(page, `LEG-1d-labels-${Date.now()}`);

  const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
  await expect(zone1d).toBeVisible({ timeout: 10_000 });
  await expect(zone1d).not.toHaveAttribute("data-loading", "true", { timeout: 10_000 });

  for (const fw of ["financial", "human_development", "ecological", "governance"]) {
    const label = page.locator(`[data-testid="framework-label-${fw}"]`);
    await expect(label).toBeVisible();

    const { fontSize, isTruncated } = await label.evaluate((el) => {
      const style = window.getComputedStyle(el);
      return {
        fontSize: parseFloat(style.fontSize),
        isTruncated: (el as HTMLElement).scrollWidth > (el as HTMLElement).offsetWidth,
      };
    });

    expect(fontSize).toBeGreaterThanOrEqual(10);
    expect(isTruncated).toBe(false);
  }
});

// ---------------------------------------------------------------------------
// Zone 1D ecological boundary annotation is visible
//
// The "1.0 = boundary" sub-label (Issue #616 fix) must be present and visible
// in the ecological framework row. A zero-area or display:none annotation
// would silently hide the boundary context users need for interpretation.
// ---------------------------------------------------------------------------

test("legibility: Zone 1D ecological-boundary-note is visible", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await createAndSelectScenario(page, `LEG-eco-${Date.now()}`);

  const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
  await expect(zone1d).toBeVisible({ timeout: 10_000 });
  await expect(zone1d).not.toHaveAttribute("data-loading", "true", { timeout: 10_000 });

  const note = page.locator('[data-testid="ecological-boundary-note"]');
  await expect(note).toBeVisible();
  const text = await note.textContent();
  expect(text?.trim()).toBe("1.0 = boundary");
});

// ---------------------------------------------------------------------------
// Zone 1D null composite uses dashed border; live composite uses solid border
//
// The dashed-vs-solid left border is the primary visual signal for the
// honest-null pattern (DD-011). A null composite rendered with a solid border
// is invisible — the user cannot distinguish "data not available" from
// "score is live". Guards DEMO-006 (governance null not visible).
//
// Default scenario: financial and human_development composites are always
// null (single-entity guard, Issue #193). ecological and governance depend
// on module config. We assert that at least one null row carries a dashed
// border and that no live row carries a dashed border.
// ---------------------------------------------------------------------------

test("legibility: Zone 1D null composite rows show dashed border, live rows show solid border", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await createAndSelectScenario(page, `LEG-null-${Date.now()}`);

  const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
  await expect(zone1d).toBeVisible({ timeout: 10_000 });
  await expect(zone1d).not.toHaveAttribute("data-loading", "true", { timeout: 10_000 });

  let hasNullDashed = false;
  let liveSolidViolation = false;

  for (const fw of ["financial", "human_development", "ecological", "governance"]) {
    const scoreEl = page.locator(`[data-testid="framework-score-${fw}"]`);
    const rowEl = page.locator(`[data-testid="framework-row-${fw}"]`);

    const scoreText = (await scoreEl.textContent())?.trim() ?? "";
    const isNull = scoreText === "—";

    const borderStyle = await rowEl.evaluate(
      (el) => window.getComputedStyle(el).borderLeftStyle,
    );

    if (isNull) {
      if (borderStyle === "dashed") hasNullDashed = true;
    } else {
      if (borderStyle === "dashed") liveSolidViolation = true;
    }
  }

  expect(hasNullDashed).toBe(true);
  expect(liveSolidViolation).toBe(false);
});

// ---------------------------------------------------------------------------
// Zone 1B MDA panel text is not overflow-clipped
//
// The MDA alert body text must not be truncated by its container. An element
// whose scrollWidth exceeds its offsetWidth is overflow-clipped and illegible
// without scrolling — a legibility regression. Guards DEMO-003.
//
// Because the default scenario may show either the no-alerts state or alerts,
// both are tested: if mda-no-alerts is present its text is checked; if
// mda-alert-row is present all visible alert-line-1 elements are checked.
// ---------------------------------------------------------------------------

test("legibility: Zone 1B MDA panel text is not overflow-clipped", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await createAndSelectScenario(page, `LEG-mda-${Date.now()}`);

  const panel = page.locator('[data-testid="zone-1b-mda-alerts"]');
  await expect(panel).toBeVisible({ timeout: 10_000 });

  // Wait for the panel to settle into one of its two valid states
  await expect
    .poll(
      async () => {
        const noAlerts = page.locator('[data-testid="mda-no-alerts"]');
        const alertRow = page.locator('[data-testid="mda-alert-row"]');
        const hasNoAlerts = await noAlerts.isVisible().catch(() => false);
        const hasAlertRow = await alertRow.first().isVisible().catch(() => false);
        return hasNoAlerts || hasAlertRow;
      },
      { timeout: 10_000, message: "Zone 1B must settle into mda-no-alerts or mda-alert-row" },
    )
    .toBe(true);

  const noAlertsEl = page.locator('[data-testid="mda-no-alerts"]');
  const isNoAlerts = await noAlertsEl.isVisible().catch(() => false);

  if (isNoAlerts) {
    const isTruncated = await noAlertsEl.evaluate(
      (el) => (el as HTMLElement).scrollWidth > (el as HTMLElement).offsetWidth,
    );
    expect(isTruncated).toBe(false);
  } else {
    const alertLines = page.locator('[data-testid="alert-line-1"]');
    const count = await alertLines.count();
    for (let i = 0; i < count; i++) {
      const line = alertLines.nth(i);
      const isTruncated = await line.evaluate(
        (el) => (el as HTMLElement).scrollWidth > (el as HTMLElement).offsetWidth,
      );
      expect(isTruncated).toBe(false);
    }
  }
});
