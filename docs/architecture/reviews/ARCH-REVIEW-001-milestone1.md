# ARCH-REVIEW-001: Full Council Architecture Review — Milestone 1

**Review type:** Full — all Domain Intelligence Council members, CHALLENGE mode
**Scope:** ADR-001, ADR-002, CLAUDE.md, `docs/scenarios/module-capability-registry.md`,
all files in `docs/adr/`
**Facilitated by:** Architecture Review Facilitator
**Date:** 2026-04-16
**Status:** Complete — GitHub Issues created for all Immediate and Near-Term findings

---

## Executive Summary

The Milestone 1 architecture establishes a sound structural foundation: immutable
state transitions, an explicit endogenous/exogenous distinction, a clean module
interface, and a working propagation engine with 42 passing tests. The design
decisions in ADR-001 and ADR-002 are architecturally coherent and the rationale
for the choices made (graph over relational tables, ControlInput layer over
module-handled inputs) is well-documented.

The council review surfaces a consistent finding across all nine frameworks:
**the architecture makes aspirational claims that the current implementation
does not yet support.** The `MeasurementFramework` enum exists but attributes
are untagged. The human cost ledger is a stated primary output but no human
development attributes exist in any entity. Uncertainty quantification is
described as a guiding principle ("we are calibrated, not confident") but every
output is a point estimate. Backtesting is called "the most important test suite"
but no backtesting infrastructure exists.

These are not failures — they are Milestone 1 scope decisions. But several of
them create risks that compound across milestones: a flat `Dict[str, float]`
attribute store that doesn't distinguish stocks from flows or tag measurement
frameworks will require breaking changes to fix later; a propagation model
that is structurally linear will produce systematically wrong outputs for
crisis dynamics regardless of how well it is calibrated; and a simulation
that has never been run against historical data has no empirical grounding for
any quantitative claim.

**Key tensions identified by the council:**

- The Chief Methodologist and the Development Economist agree that outputs
  currently have no calibration basis and should not be presented as quantitative
  estimates — but the Investment Agent (RISK-TOLERANT mode) notes that excessive
  uncertainty hedging may prevent the tool from being usable for the decisions
  it is designed to inform.
- The Ecological Economist and the Intergenerational Advocate agree that the
  stock/flow distinction is architecturally critical and must be addressed before
  significant module development begins — but the Political Economist notes that
  governance and political variables are also misrepresented by the current
  one-dimensional attribute model, and those modules will be built before
  ecological ones.
- The Social Dynamics Agent and the Political Economist agree that social
  legitimacy must be a state variable that affects policy efficacy — the
  Geopolitical Analyst notes that this is also the mechanism through which
  external pressure campaigns operate, making it a security dimension as well.

The council identified **24 distinct blindspots**: 6 immediate, 10 near-term,
and 8 long-term. GitHub Issues have been created for all immediate and near-term
findings.

---

## Findings by Agent

---

### Development Economist Agent — CHALLENGE

**Finding 1: MeasurementFramework is structural but not operational.**
The `MeasurementFramework` enum (`FINANCIAL`, `HUMAN_DEVELOPMENT`, `ECOLOGICAL`,
`GOVERNANCE`) exists in the data model and is referenced in `to_events()` methods.
But `SimulationEntity.attributes` is a flat `Dict[str, float]` with no framework
tagging. The claim that the simulation "produces outputs simultaneously in multiple
measurement frameworks" describes an architectural aspiration — in practice,
`gdp_growth` and `political_stability` coexist in the same dict without any
structural enforcement of which framework they belong to. A query for "all human
development attributes" cannot be answered by the current model without inspecting
string key names. This will produce subtle misattribution errors in any multi-framework
output rendering downstream.

**Finding 2: The simulation is seeded exclusively with financial proxies.**
The demo scenario (`backend/scripts/demo_scenario.py`) seeds all ten entities
with four attributes: `gdp_growth`, `debt_gdp_ratio`, `trade_openness`, and
`political_stability`. No health indicators. No education attainment. No poverty
headcount. No child mortality. No food security proxy. These are not missing
because the data is unavailable — IMF WEO, World Bank WDI, and WHO all publish
them. They are missing because the capability registry correctly notes the
Demographic and Health Module is not yet built. But the consequence is that
the simulation currently produces outputs that are structurally incapable of
informing the human development questions that motivate the project. The finance
minister sitting across from the IMF cannot ask "what does this program do to
maternal mortality in rural provinces?" — not because the question is hard, but
because the data model doesn't have those variables. Milestones 1 through 3
will be built and demonstrated with this gap, potentially establishing patterns
and user expectations that the Human Cost Ledger will have to override rather
than extend.

