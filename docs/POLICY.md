# WorldSim Policy Transparency Statement

This document is written for a non-technical audience: finance ministers,
civil society organizations, journalists, researchers, and governments deciding
whether to trust this tool. It states the policy choices WorldSim has made,
why those choices were made, and how any of them can be challenged.

WorldSim makes policy choices. Every tool that analyzes sovereign economic
data makes policy choices — about which countries are recognized, which exchange
rates are official, which base year is used for comparison, which limitations
are disclosed and which are buried. Most tools make these choices without
declaring them. WorldSim declares them.

Transparency is a trust mechanism, not a bureaucratic obligation. A tool that
declares its positions and their rationale can be audited, challenged, and
improved. A tool that hides its positions cannot. The finance minister across
from an IMF negotiating team deserves to know what assumptions are built into
the analysis they are relying on.

---

## Governing Philosophy

WorldSim is built on the premise that analytical capability is currently
distributed asymmetrically. The most sophisticated sovereign debt analysis
tools are expensive and proprietary, accessible to the actors who are least
likely to be harmed by bad sovereign decisions and least likely to bear the
human cost of those decisions.

WorldSim exists to correct this asymmetry in one direction only. It is a
tool for governments and vulnerable actors to build situational awareness
and defensive capability. It is not designed to help anyone identify
exploitable vulnerabilities in adversaries, execute financial attacks, or
amplify existing power asymmetries.

The choices documented in this policy statement are made against this
governing principle. Where a choice could serve either defensive or offensive
purposes, WorldSim makes the choice that maximizes defensive utility while
minimizing attack surface identification capability.

---

## Territorial and Nomenclature Positions

These are the positions WorldSim takes on contested territorial and political
designations. We follow internationally recognized standards bodies and present
disputed cases transparently without taking political positions that are not
ours to take.

### The Framework

Country identifiers throughout WorldSim use ISO 3166-1 alpha-3 codes. Where
ISO 3166-1 is silent or ambiguous, we follow the IMF country list for economic
entities and UN Secretariat terminology for political designations. This is
our primary standard. We document all deviations from it.

For disputed territories, we store de facto administrative boundaries
separately from de jure claimed boundaries, both labeled explicitly, and
display a dispute note to users. We do not silently assert any claimant's
position.

### Specific Positions

**Taiwan (TWN)**

Internal code: TWN (ISO 3166-1 alpha-3).
Display: "Taiwan."

Taiwan has a separate, functioning government with independent economic
policy, its own currency, and its own economic statistics. For simulation
purposes, it is modeled as a separate economic entity. Economic data comes
from the Asian Development Bank, IMF Article IV consultations, and Taiwan's
Directorate-General of Budget, Accounting and Statistics.

This does not constitute a position on sovereignty. We are not equipped to
adjudicate a dispute that the United Nations and most governments navigate
with deliberate ambiguity. We model Taiwan as a separate economic entity
because that is what the economic data reflects, and because a user analyzing
Taiwanese fiscal policy needs Taiwan's data, not data merged with the PRC's.

Users will see the note: *"Taiwan's international status is disputed. WorldSim
presents it as a separate economic entity for simulation purposes. This does
not constitute a position on sovereignty."*

**Palestine (PSE)**

Internal code: PSE (ISO 3166-1 alpha-3: Palestinian Territory, Occupied).
Display: "State of Palestine" (the entity's self-designation as a UN observer
state).

Economic data comes from the Palestinian Central Bureau of Statistics, the
World Bank, and the IMF. The administrative complexity of West Bank and
Gaza Strip governance is noted in scenario metadata where simulation-relevant.

**Kosovo (XKX)**

Internal code: XKX (user-assigned code; Kosovo has no ISO 3166-1 assignment).
Display: "Kosovo."

Kosovo has been an IMF member since 2009 and a World Bank member since 2009.
Its fiscal and monetary policy is independent. We model it as a separate
economic entity because that is what its institutional membership and
independent economic policy reflect. Recognition status (recognized by
approximately 100 states, not recognized by Russia, China, Serbia, and five
EU members) is noted in scenario metadata for geopolitical scenarios.

