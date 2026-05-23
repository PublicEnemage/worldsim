/**
 * E2E: Greece Mode 1 step-through — full instrument cluster integration.
 *
 * Issue #463 scope: full Zone 1 cluster (1A–1D) survives a complete Mode 1
 * step-through without assertion failures. Validates the end-to-end flow from
 * scenario creation through step advance through instrument-cluster state.
 *
 * Test coverage:
 *   - Instrument cluster renders at every step (1A–1D all visible)
 *   - data-current-step attribute tracks step advances
 *   - Governance null renders as "—" + score-value--null class (not zero)
 *   - MDA alert panel renders without error (no-alert or alert state)
 *   - Mode indicator shows "Replay" throughout Mode 1
 *   - Mode switch guard: if a mode switcher is present, mode label updates
 *
 * Source: Issue #463 — Zone 1 instrument cluster integration (PR 2 of 2)
 *
 * Setup pattern mirrors scenario-advance.spec.ts:
 *   create scenario via UI → select as primary → advance all 3 default steps.
 *
 * data-testids asserted:
 *   zone-1a-trajectory-container, zone-1b-mda-alerts, zone-1c-pmm,
 *   zone-1d-four-framework, framework-row-governance, framework-score-governance,
 *   mda-no-alerts, mode-indicator
 */
import { test, expect } from "@playwright/test";

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

async function advanceStep(
  page: import("@playwright/test").Page,
  toStep: number,
  totalSteps: number,
) {
  await page.getByRole("button", { name: /Next Step/ }).click();
  await expect(
    page.getByText(`Step ${toStep} / ${totalSteps}`),
  ).toBeVisible({ timeout: 15_000 });
}

// ---------------------------------------------------------------------------
// Smoke: instrument cluster renders immediately after scenario selection
// ---------------------------------------------------------------------------

test("Greece step-through: cluster renders on scenario selection", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");
  await createAndSelectScenario(page, `GRC-smoke-${Date.now()}`);

  // All four Zone 1 instruments must be visible at step 0 (before any advance)
  await expect(
    page.locator('[data-testid="zone-1a-trajectory-container"]'),
  ).toBeVisible({ timeout: 10_000 });
  await expect(
    page.locator('[data-testid="zone-1b-mda-alerts"]'),
  ).toBeVisible();
  await expect(page.locator('[data-testid="zone-1c-pmm"]')).toBeVisible();
  await expect(
    page.locator('[data-testid="zone-1d-four-framework"]'),
  ).toBeVisible();
});

// ---------------------------------------------------------------------------
// Mode 1: mode indicator shows "Replay" before and during step advances
// ---------------------------------------------------------------------------

test("Greece step-through: mode indicator shows Replay throughout Mode 1", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");
  await createAndSelectScenario(page, `GRC-mode-${Date.now()}`);

  const indicator = page.locator('[data-testid="mode-indicator"]');
  await expect(indicator).toBeVisible({ timeout: 10_000 });
  await expect(indicator).toHaveText("Replay");
  await expect(indicator).toHaveAttribute("data-mode", "MODE_1");

  // Advance step 1 — mode must remain Replay
  await advanceStep(page, 1, 3);
  await expect(indicator).toHaveText("Replay");
  await expect(indicator).toHaveAttribute("data-mode", "MODE_1");
});

// ---------------------------------------------------------------------------
// data-current-step attribute tracks step advances on Zone 1D
// ---------------------------------------------------------------------------

test("Greece step-through: data-current-step tracks step advances", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");
  await createAndSelectScenario(page, `GRC-steps-${Date.now()}`);

  const fourFramework = page.locator('[data-testid="zone-1d-four-framework"]');
  await expect(fourFramework).toBeVisible({ timeout: 10_000 });

  // Step 0 on initial selection
  await expect(fourFramework).toHaveAttribute("data-current-step", "0");

  await advanceStep(page, 1, 3);
  await expect(fourFramework).toHaveAttribute("data-current-step", "1");

  await advanceStep(page, 2, 3);
  await expect(fourFramework).toHaveAttribute("data-current-step", "2");

  await advanceStep(page, 3, 3);
  await expect(fourFramework).toHaveAttribute("data-current-step", "3");
});

