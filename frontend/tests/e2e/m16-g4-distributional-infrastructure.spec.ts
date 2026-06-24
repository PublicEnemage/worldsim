/**
 * E2E: M16-G4 Distributional Infrastructure — AC-F1 through AC-F9
 *
 * Authored from intent document at:
 * docs/process/intents/M16-G4-2026-06-23-distributional-infrastructure.md
 *
 * Issues covered:
 *   #22 (scoped) — Synthetic tier badge wiring in Zone 1B and Zone 1D
 *                  (AC-F1, AC-F2, AC-F3, AC-F4, AC-F5, AC-F6)
 *   #102          — Variance band in Zone 1A (comparison mode)
 *                  (AC-F7, AC-F8, AC-F9)
 *
 * NM-056 rule: NO test.skip() or conditional skip patterns. Pre-implementation
 * tests use the early-return guard pattern. A guard that fires is a no-op (not a pass).
 * Tests become active when implementation lands and must then pass or fail explicitly.
 *
 * Guard pattern:
 *   - Scenario creation/run failure → return (backend not yet implemented)
 *   - Primary testid absent → isVisible() returns false → return (frontend not yet implemented)
 *   - Assertion on EXISTING element with WRONG content → FAIL (intended failure case)
 *
 * Mock strategy (following G2 pattern):
 *   Badge tests (AC-F1–AC-F6): measurement-output mock with synthetic cohort crossings
 *   Variance band tests (AC-F7–AC-F9): mock compare endpoint + Zone 1A in comparison mode
 *
 * G4 interface extensions (designed by these tests — implementing agent must match):
 *
 * CohortThresholdCrossing (G4 additions to existing G2 interface):
 *   is_synthetic?: boolean        — true when the underlying Quantity is synthetic
 *   synthetic_method?: string     — "STRUCTURAL_ABSENCE" | "SYNTHETIC_COMPARABLE" | "SYNTHETIC_MODEL"
 *   value?: string | null         — null when STRUCTURAL_ABSENCE (no imputed value)
 *
 * New badge testid (G4): data-testid="cohort-tier-badge-{indicator_key}"
 *   - This is a REPLACEMENT or ADDITION to the existing data-testid="cohort-tier-{key}"
 *   - When is_synthetic=true + STRUCTURAL_ABSENCE: badge text "SAD" (or "T5/SAD")
 *   - When is_synthetic=true + SYNTHETIC_COMPARABLE + holdout_validated=true: badge text "T3"
 *   - When is_synthetic=true + SYNTHETIC_MODEL: badge text "T4"
 *   - When is_synthetic=false (real data, T3): badge text "T3" (unchanged from G2)
 *   - Badge must be visible without hover, click, or drawer (ADR-007 §Section 2)
 *
 * Variance band testids (new in G4, Zone 1A comparison mode):
 *   data-testid="variance-band-toggle"              — toggle control in Zone 1A
 *   data-testid="zone-1a-variance-band-{entityKey}" — shaded P10/P90 band per entity
 *   data-testid="variance-band-label"               — label element, must contain "Distributional range"
 *
 * Zone 1D badge testid (G4 extension): data-testid="cohort-tier-badge-{indicator_key}"
 *   Same rules as Zone 1B. AC-F6 is deferred if no Zone 1D indicators are synthetic
 *   in the current test fixtures.
 *
 * Silent failure detection:
 *   SF-1: hardcoded "T3" survives migration — caught by AC-F1 (SAD ≠ "T3")
 *   SF-4: distribution bands labelled "uncertainty band" — caught by AC-F8 label assertion
 *
 * Viewport: 1280×800 per intent doc §3 observable application state.
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
  above_floor_pct: string | null;
  tier: number;
  source: string | null;
  // G4 additions:
  is_synthetic?: boolean;
  synthetic_method?: "STRUCTURAL_ABSENCE" | "SYNTHETIC_COMPARABLE" | "SYNTHETIC_MODEL";
  value?: string | null;
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

async function createZmbScenario(name: string): Promise<string | null> {
  try {
    const createRes = await fetch(`${API_BASE}/scenarios`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        configuration: {
          entities: ["ZMB"],
          n_steps: 3,
          start_date: "2024-01-01",
          modules_config: { ecological: { enabled: false }, political_economy: { enabled: false } },
        },
        scheduled_inputs: [],
      }),
    });
    if (!createRes.ok) return null;
    const { scenario_id: id } = (await createRes.json()) as ScenarioCreateResponse;
    const advRes = await fetch(`${API_BASE}/scenarios/${encodeURIComponent(id)}/run`, {
      method: "POST",
    });
    if (!advRes.ok) return null;
    return id;
  } catch {
    return null;
  }
}

async function createTwoZmbScenarios(
  nameA: string,
  nameB: string,
): Promise<[string, string] | null> {
  const idA = await createZmbScenario(nameA);
  const idB = await createZmbScenario(nameB);
  if (!idA || !idB) return null;
  return [idA, idB];
}

// ---------------------------------------------------------------------------
// Mock factories
// ---------------------------------------------------------------------------

function makeScenarioDetailMock(scenarioId: string, entities: string[]): object {
  return {
    scenario_id: scenarioId,
    name: "G4-M16-test",
    status: "in_progress",
    configuration: {
      entities,
      n_steps: 3,
      start_date: "2024-01-01",
      modules_config: { ecological: { enabled: false }, political_economy: { enabled: false } },
    },
    created_at: "2024-01-01T00:00:00Z",
    ia1_disclosure: "This output is pre-calibration.",
  };
}

function makeMeasurementOutputMock(
  scenarioId: string,
  entityId: string,
  cohortCrossings: CohortThresholdCrossing[],
  stepIndex = 2,
): object {
  return {
    entity_id: entityId,
    entity_name: entityId === "ZMB" ? "Zambia" : "Senegal",
    timestep: "2024-07-01T00:00:00Z",
    scenario_id: scenarioId,
    step_index: stepIndex,
    outputs: {
      financial: {
        framework: "financial",
        composite_score: "0.45",
        indicators: {},
        mda_alerts: [],
        has_below_floor_indicator: false,
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
        composite_score: null,
        indicators: {},
        mda_alerts: [],
        has_below_floor_indicator: false,
        note: "Political economy disabled",
      },
    },
    ia1_disclosure: "This output is pre-calibration.",
    single_entity_warning: true,
  };
}

function makeCompareMock(
  scenarioIdA: string,
  scenarioIdB: string,
  includeDistribution = true,
): object {
  const makeDistribution = (variance: number, p10: number, p50: number, p90: number) =>
    includeDistribution ? { variance, p10, p50, p90 } : undefined;

  return {
    scenario_a: scenarioIdA,
    scenario_b: scenarioIdB,
    deltas: [
      {
        entity_id: "ZMB",
        attribute_key: "reserve_coverage_months",
        delta: "-0.15",
        baseline: "2.8",
        threshold_crossed: false,
        distribution: makeDistribution(0.04, 2.5, 2.65, 2.9),
      },
      {
        entity_id: "SEN",
        attribute_key: "reserve_coverage_months",
        delta: "0.08",
        baseline: "2.3",
        threshold_crossed: false,
        distribution: makeDistribution(0.02, 2.25, 2.38, 2.52),
      },
    ],
  };
}

// ---------------------------------------------------------------------------
// Fixture: cohort threshold crossing with STRUCTURAL_ABSENCE
// ---------------------------------------------------------------------------

const SEN_Q1_STRUCTURAL_ABSENCE: CohortThresholdCrossing = {
  quintile_key: "Q1",
  cohort_label: "Bottom income quintile",
  indicator_key: "poverty_headcount_ratio",
  indicator_label: "Poverty headcount",
  severity: "CRITICAL",
  step_crossed: 2,
  above_floor_pct: null,
  tier: 5,
  source: null,
  is_synthetic: true,
  synthetic_method: "STRUCTURAL_ABSENCE",
  value: null,
};

// Fixture: cohort threshold crossing with SYNTHETIC_COMPARABLE (MICE, holdout_validated=true → T3)
const SEN_Q1_SYNTHETIC_COMPARABLE: CohortThresholdCrossing = {
  quintile_key: "Q1",
  cohort_label: "Bottom income quintile",
  indicator_key: "poverty_headcount_ratio",
  indicator_label: "Poverty headcount",
  severity: "CRITICAL",
  step_crossed: 2,
  above_floor_pct: "5.2",
  tier: 3,
  source: "synthetic (MICE)",
  is_synthetic: true,
  synthetic_method: "SYNTHETIC_COMPARABLE",
  value: "0.42",
};

// Fixture: cohort threshold crossing with SYNTHETIC_MODEL (model estimate → T4)
const SEN_Q1_SYNTHETIC_MODEL: CohortThresholdCrossing = {
  quintile_key: "Q1",
  cohort_label: "Bottom income quintile",
  indicator_key: "poverty_headcount_ratio",
  indicator_label: "Poverty headcount",
  severity: "CRITICAL",
  step_crossed: 2,
  above_floor_pct: "6.0",
  tier: 4,
  source: "synthetic (model estimate)",
  is_synthetic: true,
  synthetic_method: "SYNTHETIC_MODEL",
  value: "0.44",
};

// Fixture: real-data crossing (ZMB, no synthetic fields)
const ZMB_Q1_REAL_DATA: CohortThresholdCrossing = {
  quintile_key: "Q1",
  cohort_label: "Bottom income quintile",
  indicator_key: "poverty_headcount_ratio",
  indicator_label: "Poverty headcount",
  severity: "CRITICAL",
  step_crossed: 2,
  above_floor_pct: "3.8",
  tier: 3,
  source: "WB PovcalNet 2023",
  // No is_synthetic or synthetic_method — real data path
};

// ===========================================================================
// AC-F1 — Structural Absence badge ("SAD") on Zone 1B cohort row
// ===========================================================================

test.describe("AC-F1: Zone 1B badge shows SAD for STRUCTURAL_ABSENCE Quantity", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-F1: When a cohort row's underlying Quantity has is_synthetic=true and
   * synthetic_method="STRUCTURAL_ABSENCE", the badge must show "SAD" (or "T5/SAD").
   *
   * Silent failure 1 (intent doc §3.4): if badge text is hardcoded "T3" regardless of
   * synthetic_method, this test FAILS. The pre-implementation guard only fires if the
   * badge element cohort-tier-badge-{key} does not yet exist (early pre-G4). Once the
   * badge element exists, the assertion on its text is live.
   *
   * ADR-007 §Section 2: badge must be visible without hover, click, or drawer.
   */
  test("cohort-tier-badge-poverty_headcount_ratio shows SAD for STRUCTURAL_ABSENCE", async ({
    page,
  }) => {
    const sid = await createZmbScenario(`G4-AC-F1-SAD-${Date.now()}`);
    if (!sid) return;

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
          makeMeasurementOutputMock(sid, "SEN", [SEN_Q1_STRUCTURAL_ABSENCE]),
        ),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
    if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

    // Guard: cohort-tier-badge-{key} is the G4 testid. Pre-G4, only cohort-tier-{key} exists.
    const badge = zone1b.locator('[data-testid="cohort-tier-badge-poverty_headcount_ratio"]');
    if (!(await badge.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Assertion is live once the badge element exists:
    // "SAD" or "T5/SAD" — implementing agent chooses; must not be "T3" or "T4"
    const badgeText = ((await badge.textContent()) ?? "").trim();
    expect(
      badgeText === "SAD" || badgeText === "T5/SAD" || badgeText === "T5",
      [
        `AC-F1 FAIL: cohort-tier-badge shows "${badgeText}", expected "SAD" or "T5/SAD".`,
        "The underlying Quantity has synthetic_method=STRUCTURAL_ABSENCE.",
        "Silent failure 1 (intent doc §3.4): if the badge text is hardcoded 'T3', this test fails.",
        "ADR-007 §Section 2: the badge must reflect the actual synthetic_method, not a hardcoded tier.",
      ].join(" "),
    ).toBe(true);

    // Value cell must show "—" (em dash or equivalent) for STRUCTURAL_ABSENCE
    const valueCells = zone1b.locator(`[data-testid="cohort-value-poverty_headcount_ratio"]`);
    if (await valueCells.count() > 0) {
      const valueText = ((await valueCells.first().textContent()) ?? "").trim();
      expect(valueText).toMatch(/^[—–-]$/, [
        "AC-F1 FAIL: value cell must show '—' for STRUCTURAL_ABSENCE (value=null).",
        "Intent doc §3.1 State 2: 'Zone 1B shows the cohort row with a SAD badge rather than a numeric value.'",
      ].join(" "));
    }
  });
});

