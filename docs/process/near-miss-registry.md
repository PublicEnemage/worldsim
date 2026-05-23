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
