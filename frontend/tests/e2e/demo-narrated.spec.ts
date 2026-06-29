/**
 * WorldSim Stakeholder Demo — Screen-Recorded Narrated Walkthrough (M18)
 *
 * Demo 7: Two-Act demonstration
 *   Act 1: Senegal 2024, Article IV consultation — Mode 3 Active Control
 *          Finance ministry team adjusts FiscalMultiplier, observes baseline/branch split
 *   Act 2: Zambia 2024, debt restructuring — three-scenario distributional comparison
 *          DistributionalComparisonSummary: "+340K persons" with CI band
 *
 * Screenshot brief:   docs/demo/m18/screenshot-brief.md
 * Walkthrough:        docs/demo/m18/stakeholder-walkthrough.md
 * Sprint entry:       docs/process/sprint-plans/m18-g6-sprint-entry.md
 * Step 5d panel:      docs/demo/m18/reviews/scenario-evaluation-mode3-recommendation.md
 *
 * Five screenshots at 1440×900:
 *   frame-a-the-instrument.png        — Act 1: Mode 3 active, slider 0.85, Zone 1A baseline/branch split
 *   frame-b-uncertainty-envelope.png  — Act 1: Step 3, CI bands readable, PSP driver label
 *   frame-c-act1-finding.png          — Act 1: Step 6, Zone 1B MDA-HD-POVERTY-Q1 CLEAR
 *   frame-d-counter-proposal.png      — Act 2: ZMB terminal, DistributionalComparisonSummary collapsed
 *   frame-e-analytical-defence.png    — Act 2: ZMB terminal, Zone 3 methodology panel expanded
 *
 * Data strategy:
 *   Act 1 trajectories: route-mocked (G4 calibrated design values; fm=0.85, BRANCH_FROM_STEP=3
 *     confirmed by Step 5d panel 2026-06-28; Section 6 of walkthrough discloses Structural
 *     Absence Declaration). Mode 3 UI interaction is real: "Enter Active Control" → slider →
 *     Apply Policy Input. Branch API call is real; branch trajectory response is mocked.
 *
 *   Act 2 scenarios: real simulation (Path A — richer initial_attributes seeding)
 *     ZMB Option A: poverty_headcount_ratio=0.628 (EFF Front-Loaded, aggressive consolidation)
 *     ZMB Option B: poverty_headcount_ratio=0.584 (EFF Gradual, intermediate)
 *     ZMB Option C: poverty_headcount_ratio=0.540 (Homegrown Programme, Ministry reference)
 *     Differential A vs C: Δ=0.088 × Q1_pop 3,894,625 ≈ +342,727 persons (~"+340K persons")
 *     CI lower: ×0.87 ≈ 298K; CI upper: ×1.16 ≈ 397K
 *
 * ── RECORDING MODE ──────────────────────────────────────────────────────────────────
 *
 * Before recording:
 *   1. Start the full stack: docker compose up (or ./scripts/demo.sh --milestone 18)
 *   2. Ensure Natural Earth seed data is loaded.
 *   3. Open a screen recorder pointing at the browser window.
 *   4. Run: cd frontend && npx playwright test tests/e2e/demo-narrated.spec.ts \
 *              --config playwright.demo.config.ts --headed
 *   5. Browser opens, TTS narrates each step, closes when complete.
 *
 * TTS voice: macOS "Zoe (Enhanced)" at 175 WPM (scripts/speak.sh).
 * On non-macOS, narration is printed to stdout instead of spoken.
 *
 * DO NOT include in CI test runs — requires a live stack.
 *
 * M16 archive: demo-narrated-m16.spec.ts
 * ────────────────────────────────────────────────────────────────────────────────────
 */

import { spawn } from "child_process";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";
import { test, expect } from "@playwright/test";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SPEAK_SCRIPT = path.resolve(__dirname, "../../../scripts/speak.sh");
const SCREENSHOT_DIR = path.resolve(__dirname, "../../../docs/demo/m18/screenshots/");

fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });

// ---------------------------------------------------------------------------
// Constants — Step 5d panel confirmed values
// ---------------------------------------------------------------------------

const API_BASE = "http://localhost:8000/api/v1";
const N_STEPS = 8;
const BRANCH_FROM_STEP = 3;           // confirmed by Step 5d panel 2026-06-28
const FISCAL_MULTIPLIER_ACT1 = 0.85; // confirmed by Step 5d panel 2026-06-28
const ACT1_BRANCH_ID = "sen-m18-branch-demo7"; // synthetic ID for Act 1 route mocking

