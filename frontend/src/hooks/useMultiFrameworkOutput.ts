import { useEffect, useState } from "react";
import type { MultiFrameworkOutput } from "../types";

const API_BASE = "http://localhost:8000/api/v1";

interface State {
  data: MultiFrameworkOutput | null;
  loading: boolean;
  error: string | null;
}

/**
 * Fetches MultiFrameworkOutput for a (scenarioId, entityId, step) triple.
 * Re-fetches whenever any of the three keys change.
 * Returns null data while loading or if any key is null.
 */
export function useMultiFrameworkOutput(
  scenarioId: string | null,
  entityId: string | null,
  step: number | null,
): State {
  const [state, setState] = useState<State>({ data: null, loading: false, error: null });

  useEffect(() => {
    if (!scenarioId || !entityId || step === null) {
      setState({ data: null, loading: false, error: null });
      return;
    }

    let cancelled = false;
    setState({ data: null, loading: true, error: null });

    const url =
      `${API_BASE}/scenarios/${encodeURIComponent(scenarioId)}/measurement-output` +
      `?step=${step}&entity_id=${encodeURIComponent(entityId)}`;

    fetch(url)
      .then((res) => {
        if (!res.ok) {
          return res.json().catch(() => ({})).then((body) => {
            throw new Error(body?.detail ?? `HTTP ${res.status}`);
          });
        }
        return res.json() as Promise<MultiFrameworkOutput>;
      })
      .then((data) => {
        if (!cancelled) setState({ data, loading: false, error: null });
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setState({
            data: null,
            loading: false,
            error: err instanceof Error ? err.message : "Unexpected error",
          });
        }
      });

    return () => {
      cancelled = true;
    };
  }, [scenarioId, entityId, step]);

  return state;
}
