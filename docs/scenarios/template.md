# Scenario Specification: [SCENARIO NAME]

**Status:** PROPOSED | REVIEWED | ACTIVE | VALIDATED | ARCHIVED
**Created:** YYYY-MM-DD
**Last updated:** YYYY-MM-DD
**Specification author:** [name or agent role]

---

## Classification

**Complexity:** Low | Medium | High | Very High
**Scenario type:** Trade shock | Monetary crisis | Fiscal consolidation |
Sovereign debt restructuring | Geopolitical shock | Climate forcing |
Structural reform | Compound crisis

**Primary modules required:**
- [ ] Macroeconomic Module
- [ ] Trade and Currency Module
- [ ] Monetary System Module
- [ ] Capital Flow Module
- [ ] Geopolitical Module
- [ ] Climate Module
- [ ] Demographic and Health Module
- [ ] Financial Warfare Module
- [ ] Institutional Cognition Module

**Modules not yet built that this scenario would benefit from:**
List modules from CLAUDE.md that are not in the codebase but would improve
this scenario's fidelity. This is not a blocker — document it as a known
limitation (see section 8 below).

**Current capability constraint:** What the scenario CAN model given
current module capabilities (see `module-capability-registry.md`).

---

## Historical Grounding

**Primary precedent cases:**
The historical scenarios this specification draws from for expected direction
of effects, calibration, and validation approach. Be specific: not "currency
crises" but "Thailand 1997 baht devaluation" and "Mexico 1994 tequila crisis."

**Key similarities to precedent:**
What makes this scenario structurally similar to the precedent cases.

**Key differences from precedent:**
The important ways this scenario differs — why the precedents are informative
but not directly predictive.

**Failure mode classification:**
Which of the five aviation failure modes from CLAUDE.md this scenario tests:
Spin | Coffin Corner | Hypoxia | Backside of Power Curve | Get-There-Itis

---

## Initial Conditions

All attribute values require a data source citation in the format:
`[Dataset name], [Release/version], accessed [YYYY-MM-DD]`

Vintage dating requirement: only data published before the scenario's
start date may be used as seed data.

### Entity: [ISO 3166-1 alpha-3 code] — [Country Name]

| Attribute | Value | Source |
|---|---|---|
| gdp_growth | 0.XXX | IMF WEO October 2024, accessed 2026-04-16 |
| debt_gdp_ratio | X.XX | IMF WEO October 2024, accessed 2026-04-16 |
| trade_openness | X.XX | World Bank WDI 2024 release, accessed 2026-04-16 |
| political_stability | X.XX | World Bank WGI 2023, accessed 2026-04-16 |
| [other attributes] | | |

### Entity: [ISO3] — [Country Name]

[Repeat for each entity in the scenario]

### Relationships

| Source | Target | Type | Weight | Basis |
|---|---|---|---|---|
| XXX | YYY | trade | 0.XX | [data source and calculation method] |
| XXX | ZZZ | debt | 0.XX | [data source and calculation method] |

