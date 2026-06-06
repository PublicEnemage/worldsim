/**
 * ControlPlane — Zone: control-plane. Mode 3 Active Control panel.
 *
 * Implements the control input interface for Mode 3 (G6b, Issue #753).
 * Renders at least two configurable policy instruments:
 *   1. Fiscal multiplier — scaling factor for spending and tax multipliers
 *   2. Legitimacy index — political feasibility constraint (0–1)
 *
 * When the user clicks "Apply Change", onApplyChange is called with the
 * current parameter values. The parent (ScenarioInstrumentCluster) drives
 * the branch creation and advance loop.
 *
 * Disabled during recompute (recomputeStatus === "computing" | "pending").
 */
import React, { useState } from "react";
import { useScenarioStepStore } from "../store/scenarioStepStore";

export interface Mode3Params {
  fiscal_multiplier: number;
  branch_from_step: number;
}

interface ControlPlaneProps {
  /** Called when the user applies a parameter change. Parent drives the branch. */
  onApplyChange: (params: Mode3Params) => void;
  /** Current step — used as the default branch_from_step. */
  currentStep: number;
}

const PANEL_STYLE: React.CSSProperties = {
  padding: "10px 12px",
  background: "#f8f4ff",
  borderTop: "2px solid #8b5cf6",
  display: "flex",
  flexDirection: "column",
  gap: 10,
};

const LABEL_STYLE: React.CSSProperties = {
  fontSize: 11,
  fontWeight: 600,
  color: "#555",
  marginBottom: 2,
  display: "block",
};

const VALUE_STYLE: React.CSSProperties = {
  fontSize: 12,
  fontWeight: 700,
  color: "#8b5cf6",
  minWidth: 32,
  textAlign: "right" as const,
  fontVariantNumeric: "tabular-nums",
};

const APPLY_BTN_STYLE: React.CSSProperties = {
  marginTop: 4,
  padding: "6px 14px",
  background: "#8b5cf6",
  color: "#fff",
  border: "none",
  borderRadius: 4,
  fontSize: 12,
  fontWeight: 700,
  cursor: "pointer",
  alignSelf: "flex-start",
};

const APPLY_BTN_DISABLED_STYLE: React.CSSProperties = {
  ...APPLY_BTN_STYLE,
  background: "#c4b5fd",
  cursor: "not-allowed",
};

/**
 * Format fiscal multiplier for display (e.g. 1.50x).
 * Exported for unit testing.
 */
export function formatFiscalMultiplier(value: number): string {
  return `${value.toFixed(2)}×`;
}

/**
 * Format legitimacy index for display (e.g. 0.75 → "75%").
 * Exported for unit testing.
 */
export function formatLegitimacyIndex(value: number): string {
  return `${Math.round(value * 100)}%`;
}

export function ControlPlane({ onApplyChange, currentStep }: ControlPlaneProps) {
  const { recomputeStatus, branchFromStep } = useScenarioStepStore();

  const isDisabled = recomputeStatus === "computing" || recomputeStatus === "pending";

  const [fiscalMultiplier, setFiscalMultiplier] = useState(1.0);
  const [branchStep, setBranchStep] = useState(currentStep);

  const handleApply = () => {
    if (isDisabled) return;
    onApplyChange({
      fiscal_multiplier: fiscalMultiplier,
      branch_from_step: branchStep,
    });
  };

  const activeFromStep = branchFromStep ?? currentStep;

  return (
    <div data-testid="zone-control-plane" style={PANEL_STYLE}>
      <div style={{ fontSize: 11, fontWeight: 700, color: "#8b5cf6", letterSpacing: 0.5 }}>
        ACTIVE CONTROL
      </div>

      {/* Instrument 1: Fiscal Multiplier */}
      <div>
        <span style={LABEL_STYLE}>
          Fiscal Multiplier
          <span style={{ fontWeight: 400, color: "#888", marginLeft: 6 }}>
            (spending &amp; tax scaling)
          </span>
        </span>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <input
            data-testid="fiscal-multiplier-slider"
            type="range"
            min={0.1}
            max={3.0}
            step={0.05}
            value={fiscalMultiplier}
            disabled={isDisabled}
            onChange={(e) => setFiscalMultiplier(parseFloat(e.target.value))}
            style={{ flex: 1, accentColor: "#8b5cf6" }}
          />
          <span data-testid="fiscal-multiplier-value" style={VALUE_STYLE}>
            {formatFiscalMultiplier(fiscalMultiplier)}
          </span>
        </div>
      </div>

      {/* Instrument 2: Branch From Step */}
      <div>
        <span style={LABEL_STYLE}>
          Branch From Step
          <span style={{ fontWeight: 400, color: "#888", marginLeft: 6 }}>
            (recompute forward from step)
          </span>
        </span>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <input
            data-testid="branch-from-step-slider"
            type="range"
            min={0}
            max={Math.max(0, currentStep)}
            step={1}
            value={branchStep}
            disabled={isDisabled}
            onChange={(e) => setBranchStep(parseInt(e.target.value, 10))}
            style={{ flex: 1, accentColor: "#8b5cf6" }}
          />
          <span data-testid="branch-from-step-value" style={VALUE_STYLE}>
            {branchStep}
          </span>
        </div>
      </div>

      {/* Apply button */}
      <button
        data-testid="apply-control-change"
        style={isDisabled ? APPLY_BTN_DISABLED_STYLE : APPLY_BTN_STYLE}
        disabled={isDisabled}
        onClick={handleApply}
      >
        {isDisabled ? "Recomputing…" : "Apply Change"}
      </button>

      {/* Branch anchor annotation */}
      {activeFromStep > 0 && (
        <div
          data-testid="branch-anchor-label"
          style={{ fontSize: 10, color: "#888", fontStyle: "italic" }}
        >
          Branched from step {activeFromStep} — baseline locked
        </div>
      )}
    </div>
  );
}
