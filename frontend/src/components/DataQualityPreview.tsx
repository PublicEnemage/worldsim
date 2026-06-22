import { useEffect, useState, useRef } from "react";
import type { DataQualityResponse, DataQualityFramework, PullJobResponse, PullJobStatusResponse } from "../types";

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

function FrameworkRow({ fw, onLoad }: { fw: DataQualityFramework; onLoad?: () => void }) {
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
        ) : fw.loadable ? (
          <span
            style={{ color: "#fbbf24", cursor: onLoad ? "pointer" : "default" }}
            onClick={onLoad}
            title="Click to load data for this entity"
          >
            {citation ? `${citation} · ` : ""}available — click to load
          </span>
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
  onPullComplete?: () => void;
}

export default function DataQualityPreview({ entityId, year, onPullComplete }: Props) {
  const [data, setData] = useState<DataQualityResponse | null>(null);
  const [unavailable, setUnavailable] = useState(false);
  const [pulling, setPulling] = useState(false);
  const [pullStatus, setPullStatus] = useState<string | null>(null);
  const [pullError, setPullError] = useState<string | null>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchData = () => {
    if (!entityId || !year) return;
    setData(null);
    setUnavailable(false);

    fetch(`${API_BASE}/entities/${encodeURIComponent(entityId)}/data-quality?year=${year}`)
      .then((res) => {
        if (!res.ok) throw new Error(`${res.status}`);
        return res.json() as Promise<DataQualityResponse>;
      })
      .then((body) => setData(body))
      .catch(() => setUnavailable(true));
  };

  useEffect(() => {
    fetchData();
    // Cancel any active pull when entity/year changes
    setPulling(false);
    setPullStatus(null);
    setPullError(null);
    if (pollRef.current) {
      clearInterval(pollRef.current);
      pollRef.current = null;
    }
  }, [entityId, year]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, []);

  const handlePull = async () => {
    if (pulling || !entityId || !year) return;
    setPulling(true);
    setPullStatus("queued");
    setPullError(null);

    try {
      const res = await fetch(
        `${API_BASE}/entities/${encodeURIComponent(entityId)}/pull?year=${year}`,
        { method: "POST" }
      );
      if (!res.ok) throw new Error(`Pull request failed: ${res.status}`);
      const job = await res.json() as PullJobResponse;
      setPullStatus(job.status);

      // Poll until complete or failed
      pollRef.current = setInterval(async () => {
        try {
          const pollRes = await fetch(
            `${API_BASE}/entities/${encodeURIComponent(entityId)}/pull/${encodeURIComponent(job.job_id)}`
          );
          if (!pollRes.ok) return;
          const statusData = await pollRes.json() as PullJobStatusResponse;
          setPullStatus(statusData.status);

          if (statusData.status === "complete") {
            if (pollRef.current) clearInterval(pollRef.current);
            pollRef.current = null;
            setPulling(false);
            fetchData();
            onPullComplete?.();
          } else if (statusData.status === "failed") {
            if (pollRef.current) clearInterval(pollRef.current);
            pollRef.current = null;
            setPulling(false);
            setPullError(statusData.error ?? "Pull failed");
          }
        } catch {
          // poll errors are transient — continue polling
        }
      }, 3000);
    } catch (err) {
      setPulling(false);
      setPullStatus("failed");
      setPullError(err instanceof Error ? err.message : "Pull failed");
    }
  };

  const hasLoadable = data?.frameworks.some((fw) => fw.loadable) ?? false;

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
            <FrameworkRow
              key={fw.framework}
              fw={fw}
              onLoad={fw.loadable ? () => void handlePull() : undefined}
            />
          ))}

          {hasLoadable && !pulling && pullStatus !== "complete" && (
            <button
              data-testid="data-pull-action"
              onClick={() => void handlePull()}
              style={{
                marginTop: 6,
                fontSize: 11,
                background: "rgba(59,130,246,0.15)",
                border: "1px solid rgba(59,130,246,0.4)",
                borderRadius: 3,
                color: "#93c5fd",
                padding: "3px 8px",
                cursor: "pointer",
                width: "100%",
              }}
            >
              Load data for {entityId} {year}
            </button>
          )}

          {pulling && (
            <div
              data-testid="data-pull-progress"
              style={{
                marginTop: 6,
                fontSize: 11,
                color: "#fbbf24",
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              <span
                style={{
                  display: "inline-block",
                  width: 10,
                  height: 10,
                  borderRadius: "50%",
                  border: "2px solid #fbbf24",
                  borderTopColor: "transparent",
                  animation: "spin 0.8s linear infinite",
                }}
              />
              Pulling data{pullStatus ? ` — ${pullStatus}` : ""}…
            </div>
          )}

          {pullError && (
            <div style={{ marginTop: 4, fontSize: 11, color: "#f87171" }}>
              Pull failed: {pullError}
            </div>
          )}

          {pullStatus === "complete" && !pulling && (
            <div style={{ marginTop: 4, fontSize: 11, color: "#6ee7b7" }}>
              Data loaded ✓
            </div>
          )}
        </>
      )}

      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
