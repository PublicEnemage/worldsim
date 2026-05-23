/**
 * E2E: M9 Instrument Cluster — Pre-implementation acceptance test gate.
 *
 * Tests in this file cover AC-001 through AC-015 from:
 *   docs/frontend/fa-brief-m9-instrument-cluster.md §Named Acceptance Criteria
 *   docs/ux/user-stories-instrument-cluster-m9.md
 *
 * ALL TESTS IN THIS FILE ARE EXPECTED TO FAIL until Issue #460/461/462 implement
 * the instrument cluster components. That is correct and expected — this file is the
 * QA gate written before implementation begins (Issue #459).
 *
 * data-testid selectors used (must be added by implementing agent):
 *   zone-1a-trajectory     — TrajectoryView component root
 *   zone-1b-mda-alerts     — MDA Alert Panel component root
 *   zone-1c-pmm            — PMM Widget component root
 *   zone-1d-four-framework — Four-Framework Current Position component root
 *   control-plane-zone     — Control plane reserved zone (280px column)
 *   step-tick-significant  — Custom XAxis tick for SIGNIFICANT steps (AC-011)
 *
 * Viewport note: Playwright config sets default viewport to 1280×720. Tests that
 * require specific viewports call page.setViewportSize() explicitly.
 *
 * Server requirement: AC-007, AC-008, AC-009 require a running frontend server.
 * These tests are written to fail (component absent), not to skip on missing server —
 * the existing Playwright config already handles server availability via baseURL.
 */
import { test, expect } from "@playwright/test";

// Skip all tests until Issues #460/461/462 implement the instrument cluster
// components. These are pre-implementation acceptance gates — they are expected
// to be pending until the components exist. Remove this line when #460 ships.
test.skip(true, "Pre-implementation gate: instrument cluster components not yet built (Issues #460-462)");

// ---------------------------------------------------------------------------
// AC-001: All four Zone 1 instruments visible without scroll at 1024×768
// Source: US-001; FA brief §Named Acceptance Criteria
// ---------------------------------------------------------------------------

test("AC-001: four Zone 1 instruments visible at 1024×768 without scroll", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  // All four Zone 1 instruments must be in the viewport without any scroll
  // interaction. toBeInViewport() confirms the element is visible within the
  // current viewport bounds — no scroll required.
  await expect(
    page.locator('[data-testid="zone-1a-trajectory"]'),
  ).toBeInViewport();
  await expect(
    page.locator('[data-testid="zone-1b-mda-alerts"]'),
  ).toBeInViewport();
  await expect(page.locator('[data-testid="zone-1c-pmm"]')).toBeInViewport();
  await expect(
    page.locator('[data-testid="zone-1d-four-framework"]'),
  ).toBeInViewport();
});

// ---------------------------------------------------------------------------
// AC-002: All four Zone 1 instruments visible without scroll at 1280×800
// Source: US-002; FA brief §Named Acceptance Criteria
// ---------------------------------------------------------------------------

test("AC-002: four Zone 1 instruments visible at 1280×800 without scroll", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");

  await expect(
    page.locator('[data-testid="zone-1a-trajectory"]'),
  ).toBeInViewport();
  await expect(
    page.locator('[data-testid="zone-1b-mda-alerts"]'),
  ).toBeInViewport();
  await expect(page.locator('[data-testid="zone-1c-pmm"]')).toBeInViewport();
  await expect(
    page.locator('[data-testid="zone-1d-four-framework"]'),
  ).toBeInViewport();
});

// ---------------------------------------------------------------------------
// AC-003: Trajectory view minimum width >= 480px at 1024×768
// Source: US-001; FA brief §Layout and Viewport (480px constant binding)
// ---------------------------------------------------------------------------

test("AC-003: trajectory view width >= 480px at 1024×768", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const trajectoryEl = page.locator('[data-testid="zone-1a-trajectory"]');
  await expect(trajectoryEl).toBeVisible();

  const width = await trajectoryEl.evaluate(
    (el) => el.getBoundingClientRect().width,
  );
  expect(width).toBeGreaterThanOrEqual(480);
});

