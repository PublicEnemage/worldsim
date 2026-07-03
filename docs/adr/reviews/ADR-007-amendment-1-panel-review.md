---
name: ADR-007-amendment-1-panel-review
type: adr-panel-review
adr: ADR-007 Amendment 1
amendment: 1
milestone: M19 — Constraint Search and Empirical Calibration
status: In progress
authored-date: 2026-07-02
---

# ADR-007 Amendment 1 — Panel Review

**Amendment:** Bayesian Posterior Calibration Layer + Section 6 Implementation Clause
**ADR:** `docs/adr/ADR-007-synthetic-data-framework.md §Amendment 1`
**Amending sections:** Section 6 (implementation clause) + new Section 8
**Panel authority:** ARCH-016 (ADR backlog entry 2026-07-02)

---

## Panel Composition

| Reviewer | Role | Status |
|---|---|---|
| Architect Agent | R — author | Complete ✓ (2026-07-02) |
| Chief Methodologist (DIC) | C — posterior calibration method and coverage measurement protocol | **Pending** |
| Computation Engine Agent | C — implementation feasibility of §6 clause and §8.3 MAGNITUDE_MATCH gate | **Pending** |
| UX Designer Agent | C — display contract for is_pre_calibration and band_method (#1537) | **Pending** |
| Engineering Lead | A — final acceptance authority | **Pending** |

*NM-084 gate: PI Agent must post gate comment on the implementation PR for #1543 confirming
CM sign-off before auto-merge is set.*

---

## Chief Methodologist — Review

**Activation:** `Chief Methodologist: VALIDATE — ADR-007 Amendment 1 posterior calibration method`
**Date:** 2026-07-02

The amendment's coverage measurement protocol (§8.2) and correction factor formula (§8.4) are statistically sound for the evidence available. Square-root dampening is appropriate for a two-case calibration set; it errs toward wider bands rather than narrower ones, which is the correct failure direction for a tool serving data-poor environments.

The MAGNITUDE_MATCH gate (§8.3) is correctly framed as a precondition — ensuring the model is in the right ballpark before CI coverage is measured, not itself a CI calibration metric. Point-estimate accuracy and CI coverage are independent properties; the amendment should note this distinction in §8.4 to prevent readers from conflating them.

**Condition A (INCORPORATE):** §8.4 must specify a `C_mag` floor. If `C_mag = 0`, the formula produces `sqrt(0.80/0) = ∞`, consumed by the clamp. Floor: `max(C_mag, 0.05)`. If `C_mag < 0.05`, record the registry entry with status `EVIDENCE_INSUFFICIENT` and do not update the multiplier. Structural prior remains in use for that tier.

**Condition B (INCORPORATE):** SEN's CommodityShockConfig export/import direction mismatch (#1541 known gap) compromises directional coverage for external-sector-sensitive indicators. The calibration registry entry for SEN must record `affected_indicators_excluded: list[str]` and measure coverage over the clean-indicator subset only.

With conditions A and B incorporated: **VALIDATE**.

— Chief Methodologist (in-session, 2026-07-02)

---

## Computation Engine Agent — Review

**Activation:** `Computation Engine Agent: VALIDATE — ADR-007 Amendment 1 implementation of §6 clause and §8.3 MAGNITUDE_MATCH gate`
**Date:** 2026-07-02

**§6 clause:** Implementable as written. Detection (`clipped_lower AND clipped_upper AND ci_upper - ci_lower == natural_upper - natural_lower`) is exact under `Decimal` arithmetic — no floating-point tolerance needed. `BandResult` field additions (`band_method`, `is_meaningless`, `suppressed_reason`) with Python dataclass defaults are backwards-compatible: all existing constructions use keyword arguments.

**Condition A (scope gap — resolve in #1543 intent doc):** `_classify_fidelity()` currently receives only `per_step_records` (model output). MAGNITUDE_MATCH requires historical reference values alongside model output. Preferred resolution: extend `per_step_records` dicts with a `"hist_value"` key populated by the harness when historical data is present. Option 2: separate `reference_records` parameter. The #1543 intent document must specify which option is adopted. **The #1543 implementation PR must not open until this interface is specified.**

**Condition B (scope gap — resolve in #1543 intent doc):** §8.5 says `compute_band()` "reads the most recent accepted entry per tier at startup." `compute_band()` is currently a pure function. Recommended pattern: module-level `_CALIBRATION_MULTIPLIERS: dict[int, Decimal]` (structural priors by default) overridable via `set_calibration_multipliers(m: dict[int, Decimal])` for testing — no file I/O in the hot path. The intent doc must adopt this pattern or a documented equivalent.

Both conditions are intent-doc–level scope gaps, not amendment defects. **VALIDATE**.

— Computation Engine Agent (in-session, 2026-07-02)

---

## UX Designer Agent — Review (Consultation)

**Activation:** `UX Designer Agent: CHALLENGE — ADR-007 Amendment 1 display contract for is_pre_calibration and band_method (#1537)`
**Governing documents reviewed:** `docs/ux/information-hierarchy.md §Confidence and Uncertainty Display`; `docs/ux/north-star.md §Primary Cognitive Tasks`
**Date:** 2026-07-02 — same session as ADR authorship, acknowledged

Three concerns found.

**Concern 1 — Enum stability (INCORPORATE):** `band_method` values are frozen API the moment G3 #1537 merges. G4 #1529 hardcodes label strings keyed to these exact values. Add stability clause to §8.7: values may not be renamed post-merge; new values may be appended; any addition requires a minor amendment entry.

**Concern 2 — Suppressed CI slot (INCORPORATE):** When `is_meaningless=True`, "suppressed entirely" leaves a blank slot that forces the analyst to investigate the absence. The display contract must specify a placeholder: "Data range too wide for confidence interval." G3 #1537's intent document must include this as a frontend acceptance criterion.

**Concern 3 — Provisional state UI treatment (flag for #1537 intent doc):** "PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL" is the state Aicha encounters at Demo 8. If it has no UI treatment, the north star test conditional PASS becomes a FAIL. G3 #1537's intent document must include a display contract table for all four `band_method` states — what each state must show, even if label strings are delegated to G4 #1529.

Concerns 1+2 are INCORPORATE items. Concern 3 is a flag for #1537 intent doc. **CONSULT — no objection to acceptance** once 1+2 are incorporated.

— UX Designer Agent (in-session, same session as ADR authorship — acknowledged; 2026-07-02)

---

## Engineering Lead — Acceptance

*[EL acceptance to be recorded here]*

---

## Acceptance Vote Summary

| Reviewer | Verdict | Date | Conditions |
|---|---|---|---|
| Architect Agent | AUTHOR | 2026-07-02 | — |
| Chief Methodologist | VALIDATE (conditional) | 2026-07-02 | Conditions A + B — INCORPORATE |
| Computation Engine Agent | VALIDATE (conditional) | 2026-07-02 | Conditions A + B — scope gaps in #1543 intent doc |
| UX Designer Agent | CONSULT — no objection | 2026-07-02 | Concerns 1+2 INCORPORATE; Concern 3 in #1537 intent doc |
| Engineering Lead | Pending | — | — |
