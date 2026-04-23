# ARCH-REVIEW-002: Full Council Architecture Review — Milestone 2

**Review type:** Full — all Domain Intelligence Council members, CHALLENGE mode
**Scope:** ADR-001, ADR-002, ADR-003, ADR-004, CLAUDE.md,
`docs/scenarios/module-capability-registry.md`, all files in `docs/adr/`
**Facilitated by:** Architecture Review Facilitator
**Date:** 2026-04-21
**Status:** Complete — GitHub Issues created for all Immediate and Near-Term findings

---

## Executive Summary

Milestone 2 delivered substantial architectural progress: a live PostGIS
database with 177 country entities, a FastAPI layer with six endpoints, a
MapLibre choropleth frontend, and ADR-004 establishing the Scenario Engine
architecture for Milestone 3. The float prohibition, Quantity type system
(SCR-001), and TerritorialValidator represent genuine improvements in data
integrity. All three active ADRs are CURRENT. The compliance posture is clean.

The council review surfaces a consistent finding across nine frameworks: **the
scenario engine architecture in ADR-004 operationalises the simulation primarily
as a financial instrument.** The Greece 2010–2012 backtesting case — the first
empirical validation of the simulation — tests two financial indicators (GDP
growth and debt/GDP ratio) with DIRECTION_ONLY thresholds. No human development,
ecological, governance, or social dynamics indicators appear in the backtesting
fidelity thresholds. The first time the simulation is held accountable to
historical reality, only the financial framework is tested. This creates a
precedent risk: a simulation that passes its first backtesting validation may
appear validated when in fact it has been validated only in the narrowest
possible dimension.

The ADR-004 comparative scenario output architecture compounds this: the
comparison endpoint returns a delta for a single attribute at a single step.
Two scenarios can be compared on GDP growth or on debt/GDP ratio, but not
on both simultaneously, and never on the full multi-framework profile that
CLAUDE.md calls a primary output with equal visual weight to financial
indicators. The architecture makes multi-framework comparative analysis
structurally harder than single-metric financial comparison.

Several ADR-004 decisions introduce new architectural gaps not present in
Milestone 1. The DIRECTION_ONLY backtesting threshold design produces sign
checks with no statistical power. The synchronous execution model creates a
brittle timeout boundary. The snapshot architecture produces terminal-state
comparisons but makes cumulative welfare analysis structurally difficult. The
`StateCondition` mechanism for contingent triggers cannot model compound
political conditions or information cascade dynamics.

**Key tensions identified by the council:**

- The Chief Methodologist, Development Economist, and Ecological Economist
  agree that the Greece backtesting case validates the wrong things: financial
  direction, not magnitude, and no other framework. The Investment Agent (RISK-
  TOLERANT mode) argues that a working financial validation pass is better than
  no validation, and that perfectionism in backtesting design delays the
  learning that only running backtests produces.
- The Social Dynamics Agent and Political Economist agree that social legitimacy
  and political feasibility need to be modeled as state variables that modify
  ControlInput efficacy; the Geopolitical Analyst adds that the coercive dynamics
  behind ControlInputs (external pressure, conditionality) are also absent. All
  three find the same architectural gap from different angles.
- The Intergenerational Advocate and Community Resilience Agent agree that the
  nation-state Level 1 resolution of the scenario engine, combined with annual
  timesteps, structurally cannot represent the long-horizon intergenerational and
  subnational community effects that are central to the tool's mission. The Chief
  Methodologist notes that adding these dimensions without corresponding data
  sources and calibration would produce outputs that appear more precise than
  they are.

The council identified **24 distinct blindspots**: 7 immediate, 12 near-term,
and 5 long-term. GitHub Issues have been created for all immediate and near-term
findings.

---

## Findings by Agent

---

### Development Economist Agent — CHALLENGE

**Finding 1: Greece backtesting initial state contains no human development
indicators.**

