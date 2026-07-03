/**
 * Vitest: FourFrameworkZone1D — unit tests.
 *
 * Covers:
 *   US-021 — four framework scores visible simultaneously; human-readable labels
 *   US-022 — null vs zero score CSS class and display text (UX-RULING-2)
 *   DD-011 — null governance pattern extended into Zone 1D
 *   IR-005 annotation removed — governance promoted (Issue #556)
 *
 * These are unit tests of pure functions exported from FourFrameworkZone1D.tsx.
 * Playwright E2E tests covering DOM assertions live in tests/e2e/pmm-four-framework.spec.ts.
 */
import { describe, it, expect, beforeAll } from "vitest";
import {
  formatScore,
  getScoreClass,
  FRAMEWORK_DISPLAY_LABELS,
  FRAMEWORK_ORDER,
} from "../FourFrameworkZone1D";

// ---------------------------------------------------------------------------
// US-022 — formatScore: null vs numeric display text
// ---------------------------------------------------------------------------

describe("US-022 — formatScore: null renders as '—', numeric renders as number", () => {
  it("null → '—' (em dash)", () => {
    expect(formatScore(null)).toBe("—");
  });

  it("0 → '0.00' (not '—', not blank)", () => {
    expect(formatScore(0)).toBe("0.00");
  });

  it("0.5 → '0.50'", () => {
    expect(formatScore(0.5)).toBe("0.50");
  });

  it("1 → '1.00'", () => {
    expect(formatScore(1)).toBe("1.00");
  });

  it("0.123 rounds to two decimal places", () => {
    expect(formatScore(0.123)).toBe("0.12");
  });

  it("null produces '—' not '0' or empty string", () => {
    const result = formatScore(null);
    expect(result).toBe("—");
    expect(result).not.toBe("0");
    expect(result).not.toBe("");
    expect(result).not.toBe("0.00");
  });

  it("zero produces numeric text, not '—'", () => {
    const result = formatScore(0);
    expect(result).not.toBe("—");
    expect(result).toMatch(/^\d/);
  });
});

// ---------------------------------------------------------------------------
// US-022 — getScoreClass: CSS class assignment (UX-RULING-2)
// ---------------------------------------------------------------------------

describe("US-022 — getScoreClass: CSS class by score type (UX-RULING-2)", () => {
  it("null → 'score-value--null'", () => {
    expect(getScoreClass(null)).toBe("score-value--null");
  });

  it("0 → 'score-value--numeric'", () => {
    expect(getScoreClass(0)).toBe("score-value--numeric");
  });

  it("positive value → 'score-value--numeric'", () => {
    expect(getScoreClass(0.75)).toBe("score-value--numeric");
  });

  it("null and zero produce different classes (core US-022 contract)", () => {
    expect(getScoreClass(null)).not.toBe(getScoreClass(0));
  });

  it("zero and positive value produce the same class", () => {
    expect(getScoreClass(0)).toBe(getScoreClass(1));
  });

  it("'score-value--null' is the exact string for null", () => {
    expect(getScoreClass(null)).toBe("score-value--null");
  });

  it("'score-value--numeric' is the exact string for numeric", () => {
    expect(getScoreClass(0.5)).toBe("score-value--numeric");
  });
});

// ---------------------------------------------------------------------------
// US-021 — FRAMEWORK_DISPLAY_LABELS: human-readable labels (no raw field names)
// ---------------------------------------------------------------------------

describe("US-021 — FRAMEWORK_DISPLAY_LABELS: human-readable framework labels", () => {
  it("financial → 'Financial'", () => {
    expect(FRAMEWORK_DISPLAY_LABELS.financial).toBe("Financial");
  });

  it("human_development → 'Human Development'", () => {
    expect(FRAMEWORK_DISPLAY_LABELS.human_development).toBe("Human Development");
  });

  it("ecological → 'Ecological'", () => {
    expect(FRAMEWORK_DISPLAY_LABELS.ecological).toBe("Ecological");
  });

  it("governance → 'Governance'", () => {
    expect(FRAMEWORK_DISPLAY_LABELS.governance).toBe("Governance");
  });

  it("no label equals its raw database field name", () => {
    expect(FRAMEWORK_DISPLAY_LABELS.financial).not.toBe("financial");
    expect(FRAMEWORK_DISPLAY_LABELS.human_development).not.toBe("human_development");
    expect(FRAMEWORK_DISPLAY_LABELS.ecological).not.toBe("ecological");
    expect(FRAMEWORK_DISPLAY_LABELS.governance).not.toBe("governance");
  });

  it("no label contains underscores (raw field name signal)", () => {
    for (const label of Object.values(FRAMEWORK_DISPLAY_LABELS)) {
      expect(label).not.toContain("_");
    }
  });
});

// ---------------------------------------------------------------------------
// FRAMEWORK_ORDER: all four frameworks present
// ---------------------------------------------------------------------------

