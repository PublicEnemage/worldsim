---
name: adr-020-panel-review
type: adr-panel-review
adr: ADR-020
issue: "#1532"
panel-composition: Architect Agent (author), Computation Engine Agent (C), Chief Methodologist (C — calibration), Development Economist (C), Geopolitical Analyst (C), UX Designer Agent (Tier 2 trace review — same session), Engineering Lead (A)
review-date: 2026-07-03
outcome: ACCEPTED
---

# ADR-020 Panel Review — Emergency Instrument Economic Transmission Pattern

**ADR:** ADR-020-emergency-instrument-transmission-pattern.md
**Issue:** #1532
**Tier:** 2
**Panel:** Architect Agent (author), CE Agent (C), Chief Methodologist (C — calibration), Development Economist (C), Geopolitical Analyst (C), UX Designer Agent (Tier 2 trace), EL (A)
**Date:** 2026-07-03

---

## Panel Review Record

### Computation Engine Agent — Implementation Feasibility Review

**Verdict:** PASS with two INCORPORATE items

**Architectural feasibility of three channels:**

All three channels are architecturally implementable within existing module boundaries without engine refactor.

*Channel A — ExternalSectorModule (reserve protection):*
The ExternalSectorModule already operates on a per-step capital account model. Adding an `emergency_policy_capital_controls` event subscription is a standard module extension: register the handler, apply the `controls_effectiveness` factor ε to `capital_account_outflow_velocity`, propagate downstream to `reserve_coverage_months`. The partial hysteresis at duration expiry (0.3 × original outflow rate) requires storing `pre_controls_outflow_velocity` at the moment of controls imposition — one additional field on simulation state. This is the correct approach; I'll implement it as a `CapitalControlsState` named tuple on the ExternalSectorModule instance.

*Channel B — MacroeconomicModule (credit contraction):*
The MacroeconomicModule credit computation runs at each step. Adding a `domestic_credit_growth_modifier` field that is applied when the capital controls state is active is a one-line addition to the step computation, plus the event handler that sets the modifier. The γ=1.2 GDP-credit multiplier is already parameterised in the module's config; the channel uses the existing multiplier rather than introducing a new one. The `fdi_stock_pct_gdp` step-down is straightforward.

*Channel C — DemographicModule (subscription fix + activation):*
The subscription fix is a one-line change: `capital_controls_imposition` → `emergency_policy_capital_controls`. The Channel B → Channel C bridge (labour market shock) is implemented as a published secondary event: MacroeconomicModule emits `credit_contraction_labour_shock` when the capital controls credit modifier exceeds a threshold, and DemographicModule subscribes to this secondary event. This maintains clean module boundaries — DemographicModule does not need to subscribe to the raw capital controls event and compute credit contraction independently.

*Decision 1 runtime validation:*
The `SimulationError` on unregistered event strings is architecturally correct and implementable. The event registry will be a module-level constant (`REGISTERED_EMERGENCY_POLICY_EVENTS: frozenset[str]`) checked in the input processor at event emission time.

**INCORPORATE-1 — γ source declaration:**
The ADR states γ=1.2 GDP-credit multiplier "calibrated to CM-supplied regression estimate." CE confirms γ is already parameterised in the module config — but the ADR should explicitly state that γ is a CM-supplied calibration value that CE treats as a given constant (not an implementer determination). Without this declaration, a future CE agent might assume ownership of γ and change it without CM review. Add to ADR §Decision 2 Channel B: "γ is a CM-supplied constant fixed at CM review time. Changes to γ require CM Consulted review, not CE author authority."

**INCORPORATE-2 — `SimulationError` log-before-raise:**
The ADR specifies that the input processor raises `SimulationError` for unregistered event strings. Implementation note: in long simulation runs, a bare raise without prior logging makes the error hard to locate in traces. The implementation must emit a `logger.error(f"Unregistered emergency policy event string: {event_string!r}. Registered strings: {REGISTERED_EMERGENCY_POLICY_EVENTS}")` before raising. Add to ADR Decision 1 implementation requirement: "Prior to raising `SimulationError`, the input processor must emit a logger.error message naming the unregistered string and the full registered set." This is an implementation contract, not a decision change.

