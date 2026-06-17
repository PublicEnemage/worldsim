import { useEffect, useState } from "react";
import type { InitialStateResponse, GroundingIndicator } from "../types";

const API_BASE = "http://localhost:8000/api/v1";

// Named frameworks only — "None" key must not render as a section heading.
const FRAMEWORK_LABELS: Record<string, string> = {
  financial: "Financial",
  human_development: "Human Development",
  ecological: "Ecological",
  governance: "Governance",
  political_economy: "Political Economy",
};

function IndicatorRow({ ind }: { ind: GroundingIndicator }) {
  const value =
    ind.value != null
      ? `${ind.value}${ind.unit ? " " + ind.unit : ""}`
      : "—";
  const citation = [ind.source_institution, ind.data_vintage]
    .filter(Boolean)
    .join(" · ");
  const tier = ind.confidence_tier != null ? ` · T${ind.confidence_tier}` : "";

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "1fr auto",
        gap: "0 12px",
        padding: "3px 0",
        fontSize: 11,
        borderBottom: "1px solid rgba(255,255,255,0.04)",
        alignItems: "baseline",
      }}
    >
      <span style={{ color: "#cbd5e1" }}>
        <span style={{ color: "#8aa8c4" }}>{ind.display_name}:</span>{" "}
        <span style={{ fontWeight: 600 }}>{value}</span>
      </span>
      <span style={{ color: "#475569", whiteSpace: "nowrap" }}>
        {citation ? `${citation}${tier}` : tier || "—"}
      </span>
    </div>
  );
}

interface Props {
  scenarioId: string;
}

export default function GroundingStrip({ scenarioId }: Props) {
  const [data, setData] = useState<InitialStateResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setData(null);
    setLoading(true);

    let cancelled = false;
    fetch(`${API_BASE}/scenarios/${encodeURIComponent(scenarioId)}/initial-state`)
      .then((res) => {
        if (!res.ok) throw new Error(`${res.status}`);
        return res.json() as Promise<InitialStateResponse>;
      })
      .then((body) => {
        if (!cancelled) {
          setData(body);
          setLoading(false);
        }
      })
      .catch(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [scenarioId]);

  // Filter to named frameworks only — "None" key must not render.
  const namedFrameworks = data
    ? Object.entries(data.frameworks).filter(([key]) => key in FRAMEWORK_LABELS)
    : [];

  const hasData = namedFrameworks.length > 0;

  return (
    <div
      data-testid="grounding-strip"
      style={{
        background: "#0f1f33",
        borderBottom: "1px solid rgba(255,255,255,0.08)",
        color: "#cbd5e1",
        fontFamily: "system-ui, 'Segoe UI', sans-serif",
        maxHeight: 400,
        overflowY: "auto",
        padding: "8px 16px",
      }}
    >
      {loading ? (
        <span style={{ fontSize: 11, color: "#64748b" }}>Loading grounding data…</span>
      ) : !hasData ? (
        <span style={{ fontSize: 11, color: "#64748b" }}>
          Initial state data not available for this scenario
        </span>
      ) : (
        namedFrameworks.map(([key, section]) => {
          const visibleIndicators = section.indicators.filter(
            (ind: GroundingIndicator) => ind.value != null,
          );
          if (visibleIndicators.length === 0) return null;
          return (
            <div key={key} style={{ marginBottom: 10 }}>
              <div
                role="heading"
                aria-level={4}
                style={{
                  fontSize: 10,
                  fontWeight: 700,
                  textTransform: "uppercase",
                  letterSpacing: "0.08em",
                  color: "#8aa8c4",
                  marginBottom: 4,
                  paddingBottom: 2,
                  borderBottom: "1px solid rgba(138,168,196,0.2)",
                }}
              >
                {FRAMEWORK_LABELS[key]}
              </div>
              {visibleIndicators.map((ind: GroundingIndicator) => (
                <IndicatorRow key={ind.name} ind={ind} />
              ))}
            </div>
          );
        })
      )}
    </div>
  );
}
