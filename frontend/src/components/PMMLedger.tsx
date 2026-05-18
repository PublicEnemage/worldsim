// PMMLedger — Coffin Corner / Policy Maneuver Margin widget
// Zone 1C: between MDA alert panel (Zone 1A) and radar chart (Zone 1B).
// ADR-005 Amendment 3 Area 2: dedicated Zone 1 widget with directional indicator.
// M8 render state: pmm_score is null (backend computation not yet complete).
// Live score ships when backend PMM computation is implemented.

export interface PMMLedgerProps {
  pmm_score: number | null;
  pmm_trend: "improving" | "stable" | "deteriorating" | null;
}

function trendArrow(trend: "improving" | "stable" | "deteriorating" | null): string {
  if (trend === "improving") return "↑";
  if (trend === "deteriorating") return "↓";
  if (trend === "stable") return "→";
  return "—";
}

function scoreColor(score: number): string {
  if (score > 0.6) return "#0a6b0a";
  if (score >= 0.3) return "#a66000";
  return "#c00";
}

function scoreLabel(score: number | null): string {
  if (score === null) return "—";
  return `${(score * 100).toFixed(0)}`;
}

export default function PMMLedger({ pmm_score, pmm_trend }: PMMLedgerProps) {
  const isNull = pmm_score === null;

  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: 4,
        padding: "8px 12px",
        marginBottom: 12,
        background: "#fafcff",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div>
          <div style={{ fontSize: 11, color: "#666", marginBottom: 2, fontWeight: 600 }}>
            Policy Maneuver Margin
          </div>
          <div style={{ fontSize: 9, color: "#aaa" }}>
            Coffin Corner indicator — remaining degrees of policy freedom
          </div>
        </div>

        {isNull ? (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 6,
              fontSize: 12,
              color: "#aaa",
              fontStyle: "italic",
            }}
          >
            <span
              style={{
                display: "inline-block",
                width: 10,
                height: 10,
                borderRadius: "50%",
                border: "2px solid #ccc",
                borderTopColor: "#888",
                animation: "spin 1s linear infinite",
              }}
            />
            computing…
          </div>
        ) : (
          <div style={{ display: "flex", alignItems: "baseline", gap: 4 }}>
            <span
              style={{
                fontSize: 28,
                fontWeight: 700,
                color: scoreColor(pmm_score!),
                lineHeight: 1,
              }}
            >
              {scoreLabel(pmm_score)}
            </span>
            <span style={{ fontSize: 13, color: "#888" }}>/100</span>
            <span
              style={{
                fontSize: 18,
                color: pmm_trend === "improving"
                  ? "#0a6b0a"
                  : pmm_trend === "deteriorating"
                  ? "#c00"
                  : "#888",
                marginLeft: 4,
              }}
              title={pmm_trend ?? undefined}
            >
              {trendArrow(pmm_trend)}
            </span>
          </div>
        )}
      </div>

      {!isNull && (
        <div style={{ marginTop: 6 }}>
          <div
            style={{
              height: 4,
              borderRadius: 2,
              background: "#eee",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                height: "100%",
                width: `${(pmm_score! * 100).toFixed(0)}%`,
                background: scoreColor(pmm_score!),
                transition: "width 0.3s ease-in-out",
              }}
            />
          </div>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontSize: 9,
              color: "#ccc",
              marginTop: 2,
            }}
          >
            <span>Constrained</span>
            <span>Full margin</span>
          </div>
        </div>
      )}
    </div>
  );
}
