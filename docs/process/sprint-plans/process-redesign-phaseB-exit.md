---
name: process-redesign-phaseB-exit
type: sprint-exit
phase: Phase B — Business PO Acceptance Protocol
status: ENDORSED — EL endorsement recorded 2026-06-12
authored-by: PM Agent (orchestration); PI Agent (exit gate confirmation + enforcement review)
date: 2026-06-12
sprint-entry: docs/process/sprint-plans/process-redesign-phaseB-sprint-entry.md
phaseA-exit: docs/process/sprint-plans/process-redesign-phaseA-exit.md
---

# Phase B Exit Artifact — Business PO Acceptance Protocol

**Status:** ENDORSED
**Date produced:** 2026-06-12
**PI Agent enforcement review:** Below (Part III)
**EL endorsement:** 2026-06-12 — see Part VII

---

## Part I — Primary Outputs Delivered

All primary output artifacts are filed at their canonical locations per
`docs/process/sprint-plans/process-redesign-phaseB-sprint-entry.md §Output Artifact Canonical Locations`.

| Output | Status | Canonical location | Authored by |
|---|---|---|---|
| Per-work-type verification criteria — frontend (Step 1) | ✅ Filed | `docs/process/acceptance-protocol.md §Part 1 §1.1` | Business PO |
| Per-work-type verification criteria — backend (Step 1) | ✅ Filed | `docs/process/acceptance-protocol.md §Part 1 §1.2` | Business PO |
| Per-work-type verification criteria — documentation (Step 1) | ✅ Filed | `docs/process/acceptance-protocol.md §Part 1 §1.3` | Business PO |
| Per-work-type verification criteria — analytics (Step 1) | ✅ Filed | `docs/process/acceptance-protocol.md §Part 1 §1.4` | Business PO |
| Exception path specification — rejection triggers (Step 2) | ✅ Filed | `docs/process/acceptance-protocol.md §Part 2 §2.1` | PI Agent |
| Exception path specification — rejection artifact requirements (Step 2) | ✅ Filed | `docs/process/acceptance-protocol.md §Part 2 §2.2` | PI Agent |
| Exception path specification — re-acceptance process (Step 2) | ✅ Filed | `docs/process/acceptance-protocol.md §Part 2 §2.3` | PI Agent |
| Exception path specification — EL exception path (Step 2) | ✅ Filed | `docs/process/acceptance-protocol.md §Part 2 §2.4` | PI Agent |
| PI enforcement review within acceptance-protocol.md (Step 2) | ✅ Filed | `docs/process/acceptance-protocol.md §Part 2 §2.5` | PI Agent |
| ACCEPT mode in agents.md §Business Product Owner Agent | ✅ Filed | `docs/process/agents.md §Business Product Owner Agent — Activation prompt reference` | Business PO |
| Sprint Exit Gate in sprint-planning-sop.md | ✅ Filed | `docs/process/sprint-planning-sop.md §Sprint Exit Gate` | PM Agent |
| PI enforcement review (this document Part III) | ✅ Below | `docs/process/sprint-plans/process-redesign-phaseB-exit.md §Part III` | PI Agent |
| Phase B exit artifact (this document) | ✅ Filed | `docs/process/sprint-plans/process-redesign-phaseB-exit.md` | PM Agent |
| Phase C sprint entry (Step 3) | ✅ Filed | `docs/process/sprint-plans/process-redesign-phaseC-sprint-entry.md` | PM Agent |

---

## Part II — What Phase B Delivered and Why It Matters

Phase B was tasked with making the Validate step (Step 5 of the Agent Execution Lifecycle)
repeatable rather than improvised. The core gap: Phase A defined the execution lifecycle
including the Validate step, but left the Business PO with four under-specified questions:

1. What does the Business PO actually do for a frontend feature Validate step?
2. What constitutes evidence of analytical intent satisfied for a backend capability?
3. What is the standard for "navigability in under five minutes" for documentation?
4. What does "names the specific argument" mean for analytics?

Phase B answers all four with concrete, per-type verification protocols. The protocols are
repeatable because each uses a binary passing checklist rather than a quality judgment. A
checklist item is either true or false; it does not vary by Business PO preference or by session.

**Three structural decisions embedded in the protocol:**

1. **The checklist is the gate, not the relationship.** When the Business PO and implementing
   agent have aligned views, the protocol is fast. When they diverge, the protocol is what
   makes the disagreement visible and resolvable rather than suppressed. This is the protocol's
   primary value — it performs best when relationships are under pressure.

