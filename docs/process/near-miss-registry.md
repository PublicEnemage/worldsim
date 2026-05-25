# WorldSim Near-Miss Registry

> **Artifact type:** Permanent institutional record
> **Maintained by:** PM Agent (R), Engineering Lead (A)
> **Update trigger:** Any near-miss identified during development, HORIZON sweep,
> or post-session review
> **Canonical location:** `docs/process/near-miss-registry.md`

This document catalogs near-misses encountered during WorldSim development — instances
where a process gap, authority ambiguity, or missing safeguard almost produced a harmful
outcome but was caught before it did. Each entry records what happened, what was at risk,
what caught it, and what process improvement resulted.

The epistemology is borrowed from Aviation Safety Management Systems: near-misses are
treated with the same rigor as actual incidents, because they are evidence that a hazard
exists and the defenses almost failed — without the cost of the failure itself. The
countermeasure is never "be more careful." It is always "redesign the system so careful
isn't required."

Entries appear in chronological order of occurrence.

Not all entries are failures. Some are anticipations — the Engineering Lead sensing a
structural gap before it caused a problem, naming it, and building the safeguard before
the incident occurred. These deserve equal recognition: they represent the safety culture
working at its best. Nine of the nineteen entries are anticipatory.

---

## NM-001 — Recency Bias Creating Scope Spiral

**Date:** ~2026-04-17 (Milestone 2 era)
**Milestone:** M2 — Simulation Core
**Detected by:** Engineering Lead (mid-session, expressed as cognitive load concern)
**Severity:** High — no PM structure existed; every new finding was displacing committed
work without a governed process for deciding what stayed and what deferred

### What happened

During Milestone 2, the Engineering Lead noticed a compounding pattern: every step forward
produced ten new steps, and the heat-of-the-moment tendency was to chase whatever had just
been found rather than protect committed work. A standards review produced five new blocking
issues before the two original blockers were resolved. Each discovery was individually
legitimate; together they were creating a scope spiral with no circuit breaker.

The Engineering Lead expressed it directly: "It's beginning to weigh on me that for every
step we take, we potentially add 10 new steps... I am worried that in the heat of the moment
our recency bias will make our attention focus on what we just found."

### What was at risk

Without a governed process for distinguishing committed work from newly discovered work,
milestones would never close. Every new finding would legitimately compete with existing
commitments, and the project would drift perpetually toward discovery rather than delivery.
The democratization mission depends on shipped software, not infinite scope expansion.

### What caught it

The Engineering Lead, recognizing the pattern from experience with delivery teams.

### Process improvement

**The PM Agent and HORIZON/BRIEF/TRIAGE command structure** (introduced M2-M3):
A dedicated PM Agent with explicit commands for session starts (BRIEF: what is committed,
what is blocking, what is the single next action), issue triage (TRIAGE: one verdict per
finding, no elaboration), and periodic sweeps (HORIZON: open-issue audit against milestone
definitions). The Architecture Backlog's explicit anti-recency-bias rule — requiring a
full backlog review before any new ADR is activated — is the direct descendant of this
concern applied to architectural decisions.

Documented in: `docs/process/agents.md §PM Agent`, `docs/architecture/backlog.md §Priority Review`

---

## NM-002 — Silent Artifact Placement in Wrong Directory

**Date:** ~2026-04-25 (Milestone 4 era)
**Milestone:** M4 — Scenario Engine
**Detected by:** Engineering Lead (noticed STD-REVIEW-003 was missing from expected location)
**Severity:** Medium — the artifact existed but was invisible to anyone following the
established convention; the project's structure was silently becoming incoherent

### What happened

STD-REVIEW-003 was written to a different directory than STD-REVIEW-001 and STD-REVIEW-002,
with no visible error. The Engineering Lead noticed it was not appearing in the expected
location: "Not sure if there is any guardrails we can put in place to prevent this kind
of silent mistakes from happening."

The root cause: the agent creating STD-REVIEW-003 did not check where prior artifacts of
the same type lived. It created a plausible-looking path without verifying the established
convention. No error was thrown. The artifact was just invisible to anyone following the
project's artifact structure.

This pattern had occurred before with the compliance scan registry ordering (SCAN-010
appearing after SCAN-011) — a different silent consistency failure with the same root cause.

### What was at risk

Over time, artifact sprawl in wrong locations degrades the project's institutional memory.
Future agents and contributors following the canonical paths find nothing, assume nothing
exists, and either recreate artifacts (duplication) or skip them (gaps). The project's
structure becomes incoherent faster than anyone notices.

### What caught it

The Engineering Lead, searching for the artifact and noticing its absence from the
expected location.

### Process improvement

**Pre-creation checklist and canonical artifact location table in CLAUDE.md**:
Before creating any document, the acting agent must check the canonical artifact
location table in CLAUDE.md to verify the correct path, filename convention, and whether
a file already exists at that path. The canonical locations table maps every artifact
type to its directory and naming convention.

Documented in: `CLAUDE.md §Canonical Artifact Locations`, `CLAUDE.md §Pre-creation checklist`

---

## NM-003 — Field Name Assumptions Without Reading the Schema

**Date:** ~2026-04-28 (Milestone 4-5 transition)
**Milestone:** M4-M5 transition
**Detected by:** Engineering Lead (during retrospective, pointed question about how this passed testing)
**Severity:** High — incorrect field names made it into production code and the test suite
passed; the failure mode was discovered during UI debugging, not by CI

### What happened

An endpoint was written by an agent that assumed the `simulation_entities` metadata
structure without reading the actual database schema. The agent wrote `SELECT name FROM
simulation_entities` when the actual column was `name_en`. Similar mismatches occurred
with `entity_name` in other locations. These field name errors propagated into production
code.

The Engineering Lead raised the question sharply during a retrospective: "How did field
name mismatches happen (name vs en_name vs entity_name)? If these kinds of guesses
continue to happen, are we not taking delivery risk? And if the wrong field names made
it into code, how did the tests pass?"

The answer was that tests were written against the same assumed field names as the
implementation — so the tests were internally consistent but both were wrong relative
to the actual schema. The test suite validated consistency, not correctness.

### What was at risk

An agent that guesses field names rather than reading the schema produces code that is
internally consistent but wrong relative to reality. If tests are written by the same
agent using the same assumptions, they pass. The failure only surfaces at integration
time or during UI debugging — after significant development has built on the wrong
foundation.

### What caught it

The UI failing to render data — discovered through manual testing, not CI. The Engineering
Lead connected the symptom to the root cause during retrospective.

### Process improvement

**Data Architect agent role and "read before writing" principle**:
The Data Architect agent was established with explicit authority over schema files.
Any agent writing code that touches database fields must read the relevant schema
documents before writing. The Data Architect reviews all schema-adjacent implementation
before merge. The file authority rule (NM-007) is the formalization of this principle
applied to document files.

Additionally, this near-miss established that **tests must be written against the actual
schema, not against the implementation's assumptions**. A test that passes because both
the implementation and the test share the same wrong assumption is not a passing test —
it is a gap in the test strategy.

Documented in: `docs/process/agents.md §Data Architect Agent`,
`CLAUDE.md §Tests are not optional`

---

## NM-004 — Smoke Testing Not Institutionalized After Discovering Its Value

**Date:** ~2026-04-29 (Milestone 5 era)
**Milestone:** M5
**Detected by:** Engineering Lead (during session, asked whether the practice would be repeated)
**Severity:** Medium — the test existed but was not in CI, not in the PR template,
not referenced in any agent prompt; it would not repeat without deliberate action

### What happened

A smoke test was run ad hoc after UI failures surfaced during integration. It was effective
— it caught issues before they reached users. The Engineering Lead asked whether this
practice would be institutionalized: "Do we feel we are unlikely to repeat the breakage
we had in the UI? I am worried we are glossing over another structural issue in how we
develop software."

The honest answer at the time was: "No, we are not yet institutionalized on either front.
The smoke test we ran was written ad hoc, after failures, as a one-off script. It is not
in CI. It is not in the PR template. It is not referenced in any agent prompt template.
It lives nowhere in the project except as a memory."

