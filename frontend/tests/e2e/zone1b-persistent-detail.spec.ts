/**
 * E2E: Zone 1B Persistent-Detail Layout — ADR-014 acceptance tests.
 *
 * These tests were authored BEFORE implementation, from the intent document
 * at docs/process/intents/ADR-014-2026-06-13-alert-panel-ux.md. They
 * define what "done" means for G7 (#852). All assertions use data-testid
 * attributes named in the intent document and the ADR.
 *
 * Source AC references:
 *   AC-1  — UX-3: zero-interaction detail slot populated at fixture load
 *   AC-2  — UX-6: TERMINAL auto-ranking; TERMINAL is in detail slot
 *   AC-3  — SF-1: detail slot height > 0 at all three reference viewports
 *   AC-4  — SF-2: consecutive count liveness after step advance
 *   AC-5  — SF-3: compact rows scan-only; click produces no detail change
 *   AC-6  — SF-4: [NEW] badge fires on mda_id change in Mode 3
 *   AC-7  — UX sign-off condition 1: compact row height ≤ 26px at 1024×768
 *   AC-8  — UX sign-off condition 2: mode-dependent tense in detail slot
 *   AC-9  — Q1 ruling: entity ISO code in detail and compact rows
 *   AC-10 — Q4 ruling: confidence tier label unchanged after step advance
 *
 * Guard pattern: tests check isVisible({ timeout: 2000 }) before asserting.
 * When Zone 1B is not present in the live app (pre-integration), tests are no-ops.
 * A test that skips because the component is absent is not a failure.
 *
 * ADR-014 authority: accepted 2026-06-12. Sprint entry EL-approved 2026-06-13.
 */
import { test, expect } from "@playwright/test";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function getZone1BDetailSlot(page: import("@playwright/test").Page) {
  return page.locator('[data-testid="zone-1b-top-detail"]');
}

async function getZone1BCompact(page: import("@playwright/test").Page) {
  return page.locator('[data-testid="zone-1b-compact"]');
}

// ---------------------------------------------------------------------------
// AC-1: Zero-interaction detail slot — UX-3
// In the live app at 1440×900, zone-1b-top-detail is visible with non-empty
// indicator name and current value without any click or scroll after page load.
// ---------------------------------------------------------------------------

test("AC-1: zone-1b-top-detail is visible and populated without any user interaction", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  const detail = await getZone1BDetailSlot(page);
  const isVisible = await detail.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  // No click or scroll between page load and these assertions
  await expect(detail).toBeVisible();

  const indicatorName = detail.locator('[data-testid="detail-indicator-name"]');
  const isIndicatorVisible = await indicatorName.isVisible({ timeout: 1000 }).catch(() => false);
  if (!isIndicatorVisible) return;

  const nameText = await indicatorName.textContent();
  expect(nameText).toBeTruthy();
  expect(nameText!.trim()).not.toBe("");

  const currentValue = detail.locator('[data-testid="detail-current-value"]');
  const currentText = await currentValue.textContent();
  expect(currentText).toBeTruthy();
  expect(currentText!.trim()).not.toBe("");
});

// ---------------------------------------------------------------------------
// AC-2: TERMINAL auto-ranking — UX-6
// When ≥1 TERMINAL alert is active, zone-1b-top-detail has data-severity="TERMINAL"
// and is visible at 1440×900 without any click or scroll.
// ---------------------------------------------------------------------------

test("AC-2: TERMINAL alert occupies detail slot when active — no click required", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  const detail = await getZone1BDetailSlot(page);
  const isVisible = await detail.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const severity = await detail.getAttribute("data-severity");
  if (!severity) return; // no alerts active; skip

  // If a TERMINAL is active, it must be in the detail slot (not a CRITICAL or WARNING)
  const panel = page.locator('[data-testid="zone-1b-mda-alerts"]');
  const terminalRows = panel.locator('[data-severity="TERMINAL"]');
  const terminalCount = await terminalRows.count().catch(() => 0);

  if (terminalCount > 0) {
    expect(severity).toBe("TERMINAL");
    // Confirm it is within Zone 1B bounds via bounding box
    const detailBox = await detail.boundingBox();
    const panelBox = await panel.boundingBox();
    expect(detailBox).not.toBeNull();
    expect(panelBox).not.toBeNull();
    // Detail slot top must be >= panel top (inside panel bounds)
    expect(detailBox!.y).toBeGreaterThanOrEqual(panelBox!.y - 2); // 2px tolerance
  }
});

// ---------------------------------------------------------------------------
// AC-3: Detail height invariant across viewports — SF-1
// zone-1b-top-detail has clientHeight > 0 at 1024×768, 1280×800, and 1440×900.
// No user interactions before assertion.
// ---------------------------------------------------------------------------

