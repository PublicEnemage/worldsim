# Scenario Specification: USA Tariff Escalation 2025

**Status:** REVIEWED
**Created:** 2026-04-16
**Last updated:** 2026-04-16
**Specification author:** Architect Agent

---

## Classification

**Complexity:** Medium
**Scenario type:** Trade shock

**Primary modules required:**
- [ ] Macroeconomic Module *(not yet built — see limitations)*
- [x] Event propagation engine (ADR-001) *(available)*
- [x] Input Orchestration Layer (ADR-002) *(available)*
- [ ] Trade and Currency Module *(not yet built — see limitations)*

**Modules not yet built that this scenario would benefit from:**
- Trade and Currency Module: needed for dynamic trade flow rebalancing,
  exchange rate pass-through, and bilateral trade weight updating
- Macroeconomic Module: needed for GDP multiplier effects, consumption
  function, and investment response to uncertainty

**Current capability constraint:** This scenario models the first-round
propagation of a trade tariff shock through the static relationship graph.
It can show which countries are most exposed by their network position but
cannot model the rebalancing, substitution, or multiplier dynamics that
would follow in a full trade model.

---

## Historical Grounding

**Primary precedent cases:**

1. **Smoot-Hawley Tariff Act, 1930 (USA)** — Broad tariff increases on over
   20,000 imported goods. Triggered retaliatory tariffs from 25+ trading
   partners within months. US imports fell 66%, exports fell 61% between
   1929 and 1933. Contribution to the severity of the Great Depression is
   contested but widely regarded as having worsened the downturn.
   Key difference: 1930 global trade network was less integrated; currency
   was on gold standard with different transmission mechanism.

2. **US-China Trade War, 2018-2019** — Section 301 tariffs beginning at 25%
   on $34bn of Chinese goods, escalating to cover ~$550bn by end of 2019.
   Chinese GDP growth slowed from 6.8% (2017) to 6.0% (2019). US agricultural
   exporters sustained significant losses. Trade diversion toward Vietnam,
   Mexico, and other ASEAN economies was documented. Smoot-Hawley-scale
   retaliation did not materialise; both sides negotiated Phase One deal
   in January 2020.
   Key similarity: bilateral tariff escalation with documented trade diversion.
   Key difference: US-China economies are far more integrated into global
   value chains in 2025 than bilateral trade flows alone suggest; tariffs
   on goods now affect services and technology supply chains in ways Smoot-
   Hawley did not.

3. **US Tariff Escalation 2025** — Beginning April 2025, the US administration
   announced a broad tariff regime: 10% baseline tariff on most countries,
   25% on Canada and Mexico, and tariffs up to 145% on Chinese goods, with
   90-day pauses and periodic escalation/de-escalation. This scenario draws
   directly on these conditions as initial context and projects forward.

**Failure mode classification:** Coffin Corner — the tariff escalation
creates converging constraints on multiple economies simultaneously. China
faces export demand contraction while managing domestic stimulus constraints.
Mexico and Canada face USMCA relationship uncertainty simultaneous with tariff
exposure. Countries with high trade openness and limited fiscal space have
few degrees of freedom remaining.

---

## Initial Conditions

All values from IMF World Economic Outlook October 2024 release unless noted.
Trade openness from World Bank WDI 2024 release. Political stability from
World Bank Worldwide Governance Indicators 2023 release.
All accessed 2026-04-16.

### Entity: USA — United States of America

| Attribute | Value | Source |
|---|---|---|
| gdp_growth | 0.028 | IMF WEO Oct 2024 |
| debt_gdp_ratio | 1.22 | IMF WEO Oct 2024 (gross general government debt) |
| trade_openness | 0.27 | World Bank WDI 2024 (exports + imports as % GDP) |
| political_stability | 0.65 | World Bank WGI 2023 (percentile rank, normalised 0-1) |

### Entity: CHN — China

| Attribute | Value | Source |
|---|---|---|
| gdp_growth | 0.049 | IMF WEO Oct 2024 |
| debt_gdp_ratio | 0.83 | IMF WEO Oct 2024 |
| trade_openness | 0.37 | World Bank WDI 2024 |
| political_stability | 0.40 | World Bank WGI 2023 |

### Entity: DEU — Germany (proxying EU core)

| Attribute | Value | Source |
|---|---|---|
| gdp_growth | 0.001 | IMF WEO Oct 2024 |
| debt_gdp_ratio | 0.63 | IMF WEO Oct 2024 |
| trade_openness | 0.89 | World Bank WDI 2024 |
| political_stability | 0.80 | World Bank WGI 2023 |

### Entity: MEX — Mexico

