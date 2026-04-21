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