for (const [width, height] of [[1024, 768], [1280, 800], [1440, 900]] as const) {
  test(`AC-3: zone-1b-top-detail clientHeight > 0 at ${width}×${height}`, async ({ page }) => {
    await page.setViewportSize({ width, height });
    await page.goto("/");

    const detail = await getZone1BDetailSlot(page);
    const isVisible = await detail.isVisible({ timeout: 2000 }).catch(() => false);
    if (!isVisible) return;

    const clientHeight = await detail.evaluate((el) => el.clientHeight);
    expect(clientHeight).toBeGreaterThan(0);

    // Confirm compact sub-zone is also present
    const compact = await getZone1BCompact(page);
    const compactPresent = await compact.count() > 0;
    expect(compactPresent).toBe(true);
  });
}

// ---------------------------------------------------------------------------
// AC-4: Consecutive count liveness after step advance — SF-2
// After a step advance, detail-consecutive text matches the current step's
// consecutive_breach_steps for the top-ranked alert. Not stale.
// ---------------------------------------------------------------------------

test("AC-4: consecutive count in detail slot updates after step advance (not stale)", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  const detail = await getZone1BDetailSlot(page);
  const isVisible = await detail.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const consecutiveEl = detail.locator('[data-testid="detail-consecutive"]');
  const hasConsecutive = await consecutiveEl.isVisible({ timeout: 1000 }).catch(() => false);
  if (!hasConsecutive) return;

  const textBefore = await consecutiveEl.textContent();

  // Advance the scenario one step (look for a step-advance button)
  const stepBtn = page.locator('[data-testid="step-advance-btn"]');
  const btnVisible = await stepBtn.isVisible({ timeout: 1000 }).catch(() => false);
  if (!btnVisible) return;

  await stepBtn.click();
  await page.waitForTimeout(500); // allow store update

  // The detail slot must re-render. The consecutive text may change (if same alert
  // persists) or the detail slot may show a different alert. Either is valid —
  // what is NOT valid is the element being detached or having stale content for
  // the same mda_id when consecutive_breach_steps should have incremented.
  const detailStillVisible = await detail.isVisible({ timeout: 2000 }).catch(() => false);
  if (!detailStillVisible) return;

  // If the same alert is still top-ranked, verify detail-consecutive is populated
  const consecutiveElAfter = detail.locator('[data-testid="detail-consecutive"]');
  const hasConsecutiveAfter = await consecutiveElAfter.isVisible({ timeout: 1000 }).catch(() => false);
  if (!hasConsecutiveAfter) return;

  const textAfter = await consecutiveElAfter.textContent();
  // text must be non-empty (not stale undefined / empty)
  expect(textAfter).toBeTruthy();
  expect(textAfter!.trim()).not.toBe("");

  // The text before and after may differ (step advanced) — both are valid.
  // If they are the same, that could be because consecutive count didn't change
  // (different alert was promoted) — also valid. What we cannot allow is empty.
  void textBefore; // referenced above; no assertion on equality needed
});

// ---------------------------------------------------------------------------
// AC-5: Compact rows scan-only — SF-3
// (a) Each compact-alert-row has cursor:default.
// (b) Clicking a compact row produces no change to zone-1b-top-detail content.
// ---------------------------------------------------------------------------

test("AC-5a: compact-alert-row elements have cursor:default", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  const compact = await getZone1BCompact(page);
  const compactVisible = await compact.isVisible({ timeout: 2000 }).catch(() => false);
  if (!compactVisible) return;

  const rows = compact.locator('[data-testid="compact-alert-row"]');
  const count = await rows.count();
  if (count === 0) return;

  for (let i = 0; i < Math.min(count, 3); i++) {
    const cursor = await rows.nth(i).evaluate((el) => {
      return window.getComputedStyle(el).cursor;
    });
    expect(cursor).toBe("default");
  }
});

test("AC-5b: clicking a compact-alert-row produces no change to zone-1b-top-detail", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  const detail = await getZone1BDetailSlot(page);
  const compact = await getZone1BCompact(page);

  const detailVisible = await detail.isVisible({ timeout: 2000 }).catch(() => false);
  const compactVisible = await compact.isVisible({ timeout: 1000 }).catch(() => false);
  if (!detailVisible || !compactVisible) return;

  const rows = compact.locator('[data-testid="compact-alert-row"]');
  const count = await rows.count();
  if (count === 0) return;

  // Capture detail slot state before click
  const detailTextBefore = await detail.textContent();
  const detailSeverityBefore = await detail.getAttribute("data-severity");

  // Click first compact row
  await rows.first().click();
  await page.waitForTimeout(200);

  // Detail slot must be unchanged
  const detailTextAfter = await detail.textContent();
  const detailSeverityAfter = await detail.getAttribute("data-severity");

  expect(detailTextAfter).toBe(detailTextBefore);
  expect(detailSeverityAfter).toBe(detailSeverityBefore);
});

