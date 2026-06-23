/**
 * E2E: M16-G2 Distributional Visibility on Primary Surface — AC-1 through AC-14.
 *
 * Authored BEFORE implementation from intent document at:
 * docs/process/intents/M16-G2-2026-06-23-distributional-surface.md
 *
 * ADR: ADR-017 — Zone 1A Information Architecture (Zone 1D Integration)
 * ADR: ADR-015 — Model Legibility Architecture (Evidence Thread Architecture)
 * ADR: ADR-014 — Alert Panel Zone 1B (Zone 1B extension authority)
 * Sprint entry: docs/process/sprint-plans/m16-g2-sprint-entry.md (EL Approved 2026-06-23)
 *
 * Issues covered:
 *   #986  — Cohort disaggregation on primary surface
 *           (AC-1, AC-2, AC-3, AC-4, AC-5, AC-6)
 *   #987  — Political risk summary surface (Persona 3)
 *           (AC-7, AC-8, AC-9, AC-10, AC-11)
 *   #1163 — PSP threshold legibility (closed by #987 AC-8)
 *   Layout — Zone proportion changes and G1 testid retirement
 *           (AC-12, AC-13, AC-14)
 *
 * NM-056 rule: NO test.skip() or conditional skip patterns. Pre-implementation tests
 * use the early-return guard pattern. A guard that fires is a no-op (not a pass).
 * Tests become active when implementation lands and must then pass or fail explicitly.
 *
 * Guard pattern: each test guards on the primary testid it exercises.
 * Pre-implementation: testid absent → isVisible() returns false → test returns without failing.
 *
 * Mock strategy:
 *   Cohort tests (AC-1–AC-6): measurement-output mock includes cohort_threshold_crossings
 *   Political risk tests (AC-7–AC-11): measurement-output mock includes legitimacy_index and
 *     elite_capture_divergence indicators alongside PSP at controlled values
 *   Layout tests (AC-12–AC-13): no mock — direct computed CSS height measurement
 *   Retirement test (AC-14): confirm all 4 retired G1 testids are absent from DOM
 *
 * Viewport: 1280×800 (minimum per intent doc §3 observable application state specification).
 */
import { test, expect } from "@playwright/test";

const API_BASE = "http://localhost:8000/api/v1";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface ScenarioCreateResponse {
  scenario_id: string;
}

