/**
 * Zustand atom for shared Zone 1 instrument state.
 *
 * All four Zone 1 instruments subscribe to this store. State transitions must always
 * call set() ONCE — never field-by-field across multiple set() calls. See DD-012.
 * AC-006 tests the single-set() invariant via a Zustand setState spy.
 *
 * Mode 3 branch state (G6b, Issue #753) is co-located here per mode3-interaction-spec.md §7.
 * State machine: idle → pending → computing → complete | failed.
 */
import { create } from "zustand";

export interface TrajectoryFrameworkPoint {
  composite_score: number | null;
  ci_lower: number | null;
  ci_upper: number | null;
  confidence_tier: number;
  scoring_basis: "percentile_rank" | "normalized_absolute";
  /** M18-G7-C — indicator values keyed by indicator_key. Populated by parseTrajectoryResponse. */
  indicators?: Record<string, string | null>;
}

export interface TrajectoryStep {
  step_index: number;
  effective_from: string;
  step_event_label: string | null;
  step_significance: "SIGNIFICANT" | "ROUTINE";
  frameworks: Record<string, TrajectoryFrameworkPoint>;
  pmm: { value: number; direction: "up" | "down" | "flat" } | null;
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

/**
 * Zone 1B MDA alert — enriched alert type for the instrument cluster panel.
 * Extends indicator-level MDA data with framework context, step, confidence tier,
 * and optional causal attribution (Mode 3 only).
 */
export interface Zone1BAlert {
  mda_id: string;
  /** ISO 3166-1 alpha-3 entity code (e.g. "JOR", "EGY"). Used in Zone 1B detail slot header and compact rows. */
  entity_id: string;
  indicator_key: string;
  /** Human-readable indicator name — title-cased from backend; frontend registry may override. */
  indicator_name: string;
  framework: string;
  severity: "WARNING" | "CRITICAL" | "TERMINAL";
  step_index: number;
  cohort: string | null;
  confidence_tier: number;
  causal_attribution: string | null;
  /** Threshold value (Decimal as string) for the breached/approached indicator. */
  floor_value: string;
  /** Current indicator value (Decimal as string) at the step of this alert. */
  current_value: string;
  /** Remaining approach headroom (Decimal as string; negative = breached). */
  approach_pct_remaining: string;
  /** Number of consecutive steps in breach (≥2 → TERMINAL). null if computation unavailable. */
  consecutive_breach_steps: number | null;
  /**
   * Rider #271 — reversibility classification.
   * null = irreversible threshold; integer = recoverable within N years given intervention.
   * Source: mda_thresholds.recovery_horizon_years via MDAAlert.recovery_horizon_years.
   */
  recovery_horizon_years: number | null;
}

/**
 * Cohort threshold crossing — from outputs.human_development.cohort_threshold_crossings.
 * M16-G2 (#986): income quintile cohort disaggregation on primary surface (Zone 1B).
 * Scope: poverty_headcount_ratio Q1/Q2 only (DA sign-off 2026-06-23).
 */
export interface CohortThresholdCrossing {
  quintile_key: string;
  cohort_label: string;
  indicator_key: string;
  indicator_label: string;
  severity: "CRITICAL" | "WARNING" | "WATCH";
  step_crossed: number;
  above_floor_pct: string | null;
  tier: number;
  source: string;
  /** M16-G4 #22 — ADR-007 synthetic disclosure fields. Null = real primary-source data. */
  is_synthetic?: boolean;
  synthetic_method?: "STRUCTURAL_ABSENCE" | "SYNTHETIC_COMPARABLE" | "SYNTHETIC_MODEL" | null;
  value?: string | null;
  /** Issue #1239 (DEMO6-010): True when the breach direction is value below floor (gte threshold).
   *  False when breach is value above floor (lte threshold — future). Drives label in Zone 1B. */
  breaches_below?: boolean;
}

// ---------------------------------------------------------------------------
// M18-G3 #1349 — Distributional comparison summary types
// ---------------------------------------------------------------------------

export interface DistributionalStepSummary {
  step: number;
  headcount_differential: number;
  ci_lower: number;
  ci_upper: number;
  direction_stable: boolean;
}

export interface DistributionalPairSummary {
  scenario_id: string;
  scenario_label: string;
  steps: DistributionalStepSummary[];
}

export interface MethodologyDetail {
  q1_population: number;
  ci_methodology: string;
  extraction_path: string;
  tier_rationale: string;
}

export interface DistributionalSummaryData {
  entity_id: string;
  reference_scenario_id: string;
  reference_scenario_label: string;
  terminal_step: number;
  tier: string;
  methodology_summary: string;
  methodology_detail?: MethodologyDetail;
  pairs: DistributionalPairSummary[];
}

// ---------------------------------------------------------------------------

interface ScenarioStepState {
  scenario_id: string;
  current_step: number;
  step_count: number;
  trajectory: TrajectoryResponse | null;
  baseline_trajectory: TrajectoryResponse | null;
  computation_state: "idle" | "computing" | "complete";
  mode: "MODE_1" | "MODE_2" | "MODE_3";
  mda_alerts: Zone1BAlert[];
  /** M16-G2 (#986) — cohort threshold crossings at the current step (Zone 1B Cohort Impact sub-section). */
  cohort_threshold_crossings: CohortThresholdCrossing[];
  /** Zone 1C — Policy Maneuver Margin value at current step. */
  pmm_value: number | null;
  /** Zone 1C — Direction indicator: margin growing, shrinking, or flat since last step. */
  pmm_direction: "up" | "down" | "flat" | null;
  /** M18-G3 (#1349) — distributional comparison summary for Zone 1B sticky-bottom element. */
  distributionalSummary: DistributionalSummaryData | null;

