/**
 * Vitest: CohortIndicatorsPanel — unit tests.
 *
 * Covers:
 *   #747 — Zone 1A cohort disaggregation; pure functions for direction,
 *           glyph rendering, and value formatting
 *
 * These are unit tests of pure functions exported from CohortIndicatorsPanel.tsx.
 * Playwright E2E tests covering DOM assertions live in tests/e2e/.
 */
import { describe, it, expect } from "vitest";
import {
  computeDirection,
  directionGlyph,
  formatIndicatorValue,
  PRIORITY_INDICATORS,
} from "../CohortIndicatorsPanel";
import type { QuantitySchema } from "../../types";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function qty(value: string, unit?: string, confidence_tier?: number): QuantitySchema {
  return {
    value,
    unit: unit ?? "fraction",
    variable_type: "stock",
    confidence_tier: confidence_tier ?? 2,
    observation_date: null,
    source_id: null,
  };
}

// ---------------------------------------------------------------------------
// computeDirection
// ---------------------------------------------------------------------------

describe("computeDirection", () => {
  it("returns null when current is undefined", () => {
    expect(computeDirection(undefined, qty("0.5"))).toBeNull();
  });

  it("returns null when prev is undefined", () => {
    expect(computeDirection(qty("0.5"), undefined)).toBeNull();
  });

  it("returns null when both are undefined", () => {
    expect(computeDirection(undefined, undefined)).toBeNull();
  });

  it("returns 'up' when current > prev", () => {
    expect(computeDirection(qty("0.6"), qty("0.4"))).toBe("up");
  });

  it("returns 'down' when current < prev", () => {
    expect(computeDirection(qty("0.3"), qty("0.5"))).toBe("down");
  });

  it("returns null when current === prev", () => {
    expect(computeDirection(qty("0.5"), qty("0.5"))).toBeNull();
  });

  it("returns null when value is non-finite", () => {
    expect(computeDirection(qty("NaN"), qty("0.5"))).toBeNull();
    expect(computeDirection(qty("0.5"), qty("Infinity"))).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// directionGlyph
// ---------------------------------------------------------------------------

describe("directionGlyph", () => {
  it("returns null when direction is null", () => {
    expect(directionGlyph(null, "higher_better")).toBeNull();
    expect(directionGlyph(null, "lower_better")).toBeNull();
  });

  it("up + higher_better → green arrow up (good)", () => {
    const g = directionGlyph("up", "higher_better");
    expect(g).not.toBeNull();
    expect(g!.symbol).toBe("↑");
    expect(g!.color).toBe("#2e7d32");
  });

  it("down + lower_better → green arrow down (good)", () => {
    const g = directionGlyph("down", "lower_better");
    expect(g).not.toBeNull();
    expect(g!.symbol).toBe("↓");
    expect(g!.color).toBe("#2e7d32");
  });

  it("up + lower_better → red arrow up (bad)", () => {
    const g = directionGlyph("up", "lower_better");
    expect(g).not.toBeNull();
    expect(g!.symbol).toBe("↑");
    expect(g!.color).toBe("#c62828");
  });

  it("down + higher_better → red arrow down (bad)", () => {
    const g = directionGlyph("down", "higher_better");
    expect(g).not.toBeNull();
    expect(g!.symbol).toBe("↓");
    expect(g!.color).toBe("#c62828");
  });

  it("good and bad states produce different colors", () => {
    const good = directionGlyph("up", "higher_better");
    const bad = directionGlyph("up", "lower_better");
    expect(good!.color).not.toBe(bad!.color);
  });
});

// ---------------------------------------------------------------------------
// formatIndicatorValue
// ---------------------------------------------------------------------------

describe("formatIndicatorValue", () => {
  it("returns '—' for undefined", () => {
    expect(formatIndicatorValue(undefined)).toBe("—");
  });

  it("returns '—' for non-finite value", () => {
    expect(formatIndicatorValue(qty("NaN"))).toBe("—");
  });

  it("fraction unit ≤ 1.0 → percentage string", () => {
    expect(formatIndicatorValue(qty("0.05", "fraction"))).toBe("5.0%");
    expect(formatIndicatorValue(qty("0.123", "fraction"))).toBe("12.3%");
  });

  it("ratio unit ≤ 1.0 → percentage string", () => {
    expect(formatIndicatorValue(qty("0.25", "ratio"))).toBe("25.0%");
  });

  it("index unit ≤ 1.0 → percentage string", () => {
    expect(formatIndicatorValue(qty("0.8", "index"))).toBe("80.0%");
  });

  it("large value (≥ 1000) → no decimal places", () => {
    expect(formatIndicatorValue(qty("12345", "count"))).toBe("12345");
  });

  it("small non-fraction value → two decimal places", () => {
    expect(formatIndicatorValue(qty("3.14159", "count"))).toBe("3.14");
  });

  it("fraction > 1.0 is NOT converted to percentage", () => {
    // value > 1 is not in the fraction conversion range
    const result = formatIndicatorValue(qty("1.5", "fraction"));
    expect(result).not.toContain("%");
  });
});

// ---------------------------------------------------------------------------
// PRIORITY_INDICATORS — Issue #826 (DEMO4-005)
// ---------------------------------------------------------------------------

describe("PRIORITY_INDICATORS", () => {
  it("includes bottom_quintile_consumption_capacity (primary M12 HCL signal)", () => {
    const keys = PRIORITY_INDICATORS.map((i) => i.key);
    expect(keys).toContain("bottom_quintile_consumption_capacity");
  });

  it("bottom_quintile_consumption_capacity is first (highest priority)", () => {
    expect(PRIORITY_INDICATORS[0].key).toBe("bottom_quintile_consumption_capacity");
  });

  it("bottom_quintile_consumption_capacity polarity is higher_better", () => {
    const entry = PRIORITY_INDICATORS.find(
      (i) => i.key === "bottom_quintile_consumption_capacity",
    );
    expect(entry?.direction).toBe("higher_better");
  });

  it("decreasing bottom_quintile_consumption_capacity shows red down arrow", () => {
    // Confirm the polarity × direction combination produces the expected bad signal.
    const glyph = directionGlyph("down", "higher_better");
    expect(glyph).not.toBeNull();
    expect(glyph!.symbol).toBe("↓");
    expect(glyph!.color).toBe("#c62828");
  });

  it("dimensionless unit value displays as decimal (not percentage)", () => {
    // bottom_quintile_consumption_capacity uses unit="dimensionless"
    const result = formatIndicatorValue(qty("-0.12", "dimensionless"));
    expect(result).not.toContain("%");
    expect(result).toBe("-0.12");
  });
});
