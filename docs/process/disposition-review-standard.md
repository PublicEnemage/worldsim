# Disposition Review Standard

**Established:** 2026-05-11
**Applies to:** All STD-REVIEW and ARCH-REVIEW gap dispositions
**Reference case:** STD-REVIEW-004, 2026-05-11

---

## The Principle

Agent consultation on standards and architecture gaps must be generative,
not confirmatory. Agents are activated before dispositions are drafted,
not after. An agent asked to review a disposition already made is being
asked to find holes in a framed decision. An agent asked to reason from
the gap description alone will surface different concerns — including
concerns the original analysis missed.

---

## The Protocol

**Step 1 — Identify gaps requiring disposition.**
When a STD-REVIEW or ARCH-REVIEW produces gaps requiring Engineering Lead
disposition, do not draft dispositions yet. Proceed to Step 2.

**Step 2 — Activate domain agents independently.**
Activate the relevant domain agents in fresh sessions before any
disposition is drafted.

For STD-REVIEW gaps: activate Data Architect, QA Lead, and Architect.
For ARCH-REVIEW gaps: activate Architect, Chief Methodologist, and the
domain-relevant council member (e.g., Development Economist for fiscal
policy gaps, Ecological Economist for planetary boundary gaps).

**Step 3 — Brief each agent identically and independently.**
Each agent receives only:
- The gap inventory document (the full STD-REVIEW or ARCH-REVIEW file)
- The three standard questions (below)

No draft dispositions. No framing of the expected answer. No shared
context between agents.

**The three standard questions:**
1. For each gap, what is your primary concern and what resolution would
   you recommend? Do not assume any resolution direction — reason from
   the gap description alone.
2. Which gap poses the highest risk if left unresolved, and why?
3. Are there any dependencies between gaps that the gap descriptions do
   not make explicit? If two gaps must be resolved in a specific order,
   identify the ordering constraint and the reason.

**Step 4 — Synthesize agent responses.**
After all agents complete, produce a synthesis identifying:
- Cross-cutting concerns raised by two or more agents independently
- Direct disagreements between agents requiring Engineering Lead decision
- Findings not present in the gap description

**Step 5 — Record Engineering Lead dispositions.**
Engineering Lead reviews the synthesis and records dispositions. The
disposition record must note:
- Which agent findings were incorporated
- Which agent findings were overridden, with rationale
- How direct agent disagreements were resolved
- The single-principal governance limitation acknowledgment and
  the compensating control applied

---

## Severity Thresholds for Activation

**Immediate gaps:** Full three-agent panel required before any disposition
is recorded. No exceptions.

**Near-term gaps:** Minimum one domain-relevant agent (Data Architect for
data standards gaps, Architect for architectural gaps, QA Lead for
testing and enforcement gaps). Full panel recommended if multiple
near-term gaps are interdependent.

**Horizon:long-term gaps:** Panel activation not required before
disposition. Engineering Lead may record dispositions directly with a
note that long-term horizon reduces the urgency of independent review.

---

## What This Process Is Not

**Not a rubber-stamp process.** If agents disagree with each other or
with a draft, those disagreements surface for Engineering Lead decision.
They are not resolved by averaging or by deferring to the most senior
agent. Direct agent conflicts are the most valuable output of the panel —
they identify dependencies, circular constraints, and framing assumptions
that the gap descriptions did not make explicit.

**Not a substitute for independent human review.** The three-agent panel
is the compensating control for single-principal governance, not a
replacement for independent human review. The documented plan to address
the single-principal limitation remains in force per CLAUDE.md §Governance.

**Not optional for Immediate gaps.** An Engineering Lead who records
dispositions on Immediate-severity gaps without activating the panel
is in breach of this standard. The disposition record must reference
the panel synthesis document.

---

## Disposition Record Requirements

Every disposition record in a STD-REVIEW or ARCH-REVIEW document must
include:

| Field | Required content |
|---|---|
| Date | Date dispositions recorded |
| Panel activation | Agents activated, questions asked, no-draft-shared confirmation |
| Panel synthesis reference | Path or inline content of synthesis |
| Key findings incorporated | Numbered list of agent findings that changed the disposition |
| EL decisions on conflicts | How direct agent disagreements were resolved |
| Single-principal disclosure | Verbatim per CLAUDE.md §Governance |
| Gap-by-gap table | Severity, amendment target, disposition, notes |

---

## Reference Case: STD-REVIEW-004 (2026-05-11)

The three-agent panel (Data Architect, QA Lead, Architect) on
STD-REVIEW-004 produced ten substantive improvements to the draft
dispositions, including:

- A hard ordering dependency not in the gap descriptions (Gap 1 → Gap 2:
  canonical vocabulary must exist before field mappings can reference it)
- A factual error in the gap description (runner.py duplicate event_id
  warning was missing the [SIM-INTEGRITY] prefix — the gap description
  treated it as compliant)
- A missing schema field in the proposed source_field_registry structure
  (transformation_test_id — paper certification without a verification
  test is not sufficient)
- A mechanical coupling between two gaps at the same function
  (_compute_composite_score() dispatch architecture must accommodate both
  ecological and governance normalization before either is implemented)
- A genuine circular dependency between two gaps requiring joint
  same-commit resolution rather than sequential ordering (Gaps 2 and 3)

The process also surfaced the standing process failure it was designed
to prevent: dispositions had been drafted before agents were consulted,
and the Engineering Lead course-corrected mid-session. The ten
improvements are the evidence that generative consultation produces
better outcomes than confirmatory review.

---

## Process History

| Date | Applied to | Outcome |
|---|---|---|
| 2026-05-11 | STD-REVIEW-004 — M7 exit standards gaps | 10 substantive improvements to draft dispositions; runner.py code fix caught; circular dependency identified |
