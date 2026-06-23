---
name: m15-g7-sprint-entry
type: sprint-entry
milestone: M15 — Human Cost Architecture
sprint-group: G7
status: Filed — awaiting EL approval before extraction begins
authored-by: PM Agent
authored-date: 2026-06-23
el-approved: false
release-branch: release/m15
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M15, G7: Process Documentation

**Status:** Filed — awaiting EL approval before extraction begins
**Date authored:** 2026-06-23
**Release branch:** `release/m15`
**Sprint plan:** `docs/process/sprint-plans/m15-sprint-plan.md` (EL Approved 2026-06-20; amended 2026-06-21)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G7. G7 is a parallel documentation-only track — no sequential dependency on
G1–G6. G7 does not gate G8; G8 (#843, live external demo) is the M15 exit gate and has been
unblocked since G5 closed (2026-06-22).*

*Sprint plan exception noted: `docs/process/sprint-plans/m15-sprint-plan.md §Sprint Entry Gate
Requirements` explicitly exempts `G7 §1091 component (process documentation — no code, only
document edits)` from requiring a sprint entry document. This entry is filed voluntarily for
process consistency — the observable states below give the implementing agent the same
pre-implementation specification that intent documents provide for code deliverables.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M15 — Human Cost Architecture |
| GitHub Milestone | #16 |
| Sprint group | G7 — Process Documentation |
| Release branch | `release/m15` |
| Sprint plan document | `docs/process/sprint-plans/m15-sprint-plan.md` |
| Exit checklist issue | #984 |
| Sprint groups in scope | G7 only |
| ADR gate | None — all G7 items are process/documentation changes; no new surface requires an ADR |
| Implementing agent | Architect Agent (#1091 extraction) |
| EL-action items | #3 (single-principal separation of duties), #6 (branch protection restoration) — no implementing agent can act; EL actions only |
| Wave | Parallel (no sequential dependency on G1–G6; does not gate G8) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any G7 extraction PR is opened.
An unchecked invariant blocks the extraction from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m15` cut from `main` 2026-06-20 (commit 500e50d)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed 2026-06-20 (line 5: `branches: [ main, develop, release/m* ]`;
  line 7: `branches: [ main, release/m* ]`). Ruleset ID 17751852 with 6 required checks:
  `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
  KI-005 permanent fix (`do_not_enforce_on_create: true`) applied 2026-06-20.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m15-sprint-plan.md`
  `el-approved: 2026-06-20`

### 2.2 — ADR prerequisite gate

G7 contains no items requiring a new ADR. The extraction (#1091) relocates existing content
without introducing new architecture, new surface, or new behavior. The governance items
(#3, #6) are EL-level actions on GitHub and infrastructure settings — not implementation
decisions requiring an ADR.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G7 — #1091 (CLAUDE.md extraction) | None — documentation reorganisation; no new architecture | N/A | **CLEAR** |
| G7 — #3 (separation of duties) | None — EL governance action | N/A | **EL-ACTION ONLY** |
| G7 — #6 (branch protection) | None — EL infrastructure action | N/A | **EL-ACTION ONLY** |

- [x] All G7 ADR prerequisites are clear. No new ADR required. Gate: **CLEAR**.

### 2.3 — Intent document gate

*G7 is a documentation-only sprint. The sprint plan exempts G7 §1091 from the sprint entry
requirement; by extension, the formal intent document gate is also not required. The
observable states in Section 3.1 of this entry document serve as the pre-implementation
specification — they are specific enough for the implementing agent to begin extraction and
for a reviewer to confirm completion without reading any implementation plan.*

*For the EL-action items (#3, #6): no implementation intent is applicable — these require
EL decisions on GitHub organization settings and branch protection rulesets, not agent
implementation work.*

- [x] **Documentation sprint — intent document not required** per sprint plan exception.
  Observable states in Section 3.1 serve as the implementation specification.

| Deliverable | ADR reference | Observable state specification | Coverage |
|---|---|---|---|
| #1091 — CLAUDE.md extraction to child docs | None | Section 3.1 of this entry document | **Covered — see Section 3.1** |
| #3 — separation of duties (EL-action) | None | N/A — EL action only | **N/A** |
| #6 — branch protection restoration (EL-action) | None | N/A — EL action only | **N/A** |

### 2.4 — QA test authorship gate

*G7 uses document-level observable states (file existence and content-presence checks) rather
than Playwright or API tests. A single pytest file provides grep-based assertions against
the acceptance criteria in Section 3.1.*

*Test file must be authored from Section 3.1's acceptance criteria before the extraction PR
opens — not after.*

- [ ] QA test file authored before extraction PR opens — **MUST FILE BEFORE EXTRACTION PR OPENS**

| Deliverable | Specification source | Test file path | Authored before extraction? |
|---|---|---|---|
| #1091 — all acceptance criteria | Section 3.1 of this entry document | `backend/tests/test_m15_g7_claude_md_extraction.py` | No — **BLOCKING** |

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

#### #1091 — CLAUDE.md extraction to child docs

**Primary deliverable.** CLAUDE.md is 1,082 lines as of 2026-06-23. The issue targets a
~25% reduction by extracting three long procedure sections to canonical child documents,
retaining summary sentences and `see <file>` links in CLAUDE.md.

**Three extraction targets:**

| Section | Current location | Target child document | Approximate lines extracted |
|---|---|---|---|
| Agent Execution Lifecycle | `CLAUDE.md §Agent Execution Lifecycle` (Steps 1–5, rejection artifact, Layer 3 Quality Gate, Kryptonite Design Constraint, Observable Application State definition, lifecycle canonical document table, self-attestation limitation) | `docs/process/agent-execution-lifecycle.md` | ~200 |
| Milestone Exit Ceremony + Retrospective Process | `CLAUDE.md §Milestone Exit Ceremony` + `CLAUDE.md §Milestone Retrospective Process` | `docs/process/milestone-exit-sop.md` | ~65 |
| Domain Intelligence Council | `CLAUDE.md §Domain Intelligence Council` (detailed table + description) | Already canonical in `docs/process/agents.md` — deduplication only; DIC activation table stays in CLAUDE.md; prose description moves to `docs/process/agents.md` or is confirmed already present | ~25 |

**Mandatory pre-extraction step — cross-reference audit:**

Run `grep -rn "CLAUDE.md §Agent Execution Lifecycle\|CLAUDE.md §Milestone Exit\|CLAUDE.md §Retrospective"
docs/` before extracting. Every reference found must be updated in the same PR to point to
the child document rather than CLAUDE.md. As of 2026-06-23, ~35 files contain `CLAUDE.md §`
references; the subset pointing specifically to the three extracted sections must be confirmed
and updated. A reference that breaks silently (404 anchor) without a redirect is a compliance
violation — the canonical artifact location must be resolvable.

**Acceptance criteria (observable states):**

| AC | Observable state | Test method |
|---|---|---|
| AC-1 | `docs/process/agent-execution-lifecycle.md` exists | `test: os.path.exists("docs/process/agent-execution-lifecycle.md")` |
| AC-2 | `docs/process/agent-execution-lifecycle.md` contains all five lifecycle step headings: "Step 1 — Intent authorship", "Step 2 — Test authorship", "Step 3 — Implementation", "Step 4 — Verify", "Step 5 — Validate" | `grep -c "Step [1-5] —" docs/process/agent-execution-lifecycle.md` returns 5 |
| AC-3 | `docs/process/agent-execution-lifecycle.md` contains the rejection artifact section ("Rejection artifact requirements") | `grep -c "Rejection artifact requirements" docs/process/agent-execution-lifecycle.md` returns ≥1 |
| AC-4 | `docs/process/agent-execution-lifecycle.md` contains the Layer 3 Quality Gate section | `grep -c "Layer 3 Quality Gate" docs/process/agent-execution-lifecycle.md` returns ≥1 |
| AC-5 | `docs/process/agent-execution-lifecycle.md` contains the Kryptonite Design Constraint section | `grep -c "Kryptonite Design Constraint" docs/process/agent-execution-lifecycle.md` returns ≥1 |
| AC-6 | `docs/process/agent-execution-lifecycle.md` contains the Observable Application State definition section | `grep -c "Observable Application State" docs/process/agent-execution-lifecycle.md` returns ≥1 |
| AC-7 | `docs/process/milestone-exit-sop.md` exists | `test: os.path.exists("docs/process/milestone-exit-sop.md")` |
| AC-8 | `docs/process/milestone-exit-sop.md` contains all four exit ceremony step headings: "Step 1 — Open issue audit", "Step 2 — Milestone reference audit", "Step 3 — SESSION_STATE internal consistency check", "Step 4 — Fresh session continuity test" | `grep -c "Step [1-4] —" docs/process/milestone-exit-sop.md` returns 4 |
| AC-9 | `docs/process/milestone-exit-sop.md` contains the retrospective process section (three named questions) | `grep -c "What defects evaded\|What process gaps\|What testing improvements" docs/process/milestone-exit-sop.md` returns 3 |
| AC-10 | `wc -l CLAUDE.md` returns ≤ 800 | `subprocess.run(["wc", "-l", "CLAUDE.md"])` output integer ≤ 800 |
| AC-11 | CLAUDE.md retains a summary sentence and a `see docs/process/agent-execution-lifecycle.md` link in the position of the extracted lifecycle section | `grep -c "agent-execution-lifecycle.md" CLAUDE.md` returns ≥1 |
| AC-12 | CLAUDE.md retains a summary sentence and a `see docs/process/milestone-exit-sop.md` link in the position of the extracted exit ceremony section | `grep -c "milestone-exit-sop.md" CLAUDE.md` returns ≥1 |
| AC-13 | No cross-reference in `docs/` points to `CLAUDE.md §Agent Execution Lifecycle` (all such references updated to point to `docs/process/agent-execution-lifecycle.md`) | `grep -rn "CLAUDE.md §Agent Execution Lifecycle" docs/` returns 0 results |
| AC-14 | No cross-reference in `docs/` points to `CLAUDE.md §Milestone Exit Ceremony` or `CLAUDE.md §Milestone Retrospective Process` (all such references updated to point to `docs/process/milestone-exit-sop.md`) | `grep -rn "CLAUDE.md §Milestone Exit\|CLAUDE.md §Milestone Retrospective" docs/` returns 0 results |

**Completeness requirement:** The child documents must be complete transplants — not summaries.
Every sentence, every table, every bullet point from the extracted sections must appear verbatim
(or near-verbatim with section-local reference corrections) in the child documents. A
child document that abbreviates or omits content from the extracted section fails AC-2 through
AC-9 implicitly. The QA Lead must verify completeness by reading the child document against
the current CLAUDE.md section before marking ACs as passing.

**DIC handling note:** The Domain Intelligence Council section is a deduplication target, not
a full extraction. The activation table (nine agents, their `Speaks for` and `Activation`
columns) is retained in CLAUDE.md. The prose description and operational agent definitions
are already canonical in `docs/process/agents.md`. If the prose in CLAUDE.md §Domain
Intelligence Council is already present in `docs/process/agents.md`, it may be reduced to
a summary sentence + table in CLAUDE.md without a separate AC — deduplication is
judgment-guided, not test-gated, because the DIC line-count contribution (~25 lines) is
not needed to reach the ≤ 800-line target if the two primary extractions succeed.

---

#### #3 — Governance: Resolve single-principal separation of duties gap (EL-action)

No implementing agent can act on this issue. The required governance progression is defined
in `CLAUDE.md §Governance §Intended Governance Progression — Stage 2`: a second GitHub
account with merge and exception-approval authority for engine core, docs, and `.github`.
This requires EL action at the GitHub organization level. G7 records this issue as an
open EL-action item; it does not constitute a blocking condition on G7 close.

**EL-action required:** Provision a second GitHub account with merge authority for the
Stage 2 governance trigger condition. Record action in the G7 sprint exit document.

---

#### #6 — Governance: Branch protection restoration (EL-action)

No implementing agent can act on this issue. Branch protection bypass capability is a
GitHub organization / repository settings action requiring EL access. The trigger condition
per `CLAUDE.md §Governance` is Stage 2 governance completion — a second governance account
in place. G7 records this issue as an open EL-action item dependent on #3.

**EL-action required:** After #3 Stage 2 governance is complete, restore branch protection
bypass restriction in repository settings. Record action in the G7 sprint exit document.

---

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| All G1–G6 completed deliverables | Complete; merged to `release/m15` |
| #843 (live stakeholder demo) | G8 scope — M15 exit gate; unblocked since G5 close |
| #845 Phase 4 (Zone 1A implementation) | Out of G7 scope; separate sprint entry required; may extend to M16 |
| Any modifications to process gate logic or SOP rules | #1091 is extraction only — no content changes to the extracted sections; any process change requires its own issue and process |
| Modifying `CLAUDE.md §Guiding Principles`, `§Architectural Principles`, or other non-extracted sections | Outside #1091 scope; CLAUDE.md constitution content is unchanged |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G7 — #1091 (extraction) | None | N/A | **Yes — after EL approves this entry document and QA test gate is satisfied** |
| G7 — #3 (EL-action) | None | N/A | **EL-action only — no agent implementation** |
| G7 — #6 (EL-action) | None | N/A | **EL-action only; dependent on #3** |

**Implementation sequencing for G7 — #1091:**

1. EL approves this entry document
2. QA Lead authors `backend/tests/test_m15_g7_claude_md_extraction.py` from Section 3.1
   acceptance criteria (AC-1–AC-14) — authored before any extraction begins; tests may not
   pass yet (the child docs do not exist) but must be runnable as failing tests
3. Architect Agent runs the mandatory cross-reference audit:
   `grep -rn "CLAUDE.md §Agent Execution Lifecycle\|CLAUDE.md §Milestone Exit\|CLAUDE.md §Retrospective" docs/`
   and records the full list of affected files in the PR description
4. Architect Agent creates `docs/process/agent-execution-lifecycle.md` (verbatim transplant
   of §Agent Execution Lifecycle through §Observable Application State definition)
5. Architect Agent creates `docs/process/milestone-exit-sop.md` (verbatim transplant of
   §Milestone Exit Ceremony through §Milestone Retrospective Process)
6. Architect Agent updates CLAUDE.md: replaces each extracted block with a two-sentence
   summary + `see <child-doc-path>` link; confirms `wc -l CLAUDE.md` ≤ 800
7. Architect Agent updates all ~35 cross-reference files identified in step 3; no
   `CLAUDE.md §Agent Execution Lifecycle` or `CLAUDE.md §Milestone Exit` references remain
8. DIC deduplication: Architect Agent confirms DIC prose in CLAUDE.md is already present
   in `docs/process/agents.md`; if so, reduces CLAUDE.md §Domain Intelligence Council to
   the activation table + one summary sentence
9. PR opens targeting `release/m15`; `branch-naming` check requires `m15` prefix —
   use `docs/m15-g7-claude-md-extraction`
10. Step 4 Verify: Architect Agent confirms AC-1–AC-14 pass in the PR environment; child
    docs are complete (not truncated); CLAUDE.md line count ≤ 800
11. Step 5 Validate: Business PO reads CLAUDE.md cold — session start to all process gates
    located in ≤ 60 seconds via links (analogous to the documentation validation protocol
    in `docs/process/acceptance-protocol.md`); confirms no information was lost by reading
    child docs against the original CLAUDE.md sections

**G7 does not gate G8.** G8 sprint entry may open concurrently or after G7 — EL may approve
G7 and G8 entries in the same session if preferred.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-23
**Sweep period:** Since M15-G6 sprint entry filed (2026-06-22) through G7 sprint entry
authorship (2026-06-23)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| NM-056 — E2E test soft-skip masked AC-4 mock bug (`null ?? 2` in `makeTrajectoryMock`) for 8 sprints; root cause: backend startup failure before PR #1123 made tests silently soft-skip. Fixed PR #1130. Filed in same session as G6 exit. | Near-miss (reactive; pre-existing) | Yes — NM-056 filed 2026-06-23 | NM-056 |

No additional process gaps identified in the sweep period. G6 accessibility validation
(PR #1128, #1131) and mid-milestone main sync (PR #1133, #1134) produced no new deviations.

---

## EL Approval Record

**EL approval:** Pending

> {EL approval statement — to be filled at approval time}
> — @PublicEnemage ({date})
