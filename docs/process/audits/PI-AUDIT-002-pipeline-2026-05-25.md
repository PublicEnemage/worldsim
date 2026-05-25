# PI-AUDIT-002 — End-to-End Feature Delivery Pipeline

**Date:** 2026-05-25
**Conducted by:** Process Integrity Agent
**Scope:** Complete pipeline from functional intent inception to demo delivery
**Related:** PI-REVIEW-001 (agent team audit, 2026-05-25); Issues #521–#529

---

## 1. Scope and Method

This audit traces the complete lifecycle of a piece of functional intent through the WorldSim delivery pipeline: from first surfacing through prioritization, ADR review, implementation, testing, milestone closure, and demo. It is an anticipatory audit — no single near-miss triggered it, but the project is entering M10 (its first major instrument-cluster implementation sprint) and process robustness now matters more than at any prior milestone.

**Source documents read before any findings were recorded:**

| Document | Lines | Key scope |
|---|---|---|
| `CLAUDE.md` | — | Constitutional rules and principles |
| `SESSION_STATE.md` | — | Current work streams |
| `docs/MILESTONE_RUNBOOK.md` | 598 | Milestone ceremony, exit checklist, governance cadence |
| `docs/roadmap/worldsim-roadmap.md` | 209 | M9–M13 deliverables and demo anchors |
| `docs/architecture/backlog.md` | 71 | ADR number assignment queue |
| `docs/vision/worldsim-founding-document.md` | 329 | Foundational purpose — pipeline frame |
| `docs/CODING_STANDARDS.md` | 1832 | Commit format, testing, AC taxonomy |
| `docs/CONTRIBUTING.md` | 950 | Agent workflow, PR process |
| `docs/process/agents.md` | 1141 | Agent roster, personas, activation, RACI |
| `docs/process/agent-raci.md` | 604 | Decision types, file ownership, interaction patterns |
| `docs/process/near-miss-registry.md` | 1408 | NM-001 through NM-022 |
| `docs/adr/ADR-001` through `ADR-008`, `ADR-010` | — | Full ADR library |
| `docs/adr/reviews/ADR-007/008/010-panel-review.md` | — | Panel review artifacts |

**What this audit does not do:** It does not evaluate whether any individual agent performed their role correctly. It evaluates whether the process is designed to produce correct outcomes reliably. Blameless by construction.

---

## 2. Pipeline Stage Map

The following map reflects the pipeline as actually documented. Each stage is reconstructed from the source documents. Gaps are noted inline and developed in Section 3.

### Stage 1 — Intent Surfacing

Functional intent enters the pipeline through one of five documented channels:

1. **EL vision** — Engineering Lead identifies a strategic need directly and files an Epic or Feature Issue.
2. **PM HORIZON sweep** — PM Agent runs a 6-step horizon scan (surfacing latent needs, gap analysis against roadmap, DIC consultation, prioritization input). Documented in `docs/process/agents.md §PM Agent`.
3. **DIC session** — A Domain Intelligence Council agent raises a gap via `[Agent]: SCENARIO|CHALLENGE|VALIDATE — [topic]`. The Council Orchestrator synthesizes and escalates to PM.
4. **Customer Agent AUDIT** — Customer Agent audits a use-case cluster and identifies Layer 1 (terminology), Layer 2 (information architecture), or Layer 3 (institutional capacity) gaps. Layer 3 gaps are the primary source of pipeline-worthy intent.
5. **Near-miss process improvement** — A filed near-miss entry generates a system redesign recommendation that becomes functional intent (e.g., NM-014 → AC taxonomy requirement, NM-019 → kickoff gate).

**Not documented:** The triggering cadence for PM HORIZON sweeps. Agents.md describes what the sweep does but not when or how often it is run. See `F-PIPELINE-3`.

### Stage 2 — Prioritization and Issue Creation

**PM TRIAGE** produces one of four verdicts: Build Now / Defer / Reject / Need Info.

**Issue hierarchy** (PM Agent §Issue Hierarchy):
- Epic → Feature Issue → Task Issue
- Spawn children only when more than one agent or more than one PR is required
- No commits directly against Epics

Feature Issues must include: a Closes link to the parent Epic; a rough scope estimate; the ADR number if one is required.

**Kickoff gate (NM-019 response):** PM performs a scope-completeness check before the first implementation issue is spawned. This is documented and enforced by convention.

**Not documented:** How PM distinguishes between a feature that requires a new ADR vs. an amendment to an existing ADR vs. no ADR at all. The "significant feature" threshold is left to PM/EL judgment with no written criteria. See `F-PIPELINE-1` (generalized from the small-feature handoff gap).

### Stage 3 — ADR Process

1. **Architect checks Architecture Backlog** (`docs/architecture/backlog.md`) for next available ADR number and marks it ASSIGNED.
2. **Panel composition** derived from `docs/process/agent-raci.md` — the 9 decision types map to R/A/C/I agents; implementing agent always required.
3. **Architect drafts ADR** — required sections: Status, Context, Decisions, Alternatives Considered, Consequences, Panel, Architecture License.
4. **Generative consultation:** agents are activated and consulted *before* framing, not after the draft is complete.
5. **Panel review** — each agent produces ACCEPT / REJECT / INCORPORATE / DEFER findings; Architect incorporates INCORPORATE items; EL resolves conflicts and accepts.
6. **Panel review artifact** committed to `docs/adr/reviews/ADR-NNN-panel-review.md`.

**Not documented:** An explicit algorithm for deriving panel composition from RACI tables when a feature spans multiple decision types simultaneously. The rule says "derive from agent-raci.md" but doesn't specify how to resolve conflicts when a feature touches Architectural + Domain/measurement + UX component decision types at once. See `F-ADR-8`.

### Stage 4 — Stories, Acceptance Criteria, and Test-First Gate

**PO Agent** writes user stories before implementation begins. This is the non-negotiable gate.

**AC taxonomy (NM-017 response):**
- **Type 1 AC:** Observable system behavior (widget displays value, latency ≤ 500ms) — verified by automated test.
- **Type 2 AC:** Human judgment required (adequacy, appropriateness) — verified by structured review session with documented outcome.