ADR-004 Decision 3 specifies that the Greece 2010–2012 initial state will be
loaded from `tests/fixtures/backtesting/greece_2010_initial_state.json`, seeded
from IMF World Economic Outlook April 2010. IMF WEO April 2010 contains GDP
growth, debt/GDP, and fiscal balance data. It does not contain unemployment rate,
poverty headcount, infant mortality, health system capacity, or educational
attainment. The simulation will start the Greece backtesting run with a picture
of Greece that is financially detailed and humanly invisible.

This is not a Milestone 3 implementation failure — it is an architectural
decision that needs to be explicit. If the Greece fixture will contain only
financial attributes, the backtesting documentation must state that the case
validates financial propagation only. The CLAUDE.md principle "the human cost
ledger is never a footnote" is violated by default in the first backtesting case
unless human development attributes are added to the initial state fixture from
World Bank WDI 2010 or WHO Global Health Observatory 2010 sources.

**Finding 2: Backtesting fidelity thresholds test financial indicators only.**

ADR-004 Decision 3 defines four fidelity thresholds: `gdp_growth DOWN` and
`debt_gdp_ratio UP` at steps 1 and 2. The historically documented consequences
of the 2010–2012 Greek austerity program include: unemployment rising from 12%
to 27%, healthcare spending cuts of 25%, infant mortality rising for the first
time in decades, and suicide rates increasing 35%. None of these appear in the
backtesting thresholds. A simulation that correctly models GDP contraction and
debt ratio increase while producing no human development output whatsoever
passes the backtesting gate. The first external validation of this tool will
certify it on purely financial grounds. This creates a precedent that shapes
all subsequent backtesting case design.

**Finding 3: Comparative output architecture enforces single-metric comparison.**

`GET /api/v1/scenarios/compare` returns delta for one `attribute` at a time.
Comparing two scenarios requires N API calls for N attributes, with no
structured relationship between them. A scenario that improves GDP growth while
worsening unemployment cannot be compared against one that trades those outcomes
in a single call. The architecture makes multi-framework simultaneous comparison
structurally harder than single-metric financial comparison, directly inverting
the stated design principle of equal visual weight across frameworks.

---

### Political Economist Agent — CHALLENGE

**Finding 4: Political feasibility absent from ControlInput validation.**

ADR-004 Decision 1 defines semantic validation at `POST /run` time: entity IDs
exist, inputs deserialise to valid ControlInput instances, no conflicting
instrument types at the same step. None of the validation criteria concern
political feasibility. A `FiscalPolicyInput` specifying 15% of GDP spending cuts
in one year fires without any check against the political implementation capacity
of the government. The Greece 2010 scenario fires three ControlInputs in step 1
(IMF program acceptance, spending change, VAT increase) with zero structural
acknowledgment that each of those required a parliament vote under conditions of
mass protest.

This is the same Finding 3 from ARCH-REVIEW-001, now made more concrete by the
Greece backtesting case. In ARCH-REVIEW-001 it was a general concern; in
ARCH-REVIEW-002 it is a specific architectural deficiency in the first
backtesting case that will produce optimistic simulation outputs compared to
historical reality.

**Finding 5: No political context field in scenario configuration.**

The `scenarios` table (ADR-004 Decision 1) has `modules_config` (which modules
to activate) and `initial_overrides` (attribute value overrides). It has no
`political_context` or `legitimacy_initial_state` field. A Greece scenario and
a Germany scenario starting from the same fiscal attributes are politically
non-equivalent in ways the architecture cannot represent. Electoral calendar,
government approval rating, coalition stability, and civil society organisation
strength are all preconditions that affect what ControlInputs can be implemented
and at what speed. The absence of political context from scenario configuration
means every scenario implicitly assumes a neutral political environment.

**Finding 6: `StateCondition` cannot model compound political triggers.**