**Western Sahara (ESH)**

Internal code: ESH (ISO 3166-1 alpha-3).
Display: "Western Sahara."

The UN lists Western Sahara as a Non-Self-Governing Territory. The majority
of the territory is administered by Morocco; eastern territory is controlled
by the Sahrawi Arab Democratic Republic. Users will see this administrative
note. We do not use "Morocco" for Western Sahara data or present Moroccan
claims as settled.

**Crimea**

Crimea is handled at the Ukraine (UKR) national level, with the administrative
change of 2014 noted in entity metadata. We do not create a separate Crimea
entity. Creating a separate entity would implicitly endorse the annexation
that is not recognized under international law by the UN General Assembly
majority position (UNGA Resolution ES-11/1, 2022, and prior resolutions).

Users analyzing subnational Ukrainian scenarios will see: *"Crimea's
administrative status changed in 2014. WorldSim models it within Ukraine's
national boundary consistent with UNGA majority position. Actual conditions
on the ground in Crimea since 2014 are modeled using available data with
appropriate uncertainty."*

**The general framework for future cases**

New contested territory cases will be handled using the same framework:
follow ISO 3166-1 where it applies, follow IMF/UN Secretariat where it does
not, store de facto and de jure separately, display a dispute note, and never
silently assert one claimant's terminology.

---

## Data Source Selection Philosophy

### Why International Bodies Are Prioritized

Primary data comes from the World Bank, IMF, UN agencies, BIS, and national
statistical offices. These are prioritized because:

1. **Methodology transparency.** These institutions publish their methodology.
   We can inspect what they measure, how they measure it, and what they
   exclude. Most proprietary data sources do not.

2. **Vintage retrieval.** Backtesting requires data that was available at the
   scenario's start date — not revised data published years later. World Bank,
   IMF WEO archive, and FRED support historical vintage retrieval. This is
   a technical constraint that limits which sources can be used for
   backtesting.

3. **Consistent coverage.** Cross-country analysis requires data collected
   using compatible methodologies. The World Bank's consistent national
   accounts approach makes Bolivia's GDP directly comparable to Germany's
   in a way that ad hoc national data often is not.

### How Unreliable Official Statistics Are Handled

Some governments publish official statistics that are widely considered
unreliable — either due to measurement limitations or political interference
with statistical agencies. WorldSim's response is:

1. **Flag the reliability concern explicitly.** A GDP figure for a country
   where official statistics are considered unreliable carries a lower
   confidence tier and a note.

2. **Use alternative sources where they exist.** For countries with known
   official statistics reliability issues, we supplement with research
   institution estimates and note the divergence.

3. **Widen uncertainty bands.** Simulation outputs that rely heavily on
   lower-quality data display wider confidence intervals. The relationship
   between data quality tier and output uncertainty is quantified, not
   qualitative.

4. **Never hide the limitation.** If the simulation's output for a specific
   country or period is based on data we know to be questionable, the user
   sees this. No false precision.

### The Tier System

WorldSim classifies data on a five-tier quality scale (detailed in
DATA_STANDARDS.md). What this means for you as a user:

- Tier 1 (primary official statistics from international bodies): full weight
  in simulation, narrow uncertainty bands
- Tier 3 (research estimates with published methodology): weighted by stated
  uncertainty, flagged in output
- Tier 5 (gap-filled values): excluded from high-stakes outputs unless there
  is no alternative; proportion disclosed when used

The confidence tier of key inputs is shown alongside simulation outputs.
An output that looks precise but is based on Tier 4 and Tier 5 inputs will
show wide uncertainty bands, not a confident point estimate.

---

## Economic Methodology Positions

### Why Constant 2015 USD

