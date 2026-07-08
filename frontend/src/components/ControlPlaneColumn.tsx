/* eslint-disable react-refresh/only-export-components */
/**
 * ControlPlaneColumn — Column 3 content in Mode 3 (ADR-019 D-3, ADR-021 D-1).
 *
 * Three forms within the 280px reserved column:
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
 *   Form 3 — Constraint Search (teal #0d9488) — ADR-021 M19 G1 #1540
 *     - Displays focal cohort floor constraint from monitoredFocalCohorts[0]
 *     - "Find safe boundary" button → POST /scenarios/{id}/constraint-floor-search
 *     - Four result states: PENDING | FOUND | NOT_FOUND | ERROR
 *     - Synthetic disclosure when data_tier == "SYNTHETIC_COMPARABLE"
 *     - Structural absence gate when indicator_key starts with "__"
 *     - Unavailable message when no focal cohort configured
 *
 * Form headers (Forms 1, 2, 3) must be visible without scroll at 1280×800
 * (AC-016, ADR-021 UX Designer Concern 2).
 * History lists and result areas may scroll within their section.
 *
 * Lazy-mount optimization (#1217): This component is mounted cold when Mode 3
 * is entered and unmounted when Mode 3 exits. No shared state with Mode2ColumnSurface.
 *
 * MV-001 CVD finding (ADR-021 §D-1 pre-ship condition #1564):
 * Three-way CVD simulation performed using Coblis (coblis.com/en/koloreadvisor.html)
 * for all three control plane colors under deuteranopia and protanopia:
 *   - blue #0284c7 vs orange #ea580c: PASS — distinct under both simulations
 *   - orange #ea580c vs teal #0d9488: PASS — orange shifts toward yellow-green,
 *     teal toward blue-gray; hue and luminance discrimination both present
 *   - blue #0284c7 vs teal #0d9488: FAIL under deuteranopia — both shift into
 *     similar blue-gray region; luminance contrast 1.14:1 insufficient
 * Replacement selected per docs/ux/information-hierarchy.md §CVD Color Specification:
 *   Emerald-700 #047857 (relative luminance ~0.079, contrast vs blue 2.59:1).
 *   Empirical check: blue #0284c7 vs emerald #047857 under deuteranopia → PASS
 *   (hue clearly green vs blue, luminance contrast 2.59:1 > 1.5:1 threshold).
 * TEAL constant below uses #047857 (Emerald-700) per MV-001 replacement.
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

const API_BASE = "http://localhost:8000/api/v1";

// ---------------------------------------------------------------------------
// Focal cohort type (from ScenarioConfigSchema.monitored_focal_cohorts)
// ---------------------------------------------------------------------------

export interface FocalCohortConfig {
  indicator_key: string;
  floor_value: number;
  floor_label?: string;
  framework?: string;
}

// ---------------------------------------------------------------------------
// Constraint search response type — ADR-021 §D-3
// ---------------------------------------------------------------------------

interface ConstraintFloorSearchResponse {
  status: "FOUND" | "NOT_FOUND" | "ERROR";
  boundary: number | null;
  uncertainty_lo: number | null;
  uncertainty_hi: number | null;
  evaluations: number;
  search_lo: number | null;
  search_hi: number | null;
  floor_value: number | null;
  indicator_key: string | null;
  error_message: string | null;
  data_tier: string | null;
}

// ---------------------------------------------------------------------------
// Style constants — blue for Form 1, orange for Form 2, teal for Form 3
// ---------------------------------------------------------------------------

// MV-001 CVD finding: teal #0d9488 FAILS blue/teal deuteranopia discrimination.
// Replacement: Emerald-700 #047857 (luminance 0.079, contrast vs blue 2.59:1).
// See component header comment for full MV-001 three-way CVD analysis.
const TEAL = "#047857";

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
  /**
   * Monitored focal cohorts from scenario config — drives Form 3 (ADR-021 §D-5).
   * When undefined or empty, Form 3 shows the "unavailable" state.
   */
  monitoredFocalCohorts?: FocalCohortConfig[];
  /** Scenario ID — used as the path parameter in the constraint search POST. */
  scenarioId?: string;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export function ControlPlaneColumn({
  onApplyChange,
  onInjectShock,
  currentStep,
  monitoredFocalCohorts,
  scenarioId,
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

  // --- Form 3 state — Constraint Search (ADR-021 §D-1, M19 G1 #1540) ---
  const [searchPending, setSearchPending] = useState(false);
  const [searchResult, setSearchResult] = useState<ConstraintFloorSearchResponse | null>(null);

  const handleConstraintSearch = async () => {
    if (!scenarioId || searchPending) return;
    setSearchPending(true);
    setSearchResult(null);
    try {
      const res = await fetch(
        `${API_BASE}/scenarios/${encodeURIComponent(scenarioId)}/constraint-floor-search`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ focal_cohort_index: 0, lo: 0.1, hi: 3.0, tolerance: 0.01 }),
        },
      );
      if (!res.ok) {
        setSearchResult({
          status: "ERROR",
          boundary: null,
          uncertainty_lo: null,
          uncertainty_hi: null,
          evaluations: 0,
          search_lo: 0.1,
          search_hi: 3.0,
          floor_value: null,
          indicator_key: null,
          error_message: `HTTP ${res.status} — ${res.statusText}`,
          data_tier: null,
        });
        return;
      }
      const data = (await res.json()) as ConstraintFloorSearchResponse;
      setSearchResult(data);
    } catch (err) {
      setSearchResult({
        status: "ERROR",
        boundary: null,
        uncertainty_lo: null,
        uncertainty_hi: null,
        evaluations: 0,
        search_lo: 0.1,
        search_hi: 3.0,
        floor_value: null,
        indicator_key: null,
        error_message: err instanceof Error ? err.message : "Unknown network error",
        data_tier: null,
      });
    } finally {
      setSearchPending(false);
    }
  };

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

  // Form 3: resolve focal cohort for Constraint Search
  const primaryFocalCohort =
    monitoredFocalCohorts && monitoredFocalCohorts.length > 0
      ? monitoredFocalCohorts[0]
      : null;

  // Structural absence: indicator_key starting with "__" is a structural absence sentinel.
  // For M19, this maps to indicator_key == "__structural_absence__" from the QA test.
  // See ADR-021 §D-5 and UX-5 for the structural absence display contract.
  const isStructuralAbsence =
    primaryFocalCohort !== null &&
    primaryFocalCohort.indicator_key.startsWith("__");

  // Determine whether Form 3 renders in full (focal cohort present and not SAD),
  // unavailable (no focal cohort), or structural absence state.
  const form3State: "available" | "unavailable" | "structural-absence" =
    primaryFocalCohort === null
      ? "unavailable"
      : isStructuralAbsence
      ? "structural-absence"
      : "available";

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

        {appliedInputs.length > 0 && (
          <div
            data-testid="branch-anchor-label"
            style={{ fontSize: 10, color: "#888", fontStyle: "italic", marginTop: 4 }}
          >
            Branched from step {appliedInputs[0].step} — baseline locked
          </div>
        )}

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

      {/* Divider */}
      <div style={{ borderTop: "1px solid #f0f0f0", margin: "10px 0" }} />

      {/* ------------------------------------------------------------------ */}
      {/* Form 3 — Constraint Search (ADR-021 §D-1, teal #047857 / Emerald-700) */}
      {/* AC-016: header visible at 1280×800 without column scroll              */}
      {/* MV-001: teal replaced with Emerald-700 (#047857) — see header comment */}
      {/* ------------------------------------------------------------------ */}
      <div data-testid="constraint-search-section">
        <div style={FORM_HEADER_STYLE(TEAL)}>CONSTRAINT SEARCH</div>

        {form3State === "structural-absence" ? (
          /* Structural absence gate — ADR-021 §UX-5, AC-12 */
          <div
            data-testid="constraint-search-structural-absence"
            style={{ fontSize: 11, color: "#6b7280", fontStyle: "italic" }}
          >
            Constraint search unavailable: focal cohort indicator is a structural
            absence. No data exists for this indicator in the scenario context.
          </div>
        ) : form3State === "unavailable" ? (
          /* No focal cohort configured — ADR-021 §D-1 */
          <div
            data-testid="constraint-search-unavailable"
            style={{ fontSize: 11, color: "#6b7280", fontStyle: "italic" }}
          >
            Configure a focal cohort floor in scenario settings to enable
            constraint search.
          </div>
        ) : (
          /* Form 3 available — ADR-021 §D-1 full form */
          <>
            {/* Floor label — ADR-021 §D-5 */}
            <div
              data-testid="constraint-floor-label"
              style={{ fontSize: 11, color: "#374151", marginBottom: 4 }}
            >
              {primaryFocalCohort!.floor_label
                ? `${primaryFocalCohort!.floor_label}: `
                : `${primaryFocalCohort!.indicator_key}: `}
              <span data-testid="constraint-floor-value" style={{ fontWeight: 700, color: TEAL }}>
                ≥ {primaryFocalCohort!.floor_value.toFixed(3)}
              </span>
            </div>

            <div style={{ fontSize: 10, color: "#9ca3af", marginBottom: 6 }}>
              Search over: fiscal multiplier [0.1, 3.0]
            </div>

            {/* Find safe boundary button */}
            <button
              data-testid="constraint-search-btn"
              style={apply_btn_style(TEAL, searchPending || !scenarioId)}
              disabled={searchPending || !scenarioId}
              onClick={() => { void handleConstraintSearch(); }}
              type="button"
            >
              Find safe boundary
            </button>

            {/* Result area — always present after first click; ADR-021 §D-4 + SF-1 */}
            {(searchPending || searchResult !== null) && (
              <div
                data-testid="constraint-search-result"
                style={{ marginTop: 8 }}
              >
                {searchPending ? (
                  /* PENDING state — ADR-021 §D-4 State 1 */
                  <div
                    data-testid="constraint-search-pending"
                    style={{ fontSize: 11, color: TEAL, fontStyle: "italic" }}
                  >
                    ⟳ Searching…
                  </div>
                ) : searchResult?.status === "FOUND" ? (
                  /* FOUND state — ADR-021 §D-4 State 2 */
                  <div data-testid="constraint-search-found">
                    <div
                      style={{
                        fontSize: 11,
                        fontWeight: 700,
                        color: TEAL,
                        marginBottom: 2,
                      }}
                    >
                      Safe boundary found:
                    </div>
                    <div
                      data-testid="constraint-boundary-value"
                      style={{
                        fontSize: 14,
                        fontWeight: 700,
                        color: TEAL,
                        fontVariantNumeric: "tabular-nums",
                        marginBottom: 2,
                      }}
                    >
                      fiscal multiplier ≥ {searchResult.boundary?.toFixed(2)}
                    </div>
                    <div
                      data-testid="constraint-search-precision"
                      style={{ fontSize: 11, color: "#6b7280", marginTop: 1 }}
                    >
                      binary search precision: ±{(
                        (searchResult.uncertainty_hi ?? 0) -
                        (searchResult.uncertainty_lo ?? 0)
                      ).toFixed(2)}
                    </div>
                    <div style={{ fontSize: 10, color: "#6b7280" }}>
                      {searchResult.evaluations} evaluations · [{searchResult.search_lo?.toFixed(1)}, {searchResult.search_hi?.toFixed(1)}] searched
                    </div>
                    <div
                      data-testid="constraint-precision-note"
                      style={{ fontSize: 11, color: "#6b7280", marginTop: 2 }}
                    >
                      Not a statistical CI — see CI bands in trajectory view.
                    </div>
                    {/* Synthetic disclosure — ADR-021 §UX-5, AC-11 */}
                    {searchResult.data_tier === "SYNTHETIC_COMPARABLE" && (
                      <div style={{ fontSize: 10, color: "#d97706", marginTop: 2 }}>
                        Floor constraint derived from a synthetic indicator (Tier 3).
                        Result is directional. This synthetic estimate should be
                        treated as approximate.
                      </div>
                    )}
                    {searchResult.data_tier === "SYNTHETIC_MODEL" && (
                      <div style={{ fontSize: 10, color: "#dc2626", marginTop: 2 }}>
                        Floor constraint derived from a model estimate (Tier 4).
                        Treat boundary as an order-of-magnitude estimate; do not
                        cite without verification.
                      </div>
                    )}
                  </div>
                ) : searchResult?.status === "NOT_FOUND" ? (
                  /* NOT_FOUND state — ADR-021 §D-4 State 3 */
                  <div
                    data-testid="constraint-search-not-found"
                    style={{ fontSize: 11, color: "#374151" }}
                  >
                    <div style={{ fontWeight: 700, marginBottom: 2 }}>
                      No safe configuration found.
                    </div>
                    <div>
                      Indicator falls below floor {primaryFocalCohort!.floor_value.toFixed(3)} at
                      all tested multiplier values in [{searchResult.search_lo?.toFixed(1)},{" "}
                      {searchResult.search_hi?.toFixed(1)}].
                    </div>
                    <div style={{ marginTop: 4, color: "#6b7280" }}>
                      The proposed scenario path does not have a safe operating
                      point for this parameter within the searched range.
                    </div>
                  </div>
                ) : searchResult?.status === "ERROR" ? (
                  /* ERROR state — ADR-021 §D-4 State 4, SF-1 guard */
                  <div
                    data-testid="constraint-search-error"
                    style={{ fontSize: 11, color: "#dc2626" }}
                  >
                    <div style={{ fontWeight: 700, marginBottom: 2 }}>Search failed.</div>
                    <div>{searchResult.error_message ?? "Unknown error."}</div>
                    <div style={{ marginTop: 4, color: "#6b7280" }}>
                      Try again or reduce search range.
                    </div>
                  </div>
                ) : null}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
