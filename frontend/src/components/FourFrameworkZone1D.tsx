/**
 * FourFrameworkZone1D — Zone 1D co-primary instrument.
 *
 * Quick-read numeric readout of the four composite scores at the current step.
 * All four values visible simultaneously — no tabs, toggles, or scroll (US-021).
 *
 * Null governance pattern extends DD-011 (M8 radar) into Zone 1:
 *   composite_score === null → class "score-value--null", displays "—" (US-022)
 *   composite_score === 0.00 → class "score-value--numeric", displays "0.00" (US-022)
 *
 * Derives current step scores from trajectory + current_step in the Zustand atom.
 * Atomicity guaranteed by single-store subscription (DD-012, US-023).
 *
 * Implements: US-021, US-022, ADR-008 Decision 7, DD-011
 */
import React from "react";
import { useScenarioStepStore } from "../store/scenarioStepStore";
import { FRAMEWORK_COLORS } from "../constants/frameworkColors";
import { sortAlerts } from "./MDAAlertPanelZone1B";

// ---------------------------------------------------------------------------
// Exported constants and pure functions (tested by FourFrameworkZone1D.test.ts)
// ---------------------------------------------------------------------------

/** Human-readable labels for the four frameworks (US-021 — no raw field names). */
export const FRAMEWORK_DISPLAY_LABELS: Record<string, string> = {
  financial: "Financial",
  human_development: "Human Development",
  ecological: "Ecological",
  governance: "Governance",
};

/** Canonical display order for the four frameworks. */
export const FRAMEWORK_ORDER = [
  "financial",
  "human_development",
  "ecological",
  "governance",
] as const;

/**
 * Format a composite score for display.
 * null → "—"; numeric (including 0) → toFixed(2). US-022.
 */
export function formatScore(score: number | null): string {
  if (score === null) return "—";
  return score.toFixed(2);
}

/**
 * Returns the CSS class for a score value element.
 * null → "score-value--null"; numeric → "score-value--numeric". UX-RULING-2 / US-022.
 */
export function getScoreClass(score: number | null): "score-value--null" | "score-value--numeric" {
  return score === null ? "score-value--null" : "score-value--numeric";
}

// ---------------------------------------------------------------------------
// FourFrameworkZone1D
// ---------------------------------------------------------------------------

interface FourFrameworkZone1DProps {
  "data-testid"?: string;
  /** True while the trajectory fetch is in flight (IR-006). */
  isLoading?: boolean;
  /** True if the trajectory fetch failed (IR-006). */
  isError?: boolean;
  /** Called when the user clicks "see alerts →" for a framework (#745). */
  onSelectFrameworkAlert?: (mdaId: string) => void;
}

const CONTAINER_STYLE: React.CSSProperties = {
  padding: "6px 10px",
  boxSizing: "border-box",
  height: "100%",
  display: "flex",
  flexDirection: "column",
  justifyContent: "space-around",
};

