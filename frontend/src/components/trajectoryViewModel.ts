/**
 * trajectoryViewModel — pure view-model functions for Zone 1 trajectory instruments.
 *
 * Extracted from TrajectoryView.tsx by M19-G5 #1522 (view model layer retrofit).
 * TrajectoryView.tsx re-exports all symbols below for backward compatibility.
 *
 * Hosting pure functions here:
 *   - Makes them testable without mounting a React component
 *   - Provides a clean `visibleStepRange` parameter seam for #1524 trackwheel zoom
 *   - Satisfies the platform principle: new scenario types add logic here, not in a renderer
 */
import type { TrajectoryResponse, TrajectoryStep } from "../store/scenarioStepStore";

// ---------------------------------------------------------------------------
// MergedStepDatum — output type of mergeTrajectories
// ---------------------------------------------------------------------------

export interface MergedStepDatum {
  step_index: number;
  effective_from: string;
  step_event_label: string | null;
  step_significance: "SIGNIFICANT" | "ROUTINE";
  financial_active: number | null;
  financial_baseline: number | null;
  human_development_active: number | null;
  human_development_baseline: number | null;
  ecological_active: number | null;
  ecological_baseline: number | null;
  governance_active: number | null;
  governance_baseline: number | null;
  financial_confidence_tier: number;
  human_development_confidence_tier: number;
  ecological_confidence_tier: number;
  governance_confidence_tier: number;
  financial_scoring_basis: string;
  human_development_scoring_basis: string;
  financial_ci_lower: number | null;
  financial_ci_upper: number | null;
  human_development_ci_lower: number | null;
  human_development_ci_upper: number | null;
  ecological_ci_lower: number | null;
  ecological_ci_upper: number | null;
  governance_ci_lower: number | null;
  governance_ci_upper: number | null;
  /** M19-G3 (#1537) / G4 (#1529): BandingEngine calibration state for CI display. */
  financial_band_method: string | null;
}

// ---------------------------------------------------------------------------
// Pure functions
// ---------------------------------------------------------------------------

/**
 * Returns true when |active - baseline| > 0.01 and both values are non-null.
 * The 0.01 threshold prevents fill noise from floating-point rounding near convergence.
 * AC-010 tests the boundary exactly.
 */
export function computeDivergenceFill(
  active: number | null,
  baseline: number | null,
): boolean {
  if (active === null || baseline === null) return false;
  // Round to 4 decimal places to eliminate floating-point artifacts.
  // 0.76 - 0.75 in IEEE 754 = 0.010000000000000009; rounded = 0.01 → not above threshold → false.
  const delta = parseFloat(Math.abs(active - baseline).toFixed(4));
  return delta > 0.01;
}

/**
 * Returns true when the confidence tier warrants the "(exp)" curve-face badge.
 * Badge appears at Tier 4 and 5 only. AC-013 tests the boundary at tier 3/4.
 */
export function getConfidenceBadgeVisible(confidenceTier: number): boolean {
  return confidenceTier >= 4;
}

/**
 * Compute adaptive y-axis domain from a set of composite score values.
 * Padding = max(0.05, 10% of range); result clamped to [0, 1].
 * Used by both the recharts path and CompositeChartSVG to ensure curve separation
 * is visible when scores cluster in a narrow band (e.g. FIN ~0.51–0.56, GOV ~0.51).
 */
export function computeYDomain(values: number[]): [number, number] {
  if (values.length === 0) return [0, 1];
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min;
  const padding = Math.max(0.05, range * 0.1);
  return [
    Math.max(0, parseFloat((min - padding).toFixed(2))),
    Math.min(1, parseFloat((max + padding).toFixed(2))),
  ];
}

/**
 * Merge active and baseline trajectory responses into a flat array of step datums.
 * Optional `visibleStepRange` slices to [lo, hi] inclusive before returning —
 * the seam used by #1524 trackwheel zoom to scope the recharts data window.
 */
export function mergeTrajectories(
  active: TrajectoryResponse,
  baseline: TrajectoryResponse | null,
  visibleStepRange?: [number, number] | null,
): MergedStepDatum[] {
  const baselineByStep = new Map<number, TrajectoryStep>();
  if (baseline) {
    for (const step of baseline.steps) {
      baselineByStep.set(step.step_index, step);
    }
  }

  const steps = visibleStepRange
    ? active.steps.filter(
        (s) => s.step_index >= visibleStepRange[0] && s.step_index <= visibleStepRange[1],
      )
    : active.steps;

  return steps.map((step) => {
    const bStep = baselineByStep.get(step.step_index) ?? null;

    const get = (
      source: TrajectoryStep | null,
      fw: string,
    ): number | null => source?.frameworks[fw]?.composite_score ?? null;

    const tier = (fw: string): number =>
      step.frameworks[fw]?.confidence_tier ?? 1;

    const basis = (fw: string): string =>
      step.frameworks[fw]?.scoring_basis ?? "percentile_rank";

    const ci = (fw: string, bound: "ci_lower" | "ci_upper"): number | null => {
      const raw = step.frameworks[fw]?.[bound] ?? null;
      return raw !== null ? parseFloat(raw as unknown as string) : null;
    };

    return {
      step_index: step.step_index,
      effective_from: step.effective_from,
      step_event_label: step.step_event_label,
      step_significance: step.step_significance,
      financial_active: get(step, "financial"),
      financial_baseline: get(bStep, "financial"),
      human_development_active: get(step, "human_development"),
      human_development_baseline: get(bStep, "human_development"),
      ecological_active: get(step, "ecological"),
      ecological_baseline: get(bStep, "ecological"),
      governance_active: get(step, "governance"),
      governance_baseline: get(bStep, "governance"),
      financial_confidence_tier: tier("financial"),
      human_development_confidence_tier: tier("human_development"),
      ecological_confidence_tier: tier("ecological"),
      governance_confidence_tier: tier("governance"),
      financial_scoring_basis: basis("financial"),
      human_development_scoring_basis: basis("human_development"),
      financial_ci_lower: ci("financial", "ci_lower"),
      financial_ci_upper: ci("financial", "ci_upper"),
      human_development_ci_lower: ci("human_development", "ci_lower"),
      human_development_ci_upper: ci("human_development", "ci_upper"),
      ecological_ci_lower: ci("ecological", "ci_lower"),
      ecological_ci_upper: ci("ecological", "ci_upper"),
      governance_ci_lower: ci("governance", "ci_lower"),
      governance_ci_upper: ci("governance", "ci_upper"),
      financial_band_method: step.frameworks["financial"]?.band_method ?? null,
    };
  });
}

/**
 * Filter a pre-merged MergedStepDatum array to a visible step range [lo, hi] inclusive.
 * Used by CompositeChartSVG to scope the SVG rendering window (#1524 trackwheel zoom).
 */
export function sliceToStepRange(
  data: MergedStepDatum[],
  range: [number, number],
): MergedStepDatum[] {
  return data.filter((d) => d.step_index >= range[0] && d.step_index <= range[1]);
}
