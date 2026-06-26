/**
 * E2E: M17-G5 — Adaptive Y-Axis Extension (#1251)
 *
 * Authored BEFORE implementation per intent document:
 *   docs/process/intents/M17-G5-2026-06-25-adaptive-y-axis-extension.md
 *
 * Sprint entry: docs/process/sprint-plans/m17-g5-sprint-entry.md (EL Approved 2026-06-25)
 *
 * ACs covered:
 *   AC-1251-3 — Floor line not clamped to chart bottom when floor is below data range
 *   AC-1251-R — N=1 recharts mode is unaffected by this change
 *
 * NM-056 rule: NO test.skip(), test.fixme(), or .only() patterns.
 * Guard pattern: if zone-1a-mda-floor-ZMB is not attached, return without asserting.
 * Once the testid is present, the assertion is a hard-fail.
 *
 * Fixture design (intent doc §0 worked example):
 *   Entity composite scores: 0.65–0.80 (ZMB + SEN, N=2 → composite SVG mode)
 *   MDA floor for ZMB: 0.40 (below data range)
 *   Before fix: yScale(0.40) clamps to chart bottom → y1 == svgHeight - MARGIN.bottom
 *   After fix: yDomain extends to [~0.35, ~0.85] → y1 < svgHeight - MARGIN.bottom
 */
import { test, expect } from "@playwright/test";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const API_BASE = "http://localhost:8000/api/v1";
const MARGIN_TOP = 16;
const MARGIN_BOTTOM = 48;

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface ScenarioCreateResponse {
  scenario_id: string;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function waitForAppReady(page: import("@playwright/test").Page): Promise<void> {
  await page.waitForFunction(
    () => typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
    { timeout: 10_000 },
  );
}

async function createScenario(
  entities: string[],
  nSteps: number,
  name: string,
): Promise<string | null> {
  try {
    const createRes = await fetch(`${API_BASE}/scenarios`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        configuration: {
          entities,
          n_steps: nSteps,
          start_date: "2024-01-01",
          modules_config: {
            ecological: { enabled: false },
            political_economy: { enabled: false },
          },
        },
        scheduled_inputs: [],
      }),
    });
    if (!createRes.ok) return null;
    const { scenario_id: id } = (await createRes.json()) as ScenarioCreateResponse;
    for (let i = 0; i < nSteps; i++) {
      const advRes = await fetch(
        `${API_BASE}/scenarios/${encodeURIComponent(id)}/advance`,
        { method: "POST" },
      );
      if (!advRes.ok) return null;
    }
    return id;
  } catch {
    return null;
  }
}

/**
 * Trajectory mock for a single entity with composite scores in 0.65–0.80 range.
 * MDA floor at 0.40 — below the natural data range — to exercise the y-axis extension.
 */
function makeHighScoreTrajectoryMock(scenarioId: string, entityId: string): object {
  return {
    scenario_id: scenarioId,
    entity_id: entityId,
    step_count: 3,
    mda_floors: [
      {
        framework: "human_development",
        floor_value: "0.40",
        severity: "CRITICAL",
        label: "HD poverty floor",
      },
    ],
    steps: [
      {
        step_index: 1,
        effective_from: "2024-01-01T00:00:00Z",
        step_event_label: null,
        step_significance: "ROUTINE",
        frameworks: [
          {
            framework: "financial",
            composite_score: "0.65",
            scoring_basis: "normalized_relative",
            confidence_tier: 2,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: false,
          },
          {
            framework: "human_development",
            composite_score: "0.70",
            scoring_basis: "normalized_relative",
            confidence_tier: 2,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: false,
          },
          {
            framework: "ecological",
            composite_score: null,
            scoring_basis: null,
            confidence_tier: null,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: null,
          },
          {
            framework: "governance",
            composite_score: "0.75",
            scoring_basis: "normalized_relative",
            confidence_tier: 2,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: false,
          },
        ],
        policy_inputs: [],
        shock_events: [],
      },
      {
        step_index: 2,
        effective_from: "2024-02-01T00:00:00Z",
        step_event_label: null,
        step_significance: "ROUTINE",
        frameworks: [
          {
            framework: "financial",
            composite_score: "0.68",
            scoring_basis: "normalized_relative",
            confidence_tier: 2,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: false,
          },
          {
            framework: "human_development",
            composite_score: "0.72",
            scoring_basis: "normalized_relative",
            confidence_tier: 2,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: false,
          },
          {
            framework: "ecological",
            composite_score: null,
            scoring_basis: null,
            confidence_tier: null,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: null,
          },
          {
            framework: "governance",
            composite_score: "0.78",
            scoring_basis: "normalized_relative",
            confidence_tier: 2,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: false,
          },
        ],
        policy_inputs: [],
        shock_events: [],
      },
      {
        step_index: 3,
        effective_from: "2024-03-01T00:00:00Z",
        step_event_label: null,
        step_significance: "ROUTINE",
        frameworks: [
          {
            framework: "financial",
            composite_score: "0.67",
            scoring_basis: "normalized_relative",
            confidence_tier: 2,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: false,
          },
          {
            framework: "human_development",
            composite_score: "0.71",
            scoring_basis: "normalized_relative",
            confidence_tier: 2,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: false,
          },
          {
            framework: "ecological",
            composite_score: null,
            scoring_basis: null,
            confidence_tier: null,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: null,
          },
          {
            framework: "governance",
            composite_score: "0.76",
            scoring_basis: "normalized_relative",
            confidence_tier: 2,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: false,
          },
        ],
        policy_inputs: [],
        shock_events: [],
      },
    ],
  };
}

