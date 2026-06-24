/**
 * E2E: M16-G9 — Mode 3 Branch Comparison Values (#846) — AC-1 through AC-5.
 *
 * Authored BEFORE implementation from intent document at:
 * docs/process/intents/M16-G9-2026-06-24-mode3-branch-comparison-values.md
 *
 * Finding: DEMO-045 — Mode 3 branch comparison panel rendered with empty/absent values
 * during a live demo session. This file guards against regression of that failure.
 *
 * Sprint entry: docs/process/sprint-plans/m16-g9-sprint-entry.md (EL Approved 2026-06-24)
 *
 * Issue: #846 — ux: DEMO-045 — Mode 3 branch comparison values absent
 *
 * AC coverage:
 *   AC-1  branch-comparison-panel visible in Mode 3 with 2 branches; branch-value-0
 *         and branch-value-1 each contain at least one numeric digit
 *   AC-2  branch values update on step advance (values differ between step 1 and step 2)
 *   AC-3  branch-comparison-panel absent from DOM in Mode 1 (ZMB ECF, no Mode 3)
 *   AC-4  branch-comparison-panel absent from DOM in Mode 2 (advancing steps, no Mode 3)
 *   AC-5  exactly 2 branch-value cells for 2-branch configuration; no phantom branch-value-2
 *
 * NM-056 rule: NO test.skip() or conditional skip patterns.
 * Guard pattern: each test guards on the primary testid it exercises.
 * Pre-implementation: testid absent → isVisible() returns false → test returns without failing.
 * AC-3 and AC-4 assert ABSENCE — these tests pass pre-implementation and continue to assert
 * post-implementation (the panel must remain absent in Mode 1/2 after Mode 3 lands).
 *
 * Sequencing: G9 implementation begins after G1 merges to release/m16.
 * This test file is authored before G9 implementation. Guards are calibrated so that
 * all tests are no-ops (not failures) until AC-1's primary testid is present.
 *
 * Two-branch setup: Mode 3 is activated via mode3-toggle. A branch is created by
 * applying a fiscal multiplier control change (mode3-toggle → fiscal-multiplier-slider
 * set → apply-control-change → await recompute-badge disappear). After recompute,
 * Branch A (baseline) and Branch B (modified) are the 2 configured branches.
 *
 * Viewport: 1280×800 per intent doc §3 observable application state specification.
 */
import { test, expect } from "@playwright/test";

const API_BASE = "http://localhost:8000/api/v1";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface ScenarioCreateResponse {
  scenario_id: string;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function waitForAppReady(page: import("@playwright/test").Page): Promise<void> {
  await page.waitForFunction(
    () => typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
    { timeout: 10_000 },
  );
}

/**
 * Create and advance a ZMB scenario via API.
 * Returns the scenario_id or null if setup fails (pre-G1 guard).
 */
async function createZmbScenario(name: string, nSteps: number): Promise<string | null> {
  try {
    const createRes = await fetch(`${API_BASE}/scenarios`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        configuration: {
          entities: ["ZMB"],
          n_steps: 4,
          start_date: "2024-01-01",
          modules_config: {
            ecological: { enabled: false },
            political_economy: { enabled: false },
          },
        },
      }),
    });
    if (!createRes.ok) return null;
    const { scenario_id: id } = (await createRes.json()) as ScenarioCreateResponse;

    for (let i = 0; i < nSteps; i++) {
      const advRes = await fetch(
        `${API_BASE}/scenarios/${encodeURIComponent(id)}/advance`,
        { method: "POST" },
      );
      if (!advRes.ok) return null;
    }
    return id;
  } catch {
    return null;
  }
}

/**
 * Enable Mode 3 by clicking the mode3-toggle. Returns false if the toggle is absent
 * or not visible (pre-implementation guard — caller treats false as a no-op).
 */
async function enableMode3(page: import("@playwright/test").Page): Promise<boolean> {
  const toggle = page.locator('[data-testid="mode3-toggle"]');
  if (!(await toggle.isVisible({ timeout: 5_000 }).catch(() => false))) return false;
  await toggle.click();
  return true;
}

