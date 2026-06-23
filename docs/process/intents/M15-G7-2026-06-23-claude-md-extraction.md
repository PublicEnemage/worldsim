---
name: M15-G7-claude-md-extraction
type: implementation-intent
issues: "#1091"
status: Filed
authored-by: Architect Agent
authored-date: 2026-06-23
implementing-agents: "Architect Agent (#1091 extraction)"
sprint-entry: "docs/process/sprint-plans/m15-g7-sprint-entry.md — EL approval pending"
adr-reference: "None — documentation reorganisation; no new architecture, no new surface, no new behaviour"
release-branch: release/m15
---

# Implementation Intent: M15-G7 — CLAUDE.md Extraction to Child Documents

> **Documentation sprint note:** The M15 sprint plan explicitly exempts G7 §1091 from requiring
> a sprint entry document (and by extension a formal intent document) because this is a
> documentation-only reorganisation — no code, no new architecture, no user-facing behaviour.
> This intent document is authored voluntarily for lifecycle consistency: the QA test authorship
> gate requires a canonical specification, and the lifecycle is stronger with it. The sprint
> entry's Section 3.1 is the authoritative source for all ACs below; this document reorganises
> that specification into the lifecycle-canonical intent format.

---

## 1. Source Reference

**Sprint entry:** `docs/process/sprint-plans/m15-g7-sprint-entry.md` — EL approval pending
**ADR gate:** None — documentation reorganisation; no new architecture required
**Date authored:** 2026-06-23
**Authored by:** Architect Agent
**Implementing agent:** Architect Agent

**Issue in scope:**

| Issue | Title | Implementing agent |
|---|---|---|
| #1091 | docs(claude-md): extract Lifecycle, Exit SOP, and DIC sections to child docs | Architect Agent |

**EL-action items (no implementing agent can act):**

| Issue | Required action | Dependency |
|---|---|---|
| #3 | Second GitHub account with merge authority (Stage 2 governance) | EL only |
| #6 | Branch protection restoration | EL only; depends on #3 |

---

## 2. Persona Trace Elements Targeted

> *G7 has no governing ADR. This is a documentation reorganisation serving internal users
> (Claude Code agents and the Engineering Lead) rather than end-user personas. Trace is
> forward to the navigability and session-start reliability that downstream Tier 1 deliverables
> depend on.*

**Personas served (indirect):** All agents operating in this codebase. The primary
navigability benefit serves the next implementing agent who opens a session: they must find
the Agent Execution Lifecycle and Milestone Exit SOP within the first 60 seconds of session
initialisation by following links from CLAUDE.md.

**P-2 — Entry state:** Session start — an agent has just read SESSION_STATE.md and is now
reading CLAUDE.md as the second required document. The 25% line-count reduction (1,082 → ≤ 800)
reduces mandatory-reading time and makes the three extracted sections linkable rather than
inlined.

**P-7 — Forward capability delivered:**
Any implementing agent or EL can navigate from CLAUDE.md to the complete Agent Execution
Lifecycle or Milestone Exit SOP in one click (≤ 60 seconds, cold session), rather than
scrolling ~400 lines of CLAUDE.md. The extracted documents remain complete transplants —
no information is lost.

---

## 3. Observable Application State

> *All observable states are file-system observable: confirmable by an external reviewer
> running `ls`, `grep`, or `wc -l` against the repository — without reading any implementation
> plan or implementation code.*

### 3.1 Primary observable state

`docs/process/agent-execution-lifecycle.md` exists and contains all five lifecycle step
headings (Step 1–5), the Rejection Artifact Requirements section, the Layer 3 Quality Gate
section, the Kryptonite Design Constraint section, and the Observable Application State
definition section — confirmed by `grep` against the file.

`docs/process/milestone-exit-sop.md` exists and contains all four exit ceremony step
headings (Step 1–4) and the three named retrospective questions — confirmed by `grep` against
the file.

### 3.2 Secondary observable states

**CLAUDE.md line count:** `wc -l CLAUDE.md` returns ≤ 800. Current count is 1,082 — the
two primary extractions (~200 lines for lifecycle, ~65 lines for exit ceremony) plus any DIC
deduplication must reduce the total by ≥ 282 lines.

**CLAUDE.md retains links:** `grep -c "agent-execution-lifecycle.md" CLAUDE.md` returns ≥ 1
and `grep -c "milestone-exit-sop.md" CLAUDE.md` returns ≥ 1 — summary sentences and `see`
links are present in the positions of the extracted blocks.

**Cross-references updated:** `grep -rn "CLAUDE.md §Agent Execution Lifecycle" docs/` returns
0 results and `grep -rn "CLAUDE.md §Milestone Exit\|CLAUDE.md §Milestone Retrospective" docs/`
returns 0 results — all 91 cross-references updated to point to child documents.

### 3.3 Silent failure detection

