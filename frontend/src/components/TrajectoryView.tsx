/* eslint-disable react-refresh/only-export-components */
/**
 * TrajectoryView — Zone 1A primary instrument.
 *
 * Implements: ADR-010 Decisions 1–10, FA brief §TrajectoryView.
 * Design decisions: DD-012 (Zustand atom), DD-013 (divergence fill), DD-014 (step annotation).
 * Framework colors: frameworkColors.ts (UX Designer ruling, MV-001 closed 2026-05-23).
 */
import { useMemo, useLayoutEffect, useRef } from "react";
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

function legendFormatter(framework: FrameworkKey, scoringBasis: string): string {
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
  return base;
}

// ---------------------------------------------------------------------------
// TrajectoryView props
// ---------------------------------------------------------------------------

interface TrajectoryViewProps {
  /** Width of the trajectory view zone in px (480 at 1024×768, 580 at 1280×800). */
  width?: number;
  /** Entity ISO 3166-1 alpha-3 codes — provide two for multi-case Mode 1. */
  entityIds?: string[];
  /** test-id for AC-006 DOM assertions. */
  "data-testid"?: string;
}

// ---------------------------------------------------------------------------
// TrajectoryView
// ---------------------------------------------------------------------------

export function TrajectoryView({
  width,
  entityIds,
  "data-testid": dataTestId = "zone-1a-trajectory",
}: TrajectoryViewProps) {
  const { trajectory, baseline_trajectory, current_step, mode } =
    useScenarioStepStore();

  const mergedData = useMemo<MergedStepDatum[]>(() => {
    if (!trajectory) return [];
    return mergeTrajectories(trajectory, baseline_trajectory);
  }, [trajectory, baseline_trajectory]);

  const showBaseline = (mode === "MODE_2" || mode === "MODE_3") && baseline_trajectory !== null;

  // Performance mark for AC-007 / MV-002. Fires once when trajectory data first
  // arrives: measures from post-DOM-update to post-paint via requestAnimationFrame.
  // Name starts with "trajectory-render" to match the AC-007 assertion.
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

  // Determine if single-entity scenario (Path A: normalized_absolute scoring)
  const isSingleEntity = mergedData.some(
    (d) => d.financial_scoring_basis === "normalized_absolute",
  );

  if (!trajectory) {
    return (
      <div
        data-testid={dataTestId}
        data-current-step={current_step}
        style={{
          width: width ?? 480,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#999",
          fontSize: 13,
          fontFamily: "monospace",
        }}
      >
        No trajectory data
      </div>
    );
  }

  return (
    <div
      data-testid={dataTestId}
      data-current-step={current_step}
      style={{ width: width ?? 480, position: "relative" }}
    >
      <ResponsiveContainer width="100%" height={300}>
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

          {/* Uncertainty band Areas (ADR-007-gated: renders nothing until ci_lower is non-null) */}
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

          {/* Divergence fill Areas (Mode 3 only — always mounted, fillOpacity controls visibility) */}
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

          {/* Ecological WARNING floor at y=1.0 (EL Decision A — only defensible M9 floor) */}
          {trajectory.mda_floors
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

          {/* Rider #97 — threshold-crossing markers in Mode 3 comparison.
              Vertical lines at steps where the active trajectory crosses an MDA floor
              that the baseline did not cross (or vice versa). Only ecological floor
              is defined in composite score space (1.0 boundary). */}
          {showBaseline &&
            trajectory.mda_floors
              .filter((f) => f.framework === "ecological")
              .flatMap((floor) =>
                mergedData
                  .filter((d) => {
                    const active = d.ecological_active;
                    const baseline = d.ecological_baseline;
                    if (active === null || baseline === null) return false;
                    const activeBreached = active >= floor.floor_value;
                    const baselineBreached = baseline >= floor.floor_value;
                    return activeBreached !== baselineBreached;
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
                name={legendFormatter(fw, scoringBasis) as never}
                isAnimationActive={false}
              />
            );
          })}
        </ComposedChart>
      </ResponsiveContainer>

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
    </div>
  );
}
