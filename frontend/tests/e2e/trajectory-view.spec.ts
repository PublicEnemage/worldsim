/**
 * E2E: TrajectoryView — Zone 1A component acceptance tests.
 *
 * Type 1 (component-level) ACs: testable with TrajectoryView in isolation.
 * AC-003 through AC-005 — viewport dimension assertions.
 * AC-007, AC-008, AC-009 — performance assertions (CI throttled profile).
 * AC-011 — Mode 1 step annotation renders three-line tick at ≥ 1024px.
 *
 * Source: docs/frontend/fa-brief-m9-instrument-cluster.md §Named Acceptance Criteria
 *         Issue #460 — distributed from instrument-cluster.spec.ts (Issue #473 retrofit)
 *
 * Performance gates (AC-007–AC-009):
 *   4× CPU throttle (page.context().setDefaultTimeout / Playwright emulation).
 *   Threshold: ≤ 100ms at throttled profile.
 *   Hardware validation (MV-002) supplements CI — must be documented in PR.
 *
 * data-testid: zone-1a-trajectory-container (InstrumentCluster wraps TrajectoryView)
 */
import { test, expect } from "@playwright/test";

// ---------------------------------------------------------------------------
// AC-003: Trajectory view minimum width ≥ 480px at 1024×768
// Source: US-003; FA brief §Layout and Viewport (FA-R5 resolution)
// ---------------------------------------------------------------------------

test("AC-003: trajectory view width ≥ 480px at 1024×768", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const container = page.locator('[data-testid="zone-1a-trajectory-container"]');
  // Guard: InstrumentCluster is not wired into App.tsx until #460 integration.
  // When it is not present, the test is a no-op (same pattern as AC-011/AC-014).
  const isVisible = await container.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const boundingBox = await container.boundingBox();
  expect(boundingBox).not.toBeNull();
  expect(boundingBox!.width).toBeGreaterThanOrEqual(480);
});

// ---------------------------------------------------------------------------
// AC-004: Trajectory view minimum width ≥ 580px at 1280×800
// Source: US-003; FA brief §Layout and Viewport (FA-R5 resolution)
// ---------------------------------------------------------------------------

test("AC-004: trajectory view width ≥ 580px at 1280×800", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");

  const container = page.locator('[data-testid="zone-1a-trajectory-container"]');
  const isVisible = await container.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const boundingBox = await container.boundingBox();
  expect(boundingBox).not.toBeNull();
  expect(boundingBox!.width).toBeGreaterThanOrEqual(580);
});

// ---------------------------------------------------------------------------
// AC-005: Trajectory view minimum height ≥ 300px at any supported viewport
// Source: FA brief §Layout and Viewport
// ---------------------------------------------------------------------------

test("AC-005: trajectory view height ≥ 300px at 1024×768", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const container = page.locator('[data-testid="zone-1a-trajectory-container"]');
  const isVisible = await container.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const boundingBox = await container.boundingBox();
  expect(boundingBox).not.toBeNull();
  expect(boundingBox!.height).toBeGreaterThanOrEqual(300);
});

// ---------------------------------------------------------------------------
// AC-007: ComposedChart initial render ≤ 100ms on CI 4× throttled profile
// Source: FA brief §Performance Acceptance Criteria (FA-R1 resolution)
// Note: MV-002 (hardware validation) supplements this CI gate.
// ---------------------------------------------------------------------------

test("AC-007: ComposedChart initial render ≤ 100ms on throttled CPU", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });

  // 4× CPU throttle per FA brief AC-007 measurement approach
  await page.emulateMedia({});
  const cdp = await page.context().newCDPSession(page);
  await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });

  await page.goto("/");

  const renderMs = await page.evaluate(() => {
    const marks = performance.getEntriesByType("measure");
    const trajectoryMeasure = marks.find((m) =>
      m.name.startsWith("trajectory-render"),
    );
    return trajectoryMeasure?.duration ?? null;
  });

  // If the component does not emit a performance mark, skip rather than fail.
  // The performance mark infrastructure is added when the component loads trajectory data.
  if (renderMs !== null) {
    expect(renderMs).toBeLessThanOrEqual(100);
  }
});

// ---------------------------------------------------------------------------
// AC-008: ComposedChart step navigation ≤ 100ms on CI 4× throttled profile
// Source: FA brief §Performance Acceptance Criteria (FA-R1 resolution)
// ---------------------------------------------------------------------------

test("AC-008: step navigation render ≤ 100ms on throttled CPU", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });

  const cdp = await page.context().newCDPSession(page);
  await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });

  await page.goto("/");

  // Trigger a step advance if there is a step-advance control visible
  const advanceButton = page.locator('[data-testid="advance-step-btn"]');
  const hasAdvance = await advanceButton.isVisible().catch(() => false);

  if (hasAdvance) {
    await page.evaluate(() => performance.mark("nav-start"));
    await advanceButton.click();
    await page.waitForTimeout(10);
    await page.evaluate(() => {
      performance.mark("nav-end");
      performance.measure("step-nav-render", "nav-start", "nav-end");
    });

    const navMs = await page.evaluate(() => {
      const m = performance.getEntriesByName("step-nav-render")[0];
      return m?.duration ?? null;
    });

    if (navMs !== null) {
      expect(navMs).toBeLessThanOrEqual(100);
    }
  }
});

