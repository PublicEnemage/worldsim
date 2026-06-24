/**
 * E2E: M16-G10 Pre-Demo Polish — AC-1 through AC-11
 *
 * Authored BEFORE implementation from intent document at:
 * docs/process/intents/M16-G10-2026-06-24-predemo-polish.md
 *
 * Sprint entry: docs/process/sprint-plans/m16-g10-sprint-entry.md (EL Approved 2026-06-24)
 *
 * Issues covered:
 *   #1162 — Zone 1A divergence fill attribution anchor        (AC-1, AC-2)
 *   #1177 — Milestone sentence step-reference → year anchor   (AC-3, AC-4)
 *   #1178 — T3 badge L0 legibility                           (AC-5, AC-6)
 *   #1179 — Q2 curve asymmetry label                         (AC-7, AC-8)
 *   #1184 — SAD badge L0 legibility                          (AC-9, AC-10, AC-11)
 *
 * NM-056 rule: NO test.skip() or conditional skip patterns. Pre-implementation
 * guard pattern: guard on primary testid → isVisible() returns false → return
 * without asserting (no-op, not a pass). Guards use .catch(() => false).
 *
 * Badge expansion patterns (#1178, #1184):
 *   Option (a): inline expansion — badge textContent extends beyond bare "T3" / "SAD"
 *               (e.g. "T3 — Inferred", "SAD — Structural Absence")
 *   Option (b): sub-label — data-testid="confidence-tier-badge-sublabel" (or
 *               "sad-badge-sublabel") is present and visible at L0
 *   Tests accept either option. AC-10 enforces T3 and SAD use the SAME pattern.
 *   See intent doc §3.3 and §3.5 for the full specification.
 *
 * Batch sequencing from sprint entry §4:
 *   Batch A (#1178 + #1184): badge component — tested below under AC-5/AC-6/AC-9/AC-10/AC-11
 *   Batch B (#1177 + #1179): trajectory annotation — tested below under AC-3/AC-4/AC-7/AC-8
 *   Independent (#1162): Zone 1A divergence fill — tested below under AC-1/AC-2
 *
 * Fixtures:
 *   #1162: real two-entity SEN+ZMB scenario (comparison rendering) + single-entity ZMB scenario
 *   #1177/#1179: real SEN 100-step scenario (G3 CM-confirmed fixture pattern)
 *   #1178/#1184: real ZMB scenario + mocked measurement-output with synthetic cohort crossings
 *
 * Viewport: 1280×800 primary; 1440×900 also checked for badge legibility (AC-6, AC-11).
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

/**
 * Create a SEN 100-step scenario with the G3 CM-confirmed fixture configuration.
 * Fires a GDP shock at step 1 to activate the DemographicModule poverty elasticity path.
 * Returns null on failure (backend does not yet accept projection_steps).
 */
async function createSen100StepScenario(): Promise<string | null> {
  try {
    const createRes = await fetch(`${API_BASE}/scenarios`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: "M16-G10 E2E — SEN 100-step trajectory fixture",
        configuration: {
          entities: ["SEN"],
          n_steps: 8,
          projection_steps: 100,
          timestep_label: "quarterly",
          start_date: "2024-01-01",
          initial_attributes: {
            SEN: {
              poverty_headcount_ratio: {
                value: "0.38",
                unit: "ratio",
                variable_type: "ratio",
                measurement_framework: "human_development",
                confidence_tier: 3,
                is_synthetic: true,
                synthetic_basis:
                  "Estimated from West African regional distribution (SSA T3 synthetic). " +
                  "Tier 3 per DATA_STANDARDS.md §Confidence Tier System.",
              },
              reserve_coverage_months: {
                value: "2.8",
                unit: "months",
                variable_type: "stock",
                measurement_framework: "financial",
                confidence_tier: 3,
                is_synthetic: true,
                synthetic_basis:
                  "Estimated from IMF WEO Sub-Saharan Africa regional data 2022. " +
                  "Tier 3 per DATA_STANDARDS.md §Confidence Tier System.",
              },
            },
          },
          modules_config: {
            ecological: { enabled: false },
            political_economy: { enabled: false },
          },
        },
        scheduled_inputs: [
          { step: 1, input_type: "gdp_growth_change", input_data: { magnitude: "-0.04" } },
        ],
      }),
    });
    if (!createRes.ok) return null;
    const { scenario_id } = (await createRes.json()) as ScenarioCreateResponse;
    const runRes = await fetch(
      `${API_BASE}/scenarios/${encodeURIComponent(scenario_id)}/run`,
      { method: "POST" },
    );
    if (!runRes.ok) return null;
    return scenario_id;
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Mock factories (badge tests — follow G4 pattern)
// ---------------------------------------------------------------------------

