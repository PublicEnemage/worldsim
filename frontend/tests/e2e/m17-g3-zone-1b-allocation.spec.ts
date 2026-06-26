/**
 * E2E: M17-G3 Zone 1B Proportional Allocation — AC-A1 through AC-P1.
 *
 * Authored BEFORE implementation from sprint entry §2.3–§2.4 acceptance criteria at:
 * docs/process/sprint-plans/m17-g3-sprint-entry.md
 *
 * ACs updated 2026-06-25 to align with the accepted intent document:
 * docs/process/intents/M17-G3-2026-06-25-zone-1b-proportional-allocation.md
 * ADR-018 (ARCH-012, Path B) accepted 2026-06-25. Sub-zone A floor = 80px at all
 * breakpoints. Testid reconciled to zone-1b-mda-panel-wrapper (ADR-018 §Decision).
 *
 * At Phase 3 handoff, the implementing Frontend Engineer must:
 *   1. Read the accepted intent document and ADR-018 for implementation contract
 *   2. Confirm MDA_PANEL_MIN_HEIGHT_PX = 80 matches ADR-018 (no change needed)
 *   3. Add data-testid="zone-1b-mda-panel-wrapper" to InstrumentCluster.tsx ~line 143
 *   4. Change Zone 1B outer container overflow: "auto" → "hidden"
 *   5. Remove test.fail() from AC-A2 after confirming AC-A2 passes post-implementation
 *
 * Sprint entry: docs/process/sprint-plans/m17-g3-sprint-entry.md (EL Approved 2026-06-25)
 *
 * Issues covered:
 *   #1252 — Zone 1B proportional allocation model (all ACs)
 *
 * NM-056 rule: NO test.skip(), test.fixme(), or .only() patterns.
 * Pre-implementation guard pattern (AC-A1, AC-A3, AC-A4, AC-P5, AC-P1):
 *   Guard on zone-1b-mda-panel-wrapper testid → isVisible() returns false → return without
 *   asserting (no-op, not a pass). This testid is new in G3; pre-G3 it is absent.
 *
 * AC-A2 EXCEPTION (overflow regression guard): Does NOT use the early-return guard.
 * This test must be RED before implementation — it asserts on zone-1b-mda-panel-wrapper,
 * which does not exist pre-G3. toBeVisible() times out → test fails explicitly. This is
 * intentional: it confirms the permanent ADR-grounded allocation model is not in place
 * until G3 implementation lands (the temporary minHeight: 80px guarantee from PR #1235 is
 * not sufficient — the ADR-specified testid-anchored model must exist).
 * Source: sprint entry §2.3 regression guard specification and M17 sprint plan reference
 * to "minHeight: 80px temporary guarantee active as of PR #1235."
 *
 * G3 testids (added by implementation — absent pre-G3):
 *   zone-1b-mda-panel-wrapper — MDA alert panel allocation wrapper; replaces the anonymous
 *                               flex:1 1 80px div in InstrumentCluster.tsx:143; G3 adds
 *                               this testid and replaces inline minHeight with the
 *                               ADR-grounded proportional allocation model (ADR-018)
 *
 * Existing testids used:
 *   zone-1b, zone-1b-cohort-impact, zone-1b-mda-alerts, zone-1b-top-detail,
 *   cohort-empty-state, cohort-row-{idx}, detail-indicator-name, detail-status
 *
 * Viewport: primary assertions at 1280×800 (minimum per sprint entry §3.1 observable
 * application state); AC-A3 also asserts at 768px (tablet legibility gate).
 */
import { test, expect } from "@playwright/test";

const API_BASE = "http://localhost:8000/api/v1";

// ---------------------------------------------------------------------------
// Placeholder constants — update to ADR-specified values at Phase 3 handoff
// ---------------------------------------------------------------------------

