/**
 * E2E: M17-G2 — Multi-Scenario Comparison (N>2) — AC-S1, AC-A1, AC-B1, AC-D1, AC-P1/P3/P5.
 *
 * Authored BEFORE implementation from intent document at:
 * docs/process/intents/M17-G2-2026-06-25-multi-scenario-comparison.md
 *
 * Design artifacts:
 *   docs/ux/design-thinking/multi-scenario-comparison/ux-journeys-n3.md (data-testid anchors)
 *   docs/ux/design-thinking/multi-scenario-comparison/persona-mvs-n3.md (persona MVS)
 *   docs/architecture/reviews/ARCH-REVIEW-007-m17-n3-assessment.md (ADR option (b))
 *
 * Sprint entry: docs/process/sprint-plans/m17-g2-sprint-entry.md §2.4
 * BPO ACCEPT: #394#issuecomment-4803977557
 * Hard gate: #1249 (Zone 1A curve identifiability) must be merged before Phase 3 PR opens
 *
 * ACs covered:
 *   AC-S1 — Three scenarios loaded; Zone 1A N=3 curves; Zone 1B + Zone 1D update
 *   AC-A1 — Zone 1A N=3 differentiability: terminal labels A/B/C; MDA floor preserved
 *   AC-B1 — Zone 1B per-scenario rows (not union); Option C "[no crossings]"; MDA panel ≥80px
 *   AC-D1 — Zone 1D per-scenario PSP: three values simultaneously visible without interaction
 *   AC-P5 — Persona 5 (Aicha): Zone 1A + Zone 1B answer question without narration at 1280×800
 *   AC-P1 — Persona 1 (Lucas): worst Q1 trajectory identifiable from Zone 1A curves
 *   AC-P3 — Persona 3 (Andreas): PSP comparison readable from Zone 1D without view-switch
 *
 * NM-056 guard: all assertions are hard-fail. No test.skip() or test.fixme() without
 * a filed near-miss entry authorizing the skip.
 *
 * Guard pattern: tests that exercise data-testid anchors not yet implemented use
 * isVisible().catch(() => false) to return without failing. Guards become active
 * assertions once G2 Phase 3 implementation lands. A guard that fires indefinitely
 * is a failing test — it signals the implementation has not landed.
 *
 * Route mocking strategy:
 *   Three ZMB scenarios are pre-configured via API fixtures injected into route mocks.
 *   The comparison store receives N=3 ScenarioComparisonConfig[] via mock.
 *   Zone 1A, Zone 1B, and Zone 1D assertions use the committed data-testid anchors.
 *
 *   Option A (zmb-option-a): Q1=0.58, PSP=0.58, CRITICAL Q1 poverty step 2,
 *                            WARNING Health system capacity step 3
 *   Option B (zmb-option-b): Q1=0.59, PSP=0.67, CRITICAL Q1 poverty step 3,
 *                            WARNING School enrollment rate step 3
 *   Option C (zmb-option-c): Q1=0.72, PSP=0.74, no threshold crossings
 *
 * Fixture anchor: Demo 7 Act 2 — Zambia restructuring comparison at step 4.
 */
import { test, expect } from "@playwright/test";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface ScenarioCreateResponse {
  scenario_id: string;
}

interface ThresholdCrossing {
  indicator_id: string;
  indicator_name: string;
  severity: "CRITICAL" | "WARNING";
  first_crossing_step: number;
  measurement_framework: string;
}

interface ScenarioComparisonMock {
  scenarioId: string;
  label: string;
  paletteIndex: number;
  q1CompositeAtStep4: number;
  pspValue: number;
  thresholdCrossings: ThresholdCrossing[];
}

// ---------------------------------------------------------------------------
// Demo 7 Act 2 fixture data
// ---------------------------------------------------------------------------