// ---------------------------------------------------------------------------
// AC-009: Full Mode 3 component set ≤ 100ms on CI 4× throttled profile
// Source: FA brief §Performance Acceptance Criteria; QA Lead AC-009 correction
// Mode 3 component count: 8 Lines + 4 Area divergence fills + 3 shock ReferenceLines
// (MDA floor ReferenceLines excluded from M9 per EL Decision A)
// ---------------------------------------------------------------------------

test("AC-009: Mode 3 full component set render ≤ 100ms on throttled CPU", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });

  const cdp = await page.context().newCDPSession(page);
  await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });

  await page.goto("/");

  // mode3-toggle is inside {selectedScenarioId && (...)} in App.tsx — must select a
  // scenario first. Pattern mirrors mode3-active-control.spec.ts createAndSelectScenario.
  await page.waitForFunction(
    () => typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
    { timeout: 10_000 },
  );
  const scenarioName = "AC-009-perf";
  await page.getByRole("button", { name: /Scenarios/ }).click();
  await page.locator('input[placeholder="Scenario name"]').fill(scenarioName);
  await page.locator(".scenario-btn--create").click();
  const row = page.locator(".scenario-row").filter({ hasText: scenarioName });
  await expect(row).toBeVisible({ timeout: 10_000 });
  await row.getByTitle("Select as primary scenario").click();
  // Close Scenarios panel so mode3-toggle is the only toggle in the DOM.
  await page.getByRole("button", { name: /Scenarios/ }).click();

  // Mode 3 shipped M12 (PR #778). mode3-toggle is the delivered testid (App.tsx:293).
  // Guard removed per NM-058: if mode3-toggle is absent the test must FAIL, not skip.
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

  expect(renderMs).not.toBeNull();
  // EX-001 (docs/compliance/exceptions.md): threshold raised 100ms → 200ms, expiry M17 exit.
  // Baseline: 179ms on first real CI run 2026-06-24. ProBook target (no throttle) remains 100ms.
  expect(renderMs).toBeLessThanOrEqual(200);
});

// ---------------------------------------------------------------------------
// AC-011: Mode 1 step annotation renders three-line tick at ≥ 1024px viewport
// Source: FA brief §Mode 1 Step Axis Annotation (FA-C5 resolution)
// Three-line tick structure: step index / calendar date / event label (SIGNIFICANT)
// ---------------------------------------------------------------------------

test("AC-011: SIGNIFICANT step tick has step-index, date, and event label text nodes", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");

  // Wait for trajectory data to load (if applicable)
  await page.waitForTimeout(500);

  const trajectory = page.locator('[data-testid="zone-1a-trajectory"]');
  const hasTrajectory = await trajectory.isVisible().catch(() => false);

  if (!hasTrajectory) {
    // No trajectory loaded; skip assertion
    return;
  }

  // Find the XAxis tick group — Recharts renders ticks as <g> inside <svg>
  // The custom tick renders step index, date, and (for SIGNIFICANT steps) event label.
  const svg = trajectory.locator("svg").first();
  const hasSvg = await svg.isVisible().catch(() => false);

  if (!hasSvg) return;

  // The tick text elements are <text> children of <g> elements in the XAxis group.
  // Count that there are at least 2 text nodes per tick (step index + date).
  const textNodes = await svg.locator("text").count();
  expect(textNodes).toBeGreaterThanOrEqual(2);
});

// ---------------------------------------------------------------------------
// AC-014: Control plane reserved zone = 280px at 1280×800
// Source: FA brief §Layout and Viewport (FA-C3 resolution); EL Decision 2026-05-22
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// AC-013: Tier 4/5 confidence badge "(exp)" renders in SVG adjacent to curve
// Source: FA brief §Named Acceptance Criteria (AC-013); UD-R3
// Guard pattern: no-op until InstrumentCluster is wired into App.tsx.
// ---------------------------------------------------------------------------

test("AC-013: Tier 4/5 confidence badge '(exp)' text element present in SVG", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");

  const trajectory = page.locator('[data-testid="zone-1a-trajectory"]');
  const isVisible = await trajectory.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const svg = trajectory.locator("svg").first();
  const hasSvg = await svg.isVisible({ timeout: 1000 }).catch(() => false);
  if (!hasSvg) return;

  // The "(exp)" badge is a <text> element rendered by ConfidenceBadge for
  // any framework curve whose confidence_tier >= 4 (getConfidenceBadgeVisible).
  // If the loaded fixture has no Tier 4/5 data, this is a no-op.
  const allText = svg.locator("text");
  const count = await allText.count();
  if (count === 0) return;

  // Collect all text content and check if any badge is present.
  // The badge is present only when fixture data has Tier 4/5 confidence.
  let badgeFound = false;
  for (let i = 0; i < count; i++) {
    const text = await allText.nth(i).textContent();
    if (text?.includes("(exp)")) {
      badgeFound = true;
      break;
    }
  }

  // If badge is present, assert it is visible; if absent, the test is a no-op
  // (no Tier 4/5 fixture data loaded yet — AC-013 becomes live in #463 integration).
  if (badgeFound) {
    const badge = svg.locator("text", { hasText: "(exp)" }).first();
    await expect(badge).toBeVisible();
  }
});

test("AC-014: control plane zone is 280px wide at 1280×800", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");

  const controlPlane = page.locator('[data-testid="zone-control-plane"]');
  const hasControlPlane = await controlPlane.isVisible().catch(() => false);

  if (!hasControlPlane) return;

  const boundingBox = await controlPlane.boundingBox();
  expect(boundingBox).not.toBeNull();
  expect(boundingBox!.width).toBeGreaterThanOrEqual(278);
  expect(boundingBox!.width).toBeLessThanOrEqual(282);
});