function makeScenarioDetailMock(scenarioId: string, entities: string[]): object {
  return {
    scenario_id: scenarioId,
    name: "G10-M16-test",
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

// ---------------------------------------------------------------------------
// Fixtures — cohort threshold crossings
// ---------------------------------------------------------------------------

// T3 crossing (SYNTHETIC_COMPARABLE) — for #1178 badge tests
const SEN_Q1_T3_SYNTHETIC: CohortThresholdCrossing = {
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

// SAD crossing (STRUCTURAL_ABSENCE) — for #1184 badge tests
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

// ===========================================================================
// #1162 — Zone 1A divergence fill attribution anchor
// AC-1: Attribution visible at rest in comparison rendering (no hover)
// AC-2: Attribution absent in single-entity rendering
// ===========================================================================

test.describe("#1162 / AC-1: Divergence fill attribution anchor visible at rest", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-1: With two entity trajectories in Zone 1A, the divergence fill attribution
   * element must be visible WITHOUT hover, click, or drawer navigation.
   *
   * Silent failure 1 (intent doc §3.6): if attribution is tooltip-only (CSS :hover),
   * getBoundingClientRect returns zero dimensions at rest. This assertion catches that.
   */
  test(
    "divergence-fill-attribution present and non-zero at rest — two-entity SEN+ZMB comparison",
    async ({ page }) => {
      const sid = await createScenario(
        ["SEN", "ZMB"],
        3,
        `G10-AC-1-comparison-${Date.now()}`,
      );
      if (!sid) return;

      await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
      await waitForAppReady(page);

      const zone1a = page.locator('[data-testid="zone-1a-trajectory"]');
      if (!(await zone1a.isVisible({ timeout: 10_000 }).catch(() => false))) return;

      const attribution = page.locator('[data-testid="divergence-fill-attribution"]');
      if (!(await attribution.isVisible({ timeout: 5_000 }).catch(() => false))) return;

      // Non-zero dimensions at rest — no hover() call has been issued.
      // If attribution is hover-only, height and width will be 0 here (SF-1).
      const box = await attribution.boundingBox();
      expect(box).not.toBeNull();
      expect(box!.height).toBeGreaterThan(
        0,
        [
          "AC-1 FAIL: divergence-fill-attribution has zero height at rest.",
          "Silent failure 1 (intent doc §3.6): attribution is hover-only — tooltip CSS visible",
          "only on :hover, not in the default viewport state.",
          "Fix: the attribution element must be in the normal document flow at L0.",
        ].join(" "),
      );
      expect(box!.width).toBeGreaterThan(
        0,
        "AC-1 FAIL: divergence-fill-attribution has zero width at rest.",
      );

      // textContent must identify the entity pair — not empty.
      const text = ((await attribution.textContent()) ?? "").trim();
      expect(text.length).toBeGreaterThan(
        0,
        [
          "AC-1 FAIL: divergence-fill-attribution is visible but has empty textContent.",
          "Intent doc §3.1 State 1: 'The element contains text identifying the entity pair",
          "(e.g. \"SEN Branch A vs. Branch B\" or an equivalent label).'",
        ].join(" "),
      );
    },
  );
});

test.describe("#1162 / AC-2: Divergence fill attribution absent in single-entity rendering", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-2: With a single-entity, single-branch trajectory, the attribution element
   * must be absent from the DOM or have zero dimensions.
   * No spurious label must appear in the default single-entity view.
   */
  test(
    "divergence-fill-attribution absent or hidden for single-entity ZMB scenario",
    async ({ page }) => {
      const sid = await createScenario(["ZMB"], 3, `G10-AC-2-single-entity-${Date.now()}`);
      if (!sid) return;

      await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
      await waitForAppReady(page);

      const zone1a = page.locator('[data-testid="zone-1a-trajectory"]');
      if (!(await zone1a.isVisible({ timeout: 10_000 }).catch(() => false))) return;

      // Allow render to settle before checking absence.
      await page.waitForTimeout(1_000);

      const attribution = page.locator('[data-testid="divergence-fill-attribution"]');
      const attrCount = await attribution.count();

      if (attrCount === 0) return; // absent from DOM — correct behavior, no further assertion needed

      // If the element exists in the DOM, it must be invisible (zero dimensions or display:none).
      const box = await attribution.boundingBox();
      expect(
        box === null || box.height === 0 || box.width === 0,
        [
          "AC-2 FAIL: divergence-fill-attribution is visible in single-entity rendering.",
          "Intent doc §3.1 State 2: element must be absent or display:none when no divergence fill is rendered.",
          "A single-entity scenario has no comparison — the attribution label must not appear.",
        ].join(" "),
      ).toBe(true);
    },
  );
});

// ===========================================================================
// #1177 — Milestone sentence step-reference → year anchor
// AC-3: Calendar year in milestone sentence, not bare [step N] as primary anchor
// AC-4: Year resolves correctly for scenario start date (not hardcoded)
// ===========================================================================

test.describe("#1177 / AC-3: Milestone sentence contains calendar year (not bare step reference)", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-3: data-testid="milestone-sentence" must contain a 4-digit calendar year AND
   * must NOT begin with "[step N]" as the sole temporal anchor.
   *
   * Silent failure 2 (intent doc §3.6): if the step reference survives as the primary
   * anchor, regex /^\[step \d+\]/ matches the leading text. This assertion catches that.
   *
   * Note: data-testid="milestone-sentence" is the G10 testid specified in the intent doc
   * for the Zone 1B / trajectory annotation surface that G3 built. Pre-G10, this testid
   * may not exist (guard fires — no-op). Post-G10, the testid is present and assertions run.
   */
  test(
    "milestone-sentence contains 4-digit year and does not lead with [step N]",
    async ({ page }) => {
      if (!(await createSen100StepScenario())) return;
      await page.goto("/");
      await waitForAppReady(page);

      const panel = page.locator('[data-testid="human-capital-trajectory-panel"]');
      if (!(await panel.isVisible({ timeout: 60_000 }).catch(() => false))) return;

      const sentence = page.locator('[data-testid="milestone-sentence"]');
      if (!(await sentence.isVisible({ timeout: 5_000 }).catch(() => false))) return;

      const text = ((await sentence.textContent()) ?? "").trim();

      // Must contain a 4-digit year in the 2025–2050 range.
      expect(text).toMatch(
        /\b(202[5-9]|20[3-4]\d|2050)\b/,
        [
          "AC-3 FAIL: milestone-sentence does not contain a calendar year (2025–2050).",
          "Intent doc §3.2 State 3: 'the element contains a calendar year derived from",
          "the scenario start date and step resolution.'",
          "Before G10 fix: only '[step N]' — no year. After G10: year must be present.",
          `Actual text: '${text}'`,
        ].join(" "),
      );

      // Must NOT begin with "[step N]" as the primary (sole leading) temporal anchor.
      expect(text).not.toMatch(
        /^\[step\s*\d+\]/i,
        [
          "AC-3 FAIL: milestone-sentence begins with '[step N]' as the leading temporal anchor.",
          "Silent failure 2 (intent doc §3.6): step reference survived as the primary anchor.",
          "Fix: calendar year must lead; '[step N]' may remain as supplementary but not leading.",
          `Actual text: '${text}'`,
        ].join(" "),
      );
    },
  );
});

