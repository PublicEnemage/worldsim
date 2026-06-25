/**
 * Vitest: MDAAlertPanelZone1B — unit tests.
 *
 * Covers:
 *   US-014 — severity ordering (TERMINAL → CRITICAL → WARNING); secondary sort by step_index
 *   US-016 — mode-specific alert text: "crossed" / "is projected to cross" / " — " format
 *   US-017 — "Caused by:" present in Mode 3; absent in Mode 1/2
 *   ADR-008 Decision 5 — negotiation-defensibility label by confidence tier
 *
 * These are unit tests of pure functions exported from MDAAlertPanelZone1B.tsx.
 * Playwright E2E tests covering DOM assertions live in tests/e2e/mda-alert-panel.spec.ts.
 */
import { describe, it, expect } from "vitest";
import {
  sortAlerts,
  getNegotiationLabel,
  formatAlertText,
  truncateIndicatorName,
  buildSparklinePoints,
  formatCohortDistance,
  formatSourceId,
  SEVERITY_ORDER,
  FRAMEWORK_ABBREV,
} from "../MDAAlertPanelZone1B";
import type { Zone1BAlert } from "../../store/scenarioStepStore";

// ---------------------------------------------------------------------------
// Fixtures
// ---------------------------------------------------------------------------

function makeAlert(
  overrides: Partial<Zone1BAlert> & Pick<Zone1BAlert, "severity" | "step_index">,
): Zone1BAlert {
  return {
    mda_id: `mda-${overrides.severity}-${overrides.step_index}`,
    entity_id: "GRC",
    indicator_key: "poverty_headcount",
    indicator_name: "Poverty Headcount",
    framework: "human_development",
    cohort: "bottom_quintile",
    confidence_tier: 2,
    causal_attribution: null,
    floor_value: "0.2000",
    current_value: "0.1800",
    approach_pct_remaining: "-0.1000",
    consecutive_breach_steps: 1,
    recovery_horizon_years: null,
    ...overrides,
  };
}

// ---------------------------------------------------------------------------
// US-014 — Severity ordering + secondary sort by step_index
// ---------------------------------------------------------------------------

describe("US-014 — sortAlerts: severity ordering and secondary sort", () => {
  it("TERMINAL appears before CRITICAL", () => {
    const alerts = [
      makeAlert({ severity: "CRITICAL", step_index: 1 }),
      makeAlert({ severity: "TERMINAL", step_index: 2 }),
    ];
    const sorted = sortAlerts(alerts);
    expect(sorted[0].severity).toBe("TERMINAL");
    expect(sorted[1].severity).toBe("CRITICAL");
  });

  it("CRITICAL appears before WARNING", () => {
    const alerts = [
      makeAlert({ severity: "WARNING", step_index: 1 }),
      makeAlert({ severity: "CRITICAL", step_index: 2 }),
    ];
    const sorted = sortAlerts(alerts);
    expect(sorted[0].severity).toBe("CRITICAL");
    expect(sorted[1].severity).toBe("WARNING");
  });

  it("full sort: TERMINAL → CRITICAL → WARNING across mixed steps", () => {
    const alerts = [
      makeAlert({ severity: "WARNING", step_index: 1 }),
      makeAlert({ severity: "TERMINAL", step_index: 3 }),
      makeAlert({ severity: "CRITICAL", step_index: 2 }),
      makeAlert({ severity: "WARNING", step_index: 4 }),
    ];
    const sorted = sortAlerts(alerts);
    expect(sorted[0].severity).toBe("TERMINAL");
    expect(sorted[1].severity).toBe("CRITICAL");
    expect(sorted[2].severity).toBe("WARNING");
    expect(sorted[3].severity).toBe("WARNING");
  });

  it("within same severity, earlier step_index comes first", () => {
    const alerts = [
      makeAlert({ severity: "WARNING", step_index: 3 }),
      makeAlert({ severity: "WARNING", step_index: 1 }),
      makeAlert({ severity: "WARNING", step_index: 2 }),
    ];
    const sorted = sortAlerts(alerts);
    expect(sorted[0].step_index).toBe(1);
    expect(sorted[1].step_index).toBe(2);
    expect(sorted[2].step_index).toBe(3);
  });

  it("does not mutate the original array", () => {
    const alerts = [
      makeAlert({ severity: "WARNING", step_index: 2 }),
      makeAlert({ severity: "TERMINAL", step_index: 1 }),
    ];
    const original = [...alerts];
    sortAlerts(alerts);
    expect(alerts[0].severity).toBe(original[0].severity);
    expect(alerts[1].severity).toBe(original[1].severity);
  });

  it("SEVERITY_ORDER constants match the sort expectation", () => {
    expect(SEVERITY_ORDER.TERMINAL).toBeLessThan(SEVERITY_ORDER.CRITICAL);
    expect(SEVERITY_ORDER.CRITICAL).toBeLessThan(SEVERITY_ORDER.WARNING);
  });
});

