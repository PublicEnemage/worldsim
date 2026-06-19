import { useEffect, useState } from "react";
import type { DataQualityResponse, DataQualityFramework } from "../types";

const API_BASE = "http://localhost:8000/api/v1";

const FRAMEWORK_LABELS: Record<string, string> = {
  financial: "Financial",
  human_development: "Human Dev",
  ecological: "Ecological",
  governance: "Governance",
  political_economy: "Pol. Economy",
};

function TierBadge({ tier }: { tier: number }) {
  const color = tier <= 2 ? "#6ee7b7" : tier === 3 ? "#fbbf24" : "#f87171";
  return (
    <span
      style={{
        fontWeight: 700,
        color,
        fontSize: 11,
        minWidth: 22,
        display: "inline-block",
      }}
    >
      T{tier}
    </span>
  );
}

function FrameworkRow({ fw }: { fw: DataQualityFramework }) {
  const label = FRAMEWORK_LABELS[fw.framework] ?? fw.framework;
  const citation = [fw.source_institution, fw.data_vintage].filter(Boolean).join(" · ");
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "90px 24px 1fr",
        gap: "0 6px",
        padding: "2px 0",
        fontSize: 11,
        alignItems: "baseline",
      }}
    >
      <span style={{ color: "#94a3b8" }}>{label}</span>
      <TierBadge tier={fw.confidence_tier} />
      <span style={{ color: "#64748b" }}>
        {fw.is_synthetic ? (
          <>
            <span style={{ color: "#f87171" }}>synthetic</span>
            {fw.synthetic_basis ? ` — ${fw.synthetic_basis}` : ""}
          </>
        ) : (
          citation || "—"
        )}
      </span>
    </div>
  );
}

interface Props {
  entityId: string;
  year: number;
}

export default function DataQualityPreview({ entityId, year }: Props) {
  const [data, setData] = useState<DataQualityResponse | null>(null);
  const [unavailable, setUnavailable] = useState(false);

  useEffect(() => {
    if (!entityId || !year) return;
    setData(null);
    setUnavailable(false);

    let cancelled = false;
    fetch(`${API_BASE}/entities/${encodeURIComponent(entityId)}/data-quality?year=${year}`)
      .then((res) => {
        if (!res.ok) throw new Error(`${res.status}`);
        return res.json() as Promise<DataQualityResponse>;
      })
      .then((body) => {
        if (!cancelled) setData(body);
      })
      .catch(() => {
        if (!cancelled) setUnavailable(true);
      });

    return () => {
      cancelled = true;
    };
  }, [entityId, year]);

  return (
    <div
      data-testid="data-quality-preview"
      style={{
        background: "rgba(15,31,51,0.92)",
        border: "1px solid rgba(100,148,200,0.25)",
        borderRadius: 4,
        padding: "8px 10px",
        marginTop: 8,
        color: "#cbd5e1",
        fontFamily: "system-ui, 'Segoe UI', sans-serif",
      }}
    >
      {unavailable ? (
        <span style={{ fontSize: 11, color: "#f87171" }}>
          Data quality preview unavailable
        </span>
      ) : !data ? (
        <span style={{ fontSize: 11, color: "#64748b" }}>Loading…</span>
      ) : data.frameworks.length === 0 ? (
        <span style={{ fontSize: 11, color: "#64748b" }}>
          No coverage data for {entityId} {year}.
        </span>
      ) : (
        <>
          <div style={{ fontSize: 11, color: "#8aa8c4", marginBottom: 4, fontWeight: 600 }}>
            {data.entity_id} · {data.year}
          </div>
          {data.frameworks.map((fw) => (
            <FrameworkRow key={fw.framework} fw={fw} />
          ))}
        </>
      )}
    </div>
  );
}