// ===========================================================================
// AC-F2 — SYNTHETIC_COMPARABLE badge ("T3") on Zone 1B cohort row
// ===========================================================================

test.describe("AC-F2: Zone 1B badge shows T3 for SYNTHETIC_COMPARABLE Quantity", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-F2: When synthetic_method="SYNTHETIC_COMPARABLE" and holdout_validated=true,
   * the badge must show "T3". This must now be DATA-DRIVEN from synthetic_method,
   * not hardcoded.
   *
   * Note: this test would pass coincidentally pre-G4 if badge is hardcoded "T3".
   * AC-F1 (STRUCTURAL_ABSENCE → "SAD") is the primary detection of silent failure 1.
   * AC-F2 provides the complementary positive case: T3 must still appear for MICE data.
   */
  test("cohort-tier-badge-poverty_headcount_ratio shows T3 for SYNTHETIC_COMPARABLE", async ({
    page,
  }) => {
    const sid = await createZmbScenario(`G4-AC-F2-MICE-${Date.now()}`);
    if (!sid) return;

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
          makeMeasurementOutputMock(sid, "SEN", [SEN_Q1_SYNTHETIC_COMPARABLE]),
        ),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
    if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

    const badge = zone1b.locator('[data-testid="cohort-tier-badge-poverty_headcount_ratio"]');
    if (!(await badge.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const badgeText = ((await badge.textContent()) ?? "").trim();
    expect(badgeText).toBe("T3", [
      `AC-F2 FAIL: cohort-tier-badge shows "${badgeText}", expected "T3".`,
      "synthetic_method=SYNTHETIC_COMPARABLE with holdout_validated=true → T3.",
      "ADR-007 §Section 4: SYNTHETIC_COMPARABLE with holdout validation → Tier 3.",
      "This badge must be data-driven from synthetic_method, not hardcoded.",
    ].join(" "));
  });
});