// ---------------------------------------------------------------------------
// US-016 — Mode-specific alert text (UX-RULING-1)
// ---------------------------------------------------------------------------

describe("US-016 — formatAlertText: mode-specific alert language", () => {
  const alert = makeAlert({ severity: "CRITICAL", step_index: 3 });

  it("Mode 1: text contains 'crossed'", () => {
    const text = formatAlertText(alert, "MODE_1");
    expect(text).toContain("crossed");
  });

  it("Mode 1: text does not contain 'is projected'", () => {
    const text = formatAlertText(alert, "MODE_1");
    expect(text).not.toContain("is projected");
  });

  it("Mode 1: text does not contain 'Caused by:'", () => {
    const text = formatAlertText(alert, "MODE_1");
    expect(text).not.toContain("Caused by:");
  });

  it("Mode 2: text contains 'is projected to cross'", () => {
    const text = formatAlertText(alert, "MODE_2");
    expect(text).toContain("is projected to cross");
  });

  it("Mode 3: text contains ' — ' separator", () => {
    const text = formatAlertText(alert, "MODE_3");
    expect(text).toContain(" — ");
  });

  it("Mode 3: text begins with severity in uppercase (CRITICAL or WARNING)", () => {
    const textCritical = formatAlertText(makeAlert({ severity: "CRITICAL", step_index: 1 }), "MODE_3");
    const textWarning = formatAlertText(makeAlert({ severity: "WARNING", step_index: 1 }), "MODE_3");
    expect(textCritical.startsWith("CRITICAL")).toBe(true);
    expect(textWarning.startsWith("WARNING")).toBe(true);
  });

  it("Mode 3: text contains step index", () => {
    const text = formatAlertText(alert, "MODE_3");
    expect(text).toContain("step 3");
  });

  it("Mode 3: text contains indicator (spaces, not underscores)", () => {
    const text = formatAlertText(alert, "MODE_3");
    expect(text).toContain("poverty headcount");
    expect(text).not.toContain("poverty_headcount");
  });
});

// ---------------------------------------------------------------------------
// US-017 — "Caused by:" in Mode 3 only
// The pure function formatAlertText does NOT add causal attribution —
// that is rendered by the component from alert.causal_attribution.
// These tests assert the text contract: Mode 1/2 text is free of "Caused by:".
// ---------------------------------------------------------------------------

describe("US-017 — causal attribution: 'Caused by:' absent from Mode 1 and 2 text", () => {
  const alert = makeAlert({ severity: "WARNING", step_index: 2 });

  it("formatAlertText Mode 1 never produces 'Caused by:'", () => {
    expect(formatAlertText(alert, "MODE_1")).not.toContain("Caused by:");
  });

  it("formatAlertText Mode 2 never produces 'Caused by:'", () => {
    expect(formatAlertText(alert, "MODE_2")).not.toContain("Caused by:");
  });
});

// ---------------------------------------------------------------------------
// ADR-008 Decision 5 — Negotiation-defensibility label
// ---------------------------------------------------------------------------

