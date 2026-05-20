# WorldSim Simulation Framework

> Extracted from CLAUDE.md (Issue #359). This document is mandatory reading
> for all agents. See CLAUDE.md §Session Continuity for the role-based
> reading table.

---

## Core Metaphor: The Flight Simulator

The tool is designed around aviation's approach to high-stakes decision-making
under uncertainty. The primary instrument framework:

**Situational Awareness (Endsley's Three Levels)**
- Level 1 Perception: What are current indicator states?
- Level 2 Comprehension: What does this pattern mean given current conditions?
- Level 3 Projection: Where is this trajectory going if nothing changes?

The tool is primarily a Level 2 and Level 3 instrument. Data display is the
minimum. Pattern recognition and trajectory projection are the mission.

---

## Three Interaction Modes

WorldSim operates in three interaction modes. Mode 3 is the north star for
instrument design — every instrument architecture decision must survive Mode 3.

**Mode 1 — Replay**
The user examines a historical scenario step by step. Primary cognitive task:
trajectory reconstruction. What happened, in what sequence, and why?

**Mode 2 — Simulation**
The user runs forward scenarios from a baseline. Primary cognitive task:
threshold-safe path construction. Which policy combinations keep all four
framework axes above their Minimum Descent Altitudes?

**Mode 3 — Active Control**
The user applies control inputs in real time and observes trajectory effects
as they propagate. Primary cognitive task: real-time steering within human
cost constraints. The instrument cluster must support split-second
comprehension of multi-framework trajectory effects.

Full UX architecture for all three modes: `docs/ux/north-star.md`,
`docs/ux/information-hierarchy.md`, `docs/ux/user-journeys.md`.

---

## Failure Mode Architecture

Six failure modes from aviation map to sovereign governance failures and are
explicitly modeled:

**The Spin** — Self-sustaining deterioration where standard responses accelerate
the problem. Diagnostic: Recovery Envelope (remaining fiscal space, reserves,
political capital, time before the corrective maneuver window closes).

**Coffin Corner** — The operating envelope narrows through individually rational
decisions until no policy response avoids a binding constraint. Diagnostic:
Policy Maneuver Margin (composite of remaining policy degrees of freedom),
displayed as a primary indicator with trend vector.

**Hypoxia** — The decision instrument itself is compromised without awareness
of impairment. Diagnostic: Institutional Cognitive Integrity Index (press
freedom, leadership insularity, technocratic independence, dissent tolerance,
policy-reality divergence).

**Backside of the Power Curve** — Regime-dependent relationships where the sign
of the effect inverts beyond a threshold: fiscal multiplier inversion under
depressed conditions, currency defense reversal as reserves deplete, security
dilemma escalation beyond a threshold.

**Get-There-Itis** — Commitment escalation overriding situational assessment.
The clean-slate question is surfaced explicitly: if encountering these conditions
today with no prior commitment, would this path be chosen?

**The CB Cloud** — Asymmetric visibility: decision-makers see policy from the
trailing edge (intent, tradeoffs); affected populations see it from the leading
edge (consequences). The human cost ledger is the weather radar for the leading
edge.

---

## Simulation Architecture

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

Resolution is configurable per simulation run.

**Adaptive Temporal Resolution**
Default: annual or monthly timesteps for structural dynamics. Auto-switches to
finer resolution when a crisis threshold is detected in a subsystem — a currency
crisis runs at daily resolution while the rest of the world continues at monthly.

**Variable Resolution Simulation**
"Run this scenario at Level 1 globally, Level 2 for Middle East, Level 3 for
Saudi Arabia specifically." This is a first-class architectural feature.

---

## Key Simulation Modules

Each module is a discrete component with defined interfaces to the event
propagation system. Modules plug into the core graph — they do not replace it.

Full capability status and per-module status: `docs/scenarios/module-capability-registry.md`

---

## Multi-Currency Measurement

The simulation produces outputs simultaneously in multiple accounting units.
No master conversion rate between them. False aggregation is not acceptable.

- Financial units: standard economic metrics
- Human development units: Sen capability approach, HDI dimensions
- Ecological units: planetary boundary proximity, natural capital depletion
- Governance units: institutional quality, political freedom, rule of law

The dashboard displays all simultaneously. A radar chart shows the full
multi-dimensional profile. Deformation in any dimension is visible regardless
of performance in others.

User-defined weighting is supported. But threshold alerts fire regardless of
user weighting when any dimension crosses below a critical floor. No aggregate
score can hide a catastrophic failure in a single dimension.

**Minimum Descent Altitudes**
Hard floors below which the simulation flags terrain — levels below which
normal policy frameworks no longer provide protection and damage becomes
irreversible or generational. These are constraints, not suggestions.
The simulation does not recommend pathways that cross below them.

---

## Key Use Cases

- **IMF/World Bank Loan Evaluation** — Evaluate conditionality packages across scenario distributions; decompose which terms are mathematically load-bearing for debt sustainability; track Policy Maneuver Margin over program duration.
- **Privatization Sovereign Resilience Assessment** — Evaluate asset sales against the Sovereign Resilience Floor; track foreign ownership concentration (HHI) by strategic sector; assess buyback trajectory under recovery scenarios.
- **Financial Attack Detection and Defense** — Monitor Currency Attack Vulnerability Index; match signatures against documented historical cases; emergency defense protocol library.
- **Scenario Exploration and Geopolitical Stress Testing** — User-defined scenarios with time acceleration and comparative output. Hormuz closure, petrodollar relaxation, de-dollarization tipping point dynamics.
- **Backtesting and Historical Calibration** — Run forward from historical baselines with injected known events; surface variables that were present, measurable, and consequential but ignored in real-time. The Eureka function: structure of the past, not prediction of the future.
- **Emergency Procedure Generation** — Country-specific, terrain-aware emergency procedures pre-computed when cognitive capacity is full; available when the emergency makes computation impossible.

Persona-anchored acceptance tests for each use case: `docs/ux/personas.md`
