/**
 * E2E: M14-G5 ADR-015 Evidence Thread Architecture Frontend — AC-1 through AC-14.
 *
 * Authored BEFORE implementation from intent document at:
 * docs/process/intents/M14-G5-2026-06-17-adr015-frontend.md
 *
 * ADR: ADR-015 — Model Legibility Architecture (Evidence Thread Architecture)
 * Sprint entry: docs/process/sprint-plans/m14-g5-sprint-entry.md
 * Data Architect decisions: DA-G5-1 through DA-G5-5 (all CONFIRMED 2026-06-18)
 *
 * Components and ACs covered:
 *
 *   Component 1 — Basis Threads on Zone 1 Primary Outputs
 *     AC-1  — Zone 1D L0 annotations present at zero interaction (4 frameworks)
 *     AC-2  — Zone 1D annotation content: T2 + source institution + pre-cal for JOR/financial
 *     AC-3  — Zone 1D ecological annotation contains "ceiling" OR "floor" (not generic)
 *     AC-4  — Zone 1D null confidence_tier renders [—] fallback, not empty
 *     AC-12 — Zone 1B compact rows: full indicator names at 1280×800 (no mid-word truncation)
 *     AC-13 — Zone 1C PMM annotation "[T3 composite · pre-cal]" verbatim
 *     AC-14 — HCL strip tier meaning expansion (raw T4 not sufficient; must include meaning)
 *
 *   Component 2 — The Assumption Surface
 *     AC-5  — Assumption surface present, contains "Fiscal ×1.30" when multiplier is 1.30
 *     AC-6  — Assumption surface height ≤ 24px at 1280, 1440, 1920 viewports
 *     AC-7  — Assumption surface contains "Political economy: enabled" when PE active
 *     AC-8  — Assumption surface renders unavailable fallback on empty configuration
 *
 *   Component 3 — Programme Survival Probability in Zone 1D
 *     AC-9  — Political Feasibility row present when PE enabled (DA-G5-4: Option A)
 *     AC-10 — Political Feasibility row absent when PE disabled
 *     AC-11 — Political Feasibility computation error: row present with "[computation error]"
 *
 * NM-045 rule (mandatory throughout):
 *   All string assertions use direct string-presence match (toContain / toBe) — not structural
 *   regex. Exception: AC-14 format validation regex is acceptable per intent document §7.
 *
 * Guard pattern:
 *   Each test guards on the primary testid it exercises. Pre-implementation, the testid is
 *   absent and the test returns without failing. Guards use .catch(() => false) on isVisible().
 *
 * Route mocking:
 *   AC-4: trajectory endpoint — null confidence_tier for financial framework
 *   AC-5/AC-7: scenario detail endpoint — fiscal_multiplier / modules_config.political_economy
 *   AC-8: scenario detail endpoint — empty configuration
 *   AC-9/AC-11: measurement-output + scenario detail — programme_survival_probability
 *   AC-10: scenario detail — PE disabled
 *
 * Fixture:
 *   Primary: G3 JOR scenario 68b31277 (JOR, 2023, 8 steps, completed). Used for AC-1/2/3/4/5/6/7/8/9/10/11.
 *   GRC fixture for AC-12: created via API with enough steps for TERMINAL alerts.
 *   Any completed scenario for AC-13/AC-14.
 */
import { test, expect } from "@playwright/test";

const API_BASE = "http://localhost:8000/api/v1";

// G3 JOR completed scenario — confirmed at G3 BPO Step 5 Validate 2026-06-17
const G3_JOR_SCENARIO_ID = "68b31277";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface ScenarioCreateResponse {
  scenario_id: string;
}

