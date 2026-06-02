import { useState, useEffect } from "react";
import AttributeSelector from "./components/AttributeSelector";
import ChoroplethMap from "./components/ChoroplethMap";
import DeltaChoropleth from "./components/DeltaChoropleth";
import EntityDetailDrawer from "./components/EntityDetailDrawer";
import FidelityDashboard from "./components/FidelityDashboard";
import { ModeIndicator } from "./components/ModeIndicator";
import { ScenarioInstrumentCluster } from "./components/ScenarioInstrumentCluster";
import ScenarioControls from "./components/ScenarioControls";
import ScenarioPanel from "./components/ScenarioPanel";
import type { ScenarioDetailResponse } from "./types";
import "./App.css";

const API_BASE = "http://localhost:8000/api/v1";

const DEFAULT_ATTRIBUTE = "gdp_usd_millions";

// ---------------------------------------------------------------------------
// Persistent scenario state — IR-003
// ---------------------------------------------------------------------------

const LAST_SCENARIO_KEY = "worldsim_last_scenario";

interface StoredScenario {
  id: string;
  name: string;
  totalSteps: number;
}

function readStoredScenario(): StoredScenario | null {
  try {
    const raw = localStorage.getItem(LAST_SCENARIO_KEY);
    return raw ? (JSON.parse(raw) as StoredScenario) : null;
  } catch {
    return null;
  }
}

function writeStoredScenario(s: StoredScenario): void {
  try {
    localStorage.setItem(LAST_SCENARIO_KEY, JSON.stringify(s));
  } catch {
    // Non-fatal — private browsing or quota exceeded
  }
}

// Returns ?scenario= URL param value, or null if absent.
function getUrlScenarioId(): string | null {
  try {
    return new URLSearchParams(window.location.search).get("scenario");
  } catch {
    return null;
  }
}

