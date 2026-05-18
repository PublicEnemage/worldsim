/**
 * Unit tests for RadarChart null governance axis — ADR-005 Decision M8-5, Issue #315.
 *
 * Tests verify:
 *   1. Named constants match exact ADR-005 M8-5 values (text-drift guard).
 *   2. null composite_score produces null final_score (no filled polygon vertex).
 *   3. 0.0 composite_score produces 0.0 final_score (valid filled vertex at zero).
 *
 * Tests 2 and 3 encode the ADR-level constraint: null and 0.0 must produce
 * visually distinct renders. null → Recharts polygon gap (dashed). 0.0 → filled
 * polygon at zero. These are not interchangeable.
 */
import { describe, it, expect } from "vitest";
import {
  GOVERNANCE_IN_VALIDATION_LABEL,
  GOVERNANCE_IN_VALIDATION_TOOLTIP,
  computeFinalScore,
} from "../RadarChart";

// ---------------------------------------------------------------------------
// Named constant tests — ADR-005 Decision M8-5 text-drift guard
// ---------------------------------------------------------------------------

describe("GOVERNANCE_IN_VALIDATION_LABEL", () => {
  it("matches exact ADR-005 Decision M8-5 value", () => {
    expect(GOVERNANCE_IN_VALIDATION_LABEL).toBe("Governance — in validation");
  });
});

describe("GOVERNANCE_IN_VALIDATION_TOOLTIP", () => {
  it("matches exact ADR-005 Decision M8-5 value", () => {
    expect(GOVERNANCE_IN_VALIDATION_TOOLTIP).toBe(
      "Governance composite score is in validation. Promotion criteria: 0 of 5 met at M8. Target: M9. See §Framework Promotion Protocol in CODING_STANDARDS.md.",
    );
  });

  it("includes promotion criteria count", () => {
    expect(GOVERNANCE_IN_VALIDATION_TOOLTIP).toContain("0 of 5");
  });

  it("references M9 target milestone", () => {
    expect(GOVERNANCE_IN_VALIDATION_TOOLTIP).toContain("M9");
  });
});

// ---------------------------------------------------------------------------
// computeFinalScore — null vs 0.0 distinction (ADR-level constraint)
// ---------------------------------------------------------------------------

describe("computeFinalScore — null composite_score", () => {
  it("returns null for null composite_score (renders dashed, not filled polygon)", () => {
    // ADR-005 M8-5: null → Recharts polygon gap, no vertex drawn.
    // Returning null is what causes the 'dashed' (missing polygon vertex) render.
    const result = computeFinalScore(null, 1.0);
    expect(result).toBeNull();
  });

  it("returns null regardless of weight when composite_score is null", () => {
    expect(computeFinalScore(null, 0.5)).toBeNull();
    expect(computeFinalScore(null, 2.0)).toBeNull();
    expect(computeFinalScore(null, 0)).toBeNull();
  });
});

describe("computeFinalScore — 0.0 composite_score", () => {
  it("returns 0 for 0.0 composite_score (renders filled polygon vertex at zero)", () => {
    // ADR-005 M8-5: 0.0 is a valid score. Renders as filled polygon vertex at zero.
    // This is visually and semantically distinct from null.
    const result = computeFinalScore(0.0, 1.0);
    expect(result).toBe(0);
    expect(result).not.toBeNull();
  });
});

describe("computeFinalScore — active scores", () => {
  it("applies weight to non-null composite_score", () => {
    expect(computeFinalScore(0.5, 1.0)).toBe(0.5);
    expect(computeFinalScore(0.5, 2.0)).toBe(1.0);
  });

  it("caps at 1.0 (radar chart domain)", () => {
    expect(computeFinalScore(0.8, 2.0)).toBe(1.0);
    expect(computeFinalScore(1.5, 1.0)).toBe(1.0);
  });

  it("null and 0.0 produce distinct results — ADR-level constraint", () => {
    const nullResult = computeFinalScore(null, 1.0);
    const zeroResult = computeFinalScore(0.0, 1.0);
    expect(nullResult).toBeNull();
    expect(zeroResult).not.toBeNull();
    expect(nullResult).not.toBe(zeroResult);
  });
});
