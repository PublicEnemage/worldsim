/**
 * WorldSim Stakeholder Demo — Screen-Recorded Narrated Walkthrough (M12)
 *
 * Demo 4: Jordan + Egypt, Strait of Hormuz 2024–2031.
 * Eight steps. Two entities. ExternalSectorModule live (ADR-012).
 * All four composite scores live simultaneously (first time in Demo history).
 * Mode 3 Active Control: branch from step 3, fiscal_multiplier=1.30.
 * Two-act structure: Act 1 (baseline reveals consequence) + Act 2 (counter-proposal).
 *
 * Five screenshots per UX Agent brief (docs/demo/m12/screenshot-brief.md):
 *   frame-a-instrument-cluster.png   — Step 1, Zone 1 loaded, all four axes seeded
 *   frame-b-terminal-alerts.png      — Step 2, Zone 1B: Egypt CRITICAL governance alert
 *   frame-c-mena-choropleth.png      — Step 3, thesis frame: two entities, two alert states
 *   frame-d-mode3-active-control.png — Step 3 + Mode 3: branch anchor visible, 1.30× applied
 *   frame-e-step5-divergence.png     — Step 5, all four composite axes in baseline + branch
 *
 * ── RECORDING MODE ───────────────────────────────────────────────────────────
 *
 * Before recording:
 *   1. Start the full stack: docker compose up (or ./scripts/demo.sh)
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
 * M8 archive: demo-narrated-m8.spec.ts
 * M10 archive: demo-narrated-m10.spec.ts
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
const SCREENSHOT_DIR = path.resolve(__dirname, "../../../docs/demo/m12/screenshots/");

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
const DEMO_SCENARIO_NAME = `Jordan/Egypt 2024 Hormuz Demo 4 — ${new Date().toISOString().slice(0, 10)}-${RUN_ID}`;

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
      s.name.startsWith("Jordan/Egypt 2024 Hormuz Demo 4") &&
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
  "Stakeholder demo walkthrough — narrated screen recording (M12)",
  { tag: ["@demo"] },
  async ({ page }) => {
    test.setTimeout(25 * 60 * 1000);

    // Match legibility gate and live demo viewport — NM-032 / Issue #675.
    // Do NOT rely on playwright.config.ts default (1280×720).
    await page.setViewportSize({ width: 1440, height: 900 });

    // ── STEP 1: Map loads ────────────────────────────────────────────────────

    await page.goto("/");

    // Wait for the application shell to be interactive — same sentinel used
    // by demo-legibility.spec.ts and demo-advancement-flow.spec.ts.
    await page.waitForFunction(
      () => typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
      { timeout: 15_000 },
    );

    // Create the M12 Jordan/Egypt Hormuz demo scenario via API.
    // Matches jordan_hormuz_scenario.py fixture: 8 steps, ExternalSectorModule
    // commodity shocks, GovernanceModule enabled, initial attributes from
    // AMDB/WDI/WGI/V-Dem 2024 observation vintage.
    const createRes = await page.request.post("http://localhost:8000/api/v1/scenarios", {
      data: {
        name: DEMO_SCENARIO_NAME,
        description: "Jordan/Egypt Hormuz disruption — M12 stakeholder demo run",
        configuration: {
          entities: ["JOR", "EGY"],
          n_steps: 8,
          timestep_label: "annual",
          start_date: "2024-01-01",
          modules_config: {
            ecological: { enabled: true },
            governance: { enabled: true },
          },
          commodity_price_shocks: [
            { commodity_category: "fuel", magnitude: "0.25", start_step: 1, duration_steps: 6 },
            { commodity_category: "food", magnitude: "0.15", start_step: 2, duration_steps: 5 },
          ],
          initial_attributes: {
            JOR: {
              gdp_growth: {
                value: "0.025", unit: "ratio", variable_type: "ratio",
                confidence_tier: 3, observation_date: "2024-04-01",
                source_registry_id: "IMF_WEO_APR2024", measurement_framework: "financial",
              },
              unemployment_rate: {
                value: "0.178", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-07-01",
                source_registry_id: "ILO_2024", measurement_framework: "human_development",
              },
              health_expenditure_pct_gdp: {
                value: "0.078", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-12-01",
                source_registry_id: "WDI_2024", measurement_framework: "human_development",
              },
              net_enrollment_secondary: {
                value: "0.830", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-12-01",
                source_registry_id: "WDI_2024", measurement_framework: "human_development",
              },
              reserve_coverage_months: {
                value: "7.1", unit: "months", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-05-01",
                source_registry_id: "IMF_CR2024_JOR", measurement_framework: "financial",
              },
              trend_growth: {
                value: "0.030", unit: "ratio", variable_type: "ratio",
                confidence_tier: 3, observation_date: "2024-01-01",
                source_registry_id: "IMF_WEO_APR2024", measurement_framework: "financial",
              },
              commodity_import_dependency_fuel: {
                value: "0.42", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-01-01",
                source_registry_id: "IEA_2024", measurement_framework: "financial",
              },
              commodity_import_dependency_food: {
                value: "0.28", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-01-01",
                source_registry_id: "FAO_2024", measurement_framework: "human_development",
              },
              co2_concentration_ppm: {
                value: "421.0", unit: "ppm", variable_type: "stock",
                confidence_tier: 1, observation_date: "2024-01-01",
                source_registry_id: "NOAA_MLO_2024", measurement_framework: "ecological",
              },
              rule_of_law_percentile: {
                value: "52.4", unit: "percentile", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-01-01",
                source_registry_id: "WB_WGI_2024", measurement_framework: "governance",
              },
              democratic_quality_score: {
                value: "0.21", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-01-01",
                source_registry_id: "VDEM_2024", measurement_framework: "governance",
              },
            },
            EGY: {
              gdp_growth: {
                value: "0.029", unit: "ratio", variable_type: "ratio",
                confidence_tier: 3, observation_date: "2024-04-01",
                source_registry_id: "IMF_WEO_APR2024", measurement_framework: "financial",
              },
              unemployment_rate: {
                value: "0.071", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-07-01",
                source_registry_id: "ILO_2024", measurement_framework: "human_development",
              },
              health_expenditure_pct_gdp: {
                value: "0.048", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-12-01",
                source_registry_id: "WDI_2024", measurement_framework: "human_development",
              },
              net_enrollment_secondary: {
                value: "0.790", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-12-01",
                source_registry_id: "WDI_2024", measurement_framework: "human_development",
              },
              reserve_coverage_months: {
                value: "5.3", unit: "months", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-05-01",
                source_registry_id: "IMF_CR2024_EGY", measurement_framework: "financial",
              },
              trend_growth: {
                value: "0.045", unit: "ratio", variable_type: "ratio",
                confidence_tier: 3, observation_date: "2024-01-01",
                source_registry_id: "IMF_WEO_APR2024", measurement_framework: "financial",
              },
              commodity_import_dependency_fuel: {
                value: "0.23", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-01-01",
                source_registry_id: "IEA_2024", measurement_framework: "financial",
              },
              commodity_import_dependency_food: {
                value: "0.35", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-01-01",
                source_registry_id: "FAO_2024", measurement_framework: "human_development",
              },
              co2_concentration_ppm: {
                value: "421.0", unit: "ppm", variable_type: "stock",
                confidence_tier: 1, observation_date: "2024-01-01",
                source_registry_id: "NOAA_MLO_2024", measurement_framework: "ecological",
              },
              rule_of_law_percentile: {
                value: "29.3", unit: "percentile", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-01-01",
                source_registry_id: "WB_WGI_2024", measurement_framework: "governance",
              },
              democratic_quality_score: {
                value: "0.07", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-01-01",
                source_registry_id: "VDEM_2024", measurement_framework: "governance",
              },
            },
          },
        },
        scheduled_inputs: [
          {
            step: 3,
            input_type: "EmergencyPolicyInput",
            input_data: { instrument: "imf_program_acceptance", target_entity: "JOR", expected_duration: 3 },
          },
          {
            step: 3,
            input_type: "EmergencyPolicyInput",
            input_data: { instrument: "emergency_declaration", target_entity: "EGY", expected_duration: 2 },
          },
          {
            step: 3,
            input_type: "FiscalPolicyInput",
            input_data: { instrument: "spending_change", target_entity: "JOR", sector: "government", value: "0.06", duration_years: 1 },
          },
          {
            step: 4,
            input_type: "FiscalPolicyInput",
            input_data: { instrument: "spending_change", target_entity: "JOR", sector: "government", value: "-0.03", duration_years: 2 },
          },
        ],
      },
    });

    if (!createRes.ok()) {
      throw new Error(`Jordan/Egypt M12 scenario creation failed: ${createRes.status()} — ${await createRes.text()}`);
    }

    await speak(
      "This is the WorldSim application. The choropleth behind me shows GDP growth " +
      "rate across the map — geographic context for where we are simulating. " +
      "The analytical instrument is the cluster of panels above the map — " +
      "the trajectory chart, the alert panel, and the framework overview. " +
      "The platform is situation-agnostic. The engine is the same as the one that " +
      "ran Greece in 2010 and Argentina in 2001. Today's inputs are Jordan and Egypt " +
      "in 2024, and a disruption in the Strait of Hormuz.",
    );

    // ── Open scenario panel and select demo scenario ─────────────────────────

    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(800);

    await speak(
      "We have loaded a scenario: Jordan and Egypt, eight annual steps from 2024 to 2031. " +
      "The Strait of Hormuz disruption hits in year one — a fuel price shock " +
      "of twenty-five percent sustained over six steps. " +
      "Food supply chains follow in year two. " +
      "Jordan imports forty-two percent of its fuel. Egypt imports thirty-five percent of its food. " +
      "Same shock. Different import structures. Different crises. " +
      "On the trajectory chart, Jordan's primary indicator is reserve coverage — " +
      "it starts at seven point one months and will decline over the arc. " +
      "Egypt's primary indicator is governance — " +
      "it starts already far below the minimum floor before the shock begins.",
    );

    const scenarioRow = page.locator(".scenario-row").filter({ hasText: DEMO_SCENARIO_NAME });
    await expect(scenarioRow).toBeVisible({ timeout: 10_000 });
    await scenarioRow.getByTitle("Select as primary scenario").click();
    await page.waitForTimeout(1_500);
    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(600);

    // Wait for Zone 1 instrument cluster to load after scenario selection.
    await expect(page.locator('[data-testid="zone-1a-trajectory-container"]')).toBeVisible({ timeout: 15_000 });

    const nextStepBtn = page.getByRole("button", { name: /Next Step/ });
    await expect(nextStepBtn).toBeVisible({ timeout: 10_000 });

    // ── ACT 1: BASELINE ──────────────────────────────────────────────────────

    // ── Frame A: Advance to Step 1 — Instrument cluster seeded ──────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 1 / 8")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Step one. Year 2024. The Hormuz disruption begins. The fuel shock " +
      "propagates through the ExternalSector module. " +
      "Look at the four-framework overview — four axes, all live: financial, human development, ecological, governance. " +
      "This is the first demonstration in the tool's history where all four composite scores " +
      "are computed simultaneously. " +
      "Jordan and Egypt are both present in every axis. " +
      "Watch the financial axis for Jordan's reserve stress, and the governance axis for Egypt's pre-existing deficit.",
    );

    // Frame A: Full Zone 1 instrument cluster at step 1.
    await page.screenshot({ path: screenshotPath("frame-a-instrument-cluster.png") });

    // ── Frame B: Advance to Step 2 — Food shock joins, Egypt alert critical ──

    await nextStepBtn.click();
    await expect(page.getByText("Step 2 / 8")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Step two. Year 2025. The food supply chain disruption joins the fuel shock. " +
      "Look at the alert panel. " +
      "Egypt's governance alert: CRITICAL. Democratic quality score of zero point zero seven " +
      "on the V-Dem Liberal Democracy Index. " +
      "That number is not a step two finding. It was true in 2024. " +
      "The model surfaced it at step one, and it is still critical now. " +
      "Jordan's governance: stable, at fifty-two point four on the rule-of-law percentile. " +
      "Two countries, same external shock, entirely different institutional starting positions.",
    );

    // Frame B: MDA alert panel prominent — Egypt governance CRITICAL in Zone 1B.
    await page.screenshot({ path: screenshotPath("frame-b-terminal-alerts.png") });

    // ── Frame C: Advance to Step 3 — THESIS FRAME ────────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 3 / 8")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Step three. Year 2026. Dual shock peak. The IMF enters. " +
      "Jordan has accepted an IMF liquidity programme — emergency backstop. " +
      "GCC partners have provided budget support — three precedents in the last decade. " +
      "This is the thesis frame. " +
      "Jordan reserves: five months, down from seven point one. " +
      "Jordan's reserve curve is burning at approximately one point two months per step. " +
      "Pause here. Read what the instruments are telling you before we test a counter-proposal. " +
      "One note on the governance alert for Egypt: it carries an Exploratory confidence tier. " +
      "The direction of deterioration is consistent with V-Dem historical data. " +
      "The label means magnitude calibration is pending — not that the finding is invalid.",
    );

    // Frame C: Step 3 thesis frame — choropleth + Zone 1 showing two entities.
    await page.screenshot({ path: screenshotPath("frame-c-mena-choropleth.png") });

    // ── ACT 2: MODE 3 COUNTER-PROPOSAL ───────────────────────────────────────

    await speak(
      "Act two. The ministry team does not accept this trajectory as inevitable. " +
      "Jordan is in the negotiating room at step three. " +
      "The IMF backstop is on the table. The conditionality terms are also on the table. " +
      "The question is: what does the trajectory look like if the ministry accepts the " +
      "liquidity support but negotiates successfully on the fiscal conditionality? " +
      "Mode 3 is the counter-proposal function.",
    );

    // Enable Mode 3 Active Control.
    await page.locator('[data-testid="mode3-toggle"]').click();
    // G4: policy-param-slider replaces fiscal-multiplier-slider (ADR-019 D-3).
    await expect(page.locator('[data-testid="policy-param-slider"]')).toBeVisible({ timeout: 5_000 });

    // Set fiscal multiplier to 1.30 using native input setter (required for React controlled inputs).
    await page.locator('[data-testid="policy-param-slider"]').evaluate(
      (el, value) => {
        const slider = el as HTMLInputElement;
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
          window.HTMLInputElement.prototype,
          "value",
        )?.set;
        nativeInputValueSetter?.call(slider, value);
        slider.dispatchEvent(new Event("input", { bubbles: true }));
      },
      "1.30",
    );
    await page.waitForTimeout(300);

    // Apply the branch — this runs the parallel trajectory from step 3 onward.
    // G4: apply-policy-input replaces apply-control-change (ADR-019 D-3).
    await page.locator('[data-testid="apply-policy-input"]').click();

    // Wait for branch computation to complete (recompute badge disappears).
    await expect(page.locator('[data-testid="recompute-badge"]')).not.toBeVisible({ timeout: 30_000 });
    await expect(page.locator('[data-testid="branch-anchor-label"]')).toBeVisible({ timeout: 5_000 });
    await page.waitForTimeout(800);

    await speak(
      "Branch applied. The fiscal multiplier is set to one point three. " +
      "In the branch: Jordan accepts the IMF emergency liquidity backstop at step three. " +
      "The GCC support remains, amplified by the higher implementation efficiency. " +
      "The austerity conditionality at step four does not enter the branch. " +
      "The question being asked is: what does that negotiating outcome cost the IMF, " +
      "and what does it give Jordan? " +
      "Look at the trajectory chart. Jordan's baseline and branch curves are not yet diverging at step three — " +
      "the GCC multiplier effect appears at step four. " +
      "Advance to step five to see where Jordan's two trajectories separate.",
    );

    // Frame D: Mode 3 active, branch anchor visible, step 3.
    await page.screenshot({ path: screenshotPath("frame-d-mode3-active-control.png") });

    // ── Frame E: Advance to Step 5 — Primary divergence peak ─────────────────

    // Step 3 → Step 4
    await nextStepBtn.click();
    await expect(page.getByText("Step 4 / 8")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(600);

    // Step 4 → Step 5 (primary divergence)
    await nextStepBtn.click();
    await expect(page.getByText("Step 5 / 8")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Step five. Year 2028. This is where the divergence peaks. " +
      "The trajectory chart — two curves for Jordan GDP: baseline and branch. " +
      "The gap at step five is approximately one point seven percentage points. " +
      "That is the cost of the conditionality. " +
      "Unemployment in the baseline: the GCC support drove it down to sixteen point six " +
      "percent at step four, then conditionality reversed it to seventeen point two " +
      "percent at step five. In the branch, unemployment continues declining. " +
      "One step. One conditionality term. The direction of the unemployment curve reverses. " +
      "Now look at Jordan's reserve curve. " +
      "Both of Jordan's trajectories — baseline and branch — reach zero reserves by step seven. " +
      "Better conditionality terms improved Jordan's GDP and unemployment trajectory. " +
      "They did not change Jordan's structural fuel import dependency during a live Hormuz disruption. " +
      "The reserve crisis is survived under better internal conditions. It is not avoided. " +
      "The minister should know this before she uses this finding at the table.",
    );

    // Frame E: Step 5, all four axes showing baseline + branch divergence.
    await page.screenshot({ path: screenshotPath("frame-e-step5-divergence.png") });

    await speak(
      "The four-framework overview — all four composite scores at step five, branch trajectory. " +
      "Financial: Jordan is substantially above Egypt in the branch — the fiscal multiplier " +
      "produced a percentile rank divergence. In the baseline, the two are nearly identical. " +
      "Human Development: bottom-quintile consumption capacity eroded. The branch slows the erosion. " +
      "Ecological: CO2 accumulation is independent of the Hormuz crisis. Both trajectories track identically. " +
      "Governance: Egypt far below the MDA floor from step one — this is unchanged. " +
      "No axis is null. No axis is dashed. " +
      "Greece 2014 looked like recovery on GDP. It was not recovery on unemployment, " +
      "child poverty, or life expectancy. " +
      "This instrument shows all four axes in the room, at the moment when it can still " +
      "be argued at the table.",
    );

    // Sections 3–5 (backtesting, roadmap, North Star) delivered verbally.
    // See docs/demo/m12/stakeholder-walkthrough.md §§3–7.
  },
);