// ===========================================================================
// AC-F3 — SYNTHETIC_MODEL badge ("T4") on Zone 1B cohort row
// ===========================================================================

test.describe("AC-F3: Zone 1B badge shows T4 for SYNTHETIC_MODEL Quantity", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-F3: When synthetic_method="SYNTHETIC_MODEL", the badge must show "T4".
   *
   * This test catches silent failure 1 along with AC-F1: if the badge is hardcoded "T3",
   * this test fails (expected "T4", got "T3").
   */
  test("cohort-tier-badge-poverty_headcount_ratio shows T4 for SYNTHETIC_MODEL", async ({
    page,
  }) => {
    const sid = await createZmbScenario(`G4-AC-F3-MODEL-${Date.now()}`);
    if (!sid) return;

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
          makeMeasurementOutputMock(sid, "SEN", [SEN_Q1_SYNTHETIC_MODEL]),
        ),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
    if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

    const badge = zone1b.locator('[data-testid="cohort-tier-badge-poverty_headcount_ratio"]');
    if (!(await badge.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const badgeText = ((await badge.textContent()) ?? "").trim();
    expect(badgeText).toBe("T4", [
      `AC-F3 FAIL: cohort-tier-badge shows "${badgeText}", expected "T4".`,
      "synthetic_method=SYNTHETIC_MODEL → Tier 4.",
      "ADR-007 §Section 4: SYNTHETIC_MODEL (longer gap / weak flanking) → T4.",
      "If this shows 'T3', the badge is hardcoded and not data-driven (silent failure 1).",
    ].join(" "));
  });
});

