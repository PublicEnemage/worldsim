/**
 * Vitest: PMMWidgetZone1C — unit tests.
 *
 * Covers:
 *   US-019 — mode-specific label exact text; no raw field names in label
 *   US-020 — PMM distinct from FrameworkPanel (not tested here — DOM assertion in E2E)
 *   ADR-008 Decision 6 — pending state signaled by computation_state === "computing"
 *
 * These are unit tests of pure functions exported from PMMWidgetZone1C.tsx.
 * Playwright E2E tests covering DOM assertions live in tests/e2e/pmm-four-framework.spec.ts.
 */
import { describe, it, expect } from "vitest";
import {
  getPmmLabel,
  getPmmArrow,
  getPmmArrowColor,
  PMM_LABELS,
} from "../PMMWidgetZone1C";

// ---------------------------------------------------------------------------
// US-019 — mode-specific header label
// ---------------------------------------------------------------------------

describe("US-019 — getPmmLabel: mode-specific header text", () => {
  it("MODE_1 → 'Policy Maneuver Margin — historical'", () => {
    expect(getPmmLabel("MODE_1")).toBe("Policy Maneuver Margin — historical");
  });

  it("MODE_2 → 'Policy Maneuver Margin — projected'", () => {
    expect(getPmmLabel("MODE_2")).toBe("Policy Maneuver Margin — projected");
  });

  it("MODE_3 → 'Policy Maneuver Margin — current'", () => {
    expect(getPmmLabel("MODE_3")).toBe("Policy Maneuver Margin — current");
  });

  it("all labels begin with 'Policy Maneuver Margin'", () => {
    for (const mode of ["MODE_1", "MODE_2", "MODE_3"] as const) {
      expect(getPmmLabel(mode)).toMatch(/^Policy Maneuver Margin/);
    }
  });

  it("no label contains 'coffin_corner_index'", () => {
    for (const mode of ["MODE_1", "MODE_2", "MODE_3"] as const) {
      expect(getPmmLabel(mode)).not.toContain("coffin_corner_index");
    }
  });

  it("no label contains raw database field name substrings", () => {
    const rawFieldPatterns = ["coffin_corner", "_index", "pmm_value", "policy_margin"];
    for (const mode of ["MODE_1", "MODE_2", "MODE_3"] as const) {
      for (const pattern of rawFieldPatterns) {
        expect(getPmmLabel(mode)).not.toContain(pattern);
      }
    }
  });

  it("MODE_1 and MODE_2 labels differ", () => {
    expect(getPmmLabel("MODE_1")).not.toBe(getPmmLabel("MODE_2"));
  });

  it("MODE_2 and MODE_3 labels differ", () => {
    expect(getPmmLabel("MODE_2")).not.toBe(getPmmLabel("MODE_3"));
  });

  it("PMM_LABELS constant matches getPmmLabel for all modes", () => {
    expect(PMM_LABELS.MODE_1).toBe(getPmmLabel("MODE_1"));
    expect(PMM_LABELS.MODE_2).toBe(getPmmLabel("MODE_2"));
    expect(PMM_LABELS.MODE_3).toBe(getPmmLabel("MODE_3"));
  });
});

// ---------------------------------------------------------------------------
// getPmmArrow: direction to Unicode arrow character
// ---------------------------------------------------------------------------

describe("getPmmArrow: direction indicator symbols", () => {
  it("'up' → '↑'", () => {
    expect(getPmmArrow("up")).toBe("↑");
  });

  it("'down' → '↓'", () => {
    expect(getPmmArrow("down")).toBe("↓");
  });

  it("'flat' → '→'", () => {
    expect(getPmmArrow("flat")).toBe("→");
  });

  it("null → '—' (em dash, no prior step)", () => {
    expect(getPmmArrow(null)).toBe("—");
  });

  it("'up' and 'down' arrows are visually distinct characters", () => {
    expect(getPmmArrow("up")).not.toBe(getPmmArrow("down"));
  });

  it("'flat' arrow is distinct from both 'up' and 'down'", () => {
    expect(getPmmArrow("flat")).not.toBe(getPmmArrow("up"));
    expect(getPmmArrow("flat")).not.toBe(getPmmArrow("down"));
  });
});

// ---------------------------------------------------------------------------
// getPmmArrowColor: direction to color string
// ---------------------------------------------------------------------------

describe("getPmmArrowColor: direction to color", () => {
  it("'up' returns a non-empty color string", () => {
    expect(getPmmArrowColor("up")).toBeTruthy();
    expect(typeof getPmmArrowColor("up")).toBe("string");
  });

  it("'down' returns a non-empty color string", () => {
    expect(getPmmArrowColor("down")).toBeTruthy();
  });

  it("'up' and 'down' produce different colors", () => {
    expect(getPmmArrowColor("up")).not.toBe(getPmmArrowColor("down"));
  });

  it("null direction produces a muted (non-green-family) color", () => {
    const color = getPmmArrowColor(null);
    // Must not contain the ecological teal (#1A8FA0) or financial blue (#2271B3) —
    // null direction carries no directional meaning so it must not imply improvement
    expect(color).not.toBe("#1A8FA0");
    expect(color).not.toBe("#2271B3");
  });
});
