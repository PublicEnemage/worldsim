import type { ScenarioDetailResponse } from "../types";

const NOT_RECORDED = "(not recorded)";

function ParamRow({ label, value }: { label: string; value: string }) {
  const isAbsent = value === NOT_RECORDED;
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "130px 1fr",
        gap: "0 8px",
        padding: "3px 0",
        fontSize: 11,
        borderBottom: "1px solid rgba(255,255,255,0.05)",
        alignItems: "baseline",
      }}
    >
      <span style={{ color: "#64748b" }}>{label}</span>
      <span
        style={{
          color: isAbsent ? "#475569" : "#cbd5e1",
          fontStyle: isAbsent ? "italic" : "normal",
          fontWeight: isAbsent ? 400 : 600,
        }}
      >
        {value}
      </span>
    </div>
  );
}

interface Props {
  detail: ScenarioDetailResponse | null;
}

export default function ScenarioParameters({ detail }: Props) {
  if (!detail) return null;

  const cfg = detail.configuration;

  const entity = cfg.entities[0] ?? NOT_RECORDED;
  const nSteps = cfg.n_steps != null ? String(cfg.n_steps) : NOT_RECORDED;
  const fiscalMultiplier =
    cfg.fiscal_multiplier != null ? cfg.fiscal_multiplier.toFixed(2) : NOT_RECORDED;

  // Base year from start_date "YYYY-MM-DD" or "(not recorded)"
  let baseYear = NOT_RECORDED;
  if (cfg.start_date) {
    const year = cfg.start_date.slice(0, 4);
    if (/^\d{4}$/.test(year)) baseYear = year;
  }

  return (
    <div
      data-testid="scenario-parameters"
      style={{
        background: "#0f1f33",
        borderBottom: "1px solid rgba(255,255,255,0.08)",
        color: "#cbd5e1",
        fontFamily: "system-ui, 'Segoe UI', sans-serif",
        padding: "10px 16px",
      }}
    >
      <div
        style={{
          fontSize: 10,
          fontWeight: 700,
          textTransform: "uppercase",
          letterSpacing: "0.08em",
          color: "#8aa8c4",
          marginBottom: 6,
        }}
      >
        Scenario Parameters
      </div>
      <ParamRow label="Entity" value={entity} />
      <ParamRow label="Base year" value={baseYear} />
      <ParamRow label="Steps" value={nSteps} />
      <ParamRow label="Fiscal multiplier" value={fiscalMultiplier} />
    </div>
  );
}
