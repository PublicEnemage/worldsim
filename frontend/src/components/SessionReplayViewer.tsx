/**
 * SessionReplayViewer — Pillar 1, M11.5 usability audit.
 *
 * Shown when ?replay_session=<id> is present in the URL.
 * Fetches the recording artifact from the backend and replays it using
 * rrweb's Replayer class in an iframe embedded in the page.
 *
 * Usage: http://localhost:5173/?replay_session=2026-06-04-persona-1-001
 */
import { useEffect, useRef, useState } from "react";
import { Replayer } from "rrweb";
import "rrweb/dist/style.css";

const API_BASE = "http://localhost:8000/api/v1";

interface SessionArtifact {
  session_id: string;
  schema_version: string;
  created_at: string;
  started_at: string;
  ended_at: string;
  metadata: {
    persona_id: string;
    canonical_use_case: string;
    viewport_width: number;
    viewport_height: number;
    app_version: string;
    git_commit: string;
  };
  events: object[];
  event_count: number;
  duration_ms: number;
}

export function SessionReplayViewer({ sessionId }: { sessionId: string }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const replayerRef = useRef<Replayer | null>(null);
  const [artifact, setArtifact] = useState<SessionArtifact | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/sessions/recording/${encodeURIComponent(sessionId)}`)
      .then((r) => {
        if (!r.ok) throw new Error(`Session '${sessionId}' not found (HTTP ${r.status})`);
        return r.json();
      })
      .then((data: SessionArtifact) => setArtifact(data))
      .catch((err: unknown) =>
        setError(err instanceof Error ? err.message : String(err))
      );
  }, [sessionId]);

  useEffect(() => {
    if (!artifact || !containerRef.current) return;
    const replayer = new Replayer(artifact.events as never[], {
      root: containerRef.current,
      speed: 1,
      showWarning: false,
      showDebug: false,
      skipInactive: true,
    });
    replayerRef.current = replayer;
    return () => {
      replayerRef.current = null;
    };
  }, [artifact]);

  const handlePlay = () => {
    replayerRef.current?.play();
    setIsPlaying(true);
  };

  const handlePause = () => {
    replayerRef.current?.pause();
    setIsPlaying(false);
  };

  if (error) {
    return (
      <div style={{ padding: 32, fontFamily: "monospace", color: "#c0392b" }}>
        <strong>Replay error:</strong> {error}
      </div>
    );
  }

  if (!artifact) {
    return (
      <div style={{ padding: 32, fontFamily: "monospace", color: "#666" }}>
        Loading session {sessionId}…
      </div>
    );
  }

  const durationSec = Math.round(artifact.duration_ms / 1000);

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", height: "100vh", display: "flex", flexDirection: "column" }}>
      {/* Header */}
      <div style={{ background: "#1a1a2e", color: "#e0e0e0", padding: "12px 20px", display: "flex", alignItems: "center", gap: 24, flexShrink: 0 }}>
        <span style={{ fontWeight: 700, fontSize: 14 }}>WorldSim Session Replay</span>
        <span style={{ fontSize: 12, color: "#9090c0" }}>
          {artifact.session_id} · {artifact.metadata.persona_id} · {artifact.metadata.canonical_use_case}
        </span>
        <span style={{ fontSize: 12, color: "#9090c0", marginLeft: "auto" }}>
          {artifact.event_count} events · {durationSec}s · {artifact.metadata.app_version}
        </span>
      </div>

      {/* Controls */}
      <div style={{ background: "#f0f0f0", padding: "8px 20px", display: "flex", gap: 12, alignItems: "center", flexShrink: 0 }}>
        {isPlaying ? (
          <button onClick={handlePause} style={btnStyle}>⏸ Pause</button>
        ) : (
          <button onClick={handlePlay} style={btnStyle}>▶ Play</button>
        )}
        <span style={{ fontSize: 12, color: "#666" }}>
          Recorded {new Date(artifact.created_at).toLocaleString()}
        </span>
      </div>

      {/* Replay container — rrweb injects an iframe here */}
      <div
        ref={containerRef}
        style={{ flex: 1, overflow: "hidden", background: "#222", position: "relative" }}
      />
    </div>
  );
}

const btnStyle: React.CSSProperties = {
  padding: "4px 14px",
  fontSize: 13,
  cursor: "pointer",
  background: "#1a1a2e",
  color: "#e0e0e0",
  border: "none",
  borderRadius: 4,
};