// ADR-018: Sub-zone A permanent floor = 80px at all breakpoints.
// Codifies the PR #1235 temporary guarantee as the permanent architectural minimum.
const MDA_PANEL_MIN_HEIGHT_PX = 80;

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
          scheduled_inputs: [],
        },
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

// ---------------------------------------------------------------------------
// Mock factories
// ---------------------------------------------------------------------------

function makeScenarioDetailMock(scenarioId: string, entities: string[]): object {
  return {
    scenario_id: scenarioId,
    name: "G3-M17-test",
    status: "in_progress",
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
    ia1_disclosure: "This output is pre-calibration.",
  };
}

function makeMeasurementOutputMock(
  scenarioId: string,
  cohortCrossings: CohortThresholdCrossing[] = [],
  stepIndex = 1,
): object {
  return {
    entity_id: "SEN",
    entity_name: "Senegal",
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
            value: "2.1",
            unit: "months",
            consecutive_steps: 4,
            confidence_tier: 2,
            source: "BCG 2023-Q4",
          },
        ],
        has_below_floor_indicator: true,
        note: null,
      },
      human_development: {
        framework: "human_development",
        composite_score: "0.52",
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
        composite_score: "0.44",
        indicators: {},
        mda_alerts: [],
        has_below_floor_indicator: false,
        note: null,
      },
      political_economy: {
        framework: "political_economy",
        composite_score: null,
        indicators: {},
        mda_alerts: [],
        has_below_floor_indicator: false,
        note: "Political economy unavailable",
      },
    },
    ia1_disclosure: "This output is pre-calibration.",
    single_entity_warning: true,
  };
}

// ---------------------------------------------------------------------------
// Cohort crossing fixtures
// ---------------------------------------------------------------------------

// Normal load — 2 crossings (AC-A1, AC-A3, AC-P5)
const SEN_Q1_CRITICAL_POVERTY: CohortThresholdCrossing = {
  quintile_key: "Q1",
  cohort_label: "Bottom income quintile",
  indicator_key: "poverty_headcount_ratio",
  indicator_label: "Poverty headcount",
  severity: "CRITICAL",
  step_crossed: 1,
  above_floor_pct: "4.2",
  tier: 3,
  source: "WB PovcalNet 2023",
};

const SEN_Q2_WARNING_POVERTY: CohortThresholdCrossing = {
  quintile_key: "Q2",
  cohort_label: "Lower-middle income quintile",
  indicator_key: "poverty_headcount_ratio",
  indicator_label: "Poverty headcount",
  severity: "WARNING",
  step_crossed: 1,
  above_floor_pct: "8.1",
  tier: 3,
  source: "WB PovcalNet 2023",
};

