# CLAUDE.md — WorldSim Project Context

## What This Project Is:

This is an open-source geopolitical-economic simulation platform designed to
level the playing field between sophisticated financial and political actors
and the governments, communities, and people most vulnerable to their actions.

It is a flight simulator for national decision-making.

The mission is to give a finance minister sitting across from an IMF
negotiating team the same quality of scenario analysis, risk assessment, and
historical pattern recognition that the most sophisticated sovereign wealth
funds and financial institutions currently reserve for themselves.

The tool exists for the quinoa farmer in Bolivia who will never know it
exists, but whose government may make better decisions because it does.

---

## Guiding Principles

These principles are not constraints imposed from outside. They are values
embedded in the architecture. Every technical decision should be evaluated
against them.

**The Human Cost Ledger is Primary**
Financial metrics are necessary but not sufficient. Every scenario output
surfaces human impact alongside financial impact — lives affected, capability
losses, intergenerational consequences, distributional effects by cohort.
The human cost ledger is never a footnote. It is a primary output with equal
visual weight to financial indicators.

**No False Precision**
The simulation is not a prediction engine. It is a structured reasoning tool.
Outputs are distributions, not point estimates. Uncertainty is quantified and
displayed, not hidden. The model's blindspots are documented and visible.
We are calibrated, not confident.

**Open Source as Strategy, Not Ideology**
The tool must be accessible to the actors who most need it. Proprietary
analytical capability that costs what sophisticated platforms cost defeats the
purpose entirely. Open source also provides the methodological transparency
that gives the tool credibility — anyone can inspect, challenge, and improve
the assumptions.

**Backtesting as Epistemic Discipline**
Every model relationship must be validated against historical cases before
being trusted for forward projection. The gap between model prediction and
historical outcome is not a failure — it is the primary signal for improvement.
We know where our model is wrong by running it against history.

**Defense, Not Offense**
The tool builds situational awareness and defensive capability for vulnerable
actors. It is not designed to help anyone execute financial attacks, identify
exploitable vulnerabilities in adversaries, or amplify power asymmetries. The
asymmetry we are correcting runs one direction. So does the tool.

**The Flywheel**
The tool makes users better. Better users make the tool better. The community
intelligence that accumulates through use is as valuable as the codebase.
Architecture decisions should support this flywheel — feedback loops, learning
progression, community contribution pathways.

---

## The Simulation Framework

### Core Metaphor: The Flight Simulator

The tool is explicitly designed around aviation's approach to high-stakes
decision-making under uncertainty. Key concepts from aviation that shape both
the simulation engine and the user interface:

**Situational Awareness (Endsley's Three Levels)**
- Level 1 Perception: What are current indicator states?
- Level 2 Comprehension: What does this pattern mean given current conditions?
- Level 3 Projection: Where is this trajectory going if nothing changes?

The tool is primarily a Level 2 and Level 3 instrument. Data display is the
minimum. Pattern recognition and trajectory projection are the mission.

**Failure Mode Architecture**
Three distinct failure modes from aviation map to sovereign governance failures
and must be explicitly modeled:

*The Spin (Compounding Feedback with Narrow Recovery Window)*
Self-sustaining deterioration where standard responses accelerate the problem.
Historical analogs: sovereign debt spirals, hyperinflation cascades, ethnic
conflict autorotation. The simulation tracks recovery envelope — how much
fiscal space, reserve capacity, political capital, and time remains for the
recovery maneuver. When the recovery envelope closes, the simulation flags it
explicitly.

*Coffin Corner (Convergence of Constraints)*
The operating envelope narrows through individually rational decisions until
no policy response is available that doesn't cross a binding constraint.
The simulation tracks Policy Maneuver Margin continuously — a composite of
remaining policy degrees of freedom. Displayed as a primary indicator with
trend vector. Historical analogs: Thailand 1997, Greece 2010, Lebanon 2019.

*Hypoxia (Impaired Judgment Without Awareness of Impairment)*
The instrument that does the detecting and responding is itself compromised.
Modeled through an Institutional Cognitive Integrity Index — composite of
press freedom, leadership insularity, technocratic independence, dissent
tolerance, and policy-reality divergence. Degrades policy response
effectiveness in the simulation. Historical analogs: Soviet planning apparatus
1980s, regulatory capture pre-2008 financial crisis.

**Backside of the Power Curve (Counterintuitive Control Response)**
Regime-dependent relationships where the sign of the effect inverts beyond a
threshold. The simulation models these explicitly — not single functions but
regime-dependent functions with bifurcation points. Examples: fiscal
multiplier inversion under depressed conditions, currency defense effectiveness
reversal as reserves deplete, security dilemma escalation beyond a threshold.

**Get-There-Itis (Commitment Overriding Situational Assessment)**
The simulation monitors for policy trajectory commitment escalation — when
continued adherence to a plan shows signs of sunk cost reasoning rather than
genuine ongoing assessment. The clean-slate question is surfaced explicitly:
if encountering these conditions today with no prior commitment, would this
path be chosen?

**The CB Cloud (Asymmetric Visibility)**
Decision-makers see policy from the trailing edge — the reasoning, intention,
carefully considered tradeoffs. Affected populations see it from the leading
edge — the consequences. The human cost ledger is the weather radar that shows
the leading edge structure to those flying from behind.

---

## Architecture Decisions

### Technology Stack

**Backend Simulation Engine**
- Python (FastAPI) — scientific ecosystem for simulation mathematics
- NumPy, Pandas for numerical computation
- NetworkX for dependency graph modeling
- xarray for climate/geospatial time-series data (NetCDF format)

**Database**
- PostgreSQL with PostGIS extension — spatially-aware data storage
- Redis — real-time simulation state during active runs

**Frontend**
- React with MapLibre GL — map as hero element
- The map is not decorative. It is the primary interface.

**Infrastructure**
- AWS (ECS for long-running simulations, Lambda for request-scoped)
- AWS CDK for infrastructure as code — committed to the same repo
- GitHub Actions for CI/CD

**Development**
- Claude Code for AI-assisted development with agent team workflow
- All tasks managed through GitHub Issues and GitHub Projects
- Everything lives in GitHub — code, tasks, documentation, CI/CD

### Simulation Architecture

**Event-Driven Core**
The simulation engine is a graph of feedback loops, not a collection of
separate calculators. At each timestep, events propagate through the graph.
Modules update state. Updated state generates new events for the next
timestep. The ordering and weighting of propagations encodes the model's
theory of the world.

**Hierarchical Resolution**
- Level 1: Nation states (foundational, always active)
- Level 2: Subnational regions (activated per scenario requirement)
- Level 3: Urban/rural sector distinction within regions
- Level 4: Demographic cohorts (income quintiles × age bands × employment sector)
- Level 5: Key institutional actors (central bank, finance ministry, military)
- Level 6: Individual archetypes (future / Agent-Based Modeling territory)

Resolution is configurable per simulation run. Start with Level 1 globally.
Activate higher resolution for specific regions when the question demands it.

**Adaptive Temporal Resolution**
Default: annual or monthly timesteps for structural dynamics.
Auto-switch to finer resolution when crisis threshold is detected in a
subsystem. A currency crisis runs at daily resolution while the rest of
the world continues at monthly. Reverts when crisis resolves.

**Variable Resolution Simulation**
"Run this scenario at Level 1 globally, Level 2 for Middle East, Level 3
for Saudi Arabia specifically." This is a first-class architectural feature,
not a future enhancement.

### Key Simulation Modules

Each module is a discrete component with defined interfaces to the event
propagation system. Modules plug into the core graph — they do not replace it.

**Geopolitical Module**
Alliance relationships, territorial disputes, military capability indices,
diplomatic channel quality, information environment integrity.

**Macroeconomic Module**
GDP, growth rate, inflation, interest rates, fiscal balance, debt levels
and structure, monetary policy rules, fiscal multipliers (regime-dependent).

**Trade and Currency Module**
Bilateral trade flows, tariff schedules, trade agreement membership,
exchange rate dynamics, reserve currency composition, current account.

**Monetary System Module**
Global reserve currency basket dynamics, payment network membership
(SWIFT/CIPS), sovereign debt holdings matrix, currency confidence indices,
petrodollar and de-dollarization dynamics.

**Capital Flow Module**
Foreign direct investment by sector and source country, portfolio flows,
profit repatriation, transfer pricing gap estimates, illicit financial flows.

**National Asset Registry**
Public asset inventory by sector, foreign ownership percentage and
concentration (HHI) by sector, sovereign resilience floor thresholds,
privatization history and trajectory, reversibility assessment.

**Demographic and Health Module**
Population by cohort, birth and mortality rates, doctor-to-population ratio,
health system capacity, migration flows, urbanization rate, education
attainment by cohort.

**Climate Module**
Climate forcing from IPCC scenario data (SSP/RCP), El Niño/La Niña ENSO
forcing, agricultural stress indices, water stress by watershed, extreme
event frequency and intensity, infrastructure destruction probability.
Consumes pre-computed climate time series — does not do climate science.
Data sources: ERA5 reanalysis, NOAA, UK Met Office, Copernicus.

**Financial Warfare Module**
Currency attack vulnerability index, sanctions exposure, SWIFT dependency,
cyber infrastructure vulnerability, information environment manipulation
susceptibility. Attack surface composite scoring. Defense protocol library.

**Institutional Cognition Module**
Institutional Cognitive Integrity Index, policy-reality divergence tracking,
ghost flight detection (institution executing last programmed heading while
no longer genuinely responsive to environment).

### Multi-Currency Measurement

The simulation produces outputs simultaneously in multiple accounting units.
No master conversion rate between them. False aggregation is not acceptable.

- Financial units: standard economic metrics
- Human development units: Sen capability approach, HDI dimensions
- Ecological units: planetary boundary proximity, natural capital depletion
- Governance units: institutional quality, political freedom, rule of law

The dashboard displays all simultaneously. A radar chart shows the full
multi-dimensional profile. Deformation in any dimension is visible regardless
of performance in others.

User-defined weighting is supported — different users legitimately weight
dimensions differently. But threshold alerts fire regardless of user weighting
when any dimension crosses below a critical floor. No aggregate score can
hide a catastrophic failure in a single dimension.

**Minimum Descent Altitudes**
Hard floors below which the simulation flags terrain — levels below which
normal policy frameworks no longer provide protection and damage becomes
irreversible or generational. These are constraints, not suggestions.
The simulation does not recommend pathways that cross below them.

---

## Key Use Cases

### IMF/World Bank Loan Evaluation
A country on the cusp of accepting or declining a loan evaluates the full
conditionality package across a distribution of plausible futures. Not
"can we service this debt under the base case" but "across the full scenario
envelope, including plausible bad cases, what is the distribution of outcomes
for both the macroeconomic position and the human cost ledger."

Conditionality decomposition: which terms are mathematically load-bearing
for debt sustainability and which are not? Which combinations create coffin
corner configurations? What does the Policy Maneuver Margin look like under
the proposed program over its duration?

### Privatization Sovereign Resilience Assessment
Evaluating asset sales under fiscal duress against the Sovereign Resilience
Floor. Foreign ownership percentage and concentration (HHI) by strategic
sector. The low water mark — the point below which the country has put the
crown jewels on a firesale and crossed into sovereignty-impairing territory.
Buyback trajectory under recovery scenarios.

### Financial Attack Detection and Defense
Continuous monitoring of Currency Attack Vulnerability Index and composite
attack surface indicators. Early warning signatures calibrated against
documented historical cases. Emergency defense protocol library — the
sovereign equivalent of engine-out emergency landing procedures.

### Scenario Exploration and Geopolitical Stress Testing
User-defined scenarios with configurable variables, time acceleration,
and comparative analysis. The Hormuz closure. Saudi petrodollar relaxation.
De-dollarization tipping point dynamics. Sovereign debt as financial weapon.

### Backtesting and Historical Calibration
Run the simulation forward from historical baselines with injected known
events. Compare outputs to historical record. Surface variables that were
present, measurable, and consequential but were ignored in real-time
decision-making. The Eureka function: not predicting the future but exposing
the structure of the past.

### Emergency Procedure Generation
Country-specific, terrain-aware emergency procedures for anticipated failure
modes. The sovereign equivalent of engine-out landing options and emergency
descent profiles. Pre-computed when cognitive capacity is full. Available
when the emergency makes computation impossible.

---

## Data Sources

**Economic and Financial**
- World Bank Open Data — GDP, health, education, poverty (historical)
- IMF Balance of Payments Statistics
- BIS International Banking Statistics
- UNCTAD FDI database
- Tax Justice Network illicit flow estimates

**Geopolitical and Governance**
- V-Dem (Varieties of Democracy) — institutional quality indicators
- Freedom House — press freedom, political rights
- Transparency International — corruption perception
- GDELT Project — coded global events since 1979
- Uppsala Conflict Data Program — armed conflict database

**Climate and Physical**
- ERA5 Reanalysis (Copernicus) — historical climate 1940-present
- NOAA Climate Data Online
- UK Met Office HadCRUT
- IPCC Scenario Data (SSP/RCP) — future climate projections
- FAO AQUASTAT — water resources data

**Demographic and Health**
- UN Population Division — historical and projected demographics
- WHO Global Health Observatory
- Our World in Data — aggregated cross-domain datasets

---

## Agent Team Workflow

Development uses a multi-agent Claude Code workflow. Agents have defined
roles and operate against GitHub Issues as their task source.

**Architect Agent**
Produces system design documents, Architecture Decision Records (ADRs),
and API contracts before implementation begins. No code is written for a
significant feature without an ADR. Lives in `/docs/adr/`.

**Implementation Agents**
Write feature code against contracts produced by the Architect Agent.
May run in parallel for independent features. Always work against a
GitHub Issue. Always produce tests alongside code.

**QA Agent**
Writes tests, runs backtesting validation suites, reports failures.
Backtesting runs are part of CI — regressions in historical fidelity
are treated as build failures.

**Security and Review Agent**
Audits for vulnerabilities, dependency issues, data handling problems.
Specifically reviews any feature that touches sensitive country data
or financial attack surface modeling for dual-use concerns.

**DevOps Agent**
Manages CDK infrastructure, GitHub Actions pipeline configuration,
environment consistency.


**Socratic Agent**
Role: Architecture teacher and comprehension validator.
Purpose: Ensure the Engineering Lead maintains genuine understanding
of the architecture as it is built and evolves. Guards against
autopilot delegation where work gets done but judgment doesn't develop.

Operating modes:

TEACH: After a build session, explain what was just built conceptually.
Cover: what problem it solves, why this design over alternatives,
what contracts it enforces, what would break if a constraint were
removed. Use the ADR as curriculum. Use the actual code as primary text.
Calibrate depth to the Engineering Lead's current understanding.
Ask one check question at the end to confirm comprehension.

TEST: Before a build session or on request, probe comprehension of
existing architecture. Ask one conceptual question at a time. Wait
for the answer. Respond to what the answer reveals — correct
misconceptions directly, affirm correct understanding, and follow
threads where the mental model has gaps. Never move to the next
question until the current one is genuinely understood.

Tone: Socratic, not didactic. Ask before explaining. Surface the
Engineering Lead's existing mental model before correcting it.
The goal is not information transfer — it is genuine understanding
that persists and compounds.

Activation prompt: "Socratic Agent: [TEACH|TEST] — [topic or
recent session to cover]"