| Attribute | Value | Source |
|---|---|---|
| gdp_growth | 0.015 | IMF WEO Oct 2024 |
| debt_gdp_ratio | 0.54 | IMF WEO Oct 2024 |
| trade_openness | 0.78 | World Bank WDI 2024 |
| political_stability | 0.30 | World Bank WGI 2023 |

### Entity: CAN — Canada

| Attribute | Value | Source |
|---|---|---|
| gdp_growth | 0.012 | IMF WEO Oct 2024 |
| debt_gdp_ratio | 1.07 | IMF WEO Oct 2024 |
| trade_openness | 0.66 | World Bank WDI 2024 |
| political_stability | 0.90 | World Bank WGI 2023 |

### Entity: JPN — Japan

| Attribute | Value | Source |
|---|---|---|
| gdp_growth | 0.009 | IMF WEO Oct 2024 |
| debt_gdp_ratio | 2.53 | IMF WEO Oct 2024 |
| trade_openness | 0.36 | World Bank WDI 2024 |
| political_stability | 0.80 | World Bank WGI 2023 |

### Entity: GBR — United Kingdom

| Attribute | Value | Source |
|---|---|---|
| gdp_growth | 0.009 | IMF WEO Oct 2024 |
| debt_gdp_ratio | 1.04 | IMF WEO Oct 2024 |
| trade_openness | 0.58 | World Bank WDI 2024 |
| political_stability | 0.70 | World Bank WGI 2023 |

### Entity: VNM — Vietnam

| Attribute | Value | Source |
|---|---|---|
| gdp_growth | 0.050 | IMF WEO Oct 2024 |
| debt_gdp_ratio | 0.37 | IMF WEO Oct 2024 |
| trade_openness | 1.93 | World Bank WDI 2024 (highly trade-dependent economy) |
| political_stability | 0.40 | World Bank WGI 2023 |

### Entity: BRA — Brazil

| Attribute | Value | Source |
|---|---|---|
| gdp_growth | 0.029 | IMF WEO Oct 2024 |
| debt_gdp_ratio | 0.87 | IMF WEO Oct 2024 |
| trade_openness | 0.33 | World Bank WDI 2024 |
| political_stability | 0.30 | World Bank WGI 2023 |

### Entity: IND — India

| Attribute | Value | Source |
|---|---|---|
| gdp_growth | 0.070 | IMF WEO Oct 2024 |
| debt_gdp_ratio | 0.84 | IMF WEO Oct 2024 |
| trade_openness | 0.46 | World Bank WDI 2024 |
| political_stability | 0.40 | World Bank WGI 2023 |

### Relationships

Trade relationship weights are computed as bilateral trade value as a fraction
of the source entity's total trade (imports + exports), using UN Comtrade 2023
data and OECD Trade in Value Added (TiVA) 2023.

**USA outbound trade relationships:**

| Source | Target | Type | Weight | Basis |
|---|---|---|---|---|
| USA | CHN | trade | 0.14 | 14% of US total trade, UN Comtrade 2023 |
| USA | DEU | trade | 0.06 | 6% of US total trade (Germany as EU proxy) |
| USA | MEX | trade | 0.16 | 16% of US total trade, USMCA partner |
| USA | CAN | trade | 0.15 | 15% of US total trade, USMCA partner |
| USA | JPN | trade | 0.05 | 5% of US total trade |
| USA | GBR | trade | 0.04 | 4% of US total trade |
| USA | VNM | trade | 0.03 | 3% of US total trade |
| USA | BRA | trade | 0.02 | 2% of US total trade |
| USA | IND | trade | 0.02 | 2% of US total trade |

**CHN outbound trade relationships:**

| Source | Target | Type | Weight | Basis |
|---|---|---|---|---|
| CHN | USA | trade | 0.15 | 15% of China's total trade |
| CHN | DEU | trade | 0.08 | 8% of China's total trade |
| CHN | JPN | trade | 0.06 | 6% of China's total trade |
| CHN | VNM | trade | 0.10 | 10% of China's total trade (GVC integration) |
| CHN | BRA | trade | 0.03 | 3% of China's total trade |

---

## Injected Events (ControlInput Specifications)

### Input 1: US Broad Tariff Imposition

