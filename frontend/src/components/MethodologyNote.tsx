import { useState } from "react";

interface MethodologyNoteProps {
  label: string;
  children: React.ReactNode;
}

// Zone 3A expandable — collapsed by default, accessible via (i).
// ADR-005 Amendment 3 Area 4: methodology notes are Zone 3 deliberate navigation.
// Same component will serve governance methodology note at M9 promotion.
export default function MethodologyNote({ label, children }: MethodologyNoteProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div style={{ marginTop: 8, borderTop: "1px solid #eee", paddingTop: 6 }}>
      <button
        onClick={() => setExpanded((v) => !v)}
        aria-expanded={expanded}
        style={{
          background: "none",
          border: "none",
          cursor: "pointer",
          fontSize: 11,
          color: "#888",
          padding: 0,
          display: "flex",
          alignItems: "center",
          gap: 4,
        }}
      >
        <span
          style={{
            display: "inline-flex",
            alignItems: "center",
            justifyContent: "center",
            width: 14,
            height: 14,
            borderRadius: "50%",
            border: "1px solid #aaa",
            fontSize: 10,
            color: "#888",
            flexShrink: 0,
          }}
        >
          i
        </span>
        <span>{label}</span>
        <span style={{ marginLeft: 2 }}>{expanded ? "▲" : "▼"}</span>
      </button>

      {expanded && (
        <div
          style={{
            marginTop: 6,
            fontSize: 11,
            color: "#666",
            lineHeight: 1.5,
          }}
        >
          {children}
        </div>
      )}
    </div>
  );
}
