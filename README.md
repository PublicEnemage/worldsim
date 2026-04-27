# WorldSim

[![CI](https://github.com/PublicEnemage/worldsim/actions/workflows/ci.yml/badge.svg)](https://github.com/PublicEnemage/worldsim/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Release](https://img.shields.io/badge/release-v0.4.0%20M4%20complete-green)](https://github.com/PublicEnemage/worldsim/releases/tag/v0.4.0)

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
model's blindspots are documented and visible. Full distribution outputs across
all simulation outputs are in progress (Milestone 5).

**This tool is in active pre-release development.** The working software
described below reflects Milestone 4. It is not yet usable for consequential
analysis.

---

## What's Built

The working system at Milestone 4:

- **Simulation engine** — Event-driven graph in Python. The `Quantity` type
  system tracks `value: Decimal`, unit, variable type (STOCK/FLOW/RATIO/
  DIMENSIONLESS), confidence tier (1–5), measurement framework, observation
  date, and source provenance. Events propagate through the relationship graph
  with hop-by-hop confidence tier attenuation.

- **Database** — PostgreSQL/PostGIS with 177 country entities loaded from
  Natural Earth 110m boundary data, 10 attributes per entity. Five declared
  territorial positions (Taiwan, Palestine, Kosovo, Western Sahara, Crimea)
  are enforced by a hard-gate validator on every database INSERT.

- **Backend API** — FastAPI with 15 endpoints. Float prohibition enforced
  end-to-end: `Quantity.value` is always `Decimal` in Python and `str` at
  the API boundary.

- **Scenario engine** — Create scenarios, advance step by step, compare two
  scenarios via delta choropleth. Scenario deletion writes a tombstone record
  enabling reconstruction from first principles under the determinism guarantee.

- **Backtesting fixture** — Greece 2010–2012: an annual forward simulation
  from the 2010 baseline with fiscal adjustment ControlInputs, validated
  against documented historical outcomes. Runs in CI as a build gate — a
  backtesting regression is a build failure.

- **Human Cost Ledger** — Multi-framework measurement output across financial,
  human development, ecological, and governance dimensions simultaneously, with
  equal visual weight to financial indicators. MDA (Minimum Descent Altitude)
  threshold system fires WARNING/CRITICAL/TERMINAL alerts when indicators cross
  hard floors. Demographic cohort model produces indicators by income quintile,
  age band, and employment sector. Note: ecological and governance composite
  scores are null at M4 — modules are planned for M6–M7; these axes render
  with a ⊘ indicator in the dashboard.

- **Frontend** — React + MapLibre GL choropleth map; scenario panel and step
  controls; EntityDetailDrawer with a four-axis radar chart, MDA alert panel,
  and per-framework indicator tables with collapsible cohort breakdowns; delta
  choropleth for side-by-side scenario comparison.

---

## Development Status

**Active pre-release development. Not yet usable for analysis.**

| Milestone | Status | Version | Description |
|---|---|---|---|
| M0 — Foundation | ✅ Complete | — | Repository, CI pipeline, compliance framework, ADR-001 |
| M1 — Simulation Core | ✅ Complete | v0.1.0 | Quantity type system, event propagation engine, input orchestration, ScenarioRunner |
| M2 — Geospatial Foundation | ✅ Complete | v0.2.0 | PostGIS schema, 177-entity seed, FastAPI layer, MapLibre GL choropleth |
| M3 — Scenario Engine | ✅ Complete | v0.3.0 | Scenario create/advance/compare, Greece 2010–2012 backtesting fixture, tombstones |
| M4 — Human Cost Ledger | ✅ Complete | [v0.4.0](https://github.com/PublicEnemage/worldsim/releases/tag/v0.4.0) | DemographicModule, MDA threshold system, radar chart dashboard, schema registry |
| M5 — Calibration and Uncertainty | 🔧 In progress | — | Distribution outputs, Macroeconomic Module, Playwright test suite, ADR-006 |

Full milestone history: [`CHANGELOG.md`](CHANGELOG.md). Live issue tracker:
[GitHub Milestones](https://github.com/PublicEnemage/worldsim/milestones).

Development uses a structured multi-agent Claude Code workflow: a single
Engineering Lead working with specialized agents (Architect, Implementation,
QA, Security, DevOps, and a nine-member Domain Intelligence Council of domain
experts). External contributor infrastructure is a Milestone 8 deliverable.

---

## What Makes It Different

**The human cost ledger is a primary output.** Every scenario surfaces human
impact alongside financial impact — poverty headcount changes, health system
capacity, cohort-level distributional effects. These outputs have equal weight
to the macroeconomic indicators. They are never cut for velocity, never treated
as optional annotations on the real results.

**Backtesting as epistemic discipline.** Every model relationship is validated
against historical cases before being trusted for forward projection. Greece
2010–2012 is the first implemented case, selected for the quality of its
historical data record and the IMF's own documented multiplier estimation error
(assumed ~0.5; empirical ~1.5). The gap between model prediction and historical
outcome is not a failure — it is the primary signal for improvement. Additional
cases (Argentina 2001–2002, Thailand 1997, Lebanon 2019–2020) are planned for
Milestone 6.

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

External contribution infrastructure — documentation written for non-agent
contributors, public methodology review, and Technical Steering Committee
formation — is a Milestone 8 deliverable. **The project is not yet ready for
general open-source contribution.**

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
