/* eslint-disable react-refresh/only-export-components */
/**
 * TrajectoryView — Zone 1A primary instrument.
 *
 * Implements: ADR-010 Decisions 1–10, FA brief §TrajectoryView.
 * Design decisions: DD-012 (Zustand atom), DD-013 (divergence fill), DD-014 (step annotation).
 * Framework colors: frameworkColors.ts (UX Designer ruling, MV-001 closed 2026-05-23).
 */
import { useMemo, useLayoutEffect, useRef, useState } from "react";
import {
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import { FRAMEWORK_COLORS, type FrameworkKey } from "../constants/frameworkColors";
import {
  useScenarioStepStore,
  type TrajectoryStep,
  type TrajectoryResponse,
  type MDAFloor,
} from "../store/scenarioStepStore";

// ---------------------------------------------------------------------------
// Exported constants and pure functions (tested by TrajectoryView.test.ts)
// ---------------------------------------------------------------------------

/** All four framework keys in display-priority order. */
export const FRAMEWORKS: readonly FrameworkKey[] = [
  "financial",
  "human_development",
  "ecological",
  "governance",
] as const;

/** connectNulls prop value — must be literally false (AC-015). */
export const CONNECT_NULLS = false as const;

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

// ---------------------------------------------------------------------------
// Phase 4 — composite encoding constants and helpers (ADR-017 §Decision table)
// ---------------------------------------------------------------------------

/** Entity color palette indexed by position in entityIds (max 4 entities per ADR-017). */
const ENTITY_PALETTE: readonly string[] = [
  FRAMEWORK_COLORS.financial,          // #2271B3 — entity 0
  FRAMEWORK_COLORS.ecological,         // #1A8FA0 — entity 1
  FRAMEWORK_COLORS.human_development,  // #D4841A — entity 2
  FRAMEWORK_COLORS.governance,         // #7B50A8 — entity 3
] as const;

/** Mean of non-null framework composite_scores at a step. */
function computeEntityCompositeScore(step: TrajectoryStep): number | null {
  const scores = Object.values(step.frameworks)
    .map((fw) => fw.composite_score)
    .filter((s): s is number => s !== null);
  if (scores.length === 0) return null;
  return scores.reduce((a, b) => a + b, 0) / scores.length;
}

/** Worst (highest-number) confidence tier across all frameworks at a step. */
function getEntityWorstTier(step: TrajectoryStep): number {
  const tiers = Object.values(step.frameworks).map((fw) => fw.confidence_tier);
  if (tiers.length === 0) return 3;
  return Math.max(...tiers);
}

/** Lowest non-trivial MDA floor value (0 < value < 1) across all frameworks. */
function getEntityMdaFloor(mda_floors: MDAFloor[]): number | null {
  const floors = mda_floors.map((f) => f.floor_value).filter((v) => v > 0 && v < 1.0);
  if (floors.length === 0) return null;
  return Math.min(...floors);
}

// ---------------------------------------------------------------------------
// Internal types
// ---------------------------------------------------------------------------

interface MergedStepDatum {
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
}

// ---------------------------------------------------------------------------
// Data merging
// ---------------------------------------------------------------------------

function mergeTrajectories(
  active: TrajectoryResponse,
  baseline: TrajectoryResponse | null,
): MergedStepDatum[] {
  const baselineByStep = new Map<number, TrajectoryStep>();
  if (baseline) {
    for (const step of baseline.steps) {
      baselineByStep.set(step.step_index, step);
    }
  }

  return active.steps.map((step) => {
    const bStep = baselineByStep.get(step.step_index) ?? null;

    const get = (
      source: TrajectoryStep | null,
      fw: string,
    ): number | null => source?.frameworks[fw]?.composite_score ?? null;

    const tier = (fw: string): number =>
      step.frameworks[fw]?.confidence_tier ?? 1;

    const basis = (fw: string): string =>
      step.frameworks[fw]?.scoring_basis ?? "percentile_rank";

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
    };
  });
}

