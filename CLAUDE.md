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

The tool is designed around aviation's approach to high-stakes decision-making
under uncertainty. The primary instrument framework:

**Situational Awareness (Endsley's Three Levels)**
- Level 1 Perception: What are current indicator states?
- Level 2 Comprehension: What does this pattern mean given current conditions?
- Level 3 Projection: Where is this trajectory going if nothing changes?

The tool is primarily a Level 2 and Level 3 instrument. Data display is the
minimum. Pattern recognition and trajectory projection are the mission.

### Failure Mode Architecture

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

Resolution is configurable per simulation run.

**Adaptive Temporal Resolution**
Default: annual or monthly timesteps for structural dynamics. Auto-switches to
finer resolution when a crisis threshold is detected in a subsystem — a currency
crisis runs at daily resolution while the rest of the world continues at monthly.

**Variable Resolution Simulation**
"Run this scenario at Level 1 globally, Level 2 for Middle East, Level 3 for
Saudi Arabia specifically." This is a first-class architectural feature.

### Key Simulation Modules

Each module is a discrete component with defined interfaces to the event
propagation system. Modules plug into the core graph — they do not replace it.

Full capability status and per-module status: `docs/scenarios/module-capability-registry.md`

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

---

## Data Sources

Approved sources by category: `docs/data-sources/approved-sources.md`

All sources must be registered in `source_registry` before their data is
loaded. Data quality tiers, provenance requirements, and backtesting integrity
rules: `docs/DATA_STANDARDS.md`.

---

## Agent Team Workflow

Development uses a multi-agent Claude Code workflow. Agents have defined
roles and operate against GitHub Issues as their task source.

**Engineering Lead (Human)**
Final decision authority on all architectural choices, mission alignment, and
milestone governance. The Engineering Lead is the human-in-the-loop that the
governance process is designed to surface decisions to, not bypass.

Specific responsibilities:

1. Final decision on all ADR option selections — agents propose, Engineering
   Lead accepts or rejects.
2. Mission alignment guardian — ensures technical decisions serve the canonical
   user (the debt restructuring specialist at a finance ministry) and the
   Equitable Build Process principle.
3. Milestone exit authority — no milestone closes without Engineering Lead
   sign-off on the exit checklist.
4. Agent instantiation decisions — which agents to activate, when to commission
   a new agent role.
5. Escalation point — when agents disagree, when a recommendation requires
   judgment beyond pattern-matching, or when the right answer requires breaking
   from established process.

What the Engineering Lead does not do: routine implementation prompts that
follow a clear ADR contract, issue closure and tracking hygiene, compliance
scan execution, test suite runs. These are delegated to agents.

The boundary is judgment vs. process. Decisions that require weighing mission
alignment, epistemic sequencing, or tradeoffs between competing principles
require the Engineering Lead. Decisions that follow clearly from an accepted
ADR or a documented standard do not.

Note: the desire to step back into a pure steering role is understandable as
the project matures. The path there is not creating an Engineering Lead agent
— it is ensuring agents are specified well enough to need human input only for
genuine judgment calls. Revisit the Engineering Lead scope at M9 entry, after
the methodology publication milestone, when there is empirical data on which
decisions actually required human judgment versus which the agents handled
autonomously.

**Architect Agent**
Produces system design documents, Architecture Decision Records (ADRs),
and API contracts before implementation begins. No code is written for a
significant feature without an ADR. Lives in `docs/adr/`.

**Implementation Agents**
Write feature code against contracts produced by the Architect Agent.
May run in parallel for independent features. Always work against a
GitHub Issue. Always produce tests alongside code.

**Pre-PR Checklist (Implementation Agent)**
Before opening any PR for a new feature, architecture change, or standards
modification, the Implementation Agent must:

1. Verify a GitHub Issue exists that describes the work. If no issue exists,
   create one before opening the PR. The issue must be assigned to the current
   milestone and labeled horizon:immediate.
2. Reference the issue in the PR description using 'Closes #N' so the issue
   closes automatically on merge.
3. Add the issue to the WorldSim Development Board project and set its status
   to In Review when the PR opens.
4. Cross-ADR impact: Does this commit change behavior documented in a different
   ADR? If yes, identify which ADR and which section. That ADR must be updated
   in the same commit — not as a follow-up. (Example: a commit implementing an
   ADR-006 constraint that changes a module's subscription list documented in
   ADR-005 must update ADR-005 Decision 1 in the same commit.)

Exempt from issue requirement: purely mechanical commits such as lint fixes,
import reordering, noqa suppressions, compliance scan registry updates, and
dependency patches. These must be part of a PR that references a parent issue
or ADR but do not require their own issue. The PR description must include a
one-line explanation of why no separate issue was needed.

**Issue Closure Rule (all agents)**
Every commit that resolves a tracked issue must close that issue in the same
session using `gh issue close N --comment "..."` with a one-sentence summary
of what was done and the commit SHA. For direct-to-main commits this replaces
the PR `Closes #N` mechanism — there is no automatic closure without a PR, so
the explicit `gh issue close` call is mandatory. An issue that is not explicitly
closed remains open in the tracker regardless of whether the work is done in
the codebase. The PM Agent reads the tracker — if the tracker is wrong, the
BRIEF is wrong.

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

**PM Agent**
Role: Execution governance and session focus.
Purpose: Keep the Engineering Lead working on the highest-priority committed
Milestone work rather than the most recently discovered work. Guards against
scope drift, cognitive overload from open issue accumulation, and the
gravitational pull of interesting new problems away from committed deliverables.

BRIEF: Structured session-start brief — committed milestone work, blockers
requiring Engineering Lead decision (max 3), decisions due today (max 3),
everything else filed, one recommended next action.

TRIAGE: One verdict per new issue or finding — BLOCKING NOW / THIS MILESTONE /
NEXT MILESTONE / PARKING LOT / WONTFIX. No elaboration unless asked.

HORIZON: Open-issue audit against current and upcoming Milestone definitions —
surfaces scope creep, orphaned issues, and committed work at risk.

FOCUS: One action and one reason. No list. No context.

Tone: Direct and short. Every response ends with a clear next action or an
explicit statement that no action is needed today.

Activation: "PM Agent: BRIEF", "PM Agent: TRIAGE — [issue or finding]",
"PM Agent: HORIZON", "PM Agent: FOCUS — [question or context]"

**Data Architect Agent**
Role: Schema registry owner and JSONB contract enforcer. Guards against the
class of silent bugs where code queries the right table but the wrong key and
returns null without error.

Owns and maintains `docs/schema/` (three authoritative files: `database.yml`,
`api_contracts.yml`, `simulation_state.yml`). Updates the relevant schema file
in the same commit as any code change that alters a table column, JSONB key
structure, API endpoint, or simulation type. Schema drift from code drift is a
compliance violation.

Activation: `Data Architect: REVIEW — [query or type access description]`
or `Data Architect: UPDATE — [what changed and which schema file to update]`

**UI/Frontend Architect Agent**
Role: Architectural authority for the React frontend layer. Guards against
the class of bugs that emerge when state management grows by accretion without
an owner (the M4 EntityDetailDrawer race condition is the canonical example).

Owns `docs/frontend/` (five architecture documents + five standards documents).
Sets binding standards from M5 onward. No component extraction, state library
adoption, or router introduction without a design decision in `design-decisions.md`.
Updates frontend docs in the same commit as any architectural change — architecture
drift from code drift is a compliance violation.

Activation: `UI/Frontend Architect: REVIEW — [component or feature area]`
or `UI/Frontend Architect: DESIGN — [decision to be made]`
or `UI/Frontend Architect: UPDATE — [what changed]`

**Chief Engineer Agent**
Role: Computational substrate authority for the simulation engine. Owns how
the simulation computes efficiently — propagation engine design, state vector
representation, memory layout, serialization performance, and hardware
utilization. Distinct from the Architect Agent, which owns system design and
module boundaries: the Chief Engineer owns how the system computes, not what
it computes.

Responsibilities:

1. Authors or co-authors any ADR that touches the simulation engine's
   computational model. ADR-007 (sparse matrix propagation) is the first;
   any future ADR covering state vector layout, parallelism, or serialization
   format requires Chief Engineer authorship or co-authorship.

2. Reviews all Architect Agent proposals that have computational performance
   implications before they are accepted. A proposal that defines a new module
   interface or relationship type without Chief Engineer review may create
   performance constraints that cannot be resolved without interface rework.

3. Owns the interpretability tooling suite (Issue #216) — propagation trace,
   equivalence harness, matrix visualizer, sparse profiler. These tools are
   the Chief Engineer's primary accountability to contributor accessibility:
   every performance optimization must remain inspectable by contributors
   without numerical computing backgrounds.

4. Benchmarks all performance-sensitive changes against the Equitable Build
   Process hardware targets (2-core, 8GB RAM) before they are merged. A
   change that passes CI but degrades performance on the target hardware is
   not mergeable without a documented tradeoff and Engineering Lead approval.

5. Owns the Decimal↔float precision boundary — specifies where conversion
   happens, how precision loss is bounded, and what tests enforce the contract.
   The boundary is defined in ADR-007; any change to the boundary requires
   Chief Engineer sign-off and a test demonstrating the new bound.

**Relationship to Architect Agent:** Architect defines what the system must
do (contracts, interfaces, module boundaries); Chief Engineer defines how it
does it efficiently (computation model, memory layout, hardware utilization).
Design decisions flow Architect → Chief Engineer for feasibility review;
performance constraints that require interface changes flow Chief Engineer →
Architect for resolution. Neither overrides the other — conflicts escalate to
the Engineering Lead.

**Relationship to Engineering Lead:** The Chief Engineer is the technical
authority on computational substrate decisions within the constraints the
Engineering Lead sets. The Engineering Lead sets the hardware target and the
equity constraint; the Chief Engineer finds the best solution within them.

Activation: `Chief Engineer: DESIGN — [computational problem to solve]`
or `Chief Engineer: BENCHMARK — [component to profile against hardware target]`
or `Chief Engineer: REVIEW — [ADR or implementation with performance implications]`

**UX Designer Agent** *(PLANNED — NOT YET ACTIVE; planned for instantiation at M6 entry)*
Role: UX north star owner and user journey authority. Defines what the
experience should be before the Frontend Architect Agent translates those
decisions into technical architecture. The UX Designer is upstream of
implementation — no significant frontend capability is built without a
documented user journey or information hierarchy decision from this agent.

Owns `docs/ux/north-star.md`, `user-journeys.md`, and `information-hierarchy.md` (full ownership detail restored at M6 activation).

Relationship to UI/Frontend Architect Agent: UX Designer defines the
experience; Frontend Architect owns the technical implementation of that
experience. Design decisions flow UX → Frontend Architecture, not the
reverse. Where the two are in tension, the UX Designer's user-outcome
rationale takes precedence; the Frontend Architect raises technical
feasibility constraints for the UX Designer to resolve.

Activation: `UX Designer: JOURNEY — [use case or user type]`
or `UX Designer: HIERARCHY — [screen or workflow to prioritize]`
or `UX Designer: REVIEW — [proposed UI change or component]`

All agents read this CLAUDE.md at the start of every session.
All agents reference the relevant ADR before implementing any significant
feature. All agents treat the human cost ledger as a primary output,
never an afterthought.

---

## Domain Intelligence Council

A panel of nine domain intelligence agents, each speaking for one measurement
framework or cross-cutting analytical perspective. Council agents do not
synthesise across frameworks — their role is to surface what their framework
reveals and where frameworks are in tension. Where all frameworks agree:
higher confidence. Where they conflict: the result most requiring human judgment.

The simulation architecture refuses to convert between measurement frameworks
because that conversion embeds a political choice. The council makes competing
interests explicit and visible. That adjudication is a human decision —
specifically, the decision of the people who will live with the consequences.

**Activation pattern:** `[Agent Name]: [SCENARIO|CHALLENGE|VALIDATE] — [topic]`
Full agent profiles and operational agent definitions: `docs/agents/domain-intelligence-council.md`

| Agent | Speaks for | Activation |
|---|---|---|
| Development Economist | Human development; Sen capability; HDI; distributional effects on cohorts | `Development Economist:` |
| Political Economist | Governance; political feasibility; elite capture; democratic legitimacy | `Political Economist:` |
| Ecological Economist | Natural capital; planetary boundaries; ecological cost distribution | `Ecological Economist:` |
| Geopolitical Analyst | Coercive dynamics; financial warfare; sanctions; debt leverage | `Geopolitical Analyst:` |
| Intergenerational Advocate | Future generations; irreversible thresholds; discounting injustice | `Intergenerational Advocate:` |
| Community Resilience | Social fabric; traditional practices; community cohesion | `Community Resilience:` |
| Investment Agent | Private capital; growth opportunity; RISK-AVERSE / RISK-TOLERANT / CATALYTIC | `Investment Agent: [mode]` |
| Social Dynamics | Public sentiment; collective behavior; legitimacy cascades | `Social Dynamics:` |
| Chief Methodologist | Statistical integrity; uncertainty quantification; distributional honesty | `Chief Methodologist:` |

**Operational agents:**
- **Council Orchestrator** — `Council Orchestrator: ORCHESTRATE — [scenario]` or `Council Orchestrator: ROADMAP — [gap]`
- **Architecture Review Facilitator** — `Architecture Review: FULL — [scope]` or `Architecture Review: TARGETED — [module]`

---

## What We Are Building First

M0–M7 complete (v0.1.0–v0.7.0). ADRs 001–006 current. See GitHub Releases
for full delivery history.

**Milestone 8 — Ecological and Governance Frameworks (Current)**
- All four radar chart axes live with real data
- Ecological Module complete; Governance Module complete
- Coffin Corner / Policy Maneuver Margin Zone 1 indicator
- MDA extended to ecological and governance indicators
- End-of-milestone demo: all four radar axes simultaneously

Each milestone is a vertical slice — working software at every stage,
not infrastructure waiting for features.

---

## Milestone Roadmap

**Milestone 7 — Technical Foundation (Complete — v0.7.0)**
Core deliverable: P0 technical debt resolved; compliance scan clean;
defensive programming standards codified. See GitHub Releases for full
delivery record.

**Milestone 8 — Ecological and Governance Frameworks (Current)**
Core deliverable: All four radar axes live; ecological and governance
composite scores non-null for the first time.

Scope:
- Ecological Module complete (planetary boundaries, natural capital depletion)
- Governance Module complete (institutional quality, political freedom, rule of law)
- All four radar chart axes live with real data
- Coffin Corner indicator: Policy Maneuver Margin Zone 1 widget
- MDA threshold system extended to ecological and governance indicators
- ADR-005 reviewed and extended for Ecological/Governance framework coverage
- End-of-milestone demo scenario (Greece 2010–2012 candidate)

**Milestone 9 — Standards Foundation**
Core deliverable: Canonical unit registry, field-level data certification,
and legibility framework. STD-REVIEW-004 gaps resolved.

Scope:
- Canonical unit registry replacing `unit="dimensionless"` placeholders
- Field-level certification chain and data admission tests
- WGI territorial conventions documented
- Legibility baseline audit and North Star legibility section
- Domain Intelligence Council blind stakeholder interviews
- M7 orphan issues triaged and closed

**Milestone 10 — Engine Integrity and Backtesting**
Core deliverable: Mean-reversion channels, Ecuador backtesting case,
sparse matrix propagation foundation, interpretability tooling suite.

**Milestone 11 — Political Economy and Conditionality**
Core deliverable: IMF conditionality modeling, political feasibility
constraints, elite capture dynamics, debt sustainability extension.

**Milestone 12 — Analyst Tooling and External Sector**
Core deliverable: Trade and external sector module; analyst tooling
polished; branch protection and second governance account established.

**Milestone 13 — Methodology Publication**
Core deliverable: Methodology publication and external validation;
Technical Steering Committee formation; public launch.

Full roadmap: `docs/roadmap/milestone-roadmap-m6-m8.md`

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

**Equitable Build Process.**
WorldSim's build, test, and development infrastructure must be accessible
to contributors who do not have access to high-end hardware or expensive
CI resources. A tool designed to level the playing field for vulnerable
actors must not reproduce the resource asymmetry it is designed to counter
in its own development infrastructure. The CI pipeline targets the GitHub
Actions free-tier runner (2-core, 7GB RAM, Ubuntu). Local development must
be possible on a machine with 8GB RAM. Test suites must not require
proprietary data, paid APIs, or licensed software to pass — all test
fixtures use open-licensed data. The Playwright E2E suite must have a
documented path to run without the full Docker Compose stack so that
contributors on modest hardware can run the complete test suite locally.

5. Computational efficiency is an equity requirement. The simulation engine
   must be optimized for the hardware that resource-constrained users and
   contributors actually have — not for well-resourced institutional
   infrastructure. Performance work that enables a finance ministry analyst
   on a four-core laptop to run analyses that previously required expensive
   compute is treated as first-class feature development, not optional
   optimization. Any future performance decision that trades accessibility
   for raw throughput must document the tradeoff explicitly and demonstrate
   that the resource-constrained user is not disadvantaged.

See `docs/CONTRIBUTING.md §Equitable Build Process` for the full numbered
requirements and implementation guidance.

---

## Standards and Conventions

Every Claude Code session — regardless of which agent is active — operates
under these standards without being reminded. Reading them is part of session
initialization, not something that happens when a human asks.

**`docs/CODING_STANDARDS.md`**
Python style, testing requirements, ADR standards, commit format (Conventional
Commits), diagram standards (Mermaid, mandatory per ADR). Key contracts:
`Decimal` not `float` for all monetary arithmetic; every public method has a
test; human cost ledger outputs tested explicitly.

**`docs/DATA_STANDARDS.md`**
Data encoding, calendar support, units, currency standards, quality tier system,
data lineage, backtesting integrity. Key contracts: ISO 3166-1 alpha-3 entity
IDs; declared positions on Taiwan/Palestine/Kosovo/Western Sahara/Crimea;
vintage dating required for all backtesting inputs.

**`docs/CONTRIBUTING.md`**
Development setup, agent workflow, PR format, review process. Key contract:
read CLAUDE.md + ADR-001 + CODING_STANDARDS.md before first contribution.

**`docs/POLICY.md`**
Public methodology transparency: territorial positions with rationale, what
the simulation claims and does not claim, dual-use position, challenge/correction
process.

**Compliance scan registry (`docs/compliance/scan-registry.md`)**
SCAN entries must always be appended at the end of the scan registry table.
Never insert a new entry mid-table. After adding a new entry, verify that the
table reads in ascending SCAN number order before committing. This rule exists
because mid-table insertions have caused ordering inversions twice — Issue #133
documents the recurring pattern.

**Schema registry (`docs/schema/`)**
Any agent writing a SQL query, reading a JSONB key, calling an API endpoint,
or instantiating a simulation type MUST first read the relevant schema file:

- Writing SQL or reading JSONB → read `docs/schema/database.yml` first.
  Verify column names, types, nullability, and JSONB key structure before
  writing the query. The `name_en` / `name` incident and the asyncpg JSONB
  string / dict incident are the canonical examples of what this prevents.
- Calling or implementing an API endpoint → read `docs/schema/api_contracts.yml`
  first. Verify request shape, response shape, and status codes.
- Writing simulation engine code or accessing Quantity fields → read
  `docs/schema/simulation_state.yml` first. Verify field names, types,
  and serialisation contracts (quantity_to_jsonb / quantity_from_jsonb).

Schema reads are mandatory pre-implementation steps, not optional references.
When schema files are out of date with the code, update them in the same
commit as the code change — schema drift is a compliance violation.

---

## Governance

### Current State

WorldSim is currently developed and maintained by a single Engineering Lead
(@PublicEnemage) who holds full repository authority — merge rights, exception
approval, architectural decisions, and infrastructure access.

This is a governance gap, and it is acknowledged as one. The compliance
framework in `docs/COMPLIANCE.md`, the CODEOWNERS file, and the Socratic Agent
partially compensate: the compliance workflow creates an audit trail, CODEOWNERS
establishes routing structure, and the Socratic Agent surfaces reasoning that
might otherwise go unexamined. But none of these substitute for genuine
separation of duties. An exception approved by the same person who introduced
the deviation is not independent review — it is documented self-approval.

The audit trail must reflect reality. Any compliance exception approved during
the single-principal phase must explicitly note the limitation in the exception
record itself. Exceptions must not imply a separation of duties that does not
exist.

### Intended Governance Progression

| Stage | Trigger | What changes |
|---|---|---|
| 1 — Immediate | Current milestone | Branch protection on `main`; CODEOWNERS in place; single-principal limitation declared |
| 2 — Second governance account | On demand | Second GitHub account with merge and exception-approval authority for engine core, docs, `.github` |
| 3 — First external domain reviewer | First complete module published | Domain expert with review authority over methodology; no implementation authority |
| 4 — Technical Steering Committee | First institutional user engagement | TSC authority over policy positions, methodology, and dual-use framework |

### Audit Trail Integrity Rule

No compliance exception may be self-approved during the single-principal phase
without the following statement appearing verbatim in the exception record:

> *"This exception was approved by the same individual who holds full
> repository authority. No independent review is available at this governance
> stage. See CLAUDE.md § Governance for the documented plan to address this
> limitation."*

This requirement exists so that the audit trail, when reviewed by future
contributors or institutional users, accurately represents the governance
conditions under which exceptions were made — rather than implying an
independence that did not exist.

---

## Canonical Artifact Locations

Every document type produced by agents has a canonical directory and naming
convention. **Before creating any document that has prior instances of the
same type, an agent must first locate the existing instances using `find` or
`grep` and confirm the new document follows the same directory and naming
convention.** Creating a document in the wrong directory (e.g. `docs/reviews/`
instead of `docs/standards/reviews/`) silently breaks the discoverability of
the artifact type and cannot be caught by CI.

| Artifact type | Directory | Naming convention | Update policy |
|---|---|---|---|
| Architecture Reviews | `docs/architecture/reviews/` | `ARCH-REVIEW-NNN-milestoneN.md` | New file per review |
| Standards Reviews | `docs/standards/reviews/` | `STD-REVIEW-NNN-milestoneN.md` | New file per review |
| Compliance Scan Registry | `docs/compliance/scan-registry.md` | Single file — append SCAN entries only | Append only; never create a new file; never insert mid-table |
| Architecture Decision Records | `docs/adr/` | `ADR-NNN-short-name.md` | New file per decision |
| Module Capability Registry | `docs/scenarios/module-capability-registry.md` | Single file | Updated in place with each milestone |

### Pre-creation checklist for documents

Before writing a new review, ADR, or registry entry:

1. Run `find docs/ -name "ARCH-REVIEW*"` (or the equivalent pattern for the
   document type) to locate existing instances.
2. Confirm the target directory matches where existing instances live — not
   where it seems like they should live.
3. Confirm the filename follows the naming convention of existing instances
   exactly (prefix, separator style, milestone label).
4. Only then create the file.

This check takes ten seconds. The STD-REVIEW-003 incident (placed in
`docs/reviews/` instead of `docs/standards/reviews/`) is the canonical
example of what this rule prevents.

---

## GitHub Label Reference

Use only the labels defined in `docs/labels.md`. **Do not invent new labels.**
If a required label is missing, use the closest existing label, add a comment
explaining which label would be more precise, and note the gap in the PR
description.

### Labels that do not exist and must not be invented

| Requested label | Use instead | Notes |
|---|---|---|
| `standards` | `documentation` | Standards review issues are documentation work |
| `architecture` | `enhancement` or `documentation` | ADRs → `documentation`; new modules → `enhancement` |
| `backtesting` | `enhancement` | Backtesting fixture work is an enhancement |
| `security` | `compliance:critical` or `compliance:major` | Security findings are compliance findings |
| `performance` | `enhancement` | No dedicated performance label exists |
| `milestone:N` | Use the GitHub milestone assignment | Do not encode milestone in a label |

---

## Milestone Retrospective Process

Every milestone exit ceremony must include a retrospective. The retrospective
is not optional and is not a formality. It is an epistemic discipline — the
same discipline that makes backtesting the primary signal for model improvement
applies here to the development process itself.

### What the Retrospective Covers

Every retrospective addresses three questions, in writing, as a comment on
the exit checklist Issue:

**1. What defects evaded the test suite?**
Name every bug that was caught by manual testing, user report, or visual
inspection rather than by an automated test. For each: what was the defect,
how was it caught, and at what point in development would a test have caught
it earlier?

**2. What process gaps caused them?**
For each defect that evaded testing: what test did not exist that would have
caught it? Was the gap a missing test type (unit, integration, end-to-end),
a missing coverage area, or a test-after rather than test-before discipline
failure? Name the gap specifically — not "we need more tests" but "we had
no Playwright test for the scenario advance → drawer open flow."

**3. What testing improvements are required before the next milestone begins?**
Specific, named deliverables — not intentions. Each improvement is a blocking
requirement for the next milestone exit, not a suggestion. If a testing gap
was identified, the next milestone exit checklist must include a checkbox
confirming the gap was closed.

### The M4 Radar Chart Drawer Incident — Canonical Reference

Canonical incident record: `docs/frontend/testing-standards.md §Anti-Patterns from M4` and `design-decisions.md DD-004`.


---

## The North Star

The tool's positions are declared, not hidden. Transparency about what we claim and do not claim is as important as the quality of what we build. A user who cannot understand and challenge our methodology cannot genuinely use our tool — they can only depend on it. Dependency is not leveling.

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