Stories and tests must be committed before the first implementation PR is opened. This is documented in `docs/CODING_STANDARDS.md §Testing Requirements`.

**Backtesting obligation:** For any new indicator or composite score, a backtesting case must be registered per ADR-005 Decision 5 protocol (4 files: case definition, fixture data, expected outcomes, audit trail). See `F-ADR-9`.

### Stage 5 — Implementation

**File authority gate (CLAUDE.md §Architectural Principles):**
Before writing to any file, the acting agent verifies R (Responsible) from `docs/process/agent-raci.md §File Ownership`. Cross-ownership features require multi-agent coordination.

**Pre-PR checklist (CODING_STANDARDS.md):**
- [ ] Issue exists with Closes #N
- [ ] File authority verified for each file
- [ ] Cross-ADR impact enumerated (which ADRs does this PR touch?)
- [ ] Backend: `ruff check . && mypy app/` passes
- [ ] Schema files updated in same commit if schema changes made

**Not documented:** The cross-ADR impact check has no artifact. It is a mental checklist in the PR description with no required field. For features touching 3+ ADRs simultaneously, there is no template enforcing enumeration. See `F-PIPELINE-4`.

### Stage 6 — Testing and Quality Gates

Four testing tiers are required:

1. **Unit tests** — every public method; `Decimal` arithmetic invariants; human cost ledger outputs tested explicitly.
2. **Integration tests** — endpoint tests against real database (not mocked, per NM-013 pattern).
3. **Backtesting suite** — must pass before any merge touching the simulation engine.
4. **Playwright sequence** (ADR-006 Decision 12) — 4 phases for frontend changes:
   - Phase 1: Component isolation
   - Phase 2: Full render cycle (advance step → instrument updates)
   - Phase 3: Mode transition safety
   - Phase 4: Performance envelope (render budget)

The Playwright sequence is a PR review discipline requirement, not CI-enforced. See `F-ADR-3`.

### Stage 7 — Milestone Ceremony

**Milestone creation** (MILESTONE_RUNBOOK.md §Creation Ceremony):
1. Create GitHub milestone object
2. File auto-exit-checklist issue against milestone
3. File scope definition issue with PM scope-completeness check (kickoff gate)

**Milestone exit** (7 steps):
1. All exit-checklist items green
2. Compliance scan (append to `docs/compliance/scan-registry.md`)
3. Frontend smoke test (per `docs/frontend/testing-standards.md`)
4. Socratic Agent TEST session on milestone architecture
5. Release tag (vX.Y.0)
6. CHANGELOG entry
7. Next milestone creation ceremony

### Stage 8 — Demo

The roadmap defines demo anchors for each milestone. A demo requires:
- A working scenario with real fixture data (not synthetic-only)
- Human cost ledger visible alongside financial indicators
- Methodology transparency visible (confidence tiers, blindspot disclosure)

**Not documented:** Who holds R on the demo end-to-end. The roadmap names demo anchors but does not assign an owner. See `F-AGENTS-2`.

---

## 3. Findings

Findings are classified by severity:

- **Critical** — process gap that could produce a governance violation, data integrity failure, or undetectable error if triggered.
- **Major** — gap that will predictably cause rework, confusion, or process violation under normal M10 conditions.
- **Minor** — stale documentation or low-probability ambiguity; clarification recommended.

### F-RUNBOOK-1 — MILESTONE_RUNBOOK.md Milestone Table Stale

**Severity:** Minor
**Source:** `docs/MILESTONE_RUNBOOK.md §Milestone Definition Table`
**Observation:** The table lists M1 as "In Progress" and M2–M4 as "Upcoming." The project is at M9 exit / M10 creation. The table has not been updated since initial authoring.
**Risk:** A new agent or contributor reading MILESTONE_RUNBOOK.md as required session reading receives a false picture of project state.
**Recommended action:** Update table to reflect M1–M9 as complete, M10 as current. Assign PM Agent R for this update.
**GitHub issue:** to be filed — see Section 5.

---

### F-CONTRIB-1 — CONTRIBUTING.md "Branch from develop" Contradicts Practice

**Severity:** Major
**Source:** `docs/CONTRIBUTING.md §Branch Discipline`
**Observation:** CONTRIBUTING.md instructs contributors to "Branch from develop, not main." The project operates entirely on main. CLAUDE.md PR merge gate specifies `git pull origin main`. SESSION_STATE.md shows all branches target main. No `develop` branch exists.
**Risk:** A new contributor (human or agent) following CONTRIBUTING.md literally would try to branch from `develop`, find it doesn't exist, and be blocked or create an incorrect base. This is the most actively misleading stale document in the repository.
**Recommended action:** Update CONTRIBUTING.md to specify `main` as the base branch. File near-miss entry (see NM-023).
**GitHub issue:** to be filed — see Section 5.

---

### F-AGENTS-1 — IB and DQ Agents Remain Proposed Past M9 Target

**Severity:** Major
**Source:** `docs/process/agents.md §Proposed Agents`; Issue #299 (IB), Issue #300 (DQ)
**Observation:** Both the Integration Bridge Agent (IB) and Data Quality Agent (DQ) had "target activation: M9 Standards Foundation" in agents.md. M9 has now exited to human-gate phase without activating either. Issues #299 and #300 are still open.
**Risk:** M10 includes schema-intensive implementation (trajectory endpoint, api_contracts.yml registration, Quantity field extensions for ADR-007). The DA currently holds both design and quality-checking responsibilities, which conflicts with the DQ independence requirement ("not the same agent who designed the standard").
**Recommended action:** File M10 scope-blocking issue to complete IB and DQ definitions before first implementation issue spawns. Already tracked as Issue #523 from PI-REVIEW-001.
**GitHub issue:** existing #523.

---

### F-AGENTS-2 — No Single Agent Owns Demo Story End-to-End

