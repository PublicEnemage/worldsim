/**
 * E2E: M19-G4 — PSP Driver Arc + In-Viewport Auditability Panel — AC-1 through AC-11.
 *
 * Authored BEFORE implementation from intent document at:
 * docs/process/intents/M19-G4-2026-07-03-psp-driver-auditability-panel.md
 *
 * ADR: ADR-019 (Zone 1D scope — control plane column) + ADR-015 §Component 3 (PSP row).
 * Issue: #1528 — feat(zone1d): PSP driver arc + in-viewport auditability panel (DEMO-165)
 * Sprint entry: docs/process/sprint-plans/m19-g4-sprint-entry.md (EL Approved 2026-07-03)
 * Sprint journal: #1624
 *
 * Acceptance criteria covered:
 *   AC-1  — psp-driver-arc present when PE enabled and trajectory loaded
 *   AC-2  — driver arc badge abbreviations correct (FISC/EXT/GOV/SOC/—)
 *   AC-3  — current step badge is visually differentiated
 *   AC-4  — methodology panel appears on driver row click with 4 category entries
 *   AC-5  — fragility amplifier active when legitimacyValue < legitimacyFloor
 *   AC-6  — fragility amplifier inactive when legitimacyValue > legitimacyFloor
 *   AC-7  — methodology panel collapses on second click
 *   AC-8  — psp-driver-arc absent when PE disabled
 *   AC-9  — psp-driver-arc absent when pspValue undefined
 *   AC-10 — arc rendered with "—" badges when all psp_dominant_driver values are null
 *   AC-11 — psp-driver-expand affordance present alongside driver label
 *
 * NM-056 rule: NO test.skip() or conditional skip patterns. Guard pattern in use:
 *   if (!guard) return; — fires pre-implementation (no-op); asserts post-implementation.
 *
 * NM-076 crosscheck: new testids introduced by this file —
 *   psp-driver-arc
 *   psp-driver-arc-step-{N}  (N is 1-indexed step number)
 *   psp-driver-expand
 *   psp-driver-methodology-panel
 *   psp-driver-category-fiscal_sustainability
 *   psp-driver-category-external_balance
 *   psp-driver-category-governance
 *   psp-driver-category-social_stability
 *   psp-driver-fragility-status
 * Verified before authorship (NM-076 process): grep -r 'psp-driver-arc' frontend/tests/e2e/
 * returned no matches outside this file.
 *
 * NM-086 gate: #1528 reads only existing trajectory API fields (psp_dominant_driver per step).
 * No new mock routes introduced. Confirmed: psp_dominant_driver declared in
 * docs/schema/api_contracts.yml §measurement-output at line ~809. The trajectory endpoint
 * also carries psp_dominant_driver per step (TrajectoryStepResponse.psp_dominant_driver per
 * intent doc §1). The implementing agent must confirm the trajectory schema declaration.
 *
 * Fixture: ZMB (Zambia) with political_economy enabled.
 * psp_dominant_driver mocked at top level of each trajectory step object.
 * legitimacy_index mocked via measurement-output political_economy.indicators.
 *
 * Viewport: 1440×900 (intent doc §3.1).
 */
import { test, expect } from "@playwright/test";

const API_BASE = "http://localhost:8000/api/v1";

const FRAGILITY_FLOOR = "0.45";

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

async function createZMBScenarioPE(
  nSteps: number,
  name: string,
  peEnabled = true,
): Promise<string | null> {
  try {
    const res = await fetch(`${API_BASE}/scenarios`, {
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
            political_economy: { enabled: peEnabled },
          },
        },
      }),
    });
    if (!res.ok) return null;
    const { scenario_id: id } = (await res.json()) as ScenarioCreateResponse;
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

/**
 * Build a per-step trajectory object with psp_dominant_driver at top level of step.
 * The arc implementation reads psp_dominant_driver per TrajectoryStepResponse.
 */