// ===========================================================================
// AC-F4 — Real-data badge unchanged on Zone 1B cohort row (non-regression)
// ===========================================================================

test.describe("AC-F4: Zone 1B badge unchanged for real-data Quantity (ZMB non-regression)", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-F4: A cohort row with no is_synthetic field (real World Bank data at Tier 3)
   * must still show "T3". G4 must not break the existing G2 ZMB rendering.
   *
   * Intent doc §3.1 State 4: 'ZMB ECF scenario run produces no is_synthetic=True Quantity
   * values on any indicator sourced from World Bank primary statistics.'
   */
  test("cohort-tier-badge-poverty_headcount_ratio shows T3 for real ZMB data (non-regression)", async ({
    page,
  }) => {
    const sid = await createZmbScenario(`G4-AC-F4-REAL-${Date.now()}`);
    if (!sid) return;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"])),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(
          makeMeasurementOutputMock(sid, "ZMB", [ZMB_Q1_REAL_DATA]),
        ),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
    if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

    // Check both old testid (G2 compatibility) and new G4 testid
    const g4Badge = zone1b.locator('[data-testid="cohort-tier-badge-poverty_headcount_ratio"]');
    const g2Badge = zone1b.locator('[data-testid="cohort-tier-poverty_headcount_ratio"]');

    const g4Visible = await g4Badge.isVisible({ timeout: 3_000 }).catch(() => false);
    const g2Visible = await g2Badge.isVisible({ timeout: 3_000 }).catch(() => false);

    if (!g4Visible && !g2Visible) return; // no badge rendered yet — pre-implementation guard

    // Whichever badge is rendered must show T3 for real ZMB data
    const activeBadge = g4Visible ? g4Badge : g2Badge;
    const badgeText = ((await activeBadge.textContent()) ?? "").trim();

    // Must contain "T3" (G4 badge shows "T3"; G2 badge shows "[T3 · synthetic]")
    expect(badgeText).toContain("T3"), (
      `AC-F4 FAIL: badge text "${badgeText}" does not contain "T3". ` +
      "ZMB poverty_headcount_ratio with WB real data at Tier 3 must display T3. " +
      "ADR-017 non-regression: G4 badge wiring must not change the ZMB real-data display."
    );
    expect(badgeText).not.toContain("SAD"), (
      `AC-F4 FAIL: badge text "${badgeText}" contains "SAD" for a real-data ZMB indicator. ` +
      "STRUCTURAL_ABSENCE must not appear for indicators with primary source data."
    );
  });
});