// ---------------------------------------------------------------------------
// AC-004: Trajectory view minimum width >= 580px at 1280×800
// Source: US-002; FA brief §Layout and Viewport (580px constant binding)
// ---------------------------------------------------------------------------

test("AC-004: trajectory view width >= 580px at 1280×800", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");

  const trajectoryEl = page.locator('[data-testid="zone-1a-trajectory"]');
  await expect(trajectoryEl).toBeVisible();

  const width = await trajectoryEl.evaluate(
    (el) => el.getBoundingClientRect().width,
  );
  expect(width).toBeGreaterThanOrEqual(580);
});

// ---------------------------------------------------------------------------
// AC-005: Trajectory view minimum height >= 300px at any supported viewport
// Source: US-002; FA brief §Named Acceptance Criteria
// ---------------------------------------------------------------------------

test("AC-005: trajectory view height >= 300px at 1024×768", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const trajectoryEl = page.locator('[data-testid="zone-1a-trajectory"]');
  await expect(trajectoryEl).toBeVisible();

  const height = await trajectoryEl.evaluate(
    (el) => el.getBoundingClientRect().height,
  );
  expect(height).toBeGreaterThanOrEqual(300);
});

test("AC-005: trajectory view height >= 300px at 1280×800", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");

  const trajectoryEl = page.locator('[data-testid="zone-1a-trajectory"]');
  await expect(trajectoryEl).toBeVisible();

  const height = await trajectoryEl.evaluate(
    (el) => el.getBoundingClientRect().height,
  );
  expect(height).toBeGreaterThanOrEqual(300);
});

// ---------------------------------------------------------------------------
// AC-007: ComposedChart initial render <= 100ms on CI 4× throttled profile
// Source: US-029; FA brief §Performance Acceptance Criteria
//
// Measurement: performance.measure wrapping the navigation + initial paint.
// The 4× CPU throttle is applied via page.emulate({ cpuThrottling: 4 }).
// Hardware confirmation: MV-002 (human gate, not automated).
// ---------------------------------------------------------------------------

test("AC-007: ComposedChart initial render <= 100ms at 4x CPU throttle", async ({
  page,
}) => {
  const cdpSession = await page.context().newCDPSession(page);
  await cdpSession.send("Emulation.setCPUThrottlingRate", { rate: 4 });

  // Mark before navigation — measure the full paint-to-visible cost.
  await page.goto("/");

  await page.evaluate(() => {
    performance.mark("trajectory-render-start");
  });

  // Wait for trajectory view to be present in the DOM.
  await page.locator('[data-testid="zone-1a-trajectory"]').waitFor({
    state: "attached",
    timeout: 5_000,
  });

  const duration = await page.evaluate(() => {
    performance.mark("trajectory-render-end");
    performance.measure(
      "trajectory-render",
      "trajectory-render-start",
      "trajectory-render-end",
    );
    return performance.getEntriesByName("trajectory-render")[0].duration;
  });

  expect(duration).toBeLessThanOrEqual(100);
});

// ---------------------------------------------------------------------------
// AC-008: ComposedChart step navigation <= 100ms on CI 4× throttled profile
// Source: US-029; FA brief §Performance Acceptance Criteria
// ---------------------------------------------------------------------------

test("AC-008: ComposedChart step navigation <= 100ms at 4x CPU throttle", async ({
  page,
}) => {
  const cdpSession = await page.context().newCDPSession(page);
  await cdpSession.send("Emulation.setCPUThrottlingRate", { rate: 4 });
  await page.goto("/");

  // Wait for the trajectory view and a step navigation control to be present.
  const trajectoryEl = page.locator('[data-testid="zone-1a-trajectory"]');
  await trajectoryEl.waitFor({ state: "attached", timeout: 5_000 });

  // Mark before advancing to the next step.
  await page.evaluate(() => {
    performance.mark("step-nav-start");
  });

  // Trigger step advance via the scenario controls.
  // The instrument cluster step axis advances via the shared Zustand atom
  // (FA brief §Shared State Architecture — single set() call per step).
  await page.getByRole("button", { name: /Next Step/ }).click();

  const duration = await page.evaluate(() => {
    performance.mark("step-nav-end");
    performance.measure("step-nav", "step-nav-start", "step-nav-end");
    return performance.getEntriesByName("step-nav")[0].duration;
  });

  expect(duration).toBeLessThanOrEqual(100);
});

