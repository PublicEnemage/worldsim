/**
 * ModeSelector — interactive mode selector replacing ModeIndicator in App.tsx.
 *
 * Three clickable labels: Replay | Simulation | Active Control.
 * Active mode label tap is a no-op. Inactive label tap:
 *   - At current_step === 0: direct setMode call, no modal.
 *   - At current_step > 0: ModeTransitionModal confirms before mode changes (SF-2 guard).
 *
 * data-testid="mode-indicator" and data-mode on the outer container are
 * retained for backward compatibility with existing tests (US-026, atomicity-rtl).
 *
 * Design authority: G8b intent document §7.2; Gap 5 of
 * worldsim-ux-architecture-first-principles-depth.md.
 */
import { useState } from "react";
import { useScenarioStepStore } from "../store/scenarioStepStore";
import { getModeLabel } from "./ModeIndicator";
import { ModeTransitionModal } from "./ModeTransitionModal";

type Mode = "MODE_1" | "MODE_2" | "MODE_3";
const MODES: Mode[] = ["MODE_1", "MODE_2", "MODE_3"];

export function ModeSelector() {
  const { mode, current_step, setMode } = useScenarioStepStore();
  const [pendingMode, setPendingMode] = useState<Mode | null>(null);

  function handleLabelClick(target: Mode) {
    if (target === mode) return;
    if (current_step > 0) {
      setPendingMode(target);
    } else {
      setMode(target);
    }
  }

  function handleConfirm() {
    if (pendingMode) {
      setMode(pendingMode);
      setPendingMode(null);
    }
  }

  function handleCancel() {
    setPendingMode(null);
  }

  return (
    <div
      data-testid="mode-indicator"
      data-mode={mode}
      style={{ position: "relative", display: "inline-flex", gap: 2 }}
    >
      {MODES.map((m) => {
        const isActive = m === mode;
        return (
          <span
            key={m}
            data-testid={`mode-selector-label-${m}`}
            onClick={() => handleLabelClick(m)}
            style={{
              fontSize: 12,
              fontWeight: 600,
              letterSpacing: 0.3,
              padding: "2px 8px",
              borderRadius: 3,
              cursor: isActive ? "default" : "pointer",
              background: isActive ? "#4f6ef7" : "#f4f4f4",
              color: isActive ? "#fff" : "#666",
              border: isActive ? "1px solid #4f6ef7" : "1px solid #ddd",
              userSelect: "none",
              transition: "background 0.1s",
            }}
          >
            {getModeLabel(m)}
          </span>
        );
      })}
      {pendingMode && (
        <ModeTransitionModal
          targetMode={pendingMode}
          currentStep={current_step}
          onConfirm={handleConfirm}
          onCancel={handleCancel}
        />
      )}
    </div>
  );
}
