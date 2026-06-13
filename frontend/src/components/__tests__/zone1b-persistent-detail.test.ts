/**
 * Vitest: Zone 1B Persistent-Detail — unit tests for new pure functions.
 *
 * Authored BEFORE implementation from intent document at:
 * docs/process/intents/ADR-014-2026-06-13-alert-panel-ux.md
 *
 * Covers:
 *   - sortAlerts 4-level ranking rule (confidence_tier tertiary; stable L4 fallback)
 *   - getDetailStatusText — mode-dependent tense in detail slot (UX sign-off condition 2)
 *   - entity_id propagation — Zone1BAlert type includes entity_id field
 *
 * AC references: AC-2 (TERMINAL ranking), AC-8 (mode-dependent tense), AC-10 (per-step tier)
 */
import { describe, it, expect } from "vitest";
import {
  sortAlerts,
  getDetailStatusText,
} from "../MDAAlertPanelZone1B";
import type { Zone1BAlert } from "../../store/scenarioStepStore";

// ---------------------------------------------------------------------------
// Fixture helper
// ---------------------------------------------------------------------------

function makeAlert(
  overrides: Partial<Zone1BAlert> & Pick<Zone1BAlert, "severity" | "step_index">,
): Zone1BAlert {
  return {
    mda_id: `mda-${overrides.severity}-${overrides.step_index}-${Math.random().toString(36).slice(2, 6)}`,
    entity_id: overrides.entity_id ?? "GRC",
    indicator_key: "reserve_coverage_months",
    indicator_name: "Reserve Coverage Months",
    framework: "financial",
    cohort: null,
    confidence_tier: overrides.confidence_tier ?? 2,
    causal_attribution: overrides.causal_attribution ?? null,
    floor_value: "3.0000",
    current_value: "1.8420",
    approach_pct_remaining: overrides.approach_pct_remaining ?? "-0.3860",
    consecutive_breach_steps: overrides.consecutive_breach_steps ?? 1,
    recovery_horizon_years: null,
    ...overrides,
  };
}

// ---------------------------------------------------------------------------
// sortAlerts — 4-level ranking rule
// Level 1: severity DESC (TERMINAL=0, CRITICAL=1, WARNING=2)
// Level 2: step_index ASC (earlier breach first)
// Level 3: confidence_tier ASC (lower = more confident = ranks first)
// Level 4: stable insertion-order (population tiebreak not available)
// ---------------------------------------------------------------------------

