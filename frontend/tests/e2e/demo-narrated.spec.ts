/**
 * WorldSim Stakeholder Demo — Screen-Recorded Narrated Walkthrough (M8)
 *
 * M8 update: Greece 2010–2015, six steps. EcologicalModule live (CO2
 * boundary proximity). Governance axis: dashed null, labeled "in validation".
 * Five screenshots captured per UX Agent brief (Issue #233):
 *   frame-a-step1-instrument.png  — Step 1, full Zone 1, thesis setup
 *   frame-b-step3-collapse.png    — Step 3, Financial tab, max stress
 *   frame-c-step5-divergence.png  — Step 5, HD tab, THESIS FRAME
 *   frame-d-step3-evidence.png    — Step 3, MDA alert panel prominent
 *   frame-e-step3-ecological.png  — Step 3, Ecological tab + note expanded
 *
 * ── RECORDING MODE ───────────────────────────────────────────────────────────
 *
 * Before recording:
 *   1. Start the full stack: docker compose up (or ./scripts/demo.sh --up)
 *   2. Ensure Natural Earth seed data is loaded.
 *   3. Open a screen recorder pointing at the browser window.
 *   4. Run: cd frontend && npx playwright test tests/e2e/demo-narrated.spec.ts \
 *              --config playwright.demo.config.ts --headed
 *   5. The browser opens, TTS narrates each step, and closes when complete.
 *      Stop the screen recorder after the browser closes.
 *
 * TTS voice: macOS "Zoe (Enhanced)" at 175 WPM (scripts/speak.sh).
 * On non-macOS, narration is printed to stdout instead of spoken.
 *
 * DO NOT include in CI test runs — requires a live stack.
 *
 * M6 archive: demo-narrated-m6.spec.ts
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

// Ensure screenshot directory exists (created by PR #334; guard against clean clones).
fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });

function speak(text: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const proc = spawn("bash", [SPEAK_SCRIPT, text], { stdio: "inherit" });
    proc.on("close", (code) => {
      if (code === 0 || code === null) { resolve(); } else { reject(new Error(`speak.sh exited ${code}`)); }
    });
    proc.on("error", reject);
  });
}

function screenshotPath(filename: string): string {
  return path.resolve(SCREENSHOT_DIR, filename);
}

const RUN_ID = Math.random().toString(36).slice(2, 8);
const DEMO_SCENARIO_NAME = `Greece 2010-2015 M8 Demo — ${new Date().toISOString().slice(0, 10)}-${RUN_ID}`;
const COMPARE_SCENARIO_NAME = `Greece Alternative — ${new Date().toISOString().slice(0, 10)}-${RUN_ID}`;

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
      (s.name.startsWith("Greece 2010-2015 M8 Demo") ||
        s.name.startsWith("Greece 2010-2012 Demo") ||
        s.name.startsWith("Greece Alternative")) &&
      s.name !== DEMO_SCENARIO_NAME &&
      s.name !== COMPARE_SCENARIO_NAME,
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
  "Stakeholder demo walkthrough — narrated screen recording (M8)",
  { tag: ["@demo"] },
  async ({ page }) => {
    test.setTimeout(20 * 60 * 1000);

    // Match legibility gate and live demo viewport — NM-032 / Issue #675.
    // Do NOT rely on playwright.config.ts default (1280×720).
    await page.setViewportSize({ width: 1440, height: 900 });

    // ── STEP 1: Map loads ────────────────────────────────────────────────────

    await page.goto("/");

    await page.waitForFunction(
      () =>
        typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function" &&
        typeof (window as Record<string, unknown>).__worldsim_setAttributeName === "function",
      { timeout: 15_000 },
    );

    // Create the M8 Greece demo scenario via API before opening the panel.
    // Matches build_greece_demo_scenario(): 6 steps, EcologicalModule enabled,
    // CO2 seed (388.0 ppm NOAA MLO 2010), all eight programme scheduled inputs.
    const createRes = await page.request.post("http://localhost:8000/api/v1/scenarios", {
      data: {
        name: DEMO_SCENARIO_NAME,
        description: "Greece 2010-2015 IMF Program — M8 stakeholder demo run",
        configuration: {
          entities: ["GRC"],
          n_steps: 6,
          timestep_label: "annual",
          start_date: "2010-01-01",
          modules_config: { ecological: { enabled: true } },
          initial_attributes: {
            GRC: {
              gdp_growth: {
                value: "-0.054", unit: "ratio", variable_type: "ratio",
                confidence_tier: 3, observation_date: "2010-04-01",
                source_registry_id: "IMF_WEO_APR2010", measurement_framework: "financial",
              },
              unemployment_rate: {
                value: "0.127", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2010-07-01",
                source_registry_id: "EUROSTAT_LFS_2010", measurement_framework: "human_development",
              },
              health_expenditure_pct_gdp: {
                value: "0.095", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2011-12-01",
                source_registry_id: "WDI_2010", measurement_framework: "human_development",
              },
              net_enrollment_secondary: {
                value: "0.991", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2011-12-01",
                source_registry_id: "WDI_2010", measurement_framework: "human_development",
              },
              reserve_coverage_months: {
                value: "2.0", unit: "months", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2010-05-01",
                source_registry_id: "IMF_CR10_110", measurement_framework: "financial",
              },
              co2_concentration_ppm: {
                value: "388.0", unit: "ppm", variable_type: "stock",
                confidence_tier: 1, observation_date: "2010-01-01",
                source_registry_id: "NOAA_MLO_2010", measurement_framework: "ecological",
              },
            },
          },
        },
        scheduled_inputs: [
          { step: 1, input_type: "EmergencyPolicyInput",
            input_data: { instrument: "imf_program_acceptance", target_entity: "GRC", expected_duration: 3, program_size_gdp_ratio: "0.48" } },
          { step: 1, input_type: "FiscalPolicyInput",
            input_data: { instrument: "spending_change", target_entity: "GRC", sector: "government", value: "-0.08", duration_years: 1 } },
          { step: 2, input_type: "FiscalPolicyInput",
            input_data: { instrument: "spending_change", target_entity: "GRC", sector: "government", value: "-0.05", duration_years: 1 } },
          { step: 2, input_type: "FiscalPolicyInput",
            input_data: { instrument: "deficit_target", target_entity: "GRC", sector: "", value: "-0.03", duration_years: 4 } },
          { step: 3, input_type: "FiscalPolicyInput",
            input_data: { instrument: "spending_change", target_entity: "GRC", sector: "government", value: "-0.04", duration_years: 1 } },
          { step: 4, input_type: "FiscalPolicyInput",
            input_data: { instrument: "spending_change", target_entity: "GRC", sector: "government", value: "-0.02", duration_years: 1 } },
          { step: 4, input_type: "FiscalPolicyInput",
            input_data: { instrument: "deficit_target", target_entity: "GRC", sector: "", value: "0.015", duration_years: 2 } },
          { step: 5, input_type: "StructuralPolicyInput",
            input_data: { instrument: "privatization", target_entity: "GRC", affected_sector: "public_assets", implementation_years: 3 } },
          { step: 6, input_type: "EmergencyPolicyInput",
            input_data: { instrument: "capital_controls", target_entity: "GRC", expected_duration: 2 } },
        ],
      },
    });
    if (!createRes.ok()) {
      throw new Error(`Greece M8 scenario creation failed: ${createRes.status()} — ${await createRes.text()}`);
    }

    await speak(
      "This is the application's baseline view. The choropleth shows a simulation " +
      "attribute across entities — GDP growth rate from the most recent completed " +
      "scenario step. Click any country to open its analysis panel. " +
      "What makes this different from a data visualization tool will become clear in a moment.",
    );

    // ── STEP 2: Open scenario panel ──────────────────────────────────────────

    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(800);

    await speak(
      "We're going to model Greece's 2010 to 2015 fiscal adjustment programme — " +
      "six years, from the IMF programme entry through the capital controls episode. " +
      "This is a historical case. We inject the programme conditions as scheduled inputs: " +
      "the fiscal tightening, the emergency declarations, the structural conditionality. " +
      "Then we advance step by step and observe what the model produces.",
    );

    // ── STEP 3: Select the pre-created M8 Greece scenario ───────────────────

    const scenarioRow = page.locator(".scenario-row").filter({ hasText: DEMO_SCENARIO_NAME });
    await expect(scenarioRow).toBeVisible({ timeout: 10_000 });
    await scenarioRow.getByTitle("Select as primary scenario").click();
    await page.waitForTimeout(1500);
    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(600);

    const nextStepBtn = page.getByRole("button", { name: /Next Step/ });
    await expect(nextStepBtn).toBeVisible({ timeout: 10_000 });

    await speak(
      "The scenario is active. The step counter shows zero of six steps completed. " +
      "Each step is one programme year: 2010 through 2015.",
    );

    // ── STEP 4: Advance to Step 1 — Frame A ─────────────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 1 / 6")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    // Switch choropleth to gdp_growth now that step 1 output exists.
    await page.evaluate(() => {
      (window as Record<string, (key: string) => void>).__worldsim_setAttributeName("gdp_growth");
    });

    await speak(
      "Step 1. Year 2010. The IMF programme begins — fiscal tightening applied. " +
      "Watch Greece shift in the choropleth as the contraction propagates.",
    );

    // Frame A: "The Instrument" — Step 1, all zones visible.
    await page.evaluate(() => {
      (window as Record<string, (id: string) => void>).__worldsim_selectEntity("GRC");
    });
    await expect(page.getByLabel("Close drawer")).toBeVisible({ timeout: 20_000 });
    await expect(page.getByText("Multi-Framework Overview")).toBeVisible({ timeout: 30_000 });
    await page.waitForTimeout(800); // radar animation settles (250ms + margin)
    await page.screenshot({ path: screenshotPath("frame-a-step1-instrument.png") });
    await page.getByLabel("Close drawer").click();
    await page.waitForTimeout(600);

    // ── STEP 5: Advance to Step 2 ────────────────────────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 2 / 6")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Step 2. Year 2011. The fiscal contraction compounds. In the historical case, " +
      "Greece's GDP contracted negative 8.9 percent this year.",
    );

    // ── STEP 6: Advance to Step 3 — Frames B, D, E ───────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 3 / 6")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Step 3. Year 2012. Third memorandum fiscal consolidation. Maximum stress across " +
      "the programme so far. Let's open the analysis panel.",
    );

    await page.evaluate(() => {
      (window as Record<string, (id: string) => void>).__worldsim_selectEntity("GRC");
    });
    await expect(page.getByLabel("Close drawer")).toBeVisible({ timeout: 20_000 });
    await expect(page.getByText("Multi-Framework Overview")).toBeVisible({ timeout: 30_000 });
    await page.waitForTimeout(800);

    // Frame D: "The Evidence" — MDA alert panel prominent.
    // Scroll drawer to top so alert panel fills the upper portion.
    await page.evaluate(() => {
      const panel = document.querySelector('[role="dialog"], [data-testid="entity-drawer"]') as HTMLElement | null;
      if (panel) panel.scrollTop = 0;
    });
    await page.waitForTimeout(400);
    await page.screenshot({ path: screenshotPath("frame-d-step3-evidence.png") });

    // Frame B: "The Collapse" — Financial tab active.
    const financialTab = page.getByRole("button", { name: /^Financial$/ });
    await expect(financialTab).toBeVisible({ timeout: 5_000 });
    await financialTab.click();
    await page.waitForTimeout(500);
    await page.screenshot({ path: screenshotPath("frame-b-step3-collapse.png") });

    // Frame E: "The Planetary Dimension" — Ecological tab + note expanded.
    const ecologicalTab = page.getByRole("button", { name: /^Ecological$/ });
    await expect(ecologicalTab).toBeVisible({ timeout: 5_000 });
    await ecologicalTab.click();
    await page.waitForTimeout(500);
    // Expand the ecological methodology note drawer (Zone 3A).
    const noteToggle = page.getByText(/Methodology notes|boundary.*note|ⓘ/i).first();
    const noteToggleVisible = await noteToggle.isVisible().catch(() => false);
    if (noteToggleVisible) {
      await noteToggle.click();
      await page.waitForTimeout(500);
    }
    await page.screenshot({ path: screenshotPath("frame-e-step3-ecological.png") });

    await speak(
      "This panel is the primary analytical surface. Two things to notice. " +
      "First, the top: Minimum Descent Altitude alerts — levels below which " +
      "consequences become irreversible. What you are reading is not a model warning. " +
      "It is a finding about where this path takes the population. " +
      "Second: the ecological axis. As of Milestone 8, planetary boundary proximity " +
      "is live — CO2 concentration tracked against the Rockström 2009 safe operating " +
      "space boundary. This is the first time ecological data has appeared on this radar.",
    );

    await page.getByLabel("Close drawer").click();
    await page.waitForTimeout(600);

    // ── STEP 7: Advance to Step 4 ────────────────────────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 4 / 6")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    // Open drawer at step 4: primary surplus is visible in the financial indicators.
    await page.evaluate(() => {
      (window as Record<string, (id: string) => void>).__worldsim_selectEntity("GRC");
    });
    await expect(page.getByLabel("Close drawer")).toBeVisible({ timeout: 20_000 });
    await expect(page.getByText("Multi-Framework Overview")).toBeVisible({ timeout: 30_000 });
    await page.waitForTimeout(800);

    await speak(
      "Step 4. Year 2013. Primary surplus conditionality. Greece achieves its first " +
      "primary surplus — plus 1.5 percent of GDP — but at significant human cost. " +
      "Look at the radar: financial axis is recovering. Human development remains depressed.",
    );

    await page.getByLabel("Close drawer").click();
    await page.waitForTimeout(600);

    // ── STEP 8: Advance to Step 5 — Frame C (thesis) ────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 5 / 6")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Step 5. Year 2014. This is the step that shows why WorldSim must exist.",
    );

    await page.evaluate(() => {
      (window as Record<string, (id: string) => void>).__worldsim_selectEntity("GRC");
    });
    await expect(page.getByLabel("Close drawer")).toBeVisible({ timeout: 20_000 });
    await expect(page.getByText("Multi-Framework Overview")).toBeVisible({ timeout: 30_000 });
    await page.waitForTimeout(800);

    // Frame C: "The Divergence" — HD tab active. THESIS FRAME.
    const hdTab = page.getByRole("button", { name: /Human Development/ });
    await expect(hdTab).toBeVisible({ timeout: 5_000 });
    await hdTab.click();
    await page.waitForTimeout(500);
    await page.screenshot({ path: screenshotPath("frame-c-step5-divergence.png") });

    await speak(
      "Step 5 is 2014. In the historical record, Greece's GDP grew 0.7 percent — " +
      "a financial recovery. But unemployment was still 26.5 percent. " +
      "Look at the radar: the financial axis is extending as the model registers " +
      "partial recovery. The human development axis remains near its most depressed point. " +
      "This asymmetry is the WorldSim argument in a single image. " +
      "Financial recovery and human recovery are not the same event. " +
      "No single-axis measurement tool can show you both simultaneously.",
    );

    await page.getByLabel("Close drawer").click();
    await page.waitForTimeout(600);

    // ── STEP 9: Advance to Step 6 ────────────────────────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 6 / 6")).toBeVisible({ timeout: 20_000 });
    await expect(page.getByText(/Complete/)).toBeVisible({ timeout: 10_000 });
    await expect(nextStepBtn).toBeDisabled();
    await page.waitForTimeout(1_200);

    await speak(
      "Step 6. Year 2015. Capital controls imposed, June 26th. Programme ends. " +
      "Six years, fully modeled.",
    );

    // ── STEP 10: Open drawer for MDA + radar narration ───────────────────────

    await page.evaluate(() => {
      (window as Record<string, (id: string) => void>).__worldsim_selectEntity("GRC");
    });
    await expect(page.getByLabel("Close drawer")).toBeVisible({ timeout: 20_000 });
    await expect(page.getByText("Multi-Framework Overview")).toBeVisible({ timeout: 30_000 });
    await page.waitForTimeout(1_500);

    await speak(
      "This is the primary analytical surface. The MDA alert panel at the top. " +
      "These are the Minimum Descent Altitude alerts — " +
      "aviation's term for levels below which an aircraft cannot safely descend given the terrain. " +
      "In this simulation, MDAs are human cost floors. Read each alert as a piece of " +
      "evidence: indicator, step, severity, cohort. That sentence is specific enough to " +
      "cite in a negotiation.",
    );

    const mdaSection = page.getByRole("heading", { name: "MDA Threshold Breaches" });
    await expect(mdaSection).toBeVisible({ timeout: 10_000 });
    await page.waitForTimeout(2_000);

    await speak(
      "The radar chart below. Four axes: financial, human development, ecological, governance. " +
      "Financial and human development are live. " +
      "Ecological is live as of Milestone 8 — CO2 planetary boundary proximity, " +
      "boundary-normalized against 350 parts per million. " +
      "Governance shows as a dashed axis, labeled 'Governance — in validation.' " +
      "It renders honest null — not zero. " +
      "Zero would imply governance failure. Null means the composite is not yet computed. " +
      "The fourth axis will show scores when the GovernanceModule promotion criteria are met at M9.",
    );

    // ── STEP 11: Enter compare mode ──────────────────────────────────────────

    await page.getByLabel("Close drawer").click();
    await page.waitForTimeout(600);

    // Comparison scenario: same 6-step span, same initial state, lighter fiscal path.
    // Half the spending cuts — demonstrates that the fiscal target can be approached
    // without crossing the MDA threshold. Must be n_steps: 6 to match the primary
    // so the DeltaChoropleth has data at currentStep (6).
    const compareCreateRes = await page.request.post("http://localhost:8000/api/v1/scenarios", {
      data: {
        name: COMPARE_SCENARIO_NAME,
        description: "Greece Alternative — lighter austerity path, M8 stakeholder demo",
        configuration: {
          entities: ["GRC"],
          n_steps: 6,
          timestep_label: "annual",
          start_date: "2010-01-01",
          modules_config: { ecological: { enabled: true } },
          initial_attributes: {
            GRC: {
              gdp_growth: {
                value: "-0.054", unit: "ratio", variable_type: "ratio",
                confidence_tier: 3, observation_date: "2010-04-01",
                source_registry_id: "IMF_WEO_APR2010", measurement_framework: "financial",
              },
              unemployment_rate: {
                value: "0.127", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2010-07-01",
                source_registry_id: "EUROSTAT_LFS_2010", measurement_framework: "human_development",
              },
              reserve_coverage_months: {
                value: "2.0", unit: "months", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2010-05-01",
                source_registry_id: "IMF_CR10_110", measurement_framework: "financial",
              },
              co2_concentration_ppm: {
                value: "388.0", unit: "ppm", variable_type: "stock",
                confidence_tier: 1, observation_date: "2010-01-01",
                source_registry_id: "NOAA_MLO_2010", measurement_framework: "ecological",
              },
            },
          },
        },
        scheduled_inputs: [
          { step: 1, input_type: "FiscalPolicyInput",
            input_data: { instrument: "spending_change", target_entity: "GRC", sector: "government", value: "-0.04", duration_years: 1 } },
          { step: 2, input_type: "FiscalPolicyInput",
            input_data: { instrument: "spending_change", target_entity: "GRC", sector: "government", value: "-0.025", duration_years: 1 } },
          { step: 3, input_type: "FiscalPolicyInput",
            input_data: { instrument: "spending_change", target_entity: "GRC", sector: "government", value: "-0.02", duration_years: 1 } },
        ],
      },
    });
    if (!compareCreateRes.ok()) {
      throw new Error(`Compare scenario creation failed: ${compareCreateRes.status()} — ${await compareCreateRes.text()}`);
    }
    const { scenario_id: compareScenarioId } = await compareCreateRes.json() as { scenario_id: string };

    // Run comparison scenario to completion via API.
    const runRes = await page.request.post(
      `http://localhost:8000/api/v1/scenarios/${encodeURIComponent(compareScenarioId)}/run`,
    );
    if (!runRes.ok()) {
      throw new Error(`Comparison run failed: ${runRes.status()} — ${await runRes.text()}`);
    }

    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(600);

    const compareRow = page.locator(".scenario-row").filter({ hasText: COMPARE_SCENARIO_NAME });
    await expect(compareRow).toBeVisible({ timeout: 10_000 });
    await compareRow.getByTitle("Select as comparison scenario").click();
    await page.waitForTimeout(600);

    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(600);

    await page.getByText("Compare scenarios").click();
    // Wait for DeltaChoropleth to fetch and render both scenarios at step 6.
    await page.waitForTimeout(3_000);

    await speak(
      "This is the counter-proposal function. You have identified which terms produce " +
      "threshold crossings. Now you model an alternative — the same fiscal outcome, " +
      "achieved differently. The DeltaChoropleth shows, geographically, where the two " +
      "scenarios diverge. The argument becomes: this path crosses the threshold; " +
      "this alternative achieves the same fiscal objective and does not. " +
      "Here is the evidence for both.",
    );

    // Sections 3–5 (backtesting, roadmap, North Star) delivered verbally.
    // See docs/demo/m8/stakeholder-walkthrough.md.
  },
);