```
Input type: TradePolicyInput
Step index: 1 (fires at year 1 of the simulation)
actor_id: usa_trade_representative
actor_role: president
target_entity: CHN
source_entity: USA
instrument: TARIFF_RATE
value: Decimal("0.01")
  Note: Value represents the GDP growth impact per unit of trade weight,
  not the tariff rate itself. A 0.01 delta propagated through USA's trade
  edges represents a -1% GDP growth shock to the US economy from tariff
  costs and uncertainty, which then attenuates through trading partners.
  This is a Milestone 1 simplification — the Trade Module will model this
  endogenously with proper pass-through coefficients.
affected_sector: goods
retaliation_modeled: False
  Note: Chinese retaliation not modelled in Milestone 1. A separate input
  could model this; excluded here to demonstrate the unilateral shock first.
propagation_rules:
  - relationship_type: trade
    attenuation_factor: 0.6
    max_hops: 2
    Note: 0.6 attenuation reflects rough approximation of trade spillover
    from 2018-2019 US-China trade war literature (IMF WP/19/14: global GDP
    impact ~0.5% from full escalation). Calibration pending Trade Module.
justification: US administration announced broad tariff regime from
  April 2025; models the first-round global trade network shock.
```

---

## Expected Direction of Effects

**Economic theory basis:** Standard Heckscher-Ohlin and gravity model
predictions for tariff shocks. Trade barriers reduce trade volume, raise
consumer prices, redirect trade flows, and reduce aggregate welfare in
the imposing country as well as trading partners (though distribution of
gains/losses differs by factor endowment). The 2018-2019 trade war literature
(Amiti, Redding, Weinstein 2019; Fajgelbaum et al. 2020) documents that
US consumers and firms bore most of the tariff costs, not Chinese exporters.

**Dissenting view:** Mercantilist and strategic trade theory arguments hold
that tariffs can be welfare-improving if they induce terms-of-trade gains,
force technology transfer concessions, or protect infant industries. The
dissenting view in 2025 context is that tariff pressure forced supply chain
diversification away from Chinese dependency, which has long-run strategic
benefits not captured in short-run GDP accounting.

### Expected indicator movements (Year 1-2)

| Entity | Attribute | Expected direction | Confidence | Basis |
|---|---|---|---|---|
| USA | gdp_growth | Down | Medium | Tariff costs, uncertainty, reduced exports |
| CHN | gdp_growth | Down | High | Export demand contraction to largest market |
| MEX | gdp_growth | Down | High | USMCA disruption, strong trade link to USA |
| CAN | gdp_growth | Down | High | USMCA disruption, strong trade link to USA |
| DEU | gdp_growth | Down | Medium | Indirect through global demand contraction |
| VNM | gdp_growth | Ambiguous | Low | Trade diversion gain vs. US market demand loss |
| JPN | gdp_growth | Down | Medium | Indirect global demand and supply chain effects |
| BRA | gdp_growth | Ambiguous | Low | May gain from commodity demand diversion |
| IND | gdp_growth | Ambiguous | Low | May gain from supply chain diversification |

Note on ambiguous cases: Vietnam, Brazil, and India show ambiguous direction
because the current simulation's static relationship weights cannot model
trade diversion (a core mechanism of tariff shock adjustment). The Trade
Module will resolve this ambiguity. Current simulation will show them taking
attenuated hits, which understates the diversion gains they historically
receive.

---

## Domain Intelligence Council Review

### Development Economist

The tariff shock scenario activates several human development concerns that
GDP accounting will not capture.

The immediate impact falls hardest on workers in export-dependent sectors:
manufacturing workers in Mexico's maquiladora zones, agricultural workers
in regions dependent on US market access, and factory workers in Vietnam's
electronics assembly sector. These are predominantly young workers with few
alternative employment options in the short run.

In the medium run, the inflationary effect of US tariffs on imported consumer
goods raises the cost of living for US households in the bottom income
quintiles, who spend a higher fraction of income on imported goods (apparel,
electronics, household goods). The 2018-2019 trade war evidence (Jaravel and
Sager 2019) documents this regressive incidence clearly.

For China, a sustained export demand reduction exerts pressure on the
government's ability to maintain the urban employment levels and wage growth
that have been the primary mechanism of poverty reduction over the past 30
years. Capability deprivation risks are highest for workers in export
manufacturing provinces (Guangdong, Zhejiang, Jiangsu).

**Key concern:** The scenario's GDP growth impacts are likely underestimates
of the human development impacts, because the distributional incidence falls
hardest on low-income workers and households who are already in the lower
cohorts of the capability distribution.

### Political Economist

The political economy of this scenario is as important as the economics.

For the US: tariff protection is politically popular in the short run with
manufacturing workers who benefit from reduced import competition. The
political economy gains from visible employment protection outweigh the
diffuse costs to consumers who face higher prices. This creates a credibility
asymmetry: the US administration has political incentives to maintain tariffs
even when aggregate welfare analysis recommends removal.

For China: the political economy of response is constrained by the need to
maintain growth sufficient to sustain social stability. Aggressive retaliation
that would further slow growth is politically costly domestically. This
constrains the negotiating space — China cannot credibly threaten to escalate
if escalation hurts its own economy more than the US's.

