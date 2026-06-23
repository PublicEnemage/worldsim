/* eslint-disable react-refresh/only-export-components */
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
 * ADR-015 §Component 1: L0 basis annotations on each framework row.
 * ADR-015 §Component 3: Political Feasibility (programme_survival_probability) row.
 *
 * Implements: US-021, US-022, ADR-008 Decision 7, DD-011, ADR-015 Components 1+3
 */
import React from "react";
import { useScenarioStepStore } from "../store/scenarioStepStore";
import { FRAMEWORK_COLORS } from "../constants/frameworkColors";
import { sortAlerts } from "./MDAAlertPanelZone1B";

// ---------------------------------------------------------------------------
// ADR-015 §Component 1 — L0 annotation constants and helpers
// ---------------------------------------------------------------------------

/**
 * Static ecological breach-type mapping for the four M14 entities.
 * DA-G5-5: GRC/EGY → ceiling; JOR/ZMB → floor.
 * M15 schema-level fix will supersede this static mapping.
 */
const ECOLOGICAL_BREACH_TYPES: Record<string, { label: string; arrow: string }> = {
  GRC: { label: "approaching planetary ceiling — climate", arrow: "↑" },
  EGY: { label: "approaching planetary ceiling — climate", arrow: "↑" },
  JOR: { label: "approaching resource floor — freshwater", arrow: "↓" },
  ZMB: { label: "approaching resource floor — freshwater", arrow: "↓" },
};

/** Data quality info per framework from GET /entities/{id}/data-quality (DA-G5-1). */
export interface FrameworkDataQuality {
  source_institution: string | null;
  data_vintage: string | null;
  confidence_tier?: number | null;
}

/**
 * Build the L0 basis annotation string for a framework row.
 * Format: [T{N} · {source} · pre-cal] — always shows pre-cal in M14 (ia1_disclosure always set).
 * Null tier → [—] (ADR-015 §Silent Failure Mode Component 1).
 * Ecological framework uses the breach-type label from ECOLOGICAL_BREACH_TYPES.
 */
export function buildFrameworkAnnotation(
  fw: string,
  tier: number | null | undefined,
  sourceInstitution: string | null,
  entityId?: string | null,
): string {
  if (tier === null || tier === undefined) return "[—]";

  if (fw === "ecological") {
    const breachInfo = entityId ? (ECOLOGICAL_BREACH_TYPES[entityId] ?? null) : null;
    if (breachInfo) {
      return `[T${tier} · ${breachInfo.arrow} ${breachInfo.label} · pre-cal]`;
    }
    return `[T${tier} · pre-cal]`;
  }

  if (sourceInstitution) {
    return `[T${tier} · ${sourceInstitution} · pre-cal]`;
  }
  return `[T${tier} · pre-cal]`;
}

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

/**
 * Rider #271 — reversibility classification label.
 *
 * recovery_horizon_years === null → "Irreversible"
 * recovery_horizon_years === integer → "Recoverable (N yrs)"
 *
 * Exported for unit testing.
 */
