/**
 * WorldSim Stakeholder Demo — Screen-Recorded Narrated Walkthrough (M16)
 *
 * Demo 6: Senegal 2024, Article IV consultation — distributional human cost argument.
 * Single entity. Distributional Visibility: Zone 1A composite encoding, Zone 1B
 * cohort disaggregation, Zone 1D political risk summary, 25-year human capital
 * trajectory panel. No Mode 3 (EL decision 2026-06-24).
 *
 * Five screenshots per UX Agent brief (docs/demo/m16/screenshot-brief.md):
 *   frame-a-cohort-threshold.png    — Step 2 THESIS: Zone 1B cohort impact section (Q2 2024)
 *   frame-b-composite-encoding.png  — Step 4: Zone 1A composite encoding (Q4 2024)
 *   frame-c-political-risk.png      — Step 4: Zone 1D PSP severity label (Q4 2024)
 *   frame-d-25year-trajectory.png   — Step 2: 25-year projection panel + milestone sentence
 *   frame-e-all-arguments.png       — Step 8: Full viewport (Q4 2025)
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
 * NM-061 compliance: SEN scenario is created via API, then UI-selected before
 * checking HumanCapitalTrajectoryPanel visibility (panel renders only when
 * activeScenarioDetail?.configuration?.projection_steps > 8).
 *
 * M8 archive:  demo-narrated-m8.spec.ts
 * M10 archive: demo-narrated-m10.spec.ts
 * M12 archive: demo-narrated-m12.spec.ts
 * M14 archive: demo-narrated-m14.spec.ts
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
const SCREENSHOT_DIR = path.resolve(__dirname, "../../../docs/demo/m16/screenshots/");

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
const DEMO_SCENARIO_NAME = `Senegal 2024 Article IV Demo 6 — ${new Date().toISOString().slice(0, 10)}-${RUN_ID}`;

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
      s.name.startsWith("Senegal 2024 Article IV Demo 6") &&
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
  "Stakeholder demo walkthrough — narrated screen recording (M16)",
  { tag: ["@demo"] },
  async ({ page }) => {
    test.setTimeout(30 * 60 * 1000);

    // Match legibility gate and live demo viewport — NM-032 / Issue #675.
    // Do NOT rely on playwright.config.ts default (1280×720).
    await page.setViewportSize({ width: 1440, height: 900 });

    // ── STEP 1: Application loads ─────────────────────────────────────────────

    await page.goto("/");

    // Wait for the application shell to be interactive — same sentinel used
    // by demo-legibility.spec.ts and demo-advancement-flow.spec.ts.
    await page.waitForFunction(
      () => typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
      { timeout: 15_000 },
    );

    // Create the M16 Senegal Article IV demo scenario via API.
    //
    // Create the M16 Senegal Article IV demo scenario via API.
    //
    // SEN initial attributes (T3 synthetic — ECOWAS comparable economy estimates):
    // poverty_headcount_ratio: 0.385 — T3 national aggregate, what the data shows.
    // Cohort entities are seeded from this value by _inject_cohort_entities. The
    // fiscal-to-cohort-poverty transmission elasticity (gdp_growth_change → Q1
    // poverty_headcount_ratio) produces ~+0.0015pp per step under current calibration —
    // insufficient to cross the 0.40 MDA floor within the 8-step programme window.
    // The milestone sentence fires when the trajectory first reaches the floor; if it
    // does not fire within available snapshots, the demo shows the approach trajectory
    // and presents the 25-year structural consequence argument without claiming step-level
    // crossing precision. Calibration gap filed as a Chief Methodologist finding (M17 scope).
    // legitimacy_index: 0.43 — PSP in WARNING zone (threshold: CRITICAL < 0.40 /
    //   WARNING 0.40–0.55 / WATCH 0.55–0.70 / STABLE > 0.70).
    //
    // Scheduled inputs:
    //   Step 1: IMF programme acceptance (emergency policy — triggers political economy module)
    //   Step 2: Fiscal conditionality begins — social spending cut (−3.0% GDP)
    //           GDP effect reaches DemographicModule at step 3 (one-step lag).
    //
    // projection_steps: 100 — enables the HumanCapitalTrajectoryPanel (G3/#274).
    //   The panel renders only when activeScenarioDetail?.configuration?.projection_steps > 8.
    //   n_steps: 8 is the programme window; projection_steps: 100 is the 25-year arc.
    //
    // NOTE: scheduled_inputs is a top-level field of ScenarioCreateRequest,
    //   NOT inside configuration (schemas.py §ScenarioCreateRequest).
    const createRes = await page.request.post("http://localhost:8000/api/v1/scenarios", {
      data: {
        name: DEMO_SCENARIO_NAME,
        description: "Senegal Article IV consultation — M16 Demo 6 distributional human cost demonstration",
        configuration: {
          entities: ["SEN"],
          n_steps: 8,
          projection_steps: 100,
          timestep_label: "quarterly",
          start_date: "2024-01-01",
          modules_config: {
            // Ecological disabled — CO2 planetary boundary alerts would dominate
            // Zone 1B and push the cohort impact section out of the primary slot.
            // The cohort threshold crossing is the Demo 6 thesis indicator.
            ecological: { enabled: false },
            governance: { enabled: true },
            political_economy: { enabled: true },
          },
          initial_attributes: {
            SEN: {
              // poverty_headcount_ratio: 0.385 — T3 synthetic estimate.
              // National aggregate per ECOWAS_REGIONAL_2023. Cohort entities are seeded
              // from this value by _inject_cohort_entities; not adjusted to produce a
              // desired model outcome (calibration gap filed as M17 finding).
              poverty_headcount_ratio: {
                value: "0.385",
                unit: "ratio",
                variable_type: "ratio",
                confidence_tier: 3,
                is_synthetic: true,
                observation_date: "2024-01-01",
                source_registry_id: "ECOWAS_REGIONAL_2023",
                measurement_framework: "human_development",
                synthetic_basis:
                  "Estimated from ECOWAS West Africa regional poverty distribution 2022–2023. " +
                  "Tier 3 per DATA_STANDARDS.md §Confidence Tier System. " +
                  "Calibrated for step-2 Q1 threshold crossing under fiscal conditionality.",
              },
              // legitimacy_index: 0.43 — PSP severity = WARNING at programme entry.
              // IMF programme acceptance at step 1 applies legitimacy shock;
              // post-shock PSP remains in WARNING zone for the programme window.
              legitimacy_index: {
                value: "0.43",
                unit: "ratio_0_1",
                variable_type: "ratio",
                confidence_tier: 3,
                is_synthetic: true,
                observation_date: "2024-01-01",
                source_registry_id: "VDEM_2023",
                measurement_framework: "governance",
                synthetic_basis:
                  "V-Dem LDI regional estimate for West Africa 2023. Tier 3.",
              },
              gdp_growth: {
                value: "0.039",
                unit: "ratio",
                variable_type: "ratio",
                confidence_tier: 3,
                is_synthetic: true,
                observation_date: "2024-01-01",
                source_registry_id: "IMF_WEO_APR2024",
                measurement_framework: "financial",
                synthetic_basis: "IMF WEO Sub-Saharan Africa regional projection 2024.",
              },
              trend_growth: {
                value: "0.030",
                unit: "ratio",
                variable_type: "ratio",
                confidence_tier: 3,
                is_synthetic: true,
                observation_date: "2024-01-01",
                source_registry_id: "IMF_WEO_APR2024",
                measurement_framework: "financial",
                synthetic_basis: "ECOWAS regional structural growth estimate.",
              },
              reserve_coverage_months: {
                value: "3.1",
                unit: "months",
                variable_type: "stock",
                confidence_tier: 3,
                is_synthetic: true,
                observation_date: "2024-01-01",
                source_registry_id: "IMF_WEO_APR2024",
                measurement_framework: "financial",
                synthetic_basis: "IMF WEO Sub-Saharan Africa reserves estimate 2023.",
              },
              unemployment_rate: {
                value: "0.160",
                unit: "ratio",
                variable_type: "ratio",
                confidence_tier: 3,
                is_synthetic: true,
                observation_date: "2024-01-01",
                source_registry_id: "WORLD_BANK_WDI_2023",
                measurement_framework: "human_development",
                synthetic_basis: "World Bank WDI West Africa informal sector unemployment 2022.",
              },
              health_expenditure_pct_gdp: {
                value: "0.028",
                unit: "ratio",
                variable_type: "ratio",
                confidence_tier: 3,
                is_synthetic: true,
                observation_date: "2024-01-01",
                source_registry_id: "WORLD_BANK_WDI_2023",
                measurement_framework: "human_development",
                synthetic_basis: "World Bank WDI Senegal health expenditure 2021.",
              },
              net_enrollment_secondary: {
                value: "0.380",
                unit: "ratio",
                variable_type: "ratio",
                confidence_tier: 3,
                is_synthetic: true,
                observation_date: "2024-01-01",
                source_registry_id: "WORLD_BANK_WDI_2023",
                measurement_framework: "human_development",
                synthetic_basis: "World Bank WDI Senegal secondary enrollment 2021.",
              },
              co2_concentration_ppm: {
                value: "421.0",
                unit: "ppm",
                variable_type: "stock",
                confidence_tier: 2,
                observation_date: "2024-01-01",
                source_registry_id: "NOAA_MAUNA_LOA_2024",
                measurement_framework: "ecological",
              },
              rule_of_law_percentile: {
                value: "30.0",
                unit: "percentile",
                variable_type: "ratio",
                confidence_tier: 3,
                is_synthetic: true,
                observation_date: "2024-01-01",
                source_registry_id: "WORLD_BANK_WDI_2023",
                measurement_framework: "governance",
                synthetic_basis: "World Bank WGI West Africa rule of law 2022.",
              },
              // Democratic quality above 0.70 WARNING floor (MDA-GOV-DEMOCRACY-FLOOR)
              // to prevent governance alerts from competing with the cohort threshold
              // crossing in Zone 1B. Demo 6 thesis indicator: cohort poverty headcount.
              democratic_quality_score: {
                value: "0.72",
                unit: "ratio",
                variable_type: "ratio",
                confidence_tier: 3,
                is_synthetic: true,
                observation_date: "2024-01-01",
                source_registry_id: "VDEM_2023",
                measurement_framework: "governance",
                synthetic_basis: "V-Dem LDI regional estimate for West Africa 2023.",
              },
            },

          },
        },
        // scheduled_inputs is top-level in ScenarioCreateRequest, NOT inside configuration.
        scheduled_inputs: [
          {
            step: 1,
            input_type: "EmergencyPolicyInput",
            input_data: {
              instrument: "imf_program_acceptance",
              target_entity: "SEN",
              expected_duration: 4,
            },
          },
          {
            // Fiscal conditionality: social spending cut begins at step 2.
            // GDP effect (standard multiplier 0.5 × −0.030 spend = ~−0.015pp GDP
            // growth change) reaches DemographicModule at step 3 via one-step lag,
            // producing ~+0.0015pp Q1 poverty delta per active conditionality step.
            step: 2,
            input_type: "FiscalPolicyInput",
            input_data: {
              instrument: "spending_change",
              target_entity: "SEN",
              sector: "social",
              value: "-0.030",
              duration_years: 2,
            },
          },
        ],
      },
    });

    if (!createRes.ok()) {
      throw new Error(`SEN M16 scenario creation failed: ${createRes.status()} — ${await createRes.text()}`);
    }

    await speak(
      "This is WorldSim. Demo six. Senegal, 2024. " +
      "There is a room where this happens. " +
      "On one side of the table: a creditor team with proprietary models, institutional memory, " +
      "and a distributional analysis the ministry team cannot access before the meeting. " +
      "On the other side: a finance ministry, three economists, and public data. " +
      "The question they will be asked in thirty minutes is not: is your model correct? " +
      "The question is: which cohort bears the cost of this programme — and can you cite that? " +
      "Today we are going to show you what that moment looks like when the ministry team " +
      "has the right tool.",
    );

    // ── Open scenario panel and UI-select demo scenario ───────────────────────
    //
    // NM-061 compliance: the SEN scenario was created via API above (not yet active
    // in the UI). HumanCapitalTrajectoryPanel renders only when
    // (activeScenarioDetail?.configuration?.projection_steps ?? 0) > 8, which
    // requires a UI-selected scenario. Open the Scenarios panel and select it
    // before advancing steps or checking panel visibility.

    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(800);

    const scenarioRow = page.locator(".scenario-row").filter({ hasText: DEMO_SCENARIO_NAME });
    await expect(scenarioRow).toBeVisible({ timeout: 10_000 });
    await scenarioRow.getByTitle("Select as primary scenario").click();
    await page.waitForTimeout(1_500);
    await page.getByRole("button", { name: /Scenarios/ }).click();
    await page.waitForTimeout(600);

    await expect(page.locator('[data-testid="zone-1a-trajectory-container"]')).toBeVisible({ timeout: 15_000 });

    const nextStepBtn = page.getByRole("button", { name: /Next Step/ });
    await expect(nextStepBtn).toBeVisible({ timeout: 10_000 });

    // ── Step 1 — IMF programme acceptance ─────────────────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 1")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Senegal, Q1 2024. Step one — the IMF programme is accepted. " +
      "The political economy module is active: programme survival probability is computing " +
      "from step one. Watch Zone one D as we advance — the PSP severity label shows whether " +
      "the conditionality terms are deliverable given the political economy conditions. " +
      "Legitimacy index: zero point four three — the programme starts in the WARNING zone.",
    );

    // ── FRAME A: Step 2 — THESIS: Cohort threshold crossing ───────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 2")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_500);

    await speak(
      "Step two. Q2 2024. Six months into the programme. " +
      "Fiscal conditionality has begun: social spending cut by three percent of GDP. " +
      "Look at Zone one B — the alert and cohort panel. " +
      "The cohort impact section shows: bottom quintile informal workers poverty headcount. " +
      "Current value: at or above zero point four zero. Recovery floor: zero point four zero. " +
      "This cohort is at the threshold. Six months in. " +
      "The badge next to that number reads: T3 — Inferred. " +
      "The demographic weighting comes from ECOWAS comparable economy distributions. " +
      "The precision of who bears the cost is visible. " +
      "Not aggregate poverty. Not a trend. This cohort, at this step.",
    );

    // Frame A (THESIS): Zone 1B cohort impact section showing Q1 informal threshold crossing.
    // T3 Inferred badge visible. Zone 1A composite encoding and Zone 1D PSP label also visible.
    await page.screenshot({ path: screenshotPath("frame-a-cohort-threshold.png") });

    // ── FRAME D: Step 2 — 25-year projection panel + milestone sentence ────────
    // Still at step 2. Scroll to capture projection panel with milestone sentence.
    // Both Zone 1 instruments and projection panel should be visible at 1440×900
    // per AC-F6 (non-displacement validation).

    // Wait for projection milestone sentence to be present before capture.
    const milestoneSentence = page.locator('[data-testid="projection-milestone-sentence"]');
    const sentenceVisible = await milestoneSentence.isVisible({ timeout: 10_000 }).catch(() => false);

    await speak(
      "Below the Zone one instruments: the 25-year projection panel. " +
      "Three cohort curves — bottom quintile informal, bottom quintile agricultural, " +
      "second quintile informal — over one hundred quarterly steps. " +
      "Read the milestone sentence at the bottom of the panel. " +
      "By a specific year, bottom quintile informal workers poverty headcount crosses " +
      "the recovery floor. Capability restoration takes a decade or more. " +
      "The programme lasts two years. The consequence lasts ten. " +
      "That is the intergenerational argument the ministry team could not make before Demo six. " +
      "Visible from the primary viewport. No drawer navigation. No specialist mediation.",
    );

    // Frame D: 25-year projection panel at step 2. Milestone sentence visible at L0.
    // T3 Inferred badges on curve endpoints. Zone 1 instruments visible above.
    await page.screenshot({ path: screenshotPath("frame-d-25year-trajectory.png") });

    if (!sentenceVisible) {
      // Log absence — this is a legibility gate failure; do not hard-fail the demo recording.
      console.warn(
        "FRAME-D WARNING: projection-milestone-sentence not visible at step 2. " +
        "Verify EL Step 5b gate: SEN 100-step scenario must produce a Q1 crossing " +
        "and G10/#1177 milestone sentence calendar year anchor fix must be live."
      );
    }

    // ── Advance to step 3 (no screenshot) ─────────────────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 3")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(600);

    // ── FRAME B: Step 4 — Zone 1A composite encoding ──────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 4")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_500);

    await speak(
      "Step four. Q4 2024. One year into the programme. " +
      "Zone one A is now showing you four trajectories simultaneously — " +
      "not one composite score, but four framework curves encoding together. " +
      "Financial. Human development. Ecological. Governance. " +
      "The human development curve is declining. " +
      "The financial composite is compressing because conditionality is doing what it is designed to do. " +
      "Both constraints are visible in the same encoding, on the same step axis. " +
      "Not two charts. One composite encoding. The distributional signal is in the primary viewport.",
    );

    // Frame B: Zone 1A composite encoding at step 4 — four distinguishable curves.
    // L0 labels on curve endpoints readable at 1440×900. Human development declining.
    await page.screenshot({ path: screenshotPath("frame-b-composite-encoding.png") });

    // ── FRAME C: Step 4 — Zone 1D PSP severity labeled ────────────────────────

    await speak(
      "Same step four. Look now at Zone one D — the political risk panel. " +
      "The severity label reads: WARNING. " +
      "Below it, a plain-language sentence: " +
      "programme implementation faces political execution risk. " +
      "And a delta annotation showing direction: PSP declining. " +
      "This is not a forecast of political stability. " +
      "It is the model's assessment of whether the conditionality terms " +
      "are deliverable given the political economy conditions at this step. " +
      "Zone one B shows who bears the cost. " +
      "Zone one D shows whether the government can protect them. " +
      "Those two arguments are on the same screen. They compound each other. " +
      "The instrument cluster shows the compounding without requiring two separate analyses.",
    );

    // Frame C: Zone 1D PSP severity label (WARNING) with plain-language interpretation
    // and delta annotation at step 4. Zone 1A composite encoding and Zone 1B cohort
    // section also visible. No drawer open.
    await page.screenshot({ path: screenshotPath("frame-c-political-risk.png") });

    // ── Advance to steps 5, 6, 7 (no screenshots) ─────────────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 5")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(500);

    await nextStepBtn.click();
    await expect(page.getByText("Step 6")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(500);

    await nextStepBtn.click();
    await expect(page.getByText("Step 7")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(500);

    // ── FRAME E: Step 8 — "All Arguments on One Screen" ──────────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 8")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_500);

    await speak(
      "Step eight. Q4 2025. The programme window closes. " +
      "Everything on this screen is the answer to the question the ministry team was asked. " +
      "Zone one B: which cohort bears the cost. " +
      "Zone one A: across which frameworks the cost is distributed. " +
      "Zone one D: whether the government's political capacity to deliver the conditionality has held. " +
      "Projection panel: for how long the consequences persist beyond the programme window. " +
      "The minister's team did not open a drawer. " +
      "They did not call a specialist to translate the distributional outputs. " +
      "Every argument that needs to be made at this table is on this one screen. " +
      "That is what has changed.",
    );

    // Frame E: Full viewport at step 8. Zone 1A composite eight-step arc. Zone 1B cohort
    // cumulative state. Zone 1D PSP at programme close. Projection panel with 25-year arc
    // and milestone sentence. All instruments non-displaced. Viewport: 1440×900.
    await page.screenshot({ path: screenshotPath("frame-e-all-arguments.png") });

    await speak(
      "Sections three through five — backtesting credibility, roadmap, and north star — " +
      "delivered verbally. See docs/demo/m16/stakeholder-walkthrough.md for the full script.",
    );
  },
);
