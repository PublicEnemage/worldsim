/* eslint-disable react-refresh/only-export-components */
/**
 * MDAAlertPanelZone1B — Zone 1B co-primary instrument.
 *
 * Replaces the M8 EntityDetailDrawer MDAAlertPanel with a Zone 1 instrument that:
 * - subscribes to useScenarioStepStore (atomicity invariant — DD-012)
 * - sorts by severity (TERMINAL → CRITICAL → WARNING) then step_index ascending (US-014)
 * - renders compact three-line format at 240px (1024×768) and full-density at 400px+ (US-013)
 * - shows framework source (FIN/HDI/ECO/GOV) without expanding (US-015)
 * - formats alert text per mode (US-016, UX-RULING-1)
 * - shows "Caused by:" causal attribution in Mode 3 only (US-017)
 * - shows negotiation-defensibility label in Mode 2 and 3 (ADR-008 Decision 5)
 * - clicking any row opens AlertDetailPanel showing sparkline + threshold detail (#745)
 *
 * Implements: ADR-008 Decision 5, FA brief §Layout and Viewport (UD-F1 compact row format)
 */
import { useScenarioStepStore, type Zone1BAlert } from "../store/scenarioStepStore";
import { getIndicatorDisplayNameAny } from "../lib/indicatorDisplayNames";

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
// Exported pure functions (tested by MDAAlertPanelZone1B.test.ts)
// ---------------------------------------------------------------------------

/**
 * Sort alerts: TERMINAL first, CRITICAL second, WARNING third.
 * Within same severity: ascending step_index (earlier step first).
 * US-014 contract.
 */
export function sortAlerts(alerts: Zone1BAlert[]): Zone1BAlert[] {
  return [...alerts].sort((a, b) => {
    const severityDiff = SEVERITY_ORDER[a.severity] - SEVERITY_ORDER[b.severity];
    if (severityDiff !== 0) return severityDiff;
    return a.step_index - b.step_index;
  });
}

/**
 * Returns the negotiation-defensibility label for a confidence tier.
 * Required in Mode 2 and Mode 3. ADR-008 Decision 5.
 */
export function getNegotiationLabel(tier: number): string {
  if (tier <= 2) return "High confidence — cite directly";
  if (tier === 3) return "Moderate confidence — cite with caveat";
  return "Exploratory — do not cite";
}

/**
 * Format the alert tense text per mode. UX-RULING-1 (US-016).
 *
 * Mode 1: "[indicator] crossed [severity] threshold at step N."
 * Mode 2: "[indicator] is projected to cross [severity] threshold at step N."
 * Mode 3: "[SEVERITY] — [indicator] — [cohort] — step N"
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
  // Mode 3: "[SEVERITY] — [indicator] — [cohort] — step N"
  return `${alert.severity} — ${indicator} — ${cohort} — step ${alert.step_index}`;
}

/**
 * Truncate indicator display name to ≤ maxChars, appending "…" if truncated.
 * US-013 compact row format at 240px: 22 char limit.
 */
export function truncateIndicatorName(name: string, maxChars = 22): string {
  if (name.length <= maxChars) return name;
  return name.slice(0, maxChars - 1) + "…";
}

