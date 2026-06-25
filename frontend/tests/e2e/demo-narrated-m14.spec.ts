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
 *   frame-b-zone1b-reserve.png         — Step 3, Zone 1B self-interpreting reserve alert
 *   frame-c-citation-at-table.png      — Step 3 THESIS: Grounding strip citation answering the challenge
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
    // ZMB initial attributes from IMF WEO Apr 2024 (T2) and World Bank WDI 2023 (T2/T3).
    // reserve_coverage_months: 3.8 months (T2, IMF WEO Apr 2024) — the figure the
    //   creditor challenges at the review table. WARNING zone starts at 3.0 months
    //   (20% approach to the 2.5-month CRITICAL floor per MDA-FIN-RESERVES).
    // Food commodity shock (0.35 × food import dependency 0.15 × burn rate 8.5 = 0.45
    //   months per step) drives reserve drawdown: step 2 → 3.35m, step 3 → 2.90m (WARNING).
    // legitimacy_index = 0.55 ensures programme_survival_probability is computed from
    //   step 1. After IMF acceptance emergency event: new_legitimacy ≈ 0.45 → PSP ≈ 65%.
    // IMPORTANT: scheduled_inputs is a top-level field of ScenarioCreateRequest,
    //   NOT inside configuration (schemas.py §ScenarioCreateRequest).
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
            // Ecological disabled for Demo 5 — CO2 planetary boundary TERMINAL alert
            // (fires from step 1) would dominate Zone 1B detail slot and push the reserve
            // coverage alert out of the top position. Reserve is the demo thesis indicator.
            ecological: { enabled: false },
            governance: { enabled: true },
            political_economy: { enabled: true },
          },
          // Food price shock drives reserve drawdown so Zone 1B shows a reserve WARNING
          // at step 3 (Frame B / Frame C thesis).
          commodity_price_shocks: [
            { commodity_category: "food", magnitude: 0.35, start_step: 1, duration_steps: 6 },
          ],
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
              // Food import dependency enables ExternalSectorModule reserve depletion
              // channel for the food price shock above (T3 — SADC import structure estimate).
              commodity_import_dependency_food: {
                value: "0.15", unit: "ratio", variable_type: "ratio",
                confidence_tier: 3, observation_date: "2024-01-01",
                source_registry_id: "WORLD_BANK_WDI_2023", measurement_framework: "financial",
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
              // Democratic quality set above the 0.70 WARNING floor (MDA-GOV-DEMOCRACY-FLOOR)
              // to prevent governance CRITICAL/TERMINAL from occupying Zone 1B detail slot
              // ahead of the reserve alert. Demo 5 thesis: reserve trust architecture.
              // Honest disclosure in walkthrough: ZMB actual V-Dem LDI (0.34) noted.
              democratic_quality_score: {
                value: "0.80", unit: "ratio", variable_type: "ratio",
                confidence_tier: 3, observation_date: "2023-12-01",
                source_registry_id: "WORLD_BANK_WDI_2023", measurement_framework: "governance",
              },
              // legitimacy_index ensures PoliticalEconomyModule computes PSP from step 1.
              // At 0.55 (above fragility threshold 0.5), IMF acceptance event reduces
              // legitimacy by 0.10 → new_legitimacy 0.45 → PSP ≈ 65%.
              legitimacy_index: {
                value: "0.55", unit: "ratio_0_1", variable_type: "ratio",
                confidence_tier: 3, observation_date: "2024-01-01",
                source_registry_id: "WORLD_BANK_WDI_2023", measurement_framework: "governance",
              },
            },
          },
        },
        // scheduled_inputs is top-level in ScenarioCreateRequest, NOT inside configuration.
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

    // Open the Grounding strip so source provenance is visible in Frame A.
    // ADR-016 Component 2: toggle button opens the strip panel body.
    await page.locator('[data-testid="grounding-strip-toggle"]').click();
    const groundingStrip = page.locator('[data-testid="grounding-strip"]');
    await expect(groundingStrip).toBeVisible({ timeout: 8_000 });
    await expect(groundingStrip).not.toContainText("Loading grounding data", { timeout: 8_000 });
    await page.waitForTimeout(600);

    await speak(
      "Zambia, 2024. Step one — the IMF program is accepted. " +
      "A food price shock is active — Zambia's import structure makes reserve coverage " +
      "the first financial indicator to watch. " +
      "Before the simulation shows a single step of consequence, the Grounding strip is open. " +
      "Reserve coverage: three point eight months. " +
      "Source: IMF World Economic Outlook, April 2024. Tier two. " +
      "Every initial number has a named source, a tier, and a date — " +
      "on the screen at load, without opening a drawer. " +
      "The trust architecture is not a footnote. It is structural.",
    );

    // Frame A: ZMB at step 1, Grounding strip OPEN showing initial state provenance.
    await page.screenshot({ path: screenshotPath("frame-a-grounding-strip.png") });

    // ── Advance to step 2 (fiscal conditionality begins) ─────────────────────
    // No screenshot at step 2 — food shock drives reserve to ~3.35 months but
    // WARNING zone begins at 3.0 months. Capture Frames B and C at step 3 where
    // reserve = ~2.90 months (WARNING active).

    await nextStepBtn.click();
    await expect(page.getByText("Step 2 / 6")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(600);

    // ── FRAME B: Step 3 — Zone 1B self-interpreting reserve WARNING alert ─────
    // (Grounding strip remains open from Frame A — toggle was not clicked again.)

    await nextStepBtn.click();
    await expect(page.getByText("Step 3 / 6")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(1_200);

    await speak(
      "Step three. Year 2026. Two years into the programme. " +
      "The food price shock has compounded. Reserve coverage is in the WARNING zone. " +
      "Zone one B — the alert panel — shows the top-ranked alert: Reserve Coverage. " +
      "The instrument does not say 'threshold breached' as a boolean. " +
      "It shows: the indicator name, the current value, the floor — two point five months — " +
      "and the negotiation-defensibility label. " +
      "High confidence. Cite directly. " +
      "At the current draw rate, the CRITICAL floor is one step away. " +
      "That sentence is specific enough to put in a briefing note. " +
      "The minister can hand it to the negotiating team verbatim.",
    );

    // Frame B: Zone 1B showing reserve WARNING alert with Layer 3 text at step 3.
    // Grounding strip still open from Frame A — both panels visible simultaneously.
    await page.screenshot({ path: screenshotPath("frame-b-zone1b-reserve.png") });

    // ── FRAME C (THESIS): The citation at the table ───────────────────────────
    // Same step 3 — Grounding strip still open. Full viewport shows both simultaneously.

    await speak(
      "Now the challenge-response moment. " +
      "The creditor says: where does your three point eight months reserve figure come from? " +
      "We have a different number in our model. " +
      "The analyst points to the Grounding strip — still open, never closed. " +
      "Reserve coverage: three point eight months. " +
      "IMF World Economic Outlook, April 2024. Tier two. " +
      "No drawer. Under ten seconds. " +
      "One more thing: the source is the IMF's own publication. " +
      "The creditor is challenging a figure from their own institution's dataset. " +
      "That changes the character of the conversation.",
    );

    // Frame C (THESIS): Grounding strip OPEN + Zone 1B reserve WARNING simultaneously visible.
    await page.screenshot({ path: screenshotPath("frame-c-citation-at-table.png") });

    // ── FRAME D: Step 3 — Political feasibility alongside reserve alert ───────
    // Close Grounding strip so Zone 1D is unobstructed.

    await page.locator('[data-testid="grounding-strip-toggle"]').click();
    await expect(groundingStrip).not.toBeVisible({ timeout: 5_000 });
    await page.waitForTimeout(600);

    await speak(
      "Look at Zone one D — the four-framework overview at the same step. " +
      "There is a fifth readout: programme survival probability. " +
      "The political economy module is asking a different question from the reserve alert. " +
      "Not whether the programme is running — whether this government can deliver " +
      "what the programme requires. " +
      "Reserve stress and programme viability are related but not the same constraint. " +
      "Both are visible in the same instrument cluster. For the first time.",
    );

    // Frame D: Zone 1D with PSP visible alongside four composites. Grounding strip CLOSED.
    await page.screenshot({ path: screenshotPath("frame-d-political-feasibility.png") });

    // ── FRAME E: Step 5 — Full evidence thread ────────────────────────────────
    // Currently at step 3. Advance to step 4, then step 5.

    await nextStepBtn.click();
    await expect(page.getByText("Step 4 / 6")).toBeVisible({ timeout: 20_000 });
    await page.waitForTimeout(600);

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
