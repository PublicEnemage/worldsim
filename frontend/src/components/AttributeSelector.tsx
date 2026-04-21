import { useEffect, useState } from "react";
import type { AttributeSummary } from "../types";

const API_BASE = "http://localhost:8000/api/v1";

interface Props {
  onChange: (attributeKey: string) => void;
}

export default function AttributeSelector({ onChange }: Props) {
  const [attributes, setAttributes] = useState<AttributeSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/attributes/available`)
      .then((res) => {
        if (!res.ok) throw new Error(`API error ${res.status}`);
        return res.json() as Promise<AttributeSummary[]>;
      })
      .then((data) => {
        setAttributes(data);
        setLoading(false);
      })
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : "Failed to load attributes");
        setLoading(false);
      });
  }, []);

  if (loading) return <span style={{ color: "#999" }}>Loading attributes…</span>;
  if (error) return <span style={{ color: "#c00" }}>Error: {error}</span>;

  return (
    <select
      onChange={(e) => onChange(e.target.value)}
      style={{ fontSize: 14, padding: "4px 8px", borderRadius: 4 }}
    >
      {attributes.map((a) => (
        <option key={a.attribute_key} value={a.attribute_key}>
          {a.attribute_key} ({a.unit}, {a.variable_type})
        </option>
      ))}
    </select>
  );
}
