/**
 * Vitest: trajectoryViewModel — unit tests for extracted pure functions (M19-G5 #1522).
 *
 * Authored BEFORE implementation per intent document:
 *   docs/process/intents/M19-G5-2026-07-03-view-model-retrofit.md
 *
 * ACs covered:
 *   AC-1 — trajectoryViewModel.ts exports computeYDomain, computeDivergenceFill,
 *           getConfidenceBadgeVisible, mergeTrajectories, sliceToStepRange
 *   AC-3 — all existing pure-function behavior is preserved after extraction
 *   AC-4 — mergeTrajectories accepts optional visibleStepRange: [number, number]
 *           and returns only steps within [lo, hi] inclusive
 *   AC-5 — sliceToStepRange(data, range) filters MergedStepDatum[] by step_index
 *
 * AC-2 (TrajectoryView.tsx re-export) is covered implicitly: if TrajectoryView.tsx
 * re-exports from trajectoryViewModel.ts, the existing TrajectoryView.test.ts
 * continues to pass without change. No separate unit test needed here.
 *
 * AC-6 (no behavior regression) is covered by E2E suite.
 *
 * RED state: trajectoryViewModel.ts does not exist until #1522 implementation.
 * All imports below will fail at TypeScript build until the module is created.
 *
 * NM-056 rule: NO test.skip(), test.fixme(), or .only() patterns.
 */
import { describe, it, expect } from "vitest";
import type { TrajectoryResponse } from "../../store/scenarioStepStore";
import {
  computeYDomain,
  computeDivergenceFill,
  getConfidenceBadgeVisible,
  mergeTrajectories,
  sliceToStepRange,
  type MergedStepDatum,
} from "../trajectoryViewModel";

// ---------------------------------------------------------------------------
// Fixtures
// ---------------------------------------------------------------------------

function makeStep(stepIndex: number, score: number) {
  return {
    step_index: stepIndex,
    effective_from: `2020-0${stepIndex}-01`,
    step_event_label: null,
    step_significance: "ROUTINE" as const,
    frameworks: {
      financial: { composite_score: score, confidence_tier: 2, scoring_basis: "percentile_rank", ci_lower: null, ci_upper: null, band_method: null },
      human_development: { composite_score: score, confidence_tier: 2, scoring_basis: "percentile_rank", ci_lower: null, ci_upper: null, band_method: null },
      ecological: { composite_score: score, confidence_tier: 2, scoring_basis: "percentile_rank", ci_lower: null, ci_upper: null, band_method: null },
      governance: { composite_score: score, confidence_tier: 2, scoring_basis: "percentile_rank", ci_lower: null, ci_upper: null, band_method: null },
    },
  };
}

function makeMergedDatum(stepIndex: number): MergedStepDatum {
  return {
    step_index: stepIndex,
    effective_from: `2020-0${stepIndex}-01`,
    step_event_label: null,
    step_significance: "ROUTINE",
    financial_active: 0.60,
    financial_baseline: 0.55,
    human_development_active: 0.65,
    human_development_baseline: 0.60,
    ecological_active: 0.70,
    ecological_baseline: 0.68,
    governance_active: 0.50,
    governance_baseline: 0.48,
    financial_confidence_tier: 2,
    human_development_confidence_tier: 2,
    ecological_confidence_tier: 2,
    governance_confidence_tier: 2,
    financial_scoring_basis: "percentile_rank",
    human_development_scoring_basis: "percentile_rank",
    financial_ci_lower: null,
    financial_ci_upper: null,
    human_development_ci_lower: null,
    human_development_ci_upper: null,
    ecological_ci_lower: null,
    ecological_ci_upper: null,
    governance_ci_lower: null,
    governance_ci_upper: null,
    financial_band_method: null,
  };
}

// Cast to TrajectoryResponse — fixture omits optional/rarely-set fields (pmm, MDAFloor label/severity).
const TRAJECTORY_10_STEPS = {
  scenario_id: "test-scenario-001",
  entity_id: "ZMB",
  step_count: 10,
  steps: Array.from({ length: 10 }, (_, i) => makeStep(i + 1, 0.55 + i * 0.01)),
  mda_floors: [{ framework: "financial", floor_value: 0.40, label: "MDA floor", severity: "WARNING" }],
} as unknown as TrajectoryResponse;

