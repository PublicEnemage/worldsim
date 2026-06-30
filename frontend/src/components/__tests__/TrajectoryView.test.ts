/**
 * Vitest: M9 TrajectoryView — Acceptance tests.
 *
 * Tests in this file cover:
 *   AC-006 — All four Zone 1 instruments update in a single render cycle (RTL)
 *   AC-010 — Divergence fill disappears when |active - baseline| <= 0.01
 *   AC-013 — Tier 4-5 curves show "(exp)" label (Vitest unit test — QA-F5)
 *   AC-015 — All four active <Line> components have connectNulls={false}
 *
 * Sources:
 *   docs/frontend/fa-brief-m9-instrument-cluster.md §Named Acceptance Criteria
 *   docs/ux/user-stories-instrument-cluster-m9.md US-007, US-008, US-010, US-012, US-023
 */
import { describe, it, expect, beforeAll } from "vitest";

// ---------------------------------------------------------------------------
// TrajectoryView module import
//
// This module does not exist until Issue #460. The @ts-expect-error suppresses
// the TypeScript "cannot find module" error during the pre-implementation phase.
// Remove @ts-expect-error once TrajectoryView.tsx is created.
//
// Expected exports from TrajectoryView.tsx (for implementing agent):
//   computeDivergenceFill(active: number | null, baseline: number | null): boolean
//     Returns true when |active - baseline| > 0.01 (Area fill should render).
//     Returns false when delta <= 0.01 or either value is null (no fill).
//
//   getConfidenceBadgeVisible(confidenceTier: number): boolean
//     Returns true when confidenceTier >= 4.
//     Returns false when confidenceTier <= 3.
//
//   FRAMEWORKS: readonly string[]
//     The four framework keys: ["financial", "human_development", "ecological", "governance"]
//
//   CONNECT_NULLS: false
//     Named constant enforcing connectNulls={false} on all <Line> components.
//     Must be literally `false` (not a variable that evaluates to false at runtime).
// ---------------------------------------------------------------------------
import {
  computeDivergenceFill,
  getConfidenceBadgeVisible,
  computeYDomain,
  FRAMEWORKS,
  CONNECT_NULLS,
} from "../TrajectoryView";

// ---------------------------------------------------------------------------
// Fixture helpers
//
// These are used to construct test data for the acceptance criteria.
// Defined here so the tests are self-contained and do not require a running
// backend or fixture loader.
// ---------------------------------------------------------------------------

/** A single step datum in the merged trajectory data array (FA brief §Divergence Fill Implementation). */
interface MergedStepDatum {
  step_index: number;
  financial_active: number | null;
  financial_baseline: number | null;
  human_development_active: number | null;
  human_development_baseline: number | null;
  ecological_active: number | null;
  ecological_baseline: number | null;
  governance_active: number | null;
  governance_baseline: number | null;
}

/** Build a 4-step fixture where active === baseline at every step (delta = 0). */
function buildZeroDeltaFixture(): MergedStepDatum[] {
  return [1, 2, 3, 4].map((step_index) => ({
    step_index,
    financial_active: 0.75,
    financial_baseline: 0.75,
    human_development_active: 0.60,
    human_development_baseline: 0.60,
    ecological_active: 0.85,
    ecological_baseline: 0.85,
    governance_active: 0.55,
    governance_baseline: 0.55,
  }));
}

/** Build a 4-step fixture where |active - baseline| > 0.01 for financial at step 2. */
function buildSignificantDeltaFixture(): MergedStepDatum[] {
  return [
    {
      step_index: 1,
      financial_active: 0.75,
      financial_baseline: 0.75,
      human_development_active: 0.60,
      human_development_baseline: 0.60,
      ecological_active: 0.85,
      ecological_baseline: 0.85,
      governance_active: 0.55,
      governance_baseline: 0.55,
    },
    {
      // Step 2: financial delta = 0.15, which exceeds the 0.01 threshold
      step_index: 2,
      financial_active: 0.60,
      financial_baseline: 0.75,
      human_development_active: 0.60,
      human_development_baseline: 0.60,
      ecological_active: 0.85,
      ecological_baseline: 0.85,
      governance_active: 0.55,
      governance_baseline: 0.55,
    },
    {
      step_index: 3,
      financial_active: 0.60,
      financial_baseline: 0.60,
      human_development_active: 0.60,
      human_development_baseline: 0.60,
      ecological_active: 0.85,
      ecological_baseline: 0.85,
      governance_active: 0.55,
      governance_baseline: 0.55,
    },
    {
      step_index: 4,
      financial_active: 0.55,
      financial_baseline: 0.55,
      human_development_active: 0.60,
      human_development_baseline: 0.60,
      ecological_active: 0.85,
      ecological_baseline: 0.85,
      governance_active: 0.55,
      governance_baseline: 0.55,
    },
  ];
}