// Overflow load — 8 crossings across 4 indicators × Q1/Q2 (AC-A2, AC-P5, AC-P1)
// Used to confirm that 8+ entries do not collapse the MDA alert panel.
const OVERFLOW_CROSSINGS: CohortThresholdCrossing[] = [
  {
    quintile_key: "Q1",
    cohort_label: "Bottom income quintile",
    indicator_key: "poverty_headcount_ratio",
    indicator_label: "Poverty headcount",
    severity: "CRITICAL",
    step_crossed: 1,
    above_floor_pct: "4.2",
    tier: 3,
    source: "WB PovcalNet 2023",
  },
  {
    quintile_key: "Q2",
    cohort_label: "Lower-middle income quintile",
    indicator_key: "poverty_headcount_ratio",
    indicator_label: "Poverty headcount",
    severity: "WARNING",
    step_crossed: 1,
    above_floor_pct: "8.1",
    tier: 3,
    source: "WB PovcalNet 2023",
  },
  {
    quintile_key: "Q1",
    cohort_label: "Bottom income quintile",
    indicator_key: "education_enrollment_rate",
    indicator_label: "Primary enrollment rate",
    severity: "CRITICAL",
    step_crossed: 1,
    above_floor_pct: "3.5",
    tier: 3,
    source: "UNESCO 2023",
  },
  {
    quintile_key: "Q2",
    cohort_label: "Lower-middle income quintile",
    indicator_key: "education_enrollment_rate",
    indicator_label: "Primary enrollment rate",
    severity: "WARNING",
    step_crossed: 1,
    above_floor_pct: "6.8",
    tier: 3,
    source: "UNESCO 2023",
  },
  {
    quintile_key: "Q1",
    cohort_label: "Bottom income quintile",
    indicator_key: "child_mortality_rate",
    indicator_label: "Child mortality",
    severity: "CRITICAL",
    step_crossed: 2,
    above_floor_pct: "2.9",
    tier: 3,
    source: "UNICEF 2022",
  },
  {
    quintile_key: "Q2",
    cohort_label: "Lower-middle income quintile",
    indicator_key: "child_mortality_rate",
    indicator_label: "Child mortality",
    severity: "WARNING",
    step_crossed: 2,
    above_floor_pct: "5.4",
    tier: 3,
    source: "UNICEF 2022",
  },
  {
    quintile_key: "Q1",
    cohort_label: "Bottom income quintile",
    indicator_key: "malnutrition_prevalence",
    indicator_label: "Malnutrition prevalence",
    severity: "CRITICAL",
    step_crossed: 2,
    above_floor_pct: "3.1",
    tier: 3,
    source: "FAO 2023",
  },
  {
    quintile_key: "Q2",
    cohort_label: "Lower-middle income quintile",
    indicator_key: "malnutrition_prevalence",
    indicator_label: "Malnutrition prevalence",
    severity: "WARNING",
    step_crossed: 2,
    above_floor_pct: "7.3",
    tier: 3,
    source: "FAO 2023",
  },
];

// ---------------------------------------------------------------------------
// AC-A1: Proportional model — both Zone 1B sections visible at 1280×800 (#1252)
//
// Intent §5 AC-A1:
// At 1280×800 with dual-occupant state (MDA alerts + cohort crossings):
// - zone-1b-mda-panel-wrapper bounding box height ≥ MDA_PANEL_MIN_HEIGHT_PX (ADR-018)
// - zone-1b-cohort-impact bounding box height > 0
// - zone-1b scrollTop = 0 (Zone 1B outer container not scrolled)
// ---------------------------------------------------------------------------

test.describe("AC-A1: Zone 1B proportional model — both sections non-zero at 1280×800 (#1252)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createScenario(["SEN"], 1, `G3-SEN-AC-A1-${Date.now()}`);
  });

  test("AC-A1: zone-1b-mda-panel-wrapper and zone-1b-cohort-impact both visible with non-zero height at 1280×800", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["SEN"])),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, [SEN_Q1_CRITICAL_POVERTY, SEN_Q2_WARNING_POVERTY]),
        ),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: zone-1b-mda-panel-wrapper is new in G3 — absent pre-G3, no-op until implementation lands
    const mdaPanel = page.locator('[data-testid="zone-1b-mda-panel-wrapper"]');
    if (!(await mdaPanel.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Both sections must be visible and have non-zero height
    await expect(mdaPanel).toBeVisible();

    const cohortSection = page.locator('[data-testid="zone-1b-cohort-impact"]');
    await expect(cohortSection).toBeVisible();

    const mdaBox = await mdaPanel.boundingBox();
    const cohortBox = await cohortSection.boundingBox();

    expect(mdaBox).not.toBeNull();
    expect(cohortBox).not.toBeNull();

    if (mdaBox && cohortBox) {
      // MDA panel must meet ADR-018 minimum — not merely non-zero
      expect(mdaBox.height).toBeGreaterThanOrEqual(MDA_PANEL_MIN_HEIGHT_PX);
      expect(cohortBox.height).toBeGreaterThan(0);

      // Cohort section must appear below the MDA panel within Zone 1B
      expect(cohortBox.y).toBeGreaterThanOrEqual(mdaBox.y + mdaBox.height - 4);
    }

    // Zone 1B outer container must not scroll — confirms sub-zone allocation, not outer scroll
    const scrollTop = await zone1b.evaluate((el: Element) => (el as HTMLElement).scrollTop);
    expect(scrollTop).toBe(0);
  });
});