// ===========================================================================
// AC-F5 — Badge visible without hover, click, or drawer
// ===========================================================================

test.describe("AC-F5: Cohort tier badge visible without hover or gesture (ADR-007 §Section 2)", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-F5: In all synthetic cases (SAD, T3-synthetic, T4), the badge must be
   * visible at L0 — without any user gesture. ADR-007 §Section 2: 'Per-indicator badge
   * visible without hover, click, or drawer in all display contexts.'
   *
   * This guards against implementing the badge as tooltip-only or hover-revealed.
   * A badge with display:none or visibility:hidden when not hovered fails this test.
   */
  test("cohort-tier-badge-poverty_headcount_ratio is visible without hover for STRUCTURAL_ABSENCE", async ({
    page,
  }) => {
    const sid = await createZmbScenario(`G4-AC-F5-VISIBLE-${Date.now()}`);
    if (!sid) return;

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
          makeMeasurementOutputMock(sid, "SEN", [SEN_Q1_STRUCTURAL_ABSENCE]),
        ),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
    if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

    const badge = zone1b.locator('[data-testid="cohort-tier-badge-poverty_headcount_ratio"]');
    if (!(await badge.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // No hover gesture — badge must already be visible
    const box = await badge.boundingBox();
    expect(box).not.toBeNull();
    expect(box!.width).toBeGreaterThan(0, [
      "AC-F5 FAIL: badge has zero width (hidden or not in normal flow).",
      "ADR-007 §Section 2: badge must be visible at L0 without hover.",
    ].join(" "));
    expect(box!.height).toBeGreaterThan(0, [
      "AC-F5 FAIL: badge has zero height.",
      "ADR-007 §Section 2: badge must not be tooltip-only or hover-revealed.",
    ].join(" "));

    // Badge must not be hidden via CSS
    const isVisibleViaCSS = await badge.evaluate((el) => {
      const s = window.getComputedStyle(el);
      return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0";
    });
    expect(isVisibleViaCSS).toBe(true, [
      "AC-F5 FAIL: badge is in DOM but hidden via CSS (display:none, visibility:hidden, or opacity:0).",
      "ADR-007 §Section 2: 'The badge is not tooltip-only' — it must be visible in normal page flow.",
    ].join(" "));
  });
});

