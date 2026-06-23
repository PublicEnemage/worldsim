# WorldSim

[![CI](https://github.com/PublicEnemage/worldsim/actions/workflows/ci.yml/badge.svg)](https://github.com/PublicEnemage/worldsim/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Release](https://img.shields.io/badge/release-v0.15.0%20M15%20complete-green)](https://github.com/PublicEnemage/worldsim/releases/tag/v0.15.0)

**An open-source geopolitical-economic simulation platform for governments and
vulnerable actors navigating high-stakes decisions under uncertainty.**

---

## The Problem

When a finance minister sits across a table from an IMF negotiating team, the
asymmetry is severe. The negotiating team has access to sophisticated scenario
analysis — decades of historical pattern data, stress-tested debt sustainability
models, distributional impact projections. The minister may be working from a
briefing document and instinct.

That asymmetry is not an accident. The best sovereign debt analysis tools are
expensive, proprietary, and built for the institutions that can afford them.
The governments that most need rigorous independent analysis — smaller economies,
lower-income countries, states under external fiscal pressure — are the least
likely to have it.

WorldSim exists to close that gap.

---

## What It Is

WorldSim is a flight simulator for national decision-making.

A flight simulator does not fly the plane. It builds judgment. It lets pilots
rehearse emergencies before emergencies happen, test decisions without paying
the cost of getting them wrong, and develop the situational awareness that only
comes from seeing a crisis from the inside.

WorldSim does the same for sovereign economic decisions. It runs historical
scenarios forward to validate what the model knows and does not know. It
stress-tests policy choices across a distribution of futures rather than a
single forecast. It makes the consequences of decisions visible before they are
made — including the consequences that standard macroeconomic dashboards do
not show.

**The simulation is a structured reasoning tool, not a prediction engine.** It
is designed to produce distributions, not point estimates — outputs carry
confidence tiers, uncertainty bounds are quantified and displayed, and the
model's blindspots are documented and visible. All four measurement framework
axes are live at Milestone 12 (financial, human development, ecological,
governance); Mode 3 Active Control enables counter-scenario branching for
negotiation support.

**This tool is in active pre-release development.** The working software
described below reflects Milestone 15 (ADR-017 Zone 1A Information Architecture;
Layer 3 self-interpreting outputs in Zone 1B and Zone 1D; Path 1 approved source
network; cohort disaggregation and political risk designs; grounding strip date
accuracy; accessibility validated on 8GB/4-core target hardware). M16 is in
active development.

---

## What's Built

The working system at Milestone 15 (core components — not exhaustive):

- **Simulation engine** — Event-driven graph in Python. The `Quantity` type
  system tracks `value: Decimal`, unit, variable type (STOCK/FLOW/RATIO/
  DIMENSIONLESS), confidence tier (1–5), measurement framework, observation
  date, and source provenance. Events propagate through the relationship graph
  with hop-by-hop confidence tier attenuation.

- **MacroeconomicModule** — GDP, fiscal balance, and inflation with
  regime-dependent fiscal multipliers: standard multiplier (0.8) in healthy
  conditions; elevated multiplier (1.5) in depressed regimes (unemployment
  above 15%). Processes FiscalPolicyInput, MonetaryRateInput, and
  EmergencyPolicyInput events.

- **EcologicalModule** — Planetary boundary proximity scoring. CO2 concentration
  tracked against the Rockström 2009 350 ppm boundary (confidence tier 2).
  Land-use pressure index tracked against the Richardson 2023 boundary.
  Composite score: unweighted mean of boundary proximity scores.
  STOCK delta path emits new absolute levels (not raw deltas) — the propagation
  engine replaces STOCK attributes.

- **Database** — PostgreSQL/PostGIS with 177 country entities loaded from
  Natural Earth 110m boundary data. Five declared territorial positions
  (Taiwan, Palestine, Kosovo, Western Sahara, Crimea) are enforced by a
  hard-gate validator on every database INSERT. `backtesting_thresholds`,
  `simulation_reference_constants` (planetary boundary values with temporal
  guards), and `scenario_deleted_tombstones` tables.

- **Backend API** — FastAPI. Float prohibition enforced end-to-end:
  `Quantity.value` is always `Decimal` in Python and `str` at the API
  boundary. Composite score computation via framework-dispatched strategy:
  ecological uses boundary proximity; financial and human development use
  percentile rank. Ecological is exempt from the single-entity guard
  (boundary proximity is physically meaningful for one country).

- **Scenario engine** — Create scenarios, advance step by step, compare two
  scenarios via delta choropleth. Scenario deletion writes a tombstone record
  enabling reconstruction from first principles under the determinism guarantee.

- **Backtesting fixtures** — Two validated historical cases:
  - *Greece 2010–2015*: six-step fixture; fiscal adjustment under the IMF/EU
    program; CO2 ecological trajectory live from step 1 (NOAA MLO 388 ppm
    seed); step 5 (2014) is the thesis frame — financial partial recovery,
    human development depressed; DIRECTION_ONLY thresholds
  - *Argentina 2001–2002*: Zero Deficit Plan spending cut and sovereign
    default; DIRECTION_ONLY GDP contraction thresholds at both steps
  Both run in CI as a build gate — a backtesting regression is a build failure.

- **Human Cost Ledger** — Multi-framework measurement output across financial,
  human development, ecological, and governance dimensions simultaneously, with
  equal visual weight to financial indicators. MDA (Minimum Descent Altitude)
  threshold system fires WARNING/CRITICAL/TERMINAL alerts when indicators cross
  hard floors. Demographic cohort model produces indicators by income quintile,
  age band, and employment sector. GovernanceModule promoted to live axis at M10
  (five promotion criteria met; V-Dem data; ADR-005 Amendment 4).

- **Frontend** — React + MapLibre GL choropleth map; scenario panel and step
  controls; instrument cluster (Zone 1A TrajectoryView, Zone 1B MDA Alert Panel
  with persistent-detail [indicator name, floor, negotiation-defensibility label],
  Zone 1C PMM widget, Zone 1D four-framework composite display with L0 tier
  annotations); Grounding strip (source-cited initial state at zero interaction);
  Assumption Surface (active parameter display); persistent scenario identity
  header; Mode 3 Active Control (branch-from-snapshot, fiscal multiplier input,
  live A/B trajectory comparison); multi-country scenario support; delta
  choropleth; Playwright E2E suite at 1440×900.

---

## Development Status

**Active pre-release development. Demo 5 delivered 2026-06-20. M15 complete (v0.15.0). M16 in active development.**

| Milestone | Status | Version | Description |
|---|---|---|---|
| M0 — Foundation | ✅ Complete | — | Repository, CI pipeline, compliance framework, ADR-001 |
| M1 — Simulation Core | ✅ Complete | v0.1.0 | Quantity type system, event propagation engine, input orchestration, ScenarioRunner |
| M2 — Geospatial Foundation | ✅ Complete | v0.2.0 | PostGIS schema, 177-entity seed, FastAPI layer, MapLibre GL choropleth |
| M3 — Scenario Engine | ✅ Complete | v0.3.0 | Scenario create/advance/compare, Greece 2010–2012 backtesting fixture, tombstones |
| M4 — Human Cost Ledger | ✅ Complete | [v0.4.0](https://github.com/PublicEnemage/worldsim/releases/tag/v0.4.0) | DemographicModule, MDA threshold system, radar chart dashboard, schema registry |
| M5 — Calibration and Uncertainty | ✅ Complete | [v0.5.0](https://github.com/PublicEnemage/worldsim/releases/tag/v0.5.0) | MacroeconomicModule, Argentina backtesting, DISTRIBUTION_COMBINED thresholds, Playwright suite |
| M6 — Backtesting Coverage Expansion | ✅ Complete | v0.6.0 | EcologicalModule initial, HumanDevelopmentModule, Greece 2010–2015 fixture extension |
| M7 — Technical Foundation | ✅ Complete | v0.7.0 | P0 technical debt resolved; compliance scan clean; defensive programming standards |
| M8 — Ecological and Governance Frameworks | ✅ Complete | [v0.8.0](https://github.com/PublicEnemage/worldsim/releases/tag/v0.8.0) | Three live radar axes; honest-null governance; Greece 2010–2015 demo; Case B UX verdict |
| M9 — Standards Foundation | ✅ Complete | — | UX architecture (ADR-008/010); five user personas; instrument cluster specification; agent RACI |
| M10 — Engine Integrity and Instrument Delivery | ✅ Complete | [v0.10.0](https://github.com/PublicEnemage/worldsim/releases/tag/v0.10.0) | Instrument cluster live; all four framework axes live; GovernanceModule promoted; Demo 3 |
| M11 — Engine Investigation and Political Economy | ✅ Complete | [v0.11.0](https://github.com/PublicEnemage/worldsim/releases/tag/v0.11.0) | Matrix engine (ADR-009); PoliticalEconomyModule; non-linear propagation (ADR-011); snapshots/restore |
| M11.5 — Usability Validation | ✅ Complete | — | Priority A usability sessions (3 personas); universal finding; M12 scope filed |
| M12 — Active Control and External Sector | ✅ Complete | [v0.12.1](https://github.com/PublicEnemage/worldsim/releases/tag/v0.12.1) | Matrix engine production (ADR-012); ExternalSectorModule; Mode 3 Active Control; Demo 4 |
| M13 — Political Economy and Instrument Credibility | ✅ Complete | v0.13.0 | ADR-013/ADR-014; political economy module; alert panel Zone 1B persistent-detail; instrument legibility; mode transition UX; Process Redesign Phases 0–D |
| M14 — Trust Architecture and Instrument Credibility | ✅ Complete | [v0.14.0](https://github.com/PublicEnemage/worldsim/releases/tag/v0.14.0) | ADR-016 (Scenario Grounding Architecture); ADR-015 (Evidence Thread Architecture); PSP in Zone 1D; methodology foundation docs; governance; Demo 5 |
| M15 — Human Cost Architecture | ✅ Complete | [v0.15.0](https://github.com/PublicEnemage/worldsim/releases/tag/v0.15.0) | ADR-017 Zone 1A information architecture; Layer 3 self-interpreting outputs (Zone 1B + Zone 1D); Path 1 approved source network; cohort disaggregation and political risk designs; accessibility validation |
| M16 — Distributional Visibility | 🔧 In progress | — | Zone 1A implementation (Phase 4); cohort disaggregation on primary surface; political risk summary; live external demo (#843 — exit gate); Demo 6 |

Full milestone history: [`CHANGELOG.md`](CHANGELOG.md). Live issue tracker:
[GitHub Milestones](https://github.com/PublicEnemage/worldsim/milestones).

Development uses a structured multi-agent Claude Code workflow: a single
Engineering Lead working with specialized agents (Architect, Implementation,
QA, Security, DevOps, and a nine-member Domain Intelligence Council of domain
experts). External contributor infrastructure is on the M14+ roadmap.

---

## What Makes It Different

**The human cost ledger is a primary output.** Every scenario surfaces human
impact alongside financial impact — poverty headcount changes, health system
capacity, cohort-level distributional effects. These outputs have equal weight
to the macroeconomic indicators. They are never cut for velocity, never treated
as optional annotations on the real results.

**Backtesting as epistemic discipline.** Every model relationship is validated
against historical cases before being trusted for forward projection. Five cases are validated: Greece 2010–2015 (fiscal multiplier estimation
error — IMF assumed ~0.5, empirical ~1.5), Argentina 2001–2002 (Zero Deficit
Plan sovereign default; Argentina year 1 reaches MAGNITUDE calibration:
−10.55% vs historical −10.9%), Lebanon, Thailand, and Ecuador. All five run
in CI as a build gate — a backtesting regression is a build failure. Argentina
year 1 is MAGNITUDE calibrated; remaining cases are DIRECTION_ONLY. The gap
between model prediction and historical outcome is not a failure — it is the
primary signal for improvement.

**No false precision.** Outputs are designed to be distributions over scenarios
conditional on stated assumptions, not point forecasts about the future.
Confidence tiers degrade when input data quality is lower. Blindspots are
documented explicitly, not buried in methodology appendices.

**Defense, not offense.** The simulation builds situational awareness and
defensive capability for vulnerable actors. It is not designed to help anyone
identify exploitable vulnerabilities in adversaries or amplify existing power
asymmetries. The asymmetry we are correcting runs one direction. So does the
tool.

---

## Who It Is For

Finance ministries and central banks in countries facing external financing
negotiations, debt restructuring, or structural adjustment programs.

Civil society organizations that need independent analytical capacity to
scrutinize official economic projections and conditionality terms.

Researchers and economists working on sovereign debt, development finance, and
the political economy of adjustment.

Journalists and policy advocates who need to understand what a proposed program
actually implies for real people — not just what the headline debt ratios say.

The tool is open source by design. Proprietary analytical capability that costs
what sophisticated platforms cost defeats the purpose entirely. Anyone can
inspect, challenge, and improve the assumptions. That transparency is not a
compromise — it is the source of the tool's credibility.

---

## Getting Started

New to WorldSim? The onboarding guides are the fastest path to working proficiency:

- **[Quick Start Guide](docs/onboarding/quick-start.md)** — load a scenario and read
  the instrument cluster in 10 minutes, no prior knowledge required
- **[Scenario Creation Guide](docs/onboarding/scenario-creation.md)** — understand
  the Grounding Strip, data quality tiers, and module configuration before running a scenario
- **[Data Provenance Guide](docs/onboarding/data-provenance.md)** — confidence tiers
  (T1–T5), Structural Absence Declarations, and how to cite WorldSim outputs in a
  negotiating context
- **[Methodology Overview](docs/onboarding/methodology-overview.md)** — what the
  simulation claims, what it does not claim, and documented model blindspots

---

## Running Locally

Requires [Docker](https://docs.docker.com/get-docker/) and Docker Compose.

```bash
# Start all services (database, API, frontend)
docker compose up

# In a second terminal, once the API container is healthy:
docker compose exec api alembic upgrade head
docker compose exec api python -m app.db.seed.natural_earth_loader
```

Open `http://localhost:5173`. You should see:

- A world choropleth map with 177 country entities and switchable attributes
- A scenario panel — create a scenario, advance it step by step, watch the
  choropleth update
- An entity detail drawer — click any country to see its multi-framework
  output, radar chart, and MDA threshold alerts
- Compare mode — select a second scenario to see the delta choropleth

This is a development environment. There is no production deployment.

---

## Architecture

The simulation architecture is documented in [`CLAUDE.md`](CLAUDE.md) (project
context, guiding principles, agent roles, and behavioral conventions for all
Claude Code sessions) and in Architecture Decision Records (ADRs) in
[`docs/adr/`](docs/adr/). No significant feature is implemented without an ADR
— the ADR is the primary mechanism for architectural decisions and the
institutional memory that survives session boundaries.

Development uses a structured multi-agent Claude Code workflow documented in
`CLAUDE.md`. Significant features are designed by an Architect Agent and
reviewed by Domain Intelligence Council members before implementation begins.
The [`docs/schema/`](docs/schema/) directory contains authoritative YAML
contracts for the database schema, API endpoints, and simulation types —
agents are required to read the relevant schema file before writing any query
or type access.

The compliance scan registry at
[`docs/compliance/scan-registry.md`](docs/compliance/scan-registry.md) records
all compliance scans. The project runs at zero violations against its own
standards at every milestone exit.

---

## Contributing

External contribution infrastructure — documentation for non-agent contributors,
public methodology review, and Technical Steering Committee formation — is
roadmapped for M13–M14. **The project is not yet ready for general open-source
contribution.**

What is valuable now:

- **Domain expertise** — If you are a development economist, sovereign debt
  analyst, or someone with direct experience of the decisions this tool is
  designed to support, open an issue. The model's assumptions need scrutiny
  from people who understand the reality they represent.
- **Backtesting case proposals** — A documented historical scenario with cited
  data sources, a clear policy decision sequence, and proposed fidelity
  thresholds. Backtesting contributions are first-class contributions alongside
  feature code.

Read [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) before opening a pull
request. Read `CLAUDE.md` and the relevant ADR before writing code.

---

## Technology

Python (FastAPI simulation engine, `Decimal` arithmetic throughout,
NumPy/NetworkX for propagation), PostgreSQL 16 with PostGIS 3.4, asyncpg for
runtime queries (SQLAlchemy retained for Alembic migrations only), React with
TypeScript and MapLibre GL JS, Recharts, AWS (ECS and Lambda) deployed as
infrastructure-as-code via AWS CDK.

---

## Policy and Methodology Transparency

WorldSim makes policy choices — about which countries are recognized, which
exchange rates are treated as official, what base year is used for monetary
comparison, and how disputed territories are handled. These choices are declared
rather than hidden.

[`docs/POLICY.md`](docs/POLICY.md) is a plain-language transparency statement
written for non-technical readers. It covers the territorial positions, data
source philosophy, economic methodology choices, what the simulation claims and
does not claim, the declared blindspots, and how any position can be challenged.
If you are considering using this tool to inform a consequential decision, read
it first.

---

## Export Control and Legal

This software is believed to qualify for the publicly available software
exclusion under US EAR Section 742.15(b) (expected ECCN: EAR99) and is not
believed to be listed on Canada's Export Control List. Users remain responsible
for compliance with US OFAC sanctions programs and Canadian sanctions
regulations under SEMA and JVCFOA. This software is not designed for weapons
development, military targeting, or intelligence operations directed against
civilian populations. See [`LEGAL.md`](LEGAL.md) for the full export control
statement and jurisdiction-specific guidance.

---

## The North Star

A quinoa farmer in Bolivia will never know this tool exists. He did not build
it and will not use it. But his government may make better decisions because
it does — decisions about whether to accept a loan and on what terms, about
which conditions are mathematically necessary for debt sustainability and which
are not, about where the recovery envelope closes if a program goes wrong.

Build it as if he does.

---

## License

[MIT](LICENSE). Use it, fork it, build on it. If you improve it in ways that
serve the mission, contribute back.
