/**
 * AssumptionSurface — ADR-015 §Component 2.
 *
 * A single-line fixed-height strip rendered between the scenario identity header
 * (Zone 0) and the instrument cluster (Zone 1). Shows the key assumptions that
 * shaped the current trajectory at zero interaction.
 *
 * Content priority (fallback order per DA-G5-3 and intent doc §4c §Component 2):
 *   1. Fiscal multiplier (if non-null and non-default)
 *   2. Political economy: enabled (if PE module is enabled)
 *   3. Conditionality type (if PE enabled and conditionality_type is present)
 *   4. Data vintage (derived from start_date as YYYY-Q{N})
 *
 * Silent failure: if no content items can be derived (empty configuration),
 * renders data-testid="assumption-surface-unavailable" instead of an empty strip.
 *
 * Max height: 24px at all viewport widths (AC-6 constraint).
 * Content overflow: truncated with ellipsis — no wrapping.
 *
 * Implements: ADR-015 §Component 2, AC-5 through AC-8.
 */
import type { CSSProperties } from "react";
import type { ScenarioDetailResponse } from "../types";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Derive a "YYYY-Q{N}" vintage label from a start_date string like "2023-01-01". */
function deriveVintageFromStartDate(startDate: string | null | undefined): string | null {
  if (!startDate) return null;
  const match = /^(\d{4})-(\d{2})/.exec(startDate);
  if (!match) return null;
  const year = match[1];
  const month = parseInt(match[2], 10);
  const quarter = Math.ceil(month / 3);
  return `${year}-Q${quarter}`;
}

// ---------------------------------------------------------------------------
// Styles — single-line constraint: max 24px height, ellipsis overflow (AC-6)
// ---------------------------------------------------------------------------

const SURFACE_STYLE: CSSProperties = {
  maxHeight: 24,
  height: 24,
  lineHeight: "24px",
  overflow: "hidden",
  whiteSpace: "nowrap",
  textOverflow: "ellipsis",
  padding: "0 10px",
  fontSize: 10,
  color: "#666",
  background: "#f7f5ff",
  borderBottom: "1px solid #e9d5ff",
  boxSizing: "border-box",
};

const UNAVAILABLE_STYLE: CSSProperties = {
  height: 0,
  overflow: "hidden",
};

// ---------------------------------------------------------------------------
// AssumptionSurface
// ---------------------------------------------------------------------------

interface AssumptionSurfaceProps {
  detail: ScenarioDetailResponse | null;
}

export function AssumptionSurface({ detail }: AssumptionSurfaceProps) {
  if (!detail) {
    return (
      <div
        data-testid="assumption-surface-unavailable"
        style={UNAVAILABLE_STYLE}
      />
    );
  }

  const { configuration } = detail;

  const parts: string[] = [];

  // Fiscal multiplier — only if non-default (default 1.0) and present
  const fiscalMultiplier = configuration.fiscal_multiplier;
  if (fiscalMultiplier !== null && fiscalMultiplier !== undefined && fiscalMultiplier !== 1.0) {
    parts.push(`Fiscal ×${fiscalMultiplier.toFixed(2)}`);
  }

  // Political economy module status
  const peEnabled = configuration.modules_config?.political_economy?.enabled;
  if (peEnabled === true) {
    parts.push("Political economy: enabled");
    // Conditionality type — only shown when PE is enabled
    const condType = configuration.modules_config?.political_economy?.conditionality_type;
    if (condType) {
      parts.push(`Conditionality: ${condType}`);
    }
  }

  // Data vintage — derived from start_date
  const vintage = deriveVintageFromStartDate(configuration.start_date);
  if (vintage) {
    parts.push(`Data: ${vintage} vintage`);
  }

  if (parts.length === 0) {
    return (
      <div
        data-testid="assumption-surface-unavailable"
        style={UNAVAILABLE_STYLE}
      />
    );
  }

  return (
    <div
      data-testid="assumption-surface"
      style={SURFACE_STYLE}
    >
      {parts.join(" · ")}
    </div>
  );
}