Silent failure mode: CLAUDE.md line count falls below 800 because content was deleted rather
than transplanted. Distinguishing characteristic: the child document `docs/process/agent-execution-lifecycle.md`
must contain all five step headings AND the three subsections (Rejection Artifact, Layer 3
Quality Gate, Kryptonite Design Constraint). A file that exists but is abbreviated — e.g.,
contains only step headings without subsection content — is a silent failure. The QA check
for AC-2 through AC-6 combined (5 distinct grep assertions) detects this.

Second silent failure mode: cross-references updated in CLAUDE.md but not in `docs/` subdirectories.
AC-13 and AC-14 (`grep -rn` returning 0) detect this.

---

## 4. Acceptance Criteria

> *All criteria are grep- or filesystem-verifiable by an external reviewer with no knowledge
> of the implementation. Test file: `backend/tests/test_m15_g7_claude_md_extraction.py`.*

**AC-1:** When the extraction PR is merged, `docs/process/agent-execution-lifecycle.md`
exists as a file in the repository.
*Test method: `os.path.exists("docs/process/agent-execution-lifecycle.md")` returns True.*

**AC-2:** `docs/process/agent-execution-lifecycle.md` contains all five lifecycle step
headings in sequence.
*Test method: `grep -c "Step [1-5] —" docs/process/agent-execution-lifecycle.md` returns 5.*

**AC-3:** `docs/process/agent-execution-lifecycle.md` contains the Rejection Artifact
Requirements section.
*Test method: `grep -c "Rejection artifact requirements" docs/process/agent-execution-lifecycle.md`
returns ≥ 1.*

**AC-4:** `docs/process/agent-execution-lifecycle.md` contains the Layer 3 Quality Gate
section.
*Test method: `grep -c "Layer 3 Quality Gate" docs/process/agent-execution-lifecycle.md`
returns ≥ 1.*

**AC-5:** `docs/process/agent-execution-lifecycle.md` contains the Kryptonite Design
Constraint section.
*Test method: `grep -c "Kryptonite Design Constraint" docs/process/agent-execution-lifecycle.md`
returns ≥ 1.*

**AC-6:** `docs/process/agent-execution-lifecycle.md` contains the Observable Application
State definition section.
*Test method: `grep -c "Observable Application State" docs/process/agent-execution-lifecycle.md`
returns ≥ 1.*

**AC-7:** When the extraction PR is merged, `docs/process/milestone-exit-sop.md` exists
as a file in the repository.
*Test method: `os.path.exists("docs/process/milestone-exit-sop.md")` returns True.*

**AC-8:** `docs/process/milestone-exit-sop.md` contains all four exit ceremony step headings.
*Test method: `grep -c "Step [1-4] —" docs/process/milestone-exit-sop.md` returns 4.*

**AC-9:** `docs/process/milestone-exit-sop.md` contains all three named retrospective
questions.
*Test method: `grep -c "What defects evaded\|What process gaps\|What testing improvements"
docs/process/milestone-exit-sop.md` returns 3.*

**AC-10:** `wc -l CLAUDE.md` returns ≤ 800 lines after the extraction.
*Test method: integer line count from `subprocess.run(["wc", "-l", "CLAUDE.md"])` ≤ 800.*

**AC-11:** CLAUDE.md retains a link to `docs/process/agent-execution-lifecycle.md` in the
position of the extracted lifecycle section.
*Test method: `grep -c "agent-execution-lifecycle.md" CLAUDE.md` returns ≥ 1.*

**AC-12:** CLAUDE.md retains a link to `docs/process/milestone-exit-sop.md` in the position
of the extracted exit ceremony section.
*Test method: `grep -c "milestone-exit-sop.md" CLAUDE.md` returns ≥ 1.*

**AC-13:** No file in `docs/` contains the string `CLAUDE.md §Agent Execution Lifecycle`
(all such cross-references updated to point to `docs/process/agent-execution-lifecycle.md`).
*Test method: `subprocess.run(["grep", "-rn", "CLAUDE.md §Agent Execution Lifecycle", "docs/"])` stdout is empty.*

**AC-14:** No file in `docs/` contains `CLAUDE.md §Milestone Exit Ceremony` or
`CLAUDE.md §Milestone Retrospective Process` (all such cross-references updated to point
to `docs/process/milestone-exit-sop.md`).
*Test method: `subprocess.run(["grep", "-rn", "CLAUDE.md §Milestone Exit\\|CLAUDE.md §Milestone Retrospective", "docs/"])` stdout is empty.*

---

## 4b. Visual Spec (before/after)

N/A — no UI changes. All deliverables are file creation and text substitution in markdown
documents. No `data-testid`, viewport, or zone specification applies.

---

## 5. Kryptonite Constraint Check

> *Authority: CLAUDE.md §Agent Execution Lifecycle — Kryptonite Design Constraint (FD-3).
> Applies to implementations that introduce or modify a user-facing analytical output.*

**Does this implementation's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` **Not applicable — documentation reorganisation with no user-facing output.**
G7 produces two child markdown documents and reduces CLAUDE.md line count. There is no
user-facing analytical output, no indicator label, no alert text, and no output narrative.
The kryptonite constraint is a gate for user-facing capability deliverables. This intent
is process/infrastructure documentation.

