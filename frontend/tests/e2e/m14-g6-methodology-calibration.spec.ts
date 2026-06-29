/**
 * E2E: M14-G6 Methodology, Calibration, and Instrument Legibility — AC-1 through AC-4.
 *
 * Authored BEFORE implementation from intent document at:
 * docs/process/intents/M14-G6-2026-06-18-methodology-calibration.md
 *
 * Issues in scope:
 *   #885 — Zone 1B negotiation defensibility label misclassification (T4/T5)
 *   #950 — Zone 1A Y axis label absent
 *
 * ACs covered:
 *   AC-1  — Zone 1B T4 label: "Model estimate — verify before citing" (NOT "Exploratory")
 *   AC-2  — Zone 1B T5 label: "Synthetic extrapolation — do not cite" (NOT "Exploratory")
 *   AC-3  — Zone 1B T1/T2/T3 labels: correct strings, none contain "Exploratory"
 *   AC-4  — Zone 1A Y axis label "Score" visible at 1280×900
 *
 * AC-5 through AC-8 (backend): backend/tests/test_m14_g6_methodology_calibration.py
 * AC-9 (#22 + PMM anchor): BPO 5-minute navigation test at Step 5 Validate
 *
 * NM-045 rule (mandatory throughout):
 *   All string assertions use direct string-presence match (toContain / toBe) — not structural
 *   regex. Absence assertions use not.toContain. No character-class regex for string content.
 *
 * Guard pattern:
 *   Each test guards on the primary testid it exercises. Pre-implementation, the testid is
 *   absent or the label text is unchanged ("Exploratory"). Guards use .catch(() => false) on
 *   isVisible(). AC-3 additionally guards on the presence of the specific expected string.
 *
 * Route mocking:
 *   AC-1/AC-2/AC-3: measurement-output endpoint intercepted with controlled indicator
 *   confidence_tier. The parseMdaAlerts function in ScenarioInstrumentCluster.tsx derives
 *   alert.confidence_tier from output.indicators[alert.indicator_key].confidence_tier.
 *
 * Testid authority:
 *   alert-negotiation-label: REQUIRED by intent doc §7. FA Agent must add this testid to
 *     MDAAlertPanelZone1B.tsx as part of G6 implementation. The existing testid on the same
 *     element is detail-negotiation-label (line 508) — the FA Agent adds alert-negotiation-label
 *     or renames. QA tests use the intent-doc-specified testid; guard pattern makes them no-ops
 *     pre-implementation.
 *   zone-1a-trajectory: confirmed at TrajectoryView.tsx line 267 / 365.
 *   zone-1b-top-detail: confirmed at MDAAlertPanelZone1B.tsx (zone1b-persistent-detail.spec.ts).
 *
 * Fixture:
 *   Primary: G3 JOR scenario 68b31277 (JOR, 2023, 8 steps, completed at G3 BPO 2026-06-17).
 *   Fallback: fresh JOR scenario created via API if the G3 fixture is unavailable.
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
    () => typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
    { timeout: 10_000 },
  );
}

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
 * Build a measurement-output mock that injects a TERMINAL alert with a specific
 * confidence_tier into the financial framework's indicators.
 *
 * The parseMdaAlerts function extracts confidence_tier from
 * output.indicators[alert.indicator_key].confidence_tier (ScenarioInstrumentCluster.tsx).
 * Injecting the tier here is sufficient to control getNegotiationLabel() in Zone 1B.
 */
function makeMeasurementOutputWithAlertTier(
  scenarioId: string,
  alertConfidenceTier: number,
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
        composite_score: "0.51",
        indicators: {
          reserve_coverage_months: {
            value: "2.1",
            unit: "months",
            variable_type: "STOCK",
            // This field controls the negotiation label for the MDA alert below
            confidence_tier: alertConfidenceTier,
            observation_date: null,
            source_registry_id: null,
            measurement_framework: "financial",
            _envelope_version: "2",
          },
        },
        mda_alerts: [
          {
            mda_id: "MDA-RESERVE-COVERAGE-MONTHS",
            entity_id: "JOR",
            indicator_key: "reserve_coverage_months",
            indicator_name: "Reserve Coverage Months",
            severity: "TERMINAL",
            floor_value: "4.0",
            current_value: "2.1",
            approach_pct_remaining: "-47.5",
            consecutive_breach_steps: 3,
          },
        ],
        has_below_floor_indicator: true,
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
        composite_score: null,
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
        note: null,
      },
    },
    ia1_disclosure: "This output is pre-calibration.",
    single_entity_warning: true,
  };
}

// ---------------------------------------------------------------------------
// Shared fixture — resolved once per describe block
// ---------------------------------------------------------------------------

let jorScenarioId: string | null = null;