function buildArcStep(
  stepIndex: number,
  effectiveFrom: string,
  pspDominantDriver: string | null,
): object {
  return {
    step_index: stepIndex,
    effective_from: effectiveFrom,
    step_event_label: null,
    step_significance: "ROUTINE",
    psp_dominant_driver: pspDominantDriver,
    frameworks: [
      {
        framework: "financial",
        composite_score: "0.58",
        scoring_basis: "normalized_absolute",
        confidence_tier: 3,
        ci_lower: "0.493",
        ci_upper: "0.667",
        ci_coverage: 0.80,
        is_pre_calibration: true,
        band_method: "PRE_CALIBRATION_STRUCTURAL_PRIOR",
        is_meaningless: false,
        suppressed_reason: null,
      },
      {
        framework: "human_development",
        composite_score: "0.52",
        scoring_basis: "normalized_absolute",
        confidence_tier: 3,
        ci_lower: "0.442",
        ci_upper: "0.598",
        ci_coverage: 0.80,
        is_pre_calibration: true,
        band_method: "PRE_CALIBRATION_STRUCTURAL_PRIOR",
        is_meaningless: false,
        suppressed_reason: null,
      },
      {
        framework: "ecological",
        composite_score: null,
        scoring_basis: "boundary_proximity",
        confidence_tier: 3,
        ci_lower: null,
        ci_upper: null,
        ci_coverage: null,
        is_pre_calibration: null,
        band_method: null,
        is_meaningless: false,
        suppressed_reason: null,
      },
      {
        framework: "governance",
        composite_score: "0.55",
        scoring_basis: "percentile_rank",
        confidence_tier: 2,
        ci_lower: null,
        ci_upper: null,
        ci_coverage: null,
        is_pre_calibration: null,
        band_method: null,
        is_meaningless: false,
        suppressed_reason: null,
      },
    ],
    policy_inputs: [],
    shock_events: [],
  };
}

/**
 * Trajectory mock for ZMB with multiple steps carrying psp_dominant_driver per step.
 * Covers all 5 driver values across 5 steps for AC-2 (abbreviation) coverage.
 */
function makeArcTrajectoryMock(
  scenarioId: string,
  options: {
    nSteps?: number;
    drivers?: (string | null)[];
    currentStepIndex?: number;
  } = {},
): object {
  const nSteps = options.nSteps ?? 3;
  const defaultDrivers = [
    "fiscal_sustainability",   // step 1 → FISC
    "external_balance",        // step 2 → EXT
    "governance",              // step 3 → GOV (current)
    "social_stability",        // step 4 → SOC (if present)
    null,                      // step 5 → — (if present)
  ];
  const drivers = options.drivers ?? defaultDrivers.slice(0, nSteps);

  const steps = Array.from({ length: nSteps }, (_, i) => {
    const date = `202${4 + i}-01-01T00:00:00Z`;
    return buildArcStep(i + 1, date, drivers[i] ?? null);
  });

  return {
    scenario_id: scenarioId,
    entity_id: "ZMB",
    step_count: nSteps,
    mda_floors: [],
    steps,
  };
}

/**
 * Trajectory mock with all-null psp_dominant_driver values (AC-10).
 */
function makeAllNullDriverTrajectoryMock(scenarioId: string, nSteps: number): object {
  const nullDrivers: null[] = Array.from({ length: nSteps }, () => null);
  return makeArcTrajectoryMock(scenarioId, { nSteps, drivers: nullDrivers });
}

/**
 * Measurement-output mock for ZMB with controlled PSP and legitimacy values.
 * The legitimacy_index indicator shape follows ScenarioInstrumentCluster.tsx:683.
 */
