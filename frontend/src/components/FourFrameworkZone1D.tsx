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
import { type ScenarioComparisonConfig } from "./TrajectoryView";

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

// ---------------------------------------------------------------------------
// PSP severity classification (M16-G2 #987, #1163)
// ---------------------------------------------------------------------------

export type PspSeverity = "CRITICAL" | "WARNING" | "WATCH" | "STABLE";

/** Classify PSP value into severity tier per CM-calibrated thresholds (2026-06-23). */
export function getPspSeverity(pspValue: string): PspSeverity {
  const v = parseFloat(pspValue);
  if (v < 0.40) return "CRITICAL";
  if (v < 0.55) return "WARNING";
  if (v < 0.70) return "WATCH";
  return "STABLE";
}

const PSP_SEVERITY_COLOR: Record<PspSeverity, string> = {
  CRITICAL: "#cc0000",
  WARNING: "#a06000",
  WATCH: "#0070a0",
  STABLE: "#059669",
};

/** Historical analogue sentence per PSP severity (CM sign-off 2026-06-23; updated #1253 2026-06-25). */
function getPspHistoricalAnalogue(severity: PspSeverity): string | null {
  if (severity === "CRITICAL")
    return "Comparable: Zambia 2015 ECF — abandoned Step 3 (PSP 38%). Board review failed.";
  if (severity === "WARNING")
    return "Comparable: Ghana 2014 ECF — modified Step 5 (PSP 52%). Conditionality relaxed.";
  if (severity === "WATCH")
    return "At this PSP level, ECF programmes show elevated discontinuation risk (approx. 35%).";
  return null;
}

// ---------------------------------------------------------------------------
// Legitimacy floor proximity label
// ---------------------------------------------------------------------------

function getFloorProximityLabel(value: string, floor: string): string {
  const v = parseFloat(value);
  const f = parseFloat(floor);
  const diff = Math.abs(v - f);
  if (Math.abs(v - f) < 0.001) return "AT fragility threshold";
  if (v > f) return `${diff.toFixed(2)} above fragility threshold`;
  return `${diff.toFixed(2)} below fragility threshold`;
}

// ---------------------------------------------------------------------------
// Props
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
  /** Whether political economy module is enabled (DA-G5-3). */
  peEnabled?: boolean;
  /**
   * M16-G2 (#987): programme_survival_probability value as Decimal string.
   * undefined = not fetched / PE disabled (section absent).
   * null = PE enabled but computation returned null.
   * string = valid value.
   */
  pspValue?: string | null;
  /** Confidence tier of the PSP indicator. */
  pspTier?: number | null;
  /** M16-G2 (#987): legitimacy_index value as Decimal string (null = unavailable). */
  legitimacyValue?: string | null;
  /** M16-G2 (#987): legitimacy_index floor value as Decimal string. */
  legitimacyFloor?: string | null;
  /** M16-G2 (#987): legitimacy_index direction ("declining" | "stable" | "improving"). */
  legitimacyDirection?: string | null;
  /** M16-G2 (#987): elite_capture_divergence direction ("widening" | "stable" | "narrowing"). */
  eliteCaptureDirection?: string | null;
  /** M16-G2 (#987): elite_capture_divergence qualifier text (e.g. "fiscal benefits concentrating"). */
  eliteCaptureQualifier?: string | null;
  /** M17-G2 — loaded comparison scenario configs with PSP values for Zone 1D rows. */
  comparisonScenarios?: ScenarioComparisonConfig[];
  /** M18-G2 (#1255): dominant driver of PSP change at current step. null = no driver row rendered. */
  pspDominantDriver?: string | null;
}