const MERGED_10_STEPS: MergedStepDatum[] = Array.from({ length: 10 }, (_, i) => makeMergedDatum(i + 1));

// ---------------------------------------------------------------------------
// AC-1 — Module exports all required functions
// ---------------------------------------------------------------------------

describe("M19-G5 AC-1 — trajectoryViewModel exports", () => {
  it("exports computeYDomain as a function", () => {
    expect(typeof computeYDomain).toBe("function");
  });

  it("exports computeDivergenceFill as a function", () => {
    expect(typeof computeDivergenceFill).toBe("function");
  });

  it("exports getConfidenceBadgeVisible as a function", () => {
    expect(typeof getConfidenceBadgeVisible).toBe("function");
  });

  it("exports mergeTrajectories as a function", () => {
    expect(typeof mergeTrajectories).toBe("function");
  });

  it("exports sliceToStepRange as a function", () => {
    expect(typeof sliceToStepRange).toBe("function");
  });
});

// ---------------------------------------------------------------------------
// AC-3 — Preserved behavior: computeYDomain
// ---------------------------------------------------------------------------

describe("M19-G5 AC-3 — computeYDomain behavior preserved after extraction", () => {
  it("empty array returns [0, 1]", () => {
    expect(computeYDomain([])).toEqual([0, 1]);
  });

  it("single value — padding = 0.05 minimum; clamps to [0, 1]", () => {
    const [lo, hi] = computeYDomain([0.5]);
    expect(lo).toBe(0.45);
    expect(hi).toBe(0.55);
  });

  it("tightly clustered values — padding = max(0.05, range * 0.1)", () => {
    // range = 0.04; 0.04 * 0.1 = 0.004 < 0.05 → padding = 0.05
    const [lo, hi] = computeYDomain([0.58, 0.62]);
    expect(lo).toBeLessThan(0.58);
    expect(hi).toBeGreaterThan(0.62);
  });

  it("result clamped to [0, 1] — values near 0 do not produce negative lower bound", () => {
    const [lo] = computeYDomain([0.02, 0.03]);
    expect(lo).toBeGreaterThanOrEqual(0);
  });

  it("result clamped to [0, 1] — values near 1 do not produce upper bound > 1", () => {
    const [, hi] = computeYDomain([0.97, 0.99]);
    expect(hi).toBeLessThanOrEqual(1);
  });

  it("ZMB three-scenario tight-scoping: [0.540, 0.584, 0.628] produces narrow domain", () => {
    const [lo, hi] = computeYDomain([0.540, 0.584, 0.628]);
    // range = 0.088; padding = max(0.05, 0.088 * 0.1) = max(0.05, 0.0088) = 0.05
    expect(lo).toBeLessThan(0.540);
    expect(hi).toBeGreaterThan(0.628);
    // domain width should be ≈ 0.088 + 0.10 = ~0.188 — much smaller than 0.328 (before fix)
    expect(hi - lo).toBeLessThan(0.25);
  });
});

// ---------------------------------------------------------------------------
// AC-3 — Preserved behavior: computeDivergenceFill
// ---------------------------------------------------------------------------

