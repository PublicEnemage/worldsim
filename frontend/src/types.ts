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