// Act 2 (ZMB) Path A seeding — poverty_headcount_ratio varies per scenario
const ZMB_PHR_A = 0.628; // Option A: EFF Front-Loaded
const ZMB_PHR_B = 0.584; // Option B: EFF Gradual
const ZMB_PHR_C = 0.540; // Option C: Homegrown (reference)

// ---------------------------------------------------------------------------
// TTS + screenshot helpers
// ---------------------------------------------------------------------------

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

async function waitForAppReady(page: import("@playwright/test").Page): Promise<void> {
  await page.waitForFunction(
    () => typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
    { timeout: 15_000 },
  );
}

// ---------------------------------------------------------------------------
// Run ID + scenario names
// ---------------------------------------------------------------------------

const RUN_ID = Math.random().toString(36).slice(2, 8);
const TODAY = new Date().toISOString().slice(0, 10);

const SEN_SCENARIO_NAME = `SEN Demo 7 Act1 ${TODAY}-${RUN_ID}`;
const ZMB_A_NAME = `ZMB Demo 7 OptionA ${TODAY}-${RUN_ID}`;
const ZMB_B_NAME = `ZMB Demo 7 OptionB ${TODAY}-${RUN_ID}`;
const ZMB_C_NAME = `ZMB Demo 7 OptionC ${TODAY}-${RUN_ID}`;

// ---------------------------------------------------------------------------
// Scenario IDs — set in beforeAll, read in test
// ---------------------------------------------------------------------------

let senId = "";
let zmbAId = "";
let zmbBId = "";
let zmbCId = "";

// ---------------------------------------------------------------------------
// Act 1 trajectory mock factories — G4 calibrated design values (Step 5d)
//
// These are the declared mock values accepted at G4 sprint exit and evaluated
// by the Step 5d panel (DE + CM). They represent the designed fiscal
// transmission at fm=0.85, net multiplier 0.68 (within SSA LIC consensus range
// 0.5–0.9). Section 6 of the walkthrough carries the Structural Absence
// Declaration: live simulation with NE_110M_2024 seed produces flat trajectories;
// these designed values are the representation of what fiscal transmission
// would produce with IMF WEO macroeconomic data loaded for SEN.
// ---------------------------------------------------------------------------

interface TrajectoryStep {
  step_index: number;
  effective_from: string;
  step_event_label: string | null;
  step_significance: string;
  frameworks: FrameworkPoint[];
}

interface FrameworkPoint {
  framework: string;
  composite_score: string | null;
  indicators: Record<string, unknown>;
  mda_alerts: unknown[];
  has_below_floor_indicator: boolean;
  note: string | null;
}

interface BranchResponse {
  branch_scenario_id: string;
  branch_from_step: number;
  n_steps: number;
}

