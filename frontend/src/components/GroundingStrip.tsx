import { useEffect, useState } from "react";
import type { InitialStateResponse, GroundingIndicator } from "../types";
import { useScenarioStepStore } from "../store/scenarioStepStore";

const API_BASE = "http://localhost:8000/api/v1";

// Named frameworks only — "None" key must not render as a section heading.
const FRAMEWORK_LABELS: Record<string, string> = {
  financial: "Financial",
  human_development: "Human Development",
  ecological: "Ecological",
  governance: "Governance",
  political_economy: "Political Economy",
};

// Month abbreviations for Q1–Q4 (start-of-quarter convention).
const QUARTER_MONTHS = ["Jan", "Apr", "Jul", "Oct"];

/**
 * Format a vintage date string for human-readable display.
 *
 * "YYYY-QN" → "Mmm YYYY" (e.g., "2024-Q1" → "Jan 2024").
 * "YYYY-MM-DD" → "Mmm YYYY" via Date parsing.
 * Anything else is returned unchanged.
 */
function formatVintageDate(vintage: string): string {
  const quarterMatch = vintage.match(/^(\d{4})-Q([1-4])$/i);
  if (quarterMatch) {
    const year = quarterMatch[1];
    const quarter = parseInt(quarterMatch[2], 10);
    return `${QUARTER_MONTHS[quarter - 1]} ${year}`;
  }
  const isoMatch = vintage.match(/^(\d{4})-(\d{2})-\d{2}$/);
  if (isoMatch) {
    const d = new Date(`${vintage}T00:00:00Z`);
    return d.toLocaleDateString("en-US", { month: "short", year: "numeric", timeZone: "UTC" });
  }
  return vintage;
}

/**
 * Extract the first non-null vintage date across all frameworks and format it.
 * Returns null if no vintage is available.
 */
function extractReferenceDate(frameworks: InitialStateResponse["frameworks"]): string | null {
  for (const section of Object.values(frameworks)) {
    for (const ind of section.indicators) {
      if (ind.vintage) return formatVintageDate(ind.vintage);
    }
  }
  return null;
}

