/**
 * FidelityDashboard — Backtesting validation transparency display.
 *
 * Shows the five historical validation cases (GRC, ARG, LBN, THA, ECU) with
 * per-step fidelity gate status, the first MAGNITUDE-validated result, and
 * the two documented structural gaps as known limitations deferred to M7.
 *
 * Framing: capability analysis evidence, not a report card. The model knows
 * where it is right and where it is not. That is a harder standard than
 * producing plausible-looking outputs. See stakeholder-walkthrough.md §Section 3.
 *
 * Data is hardcoded — this is methodology documentation alongside outputs,
 * not a live status board. Values are sourced from the backtesting_thresholds
 * table migrations (c7e2a9f4d1b8, a3d9e7c2f4b1, and related migrations).
 */

interface StepResult {
  step: number;
  year: string;
  thresholdType: "DIRECTION_ONLY" | "MAGNITUDE";
  status: "PASS" | "STRUCTURAL_GAP";
  // For MAGNITUDE gates — the actual numbers
  magnitudeDetail?: {
    simulated: string;
    actual: string;
    deviation: string;
    band: string;
  };
  // For STRUCTURAL_GAP — the issue reference and cause
  gapDetail?: {
    issueNumber: number;
    cause: string;
    milestone: string;
  };
}

interface CrisisCase {
  caseId: string;
  entityId: string;
  name: string;
  crisisType: string;
  years: string;
  steps: StepResult[];
  notes?: string;
}

const CASES: CrisisCase[] = [
  {
    caseId: "GREECE_2010_2012",
    entityId: "GRC",
    name: "Greece",
    crisisType: "Fiscal consolidation / external conditionality",
    years: "2010–2012",
    steps: [
      { step: 1, year: "2010", thresholdType: "DIRECTION_ONLY", status: "PASS" },
      { step: 2, year: "2011", thresholdType: "DIRECTION_ONLY", status: "PASS" },
      { step: 3, year: "2012", thresholdType: "DIRECTION_ONLY", status: "PASS" },
    ],
    notes:
      "Three consecutive years of GDP contraction correctly predicted. " +
      "MAGNITUDE deferred to M11 — accumulation-only model lacks mean-reversion channel " +
      "(Issue #221).",
  },
  {
    caseId: "ARGENTINA_2001_2002",
    entityId: "ARG",
    name: "Argentina",
    crisisType: "Sovereign default / convertibility peg collapse",
    years: "2001–2002",
    steps: [
      { step: 1, year: "2001", thresholdType: "DIRECTION_ONLY", status: "PASS" },
      {
        step: 2,
        year: "2002",
        thresholdType: "MAGNITUDE",
        status: "PASS",
        magnitudeDetail: {
          simulated: "−10.55%",
          actual: "−10.9%",
          deviation: "3.2%",
          band: "±20% → [−13.08%, −8.72%]",
        },
      },
    ],
    notes:
      "Step 2 is the first MAGNITUDE-validated result in WorldSim. " +
      "Mechanism: depressed-regime multiplier (1.5×) applied to Zero Deficit Plan " +
      "spending cut (−6.5% of GDP). " +
      "Step 1 MAGNITUDE deferred to M11 — one-step lag structural gap (Issue #222).",
  },
  {
    caseId: "LEBANON_2019_2020",
    entityId: "LBN",
    name: "Lebanon",
    crisisType: "Banking collapse / compound crisis",
    years: "2019–2020",
    steps: [
      { step: 1, year: "2019", thresholdType: "DIRECTION_ONLY", status: "PASS" },
      { step: 2, year: "2020", thresholdType: "DIRECTION_ONLY", status: "PASS" },
    ],
    notes:
      "Cascade case — banking collapse, currency crisis, sovereign default, and " +
      "Beirut port explosion. Full cascade propagation dynamics deferred to Issue #29.",
  },
  {
    caseId: "THAILAND_1997_2000",
    entityId: "THA",
    name: "Thailand",
    crisisType: "External contagion / balance-sheet deterioration",
    years: "1997–1998",
    steps: [
      { step: 1, year: "1997", thresholdType: "DIRECTION_ONLY", status: "PASS" },
      { step: 2, year: "1998", thresholdType: "DIRECTION_ONLY", status: "PASS" },
    ],
    notes:
      "Externally-triggered currency speculative attack producing domestic " +
      "balance-sheet deterioration — distinct crisis mechanism from all other cases.",
  },
  {
    caseId: "ECUADOR_1999_2000",
    entityId: "ECU",
    name: "Ecuador",
    crisisType: "Banking collapse / dollarization",
    years: "1999–2000",
    steps: [
      { step: 1, year: "1999", thresholdType: "DIRECTION_ONLY", status: "PASS" },
      { step: 2, year: "2000", thresholdType: "DIRECTION_ONLY", status: "PASS" },
    ],
    notes:
      "First case with a recovery at step 2 (+2.8% historical outturn). Fidelity gate: " +
      "'not deeper than step 1' (not 'predict contraction'). Model passes — reports equal " +
      "GDP (−6.3%), satisfying the ≥ threshold. Documented blind spot: dollarization " +
      "stabilization and oil recovery channels not yet modeled.",
  },
];