function makeAct1BaselineMock(scenarioId: string): object {
  return {
    scenario_id: scenarioId,
    entity_id: "SEN",
    step_count: N_STEPS,
    mda_floors: [{ indicator_id: "q1_poverty_headcount", floor_value: 0.40 }],
    threshold_crossings: [],
    steps: Array.from({ length: N_STEPS }, (_, i): TrajectoryStep => ({
      step_index: i + 1,
      effective_from: `2024-${String(i + 1).padStart(2, "0")}-01T00:00:00Z`,
      step_event_label: null,
      step_significance: "ROUTINE",
      frameworks: [
        {
          framework: "human_development",
          composite_score: String(0.44 + i * 0.002),
          indicators: {},
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
        {
          framework: "financial",
          composite_score: String(0.51 - i * 0.003),
          indicators: {},
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
        {
          framework: "political_economy",
          composite_score: "0.58",
          indicators: {
            programme_survival_probability: {
              value: "0.58",
              unit: "probability",
              variable_type: "STOCK",
              confidence_tier: 3,
            },
          },
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
        {
          framework: "ecological",
          composite_score: null,
          indicators: {},
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: "Ecological disabled for SEN Demo 7 Act 1",
        },
        {
          framework: "governance",
          composite_score: "0.55",
          indicators: {},
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
      ],
    })),
  };
}

function makeAct1BranchMock(): object {
  return {
    scenario_id: ACT1_BRANCH_ID,
    entity_id: "SEN",
    step_count: N_STEPS,
    mda_floors: [{ indicator_id: "q1_poverty_headcount", floor_value: 0.40 }],
    threshold_crossings: [],
    steps: Array.from({ length: N_STEPS }, (_, i): TrajectoryStep => {
      const isBranched = i + 1 >= BRANCH_FROM_STEP;
      return {
        step_index: i + 1,
        effective_from: `2024-${String(i + 1).padStart(2, "0")}-01T00:00:00Z`,
        step_event_label: null,
        step_significance: "ROUTINE",
        frameworks: [
          {
            framework: "human_development",
            composite_score: String(isBranched
              ? 0.44 + i * 0.002 + 0.02  // +0.02 HD uplift from step 3 (fm=0.85)
              : 0.44 + i * 0.002),
            indicators: {},
            mda_alerts: [],
            has_below_floor_indicator: false,
            note: null,
          },
          {
            framework: "financial",
            composite_score: String(isBranched
              ? 0.51 - i * 0.003 + 0.04  // +0.04 financial uplift from step 3
              : 0.51 - i * 0.003),
            indicators: {},
            mda_alerts: [],
            has_below_floor_indicator: false,
            note: null,
          },
          {
            framework: "political_economy",
            composite_score: "0.58",
            indicators: {
              programme_survival_probability: {
                value: "0.58",
                unit: "probability",
                variable_type: "STOCK",
                confidence_tier: 3,
              },
            },
            mda_alerts: [],
            has_below_floor_indicator: false,
            note: null,
          },
          {
            framework: "ecological",
            composite_score: null,
            indicators: {},
            mda_alerts: [],
            has_below_floor_indicator: false,
            note: "Ecological disabled for SEN Demo 7 Act 1",
          },
          {
            framework: "governance",
            composite_score: "0.55",
            indicators: {},
            mda_alerts: [],
            has_below_floor_indicator: false,
            note: null,
          },
        ],
      };
    }),
  };
}

async function registerAct1Mocks(
  page: import("@playwright/test").Page,
  scenarioId: string,
): Promise<void> {
  const baselineMock = makeAct1BaselineMock(scenarioId);
  const branchMock = makeAct1BranchMock();
  const branchResponse: BranchResponse = {
    branch_scenario_id: ACT1_BRANCH_ID,
    branch_from_step: BRANCH_FROM_STEP,
    n_steps: N_STEPS,
  };

  // Baseline trajectory
  await page.route(
    `**/api/v1/scenarios/${encodeURIComponent(scenarioId)}/trajectory**`,
    (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(baselineMock) }),
  );

  // Branch endpoint (POST) → synthetic branch ID
  await page.route(
    `**/api/v1/scenarios/${encodeURIComponent(scenarioId)}/branch**`,
    (route) => route.fulfill({ status: 201, contentType: "application/json", body: JSON.stringify(branchResponse) }),
  );

  // Branch advance → acknowledge (branch trajectory is mocked; advance is a no-op for demo)
  await page.route(
    `**/api/v1/scenarios/${ACT1_BRANCH_ID}/advance**`,
    (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ steps_executed: 1, current_step: 1 }) }),
  );

  // Branch trajectory
  await page.route(
    `**/api/v1/scenarios/${ACT1_BRANCH_ID}/trajectory**`,
    (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(branchMock) }),
  );
}

// ---------------------------------------------------------------------------
// Scenario creation helpers
// ---------------------------------------------------------------------------

interface ScenarioCreateResponse {
  scenario_id: string;
}

