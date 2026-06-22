import { useState, useEffect, useCallback } from "react";
import DataQualityPreview from "./DataQualityPreview";
import type { ScenarioDetailResponse, ScenarioResponse } from "../types";

const API_BASE = "http://localhost:8000/api/v1";

// Entity name mapping for the searchable selector (M15-G4)
const ENTITY_NAMES: Record<string, string> = {
  GRC: "Greece", JOR: "Jordan", EGY: "Egypt", ZMB: "Zambia",
  SEN: "Senegal", GHA: "Ghana", KEN: "Kenya", ETH: "Ethiopia",
  TZA: "Tanzania", UGA: "Uganda", CMR: "Cameroon", CIV: "Côte d'Ivoire",
  MOZ: "Mozambique", ZWE: "Zimbabwe", PAK: "Pakistan", BGD: "Bangladesh",
  NPL: "Nepal", LKA: "Sri Lanka", MMR: "Myanmar", KHM: "Cambodia",
  LAO: "Laos", IDN: "Indonesia", PHL: "Philippines", VNM: "Vietnam",
  BRA: "Brazil", ARG: "Argentina", COL: "Colombia", PER: "Peru",
  ECU: "Ecuador", BOL: "Bolivia", PRY: "Paraguay", URY: "Uruguay",
  VEN: "Venezuela", LBN: "Lebanon", TUN: "Tunisia", MAR: "Morocco",
  DZA: "Algeria", SDN: "Sudan", YEM: "Yemen", IRQ: "Iraq",
  PSE: "Palestine",
};

const ALL_ENTITIES = Object.keys(ENTITY_NAMES);

interface Props {
  selectedScenarioId: string | null;
  secondScenarioId: string | null;
  onSelectScenario: (id: string, name: string, totalSteps: number) => void;
  onSelectSecondScenario: (id: string) => void;
  refreshKey?: number;
}

