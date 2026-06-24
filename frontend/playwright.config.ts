import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 30_000,
  // HTML report always generated; never auto-opens (required for CI / Docker).
  // List reporter provides per-test stdout lines in GitHub Actions log output.
  reporter: [["html", { open: "never" }], ["list"]],
  // Exclude @demo tests from CI — they require a live stack and TTS narration.
  // Exclude @hardware-only tests from CI — they must run on target hardware without
  // CPU throttle (MV-002 pattern). Run explicitly: npx playwright test --grep @hardware-only
  // The demo config (playwright.demo.config.ts) runs @demo tests explicitly.
  grep: /^(?!.*(@demo|@hardware-only))/,
  use: {
    baseURL: "http://localhost:5173",
    headless: true,
    viewport: { width: 1280, height: 720 },
  },
  projects: [
    {
      name: "chromium",
      // channel: "chrome" uses the system-installed Google Chrome instead of
      // downloading Playwright's Chromium build. GitHub Actions ubuntu-latest
      // runners have Chrome pre-installed; local dev machines typically do too.
      // This eliminates the ~60-minute free-tier CDN download from CI.
      use: { browserName: "chromium", channel: "chrome" },
    },
  ],
});
