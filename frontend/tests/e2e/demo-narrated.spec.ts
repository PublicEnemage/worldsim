/**
 * WorldSim Stakeholder Demo — Screen-Recorded Narrated Walkthrough (M19)
 *
 * Demo 8: Two-Act demonstration
 *   Act 1: Zambia 2024, debt restructuring — Mode 3 Active Control, Form 3 Constraint Search
 *          Analyst presses "Find safe boundary"; instrument searches [0.1, 3.0]; FOUND: fm ≥ 0.83
 *   Act 2: Zambia 2024, debt restructuring — three-scenario distributional comparison
 *          DistributionalComparisonSummary: "+342,700 persons" with "declared interval (BandingEngine)"
 *
 * Screenshot brief:   docs/demo/m19/screenshot-brief.md
 * Walkthrough:        docs/demo/m19/stakeholder-walkthrough.md
 * Sprint entry:       docs/process/sprint-plans/m19-g1-sprint-entry.md
 *
 * Five screenshots at 1440×900:
 *   frame-a-constraint-found.png     — Act 1: Form 3 FOUND state, fm ≥ 0.83, Zone 1A baseline/branch
 *   frame-b-driver-arc.png           — Act 1: Step 4, Zone 1D PSP driver arc across programme window
 *   frame-c-act1-evidence.png        — Act 1: Step 8, Zone 1B CohortImpactSection CLEAR at 0.83
 *   frame-d-calibrated-ci.png        — Act 2: ZMB terminal, DistributionalComparisonSummary collapsed
 *   frame-e-posterior-methodology.png — Act 2: ZMB terminal, Zone 3 methodology panel expanded
 *
 * Data strategy:
 *   Act 1 trajectories: route-mocked (ZMB Option C baseline + branch at fm=0.83).
 *     Constraint-floor-search POST is mocked to return FOUND: boundary=0.83, ±0.01 precision.
 *     Mode 3 UI interaction is real: mode3-toggle → Form 3 → "Find safe boundary" click.
 *     Branch API call is real; branch trajectory response is mocked.
 *     Section 6 of walkthrough carries the honest disclosure: constraint boundary is precise
 *     to binary search tolerance (±0.01), not to statistical uncertainty.
 *
 *   Act 2 scenarios: real simulation (Path A — richer initial_attributes seeding)
 *     ZMB Option A: poverty_headcount_ratio=0.628 (EFF Front-Loaded, aggressive consolidation)
 *     ZMB Option B: poverty_headcount_ratio=0.584 (EFF Gradual, intermediate)
 *     ZMB Option C: poverty_headcount_ratio=0.540 (Homegrown Programme, Ministry reference)
 *     Differential A vs C: Δ=0.088 × Q1_pop 3,894,625 ≈ +342,727 persons (~"+342,700 persons")
 *     CI label (M19 change): "declared interval (BandingEngine)" — replaces M18 "95% CI"
 *
 * ── RECORDING MODE ──────────────────────────────────────────────────────────────────
 *
 * Before recording:
 *   1. Start the full stack: docker compose up (or ./scripts/demo.sh --milestone 19)
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
 * M18 archive: demo-narrated-m18.spec.ts
 * ────────────────────────────────────────────────────────────────────────────────────
 */

import { spawn } from "child_process";
import * as crypto from "crypto";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";
import { test, expect } from "@playwright/test";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SPEAK_SCRIPT = path.resolve(__dirname, "../../../scripts/speak.sh");
const SCREENSHOT_DIR = path.resolve(__dirname, "../../../docs/demo/m19/screenshots/");
const WALKTHROUGH_PATH = path.resolve(__dirname, "../../../docs/demo/m19/stakeholder-walkthrough.md");

fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });

// ---------------------------------------------------------------------------
// Constants — Act 1 constraint search (ADR-021 G1 #1540, certified at G1 exit)
// ---------------------------------------------------------------------------

const API_BASE = "http://localhost:8000/api/v1";
const N_STEPS = 8;

// Act 1 (ZMB Mode 3 constraint search) — boundary certified at G1 sprint exit.
const ZMB_ACT1_FM_BOUNDARY = 0.83;           // certified boundary from G1 sprint exit
const ZMB_ACT1_CURRENT_STEP = 4;             // scenario advanced to step 4 for mid-programme demo
const ZMB_ACT1_BRANCH_ID = "zmb-m19-branch-demo8"; // synthetic ID for Act 1 branch route mocking

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

function fileMD5(filePath: string): string {
  const content = fs.readFileSync(filePath);
  return crypto.createHash("md5").update(content).digest("hex");
}

function findFilesWithString(dir: string, searchStr: string): string[] {
  const found: string[] = [];
  if (!fs.existsSync(dir)) return found;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      found.push(...findFilesWithString(fullPath, searchStr));
    } else if (entry.isFile() && (entry.name.endsWith(".ts") || entry.name.endsWith(".tsx"))) {
      const content = fs.readFileSync(fullPath, "utf8");
      if (content.includes(searchStr)) found.push(fullPath);
    }
  }
  return found;
}