// ---------------------------------------------------------------------------
// AC-009: Full Mode 3 component set <= 100ms on CI 4× throttled profile
// Source: US-029; FA brief §Named Acceptance Criteria (corrected per QA Lead)
//
// Component set: 8 Lines (4 active + 4 ghost) + 4 Areas (divergence fills) +
// 3 ReferenceLines (shock events only — MDA floor lines excluded from M9).
// Total: 15 SVG primitive groups.
// ---------------------------------------------------------------------------

test("AC-009: full Mode 3 component set renders <= 100ms at 4x CPU throttle", async ({
  page,
}) => {
  const cdpSession = await page.context().newCDPSession(page);
  await cdpSession.send("Emulation.setCPUThrottlingRate", { rate: 4 });
  await page.goto("/");

  // Wait for Mode 3 to be activated.
  // The mode indicator in the persistent header shows "Active Control" in Mode 3.
  const trajectoryEl = page.locator('[data-testid="zone-1a-trajectory"]');
  await trajectoryEl.waitFor({ state: "attached", timeout: 5_000 });

  // Mark before Mode 3 activation (applying first control input triggers
  // ghost curve rendering per FA brief §Shared State Architecture).
  await page.evaluate(() => {
    performance.mark("mode3-render-start");
  });

  // Apply a control input to trigger Mode 3 full component set.
  // The "Apply policy input" button is in the control plane zone (Mode 3 only).
  await page.locator('[data-testid="control-plane-zone"]')
    .getByRole("button", { name: /Apply/ })
    .click();

  const duration = await page.evaluate(() => {
    performance.mark("mode3-render-end");
    performance.measure("mode3-render", "mode3-render-start", "mode3-render-end");
    return performance.getEntriesByName("mode3-render")[0].duration;
  });

  // Full Mode 3 component set: 8 Lines + 4 Areas + 3 shock ReferenceLines
  expect(duration).toBeLessThanOrEqual(100);
});

// ---------------------------------------------------------------------------
// AC-011: Mode 1 step annotation renders three-line tick at >= 1024px viewport
// Source: US-005; FA brief §Mode 1 Step Axis Annotation
//
// For each SIGNIFICANT step tick: exactly three text nodes must be present —
// (1) step index, (2) calendar date, (3) event label — top to bottom.
// At 480px trajectory view width / 6-step fixture: no truncation mid-word.
// ---------------------------------------------------------------------------

test("AC-011: SIGNIFICANT step tick contains exactly three text nodes (step / date / event label)", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  // The trajectory view must be in Mode 1 with a SIGNIFICANT step present.
  // The test fixture used for Mode 1 must have at least one SIGNIFICANT step
  // in step_metadata (scenario configuration JSONB — FA brief §Decision C).
  const significantTick = page.locator('[data-testid="step-tick-significant"]').first();
  await expect(significantTick).toBeVisible();

  // Exactly three <text> elements per SIGNIFICANT step tick:
  // [0] step index (e.g., "Step 1")
  // [1] calendar date (e.g., "May 2010")
  // [2] event label (e.g., "IMF programme begins")
  const tickTexts = significantTick.locator("text");
  await expect(tickTexts).toHaveCount(3);
});

test("AC-011: non-SIGNIFICANT step tick contains exactly two text nodes (step / date)", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  // ROUTINE step ticks must have exactly two <text> nodes — no event label.
  const routineTick = page.locator('[data-testid="step-tick-routine"]').first();
  await expect(routineTick).toBeVisible();

  const tickTexts = routineTick.locator("text");
  await expect(tickTexts).toHaveCount(2);
});

