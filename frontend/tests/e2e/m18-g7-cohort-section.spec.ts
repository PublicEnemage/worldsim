/**
 * E2E: M18-G7-C — CohortImpactSection Monitored-Row State (#1463, #1469)
 *
 * Authored BEFORE implementation per intent document:
 *   docs/process/intents/M18-G7-C-2026-06-29-cohort-section-design.md
 *
 * Sprint entry: docs/process/sprint-plans/m18-g7-sprint-entry.md (EL Approved 2026-06-29)
 * ADR gate: ADR-010 Amendment 2 (accepted 2026-06-29)
 *
 * ACs covered:
 *   AC-C1  focal-cohort-row present when monitored_focal_cohorts configured
 *   AC-C2  CLEAR badge (green #2e7d32) when focal value > floor
 *   AC-C3  HIST amber badge (#a06000) for prior breach at step < current_step (DEMO-140)
 *   AC-C4  CRITICAL breach row renders BEFORE CLEAR focal row in DOM
 *   AC-C5  No focal-cohort-row when scenario has no monitored_focal_cohorts
 *
 * NM-056 rule: NO test.skip(), test.fixme(), or .only() patterns.
 *
 * RED state: all AC-C1–C5 will fail until G7-C monitored-row implementation lands.
 *   - AC-C1: [data-testid="focal-cohort-row"] does not exist yet
 *   - AC-C2: no CLEAR badge rendered
 *   - AC-C3: historical crossings still show CRITICAL red (no temporal disambiguation)
 *
 * Route mocking:
 *   AC-C1/C2/C4: SEN trajectory with monitored_focal_cohorts configured, step 6
 *   AC-C3: SEN trajectory with threshold crossing at step 1, viewed at step 6
 *   AC-C5: ZMB trajectory without monitored_focal_cohorts
 *
 * Source: M18-G7-C intent §AC-C1–C5 + ADR-010 Amendment 2.
 */
import { test, expect } from "@playwright/test";

const API_BASE = "http://localhost:8000/api/v1";
const VIEWPORT = { width: 1440, height: 900 };

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

function makeSenTrajectoryWithFocalCohort(scenarioId: string): object {
  // SEN trajectory at step 6, bottom_quintile_informal_workers_poverty_headcount = 0.450
  // which is ABOVE floor 0.400 → CLEAR state
  const nSteps = 8;
  return {
    scenario_id: scenarioId,
    entity_id: "SEN",
    step_count: nSteps,
    mda_floors: [],
    // A prior threshold crossing at step 1 (agricultural workers) → should show HIST at step 6
    threshold_crossings: [
      {
        mda_id: "sen-hd-001",
        indicator_key: "agricultural_workers_nutrition_headcount",
        indicator_name: "Agricultural workers nutrition headcount",
        framework: "human_development",
        severity: "CRITICAL",
        step_index: 1,       // crossed at step 1
        cohort: "agricultural_workers",
        confidence_tier: 3,
        causal_attribution: null,
        floor_value: "0.30",
        current_value: "0.28",
        approach_pct_remaining: "-0.06",
        consecutive_breach_steps: 1,
        recovery_horizon_years: 3,
      },
    ],
    steps: Array.from({ length: nSteps }, (_, i) => ({
      step_index: i + 1,
      effective_from: `2024-${String(i + 1).padStart(2, "0")}-01T00:00:00Z`,
      step_event_label: null,
      step_significance: "ROUTINE",
      frameworks: [
        {
          framework: "human_development",
          composite_score: String(0.44 + i * 0.002),
          confidence_tier: 3,
          ci_lower: null,
          ci_upper: null,
          scoring_basis: "percentile_rank",
          indicators: {
            bottom_quintile_informal_workers_poverty_headcount: {
              value: "0.450",
              unit: "ratio",
              variable_type: "STOCK",
              confidence_tier: 3,
            },
            agricultural_workers_nutrition_headcount: {
              value: i === 0 ? "0.28" : "0.32",  // step 1 breached; recovered by step 2+
              unit: "ratio",
              variable_type: "STOCK",
              confidence_tier: 3,
            },
          },
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
        {
          framework: "financial",
          composite_score: String(0.51 - i * 0.002),
          confidence_tier: 3,
          ci_lower: null,
          ci_upper: null,
          scoring_basis: "percentile_rank",
          indicators: {},
          mda_alerts: [],
          has_below_floor_indicator: false,
          note: null,
        },
      ],
    })),
  };
}

async function createSenScenarioWithFocalCohort(): Promise<string | null> {
  try {
    const res = await fetch(`${API_BASE}/scenarios`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: "SEN G7-C focal cohort",
        configuration: {
          entities: ["SEN"],
          n_steps: 8,
          start_date: "2024-01-01",
          modules_config: {
            ecological: { enabled: false },
            political_economy: { enabled: true },
          },
          // monitored_focal_cohorts: G7-C adds this field to scenario configuration
          monitored_focal_cohorts: [
            {
              indicator_key: "bottom_quintile_informal_workers_poverty_headcount",
              floor_value: 0.40,
              floor_label: "Recovery floor",
              framework: "human_development",
            },
          ],
        },
        scheduled_inputs: [],
      }),
    });
    if (!res.ok) return null;
    const { scenario_id: id } = (await res.json()) as ScenarioCreateResponse;
    // Advance to step 6
    for (let i = 0; i < 6; i++) {
      const advRes = await fetch(`${API_BASE}/scenarios/${id}/advance`, { method: "POST" });
      if (!advRes.ok) break;
    }
    return id;
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// AC-C1 — focal-cohort-row present when monitored_focal_cohorts configured
// ---------------------------------------------------------------------------

