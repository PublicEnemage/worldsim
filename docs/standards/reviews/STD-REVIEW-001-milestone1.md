# STD-REVIEW-001: Standards and Policy Review — Milestone 1

**Review type:** Full — all Domain Intelligence Council members (Track 1) and
all technical agents (Track 2), with cross-track reconciliation
**Scope:** `docs/CODING_STANDARDS.md`, `docs/DATA_STANDARDS.md`,
`docs/POLICY.md`, `docs/CONTRIBUTING.md`, Domain Intelligence Council section
of `CLAUDE.md`
**Seeded with:** Standards gaps identified from ARCH-REVIEW-001 Finding Disposition
**Date:** 2026-04-16
**Status:** Phase 3 Complete — Phase 4 (Engineering Lead Synthesis) pending
**PR:** See STD-REVIEW-001 PR for full diff

---

## Executive Summary

The standards documents are methodologically serious for the domains they
cover — monetary arithmetic, calendar systems, territorial nomenclature,
data provenance — and show genuine care for correctness. The standards suite
is, however, substantially narrower than the project's stated mission. CLAUDE.md
describes a simulation that produces outputs in four simultaneous measurement
frameworks with no false precision, calibrated against historical data, visible
to users with appropriate uncertainty representation. The current standards
describe a simulation that handles monetary arithmetic, calendar edge cases, and
territorial designations correctly.

The gap between the two is the subject of this review.

**Most significant Track 1 finding (council):** `CODING_STANDARDS.md` has no
requirement that modules tag their events with a `MeasurementFramework` value.
The four-framework architecture is structurally enforced nowhere. A fully
compliant module can produce outputs that are invisible to the human cost
ledger, the ecological framework, or the governance framework, and nothing
in the current standards will catch it.

**Most significant Track 2 finding (technical):** The `SimulationEntity.attributes`
store is `Dict[str, float]` throughout the codebase, while `CODING_STANDARDS.md`
forbids `float` for monetary arithmetic. This is a direct contradiction between
the data model (ADR-001) and the coding standards — and the boundary between the
typed world (`MonetaryValue`, `Quantity`) and the attribute store is nowhere defined.
Every module author faces an arbitrary choice the standard should have resolved.

**Three CONVERGENT finding pairs** (same gap identified independently by both
tracks) are the highest-priority amendments: MeasurementFramework event tagging
enforcement, the tier-to-uncertainty quantification formula, and the parameter
calibration tier system.

**One CONFLICT finding** requires Engineering Lead disposition before the
corresponding GitHub Issue can be created: the tension between the Investment
Agent's requirement for opportunity cost assessment (Track 1) and the Security
Agent's concern that comparative investment attractiveness outputs reconstruct
the prohibited cross-country vulnerability ranking (Track 2).

**Architecture license impact:** Both ADR-001 and ADR-002 are UNDER-REVIEW
pending this review. Four dependent ADRs (ADR-003 through ADR-006) are
deferred until standards are updated and ADR licenses renewed.

---

## Track 1 Findings — Domain Intelligence Council

---

### Development Economist Agent — CHALLENGE

**T1-F1: `CODING_STANDARDS.md` has no rule requiring MeasurementFramework tags on module outputs.**

The CODING_STANDARDS.md diagram shows the `Event` class with a `framework:
MeasurementFramework` field. `CONTRIBUTING.md` says macroeconomic modules must
produce events tagged `MeasurementFramework.HUMAN_DEVELOPMENT` for welfare
consequences. But neither document contains a stated standard requiring
this — it appears only in an illustrative example in CONTRIBUTING.md. A module
that generates only `FINANCIAL` events is fully standards-compliant. The entire
four-framework architecture rests on an unenforced convention.

Amendment required: `CODING_STANDARDS.md` must add an explicit rule — modules
affecting welfare-relevant attributes must generate events tagged with
`MeasurementFramework.HUMAN_DEVELOPMENT` and the module's unit tests must verify
this. The word "must" is currently absent from any statement about framework
tagging.

**T1-F2: `DATA_STANDARDS.md` has no standard for human development indicator representation.**

The document covers monetary values (with full type specification, canonical
units, PPP vs. market rate rules), physical quantities (dimensional safety,
canonical units), calendar systems (five calendar systems), territorial
designations (disputed territory framework). Human welfare indicators — HDI
components, child stunting rates, maternal mortality, food security indices,
education attainment, health system capacity — have no analogous treatment.

This means human development data enters the simulation with less rigorous
treatment than monetary data. For the project's primary output dimension, this
is a priority inversion. At minimum, DATA_STANDARDS.md should specify which
human development data sources are Tier 1, what their methodology versioning
requirements are, and how their confidence tiers translate to output uncertainty.

---

### Political Economist Agent — CHALLENGE

**T1-F3: Political feasibility and social legitimacy are not required state variables in any standard.**

CLAUDE.md describes political legitimacy as a core simulation concern (Political
Economist profile, Get-There-Itis failure mode). DATA_STANDARDS.md has no
standard for political or social variables. A simulation that ignores
implementation feasibility entirely — applying all ControlInputs at 100% fidelity
regardless of political context — is fully standards-compliant. This is the
single largest source of systematic optimism bias in scenario outputs.