// ---------------------------------------------------------------------------
// Custom XAxis tick — Mode 1 step annotation (FA-C5, UD-R2)
// ---------------------------------------------------------------------------

interface CustomTickProps {
  x?: number;
  y?: number;
  payload?: { value: number };
  data: MergedStepDatum[];
  entityIds?: string[];
}

function CustomStepTick({ x = 0, y = 0, payload, data, entityIds }: CustomTickProps) {
  if (!payload) return null;
  const step = data.find((d) => d.step_index === payload.value);
  if (!step) return null;

  const isSig = step.step_significance === "SIGNIFICANT";
  const label = step.step_event_label;
  // Truncate at 31 chars + ellipsis if backend violates 32-char constraint (DD-014)
  const truncated = label && label.length > 32 ? label.slice(0, 31) + "…" : label;

  const dateStr = new Date(step.effective_from).toLocaleDateString("en-US", {
    month: "short",
    year: "numeric",
  });

  return (
    <g transform={`translate(${x},${y})`}>
      <text
        x={0}
        y={0}
        dy={12}
        textAnchor="middle"
        fill="#666"
        fontSize={11}
      >
        {`Step ${step.step_index}`}
      </text>
      {entityIds && entityIds.length === 2 ? (
        <>
          <text x={0} y={0} dy={24} textAnchor="middle" fill="#666" fontSize={11}>
            {`${entityIds[0]}: ${dateStr}`}
          </text>
          <text x={0} y={0} dy={36} textAnchor="middle" fill="#666" fontSize={11}>
            {`${entityIds[1]}: ${dateStr}`}
          </text>
          {isSig && truncated && (
            <text x={0} y={0} dy={48} textAnchor="middle" fill="#555" fontSize={10} fontStyle="italic">
              {truncated}
            </text>
          )}
        </>
      ) : (
        <>
          <text x={0} y={0} dy={24} textAnchor="middle" fill="#666" fontSize={11}>
            {dateStr}
          </text>
          {isSig && truncated && (
            <text x={0} y={0} dy={36} textAnchor="middle" fill="#555" fontSize={10} fontStyle="italic">
              {truncated}
            </text>
          )}
        </>
      )}
    </g>
  );
}

// ---------------------------------------------------------------------------
// Confidence badge — rendered as SVG <text> adjacent to rightmost data point
// Position: curve-face, 4px right of rightmost non-null point (UD-R3 / UD-F2)
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// TrajectoryView legend formatter
// ---------------------------------------------------------------------------

function legendFormatter(
  framework: FrameworkKey,
  scoringBasis: string,
  entityIds?: string[],
): string {
  const names: Record<FrameworkKey, string> = {
    financial: "Financial",
    human_development: "Human Development",
    ecological: "Ecological",
    governance: "Governance",
  };
  const base = names[framework];
  if (scoringBasis === "normalized_absolute") {
    return `${base} (single-country index)`;
  }
  if (entityIds && entityIds.length === 2) {
    return `${base} (${entityIds[0]} · ${entityIds[1]})`;
  }
  return base;
}

// ---------------------------------------------------------------------------
// Phase 4 — composite SVG chart (ADR-017 §Decision table rows N≤4)
// ---------------------------------------------------------------------------

interface CompositeChartSVGProps {
  entityCodes: string[];
  activeTrajectories: Record<string, TrajectoryResponse>;
  baselineTrajectories: Record<string, TrajectoryResponse>;
  mode: "MODE_1" | "MODE_2" | "MODE_3";
  width: number;
  height: number;
}