**Severity:** Major
**Source:** `docs/roadmap/worldsim-roadmap.md §Demo Anchors`; `docs/process/agents.md`; `docs/process/agent-raci.md §File Ownership`
**Observation:** The roadmap defines demo anchors for M10 (Demo 3) and M11 (Demo 4). No agent is listed as R (Responsible) for demo preparation, demo script, or demo delivery in agent-raci.md. The PM Agent holds R on roadmap/; the Customer Agent holds R on docs/customer/ — but neither owns the demo artifact.
**Risk:** Approaching M10 exit, no process-defined owner means demo prep is the first thing cut under time pressure. The demo is the primary external validation mechanism for the project's mission.
**Recommended action:** Designate a single agent (PM Agent is the natural owner) as R on demo preparation per milestone. Add to agent-raci.md File Ownership table. File GitHub issue.
**GitHub issue:** to be filed — see Section 5.

---

### F-PIPELINE-1 — "Significant Feature" ADR Threshold Is Undocumented

**Severity:** Major
**Source:** `CLAUDE.md §Architectural Principles`; `docs/CODING_STANDARDS.md §ADR Standards`; `docs/process/agents.md §PM Agent`
**Observation:** CLAUDE.md states "No significant feature without an ADR." Neither CLAUDE.md nor CODING_STANDARDS.md defines "significant." The PM Agent section describes the TRIAGE process but does not give criteria for "this requires an ADR" vs. "this can proceed as an amendment" vs. "this can proceed without any ADR."
**Risk:** Two failure modes. Mode 1: Agent determines a feature doesn't need an ADR, implements it, and it turns out to constitute a significant architectural decision that should have been reviewed. Mode 2: Agent concludes everything needs an ADR, creating ADR-process overhead for routine implementation work, choking throughput.
**Recommended action:** Document explicit criteria in MILESTONE_RUNBOOK.md or CODING_STANDARDS.md: (a) new public API endpoint → ADR required; (b) new composite score methodology → ADR required; (c) new database table → ADR required; (d) amendment to an existing module's behavior → ADR amendment required; (e) frontend-only visual change within existing ADR spec → no ADR required. PM + Architect jointly own this decision when unclear. File GitHub issue.
**GitHub issue:** to be filed — see Section 5.

---

### F-PIPELINE-2 — Customer Agent ADR Consultation Trigger Is Not Automatic

**Severity:** Major
**Source:** `docs/process/agents.md §Customer Agent`; `docs/process/agent-raci.md`
**Observation:** The Customer Agent activation protocol requires `Customer Agent: AUDIT — [scope]` invocation. No working agreement or consultation trigger requires the Architect to consult the Customer Agent during ADR panel composition for features that will be visible in the user-facing interface. The 12 named standing consultation obligations in agent-raci.md do not include a trigger for Customer Agent in the ADR panel.
**Risk:** A UX-facing ADR goes through the full panel review (Architect, CM, FA, UD, EL) without Customer Agent input. Layer 3 usability gaps (institutional capacity mismatches) are the most likely category to go undetected when the Customer Agent is not in the panel.
**Recommended action:** Add a 13th standing consultation obligation: "For any ADR whose scope includes a user-visible instrument, widget, or workflow, the Architect must invite Customer Agent AUDIT on the draft before the panel review is distributed." File GitHub issue.
**GitHub issue:** to be filed — see Section 5.

---

### F-PIPELINE-3 — PM HORIZON Sweep Cadence Undocumented

**Severity:** Minor
**Source:** `docs/process/agents.md §PM Agent`
**Observation:** The PM HORIZON sweep is well-defined (6 steps including DIC consultation, gap analysis, prioritization input) but agents.md does not specify when it runs: at milestone start, at milestone midpoint, on EL request, or continuously.
**Risk:** Between milestones, latent needs go unsurfaced until a crisis forces them. The HORIZON sweep exists precisely to avoid reactive feature requests — but if it has no cadence, it will only run when someone thinks to call it.
**Recommended action:** Add cadence to agents.md: HORIZON sweep runs at (a) milestone creation ceremony and (b) milestone midpoint. PM Agent holds R for scheduling. File GitHub issue (low priority).
**GitHub issue:** to be filed — see Section 5.

---

### F-PIPELINE-4 — Cross-ADR Impact Has No Required Artifact

**Severity:** Major
**Source:** `docs/CODING_STANDARDS.md §Pre-PR Checklist`; `docs/process/agents.md §Implementation Agent`
**Observation:** The pre-PR checklist requires agents to check cross-ADR impact, but this check produces no artifact. There is no PR template field requiring the agent to enumerate which ADRs the PR touches. For features that span multiple ADRs (e.g., a Zone 1D widget addition touches ADR-008 zone assignments, ADR-010 ScenarioStepState atom, and ADR-005 GovernanceModule contract), this means the review process relies entirely on reviewer memory.
**Risk:** A PR slips through that modifies behavior governed by ADR-010 without the FA or UD reviewers knowing to check ADR-010 compliance. The adage "CI is a confirmation, not a discovery mechanism" applies here — reviewers cannot confirm ADR compliance they haven't been told to check.
**Recommended action:** Add a required section to the PR description template: "**ADRs affected:** List each ADR whose scope this PR touches. For each: state whether this PR is compliant with the current ADR or requires an ADR amendment." File GitHub issue.
**GitHub issue:** to be filed — see Section 5.

---

### F-ADR-1 — No Panel Review Artifacts for ADR-001 through ADR-006

**Severity:** Minor (retrospective gap, not active risk)
**Source:** `docs/adr/reviews/ADR-008-panel-review.md` (notes "first ADR Panel Review document in the WorldSim codebase")
**Observation:** The ADR panel review process (artifact at `docs/adr/reviews/ADR-NNN-panel-review.md`) was established at ADR-008 acceptance (2026-05-22). ADR-001 through ADR-006 were accepted without formal panel review artifacts. This is a retrospective gap — these ADRs went through consultation and review, but no structured artifact records the findings.
**Risk:** Future agents auditing the ADR library will find no review record for the foundational decisions. When those ADRs come up for renewal (M10 for all 6), the renewal process cannot reference panel findings it doesn't have.
**Recommended action:** Do not retrofit retroactive panel reviews — the decisions are settled. Instead, when ADR-001 through ADR-006 come up for M10 renewal review, the renewal artifact should include a note acknowledging the pre-panel-review-era origin and performing the equivalent review at renewal time. File GitHub issue for M10 renewal tracking.
**GitHub issue:** to be filed — see Section 5.