For Mexico and Canada: USMCA renegotiation creates political economy pressure
for concessions that may not be economically optimal (immigration concessions,
energy policy) as the price of tariff exemptions. The political feasibility of
these concessions depends on domestic politics in each country.

**Key concern:** The simulation models the economic network but not the
political economy network. Countries with politically sensitive trade exposures
(Mexico's agricultural sectors, Canada's auto industry) face domestically
destabilising pressure that may produce responses not captured in any
economically rational model.

### Geopolitical and Security Analyst

This scenario is not primarily an economic event — it is a strategic one.

The US tariff escalation in 2025 is best understood as using economic
instruments to achieve strategic objectives: reducing dependency on Chinese
manufactured goods, forcing supply chain repatriation, pressuring China on
Taiwan and South China Sea commitments, and extracting concessions from
USMCA partners on migration and security cooperation. The tariff is the
instrument; the geopolitical objectives are the goals.

This matters for simulation interpretation because the US is optimising for
strategic outcomes, not aggregate economic welfare. A tariff that costs the
US $200bn in consumer welfare but forces $500bn in supply chain relocation
out of China may be welfare-negative by conventional accounting and
strategically optimal by the administration's revealed preferences.

The scenario also activates the Financial Warfare Module's threat surface:
China holds approximately $800bn in US Treasury securities. The credibility
of Chinese threats to liquidate this holding (which would raise US borrowing
costs) affects the US administration's calculus and is entirely absent from
the current simulation's capabilities.

**Key concern:** The economic model treats trade policy as welfare optimisation.
The actual decision environment treats it as strategic competition. The
simulation's output will be directionally wrong for any entity whose objective
function includes strategic considerations that dominate economic welfare
optimisation.

---

## Validation Approach

**Validation data sources:**
- IMF World Economic Outlook (semi-annual releases, 2025-2027)
- World Bank Global Economic Prospects
- OECD Economic Outlook
- WTO World Trade Report

**Fidelity thresholds:**

| Variable | Expected direction | Fidelity threshold | Data source |
|---|---|---|---|
| CHN gdp_growth (Year 1) | Down | Declines ≥ 0.3pp vs baseline | IMF WEO 2026 |
| USA gdp_growth (Year 1) | Down | Declines ≥ 0.2pp vs baseline | IMF WEO 2026 |
| MEX gdp_growth (Year 1) | Down | Declines ≥ 0.4pp vs baseline | IMF WEO 2026 |
| CAN gdp_growth (Year 1) | Down | Declines ≥ 0.3pp vs baseline | IMF WEO 2026 |

Note: "Baseline" is the IMF WEO October 2024 forecast, which was made before
the full tariff escalation was known. The delta vs. forecast is the relevant
comparison.

**Failure criteria:** The simulation has failed this scenario if the primary
affected entity (CHN) shows GDP growth increasing in Year 1 relative to
its initial condition, OR if the propagation ordering is inverted (CHN less
affected than a low-weight partner like GBR).

---

## Known Model Limitations For This Scenario

| Limitation | Impact on results | Future module |
|---|---|---|
| No Trade and Currency Module | Static relationship weights; no trade diversion, exchange rate pass-through, or J-curve dynamics | Trade Module (Milestone X) |
| No Macroeconomic Module | No fiscal/monetary multiplier; no investment uncertainty channel; no consumption function | Macroeconomic Module (Milestone X) |
| No retaliation modelling in current input | Chinese and EU retaliation excluded; real shock is bilateral | Can be added as additional TradePolicyInput now |
| No endogenous relationship updating | Trade weights stay fixed regardless of tariff effects | Trade Module (Milestone X) |
| Float attributes, not Decimal | Monetary arithmetic precision is limited until CF-001-F01 is resolved | Pending Engineering Lead decision on DATA_STANDARDS.md amendment (GitHub Issue #9) |

**Overall confidence in current results:**

The current simulation can demonstrate that countries with higher trade
weights to the USA take larger first-round hits, and that the network
structure amplifies the shock to more connected economies. These are
directionally correct structural conclusions.

The simulation CANNOT currently produce reliable magnitudes, model
adjustment dynamics, or capture the trade diversion that would benefit
Vietnam, India, and other non-primary-tariff-targets. Do not use current
results to estimate economic impact in percentage points. Use them only
to understand the network exposure structure.

---

## Status History

| Date | Status | Notes |
|---|---|---|
| 2026-04-16 | PROPOSED | Initial specification |
| 2026-04-16 | REVIEWED | Council review complete (Development Economist, Political Economist, Geopolitical Analyst) |
