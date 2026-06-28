/* eslint-disable react-refresh/only-export-components */
/**
 * ControlPlaneColumn — Column 3 content in Mode 3 (ADR-019 D-3).
 *
 * Two forms within the 280px reserved column:
 *   Form 1 — Policy Instruments (blue #0284c7)
 *     - policyInputType selector: FiscalMultiplier | LegitimacyConstraint
 *     - Type-driven parameter slider
 *     - Apply at step selector
 *     - "Apply policy input" button
 *     - Applied inputs history list
 *
 *   Form 2 — Scenario Shocks (orange #ea580c)
 *     - shockType selector: all 7 ADR-019 types
 *     - Type-driven parameter inputs
 *     - Inject at step selector
 *     - "Inject scenario shock" button
 *     - Injected shocks history list
 *
 * Both form HEADERS must be visible without scroll at 1280×800 (Artifact 3 Q3).
 * History lists may scroll within their section.
 *
 * Lazy-mount optimization (#1217): This component is mounted cold when Mode 3
 * is entered and unmounted when Mode 3 exits. No shared state with Mode2ColumnSurface.
 */
import React, { useState } from "react";
import { useScenarioStepStore } from "../store/scenarioStepStore";

// ---------------------------------------------------------------------------
// Exported types
// ---------------------------------------------------------------------------

export interface Mode3Params {
  input_type: "FiscalMultiplier" | "LegitimacyConstraint";
  fiscal_multiplier: number;
  legitimacy_index: number | null;
  apply_at_step: number;
  /** Alias for apply_at_step — used by handleApplyControlChange branch request. */
  branch_from_step: number;
}

export interface ShockInjectRequest {
  shock_type: string;
  inject_at_step: number;
  severity?: number;
  growth_rate_delta?: number;
  duration_steps?: number;
  attack_magnitude?: number;
  creditor_class?: string;
  share_affected?: number;
  source_country?: string;
  transmission_rate?: number;
  gdp_impact?: number;
}

// ---------------------------------------------------------------------------
// Style constants — blue for Form 1, orange for Form 2
// ---------------------------------------------------------------------------

const PANEL_STYLE: React.CSSProperties = {
  padding: "10px 12px",
  background: "#fff",
  display: "flex",
  flexDirection: "column",
  gap: 0,
  height: "100%",
  boxSizing: "border-box",
  overflowY: "auto",
};

const FORM_HEADER_STYLE = (color: string): React.CSSProperties => ({
  fontSize: 11,
  fontWeight: 700,
  color,
  letterSpacing: 0.5,
  paddingBottom: 6,
  borderBottom: `2px solid ${color}`,
  marginBottom: 8,
});

const LABEL_STYLE: React.CSSProperties = {
  fontSize: 11,
  fontWeight: 600,
  color: "#555",
  marginBottom: 2,
  display: "block",
};

const value_style = (color: string): React.CSSProperties => ({
  fontSize: 12,
  fontWeight: 700,
  color,
  minWidth: 32,
  textAlign: "right" as const,
  fontVariantNumeric: "tabular-nums",
});

const apply_btn_style = (color: string, disabled: boolean): React.CSSProperties => ({
  marginTop: 4,
  padding: "6px 14px",
  background: disabled ? "#d1d5db" : color,
  color: "#fff",
  border: "none",
  borderRadius: 4,
  fontSize: 12,
  fontWeight: 700,
  cursor: disabled ? "not-allowed" : "pointer",
  alignSelf: "flex-start" as const,
});

// ---------------------------------------------------------------------------
// Shock types from ADR-019 D-6
// ---------------------------------------------------------------------------

const SHOCK_TYPES = [
  { value: "GrowthShock",       label: "Growth Shock",       testid: "shock-type-growth-shock" },
  { value: "ElectionShock",     label: "Election Shock",     testid: "shock-type-election-shock" },
  { value: "CurrencyAttack",    label: "Currency Attack",    testid: "shock-type-currency-attack" },
  { value: "CreditorDefection", label: "Creditor Defection", testid: "shock-type-creditor-defection" },
  { value: "GeopoliticalShock", label: "Geopolitical Shock", testid: "shock-type-geopolitical-shock" },
  { value: "NaturalDisaster",   label: "Natural Disaster",   testid: "shock-type-natural-disaster" },
  { value: "ContagionShock",    label: "Contagion Shock",    testid: "shock-type-contagion-shock" },
] as const;

