import { useState } from "react";
import AttributeSelector from "./components/AttributeSelector";
import ChoroplethMap from "./components/ChoroplethMap";
import "./App.css";

const DEFAULT_ATTRIBUTE = "population_total";

export default function App() {
  const [attributeName, setAttributeName] = useState(DEFAULT_ATTRIBUTE);

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">WorldSim</h1>
        <AttributeSelector onChange={setAttributeName} />
      </header>
      <main className="app-main">
        <ChoroplethMap attributeName={attributeName} title={attributeName} />
      </main>
    </div>
  );
}