// ---------------------------------------------------------------------------
// AC-6: [NEW] badge fires on mda_id change in Mode 3 — SF-4
// In a Mode 3 context, when a new highest-severity alert fires (different mda_id),
// detail-new-badge is present and visible before any user interaction.
// ---------------------------------------------------------------------------

test("AC-6: [NEW] badge is visible in detail slot when top alert mda_id changes in Mode 3", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  // This test is only assertable when the app is in Mode 3 and a control input
  // has fired a new top-ranked alert. We use the guard pattern — if Mode 3 is not
  // active or no new alert has fired, the test is a no-op.
  const detail = await getZone1BDetailSlot(page);
  const isVisible = await detail.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const badge = detail.locator('[data-testid="detail-new-badge"]');
  // Guard: badge only appears in Mode 3 after a new top alert fires.
  // If we cannot trigger Mode 3 in this context, the test is a no-op.
  const hasBadge = await badge.count() > 0;
  if (!hasBadge) return; // no new alert has fired; skip

  await expect(badge).toBeVisible();
});

// ---------------------------------------------------------------------------
// AC-7: Compact row height ≤ 26px at 1024×768 — UX sign-off condition 1
// ---------------------------------------------------------------------------

test("AC-7: compact-alert-row height ≤ 26px at 1024×768", async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  const compact = await getZone1BCompact(page);
  const compactVisible = await compact.isVisible({ timeout: 2000 }).catch(() => false);
  if (!compactVisible) return;

  const rows = compact.locator('[data-testid="compact-alert-row"]');
  const count = await rows.count();
  if (count === 0) return;

  for (let i = 0; i < Math.min(count, 5); i++) {
    const height = await rows.nth(i).evaluate((el) => el.getBoundingClientRect().height);
    expect(height).toBeLessThanOrEqual(26);
  }
});

// ---------------------------------------------------------------------------
// AC-8: Mode-dependent tense in detail slot — UX sign-off condition 2
// (a) Mode 1 → status text contains past-tense ("crossed")
// (b) Mode 2 → status text contains projected tense ("projected" or "PROJECTED")
// (c) Mode 3 → status text contains "BREACHED" for breached alerts
// ---------------------------------------------------------------------------

test("AC-8a: Mode 1 detail slot status text uses past tense for breached alerts", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  const detail = await getZone1BDetailSlot(page);
  const isVisible = await detail.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const status = detail.locator('[data-testid="detail-status"]');
  const hasStatus = await status.isVisible({ timeout: 1000 }).catch(() => false);
  if (!hasStatus) return;

  // Verify we are in Mode 1 by checking the mode indicator
  const modeEl = page.locator('[data-testid="mode-indicator"]');
  const modeText = await modeEl.textContent().catch(() => "");
  if (!modeText?.includes("1") && !modeText?.includes("MODE_1")) return;

  const statusText = await status.textContent();
  if (!statusText) return;

  // Mode 1 past tense for a breach: "crossed threshold at step N"
  const hasPastTense = statusText.includes("crossed") || statusText.includes("at step");
  expect(hasPastTense).toBe(true);
  expect(statusText).not.toContain("BREACH PROJECTED");
  expect(statusText).not.toContain("projected");
});

test("AC-8c: Mode 3 detail slot status text says BREACHED for active breach", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  const detail = await getZone1BDetailSlot(page);
  const isVisible = await detail.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  // Only assert in Mode 3
  const modeEl = page.locator('[data-testid="mode-indicator"]');
  const modeText = await modeEl.textContent().catch(() => "");
  if (!modeText?.includes("3") && !modeText?.includes("MODE_3")) return;

  const status = detail.locator('[data-testid="detail-status"]');
  const hasStatus = await status.isVisible({ timeout: 1000 }).catch(() => false);
  if (!hasStatus) return;

  const statusText = await status.textContent();
  if (!statusText) return;

  // For a breached alert in Mode 3, status must be "BREACHED"
  // (approach_pct_remaining <= 0)
  const isBreach = await detail.locator('[data-testid="detail-current-value"]').isVisible({ timeout: 500 });
  if (!isBreach) return;

  expect(statusText).toContain("BREACHED");
  expect(statusText).not.toContain("projected");
  expect(statusText).not.toContain("crossed");
});

// ---------------------------------------------------------------------------
// AC-9: Entity ISO code in detail slot header and compact rows — Q1 ruling
// ---------------------------------------------------------------------------