From ARCH-REVIEW-001 Finding 4 — this finding is unresolved and made more
consequential by ADR-004. The Greece scenario has well-documented compound
triggers: the June 2011 Greek parliament confidence vote passed by a margin of
5 votes under threat of immediate default — a compound condition of fiscal
stress, political fragility, and external creditor ultimatum. The architecture
still only supports single-attribute threshold conditions. This limitation now
applies to the backtesting case that will be used to validate the model.

---

### Ecological Economist Agent — CHALLENGE

**Finding 7: The first backtesting case systematically excludes the ecological
framework.**

The Greece 2010–2012 case was selected based on its well-documented financial
data and unambiguous ControlInput sequence. Both selection criteria are sound.
But the practical effect is that the ecological framework has no data to test
against in the first backtesting case. There are no ecological attributes in
the Greece initial state fixture, no ecological fidelity thresholds, and no
ecological dimension in the `backtesting_runs` output record. The first time
the simulation is validated empirically, the ecological framework is confirmed
as not-yet-modeled by the implicit act of exclusion.

This becomes architecturally significant because the `backtesting_thresholds`
table has a `threshold_type` column (DIRECTION_ONLY | MAGNITUDE) and a
`calibration_tier` column — both calibrated around financial and macroeconomic
variables. The schema itself does not prohibit ecological thresholds, but the
Greece case will be the template that subsequent backtesting cases are written
against. Templates without ecological dimensions produce descendants without
ecological dimensions.

**Finding 8: No ecological attributes exist in the database — ecological
scenarios have no initial conditions.**

ADR-003 loaded 10 Level 1 attributes from Natural Earth 110m data: population,
GDP, ordinal indices. None are ecological. The `simulation_entities.attributes`
JSONB column can hold any Quantity, but no ecological Quantities have been
loaded. A scenario that attempts to model deforestation-driven fiscal stress, or
agricultural productivity loss under drought, has no ecological initial conditions
to run from. Ecological scenarios are not merely unimplemented — they are
unseeded.

---

### Geopolitical and Security Analyst Agent — CHALLENGE

**Finding 9: ControlInput sequence models sovereign decisions, not coercive
dynamics.**

The Greece backtesting ControlInput sequence is: `EmergencyPolicyInput(IMF_
PROGRAM_ACCEPTANCE)`, `FiscalPolicyInput(SPENDING_CHANGE)`, `FiscalPolicyInput
(TAX_RATE_CHANGE)`. Each is modeled as a unilateral sovereign decision by Greece.
The historical record is more complex: IMF program acceptance was the result of
Germany, France, and the ECB threatening to withdraw eurozone support if Greece
did not comply; the austerity packages were written in large part by the troika
(IMF, ECB, European Commission) rather than the Greek government. The coercive
structure — external actors constraining the sovereign's decision space — is
architecturally invisible. The scenario looks like Greece chose these policies;
Greece was constrained to them.

The `ControlInput.actor_id` and `actor_role` fields can record "IMF" as the
actor, but this does not model the mechanism of coercion. The `InputSource`
enum has no `EXTERNAL_PRESSURE` or `CONDITIONALITY` value. The architecture
models inputs as discrete sovereign decisions; it cannot model the negotiation
dynamics and creditor leverage that produced those decisions.

**Finding 10: Threshold crossings invisible in delta comparative output.**

`GET /compare` returns `delta = value_b - value_a` as a continuous value. For
geopolitical and security analysis, the relevant question is not "how much did
reserves change" but "did reserves cross the 3-month import coverage threshold
that triggers capital flight and IMF Article IV intervention." The same delta
can be strategically irrelevant (reserves at 8 months → 7 months) or
strategically catastrophic (reserves at 4 months → 3 months). A delta of -1
month of import coverage has qualitatively different security implications
depending on where it lands relative to known threshold values. The comparative
output architecture has no threshold-crossing marker.

---

### Intergenerational Equity Advocate Agent — CHALLENGE

**Finding 11: Annual timesteps cannot model intergenerational consequences.**