All monetary values inside the simulation are stored in constant 2015 USD.
The World Bank's International Comparison Program (ICP) uses 2015 as its
base year for purchasing power parity calculations. This choice aligns
WorldSim with the dataset that enables the most comprehensive cross-country
economic comparisons available.

"Constant" means we remove the effect of inflation. Comparing Ghana's GDP
in 2005 and 2020 in nominal terms conflates real economic growth with
inflation — they look similar but reflect very different things. Constant
prices enable real comparisons.

"2015" is not a statement that 2015 is economically significant. It is a
choice to align with the World Bank's base year for PPP comparability.
As the World Bank updates its ICP base year, WorldSim's canonical base year
will be reviewed.

### Why PPP for Human Cost, Market Rates for Financial Flows

These two concepts measure different things and must not be confused:

**Purchasing Power Parity (PPP) rates** convert currencies so that a given
amount buys the same basket of goods in each country. This is the right
concept for measuring living standards, poverty, and human welfare — what
can people actually buy with their income?

**Market exchange rates** are the rates at which currencies actually trade.
This is the right concept for financial flows — debt service payments, trade
balances, reserve adequacy — because these transactions occur at market rates.

Using PPP rates for debt sustainability analysis would understate the burden
of foreign-currency-denominated debt on countries with weak currencies. Using
market rates for poverty measurement would make a poor country with a weak
currency appear poorer than its residents' actual purchasing power.

WorldSim's human cost ledger uses PPP. WorldSim's financial flow outputs use
market exchange rates. Outputs that mix both concepts explicitly document
which applies to which component.

### What the World Bank ICP Reference Means for Cross-Country Comparability

The ICP produces PPP conversion factors by measuring prices of comparable
goods across countries. This enables comparison — is Bolivia's public health
spending adequate relative to similar countries? — that nominal dollar
comparisons cannot provide.

The ICP methodology has known limitations:
- Coverage is uneven; some small and conflict-affected states have poor coverage
- The basket of goods may not reflect local consumption patterns
- Revisions between ICP rounds can be substantial (2005 to 2011 revisions
  significantly changed estimates for China and India)

WorldSim users analyzing countries with poor ICP coverage will see wider
uncertainty bands and data limitation notes.

---

## What the Simulation Claims and Does Not Claim

### What It Is

WorldSim is a **structured reasoning tool**. It is designed to help
decision-makers think through the consequences of different policy choices
across a distribution of plausible futures.

When WorldSim shows that an IMF program has a 40% probability of leading
to a Coffin Corner configuration within three years under a pessimistic
commodity price scenario, this means: given the model's assumptions and the
historical relationships it has been calibrated against, the simulation
reached this configuration in approximately 40 out of 100 runs under those
conditions.

It does not mean: this will happen with 40% probability.

### What It Is Not

WorldSim is not a prediction engine. It does not forecast. It does not output
facts about the future. It outputs distributions over scenarios conditional
on assumptions.

**Do not use WorldSim outputs as the sole basis for sovereign decisions.**
Use them as one structured input among several, including human judgment,
local knowledge, and expert consultation. The tool is a flight simulator —
it builds judgment and tests decisions in a structured environment. It is not
the aircraft.

**Do not use WorldSim for scenarios with malicious intent.** The dual-use
position section below addresses this explicitly.

### What Confidence Intervals Mean

Every simulation output includes uncertainty bounds. These reflect:
- The range of outcomes across Monte Carlo runs under the specified scenario
- The uncertainty introduced by lower-quality input data (Tier 3-5 inputs
  widen the bands)
- The documented sensitivity of outcomes to key assumptions

Narrow confidence intervals mean the model converges across runs under
these conditions. Wide confidence intervals mean outcomes are sensitive
to the assumptions — which is important information, not a weakness.

A scenario where all outcomes are bad regardless of assumption variation
is important information for a decision-maker. So is a scenario where the
outcome distribution is strongly bimodal — good outcomes and bad outcomes
with few middle cases — because that tells you something about the nature
of the risk.

---

## Human Cost Ledger Methodology

### What We Measure

