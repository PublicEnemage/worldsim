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
}

export function FourFrameworkZone1D({
  "data-testid": dataTestId = "zone-1d-four-framework",
}: FourFrameworkZone1DProps) {
  const { trajectory, current_step } = useScenarioStepStore();

  const currentStepData = trajectory?.steps.find(
    (s) => s.step_index === current_step,
  ) ?? null;

  return (
    <div
      data-testid={dataTestId}
      data-current-step={current_step}
      style={{
        padding: "6px 10px",
        boxSizing: "border-box",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-around",
      }}
    >
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
              // Dashed border treatment for null axes (DD-011 extension into Zone 1)
              borderLeftStyle: isNull ? "dashed" : "solid",
              opacity: isNull ? 0.6 : 1,
            }}
          >
            <span
              data-testid={`framework-label-${key}`}
              style={{
                fontSize: 11,
                color: "#555",
                fontWeight: 500,
              }}
            >
              {displayLabel}
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
