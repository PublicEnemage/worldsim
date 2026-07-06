/* eslint-disable react-refresh/only-export-components */
/**
 * TrajectoryView — Zone 1A primary instrument.
 *
 * Implements: ADR-010 Decisions 1–10, FA brief §TrajectoryView.
 * Design decisions: DD-012 (Zustand atom), DD-013 (divergence fill), DD-014 (step annotation).
 * Framework colors: frameworkColors.ts (UX Designer ruling, MV-001 closed 2026-05-23).
 *
 * Pure view-model functions (computeYDomain, computeDivergenceFill, getConfidenceBadgeVisible,
 * mergeTrajectories, sliceToStepRange, MergedStepDatum) live in trajectoryViewModel.ts (#1522).
 * Re-exported below for backward compatibility with existing import sites.
 */
import React, { useMemo, useLayoutEffect, useRef, useState, useEffect } from "react";
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
import {
  computeYDomain,
  computeDivergenceFill,
  getConfidenceBadgeVisible,
  mergeTrajectories,
  type MergedStepDatum,
} from "./trajectoryViewModel";

export {
  computeYDomain,
  computeDivergenceFill,
  getConfidenceBadgeVisible,
  mergeTrajectories,
  type MergedStepDatum,
};

// ---------------------------------------------------------------------------
// Exported constants (tested by TrajectoryView.test.ts)
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

/** CI ribbon fill opacity for single/multi-entity view (M18-G1 #1254). */
export const CI_BAND_OPACITY = 0.12;
/** Reduced opacity when showBaseline=true — divergence fill + CI ribbon coexist (M18-G1 #1254). */
export const CI_BAND_OPACITY_MODE3 = 0.05;

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

/** Palette for N-scenario comparison mode (M17-G2 multi-scenario comparison). */
export const SCENARIO_COMPARISON_PALETTE = [
  { color: '#2563EB', strokeDasharray: 'none', label: 'A' },
  { color: '#D97706', strokeDasharray: '8 2',  label: 'B' },
  { color: '#16A34A', strokeDasharray: '2 4',  label: 'C' },
  { color: '#7C3AED', strokeDasharray: '12 4', label: 'D' },
  { color: '#E11D48', strokeDasharray: '2 2 8 2', label: 'E' },
] as const;

export interface ScenarioComparisonThresholdCrossing {
  indicator_id: string;
  indicator_name?: string;
  severity: "CRITICAL" | "WARNING";
  first_crossing_step: number;
}

export interface ScenarioComparisonConfig {
  scenarioId: string;
  label: string;
  paletteIndex: number;
  trajectory?: TrajectoryResponse | null;
  thresholdCrossings?: ScenarioComparisonThresholdCrossing[];
  pspValue?: string | null;
}

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
  const tiers = Object.values(step.frameworks)
    .map((fw) => fw.confidence_tier)
    .filter((t): t is number => typeof t === "number" && !isNaN(t));
  if (tiers.length === 0) return 3;
  return Math.max(...tiers);
}

/** Lowest non-trivial MDA floor value (0 < value < 1) across all frameworks. */
function getEntityMdaFloor(mda_floors: MDAFloor[]): number | null {
  const floors = mda_floors.map((f) => f.floor_value).filter((v) => v > 0 && v < 1.0);
  if (floors.length === 0) return null;
  return Math.min(...floors);
}

/**
 * Half-width schedule mirrors BandingEngine §3.1 (M18-G1 #1254).
 * Exported for unit tests (AC-1254-HW).
 */
export function computeCompositeHalfWidth(stepIndex: number, tier: number): number {
  const baseHW = stepIndex === 1 ? 0.10 : stepIndex === 2 ? 0.20 : stepIndex <= 5 ? 0.35 : 0.50;
  const multiplier = [1.0, 1.0, 1.2, 1.5, 2.0, 3.0][Math.min(tier, 5)];
  return baseHW * multiplier;
}

