/**
 * Playwright configuration for the live stakeholder demo walkthrough.
 *
 * Differences from playwright.config.ts (CI):
 *   headless: false          — browser window is visible so the presenter can narrate
 *   slowMo: 800              — 800 ms between every action (~0.8× natural interaction pace)
 *   timeout: 60_000          — longer per-step timeout for live presenter pauses
 *   --start-fullscreen       — Chromium enters fullscreen on launch; hides the address
 *                              bar, tab strip, and OS chrome so recordings show only the
 *                              application. On macOS this is the native fullscreen mode.
 *
 * Invoked by scripts/demo.sh --run, or directly:
 *   cd frontend && npx playwright test tests/e2e/demo-narrated.spec.ts \
 *     --config playwright.demo.config.ts --headed
 */
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 60_000,
  reporter: [["list"]],
  use: {
    baseURL: "http://localhost:5173",
    headless: false,
    slowMo: 800,
    viewport: { width: 1440, height: 900 },
  },
  projects: [
    {
      name: "chromium",
      use: {
        browserName: "chromium",
        launchOptions: {
          // --start-fullscreen hides address bar and OS chrome for clean recordings.
          // --hide-crash-restore-bubble suppresses the session-restore prompt that
          // appears after a prior run was killed mid-session.
          args: ["--start-fullscreen", "--hide-crash-restore-bubble"],
        },
      },
    },
  ],
});