---

### Political Economist Agent — CHALLENGE

**Finding 3: Policy inputs produce uniform effects regardless of political context.**
The `ControlInput` hierarchy captures who made a decision (actor_id, actor_role)
and why (justification), but nothing about the political conditions under which
it was made. A fiscal consolidation injected by a government with 80% approval
rating and a parliamentary supermajority produces exactly the same simulation
effect as the same consolidation injected by a caretaker government facing a
no-confidence motion. Political legitimacy, implementation capacity, and
coalition support are not state variables in the current model. Every policy
input is implicitly modeled as having 100% implementation fidelity — which
is precisely the assumption that the historical record most consistently refutes.
This is not a minor calibration issue; it is a structural misspecification that
will produce systematically optimistic outcomes for any scenario involving
politically contested reforms.

**Finding 4: ContingentInput models thresholds, not compound political triggers.**
`StateCondition` watches a single entity, single attribute, single threshold:
`entity_id="MEX"`, `attribute="political_stability"`, `operator=LT`,
`threshold=0.3`. Real political dynamics are compound and path-dependent.
Capital controls get imposed when reserves + election proximity + IMF
relationship quality + social stability all align in a specific configuration.
The model cannot represent "if Mexico's political stability falls below 0.3
AND trade_openness has declined more than 15% AND debt_gdp_ratio has risen
above 0.7 in the previous three timesteps, trigger emergency response."
This limits the model's ability to represent the political economy of crisis
response — which is characterised precisely by the interaction of multiple
stresses, not by single-variable thresholds.

---

### Ecological Economist Agent — CHALLENGE

**Finding 5: Stock and flow variables are structurally indistinguishable.**
`SimulationEntity.attributes` stores all values as bare floats. `gdp_growth`
(a flow — a rate of change per period) and `debt_gdp_ratio` (a stock ratio)
and `trade_openness` (a structural characteristic) are all represented
identically. This creates a critical risk for ecological modeling: natural
capital stocks (forest cover, aquifer level, soil quality) are fundamentally
different from the flows they generate (timber revenue, irrigation yield,
agricultural output). A simulation that treats them identically will conflate
stock depletion with flow income — exactly the error that national accounts
made for decades and that natural capital accounting was designed to correct.
If the Ecological module is built on top of the current flat attribute store,
it will reproduce this error in the simulation's outputs.

**Finding 6: No minimum descent altitude system exists in the architecture.**
CLAUDE.md defines Minimum Descent Altitudes as "hard floors below which the
simulation flags terrain — levels below which normal policy frameworks no
longer provide protection and damage becomes irreversible or generational."
Nothing in ADR-001 or ADR-002 implements this concept. The propagation
engine has no mechanism to flag when a delta would push an attribute below
an irreversibility threshold. It will apply the delta and move on. In the
ecological domain, several such thresholds have well-documented empirical
support: aquifer depletion below replenishment rate (irreversible on human
timescales), deforestation above 40% of Amazon basin (climate feedback loop
trigger), soil erosion beyond organic matter recovery rate. A simulation
that cannot flag these thresholds is structurally incapable of the
"flight simulator" function it is designed to perform.

---

### Geopolitical and Security Analyst Agent — CHALLENGE

**Finding 7: The ControlInput taxonomy is limited to economic policy instruments.**
`MonetaryPolicyInput`, `FiscalPolicyInput`, `TradePolicyInput`,
`EmergencyPolicyInput`, `StructuralPolicyInput` — the five subclasses cover
government economic policy well. They do not cover the non-economic instruments
of statecraft: military posturing, diplomatic recognition and derecognition,
information operations, intelligence-sharing agreements, security guarantees.
`TradePolicyInput` includes `SANCTIONS` and `EXPORT_CONTROL`, which are
economic-adjacent coercive instruments. But a scenario involving military
pressure, threat of force, or diplomatic isolation — all of which have
well-documented economic transmission mechanisms — cannot be modeled with
any existing ControlInput subclass. The geopolitical dimension is reducible
to economic proxies in the current model, which means any scenario where
the primary mechanism is power rather than price will be systematically
misspecified.