describe("ADR-008 Decision 5 — getNegotiationLabel: confidence tier to label", () => {
  it("Tier 1 → 'High confidence — cite directly'", () => {
    expect(getNegotiationLabel(1)).toBe("High confidence — cite directly");
  });

  it("Tier 2 → 'High confidence — cite directly'", () => {
    expect(getNegotiationLabel(2)).toBe("High confidence — cite directly");
  });

  it("Tier 3 → 'Moderate confidence — cite with caveat'", () => {
    expect(getNegotiationLabel(3)).toBe("Moderate confidence — cite with caveat");
  });

  it("Tier 4 → 'Exploratory — do not cite'", () => {
    expect(getNegotiationLabel(4)).toBe("Exploratory — do not cite");
  });

  it("Tier 5 → 'Exploratory — do not cite'", () => {
    expect(getNegotiationLabel(5)).toBe("Exploratory — do not cite");
  });

  it("boundary: Tier 2 and Tier 3 produce different labels", () => {
    expect(getNegotiationLabel(2)).not.toBe(getNegotiationLabel(3));
  });

  it("boundary: Tier 3 and Tier 4 produce different labels", () => {
    expect(getNegotiationLabel(3)).not.toBe(getNegotiationLabel(4));
  });
});

// ---------------------------------------------------------------------------
// Framework abbreviations
// ---------------------------------------------------------------------------

describe("FRAMEWORK_ABBREV: known framework keys", () => {
  it("financial → FIN", () => {
    expect(FRAMEWORK_ABBREV.financial).toBe("FIN");
  });

  it("human_development → HDI", () => {
    expect(FRAMEWORK_ABBREV.human_development).toBe("HDI");
  });

  it("ecological → ECO", () => {
    expect(FRAMEWORK_ABBREV.ecological).toBe("ECO");
  });

  it("governance → GOV", () => {
    expect(FRAMEWORK_ABBREV.governance).toBe("GOV");
  });
});

// ---------------------------------------------------------------------------
// truncateIndicatorName — compact row display name (US-013)
// ---------------------------------------------------------------------------

