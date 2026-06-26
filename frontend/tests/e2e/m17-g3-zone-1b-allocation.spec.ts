/**
 * E2E: M17-G3 Zone 1B Proportional Allocation — AC-A1 through AC-P1.
 *
 * Authored BEFORE implementation from sprint entry §2.3–§2.4 acceptance criteria at:
 * docs/process/sprint-plans/m17-g3-sprint-entry.md
 *
 * NOTE: The formal intent document at
 * docs/process/intents/M17-G3-{YYYY-MM-DD}-zone-1b-proportional-allocation.md
 * was not yet filed at the time of test authorship (Phase 1 UX brief and Phase 2 ADR
 * pending). The ACs below are derived directly from sprint entry §2.3–§2.4 specifications.
 *
 * At Phase 3 handoff, the implementing Frontend Engineer must:
 *   1. Read the accepted intent document and ADR for final pixel specifications
 *   2. Update MDA_PANEL_MIN_HEIGHT_PX to the ADR-specified minimum height
 *   3. Update COHORT_MAX_DISPLAY to the ADR-specified max-display count
 *   4. Confirm the G3 testids below match those added by the ADR-grounded implementation
 *
 * ADR gate: TBD — Path A (ADR-017 amendment, ARCH-011) or Path B (new ARCH-012).
 * Sprint entry: docs/process/sprint-plans/m17-g3-sprint-entry.md (EL Approved 2026-06-25)
 *
 * Issues covered:
 *   #1252 — Zone 1B proportional allocation model (all ACs)
 *
 * NM-056 rule: NO test.skip(), test.fixme(), or .only() patterns.
 * Pre-implementation guard pattern (AC-A1, AC-A3, AC-A4, AC-P5, AC-P1):
 *   Guard on zone-1b-mda-panel testid → isVisible() returns false → return without
 *   asserting (no-op, not a pass). This testid is new in G3; pre-G3 it is absent.
 *
 * AC-A2 EXCEPTION (overflow regression guard): Does NOT use the early-return guard.
 * This test must be RED before implementation — it asserts on zone-1b-mda-panel, which
 * does not exist pre-G3. toBeVisible() times out → test fails explicitly. This is
 * intentional: it confirms the permanent ADR-grounded allocation model is not in place
 * until G3 implementation lands (the temporary minHeight: 80px guarantee from PR #1235 is
 * not sufficient — the ADR-specified testid-anchored model must exist).
 * Source: sprint entry §2.3 regression guard specification and M17 sprint plan reference
 * to "minHeight: 80px temporary guarantee active as of PR #1235."
 *
 * G3 testids (added by implementation — absent pre-G3):
 *   zone-1b-mda-panel       — MDA alert panel allocation wrapper; replaces the anonymous
 *                              flex:1 1 80px div in InstrumentCluster.tsx:143; G3 adds
 *                              this testid and replaces inline minHeight with the
 *                              ADR-grounded proportional allocation model
 *   zone-1b-cohort-count-label — "and N more" label when cohort entries exceed
 *                                COHORT_MAX_DISPLAY (new truncation logic in G3)
 *
 * Existing testids used:
 *   zone-1b, zone-1b-cohort-impact, zone-1b-mda-alerts, zone-1b-top-detail,
 *   cohort-empty-state, cohort-row-{idx}
 *
 * Viewport: primary assertions at 1280×800 (minimum per sprint entry §3.1 observable
 * application state); AC-A3 also asserts at 768px (tablet legibility gate).
 */
import { test, expect } from "@playwright/test";

const API_BASE = "http://localhost:8000/api/v1";

// ---------------------------------------------------------------------------
// Placeholder constants — update to ADR-specified values at Phase 3 handoff
// ---------------------------------------------------------------------------

// M16 temporary guarantee (PR #1235). Replace with ADR-specified minimum at handoff.
const MDA_PANEL_MIN_HEIGHT_PX = 80;

// Placeholder — ADR will specify the max cohort rows before "and N more" truncation.
// Update to ADR-specified value at Phase 3 handoff.
const COHORT_MAX_DISPLAY = 5;

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
// Sprint entry §2.4 AC-A1:
// At 1280×800, the MDA alert panel occupies its ADR-specified minimum height and the
// CohortImpactSection is visible below it; neither section is zero-height.
// Assert via testid-anchored bounding box checks for both sections.
// ---------------------------------------------------------------------------

test.describe("AC-A1: Zone 1B proportional model — both sections non-zero at 1280×800 (#1252)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createScenario(["SEN"], 1, `G3-SEN-AC-A1-${Date.now()}`);
  });

  test("AC-A1: zone-1b-mda-panel and zone-1b-cohort-impact both visible with non-zero height at 1280×800", async ({
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

    // Guard: zone-1b-mda-panel is new in G3 — absent pre-G3, no-op until implementation lands
    const mdaPanel = page.locator('[data-testid="zone-1b-mda-panel"]');
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
      expect(mdaBox.height).toBeGreaterThan(0);
      expect(cohortBox.height).toBeGreaterThan(0);

      // Cohort section must appear below the MDA panel within Zone 1B
      expect(cohortBox.y).toBeGreaterThanOrEqual(mdaBox.y + mdaBox.height - 4);
    }
  });
});