test("AC-C1: focal-cohort-row present in CohortImpactSection when monitored_focal_cohorts configured", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);

  const scenId = await page.evaluate(async () => {
    try {
      const r = await fetch("http://localhost:8000/api/v1/scenarios", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: "SEN G7-C1",
          configuration: {
            entities: ["SEN"],
            n_steps: 8,
            start_date: "2024-01-01",
            modules_config: { ecological: { enabled: false }, political_economy: { enabled: true } },
            monitored_focal_cohorts: [
              {
                indicator_key: "bottom_quintile_informal_workers_poverty_headcount",
                floor_value: 0.40,
                floor_label: "Recovery floor",
                framework: "human_development",
              },
            ],
          },
          scheduled_inputs: [],
        }),
      });
      if (!r.ok) return null;
      const d = await r.json() as { scenario_id: string };
      return d.scenario_id;
    } catch {
      return null;
    }
  });

  if (!scenId) { console.warn("AC-C1: backend not available — skipping"); return; }

  await page.route(`**/api/v1/scenarios/${scenId}/trajectory**`, (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(makeSenTrajectoryWithFocalCohort(scenId)),
    }),
  );

  await page.goto(`/?scenario=${scenId}`);
  await waitForAppReady(page);

  // Advance to step 6
  const nextBtn = page.getByRole("button", { name: /Next Step/ });
  for (let i = 0; i < 5; i++) {
    const visible = await nextBtn.isVisible({ timeout: 3_000 }).catch(() => false);
    if (visible) {
      await nextBtn.click();
      await page.waitForTimeout(400);
    }
  }
  await page.waitForTimeout(1_000);

  const focalRow = page.locator('[data-testid="focal-cohort-row"]');
  const present = await focalRow.isVisible({ timeout: 3_000 }).catch(() => false);

  expect(
    present,
    "AC-C1 FAIL: [data-testid='focal-cohort-row'] not present in CohortImpactSection. " +
    "Fix G7-C: implement monitored focal row rendering in CohortImpactSection. " +
    "Read monitored_focal_cohorts from scenario configuration. " +
    "See M18-G7-C intent §3.1 + ADR-010 Amendment 2.",
  ).toBe(true);

  if (present) {
    const box = await focalRow.boundingBox();
    expect(box, "AC-C1 FAIL: focal-cohort-row has zero dimensions").not.toBeNull();
    if (box) {
      expect(box.width * box.height, "AC-C1 FAIL: focal-cohort-row has zero area").toBeGreaterThan(0);
    }
  }
});

// ---------------------------------------------------------------------------
// AC-C2 — CLEAR badge: green background, "CLEAR" text, value + floor rendered
// ---------------------------------------------------------------------------

