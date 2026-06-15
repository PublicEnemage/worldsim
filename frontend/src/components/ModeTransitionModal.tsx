/**
 * ModeTransitionModal — confirmation dialog for explicit mode transitions.
 *
 * Shown when the user taps an inactive mode label in ModeSelector and the
 * current step is > 0. Names the preserved state (step position + entity
 * configuration) and the changed state (replay event annotations) per
 * G8b intent document §7.3 AC-3.
 *
 * Not full-screen. No backdrop or scroll lock — Gap 5 "single non-modal
 * confirmation" pattern.
 */

const TARGET_LABELS: Record<"MODE_1" | "MODE_2" | "MODE_3", string> = {
  MODE_1: "Replay",
  MODE_2: "Simulation",
  MODE_3: "Active Control",
};

interface ModeTransitionModalProps {
  targetMode: "MODE_1" | "MODE_2" | "MODE_3";
  currentStep: number;
  onConfirm: () => void;
  onCancel: () => void;
}

export function ModeTransitionModal({
  targetMode,
  currentStep,
  onConfirm,
  onCancel,
}: ModeTransitionModalProps) {
  const targetLabel = TARGET_LABELS[targetMode];

  return (
    <div
      data-testid="mode-transition-modal"
      style={{
        position: "absolute",
        top: "calc(100% + 6px)",
        left: 0,
        zIndex: 100,
        background: "#fff",
        border: "1px solid #ccc",
        borderRadius: 6,
        padding: "12px 14px",
        minWidth: 300,
        maxWidth: 360,
        boxShadow: "0 4px 12px rgba(0,0,0,0.12)",
        fontSize: 13,
        lineHeight: 1.5,
        color: "#333",
      }}
    >
      <p style={{ margin: "0 0 10px" }}>
        Switching to <strong>{targetLabel}</strong> mode. Your current{" "}
        <strong>step position</strong> (step {currentStep}) and{" "}
        <strong>entity configuration</strong> are preserved. Replay event
        annotations will not be shown in {targetLabel} mode.
      </p>
      <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
        <button
          data-testid="mode-transition-modal-cancel"
          onClick={onCancel}
          style={{
            padding: "4px 10px",
            fontSize: 12,
            border: "1px solid #ccc",
            borderRadius: 4,
            background: "#f5f5f5",
            cursor: "pointer",
          }}
        >
          Stay in Replay
        </button>
        <button
          data-testid="mode-transition-modal-confirm"
          onClick={onConfirm}
          style={{
            padding: "4px 10px",
            fontSize: 12,
            border: "1px solid #4f6ef7",
            borderRadius: 4,
            background: "#4f6ef7",
            color: "#fff",
            cursor: "pointer",
            fontWeight: 600,
          }}
        >
          Switch to {targetLabel}
        </button>
      </div>
    </div>
  );
}
