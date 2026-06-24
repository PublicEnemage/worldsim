export interface QuantitySchema {
  value: string; // Decimal as string — float prohibition at API boundary
  unit: string;
  variable_type: string;
  confidence_tier: number;
  observation_date: string | null;
  source_id: string | null;
}

export interface ChoroplethFeatureProperties {
  entity_id: string;
  name: string;
  attribute_value: string; // Decimal as string — to-number only in MapLibre paint expression
  has_territorial_note: boolean;
  territorial_note: string | null;
  confidence_tier: number;
}

export interface AttributeSummary {
  attribute_key: string;
  unit: string;
  variable_type: string;
}

export interface GeoJSONFeature {
  type: "Feature";
  geometry: object;
  properties: ChoroplethFeatureProperties;
}

export interface GeoJSONFeatureCollection {
  type: "FeatureCollection";
  features: GeoJSONFeature[];
}

export interface AdvanceResponse {
  scenario_id: string;
  step_executed: number;
  steps_remaining: number;
  final_status: string;
  is_complete: boolean;
}

export interface DeltaRecord {
  value_a: string;
  value_b: string;
  delta: string;
  direction: "increase" | "decrease" | "unchanged";
  confidence_tier: number;
}

export interface CompareResponse {
  scenario_a_id: string;
  scenario_b_id: string;
  step_a: number;
  step_b: number;
  deltas: Record<string, Record<string, DeltaRecord>>;
}

export interface ScenarioResponse {
  scenario_id: string;
  name: string;
  description: string | null;
  status: string;
  version: number;
  created_at: string;
}

export interface ScenarioConfigSchema {
  entities: string[];
  initial_attributes: Record<string, unknown>;
  n_steps: number;
  timestep_label: string;
  fiscal_multiplier?: number;
  start_date?: string;
  /** M16-G3 #274 — long-run projection horizon (1–100). When set, overrides n_steps as total step count. */
  projection_steps?: number | null;
  // DA-G5-3: confirmed JSONB paths for political economy module configuration
  modules_config?: {
    political_economy?: {
      enabled?: boolean;
      conditionality_type?: "standard" | "strict" | "relaxed";
    };
  };
}

// ADR-016 Component 1 — Data quality preview response
export interface DataQualityFramework {
  framework: string;
  confidence_tier: number;
  source_institution: string | null;
  data_vintage: string | null;
  is_synthetic: boolean;
  synthetic_basis: string | null;
  loadable: boolean;           // G4: true if registered but not yet pulled
  load_action_available: boolean; // G4: true when loadable is true
}

export interface DataQualityResponse {
  entity_id: string;
  year: number;
  frameworks: DataQualityFramework[];
}

// M15-G4 Path 1 — Pull job and fidelity contextualisation types
export interface PullJobResponse {
  job_id: string;
  entity_id: string;
  year: number;
  status: "queued" | "running" | "complete" | "failed";
}

export interface PullJobStatusResponse {
  job_id: string;
  status: "queued" | "running" | "complete" | "failed";
  frameworks_loaded: string[];
  error: string | null;
}

export interface AnalogousCase {
  case_id: string;
  case_name: string;
  mechanism_type: string;
  mechanism_match: string;
  directional_accuracy_validated: boolean;
  magnitude_validated: boolean;
  use_for: string;
}

export interface FidelityContextResponse {
  scenario_id: string;
  entity_id: string;
  analogous_case: AnalogousCase | null;
}

// ADR-016 Component 2 — Initial state (Grounding Strip) response
// Field names match /initial-state (api_contracts.yml): `source` + `vintage`.
// Do not use source_institution/data_vintage here — those are /data-quality fields.
export interface GroundingIndicator {
  name: string;
  display_name: string;
  value: number | null;
  unit: string | null;
  source: string | null;
  vintage: string | null;
  confidence_tier: number | null;
  is_synthetic: boolean;
}

export interface GroundingFramework {
  indicators: GroundingIndicator[];
}

export interface InitialStateResponse {
  scenario_id: string;
  entity_id: string;
  step_0_year: number | null;
  frameworks: Record<string, GroundingFramework>;
}

export interface ScenarioDetailResponse extends ScenarioResponse {
  configuration: ScenarioConfigSchema;
  scheduled_inputs: unknown[];
}

export interface DeltaChoroplethFeatureProperties {
  entity_id: string;
  name: string;
  attribute_value: string; // str(delta) — Decimal as string
  value_a: string;
  value_b: string;
  delta_direction: "increase" | "decrease" | "unchanged";
  confidence_tier: number;
  has_territorial_note: boolean;
  territorial_note: string | null;
}

// ---------------------------------------------------------------------------
// Multi-framework measurement output — ADR-005 Decision 2 / Decision 4
// ---------------------------------------------------------------------------

export type MDASeverity = "WARNING" | "CRITICAL" | "TERMINAL";

export interface MDAAlert {
  mda_id: string;
  entity_id: string;
  indicator_key: string;
  severity: MDASeverity;
  floor_value: string;       // Decimal as string
  current_value: string;     // Decimal as string
  approach_pct_remaining: string; // Decimal as string; negative when breached
  consecutive_breach_steps: number;
}

export interface FrameworkOutput {
  framework: string;
  composite_score: string | null; // Decimal as string, or null if unimplemented
  indicators: Record<string, QuantitySchema | Record<string, QuantitySchema>>; // flat or nested per cohort
  mda_alerts: MDAAlert[];
  has_below_floor_indicator: boolean;
  note: string | null;
}

export interface MultiFrameworkOutput {
  entity_id: string;
  entity_name: string;
  timestep: string;
  scenario_id: string;
  step_index: number;
  outputs: Record<string, FrameworkOutput>;
  ia1_disclosure: string;
}

// ADR-005 Decision 4 — radar chart data shapes

// ADR-005 Decision M8-5: composite_score is number | null.
// null = framework not yet certified for API surface (e.g. governance at M8).
// 0.0 is a valid score — distinct from null. Do not conflate.
export interface RadarAxisDatum {
  framework: string;
  label: string;
  composite_score: number | null;  // null = not yet implemented; 0.0–2.0 when active
  is_implemented: boolean;
  has_critical_breach: boolean;
  breach_count: number;
}

export interface FrameworkWeights {
  financial: number;
  human_development: number;
  ecological: number;
  governance: number;
}
