# CLAUDE.md — WorldSim Project Context

> Last significant revision: 2026-06-26
> Updated against: M17 close — Calibration and Comparative Infrastructure complete; Wave 1 CM calibration (fiscal-to-cohort elasticity, governance sensitivity) delivered; Wave 2 N=3 multi-scenario, DEMO6 CRITICAL polish, adaptive y-axis, Zone 1B proportional allocation (ADR-018), GovernanceModule institutional_capacity_index all delivered; M18 now current
> Previous version context: 2026-06-25 — M16 closed; M17 active; DEMO6 findings (001–049) retained as Demo 7 specification foundation

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
4. `docs/insights-log.md` — pre-GitHub inbox; findings, open questions, and insights not yet promoted to issues or near-miss entries

`CLAUDE.md` is the permanent constitution. `SESSION_STATE.md` is the
current situation report. `docs/process/agents.md` is the canonical home
for all agent personas. All four are required reading at session start.

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

### Entry and Exit Invariants

*Authority: Phase D of the Process Redesign Sequence (2026-06-12).
Changes to this section require PI Agent review and EL endorsement.*

**Sprint entry invariant — implementation may not begin without a filed, EL-approved entry document.**

The PM Agent may not authorize implementation to begin — and no implementing agent may open an implementation PR — without a sprint entry document filed and EL-approved. The document must satisfy all five entry conditions in `docs/process/sprint-planning-sop.md §Sprint Entry Gate`. If implementation begins without a complete entry document, the PI Agent files a near-miss in the same session — not after the sprint closes — regardless of whether implementation ultimately succeeds.

This is a hard stop, not guidance. An implementation PR opened before the entry document is filed and EL-approved is a process deviation of the same severity as pushing code without running the pre-push lint gate.

Template: `docs/process/sprint-plans/templates/sprint-entry-template.md`
Reference: `docs/process/sprint-planning-sop.md §Sprint Entry Gate`

**Sprint exit invariant — a sprint does not close when issues are closed and CI is green.**

A sprint closes when:
1. Business PO acceptance is recorded for every user-facing deliverable (ACCEPT verdict or EL exception on record)
2. Customer Agent Layer 3 assessment is on record for any deliverable serving Personas 2, 3, or 5
3. No open rejection artifacts remain unresolved
4. PI Agent confirms all exit conditions are satisfied and records confirmation in the sprint exit document

CI green and issue closure are necessary but not sufficient. The PI Agent blocks sprint exit confirmation until all conditions are met. A sprint that closes with outstanding rejections or missing Business PO verdicts has not exited — it has been abandoned without a record.

Template: `docs/process/sprint-plans/templates/sprint-exit-template.md`
Reference: `docs/process/sprint-planning-sop.md §Sprint Exit Gate`

**"If it isn't written down, it doesn't exist."**

An intent document that exists in session context but has not been filed at `docs/process/intents/` does not satisfy the entry gate. A Business PO verdict delivered verbally but not as a filed artifact does not satisfy the exit gate. A sprint entry document that exists as a draft but has not been committed and referenced in `SESSION_STATE.md` does not satisfy the entry gate.

These gates are satisfied by artifacts in the repository — not by session memory, not by agent confidence that the conditions are met, and not by knowledge that the equivalent work was done informally. If the artifact does not exist in the repository, the condition is not satisfied.

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

All agents must read `docs/process/agents.md` before beginning any task — canonical home for all agent personas, activation protocols, independence requirements, and RACI positions. Never rely on session memory of agent personas. All agents reference the relevant ADR before implementing any significant feature and treat the human cost ledger as a primary output.
---

## Domain Intelligence Council

Full agent profiles, independence requirements, and operational agent definitions: `docs/process/agents.md §Domain Intelligence Council`
**Activation pattern:** `[Agent Name]: [SCENARIO|CHALLENGE|VALIDATE] — [topic]`

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

---

## What We Are Building First

M0–M17 complete (v0.1.0–v0.17.0). ADRs 001–018 current.
See GitHub Releases for full delivery history.

**Milestone 17 — Calibration and Comparative Infrastructure (Complete)**

