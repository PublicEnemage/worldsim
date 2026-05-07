/**
 * WorldSim Stakeholder Demo — Playwright Walkthrough
 *
 * This script automates the live application sequence from the stakeholder
 * demonstration guide (docs/demo/stakeholder-walkthrough.md §Section 2).
 *
 * HOW TO RUN:
 *   ./scripts/demo.sh --run
 *   — or —
 *   cd frontend && npx playwright test tests/e2e/demo.spec.ts \
 *       --config playwright.demo.config.ts --headed
 *
 * The browser runs visible at 0.8× pace (slowMo: 800 in playwright.demo.config.ts).
 * page.pause() calls open the Playwright inspector — press "Resume" to advance
 * to the next demo step when the audience is ready. This gives the presenter
 * full control of pacing without time pressure.
 *
 * DO NOT include this file in CI test runs. It requires a live stack
 * (Docker Compose up + migrations + Natural Earth seed). The CI playwright
 * script uses playwright.config.ts which excludes demo.spec.ts by convention
 * (CI runs all specs; add a grep filter if needed: --grep-invert @demo).
 *
 * ──────────────────────────────────────────────────────────────────────────
 * PRESENTER TALKING POINTS — read before the demo, narrate alongside pauses
 * ──────────────────────────────────────────────────────────────────────────
 *
 * STEP 1 — MAP LOADS
 *   "This is the baseline view. The choropleth shows a simulation attribute
 *   across entities — in this case, a GDP growth rate from the most recently
 *   completed scenario step. Each country is colored by its simulated value.
 *   Click any country to open its analysis panel. What makes this different
 *   from a data visualization tool will become clear in a moment."
 *
 * STEP 2 — SCENARIO PANEL OPENS
 *   "We're going to model Greece's 2010–2012 fiscal adjustment programme.
 *   This is a historical case — we know what happened. In the simulation,
 *   we inject the IMF programme conditions as scheduled inputs: the fiscal
 *   tightening, the emergency declarations, the structural conditionality.
 *   Then we advance step by step and observe what the model produces.
 *   The reason we start with a historical case is the backtesting
 *   discipline — which we'll come back to."
 *
 * STEP 3 — SCENARIO CREATED AND SELECTED
 *   "The scenario is now the active primary scenario. The step counter
 *   shows 0 of 3 steps completed — we haven't run the simulation yet.
 *   Each step corresponds to one programme year: 2010, 2011, 2012."
 *
 * STEP 4 — ADVANCE STEP 1
 *   "Step 1. Year 2010. The simulation applies the first year of fiscal
 *   tightening. Watch the choropleth — Greece shifts as the contraction
 *   propagates through the model's relationship graph."
 *
 * STEP 5 — ADVANCE STEP 2
 *   "Step 2. Year 2011. The fiscal contraction compounds. In the historical
 *   case, Greece's GDP contracted -9.1% this year — deeper than 2010."
 *
 * STEP 6 — ADVANCE STEP 3
 *   "Step 3. Year 2012. Programme complete. Three years of fiscal adjustment,
 *   modeled across the full programme horizon. Now let's look inside."
 *
 * STEP 7 — ENTITY DRAWER OPENS
 *   "This panel is the primary analytical surface."
 *   [PAUSE — let the audience read it. Say nothing for 3–5 seconds.]
 *
 * STEP 8 — MDA ALERT PANEL CALLED OUT
 *   "I want to draw your attention to the top of the panel. These are
 *   Minimum Descent Altitude alerts — the terminology comes from aviation.
 *   An MDA is the altitude below which an aircraft cannot safely descend
 *   given the terrain. In this simulation, MDAs are human cost floors:
 *   levels below which consequences become irreversible, or where standard
 *   policy frameworks no longer provide protection.
 *
 *   Read this alert as a piece of evidence: 'Under this fiscal adjustment
 *   path, [indicator] crosses the critical threshold at programme year 3.
 *   This affects primarily [cohort].' That sentence is specific enough to
 *   cite in a negotiation. This is what capability analysis means in practice.
 *   The finance ministry specialist is not being alarmed. She is being handed
 *   a finding she can use."
 *
 * STEP 9 — RADAR CHART CALLED OUT
 *   "Below the alert panel is the radar chart — four axes, one for each
 *   measurement framework: financial, human development, ecological, governance.
 *   The chart tells you which dimensions are under stress, supporting the
 *   threshold scan the alert panel completed. I will be honest about what
 *   is not on screen yet: the ecological axis shows preliminary values. Full
 *   composite scores for all four axes ship in Milestone 8."
 *
 * STEP 10 — COMPARE MODE ENTERED
 *   "This is the counter-proposal function. Once we have identified which
 *   terms produce threshold crossings, we model an alternative. The
 *   DeltaChoropleth shows where the two scenarios diverge geographically.
 *   The argument becomes: 'This path crosses the threshold. This alternative
 *   achieves the same primary fiscal objective and does not. Here is the
 *   evidence for both.'"
 *
 * ──────────────────────────────────────────────────────────────────────────
 */