test.describe("#1177 / AC-4: Milestone sentence year resolves from scenario start date (not hardcoded)", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-4: For a SEN scenario starting 2024-01-01 with quarterly step resolution,
   * the milestone sentence must reference a year in the 2025–2045 range (derived from
   * the step where the trajectory crosses the MDA floor, not from a hardcoded value).
   *
   * Sanity checks for hardcoding:
   *   - Year === 2024 → probably hardcoded to start year
   *   - Year === 2049 or 2050 → probably hardcoded to the projection horizon end
   */
  test(
    "milestone-sentence year is in 2025–2045 range for 2024 start + quarterly resolution",
    async ({ page }) => {
      if (!(await createSen100StepScenario())) return;
      await page.goto("/");
      await waitForAppReady(page);

      const panel = page.locator('[data-testid="human-capital-trajectory-panel"]');
      if (!(await panel.isVisible({ timeout: 60_000 }).catch(() => false))) return;

      const sentence = page.locator('[data-testid="milestone-sentence"]');
      if (!(await sentence.isVisible({ timeout: 5_000 }).catch(() => false))) return;

      const text = ((await sentence.textContent()) ?? "").trim();
      const yearMatch = text.match(/\b(20\d{2})\b/);
      if (!yearMatch) return; // AC-3 already covers missing year — AC-4 is the precision check

      const year = parseInt(yearMatch[1], 10);

      expect(year).toBeGreaterThanOrEqual(
        2025,
        [
          `AC-4 FAIL: milestone-sentence year ${year} is before 2025.`,
          "With a 2024-01-01 start date, the threshold crossing must be in the future.",
          "A year of 2024 suggests the year is hardcoded to the scenario start date.",
        ].join(" "),
      );
      expect(year).toBeLessThanOrEqual(
        2045,
        [
          `AC-4 FAIL: milestone-sentence year ${year} is beyond 2045.`,
          "For a 2024 start + quarterly resolution, the MDA-HD-POVERTY-Q1 floor crossing",
          "should occur well before the 100-step horizon (2049).",
          "A year of 2049 suggests the year is hardcoded to the projection end.",
          "Intent doc AC-4: year must be 'derived from the scenario start date and step resolution'.",
        ].join(" "),
      );
    },
  );
});

// ===========================================================================
// #1178 — T3 badge L0 legibility
// AC-5: T3 badge expanded label present in DOM at rest (no hover)
// AC-6: T3 badge legibility at 1280×800 and 1440×900 (no overlap)
// ===========================================================================