function CompositeChartSVG({
  entityCodes,
  activeTrajectories,
  baselineTrajectories,
  mode,
  width,
  height,
}: CompositeChartSVGProps) {
  const MARGIN = { top: 16, right: 60, bottom: 48, left: 44 };
  const chartW = width - MARGIN.left - MARGIN.right;
  const chartH = height - MARGIN.top - MARGIN.bottom;

  const refCode = entityCodes.find((c) => activeTrajectories[c]);
  const refSteps = refCode ? activeTrajectories[refCode].steps : [];
  const stepIndices = refSteps.map((s) => s.step_index);

  const xScale = (idx: number): number => {
    if (stepIndices.length <= 1) return MARGIN.left + chartW / 2;
    const i = stepIndices.indexOf(idx);
    if (i < 0) return MARGIN.left;
    return MARGIN.left + (i / (stepIndices.length - 1)) * chartW;
  };

  const yScale = (score: number): number =>
    MARGIN.top + (1 - Math.min(1, Math.max(0, score))) * chartH;

  const buildPathD = (steps: TrajectoryStep[]): string => {
    const pts: string[] = [];
    for (const step of steps) {
      const score = computeEntityCompositeScore(step);
      if (score === null) continue;
      pts.push(`${xScale(step.step_index).toFixed(1)},${yScale(score).toFixed(1)}`);
    }
    return pts.length >= 2 ? "M " + pts.join(" L ") : "";
  };

  const showBaseline =
    (mode === "MODE_2" || mode === "MODE_3") &&
    Object.keys(baselineTrajectories).length > 0;

  // Only render divergence fill when trajectories actually diverge (> 0.001 delta).
  // This prevents a zero-area fill element that would break bounding-box assertions.
  const hasDivergence =
    showBaseline &&
    entityCodes.some((code) => {
      const active = activeTrajectories[code];
      const baseline = baselineTrajectories[code];
      if (!active || !baseline) return false;
      const baselineByStep = new Map(baseline.steps.map((s) => [s.step_index, s]));
      return active.steps.some((step) => {
        const aScore = computeEntityCompositeScore(step);
        const bStep = baselineByStep.get(step.step_index);
        const bScore = bStep ? computeEntityCompositeScore(bStep) : null;
        return aScore !== null && bScore !== null && Math.abs(aScore - bScore) > 0.001;
      });
    });

  const yGridValues = [0, 0.25, 0.5, 0.75, 1.0];

  return (
    <svg width={width} height={height} style={{ display: "block", overflow: "visible" }}>
      {/* Y-axis grid and labels */}
      {yGridValues.map((val) => (
        <g key={val}>
          <line
            x1={MARGIN.left}
            y1={yScale(val)}
            x2={MARGIN.left + chartW}
            y2={yScale(val)}
            stroke="#f0f0f0"
            strokeWidth={1}
          />
          <text
            x={MARGIN.left - 4}
            y={yScale(val)}
            textAnchor="end"
            fontSize={9}
            fill="#888"
            dy={3}
          >
            {val.toFixed(2)}
          </text>
        </g>
      ))}

      {/* X-axis step ticks */}
      {stepIndices.map((idx) => (
        <g key={idx} transform={`translate(${xScale(idx)},${MARGIN.top + chartH})`}>
          <line y1={0} y2={4} stroke="#ccc" strokeWidth={1} />
          <text y={14} textAnchor="middle" fontSize={9} fill="#888">
            {`Step ${idx}`}
          </text>
        </g>
      ))}

      {/* Divergence fills — only rendered when hasDivergence */}
      {hasDivergence &&
        entityCodes.map((code, i) => {
          const active = activeTrajectories[code];
          const baseline = baselineTrajectories[code];
          if (!active || !baseline) return null;
          const baselineByStep = new Map(baseline.steps.map((s) => [s.step_index, s]));
          const fwdPts: string[] = [];
          const revPts: string[] = [];
          for (const step of active.steps) {
            const aScore = computeEntityCompositeScore(step);
            const bStep = baselineByStep.get(step.step_index);
            const bScore = bStep ? computeEntityCompositeScore(bStep) : null;
            if (aScore === null || bScore === null) continue;
            const x = xScale(step.step_index);
            fwdPts.push(`${x.toFixed(1)},${yScale(aScore).toFixed(1)}`);
            revPts.unshift(`${x.toFixed(1)},${yScale(bScore).toFixed(1)}`);
          }
          if (fwdPts.length < 2) return null;
          const fillD = "M " + fwdPts.join(" L ") + " L " + revPts.join(" L ") + " Z";
          const color = ENTITY_PALETTE[i % ENTITY_PALETTE.length];
          return (
            <path
              key={`fill-${code}`}
              data-testid="zone-1a-divergence-fill"
              d={fillD}
              fill={color}
              opacity={0.08}
              stroke="none"
            />
          );
        })}

      {/* MDA floor lines — one per entity (lowest non-trivial floor) */}
      {entityCodes.map((code, i) => {
        const active = activeTrajectories[code];
        if (!active) return null;
        const floor = getEntityMdaFloor(active.mda_floors);
        if (floor === null) return null;
        const color = ENTITY_PALETTE[i % ENTITY_PALETTE.length];
        return (
          <line
            key={`mda-${code}`}
            data-testid={`zone-1a-mda-floor-${code}`}
            x1={MARGIN.left}
            y1={yScale(floor)}
            x2={MARGIN.left + chartW}
            y2={yScale(floor)}
            stroke={color}
            strokeWidth={1}
            strokeDasharray="6 3"
            strokeOpacity={0.6}
          />
        );
      })}

      {/* Baseline ghost paths — Mode 2/3, opacity=0.5 + dasharray (ADR-017) */}
      {showBaseline &&
        entityCodes.map((code, i) => {
          const baseline = baselineTrajectories[code];
          if (!baseline) return null;
          const pathD = buildPathD(baseline.steps);
          if (!pathD) return null;
          const color = ENTITY_PALETTE[i % ENTITY_PALETTE.length];
          return (
            <path
              key={`ghost-${code}`}
              d={pathD}
              stroke={color}
              strokeWidth={1}
              opacity={0.5}
              strokeDasharray="4 2"
              fill="none"
            />
          );
        })}

      {/* Active composite paths — solid, full opacity */}
      {entityCodes.map((code, i) => {
        const active = activeTrajectories[code];
        if (!active) return null;
        const pathD = buildPathD(active.steps);
        if (!pathD) return null;
        const color = ENTITY_PALETTE[i % ENTITY_PALETTE.length];
        return (
          <path
            key={`active-${code}`}
            d={pathD}
            stroke={color}
            strokeWidth={2}
            opacity={1}
            fill="none"
          />
        );
      })}

      {/* Tier badges at right edge of each entity's active curve endpoint */}
      {entityCodes.map((code, i) => {
        const active = activeTrajectories[code];
        if (!active || active.steps.length === 0) return null;
        const lastStep = active.steps[active.steps.length - 1];
        const lastScore = computeEntityCompositeScore(lastStep);
        if (lastScore === null) return null;
        const tier = getEntityWorstTier(lastStep);
        const color = ENTITY_PALETTE[i % ENTITY_PALETTE.length];
        const x = MARGIN.left + chartW + 4;
        const y = yScale(lastScore);
        return (
          <text
            key={`tier-${code}`}
            data-testid={`zone-1a-tier-badge-${code}`}
            x={x}
            y={y}
            fontSize={9}
            fontWeight="bold"
            fill={color}
            dominantBaseline="middle"
          >
            T{tier}
          </text>
        );
      })}
    </svg>
  );
}