**Decision 3 audit scope:**
The scope (pre-G2D implementation PR, all ten variants) is correct and achievable. I will conduct the audit during the G2D sprint entry phase, before opening the implementation PR. If additional dead subscriptions are found, near-miss entries are filed before the PR opens — not after. Confirmed.

**Session context:** Computation Engine Agent in session with ADR authorship — acknowledged.

`[x]` CE Agent: Channels A, B, C architecturally feasible. Event routing implementable. Two INCORPORATE items raised. Decision 3 audit scope confirmed. 2026-07-03

---

### Chief Methodologist — Calibration Review

**Verdict:** PASS with two INCORPORATE items and one PENDING calibration deliverable

**Iceland 2008 anchor — ε (reserve protection effectiveness):**

The cited source (Central Bank of Iceland Annual Report 2009) reports that foreign exchange reserves increased from approximately ISK 390bn to ISK 550bn in the four quarters following October 2008 controls imposition. Converting to months of import cover and accounting for the contemporaneous IMF programme drawdown (which also contributed to the reserve increase), the capital-controls-specific contribution to reserve recovery implies ε in the range 0.55–0.70. The ADR's default ε=0.60 ±0.15 is consistent with this range. However:

**INCORPORATE-3 — Iceland anchor precision note:**
The ε calculation is complicated by the simultaneous IMF Stand-By Arrangement (SBA, ~€1.5bn) that began October 2008 alongside the capital controls. Some of the reserve increase is attributable to the SBA drawdown, not the capital controls themselves. The ADR's ε=0.60 default blends both effects. For the Iceland G2D fixture, where the scenario does not include an IMF programme (it is specifically the heterodox non-IMF pathway), the capital-controls-only ε should be bounded lower: ε_controls_only ∈ [0.45, 0.60]. Add to ADR Decision 2 Channel A, and to the `known_limitations` for the Iceland fixture: "Iceland 2008 ε calibration includes partial SBA reserve contribution; capital-controls-only ε may be at the lower bound of the stated range. Iceland heterodox (non-IMF) fixture uses ε=0.50 as Type A calibration anchor."

**Malaysia 1998 anchor — ε validation:**
Malaysia September 1998: ringgit peg fixed at MYR 3.80/USD + capital controls. Bank Negara Malaysia foreign exchange reserves stabilised within one quarter (Q4 1998) after declining ~40% in the preceding 18 months. The implied ε for the reserve stabilisation (not growth) effect is approximately 0.50–0.60. The ADR's Malaysia anchor of ε≈0.55 is consistent. The ε=0.60 default remains appropriate as a two-anchor average.

**Iceland 2009 GDP decomposition — β (credit contraction):**
Iceland real GDP declined 6.6% in 2009 (Statistics Iceland). The IMF Article IV (2010) decomposes this into: banking sector collapse contribution ~3–4pp; capital controls credit contraction ~1.5–2pp; external demand shock ~1–1.5pp. The ADR's β≈0.025 per step (annual) → approximately 2.5% credit contraction contribution per year → at γ=1.2 multiplier → ~3pp GDP impact. This is slightly above the upper bound of the IMF credit contraction decomposition (~2pp). I will supply β=0.020 as the preferred calibration default, with a 0.015–0.030 range. The ADR states β ∈ [0.02, 0.06] — the lower end of this range is the empirically grounded value. The upper end (0.06) should be documented as a severe-case bound, not a central estimate.

**INCORPORATE-4 — β calibration default update:**
Revise ADR Decision 2 Channel B: "β default = 0.020 (annual per step), range [0.015, 0.030] for Iceland/Malaysia-class controls environments; [0.030, 0.060] reserved for full banking freeze co-occurrence (documented in G2D fixture calibration notes)." This prevents a future implementing agent from using β=0.06 as a central value for a non-crisis-severity scenario.

**γ (GDP-credit multiplier) — CM-supplied constant:**
γ=1.2 is consistent with the WorldSim MacroeconomicModule's existing calibration for credit-to-GDP transmission. This is a stored CM calibration constant. As noted by CE Agent, γ is CE's given constant — CM holds R for any future change. Confirmed.