type ShockTypeValue = typeof SHOCK_TYPES[number]["value"];

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Format fiscal multiplier for display (e.g. 1.50×). Exported for unit tests. */
export function formatFiscalMultiplier(value: number): string {
  return `${value.toFixed(2)}×`;
}

/** Format legitimacy index for display (e.g. 0.75 → "75%"). Exported for unit tests. */
export function formatLegitimacyIndex(value: number): string {
  return `${Math.round(value * 100)}%`;
}

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

interface ControlPlaneColumnProps {
  /** Called when the user applies a Form 1 policy input. */
  onApplyChange: (params: Mode3Params) => void;
  /** Called when the user injects a Form 2 scenario shock. */
  onInjectShock: (request: ShockInjectRequest) => void;
  /** Current step — used as the default apply/inject step. */
  currentStep: number;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export function ControlPlaneColumn({
  onApplyChange,
  onInjectShock,
  currentStep,
}: ControlPlaneColumnProps) {
  const { recomputeStatus } = useScenarioStepStore();
  const isDisabled = recomputeStatus === "computing" || recomputeStatus === "pending";

  // --- Form 1 state ---
  const [policyInputType, setPolicyInputType] = useState<"FiscalMultiplier" | "LegitimacyConstraint">(
    "FiscalMultiplier",
  );
  const [fiscalMultiplier, setFiscalMultiplier] = useState(1.0);
  const [legitimacyIndex, setLegitimacyIndex] = useState(0.7);
  const [policyStep, setPolicyStep] = useState(Math.max(1, currentStep));
  const [appliedInputs, setAppliedInputs] = useState<Array<{ step: number; type: string; value: number }>>([]);

  // --- Form 2 state ---
  const [shockType, setShockType] = useState<ShockTypeValue>("GrowthShock");
  const [shockStep, setShockStep] = useState(Math.max(1, currentStep));
  const [severity, setSeverity] = useState(0.3);
  const [growthRateDelta, setGrowthRateDelta] = useState(-0.02);
  const [durationSteps, setDurationSteps] = useState(2);
  const [attackMagnitude, setAttackMagnitude] = useState(0.1);
  const [shareAffected, setShareAffected] = useState(0.2);
  const [creditorClass, setCreditorClass] = useState("bilateral");
  const [transmissionRate, setTransmissionRate] = useState(0.2);
  const [sourceCountry, setSourceCountry] = useState("");
  const [gdpImpact, setGdpImpact] = useState(-0.03);
  const [injectedShocks, setInjectedShocks] = useState<Array<{ step: number; type: string }>>([]);

  // --- Form 1: Apply policy input ---
  const handleApplyPolicy = () => {
    if (isDisabled) return;
    const params: Mode3Params = {
      input_type: policyInputType,
      fiscal_multiplier: policyInputType === "FiscalMultiplier" ? fiscalMultiplier : 1.0,
      legitimacy_index: policyInputType === "LegitimacyConstraint" ? legitimacyIndex : null,
      apply_at_step: policyStep,
      branch_from_step: policyStep,
    };
    onApplyChange(params);
    setAppliedInputs((prev) => [
      ...prev,
      {
        step: policyStep,
        type: policyInputType,
        value: policyInputType === "FiscalMultiplier" ? fiscalMultiplier : legitimacyIndex,
      },
    ]);
  };

  // --- Form 2: Inject scenario shock ---
  const handleInjectShock = () => {
    if (isDisabled) return;
    const base: ShockInjectRequest = { shock_type: shockType, inject_at_step: shockStep };
    let request: ShockInjectRequest = { ...base };

    switch (shockType) {
      case "GrowthShock":
        request = { ...base, growth_rate_delta: growthRateDelta, duration_steps: durationSteps };
        break;
      case "ElectionShock":
        request = { ...base, severity };
        break;
      case "CurrencyAttack":
        request = { ...base, attack_magnitude: attackMagnitude };
        break;
      case "CreditorDefection":
        request = { ...base, creditor_class: creditorClass, share_affected: shareAffected };
        break;
      case "GeopoliticalShock":
        request = { ...base, severity };
        break;
      case "NaturalDisaster":
        request = { ...base, gdp_impact: gdpImpact };
        break;
      case "ContagionShock":
        request = { ...base, source_country: sourceCountry, transmission_rate: transmissionRate };
        break;
    }
    onInjectShock(request);
    setInjectedShocks((prev) => [...prev, { step: shockStep, type: shockType }]);
  };

  const maxStep = Math.max(1, currentStep);
  const BLUE = "#0284c7";
  const ORANGE = "#ea580c";

  return (
    <div data-testid="control-plane" style={PANEL_STYLE}>
      {/* ------------------------------------------------------------------ */}
      {/* Form 1 — Policy Instruments */}
      {/* ------------------------------------------------------------------ */}
      <div data-testid="control-plane-form1">
        <div style={FORM_HEADER_STYLE(BLUE)}>POLICY INSTRUMENTS</div>

        {/* Input type selector */}
        <div style={{ marginBottom: 8 }}>
          <span style={LABEL_STYLE}>Input type</span>
          <select
            data-testid="policy-input-type-selector"
            value={policyInputType}
            disabled={isDisabled}
            onChange={(e) => setPolicyInputType(e.target.value as typeof policyInputType)}
            style={{ width: "100%", fontSize: 11, padding: "3px 4px", borderRadius: 3 }}
          >
            <option value="FiscalMultiplier">Fiscal Multiplier</option>
            <option value="LegitimacyConstraint">Legitimacy Constraint</option>
          </select>
        </div>

        {/* Type-driven parameter slider */}
        {policyInputType === "FiscalMultiplier" ? (
          <div style={{ marginBottom: 8 }}>
            <span style={LABEL_STYLE}>
              Fiscal Multiplier
              <span style={{ fontWeight: 400, color: "#888", marginLeft: 4 }}>(0.10–3.00)</span>
            </span>
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <input
                data-testid="policy-param-slider"
                type="range"
                min={0.1}
                max={3.0}
                step={0.05}
                value={fiscalMultiplier}
                disabled={isDisabled}
                onChange={(e) => setFiscalMultiplier(parseFloat(e.target.value))}
                style={{ flex: 1, accentColor: BLUE }}
              />
              <span data-testid="fiscal-multiplier-value" style={value_style(BLUE)}>
                {formatFiscalMultiplier(fiscalMultiplier)}
              </span>
            </div>
          </div>
        ) : (
          <div style={{ marginBottom: 8 }}>
            <span style={LABEL_STYLE}>
              Legitimacy Index
              <span style={{ fontWeight: 400, color: "#888", marginLeft: 4 }}>(0.0–1.0)</span>
            </span>
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <input
                data-testid="policy-param-slider"
                type="range"
                min={0.0}
                max={1.0}
                step={0.05}
                value={legitimacyIndex}
                disabled={isDisabled}
                onChange={(e) => setLegitimacyIndex(parseFloat(e.target.value))}
                style={{ flex: 1, accentColor: BLUE }}
              />
              <span data-testid="legitimacy-index-value" style={value_style(BLUE)}>
                {formatLegitimacyIndex(legitimacyIndex)}
              </span>
            </div>
          </div>
        )}

        {/* Apply at step selector */}
        <div style={{ marginBottom: 8 }}>
          <span style={LABEL_STYLE}>Apply at step</span>
          <select
            data-testid="policy-step-selector"
            value={policyStep}
            disabled={isDisabled}
            onChange={(e) => setPolicyStep(parseInt(e.target.value, 10))}
            style={{ width: "100%", fontSize: 11, padding: "3px 4px", borderRadius: 3 }}
          >
            {Array.from({ length: maxStep }, (_, i) => i + 1).map((s) => (
              <option key={s} value={s}>
                Step {s}
              </option>
            ))}
          </select>
        </div>

        {/* Apply button */}
        <button
          data-testid="apply-policy-input"
          style={apply_btn_style(BLUE, isDisabled)}
          disabled={isDisabled}
          onClick={handleApplyPolicy}
          type="button"
        >
          {isDisabled ? "Recomputing…" : "Apply policy input"}
        </button>

        {/* History list */}
        <div style={{ marginTop: 8 }}>
          <span style={{ ...LABEL_STYLE, color: BLUE }}>Applied inputs</span>
          <div
            data-testid="policy-inputs-history"
            data-testid-scroll="policy-history-scroll"
            style={{
              maxHeight: 60,
              overflowY: "auto",
              fontSize: 10,
              color: "#555",
              border: appliedInputs.length > 0 ? "1px solid #e2e8f0" : "none",
              borderRadius: 3,
              padding: appliedInputs.length > 0 ? "3px 5px" : 0,
            }}
          >
            {appliedInputs.length === 0 ? (
              <span style={{ color: "#bbb", fontStyle: "italic" }}>None yet</span>
            ) : (
              appliedInputs.map((inp, i) => (
                <div key={i} style={{ paddingBottom: 2 }}>
                  Step {inp.step} — {inp.type}: {inp.value.toFixed(2)}
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Divider */}
      <div style={{ borderTop: "1px solid #f0f0f0", margin: "10px 0" }} />

      {/* ------------------------------------------------------------------ */}
      {/* Form 2 — Scenario Shocks */}
      {/* ------------------------------------------------------------------ */}
      <div data-testid="control-plane-form2">
        <div style={FORM_HEADER_STYLE(ORANGE)}>SCENARIO SHOCKS</div>

        {/* Shock type selector — all 7 ADR-019 types */}
        <div style={{ marginBottom: 8 }}>
          <span style={LABEL_STYLE}>Shock type</span>
          <select
            value={shockType}
            disabled={isDisabled}
            onChange={(e) => setShockType(e.target.value as ShockTypeValue)}
            style={{ width: "100%", fontSize: 11, padding: "3px 4px", borderRadius: 3 }}
          >
            {SHOCK_TYPES.map(({ value, label, testid }) => (
              <option key={value} value={value} data-testid={testid}>
                {label}
              </option>
            ))}
          </select>
        </div>

        {/* Type-driven parameter inputs */}
        {shockType === "GrowthShock" && (
          <>
            <div style={{ marginBottom: 6 }}>
              <span style={LABEL_STYLE}>Growth rate delta</span>
              <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                <input
                  type="range" min={-0.1} max={0.1} step={0.005}
                  value={growthRateDelta} disabled={isDisabled}
                  onChange={(e) => setGrowthRateDelta(parseFloat(e.target.value))}
                  style={{ flex: 1, accentColor: ORANGE }}
                />
                <span style={value_style(ORANGE)}>{(growthRateDelta * 100).toFixed(1)}%</span>
              </div>
            </div>
            <div style={{ marginBottom: 6 }}>
              <span style={LABEL_STYLE}>Duration (steps)</span>
              <input
                type="number" min={1} max={10} value={durationSteps} disabled={isDisabled}
                onChange={(e) => setDurationSteps(parseInt(e.target.value, 10) || 1)}
                style={{ width: 60, fontSize: 11, padding: "2px 4px", borderRadius: 3 }}
              />
            </div>
          </>
        )}

        {(shockType === "ElectionShock" || shockType === "GeopoliticalShock") && (
          <div style={{ marginBottom: 6 }}>
            <span style={LABEL_STYLE}>Severity</span>
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <input
                type="range" min={0} max={1} step={0.05}
                value={severity} disabled={isDisabled}
                onChange={(e) => setSeverity(parseFloat(e.target.value))}
                style={{ flex: 1, accentColor: ORANGE }}
              />
              <span style={value_style(ORANGE)}>{(severity * 100).toFixed(0)}%</span>
            </div>
          </div>
        )}

        {shockType === "CurrencyAttack" && (
          <div style={{ marginBottom: 6 }}>
            <span style={LABEL_STYLE}>Attack magnitude</span>
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <input
                type="range" min={0} max={0.5} step={0.01}
                value={attackMagnitude} disabled={isDisabled}
                onChange={(e) => setAttackMagnitude(parseFloat(e.target.value))}
                style={{ flex: 1, accentColor: ORANGE }}
              />
              <span style={value_style(ORANGE)}>{(attackMagnitude * 100).toFixed(0)}%</span>
            </div>
          </div>
        )}

        {shockType === "CreditorDefection" && (
          <>
            <div style={{ marginBottom: 6 }}>
              <span style={LABEL_STYLE}>Creditor class</span>
              <select
                value={creditorClass} disabled={isDisabled}
                onChange={(e) => setCreditorClass(e.target.value)}
                style={{ width: "100%", fontSize: 11, padding: "3px 4px", borderRadius: 3 }}
              >
                <option value="bilateral">Bilateral</option>
                <option value="multilateral">Multilateral</option>
                <option value="commercial">Commercial</option>
              </select>
            </div>
            <div style={{ marginBottom: 6 }}>
              <span style={LABEL_STYLE}>Share affected</span>
              <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                <input
                  type="range" min={0} max={1} step={0.05}
                  value={shareAffected} disabled={isDisabled}
                  onChange={(e) => setShareAffected(parseFloat(e.target.value))}
                  style={{ flex: 1, accentColor: ORANGE }}
                />
                <span style={value_style(ORANGE)}>{(shareAffected * 100).toFixed(0)}%</span>
              </div>
            </div>
          </>
        )}

        {shockType === "NaturalDisaster" && (
          <div style={{ marginBottom: 6 }}>
            <span style={LABEL_STYLE}>GDP impact</span>
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <input
                type="range" min={-0.2} max={0} step={0.005}
                value={gdpImpact} disabled={isDisabled}
                onChange={(e) => setGdpImpact(parseFloat(e.target.value))}
                style={{ flex: 1, accentColor: ORANGE }}
              />
              <span style={value_style(ORANGE)}>{(gdpImpact * 100).toFixed(1)}%</span>
            </div>
          </div>
        )}

        {shockType === "ContagionShock" && (
          <>
            <div style={{ marginBottom: 6 }}>
              <span style={LABEL_STYLE}>Source country (ISO)</span>
              <input
                type="text" maxLength={3} value={sourceCountry} disabled={isDisabled}
                placeholder="e.g. EGY"
                onChange={(e) => setSourceCountry(e.target.value.toUpperCase())}
                style={{ width: "100%", fontSize: 11, padding: "3px 4px", borderRadius: 3 }}
              />
            </div>
            <div style={{ marginBottom: 6 }}>
              <span style={LABEL_STYLE}>Transmission rate</span>
              <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                <input
                  type="range" min={0} max={1} step={0.05}
                  value={transmissionRate} disabled={isDisabled}
                  onChange={(e) => setTransmissionRate(parseFloat(e.target.value))}
                  style={{ flex: 1, accentColor: ORANGE }}
                />
                <span style={value_style(ORANGE)}>{(transmissionRate * 100).toFixed(0)}%</span>
              </div>
            </div>
          </>
        )}

        {/* Inject at step selector */}
        <div style={{ marginBottom: 8 }}>
          <span style={LABEL_STYLE}>Inject at step</span>
          <select
            data-testid="shock-step-selector"
            value={shockStep}
            disabled={isDisabled}
            onChange={(e) => setShockStep(parseInt(e.target.value, 10))}
            style={{ width: "100%", fontSize: 11, padding: "3px 4px", borderRadius: 3 }}
          >
            {Array.from({ length: maxStep }, (_, i) => i + 1).map((s) => (
              <option key={s} value={s}>
                Step {s}
              </option>
            ))}
          </select>
        </div>

        {/* Inject button */}
        <button
          data-testid="inject-scenario-shock"
          style={apply_btn_style(ORANGE, isDisabled)}
          disabled={isDisabled}
          onClick={handleInjectShock}
          type="button"
        >
          {isDisabled ? "Processing…" : "Inject scenario shock"}
        </button>

        {/* Shock history list */}
        <div style={{ marginTop: 8 }}>
          <span style={{ ...LABEL_STYLE, color: ORANGE }}>Injected shocks</span>
          <div
            data-testid="shock-events-history"
            data-testid-scroll="shock-history-scroll"
            style={{
              maxHeight: 60,
              overflowY: "auto",
              fontSize: 10,
              color: "#555",
              border: injectedShocks.length > 0 ? "1px solid #e2e8f0" : "none",
              borderRadius: 3,
              padding: injectedShocks.length > 0 ? "3px 5px" : 0,
            }}
          >
            {injectedShocks.length === 0 ? (
              <span style={{ color: "#bbb", fontStyle: "italic" }}>None yet</span>
            ) : (
              injectedShocks.map((shock, i) => (
                <div key={i} style={{ paddingBottom: 2 }}>
                  Step {shock.step} — {shock.type}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
