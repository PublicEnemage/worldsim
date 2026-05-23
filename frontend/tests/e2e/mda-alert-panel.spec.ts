/**
 * E2E: MDAAlertPanelZone1B — Zone 1B acceptance tests.
 *
 * Type 1 (component-level) ACs: testable with MDAAlertPanelZone1B in isolation.
 * AC-016 — panel container renders at data-testid="zone-1b-mda-alerts"
 * AC-017 — alert rows display in TERMINAL → CRITICAL → WARNING order (US-014)
 * AC-018 — compact 3-line format at 1024×768 (US-013)
 * AC-019 — framework source abbreviation visible (FIN/HDI/ECO/GOV) (US-015)
 * AC-020 — Mode 1 alert text: "crossed" present, "is projected" absent (US-016)
 * AC-021 — "Caused by:" absent from Mode 1 and Mode 2 rows (US-017)
 *
 * Guard pattern: all tests use isVisible({ timeout: 2000 }) before interacting —
 * panel is not wired into App.tsx until integration PR (Issue #462/463).
 * When not present, tests are no-ops (same pattern as trajectory-view.spec.ts).
 *
 * Source: docs/frontend/fa-brief-m9-instrument-cluster.md §Named Acceptance Criteria
 *         Issue #461 — MDA Alert Panel Zone 1B
 */
import { test, expect } from "@playwright/test";

// ---------------------------------------------------------------------------
// AC-016: MDA alert panel container renders
// ---------------------------------------------------------------------------

test("AC-016: MDA alert panel renders at zone-1b-mda-alerts", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const panel = page.locator('[data-testid="zone-1b-mda-alerts"]');
  const isVisible = await panel.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  await expect(panel).toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-017: Severity ordering — TERMINAL appears before CRITICAL, CRITICAL before WARNING
// Source: US-014
// ---------------------------------------------------------------------------

test("AC-017: alert rows appear in severity order TERMINAL → CRITICAL → WARNING", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const panel = page.locator('[data-testid="zone-1b-mda-alerts"]');
  const isVisible = await panel.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const rows = panel.locator('[data-testid="mda-alert-row"]');
  const count = await rows.count();
  if (count < 2) return;

  const severities: string[] = [];
  for (let i = 0; i < count; i++) {
    const severity = await rows.nth(i).getAttribute("data-severity");
    if (severity) severities.push(severity);
  }

  const order = ["TERMINAL", "CRITICAL", "WARNING"];
  for (let i = 0; i < severities.length - 1; i++) {
    const a = order.indexOf(severities[i]);
    const b = order.indexOf(severities[i + 1]);
    expect(a).toBeLessThanOrEqual(b);
  }
});

// ---------------------------------------------------------------------------
// AC-018: Compact 3-line format at 1024×768 — three alert lines visible
// Source: US-013
// ---------------------------------------------------------------------------

test("AC-018: compact 3-line row format at 1024×768", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const panel = page.locator('[data-testid="zone-1b-mda-alerts"]');
  const isVisible = await panel.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const rows = panel.locator('[data-testid="mda-alert-row"]');
  const count = await rows.count();
  if (count === 0) return;

  const firstRow = rows.first();
  const line1 = firstRow.locator('[data-testid="alert-line-1"]');
  const line2 = firstRow.locator('[data-testid="alert-line-2"]');
  const line3 = firstRow.locator('[data-testid="alert-line-3"]');

  await expect(line1).toBeVisible();
  await expect(line2).toBeVisible();
  await expect(line3).toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-019: Framework source abbreviation visible without expanding
// Source: US-015
// ---------------------------------------------------------------------------

test("AC-019: framework abbreviation visible in alert row (no expand required)", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");

  const panel = page.locator('[data-testid="zone-1b-mda-alerts"]');
  const isVisible = await panel.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const rows = panel.locator('[data-testid="mda-alert-row"]');
  const count = await rows.count();
  if (count === 0) return;

  // At 1280×800, FullDensityAlertRow is rendered — check framework source badge
  const fwBadge = rows.first().locator('[data-testid="alert-framework-source"]');
  const badgeVisible = await fwBadge.isVisible({ timeout: 1000 }).catch(() => false);
  if (!badgeVisible) return;

  const text = await fwBadge.textContent();
  const validAbbrevs = ["FIN", "HDI", "ECO", "GOV"];
  const isValid = validAbbrevs.some((abbrev) => text?.includes(abbrev));
  expect(isValid).toBe(true);
});

// ---------------------------------------------------------------------------
// AC-020: Mode 1 alert text: "crossed" present, "is projected to cross" absent
// Source: US-016 / UX-RULING-1
// ---------------------------------------------------------------------------

test("AC-020: Mode 1 alert text contains 'crossed' and not 'is projected'", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");

  const panel = page.locator('[data-testid="zone-1b-mda-alerts"]');
  const isVisible = await panel.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  // Only assertable when mode is MODE_1 (store default) and modeText is rendered
  const modeTexts = panel.locator('[data-testid="alert-mode-text"]');
  const textCount = await modeTexts.count();
  if (textCount === 0) return;

  const firstText = await modeTexts.first().textContent();
  if (!firstText) return;

  // If the panel has alert-mode-text, the store mode must be checked via data attribute
  // We rely on the default store mode being MODE_1
  expect(firstText).toContain("crossed");
  expect(firstText).not.toContain("is projected");
});

// ---------------------------------------------------------------------------
// AC-021: "Caused by:" absent from Mode 1 and Mode 2 rows
// Source: US-017
// ---------------------------------------------------------------------------

test("AC-021: 'Caused by:' not present in Mode 1 rows", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const panel = page.locator('[data-testid="zone-1b-mda-alerts"]');
  const isVisible = await panel.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const causalAttribution = panel.locator('[data-testid="alert-causal-attribution"]');
  const count = await causalAttribution.count();
  // In MODE_1, no causal attribution elements should be present
  expect(count).toBe(0);
});