describe("truncateIndicatorName: 22-char limit with ellipsis", () => {
  it("name ≤ 22 chars is returned unchanged", () => {
    expect(truncateIndicatorName("poverty headcount", 22)).toBe("poverty headcount");
  });

  it("name exactly 22 chars is returned unchanged", () => {
    const name = "a".repeat(22);
    expect(truncateIndicatorName(name, 22)).toBe(name);
  });

  it("name > 22 chars is truncated with '…' at position 21", () => {
    const name = "structural adjustment programme";
    const result = truncateIndicatorName(name, 22);
    expect(result.endsWith("…")).toBe(true);
    expect(result.length).toBe(22);
  });

  it("truncated string without the '…' is a prefix of the original", () => {
    const name = "social_cohesion_index_long";
    const result = truncateIndicatorName(name, 22);
    expect(name.startsWith(result.slice(0, -1))).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// buildSparklinePoints — SVG polyline coordinates for AlertDetailPanel (#745)
// ---------------------------------------------------------------------------

describe("buildSparklinePoints: SVG polyline generation", () => {
  it("returns null when fewer than 2 non-null scores", () => {
    expect(buildSparklinePoints([], 200, 56)).toBeNull();
    expect(buildSparklinePoints([null], 200, 56)).toBeNull();
    expect(buildSparklinePoints([0.5], 200, 56)).toBeNull();
  });

  it("returns null when only one finite score among nulls", () => {
    expect(buildSparklinePoints([null, 0.5, null], 200, 56)).toBeNull();
  });

  it("returns a non-empty string for 2+ non-null scores", () => {
    const result = buildSparklinePoints([0.3, 0.5, 0.7], 200, 56);
    expect(result).not.toBeNull();
    expect(typeof result).toBe("string");
    expect(result!.length).toBeGreaterThan(0);
  });

  it("output contains comma-separated coordinate pairs", () => {
    const result = buildSparklinePoints([0.3, 0.6], 200, 56);
    expect(result).not.toBeNull();
    const pairs = result!.split(" ");
    expect(pairs.length).toBeGreaterThanOrEqual(2);
    for (const pair of pairs) {
      expect(pair).toMatch(/^\d+\.\d,\d+\.\d$/);
    }
  });

  it("null scores are skipped — not represented as a point", () => {
    const withNulls = buildSparklinePoints([0.3, null, 0.6], 200, 56);
    const withoutNulls = buildSparklinePoints([0.3, 0.6], 200, 56);
    // Skipping a null mid-series means fewer points than all-filled series of same length
    expect(withNulls!.split(" ").length).toBeLessThan(
      buildSparklinePoints([0.3, 0.5, 0.6], 200, 56)!.split(" ").length,
    );
    // Two-point result should equal the all-non-null 2-point case
    expect(withNulls).toBe(withoutNulls);
  });

  it("all-zero scores produce valid points (not NaN)", () => {
    const result = buildSparklinePoints([0, 0, 0], 200, 56);
    expect(result).not.toBeNull();
    expect(result).not.toContain("NaN");
  });

  it("points respect padding — x starts at padding, not 0", () => {
    const padding = 4;
    const result = buildSparklinePoints([0.3, 0.6], 200, 56, padding);
    expect(result).not.toBeNull();
    const firstPair = result!.split(" ")[0];
    const x = parseFloat(firstPair.split(",")[0]);
    expect(x).toBeCloseTo(padding, 0);
  });
});

// ---------------------------------------------------------------------------
// formatCohortDistance — dynamic floor distance label (Issue #1239 / DEMO6-010)
// ---------------------------------------------------------------------------

describe("formatCohortDistance — dynamic floor distance label", () => {
  it("gte threshold (breachesBelow=true): returns 'X% below floor'", () => {
    expect(formatCohortDistance("3.75", true, false)).toBe("3.75% below floor");
  });

  it("lte threshold (breachesBelow=false): returns 'X% above floor'", () => {
    expect(formatCohortDistance("2.00", false, false)).toBe("2.00% above floor");
  });

  it("SAD case (isSad=true): returns '—' regardless of breachesBelow", () => {
    expect(formatCohortDistance("3.75", true, true)).toBe("—");
    expect(formatCohortDistance("2.00", false, true)).toBe("—");
  });

  it("null pct: returns '—' regardless of direction", () => {
    expect(formatCohortDistance(null, true, false)).toBe("—");
    expect(formatCohortDistance(null, false, false)).toBe("—");
  });

  it("zero pct: returns '0% below floor' (boundary — cohort exactly at floor)", () => {
    expect(formatCohortDistance("0", true, false)).toBe("0% below floor");
  });
});

// ---------------------------------------------------------------------------
// formatSourceId — human-readable source registry ID (Issue #DEMO6-012)
// ---------------------------------------------------------------------------

describe("formatSourceId — source registry ID to human-readable label", () => {
  it("ECOWAS_REGIONAL_2023 → 'Ecowas Regional 2023'", () => {
    expect(formatSourceId("ECOWAS_REGIONAL_2023")).toBe("Ecowas Regional 2023");
  });

  it("IMF_WEO_2023 → 'Imf Weo 2023'", () => {
    expect(formatSourceId("IMF_WEO_2023")).toBe("Imf Weo 2023");
  });

  it("WORLD_BANK_WDI_2022 → 'World Bank Wdi 2022'", () => {
    expect(formatSourceId("WORLD_BANK_WDI_2022")).toBe("World Bank Wdi 2022");
  });

  it("null → '—'", () => {
    expect(formatSourceId(null)).toBe("—");
  });

  it("undefined → '—'", () => {
    expect(formatSourceId(undefined)).toBe("—");
  });

  it("empty string → '—'", () => {
    expect(formatSourceId("")).toBe("—");
  });

  it("numeric year part is preserved unchanged", () => {
    expect(formatSourceId("V_DEM_2024")).toBe("V Dem 2024");
  });
});
