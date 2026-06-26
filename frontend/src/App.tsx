import { useState, useEffect } from "react";
import AttributeSelector from "./components/AttributeSelector";
import ChoroplethMap from "./components/ChoroplethMap";
import DeltaChoropleth from "./components/DeltaChoropleth";
import EntityDetailDrawer from "./components/EntityDetailDrawer";
import FidelityDashboard from "./components/FidelityDashboard";
import GroundingStrip from "./components/GroundingStrip";
import { ModeSelector } from "./components/ModeSelector";
import ScenarioParameters from "./components/ScenarioParameters";
import { AssumptionSurface } from "./components/AssumptionSurface";
import { ScenarioIdentityHeader } from "./components/ScenarioIdentityHeader";
import { ScenarioInstrumentCluster } from "./components/ScenarioInstrumentCluster";
import ScenarioControls from "./components/ScenarioControls";
import ScenarioPanel from "./components/ScenarioPanel";
import { SessionRecordingBanner } from "./components/SessionRecordingBanner";
import { SessionReplayViewer } from "./components/SessionReplayViewer";
import { useSessionRecording } from "./hooks/useSessionRecording";
import type { ScenarioDetailResponse } from "./types";
import { type ScenarioComparisonConfig } from "./components/TrajectoryView";
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

// Returns [idA, idB] from ?compare=idA,idB, or null if absent or malformed.
function getUrlCompareIds(): [string, string] | null {
  try {
    const val = new URLSearchParams(window.location.search).get("compare");
    if (!val) return null;
    const parts = val.split(",");
    if (parts.length !== 2 || !parts[0] || !parts[1]) return null;
    return [parts[0].trim(), parts[1].trim()];
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

  const [attributeName, setAttributeName] = useState(DEFAULT_ATTRIBUTE);
  const [selectedScenarioId, setSelectedScenarioId] = useState<string | null>(null);
  const [selectedScenarioName, setSelectedScenarioName] = useState<string | null>(null);
  const [selectedScenarioSteps, setSelectedScenarioSteps] = useState<number>(3);
  const [currentStep, setCurrentStep] = useState<number | null>(null);
  const [compareMode, setCompareMode] = useState(false);
  const [secondScenarioId, setSecondScenarioId] = useState<string | null>(null);
  const [panelOpen, setPanelOpen] = useState(false);
  const [fidelityOpen, setFidelityOpen] = useState(false);
  const [groundingOpen, setGroundingOpen] = useState(false);
  const [paramsOpen, setParamsOpen] = useState(false);
  const [activeScenarioDetail, setActiveScenarioDetail] = useState<ScenarioDetailResponse | null>(null);
  const [selectedEntityId, setSelectedEntityId] = useState<string | null>(null);
  // All active entities for the scenario — used by ScenarioIdentityHeader and choropleth highlight (#754)
  const [activeEntityIds, setActiveEntityIds] = useState<string[]>([]);
  // Incremented on every advance — ScenarioPanel watches this to refresh the list.
  const [scenarioListVersion, setScenarioListVersion] = useState(0);
  // Mode 2 fiscal multiplier for the active scenario (Issue #746)
  const [activeFiscalMultiplier, setActiveFiscalMultiplier] = useState<number | null>(null);
  // Mode 3 Active Control toggle (G6b, Issue #753)
  const [mode3Active, setMode3Active] = useState(false);
  // M17-G2 — N>2 scenario comparison configs (IDs + palette; trajectories fetched by cluster)
  const [comparisonScenarios, setComparisonScenarios] = useState<ScenarioComparisonConfig[]>([]);

  const handleStepChange = (step: number) => {
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
    setActiveScenarioDetail(null);
    setParamsOpen(false);
    writeStoredScenario({ id, name, totalSteps });
  };

  const handleEntityClick = (entityId: string) => {
    setSelectedEntityId(entityId);
  };

  // Restore last active scenario on mount (IR-003).
  // ?compare=idA,idB takes precedence over ?scenario= for E2E comparison mode (M16-G4 AC-F9).
  // ?scenario= takes precedence over localStorage.
  // Non-fatal: if the stored ID no longer exists, clear stale localStorage silently.
  useEffect(() => {
    const compareIds = getUrlCompareIds();
    if (compareIds) {
      // Comparison mode from URL — load scenario A as primary, B as comparison.
      const [idA, idB] = compareIds;
      setCompareMode(true);
      setSecondScenarioId(idB);
      let cancelled = false;
      fetch(`${API_BASE}/scenarios/${encodeURIComponent(idA)}`)
        .then((res) => (res.ok ? (res.json() as Promise<ScenarioDetailResponse>) : null))
        .then((detail) => {
          if (cancelled || !detail) return;
          setSelectedScenarioId(detail.scenario_id);
          setSelectedScenarioName(detail.name);
          setSelectedScenarioSteps(detail.configuration.n_steps);
          if (detail.status === "completed") {
            setCurrentStep(detail.configuration.n_steps);
          }
        })
        .catch(() => {});
      return () => { cancelled = true; };
    }

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
  }, []);

  // Playwright E2E test seam — DEV mode only, eliminated from production builds.
  // Exposes entity-selection handler so tests can open the drawer without clicking
  // on the WebGL canvas (unreliable in headless Chromium at map zoom levels).
  useEffect(() => {
    if (!import.meta.env.DEV) return;
    (window as unknown as Record<string, unknown>).__worldsim_selectEntity = (id: string) =>
      setSelectedEntityId(id);
    (window as unknown as Record<string, unknown>).__worldsim_setAttributeName = (key: string) =>
      setAttributeName(key);
    // M17-G2 — inject N>2 comparison scenario configs for E2E test seam (AC-S1).
    (window as unknown as Record<string, unknown>).__worldsim_setComparisonScenarios = (
      configs: ScenarioComparisonConfig[],
    ) => setComparisonScenarios(configs);
  }, [setSelectedEntityId, setAttributeName]);

  // When a scenario is selected: fast-forward currentStep if already completed,
  // and extract the primary entity for the identity header + choropleth highlight (#744).
  // Also stores the full detail for the ScenarioParameters panel (ADR-016 Component 4).
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
        // Store full detail for ScenarioParameters panel (ADR-016 Component 4)
        setActiveScenarioDetail(detail);
      })
      .catch(() => {
        // Non-fatal — currentStep and activeEntityId stay at previous values
      });

    return () => {
      cancelled = true;
    };
  }, [selectedScenarioId]);

  // Replay mode early return — placed after all hooks so rules-of-hooks is satisfied.
  const replaySessionId = new URLSearchParams(window.location.search).get("replay_session");
  if (replaySessionId) {
    return <SessionReplayViewer sessionId={replaySessionId} />;
  }

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
          onClick={() => { setPanelOpen((v) => !v); setFidelityOpen(false); setGroundingOpen(false); setParamsOpen(false); }}
        >
          Scenarios {panelOpen ? "▲" : "▼"}
        </button>
        <button
          className={`scenario-toggle-btn${fidelityOpen ? " scenario-toggle-btn--open" : ""}`}
          onClick={() => { setFidelityOpen((v) => !v); setPanelOpen(false); setGroundingOpen(false); setParamsOpen(false); }}
          data-testid="fidelity-toggle"
        >
          Fidelity {fidelityOpen ? "▲" : "▼"}
        </button>
        {selectedScenarioId && (
          <>
            <button
              data-testid="grounding-strip-toggle"
              onClick={() => { setGroundingOpen((v) => !v); setPanelOpen(false); setFidelityOpen(false); setParamsOpen(false); }}
              style={{
                padding: "4px 10px",
                fontSize: 13,
                background: groundingOpen ? "rgba(255,255,255,0.25)" : "rgba(255,255,255,0.15)",
                color: "#fff",
                border: "none",
                borderRadius: 4,
                cursor: "pointer",
                fontWeight: groundingOpen ? 600 : 400,
              }}
            >
              Grounding {groundingOpen ? "▲" : "▼"}
            </button>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              {selectedScenarioName && (
                <span style={{ fontSize: 13, opacity: 0.85, maxWidth: 160, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {selectedScenarioName}
                </span>
              )}
              {/* ModeSelector wrapper click opens parameter persistence panel (ADR-016 Component 4) */}
              <ModeSelector
                onWrapperClick={() => { setParamsOpen((v) => !v); setGroundingOpen(false); setPanelOpen(false); setFidelityOpen(false); }}
              />
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
                initialStep={currentStep ?? 0}
                onStepChange={handleStepChange}
              />
            </div>
          </>
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

      {fidelityOpen && <FidelityDashboard scenarioId={selectedScenarioId} />}

      {groundingOpen && selectedScenarioId && (
        <GroundingStrip scenarioId={selectedScenarioId} />
      )}

      {paramsOpen && <ScenarioParameters detail={activeScenarioDetail} />}

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

        {/* ADR-015 §Component 2 — Assumption surface strip (between Zone 0 and Zone 1) */}
        {selectedScenarioId && (
          <AssumptionSurface detail={activeScenarioDetail} />
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
              entityIds={activeEntityIds}
              activeScenarioDetail={activeScenarioDetail}
              comparisonScenarios={comparisonScenarios.length > 0 ? comparisonScenarios : undefined}
            />
          </div>
        )}

        {/* Context layer — choropleth map (navigable context per CLAUDE.md UX commitment 2) */}
        {/* IC-6 reference header rendered inside ChoroplethMap (ADR-016 §EL Decision 5) */}
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
