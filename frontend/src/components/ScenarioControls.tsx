import { useState, useEffect } from "react";
import type { AdvanceResponse } from "../types";

const API_BASE = "http://localhost:8000/api/v1";

interface Props {
  scenarioId: string;
  totalSteps: number;
  onStepChange: (step: number, isComplete: boolean) => void;
  initialStep?: number;
  initialComplete?: boolean;
}

export default function ScenarioControls({ scenarioId, totalSteps, onStepChange, initialStep = 0, initialComplete = false }: Props) {
  const [currentStep, setCurrentStep] = useState(initialStep);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isComplete, setIsComplete] = useState(initialComplete);

  useEffect(() => {
    setCurrentStep(initialStep);
    setIsComplete(initialComplete);
  }, [initialStep, initialComplete]);

  const advance = async () => {
    if (isComplete || loading) return;
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_BASE}/scenarios/${encodeURIComponent(scenarioId)}/advance`, {
        method: "POST",
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        setError(body?.detail ?? `Error ${res.status} advancing scenario.`);
        return;
      }

      const data: AdvanceResponse = await res.json();
      setCurrentStep(data.step_executed);
      setIsComplete(data.is_complete);
      onStepChange(data.step_executed, data.is_complete);
    } catch {
      setError("Network error — could not advance scenario.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", alignItems: "center", gap: 12, fontSize: 14 }}>
      <span style={{ fontWeight: 600 }}>
        Step {currentStep} / {totalSteps}
        {isComplete && " — Complete"}
      </span>

      <button
        onClick={advance}
        disabled={loading || isComplete}
        style={{
          padding: "4px 12px",
          cursor: loading || isComplete ? "not-allowed" : "pointer",
          opacity: loading || isComplete ? 0.5 : 1,
        }}
      >
        {loading ? "Advancing…" : "Next Step ▶"}
      </button>

      <button
        disabled
        title="Reset coming in M4"
        style={{ padding: "4px 12px", cursor: "not-allowed", opacity: 0.4 }}
      >
        ↺ Reset
      </button>

      {error && (
        <span style={{ color: "#c00", marginLeft: 8 }}>{error}</span>
      )}
    </div>
  );
}
