import { useState, useEffect, useRef } from "react";
import { useMultiFrameworkOutput } from "../hooks/useMultiFrameworkOutput";
import RadarChart from "./RadarChart";
import FrameworkPanel from "./FrameworkPanel";
import MDAAlertPanel from "./MDAAlertPanel";
import type { MDAAlert, RadarAxisDatum, FrameworkWeights } from "../types";

const WEIGHTS_KEY = "worldsim.frameworkWeights";

const DEFAULT_WEIGHTS: FrameworkWeights = {
  financial: 1,
  human_development: 1,
  ecological: 1,
  governance: 1,
};

const FRAMEWORK_ORDER = ["financial", "human_development", "ecological", "governance"] as const;
const FRAMEWORK_LABELS: Record<string, string> = {
  financial: "Financial",
  human_development: "Human Development",
  ecological: "Ecological",
  governance: "Governance",
};

function loadWeights(): FrameworkWeights {
  try {
    const raw = localStorage.getItem(WEIGHTS_KEY);
    if (raw) return { ...DEFAULT_WEIGHTS, ...(JSON.parse(raw) as Partial<FrameworkWeights>) };
  } catch {
    // ignore parse errors
  }
  return DEFAULT_WEIGHTS;
}

interface Props {
  scenarioId: string;
  entityId: string;
  step: number | null;
  onClose: () => void;
}