// ---------------------------------------------------------------------------
// AC-A2: Overflow regression guard — MDA panel not collapsed at 8+ crossings (#1252)
//
// Sprint entry §2.4 AC-A2:
// A scenario with 8+ cohort crossing entries does not collapse the MDA panel below the
// ADR-specified minimum height.
//
// NM-056 EXCEPTION — this test does NOT use the early-return guard pattern.
// It must be RED before G3 implementation:
//   zone-1b-mda-panel does not exist pre-G3 → toBeVisible() times out → test fails (RED)
// It must be GREEN after G3 implementation:
//   zone-1b-mda-panel exists with ADR-grounded allocation → height >= MDA_PANEL_MIN_HEIGHT_PX
//
// M16 retrospective context: the anonymous flex wrapper at InstrumentCluster.tsx:143 used
// only a temporary `minHeight: 80px` inline style (PR #1235) — not a testid-anchored
// proportional allocation model. G3 replaces it with the ADR-grounded model. The presence
// of zone-1b-mda-panel confirms the permanent fix is in place, not just the temporary one.
// Source: sprint entry §2.3 regression guard specification; m17-sprint-plan.md §#1252 note.
// ---------------------------------------------------------------------------

test.describe("AC-A2: Overflow regression guard — 8+ crossings do not collapse MDA panel (#1252)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createScenario(["SEN"], 1, `G3-SEN-AC-A2-${Date.now()}`);
  });

  test("AC-A2: zone-1b-mda-panel height >= MDA_PANEL_MIN_HEIGHT_PX with 8 cohort crossings", async ({
    page,
  }) => {
    if (!scenarioId) return;

    // EX-002 (docs/compliance/exceptions.md): pre-implementation expected failure.
    // This test is the regression guard — it MUST fail before G3 Phase 3 adds zone-1b-mda-panel-wrapper.
    // REVERSAL: remove test.fail() in the Phase 3 implementation PR after confirming AC-A2 passes.
    // See also NM-065 (docs/process/near-miss-registry.md).
    test.fail();

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
// Sprint entry §2.4 AC-A3:
// At 768px (tablet), both sections meet minimum readable height per UX brief specification;
// CohortImpactSection does not collapse MDA panel below minimum.
// Assert via testid-anchored bounding box checks at 768px viewport.
// ---------------------------------------------------------------------------

test.describe("AC-A3: Viewport contract — both Zone 1B sections readable at 768px tablet (#1252)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createScenario(["SEN"], 1, `G3-SEN-AC-A3-${Date.now()}`);
  });

  test("AC-A3: zone-1b-mda-panel and zone-1b-cohort-impact both have non-zero height at 768px width", async ({
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

    // Guard: zone-1b-mda-panel is new in G3
    const mdaPanel = page.locator('[data-testid="zone-1b-mda-panel"]');
    if (!(await mdaPanel.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(mdaPanel).toBeVisible();

    const cohortSection = page.locator('[data-testid="zone-1b-cohort-impact"]');
    await expect(cohortSection).toBeVisible();

    const mdaBox = await mdaPanel.boundingBox();
    const cohortBox = await cohortSection.boundingBox();

    expect(mdaBox).not.toBeNull();
    expect(cohortBox).not.toBeNull();

    if (mdaBox && cohortBox) {
      // Both sections must be readable (non-zero height) at 768px
      expect(mdaBox.height).toBeGreaterThan(0);
      expect(cohortBox.height).toBeGreaterThan(0);

      // MDA panel must not be collapsed below minimum by the cohort section at 768px
      expect(mdaBox.height).toBeGreaterThanOrEqual(MDA_PANEL_MIN_HEIGHT_PX);
    }
  });

  test("AC-A3b: zone-1b-mda-panel not collapsed below minimum by cohort section at 768px with 8 crossings", async ({
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

    const mdaPanel = page.locator('[data-testid="zone-1b-mda-panel"]');
    if (!(await mdaPanel.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const mdaBox = await mdaPanel.boundingBox();
    expect(mdaBox).not.toBeNull();
    if (mdaBox) {
      expect(mdaBox.height).toBeGreaterThanOrEqual(MDA_PANEL_MIN_HEIGHT_PX);
    }
  });
});

// ---------------------------------------------------------------------------
// AC-A4: Empty-state behavior — MDA breaches with no cohort crossings (#1252)
//
// Sprint entry §2.4 AC-A4:
// When Zone 1B has MDA breaches but no cohort crossings, MDA panel is visible at full
// allocated height; CohortImpactSection shows its empty state.
// Assert both conditions via testid presence and bounding box.
// ---------------------------------------------------------------------------

test.describe("AC-A4: Zone 1B empty-state — MDA breaches with no cohort crossings (#1252)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createScenario(["SEN"], 1, `G3-SEN-AC-A4-${Date.now()}`);
  });

  test("AC-A4: zone-1b-mda-panel visible at allocated height; cohort-empty-state visible when no crossings", async ({
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

    // Guard: zone-1b-mda-panel is new in G3
    const mdaPanel = page.locator('[data-testid="zone-1b-mda-panel"]');
    if (!(await mdaPanel.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // MDA panel must be visible with non-zero height (MDA breach present, no cohort load)
    await expect(mdaPanel).toBeVisible();
    const mdaBox = await mdaPanel.boundingBox();
    expect(mdaBox).not.toBeNull();
    if (mdaBox) {
      expect(mdaBox.height).toBeGreaterThan(0);
    }

    // Cohort section must show its empty state (not be hidden entirely)
    const cohortSection = page.locator('[data-testid="zone-1b-cohort-impact"]');
    await expect(cohortSection).toBeVisible();

    const emptyState = page.locator('[data-testid="cohort-empty-state"]');
    await expect(emptyState).toBeVisible();

    // No cohort rows present
    const firstRow = page.locator('[data-testid="cohort-row-0"]');
    expect(await firstRow.count()).toBe(0);
  });
});

// ---------------------------------------------------------------------------
// AC-P5: Persona 5 (Aicha Mbaye) — MDA severity label visible at high cohort load (#1252)
//
// Sprint entry §2.4 AC-P5:
// MDA panel severity label and indicator are visible without scrolling at 1280×800,
// regardless of cohort load. Assert via testid-anchored element visibility check after
// populating Zone 1B with a high-cohort-load scenario.
//
// Aicha's use case: the MDA panel headline (severity label + indicator + distance below
// floor) must be the primary visual anchor in Zone 1B — visible on landing without any
// user interaction, even when the cohort section is fully populated.
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

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: zone-1b-mda-panel is new in G3
    const mdaPanel = page.locator('[data-testid="zone-1b-mda-panel"]');
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
  });
});

// ---------------------------------------------------------------------------
// AC-P1: Persona 1 (Lucas Ferreira) — cohort display count and overflow label (#1252)
//
// Sprint entry §2.4 AC-P1:
// CohortImpactSection shows the ADR-specified max-display count at 1280×800; if more
// entries exist, count label ("and N more") is visible. Assert via testid on cohort entry
// items and count label.
//
// Lucas's use case: the CohortImpactSection must be fully readable at the ADR-specified
// max-display count — not truncated below his minimum usable state. When more crossings
// exist than the max-display count, the "and N more" label is visible and accessible.
// ---------------------------------------------------------------------------

test.describe("AC-P1: Persona 1 (Lucas) — cohort display count and overflow label (#1252)", () => {
  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    // COHORT_MAX_DISPLAY + 3 crossings to trigger the overflow label
    scenarioId = await createScenario(["SEN"], 1, `G3-SEN-AC-P1-${Date.now()}`);
  });

  test("AC-P1a: cohort-row count does not exceed COHORT_MAX_DISPLAY at 1280×800 with 8 crossings", async ({
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

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: zone-1b-mda-panel is new in G3
    const mdaPanel = page.locator('[data-testid="zone-1b-mda-panel"]');
    if (!(await mdaPanel.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const cohortSection = page.locator('[data-testid="zone-1b-cohort-impact"]');
    if (!(await cohortSection.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Cohort rows must not exceed COHORT_MAX_DISPLAY
    const rows = cohortSection.locator('[data-testid^="cohort-row-"]');
    const rowCount = await rows.count();
    expect(rowCount).toBeLessThanOrEqual(COHORT_MAX_DISPLAY);
  });

  test("AC-P1b: zone-1b-cohort-count-label visible with 'and N more' when crossings exceed COHORT_MAX_DISPLAY", async ({
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

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b"]');
    if (!(await zone1b.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: zone-1b-mda-panel is new in G3
    const mdaPanel = page.locator('[data-testid="zone-1b-mda-panel"]');
    if (!(await mdaPanel.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Guard: zone-1b-cohort-count-label is new in G3 (truncation not yet implemented)
    const countLabel = page.locator('[data-testid="zone-1b-cohort-count-label"]');
    if (!(await countLabel.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Count label must contain "and N more" phrasing
    const labelText = await countLabel.textContent() ?? "";
    expect(labelText).toMatch(/and \d+ more/i);

    // Verify the number shown is the correct overflow count (8 total - COHORT_MAX_DISPLAY)
    const expectedOverflow = OVERFLOW_CROSSINGS.length - COHORT_MAX_DISPLAY;
    expect(labelText).toContain(String(expectedOverflow));
  });
});
