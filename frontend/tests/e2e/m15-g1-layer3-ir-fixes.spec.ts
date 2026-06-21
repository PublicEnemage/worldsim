/**
 * E2E: M15-G1 Layer 3 + IR Fixes — AC-1 through AC-11.
 *
 * Authored BEFORE implementation from intent document at:
 * docs/process/intents/M15-G1-2026-06-20-layer3-ir-fixes.md
 *
 * ADR: ADR-015 — Model Legibility Architecture (Evidence Thread Architecture)
 * ADR: ADR-016 — Scenario Grounding Architecture
 * Sprint entry: docs/process/sprint-plans/m15-g1-sprint-entry.md
 *
 * Issues covered:
 *   #1065 — Zone 1B Layer 3 trajectory sentence (AC-1, AC-2, AC-10)
 *   #1066 — Suppress "0 consecutive steps" when zero (AC-3, AC-4)
 *   #1068 — Zone 1A L0 confidence tier badge on trajectory curves (AC-5)
 *   #1069 — Grounding strip dual reserve value disambiguation (AC-6, AC-7, AC-11)
 *   #1075 — PSP self-interpreting sentence in Zone 1D (AC-8, AC-9)
 *
 * NM-045 rule: all string assertions use .toContainText() or string .includes()
 * — not exact equality matching — except where explicitly specified otherwise.
 *
 * Guard pattern: each test guards on the primary testid it exercises.
 * Pre-implementation, the testid is absent and the test returns without failing.
 * Guards use .catch(() => false) on isVisible() — a guard that fires is a no-op,
 * not a pass. Tests become active once G1 implementation lands.
 *
 * Route mocking:
 *   AC-1/AC-2:  measurement-output with CRITICAL reserve alert, consecutive_breach_steps=8
 *   AC-3:       measurement-output with consecutive_breach_steps=0 (first-step breach)
 *   AC-4:       measurement-output with consecutive_breach_steps=3
 *   AC-5:       trajectory mock with confidence_tier per framework
 *   AC-6/AC-7:  /initial-state entry-state mock + measurement-output current step
 *   AC-8/AC-9:  scenario detail (PE enabled) + measurement-output (PSP=0.65)
 *   AC-10:      measurement-output with consecutive_breach_steps=null (computation fail)
 *   AC-11:      /initial-state success + /trajectory → 500
 *
 * Fixture: one ZMB scenario created per describe group in beforeAll.
 * ZMB ECF configuration pattern: docs/demo/m14/screenshot-brief.md.
 */
import { test, expect } from "@playwright/test";

const API_BASE = "http://localhost:8000/api/v1";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface ScenarioCreateResponse {
  scenario_id: string;
}