export function FourFrameworkZone1D({
  "data-testid": dataTestId = "zone-1d-four-framework",
  isLoading = false,
  isError = false,
  onSelectFrameworkAlert,
}: FourFrameworkZone1DProps) {
  const { trajectory, current_step, mda_alerts } = useScenarioStepStore();

  // Top alert per framework for the "see alerts →" navigation link (#745)
  const topAlertByFramework: Record<string, string> = {};
  for (const alert of sortAlerts(mda_alerts)) {
    if (!(alert.framework in topAlertByFramework)) {
      topAlertByFramework[alert.framework] = alert.mda_id;
    }
  }

  const currentStepData = trajectory?.steps.find(
    (s) => s.step_index === current_step,
  ) ?? null;

  // Loading skeleton: maintain DOM structure so framework-row testids are
  // always present — existing E2E tests can locate them immediately (IR-006).
  if (isLoading) {
    return (
      <div
        data-testid={dataTestId}
        data-current-step={current_step}
        data-loading="true"
        style={CONTAINER_STYLE}
      >
        {FRAMEWORK_ORDER.map((key) => {
          const color = FRAMEWORK_COLORS[key as keyof typeof FRAMEWORK_COLORS] ?? "#888";
          return (
            <div
              key={key}
              data-testid={`framework-row-${key}`}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                borderLeft: `3px solid ${color}`,
                paddingLeft: 6,
                paddingTop: 3,
                paddingBottom: 3,
                borderLeftStyle: "dashed",
                opacity: 0.35,
              }}
            >
              <span style={{ fontSize: 11, color: "#555", fontWeight: 500 }}>
                {FRAMEWORK_DISPLAY_LABELS[key] ?? key}
              </span>
              <span
                data-testid={`framework-score-${key}`}
                className="score-value--loading"
                style={{ fontSize: 13, fontWeight: 700, color: "#bbb", fontVariantNumeric: "tabular-nums" }}
              >
                …
              </span>
            </div>
          );
        })}
      </div>
    );
  }

  // Normal render — framework rows always present in DOM regardless of error
  // state (IR-006). Error indicator is inline above the rows so existing
  // testids remain discoverable. When isError=true, trajectory is null so
  // all scores render as "—" (same as pre-fetch state).
  return (
    <div
      data-testid={dataTestId}
      data-current-step={current_step}
      {...(isError ? { "data-error": "true" } : {})}
      style={CONTAINER_STYLE}
    >
      {isError && (
        <span
          data-testid="zone-1d-error"
          style={{ fontSize: 9, color: "#aaa", fontStyle: "italic", paddingBottom: 2 }}
        >
          Data unavailable
        </span>
      )}
      {FRAMEWORK_ORDER.map((key) => {
        const point = currentStepData?.frameworks[key] ?? null;
        const score = point?.composite_score ?? null;
        const scoreClass = getScoreClass(score);
        const displayLabel = FRAMEWORK_DISPLAY_LABELS[key] ?? key;
        const color = FRAMEWORK_COLORS[key as keyof typeof FRAMEWORK_COLORS] ?? "#888";
        const isNull = score === null;

        return (
          <div
            key={key}
            data-testid={`framework-row-${key}`}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              borderLeft: `3px solid ${color}`,
              paddingLeft: 6,
              paddingTop: 3,
              paddingBottom: 3,
              borderLeftStyle: isNull ? "dashed" : "solid",
              opacity: isNull ? 0.6 : 1,
            }}
          >
            <span style={{ display: "flex", flexDirection: "column", gap: 1 }}>
              <span
                data-testid={`framework-label-${key}`}
                style={{
                  fontSize: 11,
                  color: "#555",
                  fontWeight: 500,
                }}
              >
                {displayLabel}
                {key === "ecological" && (
                  <span
                    data-testid="ecological-boundary-note"
                    style={{ display: "block", fontSize: 9, color: "#888", fontWeight: 400 }}
                  >
                    1.0 = boundary
                  </span>
                )}
              </span>
              {/* "Primary dimension — see alerts →" navigation link (#745) */}
              {topAlertByFramework[key] && onSelectFrameworkAlert && (
                <button
                  data-testid={`see-alerts-${key}`}
                  onClick={() => onSelectFrameworkAlert(topAlertByFramework[key])}
                  style={{
                    background: "none",
                    border: "none",
                    padding: 0,
                    cursor: "pointer",
                    color: "#cc0000",
                    fontSize: 9,
                    textAlign: "left",
                    fontWeight: 600,
                    letterSpacing: 0.2,
                  }}
                >
                  Primary dimension — see alerts →
                </button>
              )}
            </span>

            <span
              data-testid={`framework-score-${key}`}
              className={scoreClass}
              style={{
                fontSize: 13,
                fontWeight: 700,
                color: isNull ? "#aaa" : color,
                fontVariantNumeric: "tabular-nums",
              }}
            >
              {formatScore(score)}
            </span>
          </div>
        );
      })}
    </div>
  );
}
