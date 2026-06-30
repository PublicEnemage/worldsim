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