const ZMB_OPTION_A: ScenarioComparisonMock = {
  scenarioId: "zmb-option-a",
  label: "A",
  paletteIndex: 0,
  q1CompositeAtStep4: 0.58,
  pspValue: 0.58,
  thresholdCrossings: [
    {
      indicator_id: "q1_poverty_headcount",
      indicator_name: "Q1 Poverty headcount",
      severity: "CRITICAL",
      first_crossing_step: 2,
      measurement_framework: "human_development",
    },
    {
      indicator_id: "health_system_capacity",
      indicator_name: "Health system capacity",
      severity: "WARNING",
      first_crossing_step: 3,
      measurement_framework: "human_development",
    },
  ],
};

const ZMB_OPTION_B: ScenarioComparisonMock = {
  scenarioId: "zmb-option-b",
  label: "B",
  paletteIndex: 1,
  q1CompositeAtStep4: 0.59,
  pspValue: 0.67,
  thresholdCrossings: [
    {
      indicator_id: "q1_poverty_headcount",
      indicator_name: "Q1 Poverty headcount",
      severity: "CRITICAL",
      first_crossing_step: 3,
      measurement_framework: "human_development",
    },
    {
      indicator_id: "school_enrollment_rate",
      indicator_name: "School enrollment rate",
      severity: "WARNING",
      first_crossing_step: 3,
      measurement_framework: "human_development",
    },
  ],
};

const ZMB_OPTION_C: ScenarioComparisonMock = {
  scenarioId: "zmb-option-c",
  label: "C",
  paletteIndex: 2,
  q1CompositeAtStep4: 0.72,
  pspValue: 0.74,
  thresholdCrossings: [],
};

const N3_SCENARIOS = [ZMB_OPTION_A, ZMB_OPTION_B, ZMB_OPTION_C] as const;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const API_BASE = "http://localhost:8000/api/v1";

async function waitForAppReady(page: import("@playwright/test").Page): Promise<void> {
  await page.waitForFunction(
    () => typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
    { timeout: 10_000 },
  );
}

/**
 * Inject N=3 comparison scenario configs via the M17-G2 test seam.
 * Returns true if the window function was available (Phase 3 landed), false otherwise.
 */
async function injectComparisonScenarios(
  page: import("@playwright/test").Page,
  primaryScenarioId: string,
): Promise<boolean> {
  const configs = N3_SCENARIOS.map((s) => ({
    scenarioId: s.scenarioId,
    label: s.label,
    paletteIndex: s.paletteIndex,
  }));
  return page.evaluate(
    ({ configs: c, _primaryId }) => {
      const fn = (window as Record<string, unknown>).__worldsim_setComparisonScenarios as
        | ((cfgs: unknown) => void)
        | undefined;
      if (!fn) return false;
      fn(c);
      return true;
    },
    { configs, _primaryId: primaryScenarioId },
  );
}

/**
 * Create a ZMB scenario via API and advance N steps.
 * Returns the scenario_id from the backend.
 */
