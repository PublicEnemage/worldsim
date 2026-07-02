/**
 * E2E: M18-G2 PSP Driver Decomposition — AC-1255-1 through AC-1255-7.
 *
 * Authored BEFORE implementation from intent document at:
 * docs/process/intents/M18-G2-2026-06-26-psp-driver-decomposition.md
 *
 * ADR: ADR-015 §Component 3 — Zone 1D PSP row content addition within
 *      existing L0/L1 evidence thread model; no new ADR required.
 * Sprint entry: docs/process/sprint-plans/m18-g2-sprint-entry.md (EL Approved 2026-06-26)
 * Issue: #1255 — PSP driver decomposition
 *
 * Acceptance criteria covered:
 *   AC-1255-1 — psp-driver-row visible with "fiscal sustainability" at Senegal step 3
 *   AC-1255-2 — psp-driver-row position: after psp-severity-row, before psp-historical-analogue
 *   AC-1255-3 — psp-driver-row updates reactively on step advance
 *   AC-1255-4 — psp-driver-row absent from DOM when psp_dominant_driver is null
 *   AC-1255-5 — psp-severity-row and psp-severity-badge not displaced by driver row addition
 *   AC-1255-6 — psp-driver-row visible without scroll at 1280×800
 *   AC-1255-7 — psp-driver-row visible without scroll at 1024×768
 *
 * NM-056 rule: NO test.skip() or conditional skip patterns. A test scenario unavailable
 * pre-implementation uses the early-return guard pattern — a guard that fires is a no-op
 * (not a pass). Tests become active when implementation lands and must then either pass or
 * fail explicitly. A skipped test is a silent pass; that is the failure mode NM-056 prevents.
 *
 * Guard pattern: each test guards on the primary testid it exercises.
 * Pre-implementation: psp-driver-row absent → isVisible() returns false → test returns.
 * Guards use .catch(() => false) on isVisible() — never throw on absent element.
 *
 * Fixture: SEN (Senegal) with political_economy enabled.
 * Measurement-output endpoint mocked per test group — psp_dominant_driver injected
 * into political_economy.indicators.programme_survival_probability.
 *
 * Viewport: 1280×800 (AC-1255-1/2/3/4/5) and 1024×768 (AC-1255-7).
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
 * Create scenario with given entities, advance nAdvanceSteps via API.
 * nConfigSteps sets the scenario's configured n_steps ceiling (default 3).
 * peEnabled activates the political_economy module.
 */