export default function App() {
  const [attributeName, setAttributeName] = useState(DEFAULT_ATTRIBUTE);
  const [selectedScenarioId, setSelectedScenarioId] = useState<string | null>(null);
  const [selectedScenarioName, setSelectedScenarioName] = useState<string | null>(null);
  const [selectedScenarioSteps, setSelectedScenarioSteps] = useState<number>(3);
  const [currentStep, setCurrentStep] = useState<number | null>(null);
  const [compareMode, setCompareMode] = useState(false);
  const [secondScenarioId, setSecondScenarioId] = useState<string | null>(null);
  const [panelOpen, setPanelOpen] = useState(false);
  const [fidelityOpen, setFidelityOpen] = useState(false);
  const [selectedEntityId, setSelectedEntityId] = useState<string | null>(null);
  // Incremented on every advance — ScenarioPanel watches this to refresh the list.
  const [scenarioListVersion, setScenarioListVersion] = useState(0);

  const handleStepChange = (step: number, _isComplete: boolean) => {
    // Always set — never reset to null on completion so EntityDetailDrawer
    // continues showing data at the final step after the scenario is done.
    setCurrentStep(step);
    setScenarioListVersion((v) => v + 1);
  };

  const handleSelectScenario = (id: string, name: string, totalSteps: number) => {
    setSelectedScenarioId(id);
    setSelectedScenarioName(name);
    setSelectedScenarioSteps(totalSteps);
    setCurrentStep(null);
    setSelectedEntityId(null);
    writeStoredScenario({ id, name, totalSteps });
  };

  const handleEntityClick = (entityId: string) => {
    setSelectedEntityId(entityId);
  };

  // Restore last active scenario on mount (IR-003).
  // URL ?scenario= takes precedence; falls back to localStorage.
  // Non-fatal: if the stored ID no longer exists, clear stale localStorage silently.
  useEffect(() => {
    const urlId = getUrlScenarioId();
    const stored = readStoredScenario();
    const scenarioId = urlId ?? stored?.id ?? null;
    if (!scenarioId) return;

    let cancelled = false;
    fetch(`${API_BASE}/scenarios/${encodeURIComponent(scenarioId)}`)
      .then((res) => (res.ok ? (res.json() as Promise<ScenarioDetailResponse>) : null))
      .then((detail) => {
        if (cancelled || !detail) {
          if (!urlId) localStorage.removeItem(LAST_SCENARIO_KEY);
          return;
        }
        setSelectedScenarioId(detail.scenario_id);
        setSelectedScenarioName(detail.name);
        setSelectedScenarioSteps(detail.configuration.n_steps);
        // Fast-forward step if already completed — mirrors the existing completed-scenario effect.
        if (detail.status === "completed") {
          setCurrentStep(detail.configuration.n_steps);
        }
      })
      .catch(() => {
        if (!cancelled && !urlId) localStorage.removeItem(LAST_SCENARIO_KEY);
      });

    return () => {
      cancelled = true;
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps — intentionally runs once on mount

  // Playwright E2E test seam — DEV mode only, eliminated from production builds.
  // Exposes entity-selection handler so tests can open the drawer without clicking
  // on the WebGL canvas (unreliable in headless Chromium at map zoom levels).
  useEffect(() => {
    if (!import.meta.env.DEV) return;
    (window as unknown as Record<string, unknown>).__worldsim_selectEntity = (id: string) =>
      setSelectedEntityId(id);
    (window as unknown as Record<string, unknown>).__worldsim_setAttributeName = (key: string) =>
      setAttributeName(key);
  }, [setSelectedEntityId, setAttributeName]);

  // When a scenario is selected, check if it's already completed and fast-forward
  // currentStep to its final step — ScenarioControls won't emit onStepChange for
  // a scenario that was completed before this session.
  useEffect(() => {
    if (!selectedScenarioId) return;

    let cancelled = false;
    fetch(`${API_BASE}/scenarios/${encodeURIComponent(selectedScenarioId)}`)
      .then((res) => (res.ok ? (res.json() as Promise<ScenarioDetailResponse>) : null))
      .then((detail) => {
        if (cancelled || !detail) return;
        if (detail.status === "completed") {
          setCurrentStep(detail.configuration.n_steps);
        }
      })
      .catch(() => {
        // Non-fatal — currentStep stays at whatever handleSelectScenario set
      });

    return () => {
      cancelled = true;
    };
  }, [selectedScenarioId]);

  const showDelta = compareMode && selectedScenarioId !== null && secondScenarioId !== null;

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">WorldSim</h1>
        <AttributeSelector value={attributeName} onChange={setAttributeName} />
        <label style={{ marginLeft: 4, fontSize: 13 }}>
          <input
            type="checkbox"
            checked={compareMode}
            onChange={(e) => setCompareMode(e.target.checked)}
            style={{ marginRight: 4 }}
          />
          Compare scenarios
        </label>
        <button
          className={`scenario-toggle-btn${panelOpen ? " scenario-toggle-btn--open" : ""}`}
          onClick={() => { setPanelOpen((v) => !v); setFidelityOpen(false); }}
        >
          Scenarios {panelOpen ? "▲" : "▼"}
        </button>
        <button
          className={`scenario-toggle-btn${fidelityOpen ? " scenario-toggle-btn--open" : ""}`}
          onClick={() => { setFidelityOpen((v) => !v); setPanelOpen(false); }}
          data-testid="fidelity-toggle"
        >
          Fidelity {fidelityOpen ? "▲" : "▼"}
        </button>
        {selectedScenarioId && (
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            {selectedScenarioName && (
              <span style={{ fontSize: 13, opacity: 0.85, maxWidth: 160, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {selectedScenarioName}
              </span>
            )}
            <ModeIndicator />
            <ScenarioControls
              scenarioId={selectedScenarioId}
              totalSteps={selectedScenarioSteps}
              onStepChange={handleStepChange}
            />
          </div>
        )}
      </header>

      {panelOpen && (
        <ScenarioPanel
          selectedScenarioId={selectedScenarioId}
          secondScenarioId={secondScenarioId}
          onSelectScenario={handleSelectScenario}
          onSelectSecondScenario={setSecondScenarioId}
          refreshKey={scenarioListVersion}
        />
      )}

      {fidelityOpen && <FidelityDashboard />}

      <main className="app-main" style={{ position: "relative" }}>
        {/* Instrument cluster — primary viewport when a scenario is active (CLAUDE.md UX commitment 1) */}
        {selectedScenarioId && (
          <div style={{ overflowX: "auto", background: "#fafafa", borderBottom: "1px solid #e8e8e8" }}>
            <ScenarioInstrumentCluster
              scenarioId={selectedScenarioId}
              stepCount={selectedScenarioSteps}
              currentStep={currentStep ?? 0}
            />
          </div>
        )}

        {/* Context layer — choropleth map (navigable context per CLAUDE.md UX commitment 2) */}
        {showDelta ? (
          <DeltaChoropleth
            scenarioAId={selectedScenarioId}
            scenarioBId={secondScenarioId}
            attributeName={attributeName}
            title={attributeName}
          />
        ) : (
          <ChoroplethMap
            attributeName={attributeName}
            title={attributeName}
            scenarioId={selectedScenarioId}
            currentStep={currentStep}
            onEntityClick={selectedScenarioId ? handleEntityClick : undefined}
          />
        )}

        {selectedEntityId && selectedScenarioId && (
          <EntityDetailDrawer
            scenarioId={selectedScenarioId}
            entityId={selectedEntityId}
            step={currentStep ?? selectedScenarioSteps}
            onClose={() => setSelectedEntityId(null)}
          />
        )}
      </main>
    </div>
  );
}
