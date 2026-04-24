import { useState } from "react";
import AttributeSelector from "./components/AttributeSelector";
import ChoroplethMap from "./components/ChoroplethMap";
import DeltaChoropleth from "./components/DeltaChoropleth";
import ScenarioControls from "./components/ScenarioControls";
import "./App.css";

const DEFAULT_ATTRIBUTE = "population_total";

export default function App() {
  const [attributeName, setAttributeName] = useState(DEFAULT_ATTRIBUTE);
  const [selectedScenarioId] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState<number | null>(null);
  const [compareMode, setCompareMode] = useState(false);
  const [secondScenarioId] = useState<string | null>(null);

  const handleStepChange = (step: number, _isComplete: boolean) => {
    setCurrentStep(step);
  };

  const showDelta = compareMode && selectedScenarioId !== null && secondScenarioId !== null;

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">WorldSim</h1>
        <AttributeSelector onChange={setAttributeName} />
        <label style={{ marginLeft: 12, fontSize: 13 }}>
          <input
            type="checkbox"
            checked={compareMode}
            onChange={(e) => setCompareMode(e.target.checked)}
            style={{ marginRight: 4 }}
          />
          Compare scenarios
        </label>
        {selectedScenarioId && (
          <ScenarioControls
            scenarioId={selectedScenarioId}
            totalSteps={3}
            onStepChange={handleStepChange}
          />
        )}
      </header>
      <main className="app-main">
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
          />
        )}
      </main>
    </div>
  );
}