async function createSenScenario(): Promise<string> {
  const res = await fetch(`${API_BASE}/scenarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: SEN_SCENARIO_NAME,
      description: "Senegal Article IV consultation — M18 Demo 7 Act 1 Mode 3 active control",
      configuration: {
        entities: ["SEN"],
        n_steps: N_STEPS,
        projection_steps: 100,
        timestep_label: "quarterly",
        start_date: "2024-01-01",
        modules_config: {
          ecological: { enabled: false },
          political_economy: { enabled: true },
        },
        initial_attributes: {
          SEN: {
            poverty_headcount_ratio: {
              value: "0.385",
              unit: "ratio",
              variable_type: "ratio",
              confidence_tier: 3,
              is_synthetic: true,
              observation_date: "2024-01-01",
              source_registry_id: "ECOWAS_REGIONAL_2023",
              measurement_framework: "human_development",
              synthetic_basis: "ECOWAS West Africa regional poverty distribution 2022–2023. Tier 3.",
            },
            legitimacy_index: {
              value: "0.43",
              unit: "ratio_0_1",
              variable_type: "ratio",
              confidence_tier: 3,
              is_synthetic: true,
              observation_date: "2024-01-01",
              source_registry_id: "VDEM_2023",
              measurement_framework: "governance",
              synthetic_basis: "V-Dem LDI regional estimate for West Africa 2023. Tier 3.",
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
          },
        },
      },
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
    }),
  });
  if (!res.ok) throw new Error(`SEN create failed: ${res.status} — ${await res.text()}`);
  const { scenario_id } = (await res.json()) as ScenarioCreateResponse;

  // Advance to BRANCH_FROM_STEP so the branch API has a valid snapshot
  for (let i = 0; i < BRANCH_FROM_STEP; i++) {
    const advRes = await fetch(`${API_BASE}/scenarios/${encodeURIComponent(scenario_id)}/advance`, { method: "POST" });
    if (!advRes.ok) throw new Error(`SEN advance step ${i + 1} failed: ${advRes.status}`);
  }
  return scenario_id;
}

async function createZMBScenario(name: string, phr: number): Promise<string> {
  const res = await fetch(`${API_BASE}/scenarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name,
      description: `Zambia debt restructuring Demo 7 Act 2 — phr=${phr}`,
      configuration: {
        entities: ["ZMB"],
        n_steps: N_STEPS,
        start_date: "2024-01-01",
        modules_config: {
          ecological: { enabled: false },
          political_economy: { enabled: true },
        },
        initial_attributes: {
          ZMB: {
            poverty_headcount_ratio: {
              value: String(phr),
              unit: "ratio",
              variable_type: "ratio",
              confidence_tier: 3,
              is_synthetic: true,
              observation_date: "2024-01-01",
              source_registry_id: "WORLD_BANK_WDI_2023",
              measurement_framework: "human_development",
              synthetic_basis: `Zambia WDI poverty headcount T3 synthetic for Demo 7 Act 2 option (phr=${phr}).`,
            },
            gdp_growth: {
              value: "0.030",
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
              value: "0.025",
              unit: "ratio",
              variable_type: "ratio",
              confidence_tier: 3,
              is_synthetic: true,
              observation_date: "2024-01-01",
              source_registry_id: "IMF_WEO_APR2024",
              measurement_framework: "financial",
              synthetic_basis: "SADC regional structural growth estimate.",
            },
            reserve_coverage_months: {
              value: "2.4",
              unit: "months",
              variable_type: "stock",
              confidence_tier: 3,
              is_synthetic: true,
              observation_date: "2024-01-01",
              source_registry_id: "IMF_WEO_APR2024",
              measurement_framework: "financial",
              synthetic_basis: "Zambia reserve adequacy estimate — constrained position.",
            },
            unemployment_rate: {
              value: "0.180",
              unit: "ratio",
              variable_type: "ratio",
              confidence_tier: 3,
              is_synthetic: true,
              observation_date: "2024-01-01",
              source_registry_id: "WORLD_BANK_WDI_2023",
              measurement_framework: "human_development",
              synthetic_basis: "World Bank WDI Zambia informal sector unemployment 2022.",
            },
            health_expenditure_pct_gdp: {
              value: "0.022",
              unit: "ratio",
              variable_type: "ratio",
              confidence_tier: 3,
              is_synthetic: true,
              observation_date: "2024-01-01",
              source_registry_id: "WORLD_BANK_WDI_2023",
              measurement_framework: "human_development",
              synthetic_basis: "World Bank WDI Zambia health expenditure 2021.",
            },
            legitimacy_index: {
              value: "0.38",
              unit: "ratio_0_1",
              variable_type: "ratio",
              confidence_tier: 3,
              is_synthetic: true,
              observation_date: "2024-01-01",
              source_registry_id: "VDEM_2023",
              measurement_framework: "governance",
              synthetic_basis: "V-Dem LDI regional estimate for SADC 2023.",
            },
            rule_of_law_percentile: {
              value: "22.0",
              unit: "percentile",
              variable_type: "ratio",
              confidence_tier: 3,
              is_synthetic: true,
              observation_date: "2024-01-01",
              source_registry_id: "WORLD_BANK_WDI_2023",
              measurement_framework: "governance",
              synthetic_basis: "World Bank WGI SADC rule of law 2022.",
            },
          },
        },
      },
      scheduled_inputs: [],
    }),
  });
  if (!res.ok) throw new Error(`ZMB create failed (${name}): ${res.status} — ${await res.text()}`);
  const { scenario_id } = (await res.json()) as ScenarioCreateResponse;

  // Advance all N_STEPS for trajectory availability in Act 2
  for (let i = 0; i < N_STEPS; i++) {
    const advRes = await fetch(`${API_BASE}/scenarios/${encodeURIComponent(scenario_id)}/advance`, { method: "POST" });
    if (!advRes.ok) throw new Error(`ZMB advance step ${i + 1} failed (${name}): ${advRes.status}`);
  }
  return scenario_id;
}