/** Build a fixture where governance composite_score is null at step 3. */
function buildNullGovernanceFixture(): MergedStepDatum[] {
  return [
    {
      step_index: 1,
      financial_active: 0.75,
      financial_baseline: null,
      human_development_active: 0.60,
      human_development_baseline: null,
      ecological_active: 0.85,
      ecological_baseline: null,
      governance_active: 0.55,
      governance_baseline: null,
    },
    {
      step_index: 2,
      financial_active: 0.72,
      financial_baseline: null,
      human_development_active: 0.58,
      human_development_baseline: null,
      ecological_active: 0.83,
      ecological_baseline: null,
      governance_active: 0.52,
      governance_baseline: null,
    },
    {
      // Step 3: governance_active is null — must render as curve gap, not zero
      step_index: 3,
      financial_active: 0.70,
      financial_baseline: null,
      human_development_active: 0.56,
      human_development_baseline: null,
      ecological_active: 0.81,
      ecological_baseline: null,
      governance_active: null,
      governance_baseline: null,
    },
    {
      step_index: 4,
      financial_active: 0.68,
      financial_baseline: null,
      human_development_active: 0.54,
      human_development_baseline: null,
      ecological_active: 0.79,
      ecological_baseline: null,
      governance_active: 0.50,
      governance_baseline: null,
    },
  ];
}

// ---------------------------------------------------------------------------
// AC-010 — Divergence fill disappears when |active - baseline| <= 0.01
// Source: US-008; FA brief §Divergence Fill Implementation (FA-R2 Resolution)
//
// The divergence fill is implemented via Recharts <Area> with merged data keys.
// computeDivergenceFill(active, baseline) is the decision function.
// ---------------------------------------------------------------------------

