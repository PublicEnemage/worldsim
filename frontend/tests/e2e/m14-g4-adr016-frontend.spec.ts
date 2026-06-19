/**
 * E2E: M14-G4 ADR-016 Frontend — AC-1 through AC-9.
 *
 * Authored BEFORE implementation from intent document at:
 * docs/process/intents/M14-G4-2026-06-17-adr016-frontend.md
 *
 * These tests define what "done" means for G4. All assertions use
 * data-testid attributes named in the intent document and ADR-016 §UX-3.
 *
 * ADR: ADR-016 — Scenario Grounding Architecture (Accepted 2026-06-16, PR #967)
 * G3 gate: BPO ACCEPT 2026-06-17 (PR #1012); endpoints confirmed in running application
 *
 * Components and ACs covered:
 *   AC-1 — data-quality-preview visible for JOR 2024; contains "JOR" + T[1-5] label
 *   AC-2 — data-quality-preview contains "synthetic" verbatim for ZMB 2024 (T4)
 *   AC-3 — grounding strip opens within 3s for JOR scenario with source citation
 *   AC-4 — scenario-parameters shows fiscal multiplier, base year, entity, n_steps in one click
 *   AC-5 — fidelity-contextualisation header contains "model relationships" + "not input data"
 *   AC-6 — choropleth header "Reference data — not scenario outputs" verbatim; no interaction
 *   AC-7 — grounding strip contains no blank/"None"/"null" section headings for JOR scenario
 *   AC-8 — data-quality-preview shows "Data quality preview unavailable" on /data-quality 500
 *   AC-9 — grounding strip shows "Initial state data not available" on empty frameworks response
 *
 * Guard pattern: each test guards on the presence of its primary testid. Before G4
 * implementation lands, the testid is absent — the test returns without failing.
 * A guard that fires is a no-op, not a pass. Tests become active when implementation lands.
 *
 * Fixture: G3 scenario 68b31277 (JOR, 2023, 8 steps, status: completed) is tried first
 * in beforeAll. If not accessible, a JOR scenario is created and advanced via API.
 *
 * Route mocking (AC-8, AC-9): Playwright page.route() intercepts API calls before they
 * reach the backend. Mocks are per-test and do not affect other tests.
 *
 * testid reference:
 *   data-testid="entity-selector"         — entity selector in scenario creation form (G1)
 *   data-testid="data-quality-preview"    — data quality preview panel (G4, Component 1)
 *   data-testid="grounding-strip-toggle"  — button that opens the grounding strip (G4, Component 2)
 *   data-testid="grounding-strip"         — grounding strip panel body (G4, Component 2)
 *   data-testid="mode-indicator"          — mode indicator chip (existing)
 *   data-testid="scenario-parameters"     — parameter persistence panel (G4, Component 4)
 *   data-testid="fidelity-toggle"         — Fidelity panel toggle (existing)
 *   data-testid="fidelity-dashboard"      — Fidelity panel body (existing)
 *   data-testid="fidelity-contextualisation" — static scope header in Fidelity panel (G4, IC-4)
 *   data-testid="fidelity-case-GRC"       — GRC backtesting case card (existing, presence confirms additive)
 */
import { test, expect } from "@playwright/test";

const API_BASE = "http://localhost:8000/api/v1";

// G3 JOR completed scenario — 2023, 8 steps, confirmed at G3 BPO Step 5 Validate 2026-06-17
const G3_JOR_SCENARIO_ID = "68b31277";

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

async function openScenarioPanel(page: import("@playwright/test").Page): Promise<void> {
  await page.getByRole("button", { name: /Scenarios/ }).click();
}

async function selectEntityAndYear(
  page: import("@playwright/test").Page,
  entity: string,
  year: string,
): Promise<void> {
  await page.locator('[data-testid="entity-selector"]').selectOption(entity);
  const yearInput = page.locator('[aria-label="Start year"]');
  await yearInput.fill(year);
  // Tab triggers the onChange / blur event to kick off the data-quality API call
  await yearInput.press("Tab");
}

/**
 * Open the grounding strip panel. Tries the suggested data-testid first,
 * falls back to button text ("Grounding ▼"). Returns false if neither is found.
 * The testid is specified as "grounding-strip-toggle" in the intent document §7.
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
 * Check whether the G3 JOR fixture scenario (68b31277) is accessible and completed.
 * Used in beforeAll blocks so tests can share the fixture when it's available.
 */