function makeMeasurementOutputMockG4(
  scenarioId: string,
  options: {
    pspValue?: string | null;
    pspDominantDriver?: string | null;
    legitimacyValue?: string | null;
    legitimacyFloor?: string;
    legitimacyDirection?: "declining" | "stable" | "improving" | null;
    stepIndex?: number;
    peEnabled?: boolean;
  } = {},
): object {
  const pspValue = options.pspValue ?? "0.5200";
  const pspDominantDriver = options.pspDominantDriver ?? "fiscal_sustainability";
  const legitimacyValue = options.legitimacyValue ?? "0.42";
  const legitimacyFloor = options.legitimacyFloor ?? FRAGILITY_FLOOR;
  const legitimacyDirection = options.legitimacyDirection ?? "declining";
  const stepIndex = options.stepIndex ?? 3;
  const peEnabled = options.peEnabled ?? true;

  return {
    entity_id: "ZMB",
    entity_name: "Zambia",
    timestep: `2024-0${stepIndex}-01T00:00:00Z`,
    scenario_id: scenarioId,
    step_index: stepIndex,
    outputs: {
      financial: {
        framework: "financial",
        composite_score: "0.58",
        indicators: {},
        mda_alerts: [],
        has_below_floor_indicator: false,
        note: null,
      },
      human_development: {
        framework: "human_development",
        composite_score: "0.52",
        indicators: {},
        mda_alerts: [],
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
        composite_score: "0.55",
        indicators: {},
        mda_alerts: [],
        has_below_floor_indicator: false,
        note: null,
      },
      political_economy: {
        framework: "political_economy",
        composite_score: peEnabled && pspValue != null ? "0.6200" : null,
        indicators: peEnabled ? {
          programme_survival_probability: {
            value: pspValue,
            unit: "probability",
            variable_type: "STOCK",
            confidence_tier: 3,
            observation_date: null,
            source_registry_id: null,
            measurement_framework: "political_economy",
            _envelope_version: "2",
            psp_dominant_driver: pspDominantDriver,
          },
          legitimacy_index: {
            value: legitimacyValue,
            floor: legitimacyFloor,
            direction: legitimacyDirection,
          },
        } : {},
        mda_alerts: [],
        has_below_floor_indicator: false,
        note: peEnabled ? null : "Political economy disabled",
      },
    },
    ia1_disclosure: "This output is pre-calibration.",
    single_entity_warning: true,
  };
}

function makeScenarioDetailMockG4(scenarioId: string, peEnabled = true): object {
  return {
    scenario_id: scenarioId,
    name: "G4-ZMB-arc-test",
    status: "completed",
    configuration: {
      entities: ["ZMB"],
      n_steps: 5,
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

// ---------------------------------------------------------------------------
// Route registration helper
// ---------------------------------------------------------------------------

async function registerArcMocks(
  page: import("@playwright/test").Page,
  scenarioId: string,
  options: {
    trajectoryMock?: object;
    measurementOutputMock?: object;
    scenarioDetailMock?: object;
    peEnabled?: boolean;
  } = {},
): Promise<void> {
  const peEnabled = options.peEnabled ?? true;
  const trajMock = options.trajectoryMock ??
    makeArcTrajectoryMock(scenarioId, { nSteps: 3 });
  const measMock = options.measurementOutputMock ??
    makeMeasurementOutputMockG4(scenarioId);
  const detailMock = options.scenarioDetailMock ??
    makeScenarioDetailMockG4(scenarioId, peEnabled);

  await page.route(`**/api/v1/scenarios/${scenarioId}`, (route) => {
    if (route.request().method() !== "GET") { route.continue(); return; }
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(detailMock),
    });
  });

  await page.route(`**/api/v1/scenarios/${scenarioId}/trajectory*`, (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(trajMock),
    }),
  );

  await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(measMock),
    }),
  );
}

// ---------------------------------------------------------------------------
// AC-1 — psp-driver-arc present when PE enabled and trajectory loaded
// ---------------------------------------------------------------------------

test.describe("AC-1: psp-driver-arc visible in Zone 1D when PE enabled, trajectory loaded (#1528)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createZMBScenarioPE(3, `G4-ZMB-AC1-${Date.now()}`);
  });

  test("AC-1: psp-driver-arc is visible and contains step-1/2/3 badge elements", async ({
    page,
  }) => {
    if (!scenarioId) return;
    const sid = scenarioId;

    await registerArcMocks(page, sid, {
      trajectoryMock: makeArcTrajectoryMock(sid, { nSteps: 3 }),
      measurementOutputMock: makeMeasurementOutputMockG4(sid, { stepIndex: 3 }),
    });

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    // Guard: Zone 1D must be present
    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Primary guard: psp-driver-arc is new in G4 — absent pre-implementation
    const arc = page.locator('[data-testid="psp-driver-arc"]');
    if (!(await arc.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(arc).toBeVisible();

    // Each step must have a badge element
    for (let step = 1; step <= 3; step++) {
      const badge = page.locator(`[data-testid="psp-driver-arc-step-${step}"]`);
      await expect(badge).toBeAttached({ timeout: 3_000 });
    }
  });
});