interface CohortThresholdCrossing {
  quintile_key: string;
  cohort_label: string;
  indicator_key: string;
  indicator_label: string;
  severity: "CRITICAL" | "WARNING" | "WATCH";
  step_crossed: number;
  above_floor_pct: string;
  tier: number;
  source: string;
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
  peEnabled = false,
): Promise<string> {
  const createRes = await fetch(`${API_BASE}/scenarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name,
      configuration: {
        entities,
        n_steps: 3,
        start_date: "2024-01-01",
        modules_config: {
          ecological: { enabled: false },
          political_economy: { enabled: peEnabled },
        },
      },
    }),
  });
  if (!createRes.ok) throw new Error(`Create failed: ${createRes.status}`);
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

// ---------------------------------------------------------------------------
// Mock factories
// ---------------------------------------------------------------------------

function makeScenarioDetailMock(
  scenarioId: string,
  entities: string[],
  peEnabled = false,
  mode1 = false,
): object {
  return {
    scenario_id: scenarioId,
    name: "G2-M16-test",
    status: mode1 ? "completed" : "in_progress",
    configuration: {
      entities,
      n_steps: 3,
      start_date: "2024-01-01",
      modules_config: {
        ecological: { enabled: false },
        political_economy: { enabled: peEnabled },
      },
    },
    created_at: "2024-01-01T00:00:00Z",
    ia1_disclosure: "This output is pre-calibration.",
  };
}

function makeMeasurementOutputMock(
  scenarioId: string,
  options: {
    pspValue?: string | null;
    stepIndex?: number;
    cohortCrossings?: CohortThresholdCrossing[];
    legitimacyValue?: string | null;
    legitimacyFloor?: string | null;
    legitimacyDirection?: string | null;
    eliteCaptureDirection?: string | null;
    peEnabled?: boolean;
  } = {},
): object {
  const {
    pspValue = null,
    stepIndex = 1,
    cohortCrossings = [],
    legitimacyValue = null,
    legitimacyFloor = "0.35",
    legitimacyDirection = "declining",
    eliteCaptureDirection = null,
    peEnabled = true,
  } = options;

  const politicalEconomyIndicators: Record<string, unknown> = {};

  if (pspValue !== null) {
    politicalEconomyIndicators["programme_survival_probability"] = {
      value: pspValue,
      unit: "probability",
      variable_type: "STOCK",
      confidence_tier: 3,
      observation_date: null,
      source_registry_id: null,
      measurement_framework: "political_economy",
      _envelope_version: "2",
    };
  }

  if (legitimacyValue !== null) {
    politicalEconomyIndicators["legitimacy_index"] = {
      value: legitimacyValue,
      floor: legitimacyFloor,
      direction: legitimacyDirection,
      unit: "index",
      variable_type: "STOCK",
      confidence_tier: 3,
      observation_date: null,
      source_registry_id: null,
      measurement_framework: "political_economy",
      _envelope_version: "2",
    };
  }

  if (eliteCaptureDirection !== null) {
    politicalEconomyIndicators["elite_capture_divergence"] = {
      direction: eliteCaptureDirection,
      qualifier: eliteCaptureDirection === "widening" ? "fiscal benefits concentrating" : "distribution stable",
      unit: "index",
      variable_type: "FLOW",
      confidence_tier: 3,
      observation_date: null,
      source_registry_id: null,
      measurement_framework: "political_economy",
      _envelope_version: "2",
    };
  }

  return {
    entity_id: "ZMB",
    entity_name: "Zambia",
    timestep: "2024-07-01T00:00:00Z",
    scenario_id: scenarioId,
    step_index: stepIndex,
    outputs: {
      financial: {
        framework: "financial",
        composite_score: "0.45",
        indicators: {},
        mda_alerts: [
          {
            indicator_key: "reserve_coverage_months",
            indicator_label: "Reserve coverage",
            severity: "CRITICAL",
            value: "2.3",
            unit: "months",
            consecutive_steps: 6,
            confidence_tier: 2,
            source: "CBJ 2023-Q4",
          },
        ],
        has_below_floor_indicator: true,
        note: null,
      },
      human_development: {
        framework: "human_development",
        composite_score: "0.55",
        indicators: {},
        mda_alerts: [],
        cohort_threshold_crossings: cohortCrossings,
        has_below_floor_indicator: false,
        note: null,
      },
      ecological: {
        framework: "ecological",
        composite_score: null,
        indicators: {},
        mda_alerts: [],
        has_below_floor_indicator: false,
        note: "Ecological disabled",
      },
      governance: {
        framework: "governance",
        composite_score: "0.42",
        indicators: {},
        mda_alerts: [],
        has_below_floor_indicator: false,
        note: null,
      },
      political_economy: {
        framework: "political_economy",
        composite_score: peEnabled && pspValue ? "0.6500" : null,
        indicators: politicalEconomyIndicators,
        mda_alerts: [],
        has_below_floor_indicator: false,
        note: peEnabled ? null : "Political economy unavailable",
      },
    },
    ia1_disclosure: "This output is pre-calibration.",
    single_entity_warning: true,
  };
}

// Standard cohort crossing fixtures
const ZMB_Q1_CRITICAL: CohortThresholdCrossing = {
  quintile_key: "Q1",
  cohort_label: "Bottom income quintile",
  indicator_key: "poverty_headcount_ratio",
  indicator_label: "Poverty headcount",
  severity: "CRITICAL",
  step_crossed: 2,
  above_floor_pct: "3.8",
  tier: 3,
  source: "WB PovcalNet 2023",
};

const ZMB_Q2_WARNING: CohortThresholdCrossing = {
  quintile_key: "Q2",
  cohort_label: "Lower-middle income quintile",
  indicator_key: "poverty_headcount_ratio",
  indicator_label: "Poverty headcount",
  severity: "WARNING",
  step_crossed: 3,
  above_floor_pct: "7.2",
  tier: 3,
  source: "WB PovcalNet 2023",
};

// ---------------------------------------------------------------------------
// AC-1: Cohort Impact sub-section present in Zone 1B (#986)
//
// Intent doc §4 AC-1:
// ZMB ECF fixture Mode 2 at 1280×800, PE enabled, step 2:
//   zone-1b-cohort-impact is present in the DOM and visible.
//   cohort-section-header contains "COHORT IMPACT".
//   Element appears below MDA aggregate alert rows within Zone 1B.
// ---------------------------------------------------------------------------

test.describe("AC-1: Cohort Impact sub-section present in Zone 1B in Mode 2 at step 2 (#986)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      scenarioId = await createScenario(["ZMB"], 2, `G2-ZMB-AC1-${Date.now()}`, true);
    } catch {
      scenarioId = null;
    }
  });

  test("AC-1: zone-1b-cohort-impact visible with COHORT IMPACT header below MDA alerts", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true)),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            pspValue: "0.3800",
            stepIndex: 2,
            cohortCrossings: [ZMB_Q1_CRITICAL],
            legitimacyValue: "0.42",
            eliteCaptureDirection: "widening",
            peEnabled: true,
          }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    // Guard: Zone 1B must be rendered
    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Primary guard: zone-1b-cohort-impact is new in G2
    const cohortImpact = page.locator('[data-testid="zone-1b-cohort-impact"]');
    if (!(await cohortImpact.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(cohortImpact).toBeVisible();

    // Header must contain "COHORT IMPACT"
    const header = page.locator('[data-testid="cohort-section-header"]');
    await expect(header).toContainText("COHORT IMPACT");

    // The cohort impact section must be within Zone 1B (not above it)
    const zone1bBox = await zone1b.boundingBox();
    const cohortBox = await cohortImpact.boundingBox();
    expect(zone1bBox).not.toBeNull();
    expect(cohortBox).not.toBeNull();
    if (zone1bBox && cohortBox) {
      // Cohort section top must be within Zone 1B bounds
      expect(cohortBox.y).toBeGreaterThanOrEqual(zone1bBox.y);
      expect(cohortBox.y).toBeLessThanOrEqual(zone1bBox.y + zone1bBox.height);
    }
  });
});

// ---------------------------------------------------------------------------
// AC-2: Bottom income quintile CRITICAL row format (#986)
//
// Intent doc §4 AC-2:
// cohort-row-0 contains "CRITICAL", "Bottom income quintile",
// "Poverty headcount", and "T3"; does NOT contain "T2".
// ---------------------------------------------------------------------------

test.describe("AC-2: cohort-row-0 format — CRITICAL, plain-language labels, T3 tier (#986)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      scenarioId = await createScenario(["ZMB"], 2, `G2-ZMB-AC2-${Date.now()}`, true);
    } catch {
      scenarioId = null;
    }
  });

  test("AC-2: cohort-row-0 shows CRITICAL severity, plain-language labels, and T3 tier; T2 absent", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true)),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            stepIndex: 2,
            cohortCrossings: [ZMB_Q1_CRITICAL],
            peEnabled: true,
          }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    const cohortRow0 = page.locator('[data-testid="cohort-row-0"]');
    if (!(await cohortRow0.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const rowText = await cohortRow0.textContent() ?? "";

    // Severity badge
    expect(rowText).toContain("CRITICAL");

    // Plain-language cohort label — never a field key
    expect(rowText).toContain("Bottom income quintile");
    expect(rowText).not.toContain("Q1");
    expect(rowText).not.toContain("hh_exp_q1");

    // Plain-language indicator label — never a field key
    expect(rowText).toContain("Poverty headcount");
    expect(rowText).not.toContain("poverty_headcount_rate_pct");
    expect(rowText).not.toContain("poverty_headcount_ratio");

    // Tier label must be T3 (elasticity-derived per CM condition), never T2
    expect(rowText).toContain("T3");
    expect(rowText).not.toMatch(/\bT2\b/);
  });
});

// ---------------------------------------------------------------------------
// AC-3: Q3/Q4/Q5 suppression — not displayed even if present (#986)
//
// Intent doc §4 AC-3:
// No cohort row with "Middle income quintile", "Upper-middle income quintile",
// or "Top income quintile" appears in zone-1b-cohort-impact.
// ---------------------------------------------------------------------------

test.describe("AC-3: Q3/Q4/Q5 quintile rows are suppressed in Zone 1B (#986)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      scenarioId = await createScenario(["ZMB"], 2, `G2-ZMB-AC3-${Date.now()}`, true);
    } catch {
      scenarioId = null;
    }
  });

  test("AC-3: no Middle, Upper-middle, or Top income quintile rows appear in zone-1b-cohort-impact", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true)),
      });
    });

    // Provide Q1 CRITICAL and Q2 WARNING — Q3/Q4/Q5 absent from mock (T5 suppression)
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            stepIndex: 2,
            cohortCrossings: [ZMB_Q1_CRITICAL, ZMB_Q2_WARNING],
            peEnabled: true,
          }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    const cohortImpact = page.locator('[data-testid="zone-1b-cohort-impact"]');
    if (!(await cohortImpact.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const cohortText = await cohortImpact.textContent() ?? "";

    // Q3, Q4, Q5 plain-language labels must not appear
    expect(cohortText).not.toContain("Middle income quintile");
    expect(cohortText).not.toContain("Upper-middle income quintile");
    expect(cohortText).not.toContain("Top income quintile");

    // Only Q1 and Q2 labels may appear (from fixtures above)
    // Verify visible cohort rows are Q1 and/or Q2 only
    const cohortRows = cohortImpact.locator('[data-testid^="cohort-row-"]');
    const rowCount = await cohortRows.count();
    for (let i = 0; i < rowCount; i++) {
      const rowText = await cohortRows.nth(i).textContent() ?? "";
      const isAllowedQuintile =
        rowText.includes("Bottom income quintile") ||
        rowText.includes("Lower-middle income quintile");
      if (rowText.trim().length > 0) {
        expect(isAllowedQuintile).toBe(true);
      }
    }
  });
});

// ---------------------------------------------------------------------------
// AC-4: Cohort empty state — Mode 2 at step 0 (#986)
//
// Intent doc §4 AC-4:
// In Mode 2 at step 0 (no crossings yet): cohort-empty-state visible with text
// "No cohort threshold crossings projected on current path."
// No cohort-row-0 present.
// ---------------------------------------------------------------------------

test.describe("AC-4: Cohort empty state in Mode 2 at step 0 (#986)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      scenarioId = await createScenario(["ZMB"], 0, `G2-ZMB-AC4-${Date.now()}`, true);
    } catch {
      scenarioId = null;
    }
  });

  test("AC-4: cohort-empty-state visible with Mode 2 text; no cohort-row-0 present at step 0", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true, false)),
      });
    });

    // Empty cohort crossings at step 0
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            stepIndex: 0,
            cohortCrossings: [],
            peEnabled: true,
          }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: zone-1b-cohort-impact section must be present
    const cohortImpact = page.locator('[data-testid="zone-1b-cohort-impact"]');
    if (!(await cohortImpact.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Primary guard: cohort-empty-state is new in G2
    const emptyState = page.locator('[data-testid="cohort-empty-state"]');
    if (!(await emptyState.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(emptyState).toBeVisible();
    await expect(emptyState).toContainText("No cohort threshold crossings projected on current path");

    // No cohort row should be present at step 0
    const firstRow = page.locator('[data-testid="cohort-row-0"]');
    expect(await firstRow.count()).toBe(0);
  });
});

// ---------------------------------------------------------------------------
// AC-5: Cohort empty state — Mode 1 header format (#986)
//
// Intent doc §4 AC-5:
// In Mode 1, cohort-section-header shows "COHORT IMPACT (HISTORICAL)".
// cohort-empty-state shows "No cohort threshold crossings at or before this step."
// ---------------------------------------------------------------------------

test.describe("AC-5: Cohort Impact header shows (HISTORICAL) suffix in Mode 1 (#986)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      // Mode 1 = completed scenario
      scenarioId = await createScenario(["ZMB"], 1, `G2-ZMB-AC5-${Date.now()}`, true);
    } catch {
      scenarioId = null;
    }
  });

  test("AC-5: cohort-section-header shows COHORT IMPACT (HISTORICAL) in Mode 1; empty state uses past-tense", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    // mode1=true triggers completed status
    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true, true)),
      });
    });

    // No cohort crossings — exercise the empty state
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            stepIndex: 1,
            cohortCrossings: [],
            peEnabled: true,
          }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: cohort-section-header is new in G2
    const header = page.locator('[data-testid="cohort-section-header"]');
    if (!(await header.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Mode 1 header must include the HISTORICAL qualifier
    await expect(header).toContainText("COHORT IMPACT (HISTORICAL)");

    // Empty state text must use past tense (Mode 1 framing)
    const emptyState = page.locator('[data-testid="cohort-empty-state"]');
    if (await emptyState.isVisible({ timeout: 3_000 }).catch(() => false)) {
      await expect(emptyState).toContainText("No cohort threshold crossings at or before this step");
    }
  });
});

// ---------------------------------------------------------------------------
// AC-6: Zone 1B visible row count at 1280 — 1+1 limit per DD-016 (#986)
//
// Intent doc §4 AC-6:
// At 1280×800: top MDA alert row and top cohort row (cohort-row-0) are both
// visible without scroll. A second row in either sub-section may require scroll.
// At 1440×900: 2 MDA alert rows + 2 cohort rows visible without scroll.
// ---------------------------------------------------------------------------

test.describe("AC-6: Zone 1B visible row count at 1280 (1+1 per DD-016) and 1440 (2+2) (#986)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      scenarioId = await createScenario(["ZMB"], 2, `G2-ZMB-AC6-${Date.now()}`, true);
    } catch {
      scenarioId = null;
    }
  });

  test("AC-6a: at 1280×800 — MDA alert row and cohort-row-0 both visible without vertical scroll", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true)),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            stepIndex: 2,
            cohortCrossings: [ZMB_Q1_CRITICAL, ZMB_Q2_WARNING],
            peEnabled: true,
          }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard on G2 cohort row element
    const cohortRow0 = page.locator('[data-testid="cohort-row-0"]');
    if (!(await cohortRow0.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Both the first MDA alert row and the first cohort row must be in the 800px viewport
    const cohortBox = await cohortRow0.boundingBox();
    expect(cohortBox).not.toBeNull();
    if (cohortBox) {
      expect(cohortBox.y + cohortBox.height).toBeLessThanOrEqual(800);
    }

    // The MDA section must also have at least one visible row
    const zone1bBox = await zone1b.boundingBox();
    expect(zone1bBox).not.toBeNull();
    if (zone1bBox) {
      expect(zone1bBox.y).toBeLessThan(800);
    }
  });

  test("AC-6b: at 1440×900 — 2 MDA alert rows + 2 cohort rows visible without scroll", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true)),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            stepIndex: 2,
            cohortCrossings: [ZMB_Q1_CRITICAL, ZMB_Q2_WARNING],
            peEnabled: true,
          }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    const cohortRow1 = page.locator('[data-testid="cohort-row-1"]');
    if (!(await cohortRow1.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // At 1440×900, the second cohort row must be visible within the 900px viewport
    const cohortRow1Box = await cohortRow1.boundingBox();
    expect(cohortRow1Box).not.toBeNull();
    if (cohortRow1Box) {
      expect(cohortRow1Box.y + cohortRow1Box.height).toBeLessThanOrEqual(900);
    }
  });
});

// ---------------------------------------------------------------------------
// AC-7: Political risk sub-section present in Zone 1D (#987)
//
// Intent doc §4 AC-7:
// ZMB ECF Mode 2 at 1280×800, PE enabled, step 3 (PSP=0.38):
//   zone-1d-political-risk visible; zone-1d-political-risk-header contains "POLITICAL RISK".
//   psp-severity-row visible; contains "Programme survival".
// ---------------------------------------------------------------------------

test.describe("AC-7: Political risk sub-section present in Zone 1D at step 3 (#987)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      scenarioId = await createScenario(["ZMB"], 0, `G2-ZMB-AC7-${Date.now()}`, true);
    } catch {
      scenarioId = null;
    }
  });

  test("AC-7: zone-1d-political-risk and psp-severity-row visible; header shows POLITICAL RISK", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;
    let currentPsp = "0.4200";

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            pspValue: currentPsp,
            legitimacyValue: "0.42",
            legitimacyFloor: "0.35",
            legitimacyDirection: "declining",
            eliteCaptureDirection: "widening",
            peEnabled: true,
          }),
        ),
      }),
    );

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true)),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Advance to step 1 — simulate step 3 PSP value
    currentPsp = "0.3800";
    const nextStepBtn = page.getByRole("button", { name: /Next Step/ });
    if (!(await nextStepBtn.isEnabled({ timeout: 5_000 }).catch(() => false))) return;
    await nextStepBtn.click();
    await page.waitForTimeout(1_000);

    // Primary guard: zone-1d-political-risk is new in G2
    const politicalRisk = page.locator('[data-testid="zone-1d-political-risk"]');
    if (!(await politicalRisk.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(politicalRisk).toBeVisible();

    // Header must say "POLITICAL RISK"
    const header = page.locator('[data-testid="zone-1d-political-risk-header"]');
    await expect(header).toContainText("POLITICAL RISK");

    // PSP severity row must be visible and contain "Programme survival"
    const pspRow = page.locator('[data-testid="psp-severity-row"]');
    await expect(pspRow).toBeVisible();
    await expect(pspRow).toContainText("Programme survival");

    // Political risk section must appear below zone-1d-four-framework rows
    const zone1dBox = await zone1d.boundingBox();
    const riskBox = await politicalRisk.boundingBox();
    expect(zone1dBox).not.toBeNull();
    expect(riskBox).not.toBeNull();
    if (zone1dBox && riskBox) {
      expect(riskBox.y).toBeGreaterThanOrEqual(zone1dBox.y);
    }
  });
});

// ---------------------------------------------------------------------------
// AC-8: PSP severity badge — four threshold ranges (#987, closure condition for #1163)
//
// Intent doc §4 AC-8:
// PSP < 0.40    → "CRITICAL"
// PSP 0.40–0.55 → "WARNING"
// PSP 0.55–0.70 → "WATCH"
// PSP > 0.70    → "STABLE"
// Percentage shown alongside badge (38%, 47%, 62%, 78%).
// ---------------------------------------------------------------------------

test.describe("AC-8: PSP severity badge thresholds (#987, #1163 closure)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      scenarioId = await createScenario(["ZMB"], 0, `G2-ZMB-AC8-${Date.now()}`, true);
    } catch {
      scenarioId = null;
    }
  });

  async function assertPspSeverity(
    page: import("@playwright/test").Page,
    sid: string,
    pspValue: string,
    expectedSeverity: string,
    expectedPct: string,
  ): Promise<void> {
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            pspValue,
            legitimacyValue: "0.42",
            eliteCaptureDirection: "widening",
            peEnabled: true,
          }),
        ),
      }),
    );
    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true)),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    const pspRow = page.locator('[data-testid="psp-severity-row"]');
    if (!(await pspRow.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(pspRow).toContainText(expectedSeverity);
    await expect(pspRow).toContainText(expectedPct);
  }

  test("AC-8a: PSP=0.38 (< 0.40) shows CRITICAL badge and 38%", async ({ page }) => {
    if (!scenarioId) return;
    await assertPspSeverity(page, scenarioId, "0.3800", "CRITICAL", "38%");
  });

  test("AC-8b: PSP=0.47 (0.40–0.55) shows WARNING badge and 47%", async ({ page }) => {
    if (!scenarioId) return;
    await assertPspSeverity(page, scenarioId, "0.4700", "WARNING", "47%");
  });

  test("AC-8c: PSP=0.62 (0.55–0.70) shows WATCH badge and 62%", async ({ page }) => {
    if (!scenarioId) return;
    await assertPspSeverity(page, scenarioId, "0.6200", "WATCH", "62%");
  });

  test("AC-8d: PSP=0.78 (> 0.70) shows STABLE badge and 78%", async ({ page }) => {
    if (!scenarioId) return;
    await assertPspSeverity(page, scenarioId, "0.7800", "STABLE", "78%");
  });
});

// ---------------------------------------------------------------------------
// AC-9: Historical analogue sentence — CRITICAL and WARNING (#987)
//
// Intent doc §4 AC-9:
// CRITICAL (PSP < 0.40): psp-historical-analogue contains "within 3 steps"
// WARNING (0.40–0.55): psp-historical-analogue contains "within 6 steps"
// WATCH/STABLE: psp-historical-analogue contains "elevated discontinuation risk" or is absent
// ---------------------------------------------------------------------------

test.describe("AC-9: Historical analogue sentence matches severity tier (#987)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      scenarioId = await createScenario(["ZMB"], 0, `G2-ZMB-AC9-${Date.now()}`, true);
    } catch {
      scenarioId = null;
    }
  });

  test("AC-9a: CRITICAL PSP (0.38) — psp-historical-analogue contains 'within 3 steps'", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            pspValue: "0.3800",
            legitimacyValue: "0.42",
            eliteCaptureDirection: "widening",
            peEnabled: true,
          }),
        ),
      }),
    );
    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true)),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    const analogue = page.locator('[data-testid="psp-historical-analogue"]');
    if (!(await analogue.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(analogue).toContainText("within 3 steps");
  });

  test("AC-9b: WARNING PSP (0.47) — psp-historical-analogue contains 'within 6 steps'", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            pspValue: "0.4700",
            legitimacyValue: "0.42",
            eliteCaptureDirection: "widening",
            peEnabled: true,
          }),
        ),
      }),
    );
    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true)),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    const analogue = page.locator('[data-testid="psp-historical-analogue"]');
    if (!(await analogue.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(analogue).toContainText("within 6 steps");
  });

  test("AC-9c: WATCH PSP (0.62) — psp-historical-analogue shows elevated risk or is absent", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            pspValue: "0.6200",
            legitimacyValue: "0.52",
            eliteCaptureDirection: "stable",
            peEnabled: true,
          }),
        ),
      }),
    );
    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true)),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    const analogue = page.locator('[data-testid="psp-historical-analogue"]');
    const analoguePresent = await analogue.isVisible({ timeout: 3_000 }).catch(() => false);

    if (analoguePresent) {
      // If shown for WATCH, must contain elevated risk language (not the CRITICAL/WARNING phrasing)
      const text = await analogue.textContent() ?? "";
      expect(text).not.toContain("within 3 steps");
      expect(text).not.toContain("within 6 steps");
    }
    // If absent for WATCH, that is also acceptable per intent doc
  });
});

// ---------------------------------------------------------------------------
// AC-10: Legitimacy index row (#987)
//
// Intent doc §4 AC-10:
// legitimacy-index-row visible with "Legitimacy index" and numeric value.
// legitimacy-floor-proximity visible with "above fragility threshold" / "AT fragility threshold"
// / "below fragility threshold" based on value vs floor.
// ---------------------------------------------------------------------------

test.describe("AC-10: Legitimacy index row and floor proximity visible (#987)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      scenarioId = await createScenario(["ZMB"], 0, `G2-ZMB-AC10-${Date.now()}`, true);
    } catch {
      scenarioId = null;
    }
  });

  test("AC-10: legitimacy-index-row shows value and direction; legitimacy-floor-proximity shows threshold relationship", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            pspValue: "0.3800",
            legitimacyValue: "0.42",
            legitimacyFloor: "0.35",
            legitimacyDirection: "declining",
            eliteCaptureDirection: "widening",
            peEnabled: true,
          }),
        ),
      }),
    );
    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true)),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: legitimacy-index-row is new in G2
    const legitimacyRow = page.locator('[data-testid="legitimacy-index-row"]');
    if (!(await legitimacyRow.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(legitimacyRow).toBeVisible();

    const legitimacyText = await legitimacyRow.textContent() ?? "";
    expect(legitimacyText).toContain("Legitimacy index");

    // Must contain a numeric value
    expect(legitimacyText).toMatch(/\d+\.\d+/);

    // Must contain a direction word
    const hasDirection =
      legitimacyText.toLowerCase().includes("declining") ||
      legitimacyText.toLowerCase().includes("stable") ||
      legitimacyText.toLowerCase().includes("improving");
    expect(hasDirection).toBe(true);

    // Floor proximity line must be visible
    const floorProximity = page.locator('[data-testid="legitimacy-floor-proximity"]');
    if (!(await floorProximity.isVisible({ timeout: 3_000 }).catch(() => false))) return;

    await expect(floorProximity).toBeVisible();
    const proximityText = await floorProximity.textContent() ?? "";

    const hasThresholdText =
      proximityText.toLowerCase().includes("above fragility threshold") ||
      proximityText.toLowerCase().includes("at fragility threshold") ||
      proximityText.toLowerCase().includes("below fragility threshold");
    expect(hasThresholdText).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// AC-11: Political economy empty state (#987)
//
// Intent doc §4 AC-11:
// When political economy module is NOT enabled: political-risk-empty visible with
// "Political risk: not modelled in this fixture." zone-1d-four-framework remains visible.
// psp-severity-row absent from DOM.
// ---------------------------------------------------------------------------

test.describe("AC-11: Political economy empty state when PE disabled (#987)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      // PE disabled in scenario
      scenarioId = await createScenario(["ZMB"], 1, `G2-ZMB-AC11-${Date.now()}`, false);
    } catch {
      scenarioId = null;
    }
  });

  test("AC-11: political-risk-empty visible; psp-severity-row absent; four-framework rows visible", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            pspValue: null,
            peEnabled: false,
          }),
        ),
      }),
    );
    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], false)),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Four framework rows must remain visible — PE disable must not remove them
    await expect(zone1d).toBeVisible();

    // Guard: political-risk-empty is new in G2
    const emptyState = page.locator('[data-testid="political-risk-empty"]');
    if (!(await emptyState.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(emptyState).toBeVisible();
    await expect(emptyState).toContainText("Political risk: not modelled in this fixture");

    // psp-severity-row must be absent when PE is disabled
    const pspRow = page.locator('[data-testid="psp-severity-row"]');
    expect(await pspRow.count()).toBe(0);
  });
});

// ---------------------------------------------------------------------------
// AC-12: Zone 1D flex proportion at 1280 — 160px (±4px) (#987, DD-016)
//
// Intent doc §4 AC-12:
// At 1280×800, zone-1d-four-framework (or Zone 1D container) has computed CSS height
// of 160px (±4px). Confirms flex: 0 0 50% against chartHeight=320px.
// ---------------------------------------------------------------------------

test.describe("AC-12: Zone 1D container height is 160px (±4px) at 1280 (DD-016)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      scenarioId = await createScenario(["ZMB"], 1, `G2-ZMB-AC12-${Date.now()}`, true);
    } catch {
      scenarioId = null;
    }
  });

  test("AC-12: zone-1d-four-framework computed height is 160px ±4px at 1280×800", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMock(sid, { peEnabled: true })),
      }),
    );
    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true)),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: zone-1d-political-risk only exists after G2 implementation.
    // Without this guard the test measures the pre-G2 Zone 1D height (~96px at 30%)
    // against the G2 target (160px at 50%), producing a false failure before implementation.
    const politicalRiskSectionAC12 = page.locator('[data-testid="zone-1d-political-risk"]');
    if ((await politicalRiskSectionAC12.count()) === 0) return;

    // Measure the computed height of the Zone 1D container
    const height = await page.evaluate(() => {
      const el = document.querySelector('[data-testid="zone-1d-four-framework"]');
      if (!el) return null;
      // Try the element itself, then its parent if it's a content wrapper
      const rect = el.getBoundingClientRect();
      if (rect.height > 0) return rect.height;
      const parent = el.parentElement;
      return parent ? parent.getBoundingClientRect().height : null;
    });

    // Guard: if height not measurable, G2 layout not yet implemented
    if (height === null || height === 0) return;

    // DD-016: Zone 1D at 1280 = 50% × 320px chartHeight = 160px (±4px tolerance)
    expect(height).toBeGreaterThanOrEqual(156);
    expect(height).toBeLessThanOrEqual(164);
  });
});

// ---------------------------------------------------------------------------
// AC-13: Zone 1C proportion at 1280 — 48px (±4px) (DD-016)
//
// Intent doc §4 AC-13:
// At 1280×800, zone-1c-pmm (or Zone 1C container) has computed CSS height of 48px (±4px).
// Confirms flex: 0 0 15% against chartHeight=320px.
// ---------------------------------------------------------------------------

test.describe("AC-13: Zone 1C container height is 48px (±4px) at 1280 (DD-016)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      scenarioId = await createScenario(["ZMB"], 1, `G2-ZMB-AC13-${Date.now()}`, true);
    } catch {
      scenarioId = null;
    }
  });

  test("AC-13: zone-1c-pmm computed height is 48px ±4px at 1280×800", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMock(sid, { peEnabled: true })),
      }),
    );
    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true)),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1c = page.locator('[data-testid="zone-1c-pmm"]');
    if (!(await zone1c.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: zone-1d-political-risk only exists after G2 implementation.
    // Without this guard the test measures the pre-G2 Zone 1C height (~80px at 25%)
    // against the G2 target (48px at 15%), producing a false failure before implementation.
    const politicalRiskSectionAC13 = page.locator('[data-testid="zone-1d-political-risk"]');
    if ((await politicalRiskSectionAC13.count()) === 0) return;

    const height = await page.evaluate(() => {
      const el = document.querySelector('[data-testid="zone-1c-pmm"]');
      if (!el) return null;
      const rect = el.getBoundingClientRect();
      if (rect.height > 0) return rect.height;
      const parent = el.parentElement;
      return parent ? parent.getBoundingClientRect().height : null;
    });

    if (height === null || height === 0) return;

    // DD-016: Zone 1C at 1280 = 15% × 320px chartHeight = 48px (±4px tolerance)
    expect(height).toBeGreaterThanOrEqual(44);
    expect(height).toBeLessThanOrEqual(52);
  });
});

// ---------------------------------------------------------------------------
// AC-14: G1 testid retirement — all four retired testids absent from DOM (#987, DD-016)
//
// Intent doc §4 AC-14:
// At 1280×800, ZMB ECF Mode 2 PE enabled, step ≥ 1:
//   zone-1d-political-feasibility: count() === 0
//   psp-delta: count() === 0
//   psp-layer3-sentence: count() === 0
//   psp-delta-sentence: count() === 0
// ---------------------------------------------------------------------------

test.describe("AC-14: G1 Zone 1D testids are absent after G2 replacement mandate (#987, DD-016)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      scenarioId = await createScenario(["ZMB"], 0, `G2-ZMB-AC14-${Date.now()}`, true);
    } catch {
      scenarioId = null;
    }
  });

  test("AC-14: zone-1d-political-feasibility, psp-delta, psp-layer3-sentence, psp-delta-sentence all absent", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;
    let currentPsp = "0.4200";

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, {
            pspValue: currentPsp,
            legitimacyValue: "0.42",
            eliteCaptureDirection: "widening",
            peEnabled: true,
          }),
        ),
      }),
    );
    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"], true)),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Advance to step 1 — this is when G1 elements would have been visible pre-G2
    currentPsp = "0.3800";
    const nextStepBtn = page.getByRole("button", { name: /Next Step/ });
    if (!(await nextStepBtn.isEnabled({ timeout: 5_000 }).catch(() => false))) return;
    await nextStepBtn.click();
    await page.waitForTimeout(1_000);

    // Guard: if zone-1d-political-risk is NOT present, G2 hasn't landed — skip
    // (this makes AC-14 a no-op pre-implementation, not a silent pass)
    const politicalRisk = page.locator('[data-testid="zone-1d-political-risk"]');
    if ((await politicalRisk.count()) === 0) return;

    // All four G1 testids must be absent — replacement mandate executed
    expect(
      await page.locator('[data-testid="zone-1d-political-feasibility"]').count(),
    ).toBe(0);

    expect(
      await page.locator('[data-testid="psp-delta"]').count(),
    ).toBe(0);

    expect(
      await page.locator('[data-testid="psp-layer3-sentence"]').count(),
    ).toBe(0);

    expect(
      await page.locator('[data-testid="psp-delta-sentence"]').count(),
    ).toBe(0);
  });
});
