/**
 * Divergence fill proof-of-concept — FA brief §Divergence Fill Implementation (FA-R2)
 *
 * Validates the merged-key <Area> approach for Mode 3 divergence fill at:
 *   (a) full 8-curve configuration
 *   (b) re-convergence case (fill disappears when delta collapses to zero)
 *   (c) step-count mismatch (partial active trajectory — null on steps not yet computed)
 *
 * This file is a standalone sandbox component. It is not imported by the application.
 * Referenced in Issue #460 PR per FA brief requirement.
 */
import React from "react";
import {
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { FRAMEWORK_COLORS } from "../src/constants/frameworkColors";

interface MergedStep {
  step_index: number;
  financial_active: number | null;
  financial_baseline: number | null;
  human_development_active: number | null;
  human_development_baseline: number | null;
  ecological_active: number | null;
  ecological_baseline: number | null;
  governance_active: number | null;
  governance_baseline: number | null;
}

// (a) Full 8-curve configuration with divergence
const fullConfigData: MergedStep[] = [
  { step_index: 1, financial_active: 0.75, financial_baseline: 0.75, human_development_active: 0.60, human_development_baseline: 0.60, ecological_active: 0.85, ecological_baseline: 0.85, governance_active: 0.55, governance_baseline: 0.55 },
  { step_index: 2, financial_active: 0.65, financial_baseline: 0.75, human_development_active: 0.55, human_development_baseline: 0.60, ecological_active: 0.80, ecological_baseline: 0.85, governance_active: 0.48, governance_baseline: 0.55 },
  { step_index: 3, financial_active: 0.55, financial_baseline: 0.75, human_development_active: 0.48, human_development_baseline: 0.60, ecological_active: 0.72, ecological_baseline: 0.85, governance_active: 0.40, governance_baseline: 0.55 },
  { step_index: 4, financial_active: 0.52, financial_baseline: 0.75, human_development_active: 0.45, human_development_baseline: 0.60, ecological_active: 0.68, ecological_baseline: 0.85, governance_active: 0.38, governance_baseline: 0.55 },
  { step_index: 5, financial_active: 0.50, financial_baseline: 0.75, human_development_active: 0.44, human_development_baseline: 0.60, ecological_active: 0.65, ecological_baseline: 0.85, governance_active: 0.35, governance_baseline: 0.55 },
];

// (b) Re-convergence: delta collapses to zero at step 4
const reconvergenceData: MergedStep[] = [
  { step_index: 1, financial_active: 0.75, financial_baseline: 0.75, human_development_active: 0.60, human_development_baseline: 0.60, ecological_active: 0.85, ecological_baseline: 0.85, governance_active: 0.55, governance_baseline: 0.55 },
  { step_index: 2, financial_active: 0.60, financial_baseline: 0.75, human_development_active: 0.50, human_development_baseline: 0.60, ecological_active: 0.72, ecological_baseline: 0.85, governance_active: 0.42, governance_baseline: 0.55 },
  { step_index: 3, financial_active: 0.65, financial_baseline: 0.75, human_development_active: 0.55, human_development_baseline: 0.60, ecological_active: 0.78, ecological_baseline: 0.85, governance_active: 0.48, governance_baseline: 0.55 },
  { step_index: 4, financial_active: 0.75, financial_baseline: 0.75, human_development_active: 0.60, human_development_baseline: 0.60, ecological_active: 0.85, ecological_baseline: 0.85, governance_active: 0.55, governance_baseline: 0.55 },
  { step_index: 5, financial_active: 0.75, financial_baseline: 0.75, human_development_active: 0.60, human_development_baseline: 0.60, ecological_active: 0.85, ecological_baseline: 0.85, governance_active: 0.55, governance_baseline: 0.55 },
];

// (c) Step-count mismatch: active trajectory only computed through step 3
const mismatchData: MergedStep[] = [
  { step_index: 1, financial_active: 0.75, financial_baseline: 0.75, human_development_active: 0.60, human_development_baseline: 0.60, ecological_active: 0.85, ecological_baseline: 0.85, governance_active: 0.55, governance_baseline: 0.55 },
  { step_index: 2, financial_active: 0.65, financial_baseline: 0.75, human_development_active: 0.52, human_development_baseline: 0.60, ecological_active: 0.78, ecological_baseline: 0.85, governance_active: 0.48, governance_baseline: 0.55 },
  { step_index: 3, financial_active: 0.55, financial_baseline: 0.75, human_development_active: 0.45, human_development_baseline: 0.60, ecological_active: 0.70, ecological_baseline: 0.85, governance_active: 0.40, governance_baseline: 0.55 },
  // Steps 4-5: active not yet computed
  { step_index: 4, financial_active: null, financial_baseline: 0.75, human_development_active: null, human_development_baseline: 0.60, ecological_active: null, ecological_baseline: 0.85, governance_active: null, governance_baseline: 0.55 },
  { step_index: 5, financial_active: null, financial_baseline: 0.75, human_development_active: null, human_development_baseline: 0.60, ecological_active: null, ecological_baseline: 0.85, governance_active: null, governance_baseline: 0.55 },
];

function TrajectoryChart({ data, title }: { data: MergedStep[]; title: string }) {
  return (
    <div style={{ marginBottom: 48 }}>
      <h3 style={{ fontFamily: "monospace", fontSize: 14, marginBottom: 8 }}>{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <ComposedChart data={data} margin={{ top: 8, right: 16, bottom: 8, left: 8 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
          <XAxis dataKey="step_index" />
          <YAxis domain={[0, 1]} />
          <Tooltip />
          <Legend />

          {/* Divergence fill Areas — rendered first (below lines) */}
          <Area dataKey="financial_active" baseLine="financial_baseline" fill={FRAMEWORK_COLORS.financial} fillOpacity={0.12} stroke="none" connectNulls={false} />
          <Area dataKey="human_development_active" baseLine="human_development_baseline" fill={FRAMEWORK_COLORS.human_development} fillOpacity={0.12} stroke="none" connectNulls={false} />
          <Area dataKey="ecological_active" baseLine="ecological_baseline" fill={FRAMEWORK_COLORS.ecological} fillOpacity={0.12} stroke="none" connectNulls={false} />
          <Area dataKey="governance_active" baseLine="governance_baseline" fill={FRAMEWORK_COLORS.governance} fillOpacity={0.12} stroke="none" connectNulls={false} />

          {/* Baseline ghost Lines */}
          <Line dataKey="financial_baseline" stroke={FRAMEWORK_COLORS.financial} strokeOpacity={0.5} strokeWidth={1} strokeDasharray="4 2" dot={false} connectNulls={false} name="Financial (baseline)" />
          <Line dataKey="human_development_baseline" stroke={FRAMEWORK_COLORS.human_development} strokeOpacity={0.5} strokeWidth={1} strokeDasharray="4 2" dot={false} connectNulls={false} name="HD (baseline)" />
          <Line dataKey="ecological_baseline" stroke={FRAMEWORK_COLORS.ecological} strokeOpacity={0.5} strokeWidth={1} strokeDasharray="4 2" dot={false} connectNulls={false} name="Ecological (baseline)" />
          <Line dataKey="governance_baseline" stroke={FRAMEWORK_COLORS.governance} strokeOpacity={0.5} strokeWidth={1} strokeDasharray="4 2" dot={false} connectNulls={false} name="Governance (baseline)" />

          {/* Active Lines */}
          <Line dataKey="financial_active" stroke={FRAMEWORK_COLORS.financial} strokeWidth={2} dot={false} connectNulls={false} name="Financial" />
          <Line dataKey="human_development_active" stroke={FRAMEWORK_COLORS.human_development} strokeWidth={2} dot={false} connectNulls={false} name="Human Development" />
          <Line dataKey="ecological_active" stroke={FRAMEWORK_COLORS.ecological} strokeWidth={2} dot={false} connectNulls={false} name="Ecological" />
          <Line dataKey="governance_active" stroke={FRAMEWORK_COLORS.governance} strokeWidth={2} dot={false} connectNulls={false} name="Governance" />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}

export function DivergenceFillPOC() {
  return (
    <div style={{ padding: 24, fontFamily: "monospace" }}>
      <h2 style={{ fontSize: 16, marginBottom: 24 }}>
        Divergence Fill POC — FA brief §Divergence Fill Implementation (FA-R2)
      </h2>
      <TrajectoryChart data={fullConfigData} title="(a) Full 8-curve configuration with divergence" />
      <TrajectoryChart data={reconvergenceData} title="(b) Re-convergence: fill disappears when delta collapses to zero at step 4" />
      <TrajectoryChart data={mismatchData} title="(c) Step-count mismatch: active null at steps 4-5 (not yet computed)" />
    </div>
  );
}