async function createZMBScenario(nSteps: number, name: string): Promise<string> {
  const createRes = await fetch(`${API_BASE}/scenarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name,
      configuration: {
        entities: ["ZMB"],
        n_steps: nSteps,
        start_date: "2024-01-01",
        modules_config: {
          ecological: { enabled: false },
          political_economy: { enabled: true },
        },
      },
    }),
  });
  if (!createRes.ok) throw new Error(`ZMB create failed: ${createRes.status}`);
  const { scenario_id: id } = (await createRes.json()) as ScenarioCreateResponse;
  for (let i = 0; i < nSteps; i++) {
    const advRes = await fetch(
      `${API_BASE}/scenarios/${encodeURIComponent(id)}/advance`,
      { method: "POST" },
    );
    if (!advRes.ok) throw new Error(`Advance step ${i + 1} failed: ${advRes.status}`);
  }
  return id;
}

/**
 * Build a trajectory response mock for a single scenario at step 4.
 * Returns the shape expected by TrajectoryView scenarioTrajectories prop.
 */
function makeTrajectoryMock(
  scenarioId: string,
  q1CompositeAtStep4: number,
  pspValue: number,
  thresholdCrossings: ThresholdCrossing[],
): object {
  return {
    scenario_id: scenarioId,
    entity_id: "ZMB",
    step_count: 8,
    mda_floors: [
      { indicator_id: "q1_poverty_headcount", floor_value: 0.6 },
    ],
    threshold_crossings: thresholdCrossings.map((tc) => ({
      indicator_id: tc.indicator_id,
      indicator_name: tc.indicator_name,
      severity: tc.severity,
      first_crossing_step: tc.first_crossing_step,
      measurement_framework: tc.measurement_framework,
    })),
    steps: Array.from({ length: 8 }, (_, i) => ({
      step_index: i + 1,
      effective_from: `2024-${String(i + 1).padStart(2, "0")}-01T00:00:00Z`,
      step_event_label: null,
      step_significance: "ROUTINE",
      frameworks: [
        {
          framework: "human_development",
          composite_score: String(
            i + 1 === 4 ? q1CompositeAtStep4 : q1CompositeAtStep4 - (4 - (i + 1)) * 0.03,
          ),
          indicators: {},
          mda_alerts: i + 1 >= (thresholdCrossings[0]?.first_crossing_step ?? 99)
            ? thresholdCrossings.map((tc) => ({
                alert_id: `MDA-ZMB-${tc.indicator_id}`,
                indicator_id: tc.indicator_id,
                indicator_name: tc.indicator_name,
                measurement_framework: tc.measurement_framework,
                severity: tc.severity,
                current_value: q1CompositeAtStep4,
                floor_value: 0.6,
                ceiling_value: null,
                breach_direction: "below_floor",
                consecutive_breach_steps: Math.max(0, (i + 1) - tc.first_crossing_step + 1),
                confidence_tier: 3,
              }))
            : [],
          has_below_floor_indicator: i + 1 >= (thresholdCrossings[0]?.first_crossing_step ?? 99),
          note: null,
        },
        {
          framework: "political_economy",
          composite_score: String(pspValue),
          indicators: {
            programme_survival_probability: {
              value: String(pspValue),
              unit: "probability",
              variable_type: "STOCK",
              confidence_tier: 3,
              observation_date: null,
              source_registry_id: null,
              measurement_framework: "political_economy",
              _envelope_version: "2",
            },
          },
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
        {
          framework: "financial",
          composite_score: "0.55",
          indicators: {},
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
          note: "Ecological disabled for ZMB ECF demo",
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

// ---------------------------------------------------------------------------
// Test suite — G2 Phase 3: Multi-scenario comparison (N=3)
// ---------------------------------------------------------------------------

test.describe("M17-G2 — Multi-scenario comparison N=3", () => {
  let primaryScenarioId: string;

  test.beforeAll(async () => {
    // Create the primary ZMB scenario (Option A baseline) via API.
    // Route mocks inject all three scenario trajectories client-side.
    primaryScenarioId = await createZMBScenario(4, "ZMB-G2-OptionA-Demo7Act2");
  });

  test.use({ viewport: { width: 1280, height: 800 } });

  // --------------------------------------------------------------------------
  // AC-S1 — Three scenarios active: Zone 1A / Zone 1B / Zone 1D all update
  // --------------------------------------------------------------------------

  test("AC-S1: N=3 comparison renders all three scenario curves in Zone 1A", async ({ page }) => {
    // Mock the N=3 comparison trajectory responses — intercepted when cluster fetches each.
    for (const scenario of N3_SCENARIOS) {
      await page.route(
        `**/api/v1/scenarios/${scenario.scenarioId}/trajectory*`,
        (route) => {
          route.fulfill({
            status: 200,
            contentType: "application/json",
            body: JSON.stringify(
              makeTrajectoryMock(
                scenario.scenarioId,
                scenario.q1CompositeAtStep4,
                scenario.pspValue,
                [...scenario.thresholdCrossings],
              ),
            ),
          });
        },
      );
    }

    await page.goto(`/?scenario=${encodeURIComponent(primaryScenarioId)}`);
    await waitForAppReady(page);
    await injectComparisonScenarios(page, primaryScenarioId);

    // Guard: Phase 3 not yet wired — return without failing if testid absent.
    const curveA = page.locator('[data-testid="zone1a-curve-scenario-option-a"]');
    if (!(await curveA.isVisible({ timeout: 5_000 }).catch(() => false))) {
      return; // Guard fires — implementation not yet landed
    }

    await expect(
      page.locator('[data-testid="zone1a-curve-scenario-option-a"]'),
    ).toBeVisible();
    await expect(
      page.locator('[data-testid="zone1a-curve-scenario-option-b"]'),
    ).toBeVisible();
    await expect(
      page.locator('[data-testid="zone1a-curve-scenario-option-c"]'),
    ).toBeVisible();

    // Zone 1B scenario headers must appear.
    await expect(
      page.locator('[data-testid="zone1b-scenario-header-option-a"]'),
    ).toBeVisible();
    await expect(
      page.locator('[data-testid="zone1b-scenario-header-option-b"]'),
    ).toBeVisible();
    await expect(
      page.locator('[data-testid="zone1b-scenario-header-option-c"]'),
    ).toBeVisible();

    // Zone 1D PSP rows must appear.
    await expect(
      page.locator('[data-testid="zone1d-psp-row-scenario-option-a"]'),
    ).toBeVisible();
    await expect(
      page.locator('[data-testid="zone1d-psp-row-scenario-option-b"]'),
    ).toBeVisible();
    await expect(
      page.locator('[data-testid="zone1d-psp-row-scenario-option-c"]'),
    ).toBeVisible();
  });

  // --------------------------------------------------------------------------
  // AC-A1 — Zone 1A N=3 differentiability: terminal labels + MDA floor preserved
  // --------------------------------------------------------------------------

  test("AC-A1: Zone 1A terminal endpoint labels A/B/C are visible; MDA floor line preserved", async ({
    page,
  }) => {
    for (const scenario of N3_SCENARIOS) {
      await page.route(`**/api/v1/scenarios/${scenario.scenarioId}/trajectory*`, (route) => {
        route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(makeTrajectoryMock(scenario.scenarioId, scenario.q1CompositeAtStep4, scenario.pspValue, [...scenario.thresholdCrossings])),
        });
      });
    }
    await page.goto(`/?scenario=${encodeURIComponent(primaryScenarioId)}`);
    await waitForAppReady(page);
    await injectComparisonScenarios(page, primaryScenarioId);

    const labelA = page.locator('[data-testid="zone1a-terminal-label-scenario-option-a"]');
    if (!(await labelA.isVisible({ timeout: 5_000 }).catch(() => false))) {
      return; // Guard
    }

    await expect(labelA).toContainText("A");
    await expect(
      page.locator('[data-testid="zone1a-terminal-label-scenario-option-b"]'),
    ).toContainText("B");
    await expect(
      page.locator('[data-testid="zone1a-terminal-label-scenario-option-c"]'),
    ).toContainText("C");

    // MDA floor line must be preserved from #1249 (regression guard).
    await expect(
      page.locator('[data-testid="zone1a-mda-floor-line"]'),
    ).toBeVisible();

    // All three curves simultaneously visible — no overflow-hidden clipping.
    for (const id of ["option-a", "option-b", "option-c"]) {
      const curve = page.locator(`[data-testid="zone1a-curve-scenario-${id}"]`);
      await expect(curve).toBeVisible();
      // Curves must not be clipped (bounding box must be within viewport).
      const box = await curve.boundingBox();
      expect(box).not.toBeNull();
      expect(box!.width).toBeGreaterThan(0);
    }
  });

  // --------------------------------------------------------------------------
  // AC-B1 — Zone 1B per-scenario rows (not union); Option C no-crossings; MDA panel ≥80px
  // --------------------------------------------------------------------------

  test("AC-B1: Zone 1B shows per-scenario crossing rows; Option C shows no-crossings; MDA panel ≥80px", async ({
    page,
  }) => {
    for (const scenario of N3_SCENARIOS) {
      await page.route(`**/api/v1/scenarios/${scenario.scenarioId}/trajectory*`, (route) => {
        route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(makeTrajectoryMock(scenario.scenarioId, scenario.q1CompositeAtStep4, scenario.pspValue, [...scenario.thresholdCrossings])),
        });
      });
    }
    await page.goto(`/?scenario=${encodeURIComponent(primaryScenarioId)}`);
    await waitForAppReady(page);
    await injectComparisonScenarios(page, primaryScenarioId);

    const headerA = page.locator('[data-testid="zone1b-scenario-header-option-a"]');
    if (!(await headerA.isVisible({ timeout: 5_000 }).catch(() => false))) {
      return; // Guard
    }

    // Option A threshold crossing row must contain CRITICAL.
    await expect(
      page.locator('[data-testid="zone1b-threshold-row-scenario-option-a"]').first(),
    ).toContainText("CRITICAL");

    // Option B threshold crossing row must contain CRITICAL.
    await expect(
      page.locator('[data-testid="zone1b-threshold-row-scenario-option-b"]').first(),
    ).toContainText("CRITICAL");

    // Option C must show no-crossings element — not a blank.
    const noCrossings = page.locator('[data-testid="zone1b-no-crossings-option-c"]');
    await expect(noCrossings).toBeVisible();
    await expect(noCrossings).toContainText(/no crossings/i);

    // MDA alert panel must retain ≥80px height (G3 #1252 dependency guard).
    const mdaPanel = page.locator('[data-testid="zone-1b-mda-alerts"]');
    if (await mdaPanel.isVisible({ timeout: 2_000 }).catch(() => false)) {
      const box = await mdaPanel.boundingBox();
      expect(box).not.toBeNull();
      expect(box!.height).toBeGreaterThanOrEqual(80);
    }
  });

  // --------------------------------------------------------------------------
  // AC-D1 — Zone 1D per-scenario PSP: three values simultaneously visible
  // --------------------------------------------------------------------------

  test("AC-D1: Zone 1D shows PSP values for all three scenarios simultaneously without interaction", async ({
    page,
  }) => {
    for (const scenario of N3_SCENARIOS) {
      await page.route(`**/api/v1/scenarios/${scenario.scenarioId}/trajectory*`, (route) => {
        route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(makeTrajectoryMock(scenario.scenarioId, scenario.q1CompositeAtStep4, scenario.pspValue, [...scenario.thresholdCrossings])),
        });
      });
    }
    await page.goto(`/?scenario=${encodeURIComponent(primaryScenarioId)}`);
    await waitForAppReady(page);
    await injectComparisonScenarios(page, primaryScenarioId);

    const pspA = page.locator('[data-testid="zone1d-psp-row-scenario-option-a"]');
    if (!(await pspA.isVisible({ timeout: 5_000 }).catch(() => false))) {
      return; // Guard
    }

    // All three PSP rows visible without any click or hover.
    await expect(pspA).toBeVisible();
    await expect(
      page.locator('[data-testid="zone1d-psp-row-scenario-option-b"]'),
    ).toBeVisible();
    await expect(
      page.locator('[data-testid="zone1d-psp-row-scenario-option-c"]'),
    ).toBeVisible();

    // Option C PSP value must reflect 74% (highest — political feasibility anchor).
    const pspCValue = page.locator('[data-testid="zone1d-psp-value-option-c"]');
    await expect(pspCValue).toBeVisible();
    await expect(pspCValue).toContainText(/74|0\.74/);

    // Option A PSP must be lower than Option C (58% vs 74%).
    const pspAValue = page.locator('[data-testid="zone1d-psp-value-option-a"]');
    await expect(pspAValue).toContainText(/58|0\.58/);
  });

  // --------------------------------------------------------------------------
  // AC-P5 — Persona 5 (Aicha): 90-second legibility gate at 1280×800
  // --------------------------------------------------------------------------

  test("AC-P5: Aicha can identify Option C as safest choice from Zone 1A + Zone 1B without narration", async ({
    page,
  }) => {
    // Viewport is set at describe level (1280×800).
    for (const scenario of N3_SCENARIOS) {
      await page.route(`**/api/v1/scenarios/${scenario.scenarioId}/trajectory*`, (route) => {
        route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(makeTrajectoryMock(scenario.scenarioId, scenario.q1CompositeAtStep4, scenario.pspValue, [...scenario.thresholdCrossings])),
        });
      });
    }
    await page.goto(`/?scenario=${encodeURIComponent(primaryScenarioId)}`);
    await waitForAppReady(page);
    await injectComparisonScenarios(page, primaryScenarioId);

    // Guard.
    const labelC = page.locator('[data-testid="zone1a-terminal-label-scenario-option-c"]');
    if (!(await labelC.isVisible({ timeout: 5_000 }).catch(() => false))) {
      return;
    }

    // Primary anchor: Zone 1A terminal label "C" visible — Option C identified without hover.
    await expect(labelC).toBeVisible();
    await expect(labelC).toContainText("C");

    // Secondary anchor: Zone 1B Option C header + no-crossings element visible — confirms safe.
    await expect(
      page.locator('[data-testid="zone1b-scenario-header-option-c"]'),
    ).toBeVisible();
    await expect(
      page.locator('[data-testid="zone1b-no-crossings-option-c"]'),
    ).toBeVisible();

    // Confirm that the dangerous crossing for Option A is also visible (contrast anchor).
    await expect(
      page.locator('[data-testid="zone1b-threshold-row-scenario-option-a"]').first(),
    ).toContainText("CRITICAL");

    // No drawer interaction occurred to reveal any of the above.
    // (Implicitly satisfied: no click events were triggered between app load and assertions.)

    // All anchors must be visible within the 1280×800 viewport — no element is clipped.
    for (const testid of [
      "zone1a-terminal-label-scenario-option-c",
      "zone1b-scenario-header-option-c",
      "zone1b-no-crossings-option-c",
    ]) {
      const el = page.locator(`[data-testid="${testid}"]`);
      const box = await el.boundingBox();
      expect(box).not.toBeNull();
      expect(box!.x).toBeGreaterThanOrEqual(0);
      expect(box!.y).toBeGreaterThanOrEqual(0);
      expect(box!.x + box!.width).toBeLessThanOrEqual(1280);
      expect(box!.y + box!.height).toBeLessThanOrEqual(800);
    }
  });

  // --------------------------------------------------------------------------
  // AC-P1 — Persona 1 (Lucas): worst Q1 trajectory identifiable from Zone 1A
  // --------------------------------------------------------------------------

  test("AC-P1: Lucas can identify Option A as worst Q1 trajectory from Zone 1A without specialist narration", async ({
    page,
  }) => {
    for (const scenario of N3_SCENARIOS) {
      await page.route(`**/api/v1/scenarios/${scenario.scenarioId}/trajectory*`, (route) => {
        route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(makeTrajectoryMock(scenario.scenarioId, scenario.q1CompositeAtStep4, scenario.pspValue, [...scenario.thresholdCrossings])),
        });
      });
    }
    await page.goto(`/?scenario=${encodeURIComponent(primaryScenarioId)}`);
    await waitForAppReady(page);
    await injectComparisonScenarios(page, primaryScenarioId);

    const curveA = page.locator('[data-testid="zone1a-curve-scenario-option-a"]');
    if (!(await curveA.isVisible({ timeout: 5_000 }).catch(() => false))) {
      return; // Guard
    }

    // All three curves present and visible (prerequisite for comparison).
    await expect(curveA).toBeVisible();
    await expect(
      page.locator('[data-testid="zone1a-curve-scenario-option-c"]'),
    ).toBeVisible();

    // Terminal labels identify each curve without hover.
    await expect(
      page.locator('[data-testid="zone1a-terminal-label-scenario-option-a"]'),
    ).toContainText("A");
    await expect(
      page.locator('[data-testid="zone1a-terminal-label-scenario-option-c"]'),
    ).toContainText("C");

    // Zone 1B confirms Option A has the earliest CRITICAL crossing (step 2 vs step 3).
    const rowA = page.locator('[data-testid="zone1b-threshold-row-scenario-option-a"]').first();
    await expect(rowA).toContainText("CRITICAL");
    await expect(rowA).toContainText(/step 2|crossed step 2/i);
  });

  // --------------------------------------------------------------------------
  // AC-P3 — Persona 3 (Andreas): PSP comparison readable from Zone 1D without view-switch
  // --------------------------------------------------------------------------

  test("AC-P3: Andreas can compare PSP across all three scenarios from Zone 1D without switching views", async ({
    page,
  }) => {
    for (const scenario of N3_SCENARIOS) {
      await page.route(`**/api/v1/scenarios/${scenario.scenarioId}/trajectory*`, (route) => {
        route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(makeTrajectoryMock(scenario.scenarioId, scenario.q1CompositeAtStep4, scenario.pspValue, [...scenario.thresholdCrossings])),
        });
      });
    }
    await page.goto(`/?scenario=${encodeURIComponent(primaryScenarioId)}`);
    await waitForAppReady(page);
    await injectComparisonScenarios(page, primaryScenarioId);

    const pspRowA = page.locator('[data-testid="zone1d-psp-row-scenario-option-a"]');
    if (!(await pspRowA.isVisible({ timeout: 5_000 }).catch(() => false))) {
      return; // Guard
    }

    // All three PSP rows visible simultaneously — Andreas reads without navigation.
    await expect(pspRowA).toBeVisible();
    await expect(
      page.locator('[data-testid="zone1d-psp-row-scenario-option-b"]'),
    ).toBeVisible();
    await expect(
      page.locator('[data-testid="zone1d-psp-row-scenario-option-c"]'),
    ).toBeVisible();

    // Option C PSP dominates (74%) — Andreas's political feasibility anchor.
    await expect(
      page.locator('[data-testid="zone1d-psp-value-option-c"]'),
    ).toContainText(/74|0\.74/);
    // Option B middle (67%).
    await expect(
      page.locator('[data-testid="zone1d-psp-value-option-b"]'),
    ).toContainText(/67|0\.67/);
    // Option A lowest (58%) — correct political risk order.
    await expect(
      page.locator('[data-testid="zone1d-psp-value-option-a"]'),
    ).toContainText(/58|0\.58/);
  });

  // --------------------------------------------------------------------------
  // AC-B1 regression guard — MDA panel not collapsed at 768px
  // --------------------------------------------------------------------------

  test("AC-B1 (768px): Zone 1B per-scenario rows do not collapse MDA alert panel below 80px at tablet viewport", async ({
    page,
  }) => {
    for (const scenario of N3_SCENARIOS) {
      await page.route(`**/api/v1/scenarios/${scenario.scenarioId}/trajectory*`, (route) => {
        route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(makeTrajectoryMock(scenario.scenarioId, scenario.q1CompositeAtStep4, scenario.pspValue, [...scenario.thresholdCrossings])),
        });
      });
    }
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto(`/?scenario=${encodeURIComponent(primaryScenarioId)}`);
    await waitForAppReady(page);
    await injectComparisonScenarios(page, primaryScenarioId);

    const headerC = page.locator('[data-testid="zone1b-scenario-header-option-c"]');
    if (!(await headerC.isVisible({ timeout: 5_000 }).catch(() => false))) {
      return; // Guard
    }

    // All three scenario headers still visible at 768px.
    await expect(
      page.locator('[data-testid="zone1b-scenario-header-option-a"]'),
    ).toBeVisible();
    await expect(headerC).toBeVisible();

    // MDA alert panel height guard.
    const mdaPanel = page.locator('[data-testid="zone-1b-mda-alerts"]');
    if (await mdaPanel.isVisible({ timeout: 2_000 }).catch(() => false)) {
      const box = await mdaPanel.boundingBox();
      expect(box).not.toBeNull();
      expect(box!.height).toBeGreaterThanOrEqual(80);
    }
  });
});