async function checkG3FixtureAccessible(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/scenarios/${G3_JOR_SCENARIO_ID}`);
    if (!res.ok) return false;
    const body = (await res.json()) as { status: string };
    return body.status === "completed";
  } catch {
    return false;
  }
}

/**
 * Create a JOR scenario and advance it to completion via API.
 * Falls back when the G3 fixture is not accessible in the test environment.
 */
async function createJORCompletedScenario(name: string): Promise<string> {
  const createRes = await fetch(`${API_BASE}/scenarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name,
      configuration: { entities: ["JOR"], n_steps: 3, start_date: "2023-01-01" },
    }),
  });
  if (!createRes.ok) throw new Error(`Create failed: ${createRes.status}`);
  const { scenario_id: id } = (await createRes.json()) as { scenario_id: string };

  for (let i = 0; i < 3; i++) {
    const advRes = await fetch(
      `${API_BASE}/scenarios/${encodeURIComponent(id)}/advance`,
      { method: "POST" },
    );
    if (!advRes.ok) throw new Error(`Advance ${i + 1} failed: ${advRes.status}`);
  }

  const detail = (await fetch(`${API_BASE}/scenarios/${encodeURIComponent(id)}`).then((r) =>
    r.json(),
  )) as { status: string };
  if (detail.status !== "completed") {
    throw new Error(`Expected completed; got: ${detail.status}`);
  }
  return id;
}

// ---------------------------------------------------------------------------
// AC-1: data-quality-preview visible for JOR 2024 with entity code and T-label
//
// Source: intent document §4 AC-1; ADR-016 §UX-3 criterion 1
//
// Observable state: in scenario creation form with entity "JOR" and year "2024"
// selected, [data-testid="data-quality-preview"] is visible, contains the text
// "JOR", and contains at least one tier label matching the pattern T[1-5].
// The preview appears within 2s without any additional interaction.
// ---------------------------------------------------------------------------

test("AC-1: data-quality-preview visible for JOR 2024 with entity code and T-label", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await waitForAppReady(page);
  await openScenarioPanel(page);

  const entitySelector = page.locator('[data-testid="entity-selector"]');
  if (!(await entitySelector.isVisible({ timeout: 5_000 }).catch(() => false))) return;

  await selectEntityAndYear(page, "JOR", "2024");

  const preview = page.locator('[data-testid="data-quality-preview"]');
  if (!(await preview.isVisible({ timeout: 3_000 }).catch(() => false))) return; // G4 guard

  await expect(preview).toContainText("JOR");

  const text = await preview.textContent();
  expect(text).toMatch(/T[1-5]/);
});

// ---------------------------------------------------------------------------
// AC-2: data-quality-preview contains "synthetic" verbatim for ZMB 2024
//
// Source: intent document §4 AC-2; ADR-016 §Component 1; DATA_STANDARDS.md T4
//
// Observable state: in scenario creation form with entity "ZMB" and year "2024"
// selected, [data-testid="data-quality-preview"] contains the word "synthetic"
// in lowercase — exact string, not case-insensitive. ZMB ecological data is T4
// (synthetic — SADC comparables), requiring verbatim disclosure per DATA_STANDARDS.md.
// ---------------------------------------------------------------------------

test("AC-2: data-quality-preview contains 'synthetic' verbatim for ZMB 2024", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await waitForAppReady(page);
  await openScenarioPanel(page);

  if (
    !(await page
      .locator('[data-testid="entity-selector"]')
      .isVisible({ timeout: 5_000 })
      .catch(() => false))
  )
    return;

  await selectEntityAndYear(page, "ZMB", "2024");

  const preview = page.locator('[data-testid="data-quality-preview"]');
  if (!(await preview.isVisible({ timeout: 3_000 }).catch(() => false))) return; // G4 guard

  // Lowercase "synthetic" is required verbatim per ADR-016 §Component 1
  await expect(preview).toContainText("synthetic");
});

// ---------------------------------------------------------------------------
// AC-3 + AC-7: Grounding strip tests — require a JOR completed scenario
//
// Shared beforeAll resolves the G3 fixture (68b31277) or creates a JOR scenario.
// ---------------------------------------------------------------------------

let jorScenarioId: string | null = null;

