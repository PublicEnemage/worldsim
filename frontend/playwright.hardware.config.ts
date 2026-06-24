/**
 * Playwright configuration for hardware validation runs (@hardware-only tests).
 *
 * Differences from playwright.config.ts (CI):
 *   grep: /@hardware-only/   — runs only hardware-tagged tests (excluded from CI config)
 *   headless: true           — no display required on target hardware
 *   timeout: 60_000          — longer timeout for slower hardware
 *
 * Usage (from frontend/ directory):
 *   npx playwright test --config playwright.hardware.config.ts
 *
 * Current hardware-only tests:
 *   mv-002-hardware-validation.spec.ts — AC-009 Mode 3 render ≤ 100ms (no CPU throttle)
 *
 * Target hardware: ProBook (Intel i5-8265U, 4 cores, 8 GiB, Windows 11)
 * Results to be posted on Issue #550 and recorded in the G6 validation report.
 * Authority: M16-G6 sprint entry §3.1 MV-002; EX-001 (docs/compliance/exceptions.md).
 */
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  grep: /@hardware-only/,
  timeout: 60_000,
  reporter: [["list"]],
  use: {
    baseURL: "http://localhost:5173",
    headless: true,
    viewport: { width: 1280, height: 800 },
  },
  projects: [
    {
      name: "chromium",
      use: { browserName: "chromium", channel: "chrome" },
    },
  ],
});