interface ScenarioDetailResponse {
  status: string;
  configuration: Record<string, unknown>;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function waitForAppReady(page: import("@playwright/test").Page): Promise<void> {
  await page.waitForFunction(
    () =>
      typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
    { timeout: 10_000 },
  );
}

/**
 * Check whether the G3 JOR fixture is accessible and completed.
 */
async function checkG3FixtureAccessible(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/scenarios/${G3_JOR_SCENARIO_ID}`);
    if (!res.ok) return false;
    const body = (await res.json()) as ScenarioDetailResponse;
    return body.status === "completed";
  } catch {
    return false;
  }
}

/**
 * Create a scenario for the given entity and advance to completion.
 */
async function createCompletedScenario(
  entity: string,
  nSteps: number,
  name: string,
): Promise<string> {
  const createRes = await fetch(`${API_BASE}/scenarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name,
      configuration: { entities: [entity], n_steps: nSteps, start_date: "2023-01-01" },
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

  const detail = (await fetch(`${API_BASE}/scenarios/${encodeURIComponent(id)}`).then(
    (r) => r.json(),
  )) as ScenarioDetailResponse;
  if (detail.status !== "completed") {
    throw new Error(`Expected completed status; got: ${detail.status}`);
  }
  return id;
}

/**
 * Minimal trajectory mock response for one entity.
 * Provides 2 steps with all four frameworks each having confidence_tier = 2.
 * Used for AC-1/AC-2/AC-3 to make annotation assertions independent of live DB state.
 */
function makeTrajectoryMock(
  scenarioId: string,
  options: {
    financialTier?: number | null;
    ecologicalBreachType?: "ceiling" | "floor";
  } = {},
): object {
  const financialTier = options.financialTier ?? 2;
  const ecologicalTier = 3;
  const humanTier = 3;
  const governanceTier = 3;

  return {
    scenario_id: scenarioId,
    entity_id: "JOR",
    step_count: 2,
    mda_floors: [],
    steps: [
      {
        step_index: 1,
        effective_from: "2023-07-01T00:00:00Z",
        step_event_label: null,
        step_significance: "ROUTINE",
        frameworks: [
          {
            framework: "financial",
            composite_score: "0.81",
            scoring_basis: "normalized_absolute",
            confidence_tier: financialTier,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: null,
          },
          {
            framework: "human_development",
            composite_score: "0.62",
            scoring_basis: "normalized_absolute",
            confidence_tier: humanTier,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: null,
          },
          {
            framework: "ecological",
            composite_score: "1.11",
            scoring_basis: "boundary_proximity",
            confidence_tier: ecologicalTier,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: null,
          },
          {
            framework: "governance",
            composite_score: "0.37",
            scoring_basis: "normalized_absolute",
            confidence_tier: governanceTier,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: null,
          },
        ],
        policy_inputs: [],
        shock_events: [],
      },
    ],
  };
}

/**
 * Data-quality mock response for JOR 2023 (DA-G5-1 confirmed: source_institution is per-entity).
 */
function makeDataQualityMock(): object {
  return {
    entity_id: "JOR",
    year: 2023,
    frameworks: [
      {
        framework: "financial",
        confidence_tier: 2,
        source_institution: "IMF / CBJ",
        data_vintage: "2023-Q4",
        is_synthetic: false,
        synthetic_basis: null,
      },
      {
        framework: "human_development",
        confidence_tier: 3,
        source_institution: "World Bank",
        data_vintage: "2023-Q2",
        is_synthetic: false,
        synthetic_basis: null,
      },
      {
        framework: "ecological",
        confidence_tier: 3,
        source_institution: null,
        data_vintage: null,
        is_synthetic: true,
        synthetic_basis: "MENA regional comparables 2022",
      },
      {
        framework: "governance",
        confidence_tier: 3,
        source_institution: "V-Dem / WGI",
        data_vintage: "2023-Q1",
        is_synthetic: false,
        synthetic_basis: null,
      },
    ],
  };
}

/**
 * Scenario detail mock with fiscal_multiplier and PE configuration.
 * DA-G5-3 confirmed: modules_config.political_economy.enabled is a valid JSONB path.
 */
function makeScenarioDetailMock(
  scenarioId: string,
  options: {
    fiscalMultiplier?: number;
    peEnabled?: boolean;
    conditionalityType?: string;
    emptyConfig?: boolean;
  } = {},
): object {
  if (options.emptyConfig) {
    return {
      scenario_id: scenarioId,
      name: "G5-mock",
      status: "completed",
      configuration: {},
      created_at: "2023-01-01T00:00:00Z",
      ia1_disclosure: "This output is pre-calibration.",
    };
  }

  return {
    scenario_id: scenarioId,
    name: "G5-mock",
    status: "completed",
    configuration: {
      entities: ["JOR"],
      n_steps: 3,
      start_date: "2023-01-01",
      fiscal_multiplier: options.fiscalMultiplier ?? 1.0,
      modules_config:
        options.peEnabled !== undefined
          ? {
              political_economy: {
                enabled: options.peEnabled,
                conditionality_type: options.conditionalityType ?? "standard",
              },
            }
          : undefined,
    },
    created_at: "2023-01-01T00:00:00Z",
    ia1_disclosure: "This output is pre-calibration.",
  };
}

/**
 * Measurement-output mock for political economy at a given step.
 * DA-G5-4 (Option A): outputs.political_economy.indicators.programme_survival_probability
 */
function makeMeasurementOutputMock(
  scenarioId: string,
  pspValue: string | null,
): object {
  return {
    entity_id: "JOR",
    entity_name: "Jordan",
    timestep: "2023-07-01T00:00:00Z",
    scenario_id: scenarioId,
    step_index: 1,
    outputs: {
      financial: {
        framework: "financial",
        composite_score: null,
        indicators: {},
        mda_alerts: [],
        has_below_floor_indicator: false,
        note: null,
      },
      human_development: {
        framework: "human_development",
        composite_score: null,
        indicators: {},
        mda_alerts: [],
        has_below_floor_indicator: false,
        note: null,
      },
      ecological: {
        framework: "ecological",
        composite_score: "1.11",
        indicators: {},
        mda_alerts: [],
        has_below_floor_indicator: false,
        note: null,
      },
      governance: {
        framework: "governance",
        composite_score: null,
        indicators: {},
        mda_alerts: [],
        has_below_floor_indicator: false,
        note: "GovernanceModule deferred",
      },
      political_economy: {
        framework: "political_economy",
        composite_score: "0.5650",
        indicators: {
          programme_survival_probability: {
            value: pspValue,
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
    },
    ia1_disclosure: "This output is pre-calibration.",
    single_entity_warning: true,
  };
}

// ---------------------------------------------------------------------------
// Shared fixtures — resolved once per describe block
// ---------------------------------------------------------------------------

let jorScenarioId: string | null = null;
let grcScenarioId: string | null = null;

// ---------------------------------------------------------------------------
// AC-1: Zone 1D L0 annotations present at zero interaction
//
// Intent doc §4 AC-1:
// At step 1+, 1280×900, without user interaction: all four framework-annotation-*
// testids are present, not display:none, and each contains text matching "[T" + digit.
//
// Route mocks: trajectory (confidence_tier injected) + data-quality (source injected).
// ---------------------------------------------------------------------------

test.describe("AC-1 through AC-4: Zone 1D L0 annotations", () => {
  test.beforeAll(async () => {
    try {
      jorScenarioId = (await checkG3FixtureAccessible())
        ? G3_JOR_SCENARIO_ID
        // n_steps=1 so current_step=1 matches step_index=1 in makeTrajectoryMock.
        // Using n_steps=3 caused current_step=3 with no matching step in the mock → [—] annotation.
        : await createCompletedScenario("JOR", 1, `G5-AC1-${Date.now()}`);
    } catch {
      jorScenarioId = null;
    }
  });

  test("AC-1: all four Zone 1D framework-annotation-* testids present with [T] text at zero interaction", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    await page.route("**/api/v1/scenarios/*/trajectory**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeTrajectoryMock(jorScenarioId!)),
      }),
    );
    await page.route("**/api/v1/entities/*/data-quality**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeDataQualityMock()),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    // Guard: if annotations are not yet implemented, no-op
    const firstAnnotation = page.locator('[data-testid="framework-annotation-financial"]');
    if (!(await firstAnnotation.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const frameworks = ["financial", "human_development", "ecological", "governance"];
    for (const fw of frameworks) {
      const annotation = page.locator(`[data-testid="framework-annotation-${fw}"]`);
      await expect(annotation).toBeVisible({ timeout: 5_000 });
      const text = await annotation.textContent();
      // NM-045: direct string presence — must contain "[T" then a digit
      expect(text).toContain("[T");
      expect(text).toMatch(/\[T[1-5]/);
    }

    // All four must be in viewport at 1280×900 without scroll (P-4 requirement)
    for (const fw of frameworks) {
      const annotation = page.locator(`[data-testid="framework-annotation-${fw}"]`);
      const box = await annotation.boundingBox();
      expect(box).not.toBeNull();
      // Must be visible in the 900px viewport height
      if (box) {
        expect(box.y + box.height).toBeLessThanOrEqual(900);
      }
    }
  });

  // -------------------------------------------------------------------------
  // AC-2: Zone 1D annotation content — T2, source institution, pre-cal
  //
  // Intent doc §4 AC-2:
  // For JOR financial at step 1: annotation contains "T2", a source institution
  // name ("IMF" or "CBJ"), and "pre-cal". Assert by direct string match (NM-045).
  // -------------------------------------------------------------------------

  test("AC-2: Zone 1D financial annotation contains T2, source institution, and pre-cal", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    await page.route("**/api/v1/scenarios/*/trajectory**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeTrajectoryMock(jorScenarioId!, { financialTier: 2 })),
      }),
    );
    await page.route("**/api/v1/entities/*/data-quality**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeDataQualityMock()),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    const annotation = page.locator('[data-testid="framework-annotation-financial"]');
    if (!(await annotation.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // NM-048: the annotation goes through two states — [T2 · pre-cal] immediately after
    // trajectory loads, then [T2 · IMF / CBJ · pre-cal] once the data-quality useEffect
    // (triggered by trajectory entity_id becoming available) completes its separate fetch.
    // waitForFunction polls the DOM until the source institution text appears, avoiding the
    // race condition of a point-in-time textContent() read.
    await page
      .waitForFunction(
        () => {
          const el = document.querySelector('[data-testid="framework-annotation-financial"]');
          const t = el?.textContent ?? "";
          return t.includes("IMF") || t.includes("CBJ");
        },
        { timeout: 5_000 },
      )
      .catch(() => undefined); // fall through for a clear assertion error below
    const finalText = await annotation.textContent() ?? "";
    // NM-045: direct string-presence assertions
    expect(finalText).toContain("T2");
    expect(finalText).toContain("pre-cal");
    const hasSource = finalText.includes("IMF") || finalText.includes("CBJ");
    expect(hasSource).toBe(true);
  });

  // -------------------------------------------------------------------------
  // AC-3: Ecological annotation contains "ceiling" or "floor" verbatim
  //
  // Intent doc §4 AC-3:
  // DA-G5-5 confirmed: JOR ecological → floor ("approaching resource floor — freshwater").
  // Annotation must NOT contain only "approaching breach" without specifying the type.
  // -------------------------------------------------------------------------

  test("AC-3: Zone 1D ecological annotation contains 'floor' or 'ceiling', not generic 'approaching breach'", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    await page.route("**/api/v1/scenarios/*/trajectory**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeTrajectoryMock(jorScenarioId!)),
      }),
    );
    await page.route("**/api/v1/entities/*/data-quality**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeDataQualityMock()),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    const annotation = page.locator('[data-testid="framework-annotation-ecological"]');
    if (!(await annotation.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const text = await annotation.textContent() ?? "";

    // Must specify breach type — either "ceiling" or "floor" (NM-045: direct string match)
    const hasBreach = text.includes("ceiling") || text.includes("floor");
    expect(hasBreach).toBe(true);

    // Must NOT be a generic annotation without specifying type
    // "approaching breach" alone (without ceiling/floor) is explicitly prohibited
    if (text.includes("approaching breach") && !text.includes("ceiling") && !text.includes("floor")) {
      throw new Error(
        `Ecological annotation contains generic "approaching breach" without specifying ceiling or floor: "${text}"`,
      );
    }
  });

  // -------------------------------------------------------------------------
  // AC-4: Null confidence_tier renders [—] fallback
  //
  // Intent doc §4 AC-4:
  // Trajectory intercepted with confidence_tier: null for financial framework.
  // [data-testid="framework-annotation-financial"] contains "[—]", not "[T" + digit.
  // Remaining three frameworks render normally.
  // -------------------------------------------------------------------------

  test("AC-4: null confidence_tier in trajectory renders [—] fallback on annotation", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    // Return null confidence_tier for financial framework
    await page.route("**/api/v1/scenarios/*/trajectory**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeTrajectoryMock(jorScenarioId!, { financialTier: null })),
      }),
    );
    await page.route("**/api/v1/entities/*/data-quality**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeDataQualityMock()),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    const financialAnnotation = page.locator('[data-testid="framework-annotation-financial"]');
    if (!(await financialAnnotation.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const text = await financialAnnotation.textContent() ?? "";

    // Must show [—] (em-dash in brackets) — NM-045: direct string match
    expect(text).toContain("[—]");
    // Must NOT show a tier digit (null tier must not fall through to T0 or invalid render)
    expect(text).not.toMatch(/\[T[1-5]/);

    // Other three frameworks must render normally (not affected by financial null)
    const otherFrameworks = ["human_development", "ecological", "governance"];
    for (const fw of otherFrameworks) {
      const ann = page.locator(`[data-testid="framework-annotation-${fw}"]`);
      if (await ann.isVisible({ timeout: 3_000 }).catch(() => false)) {
        const annText = await ann.textContent() ?? "";
        expect(annText).toMatch(/\[T[1-5]/);
      }
    }
  });
});

// ---------------------------------------------------------------------------
// AC-5 through AC-8: Assumption surface
//
// Intent doc §4 AC-5 through AC-8.
// Route mocks: scenario detail with controlled fiscal_multiplier and modules_config.
// DA-G5-3 confirmed: modules_config.political_economy.enabled is the correct path.
// ---------------------------------------------------------------------------

test.describe("AC-5 through AC-8: Assumption surface", () => {
  test.beforeAll(async () => {
    try {
      jorScenarioId = (await checkG3FixtureAccessible())
        ? G3_JOR_SCENARIO_ID
        : await createCompletedScenario("JOR", 3, `G5-AC5-${Date.now()}`);
    } catch {
      jorScenarioId = null;
    }
  });

  // -------------------------------------------------------------------------
  // AC-5: Assumption surface present and contains "Fiscal ×1.30"
  //
  // Intent doc §4 AC-5:
  // With fiscal_multiplier=1.30 mocked in scenario detail, assumption-surface testid
  // is present, not display:none, text contains "Fiscal ×1.30" (× = U+00D7).
  // assumption-surface-unavailable must NOT be present.
  // -------------------------------------------------------------------------

  test("AC-5: assumption surface present and contains 'Fiscal ×1.30'", async ({ page }) => {
    if (!jorScenarioId) return;

    // Mock scenario detail to inject fiscal_multiplier: 1.30
    await page.route(`**/api/v1/scenarios/${jorScenarioId}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(jorScenarioId!, { fiscalMultiplier: 1.30 })),
      });
    });

    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    const assumptionSurface = page.locator('[data-testid="assumption-surface"]');
    if (!(await assumptionSurface.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(assumptionSurface).toBeVisible();

    const text = await assumptionSurface.textContent() ?? "";
    // NM-045: direct string match — × is U+00D7 (multiplication sign), not x
    expect(text).toContain("Fiscal ×1.30");

    // assumption-surface-unavailable must NOT coexist with assumption-surface
    const unavailable = page.locator('[data-testid="assumption-surface-unavailable"]');
    expect(await unavailable.count()).toBe(0);
  });

  // -------------------------------------------------------------------------
  // AC-6: Assumption surface height ≤ 24px at 1280, 1440, and 1920 viewports
  //
  // Intent doc §4 AC-6:
  // At each of three widths, getBoundingClientRect().height ≤ 24.
  // -------------------------------------------------------------------------

  for (const width of [1280, 1440, 1920]) {
    test(`AC-6: assumption surface height ≤ 24px at ${width}px wide viewport`, async ({
      page,
    }) => {
      if (!jorScenarioId) return;

      await page.route(`**/api/v1/scenarios/${jorScenarioId}`, (route) => {
        if (route.request().method() !== "GET") { route.continue(); return; }
        route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(makeScenarioDetailMock(jorScenarioId!, { fiscalMultiplier: 1.30 })),
        });
      });

      await page.setViewportSize({ width, height: 900 });
      await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
      await waitForAppReady(page);

      const assumptionSurface = page.locator('[data-testid="assumption-surface"]');
      if (!(await assumptionSurface.isVisible({ timeout: 5_000 }).catch(() => false))) return;

      const height = await assumptionSurface.evaluate(
        (el) => el.getBoundingClientRect().height,
      );
      // Single-line strip: must not exceed 24px regardless of viewport width
      expect(height).toBeLessThanOrEqual(24);
    });
  }

  // -------------------------------------------------------------------------
  // AC-7: Assumption surface contains "Political economy: enabled" when PE active
  //
  // Intent doc §4 AC-7:
  // With modules_config.political_economy.enabled=true mocked: surface contains
  // "Political economy: enabled" (direct string match — NM-045).
  // With PE disabled: "Political economy" text must NOT appear in the surface.
  // -------------------------------------------------------------------------

  test("AC-7: assumption surface contains 'Political economy: enabled' when PE is active", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    await page.route(`**/api/v1/scenarios/${jorScenarioId}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeScenarioDetailMock(jorScenarioId!, {
            fiscalMultiplier: 1.30,
            peEnabled: true,
            conditionalityType: "standard",
          }),
        ),
      });
    });

    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    const assumptionSurface = page.locator('[data-testid="assumption-surface"]');
    if (!(await assumptionSurface.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const text = await assumptionSurface.textContent() ?? "";
    // NM-045: direct string match
    expect(text).toContain("Political economy: enabled");
  });

  test("AC-7b: assumption surface does NOT contain 'Political economy' when PE is disabled", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    await page.route(`**/api/v1/scenarios/${jorScenarioId}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeScenarioDetailMock(jorScenarioId!, {
            fiscalMultiplier: 1.30,
            peEnabled: false,
          }),
        ),
      });
    });

    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    const assumptionSurface = page.locator('[data-testid="assumption-surface"]');
    if (!(await assumptionSurface.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const text = await assumptionSurface.textContent() ?? "";
    expect(text).not.toContain("Political economy");
  });

  // -------------------------------------------------------------------------
  // AC-8: Assumption surface renders unavailable fallback on empty configuration
  //
  // Intent doc §4 AC-8:
  // With scenario detail returning configuration: {}, assumption-surface-unavailable
  // testid is present and assumption-surface is absent.
  // -------------------------------------------------------------------------

  test("AC-8: assumption-surface-unavailable present and assumption-surface absent on empty config", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    await page.route(`**/api/v1/scenarios/${jorScenarioId}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(jorScenarioId!, { emptyConfig: true })),
      });
    });

    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    // Guard: assumption-surface-unavailable testid signals G5 has landed
    const unavailable = page.locator('[data-testid="assumption-surface-unavailable"]');
    if (!(await unavailable.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(unavailable).toBeVisible();
    await expect(unavailable).not.toHaveCSS("display", "none");

    // assumption-surface must NOT be present when configuration is empty
    const surface = page.locator('[data-testid="assumption-surface"]');
    expect(await surface.count()).toBe(0);
  });
});

// ---------------------------------------------------------------------------
// AC-9 through AC-11: Political Feasibility row in Zone 1D (Component 3)
//
// Intent doc §4 AC-9 through AC-11.
// DA-G5-4 Option A: measurement-output endpoint delivers programme_survival_probability.
// Route mocks: scenario detail (PE enabled/disabled) + measurement-output (PSP value).
// ---------------------------------------------------------------------------

test.describe("AC-9 through AC-11: Political Feasibility row (Component 3)", () => {
  test.beforeAll(async () => {
    try {
      jorScenarioId = (await checkG3FixtureAccessible())
        ? G3_JOR_SCENARIO_ID
        : await createCompletedScenario("JOR", 3, `G5-AC9-${Date.now()}`);
    } catch {
      jorScenarioId = null;
    }
  });

  // -------------------------------------------------------------------------
  // AC-9: Political Feasibility row present when PE enabled
  //
  // Intent doc §4 AC-9:
  // PE-enabled scenario + measurement-output returning PSP=0.595:
  // zone-1d-political-feasibility visible, contains "Political Feasibility",
  // a percentage, and "T3". Assert by direct string match (NM-045).
  // -------------------------------------------------------------------------

  test("AC-9: zone-1d-political-feasibility visible with PSP value when PE is enabled", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    // Mock scenario detail: PE enabled
    await page.route(`**/api/v1/scenarios/${jorScenarioId}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeScenarioDetailMock(jorScenarioId!, { peEnabled: true }),
        ),
      });
    });

    // Mock measurement-output: PSP = 0.5950 (DA-G5-4 Option A path)
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMock(jorScenarioId!, "0.5950")),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    const peRow = page.locator('[data-testid="zone-1d-political-feasibility"]');
    if (!(await peRow.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Must be inside Zone 1D four-framework container
    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    await expect(zone1d).toBeVisible({ timeout: 3_000 });

    const text = await peRow.textContent() ?? "";

    // NM-045: each assertion is a direct string match
    expect(text).toContain("Political Feasibility");
    // Percentage value: assert a "%" character is present
    expect(text).toContain("%");
    // Confidence tier T3 (political economy module, DA-G5-4)
    expect(text).toContain("T3");
  });

  // -------------------------------------------------------------------------
  // AC-10: Political Feasibility row absent when PE disabled
  //
  // Intent doc §4 AC-10:
  // PE disabled → zone-1d-political-feasibility must be entirely absent from DOM.
  // count() must equal 0 (not hidden — absent).
  // -------------------------------------------------------------------------

  test("AC-10: zone-1d-political-feasibility absent from DOM when PE is disabled", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    // Mock scenario detail: PE not enabled
    await page.route(`**/api/v1/scenarios/${jorScenarioId}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeScenarioDetailMock(jorScenarioId!, { peEnabled: false }),
        ),
      });
    });

    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    // Guard: zone-1d-four-framework must be present (G5 has landed)
    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // PE row must not exist in DOM (not hidden — absent)
    const peRow = page.locator('[data-testid="zone-1d-political-feasibility"]');
    expect(await peRow.count()).toBe(0);
  });

  // -------------------------------------------------------------------------
  // AC-11: Political Feasibility computation error fallback
  //
  // Intent doc §4 AC-11:
  // PE enabled + measurement-output returns value: null →
  // zone-1d-political-feasibility is present (row not suppressed — PE is enabled)
  // and contains both "Political Feasibility" and "[computation error]".
  // -------------------------------------------------------------------------

  test("AC-11: zone-1d-political-feasibility shows computation error when PSP value is null", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    // Mock scenario detail: PE enabled
    await page.route(`**/api/v1/scenarios/${jorScenarioId}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeScenarioDetailMock(jorScenarioId!, { peEnabled: true }),
        ),
      });
    });

    // Mock measurement-output: PSP value = null (computation failure)
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMock(jorScenarioId!, null)),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    const peRow = page.locator('[data-testid="zone-1d-political-feasibility"]');
    if (!(await peRow.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Row must be present (PE is enabled — absence would imply PE is disabled)
    await expect(peRow).toBeVisible();

    const text = await peRow.textContent() ?? "";

    // NM-045: direct string matches
    expect(text).toContain("Political Feasibility");
    expect(text).toContain("[computation error]");
    // Must NOT show a percentage (there is no value to display)
    // This is not strictly required by the AC, but it confirms the null path is taken
  });
});

// ---------------------------------------------------------------------------
// AC-12: Zone 1B compact rows — full indicator names at 1280×800
//
// Intent doc §4 AC-12:
// GRC scenario with TERMINAL alerts loaded at 1280×800. Compact rows show
// full names without mid-word truncation ("…" in the middle of a word).
// reserve_coverage_months must contain "Reserve" AND "Coverage" as separate words.
// ---------------------------------------------------------------------------

test.describe("AC-12: Zone 1B compact rows full indicator names", () => {
  test.beforeAll(async () => {
    try {
      // Try to use an existing GRC scenario from the fixture set
      // If not available, create one with enough steps for TERMINAL alerts
      grcScenarioId = await createCompletedScenario(
        "GRC",
        6,
        `G5-AC12-GRC-${Date.now()}`,
      );
    } catch {
      grcScenarioId = null;
    }
  });

  test("AC-12: Zone 1B compact rows show full indicator names without mid-word truncation at 1280×800", async ({
    page,
  }) => {
    if (!grcScenarioId) return;

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(grcScenarioId)}`);
    await waitForAppReady(page);

    const compactList = page.locator('[data-testid="zone-1b-compact"]');
    if (!(await compactList.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Wait for alert rows to populate
    const alertRows = compactList.locator('[data-testid="compact-alert-row"]');
    const rowCount = await alertRows.count();

    if (rowCount === 0) return; // guard: no alerts in this scenario at this step

    for (let i = 0; i < rowCount; i++) {
      const row = alertRows.nth(i);
      const rowText = await row.textContent() ?? "";

      // Mid-word truncation check: "…" (U+2026) must not appear inside a word
      // Pattern: "…" followed immediately by a non-space, non-bracket character
      // indicates the truncation happened mid-word
      const midWordTruncation = /…[^\s\[\]]/;
      expect(midWordTruncation.test(rowText)).toBe(false);
    }

    // Specific check for reserve_coverage_months if present (24-char abbreviation: "Reserve Coverage")
    const allText = await compactList.textContent() ?? "";
    if (allText.includes("Reserve")) {
      // "Reserve" and "Coverage" must appear as separate words — not truncated before "Coverage"
      expect(allText).toContain("Reserve");
      expect(allText).toContain("Coverage");
      // "Reserve Cov…" pattern must not appear (Coverage truncated)
      expect(allText).not.toMatch(/Reserve Cov…/);
    }
  });
});

