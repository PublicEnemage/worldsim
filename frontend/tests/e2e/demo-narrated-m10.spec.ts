/**
 * WorldSim Stakeholder Demo — Screen-Recorded Narrated Walkthrough (M10)
 *
 * Demo 3: Argentina 2001–2004 crisis arc — four steps. All four Zone 1 axes live.
 * GovernanceModule promoted (not dashed). PMM live. EcologicalModule live.
 * Platform Principle: same engine as Greece (Demo 1/2), different crisis arc.
 *
 * Five screenshots captured per UX Agent brief (docs/demo/m10/screenshot-brief.md):
 *   frame-a-step1-instrument.png  — Step 1, Zone 1 baseline (all four instruments)
 *   frame-b-step2-crisis.png      — Step 2, default/devaluation inflection
 *   frame-c-step3-divergence.png  — Step 3, THESIS FRAME: financial rising, governance flat
 *   frame-d-step3-evidence.png    — Step 3, Zone 1B MDA governance WARNING
 *   frame-e-step4-recovery.png    — Step 4, Zone 1D four-framework recovery arc
 *
 * ── RECORDING MODE ───────────────────────────────────────────────────────────
 *
 * Before recording:
 *   1. Start the full stack: docker compose up (or ./scripts/demo.sh --up)
 *   2. Ensure Natural Earth seed data is loaded.
 *   3. Ensure IR-M10-002 fix is deployed (ecological "(1.0 = boundary)" annotation).
 *   4. Open a screen recorder pointing at the browser window.
 *   5. Run: cd frontend && npx playwright test tests/e2e/demo-narrated-m10.spec.ts \
 *              --config playwright.demo.config.ts --headed
 *   6. The browser opens, TTS narrates each step, and closes when complete.
 *      Stop the screen recorder after the browser closes.
 *
 * TTS voice: macOS "Zoe (Enhanced)" at 175 WPM (scripts/speak.sh).
 * On non-macOS, narration is printed to stdout instead of spoken.
 *
 * DO NOT include in CI test runs — requires a live stack.
 *
 * M8 archive: demo-narrated-m8.spec.ts
 * ─────────────────────────────────────────────────────────────────────────────
 */

import { spawn } from "child_process";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";
import { test, expect } from "@playwright/test";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SPEAK_SCRIPT = path.resolve(__dirname, "../../../scripts/speak.sh");
const SCREENSHOT_DIR = path.resolve(__dirname, "../../../docs/demo/m10/screenshots/");

fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });

function speak(text: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const proc = spawn("bash", [SPEAK_SCRIPT, text], { stdio: "inherit" });
    proc.on("close", (code) => {
      code === 0 || code === null ? resolve() : reject(new Error(`speak.sh exited ${code}`));
    });
    proc.on("error", reject);
  });
}

function screenshotPath(filename: string): string {
  return path.resolve(SCREENSHOT_DIR, filename);
}

const RUN_ID = Math.random().toString(36).slice(2, 8);
const DEMO_SCENARIO_NAME = `Argentina 2001-2002 Demo 3 — ${new Date().toISOString().slice(0, 10)}-${RUN_ID}`;

// ── Pre-demo cleanup ─────────────────────────────────────────────────────────

test.beforeAll(async () => {
  const API = "http://localhost:8000/api/v1";
  let scenarios: Array<{ scenario_id: string; name: string }> = [];
  try {
    const res = await fetch(`${API}/scenarios`);
    if (res.ok) scenarios = await res.json() as typeof scenarios;
  } catch {
    return;
  }

  const stale = scenarios.filter(
    (s) =>
      s.name.startsWith("Argentina 2001-2002 Demo 3") &&
      s.name !== DEMO_SCENARIO_NAME,
  );

  await Promise.all(
    stale.map((s) =>
      fetch(`${API}/scenarios/${encodeURIComponent(s.scenario_id)}`, {
        method: "DELETE",
      }),
    ),
  );
});