---

### F-ADR-2 — ADR-004 Engine Version Layer 2 Overdue at M9 Exit

**Severity:** Major
**Source:** `docs/adr/ADR-004-scenario-engine.md §Decision 1`; Issue #139
**Observation:** ADR-004 Decision 1 explicitly defers "building the artifact convention... the Milestone 9 scope... is the earliest point where the deployment mechanism and the reconstruction endpoint can be co-designed." M9 has entered human-gate phase. Issue #139 tracks this gap. Whether Layer 2 (on-demand engine instantiation) was delivered in M9 is not confirmed.
**Risk:** If Layer 2 was not delivered in M9 (consistent with the M9 exit state captured in SESSION_STATE.md), then the ADR-004 deferral language has expired. The engine_version Layer 2 gap is now blocking backtesting reconstruction integrity for any M10 simulation run.
**Recommended action:** Confirm Layer 2 delivery status at M10 creation ceremony. If not delivered, reclassify Issue #139 as M10 P1 blocking. Do not open any new M10 backtesting issues until #139 is resolved.
**GitHub issue:** existing #139 — confirm M10 assignment.

---

### F-ADR-3 — ADR-006 Decision 12 Playwright Sequence Not CI-Enforceable

**Severity:** Major
**Source:** `docs/adr/ADR-006-uncertainty-quantification.md §Decision 12`
**Observation:** ADR-006 Decision 12 states: "The Playwright test sequence (Decision 12) cannot be automatically enforced by CI. It is a PR review discipline requirement." The 4-phase sequence is mandatory for all frontend changes touching the instrument cluster. The ADR acknowledges this gap within its own text.
**Risk:** Under M10 implementation pressure, the Playwright sequence is the first gate to slip. It is invisible to CI. It requires a reviewer to know it must be checked. If the reviewer also worked on the PR, the independence fails entirely.
**Recommended action:** (1) Add the Playwright sequence explicitly to the PR review checklist in CONTRIBUTING.md and/or CODING_STANDARDS.md, making it visible at the PR-level. (2) Evaluate whether a CI job can run at least phases 1 and 2 without the full Docker Compose stack (equitable build requirement). File near-miss entry NM-023. File GitHub issue.
**GitHub issue:** to be filed — see Section 5.

---

### F-ADR-4 — Module Behavioral Contract Renewal Trigger Is ADR-005-Only

**Severity:** Major
**Source:** `docs/adr/ADR-005-human-cost-ledger.md §Amendment 2`; `docs/CODING_STANDARDS.md`
**Observation:** ADR-005 Amendment 2 added a renewal trigger for DemographicModule._SUBSCRIBED_EVENTS: "any `_SUBSCRIBED_EVENTS` change must update ADR same-commit." This trigger was added retroactively after the Amendment 2 incident. ADR-002 defines `ControlInput` subclasses and ADR-004 defines `ScenarioRunner` — both have behavioral contracts that could change without triggering ADR updates.
**Risk:** A future implementation agent adds a new `ControlInput` subclass or modifies `ScenarioRunner.advance_timestep()` without realizing this constitutes a behavioral contract change requiring an ADR amendment. The pattern is documented only for DemographicModule.
**Recommended action:** Generalize the renewal trigger rule in CODING_STANDARDS.md: "Any change to a class interface defined by an ADR (its public methods, subscribed events, ABC contract, or event emission) requires an ADR amendment in the same commit." File GitHub issue.
**GitHub issue:** to be filed — see Section 5.

---

### F-ADR-5 — ADR-010 api_contracts.yml Registration Is a Future Compliance Obligation

**Severity:** Minor (known, tracked in ADR)
**Source:** `docs/adr/ADR-010-trajectory-view.md §Decision 2`
**Observation:** ADR-010 Decision 2 states: "`docs/schema/api_contracts.yml` must be updated with this endpoint in the same commit that implements it. Schema drift is a compliance violation." The `GET /scenarios/{id}/trajectory` endpoint does not exist yet (M10 implementation). The obligation is documented in the ADR but has no corresponding GitHub issue to ensure it is not forgotten at implementation time.
**Risk:** M10 implementation of the trajectory view proceeds; the endpoint is implemented; no one checks the ADR; api_contracts.yml is not updated in the same commit; schema drift violation occurs. CI would not catch this.
**Recommended action:** File a Task Issue against the trajectory view Feature Issue that explicitly requires api_contracts.yml update as a pre-merge condition. File GitHub issue.
**GitHub issue:** to be filed — see Section 5.

---

### F-ADR-6 — CONTRIBUTING.md "Branch from develop" (Confirmed Stale)

**Severity:** Major (same root cause as F-CONTRIB-1 — consolidated)
**Note:** This finding consolidates F-CONTRIB-1. CONTRIBUTING.md is the document read by new agents at session start. The stale instruction is not a minor discrepancy — it is actionable in the wrong direction. Tracked under F-CONTRIB-1 for issue filing.

---

### F-ADR-7 — ADR-007 Anomaly Detection TSC Gate: No TSC Exists

**Severity:** Minor (governance limitation, documented)
**Source:** `docs/adr/ADR-007-synthetic-data-framework.md §Anomaly Detection`; `CLAUDE.md §Governance`
**Observation:** ADR-007 requires "TSC sign-off required before production deployment" of the anomaly detection feature. CLAUDE.md §Governance documents the intended governance progression — Stage 4 (TSC formation) is triggered by "first institutional user engagement," which has not occurred. The TSC does not exist.
**Risk:** If anomaly detection is implemented in M10 or M11, the TSC sign-off gate cannot be passed. The feature would be blocked from production deployment indefinitely, or the gate would be waived by the same individual who holds full repository authority — a self-approval scenario CLAUDE.md explicitly flags.
**Recommended action:** Add to M10 scope definition: "Anomaly detection feature is blocked pending TSC formation per ADR-007. Implementation may proceed but production deployment requires TSC sign-off per CLAUDE.md §Governance." No new GitHub issue required — this is a documented governance constraint, not a process gap.

