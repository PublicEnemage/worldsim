---
name: process-redesign-phaseD-exit
type: sprint-exit
phase: Phase D — Session Boundary Discipline
status: Filed — awaiting EL endorsement
authored-by: PM Agent (orchestration + enforceability review); PI Agent (CLAUDE.md amendment)
date: 2026-06-12
sprint-entry: docs/process/sprint-plans/process-redesign-phaseD-sprint-entry.md
phaseC-exit: docs/process/sprint-plans/process-redesign-phaseC-exit.md
---

# Phase D Exit Artifact — Session Boundary Discipline

**Status:** Filed — awaiting EL endorsement
**Date produced:** 2026-06-12
**PM Agent enforceability review:** Below (Part III)
**EL endorsement:** Pending (Part VII)

---

## Part I — Primary Outputs Delivered

All primary output artifacts are filed at their canonical locations per
`docs/process/sprint-plans/process-redesign-phaseD-sprint-entry.md §Output Artifact Canonical Locations`.

| Output | Status | Canonical location | Authored by |
|---|---|---|---|
| CLAUDE.md §Session Continuity amendment — §Entry and Exit Invariants | ✅ Filed | `CLAUDE.md §Session Continuity — §Entry and Exit Invariants` | PI Agent |
| PM Agent enforceability review | ✅ Filed | This document, Part III | PM Agent |
| Phase D exit artifact (this document) | ✅ Filed | `docs/process/sprint-plans/process-redesign-phaseD-exit.md` | PM Agent |

---

## Part II — What Phase D Delivered and Why It Matters

Phases A through C defined the execution lifecycle, the Business PO acceptance protocol,
and the sprint boundary templates. Each of those artifacts lives in `docs/process/` or
`docs/process/agents.md` — documents that agents read as part of their role-specific
mandatory reading, but that are not in the primary reading sequence that every agent
executes at session start.

