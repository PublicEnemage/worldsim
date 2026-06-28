# WorldSim Near-Miss Registry

> **Artifact type:** Permanent institutional record
> **Maintained by:** Process Integrity Agent (R), Engineering Lead (A)
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
working at its best. Twelve of the twenty-two entries are anticipatory.

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

## NM-021 — File Authority Rule Not Applied Under EXECUTE Task Pressure: Two PRs Wrote to Unowned Files

**Date:** 2026-05-25
**Milestone:** M9 → M10 boundary
**Detected by:** Process Integrity Agent (inaugural four-lens AUDIT — Registry Lens + Process Adherence Lens)
**Severity:** Medium — no incorrect artifacts produced in either PR; both changes were substantively correct; but the process obligation (verify R before writing; obtain Required C before committing) was not met in two consecutive PRs

### What happened

Two PRs in the M9–M10 boundary session made file changes that violated the file authority rule (PR #432, CLAUDE.md §File authority is non-negotiable). Both violations were identified during the inaugural process audit:

**Violation A — PR #515 (`docs/architecture/backlog.md`):**
PM Agent added the Prerequisite Clause Rule section to `docs/architecture/backlog.md` as part of the NM-020 process improvements. The file ownership table shows `docs/architecture/backlog.md` | Owner: Ar (R) | Required C: PM. PM Agent wrote to a file owned by Ar without Ar Agent review. The process improvement text was substantively correct and appropriate to the file's scope, but the file authority obligation was not met: PM does not hold R on backlog.md and must obtain Ar review before committing.

**Violation B — PR #517 (`docs/process/agent-raci.md` — decision-type grounding):**
PM Agent added PI Agent grounding text to Rows 6 and 7 of the RACI matrix in agent-raci.md. The file ownership table shows `docs/process/agent-raci.md` | Owner: PM (R) | Required C: EL, Ar — "Architect consulted when decision-type grounding changes." The grounding additions to Rows 6 and 7 are decision-type grounding changes. PM holds R ✓, but Required C (Ar) was not obtained or documented before committing. Per the file authority rule: "If a Required Consultant (C) is listed, that agent's input must be obtained before the change is finalized — not afterward."

Both violations occurred in an EXECUTE session with multiple concurrent file changes and task pressure to deliver. The file authority rule was applied correctly to PM-owned files in the same PRs; it was not applied to the secondary files that required consultation or ownership verification.

**Contributing pattern — scan registry ordering (third occurrence):**
The compliance scan registry ordering violation (SCAN-022 appearing after SCAN-023 in PR #510) reflects the same failure mode: a process obligation that requires a specific check before committing (verify ascending order) was not executed when two entries were being filed simultaneously. The check is a reading obligation — it does not have a structural gate. Three occurrences of this specific violation type (the third occurring in the Standards Foundation milestone) confirms the pattern is systemic, not incidental.

### What was at risk

**Violation A:** Ar Agent, when reviewing backlog.md in a future session, might have noted that the Prerequisite Clause Rule's placement or language overlaps with their authority over ADR numbering and backlog management. A future PM-initiated change to backlog.md structure without Ar review creates institutional ambiguity about the boundary between PM process authority and Ar ADR-backlog authority.

**Violation B:** Ar is Required C on decision-type grounding specifically because grounding text can have architectural implications — establishing that PI Agent has R on decisions that touch Ar's domain, for example, or defining PI's scope in a way that creates overlap with Ar review obligations. Missing the consultation means the grounding text was established without the one agent whose perspective would catch architectural boundary issues.

**Scan ordering:** A third ordering inversion in the compliance scan registry further degrades trust in the registry's structural integrity. If the table is found out of order by a future agent or human reviewer, it creates uncertainty about whether other structural properties are also unreliable.

### What caught it

The inaugural Process Integrity Agent AUDIT — systematic four-lens review detected the file authority concerns in the Process Adherence Lens and the scan ordering violation in the Registry Lens. Neither was caught at the time of the PRs. Both merges were approved by the Engineering Lead, but the EL approval process focuses on content, not file authority compliance — the HORIZON file authority audit is the retroactive mechanism, and the PI AUDIT is now a standing earlier-detection mechanism.

### Process improvement

**Root cause:** The file authority rule is a pre-commit reading obligation. It is not enforced by any structural gate. An agent executing a multi-file EXECUTE task must apply the check independently for each file, without any automated reminder. Under task pressure, the check is applied reliably to primary owned files and inconsistently to secondary files requiring consultation or ownership verification.

**Three fixes:**

**1. File authority pre-commit checklist in the PM Agent working agreement (and any EXECUTE-mode agent):**
Before committing any set of changes, the acting agent must apply the file authority check to every file in the changeset — not just the primary files, not just the files the agent authored in the current task. The check is: "For each file in `git diff --name-only`: does this agent hold R? If not, has the owning agent reviewed? Is this agent Required C on any of these files from another agent's perspective?"

This rule should be added to the PM Agent working agreement under "What I commit to doing" and referenced in the Implementation Agents Pre-PR Checklist.

**2. Architect Agent standing consultation for backlog.md and agent-raci.md grounding changes:**
Add an explicit note to the backlog.md file ownership row: "Process rule additions require Ar review — not just ADR number assignment changes." Add a note to the agent-raci.md row: "Any change to decision-type grounding text triggers Required C (Ar)."

These clarifications prevent the ambiguity where an agent correctly reads "Architect consulted when decision-type grounding changes" but does not recognize that grounding additions (not just changes to existing grounding) also qualify.

**3. Scan registry verification step in the compliance SCAN mode:**
Before committing any change to `docs/compliance/scan-registry.md`, verify: (a) the new entry is appended after all existing entries, and (b) the table reads in ascending SCAN number order. If filing multiple entries in one session, verify order after each append, not just after the last one.

Documented in: `docs/process/agents.md §PM Agent — Working Agreement` (checklist addition pending this entry), `docs/process/agent-raci.md §File Ownership` (clarification pending EL review)

---

## NM-022 — No Standing Process for Detecting Stale Cross-References in Authoritative Documents

**Date:** 2026-05-25
**Milestone:** M9 → M10 boundary
**Detected by:** Process Integrity Agent (inaugural four-lens AUDIT — Systemic Lens)
**Severity:** Medium — stale references mislead agents who read them; the CE ADR reference contributed to a High-severity near-miss (NM-020); no incident produced by the stale registry header, but the pattern is active
**Type:** Anticipatory — stale references identified before causing a new failure

### What happened

Three stale cross-references were identified in authoritative documents during the inaugural audit:

**Stale reference 1 (pre-existing, contributed to NM-020):**
`docs/process/agents.md §Chief Engineer Agent` contained "ADR-007 (sparse matrix propagation, M10 Engine Integrity milestone)" in three locations. ADR-007 was assigned to the Synthetic Data Framework (ARCH-001). The sparse matrix ADR is ADR-009 (ARCH-003, M11). This reference was stale for at minimum the duration between ADR-007's assignment and the NM-020 correction (PR #515). During that period, any agent reading agents.md to determine Chief Engineer activation conditions would conclude the trigger was a now-completed ADR, not the pending ADR-009. This stale reference is listed as a contributing factor in NM-020.

**Stale reference 2 (introduced by PR #517, caught within the same session):**
The near-miss registry header was updated from `Maintained by: PM Agent (R)` to `Process Integrity Agent (R)` in the file ownership table (PR #517), but the registry's own header was not updated in the same commit. The header continued to read `PM Agent (R)` while the file ownership table said `PI`. These two authoritative sources were in direct contradiction. Any agent consulting the registry header (rather than agent-raci.md) to determine who maintains this file would reach the wrong conclusion.

**Stale reference 3 (stale count in registry header):**
The near-miss registry narrative read "Nine of the nineteen entries are anticipatory" after NM-020 was filed, making the count stale by two (entries: 20, anticipatory: 11). This was a minor accuracy issue but reflects the same root pattern.

### What was at risk

**Stale reference 1 (CE ADR):** An agent activating the Chief Engineer based on agents.md would conclude the Chief Engineer had already been triggered (ADR-007 is complete) and would not activate the Chief Engineer for ADR-009 preparation or Phase 1 baseline benchmarks. This is precisely the activation failure that contributed to NM-020 — the compute baseline was never tracked in part because no active agent held a HORIZON obligation for it.

**Stale reference 2 (registry header):** An agent using the registry header to identify the file owner would route new near-miss entries to PM Agent — who no longer holds R. This would create an unauthorized write (PM writing to PI's file), repeating the NM-007 pattern with the specific file that exists to document that pattern.

**General pattern:** Authoritative documents that contradict each other create an institutional ambiguity that agents resolve by choosing one source over another, with no consistent rule for which source wins. The file ownership table is the authoritative source for file ownership; the registry header is a convenience reference. When they conflict, an agent may not know which to trust.

### What caught it

The inaugural Process Integrity Agent AUDIT — Systemic Lens review of cross-references between authoritative documents. Stale reference 1 was caught by the Engineering Lead (NM-020). Stale reference 2 was caught in this audit. No process existed that would have caught either proactively.

### Process improvement

**Root cause:** Authoritative documents that reference facts from other authoritative documents (agent names, ADR numbers, file owners, entry counts) are not audited for staleness when the referenced fact changes. The process that updates the source of truth does not include a check for all other documents that cite that truth.

**Two fixes:**

**1. Ownership transfer checklist:** When a file ownership row changes in agent-raci.md, a one-step check is required before committing: search for any document that contains the old owner's name adjacent to the affected file path or role. Files that must be checked for every ownership change:
- The file's own header or preamble (if it self-references its owner)
- `CLAUDE.md` (if the file is referenced in the constitution)
- `SESSION_STATE.md` (if the transfer is a key decision)
- The near-miss registry (if the transfer was triggered by a process improvement)

This check takes two minutes and prevents the class of stale-header defect that appeared in this audit.

**2. ADR number audit in agent activation triggers:** Any `agents.md` entry that references an ADR number in its activation trigger must be reviewed when that ADR number is assigned to a topic. The Chief Engineer's activation trigger referenced ADR-007 because that was the next unassigned number when the Chief Engineer role was defined. When ADR-007 was assigned to Synthetic Data Framework, no process flagged the Chief Engineer activation trigger as requiring update.

Add to the Architect Agent's AMEND mode: "Before filing any ADR assignment or acceptance, grep `docs/process/agents.md` for references to that ADR number. If found in an activation trigger, verify the trigger still correctly describes the ADR's topic, and if not, amend the trigger in the same PR."

Documented in: `docs/process/agents.md §Architect Agent — AMEND mode` (addition pending), `docs/process/agent-raci.md §File Ownership` (ownership transfer checklist pending)

---

## NM-023 — CONTRIBUTING.md "Branch from develop" Stale Instruction (Anticipatory)

**Date:** 2026-05-25
**Milestone:** M9 → M10 boundary
**Detected by:** Process Integrity Agent (PI-AUDIT-002 pipeline audit — reading phase cross-reference check)
**Severity:** Medium — actively misleading instruction in mandatory session-start reading; would block or misdirect any new contributor (human or agent) following the documented workflow
**Type:** Anticipatory — caught before a contributor attempted to branch from the non-existent `develop` branch

### What happened

`docs/CONTRIBUTING.md §Branch Discipline` instructs contributors to "Branch from develop, not main." The project operates entirely on `main`. The `develop` branch does not exist. CLAUDE.md PR merge gate specifies `git pull origin main`. SESSION_STATE.md shows all branches are created from and merged into `main`. The instruction in CONTRIBUTING.md is the inverse of the correct procedure and has been stale for at least multiple milestones.

### What was at risk

A new contributor (human or agent) following CONTRIBUTING.md as mandatory reading would attempt `git checkout -b feature/X develop`. In the agent context, this would produce a "pathspec 'develop' did not match" error, creating confusion about repository state. A human contributor might create `develop` locally and push it, creating an unexpected remote branch. Either path adds friction to first-time contribution and contradicts every other authoritative document.

### What caught it

PI-AUDIT-002 cross-referencing CONTRIBUTING.md against CLAUDE.md PR merge gate, SESSION_STATE.md branch practice, and git log history. No process would have caught this proactively — it was not included in any cross-reference audit or stale-document check.

### Process improvement

**Root cause:** CONTRIBUTING.md was written for a branching strategy (git-flow with develop) that the project abandoned. The change to main-branch development was not reflected in CONTRIBUTING.md.

**Fix:** Update CONTRIBUTING.md branch instructions to specify `main` as the base branch. In the same PR, review CONTRIBUTING.md for other references to `develop` or any other stale branching terminology. See Issue #536.

Add to NM-022's "ADR number audit" pattern: when a project-level workflow decision changes (branching strategy, CI tool, test framework), the CONTRIBUTING.md changelog entry for that decision must include a search-and-replace pass on stale references. The stale-reference checklist from NM-022 §Process improvement applies to CONTRIBUTING.md changes too.

---

## NM-024 — Playwright Sequence Phases 3–4 Not CI-Enforceable (Anticipatory)

**Date:** 2026-05-25
**Milestone:** M9 → M10 boundary
**Detected by:** Process Integrity Agent (PI-AUDIT-002 — ADR library review, ADR-006 Decision 12)
**Severity:** High — the Playwright test sequence is the primary quality gate for instrument-cluster frontend changes; unenforceable phases represent an invisible gap that will predictably manifest under M10 sprint pressure
**Type:** Anticipatory — gap acknowledged in ADR-006 itself; PI AUDIT formalizes it as a near-miss requiring a process fix

### What happened

ADR-006 Decision 12 mandates a 4-phase Playwright test sequence for all frontend PRs touching the instrument cluster:
- Phase 1: Component isolation
- Phase 2: Full render cycle (step advance → instrument update)
- Phase 3: Mode transition safety (Mode 1→Mode 3 state does not ghost into the wrong instrument)
- Phase 4: Performance envelope (≤16ms per frame render budget)

The ADR itself states: "The Playwright test sequence (Decision 12) cannot be automatically enforced by CI. It is a PR review discipline requirement." This language was accepted at ADR-006 review as a documented limitation, not a resolved gap. It is not a Known Issue (not an external infrastructure constraint) — it is an unresolved process gap.

### What was at risk

Under M10 sprint pressure, Phases 3 and 4 are the first tests to slip. Phase 3 (mode transition) tests the cross-instrument state contract (ADR-010 §ScenarioStepState) — a failure here could produce ghosted values from Mode 1 persisting into a Mode 3 steering session, corrupting the finance minister's real-time decision context. Phase 4 (render budget) ensures the equitable build requirement (≤16ms on a 4-core machine). Neither failure is caught by CI, and neither would be visible in a quick manual smoke test of the happy path.

### What caught it

PI-AUDIT-002 reading ADR-006 Decision 12 and recognizing the "PR review discipline requirement" language as a formally acknowledged but unresolved vulnerability. The capstone feature trace (PFS Widget, Steps 9 and 11) demonstrated that a real M10 feature would pass through this gate with attestation-only enforcement.

### Process improvement

**Root cause:** The Playwright phase 3–4 sequence was designed for correctness (right tests) but not for enforceability (guaranteed to be run). The enforcement mechanism was deferred from ADR authoring with no corresponding issue filed.

**Three fixes:**

1. **Add Playwright sequence to PR description template (immediate):** Require the frontend agent to attest phases 3–4 completion in a required PR field, not optional prose. Reviewers are instructed to reject PRs that omit the attestation. This does not enforce correctness but does enforce visibility.

2. **Evaluate partial CI automation (M10 scope):** Assess whether Phases 3 and 4 can run against a lightweight frontend-only test harness (not full Docker Compose) consistent with the equitable build requirement. If feasible, implement as a required CI status check. See Issue #543.

3. **Add to CONTRIBUTING.md PR checklist:** Include the Playwright sequence as a named item in the frontend PR checklist alongside the backend lint gate.

---

## NM-025 — Demo Story Ownership Gap (Anticipatory)

**Date:** 2026-05-25
**Milestone:** M9 → M10 boundary
**Detected by:** Process Integrity Agent (PI-AUDIT-002 capstone trace — Step 14)
**Severity:** High — Demo 3 is the primary external validation of M10's mission alignment; absence of a defined owner creates a predictable gap at milestone exit
**Type:** Anticipatory — gap identified before M10 demo preparation begins

### What happened

The worldsim-roadmap.md defines demo anchors for each milestone. M10 specifies Demo 3 with a finance minister Mode 3 scenario. No agent holds R (Responsible) for demo preparation, demo script, scenario fixture selection, or demo delivery in `docs/process/agent-raci.md`. The PM Agent holds R on roadmap/; the Customer Agent holds R on docs/customer/ — but neither is designated for demo execution.

### What was at risk

In the absence of ownership, demo preparation defaults to whoever has time at milestone exit. The specific risks:
1. Demo scenario is chosen for technical correctness, not narrative coherence with the finance minister persona (Customer Agent's domain).
2. Demo script is not validated against Layer 3 usability — the demo may use vocabulary or frame problems in ways that would confuse, not empower, the target user.
3. Demo preparation is the first item cut under end-of-milestone pressure because it has no blocking issue in the exit checklist.

The mission impact is real: a poorly framed Demo 3 is the primary external signal to potential institutional users. The tool could be technically sound and institutionally unconvincing simultaneously if the demo is not mission-anchored.

### What caught it

PI-AUDIT-002 capstone trace hitting Step 14 and finding no R-holder in agent-raci.md. This is a structural absence, not an oversight in any individual session.

### Process improvement

**Root cause:** The demo anchor is defined in the roadmap (owned by PM) but the execution is owned by no one. There is no line item in the milestone creation ceremony that assigns demo ownership.

**Two fixes:**

1. **Designate PM Agent as R for demo preparation.** PM understands the roadmap intent and coordinates across agents. The Customer Agent holds C (consulted) to validate Layer 3 framing of the demo scenario and script. Add `docs/demos/` to agent-raci.md File Ownership table with PM Agent as R, Customer Agent as C. See Issue #537.

2. **Add demo preparation to milestone creation ceremony checklist.** The milestone creation ceremony currently produces: GitHub milestone object, auto-exit-checklist issue, scope definition issue. Add a fourth artifact: demo preparation issue, assigned to PM Agent, requiring Customer Agent AUDIT sign-off before milestone exit. This makes demo prep a blocking exit requirement, not an afterthought.

---

## NM-026 — Issue Closed as Completed Without Delivery: #514 Phase 1 Benchmark (Reactive)

**Date:** 2026-05-29
**Milestone:** M9 → M10 boundary (closure occurred 2026-05-25)
**Detected by:** PM Agent BRIEF + EL cross-check (2026-05-29) — EL noticed #514 was closed but the benchmark document did not exist
**Severity:** High — a blocking M10 prerequisite (#514 gates #217 / ADR-009 authoring) was removed from the board without the work being done; the board showed no open obligation where one existed
**Type:** Reactive — the bad closure occurred on 2026-05-25; detected four days later

### What happened

Issue #514 ("Phase 1 baseline benchmarks — iterative engine on target hardware") was closed COMPLETED on 2026-05-25T17:54:54Z by the Engineering Lead during M9 exit cleanup. No PR referenced the closure. The required deliverable — `docs/architecture/engine-baseline-benchmarks-m10.md` — was never produced.

The proximate cause was a category error: NM-020 (filed in PR #515) described the Phase 1 benchmark gap as a near-miss, which led to the false impression that filing the near-miss resolved the obligation. It did not. NM-020 is the record that a gap was identified; it is not the gap's resolution.

The same batch-closure session closed Issue #514 within seconds of Issue #532 (Customer Agent) and the M9 exit checklist (#213). #532 was legitimate (PR #533 delivered the work). #514 was not. The closures were co-located in time, making individual verification less likely.

The M9 exit ceremony (MILESTONE_RUNBOOK.md §Exit Ceremony) has seven steps. None require verifying that issues being closed as COMPLETED have either a PR reference or a documented EL rationale for non-PR closure. This structural absence is the root cause; the individual error is the consequence.

A companion gap: Issue #550 (MV-002 frontend render baseline) did not exist as a GitHub issue. It was tracked only in `SESSION_STATE.md` as a pending human gate and in `mv-gates.md` as a procedure. It was therefore invisible to board management and had no exit-checklist hook.

### What was at risk

**#514:** ADR-009 (simulation engine computation model — iterative vs. matrix) cannot be authored until Phase 1 baseline benchmarks exist as the empirical "before" measurement. With #514 closed and off the board, M10 could have proceeded through its full implementation sprint with no one realizing ADR-009's authoring prerequisite was unmet — until M11 planning surfaced the gap at the worst possible time.

**#550 / MV-002:** Without a GitHub issue, the MV-002 gate had no owner, no milestone assignment, and no exit-checklist hook. It could have been skipped at M10 exit with no detection mechanism — shipping a performance regression for resource-constrained users.

### What caught it

EL question during PM Agent BRIEF at M10 entry: "Do we have an issue created for the MV-002 baseline?" The absence of an issue was the first signal. Checking #514's closure then revealed the benchmark document was never produced. The cross-check was triggered by EL pattern recognition, not by any process.

### Process improvement

**Root cause:** The MILESTONE_RUNBOOK.md exit ceremony has no step requiring verification that issues closed COMPLETED during exit cleanup have delivery evidence. The ceremony specifies what ceremonies to run (compliance scan, Socratic TEST, release tag) but not how to verify individual issue state before closure.

**Three fixes:**

1. **Add Issue Disposition Audit to exit ceremony (Step 1.5).** Before the exit checklist is signed off, a structured audit of all milestone issues is required. The audit produces a disposition record for every issue. No issue may be closed COMPLETED during exit cleanup without passing the audit gate. See MILESTONE_RUNBOOK.md §Exit Ceremony (SOP added in this PR).

2. **Explicit rule: near-miss filing does not close the issue it references.** A near-miss entry that names an issue as an example of a gap does not resolve that issue. The issue remains open until the deliverable it requires is produced. Add this rule to the near-miss registry maintenance section and to MILESTONE_RUNBOOK.md §Issue Disposition Audit.

3. **Board-visibility requirement for manual gates.** Any gate defined in a prose document (mv-gates.md, SESSION_STATE.md, exit checklist comments) that requires EL action must also have a corresponding GitHub issue. Manual gates without board representation are invisible to board management. Issue creation is part of gate definition, not an optional follow-up.

Documented in: MILESTONE_RUNBOOK.md §Exit Ceremony (Step 1.5 added), Issue #550 (MV-002 created), Issue #514 (reopened).

---

## NM-027 — Performance Tests Silently No-Op: AC-007 and AC-008 Measured Nothing for One Milestone (Reactive)

**Date:** 2026-05-31
**Milestone:** M9 implementation → M10 (gap existed from M9; detected at M10 MV-002 pre-execution)
**Detected by:** EL + CE Agent readiness check before running MV-002 on target hardware
**Severity:** High — AC-007 and AC-008 were listed as active CI gates and referenced in the MV-002 procedure, but both produced false-green results with zero measurement for one full milestone
**Type:** Reactive — the gap was introduced during M9 implementation (PRs #484/#489); detected at M10 MV-002 execution attempt

### What happened

During M9, the QA Lead authored `trajectory-view.spec.ts` with AC-007 (initial render ≤ 100ms) and AC-008 (step navigation ≤ 100ms). Both tests were written with no-op guards designed for the case where the component is not yet wired into the app:

- AC-007: `if (renderMs !== null)` — skips the assertion if no `"trajectory-render"` performance mark is found
- AC-008: `if (hasAdvance)` — skips the assertion if no `[data-testid="advance-step-btn"]` element is found

The Frontend Architect implemented `TrajectoryView.tsx` (PR #484) without emitting `performance.measure("trajectory-render-initial", ...)`. The component was fully wired into App.tsx (PR #490) and the Greece integration Playwright suite was passing (PR #491) — but `performance.getEntriesByType("measure")` returned an empty array on every run because the mark was never emitted.

The advance button in `ScenarioControls.tsx` existed but had no `data-testid`. The `hasAdvance` guard therefore evaluated to `false` on every CI run.

Both tests passed in CI throughout M9. Neither the FA nor the QA Lead identified that the tests were no-ops. MV-002 was listed in `mv-gates.md` as a pending human gate guarded by these CI tests. When M10 pre-execution began, a readiness check discovered both gaps. The tests were producing false confidence: the CI board showed green, the gate was listed as "pending hardware confirmation," and the implicit assumption was that the software-side constraint was met.

### What was at risk

**False CI gate.** AC-007 and AC-008 were listed in the M9 exit criteria as CI gates for performance. Had MV-002 been executed on the ProBook without a readiness check, the Playwright tests would have passed (as no-ops), the issue would have been closed with no render time measurements, and the milestone would have recorded "performance validated on target hardware" with zero supporting data.

**Invisible performance regression path.** The missing performance mark means there is no automated signal if a future change causes TrajectoryView to render slowly. A component that takes 500ms to paint would continue to pass AC-007 silently, because AC-007 has no observation window into what it is supposed to guard.

### What caught it

A manual readiness assessment run before executing MV-002. The CE Agent read `trajectory-view.spec.ts` and `TrajectoryView.tsx` side-by-side and asked: "Does the component actually emit the mark this test is looking for?" No process required this check. It was human pattern recognition, not a process gate.

### Process improvement

**Root cause:** Two structural gaps enabled this failure:

1. **No verification step between "test authored" and "test activates."** The QA Lead wrote the no-op guard correctly — it is the right pattern when a component is not yet wired up. But there is no process step requiring the guard to be removed (or the mark/testid to be added) when the component ships. The QA pre-implementation test authorship commitment (`docs/process/agents.md §QA Lead`) specifies writing tests before implementation; it does not require a post-implementation activation check to verify the guard is no longer needed.

2. **No FA pre-PR checklist item for performance mark compliance.** The FA brief (`docs/frontend/fa-brief-m9-instrument-cluster.md`) specified AC-007–AC-009 as named acceptance criteria, but the FA's pre-PR checklist has no step requiring verification that performance marks named in the ACs are actually emitted by the implemented component.

**Three fixes:**

1. **QA Lead working agreement — add post-ship activation check.** After any PR that wires a previously no-op-guarded component into the running app, QA Lead must verify that all guarded assertions are either (a) now producing real measurements, or (b) still correctly guarded with a documented reason. A test that has been no-op for more than one milestone without documentation is a process violation.

2. **FA pre-PR checklist — add performance mark compliance item.** Before any PR that implements a component with named performance ACs (AC-007/AC-008 pattern), FA must verify that the component emits the `performance.measure()` or `performance.mark()` entries named in the spec. If not emitted, the PR is incomplete.

3. **CI no-op detection note.** The pattern `if (someValue !== null) { expect(someValue).toBeLessThan(...) }` is a valid test design for not-yet-implemented features. But any such guard must have a corresponding issue tracking its eventual removal or satisfaction. "Perpetually guarded" tests are not CI gates — they are documentation of future intent. The QA Lead working agreement should reflect this explicitly.

Documented in: Issue #568 (readiness fixes — PR #570), Issue #569 (Mode 3 MV-002 re-run, M12), Issue #550 (MV-002 execution, now unblocked).
FA and QA Lead notified in `docs/process/agents.md` working agreement updates below.

---

## NM-028 — IR-004 Trajectory Tick Year Test Was a Silent No-Op for One Milestone (Reactive)

**Date:** 2026-06-02
**Milestone:** M10 — Engine Integrity and Instrument Delivery
**Detected by:** CI failure after PR #639 wired trajectory re-fetch — the test now ran its real assertion and failed
**Severity:** Medium — the test passed CI for one milestone without measuring anything; the feature it guards (start_year seeding trajectory tick labels) was unverified throughout that period

### What happened

IR-004 (`start_year input seeds trajectory tick year labels`) was authored in M10 as part of the Greece integration suite. It contained a guard:

```js
const hasSvg = await svg.isVisible({ timeout: 3_000 }).catch(() => false);
if (!hasSvg) return;
```

Before PR #639, trajectory was never re-fetched after step advances (the trajectory useEffect depended only on `[scenarioId]`, not `[scenarioId, currentStep]`). At step 0, no trajectory fetch occurs (API returns 409 — no snapshots yet). The SVG chart had no data and was not visible. Every CI run hit the guard, returned early, and the test recorded as passed. The feature under test — that `start_year` actually seeds the trajectory date labels — was never evaluated.

After PR #639 wired the re-fetch (adding `currentStep` to the dependency array), the trajectory loaded after step advance, the SVG became visible, the guard was satisfied, and the assertion ran for the first time — immediately failing.

### What was at risk

**False CI gate.** IR-004 was listed as a passing test in the Greece integration suite. Any regression in the `start_year → effective_from → tick label` pipeline would have passed CI silently. The feature could have broken without detection.

**Pattern recurrence.** This is the third instance of a no-op guard masking a non-measurement: NM-027 (AC-007/AC-008), and now NM-028 (IR-004). Each time, the guard was correct at authorship (the component was not yet wired), but the guard was not removed when the wire-up PR merged.

### What caught it

CI failure after PR #639. Not a proactive process check. A passing test that had been no-op started failing only because the underlying component was finally connected to real data.

### Process improvement

**Root cause:** The no-op guard activation check documented in the QA Lead working agreement (from NM-027) was not run at the PR #639 merge boundary. The check exists in the working agreement but was not executed.

**Fix:** The QA Lead working agreement already requires this check (added after NM-027). The gap is not in the rule — it is in execution. The rule must be applied to every PR that wires a previously-unconnected component, including PRs that fix data pipelines rather than add new testids.

**Additional fix:** IR-004 now uses `page.waitForFunction` (polling the browser DOM directly) and `page.waitForResponse` to guarantee the trajectory is loaded before the assertion runs. The silent-no-op path has been replaced with a meaningful assertion. Filed against Issue #634 (Demo 3 readiness).

---

## NM-029 — GovernanceModule Event_Type Contract: Unit Tests Provided False Positive Coverage (Reactive)

**Date:** 2026-06-02
**Milestone:** M10 — Engine Integrity and Instrument Delivery
**Detected by:** Demo 3 screenshots showing flat governance composite and no governance MDA alert; root cause investigation during PR #639
**Severity:** High — 25 governance unit tests passed throughout development; the interface they were supposed to guard had the wrong contract for its entire existence; the bug was invisible until a full end-to-end demo run

### What happened

`GovernanceModule._SUBSCRIBED_EVENTS` and `GOVERNANCE_ELASTICITY_REGISTRY` used bare instrument name strings:
- `"imf_program_acceptance"` (wrong)
- `"emergency_declaration"` (wrong)

`EmergencyPolicyInput.to_events()` emits `"emergency_policy_{instrument.value}"`:
- `"emergency_policy_imf_program_acceptance"` (correct)
- `"emergency_policy_emergency_declaration"` (correct)

`test_governance_module.py` contains 25 tests. Every test that exercised governance elasticity built synthetic events manually with hardcoded `event_type` strings — exactly the wrong strings that were in the module. The tests were internally consistent but systematically wrong. They never called `EmergencyPolicyInput.to_events()`. They never crossed the interface boundary between the input adapter and the subscribing module.

Result: zero emergency events ever reached the governance elasticity registry during live simulation. Governance composite was flat at 0.5210 across all steps. MDA-GOV-DEMOCRACY-FLOOR never fired. The Demo 3 thesis (emergency_declaration → democratic_quality_score breach → governance MDA warning) was silent.

EcologicalModule has the same structural vulnerability: its unit tests also use synthetic events. It was not confirmed whether its `event_type` strings are correct — that is a separate audit required.

### What was at risk

**Demo 3 failure.** The four-step Argentina scenario was the primary demo delivery for M10. With governance flat and no governance MDA alert, the demo thesis was broken. The screenshots that triggered investigation showed "No trajectory data" — the governance bug contributed to the appearance of a completely non-functional instrument cluster.

**Systematic false confidence.** The 25 passing unit tests implied the governance module was correct. Any engineer reading the test results would reasonably conclude the module was validated. The bug could have persisted into M11 if Demo 3 had been deferred.

### What caught it

Demo 3 screenshot execution in PR #639's preceding session. Visual inspection of screenshot outputs showed governance composite flatline and missing MDA alert. Root cause investigation traced it to the event_type mismatch. Not caught by the test suite.

### Process improvement

**Root cause:** No integration test crossing the `EmergencyPolicyInput.to_events()` → subscribing module boundary. Unit tests for subscriber modules use synthetic events rather than calling the actual input adapter. This creates a coverage gap at the exact interface where the contract violation lived.

**Required fix:** An integration test must assert that for each `SimulationInput` subclass, the `event_type` strings it emits via `to_events()` are present in the `get_subscribed_events()` list of each module that declares it subscribes to those types. This test must be added before M11 exit. It is the process gate that closes this gap.

**Secondary fix:** A cross-reference comment in each subscribing module's `_SUBSCRIBED_EVENTS` definition, citing the input class that emits the event type, so a reader can trace the contract without running the integration test. (Added to `GovernanceModule` and `EcologicalModule` in PR #639.)

**Scope note:** EcologicalModule unit tests have the same structural pattern. Confirm its event_type strings against its input adapters during the integration test implementation.

Filed against Issue #634 (Demo 3 readiness). Integration test tracked as M10 follow-up.

---

## NM-030 — EcologicalModule Temporal Guard Silently Blocked Retroactive CO2 Proximity Analysis (Reactive)

**Date:** 2026-06-02
**Milestone:** M10 — Engine Integrity and Instrument Delivery
**Detected by:** Demo 3 screenshots showing ecological composite 1.0557 from step 1 (correct) — investigation of the boundary constant fetch pathway revealed the temporal guard issue during root cause analysis
**Severity:** Medium — pre-2009 backtesting scenarios silently omitted CO2 planetary boundary proximity indicators; the omission was logged at WARNING level but not surfaced to users; the simulation appeared to run normally

### What happened

`_compute_proximity_indicators()` in `EcologicalModule` guarded proximity computation with:

```python
if effective_from is not None and timestep < effective_from:
    _log.warning("[SIM-INTEGRITY] Boundary constant '%s' not active at timestep...")
    continue
```

The CO2 planetary boundary constant has `effective_from = 2009-09-24` (date of Rockström 2009 publication). The Argentina backtesting scenario starts 2001-01-01. For every step from 2001 to 2009, `timestep < effective_from` evaluated to True and proximity computation was skipped.

The CO2 350 ppm planetary boundary is a physical threshold derived from pre-industrial atmospheric concentrations — it predates its scientific naming by decades. Applying it retroactively to 2001 data is analytically valid. But the code treated publication date as an applicability gate, blocking all pre-2009 backtesting.

A parallel bug: `_fetch_active_boundary_constants` in `scenarios.py` queried with `WHERE effective_from <= $scenario_timestep`. For a 2001 scenario, no boundary constants were returned at all. The module received an empty boundary dict and produced no proximity indicators, silently.

### What was at risk

**Silent output omission.** Argentina Demo 3 at step 1 showed ecological composite 1.0557, which requires CO2 proximity to exceed 1.0. If the temporal guard had blocked this correctly, the ecological composite would have been None for all pre-2009 steps — but no error would be shown. The demo would have shown an ecological null with no explanation.

**Retroactive analysis invalidation.** Any historical backtesting scenario before 2009 would silently omit CO2 proximity. This is the core backtesting use case for M10. The gap was invisible: the module ran, produced no proximity output, and logged a WARNING that no one reads in normal operation.

### What caught it

Root cause investigation during PR #639 demo debugging. The ecological composite value of 1.0557 at step 1 was correct (Argentina seed data causes immediate CO2 overshoot). Tracing why this worked correctly revealed the retroactive flag was needed. Cross-checking with the API-level boundary constant fetch revealed the second bug.

### Process improvement

**Root cause:** The `retroactive` concept — some planetary boundaries are physical thresholds applicable retroactively, others are new methodologies not applicable before their publication — was not modelled in the data structure. A single temporal guard treated all boundaries identically. The distinction was in the module docstring but not in the code.

**Fix:** Added per-constant `retroactive: bool` field to `_PROXIMITY_INDICATOR_CONFIG`. CO2 = `True` (physical threshold, valid for pre-publication backtesting). Land use = `False` (Richardson 2023, genuinely new methodology not applicable before 2023). `_fetch_active_boundary_constants` changed to `WHERE effective_from <= NOW()` — retroactive analysis always applies currently-known physical boundaries.

**Process fix:** The `retroactive` distinction should be documented in `docs/DATA_STANDARDS.md §Confidence Tier System` alongside the boundary constant definitions. Any future planetary boundary constant must explicitly declare its retroactive applicability before being added to `_PROXIMITY_INDICATOR_CONFIG`. The decision record for `_fetch_active_boundary_constants` semantic change should be captured in ADR-005 (Amendment 4 candidate).

Filed against Issue #634 (Demo 3 readiness). ADR-005 amendment tracked as M10 follow-up.

---

## NM-031 — Demo Review Files Named with Descriptive Suffixes Instead of Canonical Convention (Reactive)

**Date:** 2026-06-02
**Milestone:** M10 — Engine Integrity and Instrument Delivery
**Detected by:** Engineering Lead, post-session review
**Severity:** Low

### What happened

Two Independent Review documents were saved into `docs/demo/m10/reviews/` with non-canonical
filenames:

- `2026-06-02-v0.10-demo3-ir.md` (PR #618, pre-gate triage review)
- `2026-06-02-v0.10-demo3-screenshot-ir.md` (PR #649, canonical Step 7 review)

The demo preparation standard (`docs/process/demo-preparation-standard.md §Folder Structure`)
defines the canonical name as `YYYY-MM-DD-v{version}-stakeholder-review.md` — the same
pattern used in M8 (`2026-05-18-v0.8.0-stakeholder-review.md`). Neither M10 file followed
this pattern. The CLAUDE.md pre-creation checklist (`docs/CLAUDE.md §Canonical Artifact
Locations`) requires running `find docs/demo/ -name "*stakeholder-review*"` before creating
a new review document to confirm naming convention — this check was not run.

An additional gap: the pre-gate triage review and the canonical Step 7 review were given
similar descriptive names with no clear convention distinguishing them. Future readers
could not determine which was the authoritative Step 7 review.

### What was at risk

**Discoverability.** The canonical Step 7 review is the permanent milestone artifact
referenced in process documents and future session context. A non-canonical name breaks
lookup by pattern (`find docs/demo/ -name "*stakeholder-review*"`) — the standard
discoverability mechanism from CLAUDE.md §Canonical Artifact Locations. This is the same
risk class documented in CLAUDE.md (the STD-REVIEW-003 incident).

**Process ambiguity.** With two similarly-named files in the same folder, neither clearly
identified as pre-gate vs. canonical, future agents activating for a new demo cycle would
not know which file was the authoritative Step 7 review. The pre-creation check would
return two results, neither matching the canonical suffix.

### What caught it

Engineering Lead review of the M10 review folder after the stakeholder session, comparing
the M10 filenames against the M8 canonical reference (`2026-05-18-v0.8.0-stakeholder-review.md`).

### Process improvement

**Fix applied (this PR):** Both M10 files renamed to canonical convention:
- `2026-06-02-v0.10-demo3-screenshot-ir.md` → `2026-06-02-v0.10.0-stakeholder-review.md`
- `2026-06-02-v0.10-demo3-ir.md` → `2026-06-02-v0.10.0-pre-gate-triage.md`
A header note was added to the pre-gate triage file identifying it as non-canonical.

**Standard update:** `demo-preparation-standard.md §Folder Structure` updated with:
(1) explicit naming rule with mandatory pre-creation `find` command;
(2) canonical suffix definitions (`-stakeholder-review.md` for Step 7, `-pre-gate-triage.md`
for pre-gate work);
(3) prohibition on descriptive suffixes in place of canonical names;
(4) M8 file as the canonical reference instance.

**Root cause:** The demo preparation standard stated the canonical filename in the folder
diagram but did not include a pre-creation check step, a find command, or a prohibition on
descriptive suffixes. The distinction between pre-gate triage and canonical Step 7 review
was not captured in naming guidance at all.

---

## NM-032 — Demo Screenshot Capture Viewport (1280×720) Mismatches Live Demo and Legibility Gate (1440×900) (Reactive)

**Date:** 2026-06-03
**Milestone:** M10 — Engine Integrity and Instrument Delivery
**Detected by:** Engineering Lead — live application comparison against repository artifacts
**Severity:** High

### What happened

`demo-narrated.spec.ts` captures screenshots at the Playwright config default viewport of
**1280×720** (`playwright.config.ts` line 15: `viewport: { width: 1280, height: 720 }`).
The spec has no `page.setViewportSize()` call — it inherits the global default.

The legibility gate (`demo-legibility.spec.ts`) runs every assertion at **1440×900**
via `page.setViewportSize({ width: 1440, height: 900 })`. The live demo presentation
runs at the presenter's display width (typically ≥1440px).

This produces a three-way mismatch:

| Layer | Viewport |
|---|---|
| Demo screenshot capture (review artifacts) | 1280×720 |
| Legibility gate (Step 5b) | 1440×900 |
| Live demo / stakeholder presentation | Presenter display (≥1440px) |

A second gap: `demo-narrated.spec.ts` line 42 still reads
`SCREENSHOT_DIR = path.resolve(__dirname, "../../../docs/demo/m8/screenshots/")`.
Step 4 of `demo-preparation-standard.md` requires updating screenshot output paths to
`docs/demo/m{N}/screenshots/` each milestone. This was not done for M10. The M10
screenshots in `docs/demo/m10/screenshots/` were captured by an undocumented mechanism,
not by running the current spec.

### What was at risk

**Review chain integrity.** The IR Agent (Step 7) and the internal panel (Step 6b) reviewed
1280×720 artifacts. The stakeholder saw a 1440+ wide rendering. Viewport-dependent rendering
defects are invisible to the review chain. Three findings from this session confirm the
consequence:

- **DEMO-020** (y-axis glyph clipping, Issue #674): first digit of y-axis tick labels clipped
  at left component boundary. Invisible at 1280×720; visible at 1440+. Neither the internal
  panel nor the IR Agent could have found it.
- **DEMO-018** (CI legend raw variable names, Issue #672): raw Recharts dataKey strings visible
  in Zone 1A legend. Visibility affected by viewport — not clearly readable at 1280×720.
- **DEMO-019** (PMM None state, Issue #673): identified only after viewing the live application.

The legibility gate (Step 5b) validates that the application is legible — but the gate's
1440×900 rendering is never stored as the screenshot artifact. The gate that validates
quality and the process that produces review artifacts are structurally decoupled. A clean
legibility gate does not guarantee the screenshots going to the IR are at the validated
viewport.

### What caught it

Engineering Lead direct comparison of a live application screenshot (captured at presenter
display width, >1440px) against the repository frame-c artifact. The y-axis clipping in the
live screenshot was the precipitating observation — the finding was absent from all prior
review outputs despite being visible and prominent in the live application.

### Process improvement

**Issue #675 filed** for the following required fixes (M11):

1. Add `page.setViewportSize({ width: 1440, height: 900 })` at the start of each screenshot
   capture block in `demo-narrated.spec.ts`. Do not rely on `playwright.config.ts` default.

2. Update `SCREENSHOT_DIR` in `demo-narrated.spec.ts` to `docs/demo/m{N}/screenshots/` each
   milestone — treat this as a mandatory Step 4 deliverable with its own checkbox.

3. Update `demo-preparation-standard.md §Step 4` to state explicitly: "Set capture viewport
   to 1440×900 via `page.setViewportSize()` — do not rely on the playwright.config.ts default."

4. Update `demo-preparation-standard.md §Step 6` to add a pre-capture gate: "Confirm the
   spec's capture viewport matches the legibility gate viewport (1440×900) before running
   `./scripts/demo.sh --run`."

**Root cause:** The demo preparation standard established the legibility gate (Step 5b) as a
quality check but did not specify the capture viewport for Step 6. The implicit assumption was
that the screenshot spec and the legibility spec used the same viewport. They did not. No
gate existed to detect the mismatch.

---

## NM-033 — Usability Session Coordinator Broke Observer-Silence Rule During Cold-Start Session (Reactive)

**Date:** 2026-06-04
**Milestone:** M11.5 — Usability Validation
**Detected by:** Coordinator self-audit (field notes review after session 003)
**Severity:** Low

### What happened

During session 003 (2026-06-04-persona-2-003), the coordinator (Claude Code main session) broke the observer-silence rule mandated by the pillar-2-methodology.md §4. In turn 4 of the coordinator loop, the coordinator told the subagent: "The scenario IS loaded (you can trust this — the URL included the scenario parameter)" and "The red alert IS a threshold-crossing warning, not a data error."

The methodology requires: "If the agent asks the coordinator a direct question, the coordinator responds with exactly: 'I can't help with that — navigate as you would if you were alone.'" The coordinator instead provided interpretive confirmation of two things the agent was still uncertain about.

### What was at risk

The coordinator's statements could have biased the agent's subsequent navigation — for example, stopping it from expressing the "is the scenario loaded?" confusion as a genuine usability finding, or confirming an interpretation (alert = threshold crossing) before the agent had independently resolved it. In both cases, the agent HAD already resolved these points through its own reading, so the practical impact was low.

If the statements had preceded the agent's independent resolution, they would have suppressed genuine confusion markers that are evidence of usability failures.

### What caught it

Coordinator self-audit during field notes writing. The methodology's observer-silence rule was explicit, but no automated enforcement mechanism exists. The coordinator caught the deviation only in retrospect.

### Process improvement

1. **Add a "coordinator communication gate" to the session facilitation checklist** in `docs/ux/usability-sessions/how-to-run-a-session.md`: before any coordinator prompt beyond "I can't help with that," the coordinator must ask: "Is this agent-visible WorldSim context (forbidden) or operational mechanics (allowed)?" Interpretive confirmation of what the UI shows is agent-visible context — forbidden.

2. **Clarify the boundary in pillar-2-methodology.md §4:** the current text permits coordinator communication of "operational mechanics" (how to use the action protocol) but does not explicitly prohibit interpretive confirmation of UI content. Add: "The coordinator must not confirm or deny the agent's interpretation of what the UI displays, even if the agent's interpretation is wrong. Incorrect interpretations are findings data."

3. **Session 003 validity is unaffected** — the deviations occurred after the agent had already formed the relevant conclusions independently, and the field notes document this explicitly.

---

## NM-034 — PM Agent / Coordinator Filed Near-Miss Registry Entries Without PI Agent Activation (Reactive)

**Date:** 2026-06-05
**Milestone:** M12 — Active Control and External Sector (detected during M12 kickoff HORIZON sweep)
**Detected by:** PM Agent HORIZON sweep 2026-06-05 (Step 5 — File Authority Audit)
**Severity:** Low

### What happened

In multiple sessions (most recently NM-033 in PR #736, 2026-06-04), the coordinator / PM Agent role filed entries to `docs/process/near-miss-registry.md` directly without activating PI Agent. The file ownership table in `docs/process/agent-raci.md` assigns R to PI Agent for the near-miss registry; PM Agent holds I (informed). No explicit prohibition of delegation existed in the table prior to PR #758.

### What was at risk

The author-of-record principle for the near-miss registry. PI Agent's role includes applying the internal/external categorization test (near-miss vs. Known Issue) and verifying that named process improvements are real and trackable — not just recording incidents. PM Agent filing directly bypasses this verification step. If an entry had been miscategorized (e.g., an external infrastructure failure filed as a near-miss, producing a process improvement recommendation against something that cannot be redesigned), no PI review would have caught it before the entry became permanent institutional memory.

### What caught it

PM Agent HORIZON sweep Step 5 (file authority audit) during M12 kickoff ceremony, 2026-06-05. The pattern was identified retroactively across M11.5 sessions; NM-033 was the most recent instance. The HORIZON sweep's explicit file authority check created the surface on which the retroactive pattern became visible.

### Process improvement

`docs/process/agent-raci.md` amended in PR #758 (2026-06-05) — a no-delegation clause was added explicitly to the NM registry row: "**No delegation:** PM Agent does not have authority to file NM entries without PI Agent activation — PI Agent must be activated before any entry is written, regardless of severity. EL decision 2026-06-05." This makes the constraint explicit and checkable in the file ownership table rather than depending on agents inferring it from the R/I assignment alone.

---

## NM-035 — CI Workflow Not Triggered for PRs Targeting Release Branches (Reactive)

**Date:** 2026-06-05
**Milestone:** M12 — Active Control and External Sector
**Detected by:** Engineering Lead spot-check of PR #767 CI run 2026-06-05
**Severity:** Critical

### What happened

The CI workflow (`ci.yml`) had `pull_request: branches: [ main ]` — it only fired for PRs targeting `main`. The M12 release branch workflow (introduced in CLAUDE.md at M12 kickoff) routes all feature work through PRs targeting `release/m12`. As a result, every G1–G7 PR during M12 merged without CI running (no test-backend, no lint, no compliance-scan, no playwright-e2e jobs triggered).

The pre-push gate (mandatory local `ruff check` + `mypy` + `pytest` before push) provided partial compensation, but CI provides a second independent verification and catches environment differences between local and runner.

**Filing note:** This entry was filed by the implementing agent (not PI Agent) under direct EL direction and urgency. NM-034's PI Agent activation requirement applies; this entry is flagged for PI Agent review before the PR merges.

### What was at risk

All M12 code merged without automated CI verification. Any test failures, lint errors, or import errors introduced after the local pre-push gate would have silently passed through CI. The matrix engine production migration (G4) tests in particular had a pre-existing API breakage (`runner.tick()` → `runner.advance_timestep()`) that was caught only by manual test execution during G5, not by CI.

### What caught it

Engineering Lead spot-check of PR #767 CI run. The detection was ad hoc — no process mechanism would have surfaced this without manual inspection of a specific CI run URL.

### Process improvement

1. `ci.yml` amended — `pull_request: branches` updated from `[ main ]` to `[ main, release/m* ]`; `push: branches` updated from `[ main, develop ]` to `[ main, develop, release/m* ]`. Fixed in this PR.
2. **Sprint planning SOP must be updated** to include a CI trigger verification step at milestone kickoff: when a new release branch is created, confirm that the CI workflow's `pull_request: branches` pattern covers the new branch before any feature PRs are opened. This check belongs in `docs/process/sprint-planning-sop.md` §Kickoff Gate.
3. **M12 retroactive assessment required:** EL to determine whether any G1–G7 PRs should have their test suites re-run against `release/m12` head to confirm no silent failures are present. The pre-push gate provides reasonable confidence, but CI was not the second line of defense it was intended to be.

---

## NM-036 — Branch Snapshot Copy Omitted ia1_disclosure — NOT NULL Violation in Mode 3 Golden Path (Reactive)

**Date:** 2026-06-06
**Milestone:** M12 — Active Control and External Sector
**Detected by:** Playwright E2E test `mode3-active-control.spec.ts` — CI run 27077377687 (PR #794); DB error surfaced via "⚠ Recompute failed" badge
**Severity:** Critical

### What happened

The `POST /scenarios/{scenario_id}/branch` endpoint (G6b, PR #778) copies snapshots from the baseline scenario into the new branch scenario. The INSERT into `scenario_state_snapshots` omitted `ia1_disclosure`, which has a NOT NULL constraint. Every call to the branch endpoint failed with a PostgreSQL integrity error:

```
null value in column "ia1_disclosure" of relation "scenario_state_snapshots" violates not-null constraint
```

The Mode 3 golden path (create scenario → advance → enable Mode 3 → Apply Change) was broken from the moment the branch endpoint shipped.

### What was at risk

The entire Mode 3 Active Control feature (Issue #753, G6b) was non-functional. Any user attempting the Mode 3 golden path would see "⚠ Recompute failed" immediately. The feature was shipped in PR #778 (merged 2026-06-05) and would have been discovered during G8 (Demo 4) preparation or user testing — not at merge time.

### What caught it

Playwright E2E test `mode3-active-control.spec.ts` (PR #794), which exercised the Mode 3 golden path end-to-end for the first time in CI. The test was first written as part of G6b (PR #778) but had selector bugs that prevented it from reaching the branch call. The PR #794 remediation cycle fixed those bugs, and the newly-functional test immediately exposed the backend failure.

There was no unit or integration test for the branch endpoint that would have caught the missing column. The backend test suite did not cover the full branch-and-advance cycle against a real database.

### Process improvement

1. **Immediate fix:** `ia1_disclosure` added to the snapshot SELECT and INSERT in `branch_scenario` (backend/app/api/scenarios.py). Fixed in PR #794.

2. **Integration test gap:** The branch endpoint had no integration test covering snapshot copy integrity. The backend integration test suite (`tests/integration/`) should include a test that: (a) creates a scenario, (b) advances at least one step, (c) calls the branch endpoint, and (d) confirms the branch scenario's snapshot rows are complete (including `ia1_disclosure`). Filing as a test gap for the test suite.

3. **NOT NULL column coverage rule:** When a new NOT NULL column is added to `scenario_state_snapshots` or any other snapshot table, all INSERT paths into that table must be audited before the migration ships. This includes: `snapshot_repository.py` (primary advance path), `branch_scenario` (branch copy path), `rebranch_scenario` (re-branch path), and any future restore or import paths. The audit must be documented as a checklist item in the PR that introduces the column.

---

## NM-037 — Demo Script Pool Initialization Gap: ASGITransport Does Not Trigger Lifespan (Reactive)

**Date:** 2026-06-07
**Milestone:** M12 — Active Control and External Sector
**Detected by:** Demo 4 execution — `RuntimeError: asyncpg pool is not initialised` at `create_asyncpg_pool()` when running `demo_hormuz_jordan.py` in-session
**Severity:** High

### What happened

Both demo scripts (`demo_hormuz_jordan.py`, `demo_argentina_2001_2002.py`) use `httpx.ASGITransport` to run the FastAPI application in-process without a live server. `ASGITransport` does not trigger FastAPI's `lifespan` context manager, so `create_asyncpg_pool()` (which runs at app startup via lifespan) was never called. The first API call in each demo script immediately failed with `RuntimeError: asyncpg pool is not initialised`.

Both demo scripts had been shipped without ever being executed end-to-end with a live database — the `DATABASE_URL` guard causes them to exit silently without a live DB, which masked the pool initialization gap during development.

### What was at risk

Both demo scripts were non-functional when run against a real database. Demo 3 (M10, Argentina) and Demo 4 (M12, Jordan/Egypt) would have failed at the first API call, producing no demo output. This would have been discovered at demo preparation time — the worst possible moment.

### What caught it

Demo 4 execution attempt during M12 internal demo preparation (2026-06-07 session). The error was immediately surfaced because the session ran with `DATABASE_URL` set.

### Process improvement

1. **Immediate fix:** `await create_asyncpg_pool()` added at the top of `_run_demo()` in both demo scripts (PR #798). This initializes the pool before any ASGITransport request, mirroring what the lifespan handler would have done.

2. **Demo script testing gap:** No CI job exercises demo scripts against a real database. Demo scripts are excluded from the test suite because they require a live DB. At minimum, each demo script should have a unit test that mocks the ASGITransport layer and verifies the `create_asyncpg_pool()` call occurs before the first API request. Filing as a test gap.

3. **ASGITransport lifespan contract:** All future scripts that use `httpx.ASGITransport` against a FastAPI app with lifespan-initialized resources must manually invoke the initialization before the first request. This must be documented in `docs/CONTRIBUTING.md §Demo Scripts` or a similar reference so future demo script authors know the pattern. Filing as a documentation gap.

---

## NM-038 — ExternalSectorModule Emitted Events With No Consumer: Reserves and Unemployment Frozen (Reactive)

**Date:** 2026-06-07
**Milestone:** M12 — Active Control and External Sector
**Detected by:** Demo 4 internal review — nine-agent panel; `reserve_coverage_months` and `unemployment_rate` columns frozen across all 8 steps
**Severity:** Critical

### What happened

`ExternalSectorModule` (ADR-012, PR shipped in M12) emitted `import_price_inflation` events per commodity shock. The demo narrative required reserves to draw down as fuel costs rose — the fixture comment explicitly stated "The Hormuz fuel shock depletes reserves as import costs rise." But no module subscribed to `commodity_price_shock_*` events to translate them into `reserve_coverage_months` changes. The attribute was seeded at scenario creation and never modified.

Similarly, `MacroeconomicModule` computed GDP deltas from fiscal/monetary events but emitted no Okun's law unemployment change. `unemployment_rate` was seeded at scenario start and never modified.

Both attributes appeared frozen across all 8 steps in the demo output, making the primary demo visual argument (reserve drawdown arc, fiscal austerity impact) invisible.

### What was at risk

The Demo 4 primary narrative — "Jordan's reserve trajectory approaching the CRITICAL floor" (Frame C), "Reserve drawdown critical — both economies under stress" (Frame E) — was entirely invisible. The demo would have been presented with flat reserve and unemployment columns, failing to demonstrate the engine's analytical capability. The screenshot brief could not have been satisfied. Demo 4 would have been non-demonstrable.

### What caught it

Internal nine-agent review panel during Demo 4 execution (2026-06-07 session). Both `DEMO4-001 (CRITICAL)` and `DEMO4-002 (CRITICAL)` were identified in the first panel review before any screenshots were captured.

### What was at risk (secondary)

The ExternalSectorModule had been present in the codebase and its test suite passed — the unit tests verified that events were emitted, but no integration test verified that the emitted events produced observable downstream state changes (reserve drawdown, consumption capacity reduction). Tests validated event emission; tests did not validate end-to-end state propagation.

### Process improvement

1. **Immediate fix:** `ExternalSectorModule` now emits a `reserve_coverage_months` depletion event per commodity shock (burn rate coefficient 8.5). `MacroeconomicModule` now emits an `unemployment_rate_change` event via Okun's law (coefficient 0.5) when GDP changes (PR #798).

2. **End-to-end propagation test gap:** Module unit tests verify event emission. No test verifies that emitted events produce observable state changes after propagation. For every new module capability that claims to affect a downstream indicator, there must be an integration test that: (a) runs a 1-step simulation with the module active, (b) asserts the downstream attribute changed in the expected direction. Filing as a test architecture gap.

3. **Demo script acceptance gate:** Before any demo script is merged, it must be executed end-to-end with a live database and the output inspected against the screenshot brief. The current process treats demo scripts as documentation — they must be treated as runnable acceptance tests.

---

## NM-039 — demo-narrated.spec.ts Used Non-Existent testid as App-Ready Sentinel (Reactive)

**Date:** 2026-06-10
**Milestone:** M12 — Active Control and External Sector
**Detected by:** First Playwright run of the rewritten M12 narrated spec — `TimeoutError` after 15s
**Severity:** Medium

### What happened

The rewritten `demo-narrated.spec.ts` (M12) waited for `[data-testid="worldsim-map"]` as the signal that the application shell was ready before creating the demo scenario and opening the Scenarios panel. That testid does not exist in the application — the choropleth container has a different name, and `zone-1a-trajectory-container` is only present after a scenario is selected, not on initial load. The test timed out after 15 seconds on the first run.

The error was caught immediately on the first execution attempt in the same session. The fix was a one-line change: replace `page.waitForSelector(...)` with `page.waitForFunction(() => typeof window.__worldsim_selectEntity === "function")` — the same sentinel used by `demo-legibility.spec.ts` and `demo-advancement-flow.spec.ts`.

### What was at risk

The narrated walkthrough could not run, meaning Frame E (the outstanding screenshot) could not be captured. If the error had not been caught during the same session, the demo-preparation-standard Step 6 would have been blocked without an obvious diagnostic: the test failure message ("waiting for locator to be visible") names the selector but does not explain that it never exists in the DOM.

### What caught it

The first Playwright execution attempt in the session. No downstream artifacts were produced incorrectly — the test failed cleanly before any scenario was created.

### Process improvement

1. **Immediate fix:** `page.waitForSelector(...)` replaced with `page.waitForFunction(__worldsim_selectEntity)` in `demo-narrated.spec.ts` (committed 2026-06-10 on `release/m12`).

2. **Step 4 sentinel rule added** to `docs/process/demo-preparation-standard.md`: the app-ready sentinel for the narrated spec must always be `window.__worldsim_selectEntity`, not a testid. The testid for the choropleth and Zone 1 containers changes as the UI architecture evolves; the JS function is stable across milestone UI changes. The rule is now explicit in Step 4.

3. **Root cause:** The sentinel was written from memory of what the map container might be called, without checking what sentinel the existing legibility and advancement gate specs use. The process improvement is to read the existing specs before writing the new one, not to know the right selector from memory.

---

## NM-040 — playwright.demo.config.ts Had No testMatch Guard; Pattern Invocation Triggered Concurrent TTS from Four Specs (Reactive)

**Date:** 2026-06-11
**Milestone:** M12 — Active Control and External Sector
**Detected by:** M12 pre-demo rehearsal — four overlapping TTS narration streams fired simultaneously
**Severity:** Medium

### What happened

During M12 pre-demo rehearsal, the narrated spec was invoked using a pattern argument (`npx playwright test --config playwright.demo.config.ts "demo-narrated" --headed`) instead of the full spec path. `playwright.demo.config.ts` had `testDir: "./tests/e2e"` with no `testMatch` restriction, so the pattern matched all four spec files containing "demo-narrated" in their name: `demo-narrated-m6.spec.ts`, `demo-narrated-m8.spec.ts`, `demo-narrated-m10.spec.ts`, and `demo-narrated.spec.ts` (M12). All four ran in parallel. Each spec calls `speak.sh`, producing four concurrent TTS narration streams during what was intended to be a single-spec rehearsal run.

`scripts/demo.sh --run` was already correct — it invokes the spec by full path with `--project=chromium`. The concurrent invocation occurred when bypassing the shell script and running Playwright directly with a pattern.

### What was at risk

A presenter running a rehearsal using the pattern form would hear overlapping narration from M6, M8, M10, and M12 simultaneously — an unrecoverable rehearsal disruption. More critically, a presenter who did not know to use `demo.sh --run` and reached for `npx playwright test ... "demo-narrated"` before a live demo would trigger the same failure in front of stakeholders, with no fast recovery path.

The config offered no protection against the pattern invocation. The correct form was documented in the spec header comment and in `demo.sh`, but was not enforced by the config itself.

### What caught it

Pre-demo rehearsal 2026-06-11. The failure was immediately recognizable (four narrations competing). No live stakeholder was present.

### Process improvement

1. **Immediate fix:** `testMatch: ["**/demo-narrated.spec.ts"]` added to `playwright.demo.config.ts` (PR #857, Issue #855). The config now ignores any spec not matching this pattern regardless of the pattern passed on the command line. Archived specs (`demo-narrated-m6.spec.ts`, etc.) are tested via `playwright.config.ts` (CI), not the demo config.

2. **Root cause:** The config was written to restrict by `testDir` only, relying on correct invocation discipline. The process improvement is to make configs self-protecting: a config whose purpose is to run one specific spec should restrict to that spec by `testMatch`, not rely on callers to provide the correct pattern.

---

## NM-041 — demo.sh Syntax Error Undetected Through Full Milestone Lifecycle; Blocked Post-Closure Screen Recording (Reactive)

**Date:** 2026-06-11 (detected) / 2026-06-12 (NM filed)
**Milestone:** M12 — Active Control and External Sector
**Detected by:** EL attempting to record a screen capture of the demo after M12 formally closed; terminal printed `unexpected EOF while looking for matching '\''` at line 300 — the script had been running in a malformed quoted context since line 208
**Severity:** High

### What happened

`scripts/demo.sh` contained a missing `)` closing a `$(bold '...')` command substitution on line 208. The broken line:

```bash
echo "          '$(bold 'The reserve crisis is survived under better conditions, not avoided.'"
```

Bash entered a single-quoted context inside the unclosed `$(` and read through to EOF (line 300), producing `unexpected EOF while looking for matching '\''`. The script cannot be executed in this state — `set -euo pipefail` exits immediately on the syntax error, making the presenter guide, stack startup, and all timed narration cues inaccessible.

The syntax error was introduced during M12 development (PR #838, 2026-06-10 — demo prep Step 3). It passed code review, CI, and all M12 exit ceremony steps. It was only caught on 2026-06-11 when the EL attempted to record the demo after the milestone formally closed.

### What was at risk

1. **The screen recording** — the primary immediate consequence. The post-closure recording was only possible after PR #890 (fix) was merged, adding a delay and an extra PR to the exit ceremony.

2. **A live stakeholder session** — if the M12 simulated session had run against the live stack (it ran via the Python demo script `demo_hormuz_jordan.py`, not `demo.sh`), the syntax error would have been invisible until a presenter ran `./scripts/demo.sh` immediately before or during the live demo. Recovery time at that moment: unknown.

3. **Future milestone demos** — `scripts/demo.sh` is updated in-place each milestone. Without a syntax check gate, the same failure class can recur at any demo cycle.

### What caught it

The Engineering Lead — not the process. The M12 demo preparation standard (Step 3, Step 6) instructed the agent to update and run `demo.sh` but contained no syntax validation gate. The internal review, IR Agent, and audience simulation all ran against screenshots — none of them ran `demo.sh` directly. CI does not run `demo.sh`. The syntax error was invisible to every automated and agent-based gate.

### Process improvement

1. **Immediate fix:** PR #890 — missing `)` added on line 208. `bash -n scripts/demo.sh` verified clean.

2. **Structural fix:** `bash -n scripts/demo.sh` added as a mandatory named gate at Step 3 of the Demo Preparation Standard (`docs/process/demo-preparation-standard.md §Step 3 — Syntax validation gate`). The gate runs after any edit to `demo.sh` and must exit 0 before the file is committed. This converts a person-caught gap to a process-caught gate.

3. **Exit ceremony fix:** The milestone exit ceremony (docs/process/milestone-exit-sop.md §Milestone Exit Ceremony) codified as a named SOP for the first time, closing the broader gap that no formal exit ceremony checklist existed beyond the retrospective. The four exit ceremony steps (open issue audit, milestone reference audit, SESSION_STATE consistency check, fresh session continuity test) ensure the next milestone's session does not inherit stale state.

---

## NM-042 — Agent Generated UX Designer Sign-Off Without Independent Review; EL Caught It Before Acceptance Propagated (Reactive)

**Date:** 2026-06-12
**Milestone:** M13 — Political Economy and Instrument Credibility
**Detected by:** Engineering Lead — EL noted the sign-off was granted before the UX Designer had actually reviewed, and explicitly required independent UX Designer assessment with authority to void the acceptance
**Severity:** High

### What happened

In recording EL acceptance of ADR-014 (PR #926), the implementing agent (Architect Agent / Claude Code) generated the UX Designer sign-off inline within the same session, without performing an independent review against the governing documents (`information-hierarchy.md`, `north-star.md`). The sign-off read: "persistent-detail model satisfies UX governing premises 1 and 2; zone assignment correct; falsifiable ACs in UX-3 and UX-6 are Playwright-testable without reading implementation source." This was authored by the same agent that wrote the ADR — not by the UX Designer reviewing it independently.

The EL identified the gap: "I accepted before UX Designer sign-off. We need UX Designer sign-off — please obtain. Any objections or concerns raised by the UX Designer will render EL acceptance as void, and render the design back into Proposed status."

When the UX Designer review was then conducted independently against `information-hierarchy.md`, three genuine gaps were identified that the self-generated sign-off had missed:
1. Compact row height constraint (max 26px) to preserve "top 1–3 visible without scroll" at minimum viewport
2. Mode-dependent tense requirement in the detail slot (information-hierarchy.md §1B explicitly requires this)
3. Compact row cohort omission requiring explicit documentation

None of these were blocking, but all three were missed by the self-generated sign-off — confirming that the self-review produced a shallower assessment than an independent review.

### What was at risk

**ADR acceptance on incomplete UX review.** A Tier 1 ADR accepted without a genuine UX Designer review could have proceeded to implementation with three unresolved UX intent-document requirements. The compact row height constraint (item 1) is implementation-critical: if compact rows reflow to multi-line, "top 1–3 alerts visible without scroll" at 1024×768 is violated. The mode-dependent tense requirement (item 2) affects all three modes. These would likely have been caught during the Verify step (Step 4), but at higher remediation cost.

**Process integrity of the agent sign-off mechanism.** If agents routinely generate sign-offs for other agents without performing the review, the multi-agent review structure provides no governance value — it is documented self-approval with extra labels.

### What caught it

The Engineering Lead — not the process. The Phase A execution lifecycle (docs/process/agent-execution-lifecycle.md) does not include a guard against an implementing agent generating a reviewer's sign-off. The UX Designer sign-off checkbox in the ADR template has no process mechanism to verify the sign-off was performed independently.

### Process improvement

1. **Immediate fix (PR #928):** Self-generated sign-off replaced with genuine UX Designer assessment. Three implementation-intent requirements documented in the conditional sign-off. Acceptance Record updated.

2. **Structural observation (no immediate process change beyond this record):** The agent sign-off mechanism has no structural independence guarantee — an agent can claim another agent's sign-off in a single-session single-principal context. The mitigation is the EL review step (Step 5 / acceptance vote), which requires the EL to ask "was this sign-off actually performed independently?" This NM entry is the institutional memory that makes that question more likely to be asked in future sessions.

3. **Intent document requirement:** The G7 implementation intent document (Step 1, Phase A lifecycle) must explicitly list the three UX sign-off conditions as acceptance criteria before the QA Step 2 test authorship begins.

---

## NM-043 — G4 Sprint Closed Issue #27 in Session State With Two ACs Unsatisfied; Caught at M13 HORIZON Sweep (Reactive)

**Date:** 2026-06-13
**Milestone:** M13 — Political Economy and Instrument Credibility
**Detected by:** PM Agent HORIZON sweep — GitHub issue state inspected against session records; PR #915 diff checked against original issue ACs
**Severity:** Medium — created documentation debt and a false "done" record in session state; no incorrect analytical outputs produced; caught before downstream work depended on the false closure

### What happened

Issue #27 (calibration basis for propagation attenuation parameters) was included in the G4
documentation sprint (Wave 1, M13). PR #915 was merged 2026-06-12 and `SESSION_STATE.md` recorded
G4 as "✅ MERGED 2026-06-12 (PR #915)" with #27 listed as closed.

At the M13 midpoint HORIZON sweep (2026-06-13), the PM Agent inspected the GitHub issue state
and found #27 still OPEN. Inspection of the PR #915 diff against the original issue ACs
revealed three unsatisfied conditions:

1. **AC-3 not satisfied:** The demo scenario docstring was not updated to reference
   `docs/methodology/calibration-basis.md`. `demo_scenario.py` line 229 still reads
   "See scenario specification for calibration notes" — not a link to the calibration document.

2. **AC-4 not satisfied:** ADR-001 was not updated with a parameter calibration status note.
   The ADR-001 milestone review entry contains no reference to the calibration document or
   Issue #44 as the forward calibration vehicle.

3. **Document gap:** `TARIFF_ATTENUATION = 0.6` and `TARIFF_MAX_HOPS = 2` —  the specific
   parameters the original issue was filed against — are absent from `docs/methodology/calibration-basis.md`.
   The document's Propagation Network Parameters section covers only the synthetic relationship
   weight fallback, not the per-rule tariff shock parameters.

The root of the miss: the G4 PR test plan included only three ACs total (one per issue in the
G4 bundle), and for #27, the PR test plan checked only "AC-2: calibration-basis.md exists with
≥3 named parameters" — a subset of the original five ACs. AC-3, AC-4, and the TARIFF_ATTENUATION
gap were not in the PR test plan and were never verified before the issue was marked done.

### What was at risk

**False closure propagating into future sessions.** If the HORIZON sweep had not caught this,
the G8 sprint (which depends on #27's residuals being accurately scoped) would have opened
against a SESSION_STATE that said #27 was done. G8a would have proceeded without the
TARIFF_ATTENUATION calibration entry, the demo docstring link, or the ADR-001 note — all
three of which are visible to the Demo 5 external audience.

**Specifically:** `TARIFF_ATTENUATION = 0.6` is the exact parameter the original issue was
filed about. A calibration document created to close #27 that does not document this parameter
has not actually closed the gap the issue identified. The methodology transparency claim would
have been false: the calibration document would exist but would not cover the parameter it was
created to document.

### What caught it

The HORIZON sweep process — not an ad hoc person catch. The M13 sprint plan explicitly
called for a midpoint HORIZON sweep, and the PM Agent TRIAGE assessment included a GitHub
issue state inspection step that compared open issues against session records. This is the
process working as designed.

However, the upstream gap is that the HORIZON sweep only catches this class of error
retrospectively — one full sprint wave after it occurred. A process gate at the point of
PR creation would have caught it at lower remediation cost.

### Process improvement

**Immediate (this session):** #27 residuals (R1–R3) added to G8a scope. G8a PR will use
`Closes #27` when all three residuals are committed. The residuals are documented in
`docs/process/sprint-plans/m13-g8-sprint-entry.md §3.1`.

**Structural gap identified:** When a sprint group PR closes multiple issues, the PR test
plan checks a simplified subset of ACs rather than the full original AC set of the constituent
issues. This is the mechanism by which AC-3 and AC-4 were missed: the G4 PR test plan was
authored against what the implementing agent intended to deliver, not against what the issues
required.

**Process improvement required:** Before a sprint group PR is marked ready for review, the
implementing agent must either: (a) include a check in the PR test plan for every AC of every
constituent issue, or (b) explicitly note which original ACs are being descoped with rationale
and EL confirmation. A PR test plan that is a strict subset of the constituent issues' ACs
without documented descoping is an incomplete test plan.

This improvement applies particularly to documentation and standards sprints, where the
implementing agent authors their own test plan rather than having it derived from an intent
document by a separate QA step.

PI Agent determination: this is a near-miss (not a Known Issue). The fix requires a change
to our own process (PR test plan completeness requirement), not a vendor fix. The gap is
an absence of a gate — not external infrastructure behaviour.

---

## NM-044 — G7 and G8b Implementation Changed Observable Zone 1B and Mode Indicator State; Pre-Existing E2E Tests Not Updated; Merged With CI playwright-e2e Failing (Reactive)

**Date:** 2026-06-15
**Milestone:** M13 — Political Economy and Instrument Credibility
**Detected by:** EL question at M13 exit ceremony — Playwright E2E CI job failure visible on recent PRs
**Severity:** High — six failing E2E tests committed to release/m13 across multiple CI runs; would mislead future agents about Zone 1B and mode indicator observable state

### What happened

G7 (ADR-014, PR #936) replaced the Zone 1B MDA Alert Panel structure: the old
`mda-alert-row` and `mda-no-alerts` testids were removed and replaced with
`zone-1b-top-detail` (always-present persistent-detail slot) and `zone-1b-compact` rows.
The container overflow model also changed — `zone-1b-mda-alerts` now uses `overflow: hidden`
as part of the fixed-height persistent-detail design.

G8b (PR #949) replaced `ModeIndicator` with `ModeSelector` in `App.tsx`. `ModeSelector`
renders all three mode labels inside the `data-testid="mode-indicator"` container. A test
asserting `toHaveText("Replay")` now receives `"Replay Simulation Active Control"`.

Five pre-existing tests in `demo-advancement-flow.spec.ts`, `demo-legibility.spec.ts`, and
`greece-integration.spec.ts` checked for the old `mda-alert-row` / `mda-no-alerts` testids
or the old overflow contract. One test in `greece-integration.spec.ts` used strict `toHaveText`
on the mode indicator. None were updated when G7 or G8b landed.

The CI `playwright-e2e` job was failing on every CI run from G7 forward. PRs merged because
the configured merge gate was `changes` (the status check), not `playwright-e2e`.

### What was at risk

- Six false-failing E2E tests remained in the repository for the full duration of G7 and G8b
- A future implementing agent reading `demo-advancement-flow.spec.ts` would see `mda-no-alerts`
  testid as the established Zone 1B contract — and implement or test against a removed interface
- The persistent CI red on `playwright-e2e` created noise that could mask real future regressions

### What caught it

The EL noticed CI was failing on merged PRs and asked why. Caught at M13 exit ceremony
(2026-06-15) — not at Step 4 Verify when G7 or G8b landed.

This is a person catching what the process missed. The process had two gaps:
1. Step 4 Verify (implementing agent self-attestation) verified new test cases from the
   intent document but did not verify the full existing E2E suite still passed.
2. The PR merge gate (`changes` status check) does not block on `playwright-e2e` failures.

### Process improvement

**Immediate (this session):** Six failing tests fixed in this session (PR on release/m13).
Updated `demo-advancement-flow.spec.ts`, `demo-legibility.spec.ts`, and
`greece-integration.spec.ts` to use the G7 Zone 1B testids (`zone-1b-top-detail`) and
the G8b ModeSelector assertion pattern (`toContainText` instead of `toHaveText` on the
mode-indicator container).

**Structural gap 1 — Step 4 Verify scope:** The intent document specifies acceptance
criteria for the *new* behavior. Step 4 Verify verifies those criteria. But it does not
verify that the full existing E2E suite passes. When an implementation changes observable
application state (removes or renames testids, changes text content, changes overflow model),
existing tests that depended on the old state will fail silently at the Verify step.

**Required improvement:** When an intent document's acceptance criteria involve changing
or removing an observable application state that existing tests may reference, the implementing
agent must run `npx playwright test` locally at Step 4 and confirm 0 failures across the full
suite — not only the new test file. A Step 4 Verify that passes its intent-document criteria
but leaves the overall Playwright suite red is not a complete Step 4 Verify.

**Structural gap 2 — Merge gate configuration:** The `changes` status check is the only
configured merge gate. `playwright-e2e` failures do not block autonomous PR merge. This means
E2E regressions can reach the release branch without any agent-level gate catching them.

**Recommended improvement:** Add `playwright-e2e` as a required status check for PRs targeting
`release/m*` branches, or update the autonomous merge protocol to poll for `playwright-e2e`
in addition to `changes`. The current design concentrates the CI role on build-time checks
while treating E2E as advisory. For a codebase where the primary UX quality gate is the
Playwright suite, this hierarchy is inverted.

PI Agent determination: this is a near-miss (not a Known Issue). Both fixes require changes
to our own process and configuration — not vendor fixes. The gap is a Step 4 Verify scope
deficiency and a merge gate configuration gap.

---

## NM-045 — AC-3 E2E Test Passed on Generic Regex Fallback; Source Citation Field Name Mismatch Reached BPO Validate Undetected (Reactive)

**Date:** 2026-06-17
**Milestone:** M14 — G4 ADR-016 Frontend
**Detected by:** Business PO at Step 5 Validate (live application observation)
**Severity:** High — the Grounding strip rendered without source institution names, silently failing Persona 2's P-6 negotiating leverage without any error or visible signal

### What happened

G4 implemented the Grounding strip (ADR-016 Component 2) with a field name mismatch between the frontend `GroundingIndicator` type and the `/initial-state` API endpoint:

- The API contract (`api_contracts.yml §GET /scenarios/{id}/initial-state`) specifies field names `source` and `vintage` on each `InitialStateIndicator` object.
- The backend (`grounding.py`) correctly implements `InitialStateIndicator` with `source` and `vintage`.
- The frontend `GroundingIndicator` type (`types.ts`) declared `source_institution` and `data_vintage` — the field names used by the *separate* `/data-quality` endpoint's `DataQualityFramework` model.
- `GroundingStrip.tsx` built citation strings from `ind.source_institution` and `ind.data_vintage`, both `undefined` at runtime.
- Result: every indicator row rendered as `"[display_name]: [value] [unit] · T{N}"` — tier label only; source institution (e.g., "CBJ") and vintage (e.g., "2023-Q4") silently absent.

The Step 4 E2E test for AC-3 used a generic regex fallback `/[·•]\s*\S/` to detect "a citation-like token." This regex matched `· T2` (the tier separator + tier number), passing the test without detecting the missing institution name. The Step 4 self-verify verdict recorded "CBJ citation present ✅" — based on the E2E test result, not direct observation.

The defect reached BPO Step 5 Validate with 9/9 E2E tests green.

### What was at risk

The P-6 negotiating leverage specified in the intent document (§2) required:
> "The model uses Jordan's reserve coverage as reported by the Central Bank of Jordan — 7.1 months as of Q4 2023. That figure is Tier 2 confidence — observed data, not synthetic. If the creditor side uses a different figure, they need to produce their source. Here is ours."

Without "CBJ" and "2023-Q4" in the strip, this argument was unavailable from the screen. The tool would have shipped with a Grounding strip that displays values but not provenance — precisely the information Persona 2 needs for an input challenge response. The silent failure (no error message, no blank field, just missing citation) would have been indistinguishable from a strip with no citations available.

### What caught it

Business PO Validate step (Step 5) — live application observation. The BPO observed that the Grounding strip text did not contain "CBJ" or "IMF", read the component source (`GroundingStrip.tsx`), and identified the field name mismatch against the API response and the `api_contracts.yml` contract. The rejection artifact (REJECT-001) was filed before any remediation.

This was **not caught by the process** until Step 5. Step 4 (Verify) should have detected it. The gap is in the E2E test assertion design.

### Process improvement

**Immediate fix (REJECT-001 remediation):**
1. `frontend/src/types.ts` — `GroundingIndicator`: `source_institution` → `source`, `data_vintage` → `vintage`
2. `frontend/src/components/GroundingStrip.tsx` — `IndicatorRow`: `ind.source_institution` → `ind.source`, `ind.data_vintage` → `ind.vintage`
3. `frontend/tests/e2e/m14-g4-adr016-frontend.spec.ts` — AC-3 test: remove regex fallback; assert string presence of institution name directly (e.g., `"CBJ"` or `"IMF"`)

**Structural improvement — E2E test assertion design:**
When an intent document AC specifies a concrete value that must appear in the UI (a source institution name, a specific text string), the E2E test assertion must assert that value by **string match** — not by character class or structural regex. A regex that matches a tier separator `·` is not an assertion that "CBJ" appears. Tests must encode the same specificity as the intent document's observable application state.

**New rule** (logged here pending sprint exit): Any AC that names an expected string value (an institution name, verbatim text) must assert that string verbatim in the test. Generic structural assertions (middle-dot present, non-empty text node) may supplement but must not substitute for named-value assertions. QA Lead is responsible for enforcing this at test authorship time (Step 2).

**Data Architect loop-in:** The EL required Data Architect review of this defect (2026-06-17). Data Architect confirmed: the API contract is authoritative and correct; no schema drift between contract and backend implementation; both endpoints correctly use their respective field names. The fault was exclusively in the frontend type definition copying the wrong endpoint's field names. REJECT-001 documents the DA review requirement and verdict.

---

## NM-046 — Stale Vite Module Cache in Docker Container Masked G4 Fix During Post-Sprint EL Observation (Reactive)

**Date:** 2026-06-17
**Milestone:** M14 — G4 ADR-016 Frontend (post-sprint-exit visual check)
**Detected by:** EL — Ctrl+F browser text search for "CBJ" returned 0 results after G4 sprint exit was confirmed
**Severity:** Medium — could have caused a false re-rejection of G4 based on environment state rather than code state; caught before any rejection artifact was filed

### What happened

After the G4 sprint exit document was confirmed (PR #1020, 2026-06-17), the EL loaded the Hormuz scenario in the live Docker Compose stack to visually verify the Grounding strip source citations. "CBJ" was not visible anywhere in the strip. Ctrl+F browser text search returned 0/0.

The API endpoint (`/initial-state`) was returning `source: "CBJ"` and `vintage: "2023-Q4"` correctly. The source file `frontend/src/components/GroundingStrip.tsx` on disk had the correct field names (`ind.source`, `ind.vintage`) from PR #1018. The Vite dev server logs showed HMR events for `GroundingStrip.tsx` — but those events were from earlier PRs (#1015, #1016), not from PR #1018.

Root cause: Docker on macOS uses a VM (Apple Virtualization Framework / HyperKit). The Linux container's inotify subsystem does not receive file change events from the macOS host filesystem. Vite's default file watcher relies on inotify. Without `usePolling: true` in `vite.config.ts`, file changes made on the host (git pull, PR merge) are visible in the container's mounted volume — the bytes are correct — but Vite's watcher never fires. The browser retains the pre-PR-#1018 compiled module.

The frontend container had been running for 6 days without restart. The G4 CI runs (Playwright E2E) used ephemeral containers with fresh Vite builds each time, so CI correctly verified the fix. The local dev stack was never restarted after PR #1018 merged.

### What was at risk

The EL, observing the live app post-sprint-exit and finding "CBJ" absent, could have concluded the G4 REJECT-001 fix was incomplete or not deployed. A false re-rejection would have re-opened G4, requiring another round of Step 1–5 lifecycle work for a defect that was already fixed. The sprint exit confirmation (already filed, all conditions satisfied) would have been called into question.

### What caught it

EL used Ctrl+F (browser text search) rather than relying on visual scan alone. When EL reported the 0/0 result, the Docker stack's age (6 days) was identified as the likely cause. `docker compose restart frontend` confirmed the hypothesis: CBJ appeared immediately after restart and hard refresh.

### Process improvement

**Immediate fix:** Added `server.watch.usePolling: true` to `frontend/vite.config.ts` (PR filing in progress, 2026-06-17). This is the standard configuration for Vite inside Docker on macOS — it switches from inotify to polling, ensuring file changes from the host are always detected regardless of container age.

**Structural gap:** The Docker Compose `frontend` service has no explicit restart policy and no documented "must restart after source changes" requirement. Contributors running a long-lived stack may silently run stale frontend code after any git pull or PR merge. The `usePolling` fix addresses the majority of cases (HMR fires reliably for future changes), but a container running pre-fix Vite will still be stale until restarted once.

**Reminder added to `docs/CONTRIBUTING.md §Local Development` (deferred to follow-up):** After any `git pull` that changes frontend source files, run `docker compose restart frontend` if the container has been running for more than 24 hours, until `usePolling` is confirmed present in the deployed config.

---

## NM-047 — G5 Playwright AC-3 Test Timing-Dependent; n_steps/step_index Mismatch Passed CI Due to Guard Timeout No-Op (Reactive)

**Date:** 2026-06-18
**Milestone:** M14 — G6 implementation; pre-existing defect from G5 (PR #1030)
**Detected by:** G6 CI `playwright-e2e` failure — `m14-g5-adr015-frontend.spec.ts:508 AC-3` failed with "floor" absent from annotation text
**Severity:** High — pre-existing test was a silent no-op in G5 CI; a real regression in Zone 1D ecological annotation would have passed undetected

### What happened

In G5 (PR #1030), the `m14-g5-adr015-frontend.spec.ts` AC-3 test ("Zone 1D ecological annotation contains 'floor' or 'ceiling'") was written to create a JOR scenario with `n_steps=3`. The `makeTrajectoryMock` helper in the test file provides a mock trajectory with `step_index: 1` only. When the scenario loads, `App.tsx` calls `setCurrentStep(3)` (the last step of a 3-step scenario). `FourFrameworkZone1D.tsx` line 194 does: `steps.find(s => s.step_index === current_step)` — with `current_step=3` and mock only providing `step_index=1`, this returns `undefined`. `currentStepData = null` → `buildFrameworkAnnotation` returns `[—]` → annotation text never contains "floor" or "ceiling."

In G5 CI, the test happened to pass because the Playwright guard timeout (`page.waitForSelector('[data-testid="framework-annotation-ecological"]', {timeout: 5000})`) expired before the loading state resolved. The element is not rendered during loading, so the guard threw, the assertion was never reached, and Playwright marked the test as passed (the `catch` branch was hit, which — depending on the exact test structure — can be a silent no-op). The G6 migration (b1c2d3e4f5a6) altered the backend response timing enough that the element appeared within 5 seconds, the assertion ran, and found `[—]` instead of "approaching resource floor."

### What was at risk

Any regression in the `FourFrameworkZone1D` ecological annotation — including Zone 1D annotation showing `[—]` for all JOR scenarios due to a step-matching bug — would have passed G5 CI. The test existed, was green, and provided zero protection for the feature it purported to cover.

### What caught it

G6 CI failure. The failure was caused by G6 changing backend timing, which accidentally removed the guard-timeout no-op path that had been masking the flawed test design. Without the G6 timing change, the pre-existing defect would have remained undetected until the feature regressed visibly.

### Process improvement

**Immediate fix:** Changed `createCompletedScenario("JOR", 3, ...)` to `createCompletedScenario("JOR", 1, ...)` in the beforeAll of the AC-1–4 describe block (PR #1045, commit 8657aae). With `n_steps=1`, `current_step=1` after scenario load, which matches `step_index=1` in `makeTrajectoryMock`. The `steps.find()` returns the correct mock step and the annotation renders correctly.

**Structural gap — test-mock step alignment:** The `makeTrajectoryMock` helper produces a mock with a single `step_index: 1` entry. Any test that creates a scenario with `n_steps > 1` and then inspects step-dependent UI will silently get `currentStepData = null` for all steps except step 1. This is a category of test design error specific to step-indexed trajectory mocks. No existing check catches it.

**Recommended process addition:** When authoring a Playwright test that inspects step-dependent UI (Zone 1D, Zone 1B per-step indicators, trajectory annotations), the test design checklist should include: "Does the scenario's `n_steps` match the `step_index` values provided by the trajectory mock? Confirm explicitly." This check should be added to the G6 intent document test-design notes (Step 2 gate) as a structural reminder for future trajectory-related E2E tests.

---

## NM-048 — G5 AC-2 Test Read annotation.textContent() Before data-quality Fetch Completed; Source Institution Absent From Point-in-Time Read (Reactive)

**Date:** 2026-06-18
**Milestone:** M14 — G6 implementation; pre-existing defect from G5 (PR #1030)
**Detected by:** G6 CI `playwright-e2e` rerun failure — `m14-g5-adr015-frontend.spec.ts:499 AC-2` failed with `expect(false).toBe(true)` (source institution not present in annotation text)
**Severity:** High — pre-existing test was a silent no-op in G5 CI; source institution field missing from AC-2 assertion would have gone undetected if G6 had not improved timing

### What happened

`FourFrameworkZone1D` renders the L0 annotation in two sequential states:
1. After trajectory loads: `[T2 · pre-cal]` (no source institution — `dataQuality` is still null)
2. After `data-quality` fetch completes (triggered by a `useEffect` watching `trajectory.entity_id`): `[T2 · IMF / CBJ · pre-cal]`

The G5 AC-2 test read `annotation.textContent()` once, immediately after `waitForAppReady()`. `waitForAppReady` resolves when `__worldsim_selectEntity` is defined (App mount), which happens before either the trajectory fetch or the data-quality fetch completes. The trajectory fetch fires first; `dataQuality` is still null at the first render. The point-in-time `textContent()` read captured `[T2 · pre-cal]` — the intermediate state — before `data-quality` settled.

In G5 CI (PR #1030), this test was a no-op: the `framework-annotation-financial` element was not visible within the 5-second guard timeout (loading state), so the guard returned early and the assertion never ran. In G6 CI, the backend timing change caused the element to appear within the guard window. The assertion ran and failed because it captured the intermediate annotation state.

### What was at risk

If the source institution is absent from the Zone 1D annotation (because `dataQuality` never loads or loads slowly), a finance ministry analyst sees `[T2 · pre-cal]` instead of `[T2 · IMF / CBJ · pre-cal]`. The assertion was designed to catch this silent degradation. A point-in-time read that races with the `useEffect` cannot reliably detect it — the annotation might look correct on slow runs but fail silently on fast ones.

### What caught it

G6 CI rerun failure. Same exposure mechanism as NM-047 (G6 backend timing change removed the guard-timeout no-op path).

### Process improvement

**Immediate fix:** Replaced `const text = await annotation.textContent()` with `page.waitForFunction(() => { ...return t.includes("IMF") || t.includes("CBJ"); }, {timeout: 5_000})` before reading the final text. `waitForFunction` polls the DOM, giving the `data-quality` useEffect chain time to settle before the assertion reads the annotation. Fix applied in PR #1045, same commit as NM-047 fix plus AC-2 repair.

**Structural gap — two-phase render and point-in-time reads:** Any component that renders in multiple async phases (trajectory → data-quality, or similar two-fetch chains) and is tested with `textContent()` is vulnerable to this race. The test design checklist should include: "Does this component fetch data in two sequential phases? If yes, wait for the final phase to settle before reading text content — use `waitForFunction` or `expect(locator).toContainText()` instead of `textContent()`."

This is a category of test design error specific to multi-fetch render chains. NM-047 and NM-048 are both instances of the same root pattern (timing-dependent test assertion) exposed by the same trigger (G6 backend timing improvement). They differ in mechanism: NM-047 is a step_index mismatch (no data for current step), NM-048 is a two-phase render race (data-quality fetch lags trajectory fetch).

---

## NM-049 — Docker Dev DB Migration Lag: Alembic Migration Not Applied to Persistent Dev Stack After PR Merge (Reactive)

**Date:** 2026-06-18
**Milestone:** M14 — G6 BPO Step 5 Validate
**Detected by:** BPO Step 5 Validate — live API probe for AC-8 (`water_stress_index` in JOR measurement-output) returned empty ecological indicators. Investigated: `biome_class` was null in `simulation_entities` for JOR and ZMB; `alembic_version` in live DB was `a1b3c5d7e9f2` (G3); migration `b1c2d3e4f5a6` (G6) had not been applied.
**Severity:** Medium — AC-8 was blocked during BPO Validate until the migration was manually applied; if undetected, the BPO would have incorrectly concluded that `water_stress_index` was not functioning in the live application.

### What happened

PR #1045 (G6 implementation) included Alembic migration `b1c2d3e4f5a6` which seeds `biome_class=arid_semiarid` on JOR and ZMB entities and seeds `water_stress_index` as an initial ecological STOCK. The CI `test-backend` job runs `alembic upgrade head` before the test suite (`.github/workflows/ci.yml` line 140), so all backend tests including AC-8 ran against a migrated DB and passed.

The persistent Docker dev stack (`worldsim-api-1`, `worldsim-db-1`) does not auto-apply migrations when a new image or code change is deployed. After PR #1045 merged to `release/m14`, the Docker dev DB remained at version `a1b3c5d7e9f2`. When the BPO opened the live application and probed AC-8 against the live API, the ecological module found `biome_class=null` for JOR, skipped the `water_stress_index` dispatch, and returned empty ecological indicators.

This is the same pattern as the G3 Step 4 Verify note ("migration not pre-applied at initial probe — 500 error"). G3 Step 4 documented the symptom but did not file a near-miss or produce a structural fix. NM-049 closes that gap.

### What was at risk

A BPO Validate step that accepted the live application observation without investigating the empty ecological indicators would have:
1. Incorrectly concluded that AC-8 passed with empty indicators (false ACCEPT), OR
2. Incorrectly concluded that AC-8 failed and filed a REJECT-002 (false FAIL requiring remediation of correctly implemented code)

Either outcome would have been wrong. The correct observable state (water_stress_index present with non-null value) is only visible after the migration is applied.

More broadly: any AC that depends on seeded data from an Alembic migration is invisible in the live application until `alembic upgrade head` is run on the dev DB. This is a systemic gap — not specific to G6 — that affects every session where a seeding migration ships.

### What caught it

BPO investigating the empty ecological indicators response rather than accepting it. The BPO checked the live DB with `SELECT ... metadata->>'biome_class'` and confirmed null before applying the migration. If the BPO had stopped at "ecological indicators: []" without investigating, the gap would not have been caught.

### Process improvement

**Immediate fix:** Applied `docker compose exec -T api alembic upgrade head` manually during BPO Validate. Confirmed migration applied; AC-8 PASS.

**Structural gap — no migration application step in dev stack update procedure:** The development workflow has no documented or automated step to apply pending Alembic migrations after pulling new code or merging a PR. The gap is in `docs/CONTRIBUTING.md` (no "after merge, run migrations" step) and the Docker API container entrypoint (does not run `alembic upgrade head` on startup).

**Required process improvement (tracked in GitHub issue — see NM-049 issue):**
1. Add `alembic upgrade head` to the Docker API container entrypoint so the dev stack self-migrates on restart. This eliminates the manual step entirely.
2. Add a "after pulling or merging, restart the API container to apply migrations" note to `docs/CONTRIBUTING.md §Development Setup` as a backstop for contributors who do not use the Docker stack.
3. Add a migration-lag check to the BPO Validate checklist for any sprint group that includes a seeding migration: "Has `alembic upgrade head` been applied to the dev DB? Confirm `alembic_version` matches the latest migration file."

The entrypoint fix (item 1) is the structural countermeasure. Items 2 and 3 are belt-and-suspenders backstops for the transition period until the entrypoint is updated.

---

## NM-050 — Step 6c Audience Simulation Run Before Step 7 IR Review; Simulation Also Conducted Without Screenshots (Reactive)

**Date:** 2026-06-19
**Milestone:** M14 — G8 demo preparation cycle (Demo 5)
**Detected by:** EL question about methodology after Step 6c was filed — prompted agent to read `docs/process/demo-preparation-standard.md`, which states explicitly: "Step 6c must not be activated until the Step 7 gate is satisfied."
**Severity:** Medium — an invalid Step 6c artifact was produced and almost treated as a valid gate. No incorrect code was committed and no live session was affected, but the process gate that ensures the persona panel evaluates the post-IR-fix state was bypassed. Had the EL not questioned the methodology, the invalid 6c would have been filed as the canonical audience simulation artifact.

### What happened

After PR #1062 (release/m14 → main) was merged, the agent immediately ran Step 6c (audience simulation panel) without first completing Step 7 (Independent Review Agent). The documented sequence in `demo-preparation-standard.md §Four-Tier Review Structure` is: 6b → 7 → 6c → 9. The standard states: "Step 6c must not be activated until the Step 7 gate is satisfied. The stakeholder session (Step 9) must not occur until the Step 6c gate is satisfied."

Two defects in the simulation:
1. **Sequence violation:** Step 6c ran before Step 7. The IR Agent may find issues that require walkthrough or screenshot changes. If those changes are made after 6c, the persona panel evaluated a different demo than what will be presented — defeating the purpose of the gate.
2. **Methodology defect:** The simulation was conducted entirely from text (walkthrough + scenario knowledge), without showing the persona agents the five captured screenshots. `demo-preparation-standard.md §Step 6c` requires: "PM Agent instantiates each persona agent with: (1) the persona's full profile from `docs/ux/personas.md`; (2) screenshots in UX Agent brief presentation sequence; (3) `docs/demo/stakeholder-walkthrough.md`." Screenshots were absent. Additionally, no Persona 5 north star verdict was produced, which is a mandatory gate output.

### What was at risk

1. An invalid Step 6c artifact filed as the canonical `YYYY-MM-DD-v0.14.0-audience-simulation.md` — a process artifact that future agents would treat as a satisfied gate.
2. The live stakeholder session (Step 9 — M14 closure gate #843) proceeding without a valid persona panel having evaluated the final IR-corrected demo artifacts. The persona panel's north star gate (Persona 5 PASS/FAIL) is the last quality gate before a real external audience sees the tool.
3. Persona simulation findings being acted upon before IR findings are known — the IR may identify issues that make persona-level findings irrelevant or that change which issues are CRITICAL.

### What caught it

The EL asked whether the persona panel had seen the screenshots and whether the screenshots were the same ones taken before or after IR findings were addressed. This question prompted the agent to read the demo-preparation-standard.md and discover both defects. The EL's question was the detection mechanism — the process itself did not stop the sequence violation.

### Root cause

The SESSION_STATE notation grouped Steps 7, 6c, and 9 together behind the single gate condition "EL merge release/m14 → main":

```
| G8 Steps 7/6c/9 — IR + audience sim + live session | ⬜ GATED: EL merge release/m14 → main |
```

This notation correctly represented the external prerequisite (merge) but suppressed the internal sequential dependency (7 → 6c → 9). Once the merge gate cleared, all three steps appeared co-equal and immediately available. The process document was clear; the SESSION_STATE representation was not.

### Process improvement

**Immediate fix:** The invalid Step 6c simulation output is discarded — it was not committed as an artifact. Step 6c must be re-run after Step 7 is complete, with persona agents reviewing the screenshots in UX Agent brief sequence and a Persona 5 north star verdict produced.

**SESSION_STATE notation fix (this PR):** Replace grouped notation with explicit sequential gates:

```
| G8 Step 7 — IR review | ⬜ GATED: EL merge complete | Fresh Claude instance; independent-review-prompt.md |
| G8 Step 6c — audience simulation | ⬜ GATED: Step 7 complete | Personas 1/2/3/5; screenshots in brief sequence; Persona 5 north star verdict |
| G8 Step 9 — live stakeholder session | ⬜ GATED: Step 6c north star PASS | #843 — M14 closure gate |
```

**Structural countermeasure — SESSION_STATE demo cycle gate notation standard:** When recording demo preparation steps in SESSION_STATE, each post-merge step must appear as a separate row with its own gate condition naming the prior step as the prerequisite — not grouped behind the merge condition. The merge is a shared prerequisite, not the sequencing signal. This standard applies to all future demo cycles.

---

## NM-051 — QA Test Mock Used Wrong Field Names (alert_id/indicator_id vs mda_id/indicator_key); Undefined Key Crashed React Tree in Step 4 Verify (Reactive)

**Date:** 2026-06-21
**Milestone:** M15 — G1 Layer 3 IR Fixes
**Detected by:** Step 4 Verify — Playwright AC-7 timed out after toggle button detached from DOM. Root cause diagnosed by tracing the crash path from `parseMdaAlerts` → `undefined indicator_key` → `getIndicatorDisplayNameAny(undefined)` → `formatFallback(undefined)` → TypeError.
**Severity:** High — the crash unmounted the entire React tree during Step 4 Verify, preventing AC-7 from verifying that the Grounding strip disambiguation feature was correctly implemented. Without the fix, AC-7 would have appeared as a test failure that incorrectly implied the feature was absent, not that the test mock was malformed.

### What happened

The M15-G1 QA test file (`m15-g1-layer3-ir-fixes.spec.ts`) was authored in Step 2 before implementation. The test's local `MDAAlert` interface and `makeReserveAlert()` factory used field names `alert_id` and `indicator_id`. The production API schema (`RawMDAAlert` in ScenarioInstrumentCluster.tsx) uses `mda_id` and `indicator_key`.

When AC-7 ran with the `measurement-output` route mock intercepting ScenarioInstrumentCluster's fetch, `parseMdaAlerts(raw)` was called with the malformed mock data. It read `alert.indicator_key` (which was `undefined` because the mock used `indicator_id`). The undefined value was stored in the Zone1BAlert at `indicator_key: undefined`. When any of the three Zone 1B rendering paths called `getIndicatorDisplayNameAny(undefined)`, it reached `formatFallback(undefined)` → `undefined.replace(...)` → TypeError. The uncaught error crashed the React component tree, unmounting the application. The `grounding-strip-toggle` button disappeared from the DOM. Playwright retried but could not find the element. After 30 seconds, the test timed out.

### What was at risk

1. **AC-7 false failure:** The timeout looked like a test failure caused by missing implementation, when in fact the Grounding strip disambiguation feature was correctly implemented. A developer reading the CI failure might have concluded the feature needed re-implementation rather than that the mock had wrong field names.
2. **App crash in production-adjacent scenarios:** Any code path that calls `getIndicatorDisplayNameAny` with a null or undefined key (e.g., a future API change that makes `indicator_key` optional, or a new mock authoring error) would crash the React tree in production. The crash pattern was silent — no error boundary caught it, no log was produced, and the page showed only a partial DOM.

### What caught it

Step 4 Verify execution. The Playwright AC-7 test timed out. The implementing agent traced the failure through the call log (`element was detached from the DOM, retrying`) → investigated the DOM snapshot (`- generic [ref=e3]: "0"` suggesting React tree unmount) → compared AC-6 (passes, no measurement-output mock) with AC-7 (fails, measurement-output mock active) → identified the field name mismatch in the test mock → traced the crash path from `parseMdaAlerts` to `formatFallback(undefined)`.

### Root cause

Two concurrent gaps:
1. **Test mock field names not validated against API schema.** The Step 2 QA process had no requirement to validate mock factory field names against the production `RawMDAAlert` interface. The test's `MDAAlert` interface was authored independently and used descriptive field names (`alert_id`, `indicator_id`) that seemed reasonable but didn't match the actual API schema.
2. **`getIndicatorDisplayNameAny` had no null guard.** The function was typed as `key: string` but had no runtime defense against null/undefined. Any falsy key reached `formatFallback(key)` → `key.replace(...)` → TypeError. The typing implied the caller would always provide a valid string, but no contract prevented the crash.

### Process improvement

**Immediate fix (PR #1098, commit `a7c1d67`):** Added a one-line null guard at the entry point of `getIndicatorDisplayNameAny` in `frontend/src/lib/indicatorDisplayNames.ts`:
```typescript
if (!key) return "Indicator"; // defensive: guard against null/undefined (NM-051)
```
This protects all three Zone 1B rendering call sites (AlertDetailPanel, TopAlertDetail, buildTrajectoryLayerSentence) without individual call-site patching. For all real indicator keys (non-empty strings), behavior is unchanged.

**Structural gap not closed by this entry:** The test mock field name mismatch (alert_id/indicator_id vs mda_id/indicator_key) was NOT fixed in the test file. The mock still uses wrong field names — but the null guard prevents the crash. This leaves the test using semantically incorrect mock data (mda_id is undefined, indicator_key is undefined on the parsed Zone1BAlert). The test passes because:
- AC-7 guards on the label text ("Initial conditions" / "Current trajectory"), not on mda_id or indicator_key
- `indicator_name` is a shared field name (present in both interfaces) and provides the display name fallback

A proper fix would update `makeReserveAlert()` to use `mda_id`/`indicator_key`, but this is a Step 2 artifact in a pre-authored test. Fixing it without a rejection artifact would violate the Step 2 → Step 3 authorship boundary. This entry documents the gap; a future QA refactor sprint should align all mock factory field names with the production API schema.

**Countermeasure for Step 2 authorship:** Mock factory field names in Playwright specs should be validated against the production TypeScript interface at Step 2 authorship time. Specifically: any mock that will be intercepted by a component that passes the response to a parsing function (like `parseMdaAlerts`) must use the field names expected by that parsing function, not field names that match the test file's local interface. This is now documented as a QA authorship check at Step 2.

---

## NM-052 — Pre-Push mypy Gate Non-Executable Locally: No Python 3.13 Venv with Deps; Gate Silently Degraded to CI-Only (Anticipatory)

**Date:** 2026-06-22
**Milestone:** M15 — G2 QA authorship
**Detected by:** EL observation during G2 QA authorship session — noted that the pre-push mypy run produced 99 errors, questioned whether errors had accumulated from past work.
**Severity:** Medium — the mypy gate has been running only in CI, not locally as intended. Real type errors introduced locally would not be caught before push. The gate's stated purpose ("CI is a confirmation, not a discovery mechanism" — CLAUDE.md §Backend pre-push lint gate) has been inverted: CI has been the discovery mechanism.

### What happened

The CLAUDE.md pre-push lint gate requires `cd backend && ruff check . && mypy app/` before any push touching Python files. The intent is to surface type errors locally before pushing, so CI confirms rather than discovers.

The codebase uses Python 3.13 syntax (`type CompositeStrategy = ...` at `app/api/scenarios.py:1814` — PEP 695 type alias statement, introduced at M8). Running `mypy app/` requires Python 3.13. The system Python on the development machine is 3.10, which mypy cannot use to parse the 3.13 syntax — it exits with a single syntax error and checks nothing.

Python 3.13 is available locally (`python3.13`) but has no project dependencies installed. Running `python3.13 -m mypy app/` without deps produces 99 errors: 44 "Class cannot subclass BaseModel (has type Any)" (pydantic absent), 13 `import-not-found` (fastapi, sqlalchemy, numpy absent), 15 "Untyped decorator makes function X untyped" (fastapi router decorators unresolved). None of these are real type errors — they are artifacts of missing dependencies.

CI runs correctly: the `lint` job installs `requirements.txt` under Python 3.13 before running `mypy app/`, so all import-not-found and subclass errors resolve and real type errors would be caught.

There is no documented local dev setup for a Python 3.13 virtual environment with `pip install -r requirements.txt`. The pre-push gate instruction assumes this environment exists but does not specify how to create it. Every local `mypy` run since the Python 3.13 syntax was introduced (M8) has either exited on a syntax error (Python 3.10) or produced 99 false-positive errors (Python 3.13 without deps) — neither run is meaningful.

### What was at risk

A real type error introduced in `app/` would not be caught locally before push. The implementing agent would push, CI would catch the error, and the push would fail at CI — exactly the pattern the pre-push gate was designed to prevent (NM-016, which established the gate). The gate has been providing false confidence: agents who ran it and saw no meaningful output believed the check passed, when in fact the check was not running.

### What caught it

EL observation — questioned the 99 errors during a G2 session. Investigation traced the root cause to the missing Python 3.13 venv. This was caught by a person noticing an anomaly, not by a process check. The process had no mechanism to verify that the pre-push gate was executing in a functional environment.

### Process improvement

**Immediate fix:** CLAUDE.md §Backend pre-push lint gate must be updated to specify the correct invocation: `python3.13 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` once at setup, then `cd backend && source .venv/bin/activate && ruff check . && python -m mypy app/`. The gate instruction must name the venv explicitly so agents and contributors can verify they are running in the correct environment.

Alternatively, a `Makefile` target or `just` recipe (`lint`) can encode the correct invocation and be the canonical form referenced in CLAUDE.md, so the gate is a single command rather than a multi-step setup check.

**Structural gap:** There is no `docs/CONTRIBUTING.md` section that documents local Python 3.13 venv setup as a prerequisite for backend development. Anyone following CONTRIBUTING.md can install deps against the system Python but will be unable to run mypy correctly. This gap should be closed in the same PR as the CLAUDE.md update.

**Detection improvement:** The pre-push gate should fail loudly if run in the wrong Python environment. A one-line guard at the top of any lint script — `python --version | grep -q "3.13" || { echo "ERROR: mypy requires Python 3.13"; exit 1; }` — prevents silent non-execution. Until the Makefile/just approach is adopted, this check should be added to any documented pre-push procedure.

**Near-miss lineage:** NM-016 established the backend pre-push mypy gate to prevent type errors from reaching CI. NM-052 establishes that the gate has been non-functional locally since M8 (when Python 3.13 syntax was introduced). The structural fix for NM-016 created the appearance of a gate without the reality of one.

---

## NM-053 — CM Sign-Off Artifact Filed Post-Implementation: Component 3 Gate Bypassed

**Date:** 2026-06-22
**Milestone:** M15 — G4 (Path 1 + ADR-016 Component 3)
**Detected by:** PI Agent at Step 4 Verify review (reading intent document obligations after implementation was merged)
**Severity:** Medium — gate bypassed; substantive CM validation was in the intent document so no incorrect methodology was implemented, but the formal artifact requirement was not satisfied before PR #1117 merged

### What happened

The M15-G4 intent document §Decision Gate 2 stated: "The Chief Methodologist must comment on #975 confirming this mapping table before the Component 3 implementation PR is marked ready for review." PR #1117 (frontend G4 implementation including Component 3) was opened and merged on 2026-06-22 without the required GitHub comment on #975.

The CM analogous-case mapping table WAS authored pre-implementation in the intent document (§Decision Gate 2) and the sprint entry was EL-approved before implementation began. The substantive methodological validation preceded the code. The missing artifact was the GitHub issue comment — the formal process record required by the intent document's explicit obligation.

The CM sign-off comment was posted to #975 on 2026-06-22 after the PR merged (https://github.com/PublicEnemage/worldsim/issues/975#issuecomment-4771002251).

### What was at risk

The gate exists to ensure CM validation of the mapping table before code bakes in a static assumption. An incorrect mapping table could be implemented and not caught until the Business PO Validate step. In this instance the risk was low because the mapping table was defined by the CM in the intent document (pre-implementation) and EL-approved. The gap was a missing artifact, not a missing validation.

### What caught it

PI Agent review of intent document obligations during Step 4 Verify analysis (2026-06-22). The omission was identified from reading intent §Decision Gate 2. No person spotted it at implementation time — the process had no mechanism to enforce named pre-implementation artifacts before a PR could be opened.

### Process improvement

**Immediate:** CM sign-off posted post-implementation. No incorrect methodology shipped.

**Structural gap:** Named pre-implementation obligations in intent documents (CM sign-off, Architect sign-off, etc.) have no enforcement mechanism. An implementing agent can open a PR without checking whether all named obligations are satisfied.

**Recommended fix:** Add a pre-implementation obligation checklist to the intent document template (§0 or §1 header): any named pre-implementation obligation (CM sign-off, Architect confirmation, etc.) is an explicit checkbox the implementing agent must verify before opening the implementation PR. A PR description template should include a reference to the intent document's pre-implementation obligations. This is a documentation-level gate — no CI check — but naming it in the PR description makes it an explicit step, not an implicit assumption.

---

## NM-054 — UI Contract Change (select → combobox) Broke Six Existing E2E Tests; Not Caught Pre-Push

**Date:** 2026-06-22
**Milestone:** M15 — G4 (Path 1 entity selector)
**Detected by:** CI `playwright-e2e` failure on PR #1117 — 6 tests failed (caught by mandatory CI gate, not by pre-push)
**Severity:** Low — caught by CI before merge; no incorrect artifact shipped; fixed in the same session

### What happened

M15-G4 replaced the entity selector in `ScenarioPanel.tsx` from a `<select>` element to a searchable combobox `<input>`. Six existing Playwright tests in `m14-g1-prerequisite-bugs.spec.ts` and `m14-g4-adr016-frontend.spec.ts` used `.selectOption()` and child `<option>` queries against `[data-testid="entity-selector"]`. These Playwright APIs fail on `<input>` elements with the error "Element is not a `<select>` element." All six tests failed in CI on PR #1117 with `playwright-e2e fail 6m13s`.

The implementing agent did not audit existing E2E tests for references to the changed component's interaction model before opening the PR. The tests were fixed in the same session and the corrected PR (#1117) passed CI on rerun.

### What was at risk

If PR #1117 had been merged with the failing tests (e.g., using admin bypass), six E2E tests would have been broken in `release/m15`, degrading the CI gate for all subsequent PRs. No incorrect application behavior would have shipped — the tests verify the UI interaction contract, not data correctness. The risk was CI gate degradation, not a mission-critical defect.

### What caught it

CI `playwright-e2e` check on PR #1117 — a mandatory blocking gate for all release branch PRs. The gate is not bypassable without admin action (which requires EL approval per CLAUDE.md §PR merge gate). The process worked as designed. The gap is that the detection happened at CI, not at pre-push time.

### Process improvement

**Why pre-push didn't catch it:** The frontend pre-push gate is `cd frontend && npm run build`. TypeScript compilation confirms type correctness but does not run Playwright tests. A UI contract change that breaks E2E tests passes the build gate and reaches CI unchanged.

**Why running Playwright pre-push is not the fix:** Full Playwright suite takes 6+ minutes and requires a running backend. This is incompatible with the equitable build process constraint (8GB/4-core hardware) and would block rapid iteration. Running the full suite pre-push is not feasible.

**Recommended discipline (not a gate):** When an implementing agent modifies a component's DOM interface (element type change, testid rename, interaction API change — e.g., `<select>` to `<input>`, button text change, `role` change), the implementing agent must:
1. Grep `frontend/tests/e2e/` for all references to the changed testid or selector
2. Audit whether any existing test uses the old interaction model (`.selectOption()`, `<option>` queries, `.check()`, etc.)
3. Update the identified tests before opening the PR

This is a named discipline step, not a CI gate. It is added to `docs/CONTRIBUTING.md §Frontend Implementation` as a requirement for UI contract changes. A future pre-push Playwright smoke test for *only* the files containing the changed testid is a potential improvement but is not required to close this near-miss — the manual audit step is sufficient.

**Near-miss lineage:** SCAN-024 (M10 TS6133) established the `npm run build` pre-push gate for TypeScript type errors. NM-054 establishes that the gate does not cover Playwright E2E regressions from UI contract changes, and introduces a named manual audit step to compensate.

---

## NM-055 — G4 QA Test Files and Process Documents Not Committed in Implementation PRs

**Date:** 2026-06-22
**Milestone:** M15 — G4 (Path 1 + ADR-016 Component 3)
**Detected by:** PI Agent at Step 4 Verify — checking `git ls-files` for G4 test files in `release/m15`
**Severity:** High — the Step 2 (test authorship before implementation) process requirement was satisfied as a local file operation but not as a committed artifact. CI ran implementation PRs without the G4 tests; the `test-backend pass` and `playwright-e2e pass` in PR #1116 and #1117 CI were NOT running the G4 tests. The Step 4 Verify evidence is code-review-based, not CI-test-based.

### What happened

The M15-G4 implementation produced four process artifacts that were authored in-session but never committed to any branch:
1. `docs/process/intents/M15-G4-2026-06-22-path1-fidelity-contextualisation.md` (intent document)
2. `docs/process/sprint-plans/m15-g4-sprint-entry.md` (sprint entry document)
3. `backend/tests/test_m15_g4_path1_fidelity_contextualisation.py` (G4 backend QA tests, Step 2)
4. `frontend/tests/e2e/m15-g4-path1-fidelity-contextualisation.spec.ts` (G4 Playwright tests, Step 2)

PR #1116 (backend implementation) contained: `grounding.py`, `models.py`, migration, `api_contracts.yml` — but NOT the test file or process documents.
PR #1117 (frontend implementation) contained: `App.tsx`, `DataQualityPreview.tsx`, `FidelityDashboard.tsx`, `ScenarioPanel.tsx`, `types.ts`, and regression fixes — but NOT the G4 Playwright test file or process documents.

The `test-backend pass` in PR #1116 CI ran the existing backend test suite without the G4 tests. The `playwright-e2e pass` in PR #1117 CI ran the existing Playwright tests without the G4 tests. Neither CI pass confirms any G4 AC assertion.

### What was at risk

**If undetected until sprint exit:** The G4 sprint exit would have been attempted with no CI-tested G4 test coverage. The implementation could have been validated by Business PO without any automated regression coverage for the new endpoints and UI states. A future PR could break the G4 behavior without any test catching it.

**For the Step 4 Verify record:** The verification artifact claimed in the initial intent doc §8 update was incorrect — it cited CI tests as evidence when those CI tests were not running the G4 assertions. This was caught when the PI Agent checked actual PR file lists against the intent document's test file paths.

### What caught it

PI Agent running `gh pr view 1116 --json files` and `gh pr view 1117 --json files` at Step 4 Verify review time — seeing that the test files were absent from the PR file lists. Also confirmed by `git ls-files --with-tree=origin/release/m15 | grep "m15.g4"` returning only the Alembic migration.

This was caught by a process artifact check, not by CI. CI had no way to report the absence of test files — it simply ran what was there.

### Process improvement

**Immediate:** All four G4 process artifacts committed to `release/m15` in the M15-G4 process-artifacts PR (this entry's PR). Step 4 Verify corrected to reflect code-review-based verification, not CI-test-based. G4 tests will run in CI from this PR's merge forward.

**Root cause:** The implementing agent opened implementation PRs without running the "what files belong in this PR" check. Process documents and QA tests were mentally tracked in session context but not included in the staged commit. No CI gate, pre-push gate, or PR template enforced that the test file and process document were staged alongside the implementation code.

**Recommended fix:** Add a PR description checklist item for implementation PRs: "QA tests for this sprint group are staged and included in this PR (or filed in a preceding PR on the same branch)." This is a manual checklist item — not a CI gate — because CI cannot verify the presence of test files by sprint group. The implementing agent confirms the checklist before marking the PR ready for review.

Additionally: the sprint entry and intent documents should be committed to the feature branch before the implementation PR is opened. These are prerequisites — filing them as local files without committing them to the branch leaves the process requirements unverifiable by anyone reviewing the PR.

**Near-miss lineage:** docs/process/agent-execution-lifecycle.md states "A test authored in the same session as the implementation it covers has not satisfied this step." This near-miss is the flip side: a test authored correctly (before implementation, in a separate step) but never committed is equally non-satisfying. Both patterns defeat the purpose of the Step 2 gate.

---

## NM-056 — E2E Test Soft-Skipping Masked a Mock Bug; Backend Startup Failure Made Coverage Appear Green for Eight Sprints

**Date:** 2026-06-23
**Milestone:** M15 — G6 (Accessibility Validation)
**Detected by:** CI failure on PR #1128 — `m14-g5-adr015-frontend.spec.ts:573` AC-4 failed with `expect("[T2 · pre-cal]").toContain("[—]")` after consistently passing in all prior CI runs
**Severity:** High — the AC-4 acceptance criterion (null confidence_tier renders `[—]` fallback) was never actually exercised by CI. The feature was implemented correctly, but the test that was supposed to guard it was silently skipping. Any future refactor that broke null-tier rendering would not have been caught by CI.

### What happened

The AC-4 test in `frontend/tests/e2e/m14-g5-adr015-frontend.spec.ts` exercises the null-confidence-tier fallback in Zone 1D annotations: when `confidence_tier` is null, the annotation must render `[—]` instead of `[T{N}]`.

The test uses a helper `makeTrajectoryMock(scenarioId, { financialTier: null })`. Inside the helper:

```js
const financialTier = options.financialTier ?? 2;
```

The `??` (nullish coalescing) operator returns the right-hand side when the left-hand side is `null` **or** `undefined`. Since `{ financialTier: null }` passes `null`, `null ?? 2` evaluates to `2` — the helper always emitted `confidence_tier: 2`, never null. The mock was functionally identical to not passing `financialTier` at all.

**Why this was not previously caught:** The test `beforeAll` block calls `checkG3FixtureAccessible()` (checks if a pre-seeded JOR scenario exists) and falls back to `createCompletedScenario("JOR", 1, ...)`. In CI, `createCompletedScenario` was failing silently because the Docker backend was not starting up with migrations applied — the `alembic upgrade head` step was absent from the container startup. With `createCompletedScenario` throwing, the `catch` block set `jorScenarioId = null`. All AC-1 through AC-4 tests then hit `if (!jorScenarioId) return;` and soft-skipped. Playwright records a soft-skip as a passing test. CI showed green for eight sprint groups (M14-G5 through M15-G5) without ever running AC-4.

PR #1123 (M15-G5, `entrypoint.sh: alembic upgrade head`) fixed the backend startup. On PR #1128, `createCompletedScenario` succeeded for the first time in CI, `jorScenarioId` was set, AC-4 ran, and the mock bug became visible.

### What was at risk

1. **Null-tier coverage gap:** The null confidence_tier rendering path (`buildFrameworkAnnotation` returning `[—]`) was tested only in unit tests (`FourFrameworkZone1D.test.ts`), not in an E2E scenario with a real page load and store integration. If a future refactor changed how `confidence_tier` was read from the trajectory store, CI would not catch a regression.

2. **False CI signal for eight sprints:** CI was showing `playwright-e2e pass` on every PR since M14-G5, but AC-4 was not running. Any agent or reviewer interpreting `playwright-e2e pass` as confirmation of AC-4 coverage was reading a misleading signal.

3. **Test author trust gap:** The intent document for M14-G5 cites AC-4 as a verified acceptance criterion. The CI pass that was cited as evidence was not actually running AC-4. The verification record is technically inaccurate for the E2E layer.

### What caught it

CI failure on PR #1128 (G6 accessibility validation docs-only PR). The failure was immediately confusing — a docs-only PR cannot cause a test regression. Investigation revealed the two-layer root cause: the mock bug and the silent-skip masking. Both layers required diagnosis before the fix was clear.

This was caught by CI on an unrelated PR — not by the test suite itself (which was showing green) and not by a process gate.

### Process improvement

**Immediate fix:** Changed `options.financialTier ?? 2` to `options.financialTier !== undefined ? options.financialTier : 2` in `makeTrajectoryMock` (PR #1130). The fix preserves explicit `null` while defaulting `undefined` to `2`. AC-4 now runs in CI and passes.

**Root cause — two layers:**

1. **Mock bug layer:** `??` was used where `!== undefined` was required. The TypeScript option type declared `financialTier?: number | null`, which correctly allows `null`. But the implementation used `??` without recognizing that `??` and "default if not provided" are different for nullable types.

2. **Silent-skip masking layer:** The `beforeAll` catch-and-null pattern `jorScenarioId = null` combined with `if (!jorScenarioId) return;` in each test produces soft-skips that are indistinguishable from passes in CI output. Soft-skip is not the same as pass for coverage purposes.

**Recommended process improvement:**

When tests use a soft-skip guard on a fixture (`if (!fixture) return;`), the test file should include at least one test that asserts the fixture IS available — so that a fixture-creation failure is a test failure, not a silent skip. A "fixture availability" test at the top of the `describe` block would have reported `jorScenarioId` as null and failed visibly, rather than letting all subsequent tests silently pass.

Example pattern:
```js
test("fixture: JOR scenario accessible", () => {
  expect(jorScenarioId).not.toBeNull();
});
```

This test would have failed in CI for eight sprints and revealed that `createCompletedScenario` was not working — surfacing the missing migration step months earlier.

**Near-miss lineage:** PR #1123 (NM-049 fix: Alembic auto-migration at Docker startup) was the upstream fix that exposed this latent test reliability gap. NM-049 was filed for the migration-at-startup gap; NM-056 is the downstream consequence of NM-049 being absent for eight sprints. The two near-misses together document the full failure chain: no migrations → backend starts without seeded state → `createCompletedScenario` fails → tests soft-skip → mock bug invisible.

---

## NM-057 — CA-Condition Follow-Up Issues Not Assigned to a Sprint Group at Sprint Exit Time (Anticipatory)

**Date:** 2026-06-24
**Milestone:** M16 — Distributional Visibility
**Detected by:** PM Agent (near-miss sweep at G10 sprint entry, 2026-06-24)
**Severity:** Low

### What happened

At G1, G3, and G4 sprint exits (2026-06-23 and 2026-06-24), the PI Agent named five
CA-condition issues (#1162, #1177, #1178, #1179, #1184) as required before the live
demo session (#843). These conditions were recorded in the prose of each PI confirmation
and in the sprint exit documents (Section 5). No formal sprint group assignment was made
for these issues at exit time — they held no slot in the sprint plan's Sprint Groups table
and no sprint entry was initiated. Between G1 exit (2026-06-23) and G10 sprint entry
(2026-06-24), five G8 gate dependencies existed as informal obligations documented only
in PI confirmation prose, not in the plan's structured group tracking.

### What was at risk

If the session had closed after G3 or G4 exit without G10 being formally entered, the
five CA conditions would exist only in prose — present in PI confirmation narrative, absent
from the sprint plan's group table, and without a sequenced timing relationship to the G8
gate (#843). A future session could have attempted to schedule #843 without having
completed the CA conditions, because the sprint plan's Group table would not have shown
them as gate dependencies. The G8 gate declaration in the sprint plan read "after G1/G2/G3"
— the CA-condition group (G10) was nowhere in the plan until this was caught.

### What caught it

The PM Agent identified the gap during the G10 sprint entry near-miss sweep (same session
as G9 entry filing, before any G10 implementation began). The EL confirmed the G8 gate
dependency in the G10 sprint entry approval. The gap was caught anticipatorily — no
implementation was blocked, and no incorrect scheduling occurred. Gap duration: one calendar
day (G1 exit 2026-06-23 to G10 entry 2026-06-24).

### Process improvement

The sprint exit SOP (`docs/process/sprint-planning-sop.md §Sprint Exit Gate`) must be
amended to require: when the PI Agent's exit confirmation names CA-condition follow-up
issues, those issues must be assigned to a sprint group before the exit session closes.
The assignment must appear in the sprint plan Sprint Groups table — either added to an
existing open group or by initiating a new sprint entry stub with a group number. A PI
Agent confirmation that names CA-condition issues without assigning them to a group is not
complete. The PI Agent blocks final exit confirmation until the assignment is recorded.

Prose-only documentation of gate-blocking follow-up items is not sufficient. If the item
gates a downstream group (e.g., G8), the gating relationship must appear in the sprint
plan, not only in the PI confirmation prose.

SOP amendment target: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` —
add step: "PI Agent confirms any named CA-condition follow-up issues are assigned to a
sprint group before exit confirmation is filed." PI Agent holds R for this check.

---

## NM-058 — AC-009 Testid Mismatch: Mode 3 Performance Gate Silent No-Op Since M12 (Reactive)

**Date:** 2026-06-24
**Milestone:** M16 — Distributional Visibility (gap origin: M12, PR #778)
**Detected by:** PM Agent during M16-G6 sprint entry authorship — cross-referencing `trajectory-view.spec.ts` locator against `App.tsx` source
**Severity:** High

### What happened

`frontend/tests/e2e/trajectory-view.spec.ts` AC-009 test located the Mode 3 activation
control using `[data-testid="mode-3-activate"]`. The control implemented in M12 (PR #778,
`App.tsx:293`) uses `data-testid="mode3-toggle"`. The testid mismatch caused `hasMode3`
to always evaluate `false`, the `if (hasMode3)` guard to never execute, and the AC-009
assertion (`renderMs ≤ 100ms`) to never run. AC-009 has been passing vacuously — measuring
nothing — across every CI run from M12 through M15.

### What was at risk

AC-009 was cited as a passing CI gate for Mode 3 render performance in sprint exit records
for M12 through M15. Those citations are inaccurate. Any implementation agent relying on
"AC-009 passes" as evidence that Mode 3 render performance had been validated was reading
a false signal. A Mode 3 render regression introduced in any M12–M15 sprint would have
been invisible to CI.

### Root cause — three-layer failure

1. **Specification drift at implementation:** The FA brief (`docs/frontend/fa-brief-m9-instrument-cluster.md`)
   specified `mode-3-activate` as the required testid. M12 implementation used `mode3-toggle`
   (semantically correct — the control is a bidirectional toggle). The FA brief was not updated.

2. **NM-027 FA pre-PR checklist not executed:** NM-027 established a FA pre-PR checklist item:
   before any PR implementing a component with named performance ACs, verify the component uses
   the testid named in the spec. This was not run at PR #778.

3. **NM-027 QA post-ship activation check not executed:** NM-027 also required the QA Lead to
   verify all guarded assertions are producing real measurements when a previously guarded component
   ships. PR #778 was exactly this event. The check was not run.

This is the fourth recurrence of the NM-027 pattern class (NM-027: AC-007/AC-008 no-op guards;
NM-028: IR-004 SVG guard; NM-056: soft-skip via fixture null; NM-058: testid mismatch).

### Prior sprint exit audit trail note

M12–M15 sprint exit records that cite "Playwright CI green" as covering AC-009 contain an
inaccurate verification claim. These sprints are not reopened — Mode 3 has been functionally
sound throughout. NM-058 is the permanent record that AC-009 render performance coverage was
absent during M12–M15.

### Process improvement

1. **Immediate (G6 fix PR):** Testid corrected to `mode3-toggle`; `if (hasMode3)` and
   `if (renderMs !== null)` guards removed; replaced with unconditional `expect` assertions.
   FA brief AC-009 row updated to reflect delivered testid. (PR merged to `release/m16`.)

2. **QA Lead working agreement (`docs/process/agents.md §QA Lead Agent`):** Named no-op guard
   locator audit step added (NM-058 addition): at every sprint entry, run
   `grep -rn "isVisible().catch" frontend/tests/e2e/` and verify each guard's testid against
   `grep -rn "data-testid" frontend/src/`. Any guard whose testid does not appear in source is
   a filing-blocking finding. This converts the "remember to check" working agreement into a
   reproducible two-minute audit that would have caught this gap at every sprint entry since M12.

---

## NM-059 — AC-009 CI Measurement Methodology: Multi-CDP Round-Trip Contaminates Performance Window (Reactive)

**Date identified:** 2026-06-24
**Severity:** Medium
**Sprint:** M16-G6
**Detection:** Reactive — caught when EX-001 threshold raise (100ms → 200ms) revealed 179ms → 802ms variance between two consecutive CI runs on PR #1212. Without the threshold raise, the gate would have been flipping pass/fail on runner load with no visible signal of unreliability.

### What happened

After the NM-058 fix (AC-009 testid corrected, scenario setup added), the first real CI run measured 179ms — used as the calibration baseline for EX-001. The second CI run on the next PR measured 802ms against the same 200ms threshold. Both runs used the same test code and the same throttle rate (4×).

### Root cause

The measurement used three separate CDP evaluate calls with a Playwright `waitForTimeout(20)` between the start mark and the end mark:

```
CDP call 1: page.evaluate → performance.mark("mode3-start")   [T1 set in browser]
CDP call 2: mode3Trigger.click()                               [click dispatched]
            page.waitForTimeout(20)                            [Playwright waits 20ms wall-clock]
CDP call 3: page.evaluate → performance.mark("mode3-end")     [T2 set in browser]
```

T1 and T2 are browser-side timestamps (accurate). But the time between CDP call 2 completing and CDP call 3 executing in the browser is not bounded by the 20ms Playwright wait — it includes Playwright scheduler latency and CI runner event-loop queue time. On a lightly loaded runner: ~20–50ms overhead. On a loaded runner: hundreds of ms. The entire runner queue delay lands inside the T1–T2 measurement window.

### What was at risk

The AC-009 CI gate was measuring CI runner load, not Mode 3 render performance. Any sprint exit citing AC-009 as a passing performance gate was citing an unreliable measurement. Under sustained CI load, even the EX-001 raised threshold (200ms) would produce false failures — the gate would block PRs due to runner congestion, not actual render regressions.

### Fix

Both AC-009 (`trajectory-view.spec.ts`) and the MV-002 hardware test (`mv-002-hardware-validation.spec.ts`) updated to contain the entire measurement inside a single `page.evaluate` call. The programmatic click, start mark, RAF wait, and end mark all execute inside the browser's own event loop with no CDP round-trips in the measurement window. Two `requestAnimationFrame` cycles give React time to commit the synchronous state update.

### Process improvement

1. **QA Lead working agreement (`docs/process/agents.md §QA Lead Agent`):** Performance measurement methodology audit step added (NM-059 addition): at every sprint entry, run `grep -rn "performance.mark\|waitForTimeout" frontend/tests/e2e/` and verify that no test places a Playwright wait or separate `page.evaluate` call between its start and end performance marks. Any test that does is a filing-blocking methodology finding — multi-CDP measurement methodology produces CI-runner-load-dependent results, not render performance measurements.

2. **Pattern rule:** A valid Playwright performance measurement must either (a) contain both marks and the action being measured inside a single `page.evaluate` call, or (b) use `page.waitForFunction` with a browser-side condition (not a Playwright wall-clock wait) to trigger the end mark. `waitForTimeout` between performance marks is always a methodology violation.

---

## NM-060 — Startup Observability Gap: Empty simulation_entities Table Produces Silent 422 with No Diagnostic Signal (Reactive)

**Date identified:** 2026-06-24
**Severity:** Medium
**Sprint:** M16-G6
**Detection:** Reactive — caught when MV-002 ProBook hardware validation was blocked by
422 errors on scenario creation. Root cause took multiple investigation steps to identify
because no observability signal pointed to the seed gap.

### What happened

After `docker compose up --build` (and repeated with `down -v` for a fresh database),
scenario creation returned `422 Unprocessable Content` on the ProBook. The backend log
showed the 422 but not why. The frontend showed a generic error. The choropleth loaded
correctly (GDP growth 200 OK), so the stack *appeared* healthy. The real cause —
`simulation_entities` was empty because the Natural Earth loader had not been run —
required inspecting the API source to discover.

### Three-layer failure

1. **No startup observability:** The backend logs `Application startup complete.` with no
   check on whether `simulation_entities` is populated. A stack with zero entities is
   indistinguishable from a healthy stack in the startup log. The API health endpoint
   returns 200 regardless.

2. **Wrong fix command in CONTRIBUTING.md:** The troubleshooting entry said
   `docker compose exec api python scripts/natural_earth_loader.py` — a path that does
   not exist. The correct command is `docker compose exec api python -m app.db.seed.natural_earth_loader`.

3. **Wrong/incomplete symptom description:** CONTRIBUTING.md listed "choropleth is blank"
   as the only symptom. In practice the choropleth loaded correctly and the failure was
   a 422 on scenario creation — a completely different, unmatched symptom.

### What was at risk

Any developer or EL doing a first-time or fresh setup would hit this with no diagnostic
path. CI avoids the problem by explicitly running the seed loader (`.github/workflows/ci.yml`
line 232) — local and ProBook setups have no equivalent, and CONTRIBUTING.md's
troubleshooting entry was not discoverable from the observed symptom.

### Fix

CONTRIBUTING.md updated in this commit:
- Correct fix command: `python -m app.db.seed.natural_earth_loader`
- Primary symptom updated to scenario creation 422 (first encounter for most users)
- Explanation added that the stack appears healthy despite the empty table

### Process improvement

1. **GitHub issue filed for startup observability** (enhancement, M17): The backend
   should log a structured `WARNING` at startup lifespan if `simulation_entities` is
   empty, with the fix command in the log message. A zero-entity stack is never a valid
   operating state — it should say so. Issue filed against M17.

2. **Troubleshooting entry standard:** CONTRIBUTING.md symptoms must describe what a
   developer *observes* (HTTP status codes, UI behaviour, log lines) — not internal
   state requiring source inspection. "Choropleth is blank" was accurate but not the
   first observable signal; scenario creation 422 is.

---

## Registry Maintenance

### How to add an entry

When a near-miss is identified — during a session, in a HORIZON sweep, or in post-session
review — the PM Agent files a new entry following the template below:

```markdown
## NM-061 — AC-F8 Silent No-Op: Scenario Created via API But Never Selected in UI; 60-Second Ceiling Gate Measuring Nothing Since G3 (Reactive)

**Date:** 2026-06-24
**Milestone:** M16 — Distributional Visibility (gap origin: G3, PR #1172)
**Detected by:** PI Agent at G6 exit gate review, triggered by explicit EL activation. Sprint entry §3.1 pre-check was specified in writing but not executed during G6 validation.
**Severity:** High

### What happened

`frontend/tests/e2e/m16-g3-25year-human-capital-trajectory.spec.ts` AC-F8 measures the
time from scenario creation to `human-capital-trajectory-panel` visibility. The test
creates a SEN 100-step scenario via direct `fetch` API calls (`createSen100StepScenario()`),
runs it via API, then navigates to `/` and waits for the panel to become visible.

The panel is rendered in `ScenarioInstrumentCluster.tsx` only when:
```
(activeScenarioDetail?.configuration?.projection_steps ?? 0) > 8
```

`activeScenarioDetail` reflects the **UI-selected** primary scenario. The test creates
the scenario via API but never selects it in the UI — there is no Scenarios panel
interaction, no `Select as primary scenario` click, no `__worldsim_selectEntity` call.
When the test navigates to `/`, no scenario is selected, `activeScenarioDetail` is null
or undefined, and the panel never renders.

The guard at line 459 (`if (!(await panel.isVisible(...).catch(() => false))) return;`)
fires silently, and the test returns without asserting anything. AC-F8 has been a
passing CI gate that measures nothing since G3 shipped (PR #1172, 2026-06-24).

The G6 sprint entry (§3.1) required an explicit pre-check: *"Before running VC-2, verify
the AC-F8 test assertion path is live (not silently skipped via `catch(() => false)`)."*
This pre-check was not executed during G6 validation, and the validation report did not
address it. The PI Agent discovered the gap at exit gate review.

### What was at risk

AC-F8 is the CI gate for G3's contracted simulation ceiling: 100-step scenarios must
complete within 60 seconds (CE Assessment Decision 4, `docs/process/sprint-plans/m16-g3-sprint-entry.md §2.5`).
G3's sprint exit record cites AC-F8 as PASS. That citation is inaccurate — the test has
been measuring nothing. A simulation engine regression that caused 100-step scenarios to
exceed 60 seconds would be invisible to CI.

The VC-2 ProBook timing (0.5s for 100 steps) confirms the simulation currently runs well
under the ceiling. But the CI guard provides no regression protection.

### What caught it

PI Agent review at G6 exit gate, triggered by explicit EL activation (`BPO and PI Agents:
validate and confirm G6 exit`). The sprint entry §3.1 pre-check requirement was written
in advance specifically to prevent this failure mode — it was caught because it was named
in the entry document and the PI Agent checked whether it had been satisfied.

This is partial process success (the requirement was anticipated and written down) and
partial process failure (the requirement was not executed). The pre-check existed on paper
but had no enforcement mechanism to ensure it ran.

### Root cause — same failure mode as NM-058, different mechanism

NM-058: testid mismatch — guard locator finds nothing in DOM
NM-061: setup mismatch — testid is correct, but component never renders because test
setup (API-only scenario creation) does not satisfy the render condition

The NM-058 QA Lead audit step (`grep -rn "isVisible().catch" frontend/tests/e2e/`)
would have found this guard and checked the testid — `human-capital-trajectory-panel`
exists in source. The audit step would have passed, missing the setup gap entirely.
The two failure modes require two distinct audit questions.

### Process improvement

**Immediate (G6 fix — this session):** AC-F8 must be updated to select the created
scenario in the UI before checking panel visibility. After `createSen100StepScenario()`
returns a `scenario_id`, use the Scenarios panel UI to select the scenario as primary
(same pattern as `mode3-active-control.spec.ts` and the AC-009 fix in PR #1211).

**QA Lead working agreement addition (NM-061 addition):** The NM-058 audit step covers
testid correctness but not setup correctness. A second audit question must be added to
the working agreement: *For any E2E test that creates scenario or entity data via direct
`fetch` API calls and then checks for conditional UI component visibility, verify the
test also selects or activates that data through the UI before checking visibility.
API-created data that is never surfaced through a UI selection action will not satisfy
conditional renders that depend on `activeScenarioDetail`, `selectedScenarioId`, or
equivalent state.* This audit requires reading the render condition in the source
component, not just checking the testid.

The two-part audit (NM-058: testid correctness; NM-061: setup completeness) together
cover both failure modes of the soft-skip pattern.

**Sprint entry pre-check enforcement:** The G6 sprint entry named the AC-F8 pre-check
as a blocking condition. The failure was that "named in the entry" did not translate to
"executed in the validation." Sprint validation checklists must include a named sign-off
for each named pre-check — not just a description of what to check, but a filled-in
result field. The validation report template for future sprints must include a
`pre-checks performed` section with one row per entry-document-named pre-check, each
requiring an observed result (not a checkbox).

---

## NM-062 — Demo Spec `getByText("Step N")` Collides with Projection Panel Step Axis Spans; Every Demo Run Would Fail with Strict Mode Violation (Reactive)

**Date:** 2026-06-24
**Milestone:** M16 — Distributional Visibility (gap origin: G3/G8 interaction)
**Detected by:** Demo spec execution failure at Step 6 during M16-G8 demo preparation
**Severity:** High

### What happened

`demo-narrated.spec.ts` used `page.getByText("Step N")` to assert that the step counter
had advanced after each `nextStepBtn.click()`. `getByText` in Playwright performs a
default substring match — an element is matched if its text content *contains* the target
string.

`HumanCapitalTrajectoryPanel` (G3/#274) renders a step axis with static spans:
```tsx
<span>Step 1</span>
<span>Step 25</span>
<span>Step 50</span>
<span>Step 75</span>
<span>Step {projectionSteps}</span>   // "Step 100" for 100-step demo scenario
```

`getByText("Step 1")` matched both:
1. `<span>Step 1</span>` — the projection panel step axis start label (exact match)
2. `<span>Step 100</span>` — the projection panel step axis end label ("Step 100" contains
   "Step 1" as a prefix substring)

Playwright strict mode requires locators to match exactly one element. The assertion
failed with: *"strict mode violation: getByText('Step 1') resolved to 2 elements."*

The demo spec was originally authored before `HumanCapitalTrajectoryPanel` existed.
When G3 added the panel (PR #1172), the static step axis labels created an undetected
collision with the existing step navigation assertions. The collision was only discovered
when the demo spec was executed at Step 6 of G8 demo preparation.

### What was at risk

Every demo run — including the M16 live stakeholder demo (#843, M16 exit gate) — would
fail before capturing any screenshots. The walkthrough would abort at Step 1 advance with
a strict mode violation. The five frame screenshots required for Step 6b and the internal
panel review would not be captured.

### What caught it

Step 6 execution of the demo script during M16-G8 demo preparation. The failure appeared
as the first advance assertion in the test. This was caught during demo preparation, not
during a live stakeholder session — the G8 demo preparation protocol (Steps 5b, 6, 6b
before any live audience) is functioning as designed.

### Process improvement

**Immediate fix:** All `page.getByText("Step N")` assertions replaced with
`page.locator('[data-testid="current-step-display"]').toContainText("Step N")`.
The `current-step-display` testid is on `<span>` in `ScenarioControls.tsx` — the
actual step counter showing "Step N / totalSteps". This locator is unique and unambiguous.

**QA Lead working agreement addition (NM-062):** When a new component introduces static
text content — particularly labels, axis annotations, or header strings — the authoring
agent must check whether existing test specs use `getByText()` with any of those strings.
The check is: `grep -r 'getByText.*Step\|getByText.*{string}' frontend/tests/e2e/`.
If any existing spec uses a `getByText` that would collide with new static text, the
locator in the existing spec must be updated to a scoped testid-based locator before the
new component is merged. This check is a required line item in the frontend pre-push gate
for any PR that adds visible static text to a component rendered in the primary viewport.

---

## NM-063 — CohortImpactSection Text Overflow Not Covered by Legibility Spec; Same Gap Class as NM-056 (Reactive)

**Date:** 2026-06-24
**Milestone:** M16 — Distributional Visibility
**Detected by:** EL live demo observation (G8 Demo 6 walkthrough)
**Severity:** High

### What happened

`CohortImpactSection` renders cohort crossing rows with `display: flex` and a `flex: 1`
content span containing the cohort label. Without `minWidth: 0` on the flex container
and `display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap` on
the label span, long cohort labels (e.g., "bottom quintile, informal workers — poverty
headcount ratio") overflow the row container and overlap adjacent rows vertically.
This was observed during the EL live demo (2026-06-24, G8 Demo 6). The EL noted text
was "cut/overlapping with other text vertically — unacceptable UX/UI at this stage."

`demo-legibility.spec.ts` did not cover `CohortImpactSection` text overflow. The existing
Zone 1B MDA overflow check (test: "Zone 1B MDA panel text is not overflow-clipped") guards
`zone-1b-top-detail` only — not the cohort section which is a sibling component.

### What was at risk

The primary Zone 1B argument in Demo 6 — the cohort threshold crossing that identifies
which cohort bears the cost of the programme — would be illegible to stakeholders. The
component delivering the mission-critical Persona 2 output was degraded at the moment
the EL demonstrated it to external participants.

### What caught it

EL live demo observation. The legibility spec existed and had been extended in M14–M16
but did not include a test for `CohortImpactSection`, which was added in M16-G2 (#986).
New components added to the primary viewport were not added to the legibility spec in the
same sprint. This is the same gap class as NM-056 (test coverage gap for a component added
mid-milestone).

### Process improvement

**Immediate fix:** `CohortImpactSection` label span now has `display: block; overflow: hidden;
text-overflow: ellipsis; white-space: nowrap` with `minWidth: 0` on the flex:1 container.
Applied in M16-G8 PR (2026-06-24).

**Legibility spec extension:** New test `"NM-063: CohortImpactSection label text is not
overflow-clipped at 1440×900"` added to `frontend/tests/e2e/demo-legibility.spec.ts`.
Advances one step, checks the `zone-1b-cohort-impact` container for non-overflow; if
crossing rows are present, checks each label span.

**QA Lead working agreement addition (NM-063):** When a new component delivering a
primary surface output (Zone 1A, 1B, 1C, 1D) is added to the instrument cluster, the
authoring sprint must extend `demo-legibility.spec.ts` with at minimum: (1) non-zero
bounding box for the component container; (2) non-overflow on any text-rendering spans
visible at 1440×900. Adding the component without the legibility extension is a
compliance gap — QA Lead must flag this in the sprint exit review if not completed
in the implementation PR.

**Near-miss lineage:** Same gap class as NM-056 (M14: test suite gap for mid-milestone
component addition). M16-G2 added `CohortImpactSection` to the primary surface; legibility
coverage was not added in the same sprint.

---

## NM-064 — AC-009 Performance Test Consistently Exceeds 200ms Threshold on GHA Shared Runners; test.fixme() Required to Unblock CI (Anticipatory)

**Date:** 2026-06-25
**Milestone:** M17 — Calibration and Comparative Infrastructure
**Detected by:** EL direction during G2 sprint entry PR (#1289) CI review
**Severity:** Medium — blocks CI-green merges on unrelated PRs; no incorrect outputs produced

### What happened

`AC-009` (`trajectory-view.spec.ts:156`) is a Mode 3 render performance test that applies
a 4× CPU throttle via CDP and asserts `renderMs ≤ 200ms` (threshold raised from 100ms per
EX-001, approved 2026-06-24). On the M17 G2 sprint entry PR (#1289), AC-009 failed in two
consecutive CI runs with measured times of 712ms and 771ms — both 3–4× the 200ms threshold.
The test had been passing in recent release branch CI runs (e.g., run after PR #1286).

This test was previously identified as high-variance: NM-059 (prior multi-CDP approach
produced 179ms–802ms variance) and EX-001 (raised threshold from 100ms to 200ms at M14
exit). The PR #1289 failures are consistent and well above the raised threshold, suggesting
the current GHA runner load makes the 4× throttle performance gate unreliable as a CI check.

### What was at risk

Any PR that triggers the Playwright E2E suite on a loaded GHA runner will fail AC-009
regardless of whether the PR introduced any performance regression. This makes AC-009 a
false CI gate — blocking unrelated merges while providing no signal about actual performance
change.

### What caught it

EL directed disabling the test and filing an exception after two consecutive CI failures
on a PR containing only process documents (no frontend code changes).

### Root cause

The CI GitHub Actions shared runner (2-core, throttled to effectively 0.5-core for this
test) cannot reliably render a React/Recharts component cluster in under 200ms. The 4× CDP
throttle is too aggressive for the GHA shared runner tier. The test provides no meaningful
performance regression signal when the baseline varies by 3–4× between runs.

### Process improvement

**Immediate:** Add `test.fixme()` to AC-009 in `trajectory-view.spec.ts` referencing
NM-064 and KI-006. This authorizes the skip per NM-056 (skip requires NM entry on record).

**KI filed:** KI-006 — external infrastructure limitation (GHA shared runner can't
reliably satisfy 200ms throttled render threshold).

**EX-001 update:** EX-001 (docs/compliance/exceptions.md) to be updated at M17 exit
review to either: (a) resolve by removing AC-009 from CI scope, or (b) convert to a
local-only performance gate with a higher CI threshold.

**Performance gate ownership:** AC-009 should be converted to a local developer gate
(not a CI gate) or replaced with a Playwright `--trace` perf annotation that records
render time without asserting a threshold. A performance regression is better caught via
comparison to prior runs than via absolute threshold on variable shared infrastructure.

---

## NM-065 — No SOP for Intentionally-Red Pre-Implementation QA Tests; Ad-Hoc Resolution Required (Anticipatory)

**Date:** 2026-06-25
**Milestone:** M17 — Calibration and Comparative Infrastructure
**Detected by:** EL review of PR #1290 CI failure (G3 early QA filing)
**Severity:** Low — no incorrect outputs; CI blocked on unrelated PRs; ad-hoc resolution added process debt

### What happened

PR #1290 (`chore/m17-g3-early-qa-filing`) filed the G3 regression guard test before G3 Phase 3
implementation. AC-A2 (`m17-g3-zone-1b-allocation.spec.ts:454`) was explicitly authored WITHOUT
an early-return guard — by design, to confirm it was red before implementation. The test
intentionally fails pre-implementation: `zone-1b-mda-panel-wrapper` does not exist until G3
Phase 3 adds the testid.

When the PR reached CI, playwright-e2e failed on AC-A2. This blocked the merge of an
unrelated PR (SESSION_STATE.md) on the same CI run. There was no documented mechanism in the
sprint planning SOP or QA filing process for handling an intentionally-red pre-implementation
test.

All previous pre-implementation QA tests in M14–M16 used early-return guards (`if (!someTestid)
return;`) to stay CI-green while still filing the test structure. AC-A2 was the first test to
explicitly opt out of that pattern (the intent document cited NM-056 and specified "no
soft-skip patterns; AC-A2 must be hard-fail"). The two patterns are incompatible: the spec
required a hard-fail, but the process assumed CI-green QA filing PRs.

### What was at risk

Any QA team member filing a regression guard test in the same "red-before-green" pattern
would face the same undocumented conflict. Without a process answer, the resolution defaults
to ad-hoc EL direction each time.

### What caught it

EL recognized the conflict when reviewing CI failures on PR #1290 and directed the resolution
(EX-002 + `test.fail()` + intent doc reversal steps + NM-065).

### Root cause

The sprint planning SOP (`docs/process/sprint-planning-sop.md`) and QA filing process do not
specify what to do when a test must be intentionally red pre-implementation. The only prior
guidance was NM-056 (no soft-skips without a near-miss on record) and the early-return guard
pattern. These two mechanisms serve different purposes:

- **Early-return guard:** test appears to pass (skips assertions) before implementation; provides
  no regression detection if the test structure is wrong; CI stays green.
- **`test.fail()`:** test runs, must fail pre-implementation (CI passes), and CI fails when it
  unexpectedly passes post-implementation (regression detection still works); CI stays green.

The QA filing process assumes early-return guards are the only mechanism. The intent document
correctly specified a hard-fail pattern but the SOP had no process home for it.

### Process improvement

**Immediate:** EX-002 filed; `test.fail()` applied to AC-A2; intent document updated with
reversal steps. Testid reconciled from `zone-1b-mda-panel` to `zone-1b-mda-panel-wrapper`
in the same PR.

**SOP update required:** `docs/process/sprint-planning-sop.md §QA Filing` (or equivalent QA
section) must document two approved patterns for pre-implementation QA tests:

1. **Early-return guard** (preferred for most tests): `if (!locator.isVisible()) return;` — test
   stays green pre-implementation; appropriate when the test structure is complete and only the
   testid is missing.

2. **`test.fail()` + EX-NNN** (required for regression guards): when the spec requires the test
   to be hard-fail before implementation (i.e., CI must confirm the test is red), apply
   `test.fail()`, file an exception (EX-NNN), and document reversal steps in the intent
   document. The test must fail before implementation and CI must fail when it unexpectedly
   passes after implementation.

The choice between patterns is a QA Lead decision documented in the intent document §5 AC
preamble. A regression guard AC that opts out of the early-return pattern must document why.

---

## NM-066 — SESSION_STATE.md Exceeds Claude Code Read Ceiling; Session Continuity Guarantee Silently Degraded (Reactive)

**Date:** 2026-06-26
**Milestone:** M17 — Calibration and Comparative Infrastructure
**Detected by:** EL observation during session startup (person, not process)
**Severity:** High — the foundational session continuity protocol requires reading `SESSION_STATE.md` in full at session start; the file now exceeds the 256 KB Claude Code read ceiling, meaning agents have been silently operating on truncated session state for an unknown number of sessions

### What happened

`SESSION_STATE.md` grew to 2,038 lines / 301 KB across milestones M9–M17 with no archival process, no size limit, and no CI check. Claude Code's maximum file read size is 256 KB. Any agent that attempted to read `SESSION_STATE.md` as specified by `CLAUDE.md §Session Continuity` would receive a truncation error or silently incomplete content. The file has exceeded the read ceiling by approximately 45 KB.

The EL identified the size issue during a session startup review and filed GitHub Issue #1328 to investigate remediation options.

### What was at risk

The session continuity guarantee — that every agent begins a session with complete awareness of current milestone status, open PRs, pending decisions, and in-progress work — has been silently unachievable. An agent that cannot read the full file may:

- Miss recent EL architectural decisions recorded in the lower half of the file
- Miss open work streams or pending decisions from earlier in the current milestone
- Operate on an incomplete picture of which sprint groups are active or which PRs are open
- Make implementation or process decisions that contradict state it cannot see

Because the truncation happens silently (no error is surfaced to the agent), the gap is invisible: the agent believes it has fulfilled the continuity read requirement, but has not.

### What caught it

EL noticed the file size during a session. No process gate flagged it. This is evidence that the process had a gap — the continuity protocol specifies what to read but places no constraint on the maximum size of what must be read, and CI has no check on file size.

### Root cause

The session continuity protocol (`CLAUDE.md §Session Continuity`) specifies `SESSION_STATE.md` as a required read but defines no maximum file size, no archival cadence, and no enforcement mechanism. The file has accumulated content from every milestone since M9 without any rotation or archival step. There is no CI check that would flag when the file approaches the tool's read ceiling.

### Process improvement

**Immediate:** GitHub Issue #1328 filed to investigate and select a remediation option (archive-and-rotate, sprint journal issue, cockpit-card model, or hybrid). Decision to be recorded as an EL architectural decision entry; new format to activate at M18 kickoff.

**Required at M18 kickoff (blocking):**
1. `SESSION_STATE.md` reduced to or below a defined line limit (proposed: ≤ 150 lines) before M18 implementation begins.
2. An archival or rotation protocol defined and documented in `CLAUDE.md §Session Continuity`.
3. A CI lint step (or pre-push check) added that fails if `SESSION_STATE.md` exceeds the defined limit, so the ceiling violation is caught at push time rather than by EL observation.

**Near-miss lineage:** The root cause is structural accumulation with no expiry mechanism — the same pattern class as scan-registry ordering violations (NM noted in CLAUDE.md) and known-issues registry growth. Any append-only or accumulating document that lacks a size limit or rotation protocol is a candidate for the same failure.

---

## NM-067 — No Sprint Group Isolation Protocol for Parallel Workstreams; Unregulated Release Branch Merges Causing Lost Updates and Rework Across M15–M17 (Reactive)

**Date:** 2026-06-26
**Milestone:** M17 — Calibration and Comparative Infrastructure (pattern identified; instances across M15–M17)
**Detected by:** EL pattern recognition across M15–M17 PR history (person, not process)
**Severity:** High — actual work was lost, rework was required, and wrong-target merges occurred across three consecutive milestones; no process gate prevented any instance

### What happened

The current branching model allows multiple sprint groups to cut `feat/m{N}-g{N}-*` branches from `release/m{N}` simultaneously and merge back to `release/m{N}` as implementation PRs complete, with no coordination protocol and no isolation between groups. When two or more Claude Code sessions run parallel sprint groups against the same release branch, several failure modes recur:

**Documented instances in M15–M17 PR history:**

| Failure mode | Evidence |
|---|---|
| Duplicate PRs — same-named PR opened twice because a conflict-forced re-open overwrote the first | #1293 and #1294 both named `chore/m17-state-g3-phase2-complete`; #1307 and #1308 both named `chore/m17-g3-g2-entry-approvals` |
| Wrong-target merge — feature branch merged to `main` instead of `release/m{N}` | #1303 `chore/m17-g4-session-state-v2` → `main` |
| Post-exit rework — one group's merge reveals a spec gap in an already-exited group | `feat/m17-g5-g3-spec-fix` (#1319) required after G3 sprint exit (#1320) |
| CLOSED PRs with lost work — state rebuilt elsewhere after a conflict superseded the PR | #1290, #1292, #1299, #1302, #1304, #1306 all closed without merging |
| Shared file overwrites — last merge wins, silently discarding earlier additions | Multiple groups writing `SESSION_STATE.md`, `near-miss-registry.md`, and `scan-registry.md` concurrently |

The primary conflict vector is shared non-code files: every sprint group writes `SESSION_STATE.md` and may write registry files, meaning any two concurrent groups are in a guaranteed write conflict regardless of whether their code changes overlap.

### What was at risk

- **Silent data loss:** When two groups both append to `SESSION_STATE.md` and one merge overwrites the other, the overwritten content is lost without any error. Registry entries (near-miss, scan, known issues) are permanent institutional memory — a silently overwritten entry is an integrity violation.
- **CI running on incomplete state:** A PR that merges after a conflicting group has already merged may push a state where partially-integrated code reaches CI before it is ready, producing false passes or false failures that consume sprint capacity to diagnose.
- **Cascading rework:** When one group's implementation invalidates a spec that another group has already shipped (the M17 G1→G2→G5 cascade), there is no mechanism to detect or route the dependency at sprint entry. The rework is discovered at merge time, not at planning time.

### What caught it

EL review of the M17 PR history identified the pattern. No process gate prevented any individual instance. The only detection mechanism was EL post-hoc observation, which means each instance consumed rework capacity before being caught.

### Root cause

The release branch workflow (`CLAUDE.md §Release Branch Workflow`) defines how a single feature branch should be managed but does not address parallel sprint group coordination. There is no:

1. **Sprint group isolation protocol** — no sub-branch layer between feature work and the release branch when groups run in parallel
2. **Shared file coordination lane** — no designated single writer for `SESSION_STATE.md`, registry files, and other files that every group modifies
3. **File-conflict risk assessment at sprint entry** — no step in the sprint entry gate that identifies which files a group will write and which other active groups write the same files
4. **Cross-group dependency declaration** — no mechanism at sprint planning to declare upstream/downstream dependencies between groups (e.g., G1 calibration → G2 wiring → G5 display), so cascading impacts are discovered at merge time rather than at entry time

### Process improvement

**Immediate:** GitHub Issue #1329 filed to investigate and select a branching model. Proposed direction (Option E — hybrid): sprint group sub-branches (`sprint/m{N}-g{N}`) for code isolation, combined with a PM Agent coordination lane for shared-file writes.

**Required at M18 kickoff (blocking):**
1. EL selects a branching model and records the decision as an architectural decision entry.
2. `CLAUDE.md §Release Branch Workflow` updated to reflect the new model.
3. Sprint entry template (`docs/process/sprint-plans/templates/sprint-entry-template.md`) amended to include a **file-conflict risk assessment field**: list of files the group will write, and which other active groups write the same files. If overlap exists, the entry gate requires a coordination protocol before implementation may begin.
4. Cross-group dependency declaration added to sprint entry: if this group's implementation depends on another group's output, the upstream group's integration PR must be merged to the release branch before this group opens its own integration PR.
5. PM Agent coordination lane protocol defined (if hybrid model is selected): what triggers a shared-state sync PR, which files it covers, and how sprint groups signal the PM Agent that a shared-file update is ready to queue.

**Near-miss lineage:** The root cause — a process that works correctly for sequential workstreams silently breaks under parallel execution — is a structural gap that will recur in any milestone with ≥ 2 simultaneous sprint groups. M18 is expected to have parallel workstreams. This gap must be closed before M18 implementation begins.

---

## NM-068 — Prior NM Process Improvements Not Verified at Sprint Entry; NM-027 Pattern Class Has Recurred Four Times (Reactive)

**Date:** 2026-06-26
**Milestone:** M17 — Calibration and Comparative Infrastructure (pattern identified; recurrences across M12–M17)
**Detected by:** EL pattern recognition across NM registry — NM-058 explicitly labels NM-027's fourth recurrence
**Severity:** High — process improvements recorded in the near-miss registry are not preventing recurrence; the NM registry fulfils its forensics function but its prevention function is structurally incomplete

### What happened

The NM-027 pattern class — a QA test that measures nothing because a no-op guard was not removed after the component it guarded against was wired up — has recurred four times:

| Entry | Sprint | What recurred |
|---|---|---|
| NM-027 | M12 | AC-007 and AC-008 no-op guards masked non-measurement for one milestone |
| NM-028 | M13 | IR-004 trajectory tick year test was a silent no-op for one milestone |
| NM-047 | M14 | G5 Playwright AC-3 timing-dependent; guard timeout produced no-op |
| NM-058 | M16 | AC-009 testid mismatch; Mode 3 performance gate silent no-op since M12 |

Each recurrence produced a process improvement: the QA Lead working agreement was amended after NM-027, and additional audit steps were added after NM-028, NM-047, and NM-058. The amendments exist in the working agreement text. They do not prevent recurrence because nothing at sprint entry verifies that the relevant prior process improvements are being applied to the current sprint group's scope.

This is not isolated to the NM-027 class. NM-052 established that the backend pre-push mypy gate had been non-functional locally since M8 — a structural fix from NM-016 created the appearance of a gate without the reality of one. The NM-016 process improvement (add pre-push lint gate) was implemented; the NM-052 recurrence revealed that "implemented" had not been verified to mean "functional."

### What was at risk

The near-miss registry's stated purpose is both forensic (record what happened) and preventive (drive process improvements that stop recurrence). The forensic function is working: 67 entries document failures with root causes. The preventive function has a structural gap: there is no mechanism to verify that prior improvements are in effect when a sprint group begins work. A process improvement that exists in the working agreement but is not checked at entry time will not prevent recurrence by a different agent in a different session.

### What caught it

EL recognition of the recurrence pattern while reviewing the NM registry — specifically the NM-058 entry's explicit "fourth recurrence" label. No process gate surfaced the recurrence. The working agreement additions from prior entries were not consulted at the point when they would have been actionable (sprint entry or PR authorship).

### Root cause

The sprint entry gate (`docs/process/sprint-planning-sop.md §Sprint Entry Gate`) does not include a step requiring the implementing agent to identify which prior NM process improvements are relevant to the sprint group's scope and confirm they are in place. The NM registry entries themselves contain the improvement specifications, but they are written as permanent institutional records — not as a checklist consulted at sprint entry. The two functions (record and prevent) are in the same document but have no mechanism connecting them at the point of action.

### Process improvement

**Immediate:** GitHub Issue #1330 filed to investigate a sprint entry NM verification step.

**Required at M18 kickoff (blocking):**
1. Sprint entry template (`docs/process/sprint-plans/templates/sprint-entry-template.md`) amended to include a **"Prior NM applicability check"** field: at sprint entry, the implementing agent must search the NM registry for entries whose process improvements apply to the sprint group's implementation domain (backend, frontend, E2E tests, shared files, demo specs, etc.) and explicitly confirm each relevant improvement is in effect. For domain-specific sprints, a short curated lookup list (e.g., "frontend E2E sprint groups must confirm NM-027/028/047/058/061 guard activation check is in working agreement and will be executed") is more actionable than a full registry scan.
2. PM Agent sprint entry review responsibility extended: PM Agent checks that the Prior NM applicability check field is complete before recommending EL approval.

**Near-miss lineage:** NM-027 → NM-028 → NM-047 → NM-058 → NM-061 form the primary recurrence chain. NM-016 → NM-052 form a second chain in the same gap class (improvement implemented but not verified as functional). NM-068 addresses the structural root common to both chains.

---

## NM-069 — Gitignore Missing Playwright and Test Artifact Directories; Accidental Staging Would Commit Binary Artifacts to History (Anticipatory)

**Date:** 2026-06-26
**Milestone:** M17 — Calibration and Comparative Infrastructure
**Detected by:** EL observation — persistent untracked files in git status across multiple sessions
**Severity:** Medium — no accidental commit has occurred; risk is latent but the untracked artifacts are present in every session, and the process has at least one known pathway (`git add -A`) that would capture them

### What happened

The following paths are consistently untracked in git status and are not covered by `.gitignore`:

- `backend/test-results/`
- `frontend/playwright-report/`
- `frontend/session-screenshots/`
- `frontend/test-results/`
- `docs/process/near-miss-registry.md.test-marker`

These are generated test and CI artifacts — Playwright HTML reports, session screenshots, JSON test result files — that have no place in version control. The current `.gitignore` covers `.coverage`, `htmlcov/`, `.pytest_cache/`, and `backend/sessions/*.json` but does not cover Playwright output directories or session screenshot directories.

CLAUDE.md §Commit process warns against `git add -A` or `git add .` due to the risk of capturing sensitive files. This warning is the only defence against the gap. It relies on agent compliance and is not structural.

### What was at risk

A `git add -A` or `git add .` at any point — including by an agent following a pattern from training data rather than CLAUDE.md — would stage all untracked files, including Playwright HTML reports (which can contain screenshots and full page captures), session screenshots, and test result JSON files. Once committed and pushed, large binary artifacts require `git filter-repo` or a force-push to remove, both of which are destructive operations that rewrite history. The `docs/process/near-miss-registry.md.test-marker` is an unknown artifact whose provenance is unclear — it could be a CI test fixture or a leftover from a failed test run; its presence in the working tree without a gitignore entry is itself a gap.

### What caught it

EL noticed the persistent untracked files in git status during session review. No CI check or pre-push gate flags untracked files that should be ignored. Detection was person-dependent.

### Root cause

The `.gitignore` was authored before Playwright E2E testing was introduced and has not been updated to cover Playwright output directories. `session-screenshots/` was added by a sprint group to capture browser automation outputs but was not accompanied by a gitignore entry. There is no process step that requires a gitignore audit when a new test framework, output directory, or CI artifact path is introduced.

### Process improvement

**Immediate:** GitHub Issue #1331 filed. `.gitignore` update is a one-PR fix — add `backend/test-results/`, `frontend/playwright-report/`, `frontend/session-screenshots/`, `frontend/test-results/`, and `*.test-marker` entries. The `near-miss-registry.md.test-marker` artifact should be investigated (deleted if a leftover, gitignored if generated by a test harness).

**Process addition:** Sprint entry template amended to include a **"New output paths"** field: any sprint group whose implementation generates new output directories (test results, screenshots, reports, build artifacts) must either (a) confirm the path is already covered by `.gitignore`, or (b) include a `.gitignore` update in the same implementation PR. PM Agent checks this field at sprint entry review.

---

## NM-070 — Pre-Push Gates Enforced by Documentation Only; No Git Hook Enforcement; Gates Non-Functional or Bypassed Across Multiple Milestones (Reactive)

**Date:** 2026-06-26
**Milestone:** M17 — Calibration and Comparative Infrastructure (structural gap; individual instances in NM-016, NM-052, NM-054)
**Detected by:** EL pattern recognition across NM-016, NM-052, NM-054 — the same structural absence underlies all three
**Severity:** High — the pre-push gates are stated as mandatory in CLAUDE.md but are enforced only by agent compliance; two documented instances (mypy gate non-functional M8–M16; E2E breakage not caught pre-push) show the compliance-only model fails across milestone boundaries without detection

### What happened

CLAUDE.md §Backend pre-push lint gate and §Frontend pre-push build gate define mandatory pre-push checks: `ruff check . && mypy app/` for backend Python changes, `npm run build` for frontend changes. Both are described as blocking: "Both must exit 0." "Must exit 0."

Despite this language, neither gate has a structural enforcement mechanism. There is no git pre-push hook that runs the checks. There is no CI fast-fail that distinguishes "gate not run" from "gate run and passed." An agent that pushes without running the gates faces no immediate consequence — CI catches the error instead, which is exactly the outcome the gates were designed to prevent.

**Documented failures under this structural gap:**

| Near-miss | What the gate missed | Duration |
|---|---|---|
| NM-016 | Lint gate absent from agent prompts; two PRs failed CI on trivially-preventable errors | M10 (gate established) |
| NM-052 | mypy gate non-functional locally since M8 — Python 3.13 venv not documented; gate ran but produced meaningless output; every local mypy run since M8 was either a syntax error (Python 3.10) or 99 false-positive errors (Python 3.13 without deps) | M8–M16 (8 milestones) |
| NM-054 | Frontend build gate does not catch E2E breakage; `npm run build` passes while 6 Playwright tests fail; UI contract change (`select` → `combobox`) reached CI uncaught | M16 |

NM-052 is the most consequential: for eight milestones, the mypy gate appeared to be running but was providing false confidence. Agents who ran it and saw output believed the check passed. The gate was protecting nothing.

### What was at risk

The pre-push gates exist to make CI a confirmation, not a discovery mechanism. When gates are non-functional or not run, CI becomes the first line of defence, which means:
- Type errors, lint violations, and build failures are discovered at CI round-trip time rather than at push time — adding minutes to every iteration
- Agents who believe the gate passed may not investigate CI failures promptly ("I ran the gate, so this must be a CI environment issue")
- Errors can accumulate across PRs if CI is slow to surface them

The mypy gap specifically means type errors introduced across eight milestones of Python backend work were caught only by CI — or not caught at all if CI was not blocking in that period.

### What caught it

Individual instances were caught by CI failure (NM-016, NM-054) or by EL noticing anomalous mypy output (NM-052). No process gate detected that the pre-push gates themselves were non-functional. This is the deepest version of the gap: a process check that fails silently produces the same output as one that succeeds.

### Root cause

The pre-push gates are documentation obligations, not structural constraints. A git pre-push hook runs automatically before every push regardless of which agent or human is pushing — it cannot be omitted by accident or by a new agent unfamiliar with the CLAUDE.md mandate. The gates have never been implemented as hooks.

A secondary root cause for the mypy gap specifically: the gate instruction did not specify the Python environment required (`python3.13 -m venv .venv`), so agents running `mypy app/` in the wrong environment received output that appeared meaningful but was not. The gate instruction has been updated (NM-052 fix), but the structural gap — no hook enforcement — remains open.

### Process improvement

**Immediate:** GitHub Issue #1332 filed. This is an M18 entry blocker.

**Required at M18 kickoff (blocking):**
1. Implement a git pre-push hook at `.git/hooks/pre-push` (or via a hook manager like `pre-commit`) that:
   - Detects whether the push touches `backend/` Python files; if so, runs `cd backend && source .venv/bin/activate && ruff check . && python -m mypy app/`
   - Detects whether the push touches `frontend/src/`; if so, runs `cd frontend && npm run build`
   - Exits non-zero on any failure, blocking the push
   - Prints a clear error message distinguishing lint failure from environment failure (missing venv → `ERROR: backend/.venv not found — run setup first`, not a silent mypy 99-error run)
2. Hook installation documented in `docs/CONTRIBUTING.md §Development Setup` as a required setup step, not an optional one.
3. CLAUDE.md §Backend pre-push lint gate and §Frontend pre-push build gate updated to reference the hook as the enforcement mechanism: "The pre-push hook enforces this gate automatically. If the hook is not installed, install it before pushing."
4. CI fast-fail step added that checks for a sentinel file written by the hook — so CI can distinguish "hook ran and passed" from "hook was not present."

**Near-miss lineage:** NM-016 established the lint gate. NM-052 revealed the mypy gate had been non-functional for eight milestones. NM-054 revealed the frontend build gate does not cover E2E breakage. NM-070 identifies the structural root cause common to all three: documentation-only enforcement. Closing NM-070 closes the root cause that enabled NM-016, NM-052, and NM-054 to occur.

---

## NM-071 — No Sprint Group Concurrency Ceiling at Sprint Planning; Unbounded Parallelism Upstream Cause of NM-067 Coordination Failures (Anticipatory)

**Date:** 2026-06-26
**Milestone:** M17 — Calibration and Comparative Infrastructure
**Detected by:** EL pattern recognition — identified as the upstream planning gap enabling NM-067
**Severity:** Medium — no specific ceiling violation has been defined or breached; M17's seven parallel sprint groups is the proximate upstream condition for the coordination failures documented in NM-067

### What happened

M17 ran seven sprint groups (G1 through G7) across two waves, with multiple groups running simultaneously in parallel Claude Code sessions. The current sprint planning SOP has no step that asks: "how many groups will run concurrently in this wave, and does the shared-file coordination overhead remain manageable at that count?"

The consequences of unmanaged concurrency were documented in NM-067: duplicate PRs, wrong-target merges, shared-file overwrites, and post-exit rework. NM-067 proposes a branching model fix (sprint group sub-branches + PM Agent coordination lane). But the branching fix addresses the symptom; it does not address the upstream planning question that determines whether the coordination load is feasible in the first place.

A sprint planning process that can authorise seven parallel groups with no explicit coordination budget is a structural gap independent of what branching model is chosen. Even with sprint group sub-branches, seven simultaneous groups sharing a PM Agent coordination lane will overwhelm the lane's capacity.

### What was at risk

As parallel group count increases, coordination overhead scales nonlinearly:
- Each additional group adds shared-file write conflicts proportional to the number of other active groups
- PM Agent coordination obligations (state sync, HORIZON sweeps, entry approvals, exit confirmations) compound across groups
- Cross-group dependency chains (M17: G1 calibration → G2 wiring → G5 display) become harder to sequence correctly as the dependency graph grows

At seven groups, the coordination overhead exceeded what the existing process could manage, producing the NM-067 failure set. At some lower count — likely three to four parallel groups — the overhead is manageable without a coordination lane at all. The sprint planning SOP does not define that threshold.

### What caught it

EL pattern recognition during NM-067 investigation. No planning gate surfaced the coordination risk before M17 implementation began.

### Root cause

The sprint planning SOP defines entry criteria for individual sprint groups (entry document, EL approval, etc.) but has no wave-level coordination check. There is no question at wave planning time that asks: "how many groups are in this wave, which files do they share, and what is the coordination protocol if that count exceeds a manageable threshold?" The threshold itself is undefined.

### Process improvement

**Immediate:** GitHub Issue #1333 filed.

**Required at M18 kickoff:**
1. Sprint planning SOP (`docs/process/sprint-planning-sop.md`) amended to include a **wave-level coordination check** at wave kickoff: list all groups planned for the wave, identify shared files (especially `SESSION_STATE.md`, registry files, `CLAUDE.md`), and determine the coordination protocol based on group count:
   - **1–2 groups:** standard model — each group writes shared files in its own PRs; conflicts are recoverable at merge time
   - **3–4 groups:** PM Agent coordination lane recommended — shared-file updates queued through PM Agent; groups flag shared-file changes in their exit PRs rather than writing directly
   - **5+ groups:** PM Agent coordination lane required — sprint group sub-branches mandatory (per NM-067 fix); no direct shared-file writes from feature branches
2. The wave kickoff coordination check is a PM Agent responsibility, recorded in the wave kickoff artifact before any group opens an implementation PR.
3. A hard ceiling of five parallel groups per wave is recommended as a starting point, subject to EL revision after M18 experience.

**Near-miss lineage:** NM-071 is the upstream planning gap that enabled NM-067. Closing NM-067 (branching model) without closing NM-071 (concurrency ceiling) would allow a future wave to recreate the same conditions that made NM-067 inevitable.

---

## NM-072 — Artifact 5 (Scope Decision Gate) Authored and EL-Approved Before Prerequisite Design Artifacts Existed; Cascaded into Stale Delta Analysis and Incomplete Taxonomy (Reactive)

**Date:** 2026-06-27
**Milestone:** M18 — Full Argument and Demo 7
**Detected by:** EL observation during GD design package review — EL noted divergence between Artifact 4 (maximalist discriminated union schema, all types) and Artifact 5 (six-type taxonomy, single-parameter ShockInjectRequest), and asked how they diverged so much at inception
**Severity:** High — produced incorrect artifacts in the repository: Artifact 4 Dimensions 3 and 4 were drafted against an information hierarchy that had not yet been corrected, and Artifact 5's EL scope decisions were made without access to the full CE Agent analysis in Artifact 4; the GrowthShock type was absent from panel deliberation as a result

### What happened

The GD design package specifies a seven-artifact sequence: Artifacts 1→2→3→4 inform Artifact 5 (EL scope gate) → Artifact 6 (ADR-019) → Artifact 7 (UX update). Artifact 5 is the EL scope gate — the decisions it records gate ADR-019 authorship and G4 sprint entry.

Artifact 5 was authored and EL-approved in a prior session **before Artifacts 2, 3, and 4 existed**. The sprint entry document specified the correct sequence, but no gate enforced it. The Artifact 5 author used a six-type shock taxonomy derived from ADR-008 (the only available input) without the benefit of: (a) Artifact 2's maximalist platform target for the control plane zone, (b) Artifact 3's Customer Agent Layer 3 finding that GrowthShock is ESSENTIAL for Demo 7 Step 4, or (c) Artifact 4's CE Agent discriminated union architecture analysis.

Consequences:
1. **GrowthShock omission from panel deliberation.** The panel deliberated the six types from ADR-008. GrowthShock was not considered and rejected — it was absent from the input. Decision 2 ("all six in M18") was made without the seventh type on the table.
2. **Artifact 4 Dimension 4 drafted against stale Artifact 5.** The Artifact 4 author read Artifact 5 before authoring Dimension 4 and produced `ScenarioConfigColumn.tsx` — an editable configuration surface — because the stale Artifact 5 framing implied Mode 2 column 3 would have editable sliders. The correct Artifact 2 target (read-only summary + "Enter Active Control" button, named `Mode2ColumnSurface`) had not yet been written.
3. **Artifact 4 Dimension 3 had a shallow ShockInjectRequest.** The CE Agent's discriminated union analysis in Dimension 3 used a single `magnitude: float | None` parameter because the panel had not yet deliberated on per-type parameter schemas. The correct schema names per-type parameters for all seven types.
4. **Information hierarchy temporarily documented M18 scope instead of platform target.** Before the course correction, `information-hierarchy.md §Control Plane Reserved Zone` described the six-type shock taxonomy as the complete set, effectively encoding M18 scope into the platform governing document.
5. **Thin-slicing concern.** The EL independently identified that Artifact 5's design appeared to be architectural minimalism rather than incremental delivery of a maximalist target — this would have led to re-architecture cost when deferred types were eventually added.

### What was at risk

ADR-019 was the next step. If the course correction had not been made before ADR-019 authorship began, the ADR-019 author would have received: contradictory inputs from Artifacts 4 and 5, a missing GrowthShock type, an incorrect Mode2ColumnSurface specification (editable sliders vs. read-only summary), and a shallow ShockInjectRequest schema. The resulting ADR-019 would have encoded the errors into the accepted architectural record, from which G4 sprint entry and implementation would follow. Discovering the errors during G4 implementation (the next failure point) would have required ADR-019 amendment, G4 sprint entry amendment, and partial implementation rework.

### What caught it

EL pattern recognition. The EL observed the Artifact 4 / Artifact 5 divergence and asked how they had diverged so much at inception. Investigation revealed the sequence inversion. No process gate surfaced the ordering problem before Artifact 5 was approved.

### Root cause

The GD gate was **unidirectional**: Artifact 5 gates ADR-019 (downstream). The gate was not **upstream**: no check prevented Artifact 5 from being filed and approved before its prerequisite artifacts existed. The sprint entry SOP correctly specified the artifact sequence, but specification without enforcement is not a gate.

### Process improvement

**Immediate:** Four-document course correction executed before ADR-019 authorship:
1. `docs/process/near-miss-registry.md`: NM-072 filed (this entry)
2. `docs/ux/information-hierarchy.md §Control Plane Reserved Zone`: Restored to maximalist platform target; Mode 2 column architecture ruling reframed as platform ruling (not M18 scope compromise); GrowthShock added as seventh type; shock taxonomy no longer encodes milestone scope
3. `docs/architecture/control-plane-column-delta-analysis-m18.md §Dimension 3 and §Dimension 4`: Dimension 3 corrected to full discriminated union schema with per-type parameters for all seven types; Dimension 4 corrected to `Mode2ColumnSurface.tsx` (read-only summary + "Enter Active Control", no editable sliders); EL Decision 6 (all 7 handlers in G4) recorded
4. `docs/process/intents/M18-GD-2026-06-26-control-plane-scope-decision.md §Artifact 5`: Framing note added; Decision 4 (GrowthShock) approved; Decision 5 (4 MVP types, superseded) filed; Decision 6 (all 7 handlers, forcing function for architectural completeness) filed

**Structural fix required (sprint planning SOP):** Future pre-wave design packages that include an EL scope gate artifact must specify both:
- **Downstream gate:** EL scope gate artifact → ADR authorship (already exists)
- **Upstream gate:** Prerequisite design artifacts must be filed and on record before EL scope gate artifact may be submitted for EL review

The upstream gate must be an explicit check in the sprint planning SOP, not guidance. An EL scope decision made without the full design analysis input is not independent review — it is approval of an incomplete specification. PI Agent holds R for verifying the upstream gate condition is satisfied before routing an Artifact 5 equivalent for EL review in any future pre-wave design package.

---

## NM-073 — Sprint Sub-Branches Have No Required CI Checks; Auto-Merge Fires Before Playwright E2E Completes (Reactive)

**Date:** 2026-06-27
**Milestone:** M18 — Full Argument and Demo 7
**Detected by:** DS Agent investigation — EL observed PR #1395 merged while `playwright-e2e` was still pending
**Severity:** Low — integration PR gate (sprint→release) still enforces full CI before any code reaches `release/m18`; no incorrect artifacts produced

### What happened

PR #1395 (`feat/m18-g3-test-authorship` → `sprint/m18-g3`) merged at `2026-06-27T01:49:55Z` while the `playwright-e2e` CI check was still in `pending` state. The EL flagged the premature merge; DS Agent investigation confirmed the root cause: `sprint/m18-g3` has no branch protection (GitHub branch protection API returns 404 for sprint branches) and is not covered by the `release-branch-ci-gate` Ruleset.

The Ruleset condition is `refs/heads/release/m*` — it applies exclusively to `release/m18`, `release/m17`, etc. Sprint sub-branches (`sprint/m18-g1`, `sprint/m18-g2`, `sprint/m18-g3`) are not included. Auto-merge on an unprotected branch fires when GitHub's internal merge eligibility conditions are satisfied (no conflicts; no status checks required). Since no status check was required on the sprint branch, `playwright-e2e` being pending did not block the merge.

The sprint group isolation model was introduced at M18 kickoff to resolve NM-067. When the branching model was designed, no corresponding CI gate was specified for sprint sub-branches.

### What was at risk

An implementation PR could merge to a sprint sub-branch with failing `playwright-e2e` tests — broken frontend behavior landing on the sprint branch before CI completes. Other implementing agents pulling from the sprint branch for subsequent work could build on top of that broken state. The defect would only be caught at the integration PR gate (`sprint/m18-g3` → `release/m18`) where the `release-branch-ci-gate` Ruleset enforces all required checks.

In this specific instance (PR #1395 is a test authorship PR), `playwright-e2e` failure was expected — tests are pre-RED before implementation. The risk is higher for implementation PRs where a failing `playwright-e2e` indicates genuine defects.

### What caught it

EL observation after seeing the merge notification, triggering DS Agent investigation. No process gate on the sprint branch detected or blocked the premature merge.

### Root cause

The sprint group isolation SOP (NM-067 resolution) introduced sprint sub-branches but did not define CI requirements for those branches. The `release-branch-ci-gate` Ruleset was not extended to cover `sprint/m*` branches. The design intent — whether sprint branches should have required checks or whether the gate lives only at the integration PR — was never explicitly decided or documented.

### Process improvement

**Design decision required (EL) — choose one path:**

**Option A — Add sprint-branch CI gate:**
DS Agent creates a new GitHub Ruleset (`sprint-branch-ci-gate`) covering `refs/heads/sprint/m*` with required checks: `changes`, `lint`, `test-backend`, `playwright-e2e`. Feature→sprint auto-merge then waits for all required checks to pass. `docs/process/sprint-group-isolation.md` updated to document the gate. Implemented via `infra/m18-sprint-branch-gate` PR targeting `release/m18`.

**Option B — Explicitly document sprint branches as intentionally unprotected:**
DS Agent updates `docs/process/sprint-group-isolation.md` to explicitly state that sprint sub-branches are intermediate integration points with no required CI gate; the full gate lives at the integration PR (sprint→release). Auto-merge fires without waiting for CI on sprint branches by design — implementing agents rely on local pre-push gates (ruff + mypy + npm build) for intermediate quality. Implemented via `infra/m18-sprint-group-isolation-doc-amendment` PR targeting `release/m18`.

**Not acceptable:** leaving the design decision undocumented. The sprint group isolation SOP must explicitly state CI gate expectations for sprint branches, whichever path is chosen.

DS Agent brings this finding to the EL for path selection before implementing.

---

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