*Forward trace:* The navigability improvement (CLAUDE.md ≤ 800 lines; process gates linkable)
reduces session-start friction for implementing agents, which indirectly improves the
speed and accuracy of user-facing Tier 1 deliverables that those agents produce. No direct
Persona 2 / 3 / 5 output is introduced.

---

## 6. Out of Scope

**Content changes to extracted sections:** #1091 is extraction only — verbatim (or
near-verbatim with section-local reference corrections) transplant. Any substantive process
change to the Agent Execution Lifecycle rules or Milestone Exit Ceremony steps requires its
own issue and its own process.

**Modifications to non-extracted CLAUDE.md sections:** `§Guiding Principles`, `§Architectural
Principles for Claude Code Sessions`, `§Governance`, `§UX Architectural Commitments`, and
all other non-extracted sections are unchanged.

**DIC full extraction:** The Domain Intelligence Council activation table (nine agents,
`Speaks for`, `Activation` columns) is retained in CLAUDE.md. Only the prose description
and operational agent definitions — already canonical in `docs/process/agents.md` — are
reduced. This is deduplication and does not require a separate AC; the DIC line contribution
(~25 lines) is not needed to reach ≤ 800 if the two primary extractions succeed.

**G8 scope (#843):** Live stakeholder demo — separate sprint entry; M15 exit gate.

**#845 Phase 4:** Zone 1A implementation — separate sprint entry; may extend to M16.

**EL-action items (#3, #6):** Cannot be implemented by any agent; EL-only GitHub
organisation and repository settings actions.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any extraction PR is opened against `release/m15`
**Test file location:** `backend/tests/test_m15_g7_claude_md_extraction.py`
**Acceptance criteria covered:** AC-1 through AC-14

**Implementation sequence (canonical — from sprint entry §Section 4):**
1. EL approves sprint entry document
2. QA Lead authors `backend/tests/test_m15_g7_claude_md_extraction.py` from AC-1–AC-14 above — tests must be runnable (as failing) before extraction begins
3. Architect Agent runs mandatory cross-reference audit: `grep -rn "CLAUDE.md §Agent Execution Lifecycle\|CLAUDE.md §Milestone Exit\|CLAUDE.md §Retrospective" docs/` and records affected files
4. Architect Agent creates `docs/process/agent-execution-lifecycle.md` (verbatim transplant)
5. Architect Agent creates `docs/process/milestone-exit-sop.md` (verbatim transplant)
6. Architect Agent updates CLAUDE.md — replaces each extracted block with two-sentence summary + `see <child-doc-path>` link; confirms `wc -l CLAUDE.md` ≤ 800
7. Architect Agent updates all cross-reference files from step 3; confirms AC-13 and AC-14 pass
8. DIC deduplication: confirms DIC prose is already in `docs/process/agents.md`; reduces CLAUDE.md §DIC to activation table + one summary sentence if confirmed
9. PR opens targeting `release/m15` with branch name `docs/m15-g7-claude-md-extraction`
10. Step 4 Verify: Architect Agent confirms AC-1–AC-14 pass; child docs are complete transplants (not truncated); CLAUDE.md line count ≤ 800
11. Step 5 Validate: Business PO reads CLAUDE.md cold from session start and locates all process gates via links in ≤ 60 seconds; confirms no information was lost by spot-reading child docs against original CLAUDE.md sections

**QA Lead acknowledgment:**
`[ ]` QA Lead: Tests for AC-1 through AC-14 authored and filed before extraction PR opens. [Date]

---

## 8. Step 4 Verify Record

> *To be completed by implementing agent after PR is opened and before marking PR ready for review.*

**Verify date:** —
**Verifier:** —
**AC results:** —
**Child document completeness check:** —
**CLAUDE.md line count post-extraction:** —
**Cross-reference scan (AC-13):** —
**Cross-reference scan (AC-14):** —
**Step 4 verdict:** —

---

## 9. Step 5 Validate Record

> *To be completed by Business PO after PR is merged to release/m15 and the repository is in its post-extraction state.*

**Validate date:** —
**Validator (Business PO):** —
**Cold-read navigability test:** —
**Information loss check:** —
**Layer 3 assessment:** N/A — process documentation; Customer Agent Layer 3 gate does not apply
**North star:** N/A — process infrastructure (Tier 3); no direct finance minister scenario served
**Kryptonite:** N/A — no user-facing output
**Step 5 verdict:** —

---

*Intent document authority: `docs/process/intent-template.md` (version 2026-06-17).
Sprint entry: `docs/process/sprint-plans/m15-g7-sprint-entry.md`.
Sprint plan exception recorded: G7 §1091 is exempted from sprint entry and intent document
requirements per `docs/process/sprint-plans/m15-sprint-plan.md §Sprint Entry Gate Requirements`.
This document is authored voluntarily to close the QA test authorship gate cleanly.*
