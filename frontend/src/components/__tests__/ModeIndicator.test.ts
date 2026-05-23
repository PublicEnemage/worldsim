/**
 * Vitest: ModeIndicator — unit tests.
 *
 * Covers:
 *   US-026 — exact mode label text: "Replay" / "Simulation" / "Active Control"
 *   UX-RULING-3 — no raw MODE_N field names in displayed text
 *
 * These are unit tests of pure functions exported from ModeIndicator.tsx.
 * RTL render tests (act() boundary + mode switch render cycle) live in
 * atomicity-rtl.test.tsx.
 */
import { describe, it, expect } from "vitest";
import { getModeLabel, MODE_LABELS } from "../ModeIndicator";

// ---------------------------------------------------------------------------
// US-026 — getModeLabel: exact text per mode (UX-RULING-3)
// ---------------------------------------------------------------------------

describe("US-026 — getModeLabel: exact mode label text (UX-RULING-3)", () => {
  it("MODE_1 → 'Replay'", () => {
    expect(getModeLabel("MODE_1")).toBe("Replay");
  });

  it("MODE_2 → 'Simulation'", () => {
    expect(getModeLabel("MODE_2")).toBe("Simulation");
  });

  it("MODE_3 → 'Active Control'", () => {
    expect(getModeLabel("MODE_3")).toBe("Active Control");
  });

  it("all three labels are distinct", () => {
    const labels = new Set([
      getModeLabel("MODE_1"),
      getModeLabel("MODE_2"),
      getModeLabel("MODE_3"),
    ]);
    expect(labels.size).toBe(3);
  });

  it("MODE_LABELS constant matches getModeLabel for all modes", () => {
    expect(MODE_LABELS.MODE_1).toBe(getModeLabel("MODE_1"));
    expect(MODE_LABELS.MODE_2).toBe(getModeLabel("MODE_2"));
    expect(MODE_LABELS.MODE_3).toBe(getModeLabel("MODE_3"));
  });
});

// ---------------------------------------------------------------------------
// UX-RULING-3 — no raw field name strings in any label
// ---------------------------------------------------------------------------

describe("UX-RULING-3 — mode labels contain no raw field name substrings", () => {
  const modes = ["MODE_1", "MODE_2", "MODE_3"] as const;

  it("no label contains 'MODE_1'", () => {
    for (const mode of modes) {
      expect(getModeLabel(mode)).not.toContain("MODE_1");
    }
  });

  it("no label contains 'MODE_2'", () => {
    for (const mode of modes) {
      expect(getModeLabel(mode)).not.toContain("MODE_2");
    }
  });

  it("no label contains 'MODE_3'", () => {
    for (const mode of modes) {
      expect(getModeLabel(mode)).not.toContain("MODE_3");
    }
  });

  it("no label contains underscore (raw field name signal)", () => {
    for (const mode of modes) {
      expect(getModeLabel(mode)).not.toContain("_");
    }
  });

  it("'Replay' label does not start with 'Mode'", () => {
    expect(getModeLabel("MODE_1")).not.toMatch(/^Mode\s/);
  });
});
