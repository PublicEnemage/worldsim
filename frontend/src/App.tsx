import { useState } from "react";
import AttributeSelector from "./components/AttributeSelector";
import ChoroplethMap from "./components/ChoroplethMap";
import ScenarioControls from "./components/ScenarioControls";
import "./App.css";

const DEFAULT_ATTRIBUTE = "population_total";

export default function App() {
  const [attributeName, setAttributeName] = useState(DEFAULT_ATTRIBUTE);
  const [selectedScenarioId] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState<number | null>(null);

  const handleStepChange = (step: number, _isComplete: boolean) => {
    setCurrentStep(step);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">WorldSim</h1>
        <AttributeSelector onChange={setAttributeName} />
        {selectedScenarioId && (
          <ScenarioControls
            scenarioId={selectedScenarioId}
            totalSteps={3}
            onStepChange={handleStepChange}
          />
        )}
      </header>
      <main className="app-main">
        <ChoroplethMap
          attributeName={attributeName}
          title={attributeName}
          scenarioId={selectedScenarioId}
          currentStep={currentStep}
        />
      </main>
    </div>
  );
}