All agents read this CLAUDE.md at the start of every session.
All agents reference the relevant ADR before implementing any significant
feature. All agents treat the human cost ledger as a primary output,
never an afterthought.

---

## What We Are Building First

**Milestone 0 — Foundation (Current)**
- Repository structure established
- CLAUDE.md in place
- Technology stack installed and verified
- First Architecture Decision Record written: simulation core data model
- CI/CD pipeline skeleton in GitHub Actions

**Milestone 1 — Simulation Core**
- Country entity data model with Level 1 attributes
- Basic event propagation graph
- Annual timestep engine
- Seed database with real country data (World Bank)
- No UI — verify simulation logic through tests and CLI output

**Milestone 2 — Geospatial Foundation**
- PostGIS database with country boundary GeoJSON (Natural Earth)
- FastAPI layer serving country data
- MapLibre GL frontend rendering one variable as choropleth
- The map works. One variable. No scenarios yet.

**Milestone 3 — Scenario Engine**
- User-defined scenario configuration
- Time acceleration controls
- Comparative scenario output
- First backtesting run against a documented historical case

**Milestone 4 — Human Cost Ledger**
- Cohort-level demographic module
- Multi-currency measurement output
- Minimum Descent Altitude threshold system
- Radar chart dashboard displaying all dimensions simultaneously