const DRIVER_LABELS: Record<string, string> = {
  fiscal_sustainability: "fiscal sustainability",
  external_balance: "external balance",
  governance: "governance",
  social_stability: "social stability",
};

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
  pspTier: _pspTier,
  legitimacyValue,
  legitimacyFloor,
  legitimacyDirection,
  eliteCaptureDirection,
  eliteCaptureQualifier,
  comparisonScenarios = [],
  pspDominantDriver,
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

      {/* #1276 — Governance horizon disclosure (No False Precision; Placement A — always visible). */}
      <div
        data-testid="governance-horizon-disclosure"
        style={{
          fontSize: 8,
          color: "#888",
          lineHeight: 1.4,
          paddingTop: 3,
          paddingLeft: 9,
          fontStyle: "italic",
        }}
      >
        Governance indicators (rule of law, democratic quality) respond to fiscal adjustment over
        3–6 year horizons in this model&apos;s calibration. An 8-step quarterly window captures the
        beginning of the governance stress trajectory; full divergence requires a 12–24 step analysis.
      </div>

      {/* M16-G2 #987 — Political Risk sub-section (replaces G1 political economy elements).
          Visible when PE enabled; shows structured severity-labeled summary for Persona 3.
          Empty state shown when PE is disabled. G1 testids fully retired (DD-016). */}
      {peEnabled ? (
        pspValue !== undefined ? (
          <div data-testid="zone-1d-political-risk">
            {/* Section divider + header */}
            <div
              style={{
                borderTop: "1px solid #e0e0e0",
                paddingTop: 4,
                marginTop: 2,
              }}
            >
              <span
                data-testid="zone-1d-political-risk-header"
                style={{ fontSize: 9, fontWeight: 600, color: "#555", letterSpacing: 0.3 }}
              >
                POLITICAL RISK
              </span>
            </div>

            {/* Scenario comparison PSP rows (M17-G2) */}
            {comparisonScenarios.length > 0 && (
              <div style={{ marginTop: 2 }}>
                {comparisonScenarios.map((sc) => {
                  const slug = sc.scenarioId.replace(/^[a-z]{3}-/, "");
                  const pspNum = sc.pspValue != null ? parseFloat(sc.pspValue) : null;
                  const pspPct = pspNum !== null ? Math.round(pspNum * 100) : null;
                  return (
                    <div
                      key={sc.scenarioId}
                      data-testid={`zone1d-psp-row-scenario-${slug}`}
                      style={{ fontSize: 10, color: "#333", paddingTop: 1 }}
                    >
                      {`Option ${sc.label}: `}
                      <span data-testid={`zone1d-psp-value-${slug}`}>
                        {pspPct !== null ? `${pspPct}%` : "—"}
                      </span>
                    </div>
                  );
                })}
              </div>
            )}

            {/* PSP severity row */}
            {pspValue !== null ? (() => {
              const severity = getPspSeverity(pspValue);
              const pspPct = Math.round(parseFloat(pspValue) * 100);
              const severityColor = PSP_SEVERITY_COLOR[severity];
              const analogue = getPspHistoricalAnalogue(severity);
              return (
                <>
                  <div
                    data-testid="psp-severity-row"
                    style={{ paddingTop: 2, fontSize: 11, color: "#333" }}
                  >
                    {"Programme survival: "}
                    <span
                      data-testid="psp-severity-badge"
                      style={{ fontWeight: 700, color: severityColor }}
                    >
                      {severity}
                    </span>
                    {` (${pspPct}%) — `}
                    <span style={{ color: "#555" }}>
                      {legitimacyDirection === "declining" || eliteCaptureDirection === "widening"
                        ? "DECLINING"
                        : "STABLE"}
                    </span>
                  </div>
                  {pspDominantDriver != null && DRIVER_LABELS[pspDominantDriver] && (
                    <div
                      data-testid="psp-driver-row"
                      style={{ paddingTop: 1, fontSize: 10, color: "#555" }}
                    >
                      {`Driver: ${DRIVER_LABELS[pspDominantDriver]}`}
                    </div>
                  )}
                  {analogue && (
                    <div
                      data-testid="psp-historical-analogue"
                      style={{ paddingTop: 1, paddingBottom: 1, fontSize: 10, color: "#555", lineHeight: 1.3 }}
                    >
                      {analogue}
                    </div>
                  )}
                </>
              );
            })() : (
              <div
                data-testid="psp-severity-row"
                style={{ paddingTop: 2, fontSize: 10, color: "#aaa", fontStyle: "italic" }}
              >
                Programme survival: unavailable
              </div>
            )}

            {/* Legitimacy index row */}
            {legitimacyValue != null && (
              <>
                <div
                  data-testid="legitimacy-index-row"
                  style={{ paddingTop: 1, fontSize: 10, color: "#333" }}
                >
                  {`Legitimacy index: ${parseFloat(legitimacyValue).toFixed(2)} — `}
                  <span style={{ color: "#555" }}>{legitimacyDirection ?? "unknown"}</span>
                  {legitimacyFloor != null && (
                    <span style={{ color: "#888" }}>{` (floor: ${parseFloat(legitimacyFloor).toFixed(2)})`}</span>
                  )}
                </div>
                {legitimacyFloor != null && (
                  <div
                    data-testid="legitimacy-floor-proximity"
                    style={{ fontSize: 9, color: "#777", paddingBottom: 1 }}
                  >
                    {getFloorProximityLabel(legitimacyValue, legitimacyFloor)}
                  </div>
                )}
              </>
            )}

            {/* Elite capture row */}
            {eliteCaptureDirection != null && (
              <div
                data-testid="elite-capture-row"
                style={{
                  paddingTop: 1,
                  paddingBottom: 1,
                  fontSize: 10,
                  color: "#333",
                  whiteSpace: "nowrap",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                }}
              >
                {`Elite capture divergence: ${eliteCaptureDirection}`}
                {eliteCaptureQualifier != null && ` — ${eliteCaptureQualifier}`}
              </div>
            )}
          </div>
        ) : null
      ) : (
        <div
          data-testid="political-risk-empty"
          style={{ paddingTop: 4, fontSize: 10, color: "#aaa", fontStyle: "italic" }}
        >
          Political risk: not modelled in this fixture.
        </div>
      )}
    </div>
  );
}