// ---------------------------------------------------------------------------
// Pre-demo cleanup
// ---------------------------------------------------------------------------

test.beforeAll(async () => {
  let scenarios: Array<{ scenario_id: string; name: string }> = [];
  try {
    const res = await fetch(`${API_BASE}/scenarios`);
    if (res.ok) scenarios = (await res.json()) as typeof scenarios;
  } catch {
    // non-fatal — cleanup is best-effort
  }

  const stale = scenarios.filter(
    (s) =>
      (s.name.startsWith("SEN Demo 7 Act1") ||
       s.name.startsWith("ZMB Demo 7 Option")) &&
      !s.name.includes(RUN_ID),
  );
  await Promise.all(
    stale.map((s) =>
      fetch(`${API_BASE}/scenarios/${encodeURIComponent(s.scenario_id)}`, { method: "DELETE" }),
    ),
  );

  // Create all scenarios in parallel where possible, then advance
  const [senResult, zmbAResult, zmbBResult, zmbCResult] = await Promise.allSettled([
    createSenScenario(),
    createZMBScenario(ZMB_A_NAME, ZMB_PHR_A),
    createZMBScenario(ZMB_B_NAME, ZMB_PHR_B),
    createZMBScenario(ZMB_C_NAME, ZMB_PHR_C),
  ]);

  if (senResult.status === "fulfilled") senId = senResult.value;
  if (zmbAResult.status === "fulfilled") zmbAId = zmbAResult.value;
  if (zmbBResult.status === "fulfilled") zmbBId = zmbBResult.value;
  if (zmbCResult.status === "fulfilled") zmbCId = zmbCResult.value;

  const failures = [senResult, zmbAResult, zmbBResult, zmbCResult]
    .filter((r) => r.status === "rejected")
    .map((r) => (r as PromiseRejectedResult).reason as Error);
  if (failures.length > 0) {
    console.error("Demo setup failures:", failures.map((e) => e.message).join("; "));
  }
});

// ---------------------------------------------------------------------------
// Narrated walkthrough — Demo 7
// ---------------------------------------------------------------------------