import { test, expect } from "@playwright/test";

// Scenario name unique per run so repeated demos do not collide.
// In production demos, a pre-seeded scenario can be looked up by name instead.
const DEMO_SCENARIO_NAME = `Greece 2010-2012 Demo — ${new Date().toISOString().slice(0, 10)}`;
const COMPARE_SCENARIO_NAME = `Greece Alternative — ${new Date().toISOString().slice(0, 10)}`;

test(
  "Stakeholder demo walkthrough — Greece 2010–2012 full sequence",
  // Mark so CI grep filters can exclude: --grep-invert @demo
  { tag: ["@demo"] },
  async ({ page }) => {
    // ── STEP 1: Map loads ────────────────────────────────────────────────────
    // TALKING POINT: "This is the baseline view..."
    // (see full script in file header above)

    await page.goto("/");

    // Wait for the test seam — confirms React has mounted and the app is
    // fully interactive. The seam is DEV-only and disappears in production.
    await page.waitForFunction(
      () =>
        typeof (window as Record<string, unknown>).__worldsim_selectEntity ===
        "function",
      { timeout: 15_000 },
    );

    // Map is visible. Give presenter a moment to set the scene.
    await page.pause();

    // ── STEP 2: Open scenario panel ──────────────────────────────────────────
    // TALKING POINT: "We're going to model Greece's 2010–2012 programme..."

    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(800);

    // Pause for presenter to explain the scenario creation flow.
    await page.pause();

    // ── STEP 3: Create and select the Greece scenario ────────────────────────
    // TALKING POINT: "The scenario is now the active primary scenario..."

    await page.locator('input[placeholder="Scenario name"]').fill(DEMO_SCENARIO_NAME);
    await page.locator(".scenario-btn--create").click();

    const scenarioRow = page
      .locator(".scenario-row")
      .filter({ hasText: DEMO_SCENARIO_NAME });
    await expect(scenarioRow).toBeVisible({ timeout: 20_000 });

    await scenarioRow.getByTitle("Select as primary scenario").click();
    await page.waitForTimeout(600);

    // Close panel to reveal the choropleth.
    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(600);

    // Confirm step counter at 0 is not visible (no steps advanced yet).
    // The "Next Step" button is the presenter's advance control.
    const nextStepBtn = page.getByRole("button", { name: /Next Step/ });
    await expect(nextStepBtn).toBeVisible({ timeout: 10_000 });

    await page.pause();

    // ── STEP 4: Advance to Step 1 ────────────────────────────────────────────
    // TALKING POINT: "Step 1. Year 2010..."

    await nextStepBtn.click();
    await expect(page.getByText("Step 1 / 3")).toBeVisible({ timeout: 20_000 });

    // Give the choropleth time to update visually before the presenter speaks.
    await page.waitForTimeout(1_200);
    await page.pause();

    // ── STEP 5: Advance to Step 2 ────────────────────────────────────────────
    // TALKING POINT: "Step 2. Year 2011..."

    await nextStepBtn.click();
    await expect(page.getByText("Step 2 / 3")).toBeVisible({ timeout: 20_000 });

    await page.waitForTimeout(1_200);
    await page.pause();

    // ── STEP 6: Advance to Step 3 ────────────────────────────────────────────
    // TALKING POINT: "Step 3. Year 2012. Programme complete..."

    await nextStepBtn.click();
    await expect(page.getByText("Step 3 / 3")).toBeVisible({ timeout: 20_000 });
    await expect(page.getByText(/Complete/)).toBeVisible({ timeout: 10_000 });

    // The Advance button becomes disabled at completion — this is visible to
    // the audience and confirms the programme horizon has been reached.
    await expect(nextStepBtn).toBeDisabled();

    await page.waitForTimeout(1_200);
    await page.pause();

    // ── STEP 7: Open entity drawer for Greece ────────────────────────────────
    // TALKING POINT: "This panel is the primary analytical surface."
    // [PAUSE — let them read. Say nothing for 3–5 seconds.]

    // Use the test seam — avoids clicking on the WebGL canvas, which is
    // unreliable at map zoom levels in automated browsers.
    await page.evaluate(() => {
      (window as Record<string, (id: string) => void>).__worldsim_selectEntity(
        "GRC",
      );
    });

    // Drawer must open and show measurement output — not the placeholder.
    await expect(page.getByLabel("Close drawer")).toBeVisible({ timeout: 20_000 });
    await expect(page.getByText("Greece")).toBeVisible({ timeout: 10_000 });
    await expect(
      page.getByText("Advance the scenario at least one step to view measurement output."),
    ).not.toBeVisible();

    // Confirm both primary surfaces are rendered before pausing.
    await expect(page.getByText("Multi-Framework Overview")).toBeVisible({
      timeout: 10_000,
    });

    // Long pause — presenter explains the drawer layout before calling out alerts.
    await page.waitForTimeout(1_500);
    await page.pause();

    // ── STEP 8: MDA alert panel called out ───────────────────────────────────
    // TALKING POINT: "I want to draw your attention to the top of the panel..."
    //
    // The "MDA Threshold Breaches" heading appears only when alerts are present.
    // If no alerts fired (no MacroeconomicModule inputs at step 1 by default),
    // the "No active MDA threshold breaches." message is shown instead — which
    // is still the correct surface to call out (it confirms the tool is scanning).
    //
    // In a production demo with a pre-seeded Greece backtesting scenario
    // (FiscalPolicyInput at step 1), alerts will fire. The ScenarioPanel
    // create flow uses the default entity-only config with no ControlInputs,
    // so the MDA panel will show "No active MDA threshold breaches." — the
    // presenter should acknowledge this honestly:
    // "In a fully configured backtesting scenario, this panel would show
    // specific threshold breaches. The surface is live — the alerts appear
    // when the model detects a crossing."
    //
    // To demo with live alerts: pre-seed the Greece 2010-2012 backtesting
    // scenario via the API before running this script (see docs/demo/).

    const mdaSection = page.getByText(
      /MDA Threshold Breaches|No active MDA threshold breaches/,
    );
    await expect(mdaSection).toBeVisible({ timeout: 10_000 });

    await page.waitForTimeout(2_000);
    await page.pause();

    // ── STEP 9: Radar chart called out ───────────────────────────────────────
    // TALKING POINT: "Below the alert panel is the radar chart — four axes..."

    await expect(page.getByText("Multi-Framework Overview")).toBeVisible();

    // Scroll the drawer to ensure the radar chart is in the visible viewport.
    await page.evaluate(() => {
      const drawer = document.querySelector('[aria-label="Close drawer"]')
        ?.closest('div[style*="position: absolute"]');
      if (drawer) drawer.scrollTop = 0;
    });

    await page.waitForTimeout(1_500);
    await page.pause();

    // ── STEP 10: Enter compare mode ──────────────────────────────────────────
    // TALKING POINT: "This is the counter-proposal function..."

    // Close the entity drawer first to return to the full map view.
    await page.getByLabel("Close drawer").click();
    await page.waitForTimeout(600);

    // Open scenarios panel to create the comparison scenario.
    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(600);

    await page.locator('input[placeholder="Scenario name"]').fill(COMPARE_SCENARIO_NAME);
    await page.locator(".scenario-btn--create").click();

    const compareRow = page
      .locator(".scenario-row")
      .filter({ hasText: COMPARE_SCENARIO_NAME });
    await expect(compareRow).toBeVisible({ timeout: 20_000 });

    // Tag the new scenario as the comparison scenario.
    await compareRow.getByTitle("Select as comparison scenario").click();
    await page.waitForTimeout(600);

    // Close the scenarios panel.
    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(600);

    // Enable compare mode via the header checkbox.
    const compareCheckbox = page.locator('input[type="checkbox"]').filter({
      has: page.locator(":scope"),
    }).first();
    // Use the label text to find it reliably.
    await page.getByText("Compare scenarios").click();
    await page.waitForTimeout(800);

    // The DeltaChoropleth renders when both scenarios are selected and
    // compare mode is active. It replaces the ChoroplethMap in the main view.
    // With both scenarios at different step counts (primary at step 3,
    // comparison at step 0), the delta will show zero deltas — which is
    // honest: no divergence yet because the comparison scenario has not been
    // advanced. In a production demo, both scenarios would be at the same step.

    await page.waitForTimeout(1_500);
    await page.pause();

    // ── Demo complete ────────────────────────────────────────────────────────
    // The presenter continues with backtesting credibility (Section 3),
    // roadmap (Section 4), and the North Star closing (Section 5) verbally.
    // No further automation — those sections are slide or verbal content.
    //
    // See docs/demo/stakeholder-walkthrough.md for the full script.
  },
);