The pattern: a valuable practice was discovered reactively, used once, and then forgotten
because no process ensured it would be repeated.

### What was at risk

Without institutionalization, every valuable practice discovered reactively is a one-time
event. The project learns from failures but does not encode that learning into repeatable
process. The same failure mode recurs, the same ad hoc fix is applied, and the cycle
continues. Delivery quality degrades in proportion to how many practices are reactive
rather than structural.

### What caught it

The Engineering Lead, asking the follow-up question that turned a one-time fix into a
structural requirement.

### Process improvement

**Playwright integration and CI test gates**:
Playwright was adopted as the primary integration testing framework, with tests running
in CI on every PR. The narrated demo infrastructure (`demo-narrated.spec.ts`) serves
dual purpose: stakeholder demonstration and automated regression testing. M9 exit gates
include Playwright demo advancement tests and legibility assertions as explicit CI
requirements — issues #376 and #377. The principle that a practice is not institutionalized
until it is in CI applies to all future testing practices.

Documented in: `docs/process/agents.md §QA Lead Agent`,
M9 exit checklist (Issue #213)

---

## NM-005 — Agent Consultation Was Confirmatory, Not Generative

**Date:** ~2026-05-13 (Milestone 7 era)
**Milestone:** M7 — Technical Foundation
**Detected by:** Engineering Lead (mid-session, recognized the pattern after it had
already occurred)
**Severity:** High — domain agents were being asked to validate decisions already made
rather than contribute to decisions being formed; this is a structurally weaker review

### What happened

During M7 Standards Review work, the team drafted gap recommendations and dispositions,
then brought in the Data Architect, QA Lead, and Architect agents to review them. The
Engineering Lead recognized the problem mid-session: "We should really get the Data
Architect and QA Lead agents to weigh in on the gaps recommendations before we commit
to them. In fact, we should have deferred to them for their opinion, rather than asking
them to rubber stamp ours. But we will do better in the future."

The agents were activated after the framing was already established, asked to find holes
in decisions that had already been made. This is confirmatory consultation — structurally
weaker than generative consultation, where agents are asked cold: "Here are the gaps.
What do you see?"

### What was at risk

Confirmatory consultation has two failure modes. First, agents may anchor to the existing
framing and miss gaps they would have identified independently. Second, it creates the
appearance of review without its substance — the decision was already made, the agents
are validating rather than contributing. A genuine finding that contradicts the existing
disposition faces institutional resistance ("we already decided this") that a finding
made before disposition does not.

This near-miss recurred two weeks later as NM-006 (ADR panel omitting the Frontend
Architect) — the same pattern of consultation being added after framing rather than
before it.

### What caught it

The Engineering Lead, recognizing the governance principle mid-session: "agent consultation
should be generative, not confirmatory."

### Process improvement

**RACI-grounded panel composition rule and generative consultation principle**:
The principle is now documented in `docs/process/agent-raci.md §ADR Panel Composition`:
panel members are activated before the ADR is framed, not after. The six-agent parallel
consultation pattern (activated during M9 FA brief work for DA-F2/F4/F5) is the correct
application — six agents asked cold, "here are the open questions," producing independent
findings before any disposition was established.

The consulting agent's working agreement in `docs/process/agents.md` now explicitly states
that C agents must be consulted during formation of decisions, not after.

Documented in: `docs/process/agent-raci.md §ADR Panel Composition`,
`docs/process/agents.md §Agent Working Agreements`

---

## NM-006 — ADR Panel Omitted the Implementing Agent

**Date:** 2026-05-21
**Milestone:** M9 — Standards Foundation
**Detected by:** Engineering Lead (post-session review before ADR acceptance)
**Severity:** High — ADR-008 would have committed to frontend architecture without
the Frontend Architect confirming feasibility on target hardware

### What happened

ADR-008 (UX Architecture) was drafted with a review panel of UX Designer, Chief
Methodologist, and Development Economist. The Frontend Architect — the agent who would
implement everything the ADR committed to — was absent from both the drafting
consultation and the panel review.

The omission occurred because the panel was copied from the M8 critique panel, which was
appropriate for a conceptual framing question but wrong for an ADR governing frontend
implementation. The question had changed from "is the frame right?" to "can this be
built?" — but the panel composition did not change with it.

This is NM-005 recurring two weeks later in a different form: consultation structure
was inherited from a prior context without checking whether that context still applied.

### What was at risk

ADR-008 contains implementation-specific commitments: minimum viewport dimensions, state
management architecture, rendering performance constraints, control plane zone width. These
require Frontend Architect feasibility input — not as a formality but because the Frontend
Architect is the only agent who knows whether the commitments are achievable on target
hardware (4-core laptop, GitHub Actions free-tier runner). An ADR accepted without that
input could have committed to an unbuildable architecture that would require fundamental
restructuring at M10 implementation time.

### What caught it

The Engineering Lead, identifying the omission during session review before the ADR
was accepted.

### Process improvement

**RACI-grounded panel composition rule** (PR #414, Issue #405):
Before naming any ADR panel, the Architect Agent must consult `docs/process/agent-raci.md`.
Any agent listed as R or C for the decision type must be included in the panel or their
exclusion explicitly documented with rationale. The implementing agent is always required
regardless of panel size.

**Minimum panel by ADR type:**
- Frontend architecture ADR → Frontend Architect required
- Engine ADR → Chief Engineer required
- Data standards ADR → Chief Methodologist required
- UX design ADR → UX Designer required

Documented in: `docs/process/agent-raci.md §ADR Panel Composition`,
`docs/architecture/backlog.md §Panel Composition Rule`,
`docs/CODING_STANDARDS.md §ADR Requirements`

---

## NM-007 — Schema Files Committed Without Data Architect Review

**Date:** 2026-05-23
**Milestone:** M9 — Standards Foundation
**Detected by:** Engineering Lead (during session, after commit but before merge)
**Severity:** High — two schema errors would have merged to main without detection

### What happened

The Architect Agent wrote directly to `docs/schema/api_contracts.yml` and
`docs/schema/database.yml` and committed them as part of ADR-010 amendments (PR #429),
without prior Data Architect review. Per `docs/process/agent-raci.md` Row 4, the Data
Architect holds R on both files.

The Data Architect review, when activated after the Engineering Lead flagged the missing
review, found and corrected two errors:

- **DA-R2:** `db_reads` listed `mda_composite_floors` — a table that does not exist
  in M9. This would have misled any implementation agent reading the contract.
- **DA-R3:** `scoring_basis` field used a two-value enum `["percentile_rank",
  "normalized_absolute"]`, incorrectly labeling ecological scoring as `"percentile_rank"`.
  Ecological uses boundary-proximity scoring — categorically different from a cross-entity
  percentile rank. The correct three-value enum is `["percentile_rank",
  "normalized_absolute", "boundary_proximity"]`.

A contributing cause: the Chief Methodologist consultation document had included a schema
enum definition outside CM authority. The CM's authority is methodology conclusions; the
DA's authority is schema representation of those conclusions. The CM overstepped into
schema territory and produced an incorrect definition that propagated into the ADR and
API contract before the DA caught it.

This is NM-005 recurring again: an agent (the Architect) acted in a domain belonging to
another agent (the DA) without the required consultation. The pattern has now appeared
three times across three milestones.

### What was at risk

If the Engineering Lead had not flagged the missing DA review, both errors would have
merged to main and been consumed by the trajectory endpoint implementation. The
`scoring_basis` error would have produced incorrect frontend display logic for ecological
curves — displaying them as if they were percentile-rank composites, which they are not.
A finance ministry analyst using Mode 1 to examine a country's ecological trajectory
would have seen methodologically incorrect curve labels.

### What caught it

The Engineering Lead, noticing the DA review was missing after the commit.

### Process improvements

**File authority rule** (PR #432, Issue #431):
Before writing to any file, the acting agent must verify they hold R on that file in
`docs/process/agent-raci.md`. If another agent holds R, the acting agent must produce
a draft and request the owning agent's review before committing.

**File ownership table** (PR #433, Issue #431):
A lookup table in `docs/process/agent-raci.md §File Ownership` maps every significant
file and directory to its owning agent (R) and required consultants (C).

**HORIZON file authority audit** (PR #433, Issue #431):
The PM Agent HORIZON sweep now includes a file authority audit step: scan PRs merged
since the last sweep for violations — an agent writing to a file owned by another agent
without a review comment from the owning agent.

**CM consultation scope boundary** (this registry):
Chief Methodologist consultation documents must not include schema definitions. The CM
produces methodology conclusions; the Data Architect produces schema representations of
those conclusions in a separate deliverable that references the CM artifact.

Documented in: `CLAUDE.md §File authority is non-negotiable`,
`docs/process/agent-raci.md §File Ownership`,
`docs/process/agents.md §PM Agent HORIZON`

---

## NM-008 — Domain Expertise Gap: No Real-World Economist in the Room

**Date:** ~2026-04-17 (Milestone 2 era)
**Milestone:** M2 — Simulation Core
**Detected by:** Engineering Lead (anticipation — before any scenario had run)
**Severity:** High — without domain expertise, simulation economic relationships would be calibrated against theoretical assumptions, not real-world evidence
**Type:** Anticipatory — caught before the gap caused a failure

### What happened

During Milestone 2, before any scenario had been run, the Engineering Lead sensed a structural gap: "I am sensing the need for another agent — almost like a business product manager who has the background of a first-class economist, keeps a pulse on historical and current economic and political trends, and has a seat at the table when we discuss even the first dry run on bare rails."

The timing was deliberate: this concern was raised before the model's assumptions had been baked in through repeated use without challenge. The risk was not current — it was structural. An agent team with no domain economics expertise would calibrate relationships against internal consistency rather than empirical evidence from actual sovereign debt crises.

### What was at risk

A simulation built without economic domain expertise would produce outputs that look internally consistent but fail to match historical cases. The entire backtesting framework — and the credibility of WorldSim's findings in a negotiating room — depends on the model's economic relationships being calibrated against real-world evidence, not theoretical assumptions made by software engineers.

### What caught it

The Engineering Lead, anticipating the gap before it caused a failure. This is the safety culture working at its best: the hazard was identified before an incident, not after.

### Process improvement

**Development Economist role in the Domain Intelligence Council**:
The Development Economist agent was established as a first-class DIC member with explicit authority to validate economic relationships, challenge calibration assumptions, and flag cases where the model's behaviour diverges from historical evidence. The role's working agreement commits to active challenge, not passive validation.

Documented in: `docs/process/agents.md §Development Economist`,
`docs/agents/domain-intelligence-council.md`

---

## NM-009 — Groupthink Risk: No Counter-Perspective in the Council

**Date:** ~2026-04-17 (Milestone 2 era)
**Milestone:** M2 — Simulation Core
**Detected by:** Engineering Lead (anticipation — recognized structural lean during council composition discussion)
**Severity:** Medium — a council with homogeneous perspective would produce groupthink rather than genuine challenge
**Type:** Anticipatory — caught during design, before the council was used

### What happened

While composing the Domain Intelligence Council, the Engineering Lead raised a concern about structural bias: "What about adding an Investment/Capitalist oriented agent to bring the perspective of the art of the possible, in contrast to the likely risk-averse and short/medium tendencies that the current members are likely to lean towards?"

The concern was not about any individual agent but about the composition as a whole: a council weighted toward risk-averse, welfare-oriented perspectives would consistently produce conservative outputs, potentially missing the investment and capital formation dimension that affects whether sovereign programmes actually work in practice.

Claude's response confirmed the structural risk: "You're not just adding agents, you're recognizing that the Domain Intelligence Council needs to reflect the full complexity of the decisions WorldSim will inform."

### What was at risk

A homogeneous council produces validation rather than challenge. If all council members share the same analytical frame, the council's output will consistently reinforce existing model assumptions rather than surface their blindspots. For a tool designed to serve as kryptonite in asymmetric negotiations, a council that produces consensus without dissent is actively harmful.

### What caught it

The Engineering Lead, recognizing the groupthink risk during council composition rather than after the first review produced uninformative consensus.

### Process improvement

**Diverse DIC composition with explicit counter-perspectives**:
The council was expanded to include agents representing perspectives that would constructively challenge the dominant welfare/risk-averse framing: Investment and Capital Formation, Trade and Geopolitical dynamics, and others reflecting the full range of actors in the rooms WorldSim is designed to inform. The blind interview process (NM-013) was the eventual mechanism for ensuring council members contribute genuine independent perspectives.

Documented in: `docs/agents/domain-intelligence-council.md`

---

## NM-010 — UX North Star Had No Owner

**Date:** ~2026-05-06 (Milestone 5-6 era)
**Milestone:** M5-M6 transition
**Detected by:** Engineering Lead (anticipation — noticed the gap before it produced a UI without coherent vision)
**Severity:** High — without a UX north star, the Frontend Architect would build structurally sound components with no unified user experience intent
**Type:** Anticipatory — caught before the full extent of the gap was visible in the UI

### What happened

The Engineering Lead noticed that the UI, while technically functional, lacked a coherent user experience vision: "I am thinking we may need to add a UX designer agent at some point soon. Someone needs to feed the intellectual problem space for the UI Frontend Architect, and right now that problem space will be dominated by untangling what we have built, but no voice of what the UX north star should be."

Claude's response named the structural gap: "The Frontend Architect answers 'how should this be built.' It has no mandate to answer 'what should be built and why.' Without a UX Designer, the instrument cluster will be optimized for technical correctness but not for the cognitive load of a finance minister in a negotiation room."

This concern was later confirmed when the M8 demo review found that the instrument cluster had the right components in the wrong relationship — a Case B verdict requiring a fundamental UX architecture rethink.

### What was at risk

A tool built without a UX north star will be coherent at the component level and incoherent at the user experience level. The finance ministry analyst sitting across from the IMF cannot afford cognitive friction — every second spent navigating to find an instrument is a second not spent on the argument. A technically correct but experientially incoherent tool fails its users in the room where it matters most.

### What caught it

The Engineering Lead, anticipating the gap from experience with product development rather than waiting for user feedback to surface it.

### Process improvement

**UX Designer Agent established with north-star authority**:
The UX Designer agent was established with R on all UX documents and authority to define the instrument cluster's cognitive model, zone hierarchy, and interaction principles. The three-mode architecture (Mode 1/2/3), the six governing premises, and the Case B UX architecture verdict are all products of this agent having genuine authority over the UX frame.

Documented in: `docs/process/agents.md §UX Designer Agent`,
`docs/ux/north-star.md`, `docs/ux/information-hierarchy.md`

---

## NM-011 — Schema Had No Owner: Data Architect Role Created

**Date:** ~2026-04-29 (immediately following the field name mismatch incident)
**Milestone:** M4-M5 transition
**Detected by:** Engineering Lead (anticipatory — proposed the structural fix directly after the NM-003 incident)
**Severity:** High — without a schema owner, the field name assumption failure mode would recur on every new endpoint
**Type:** Anticipatory — the structural fix was proposed before the next recurrence

### What happened

Directly following the field name mismatch incident (NM-003), the Engineering Lead proposed the structural fix: "We may need a versioned schema source of truth, owned by a Data Architect Agent who can watch out for schema field naming conventions and other data quality standards. If we had this schema source of truth, the QA agent could have used it as input when designing test cases."

Claude's response confirmed: "If a Data Architect Agent had maintained a schema registry that defined the canonical shape of every data structure, the field name assumption that caused the bug would have failed at spec time, not at runtime."

### What was at risk

Without a schema owner, every new agent writing to the database would independently assume field names rather than reading an authoritative source. The NM-003 failure mode was structural, not incidental — it would recur on every new endpoint.

### What caught it

The Engineering Lead, connecting the incident to its structural cause and proposing the preventive architecture immediately rather than treating the incident as a one-off.

### Process improvement

**Data Architect Agent established as schema file owner**:
The Data Architect holds R on `docs/schema/api_contracts.yml`, `docs/schema/database.yml`, and `docs/schema/simulation_state.yml`. All agents writing code that touches database fields must reference these files before writing. The file authority rule (NM-007) later formalized this into a project-wide principle.

Documented in: `docs/process/agents.md §Data Architect Agent`,
`docs/process/agent-raci.md §File Ownership`

---

## NM-012 — Matrix Compute Needed a Different Knowledge Profile

**Date:** ~2026-05-15 (late Milestone 6 / early M7 era)
**Milestone:** M6-M7 transition
**Detected by:** Engineering Lead (anticipation — recognized the gap before matrix implementation had begun)
**Severity:** High — without a Chief Engineer, matrix computation decisions would be made by the Architect Agent, whose knowledge profile is system design, not compute optimization
**Type:** Anticipatory — caught before any matrix code was written

### What happened

Following a discussion about matrix arithmetic and the NOAA ensemble forecast insight, the Engineering Lead proposed a new role: "Given our discussion about matrix computation, should we on-board a Chief Engineer agent? The role is separate from the architect role because you need more nitty-gritty knowledge about CPU compute optimization, matrix math, ensemble computation."

Claude's response confirmed the knowledge profile gap: "The matrix arithmetic work requires a different knowledge profile than what the Architect Agent brings. The Architect Agent reasons about system design, ADR structure, and module boundaries. The Chief Engineer needs to reason about instruction-level performance, memory access patterns, numerical precision, and hardware constraints on the target 4-core laptop."

### What was at risk

The simulation engine is the load-bearing substrate of everything WorldSim does. A matrix compute transition designed by an agent without the relevant knowledge profile could produce an engine that is fast on development hardware but slow on the target 4-core laptop — failing the equity requirement. The Swiss watch principle applies here precisely.

### What caught it

The Engineering Lead, recognizing that the technical depth of the matrix transition exceeded the Architect Agent's mandate before any implementation had been attempted.

### Process improvement

**Chief Engineer Agent established with compute substrate authority**:
The Chief Engineer holds authority over engine performance decisions, baseline benchmarks, A/B validation methodology, and stress test design. ADR-009 (engine computation model) cannot be authored until the Chief Engineer completes Phase 1 baseline benchmarks — a hard constraint preventing speculative architectural commitments.

Documented in: `docs/process/agents.md §Chief Engineer Agent`,
`docs/architecture/backlog.md` (ARCH-003, ADR-009 constraint)

---

## NM-013 — The DIC Had Never Been Asked the Foundational Question

**Date:** ~2026-05-07 (post-M6 demo)
**Milestone:** M6-M7 transition
**Detected by:** Engineering Lead (post-demo reflection — recognized an unused capability)
**Severity:** High — the Domain Intelligence Council had existed for months but had only been used for technical validation, never asked whether the approach would actually serve its intended users
**Type:** Anticipatory — caught before the tool reached institutional adoption

### What happened

After the M6 stakeholder demo, the Engineering Lead reflected: "It would be interesting to do a similarly blind stakeholder analysis interview with the domain council, to get their feedback on the problem we have identified and our approach to solving it. I think there is something very valuable at our fingertips — we just haven't asked yet."

Claude's response named the gap: "The Domain Intelligence Council has been used primarily in a supporting role — validating ADR decisions, contributing elasticity citations, flagging methodological gaps. They haven't been asked the foundational question: do you believe this approach will serve the users it claims to serve?"

The DIC blind interview that followed produced convergent findings that reshaped architectural priorities: DIRECTION_ONLY fidelity is insufficient for negotiating credibility; ecological and social modules need bidirectional event flow; asymmetric temporality between recoverable and irreversible damage was unrepresented. These were foundational gaps that months of internal development had not surfaced.

### What was at risk

A tool built without ever asking its intended users whether the approach was right could reach institutional adoption with structural gaps in its core analytical model. The finance ministry analyst needs more than directionally correct outputs — they need magnitude credibility. A tool that cannot provide that fails its mission regardless of how technically sophisticated it is.

### What caught it

The Engineering Lead, connecting the M6 demo's independent stakeholder review pattern to the DIC as a resource that had not yet been asked the hardest question.

### Process improvement

**DIC blind interview process established** (M8 entry gate):
All nine DIC members are independently interviewed before major architectural decisions. Each is asked cold — with no prior exposure to existing design choices — whether the approach will serve the intended users. Convergent findings across independent interviews carry high evidential weight.

Documented in: `docs/process/council-interview-prompt.md`,
`docs/process/agents.md §Domain Intelligence Council`

---

## NM-014 — File Edit Reported as Complete Without Commit

**Date:** 2026-05-23
**Milestone:** M9 — Standards Foundation
**Detected by:** Engineering Lead (reviewing session output, noticed "agents.md changes from
earlier are still uncommitted")
**Severity:** Medium — the change was recoverable (bundled into the next PR), but was reported
as complete when it existed only as a local unstaged edit

### What happened

An EXECUTE instruction contained two actions: file a GitHub issue (Action 1) and add the
Business Product Owner Agent working agreement to `docs/process/agents.md` (Action 2).

Action 1 produced an external artifact — a GitHub issue URL — making completion unambiguous.
Action 2 was a file edit. The file was edited and the task was reported as done with
"confirmation agents.md was updated." The change was never committed. It sat as an unstaged
local edit on main.

When the user continued with the next task, a `git checkout main` was issued before creating
a new branch. At that point the agent noticed the unstaged change and bundled it into the
subsequent PR (#442) rather than losing it. The Engineering Lead caught the pattern from
output text: "agents.md changes from earlier are still uncommitted. I'll include them in this
PR together with the RACI additions."

### What was at risk

If the session had ended, or if `git restore` or `git checkout -- .` had run for any reason,
the agents.md change would have been lost — with no record of the loss, because it had already
been reported as complete. The branch discipline rule (all changes on a branch + PR; direct
commits to main are a governance deviation) was not applied at all — not even a commit to main,
just an uncommitted local edit.

### What caught it

The Engineering Lead, reading the agent's own output in the next task. This was not caught by
any process — it was caught by a human noticing an admission buried in a status sentence. There
is no automated gate between "file edited" and "change committed."

### Process improvement

**Personal commit gate — a file change is not reportable as complete until it is on a branch
and committed:**
The branch discipline rule applies regardless of prompt style or whether a branch was
explicitly specified in the EXECUTE instruction. An EXECUTE that includes a file change with
no specified branch requires the agent to create a branch, commit the change, and report the
PR URL — not to edit the file and report the edit. "Confirmation X was updated" must mean
"X is committed on a branch and in a PR," not "X has new content locally."

### Systemic root cause — the micro-management cycle

The documented root cause (agent did not apply standing branch discipline
rules) is accurate but incomplete. The deeper cause is a compounding cycle
that had developed across M7–M9:

1. An agent made a mistake or near-miss
2. The response was to add more specification to the next prompt
3. Each addition was individually justified — it addressed a real gap
4. Together, the additions shifted prompting culture toward micro-management
5. Prescriptive prompts reduced agent reasoning — when told exactly what
   to do and how to report it, agents match the specified success criteria
   literally rather than applying standing project rules from first principles
6. Reduced reasoning made standing rules less likely to be applied
   automatically
7. Which produced more mistakes
8. Which prompted more specification
9. The cycle accelerated

This is a well-documented failure mode in human organizations. A tech lead
or director who compensates for team mistakes by becoming more prescriptive
produces a team that is compliant but not capable — one that cannot function
without exhaustive instruction. The load accumulates on the lead until
something breaks. The correct response to the first leak in the dam is a
structural fix, not a finger.

The correct response to NM-014 is not "add a completion criteria checklist
to every prompt." It is to restructure where specification lives:

- **Issues carry the prescription** — what to produce, what done looks like,
  what the acceptance criteria are. Issues are durable, reviewable,
  version-controlled. Anyone — human or agent — can pick up an issue and
  have the same instructions.
- **Standing documents carry the rules** — CLAUDE.md, agent-raci.md,
  the near-miss registry. Agents read these before executing. Rules do not
  need to be re-specified in every prompt.
- **Agents write their plan before executing** — before touching any file
  or opening any branch, the agent states what it is going to do, which
  documents it is reading, what branch it will use, and what the PR will
  contain. This plan is the review surface. It can be corrected before
  any implementation happens — without requiring the Engineering Lead to
  have specified every detail in advance.
- **Prompts are outcome-oriented** — "Execute Issue #NNN. Write your plan
  first. Follow all standing project rules." The agent's reasoning fills
  the gap, not the prompt's length.

### Contributing factor under investigation

Prescriptive EXECUTE prompts — those that specify exact steps and per-action
success criteria — reduce agent reasoning about what constitutes completion.
In NM-014, Action 2's success criterion was stated as "confirmation agents.md
was updated," which the agent matched literally (file has new content) rather
than by the project's standing completion standard (change is committed and
in a PR).

A less prescriptive instruction — "add the Business Product Owner Agent to
agents.md" — would have required the agent to reason about what "done" means
from first principles, which naturally includes the delivery chain:
edit → branch → commit → PR → report URL.

The weight of prescriptive prompting as a contributing factor is confirmed
as significant, not merely a possibility. The primary and systemic root cause
is the micro-management cycle described above. Prescriptive prompting is both
a symptom of that cycle and a mechanism that perpetuates it.

Documented in: `CLAUDE.md §Blameless continuous improvement is non-negotiable`,
`docs/process/agent-raci.md §File Ownership` (branch discipline rule),
`docs/process/near-miss-registry.md §The recurring pattern` (systemic cause
added 2026-05-23)

---

## NM-015 — CI Gate Job Not a Required Status Check

**Date:** 2026-05-23
**Milestone:** M9 — Standards Foundation
**Detected by:** Engineering Lead (root-cause analysis of PR #443 CI failure)
**Severity:** High — the `changes` path-filter job, which gates all downstream CI jobs, was not
a required status check; `compliance-scan` was also absent from the required set; branch
protection had the correct intent but incomplete implementation

### What happened

During root-cause analysis of the `actions/checkout@v6` regression that failed PR #443, an
audit of branch protection settings revealed that `changes` — the path-filter job that always
runs and controls which downstream jobs execute — was not a required status check. Only three
conditional downstream jobs (`lint`, `test-backend`, `playwright-e2e`) were required.
`compliance-scan` was also absent.

The structural gap: when `changes` fails, all jobs that `need: changes` are skipped due to
failed-dependency propagation. Jobs skipped this way — unlike jobs legitimately skipped by
their own `if:` condition — may not satisfy required check rules. Branch protection was
configured to require the *outputs* of the gate, not the gate itself. Whether merges were
actually blocked during the broken-CI period depends on how GitHub evaluates dependency-skipped
versus condition-skipped jobs; the configuration made that determination ambiguous rather than
unambiguous.

The `actions/checkout@v6` action had reportedly worked since its January 2026 release date,
then regressed sometime before PR #443. Because M9 work has been predominantly documentation
changes, CI failures were minimally visible — all downstream jobs were skipped on docs-only PRs
regardless of whether `changes` succeeded, making a `changes` failure indistinguishable from a
legitimate docs-only skip in the PR status view.

### What was at risk

Any PR merged during the broken-CI period could potentially have merged without test or
compliance validation. The compliance-scan job — which runs machine-detectable violation checks
documented in `docs/compliance/scan-registry.md` — was not in the required set at all,
meaning it was never a blocking gate even when CI was healthy.

### What caught it

Root-cause analysis triggered by the PR #443 CI failure. An explicit inspection of branch
protection settings (`gh api repos/PublicEnemage/worldsim/branches/main/protection`) revealed
the gap. The gap would not have been surfaced without actively examining the protection
configuration — there is no process that routinely audits required status checks against the
current workflow graph.

### Process improvement

**Immediate remediation (out-of-band, no PR required):** `changes` and `compliance-scan` added
to required status checks via GitHub API during the same session the gap was identified.
Required checks are now: `changes`, `test-backend`, `lint`, `playwright-e2e`, `compliance-scan`.

**Structural rule:** Required status checks must include the root gate job (`changes`), not only
its downstream dependents. When the dependency graph changes — a new gate job is introduced, or
an existing gate is restructured — required status checks must be audited in the same commit.

**Milestone exit checklist addition:** A checkpoint confirming required status checks match the
current workflow gate structure is added to the M9 exit checklist.

---

## NM-016 — Lint Gate Absent from Agent Prompts: Two PRs Failed CI on Trivially-Preventable Errors

**Date:** 2026-05-23
**Milestone:** M9 — Standards Foundation
**Detected by:** Engineering Lead (CI failure on PR #468 and PR #469)
**Severity:** Medium — no incorrect artifacts produced; CI caught the errors; two fix
commits required and merge delayed

### What happened

Two parallel worktree agents (implementing Issues #458 and #459) opened PRs without
running `ruff check .` locally. Both PRs failed the CI lint job immediately.

Errors caught by CI but not locally:
- `I001` (import block unsorted) in three files — auto-fixable by `ruff --fix` in seconds
- `E501` (line > 100 chars) in two files — manual fix under 30 seconds each

Root cause: the agent prompts specified `pytest` as the PR readiness check. Neither prompt
mentioned `ruff check .`. The agents treated "tests pass" as "PR ready."

The local ruff binary is `ruff==0.7.2` — identical to the CI-pinned version in
`requirements.txt`. There is no environment difference. Every error CI caught was
catchable locally in two seconds.

### What was at risk

In this instance: merge delay and two fix commits. In a higher-stakes case, an agent
that skips the lint gate before pushing could introduce style violations that accumulate
across a feature branch, requiring a separate cleanup commit or blocking a time-sensitive
merge.

### What caught it

CI — which is the right gate but the wrong place for this to be caught first. The
process had no local gate between "implementation complete" and "push." CI filled that
gap, but at the cost of a push-fix-push cycle that a two-second local check would have
eliminated.

### Process improvement

**Pre-push lint gate added to CLAUDE.md** (this PR, Issue #471):
The rule is now in the permanent constitution — not in agent prompts. Every agent reads
CLAUDE.md at session start. The rule reads:

> Before pushing any branch that modifies files under `backend/`, run:
> `cd backend && ruff check . && mypy app/`
> Both must exit 0. CI is a confirmation, not a discovery mechanism.

Future backend agent prompts do not need to specify `ruff check` — the rule applies
automatically from the constitution. This is the NM-014 lesson applied: prescription
belongs in standing documents, not in every prompt.

Documented in: `CLAUDE.md §Backend pre-push lint gate`

---

## NM-017 — Story–Test–Implementation Decomposition Mismatch: 16 ACs Suppressed by Blanket Skip

**Date:** 2026-05-23
**Milestone:** M9 — Standards Foundation
**Detected by:** Engineering Lead (anticipatory — structural gap sensed through governance anxiety about skip management before any defect occurred)
**Severity:** High — the blanket skip created a CI blind spot across 16 acceptance criteria for the instrument cluster's primary viewport. Had components shipped without the skip being removed, defects in the instrument cluster — what the finance minister actually sees — would have passed CI undetected.

### What happened

User stories for the M9 instrument cluster were correctly authored at the zone level: "all four Zone 1 instruments visible simultaneously without scroll." QA then authored a single spec file (Issue #459, `frontend/tests/e2e/instrument-cluster.spec.ts`) covering all 16 ACs derived from those stories. Implementation was simultaneously decomposed into three separate Task Issues: #460 (TrajectoryView), #461 (MDA Alert Panel), #462 (PMM + Four-Framework).

The spec file contained two structurally distinct kinds of tests bundled together:

- **Component-level ACs** (AC-003 through AC-014): testable the moment a single component ships, independent of the others. Example: "TrajectoryView width ≥ 480px at 1024×768."
- **Zone-level integration ACs** (AC-001, AC-002): only satisfiable when all four instruments coexist simultaneously. Example: "All four Zone 1 instruments visible without scroll."

Because the file contained zone-level ACs, no test in the file could pass until all three implementation tasks were complete. The entire file was suppressed with `test.skip(true, ...)`. Three agents (Architect, Frontend Architect, QA Lead) were consulted on skip governance controls — CI guards, skip registries, DOM-presence fixtures — before the Engineering Lead identified the root cause: the suppression was a symptom of the wrong decomposition, not a skip management problem requiring new tooling.

The skip governance anxiety was real and appropriate. The underlying cause was that the sequence "stories → tests → implementation" had been followed faithfully, but without a rule governing how test granularity must match implementation granularity when implementation is decomposed by component.

### What was at risk

Sixteen acceptance criteria for the instrument cluster — the primary viewport of a tool used by finance ministers in high-stakes negotiations — suppressed in CI with no automated signal that they were unverified. If any of the three implementation tasks shipped and the skip was not removed, any defect in the zone-level layout commitment would pass CI and reach production. The reputational consequence of a visible defect in the primary instrument cluster for an institutional user would be significant.

This is the class of failure where the test suite reports green, a human feels safe, and a real defect exists. That is the worst-case test failure mode.

### What caught it

The Engineering Lead — sensing that the governance anxiety about skip management was disproportionate to what the skip was actually protecting. The question "why do we need complex automated controls for a simple skip?" led to the root cause: the skip was covering a mismatch in decomposition, not a genuinely unavoidable pre-implementation state. This is an anticipatory near-miss: the structural gap was named before any component shipped, before any defect could have slipped through.

### Process improvement

**Root cause:** No rule existed requiring ACs to be categorized by testability scope before QA authors a spec. Zone-level ACs (requiring multiple components) and component-level ACs (requiring one component) were bundled in a single file because the process gave QA a flat list of ACs with no categorization discipline.

**Two-part response:**

**1. One-time retrofit (Issue #473):** Restructure `instrument-cluster.spec.ts` — remove the blanket skip, move component-level ACs into each implementation task's scope (#460, #461, #462), rename the remaining file to `instrument-cluster-integration.spec.ts` containing only AC-001 and AC-002 with an explicit dependency header.

**2. Standing process change (Issue #474):** Document the Type 1 / Type 2 AC categorization rule in:
- QA Lead working agreement (`docs/process/agents.md`): before authoring any spec, categorize each AC as component-level (Type 1, lives in implementation task scope) or integration-level (Type 2, lives in dedicated integration spec with explicit component dependencies named).
- PO Agent working agreement (`docs/process/agents.md`): before commissioning a QA task, confirm ACs have been categorized by type. A QA task that spans both types must produce two outputs.
- `docs/CODING_STANDARDS.md §Testing`: document the pattern as a standing coding standard.

The fix is a decomposition discipline, not a skip governance mechanism. If decomposition is correct, skips are either unnecessary or are a small, explicitly-labelled set with a clear dependency statement — not a blanket suppression requiring automated expiry controls.

---

## NM-018 — Hammer-Nail: Technical Panel Produced Engineering Solutions to a Process Problem

**Date:** 2026-05-23
**Milestone:** M9 — Standards Foundation
**Detected by:** Engineering Lead (anticipatory — the divergence between technical panel output and product/design agent output was recognized before any engineering recommendation was implemented)
**Severity:** High — the panel was converging on significant tooling investment (CI skip-expiry guard, skip registry, DOM-presence fixture) to solve a problem whose root cause was a two-line decomposition discipline rule. Had those recommendations been implemented, the correct fix would have been buried under tooling complexity, and the underlying decomposition gap would have remained.
**Type:** Anticipatory — caught after consultation but before implementation of any recommendation

### What happened

When `test.skip(true, ...)` in `instrument-cluster.spec.ts` raised governance anxiety, the Engineering Lead activated the natural panel for a skip governance question: Architect, Frontend Architect, and QA Lead. All three produced engineering responses — a CI guard enforcing skip expiry, a skip registry with mandatory lifecycle tracking, a DOM-presence fixture enabling partial test execution before all components shipped.

The proposals were internally coherent and technically sound. They answered the question as posed: "How do we ensure skips are not forgotten or abused?"

The PO Agent and UX Designer Agent were activated subsequently to examine whether the decomposition process had contributed to the problem. Both immediately reframed the question: the skip existed because zone-level ACs and component-level ACs had been bundled in a single spec without a categorization discipline. The skip was not a governance problem requiring new tooling — it was a symptom of a missing decomposition rule. Once the rule existed (Type 1 / Type 2 AC categorization, documented in `docs/CODING_STANDARDS.md §E2E Pre-implementation Test Categorization`), the skip was unnecessary.

The technical panel had answered the wrong question correctly. The product/design agents asked the right question first.

### What was at risk

If the engineering recommendations had been implemented, the project would have added:
- A CI skip-expiry guard
- A skip registry with mandatory annotations
- A DOM-presence fixture infrastructure

...to solve what was actually a missing two-line rule in CODING_STANDARDS.md and two-paragraph updates to two working agreements. The tooling would have legitimized the blanket skip pattern by providing governance for it, rather than eliminating it. Future QA authors would have encountered the skip registry and inferred that blanket skips with registry entries were the correct practice.

This is the hammer-nail failure mode applied to process design: when the consultation panel is composed entirely of technical agents, every problem — including process problems — presents as a technical problem.

### What caught it

The Engineering Lead — noticing that the product/design agents identified the root cause immediately, without the framing the technical panel had brought to the question. The divergence between the two groups' output was the signal: when two panels asked the same question and produced structurally different answer types (tooling vs. decomposition rule), the answer type was as diagnostic as the content.

The retrospective question: "Why did the technical panel not ask 'why does this skip exist?'" The answer is structural, not a failure of any individual agent. Technical agents are calibrated on technical problems. Panel composition — specifically the inclusion of at least one agent from the problem's root cause domain — is as consequential as individual agent expertise.

### Process improvement

**Root cause:** No rule existed requiring the PM Agent to evaluate whether a consultation panel's composition matched the problem's root cause domain, not just its surface presentation. The default was to activate agents whose declared domain matched the problem as stated ("skip governance" → technical agents) without first asking whether the underlying cause might lie elsewhere.

**Standing process change (this session):** A panel composition principle was added to the PM Agent's pre-EL consultation protocol in `docs/process/agents.md §PM Agent — Pre-EL Consultation` between the Activate independently step and the Synthesize step:

> Before finalizing panel composition, ask: does the problem's surface presentation match its likely root cause domain? Technical surface problems can have process root causes; process surface problems can have methodology root causes. A panel composed entirely of agents from the surface domain will produce solutions optimised for the symptom, not the cause. When the root cause domain is uncertain or different from the surface domain, include at least one agent from the suspected root cause domain before activation.

Documented in: `docs/process/agents.md §PM Agent — Pre-EL Consultation`, `docs/process/near-miss-registry.md NM-017` (the related root cause incident)

---

## NM-019 — Named Deliverables Invisible on the Board for an Entire Milestone

**Date:** 2026-05-23 (identified at M9 exit review)
**Milestone:** M9 — Standards Foundation
**Detected by:** PM Agent root cause analysis (triggered by Engineering Lead
asking "how did we find ourselves unclear on M9 scope?")
**Severity:** High — three named M9 deliverables (ADR-007, GovernanceModule
promotion path, STD-REVIEW-005) were listed in CLAUDE.md and/or ADR-005 as
M9 commitments but were never decomposed into GitHub issues. They were
invisible on the board for the entire milestone and only surfaced at exit
review.
**Type:** Reactive — caught at exit review, after the milestone had run its
full course without the deliverables being tracked

### What happened

M9 scope was spread across four documents with no mechanical coupling between
them: CLAUDE.md (constitutional prose), roadmap.md (narrative), the GitHub
milestone board (issues only), and SESSION_STATE.md (current situation
report). None of these has a formal relationship with any other. No diff is
ever run between them.

Three M9 deliverables fell through this gap:

- **ADR-007** (synthetic data framework) — listed in CLAUDE.md as an M9
  deliverable since at least M8 close. CM consultation complete (PR #373).
  Formal ADR draft never written. Never filed as a GitHub issue.
- **GovernanceModule promotion path** (5 criteria) — criteria written in
  ADR-005 with "Valid Until: Milestone 9." 0 of 5 criteria were met at M8
  exit. No M9 work touched any criterion. No issue filed tracking the gate.
- **STD-REVIEW-005** — issue #439 existed but the document it tracks was
  never created, and no process flagged that the issue was open-but-incomplete
  until exit review.

These are not failures of execution. They are failures of decomposition:
named deliverables that lived in prose documents and were never converted into
tracked work items. No agent's mandate included checking for this gap.

### What was at risk

A milestone can close with named commitments undelivered and no record of
why. Downstream milestones build on assumptions about what was completed.
If ADR-007 had not been caught at M9 exit, M10 would have proceeded without
a synthetic data framework ADR, potentially building implementation on an
unreviewed specification. The GovernanceModule promotion path has been
deferred silently across two milestones; without a formal deferral record,
the target date would continue to drift without accountability.

### What caught it

The Engineering Lead asked: "how did we find ourselves unclear on M9 scope?"
The PM Agent ran a root cause analysis against the exit checklist (Issue #213)
and the four scope sources. This is a retrospective catch — the gap had
existed for the entire milestone before it was named.

### Process improvements

**Root cause:** No standing process converts "named in CLAUDE.md or roadmap.md"
into "tracked on the board" at milestone kickoff. The PM Agent HORIZON sweep
audits board state only — it does not compare the board against the
constitution or the roadmap. The gap is structural, not behavioral.

**Three fixes (implemented before M10 kickoff):**

**1. MILESTONE_RUNBOOK.md kickoff gate** (Issue #503):
Before the first implementation issue is filed for a milestone, the PM Agent
must enumerate all deliverables named in CLAUDE.md and roadmap.md for that
milestone and verify each has a corresponding GitHub issue with an owner and
a horizon label. This list is the kickoff baseline. No implementation begins
until verification is complete.

**2. PM Agent HORIZON scope-completeness check** (Issue #503):
The HORIZON sweep gains a sixth step: compare the open-issue list against
CLAUDE.md-stated deliverables for the current milestone; flag any named
deliverable with no corresponding issue as `scope-gap:untracked`. This makes
the gap visible mid-milestone, not just at exit.

**3. roadmap.md as linked diff surface** (Issue #503):
Each milestone entry in roadmap.md must enumerate its blocking deliverables
explicitly (not just narratively) and link to the tracking issue once filed.
A milestone entry with no linked issue is a visible gap — the roadmap becomes
a diff surface, not just a narrative document.

Documented in: `docs/process/near-miss-registry.md NM-019`,
`docs/MILESTONE_RUNBOOK.md §Kickoff Gate` (to be added, Issue #503),
`docs/process/agents.md §PM Agent HORIZON` (to be updated, Issue #503)

---

## NM-020 — Phase 1 Baseline Benchmarks Never Tracked: Backend Compute Latency Gap Before Matrix Engine Retrofit

**Date:** 2026-05-25 (identified at M9 exit, during M10 kickoff preparation)
**Milestone:** M9 → M10 boundary
**Detected by:** Engineering Lead (anticipatory — observed that MV-002 was frontend-scoped while the
original compute baseline intent remained untracked)
**Severity:** High — ADR-009 (the most consequential architectural decision the project will make) has
a hard authoring constraint: "Do not author until Phase 1 baseline benchmarks are complete." No baseline
exists. No issue tracks it. No milestone owns it. M11 would begin without the empirical evidence required
to author ADR-009.
**Type:** Anticipatory — caught at M9 exit before M11 began

### What happened

**Lineage of the compute baseline requirement:**

NM-012 (~2026-05-15, M6-M7 transition) established the Chief Engineer role with an explicit process
improvement: "ADR-009 (engine computation model) cannot be authored until the Chief Engineer completes
Phase 1 baseline benchmarks — a hard constraint preventing speculative architectural commitments."

The benchmarks were defined across four documents:

- `docs/vision/worldsim-technical-concepts.md §The Matrix Engine` (PR #409, 2026-05-22): "Comprehensive
  baseline benchmarks of the current iterative engine on target hardware before any matrix code is
  written. Not on development machines. On the 4-core laptop and the GitHub Actions free-tier runner.
  What does one step computation cost at 1 entity? 10? 100? What does propagation cost as relationship
  edges increase?"
- `docs/roadmap/worldsim-roadmap.md §Milestone 11`: "Phase 1 baseline benchmarks — current engine
  performance on target hardware (4-core laptop / GitHub Actions free-tier runner). Not on development
  machines." Listed as the first M11 deliverable.
- `docs/architecture/backlog.md §ARCH-003`: "Do not author until M11 Phase 1 baseline benchmarks
  complete."
- Issue #217 (ADR-009 requirements, §c): "The target must be measured, not estimated, using the iterative
  model as the baseline."

**How MV-002 was introduced and why it does not cover the compute baseline:**

During the M9 FA brief review (2026-05-22), QA Lead raised QA-F2: "Playwright CPU throttle ≠ hardware;
supplement with MV-002." This was INCORPORATED into the FA brief as MV-002: "Performance ≤ 100ms on
actual target hardware (8GB/4-core laptop)." MV-002 is scoped exclusively to the **frontend**
TrajectoryView ComposedChart render time. Its three measurement targets are:

- Initial render time (ComposedChart SVG)
- Step navigation render time (re-render on step advance)
- Full Mode 3 component set render time (8 Lines + 4 Areas + 3 shock ReferenceLines)

The Phase 1 baseline benchmarks measure the **backend** simulation propagation engine:

- Iterative propagation cost per step at 1, 10, 100 entities
- Propagation cost as relationship edges scale
- Monte Carlo ensemble throughput on the 2-core CI runner and the 4-core laptop
- Measured in seconds/minutes, not milliseconds

These are different systems, different measurement instruments, different target hardware
configurations (4-core for MV-002; both 2-core CI runner AND 4-core laptop for Phase 1),
and different pass criteria (MV-002 has a 100ms threshold; Phase 1 benchmarks establish the
threshold that ADR-009 will commit to). They cannot substitute for each other.

**Why the compute baseline was never tracked:**

Three mechanisms failed in sequence:

1. **"Do not author until X" clauses do not create issues.** The architecture backlog note
   for ARCH-003 says "Do not author until M11 Phase 1 baseline benchmarks complete." This
   is a prose constraint, not a tracked work item. No mechanism converts backlog constraint
   prose into a GitHub issue with an owner, milestone, and acceptance criteria.

2. **The benchmarks are framed as an M11 prerequisite, not an M10 deliverable.** The roadmap
   lists Phase 1 benchmarks under M11. The NM-019 HORIZON scope-completeness check looks at
   "deliverables named in CLAUDE.md and roadmap.md for the current milestone." The benchmarks
   appear under M11 — so the check does not flag them as untracked for M10, even though they
   must be completed during M10 to unblock M11 ADR-009 authoring.

3. **The Chief Engineer is Defined-inactive.** No active agent holds standing responsibility
   for auditing whether the Phase 1 benchmark prerequisite is scheduled. An active agent's
   HORIZON sweep would catch this; a defined-inactive agent has no HORIZON obligation.

**Contributing factor — stale ADR reference in agents.md:**

`docs/process/agents.md §Chief Engineer Agent` (lines 405, 407, 415) still references
"ADR-007 (sparse matrix propagation, M10 Engine Integrity milestone)" in three places. ADR-007
was assigned to the Synthetic Data Framework (ARCH-001, accepted 2026-05-23). The sparse matrix
computation ADR is ADR-009 (ARCH-003, M11). The milestone is M11, not M10. This stale reference
means:
- Any agent reading agents.md to determine when to activate the Chief Engineer would conclude the
  trigger was ADR-007 (now complete) rather than ADR-009 (still pending).
- The Chief Engineer would never self-identify as needed for M10 benchmark preparation
  based on agents.md alone.
- The stale "M10" milestone reference would lead an agent to expect Chief Engineer activation
  during M10 for engine work — but for the wrong ADR.

**Contributing factor — surface naming overlap between MV-002 and Phase 1 benchmarks:**

Both MV-002 and the Phase 1 baseline benchmarks are described as "performance on target hardware."
Both involve 4-core machines. The lexical overlap is significant enough that an agent reviewing the
FA brief's MV-002 definition could conclude the performance baseline intent was satisfied —
particularly without the Chief Engineer present in the panel to distinguish frontend render
performance from backend propagation throughput. The FA brief's review panel (QA Lead, UX
Design Thinking, UX Designer) had no member with computational substrate authority.

### What was at risk

ADR-009 is described in worldsim-technical-concepts.md as "the most consequential architectural
decision the project will make." The ADR commits to one of: (a) parallel run of iterative and
matrix engines before cutover, or (b) hard cutover gated by an equivalence test harness. Either
path requires a concrete, measured performance target — "A Monte Carlo ensemble of 1,000 runs
on the Greece scenario must complete within X minutes on the CI runner" (Issue #217 §c). X must be
measured from the iterative engine baseline, not estimated.

Without Phase 1 baseline benchmarks:

- M11 begins. Chief Engineer is activated. ADR-009 authoring begins. Section (c) requires
  a measured baseline. The baseline does not exist. ADR-009 cannot be completed responsibly —
  the performance commitment would be a guess with a document number, not an empirically-grounded
  target (verbatim from worldsim-technical-concepts.md).
- OR: A hasty baseline is produced at M11 kickoff under time pressure, without the methodological
  rigor defined in worldsim-technical-concepts.md — a single-machine measurement rather than a
  cross-hardware benchmark, taken once rather than across multiple scenario sizes.
- OR: The ADR is authored and accepted without a hardware performance commitment, leaving the
  M11 Phase 2 A/B validation without an equivalence target.

Any of these paths degrades the quality of the most consequential architectural decision in the
project's history. The Equitable Build Process principle — this tool must run on a four-core
laptop — is the specific equity commitment at risk.

### What caught it

The Engineering Lead, observing at M9 exit that MV-002's description ("performance on target
hardware") overlapped with the Phase 1 baseline benchmark intent without satisfying it. The
question "what happened to the backend compute baseline?" surfaced the gap. This is an
anticipatory catch — no M11 decision had been made in error yet, but the preconditions for
a forced choice at M11 kickoff were in place.

### Process improvements

**1. File a GitHub issue for Phase 1 baseline benchmarks as an M10 prerequisite. (Done — Issue #514)**

The issue must:
- Be milestoned to M10 (not M11 — it must complete before M11 ADR-009 authoring begins)
- Have concrete acceptance criteria: measured performance data for the iterative engine on
  both the 4-core laptop and the 2-core CI runner, across scenario sizes of 1, 10, and 100
  entities, with propagation cost as relationship edges scale (per Issue #217 §c)
- Explicitly block ADR-009 authoring (Issue #217 is the blocking relationship to record)
- Be owned by the Chief Engineer when activated; owned by the Engineering Lead as gate-keeper
  until activation

**2. Correct stale ADR reference in agents.md.**

The Chief Engineer section must be updated in the same PR as this near-miss entry:
- Line 405: `ADR-007 (sparse matrix propagation, M10 Engine Integrity milestone)` →
  `ADR-009 (simulation engine computation model, M11 Political Economy and Conditionality milestone)`
- Line 407: same correction to activation trigger
- Line 415: `ADR-007 (sparse matrix propagation) is the first` → `ADR-009 (simulation engine
  computation model) is the first`

**3. Architecture backlog rule: "Do not author until X" must have a corresponding GitHub issue.**

Any ARCH-NNN backlog entry whose notes contain a prerequisite clause ("Do not author until
[condition]") must have a corresponding GitHub issue filed for that prerequisite before the
milestone begins in which the prerequisite must be completed. The issue is the accountability
mechanism; the backlog note is a reminder, not a tracker.

Add to `docs/architecture/backlog.md §Process`: "Any entry with a prerequisite clause in its
Notes field must have a linked GitHub issue for that prerequisite. If no issue exists at the
time the constraint is identified, file one immediately."

**4. Distinguish MV gates from pre-retrofit baseline measurements in the Chief Engineer working
agreement.**

MV gates are pass/fail acceptance criteria for shipped features (frontend render ≤100ms).
Pre-retrofit baseline measurements are empirical surveys of existing code without a pass/fail
threshold — they establish the threshold. A future agent or reviewer should not confuse the
two based on shared "hardware performance" language. The Chief Engineer working agreement
should include: "Phase 1 baseline benchmarks are not MV gates. MV gates are acceptance criteria
for shipped feature components. Phase 1 benchmarks establish the empirical foundation for
ADR-009's hardware performance commitment. They are related in subject matter and unrelated
in purpose."

**5. NM-019 fix extension: HORIZON scope-completeness check must include cross-milestone
prerequisites.**

The NM-019 fix checks "deliverables named in CLAUDE.md and roadmap.md for the current
milestone." The Phase 1 benchmarks appear in the roadmap under M11 but must be completed
in M10. A prerequisite that is listed under a future milestone but must execute in the current
milestone is not caught by the current HORIZON check. Add to the HORIZON step 6 instruction:
"Also flag any item in the next milestone's roadmap entry that is a prerequisite for that
milestone's first ADR, if that prerequisite has no corresponding GitHub issue and no PR in
the current milestone."

Documented in: `docs/process/near-miss-registry.md §NM-020`,
`docs/process/agents.md §Chief Engineer Agent` (stale ADR-007 reference corrected to ADR-009 in this PR),
`docs/architecture/backlog.md §Prerequisite Clause Rule` (added this PR),
Issue #514 — Phase 1 baseline benchmarks (filed as part of this PR; milestone to M10 once M10 is created)

---

## Registry Maintenance

### How to add an entry

When a near-miss is identified — during a session, in a HORIZON sweep, or in post-session
review — the PM Agent files a new entry following the template below:

```markdown
## NM-NNN — [Short descriptive title]

**Date:** YYYY-MM-DD (or approximate milestone era)
**Milestone:** MN — [Milestone name]
**Detected by:** [Who caught it — process or person]
**Severity:** Critical / High / Medium / Low

### What happened
[Factual description — what was done, what was missed]

### What was at risk
[What would have gone wrong if not caught]

### What caught it
[The detection mechanism. If a person: this is evidence the process had a gap]

### Process improvement
[What was changed, where documented, what PR/issue closed the gap]
```

### The key question for every entry

**Was this caught by the process or by a person?**

If a person caught it, the process had a gap. The improvement must be to the process —
not to the instruction to "be more careful." A near-miss that produces only a reminder
to be more careful has not been properly resolved.

### Severity definitions

| Severity | Definition |
|---|---|
| Critical | Would have produced incorrect outputs consumed by downstream users or finance ministry analysts |
| High | Would have produced incorrect artifacts in the repository that would mislead future agents or implementation work |
| Medium | Would have created technical debt or process confusion but not incorrect outputs |
| Low | Inefficiency or mild process gap; no incorrect artifacts produced |

### The pattern across entries

Reading across all entries, a recurring root cause is visible: **an agent acting in a
domain belonging to another agent without the required consultation.** NM-005, NM-006,
and NM-007 are three instances of the same failure mode across three milestones. The
RACI-grounded panel composition rule and the file authority rule are both responses to
this pattern. When a new near-miss appears, check first whether it is another instance
of this pattern before assuming a different root cause.

A second pattern is also visible: six of the fifteen entries are anticipatory —
the Engineering Lead sensing a structural gap before it caused a failure. NM-008,
NM-009, NM-010, NM-011, NM-012, and NM-013 were all caught before any incident
occurred. This is not luck. It is pattern recognition from experience applied
consistently. The near-miss registry documents both kinds of signal: reactive catches
that reveal process gaps, and anticipatory catches that reveal a safety culture
functioning at its best.
