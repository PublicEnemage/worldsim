import { useEffect, useRef, useState } from "react";
import type { AttributeSummary } from "../types";

const API_BASE = "http://localhost:8000/api/v1";

interface Props {
  value: string;
  onChange: (attributeKey: string) => void;
}

export default function AttributeSelector({ value, onChange }: Props) {
  const [attributes, setAttributes] = useState<AttributeSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const onChangeRef = useRef(onChange);
  onChangeRef.current = onChange;

  useEffect(() => {
    fetch(`${API_BASE}/attributes/available`)
      .then((res) => {
        if (!res.ok) throw new Error(`API error ${res.status}`);
        return res.json() as Promise<AttributeSummary[]>;
      })
      .then((data) => {
        setAttributes(data);
        setLoading(false);
        // Fire initial selection so App.tsx state matches what the select shows.
        // If the current value isn't in the list (e.g. a scenario attribute like
        // gdp_growth), keep the current value — ChoroplethMap handles 404 gracefully.
        if (data.length > 0 && !data.some((a) => a.attribute_key === value)) {
          onChangeRef.current(data[0].attribute_key);
        }
      })
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : "Failed to load attributes");
        setLoading(false);
      });
    // value intentionally omitted — only fire on mount
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (loading) return <span style={{ color: "#999" }}>Loading attributes…</span>;
  if (error) return <span style={{ color: "#c00" }}>Error: {error}</span>;

  // value may be a scenario attribute (e.g. gdp_growth) not in the static list.
  // Render it as a synthetic option so the select stays in sync.
  const inList = attributes.some((a) => a.attribute_key === value);
  const options = inList
    ? attributes
    : [{ attribute_key: value, unit: "—", variable_type: "—" }, ...attributes];

  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      style={{ fontSize: 14, padding: "4px 8px", borderRadius: 4, maxWidth: 260 }}
    >
      {options.map((a) => (
        <option key={a.attribute_key} value={a.attribute_key}>
          {a.attribute_key} ({a.unit}, {a.variable_type})
        </option>
      ))}
    </select>
  );
}