Amendment required: DATA_STANDARDS.md should define `social_legitimacy`
(range 0–1), `implementation_capacity` (range 0–1), and `policy_acceptance`
as required state variables for country entities, with documentation of
approved measurement sources (World Bank WGI, V-Dem, Freedom House) and
methodology versioning requirements.

**T1-F4: Governance indicators have no methodology version or vintage dating standard.**

`political_stability` appears in the demo scenario seeded from World Bank WGI
2023. But DATA_STANDARDS.md has no standard governing governance indicator
usage — no methodology version requirement (WGI methodology has changed over
its history), no vintage dating requirement for backtesting use, no confidence
tier assignment for this source. A governance indicator from WGI 2015 and WGI
2023 are not directly comparable; the absence of a versioning standard allows
this incompatibility to go undetected.

Amendment required: DATA_STANDARDS.md should add a governance indicator subsection
specifying approved sources, methodology version tracking, vintage dating
requirements, and confidence tier assignments.

---

### Ecological Economist Agent — CHALLENGE

**T1-F5: `DATA_STANDARDS.md` Dimension enum has no ecological or natural capital dimensions.**

The `Dimension` enum covers `MONETARY_VALUE`, `POPULATION`, `MASS`, `ENERGY`,
`POWER`, `TEMPERATURE`, `AREA`, `VOLUME`, `CROP_YIELD`, `ENERGY_INTENSITY`,
`MONETARY_PER_CAPITA`, `RATIO`, `INDEX`. There is no `NATURAL_CAPITAL_STOCK`,
`ECOSYSTEM_SERVICE_FLOW`, `ECOLOGICAL_FOOTPRINT`, `BIODIVERSITY_INDEX`, or
`BIOLOGICAL_PRODUCTIVITY`. This means ecological variables either get forced
into `INDEX` (losing their specific dimensional meaning) or cannot be cleanly
represented at all. When the Ecological module is built, every ecological
variable will require a workaround for the absence of appropriate dimensions.

**T1-F6: `Quantity` type has no stock-or-flow attribute.**

`Quantity` stores `value: Decimal`, `unit: Unit`, `observation_date: date`,
`source_registry_id: str`, `confidence_tier: int`. It has no field indicating
whether the quantity is a stock (accumulated capital) or a flow (rate of change
per period). This distinction has mathematical consequences: the same delta
arithmetic applied to a flow (GDP growth) is wrong when applied to a stock
(forest cover). A simulation that reduces forest cover by 5% per year for
ten years is depleting a stock, not adjusting a rate. The current `Quantity`
type cannot represent this distinction.

**T1-F7: `CONTRIBUTING.md` has no ecological output requirement.**

CONTRIBUTING.md says: "a macroeconomic module that models fiscal contraction
must produce events tagged with `MeasurementFramework.HUMAN_DEVELOPMENT` for the
welfare consequences, not just `MeasurementFramework.FINANCIAL`." There is no
analogous statement for ecological consequences. A trade liberalization module
that affects deforestation rates through agricultural expansion can be fully
standards-compliant while producing zero ecological events. The human cost
ledger has a partial requirement; the ecological ledger has none.

---

### Geopolitical and Security Analyst Agent — CHALLENGE

**T1-F8: `DATA_STANDARDS.md` permanent URL requirement in `SourceRegistration` creates potential intelligence exposure.**

`SourceRegistration` requires `permanent_url: str` (DOI preferred). This is
appropriate for standard international datasets. But WorldSim's module registry
includes a Financial Warfare Module modeling sanctions exposure, SWIFT dependency,
and currency attack vulnerability. A scenario using a data source documenting a
specific country's payment network exposure structure — with that source URL
committed to the public repository — reveals which specific analytical data
streams are being monitored for that country's vulnerability. In sensitive
political contexts, this is an operational security concern.

Amendment required: `SourceRegistration` should add a `classification_level`
field (`PUBLIC | INTERNAL | SENSITIVE`) with different URL handling per level.
`SENSITIVE` sources document methodology without publishing the specific access
URL in the public repository.

---

### Intergenerational Equity Advocate Agent — CHALLENGE

**T1-F9: No discount rate standard in `DATA_STANDARDS.md`.**

The choice of discount rate for intergenerational analysis is among the most
consequential methodological choices in any long-run assessment — a 3% rate
versus a near-zero Stern-type rate implies radically different present values
for future generations' welfare. DATA_STANDARDS.md is silent on this.
Any discount rate (including an implicit 100% rate that ignores future
consequences entirely) is currently standards-compliant. The policy commits
to showing intergenerational consequences but provides no standard for how
they are calculated.

Amendment required: DATA_STANDARDS.md should require: (a) explicit documentation
of the discount rate used for any intergenerational calculation, (b) sensitivity
analysis across at least three discount rate assumptions (near-zero / mid /
market rate), (c) display of all three in outputs affecting multi-generational
decisions.

**T1-F10: `POLICY.md` does not specify a minimum simulation horizon for intergenerational effects.**

POLICY.md acknowledges that "the full intergenerational consequences of decisions
(education interruption, stunting, institutional damage) extend beyond the
simulation horizon." But it specifies no minimum horizon, no requirement to
extend the horizon when intergenerational effects are material, and no guidance
on flagging outputs where the simulation terminates before the main consequences
appear. A scenario that models an IMF program with its heaviest human costs
appearing in year 8 but uses a 5-year simulation horizon produces outputs that
look clean but are structurally misleading.