export function formatReversibilityLabel(
  recovery_horizon_years: number | null | undefined,
): string {
  if (recovery_horizon_years == null) return "Irreversible";
  return `Recoverable (${recovery_horizon_years} yrs)`;
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
  /** Entity ISO codes — when two provided, shows entity context label (DEMO-062). */
  entityIds?: string[];
  /** ADR-015 §Component 1: data-quality per framework (DA-G5-1). */
  dataQuality?: Record<string, FrameworkDataQuality> | null;
  /** ADR-015 §Component 3: whether political economy module is enabled (DA-G5-3). */
  peEnabled?: boolean;
  /**
   * ADR-015 §Component 3: programme_survival_probability value as Decimal string.
   * undefined = not fetched / PE disabled (row absent).
   * null = PE enabled but computation returned null (show error row).
   * string = valid value (show percentage).
   */
  pspValue?: string | null;
  /** ADR-015 §Component 3: confidence tier of the PSP indicator. */
  pspTier?: number | null;
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
  entityIds,
  dataQuality,
  peEnabled,
  pspValue,
  pspTier,
}: FourFrameworkZone1DProps) {
  const { trajectory, current_step, mda_alerts, mode } = useScenarioStepStore();

  // Top alert per framework for the "see alerts →" navigation link (#745)
  const topAlertByFramework: Record<string, string> = {};
  // Rider #271 — reversibility classification: worst-severity alert per framework
  const reversibilityByFramework: Record<string, { recovery_horizon_years: number | null }> = {};
  for (const alert of sortAlerts(mda_alerts)) {
    if (!(alert.framework in topAlertByFramework)) {
      topAlertByFramework[alert.framework] = alert.mda_id;
    }
    if (!(alert.framework in reversibilityByFramework)) {
      reversibilityByFramework[alert.framework] = {
        recovery_horizon_years: alert.recovery_horizon_years,
      };
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

  // Primary entity ID for ecological breach type mapping (DA-G5-5).
  const primaryEntityId = trajectory?.entity_id ?? entityIds?.[0] ?? null;

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
      {/* Entity context label (DEMO-062) — shows which entities' composite is displayed */}
      {entityIds && entityIds.length >= 2 && (
        <span
          data-testid="zone-1d-primary-entity"
          style={{ fontSize: 9, color: "#888", paddingBottom: 2 }}
        >
          {entityIds[0]} · {entityIds[1]}
        </span>
      )}
      {FRAMEWORK_ORDER.map((key) => {
        const point = currentStepData?.frameworks[key] ?? null;
        const score = point?.composite_score ?? null;
        const scoreClass = getScoreClass(score);
        const displayLabel = FRAMEWORK_DISPLAY_LABELS[key] ?? key;
        const color = FRAMEWORK_COLORS[key as keyof typeof FRAMEWORK_COLORS] ?? "#888";
        const isNull = score === null;

        // ADR-015 §Component 1 — L0 annotation from trajectory confidence_tier + data-quality source
        const trajectoryTier = point?.confidence_tier ?? null;
        const dqFramework = dataQuality?.[key] ?? null;
        const annotationText = buildFrameworkAnnotation(
          key,
          trajectoryTier,
          dqFramework?.source_institution ?? null,
          primaryEntityId,
        );

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
              paddingTop: 2,
              paddingBottom: 2,
              borderLeftStyle: isNull ? "dashed" : "solid",
              opacity: isNull ? 0.6 : 1,
            }}
          >
            <span style={{ display: "flex", flexDirection: "column", gap: 0 }}>
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
              {/* ADR-015 §Component 1 — L0 basis annotation (always visible at zero interaction) */}
              <span
                data-testid={`framework-annotation-${key}`}
                style={{ fontSize: 8, color: "#aaa", lineHeight: 1.2 }}
              >
                {annotationText}
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
              {/* Rider #271 — reversibility classification badge.
                  Shown in Mode 3 when there's an active alert for this framework. */}
              {mode === "MODE_3" && reversibilityByFramework[key] && (
                <span
                  data-testid={`reversibility-${key}`}
                  style={{
                    fontSize: 9,
                    fontWeight: 600,
                    color: reversibilityByFramework[key].recovery_horizon_years == null
                      ? "#dc2626"
                      : "#059669",
                    letterSpacing: 0.2,
                  }}
                >
                  {formatReversibilityLabel(reversibilityByFramework[key].recovery_horizon_years)}
                </span>
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

      {/* ADR-015 §Component 3 — Political Feasibility row (programme_survival_probability).
          Visible only when PE module is enabled. Absent entirely when PE is disabled. */}
      {peEnabled && (
        <div
          data-testid="zone-1d-political-feasibility"
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            borderLeft: "3px solid #7c3aed",
            paddingLeft: 6,
            paddingTop: 2,
            paddingBottom: 2,
          }}
        >
          <span style={{ fontSize: 11, color: "#555", fontWeight: 500 }}>
            Political Feasibility
          </span>
          <span
            style={{
              fontSize: 12,
              fontWeight: 700,
              color: "#7c3aed",
              fontVariantNumeric: "tabular-nums",
            }}
          >
            {pspValue === undefined ? (
              "—"
            ) : pspValue === null ? (
              <span style={{ color: "#cc0000", fontSize: 10 }}>— [computation error]</span>
            ) : (
              `${(parseFloat(pspValue) * 100).toFixed(0)}% [T${pspTier ?? 3} · political economy module]`
            )}
          </span>
        </div>
      )}

      {/* ADR-015 §Component 3 — PSP Layer 3 self-interpreting sentence (#1075).
          Visible when PE enabled and PSP value is available. Fallback when null. */}
      {peEnabled && pspValue !== undefined && (
        <div
          data-testid="psp-layer3-sentence"
          style={{
            borderLeft: "3px solid #7c3aed",
            paddingLeft: 6,
            paddingTop: 2,
            paddingBottom: 2,
            fontSize: 10,
            color: "#555",
            lineHeight: 1.4,
          }}
        >
          {pspValue === null ? (
            "Programme survival probability unavailable — computation error."
          ) : (
            `Programme survival probability: ${(parseFloat(pspValue) * 100).toFixed(0)}%. This means the programme has a ${(parseFloat(pspValue) * 100).toFixed(0)}% chance of remaining on track through conditionality compliance.`
          )}
        </div>
      )}
    </div>
  );
}