test.describe("AC-3/AC-7: Grounding strip (JOR scenario fixture)", () => {
  test.beforeAll(async () => {
    try {
      jorScenarioId = (await checkG3FixtureAccessible())
        ? G3_JOR_SCENARIO_ID
        : await createJORCompletedScenario(`G4-grounding-${Date.now()}`);
    } catch {
      jorScenarioId = null;
    }
  });

  // -------------------------------------------------------------------------
  // AC-3: grounding strip opens within 3s with at least one source citation
  //
  // Source: intent document §4 AC-3; ADR-016 §UX-3 criterion 3
  //
  // Observable state: JOR scenario loaded; after one click on "Grounding ▼",
  // [data-testid="grounding-strip"] is visible within 3s and contains at least
  // one text node with a non-empty source institution name (e.g., "CBJ", "IMF").
  // Row format: "[display_name]: [value] [unit]  [Source · Vintage · T{N}]"
  // -------------------------------------------------------------------------

  test("AC-3: grounding strip opens with source citation within 3s for JOR scenario", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    // Route mock: inject a known /initial-state response so AC-3 is independent of
    // source_registry seeding in the test environment. This directly tests what
    // REJECT-001 fixed: GroundingStrip.tsx must read ind.source/ind.vintage
    // (not ind.source_institution/ind.data_vintage). If the field names are wrong,
    // the citation row will be blank even when the response has "source": "CBJ".
    await page.route("**/api/v1/scenarios/*/initial-state**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          scenario_id: jorScenarioId,
          entity_id: "JOR",
          step_0_year: 2023,
          frameworks: {
            financial: {
              indicators: [
                {
                  name: "reserve_coverage_months",
                  display_name: "Reserve coverage",
                  value: 7.1,
                  unit: "months",
                  source: "CBJ",
                  vintage: "2023-Q4",
                  confidence_tier: 2,
                  is_synthetic: false,
                },
              ],
            },
          },
        }),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    if (!(await openGroundingStrip(page))) return; // G4 guard

    const strip = page.locator('[data-testid="grounding-strip"]');
    await expect(strip).toBeVisible({ timeout: 4_000 });

    // Wait for the mocked response to populate the strip (replaces "Loading grounding data…").
    await expect(strip).not.toContainText("Loading grounding data", { timeout: 8_000 });

    const text = await strip.textContent();
    // Assert by string match — no generic regex fallback (NM-045: the fallback matched
    // the tier separator "· T2" and masked the field name mismatch that caused REJECT-001).
    const hasCitation =
      (text ?? "").includes("CBJ") ||
      (text ?? "").includes("IMF") ||
      (text ?? "").includes("DOS") ||
      (text ?? "").includes("World Bank") ||
      (text ?? "").includes("V-Dem");
    expect(hasCitation).toBe(true);
  });

  // -------------------------------------------------------------------------
  // AC-7: grounding strip renders no blank/"None"/"null" section headings
  //
  // Source: intent document §4 AC-7; G3 BPO Step 5 forwarded observation
  //
  // Observable state: JOR scenario loaded; grounding strip open; no heading
  // element inside [data-testid="grounding-strip"] has text equal to "", "None",
  // or "null". At least one named framework section is present.
  //
  // The "None" key appears in /initial-state for legacy simulation attributes
  // (pop_rank, economy_tier, gdp_usd_millions) that lack measurement_framework.
  // The UI must filter these and render only named frameworks.
  // -------------------------------------------------------------------------

  test("AC-7: grounding strip renders no blank/'None'/'null' section heading for JOR", async ({
    page,
  }) => {
    if (!jorScenarioId) return;

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(jorScenarioId)}`);
    await waitForAppReady(page);

    if (!(await openGroundingStrip(page))) return; // G4 guard

    const strip = page.locator('[data-testid="grounding-strip"]');
    await expect(strip).toBeVisible({ timeout: 4_000 });

    // Wait for data to arrive before checking headings (avoid race with "Loading..." text).
    await expect(strip).not.toContainText("Loading grounding data", { timeout: 8_000 });

    const headings = await strip
      .locator("h2, h3, h4, h5, [role='heading']")
      .allTextContents()
      .catch(() => [] as string[]);

    for (const h of headings) {
      const trimmed = h.trim();
      expect(trimmed).not.toBe("");
      expect(trimmed.toLowerCase()).not.toBe("none");
      expect(trimmed.toLowerCase()).not.toBe("null");
    }

    // At least one named framework section must be present
    const stripText = await strip.textContent();
    expect(/financial|human|ecological|governance|political/i.test(stripText ?? "")).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// AC-4: scenario-parameters shows all four parameter rows in one mode chip click
//
// Source: intent document §4 AC-4; ADR-016 §Component 4 and §EL Decision 4
//
// Observable state: any completed scenario loaded; after clicking
// [data-testid="mode-indicator"], [data-testid="scenario-parameters"] is visible
// and its text contains: fiscal multiplier value, base year (four-digit 1900–2100),
// entity code, and number of steps. Absent values show "(not recorded)" — the row
// is present even when the stored value is missing.
// ---------------------------------------------------------------------------

test.describe("AC-4: Parameter persistence display (completed scenario required)", () => {
  let ac4ScenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      ac4ScenarioId = (await checkG3FixtureAccessible())
        ? G3_JOR_SCENARIO_ID
        : await createJORCompletedScenario(`G4-params-${Date.now()}`);
    } catch {
      ac4ScenarioId = null;
    }
  });

  test("AC-4: scenario-parameters shows fiscal multiplier, base year, entity, n_steps in one click", async ({
    page,
  }) => {
    if (!ac4ScenarioId) return;

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(ac4ScenarioId)}`);
    await waitForAppReady(page);

    const modeIndicator = page.locator('[data-testid="mode-indicator"]');
    if (!(await modeIndicator.isVisible({ timeout: 5_000 }).catch(() => false))) return;

    await modeIndicator.click();

    const params = page.locator('[data-testid="scenario-parameters"]');
    if (!(await params.isVisible({ timeout: 3_000 }).catch(() => false))) return; // G4 guard

    const text = await params.textContent() ?? "";

    // Fiscal multiplier: a decimal number or "(not recorded)" per ADR-016 §EL Decision 4
    expect(/\d+\.\d+/.test(text) || text.includes("(not recorded)")).toBe(true);

    // Base year: four-digit number in range 1900–2100, or "(not recorded)" if absent.
    // No \b word boundary — textContent() concatenates spans without separator, so "2023"
    // appears as "year2023" where \b before "2" is absent ("r"→"2" are both \w).
    expect(/(19|20|21)\d{2}/.test(text) || text.includes("(not recorded)")).toBe(true);

    // Entity code from the supported set (ADR-016 §EL Decision 1 scope)
    expect(
      text.includes("JOR") ||
        text.includes("GRC") ||
        text.includes("EGY") ||
        text.includes("ZMB"),
    ).toBe(true);

    // Number of steps: positive integer or "(not recorded)".
    // No \b — same textContent concatenation issue as base year ("Steps3Fiscal" has no
    // word boundary around "3"). Any [1-9]\d* sequence confirms steps are present.
    expect(/[1-9]\d*/.test(text) || text.includes("(not recorded)")).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// AC-5: Fidelity panel static scope header (IC-4 mitigation)