// ---------------------------------------------------------------------------
// TrajectoryView props
// ---------------------------------------------------------------------------

interface TrajectoryViewProps {
  /** Width of the trajectory view zone in px (480 at 1024×768, 580 at 1280×800). */
  width?: number;
  /** Chart height in px — defaults to 300. Increased at 1440px viewport (DEMO-061). */
  height?: number;
  /** Entity ISO 3166-1 alpha-3 codes — provide two for multi-case Mode 1. */
  entityIds?: string[];
  /**
   * Phase 4 (ADR-017): per-entity trajectory responses keyed by ISO entity code.
   * When provided for N>1 entities, composite encoding is used instead of recharts.
   */
  entityTrajectories?: Record<string, TrajectoryResponse> | null;
  /**
   * Phase 4 (ADR-017): per-entity baseline trajectories for Mode 3 ghost paths.
   * Keyed by ISO entity code. Empty object or null = no baseline overlay.
   */
  entityBaselineTrajectories?: Record<string, TrajectoryResponse> | null;
  /** M16-G4 #102 — when true, show the variance-band toggle button in Zone 1A. */
  comparisonMode?: boolean;
  /** test-id for AC-006 DOM assertions. */
  "data-testid"?: string;
}

// ---------------------------------------------------------------------------
// TrajectoryView
// ---------------------------------------------------------------------------