export function computeCompositeCIBounds(step: TrajectoryStep): { lower: number | null; upper: number | null } {
  const score = computeEntityCompositeScore(step);
  if (score === null) return { lower: null, upper: null };
  const worstTier = getEntityWorstTier(step);
  const halfWidth = computeCompositeHalfWidth(step.step_index, worstTier);
  return {
    lower: Math.max(0.0, score - halfWidth),
    upper: Math.min(1.0, score + halfWidth),
  };
}

// MergedStepDatum and mergeTrajectories live in trajectoryViewModel.ts (#1522).
// Re-exported above for backward compatibility.

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
  comparisonScenarios?: ScenarioComparisonConfig[];
  visibleStepRange?: [number, number] | null;
}

function CompositeChartSVG({
  entityCodes,
  activeTrajectories,
  baselineTrajectories,
  mode,
  width,
  height,
  comparisonScenarios = [],
  visibleStepRange = null,
}: CompositeChartSVGProps) {
  const MARGIN = { top: 16, right: 60, bottom: 48, left: 44 };
  const chartW = width - MARGIN.left - MARGIN.right;
  const chartH = height - MARGIN.top - MARGIN.bottom;

  const refCode = entityCodes.find((c) => activeTrajectories[c]);
  const refSteps = refCode ? activeTrajectories[refCode].steps : [];
  const allStepIndices = refSteps.map((s) => s.step_index);
  const stepIndices = visibleStepRange
    ? allStepIndices.filter((i) => i >= visibleStepRange[0] && i <= visibleStepRange[1])
    : allStepIndices;

  const filterSteps = (steps: TrajectoryStep[]): TrajectoryStep[] =>
    visibleStepRange
      ? steps.filter((s) => s.step_index >= visibleStepRange![0] && s.step_index <= visibleStepRange![1])
      : steps;

  const xScale = (idx: number): number => {
    if (stepIndices.length <= 1) return MARGIN.left + chartW / 2;
    const i = stepIndices.indexOf(idx);
    if (i < 0) return MARGIN.left;
    return MARGIN.left + (i / (stepIndices.length - 1)) * chartW;
  };

  // In comparison mode, MDA floors are excluded from the y-domain so tightly clustered
  // scenario curves are not collapsed by a floor that anchors the scale far below the data.
  // comparisonDataMin tracks the raw data minimum (pre-padding) for floor suppression (AC-2/#1629).
  const [yMin, yMax, comparisonDataMin] = useMemo(() => {
    const inRange = (step: TrajectoryStep) =>
      !visibleStepRange ||
      (step.step_index >= visibleStepRange[0] && step.step_index <= visibleStepRange[1]);
    const values: number[] = [];
    const inComparisonMode = comparisonScenarios.length > 0;
    for (const traj of [...Object.values(activeTrajectories), ...Object.values(baselineTrajectories)]) {
      for (const step of traj.steps) {
        if (!inRange(step)) continue;
        const s = computeEntityCompositeScore(step);
        if (s !== null) values.push(s);
      }
      if (!inComparisonMode) {
        const floor = getEntityMdaFloor(traj.mda_floors);
        if (floor !== null) values.push(floor);
      }
    }
    let compDataMin: number | null = null;
    for (const sc of comparisonScenarios) {
      if (!sc.trajectory) continue;
      for (const step of sc.trajectory.steps) {
        if (!inRange(step)) continue;
        const s = computeEntityCompositeScore(step);
        if (s !== null) {
          values.push(s);
          compDataMin = compDataMin === null ? s : Math.min(compDataMin, s);
        }
      }
      // Floor excluded from values in comparison mode (see comment above)
    }
    return [...computeYDomain(values), compDataMin] as [number, number, number | null];
  }, [activeTrajectories, baselineTrajectories, comparisonScenarios, visibleStepRange]);

  const yScale = (score: number): number => {
    const clamped = Math.min(yMax, Math.max(yMin, score));
    return MARGIN.top + (1 - (clamped - yMin) / (yMax - yMin)) * chartH;
  };

  const yGridValues = [
    yMin,
    yMin + (yMax - yMin) * 0.25,
    yMin + (yMax - yMin) * 0.5,
    yMin + (yMax - yMin) * 0.75,
    yMax,
  ];

  const buildPathD = (steps: TrajectoryStep[]): string => {
    const pts: string[] = [];
    for (const step of steps) {
      const score = computeEntityCompositeScore(step);
      if (score === null) continue;
      pts.push(`${xScale(step.step_index).toFixed(1)},${yScale(score).toFixed(1)}`);
    }
    return pts.length >= 2 ? "M " + pts.join(" L ") : "";
  };

  const buildCIRibbonPath = (steps: TrajectoryStep[]): string => {
    const upperPts: string[] = [];
    const lowerPts: string[] = [];
    for (const step of steps) {
      const { lower, upper } = computeCompositeCIBounds(step);
      if (lower === null || upper === null) continue;
      upperPts.push(`${xScale(step.step_index).toFixed(1)},${yScale(upper).toFixed(1)}`);
      lowerPts.unshift(`${xScale(step.step_index).toFixed(1)},${yScale(lower).toFixed(1)}`);
    }
    if (upperPts.length < 2) return "";
    return "M " + upperPts.join(" L ") + " L " + lowerPts.join(" L ") + " Z";
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

      {/* CI ribbons — rendered before trajectory paths so lines render on top (M18-G1 #1254) */}
      {comparisonScenarios.length === 0 && entityCodes.map((code, i) => {
        const active = activeTrajectories[code];
        if (!active) return null;
        const ribbonD = buildCIRibbonPath(filterSteps(active.steps));
        if (!ribbonD) return null;
        const color = ENTITY_PALETTE[i % ENTITY_PALETTE.length];
        return (
          <path
            key={`ci-ribbon-${code}`}
            data-testid={`zone-1a-ci-ribbon-${code}`}
            d={ribbonD}
            fill={color}
            opacity={mode === "MODE_3" ? CI_BAND_OPACITY_MODE3 : CI_BAND_OPACITY}
            stroke="none"
          />
        );
      })}
      {comparisonScenarios.length > 0 && comparisonScenarios.map((sc) => {
        if (!sc.trajectory) return null;
        const ribbonD = buildCIRibbonPath(filterSteps(sc.trajectory.steps));
        if (!ribbonD) return null;
        const palette = SCENARIO_COMPARISON_PALETTE[sc.paletteIndex];
        const slug = sc.scenarioId.replace(/^[a-z]{3}-/, "");
        return (
          <path
            key={`ci-ribbon-scenario-${sc.scenarioId}`}
            data-testid={`zone-1a-ci-ribbon-scenario-${slug}`}
            d={ribbonD}
            fill={palette.color}
            opacity={CI_BAND_OPACITY}
            stroke="none"
          />
        );
      })}

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

      {/* Divergence fill attribution — G10 #1162 */}
      {hasDivergence && (
        <text
          data-testid="divergence-fill-attribution"
          x={MARGIN.left + chartW / 2}
          y={MARGIN.top + 10}
          fontSize={9}
          fill="#555"
          textAnchor="middle"
        >
          {entityCodes
            .filter((code) => activeTrajectories[code] && baselineTrajectories[code])
            .join(" / ")}{" "}
          — active vs. baseline
        </text>
      )}

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

      {/* Scenario comparison MDA floor lines — suppressed when floor is >0.10 below data min (AC-2/#1629) */}
      {comparisonScenarios.length > 0 && comparisonScenarios.map((sc, i) => {
        if (!sc.trajectory) return null;
        const floor = getEntityMdaFloor(sc.trajectory.mda_floors);
        if (floor === null) return null;
        if (comparisonDataMin !== null && (comparisonDataMin - floor) > 0.10) return null;
        return (
          <line
            key={`scenario-mda-${sc.scenarioId}`}
            data-testid={i === 0 ? "zone1a-mda-floor-line" : undefined}
            x1={MARGIN.left}
            y1={yScale(floor)}
            x2={MARGIN.left + chartW}
            y2={yScale(floor)}
            stroke="#888"
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
          const pathD = buildPathD(filterSteps(baseline.steps));
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
      {comparisonScenarios.length === 0 && entityCodes.map((code, i) => {
        const active = activeTrajectories[code];
        if (!active) return null;
        const pathD = buildPathD(filterSteps(active.steps));
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

      {/* Scenario comparison curves — N palette-colored paths */}
      {comparisonScenarios.length > 0 && comparisonScenarios.map((sc) => {
        if (!sc.trajectory) return null;
        const pathD = buildPathD(filterSteps(sc.trajectory.steps));
        if (!pathD) return null;
        const palette = SCENARIO_COMPARISON_PALETTE[sc.paletteIndex];
        const slug = sc.scenarioId.replace(/^[a-z]{3}-/, "");
        return (
          <path
            key={`scenario-curve-${sc.scenarioId}`}
            data-testid={`zone1a-curve-scenario-${slug}`}
            d={pathD}
            stroke={palette.color}
            strokeWidth={2}
            strokeDasharray={palette.strokeDasharray === 'none' ? undefined : palette.strokeDasharray}
            fill="none"
          />
        );
      })}

      {/* Tier badges at right edge of each entity's active curve endpoint */}
      {entityCodes.map((code, i) => {
        const active = activeTrajectories[code];
        if (!active || active.steps.length === 0) return null;
        const visibleSteps = filterSteps(active.steps);
        if (visibleSteps.length === 0) return null;
        const lastStep = visibleSteps[visibleSteps.length - 1];
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

      {/* Terminal entity labels — #1249 Zone 1A curve identifiability (DEMO6-014) */}
      {comparisonScenarios.length === 0 && entityCodes.map((code, i) => {
        const active = activeTrajectories[code];
        if (!active || active.steps.length === 0) return null;
        const visibleSteps = filterSteps(active.steps);
        if (visibleSteps.length === 0) return null;
        const lastStep = visibleSteps[visibleSteps.length - 1];
        const lastScore = computeEntityCompositeScore(lastStep);
        if (lastScore === null) return null;
        const color = ENTITY_PALETTE[i % ENTITY_PALETTE.length];
        const x = xScale(lastStep.step_index);
        const y = yScale(lastScore);
        return (
          <text
            key={`terminal-label-${code}`}
            data-testid={`zone-1a-terminal-label-${code}`}
            x={x + 3}
            y={y - 7}
            fontSize={8}
            fontWeight="bold"
            fill={color}
            dominantBaseline="auto"
          >
            {code}
          </text>
        );
      })}

      {/* Scenario comparison terminal labels */}
      {comparisonScenarios.length > 0 && comparisonScenarios.map((sc) => {
        if (!sc.trajectory || sc.trajectory.steps.length === 0) return null;
        const visibleSteps = filterSteps(sc.trajectory.steps);
        if (visibleSteps.length === 0) return null;
        const lastStep = visibleSteps[visibleSteps.length - 1];
        const lastScore = computeEntityCompositeScore(lastStep);
        if (lastScore === null) return null;
        const palette = SCENARIO_COMPARISON_PALETTE[sc.paletteIndex];
        const x = xScale(lastStep.step_index);
        const y = yScale(lastScore);
        const slug = sc.scenarioId.replace(/^[a-z]{3}-/, "");
        return (
          <text
            key={`scenario-terminal-${sc.scenarioId}`}
            data-testid={`zone1a-terminal-label-scenario-${slug}`}
            x={x + 3}
            y={y - 7}
            fontSize={8}
            fontWeight="bold"
            fill={palette.color}
            dominantBaseline="auto"
          >
            {sc.label}
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
  /** M17-G2 — multi-scenario comparison configs for Zone 1A curve rendering. */
  comparisonScenarios?: ScenarioComparisonConfig[];
  /** test-id for AC-006 DOM assertions. */
  "data-testid"?: string;
}

// ---------------------------------------------------------------------------
// TrajectoryView
// ---------------------------------------------------------------------------

// React.memo: prevents re-renders when parent re-renders but trajectory data is unchanged.
// Required for ControlPlaneColumn lazy-mount optimization (#1217, EX-001 resolution).
// useMemo wraps are applied per-hook inside the component body.
export const TrajectoryView = React.memo(function TrajectoryView({
  width,
  height = 300,
  entityIds,
  entityTrajectories,
  entityBaselineTrajectories,
  comparisonScenarios,
  "data-testid": dataTestId = "zone-1a-trajectory",
}: TrajectoryViewProps) {
  const { trajectory, baseline_trajectory, current_step, mode } =
    useScenarioStepStore();

  // ---------------------------------------------------------------------------
  // Trackwheel zoom state (#1524)
  // ---------------------------------------------------------------------------
  const [visibleStepRange, setVisibleStepRange] = useState<[number, number] | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const minStep = trajectory ? Math.min(...trajectory.steps.map((s) => s.step_index)) : 1;
  const maxStep = trajectory ? Math.max(...trajectory.steps.map((s) => s.step_index)) : 1;

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const ZOOM_FACTOR = 0.20;

    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      if (!trajectory) return;
      const [lo, hi] = visibleStepRange ?? [minStep, maxStep];
      const center = Math.round((lo + hi) / 2);
      const halfRange = Math.round((hi - lo) / 2);

      if (e.deltaY > 0) {
        const newHalf = Math.max(1, Math.round(halfRange * (1 - ZOOM_FACTOR)));
        setVisibleStepRange([
          Math.max(minStep, center - newHalf),
          Math.min(maxStep, center + newHalf),
        ]);
      } else {
        const newHalf = Math.round(halfRange / (1 - ZOOM_FACTOR));
        const newLo = Math.max(minStep, center - newHalf);
        const newHi = Math.min(maxStep, center + newHalf);
        if (newLo === minStep && newHi === maxStep) {
          setVisibleStepRange(null);
        } else {
          setVisibleStepRange([newLo, newHi]);
        }
      }
    };

    const onDblClick = () => setVisibleStepRange(null);

    el.addEventListener("wheel", onWheel, { passive: false });
    el.addEventListener("dblclick", onDblClick);

    return () => {
      el.removeEventListener("wheel", onWheel);
      el.removeEventListener("dblclick", onDblClick);
    };
  }, [trajectory, visibleStepRange, minStep, maxStep]);

  const mergedData = useMemo<MergedStepDatum[]>(() => {
    if (!trajectory) return [];
    return mergeTrajectories(trajectory, baseline_trajectory, visibleStepRange);
  }, [trajectory, baseline_trajectory, visibleStepRange]);

  const showBaseline = (mode === "MODE_2" || mode === "MODE_3") && baseline_trajectory !== null;

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

  const yDomain = useMemo<[number, number]>(() => {
    const values: number[] = [];
    const fields = [
      "financial_active", "financial_baseline",
      "human_development_active", "human_development_baseline",
      "ecological_active", "ecological_baseline",
      "governance_active", "governance_baseline",
    ] as const;
    for (const d of mergedData) {
      for (const field of fields) {
        const v = d[field];
        if (typeof v === "number") values.push(v);
      }
    }
    return computeYDomain(values);
  }, [mergedData]);

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
  const useComposite = !isLegibilityLimit && (!(entityCount <= 1 && mode !== "MODE_3") || (comparisonScenarios?.length ?? 0) > 0);
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

  const zoomAttrs = visibleStepRange
    ? { "data-visible-step-min": String(visibleStepRange[0]), "data-visible-step-max": String(visibleStepRange[1]) }
    : {};

  // ---------------------------------------------------------------------------
  // Legibility-limit notice (N > 4)
  // ---------------------------------------------------------------------------
  if (isLegibilityLimit) {
    return (
      <div
        ref={containerRef}
        data-testid={dataTestId}
        data-current-step={current_step}
        {...zoomAttrs}
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
        ref={containerRef}
        data-testid={dataTestId}
        data-current-step={current_step}
        {...zoomAttrs}
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
        ref={containerRef}
        data-testid={dataTestId}
        data-current-step={current_step}
        {...zoomAttrs}
        style={{ width: width ?? 480, position: "relative" }}
      >
        {/* AC-G4-C trajectory presence indicators (ADR-019 D-10, #1217) */}
        {showBaseline && (
          <span
            data-testid="trajectory-baseline"
            aria-hidden="true"
            style={{ position: "absolute", width: 2, height: 2, opacity: 0, pointerEvents: "none" }}
          />
        )}
        {mode === "MODE_3" && (
          <span
            data-testid="trajectory-counter"
            aria-hidden="true"
            style={{ position: "absolute", width: 2, height: 2, opacity: 0, pointerEvents: "none" }}
          />
        )}
        <CompositeChartSVG
          entityCodes={entityCodes}
          activeTrajectories={effectiveActiveTrajectories}
          baselineTrajectories={effectiveBaselineTrajectories}
          mode={mode}
          width={width ?? 480}
          height={height}
          comparisonScenarios={comparisonScenarios ?? []}
          visibleStepRange={visibleStepRange}
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
      ref={containerRef}
      data-testid={dataTestId}
      data-current-step={current_step}
      {...zoomAttrs}
      style={{ width: width ?? 480, position: "relative" }}
    >
      {/* AC-G4-C trajectory presence indicators (ADR-019 D-10, #1217) */}
      {showBaseline && (
        <span
          data-testid="trajectory-baseline"
          aria-hidden="true"
          style={{ position: "absolute", width: 2, height: 2, opacity: 0, pointerEvents: "none" }}
        />
      )}
      {mode === "MODE_3" && (
        <span
          data-testid="trajectory-counter"
          aria-hidden="true"
          style={{ position: "absolute", width: 2, height: 2, opacity: 0, pointerEvents: "none" }}
        />
      )}
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
            domain={yDomain}
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

          {/* Uncertainty band Areas (ADR-007 / M18-G1 #1254) */}
          {FRAMEWORKS.map((fw) => (
            <Area
              key={`${fw}-band`}
              dataKey={`${fw}_ci_upper` as never}
              baseLine={`${fw}_ci_lower` as never}
              fill={FRAMEWORK_COLORS[fw]}
              fillOpacity={showBaseline ? CI_BAND_OPACITY_MODE3 : CI_BAND_OPACITY}
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
              fill={showBaseline ? FRAMEWORK_COLORS[fw] : "none"}
              fillOpacity={0.12}
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

      {/* M19-G3 (#1537) / G4 (#1529): CI calibration status disclosure (ADR-007 Amendment 1 §8.7).
          Absent when band_method is SUPPRESSED_MEANINGLESS (CI bounds hidden per G3 §4). */}
      {(() => {
        const lastStep = mergedData[mergedData.length - 1];
        const bandMethod = lastStep?.financial_band_method ?? null;
        if (!bandMethod || bandMethod === "SUPPRESSED_MEANINGLESS") return null;
        const STATUS_TEXT: Record<string, string> = {
          PRE_CALIBRATION_STRUCTURAL_PRIOR: "structural prior — not yet empirically calibrated",
          PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL: "provisional — directional calibration only",
          BAYESIAN_POSTERIOR_CALIBRATED: "empirically calibrated interval",
        };
        const text = STATUS_TEXT[bandMethod];
        if (!text) return null;
        return (
          <div
            data-testid="ci-calibration-status"
            style={{
              fontSize: 9,
              color: "#888",
              marginTop: 2,
              padding: "2px 8px",
              fontStyle: "italic",
            }}
          >
            {text}
          </div>
        );
      })()}

    </div>
  );
});