Relationship weights should be grounded in data where possible. Document
the source and calculation method (e.g. "bilateral trade as fraction of
source entity's total trade, OECD TiVA 2023").

---

## Injected Events (ControlInput Specifications)

List all exogenous inputs to be injected, in chronological order. Use the
ControlInput types defined in ADR-002.

### Input 1: [Descriptive Name]

```
Input type: TradePolicyInput | MonetaryPolicyInput | FiscalPolicyInput |
            EmergencyPolicyInput | StructuralPolicyInput
Step index: N (fires at the transition from step N-1 to step N)
actor_id: [actor identifier]
actor_role: [role, e.g. 'president', 'finance_minister', 'central_bank']
target_entity: [ISO3]
source_entity: [ISO3] (TradePolicyInput only)
instrument: [instrument enum value]
value: [magnitude, with units]
affected_sector: [sector] (where applicable)
retaliation_modeled: True | False (TradePolicyInput only)
propagation_rules:
  - relationship_type: [type]
    attenuation_factor: [0.0–1.0]
    max_hops: [N]
justification: [one sentence on why this input is in the scenario]
```

### Input N: [Descriptive Name]

[Repeat for each input]

---

## Expected Direction of Effects

This section documents, before any simulation runs, what direction we
expect key indicators to move and why. Direction only — not magnitude.
The simulation is a structured reasoning tool, not a prediction engine.

**Economic theory basis:** Why these directional predictions follow from
established economic theory (cite relevant theory or empirical literature).

**Dissenting view:** What alternative theoretical frameworks predict, and
why reasonable analysts might expect different directions.

### Expected indicator movements

| Entity | Attribute | Expected direction | Confidence | Basis |
|---|---|---|---|---|
| XXX | gdp_growth | Down | High | Demand contraction from tariffs |
| YYY | trade_openness | Down | High | Direct effect of trade barriers |
| ZZZ | political_stability | Down | Medium | Historical pattern in trade wars |

Confidence levels: High (well-established theory + precedent) | Medium
(contested theory or weak precedent) | Low (speculative).

---

## Domain Intelligence Council Review

At least three council agents must complete their review sections before
this scenario moves from PROPOSED to REVIEWED. Write these sections before
the simulation runs — not after. Council review sections written after
seeing simulation output are not independent analysis.

### Development Economist

*What does the human development framework reveal about this scenario?
What populations are most exposed? What capability dimensions are most at
risk? What historical evidence about similar situations should inform our
interpretation of the simulation's output?*

[To be completed — activate with: `Development Economist: SCENARIO — [scenario name]`]

**Key concern:** [One sentence on the single most important human development
concern for this scenario]

### Political Economist

*What political economy constraints shape what is actually achievable in
this scenario? Who gains and who loses in ways that affect the political
sustainability of the policy response? What does the historical record of
political responses to similar situations suggest?*

[To be completed — activate with: `Political Economist: SCENARIO — [scenario name]`]

**Key concern:** [One sentence on the single most important political
economy concern]

### Ecological Economist

*What natural capital flows are implicated in this scenario? Which populations
bear ecological costs that will not appear in GDP accounting? What planetary
boundary considerations are relevant?*

[To be completed — activate with: `Ecological Economist: SCENARIO — [scenario name]`]

**Key concern:** [One sentence on the single most important ecological concern]

### Geopolitical and Security Analyst

*What coercive dynamics shape this scenario? Who has leverage over whom?
How does the geopolitical context constrain the available policy responses?
What does the financial warfare literature suggest about vulnerability exposure?*

[To be completed — activate with: `Geopolitical Analyst: SCENARIO — [scenario name]`]

**Key concern:** [One sentence on the single most important geopolitical concern]

### Intergenerational Equity Advocate

*What decisions made in this scenario will bind future generations? What
irreversibilities are at stake? What is the intergenerational distribution
of costs and benefits?*

[To be completed — activate with: `Intergenerational Advocate: SCENARIO — [scenario name]`]

**Key concern:** [One sentence on the single most important intergenerational
equity concern]

### Community and Cultural Resilience Agent

*What communities are most exposed to social fabric disruption in this
scenario? What traditional practices or ways of life are at risk? What
does the anthropological record of similar disruptions suggest?*

[To be completed — activate with: `Community Resilience: SCENARIO — [scenario name]`]

**Key concern:** [One sentence on the single most important community
resilience concern]

---

## Validation Approach

How we evaluate whether the simulation got this scenario directionally right.
This section is completed before running the simulation — before we know the
output — so that the validation criteria cannot be reverse-engineered from
a favourable result.

**Validation data sources:** Specific datasets and time series against which
simulation output will be compared. Cite fully.

**Fidelity thresholds:** Specific quantitative criteria. Not "GDP should go
down" but "GDP growth rate should decline by at least 0.5 percentage points
within two years for the primary affected entity."

| Variable | Expected direction | Fidelity threshold | Data source |
|---|---|---|---|
| [variable] | [direction] | [±X.X pp within Y years] | [source] |

**Failure criteria:** Conditions under which we conclude the simulation
got this scenario wrong and investigation is required.

---

## Known Model Limitations For This Scenario

Explicit documentation of what the current simulation cannot model that
would be important for this scenario. Every limitation listed here is a
known blindspot — visible to users of this scenario's outputs.

| Limitation | Impact on results | Future module that addresses this |
|---|---|---|
| No fiscal module | Cannot model direct fiscal multiplier effects | Macroeconomic Module (Milestone X) |
| No trade flow module | Relationship weights are static | Trade and Currency Module (Milestone X) |
| [other limitation] | | |

**Overall confidence in current results:** Given the above limitations,
what should users understand about the reliability of this scenario's
current output? What conclusions are safe to draw? What conclusions
should not be drawn until the listed modules are available?

---

## Status History

| Date | Status | Notes |
|---|---|---|
| YYYY-MM-DD | PROPOSED | Initial specification |