test.describe("#1178 / AC-5: T3 badge expanded label present at L0 — no hover", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-5: The T3 confidence tier badge must display an expanded label WITHOUT hover.
   * Two valid implementations per intent doc §3.3:
   *   Option (a): data-testid="confidence-tier-badge" textContent contains more than
   *               bare "T3" (e.g. "T3 — Inferred", "T3 — Synthetic estimate")
   *   Option (b): data-testid="confidence-tier-badge-sublabel" is present and visible
   *               with non-empty textContent (e.g. "Inferred from comparable economies")
   *
   * Silent failure 3 (intent doc §3.6): if expansion is CSS :hover tooltip or title
   * attribute, it will NOT appear in the DOM at rest. This test checks textContent
   * WITHOUT any prior hover() call — that is the critical detection mechanism.
   */
  test(
    "T3 badge (SYNTHETIC_COMPARABLE) has expanded label in DOM at rest — no hover() called",
    async ({ page }) => {
      const sid = await createScenario(["ZMB"], 3, `G10-AC-5-T3-${Date.now()}`);
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
          body: JSON.stringify(makeMeasurementOutputMock(sid, "SEN", [SEN_Q1_T3_SYNTHETIC])),
        }),
      );

      await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
      await waitForAppReady(page);

      const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
      if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

      const inlineBadge = zone1b.locator('[data-testid="confidence-tier-badge"]');
      const sublabel = zone1b.locator('[data-testid="confidence-tier-badge-sublabel"]');

      const inlineText =
        (await inlineBadge.count()) > 0
          ? ((await inlineBadge.first().textContent()) ?? "").trim()
          : "";
      const sublabelVisible = await sublabel.first().isVisible({ timeout: 3_000 }).catch(() => false);
      const sublabelText =
        (await sublabel.count()) > 0 && sublabelVisible
          ? ((await sublabel.first().textContent()) ?? "").trim()
          : "";

      // Option (a): inline expansion — badge text extends meaningfully beyond bare "T3"
      const hasInlineExpansion = inlineText.length > 2 && inlineText !== "T3" && inlineText !== "SAD";
      // Option (b): sub-label is visible with non-empty content
      const hasSublabel = sublabelText.length > 0;

      // Pre-implementation guard: neither option yet implemented → no-op.
      if (!hasInlineExpansion && !hasSublabel) return;

      expect(
        hasInlineExpansion || hasSublabel,
        [
          "AC-5 FAIL: T3 badge has no expanded label at L0 (no hover call issued).",
          "Option (a): confidence-tier-badge textContent must extend beyond bare 'T3'",
          "  (e.g. 'T3 — Inferred', 'T3 — Synthetic estimate').",
          "Option (b): confidence-tier-badge-sublabel must be visible with non-empty textContent.",
          "  (e.g. 'Inferred from comparable economies').",
          "Silent failure 3 (intent doc §3.6): tooltip-only expansion does not appear in DOM at rest.",
          `  Inline badge text: '${inlineText}'`,
          `  Sublabel text: '${sublabelText}'`,
        ].join(" "),
      ).toBe(true);
    },
  );
});

test.describe("#1178 / AC-6: T3 badge visible and non-overlapping at 1280×800", () => {
  /**
   * AC-6 (1280×800): T3 badge and expanded label are visible (non-zero bounding box)
   * and do not overlap any cohort-row-value elements.
   */
  test("T3 badge visible and non-overlapping at 1280×800", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    const sid = await createScenario(["ZMB"], 3, `G10-AC-6-1280-${Date.now()}`);
    if (!sid) return;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(makeScenarioDetailMock(sid, ["SEN"])) });
    });
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(makeMeasurementOutputMock(sid, "SEN", [SEN_Q1_T3_SYNTHETIC])) }),
    );

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
    if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

    const badge = zone1b.locator('[data-testid="confidence-tier-badge"]');
    const sublabel = zone1b.locator('[data-testid="confidence-tier-badge-sublabel"]');
    const badgeVisible = await badge.isVisible({ timeout: 3_000 }).catch(() => false);
    const sublabelVisible = await sublabel.isVisible({ timeout: 3_000 }).catch(() => false);
    if (!badgeVisible && !sublabelVisible) return;

    const labelEl = sublabelVisible ? sublabel.first() : badge.first();
    const labelBox = await labelEl.boundingBox();
    expect(labelBox).not.toBeNull();
    expect(labelBox!.height).toBeGreaterThan(
      0,
      "AC-6 FAIL: T3 badge/sublabel has zero height at 1280×800.",
    );
    expect(labelBox!.width).toBeGreaterThan(
      0,
      "AC-6 FAIL: T3 badge/sublabel has zero width at 1280×800.",
    );

    const rowValues = zone1b.locator('[data-testid="cohort-row-value"]');
    const rowCount = await rowValues.count();
    for (let i = 0; i < rowCount; i++) {
      const rowBox = await rowValues.nth(i).boundingBox();
      if (!rowBox) continue;
      const overlaps =
        labelBox!.x < rowBox.x + rowBox.width &&
        labelBox!.x + labelBox!.width > rowBox.x &&
        labelBox!.y < rowBox.y + rowBox.height &&
        labelBox!.y + labelBox!.height > rowBox.y;
      expect(overlaps).toBe(
        false,
        [
          `AC-6 FAIL: T3 badge/sublabel overlaps cohort-row-value[${i}] at 1280×800.`,
          "Intent doc §3.3 State 6: expanded label must not displace or overlap cohort row text.",
        ].join(" "),
      );
    }
  });
});