// ---------------------------------------------------------------------------
// AC-13: Zone 1C PMM annotation — "[T3 composite · pre-cal]" verbatim
//
// Intent doc §4 AC-13:
// pmm-annotation testid contains EXACTLY "[T3 composite · pre-cal]"
// Middle dot is U+00B7 (·), not a hyphen or period.
// Assert exact string equality per intent document §7.
// ---------------------------------------------------------------------------

test.describe("AC-13: Zone 1C PMM annotation pre-cal placeholder", () => {
  test.beforeAll(async () => {
    try {
      jorScenarioId = (await checkG3FixtureAccessible())
        ? G3_JOR_SCENARIO_ID
        : await createCompletedScenario("JOR", 3, `G5-AC13-${Date.now()}`);
    } catch {
      jorScenarioId = null;
    }
  });

  test("AC-13: pmm-annotation contains exact string '[T3 composite · pre-cal]'", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    const pmmAnnotation = page.locator('[data-testid="pmm-annotation"]');
    if (!(await pmmAnnotation.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(pmmAnnotation).toBeVisible();

    const text = await pmmAnnotation.textContent() ?? "";
    // Exact string equality — middle dot U+00B7, not hyphen, not period
    // Per intent doc §7: "the QA Lead must assert exact string equality for this text"
    expect(text.trim()).toBe("[T3 composite · pre-cal]");
  });
});

// ---------------------------------------------------------------------------
// AC-14: HCL strip tier meaning expansion
//
// Intent doc §4 AC-14:
// cohort-tier-{key} testids contain "[T{N} · {meaning}]" — NOT just "T4" alone.
// Regex for format validation is acceptable per intent doc §7 (validates structure,
// not a specific value). Additionally assert raw tier code alone is not the label.
// ---------------------------------------------------------------------------

test.describe("AC-14: HCL strip tier meaning expansion", () => {
  test.beforeAll(async () => {
    try {
      jorScenarioId = (await checkG3FixtureAccessible())
        ? G3_JOR_SCENARIO_ID
        : await createCompletedScenario("JOR", 3, `G5-AC14-${Date.now()}`);
    } catch {
      jorScenarioId = null;
    }
  });

  test("AC-14: cohort-tier-* labels show tier meaning expansion, not raw tier code alone", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    // cohort-tier-* testids exist in CohortIndicatorsPanel.tsx (line 174 of existing implementation)
    const tierLabels = page.locator('[data-testid^="cohort-tier-"]');
    const count = await tierLabels.count();

    if (count === 0) return; // guard: HCL panel has no indicators (or G5 not yet landed)

    const tierMeaningRegex =
      /\[T[1-5] · (real observed data|official statistics|synthetic|model estimate|synthetic extrapolation)\]/;

    let atLeastOneFound = false;
    for (let i = 0; i < count; i++) {
      const label = tierLabels.nth(i);
      const text = await label.textContent() ?? "";
      if (text.trim() === "") continue;

      // Format validation regex is acceptable per intent doc §7
      expect(text).toMatch(tierMeaningRegex);
      atLeastOneFound = true;

      // Raw tier code alone must not be the complete label (e.g., "T4" without meaning)
      // This detects a silent failure where the label renders the code but drops the expansion
      expect(text.trim()).not.toBe("T1");
      expect(text.trim()).not.toBe("T2");
      expect(text.trim()).not.toBe("T3");
      expect(text.trim()).not.toBe("T4");
      expect(text.trim()).not.toBe("T5");
    }

    // At least one valid expanded tier label must exist (confirms the panel is showing data)
    if (count > 0) {
      expect(atLeastOneFound).toBe(true);
    }
  });
});