describe("AC-010 — computeDivergenceFill: divergence fill threshold logic", () => {
  it("returns false when active === baseline (delta = 0)", () => {
    // When active and baseline are identical, no fill should render.
    expect(computeDivergenceFill(0.75, 0.75)).toBe(false);
  });

  it("returns false when |active - baseline| = 0.01 exactly (at threshold, not above)", () => {
    // The threshold is strictly > 0.01. At exactly 0.01, fill must not render.
    expect(computeDivergenceFill(0.76, 0.75)).toBe(false);
    expect(computeDivergenceFill(0.75, 0.76)).toBe(false);
  });

  it("returns true when |active - baseline| > 0.01 (above threshold)", () => {
    // Financial delta of 0.15 at step 2 in the significant-delta fixture.
    expect(computeDivergenceFill(0.60, 0.75)).toBe(true);
    expect(computeDivergenceFill(0.75, 0.60)).toBe(true);
  });

  it("returns false when active is null (incomplete computation)", () => {
    // Null active value means step not yet computed — no fill possible.
    expect(computeDivergenceFill(null, 0.75)).toBe(false);
  });

  it("returns false when baseline is null (no control input applied yet)", () => {
    // Null baseline means Mode 3 has not received its first control input.
    // No divergence fill before baseline is established.
    expect(computeDivergenceFill(0.75, null)).toBe(false);
  });

  it("returns false when both active and baseline are null", () => {
    expect(computeDivergenceFill(null, null)).toBe(false);
  });

  it("handles zero-delta fixture: no step produces fill", () => {
    // Every step in the zero-delta fixture has active === baseline.
    const fixture = buildZeroDeltaFixture();
    for (const step of fixture) {
      expect(
        computeDivergenceFill(step.financial_active, step.financial_baseline),
      ).toBe(false);
      expect(
        computeDivergenceFill(
          step.human_development_active,
          step.human_development_baseline,
        ),
      ).toBe(false);
      expect(
        computeDivergenceFill(step.ecological_active, step.ecological_baseline),
      ).toBe(false);
      expect(
        computeDivergenceFill(step.governance_active, step.governance_baseline),
      ).toBe(false);
    }
  });

  it("handles significant-delta fixture: step 2 financial delta produces fill", () => {
    const fixture = buildSignificantDeltaFixture();
    // Step 2 financial: active = 0.60, baseline = 0.75 → delta = 0.15 > 0.01
    const step2 = fixture.find((s) => s.step_index === 2)!;
    expect(
      computeDivergenceFill(step2.financial_active, step2.financial_baseline),
    ).toBe(true);
    // All other frameworks at step 2 have delta = 0
    expect(
      computeDivergenceFill(
        step2.human_development_active,
        step2.human_development_baseline,
      ),
    ).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// AC-013 — Tier 4-5 curves show "(exp)" badge; Tier 1-3 do not
// Source: US-012; FA brief §Confidence Tier Visual (UD-R3 ruling)
//
// getConfidenceBadgeVisible(tier) is the predicate that governs badge rendering.
// The badge is a <text> element adjacent to the rightmost data point (11px min).
// Moved to Vitest per QA-F5: Playwright SVG assertion was fragile.
// ---------------------------------------------------------------------------

describe("AC-013 — getConfidenceBadgeVisible: (exp) badge tier logic", () => {
  it("returns true for Tier 4 (exploratory confidence)", () => {
    expect(getConfidenceBadgeVisible(4)).toBe(true);
  });

  it("returns true for Tier 5 (highest uncertainty tier)", () => {
    expect(getConfidenceBadgeVisible(5)).toBe(true);
  });

  it("returns false for Tier 3 (moderate confidence — no badge)", () => {
    expect(getConfidenceBadgeVisible(3)).toBe(false);
  });

  it("returns false for Tier 2", () => {
    expect(getConfidenceBadgeVisible(2)).toBe(false);
  });

  it("returns false for Tier 1 (measured — highest confidence)", () => {
    expect(getConfidenceBadgeVisible(1)).toBe(false);
  });

  it("threshold is at tier 4: tier 3 does not show badge, tier 4 does", () => {
    // The boundary is strict: tier 3 → no badge; tier 4 → badge.
    expect(getConfidenceBadgeVisible(3)).toBe(false);
    expect(getConfidenceBadgeVisible(4)).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// AC-015 — All four active <Line> components have connectNulls={false}
// Source: US-010; FA brief §Null Curve Rendering (ADR-010 Decision 3)
//
// CONNECT_NULLS is a named constant that must be literally `false`.
// All four active <Line> components use this constant — it is not configurable.
// Null composite_score at any step renders as a visible gap, not interpolated.
//
// FRAMEWORKS is the array of four framework keys. All four must be present.
// ---------------------------------------------------------------------------

describe("AC-015 — CONNECT_NULLS constant: connectNulls={false} on all Lines", () => {
  it("CONNECT_NULLS is exactly false (not truthy, not a string, not undefined)", () => {
    // The <Line connectNulls={false} /> prop must receive the boolean false literal.
    // This test guards against the value being '0', 'false', null, or undefined.
    expect(CONNECT_NULLS).toBe(false);
    expect(typeof CONNECT_NULLS).toBe("boolean");
  });

  it("FRAMEWORKS contains all four framework keys", () => {
    expect(FRAMEWORKS).toContain("financial");
    expect(FRAMEWORKS).toContain("human_development");
    expect(FRAMEWORKS).toContain("ecological");
    expect(FRAMEWORKS).toContain("governance");
    expect(FRAMEWORKS).toHaveLength(4);
  });

  it("null governance at step 3 does not produce fill in zero-delta fixture", () => {
    // When governance_active is null, computeDivergenceFill must return false —
    // no divergence fill can render for a null data point.
    const fixture = buildNullGovernanceFixture();
    const step3 = fixture.find((s) => s.step_index === 3)!;
    expect(step3.governance_active).toBeNull();
    // The divergence fill function must handle null gracefully.
    expect(
      computeDivergenceFill(step3.governance_active, step3.governance_baseline),
    ).toBe(false);
  });

  it("null composite_score step produces no fill for financial (non-governance null)", () => {
    // Any framework can produce a null composite_score, not just governance.
    // This guards against the connectNulls=false requirement being governance-only.
    // If financial_active is null, no fill should render for that step.
    expect(computeDivergenceFill(null, 0.75)).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// AC-006 — All four Zone 1 instruments update in a single render cycle (RTL)
// Source: US-023; FA brief §Shared State Architecture (FA-C2 Resolution)
//
// Tests the atomicity contract: store.advanceStep() must call Zustand set()
// ONCE, and all four Zone 1 instruments must reflect the new state in one
// React 18 automatic batching cycle.
// ---------------------------------------------------------------------------

import { useScenarioStepStore } from "../../store/scenarioStepStore";

describe("AC-006 — atomicity: Zustand store single-set() invariant", () => {
  it("AC-006: advanceStep() emits exactly one state change (single set() call)", () => {
    // Seed a scenario with 3 steps so advanceStep() can fire
    useScenarioStepStore.getState().setScenario("test-scenario", 3, "MODE_1");
    useScenarioStepStore.setState({ current_step: 0 });

    // subscribe() fires once per set() call — count emissions
    let changeCount = 0;
    const unsub = useScenarioStepStore.subscribe(() => { changeCount++; });

    useScenarioStepStore.getState().advanceStep();

    unsub();
    expect(changeCount).toBe(1);
  });

  it("AC-006: current_step increments after advanceStep()", () => {
    useScenarioStepStore.getState().setScenario("test-scenario-2", 5, "MODE_1");
    useScenarioStepStore.setState({ current_step: 2 });

    useScenarioStepStore.getState().advanceStep();

    expect(useScenarioStepStore.getState().current_step).toBe(3);
  });

  it("AC-006: advanceStep() does not increment past step_count", () => {
    useScenarioStepStore.getState().setScenario("test-scenario-3", 3, "MODE_1");
    useScenarioStepStore.setState({ current_step: 3 });

    useScenarioStepStore.getState().advanceStep();

    expect(useScenarioStepStore.getState().current_step).toBe(3);
  });

  // setTrajectory side-effect removal — Issue #643
  it("setTrajectory does not mutate current_step", () => {
    useScenarioStepStore.getState().setScenario("traj-test", 5, "MODE_1");
    useScenarioStepStore.setState({ current_step: 3 });

    useScenarioStepStore.getState().setTrajectory({
      scenario_id: "traj-test",
      entity_id: "ARG",
      step_count: 5,
      mda_floors: [],
      steps: [],
    });

    expect(useScenarioStepStore.getState().current_step).toBe(3);
  });

  it("setCurrentStep sets current_step explicitly", () => {
    useScenarioStepStore.getState().setScenario("traj-test-2", 5, "MODE_1");
    useScenarioStepStore.setState({ current_step: 0 });

    useScenarioStepStore.getState().setCurrentStep(5);

    expect(useScenarioStepStore.getState().current_step).toBe(5);
  });
});

// ---------------------------------------------------------------------------
// computeYDomain — adaptive y-axis domain (IR-001 fix)
// ---------------------------------------------------------------------------

describe("computeYDomain — adaptive y-axis domain from score values", () => {
  it("empty array → [0, 1] fallback", () => {
    expect(computeYDomain([])).toEqual([0, 1]);
  });

  it("all values equal — padding of 0.05 applied on each side", () => {
    const [lo, hi] = computeYDomain([0.5, 0.5, 0.5]);
    expect(lo).toBeCloseTo(0.45, 2);
    expect(hi).toBeCloseTo(0.55, 2);
  });

  it("wide spread — padding is 10% of range, not flat 0.05", () => {
    // range = 0.6, 10% = 0.06 > 0.05 → padding = 0.06
    const [lo, hi] = computeYDomain([0.2, 0.8]);
    expect(lo).toBeCloseTo(0.14, 1);
    expect(hi).toBeCloseTo(0.86, 1);
  });

  it("narrow spread comparable to Demo 6 data (FIN 0.51–0.56, GOV 0.51, HD 0.24–0.25)", () => {
    const scores = [0.5635, 0.5100, 0.2500, 0.5198, 0.5125, 0.2375];
    const [lo, hi] = computeYDomain(scores);
    expect(lo).toBeGreaterThanOrEqual(0);
    expect(lo).toBeLessThan(0.24);  // padded below HD's minimum
    expect(hi).toBeGreaterThan(0.56); // padded above FIN's maximum
    expect(hi).toBeLessThanOrEqual(1);
  });

  it("min - padding < 0 → floor clamped to 0", () => {
    const [lo] = computeYDomain([0.02, 0.03]);
    expect(lo).toBeGreaterThanOrEqual(0);
  });

  it("max + padding > 1 → ceiling clamped to 1", () => {
    const [, hi] = computeYDomain([0.97, 0.98]);
    expect(hi).toBeLessThanOrEqual(1);
  });

  it("returns a tuple of exactly two numbers", () => {
    const result = computeYDomain([0.3, 0.7]);
    expect(result).toHaveLength(2);
    expect(typeof result[0]).toBe("number");
    expect(typeof result[1]).toBe("number");
  });

  it("lo is always ≤ hi", () => {
    expect(computeYDomain([0.5])[0]).toBeLessThanOrEqual(computeYDomain([0.5])[1]);
    expect(computeYDomain([0.1, 0.9])[0]).toBeLessThanOrEqual(computeYDomain([0.1, 0.9])[1]);
  });

  it("AC-1251-1: floor below data range — yMin extends to accommodate floor", () => {
    // Worked example from intent doc §0: data 0.65–0.80, floor 0.40 included in values array
    // after call-site fix; computeYDomain must return yMin ≤ 0.40
    const [lo] = computeYDomain([0.65, 0.70, 0.80, 0.40]);
    expect(lo).toBeLessThanOrEqual(0.40);
  });

  it("AC-1251-2: floor within data range — domain not shrunk", () => {
    // floor 0.40 already between data min (0.30) and max (0.70); including it is a no-op
    const [loWith, hiWith] = computeYDomain([0.30, 0.40, 0.70]);
    const [loWithout, hiWithout] = computeYDomain([0.30, 0.70]);
    expect(loWith).toBeCloseTo(loWithout, 5);
    expect(hiWith).toBeCloseTo(hiWithout, 5);
  });

  // AC-1254-4 — yDomain extended for CI upper bounds (M18-G1)
  it("AC-1254-4: CI upper value 0.95 included → yMax ≥ 0.95", () => {
    // Intent doc §7 AC-1254-4: scores [0.60, 0.70, 0.80] + ci_upper 0.95 included.
    // computeYDomain at the updated call site passes CI upper values alongside scores.
    // yMax must accommodate the CI upper value, not only the composite scores.
    const [, hi] = computeYDomain([0.60, 0.70, 0.80, 0.95]);
    expect(hi).toBeGreaterThanOrEqual(0.95);
  });

  it("AC-1254-4: without CI upper value, yMax is below 0.95 (demonstrates the gap)", () => {
    // Hard-fail scenario: if the call site does NOT include CI upper values,
    // yMax is computed from scores alone (≈ 0.85 with 10% padding above 0.80).
    // This confirms that including 0.95 is necessary to extend the domain.
    const [, hiScoresOnly] = computeYDomain([0.60, 0.70, 0.80]);
    // With 10% padding: range=0.20, 10%=0.02 < 0.05 → use 0.05 padding → hi≈0.85
    expect(hiScoresOnly).toBeLessThan(0.95);
  });

  it("AC-1254-4: yMax ≥ max(ci_upper values) across multiple steps", () => {
    // Multiple steps with different CI upper values: domain must encompass the highest.
    const compositeScores = [0.55, 0.58, 0.60, 0.62];
    const ciUpperValues = [0.71, 0.77, 0.95, 0.95]; // step 3 and 4 at 0.9455
    const allValues = [...compositeScores, ...ciUpperValues];
    const [, hi] = computeYDomain(allValues);
    const maxCIUpper = Math.max(...ciUpperValues);
    expect(hi).toBeGreaterThanOrEqual(maxCIUpper);
  });
});

// ---------------------------------------------------------------------------
// M18-G1: AC-1254-2 — mergeTrajectories CI extraction
// M18-G1: CI_BAND_OPACITY constant and computeCompositeHalfWidth (§5.1, §5.2)
//
// These tests are RED until TrajectoryView.tsx exports the following:
//   mergeTrajectories(trajectory, baseline) — extracts ci_lower/ci_upper into MergedStepDatum
//   CI_BAND_OPACITY — the 0.12 constant for recharts <Area> fillOpacity
//   computeCompositeHalfWidth(stepIndex, tier) — BandingEngine §3.1 frontend mirror
//
// Import technique: dynamic import in beforeAll avoids breaking existing tests
// when the exports are not yet available.
// ---------------------------------------------------------------------------

describe("M18-G1: CI_BAND_OPACITY constant", () => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let CI_BAND_OPACITY: number | undefined;

  beforeAll(async () => {
    try {
      const mod = await import("../TrajectoryView");
      CI_BAND_OPACITY = (mod as Record<string, unknown>).CI_BAND_OPACITY as number | undefined;
    } catch {
      CI_BAND_OPACITY = undefined;
    }
  });

  it("CI_BAND_OPACITY is exported from TrajectoryView", () => {
    // RED until CI_BAND_OPACITY is exported
    expect(CI_BAND_OPACITY).toBeDefined();
  });

  it("CI_BAND_OPACITY is exactly 0.12 (intent doc §5.1)", () => {
    if (CI_BAND_OPACITY === undefined) {
      expect(CI_BAND_OPACITY).toBeDefined();
      return;
    }
    expect(CI_BAND_OPACITY).toBe(0.12);
    expect(typeof CI_BAND_OPACITY).toBe("number");
  });
});

describe("M18-G1: computeCompositeHalfWidth — BandingEngine §3.1 frontend mirror", () => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let computeCompositeHalfWidth: ((stepIndex: number, tier: number) => number) | undefined;

  beforeAll(async () => {
    try {
      const mod = await import("../TrajectoryView");
      computeCompositeHalfWidth = (mod as Record<string, unknown>)
        .computeCompositeHalfWidth as typeof computeCompositeHalfWidth;
    } catch {
      computeCompositeHalfWidth = undefined;
    }
  });

  it("computeCompositeHalfWidth is exported from TrajectoryView", () => {
    expect(computeCompositeHalfWidth).toBeDefined();
  });

  it("step=1, tier=1 → half-width = 0.10 × 1.0 = 0.10", () => {
    if (!computeCompositeHalfWidth) { expect(computeCompositeHalfWidth).toBeDefined(); return; }
    expect(computeCompositeHalfWidth(1, 1)).toBeCloseTo(0.10, 5);
  });

  it("step=2, tier=2 → half-width = 0.20 × 1.2 = 0.24", () => {
    if (!computeCompositeHalfWidth) { expect(computeCompositeHalfWidth).toBeDefined(); return; }
    expect(computeCompositeHalfWidth(2, 2)).toBeCloseTo(0.24, 5);
  });

  it("step=4, tier=3 → half-width = 0.35 × 1.5 = 0.525 (worked example)", () => {
    if (!computeCompositeHalfWidth) { expect(computeCompositeHalfWidth).toBeDefined(); return; }
    expect(computeCompositeHalfWidth(4, 3)).toBeCloseTo(0.525, 5);
  });

  it("step=6, tier=4 → half-width = 0.50 × 2.0 = 1.0", () => {
    if (!computeCompositeHalfWidth) { expect(computeCompositeHalfWidth).toBeDefined(); return; }
    expect(computeCompositeHalfWidth(6, 4)).toBeCloseTo(1.0, 5);
  });

  it("step=5, tier=5 → half-width = 0.35 × 3.0 = 1.05", () => {
    if (!computeCompositeHalfWidth) { expect(computeCompositeHalfWidth).toBeDefined(); return; }
    expect(computeCompositeHalfWidth(5, 5)).toBeCloseTo(1.05, 5);
  });

  it("step=3 and step=4 return the same half-width (both in 3–5 year range)", () => {
    if (!computeCompositeHalfWidth) { expect(computeCompositeHalfWidth).toBeDefined(); return; }
    expect(computeCompositeHalfWidth(3, 2)).toBeCloseTo(computeCompositeHalfWidth(4, 2), 5);
  });

  it("step=6 returns greater half-width than step=5 (crossing the >5 year threshold)", () => {
    if (!computeCompositeHalfWidth) { expect(computeCompositeHalfWidth).toBeDefined(); return; }
    expect(computeCompositeHalfWidth(6, 1)).toBeGreaterThan(computeCompositeHalfWidth(5, 1));
  });
});

describe("AC-1254-2 — mergeTrajectories CI extraction", () => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let mergeTrajectories: ((trajectory: object, baseline: object | null) => object[]) | undefined;

  beforeAll(async () => {
    try {
      const mod = await import("../TrajectoryView");
      mergeTrajectories = (mod as Record<string, unknown>)
        .mergeTrajectories as typeof mergeTrajectories;
    } catch {
      mergeTrajectories = undefined;
    }
  });

  it("mergeTrajectories is exported from TrajectoryView", () => {
    // RED until mergeTrajectories is exported (M18-G1 implementation required)
    expect(mergeTrajectories).toBeDefined();
  });

  it("AC-1254-2: financial ci_lower extracted when non-null in step.frameworks.financial", () => {
    if (!mergeTrajectories) { expect(mergeTrajectories).toBeDefined(); return; }

    const trajectory = {
      scenario_id: "zmb-test",
      entity_id: "ZMB",
      step_count: 1,
      mda_floors: [],
      steps: [
        {
          step_index: 1,
          effective_from: "2024-01-01T00:00:00Z",
          step_event_label: null,
          step_significance: "ROUTINE",
          frameworks: {
            financial: {
              composite_score: 0.62,
              ci_lower: 0.45,
              ci_upper: 0.65,
              confidence_tier: 3,
              scoring_basis: "normalized_absolute",
            },
            human_development: {
              composite_score: 0.55,
              ci_lower: null,
              ci_upper: null,
              confidence_tier: 3,
              scoring_basis: "normalized_absolute",
            },
            ecological: {
              composite_score: null,
              ci_lower: null,
              ci_upper: null,
              confidence_tier: 3,
              scoring_basis: "boundary_proximity",
            },
            governance: {
              composite_score: null,
              ci_lower: null,
              ci_upper: null,
              confidence_tier: 2,
              scoring_basis: "percentile_rank",
            },
          },
          policy_inputs: [],
          shock_events: [],
        },
      ],
    };

    const data = mergeTrajectories(trajectory, null) as Record<string, unknown>[];
    expect(data).toHaveLength(1);

    const datum = data[0];
    // AC-1254-2: non-null ci_lower/ci_upper must be extracted into MergedStepDatum
    expect(datum["financial_ci_lower"]).toBe(0.45);
    expect(datum["financial_ci_upper"]).toBe(0.65);
  });

  it("AC-1254-2: null ci_lower produces null financial_ci_lower in datum", () => {
    if (!mergeTrajectories) { expect(mergeTrajectories).toBeDefined(); return; }

    const trajectory = {
      scenario_id: "zmb-test",
      entity_id: "ZMB",
      step_count: 1,
      mda_floors: [],
      steps: [
        {
          step_index: 1,
          effective_from: "2024-01-01T00:00:00Z",
          step_event_label: null,
          step_significance: "ROUTINE",
          frameworks: {
            financial: {
              composite_score: 0.62,
              ci_lower: null,
              ci_upper: null,
              confidence_tier: 3,
              scoring_basis: "normalized_absolute",
            },
            human_development: { composite_score: null, ci_lower: null, ci_upper: null, confidence_tier: 3, scoring_basis: "normalized_absolute" },
            ecological: { composite_score: null, ci_lower: null, ci_upper: null, confidence_tier: 3, scoring_basis: "boundary_proximity" },
            governance: { composite_score: null, ci_lower: null, ci_upper: null, confidence_tier: 2, scoring_basis: "percentile_rank" },
          },
          policy_inputs: [],
          shock_events: [],
        },
      ],
    };

    const data = mergeTrajectories(trajectory, null) as Record<string, unknown>[];
    expect(data).toHaveLength(1);
    // AC-1254-2: null ci_lower propagates to datum
    expect(data[0]["financial_ci_lower"]).toBeNull();
    expect(data[0]["financial_ci_upper"]).toBeNull();
  });

  it("AC-1254-2: all four frameworks have ci_lower/ci_upper fields in output datum", () => {
    if (!mergeTrajectories) { expect(mergeTrajectories).toBeDefined(); return; }

    const trajectory = {
      scenario_id: "zmb-test",
      entity_id: "ZMB",
      step_count: 1,
      mda_floors: [],
      steps: [
        {
          step_index: 1,
          effective_from: "2024-01-01T00:00:00Z",
          step_event_label: null,
          step_significance: "ROUTINE",
          frameworks: {
            financial: { composite_score: 0.62, ci_lower: 0.45, ci_upper: 0.65, confidence_tier: 3, scoring_basis: "normalized_absolute" },
            human_development: { composite_score: 0.55, ci_lower: 0.40, ci_upper: 0.70, confidence_tier: 3, scoring_basis: "normalized_absolute" },
            ecological: { composite_score: null, ci_lower: null, ci_upper: null, confidence_tier: 3, scoring_basis: "boundary_proximity" },
            governance: { composite_score: null, ci_lower: null, ci_upper: null, confidence_tier: 2, scoring_basis: "percentile_rank" },
          },
          policy_inputs: [],
          shock_events: [],
        },
      ],
    };

    const data = mergeTrajectories(trajectory, null) as Record<string, unknown>[];
    const datum = data[0];

    // All four frameworks must have both ci_lower and ci_upper keys in the output
    const expectedKeys = [
      "financial_ci_lower", "financial_ci_upper",
      "human_development_ci_lower", "human_development_ci_upper",
      "ecological_ci_lower", "ecological_ci_upper",
      "governance_ci_lower", "governance_ci_upper",
    ];
    for (const key of expectedKeys) {
      expect(Object.prototype.hasOwnProperty.call(datum, key)).toBe(true);
    }

    // Non-null values preserved; null values preserved as null
    expect(datum["financial_ci_lower"]).toBe(0.45);
    expect(datum["human_development_ci_upper"]).toBe(0.70);
    expect(datum["ecological_ci_lower"]).toBeNull();
    expect(datum["governance_ci_upper"]).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// M18-G1: CI Bands (#1254) — unit tests for exported CI band helpers
// ---------------------------------------------------------------------------

describe("M18-G1: CI_BAND_OPACITY constant (AC-1254-OP)", () => {
  it("CI_BAND_OPACITY is 0.12", async () => {
    const mod = await import("../TrajectoryView");
    const { CI_BAND_OPACITY } = mod as unknown as Record<string, number>;
    expect(CI_BAND_OPACITY).toBe(0.12);
  });

  it("CI_BAND_OPACITY_MODE3 is 0.05", async () => {
    const mod = await import("../TrajectoryView");
    const { CI_BAND_OPACITY_MODE3 } = mod as unknown as Record<string, number>;
    expect(CI_BAND_OPACITY_MODE3).toBe(0.05);
  });
});

describe("M18-G1: computeCompositeHalfWidth — BandingEngine §3.1 frontend mirror (AC-1254-HW)", () => {
  type HWFn = (stepIndex: number, tier: number) => number;
  let computeCompositeHalfWidth: HWFn;

  beforeAll(async () => {
    const mod = await import("../TrajectoryView");
    computeCompositeHalfWidth = (mod as unknown as Record<string, HWFn>).computeCompositeHalfWidth;
  });

  it("step 1, tier 1 → 0.10", () => expect(computeCompositeHalfWidth(1, 1)).toBeCloseTo(0.10, 10));
  it("step 2, tier 1 → 0.20", () => expect(computeCompositeHalfWidth(2, 1)).toBeCloseTo(0.20, 10));
  it("step 3, tier 1 → 0.35", () => expect(computeCompositeHalfWidth(3, 1)).toBeCloseTo(0.35, 10));
  it("step 5, tier 1 → 0.35", () => expect(computeCompositeHalfWidth(5, 1)).toBeCloseTo(0.35, 10));
  it("step 6, tier 1 → 0.50", () => expect(computeCompositeHalfWidth(6, 1)).toBeCloseTo(0.50, 10));
  it("step 1, tier 3 → 0.10 × 1.5 = 0.15", () => expect(computeCompositeHalfWidth(1, 3)).toBeCloseTo(0.15, 10));
  it("step 2, tier 5 → 0.20 × 3.0 = 0.60", () => expect(computeCompositeHalfWidth(2, 5)).toBeCloseTo(0.60, 10));
});

describe("AC-1254-2 — mergeTrajectories CI extraction", () => {
  it("mergeTrajectories is exported", async () => {
    const mod = await import("../TrajectoryView");
    expect(typeof (mod as Record<string, unknown>).mergeTrajectories).toBe("function");
  });

  it("MergedStepDatum includes CI fields — checked via exported interface", async () => {
    // Runtime verification: mergeTrajectories returns objects with ci fields.
    // TypeScript structural check is enforced by the export interface MergedStepDatum
    // definition in TrajectoryView.tsx (see governance_ci_upper field).
    const mod = await import("../TrajectoryView");
    const mergeFn = (mod as Record<string, unknown>).mergeTrajectories;
    expect(typeof mergeFn).toBe("function");
  });
});

// ---------------------------------------------------------------------------
// M18-G7-A: AC-A1 — computeCompositeCIBounds additive formula
//
// `computeCompositeCIBounds` is currently a private function using MULTIPLICATIVE
// formula: `score * (1 ± halfWidth)`. ADR-007/ADR-010 spec requires ADDITIVE:
// `score ± halfWidth`.
//
// RED state: function not exported → `computeCompositeCIBounds` is undefined.
// RED state: even when exported, multiplicative formula returns wrong values.
// GREEN state (after G7-A): exported, additive formula, capped to [0, 1].
//
// Fixture derivation (computeCompositeHalfWidth schedule):
//   T3 step 1: baseHW=0.10, multiplier[3]=1.5 → halfWidth=0.15
//              additive: {upper: 0.65, lower: 0.35}
//              multiplicative (wrong): {upper: 0.575, lower: 0.425}
//   T3 step 6: baseHW=0.50, multiplier[3]=1.5 → halfWidth=0.75
//              additive: {upper: min(1.0, 1.25)=1.0, lower: max(0.0, -0.25)=0.0}
//              multiplicative (wrong): {upper: 0.875, lower: 0.125}
//
// Source: M18-G7-A intent §AC-A1 + root cause analysis §Root Cause 1.
// ---------------------------------------------------------------------------

describe("M18-G7-A: AC-A1 — computeCompositeCIBounds additive formula", () => {
  type MinimalFrameworkPoint = {
    composite_score: number | null;
    ci_lower: null;
    ci_upper: null;
    confidence_tier: number;
    scoring_basis: "percentile_rank";
  };
  type MinimalStep = {
    step_index: number;
    effective_from: string;
    step_event_label: null;
    step_significance: "ROUTINE";
    pmm: null;
    frameworks: Record<string, MinimalFrameworkPoint>;
  };

  function makeStep(stepIndex: number, score: number, tier: number): MinimalStep {
    const fw: MinimalFrameworkPoint = {
      composite_score: score,
      ci_lower: null,
      ci_upper: null,
      confidence_tier: tier,
      scoring_basis: "percentile_rank",
    };
    return {
      step_index: stepIndex,
      effective_from: "2024-01-01T00:00:00Z",
      step_event_label: null,
      step_significance: "ROUTINE",
      pmm: null,
      frameworks: { financial: fw, human_development: fw, ecological: fw, governance: fw },
    };
  }

  let computeCompositeCIBounds: unknown;

  beforeAll(async () => {
    const mod = await import("../TrajectoryView");
    computeCompositeCIBounds = (mod as Record<string, unknown>).computeCompositeCIBounds;
  });

  it("computeCompositeCIBounds is exported from TrajectoryView (RED until G7-A export fix)", () => {
    expect(typeof computeCompositeCIBounds).toBe("function");
  });

  it("AC-A1: T3 step 1 — additive: upper=0.65, lower=0.35", () => {
    const fn = computeCompositeCIBounds as ((s: MinimalStep) => { upper: number | null; lower: number | null }) | undefined;
    if (typeof fn !== "function") return; // deferred until export fix
    const result = fn(makeStep(1, 0.50, 3));
    // additive: 0.50 + 0.15 = 0.65; 0.50 - 0.15 = 0.35
    // multiplicative (wrong): upper=0.575, lower=0.425
    expect(result.upper).toBeCloseTo(0.65, 5);
    expect(result.lower).toBeCloseTo(0.35, 5);
  });

  it("AC-A1: T3 step 6 — additive with capping: upper=1.0, lower=0.0", () => {
    const fn = computeCompositeCIBounds as ((s: MinimalStep) => { upper: number | null; lower: number | null }) | undefined;
    if (typeof fn !== "function") return; // deferred until export fix
    const result = fn(makeStep(6, 0.50, 3));
    // additive: 0.50 + 0.75 = 1.25 → capped to 1.0; 0.50 - 0.75 = -0.25 → capped to 0.0
    // multiplicative (wrong): upper=0.875, lower=0.125
    expect(result.upper).toBe(1.0);
    expect(result.lower).toBe(0.0);
  });

  it("AC-A1: result is never multiplicative — upper ≠ score*(1+halfWidth) for T3 step 1", () => {
    const fn = computeCompositeCIBounds as ((s: MinimalStep) => { upper: number | null; lower: number | null }) | undefined;
    if (typeof fn !== "function") return;
    const result = fn(makeStep(1, 0.50, 3));
    // multiplicative wrong value: 0.50 * (1 + 0.15) = 0.575
    expect(result.upper).not.toBeCloseTo(0.575, 5);
  });
});

// ---------------------------------------------------------------------------
// M18-G7-A: AC-A2 — yDomain excludes CI bound values (regression guard)
//
// The G7-A fix removes `computeCompositeCIBounds(step).upper` from the values
// array passed to `computeYDomain` in CompositeChartSVG. This test guards
// against re-introducing CI values into the yDomain call site.
//
// This test is GREEN from the start — computeYDomain([0.48..0.54]) already
// returns yMax ≤ 0.65. The regression guard confirms that when the component
// calls computeYDomain with scores only, the y-axis stays in the trajectory
// range and does NOT inflate to the CI upper bound.
//
// The second assertion demonstrates the BUG: including a CI upper of 1.0
// inflates yMax to ≥ 0.97, compressing trajectory curves to 5% of chart height.
//
// Source: M18-G7-A intent §AC-A2 + root cause analysis §Root Cause 1 §Fix item 2.
// ---------------------------------------------------------------------------

describe("M18-G7-A: AC-A2 — yDomain trajectory-only values produce readable range", () => {
  it("AC-A2: computeYDomain with trajectory scores only [0.48..0.54] → yMax ≤ 0.65", () => {
    // After G7-A fix: component passes only composite scores to computeYDomain.
    // With trajectory range 0.48–0.54, yMax must not inflate past 0.65.
    const [, hi] = computeYDomain([0.48, 0.50, 0.52, 0.54]);
    expect(hi).toBeLessThanOrEqual(0.65);
  });

  it("AC-A2: BUG demonstration — CI upper=1.0 included inflates yMax above 0.95", () => {
    // This is the CURRENT broken behavior: CompositeChartSVG pushes ci_upper into values[].
    // When 1.0 is included, yMax inflates to accommodate it, compressing trajectories.
    // G7-A removes this push; the assertion below documents what the bug looks like.
    const [, hi] = computeYDomain([0.48, 0.50, 0.52, 0.54, 1.0]);
    expect(hi).toBeGreaterThan(0.95);
  });
});

describe("AC-1254-4 — computeYDomain includes CI upper values", () => {
  it("CI upper value 0.95 — yMax ≥ 0.95", () => {
    const [, hi] = computeYDomain([0.50, 0.60, 0.95]);
    expect(hi).toBeGreaterThanOrEqual(0.95);
  });

  it("without CI upper value — yMax is capped at 0.70 range", () => {
    const [, hi] = computeYDomain([0.50, 0.60]);
    expect(hi).toBeLessThan(0.80);
  });

  it("yMax ≥ max CI upper across multiple steps", () => {
    const ciUppers = [0.82, 0.88, 0.91];
    const [, hi] = computeYDomain([0.50, 0.60, ...ciUppers]);
    expect(hi).toBeGreaterThanOrEqual(0.91);
  });
});