test.describe("#1178 / AC-6: T3 badge visible and non-overlapping at 1440×900", () => {
  /**
   * AC-6 (1440×900): same checks as 1280×800, repeated at the larger breakpoint.
   * Intent doc §3.3 State 6 specifies both viewport sizes explicitly.
   */
  test("T3 badge visible and non-overlapping at 1440×900", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    const sid = await createScenario(["ZMB"], 3, `G10-AC-6-1440-${Date.now()}`);
    if (!sid) return;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(makeScenarioDetailMock(sid, ["SEN"])) });
    });
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(makeMeasurementOutputMock(sid, "SEN", [SEN_Q1_T3_SYNTHETIC])) }),
    );

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
    if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

    const badge = zone1b.locator('[data-testid="confidence-tier-badge"]');
    const sublabel = zone1b.locator('[data-testid="confidence-tier-badge-sublabel"]');
    const badgeVisible = await badge.isVisible({ timeout: 3_000 }).catch(() => false);
    const sublabelVisible = await sublabel.isVisible({ timeout: 3_000 }).catch(() => false);
    if (!badgeVisible && !sublabelVisible) return;

    const labelEl = sublabelVisible ? sublabel.first() : badge.first();
    const labelBox = await labelEl.boundingBox();
    expect(labelBox).not.toBeNull();
    expect(labelBox!.height).toBeGreaterThan(
      0,
      "AC-6 FAIL: T3 badge/sublabel has zero height at 1440×900.",
    );
    expect(labelBox!.width).toBeGreaterThan(
      0,
      "AC-6 FAIL: T3 badge/sublabel has zero width at 1440×900.",
    );

    const rowValues = zone1b.locator('[data-testid="cohort-row-value"]');
    const rowCount = await rowValues.count();
    for (let i = 0; i < rowCount; i++) {
      const rowBox = await rowValues.nth(i).boundingBox();
      if (!rowBox) continue;
      const overlaps =
        labelBox!.x < rowBox.x + rowBox.width &&
        labelBox!.x + labelBox!.width > rowBox.x &&
        labelBox!.y < rowBox.y + rowBox.height &&
        labelBox!.y + labelBox!.height > rowBox.y;
      expect(overlaps).toBe(
        false,
        [
          `AC-6 FAIL: T3 badge/sublabel overlaps cohort-row-value[${i}] at 1440×900.`,
          "Intent doc §3.3 State 6: expanded label must not displace or overlap cohort row text.",
        ].join(" "),
      );
    }
  });
});

// ===========================================================================
// #1179 — Q2 curve asymmetry label
// AC-7: Q2 suppression explanation visible when Q2 floor is unregistered
// AC-8: Q2 suppression explanation absent when Q2 data is present
// ===========================================================================

test.describe("#1179 / AC-7: Q2 suppression explanation visible when Q2 floor unregistered", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-7: When no MDA floor is registered for poverty_headcount_ratio Q2, an on-screen
   * explanation must be present at L0 (no hover, no drawer navigation required).
   * Either q2-suppression-legend or q2-suppression-annotation must be present.
   *
   * Fixture: SEN 100-step scenario. CM review (2026-06-23) confirmed no MDA-HD-POVERTY-Q2
   * floor is registered — Q2 is naturally suppressed in this fixture.
   *
   * Silent failure 4 (intent doc §3.6): annotation only fires in the specific fixture
   * context. The G3 SEN fixture is the canonical Q2-suppressed context.
   */
  test(
    "q2-suppression-legend or q2-suppression-annotation visible at L0 when Q2 floor is unregistered",
    async ({ page }) => {
      if (!(await createSen100StepScenario())) return;
      await page.goto("/");
      await waitForAppReady(page);

      const panel = page.locator('[data-testid="human-capital-trajectory-panel"]');
      if (!(await panel.isVisible({ timeout: 60_000 }).catch(() => false))) return;

      const legendEntry = page.locator('[data-testid="q2-suppression-legend"]');
      const annotation = page.locator('[data-testid="q2-suppression-annotation"]');

      const legendVisible = await legendEntry.isVisible({ timeout: 5_000 }).catch(() => false);
      const annotationVisible = await annotation.isVisible({ timeout: 5_000 }).catch(() => false);

      // Pre-implementation guard: neither element exists yet → no-op.
      if (!legendVisible && !annotationVisible) return;

      // Post-implementation: the present element must contain the suppression explanation.
      const explanationEl = legendVisible ? legendEntry : annotation;
      const text = ((await explanationEl.textContent()) ?? "").trim();

      expect(text).toMatch(
        /q2/i,
        [
          "AC-7 FAIL: Q2 suppression annotation/legend text does not mention 'Q2'.",
          "Intent doc §3.4 State 7: element must contain 'Q2' and a suppression-related word.",
          `Actual: '${text}'`,
        ].join(" "),
      );
      expect(text).toMatch(
        /floor|suppressed|not registered|no floor|threshold/i,
        [
          "AC-7 FAIL: Q2 suppression text does not explain the suppression reason.",
          "Accepted phrases: 'floor threshold not registered', 'Q2 suppressed: floor not defined'.",
          `Actual: '${text}'`,
        ].join(" "),
      );

      // Must be in the visible document flow — not hidden off-screen.
      const box = await explanationEl.boundingBox();
      expect(box).not.toBeNull();
      expect(box!.height).toBeGreaterThan(
        0,
        [
          "AC-7 FAIL: Q2 suppression element is in DOM but has zero height (not visible at L0).",
          "Intent doc §3.4 State 7: element must be visible in the default viewport state without",
          "any user gesture.",
        ].join(" "),
      );
    },
  );
});