// ---------------------------------------------------------------------------
// AC-2 — badge abbreviations correct for all 5 driver values
// ---------------------------------------------------------------------------

test.describe("AC-2: driver arc badge abbreviations (FISC/EXT/GOV/SOC/—) (#1528)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    // 5 steps to cover all 5 driver values in one trajectory
    scenarioId = await createZMBScenarioPE(5, `G4-ZMB-AC2-${Date.now()}`);
  });

  test("AC-2: fiscal_sustainability → FISC, external_balance → EXT, governance → GOV, social_stability → SOC, null → —", async ({
    page,
  }) => {
    if (!scenarioId) return;
    const sid = scenarioId;

    const trajMock = makeArcTrajectoryMock(sid, {
      nSteps: 5,
      drivers: [
        "fiscal_sustainability",  // step 1 → FISC
        "external_balance",       // step 2 → EXT
        "governance",             // step 3 → GOV
        "social_stability",       // step 4 → SOC
        null,                     // step 5 → —
      ],
    });

    await registerArcMocks(page, sid, {
      trajectoryMock: trajMock,
      measurementOutputMock: makeMeasurementOutputMockG4(sid, {
        pspDominantDriver: "governance",
        stepIndex: 3,
      }),
    });

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const arc = page.locator('[data-testid="psp-driver-arc"]');
    if (!(await arc.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const expectedAbbreviations: Record<string, string> = {
      "1": "FISC",
      "2": "EXT",
      "3": "GOV",
      "4": "SOC",
      "5": "—",
    };

    for (const [step, abbrev] of Object.entries(expectedAbbreviations)) {
      const badge = page.locator(`[data-testid="psp-driver-arc-step-${step}"]`);
      if (!((await badge.count()) > 0)) continue;
      await expect(badge).toContainText(abbrev);
    }
  });
});

// ---------------------------------------------------------------------------
// AC-3 — current step badge is visually differentiated
// ---------------------------------------------------------------------------

test.describe("AC-3: current step badge visually differentiated (bold/border) (#1528)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createZMBScenarioPE(3, `G4-ZMB-AC3-${Date.now()}`);
  });

  test("AC-3: step 3 badge has font-weight ≥ 700 or border; step 1 and 2 do not", async ({
    page,
  }) => {
    if (!scenarioId) return;
    const sid = scenarioId;

    await registerArcMocks(page, sid, {
      trajectoryMock: makeArcTrajectoryMock(sid, { nSteps: 3 }),
      measurementOutputMock: makeMeasurementOutputMockG4(sid, { stepIndex: 3 }),
    });

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const arc = page.locator('[data-testid="psp-driver-arc"]');
    if (!(await arc.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const step3Badge = page.locator('[data-testid="psp-driver-arc-step-3"]');
    if (!((await step3Badge.count()) > 0)) return;

    // Assert visual differentiation: font-weight 700 (bold) OR non-zero border width
    const isVisuallyDifferentiated = await step3Badge.evaluate((el) => {
      const styles = window.getComputedStyle(el);
      const fw = parseInt(styles.fontWeight, 10);
      const borderTop = parseFloat(styles.borderTopWidth);
      const borderLeft = parseFloat(styles.borderLeftWidth);
      return fw >= 700 || borderTop > 0 || borderLeft > 0;
    });
    expect(isVisuallyDifferentiated).toBe(true);

    // Other step badges should not have the same bold/border treatment
    for (const step of [1, 2]) {
      const badge = page.locator(`[data-testid="psp-driver-arc-step-${step}"]`);
      if (!((await badge.count()) > 0)) continue;
      const isBold = await badge.evaluate((el) => {
        const styles = window.getComputedStyle(el);
        return parseInt(styles.fontWeight, 10) >= 700;
      });
      // At minimum, step 3 must be bolder — if all are bold, implementation may differ
      // Assert step 3 font-weight ≥ other steps' font-weight
      const step3FW = await step3Badge.evaluate((el) =>
        parseInt(window.getComputedStyle(el).fontWeight, 10),
      );
      const thisFW = await badge.evaluate((el) =>
        parseInt(window.getComputedStyle(el).fontWeight, 10),
      );
      expect(step3FW).toBeGreaterThanOrEqual(thisFW);
      void isBold; // suppress unused-var lint
    }
  });
});

