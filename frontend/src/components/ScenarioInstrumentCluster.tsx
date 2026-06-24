/* eslint-disable react-hooks/set-state-in-effect */
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
 *
 * Mode 3 (G6b, Issue #753): When mode === "MODE_3", the ControlPlane is
 * rendered below the instrument cluster. Parameter changes trigger a branch
 * via POST /scenarios/{id}/branch. The advance loop runs step-by-step,
 * updating branch trajectory after each step (streaming reveal per spec §3b).
 * The recompute badge in the cluster header shows progress.
 */
import { useEffect, useRef, useState } from "react";
import { InstrumentCluster, LAYOUT, useViewportBreakpoint } from "./InstrumentCluster";
import { MDAAlertPanelZone1B, CohortImpactSection } from "./MDAAlertPanelZone1B";
import { PMMWidgetZone1C } from "./PMMWidgetZone1C";
import { FourFrameworkZone1D } from "./FourFrameworkZone1D";
import { CohortIndicatorsPanel } from "./CohortIndicatorsPanel";
import { ControlPlane, type Mode3Params } from "./ControlPlane";
import { useScenarioStepStore } from "../store/scenarioStepStore";
import type { TrajectoryResponse, TrajectoryFrameworkPoint, Zone1BAlert, CohortThresholdCrossing } from "../store/scenarioStepStore";
import type { QuantitySchema, ScenarioDetailResponse } from "../types";
import type { FrameworkDataQuality } from "./FourFrameworkZone1D";

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
  indicator_name?: string;
  severity: "WARNING" | "CRITICAL" | "TERMINAL";
  floor_value: string;
  current_value: string;
  approach_pct_remaining: string;
  consecutive_breach_steps: number | null;
  recovery_horizon_years?: number | null;
}

interface RawCohortThresholdCrossing {
  quintile_key: string;
  cohort_label: string;
  indicator_key: string;
  indicator_label: string;
  severity: "CRITICAL" | "WARNING" | "WATCH";
  step_crossed: number;
  above_floor_pct: string;
  tier: number;
  source: string;
}

