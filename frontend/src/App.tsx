import { useState, useEffect } from "react";
import AttributeSelector from "./components/AttributeSelector";
import ChoroplethMap from "./components/ChoroplethMap";
import DeltaChoropleth from "./components/DeltaChoropleth";
import EntityDetailDrawer from "./components/EntityDetailDrawer";
import ScenarioControls from "./components/ScenarioControls";
import ScenarioPanel from "./components/ScenarioPanel";
import type { ScenarioDetailResponse } from "./types";
import "./App.css";

const API_BASE = "http://localhost:8000/api/v1";

const DEFAULT_ATTRIBUTE = "population_total";

export default function App() {
  const [attributeName, setAttributeName] = useState(DEFAULT_ATTRIBUTE);
  const [selectedScenarioId, setSelectedScenarioId] = useState<string | null>(null);
  const [selectedScenarioName, setSelectedScenarioName] = useState<string | null>(null);
  const [selectedScenarioSteps, setSelectedScenarioSteps] = useState<number>(3);
  const [currentStep, setCurrentStep] = useState<number | null>(null);
  const [isAlreadyComplete, setIsAlreadyComplete] = useState(false);
  const [compareMode, setCompareMode] = useState(false);
  const [secondScenarioId, setSecondScenarioId] = useState<string | null>(null);
  const [panelOpen, setPanelOpen] = useState(false);
  const [selectedEntityId, setSelectedEntityId] = useState<string | null>(null);

  const handleStepChange = (step: number, _isComplete: boolean) => {
    // Always set — never reset to null on completion so EntityDetailDrawer
    // continues showing data at the final step after the scenario is done.
    setCurrentStep(step);
  };

  const handleSelectScenario = (id: string, name: string, totalSteps: number) => {
    setSelectedScenarioId(id);
    setSelectedScenarioName(name);
    setSelectedScenarioSteps(totalSteps);
    setCurrentStep(null);
    setIsAlreadyComplete(false);
    setSelectedEntityId(null);
  };

  const handleEntityClick = (entityId: string) => {
    setSelectedEntityId(entityId);
  };

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
          setIsAlreadyComplete(true);
        } else {
          setCurrentStep(null);
          setIsAlreadyComplete(false);
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
        <AttributeSelector onChange={setAttributeName} />
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
          onClick={() => setPanelOpen((v) => !v)}
        >
          Scenarios {panelOpen ? "▲" : "▼"}
        </button>
        {selectedScenarioId && (
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            {selectedScenarioName && (
              <span style={{ fontSize: 13, opacity: 0.85, maxWidth: 160, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {selectedScenarioName}
              </span>
            )}
            <ScenarioControls
              key={`${selectedScenarioId}-${String(isAlreadyComplete)}`}
              scenarioId={selectedScenarioId}
              totalSteps={selectedScenarioSteps}
              onStepChange={handleStepChange}
              initialStep={currentStep ?? 0}
              initialComplete={isAlreadyComplete}
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
        />
      )}

      <main className="app-main" style={{ position: "relative" }}>
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
            step={currentStep}
            onClose={() => setSelectedEntityId(null)}
          />
        )}
      </main>
    </div>
  );
}