2. **The Customer Agent Layer 3 assessment is a precondition, not a follow-up.** For Persona 2/3/5
   capabilities, the Business PO requests the Layer 3 assessment before executing the Validate
   step. This sequencing prevents the pattern of validating then discovering the output requires
   specialist mediation — a pattern that forces re-validation or acceptance of a known weakness.

3. **The DEMO4 class check is explicit in the backend protocol.** The frozen-value silent failure
   (DEMO4-001/002) is now a named, mandatory check at the Validate step. It is not implicit in
   "confirm the field is non-null." The check explicitly requires that the value at step N differs
   from the value at step 0 for any dynamic-state output.

---

## Part III — PI Agent Enforcement Review

*PI Agent produces this review independently. Engineering Lead reads this review as part of the
endorsement decision.*

**Finding 1 — Enforcement language is obligation, not aspiration.**

The passing checklists in Part 1 use language that creates an observable obligation:
- "The Business PO must answer YES to all of the following" — not "should generally confirm"
- "The exception path has a mandatory near-miss entry" — not "consider filing a near-miss"
- "A verdict delivered without the Layer 3 assessment for a Persona 2/3/5 capability is a
  process violation" — not "the Layer 3 assessment is recommended"

The sprint exit gate in sprint-planning-sop.md uses the same enforcement pattern as the
pre-push lint gate and PR merge gate already in CLAUDE.md: it names who enforces (PI Agent
holds R for sprint exit confirmation), what blocks exit (open rejections, absent Customer Agent
assessments), and the consequence of proceeding without it (process violation, not advisory).

**Finding 2 — The rejection artifact has teeth.**

Per the Phase B sprint entry §Secondary Output and the PI Agent's deliberation Finding 3
requirement ("a rejected sprint must produce a written rejection artifact ... before any work in
the next sprint group begins"), the rejection protocol satisfies:

- The rejection blocks sprint exit until resolved ✅ (§2.3 sprint exit block)
- The rejection requires a near-miss entry in the same session ✅ (§2.2 near-miss requirement)
- The rejection artifact is at a canonical location with a sequential number ✅ (§2.2 location)
- The implementing agent returns to Step 1 (intent authorship), not Step 3 (implementation) ✅ (§2.3 return-to-Step-1)
- The re-acceptance condition is named specifically in the rejection artifact ✅ (§2.2 re-acceptance condition)

The EL exception path preserves the Business PO's finding as permanent institutional record
while giving the EL an explicit override mechanism. This matches the deliberation's requirement:
the sprint may proceed, but the finding does not evaporate and the forward trace is mandatory.

**Finding 3 — The DEMO4 class check is institutionally embedded.**

The frozen-value silent failure pattern (DEMO4-001: reserves frozen at 7.1 months) now has a
named mandatory check at the Validate step for backend capabilities (§1.2, checklist item 2:
"DEMO4 class check: the field value at step N differs from the value at step 0"). This pattern
was previously implicit in "the feature is working" — it is now explicit in the passing checklist.
A future implementing agent cannot pass the Validate step with a frozen output by claiming CI is
green. The check is observable and binary.

**Finding 4 — The asymmetry test closes the gap between "technical correctness" and "mission alignment."**

The backend capability and analytics protocols both include an asymmetry test: can the ministry
team with three economists use this argument at the table, or does it require specialist mediation
the creditor side has and the ministry side lacks? This test operationalizes the Kryptonite
Design Constraint (FD-3) at the Validate step for these work types. A technically correct
analytical capability that requires a PhD to interpret and cite fails the asymmetry test even if
it passes all other checklist items.

**Finding 5 — One structural limitation remains (scope for Phase C).**

The sprint exit gate is defined in this phase's sprint-planning-sop.md amendment, but the
sprint entry protocol (what must exist before implementation begins) is not yet formalized.
Phase C will encode the sprint entry gate — the mirror image of the exit gate. Until Phase C
is complete, the entry side of the sprint boundary depends on the existing PM Agent sprint
planning SOP and the Phase A lifecycle's Step 1 requirement (intent document before
implementation). This is an appropriate Phase C scope item, not a Phase B gap.

**PI Agent verdict:** Enforcement language is adequate for Phase B exit. The acceptance protocol's
per-type passing checklists are observable and binary. The rejection artifact protocol has teeth.
The DEMO4 class check is explicitly embedded. The asymmetry test operationalizes FD-3 at Validate.
One structural limitation (sprint entry gate) is correctly deferred to Phase C. Phase B may close
and Phase C may open.

---