  // ---------------------------------------------------------------------------
  // Mode 3 branch state — mode3-interaction-spec.md §7
  // ---------------------------------------------------------------------------

  /** Scenario ID set when user enters Mode 3; immutable for the session. */
  baselineScenarioId: string | null;
  /** Branch scenario ID created by POST /scenarios/{id}/branch on first parameter change. */
  branchScenarioId: string | null;
  /** Step from which the branch was created. */
  branchFromStep: number | null;
  /** Steps computed on the branch so far (for step-by-step streaming reveal). */
  branchStepsComputed: number;
  /** Recompute lifecycle state. */
  recomputeStatus: "idle" | "pending" | "computing" | "complete" | "failed";

  setScenario: (
    scenario_id: string,
    step_count: number,
    mode: "MODE_1" | "MODE_2" | "MODE_3",
  ) => void;
  setTrajectory: (trajectory: TrajectoryResponse) => void;
  /** Jump to a specific step — used by scenario re-selection to land on the final step. */
  setCurrentStep: (step: number) => void;
  setMdaAlerts: (alerts: Zone1BAlert[]) => void;
  setCohortThresholdCrossings: (crossings: CohortThresholdCrossing[]) => void;
  /** Set PMM state in a single set() call (DD-012 atomicity). */
  setPmmState: (value: number | null, direction: "up" | "down" | "flat" | null) => void;
  advanceStep: () => void;
  applyControlInput: (newTrajectory: TrajectoryResponse) => void;
  /** Initialize Mode 3 branch — called after POST /scenarios/{id}/branch returns 201. */
  initBranch: (baselineId: string, branchId: string, fromStep: number) => void;
  /** Update branch progress as each step completes (streaming reveal). */
  updateBranchProgress: (stepsComputed: number) => void;
  /** Mark branch recompute as complete; trajectory is already updated. */
  setBranchComplete: () => void;
  /** Mark branch recompute as failed; baseline restores to 100% opacity. */
  setBranchFailed: () => void;
  /** Reset Mode 3 branch state — called on session exit or scenario change. */
  resetBranch: () => void;
  /** Set mode only — does not reset current_step or any other state (SF-1 guard, G8b intent §7.1). */
  setMode: (mode: "MODE_1" | "MODE_2" | "MODE_3") => void;
  /** M18-G3 (#1349) — set or clear distributional comparison summary for Zone 1B. */
  setDistributionalSummary: (summary: DistributionalSummaryData | null) => void;
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
  mda_alerts: [],
  cohort_threshold_crossings: [],
  pmm_value: null,
  pmm_direction: null,
  distributionalSummary: null,
  baselineScenarioId: null,
  branchScenarioId: null,
  branchFromStep: null,
  branchStepsComputed: 0,
  recomputeStatus: "idle",

  setScenario: (scenario_id, step_count, mode) =>
    set({
      scenario_id,
      step_count,
      mode,
      current_step: 0,
      trajectory: null,
      baseline_trajectory: null,
      computation_state: "idle",
      mda_alerts: [],
      cohort_threshold_crossings: [],
      pmm_value: null,
      pmm_direction: null,
    }),

  setTrajectory: (trajectory) =>
    set({
      trajectory,
      computation_state: "complete",
    }),

  setCurrentStep: (step) => set({ current_step: step }),

  setMdaAlerts: (alerts) => set({ mda_alerts: alerts }),

  setCohortThresholdCrossings: (crossings) => set({ cohort_threshold_crossings: crossings }),

  setPmmState: (value, direction) => set({ pmm_value: value, pmm_direction: direction }),

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

  initBranch: (baselineId, branchId, fromStep) =>
    set({
      baselineScenarioId: baselineId,
      branchScenarioId: branchId,
      branchFromStep: fromStep,
      branchStepsComputed: 0,
      recomputeStatus: "computing",
    }),

  updateBranchProgress: (stepsComputed) =>
    set({ branchStepsComputed: stepsComputed }),

  setBranchComplete: () =>
    set({ recomputeStatus: "complete" }),

  setBranchFailed: () =>
    set({
      recomputeStatus: "failed",
      trajectory: null,
    }),

  resetBranch: () =>
    set({
      baselineScenarioId: null,
      branchScenarioId: null,
      branchFromStep: null,
      branchStepsComputed: 0,
      recomputeStatus: "idle",
    }),

  setMode: (mode) => set({ mode }),

  setDistributionalSummary: (summary) => set({ distributionalSummary: summary }),

  reset: () =>
    set({
      scenario_id: "",
      current_step: 0,
      step_count: 0,
      trajectory: null,
      baseline_trajectory: null,
      computation_state: "idle",
      mode: "MODE_1",
      mda_alerts: [],
      cohort_threshold_crossings: [],
      pmm_value: null,
      pmm_direction: null,
      distributionalSummary: null,
      baselineScenarioId: null,
      branchScenarioId: null,
      branchFromStep: null,
      branchStepsComputed: 0,
      recomputeStatus: "idle",
    }),
}));
