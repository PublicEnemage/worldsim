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
working at its best. Six of the fifteen entries are anticipatory.

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
