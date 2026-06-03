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
 *
 * Implements: ADR-008 Decision 5, FA brief §Layout and Viewport (UD-F1 compact row format)
 */
import { useScenarioStepStore, type Zone1BAlert } from "../store/scenarioStepStore";

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

// ---------------------------------------------------------------------------
// Compact row (240px — 1024×768)
// ---------------------------------------------------------------------------

interface CompactRowProps {
  alert: Zone1BAlert;
  mode: "MODE_1" | "MODE_2" | "MODE_3";
}

function CompactAlertRow({ alert, mode }: CompactRowProps) {
  const fwAbbrev = FRAMEWORK_ABBREV[alert.framework] ?? alert.framework.toUpperCase().slice(0, 3);
  const sevAbbrev = SEVERITY_ABBREV[alert.severity];
  const color = SEVERITY_COLOR[alert.severity];
  const bg = SEVERITY_BG[alert.severity];
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
      style={{
        background: bg,
        borderLeft: `3px solid ${color}`,
        borderRadius: 3,
        padding: "5px 7px",
        fontSize: 11,
        marginBottom: 4,
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

function FullDensityAlertRow({ alert, mode }: CompactRowProps) {
  const fwAbbrev = FRAMEWORK_ABBREV[alert.framework] ?? alert.framework.toUpperCase().slice(0, 3);
  const color = SEVERITY_COLOR[alert.severity];
  const bg = SEVERITY_BG[alert.severity];
  const indicatorFull = alert.indicator_key.replace(/_/g, " ");
  const cohortFull = alert.cohort ?? "all cohorts";
  const alertText = formatAlertText(alert, mode);

  return (
    <div
      data-testid="mda-alert-row"
      data-severity={alert.severity}
      data-framework={alert.framework}
      data-step={alert.step_index}
      style={{
        background: bg,
        borderLeft: `3px solid ${color}`,
        borderRadius: 3,
        padding: "7px 10px",
        fontSize: 12,
        marginBottom: 5,
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
}

export function MDAAlertPanelZone1B({
  columnWidth = 240,
  "data-testid": dataTestId = "zone-1b-mda-alerts",
}: MDAAlertPanelZone1BProps) {
  const { mda_alerts, mode, current_step } = useScenarioStepStore();

  const sorted = sortAlerts(mda_alerts);
  // Top 3 for display — panel must not scroll past the third alert (US-013)
  const topAlerts = sorted.slice(0, 3);

  const isCompact = columnWidth < 320;

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
              />
            ) : (
              <FullDensityAlertRow
                key={`${alert.mda_id}-${alert.step_index}`}
                alert={alert}
                mode={mode}
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
        </>
      )}
    </div>
  );
}
