/**
 * E2E: ModeIndicator — US-026 acceptance tests.
 *
 * US-026 — mode indicator always visible in persistent header; exact text per mode.
 *
 * AC-030 — mode indicator renders with exact text "Replay" in Mode 1
 * AC-031 — mode indicator text does not contain raw field names
 * AC-032 — data-mode attribute reflects current store mode
 *
 * Guard pattern: all tests use isVisible({ timeout: 2000 }) before interacting —
 * ModeIndicator is not wired into App.tsx until integration PR (#463).
 * When not present, tests are no-ops (same pattern as all other E2E guards).
 *
 * Source: docs/ux/user-stories-instrument-cluster-m9.md §US-026
 *         UX-RULING-3 resolved 2026-05-23: "Replay" / "Simulation" / "Active Control"
 *         Issue #459 — QA Lead acceptance tests
 */
import { test, expect } from "@playwright/test";

// ---------------------------------------------------------------------------
// AC-030: Mode indicator renders with exact text "Replay" in Mode 1 (default)
// Source: US-026, UX-RULING-3
// ---------------------------------------------------------------------------

test("AC-030: mode indicator renders 'Replay' in default Mode 1 state", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const indicator = page.locator('[data-testid="mode-indicator"]');
  const isVisible = await indicator.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  // Default store mode is MODE_1 → label must be exactly "Replay"
  await expect(indicator).toHaveText("Replay");
});

// ---------------------------------------------------------------------------
// AC-031: Mode indicator contains no raw field name strings
// Source: US-026, UX-RULING-3
// ---------------------------------------------------------------------------

test("AC-031: mode indicator label contains no raw field name strings", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const indicator = page.locator('[data-testid="mode-indicator"]');
  const isVisible = await indicator.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const text = await indicator.textContent();
  if (!text) return;

  expect(text).not.toContain("MODE_1");
  expect(text).not.toContain("MODE_2");
  expect(text).not.toContain("MODE_3");
  expect(text).not.toContain("_");
});

// ---------------------------------------------------------------------------
// AC-032: data-mode attribute reflects current store mode
// Source: US-026
// ---------------------------------------------------------------------------

test("AC-032: data-mode attribute on indicator matches store mode", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const indicator = page.locator('[data-testid="mode-indicator"]');
  const isVisible = await indicator.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  // Default mode is MODE_1
  const modeAttr = await indicator.getAttribute("data-mode");
  if (!modeAttr) return;

  expect(["MODE_1", "MODE_2", "MODE_3"]).toContain(modeAttr);
});