export default function EntityDetailDrawer({ scenarioId, entityId, step, onClose }: Props) {
  const [weights, setWeights] = useState<FrameworkWeights>(loadWeights);
  const [selectedFramework, setSelectedFramework] = useState<string>("financial");

  // Track the last non-null step so the drawer keeps showing data after scenario completes.
  // currentStep becomes null only at scenario creation time; once steps have been advanced
  // it stays at the last advanced value — but guard against hypothetical future resets.
  const lastStepRef = useRef<number | null>(null);
  if (step !== null) {
    lastStepRef.current = step;
  }
  const effectiveStep = step ?? lastStepRef.current;

  const { data, loading, error } = useMultiFrameworkOutput(scenarioId, entityId, effectiveStep);

  // Persist weights to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem(WEIGHTS_KEY, JSON.stringify(weights));
    } catch {
      // ignore storage errors (private browsing etc.)
    }
  }, [weights]);

  // Collect all MDA alerts across all frameworks
  const allAlerts: MDAAlert[] = data
    ? FRAMEWORK_ORDER.flatMap((fw) => data.outputs[fw]?.mda_alerts ?? [])
    : [];

  // Build RadarChart axis data
  const radarData: RadarAxisDatum[] = FRAMEWORK_ORDER.map((fw) => {
    const output = data?.outputs[fw];
    const alerts = output?.mda_alerts ?? [];
    const criticalAlerts = alerts.filter(
      (a) => a.severity === "CRITICAL" || a.severity === "TERMINAL",
    );
    return {
      framework: fw,
      label: FRAMEWORK_LABELS[fw],
      composite_score: output?.composite_score != null ? parseFloat(output.composite_score) : 0,
      is_implemented: output?.composite_score != null,
      has_critical_breach: criticalAlerts.length > 0,
      breach_count: criticalAlerts.length,
    };
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        right: 0,
        width: 380,
        height: "100%",
        background: "#fff",
        borderLeft: "1px solid #ccc",
        boxShadow: "-4px 0 16px rgba(0,0,0,0.12)",
        display: "flex",
        flexDirection: "column",
        zIndex: 10,
        overflowY: "auto",
      }}
    >
      {/* Header */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "12px 14px",
          borderBottom: "1px solid #eee",
          background: "#f8f8f8",
          flexShrink: 0,
        }}
      >
        <div>
          <div style={{ fontWeight: 700, fontSize: 15 }}>
            {data ? data.entity_name : entityId}
          </div>
          {data && (
            <div style={{ fontSize: 11, color: "#888", marginTop: 1 }}>
              {data.timestep.slice(0, 10)} · step {data.step_index}
            </div>
          )}
        </div>
        <button
          onClick={onClose}
          style={{
            background: "none",
            border: "1px solid #ccc",
            borderRadius: 4,
            cursor: "pointer",
            fontSize: 16,
            padding: "2px 8px",
            color: "#555",
          }}
          aria-label="Close drawer"
        >
          ✕
        </button>
      </div>

      {/* Body */}
      <div style={{ padding: "12px 14px", flex: 1 }}>
        {loading && (
          <div style={{ color: "#888", fontSize: 13, padding: "20px 0" }}>
            Loading measurement output…
          </div>
        )}

        {error && (
          <div
            style={{
              background: "#fff5f5",
              border: "1px solid #fcc",
              borderRadius: 4,
              padding: "8px 10px",
              fontSize: 13,
              color: "#900",
              marginBottom: 12,
            }}
          >
            {effectiveStep === null
              ? "Advance the scenario at least one step to load measurement output."
              : `Error: ${error}`}
          </div>
        )}

        {effectiveStep === null && !loading && !error && (
          <div style={{ color: "#888", fontSize: 13, padding: "8px 0" }}>
            Advance the scenario at least one step to view measurement output.
          </div>
        )}

        {data && (
          <>
            {/* Radar chart */}
            <section style={{ marginBottom: 16 }}>
              <h3 style={{ fontSize: 13, fontWeight: 600, margin: "0 0 8px", color: "#333" }}>
                Multi-Framework Overview
              </h3>
              <RadarChart
                data={radarData}
                weights={weights}
                onWeightsChange={setWeights}
                onAxisClick={setSelectedFramework}
              />
            </section>

            {/* MDA alerts */}
            {allAlerts.length > 0 && (
              <section style={{ marginBottom: 16 }}>
                <h3 style={{ fontSize: 13, fontWeight: 600, margin: "0 0 8px", color: "#c00" }}>
                  MDA Threshold Breaches
                </h3>
                <MDAAlertPanel alerts={allAlerts} />
              </section>
            )}

            {/* Framework indicator panels */}
            <section style={{ marginBottom: 16 }}>
              <h3 style={{ fontSize: 13, fontWeight: 600, margin: "0 0 8px", color: "#333" }}>
                Framework Indicators
              </h3>
              <div style={{ display: "flex", gap: 4, marginBottom: 8, flexWrap: "wrap" }}>
                {FRAMEWORK_ORDER.map((fw) => (
                  <button
                    key={fw}
                    onClick={() => setSelectedFramework(fw)}
                    style={{
                      fontSize: 11,
                      padding: "2px 8px",
                      borderRadius: 3,
                      border: `1px solid ${fw === selectedFramework ? "#1a6eb5" : "#ccc"}`,
                      background: fw === selectedFramework ? "#e8f0fb" : "#fafafa",
                      color: fw === selectedFramework ? "#1a6eb5" : "#555",
                      cursor: "pointer",
                      fontWeight: fw === selectedFramework ? 700 : 400,
                    }}
                  >
                    {FRAMEWORK_LABELS[fw]}
                  </button>
                ))}
              </div>
              {FRAMEWORK_ORDER.filter((fw) => fw === selectedFramework).map((fw) => (
                <FrameworkPanel
                  key={fw}
                  framework={fw}
                  output={data.outputs[fw] ?? {
                    framework: fw,
                    composite_score: null,
                    indicators: {},
                    mda_alerts: [],
                    has_below_floor_indicator: false,
                    note: "Framework data unavailable.",
                  }}
                />
              ))}
            </section>

            {/* IA-1 disclosure */}
            <section>
              <p
                style={{
                  fontSize: 10,
                  color: "#aaa",
                  fontStyle: "italic",
                  borderTop: "1px solid #eee",
                  paddingTop: 8,
                  margin: 0,
                }}
              >
                {data.ia1_disclosure}
              </p>
            </section>
          </>
        )}
      </div>
    </div>
  );
}