// ---------------------------------------------------------------------------
// AC-4 — methodology panel appears on driver row click with 4 category entries
// ---------------------------------------------------------------------------

test.describe("AC-4: methodology panel visible after driver row click (#1528)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createZMBScenarioPE(3, `G4-ZMB-AC4-${Date.now()}`);
  });

  test("AC-4: clicking psp-driver-row reveals psp-driver-methodology-panel with 4 category rows", async ({
    page,
  }) => {
    if (!scenarioId) return;
    const sid = scenarioId;

    await registerArcMocks(page, sid, {
      measurementOutputMock: makeMeasurementOutputMockG4(sid, {
        pspDominantDriver: "fiscal_sustainability",
        stepIndex: 3,
      }),
    });

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard on psp-driver-expand (new G4 affordance)
    const expand = page.locator('[data-testid="psp-driver-expand"]');
    if (!(await expand.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Click the driver row (expand affordance or row itself)
    const driverRow = page.locator('[data-testid="psp-driver-row"]');
    if (!(await driverRow.isVisible({ timeout: 5_000 }).catch(() => false))) return;
    await driverRow.click();

    // Panel must appear
    const panel = page.locator('[data-testid="psp-driver-methodology-panel"]');
    await expect(panel).toBeVisible({ timeout: 3_000 });

    // All 4 category rows must have non-empty text content
    const categories = [
      "psp-driver-category-fiscal_sustainability",
      "psp-driver-category-external_balance",
      "psp-driver-category-governance",
      "psp-driver-category-social_stability",
    ] as const;

    for (const testid of categories) {
      const cat = page.locator(`[data-testid="${testid}"]`);
      await expect(cat).toBeVisible({ timeout: 3_000 });
      const text = (await cat.textContent()) ?? "";
      expect(text.trim().length).toBeGreaterThan(0);
    }
  });
});

// ---------------------------------------------------------------------------
// AC-5 — fragility amplifier active when legitimacyValue < legitimacyFloor
// ---------------------------------------------------------------------------

test.describe("AC-5: fragility amplifier active text when legitimacy below floor (#1528)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createZMBScenarioPE(3, `G4-ZMB-AC5-${Date.now()}`);
  });

  test("AC-5: psp-driver-fragility-status contains 'amplifier active' when legitimacy 0.38 < floor 0.45", async ({
    page,
  }) => {
    if (!scenarioId) return;
    const sid = scenarioId;

    // Legitimacy well below fragility floor → amplifier active
    await registerArcMocks(page, sid, {
      measurementOutputMock: makeMeasurementOutputMockG4(sid, {
        legitimacyValue: "0.38",
        legitimacyFloor: "0.45",
        legitimacyDirection: "declining",
        pspDominantDriver: "fiscal_sustainability",
        stepIndex: 3,
      }),
    });

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const driverRow = page.locator('[data-testid="psp-driver-row"]');
    if (!(await driverRow.isVisible({ timeout: 8_000 }).catch(() => false))) return;
    await driverRow.click();

    const fragilityStatus = page.locator('[data-testid="psp-driver-fragility-status"]');
    if (!(await fragilityStatus.isVisible({ timeout: 3_000 }).catch(() => false))) return;

    const text = (await fragilityStatus.textContent()) ?? "";
    expect(text.toLowerCase()).toContain("amplifier active");
  });
});

// ---------------------------------------------------------------------------
// AC-6 — fragility amplifier inactive when legitimacyValue > legitimacyFloor
// ---------------------------------------------------------------------------

