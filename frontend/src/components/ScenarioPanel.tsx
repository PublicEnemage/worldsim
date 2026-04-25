import { useState, useEffect, useCallback } from "react";
import type { ScenarioDetailResponse, ScenarioResponse } from "../types";

const API_BASE = "http://localhost:8000/api/v1";

interface Props {
  selectedScenarioId: string | null;
  secondScenarioId: string | null;
  onSelectScenario: (id: string, name: string, totalSteps: number) => void;
  onSelectSecondScenario: (id: string) => void;
}

export default function ScenarioPanel({
  selectedScenarioId,
  secondScenarioId,
  onSelectScenario,
  onSelectSecondScenario,
}: Props) {
  const [scenarios, setScenarios] = useState<ScenarioResponse[]>([]);
  const [listError, setListError] = useState<string | null>(null);
  const [createName, setCreateName] = useState("");
  const [creating, setCreating] = useState(false);
  const [createSuccess, setCreateSuccess] = useState<string | null>(null);
  const [createError, setCreateError] = useState<string | null>(null);

  const fetchScenarios = useCallback(async () => {
    setListError(null);
    try {
      const res = await fetch(`${API_BASE}/scenarios`);
      if (res.ok) {
        setScenarios(await res.json() as ScenarioResponse[]);
      } else {
        setListError(`Could not load scenarios (${res.status}).`);
      }
    } catch {
      setListError("Network error — could not load scenarios.");
    }
  }, []);

  useEffect(() => { void fetchScenarios(); }, [fetchScenarios]);

  const handleSelectPrimary = async (scenario: ScenarioResponse) => {
    try {
      const res = await fetch(
        `${API_BASE}/scenarios/${encodeURIComponent(scenario.scenario_id)}`
      );
      if (res.ok) {
        const detail = await res.json() as ScenarioDetailResponse;
        onSelectScenario(scenario.scenario_id, scenario.name, detail.configuration.n_steps);
      } else {
        onSelectScenario(scenario.scenario_id, scenario.name, 3);
      }
    } catch {
      onSelectScenario(scenario.scenario_id, scenario.name, 3);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    const name = createName.trim();
    if (!name) return;
    setCreating(true);
    setCreateError(null);
    setCreateSuccess(null);

    try {
      const res = await fetch(`${API_BASE}/scenarios`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          description: null,
          configuration: {
            entities: ["GRC"],
            n_steps: 3,
            timestep_label: "annual",
            initial_attributes: {},
          },
          scheduled_inputs: [],
        }),
      });

      if (res.ok) {
        setCreateSuccess(`"${name}" created.`);
        setCreateName("");
        void fetchScenarios();
      } else {
        const body = await res.json().catch(() => ({})) as { detail?: string };
        setCreateError(body?.detail ?? `Error ${res.status}.`);
      }
    } catch {
      setCreateError("Network error — could not create scenario.");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="scenario-panel">
      <div className="scenario-panel-inner">
        {/* Scenario list */}
        <div className="scenario-panel-section">
          <div className="scenario-panel-section-title">
            Scenarios
            <button
              className="scenario-panel-refresh"
              onClick={() => void fetchScenarios()}
              title="Refresh list"
            >
              ↻
            </button>
          </div>

          {listError && (
            <div className="scenario-panel-error">{listError}</div>
          )}

          {scenarios.length === 0 && !listError && (
            <div className="scenario-panel-empty">No scenarios yet — create one below.</div>
          )}

          {scenarios.length > 0 && (
            <div className="scenario-list">
              {scenarios.map((s) => {
                const isPrimary = s.scenario_id === selectedScenarioId;
                const isSecond = s.scenario_id === secondScenarioId;
                return (
                  <div
                    key={s.scenario_id}
                    className={`scenario-row${isPrimary ? " scenario-row--primary" : ""}${isSecond ? " scenario-row--second" : ""}`}
                  >
                    <div className="scenario-row-info">
                      <span className="scenario-row-name">{s.name}</span>
                      <span className={`scenario-row-status scenario-row-status--${s.status}`}>
                        {s.status}
                      </span>
                    </div>
                    <div className="scenario-row-actions">
                      <button
                        className={`scenario-btn${isPrimary ? " scenario-btn--active" : ""}`}
                        onClick={() => void handleSelectPrimary(s)}
                        title="Select as primary scenario"
                      >
                        {isPrimary ? "✓ Primary" : "Select"}
                      </button>
                      <button
                        className={`scenario-btn scenario-btn--compare${isSecond ? " scenario-btn--active" : ""}`}
                        onClick={() => onSelectSecondScenario(s.scenario_id)}
                        title="Select as comparison scenario"
                      >
                        {isSecond ? "✓ Compare" : "+ Compare"}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Create form */}
        <div className="scenario-panel-section scenario-panel-section--create">
          <div className="scenario-panel-section-title">New Scenario</div>
          <form className="scenario-create-form" onSubmit={(e) => void handleCreate(e)}>
            <input
              className="scenario-create-input"
              type="text"
              placeholder="Scenario name"
              value={createName}
              onChange={(e) => {
                setCreateName(e.target.value);
                setCreateSuccess(null);
                setCreateError(null);
              }}
              disabled={creating}
            />
            <button
              className="scenario-btn scenario-btn--create"
              type="submit"
              disabled={creating || !createName.trim()}
            >
              {creating ? "Creating…" : "Create"}
            </button>
          </form>
          {createSuccess && (
            <div className="scenario-panel-success">{createSuccess}</div>
          )}
          {createError && (
            <div className="scenario-panel-error">{createError}</div>
          )}
          <div className="scenario-create-hint">
            Creates a GRC scenario with 3 annual steps.
          </div>
        </div>
      </div>
    </div>
  );
}
