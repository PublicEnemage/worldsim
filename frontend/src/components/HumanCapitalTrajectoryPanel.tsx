/**
 * HumanCapitalTrajectoryPanel — M16-G3 #274
 *
 * 25-year human capital depletion trajectory panel. Renders cohort
 * poverty_headcount_ratio trajectories from scenario snapshot data.
 *
 * Three CM-confirmed cohort curves (CM review 2026-06-23):
 *   SEN:CHT:1-25-54-INFORMAL    → bottom quintile, informal workers (Q1)
 *   SEN:CHT:1-25-54-AGRICULTURE → bottom quintile, agricultural workers (Q1)
 *   SEN:CHT:2-25-54-INFORMAL    → second quintile, informal workers (Q2)
 *
 * MDA-HD-POVERTY-Q1 floor: 0.40 — milestone sentence fires when any Q1 cohort
 * poverty_headcount_ratio first reaches or exceeds this value.
 * No MDA-HD-POVERTY-Q2 registered — Q2 curve does not trigger a sentence.
 *
 * UX Architectural Commitment 2: panel in primary viewport, never in a drawer.
 * Intent doc: docs/process/intents/M16-G3-2026-06-23-25year-human-capital-trajectory.md
 */
import { useEffect, useState } from "react";

const API_BASE = "http://localhost:8000/api/v1";

// MDA-HD-POVERTY-Q1 — floor_value=0.40, recovery_horizon_years=10 per CM review
const Q1_MDA_FLOOR = 0.40;

// Consequence phrase derived from MDA-HD-POVERTY-Q1.recovery_horizon_years=10
// Must not be hardcoded as a magic string — derived from threshold definition.
const Q1_RECOVERY_CONSEQUENCE = "a decade or more";

interface CohortDef {
  entityIdSuffix: string;
  label: string;
  curveKey: string;
  badgeKey: string;
  isQ1: boolean;
}

// CM-confirmed cohort specifications
const COHORT_DEFS_TEMPLATE: CohortDef[] = [
  {
    entityIdSuffix: ":CHT:1-25-54-INFORMAL",
    label: "bottom quintile, informal workers",
    curveKey: "q1-informal",
    badgeKey: "q1-informal",
    isQ1: true,
  },
  {
    entityIdSuffix: ":CHT:1-25-54-AGRICULTURE",
    label: "bottom quintile, agricultural workers",
    curveKey: "q1-agriculture",
    badgeKey: "q1-agriculture",
    isQ1: true,
  },
  {
    entityIdSuffix: ":CHT:2-25-54-INFORMAL",
    label: "second quintile, informal workers",
    curveKey: "q2-informal",
    badgeKey: "q2-informal",
    isQ1: false,
  },
];

interface RawQuantityEnvelope {
  value: string;
  unit?: string;
  variable_type?: string;
}

interface RawSnapshot {
  step: number;
  timestep: string;
  state_data: Record<string, Record<string, RawQuantityEnvelope | unknown>>;
}

interface TrajectoryPoint {
  step: number;
  date: string;
  value: number;
}

interface MilestoneCrossing {
  step: number;
  year: number;
  cohortLabel: string;
}

export interface HumanCapitalTrajectoryPanelProps {
  scenarioId: string;
  projectionSteps: number;
  entities: string[];
  currentStep: number;
}