export function TrajectoryView({
  width,
  height = 300,
  entityIds,
  entityTrajectories,
  entityBaselineTrajectories,
  comparisonMode = false,
  "data-testid": dataTestId = "zone-1a-trajectory",
}: TrajectoryViewProps) {
  const { trajectory, baseline_trajectory, current_step, mode } =
    useScenarioStepStore();

  const mergedData = useMemo<MergedStepDatum[]>(() => {
    if (!trajectory) return [];
    return mergeTrajectories(trajectory, baseline_trajectory);
  }, [trajectory, baseline_trajectory]);

  const showBaseline = (mode === "MODE_2" || mode === "MODE_3") && baseline_trajectory !== null;

  // M16-G4 #102 — variance band toggle state (Zone 1A comparison mode).
  const [showVarianceBand, setShowVarianceBand] = useState(false);

  // Performance mark for AC-007 / MV-002.
  const perfMarkFired = useRef(false);
  useLayoutEffect(() => {
    if (mergedData.length === 0 || perfMarkFired.current) return;
    perfMarkFired.current = true;
    const start = performance.now();
    const raf = requestAnimationFrame(() => {
      performance.measure("trajectory-render-initial", { start, end: performance.now() });
    });
    return () => cancelAnimationFrame(raf);
  }, [mergedData.length]);

  const isSingleEntity = mergedData.some(
    (d) => d.financial_scoring_basis === "normalized_absolute",
  );

  // ---------------------------------------------------------------------------
  // Phase 4 — composite encoding data (ADR-017 §Decision table)
  // ---------------------------------------------------------------------------
  const primaryEntityId = entityIds?.[0] ?? null;

  const effectiveActiveTrajectories = useMemo<Record<string, TrajectoryResponse>>(() => {
    if (entityTrajectories && Object.keys(entityTrajectories).length > 0) return entityTrajectories;
    if (trajectory && primaryEntityId) return { [primaryEntityId]: trajectory };
    return {};
  }, [entityTrajectories, trajectory, primaryEntityId]);

  const effectiveBaselineTrajectories = useMemo<Record<string, TrajectoryResponse>>(() => {
    if (entityBaselineTrajectories && Object.keys(entityBaselineTrajectories).length > 0) return entityBaselineTrajectories;
    if (baseline_trajectory && primaryEntityId) return { [primaryEntityId]: baseline_trajectory };
    return {};
  }, [entityBaselineTrajectories, baseline_trajectory, primaryEntityId]);

  const entityCount = entityIds?.length ?? 1;
  const isLegibilityLimit = entityCount > 4;
  // Composite path: N>1 entities, or N=1 in Mode 3 (ghost+active from store).
  const useComposite = !isLegibilityLimit && !(entityCount <= 1 && mode !== "MODE_3");
  const hasCompositeData = Object.keys(effectiveActiveTrajectories).length > 0;

  // Shared entity-labels-overlay — rendered in every path (DEMO-063).
  // Dynamic: N labels for N entities, indexed by position in entityIds.
  const entityLabelsOverlay =
    entityIds && entityIds.length >= 2 ? (
      <div
        data-testid="entity-labels-overlay"
        style={{
          position: "absolute",
          top: 4,
          right: 28,
          display: "flex",
          flexDirection: "column",
          gap: 3,
          pointerEvents: "none",
        }}
      >
        {entityIds.map((entityId, i) => (
          <span
            key={entityId}
            data-testid={`entity-label-${i}`}
            style={{
              fontSize: 9,
              fontWeight: 700,
              color: ENTITY_PALETTE[i % ENTITY_PALETTE.length],
              background: "rgba(255,255,255,0.85)",
              padding: "1px 3px",
            }}
          >
            {entityId}
          </span>
        ))}
      </div>
    ) : null;

  // ---------------------------------------------------------------------------
  // Legibility-limit notice (N > 4)
  // ---------------------------------------------------------------------------
  if (isLegibilityLimit) {
    return (
      <div
        data-testid={dataTestId}
        data-current-step={current_step}
        style={{ width: width ?? 480, position: "relative" }}
      >
        <div
          data-testid="zone-1a-legibility-limit"
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#555",
            fontSize: 12,
            fontFamily: "monospace",
            height,
            padding: "16px 24px",
            lineHeight: 1.5,
            textAlign: "center",
            borderLeft: "3px solid #ddd",
          }}
        >
          Zone 1A shows individual entity trajectories for up to 4 entities. This scenario
          has {entityCount} entities. Reduce the entity selection to 4 or fewer to see
          trajectory curves.
        </div>
        {entityLabelsOverlay}
      </div>
    );
  }

  // ---------------------------------------------------------------------------
  // No data placeholder
  // ---------------------------------------------------------------------------
  if (!trajectory && !hasCompositeData) {
    return (
      <div
        data-testid={dataTestId}
        data-current-step={current_step}
        style={{ width: width ?? 480, position: "relative" }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#999",
            fontSize: 13,
            fontFamily: "monospace",
            height: "100%",
            minHeight: 80,
          }}
        >
          No trajectory data
        </div>
        {entityLabelsOverlay}
      </div>
    );
  }

  // ---------------------------------------------------------------------------
  // Phase 4 composite SVG (N>1 entities, or N=1 in Mode 3)
  // ---------------------------------------------------------------------------
  if (useComposite && hasCompositeData) {
    const entityCodes = entityIds ?? Object.keys(effectiveActiveTrajectories);
    return (
      <div
        data-testid={dataTestId}
        data-current-step={current_step}
        style={{ width: width ?? 480, position: "relative" }}
      >
        <CompositeChartSVG
          entityCodes={entityCodes}
          activeTrajectories={effectiveActiveTrajectories}
          baselineTrajectories={effectiveBaselineTrajectories}
          mode={mode}
          width={width ?? 480}
          height={height}
        />
        {entityLabelsOverlay}
      </div>
    );
  }

  // ---------------------------------------------------------------------------
  // Existing recharts rendering (N=1, Mode 1/2 — unchanged path)
  // ---------------------------------------------------------------------------
  return (
    <div
      data-testid={dataTestId}
      data-current-step={current_step}
      style={{ width: width ?? 480, position: "relative" }}
    >
      <ResponsiveContainer width="100%" height={height}>
        <ComposedChart
          data={mergedData}
          margin={{ top: 16, right: 24, bottom: 48, left: 8 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />

          <XAxis
            dataKey="step_index"
            tick={
              <CustomStepTick
                data={mergedData}
                entityIds={entityIds}
              />
            }
            height={60}
          />

          <YAxis
            domain={[0, "auto"]}
            tick={{ fontSize: 11 }}
            width={44}
            tickFormatter={(v: number) => v.toFixed(2)}
            label={{ value: "Score", angle: -90, position: "insideLeft", fontSize: 10 }}
          />

          <Tooltip
            formatter={(value, name) => {
              const framework = String(name).replace(/ \(.*\)$/, "").toLowerCase().replace(" ", "_") as FrameworkKey;
              const isSingleCountry = isSingleEntity && (framework === "financial" || framework === "human_development");
              if (isSingleCountry) {
                return [value, `${name} — Single-country index — not comparable across scenarios`];
              }
              return [value, name];
            }}
          />

          <Legend
            formatter={(value) => value}
          />

          {/* Uncertainty band Areas (ADR-007-gated) */}
          {FRAMEWORKS.map((fw) => (
            <Area
              key={`${fw}-band`}
              dataKey={`${fw}_ci_upper` as never}
              baseLine={`${fw}_ci_lower` as never}
              fill={FRAMEWORK_COLORS[fw]}
              fillOpacity={0}
              stroke="none"
              isAnimationActive={false}
              connectNulls={CONNECT_NULLS}
              legendType="none"
            />
          ))}

          {/* Divergence fill Areas (Mode 3 only) */}
          {FRAMEWORKS.map((fw) => (
            <Area
              key={`${fw}-divergence`}
              dataKey={`${fw}_active` as never}
              baseLine={`${fw}_baseline` as never}
              fill={FRAMEWORK_COLORS[fw]}
              fillOpacity={showBaseline ? 0.12 : 0}
              stroke="none"
              isAnimationActive={false}
              connectNulls={CONNECT_NULLS}
              legendType="none"
            />
          ))}

          {/* Ecological WARNING floor */}
          {trajectory && trajectory.mda_floors
            .filter((f) => f.framework === "ecological" && f.severity === "WARNING")
            .map((floor) => (
              <ReferenceLine
                key={`mda-${floor.framework}-${floor.severity}`}
                y={floor.floor_value}
                stroke={FRAMEWORK_COLORS.ecological}
                strokeDasharray="6 3"
                strokeOpacity={0.6}
                label={{ value: floor.label, fontSize: 10, fill: FRAMEWORK_COLORS.ecological }}
              />
            ))}

          {/* Rider #97 — threshold-crossing markers in Mode 3 */}
          {showBaseline && trajectory &&
            trajectory.mda_floors
              .filter((f) => f.framework === "ecological")
              .flatMap((floor) =>
                mergedData
                  .filter((d) => {
                    const active = d.ecological_active;
                    const baseline = d.ecological_baseline;
                    if (active === null || baseline === null) return false;
                    return (active >= floor.floor_value) !== (baseline >= floor.floor_value);
                  })
                  .map((d) => (
                    <ReferenceLine
                      key={`threshold-cross-${floor.framework}-step${d.step_index}`}
                      x={d.step_index}
                      stroke={FRAMEWORK_COLORS.ecological}
                      strokeDasharray="4 2"
                      strokeOpacity={0.8}
                      strokeWidth={1.5}
                      label={{
                        value: "⚠ threshold",
                        fontSize: 9,
                        fill: FRAMEWORK_COLORS.ecological,
                        position: "top",
                      }}
                    />
                  )),
              )}

          {/* Baseline ghost Lines (Mode 2 and Mode 3) */}
          {showBaseline &&
            FRAMEWORKS.map((fw) => {
              const isDashed = isSingleEntity && (fw === "financial" || fw === "human_development");
              return (
                <Line
                  key={`${fw}-baseline`}
                  dataKey={`${fw}_baseline` as never}
                  stroke={FRAMEWORK_COLORS[fw]}
                  strokeOpacity={0.5}
                  strokeWidth={1}
                  strokeDasharray={isDashed ? "8 3" : "4 2"}
                  dot={false}
                  connectNulls={CONNECT_NULLS}
                  name={`${legendFormatter(fw, "percentile_rank")} (baseline)` as never}
                  isAnimationActive={false}
                  legendType={mode === "MODE_2" ? "line" : "none"}
                />
              );
            })}

          {/* Active Lines */}
          {FRAMEWORKS.map((fw) => {
            const scoringBasis =
              mergedData[0]?.[`${fw}_scoring_basis` as keyof MergedStepDatum] as string ?? "percentile_rank";
            const isDashed =
              isSingleEntity && (fw === "financial" || fw === "human_development");
            return (
              <Line
                key={`${fw}-active`}
                dataKey={`${fw}_active` as never}
                stroke={FRAMEWORK_COLORS[fw]}
                strokeWidth={2}
                strokeDasharray={isDashed ? "8 3" : undefined}
                dot={false}
                connectNulls={CONNECT_NULLS}
                name={legendFormatter(fw, scoringBasis, entityIds) as never}
                isAnimationActive={false}
              />
            );
          })}
        </ComposedChart>
      </ResponsiveContainer>

      {/* ADR-015 §Component 1 — L0 confidence tier badges */}
      {mergedData.length > 0 && (
        <div
          style={{
            position: "absolute",
            top: 16,
            right: 4,
            display: "flex",
            flexDirection: "column",
            gap: 3,
            pointerEvents: "none",
            zIndex: 10,
          }}
        >
          {FRAMEWORKS.map((fw) => {
            const lastStep = mergedData[mergedData.length - 1];
            const score = lastStep[`${fw}_active` as keyof MergedStepDatum] as number | null;
            const tier = lastStep[`${fw}_confidence_tier` as keyof MergedStepDatum] as number;
            if (score === null) return null;
            const color = FRAMEWORK_COLORS[fw];
            return (
              <span
                key={fw}
                data-testid="zone-1a-l0-badge"
                style={{
                  fontSize: 9,
                  fontWeight: 700,
                  color,
                  background: "rgba(255,255,255,0.92)",
                  padding: "1px 4px",
                  borderRadius: 2,
                  border: `1px solid ${color}`,
                  lineHeight: 1.4,
                  whiteSpace: "nowrap",
                }}
              >
                T{tier}
              </span>
            );
          })}
        </div>
      )}

      {/* Entity labels overlay — N-entity dynamic (DEMO-063) */}
      {entityLabelsOverlay}

      {/* Multi-entity composite note */}
      {!isSingleEntity && entityIds && entityIds.length === 2 && (
        <div
          style={{
            fontSize: 11,
            color: "#888",
            marginTop: 4,
            padding: "4px 8px",
            borderLeft: "2px solid #ddd",
          }}
        >
          Each curve is a framework composite across {entityIds[0]} and {entityIds[1]}. Both entities contribute to each trajectory.
        </div>
      )}

      {/* Single-entity methodology note (Zone 3, Path A — EL Decision B) */}
      {isSingleEntity && (
        <div
          style={{
            fontSize: 11,
            color: "#888",
            marginTop: 4,
            padding: "4px 8px",
            borderLeft: "2px solid #ddd",
          }}
        >
          Scores reflect absolute indicator position, not ranking. Cross-scenario
          comparison is not valid.
        </div>
      )}

      {/* M16-G4 #102 — Variance band toggle (comparison mode only) */}
      {comparisonMode && (
        <div style={{ display: "flex", alignItems: "center", gap: 6, marginTop: 4, padding: "2px 6px" }}>
          <button
            data-testid="variance-band-toggle"
            onClick={() => setShowVarianceBand((v) => !v)}
            style={{
              fontSize: 10,
              padding: "2px 6px",
              border: "1px solid #aaa",
              borderRadius: 3,
              background: showVarianceBand ? "#e0eeff" : "#f5f5f5",
              cursor: "pointer",
              fontWeight: showVarianceBand ? 700 : 400,
            }}
          >
            {showVarianceBand ? "Hide range" : "Show range"}
          </button>
          {showVarianceBand && (
            <span
              data-testid="variance-band-label"
              style={{ fontSize: 10, color: "#555" }}
            >
              Distributional range
            </span>
          )}
        </div>
      )}

      {/* M16-G4 #102 — Variance band overlay per entity */}
      {comparisonMode && showVarianceBand && (entityIds ?? ["primary"]).map((entityKey) => (
        <div
          key={entityKey}
          data-testid={`zone-1a-variance-band-${entityKey}`}
          style={{
            width: "100%",
            height: 8,
            background: "rgba(0, 90, 158, 0.12)",
            borderTop: "1px solid rgba(0, 90, 158, 0.25)",
            borderBottom: "1px solid rgba(0, 90, 158, 0.25)",
            marginTop: 2,
          }}
        />
      ))}
    </div>
  );
}