describe("M19-G5 AC-3 — computeDivergenceFill behavior preserved after extraction", () => {
  it("returns false when either value is null", () => {
    expect(computeDivergenceFill(null, 0.5)).toBe(false);
    expect(computeDivergenceFill(0.5, null)).toBe(false);
    expect(computeDivergenceFill(null, null)).toBe(false);
  });

  it("returns false when |delta| <= 0.01", () => {
    expect(computeDivergenceFill(0.75, 0.74)).toBe(false);
    expect(computeDivergenceFill(0.75, 0.75)).toBe(false);
  });

  it("returns true when |delta| > 0.01", () => {
    expect(computeDivergenceFill(0.75, 0.73)).toBe(true);
    expect(computeDivergenceFill(0.60, 0.65)).toBe(true);
  });

  it("boundary: 0.76 - 0.75 in IEEE 754 = 0.010000...9; rounds to 0.01 → false (AC-010 contract)", () => {
    expect(computeDivergenceFill(0.76, 0.75)).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// AC-3 — Preserved behavior: getConfidenceBadgeVisible
// ---------------------------------------------------------------------------

describe("M19-G5 AC-3 — getConfidenceBadgeVisible behavior preserved after extraction", () => {
  it("tier 3 → false", () => {
    expect(getConfidenceBadgeVisible(3)).toBe(false);
  });

  it("tier 4 → true (boundary)", () => {
    expect(getConfidenceBadgeVisible(4)).toBe(true);
  });

  it("tier 5 → true", () => {
    expect(getConfidenceBadgeVisible(5)).toBe(true);
  });

  it("tier 1, 2 → false", () => {
    expect(getConfidenceBadgeVisible(1)).toBe(false);
    expect(getConfidenceBadgeVisible(2)).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// AC-4 — mergeTrajectories visibleStepRange filtering
// ---------------------------------------------------------------------------

describe("M19-G5 AC-4 — mergeTrajectories visibleStepRange parameter", () => {
  it("no visibleStepRange — returns all 10 steps", () => {
    const result = mergeTrajectories(TRAJECTORY_10_STEPS, null);
    expect(result).toHaveLength(10);
  });

  it("visibleStepRange [3, 7] — returns steps 3-7 inclusive (5 steps)", () => {
    const result = mergeTrajectories(TRAJECTORY_10_STEPS, null, [3, 7]);
    expect(result).toHaveLength(5);
    expect(result.map((d) => d.step_index)).toEqual([3, 4, 5, 6, 7]);
  });

  it("visibleStepRange [1, 1] — returns single step", () => {
    const result = mergeTrajectories(TRAJECTORY_10_STEPS, null, [1, 1]);
    expect(result).toHaveLength(1);
    expect(result[0].step_index).toBe(1);
  });

  it("visibleStepRange [1, 10] — returns all steps (full range)", () => {
    const result = mergeTrajectories(TRAJECTORY_10_STEPS, null, [1, 10]);
    expect(result).toHaveLength(10);
  });

  it("visibleStepRange beyond data bounds — clamps gracefully (returns available steps)", () => {
    const result = mergeTrajectories(TRAJECTORY_10_STEPS, null, [8, 15]);
    expect(result.every((d) => d.step_index >= 8)).toBe(true);
  });

  it("visibleStepRange undefined — returns all steps (backward compat)", () => {
    const result = mergeTrajectories(TRAJECTORY_10_STEPS, null, undefined);
    expect(result).toHaveLength(10);
  });

  it("merged data preserves step_index values within the range", () => {
    const result = mergeTrajectories(TRAJECTORY_10_STEPS, null, [5, 7]);
    const indices = result.map((d) => d.step_index);
    expect(indices).toContain(5);
    expect(indices).toContain(6);
    expect(indices).toContain(7);
    expect(indices).not.toContain(4);
    expect(indices).not.toContain(8);
  });
});

// ---------------------------------------------------------------------------
// AC-5 — sliceToStepRange pure function
// ---------------------------------------------------------------------------

describe("M19-G5 AC-5 — sliceToStepRange pure function", () => {
  it("empty array returns empty array", () => {
    expect(sliceToStepRange([], [3, 7])).toHaveLength(0);
  });

  it("[3, 7] returns only steps with step_index in [3, 7] inclusive", () => {
    const result = sliceToStepRange(MERGED_10_STEPS, [3, 7]);
    expect(result).toHaveLength(5);
    expect(result.map((d) => d.step_index)).toEqual([3, 4, 5, 6, 7]);
  });

  it("[1, 10] returns all 10 items (full range)", () => {
    expect(sliceToStepRange(MERGED_10_STEPS, [1, 10])).toHaveLength(10);
  });

  it("[5, 5] returns single item (single step)", () => {
    const result = sliceToStepRange(MERGED_10_STEPS, [5, 5]);
    expect(result).toHaveLength(1);
    expect(result[0].step_index).toBe(5);
  });

  it("does not mutate the original array", () => {
    const original = [...MERGED_10_STEPS];
    sliceToStepRange(MERGED_10_STEPS, [3, 7]);
    expect(MERGED_10_STEPS).toHaveLength(original.length);
  });

  it("[0, Infinity] returns all items", () => {
    expect(sliceToStepRange(MERGED_10_STEPS, [0, Infinity])).toHaveLength(10);
  });

  it("range beyond data — returns only steps that exist in range", () => {
    const result = sliceToStepRange(MERGED_10_STEPS, [8, 20]);
    expect(result.every((d) => d.step_index >= 8)).toBe(true);
    expect(result.length).toBe(3); // steps 8, 9, 10
  });
});
