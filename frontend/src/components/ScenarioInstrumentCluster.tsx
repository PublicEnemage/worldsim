/**
 * ScenarioInstrumentCluster — composed Zone 1 cluster for App.tsx.
 *
 * Wires all four Zone 1 instruments into InstrumentCluster and connects
 * the Zustand atom to the trajectory API. Fetches trajectory when
 * scenarioId is set; keeps store current_step in sync with ScenarioControls.
 *
 * Trajectory parsing: the API returns frameworks as an array; the store
 * expects Record<string, TrajectoryFrameworkPoint>. composite_score arrives
 * as Decimal string; the store expects number | null. Both conversions
 * happen in parseTrajectoryResponse().
 *
 * MDA alerts: Zone 1B alerts are derived from the step-advance response
 * (mda_alerts per framework_output). In M9, with no advance endpoint
 * integration yet, mda_alerts defaults to [] (no alerts shown until
 * the advance endpoint is wired in a follow-up PR).
 *
 * PMM: pmm_value and pmm_direction remain null in M9 (no PMM endpoint
 * exists yet; the PMM widget renders "—"). This is correct per ADR-008
 * Decision 6: null renders as "—" (instrument in validation).
 */
import React, { useEffect } from "react";
import { InstrumentCluster } from "./InstrumentCluster";
import { MDAAlertPanelZone1B } from "./MDAAlertPanelZone1B";
import { PMMWidgetZone1C } from "./PMMWidgetZone1C";
import { FourFrameworkZone1D } from "./FourFrameworkZone1D";
import { useScenarioStepStore } from "../store/scenarioStepStore";
import type { TrajectoryResponse, TrajectoryFrameworkPoint } from "../store/scenarioStepStore";

const API_BASE = "http://localhost:8000/api/v1";

// ---------------------------------------------------------------------------
// Trajectory response parsing
// ---------------------------------------------------------------------------

interface RawFrameworkPoint {
  framework: string;
  composite_score: string | null;
  ci_lower: string | null;
  ci_upper: string | null;
  confidence_tier: number;
  scoring_basis: "percentile_rank" | "normalized_absolute" | "boundary_proximity";
}

interface RawTrajectoryStep {
  step_index: number;
  effective_from: string;
  step_event_label: string | null;
  step_significance: "SIGNIFICANT" | "ROUTINE";
  frameworks: RawFrameworkPoint[];
}

interface RawTrajectoryResponse {
  scenario_id: string;
  entity_id: string;
  step_count: number;
  mda_floors: Array<{
    framework: string;
    floor_value: string;
    severity: "WARNING" | "CRITICAL";
    label: string;
  }>;
  steps: RawTrajectoryStep[];
}

function parseTrajectoryResponse(raw: RawTrajectoryResponse): TrajectoryResponse {
  return {
    scenario_id: raw.scenario_id,
    entity_id: raw.entity_id,
    step_count: raw.step_count,
    mda_floors: raw.mda_floors.map((f) => ({
      framework: f.framework,
      floor_value: parseFloat(f.floor_value),
      label: f.label,
      severity: f.severity,
    })),
    steps: raw.steps.map((step) => {
      const frameworkMap: Record<string, TrajectoryFrameworkPoint> = {};
      for (const fw of step.frameworks) {
        frameworkMap[fw.framework] = {
          composite_score:
            fw.composite_score !== null ? parseFloat(fw.composite_score) : null,
          ci_lower: fw.ci_lower !== null ? parseFloat(fw.ci_lower) : null,
          ci_upper: fw.ci_upper !== null ? parseFloat(fw.ci_upper) : null,
          confidence_tier: fw.confidence_tier,
          scoring_basis:
            fw.scoring_basis === "boundary_proximity"
              ? "normalized_absolute"
              : fw.scoring_basis,
        };
      }
      return {
        step_index: step.step_index,
        effective_from: step.effective_from,
        step_event_label: step.step_event_label,
        step_significance: step.step_significance,
        frameworks: frameworkMap,
      };
    }),
  };
}

// ---------------------------------------------------------------------------
// ScenarioInstrumentCluster
// ---------------------------------------------------------------------------

interface ScenarioInstrumentClusterProps {
  scenarioId: string;
  stepCount: number;
  currentStep: number;
  entityIds?: string[];
}

export function ScenarioInstrumentCluster({
  scenarioId,
  stepCount,
  currentStep,
  entityIds,
}: ScenarioInstrumentClusterProps) {
  const store = useScenarioStepStore();

  // Initialise store when scenario changes
  useEffect(() => {
    store.setScenario(scenarioId, stepCount, "MODE_1");
  }, [scenarioId, stepCount]);

  // Keep current_step in sync with ScenarioControls (prop-driven)
  useEffect(() => {
    if (currentStep !== store.current_step) {
      useScenarioStepStore.setState({ current_step: currentStep });
    }
  }, [currentStep]);

  // Fetch trajectory when scenario changes
  useEffect(() => {
    if (!scenarioId) return;
    let cancelled = false;

    fetch(`${API_BASE}/scenarios/${encodeURIComponent(scenarioId)}/trajectory`)
      .then((res) => (res.ok ? (res.json() as Promise<RawTrajectoryResponse>) : null))
      .then((raw) => {
        if (cancelled || !raw) return;
        store.setTrajectory(parseTrajectoryResponse(raw));
      })
      .catch(() => {
        // Non-fatal — TrajectoryView renders empty state when trajectory is null
      });

    return () => {
      cancelled = true;
    };
  }, [scenarioId]);

  return (
    <InstrumentCluster
      entityIds={entityIds}
      mdaPanel={<MDAAlertPanelZone1B columnWidth={240} />}
      pmmWidget={<PMMWidgetZone1C />}
      fourFramework={<FourFrameworkZone1D />}
    />
  );
}
