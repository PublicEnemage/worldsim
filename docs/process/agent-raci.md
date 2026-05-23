# Agent RACI Matrix

> This chart translates the working agreements in `docs/process/agents.md` into an auditable
> RACI matrix. Every non-I cell is grounded in a specific commitment from the relevant agent's
> working agreement or persona definition. If an agent's working agreement does not speak to a
> decision type, that agent is Informed (I) — aware but with no active role.
>
> Source of truth for working agreements: `docs/process/agents.md` — read that file before
> acting on this chart. If agents.md and this chart conflict, agents.md governs.
>
> Issue: #369 (supersedes #301)
> Last updated: 2026-05-21

---

## How to Read This Chart

| Code | Meaning |
|---|---|
| R | **Responsible** — does the work. Multiple agents may share R on one decision type. |
| A | **Accountable** — owns the outcome; the one person who decides when it is complete. Only one agent holds A per row. The Engineering Lead holds A on most rows because they have final decision authority (CLAUDE.md §Governance). |
| C | **Consulted** — input required before the decision is finalized. Two-way communication; the decision waits for this input. |
| I | **Informed** — notified after the decision. One-way communication; no active role. |

---

## Agent Key

| Abbr | Full name | Status |
|---|---|---|
| EL | Engineering Lead (Human) | Active |
| PM | PM Agent | Active |
| Ar | Architect Agent | Active |
| Im | Implementation Agents | Active |
| DA | Data Architect Agent | Active |
| QA | QA Lead Agent | Active |
| Sr | Security & Review Agent | Active |
| IR | Independent Review Agent | Active |
| So | Socratic Agent | Active |
| CE | Chief Engineer Agent | Defined-inactive (activation trigger: ADR-007) |
| FA | Frontend Architect Agent | Active |
| UD | UX Designer Agent | Active |
| UT | UX Design Thinking Agent | Active |
| DI | Domain Intelligence Council (9 members) | Active |
| CO | Council Orchestrator | Active (operational) |
| AF | Architecture Review Facilitator | Active (operational) |
| IB | Intent Block Author Agent | Proposed (Issue #299) |
| DQ | Data Quality Agent | Proposed (Issue #300) |

---

## RACI Matrix

| Decision type | EL | PM | Ar | Im | DA | QA | Sr | IR | So | CE | FA | UD | UT | DI | CO | AF | IB | DQ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1. Architectural decisions | A | I | R | I | C | I | I | I | I | C | C | I | C | C | I | C | I | I |
| 2. UX frame decisions | A | I | I | I | I | I | I | C | I | I | C | C | R | I | I | I | I | I |
| 3. UX component decisions | A | I | I | I | I | I | I | C | I | I | C | R | I | I | I | I | I | I |
| 4. Data / schema decisions | A | I | C | C | R | C | I | I | I | I | I | I | I | I | I | I | I | C |
| 5. Domain / measurement decisions | A | I | C | I | I | C | C | I | I | I | I | I | I | R | C | C | I | C |
| 6. Process / milestone decisions | A | R | C | I | I | C | I | I | I | I | I | I | C | I | C | I | I | I |
| 7. Compliance decisions | A | I | I | C | C | C | R | I | I | I | I | I | I | C | I | I | I | C |
| 8. Demo / stakeholder decisions | A | R | I | I | I | I | I | R | I | I | C | C | I | C | I | I | I | I |
| 9. Agent activation decisions | A/R | C | I | I | I | I | I | I | I | I | I | I | I | I | I | I | I | I |

---

## Decision Type Grounding

Every non-I cell is grounded below in the specific working agreement passage that justifies it.
If a cell is omitted from a section, it is I.

---

### 1. Architectural decisions

*Scope: ADR authoring and amendment, module boundary definitions, API contract design, system
design documents, cross-ADR impact assessments.*

**EL — A:** "Final decision on all ADR option selections — agents propose, Engineering Lead
accepts or rejects." (`agents.md §Engineering Lead`)

**Ar — R:** "Produces system design documents, ADRs, and API contracts before implementation
begins. No code is written for a significant feature without an ADR." Activation modes DRAFT,
REVIEW, and AMEND. (`agents.md §Architect Agent`)

**DA — C:** Any ADR that touches a table column, JSONB key, or API endpoint requires schema
co-authorship. "Updates the relevant schema file in the same commit as any code change that
alters a table column, JSONB key structure, API endpoint, or simulation type. Schema drift from
code drift is a compliance violation." (`agents.md §Data Architect Agent`)

**CE — C:** "Reviews all Architect Agent proposals that have computational performance
implications before they are accepted. A proposal that defines a new module interface or
relationship type without Chief Engineer review may create performance constraints that cannot be
resolved without interface rework." (`agents.md §Chief Engineer Agent`)

**FA — C:** "RACI position: R on frontend component architecture briefs; C on ADR decisions
with frontend type implications." (`agents.md §Frontend Architect Agent`)

**UT — C:** "RACI: ... C on new capability scoping (before ADR authoring begins)." The Design
Thinking Agent is consulted before ADR authoring begins for any capability that has an
interaction-model dimension. (`agents.md §UX Design Thinking — Working Agreement`)

**DI — C:** Domain members are activated in CHALLENGE mode against architecture documents via
the Architecture Review Facilitator before significant ADRs are accepted. "Routing domain
expertise into architecture decisions before they become ADRs — not after they become production
code." (`agents.md §Architecture Review Facilitator — Working Agreement`)

**AF — C:** "I produce challenges. I do not produce ADR text." The Facilitator produces
structured domain challenges that inform ADR option selection but does not author ADR text.
(`agents.md §Architecture Review Facilitator — Working Agreement`)

---

### 2. UX frame decisions

*Scope: Interaction model critique, design premise establishment, judgments about whether the
current interaction frame is right for the canonical user — Case B level decisions.*

**EL — A:** "Engineering Lead decides which proposals advance to UX Designer. The agent does
not self-authorize design changes." (`agents.md §UX Design Thinking — Working Agreement`)

**IR — C:** The Independent Review Agent evaluates the demo surface from a stakeholder
perspective; frame decisions determine what IR reviews against. Consulted when a proposed frame
change would alter the demo surface or information hierarchy.

**FA — C:** "RACI position: ... C on UX decisions with implementation feasibility concerns."
A frame change may carry rendering implications. "When 'always visible' and 'not slow' are in
genuine tension — I bring both the requirement and the constraint to the UX Designer and
Engineering Lead simultaneously." (`agents.md §Frontend Architect — Working Agreement`)

**UD — C:** The UX Designer works within the accepted frame. A frame change redefines the
domain the UX Designer operates in; they must be consulted before a new frame is committed.
"UX Design Thinking Agent challenges whether the frame is right; I decide where things live
within the accepted frame. Those are different authorities, and I respect the boundary."
(`agents.md §UX Designer — Working Agreement`)

**UT — R:** "RACI: R on interaction model critiques and design premise proposals." "I never
receive a desired conclusion before producing a critique. Independence is the value I provide."
(`agents.md §UX Design Thinking — Working Agreement`)

---

### 3. UX component decisions

*Scope: Zone assignments (Zone 1 / 2 / 3), information hierarchy positions, where specific
elements live within the accepted frame.*

**EL — A:** "A deviation from a UX Designer ruling requires an Engineering Lead decision
recorded in `docs/frontend/design-decisions.md`." The EL is the only override authority.
(`agents.md §UX Designer Agent`)

**IR — C:** IR reviews demo outputs against current UX rulings; a hierarchy violation in the
rendered demo is an IR finding. Consulted when a ruling affects what will be shown in the next
stakeholder review.

**FA — C:** "RACI position: ... C on UX decisions with implementation feasibility concerns."
"UX Designer sign-off is required on all briefs before implementation begins. I do not
unilaterally decide that a UX trade-off is acceptable." Also, from UX Designer offer of help:
"Before a brief is produced, bring me the proposed component structure." (`agents.md §Frontend
Architect — Working Agreement`)

**UD — R:** "UX Designer rulings are ADR-level contracts for the frontend." "My rulings are
binding until overridden by the Engineering Lead with a recorded rationale in
design-decisions.md. 'This is close enough' is not an override." (`agents.md §UX Designer —
Working Agreement`)

**UT — I:** Explicitly stated: "RACI: ... I on component-level UX decisions." The Design
Thinking Agent's authority ends at the frame level; component-level decisions belong to the UX
Designer. (`agents.md §UX Design Thinking — Working Agreement`)

---

### 4. Data / schema decisions

*Scope: Schema registry changes, JSONB contract definitions, data standards amendments, new
table columns, field certification framework design.*

**EL — A:** Final authority on DATA_STANDARDS.md amendments and schema policy decisions.

**Ar — C:** API response shape is Architect territory; schema changes that alter API response
shape require Architect consultation. "Handoff point: API response shape is Architect territory;
how that shape is consumed and rendered is Frontend Architect territory." (`agents.md §Frontend
Architect Agent`, Relationships section)

**Im — C:** "Any agent writing a SQL query, reading a JSONB key, calling any API endpoint, or
instantiating any simulation type MUST first read the relevant schema file." Implementation
agents must identify cross-ADR schema impact before PR. (`agents.md §Implementation Agents`,
Pre-PR Checklist)

**DA — R:** "Owns and maintains `docs/schema/` (three authoritative files: `database.yml`,
`api_contracts.yml`, `simulation_state.yml`). Updates the relevant schema file in the same
commit as any code change that alters a table column, JSONB key structure, API endpoint, or
simulation type. Schema drift from code drift is a compliance violation." (`agents.md §Data
Architect Agent`)

**QA — C:** "Works with Data Architect Agent on data certification test gates." CI gates
enforcing schema contracts are within QA scope. (`agents.md §QA Lead Agent`)

**DQ — C:** "RACI position: R on `source_field_registry` certification execution; C on new
source registration (alongside Data Architect); C on data standards gap dispositions when gaps
involve source field semantics." (`agents.md §Data Quality Agent`)

---

### 5. Domain / measurement decisions

*Scope: Simulation methodology, framework application, indicator definitions, uncertainty
quantification, synthetic data methodology, meaninglessness thresholds.*

**EL — A:** Final authority on methodology decisions; anomaly detection deployment requires TSC
sign-off which flows through the Engineering Lead. ("When an anomaly detection output would
require TSC sign-off to deploy, I surface that governance requirement explicitly rather than
treating it as a methodological question I can resolve alone." — Chief Methodologist working
agreement)

**Ar — C:** Domain decisions that define new module boundaries or require new measurement
relationships have architectural implications; Architect is consulted before those implications
become ADR commitments.

**QA — C:** Backtesting validation is how domain/measurement hypotheses are confirmed or
refuted. "Backtesting runs are part of CI — regressions in historical fidelity are treated as
build failures." (`agents.md §QA Lead Agent`)

**Sr — C:** Geopolitical Analyst (DIC member): "I flag the dual-use boundary when a SCENARIO
finding could as easily serve a financial attack as it could serve defense, and I do so before
the finding appears in output. Security and Review Agent — when I identify a finding that crosses
the dual-use boundary, I will flag it to you before it appears in a SCENARIO output." Sr is the
escalation point for dual-use domain findings. (`agents.md §Geopolitical Analyst — Working
Agreement`)

**DI — R:** Each DIC member speaks for one measurement framework. SCENARIO, CHALLENGE, and
VALIDATE modes produce domain/measurement analysis. "At least three DIC members should be
activated for any significant council review." (`agents.md §Domain Intelligence Council`)

**CO — C:** Compiles DIC perspectives into structured Council Briefings. "Never resolves
tensions — only surfaces them with clarity." The Council Orchestrator facilitates domain
convergence without making domain decisions. (`agents.md §Council Orchestrator — Working
Agreement`)

**AF — C:** "Translates domain concerns into architectural findings." Routes domain measurement
concerns that carry architectural implications to the Architect Agent and Engineering Lead.
(`agents.md §Architecture Review Facilitator — Working Agreement`)

**DQ — C:** The Data Quality Agent certifies source data feeding domain measurements and flags
plausibility violations. ("Flag plausibility bound violations: values that pass unit and schema
checks but fall outside historically documented ranges." `agents.md §Data Quality Agent`)

---

### 6. Process / milestone decisions

*Scope: Milestone exit criteria, scope prioritization, issue horizon assignments, sprint focus,
SESSION_STATE.md accuracy.*

**EL — A:** "Milestone exit authority — no milestone closes without Engineering Lead sign-off
on the exit checklist." (`agents.md §Engineering Lead`)

**PM — R:** "Keep the Engineering Lead working on the highest-priority committed Milestone work
rather than the most recently discovered work." "SESSION_STATE.md accuracy is my
accountability." "I flag scope creep in the session it appears." Every BRIEF, TRIAGE, HORIZON,
and FOCUS output serves this function. (`agents.md §PM Agent — Working Agreement`)

**Ar — C:** ADR completion is a milestone gate. Open ADRs blocking implementation affect
milestone readiness; Architect status is consulted before exit checklist sign-off.

**QA — C:** CI gate configuration; backtesting suite passage is a milestone exit requirement.
Gate status is QA's accountability. (`agents.md §QA Lead Agent`)

**UT — C:** "RACI: ... C on milestone retrospective UX assessment." The Design Thinking Agent
is activated for post-milestone UX coherence audits that are part of the retrospective.
(`agents.md §UX Design Thinking — Working Agreement`)

**CO — C:** "ROADMAP: Translates council inputs and user needs into development priorities,
maps identified gaps onto the technical milestone roadmap, proposes new GitHub Issues for
capability gaps." "Every ROADMAP output produces GitHub Issues with issue numbers — not
recommendations that might be acted on later." Filed issues affect milestone scope.
(`agents.md §Council Orchestrator — Working Agreement`)

---

### 7. Compliance decisions

*Scope: Vulnerability audits, dependency review, dual-use assessment, exception approvals, scan
registry updates, territorial convention conflict review.*

**EL — A:** "No compliance exception may be self-approved during the single-principal phase
without the following statement appearing verbatim in the exception record." Exception approval
is exclusively the Engineering Lead's authority. (`CLAUDE.md §Governance — Audit Trail
Integrity Rule`)

**Im — C:** "Cross-ADR impact: Does this commit change behavior documented in a different ADR?
If yes, identify which ADR and which section. That ADR must be updated in the same commit — not
as a follow-up." Implementation agents self-flag compliance concerns before PR opens.
(`agents.md §Implementation Agents`, Pre-PR Checklist)

**DA — C:** Schema compliance — data lineage, provenance requirements, territorial convention
conflicts — is within the Data Architect's scope. (`agents.md §Data Architect Agent`)

**QA — C:** "CI gate configuration — ensures enforcement gates match the standards in
CODING_STANDARDS.md." (`agents.md §QA Lead Agent`)

**Sr — R:** "Audits for vulnerabilities, dependency issues, data handling problems.
Specifically reviews any feature that touches sensitive country data or financial attack surface
modeling for dual-use concerns." "Dual-use check: Is this feature more useful for executing
financial attacks than for defending against them? If yes, it is out of scope for WorldSim."
"Reports directly to Engineering Lead for dual-use concerns." (`agents.md §Security and Review
Agent`)

**DI — C:** Geopolitical Analyst (DIC member) has a standing compliance-facing commitment:
"I flag the dual-use boundary when a SCENARIO finding could as easily serve a financial attack
as it could serve defense, and I do so before the finding appears in output." This is a C
relationship — the Geopolitical Analyst flags to the Security & Review Agent, who conducts the
formal compliance review. (`agents.md §Geopolitical Analyst — Working Agreement`)

**DQ — C:** "RACI position: ... C on data standards gap dispositions when gaps involve source
field semantics." Source field compliance — transformation verification, plausibility bounds,
territorial convention conflicts in source registrations — is within DQ scope.
(`agents.md §Data Quality Agent`)

---

### 8. Demo / stakeholder decisions

*Scope: Demo content selection, demo preparation sequence, stakeholder walkthrough documents,
Independent Review scope and priority.*

**EL — A:** "Issues are filed in GitHub; Engineering Lead decides which to act on."
(`agents.md §Independent Review Agent`)

**PM — R:** "Output is triaged by PM Agent before being acted on." PM orchestrates the demo
preparation sequence and translates IR findings into a prioritized action set that respects
current milestone commitments. (`agents.md §Independent Review Agent`)

**IR — R:** "Before any stakeholder demo; before any milestone exit ceremony; before any
methodology publication submission; after any significant feature ships." Produces structured
issue list (DEMO-N format) and root cause analysis. The independence requirement (fresh session,
no source code) is what makes this R meaningful. (`agents.md §Independent Review Agent`)

**FA — C:** Demo rendering and frontend performance on the demo hardware are Frontend Architect
concerns; consulted on technical feasibility of proposed demo content decisions.

**UD — C:** Demo content must reflect current UX rulings; UX Designer is consulted when demo
framing involves zone or hierarchy decisions. UX Designer rulings are ADR-level — the demo
cannot contradict them without a recorded override. (`agents.md §UX Designer Agent`)

**DI — C:** Domain accuracy of demo outputs is DIC territory. Domain members are activated
for VALIDATE mode when simulation outputs are being presented as methodology-credible to
stakeholders. (`agents.md §Domain Intelligence Council`)

---

### 9. Agent activation decisions

*Scope: Which agents to activate for a given task, commissioning new agent roles, defining and
updating activation triggers.*

**EL — A/R:** "Agent instantiation decisions — which agents to activate, when to commission a
new agent role." This is exclusively the Engineering Lead's domain — no agent may self-activate
or activate another agent without Engineering Lead authority. EL is both accountable and
responsible because the activation decision is a human judgment call, not a delegated function.
(`agents.md §Engineering Lead`)

**PM — C:** "Coordinates across all agents; surfaces decisions to Engineering Lead." The PM
Agent surfaces the need for agent involvement (e.g., BRIEF identifies that a domain question
requires DIC activation) and escalates activation decisions — but does not make them.
(`agents.md §PM Agent — Working Agreement`)

---

## Cross-Agent Interaction Patterns

The working agreements establish several standing interaction obligations that the RACI above
encodes. These patterns are collected here for reference.

### Upstream → downstream flow

```
UX Design Thinking → UX Designer → Frontend Architect → Implementation Agents
Architect Agent → Implementation Agents
Data Architect → Data Quality Agent
Domain Intelligence Council → Council Orchestrator → Architecture Review Facilitator → Architect Agent
```

### Independence requirements (break the upstream chain)

| Agent | Independence rule | Source |
|---|---|---|
| Independent Review Agent | Fresh session; no source code; documentation and screenshots only. | `agents.md §Independent Review Agent` |
| Intent Block Author Agent | Fresh session; no implementation body before intent block is written. Must confirm: *"Intent block authored without reading implementation body."* | `agents.md §Intent Block Author Agent` |
| UX Design Thinking Agent | Must NOT be given a desired conclusion before producing a critique. | `agents.md §UX Design Thinking — Working Agreement` |
| Data Quality Agent | Must not be the same agent that designed the standard being applied (conflict of interest). | `agents.md §Data Quality Agent` |

### Standing consultation obligations

These are explicit commitments in working agreements, not inferred relationships.

| Initiating agent | Receiving agent | Obligation | Source |
|---|---|---|---|
| UX Designer | Frontend Architect | "Before a brief is produced, bring me the proposed component structure." | FA working agreement (offer of help) |
| Frontend Architect | UX Designer | "Before a ruling commits to an interaction that requires a specific technical implementation, tell me." | FA working agreement (offer of help) |
| Geopolitical Analyst | Security & Review Agent | "When I identify a finding that crosses the dual-use boundary, I will flag it to you before it appears in a SCENARIO output." | Geopolitical Analyst working agreement |
| Development Economist | Intergenerational Advocate | Capability losses compound intergenerationally; joint finding required when bottom-quintile capability collapse is detected. | Development Economist and Intergenerational Advocate working agreements |
| Chief Methodologist | Any DIC member | "Bring me the uncertainty characteristics of those outputs before committing to a finding." | Chief Methodologist working agreement |
| Investment Agent | Development Economist | "Before a CATALYTIC recommendation, I will tell you which cohorts benefit and which don't." | Development Economist working agreement (offer of help) |
| Council Orchestrator | PM Agent | "Every ROADMAP output includes filed issue numbers for the next HORIZON sweep." | Council Orchestrator working agreement (offer of help) |
| Council Orchestrator | Architecture Review Facilitator | "When a council session surfaces architectural implications, I flag them to you before the session output is finalized." | Council Orchestrator working agreement (offer of help) |

---

## Cells with Implicit I Only

The following agents have no active role in any decision type beyond passive awareness. Their I
assignments reflect general project membership, not a positive claim that they are explicitly
notified in every case.

| Agent | Basis for implicit-I-only status |
|---|---|
| So (Socratic Agent) | "Does not produce code or architecture — produces understanding." Works directly with Engineering Lead only. (`agents.md §Socratic Agent`) |
| CE (Chief Engineer Agent) | Defined-inactive until ADR-007 activation. C on architectural decisions with computational implications; I on all other decision types until activated. (`agents.md §Chief Engineer Agent`) |
| IB (Intent Block Author Agent) | Proposed status; full working agreement pending Issue #299. No active role in any decision type at this governance stage. |

---

*See also: `docs/process/disposition-review-standard.md` for the RACI applied to the specific
case of standards gap dispositions.*

---

## ADR Panel Composition

When an ADR is being drafted, the Architect Agent derives the panel from this RACI chart.
Any agent with R or C assignment for the relevant decision type is either included or
their exclusion is documented with rationale.

The implementing agent — the agent responsible for building what the ADR commits to —
is always required regardless of panel size. This rule was established after ADR-008's
panel was initially drafted without the Frontend Architect, who is the primary
implementer of all frontend architecture decisions. See Issue #397 comment
2026-05-22 for the correction record.

Minimum panels by ADR type (derived from the RACI matrix above):

| ADR type | RACI row | Required panel members |
|---|---|---|
| Frontend architecture | Row 1 (Architectural decisions) | Architect Agent (author), Frontend Architect Agent (C), Engineering Lead (A) |
| Simulation engine | Row 1 (Architectural decisions) | Architect Agent (author), Chief Engineer Agent (C), Chief Methodologist (via DI — C), Engineering Lead (A) |
| Data standards | Row 4 (Data / schema decisions) | Architect Agent (C), Chief Methodologist (via DI — C), Development Economist (domain validation), Engineering Lead (A) |
| UX design | Row 2/3 (UX frame / component decisions) | Architect Agent (C), UX Designer Agent (R), Frontend Architect Agent (C), Engineering Lead (A) |
| Cross-cutting | All relevant rows | Relevant R/C agents per RACI, Engineering Lead (A) |

The Architect Agent authors the ADR — they are not a reviewer. The Engineering Lead
holds A on all ADR decisions — their sign-off is always required.

Full backlog and panel composition process: `docs/architecture/backlog.md`

---

## File Ownership

This table is the authoritative lookup for the file authority rule in CLAUDE.md. Before writing
to any file, the acting agent verifies they hold R on that file. If another agent holds R, the
acting agent produces a draft and requests the owning agent's review before committing. If a
Required Consultant (C) is listed, that agent's input must be obtained before the change is
finalized — not afterward.

### Owned Files and Directories

| File or directory | Owner (R) | Required Consultant (C) | Notes |
|---|---|---|---|
| `CLAUDE.md` | EL | Ar, PM | Constitutional document; structural changes require Architect review |
| `SESSION_STATE.md` | PM | EL | PM maintains; EL reviews major restructuring |
| `.github/` | EL | Ar | CI/CD pipeline changes require Architect review |
| `docs/process/agents.md` | PM | EL | Agent persona definitions; EL approves new agent additions |
| `docs/process/agent-raci.md` | PM | EL, Ar | RACI matrix; Architect consulted when decision-type grounding changes |
| `docs/schema/api_contracts.yml` | DA | Ar | Ar consulted when response shape changes (API response shape is Architect territory) |
| `docs/schema/database.yml` | DA | Ar, QA | Ar consulted on schema shape; QA consulted on CI enforcement gates |
| `docs/schema/simulation_state.yml` | DA | Ar, QA | Same rules as database.yml |
| `docs/DATA_STANDARDS.md` | DA | EL | EL holds A on data standards amendments |
| `docs/adr/ADR-*.md` | Ar | EL, panel members | EL sign-off required on all ADRs; panel per §ADR Panel Composition |
| `docs/adr/reviews/` | Ar | EL | Panel review artifacts authored by Architect |
| `docs/architecture/` (non-ADR) | Ar | DA, FA | DA consulted when docs define schema contracts; FA consulted on frontend architecture |
| `docs/architecture/backlog.md` | Ar | PM | ADR backlog; PM consulted on milestone assignment |
| `docs/ux/` | UD | FA, UT | FA consulted on frontend feasibility; UT consulted on first-principles consistency |
| `docs/frontend/` | FA | UD, Ar | UD consulted on design-affecting changes; Ar consulted on architectural decisions |
| `docs/compliance/scan-registry.md` | Sr | EL | Compliance scan registry; EL informed of new entries |
| `docs/compliance/` (other files) | EL | Sr, Ar | Sr consulted on security findings; Ar on compliance-architecture intersections |
| `docs/roadmap/` | PM | EL, Ar | EL holds A on roadmap decisions; Ar consulted on milestone architecture |
| `docs/data-sources/` | DA | DI (CM) | Chief Methodologist consulted on approved-source methodology changes |
| `docs/standards/` | EL | Ar, PM | Standards documents; Ar and PM consulted on process-affecting changes |
| `docs/CONTRIBUTING.md` | EL | PM, Ar | Process-affecting changes require PM and Architect review |
| `frontend/` | FA | UD | UD consulted on design-affecting frontend changes |
| `sim/` (simulation engine) | Im | Ar, CE | Ar consulted on engine architecture; CE on performance tradeoffs |
| `tests/` | QA | Im | Im consulted on test scope and fixture coverage |

### The Near-Miss That Created This Rule

PR #429 committed changes to `docs/schema/api_contracts.yml` and `docs/schema/database.yml`
before the Data Architect Agent reviewed them. The Engineering Lead flagged the violation
mid-execution: "the Data Architect has authority over the api_contracts.yml and database.yml
files, we should be consulting that agent for review before committing."

The retroactive DA+Architect review found two substantive errors that would have shipped as
the implementation contract:

1. `scoring_basis` was labeled `"percentile_rank"` on ecological — semantically incorrect
   because ecological uses boundary-proximity scoring (entity-intrinsic by definition), not a
   cross-entity percentile rank. Fixed by extending the enum to three values:
   `"percentile_rank" | "normalized_absolute" | "boundary_proximity"`.
2. `mda_composite_floors` was listed in `db_reads` for the M9 trajectory endpoint — this
   table does not exist in M9. Moved to a comment.

A related note in the CM consultation template also labeled ecological `"percentile_rank"` and
was corrected in the same pass. These errors were caught only because the file authority
violation surfaced them. The rule exists so this review happens before committing, not after.

### What 'C' Means in Practice

A Required Consultant (C) entry means consultation must happen before the change is finalized —
not as a courtesy after the fact. The correct sequence:

1. Acting agent produces the draft change.
2. C agent reviews and provides input.
3. Acting agent incorporates the input (or documents disagreement for EL resolution).
4. Only then is the change committed.

Treating step 2 as optional ("I'll mention this to DA in the PR description") is notification,
not consultation. It violates the R/C boundary. C means two-way communication, and the decision
waits for that input. If the C agent's review would change the output — and the PR #429 incident
shows it will — then committing before that review produces incorrect artifacts.