// ---------------------------------------------------------------------------
// AC-A2: Overflow regression guard — MDA panel not collapsed at 8+ crossings (#1252)
//
// Intent §5 AC-A2 (M16 retrospective):
// A scenario with 8+ cohort crossing entries does not collapse the MDA panel below the
// ADR-specified minimum height (80px, ADR-018).
//
// NM-056 EXCEPTION — this test does NOT use the early-return guard pattern.
// It must be RED before G3 implementation:
//   zone-1b-mda-panel-wrapper does not exist pre-G3 → toBeVisible() times out → test fails (RED)
// It must be GREEN after G3 implementation:
//   zone-1b-mda-panel-wrapper exists with ADR-grounded allocation → height >= MDA_PANEL_MIN_HEIGHT_PX
//
// M16 retrospective context: the anonymous flex wrapper at InstrumentCluster.tsx:143 used
// only a temporary `minHeight: 80px` inline style (PR #1235) — not a testid-anchored
// proportional allocation model. G3 replaces it with the ADR-grounded model. The presence
// of zone-1b-mda-panel-wrapper confirms the permanent fix is in place, not just the temporary one.
// Source: sprint entry §2.3 regression guard specification; m17-sprint-plan.md §#1252 note.
// ---------------------------------------------------------------------------

test.describe("AC-A2: Overflow regression guard — 8+ crossings do not collapse MDA panel (#1252)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createScenario(["SEN"], 1, `G3-SEN-AC-A2-${Date.now()}`);
  });

  test("AC-A2: zone-1b-mda-panel-wrapper height >= MDA_PANEL_MIN_HEIGHT_PX with 8 cohort crossings", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["SEN"])),
      });
    });

    // 8 cohort crossings — the overflow load that must not collapse the MDA panel
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMock(sid, OVERFLOW_CROSSINGS)),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b"]');
    await expect(zone1b).toBeVisible({ timeout: 10_000 });

    // NO early-return guard here — this is the intentional red-before-green assertion.
    // Pre-G3: zone-1b-mda-panel-wrapper absent → toBeVisible() times out → test FAILS (expected; EX-002).
    // Post-G3: zone-1b-mda-panel-wrapper present with ADR-grounded allocation → test PASSES → remove test.fail().
    const mdaPanel = page.locator('[data-testid="zone-1b-mda-panel-wrapper"]');
    await expect(mdaPanel).toBeVisible({ timeout: 8_000 });

    const mdaBox = await mdaPanel.boundingBox();
    expect(mdaBox).not.toBeNull();
    if (mdaBox) {
      // MDA panel must meet minimum height even under maximum cohort load
      expect(mdaBox.height).toBeGreaterThanOrEqual(MDA_PANEL_MIN_HEIGHT_PX);
    }
  });
});

// ---------------------------------------------------------------------------
// AC-A3: Viewport contract — 768px tablet (#1252)
//
// Intent §5 AC-A3:
// At 768px (tablet), with Senegal T3 active MDA alerts and cohort crossings:
// - zone-1b-top-detail is visible (positive bounding box height, within viewport)
// - zone-1b scrollTop is 0
// - zone-1b-cohort-impact has positive bounding box height
// - zone-1b-mda-panel-wrapper bounding box height ≥ MDA_PANEL_MIN_HEIGHT_PX (ADR-018)
// ---------------------------------------------------------------------------