const STRUCTURAL_GAPS = [
  {
    entity: "ARG",
    step: 1,
    year: "2001",
    issueNumber: 222,
    cause:
      "One-step lag: Zero Deficit Plan fires at step 1 but MacroeconomicModule " +
      "processes prior-step events only. Step 1 reports the initial seed (−0.8%) " +
      "while the historical outturn (−4.4%) reflects the contemporaneous shock. " +
      "Model deviation: 82%. Not fixable by parameter calibration.",
    milestone: "M11",
    deviation: "−0.8% model vs −4.4% actual (82% deviation)",
  },
  {
    entity: "GRC",
    step: "2–3",
    year: "2011–2012",
    issueNumber: 221,
    cause:
      "GDP is a pure accumulation stock — it only moves when a fiscal event fires " +
      "and never receives an endogenous recovery impulse. The Greek economy improved " +
      "from −8.9% to −6.6% without a positive fiscal shock in the fixture. " +
      "Requires a mean-reversion channel in MacroeconomicModule (Chief Methodologist " +
      "+ Chief Engineer joint ADR).",
    milestone: "M11",
    deviation: "GRC step 2: −21.4% model vs −8.9% actual (140%); step 3: −31.4% vs −6.6% (376%)",
  },
];

// ─── Sub-components ────────────────────────────────────────────────────────────

function PassBadge({ type }: { type: "DIRECTION_ONLY" | "MAGNITUDE" }) {
  const isMagnitude = type === "MAGNITUDE";
  return (
    <span
      style={{
        background: isMagnitude ? "#1e3a5f" : "#064e3b",
        color: isMagnitude ? "#93c5fd" : "#6ee7b7",
        border: `1px solid ${isMagnitude ? "#3b82f6" : "#10b981"}`,
        borderRadius: 3,
        padding: "1px 6px",
        fontSize: 10,
        fontWeight: 700,
        letterSpacing: 0.4,
        whiteSpace: "nowrap",
      }}
      title={
        isMagnitude
          ? "MAGNITUDE: simulated value within 20% of historical outturn"
          : "DIRECTION_ONLY: sign of directional change correctly predicted"
      }
    >
      {isMagnitude ? "MAGNITUDE ✓" : "DIR ✓"}
    </span>
  );
}