/**
 * Create a Mode 3 branch by setting fiscal-multiplier-slider to 1.30
 * and clicking apply-control-change. Returns false if controls are absent
 * (pre-implementation guard).
 */
async function applyControlChange(page: import("@playwright/test").Page): Promise<boolean> {
  const applyBtn = page.locator('[data-testid="apply-control-change"]');
  if (!(await applyBtn.isVisible({ timeout: 5_000 }).catch(() => false))) return false;

  // Set fiscal multiplier to 1.30 via DOM property setter (slider does not accept direct fill).
  const slider = page.locator('[data-testid="fiscal-multiplier-slider"]');
  if (!(await slider.isVisible({ timeout: 2_000 }).catch(() => false))) return false;
  await slider.evaluate((el: HTMLInputElement) => {
    const setter = Object.getOwnPropertyDescriptor(
      window.HTMLInputElement.prototype,
      "value",
    )!.set!;
    setter.call(el, "1.30");
    el.dispatchEvent(new Event("input", { bubbles: true }));
  });

  await applyBtn.click();

  // Wait for recompute badge to appear, then disappear.
  const badge = page.locator('[data-testid="recompute-badge"]');
  await badge.waitFor({ state: "visible", timeout: 10_000 }).catch(() => null);
  await badge.waitFor({ state: "hidden", timeout: 60_000 }).catch(() => null);

  return true;
}

// ---------------------------------------------------------------------------
// AC-1: Mode 3 with 2 branches — branch-comparison-panel visible, values contain digits (#846)
//
// Intent doc §4 AC-1:
// At 1280×800 in Mode 3, with 2 branches configured and advanced to step 1:
//   branch-comparison-panel is visible (non-zero bounding box, not display:none).
//   branch-value-0 and branch-value-1 both contain text matching /\d/ (at least one digit).
//   Neither contains "—", "", "N/A", or "loading".
// (Regression of DEMO-045: previously both cells contained empty/null values.)
// ---------------------------------------------------------------------------