Each milestone is a vertical slice — working software at every stage,
not infrastructure waiting for features.

---

## Architectural Principles for Claude Code Sessions

**Everything lives in GitHub.**
Code, tasks, documentation, ADRs, CI/CD configuration. One system of
record that both humans and agents can read and write.

**No significant feature without an ADR.**
Architecture Decision Records document what was decided, why, and what
alternatives were considered. They are the institutional memory that
survives leadership changes — both human and AI session boundaries.

**Tests are not optional.**
The backtesting infrastructure is the most important test suite.
Unit and integration tests are table stakes. A feature is not done
until it has tests and until the backtesting suite still passes.

**The human cost ledger is never cut for velocity.**
When scope must be reduced, reduce analytical sophistication before
reducing human impact visibility. A simpler model that shows human
consequences is better than a sophisticated model that hides them.

**Blindspots are documented, not hidden.**
Every model limitation, every variable we know we're not capturing,
every domain where the simulation's fidelity is known to be weak —
documented explicitly and visible to users. The simulation's integrity
depends on its honesty about its own limitations.

**Open from day one.**
Code is written as if it will be read by a Kenyan central banker,
a Bolivian agricultural economist, and a Lebanese finance ministry
official. Documented. Accessible. Not assuming the context that
produced it.

---

## Standards and Conventions