**G2D Type A backtesting assertion:**
With ε=0.50 (Iceland heterodox, INCORPORATE-3 lower bound) and β=0.020 (INCORPORATE-4 revised default): reserve_coverage_months direction at Step 2 will be POSITIVE (outflow velocity reduced by ~50% → net reserve accumulation). This assertion is achievable. GDP growth direction at Step 2–3 will be DETERIORATING (β × γ = 0.020 × 1.2 = 2.4pp drag). The G2D Type A assertion is sound.

**PENDING calibration deliverable — pre-G2D implementation PR:**
CM will supply a calibration notes document (`docs/methodology/calibration-basis.md §Capital Controls` addendum) containing:
1. Iceland 2008 ε_controls_only validated value (separating SBA contribution)
2. β=0.020 regression basis (IMF Article IV 2010 decomposition reference)
3. φ range validation (pending Development Economist review — coordinated deliverable)
4. Malaysia 1998 cross-validation results

This document is a **hard gate** before the G2D implementation PR opens. CE may not set calibration constants without this document on record.

**Session context:** Chief Methodologist in session with ADR authorship — acknowledged.

`[x]` CM: Calibration anchors validated (ε=0.60 default sound; β revised to 0.020 default). Two INCORPORATE items raised. Pre-implementation calibration deliverable committed. G2D Type A assertion achievable. 2026-07-03

---

### Development Economist — Distributional Honesty Review

**Verdict:** PASS with one INCORPORATE item and one NOTED LIMITATION

**Channel C (φ range) — distributional honesty assessment:**

The φ∈[0.3, 0.7] range for bottom quintile concentration of credit contraction labour market impact is broadly consistent with the empirical literature on informal credit market exposure. The key empirical basis:

- In low-to-middle income economies, Q1 workers are predominantly employed in the informal sector, where working capital is financed through domestic credit markets (bank overdrafts, trade credit, rotating credit societies). Credit contraction disproportionately eliminates informal sector working capital.
- In higher-income emerging markets (Iceland 2008), the Q1 concentration is lower: Icelandic Q1 households had formal labour market ties and pension-backed credit. The credit contraction effect on Iceland's Q1 poverty headcount was real but moderated by unemployment insurance. φ≈0.30 is appropriate for Iceland-class economies; φ≈0.60–0.70 for lower-income country contexts.

The φ range is appropriately wide to span these contexts. The implementing agent must not use a single φ point estimate — the range must be scenario-parameterised or CM-calibrated per fixture.

**HCL honesty requirement:**
The ADR's P-5 (income cohort: bottom quintile, informal credit market exposure) and P-6 (negotiating leverage: Q1 PHC visible in trajectory as controls take effect) are correctly framed. Q1 poverty headcount is the correct HCL indicator for credit contraction distributional impact. The magnitude (φ × Δcredit_growth × q1_labour_market_sensitivity) is honest in that it does not overstate the Q1 impact relative to aggregate credit contraction — it applies a sub-unitary factor (φ < 1) to the aggregate signal. This is the correct direction for HCL honesty: never inflate the human cost signal beyond what the empirical basis supports.

**INCORPORATE-5 — Q1 framing vs. Q1+Q2 scope:**
The ADR frames Channel C as affecting `q1_poverty_headcount_ratio` only. However, credit contraction labour market impacts are experienced primarily in Q1 and Q2 in most country contexts — the bottom two quintiles. The ADR should note: "The Channel C φ factor applied to `q1_poverty_headcount_ratio` captures the Q1 component of a Q1+Q2 distributional effect. The Q2 component is not separately modeled in the current DemographicModule — this is a known limitation to disclose in `known_limitations` for any capital controls scenario. Future milestone: extend DemographicModule to model Q2 separately." Add this note to ADR §Known Limitations and to the Channel C description in Decision 2.

**NOTED LIMITATION — Iceland poverty headcount recovery arc:**
The ADR describes Channel C at Steps 4–5 as a "partial recovery as export recovery offsets credit contraction." For the Iceland case, this recovery arc is longer than implied: Iceland's Q1 poverty headcount remained elevated through 2011 due to household debt overhang (foreign-currency mortgages revalued upward after the krona depreciation). The export recovery (fishing and tourism) benefited export sector workers (Q2/Q3) more than the debt-distressed Q1 households. The Iceland G2D fixture's `known_limitations` should explicitly flag: "Iceland Q1 poverty headcount recovery modeled as export-driven; household debt overhang effect not captured — actual Q1 recovery was slower than modeled." This does not require an INCORPORATE to the ADR; it is a fixture-level calibration note for the G2D sprint entry.

