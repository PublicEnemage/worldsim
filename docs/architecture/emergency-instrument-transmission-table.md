# Emergency Instrument Transmission Table

> **Authority:** ADR-020, Decision 1 and Decision 2.
> **Owner:** Architect Agent (authorship), Computation Engine Agent (implementation verification).
> **Update rule:** This table must be updated in the same PR as any new EmergencyInstrument
> variant introduction. A variant with no non-governance channel must have an explicit
> "intentional — governance-only" entry rather than a blank. Missing entries are a compliance
> finding. CE Agent verifies this table against live module subscription registry before any
> EmergencyInstrument PR merges.
>
> Last updated: 2026-07-03 (ADR-020 capital controls channels authored; CE full audit
> completed 2026-07-03 — NM-090, NM-091 filed)

---

## CE Audit Summary (2026-07-03 — G2D Pre-Implementation Gate 2)

**Audit scope:** All `EmergencyInstrument` enum variants in
`backend/app/simulation/orchestration/inputs.py`; all module `_SUBSCRIBED_EVENTS`
registries in DemographicModule, GovernanceModule, MacroeconomicModule,
ExternalSectorModule.

**Audit findings:**

| Finding | Severity | NM entry | Status |
|---|---|---|---|
| DemographicModule subscribes to `"imf_program_acceptance"` — dead string (never emitted; correct: `"emergency_policy_imf_program_acceptance"`) | Medium | NM-090 | Filed |
| DemographicModule subscribes to `"emergency_declaration"` — dead string (never emitted; correct: `"emergency_policy_emergency_declaration"`) | Medium | NM-090 | Filed |
| Canonical registry in this table listed 10 variants; actual `EmergencyInstrument` enum has 7; mismatch of 3 registry-only entries and 3 code-only variants | Medium | NM-091 | Filed |
| Pre-populated GovernanceModule ✅ for `debt_moratorium`, `default_declaration` and 4 other variants was unverified — GovernanceModule only subscribes to 2 emergency event strings | Medium | NM-091 | Filed |
| β calibration value in original caption (0.025) inconsistent with ADR-020 INCORPORATE-4 accepted value (0.020) | Low | — | Corrected in this PR |

**CE gate verdict:** Audit complete. Known dead subscriptions documented. NM entries
filed. Implementation team must not use the aspirational registry variants until the
`EmergencyInstrument` enum is updated. Table below reflects code reality as audited.

---

## Canonical Event String Registry (as audited 2026-07-03)

Format: `emergency_policy_{instrument.value}` where `instrument.value` is the Python
`.value` of the `EmergencyInstrument` enum member.

**Source of truth:** `backend/app/simulation/orchestration/inputs.py` `EmergencyInstrument`
enum. Event string is always `f"emergency_policy_{self.instrument.value}"` per
`EmergencyPolicyInput.to_events()` (line ~699 in inputs.py).

### Variants confirmed in code (7 of 7 audited)

| Instrument | Enum value | Canonical event string | Code confirmed |
|---|---|---|---|
| `CAPITAL_CONTROLS` | `"capital_controls"` | `emergency_policy_capital_controls` | ✅ |
| `BANK_HOLIDAY` | `"bank_holiday"` | `emergency_policy_bank_holiday` | ✅ |
| `DEBT_MORATORIUM` | `"debt_moratorium"` | `emergency_policy_debt_moratorium` | ✅ |
| `NATIONALIZATION` | `"nationalization"` | `emergency_policy_nationalization` | ✅ |
| `IMF_PROGRAM_ACCEPTANCE` | `"imf_program_acceptance"` | `emergency_policy_imf_program_acceptance` | ✅ |
| `DEFAULT_DECLARATION` | `"default_declaration"` | `emergency_policy_default_declaration` | ✅ |
| `EMERGENCY_DECLARATION` | `"emergency_declaration"` | `emergency_policy_emergency_declaration` | ✅ |

### Registry variants NOT in code — aspirational / planned (NM-091)

The following event strings appeared in the original ADR-020 canonical registry but have
**no corresponding `EmergencyInstrument` enum value** in the current codebase. They must
not be used until the enum is extended. Using them in an `EmergencyPolicyInput` will raise
a `ValueError` at construction time.

| Aspirational variant | Would-be event string | Status |
|---|---|---|
| `emergency_austerity` | `emergency_policy_emergency_austerity` | NOT IN CODE — planned variant |
| `asset_nationalization` | `emergency_policy_asset_nationalization` | NOT IN CODE — code has `NATIONALIZATION` (value: `"nationalization"`) |
| `currency_peg_break` | `emergency_policy_currency_peg_break` | NOT IN CODE — planned variant |
| `hyperinflation_emergency` | `emergency_policy_hyperinflation_emergency` | NOT IN CODE — planned variant |
| `banking_system_freeze` | `emergency_policy_banking_system_freeze` | NOT IN CODE — planned variant |
| `debt_restructuring` | `emergency_policy_debt_restructuring` | NOT IN CODE — planned variant |

