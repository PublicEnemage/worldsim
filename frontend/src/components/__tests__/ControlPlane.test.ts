/**
 * Vitest: ControlPlane — unit tests (G6b, Issue #753).
 *
 * Covers pure functions exported from ControlPlane.tsx:
 *   - formatFiscalMultiplier: display format (e.g. 1.50×)
 *   - formatLegitimacyIndex: display format (e.g. 75%)
 *
 * Component behaviour (slider interaction, apply button, disable state)
 * is covered by the Playwright E2E tests in tests/e2e/mode3-active-control.spec.ts.
 */
import { describe, it, expect } from "vitest";
import { formatFiscalMultiplier, formatLegitimacyIndex } from "../ControlPlane";

// ---------------------------------------------------------------------------
// formatFiscalMultiplier
// ---------------------------------------------------------------------------

describe("formatFiscalMultiplier", () => {
  it("formats 1.0 as '1.00×'", () => {
    expect(formatFiscalMultiplier(1.0)).toBe("1.00×");
  });

  it("formats 1.5 as '1.50×'", () => {
    expect(formatFiscalMultiplier(1.5)).toBe("1.50×");
  });

  it("formats 0.1 as '0.10×'", () => {
    expect(formatFiscalMultiplier(0.1)).toBe("0.10×");
  });

  it("formats 3.0 as '3.00×'", () => {
    expect(formatFiscalMultiplier(3.0)).toBe("3.00×");
  });

  it("always produces exactly two decimal places", () => {
    const result = formatFiscalMultiplier(1.125);
    expect(result).toMatch(/^\d+\.\d{2}×$/);
  });

  it("ends with the × character", () => {
    expect(formatFiscalMultiplier(2.0)).toContain("×");
    expect(formatFiscalMultiplier(2.0).at(-1)).toBe("×");
  });
});

// ---------------------------------------------------------------------------
// formatLegitimacyIndex
// ---------------------------------------------------------------------------

describe("formatLegitimacyIndex", () => {
  it("formats 0.75 as '75%'", () => {
    expect(formatLegitimacyIndex(0.75)).toBe("75%");
  });

  it("formats 0.0 as '0%'", () => {
    expect(formatLegitimacyIndex(0.0)).toBe("0%");
  });

  it("formats 1.0 as '100%'", () => {
    expect(formatLegitimacyIndex(1.0)).toBe("100%");
  });

  it("rounds to nearest integer (0.506 → 51%)", () => {
    expect(formatLegitimacyIndex(0.506)).toBe("51%");
  });

  it("rounds to nearest integer (0.504 → 50%)", () => {
    expect(formatLegitimacyIndex(0.504)).toBe("50%");
  });

  it("ends with '%'", () => {
    expect(formatLegitimacyIndex(0.33)).toContain("%");
    expect(formatLegitimacyIndex(0.33).at(-1)).toBe("%");
  });
});
