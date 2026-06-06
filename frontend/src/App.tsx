import { useState, useEffect } from "react";
import AttributeSelector from "./components/AttributeSelector";
import ChoroplethMap from "./components/ChoroplethMap";
import DeltaChoropleth from "./components/DeltaChoropleth";
import EntityDetailDrawer from "./components/EntityDetailDrawer";
import FidelityDashboard from "./components/FidelityDashboard";
import { ModeIndicator } from "./components/ModeIndicator";
import { ScenarioIdentityHeader } from "./components/ScenarioIdentityHeader";
import { ScenarioInstrumentCluster } from "./components/ScenarioInstrumentCluster";
import ScenarioControls from "./components/ScenarioControls";
import ScenarioPanel from "./components/ScenarioPanel";
import { SessionRecordingBanner } from "./components/SessionRecordingBanner";
import { SessionReplayViewer } from "./components/SessionReplayViewer";
import { useSessionRecording } from "./hooks/useSessionRecording";
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
  // ---------------------------------------------------------------------------
  // Pillar 1 — M11.5 usability session recording
  // Active only when ?usability_session=<id> is in the URL. Off by default.
  // ---------------------------------------------------------------------------
  const sessionRecording = useSessionRecording();

  // ---------------------------------------------------------------------------
  // Pillar 1 — replay mode
  // When ?replay_session=<id> is in the URL, show the replay viewer instead
  // of the main application. This is a developer/audit tool, not a user feature.
  // ---------------------------------------------------------------------------
  const replaySessionId = new URLSearchParams(window.location.search).get("replay_session");
  if (replaySessionId) {
    return <SessionReplayViewer sessionId={replaySessionId} />;
  }

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
  // All active entities for the scenario — used by ScenarioIdentityHeader and choropleth highlight (#754)
  const [activeEntityIds, setActiveEntityIds] = useState<string[]>([]);
  // Incremented on every advance — ScenarioPanel watches this to refresh the list.
  const [scenarioListVersion, setScenarioListVersion] = useState(0);
  // Mode 2 fiscal multiplier for the active scenario (Issue #746)
  const [activeFiscalMultiplier, setActiveFiscalMultiplier] = useState<number | null>(null);
  // Mode 3 Active Control toggle (G6b, Issue #753)
  const [mode3Active, setMode3Active] = useState(false);

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
    setActiveEntityIds([]);
    setActiveFiscalMultiplier(null);
    setMode3Active(false);
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

  // When a scenario is selected: fast-forward currentStep if already completed,
  // and extract the primary entity for the identity header + choropleth highlight (#744).
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
        // Set all active entities for identity header and choropleth highlight (#754)
        setActiveEntityIds(detail.configuration.entities ?? []);
        // Extract fiscal multiplier for Mode 2 display (Issue #746)
        setActiveFiscalMultiplier(detail.configuration.fiscal_multiplier ?? null);
      })
      .catch(() => {
        // Non-fatal — currentStep and activeEntityId stay at previous values
      });

    return () => {
      cancelled = true;
    };
  }, [selectedScenarioId]);

  const showDelta = compareMode && selectedScenarioId !== null && secondScenarioId !== null;

  return (
    <div className="app">
      <SessionRecordingBanner recording={sessionRecording} />
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
            <button
              data-testid="mode3-toggle"
              onClick={() => setMode3Active((v) => !v)}
              style={{
                fontSize: 11,
                padding: "3px 8px",
                background: mode3Active ? "#8b5cf6" : "transparent",
                color: mode3Active ? "#fff" : "#8b5cf6",
                border: "1px solid #8b5cf6",
                borderRadius: 4,
                cursor: "pointer",
                fontWeight: 600,
              }}
            >
              Mode 3
            </button>
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
        {/* Scenario identity header — always visible when scenario active (Issue #744, GAP-02) */}
        {selectedScenarioId && selectedScenarioName && (
          <ScenarioIdentityHeader
            scenarioName={selectedScenarioName}
            entityIds={activeEntityIds}
            currentStep={currentStep}
            totalSteps={selectedScenarioSteps}
            fiscalMultiplier={activeFiscalMultiplier}
          />
        )}

        {/* Instrument cluster — primary viewport when a scenario is active (CLAUDE.md UX commitment 1) */}
        {selectedScenarioId && (
          <div style={{ overflowX: "auto", background: "#fafafa", borderBottom: "1px solid #e8e8e8" }}>
            <ScenarioInstrumentCluster
              scenarioId={selectedScenarioId}
              stepCount={selectedScenarioSteps}
              currentStep={currentStep ?? 0}
              comparisonScenarioId={compareMode ? secondScenarioId : null}
              fiscalMultiplier={activeFiscalMultiplier}
              mode3Active={mode3Active}
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
            activeEntityIds={activeEntityIds}
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
