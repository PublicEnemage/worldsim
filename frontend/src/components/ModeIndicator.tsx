/**
 * ModeIndicator — persistent header element showing current interaction mode.
 *
 * Renders human-readable mode labels (UX-RULING-3 / US-026):
 *   MODE_1 → "Replay"
 *   MODE_2 → "Simulation"
 *   MODE_3 → "Active Control"
 *
 * Subscribes to useScenarioStepStore. Updates within the same React render
 * cycle as any other Zone 1 instrument (DD-012, US-026 RTL test).
 */
import React from "react";
import { useScenarioStepStore } from "../store/scenarioStepStore";

// ---------------------------------------------------------------------------
// Exported pure functions (tested by ModeIndicator.test.ts)
// ---------------------------------------------------------------------------

export const MODE_LABELS: Record<"MODE_1" | "MODE_2" | "MODE_3", string> = {
  MODE_1: "Replay",
  MODE_2: "Simulation",
  MODE_3: "Active Control",
};

/**
 * Returns the human-readable mode label. UX-RULING-3 / US-026.
 * Never returns raw field name strings ("MODE_1", "MODE_2", "MODE_3").
 */
export function getModeLabel(mode: "MODE_1" | "MODE_2" | "MODE_3"): string {
  return MODE_LABELS[mode];
}

// ---------------------------------------------------------------------------
// ModeIndicator
// ---------------------------------------------------------------------------

interface ModeIndicatorProps {
  "data-testid"?: string;
}

export function ModeIndicator({
  "data-testid": dataTestId = "mode-indicator",
}: ModeIndicatorProps) {
  const { mode } = useScenarioStepStore();

  return (
    <span
      data-testid={dataTestId}
      data-mode={mode}
      style={{
        fontSize: 12,
        fontWeight: 600,
        letterSpacing: 0.3,
        color: "#444",
        padding: "2px 6px",
        borderRadius: 3,
        background: "#f4f4f4",
        border: "1px solid #ddd",
      }}
    >
      {getModeLabel(mode)}
    </span>
  );
}