describe("sortAlerts — 4-level ranking rule (ADR-014 §5.3)", () => {
  describe("Level 1: severity", () => {
    it("TERMINAL ranks before CRITICAL regardless of step_index", () => {
      const alerts = [
        makeAlert({ severity: "CRITICAL", step_index: 1 }),
        makeAlert({ severity: "TERMINAL", step_index: 3 }),
      ];
      const sorted = sortAlerts(alerts);
      expect(sorted[0].severity).toBe("TERMINAL");
      expect(sorted[1].severity).toBe("CRITICAL");
    });

    it("CRITICAL ranks before WARNING", () => {
      const alerts = [
        makeAlert({ severity: "WARNING", step_index: 1 }),
        makeAlert({ severity: "CRITICAL", step_index: 2 }),
      ];
      const sorted = sortAlerts(alerts);
      expect(sorted[0].severity).toBe("CRITICAL");
      expect(sorted[1].severity).toBe("WARNING");
    });

    it("full severity sort: TERMINAL → CRITICAL → WARNING", () => {
      const alerts = [
        makeAlert({ severity: "WARNING", step_index: 1 }),
        makeAlert({ severity: "TERMINAL", step_index: 3 }),
        makeAlert({ severity: "CRITICAL", step_index: 2 }),
      ];
      const sorted = sortAlerts(alerts);
      expect(sorted[0].severity).toBe("TERMINAL");
      expect(sorted[1].severity).toBe("CRITICAL");
      expect(sorted[2].severity).toBe("WARNING");
    });
  });

  describe("Level 2: step_index ASC (within same severity)", () => {
    it("earlier step_index ranks first within same severity", () => {
      const alerts = [
        makeAlert({ severity: "CRITICAL", step_index: 4 }),
        makeAlert({ severity: "CRITICAL", step_index: 1 }),
        makeAlert({ severity: "CRITICAL", step_index: 2 }),
      ];
      const sorted = sortAlerts(alerts);
      expect(sorted[0].step_index).toBe(1);
      expect(sorted[1].step_index).toBe(2);
      expect(sorted[2].step_index).toBe(4);
    });

    it("earlier step ranks first among two TERMINAL alerts (strongest consecutive argument)", () => {
      const t1 = makeAlert({ severity: "TERMINAL", step_index: 1, consecutive_breach_steps: 4 });
      const t2 = makeAlert({ severity: "TERMINAL", step_index: 3, consecutive_breach_steps: 2 });
      const sorted = sortAlerts([t2, t1]);
      expect(sorted[0].mda_id).toBe(t1.mda_id); // earliest step first
    });
  });

  describe("Level 3: confidence_tier ASC (within same severity + step_index)", () => {
    it("lower confidence_tier (higher confidence) ranks first", () => {
      const highConf = makeAlert({ severity: "CRITICAL", step_index: 2, confidence_tier: 2 });
      const modConf = makeAlert({ severity: "CRITICAL", step_index: 2, confidence_tier: 3 });
      const lowConf = makeAlert({ severity: "CRITICAL", step_index: 2, confidence_tier: 4 });

      const sorted = sortAlerts([modConf, lowConf, highConf]);
      expect(sorted[0].mda_id).toBe(highConf.mda_id); // tier 2 is most confident
      expect(sorted[1].mda_id).toBe(modConf.mda_id);  // tier 3
      expect(sorted[2].mda_id).toBe(lowConf.mda_id);  // tier 4
    });

    it("tier 2 (IMF Article IV) ranks above tier 4 (synthetic direction-only)", () => {
      const realData = makeAlert({ severity: "TERMINAL", step_index: 1, confidence_tier: 2 });
      const synthetic = makeAlert({ severity: "TERMINAL", step_index: 1, confidence_tier: 4 });
      const sorted = sortAlerts([synthetic, realData]);
      expect(sorted[0].mda_id).toBe(realData.mda_id);
    });
  });

  describe("Level 4: stable insertion-order fallback", () => {
    it("alerts tying on levels 1–3 preserve their input order", () => {
      // Same severity, step_index, confidence_tier — from different entities
      const a = makeAlert({ mda_id: "mda-A", severity: "CRITICAL", step_index: 2, confidence_tier: 3, entity_id: "JOR" });
      const b = makeAlert({ mda_id: "mda-B", severity: "CRITICAL", step_index: 2, confidence_tier: 3, entity_id: "EGY" });
      const c = makeAlert({ mda_id: "mda-C", severity: "CRITICAL", step_index: 2, confidence_tier: 3, entity_id: "LBN" });

      const sorted = sortAlerts([a, b, c]);
      // Stable sort: original order preserved for ties
      expect(sorted[0].mda_id).toBe("mda-A");
      expect(sorted[1].mda_id).toBe("mda-B");
      expect(sorted[2].mda_id).toBe("mda-C");
    });
  });

  describe("multi-entity Hormuz scenario (Q1 ruling)", () => {
    it("JOR TERMINAL at step 1 ranks before EGY TERMINAL at step 3", () => {
      const jor = makeAlert({ severity: "TERMINAL", step_index: 1, entity_id: "JOR" });
      const egy = makeAlert({ severity: "TERMINAL", step_index: 3, entity_id: "EGY" });
      const sorted = sortAlerts([egy, jor]);
      expect(sorted[0].entity_id).toBe("JOR"); // earlier step first
    });

    it("two TERMINAL alerts at same step: lower confidence_tier wins", () => {
      const jorTier2 = makeAlert({ severity: "TERMINAL", step_index: 1, confidence_tier: 2, entity_id: "JOR" });
      const egyTier3 = makeAlert({ severity: "TERMINAL", step_index: 1, confidence_tier: 3, entity_id: "EGY" });
      const sorted = sortAlerts([egyTier3, jorTier2]);
      expect(sorted[0].entity_id).toBe("JOR"); // lower tier = higher confidence
    });
  });
});

// ---------------------------------------------------------------------------
// getDetailStatusText — mode-dependent tense (UX sign-off condition 2)
// ---------------------------------------------------------------------------