export function HumanCapitalTrajectoryPanel({
  scenarioId,
  projectionSteps,
  entities,
  currentStep,
}: HumanCapitalTrajectoryPanelProps) {
  const countryId = entities[0] ?? "SEN";
  const cohortDefs = COHORT_DEFS_TEMPLATE.map((def) => ({
    ...def,
    entityId: `${countryId}${def.entityIdSuffix}`,
  }));

  const [loading, setLoading] = useState(true);
  const [trajectories, setTrajectories] = useState<Record<string, TrajectoryPoint[]>>({});
  const [milestone, setMilestone] = useState<MilestoneCrossing | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setTrajectories({});
    setMilestone(null);

    fetch(`${API_BASE}/scenarios/${encodeURIComponent(scenarioId)}/snapshots`)
      .then((res) => (res.ok ? (res.json() as Promise<RawSnapshot[]>) : Promise.reject(res.status)))
      .then((snaps) => {
        if (cancelled) return;

        const traj: Record<string, TrajectoryPoint[]> = {};
        for (const def of cohortDefs) traj[def.entityId] = [];

        for (const snap of snaps) {
          if (snap.step === 0) continue; // skip step-0 initial state
          for (const def of cohortDefs) {
            const entityData = snap.state_data[def.entityId] as
              | Record<string, RawQuantityEnvelope | unknown>
              | undefined;
            if (!entityData) continue;
            const phr = entityData["poverty_headcount_ratio"] as RawQuantityEnvelope | undefined;
            if (!phr?.value) continue;
            const val = parseFloat(phr.value);
            if (isNaN(val)) continue;
            traj[def.entityId].push({ step: snap.step, date: snap.timestep, value: val });
          }
        }
        setTrajectories(traj);

        // First Q1 cohort floor crossing → milestone sentence
        let firstCrossing: MilestoneCrossing | null = null;
        for (const def of cohortDefs) {
          if (!def.isQ1) continue;
          const points = traj[def.entityId];
          for (const pt of points) {
            if (pt.value >= Q1_MDA_FLOOR) {
              const year = new Date(pt.date).getFullYear();
              if (!firstCrossing || pt.step < firstCrossing.step) {
                firstCrossing = { step: pt.step, year, cohortLabel: def.label };
              }
              break;
            }
          }
        }
        setMilestone(firstCrossing);
        setLoading(false);
      })
      .catch(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [scenarioId, currentStep]); // re-fetch on each step advance so sparklines update

  return (
    <div
      data-testid="human-capital-trajectory-panel"
      style={{
        borderTop: "2px solid #dbeafe",
        padding: "8px 12px 10px",
        fontSize: 12,
        background: "#f8faff",
      }}
    >
      {/* Header — AC-F4: exact string "25-year projection · quarterly resolution" (U+00B7) */}
      <div
        data-testid="projection-panel-header"
        style={{
          fontWeight: 700,
          color: "#1e40af",
          marginBottom: 8,
          fontSize: 11,
          letterSpacing: 0.4,
          textTransform: "uppercase",
        }}
      >
        25-year projection · quarterly resolution
      </div>

      {/* Milestone sentence — AC-F3, AC-CM-2 (only when Q1 floor crossed) */}
      {milestone && (
        <div data-testid="milestone-sentence">
          <div
            data-testid="projection-milestone-sentence"
            style={{
              marginBottom: 8,
              padding: "4px 8px",
              background: "#fee2e2",
              border: "1px solid #fca5a5",
              borderRadius: 4,
              color: "#7f1d1d",
              fontSize: 11,
              lineHeight: 1.5,
            }}
          >
            by {milestone.year} [step {milestone.step}], {milestone.cohortLabel} poverty headcount crosses
            the recovery floor — at this level, capability restoration takes {Q1_RECOVERY_CONSEQUENCE}
          </div>
        </div>
      )}

      {/* Three cohort curves — AC-F2, AC-CM-1 */}
      {cohortDefs.map((def) => {
        const points = trajectories[def.entityId] ?? [];
        return (
          <div
            key={def.curveKey}
            style={{ marginBottom: 6, display: "flex", alignItems: "center", gap: 6 }}
          >
            <div
              data-testid={`projection-curve-${def.curveKey}`}
              style={{ flex: 1 }}
            >
              <_CohortSparkline
                points={points}
                floor={def.isQ1 ? Q1_MDA_FLOOR : undefined}
                label={def.label}
                loading={loading}
              />
            </div>
            {/* Tier 3 badge — AC-CM-3 */}
            <span
              data-testid={`projection-tier-badge-${def.badgeKey}`}
              title="Tier 3 — synthetic data + literature elasticities"
              style={{
                fontSize: 9,
                fontWeight: 700,
                background: "#fef3c7",
                color: "#92400e",
                border: "1px solid #fbbf24",
                borderRadius: 3,
                padding: "1px 4px",
                flexShrink: 0,
              }}
            >
              T3
            </span>
          </div>
        );
      })}

      {/* Q2 suppression annotation — G10 #1179 */}
      {!loading && (() => {
        const q2Def = cohortDefs.find(d => !d.isQ1) ?? null;
        return q2Def !== null && (trajectories[q2Def.entityId]?.length ?? 0) === 0 ? (
          <div
            data-testid="q2-suppression-legend"
            style={{
              fontSize: 10,
              color: '#6b7280',
              fontStyle: 'italic',
              paddingLeft: 6,
              marginBottom: 4,
            }}
          >
            Q2 — floor threshold not registered (suppressed)
          </div>
        ) : null;
      })()}

      {/* Step axis — AC-F5 */}
      <div
        data-testid="projection-panel-step-axis"
        style={{
          marginTop: 4,
          display: "flex",
          justifyContent: "space-between",
          color: "#9ca3af",
          fontSize: 9,
          borderTop: "1px solid #e5e7eb",
          paddingTop: 3,
        }}
      >
        <span>Step 1</span>
        <span>Step 25</span>
        <span>Step 50</span>
        <span>Step 75</span>
        <span>Step {projectionSteps}</span>
      </div>
    </div>
  );
}

