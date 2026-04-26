import { useState } from "react";
import type { FrameworkOutput, QuantitySchema } from "../types";

interface Props {
  framework: string;
  output: FrameworkOutput;
}

const TIER_COLORS: Record<number, string> = {
  1: "#0a0",
  2: "#5a0",
  3: "#a60",
  4: "#a00",
  5: "#600",
};

function TierBadge({ tier }: { tier: number }) {
  return (
    <span
      style={{
        background: TIER_COLORS[tier] ?? "#888",
        color: "#fff",
        borderRadius: 3,
        padding: "0 5px",
        fontSize: 10,
        fontWeight: 700,
      }}
      title={`Data quality tier ${tier}`}
    >
      T{tier}
    </span>
  );
}

function IndicatorRow({ name, qty }: { name: string; qty: QuantitySchema }) {
  return (
    <tr>
      <td style={{ padding: "3px 6px", fontFamily: "monospace", fontSize: 11, color: "#333" }}>
        {name}
      </td>
      <td style={{ padding: "3px 6px", textAlign: "right", fontFamily: "monospace", fontSize: 11 }}>
        {qty.value}
      </td>
      <td style={{ padding: "3px 6px", color: "#666", fontSize: 11 }}>
        {qty.unit}
      </td>
      <td style={{ padding: "3px 6px", textAlign: "center" }}>
        <TierBadge tier={qty.confidence_tier} />
      </td>
    </tr>
  );
}

function isCohortBlock(value: unknown): value is Record<string, QuantitySchema> {
  if (typeof value !== "object" || value === null) return false;
  // A cohort block's first key is an indicator key (no "value" at top level)
  return !("value" in value);
}

export default function FrameworkPanel({ framework, output }: Props) {
  const [open, setOpen] = useState(true);

  const label = framework
    .replace("_", " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());

  const hasIndicators = Object.keys(output.indicators).length > 0;

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 4, marginBottom: 8 }}>
      <button
        onClick={() => setOpen((v) => !v)}
        style={{
          width: "100%",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "6px 10px",
          background: "#f5f5f5",
          border: "none",
          borderBottom: open ? "1px solid #ddd" : "none",
          cursor: "pointer",
          fontSize: 13,
          fontWeight: 600,
          borderRadius: open ? "4px 4px 0 0" : 4,
        }}
      >
        <span>{label}</span>
        <span style={{ color: "#888", fontWeight: 400 }}>
          {output.composite_score !== null
            ? `score: ${(parseFloat(output.composite_score) * 100).toFixed(0)}th pct`
            : "not implemented"}
          {" "}
          {open ? "▲" : "▼"}
        </span>
      </button>

      {open && (
        <div style={{ padding: "8px 10px" }}>
          {output.note && (
            <p style={{ fontSize: 12, color: "#888", fontStyle: "italic", margin: "0 0 8px" }}>
              {output.note}
            </p>
          )}

          {!hasIndicators && !output.note && (
            <p style={{ fontSize: 12, color: "#aaa", margin: 0 }}>No indicators available.</p>
          )}

          {hasIndicators && (
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
              <thead>
                <tr style={{ background: "#fafafa" }}>
                  <th style={{ padding: "3px 6px", textAlign: "left", fontSize: 11, color: "#666" }}>Indicator</th>
                  <th style={{ padding: "3px 6px", textAlign: "right", fontSize: 11, color: "#666" }}>Value</th>
                  <th style={{ padding: "3px 6px", textAlign: "left", fontSize: 11, color: "#666" }}>Unit</th>
                  <th style={{ padding: "3px 6px", textAlign: "center", fontSize: 11, color: "#666" }}>Tier</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(output.indicators).map(([key, value]) => {
                  if (isCohortBlock(value)) {
                    // Nested cohort block — render each indicator inside
                    return (
                      <CohortBlock key={key} cohortId={key} indicators={value} />
                    );
                  }
                  return <IndicatorRow key={key} name={key} qty={value as QuantitySchema} />;
                })}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}

function CohortBlock({
  cohortId,
  indicators,
}: {
  cohortId: string;
  indicators: Record<string, QuantitySchema>;
}) {
  const [expanded, setExpanded] = useState(false);

  return (
    <>
      <tr
        onClick={() => setExpanded((v) => !v)}
        style={{ cursor: "pointer", background: "#f9f9f9" }}
      >
        <td
          colSpan={4}
          style={{ padding: "3px 6px", fontSize: 11, color: "#555", fontStyle: "italic" }}
        >
          {expanded ? "▼" : "▶"} {cohortId}
        </td>
      </tr>
      {expanded &&
        Object.entries(indicators).map(([iKey, qty]) => (
          <tr key={iKey} style={{ background: "#fdfdfd" }}>
            <td style={{ padding: "3px 6px 3px 20px", fontFamily: "monospace", fontSize: 11, color: "#444" }}>
              {iKey}
            </td>
            <td style={{ padding: "3px 6px", textAlign: "right", fontFamily: "monospace", fontSize: 11 }}>
              {qty.value}
            </td>
            <td style={{ padding: "3px 6px", color: "#666", fontSize: 11 }}>{qty.unit}</td>
            <td style={{ padding: "3px 6px", textAlign: "center" }}>
              <TierBadge tier={qty.confidence_tier} />
            </td>
          </tr>
        ))}
    </>
  );
}