---

### F-ADR-8 — ADR Panel Composition Algorithm Is Implicit

**Severity:** Major
**Source:** `CLAUDE.md §Architectural Principles`; `docs/process/agent-raci.md §Decision Types`
**Observation:** CLAUDE.md says "derive the panel composition from docs/process/agent-raci.md." agent-raci.md defines 9 decision types with R/A/C/I assignments. But no algorithm translates "this ADR touches Architectural + Domain/measurement + UX component decision types simultaneously" into a concrete panel list. The Architect makes a judgment call that is not auditable.
**Risk:** An ADR that spans multiple decision types will have a panel that either over-includes (every C in every relevant decision type) or under-includes (only the most salient decision type's panel). Under-inclusion is the higher risk: a panel that omits the CM on a new composite score methodology, for example, would produce a methodologically unchecked ADR.
**Recommended action:** Add an explicit panel composition algorithm to CODING_STANDARDS.md §ADR Standards: "The panel is the union of all C-holders across all decision types the ADR touches. The implementing agent is always added if not already in the union. EL always holds A. When in doubt, include rather than exclude." File GitHub issue.
**GitHub issue:** to be filed — see Section 5.

---

### F-ADR-9 — Backtesting Case Identification for Novel Composite Scores Is Undocumented

**Severity:** Major
**Source:** `docs/adr/ADR-005-human-cost-ledger.md §Decision 5`; `docs/CODING_STANDARDS.md §Testing Requirements`
**Observation:** ADR-005 Decision 5 defines the backtesting case registration protocol (4-file requirement: case definition, fixture data, expected outcomes, audit trail). The protocol specifies what to produce, not how to identify a valid historical case for a novel composite score. For composite scores derived from multiple frameworks (e.g., political feasibility derived from governance indicators), the historical validation case may not be obvious — or may not exist.
**Risk:** Implementation of a new composite score proceeds; the team reaches the backtesting step; no one has identified a historical validation case; the CM obligation to identify "at least one confirmed historical transition that validates the score's directional behavior" cannot be satisfied; the feature either ships without backtesting validation or is blocked indefinitely.
**Recommended action:** Add to ADR Standards: "Any ADR introducing a new composite score or measurement methodology must include, in the Consequences section, a named historical case and time period that will serve as the backtesting validation anchor. If no case can be named, the ADR must include a documented CM assessment of why and what substitute validation approach will be used." File GitHub issue.
**GitHub issue:** to be filed — see Section 5.

---

## 4. Capstone — Hypothetical Feature Trace

### Feature: Political Feasibility Score (PFS) Widget for Zone 1D

**Description:** A real-time composite score (0.0–1.0) quantifying the political viability of the current steered fiscal path, displayed as a compact widget in Zone 1D during Mode 3 Active Control. The score updates every step advance. It draws on governance indicators, social legitimacy dynamics, and distributional effects to surface whether the path the finance minister is steering would be politically sustainable given the country's political economy.

**Why this feature:**
- Non-trivial: requires new methodology ADR, new backend computation, schema changes, UI changes, and backtesting validation
- Plausible: Zone 1D is currently "four-framework current position" (ADR-008); a real-time political feasibility signal during Mode 3 is directly mission-relevant
- Tests the full pipeline: the feature spans intent surfacing → domain consultation → ADR → schema → backend → frontend → testing → milestone exit

---

### Step-by-Step Trace

#### Step 1 — Intent Surfacing

**Most natural path:** PM HORIZON sweep at M10 creation ceremony includes DIC consultation.

`Political Economist: SCENARIO — What does a finance minister in Mode 3 need to know about the political feasibility of their current steering path?`

The Political Economist surfaces that the current Zone 1D instrument ("four-framework position") shows where the country is, not whether the path it is taking is politically executable. This gap is escalated to PM.

**Alternatively:** Customer Agent AUDIT during M10 Mode 3 use-case review surfaces a Layer 3 gap: "A finance minister will need to know if the path they are steering would be supported by their coalition before they propose it to parliament — the current instruments give no political signal."

**Pipeline verdict at this step:** CLEAR. Two natural surfacing channels (HORIZON sweep + Customer Agent AUDIT) would both catch this. The channels work.

**Ambiguity:** The PM HORIZON sweep cadence is not defined. If the sweep does not run at M10 creation, this intent might only surface when the Customer Agent is explicitly invoked. See `F-PIPELINE-3`.

---

#### Step 2 — Prioritization

PM TRIAGE: This is a substantial new computation with methodology implications. Initial verdict: **Need Info** — what would the methodology be?

PM opens a scoping issue. The Political Economist and Chief Methodologist are consulted via DIC:

`Chief Methodologist: VALIDATE — Is a composite political feasibility score statistically defensible at the data quality we have for most countries?`

CM returns: feasible using available governance indicators + social legitimacy proxies, but Tier 3–4 confidence for most countries. Synthetic data rules apply. Acceptable.

PM revises TRIAGE to **Build Now** for M10 scope.

**Ambiguity (F-PIPELINE-1):** PM must decide: does this require a new ADR, or is it an amendment to ADR-005 (GovernanceModule extension) plus ADR-008 (Zone 1D widget addition)? There are no documented criteria. PM makes a judgment call: the score methodology is novel enough to warrant a new ADR. This judgment is correct, but it is not auditable — a different PM could conclude "amendment only" and skip the ADR process.

**Pipeline verdict:** FRAGILE. Correct outcome reached, but by judgment with no documentation trail. See `F-PIPELINE-1`.

---

#### Step 3 — Issue Creation

PM creates:
- Feature Issue: "PFS Widget — Political Feasibility Score for Zone 1D (Mode 3)" under M10 Epic "Mode 3 Enhancement"
- The issue notes: ADR required, Customer Agent AUDIT pending, estimated scope: Architect (ADR), Backend Agent (module), DA (schema), Frontend Agent (widget)

**Ambiguity:** Does an M10 Epic for "Mode 3 Enhancement" exist? The roadmap mentions Mode 3 instrument development as an M11 deliverable, not M10. PM would need to decide whether PFS belongs in M10 (if it contributes to the instrument cluster redesign) or M11 (if it is part of Mode 3 proper). No decision tree is documented.

**Pipeline verdict:** AMBIGUOUS. Feature could drift between milestones with no clear home.

---

#### Step 4 — ADR Process Initiation

Architect checks `docs/architecture/backlog.md`. ADR-009 is ASSIGNED to CE (M11). ADR-010 was Trajectory View. **ADR-011 would be next** for Political Feasibility Score.

Architect marks ADR-011 ASSIGNED in the backlog. This is the correct first step.

**Panel composition derivation (F-ADR-8):**
This ADR spans:
- **Architectural** (new scoring computation): Ar (R), EL (A), CM (C), DA (C), BE (C)
- **Domain/measurement** (political feasibility methodology): Political Economist (C), CM (C)
- **UX component** (Zone 1D widget): FA (C), UD (C)

Union of all C-holders: CM, DA, BE, Political Economist, FA, UD
Implementing agents: Backend Agent (module), Frontend Agent (widget) — both present
EL holds A by invariant.

**Pipeline verdict at panel composition:** CLEAR with caveats. The union rule produces the right answer here, but only if the Architect thinks to consult agent-raci.md for all three decision types simultaneously. The algorithm is not written down.

---

#### Step 5 — Generative Consultation (Pre-Draft)

Before drafting ADR-011, Architect activates:

`Political Economist: SCENARIO — How should political feasibility be operationalized as a composite score for Mode 3 real-time computation?`

`Chief Methodologist: VALIDATE — What is the minimum data quality required for a politically defensible PFS score, and what confidence tier would apply for typical country data availability?`

`Customer Agent: AUDIT — Zone 1D political feasibility widget for the finance minister Mode 3 steering use case — Layer 3 gaps?`

**BREAKDOWN — Customer Agent consultation trigger (F-PIPELINE-2):** The Architect must think to include Customer Agent. There is no standing consultation obligation that triggers Customer Agent for UX-facing ADRs. If the Architect does not invoke the Customer Agent here, the panel review would proceed with no Layer 3 usability check — and the widget could be built with a conceptual framing that means something different to the finance minister than to the developer who built it.

**Pipeline verdict:** FRAGILE. The Customer Agent is the right agent here and is not in the default panel. The feature would likely work but miss the Layer 3 gut-check.

---

#### Step 6 — ADR-011 Drafted

Architect drafts ADR-011 covering:
- Decision 1: PFS composite methodology (3 sub-indicators: governance quality index, social legitimacy proxy, coalition viability estimate)
- Decision 2: GovernanceModule extension vs. new PoliticalEconomyModule

**BREAKDOWN — Module extension vs. new module (not F- classified, pipeline gap):** ADR-005 Decision 6 defines GovernanceModule's behavioral contract (5 indicators, 4 subscribed events). PFS could be a 6th governance indicator (GovernanceModule extension) OR a new PoliticalEconomyModule. This is an architectural decision with no documented arbitration forum before ADR drafting. The Architect drafts one approach; the panel can push back. But if the Architect chooses extension and the panel reviews extension, a new-module alternative may not be surfaced.

**Pipeline verdict:** WORKS but could miss architectural alternatives. The panel review is the backstop — this is appropriate for an ADR process.

---

#### Step 7 — Panel Review

Panel: Ar (author), Political Economist, CM, DA, Backend Agent, Frontend Agent, UD, FA, EL.

Each agent produces findings. CM raises a DEFER on the coalition viability estimate sub-indicator (insufficient historical data for backtesting). Political Economist offers INCORPORATE: reframe coalition viability as "elite capture risk score" with cleaner historical precedents (Greece 2010–2012 elite capture dynamics documented). Frontend Agent raises INCORPORATE: the widget's 0.0–1.0 range needs a confidence band display, and ADR-007 synthetic tier rules apply.

Architect incorporates INCORPORATE items. CM's DEFER on coalition viability → dropped from PFS-v1, deferred to PFS-v2.

**BREAKDOWN — Backtesting case (F-ADR-9):** No one in the panel is required to name a specific historical case for validating the "elite capture risk" sub-indicator at this stage. The Consequences section of ADR-011 says "backtesting validation required" but names no case. Implementation will proceed; at test-writing time, the Backend Agent will need to identify a historical case — at which point the CM obligation has no formal forum to surface a gap.

**Pipeline verdict:** FRAGILE. Backtesting case identification happens after ADR acceptance, not during panel review. By the time the gap surfaces, the ADR is accepted and implementation is underway.

---

#### Step 8 — Stories and Acceptance Criteria

PO Agent writes:
- Story 1: "As a finance minister in Mode 3, when I advance the simulation by one step, I see the PFS score update within 500ms in Zone 1D."
- Type 1 AC: Widget renders in Zone 1D within 500ms of step advance. Verified by Playwright phase 2 render cycle test.
- Story 2: "When PFS falls below 0.3, the widget shows a caution indicator to draw my attention."
- Type 2 AC: Caution indicator appearance is appropriately prominent and does not obscure the score value. Verified by structured review session.

**Pipeline verdict:** CLEAR. The AC taxonomy (Type 1/Type 2) is well-documented and PO Agent can apply it correctly.

---

#### Step 9 — Test-First Gate

Backend Agent writes unit tests for PFSCalculator before implementation:
- test_pfs_composite_weights_sum_to_1
- test_pfs_governance_quality_tier_propagation (max() rule from ADR-001 Amendment)
- test_pfs_below_threshold_triggers_caution_flag

Frontend Agent writes Playwright tests before implementation:
- Phase 1: PFS widget renders in isolation
- Phase 2: Step advance → Zone 1D PFS update in ≤500ms
- Phase 3: Mode 1→Mode 3 transition does not ghost PFS values
- Phase 4: Render budget (≤16ms per frame during continuous step advance)

**BREAKDOWN — Playwright sequence enforcement (F-ADR-3):** Phases 3 and 4 are not CI-runnable. The Frontend Agent must run them locally and attest in the PR description. If they don't, the reviewer has no signal.

---

#### Step 10 — Implementation

Backend Agent: extends GovernanceModule with PFSCalculator sub-component (ADR-011 chose extension over new module). Adds `political_feasibility_score` as a new indicator. Updates `_SUBSCRIBED_EVENTS` — this change requires same-commit ADR amendment per the renewal trigger (ADR-005 Amendment 2). Backend Agent writes the amendment and commits together.

DA: updates `docs/schema/simulation_state.yml` with new field, `docs/schema/api_contracts.yml` with PFS field in trajectory endpoint response.

Frontend Agent: implements PFS widget in Zone 1D. References `ScenarioStepState` atom (ADR-010 Decision 4) — PFS score is added to the atom.

**File authority check:**
- `backend/app/modules/governance.py` — Backend Agent (R) ✓
- `docs/schema/simulation_state.yml` — DA (R) ✓
- `docs/schema/api_contracts.yml` — DA (R) ✓
- `frontend/src/components/zone1d/` — Frontend Agent (R) ✓

**Cross-ADR impact (F-PIPELINE-4):**
- ADR-001 (Quantity type, confidence tier propagation) — touched by PFSCalculator output type
- ADR-005 (GovernanceModule contract) — _SUBSCRIBED_EVENTS extended
- ADR-007 (Synthetic data rules, tier-gated MDA alerts) — PFS score has synthetic tier
- ADR-008 (Zone 1D instrument spec) — new widget added
- ADR-010 (ScenarioStepState atom, trajectory response shape) — PFS field added

**This PR touches 5 ADRs.** The pre-PR checklist requires cross-ADR impact enumeration, but there is no required artifact. A reviewer receiving this PR has no guaranteed visibility into all 5 ADR dependencies.

**Pipeline verdict:** FRAGILE. Five-ADR dependency with no required enumeration artifact. Any reviewer who misses one ADR is reviewing an incomplete picture.

---

#### Step 11 — Pre-PR and Push

Backend Agent: runs `cd backend && ruff check . && mypy app/` — passes. Backend lint gate is enforced locally and by CI.

Frontend Agent: runs Playwright phases 1 and 2 locally. Phases 3 and 4 are run locally but CI cannot verify this.

PR opens. PR description lists:
- Closes #[PFS feature issue]
- ADRs affected: [none listed — F-PIPELINE-4 gap manifests here]
- Playwright sequence: Phase 1–4 run locally (attestation only)

**Pipeline verdict:** FRAGILE at two points (Playwright enforcement, ADR enumeration).

---

#### Step 12 — Review

EL reviews. Backend, Frontend, DA confirm their own files are correct. CM confirms confidence tier propagation is correct (PFS score propagates tier from max() of sub-indicators per ADR-001 Amendment 1).

No Customer Agent input was sought at review time. If the Customer Agent was not activated at Step 5 (generative consultation), this is the last natural moment to catch a Layer 3 framing gap — but it is not required.

---

#### Step 13 — Milestone Exit (M10)

PFS widget ships in M10 exit. Exit ceremony:
1. Exit checklist: PFS feature issue closed ✓
2. Compliance scan: new scan entry filed ✓
3. Frontend smoke test: PFS widget renders in demo scenario ✓
4. Socratic Agent TEST: covers M10 architecture including PFS ✓
5. Release v0.10.0 ✓
6. CHANGELOG ✓
7. M11 creation ceremony ✓

**Pipeline verdict:** CLEAR. Milestone ceremony is well-documented and would handle PFS correctly.

---

#### Step 14 — Demo (Demo 3)

Demo 3 is the M10 demo anchor. The finance minister persona runs a Mode 3 scenario, steers fiscal policy, and PFS drops below 0.3 — the caution indicator fires.

**BREAKDOWN — Demo ownership (F-AGENTS-2):** Who scripted Demo 3? Who validated that the PFS widget tells a coherent story in the context of the demo scenario? No agent holds R for demo preparation. The demo could be technically correct but narratively incoherent — or the PFS widget could fire at a step where the demo scenario context makes the caution signal confusing.

---

### Capstone Summary: Where the Trace Breaks Down

| Step | Verdict | Finding |
|---|---|---|
| 1 — Intent surfacing | CLEAR (fragile cadence) | F-PIPELINE-3: HORIZON sweep cadence undocumented |
| 2 — Prioritization | FRAGILE | F-PIPELINE-1: ADR threshold not documented |
| 3 — Issue creation | AMBIGUOUS | No rule for milestone assignment of cross-cutting features |
| 4 — ADR number | CLEAR | Process works |
| 5 — Panel composition | FRAGILE | F-ADR-8: no algorithm; F-PIPELINE-2: Customer Agent not triggered |
| 6 — ADR drafting | WORKS | Panel is backstop for module extension vs. new module |
| 7 — Panel review | FRAGILE | F-ADR-9: backtesting case not named during ADR review |
| 8 — Stories | CLEAR | AC taxonomy works |
| 9 — Test-first gate | FRAGILE | F-ADR-3: Playwright phases 3–4 not CI-enforceable |
| 10 — Implementation | FRAGILE | F-PIPELINE-4: 5-ADR dependency, no required enumeration |
| 11 — Pre-PR | FRAGILE | Same: F-PIPELINE-4, F-ADR-3 |
| 12 — Review | CLEAR (fragile) | Customer Agent gap could surface late |
| 13 — Milestone exit | CLEAR | Ceremony is well-documented |
| 14 — Demo | BREAKDOWN | F-AGENTS-2: no demo owner |

**5 of 14 steps are FRAGILE or BREAKDOWN.** No step is BROKEN (produces a guaranteed bad outcome), but five steps rely on individual judgment, unenforceable conventions, or missing ownership to produce correct outcomes. Under M10 sprint pressure, the fragile steps are the ones that slip.

---

## 5. Issues Filed

The following GitHub issues are filed as part of this audit. Each maps to a finding above. Findings already tracked by existing issues are noted.

| Finding | Issue | Title | Label |
|---|---|---|---|
| F-RUNBOOK-1 | #535 | MILESTONE_RUNBOOK.md: update milestone table to reflect M9 exit | `documentation` |
| F-CONTRIB-1/F-ADR-6 | #536 | CONTRIBUTING.md: fix stale "branch from develop" instruction | `documentation` |
| F-AGENTS-2 | #537 | Assign demo preparation R ownership in agent-raci.md | `documentation` |
| F-PIPELINE-1 | #538 | Document "significant feature" threshold for ADR requirement | `documentation` |
| F-PIPELINE-2 | #539 | Add Customer Agent as 13th standing consultation obligation for UX-facing ADRs | `documentation` |
| F-PIPELINE-3 | #540 | PM HORIZON sweep: document cadence in agents.md | `documentation` |
| F-PIPELINE-4 | #541 | PR template: require cross-ADR impact enumeration | `documentation` |
| F-ADR-1 | #542 | M10 ADR renewal: include pre-panel-review-era acknowledgment for ADR-001–006 | `documentation` |
| F-ADR-3 | #543 | ADR-006 Decision 12: evaluate CI-enforcement path for Playwright phases 3–4 | `enhancement` |
| F-ADR-4 | #544 | Generalize module behavioral contract renewal trigger to all ADR-defined classes | `documentation` |
| F-ADR-5 | #545 | Task: update api_contracts.yml in same commit as trajectory endpoint implementation | `documentation` |
| F-ADR-8 | #546 | CODING_STANDARDS: document explicit ADR panel composition algorithm | `documentation` |
| F-ADR-9 | #547 | ADR Standards: require named backtesting case in Consequences section for new composite scores | `documentation` |
| F-AGENTS-1 | existing #523 | IB and DQ fully defined before M10 implementation begins | (existing) |
| F-ADR-2 | existing #139 | ADR-004 engine_version Layer 2: confirm M10 assignment | (existing) |

---

## 6. Near-Miss Entries Filed

The following entries are appended to `docs/process/near-miss-registry.md` as part of this audit. Each meets the "process gap or authority ambiguity identified — whether reactive or anticipatory" threshold in CLAUDE.md.

### NM-023 — CONTRIBUTING.md "Branch from develop" Stale Instruction (Anticipatory)

**What was at risk:** A new contributor (human or agent) following CONTRIBUTING.md literally would attempt to branch from `develop`, which does not exist. In the agent context, an agent reading CONTRIBUTING.md as mandatory session initialization could execute `git checkout -b feature/X develop` and fail silently or create a branch from main labeled as branching from develop — creating a confusing and potentially incorrect base.

**What caught it:** PI AUDIT cross-referencing CONTRIBUTING.md against CLAUDE.md PR merge gate and SESSION_STATE.md branch practice.

**Process improvement:** Update CONTRIBUTING.md branch instructions to specify `main`. Review CONTRIBUTING.md for other stale references in the same PR. See Issue #536.

---

### NM-024 — Playwright Sequence Phases 3–4 Not CI-Enforceable (Anticipatory)

**What was at risk:** ADR-006 Decision 12 mandates a 4-phase Playwright test sequence for all instrument-cluster frontend PRs. Phases 3 (mode transition) and 4 (render budget) cannot be run by CI. Under M10 sprint pressure, these phases could be skipped with no detection mechanism — a frontend PR could ship with untested mode transitions, potentially breaking Mode 1→Mode 3 instrument state.

**What caught it:** PI AUDIT reading ADR-006 Decision 12 and recognizing the "PR review discipline requirement" language as a documented vulnerability.

**Process improvement:** (1) Add Playwright sequence to CONTRIBUTING.md PR checklist explicitly. (2) Evaluate whether phases 3–4 can be partially automated without full Docker Compose stack. (3) Require Phase 3/4 attestation as a required PR description field, not optional. See Issue #543.

---

### NM-025 — Demo Story Ownership Gap (Anticipatory)

**What was at risk:** The M10 exit requires Demo 3. No agent holds R (Responsible) for demo preparation, demo script, or demo delivery. In the absence of ownership, demo preparation defaults to whoever has time at milestone close — producing a demo that may be technically correct but narratively incoherent or disconnected from the mission use case. A poorly framed Demo 3 is the primary external validation of M10 and could mislead potential institutional users.

**What caught it:** PI AUDIT capstone trace (Step 14) discovering no demo R-holder in agent-raci.md.

**Process improvement:** Assign PM Agent as R-holder for demo preparation per milestone. Add demo prep task to milestone creation ceremony checklist. Add `docs/demos/` to agent-raci.md File Ownership table with PM Agent as R. See Issue #537.

---

## 7. Summary of Pipeline Health

The WorldSim feature delivery pipeline is structurally sound. The foundational decisions — file authority, PR merge gate, branch discipline, pre-push lint gate, test-first gate, milestone ceremony — are well-documented and consistently enforced. The near-miss registry and blameless improvement process are mature and actively used (22 entries through M9).

The fragile points are concentrated in three areas:

**1. ADR process entry:** The threshold for "requires an ADR" is implicit. The panel composition algorithm is implicit. These two implicit rules govern the most architecturally consequential decisions in the pipeline.

**2. Cross-cutting features:** A feature that touches multiple ADRs simultaneously has no required artifact tracking that dependency. Cross-ADR impact is a mental checklist, not a structured PR field.

**3. Human-owned gates without tooling enforcement:** The Playwright sequence phases 3–4 exist in documentation but not in CI. Under sprint pressure, undiscoverable requirements are skipped requirements.

None of these are catastrophic — the pipeline has multiple redundant backstops. But they are the places where M10 will be under the most stress. Closing Issues #538, #541, and #543 before the first M10 implementation issue spawns would reduce the pipeline's fragility significantly.

---

*Audit conducted by the Process Integrity Agent per CLAUDE.md §Architectural Principles and MILESTONE_RUNBOOK.md §Governance Review Cadence.*
*Document committed to `docs/process/audits/` per canonical artifact location table.*