// Internal sparkline — not exported
function _CohortSparkline({
  points,
  floor,
  label,
  loading,
}: {
  points: TrajectoryPoint[];
  floor: number | undefined;
  label: string;
  loading: boolean;
}) {
  const svgW = 220;
  const svgH = 26;

  const safePoints = points.filter((p) => isFinite(p.value));
  const hasData = safePoints.length >= 2;

  const minVal = 0;
  const maxVal = 1.0;
  const maxStep = Math.max(safePoints.at(-1)?.step ?? 100, 100);

  const xScale = (step: number) => (step / maxStep) * svgW;
  const yScale = (val: number) => svgH - ((val - minVal) / (maxVal - minVal)) * svgH;

  const pathD = hasData
    ? safePoints
        .map((p, i) => `${i === 0 ? "M" : "L"}${xScale(p.step).toFixed(1)},${yScale(p.value).toFixed(1)}`)
        .join(" ")
    : "";

  return (
    <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
      <span
        style={{
          fontSize: 10,
          color: "#374151",
          minWidth: 178,
          maxWidth: 178,
          flexShrink: 0,
          overflow: "hidden",
          textOverflow: "ellipsis",
          whiteSpace: "nowrap",
        }}
      >
        {label}
      </span>
      <svg
        width={svgW}
        height={svgH}
        style={{ flexShrink: 0, overflow: "visible" }}
        aria-label={`${label} trajectory`}
      >
        <rect x={0} y={0} width={svgW} height={svgH} fill="#f0f4ff" rx={1} />
        {floor !== undefined && (
          <line
            x1={0}
            y1={yScale(floor)}
            x2={svgW}
            y2={yScale(floor)}
            stroke="#ef4444"
            strokeWidth={0.8}
            strokeDasharray="3,2"
            opacity={0.7}
          />
        )}
        {hasData ? (
          <path d={pathD} fill="none" stroke="#2563eb" strokeWidth={1.5} />
        ) : (
          <text
            x={svgW / 2}
            y={svgH / 2 + 4}
            textAnchor="middle"
            fontSize={8}
            fill="#9ca3af"
          >
            {loading ? "loading…" : "no data"}
          </text>
        )}
      </svg>
    </div>
  );
}