interface RawFrameworkOutputForAlerts {
  mda_alerts: RawMDAAlert[];
  indicators: Record<string, unknown>;
  cohort_threshold_crossings?: RawCohortThresholdCrossing[];
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
      const indicator_name =
        alert.indicator_name ??
        alert.indicator_key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
      alerts.push({
        mda_id: alert.mda_id,
        entity_id: raw.entity_id,
        indicator_key: alert.indicator_key,
        indicator_name,
        framework,
        severity: alert.severity,
        step_index: raw.step_index,
        cohort: null,
        causal_attribution: null,
        confidence_tier,
        floor_value: alert.floor_value,
        current_value: alert.current_value,
        approach_pct_remaining: alert.approach_pct_remaining,
        consecutive_breach_steps: alert.consecutive_breach_steps,
        recovery_horizon_years: alert.recovery_horizon_years ?? null,
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
  /** Mode 2 — ID of the comparison (baseline) scenario. When set, its trajectory is
   *  fetched and stored as baseline_trajectory so TrajectoryView renders the overlay. */
  comparisonScenarioId?: string | null;
  /** Mode 2 fiscal multiplier for the active scenario — displayed in identity header. */
  fiscalMultiplier?: number | null;
  /** Mode 3 Active Control — when true, ControlPlane is rendered and branching is enabled. */
  mode3Active?: boolean;
  /** ADR-015 §Component 2+3: scenario detail for AssumptionSurface and PE status. */
  activeScenarioDetail?: ScenarioDetailResponse | null;
}

export function ScenarioInstrumentCluster({
  scenarioId,
  stepCount,
  currentStep,
  entityIds,
  comparisonScenarioId,
  fiscalMultiplier,
  mode3Active = false,
  activeScenarioDetail,
}: ScenarioInstrumentClusterProps) {
  const store = useScenarioStepStore();
  const bp = useViewportBreakpoint();
  const coPrimaryWidth = LAYOUT[bp].coPrimary;
  const chartHeight = LAYOUT[bp].chartHeight;

  // Fetch lifecycle state for Zone 1D loading/error display (IR-006).
  // Local state — not Zustand — because this is fetch lifecycle, not simulation state.
  const [trajectoryLoading, setTrajectoryLoading] = useState(false);
  const [trajectoryError, setTrajectoryError] = useState(false);

  // Human development indicators for CohortIndicatorsPanel (Issue #747).
  // Single state object ensures current→prev swap is atomic (avoids stale closure).
  const [hdState, setHdState] = useState<{
    current: Record<string, QuantitySchema> | null;
    prev: Record<string, QuantitySchema> | null;
  }>({ current: null, prev: null });

  // ADR-015 §Component 1 — data-quality per framework for Zone 1D L0 annotations (DA-G5-1).
  const [dataQuality, setDataQuality] = useState<Record<string, FrameworkDataQuality> | null>(null);

  // ADR-015 §Component 3 — programme_survival_probability from measurement-output (DA-G5-4 Option A).
  // undefined = not yet fetched or PE not active; null = PE active but computation failed; string = value.
  const [pspValue, setPspValue] = useState<string | null | undefined>(undefined);
  const [pspTier, setPspTier] = useState<number | null>(null);

  // M16-G2 (#987) — political economy indicators for Zone 1D political risk sub-section.
  const [legitimacyValue, setLegitimacyValue] = useState<string | null | undefined>(undefined);
  const [legitimacyFloor, setLegitimacyFloor] = useState<string | null>(null);
  const [legitimacyDirection, setLegitimacyDirection] = useState<string | null>(null);
  const [eliteCaptureDirection, setEliteCaptureDirection] = useState<string | null>(null);
  const [eliteCaptureQualifier, setEliteCaptureQualifier] = useState<string | null>(null);

  // ADR-017 Phase 4 — per-entity trajectory maps for composite encoding.
  const [entityTrajectories, setEntityTrajectories] = useState<Record<string, TrajectoryResponse>>({});
  const [entityBaselineTrajectories, setEntityBaselineTrajectories] = useState<Record<string, TrajectoryResponse>>({});

  // Mode 3 branch advance loop — abortController cancels in-flight advances on cleanup.
  const branchAbortRef = useRef<AbortController | null>(null);

  // Track previous scenarioId to distinguish scenario change (full reset) from mode-only change.
  const prevScenarioIdRef = useRef<string>("");

  // Track Mode 3 activation to auto-save entity baselines when entering Mode 3.
  const prevMode3ActiveRef = useRef(false);
  // Deferred baseline save: when Mode 3 activates before entity trajectories are loaded,
  // save them on the next entityTrajectories update.
  const saveBaselineOnNextUpdateRef = useRef(false);

  // Initialise store when scenario changes (full reset) or update mode without resetting.
  // setScenario resets trajectory and current_step — calling it on mode changes would drop
  // the trajectory fetched after step advance and break Mode 3 comparison readout (DEMO-064).
  useEffect(() => {
    const mode: "MODE_1" | "MODE_2" | "MODE_3" = mode3Active
      ? "MODE_3"
      : fiscalMultiplier != null && fiscalMultiplier !== 1.0
        ? "MODE_2"
        : "MODE_1";
    if (prevScenarioIdRef.current !== scenarioId) {
      prevScenarioIdRef.current = scenarioId;
      store.setScenario(scenarioId, stepCount, mode);
    } else {
      // Mode changed for same scenario — preserve trajectory and current_step.
      useScenarioStepStore.setState({ mode });
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps -- store is a Zustand singleton, stable reference
  }, [scenarioId, stepCount, fiscalMultiplier, mode3Active]);

  // Keep current_step in sync with ScenarioControls (prop-driven)
  useEffect(() => {
    if (currentStep !== store.current_step) {
      useScenarioStepStore.setState({ current_step: currentStep });
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps -- store is a Zustand singleton, stable reference
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
  // eslint-disable-next-line react-hooks/exhaustive-deps -- store is a Zustand singleton, stable reference
  }, [scenarioId, currentStep]);

  // ADR-017 Phase 4 — per-entity trajectory fetch for composite encoding (N > 1).
  // Fetches trajectory for each entity using ?entity_id= query param.
  // Skipped at step 0 (no snapshots yet) and when only one entity is loaded.
  useEffect(() => {
    const ids = entityIds ?? [];
    if (!scenarioId || currentStep === 0 || ids.length <= 1) return;
    let cancelled = false;

    Promise.all(
      ids.map((entityId) =>
        fetch(
          `${API_BASE}/scenarios/${encodeURIComponent(scenarioId)}/trajectory?entity_id=${encodeURIComponent(entityId)}`
        )
          .then((res) => (res.ok ? (res.json() as Promise<RawTrajectoryResponse>) : null))
          .then((raw) => (raw ? parseTrajectoryResponse(raw) : null))
          .catch(() => null)
      )
    ).then((trajectories) => {
      if (cancelled) return;
      const map: Record<string, TrajectoryResponse> = {};
      ids.forEach((entityId, i) => {
        const traj = trajectories[i];
        if (traj) map[entityId] = traj;
      });
      setEntityTrajectories(map);
    });

    return () => { cancelled = true; };
  // eslint-disable-next-line react-hooks/exhaustive-deps -- store is a Zustand singleton, stable reference
  }, [scenarioId, currentStep, entityIds]);

  // ADR-017 Phase 4 — deferred baseline save when entity trajectories arrive after Mode 3 activation.
  useEffect(() => {
    if (!saveBaselineOnNextUpdateRef.current) return;
    if (Object.keys(entityTrajectories).length === 0) return;
    setEntityBaselineTrajectories({ ...entityTrajectories });
    saveBaselineOnNextUpdateRef.current = false;
  }, [entityTrajectories]);

  // ADR-017 Phase 4 — Mode 3 auto-baseline for multi-entity composite encoding.
  // When entering Mode 3 with N > 1, lock current entity trajectories as baseline
  // so CompositeChartSVG can render ghost (baseline) + active paths.
  // N=1 Mode 3: Zustand store's baseline_trajectory handles ghost (set by applyControlInput).
  useEffect(() => {
    const ids = entityIds ?? [];
    if (mode3Active && !prevMode3ActiveRef.current && ids.length > 1) {
      if (Object.keys(entityTrajectories).length > 0) {
        setEntityBaselineTrajectories({ ...entityTrajectories });
      } else {
        // Entity trajectories not yet loaded — save on next update
        saveBaselineOnNextUpdateRef.current = true;
      }
    }
    if (!mode3Active) {
      setEntityBaselineTrajectories({});
      saveBaselineOnNextUpdateRef.current = false;
    }
    prevMode3ActiveRef.current = mode3Active;
  // eslint-disable-next-line react-hooks/exhaustive-deps -- entityTrajectories dep handled by the deferred-save effect
  }, [mode3Active, entityIds]);

  // Reset per-entity trajectory state on scenario change.
  useEffect(() => {
    setEntityTrajectories({});
    setEntityBaselineTrajectories({});
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [scenarioId]);

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
  // eslint-disable-next-line react-hooks/exhaustive-deps -- store is a Zustand singleton, stable reference
  }, [currentStep, store.trajectory]);

  // Fetch comparison scenario trajectory for Mode 2 overlay (#746).
  // When comparisonScenarioId changes, fetch its latest trajectory and store as baseline.
  // Clears baseline when comparisonScenarioId is removed.
  useEffect(() => {
    if (!comparisonScenarioId) {
      useScenarioStepStore.setState({ baseline_trajectory: null });
      return;
    }
    let cancelled = false;
    fetch(`${API_BASE}/scenarios/${encodeURIComponent(comparisonScenarioId)}/trajectory`)
      .then((res) => (res.ok ? (res.json() as Promise<RawTrajectoryResponse>) : null))
      .then((raw) => {
        if (cancelled || !raw) return;
        useScenarioStepStore.setState({ baseline_trajectory: parseTrajectoryResponse(raw) });
      })
      .catch(() => {
        // Non-fatal — baseline overlay stays absent
      });
    return () => { cancelled = true; };
  }, [comparisonScenarioId]);

  // ADR-015 §Component 1 — fetch data-quality for Zone 1D L0 source annotations (DA-G5-1).
  // Triggered when entity_id becomes available from the trajectory response.
  // Source institution is per-entity (not per-step), so one fetch per entity suffices.
  useEffect(() => {
    const entityId = store.trajectory?.entity_id;
    const startYear = activeScenarioDetail?.configuration?.start_date
      ? parseInt(activeScenarioDetail.configuration.start_date.slice(0, 4), 10)
      : null;
    if (!entityId || !startYear) return;
    let cancelled = false;

    fetch(
      `${API_BASE}/entities/${encodeURIComponent(entityId)}/data-quality?year=${startYear}`
    )
      .then((res) => (res.ok ? (res.json() as Promise<{ frameworks: Array<{ framework: string; source_institution: string | null; data_vintage: string | null; confidence_tier?: number | null }> }>) : null))
      .then((raw) => {
        if (cancelled || !raw) return;
        const byFramework: Record<string, FrameworkDataQuality> = {};
        for (const fw of raw.frameworks) {
          byFramework[fw.framework] = {
            source_institution: fw.source_institution,
            data_vintage: fw.data_vintage,
            confidence_tier: fw.confidence_tier ?? null,
          };
        }
        setDataQuality(byFramework);
      })
      .catch(() => {
        // Non-fatal — annotations degrade gracefully (no source name shown)
      });

    return () => { cancelled = true; };
  // eslint-disable-next-line react-hooks/exhaustive-deps -- store is a Zustand singleton, stable reference
  }, [store.trajectory?.entity_id, activeScenarioDetail?.configuration?.start_date]);

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

        // Extract human development indicators for cohort panel (Issue #747).
        // indicators is Record<string, QuantitySchema | Record<string, QuantitySchema>>;
        // only flat (non-nested) entries are QuantitySchema — nested cohort objects are skipped.
        const hdOutput = raw.outputs["human_development"];
        if (hdOutput) {
          const flat: Record<string, QuantitySchema> = {};
          for (const [k, v] of Object.entries(hdOutput.indicators)) {
            if (
              v !== null &&
              typeof v === "object" &&
              "value" in v &&
              typeof (v as { value: unknown }).value === "string"
            ) {
              flat[k] = v as QuantitySchema;
            }
          }
          // Atomic current→prev swap via functional updater — avoids stale closure
          setHdState((s) => ({ prev: s.current, current: flat }));
        }

        // M16-G2 (#986) — extract cohort threshold crossings from human_development output.
        const hdCrossings = (hdOutput?.cohort_threshold_crossings ?? []) as RawCohortThresholdCrossing[];
        const parsedCrossings: CohortThresholdCrossing[] = hdCrossings.map((c) => ({
          quintile_key: c.quintile_key,
          cohort_label: c.cohort_label,
          indicator_key: c.indicator_key,
          indicator_label: c.indicator_label,
          severity: c.severity,
          step_crossed: c.step_crossed,
          above_floor_pct: c.above_floor_pct,
          tier: c.tier,
          source: c.source,
        }));
        store.setCohortThresholdCrossings(parsedCrossings);

        // ADR-015 §Component 3 — extract programme_survival_probability (DA-G5-4 Option A).
        // M16-G2 (#987) — also extract legitimacy_index and elite_capture_divergence.
        const peOutput = raw.outputs["political_economy"];
        const peEnabled = activeScenarioDetail?.configuration?.modules_config?.political_economy?.enabled;
        if (peOutput && peEnabled) {
          const pspEntry = peOutput.indicators["programme_survival_probability"];
          if (
            pspEntry !== null &&
            pspEntry !== undefined &&
            typeof pspEntry === "object" &&
            "value" in pspEntry
          ) {
            const entry = pspEntry as { value: string | null; confidence_tier?: number | null };
            setPspValue(entry.value);
            setPspTier(
              typeof entry.confidence_tier === "number" ? entry.confidence_tier : null,
            );
          } else {
            setPspValue(null);
            setPspTier(null);
          }

          // M16-G2 (#987) — legitimacy_index
          const legEntry = peOutput.indicators["legitimacy_index"];
          if (legEntry !== null && legEntry !== undefined && typeof legEntry === "object") {
            const leg = legEntry as { value?: string | null; floor?: string | null; direction?: string | null };
            setLegitimacyValue(leg.value ?? null);
            setLegitimacyFloor(leg.floor ?? null);
            setLegitimacyDirection(leg.direction ?? null);
          } else {
            setLegitimacyValue(null);
            setLegitimacyFloor(null);
            setLegitimacyDirection(null);
          }

          // M16-G2 (#987) — elite_capture_divergence
          const ecEntry = peOutput.indicators["elite_capture_divergence"];
          if (ecEntry !== null && ecEntry !== undefined && typeof ecEntry === "object") {
            const ec = ecEntry as { direction?: string | null; qualifier?: string | null };
            setEliteCaptureDirection(ec.direction ?? null);
            setEliteCaptureQualifier(ec.qualifier ?? null);
          } else {
            setEliteCaptureDirection(null);
            setEliteCaptureQualifier(null);
          }
        } else if (!peEnabled) {
          // PE not enabled — reset all PE state
          setPspValue(undefined);
          setPspTier(null);
          setLegitimacyValue(undefined);
          setLegitimacyFloor(null);
          setLegitimacyDirection(null);
          setEliteCaptureDirection(null);
          setEliteCaptureQualifier(null);
        }
      })
      .catch(() => {
        // Non-fatal — Zone 1B and cohort panel remain in previous state
      });

    return () => {
      cancelled = true;
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps -- store is a Zustand singleton, stable reference
  }, [scenarioId, currentStep, store.trajectory?.entity_id, activeScenarioDetail?.configuration?.modules_config?.political_economy?.enabled]);

