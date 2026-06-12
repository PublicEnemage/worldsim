---
name: process-redesign-phaseC-exit
type: sprint-exit
phase: Phase C — Sprint Cadence Formalization
status: Filed — awaiting EL endorsement
authored-by: PM Agent (orchestration); PI Agent (enforcement review)
date: 2026-06-12
sprint-entry: docs/process/sprint-plans/process-redesign-phaseC-sprint-entry.md
phaseB-exit: docs/process/sprint-plans/process-redesign-phaseB-exit.md
---

# Phase C Exit Artifact — Sprint Cadence Formalization

**Status:** Filed — awaiting EL endorsement
**Date produced:** 2026-06-12
**PI Agent enforcement review:** Below (Part III)
**EL endorsement:** Pending (Part VII)

---

## Part I — Primary Outputs Delivered

All primary output artifacts are filed at their canonical locations per
`docs/process/sprint-plans/process-redesign-phaseC-sprint-entry.md §Output Artifact Canonical Locations`.

| Output | Status | Canonical location | Authored by |
|---|---|---|---|
| Sprint entry template | ✅ Filed | `docs/process/sprint-plans/templates/sprint-entry-template.md` | PM Agent |
| Sprint exit template | ✅ Filed | `docs/process/sprint-plans/templates/sprint-exit-template.md` | PM Agent |
| PM Agent role amendment — sprint boundary obligations | ✅ Filed | `docs/process/agents.md §PM Agent — Sprint Boundary Obligations` | PM Agent |
| PI Agent role amendment — sprint boundary enforcement | ✅ Filed | `docs/process/agents.md §Process Integrity Agent — Sprint Boundary Enforcement` | PI Agent |
| Sprint Entry Gate — SOP amendment | ✅ Filed | `docs/process/sprint-planning-sop.md §Sprint Entry Gate` | PM Agent |
| Sprint Exit Artifact reference updated in SOP | ✅ Filed | `docs/process/sprint-planning-sop.md §Sprint Exit Gate — Sprint Exit Artifact` | PM Agent |
| Phase C exit artifact (this document) | ✅ Filed | `docs/process/sprint-plans/process-redesign-phaseC-exit.md` | PM Agent |
| Phase D sprint entry | ✅ Filed | `docs/process/sprint-plans/process-redesign-phaseD-sprint-entry.md` | PM Agent |

---

## Part II — What Phase C Delivered and Why It Matters

Phase C was tasked with encoding the sprint boundary — when the lifecycle steps run relative
to sprint entry and exit, and what must exist at each boundary. The core gap: Phase B defined
the sprint exit gate conditions, but neither the entry side nor the exit side had a filed
artifact template that made the conditions explicit and checkable sprint-over-sprint without
re-reading the SOP.

**What Phase C produces:**

**Sprint entry template** (`docs/process/sprint-plans/templates/sprint-entry-template.md`):
A structured document that the PM Agent files at every sprint kickoff to confirm the sprint is
properly bounded before implementation begins. Five entry invariants (release branch + CI
trigger, ADR gates, intent documents, QA test authorship) are now checkboxes — binary, not
judgments. A sprint that opens without this document filed and EL-approved is identifiable as
a process deviation, not an oversight. The template is what makes the entry gate self-executing
rather than SOP-dependent.

**Sprint exit template** (`docs/process/sprint-plans/templates/sprint-exit-template.md`):
A structured document that the PM Agent files at every sprint close. It surfaces the Phase B
exit gate conditions (Business PO ACCEPT verdicts, Customer Agent Layer 3 assessments, open
rejections) as a per-deliverable table that PI Agent can review and confirm without reading
the acceptance protocol on each execution. The PI Agent confirmation section (Section 5) is
the named gate — not a checklist comment on an issue.

**Three structural decisions embedded in the templates:**

1. **The entry document is filed and EL-approved before implementation PRs open — not after.**
   This is the mirror image of the PR merge gate: just as implementation cannot continue after
   an open PR without EL confirmation of merge, implementation cannot begin without EL approval
   of the sprint entry. The obligation is the same; the direction is reversed.