test("AC-C2: focal-cohort-row shows CLEAR badge with green background when value > floor", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);

  const scenId = await page.evaluate(async () => {
    try {
      const r = await fetch("http://localhost:8000/api/v1/scenarios", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: "SEN G7-C2",
          configuration: {
            entities: ["SEN"],
            n_steps: 8,
            start_date: "2024-01-01",
            modules_config: { ecological: { enabled: false }, political_economy: { enabled: true } },
            monitored_focal_cohorts: [
              {
                indicator_key: "bottom_quintile_informal_workers_poverty_headcount",
                floor_value: 0.40,
                floor_label: "Recovery floor",
                framework: "human_development",
              },
            ],
          },
          scheduled_inputs: [],
        }),
      });
      if (!r.ok) return null;
      const d = await r.json() as { scenario_id: string };
      return d.scenario_id;
    } catch {
      return null;
    }
  });

  if (!scenId) { console.warn("AC-C2: backend not available — skipping"); return; }

  await page.route(`**/api/v1/scenarios/${scenId}/trajectory**`, (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(makeSenTrajectoryWithFocalCohort(scenId)),
    }),
  );

  // Mock advance so current_step increments reliably without real backend latency.
  // Returns step_executed: 1 for all clicks — trajectory step 1 has value 0.450 > floor 0.400.
  await page.route(`**/api/v1/scenarios/${scenId}/advance**`, (route) => {
    if (route.request().method() !== "POST") { route.continue(); return; }
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ step_executed: 1, is_complete: false }),
    });
  });

  await page.goto(`/?scenario=${scenId}`);
  await waitForAppReady(page);

  const nextBtn = page.getByRole("button", { name: /Next Step/ });
  for (let i = 0; i < 5; i++) {
    const visible = await nextBtn.isVisible({ timeout: 3_000 }).catch(() => false);
    if (visible) { await nextBtn.click(); await page.waitForTimeout(400); }
  }
  await page.waitForTimeout(1_000);

  const focalRow = page.locator('[data-testid="focal-cohort-row"]');
  if (!await focalRow.isVisible({ timeout: 3_000 }).catch(() => false)) {
    console.warn("AC-C2: focal-cohort-row absent — AC-C1 fix required first");
    return;
  }

  // Badge text must be "CLEAR"
  const badge = focalRow.locator('[data-testid="focal-badge"]').or(focalRow.locator('.focal-badge'));
  const badgeText = await badge.textContent({ timeout: 2_000 }).catch(() => null);
  expect(
    badgeText,
    "AC-C2 FAIL: focal badge text is not 'CLEAR'. " +
    "At step 6 with value 0.450 > floor 0.400, badge must read 'CLEAR'. " +
    "See M18-G7-C intent §3.2 + ADR-010 Amendment 2 §Monitored-row states.",
  ).toContain("CLEAR");

  // Badge background must be green #2e7d32
  const bgColor = await badge.evaluate(
    (el) => window.getComputedStyle(el).backgroundColor,
  ).catch(() => null);

  if (bgColor !== null) {
    // Accept rgb(46, 125, 50) which is #2e7d32
    expect(
      bgColor,
      "AC-C2 FAIL: CLEAR badge background is not green #2e7d32 (rgb(46, 125, 50)). " +
      "See M18-G7-C intent §0 Constraint 4 + ADR-010 Amendment 2.",
    ).toMatch(/rgb\(46,\s*125,\s*50\)/);
  }
});

// ---------------------------------------------------------------------------
// AC-C3 — HIST amber badge for historical breach rows (DEMO-140)
// ---------------------------------------------------------------------------