## Part IV — Exit Gate Checklist

Per `docs/process/sprint-plans/process-redesign-phaseB-sprint-entry.md §Exit Gate`:

| # | Condition | Status |
|---|---|---|
| 1 | `docs/process/acceptance-protocol.md` filed with per-work-type verification criteria | ✅ Confirmed — all four work types specified |
| 2 | PI Agent confirms enforcement language is adequate (obligation, not aspiration) | ✅ Confirmed — Part III Findings 1–4 |
| 3 | EL endorses Phase B outputs | ✅ Endorsed 2026-06-12 — Part VII |
| 4 | Phase C sprint entry document is filed | ✅ Filed — `docs/process/sprint-plans/process-redesign-phaseC-sprint-entry.md` |
| 5 | SESSION_STATE.md updated to reflect Phase B complete and Phase C entry filed | ✅ Updated 2026-06-12 — Phase B ENDORSED; Phase C OPEN |
| 6 | Any deferred items explicitly listed with rationale | ✅ See Part III Finding 5 — sprint entry gate deferred to Phase C |

**Gate status: 6 of 6 conditions confirmed. Phase B CLOSED.**

---

## Part V — North Star Validation Question

Per CLAUDE.md §North Star Test (Process Gate):

*"If the Zambian finance ministry analyst is using WorldSim to prepare for a restructuring
session and the implementing agent delivers the political economy module's conditionality
constraint output — does the Business PO Acceptance Protocol ensure that output is usable
in that room before the sprint closes?"*

**Answer: Yes, in two specific ways.**

First: the analytics validation protocol (§1.4) requires the Business PO to name the specific
argument the Zambian ministry analyst can make at the table — not that the feature is delivered,
but that the argument is nameable and citable. "The conditionality constraint model shows that
the IMF's wage-cut terms reduce implementation capacity by 23% in the first year" is a citable
argument. "The model is working" is not.

Second: the asymmetry test (§1.2 and §1.4) requires confirming the argument is usable without
specialist mediation the creditor side can provide and the ministry side cannot. If the argument
can only be deployed by a PhD econometrician and the ministry team has three generalist
economists, the Validate step fails even if the output is technically correct. This is the
Kryptonite constraint at the Validate step, not only at intent authorship.

**Validation verdict:** Phase B outputs are sufficient to confirm mission alignment at the sprint
exit gate for the political economy module and for subsequent M13 deliverables.

---

## Part VI — Known Limitations

| Limitation | Mitigation in place | Forward path |
|---|---|---|
| Sprint entry gate not yet formalized: the entry side of the sprint boundary (what must exist before implementation begins) is not in this phase's scope | Phase A lifecycle Step 1 requirement (intent document before implementation) covers the pre-implementation gate; PM Agent sprint planning SOP covers entry consultation | Phase C formalizes the sprint entry gate to mirror the sprint exit gate encoded here |
| Business PO ACCEPT mode activation is described but its output filing location is not yet part of a sprint exit checklist template | sprint-planning-sop.md §Sprint Exit Gate names the conditions; Phase C will produce sprint exit checklist template that encodes these conditions as checkboxes | Phase C sprint exit template |
| The EL exception path depends on the EL being available in the session the rejection occurs | PI Agent near-miss entry and the sprint exit block provide a fallback: the sprint cannot close without either re-acceptance or EL exception, so the EL's availability gates the sprint close rather than the exception | No process fix available — this is a single-principal governance limitation documented in CLAUDE.md §Governance |

---

## Part VII — EL Endorsement Space

The Engineering Lead reviews this exit artifact and all primary outputs listed in Part I.
Endorsement constitutes approval that:
1. The per-work-type verification criteria in `docs/process/acceptance-protocol.md` are adequate
2. The exception path in `docs/process/acceptance-protocol.md §Part 2` is accepted
3. The PI enforcement review in Part III is accepted
4. The north star validation finding in Part V is accepted
5. The known limitations in Part VI are acceptable for this phase
6. Phase C may open using `docs/process/sprint-plans/process-redesign-phaseC-sprint-entry.md`

**EL endorsement:**

> Endorsed 2026-06-12. Phase B outputs accepted. Per-work-type verification criteria adequate.
> Exception path accepted. PI enforcement review accepted. North star validation finding accepted.
> Known limitations acceptable for this phase. Phase C may open.
> — @PublicEnemage (PR #902 merged)

---

*This artifact is the canonical exit record for Phase B. It must not be modified after EL
endorsement except to add the endorsement itself and update SESSION_STATE.md.*