function StepCell({ step }: { step: StepResult }) {
  return (
    <div style={{ marginBottom: step.magnitudeDetail ? 0 : 0 }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 6,
          marginBottom: step.magnitudeDetail ? 4 : 0,
        }}
      >
        <span style={{ fontSize: 11, color: "#64748b", minWidth: 32 }}>
          {step.year}
        </span>
        <PassBadge type={step.thresholdType} />
      </div>
      {step.magnitudeDetail && (
        <div
          style={{
            background: "rgba(59,130,246,0.07)",
            border: "1px solid rgba(59,130,246,0.2)",
            borderRadius: 3,
            padding: "4px 8px",
            fontSize: 11,
            color: "#93c5fd",
            marginTop: 4,
          }}
        >
          <div style={{ color: "#bfdbfe", fontWeight: 600, marginBottom: 2, fontSize: 10 }}>
            FIRST MAGNITUDE-VALIDATED RESULT
          </div>
          <div>
            Model {step.magnitudeDetail.simulated} vs actual {step.magnitudeDetail.actual}
            {" "}— deviation{" "}
            <strong style={{ color: "#6ee7b7" }}>{step.magnitudeDetail.deviation}</strong>
          </div>
          <div style={{ color: "#64748b", marginTop: 2 }}>
            Tolerance {step.magnitudeDetail.band}
          </div>
        </div>
      )}
    </div>
  );
}

function CaseRow({ c }: { c: CrisisCase }) {
  const stepCount = c.steps.length;
  return (
    <div
      data-testid={`fidelity-case-${c.entityId}`}
      style={{
        display: "grid",
        gridTemplateColumns: "80px 1fr 2fr auto",
        gap: "0 16px",
        padding: "10px 16px",
        borderBottom: "1px solid rgba(255,255,255,0.06)",
        alignItems: "start",
      }}
    >
      {/* Entity + years */}
      <div>
        <div style={{ fontWeight: 700, fontSize: 13, color: "#e2e8f0" }}>
          {c.entityId}
        </div>
        <div style={{ fontSize: 11, color: "#64748b", marginTop: 1 }}>
          {c.years}
        </div>
        <div style={{ fontSize: 10, color: "#475569", marginTop: 1 }}>
          {stepCount} {stepCount === 1 ? "step" : "steps"}
        </div>
      </div>

      {/* Name and crisis type */}
      <div>
        <div style={{ fontSize: 13, color: "#cbd5e1", fontWeight: 500 }}>
          {c.name}
        </div>
        <div style={{ fontSize: 11, color: "#64748b", marginTop: 2 }}>
          {c.crisisType}
        </div>
        {c.notes && (
          <div
            style={{
              fontSize: 11,
              color: "#475569",
              marginTop: 4,
              fontStyle: "italic",
              lineHeight: 1.4,
            }}
          >
            {c.notes}
          </div>
        )}
      </div>

      {/* Step results */}
      <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
        {c.steps.map((s) => (
          <StepCell key={s.step} step={s} />
        ))}
      </div>

      {/* Summary */}
      <div style={{ textAlign: "right" }}>
        <span
          style={{
            fontSize: 11,
            color: "#6ee7b7",
            fontWeight: 600,
          }}
        >
          All gates PASS
        </span>
      </div>
    </div>
  );
}

// ─── Main component ────────────────────────────────────────────────────────────