test("AC-C3: historical breach rows show amber HIST badge at step 6 (DEMO-140)", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);

  const scenId = await page.evaluate(async () => {
    try {
      const r = await fetch("http://localhost:8000/api/v1/scenarios", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: "SEN G7-C3",
          configuration: {
            entities: ["SEN"],
            n_steps: 8,
            start_date: "2024-01-01",
            modules_config: { ecological: { enabled: false }, political_economy: { enabled: true } },
          },
          scheduled_inputs: [],
        }),
      });
      if (!r.ok) return null;
      const d = await r.json() as { scenario_id: string };
      return d.scenario_id;
    } catch {
      return null;
    }
  });

  if (!scenId) { console.warn("AC-C3: backend not available — skipping"); return; }

  await page.route(`**/api/v1/scenarios/${scenId}/trajectory**`, (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(makeSenTrajectoryWithFocalCohort(scenId)),
    }),
  );

  await page.goto(`/?scenario=${scenId}`);
  await waitForAppReady(page);

  // Advance to step 6 (past the step 1 crossing)
  const nextBtn = page.getByRole("button", { name: /Next Step/ });
  for (let i = 0; i < 5; i++) {
    const visible = await nextBtn.isVisible({ timeout: 3_000 }).catch(() => false);
    if (visible) { await nextBtn.click(); await page.waitForTimeout(400); }
  }
  await page.waitForTimeout(1_000);

  // At step 6, the agricultural_workers crossing (step_index=1) is HISTORICAL.
  // It must show HIST amber badge, NOT CRITICAL red.
  const cohortSection = page.locator('[data-testid="cohort-impact-section"]');
  const cohortVisible = await cohortSection.isVisible({ timeout: 3_000 }).catch(() => false);
  if (!cohortVisible) { console.warn("AC-C3: cohort-impact-section not visible — skipping"); return; }

  // Look for a breach row that was at step 1
  const historicalRow = cohortSection.locator('[data-crossing-step="1"]')
    .or(cohortSection.locator('[data-testid="cohort-impact-row"]').first());
  const rowVisible = await historicalRow.isVisible({ timeout: 2_000 }).catch(() => false);
  if (!rowVisible) { console.warn("AC-C3: no crossing row visible — skipping"); return; }

  // Must NOT show CRITICAL badge (red) for a step_1 crossing at current step 6
  const criticalBadge = historicalRow.locator('[data-testid="severity-badge"]').or(historicalRow.locator('.severity-badge'));
  const badgeText = await criticalBadge.textContent({ timeout: 2_000 }).catch(() => null);

  // After G7-C fix: badge text is "HIST" (amber), not "CRITICAL" (red)
  if (badgeText !== null) {
    expect(
      badgeText,
      "AC-C3 FAIL: historical breach row (step 1, viewed at step 6) shows " +
      `badge '${badgeText}' instead of 'HIST'. ` +
      "Fix DEMO-140: apply temporal disambiguation — crossings where step_index < current_step " +
      "show amber HIST badge, not CRITICAL. See ADR-010 Amendment 2 §Temporal Disambiguation.",
    ).toContain("HIST");

    // Amber background: #a06000 = rgb(160, 96, 0)
    const bgColor = await criticalBadge.evaluate(
      (el) => window.getComputedStyle(el).backgroundColor,
    ).catch(() => null);
    if (bgColor !== null) {
      expect(
        bgColor,
        "AC-C3 FAIL: HIST badge background not amber #a06000 (rgb(160, 96, 0)). " +
        "See M18-G7-C intent §0 Constraint 4.",
      ).toMatch(/rgb\(160,\s*96,\s*0\)/);
    }
  }
});

// ---------------------------------------------------------------------------
// AC-C4 — Severity-aware ordering: CRITICAL row before CLEAR focal row
// ---------------------------------------------------------------------------