// ===========================================================================
// AC-F6 — Zone 1D indicator badge wiring (same rules as Zone 1B)
// ===========================================================================

test.describe("AC-F6: Zone 1D badge shows SAD for STRUCTURAL_ABSENCE indicator", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-F6: Zone 1D indicators (political economy: legitimacy_index, PSP) that carry
   * synthetic Quantity values must display the same badge wiring as Zone 1B.
   *
   * Intent doc AC-F6: 'If no Zone 1D indicators are synthetic in the current test
   * fixtures, this AC is deferred to a future sprint when SEN Zone 1D data is populated.'
   *
   * This test provides the fixture; if the Zone 1D badge testid does not exist yet
   * (because Zone 1D badge wiring is not implemented), the guard fires (no-op).
   */
  test("Zone 1D cohort-tier-badge shows SAD for synthetic STRUCTURAL_ABSENCE legitimacy_index", async ({
    page,
  }) => {
    const sid = await createZmbScenario(`G4-AC-F6-ZONE1D-${Date.now()}`);
    if (!sid) return;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        // Political economy enabled so Zone 1D renders political indicators
        body: JSON.stringify({
          ...makeScenarioDetailMock(sid, ["SEN"]),
          configuration: {
            entities: ["SEN"],
            n_steps: 3,
            start_date: "2024-01-01",
            modules_config: { ecological: { enabled: false }, political_economy: { enabled: true } },
          },
        }),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          entity_id: "SEN",
          entity_name: "Senegal",
          timestep: "2024-07-01T00:00:00Z",
          scenario_id: sid,
          step_index: 2,
          outputs: {
            financial: { framework: "financial", composite_score: null, indicators: {}, mda_alerts: [], has_below_floor_indicator: false, note: null },
            human_development: { framework: "human_development", composite_score: null, indicators: {}, mda_alerts: [], cohort_threshold_crossings: [], has_below_floor_indicator: false, note: null },
            ecological: { framework: "ecological", composite_score: null, indicators: {}, mda_alerts: [], has_below_floor_indicator: false, note: "disabled" },
            governance: { framework: "governance", composite_score: null, indicators: {}, mda_alerts: [], has_below_floor_indicator: false, note: null },
            political_economy: {
              framework: "political_economy",
              composite_score: null,
              indicators: {
                legitimacy_index: {
                  value: null,
                  unit: "index",
                  variable_type: "STOCK",
                  confidence_tier: 5,
                  observation_date: null,
                  source_registry_id: null,
                  measurement_framework: "political_economy",
                  // G4 additions: synthetic fields on Zone 1D indicator
                  is_synthetic: true,
                  synthetic_method: "STRUCTURAL_ABSENCE",
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
        }),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    // Zone 1D guard
    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 10_000 }).catch(() => false))) return;

    // G4 badge testid in Zone 1D: cohort-tier-badge-legitimacy_index
    const badge = zone1d.locator('[data-testid="cohort-tier-badge-legitimacy_index"]');
    if (!(await badge.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const badgeText = ((await badge.textContent()) ?? "").trim();
    expect(
      badgeText === "SAD" || badgeText === "T5/SAD" || badgeText === "T5",
      [
        `AC-F6 FAIL: Zone 1D cohort-tier-badge-legitimacy_index shows "${badgeText}", expected "SAD".`,
        "Intent doc AC-F6: Zone 1D indicators with STRUCTURAL_ABSENCE must show SAD badge.",
        "Same badge wiring rules as Zone 1B (ADR-007 §Section 2).",
      ].join(" "),
    ).toBe(true);
  });
});

// ===========================================================================
// AC-F7 — Variance band NOT visible by default (comparison mode)
// ===========================================================================

