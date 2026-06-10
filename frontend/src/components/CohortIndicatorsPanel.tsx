/* eslint-disable react-refresh/only-export-components */
/**
 * CohortIndicatorsPanel — Zone 1A human cost ledger strip.
 *
 * Shows the four highest-priority human development indicators below the
 * trajectory chart. Addresses GAP-04 (M11.5): both task-oriented Priority A
 * personas (P2 Finance Ministry Negotiator, P1 Programme Analyst) found the
 * primary analytical question — which cohorts are affected, by how much, at
 * which steps — unanswerable from composite scores alone.
 *
 * CLAUDE.md first principle: "The Human Cost Ledger is Primary." This panel
 * fulfils that commitment at the use-case level for Zone 1.
 *
 * Priority indicator order matches the M12 sprint plan acceptance criteria.
 * Indicators not present in the measurement output render as "—" without error.
 *
 * Implements: Issue #747, M11.5 Priority A synthesis GAP-04 (cross-session).
 */
import type { QuantitySchema } from "../types";
import { getIndicatorDisplayName } from "../lib/indicatorDisplayNames";

// ---------------------------------------------------------------------------
// Cohort indicator configuration
// ---------------------------------------------------------------------------

interface IndicatorConfig {
  key: string;
  direction: "higher_better" | "lower_better";
}

/** Priority order: bottom_quintile_consumption_capacity first (primary M12 HCL signal
 *  from ExternalSectorModule ADR-012). Remainder matches #747 acceptance criteria. */
export const PRIORITY_INDICATORS: IndicatorConfig[] = [
  { key: "bottom_quintile_consumption_capacity", direction: "higher_better" },
  { key: "unemployment_rate",                    direction: "lower_better"  },
  { key: "poverty_headcount_ratio",              direction: "lower_better"  },
  { key: "income_share_q1",                      direction: "higher_better" },
  { key: "access_to_healthcare",                 direction: "higher_better" },
];

// ---------------------------------------------------------------------------
// Pure functions — exported for unit tests
// ---------------------------------------------------------------------------

type Direction = "up" | "down" | null;

/** Derive movement direction from current vs previous Decimal-string values. */
export function computeDirection(
  current: QuantitySchema | undefined,
  prev: QuantitySchema | undefined,
): Direction {
  if (!current || !prev) return null;
  const curr = parseFloat(current.value);
  const prevVal = parseFloat(prev.value);
  if (!isFinite(curr) || !isFinite(prevVal)) return null;
  if (curr > prevVal) return "up";
  if (curr < prevVal) return "down";
  return null;
}

/** Arrow character + colour for a direction + polarity pair. */
export function directionGlyph(
  direction: Direction,
  polarity: "higher_better" | "lower_better",
): { symbol: string; color: string } | null {
  if (direction === null) return null;
  const isGood =
    (direction === "up" && polarity === "higher_better") ||
    (direction === "down" && polarity === "lower_better");
  return {
    symbol: direction === "up" ? "↑" : "↓",
    color: isGood ? "#2e7d32" : "#c62828",
  };
}

/** Format a Decimal-string value for display. */
export function formatIndicatorValue(qty: QuantitySchema | undefined): string {
  if (!qty) return "—";
  const n = parseFloat(qty.value);
  if (!isFinite(n)) return "—";
  // Percentages: multiply by 100 when value ≤ 1 and unit suggests a fraction
  const unit = qty.unit?.toLowerCase() ?? "";
  if ((unit === "fraction" || unit === "ratio" || unit === "index") && n <= 1.0 && n >= 0) {
    return `${(n * 100).toFixed(1)}%`;
  }
  if (n >= 1000) return n.toFixed(0);
  return n.toFixed(2);
}

// ---------------------------------------------------------------------------
// CohortIndicatorsPanel
// ---------------------------------------------------------------------------

interface Props {
  /** Current step's human_development framework indicators. */
  indicators: Record<string, QuantitySchema> | null;
  /** Previous step's human_development framework indicators (for direction). */
  prevIndicators: Record<string, QuantitySchema> | null;
}

export function CohortIndicatorsPanel({ indicators, prevIndicators }: Props) {
  const hasData = indicators !== null;

  return (
    <div
      data-testid="cohort-indicators-panel"
      style={{
        borderTop: "1px solid #e8e8e8",
        padding: "6px 8px 4px",
        background: "#fdfdfd",
      }}
    >
      <div
        style={{
          fontSize: 9,
          fontWeight: 600,
          color: "#888",
          letterSpacing: "0.08em",
          textTransform: "uppercase",
          marginBottom: 4,
        }}
      >
        Human Cost Ledger
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          columnGap: 8,
          rowGap: 3,
        }}
      >
        {PRIORITY_INDICATORS.map(({ key, direction: polarity }) => {
          const current = indicators?.[key];
          const prev = prevIndicators?.[key];
          const dir = computeDirection(current, prev);
          const glyph = directionGlyph(dir, polarity);
          const tier = current?.confidence_tier ?? null;
          const label = getIndicatorDisplayName("human_development", key);
          const shortLabel = label.replace(" Rate", "").replace(" Ratio", "").replace(" Headcount", "").replace("Secondary ", "");

          return (
            <div
              key={key}
              data-testid={`cohort-indicator-${key}`}
              style={{ display: "flex", alignItems: "baseline", gap: 3 }}
            >
              <span style={{ fontSize: 10, color: "#555", flexShrink: 0, minWidth: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: 90 }}>
                {shortLabel}
              </span>
              <span
                data-testid={`cohort-value-${key}`}
                style={{
                  fontSize: 11,
                  fontWeight: 700,
                  color: hasData ? "#1a1a2e" : "#bbb",
                  fontVariantNumeric: "tabular-nums",
                  flexShrink: 0,
                }}
              >
                {formatIndicatorValue(current)}
              </span>
              {glyph && (
                <span
                  data-testid={`cohort-direction-${key}`}
                  style={{ fontSize: 10, color: glyph.color, fontWeight: 700, flexShrink: 0 }}
                >
                  {glyph.symbol}
                </span>
              )}
              {tier !== null && (
                <span
                  data-testid={`cohort-tier-${key}`}
                  style={{ fontSize: 8, color: "#aaa", flexShrink: 0 }}
                >
                  T{tier}
                </span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