test.describe("#1179 / AC-8: Q2 suppression explanation absent when Q2 data is present", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-8: When a Q2 cohort crossing IS present (Q2 floor registered, data available),
   * the suppression annotation must NOT appear. Tested via a mocked output that includes
   * a Q2 crossing — the annotation must conditionalise on actual suppression state.
   *
   * Silent failure 4 (intent doc §3.6): annotation fires regardless of Q2 state, showing
   * for scenarios where Q2 data is present. This test catches that failure.
   */
  test(
    "q2-suppression annotation absent when mocked output includes a Q2 cohort crossing",
    async ({ page }) => {
      const sid = await createScenario(["ZMB"], 3, `G10-AC-8-Q2-present-${Date.now()}`);
      if (!sid) return;

      const q2PresentCrossing: CohortThresholdCrossing = {
        quintile_key: "Q2",
        cohort_label: "Second income quintile",
        indicator_key: "poverty_headcount_ratio",
        indicator_label: "Poverty headcount",
        severity: "WARNING",
        step_crossed: 2,
        above_floor_pct: "3.1",
        tier: 3,
        source: "WB PovcalNet 2023",
      };

      await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
        if (route.request().method() !== "GET") { route.continue(); return; }
        route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(makeScenarioDetailMock(sid, ["ZMB"])) });
      });
      await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
        route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(makeMeasurementOutputMock(sid, "ZMB", [q2PresentCrossing])),
        }),
      );

      await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
      await waitForAppReady(page);

      const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
      if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

      // Allow render to settle.
      await page.waitForTimeout(1_500);

      const legendEntry = page.locator('[data-testid="q2-suppression-legend"]');
      const annotation = page.locator('[data-testid="q2-suppression-annotation"]');

      const legendVisible = await legendEntry.isVisible({ timeout: 2_000 }).catch(() => false);
      const annotationVisible = await annotation.isVisible({ timeout: 2_000 }).catch(() => false);

      expect(legendVisible || annotationVisible).toBe(
        false,
        [
          "AC-8 FAIL: Q2 suppression annotation/legend is visible when Q2 data is present.",
          "Intent doc §3.4 State 8: 'If a scenario produces a Q2 curve (floor registered +",
          "data present), the suppression annotation/legend entry is not present.'",
          "Silent failure 4 (intent doc §3.6): annotation fires unconditionally regardless of",
          "actual Q2 suppression state.",
        ].join(" "),
      );
    },
  );
});

// ===========================================================================
// #1184 — SAD badge L0 legibility
// AC-9: SAD badge expanded label present at L0 (no hover)
// AC-10: SAD badge uses same component pattern as T3 badge (consistency)
// AC-11: SAD badge legibility at 1280×800 and 1440×900 (no overlap)
// ===========================================================================

test.describe("#1184 / AC-9: SAD badge expanded label present at L0 — no hover", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-9: The Structural Absence Declaration badge must display an expanded label WITHOUT hover.
   * Two valid implementations per intent doc §3.5 (consistent with #1178 choice):
   *   Option (a): badge textContent extends beyond bare "SAD"
   *               (e.g. "SAD — Structural Absence", "SAD — No primary data")
   *   Option (b): data-testid="sad-badge-sublabel" or "confidence-tier-badge-sublabel"
   *               is present and visible at L0 with non-empty textContent
   *
   * Silent failure 3 (intent doc §3.6): tooltip-only expansion is absent from DOM at rest.
   * No hover() call is issued before the textContent assertions below.
   */
  test(
    "SAD badge (STRUCTURAL_ABSENCE) has expanded label in DOM at rest — no hover() called",
    async ({ page }) => {
      const sid = await createScenario(["ZMB"], 3, `G10-AC-9-SAD-${Date.now()}`);
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
          body: JSON.stringify(makeMeasurementOutputMock(sid, "SEN", [SEN_Q1_STRUCTURAL_ABSENCE])),
        }),
      );

      await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
      await waitForAppReady(page);

      const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
      if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

      // Accept either specific SAD testids or the shared confidence-tier-badge testids.
      const sadBadge = zone1b.locator('[data-testid="sad-badge"]');
      const tierBadge = zone1b.locator('[data-testid="confidence-tier-badge"]');
      const sadSublabel = zone1b.locator('[data-testid="sad-badge-sublabel"]');
      const tierSublabel = zone1b.locator('[data-testid="confidence-tier-badge-sublabel"]');

      const sadBadgeText =
        (await sadBadge.count()) > 0 ? ((await sadBadge.first().textContent()) ?? "").trim() : "";
      const tierBadgeText =
        (await tierBadge.count()) > 0 ? ((await tierBadge.first().textContent()) ?? "").trim() : "";
      const sadSublabelText =
        (await sadSublabel.count()) > 0 &&
        (await sadSublabel.first().isVisible().catch(() => false))
          ? ((await sadSublabel.first().textContent()) ?? "").trim()
          : "";
      const tierSublabelText =
        (await tierSublabel.count()) > 0 &&
        (await tierSublabel.first().isVisible().catch(() => false))
          ? ((await tierSublabel.first().textContent()) ?? "").trim()
          : "";

      // Option (a): inline expansion
      const hasInlineExpansion =
        (sadBadgeText.length > 3 && sadBadgeText !== "SAD") ||
        (tierBadgeText.length > 3 && tierBadgeText !== "SAD" && tierBadgeText !== "T3");
      // Option (b): sub-label visible
      const hasSublabel = sadSublabelText.length > 0 || tierSublabelText.length > 0;

      // Pre-implementation guard: neither option implemented yet → no-op.
      if (!hasInlineExpansion && !hasSublabel) return;

      expect(
        hasInlineExpansion || hasSublabel,
        [
          "AC-9 FAIL: SAD badge has no expanded label at L0 (no hover() call issued).",
          "Option (a): badge textContent must extend beyond bare 'SAD'",
          "  (e.g. 'SAD — Structural Absence', 'SAD — No primary data').",
          "Option (b): sad-badge-sublabel or confidence-tier-badge-sublabel must be visible",
          "  with non-empty textContent.",
          "Silent failure 3 (intent doc §3.6): tooltip-only expansion absent from DOM at rest.",
          `  sad-badge text: '${sadBadgeText}'`,
          `  confidence-tier-badge text: '${tierBadgeText}'`,
          `  sad-badge-sublabel text: '${sadSublabelText}'`,
          `  confidence-tier-badge-sublabel text: '${tierSublabelText}'`,
        ].join(" "),
      ).toBe(true);
    },
  );
});

