/**
 * InstrumentCluster — Zone 1 two-column layout container.
 *
 * Layout constants (binding per FA brief §Layout and Viewport):
 *   1024×768: trajectory=480px, co-primary=240px, control-plane=280px (reserved)
 *   1280×800: trajectory=580px, co-primary=400px, control-plane=280px
 *
 * Control plane zone is always rendered (never collapsed in Mode 1/2).
 * See DD-015 for why collapsing is prohibited.
 */
import React, { useEffect, useState } from "react";
import { TrajectoryView } from "./TrajectoryView";
import { useScenarioStepStore } from "../store/scenarioStepStore";

export const LAYOUT = {
  1024: { trajectory: 480, coPrimary: 240, controlPlane: 280 },
  1280: { trajectory: 580, coPrimary: 400, controlPlane: 280 },
} as const;

export function useViewportBreakpoint(): 1024 | 1280 {
  const [bp, setBp] = useState<1024 | 1280>(
    window.innerWidth >= 1280 ? 1280 : 1024,
  );
  useEffect(() => {
    function update() {
      setBp(window.innerWidth >= 1280 ? 1280 : 1024);
    }
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);
  return bp;
}

interface InstrumentClusterProps {
  /** Slots for co-primary instruments (1B, 1C, 1D). Accept children in order. */
  mdaPanel?: React.ReactNode;
  pmmWidget?: React.ReactNode;
  fourFramework?: React.ReactNode;
  /** Entity ISO codes for multi-case Mode 1 tick format (UD-R2). */
  entityIds?: string[];
}

export function InstrumentCluster({
  mdaPanel,
  pmmWidget,
  fourFramework,
  entityIds,
}: InstrumentClusterProps) {
  const { mode } = useScenarioStepStore();
  const bp = useViewportBreakpoint();
  const layout = LAYOUT[bp];

  const isMode3 = mode === "MODE_3";

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: `${layout.trajectory}px ${layout.coPrimary}px ${layout.controlPlane}px`,
        gridTemplateRows: "1fr",
        width: layout.trajectory + layout.coPrimary + layout.controlPlane,
        overflow: "hidden",
      }}
    >
      {/* Zone 1A — Trajectory View */}
      <div
        data-testid="zone-1a-trajectory-container"
        style={{ gridColumn: 1, gridRow: 1, minWidth: layout.trajectory }}
      >
        <TrajectoryView
          width={layout.trajectory}
          entityIds={entityIds}
          data-testid="zone-1a-trajectory"
        />
      </div>

      {/* Zone 1B/1C/1D — Co-primary cluster */}
      <div
        style={{
          gridColumn: 2,
          gridRow: 1,
          display: "flex",
          flexDirection: "column",
          minWidth: layout.coPrimary,
        }}
      >
        {/* Zone 1B — MDA Alert Panel (~45% of column height) */}
        {/* data-testid lives on MDAAlertPanelZone1B root — not duplicated here */}
        <div style={{ flex: "0 0 45%", overflow: "hidden" }}>
          {mdaPanel ?? (
            <div style={{ color: "#bbb", fontSize: 12, padding: 8 }}>
              MDA Alert Panel (Zone 1B)
            </div>
          )}
        </div>

        {/* Zone 1C — PMM Widget (~25% of column height) */}
        {/* data-testid lives on PMMWidgetZone1C root — not duplicated here */}
        <div style={{ flex: "0 0 25%", overflow: "hidden" }}>
          {pmmWidget ?? (
            <div style={{ color: "#bbb", fontSize: 12, padding: 8 }}>
              PMM Widget (Zone 1C)
            </div>
          )}
        </div>

        {/* Zone 1D — Four-Framework Current Position (~30% of column height) */}
        {/* data-testid lives on FourFrameworkZone1D root — not duplicated here */}
        <div style={{ flex: "0 0 30%", overflow: "hidden" }}>
          {fourFramework ?? (
            <div style={{ color: "#bbb", fontSize: 12, padding: 8 }}>
              Four-Framework Current Position (Zone 1D)
            </div>
          )}
        </div>
      </div>

      {/* Control plane zone — always rendered, 280px reserved (DD-015) */}
      <div
        data-testid="zone-control-plane"
        className={isMode3 ? "mode-3-active" : undefined}
        style={{
          gridColumn: 3,
          gridRow: 1,
          minWidth: layout.controlPlane,
          borderLeft: "1px solid #f0f0f0",
          position: "relative",
        }}
      >
        {!isMode3 && (
          <div
            aria-label="Control plane reserved zone"
            style={{
              position: "absolute",
              bottom: 16,
              left: 8,
              fontSize: 11,
              color: "rgba(0,0,0,0.25)",
              fontFamily: "monospace",
              pointerEvents: "none",
              userSelect: "none",
            }}
          >
            Control plane (Mode 3)
          </div>
        )}
      </div>
    </div>
  );
}