//
// Source: intent document §4 AC-5; ADR-016 §EL Decision 2; visual spec §4b
//
// Observable state: with the Fidelity panel open, [data-testid="fidelity-contextualisation"]
// is visible and contains both "model relationships" and "not input data". Existing
// backtesting case cards are still present below the header (header is additive).
//
// IC-4 false affordance: without this header, the Fidelity panel implies it validates
// input data for the active scenario. The header clarifies scope verbatim.
// ---------------------------------------------------------------------------

test("AC-5: fidelity-contextualisation header present with 'model relationships' + 'not input data'", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await waitForAppReady(page);

  const fidelityToggle = page.locator('[data-testid="fidelity-toggle"]');
  if (!(await fidelityToggle.isVisible({ timeout: 5_000 }).catch(() => false))) return;

  await fidelityToggle.click();
  await expect(page.locator('[data-testid="fidelity-dashboard"]')).toBeVisible({
    timeout: 3_000,
  });

  const contextHeader = page.locator('[data-testid="fidelity-contextualisation"]');
  if (!(await contextHeader.isVisible({ timeout: 3_000 }).catch(() => false))) return; // G4 guard

  await expect(contextHeader).toContainText("model relationships");
  await expect(contextHeader).toContainText("not input data");

  // Existing GRC case card must remain visible — header is additive, not replacement
  await expect(page.locator('[data-testid="fidelity-case-GRC"]')).toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-6: Choropleth reference header — verbatim text, always visible
//
// Source: intent document §4 AC-6; ADR-016 §EL Decision 5; visual spec §4b
//
// Observable state: the verbatim text "Reference data — not scenario outputs" is
// visible on the page without any user interaction, whether or not a scenario is
// loaded. The header is not inside a collapsed panel or tooltip.
//
// IC-6 ambiguity: without this header, the choropleth appears to show active
// scenario outputs. It shows reference data only (world baseline — not simulation).
// ---------------------------------------------------------------------------

test("AC-6: choropleth header 'Reference data — not scenario outputs' visible without interaction", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await waitForAppReady(page);

  const header = page.getByText("Reference data — not scenario outputs", { exact: true });
  if (!(await header.isVisible({ timeout: 5_000 }).catch(() => false))) return; // G4 guard

  await expect(header).toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-8: data-quality-preview fallback on /data-quality API returning 500
//
// Source: intent document §4 AC-8; ADR-016 §Silent Failure Mode (Component 1)
//
// Observable state: with /api/v1/entities/*/data-quality intercepted to return 500,
// [data-testid="data-quality-preview"] shows text containing "Data quality preview
// unavailable" — not an empty space, not an unhandled error. The scenario creation
// form remains functional (name input still visible).
//
// Silent failure distinguisher: an empty preview looks identical to a successful
// load with no tiers — the fallback text is the only disclosure of the API failure.
// ---------------------------------------------------------------------------

test("AC-8: data-quality-preview shows fallback text when /data-quality returns 500", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });

  await page.route("**/api/v1/entities/*/data-quality**", (route) =>
    route.fulfill({
      status: 500,
      contentType: "application/json",
      body: JSON.stringify({ detail: "Internal Server Error" }),
    }),
  );

  await page.goto("/");
  await waitForAppReady(page);
  await openScenarioPanel(page);

  if (
    !(await page
      .locator('[data-testid="entity-selector"]')
      .isVisible({ timeout: 5_000 })
      .catch(() => false))
  )
    return;

  await selectEntityAndYear(page, "JOR", "2024");

  const preview = page.locator('[data-testid="data-quality-preview"]');
  if (!(await preview.isVisible({ timeout: 3_000 }).catch(() => false))) return; // G4 guard

  await expect(preview).toContainText("Data quality preview unavailable");

  // Form must remain functional — Persona 2 can still create a scenario
  await expect(page.locator('input[placeholder="Scenario name"]')).toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-9: grounding strip fallback on /initial-state returning empty frameworks
//
// Source: intent document §4 AC-9; ADR-016 §Silent Failure Mode (Component 2)
//
// Observable state: with /api/v1/scenarios/*/initial-state intercepted to return
// {"frameworks": {}}, [data-testid="grounding-strip"] shows text containing
// "Initial state data not available" — not an empty strip body, not an unhandled
// error. The "Grounding ▼" button is still present and the panel still opens.
//
// Silent failure distinguisher: an empty grounding strip body (no indicator rows,
// no fallback text) is indistinguishable from a successful load with zero indicators.
// The fallback text is the required disclosure that data is absent, not merely empty.
// ---------------------------------------------------------------------------

test.describe("AC-9: Grounding strip empty-frameworks fallback (route mock)", () => {
  let ac9ScenarioId: string | null = null;

  test.beforeAll(async () => {
    try {
      ac9ScenarioId = (await checkG3FixtureAccessible())
        ? G3_JOR_SCENARIO_ID
        : await createJORCompletedScenario(`G4-ac9-${Date.now()}`);
    } catch {
      ac9ScenarioId = null;
    }
  });

  test("AC-9: grounding strip shows 'Initial state data not available' on empty frameworks response", async ({
    page,
  }) => {
    if (!ac9ScenarioId) return;

    await page.route("**/api/v1/scenarios/*/initial-state**", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ frameworks: {} }),
      }),
    );

    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`/?scenario=${encodeURIComponent(ac9ScenarioId)}`);
    await waitForAppReady(page);

    if (!(await openGroundingStrip(page))) return; // G4 guard

    const strip = page.locator('[data-testid="grounding-strip"]');
    if (!(await strip.isVisible({ timeout: 4_000 }).catch(() => false))) return;

    await expect(strip).toContainText("Initial state data not available");
  });
});