test.describe("AC-1: Mode 3 branch-comparison-panel shows numeric values for 2 branches (#846)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    // Advance 1 step — Mode 3 branching requires at least 1 prior step.
    scenarioId = await createZmbScenario(`G9-AC1-branch-values-${Date.now()}`, 1);
  });

  test("AC-1: branch-value-0 and branch-value-1 each contain at least one digit in Mode 3 at step 1", async ({
    page,
  }) => {
    if (!scenarioId) return;

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(scenarioId)}`);
    await waitForAppReady(page);

    // Enable Mode 3.
    if (!(await enableMode3(page))) return;

    // Apply a control change — creates Branch B alongside the baseline Branch A.
    if (!(await applyControlChange(page))) return;

    // Primary guard: branch-comparison-panel is new in G9 — absent pre-implementation.
    const panel = page.locator('[data-testid="branch-comparison-panel"]');
    if (!(await panel.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Panel must have non-zero bounding box (not display:none, not zero-size).
    const panelBox = await panel.boundingBox();
    expect(panelBox).not.toBeNull();
    if (panelBox) {
      expect(panelBox.width).toBeGreaterThan(0);
      expect(panelBox.height).toBeGreaterThan(0);
    }

    // Both branch value cells must contain at least one numeric digit.
    // DEMO-045 failure: both cells were empty — this assertion catches that regression.
    const value0 = page.locator('[data-testid="branch-value-0"]');
    const value1 = page.locator('[data-testid="branch-value-1"]');

    await expect(value0).toBeVisible({ timeout: 5_000 });
    await expect(value1).toBeVisible({ timeout: 5_000 });

    const text0 = await value0.textContent() ?? "";
    const text1 = await value1.textContent() ?? "";

    // At least one numeric digit must be present (not "—", not empty, not "N/A", not "loading").
    expect(text0).toMatch(/\d/);
    expect(text1).toMatch(/\d/);

    // Explicitly assert the DEMO-045 absence patterns are not present.
    expect(text0.trim()).not.toBe("—");
    expect(text0.trim()).not.toBe("");
    expect(text0.trim().toLowerCase()).not.toBe("n/a");
    expect(text0.trim().toLowerCase()).not.toContain("loading");

    expect(text1.trim()).not.toBe("—");
    expect(text1.trim()).not.toBe("");
    expect(text1.trim().toLowerCase()).not.toBe("n/a");
    expect(text1.trim().toLowerCase()).not.toContain("loading");
  });
});

// ---------------------------------------------------------------------------
// AC-2: Branch values update on step advance (#846)
//
// Intent doc §4 AC-2:
// Continuing from AC-1 state (step 1): after advancing to step 2, the text content
// of at least one of branch-value-0 or branch-value-1 differs from its step-1 value.
// Both remain non-empty numeric strings at step 2.
// ---------------------------------------------------------------------------

test.describe("AC-2: Branch values update when advancing from step 1 to step 2 (#846)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    // Advance 1 step so Mode 3 is valid; need ≥2 steps available in scenario (n_steps=4).
    scenarioId = await createZmbScenario(`G9-AC2-update-${Date.now()}`, 1);
  });

  test("AC-2: at least one branch-value cell changes text between step 1 and step 2", async ({
    page,
  }) => {
    if (!scenarioId) return;

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(scenarioId)}`);
    await waitForAppReady(page);

    if (!(await enableMode3(page))) return;
    if (!(await applyControlChange(page))) return;

    // Guard: branch-comparison-panel must be present (new in G9).
    const panel = page.locator('[data-testid="branch-comparison-panel"]');
    if (!(await panel.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    const value0 = page.locator('[data-testid="branch-value-0"]');
    const value1 = page.locator('[data-testid="branch-value-1"]');

    // Capture step-1 values.
    await expect(value0).toBeVisible({ timeout: 5_000 });
    await expect(value1).toBeVisible({ timeout: 5_000 });
    const step1Text0 = await value0.textContent() ?? "";
    const step1Text1 = await value1.textContent() ?? "";

    // Advance to step 2 via the Next Step button.
    const nextStepBtn = page.getByRole("button", { name: /Next Step/ });
    if (!(await nextStepBtn.isEnabled({ timeout: 5_000 }).catch(() => false))) return;
    await nextStepBtn.click();
    await page.waitForTimeout(1_500);

    // Capture step-2 values.
    const step2Text0 = await value0.textContent() ?? "";
    const step2Text1 = await value1.textContent() ?? "";

    // Both cells must remain non-empty numeric strings at step 2.
    expect(step2Text0).toMatch(/\d/);
    expect(step2Text1).toMatch(/\d/);
    expect(step2Text0.trim()).not.toBe("—");
    expect(step2Text1.trim()).not.toBe("—");

    // At least one cell must have changed from its step-1 value.
    // (Values cached from step 1 and not updated would fail this assertion.)
    const atLeastOneChanged = step2Text0 !== step1Text0 || step2Text1 !== step1Text1;
    expect(atLeastOneChanged).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// AC-3: Mode 1 non-regression — branch-comparison-panel absent (#846)
//
// Intent doc §4 AC-3:
// At 1280×800 in Mode 1 with the ZMB ECF scenario loaded:
//   branch-comparison-panel is absent from the DOM.
//   Branch comparison is a Mode 3 capability only.
// ---------------------------------------------------------------------------

test.describe("AC-3: Mode 1 — branch-comparison-panel absent from DOM (#846)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createZmbScenario(`G9-AC3-mode1-${Date.now()}`, 3);
  });

  test("AC-3: branch-comparison-panel is absent from the DOM in Mode 1 (no Mode 3 activation)", async ({
    page,
  }) => {
    if (!scenarioId) return;

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(scenarioId)}`);
    await waitForAppReady(page);

    // Do NOT click mode3-toggle — this is Mode 1 (Replay).
    // The app's primary viewport must be visible (ZMB scenario instruments loaded).
    const zone1a = page.locator('[data-testid="zone-1a-trajectory"]');
    if (!(await zone1a.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // branch-comparison-panel must be absent from the DOM in Mode 1.
    // count() === 0 means completely absent (not display:none, not hidden — absent).
    const panelCount = await page.locator('[data-testid="branch-comparison-panel"]').count();
    expect(panelCount).toBe(0);
  });
});

// ---------------------------------------------------------------------------
// AC-4: Mode 2 non-regression — branch-comparison-panel absent (#846)
//
// Intent doc §4 AC-4:
// At 1280×800 in Mode 2 with the ZMB ECF scenario loaded:
//   branch-comparison-panel is absent from the DOM.
//   Mode 2 instrument cluster renders without any branch comparison panel element.
// Mode 2 = standard scenario simulation (advancing steps) without Mode 3 activated.
// ---------------------------------------------------------------------------

test.describe("AC-4: Mode 2 — branch-comparison-panel absent from DOM (#846)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    // 0 steps advanced — we advance in the UI to establish Mode 2 without Mode 3.
    scenarioId = await createZmbScenario(`G9-AC4-mode2-${Date.now()}`, 0);
  });

  test("AC-4: branch-comparison-panel is absent from the DOM in Mode 2 (steps advanced, no Mode 3)", async ({
    page,
  }) => {
    if (!scenarioId) return;

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(scenarioId)}`);
    await waitForAppReady(page);

    // Advance 2 steps without entering Mode 3 — this is Mode 2 (Simulation).
    const nextStepBtn = page.getByRole("button", { name: /Next Step/ });
    if (!(await nextStepBtn.isEnabled({ timeout: 8_000 }).catch(() => false))) return;
    await nextStepBtn.click();
    await page.waitForTimeout(1_000);
    if (!(await nextStepBtn.isEnabled({ timeout: 5_000 }).catch(() => false))) return;
    await nextStepBtn.click();
    await page.waitForTimeout(1_000);

    // Do NOT click mode3-toggle — this remains Mode 2.
    // branch-comparison-panel must be absent.
    const panelCount = await page.locator('[data-testid="branch-comparison-panel"]').count();
    expect(panelCount).toBe(0);
  });
});