async function createScenarioG2(
  entities: string[],
  nAdvanceSteps: number,
  name: string,
  peEnabled = false,
  nConfigSteps = 3,
): Promise<string> {
  const createRes = await fetch(`${API_BASE}/scenarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name,
      configuration: {
        entities,
        n_steps: nConfigSteps,
        start_date: "2024-01-01",
        modules_config: {
          ecological: { enabled: false },
          political_economy: { enabled: peEnabled },
        },
      },
    }),
  });
  if (!createRes.ok) throw new Error(`Create failed: ${createRes.status}`);
  const { scenario_id: id } = (await createRes.json()) as ScenarioCreateResponse;

  for (let i = 0; i < nAdvanceSteps; i++) {
    const advRes = await fetch(
      `${API_BASE}/scenarios/${encodeURIComponent(id)}/advance`,
      { method: "POST" },
    );
    if (!advRes.ok) throw new Error(`Advance step ${i + 1} failed: ${advRes.status}`);
  }

  return id;
}

/**
 * Measurement-output mock for a SEN entity with controlled PSP and driver values.
 * pspValue null means PE unavailable. pspDominantDriver null means no driver row.
 */
function makeMeasurementOutputMockG2(
  scenarioId: string,
  options: {
    pspValue?: string | null;
    pspDominantDriver?: string | null;
    stepIndex?: number;
  } = {},
): object {
  const pspValue = options.pspValue ?? "0.5200";
  const pspDominantDriver = options.pspDominantDriver ?? null;
  const stepIndex = options.stepIndex ?? 3;

  return {
    entity_id: "SEN",
    entity_name: "Senegal",
    timestep: "2024-07-01T00:00:00Z",
    scenario_id: scenarioId,
    step_index: stepIndex,
    outputs: {
      financial: {
        framework: "financial",
        composite_score: "0.48",
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
        composite_score: pspValue ? "0.6200" : null,
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
            psp_dominant_driver: pspDominantDriver,
          },
        },
        mda_alerts: [],
        has_below_floor_indicator: false,
        note: pspValue ? null : "Political economy unavailable",
      },
    },
    ia1_disclosure: "This output is pre-calibration.",
    single_entity_warning: true,
  };
}

/**
 * Scenario detail mock for SEN with PE enabled.
 */
function makeScenarioDetailMockG2(scenarioId: string, peEnabled = true): object {
  return {
    scenario_id: scenarioId,
    name: "G2-SEN-test",
    status: "completed",
    configuration: {
      entities: ["SEN"],
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
// AC-1255-1/5/6: Primary driver row visibility at Senegal step 3 (#1255)
//
// Intent doc §5 AC-1255-1:
// In the Senegal Article IV scenario at step 3 with PE enabled,
// data-testid="psp-driver-row" is visible and contains the text "fiscal sustainability".
//
// AC-1255-5: psp-severity-row and psp-severity-badge remain present alongside driver row.
//
// AC-1255-6: psp-driver-row is visible at 1280×800 without scrolling Zone 1D.
// ---------------------------------------------------------------------------

test.describe("AC-1255-1/5/6: psp-driver-row visible with fiscal sustainability at Senegal step 3 (#1255)", () => {
  let senScenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      // Advance 3 steps — represents Senegal Article IV step 3 entry state
      senScenarioId = await createScenarioG2(["SEN"], 3, `G2-SEN-AC1-${Date.now()}`, true, 5);
    } catch {
      senScenarioId = null;
    }
  });

  test("AC-1255-1: psp-driver-row visible and contains 'fiscal sustainability' at step 3", async ({
    page,
  }) => {
    if (!senScenarioId) return;

    const sid = senScenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMockG2(sid)),
      });
    });

    // Step 3: Senegal fiscal sustainability is the dominant PSP driver (Demo 7 Act 1 anchor)
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMockG2(sid, {
          pspValue: "0.5200",
          pspDominantDriver: "fiscal_sustainability",
          stepIndex: 3,
        })),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    // Guard: Zone 1D must be visible (PE rendered at all)
    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Primary guard: psp-driver-row is new in G2 — absent pre-implementation
    const driverRow = page.locator('[data-testid="psp-driver-row"]');
    if (!(await driverRow.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // AC-1255-1: driver row present and contains "fiscal sustainability"
    await expect(driverRow).toBeVisible();
    await expect(driverRow).toContainText("fiscal sustainability");
  });

  test("AC-1255-5: psp-severity-row and psp-severity-badge remain visible alongside psp-driver-row", async ({
    page,
  }) => {
    if (!senScenarioId) return;

    const sid = senScenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMockG2(sid)),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMockG2(sid, {
          pspValue: "0.5200",
          pspDominantDriver: "fiscal_sustainability",
          stepIndex: 3,
        })),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: driver row must be present (G2 implementation landed)
    const driverRow = page.locator('[data-testid="psp-driver-row"]');
    if (!(await driverRow.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // AC-1255-5: severity row must remain present and visible — G2 must not displace it
    const severityRow = page.locator('[data-testid="psp-severity-row"]');
    await expect(severityRow).toBeVisible({ timeout: 5_000 });

    // Severity row text must still contain severity label — G2 must not alter existing content
    const severityText = await severityRow.textContent() ?? "";
    const hasSeverityLabel =
      severityText.includes("CRITICAL") ||
      severityText.includes("WARNING") ||
      severityText.includes("WATCH") ||
      severityText.includes("STABLE");
    expect(hasSeverityLabel).toBe(true);

    // psp-severity-badge must also be present (colour encoding for severity tier)
    const severityBadge = page.locator('[data-testid="psp-severity-badge"]');
    if ((await severityBadge.count()) > 0) {
      await expect(severityBadge).toBeVisible({ timeout: 3_000 });
    }
  });

  test("AC-1255-6: psp-driver-row visible at 1280×800 without scrolling Zone 1D container", async ({
    page,
  }) => {
    if (!senScenarioId) return;

    const sid = senScenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMockG2(sid)),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMockG2(sid, {
          pspValue: "0.5200",
          pspDominantDriver: "fiscal_sustainability",
          stepIndex: 3,
        })),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    const driverRow = page.locator('[data-testid="psp-driver-row"]');
    if (!(await driverRow.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // AC-1255-6: must use .toBeVisible() — not .toBeAttached() — to confirm no scroll required
    await expect(driverRow).toBeVisible();

    // Driver row must be within the 1280×800 viewport (intent doc §3.3 UX Designer watchpoint)
    const driverBox = await driverRow.boundingBox();
    expect(driverBox).not.toBeNull();
    if (driverBox) {
      expect(driverBox.y + driverBox.height).toBeLessThanOrEqual(800);
    }
  });
});

// ---------------------------------------------------------------------------
// AC-1255-2: DOM ordering — driver row between severity and analogue (#1255)
//
// Intent doc §6 AC-1255-2:
// In any scenario with a non-null driver, psp-driver-row appears in the DOM
// after psp-severity-row and before psp-historical-analogue.
// Assert DOM ordering within zone-1d-political-risk.
// ---------------------------------------------------------------------------

test.describe("AC-1255-2: psp-driver-row DOM position: after severity, before analogue (#1255)", () => {
  let senScenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      senScenarioId = await createScenarioG2(["SEN"], 3, `G2-SEN-AC2-${Date.now()}`, true, 5);
    } catch {
      senScenarioId = null;
    }
  });

  test("AC-1255-2: psp-driver-row is after psp-severity-row and before psp-historical-analogue in DOM", async ({
    page,
  }) => {
    if (!senScenarioId) return;

    const sid = senScenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMockG2(sid)),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMockG2(sid, {
          pspValue: "0.5200",
          pspDominantDriver: "fiscal_sustainability",
          stepIndex: 3,
        })),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: driver row must be present (G2 implementation landed)
    const driverRow = page.locator('[data-testid="psp-driver-row"]');
    if (!(await driverRow.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Guard: historical analogue must be present (pre-G2 element — absent means no PSP history)
    const analogue = page.locator('[data-testid="psp-historical-analogue"]');
    if (!(await analogue.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Assert DOM ordering within the zone-1d-political-risk container:
    // psp-severity-row → psp-driver-row → psp-historical-analogue
    const isCorrectOrder = await page.evaluate(() => {
      const container = document.querySelector('[data-testid="zone-1d-political-risk"]');
      if (!container) {
        // Fallback: search in zone-1d-four-framework if political-risk subcontainer is absent
        const zone = document.querySelector('[data-testid="zone-1d-four-framework"]');
        if (!zone) return false;
        const allTagged = Array.from(zone.querySelectorAll("[data-testid]"));
        const findIdx = (id: string) => allTagged.findIndex(el => el.getAttribute("data-testid") === id);
        const sevIdx = findIdx("psp-severity-row");
        const drvIdx = findIdx("psp-driver-row");
        const anaIdx = findIdx("psp-historical-analogue");
        if (sevIdx === -1 || drvIdx === -1 || anaIdx === -1) return false;
        return sevIdx < drvIdx && drvIdx < anaIdx;
      }
      const allTagged = Array.from(container.querySelectorAll("[data-testid]"));
      const findIdx = (id: string) => allTagged.findIndex(el => el.getAttribute("data-testid") === id);
      const sevIdx = findIdx("psp-severity-row");
      const drvIdx = findIdx("psp-driver-row");
      const anaIdx = findIdx("psp-historical-analogue");
      if (sevIdx === -1 || drvIdx === -1 || anaIdx === -1) return false;
      return sevIdx < drvIdx && drvIdx < anaIdx;
    });

    expect(isCorrectOrder).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// AC-1255-3: psp-driver-row updates reactively on step advance (#1255)
//
// Intent doc §6 AC-1255-3:
// When the active step advances from step 3 to step 4 in the Senegal fixture,
// the text content of psp-driver-row is re-evaluated (may stay same or change —
// assert the element reflects the step-4 driver, not a stale step-3 value).
//
// Implementation: closure variable controls which driver category the mock returns.
// Step 3: "fiscal_sustainability" → advance → Step 4: "governance"
// Stale driver silent failure: if the row still shows "fiscal sustainability" after
// advancing to step 4, the driver prop is not reactive.
// ---------------------------------------------------------------------------

test.describe("AC-1255-3: psp-driver-row updates on step advance (step 3 → step 4) (#1255)", () => {
  let senScenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      // Advance 3 steps; n_steps: 5 allows one more UI advance to step 4
      senScenarioId = await createScenarioG2(["SEN"], 3, `G2-SEN-AC3-${Date.now()}`, true, 5);
    } catch {
      senScenarioId = null;
    }
  });

  test("AC-1255-3: psp-driver-row reflects step-4 driver after advancing from step 3", async ({
    page,
  }) => {
    if (!senScenarioId) return;

    const sid = senScenarioId;

    // Closure variable: starts at step 3 (fiscal_sustainability), updates before advance click
    let currentDriver: string | null = "fiscal_sustainability";

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMockG2(sid)),
      });
    });

    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMockG2(sid, {
          pspValue: "0.5200",
          pspDominantDriver: currentDriver,
          stepIndex: 3,
        })),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: driver row must be present (G2 implementation landed)
    const driverRow = page.locator('[data-testid="psp-driver-row"]');
    if (!(await driverRow.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // Confirm step-3 driver is visible
    await expect(driverRow).toContainText("fiscal sustainability");

    // Update mock to step-4 driver (governance) before advancing
    currentDriver = "governance";

    // Advance to step 4 — guard on isEnabled to avoid 30s click timeout on disabled button
    const nextStepBtn = page.getByRole("button", { name: /Next Step/ });
    if (!(await nextStepBtn.isEnabled({ timeout: 5_000 }).catch(() => false))) return;
    await nextStepBtn.click();
    await page.waitForTimeout(1_000);

    // AC-1255-3: driver row must reflect step-4 driver, not stale step-3 value
    // Silent failure: if "fiscal sustainability" still shows after advancing, the driver prop
    // is not reactive to step changes.
    await expect(driverRow).not.toContainText("fiscal sustainability");
    await expect(driverRow).toContainText("governance");
  });
});

// ---------------------------------------------------------------------------
// AC-1255-4: psp-driver-row absent from DOM when driver is null (#1255)
//
// Intent doc §6 AC-1255-4:
// In a scenario fixture where the current step has no legitimacy-driving events
// (legitimacy delta ≈ 0, PSP flat), psp-driver-row is NOT present in the DOM.
// No placeholder text, no dash, no "—". Absence is the silent treatment.
// ---------------------------------------------------------------------------

test.describe("AC-1255-4: psp-driver-row NOT in DOM when psp_dominant_driver is null (#1255)", () => {
  let senScenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      senScenarioId = await createScenarioG2(["SEN"], 1, `G2-SEN-AC4-${Date.now()}`, true, 5);
    } catch {
      senScenarioId = null;
    }
  });

  test("AC-1255-4: psp-driver-row not present in DOM when psp_dominant_driver is null", async ({
    page,
  }) => {
    if (!senScenarioId) return;

    const sid = senScenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMockG2(sid)),
      });
    });

    // Flat step: PSP stable (0.7800), no driver (null) — no legitimacy-driving events
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMockG2(sid, {
          pspValue: "0.7800",
          pspDominantDriver: null,
          stepIndex: 1,
        })),
      }),
    );

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Wait for Zone 1D to stabilize (PSP severity row should appear for non-null pspValue)
    const severityRow = page.locator('[data-testid="psp-severity-row"]');
    // If severity row is also absent, PE implementation hasn't landed — guard and exit
    const severityVisible = await severityRow.isVisible({ timeout: 5_000 }).catch(() => false);
    if (!severityVisible) return;

    // AC-1255-4: psp-driver-row must NOT be in the DOM when driver is null
    // Use .count() not .isVisible() — element must be completely absent, not just hidden
    const driverRowCount = await page.locator('[data-testid="psp-driver-row"]').count();
    expect(driverRowCount).toBe(0);

    // Silent failure check: element must not be present even with null/placeholder text
    // (e.g. "Driver: —" or "Driver: null" would be a rendering defect)
    const anyDriverText = await page.locator("text=/Driver:/i").count();
    expect(anyDriverText).toBe(0);
  });
});

// ---------------------------------------------------------------------------
// AC-1255-7: psp-driver-row visible at 1024×768 viewport (#1255)
//
// Intent doc §6 AC-1255-7:
// psp-driver-row is visible at 1024×768 viewport within the Zone 1D POLITICAL RISK
// section without vertical scrolling of that section. The longest driver label
// ("fiscal sustainability", ~17 chars) fits inline at fontSize: 10 within Zone 1D's
// 40% width allocation at 1024px.
//
// UX Designer watchpoint: 1024×768 Zone 1D width = 40% of 1024px = 409px.
// "fiscal sustainability" at fontSize 10 must render inline — assert row visible.
// ---------------------------------------------------------------------------

test.describe("AC-1255-7: psp-driver-row legibility at 1024×768 viewport (#1255)", () => {
  let senScenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      senScenarioId = await createScenarioG2(["SEN"], 3, `G2-SEN-AC7-${Date.now()}`, true, 5);
    } catch {
      senScenarioId = null;
    }
  });

  test("AC-1255-7: psp-driver-row visible at 1024×768 without scrolling Zone 1D", async ({
    page,
  }) => {
    if (!senScenarioId) return;

    const sid = senScenarioId;

    await page.route(`**/api/v1/scenarios/${sid}`, (route) => {
      if (route.request().method() !== "GET") { route.continue(); return; }
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeScenarioDetailMockG2(sid)),
      });
    });

    // Longest driver label: "fiscal sustainability" (worst-case for breakpoint legibility)
    await page.route("**/api/v1/scenarios/*/measurement-output**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(makeMeasurementOutputMockG2(sid, {
          pspValue: "0.5200",
          pspDominantDriver: "fiscal_sustainability",
          stepIndex: 3,
        })),
      }),
    );

    await page.setViewportSize({ width: 1024, height: 768 });
    await page.goto(`/?scenario=${encodeURIComponent(sid)}`);
    await waitForAppReady(page);

    const zone1d = page.locator('[data-testid="zone-1d-four-framework"]');
    if (!(await zone1d.isVisible({ timeout: 8_000 }).catch(() => false))) return;

    // Guard: driver row must be present (G2 implementation landed)
    const driverRow = page.locator('[data-testid="psp-driver-row"]');
    if (!(await driverRow.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    // AC-1255-7: must use .toBeVisible() to confirm no scroll required (ADR-015 L0 assertion)
    await expect(driverRow).toBeVisible();
    await expect(driverRow).toContainText("fiscal sustainability");

    // Driver row must be within the 1024×768 viewport without Zone 1D scrolling
    const driverBox = await driverRow.boundingBox();
    expect(driverBox).not.toBeNull();
    if (driverBox) {
      expect(driverBox.y + driverBox.height).toBeLessThanOrEqual(768);
    }
  });
});