/**
 * Build SVG polyline points for a composite score sparkline.
 * Returns null if fewer than 2 data points with non-null scores.
 * Exported for unit tests.
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
// AlertDetailPanel — drill-in view for a selected alert (#745)
// ---------------------------------------------------------------------------

interface AlertDetailPanelProps {
  alert: Zone1BAlert;
  onClose: () => void;
}

function AlertDetailPanel({ alert, onClose }: AlertDetailPanelProps) {
  const { trajectory } = useScenarioStepStore();
  const color = SEVERITY_COLOR[alert.severity];

  // Human-readable name: frontend registry takes precedence over backend title-case
  const displayName = getIndicatorDisplayNameAny(alert.indicator_key);

  // Framework composite score time-series from trajectory (already fetched)
  const scores: (number | null)[] = trajectory
    ? trajectory.steps.map((s) => s.frameworks[alert.framework]?.composite_score ?? null)
    : [];

  // MDA floor for this framework (from trajectory mda_floors)
  const mda_floor = trajectory?.mda_floors.find((f) => f.framework === alert.framework);

  const W = 200;
  const H = 56;
  const PADDING = 4;

  const polylinePoints = buildSparklinePoints(scores, W, H, PADDING);

  // Y position of the MDA floor line on the sparkline
  const floorY = (() => {
    if (!mda_floor || scores.length === 0) return null;
    const finite = scores.filter((s) => s !== null) as number[];
    if (finite.length === 0) return null;
    const maxV = Math.max(...finite, 0.01);
    return PADDING + (1 - mda_floor.floor_value / maxV) * (H - PADDING * 2);
  })();

  // X position of the alert's crossing step
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
      {/* Header: display name + close button */}
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

      {/* Framework composite score sparkline */}
      {polylinePoints && (
        <div data-testid="detail-sparkline" style={{ marginBottom: 6 }}>
          <svg
            width={W}
            height={H}
            style={{ display: "block", overflow: "visible" }}
            aria-label={`${FRAMEWORK_ABBREV[alert.framework] ?? alert.framework} composite score trajectory`}
          >
            {/* MDA floor reference line */}
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
            {/* Score trajectory */}
            <polyline
              points={polylinePoints}
              fill="none"
              stroke="#2171b5"
              strokeWidth={1.5}
              strokeLinejoin="round"
            />
            {/* Crossing step marker */}
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

      {/* Indicator snapshot: current vs floor */}
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
            {alert.consecutive_breach_steps} step{alert.consecutive_breach_steps !== 1 ? "s" : ""}
          </span>
        </div>
      </div>

      {/* Causal attribution — Mode 3 only */}
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
// Compact row (240px — 1024×768)
// ---------------------------------------------------------------------------

interface CompactRowProps {
  alert: Zone1BAlert;
  mode: "MODE_1" | "MODE_2" | "MODE_3";
  isFocused: boolean;
  onClick: () => void;
}

function CompactAlertRow({ alert, mode, isFocused, onClick }: CompactRowProps) {
  const fwAbbrev = FRAMEWORK_ABBREV[alert.framework] ?? alert.framework.toUpperCase().slice(0, 3);
  const sevAbbrev = SEVERITY_ABBREV[alert.severity];
  const color = SEVERITY_COLOR[alert.severity];
  const bg = isFocused ? "#f0f4ff" : SEVERITY_BG[alert.severity];
  const cohortDisplay = alert.cohort
    ? alert.cohort.length > 10
      ? alert.cohort.slice(0, 9) + "…"
      : alert.cohort
    : "all";
  const indicatorDisplay = truncateIndicatorName(
    alert.indicator_key.replace(/_/g, " "),
    22,
  );

  return (
    <div
      data-testid="mda-alert-row"
      data-severity={alert.severity}
      data-framework={alert.framework}
      data-step={alert.step_index}
      data-focused={isFocused ? "true" : undefined}
      onClick={onClick}
      style={{
        background: bg,
        borderLeft: `3px solid ${color}`,
        borderRadius: 3,
        padding: "5px 7px",
        fontSize: 11,
        marginBottom: 4,
        cursor: "pointer",
        outline: isFocused ? `1px solid ${color}` : undefined,
      }}
    >
      {/* Line 1: severity pill + severity abbrev + framework abbrev */}
      <div
        data-testid="alert-line-1"
        style={{ display: "flex", alignItems: "center", gap: 4, marginBottom: 2 }}
      >
        <span
          style={{
            width: 8,
            height: 6,
            borderRadius: 2,
            background: color,
            display: "inline-block",
            flexShrink: 0,
          }}
        />
        <span style={{ fontWeight: 700, color, letterSpacing: 0.3 }}>
          {sevAbbrev}
        </span>
        <span style={{ color: "#666", marginLeft: 2 }}>{fwAbbrev}</span>
      </div>

      {/* Line 2: indicator display name ≤ 22 chars */}
      <div
        data-testid="alert-line-2"
        style={{ color: "#333", marginBottom: 1 }}
      >
        {indicatorDisplay}
      </div>

      {/* Line 3: Step N • cohort */}
      <div
        data-testid="alert-line-3"
        style={{ color: "#777" }}
      >
        {`Step ${alert.step_index} • ${cohortDisplay}`}
      </div>

      {/* Causal attribution — Mode 3 only (US-017) */}
      {mode === "MODE_3" && alert.causal_attribution && (
        <div
          data-testid="alert-causal-attribution"
          style={{ color: "#555", marginTop: 3, fontStyle: "italic" }}
        >
          {`Caused by: ${alert.causal_attribution}`}
        </div>
      )}

      {/* Negotiation-defensibility label — Mode 2 and 3 (ADR-008 Decision 5) */}
      {(mode === "MODE_2" || mode === "MODE_3") && (
        <div
          data-testid="alert-negotiation-label"
          style={{
            color: alert.confidence_tier >= 4 ? "#a06000" : "#555",
            fontSize: 10,
            marginTop: 2,
          }}
        >
          {getNegotiationLabel(alert.confidence_tier)}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Full-density row (400px — 1280×800)
// ---------------------------------------------------------------------------

interface FullDensityRowProps {
  alert: Zone1BAlert;
  mode: "MODE_1" | "MODE_2" | "MODE_3";
  isFocused: boolean;
  onClick: () => void;
}

function FullDensityAlertRow({ alert, mode, isFocused, onClick }: FullDensityRowProps) {
  const fwAbbrev = FRAMEWORK_ABBREV[alert.framework] ?? alert.framework.toUpperCase().slice(0, 3);
  const color = SEVERITY_COLOR[alert.severity];
  const bg = isFocused ? "#f0f4ff" : SEVERITY_BG[alert.severity];
  const indicatorFull = alert.indicator_key.replace(/_/g, " ");
  const cohortFull = alert.cohort ?? "all cohorts";
  const alertText = formatAlertText(alert, mode);

  return (
    <div
      data-testid="mda-alert-row"
      data-severity={alert.severity}
      data-framework={alert.framework}
      data-step={alert.step_index}
      data-focused={isFocused ? "true" : undefined}
      onClick={onClick}
      style={{
        background: bg,
        borderLeft: `3px solid ${color}`,
        borderRadius: 3,
        padding: "7px 10px",
        fontSize: 12,
        marginBottom: 5,
        cursor: "pointer",
        outline: isFocused ? `1px solid ${color}` : undefined,
      }}
    >
      {/* Severity + framework source */}
      <div
        data-testid="alert-line-1"
        style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 3 }}
      >
        <span
          style={{
            background: color,
            color: "#fff",
            borderRadius: 3,
            padding: "1px 6px",
            fontSize: 11,
            fontWeight: 700,
            letterSpacing: 0.5,
          }}
        >
          {alert.severity}
        </span>
        <span
          data-testid="alert-framework-source"
          style={{ color: "#666", fontSize: 11, fontWeight: 600 }}
        >
          {fwAbbrev}
        </span>
      </div>

      {/* Indicator name — full, untruncated */}
      <div
        data-testid="alert-line-2"
        style={{ color: "#333", fontWeight: 500, marginBottom: 2 }}
      >
        {indicatorFull}
      </div>

      {/* Cohort */}
      <div
        data-testid="alert-line-3"
        style={{ color: "#666", marginBottom: 2 }}
      >
        {cohortFull}
      </div>

      {/* Mode-specific alert text */}
      <div
        data-testid="alert-mode-text"
        style={{ color: "#444", marginBottom: 2 }}
      >
        {alertText}
      </div>

      {/* Causal attribution — Mode 3 only (US-017) */}
      {mode === "MODE_3" && alert.causal_attribution && (
        <div
          data-testid="alert-causal-attribution"
          style={{ color: "#555", marginTop: 3, fontStyle: "italic" }}
        >
          {`Caused by: ${alert.causal_attribution}`}
        </div>
      )}

      {/* Negotiation-defensibility label — Mode 2 and 3 */}
      {(mode === "MODE_2" || mode === "MODE_3") && (
        <div
          data-testid="alert-negotiation-label"
          style={{
            color: alert.confidence_tier >= 4 ? "#a06000" : "#555",
            fontSize: 11,
            marginTop: 3,
          }}
        >
          {getNegotiationLabel(alert.confidence_tier)}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// MDAAlertPanelZone1B
// ---------------------------------------------------------------------------

interface MDAAlertPanelZone1BProps {
  /** Column width in px — drives compact vs full-density rendering. */
  columnWidth?: number;
  "data-testid"?: string;
  /** The mda_id of the currently focused alert (controlled externally — #745). */
  focusedAlertMdaId?: string | null;
  /** Called when the user clicks an alert row or closes the detail panel. */
  onSelectAlert?: (mdaId: string | null) => void;
}

export function MDAAlertPanelZone1B({
  columnWidth = 240,
  "data-testid": dataTestId = "zone-1b-mda-alerts",
  focusedAlertMdaId = null,
  onSelectAlert,
}: MDAAlertPanelZone1BProps) {
  const { mda_alerts, mode, current_step } = useScenarioStepStore();

  const sorted = sortAlerts(mda_alerts);
  // Top 3 for display — panel must not scroll past the third alert (US-013)
  const topAlerts = sorted.slice(0, 3);

  const isCompact = columnWidth < 320;

  const focusedAlert = focusedAlertMdaId
    ? mda_alerts.find((a) => a.mda_id === focusedAlertMdaId) ?? null
    : null;

  const handleRowClick = (alert: Zone1BAlert) => {
    if (focusedAlertMdaId === alert.mda_id) {
      // Toggle off — clicking the selected row closes the detail
      onSelectAlert?.(null);
    } else {
      onSelectAlert?.(alert.mda_id);
    }
  };

  return (
    <div
      data-testid={dataTestId}
      data-current-step={current_step}
      style={{
        padding: "6px 4px",
        overflowY: "auto",
        height: "100%",
        boxSizing: "border-box",
      }}
    >
      {sorted.length === 0 ? (
        <div
          data-testid="mda-no-alerts"
          style={{ color: "#888", fontSize: 12, padding: "8px 4px", fontStyle: "italic" }}
        >
          No active threshold breaches.
        </div>
      ) : (
        <>
          {topAlerts.map((alert) =>
            isCompact ? (
              <CompactAlertRow
                key={`${alert.mda_id}-${alert.step_index}`}
                alert={alert}
                mode={mode}
                isFocused={focusedAlertMdaId === alert.mda_id}
                onClick={() => handleRowClick(alert)}
              />
            ) : (
              <FullDensityAlertRow
                key={`${alert.mda_id}-${alert.step_index}`}
                alert={alert}
                mode={mode}
                isFocused={focusedAlertMdaId === alert.mda_id}
                onClick={() => handleRowClick(alert)}
              />
            ),
          )}
          {sorted.length > 3 && (
            <div
              data-testid="mda-more-alerts"
              style={{ color: "#aaa", fontSize: 11, textAlign: "center", padding: "4px 0" }}
            >
              +{sorted.length - 3} more
            </div>
          )}

          {/* Inline detail panel for the focused alert */}
          {focusedAlert && (
            <AlertDetailPanel
              alert={focusedAlert}
              onClose={() => onSelectAlert?.(null)}
            />
          )}
        </>
      )}
    </div>
  );
}