// ---------------------------------------------------------------------------
// Governance null: score-value--null class + "—" text (DD-011 / US-022)
//
// In Mode 1, governance may have null composite_score (no measurement yet).
// If null, the class and display text must match the null governance treatment.
// If a score exists, the class must be score-value--numeric.
// ---------------------------------------------------------------------------

test("Greece step-through: governance null renders as — not zero (AC-015)", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");
  await createAndSelectScenario(page, `GRC-gov-${Date.now()}`);

  const fourFramework = page.locator('[data-testid="zone-1d-four-framework"]');
  await expect(fourFramework).toBeVisible({ timeout: 10_000 });

  const govScore = page.locator('[data-testid="framework-score-governance"]');
  await expect(govScore).toBeVisible();

  // Determine whether governance is null or numeric at step 0
  const govClass = await govScore.getAttribute("class");
  const govText = await govScore.textContent();

  if (govClass?.includes("score-value--null")) {
    // Null case: must display "—", must not display "0" or "0.00"
    expect(govText?.trim()).toBe("—");
    expect(govText?.trim()).not.toBe("0");
    expect(govText?.trim()).not.toBe("0.00");
  } else {
    // Numeric case: class must be score-value--numeric, text must not be "—"
    expect(govClass).toContain("score-value--numeric");
    expect(govText?.trim()).not.toBe("—");
  }
});

// ---------------------------------------------------------------------------
// Full step-through: cluster remains visible and internally consistent at
// every step (no React errors, no missing testids)
// ---------------------------------------------------------------------------

test("Greece step-through: cluster consistent at all 3 steps", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");
  await createAndSelectScenario(page, `GRC-full-${Date.now()}`);

  const cluster = page.locator('[data-testid="zone-1a-trajectory-container"]');
  await expect(cluster).toBeVisible({ timeout: 10_000 });

  const nextStepBtn = page.getByRole("button", { name: /Next Step/ });

  for (let step = 1; step <= 3; step++) {
    await nextStepBtn.click();
    await expect(page.getByText(`Step ${step} / 3`)).toBeVisible({
      timeout: 15_000,
    });

    // All four instruments must remain visible after each advance
    await expect(
      page.locator('[data-testid="zone-1a-trajectory-container"]'),
    ).toBeVisible();
    await expect(
      page.locator('[data-testid="zone-1b-mda-alerts"]'),
    ).toBeVisible();
    await expect(page.locator('[data-testid="zone-1c-pmm"]')).toBeVisible();
    await expect(
      page.locator('[data-testid="zone-1d-four-framework"]'),
    ).toBeVisible();

    // Zone 1B must show either the no-alert state or alert rows — never a blank
    const noAlerts = page.locator('[data-testid="mda-no-alerts"]');
    const alertRow = page.locator('[data-testid="mda-alert-row"]');
    const hasNoAlerts = await noAlerts.isVisible().catch(() => false);
    const hasAlertRow = await alertRow.first().isVisible().catch(() => false);
    expect(hasNoAlerts || hasAlertRow).toBe(true);

    // All four framework rows must render
    for (const fw of [
      "financial",
      "human_development",
      "ecological",
      "governance",
    ]) {
      await expect(
        page.locator(`[data-testid="framework-row-${fw}"]`),
      ).toBeVisible();
    }
  }

  // After final step, advance button must be disabled
  await expect(nextStepBtn).toBeDisabled();
});

// ---------------------------------------------------------------------------
// Mode switch guard: if a mode switcher is wired, indicator updates
// (Mode 2 wiring is deferred to M10; this test is a no-op until then)
// ---------------------------------------------------------------------------

test("Greece step-through: mode switch updates indicator label (guard)", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");
  await createAndSelectScenario(page, `GRC-modeswitch-${Date.now()}`);

  // Guard: mode switcher not wired in M9 — skip if not present
  const mode2Trigger = page.locator('[data-testid="mode-2-activate"]');
  const hasMode2 = await mode2Trigger.isVisible({ timeout: 2_000 }).catch(() => false);
  if (!hasMode2) return;

  const indicator = page.locator('[data-testid="mode-indicator"]');
  await expect(indicator).toHaveText("Replay");

  await mode2Trigger.click();
  await expect(indicator).toHaveText("Simulation");
  await expect(indicator).toHaveAttribute("data-mode", "MODE_2");
});