Every Claude Code session — regardless of which agent is active — operates
under these standards without being reminded. Reading them is part of session
initialization, not something that happens when a human asks.

**`docs/CODING_STANDARDS.md`**
Python code style (Ruff configuration, type hints, Google-style docstrings),
naming conventions, testing requirements (unit, integration, backtesting),
diagram standards (Mermaid, mandatory per ADR), commit message format
(Conventional Commits), ADR requirements, and agent team workflow standards.
Key contracts: Decimal not float for all monetary arithmetic, no bare except,
every public method has a test, human cost ledger outputs tested explicitly.

**`docs/DATA_STANDARDS.md`**
Encoding (UTF-8 everywhere, conversion first), language (English canonical,
translation keys only in simulation layer), datetime (UTC storage, ISO 8601,
IANA timezones), calendar support architecture (CalendarService, Gregorian +
Islamic Hijri + Solar Hijri + Hebrew + Ethiopian), fiscal year registry,
seasonal data standards (SeasonalContext, hemisphere-aware, FAO crop calendar),
units and measurements (Quantity type, Decimal, canonical units, dimensional
safety), currency standards (MonetaryValue type, constant 2015 USD canonical,
PPP vs. market rate assignment, exchange rate regime awareness), data quality
tier system (five tiers with documented confidence impact), data lineage
tracking, backtesting integrity (vintage dating required), and political and
territorial nomenclature (ISO 3166-1 alpha-3, disputed territory framework,
specific positions on Taiwan/Palestine/Kosovo/Western Sahara/Crimea).

**`docs/CONTRIBUTING.md`**
Development environment setup, architecture understanding requirements before
contributing (CLAUDE.md + ADR-001 + CODING_STANDARDS.md), agent team workflow,
contribution workflow (branch naming, PR format, review process), standards
compliance requirements, human cost ledger requirement, adding data sources,
adding simulation modules, adding backtesting cases, multilingual contribution
process, and code of conduct.

**`docs/POLICY.md`**
WorldSim's public policy transparency statement: governing philosophy,
territorial and nomenclature positions with rationale, data source selection
philosophy, economic methodology positions (constant 2015 USD, PPP vs. market
rates), what the simulation claims and does not claim, human cost ledger
methodology and known limitations, backtesting integrity position, declared
blindspots, dual-use position, and challenge/correction process.

---

## The North Star

When in doubt about any decision — architectural, feature priority,
scope, presentation — return to this:

A finance minister in a small, vulnerable country is sitting across
a table from an IMF negotiating team. They have limited time, limited
staff, and generational consequences riding on the decision they are
about to make.

Does this decision make the tool more useful to that person in that
moment?

If yes, proceed.
If no, reconsider.

The quinoa farmer doesn't know this tool exists.
Build it as if he does.
