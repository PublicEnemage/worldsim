/**
 * Vitest: ScenarioIdentityHeader — unit tests.
 *
 * Covers:
 *   #744 — persistent scenario identity header; formatStatus pure function
 *
 * These are unit tests of the pure function exported from ScenarioIdentityHeader.tsx.
 * Playwright E2E tests covering DOM assertions live in tests/e2e/.
 */
import { describe, it, expect } from "vitest";
import { formatStatus } from "../ScenarioIdentityHeader";

// ---------------------------------------------------------------------------
// formatStatus — step-to-label mapping
// ---------------------------------------------------------------------------

describe("formatStatus", () => {
  it("null step → 'Ready'", () => {
    expect(formatStatus(null, 3)).toBe("Ready");
  });

  it("step 0 → 'Ready'", () => {
    expect(formatStatus(0, 3)).toBe("Ready");
  });

  it("mid-scenario step → 'Step N of M'", () => {
    expect(formatStatus(1, 3)).toBe("Step 1 of 3");
    expect(formatStatus(2, 3)).toBe("Step 2 of 3");
  });

  it("step equals totalSteps → 'Complete (M steps)'", () => {
    expect(formatStatus(3, 3)).toBe("Complete (3 steps)");
  });

  it("step exceeds totalSteps → 'Complete (M steps)'", () => {
    expect(formatStatus(5, 3)).toBe("Complete (3 steps)");
  });

  it("single-step scenario complete → 'Complete (1 steps)'", () => {
    expect(formatStatus(1, 1)).toBe("Complete (1 steps)");
  });

  it("does not include raw null in output", () => {
    const s = formatStatus(null, 5);
    expect(s).not.toContain("null");
  });
});