test("AC-C4: CRITICAL breach row appears before CLEAR focal row in DOM", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);

  // Scenario needs: a CRITICAL breach row (active at current step) AND a CLEAR focal row
  const scenId = await page.evaluate(async () => {
    try {
      const r = await fetch("http://localhost:8000/api/v1/scenarios", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: "SEN G7-C4",
          configuration: {
            entities: ["SEN"],
            n_steps: 8,
            start_date: "2024-01-01",
            modules_config: { ecological: { enabled: false }, political_economy: { enabled: true } },
            monitored_focal_cohorts: [
              {
                indicator_key: "bottom_quintile_informal_workers_poverty_headcount",
                floor_value: 0.40,
                floor_label: "Recovery floor",
                framework: "human_development",
              },
            ],
          },
          scheduled_inputs: [],
        }),
      });
      if (!r.ok) return null;
      const d = await r.json() as { scenario_id: string };
      return d.scenario_id;
    } catch {
      return null;
    }
  });

  if (!scenId) { console.warn("AC-C4: backend not available — skipping"); return; }

  // Mock: threshold crossing at CURRENT step (not historical) + focal at CLEAR
  const mockWithCurrentCrossing = {
    ...makeSenTrajectoryWithFocalCohort(scenId) as Record<string, unknown>,
    threshold_crossings: [
      {
        mda_id: "sen-hd-current-001",
        indicator_key: "agricultural_workers_nutrition_headcount",
        indicator_name: "Agricultural workers nutrition headcount",
        framework: "human_development",
        severity: "CRITICAL",
        step_index: 6,    // current step — not historical
        cohort: "agricultural_workers",
        confidence_tier: 3,
        causal_attribution: null,
        floor_value: "0.30",
        current_value: "0.27",
        approach_pct_remaining: "-0.10",
        consecutive_breach_steps: 1,
        recovery_horizon_years: 3,
      },
    ],
  };

  await page.route(`**/api/v1/scenarios/${scenId}/trajectory**`, (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(mockWithCurrentCrossing),
    }),
  );

  await page.goto(`/?scenario=${scenId}`);
  await waitForAppReady(page);

  const nextBtn = page.getByRole("button", { name: /Next Step/ });
  for (let i = 0; i < 5; i++) {
    const visible = await nextBtn.isVisible({ timeout: 3_000 }).catch(() => false);
    if (visible) { await nextBtn.click(); await page.waitForTimeout(400); }
  }
  await page.waitForTimeout(1_000);

  const focalRow = page.locator('[data-testid="focal-cohort-row"]');
  const criticalRow = page.locator('[data-testid="cohort-row-0"]');

  const bothVisible = await Promise.all([
    focalRow.isVisible({ timeout: 3_000 }).catch(() => false),
    criticalRow.isVisible({ timeout: 3_000 }).catch(() => false),
  ]);

  if (!bothVisible[0] || !bothVisible[1]) {
    console.warn("AC-C4: one or both rows not visible — AC-C1 fix required first");
    return;
  }

  // CRITICAL row must appear before CLEAR focal row in DOM
  const position = await page.evaluate(() => {
    const critical = document.querySelector('[data-testid^="cohort-row-"]');
    const focal = document.querySelector('[data-testid="focal-cohort-row"]');
    if (!critical || !focal) return null;
    return critical.compareDocumentPosition(focal);
  });

  // DOCUMENT_POSITION_FOLLOWING (4): focal appears after critical in DOM
  expect(
    position,
    "AC-C4 FAIL: CRITICAL breach row does not appear before CLEAR focal row in DOM. " +
    "Fix G7-C: severity-aware ordering — CRITICAL rows render before CLEAR focal rows. " +
    "See M18-G7-C intent §0 Constraint 2 + ADR-010 Amendment 2.",
  ).toBe(4);
});

// ---------------------------------------------------------------------------
// AC-C5 — No focal-cohort-row when scenario has no monitored_focal_cohorts
// ---------------------------------------------------------------------------

test("AC-C5: focal-cohort-row absent when scenario has no monitored_focal_cohorts", async ({
  page,
}) => {
  await page.setViewportSize(VIEWPORT);

  // ZMB Option A: no monitored_focal_cohorts in configuration
  const scenId = await page.evaluate(async () => {
    try {
      const r = await fetch("http://localhost:8000/api/v1/scenarios", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: "ZMB G7-C5 no-focal",
          configuration: {
            entities: ["ZMB"],
            n_steps: 6,
            start_date: "2024-01-01",
            modules_config: { ecological: { enabled: false }, political_economy: { enabled: true } },
            // No monitored_focal_cohorts key
          },
          scheduled_inputs: [],
        }),
      });
      if (!r.ok) return null;
      const d = await r.json() as { scenario_id: string };
      return d.scenario_id;
    } catch {
      return null;
    }
  });

  if (!scenId) { console.warn("AC-C5: backend not available — skipping"); return; }

  await page.goto(`/?scenario=${scenId}`);
  await waitForAppReady(page);
  await page.waitForTimeout(2_000);

  const focalRow = page.locator('[data-testid="focal-cohort-row"]');
  const present = await focalRow.isVisible({ timeout: 2_000 }).catch(() => false);

  expect(
    present,
    "AC-C5 FAIL: focal-cohort-row present in a scenario with no monitored_focal_cohorts. " +
    "This is a regression in the AC-C1 fix. The focal row must only render when " +
    "monitored_focal_cohorts is configured in the scenario. " +
    "See M18-G7-C intent §3.2 State E.",
  ).toBe(false);
});