**G2D implementation note:** The G2D intent document (§3.2) references
`instrument="asset_nationalization"`. This must be changed to use
`EmergencyInstrument.NATIONALIZATION` (which emits `"emergency_policy_nationalization"`)
until a separate enum extension PR adds `ASSET_NATIONALIZATION`. The implementing agent
must not create new enum values in the G2D feature PR without a separate ADR or at
minimum EL approval for the enum addition.

---

## Module Subscription Table

### `capital_controls` (ADR-020)

| Module | Event subscribed | Channel | Effect | Status |
|---|---|---|---|---|
| GovernanceModule | `emergency_policy_capital_controls` | Governance | `political_legitimacy_erosion ↑` | ⚠️ NOT SUBSCRIBED — GovernanceModule._SUBSCRIBED_EVENTS does not include this string; original ✅ was incorrect (see NM-091) |
| ExternalSectorModule | `emergency_policy_capital_controls` | A — Reserve protection | `capital_account_outflow_velocity ↓ (ε=0.60; ISL heterodox ε=0.50)` → `reserve_coverage_months ↑` | 🆕 ADR-020 (to implement) |
| MacroeconomicModule | `emergency_policy_capital_controls` | B — Credit contraction | `domestic_credit_growth ↓ (β=0.020, γ=1.2)` → `gdp_growth ↓`, `fdi_stock_pct_gdp ↓`; emits `credit_contraction_labour_shock` bridge | 🆕 ADR-020 (to implement) |
| DemographicModule | `credit_contraction_labour_shock` | C — Distributional (via bridge) | `q1_poverty_headcount_ratio ↑ (φ∈[0.3,0.7])` | 🔧 ADR-020 (subscription fix required + bridge event subscription) |

**Calibration anchors:** Iceland 2008 (ε=0.50 controls-only; ε=0.65 blended with SBA),
Malaysia 1998 (ε≈0.55). CM default: ε=0.60 ±0.15, **β=0.020** ±0.005, γ=1.2 (constant).

**Backtesting validation anchor:** Iceland G2D Type A run — `reserve_coverage_months` must
increase at Step 2 (post-controls); `gdp_growth` DETERIORATING at Step 2–3; `q1_poverty_headcount_ratio` rises at Step 2.

**Hysteresis (post-expiry):** Channel A outflow velocity recovers at 0.3× the imposition
rate (i.e. partial hysteresis — capital account does not fully reopen immediately per ADR-020
Decision 2).

---

### GovernanceModule — actual subscription state (CE audit)

GovernanceModule's `_SUBSCRIBED_EVENTS` contains exactly 4 entries. Only 2 are
emergency policy event strings:

| Subscribed event | Matches variant | Elasticity row exists | Status |
|---|---|---|---|
| `"gdp_growth_change"` | N/A (MacroeconomicModule output) | ✅ `rule_of_law_percentile` | ✅ Active |
| `"fiscal_policy_spending_change"` | N/A (FiscalPolicyInput output) | ✅ `institutional_capacity_index` | ✅ Active |
| `"emergency_policy_imf_program_acceptance"` | `IMF_PROGRAM_ACCEPTANCE` | ✅ `democratic_quality_score` | ✅ Active |
| `"emergency_policy_emergency_declaration"` | `EMERGENCY_DECLARATION` | ✅ `democratic_quality_score` | ✅ Active |

**All other EmergencyInstrument variants produce zero governance output** — GovernanceModule
does not subscribe to `emergency_policy_capital_controls`, `emergency_policy_bank_holiday`,
`emergency_policy_debt_moratorium`, `emergency_policy_nationalization`, or
`emergency_policy_default_declaration`. This is the current state; expanding governance
sensitivity to other emergency instruments requires adding both `_SUBSCRIBED_EVENTS` entries
and `GOVERNANCE_ELASTICITY_REGISTRY` rows.

---

### DemographicModule — subscription audit findings (CE audit, NM-090)

DemographicModule's `_SUBSCRIBED_EVENTS` as found in code (pre-ADR-020 fix):

| Subscribed string | Emission source | Status |
|---|---|---|
| `"gdp_growth_change"` | MacroeconomicModule / GdpGrowthChangeInput | ✅ Active — elasticity rows exist |
| `"capital_controls_imposition"` | NEVER EMITTED | ❌ DEAD — should be fixed to `credit_contraction_labour_shock` (ADR-020 Channel C bridge) |
| `"imf_program_acceptance"` | NEVER EMITTED | ❌ DEAD — correct string is `"emergency_policy_imf_program_acceptance"`; no elasticity row exists currently (NM-090) |
| `"emergency_declaration"` | NEVER EMITTED | ❌ DEAD — correct string is `"emergency_policy_emergency_declaration"`; no elasticity row exists currently (NM-090) |

