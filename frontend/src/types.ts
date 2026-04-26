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

export interface RadarAxisDatum {
  framework: string;
  label: string;
  composite_score: number;   // 0.0–1.0; unimplemented → 0
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