**Session context:** Development Economist in session with ADR authorship — acknowledged.

`[x]` DE: φ range [0.3, 0.7] empirically defensible; scenario-parameterised, not point-estimated. HCL honesty requirement satisfied. One INCORPORATE item (Q1+Q2 scope note). Iceland recovery arc noted as G2D fixture calibration item. 2026-07-03

---

### Geopolitical Analyst — Instrument Framing Review

**Verdict:** PASS — unconditional

**Capital controls as heterodox/coercive instrument framing:**

The ADR's framing is accurate. Capital controls occupy a contested space in the economic policy literature precisely because of the asymmetry the ADR correctly identifies: the creditor-side analytical toolkit (IMF GIMF, DSGE models) is calibrated primarily against capital controls failures (Thailand 1997, pre-crisis Malaysia 1997), not against capital controls successes (post-crisis Malaysia 1998, Iceland 2008). This produces a systematic analytical bias at the negotiating table — a bias that WorldSim can partially correct.

**Malaysia 1998 case accuracy:**
Mahathir Mohamad's September 1998 capital controls decision was made against IMF advice (the Fund's standard prescription was orthodox austerity with open capital account). The outcome — reserve stabilisation within one quarter, GDP recovery of +6.1% in 1999 — is the canonical heterodox success case. The creditor counter-argument at the time was reputational contagion (future capital market access costs). The Geopolitical Analyst confirms: the ADR does not suppress the reputational cost — GovernanceModule political legitimacy erosion fires and is visible in the trajectory alongside the reserve recovery. This is the correct two-sided representation of the capital controls trade-off.

**Iceland 2008 case accuracy:**
Iceland is a more complex case because capital controls were implemented alongside an IMF SBA (not against IMF advice, as in Malaysia 1998). The heterodox element was the refusal of bilateral EU/UK creditor claims (the Icesave dispute). The GovernanceModule political legitimacy erosion for Iceland captures the international reputational cost of this refusal correctly. The ADR's bifurcation — Iceland as the successful capital controls case for the reserve protection channel, Malaysia as the faster-recovery cross-validation — is analytically sound.

**Asymmetry assessment accuracy:**
The ADR's asymmetry claim — that Channel C (Q1 poverty headcount response to capital controls credit contraction) is absent from creditor-side modelling — is correct. IMF aggregate-model outputs in Article IV consultations do not disaggregate credit contraction impacts to income quintiles. A ministry team that can produce a WorldSim Q1 poverty headcount trajectory under capital controls is surfacing information genuinely absent from the room. This is the asymmetry WorldSim is designed to close.