**Finding 8: Relationship weights are scalar and single-dimensional.**
A `Relationship` has `relationship_type: str` and `weight: float`. A
US-China relationship has simultaneously a trade dimension, a military
rivalry dimension, an information competition dimension, a technology
supply chain dimension, and a sovereign debt holding dimension. Each of
these dimensions has different weight, different directionality, and
different propagation dynamics. Representing the relationship as a single
scalar conflates all these into one number. From a geopolitical perspective,
this is not just a simplification — it structurally prevents modeling the
most important dynamics: that countries can be deeply economically
interdependent (high trade weight) while simultaneously in strategic
competition (high security rivalry weight), and that shocks can
propagate differently along each dimension. This will be particularly
consequential for any US-China scenario, which is exactly the scenario
the demo scenario models.

---

### Intergenerational Equity Advocate Agent — CHALLENGE

**Finding 9: No mechanism tracks compounding trajectories across timesteps.**
Each simulation step applies deltas additively to a fresh state constructed
from the previous state. This correctly models the immutability contract.
But it means there is no architectural mechanism to track the trajectory
of a variable — whether it has been above threshold for three consecutive
periods, whether debt has been compounding, whether a country has been
running persistent deficits for a decade. The intergenerational consequences
of policy are almost entirely about trajectories and their compounding, not
about point-in-time deltas. A fiscal program that cuts education spending
by 3% for five years imposes costs that compound: the children who don't
receive schooling in year 1 carry that deficit forward. The current model
sees five separate 3% cuts, each isolated, with no structure to represent
or flag the compounding harm.

**Finding 10: Debt structure is a scalar with no maturity or creditor profile.**
`debt_gdp_ratio: float` stores a single number for Japan (2.53), the USA
(1.22), and Vietnam (0.37). Japan's debt is 95% domestically held, yen-denominated,
with the Bank of Japan as a major holder and a mature domestic institutional
investor base. Vietnam's debt is partially foreign-currency-denominated with
shorter maturities and external creditor concentration. These countries have
entirely different intergenerational risk profiles from their debt — but the
simulation represents them identically. Debt restructuring scenarios, IMF
program evaluations, and any analysis of debt sustainability will produce
wrong structural conclusions from this data model because the variable that
most determines intergenerational consequences (maturity profile, creditor
composition, currency denomination) is completely absent.

---

### Community and Cultural Resilience Agent — CHALLENGE

**Finding 11: National aggregates erase community-level effects by construction.**
`SimulationEntity` at Level 1 is a country. Every entity attribute is a
national average or aggregate. A tariff shock that is devastating to
subsistence farmers in Oaxaca while being mildly beneficial to export
manufacturers in Monterrey will register as a small net effect on Mexico's
`gdp_growth` attribute — or as a trade exposure number if modeled through
the tariff propagation mechanism. The community that bears the cost is
invisible in the data model. This is not resolved by adding more attributes
to the country entity — it is a structural consequence of the Level 1 entity
model. Higher resolution (Level 2-4) is documented in CLAUDE.md as a future
architectural feature, but the current design has no placeholder for community
variables, no plan for how community-level data would be linked to national
entities, and no specification for how community-level harm thresholds would
be tracked.

**Finding 12: No Community or Social Fabric module is specified.**
The module registry in CLAUDE.md lists: Geopolitical, Macroeconomic, Trade
and Currency, Monetary System, Capital Flow, National Asset Registry,
Demographic and Health, Climate, Financial Warfare, and Institutional
Cognition. There is no Community Resilience module and no Social Fabric
module. The Demographic and Health module handles population dynamics and
health system capacity — but not social trust, community cohesion, cultural
continuity, or informal mutual aid networks. These are not modeling luxuries;
they are the primary mechanisms through which communities either absorb
or collapse under economic stress. A simulation that models fiscal policy
effects on GDP but not on social fabric is systematically blind to the
mechanism by which GDP shocks become generational damage.

---

### Investment and Capital Formation Agent — CHALLENGE