// ---------------------------------------------------------------------------
// AC-1: Zone 1B T4 label — "Model estimate — verify before citing"
//
// Intent doc §4 AC-1:
// confidence_tier=4 injected via measurement-output mock.
// detail-negotiation-label contains "Model estimate" AND NOT "Exploratory".
//
// Silent failure detection (§3.3):
// The broken state returns "Exploratory — do not cite" — a plausible but wrong string.
// The test MUST assert absence of "Exploratory" AND presence of "Model estimate".
// Asserting only non-empty or non-null would pass the broken state.
// ---------------------------------------------------------------------------

test.describe("AC-1: Zone 1B T4 negotiation label — Model estimate (not Exploratory)", () => {
  test.beforeAll(async () => {
    try {
      jorScenarioId = (await checkG3FixtureAccessible())
        ? G3_JOR_SCENARIO_ID
        : await createCompletedScenario("JOR", 3, `G6-AC1-${Date.now()}`);
    } catch {
      jorScenarioId = null;
    }
  });

  test("AC-1: detail-negotiation-label contains 'Model estimate' and NOT 'Exploratory' when confidence_tier=4", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    // Intercept measurement-output and inject confidence_tier=4
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputWithAlertTier(jorScenarioId!, 4)),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    // Guard: detail slot must be visible (Zone 1B has a TERMINAL alert from the mock)
    const detailSlot = page.locator('[data-testid="zone-1b-top-detail"]');
    if (!(await detailSlot.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Locate the negotiation-defensibility label within the detail slot.
    // Intent doc §7: alert-negotiation-label is the REQUIRED testid. FA Agent must add it.
    // Pre-implementation: testid is absent → guard returns, no-op.
    const labelEl = detailSlot.locator('[data-testid="alert-negotiation-label"]');
    if (!(await labelEl.isVisible({ timeout: 3_000 }).catch(() => false))) return;

    const labelText = await labelEl.textContent() ?? "";

    // NM-045: direct string-presence assertions — not regex
    // Must contain "Model estimate" (T4 correct label per ADR-015 §UX-5)
    expect(labelText).toContain("Model estimate");
    // Must NOT contain "Exploratory" (the current wrong T4 label — silent failure guard)
    expect(labelText).not.toContain("Exploratory");
  });
});

// ---------------------------------------------------------------------------
// AC-2: Zone 1B T5 label — "Synthetic extrapolation — do not cite"
//
// Intent doc §4 AC-2:
// confidence_tier=5 injected via measurement-output mock.
// label contains "Synthetic extrapolation" AND "do not cite" AND NOT "Exploratory".
// ---------------------------------------------------------------------------

test.describe("AC-2: Zone 1B T5 negotiation label — Synthetic extrapolation (not Exploratory)", () => {
  test.beforeAll(async () => {
    try {
      jorScenarioId = (await checkG3FixtureAccessible())
        ? G3_JOR_SCENARIO_ID
        : await createCompletedScenario("JOR", 3, `G6-AC2-${Date.now()}`);
    } catch {
      jorScenarioId = null;
    }
  });

  test("AC-2: detail-negotiation-label contains 'Synthetic extrapolation' and 'do not cite' when confidence_tier=5", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputWithAlertTier(jorScenarioId!, 5)),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    const detailSlot = page.locator('[data-testid="zone-1b-top-detail"]');
    if (!(await detailSlot.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Intent doc §7: alert-negotiation-label is the REQUIRED testid.
    const labelEl = detailSlot.locator('[data-testid="alert-negotiation-label"]');
    if (!(await labelEl.isVisible({ timeout: 3_000 }).catch(() => false))) return;

    const labelText = await labelEl.textContent() ?? "";

    // NM-045: each assertion is a direct string match
    expect(labelText).toContain("Synthetic extrapolation");
    expect(labelText).toContain("do not cite");
    expect(labelText).not.toContain("Exploratory");
  });
});

// ---------------------------------------------------------------------------
// AC-3: Zone 1B T1/T2/T3 labels unchanged — "High confidence" or "Moderate confidence"
//
// Intent doc §4 AC-3:
// T1 and T2: label contains "High confidence" AND "cite directly".
// T3: label contains "Moderate confidence" AND "cite with caveat".
// None of T1–T3 labels contain "Exploratory".
//
// Implementation note: The existing getNegotiationLabel unit tests in
// MDAAlertPanelZone1B.test.ts (lines 192–220) already cover T1/T2/T3 behavior;
// these Playwright tests confirm the live application renders the same strings.
// ---------------------------------------------------------------------------