ADR-004 Decision 2 uses annual timesteps. The Greece 2010–2012 case runs 2
steps. The intergenerational consequences of the 2010–2012 austerity program —
the cohort of children who had their education truncated, the young adults who
emigrated, the pension system restructuring that redistributed wealth from
retirees to creditors — compound over 20–30 years and are structurally
unrepresentable in a 2-step scenario. The scenario engine is designed for
policy analysis; it cannot model the full time horizon over which policy
consequences manifest.

This is not a request to extend the scenario to 30 steps. It is an architectural
concern: the scenario output will be presented to users as analysis of the Greece
crisis, but it models only the 2-year adjustment period. The consequences that
the Intergenerational Advocate considers most important occur entirely outside
the modeled window. If the scenario outputs are not accompanied by an explicit
temporal scope limitation, users will draw conclusions about the Greece crisis
that the architecture structurally cannot support.

**Finding 12: Snapshot architecture produces terminal-state analysis; cumulative
welfare analysis is not supported.**

`scenario_state_snapshots` stores entity attribute values at each step. The
comparison endpoint returns `delta = value_b[step N] - value_a[step N]` — the
gap at year N. For intergenerational analysis, the relevant question is the
cumulative welfare across the scenario timeline: the integral of GDP growth over
steps 1..N, or the sum of capability losses over all years. Neither is
computable from the current snapshot architecture without client-side
aggregation across multiple API calls. The architecture makes terminal-state
comparison easy and trajectory comparison hard. This is the opposite of what
long-horizon welfare analysis requires.

---

### Community and Cultural Resilience Agent — CHALLENGE

**Finding 13: Subnational community impacts structurally invisible at Level 1
resolution.**

The M3 scenario engine operates at nation-state Level 1 resolution. The Greece
backtesting case models one entity: GRC. The community-level effects of the
2010–2012 austerity program — closure of rural health clinics, consolidation of
village schools, destruction of the agricultural cooperative network, mass
emigration from islands and mountain communities — are not representable at the
country level. A single `gdp_growth` delta for GRC says nothing about the
differential impact on communities in Thessaly vs. communities in Athens.

ADR-004 Decision 1's `entities_scope` field supports `{"entity_ids": [...]}` for
selecting specific entities but does not support subnational entity activation.
The M3 scenario engine cannot be extended to subnational resolution without
schema and API changes that are not planned until a later milestone.

**Finding 14: Social fabric modeled as entity attribute rather than relationship
property.**

CLAUDE.md discusses social trust, community cohesion, and collective resilience.
The `Relationship` model in ADR-001 carries `relationship_type` and `weight` but
all defined relationship types are economic (trade, debt, alliance, currency).
Social trust between communities, inter-community solidarity, and shared
institutional knowledge are relational phenomena — they exist between entities,
not within entities. Attempting to model social fabric as an entity attribute
(e.g., `GRC.social_cohesion = 0.6`) loses the structure: it models a country's
average cohesion rather than the network of specific solidarity and trust
relationships that either hold or fracture under stress. The relationship model
has the right structural form for social fabric representation; it is just not
used for this purpose.

---

### Investment and Capital Formation Agent — CHALLENGE

**Finding 15 (RISK-AVERSE): No investment climate indicators in initial state.**

The Greece 2010 initial state will contain IMF WEO financial data. It will not
contain CDS spreads (Greek sovereign credit default swap rates were the primary
market signal of crisis intensity from 2010), Moody's/S&P credit ratings, or
FDI stock data. Investment climate analysis of sovereign debt crises requires
these as initial conditions. The simulation will model fiscal adjustments without
the market-implied severity signal that made the 2010 program necessary in the
first place: 10-year Greek bond yields rising from 6% to 12% in the months before
program acceptance. A simulation of a market crisis that does not include market
signals in its initial conditions is missing its primary mechanism.

**Finding 16 (RISK-TOLERANT): Comparative output produces point deltas, not
distributional comparisons.**