**Finding 13 (RISK-AVERSE mode): No investment climate state variables exist.**
Foreign direct investment flows, portfolio investment, credit default swap
spreads, risk premia, and sovereign credit ratings are not modeled as entity
attributes. The simulation can model political instability (via `political_stability`)
and fiscal stress (via `debt_gdp_ratio`) as inputs to a shock, but has no
mechanism to translate those into investment climate effects. The feedback
loop from governance deterioration to risk premium widening to capital
outflow to currency pressure to growth slowdown — which is the primary
transmission mechanism of political risk in developing markets — is
completely absent. A privatization scenario or an infrastructure investment
scenario cannot currently be modeled at all because the investment side of
the transaction has no representation.

**Finding 14 (RISK-TOLERANT mode): Private capital decisions are unrepresentable.**
The ControlInput taxonomy covers government policy instruments exclusively.
There is no mechanism to model private sector investment decisions: a DFI
committing to a $500M infrastructure guarantee, a private equity fund
taking a stake in a privatized utility, foreign investors buying or selling
sovereign debt, or a multilateral bank providing budget support. These are
not edge cases — they are the primary mechanisms through which capital flows
into and out of developing economies. A sovereign wealth fund deciding to
exit Emerging Markets in response to a risk event is likely to have larger
economic consequences than many government policy decisions, but it cannot
be modeled with any existing input type. The model simulates government
decisions in a world where private capital is passive — which is exactly
backwards for the scenarios the tool is designed to analyze.

**Finding 15 (CATALYTIC mode): Public de-risking instruments are absent.**
MIGA guarantees, IFC blended finance tranches, DFI first-loss capital,
currency hedging facilities, and political risk insurance — these are the
instruments that crowd in private capital to frontier markets. They are
the policy levers that answer the question "what would it cost to attract
private infrastructure investment to this country?" None of them exist
in the ControlInput taxonomy. A finance minister asking this question
cannot use the simulation to explore the answer.

---

### Social Dynamics and Behavioral Economics Agent — CHALLENGE

**Finding 16: Policy efficacy is not modulated by social legitimacy.**
The propagation engine applies `affected_attributes` deltas unconditionally
when an event fires. A fiscal adjustment ControlInput with `value=-0.03`
reduces GDP growth by 3% regardless of whether that adjustment has 80%
public support or is being implemented against mass protests and a general
strike. Social legitimacy — the population's willingness to accept a policy
and cooperate with its implementation — is the most important variable in
determining whether a technically correct policy achieves its intended
effect. It is not a state variable anywhere in the current architecture.
This produces systematic optimism bias: every injected policy achieves
its intended effect, which is precisely what the historical record of
structural adjustment programs contradicts most consistently.

**Finding 17: Propagation is linear — information cascades and bank runs are unrepresentable.**
The event propagation model applies `delta × attenuation_factor × edge.weight`
at each hop. This models a diffusion process — the gradual seepage of an
economic shock through a network. Bank runs, information cascades, and
social panics are not diffusion processes — they are threshold-crossing
phenomena where below the threshold nothing happens and above it the dynamic
accelerates beyond any linear model's range. The Lebanon 2019 bank run was
triggered by WhatsApp messages; the 1997 Thai baht crisis was accelerated
by herding behavior among currency traders; the 2008 financial crisis was
amplified by correlated de-leveraging that violated all standard correlation
assumptions. A purely linear propagation model cannot represent any of
these dynamics. The architecture needs a non-linear propagation mode for
crisis scenarios.

---

### Chief Methodologist Agent — CHALLENGE

**Finding 18: All outputs are point estimates with no uncertainty representation.**
`SimulationEntity.attributes` stores bare floats. The propagation engine
computes deterministic deltas. Every simulation output is a single number.
But the inputs themselves carry substantial uncertainty: IMF WEO GDP growth
forecasts have historical forecast errors averaging 1-2 percentage points
at the one-year horizon; World Bank WGI political stability estimates for
many developing countries have 90% confidence intervals as wide as the
full indicator range. Propagating uncertain inputs through a deterministic
engine produces outputs that appear precise but are not. The "No False
Precision" guiding principle is violated structurally: there is no mechanism
in the current architecture to represent, propagate, or display uncertainty.
Every output will look equally certain regardless of whether it rests on
highly reliable input data or on estimates with confidence intervals spanning
the full range of plausible values.