The human cost ledger reports simulation outcomes simultaneously in four
accounting frameworks, none of which converts to another:

1. **Financial** — standard macroeconomic indicators: GDP, debt ratios,
   balance of payments, reserve adequacy
2. **Human Development** — Sen's capability approach dimensions: health,
   education, income adequacy, food security, physical security
3. **Ecological** — resource depletion, natural capital degradation,
   climate exposure
4. **Governance** — institutional quality, political freedom, rule of law

A country that is financially stable but in a human development crisis
looks fine under financial metrics alone. WorldSim shows all four dimensions
simultaneously. Collapse in any single dimension triggers an alert regardless
of performance in others.

### What We Do Not Measure

The human cost ledger is incomplete in ways we are documenting honestly:

- **Intra-household distribution** — we model income quintiles but not
  within-household distributional effects, where gender-based inequalities
  are particularly consequential
- **Non-monetary dimensions of capability** — time poverty, social exclusion,
  and political voice are represented through proxy indicators, not directly
  measured
- **Intergenerational effects** — the ledger models cohort-level impacts but
  the full intergenerational consequences of decisions (education interruption,
  stunting, institutional damage) extend beyond the simulation horizon

### The Most Significant Known Limitation

The human cost model is built on correlational relationships calibrated
against historical data. It captures the consequences that historical cases
show were typically associated with specific economic configurations. It
does not model novel causal pathways that have not appeared in the historical
record.

A genuinely unprecedented shock — a type of financial crisis or external
event without historical analog — will be modeled by extrapolation from the
nearest historical cases. The uncertainty bands in such cases should be wide.
If they are not, that is a calibration error.

---

## Backtesting Integrity Position

### What Validation Means

When we say a backtesting case "validates" the model, we mean: running the
simulation forward from the conditions that existed at the scenario start date,
injecting the known events that occurred, produces outputs within a specified
fidelity threshold of what the historical record shows actually happened.

This is meaningful but limited validation:
- It confirms the model captures the historical relationships that drove those
  specific outcomes
- It does not prove the model will be accurate for future scenarios that
  differ from historical experience
- It does not validate the model for countries, periods, or crisis types not
  yet covered by backtesting cases

### Known Cases of Good Model Performance

(To be documented as backtesting cases are added)

### Known Cases of Poor Model Performance

(To be documented honestly as backtesting cases are added)

We commit to documenting backtesting failures honestly and publicly. A model
that publishes only its successes is providing incomplete information. The
users who most need this tool — decision-makers in high-stakes environments —
are best served by knowing where the model is reliable and where it is not.

### Intellectual Honesty About Underperformance

When a backtesting case shows the model performed poorly, the WorldSim
response is:
1. Document the failure and its magnitude publicly
2. Investigate whether the cause is a missing variable, a misspecified
   relationship, or a genuinely unprecedented event
3. Improve the model where improvement is possible
4. Document the limitation explicitly where it is structural

We do not adjust fidelity thresholds to make failing cases pass. We do not
remove difficult backtesting cases from the suite because they show model
weaknesses.

---

## Declared Blindspots

These are domains where the WorldSim model is weakest. We document them
explicitly and visibly because users who do not know where the model fails
cannot apply appropriate judgment.

### Variables Known to Be Consequential But Not Yet Modeled

- **Political elite capture of adjustment burden** — IMF programs often
  distribute adjustment costs unequally; the model does not yet distinguish
  between austerity that falls on social spending versus elite wealth
- **Shadow banking and informal credit markets** — consequential in many
  developing economies; poorly captured by formal credit statistics
- **Climate tipping points** — the model uses IPCC scenario projections but
  does not model nonlinear climate tipping point dynamics
- **Diaspora remittance flows** — significant for many small states; included
  in aggregate current account but not modeled dynamically in response to
  shocks
- **Social capital and trust** — consequential for crisis recovery but
  extremely difficult to measure and model

### The Structural Limitation Most Likely to Cause a Wrong Output