Delivered: Wave 1 CM calibration — ELASTICITY_REGISTRY revised (Fosu 2011 SSA LIC, #1229), governance sensitivity spec on record (#1248), FRAME-D milestone sentence fires within 8-step Demo 6 window. Wave 2 — N=3 multi-scenario comparison (#394), Zone 1B proportional allocation (ADR-018, #1252), DEMO6 CRITICAL polish (#1249/#1250/#1253/#1239), adaptive y-axis extension (#1251), GovernanceModule institutional_capacity_index (Gupta 2002, −0.015 T3, #1275), governance horizon disclosure (#1276), SOP UX/UI design artifact gate (#1277). SCAN-027 clean.

**Milestone 18 — Full Argument and Demo 7 (Current)**

Core deliverable: Demo 7 (Senegal Mode 3 active control + Zambia three-scenario comparison, live external session #843). Counter-scenario comparison infrastructure; CI bands on Zone 1A trajectories (ADR-007 full implementation); PSP driver decomposition.

Demo 7 at M18 close.

Each milestone is a vertical slice — working software at every stage,
not infrastructure waiting for features.

---

## Milestone Roadmap

M0–M17 complete (v0.1.0–v0.17.0). M18 current. See GitHub Releases for full delivery history.

The full roadmap covering M18 and beyond — milestone deliverables, demo anchors, canonical users served, and the long-term resolution spectrum direction — is maintained at `docs/roadmap/worldsim-roadmap.md`. That document is the canonical reference. The summary below reflects current and next milestone only.

**Milestone 17 — Calibration and Comparative Infrastructure (Complete)**
Delivered: Wave 1 CM calibration (fiscal-to-cohort elasticity #1229, governance sensitivity #1248, FRAME-D gate); Wave 2 — N=3 multi-scenario (#394), Zone 1B proportional allocation ADR-018 (#1252), DEMO6 CRITICAL polish (#1249/#1250/#1253/#1239), adaptive y-axis (#1251), GovernanceModule institutional_capacity_index (#1275), governance horizon disclosure (#1276), SOP UX/UI gate (#1277). SCAN-027 clean.

**Milestone 18 — Full Argument and Demo 7 (Current)**
Core deliverable: Demo 7 (Senegal Mode 3 + Zambia three-scenario, live external session #843). CI bands on Zone 1A trajectories (ADR-007 full); PSP driver decomposition; counter-scenario comparison.

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
PRs are pre-authorized for autonomous merge. Immediately after opening the PR,
set auto-merge: `gh pr merge <number> --merge --auto`. GitHub monitors CI and
merges the PR the moment all required checks pass — no polling loop, no GraphQL
quota consumption. If CI fails, `ci-failure-notify.yml` posts a comment and the
auto-merge is abandoned; stop and report to the user.
To observe CI output in real time (e.g. to diagnose a failure), use
`gh run watch <run-id> --exit-status` — a single streaming connection, not a
polling loop. Obtain the run ID with:
`gh run list --branch <branch> --limit 1 --json databaseId --jq '.[0].databaseId'`
`release/m{N}` branches are protected by the `release-branch-ci-gate` Ruleset —
a failed required check will block the merge at the server regardless.
See §Release Branch Workflow below.

**Exception — `SESSION_STATE.md`-only PRs targeting `main`.** End-of-session
state updates that touch only `SESSION_STATE.md` and target `main` are handled
automatically by the `auto-merge-session-state` GitHub Actions workflow
(`.github/workflows/auto-merge-session-state.yml`). Claude Code must open the
PR and then stop — do not poll, do not call `gh pr merge`, do not use `--admin`.
The workflow verifies that `SESSION_STATE.md` is the only changed file, then
calls `gh pr merge --auto --squash`. All CI jobs are skipped for root-file-only
changes; GitHub branch protection treats skipped as passing. If the PR contains
any file other than `SESSION_STATE.md`, the standard gate applies — the workflow
will not fire and EL must merge manually.

**Release Branch Workflow.**
Each milestone has a release branch (`release/m{N}`) cut from `main` at
milestone kickoff by the PM Agent as part of sprint planning. All feature work
during the milestone uses this pattern:

1. Cut feature branch from `release/m{N}` using a **milestone-scoped name**:
   `git checkout -b feat/m{N}-g{N}-short-description release/m{N}`
   The branch name must contain the milestone prefix (e.g. `m14`). Sprint group
   numbers (G1, G2, …) are reused across milestones — `feat/g1-bugs` is ambiguous
   and will be rejected by the `branch-naming` CI check. Use `feat/m14-g1-bugs`.
2. Implement, run pre-push gates (lint, build), push feature branch
3. Open PR targeting `release/m{N}` (not `main`)
4. Set auto-merge immediately after opening the PR:
   `gh pr merge <number> --merge --auto`
   GitHub merges when all required checks pass. The agent does not poll or wait —
   move on to the next task or close the session. To observe CI in real time:
   `gh run watch $(gh run list --branch <branch> --limit 1 --json databaseId --jq '.[0].databaseId') --exit-status`
5. Pull from release branch before starting the next feature branch:
   `git pull origin release/m{N}`
6. Continue with next feature branch

At milestone close, EL performs one admin bypass: `release/m{N}` → `main`.
The release branch is never merged to `main` by Claude Code — that merge is
always the Engineering Lead's action.

`SESSION_STATE.md` updates during an active milestone target the release branch,
not `main`, and follow the same autonomous merge rule as all release branch PRs:
set auto-merge immediately after opening the PR (`gh pr merge <number> --merge --auto`).
No `--admin` needed — the `release-branch-ci-gate` Ruleset treats skipped checks
as passing, and GitHub's auto-merge fires the moment all checks are terminal.
The `auto-merge-session-state` workflow only fires on PRs targeting `main` and
does not apply here.

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

**UX Designer sign-off — structured attestation required (NM-042).**
The UX Designer sign-off block in every ADR requires four named fields: Reviewing agent,
Session context, Governing documents reviewed (named sections — not generic references),
and Concerns found (explicit count or "None"). A checkbox without all four fields is
non-compliant — treat it as unsigned.

The `Session context` field has two valid values:
- `Separate session, EL-triggered YYYY-MM-DD` — independence is structurally asserted; EL
  accepts at face value.
- `Same session as ADR authorship — acknowledged` — the analog to initialing "per: [delegate]"
  on a paper form. Disclosed same-session review is permitted; undisclosed same-session review
  is a process violation equivalent to a missing sign-off.

**A sign-off marked `Same session as ADR authorship — acknowledged` requires the EL to verify
governing document citations in the sign-off text before accepting.** Generic references
("governing premises", "first principles") do not satisfy the citation requirement. Named
sections (`information-hierarchy.md §1B`, `north-star.md §Primary Cognitive Tasks`) do.

**Absence of a `Session context` declaration is a non-compliant sign-off.** Treat it as
`Same session as ADR authorship — acknowledged` until a properly declared review is obtained.
PI Agent holds R for flagging non-compliant sign-offs before the acceptance vote passes.

Near-miss authority: NM-042 (`docs/process/near-miss-registry.md`).

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

**PM Agent — Insights Log Obligation**

`docs/insights-log.md` is the project's pre-GitHub inbox: a permanent append-only artifact
for findings, open questions, and insights that arise in agent deliberations or EL observations
but are not yet ready to become GitHub issues or near-miss entries.

At each HORIZON sweep, the PM Agent must:

1. Read all entries in `docs/insights-log.md` with status `open`
2. For each open entry, determine whether it is ready to promote or resolve:
   - **Promote:** File a GitHub issue or near-miss entry; update the log entry status to
     `promoted → #NNN` (issue) or `promoted → NM-NNN` (near-miss)
   - **Resolve:** If the finding is no longer actionable or was addressed informally, update
     status to `resolved — [reason]`
   - **Hold:** If still open and not yet actionable, leave status `open` — no action required,
     but the sweep must confirm the decision explicitly
3. Record in the HORIZON sweep output (sprint plan §HORIZON table) that the insights log was
   reviewed and state the count of open entries reviewed and dispositioned

New entries are added to `docs/insights-log.md` at any point by any agent or the EL when a
finding arises in deliberation or observation. Adding to the log does not require a PR — it is
appended in the same commit as the work that produced the finding.

**File authority:** EL holds R on `docs/insights-log.md` for additions; PM Agent holds R for
promotion and resolution updates at HORIZON sweep time.

---

**Agent Execution Lifecycle**
See `docs/process/agent-execution-lifecycle.md` for the five-step implementation lifecycle (intent authorship → test authorship → implementation → verify → validate), rejection artifact requirements, Layer 3 quality gate, kryptonite design constraint, and observable application state definition.

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
| Exceptions Registry | `docs/compliance/exceptions.md` | Single file — append EX entries only | Append only; never insert mid-registry. Types: threshold, architecture, security, process, data. Every entry requires an expiry condition. Expired unrenewed exceptions are compliance findings. |
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

See `docs/process/milestone-exit-sop.md` for the four mandatory exit ceremony steps and retrospective requirements. **The exit ceremony is the last action of the milestone.**

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