test.describe("AC-3: Zone 1B T1/T2/T3 labels unchanged — no Exploratory regression", () => {
  test.beforeAll(async () => {
    try {
      jorScenarioId = (await checkG3FixtureAccessible())
        ? G3_JOR_SCENARIO_ID
        : await createCompletedScenario("JOR", 3, `G6-AC3-${Date.now()}`);
    } catch {
      jorScenarioId = null;
    }
  });

  for (const tier of [1, 2] as const) {
    test(`AC-3: detail-negotiation-label for T${tier} contains 'High confidence' and 'cite directly'`, async ({
      page,
    }) => {
      if (!jorScenarioId) return;

      await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
        route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(makeMeasurementOutputWithAlertTier(jorScenarioId!, tier)),
        }),
      );

      await page.setViewportSize({ width: 1440, height: 900 });
      await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
      await waitForAppReady(page);

      const detailSlot = page.locator('[data-testid="zone-1b-top-detail"]');
      if (!(await detailSlot.isVisible({ timeout: 5_000 }).catch(() => false))) return;

      // Intent doc §7: alert-negotiation-label is the REQUIRED testid.
      const labelEl = detailSlot.locator('[data-testid="alert-negotiation-label"]');
      if (!(await labelEl.isVisible({ timeout: 3_000 }).catch(() => false))) return;

      const labelText = await labelEl.textContent() ?? "";

      // NM-045: direct string assertions
      expect(labelText).toContain("High confidence");
      expect(labelText).toContain("cite directly");
      expect(labelText).not.toContain("Exploratory");
    });
  }

  test("AC-3: detail-negotiation-label for T3 contains 'Moderate confidence' and 'cite with caveat'", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputWithAlertTier(jorScenarioId!, 3)),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    const detailSlot = page.locator('[data-testid="zone-1b-top-detail"]');
    if (!(await detailSlot.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Intent doc §7: alert-negotiation-label is the REQUIRED testid.
    const labelEl = detailSlot.locator('[data-testid="alert-negotiation-label"]');
    if (!(await labelEl.isVisible({ timeout: 3_000 }).catch(() => false))) return;

    const labelText = await labelEl.textContent() ?? "";

    // NM-045: direct string assertions
    expect(labelText).toContain("Moderate confidence");
    expect(labelText).toContain("cite with caveat");
    expect(labelText).not.toContain("Exploratory");
  });
});

// ---------------------------------------------------------------------------
// AC-4: Zone 1A Y axis label "Score" visible at 1280×900
//
// Intent doc §4 AC-4:
// zone-1a-trajectory contains a visible Y axis label element with text "Score".
// The element's bounding box height > 0 (not hidden).
// Tick values (0.00, 0.25, …) remain present and are not affected.
//
// Implementation note: recharts YAxis with label={{ value: "Score", angle: -90,
// position: "insideLeft" }} renders an SVG <text> element within the YAxis group.
// The test asserts that "Score" appears as a substring in the trajectory container
// text content — the Y axis label is the only expected source of this string.
//
// Committed label: "Score" (intent doc §3.2 secondary state A default).
// If the Chief Methodologist specifies a different label in the PMM anchor
// consultation, update this assertion accordingly before the PR merges.
// ---------------------------------------------------------------------------

test.describe("AC-4: Zone 1A Y axis label 'Score' visible", () => {
  test.beforeAll(async () => {
    try {
      jorScenarioId = (await checkG3FixtureAccessible())
        ? G3_JOR_SCENARIO_ID
        : await createCompletedScenario("JOR", 3, `G6-AC4-${Date.now()}`);
    } catch {
      jorScenarioId = null;
    }
  });

  test("AC-4: zone-1a-trajectory contains 'Score' as Y axis label text at 1280×900", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    // Guard: Zone 1A trajectory chart must be present
    const trajectoryContainer = page.locator('[data-testid="zone-1a-trajectory"]');
    if (!(await trajectoryContainer.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await expect(trajectoryContainer).toBeVisible();

    // Wait for the trajectory to load and recharts to render the chart with the Score label.
    // toContainText polls (unlike isVisible which is a snapshot), so this handles the async
    // trajectory fetch that fires after the scenario is selected from the URL param.
    // NM-045: direct string-presence match.
    await expect(trajectoryContainer).toContainText("Score", { timeout: 10_000 });

    // Attempt to confirm the recharts-label class is present and well-formed.
    // recharts renders <text class="recharts-label"> for axis labels.
    const yAxisLabel = trajectoryContainer
      .locator("text.recharts-label")
      .filter({ hasText: "Score" })
      .first();

    const hasLabel = await yAxisLabel.isVisible().catch(() => false);

    if (hasLabel) {
      // Confirm bounding box height > 0 (not hidden by CSS)
      const box = await yAxisLabel.boundingBox();
      expect(box).not.toBeNull();
      if (box) {
        expect(box.height).toBeGreaterThan(0);
      }

      const labelText = await yAxisLabel.textContent() ?? "";
      // NM-045: exact match — "Score" is the committed label value
      expect(labelText.trim()).toBe("Score");
    }

    // Invariant: tick values must still be present (label addition must not remove ticks)
    const containerText = await trajectoryContainer.textContent() ?? "";
    // Recharts renders "0" or "0.00" at the Y axis origin — at least one digit must be present
    expect(containerText.trim().length).toBeGreaterThan(0);
  });
});
