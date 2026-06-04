/**
 * M11.5 Pillar 2 session runner — infrastructure validation
 * Navigates the session URL, takes screenshots at key moments, ends the session.
 * Usage: node scripts/run-session.js <session_id>
 */
const { chromium } = require("playwright");
const path = require("path");
const fs = require("fs");

const SESSION_ID = process.argv[2] || "2026-06-04-persona-2-001";
const PERSONA = process.argv[3] || "persona-2";
const USE_CASE = process.argv[4] || "IMF+loan+evaluation";
const SCENARIO_ID = process.argv[5] || null;
const SESSION_URL = `http://localhost:5173/?usability_session=${SESSION_ID}&persona=${PERSONA}&use_case=${USE_CASE}${SCENARIO_ID ? `&scenario=${SCENARIO_ID}` : ""}`;
const SCREENSHOT_DIR = path.join(__dirname, "../session-screenshots");

fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });

async function screenshot(page, name, label) {
  const file = path.join(SCREENSHOT_DIR, `${SESSION_ID}-${String(name).padStart(2, "0")}-${label}.png`);
  await page.screenshot({ path: file, fullPage: false });
  console.log(`[screenshot] ${file}`);
  return file;
}

async function elapsed(startMs) {
  const s = Math.floor((Date.now() - startMs) / 1000);
  return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
}

(async () => {
  const browser = await chromium.launch({ headless: true, channel: "chrome" });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  console.log(`\nSession: ${SESSION_ID}`);
  console.log(`URL: ${SESSION_URL}\n`);

  const startMs = Date.now();

  // Step 1 — Land on session URL
  await page.goto(SESSION_URL, { waitUntil: "networkidle", timeout: 20000 });
  // Extra wait when scenario pre-loaded via URL param — trajectory fetch takes ~2s
  if (SCENARIO_ID) await page.waitForTimeout(3000);
  await screenshot(page, 1, "landing");
  console.log(`[${await elapsed(startMs)}] Landing page loaded`);

  // Step 2 — Check recording banner is visible
  const banner = await page.locator('[data-testid="session-recording-banner"]').isVisible().catch(() => false);
  console.log(`[${await elapsed(startMs)}] Recording banner visible: ${banner}`);

  // Step 3 — Look at the scenario list
  await page.waitForTimeout(1500);
  await screenshot(page, 2, "scenario-list");
  console.log(`[${await elapsed(startMs)}] Scenario list state captured`);

  // Step 4 — Find a Greece-related scenario and click it
  const greeceCard = page.locator("text=Greece").first();
  const greeceVisible = await greeceCard.isVisible().catch(() => false);
  console.log(`[${await elapsed(startMs)}] Greece scenario visible: ${greeceVisible}`);

  // Skip manual click when scenario pre-loaded via URL param — auto-loaded on mount
  if (greeceVisible && !SCENARIO_ID) {
    await greeceCard.click();
    await page.waitForTimeout(2000);
    await screenshot(page, 3, "after-greece-click");
    console.log(`[${await elapsed(startMs)}] Clicked Greece scenario`);
  } else if (SCENARIO_ID) {
    console.log(`[${await elapsed(startMs)}] Scenario pre-loaded via URL param — skipping click`);
    await page.waitForTimeout(2000);
    await screenshot(page, 3, "scenario-preloaded");
  }

  // Step 5 — Look for instrument cluster / Zone 1A
  const zone1a = await page.locator('[data-testid="zone-1a-trajectory"]').isVisible().catch(() => false);
  console.log(`[${await elapsed(startMs)}] Zone 1A trajectory visible: ${zone1a}`);
  await screenshot(page, 4, "instrument-cluster");

  // Step 6 — Look for MDA alerts in Zone 1B
  const zone1b = await page.locator('[data-testid="zone-1b-mda-alerts"]').isVisible().catch(() => false);
  console.log(`[${await elapsed(startMs)}] Zone 1B MDA alerts visible: ${zone1b}`);

  // Step 7 — Look for PMM in Zone 1C
  const pmmValue = await page.locator('[data-testid="pmm-value"]').isVisible().catch(() => false);
  const pmmBreached = await page.locator('[data-testid="pmm-breached-note"]').isVisible().catch(() => false);
  console.log(`[${await elapsed(startMs)}] PMM value visible: ${pmmValue}, breached note: ${pmmBreached}`);

  // Step 8 — Look for Zone 1D framework scores
  const zone1d = await page.locator('[data-testid="zone-1d-error"]').isVisible().catch(() => false);
  console.log(`[${await elapsed(startMs)}] Zone 1D error state: ${zone1d}`);

  // Step 9 — Try to advance a step if the button is available
  const advanceBtn = page.locator('[data-testid="advance-step-btn"]');
  const advanceVisible = await advanceBtn.isVisible().catch(() => false);
  console.log(`[${await elapsed(startMs)}] Advance step button visible: ${advanceVisible}`);

  if (advanceVisible) {
    const disabled = await advanceBtn.isDisabled().catch(() => true);
    console.log(`[${await elapsed(startMs)}] Advance step button disabled: ${disabled}`);
    if (!disabled) {
      // Use force:true to bypass fixed banner intercept
      await advanceBtn.click({ force: true }).catch(() => null);
      await page.waitForTimeout(3000);
      await screenshot(page, 5, "after-advance");
      console.log(`[${await elapsed(startMs)}] Advanced one step`);
    }
  }

  // Step 10 — Scroll down to look for Zone 2 content
  await page.evaluate(() => window.scrollBy(0, 400));
  await page.waitForTimeout(1000);
  await screenshot(page, 6, "zone2-scroll");
  console.log(`[${await elapsed(startMs)}] Scrolled to Zone 2`);

  // Step 11 — Scroll back up, capture final Zone 1 state
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(500);
  await screenshot(page, 7, "final-zone1-state");
  console.log(`[${await elapsed(startMs)}] Final Zone 1 state captured`);

  // Step 12 — Click End Session
  const endBtn = page.locator('[data-testid="end-session-btn"]');
  const endVisible = await endBtn.isVisible().catch(() => false);
  console.log(`[${await elapsed(startMs)}] End Session button visible: ${endVisible}`);

  if (endVisible) {
    await endBtn.click();
    await page.waitForTimeout(3000);
    await screenshot(page, 8, "after-end-session");
    console.log(`[${await elapsed(startMs)}] End Session clicked`);
  }

  // Step 13 — Check banner turned green
  const bannerText = await page.locator('[data-testid="session-recording-banner"]').textContent().catch(() => "");
  console.log(`[${await elapsed(startMs)}] Banner text after end: "${bannerText.trim().slice(0, 80)}"`);

  const durationMs = Date.now() - startMs;
  console.log(`\nSession complete. Duration: ${Math.round(durationMs / 1000)}s`);
  console.log(`Screenshots: ${SCREENSHOT_DIR}`);

  await browser.close();
})();