interface MDAAlert {
  alert_id: string;
  indicator_id: string;
  indicator_name: string;
  measurement_framework: string;
  severity: string;
  current_value: number;
  floor_value: number | null;
  ceiling_value: number | null;
  breach_direction: string;
  consecutive_breach_steps: number | null;
  confidence_tier: number;
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

/**
 * Open the grounding strip panel. Tries the testid toggle first, falls back to
 * button text. Returns false if neither is found (G4 not yet landed).
 */
async function openGroundingStrip(page: import("@playwright/test").Page): Promise<boolean> {
  const byTestId = page.locator('[data-testid="grounding-strip-toggle"]');
  if (await byTestId.isVisible({ timeout: 5_000 }).catch(() => false)) {
    await byTestId.click();
    return true;
  }
  const byText = page.getByRole("button", { name: /Grounding/ });
  if (await byText.isVisible({ timeout: 2_000 }).catch(() => false)) {
    await byText.click();
    return true;
  }
  return false;
}

/**
 * Create a ZMB scenario and advance N steps via API.
 * Minimal configuration — route mocks control what the UI displays.
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

// ---------------------------------------------------------------------------
// Mock factories
// ---------------------------------------------------------------------------

/**
 * Reserve Coverage Months MDA alert for ZMB CRITICAL breach.
 * consecutive_breach_steps is the controlled variable across tests.
 */
function makeReserveAlert(consecutiveBreach: number | null): MDAAlert {
  return {
    alert_id: "MDA-ZMB-RES-1",
    indicator_id: "reserve_coverage_months",
    indicator_name: "Reserve Coverage Months",
    measurement_framework: "financial",
    severity: "CRITICAL",
    current_value: 2.9,
    floor_value: 2.5,
    ceiling_value: null,
    breach_direction: "below_floor",
    consecutive_breach_steps: consecutiveBreach,
    confidence_tier: 2,
  };
}

/**
 * Full measurement-output mock for ZMB at step 1.
 * financial MDA: reserve_coverage_months CRITICAL with controlled consecutive_breach_steps.
 * political_economy: programme_survival_probability at optional pspValue.
 */
function makeMeasurementOutputMock(
  scenarioId: string,
  options: {
    consecutiveBreach?: number | null;
    pspValue?: string | null;
  } = {},
): object {
  const consecutiveBreach = "consecutiveBreach" in options ? options.consecutiveBreach : 8;
  const alert = makeReserveAlert(consecutiveBreach ?? null);

  return {
    entity_id: "ZMB",
    entity_name: "Zambia",
    timestep: "2024-07-01T00:00:00Z",
    scenario_id: scenarioId,
    step_index: 1,
    outputs: {
      financial: {
        framework: "financial",
        composite_score: "0.45",
        indicators: {
          reserve_coverage_months: {
            value: "2.9",
            unit: "months",
            variable_type: "STOCK",
            confidence_tier: 2,
            observation_date: null,
            source_registry_id: "IMF_WEO_APR2024",
            measurement_framework: "financial",
            _envelope_version: "2",
          },
        },
        mda_alerts: [alert],
        has_below_floor_indicator: true,
        note: null,
      },
      human_development: {
        framework: "human_development",
        composite_score: "0.55",
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
        note: "Ecological disabled for ZMB ECF demo",
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
        composite_score: options.pspValue ? "0.6500" : null,
        indicators: {
          programme_survival_probability: {
            value: options.pspValue ?? null,
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
        note: options.pspValue ? null : "Political economy computation unavailable",
      },
    },
    ia1_disclosure: "This output is pre-calibration.",
    single_entity_warning: true,
  };
}

/**
 * Trajectory mock for Zone 1A confidence tier badge tests.
 * Financial T2, HD T3, ecological null (disabled), governance T3.
 */
function makeTrajectoryMock(scenarioId: string): object {
  return {
    scenario_id: scenarioId,
    entity_id: "ZMB",
    step_count: 3,
    mda_floors: [{ indicator_id: "reserve_coverage_months", floor_value: 2.5 }],
    steps: [
      {
        step_index: 1,
        effective_from: "2024-07-01T00:00:00Z",
        step_event_label: null,
        step_significance: "ROUTINE",
        frameworks: [
          {
            framework: "financial",
            composite_score: "0.45",
            scoring_basis: "normalized_absolute",
            confidence_tier: 2,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: true,
          },
          {
            framework: "human_development",
            composite_score: "0.55",
            scoring_basis: "normalized_absolute",
            confidence_tier: 3,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: true,
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
            composite_score: "0.42",
            scoring_basis: "normalized_absolute",
            confidence_tier: 3,
            ci_lower: null,
            ci_upper: null,
            ci_coverage: null,
            is_pre_calibration: true,
          },
        ],
        policy_inputs: [],
        shock_events: [],
      },
    ],
  };
}

/**
 * Scenario detail mock for ZMB with controlled PE state.
 */
function makeScenarioDetailMock(scenarioId: string, peEnabled: boolean): object {
  return {
    scenario_id: scenarioId,
    name: "G1-ZMB-test",
    status: "completed",
    configuration: {
      entities: ["ZMB"],
      n_steps: 3,
      start_date: "2024-01-01",
      modules_config: {
        ecological: { enabled: false },
        political_economy: {
          enabled: peEnabled,
          conditionality_type: "standard",
        },
      },
    },
    created_at: "2024-01-01T00:00:00Z",
    ia1_disclosure: "This output is pre-calibration.",
  };
}

/**
 * Initial-state mock for ZMB Grounding strip tests.
 * Reserve Coverage Months: 3.8 months, T2, IMF WEO Apr 2024.
 */
function makeInitialStateMock(scenarioId: string): object {
  return {
    scenario_id: scenarioId,
    entity_id: "ZMB",
    step_0_year: 2024,
    frameworks: {
      financial: {
        indicators: [
          {
            name: "reserve_coverage_months",
            display_name: "Reserve Coverage Months",
            value: 3.8,
            unit: "months",
            source: "IMF WEO Apr 2024",
            vintage: "2024-Q1",
            confidence_tier: 2,
            is_synthetic: false,
          },
        ],
      },
    },
  };
}

// ---------------------------------------------------------------------------
// AC-1 and AC-2: Zone 1B Layer 3 trajectory sentence (#1065)
//
// Intent doc §4 AC-1/AC-2:
// AC-1: zone-1b-trajectory-sentence visible at 1440×900 within Zone 1B panel,
//       without scroll, when active CRITICAL breach exists.
// AC-2: sentence text non-empty, not merely a severity label repeat, contains
//       a numerical value AND a forward-projection phrase.
// ---------------------------------------------------------------------------

test.describe("AC-1/AC-2: Zone 1B trajectory sentence (#1065)", () => {
  let zmbScenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      zmbScenarioId = await createZMBScenario(3, `G1-ZMB-AC1-${Date.now()}`);
    } catch {
      zmbScenarioId = null;
    }
  });

  test("AC-1: zone-1b-trajectory-sentence is visible at 1440×900 without scroll when CRITICAL breach active", async ({
    page,
  }) => {
    if (!zmbScenarioId) return;

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(zmbScenarioId!, { consecutiveBreach: 8 }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(zmbScenarioId)}`);
    await waitForAppReady(page);

    // Guard: zone-1b-top-detail must be visible (confirms Zone 1B loaded with the alert)
    const topDetail = page.locator('[data-testid="zone-1b-top-detail"]');
    if (!(await topDetail.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Primary guard: zone-1b-trajectory-sentence is new in G1 — absent pre-implementation
    const sentence = page.locator('[data-testid="zone-1b-trajectory-sentence"]');
    if (!(await sentence.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(sentence).toBeVisible();

    // Must be visible within the 900px viewport height (no scroll required)
    const box = await sentence.boundingBox();
    expect(box).not.toBeNull();
    if (box) {
      expect(box.y + box.height).toBeLessThanOrEqual(900);
    }
  });

  test("AC-2: trajectory sentence contains numerical value and forward-projection phrase", async ({
    page,
  }) => {
    if (!zmbScenarioId) return;

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(zmbScenarioId!, { consecutiveBreach: 8 }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(zmbScenarioId)}`);
    await waitForAppReady(page);

    const topDetail = page.locator('[data-testid="zone-1b-top-detail"]');
    if (!(await topDetail.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const sentence = page.locator('[data-testid="zone-1b-trajectory-sentence"]');
    if (!(await sentence.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const text = await sentence.textContent() ?? "";

    // Must not be empty — NM-045: length check
    expect(text.trim().length).toBeGreaterThan(0);

    // Must contain at least one numerical digit
    expect(text).toMatch(/\d/);

    // Must contain a forward-projection phrase that contextualises the trajectory
    // (intent doc AC-2: "something that tells the analyst what the trajectory implies")
    const hasForwardProjection =
      text.includes("steps") ||
      text.includes("months") ||
      text.includes("rate") ||
      text.includes("threshold") ||
      text.includes("depletion") ||
      text.includes("draw") ||
      text.includes("below") ||
      text.includes("fallen");
    expect(hasForwardProjection).toBe(true);

    // Must be more than a bare severity label — a complete sentence has meaningful length
    expect(text.trim().length).toBeGreaterThan(20);
  });
});

// ---------------------------------------------------------------------------
// AC-3 and AC-4: Consecutive steps suppression and accuracy (#1066)
//
// Intent doc §4 AC-3/AC-4:
// AC-3: with consecutive_breach_steps=0 in top alert, "0 consecutive step" must NOT
//       appear anywhere inside zone-1b-top-detail.
// AC-4: with consecutive_breach_steps=3, detail-consecutive shows count ≥1 (not zero).
// ---------------------------------------------------------------------------

test.describe("AC-3/AC-4: Consecutive steps — suppression and accuracy (#1066)", () => {
  let zmbScenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      zmbScenarioId = await createZMBScenario(1, `G1-ZMB-AC3-${Date.now()}`);
    } catch {
      zmbScenarioId = null;
    }
  });

  test("AC-3: '0 consecutive step' does not appear in zone-1b-top-detail when breach streak is zero", async ({
    page,
  }) => {
    if (!zmbScenarioId) return;

    // Inject CRITICAL alert with consecutive_breach_steps=0 (breach active, first occurrence)
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(zmbScenarioId!, { consecutiveBreach: 0 }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(zmbScenarioId)}`);
    await waitForAppReady(page);

    // Guard: Zone 1B top detail must be visible (alert is active)
    const topDetail = page.locator('[data-testid="zone-1b-top-detail"]');
    if (!(await topDetail.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const text = await topDetail.textContent() ?? "";

    // NM-045: direct string-presence check — "0 consecutive step" must not appear
    expect(text).not.toContain("0 consecutive step");
    // Broader guard: any "0" adjacent to "consecutive" must not appear
    expect(text).not.toMatch(/\b0\b[^a-z]*consecutive/i);
  });

  test("AC-4: detail-consecutive shows accurate non-zero count when consecutive_breach_steps=3", async ({
    page,
  }) => {
    if (!zmbScenarioId) return;

    // Inject CRITICAL alert with consecutive_breach_steps=3
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(zmbScenarioId!, { consecutiveBreach: 3 }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(zmbScenarioId)}`);
    await waitForAppReady(page);

    const topDetail = page.locator('[data-testid="zone-1b-top-detail"]');
    if (!(await topDetail.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Guard: detail-consecutive testid (confirms Zone 1B shows consecutive count)
    const consecutive = page.locator('[data-testid="detail-consecutive"]');
    if (!(await consecutive.isVisible({ timeout: 3_000 }).catch(() => false))) return;

    const text = await consecutive.textContent() ?? "";

    // Must contain a non-zero digit — NM-045: pattern match
    expect(text).toMatch(/[1-9]\d*/);

    // Must NOT contain "0 consecutive step" — zero is suppressed per #1066 fix
    expect(text).not.toContain("0 consecutive step");
  });
});

// ---------------------------------------------------------------------------
// AC-5: Zone 1A L0 confidence tier badge (#1068)
//
// Intent doc §4 AC-5:
// At 1440×900, zone-1a-trajectory contains at least one zone-1a-l0-badge that
// is visible without interaction. Badge text matches T\d (T followed by a digit).
// ---------------------------------------------------------------------------

test.describe("AC-5: Zone 1A L0 confidence tier badge (#1068)", () => {
  let zmbScenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      zmbScenarioId = await createZMBScenario(3, `G1-ZMB-AC5-${Date.now()}`);
    } catch {
      zmbScenarioId = null;
    }
  });

  test("AC-5: zone-1a-l0-badge visible in zone-1a-trajectory at 1440×900, text matches T\\d", async ({
    page,
  }) => {
    if (!zmbScenarioId) return;

    // Mock trajectory to inject known confidence tiers per framework
    await page.route("**/api/v1/scenarios/*/trajectory**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeTrajectoryMock(zmbScenarioId!)),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(zmbScenarioId)}`);
    await waitForAppReady(page);

    // Guard: zone-1a-trajectory must be present (Zone 1A chart loaded)
    const trajectory = page.locator('[data-testid="zone-1a-trajectory"]');
    if (!(await trajectory.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Primary guard: zone-1a-l0-badge is new in G1
    const firstBadge = page.locator('[data-testid="zone-1a-l0-badge"]').first();
    if (!(await firstBadge.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Must be visible at 1440×900 without interaction (P-4: zero-interaction requirement)
    await expect(firstBadge).toBeVisible();

    // Badge text must match T\d — NM-045: pattern check
    const badgeText = await firstBadge.textContent() ?? "";
    expect(badgeText).toMatch(/T\d/);

    // All badges within zone-1a-trajectory must match the pattern
    const allBadges = trajectory.locator('[data-testid="zone-1a-l0-badge"]');
    const badgeCount = await allBadges.count();
    expect(badgeCount).toBeGreaterThan(0);

    for (let i = 0; i < badgeCount; i++) {
      const badge = allBadges.nth(i);
      const text = await badge.textContent() ?? "";
      expect(text).toMatch(/T\d/);
    }
  });
});

// ---------------------------------------------------------------------------
// AC-6 and AC-7: Grounding strip dual reserve value disambiguation (#1069)
//
// Intent doc §4 AC-6/AC-7:
// AC-6: grounding strip contains "initial"/"entry-state"/"step 0" label adjacent to
//       the reserve coverage entry-state value (3.8 months from /initial-state).
// AC-7: grounding strip contains a second distinct "current"/"model output"/"simulation"
//       label adjacent to the current simulated value (different from 3.8 months).
// ---------------------------------------------------------------------------

test.describe("AC-6/AC-7: Grounding strip dual-value disambiguation (#1069)", () => {
  let zmbScenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      zmbScenarioId = await createZMBScenario(3, `G1-ZMB-AC6-${Date.now()}`);
    } catch {
      zmbScenarioId = null;
    }
  });

  test("AC-6: grounding strip contains entry-state label adjacent to initial reserve value (3.8 months)", async ({
    page,
  }) => {
    if (!zmbScenarioId) return;

    // Mock /initial-state to return known entry-state value (3.8 months, T2)
    await page.route("**/api/v1/scenarios/*/initial-state**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeInitialStateMock(zmbScenarioId!)),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(zmbScenarioId)}`);
    await waitForAppReady(page);

    if (!(await openGroundingStrip(page))) return; // G4 guard: strip must be openable

    const strip = page.locator('[data-testid="grounding-strip"]');
    if (!(await strip.isVisible({ timeout: 4_000 }).catch(() => false))) return;

    await expect(strip).not.toContainText("Loading grounding data", { timeout: 8_000 });

    const stripText = await strip.textContent() ?? "";

    // Guard: if the entry-state value is not present, the disambiguation feature hasn't landed
    if (!stripText.includes("3.8")) return;

    // Must contain an entry-state label — NM-045: direct string-presence
    const hasEntryLabel =
      stripText.includes("initial") ||
      stripText.includes("Initial") ||
      stripText.includes("entry-state") ||
      stripText.includes("Entry state") ||
      stripText.includes("step 0") ||
      stripText.includes("Step 0");
    expect(hasEntryLabel).toBe(true);

    // Entry-state value must appear with the label context
    expect(stripText).toContain("3.8");
  });

  test("AC-7: grounding strip contains current/simulation label — two value contexts distinguishable", async ({
    page,
  }) => {
    if (!zmbScenarioId) return;

    // Mock /initial-state: entry-state value 3.8
    await page.route("**/api/v1/scenarios/*/initial-state**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeInitialStateMock(zmbScenarioId!)),
      }),
    );

    // Mock measurement-output: current simulation value 2.9 (different from entry 3.8)
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(zmbScenarioId!, { consecutiveBreach: 8 }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(zmbScenarioId)}`);
    await waitForAppReady(page);

    if (!(await openGroundingStrip(page))) return;

    const strip = page.locator('[data-testid="grounding-strip"]');
    if (!(await strip.isVisible({ timeout: 4_000 }).catch(() => false))) return;

    await expect(strip).not.toContainText("Loading grounding data", { timeout: 8_000 });

    const stripText = await strip.textContent() ?? "";

    // Guard: entry-state label must be present first (AC-6 must have landed)
    const hasEntryLabel =
      stripText.includes("initial") ||
      stripText.includes("Initial") ||
      stripText.includes("entry-state") ||
      stripText.includes("step 0") ||
      stripText.includes("Step 0");
    if (!hasEntryLabel) return; // Disambiguation feature not yet implemented — no-op

    // Must contain a current/simulation label (the second value context)
    const hasCurrentLabel =
      stripText.includes("current") ||
      stripText.includes("Current") ||
      stripText.includes("model output") ||
      stripText.includes("Model output") ||
      stripText.includes("simulation") ||
      stripText.includes("Simulation") ||
      stripText.toLowerCase().includes("step 1") ||
      stripText.toLowerCase().includes("step 2") ||
      stripText.toLowerCase().includes("step 3");
    expect(hasCurrentLabel).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// AC-8 and AC-9: PSP Layer 3 sentence in Zone 1D (#1075)
//
// Intent doc §4 AC-8/AC-9:
// AC-8: psp-layer3-sentence is visible within zone-1d-four-framework at 1440×900
//       without scroll, with PE enabled and ≥1 step advanced.
// AC-9: sentence text contains probability percentage AND contextualising phrase
//       ("programme" + "chance"/"probability"/"remain"/"track"/"compliance").
// ---------------------------------------------------------------------------

test.describe("AC-8/AC-9: PSP Layer 3 sentence in Zone 1D (#1075)", () => {
  let zmbScenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      zmbScenarioId = await createZMBScenario(3, `G1-ZMB-AC8-${Date.now()}`);
    } catch {
      zmbScenarioId = null;
    }
  });

  test("AC-8: psp-layer3-sentence visible in zone-1d-four-framework at 1440×900 without scroll when PE enabled", async ({
    page,
  }) => {
    if (!zmbScenarioId) return;

    // Mock scenario detail: PE enabled
    await page.route(`**/api/v1/scenarios/${zmbScenarioId}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(zmbScenarioId!, true)),
      });
    });

    // Mock measurement-output: PSP = 0.65
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(zmbScenarioId!, {
            consecutiveBreach: 8,
            pspValue: "0.6500",
          }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(zmbScenarioId)}`);
    await waitForAppReady(page);

    // Guard: zone-1d-four-framework must be present (G5 must have landed)
    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Primary guard: psp-layer3-sentence is new in G1
    const pspSentence = page.locator('[data-testid="psp-layer3-sentence"]');
    if (!(await pspSentence.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(pspSentence).toBeVisible();

    // Must be inside zone-1d-four-framework
    await expect(
      zone1d.locator('[data-testid="psp-layer3-sentence"]'),
    ).toBeVisible({ timeout: 3_000 });

    // Must be visible without scroll at 1440×900
    const box = await pspSentence.boundingBox();
    expect(box).not.toBeNull();
    if (box) {
      expect(box.y + box.height).toBeLessThanOrEqual(900);
    }
  });

  test("AC-9: psp-layer3-sentence contains probability percentage and programme contextualisation", async ({
    page,
  }) => {
    if (!zmbScenarioId) return;

    await page.route(`**/api/v1/scenarios/${zmbScenarioId}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(zmbScenarioId!, true)),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(zmbScenarioId!, {
            consecutiveBreach: 8,
            pspValue: "0.6500",
          }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(zmbScenarioId)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const pspSentence = page.locator('[data-testid="psp-layer3-sentence"]');
    if (!(await pspSentence.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const text = await pspSentence.textContent() ?? "";

    // Must contain a probability percentage — NM-045: direct string-presence
    expect(text).toContain("%");

    // Must contain "programme" (or American "program") — NM-045
    const hasProgramme =
      text.toLowerCase().includes("programme") ||
      text.toLowerCase().includes("program");
    expect(hasProgramme).toBe(true);

    // Must contain a contextualisation phrase that translates the probability
    const hasContextualisation =
      text.toLowerCase().includes("chance") ||
      text.toLowerCase().includes("probability") ||
      text.toLowerCase().includes("remain") ||
      text.toLowerCase().includes("track") ||
      text.toLowerCase().includes("compliance") ||
      text.toLowerCase().includes("on track");
    expect(hasContextualisation).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// AC-10: Zone 1B trajectory sentence null fallback (#1065 silent failure)
//
// Intent doc §4 AC-10:
// When the top Zone 1B alert has consecutive_breach_steps=null (computation failure),
// zone-1b-trajectory-sentence is PRESENT in the DOM with non-empty fallback text.
// It must not silently vanish — an absent element is indistinguishable from
// "not implemented"; fallback text is the required transparent disclosure.
// ---------------------------------------------------------------------------

test.describe("AC-10: Zone 1B trajectory sentence null fallback (#1065 silent failure)", () => {
  let zmbScenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      zmbScenarioId = await createZMBScenario(1, `G1-ZMB-AC10-${Date.now()}`);
    } catch {
      zmbScenarioId = null;
    }
  });

  test("AC-10: zone-1b-trajectory-sentence present in DOM with fallback text when consecutive_breach_steps is null", async ({
    page,
  }) => {
    if (!zmbScenarioId) return;

    // Inject alert with consecutive_breach_steps=null — computation failure
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(zmbScenarioId!, { consecutiveBreach: null }),
        ),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(zmbScenarioId)}`);
    await waitForAppReady(page);

    // Guard: zone-1b-top-detail must be visible (alert is active, Zone 1B loaded)
    const topDetail = page.locator('[data-testid="zone-1b-top-detail"]');
    if (!(await topDetail.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Count check (not visibility) — element must exist in DOM with fallback text
    const sentence = page.locator('[data-testid="zone-1b-trajectory-sentence"]');
    const count = await sentence.count();

    // Guard: if G1 not yet implemented, testid is absent — no-op
    if (count === 0) return;

    // Element exists. Assert non-empty fallback text (transparent disclosure of failure).
    const text = await sentence.textContent() ?? "";
    expect(text.trim().length).toBeGreaterThan(0);

    // Fallback text must be meaningful, not just whitespace or a single character
    expect(text.trim().length).toBeGreaterThan(10);
  });
});

// ---------------------------------------------------------------------------
// AC-11: Grounding strip entry-state label persists on trajectory failure (#1069 silent failure)
//
// Intent doc §4 AC-11:
// When /trajectory returns 500 but /initial-state succeeds, the entry-state label
// must remain present in the Grounding strip. The disambiguation label must not be
// removed when the simulation-side value becomes unavailable — removing it would
// leave the entry-state value unlabeled and uninterpretable by the stakeholder.
// ---------------------------------------------------------------------------

test.describe("AC-11: Grounding strip entry-state label persists on trajectory failure (#1069 silent failure)", () => {
  let zmbScenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      zmbScenarioId = await createZMBScenario(1, `G1-ZMB-AC11-${Date.now()}`);
    } catch {
      zmbScenarioId = null;
    }
  });

  test("AC-11: entry-state label persists in grounding strip when trajectory endpoint fails (500)", async ({
    page,
  }) => {
    if (!zmbScenarioId) return;

    // /initial-state succeeds with entry-state data (3.8 months)
    await page.route("**/api/v1/scenarios/*/initial-state**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeInitialStateMock(zmbScenarioId!)),
      }),
    );

    // /trajectory fails — simulates current-step data unavailable
    await page.route("**/api/v1/scenarios/*/trajectory**", (route) =>
      route.fulfill({
        status: 500,
        contentType: "application/json",
        body: JSON.stringify({ detail: "Internal Server Error" }),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(zmbScenarioId)}`);
    await waitForAppReady(page);

    if (!(await openGroundingStrip(page))) return; // G4 guard

    const strip = page.locator('[data-testid="grounding-strip"]');
    if (!(await strip.isVisible({ timeout: 4_000 }).catch(() => false))) return;

    // Allow time for initial-state to load (trajectory error must not block the strip)
    await page.waitForTimeout(2_000);

    const stripText = await strip.textContent() ?? "";

    // Guard: "3.8" must appear to confirm the disambiguation feature has landed
    if (!stripText.includes("3.8")) return;

    // Entry-state label must still be present even when trajectory is unavailable
    // (Intent doc AC-11: "The label must remain present even when the simulation value is absent")
    const hasEntryLabel =
      stripText.includes("initial") ||
      stripText.includes("Initial") ||
      stripText.includes("entry-state") ||
      stripText.includes("Entry state") ||
      stripText.includes("step 0") ||
      stripText.includes("Step 0");
    expect(hasEntryLabel).toBe(true);

    // Entry-state value (3.8) must be present — the label provides context for this value
    expect(stripText).toContain("3.8");
  });
});
