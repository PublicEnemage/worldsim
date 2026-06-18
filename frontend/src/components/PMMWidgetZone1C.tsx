/* eslint-disable react-refresh/only-export-components */
/**
 * PMMWidgetZone1C — Zone 1C co-primary instrument.
 *
 * Displays the Policy Maneuver Margin: numeric value, direction arrow,
 * and mode-specific header label. Distinct from FrameworkPanel rows (US-020).
 *
 * Mode-specific labels (ADR-008 Decision 6):
 *   Mode 1 → "Policy Maneuver Margin — historical"
 *   Mode 2 → "Policy Maneuver Margin — projected"
 *   Mode 3 → "Policy Maneuver Margin — current"
 *
 * Pending state: when computation_state === "computing" the widget renders
 * at reduced opacity to signal the value is stale (Mode 3 only requirement,
 * applied globally for simplicity — ADR-008 Decision 6).
 *
 * Implements: US-019, US-020, ADR-008 Decision 6
 */
import { useScenarioStepStore } from "../store/scenarioStepStore";

// ---------------------------------------------------------------------------
// Exported constants and pure functions (tested by PMMWidgetZone1C.test.ts)
// ---------------------------------------------------------------------------

export const PMM_LABELS: Record<"MODE_1" | "MODE_2" | "MODE_3", string> = {
  MODE_1: "Policy Maneuver Margin — historical",
  MODE_2: "Policy Maneuver Margin — projected",
  MODE_3: "Policy Maneuver Margin — current",
};

/**
 * Returns the mode-specific PMM header label. US-019 / ADR-008 Decision 6.
 */
export function getPmmLabel(mode: "MODE_1" | "MODE_2" | "MODE_3"): string {
  return PMM_LABELS[mode];
}

/**
 * Maps PMM direction to a Unicode arrow character for the trend indicator.
 * Null direction (no prior step to compare against) renders "—".
 */
export function getPmmArrow(direction: "up" | "down" | "flat" | null): string {
  if (direction === "up") return "↑";
  if (direction === "down") return "↓";
  if (direction === "flat") return "→";
  return "—";
}

/**
 * Returns the plain-language note shown when PMM is None due to all thresholds breached.
 * Empty string when PMM has a value — note is suppressed.
 * DEMO-019: distinguishes "margin fully exhausted" from "not computed" / "not applicable".
 */
export function getPmmBreachedNote(pmmValue: number | null): string {
  return pmmValue === null ? "All thresholds breached — see alerts" : "";
}

/**
 * Returns the CSS color for the direction arrow.
 * Green-family avoided (CVD constraint from MV-001 — teal only for ecological).
 */
export function getPmmArrowColor(direction: "up" | "down" | "flat" | null): string {
  if (direction === "up") return "#2271B3";   // financial blue — margin improving
  if (direction === "down") return "#cc0000"; // critical red — margin shrinking
  if (direction === "flat") return "#888";    // neutral gray
  return "#aaa";                              // no data
}

// ---------------------------------------------------------------------------
// PMMWidgetZone1C
// ---------------------------------------------------------------------------

interface PMMWidgetZone1CProps {
  "data-testid"?: string;
}

export function PMMWidgetZone1C({
  "data-testid": dataTestId = "zone-1c-pmm",
}: PMMWidgetZone1CProps) {
  const { pmm_value, pmm_direction, mode, computation_state } = useScenarioStepStore();

  const label = getPmmLabel(mode);
  const arrow = getPmmArrow(pmm_direction);
  const arrowColor = getPmmArrowColor(pmm_direction);
  const breachedNote = getPmmBreachedNote(pmm_value);
  const isPending = computation_state === "computing";

  const formattedValue =
    pmm_value === null ? "—" : pmm_value.toFixed(2);

  return (
    <div
      data-testid={dataTestId}
      data-mode={mode}
      data-computation-state={computation_state}
      style={{
        padding: "8px 10px",
        opacity: isPending ? 0.4 : 1,
        transition: "opacity 150ms ease",
        boxSizing: "border-box",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
      }}
    >
      {/* Mode-specific header label — US-019 */}
      <div
        data-testid="pmm-label"
        style={{
          fontSize: 10,
          color: "#666",
          letterSpacing: 0.2,
          marginBottom: 6,
          lineHeight: 1.3,
        }}
      >
        {label}
      </div>

      {/* Numeric value + direction arrow */}
      <div
        style={{ display: "flex", alignItems: "baseline", gap: 8 }}
      >
        <span
          data-testid="pmm-value"
          style={{
            fontSize: 26,
            fontWeight: 700,
            color: "#222",
            letterSpacing: -0.5,
          }}
        >
          {formattedValue}
        </span>

        <span
          data-testid="pmm-direction-arrow"
          aria-label={`PMM direction: ${pmm_direction ?? "unknown"}`}
          style={{
            fontSize: 20,
            color: arrowColor,
            fontWeight: 700,
          }}
        >
          {arrow}
        </span>
      </div>

      {/* Pre-calibration annotation — ADR-015 §Component 1 §Zone 1C (Decision 3 placeholder) */}
      <div
        data-testid="pmm-annotation"
        style={{ fontSize: 9, color: "#aaa", marginTop: 2, lineHeight: 1.3 }}
      >
        [T3 composite · pre-cal]
      </div>

      {/* Scale reference — lower value = more constrained policy space (DEMO-059) */}
      <div
        data-testid="pmm-scale-note"
        style={{ fontSize: 9, color: "#aaa", marginTop: 4, lineHeight: 1.3 }}
      >
        ↓ lower = more constrained
      </div>

      {/* Contextual note when all thresholds are breached (pmm_value === null) */}
      {breachedNote && !isPending && (
        <div
          data-testid="pmm-breached-note"
          style={{ fontSize: 10, color: "#cc0000", marginTop: 4, lineHeight: 1.3 }}
        >
          {breachedNote}
        </div>
      )}

      {/* Pending label — Mode 3 computation in flight */}
      {isPending && (
        <div
          data-testid="pmm-pending"
          style={{ fontSize: 10, color: "#aaa", marginTop: 4 }}
        >
          Updating…
        </div>
      )}
    </div>
  );
}