describe("FRAMEWORK_ORDER: canonical display order", () => {
  it("contains exactly four frameworks", () => {
    expect(FRAMEWORK_ORDER).toHaveLength(4);
  });

  it("contains all four expected framework keys", () => {
    const keys = [...FRAMEWORK_ORDER];
    expect(keys).toContain("financial");
    expect(keys).toContain("human_development");
    expect(keys).toContain("ecological");
    expect(keys).toContain("governance");
  });

  it("each framework key has a display label", () => {
    for (const key of FRAMEWORK_ORDER) {
      expect(FRAMEWORK_DISPLAY_LABELS[key]).toBeTruthy();
    }
  });
});

// ---------------------------------------------------------------------------
// M18-G7-D: AC-D2 — DRIVER_LABELS exhaustive (red until G7-D export fix)
//
// `DRIVER_LABELS` is currently a private `const` in FourFrameworkZone1D.tsx.
// The G7-D fix exports it so the psp-driver-row render logic is testable.
//
// RED state: DRIVER_LABELS is undefined (not exported) → all assertions fail.
// GREEN state (after G7-D): exported with all four valid psp_dominant_driver keys.
//
// Source: M18-G7-D intent §AC-D2 + root cause analysis §Root Cause 4 §DEMO-132.
// ---------------------------------------------------------------------------

describe("M18-G7-D: AC-D2 — DRIVER_LABELS mapping exhaustive", () => {
  let DRIVER_LABELS: unknown;

  beforeAll(async () => {
    const mod = await import("../FourFrameworkZone1D");
    DRIVER_LABELS = (mod as Record<string, unknown>).DRIVER_LABELS;
  });

  it("DRIVER_LABELS is exported from FourFrameworkZone1D (RED until G7-D export fix)", () => {
    expect(typeof DRIVER_LABELS).toBe("object");
    expect(DRIVER_LABELS).not.toBeNull();
  });

  it("AC-D2: has 'fiscal_sustainability' key", () => {
    const labels = DRIVER_LABELS as Record<string, string> | undefined;
    expect(labels).toBeDefined();
    expect(labels?.fiscal_sustainability).toBeTruthy();
  });

  it("AC-D2: has 'governance' key", () => {
    const labels = DRIVER_LABELS as Record<string, string> | undefined;
    expect(labels?.governance).toBeTruthy();
  });

  it("AC-D2: has 'external_balance' key", () => {
    const labels = DRIVER_LABELS as Record<string, string> | undefined;
    expect(labels?.external_balance).toBeTruthy();
  });

  it("AC-D2: has 'social_stability' key", () => {
    const labels = DRIVER_LABELS as Record<string, string> | undefined;
    expect(labels?.social_stability).toBeTruthy();
  });

  it("AC-D2: unknown driver key returns undefined (psp-driver-row must guard against unknown keys)", () => {
    // The component conditionally renders: `pspDominantDriver != null && DRIVER_LABELS[pspDominantDriver]`
    // An unknown key must resolve to undefined (falsy) so the row is suppressed, not blank.
    const labels = DRIVER_LABELS as Record<string, string> | undefined;
    if (labels) {
      expect(labels["unknown_driver_key"]).toBeUndefined();
    }
  });
});

// ---------------------------------------------------------------------------
// M19-G5: ADR-017 §Zone 1D Integration (Mode 3) — formatDelta + getDeltaColor
//
// These tests will be RED until the implementing agent exports `formatDelta` and
// `getDeltaColor` from FourFrameworkZone1D.tsx (Issue #1630).
//
// Function contracts (from intent doc M19-G5-2026-07-03-zone1d-delta-annotations.md):
//
//   formatDelta(current: number | null, baseline: number | null): string | null
//     Returns:  "(+N.NN)"  when delta > 0.005
//               "(−N.NN)"  when delta < −0.005  (uses en-dash U+2212, or minus sign)
//               "(±0.00)"  when |delta| ≤ 0.005
//               null       when current or baseline is null
//
//   getDeltaColor(delta: number): string
//     Returns:  "#16A34A"  when delta > 0.005   (green — improvement)
//               "#D97706"  when delta < −0.005  (amber — decline)
//               "#9CA3AF"  when |delta| ≤ 0.005 (gray — no change)
//
// Source: intent doc §Annotation rules, §AC-3 Color coding.
// ---------------------------------------------------------------------------

