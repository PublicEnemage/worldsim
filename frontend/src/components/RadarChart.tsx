import { useState } from "react";
import {
  Radar,
  RadarChart as RechartsRadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import type { RadarAxisDatum, FrameworkWeights } from "../types";

interface Props {
  data: RadarAxisDatum[];
  weights: FrameworkWeights;
  onWeightsChange: (weights: FrameworkWeights) => void;
  onAxisClick: (framework: string) => void;
}

const FRAMEWORK_LABELS: Record<string, string> = {
  financial: "Financial",
  human_development: "Human Dev.",
  ecological: "Ecological",
  governance: "Governance",
};

// Custom tick renders axis label with breach badge and grayed unimplemented state
function CustomTick(props: {
  x?: number | string;
  y?: number | string;
  payload?: { value: string };
  data: RadarAxisDatum[];
  onAxisClick: (framework: string) => void;
  [key: string]: unknown;
}) {
  const { x = 0, y = 0, payload, data, onAxisClick } = props;
  const cx = typeof x === "string" ? parseFloat(x) : x;
  const cy = typeof y === "string" ? parseFloat(y) : y;
  if (!payload) return null;

  const framework = payload.value;
  const datum = data.find((d) => d.framework === framework);
  if (!datum) return null;

  const label = FRAMEWORK_LABELS[framework] ?? framework;
  const implemented = datum.is_implemented;
  const breached = datum.has_critical_breach;

  const textColor = !implemented ? "#bbb" : breached ? "#c00" : "#333";

  return (
    <g
      onClick={() => onAxisClick(framework)}
      style={{ cursor: "pointer" }}
    >
      <text
        x={cx}
        y={cy}
        textAnchor="middle"
        dominantBaseline="central"
        fontSize={12}
        fontWeight={breached ? 700 : 400}
        fill={textColor}
      >
        {label}
        {!implemented && " ⊘"}
      </text>
      {breached && (
        <text
          x={cx}
          y={cy + 14}
          textAnchor="middle"
          fontSize={10}
          fill="#c00"
        >
          {datum.breach_count} breach{datum.breach_count !== 1 ? "es" : ""}
        </text>
      )}
    </g>
  );
}

// Recharts custom dot: red for breached axes, gray for unimplemented
function CustomDot(props: {
  cx?: number;
  cy?: number;
  payload?: RadarAxisDatum;
}) {
  const { cx = 0, cy = 0, payload } = props;
  if (!payload) return null;

  if (!payload.is_implemented) {
    return <circle cx={cx} cy={cy} r={3} fill="#ccc" stroke="#aaa" strokeWidth={1} />;
  }
  if (payload.has_critical_breach) {
    return <circle cx={cx} cy={cy} r={5} fill="#c00" stroke="#900" strokeWidth={1} />;
  }
  return <circle cx={cx} cy={cy} r={4} fill="#1a6eb5" stroke="#0d4f8a" strokeWidth={1} />;
}

export default function RadarChart({ data, weights, onWeightsChange, onAxisClick }: Props) {
  const [showSliders, setShowSliders] = useState(false);

  // Apply weights to composite scores for visual emphasis only
  const chartData = data.map((d) => ({
    ...d,
    display_score: Math.min(
      1,
      d.composite_score * (weights[d.framework as keyof FrameworkWeights] ?? 1),
    ),
    // Keep unimplemented at 0
    final_score: d.is_implemented
      ? Math.min(
          1,
          d.composite_score * (weights[d.framework as keyof FrameworkWeights] ?? 1),
        )
      : 0,
  }));

  const hasAnyBreach = data.some((d) => d.has_critical_breach);

  return (
    <div>
      {hasAnyBreach && (
        <div
          style={{
            background: "#fff0f0",
            border: "1px solid #f5c6cb",
            borderRadius: 4,
            padding: "4px 8px",
            marginBottom: 8,
            fontSize: 12,
            color: "#900",
          }}
        >
          MDA threshold breach active — see alerts below.
        </div>
      )}

      <ResponsiveContainer width="100%" height={260}>
        <RechartsRadarChart data={chartData} margin={{ top: 20, right: 30, bottom: 20, left: 30 }}>
          <PolarGrid stroke="#ddd" />
          <PolarAngleAxis
            dataKey="framework"
            tick={(props) => (
              <CustomTick
                {...props}
                data={data}
                onAxisClick={onAxisClick}
              />
            )}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 1]}
            tickCount={3}
            tick={{ fontSize: 9, fill: "#aaa" }}
          />
          <Radar
            name="Framework scores"
            dataKey="final_score"
            stroke="#1a6eb5"
            fill="#1a6eb5"
            fillOpacity={0.25}
            dot={(props) => {
              // find matching datum
              const datum = data.find((d) => d.framework === props.payload?.framework);
              return (
                <CustomDot
                  key={props.index}
                  cx={props.cx}
                  cy={props.cy}
                  payload={datum}
                />
              );
            }}
          />
          <Tooltip
            formatter={(value: unknown) => [
              typeof value === "number" ? `${(value * 100).toFixed(0)}th pct` : String(value),
            ]}
            contentStyle={{ fontSize: 12 }}
          />
        </RechartsRadarChart>
      </ResponsiveContainer>

      {/* Weighting sliders — visual emphasis only, never suppress MDA alerts */}
      <div style={{ marginTop: 4 }}>
        <button
          onClick={() => setShowSliders((v) => !v)}
          style={{
            background: "none",
            border: "none",
            cursor: "pointer",
            fontSize: 11,
            color: "#888",
            padding: 0,
          }}
        >
          {showSliders ? "▲" : "▼"} Framework emphasis weights (visual only)
        </button>

        {showSliders && (
          <div style={{ marginTop: 6, display: "flex", flexDirection: "column", gap: 4 }}>
            <p style={{ fontSize: 11, color: "#999", margin: "0 0 4px", fontStyle: "italic" }}>
              Weights scale visual fill only. MDA alerts fire unconditionally.
            </p>
            {(["financial", "human_development", "ecological", "governance"] as const).map((fw) => (
              <label key={fw} style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 12 }}>
                <span style={{ width: 120, color: "#555" }}>
                  {FRAMEWORK_LABELS[fw] ?? fw}
                </span>
                <input
                  type="range"
                  min={0}
                  max={2}
                  step={0.1}
                  value={weights[fw]}
                  onChange={(e) =>
                    onWeightsChange({ ...weights, [fw]: parseFloat(e.target.value) })
                  }
                  style={{ flex: 1 }}
                />
                <span style={{ width: 28, textAlign: "right", color: "#666" }}>
                  {weights[fw].toFixed(1)}×
                </span>
              </label>
            ))}
            <button
              onClick={() =>
                onWeightsChange({
                  financial: 1,
                  human_development: 1,
                  ecological: 1,
                  governance: 1,
                })
              }
              style={{ fontSize: 11, marginTop: 2, cursor: "pointer", alignSelf: "flex-start" }}
            >
              Reset to 1.0×
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
