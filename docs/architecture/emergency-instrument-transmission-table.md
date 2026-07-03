# Emergency Instrument Transmission Table

> **Authority:** ADR-020, Decision 1 and Decision 2.
> **Owner:** Architect Agent (authorship), Computation Engine Agent (implementation verification).
> **Update rule:** This table must be updated in the same PR as any new EmergencyInstrument
> variant introduction. A variant with no non-governance channel must have an explicit
> "intentional — governance-only" entry rather than a blank. Missing entries are a compliance
> finding. CE Agent verifies this table against live module subscription registry before any
> EmergencyInstrument PR merges.
>
> Last updated: 2026-07-03 (ADR-020 — capital controls channels; full audit pending CE)

---

## Canonical Event String Registry

Format: `emergency_policy_{instrument_name}`

| Instrument variant | Canonical event string |
|---|---|
| `imf_program_acceptance` | `emergency_policy_imf_program_acceptance` |
| `debt_moratorium` | `emergency_policy_debt_moratorium` |
| `default_declaration` | `emergency_policy_default_declaration` |
| `capital_controls` | `emergency_policy_capital_controls` |
| `emergency_austerity` | `emergency_policy_emergency_austerity` |
| `asset_nationalization` | `emergency_policy_asset_nationalization` |
| `currency_peg_break` | `emergency_policy_currency_peg_break` |
| `hyperinflation_emergency` | `emergency_policy_hyperinflation_emergency` |
| `banking_system_freeze` | `emergency_policy_banking_system_freeze` |
| `debt_restructuring` | `emergency_policy_debt_restructuring` |

---

## Module Subscription Table

### `capital_controls` (ADR-020)

| Module | Event subscribed | Channel | Effect | Status |
|---|---|---|---|---|
| GovernanceModule | `emergency_policy_capital_controls` | Governance | `political_legitimacy_erosion ↑` | ✅ existing |
| ExternalSectorModule | `emergency_policy_capital_controls` | A — Reserve protection | `capital_account_outflow_velocity ↓ (ε=0.60)` → `reserve_coverage_months ↑` | 🆕 ADR-020 |
| MacroeconomicModule | `emergency_policy_capital_controls` | B — Credit contraction | `domestic_credit_growth ↓ (β≈0.025)` → `gdp_growth ↓`, `fdi_stock_pct_gdp ↓` | 🆕 ADR-020 |
| DemographicModule | `emergency_policy_capital_controls` | C — Distributional | `q1_poverty_headcount_ratio ↑ (φ∈[0.3,0.7])` via Channel B labour market shock | 🔧 ADR-020 (subscription fix) |

**Calibration anchors:** Iceland 2008 (ε≈0.65, β≈0.025), Malaysia 1998 (ε≈0.55). CM default: ε=0.60 ±0.15, β=0.025 ±0.010.

**Backtesting validation anchor:** Iceland G2D Type A run — `reserve_coverage_months` must increase at Step 2 (post-controls); `gdp_growth` direction DETERIORATING at Step 2–3.

---

### Other EmergencyInstrument variants

> **Status as of ADR-020:** Full DemographicModule subscription audit pending (ADR-020 Decision 3).
> CE Agent must audit all variants against the canonical event string registry before G2D
> implementation PR merges. Near-miss entries required for any additional dead subscriptions found.
> Table below to be completed by CE Agent at audit time.

| Instrument | GovernanceModule | ExternalSectorModule | MacroeconomicModule | DemographicModule | Audit status |
|---|---|---|---|---|---|
| `imf_program_acceptance` | ✅ | ⬜ TBD | ⬜ TBD | ⬜ TBD | **PENDING — CE audit** |
| `debt_moratorium` | ✅ | ⬜ TBD | ⬜ TBD | ⬜ TBD | **PENDING — CE audit** |
| `default_declaration` | ✅ | ⬜ TBD | ⬜ TBD | ⬜ TBD | **PENDING — CE audit** |
| `emergency_austerity` | ✅ | ⬜ TBD | ⬜ TBD | ⬜ TBD | **PENDING — CE audit** |
| `asset_nationalization` | ✅ | ⬜ TBD | ⬜ TBD | ⬜ TBD | **PENDING — CE audit** |
| `currency_peg_break` | ✅ | ⬜ TBD | ⬜ TBD | ⬜ TBD | **PENDING — CE audit** |
| `hyperinflation_emergency` | ✅ | ⬜ TBD | ⬜ TBD | ⬜ TBD | **PENDING — CE audit** |
| `banking_system_freeze` | ✅ | ⬜ TBD | ⬜ TBD | ⬜ TBD | **PENDING — CE audit** |
| `debt_restructuring` | ✅ | ⬜ TBD | ⬜ TBD | ⬜ TBD | **PENDING — CE audit** |

Legend: ✅ verified active | 🆕 new (ADR-020) | 🔧 fixed (ADR-020) | ⬜ TBD (CE audit pending) | intentional-only (governance-only; no economic channel by design — must be documented here explicitly)

---

## CE Implementation Verification Checklist

Before merging any EmergencyInstrument PR (new variant or channel modification):

- [ ] Emitted event string matches the canonical registry in this table exactly
- [ ] All module subscriptions are listed here; any unlisted subscription is a compliance finding
- [ ] Any blank (`⬜ TBD`) cells for the affected variant are resolved (not left pending)
- [ ] Variants with intentionally no economic channel have an explicit "intentional-only" entry
- [ ] Runtime validation in input processor (raises `SimulationError` for unregistered strings) is active
- [ ] If new dead subscriptions found during audit: near-miss entries filed before PR merges
