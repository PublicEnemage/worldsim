/**
 * Mode2ColumnSurface — Column 3 content in Mode 2 (ADR-019 D-2).
 *
 * Renders a read-only scenario identity block and the "Enter Active Control"
 * affordance. The dashed border signals "this zone activates in Mode 3" without
 * competing with Zone 1A/1B content.
 *
 * No useState for form parameters — this is a pure display + navigation component.
 * State is managed entirely by the parent (ScenarioInstrumentCluster).
 *
 * Customer Agent kryptonite: button label MUST be "Enter Active Control" — not
 * "Enter Mode 3". Jargon-free label required (Artifact 3 §Decision 1 panel condition).
 */
import React from "react";

export interface Mode2ColumnSurfaceProps {
  /** Scenario display name. */
  scenarioName: string;
  /** ISO 3166-1 alpha-3 entity code (e.g. "SEN", "ZMB"). */
  entityName: string;
  /** Calibration vintage label (start_date or loaded data vintage). */
  calibrationVintage: string;
  /** First step of the simulation horizon. */
  startStep: number;
  /** Last step of the simulation horizon. */
  endStep: number;
  /** Called when the user clicks "Enter Active Control". */
  onEnterActiveControl: () => void;
}

const SURFACE_STYLE: React.CSSProperties = {
  background: "#f8fafc",
  border: "1px dashed #94a3b8",
  borderRadius: 4,
  padding: "12px 12px",
  display: "flex",
  flexDirection: "column",
  gap: 10,
  height: "100%",
  boxSizing: "border-box",
};

const SECTION_LABEL_STYLE: React.CSSProperties = {
  fontSize: 9,
  fontWeight: 700,
  letterSpacing: 0.8,
  color: "#94a3b8",
  textTransform: "uppercase" as const,
  marginBottom: 4,
};

const IDENTITY_ROW_STYLE: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: 3,
};

const IDENTITY_KEY_STYLE: React.CSSProperties = {
  fontSize: 10,
  color: "#94a3b8",
  fontWeight: 500,
};

const IDENTITY_VALUE_STYLE: React.CSSProperties = {
  fontSize: 11,
  color: "#334155",
  fontWeight: 600,
};

const ENTER_BTN_STYLE: React.CSSProperties = {
  marginTop: "auto",
  padding: "8px 12px",
  background: "#f1f5f9",
  color: "#475569",
  border: "1px solid #94a3b8",
  borderRadius: 4,
  fontSize: 12,
  fontWeight: 700,
  cursor: "pointer",
  textAlign: "center" as const,
  letterSpacing: 0.2,
  transition: "background 0.15s, color 0.15s",
};

export function Mode2ColumnSurface({
  scenarioName,
  entityName,
  calibrationVintage,
  startStep,
  endStep,
  onEnterActiveControl,
}: Mode2ColumnSurfaceProps) {
  return (
    <div data-testid="mode2-column-surface" style={SURFACE_STYLE}>
      <div style={SECTION_LABEL_STYLE}>Scenario</div>

      <div style={IDENTITY_ROW_STYLE}>
        <span style={IDENTITY_KEY_STYLE}>Name</span>
        <span style={IDENTITY_VALUE_STYLE}>{scenarioName || "—"}</span>
      </div>

      <div style={IDENTITY_ROW_STYLE}>
        <span style={IDENTITY_KEY_STYLE}>Entity</span>
        <span style={IDENTITY_VALUE_STYLE}>{entityName || "—"}</span>
      </div>

      <div style={IDENTITY_ROW_STYLE}>
        <span style={IDENTITY_KEY_STYLE}>Calibration vintage</span>
        <span style={IDENTITY_VALUE_STYLE}>{calibrationVintage || "—"}</span>
      </div>

      <div style={IDENTITY_ROW_STYLE}>
        <span style={IDENTITY_KEY_STYLE}>Run horizon</span>
        <span style={IDENTITY_VALUE_STYLE}>
          Step {startStep} → Step {endStep}
        </span>
      </div>

      <div
        style={{
          borderTop: "1px solid #e2e8f0",
          marginTop: 4,
          paddingTop: 10,
        }}
      />

      <button
        data-testid="enter-active-control-btn"
        style={ENTER_BTN_STYLE}
        onClick={onEnterActiveControl}
        type="button"
      >
        Enter Active Control
      </button>
    </div>
  );
}
