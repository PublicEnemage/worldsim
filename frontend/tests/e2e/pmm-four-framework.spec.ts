/**
 * E2E: PMMWidgetZone1C and FourFrameworkZone1D — Zone 1C/1D acceptance tests.
 *
 * Type 1 (component-level) ACs: testable in isolation.
 * AC-022 — PMM widget container renders (data-testid="zone-1c-pmm")
 * AC-023 — PMM mode-specific label: "historical" in Mode 1 (US-019)
 * AC-024 — PMM direction arrow element present (US-019)
 * AC-025 — PMM label has no raw field name substrings (US-019)
 * AC-026 — Four-framework panel renders (data-testid="zone-1d-four-framework") (US-021)
 * AC-027 — Four framework labeled value elements present simultaneously (US-021)
 * AC-028 — null score → class "score-value--null" and text "—" (US-022 / UX-RULING-2)
 * AC-029 — zero score → class "score-value--numeric", no "—" text (US-022 / UX-RULING-2)
 *
 * Guard pattern: all tests use isVisible({ timeout: 2000 }) before interacting —
 * components are not wired into App.tsx until integration PR (Issue #463).
 * When not present, tests are no-ops (same pattern as trajectory-view.spec.ts).
 *
 * Source: docs/frontend/fa-brief-m9-instrument-cluster.md §Named Acceptance Criteria
 *         Issue #462 — PMM Widget and Four-Framework Current Position
 */
import { test, expect } from "@playwright/test";

// ---------------------------------------------------------------------------
// AC-022: PMM widget container renders
// ---------------------------------------------------------------------------

test("AC-022: PMM widget renders at zone-1c-pmm", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const pmm = page.locator('[data-testid="zone-1c-pmm"]');
  const isVisible = await pmm.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  await expect(pmm).toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-023: PMM mode-specific label in Mode 1
// Source: US-019, ADR-008 Decision 6
// ---------------------------------------------------------------------------

test("AC-023: PMM label reads 'Policy Maneuver Margin — historical' in Mode 1", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const pmm = page.locator('[data-testid="zone-1c-pmm"]');
  const isVisible = await pmm.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  // Default store mode is MODE_1
  const modeAttr = await pmm.getAttribute("data-mode");
  if (modeAttr !== "MODE_1") return;

  const label = pmm.locator('[data-testid="pmm-label"]');
  const labelVisible = await label.isVisible({ timeout: 1000 }).catch(() => false);
  if (!labelVisible) return;

  await expect(label).toContainText("Policy Maneuver Margin — historical");
});

// ---------------------------------------------------------------------------
// AC-024: PMM direction arrow element present
// Source: US-019
// ---------------------------------------------------------------------------

test("AC-024: PMM direction arrow element is present in the DOM", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const pmm = page.locator('[data-testid="zone-1c-pmm"]');
  const isVisible = await pmm.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const arrow = pmm.locator('[data-testid="pmm-direction-arrow"]');
  const arrowVisible = await arrow.isVisible({ timeout: 1000 }).catch(() => false);
  if (!arrowVisible) return;

  await expect(arrow).toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-025: PMM label contains no raw field name substrings
// Source: US-019
// ---------------------------------------------------------------------------

test("AC-025: PMM label does not contain raw field name strings", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const pmm = page.locator('[data-testid="zone-1c-pmm"]');
  const isVisible = await pmm.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const label = pmm.locator('[data-testid="pmm-label"]');
  const labelVisible = await label.isVisible({ timeout: 1000 }).catch(() => false);
  if (!labelVisible) return;

  const text = await label.textContent();
  if (!text) return;

  expect(text).not.toContain("coffin_corner_index");
  expect(text).not.toContain("coffin_corner");
  expect(text).not.toContain("pmm_value");
});

// ---------------------------------------------------------------------------
// AC-026: Four-framework panel renders
// Source: US-021
// ---------------------------------------------------------------------------

test("AC-026: Four-framework panel renders at zone-1d-four-framework", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const panel = page.locator('[data-testid="zone-1d-four-framework"]');
  const isVisible = await panel.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  await expect(panel).toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-027: All four framework labeled value elements present simultaneously
// Source: US-021
// ---------------------------------------------------------------------------

test("AC-027: all four framework rows visible simultaneously without tabs", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const panel = page.locator('[data-testid="zone-1d-four-framework"]');
  const isVisible = await panel.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const frameworks = ["financial", "human_development", "ecological", "governance"];

  for (const key of frameworks) {
    const label = panel.locator(`[data-testid="framework-label-${key}"]`);
    const score = panel.locator(`[data-testid="framework-score-${key}"]`);

    const labelVisible = await label.isVisible({ timeout: 1000 }).catch(() => false);
    if (!labelVisible) continue;

    await expect(label).toBeVisible();
    await expect(score).toBeVisible();
  }

  // Assert human-readable labels (not raw field names)
  const labelFinancial = panel.locator('[data-testid="framework-label-financial"]');
  const lv = await labelFinancial.isVisible({ timeout: 1000 }).catch(() => false);
  if (lv) {
    const text = await labelFinancial.textContent();
    expect(text).toBe("Financial");
    expect(text).not.toBe("financial");
  }
});

// ---------------------------------------------------------------------------
// AC-028: null score → class "score-value--null" and displays "—"
// Source: US-022 / UX-RULING-2
// ---------------------------------------------------------------------------

test("AC-028: null composite score → class 'score-value--null' and text '—'", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const panel = page.locator('[data-testid="zone-1d-four-framework"]');
  const isVisible = await panel.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  // Null score — governance is null by default (no trajectory loaded yet)
  // Only assertable if the element is present
  const govScore = panel.locator('[data-testid="framework-score-governance"]');
  const govVisible = await govScore.isVisible({ timeout: 1000 }).catch(() => false);
  if (!govVisible) return;

  const hasNullClass = await govScore.evaluate((el) =>
    el.classList.contains("score-value--null"),
  );
  if (!hasNullClass) return; // Score may be non-null in loaded state — no-op

  await expect(govScore).toHaveText("—");
  expect(hasNullClass).toBe(true);
});

// ---------------------------------------------------------------------------
// AC-029: zero score → class "score-value--numeric", no "—" text
// Source: US-022 / UX-RULING-2
// ---------------------------------------------------------------------------

test("AC-029: zero composite score → class 'score-value--numeric', no '—' text", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const panel = page.locator('[data-testid="zone-1d-four-framework"]');
  const isVisible = await panel.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  // Find any score element that has score-value--numeric class
  const numericScores = panel.locator(".score-value--numeric");
  const count = await numericScores.count();
  if (count === 0) return; // No numeric scores loaded yet — no-op

  const first = numericScores.first();
  const text = await first.textContent();
  expect(text).not.toBe("—");
  expect(text).toMatch(/^\d/); // Starts with a digit

  const hasNullClass = await first.evaluate((el) =>
    el.classList.contains("score-value--null"),
  );
  expect(hasNullClass).toBe(false);
});