`GET /compare` returns a single delta per entity per attribute. A high-return
scenario that has high variance is indistinguishable from a lower-return scenario
with lower variance if both produce the same expected delta. Investment analysis
is fundamentally about risk-adjusted returns, not expected returns alone. The
comparative architecture has no mechanism for variance, percentile range, or
confidence intervals on deltas. Two scenarios that produce identical mean GDP
growth deltas but very different worst-case outcomes are evaluated identically.

**Finding 17 (CATALYTIC): No blended finance or public de-risking mechanics.**

`StructuralPolicyInput` has `PRIVATIZATION` and `REGULATORY_CHANGE` instruments.
The simulation has no mechanism for encoding public de-risking instruments that
attract private capital: first-loss guarantees, currency hedging facilities,
partial risk guarantees from multilateral development banks. A scenario that
models public sector regulatory reform unlocking private investment cannot
distinguish between reform that attracts DFI capital at concessional terms and
reform that attracts extractive speculative capital. Blended finance mechanics —
the primary tool for sustainable private investment in vulnerable economies —
are unrepresentable.

---

### Social Dynamics and Behavioral Economics Agent — CHALLENGE

**Finding 18: StateCondition cannot model information cascades or panic dynamics.**

`ContingentInput.condition` evaluates a numerical attribute against a threshold:
`entity.get_attribute_value(key) > threshold`. Bank runs, currency attacks, and
sovereign debt crises are information cascade phenomena — they are triggered by
*expectations* about future state and by the behavior of other actors responding
to those expectations, not by current state crossing a threshold. The Greek bank
runs of 2011 and 2015 were driven by depositor expectations of euro exit, not by
a specific current-state numerical trigger. The architecture can model "reserves
fell below X" but cannot model "depositors believe reserves will fall below X."
This is a structural gap in the contingent trigger mechanism.

**Finding 19: Social response to ControlInputs has no feedback pathway.**

The Greece backtesting scenario fires `FiscalPolicyInput(SPENDING_CHANGE)` at
step 1 and again at step 2. These fire cleanly as exogenous control inputs.
The historical record shows that the social response to those inputs — the
general strikes of May 2010, October 2011, and February 2012; the political
party fragmentation that produced SYRIZA's electoral breakthrough — materially
affected implementation capacity and the subsequent fiscal path. Social backlash
to policy inputs is not a model artifact; it is a primary transmission mechanism
in political economy. The architecture has no pathway for the social consequences
of ControlInputs to generate endogenous Events that affect subsequent inputs.

**Finding 20: Comparative output captures terminal state, not sentiment
trajectory.**

`GET /compare` at step N shows attribute delta at year N. Social dynamics
analysis requires the trajectory: a scenario where legitimacy collapses in year
2 and partially recovers by year 5 is fundamentally different from one where
legitimacy is stable throughout, even if both produce the same terminal state at
year 5. The current architecture makes trajectory analysis structurally difficult
— it requires multiple compare calls at each step and client-side aggregation.
This is the same concern as Finding 12 (Intergenerational Advocate) approached
from the social dynamics angle.

---

### Chief Methodologist Agent — CHALLENGE

**Finding 21: DIRECTION_ONLY thresholds have no statistical power.**

ADR-004 Decision 3 defines DIRECTION_ONLY thresholds as passing when
`simulated_value[step] < simulated_value[step - 1]` (for DOWN direction). This
is a sign check — it verifies that the model produces a negative delta. A model
that produces GDP growth of -0.0001% in step 1 (the minimum distinguishable from
zero) passes identically to one that produces -8.9% (the historical value). A
model whose GDP growth delta was -0.1% in a scenario where historical was -8.9%
is directionally correct and magnitude-wrong by a factor of 89. It passes the
backtesting gate.