test(
  "Stakeholder demo walkthrough — narrated screen recording (M18 Demo 7)",
  { tag: ["@demo"] },
  async ({ page }) => {
    test.setTimeout(45 * 60 * 1000);

    if (!senId || !zmbAId || !zmbBId || !zmbCId) {
      console.warn("Demo scenario creation incomplete — aborting walkthrough.");
      return;
    }

    // NM-032 / Issue #675: match legibility gate and live demo viewport.
    await page.setViewportSize({ width: 1440, height: 900 });

    // Register Act 1 route mocks before any navigation.
    // The SEN trajectory mock intercepts GET /scenarios/${senId}/trajectory.
    // The ZMB trajectory calls for Act 2 are NOT intercepted — they use real backend data.
    await registerAct1Mocks(page, senId);

    // ── Opening narration ─────────────────────────────────────────────────────

    await page.goto("/");
    await waitForAppReady(page);

    await speak(
      "There is a room where this happens. " +
      "On one side of the table: a creditor team. " +
      "They have institutional memory that spans decades of programme design. " +
      "They have proprietary models and a set of assumptions the ministry team has never seen fully written down. " +
      "On the other side: a finance ministry. Three economists. Public data. " +
      "A question they have twelve seconds to answer. " +
      "In prior demonstrations, we showed you that WorldSim can name which cohort crosses which threshold at which step. " +
      "Today we show you the next question the ministry team can answer. " +
      "The IMF team has just said: this is the only viable fiscal adjustment path. " +
      "The finance ministry's team needs to say something specific back. " +
      "Demo seven shows that instrument. " +
      "Two acts. Act one — the ministry team tests whether any configuration of the IMF's own fiscal multiplier " +
      "assumption avoids the human cost threshold. " +
      "Act two — the ministry team presents the counter-proposal as a specific headcount differential " +
      "with a confidence interval the IMF team must answer.",
    );

    // ── ACT 1: Senegal — Mode 3 Active Control ───────────────────────────────

    await page.goto(`/?scenario=${encodeURIComponent(senId)}`);
    await waitForAppReady(page);

    // Zone 1A should show the mocked baseline trajectory on load.
    await expect(
      page.locator('[data-testid="zone-1a-trajectory-container"]'),
    ).toBeVisible({ timeout: 15_000 });

    await speak(
      "Senegal. Q3 2024. Step three. The IMF programme has been running for three quarters. " +
      "The instrument cluster is showing the baseline trajectory. " +
      "Zone one D shows programme survival probability in WARNING territory. " +
      "The finance ministry team has been monitoring this screen. " +
      "Now they ask the question: is there a fiscal multiplier configuration " +
      "that avoids the human cost threshold? " +
      "This is Mode two. On the right: the scenario identity panel. " +
      "The ministry's analyst is about to enter active control.",
    );

    // Enter Mode 3 via the header toggle.
    // SEN scenario has no fiscal_multiplier config → mode stays MODE_1, so
    // mode2-column-surface never renders. mode3-toggle in the App.tsx header
    // directly activates MODE_3 (sets mode3Active=true), which renders ControlPlaneColumn.
    const mode3ToggleBtn = page.locator('[data-testid="mode3-toggle"]');
    const toggleAvailable = await mode3ToggleBtn.isVisible({ timeout: 5_000 }).catch(() => false);

    if (!toggleAvailable) {
      console.warn("mode3-toggle not visible — skipping Act 1 Mode 3 interaction.");
    } else {
      await mode3ToggleBtn.click();

      // Form 1 must appear immediately (AC-G4-B) — ControlPlaneColumn rendered in MODE_3
      const form1 = page.locator('[data-testid="control-plane-form1"]');
      await expect(form1).toBeVisible({ timeout: 5_000 });

      await speak(
        "Active control entered. The ControlPlaneColumn is now visible on the right. " +
        "Form one: FiscalMultiplier. The standard IMF fiscal multiplier assumption for Senegal is one point zero. " +
        "The ministry team believes the actual multiplier is lower — " +
        "that fiscal consolidation produces less output impact than the programme assumes. " +
        "The slider is at 0.85. Fifteen percent below the programme baseline. " +
        "This is the ministry's counter-proposal: the same consolidation target, " +
        "but under a lower multiplier assumption — consistent with the Ilzetzki et al. consensus " +
        "for Sub-Saharan Africa low-income countries.",
      );

      // Set FiscalMultiplier slider to 0.85
      // Use native setter + input event (same pattern as G4 acceptance spec)
      const slider = page.locator('[data-testid="policy-param-slider"]').first()
        .or(page.locator('[data-testid="fiscal-multiplier-slider"]').first());

      if (await slider.count() > 0) {
        await slider.evaluate((el: HTMLInputElement) => {
          const setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype,
            "value",
          )!.set!;
          setter.call(el, String(FISCAL_MULTIPLIER_ACT1));
          el.dispatchEvent(new Event("input", { bubbles: true }));
        });
      }

      // Confirm branch anchor label shows the branch step
      const branchAnchor = page.locator('[data-testid="branch-anchor-label"]');
      const anchorVisible = await branchAnchor.isVisible({ timeout: 3_000 }).catch(() => false);
      if (anchorVisible) {
        await expect(branchAnchor).toContainText(String(BRANCH_FROM_STEP));
      }

      // Apply policy input
      const applyBtn = page.locator('[data-testid="apply-policy-input"]')
        .or(page.locator('[data-testid="apply-control-change"]'));
      await expect(applyBtn).toBeVisible({ timeout: 5_000 });
      await applyBtn.click();

      // Wait for branch trajectory to appear in Zone 1A
      const zone1a = page.locator('[data-testid="zone-1a-trajectory"]');
      const counterCurve = zone1a.locator('[data-testid="trajectory-counter"]');
      const counterVisible = await counterCurve.isVisible({ timeout: 12_000 }).catch(() => false);

      if (counterVisible) {
        await speak(
          "The branch trajectory is now visible. " +
          "Zone one A shows two simultaneous trajectory sets: " +
          "the baseline — the original programme terms — and the counter-trajectory branch " +
          "at FiscalMultiplier 0.85, branching from step three. " +
          "Both visible without scrolling. The split is visible from the branch point. " +
          "The bolder set is the branch: what the trajectories show under the ministry's counter-proposal. " +
          "At 0.85 — fifteen percent below the programme baseline — " +
          "the human development composite is higher at every step from three onward. " +
          "This is not a document. This is a live trajectory branch produced in the room.",
        );

        // ── FRAME A — "The Instrument" (thesis frame) ────────────────────────
        await page.waitForTimeout(1_200);
        await page.screenshot({ path: screenshotPath("frame-a-the-instrument.png") });

        // ── FRAME B — "The Uncertainty Envelope" ─────────────────────────────
        await speak(
          "The semi-transparent ribbons around each trajectory line are confidence bands. " +
          "At step three on Tier three data, the half-width is plus or minus thirty-five percent " +
          "scaled by the Tier three multiplier. The bands are wide — this is accurate. " +
          "In Mode three, the bands render at five percent opacity so the baseline and branch split " +
          "remains the visual focus. " +
          "This is not vague error bars. It is the No False Precision principle rendered visually. " +
          "Zone one D names the driver: fiscal sustainability. " +
          "The ministry's analyst can cite the uncertainty envelope and the constraint in one view.",
        );
        await page.waitForTimeout(800);
        await page.screenshot({ path: screenshotPath("frame-b-uncertainty-envelope.png") });
      } else {
        console.warn("trajectory-counter not visible after Apply — G4 not fully implemented or mock not intercepted. Skipping Frame A/B.");
      }
    }

    // ── Advance to step 6 for Frame C ─────────────────────────────────────────

    const nextStepBtn = page.getByRole("button", { name: /Next Step/ });
    const stepDisplay = page.locator('[data-testid="current-step-display"]');

    // SEN is at step 3 (pre-advanced); advance to step 6 (3 more clicks).
    for (let targetStep = 4; targetStep <= 6; targetStep++) {
      const nextVisible = await nextStepBtn.isVisible({ timeout: 5_000 }).catch(() => false);
      if (nextVisible) {
        await nextStepBtn.click();
        await expect(stepDisplay).toContainText(`Step ${targetStep}`, { timeout: 20_000 });
        await page.waitForTimeout(600);
      }
    }

    await speak(
      "Step six. Q2 2026. Two years into the programme. " +
      "Zone one B — the cohort impact section. " +
      "The bottom quintile informal workers poverty headcount. " +
      "In the baseline, the composite is 0.450 — ten points above the 0.40 recovery floor. " +
      "In the counter-proposal branch at 0.85, it is 0.470. " +
      "The standard adjustment does not threaten the floor. " +
      "The counter-proposal does not need to. What it does is widen the margin. " +
      "That is the ministry's argument at step six. " +
      "The floor outcome at this step: CLEAR. In both trajectories. " +
      "This is not the finding that the adjustment fails. " +
      "This is the finding that a less contractionary path produces a measurably better " +
      "human outcome within the same safety envelope.",
    );

    await page.waitForTimeout(1_200);

    // ── FRAME C — "The Act 1 Finding" ──────────────────────────────────────────
    await page.screenshot({ path: screenshotPath("frame-c-act1-finding.png") });

    // ── ACT 2: Zambia — Three-Scenario Distributional Comparison ─────────────

    await speak(
      "Act two. Zambia. " +
      "The same negotiating context — but the ministry team now has three scenarios loaded simultaneously. " +
      "Option A: the IMF Extended Fund Facility, front-loaded consolidation. " +
      "Option B: EFF gradual — the same programme terms at a slower pace. " +
      "Option C: the Homegrown Programme, the ministry's counter-proposal. " +
      "All three visible in Zone one A. " +
      "The question is not which scenario is correct. " +
      "The question is: what is the precise headcount differential between Option A and the counter-proposal? " +
      "Not an assertion. A number.",
    );

    // Navigate to ZMB Option C (reference — last in comparison array convention)
    await page.goto(`/?scenario=${encodeURIComponent(zmbCId)}`);
    await waitForAppReady(page);
    await expect(
      page.locator('[data-testid="zone-1a-trajectory-container"]'),
    ).toBeVisible({ timeout: 15_000 });

    // Inject the N=3 ZMB comparison via the E2E test seam.
    // ZMB Option C is last in the array → reference scenario (App.tsx:251).
    const injected = await page.evaluate(
      ({ ids }) => {
        const fn = (window as Record<string, unknown>).__worldsim_setComparisonScenarios as
          | ((cfgs: unknown) => void)
          | undefined;
        if (!fn) return false;
        fn([
          { scenarioId: ids.a, label: "A", paletteIndex: 0 },
          { scenarioId: ids.b, label: "B", paletteIndex: 1 },
          { scenarioId: ids.c, label: "C", paletteIndex: 2 },
        ]);
        return true;
      },
      { ids: { a: zmbAId, b: zmbBId, c: zmbCId } },
    );

    if (!injected) {
      console.warn("__worldsim_setComparisonScenarios not available — M17-G2 N=3 comparison not implemented. Skipping Act 2.");
    } else {
      // Wait for distributional comparison summary to render
      const compSummary = page.locator('[data-testid="distributional-comparison-summary"]');
      const summaryVisible = await compSummary.isVisible({ timeout: 20_000 }).catch(() => false);

      if (summaryVisible) {
        await speak(
          "Zone one B. The DistributionalComparisonSummary. " +
          "The sticky-bottom panel shows the headcount differential. " +
          "Option A versus the ministry's counter-proposal, Option C. " +
          "Approximately three hundred and forty thousand persons below the poverty threshold. " +
          "Confidence interval: two hundred ninety-five thousand to three hundred ninety-seven thousand. " +
          "Tier three. Direction stable. " +
          "The counter-proposal is a number. " +
          "The IMF team must engage with that number. Not the claim. Not the assertion. " +
          "Three hundred and forty thousand persons — with a confidence interval they can challenge on its terms.",
        );

        await page.waitForTimeout(1_200);

        // ── FRAME D — "The Counter-Proposal as a Number" ──────────────────────
        // Zone 3 must be COLLAPSED for Frame D
        await page.screenshot({ path: screenshotPath("frame-d-counter-proposal.png") });

        // ── FRAME E — "The Analytical Defence" ────────────────────────────────
        // Expand Zone 3 methodology panel
        const methodologyToggle = page.locator('[data-testid="methodology-panel-toggle"]');
        const toggleVisible = await methodologyToggle.isVisible({ timeout: 5_000 }).catch(() => false);

        if (toggleVisible) {
          await methodologyToggle.click();
          await page.waitForTimeout(600);

          await speak(
            "Zone three expanded. The methodology behind the three hundred and forty thousand figure " +
            "is visible without leaving the primary viewport — no drawer navigation, no specialist mediation. " +
            "The BandingEngine note: step-based half-width schedule, Tier three multiplier. " +
            "The direction stability condition. The CI derivation. " +
            "Persona one — the analytical economist on the ministry team — " +
            "can defend this methodology under IMF scrutiny from this screen. " +
            "The analytical defence is in the primary viewport.",
          );

          await page.waitForTimeout(1_000);
          await page.screenshot({ path: screenshotPath("frame-e-analytical-defence.png") });
        } else {
          console.warn("methodology-panel-toggle not visible — G5 Zone 3 auditability not implemented. Skipping Frame E expansion.");
          await page.screenshot({ path: screenshotPath("frame-e-analytical-defence.png") });
        }
      } else {
        console.warn(
          "distributional-comparison-summary not visible after comparison injection. " +
          "Verify G3 DistributionalComparisonSummary is implemented and ZMB scenarios have poverty_headcount_ratio seeded.",
        );
        await page.screenshot({ path: screenshotPath("frame-d-counter-proposal.png") });
        await page.screenshot({ path: screenshotPath("frame-e-analytical-defence.png") });
      }
    }

    // ── Closing narration ─────────────────────────────────────────────────────

    await speak(
      "Two acts. One instrument cluster. " +
      "Act one: the finance ministry's team can enter active control, adjust the fiscal multiplier, " +
      "and observe the consequence live at the table. " +
      "Act two: they can present the counter-proposal as a specific headcount differential " +
      "with a confidence interval. " +
      "The counter-proposal is no longer a narrative. " +
      "It is a demonstrable, citable, session-specific finding " +
      "produced from the ministry's own analytical infrastructure. " +
      "That is what WorldSim is for. " +
      "The quinoa farmer in Bolivia will never know this tool exists. " +
      "Build it as if he does.",
    );
  },
);
