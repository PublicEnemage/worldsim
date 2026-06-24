/* eslint-disable react-refresh/only-export-components */
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
import { useScenarioStepStore, type TrajectoryResponse } from "../store/scenarioStepStore";

export const LAYOUT = {
  1024: { trajectory: 480, coPrimary: 240, controlPlane: 280, chartHeight: 300 },
  1280: { trajectory: 580, coPrimary: 400, controlPlane: 280, chartHeight: 320 },
  1440: { trajectory: 680, coPrimary: 400, controlPlane: 280, chartHeight: 380 },
} as const;

// DD-016 (M16-G2): viewport-responsive Zone 1B/1C/1D flex proportions.
// Previous values (M9/DD-015): 45/25/30. New values support the political risk
// sub-section in Zone 1D without overflow at 1280×800.
export const ZONE_PROPORTIONS = {
  1024: { zone1b: "50%", zone1c: "10%", zone1d: "40%" },
  1280: { zone1b: "35%", zone1c: "15%", zone1d: "50%" },
  1440: { zone1b: "40%", zone1c: "15%", zone1d: "45%" },
} as const;

export function useViewportBreakpoint(): 1024 | 1280 | 1440 {
  const [bp, setBp] = useState<1024 | 1280 | 1440>(
    window.innerWidth >= 1440 ? 1440 : window.innerWidth >= 1280 ? 1280 : 1024,
  );
  useEffect(() => {
    function update() {
      setBp(window.innerWidth >= 1440 ? 1440 : window.innerWidth >= 1280 ? 1280 : 1024);
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
  /** Human cost ledger strip rendered below Zone 1A trajectory chart (Issue #747). */
  cohortPanel?: React.ReactNode;
  /** M16-G2 (#986) — Cohort Impact sub-section rendered below MDA panel in zone-1b.
   *  Rendered as a flex sibling (not inside mdaPanel) so it has guaranteed visible space. */
  zone1bCohortSection?: React.ReactNode;
  /** Entity ISO codes for multi-case Mode 1 tick format (UD-R2). */
  entityIds?: string[];
  /** Override chart height (px) — defaults to LAYOUT[bp].chartHeight. */
  chartHeight?: number;
  /** Phase 4 (ADR-017): per-entity trajectory responses for composite encoding. */
  entityTrajectories?: Record<string, TrajectoryResponse> | null;
  /** Phase 4 (ADR-017): per-entity baseline trajectories for Mode 3 ghost paths. */
  entityBaselineTrajectories?: Record<string, TrajectoryResponse> | null;
}

export function InstrumentCluster({
  mdaPanel,
  pmmWidget,
  fourFramework,
  cohortPanel,
  zone1bCohortSection,
  entityIds,
  chartHeight: chartHeightProp,
  entityTrajectories,
  entityBaselineTrajectories,
}: InstrumentClusterProps) {
  const { mode } = useScenarioStepStore();
  const bp = useViewportBreakpoint();
  const layout = LAYOUT[bp];
  const zoneProportions = ZONE_PROPORTIONS[bp];
  const chartHeight = chartHeightProp ?? layout.chartHeight;

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
      {/* Zone 1A — Trajectory View + Human Cost Ledger strip (Issue #747) */}
      <div
        data-testid="zone-1a-trajectory-container"
        style={{ gridColumn: 1, gridRow: 1, minWidth: layout.trajectory, minHeight: chartHeight, display: "flex", flexDirection: "column" }}
      >
        <TrajectoryView
          width={layout.trajectory}
          height={chartHeight}
          entityIds={entityIds}
          entityTrajectories={entityTrajectories}
          entityBaselineTrajectories={entityBaselineTrajectories}
          data-testid="zone-1a-trajectory"
        />
        {cohortPanel}
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
        {/* Zone 1B — MDA Alert Panel + Cohort Impact sub-section (DD-016, M16-G2 #986) */}
        {/* Flex column: mdaPanel gets flex:1 1 0 (fills remaining space after cohort section);
            zone1bCohortSection gets flex:0 0 auto (natural height, always visible). */}
        <div
          data-testid="zone-1b"
          style={{
            flex: `0 0 ${zoneProportions.zone1b}`,
            overflow: "auto",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <div style={{ flex: "1 1 0", minHeight: 0, overflow: "hidden" }}>
            {mdaPanel ?? (
              <div style={{ color: "#bbb", fontSize: 12, padding: 8 }}>
                MDA Alert Panel (Zone 1B)
              </div>
            )}
          </div>
          {zone1bCohortSection}
        </div>

        {/* Zone 1C — PMM Widget (DD-016: 15% at 1280/1440, 10% at 1024) */}
        {/* data-testid lives on PMMWidgetZone1C root — not duplicated here */}
        <div style={{ flex: `0 0 ${zoneProportions.zone1c}`, overflow: "hidden" }}>
          {pmmWidget ?? (
            <div style={{ color: "#bbb", fontSize: 12, padding: 8 }}>
              PMM Widget (Zone 1C)
            </div>
          )}
        </div>

        {/* Zone 1D — Four-Framework + Political Risk sub-section (DD-016: 50% at 1280) */}
        {/* data-testid lives on FourFrameworkZone1D root — not duplicated here */}
        {/* overflow-y:auto per DD-016 — prevents clipping at 1024; no-op at 1280/1440 */}
        <div style={{ flex: `0 0 ${zoneProportions.zone1d}`, overflowY: "auto" }}>
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
