# CLAUDE.md — WorldSim Project Context

> Last significant revision: 2026-06-12
> Updated against: M13 active — M12 closed (v0.12.1); matrix engine in production (ADR-009/012); ExternalSectorModule; Mode 3 Active Control; Demo 4 complete; Process Redesign Phase 0 endorsed; Phase A endorsed (2026-06-12); Phase B open
> Previous version context: 2026-06-05 — M12 active; release branch workflow added; PM Agent SPRINT mode added; sprint planning SOP codified; north star test as formal process gate (FD-1 closed)

> **Reader Orientation:** This is the permanent project constitution — read it in full before beginning any session. It contains the mission, architectural commitments, and process rules that govern all work in this repository. Anyone making a change in this codebase, human or agent, must have read this document first. Key must-read sections if time is short: Session Continuity (what to read and in what order), Guiding Principles (the values behind every technical decision), and §Architectural Principles for Claude Code Sessions (process gates including pre-push lint, PR merge gate, and file authority rules that will cause compliance violations if not followed).

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

## Founding Document

The reasoning behind every principle in this document is in `docs/vision/worldsim-founding-document.md`. Read it to understand the why beneath the what.

---

## Session Continuity

Before beginning any task, read these files in order:
1. `SESSION_STATE.md` — current work streams, open PRs, pending decisions
2. `docs/process/agents.md` — agent roster, personas, activation protocols
3. `CLAUDE.md` — permanent constitution, architecture, standards

`CLAUDE.md` is the permanent constitution. `SESSION_STATE.md` is the
current situation report. `docs/process/agents.md` is the canonical home
for all agent personas. All three are required reading at session start.

At the end of every session, updating `SESSION_STATE.md` is the last
action before closing — not optional.

### Role-based mandatory reading

| Role | Additional required reading |
|---|---|
| All agents | `docs/architecture/simulation-framework.md` |
| UX / Frontend | `docs/ux/north-star.md`, `docs/ux/information-hierarchy.md`, `docs/ux/user-journeys.md`, `docs/ux/personas.md` (when available), `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md` |
| Data / Backend | `docs/DATA_STANDARDS.md`, `docs/schema/database.yml`, `docs/schema/simulation_state.yml` |
| Architecture | Relevant ADR in `docs/adr/` |
| Standards / Compliance | `docs/CODING_STANDARDS.md`, `docs/compliance/scan-registry.md` |

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

## The Platform Principle

WorldSim is situation-agnostic. The engine, measurement framework, instrument
architecture, and UX are invariant across scenarios. Only data inputs change.
There is no Greece mode, no tariff mode, no budget planning mode — one
platform, different ingredients.

Any proposal requiring scenario-specific modules rather than scenario-specific
data inputs must document why the platform principle cannot be satisfied. The
default answer is that it can: what looks like a mode requirement is almost
always a data requirement.

This principle is the primary constraint on M9 UX design. Instruments are
designed for the platform, not for any scenario.

---

## Synthetic Data and the Data Inference Layer

Data poverty is not a blocker. WorldSim generates synthetic data via
statistical inference from comparable economies, regional distributions, and
historical patterns when real data is unavailable or of insufficient quality.

Operating rules:
- Every synthetic output is flagged at indicator level — not at session or
  scenario level
- Mixed-mode outputs show per-indicator provenance
- Synthetic data produces scenario bands (pessimistic/realistic/optimistic),
  not point estimates
- Synthetic estimates are always Tier 3 or lower in the confidence tier system
- When uncertainty is so large the output is directionally meaningless, the
  tool says so rather than generating an uninterpretable band

This is what makes the democratization mission operationally real. A global
south finance ministry with thin, delayed, or unreliable data can still use
WorldSim — and the tool is honest about what it knows and what it inferred.

