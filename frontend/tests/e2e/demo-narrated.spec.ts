/**
 * WorldSim Stakeholder Demo — Screen-Recorded Narrated Walkthrough
 *
 * This is the screen-recording variant of demo.spec.ts. Every page.pause()
 * has been replaced with a synchronous TTS call via scripts/speak.sh so the
 * demo runs end-to-end without human input, suitable for recording.
 *
 * ── RECORDING MODE ───────────────────────────────────────────────────────────
 *
 * Before recording:
 *   1. Start the full stack: docker compose up (or ./scripts/demo.sh --up)
 *   2. Ensure Natural Earth seed data is loaded.
 *   3. Pre-create the Greece 2010-2012 backtesting scenario via the API so
 *      the "create" step is demonstrating the UI, not waiting on a write.
 *   4. Open a screen recorder pointing at the browser window.
 *   5. Run: cd frontend && npx playwright test tests/e2e/demo-narrated.spec.ts \
 *              --config playwright.demo.config.ts --headed
 *   6. The browser opens, TTS narrates each step, and closes when complete.
 *      Stop the screen recorder after the browser closes.
 *
 * TTS voice: macOS "Samantha" at 175 WPM (scripts/speak.sh).
 * On non-macOS, narration is printed to stdout instead of spoken — the test
 * still completes so Linux CI runners do not error on this file.
 *
 * DO NOT include in CI test runs — requires a live stack. See demo.spec.ts
 * for the @demo tag used to filter this file from CI greps.
 *
 * ─────────────────────────────────────────────────────────────────────────────
 */

import { spawn } from "child_process";
import * as path from "path";
import { fileURLToPath } from "url";
import { test, expect } from "@playwright/test";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SPEAK_SCRIPT = path.resolve(__dirname, "../../../scripts/speak.sh");

// Async so the Node.js event loop stays live during TTS — Playwright's CDP
// keepalive must not be blocked or the browser disconnects mid-narration.
function speak(text: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const proc = spawn("bash", [SPEAK_SCRIPT, text], { stdio: "inherit" });
    proc.on("close", (code) => {
      code === 0 || code === null ? resolve() : reject(new Error(`speak.sh exited ${code}`));
    });
    proc.on("error", reject);
  });
}

const RUN_ID = Math.random().toString(36).slice(2, 8);
const DEMO_SCENARIO_NAME = `Greece 2010-2012 Demo — ${new Date().toISOString().slice(0, 10)}-${RUN_ID}`;
const COMPARE_SCENARIO_NAME = `Greece Alternative — ${new Date().toISOString().slice(0, 10)}-${RUN_ID}`;