test(
  "Stakeholder demo walkthrough — narrated screen recording (M10 Demo 3)",
  { tag: ["@demo"] },
  async ({ page }) => {
    test.setTimeout(20 * 60 * 1000);

    // ── STEP 1: Map loads ────────────────────────────────────────────────────

    await page.goto("/");

    await page.waitForFunction(
      () =>
        typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function" &&
        typeof (window as Record<string, unknown>).__worldsim_setAttributeName === "function",
      { timeout: 15_000 },
    );

    // Create the Argentina Demo 3 scenario via API.
    // Matches build_argentina_demo_scenario(): n_steps=4, EcologicalModule + GovernanceModule
    // enabled, all initial attributes from backend fixture, emergency_declaration at step 2.
    const createRes = await page.request.post("http://localhost:8000/api/v1/scenarios", {
      data: {
        name: DEMO_SCENARIO_NAME,
        description: "Argentina 2001-2002 Demo 3 — M10 stakeholder demo run",
        configuration: {
          entities: ["ARG"],
          n_steps: 4,
          timestep_label: "annual",
          start_date: "2000-01-01",
          modules_config: {
            ecological: { enabled: true },
            governance: { enabled: true },
          },
          initial_attributes: {
            ARG: {
              gdp_growth: {
                value: "-0.008", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2001-04-01",
                source_registry_id: "IMF_WEO_APR2001", measurement_framework: "financial",
              },
              unemployment_rate: {
                value: "0.147", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2001-01-01",
                source_registry_id: "INDEC_EPH_2000", measurement_framework: "human_development",
              },
              co2_concentration_ppm: {
                value: "369.5", unit: "ppm", variable_type: "stock",
                confidence_tier: 1, observation_date: "2000-01-01",
                source_registry_id: "NOAA_MLO_2000", measurement_framework: "ecological",
              },
              rule_of_law_percentile: {
                value: "33.2", unit: "percentile_0_100", variable_type: "stock",
                confidence_tier: 2, observation_date: "2000-01-01",
                source_registry_id: "WB_WGI_ARG_2000_RULE_OF_LAW", measurement_framework: "governance",
              },
              democratic_quality_score: {
                value: "0.71", unit: "ratio_0_1", variable_type: "stock",
                confidence_tier: 3, observation_date: "2000-01-01",
                source_registry_id: "VDEM_V13_ARG_2000_LDI", measurement_framework: "governance",
              },
            },
          },
          step_metadata: {
            "1": { significance: "SIGNIFICANT", label: "Zero Deficit Plan / Blindaje" },
            "2": { significance: "SIGNIFICANT", label: "Default / Peso devaluation" },
            "3": { significance: "SIGNIFICANT", label: "Kirchner recovery begins" },
          },
        },
        scheduled_inputs: [
          // Step 1: IMF Blindaje + Zero Deficit Plan (pro-cyclical -6.5% GDP spending cut)
          { step: 1, input_type: "EmergencyPolicyInput",
            input_data: { instrument: "imf_program_acceptance", target_entity: "ARG", expected_duration: 2, program_size_gdp_ratio: "0.16" } },
          { step: 1, input_type: "FiscalPolicyInput",
            input_data: { instrument: "spending_change", target_entity: "ARG", sector: "government", value: "-0.065", duration_years: 1 } },
          // Step 2: Sovereign default declaration + emergency declaration (state of siege)
          { step: 2, input_type: "EmergencyPolicyInput",
            input_data: { instrument: "default_declaration", target_entity: "ARG", expected_duration: 1 } },
          { step: 2, input_type: "EmergencyPolicyInput",
            input_data: { instrument: "emergency_declaration", target_entity: "ARG", expected_duration: 1 } },
        ],
      },
    });
    if (!createRes.ok()) {
      throw new Error(`Argentina Demo 3 scenario creation failed: ${createRes.status()} — ${await createRes.text()}`);
    }

    await speak(
      "This is the application's baseline view. The map provides geographic context — " +
      "each country is visible as a reference point. The analytical instrument is the " +
      "panel on the left: four instruments, always visible, updated with each step. " +
      "What makes this different from a data visualization tool will become clear in a moment.",
    );

    // ── STEP 2: Open scenario panel and select Demo 3 ────────────────────────

    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(800);

    await speak(
      "We are going to model Argentina's 2001 to 2002 sovereign default — " +
      "four steps, annual, from the Zero Deficit Plan through the Kirchner recovery. " +
      "This is a historical case: we know what happened. The backtesting discipline " +
      "is how we validate that the simulation captures real causal dynamics. " +
      "The conditionality terms are the inputs. The simulation produces the consequences.",
    );

    const scenarioRow = page.locator(".scenario-row").filter({ hasText: DEMO_SCENARIO_NAME });
    await expect(scenarioRow).toBeVisible({ timeout: 10_000 });
    await scenarioRow.getByTitle("Select as primary scenario").click();
    await page.waitForTimeout(1500);
    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(600);

    const nextStepBtn = page.getByRole("button", { name: /Next Step/ });
    await expect(nextStepBtn).toBeVisible({ timeout: 10_000 });

    await speak(
      "The Argentina scenario is active. Four steps: 2001 through 2004. " +
      "Each step is one year. The step counter shows zero of four steps completed.",
    );

    // ── STEP 3: Advance to Step 1 — Frame A ─────────────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 1 / 4")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    // Frame A: "The Instrument" — Step 1, all Zone 1 instruments loaded.
    // Capture primary viewport: Zone 1A (trajectory), Zone 1B (MDA), Zone 1C (PMM), Zone 1D.
    await page.screenshot({ path: screenshotPath("frame-a-step1-instrument.png") });

    await speak(
      "Step 1. Year 2001. The IMF Blindaje programme is active. " +
      "The Zero Deficit Plan — a pro-cyclical spending cut of 6.5 percent of GDP — " +
      "has been applied. All four Zone 1 instruments are live. " +
      "The trajectory view shows the initial arc beginning. " +
      "Ecological composite: 1.07 — Argentina is already 7 percent beyond the " +
      "CO2 planetary boundary at programme entry. " +
      "Governance composite: 0.71 — a functioning democracy, but under institutional stress.",
    );

    // ── STEP 4: Advance to Step 2 — Frame B ─────────────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 2 / 4")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    // Frame B: "The Crisis" — Step 2, default/devaluation inflection.
    await page.screenshot({ path: screenshotPath("frame-b-step2-crisis.png") });

    await speak(
      "Step 2. Year 2002. Sovereign default declared — December 2001, " +
      "81.8 billion US dollars, the largest sovereign default in history at the time. " +
      "Peso devaluation ends the convertibility era. " +
      "Watch the trajectory view: the inflection at step 2 is the deepest point " +
      "of the crisis arc. The simulated GDP contraction at this step is " +
      "negative 10.55 percent. The historical outturn was negative 10.9 percent. " +
      "That is a 3.2 percent deviation — within the validated magnitude band. " +
      "Argentina 2002 is the first MAGNITUDE-validated result in WorldSim backtesting.",
    );

    // ── STEP 5: Advance to Step 3 — Frames C and D (thesis) ─────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 3 / 4")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Step 3. Year 2003. This is the step that shows why WorldSim must exist.",
    );

    // Frame C: "The Divergence" — THESIS FRAME.
    // Zone 1A: financial curve rising (Kirchner recovery) vs governance curve flat/declining.
    // Zone 1B: governance WARNING visible.
    // Zone 1D: governance score below 0.70 floor despite financial rebound.
    await page.screenshot({ path: screenshotPath("frame-c-step3-divergence.png") });

    await speak(
      "Step 3 is 2003 — the Kirchner recovery begins. " +
      "Look at the trajectory view: the financial curve is rising from the step 2 trough. " +
      "Now look at the governance curve: it is flat. Still in the breach zone. " +
      "The emergency declaration from December 2001 — the state of siege that ran " +
      "concurrent with the default — drove democratic quality below the MDA floor. " +
      "That institutional damage does not repair itself as fast as GDP recovers. " +
      "Financial recovery and institutional recovery are not the same event. " +
      "No single-axis measurement tool can show you both simultaneously. This one does.",
    );

    // Frame D: "The Evidence" — Zone 1B MDA governance WARNING.
    // Ensure Zone 1B is the dominant visual — scroll if needed.
    await page.evaluate(() => {
      const zone1b = document.querySelector('[data-testid="mda-alert-panel"]') as HTMLElement | null;
      if (zone1b) zone1b.scrollIntoView({ behavior: "instant", block: "start" });
    });
    await page.waitForTimeout(400);
    await page.screenshot({ path: screenshotPath("frame-d-step3-evidence.png") });

    await speak(
      "This is a Minimum Descent Altitude alert — the instrument that makes the finding citeable. " +
      "MDA governance democracy floor: democratic quality score has dropped to 0.665 — " +
      "below the threshold of 0.70, which is the level below which institutions " +
      "lose their protective function. " +
      "Step 3. Governance framework. " +
      "Read that sentence as evidence you can cite in a negotiation: " +
      "indicator, threshold, step, framework. That is specific enough to use.",
    );

    // ── STEP 6: Advance to Step 4 — Frame E ─────────────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 4 / 4")).toBeVisible({ timeout: 20_000 });
    await expect(page.getByText(/Complete/)).toBeVisible({ timeout: 10_000 });
    await expect(nextStepBtn).toBeDisabled();
    await page.waitForTimeout(1_200);

    // Frame E: "Recovery Without Restoration" — Step 4, Zone 1D four-framework current position.
    // Shows the full arc: financial recovering, governance healing slowly.
    await page.screenshot({ path: screenshotPath("frame-e-step4-recovery.png") });

    await speak(
      "Step 4. Year 2004. GDP is growing at plus 9 percent — the Kirchner heterodox " +
      "recovery is entrenched. " +
      "Look at Zone 1D: four frameworks, four measurements. Ecological and governance " +
      "are live composite scores. Financial and human development composites are deferred — " +
      "the percentile-rank scoring strategy requires at least two entities for comparison. " +
      "That is disclosed in the interface, not hidden. " +
      "The governance arc is healing, but slowly. Institutional recovery lags financial recovery. " +
      "This is the platform principle made concrete: " +
      "the same engine, the same instruments, the same analytical discipline " +
      "that ran Greece 2010 to 2015 now runs Argentina 2001 to 2004. " +
      "Different crisis arc, different geopolitical context, same tool.",
    );

    await speak(
      "Sections on backtesting credibility, roadmap, and the North Star " +
      "are delivered verbally — see docs/demo/stakeholder-walkthrough.md.",
    );
  },
);