DIRECTION_ONLY thresholds are explicitly a concession to the absence of
calibrated parameters (Issue #44). This is an intellectually honest concession.
But the architectural record should make clear what "passing backtesting" means
in M3: it means the model gets the sign right on two indicators for a 2-step
scenario. It means nothing about quantitative accuracy.

**Finding 22: No Monte Carlo infrastructure — outputs are deterministic point
estimates.**

ADR-004 describes no mechanism for running a scenario under parameter
uncertainty. The `scenarios` table has no `n_monte_carlo_runs` field. The
`scenario_state_snapshots` table has one row per step — not one row per
(step, run) tuple. The `backtesting_runs` table records point comparisons.
CLAUDE.md states "outputs are distributions, not point estimates" as a guiding
principle. ADR-004's architecture produces point estimates exclusively. The
simulation runs once and produces one trajectory; the uncertainty in that
trajectory is not quantified. Issue #49 (Monte Carlo standards, deferred to M4)
documents this gap but does not prevent it from affecting M3 backtesting outputs.

**Finding 23: Data quality confidence tier and model uncertainty are conflated.**

The `Quantity.confidence_tier` (1–5) measures the quality of input data sources.
A Tier 1 input is from a primary source with documented methodology. But a model
equation applied to a Tier 1 input can produce output with high model uncertainty
if the equation is poorly calibrated or unvalidated. The Greek GDP growth
simulation will carry `confidence_tier = 1` (if seeded from IMF WEO primary
data) even though the propagation model has no calibrated fiscal multiplier and
the direction-only threshold is the only validation criterion. The confidence
tier of the output will reflect input data quality, not model validity. Users who
understand confidence tiers as measuring output reliability will be systematically
misled.

**Finding 24: Two-step backtesting has no statistical validity.**

The Greece 2010–2012 case produces 2 data points (step 1 and step 2). With
n=2 comparisons, the probability of passing DIRECTION_ONLY thresholds by chance
alone — if the model were completely uncalibrated — is 25% (two independent
sign-checks, each with 50% chance of passing). A 25% false-positive rate means
one in four random models would pass the M3 backtesting gate. The architecture
presents this as the first empirical validation of the simulation. It should be
presented as the first plausibility check — a necessary but not sufficient
condition for model confidence.

---

## Blindspot Inventory

### Immediate Blindspots (7)
*Affect Milestone 3 scope directly — Greece backtesting case design or core
architectural decisions with M3 consequences.*

| ID | Finding | Agent(s) | Risk if unaddressed |
|---|---|---|---|
| BI2-I-01 | Greece backtesting initial state contains no human development or ecological attributes | Development Economist, Ecological Economist | First backtesting case validates financial propagation only; validates nothing about the tool's primary mission |
| BI2-I-02 | Backtesting fidelity thresholds test financial indicators only — no human cost validation | Development Economist | CI passes simulation that produces no human development output; mis-sets precedent for all subsequent backtesting cases |
| BI2-I-03 | DIRECTION_ONLY thresholds have no statistical power — sign check with zero magnitude testing | Chief Methodologist | A model with multipliers 89× too small passes; M3 "backtesting pass" will be misinterpreted as model validation |
| BI2-I-04 | No Monte Carlo infrastructure — outputs are deterministic point estimates contrary to CLAUDE.md principle | Chief Methodologist | All scenario outputs violate the "distributions, not point estimates" principle; no mechanism to quantify uncertainty |
| BI2-I-05 | Comparative output is single-attribute, single-step — no multi-framework simultaneous comparison | Development Economist, Ecological Economist | Multi-framework comparative analysis requires N serial API calls; architecture inverts stated design principle |
| BI2-I-06 | Data quality confidence tier conflated with model validity — Tier 1 input data on uncalibrated model misleads users | Chief Methodologist | Users interpret `confidence_tier=1` output as reliable; it reflects data provenance, not model accuracy |
| BI2-I-07 | No investment climate indicators (CDS spreads, credit ratings) in initial state — market signal mechanism absent | Investment Agent | Simulation of market crisis without market signals misses primary transmission mechanism |

### Near-Term Blindspots (12)
*Affect subsequent M3 scenarios, M4 design, or compound if not addressed.*

| ID | Finding | Agent(s) | Risk if unaddressed |
|---|---|---|---|
| BI2-N-01 | Political feasibility absent from ControlInput validation — inputs fire regardless of political capacity | Political Economist | Systematically optimistic outcomes for politically contested reforms; Greek austerity modeled as frictionless |
| BI2-N-02 | No political context field in scenario configuration — every scenario implicitly assumes neutral political environment | Political Economist | Scenarios starting from different political conditions produce identical simulation behavior |
| BI2-N-03 | `StateCondition` cannot model compound political triggers or information cascade dynamics | Political Economist, Social Dynamics | Capital controls, bank runs, and political crises require compound conditions; single-attribute thresholds cannot represent them |
| BI2-N-04 | Ecological framework excluded from backtesting by case selection — no ecological thresholds, no ecological initial state | Ecological Economist | Ecological framework remains unvalidated indefinitely; backtesting case template propagates financial-only validation |
| BI2-N-05 | ControlInput coercive dynamics absent — IMF program modeled as sovereign choice, not conditionality | Geopolitical Analyst | Greece scenario misrepresents the mechanism; all conditionality-driven scenarios will have this structural bias |
| BI2-N-06 | Threshold crossings invisible in continuous delta output — security-relevant discontinuities lost | Geopolitical Analyst | 3-month reserve threshold crossing (IMF Article IV trigger) indistinguishable from any other -1 unit reserve change |
| BI2-N-07 | Annual timesteps cannot model intergenerational consequences — 20-30 year effects invisible in 2-step scenario | Intergenerational Advocate | Scenario outputs presented as Greece crisis analysis; structural scope limitation on time horizon not disclosed |
| BI2-N-08 | Snapshot architecture supports terminal-state comparison; cumulative welfare analysis requires N serial calls | Intergenerational Advocate, Social Dynamics | Trajectory analysis structurally harder than terminal comparison; core welfare metric (integral of wellbeing) not computable |
| BI2-N-09 | Subnational community impacts invisible at Level 1 nation-state resolution | Community Resilience | Differential community impact (rural vs. urban, island vs. mainland) structurally unrepresentable in M3 scenarios |
| BI2-N-10 | Social response feedback to ControlInputs has no pathway — austerity fires cleanly without social blowback | Social Dynamics, Political Economist | Greek austerity backlash (strikes, electoral shifts) affected implementation capacity; simulation produces frictionless adjustment |
| BI2-N-11 | Comparative output produces point deltas not distributional comparison — variance invisible | Investment Agent, Chief Methodologist | Risk-adjusted scenario comparison impossible; two scenarios with same mean but different variance evaluated identically |
| BI2-N-12 | Two-step backtesting has 25% false-positive rate under null model — insufficient statistical validity | Chief Methodologist | Architecture presents 2-comparison sign-check as "empirical validation"; multi-country or multi-year extension needed for statistical credibility |

### Long-Term Blindspots (5)
*Architectural vision issues for Milestone 4 and beyond.*

| ID | Finding | Agent(s) | Risk if unaddressed |
|---|---|---|---|
| BI2-L-01 | Social fabric as entity attribute rather than relationship property — trust network structure lost | Community Resilience | Community solidarity and institutional trust networks unrepresentable; aggregated country-level proxy loses the structure |
| BI2-L-02 | Blended finance and public de-risking mechanics unrepresentable — StructuralPolicyInput has no instrument for risk transfer | Investment Agent | Catalytic finance scenarios (DFI de-risking, first-loss guarantees) cannot be specified; investment-climate scenarios limited |
| BI2-L-03 | Scenario base entity state not versioned — if NE loader is re-run with updated data, old scenarios run from a different baseline | Chief Methodologist | Scenario reproducibility claim weakened; a scenario re-run after NE data update starts from different conditions |
| BI2-L-04 | No mechanism for scenarios with binding financing endpoints — scenarios run forward without modeling the capital market constraint | Investment Agent | Bond issuance, IMF program acceptance triggered by reserves depletion requires endpoint-constrained scenario design |
| BI2-L-05 | Governance legitimacy not encoded in scenario configuration — political context that conditions all ControlInputs has no formal representation | Political Economist | Every subsequent domain module will inherit this gap; political economy effects will require a future breaking change to encode |

---

## Recommended GitHub Issues

### Immediate Blindspots — Issues to Create

| Issue title | Finding ID | Labels |
|---|---|---|
| `arch(backtesting): add human development indicators to Greece 2010 initial state fixture — WDI unemployment, health spending, poverty` | BI2-I-01 | enhancement, horizon:immediate |
| `arch(backtesting): add human cost fidelity thresholds to Greece 2010-2012 case — unemployment direction, health spending direction` | BI2-I-02 | enhancement, horizon:immediate |
| `standards(backtesting): document statistical limitations of DIRECTION_ONLY thresholds in CODING_STANDARDS.md — sign check is not validation` | BI2-I-03 | documentation, horizon:immediate |
| `feat(scenario): add Monte Carlo run support to scenario engine — n_runs field, per-run snapshots, distributional output` | BI2-I-04 | enhancement, horizon:immediate |
| `arch(api): add multi-attribute comparison endpoint — GET /compare returning all available attributes simultaneously` | BI2-I-05 | enhancement, horizon:immediate |
| `standards(confidence): distinguish data quality tier from model validity tier — add model_confidence field to backtesting output` | BI2-I-06 | enhancement, horizon:immediate |
| `arch(backtesting): add investment climate initial conditions to Greece fixture — bond yields, CDS proxy, credit tier` | BI2-I-07 | enhancement, horizon:immediate |

### Near-Term Blindspots — Issues to Create

| Issue title | Finding ID | Labels |
|---|---|---|
| `feat(orchestration): add political feasibility modifier to ControlInput — implementation_capacity field affects event magnitude` | BI2-N-01 | enhancement, horizon:near-term |
| `feat(scenario): add political_context to scenario configuration — initial legitimacy state, electoral calendar, coalition stability` | BI2-N-02 | enhancement, horizon:near-term |
| `feat(orchestration): implement compound StateCondition — multi-attribute AND/OR trigger logic (supersedes #32 if resolved)` | BI2-N-03 | enhancement, horizon:near-term |
| `arch(backtesting): plan ecological backtesting case — identify case, data sources, and fidelity threshold design` | BI2-N-04 | documentation, horizon:near-term |
| `arch(orchestration): add CONDITIONALITY InputSource — encode coercive dynamics in ControlInput audit trail` | BI2-N-05 | enhancement, horizon:near-term |
| `arch(api): add threshold-crossing markers to comparative output — flag when delta crosses a defined critical value` | BI2-N-06 | enhancement, horizon:near-term |
| `docs(scenario): add explicit temporal scope disclaimer to all scenario outputs — intergenerational consequences outside modeled window` | BI2-N-07 | documentation, horizon:near-term |
| `arch(api): add trajectory comparison endpoint — return attribute values at all steps for two scenarios in one call` | BI2-N-08 | enhancement, horizon:near-term |
| `docs(scenario): document Level 1 resolution limitation in scenario output — subnational impacts not representable` | BI2-N-09 | documentation, horizon:near-term |
| `feat(orchestration): add social response event generation — ControlInputs above legitimacy threshold generate endogenous protest/backlash events` | BI2-N-10 | enhancement, horizon:near-term |
| `arch(api): add variance and percentile range to scenario comparison output — distributional delta not just point delta` | BI2-N-11 | enhancement, horizon:near-term |
| `arch(backtesting): extend backtesting statistical validity — multi-country validation suite design after Greece case` | BI2-N-12 | documentation, horizon:near-term |