test(
  "Stakeholder demo walkthrough — narrated screen recording",
  { tag: ["@demo"] },
  async ({ page }) => {
    // TTS narration adds ~4 minutes of blocking speech on top of interactions.
    // Override the 60 s config timeout for this test only.
    test.setTimeout(15 * 60 * 1000);

    // ── STEP 1: Map loads ────────────────────────────────────────────────────

    await page.goto("/");

    await page.waitForFunction(
      () =>
        typeof (window as Record<string, unknown>).__worldsim_selectEntity ===
        "function",
      { timeout: 15_000 },
    );

    await speak(
      "This is the application's baseline view. The choropleth shows a simulation " +
      "attribute across entities — in this case, GDP growth rate from the most recent " +
      "completed scenario step. Each country is colored by its simulated value. " +
      "Click any country to open its analysis panel. " +
      "What makes this different from a data visualization tool will become clear in a moment.",
    );

    // ── STEP 2: Open scenario panel ──────────────────────────────────────────

    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(800);

    await speak(
      "We're going to model Greece's 2010 to 2012 fiscal adjustment programme. " +
      "This is a historical case — we know what happened. In the simulation, we " +
      "inject the IMF programme conditions as scheduled inputs: the fiscal tightening, " +
      "the emergency declarations, the structural conditionality. Then we advance the " +
      "scenario step by step and observe what the model produces. " +
      "The reason we're starting with a historical case rather than a hypothetical " +
      "is important. It's the point of the backtesting discipline, which we'll come back to.",
    );

    // ── STEP 3: Create and select the Greece scenario ────────────────────────

    await page.locator('input[placeholder="Scenario name"]').fill(DEMO_SCENARIO_NAME);
    await page.locator(".scenario-btn--create").click();

    const scenarioRow = page
      .locator(".scenario-row")
      .filter({ hasText: DEMO_SCENARIO_NAME });
    await expect(scenarioRow).toBeVisible({ timeout: 20_000 });

    await scenarioRow.getByTitle("Select as primary scenario").click();
    await page.waitForTimeout(600);

    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(600);

    const nextStepBtn = page.getByRole("button", { name: /Next Step/ });
    await expect(nextStepBtn).toBeVisible({ timeout: 10_000 });

    await speak(
      "The scenario is now the active primary scenario. The step counter shows " +
      "zero of three steps completed. Each step corresponds to one programme year: " +
      "2010, 2011, 2012.",
    );

    // ── STEP 4: Advance to Step 1 ────────────────────────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 1 / 3")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Step 1. Year 2010. The simulation applies the first year of fiscal tightening. " +
      "Watch the choropleth — Greece shifts as the contraction propagates through the " +
      "model's relationship graph.",
    );

    // ── STEP 5: Advance to Step 2 ────────────────────────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 2 / 3")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Step 2. Year 2011. The fiscal contraction compounds. In the historical case, " +
      "Greece's GDP contracted negative 9.1 percent this year — deeper than 2010.",
    );

    // ── STEP 6: Advance to Step 3 ────────────────────────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 3 / 3")).toBeVisible({ timeout: 20_000 });
    await expect(page.getByText(/Complete/)).toBeVisible({ timeout: 10_000 });
    await expect(nextStepBtn).toBeDisabled();
    await page.waitForTimeout(1_200);

    await speak(
      "Step 3. Year 2012. Programme complete. Three years of fiscal adjustment, " +
      "modeled across the full programme horizon. Now let's look inside.",
    );

    // ── STEP 7: Open entity drawer for Greece ────────────────────────────────

    await page.evaluate(() => {
      (window as Record<string, (id: string) => void>).__worldsim_selectEntity(
        "GRC",
      );
    });

    await expect(page.getByLabel("Close drawer")).toBeVisible({ timeout: 20_000 });
    await expect(page.getByText("Greece", { exact: true })).toBeVisible({ timeout: 10_000 });
    await expect(
      page.getByText("Advance the scenario at least one step to view measurement output."),
    ).not.toBeVisible();

    await expect(page.getByText("Multi-Framework Overview")).toBeVisible({
      timeout: 10_000,
    });

    await page.waitForTimeout(1_500);

    await speak(
      "This panel is the primary analytical surface. What I want to draw your attention " +
      "to first is the top of the panel. These are the Minimum Descent Altitude alerts. " +
      "The terminology comes from aviation: an MDA is the altitude below which an aircraft " +
      "cannot safely descend given the terrain. In this simulation, MDAs are human cost " +
      "floors — levels below which consequences become irreversible, or where standard " +
      "policy frameworks no longer provide protection. " +
      "The alert fires when the simulation determines that an indicator has crossed one of " +
      "those floors. What you are reading is not a warning about the model's own uncertainty. " +
      "It is a finding about where the proposed path takes the population.",
    );

    // ── STEP 8: MDA alert panel called out ───────────────────────────────────

    const mdaSection = page.getByText(
      /MDA Threshold Breaches|No active MDA threshold breaches/,
    );
    await expect(mdaSection).toBeVisible({ timeout: 10_000 });

    await page.waitForTimeout(2_000);

    await speak(
      "Read this alert as a piece of evidence: Under this fiscal adjustment path, " +
      "this indicator crosses the critical threshold at programme year 3. " +
      "That sentence is specific enough to cite in a negotiation. It names an indicator, " +
      "a step, a severity level, and a population cohort. " +
      "The finance ministry specialist is not being alarmed by the simulation. " +
      "She is being handed a finding she can use.",
    );

    // ── STEP 9: Radar chart called out ───────────────────────────────────────

    await expect(page.getByText("Multi-Framework Overview")).toBeVisible();

    await page.evaluate(() => {
      const drawer = document.querySelector('[aria-label="Close drawer"]')
        ?.closest('div[style*="position: absolute"]');
      if (drawer) drawer.scrollTop = 0;
    });

    await page.waitForTimeout(1_500);

    await speak(
      "Below the alert panel is the radar chart — four axes, one for each measurement " +
      "framework the simulation tracks. Financial indicators: fiscal balance, GDP trajectory. " +
      "Human development: poverty headcount, health system capacity. " +
      "Ecological: currently null — that module ships in Milestone 8. " +
      "Governance: institutional quality indicators, now live as of this milestone. " +
      "The radar chart tells you which dimensions are under stress, supporting the " +
      "threshold scan the alert panel just completed. " +
      "I will be honest about what is not on the screen yet: the ecological and governance " +
      "axes are showing preliminary values. They will show composite scores in Milestone 8.",
    );

    // ── STEP 10: Enter compare mode ──────────────────────────────────────────

    await page.getByLabel("Close drawer").click();
    await page.waitForTimeout(600);

    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(600);

    await page.locator('input[placeholder="Scenario name"]').fill(COMPARE_SCENARIO_NAME);
    await page.locator(".scenario-btn--create").click();

    const compareRow = page
      .locator(".scenario-row")
      .filter({ hasText: COMPARE_SCENARIO_NAME });
    await expect(compareRow).toBeVisible({ timeout: 20_000 });

    await compareRow.getByTitle("Select as comparison scenario").click();
    await page.waitForTimeout(600);

    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(600);

    await page.getByText("Compare scenarios").click();
    await page.waitForTimeout(800);

    await page.waitForTimeout(1_500);

    await speak(
      "This is the counter-proposal function. Once you have identified which terms produce " +
      "threshold crossings, you model an alternative — the same fiscal outcome, achieved " +
      "differently. The DeltaChoropleth shows you, geographically, where the two scenarios " +
      "diverge. The argument becomes: This path crosses the threshold. This alternative " +
      "achieves the same primary fiscal objective and does not. Here is the evidence for both.",
    );

    // ── Demo complete ────────────────────────────────────────────────────────
    // Section 3 (backtesting), Section 4 (roadmap), and Section 5 (North Star)
    // are delivered verbally or via slides. See docs/demo/stakeholder-walkthrough.md.
  },
);