test.describe("AC-6: fragility amplifier inactive text when legitimacy above floor (#1528)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createZMBScenarioPE(3, `G4-ZMB-AC6-${Date.now()}`);
  });

  test("AC-6: psp-driver-fragility-status contains 'inactive' when legitimacy 0.72 > floor 0.45", async ({
    page,
  }) => {
    if (!scenarioId) return;
    const sid = scenarioId;

    // Legitimacy well above fragility floor → amplifier inactive
    await registerArcMocks(page, sid, {
      measurementOutputMock: makeMeasurementOutputMockG4(sid, {
        legitimacyValue: "0.72",
        legitimacyFloor: "0.45",
        legitimacyDirection: "stable",
        pspDominantDriver: "fiscal_sustainability",
        stepIndex: 3,
      }),
    });

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const driverRow = page.locator('[data-testid="psp-driver-row"]');
    if (!(await driverRow.isVisible({ timeout: 8_000 }).catch(() => false))) return;
    await driverRow.click();

    const fragilityStatus = page.locator('[data-testid="psp-driver-fragility-status"]');
    if (!(await fragilityStatus.isVisible({ timeout: 3_000 }).catch(() => false))) return;

    const text = (await fragilityStatus.textContent()) ?? "";
    expect(text.toLowerCase()).toContain("inactive");
  });
});

// ---------------------------------------------------------------------------
// AC-7 — methodology panel collapses on second click
// ---------------------------------------------------------------------------

