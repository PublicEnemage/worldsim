/**
 * WorldSim Stakeholder Demo — Screen-Recorded Narrated Walkthrough (M14)
 *
 * Demo 5: Zambia 2024, IMF Extended Credit Facility Review.
 * Single entity. Trust architecture — ADR-016 Grounding strip + ADR-015 Evidence thread.
 * Reserve coverage challenge-response as thesis moment.
 * No Mode 3 (EL decision 2026-06-19).
 *
 * Five screenshots per UX Agent brief (docs/demo/m14/screenshot-brief.md):
 *   frame-a-grounding-strip.png        — Step 1, ZMB loaded, Grounding strip + L0 annotations
 *   frame-b-zone1b-reserve.png         — Step 2, Zone 1B self-interpreting reserve alert
 *   frame-c-citation-at-table.png      — Step 2 THESIS: Grounding strip citation answering the challenge
 *   frame-d-political-feasibility.png  — Step 3, Zone 1D with PSP alongside four composites
 *   frame-e-evidence-thread.png        — Step 5, full arc + evidence thread complete
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
 * M8 archive:  demo-narrated-m8.spec.ts
 * M10 archive: demo-narrated-m10.spec.ts
 * M12 archive: demo-narrated-m12.spec.ts
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
const SCREENSHOT_DIR = path.resolve(__dirname, "../../../docs/demo/m14/screenshots/");

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
const DEMO_SCENARIO_NAME = `Zambia 2024 IMF ECF Review Demo 5 — ${new Date().toISOString().slice(0, 10)}-${RUN_ID}`;

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
      s.name.startsWith("Zambia 2024 IMF ECF Review Demo 5") &&
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
  "Stakeholder demo walkthrough — narrated screen recording (M14)",
  { tag: ["@demo"] },
  async ({ page }) => {
    test.setTimeout(25 * 60 * 1000);

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

    // Create the M14 Zambia ECF demo scenario via API.
    // ZMB initial attributes from IMF WEO Apr 2024 (T2) and World Bank WDI 2023 (T2).
    // reserve_coverage_months: 3.8 months — close to the CRITICAL floor (3.0 months).
    // Fiscal conditionality at step 2 triggers drawdown below the WARNING threshold.
    // Political economy module enabled to surface programme_survival_probability (PSP) in Zone 1D.
    const createRes = await page.request.post("http://localhost:8000/api/v1/scenarios", {
      data: {
        name: DEMO_SCENARIO_NAME,
        description: "Zambia IMF ECF program review — M14 Demo 5 trust architecture demonstration",
        configuration: {
          entities: ["ZMB"],
          n_steps: 6,
          timestep_label: "annual",
          start_date: "2024-01-01",
          modules_config: {
            ecological: { enabled: true },
            governance: { enabled: true },
            political_economy: { enabled: true },
          },
          initial_attributes: {
            ZMB: {
              reserve_coverage_months: {
                value: "3.8", unit: "months", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-04-01",
                source_registry_id: "IMF_WEO_APR2024", measurement_framework: "financial",
              },
              gdp_growth: {
                value: "0.047", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2024-04-01",
                source_registry_id: "IMF_WEO_APR2024", measurement_framework: "financial",
              },
              trend_growth: {
                value: "0.035", unit: "ratio", variable_type: "ratio",
                confidence_tier: 3, observation_date: "2024-01-01",
                source_registry_id: "IMF_WEO_APR2024", measurement_framework: "financial",
              },
              unemployment_rate: {
                value: "0.130", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2023-12-01",
                source_registry_id: "WORLD_BANK_WDI_2023", measurement_framework: "human_development",
              },
              health_expenditure_pct_gdp: {
                value: "0.035", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2023-12-01",
                source_registry_id: "WORLD_BANK_WDI_2023", measurement_framework: "human_development",
              },
              net_enrollment_secondary: {
                value: "0.450", unit: "ratio", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2023-12-01",
                source_registry_id: "WORLD_BANK_WDI_2023", measurement_framework: "human_development",
              },
              co2_concentration_ppm: {
                value: "421.0", unit: "ppm", variable_type: "stock",
                confidence_tier: 2, observation_date: "2024-01-01",
                source_registry_id: "WORLD_BANK_WDI_2023", measurement_framework: "ecological",
              },
              rule_of_law_percentile: {
                value: "24.0", unit: "percentile", variable_type: "ratio",
                confidence_tier: 2, observation_date: "2023-12-01",
                source_registry_id: "WORLD_BANK_WDI_2023", measurement_framework: "governance",
              },
              democratic_quality_score: {
                value: "0.34", unit: "ratio", variable_type: "ratio",
                confidence_tier: 3, observation_date: "2023-12-01",
                source_registry_id: "WORLD_BANK_WDI_2023", measurement_framework: "governance",
              },
            },
          },
          scheduled_inputs: [
            {
              step: 1,
              input_type: "EmergencyPolicyInput",
              input_data: { instrument: "imf_program_acceptance", target_entity: "ZMB", expected_duration: 4 },
            },
            {
              step: 2,
              input_type: "FiscalPolicyInput",
              input_data: { instrument: "spending_change", target_entity: "ZMB", sector: "government", value: "-0.025", duration_years: 2 },
            },
          ],
        },
      },
    });

    if (!createRes.ok()) {
      throw new Error(`ZMB M14 scenario creation failed: ${createRes.status()} — ${await createRes.text()}`);
    }

    await speak(
      "This is WorldSim. " +
      "There is a room where this happens. " +
      "On one side of the table: a creditor team with proprietary models, institutional memory, " +
      "and a dataset the ministry team cannot access. " +
      "On the other side: a finance ministry, three economists, and public data. " +
      "Today we are in that room with Zambia. " +
      "The year is 2024. Zambia is in an IMF Extended Credit Facility program. " +
      "The program review is approaching. " +
      "The creditor team has just challenged the reserve coverage figure. " +
      "This demonstration shows what the ministry team can do when that challenge arrives.",
    );

    // ── Open scenario panel and select demo scenario ──────────────────────────

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

    // ── FRAME A: Step 1 — Grounding strip at scenario load ───────────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 1 / 6")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Zambia, 2024. Step one — the IMF program is accepted. " +
      "The instrument cluster is loaded. " +
      "Notice the scenario parameters panel — the Grounding strip. " +
      "Every initial number has a named source, a confidence tier, and a date. " +
      "Reserve coverage: three point eight months. " +
      "Source: IMF World Economic Outlook, April 2024. Tier two. " +
      "That is on the screen before the simulation runs. " +
      "The trust architecture is not a footnote. It is the first thing visible. " +
      "Zone 1A shows the reserve trajectory with a tier badge — T2 — directly on the curve. " +
      "The provenance is on the instrument, not buried in a footnote.",
    );

    // Frame A: ZMB at step 1, Grounding strip visible, L0 annotations on trajectory.
    await page.screenshot({ path: screenshotPath("frame-a-grounding-strip.png") });

    // ── FRAME B: Step 2 — Zone 1B self-interpreting reserve alert ────────────

    await nextStepBtn.click();
    await expect(page.getByText("Step 2 / 6")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Step two. Year 2025. Fiscal conditionality begins — " +
      "the programme requires a two point five percent spending reduction. " +
      "Look at Zone one B — the alert panel. " +
      "Reserve coverage is declining. " +
      "The alert panel does not say 'threshold breached.' " +
      "It says: Reserve Coverage, the current value, " +
      "approaching the three point zero month CRITICAL floor. " +
      "At the current draw rate, CRITICAL is reached within two steps. " +
      "The instrument tells you what the number means, not just what it is. " +
      "The confidence tier is visible alongside the value: Tier two. IMF WEO April 2024. " +
      "That is the answer to the creditor's question — before they finish asking it.",
    );

    // Frame B: Zone 1B persistent-detail with reserve alert, Layer 3 text visible.
    await page.screenshot({ path: screenshotPath("frame-b-zone1b-reserve.png") });

    // ── FRAME C (THESIS): The citation at the table ───────────────────────────

    await speak(
      "The creditor says: where does your three point eight months reserve figure come from? " +
      "We have a different number in our model. " +
      "The analyst points to the screen. " +
      "IMF World Economic Outlook, April 2024. Tier two source. " +
      "No drawer to open. No specialist to call. Under ten seconds. " +
      "The source is the IMF's own publication — " +
      "the creditor is challenging a figure from their own institution's dataset. " +
      "The Grounding strip and the Zone 1B detail are saying the same thing: " +
      "this number is sourced, it is verifiable, and the methodology for assigning " +
      "that tier is published — anyone can check it.",
    );

    // Frame C (THESIS): Full viewport showing citation visible in Zone 1B + Grounding strip.
    await page.screenshot({ path: screenshotPath("frame-c-citation-at-table.png") });

    // ── FRAME D: Step 3 — Political feasibility alongside reserve alert ───────

    await nextStepBtn.click();
    await expect(page.getByText("Step 3 / 6")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Step three. Year 2026. Reserve coverage crosses the CRITICAL threshold. " +
      "Look at Zone one D — the four-framework overview. " +
      "There is a fifth readout now: programme survival probability. " +
      "The political economy module is asking a different question from the reserve alert. " +
      "It is asking: given the fiscal pressure this government is under, " +
      "what is the probability that the programme's conditionality terms can actually be implemented? " +
      "That is not a financial question. It is a political feasibility question. " +
      "The reserve crisis and the political sustainability of the programme are related, " +
      "but they are not the same constraint. " +
      "Both are visible on the same instrument. For the first time.",
    );

    // Frame D: Zone 1D with PSP visible alongside four composites at step 3.
    await page.screenshot({ path: screenshotPath("frame-d-political-feasibility.png") });

    // ── FRAME E: Step 5 — Full evidence thread ────────────────────────────────

    // Advance to step 4
    await nextStepBtn.click();
    await expect(page.getByText("Step 4 / 6")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(600);

    // Advance to step 5
    await nextStepBtn.click();
    await expect(page.getByText("Step 5 / 6")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Step five. Year 2028. " +
      "From three point eight months reserve coverage at scenario entry — five annual steps. " +
      "Every number in this trajectory has a named source. " +
      "Every input that drove the output is visible in the assumption surface. " +
      "The confidence tier on every indicator tells you " +
      "whether it came from measured data or a model estimate — " +
      "and the methodology for that assignment is published and auditable. " +
      "This is what the ministry team has at the table: " +
      "not just a number, but a traceable chain " +
      "from data source to assumption to output. " +
      "The creditor can challenge the number. " +
      "They cannot challenge the chain.",
    );

    // Frame E: Full instrument cluster at step 5 — complete evidence thread visible.
    await page.screenshot({ path: screenshotPath("frame-e-evidence-thread.png") });

    await speak(
      "Sections three through five — backtesting credibility, roadmap, and north star — " +
      "delivered verbally. See docs/demo/m14/stakeholder-walkthrough.md for the full script.",
    );
  },
);