---

### Community and Cultural Resilience Agent — CHALLENGE

**T1-F11: No standards for social capital, community resilience, or informal economic activity.**

DATA_STANDARDS.md handles monetary values, physical quantities, calendar
systems, and territorial designations with specificity and care. Social capital,
community cohesion, informal mutual aid networks, and cultural continuity have
no data standard treatment. These dimensions appear in CLAUDE.md (Community
Resilience Agent profile) and POLICY.md (limitations section) but have produced
no standards requirements. Without a standard, these variables cannot be
rigorously incorporated even when data sources for them exist (World Bank Social
Capital surveys, Putnam trust indices, informal economy estimates from ILO).

**T1-F12: `CONTRIBUTING.md` has no community-level representation requirement.**

CONTRIBUTING.md's non-negotiable requirements list covers Decimal for monetary
values, UTF-8 encoding, ISO 3166-1 alpha-3 codes, seasonal context, fiscal year
registry, dimensional safety. None require any consideration of community-level
effects. A perfectly compliant contribution can aggregate all outputs to national
level and never surface the effects on the communities — subsistence farmers,
informal workers, indigenous populations — whose situations are the mission's
primary concern.

---

### Investment and Capital Formation Agent — CHALLENGE

**T1-F13: `DATA_STANDARDS.md` has no standards for investment climate variables.**

The document covers monetary values thoroughly. It has no standards for FDI
stock measurement, portfolio flow metrics, sovereign credit rating methodology,
risk premium calculation, credit default swap spread interpretation, or capital
flow velocity measurement. These are the primary variables through which private
capital makes country engagement decisions. Without standards, any module
implementing investment climate analysis will make arbitrary methodological
choices in the absence of guidance.

**T1-F14: Standards require harm assessment but not opportunity cost assessment. [CONFLICT — see reconciliation section]**

CODING_STANDARDS.md requires human cost ledger outputs. CONTRIBUTING.md
emphasizes harm identification. No equivalent requirement exists for
opportunity cost analysis: where are the latent investment opportunities, what
is the cost of foreclosing them, and what public instruments would crowd in
private capital? This asymmetry of documented requirements creates structural
bias toward excessive caution — a simulation that identifies all risks without
surfacing the pathways through which investment and growth are achievable.

*Note: This finding is flagged CONFLICT in reconciliation — see Section 5.*

---

### Social Dynamics and Behavioral Economics Agent — CHALLENGE

**T1-F15: No standards for social legitimacy, public trust, or policy acceptance variables.**

DATA_STANDARDS.md has no section for social or behavioral variables. `political_stability`
(WGI percentile rank) is a governance quality measure, not a public sentiment
measure. Social legitimacy — the population's willingness to accept a policy
and cooperate with its implementation — is a distinct dimension that degrades
through different mechanisms and has different consequences for policy efficacy.
No approved source, no methodology version, no confidence tier, no update
frequency standard.

**T1-F16: `CODING_STANDARDS.md` has no standard for policy efficacy modulation.**

Every ControlInput is applied at 100% efficacy. There is no standard specifying
how a module should reduce a policy's effect when social legitimacy is below a
threshold. The absence of this standard means the optimism bias identified in
ARCH-REVIEW-001 (BS-005) cannot be corrected by module implementation alone —
the correction requires a standard that defines the modulation mechanism.

---

### Chief Methodologist Agent — CHALLENGE

**T1-F17: `DATA_STANDARDS.md` promises a quantified tier-to-uncertainty relationship but specifies no formula.**

DATA_STANDARDS.md says: "confidence intervals in simulation outputs widen as
input data tier decreases. This relationship is quantified, not qualitative —
a Tier 4 input produces wider output uncertainty bands than a Tier 2 input by
a documented multiplier." This is a clear commitment. But no multiplier is
documented anywhere in the standards suite. The quantification is promised but
absent. A simulation using Tier 2 inputs and one using Tier 4 inputs produce
outputs that look identically precise — the tier system changes nothing in
practice because the formula connecting tier to uncertainty width does not exist.

**T1-F18: `CODING_STANDARDS.md` has no operational definition of "calibrated."**

The backtesting requirements (CODING_STANDARDS.md) specify fidelity thresholds
for simulation outputs. But they do not specify what "calibrated" means for
individual parameters. A parameter with a citation to an IMF working paper and
one chosen by intuition are both compliant with any current standard. Proposed:
a parameter calibration tier system analogous to the data quality tier system
(Tier A: calibrated against historical data with documented methodology and
reproducible procedure; Tier B: set by analogy to calibrated parameters in
peer-reviewed models; Tier C: expert judgment with documented rationale; Tier D:
placeholder requiring future calibration). Every parameter in the codebase would
carry its calibration tier explicitly.

**T1-F19: `POLICY.md` commits to Monte Carlo but no technical standard specifies implementation.**

POLICY.md says outputs include "the range of outcomes across Monte Carlo runs."
Neither CODING_STANDARDS.md nor DATA_STANDARDS.md specifies: that Monte Carlo
runs are required, which distribution assumptions to use for input sampling,
how many runs constitute an adequate sample, or how the results should be
aggregated into confidence intervals for display. "Monte Carlo" is a commitment
in the policy document and an absence in the technical standards.