export default function FidelityDashboard() {
  const totalStepChecks = CASES.reduce((n, c) => n + c.steps.length, 0);
  const magnitudePasses = CASES.flatMap((c) =>
    c.steps.filter((s) => s.thresholdType === "MAGNITUDE" && s.status === "PASS"),
  ).length;

  return (
    <div
      data-testid="fidelity-dashboard"
      style={{
        background: "#0f1f33",
        borderBottom: "1px solid rgba(255,255,255,0.08)",
        color: "#cbd5e1",
        fontFamily: "system-ui, 'Segoe UI', sans-serif",
        maxHeight: 520,
        overflowY: "auto",
      }}
    >
      {/* Header bar */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "10px 16px 8px",
          borderBottom: "1px solid rgba(255,255,255,0.08)",
          background: "#122a45",
        }}
      >
        <div>
          <span
            style={{
              fontSize: 12,
              fontWeight: 700,
              textTransform: "uppercase",
              letterSpacing: "0.07em",
              color: "#8aa8c4",
            }}
          >
            Backtesting Validation
          </span>
          <span style={{ fontSize: 12, color: "#475569", marginLeft: 10 }}>
            Five historical crises — {totalStepChecks} sign checks
          </span>
        </div>

        {/* Summary badges */}
        <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
          <span
            style={{
              background: "#064e3b",
              color: "#6ee7b7",
              border: "1px solid #10b981",
              borderRadius: 4,
              padding: "2px 8px",
              fontSize: 11,
              fontWeight: 700,
            }}
          >
            DIRECTION_ONLY: 5/5 cases ✓
          </span>
          <span
            style={{
              background: "#1e3a5f",
              color: "#93c5fd",
              border: "1px solid #3b82f6",
              borderRadius: 4,
              padding: "2px 8px",
              fontSize: 11,
              fontWeight: 700,
            }}
          >
            MAGNITUDE: {magnitudePasses}/2 cases for ADR-006 upgrade
          </span>
        </div>
      </div>

      {/* Framing note */}
      <div
        style={{
          padding: "8px 16px",
          fontSize: 12,
          color: "#64748b",
          borderBottom: "1px solid rgba(255,255,255,0.05)",
          lineHeight: 1.5,
        }}
      >
        The model is tested on whether it gets the sign right. Consistent
        directional accuracy across five distinct crisis mechanisms is evidence
        of real causal dynamics — not a coincidence. Magnitude calibration is the
        next validation layer. We are not claiming it before we have evidence.
      </div>

      {/* Case table */}
      <div>
        {CASES.map((c) => (
          <CaseRow key={c.caseId} c={c} />
        ))}
      </div>

      {/* Structural gaps */}
      <div
        style={{
          padding: "10px 16px",
          borderTop: "1px solid rgba(255,255,255,0.08)",
        }}
      >
        <div
          style={{
            fontSize: 11,
            fontWeight: 700,
            textTransform: "uppercase",
            letterSpacing: "0.06em",
            color: "#78716c",
            marginBottom: 8,
          }}
        >
          Documented Structural Gaps — Deferred to M7
        </div>
        {STRUCTURAL_GAPS.map((gap, i) => (
          <div
            key={i}
            data-testid={`structural-gap-${gap.entity}-${gap.step}`}
            style={{
              background: "rgba(120,113,108,0.08)",
              border: "1px solid rgba(120,113,108,0.2)",
              borderLeft: "3px solid #78716c",
              borderRadius: 3,
              padding: "6px 10px",
              marginBottom: 6,
              fontSize: 11,
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                marginBottom: 3,
              }}
            >
              <span style={{ fontWeight: 600, color: "#a8a29e" }}>
                {gap.entity} step {gap.step} ({gap.year}) MAGNITUDE
              </span>
              <span style={{ color: "#78716c" }}>
                Issue #{gap.issueNumber} · {gap.milestone}
              </span>
            </div>
            <div style={{ color: "#78716c", lineHeight: 1.4 }}>{gap.cause}</div>
            <div
              style={{
                color: "#57534e",
                marginTop: 3,
                fontStyle: "italic",
              }}
            >
              {gap.deviation}
            </div>
          </div>
        ))}
      </div>

      {/* ADR-006 upgrade trigger */}
      <div
        style={{
          padding: "8px 16px 10px",
          borderTop: "1px solid rgba(255,255,255,0.05)",
          background: "rgba(30,58,95,0.3)",
          fontSize: 11,
          color: "#64748b",
          lineHeight: 1.5,
        }}
      >
        <strong style={{ color: "#93c5fd" }}>ADR-006 Monte Carlo upgrade trigger:</strong>{" "}
        {magnitudePasses} of 2 required MAGNITUDE cases achieved.
        Argentina 2002 (step 2) is the first. One additional MAGNITUDE case (deferred to M11)
        unlocks the full DISTRIBUTION_COMBINED threshold infrastructure and uncertainty band
        calibration.
      </div>
    </div>
  );
}