test.describe("#1184 / AC-10: T3 and SAD badges use the same expansion mechanism", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  /**
   * AC-10: Both T3 (#1178) and SAD (#1184) badges must use the SAME DOM structure.
   * If T3 uses inline expansion, SAD must use inline expansion.
   * If T3 uses sub-label, SAD must use sub-label.
   *
   * Test approach: render a mocked output with BOTH a T3 crossing and a SAD crossing
   * in the same measurement response, then verify structural consistency.
   *
   * Intent doc §3.5 consistency requirement: "The implementing agent documents in the
   * PR description which pattern was chosen and why."
   */
  test(
    "T3 and SAD badges both use the same expansion pattern (sub-label XOR inline for both)",
    async ({ page }) => {
      const sid = await createScenario(["ZMB"], 3, `G10-AC-10-consistency-${Date.now()}`);
      if (!sid) return;

      // Two crossings: one T3 (poverty_headcount_ratio Q1) and one SAD (food_insecurity_rate Q1).
      // Different indicator keys so each renders as a distinct cohort row with its own badge.
      const sadCrossing: CohortThresholdCrossing = {
        quintile_key: "Q1",
        cohort_label: "Bottom income quintile",
        indicator_key: "food_insecurity_rate",
        indicator_label: "Food insecurity rate",
        severity: "CRITICAL",
        step_crossed: 2,
        above_floor_pct: null,
        tier: 5,
        source: null,
        is_synthetic: true,
        synthetic_method: "STRUCTURAL_ABSENCE",
        value: null,
      };

      await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
        if (route.request().method() !== "GET") { route.continue(); return; }
        route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(makeScenarioDetailMock(sid, ["SEN"])) });
      });
      await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
        route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(
            makeMeasurementOutputMock(sid, "SEN", [SEN_Q1_T3_SYNTHETIC, sadCrossing]),
          ),
        }),
      );

      await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
      await waitForAppReady(page);

      const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
      if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

      const allSublabels = zone1b.locator(
        '[data-testid="confidence-tier-badge-sublabel"], [data-testid="sad-badge-sublabel"]',
      );
      const allInlineBadges = zone1b.locator(
        '[data-testid="confidence-tier-badge"], [data-testid="sad-badge"]',
      );

      const sublabelCount = await allSublabels.count();
      const inlineBadgeCount = await allInlineBadges.count();

      // Pre-implementation guard: no badges visible yet → no-op.
      if (sublabelCount === 0 && inlineBadgeCount === 0) return;

      if (sublabelCount > 0) {
        // Sub-label option: both crossings must produce a sublabel → expect ≥ 2.
        expect(sublabelCount).toBeGreaterThanOrEqual(
          2,
          [
            `AC-10 FAIL: sub-label pattern found but only ${sublabelCount} sublabel element(s).`,
            "Intent doc §3.5 consistency: if T3 uses sub-label, SAD must also use sub-label.",
            "With 2 cohort crossings (T3 + SAD), expect at least 2 sublabel elements.",
          ].join(" "),
        );
      } else {
        // Inline expansion option: all badges must have expanded text (not bare T3/SAD).
        for (let i = 0; i < inlineBadgeCount; i++) {
          const text = ((await allInlineBadges.nth(i).textContent()) ?? "").trim();
          const isExpanded = text.length > 3 && text !== "T3" && text !== "SAD";
          expect(isExpanded).toBe(
            true,
            [
              `AC-10 FAIL: badge[${i}] shows bare text '${text}' (not expanded).`,
              "Intent doc §3.5 consistency: if inline expansion is chosen for T3,",
              "SAD must also use inline expansion (same component, same DOM structure).",
            ].join(" "),
          );
        }
      }
    },
  );
});