**T1-F20: `confidence_tier` conflates source quality with estimation uncertainty.**

`Quantity` and `MonetaryValue` both carry `confidence_tier: int` (1–5). This
conflates two distinct concepts: the quality of the source that produced the
data (an institutional property) and the estimation uncertainty of the specific
value (a statistical property). A Tier 1 measurement (primary official statistics)
can still have wide confidence intervals — the methodology may be sound but the
underlying phenomenon is genuinely uncertain. A Tier 4 model estimate can in
principle have tight intervals if the model is well-specified. Using one field
for both concepts produces misleading outputs.

---

## Track 2 Findings — Technical Agents

---

### QA Agent — CHALLENGE

**T2-F1: Data quality tier system has no testable observable distinguishing tier levels in practice.**

DATA_STANDARDS.md describes five tiers with weight assignments (full weight for
Tier 1-2, "weighted by stated uncertainty" for Tier 3, "used only where no
Tier 1-3 source exists" for Tier 4, "last resort" for Tier 5). But there is no
observable, computable test that distinguishes whether a given datum is Tier 2
or Tier 3 in practice. Without a testable boundary, the tier assignment is an
assertion in a docstring, not an enforceable standard. A test suite cannot verify
that the system is applying tiers correctly.

**T2-F2: Human cost ledger testing requirement has no minimum effect size specification.**

CODING_STANDARDS.md says human cost ledger tests must verify "outputs respond
correctly to the inputs that drive them" and gives examples: "austerity shock
increases poverty headcount." But "increases" with no lower bound is a degenerate
requirement. An austerity shock that increases poverty headcount by 0.00001%
would pass this test. The standard needs minimum effect size specifications
calibrated against historical cases — e.g., "a 10% GDP growth shock must produce
at least a 0.5 percentage point change in the poverty headcount indicator."

**T2-F3: Territorial positions in `POLICY.md` are aspirational — no data pipeline test enforces them.**

POLICY.md states specific handling for Taiwan (TWN, not merged with CHN),
Palestine (PSE, "State of Palestine"), Kosovo (XKX), Western Sahara (ESH),
Crimea (within UKR). But no test in the test suite verifies that imported data
respects these positions. A World Bank dataset that aggregates Taiwan into China
could pass all current tests without triggering any validation failure.
The territorial positions are declarations, not enforced constraints.

**T2-F4: "Calibrated" has no operational definition — proposed parameter calibration tier system.**

CODING_STANDARDS.md says parameters "must be calibrated against historical data"
(implied by the backtesting requirements). But no operational definition of
"calibrated" exists. A comment in a docstring asserting calibration is currently
indistinguishable from a genuinely calibrated parameter by any test. Proposed
parameter calibration tier system:
- **Tier A** — Calibrated against historical data with documented procedure,
  reproducible by a third party
- **Tier B** — Set by analogy to Tier A parameters in similar published models
  (cite the model and parameter)
- **Tier C** — Expert judgment with documented rationale (who, what reasoning)
- **Tier D** — Placeholder, not yet calibrated (explicit "requires calibration"
  flag, not a compliant production parameter)

**T2-F5: `MeasurementFramework` tagging is not enforced by any test requirement.**

`CODING_STANDARDS.md` contains a class diagram showing `framework: MeasurementFramework`
on the Event class. But there is no standard requiring module unit tests to verify
that every generated event carries a non-null `framework` value. Without a test
requirement, the tagging convention is enforced only by reviewer vigilance.

---

### Architect Agent — CHALLENGE

**T2-F6: Float-to-Decimal conversion boundary at the simulation attribute store is undefined and contradictory.**

`CODING_STANDARDS.md` states: "All monetary arithmetic uses Python's `decimal.Decimal`.
Never `float`." `DATA_STANDARDS.md` defines `MonetaryValue.amount: Decimal` and
`Quantity.value: Decimal`. But `SimulationEntity.attributes` is `Dict[str, float]`
throughout the codebase, and `Event.affected_attributes` is also `Dict[str, float]`.

This is a direct contradiction between the data model (ADR-001) and CODING_STANDARDS.md.
The boundary between the typed world (`MonetaryValue`, `Quantity`, monetary `Decimal`)
and the simulation attribute store (`float`) is nowhere defined. When should a module
use `MonetaryValue` vs. raw `float` in `attributes`? The answer is implied (always
use `float` in `attributes`, use typed types at ingestion and in the human cost
ledger) but never stated. Module authors face an arbitrary choice the standards should
have resolved explicitly.

**T2-F7: Derived unit handling for dimensionless quantities is unspecified.**

DATA_STANDARDS.md specifies canonical units for standard dimensions. When a
calculation produces a result in a derived unit with no canonical form —
`debt_service_ratio = debt_service / export_revenue` has dimension
`MONETARY_VALUE / MONETARY_VALUE = RATIO` — the standard provides no guidance
on canonical representation. Is the result stored as `Quantity(unit=RATIO_UNIT)`?
As a raw `Decimal`? The `Dimension.RATIO` value exists but has no canonical unit
specification or arithmetic rules defined.

**T2-F8: Multi-framework event generation vs. single-framework propagation interaction is underspecified.**

`CONTRIBUTING.md` implies modules should generate separate events for different
measurement frameworks ("must produce events tagged with `MeasurementFramework.HUMAN_DEVELOPMENT`
for the welfare consequences, not just `MeasurementFramework.FINANCIAL`"). But
the propagation engine processes all events in a single pass, applying deltas
additively to entity attributes. If a fiscal shock generates both a FINANCIAL
event and a HUMAN_DEVELOPMENT event targeting the same attribute (e.g.,
`gdp_growth`), will the propagation engine apply both deltas — effectively
doubling the effect? The interaction between multi-event generation and the
additive propagation model is unspecified and the current architecture cannot
answer this question from standards alone.

**T2-F9: `ControlInput` taxonomy completeness criterion is absent from standards.**

ADR-002 defines five ControlInput subclasses (Monetary, Fiscal, Trade, Emergency,
Structural). The Investment Agent profile in CLAUDE.md implies Capital Flow inputs
will be needed. The module registry lists Capital Flow Module, Financial Warfare
Module, Geopolitical Module — each of which will require new ControlInput types.
But CODING_STANDARDS.md has no criterion for when a new ControlInput subclass
requires an ADR amendment vs. can be added as implementation. This creates a gap
where new input types can proliferate without architectural review.

---

### Security and Review Agent — CHALLENGE

**T2-F10: `permanent_url` in `SourceRegistration` creates intelligence exposure for sensitive datasets.**

Same as T1-F8 — independently identified. DATA_STANDARDS.md requires
`permanent_url: str` committed to the repository. For Financial Warfare Module
datasets documenting SWIFT dependency, payment network topology, or currency
attack vulnerability structures, publishing the specific access URL reveals
which analytical data streams are being monitored. This is an operational
security concern for scenarios run on behalf of governments in politically
sensitive situations.

**T2-F11: Territorial positions create potential legal exposure in specific deployment jurisdictions.**

`POLICY.md` takes explicit positions: Taiwan as TWN (counter to PRC position),
Kosovo as XKX (unrecognized by Serbia, Russia, China, five EU members), Crimea
within Ukraine (counter to Russian position). If WorldSim is deployed or used
in jurisdictions where these positions could be deemed violations of local law,
operators could face legal exposure. The current POLICY.md provides no guidance
on jurisdiction-specific deployment considerations or risk mitigation for
operators in sensitive jurisdictions.

**T2-F12: Aggregation risk — sequential single-country analyses reconstruct the prohibited comparative ranking.**

`POLICY.md` says WorldSim "does not build cross-country comparative attack surface
ranking." But a user running the Financial Warfare Module analysis for each of
twenty countries separately, and comparing the outputs, reconstructs exactly this
ranking through a sequence of single-country analyses. The policy prohibition
addresses the interface design, not the aggregation attack. This gap should be
addressed in the dual-use section with guidance on output handling.

---

## Cross-Track Reconciliation

The QA Agent and Architect Agent reviewed all Track 1 findings. The Development
Economist, Chief Methodologist, and Political Economist reviewed all Track 2 findings.

### Reconciliation Table

| Finding ID | Description | Status | Notes |
|---|---|---|---|
| T1-F1 / T2-F5 | MeasurementFramework event tagging not enforced | **CONVERGENT** | Same gap from both tracks — see unified amendment SA-01 |
| T1-F17 / T2-F1 | Tier-to-uncertainty formula promised but absent; tier system not testable | **CONVERGENT** | Same gap — see unified amendment SA-02 |
| T1-F18 / T2-F4 | No operational definition of "calibrated"; no calibration tier system | **CONVERGENT** | Same gap — see unified amendment SA-03 |
| T1-F2 / T2-F2 | Human development indicator standards absent; HCL test has no effect size | **CONVERGENT** | Related gap — see unified amendment SA-04 |
| T1-F8 / T2-F10 | SourceRegistration permanent_url exposure (two independent identifications) | **CONVERGENT** | Same finding — see unified amendment SA-05 |
| T1-F3 / T1-F15 | Social legitimacy and political feasibility not in standards | **COMPATIBLE** | Independent of Track 2; SA-06 |
| T1-F4 | Governance indicator methodology versioning absent | **COMPATIBLE** | SA-07 |
| T1-F5 | Dimension enum missing ecological dimensions | **COMPATIBLE** | SA-08 (near-term) |
| T1-F6 | Quantity missing stock_or_flow attribute | **DEPENDENCY** | Depends on SA-02 data model decisions; see SA-09 (near-term) |
| T1-F7 | CONTRIBUTING.md has no ecological output requirement | **COMPATIBLE** | SA-10 (near-term) |
| T1-F9 | No discount rate standard | **COMPATIBLE** | SA-11 (near-term); Chief Methodologist confirms: specify sensitivity analysis across rates, not a single mandated rate |
| T1-F10 | No minimum simulation horizon for intergenerational effects | **COMPATIBLE** | SA-12 (near-term) |
| T1-F11 | No social capital standards | **COMPATIBLE** | SA-13 (long-term) |
| T1-F12 | CONTRIBUTING.md has no community-level requirement | **COMPATIBLE** | SA-14 (long-term) |
| T1-F13 | No investment climate variable standards | **COMPATIBLE** | SA-15 (near-term) |
| **T1-F14** | **Opportunity cost requirement vs. dual-use risk** | **CONFLICT** | Track 1 (Investment Agent): require opportunity cost. Track 2 (Security Agent): comparative outputs reconstruct prohibited ranking. See conflict documentation below. |
| T1-F16 | No policy efficacy modulation standard | **COMPATIBLE** | Dependent on SA-06 (social legitimacy standard) resolving first; SA-16 (near-term) |
| T1-F19 | POLICY.md commits to Monte Carlo but no technical standard | **COMPATIBLE** | Chief Methodologist confirms: compatible with T2-F1, both can proceed independently; SA-17 |
| T1-F20 | confidence_tier conflates source quality and estimation uncertainty | **COMPATIBLE** | Development Economist confirms: this is the root cause of T2-F1 and T1-F17's gap; SA-02 unified amendment should address it; mark as DEPENDENCY on SA-02 |
| T2-F3 | Territorial positions not enforced by tests | **COMPATIBLE** | Geopolitical Analyst confirms no Track 1 finding addresses enforcement gap; SA-18 |
| T2-F6 | Float-to-Decimal boundary at attribute store undefined | **COMPATIBLE** | Political Economist notes: this is also the boundary where policy efficacy modulation (SA-16) will need to operate; coordination required; SA-19 |
| T2-F7 | Derived unit handling for dimensionless quantities unspecified | **COMPATIBLE** | Chief Methodologist confirms: this is a precision gap in the ratio/rate standard; SA-20 (near-term) |
| T2-F8 | Multi-framework event generation vs. propagation interaction | **COMPATIBLE** | Development Economist: this is the same gap as T1-F1 at the architectural level; mark DEPENDENCY on SA-01 completing first |
| T2-F9 | ControlInput taxonomy completeness criterion absent | **COMPATIBLE** | Political Economist: this is also needed for social legitimacy inputs; SA-21 (near-term) |
| T2-F11 | Territorial positions create legal exposure in deployment jurisdictions | **COMPATIBLE** | SA-22 (near-term) |
| T2-F12 | Aggregation risk for single-country analyses | **COMPATIBLE** | SA-23 (near-term) |

### CONVERGENT Finding Unified Amendments

**SA-01 (T1-F1 / T2-F5): MeasurementFramework event tagging — unified amendment**

Both tracks identify that CODING_STANDARDS.md has no enforceable requirement
for MeasurementFramework event tagging. Unified amendment:

> Add to `CODING_STANDARDS.md` § Testing Requirements, subsection "Module
> Output Tagging":
>
> Every event generated by a simulation module must carry a non-null
> `MeasurementFramework` tag. Unit tests for every module must include
> an explicit assertion that all generated events have a framework tag:
> `assert all(e.framework is not None for e in events)`. A module that
> generates events without framework tags fails its own test suite.
>
> Modules that affect welfare-relevant attributes must generate at least
> one event tagged `MeasurementFramework.HUMAN_DEVELOPMENT`. Modules
> that affect ecological attributes must generate at least one event
> tagged `MeasurementFramework.ECOLOGICAL`. Framework tagging is a
> first-class output requirement, not an optional annotation.

**SA-02 (T1-F17 / T2-F1 / T1-F20): Tier-to-uncertainty formula and confidence_tier disambiguation — unified amendment**

Three findings converge on the same gap: the promised quantified relationship
between data quality tier and output uncertainty does not exist, the tier system
is not testable, and `confidence_tier` conflates source quality with estimation
uncertainty. Unified amendment:

> Split `confidence_tier` into two distinct fields on `Quantity` and
> `MonetaryValue`:
> - `source_quality_tier: int` (1–5, the existing DATA_STANDARDS.md tier
>   system — institutional quality of source)
> - `estimation_uncertainty: UncertaintyBounds | None` (the statistical
>   property — point estimate plus lower/upper bounds at a stated confidence
>   level, e.g., 90%)
>
> For `estimation_uncertainty`, DATA_STANDARDS.md must specify the tier-to-bounds
> multiplier table that was promised but absent. Minimum specification:
> - Tier 1: use stated confidence interval if published; default ±5% if absent
> - Tier 2: use stated uncertainty if published; default ±10% if absent
> - Tier 3: use stated uncertainty if published; minimum ±15% regardless
> - Tier 4: minimum ±30%; document model assumptions
> - Tier 5: minimum ±50%; display prominently

**SA-03 (T1-F18 / T2-F4): Parameter calibration tier system — unified amendment**

Both tracks identify that "calibrated" has no operational definition. Unified
amendment:

> Add to `CODING_STANDARDS.md` a Parameter Calibration Tier System,
> analogous to the DATA_STANDARDS.md data quality tier system:
>
> - **Tier A** — Calibrated against historical data using a documented,
>   reproducible procedure. The procedure, the historical dataset, and
>   the goodness-of-fit metric are documented in code comments or a
>   calibration note in `docs/calibration/`.
> - **Tier B** — Set by analogy to a Tier A parameter from a published,
>   peer-reviewed model. Cite the paper and the parameter.
> - **Tier C** — Expert judgment. The expert, the reasoning, and the
>   uncertainty range are documented.
> - **Tier D** — Placeholder, not yet calibrated. The parameter carries
>   a `# CALIBRATION: Tier D — requires historical calibration` comment.
>   Tier D parameters are not acceptable in production scenario outputs
>   without explicit user warning.
>
> All parameters must declare their calibration tier. CI enforces that no
> Tier D parameter appears in production code paths without a logged warning
> in the simulation output.

**SA-04 (T1-F2 / T2-F2): Human development indicator standards and HCL test effect size — unified amendment**

Both tracks identify gaps in the human cost ledger standard: missing source
standards for human development data (Track 1), and missing minimum effect size
for tests (Track 2). Unified amendment:

> Add to `DATA_STANDARDS.md` a Human Development Indicators subsection
> specifying: approved Tier 1 sources (UNDP HDI, WHO Global Health
> Observatory, World Bank WDI health and education indicators), methodology
> versioning requirements (HDI methodology has changed in 2010, 2014, 2020
> revisions), confidence tier assignments by source, and minimum update
> frequency.
>
> Amend `CODING_STANDARDS.md` § Human Cost Ledger Testing to add: minimum
> effect size requirements for human cost ledger tests, expressed as a
> calibration ratio. A 10% GDP shock must produce at least a [Tier C calibration
> value, documented in `docs/calibration/`] change in human development
> indicators. The specific values are to be set through backtesting against
> the Greece 2010-2015 case once backtesting infrastructure (#24) is in place.
> Until then, tests must at minimum verify directional correctness (sign of
> change) and non-trivial magnitude (change > 0.1% of baseline value).

**SA-05 (T1-F8 / T2-F10): SourceRegistration classification level — unified amendment**

Same finding identified by Geopolitical Analyst and Security Agent independently.
Unified amendment:

> Add `classification_level: SourceClassification` to `SourceRegistration`:
> ```python
> class SourceClassification(Enum):
>     PUBLIC = "public"           # URL published in repository
>     INTERNAL = "internal"       # URL documented in internal docs only
>     SENSITIVE = "sensitive"     # URL and access method not published
> ```
> For SENSITIVE sources: `permanent_url` contains a description of the
> dataset category and methodology reference only, not the specific access URL.
> The actual access method is documented in internal (non-public) configuration.
> Simulation outputs that depend on SENSITIVE sources display a provenance note:
> "Source: [description]. Access credentials required — contact maintainers."

---

## CONFLICT Finding Documentation

### CONFLICT C-1: Opportunity Cost Assessment vs. Dual-Use Aggregation Risk

**Track 1 position (Investment and Capital Formation Agent, T1-F14):**
CODING_STANDARDS.md requires human cost ledger outputs but not opportunity cost
assessment. The absence of a parallel requirement for investment opportunity
analysis creates structural bias toward excessive caution. Standards should
require that scenario outputs include: latent investment opportunities visible
in the scenario, conditions that would make them accessible to private capital,
and the opportunity cost of policy pathways that foreclose them. This corrects
an asymmetry where harm is documented and opportunity is invisible.

**Track 2 position (Security Agent, T2-F12, intersecting):**
A standard requiring opportunity cost analysis would produce outputs identifying
which countries and sectors are most attractive for investment. A user comparing
these outputs across multiple country runs reconstructs a cross-country
comparative attractiveness ranking. For the Financial Warfare Module's scenarios
(which model currency attack vulnerability, sanctions exposure, capital flow
reversibility), "investment attractiveness" and "exploitable financial vulnerability"
are not always distinguishable in the outputs. A standard requiring opportunity
cost documentation for scenarios involving financial warfare analysis would
directly undermine the dual-use protection framework.

**Specific contradiction:**
Track 1 wants a standard requiring opportunity cost assessment.
Track 2 identifies that the same standard, applied to financial warfare scenarios,
creates the comparative vulnerability ranking that `POLICY.md` says will not be built.

**This is a genuine conflict requiring Engineering Lead disposition.** The council
does not resolve it. Options visible to the council:
1. Accept Track 1 as written — opportunity cost required for all scenarios, accept
   the dual-use risk
2. Accept Track 2 as written — no opportunity cost standard, accept the bias toward
   excessive caution
3. Third path: scope the opportunity cost requirement to development scenarios only
   (explicitly excluding Financial Warfare Module scenarios), with the scoping
   documented in POLICY.md

The Engineering Lead must choose and document the rationale.

---

## Standards Amendment Inventory

### Immediate — Implementable after CONFLICT finding disposition

| ID | Finding Source | Document | Amendment |
|---|---|---|---|
| SA-01 | T1-F1 / T2-F5 (CONVERGENT) | `CODING_STANDARDS.md` | Add MeasurementFramework event tagging rule and test requirement — see unified amendment above |
| SA-02 | T1-F17 / T2-F1 / T1-F20 (CONVERGENT) | `DATA_STANDARDS.md` | Split confidence_tier; specify tier-to-uncertainty bounds table — see unified amendment above |
| SA-03 | T1-F18 / T2-F4 (CONVERGENT) | `CODING_STANDARDS.md` | Add parameter calibration tier system (A–D) — see unified amendment above |
| SA-04 | T1-F2 / T2-F2 (CONVERGENT) | `DATA_STANDARDS.md`, `CODING_STANDARDS.md` | Human development indicator standard; HCL minimum effect size — see unified amendment above |
| SA-05 | T1-F8 / T2-F10 (CONVERGENT) | `DATA_STANDARDS.md` | Add `SourceClassification` enum and classification_level to SourceRegistration — see unified amendment above |
| SA-06 | T1-F3 / T1-F15 (COMPATIBLE) | `DATA_STANDARDS.md` | Add social legitimacy and implementation capacity as required state variable standards |
| SA-07 | T1-F4 (COMPATIBLE) | `DATA_STANDARDS.md` | Add governance indicator subsection: approved sources, methodology versioning, vintage dating, confidence tier |
| SA-17 | T1-F19 (COMPATIBLE) | `CODING_STANDARDS.md` | Add Monte Carlo standard: distribution assumptions, minimum sample size, output aggregation method |
| SA-18 | T2-F3 (COMPATIBLE) | `CODING_STANDARDS.md` | Add territorial position validation to data pipeline test requirements |
| SA-19 | T2-F6 (COMPATIBLE) | `CODING_STANDARDS.md` | Define float-to-Decimal conversion boundary at simulation attribute store explicitly |

### Near-Term

| ID | Finding Source | Document | Amendment |
|---|---|---|---|
| SA-08 | T1-F5 (COMPATIBLE) | `DATA_STANDARDS.md` | Add NATURAL_CAPITAL_STOCK, ECOSYSTEM_SERVICE_FLOW, ECOLOGICAL_FOOTPRINT to Dimension enum |
| SA-09 | T1-F6 (DEPENDENCY on SA-02) | `DATA_STANDARDS.md` | Add stock_or_flow metadata to Quantity type after SA-02 data model decisions |
| SA-10 | T1-F7 (COMPATIBLE) | `CONTRIBUTING.md` | Add ecological output requirement analogous to human cost ledger requirement |
| SA-11 | T1-F9 (COMPATIBLE) | `DATA_STANDARDS.md` | Add discount rate documentation standard: explicit rate + sensitivity analysis across three assumptions |
| SA-12 | T1-F10 (COMPATIBLE) | `POLICY.md` | Add minimum simulation horizon guidance for intergenerational effects |
| SA-13 | T1-F13 (COMPATIBLE) | `DATA_STANDARDS.md` | Add investment climate variable standards |
| SA-14 | T1-F16 (DEPENDENCY on SA-06) | `CODING_STANDARDS.md` | Add policy efficacy modulation standard after SA-06 is in place |
| SA-15 | T2-F7 (COMPATIBLE) | `DATA_STANDARDS.md` | Specify canonical representation for dimensionless derived quantities |
| SA-16 | T2-F9 (COMPATIBLE) | `CODING_STANDARDS.md` | Add ControlInput taxonomy completeness criterion |
| SA-17 | T2-F11 (COMPATIBLE) | `POLICY.md` | Add deployment jurisdiction considerations for territorial positions |
| SA-18 | T2-F12 (COMPATIBLE) | `POLICY.md` | Add aggregation risk guidance to dual-use section |

### Long-Term

| ID | Finding Source | Document | Amendment |
|---|---|---|---|
| SA-19 | T1-F11 (COMPATIBLE) | `DATA_STANDARDS.md` | Add social capital and community resilience measurement standards |
| SA-20 | T1-F12 (COMPATIBLE) | `CONTRIBUTING.md` | Add community-level representation requirement |

### Pending Engineering Lead Disposition (CONFLICT)

| ID | Conflict | Decision Required |
|---|---|---|
| C-1 | Opportunity cost assessment requirement vs. dual-use aggregation risk (T1-F14) | Engineering Lead must choose: accept Track 1, accept Track 2, or scope opportunity cost to development scenarios only |

---

## Recommended GitHub Issues

Issues below have been created for all COMPATIBLE and CONVERGENT immediate
findings. CONFLICT C-1 is not issued — awaiting Engineering Lead Phase 4 disposition.

### Immediate Issues Created

| Issue | Finding | SA ID |
|---|---|---|
| #42 | MeasurementFramework event tagging rule (CONVERGENT T1-F1/T2-F5) | SA-01 |
| #43 | Tier-to-uncertainty formula and confidence_tier split (CONVERGENT T1-F17/T2-F1/T1-F20) | SA-02 |
| #44 | Parameter calibration tier system (CONVERGENT T1-F18/T2-F4) | SA-03 |
| #45 | Human development indicator standards and HCL effect size (CONVERGENT T1-F2/T2-F2) | SA-04 |
| #46 | SourceRegistration classification level for sensitive datasets (CONVERGENT T1-F8/T2-F10) | SA-05 |
| #47 | Social legitimacy and political feasibility as required state variables (COMPATIBLE T1-F3/T1-F15) | SA-06 |
| #48 | Governance indicator standards: sources, versioning, vintage dating (COMPATIBLE T1-F4) | SA-07 |
| #49 | Monte Carlo standard: distribution assumptions and minimum sample size (COMPATIBLE T1-F19) | SA-17 |
| #50 | Territorial position validation in data pipeline tests (COMPATIBLE T2-F3) | SA-18 |
| #51 | Define float-to-Decimal boundary at simulation attribute store (COMPATIBLE T2-F6) | SA-19 |
