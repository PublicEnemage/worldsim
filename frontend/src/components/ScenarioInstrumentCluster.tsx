/**
 * ScenarioInstrumentCluster — composed Zone 1 cluster for App.tsx.
 *
 * Wires all four Zone 1 instruments into InstrumentCluster and connects
 * the Zustand atom to the trajectory API. Fetches trajectory after each
 * step advance (currentStep > 0); skips step 0 where the API returns 409.
 * Keeps store current_step in sync with ScenarioControls.
 *
 * Trajectory parsing: the API returns frameworks as an array; the store
 * expects Record<string, TrajectoryFrameworkPoint>. composite_score arrives
 * as Decimal string; the store expects number | null. Both conversions
 * happen in parseTrajectoryResponse().
 *
 * MDA alerts: Zone 1B alerts are fetched from GET /measurement-output after
 * each step advance (IR-001). Alerts are absent at step 0 (no simulation
 * output yet). Mapping from MDAAlert → Zone1BAlert derives framework from
 * the output record key and confidence_tier from the indicator record.
 *
 * PMM: pmm_value and pmm_direction are populated from per-step PMM data
 * embedded in the trajectory response (Issue #496). Synced via useEffect
 * on currentStep + store.trajectory. Null at step 0 or when no MDA
 * thresholds have matching indicator data for the step.
 */
import React, { useEffect, useState } from "react";
import { InstrumentCluster } from "./InstrumentCluster";
import { MDAAlertPanelZone1B } from "./MDAAlertPanelZone1B";
import { PMMWidgetZone1C } from "./PMMWidgetZone1C";
import { FourFrameworkZone1D } from "./FourFrameworkZone1D";
import { useScenarioStepStore } from "../store/scenarioStepStore";
import type { TrajectoryResponse, TrajectoryFrameworkPoint, Zone1BAlert } from "../store/scenarioStepStore";

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
  pmm: { value: string; direction: string } | null;
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
      const pmm =
        step.pmm !== null && step.pmm !== undefined
          ? {
              value: parseFloat(step.pmm.value),
              direction: step.pmm.direction as "up" | "down" | "flat",
            }
          : null;

      return {
        step_index: step.step_index,
        effective_from: step.effective_from,
        step_event_label: step.step_event_label,
        step_significance: step.step_significance,
        frameworks: frameworkMap,
        pmm,
      };
    }),
  };
}

// ---------------------------------------------------------------------------
// MDA alert response parsing (IR-001)
// ---------------------------------------------------------------------------

interface RawMDAAlert {
  mda_id: string;
  entity_id: string;
  indicator_key: string;
  severity: "WARNING" | "CRITICAL" | "TERMINAL";
  floor_value: string;
  current_value: string;
  approach_pct_remaining: string;
  consecutive_breach_steps: number;
}

interface RawFrameworkOutputForAlerts {
  mda_alerts: RawMDAAlert[];
  indicators: Record<string, unknown>;
}

interface RawMultiFrameworkOutput {
  entity_id: string;
  step_index: number;
  outputs: Record<string, RawFrameworkOutputForAlerts>;
}

function parseMdaAlerts(raw: RawMultiFrameworkOutput): Zone1BAlert[] {
  const alerts: Zone1BAlert[] = [];
  for (const [framework, output] of Object.entries(raw.outputs)) {
    for (const alert of output.mda_alerts) {
      const indicator = output.indicators[alert.indicator_key];
      const confidence_tier =
        indicator != null &&
        typeof indicator === "object" &&
        "confidence_tier" in indicator &&
        typeof (indicator as { confidence_tier: unknown }).confidence_tier === "number"
          ? (indicator as { confidence_tier: number }).confidence_tier
          : 2;
      alerts.push({
        mda_id: alert.mda_id,
        indicator_key: alert.indicator_key,
        framework,
        severity: alert.severity,
        step_index: raw.step_index,
        cohort: null,
        causal_attribution: null,
        confidence_tier,
      });
    }
  }
  return alerts;
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

  // Fetch lifecycle state for Zone 1D loading/error display (IR-006).
  // Local state — not Zustand — because this is fetch lifecycle, not simulation state.
  const [trajectoryLoading, setTrajectoryLoading] = useState(false);
  const [trajectoryError, setTrajectoryError] = useState(false);

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

  // Fetch trajectory after each step advance.
  // Skipped at step 0 — no snapshots exist before the first advance (API returns 409).
  useEffect(() => {
    if (!scenarioId || currentStep === 0) return;
    let cancelled = false;

    setTrajectoryLoading(true);
    setTrajectoryError(false);

    fetch(`${API_BASE}/scenarios/${encodeURIComponent(scenarioId)}/trajectory`)
      .then((res) => {
        if (!res.ok) throw new Error(`trajectory fetch failed: ${res.status}`);
        return res.json() as Promise<RawTrajectoryResponse>;
      })
      .then((raw) => {
        if (cancelled) return;
        store.setTrajectory(parseTrajectoryResponse(raw));
        setTrajectoryLoading(false);
      })
      .catch(() => {
        if (cancelled) return;
        setTrajectoryLoading(false);
        setTrajectoryError(true);
      });

    return () => {
      cancelled = true;
    };
  }, [scenarioId, currentStep]);

  // Sync PMM from trajectory step data when current step changes (Issue #496).
  // PMM is pre-computed per step by the backend; no additional fetch needed.
  useEffect(() => {
    const traj = store.trajectory;
    if (!traj || currentStep === 0) {
      store.setPmmState(null, null);
      return;
    }
    const step = traj.steps.find((s) => s.step_index === currentStep);
    if (step?.pmm != null) {
      store.setPmmState(step.pmm.value, step.pmm.direction);
    } else {
      store.setPmmState(null, null);
    }
  }, [currentStep, store.trajectory]);

  // Fetch MDA alerts from measurement-output after each step advance (IR-001).
  // Entity ID comes from the trajectory response already fetched above.
  // Skipped at step 0 — no simulation output exists before the first advance.
  useEffect(() => {
    const entityId = store.trajectory?.entity_id;
    if (!scenarioId || !entityId || currentStep === 0) return;
    let cancelled = false;

    fetch(
      `${API_BASE}/scenarios/${encodeURIComponent(scenarioId)}/measurement-output?entity_id=${encodeURIComponent(entityId)}&step=${currentStep}`
    )
      .then((res) => (res.ok ? (res.json() as Promise<RawMultiFrameworkOutput>) : null))
      .then((raw) => {
        if (cancelled || !raw) return;
        store.setMdaAlerts(parseMdaAlerts(raw));
      })
      .catch(() => {
        // Non-fatal — Zone 1B remains in previous state
      });

    return () => {
      cancelled = true;
    };
  }, [scenarioId, currentStep, store.trajectory?.entity_id]);

  return (
    <InstrumentCluster
      entityIds={entityIds}
      mdaPanel={<MDAAlertPanelZone1B columnWidth={240} />}
      pmmWidget={<PMMWidgetZone1C />}
      fourFramework={
        <FourFrameworkZone1D
          isLoading={trajectoryLoading}
          isError={trajectoryError}
        />
      }
    />
  );
}