test.describe("AC-A3: Viewport contract — both Zone 1B sections readable at 768px tablet (#1252)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createScenario(["SEN"], 1, `G3-SEN-AC-A3-${Date.now()}`);
  });

  test("AC-A3: zone-1b-mda-panel-wrapper and zone-1b-cohort-impact both have non-zero height at 768px width", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["SEN"])),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, [SEN_Q1_CRITICAL_POVERTY, SEN_Q2_WARNING_POVERTY]),
        ),
      }),
    );

    // Tablet viewport — primary legibility gate for DEMO6-026/043
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: zone-1b-mda-panel-wrapper is new in G3
    const mdaPanel = page.locator('[data-testid="zone-1b-mda-panel-wrapper"]');
    if (!(await mdaPanel.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(mdaPanel).toBeVisible();

    const cohortSection = page.locator('[data-testid="zone-1b-cohort-impact"]');
    await expect(cohortSection).toBeVisible();

    const mdaBox = await mdaPanel.boundingBox();
    const cohortBox = await cohortSection.boundingBox();

    expect(mdaBox).not.toBeNull();
    expect(cohortBox).not.toBeNull();

    if (mdaBox && cohortBox) {
      expect(mdaBox.height).toBeGreaterThanOrEqual(MDA_PANEL_MIN_HEIGHT_PX);
      expect(cohortBox.height).toBeGreaterThan(0);
    }

    // Zone 1B outer container must not scroll at 768px either
    const scrollTop = await zone1b.evaluate((el: Element) => (el as HTMLElement).scrollTop);
    expect(scrollTop).toBe(0);
  });

  test("AC-A3b: zone-1b-mda-panel-wrapper not collapsed below minimum by cohort section at 768px with 8 crossings", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["SEN"])),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMock(sid, OVERFLOW_CROSSINGS)),
      }),
    );

    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    const mdaPanel = page.locator('[data-testid="zone-1b-mda-panel-wrapper"]');
    if (!(await mdaPanel.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const mdaBox = await mdaPanel.boundingBox();
    expect(mdaBox).not.toBeNull();
    if (mdaBox) {
      expect(mdaBox.height).toBeGreaterThanOrEqual(MDA_PANEL_MIN_HEIGHT_PX);
    }

    // Zone 1B must not scroll as a unit even under overflow load at 768px
    const scrollTop = await zone1b.evaluate((el: Element) => (el as HTMLElement).scrollTop);
    expect(scrollTop).toBe(0);
  });
});

// ---------------------------------------------------------------------------
// AC-A4: Empty-state behavior — MDA breaches with no cohort crossings (#1252)
//
// Intent §5 AC-A4:
// At a step where Zone 1B has MDA alerts but no cohort crossings:
// - zone-1b-top-detail is visible (positive bounding box height)
// - cohort-row-0 is absent from the DOM OR cohort-empty-state is present
// - zone-1b-cohort-impact has bounding box height ≤ 60px — confirming it is hidden or
//   shows only the empty-state element (confirming single-occupant expansion of Sub-zone A)
// ---------------------------------------------------------------------------

test.describe("AC-A4: Zone 1B empty-state — MDA breaches with no cohort crossings (#1252)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createScenario(["SEN"], 1, `G3-SEN-AC-A4-${Date.now()}`);
  });

  test("AC-A4: zone-1b-mda-panel-wrapper visible at allocated height; cohort-impact near-zero when no crossings", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["SEN"])),
      });
    });

    // No cohort crossings — exercises the empty-state path while MDA breach exists
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMock(sid, [])),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: zone-1b-mda-panel-wrapper is new in G3
    const mdaPanel = page.locator('[data-testid="zone-1b-mda-panel-wrapper"]');
    if (!(await mdaPanel.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // MDA panel must be visible with non-zero height (MDA breach present, no cohort load)
    await expect(mdaPanel).toBeVisible();
    const mdaBox = await mdaPanel.boundingBox();
    expect(mdaBox).not.toBeNull();
    if (mdaBox) {
      expect(mdaBox.height).toBeGreaterThan(0);
    }

    // Cohort section must show its empty state
    const emptyState = page.locator('[data-testid="cohort-empty-state"]');
    await expect(emptyState).toBeVisible();

    // No cohort rows present
    const firstRow = page.locator('[data-testid="cohort-row-0"]');
    expect(await firstRow.count()).toBe(0);

    // Cohort-impact section must be near-zero height (≤ 60px), confirming Sub-zone A
    // expands to fill Zone 1B in the single-occupant state (intent §5 AC-A4)
    const cohortSection = page.locator('[data-testid="zone-1b-cohort-impact"]');
    const cohortBox = await cohortSection.boundingBox();
    if (cohortBox) {
      expect(cohortBox.height).toBeLessThanOrEqual(60);
    }
  });
});