export default function ScenarioPanel({
  selectedScenarioId,
  secondScenarioId,
  onSelectScenario,
  onSelectSecondScenario,
  refreshKey,
}: Props) {
  const [scenarios, setScenarios] = useState<ScenarioResponse[]>([]);
  const [listError, setListError] = useState<string | null>(null);
  const [createName, setCreateName] = useState("");
  const [createEntity, setCreateEntity] = useState("GRC");
  const [entitySearch, setEntitySearch] = useState("GRC — Greece");
  const [entityDropdownOpen, setEntityDropdownOpen] = useState(false);
  const [createStartYear, setCreateStartYear] = useState(2020);
  const [createFiscalMultiplier, setCreateFiscalMultiplier] = useState(1.0);
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

  // eslint-disable-next-line react-hooks/set-state-in-effect
  useEffect(() => { void fetchScenarios(); }, [fetchScenarios, refreshKey]);

  const handleSelectPrimary = async (scenario: ScenarioResponse) => {
    // Call immediately so parent's selectedScenarioId updates synchronously —
    // prevents race when entity is selected right after clicking this button
    // before the detail fetch resolves.
    onSelectScenario(scenario.scenario_id, scenario.name, 3);
    try {
      const res = await fetch(
        `${API_BASE}/scenarios/${encodeURIComponent(scenario.scenario_id)}`
      );
      if (res.ok) {
        const detail = await res.json() as ScenarioDetailResponse;
        if (detail.configuration.n_steps !== 3) {
          onSelectScenario(scenario.scenario_id, scenario.name, detail.configuration.n_steps);
        }
      }
    } catch {
      // Fallback 3 already set above.
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
      const startDate = `${createStartYear}-01-01`;
      const res = await fetch(`${API_BASE}/scenarios`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          description: null,
          configuration: {
            entities: [createEntity],
            n_steps: 3,
            timestep_label: "annual",
            start_date: startDate,
            initial_attributes: {},
            fiscal_multiplier: createFiscalMultiplier,
          },
          scheduled_inputs: [],
        }),
      });

      if (res.ok) {
        setCreateSuccess(`"${name}" created.`);
        setCreateName("");
        setCreateStartYear(2020);
        setCreateFiscalMultiplier(1.0);
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

  const filteredEntities = ALL_ENTITIES.filter((code) => {
    const q = entitySearch.toUpperCase();
    return code.startsWith(q) || (ENTITY_NAMES[code] ?? "").toUpperCase().includes(q);
  }).slice(0, 10);

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
                    data-scenario-id={s.scenario_id}
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

            {/* Searchable entity selector (M15-G4) */}
            <div style={{ position: "relative" }}>
              <input
                className="scenario-create-input scenario-create-input--entity"
                data-testid="entity-selector"
                type="text"
                placeholder="Entity (e.g. ZMB, SEN)"
                value={entitySearch}
                onChange={(e) => {
                  setEntitySearch(e.target.value);
                  setEntityDropdownOpen(true);
                }}
                onFocus={() => setEntityDropdownOpen(true)}
                onBlur={() => setTimeout(() => setEntityDropdownOpen(false), 150)}
                disabled={creating}
                aria-label="Entity"
                autoComplete="off"
              />
              {entityDropdownOpen && entitySearch.length > 0 && (
                <div
                  style={{
                    position: "absolute",
                    top: "100%",
                    left: 0,
                    right: 0,
                    background: "#0f1f33",
                    border: "1px solid rgba(100,148,200,0.3)",
                    borderRadius: 4,
                    maxHeight: 160,
                    overflowY: "auto",
                    zIndex: 100,
                  }}
                >
                  {filteredEntities.map((code) => (
                    <div
                      key={code}
                      role="option"
                      data-testid={`entity-option-${code}`}
                      aria-selected={createEntity === code}
                      style={{
                        padding: "4px 8px",
                        fontSize: 12,
                        cursor: "pointer",
                        color: "#cbd5e1",
                        background: createEntity === code ? "rgba(59,130,246,0.15)" : "transparent",
                      }}
                      onMouseDown={() => {
                        setCreateEntity(code);
                        setEntitySearch(`${code} — ${ENTITY_NAMES[code] ?? code}`);
                        setEntityDropdownOpen(false);
                      }}
                    >
                      <span style={{ fontWeight: 700 }}>{code}</span>
                      {ENTITY_NAMES[code] ? ` — ${ENTITY_NAMES[code]}` : ""}
                    </div>
                  ))}
                  {filteredEntities.length === 0 && (
                    <div style={{ padding: "4px 8px", fontSize: 12, color: "#64748b" }}>
                      No matching entities
                    </div>
                  )}
                </div>
              )}
            </div>

            <input
              className="scenario-create-input scenario-create-input--year"
              type="number"
              aria-label="Start year"
              min={1900}
              max={2100}
              value={createStartYear}
              onChange={(e) => setCreateStartYear(Number(e.target.value))}
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
          <DataQualityPreview entityId={createEntity} year={createStartYear} />
          <div className="scenario-fiscal-multiplier" style={{ marginTop: 8 }}>
            <label style={{ fontSize: 12, display: "flex", alignItems: "center", gap: 8 }}>
              <span>Fiscal multiplier:</span>
              <input
                type="range"
                min={0.1}
                max={3.0}
                step={0.1}
                value={createFiscalMultiplier}
                onChange={(e) => setCreateFiscalMultiplier(parseFloat(e.target.value))}
                disabled={creating}
                style={{ flexGrow: 1 }}
                aria-label="Fiscal multiplier"
                data-testid="fiscal-multiplier-slider"
              />
              <span
                style={{
                  minWidth: 32,
                  fontFamily: "monospace",
                  color: createFiscalMultiplier !== 1.0 ? "#e67e22" : "#888",
                  fontWeight: createFiscalMultiplier !== 1.0 ? 600 : 400,
                }}
              >
                ×{createFiscalMultiplier.toFixed(1)}
              </span>
            </label>
            {createFiscalMultiplier !== 1.0 && (
              <div style={{ fontSize: 11, color: "#e67e22", marginTop: 2 }}>
                Mode 2 — fiscal multiplier override active
              </div>
            )}
          </div>
          {createSuccess && (
            <div className="scenario-panel-success">{createSuccess}</div>
          )}
          {createError && (
            <div className="scenario-panel-error">{createError}</div>
          )}
          <div className="scenario-create-hint">
            Creates a scenario with 3 annual steps starting at the given year. Fiscal
            multiplier 1.0 = standard; &gt;1.0 = expansionary amplification; &lt;1.0 = contractionary.
          </div>
        </div>
      </div>
    </div>
  );
}