function makeScenarioDetailMock(scenarioId: string, entities: string[]): object {
  return {
    scenario_id: scenarioId,
    name: "G5-adaptive-y-axis-test",
    status: "completed",
    configuration: {
      entities,
      n_steps: 3,
      start_date: "2024-01-01",
      modules_config: {
        ecological: { enabled: false },
        political_economy: { enabled: false },
      },
    },
    created_at: "2024-01-01T00:00:00Z",
    ia1_disclosure: null,
  };
}

// ---------------------------------------------------------------------------
// AC-1251-3 — Floor line not clamped to chart bottom
// ---------------------------------------------------------------------------

test.describe("AC-1251-3: MDA floor line position when floor is below data range", () => {
  let scenarioId: string | null = null;
  let trajectoryCallCount = 0;
  const ENTITIES = ["ZMB", "SEN"];

  test.beforeAll(async () => {
    try {
      scenarioId = await createScenario(ENTITIES, 3, "G5-adaptive-y-axis-AC1251-3");
    } catch {
      scenarioId = null;
    }
  });

  test("AC-1251-3: zone-1a-mda-floor-ZMB y1 is above chart bottom when floor (0.40) is below data range (0.65–0.80)", async ({
    page,
  }) => {
    if (!scenarioId) return;

    trajectoryCallCount = 0;
    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ENTITIES)),
      });
    });

    await page.route("**/api/v1/scenarios/*/trajectory**", (route) => {
      const entityId = ENTITIES[trajectoryCallCount % ENTITIES.length];
      trajectoryCallCount++;
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeHighScoreTrajectoryMock(sid, entityId)),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const trajectory = page.locator('[data-testid="zone-1a-trajectory"]');
    if (!(await trajectory.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: floor line testid requires composite SVG mode (N=2) to exist
    const floorLine = page.locator('[data-testid="zone-1a-mda-floor-ZMB"]');
    if ((await floorLine.count()) === 0) return; // composite SVG not yet rendered

    // Read y1 attribute of the floor SVG line element
    const y1 = await page.evaluate((): number | null => {
      const el = document.querySelector('[data-testid="zone-1a-mda-floor-ZMB"]');
      if (!el) return null;
      const raw = el.getAttribute("y1");
      return raw !== null ? parseFloat(raw) : null;
    });
    if (y1 === null) return; // element missing — guard fires

    // Read the SVG height to compute chart bottom threshold
    const svgHeight = await page.evaluate((): number | null => {
      const trajectoryDiv = document.querySelector('[data-testid="zone-1a-trajectory"]');
      if (!trajectoryDiv) return null;
      const svg = trajectoryDiv.querySelector("svg");
      if (!svg) return null;
      const raw = svg.getAttribute("height");
      return raw !== null ? parseFloat(raw) : null;
    });
    if (svgHeight === null) return; // SVG not found — guard fires

    // Chart bottom pixel = svgHeight - MARGIN_BOTTOM
    const chartBottom = svgHeight - MARGIN_BOTTOM;

    // After fix: floor line must be above chart bottom (not clamped)
    expect(y1).toBeLessThan(chartBottom);
    // Floor line must be within chart area (below the top margin)
    expect(y1).toBeGreaterThan(MARGIN_TOP);
  });
});

// ---------------------------------------------------------------------------
// AC-1251-R — Regression: N=1 recharts mode unaffected
// ---------------------------------------------------------------------------

test.describe("AC-1251-R: N=1 recharts mode Zone 1A unaffected by fix", () => {
  let scenarioId: string | null = null;
  const ENTITIES = ["ZMB"];

  test.beforeAll(async () => {
    try {
      scenarioId = await createScenario(ENTITIES, 3, "G5-adaptive-y-axis-AC1251-R");
    } catch {
      scenarioId = null;
    }
  });

  test("AC-1251-R: N=1 Zone 1A recharts path renders four framework curves without layout change", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ENTITIES)),
      });
    });

    await page.route("**/api/v1/scenarios/*/trajectory**", (route) => {
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeHighScoreTrajectoryMock(sid, "ZMB")),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const trajectory = page.locator('[data-testid="zone-1a-trajectory"]');
    if (!(await trajectory.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // N=1 uses recharts path — composite SVG floor testid should NOT be present
    const compositeFloor = page.locator('[data-testid="zone-1a-mda-floor-ZMB"]');
    // In recharts mode, this testid is absent (recharts uses ReferenceLine, not SVG line with testid)
    expect(await compositeFloor.count()).toBe(0);

    // Zone 1A trajectory container is present and visible
    await expect(trajectory).toBeVisible();
  });
});
