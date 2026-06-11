/**
 * Vitest: ScenarioIdentityHeader — unit tests.
 *
 * Covers:
 *   #744 — persistent scenario identity header; formatStatus pure function
 *   #746 — formatMultiplierLabel: Mode 2 fiscal multiplier display
 *
 * These are unit tests of the pure functions exported from ScenarioIdentityHeader.tsx.
 * Playwright E2E tests covering DOM assertions live in tests/e2e/.
 */
import { describe, it, expect } from "vitest";
import { formatStatus, formatMultiplierLabel, formatEntityLabel } from "../ScenarioIdentityHeader";

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

// ---------------------------------------------------------------------------
// formatMultiplierLabel — Mode 2 fiscal multiplier strip label (#746)
// ---------------------------------------------------------------------------

describe("formatMultiplierLabel", () => {
  it("returns null when fiscalMultiplier is null", () => {
    expect(formatMultiplierLabel(null)).toBeNull();
  });

  it("returns null when fiscalMultiplier is undefined", () => {
    expect(formatMultiplierLabel(undefined)).toBeNull();
  });

  it("returns null when fiscalMultiplier is exactly 1.0 (no override)", () => {
    expect(formatMultiplierLabel(1.0)).toBeNull();
  });

  it("returns label when multiplier is 2.0", () => {
    const label = formatMultiplierLabel(2.0);
    expect(label).not.toBeNull();
    expect(label).toContain("×2.0");
  });

  it("returns label when multiplier is 0.5", () => {
    const label = formatMultiplierLabel(0.5);
    expect(label).not.toBeNull();
    expect(label).toContain("×0.5");
  });

  it("label contains 'Fiscal' keyword", () => {
    expect(formatMultiplierLabel(1.5)).toContain("Fiscal");
  });

  it("label rounds to one decimal place — 1.50 → '×1.5'", () => {
    const label = formatMultiplierLabel(1.5);
    expect(label).toContain("×1.5");
    expect(label).not.toContain("×1.50");
  });
});

// ---------------------------------------------------------------------------
// formatEntityLabel — multi-entity identity display (#754)
// ---------------------------------------------------------------------------

describe("formatEntityLabel", () => {
  it("empty array → empty string", () => {
    expect(formatEntityLabel([])).toBe("");
  });

  it("single entity → 'Entity: GRC'", () => {
    expect(formatEntityLabel(["GRC"])).toBe("Entity: GRC");
  });

  it("two entities → 'Entities: JOR, SAU'", () => {
    expect(formatEntityLabel(["JOR", "SAU"])).toBe("Entities: JOR, SAU");
  });

  it("three entities → plural label with all IDs", () => {
    const label = formatEntityLabel(["GRC", "DEU", "FRA"]);
    expect(label).toMatch(/^Entities:/);
    expect(label).toContain("GRC");
    expect(label).toContain("DEU");
    expect(label).toContain("FRA");
  });

  it("single entity uses singular 'Entity:' not 'Entities:'", () => {
    expect(formatEntityLabel(["GRC"])).not.toContain("Entities:");
  });

  it("two entities uses plural 'Entities:' not 'Entity:'", () => {
    expect(formatEntityLabel(["GRC", "DEU"])).not.toMatch(/^Entity:/);
  });
});