2. **"Infrastructure sprint" is a declaration subject to PI Agent review at exit, not a
   self-executing exemption.** The template requires an explicit declaration in Section 2 when
   a sprint's deliverables are infrastructure. If a declared-infrastructure deliverable produces
   user-visible output, the exemption did not apply and PI Agent files a near-miss. This prevents
   the infrastructure label from becoming a mechanism for bypassing entry gates.

3. **The sprint exit document supersedes the issue comment as the exit artifact.** Phase B's
   SOP §Sprint Exit Gate named exit conditions but left the artifact as a milestone issue
   comment — which is difficult to cross-reference, version, or audit. Phase C shifts the
   artifact to a filed document that the PI Agent can review against the sprint entry document
   and the acceptance protocol. The issue comment references the filed document rather than
   replacing it.

---

## Part III — PI Agent Enforcement Review

*PI Agent produces this review independently. Engineering Lead reads this review as part of the
endorsement decision.*

**Finding 1 — Entry template makes the entry gate self-executing.**

The five entry invariants in the sprint entry template are binary checkboxes: either the
release branch exists or it does not; either the CI trigger is verified or it is not; either
the intent document is filed or it is not. There is no "mostly satisfied" or "effectively done."
A PM Agent who cannot check all five invariants cannot open the sprint — the unchecked
invariant is visible and named. This is a structural improvement over the pre-Phase C state,
where entry conditions were described in the SOP but had no artifact form that made them
verifiable at a glance.

**Finding 2 — PI Agent near-miss obligation is unconditional.**

The PI Agent role amendment makes the near-miss obligation unconditional: if a sprint begins
implementation without a complete entry document, PI Agent files a near-miss in the same
session — regardless of whether implementation ultimately succeeds. This mirrors the near-miss
principle from CLAUDE.md §Blameless Continuous Improvement: near-misses are filed whether or
not harm resulted. A sprint that succeeded despite missing the entry gate is not a counterpoint
to the obligation — it is evidence that the gate almost failed rather than evidence that the
gate is not needed.

**Finding 3 — Exit template closes the Phase B artifact gap.**

Phase B defined exit conditions; Phase C gives those conditions a home. The per-deliverable
Business PO acceptance table in Section 3 of the exit template makes it immediately visible
whether any deliverable lacks a verdict. The Customer Agent Layer 3 sequencing check
(Section 3 — "filed before verdict?") closes the Phase B obligation that the assessment
precede the verdict rather than follow it. These were implicit in the Phase B protocol;
they are now explicit checkboxes.

**Finding 4 — Infrastructure sprint exception is bounded, not open-ended.**

The "infrastructure sprint" exemption in both the SOP and the exit template is bounded by PI
Agent review at exit. A PM Agent who incorrectly labels a user-facing deliverable as
infrastructure cannot rely on the label to pass the exit gate — PI Agent reviews the
declaration against actual deliverable output. This mirrors how the "no significant feature
without an ADR" rule works: it is not self-certifying; it requires a named agent to confirm.

**Finding 5 — One limitation acknowledged.**

The entry gate requires EL approval of the entry document before implementation PRs open.
In a single-principal governance structure, this creates a dependency: if the EL is unavailable
and the PM Agent has already filed the entry document, implementation must wait. This is
correct behavior — the gate is not designed to be bypassed when it is inconvenient. The
limitation is that the EL's availability gates the sprint entry. No process improvement can
eliminate this in a single-principal context; it is a documented governance limitation (see
CLAUDE.md §Governance).

**PI Agent verdict:** Enforcement language is adequate for Phase C exit. The entry and exit
templates are self-executing — binary, not advisory. The PI Agent near-miss obligation is
unconditional. The infrastructure sprint exemption is bounded. The Phase B artifact gap is
closed. Phase C may close and Phase D may open.

---

## Part IV — Exit Gate Checklist

Per `docs/process/sprint-plans/process-redesign-phaseC-sprint-entry.md §Exit Gate`:

| # | Condition | Status |
|---|---|---|
| 1 | Sprint entry and exit templates filed at canonical locations | ✅ Confirmed — `docs/process/sprint-plans/templates/` |
| 2 | PM Agent and PI Agent role amendments filed in agents.md | ✅ Confirmed — §PM Agent — Sprint Boundary Obligations; §PI Agent — Sprint Boundary Enforcement |
| 3 | Sprint Entry Gate section added to sprint-planning-sop.md | ✅ Confirmed — §Sprint Entry Gate |
| 4 | PI Agent confirms enforcement language is adequate (obligation, not aspiration) | ✅ Confirmed — Part III Findings 1–4 |
| 5 | EL endorses Phase C outputs | Pending — Part VII |
| 6 | Phase D sprint entry document is filed | ✅ Confirmed — `docs/process/sprint-plans/process-redesign-phaseD-sprint-entry.md` |
| 7 | SESSION_STATE.md updated | Pending — will update after PR merges |
| 8 | Any deferred items explicitly listed with rationale | ✅ See Part V |

**Gate status: 6 of 8 conditions confirmed. Conditions 5 and 7 pending EL endorsement and SESSION_STATE update.**

---

## Part V — North Star Validation Question

Per CLAUDE.md §North Star Test (Process Gate):

*"If the Zambian finance ministry analyst is using WorldSim to prepare for a restructuring
session and the implementing agent is building the political economy module — does the Phase C
sprint cadence formalization ensure the module is properly bounded before implementation and
properly validated before the sprint closes?"*

**Answer: Yes, in two specific ways.**

First: the sprint entry template requires the implementing agent to file an intent document and
the QA Lead to author tests from it before implementation begins. The Zambian ministry analyst
scenario depends on the political economy module's conditionality constraint output being
analytically correct and interpretable — the test authorship gate at entry is what makes
"analytically correct" verifiable rather than asserted. Without it, the module ships when the
implementor believes it is done; with it, the module ships when the QA Lead's pre-authored
tests pass.

Second: the sprint exit template requires a Business PO ACCEPT verdict for the module output,
with a Customer Agent Layer 3 assessment as a precondition. The Layer 3 gate is what ensures
the conditionality constraint output tells the Zambian analyst what the number means — not
only displays it. Phase C gives that gate a document home where it is confirmed sprint-over-sprint
rather than improvised in each session.

**Validation verdict:** Phase C outputs are sufficient to confirm mission alignment at both the
entry and exit sides of the sprint boundary for M13 deliverables.

---

## Part VI — Known Limitations

| Limitation | Mitigation in place | Forward path |
|---|---|---|
| EL availability gates sprint entry in single-principal governance | EL approval is a standing obligation; in practice, the EL initiates sessions and the entry document is filed in the same session as sprint planning — the dependency is rarely blocking | CLAUDE.md §Governance Stage 2: second governance account would give an alternative approver |
| The entry template's QA test authorship gate requires QA Lead availability in the sprint-opening session | The gate creates an explicit obligation — QA Lead authorship before implementation, not after. If QA Lead is unavailable, implementation is held rather than the gate bypassed | Phase D may address session boundary discipline for agent availability; until then, the gate is the mitigation |
| Process redesign sprints (Phase 0–D) have used phase exit documents rather than sprint entry/exit templates — this is not retroactively required | Phase exit documents for Phase 0–D are the equivalent of sprint exit templates for process redesign work; the template pattern applies from M13 forward | No retroactive requirement — Phase 0–D are grandfathered |

---

## Part VII — EL Endorsement Space

The Engineering Lead reviews this exit artifact and all primary outputs listed in Part I.
Endorsement constitutes approval that:
1. The sprint entry template is adequate as a sprint entry gate artifact
2. The sprint exit template is adequate as a sprint exit gate artifact
3. The PM Agent and PI Agent role amendments in `docs/process/agents.md` are accepted
4. The Sprint Entry Gate section in `docs/process/sprint-planning-sop.md` is accepted
5. The PI enforcement review in Part III is accepted
6. The known limitations in Part VI are acceptable for this phase
7. Phase D may open using `docs/process/sprint-plans/process-redesign-phaseD-sprint-entry.md`

**EL endorsement:**

> {To be filled at endorsement time}
> — @PublicEnemage ({date})

---

*This artifact is the canonical exit record for Phase C. It must not be modified after EL
endorsement except to add the endorsement itself and update SESSION_STATE.md.*
