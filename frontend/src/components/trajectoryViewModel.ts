/**
 * trajectoryViewModel — view model layer for Zone 1 trajectory instruments.
 *
 * RED STUB: This file is a placeholder that satisfies TypeScript imports until
 * #1522 (view model layer retrofit) is implemented. Function signatures are
 * correct; implementations are stubs that make AC-4 and AC-5 tests FAIL.
 *
 * After #1522 lands:
 *   - computeYDomain, computeDivergenceFill, getConfidenceBadgeVisible are moved
 *     here from TrajectoryView.tsx (TrajectoryView re-exports them).
 *   - mergeTrajectories gains visibleStepRange filtering.
 *   - sliceToStepRange is implemented.
 *   - This comment block is removed.
 *
 * M19-G5 Phase C (#1522) — implement before opening #1524 implementation PR.
 */
import type { TrajectoryResponse } from "../store/scenarioStepStore";
export type { MergedStepDatum } from "./TrajectoryView";

// Re-export pure functions that exist today — behavior preserved (AC-3 GREEN).
export {
  computeYDomain,
  computeDivergenceFill,
  getConfidenceBadgeVisible,
} from "./TrajectoryView";

// Stub for internal import resolution.
import type { MergedStepDatum } from "./TrajectoryView";

/**
 * RED STUB — always returns empty array; ignores all parameters.
 * AC-4 tests will FAIL (mergeTrajectories returns [] instead of filtered steps).
 * Replaced by #1522 with real merge + visibleStepRange filtering logic.
 */
export function mergeTrajectories(
  _active: TrajectoryResponse,
  _baseline: TrajectoryResponse | null,
  _visibleStepRange?: [number, number] | null,
): MergedStepDatum[] {
  return []; // RED: replaced by #1522
}

/**
 * RED STUB — always returns empty array.
 * AC-5 tests will FAIL until #1522 replaces this with the real implementation.
 */
export function sliceToStepRange(
  _data: MergedStepDatum[],
  _range: [number, number],
): MergedStepDatum[] {
  return []; // RED: replaced by #1522
}