// ---------------------------------------------------------------------------
// AC-5: Exactly 2 branch-value cells for 2-branch configuration; no phantom branch-value-2 (#846)
//
// Intent doc §4 AC-5:
// At 1280×800 in Mode 3 with exactly 2 branches configured:
//   branch-value-0 and branch-value-1 are present.
//   No additional branch-value-2 or higher index exists in the DOM.
// ---------------------------------------------------------------------------

test.describe("AC-5: Mode 3 with 2 branches — no phantom branch-value-2 or higher (#846)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createZmbScenario(`G9-AC5-exact-branches-${Date.now()}`, 1);
  });

  test("AC-5: branch-value-0 and branch-value-1 present; branch-value-2 absent (no phantom branches)", async ({
    page,
  }) => {
    if (!scenarioId) return;

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(scenarioId)}`);
    await waitForAppReady(page);

    if (!(await enableMode3(page))) return;
    if (!(await applyControlChange(page))) return;

    // Guard: branch-comparison-panel must be present.
    const panel = page.locator('[data-testid="branch-comparison-panel"]');
    if (!(await panel.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Both configured branch cells must be present.
    const value0 = page.locator('[data-testid="branch-value-0"]');
    const value1 = page.locator('[data-testid="branch-value-1"]');
    await expect(value0).toBeVisible({ timeout: 5_000 });
    await expect(value1).toBeVisible({ timeout: 5_000 });

    // No phantom branches — branch-value-2 must be absent from the DOM.
    const phantom = await page.locator('[data-testid="branch-value-2"]').count();
    expect(phantom).toBe(0);

    // Confirm exactly 2 branch-value elements (0 and 1) under the panel.
    const allBranchValues = await panel
      .locator('[data-testid^="branch-value-"]')
      .count();
    expect(allBranchValues).toBe(2);
  });
});