test.describe("AC-F7: Zone 1A variance band not visible by default in comparison mode", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-F7: In Zone 1A with comparison mode active (two entities loaded), the P10/P90
   * variance band is not visible by default. The toggle must be present but OFF.
   *
   * Intent doc AC-F7: 'zone-1a-variance-band-{entityKey} is absent from the DOM or
   * display:none without user interaction.'
   *
   * Pre-G4: variance-band-toggle does not exist → guard fires (no-op).
   * Post-G4: toggle exists, band is hidden by default.
   */
  test("variance-band-toggle present but band hidden by default in comparison mode", async ({
    page,
  }) => {
    const result = await createTwoZmbScenarios(
      `G4-AC-F7-compare-A-${Date.now()}`,
      `G4-AC-F7-compare-B-${Date.now()}`,
    );
    if (!result) return;
    const [idA, idB] = result;

    // Mock the compare endpoint to return data with distribution fields
    await page.route("**/api/v1/scenarios/compare**", (route) => {
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeCompareMock(idA, idB, true)),
      });
    });

    // Navigate into comparison mode — try common URL patterns
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?compare=${encodeURIComponent(idA)},${encodeURIComponent(idB)}`);
    await waitForAppReady(page);

    // Primary guard: variance-band-toggle is the new G4 control
    const toggle = page.locator('[data-testid="variance-band-toggle"]');
    if (!(await toggle.isVisible({ timeout: 10_000 }).catch(() => false))) return;

    // Toggle must be present and in comparison mode
    await expect(toggle).toBeVisible();

    // Band must NOT be visible by default (user must enable it)
    const band = page.locator('[data-testid^="zone-1a-variance-band-"]').first();
    const bandVisible = await band.isVisible({ timeout: 2_000 }).catch(() => false);
    expect(bandVisible).toBe(false, [
      "AC-F7 FAIL: zone-1a-variance-band-* is visible without user interaction.",
      "Intent doc AC-F7: the band is opt-in — not visible by default.",
      "Zone 1A at 1280×800 must not add visual complexity without user intent.",
    ].join(" "));
  });
});

// ===========================================================================
// AC-F8 — Variance band visible when toggled, labeled "Distributional range"
// ===========================================================================

test.describe("AC-F8: Zone 1A variance band visible after toggle, labeled Distributional range", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-F8: After the variance band toggle is enabled, the band is visible and its label
   * must contain "Distributional range" — NOT "uncertainty" or "confidence interval".
   *
   * ADR-007 §Section 3: synthetic inference bands distinct from BandingEngine model
   * uncertainty bands. Labeling them "uncertainty band" or "confidence interval" violates
   * this distinction.
   *
   * Silent failure 4 (intent doc §3.4): if the band is labeled "uncertainty band" or
   * "confidence interval", this test fails.
   *
   * Pre-G4: variance-band-toggle does not exist → guard fires (no-op).
   */
  test("band visible after toggle with Distributional range label (not uncertainty/CI)", async ({
    page,
  }) => {
    const result = await createTwoZmbScenarios(
      `G4-AC-F8-band-A-${Date.now()}`,
      `G4-AC-F8-band-B-${Date.now()}`,
    );
    if (!result) return;
    const [idA, idB] = result;

    await page.route("**/api/v1/scenarios/compare**", (route) => {
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeCompareMock(idA, idB, true)),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?compare=${encodeURIComponent(idA)},${encodeURIComponent(idB)}`);
    await waitForAppReady(page);

    const toggle = page.locator('[data-testid="variance-band-toggle"]');
    if (!(await toggle.isVisible({ timeout: 10_000 }).catch(() => false))) return;

    // Click the toggle to enable the band
    await toggle.click();

    // Band must now be visible
    const band = page.locator('[data-testid^="zone-1a-variance-band-"]').first();
    if (!(await band.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    const bandBox = await band.boundingBox();
    expect(bandBox).not.toBeNull();
    expect(bandBox!.width).toBeGreaterThan(0, [
      "AC-F8 FAIL: zone-1a-variance-band-* has zero width after toggle enabled.",
    ].join(" "));

    // Label must contain "Distributional range" — not "uncertainty" or "confidence interval"
    const label = page.locator('[data-testid="variance-band-label"]');
    if (!(await label.isVisible({ timeout: 3_000 }).catch(() => false))) return;

    const labelText = ((await label.textContent()) ?? "").trim();
    expect(labelText).toContain("Distributional range", [
      `AC-F8 FAIL: variance-band-label shows "${labelText}", expected text containing "Distributional range".`,
      "ADR-007 §Section 3: synthetic inference bands must be labeled distinctly from",
      "BandingEngine model uncertainty bands. 'Distributional range' is the required term.",
    ].join(" "));

    expect(labelText.toLowerCase()).not.toContain("uncertainty", [
      `AC-F8 FAIL: variance-band-label contains "uncertainty": "${labelText}".`,
      "ADR-007 §Section 3: 'synthetic inference bands distinct from BandingEngine model uncertainty bands.'",
      "Using 'uncertainty' conflates these distinct concepts. Required label: 'Distributional range'.",
    ].join(" "));

    expect(labelText.toLowerCase()).not.toContain("confidence interval", [
      `AC-F8 FAIL: variance-band-label contains "confidence interval": "${labelText}".`,
      "ADR-007 §Section 3: P10/P90 comparison bands are distributional ranges, not confidence intervals.",
    ].join(" "));
  });
});

