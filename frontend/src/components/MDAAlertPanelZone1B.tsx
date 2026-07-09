/* eslint-disable react-refresh/only-export-components */
/**
 * MDAAlertPanelZone1B — Zone 1B co-primary instrument.
 *
 * ADR-014: Persistent-detail + scan-only compact list layout.
 *
 * Layout:
 *   Zone 1B-detail (top, fixed height): always shows the highest-ranked alert's
 *     full evidence without any user interaction. Zero interactions to read.
 *   Zone 1B-compact (bottom, flex-fill): scrollable scan surface for remaining
 *     alerts. Rows are informational only — no click handler, cursor:default.
 *
 * Ranking rule (4-level, §5.3 of m13-g7-sprint-entry.md):
 *   L1: severity DESC (TERMINAL=0, CRITICAL=1, WARNING=2)
 *   L2: step_index ASC (earliest breach first — longest consecutive count)
 *   L3: confidence_tier ASC (lower = more defensible; ranks first)
 *   L4: stable insertion-order (entity population unavailable in API response)
 *
 * AlertDetailPanel is exported for future EntityDetailDrawer use (ADR-014).
 */
import { useEffect, useRef, useState } from "react";
import {
  useScenarioStepStore,
  type Zone1BAlert,
  type CohortThresholdCrossing,
  type DistributionalSummaryData,
} from "../store/scenarioStepStore";
import { getIndicatorDisplayNameAny, getIndicatorAbbreviation } from "../lib/indicatorDisplayNames";
import { useViewportBreakpoint } from "./InstrumentCluster";
import { type ScenarioComparisonConfig, SCENARIO_COMPARISON_PALETTE } from "./TrajectoryView";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

export const SEVERITY_ORDER: Record<Zone1BAlert["severity"], number> = {
  TERMINAL: 0,
  CRITICAL: 1,
  WARNING: 2,
};

export const SEVERITY_ABBREV: Record<Zone1BAlert["severity"], string> = {
  TERMINAL: "TERM",
  CRITICAL: "CRIT",
  WARNING: "WARN",
};

export const SEVERITY_COLOR: Record<Zone1BAlert["severity"], string> = {
  TERMINAL: "#7f0000",
  CRITICAL: "#cc0000",
  WARNING: "#a06000",
};

export const SEVERITY_BG: Record<Zone1BAlert["severity"], string> = {
  TERMINAL: "#fff0f0",
  CRITICAL: "#fff5f5",
  WARNING: "#fffbe6",
};

export const FRAMEWORK_ABBREV: Record<string, string> = {
  financial: "FIN",
  human_development: "HDI",
  ecological: "ECO",
  governance: "GOV",
};

// ---------------------------------------------------------------------------
// Exported pure functions (tested by unit tests)
// ---------------------------------------------------------------------------

/**
 * Sort alerts by 4-level ranking rule (ADR-014 §5.3, sprint entry §5.3).
 * L1: severity DESC  L2: step_index ASC  L3: confidence_tier ASC  L4: stable order
 */
export function sortAlerts(alerts: Zone1BAlert[]): Zone1BAlert[] {
  return [...alerts].sort((a, b) => {
    const severityDiff = SEVERITY_ORDER[a.severity] - SEVERITY_ORDER[b.severity];
    if (severityDiff !== 0) return severityDiff;
    const stepDiff = a.step_index - b.step_index;
    if (stepDiff !== 0) return stepDiff;
    const tierDiff = a.confidence_tier - b.confidence_tier;
    if (tierDiff !== 0) return tierDiff;
    return 0; // stable insertion-order (L4 population tiebreak — population not in API payload)
  });
}

/**
 * Returns the negotiation-defensibility label for a confidence tier.
 * Displayed in Zone 1B-detail. Confidence tier is per-step, not cumulative.
 */
export function getNegotiationLabel(tier: number): string {
  if (tier <= 2) return "High confidence — cite directly";
  if (tier === 3) return "Moderate confidence — cite with caveat";
  if (tier === 4) return "Model estimate — verify before citing";
  return "Synthetic extrapolation — do not cite";
}

/**
 * Mode-dependent status text for the detail slot (UX sign-off condition 2).
 * Per information-hierarchy.md §1B ("Alert tense is mode-dependent").
 *
 * Mode 1 (historical): "crossed threshold at step N" / "N% above floor at step N"
 * Mode 2 (projected):  "BREACH PROJECTED at step N" / "N% above floor (projected)"
 * Mode 3 (real-time):  "BREACHED" / "N% above floor"
 */
export function getDetailStatusText(
  alert: Zone1BAlert,
  mode: "MODE_1" | "MODE_2" | "MODE_3",
): string {
  const approachPct = parseFloat(alert.approach_pct_remaining);
  const isBreached = approachPct <= 0;

  if (mode === "MODE_1") {
    if (isBreached) return `crossed threshold at step ${alert.step_index}`;
    const pct = (approachPct * 100).toFixed(1);
    return `${pct}% above floor at step ${alert.step_index}`;
  }

  if (mode === "MODE_2") {
    if (isBreached) return `BREACH PROJECTED at step ${alert.step_index}`;
    const pct = (approachPct * 100).toFixed(1);
    return `${pct}% above floor (projected)`;
  }

  // MODE_3 — real-time
  if (isBreached) return "BREACHED";
  const pct = (approachPct * 100).toFixed(1);
  return `${pct}% above floor`;
}