**Finding 19: Attenuation parameters have no documented calibration basis.**
The demo scenario uses `attenuation_factor=0.6`, `max_hops=2`. These are
structurally reasonable choices for a first-order model. But they have no
documented empirical basis. What historical data were they calibrated against?
What is the 95% confidence interval on these values? How sensitive are
outputs to changes in attenuation_factor from 0.4 to 0.8? The module
capability registry acknowledges that "magnitudes are structurally meaningful
but should not be interpreted as economic impact estimates" — but the
architecture has no path to changing this. Without backtesting infrastructure,
there is no mechanism to calibrate these parameters against historical cases,
which means every scenario run will produce outputs with unknown bias
characteristics. The propagation parameters are currently aesthetic choices
that happen to produce plausible-looking outputs, not calibrated estimates.

**Finding 20: No backtesting infrastructure exists.**
CLAUDE.md calls backtesting "the most important test suite" and "epistemic
discipline." The QA Agent workflow describes running "backtesting validation
suites." But no backtesting framework exists anywhere in the codebase —
not a stub, not a directory, not a specification. There is no mechanism
to run a historical scenario (Thailand 1997, Argentina 2001, Greece 2010)
from a known starting state with documented historical events injected as
ControlInputs, compare outputs to historical record, and measure model
fidelity. The simulation has never been run against history and its outputs
have no empirical grounding. This is the most important gap in the current
architecture relative to the project's stated epistemic standards.

---

## Blindspot Inventory

### Immediate — affects current Milestone 1 scope or creates compounding architectural risk

| ID | Finding | Source Agent | Risk if unaddressed |
|---|---|---|---|
| BS-001 | All outputs are point estimates — no uncertainty representation | Chief Methodologist | Violates "No False Precision" principle; outputs will appear more reliable than they are at every milestone |
| BS-002 | `MeasurementFramework` enum defined but attributes are untagged — multi-framework claim unimplemented | Development Economist | Multi-framework output rendering will require breaking data model changes later |
| BS-003 | No backtesting infrastructure exists — simulation has no empirical grounding | Chief Methodologist | Parameters remain uncalibrated; no validation possible; epistemic claims unsupported |
| BS-004 | No Minimum Descent Altitude (MDA) threshold system — irreversibility thresholds not flagged | Ecological Economist | Simulation will cross irreversibility thresholds without warning |
| BS-005 | Social legitimacy not a state variable — policy efficacy assumed 100% regardless of political reception | Social Dynamics / Political Economist | Systematic optimism bias in all reform scenarios |
| BS-006 | Attenuation parameters (0.6, max_hops=2) have no documented calibration basis | Chief Methodologist | Users cannot assess output reliability; parameters are aesthetic not empirical |

### Near-Term — affects Milestone 2-3 design decisions

| ID | Finding | Source Agent | Risk if unaddressed |
|---|---|---|---|
| BS-007 | No cohort disaggregation at entity level — national averages hide distributional impacts | Development Economist | Human Cost Ledger (Milestone 4) will need entity model restructuring |
| BS-008 | Linear additive propagation — misspecified for crisis and cascade dynamics | Social Dynamics / Chief Methodologist | Crisis scenarios systematically underestimate severity and speed |
| BS-009 | Stock and flow variables not architecturally distinguished | Ecological Economist / Intergenerational Advocate | Ecological and debt modules will conflate capital depletion with income |
| BS-010 | Multi-step policies not modeled — all interventions are one-shot shocks | Political Economist | IMF programs, multi-year fiscal consolidations cannot be represented |
| BS-011 | `StateCondition` supports only single-attribute triggers — compound triggers unsupported | Political Economist | Cannot model compound political/economic crisis triggers |
| BS-012 | No private capital investment ControlInput types — model is government-policy only | Investment Agent (RISK-TOLERANT) | Capital flow scenarios, FDI, DFI instruments entirely unrepresentable |
| BS-013 | No investment climate state variables — governance→capital feedback absent | Investment Agent (RISK-AVERSE) | Governance deterioration has no capital flow transmission |
| BS-014 | Relationship weights are static — cannot update in response to events | Ecological Economist / Geopolitical Analyst | Trade diversion, alliance shifts after a shock not representable |
| BS-015 | No information cascade or non-linear propagation mechanism | Social Dynamics Agent | Bank runs and social panics are structurally absent from crisis modeling |
| BS-016 | Debt structure is a scalar — no maturity, currency, or creditor profile | Intergenerational Advocate | Debt sustainability analysis will produce wrong structural conclusions |

### Long-Term — architectural considerations for later milestones

