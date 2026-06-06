/**
 * useSessionRecording — Pillar 1, M11.5 usability audit.
 *
 * Recording is OFF by default. It activates only when the URL contains
 * ?usability_session=<id>, which the session coordinator sets before handing
 * the URL to the agent. This prevents any accidental capture during normal use.
 *
 * URL params:
 *   usability_session  — session ID (required to activate recording)
 *   persona            — persona ID, e.g. "persona-1" (optional metadata)
 *   use_case           — canonical use case label (optional metadata)
 *
 * Example URL:
 *   http://localhost:5173/?usability_session=2026-06-04-persona-1-001&persona=persona-1&use_case=IMF+loan+evaluation
 */
import { useEffect, useRef, useCallback } from "react";
import { record } from "rrweb";

const API_BASE = "http://localhost:8000/api/v1";

export interface SessionConfig {
  sessionId: string;
  personaId: string;
  canonicalUseCase: string;
}

export interface UseSessionRecordingResult {
  isRecording: boolean;
  sessionId: string | null;
  endSession: () => Promise<{ ok: boolean; error?: string }>;
}

function parseSessionParams(): SessionConfig | null {
  const params = new URLSearchParams(window.location.search);
  const sessionId = params.get("usability_session");
  if (!sessionId) return null;
  return {
    sessionId,
    personaId: params.get("persona") ?? "unknown",
    canonicalUseCase: params.get("use_case") ?? "unknown",
  };
}

export function useSessionRecording(): UseSessionRecordingResult {
  const config = parseSessionParams();
  const isRecording = config !== null;

  const eventsRef = useRef<object[]>([]);
  const startedAtRef = useRef<string>(new Date().toISOString());
  const stopFnRef = useRef<(() => void) | undefined>(undefined);
  const savedRef = useRef(false);

  useEffect(() => {
    if (!config) return;

    startedAtRef.current = new Date().toISOString();
    eventsRef.current = [];
    savedRef.current = false;

    const stopFn = record({
      emit(event) {
        eventsRef.current.push(event as object);
      },
    });
    stopFnRef.current = stopFn ?? undefined;

    return () => {
      stopFnRef.current?.();
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const endSession = useCallback(async (): Promise<{ ok: boolean; error?: string }> => {
    if (!config) return { ok: false, error: "No active recording session." };
    if (savedRef.current) return { ok: false, error: "Session already saved." };

    stopFnRef.current?.();
    savedRef.current = true;

    const endedAt = new Date().toISOString();
    const startedAt = startedAtRef.current;
    const events = eventsRef.current;
    const durationMs = new Date(endedAt).getTime() - new Date(startedAt).getTime();

    try {
      const resp = await fetch(`${API_BASE}/sessions/recording`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: config.sessionId,
          started_at: startedAt,
          ended_at: endedAt,
          metadata: {
            app_version: "v0.11.0",
            git_commit: "unknown",
            persona_id: config.personaId,
            canonical_use_case: config.canonicalUseCase,
            cold_start: true,
            viewport_width: window.innerWidth,
            viewport_height: window.innerHeight,
            user_agent: navigator.userAgent,
          },
          events,
          event_count: events.length,
          duration_ms: durationMs,
        }),
      });
      if (!resp.ok) {
        const detail = await resp.json().catch(() => ({}));
        return { ok: false, error: (detail as { detail?: string }).detail ?? `HTTP ${resp.status}` };
      }
      return { ok: true };
    } catch (err) {
      return { ok: false, error: err instanceof Error ? err.message : String(err) };
    }
  }, [config]);

  return { isRecording, sessionId: config?.sessionId ?? null, endSession };
}
