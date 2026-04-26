# WorldSim

[![CI](https://github.com/PublicEnemage/worldsim/actions/workflows/ci.yml/badge.svg)](https://github.com/PublicEnemage/worldsim/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)

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
scenarios forward to validate what the model knows and does not know. It stress-
tests policy choices across a distribution of futures rather than a single
forecast. It makes the consequences of decisions visible before they are made —
including the consequences that standard macroeconomic dashboards do not show.

**The simulation is a structured reasoning tool, not a prediction engine.**
It produces distributions, not point estimates. Its blindspots are documented
and visible. It is calibrated, not confident.

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

The tool is open source by design. Proprietary analytical capability that
costs what sophisticated platforms cost defeats the purpose entirely. Anyone
can inspect, challenge, and improve the assumptions. That transparency is not
a compromise — it is the source of the tool's credibility.

---

## The North Star

A quinoa farmer in Bolivia will never know this tool exists. He did not build
it and will not use it. But his government may make better decisions because
it does — decisions about whether to accept a loan and on what terms, about
which conditions are mathematically necessary for debt sustainability and which
are not, about where the recovery envelope closes if a program goes wrong.

Build it as if he does.

---

## What Makes It Different

**The human cost ledger is a primary output.** Every scenario surfaces human
impact alongside financial impact — poverty headcount changes, health system
capacity, cohort-level distributional effects. These outputs have equal weight
to the macroeconomic indicators. They are never cut for velocity, never treated
as optional annotations on the real results.

**Backtesting as epistemic discipline.** Every model relationship is validated
against historical cases before being trusted for forward projection. Greece
2010, Thailand 1997, Lebanon 2019. The gap between model prediction and
historical outcome is not a failure to hide — it is the primary signal for
improvement. The simulation knows what it knows because it has been wrong about
what it did not.

**No false precision.** The simulation does not forecast. It does not output
facts about the future. Outputs are distributions over scenarios conditional
on stated assumptions. Confidence intervals widen when input data quality is
lower. Blindspots are documented explicitly, not buried in methodology appendices.

**Defense, not offense.** The simulation builds situational awareness and
defensive capability for vulnerable actors. It is not designed to help anyone
identify exploitable vulnerabilities in adversaries or amplify existing power
asymmetries. The asymmetry we are correcting runs one direction. So does the
tool.

---

## Current Status

**Early development. Not yet usable for analysis.**

| Milestone | Status | Description |
|---|---|---|
| 0 — Foundation | ✅ Complete | Repository structure, CI pipeline, ADR-001 |
| 1 — Simulation Core | 🔧 In progress | Data model, event propagation engine, annual timestep |
| 2 — Geospatial Foundation | Not started | PostGIS, FastAPI, MapLibre map |
| 3 — Scenario Engine | Not started | User-defined scenarios, backtesting |
| 4 — Human Cost Ledger | Not started | Cohort model, multi-framework dashboard |

The governance framework is established: coding standards, data standards,
contribution guidelines, compliance workflow, and policy transparency statement
are all in place before the codebase grows large enough to make them expensive
to retrofit.

---

## Getting Involved

Read [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) before opening a pull request.
New contributors are asked to read `CLAUDE.md`, the ADR for the area they are
working in, and the coding standards before writing code. The architecture has
intentional constraints — the simulation is designed around immutable state,
parallel measurement frameworks, and backtesting integrity requirements — and
understanding them before writing code matters.

The highest-value contribution right now is not code — it is domain expertise.
If you are an economist, a development finance specialist, a sovereign debt
analyst, or someone with direct experience of the decisions this tool is designed
to support, please open an issue. The model's assumptions need scrutiny from
people who understand the reality they are meant to represent.

Backtesting case contributions — documented historical scenarios with cited
data sources and specified fidelity thresholds — are treated as first-class
contributions alongside feature code.

---

## Technology

Python (FastAPI simulation engine, NumPy/Pandas/NetworkX), PostgreSQL with
PostGIS, Redis, React with MapLibre GL, AWS (ECS and Lambda), deployed as
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

## Export Control and Legal Compliance

### US Export Controls

This software is subject to the US Export Administration Regulations (EAR)
administered by the Bureau of Industry and Security (BIS). It is believed to
qualify for the publicly available software exclusion under EAR Section
742.15(b), as it is freely available to the public with no access controls,
restrictions on download, or restrictions on redistribution. The expected
Export Control Classification Number (ECCN) is EAR99.

Notwithstanding the open source exclusion, users remain responsible for
compliance with US sanctions programs administered by the Office of Foreign
Assets Control (OFAC). Users must not use this software in violation of
applicable sanctions programs, including but not limited to those targeting
specific countries, entities, or individuals designated by OFAC.

This software is not designed for, and is not intended for use in, weapons
development, military targeting, or intelligence operations directed against
civilian populations.

### Canadian Export Controls

This software is subject to the Export and Import Permits Act (EIPA) and the
Export Control List (ECL) administered by Global Affairs Canada.
General-purpose economic modeling and simulation software of this nature is
not believed to be listed on the Export Control List and does not require an
export permit for distribution as open source software.

Users in Canada are responsible for compliance with Canadian sanctions
regulations administered by Global Affairs Canada under the Special Economic
Measures Act (SEMA) and the Justice for Victims of Corrupt Foreign Officials
Act (JVCFOA). Contributors and users are responsible for determining the
applicability of these regulations to their specific use case.

### General Notice

This software is provided for research, policy analysis, and educational
purposes. The maintainers make no representations about the legal
permissibility of use in any specific jurisdiction. Users are solely
responsible for determining whether their use of this software complies with
applicable laws in their jurisdiction. Questions about specific use cases
should be directed to qualified legal counsel.

### Contributing

Contributions from developers in all countries are welcome, subject to the
project Code of Conduct. Accepting code contributions to a public open source
repository is not considered an export under either US or Canadian regulations.
Financial contributions, however, are subject to applicable sanctions screening
and may be declined if required by law.

---

## License

[MIT](LICENSE). Use it, fork it, build on it. If you improve it in ways that
serve the mission, contribute back.