Phase D closes the final gap: the sprint entry and exit invariants now appear in CLAUDE.md
§Session Continuity — the permanent constitution that every agent reads at the start of
every session, before any role-specific documents. An agent reading only CLAUDE.md at
session start now encounters the sprint entry gate ("implementation may not begin without
a filed, EL-approved entry document") and the sprint exit gate ("a sprint does not close
when issues are closed and CI is green") with the same architectural weight as the PR merge
gate and the pre-push lint gate. These were previously only accessible by reading the SOP.

**The three structural commitments encoded:**

1. **Sprint entry invariant as a hard stop.** The amendment uses the same enforcement
   language as existing gates: "may not authorize," "hard stop," "process deviation of the
   same severity as." This is not coincidental — it is the deliberation document's explicit
   requirement (§Phase D: "the language must create an obligation"). An agent that opens an
   implementation PR without a filed entry document cannot claim it was unaware the gate
   existed.

2. **Sprint exit invariant as a named set of conditions.** The four exit conditions are
   stated explicitly and include the consequence: "A sprint that closes with outstanding
   rejections or missing Business PO verdicts has not exited — it has been abandoned without
   a record." This names the failure mode, not only the success condition.

3. **"If it isn't written down, it doesn't exist."** This principle operationalizes the
   entry and exit invariants. It prevents the gates from being satisfied by session memory,
   verbal acknowledgment, or informally completed work. The artifact location is the proof —
   not the agent's knowledge that the work was done.

---

## Part III — PM Agent Enforceability Review

*PM Agent produces this review independently. Engineering Lead reads this review as part of
the endorsement decision. The review addresses one question: does the CLAUDE.md amendment
create genuine obligations in a single-principal governance context, or do the constraints
remain circular?*

**Finding 1 — The language creates obligations, not advisories.**

The amendment uses "may not," "hard stop," "blocks sprint exit confirmation," and "process
deviation." These are the same constructions used in the PR merge gate ("Claude Code must
stop all git operations") and the pre-push lint gate ("mandatory before any git push").
An agent reading this section encounters a named prohibition with a named consequence — not
a recommendation that it would be good to do. The deliberation document's test for whether
language creates an obligation rather than guidance is satisfied.

**Finding 2 — The single-principal circularity is real but bounded.**

The circularity: in a single-principal governance structure, the Engineering Lead who
approves the sprint entry document is the same person who could bypass the gate entirely.
This means the gate is ultimately a self-constraint, not an enforced external constraint.
Phase D does not solve this — it cannot solve it within the current governance structure.

What Phase D does: it makes the self-constraint explicit and architectural. An EL who
bypasses the entry gate must now bypass a named gate in CLAUDE.md, not simply skip a step
in a SOP that most agents read only during role activation. The bypass is visible. It
creates an audit record gap — the near-miss obligation fires regardless of whether the EL
authorized the deviation. CLAUDE.md §Governance documents this limitation and the
progression plan (Stage 2: second governance account as alternative approver). Phase D
does not add to the governance gap; it adds to the visibility of any bypass.

**Finding 3 — The PI Agent near-miss obligation is unconditional under the amendment.**

The amendment states the PI Agent obligation without qualification: "If implementation
begins without a complete entry document, the PI Agent files a near-miss in the same
session — not after the sprint closes — regardless of whether implementation ultimately
succeeds." This mirrors the Phase C finding: a sprint that succeeded despite missing the
entry gate is not a counterpoint to the obligation. The near-miss obligation is what makes
the gate visible after the fact even when the gate was bypassed without incident. This is
the blameless continuous improvement principle (CLAUDE.md §Blameless Continuous Improvement)
applied to sprint boundary discipline.

**Finding 4 — "If it isn't written down" closes the session memory loophole.**

In previous sessions (pre-Phase D), an implementing agent could satisfy themselves that an
entry condition was met without filing the artifact — because CLAUDE.md contained no
language about artifacts as the unit of gate satisfaction. The amendment closes this by
naming artifact locations as the proof, not knowledge or confidence. An agent that knows
the intent document was authored but cannot cite the path
`docs/process/intents/ADR-NNN-YYYY-MM-DD-short-name.md` cannot claim the entry gate is
satisfied.

**Finding 5 — One limitation acknowledged.**

The amendment refers to the sprint exit document but does not name the path of that
document within the constitutional text (it references the template and the SOP). This is
correct — the path includes a per-sprint variable (`{milestone-slug}-sprint-{N}-exit.md`)
that cannot be stated as a constant in CLAUDE.md. The consequence is that an agent reading
only CLAUDE.md knows a document must exist but must read the SOP to know where. This is
the same pattern as the PR merge gate ("report the PR URL and explicitly hand off") — the
gate names the obligation, the SOP specifies the mechanics. The limitation is acceptable.

**PM Agent verdict:** The CLAUDE.md amendment creates genuine obligations in the
single-principal governance context. The language is architectural, not aspirational. The
circularity is real and bounded — it is a governance gap, not a drafting gap. The
amendment is ready for EL endorsement. The process redesign sequence (Phases 0, A, B, C,
D) is complete pending EL endorsement of this document.

---

## Part IV — Exit Gate Checklist

Per `docs/process/sprint-plans/process-redesign-phaseD-sprint-entry.md §Exit Gate`:

| # | Condition | Status |
|---|---|---|
| 1 | CLAUDE.md §Session Continuity amendment filed with architectural enforcement language | ✅ Confirmed — `CLAUDE.md §Session Continuity — §Entry and Exit Invariants` |
| 2 | PM Agent enforceability review complete and on record | ✅ Confirmed — Part III above |
| 3 | EL endorses Phase D outputs | Pending — Part VII |
| 4 | SESSION_STATE.md updated to mark process redesign sequence complete | Pending — will update after PR merges |
| 5 | Any deferred items explicitly listed with rationale | ✅ See Part V |

**Gate status: 3 of 5 conditions confirmed. Conditions 3 and 4 pending EL endorsement and SESSION_STATE update.**

---

## Part V — North Star Validation Question

Per CLAUDE.md §North Star Test (Process Gate):

*"If a new Claude Code session opens for M13 implementation — does the CLAUDE.md §Entry and
Exit Invariants amendment ensure that the political economy module sprint begins with proper
preconditions and closes with proper validation for the Zambian finance ministry scenario?"*

**Answer: Yes, in a concrete and traceable way.**

The Zambian finance ministry scenario (the ministry preparing for a restructuring session,
the agent building the political economy conditionality module) now has a named gate at
session start. An M13-implementing agent reading CLAUDE.md encounters the sprint entry
invariant before any implementation begins — not as a process obligation discovered mid-
sprint, but as a constitutional requirement visible at the first session. The consequence is:
the conditionality module cannot advance to an implementation PR without an intent document
filed and EL-approved entry gate passed. This is the pre-condition chain that would have
caught the Demo 4 failure (DEMO4-001, DEMO4-002) at sprint entry rather than at live demo.

The exit side: a Zambian ministry analyst using the conditionality module output to argue
about fiscal path alternatives needs the output to tell them what the number means (Layer 3).
The exit invariant now blocks sprint closure until the Customer Agent Layer 3 assessment is
on record — not until the Business PO decides to run it. The gate fires regardless.

**Validation verdict:** Phase D outputs are sufficient to confirm mission alignment. The
amendment makes the mission-serving gates architectural commitments — visible to every agent
at every session start — rather than process obligations discoverable only through role-
specific document reading.

---

## Part VI — Known Limitations

| Limitation | Mitigation in place | Forward path |
|---|---|---|
| Single-principal circularity: EL approves their own sprint entry | Gate is architectural — bypass creates a named audit gap + PI Agent near-miss fires | CLAUDE.md §Governance Stage 2: second governance account as alternative approver |
| CLAUDE.md amendment references exit document path via SOP rather than directly | Agent must read SOP for path mechanics; obligation is visible in CLAUDE.md | Acceptable — same pattern as PR merge gate; no change required |
| Process redesign phases (0–D) predate Phase C templates; sprint entry/exit templates not retroactively required | Phase exit documents are the equivalent artifact for these phases; template pattern applies from M13 forward | No retroactive requirement — Phase 0–D grandfathered (per Phase C Known Limitations) |

---

## Part VII — Process Redesign Sequence Closure Summary

The process redesign sequence (Phases 0, A, B, C, D) is the implementation of the four
mechanisms identified in the deliberation document (`docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md`).

| Phase | Mechanism | Gap closed | Status |
|---|---|---|---|
| Phase 0 | UX/persona → ADR traceability | XD-1, XD-2, FD-1 | ✅ Complete — EL endorsed 2026-06-11 |
| Phase A | Agent execution lifecycle | Execution lifecycle gap, FD-2, FD-3 | ✅ Complete — EL endorsed 2026-06-12 |
| Phase B | Business PO acceptance protocol | Acceptance protocol gap, DEMO4 class prevention | ✅ Complete — EL endorsed 2026-06-12 |
| Phase C | Sprint cadence formalization | Sprint boundary artifact gap | ✅ Complete — EL endorsed 2026-06-12 |
| Phase D | Session boundary discipline | CLAUDE.md constitutional gap | Pending EL endorsement |

When EL endorses this document, all four mechanisms are operational and architecturally
committed. The process redesign sequence is formally closed.

---

## Part VIII — EL Endorsement Space

The Engineering Lead reviews this exit artifact and all primary outputs listed in Part I.
Endorsement constitutes approval that:
1. The CLAUDE.md §Session Continuity — §Entry and Exit Invariants amendment is accepted
2. The PM Agent enforceability review in Part III is accepted
3. The known limitations in Part VI are acceptable for this phase
4. The process redesign sequence (Phases 0, A, B, C, D) is formally closed
5. SESSION_STATE.md may be updated to mark the sequence complete

**EL endorsement:**

> {To be filled at endorsement time}
> — @PublicEnemage ({date})

---

*This artifact is the canonical exit record for Phase D and for the Process Redesign Sequence.
It must not be modified after EL endorsement except to add the endorsement itself and update
SESSION_STATE.md. Phase D is the terminal phase — there is no Phase E.*
