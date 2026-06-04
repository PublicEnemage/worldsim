/**
 * SessionRecordingBanner — unobtrusive indicator shown during active usability sessions.
 *
 * Shows a subtle banner at the top of the viewport with the session ID and an
 * "End Session" button. Designed to be visible enough to confirm recording is
 * active without distracting from the usability task.
 */
import { useState } from "react";
import type { UseSessionRecordingResult } from "../hooks/useSessionRecording";

interface Props {
  recording: UseSessionRecordingResult;
}

export function SessionRecordingBanner({ recording }: Props) {
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);

  if (!recording.isRecording) return null;

  const handleEndSession = async () => {
    setSaving(true);
    const result = await recording.endSession();
    setSaving(false);
    if (result.ok) {
      setSaved(true);
    } else {
      setSaveError(result.error ?? "Unknown error");
    }
  };

  return (
    <div
      data-testid="session-recording-banner"
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        zIndex: 9999,
        background: saved ? "#27ae60" : "#c0392b",
        color: "#fff",
        fontSize: 12,
        padding: "4px 16px",
        display: "flex",
        alignItems: "center",
        gap: 12,
        fontFamily: "monospace",
      }}
    >
      {saved ? (
        <>
          <span>● Session saved: {recording.sessionId}</span>
          <span style={{ marginLeft: "auto", opacity: 0.8 }}>
            Artifact written to backend/sessions/ — you may close this tab.
          </span>
        </>
      ) : (
        <>
          <span>● Recording: {recording.sessionId}</span>
          {saveError && (
            <span style={{ color: "#ffd" }}>Save failed: {saveError}</span>
          )}
          <button
            onClick={handleEndSession}
            disabled={saving}
            data-testid="end-session-btn"
            style={{
              marginLeft: "auto",
              padding: "2px 12px",
              fontSize: 12,
              cursor: saving ? "wait" : "pointer",
              background: "rgba(255,255,255,0.2)",
              color: "#fff",
              border: "1px solid rgba(255,255,255,0.4)",
              borderRadius: 3,
              fontFamily: "monospace",
            }}
          >
            {saving ? "Saving…" : "End Session"}
          </button>
        </>
      )}
    </div>
  );
}