  // ---------------------------------------------------------------------------
  // Mode 3 — branch-and-recompute advance loop (G6b, Issue #753)
  // ---------------------------------------------------------------------------

  const handleApplyControlChange = async (params: Mode3Params) => {
    // Cancel any in-flight advance loop.
    branchAbortRef.current?.abort();
    const abortController = new AbortController();
    branchAbortRef.current = abortController;

    // Signal pending immediately so the badge appears within the 2-second AC-4 ceiling,
    // before the branch POST returns (which may take several seconds on slow connections).
    useScenarioStepStore.setState({ recomputeStatus: "pending" });

    const { branchScenarioId } = store;

    try {
      let branchId: string;
      let fromStep: number;
      let nSteps: number;

      if (branchScenarioId == null) {
        // First branch: POST /scenarios/{baselineId}/branch
        const res = await fetch(
          `${API_BASE}/scenarios/${encodeURIComponent(scenarioId)}/branch`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              fiscal_multiplier: params.fiscal_multiplier,
              branch_from_step: params.branch_from_step,
            }),
          },
        );
        if (!res.ok) throw new Error(`Branch failed: ${res.status}`);
        const data = (await res.json()) as {
          branch_scenario_id: string;
          branch_from_step: number;
          n_steps: number;
        };
        branchId = data.branch_scenario_id;
        fromStep = data.branch_from_step;
        nSteps = data.n_steps;
        // Set baseline trajectory = current scenario's trajectory (lock it in)
        if (store.trajectory) {
          useScenarioStepStore.setState({ baseline_trajectory: store.trajectory });
        }
        store.initBranch(scenarioId, branchId, fromStep);
      } else {
        // Re-branch: POST /scenarios/{branchId}/rebranch
        const res = await fetch(
          `${API_BASE}/scenarios/${encodeURIComponent(branchScenarioId)}/rebranch`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              fiscal_multiplier: params.fiscal_multiplier,
              from_step: params.branch_from_step,
            }),
          },
        );
        if (!res.ok) throw new Error(`Rebranch failed: ${res.status}`);
        const data = (await res.json()) as {
          branch_scenario_id: string;
          branch_from_step: number;
          n_steps: number;
        };
        branchId = data.branch_scenario_id;
        fromStep = data.branch_from_step;
        nSteps = data.n_steps;
        store.initBranch(
          store.baselineScenarioId ?? scenarioId,
          branchId,
          fromStep,
        );
      }

      // Advance loop: run one step at a time, fetch trajectory after each.
      let stepsComputed = 0;
      for (let step = fromStep + 1; step <= nSteps; step++) {
        if (abortController.signal.aborted) return;

        const advRes = await fetch(
          `${API_BASE}/scenarios/${encodeURIComponent(branchId)}/advance`,
          { method: "POST" },
        );
        if (!advRes.ok) throw new Error(`Advance failed at step ${step}: ${advRes.status}`);

        // Fetch branch trajectory for streaming reveal.
        const trajRes = await fetch(
          `${API_BASE}/scenarios/${encodeURIComponent(branchId)}/trajectory`,
        );
        if (trajRes.ok) {
          const raw = (await trajRes.json()) as RawTrajectoryResponse;
          if (!abortController.signal.aborted) {
            useScenarioStepStore.setState({ trajectory: parseTrajectoryResponse(raw) });
          }
        }

        stepsComputed++;
        store.updateBranchProgress(stepsComputed);
      }

      if (!abortController.signal.aborted) {
        store.setBranchComplete();
      }
    } catch {
      if (!abortController.signal.aborted) {
        store.setBranchFailed();
      }
    }
  };

  const { recomputeStatus, branchFromStep, branchStepsComputed, step_count, mode } = store;
  const totalBranchSteps = branchFromStep != null ? step_count - branchFromStep : 0;
  const isRecomputing = recomputeStatus === "computing" || recomputeStatus === "pending";

  return (
    <div>
      {/* Recompute badge — visible during Mode 3 branch recompute (spec §3a). */}
      {mode === "MODE_3" && (isRecomputing || recomputeStatus === "failed") && (
        <div
          data-testid="recompute-badge"
          style={{
            padding: "4px 10px",
            background: recomputeStatus === "failed" ? "#fee2e2" : "#ede9fe",
            borderBottom: `1px solid ${recomputeStatus === "failed" ? "#fca5a5" : "#c4b5fd"}`,
            display: "flex",
            alignItems: "center",
            gap: 8,
            fontSize: 11,
            color: recomputeStatus === "failed" ? "#dc2626" : "#7c3aed",
            fontWeight: 600,
          }}
        >
          {recomputeStatus === "failed" ? (
            <>
              <span style={{ fontSize: 14 }}>⚠</span>
              <span>Recompute failed</span>
              <button
                data-testid="recompute-error-dismiss"
                onClick={() => store.resetBranch()}
                style={{
                  marginLeft: "auto",
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  color: "#dc2626",
                  fontSize: 11,
                  fontWeight: 600,
                }}
              >
                Dismiss ×
              </button>
            </>
          ) : (
            <>
              <span
                data-testid="recompute-pulse"
                style={{
                  display: "inline-block",
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: "#7c3aed",
                  animation: "pulse 1.2s infinite",
                }}
              />
              {recomputeStatus === "pending" ? (
                <span>Recompute pending — advance step to see updated trajectory</span>
              ) : (
                <>
                  <span>Recomputing…</span>
                  {totalBranchSteps > 0 && (
                    <span
                      data-testid="recompute-step-progress"
                      style={{ fontWeight: 400, color: "#9d78ef" }}
                    >
                      Computing step {branchStepsComputed + 1} of {totalBranchSteps}
                    </span>
                  )}
                </>
              )}
            </>
          )}
        </div>
      )}

      {/* Mode 3 comparison readout — shows labeled baseline vs. branch values (DEMO-064).
          Visible when branch is applied and recompute has completed. */}
      {mode === "MODE_3" && branchFromStep !== null && !isRecomputing && recomputeStatus !== "failed" && (() => {
        const currentStepIdx = store.current_step;
        const activeStep = store.trajectory?.steps.find(s => s.step_index === currentStepIdx)
          ?? store.trajectory?.steps.at(-1);
        const baseStep = store.baseline_trajectory?.steps.find(s => s.step_index === currentStepIdx)
          ?? store.baseline_trajectory?.steps.at(-1);
        const activeScore = activeStep?.frameworks["financial"]?.composite_score ?? null;
        const baseScore = baseStep?.frameworks["financial"]?.composite_score ?? null;
        const delta = activeScore !== null && baseScore !== null ? activeScore - baseScore : null;
        const displayStep = activeStep?.step_index ?? baseStep?.step_index ?? currentStepIdx;
        return (
          <div
            data-testid="mode3-comparison-readout"
            style={{
              padding: "4px 10px",
              background: "#f8f4ff",
              borderBottom: "1px solid #e9d5ff",
              display: "flex",
              alignItems: "center",
              gap: 16,
              fontSize: 11,
              color: "#444",
            }}
          >
            <span style={{ fontWeight: 600, color: "#7c3aed", fontSize: 10, letterSpacing: 0.2 }}>
              Financial (step {displayStep})
            </span>
            <span>
              Baseline:{" "}
              <span data-testid="mode3-baseline-value" style={{ fontWeight: 700 }}>
                {baseScore !== null ? baseScore.toFixed(2) : "—"}
              </span>
            </span>
            <span>
              Branch:{" "}
              <span data-testid="mode3-branch-value" style={{ fontWeight: 700 }}>
                {activeScore !== null ? activeScore.toFixed(2) : "—"}
              </span>
            </span>
            {delta !== null && (
              <span style={{ color: delta > 0 ? "#2271B3" : "#cc0000", fontWeight: 700 }}>
                {delta > 0 ? "+" : ""}{delta.toFixed(2)}
              </span>
            )}
          </div>
        );
      })()}

      <InstrumentCluster
        entityIds={entityIds}
        chartHeight={chartHeight}
        entityTrajectories={entityTrajectories}
        entityBaselineTrajectories={entityBaselineTrajectories}
        mdaPanel={
          <MDAAlertPanelZone1B
            columnWidth={coPrimaryWidth}
          />
        }
        zone1bCohortSection={<CohortImpactSection isCompleted={activeScenarioDetail?.status === "completed"} />}
        pmmWidget={<PMMWidgetZone1C />}
        fourFramework={
          <FourFrameworkZone1D
            isLoading={trajectoryLoading}
            isError={trajectoryError}
            entityIds={entityIds}
            dataQuality={dataQuality}
            peEnabled={activeScenarioDetail?.configuration?.modules_config?.political_economy?.enabled ?? false}
            pspValue={pspValue}
            pspTier={pspTier}
            legitimacyValue={legitimacyValue}
            legitimacyFloor={legitimacyFloor}
            legitimacyDirection={legitimacyDirection}
            eliteCaptureDirection={eliteCaptureDirection}
            eliteCaptureQualifier={eliteCaptureQualifier}
          />
        }
        cohortPanel={
          <CohortIndicatorsPanel
            indicators={hdState.current}
            prevIndicators={hdState.prev}
          />
        }
      />

      {/* ControlPlane — rendered in Mode 3 only (G6b, Issue #753). */}
      {mode === "MODE_3" && (
        <ControlPlane
          onApplyChange={handleApplyControlChange}
          currentStep={currentStep}
        />
      )}
    </div>
  );
}