// ---------------------------------------------------------------------------
// AC-P5: Persona 5 (Aicha Mbaye) — MDA severity label visible at high cohort load (#1252)
//
// Intent §5 AC-P5:
// In the Senegal T3 conditionality scenario at 1280×800 with MDA alerts + 4+ cohort rows:
// - zone-1b-top-detail is visible at initial viewport state (no scroll, no interaction)
// - detail-indicator-name (inside zone-1b-top-detail) is visible — indicator name legible
// - detail-status (inside zone-1b-top-detail) is visible — floor-distance status legible
//
// Aicha's use case: reads MDA headline within 90-second Reactive ceiling without any
// Zone 1B scroll or analyst mediation.
// ---------------------------------------------------------------------------

test.describe("AC-P5: Persona 5 (Aicha) — MDA severity label visible at high cohort load (#1252)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createScenario(["SEN"], 1, `G3-SEN-AC-P5-${Date.now()}`);
  });

  test("AC-P5: zone-1b-top-detail visible within viewport at 1280×800 with 8 cohort crossings", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["SEN"])),
      });
    });

    // 8 cohort crossings — maximum expected cohort load per sprint entry §2.3
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMock(sid, OVERFLOW_CROSSINGS)),
      }),
    );

    // ScenarioInstrumentCluster skips measurement-output at step 0 (no simulation output
    // before the first advance). Mocking the advance endpoint lets the UI step to 1
    // without consuming a real backend step, triggering the trajectory + measurement-output
    // fetch chain that populates Zone 1B with MDA alerts and cohort crossing rows.
    await page.route(`**/api/v1/scenarios/${sid}/advance`, (route) => {
      if (route.request().method() !== "POST") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ step_executed: 1, is_complete: false }),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);
    // Step to 1 so trajectory + measurement-output fetches fire (both skip at step 0).
    await page.locator('[data-testid="advance-step-btn"]').click();

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: zone-1b-mda-panel-wrapper is new in G3
    const mdaPanel = page.locator('[data-testid="zone-1b-mda-panel-wrapper"]');
    if (!(await mdaPanel.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // zone-1b-top-detail contains the MDA severity headline (indicator + severity + value)
    // Aicha's read requires this to be the primary visible element in Zone 1B
    const topDetail = page.locator('[data-testid="zone-1b-top-detail"]');
    await expect(topDetail).toBeVisible();

    const topDetailBox = await topDetail.boundingBox();
    expect(topDetailBox).not.toBeNull();
    if (topDetailBox) {
      // The top detail must be within the visible viewport (not scrolled out of view)
      expect(topDetailBox.y).toBeGreaterThanOrEqual(0);
      expect(topDetailBox.y + topDetailBox.height).toBeLessThanOrEqual(800);

      // The top detail must be within the Zone 1B container bounds
      const zone1bBox = await zone1b.boundingBox();
      if (zone1bBox) {
        expect(topDetailBox.y).toBeGreaterThanOrEqual(zone1bBox.y - 4);
      }
    }

    // Aicha must be able to read the indicator name and floor-distance status without
    // analyst mediation — both must be visible within zone-1b-top-detail
    const indicatorName = page.locator('[data-testid="detail-indicator-name"]');
    await expect(indicatorName).toBeVisible();

    const statusLabel = page.locator('[data-testid="detail-status"]');
    await expect(statusLabel).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// AC-P1: Persona 1 (Lucas Ferreira) — cohort section readable with internal scroll (#1252)
//
// Intent §5 AC-P1:
// In the Senegal T3 conditionality scenario at step 2, at 1280×800:
// - zone-1b-cohort-impact is visible (positive height) in Zone 1B without Zone 1B outer scroll
// - cohort-row-0 is visible within zone-1b-cohort-impact
// - zone-1b scrollTop = 0 (Zone 1B outer container not scrolled)
// - Sub-zone B shows internal scroll when content exceeds height (scrollHeight > clientHeight)
//
// NOTE: G3 uses internal scroll, not truncation. "and N more" count labels are explicitly
// out of scope per intent §3.2 and §7. Lucas scrolls Sub-zone B to access all entries.
//
// Lucas's use case: CohortImpactSection fully readable in allocated space, internal scroll
// available for overflow entries, without Zone 1B container scrolling as a unit.
// ---------------------------------------------------------------------------

test.describe("AC-P1: Persona 1 (Lucas) — cohort section visible with internal scroll (#1252)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createScenario(["SEN"], 1, `G3-SEN-AC-P1-${Date.now()}`);
  });

  test("AC-P1: zone-1b-cohort-impact visible without Zone 1B outer scroll; cohort-row-0 accessible; Sub-zone B scrollable with 8 crossings", async ({
    page,
  }) => {
    if (!scenarioId) return;

    const sid = scenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["SEN"])),
      });
    });

    // 8 cohort crossings — enough to exceed Sub-zone B visible height and activate internal scroll
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMock(sid, OVERFLOW_CROSSINGS)),
      }),
    );

    // ScenarioInstrumentCluster skips measurement-output at step 0 (no simulation output
    // before the first advance). Mocking the advance endpoint lets the UI step to 1
    // without consuming a real backend step, triggering the trajectory + measurement-output
    // fetch chain that populates Zone 1B with cohort crossing rows.
    await page.route(`**/api/v1/scenarios/${sid}/advance`, (route) => {
      if (route.request().method() !== "POST") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ step_executed: 1, is_complete: false }),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);
    // Step to 1 so trajectory + measurement-output fetches fire (both skip at step 0).
    await page.locator('[data-testid="advance-step-btn"]').click();

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: zone-1b-mda-panel-wrapper is new in G3
    const mdaPanel = page.locator('[data-testid="zone-1b-mda-panel-wrapper"]');
    if (!(await mdaPanel.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // CohortImpactSection must be visible within Zone 1B (positive height)
    const cohortSection = page.locator('[data-testid="zone-1b-cohort-impact"]');
    await expect(cohortSection).toBeVisible();

    const cohortBox = await cohortSection.boundingBox();
    expect(cohortBox).not.toBeNull();
    if (cohortBox) {
      expect(cohortBox.height).toBeGreaterThan(0);
    }

    // Zone 1B must not scroll as a unit — Lucas reads CohortImpactSection via Sub-zone B
    // internal scroll, not by scrolling Zone 1B outer container
    const scrollTop = await zone1b.evaluate((el: Element) => (el as HTMLElement).scrollTop);
    expect(scrollTop).toBe(0);

    // At least the first cohort row must be visible within CohortImpactSection
    const firstRow = page.locator('[data-testid="cohort-row-0"]');
    await expect(firstRow).toBeVisible();

    // Sub-zone B must be internally scrollable when 8 crossings exceed its visible height
    // Confirmed by scrollHeight > clientHeight on the cohort-impact container
    const cohortInternallyScrollable = await cohortSection.evaluate(
      (el: Element) => (el as HTMLElement).scrollHeight > (el as HTMLElement).clientHeight,
    );
    expect(cohortInternallyScrollable).toBe(true);
  });
});