function IndicatorRow({ ind }: { ind: GroundingIndicator }) {
  const value =
    ind.value != null
      ? `${ind.value}${ind.unit ? " " + ind.unit : ""}`
      : "—";
  const formattedVintage = ind.vintage ? formatVintageDate(ind.vintage) : null;
  const citation = [ind.source, formattedVintage]
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

// Current-step indicator value (model output — no citation metadata)
function CurrentIndicatorRow({
  displayName,
  value,
  unit,
}: {
  displayName: string;
  value: string | null;
  unit: string | null;
}) {
  const formatted = value != null ? `${value}${unit ? " " + unit : ""}` : "—";
  return (
    <div
      style={{
        padding: "3px 0",
        fontSize: 11,
        borderBottom: "1px solid rgba(255,255,255,0.04)",
        color: "#cbd5e1",
      }}
    >
      <span style={{ color: "#8aa8c4" }}>{displayName}:</span>{" "}
      <span style={{ fontWeight: 600 }}>{formatted}</span>
    </div>
  );
}

// Current step indicator value map: { framework -> { indicator_key -> { value, unit } } }
interface CurrentIndicatorValue {
  value: string | null;
  unit: string | null;
}

interface Props {
  scenarioId: string;
}

export default function GroundingStrip({ scenarioId }: Props) {
  const [data, setData] = useState<InitialStateResponse | null>(null);
  const [loading, setLoading] = useState(true);

  // Current step data for dual-value disambiguation (#1069, ADR-016 §Component 2)
  const [currentValues, setCurrentValues] = useState<Record<string, Record<string, CurrentIndicatorValue>> | null>(null);

  // Read current step and entity id from the Zustand store
  const { current_step, trajectory } = useScenarioStepStore();
  const entityId = trajectory?.entity_id ?? null;

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

  // Fetch current step indicator values for the simulation section (#1069)
  useEffect(() => {
    if (!entityId || current_step <= 0) {
      setCurrentValues(null);
      return;
    }

    let cancelled = false;
    fetch(
      `${API_BASE}/scenarios/${encodeURIComponent(scenarioId)}/measurement-output?entity_id=${encodeURIComponent(entityId)}&step=${current_step}`
    )
      .then((res) => {
        if (!res.ok) throw new Error(`${res.status}`);
        return res.json() as Promise<{
          outputs: Record<string, { indicators: Record<string, { value: string | null; unit?: string | null }> }>;
        }>;
      })
      .then((body) => {
        if (cancelled) return;
        const parsed: Record<string, Record<string, CurrentIndicatorValue>> = {};
        for (const [fw, output] of Object.entries(body.outputs)) {
          parsed[fw] = {};
          for (const [key, ind] of Object.entries(output.indicators)) {
            if (ind !== null && typeof ind === "object" && "value" in ind) {
              parsed[fw][key] = {
                value: (ind as { value: string | null }).value,
                unit: (ind as { unit?: string | null }).unit ?? null,
              };
            }
          }
        }
        setCurrentValues(parsed);
      })
      .catch(() => {
        if (!cancelled) setCurrentValues(null);
      });

    return () => {
      cancelled = true;
    };
  }, [scenarioId, entityId, current_step]);

  // Filter to named frameworks only — "None" key must not render.
  const namedFrameworks = data
    ? Object.entries(data.frameworks).filter(([key]) => key in FRAMEWORK_LABELS)
    : [];

  const hasData = namedFrameworks.length > 0;
  const hasCurrentData = currentValues !== null && current_step > 0;
  const referenceDate = data ? extractReferenceDate(data.frameworks) : null;

  const sectionHeaderStyle: React.CSSProperties = {
    fontSize: 10,
    fontWeight: 600,
    color: "#6b9abf",
    marginBottom: 4,
    marginTop: 2,
    letterSpacing: "0.04em",
  };

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
        <>
          {/* Initial conditions section — source-cited entry-state values */}
          <div style={{ marginBottom: hasCurrentData ? 8 : 0 }}>
            <div style={sectionHeaderStyle}>
              Initial conditions (step 0 · source-cited data)
              {referenceDate && (
                <span
                  data-testid="grounding-strip-date"
                  style={{ marginLeft: 8, fontWeight: 400, color: "#64748b" }}
                >
                  · {referenceDate}
                </span>
              )}
            </div>
            {namedFrameworks.map(([key, section]) => {
              const visibleIndicators = section.indicators.filter(
                (ind: GroundingIndicator) => ind.value != null,
              );
              if (visibleIndicators.length === 0) return null;
              return (
                <div key={key} style={{ marginBottom: 8 }}>
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
            })}
          </div>

          {/* Current trajectory section — model output at current step (#1069) */}
          {hasCurrentData && (
            <div
              style={{
                borderTop: "1px solid rgba(255,255,255,0.1)",
                paddingTop: 8,
              }}
            >
              <div style={sectionHeaderStyle}>
                Current trajectory (step {current_step} · model output)
              </div>
              {namedFrameworks.map(([fwKey, section]) => {
                const fwCurrent = currentValues![fwKey];
                if (!fwCurrent) return null;

                const matchingIndicators = section.indicators.filter((ind: GroundingIndicator) => {
                  const cur = fwCurrent[ind.name];
                  return cur && cur.value !== null;
                });

                if (matchingIndicators.length === 0) return null;

                return (
                  <div key={fwKey} style={{ marginBottom: 8 }}>
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
                      {FRAMEWORK_LABELS[fwKey]}
                    </div>
                    {matchingIndicators.map((ind: GroundingIndicator) => {
                      const cur = fwCurrent[ind.name];
                      return (
                        <CurrentIndicatorRow
                          key={ind.name}
                          displayName={ind.display_name}
                          value={cur.value}
                          unit={cur.unit ?? ind.unit}
                        />
                      );
                    })}
                  </div>
                );
              })}
            </div>
          )}
        </>
      )}
    </div>
  );
}
