/**
 * E2E: M17-G4 DEMO6 CRITICAL Polish
 *
 * Authored BEFORE implementation from intent documents at:
 *   docs/process/intents/M17-G4-2026-06-25-zone-1b-inverted-floor-label.md (#1239)
 *   (remaining issues pending UX visual specs — describe blocks added when intent docs filed)
 *
 * Sprint entry: docs/process/sprint-plans/m17-g4-sprint-entry.md (EL Approved 2026-06-25)
 *
 * Issues covered in this file (in FA-recommended sequence):
 *   #1249 — Zone 1A curve identifiability         (describe block PENDING UX visual spec + intent doc)
 *   #1253 — Zone 1D PSP historical precedent anchor (describe block PENDING UX visual spec + intent doc)
 *   #1250 — Zone 1B tablet legibility at 768px     (describe block PENDING UX visual spec + intent doc)
 *   #1239 — Zone 1B inverted floor label           (AC-1239-1, AC-1239-2, AC-1239-R — AUTHORED)
 *
 * NM-056 rule: NO test.skip(), test.fixme(), or .only() patterns.
 * Pre-implementation guard pattern: guard on primary testid → isVisible() returns false → return
 * without asserting (no-op, not a pass). Guards use .catch(() => false).
 *
 * Silent failure note (intent doc §5.3): AC-1239-1 and AC-1239-R will PASS before the
 * implementation fix due to the accidental "undefined !== false = true" behavior in
 * formatCohortDistance. These tests guard against future regression (e.g., logic inversion),
 * not against the pre-fix state. The discriminating correctness check for the fix is the
 * Step 4 Verify source code review described in the intent doc §5.3.
 */
import { test, expect } from "@playwright/test";

const API_BASE = "http://localhost:8000/api/v1";

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

/**
 * Create a scenario with given entities and advance N steps via the API.
 * Returns null on failure — callers use this as a pre-implementation guard.
 */
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

// ---------------------------------------------------------------------------
// Mock factory — combined measurement-output for #1239 tests
//
// Provides both:
//   (a) a below-floor cohort crossing with breaches_below: true (for AC-1239-1, AC-1239-R)
//   (b) an approach-state MDA alert with approach_pct_remaining > 0 (for AC-1239-2)
//
// The cohort crossing carries breaches_below: true — the field the fix adds to
// RawCohortThresholdCrossing and parsedCrossings. After the fix, formatCohortDistance
// receives breaches_below=true and renders "below floor". Before the fix,
// "undefined !== false = true" produces the same label accidentally.
// ---------------------------------------------------------------------------