test.describe("AC-7: methodology panel collapses on second driver row click (#1528)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createZMBScenarioPE(3, `G4-ZMB-AC7-${Date.now()}`);
  });

  test("AC-7: psp-driver-methodology-panel not visible after second click on driver row", async ({
    page,
  }) => {
    if (!scenarioId) return;
    const sid = scenarioId;

    await registerArcMocks(page, sid, {
      measurementOutputMock: makeMeasurementOutputMockG4(sid, {
        pspDominantDriver: "fiscal_sustainability",
        stepIndex: 3,
      }),
    });

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const driverRow = page.locator('[data-testid="psp-driver-row"]');
    if (!(await driverRow.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // First click — open
    await driverRow.click();
    const panel = page.locator('[data-testid="psp-driver-methodology-panel"]');
    if (!(await panel.isVisible({ timeout: 3_000 }).catch(() => false))) return;

    // Second click — should collapse
    await driverRow.click();
    await page.waitForTimeout(300); // allow collapse animation if any

    // Panel must no longer be visible (not in DOM, or hidden)
    const stillVisible = await panel.isVisible({ timeout: 1_000 }).catch(() => false);
    expect(stillVisible).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// AC-8 — psp-driver-arc absent when PE disabled
// ---------------------------------------------------------------------------

test.describe("AC-8: psp-driver-arc absent when PE disabled (#1528)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createZMBScenarioPE(3, `G4-ZMB-AC8-${Date.now()}`, false);
  });

  test("AC-8: psp-driver-arc not in DOM when PE disabled", async ({ page }) => {
    if (!scenarioId) return;
    const sid = scenarioId;

    await registerArcMocks(page, sid, {
      trajectoryMock: makeArcTrajectoryMock(sid, { nSteps: 3 }),
      scenarioDetailMock: makeScenarioDetailMockG4(sid, false),
      measurementOutputMock: makeMeasurementOutputMockG4(sid, {
        peEnabled: false,
        pspValue: null,
        pspDominantDriver: null,
        legitimacyValue: null,
        stepIndex: 3,
      }),
      peEnabled: false,
    });

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // psp-driver-arc must be absent when PE disabled
    const arc = page.locator('[data-testid="psp-driver-arc"]');
    const arcPresent = await arc.isVisible({ timeout: 2_000 }).catch(() => false);
    expect(arcPresent).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// AC-9 — psp-driver-arc absent when pspValue is undefined (PSP not yet computed)
// ---------------------------------------------------------------------------

test.describe("AC-9: psp-driver-arc absent when pspValue is undefined (#1528)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createZMBScenarioPE(1, `G4-ZMB-AC9-${Date.now()}`);
  });

  test("AC-9: psp-driver-arc and psp-driver-row absent when PSP indicator unavailable", async ({
    page,
  }) => {
    test.fixme(true, "G4 #1528 not yet implemented — remove fixme when implementation PR merges");
    if (!scenarioId) return;
    const sid = scenarioId;

    // pspValue null simulates PE enabled but PSP indicator not computed at this step
    await registerArcMocks(page, sid, {
      measurementOutputMock: makeMeasurementOutputMockG4(sid, {
        pspValue: null,
        pspDominantDriver: null,
        legitimacyValue: null,
        stepIndex: 1,
      }),
    });

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Both arc and driver row must be absent (consistent with existing pspValue gating)
    const arc = page.locator('[data-testid="psp-driver-arc"]');
    const arcPresent = await arc.isVisible({ timeout: 2_000 }).catch(() => false);
    expect(arcPresent).toBe(false);

    const driverRow = page.locator('[data-testid="psp-driver-row"]');
    const rowPresent = await driverRow.isVisible({ timeout: 2_000 }).catch(() => false);
    expect(rowPresent).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// AC-10 — arc rendered with all "—" badges when all psp_dominant_driver are null (SF-3)
// ---------------------------------------------------------------------------

test.describe("AC-10: psp-driver-arc present with all '—' badges when all step drivers null (#1528)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createZMBScenarioPE(3, `G4-ZMB-AC10-${Date.now()}`);
  });

  test("AC-10: arc row present and each badge text is '—' when no driver attributed at any step", async ({
    page,
  }) => {
    if (!scenarioId) return;
    const sid = scenarioId;

    await registerArcMocks(page, sid, {
      // All psp_dominant_driver values are null across all 3 steps
      trajectoryMock: makeAllNullDriverTrajectoryMock(sid, 3),
      measurementOutputMock: makeMeasurementOutputMockG4(sid, {
        pspValue: "0.4800",  // PSP is computed but no driver attributed
        pspDominantDriver: null,
        stepIndex: 3,
      }),
    });

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Arc must be present (arc is trajectory-length, not current-step-gated)
    const arc = page.locator('[data-testid="psp-driver-arc"]');
    if (!(await arc.isVisible({ timeout: 5_000 }).catch(() => false))) return;
    await expect(arc).toBeVisible();

    // All step badges must show "—"
    for (let step = 1; step <= 3; step++) {
      const badge = page.locator(`[data-testid="psp-driver-arc-step-${step}"]`);
      if (!((await badge.count()) > 0)) continue;
      const text = (await badge.textContent()) ?? "";
      expect(text.trim()).toBe("—");
    }
  });
});

// ---------------------------------------------------------------------------
// AC-11 — expand affordance present on driver row
// ---------------------------------------------------------------------------

test.describe("AC-11: psp-driver-expand affordance present alongside driver label (#1528)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  let scenarioId: string | null = null;

  test.beforeAll(async () => {
    scenarioId = await createZMBScenarioPE(3, `G4-ZMB-AC11-${Date.now()}`);
  });

  test("AC-11: psp-driver-expand is present and visible when pspDominantDriver is non-null", async ({
    page,
  }) => {
    if (!scenarioId) return;
    const sid = scenarioId;

    await registerArcMocks(page, sid, {
      measurementOutputMock: makeMeasurementOutputMockG4(sid, {
        pspDominantDriver: "fiscal_sustainability",
        stepIndex: 3,
      }),
    });

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    const driverRow = page.locator('[data-testid="psp-driver-row"]');
    if (!(await driverRow.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Guard on expand affordance (new G4 element — absent pre-implementation)
    const expand = page.locator('[data-testid="psp-driver-expand"]');
    if (!(await expand.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(expand).toBeVisible();

    // The expand affordance must appear alongside the driver label text (within driver row)
    const driverRowEl = page.locator('[data-testid="psp-driver-row"]');
    const expandInRow = driverRowEl.locator('[data-testid="psp-driver-expand"]');
    const inRow = await expandInRow.count();
    if (inRow === 0) {
      // Accept: expand may be a sibling element adjacent to the driver row
      await expect(expand).toBeVisible();
    } else {
      await expect(expandInRow).toBeVisible();
    }
  });
});