describe("M19-G5: formatDelta — Mode 3 Zone 1D per-framework delta annotation (ADR-017 §Zone 1D)", () => {
  let formatDelta: ((current: number | null, baseline: number | null) => string | null) | undefined;

  beforeAll(async () => {
    const mod = await import("../FourFrameworkZone1D");
    formatDelta = (mod as Record<string, unknown>).formatDelta as typeof formatDelta;
  });

  it("formatDelta is exported from FourFrameworkZone1D (RED until M19-G5 implementation)", () => {
    expect(typeof formatDelta).toBe("function");
  });

  it("positive delta (0.04) → '(+0.04)'", () => {
    if (!formatDelta) return;
    expect(formatDelta(0.71, 0.67)).toBe("(+0.04)");
  });

  it("positive delta (0.07) → '(+0.07)'", () => {
    if (!formatDelta) return;
    expect(formatDelta(0.62, 0.55)).toBe("(+0.07)");
  });

  it("negative delta (−0.02) → contains '0.02' and a minus/en-dash", () => {
    if (!formatDelta) return;
    const result = formatDelta(0.69, 0.71);
    expect(result).not.toBeNull();
    expect(result).toMatch(/0\.02/);
    // Accepts either standard minus '-', en-dash '–', or minus sign '−'
    expect(result).toMatch(/[−\-–]/);
  });

  it("near-zero delta (|Δ| = 0.004 ≤ 0.005) → '(±0.00)'", () => {
    if (!formatDelta) return;
    expect(formatDelta(0.714, 0.710)).toBe("(±0.00)");
  });

  it("exactly zero delta → '(±0.00)'", () => {
    if (!formatDelta) return;
    expect(formatDelta(0.510, 0.510)).toBe("(±0.00)");
  });

  it("exactly at threshold (|Δ| = 0.005) → near-zero '(±0.00)'", () => {
    if (!formatDelta) return;
    // 0.005 is the boundary; |Δ| ≤ 0.005 → gray near-zero treatment
    expect(formatDelta(0.505, 0.500)).toBe("(±0.00)");
  });

  it("null current → null (no annotation when current score unavailable)", () => {
    if (!formatDelta) return;
    expect(formatDelta(null, 0.67)).toBeNull();
  });

  it("null baseline → null (no annotation when baseline unavailable)", () => {
    if (!formatDelta) return;
    expect(formatDelta(0.71, null)).toBeNull();
  });

  it("both null → null", () => {
    if (!formatDelta) return;
    expect(formatDelta(null, null)).toBeNull();
  });

  it("result string includes parentheses (visual format contract)", () => {
    if (!formatDelta) return;
    const result = formatDelta(0.71, 0.67);
    expect(result).toMatch(/^\(/);
    expect(result).toMatch(/\)$/);
  });
});

describe("M19-G5: getDeltaColor — Mode 3 Zone 1D delta color coding (ADR-017 §Zone 1D)", () => {
  let getDeltaColor: ((delta: number) => string) | undefined;

  beforeAll(async () => {
    const mod = await import("../FourFrameworkZone1D");
    getDeltaColor = (mod as Record<string, unknown>).getDeltaColor as typeof getDeltaColor;
  });

  it("getDeltaColor is exported from FourFrameworkZone1D (RED until M19-G5 implementation)", () => {
    expect(typeof getDeltaColor).toBe("function");
  });

  it("positive delta (0.04) → green '#16A34A' (improvement)", () => {
    if (!getDeltaColor) return;
    expect(getDeltaColor(0.04)).toBe("#16A34A");
  });

  it("negative delta (−0.02) → amber '#D97706' (decline, warning tone)", () => {
    if (!getDeltaColor) return;
    expect(getDeltaColor(-0.02)).toBe("#D97706");
  });

  it("near-zero delta (0.003) → gray '#9CA3AF' (no change)", () => {
    if (!getDeltaColor) return;
    expect(getDeltaColor(0.003)).toBe("#9CA3AF");
  });

  it("exactly zero → gray '#9CA3AF'", () => {
    if (!getDeltaColor) return;
    expect(getDeltaColor(0)).toBe("#9CA3AF");
  });

  it("threshold boundary: delta = 0.005 → gray '#9CA3AF' (≤ threshold)", () => {
    if (!getDeltaColor) return;
    expect(getDeltaColor(0.005)).toBe("#9CA3AF");
  });

  it("just above threshold: delta = 0.006 → green '#16A34A'", () => {
    if (!getDeltaColor) return;
    expect(getDeltaColor(0.006)).toBe("#16A34A");
  });

  it("negative threshold boundary: delta = −0.005 → gray '#9CA3AF' (|Δ| ≤ threshold)", () => {
    if (!getDeltaColor) return;
    expect(getDeltaColor(-0.005)).toBe("#9CA3AF");
  });

  it("just below negative threshold: delta = −0.006 → amber '#D97706'", () => {
    if (!getDeltaColor) return;
    expect(getDeltaColor(-0.006)).toBe("#D97706");
  });

  it("positive and negative produce different colors (not accidentally same)", () => {
    if (!getDeltaColor) return;
    expect(getDeltaColor(0.04)).not.toBe(getDeltaColor(-0.04));
  });

  it("return value is a valid hex color string starting with '#'", () => {
    if (!getDeltaColor) return;
    const color = getDeltaColor(0.04);
    expect(color).toMatch(/^#[0-9A-Fa-f]{6}$/);
  });
});