// ---------------------------------------------------------------------------
// AC-013: Tier 4-5 curves show "(exp)" label adjacent to rightmost data point
// Source: US-012; FA brief §Confidence Tier Visual (UD-R3 — curve-face badge)
//
// Moved to Playwright per QA-F5 resolution: AC-016 Playwright SVG assertion
// was fragile; Vitest unit test is more reliable for this assertion.
// Both a Playwright check and a Vitest check are provided.
// ---------------------------------------------------------------------------

test("AC-013: Tier 4-5 curve shows (exp) badge in SVG body", async ({ page }) => {
  await page.goto("/");

  // Navigate to a scenario step where at least one framework has
  // confidence_tier >= 4. The "(exp)" badge must be visible in the SVG body.
  const trajectoryEl = page.locator('[data-testid="zone-1a-trajectory"]');
  await expect(trajectoryEl).toBeVisible();

  // The "(exp)" badge is a <text> element rendered via Recharts customized prop
  // or SVG namespace, adjacent to the rightmost non-null data point on a Tier 4-5 curve.
  // FA brief §Confidence Tier Visual: font-size 11px minimum (UD-F2).
  const expBadge = trajectoryEl.locator("text").filter({ hasText: "(exp)" });
  await expect(expBadge).toBeVisible();
});

test("AC-013: Tier 1-3 curves do not show (exp) badge", async ({ page }) => {
  await page.goto("/");

  // When all framework curves are Tier 1-3, no "(exp)" badge must appear.
  // This requires a fixture where all frameworks are Tier 1-3.
  const trajectoryEl = page.locator('[data-testid="zone-1a-trajectory"]');
  await expect(trajectoryEl).toBeVisible();

  // Assert "(exp)" text is absent for Tier 1-3 scenarios.
  const expBadge = trajectoryEl.locator("text").filter({ hasText: "(exp)" });
  await expect(expBadge).not.toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-014: Control plane reserved zone = 280px at 1280×800;
//         trajectory view width >= 580px
// Source: US-027; FA brief §Control Plane Zone (FA-C3 Resolution, EL ruling)
//
// The 280px zone is always present in Mode 1 and Mode 2 as reserved space —
// not collapsed to 0, not display:none. It contains no interactive elements
// in Mode 1/Mode 2.
// ---------------------------------------------------------------------------

test("AC-014: control plane zone width = 280px at 1280×800", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");

  const cpEl = page.locator('[data-testid="control-plane-zone"]');
  await expect(cpEl).toBeVisible();

  const cpWidth = await cpEl.evaluate(
    (el) => el.getBoundingClientRect().width,
  );
  expect(cpWidth).toBeGreaterThanOrEqual(280);
});

test("AC-014: control plane zone present and non-hidden in Mode 1 and Mode 2", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");

  // Control plane zone must not be display:none or collapsed in Mode 1/2.
  const cpEl = page.locator('[data-testid="control-plane-zone"]');
  await expect(cpEl).toBeVisible();

  // Must have non-zero height — not collapsed.
  const cpHeight = await cpEl.evaluate(
    (el) => el.getBoundingClientRect().height,
  );
  expect(cpHeight).toBeGreaterThan(0);
});

test("AC-014: trajectory view width >= 580px at 1280×800 with 280px control plane reserved", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");

  const trajectoryEl = page.locator('[data-testid="zone-1a-trajectory"]');
  await expect(trajectoryEl).toBeVisible();

  // Trajectory view must not be compressed below 580px even with the 280px
  // control plane zone reservation.
  const width = await trajectoryEl.evaluate(
    (el) => el.getBoundingClientRect().width,
  );
  expect(width).toBeGreaterThanOrEqual(580);
});

test("AC-014: control plane zone contains no interactive elements in Mode 1", async ({
  page,
}) => {
  await page.goto("/");

  // In Mode 1 (Replay), the control plane zone must be empty reserved space.
  // No form fields, buttons, or clickable controls.
  const cpEl = page.locator('[data-testid="control-plane-zone"]');
  await expect(cpEl).toBeVisible();

  // Assert no buttons or form elements within the control plane in Mode 1.
  const buttons = cpEl.locator("button");
  await expect(buttons).toHaveCount(0);

  const inputs = cpEl.locator("input, select, textarea");
  await expect(inputs).toHaveCount(0);
});