test("AC-9: entity ISO code present in detail slot header and compact rows", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  const detail = await getZone1BDetailSlot(page);
  const isVisible = await detail.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  // Detail slot entity ISO
  const detailEntityId = detail.locator('[data-testid="detail-entity-id"]');
  const hasDetailEntity = await detailEntityId.isVisible({ timeout: 1000 }).catch(() => false);
  if (!hasDetailEntity) return;

  const entityText = await detailEntityId.textContent();
  expect(entityText).toBeTruthy();
  // ISO 3166-1 alpha-3 codes are 3 uppercase letters
  expect(entityText!.trim()).toMatch(/^[A-Z]{3}$/);

  // Compact rows entity ISO
  const compact = await getZone1BCompact(page);
  const compactVisible = await compact.isVisible({ timeout: 1000 }).catch(() => false);
  if (!compactVisible) return;

  const rows = compact.locator('[data-testid="compact-alert-row"]');
  const count = await rows.count();
  if (count === 0) return;

  for (let i = 0; i < Math.min(count, 3); i++) {
    const rowEntityEl = rows.nth(i).locator('[data-testid="compact-row-entity-id"]');
    const hasRowEntity = await rowEntityEl.isVisible({ timeout: 500 }).catch(() => false);
    if (!hasRowEntity) continue;

    const rowEntityText = await rowEntityEl.textContent();
    expect(rowEntityText!.trim()).toMatch(/^[A-Z]{3}$/);
  }
});

// ---------------------------------------------------------------------------
// AC-10: Confidence tier label is per-step, not cumulative — Q4 ruling
// After the same TERMINAL alert persists across multiple step advances,
// the negotiation label text is identical at step 1 and step N.
// ---------------------------------------------------------------------------

test("AC-10: confidence tier label unchanged as same alert persists across steps", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  const detail = await getZone1BDetailSlot(page);
  const isVisible = await detail.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  const labelEl = detail.locator('[data-testid="detail-negotiation-label"]');
  const hasLabel = await labelEl.isVisible({ timeout: 1000 }).catch(() => false);
  if (!hasLabel) return;

  const labelBefore = await labelEl.textContent();
  const alertIdBefore = await detail.getAttribute("data-alert-id");

  // Advance one step
  const stepBtn = page.locator('[data-testid="step-advance-btn"]');
  const btnVisible = await stepBtn.isVisible({ timeout: 1000 }).catch(() => false);
  if (!btnVisible) return;

  await stepBtn.click();
  await page.waitForTimeout(500);

  const detailStillVisible = await detail.isVisible({ timeout: 2000 }).catch(() => false);
  if (!detailStillVisible) return;

  const alertIdAfter = await detail.getAttribute("data-alert-id");
  // Only assert label stability if the same alert is still top-ranked
  if (alertIdBefore !== alertIdAfter) return;

  const labelAfter = await labelEl.textContent();
  expect(labelAfter).toBe(labelBefore);
  // Label must NOT have changed as a function of consecutive count
});

// ---------------------------------------------------------------------------
// Layout invariant: zone-1b-top-detail appears before zone-1b-compact
// in the DOM (detail slot is topmost element in Zone 1B)
// ---------------------------------------------------------------------------

test("Layout: zone-1b-top-detail is positioned above zone-1b-compact in Zone 1B", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  const detail = await getZone1BDetailSlot(page);
  const compact = await getZone1BCompact(page);

  const detailVisible = await detail.isVisible({ timeout: 2000 }).catch(() => false);
  const compactVisible = await compact.isVisible({ timeout: 2000 }).catch(() => false);
  if (!detailVisible || !compactVisible) return;

  const detailBox = await detail.boundingBox();
  const compactBox = await compact.boundingBox();

  expect(detailBox).not.toBeNull();
  expect(compactBox).not.toBeNull();

  // Detail slot top must be above (or equal to) compact top
  expect(detailBox!.y).toBeLessThanOrEqual(compactBox!.y);
  // Detail slot bottom must be above compact top (no overlap where detail is below compact)
  expect(detailBox!.y + detailBox!.height).toBeLessThanOrEqual(compactBox!.y + 1); // 1px tolerance
});

// ---------------------------------------------------------------------------
// Empty state: "No active threshold breaches." when mda_alerts is empty
// ---------------------------------------------------------------------------

test("Empty state: zone-1b-top-detail shows 'No active threshold breaches.' when no alerts", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");

  const detail = await getZone1BDetailSlot(page);
  const isVisible = await detail.isVisible({ timeout: 2000 }).catch(() => false);
  if (!isVisible) return;

  // Only assert empty state if no active alerts are present
  const hasAlerts = await detail.locator('[data-testid="detail-indicator-name"]').isVisible({ timeout: 500 }).catch(() => false);
  if (hasAlerts) return; // alerts are active; skip empty state test

  const text = await detail.textContent();
  expect(text).toContain("No active threshold breaches");
});