/**
 * Format the alert tense text per mode (retained for compact row display, US-016).
 */
export function formatAlertText(
  alert: Zone1BAlert,
  mode: "MODE_1" | "MODE_2" | "MODE_3",
): string {
  const indicator = alert.indicator_key.replace(/_/g, " ");
  const cohort = alert.cohort ?? "all cohorts";

  if (mode === "MODE_1") {
    return `${indicator} crossed ${alert.severity} threshold at step ${alert.step_index}.`;
  }
  if (mode === "MODE_2") {
    return `${indicator} is projected to cross ${alert.severity} threshold at step ${alert.step_index}.`;
  }
  return `${alert.severity} — ${indicator} — ${cohort} — step ${alert.step_index}`;
}

/**
 * Build the Zone 1B Layer 3 directive sentence for the top alert (#1065, ADR-015 §Component 4).
 *
 * When consecutive_breach_steps is null (computation unavailable), renders a transparent
 * fallback disclosure rather than an absent element (AC-10 silent-failure rule).
 */
export function buildTrajectoryLayerSentence(alert: Zone1BAlert): string {
  const cbs = alert.consecutive_breach_steps;

  if (cbs === null || cbs === undefined) {
    return "Trajectory analysis unavailable for this alert.";
  }

  const displayName = getIndicatorDisplayNameAny(alert.indicator_key);
  const currentNum = parseFloat(String(alert.current_value));
  const floorNum = parseFloat(String(alert.floor_value));

  if (!isNaN(currentNum) && !isNaN(floorNum)) {
    const diff = Math.abs(currentNum - floorNum).toFixed(2);
    if (currentNum < floorNum) {
      return `${displayName} has fallen ${diff} below the ${alert.severity} threshold. Breach active for ${cbs} consecutive step${cbs !== 1 ? "s" : ""}.`;
    }
    const pctAbove = (((currentNum - floorNum) / floorNum) * 100).toFixed(1);
    return `${displayName} is approaching the ${alert.severity} threshold (${pctAbove}% above floor). Breach streak: ${cbs} consecutive step${cbs !== 1 ? "s" : ""}.`;
  }

  return `${displayName}: ${alert.severity} threshold breach active for ${cbs} consecutive step${cbs !== 1 ? "s" : ""}.`;
}

/**
 * Truncate indicator display name to ≤ maxChars, appending "…" if truncated.
 */
export function truncateIndicatorName(name: string, maxChars = 22): string {
  if (name.length <= maxChars) return name;
  return name.slice(0, maxChars - 1) + "…";
}

/**
 * Build SVG polyline points for a composite score sparkline.
 * Returns null if fewer than 2 data points with non-null scores.
 * Used by AlertDetailPanel (exported for EntityDetailDrawer use).
 */
