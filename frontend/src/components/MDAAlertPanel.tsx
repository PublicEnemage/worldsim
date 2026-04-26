import type { MDAAlert, MDASeverity } from "../types";

interface Props {
  alerts: MDAAlert[];
}

const SEVERITY_ORDER: Record<MDASeverity, number> = {
  TERMINAL: 0,
  CRITICAL: 1,
  WARNING: 2,
};

const SEVERITY_COLORS: Record<MDASeverity, string> = {
  TERMINAL: "#7f0000",
  CRITICAL: "#c00",
  WARNING: "#a06000",
};

const SEVERITY_BG: Record<MDASeverity, string> = {
  TERMINAL: "#fff0f0",
  CRITICAL: "#fff5f5",
  WARNING: "#fffbe6",
};

function severityBadge(severity: MDASeverity) {
  return (
    <span
      style={{
        background: SEVERITY_COLORS[severity],
        color: "#fff",
        borderRadius: 3,
        padding: "1px 6px",
        fontSize: 11,
        fontWeight: 700,
        letterSpacing: 0.5,
        marginRight: 6,
      }}
    >
      {severity}
    </span>
  );
}

export default function MDAAlertPanel({ alerts }: Props) {
  if (alerts.length === 0) {
    return (
      <div style={{ color: "#555", fontSize: 13, padding: "8px 0" }}>
        No active MDA threshold breaches.
      </div>
    );
  }

  const sorted = [...alerts].sort(
    (a, b) => SEVERITY_ORDER[a.severity] - SEVERITY_ORDER[b.severity],
  );

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      {sorted.map((alert) => (
        <div
          key={`${alert.mda_id}-${alert.entity_id}`}
          style={{
            background: SEVERITY_BG[alert.severity],
            border: `1px solid ${SEVERITY_COLORS[alert.severity]}33`,
            borderLeft: `3px solid ${SEVERITY_COLORS[alert.severity]}`,
            borderRadius: 4,
            padding: "8px 10px",
            fontSize: 12,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", marginBottom: 4 }}>
            {severityBadge(alert.severity)}
            <span style={{ fontWeight: 600, fontSize: 13 }}>{alert.mda_id}</span>
          </div>

          <div style={{ color: "#444", marginBottom: 2 }}>
            <span style={{ fontFamily: "monospace" }}>{alert.indicator_key}</span>
            {" — "}
            <span style={{ color: "#333" }}>
              current: <strong>{alert.current_value}</strong>
            </span>
            {" / floor: "}
            <strong>{alert.floor_value}</strong>
          </div>

          <div style={{ color: "#666", marginBottom: 2 }}>
            Distance to floor:{" "}
            <span
              style={{
                color:
                  parseFloat(alert.approach_pct_remaining) < 0 ? SEVERITY_COLORS[alert.severity] : "#060",
                fontWeight: 600,
              }}
            >
              {(parseFloat(alert.approach_pct_remaining) * 100).toFixed(1)}%
            </span>
            {" · consecutive breach steps: "}
            <strong>{alert.consecutive_breach_steps}</strong>
          </div>

          {alert.entity_id.includes(":CHT:") && (
            <div style={{ color: "#888", fontSize: 11, marginBottom: 2 }}>
              cohort: {alert.entity_id}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