Synthetic data framework: Chief Methodologist consultation complete (PR #373).
Five-method hierarchy, three-condition meaninglessness threshold, MDA alert
tier table. ADR-007 forthcoming.
Confidence tier system: `docs/DATA_STANDARDS.md §Confidence Tier System`.

---

## UX Architectural Commitments

Five governing premises apply from M9 forward through Mode 3 introduction.
These are architectural commitments, not design preferences. Any UX proposal
that conflicts with them requires Engineering Lead sign-off.

1. **The primary viewport is the instrument cluster.** Context (choropleth,
   geographic view) is navigable. Instruments (trajectory view, PMM, MDA
   alerts, four-framework current position) are always visible without opening
   a drawer or navigating away.

2. **Instruments are always visible; context is navigable.** No primary
   instrument lives in a drawer, a tab, or behind a click. The four primary
   flight instruments are present in the primary viewport at all times in all
   three modes.

3. **The step axis is the shared frame for all instruments.** All instruments
   that show temporal data share a single step axis. This is the visual
   contract that makes multi-framework trajectory comparison legible.

4. **Each mode has its own primary cognitive task.** Mode 1 (Replay):
   trajectory reconstruction. Mode 2 (Simulation): threshold-safe path
   construction. Mode 3 (Active Control): real-time steering within human
   cost constraints. Instrument layout serves the cognitive task of the active
   mode.

5. **The control plane layout zone is reserved before the control plane is
   built.** Mode 3 requires a dedicated screen zone for control inputs. That
   zone is reserved in the layout from M9 onward — not retrofitted when Mode 3
   arrives.

Full UX first-principles derivation and stress-testing:
`docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md`

---

## The Simulation Framework

WorldSim is a flight simulator for national decision-making. The engine models
sovereign governance through six aviation-derived failure modes (The Spin,
Coffin Corner, Hypoxia, Backside of the Power Curve, Get-There-Itis, The CB
Cloud), an event-driven feedback graph with configurable hierarchical resolution
(nation → region → sector → demographic cohort), adaptive temporal resolution
that auto-switches to daily during crisis events, and simultaneous multi-currency
measurement across financial, human development, ecological, and governance
units. Hard Minimum Descent Altitudes define irreversible thresholds that no
recommended pathway may cross.

WorldSim operates in three interaction modes: Mode 1 (Replay), Mode 2
(Simulation), Mode 3 (Active Control). Mode 3 is the north star for instrument
design.

**Full detail:** `docs/architecture/simulation-framework.md`

---

## Key Use Cases

WorldSim targets six primary use cases: IMF/World Bank loan evaluation,
privatization sovereign resilience assessment, financial attack detection and
defense, scenario exploration and geopolitical stress testing, backtesting and
historical calibration, and emergency procedure generation.

**Persona-anchored acceptance tests for each use case:** `docs/ux/personas.md`
**Full use case descriptions:** `docs/architecture/simulation-framework.md §Key Use Cases`

---

## Data Sources

Approved sources by category: `docs/data-sources/approved-sources.md`

All sources must be registered in `source_registry` before their data is
loaded. Data quality tiers, provenance requirements, and backtesting integrity
rules: `docs/DATA_STANDARDS.md`.

---

## Agent Roster

All agents operating in this codebase must read
`docs/process/agents.md` before beginning any task.
This is mandatory reading alongside `SESSION_STATE.md`.
`agents.md` is the canonical home for all agent persona
definitions, activation protocols, independence requirements,
and RACI positions. Do not rely on memory of agent personas
from prior sessions — read the file.

All agents reference the relevant ADR before implementing any significant
feature. All agents treat the human cost ledger as a primary output,
never an afterthought.

---

## Domain Intelligence Council

A panel of nine domain intelligence agents, each speaking for one measurement
framework or cross-cutting analytical perspective. The council makes competing
interests explicit and visible — that adjudication is a human decision.

**Activation pattern:** `[Agent Name]: [SCENARIO|CHALLENGE|VALIDATE] — [topic]`

Full agent profiles, independence requirements, and operational agent definitions:
`docs/process/agents.md §Domain Intelligence Council`
Detailed domain profiles: `docs/agents/domain-intelligence-council.md`

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

M0–M12 complete (v0.1.0–v0.12.1). ADRs 001–012 current.
See GitHub Releases for full delivery history.

**Milestone 13 — Political Economy and Instrument Credibility (Current)**

*Primary objective (M13 exit gate):*
- ADR-013 authored and accepted — political economy module boundary
- Political economy module — conditionality modelling, elite capture dynamics, political feasibility constraints
- Alert panel UX (Zone 1B) — master-detail layout; ADR and frontend architecture review required before implementation (#852)
- Instrument legibility improvements — Demo findings DEMO-059–064 resolved
- Process Redesign Phase A deliverables

M13 closes when the political economy module is production-ready and instrument credibility meets first-class UX standards for negotiation-room use. Demo 5 is planned for M14.

Each milestone is a vertical slice — working software at every stage,
not infrastructure waiting for features.

---

## Milestone Roadmap

M0–M12 complete (v0.1.0–v0.12.1). M13 current. See GitHub Releases for full delivery history.

The full roadmap covering M13 through M14 — milestone deliverables, demo anchors, canonical users served, and the long-term resolution spectrum direction — is maintained at `docs/roadmap/worldsim-roadmap.md`. That document is the canonical reference. The summary below reflects current and next milestone only.

**Milestone 13 — Political Economy and Instrument Credibility (Current)**
Primary objective: ADR-013 (political economy module boundary), political economy module (conditionality, elite capture, political feasibility), alert panel UX (ADR required), instrument legibility improvements. No demo — Demo 5 at M14.

**Milestone 14 — Methodology Publication and External Validation (Next)**
Core deliverable: Methodology publication, external validation by domain experts, live stakeholder demo with real external participants (#843), Technical Steering Committee formation. Public launch infrastructure.

Full roadmap: `docs/roadmap/worldsim-roadmap.md`

---

## Architectural Principles for Claude Code Sessions

**Everything lives in GitHub.**
Code, tasks, documentation, ADRs, CI/CD configuration. One system of
record that both humans and agents can read and write. Issues follow a
strict three-level hierarchy (Epic → Feature Issue → Task Issue) with a
binary spawning rule: spawn children only when more than one agent or
more than one PR is required. No commits directly against Epics. Full
rule: `docs/process/agents.md §PM Agent — Issue Hierarchy`.

**No significant feature without an ADR.**
Architecture Decision Records document what was decided, why, and what
alternatives were considered. They are the institutional memory that
survives leadership changes — both human and AI session boundaries.

The Architecture Decision Record Backlog (`docs/architecture/backlog.md`) is the
single source of ADR number assignment. Before drafting any ADR, the Architect
Agent must: (1) check the backlog for the next available number, (2) mark the
entry ASSIGNED, (3) derive the panel composition from `docs/process/agent-raci.md`,
and (4) confirm the implementing agent is included in the panel. ADR numbers must
not appear in issue titles or documents before they are assigned from the backlog.

**File authority is non-negotiable.**
Before writing to any file, the acting agent must verify they hold R (Responsible)
on that file per `docs/process/agent-raci.md`. If another agent holds R, the acting
agent must produce a draft and request the owning agent's review before committing.
Writing directly to another agent's owned files without prior owner review is a
process violation equivalent to implementing a feature without an ADR. The file
ownership table is in `docs/process/agent-raci.md §File Ownership`.

**Blameless continuous improvement is non-negotiable.**
When something goes wrong — or almost goes wrong — the response is systemic, not personal.
WorldSim operates on Aviation Safety Management System principles: near-misses are
investigated with the same rigor as actual failures, because they are evidence that a
hazard exists and the defenses almost failed. The countermeasure is never "be more
careful." It is always "redesign the system so careful isn't required."

Every near-miss, process gap, or authority ambiguity that is identified — whether
reactive (caught after the fact) or anticipatory (sensed before a failure occurs) —
must be filed as an entry in `docs/process/near-miss-registry.md`. The registry records
what happened, what was at risk, what caught it, and what process improvement resulted.
Entries are permanent institutional memory — they are never deleted or minimized.

Agents do not assign blame. They identify root causes, build process improvements, and
document both. A near-miss that produces only a reminder to "be more careful" has not
been properly resolved.

**Known Issues are distinct from near-misses.**
A Known Issue is a confirmed limitation of external infrastructure or tooling
(GitHub Actions, third-party APIs, OS behaviour) that cannot be fixed by redesigning
internal processes. The response to a Known Issue is a documented workaround, not a
process improvement. Filing an external infrastructure failure as a near-miss produces
a process improvement recommendation against something that cannot be redesigned.

Rule: if the fix requires changing our own code, process, or documents → near-miss.
If the fix requires waiting for an upstream vendor → Known Issue.

Known Issues are filed in `docs/process/known-issues-registry.md`.

**PR merge gate — mandatory pause before next task.**
After opening any PR targeting `main`, Claude Code must stop all git operations
and file edits, report the PR URL, and explicitly hand off: *"Please merge when
CI is green and confirm back — I'll pull main before continuing."* No next task
begins, no files are edited, and no git commands run until the user confirms the
merge and Claude Code has executed `git pull origin main`.

**Exception — PRs targeting a release branch (`release/m{N}`).** Release branch
PRs are pre-authorized for autonomous merge. Claude Code polls `gh pr checks`
until the `changes` status check passes, then executes `gh pr merge <number>
--merge` and pulls from the release branch without waiting for user confirmation.
`release/m{N}` is an unprotected integration branch — admin bypass is not
required. See §Release Branch Workflow below.

**Exception — `SESSION_STATE.md`-only PRs.** End-of-session state updates that
touch only `SESSION_STATE.md` are pre-authorized for auto-merge. Claude Code will
poll `gh pr checks` until the `changes` status check passes, then execute
`gh pr merge <number> --admin --merge` and `git pull origin main` without waiting
for user confirmation. If the PR contains any file other than `SESSION_STATE.md`,
the standard gate applies regardless of the other file's content.

**Release Branch Workflow.**
Each milestone has a release branch (`release/m{N}`) cut from `main` at
milestone kickoff by the PM Agent as part of sprint planning. All feature work
during the milestone uses this pattern:

1. Cut feature branch from `release/m{N}`: `git checkout -b feat/g1-xxx release/m12`
2. Implement, run pre-push gates (lint, build), push feature branch
3. Open PR targeting `release/m{N}` (not `main`)
4. Poll CI; merge autonomously once `changes` passes: `gh pr merge <number> --merge`
5. Pull from release branch: `git pull origin release/m{N}`
6. Continue with next feature branch

At milestone close, EL performs one admin bypass: `release/m{N}` → `main`.
The release branch is never merged to `main` by Claude Code — that merge is
always the Engineering Lead's action.

`SESSION_STATE.md` updates during an active milestone target the release branch
and follow the same autonomous merge rule as above (no `--admin` needed since
the branch is unprotected). The auto-merge exception's `--admin` flag is needed
only when the PR targets `main`.

**Backend pre-push lint gate — mandatory before any `git push` touching Python files.**
Before pushing any branch that modifies files under `backend/`, run:
`cd backend && ruff check . && mypy app/`
Both must exit 0. `ruff check . --fix` resolves most I001/E501 violations automatically;
fix any remaining errors before pushing. CI is a confirmation, not a discovery mechanism.
Local ruff is pinned to the same version as CI (`ruff==0.7.2` in `requirements.txt`) —
there is no environment difference that would cause CI to catch what local missed.
Near-miss record: NM-016 (`docs/process/near-miss-registry.md`).

**Frontend pre-push build gate — mandatory before any `git push` touching files under `frontend/src/`.**
Before pushing any branch that modifies files under `frontend/src/`, run:
`cd frontend && npm run build`
Must exit 0. TypeScript errors are a compliance finding — 7 TS6133 errors accumulated across M10 PRs without detection because this gate did not exist. CI is a confirmation, not a discovery mechanism.
Near-miss record: SCAN-024 (M10 exit — TS6133 findings found at compliance scan, not at push time).

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

**ADR template — mandatory starting point for all new ADRs.**
From Phase 0 forward, all new ADRs must be authored using `docs/adr/template.md` as the
starting point. The template encodes Phase 0 traceability requirements: tier classification,
persona trace, UX implication statement, silent failure mode, asymmetry assessment, north
star test, and mission impact statement. An ADR that cannot satisfy all requirements for its
tier is not ready for acceptance. The Architect determines tier classification at ADR
initiation; the UX Designer sign-off is a hard precondition for Tier 1 acceptance — not a
post-acceptance formality.

**North Star Test (Process Gate)**

The founding document's north star question — "Does this decision make the tool more useful to
a finance minister sitting across from an IMF negotiating team, in that moment?" — is now a
formal process artifact, not only an aspiration. This process gate closes gap FD-1: the north
star test previously had no artifact form, no process home, and no named agent owner.

**North star test artifact form:**
A written assessment of ≤ one page that answers the north star question for a specific
deliverable: naming the finance minister scenario (country, context, negotiation moment),
the concrete capability being evaluated, and whether the capability changes what the minister's
team can argue at the table. The assessment must be specific — "improves situational awareness"
is not an answer. "The Zambian ministry analyst can now show that the Chinese bilateral lending
opacity is a Structural Absence Declaration, not a model gap, and cite this in the restructuring
session" is an answer.

**Process home:**
A north star test artifact is a required component of the sprint exit checklist for any sprint
whose primary deliverable is a user-facing capability. The artifact must be filed before the
sprint exit gate passes. It is part of the exit artifact, not a separate document. A sprint
that closes without a north star test artifact on its user-facing capabilities has not
completed its exit gate — PI Agent blocks exit gate confirmation until the artifact exists.

**Agent authority:**
- PI Agent holds R for ensuring the north star test artifact exists before a sprint exit gate
  passes. PI Agent does not author the assessment — PI Agent confirms its existence and that
  it is specific (not aspirational).
- Business PO holds R for authoring the north star test artifact, with input from the DIC
  agent most relevant to the capability being delivered.
- The north star test artifact for each Tier 1 ADR is Element P-7 of the persona trace
  (see `docs/adr/template.md §Persona and UX Traceability`). ADR-level north star tests
  are authored by the ADR panel; sprint-level north star tests are authored by the Business PO.

**What happens if the answer is "no":**
If the north star test assessment for a sprint deliverable cannot answer the question
affirmatively — if no concrete minister scenario is improved — the deliverable is not
mission-complete. PI Agent escalates to Engineering Lead for a scope decision: either the
scope is modified until the test can be answered, or the deliverable is reclassified as
infrastructure (Tier 3, which does not require a sprint-level north star test — only a
forward trace to the downstream capability that will eventually pass the test).

**Template reference:** `docs/adr/template.md §North Star Test` for ADR-level implementation.
**Phase 0 authority:** `docs/process/sprint-plans/process-redesign-phase0-sprint-entry.md §Output 3`.

---

**Agent Execution Lifecycle**

Every agent implementing a feature — regardless of role — operates within a five-step execution
lifecycle from "ADR accepted" to "sprint exit validated." This lifecycle closes the intent-to-
implementation gap that allowed DEMO4-001 and DEMO4-002 to reach a live demo with frozen outputs
despite "CI green" status. Phase 0 encoded traceability requirements into ADRs. Phase A makes
those requirements operative at implementation time: an ADR with a complete persona trace cannot
prevent a mission failure if the implementing agent ignores the trace at implementation time.

*Authority: `docs/process/sprint-plans/process-redesign-phaseA-sprint-entry.md`. Changes to this
section require Architect Agent review and EL endorsement.*

**The five steps:**

**Step 1 — Intent authorship** (before implementation begins)
The implementing agent authors an Implementation Intent document using
`docs/process/intent-template.md` and files it at
`docs/process/intents/ADR-NNN-YYYY-MM-DD-short-name.md`. The intent document derives the
implementation's observable application state from the ADR's persona trace and UX implication
statement elements. Completeness gate: the QA Lead must be able to write a test from the intent
document without reading any implementation code. An intent document the QA Lead cannot test
from is incomplete and blocks Step 2.

**Step 2 — Test authorship** (after intent authorship; before implementation begins)
The QA Lead writes tests from the intent document's acceptance criteria before any implementation
code is written. Tests are authored from observable application states — not from the
implementation interface. "CI passes" is not a test. "Zone 1B shows the top MDA alert text
without scroll at 1440×900 with the Greece 2012 fixture at step 4" is a test. The test file is
filed before the implementation PR opens. A test authored in the same session as the
implementation it covers has not satisfied this step.

**Step 3 — Implementation**
The implementing agent writes code to satisfy the intent document's acceptance criteria. An
implementation that is not verifiable against the intent document's observable application states
is not complete, regardless of CI status.

**Step 4 — Verify** (does output match intent?)
The implementing agent confirms the observable application state defined in the intent document
is present in the running application. This is a live-application observation — not a CI check.
The verification artifact is a named Playwright test result, a recorded screen observation, or
a referenced CI test that observes the live application state against the intent document's
acceptance criteria. The implementing agent produces the verification artifact before the PR is
marked ready for review.

**Step 5 — Validate** (does output serve the mission?)
The Business PO confirms the implementation serves the mission as stated in the ADR's north star
test (Element P-7) and the intent document. Validation is a user-need confirmation — not a
technical review. CI green is not validation. Validation criteria by work type:

- **Frontend feature:** Business PO opens the live application and confirms the named persona can
  reach the observable state within the ADR's time ceiling (P-4). Customer Agent provides Layer 3
  quality assessment (see §Layer 3 Quality Gate below) before the Business PO verdict is final.
- **Backend capability:** Business PO confirms via API response or application output that the
  analytical intent is satisfied — e.g., a commodity price shock produces reserve drawdown visible
  in the trajectory response.
- **Documentation:** Business PO confirms a non-author can navigate to the key finding from the
  document's entry point in under five minutes.
- **Analytics:** Business PO confirms the output changes what the persona can argue at the
  negotiating table — naming the specific argument and why it was unavailable before.

**Business PO Acceptance as Sprint Exit Gate:** A sprint does not close when issues are closed
and CI is green. A sprint closes when the Business PO has completed the Validate step for every
user-facing deliverable in the sprint. If the Business PO cannot validate, the Business PO
produces a rejection artifact (see below). Sprint exit is blocked until the rejection is resolved.

---

**When Verify or Validate fails — the Rejection Artifact**

If, at Step 4 (Verify) or Step 5 (Validate), the observable application state defined in the
intent document is absent or the mission validation fails, the finding produces a rejection
artifact. The rejection artifact is not an advisory — it blocks sprint exit.

**Rejection artifact requirements:**

1. **Named location:** `docs/process/rejections/REJECT-NNN-YYYY-MM-DD-short-description.md`
   where NNN is a sequential rejection number (zero-padded to three digits).
2. **Required contents:**
   - Source intent document (ADR reference + intent document path)
   - Which acceptance criterion failed
   - What the observable application state actually showed vs. what the intent document specified
   - Whether the gap is in the intent document (imprecise specification) or the implementation
     (implementation did not satisfy the intent)
   - Remediation scope — what must change and which step the implementing agent returns to
3. **Return to Step 1, not Step 3:** The implementing agent returns to Intent authorship, not
   Implementation. The intent must be re-examined before the implementation is corrected — a
   Verify failure is evidence that the intent-to-implementation chain had a gap, not that only
   the code needs fixing.
4. **Near-miss entry required:** Every rejection produces a near-miss registry entry filed by
   the PI Agent in the same session. A Verify or Validate failure is institutional evidence of a
   process gap and must not evaporate without a record.
5. **Sprint exit block:** The sprint cannot close, and no subsequent sprint group begins, until
   the rejection is resolved and the Business PO or implementing agent confirms the observable
   state is present.

**Business PO rejection exception path:** The Business PO produces the rejection artifact naming
the defect, the remediation scope, and the re-acceptance condition before any remediation begins.
The implementing agent must satisfy the re-acceptance condition before the sprint closes. A
Business PO rejection handled only via verbal correction — without a written rejection artifact —
has not been properly resolved. The written record prevents the same gap from appearing in the
next sprint.

---

**Layer 3 Quality Gate (FD-2)**

Every user-facing capability that ships through this lifecycle must pass the Layer 3 quality
gate at the Validate step. This closes gap FD-2: self-interpreting output quality previously
had no process owner. The Customer Agent now holds that ownership.

Layer 3 quality: the output tells the user what the number means — not only displays the number.
An alert showing "−2.1%" without labeling the indicator, direction's meaning, or crossed threshold
is a Layer 2 output. A Layer 3 output for the same data: "Reserve coverage has fallen 2.1 months
below the CRITICAL threshold. At current draw rate, full depletion occurs in 4 steps."

**Agent authority:**
- Customer Agent holds R for Layer 3 quality assessment for any capability serving Persona 2, 3,
  or 5. Customer Agent produces the assessment before the Business PO delivers the Validate verdict.
- Business PO holds R for the Validate step verdict; Customer Agent's Layer 3 finding is a
  required input to that verdict — not an optional consultation.
- A Validate step that proceeds without a Customer Agent Layer 3 finding for a Persona 2/3/5
  capability is a process violation. PI Agent blocks sprint exit confirmation if absent.

**Trigger:** Any implementation that introduces or modifies a user-facing indicator label, alert
text, output narrative, or confidence tier disclosure. Does not apply to infrastructure work with
no direct user-visible output.

---

**Kryptonite Design Constraint (FD-3)**

This closes gap FD-3: the founding document's kryptonite frame — "on the side of the finance
ministry team with three economists, not the IMF side with one hundred" — previously had no
operational form in the execution lifecycle. It is now a concrete tradeoff rule applied at the
Intent authorship step and enforced at the Validate step.

**The constraint:** When authoring an intent document, if there is a tradeoff between:
- Analytical depth vs. interpretability in the Reactive entry state (90-second ceiling)
- Model sophistication vs. data accessibility at Tier 3 data environments
- Output richness vs. 90-second retrieval for Persona 2

Choose the option that serves the finance ministry team. The test: could the ministry team with
three economists use this output to make a specific argument at the table, or does it require
specialist mediation that the creditor side can provide and the ministry side cannot?

**Application in Step 1 (Intent authorship):** Section 5 of the intent template (Kryptonite
Constraint Check) is a required gate at authorship. An intent document with Section 5 unchecked
is incomplete and blocks Step 2.

**Application in Step 5 (Validate):** A Validate step that passes despite the Customer Agent
identifying required specialist mediation — without an EL exception recorded — is a process
violation. "This is as simple as the domain allows" does not satisfy the kryptonite constraint.
The constraint is satisfied when: the output is interpretable by a finance ministry economist
without further translation, or the required mediation is documented as an accepted asymmetry
gap with EL approval and a forward trace to a Layer 3 improvement.

**Authority:** `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md §Gap FD-3`.
**Phase 0 origin:** `docs/process/sprint-plans/process-redesign-phase0-exit.md §Part III`.

---

**Observable Application State — architectural definition**

An observable application state is a state of the running application — in the UI, the API, or
the database — confirmable by an agent other than the implementor using only external observation
(Playwright, curl, direct API call), without reading implementation source code.

Not observable application state:
- "CI passes" / "tests are green"
- "The function returns the correct result"
- "The feature is wired correctly"

Observable application state:
- "Zone 1B shows the top MDA alert text without scroll at 1440×900 with the Greece 2012 fixture
  loaded at step 4"
- "GET /api/v1/scenarios/{id}/trajectory returns `reserve_coverage_months` as a non-null float
  for each of 8 steps when the Jordan entity is loaded"
- "The PMM in Zone 1A displays 1.30 at step 3 when fiscal_multiplier=1.30 was set in the
  scenario configuration"

Test for a statement: can a QA reviewer confirm it by running the application, with no knowledge
of the implementation? If no — revise until yes.

---

**Lifecycle canonical document locations:**

| Artifact | Canonical location | Authored by |
|---|---|---|
| Intent document template | `docs/process/intent-template.md` | Architect Agent |
| Implementation Intent documents | `docs/process/intents/ADR-NNN-YYYY-MM-DD-short-name.md` | Implementing agent (per ADR panel) |
| Rejection artifacts | `docs/process/rejections/REJECT-NNN-YYYY-MM-DD-short-description.md` | Implementing agent or Business PO |
| Phase A exit artifact | `docs/process/sprint-plans/process-redesign-phaseA-exit.md` | PM Agent + PI Agent |

**Self-attestation limitation (documented):** The Verify step (Step 4) depends on the
implementing agent executing it honestly. The Business PO Validate step (Step 5) and the sprint
exit gate provide external verification that compensates for this risk but does not eliminate it.
Future tooling may automate observable state verification against fixture scenarios; until then,
the three-level structure (self-verify → Business PO validate → sprint exit artifact) is the
mitigation. This limitation is recorded in `docs/process/sprint-plans/process-redesign-phaseA-exit.md
§Known Limitations`.

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
| ADR Panel Reviews | `docs/adr/reviews/` | `ADR-NNN-panel-review.md` | New file per ADR; one review per ADR number |
| Module Capability Registry | `docs/scenarios/module-capability-registry.md` | Single file | Updated in place with each milestone |
| Near-Miss Registry | `docs/process/near-miss-registry.md` | Single file — append NM entries only | Append only; never insert mid-registry |
| Known Issues Registry | `docs/process/known-issues-registry.md` | Single file — append KI entries only | Append only; never insert mid-registry |
| Internal Demo Reviews | `docs/demo/{milestone}/reviews/` | `YYYY-MM-DD-vX.X.X-internal-review.md` | New file per demo cycle (even-numbered milestones) |
| Independent Review (IR) | `docs/demo/{milestone}/reviews/` | `YYYY-MM-DD-vX.X.X-ir-review.md` | Pre-demo quality gate; authored by Independent Review Agent (Step 7); distinct from internal-review.md. EL decision 2026-06-10. |
| Stakeholder Reviews | `docs/demo/{milestone}/reviews/` | `YYYY-MM-DD-vX.X.X-stakeholder-review.md` | Post-demo artifact; authored after the live stakeholder demo runs; captures attendees, questions raised, and outcome. A placeholder with templated sections is created at milestone close and filled in after the demo. EL decision 2026-06-10. |
| Security Review Reports | `docs/compliance/security-reviews/` | `YYYY-MM-DD-security-review-[topic].md` | New file per review; authored by Security & Review Agent; topic is a short kebab-case label (e.g., `dual-use-financial-attack-surface`) (Issue #528) |

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

## Milestone Exit Ceremony

Every milestone exit must complete the following steps in order before the exit checklist issue is closed. Each step is a named, mandatory gate — not a suggestion. The retrospective (§Milestone Retrospective Process) is also required and follows these steps.

**Step 1 — Open issue audit (GitHub)**
Run `gh issue list --milestone "Milestone {N}..."` and confirm that only the exit checklist issue remains open. Every other issue must be explicitly dispositioned — migrated to a future milestone, closed as delivered, or closed with won't-fix rationale — before the exit checklist closes. A milestone that closes with unexplained open issues has not completed its exit ceremony.

**Step 2 — Milestone reference audit**
Update the following three documents in the same PR as the exit SESSION_STATE update. They must not be deferred to a follow-up PR:
- `README.md` — release badge, development status table row for the closing milestone, any stale axis/module descriptions
- `CLAUDE.md` — "What We Are Building First" and "Milestone Roadmap" sections: current → closed, next → current
- `docs/roadmap/worldsim-roadmap.md` — milestone registry table (closing milestone → Complete; new milestone → Current); "Where We Are" narrative; current milestone section heading (`*(current)*` → `*(complete)*`); new milestone section added if absent

The roadmap has an explicit currency policy ("updated at every milestone close"). This step is the enforcement mechanism for that policy. M10, M11, M11.5, and M12 all closed without this step — the gap was caught at M13 kickoff and required PR #896 to repair. Near-miss: NM-041.

**Step 3 — SESSION_STATE internal consistency check**
Before committing the exit SESSION_STATE update, verify all four of the following:
- [ ] All issue milestone dispositions in the disposition summary match their actual GitHub milestone assignments (run `gh issue view #{N}` to spot-check)
- [ ] The exit checklist issue for the *new* milestone (M{N+1}) is listed in the Open Issues — M{N+1} table with `immediate | M{N+1} gate issue` notation
- [ ] No stale status notes remain (e.g., "EL endorsement is next required action" after the endorsement was recorded; "active work stream" entries for work that completed mid-milestone)
- [ ] Parallel-track relationships (e.g., Process Redesign phases) explicitly state whether they are blocking prerequisites or concurrent tracks for the new milestone

**Step 4 — Fresh session continuity test**
After all exit PRs are merged and main is current, run the fresh session test: reading *only* SESSION_STATE.md and CLAUDE.md, ask — "if a new Claude Code session opened tomorrow and was asked to kick off M{N+1}, what wrong assumptions would it make or what dependencies would it miss?" Fix any critical or high gaps in a SESSION_STATE-only PR before declaring the exit ceremony complete. This step is complete only when the test produces no critical or high findings.

**The exit ceremony is the last action of the milestone.** It runs after all feature work is merged, after the release branch is merged to main, after the demo cycle (for even-numbered milestones) is complete, and after the retrospective. It is not a side task to be delegated to a follow-up session.

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