export function buildSparklinePoints(
  scores: (number | null)[],
  width: number,
  height: number,
  padding = 4,
): string | null {
  const finite = scores.filter((s) => s !== null) as number[];
  if (finite.length < 2) return null;

  const usableW = width - padding * 2;
  const usableH = height - padding * 2;
  const maxV = Math.max(...finite, 0.01);

  const points = scores
    .map((s, i) => {
      if (s === null) return null;
      const x = padding + (i / (scores.length - 1)) * usableW;
      const y = padding + (1 - s / maxV) * usableH;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .filter(Boolean);

  return points.length >= 2 ? points.join(" ") : null;
}

// ---------------------------------------------------------------------------
// AlertDetailPanel — exported for EntityDetailDrawer use (ADR-014)
// No longer rendered by MDAAlertPanelZone1B itself.
// ---------------------------------------------------------------------------

/**
 * Convert a raw source registry ID (e.g. "ECOWAS_REGIONAL_2023") to a
 * human-readable label ("Ecowas Regional 2023") for display in Zone 1B.
 * Numeric parts (year) are preserved unchanged; word parts are title-cased.
 */
export function formatSourceId(id: string | null | undefined): string {
  if (!id) return "—";
  return id
    .split("_")
    .map(part => /^\d+$/.test(part) ? part : part.charAt(0).toUpperCase() + part.slice(1).toLowerCase())
    .join(" ");
}

/**
 * Format the floor-distance label for a cohort threshold crossing entry.
 * Direction is determined by breaches_below (set by the backend based on
 * comparison_operator): gte thresholds breach when value falls BELOW the floor;
 * lte thresholds (future) breach when value rises ABOVE the floor.
 */
export function formatCohortDistance(
  pct: string | null,
  breachesBelow: boolean,
  isSad: boolean,
): string {
  if (isSad || pct == null) return "—";
  return breachesBelow ? `${pct}% below floor` : `${pct}% above floor`;
}

// ---------------------------------------------------------------------------

interface AlertDetailPanelProps {
  alert: Zone1BAlert;
  onClose: () => void;
}

export function AlertDetailPanel({ alert, onClose }: AlertDetailPanelProps) {
  const { trajectory } = useScenarioStepStore();
  const color = SEVERITY_COLOR[alert.severity];
  const panelRef = useRef<HTMLDivElement>(null);

  // Scroll into view on mount — retained for EntityDetailDrawer use.
  useEffect(() => {
    panelRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, []);

  const displayName = getIndicatorDisplayNameAny(alert.indicator_key);

  const scores: (number | null)[] = trajectory
    ? trajectory.steps.map((s) => s.frameworks[alert.framework]?.composite_score ?? null)
    : [];

  const mda_floor = trajectory?.mda_floors.find((f) => f.framework === alert.framework);

  const W = 200;
  const H = 56;
  const PADDING = 4;

  const polylinePoints = buildSparklinePoints(scores, W, H, PADDING);

  const floorY = (() => {
    if (!mda_floor || scores.length === 0) return null;
    const finite = scores.filter((s) => s !== null) as number[];
    if (finite.length === 0) return null;
    const maxV = Math.max(...finite, 0.01);
    return PADDING + (1 - mda_floor.floor_value / maxV) * (H - PADDING * 2);
  })();

  const crossingX = (() => {
    if (!trajectory || scores.length < 2) return null;
    const idx = trajectory.steps.findIndex((s) => s.step_index === alert.step_index);
    if (idx < 0) return null;
    return PADDING + (idx / (scores.length - 1)) * (W - PADDING * 2);
  })();

  const approachPct = parseFloat(alert.approach_pct_remaining);
  const isBreached = approachPct <= 0;

  return (
    <div
      ref={panelRef}
      data-testid="alert-detail-panel"
      data-alert-id={alert.mda_id}
      style={{
        background: "#fff",
        border: `1px solid ${color}`,
        borderRadius: 4,
        padding: "8px 10px",
        fontSize: 11,
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 6 }}>
        <div>
          <span
            data-testid="detail-indicator-name"
            style={{ fontWeight: 700, color: "#1a1a2e", fontSize: 12 }}
          >
            {displayName}
          </span>
          <span
            style={{
              marginLeft: 6,
              background: color,
              color: "#fff",
              borderRadius: 3,
              padding: "1px 5px",
              fontSize: 10,
              fontWeight: 700,
            }}
          >
            {alert.severity}
          </span>
          <span style={{ marginLeft: 5, color: "#666", fontSize: 10 }}>
            {FRAMEWORK_ABBREV[alert.framework] ?? alert.framework} · Step {alert.step_index}
          </span>
        </div>
        <button
          data-testid="detail-close-btn"
          onClick={onClose}
          style={{
            background: "none",
            border: "none",
            cursor: "pointer",
            color: "#aaa",
            fontSize: 14,
            lineHeight: 1,
            padding: "0 2px",
          }}
          aria-label="Close detail"
        >
          ✕
        </button>
      </div>

      {polylinePoints && (
        <div data-testid="detail-sparkline" style={{ marginBottom: 6 }}>
          <svg
            width={W}
            height={H}
            style={{ display: "block", overflow: "visible" }}
            aria-label={`${FRAMEWORK_ABBREV[alert.framework] ?? alert.framework} composite score trajectory`}
          >
            {floorY !== null && (
              <line
                data-testid="detail-floor-line"
                x1={PADDING}
                y1={floorY}
                x2={W - PADDING}
                y2={floorY}
                stroke={color}
                strokeWidth={1}
                strokeDasharray="3 2"
                opacity={0.8}
              />
            )}
            <polyline
              points={polylinePoints}
              fill="none"
              stroke="#2171b5"
              strokeWidth={1.5}
              strokeLinejoin="round"
            />
            {crossingX !== null && floorY !== null && (
              <circle
                data-testid="detail-crossing-marker"
                cx={crossingX}
                cy={floorY}
                r={3}
                fill={color}
              />
            )}
          </svg>
          <div style={{ color: "#888", fontSize: 9, marginTop: 1 }}>
            Framework score · dashed = threshold
          </div>
        </div>
      )}

      <div
        data-testid="detail-snapshot"
        style={{ display: "grid", gridTemplateColumns: "1fr 1fr", columnGap: 8, rowGap: 2 }}
      >
        <div>
          <span style={{ color: "#888" }}>Current </span>
          <span data-testid="detail-current-value" style={{ fontWeight: 700, color: isBreached ? color : "#333" }}>
            {parseFloat(alert.current_value).toFixed(3)}
          </span>
        </div>
        <div>
          <span style={{ color: "#888" }}>Floor </span>
          <span data-testid="detail-floor-value" style={{ fontWeight: 700, color: "#555" }}>
            {parseFloat(alert.floor_value).toFixed(3)}
          </span>
        </div>
        <div>
          <span style={{ color: "#888" }}>Approach </span>
          <span
            data-testid="detail-approach-pct"
            style={{ fontWeight: 700, color: isBreached ? color : "#333" }}
          >
            {isBreached ? "BREACHED" : `${(approachPct * 100).toFixed(1)}% remaining`}
          </span>
        </div>
        <div>
          <span style={{ color: "#888" }}>Consecutive </span>
          <span data-testid="detail-consecutive" style={{ fontWeight: 700, color: "#555" }}>
            {alert.consecutive_breach_steps ?? "—"} step{alert.consecutive_breach_steps !== 1 ? "s" : ""}
          </span>
        </div>
      </div>

      {alert.causal_attribution && (
        <div
          data-testid="detail-causal-attribution"
          style={{ marginTop: 5, color: "#555", fontStyle: "italic" }}
        >
          Caused by: {alert.causal_attribution}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// TopAlertDetail — Zone 1B-detail sub-zone (no sparkline; zero interactions)
// ---------------------------------------------------------------------------

interface TopAlertDetailProps {
  alert: Zone1BAlert;
  mode: "MODE_1" | "MODE_2" | "MODE_3";
  showNewBadge: boolean;
}

function TopAlertDetail({ alert, mode, showNewBadge }: TopAlertDetailProps) {
  const color = SEVERITY_COLOR[alert.severity];
  const fwAbbrev = FRAMEWORK_ABBREV[alert.framework] ?? alert.framework.toUpperCase().slice(0, 3);
  const approachPct = parseFloat(alert.approach_pct_remaining);
  const isBreached = approachPct <= 0;
  const displayName = getIndicatorDisplayNameAny(alert.indicator_key);
  const statusText = getDetailStatusText(alert, mode);

  return (
    <div
      data-testid="zone-1b-top-detail"
      data-severity={alert.severity}
      data-alert-id={alert.mda_id}
      style={{
        flex: "0 0 auto",
        overflow: "hidden",
        background: SEVERITY_BG[alert.severity],
        borderLeft: `3px solid ${color}`,
        borderBottom: "1px solid #e8e8e8",
        padding: "6px 8px",
        fontSize: 11,
        boxSizing: "border-box",
      }}
    >
      {/* Header: severity pill + indicator + framework + step + entity + [NEW] badge */}
      <div style={{ display: "flex", alignItems: "center", gap: 4, flexWrap: "nowrap", marginBottom: 2 }}>
        <span
          style={{
            background: color,
            color: "#fff",
            borderRadius: 3,
            padding: "1px 5px",
            fontSize: 10,
            fontWeight: 700,
            flexShrink: 0,
          }}
        >
          {alert.severity}
        </span>
        <span
          data-testid="detail-indicator-name"
          style={{ fontWeight: 600, color: "#1a1a2e", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}
        >
          {displayName}
        </span>
        <span style={{ color: "#666", flexShrink: 0 }}>{fwAbbrev}</span>
        <span
          data-testid="detail-entity-id"
          style={{ color: "#555", fontWeight: 600, flexShrink: 0 }}
        >
          {alert.entity_id}
        </span>
        {showNewBadge && (
          <span
            data-testid="detail-new-badge"
            style={{
              background: "#2171b5",
              color: "#fff",
              borderRadius: 3,
              padding: "1px 4px",
              fontSize: 9,
              fontWeight: 700,
              flexShrink: 0,
            }}
          >
            NEW
          </span>
        )}
      </div>

      {/* Step line */}
      <div style={{ color: "#555", marginBottom: 2 }}>
        Step {alert.step_index}
        {alert.cohort && alert.cohort !== "all cohorts" && (
          <span style={{ marginLeft: 6, color: "#777" }}>{alert.cohort}</span>
        )}
      </div>

      {/* Values row */}
      <div style={{ display: "flex", gap: 12, marginBottom: 2 }}>
        <span>
          <span style={{ color: "#888" }}>Current </span>
          <span
            data-testid="detail-current-value"
            style={{ fontWeight: 700, color: isBreached ? color : "#333" }}
          >
            {parseFloat(alert.current_value).toFixed(3)}
          </span>
        </span>
        <span>
          <span style={{ color: "#888" }}>Floor </span>
          <span
            data-testid="detail-floor-value"
            style={{ fontWeight: 700, color: "#555" }}
          >
            {parseFloat(alert.floor_value).toFixed(3)}
          </span>
        </span>
      </div>

      {/* Status + consecutive steps (zero suppressed — #1066) */}
      <div style={{ display: "flex", gap: 8, marginBottom: 2 }}>
        <span
          data-testid="detail-status"
          style={{ fontWeight: 700, color: isBreached ? color : "#555" }}
        >
          {statusText}
        </span>
        {alert.consecutive_breach_steps !== null &&
         alert.consecutive_breach_steps !== undefined &&
         alert.consecutive_breach_steps > 0 && (
          <>
            <span style={{ color: "#888" }}>·</span>
            <span
              data-testid="detail-consecutive"
              style={{ fontWeight: 700, color: "#555" }}
            >
              {alert.consecutive_breach_steps} consecutive step{alert.consecutive_breach_steps !== 1 ? "s" : ""}
            </span>
          </>
        )}
      </div>

      {/* Negotiation-defensibility label (always shown in detail slot) */}
      <div
        data-testid="alert-negotiation-label"
        style={{
          color: alert.confidence_tier >= 4 ? "#a06000" : "#555",
          fontSize: 10,
        }}
      >
        {getNegotiationLabel(alert.confidence_tier)}
      </div>

      {/* Layer 3 directive sentence (#1065, ADR-015 §Component 4) — always rendered when
          top alert is present; shows fallback text when trajectory computation unavailable. */}
      <div
        data-testid="zone-1b-trajectory-sentence"
        style={{
          marginTop: 4,
          fontSize: 10,
          color: "#444",
          lineHeight: 1.4,
          borderTop: "1px solid rgba(0,0,0,0.06)",
          paddingTop: 3,
        }}
      >
        {buildTrajectoryLayerSentence(alert)}
      </div>

      {/* Causal attribution — Mode 3 only */}
      {mode === "MODE_3" && alert.causal_attribution && (
        <div
          data-testid="detail-causal-attribution"
          style={{ marginTop: 3, color: "#555", fontStyle: "italic", fontSize: 10 }}
        >
          Caused by: {alert.causal_attribution}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// CompactAlertList — Zone 1B-compact sub-zone (scan-only; no click targets)
// ---------------------------------------------------------------------------

interface CompactAlertListProps {
  alerts: Zone1BAlert[]; // all except top-ranked; already sorted
  onClearNewBadge: () => void;
}

function CompactAlertList({ alerts, onClearNewBadge }: CompactAlertListProps) {
  if (alerts.length === 0) {
    return (
      <div
        data-testid="zone-1b-compact"
        style={{ flex: "1 1 auto", overflowY: "auto", padding: "4px 8px" }}
        onScroll={onClearNewBadge}
      >
        <div style={{ color: "#ccc", fontSize: 10, fontStyle: "italic" }}>No other active alerts.</div>
      </div>
    );
  }

  // Row height is fixed at 24px max (≤ 26px per UX sign-off condition 1)
  // "+N more ↕" is rendered as a muted row when the list overflows
  return (
    <div
      data-testid="zone-1b-compact"
      style={{ flex: "1 1 auto", overflowY: "auto", padding: "2px 4px" }}
      onScroll={onClearNewBadge}
      onClick={onClearNewBadge}
    >
      {alerts.map((alert) => {
        const color = SEVERITY_COLOR[alert.severity];
        const sevAbbrev = SEVERITY_ABBREV[alert.severity];
        const fwAbbrev = FRAMEWORK_ABBREV[alert.framework] ?? alert.framework.toUpperCase().slice(0, 3);
        const indicatorDisplay = getIndicatorAbbreviation(alert.indicator_key, 24);

        return (
          <div
            key={`${alert.mda_id}-${alert.step_index}`}
            data-testid="compact-alert-row"
            data-severity={alert.severity}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 4,
              height: 24,
              maxHeight: 26,
              overflow: "hidden",
              whiteSpace: "nowrap",
              cursor: "default",
              padding: "0 4px",
              borderLeft: `2px solid ${color}`,
              marginBottom: 2,
              fontSize: 10,
            }}
          >
            <span style={{ color, fontWeight: 700, flexShrink: 0 }}>{sevAbbrev}</span>
            <span
              data-testid="compact-row-entity-id"
              style={{ color: "#555", fontWeight: 600, flexShrink: 0 }}
            >
              {alert.entity_id}
            </span>
            <span style={{ color: "#666", flexShrink: 0 }}>{fwAbbrev}</span>
            <span style={{ color: "#333", overflow: "hidden", textOverflow: "ellipsis" }}>
              {indicatorDisplay}
            </span>
            <span style={{ color: "#999", flexShrink: 0, marginLeft: "auto" }}>
              Stp {alert.step_index}
            </span>
          </div>
        );
      })}
    </div>
  );
}

// ---------------------------------------------------------------------------
// M18-G3 #1349 — DistributionalComparisonSummary — sticky-bottom Zone 1B element
// ---------------------------------------------------------------------------

function _formatHeadcount(n: number): string {
  const abs = Math.abs(n);
  const sign = n >= 0 ? "+" : "−";
  return `${sign}${abs.toLocaleString("en-US")} persons`;
}

function _formatK(n: number): string {
  if (Math.abs(n) >= 1_000) return `${Math.round(n / 1_000).toLocaleString("en-US")}K`;
  return n.toLocaleString("en-US");
}

export function DistributionalComparisonSummary({ summary }: { summary: DistributionalSummaryData }) {
  const [panelOpen, setPanelOpen] = useState(false);
  const methodologyPanelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (panelOpen && methodologyPanelRef.current) {
      methodologyPanelRef.current.scrollIntoView({ block: "nearest" });
    }
  }, [panelOpen]);

  const terminalPairs = summary.pairs.map((pair) => {
    const terminal = pair.steps.find((s) => s.step === summary.terminal_step) ?? pair.steps[pair.steps.length - 1];
    return { ...pair, terminal };
  }).filter((p) => p.terminal !== undefined);

  const totalSteps = Math.max(...summary.pairs.flatMap((p) => p.steps.map((s) => s.step)));
  const allDirectionStable = terminalPairs.every((p) => p.terminal?.direction_stable ?? false);
  const refLabel = summary.reference_scenario_label;

  const rowStyle: React.CSSProperties = { fontSize: 11, color: "#4b5563", marginBottom: 2, lineHeight: 1.4 };
  const labelStyle: React.CSSProperties = { fontWeight: 500 };

  return (
    <div
      data-testid="distributional-comparison-summary"
      style={{
        position: "sticky",
        bottom: 0,
        borderTop: "1px solid #e5e7eb",
        padding: "6px 8px",
        background: "#fff",
        zIndex: 1,
        minHeight: 160,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 4, marginBottom: 2 }}>
        <span style={{ fontSize: 11, color: "#6b7280", textTransform: "uppercase", letterSpacing: 0.5, fontWeight: 600 }}>
          DISTRIBUTIONAL COMPARISON
        </span>
        <span style={{ fontSize: 10, color: "#9ca3af" }}>step {totalSteps}</span>
        <span
          data-testid="comparison-tier-badge"
          style={{
            marginLeft: "auto",
            fontSize: 9,
            background: "#f3f4f6",
            color: "#6b7280",
            borderRadius: 3,
            padding: "1px 4px",
          }}
        >
          {summary.tier}
        </span>
        <button
          data-testid="methodology-panel-toggle"
          onClick={() => setPanelOpen((v) => !v)}
          aria-expanded={panelOpen}
          style={{
            fontSize: 10,
            color: "#6b7280",
            cursor: "pointer",
            background: "none",
            border: "none",
            padding: "0 2px",
          }}
        >
          {panelOpen ? "▼ Methodology" : "▶ Methodology"}
        </button>
      </div>
      <div style={{ fontSize: 11, color: "#4b5563", fontStyle: "italic", marginBottom: 4 }}>
        Poverty headcount differential
      </div>
      {terminalPairs.map((pair) => {
        const hc = pair.terminal!.headcount_differential;
        const ciLow = pair.terminal!.ci_lower;
        const ciHigh = pair.terminal!.ci_upper;
        return (
          <div
            key={pair.scenario_id}
            data-testid={`comparison-pair-${pair.scenario_id}-vs-${summary.reference_scenario_id}`}
            style={{ marginBottom: 4 }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
              <span style={{ fontSize: 12, fontWeight: 500, color: "#1f2937" }}>
                {`Option ${pair.scenario_label} vs. Option ${refLabel}`}
              </span>
              <span style={{ fontSize: 14, fontWeight: 600, color: "#b45309" }}>
                {_formatHeadcount(hc)}
              </span>
            </div>
            <div style={{ fontSize: 11, color: "#6b7280" }}>
              {`${_formatK(ciLow)} – ${_formatK(ciHigh)}  `}
              <span
                data-testid="distributional-ci-label"
                title="Structural uncertainty model — BandingEngine step-based schedule; not a frequentist confidence interval. See methodology panel for details."
              >
                declared interval (BandingEngine)
              </span>
            </div>
          </div>
        );
      })}
      <div
        data-testid="direction-stability-disclosure"
        style={{ fontSize: 11, color: allDirectionStable ? "#4b5563" : "#d97706", marginTop: 2 }}
      >
        {allDirectionStable
          ? "→ Direction stable across uncertainty range"
          : "→ Direction uncertain: CI spans zero"}
      </div>
      {panelOpen && summary.methodology_detail && (
        <div
          ref={methodologyPanelRef}
          data-testid="zone3-methodology-panel"
          style={{ borderTop: "1px dashed #e5e7eb", marginTop: 4, paddingTop: 4, overflowY: "auto" }}
        >
          <div data-testid="methodology-q1-population" style={rowStyle}>
            <span style={labelStyle}>Q1 population:</span>{" "}
            {summary.entity_id}: {summary.methodology_detail.q1_population.toLocaleString("en-US")} (UN WPP 2024, 20% Q1 fraction)
          </div>
          <div data-testid="methodology-ci-band" style={rowStyle}>
            <span style={labelStyle}>CI band:</span>{" "}
            {summary.methodology_detail.ci_methodology}
          </div>
          <div data-testid="methodology-extraction-path" style={rowStyle}>
            <span style={labelStyle}>Extraction path:</span>{" "}
            {summary.methodology_detail.extraction_path}
          </div>
          <div data-testid="methodology-tier-rationale" style={rowStyle}>
            <span style={labelStyle}>Tier rationale:</span>{" "}
            {summary.methodology_detail.tier_rationale}
          </div>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// CohortImpactSection — Zone 1B Cohort Impact sub-section (M16-G2 #986)
//
// Standalone store-connected component. Rendered as a sibling of MDAAlertPanelZone1B
// inside the zone-1b flex wrapper (not nested inside MDAAlertPanelZone1B) so that
// it occupies a guaranteed visible slot in zone-1b regardless of MDA panel content height.
// ---------------------------------------------------------------------------

const COHORT_SEVERITY_COLOR: Record<CohortThresholdCrossing["severity"], string> = {
  CRITICAL: "#cc0000",
  WARNING: "#a06000",
  WATCH: "#0070a0",
};

const FOCAL_BADGE_COLOR = {
  CLEAR: "#2e7d32",
  CRITICAL: "#c62828",
  UNKNOWN: "#888888",
  WARNING: "#a06000",
} as const;

interface FocalCohortConfig {
  indicator_key: string;
  floor_value: number;
  floor_label: string;
  framework: string;
}

export function CohortImpactSection({
  isCompleted = false,
  monitoredFocalCohorts,
}: {
  isCompleted?: boolean;
  monitoredFocalCohorts?: FocalCohortConfig[];
}) {
  const { cohort_threshold_crossings: crossings, current_step, trajectory } = useScenarioStepStore();
  const bp = useViewportBreakpoint();
  const isNarrow = bp === 1024;
  const headerLabel = isCompleted ? "COHORT IMPACT (HISTORICAL)" : "COHORT IMPACT";
  const emptyText = isCompleted
    ? "No cohort threshold crossings at or before this step."
    : "No cohort threshold crossings projected on current path.";

  // Sort crossings: active (non-historical) first by severity, then historical (HIST) rows.
  const activeCrossings = [...crossings]
    .filter((c) => c.step_crossed >= current_step)
    .sort((a, b) => {
      const sevOrder: Record<string, number> = { CRITICAL: 0, WARNING: 1, WATCH: 2 };
      return (sevOrder[a.severity] ?? 3) - (sevOrder[b.severity] ?? 3);
    });
  const historicalCrossings = crossings.filter((c) => c.step_crossed < current_step);
  const sortedCrossings = [...activeCrossings, ...historicalCrossings];

  // Build focal row states from trajectory indicators at current step.
  const currentStepData = trajectory?.steps.find((s) => s.step_index === current_step) ?? null;
  const focalRows = (monitoredFocalCohorts ?? []).map((focal) => {
    const rawValue = currentStepData?.frameworks[focal.framework]?.indicators?.[focal.indicator_key] ?? null;
    const numValue = rawValue !== null ? parseFloat(rawValue) : null;
    const state: "CLEAR" | "CRITICAL" | "UNKNOWN" =
      numValue === null ? "UNKNOWN" : numValue > focal.floor_value ? "CLEAR" : "CRITICAL";
    // Round to 4 decimal places before threshold comparison to avoid IEEE 754
    // accumulation (e.g. (0.420 - 0.400) / 0.400 = 0.04999... without rounding).
    const aboveFloorPct =
      numValue !== null
        ? Math.round(((numValue - focal.floor_value) / focal.floor_value) * 10000) / 10000
        : null;
    const narrowMargin = state === "CLEAR" && aboveFloorPct !== null && aboveFloorPct < 0.05;
    return { focal, numValue, state, narrowMargin };
  });

  const hasCrossings = sortedCrossings.length > 0;
  const hasFocal = focalRows.length > 0;

  function renderCrossingRow(crossing: CohortThresholdCrossing, rowIndex: number) {
    const isHistorical = crossing.step_crossed < current_step;
    const severityColor = COHORT_SEVERITY_COLOR[crossing.severity];
    const borderColor = isHistorical ? "#a06000" : severityColor;
    const isSad = !!crossing.is_synthetic && crossing.synthetic_method === "STRUCTURAL_ABSENCE";
    const badgeText = isSad
      ? "SAD"
      : crossing.is_synthetic && crossing.synthetic_method === "SYNTHETIC_MODEL"
        ? "T4"
        : crossing.is_synthetic && crossing.synthetic_method === "SYNTHETIC_COMPARABLE"
          ? "T3"
          : `T${crossing.tier}`;
    const valueDisplay = formatCohortDistance(crossing.above_floor_pct, crossing.breaches_below !== false, isSad);
    return (
      <div
        key={`${crossing.quintile_key}-${crossing.indicator_key}`}
        data-testid={`cohort-row-${rowIndex}`}
        data-crossing-step={crossing.step_crossed}
        style={{
          display: "flex",
          alignItems: "flex-start",
          gap: 4,
          borderLeft: `2px solid ${borderColor}`,
          paddingLeft: 6,
          paddingTop: 2,
          paddingBottom: 2,
          marginBottom: 2,
          fontSize: isNarrow ? 11 : 10,
        }}
      >
        <span
          data-testid="severity-badge"
          style={{
            color: isHistorical ? "#fff" : severityColor,
            background: isHistorical ? "#a06000" : undefined,
            borderRadius: isHistorical ? 3 : undefined,
            padding: isHistorical ? "1px 5px" : undefined,
            fontWeight: 700,
            flexShrink: 0,
            fontSize: isNarrow ? 10 : 9,
          }}
        >
          {isHistorical ? "HIST" : crossing.severity}
        </span>
        <span style={{ color: "#333", lineHeight: 1.3, flex: 1, minWidth: 0 }}>
          <span style={{ fontWeight: 600, display: "block", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            {crossing.cohort_label} — {crossing.indicator_label}
          </span>
          <span style={{ color: "#666", display: "block", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            {`Threshold crossed at step ${crossing.step_crossed} · `}
            <span data-testid={`cohort-value-${crossing.indicator_key}`}>
              {valueDisplay}
            </span>
            {` · ${formatSourceId(crossing.source)}`}
          </span>
        </span>
        <span
          data-testid="confidence-tier-badge"
          style={{ display: "inline-flex", flexDirection: "column", alignItems: "center", gap: 1, flexShrink: 0 }}
        >
          <span
            data-testid={`cohort-tier-badge-${crossing.indicator_key}`}
            style={{
              fontSize: isNarrow ? 10 : 8,
              fontWeight: 700,
              color: isSad ? "#7a0000" : "#005a9e",
              background: isSad ? "#ffe0e0" : "#e0eeff",
              borderRadius: 2,
              padding: "1px 3px",
              display: "inline-block",
            }}
          >
            {badgeText}
          </span>
          <span
            data-testid="confidence-tier-badge-sublabel"
            style={{ fontSize: isNarrow ? 9 : 7, color: "#6b7280", fontWeight: 400, lineHeight: 1, whiteSpace: "nowrap" }}
          >
            {isSad ? "No primary data" : badgeText === "T4" ? "Model est." : "Inferred"}
          </span>
        </span>
      </div>
    );
  }

  return (
    <div
      data-testid="zone-1b-cohort-impact"
      style={{ borderTop: "1px solid #e0e0e0", paddingTop: 2, flex: "1 1 0", overflowY: "auto", background: "#fff", position: "relative" }}
    >
      <div data-testid="cohort-impact-section">
        <div
          data-testid="cohort-section-header"
          style={{
            fontSize: 9,
            fontWeight: 600,
            color: "#555",
            letterSpacing: 0.3,
            paddingBottom: 2,
            paddingLeft: 4,
          }}
        >
          {headerLabel}
        </div>
        {!hasCrossings && !hasFocal ? (
          <div
            data-testid="cohort-empty-state"
            style={{ fontSize: 10, color: "#aaa", fontStyle: "italic", paddingLeft: 4 }}
          >
            {emptyText}
          </div>
        ) : (
          <>
            {sortedCrossings.map((crossing, idx) => renderCrossingRow(crossing, idx))}
            {focalRows.map(({ focal, numValue, state, narrowMargin }) => (
              <div
                key={`focal-${focal.indicator_key}`}
                data-testid="focal-cohort-row"
                style={{
                  display: "flex",
                  alignItems: "flex-start",
                  gap: 4,
                  borderLeft: `2px solid ${FOCAL_BADGE_COLOR[state]}`,
                  paddingLeft: 6,
                  paddingTop: 2,
                  paddingBottom: 2,
                  marginBottom: 2,
                  fontSize: isNarrow ? 11 : 10,
                }}
              >
                <span
                  data-testid="focal-badge"
                  style={{
                    background: FOCAL_BADGE_COLOR[state],
                    color: "#fff",
                    borderRadius: 3,
                    padding: "1px 5px",
                    fontSize: isNarrow ? 10 : 9,
                    fontWeight: 700,
                    flexShrink: 0,
                  }}
                >
                  {state}
                </span>
                {narrowMargin && (
                  <span
                    data-testid="focal-warning-badge"
                    style={{
                      background: FOCAL_BADGE_COLOR.WARNING,
                      color: "#fff",
                      borderRadius: 3,
                      padding: "1px 5px",
                      fontSize: isNarrow ? 10 : 9,
                      fontWeight: 700,
                      flexShrink: 0,
                    }}
                  >
                    WARNING
                  </span>
                )}
                <span style={{ color: "#333", lineHeight: 1.3, flex: 1, minWidth: 0 }}>
                  <span style={{ fontWeight: 600, display: "block", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                    {focal.indicator_key.replace(/_/g, " ")} — {focal.floor_label}
                  </span>
                  {numValue !== null && (
                    <span style={{ color: "#666", display: "block" }}>
                      {`${numValue.toFixed(3)} / floor ${focal.floor_value.toFixed(3)}`}
                    </span>
                  )}
                </span>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// MDAAlertPanelZone1B
// ---------------------------------------------------------------------------

interface MDAAlertPanelZone1BProps {
  /** Column width in px — retained for compatibility; no longer drives compact vs. full rendering. */
  columnWidth?: number;
  "data-testid"?: string;
  /** M17-G2 — loaded comparison scenario configs with threshold crossings. */
  comparisonScenarios?: ScenarioComparisonConfig[];
}

export function MDAAlertPanelZone1B({
  "data-testid": dataTestId = "zone-1b-mda-alerts",
  comparisonScenarios = [],
}: MDAAlertPanelZone1BProps) {
  const { mda_alerts, mode } = useScenarioStepStore();

  const sorted = sortAlerts(mda_alerts);
  const topAlert = sorted[0] ?? null;
  const remainingAlerts = sorted.slice(1);

  // [NEW] badge: fires when the top-ranked alert's mda_id changes between renders.
  // Does NOT fire when the same mda_id persists with an updated consecutive count.
  const [showNewBadge, setShowNewBadge] = useState(false);
  const prevTopMdaIdRef = useRef<string | null>(null);

  useEffect(() => {
    const currentMdaId = topAlert?.mda_id ?? null;
    if (prevTopMdaIdRef.current !== null && currentMdaId !== prevTopMdaIdRef.current) {
      setShowNewBadge(true);
    }
    prevTopMdaIdRef.current = currentMdaId;
  }, [topAlert?.mda_id]);

  const clearNewBadge = () => setShowNewBadge(false);

  return (
    <div
      data-testid={dataTestId}
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        overflow: "hidden",
        boxSizing: "border-box",
      }}
    >
      {comparisonScenarios.length > 0 && (
        <div style={{ padding: "4px 6px" }}>
          {comparisonScenarios.map((sc) => {
            if (!sc.scenarioId) return null;
            const slug = sc.scenarioId.replace(/^[a-z]{3}-/, "");
            const palette = SCENARIO_COMPARISON_PALETTE[sc.paletteIndex];
            const crossings = sc.thresholdCrossings ?? [];
            return (
              <div key={sc.scenarioId} style={{ marginBottom: 4 }}>
                <div
                  data-testid={`zone1b-scenario-header-${slug}`}
                  style={{ fontSize: 10, fontWeight: 700, color: palette.color, marginBottom: 2 }}
                >
                  {`Option ${sc.label}`}
                </div>
                {crossings.length > 0 ? (
                  crossings.map((tc, j) => (
                    <div
                      key={j}
                      data-testid={`zone1b-threshold-row-scenario-${slug}`}
                      style={{ fontSize: 9, color: tc.severity === "CRITICAL" ? "#b91c1c" : "#d97706", paddingLeft: 6 }}
                    >
                      {`${tc.severity} ${tc.indicator_name ?? tc.indicator_id} — crossed step ${tc.first_crossing_step}`}
                    </div>
                  ))
                ) : (
                  <div
                    data-testid={`zone1b-no-crossings-${slug}`}
                    style={{ fontSize: 9, color: "#6b7280", paddingLeft: 6, fontStyle: "italic" }}
                  >
                    {`[no crossings through step ${sc.trajectory?.step_count ?? 8}]`}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
      {topAlert === null ? (
        <div
          data-testid="zone-1b-top-detail"
          style={{
            flex: "0 0 auto",
            padding: "8px",
            color: "#888",
            fontSize: 12,
            fontStyle: "italic",
          }}
        >
          No active threshold breaches.
        </div>
      ) : (
        <TopAlertDetail
          alert={topAlert}
          mode={mode}
          showNewBadge={showNewBadge}
        />
      )}

      <CompactAlertList
        alerts={remainingAlerts}
        onClearNewBadge={clearNewBadge}
      />
    </div>
  );
}