**GovernanceModule political legitimacy erosion direction:**
Under capital controls imposition with creditor pressure, political legitimacy faces two simultaneous forces: (1) external legitimacy erosion (creditor confidence, rating agency response) — captured by GovernanceModule; (2) potential internal legitimacy gain (domestic population relief from capital flight) — not currently modeled. For net assessment: in the Malaysia 1998 case, domestic legitimacy initially held (Mahathir's domestic political position was stable despite international pressure); in the Iceland 2008 case, domestic legitimacy deteriorated (the government fell in 2009 due to economic crisis). The current GovernanceModule models net legitimacy erosion without disaggregating domestic vs. external legitimacy — this is a known simplification, not an error. Appropriate for Tier 2; would require a separate ADR for full political economy decomposition.

**Session context:** Geopolitical Analyst in session with ADR authorship — acknowledged.

`[x]` GA: Capital controls framing accurate. Malaysia 1998 and Iceland 2008 case accuracy confirmed. Asymmetry assessment correct. GovernanceModule single-dimension erosion is a known simplification, not an error. Unconditional PASS. 2026-07-03

---

### UX Designer Agent — Tier 2 Trace Review

*(Included in the ADR body as the four-field structured sign-off required by CLAUDE.md §UX Designer sign-off — reproduced here for panel record.)*

**Reviewing agent:** UX Designer Agent
**Session context:** Same session as ADR authorship — acknowledged
**Governing documents reviewed:**
- `docs/ux/information-hierarchy.md §Zone 1A` (trajectory data rendering contract)
- `docs/ux/information-hierarchy.md §Zone 1B` (alert panel state management)
- `docs/ux/north-star.md §Primary Cognitive Tasks` (Mode 1 trajectory reconstruction)
- `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md §Instruments Always Visible`
**Concerns found:** 0 — None.

*Trace review summary:*
ADR-020 changes the computation behind three Zone 1A trajectory fields (`reserve_coverage_months`, `gdp_growth`, `q1_poverty_headcount_ratio`) for capital controls scenarios. Display contracts are unchanged — the fix changes values, not rendering. Zone 1A step axis contract (ADR-017) is unaffected. MDA alert state transitions (Zone 1B, ADR-014) are correctly handled — a clearing RESERVE_COVERAGE_BREACH alert when controls produce reserve recovery is existing alert panel behaviour. HCL panel parity (q1 poverty headcount visible weight) is maintained. The Zone 3 `known_limitations` string update (Decision 4) renders correctly via the existing auditability panel (M18, #1422).

`[x]` UX Designer: Tier 2 trace complete. P-1–P-6 confirmed. Display contracts unchanged. HCL parity maintained. Zone 3 `known_limitations` update compatible with existing auditability panel. 2026-07-03

---

### Architect Agent — INCORPORATE Resolution and Determination Record

**INCORPORATE items received:** 5 total (2 from CE, 2 from CM, 1 from DE)

**INCORPORATE-1 (CE — γ source declaration):**
Accepted. Adding to ADR §Decision 2 Channel B: γ is explicitly declared as CM-supplied constant; changes require CM Consulted review. Resolution: applied to ADR §Decision 2 as an implementation constraint note.

**INCORPORATE-2 (CE — SimulationError log-before-raise):**
Accepted. Adding to ADR §Decision 1 implementation requirement: prior to raising `SimulationError`, emit `logger.error` naming the unregistered string and the full registered set. Resolution: applied.

**INCORPORATE-3 (CM — Iceland ε SBA confound):**
Accepted. The ε=0.60 default is the blended value; the Iceland heterodox (non-IMF) fixture uses ε=0.50 as the controls-only anchor. The ADR's Channel A description and the G2D `known_limitations` are updated accordingly. Resolution: applied. Backlog entry: CM calibration notes document must separate SBA contribution before G2D implementation PR.

**INCORPORATE-4 (CM — β calibration default):**
Accepted. β default revised to 0.020 (annual per step); range [0.015, 0.030] for standard controls environments; [0.030, 0.060] reserved for banking-freeze co-occurrence. ADR Decision 2 Channel B updated. Resolution: applied.

**INCORPORATE-5 (DE — Q1+Q2 scope note):**
Accepted. Adding to ADR §Decision 2 Channel C and §Known Limitations: the φ factor captures the Q1 component of a Q1+Q2 distributional effect; Q2 is a known gap for future milestone treatment. Resolution: applied.

**All INCORPORATE items resolved. ADR is implementation-ready.**

**Panel determination:**
- Tier 2 classification: confirmed (computation fix behind existing display surfaces)
- Panel composition: complete per backlog panel rule for Simulation Engine ADR type (Architect, CE, CM, EL minimum) plus cross-cutting DIC members (Development Economist, Geopolitical Analyst) per RACI; UX Designer included per Tier 2 trace requirement. Composition is correct.
- UX Designer sign-off: four-field compliant, same-session disclosed (CLAUDE.md §UX Designer sign-off compliant)
- Silent Failure Mode section: SF-1 through SF-4 specified with detection mechanisms
- Asymmetry Assessment: complete and confirmed by GA
- North Star Test: specific (named scenario, concrete capability, table impact)
- Mission Impact Statement: complete

`[x]` Architect: All five INCORPORATE items applied. ADR is implementation-ready and panel complete. Recommend EL acceptance. 2026-07-03

---

### Engineering Lead — Acceptance

Panel composition is correct per backlog panel rule for Simulation Engine ADRs (Architect, CE, CM, EL) with appropriate DIC extension (Development Economist and Geopolitical Analyst per the cross-cutting nature of capital controls as both an economic and geopolitical instrument). UX Designer Tier 2 trace review is four-field compliant; same-session disclosure is on record.

Tier 2 classification is appropriate: this is a computation fix behind existing Zone 1A trajectory display surfaces. No new display contract is introduced. The `emergency-instrument-transmission-table.md` is a process artifact, not a display surface.

Five INCORPORATE items received and resolved by the Architect. All resolutions are scope-appropriate:
- INCORPORATE-1 and INCORPORATE-2 (CE): implementation contract clarifications — do not change any decision
- INCORPORATE-3 (CM): calibration precision improvement (ε_controls_only = 0.50 for heterodox fixture) — within the stated ε=0.60 ±0.15 band
- INCORPORATE-4 (CM): β default revised from 0.025 to 0.020 — within the stated β ∈ [0.02, 0.06] range; the ADR's stated range remains valid; only the default shifts to the lower, more empirically grounded value
- INCORPORATE-5 (DE): scope note clarifying Q1 vs. Q1+Q2 — no quantitative change

CM's pre-implementation calibration deliverable (`calibration-basis.md §Capital Controls` addendum) is a hard gate before the G2D implementation PR opens — this is correctly positioned by CM and does not block ADR acceptance; it blocks implementation.

ADR-020 is **ACCEPTED**.

EL acceptance date: 2026-07-03

G2D sprint entry for Iceland 2008–11 (#1553) may be filed immediately. The CE DemographicModule audit (Decision 3) and CM calibration deliverable are both blocking pre-conditions for the G2D **implementation PR**, not for sprint entry.

---

## INCORPORATE Resolution Table

| Item | Source | Description | Resolution |
|---|---|---|---|
| INCORPORATE-1 | CE Agent | γ declared as CM-supplied constant; changes require CM Consulted review | Applied to ADR §Decision 2 Channel B |
| INCORPORATE-2 | CE Agent | `SimulationError` must log before raise | Applied to ADR §Decision 1 implementation requirement |
| INCORPORATE-3 | CM | Iceland ε SBA confound — heterodox fixture uses ε=0.50 | Applied to ADR §Decision 2 Channel A + §Known Limitations |
| INCORPORATE-4 | CM | β default revised to 0.020; range [0.015, 0.030] standard | Applied to ADR §Decision 2 Channel B |
| INCORPORATE-5 | DE | Q1+Q2 scope note — φ captures Q1 component of Q1+Q2 effect | Applied to ADR §Decision 2 Channel C + §Known Limitations |

---

## Panel Summary

| Panel member | Verdict | Notes |
|---|---|---|
| Architect Agent | AUTHOR | 5 INCORPORATE items applied; ADR implementation-ready |
| CE Agent | PASS | 2 INCORPORATE items (γ declaration, log-before-raise); audit scope confirmed |
| Chief Methodologist | PASS | 2 INCORPORATE items (Iceland ε SBA confound, β default 0.020); calibration deliverable committed (pre-G2D implementation PR gate) |
| Development Economist | PASS | 1 INCORPORATE item (Q1+Q2 scope note); Iceland recovery arc noted as G2D fixture calibration item |
| Geopolitical Analyst | PASS (unconditional) | Framing accurate; Malaysia 1998 + Iceland 2008 confirmed; asymmetry assessment correct |
| UX Designer Agent | PASS (trace review) | Display contracts unchanged; HCL parity maintained; Zone 3 compatible |
| Engineering Lead | ACCEPTED | Panel composition correct; Tier 2 confirmed; all INCORPORATE items resolved; calibration deliverable correctly gated at implementation |

**ADR-020 status:** ACCEPTED 2026-07-03

---

## Post-Acceptance Gate Conditions (G2D)

The following conditions must be satisfied before the G2D **implementation PR** may open (per EL acceptance statement):

- [ ] CE Agent conducts DemographicModule audit (Decision 3 — all ten EmergencyInstrument variants; near-miss entries for any additional dead subscriptions)
- [ ] CM delivers `calibration-basis.md §Capital Controls` addendum (ε_controls_only, β=0.020 regression basis, φ validation, Malaysia cross-validation)
- [ ] `emergency-instrument-transmission-table.md` updated with audit findings before implementation PR opens
- [ ] G2D sprint entry document filed and EL-approved (separate gate from ADR acceptance)