| ID | Finding | Source Agent |
|---|---|---|
| BS-017 | Scalar relationship weights collapse multi-dimensional power relationships | Geopolitical Analyst |
| BS-018 | Non-economic ControlInput types absent (military, diplomatic, information) | Geopolitical Analyst |
| BS-019 | Community/subnational representation has no data model pathway | Community Resilience |
| BS-020 | No Community or Social Fabric module specified in module registry | Community Resilience |
| BS-021 | Multi-actor contingent logic absent — reactive entity behaviors must be hand-scripted | Geopolitical Analyst |
| BS-022 | Public de-risking instruments (MIGA, DFI blended finance) absent from ControlInput taxonomy | Investment Agent (CATALYTIC) |
| BS-023 | Political legitimacy absent from policy efficacy modeling | Political Economist |
| BS-024 | Private sector actor model absent — capital has no agency in the simulation | Investment Agent (RISK-TOLERANT) |

---

## Framework Tensions

The council review produced three significant tensions where frameworks point
in genuinely opposite directions. These require human judgment — the council
does not resolve them.

**Tension 1: Calibration rigor vs. usability under uncertainty**
The Chief Methodologist, Development Economist, and Intergenerational Advocate
all argue for explicit uncertainty quantification before outputs are shown to
users. The Investment Agent (RISK-TOLERANT mode) notes that a tool that qualifies
every output with wide confidence intervals may be less useful to a finance
minister under time pressure than a tool that provides a clear directional signal
with a documented caveat. There is no technically correct answer to how much
uncertainty display is helpful vs. paralyzing.

**Tension 2: Adding attributes now vs. architectural refactoring later**
The Development Economist and Intergenerational Advocate argue for adding human
development and ecological attributes to entities immediately, before milestone
patterns calcify. The Political Economist notes that governance module development
will come before ecological module development and will be built on the same flat
attribute model — adding complexity before any module is built may slow the
first modules without improving their quality. The Chief Methodologist notes that
adding attributes without framework tagging only deepens BS-002.

**Tension 3: Level 1 country entities vs. community visibility**
The Community Resilience Agent argues that community-level effects are invisible
by construction in a country-entity model and that some community-level
placeholder is needed. The Architecture design (CLAUDE.md) explicitly stages
higher resolution as a feature that activates per scenario — Level 1 globally,
Level 2+ for specific regions when the question demands it. Building community
representation into Level 1 country entities contradicts this architectural
staging. The tension is between methodological completeness and architectural
coherence.

---

## Recommended GitHub Issues

All issues below have been created using the `gh` CLI. Issue numbers are
recorded after creation.

### Immediate Issues (horizon:immediate)

| Issue | Title | Blindspot |
|---|---|---|
| #22 | feat: add uncertainty quantification to simulation outputs — distributions not point estimates | BS-001 |
| #23 | feat: tag entity attributes with MeasurementFramework — enforce multi-framework separation | BS-002 |
| #24 | feat: implement backtesting infrastructure — historical scenario replay and model validation | BS-003 |
| #25 | feat: implement Minimum Descent Altitude threshold system — flag irreversibility crossings | BS-004 |
| #26 | feat: add social legitimacy state variable and policy efficacy modulation | BS-005 |
| #27 | docs: document calibration basis for attenuation parameters — methodology or explicit placeholder | BS-006 |

### Near-Term Issues (horizon:near-term)

| Issue | Title | Blindspot |
|---|---|---|
| #28 | feat: add cohort disaggregation architecture to entity model — income quintile × age band stubs | BS-007 |
| #29 | feat: implement non-linear propagation mode for crisis and cascade dynamics | BS-008 / BS-015 |
| #30 | feat: distinguish stock vs. flow variables in entity attribute model | BS-009 |
| #31 | feat: implement multi-step policy inputs — sustained programs across multiple timesteps | BS-010 |
| #32 | feat: implement compound StateCondition — multi-attribute AND/OR trigger logic | BS-011 |
| #33 | feat: add private capital ControlInput types — FDI, DFI, portfolio investment | BS-012 |
| #34 | feat: add investment climate state variables — risk premium, credit spread, FDI stock | BS-013 |
| #35 | feat: implement dynamic relationship weight updating — weights respond to event history | BS-014 |
| #36 | feat: add debt structure attributes — maturity profile, currency denomination, creditor composition | BS-016 |