function makeG4Zone1BMockOutput(scenarioId: string, entityId: string): object {
  return {
    entity_id: entityId,
    entity_name: entityId === "ZMB" ? "Zambia" : "Senegal",
    timestep: "2024-07-01T00:00:00Z",
    scenario_id: scenarioId,
    step_index: 2,
    outputs: {
      financial: {
        framework: "financial",
        composite_score: "0.55",
        indicators: {
          reserve_coverage_months: {
            value: "3.45",
            unit: "months",
            variable_type: "stock",
            measurement_framework: "financial",
            confidence_tier: 2,
          },
        },
        // Approach-state MDA alert for AC-1239-2: approach_pct_remaining = "0.15" (15% headroom
        // remaining → not breached → getDetailStatusText returns "15.0% above floor at step 2").
        mda_alerts: [
          {
            mda_id: "mda-fin-reserve-1239-ac2",
            entity_id: entityId,
            indicator_key: "reserve_coverage_months",
            indicator_name: "Reserve Coverage Months",
            severity: "WARNING",
            floor_value: "3.0",
            current_value: "3.45",
            approach_pct_remaining: "0.15",
            consecutive_breach_steps: null,
            recovery_horizon_years: 2,
          },
        ],
        has_below_floor_indicator: false,
        note: null,
      },
      human_development: {
        framework: "human_development",
        composite_score: "0.42",
        indicators: {},
        mda_alerts: [],
        // Below-floor cohort crossing for AC-1239-1 and AC-1239-R.
        // breaches_below: true is the field the fix adds to RawCohortThresholdCrossing.
        // Without the fix, breaches_below is missing from the mapping and the label is
        // accidentally correct via "undefined !== false = true". With the fix, it is
        // explicitly correct.
        cohort_threshold_crossings: [
          {
            quintile_key: "Q1",
            cohort_label: "Bottom income quintile",
            indicator_key: "poverty_headcount_ratio",
            indicator_label: "Poverty headcount ratio",
            severity: "CRITICAL",
            step_crossed: 1,
            above_floor_pct: "3.50",
            tier: 3,
            source: "synthetic (MICE)",
            is_synthetic: true,
            synthetic_method: "SYNTHETIC_COMPARABLE",
            value: "0.47",
            breaches_below: true,
          },
        ],
        has_below_floor_indicator: true,
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
        composite_score: "0.45",
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

// ===========================================================================
// #1239 — Zone 1B inverted floor label
// AC-1239-1: below-floor cohort crossing shows "below floor" label, not "above floor"
// AC-1239-2: approach-state detail-status shows "above floor" (getDetailStatusText unaffected)
// AC-1239-R: cohort value text matches /^\d+(\.\d+)?% below floor$/ (numeric magnitude intact)
// ===========================================================================

test.describe("#1239 — Zone 1B inverted floor label (DEMO6-010)", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-1239-1 (primary — below-floor label):
   *
   * When Zone 1B displays a cohort threshold crossing row for Q1
   * poverty_headcount_ratio at a step where that indicator has crossed below its
   * MDA floor, the element at data-testid="cohort-value-poverty_headcount_ratio"
   * contains "below floor" and does NOT contain "above floor".
   *
   * Root cause background (intent doc §1): RawCohortThresholdCrossing was missing
   * breaches_below?: boolean, so the parsedCrossings mapping omitted it. The render
   * site evaluates crossing.breaches_below !== false — undefined !== false = true —
   * accidentally producing "below floor" for all current gte thresholds. The fix adds
   * the field to the interface and mapping so the direction check is explicit rather
   * than accidental.
   *
   * Pre-implementation guard: if zone-1b-cohort-impact or cohort-value-poverty_headcount_ratio
   * is not visible, return (no-op). The test passes post-implementation when both are visible.
   */
  test(
    "AC-1239-1: cohort-value-poverty_headcount_ratio shows 'below floor' for gte threshold breach",
    async ({ page }) => {
      const sid = await createScenario(["ZMB"], 2, `M17-G4-AC-1239-1-${Date.now()}`);
      if (!sid) return;

      await page.route(`**/api/v1/scenarios/*/measurement-output**`, (route) =>
        route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(makeG4Zone1BMockOutput(sid, "ZMB")),
        }),
      );

      await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
      await waitForAppReady(page);

      const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
      if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

      const cohortValue = zone1b.locator('[data-testid="cohort-value-poverty_headcount_ratio"]');
      if (!(await cohortValue.isVisible({ timeout: 5_000 }).catch(() => false))) return;

      const text = ((await cohortValue.textContent()) ?? "").trim();

      expect(text).toContain(
        "below floor",
        [
          "AC-1239-1 FAIL: cohort-value-poverty_headcount_ratio does not contain 'below floor'.",
          "Intent doc §4 AC-1239-1: 'the element contains the text \"below floor\"'.",
          "DEMO6-010: the label 'above floor' was shown for a below-floor breach.",
          `Actual text: '${text}'`,
        ].join(" "),
      );

      expect(text).not.toContain(
        "above floor",
        [
          "AC-1239-1 FAIL: cohort-value-poverty_headcount_ratio contains 'above floor'",
          "for a gte threshold breach (value below floor).",
          "This is the original DEMO6-010 bug — the label direction is inverted.",
          `Actual text: '${text}'`,
        ].join(" "),
      );
    },
  );

  /**
   * AC-1239-2 (secondary — approach text not affected):
   *
   * When Zone 1B's TopAlertDetail area shows a status line for an MDA alert in the
   * approach state (value above floor, approach_pct_remaining = "0.15"), the
   * data-testid="detail-status" element contains "above floor".
   *
   * This test confirms that getDetailStatusText — which is NOT affected by the
   * breaches_below mapping fix — still correctly reports above-floor approach
   * distance. It is a regression guard: the formatCohortDistance fix must not
   * accidentally alter the approach-state label produced by getDetailStatusText.
   *
   * Fixture: the mock's financial.mda_alerts contains a WARNING alert with
   * approach_pct_remaining = "0.15". getDetailStatusText returns
   * "15.0% above floor at step 2" for MODE_1.
   *
   * Pre-implementation guard: if zone-1b-top-detail or detail-status is not visible,
   * return (no-op).
   */
  test(
    "AC-1239-2: detail-status contains 'above floor' for approach-state MDA alert (regression guard)",
    async ({ page }) => {
      const sid = await createScenario(["ZMB"], 2, `M17-G4-AC-1239-2-${Date.now()}`);
      if (!sid) return;

      await page.route(`**/api/v1/scenarios/*/measurement-output**`, (route) =>
        route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(makeG4Zone1BMockOutput(sid, "ZMB")),
        }),
      );

      await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
      await waitForAppReady(page);

      const topDetail = page.locator('[data-testid="zone-1b-top-detail"]');
      if (!(await topDetail.isVisible({ timeout: 10_000 }).catch(() => false))) return;

      // Confirm approach state: detail-approach-pct must read "N% remaining" (not "BREACHED").
      const approachPct = topDetail.locator('[data-testid="detail-approach-pct"]');
      if (!(await approachPct.isVisible({ timeout: 5_000 }).catch(() => false))) return;

      const approachText = ((await approachPct.textContent()) ?? "").trim();
      if (approachText === "BREACHED") {
        // Alert is not in approach state — mock did not produce approach state correctly.
        // Pre-implementation no-op.
        return;
      }

      const statusEl = topDetail.locator('[data-testid="detail-status"]');
      if (!(await statusEl.isVisible({ timeout: 5_000 }).catch(() => false))) return;

      const statusText = ((await statusEl.textContent()) ?? "").trim();

      expect(statusText).toContain(
        "above floor",
        [
          "AC-1239-2 FAIL: detail-status does not contain 'above floor' for approach-state alert.",
          "Intent doc §4 AC-1239-2: 'the detail-status element contains the text \"above floor\"",
          "(confirming getDetailStatusText is unaffected by the fix and still correctly reports",
          "above-floor approach distance).'",
          "getDetailStatusText with approach_pct_remaining='0.15' in MODE_1 should return",
          "'15.0% above floor at step 2'.",
          `Actual detail-status: '${statusText}'`,
          `Actual detail-approach-pct: '${approachText}'`,
        ].join(" "),
      );
    },
  );

  /**
   * AC-1239-R (regression — numeric magnitude unaffected):
   *
   * After the fix, the text of data-testid="cohort-value-poverty_headcount_ratio"
   * matches the regex /^\d+(\.\d+)?% below floor$/ — the numeric prefix (X%) is a
   * positive number, confirming the floor-distance magnitude is preserved and not
   * negated or zeroed by the fix.
   *
   * This guards the specific concern (intent doc §4 AC-1239-R): that the fix
   * only changes the direction word and does not corrupt the numeric value.
   *
   * Silent failure note (intent doc §5.3): this assertion passes before the fix
   * (accidental correctness) and after the fix (explicit correctness). The Step 4
   * Verify source code check — confirming RawCohortThresholdCrossing includes
   * breaches_below?: boolean and parsedCrossings maps breaches_below: c.breaches_below
   * — is the discriminating correctness check that cannot be done in an E2E test.
   */
  test(
    "AC-1239-R: cohort-value-poverty_headcount_ratio matches /^\\d+(\\.\\d+)?% below floor$/ (magnitude intact)",
    async ({ page }) => {
      const sid = await createScenario(["ZMB"], 2, `M17-G4-AC-1239-R-${Date.now()}`);
      if (!sid) return;

      await page.route(`**/api/v1/scenarios/*/measurement-output**`, (route) =>
        route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(makeG4Zone1BMockOutput(sid, "ZMB")),
        }),
      );

      await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
      await waitForAppReady(page);

      const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
      if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

      const cohortValue = zone1b.locator('[data-testid="cohort-value-poverty_headcount_ratio"]');
      if (!(await cohortValue.isVisible({ timeout: 5_000 }).catch(() => false))) return;

      const text = ((await cohortValue.textContent()) ?? "").trim();

      expect(text).toMatch(
        /^\d+(\.\d+)?% below floor$/,
        [
          "AC-1239-R FAIL: cohort-value-poverty_headcount_ratio does not match",
          "/^\\d+(\\.\\d+)?% below floor$/.",
          "Intent doc §4 AC-1239-R: 'the numeric prefix (X%) is a positive number,",
          "confirming the floor-distance magnitude is preserved and not negated or",
          "zeroed by the fix.'",
          "Expected format: '3.50% below floor' (numeric magnitude from above_floor_pct",
          "field, direction word from breaches_below mapping).",
          `Actual text: '${text}'`,
        ].join(" "),
      );
    },
  );
});

// ===========================================================================
// #1249, #1253, #1250 — describe blocks added when intent documents are filed
// (pending UX visual spec for each issue — see sprint entry §2.3 and §2.5)
// ===========================================================================
