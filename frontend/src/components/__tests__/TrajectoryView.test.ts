/**
 * Vitest: M9 TrajectoryView — Pre-implementation acceptance test gate.
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
 *
 * ALL TESTS ARE EXPECTED TO FAIL until Issue #460/461/462 implement the
 * TrajectoryView component. That is correct and expected (Issue #459).
 *
 * WHEN IMPLEMENTING (Issue #460):
 *   1. Create frontend/src/components/TrajectoryView.tsx exporting the functions
 *      and constants listed in the @ts-expect-error import below.
 *   2. Install @testing-library/react and update vite.config.ts test.environment
 *      to 'jsdom' for RTL tests (AC-006).
 *   3. Remove the @ts-expect-error directives once the module exists.
 *   4. Install zustand and add useScenarioStepStore to the store module.
 *
 * Implementation dependencies (none of these exist yet in M9 pre-implementation):
 *   - frontend/src/components/TrajectoryView.tsx
 *   - frontend/src/store/scenarioStepStore.ts  (Zustand atom — FA brief §Shared State)
 *   - @testing-library/react  (not yet in package.json)
 *   - zustand  (not yet in package.json)
 */
import { describe, it, expect } from "vitest";

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
// @ts-expect-error — TrajectoryView does not exist until Issue #460
import {
  computeDivergenceFill,
  getConfidenceBadgeVisible,
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
// These tests require @testing-library/react (not yet installed) and a DOM
// environment (vitest environment: 'jsdom', not yet configured).
// They are marked it.todo() to document the contract without causing failures
// from missing infrastructure.
//
// WHEN IMPLEMENTING (Issue #460):
//   1. npm install --save-dev @testing-library/react @testing-library/user-event jsdom
//   2. Update vite.config.ts: test.environment = 'jsdom'
//   3. Install zustand: npm install zustand
//   4. Implement useScenarioStepStore in frontend/src/store/scenarioStepStore.ts
//   5. Convert these it.todo() to full test implementations using the patterns
//      described in the comments below.
// ---------------------------------------------------------------------------

describe("AC-006 — atomicity: all four instruments update in one render cycle (RTL)", () => {
  it.todo(
    `AC-006: step advance wrapped in act() causes all four Zone 1 instruments to
     reflect new current_step before act() resolves.

     Implementation pattern:
       import { render, act } from '@testing-library/react';
       import { ScenarioView } from '../ScenarioView';
       import { useScenarioStepStore } from '../../store/scenarioStepStore';

       it('AC-006: instruments update atomically on step advance', async () => {
         const { getByTestId } = render(<ScenarioView />);
         const store = useScenarioStepStore.getState();

         await act(async () => {
           store.advanceStep();  // single set() call per FA brief §Shared State Architecture
         });

         // All four instruments must reflect new step within the same act() call:
         expect(getByTestId('zone-1a-trajectory').dataset.currentStep).toBe('1');
         expect(getByTestId('zone-1b-mda-alerts').dataset.currentStep).toBe('1');
         expect(getByTestId('zone-1c-pmm').dataset.currentStep).toBe('1');
         expect(getByTestId('zone-1d-four-framework').dataset.currentStep).toBe('1');
       });

     Atomicity contract (FA brief §Shared State Architecture):
       - store.advanceStep() calls Zustand set() ONCE with current_step, trajectory, and
         updated state — never via multiple set() calls in sequence.
       - All four Zone 1 instruments subscribe to useScenarioStepStore() and re-render
         in the same React 18 automatic batching cycle triggered by the single set() call.
       - No additional act() call should be needed — all four must update in the first one.`,
  );

  it.todo(
    `AC-006: Zustand store.advanceStep() issues exactly one set() call.

     Implementation pattern (spy on Zustand set):
       import { create } from 'zustand';
       import { vi } from 'vitest';

       it('AC-006: single set() call on step advance', () => {
         const setCalls: unknown[] = [];
         const store = useScenarioStepStore.getState();
         const originalSet = (useScenarioStepStore as any).setState;
         vi.spyOn(useScenarioStepStore as any, 'setState').mockImplementation((update: unknown) => {
           setCalls.push(update);
           originalSet(update);
         });

         store.advanceStep();

         expect(setCalls).toHaveLength(1);
         // The single set() must include current_step AND trajectory together:
         expect(setCalls[0]).toMatchObject({
           current_step: expect.any(Number),
           trajectory: expect.anything(),
         });
       });`,
  );
});