**ADR-020 Channel C fix scope:** The G2D implementation PR must:
1. Fix `"capital_controls_imposition"` → remove from `_SUBSCRIBED_EVENTS`
2. Add subscription to `"credit_contraction_labour_shock"` (emitted by MacroeconomicModule Channel B)
3. Add elasticity row for `"credit_contraction_labour_shock"` → `q1_poverty_headcount_ratio` (φ∈[0.3,0.7])
4. **Do not fix** `"imf_program_acceptance"` or `"emergency_declaration"` dead strings in the G2D PR — scope per NM-090 process improvement; separate PR required (no elasticity rows exist; no runtime effect from fix without adding rows first)

---

### All EmergencyInstrument variants — consolidated subscription matrix

> Legend: ✅ verified active | 🆕 new (ADR-020, to implement) | 🔧 fix required (ADR-020) | ❌ not subscribed (no elasticity; governance-silent) | ⚠️ pre-audit error corrected | `intentional-only` = governance-only by design (must be documented explicitly here); `dead` = subscribed but string never emitted

| Instrument | Canonical event string | GovernanceModule | ExternalSectorModule | MacroeconomicModule | DemographicModule | Audit status |
|---|---|---|---|---|---|---|
| `capital_controls` | `emergency_policy_capital_controls` | ❌ not subscribed (⚠️ original ✅ incorrect) | 🆕 ADR-020 | 🆕 ADR-020 | 🔧 fix + bridge | **AUDITED (ADR-020)** |
| `imf_program_acceptance` | `emergency_policy_imf_program_acceptance` | ✅ (elasticity: `democratic_quality_score`) | ❌ not subscribed | ❌ not subscribed | ✅ Active (φ: Q1 INFORMAL +0.04, Q2 INFORMAL +0.02; T3; #1657) | **FIXED (#1657)** |
| `emergency_declaration` | `emergency_policy_emergency_declaration` | ✅ (elasticity: `democratic_quality_score`) | ❌ not subscribed | ❌ not subscribed | ✅ Active (φ: Q1 INFORMAL +0.06, Q2 INFORMAL +0.04; T3; #1657) | **FIXED (#1657)** |
| `debt_moratorium` | `emergency_policy_debt_moratorium` | ❌ not subscribed (⚠️ original ✅ unverified) | ❌ not subscribed | ❌ not subscribed | ❌ not subscribed | **AUDITED — no module channels active** |
| `default_declaration` | `emergency_policy_default_declaration` | ❌ not subscribed (⚠️ original ✅ unverified) | ❌ not subscribed | ❌ not subscribed | ❌ not subscribed | **AUDITED — no module channels active** |
| `bank_holiday` | `emergency_policy_bank_holiday` | ❌ not subscribed | ❌ not subscribed | ❌ not subscribed | ❌ not subscribed | **AUDITED — no module channels active** |
| `nationalization` | `emergency_policy_nationalization` | ❌ not subscribed | ❌ not subscribed | ❌ not subscribed | ❌ not subscribed | **AUDITED — no module channels active** |

**Variants absent from code (aspirational/planned):** `emergency_austerity`,
`asset_nationalization` (⚠️ code uses `nationalization`), `currency_peg_break`,
`hyperinflation_emergency`, `banking_system_freeze`, `debt_restructuring` — not auditable
until enum is extended. See NM-091.

---

## CE Implementation Verification Checklist

Before merging the G2D implementation PR (ADR-020 channel implementation):

- [ ] `"capital_controls_imposition"` removed from DemographicModule `_SUBSCRIBED_EVENTS`
- [ ] `"credit_contraction_labour_shock"` added to DemographicModule `_SUBSCRIBED_EVENTS`
- [ ] Elasticity row for `"credit_contraction_labour_shock"` → `q1_poverty_headcount_ratio` added to `ELASTICITY_REGISTRY`
- [ ] ExternalSectorModule subscribes to `"emergency_policy_capital_controls"` and applies ε reduction
- [ ] MacroeconomicModule subscribes to `"emergency_policy_capital_controls"` and applies β credit contraction
- [ ] MacroeconomicModule emits `"credit_contraction_labour_shock"` secondary event
- [ ] Runtime validation raises `SimulationError` (with prior `logger.error`) for unregistered event strings
- [ ] G2D intent document §3.2 `instrument="asset_nationalization"` corrected to use `EmergencyInstrument.NATIONALIZATION` (value: `"nationalization"`)
- [ ] `emergency_policy_capital_controls` string in GovernanceModule either added (with elasticity row) or explicitly documented as intentionally absent in this table
- [ ] This table updated to mark ADR-020 channels as ✅ implemented (change 🆕 → ✅)
- [ ] If `dead` DM subscriptions (`"imf_program_acceptance"`, `"emergency_declaration"`) are fixed, a separate PR is required — not G2D scope

**NM-090 process improvement (applied to G2D):**
> The CE audit checklist must verify ALL module subscription strings, not only the
> variant being implemented. Future DM subscription changes must cross-check against
> the canonical event string registry in this table.

**NM-091 process improvement (applied to G2D):**
> Before any ADR documents a canonical event string registry, the Architect Agent must
> verify each listed event string against the actual Enum `.value` in the code. The
> CE Agent must flag registry-enum mismatches at audit time.