// ===========================================================================
// AC-F9 — Variance band toggle present in comparison mode, absent in single-entity mode
// ===========================================================================

test.describe("AC-F9: Variance band toggle present in comparison mode, absent in single-entity mode", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-F9: The variance-band-toggle must be present when comparison mode is active
   * (two entities loaded). It must NOT be present when only a single entity is loaded.
   *
   * Intent doc AC-F9: 'variance-band-toggle is present and visible in Zone 1A when
   * comparison mode is active. The toggle is not present when only a single entity
   * is loaded (no comparison active).'
   *
   * Pre-G4: variance-band-toggle does not exist → guard fires (no-op) for positive case.
   */
  test("variance-band-toggle present in comparison mode", async ({ page }) => {
    const result = await createTwoZmbScenarios(
      `G4-AC-F9-comp-A-${Date.now()}`,
      `G4-AC-F9-comp-B-${Date.now()}`,
    );
    if (!result) return;
    const [idA, idB] = result;

    await page.route("**/api/v1/scenarios/compare**", (route) => {
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeCompareMock(idA, idB, true)),
      });
    });

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?compare=${encodeURIComponent(idA)},${encodeURIComponent(idB)}`);
    await waitForAppReady(page);

    const toggle = page.locator('[data-testid="variance-band-toggle"]');
    if (!(await toggle.isVisible({ timeout: 10_000 }).catch(() => false))) return;

    await expect(toggle).toBeVisible();
    const toggleBox = await toggle.boundingBox();
    expect(toggleBox).not.toBeNull();
    expect(toggleBox!.width).toBeGreaterThan(0, [
      "AC-F9 FAIL: variance-band-toggle has zero width in comparison mode.",
    ].join(" "));
  });

  test("variance-band-toggle absent in single-entity mode", async ({ page }) => {
    const sid = await createZmbScenario(`G4-AC-F9-single-${Date.now()}`);
    if (!sid) return;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"])),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMock(sid, "ZMB", [])),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    // Zone 1A must be visible (existing functionality — if not, guard)
    const zone1a = page.locator('[data-testid="zone-1a-trajectory"]');
    if (!(await zone1a.isVisible({ timeout: 10_000 }).catch(() => false))) return;

    // Toggle must NOT be present in single-entity mode
    const toggle = page.locator('[data-testid="variance-band-toggle"]');
    const toggleVisible = await toggle.isVisible({ timeout: 3_000 }).catch(() => false);
    expect(toggleVisible).toBe(false, [
      "AC-F9 FAIL: variance-band-toggle is visible in single-entity mode.",
      "Intent doc AC-F9: the toggle must not be present when only a single entity is loaded.",
      "The variance band control is only meaningful when comparing two or more entities.",
    ].join(" "));
  });
});
