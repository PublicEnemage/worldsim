/**
 * Zustand atom for shared Zone 1 instrument state.
 *
 * All four Zone 1 instruments subscribe to this store. State transitions must always
 * call set() ONCE — never field-by-field across multiple set() calls. See DD-012.
 * AC-006 tests the single-set() invariant via a Zustand setState spy.
 */
import { create } from "zustand";

export interface TrajectoryFrameworkPoint {
  composite_score: number | null;
  ci_lower: number | null;
  ci_upper: number | null;
  confidence_tier: number;
  scoring_basis: "percentile_rank" | "normalized_absolute";
}

export interface TrajectoryStep {
  step_index: number;
  effective_from: string;
  step_event_label: string | null;
  step_significance: "SIGNIFICANT" | "ROUTINE";
  frameworks: Record<string, TrajectoryFrameworkPoint>;
}

export interface MDAFloor {
  framework: string;
  floor_value: number;
  label: string;
  severity: "WARNING" | "CRITICAL";
}

export interface TrajectoryResponse {
  scenario_id: string;
  entity_id: string;
  step_count: number;
  mda_floors: MDAFloor[];
  steps: TrajectoryStep[];
}

interface ScenarioStepState {
  scenario_id: string;
  current_step: number;
  step_count: number;
  trajectory: TrajectoryResponse | null;
  baseline_trajectory: TrajectoryResponse | null;
  computation_state: "idle" | "computing" | "complete";
  mode: "MODE_1" | "MODE_2" | "MODE_3";
  setScenario: (
    scenario_id: string,
    step_count: number,
    mode: "MODE_1" | "MODE_2" | "MODE_3",
  ) => void;
  setTrajectory: (trajectory: TrajectoryResponse) => void;
  advanceStep: () => void;
  applyControlInput: (newTrajectory: TrajectoryResponse) => void;
  reset: () => void;
}

export const useScenarioStepStore = create<ScenarioStepState>((set, get) => ({
  scenario_id: "",
  current_step: 0,
  step_count: 0,
  trajectory: null,
  baseline_trajectory: null,
  computation_state: "idle",
  mode: "MODE_1",

  setScenario: (scenario_id, step_count, mode) =>
    set({
      scenario_id,
      step_count,
      mode,
      current_step: 0,
      trajectory: null,
      baseline_trajectory: null,
      computation_state: "idle",
    }),

  setTrajectory: (trajectory) =>
    set({
      trajectory,
      current_step: trajectory.step_count,
      computation_state: "complete",
    }),

  advanceStep: () => {
    const { current_step, step_count } = get();
    if (current_step < step_count) {
      set({ current_step: current_step + 1, computation_state: "computing" });
    }
  },

  applyControlInput: (newTrajectory) => {
    const { trajectory, baseline_trajectory } = get();
    set({
      trajectory: newTrajectory,
      baseline_trajectory: baseline_trajectory ?? trajectory,
      computation_state: "complete",
    });
  },

  reset: () =>
    set({
      scenario_id: "",
      current_step: 0,
      step_count: 0,
      trajectory: null,
      baseline_trajectory: null,
      computation_state: "idle",
      mode: "MODE_1",
    }),
}));