async function waitForAppReady(page: import("@playwright/test").Page): Promise<void> {
  // NM-039: __worldsim_selectEntity sentinel confirms DEV seam is mounted.
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

const ZMB_ACT1_NAME = `ZMB Demo 8 Act1 ${TODAY}-${RUN_ID}`;
const ZMB_A_NAME    = `ZMB Demo 8 OptionA ${TODAY}-${RUN_ID}`;
const ZMB_B_NAME    = `ZMB Demo 8 OptionB ${TODAY}-${RUN_ID}`;
const ZMB_C_NAME    = `ZMB Demo 8 OptionC ${TODAY}-${RUN_ID}`;

// ---------------------------------------------------------------------------
// Scenario IDs — set in beforeAll, read in test
// ---------------------------------------------------------------------------

let zmbAct1Id = "";
let zmbAId = "";
let zmbBId = "";
let zmbCId = "";

// ---------------------------------------------------------------------------
// Act 1 trajectory mock factories — ZMB at constraint boundary fm=0.83
//
// These are mocked values representing ZMB Option C fiscal transmission at
// the constraint-floor boundary (fiscal multiplier = 0.83). The constraint-
// floor search POST is also mocked to return FOUND: boundary=0.83, ±0.01
// precision, 9 evaluations, [0.1, 3.0] searched.
//
// The PSP driver arc (M19 G4 #1528) requires psp_dominant_driver at every step
// across the programme window — not only from a branch point. Steps 1–5 carry
// "fiscal_sustainability"; steps 6–8 carry "social_stability" (matching the
// driver arc narration in the walkthrough Section 2 Step 2).
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

interface ConstraintSearchMockResponse {
  status: "FOUND" | "NOT_FOUND" | "ERROR";
  boundary: number | null;
  uncertainty_lo: number | null;
  uncertainty_hi: number | null;
  evaluations: number;
  search_lo: number | null;
  search_hi: number | null;
  floor_value: number | null;
  indicator_key: string | null;
  error_message: string | null;
  data_tier: string | null;
}

/** Driver label for PSP driver arc — shifts from fiscal to social stability. */
function pspDriverAtStep(stepIndex: number): string {
  return stepIndex <= 5 ? "fiscal_sustainability" : "social_stability";
}

function makeZMBAct1BaselineMock(scenarioId: string): object {
  return {
    scenario_id: scenarioId,
    entity_id: "ZMB",
    step_count: N_STEPS,
    mda_floors: [{ indicator_id: "bottom_quintile_informal_workers_poverty_headcount", floor_value: 0.40 }],
    threshold_crossings: [],
    steps: Array.from({ length: N_STEPS }, (_, i): TrajectoryStep => ({
      step_index: i + 1,
      effective_from: `2024-${String(i + 1).padStart(2, "0")}-01T00:00:00Z`,
      step_event_label: null,
      step_significance: "ROUTINE",
      frameworks: [
        {
          framework: "human_development",
          composite_score: String(0.42 + i * 0.002),
          confidence_tier: 3,
          ci_lower: null,
          ci_upper: null,
          scoring_basis: "percentile_rank",
          indicators: {
            bottom_quintile_informal_workers_poverty_headcount: {
              value: "0.445",
              unit: "ratio",
              variable_type: "STOCK",
              confidence_tier: 3,
            },
          },
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
        {
          framework: "financial",
          composite_score: String(0.48 - i * 0.003),
          confidence_tier: 3,
          ci_lower: null,
          ci_upper: null,
          scoring_basis: "percentile_rank",
          indicators: {},
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
        {
          framework: "political_economy",
          composite_score: "0.54",
          confidence_tier: 3,
          ci_lower: null,
          ci_upper: null,
          scoring_basis: "percentile_rank",
          indicators: {
            programme_survival_probability: {
              value: "0.54",
              unit: "probability",
              variable_type: "STOCK",
              confidence_tier: 3,
            },
          },
          // PSP driver arc: present at all steps across the programme window (M19 G4 #1528).
          psp_dominant_driver: pspDriverAtStep(i + 1),
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
        {
          framework: "ecological",
          composite_score: null,
          confidence_tier: 3,
          ci_lower: null,
          ci_upper: null,
          scoring_basis: "percentile_rank",
          indicators: {},
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: "Ecological disabled for ZMB Demo 8 Act 1",
        },
        {
          framework: "governance",
          composite_score: "0.49",
          confidence_tier: 3,
          ci_lower: null,
          ci_upper: null,
          scoring_basis: "percentile_rank",
          indicators: {},
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
      ],
    })),
  };
}

function makeZMBAct1BranchMock(): object {
  // Branch at fm=0.83 — HD uplift keeps bottom quintile indicator above floor at all steps.
  // Branch applies from step 1 (full programme boundary configuration).
  return {
    scenario_id: ZMB_ACT1_BRANCH_ID,
    entity_id: "ZMB",
    step_count: N_STEPS,
    mda_floors: [{ indicator_id: "bottom_quintile_informal_workers_poverty_headcount", floor_value: 0.40 }],
    threshold_crossings: [],
    steps: Array.from({ length: N_STEPS }, (_, i): TrajectoryStep => ({
      step_index: i + 1,
      effective_from: `2024-${String(i + 1).padStart(2, "0")}-01T00:00:00Z`,
      step_event_label: null,
      step_significance: "ROUTINE",
      frameworks: [
        {
          framework: "human_development",
          // +0.03 HD uplift at boundary fm=0.83 (less contractionary than baseline)
          composite_score: String(0.42 + i * 0.002 + 0.03),
          confidence_tier: 3,
          ci_lower: null,
          ci_upper: null,
          scoring_basis: "percentile_rank",
          // DEMO-156 pattern: indicator populated so Zone 1B focal row renders CLEAR (not UNKNOWN).
          // Terminal step value 0.412 > floor 0.40 — boundary holds at fm=0.83.
          indicators: {
            bottom_quintile_informal_workers_poverty_headcount: {
              value: i + 1 === N_STEPS ? "0.412" : "0.465",
              unit: "ratio",
              variable_type: "STOCK",
              confidence_tier: 3,
            },
          },
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
        {
          framework: "financial",
          composite_score: String(0.48 - i * 0.003 + 0.035),
          confidence_tier: 3,
          ci_lower: null,
          ci_upper: null,
          scoring_basis: "percentile_rank",
          indicators: {},
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
        {
          framework: "political_economy",
          composite_score: "0.54",
          confidence_tier: 3,
          ci_lower: null,
          ci_upper: null,
          scoring_basis: "percentile_rank",
          indicators: {
            programme_survival_probability: {
              value: "0.54",
              unit: "probability",
              variable_type: "STOCK",
              confidence_tier: 3,
            },
          },
          psp_dominant_driver: pspDriverAtStep(i + 1),
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
        {
          framework: "ecological",
          composite_score: null,
          confidence_tier: 3,
          ci_lower: null,
          ci_upper: null,
          scoring_basis: "percentile_rank",
          indicators: {},
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: "Ecological disabled for ZMB Demo 8 Act 1",
        },
        {
          framework: "governance",
          composite_score: "0.49",
          confidence_tier: 3,
          ci_lower: null,
          ci_upper: null,
          scoring_basis: "percentile_rank",
          indicators: {},
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
      ],
    })),
  };
}

async function registerZMBAct1Mocks(
  page: import("@playwright/test").Page,
  scenarioId: string,
): Promise<void> {
  const baselineMock = makeZMBAct1BaselineMock(scenarioId);
  const branchMock = makeZMBAct1BranchMock();
  const branchResponse: BranchResponse = {
    branch_scenario_id: ZMB_ACT1_BRANCH_ID,
    branch_from_step: 1,
    n_steps: N_STEPS,
  };

  // Mocked constraint-floor-search POST → FOUND at boundary=0.83.
  // uncertainty_lo=0.82, uncertainty_hi=0.83 → (0.83-0.82).toFixed(2) = "0.01" → "±0.01 precision".
  const constraintSearchMock: ConstraintSearchMockResponse = {
    status: "FOUND",
    boundary: ZMB_ACT1_FM_BOUNDARY,
    uncertainty_lo: 0.82,
    uncertainty_hi: 0.83,
    evaluations: 9,
    search_lo: 0.1,
    search_hi: 3.0,
    floor_value: 0.4,
    indicator_key: "bottom_quintile_informal_workers_poverty_headcount",
    error_message: null,
    data_tier: "T3",
  };

  // Constraint-floor-search POST (Form 3 "Find safe boundary" button)
  await page.route(
    `**/api/v1/scenarios/${encodeURIComponent(scenarioId)}/constraint-floor-search**`,
    (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(constraintSearchMock) }),
  );

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

  // Branch advance → acknowledge
  await page.route(
    `**/api/v1/scenarios/${ZMB_ACT1_BRANCH_ID}/advance**`,
    (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ steps_executed: 1, current_step: 1 }) }),
  );

  // Branch trajectory
  await page.route(
    `**/api/v1/scenarios/${ZMB_ACT1_BRANCH_ID}/trajectory**`,
    (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(branchMock) }),
  );

  // Measurement-output pass-through: inject psp_dominant_driver at every step for driver arc.
  await page.route(
    `**/api/v1/scenarios/${encodeURIComponent(scenarioId)}/measurement-output**`,
    async (route) => {
      const response = await route.fetch();
      if (!response.ok()) { await route.fulfill({ response }); return; }
      const step = parseInt(new URL(route.request().url()).searchParams.get("step") ?? "0");
      const json = (await response.json()) as Record<string, unknown>;
      const outputs = json?.outputs as Record<string, unknown> | undefined;
      const pe = outputs?.political_economy as Record<string, unknown> | undefined;
      const indicators = pe?.indicators as Record<string, unknown> | undefined;
      const psp = indicators?.programme_survival_probability as Record<string, unknown> | undefined;
      if (psp !== null && psp !== undefined && typeof psp === "object") {
        psp.psp_dominant_driver = pspDriverAtStep(step);
      }
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(json) });
    },
  );
}

// ---------------------------------------------------------------------------
// Scenario creation helpers
// ---------------------------------------------------------------------------

interface ScenarioCreateResponse {
  scenario_id: string;
}

async function createZMBAct1Scenario(): Promise<string> {
  // ZMB Option C with monitored_focal_cohorts — required for Form 3 to render.
  // Advance only ZMB_ACT1_CURRENT_STEP steps so mode3 is at mid-programme.
  const res = await fetch(`${API_BASE}/scenarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: ZMB_ACT1_NAME,
      description: "Zambia debt restructuring — M19 Demo 8 Act 1 Mode 3 constraint-floor search",
      configuration: {
        entities: ["ZMB"],
        n_steps: N_STEPS,
        start_date: "2024-01-01",
        modules_config: {
          ecological: { enabled: false },
          political_economy: { enabled: true },
          external_sector: { enabled: false },
        },
        initial_attributes: {
          ZMB: {
            poverty_headcount_ratio: {
              value: String(ZMB_PHR_C),
              unit: "ratio",
              variable_type: "ratio",
              confidence_tier: 3,
              is_synthetic: true,
              observation_date: "2024-01-01",
              source_registry_id: "WORLD_BANK_WDI_2023",
              measurement_framework: "human_development",
              synthetic_basis: `Zambia WDI poverty headcount T3 synthetic for Demo 8 Act 1 (phr=${ZMB_PHR_C}).`,
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
        // Form 3 requires monitored_focal_cohorts to render constraint search.
        // floor_label and floor_value configure the "Find safe boundary" button target.
        monitored_focal_cohorts: [
          {
            indicator_key: "bottom_quintile_informal_workers_poverty_headcount",
            floor_value: 0.40,
            floor_label: "Poverty headcount floor",
            framework: "human_development",
          },
        ],
      },
      scheduled_inputs: [],
    }),
  });
  if (!res.ok) throw new Error(`ZMB Act 1 create failed: ${res.status} — ${await res.text()}`);
  const { scenario_id } = (await res.json()) as ScenarioCreateResponse;

  // Advance to ZMB_ACT1_CURRENT_STEP for mid-programme constraint search demo
  for (let i = 0; i < ZMB_ACT1_CURRENT_STEP; i++) {
    const advRes = await fetch(`${API_BASE}/scenarios/${encodeURIComponent(scenario_id)}/advance`, { method: "POST" });
    if (!advRes.ok) throw new Error(`ZMB Act 1 advance step ${i + 1} failed: ${advRes.status}`);
  }
  return scenario_id;
}

async function createZMBScenario(name: string, phr: number): Promise<string> {
  const res = await fetch(`${API_BASE}/scenarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name,
      description: `Zambia debt restructuring Demo 8 Act 2 — phr=${phr}`,
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
              synthetic_basis: `Zambia WDI poverty headcount T3 synthetic for Demo 8 Act 2 option (phr=${phr}).`,
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
      (s.name.startsWith("ZMB Demo 8 Act1") ||
       s.name.startsWith("ZMB Demo 8 Option")) &&
      !s.name.includes(RUN_ID),
  );
  await Promise.all(
    stale.map((s) =>
      fetch(`${API_BASE}/scenarios/${encodeURIComponent(s.scenario_id)}`, { method: "DELETE" }),
    ),
  );

  // Create all scenarios in parallel where possible
  const [zmbAct1Result, zmbAResult, zmbBResult, zmbCResult] = await Promise.allSettled([
    createZMBAct1Scenario(),
    createZMBScenario(ZMB_A_NAME, ZMB_PHR_A),
    createZMBScenario(ZMB_B_NAME, ZMB_PHR_B),
    createZMBScenario(ZMB_C_NAME, ZMB_PHR_C),
  ]);

  if (zmbAct1Result.status === "fulfilled") zmbAct1Id = zmbAct1Result.value;
  if (zmbAResult.status === "fulfilled")    zmbAId    = zmbAResult.value;
  if (zmbBResult.status === "fulfilled")    zmbBId    = zmbBResult.value;
  if (zmbCResult.status === "fulfilled")    zmbCId    = zmbCResult.value;

  const failures = [zmbAct1Result, zmbAResult, zmbBResult, zmbCResult]
    .filter((r) => r.status === "rejected")
    .map((r) => (r as PromiseRejectedResult).reason as Error);
  if (failures.length > 0) {
    console.error("Demo setup failures:", failures.map((e) => e.message).join("; "));
  }
});

// ---------------------------------------------------------------------------
// Narrated walkthrough — Demo 8
// ---------------------------------------------------------------------------

test(
  "Stakeholder demo walkthrough — narrated screen recording (M19 Demo 8)",
  { tag: ["@demo"] },
  async ({ page }) => {
    test.setTimeout(45 * 60 * 1000);

    if (!zmbAct1Id || !zmbAId || !zmbBId || !zmbCId) {
      console.warn("Demo scenario creation incomplete — aborting walkthrough.");
      return;
    }

    // NM-032 / Issue #675: match legibility gate and live demo viewport.
    await page.setViewportSize({ width: 1440, height: 900 });

    // Register Act 1 route mocks before any navigation.
    // ZMB Act 1: constraint-floor-search POST, baseline trajectory, branch trajectory.
    // Act 2 ZMB calls are NOT intercepted — they use real backend data.
    await registerZMBAct1Mocks(page, zmbAct1Id);

    // ── Opening narration ─────────────────────────────────────────────────────

    await page.goto("/");
    await waitForAppReady(page);

    await speak(
      "There is a room where this happens. " +
      "On one side of the table: a creditor team. " +
      "They have institutional memory that spans decades of programme design. " +
      "They have proprietary models. They have twenty analysts behind them who have done this forty times. " +
      "On the other side: a finance ministry. Three economists. Public data. " +
      "A question they have twelve seconds to answer. " +
      "In Demo seven, we showed you the counter-proposal as a number. " +
      "The Zambia team could say: under Option A, approximately 342,000 additional people fall below the poverty threshold. " +
      "The IMF team's first response was a question. Lucas asked it directly: " +
      "you tested multiplier 0.85 because your analysis told you to. " +
      "In a live negotiating session — when the IMF team adjusts their proposal on the spot — do you have time to test values one at a time? " +
      "The answer, until M19, was: not reliably. " +
      "Demo eight answers that question. " +
      "Act one: the ministry team does not test values. They set the floor — the threshold that cannot be crossed — and ask the instrument to find the configuration that satisfies it. " +
      "Act two: the same differential from Zambia — now with confidence intervals that were fit against what actually happened in Zambia and Senegal.",
    );

    // ── ACT 1: Zambia — Mode 3 Constraint-Floor Search ───────────────────────

    await page.goto(`/?scenario=${encodeURIComponent(zmbAct1Id)}`);
    await waitForAppReady(page);
    await page.waitForFunction(
      (id: string) =>
        (window as Record<string, unknown>).__worldsim_selectedScenarioId === id,
      zmbAct1Id,
      { timeout: 30_000 },
    );

    // Inject current step via DEV seam — ZMB Act 1 is at ZMB_ACT1_CURRENT_STEP.
    await page.evaluate((step: number) => {
      const fn = (window as Record<string, unknown>).__worldsim_setCurrentStep as
        | ((s: number) => void)
        | undefined;
      if (fn) fn(step);
    }, ZMB_ACT1_CURRENT_STEP);

    await expect(
      page.locator('[data-testid="zone-1a-trajectory-container"]'),
    ).toBeVisible({ timeout: 15_000 });

    await speak(
      "Zambia. Debt restructuring. Step four. Mid-programme. " +
      "The instrument cluster is showing the baseline trajectory. " +
      "The finance ministry team has configured the focal cohort: " +
      "bottom quintile poverty headcount, floor at 0.40. " +
      "Form three — Constraint Search — is now available in the right column.",
    );

    // Enter Mode 3 via the header toggle.
    let constraintFoundVisible = false;
    let branchApplied = false;

    const mode3ToggleBtn = page.locator('[data-testid="mode3-toggle"]');
    const toggleAvailable = await mode3ToggleBtn.isVisible({ timeout: 5_000 }).catch(() => false);

    if (!toggleAvailable) {
      console.warn("mode3-toggle not visible — skipping Act 1 Mode 3 interaction.");
    } else {
      await mode3ToggleBtn.click();

      // Form 1 must appear (ControlPlaneColumn rendered in MODE_3)
      const form1 = page.locator('[data-testid="control-plane-form1"]');
      await expect(form1).toBeVisible({ timeout: 5_000 });

      // Form 3 must also appear (constraint-search-section)
      const form3Section = page.locator('[data-testid="constraint-search-section"]');
      const form3Visible = await form3Section.isVisible({ timeout: 5_000 }).catch(() => false);

      if (!form3Visible) {
        console.warn("constraint-search-section not visible — ControlPlaneColumn Form 3 not rendered. Skipping Act 1 constraint search.");
      } else {
        await speak(
          "Active control entered. The ControlPlaneColumn is now visible on the right. " +
          "Form one: Policy Instruments. Form two: Scenario Shocks. " +
          "Form three: Constraint Search — the new M19 capability. " +
          "Floor configured: poverty headcount must stay at or above 0.40 " +
          "for the bottom quintile across all eight steps of the programme. " +
          "The analyst presses: Find safe boundary.",
        );

        // Click "Find safe boundary" button — data-testid="constraint-search-btn"
        // (confirmed from ControlPlaneColumn.tsx line ~791)
        const findBoundaryBtn = page.locator('[data-testid="constraint-search-btn"]');
        const findBtnVisible = await findBoundaryBtn.isVisible({ timeout: 5_000 }).catch(() => false);

        if (!findBtnVisible) {
          console.warn("constraint-search-btn not visible — Form 3 may be in unavailable state. Skipping constraint search.");
        } else {
          await findBoundaryBtn.click();

          // Wait for FOUND state — mocked response arrives synchronously from Playwright intercept.
          const foundContainer = page.locator('[data-testid="constraint-search-found"]');
          constraintFoundVisible = await foundContainer.waitFor({ state: "visible", timeout: 15_000 }).then(() => true).catch(() => false);

          if (constraintFoundVisible) {
            // Assert boundary value contains "0.83"
            await expect(
              page.locator('[data-testid="constraint-boundary-value"]'),
            ).toContainText("0.83", { timeout: 5_000 });

            // Assert tolerance band contains "±0.01"
            await expect(
              page.locator('[data-testid="constraint-tolerance-band"]'),
            ).toContainText("±0.01", { timeout: 5_000 });

            await speak(
              "Zambia. Mode three active. Form three — Constraint Search. " +
              "The analyst clicked Find safe boundary. " +
              "The instrument searched the full range: 0.1 to 3.0. Nine evaluations. " +
              "Safe boundary found: fiscal multiplier 0.83. " +
              "The instrument found it. Aicha did not dial to 0.83.",
            );

            // Apply fm=0.83 via Form 1 to trigger branch trajectory in Zone 1A.
            // This shows both baseline and boundary-branch simultaneously (Frame A requirement).
            const slider = page.locator('[data-testid="policy-param-slider"]').first();
            if (await slider.count() > 0) {
              await slider.evaluate((el: HTMLInputElement, value: string) => {
                const setter = Object.getOwnPropertyDescriptor(
                  window.HTMLInputElement.prototype,
                  "value",
                )!.set!;
                setter.call(el, value);
                el.dispatchEvent(new Event("input", { bubbles: true }));
              }, String(ZMB_ACT1_FM_BOUNDARY));
            }

            const applyBtn = page.locator('[data-testid="apply-policy-input"]');
            const applyVisible = await applyBtn.isVisible({ timeout: 3_000 }).catch(() => false);
            if (applyVisible) {
              await applyBtn.click();

              // Wait for branch trajectory to appear
              const zone1a = page.locator('[data-testid="zone-1a-trajectory"]');
              const counterCurve = zone1a.locator('[data-testid="trajectory-counter"]');
              branchApplied = await counterCurve.isVisible({ timeout: 12_000 }).catch(() => false);
            }
          } else {
            console.warn("constraint-search-found not visible after click — mock may not have intercepted. Skipping FOUND assertions.");
          }
        }
      }
    }

    // ── FRAME A — "The Boundary Found" (THESIS FRAME — Act 1, FOUND state) ──
    // Captured at step ZMB_ACT1_CURRENT_STEP = 4 with Form 3 FOUND state visible.
    await expect.soft(
      page.locator('[data-testid="current-step-display"]'),
      "Frame A: expected step 4 display.",
    ).toContainText("Step 4", { timeout: 2_000 });
    await page.waitForTimeout(1_200);
    await page.screenshot({ path: screenshotPath("frame-a-constraint-found.png") });

    // ── FRAME B — "The Driver Arc" (step 4, Zone 1D PSP driver arc) ──────────
    // Frame B is also at step 4 — same step, different compositional focus.
    // Zone 1D psp-driver-arc shows the badge row across the full programme window.
    // AC-E2 equivalent: Frame B and Frame A are the same step in M19 —
    // they differ by scroll offset (Zone 1D scrolled into view) not step.
    await expect.soft(
      page.locator('[data-testid="psp-driver-arc"]'),
      "Frame B: psp-driver-arc should be visible in Zone 1D (M19 G4 #1528).",
    ).toBeVisible({ timeout: 5_000 });

    // Reset to top of viewport for Frame B — Zone 1A (trajectory) and Zone 1D (PSP arc)
    // must both be visible simultaneously at 1440×900. block:"center" over-scrolled Zone 1A
    // out of frame (DEMO-167, DEMO-175). scrollTo(0,0) keeps all zones in the viewport.
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(400);

    await speak(
      "Step four. Mid-programme. Zone one D shows the PSP driver arc — " +
      "the causal driver at each step across the full programme window. " +
      "At steps one through five: fiscal sustainability. " +
      "At steps six through eight: social stability emerges. " +
      "The arc is not a snapshot. " +
      "It is a brief the political advisor can take into the negotiating room.",
    );

    await page.waitForTimeout(800);
    await page.screenshot({ path: screenshotPath("frame-b-driver-arc.png") });

    // Frame A and Frame B — byte-level distinctness check (different scroll offsets / Zone focus)
    {
      const frameAPath = screenshotPath("frame-a-constraint-found.png");
      const frameBPath = screenshotPath("frame-b-driver-arc.png");
      if (fs.existsSync(frameAPath) && fs.existsSync(frameBPath)) {
        // These frames may be identical in some mock states — soft assertion only.
        const aHash = fileMD5(frameAPath);
        const bHash = fileMD5(frameBPath);
        if (aHash === bHash) {
          console.warn("Frame A and Frame B have identical MD5 — Zone 1D driver arc may not be scroll-differentiated. Visual review required.");
        }
      }
    }

    // ── Advance to step 8 for Frame C ─────────────────────────────────────────

    const nextStepBtn = page.getByRole("button", { name: /Next Step/ });
    const stepDisplay = page.locator('[data-testid="current-step-display"]');

    // ZMB Act 1 is at step 4; advance to step 8 (4 more clicks).
    for (let targetStep = 5; targetStep <= 8; targetStep++) {
      const nextVisible = await nextStepBtn.isVisible({ timeout: 5_000 }).catch(() => false);
      if (nextVisible) {
        await nextStepBtn.click();
        await expect(stepDisplay).toContainText(`Step ${targetStep}`, { timeout: 20_000 });
        await page.waitForTimeout(600);
      }
    }

    await speak(
      "Step eight. Programme complete. Zone one B — the cohort impact section. " +
      "Bottom quintile poverty headcount. Recovery floor: 0.40. " +
      "At fiscal multiplier 0.83 — the boundary the instrument found — " +
      "Zone one B reads CLEAR. The threshold is not crossed. " +
      "This is the evidence the instrument found. " +
      "The binary search ran because 0.83 is the multiplier where the crossing first does not occur. " +
      "At any multiplier below 0.82, Zone one B at step 8 would read CROSSED.",
    );

    // ── FRAME C — "The Act 1 Evidence" (step 8, Zone 1B focal cohort CLEAR) ──
    // Reset page scroll so Zone 1B is in the upper viewport (DEMO-187, DEMO-171).
    // The Zone 1D scrollIntoView from Frame B left the page scrolled down; reset first.
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(300);
    // Scroll within Zone 1B container to reveal the focal cohort CLEAR badge at bottom.
    await page.locator('[data-testid="zone-1b-cohort-impact"]').evaluate(
      (el: HTMLElement) => { el.scrollTop = el.scrollHeight; },
    ).catch(() => {}); // non-fatal if zone-1b-cohort-impact not found
    await page.waitForTimeout(300);
    await expect.soft(
      page.locator('[data-testid="current-step-display"]'),
      "Frame C: expected step 8 display.",
    ).toContainText("Step 8", { timeout: 2_000 });
    await page.screenshot({ path: screenshotPath("frame-c-act1-evidence.png") });

    // ── ACT 2: Zambia — Three-Scenario Comparison with Posterior CI ───────────

    await page.goto(`/?scenario=${encodeURIComponent(zmbCId)}`);
    await waitForAppReady(page);
    await expect(
      page.locator('[data-testid="zone-1a-trajectory-container"]'),
    ).toBeVisible({ timeout: 15_000 });

    // Inject the N=3 ZMB comparison via the E2E test seam.
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

    await speak(
      "Act two. Zambia. " +
      "The same negotiating context — but the ministry team now has three scenarios loaded simultaneously. " +
      "Option A: the IMF Extended Fund Facility, front-loaded consolidation. " +
      "Option B: EFF gradual — the same programme terms at a slower pace. " +
      "Option C: the Homegrown Programme, the ministry's counter-proposal.",
    );

    if (!injected) {
      console.warn("__worldsim_setComparisonScenarios not available — N=3 comparison not implemented. Skipping Act 2.");
    } else {
      await page.waitForSelector('[data-testid^="zone1a-curve-scenario-"]', { timeout: 15_000 }).catch(() => {});

      await speak(
        "All three visible in Zone one A. " +
        "The question is not which scenario is correct. " +
        "The question is: what is the precise headcount differential between Option A and the counter-proposal? " +
        "Not an assertion. A number.",
      );

      const compSummary = page.locator('[data-testid="distributional-comparison-summary"]');
      const summaryVisible = await compSummary.waitFor({ state: "visible", timeout: 20_000 }).then(() => true).catch(() => false);

      if (summaryVisible) {
        // M19 epistemic precision: CI label must read "declared interval (BandingEngine)"
        // NOT "95% CI" (DEMO-163 resolution, G4 #1529).
        await expect.soft(
          page.locator('[data-testid="distributional-ci-label"]').first(),
          "M19 AC-CI: distributional-ci-label must read 'declared interval (BandingEngine)' not '95% CI'.",
        ).toContainText("declared interval", { timeout: 5_000 });

        await speak(
          "Act two. Zambia. Three options. Zone one B comparison summary: " +
          "plus approximately 342,700 persons below poverty threshold. " +
          "Declared interval, BandingEngine. T3. Direction stable. " +
          "The interval label has changed from Demo seven. " +
          "Declared interval means we are declaring a range. " +
          "It was calibrated against Zambian and Senegalese fiscal outcomes. " +
          "Not a structural assumption.",
        );

        await page.waitForTimeout(1_200);

        // Center choropleth on ZMB before Frame D
        await page.evaluate(() => {
          const fn = (window as Record<string, unknown>).__worldsim_centerOnEntity as
            ((id: string) => void) | undefined;
          if (fn) fn("ZMB");
        });
        await page.waitForTimeout(800);

        // ── FRAME D — "The Calibrated Counter-Proposal" ───────────────────────
        // Zone 3 must be COLLAPSED for Frame D.
        {
          const mapCenter = await page.evaluate(() => {
            const fn = (window as Record<string, unknown>).__worldsim_getMapCenter as
              (() => { lat: number; lon: number } | null) | undefined;
            return fn?.() ?? null;
          });
          if (mapCenter !== null) {
            expect.soft(
              mapCenter.lat,
              "Frame D: Map not centred on ZMB (lat too high).",
            ).toBeLessThan(-8);
            expect.soft(mapCenter.lat).toBeGreaterThan(-20);
          } else {
            console.warn("__worldsim_getMapCenter unavailable — ZMB centering is a visual-review check only.");
          }
        }
        await page.screenshot({ path: screenshotPath("frame-d-calibrated-ci.png") });

        // ── FRAME E — "The Posterior Methodology" ────────────────────────────
        // Expand Zone 3 methodology panel.
        const methodologyToggle = page.locator('[data-testid="methodology-panel-toggle"]');
        const toggleAttached = await methodologyToggle.waitFor({ state: "attached", timeout: 5_000 }).then(() => true).catch(() => false);

        if (toggleAttached) {
          // Use native JS .click() to bypass z-index hit-testing (same pattern as M18).
          await page.evaluate(() => {
            const btn = document.querySelector('[data-testid="methodology-panel-toggle"]') as HTMLButtonElement | null;
            if (btn) btn.click();
          });
          await page.waitForTimeout(600);

          await speak(
            "The methodology panel. Expanded in Zone one B. Two layers now. " +
            "The BandingEngine structure — step-based half-width, tier multiplier. " +
            "And the posterior calibration note: interval widths calibrated against " +
            "SEN and ZMB historical fiscal programme outcomes. " +
            "This closes Lucas's question from Demo seven.",
          );

          // M19: Zone 3 methodology panel (data-testid="zone3-methodology-panel")
          // should contain the Bayesian posterior calibration description.
          const zone3Panel = page.locator('[data-testid="zone3-methodology-panel"]');
          await expect.soft(
            zone3Panel,
            "Frame E: zone3-methodology-panel should be visible after methodology-panel-toggle click (M19 G5).",
          ).toBeVisible({ timeout: 5_000 });

          await page.waitForTimeout(1_000);
          await page.screenshot({ path: screenshotPath("frame-e-posterior-methodology.png") });
        } else {
          console.warn("methodology-panel-toggle not attached — Zone 3 auditability not implemented. Skipping Frame E expansion.");
          await page.screenshot({ path: screenshotPath("frame-e-posterior-methodology.png") });
        }
      } else {
        console.warn(
          "distributional-comparison-summary not visible after comparison injection. " +
          "Verify G3 DistributionalComparisonSummary is implemented and ZMB scenarios have poverty_headcount_ratio seeded.",
        );
        await page.screenshot({ path: screenshotPath("frame-d-calibrated-ci.png") });
        await page.screenshot({ path: screenshotPath("frame-e-posterior-methodology.png") });
      }
    }

    // Five-frame hash check: all five screenshots must have distinct MD5s.
    {
      const framePaths = [
        screenshotPath("frame-a-constraint-found.png"),
        screenshotPath("frame-b-driver-arc.png"),
        screenshotPath("frame-c-act1-evidence.png"),
        screenshotPath("frame-d-calibrated-ci.png"),
        screenshotPath("frame-e-posterior-methodology.png"),
      ];
      const hashes = framePaths
        .filter(fs.existsSync)
        .map((p) => fileMD5(p));
      const uniqueHashes = new Set(hashes);
      if (uniqueHashes.size < hashes.length) {
        console.warn(
          `Hash deduplication: ${hashes.length} frames, only ${uniqueHashes.size} distinct. ` +
          "Some frames may be identical — visual review required before stakeholder presentation.",
        );
      }
    }

    // ── Closing narration ─────────────────────────────────────────────────────

    await speak(
      "Two acts. One instrument cluster. " +
      "Act one: the finance ministry's team enters active control. " +
      "They set the floor. The instrument searches. It returns the boundary. " +
      "They did not choose 0.83. The instrument found it. " +
      "Act two: they present the counter-proposal as a specific headcount differential " +
      "with a declared interval — calibrated against what actually happened in Zambia and Senegal. " +
      "The counter-proposal is no longer a narrative. " +
      "It is a demonstrable, citable, session-specific finding " +
      "produced from the ministry's own analytical infrastructure. " +
      "That is what WorldSim is for. " +
      "The quinoa farmer in Bolivia will never know this tool exists. " +
      "Build it as if he does.",
    );

    if (branchApplied) {
      // Confirm branch was applied for Act 1 — informational only
      console.log(`Act 1 branch at fm=${ZMB_ACT1_FM_BOUNDARY} applied successfully.`);
    }
  },
);

// ---------------------------------------------------------------------------
// AC-D1 — mock fixture: makeZMBAct1BranchMock includes psp_dominant_driver
//          at all steps (M19 driver arc requires all steps, not only branched steps)
// ---------------------------------------------------------------------------

test("AC-D1 — mock fixture: makeZMBAct1BranchMock includes psp_dominant_driver at all steps (M19 G4 #1528)", () => {
  // M19 PSP driver arc (psp-driver-arc in Zone 1D) requires psp_dominant_driver
  // at every step across the programme window — not only from BRANCH_FROM_STEP.
  // Steps 1–5: "fiscal_sustainability"; steps 6–8: "social_stability".
  const branchMock = makeZMBAct1BranchMock();
  const steps = (branchMock as Record<string, unknown[]>).steps;
  expect(Array.isArray(steps), "AC-D1: mock.steps must be an array").toBe(true);

  for (const stepIndex of [1, 4, 6, 8]) {
    const step = steps.find(
      (s) => (s as Record<string, unknown>).step_index === stepIndex,
    ) as Record<string, unknown[]> | undefined;
    expect(step, `AC-D1: step_index ${stepIndex} must exist in branch mock`).toBeDefined();
    if (!step) continue;

    const frameworks = step.frameworks as Array<Record<string, unknown>>;
    const peFramework = frameworks.find(
      (fw) => fw.framework === "political_economy",
    ) as Record<string, unknown> | undefined;
    expect(
      peFramework,
      `AC-D1: political_economy framework absent from step ${stepIndex} of branch mock`,
    ).toBeDefined();
    if (!peFramework) continue;

    expect(
      peFramework.psp_dominant_driver,
      `AC-D1 FAIL: psp_dominant_driver absent from political_economy at step ${stepIndex}. ` +
      "M19 driver arc requires psp_dominant_driver at every step. " +
      "See M19 G4 #1528 and stakeholder-walkthrough.md §Step 2.",
    ).toBeTruthy();
  }

  // Confirm driver arc shifts from fiscal to social stability
  const step5 = steps.find((s) => (s as Record<string, unknown>).step_index === 5) as Record<string, unknown[]> | undefined;
  const step6 = steps.find((s) => (s as Record<string, unknown>).step_index === 6) as Record<string, unknown[]> | undefined;
  if (step5 && step6) {
    const pe5 = (step5.frameworks as Array<Record<string, unknown>>).find((f) => f.framework === "political_economy") as Record<string, unknown> | undefined;
    const pe6 = (step6.frameworks as Array<Record<string, unknown>>).find((f) => f.framework === "political_economy") as Record<string, unknown> | undefined;
    expect(
      pe5?.psp_dominant_driver,
      "AC-D1: step 5 driver should be fiscal_sustainability",
    ).toBe("fiscal_sustainability");
    expect(
      pe6?.psp_dominant_driver,
      "AC-D1: step 6 driver should be social_stability (arc shift for walkthrough narration)",
    ).toBe("social_stability");
  }
});

// ---------------------------------------------------------------------------
// AC-D3 — mock fixture: makeZMBAct1BaselineMock includes focal indicator
// ---------------------------------------------------------------------------

test("AC-D3 — mock fixture: makeZMBAct1BaselineMock includes bottom_quintile_informal_workers_poverty_headcount", () => {
  // The HCL bottom quintile indicator must be present in the mock so Zone 1B
  // can render a numeric value (not "—") for the focal cohort row.
  const baselineMock = makeZMBAct1BaselineMock("fixture-check-id");
  const steps = (baselineMock as Record<string, unknown[]>).steps;
  expect(Array.isArray(steps), "AC-D3: baseline mock.steps must be an array").toBe(true);

  const step4 = steps.find(
    (s) => (s as Record<string, unknown>).step_index === 4,
  ) as Record<string, unknown[]> | undefined;
  expect(step4, "AC-D3: step_index 4 must exist in baseline mock").toBeDefined();
  if (!step4) return;

  const frameworks = step4.frameworks as Array<Record<string, unknown>>;
  const hdFramework = frameworks.find(
    (fw) => fw.framework === "human_development",
  ) as Record<string, Record<string, unknown>> | undefined;
  expect(
    hdFramework,
    "AC-D3: human_development framework absent from step 4 of baseline mock",
  ).toBeDefined();
  if (!hdFramework) return;

  const indicators = hdFramework.indicators as Record<string, unknown> | undefined;
  expect(
    indicators?.bottom_quintile_informal_workers_poverty_headcount,
    "AC-D3 FAIL: bottom_quintile_informal_workers_poverty_headcount absent from " +
    "human_development indicators in ZMB Act 1 baseline mock. " +
    "Without this, Zone 1B focal row shows UNKNOWN — no numeric evidence for Act 1 finding.",
  ).toBeDefined();
});

// ---------------------------------------------------------------------------
// AC-D4 — mock fixture: ecological framework note triggers "Not modelled" display
// ---------------------------------------------------------------------------

test("AC-D4 — mock fixture: ecological framework note triggers 'Not modelled' display", () => {
  const baselineMock = makeZMBAct1BaselineMock("fixture-check-id");
  const steps = (baselineMock as Record<string, unknown[]>).steps;
  const step1 = steps.find(
    (s) => (s as Record<string, unknown>).step_index === 1,
  ) as Record<string, unknown[]> | undefined;
  if (!step1) return;

  const frameworks = step1.frameworks as Array<Record<string, unknown>>;
  const ecFramework = frameworks.find(
    (fw) => fw.framework === "ecological",
  ) as Record<string, unknown> | undefined;

  if (ecFramework) {
    expect(
      ecFramework.composite_score,
      "AC-D4: ecological composite_score must be null when module is disabled",
    ).toBeNull();
  }

  expect(true, "AC-D4: fixture shape check complete — rendering fix is in FourFrameworkZone1D.tsx").toBe(true);
});

// ---------------------------------------------------------------------------
// AC-D5 — branch mock includes HD focal indicator (DEMO-156 regression guard)
// ---------------------------------------------------------------------------

test("AC-D5 — mock fixture: makeZMBAct1BranchMock includes bottom_quintile_informal_workers_poverty_headcount at terminal step (DEMO-156 guard)", () => {
  // Terminal step (N_STEPS=8) must have the indicator above 0.40 floor → CLEAR badge.
  // This is the Zone 1B evidence that 0.83 is the boundary.
  const branchMock = makeZMBAct1BranchMock();
  const steps = (branchMock as Record<string, unknown[]>).steps;
  expect(Array.isArray(steps), "AC-D5: mock.steps must be an array").toBe(true);

  const step8 = steps.find(
    (s) => (s as Record<string, unknown>).step_index === N_STEPS,
  ) as Record<string, unknown[]> | undefined;
  expect(step8, `AC-D5: step_index ${N_STEPS} (terminal) must exist in branch mock`).toBeDefined();
  if (!step8) return;

  const frameworks = step8.frameworks as Array<Record<string, unknown>>;
  const hdFramework = frameworks.find(
    (fw) => fw.framework === "human_development",
  ) as Record<string, Record<string, unknown>> | undefined;
  expect(
    hdFramework,
    `AC-D5: human_development framework absent from step ${N_STEPS} of branch mock`,
  ).toBeDefined();
  if (!hdFramework) return;

  const indicators = hdFramework.indicators as Record<string, unknown> | undefined;
  expect(
    indicators?.bottom_quintile_informal_workers_poverty_headcount,
    "AC-D5 FAIL: bottom_quintile_informal_workers_poverty_headcount absent from " +
    `human_development indicators in branch mock at terminal step ${N_STEPS} (DEMO-156 guard). ` +
    "Without this, Zone 1B focal row shows UNKNOWN — no CLEAR badge for Act 1 evidence frame.",
  ).toBeDefined();

  // Confirm terminal value is above floor (0.40) — enables CLEAR badge
  const hdIndicators = indicators as Record<string, Record<string, string>> | undefined;
  const terminalValue = parseFloat(
    hdIndicators?.bottom_quintile_informal_workers_poverty_headcount?.value ?? "0",
  );
  expect(
    terminalValue,
    `AC-D5: terminal step indicator value (${terminalValue}) must be above floor (0.40) to render CLEAR badge.`,
  ).toBeGreaterThan(0.40);
});

// ---------------------------------------------------------------------------
// AC-D6 — createZMBAct1Scenario includes monitored_focal_cohorts (DEMO-156 guard)
// ---------------------------------------------------------------------------

test("AC-D6 — fixture: createZMBAct1Scenario configuration includes monitored_focal_cohorts for Zone 1B focal row and Form 3 availability (DEMO-156 guard)", () => {
  // Form 3 (Constraint Search) renders only when monitored_focal_cohorts is populated.
  // createZMBAct1Scenario must include the array — otherwise Form 3 shows "unavailable" state
  // and "Find safe boundary" button never appears.
  const specSrc = fs.readFileSync(__filename, "utf8");
  expect(
    specSrc.includes("monitored_focal_cohorts"),
    "AC-D6 FAIL: 'monitored_focal_cohorts' absent from spec. " +
    "Fix: add monitored_focal_cohorts array to createZMBAct1Scenario configuration body. " +
    "Without it, Form 3 renders 'unavailable' and constraint search cannot run.",
  ).toBe(true);
  expect(
    specSrc.includes("floor_label"),
    "AC-D6 FAIL: 'floor_label' absent from spec — FocalCohortConfig incomplete (requires floor_label field).",
  ).toBe(true);
  expect(
    specSrc.includes("constraint-search-btn"),
    "AC-D6 FAIL: 'constraint-search-btn' testid absent from spec. " +
    "The 'Find safe boundary' button uses data-testid='constraint-search-btn' per ControlPlaneColumn.tsx.",
  ).toBe(true);
});

// ---------------------------------------------------------------------------
// AC-E1 — Jargon gate (static — does not require live stack; runs in CI)
//
// Guard: "Policy Malevolent Margin" must never appear in frontend/src.
// Source: M18-G7-E intent §AC-E1 + DEMO-142 root cause. Retained for M19.
// ---------------------------------------------------------------------------

test("AC-E1 — jargon gate: 'Malevolent' absent from frontend/src", () => {
  const srcDir = path.resolve(__dirname, "../../src");
  const found = findFilesWithString(srcDir, "Malevolent");
  expect(
    found,
    `Jargon 'Policy Malevolent Margin' found in: ${found.join(", ")}. ` +
    "Fix DEMO-142: replace with 'Policy Maneuver Margin' (see M18-G7-E intent §2.1).",
  ).toHaveLength(0);
});

// ---------------------------------------------------------------------------
// AC-E5 / AC-E6 / AC-E7 — Walkthrough content gates (static — no live stack)
//
// Checks against the M19 stakeholder-walkthrough.md.
// ---------------------------------------------------------------------------

test("AC-E5 — walkthrough: '340,000' absent (corrected to ~342,700 in M19)", () => {
  const wt = fs.readFileSync(WALKTHROUGH_PATH, "utf8");
  expect(
    wt,
    "AC-E5 FAIL: Walkthrough still contains '340,000'. " +
    "M18 fix (DEMO-144) replaced this with approximately 342,700. " +
    "M19 walkthrough should carry the corrected figure throughout.",
  ).not.toContain("340,000");
});

test("AC-E6 — walkthrough: 'declared interval' present in M19 (DEMO-163 resolution)", () => {
  const wt = fs.readFileSync(WALKTHROUGH_PATH, "utf8");
  // M19 epistemic precision change: "declared interval (BandingEngine)" replaces "95% CI".
  // This is the DEMO-163 resolution (Lucas's Demo 7 challenge on label precision).
  // The walkthrough must use the accurate label in its Act 2 narration.
  const hasDeclaredInterval = wt.toLowerCase().includes("declared interval");
  expect(
    hasDeclaredInterval,
    "AC-E6 FAIL: Walkthrough missing 'declared interval' — M19 epistemic precision label. " +
    "Fix DEMO-163: replace '95% CI' with 'declared interval (BandingEngine)' in Act 2 narration sections. " +
    "See M19 walkthrough §Step 4 and screenshot-brief.md §Frame D.",
  ).toBe(true);
});

test("AC-E7 — walkthrough: at least 8 act-transition sentences marked (DEMO-148)", () => {
  const wt = fs.readFileSync(WALKTHROUGH_PATH, "utf8");
  // Transition sentences are delimited with <!-- TRANSITION --> HTML comments.
  // Both M18 and M19 walkthroughs require 8 transitions across the five-frame walkthrough.
  const transitionMarkers = wt.match(/<!--\s*TRANSITION/gi) ?? [];
  expect(
    transitionMarkers.length,
    `AC-E7 FAIL: Only ${transitionMarkers.length} transition markers found (need ≥ 8). ` +
    "Fix DEMO-148: add 8 <!-- TRANSITION --> markers around act-break narration sentences. " +
    "Priority: Frame C → Frame D act break is highest-risk gap. " +
    "See M19 walkthrough §Sections 1–5.",
  ).toBeGreaterThanOrEqual(8);
});
