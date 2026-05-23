/**
 * E2E: M9 Instrument Cluster — Zone-level integration tests (AC-001, AC-002).
 *
 * INTEGRATION GATE — requires all three implementation tasks complete:
 *   - Issue #460 (TrajectoryView)
 *   - Issue #461 (MDA Alert Panel)
 *   - Issue #462 (PMM + Four-Framework Current Position)
 *
 * These are Type 2 (integration-level) ACs: they are only satisfiable when all
 * four Zone 1 instruments coexist simultaneously. They cannot be tested by any
 * single component implementation in isolation.
 *
 * On-ship checklist (when #460 + #461 + #462 are all merged):
 *   1. Remove the test.skip() call from each test body below.
 *   2. Verify both tests pass against the running frontend.
 *   3. Confirm this file has no remaining skip annotations.
 *
 * Type 1 (component-level) ACs from the original instrument-cluster.spec.ts
 * have been distributed to each implementation issue. See Issue #473 for the
 * retrofit record and NM-017 in docs/process/near-miss-registry.md for context.
 *
 * Source documents:
 *   docs/frontend/fa-brief-m9-instrument-cluster.md §Named Acceptance Criteria
 *   docs/ux/user-stories-instrument-cluster-m9.md
 *
 * data-testid selectors required (added by implementing agents #460/#461/#462):
 *   zone-1a-trajectory     — TrajectoryView component root
 *   zone-1b-mda-alerts     — MDA Alert Panel component root
 *   zone-1c-pmm            — PMM Widget component root
 *   zone-1d-four-framework — Four-Framework Current Position component root
 */
import { test, expect } from "@playwright/test";

// ---------------------------------------------------------------------------
// AC-001: All four Zone 1 instruments visible without scroll at 1024×768
// Source: US-001; FA brief §Named Acceptance Criteria
// Type 2 — integration-level: requires #460 + #461 + #462
// ---------------------------------------------------------------------------

test("AC-001: four Zone 1 instruments visible at 1024×768 without scroll", async ({
  page,
}) => {
  // Integration gate: remove when #460, #461, #462 are all merged.
  test.skip();

  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto("/");

  // All four Zone 1 instruments must be in the viewport without any scroll
  // interaction. toBeInViewport() confirms the element is visible within the
  // current viewport bounds — no scroll required.
  await expect(
    page.locator('[data-testid="zone-1a-trajectory"]'),
  ).toBeInViewport();
  await expect(
    page.locator('[data-testid="zone-1b-mda-alerts"]'),
  ).toBeInViewport();
  await expect(page.locator('[data-testid="zone-1c-pmm"]')).toBeInViewport();
  await expect(
    page.locator('[data-testid="zone-1d-four-framework"]'),
  ).toBeInViewport();
});

// ---------------------------------------------------------------------------
// AC-002: All four Zone 1 instruments visible without scroll at 1280×800
// Source: US-002; FA brief §Named Acceptance Criteria
// Type 2 — integration-level: requires #460 + #461 + #462
// ---------------------------------------------------------------------------

test("AC-002: four Zone 1 instruments visible at 1280×800 without scroll", async ({
  page,
}) => {
  // Integration gate: remove when #460, #461, #462 are all merged.
  test.skip();

  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");

  await expect(
    page.locator('[data-testid="zone-1a-trajectory"]'),
  ).toBeInViewport();
  await expect(
    page.locator('[data-testid="zone-1b-mda-alerts"]'),
  ).toBeInViewport();
  await expect(page.locator('[data-testid="zone-1c-pmm"]')).toBeInViewport();
  await expect(
    page.locator('[data-testid="zone-1d-four-framework"]'),
  ).toBeInViewport();
});