**The model learns from history. It can be surprised by genuinely novel
configurations.**

The calibration of fiscal multipliers, currency defense effectiveness, and
contagion effects is based on historical cases. When a configuration arises
that has no close historical analog — a combination of debt levels, reserve
positions, institutional quality, and external environment that has not been
seen before — the model extrapolates from nearest historical cases.

This extrapolation may be reasonable. It may also produce confidently wrong
outputs. The correct user response is to widen uncertainty manually and to
supplement model outputs with judgment from domain experts who have analyzed
similar situations.

---

## Dual-Use Position

### The Tension

WorldSim models financial attack vulnerability, currency attack indicators,
sanctions exposure, and SWIFT dependency for the explicit purpose of helping
vulnerable countries identify and reduce their exposure. A tool that can
identify defensive weak points is also, by definition, a tool that can
identify exploitable weak points from an attacking perspective.

This tension is real and we take it seriously.

### The Design Choices We Made

**What WorldSim builds:**
- Attack surface awareness for the entity modeling itself — "what is our
  currency attack vulnerability?"
- Historical pattern recognition for documented attack types — "what did
  previous currency attacks look like and what were the early warning signals?"
- Defense protocol library — sovereign equivalents of engine-out emergency
  procedures: what defensive actions are available, what are their tradeoffs,
  in what order should they be deployed?

**What WorldSim deliberately does not build:**
- Cross-country comparative attack surface ranking — which countries are
  most vulnerable to attack by an external actor
- Scenario modeling from an attacking actor's perspective
- Identification of specific vulnerability thresholds that would make an
  attack worthwhile
- Timing optimization for interventions designed to exploit country weakness

The line is not perfect. A user with both modeling skills and malicious intent
could attempt to use WorldSim's defensive analysis tools for offensive purposes.
We cannot prevent this entirely. We can ensure that the primary interface,
the standard outputs, and the designed scenarios are oriented toward defensive
awareness.

### What Was Deliberately Not Built, and Why

The Financial Warfare Module does not include a "scenario from attacker's
perspective" mode. It does not output a cross-country "most vulnerable targets"
ranking. It does not model the profit-and-loss of a successful currency attack
from the attacker's perspective.

These features would be technically straightforward to add. They were omitted
because they would shift the tool's primary utility from defense to offense,
and because the asymmetry we are trying to correct runs one direction. Building
a tool that helps powerful financial actors identify vulnerable country targets
would be the exact inversion of the mission.

---

## Challenge and Correction Process

### How to Challenge Any Position in This Document

Any position in this document can be challenged. The process:

1. **Open a GitHub Issue** titled "POLICY: Challenge to [section name]"
2. State the position you are challenging
3. State why you believe it is wrong, harmful, or should be changed
4. Propose the alternative position and its rationale

### The Governance Structure for Updates

Policy updates are reviewed by the WorldSim maintainer community. Changes to
territorial positions require engagement with the rationale for the current
position — a challenge that simply asserts a contested territorial claim without
engaging with the standards-based reasoning will be declined.

### The Standard Applied When Deciding Whether to Revise a Position

A position will be revised when:
1. The challenge demonstrates that the current position violates WorldSim's
   own stated principles (transparency, no silent assertion of contested
   positions, following ISO/IMF/UN standards bodies)
2. An ISO, IMF, or UN standard on which the position rests has changed
3. New evidence shows the position produces systematically misleading outputs

A position will not be revised when:
1. A government or actor advocates for a position that serves their interests
   — interest advocacy is not evidence
2. A position is criticized as insufficiently favorable to a particular
   political position without engaging the standards-based rationale

We reserve the right to decline challenges that are not made in good faith —
that seek to politicize the tool rather than improve its integrity. We commit
to responding to all good-faith challenges with a reasoned response, whether
or not we revise the position.

---

*This document is updated when WorldSim's positions change. Version history
is available in the git repository. The date of the most recent substantive
revision is tracked in the commit log.*