describe("getDetailStatusText — mode-dependent tense in detail slot", () => {
  describe("Mode 1 — historical past tense", () => {
    it("breached alert in Mode 1: contains 'crossed threshold at step N'", () => {
      const alert = makeAlert({ severity: "TERMINAL", step_index: 3, approach_pct_remaining: "-0.386" });
      const text = getDetailStatusText(alert, "MODE_1");
      expect(text).toContain("crossed");
      expect(text).toContain("step 3");
      expect(text).not.toContain("BREACHED");
      expect(text).not.toContain("projected");
    });

    it("approaching alert in Mode 1: 'N% above floor at step N'", () => {
      const alert = makeAlert({ severity: "WARNING", step_index: 2, approach_pct_remaining: "0.150" });
      const text = getDetailStatusText(alert, "MODE_1");
      expect(text).toContain("above floor");
      expect(text).toContain("step");
      expect(text).not.toContain("projected");
      expect(text).not.toContain("BREACHED");
    });
  });

  describe("Mode 2 — projected future tense", () => {
    it("breached alert in Mode 2: contains 'BREACH PROJECTED at step N'", () => {
      const alert = makeAlert({ severity: "CRITICAL", step_index: 5, approach_pct_remaining: "-0.050" });
      const text = getDetailStatusText(alert, "MODE_2");
      expect(text.toLowerCase()).toContain("projected");
      expect(text).toContain("step 5");
      expect(text).not.toContain("crossed");
      expect(text).not.toContain("BREACHED");
    });

    it("approaching alert in Mode 2: 'N% above floor (projected)'", () => {
      const alert = makeAlert({ severity: "WARNING", step_index: 4, approach_pct_remaining: "0.200" });
      const text = getDetailStatusText(alert, "MODE_2");
      expect(text).toContain("above floor");
      expect(text.toLowerCase()).toContain("projected");
      expect(text).not.toContain("crossed");
    });
  });

  describe("Mode 3 — real-time present tense", () => {
    it("breached alert in Mode 3: 'BREACHED'", () => {
      const alert = makeAlert({ severity: "TERMINAL", step_index: 1, approach_pct_remaining: "-0.386" });
      const text = getDetailStatusText(alert, "MODE_3");
      expect(text).toContain("BREACHED");
      expect(text).not.toContain("projected");
      expect(text).not.toContain("crossed");
    });

    it("approaching alert in Mode 3: 'N% above floor'", () => {
      const alert = makeAlert({ severity: "WARNING", step_index: 2, approach_pct_remaining: "0.250" });
      const text = getDetailStatusText(alert, "MODE_3");
      expect(text).toContain("above floor");
      expect(text).not.toContain("projected");
      expect(text).not.toContain("crossed");
      expect(text).not.toContain("BREACHED");
    });
  });

  describe("edge cases", () => {
    it("approach_pct_remaining exactly 0 counts as BREACHED in Mode 3", () => {
      const alert = makeAlert({ severity: "CRITICAL", step_index: 1, approach_pct_remaining: "0.000" });
      const text = getDetailStatusText(alert, "MODE_3");
      expect(text).toContain("BREACHED");
    });

    it("confidence tier label does not change based on consecutive_breach_steps (AC-10)", () => {
      const alertStep1 = makeAlert({ severity: "TERMINAL", step_index: 1, confidence_tier: 3, consecutive_breach_steps: 1 });
      const alertStep4 = makeAlert({ ...alertStep1, consecutive_breach_steps: 4 });
      // getDetailStatusText does not take confidence tier — tested via getNegotiationLabel stability
      // Both alerts have same severity / mode — status text must be consistent
      const text1 = getDetailStatusText(alertStep1, "MODE_3");
      const text4 = getDetailStatusText(alertStep4, "MODE_3");
      expect(text1).toBe(text4);
    });
  });
});

// ---------------------------------------------------------------------------
// entity_id field presence in Zone1BAlert (Q1 ruling — no deduplication)
// ---------------------------------------------------------------------------

describe("Zone1BAlert entity_id field", () => {
  it("entity_id field is accessible on Zone1BAlert objects", () => {
    const alert = makeAlert({ severity: "TERMINAL", step_index: 1, entity_id: "JOR" });
    expect(alert.entity_id).toBe("JOR");
  });

  it("sortAlerts preserves entity_id on each sorted alert", () => {
    const jor = makeAlert({ severity: "TERMINAL", step_index: 1, entity_id: "JOR" });
    const egy = makeAlert({ severity: "CRITICAL", step_index: 2, entity_id: "EGY" });
    const sorted = sortAlerts([egy, jor]);
    expect(sorted[0].entity_id).toBe("JOR"); // TERMINAL first
    expect(sorted[1].entity_id).toBe("EGY");
  });
});