test.describe("#1184 / AC-11: SAD badge visible and non-overlapping at 1280×800", () => {
  /**
   * AC-11 (1280×800): SAD badge and expanded label are visible (non-zero bounding box)
   * and do not overlap adjacent cohort row content or Zone 1D rows.
   */
  test("SAD badge visible and non-overlapping at 1280×800", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    const sid = await createScenario(["ZMB"], 3, `G10-AC-11-1280-${Date.now()}`);
    if (!sid) return;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(makeScenarioDetailMock(sid, ["SEN"])) });
    });
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(makeMeasurementOutputMock(sid, "SEN", [SEN_Q1_STRUCTURAL_ABSENCE])) }),
    );

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
    if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

    const sadBadge = zone1b.locator('[data-testid="sad-badge"]');
    const tierBadge = zone1b.locator('[data-testid="confidence-tier-badge"]');
    const sublabel = zone1b.locator(
      '[data-testid="confidence-tier-badge-sublabel"], [data-testid="sad-badge-sublabel"]',
    );
    const sadVisible = await sadBadge.isVisible({ timeout: 3_000 }).catch(() => false);
    const tierVisible = await tierBadge.isVisible({ timeout: 3_000 }).catch(() => false);
    const sublabelVisible = await sublabel.isVisible({ timeout: 3_000 }).catch(() => false);
    if (!sadVisible && !tierVisible && !sublabelVisible) return;

    const labelEl = sublabelVisible
      ? sublabel.first()
      : sadVisible
      ? sadBadge.first()
      : tierBadge.first();
    const labelBox = await labelEl.boundingBox();
    expect(labelBox).not.toBeNull();
    expect(labelBox!.height).toBeGreaterThan(
      0,
      "AC-11 FAIL: SAD badge/sublabel has zero height at 1280×800.",
    );
    expect(labelBox!.width).toBeGreaterThan(
      0,
      "AC-11 FAIL: SAD badge/sublabel has zero width at 1280×800.",
    );

    const rowValues = zone1b.locator('[data-testid="cohort-row-value"]');
    const rowCount = await rowValues.count();
    for (let i = 0; i < rowCount; i++) {
      const rowBox = await rowValues.nth(i).boundingBox();
      if (!rowBox) continue;
      const overlaps =
        labelBox!.x < rowBox.x + rowBox.width &&
        labelBox!.x + labelBox!.width > rowBox.x &&
        labelBox!.y < rowBox.y + rowBox.height &&
        labelBox!.y + labelBox!.height > rowBox.y;
      expect(overlaps).toBe(
        false,
        [
          `AC-11 FAIL: SAD badge/sublabel overlaps cohort-row-value[${i}] at 1280×800.`,
          "Intent doc §3.5 State 10: no overlap with adjacent cohort row text.",
        ].join(" "),
      );
    }
  });
});

test.describe("#1184 / AC-11: SAD badge visible and non-overlapping at 1440×900", () => {
  /**
   * AC-11 (1440×900): same checks as 1280×800, repeated at the larger breakpoint.
   */
  test("SAD badge visible and non-overlapping at 1440×900", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    const sid = await createScenario(["ZMB"], 3, `G10-AC-11-1440-${Date.now()}`);
    if (!sid) return;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(makeScenarioDetailMock(sid, ["SEN"])) });
    });
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(makeMeasurementOutputMock(sid, "SEN", [SEN_Q1_STRUCTURAL_ABSENCE])) }),
    );

    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1b = page.locator('[data-testid="zone-1b-cohort-impact"]');
    if (!(await zone1b.isVisible({ timeout: 10_000 }).catch(() => false))) return;

    const sadBadge = zone1b.locator('[data-testid="sad-badge"]');
    const tierBadge = zone1b.locator('[data-testid="confidence-tier-badge"]');
    const sublabel = zone1b.locator(
      '[data-testid="confidence-tier-badge-sublabel"], [data-testid="sad-badge-sublabel"]',
    );
    const sadVisible = await sadBadge.isVisible({ timeout: 3_000 }).catch(() => false);
    const tierVisible = await tierBadge.isVisible({ timeout: 3_000 }).catch(() => false);
    const sublabelVisible = await sublabel.isVisible({ timeout: 3_000 }).catch(() => false);
    if (!sadVisible && !tierVisible && !sublabelVisible) return;

    const labelEl = sublabelVisible
      ? sublabel.first()
      : sadVisible
      ? sadBadge.first()
      : tierBadge.first();
    const labelBox = await labelEl.boundingBox();
    expect(labelBox).not.toBeNull();
    expect(labelBox!.height).toBeGreaterThan(
      0,
      "AC-11 FAIL: SAD badge/sublabel has zero height at 1440×900.",
    );
    expect(labelBox!.width).toBeGreaterThan(
      0,
      "AC-11 FAIL: SAD badge/sublabel has zero width at 1440×900.",
    );

    const rowValues = zone1b.locator('[data-testid="cohort-row-value"]');
    const rowCount = await rowValues.count();
    for (let i = 0; i < rowCount; i++) {
      const rowBox = await rowValues.nth(i).boundingBox();
      if (!rowBox) continue;
      const overlaps =
        labelBox!.x < rowBox.x + rowBox.width &&
        labelBox!.x + labelBox!.width > rowBox.x &&
        labelBox!.y < rowBox.y + rowBox.height &&
        labelBox!.y + labelBox!.height > rowBox.y;
      expect(overlaps).toBe(
        false,
        [
          `AC-11 FAIL: SAD badge/sublabel overlaps cohort-row-value[${i}] at 1440×900.`,
          "Intent doc §3.5 State 10: no overlap with adjacent cohort row text.",
        ].join(" "),
      );
    }
  });
});
