# Calibration Registry

Append-only record of backtesting calibration results. Each entry documents
one fidelity assessment against historical data, the resulting tier, and whether
structural priors were retained or replaced by posterior multipliers.

**Authority:** ADR-007 Amendment 1 §8.2–§8.5, §8.9 (ARCH-016, accepted 2026-07-03)
**Gate:** `is_pre_calibration=False` requires MAGNITUDE_MATCH tier + accepted entry
here + Architect sign-off + CM sign-off.

---

## Entry CAL-001

| Field | Value |
|---|---|
| Case ID | SEN-2014-2019 |
| Country | Senegal |
| Programme window | 2014–2019 (IMF ECF) |
| Fidelity tier achieved | DIRECTION_ONLY |
| Empirical C_mag (T3) | < 0.05 (below C_MAG_FLOOR; measurement pending full G2B fixture run) |
| Empirical C_dir (T3) | Pending G2B SEN fixture completion |
| Correction factor (T3) | EVIDENCE_INSUFFICIENT (C_mag < 0.05) |
| Posterior multiplier (T3) | N/A — structural prior retained |
| Provisional κ_prov (T3) | Pending G2B SEN fixture completion |
| Calibration date | 2026-07-03 |
| Status | PROVISIONAL — DIRECTION_ONLY only; structural prior retained; `is_pre_calibration` remains True |
| affected_indicators_excluded | `external_sector_balance`, `export_volume` (CommodityShockConfig direction mismatch — Issue #1541) |
| Architect sign-off | Pending |
| CM sign-off | Pending |

**Rationale:** SEN 2014–2019 achieves directional fidelity (GDP growth trajectory
direction confirmed) but does not achieve MAGNITUDE_MATCH. C_mag < C_MAG_FLOOR
(0.05) because the fiscal multiplier composite deviates significantly from
historical magnitudes, driven partly by the CommodityShockConfig direction
mismatch documented in #1541. Structural priors retained unchanged.

**Forward trace:** MAGNITUDE_MATCH requires the #1541 direction mismatch to be
resolved AND a re-run producing ≥5 valid pairs with ≥50% within 20%. ZMB
2005–2015 is the next calibration target.
