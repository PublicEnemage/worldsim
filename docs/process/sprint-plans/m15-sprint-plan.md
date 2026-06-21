---
name: m15-sprint-plan
type: sprint-plan
milestone: M15 — Human Cost Architecture
status: EL Approved — implementation may begin (sprint entry document required per group)
authored-by: PM Agent
authored-date: 2026-06-20
el-approved: 2026-06-20
consulted-agents:
  - Business Product Owner (value prioritization and Demo 6 scope)
  - Frontend Architect (component grouping and ADR-015 Component 4 assessment)
  - Architect (ADR prerequisites — Zone 1A ADR-017, ADR-016 Component 3)
  - Chief Methodologist (cohort disaggregation scope and PSP calibration)
sop-reference: docs/process/sprint-planning-sop.md
---

# M15 Sprint Plan — Human Cost Architecture

**Status:** EL Approved 2026-06-20 — implementation may begin; sprint entry document required per group before implementation PR opens
**Release branch:** `release/m15` (cut from `main` 2026-06-20 at commit 500e50d)
**Exit checklist issue:** #984 (note: title reads "Milestone 16 Exit Checklist" — follows GitHub milestone numbering; content is correct for M15)
**Primary objective:** Zone 1A information architecture ADR + Layer 3 self-interpreting outputs (Zone 1B + Zone 1D) + live stakeholder demo with real external participants (#843) as M15 exit gate.

**M15 exit gate:** #843 — live stakeholder demo with real external participants AND Zone 1A architectural foundation for Demo 6 in place. #984 (exit checklist) closes last.

**CLAUDE.md reference:** "M15 closes with real external participant engagement (#843) and the architectural foundation for Demo 6."

---

## HORIZON Sweep — M15 Scope Completeness

Run against `CLAUDE.md §Milestone 15` and `docs/roadmap/worldsim-roadmap.md §Milestone 15`.

| Roadmap deliverable | Issue | Group |
|---|---|---|
| Zone 1A information architecture ADR and implementation (Phases 2–4) | #845 | G2 |
| Layer 3 trajectory sentence in Zone 1B | #1065 | G1 |
| Cohort disaggregation on primary surface | #986 | G3 |
| Path 1: approved source network query at scenario creation | #975 | G4 |
| Live stakeholder demo with real external participants | #843 | G8 (exit gate) |
| Accessibility validation on 8GB/4-core target hardware | #990 | G6 |

**Additional M15 scope (from M14 exit and IR findings):**

| Issue | Title | Group |
|---|---|---|
| #1065 | Layer 3 trajectory sentence — Zone 1B | G1 |
| #1066 | Suppress "0 consecutive steps" when zero | G1 |
| #1068 | L0 badge on Zone 1A trajectory curves | G1 |
| #1069 | Dual reserve values disambiguation in Grounding strip | G1 |
| #1075 | PSP self-interpreting sentence in Zone 1D | G1 |
| #1083 | Grounding strip date label "2024-Q1" → "Apr 2024" | G5 |
| #1084 | PSP historical calibration anchor | G5 |
| #1088 | Walkthrough update — "0 consecutive steps" plain language (DEMO-123) | G5 |
| #1089 | Walkthrough update — Grounding strip persistence note (DEMO-124) | G5 |
| #1090 | Walkthrough update — methodology documentation URL (DEMO-129) | G5 |
| #1004 | Visual Spec section for intent template | G5 |
| #1048 | Docker API container Alembic migrations (NM-049) | G5 |
| #1007 | Recompute-badge not visible after apply-control-change | G5 |
| #1091 | CLAUDE.md extraction — child docs for Lifecycle, Exit SOP, DIC | G7 |
| #53 | Information Access Architecture (RBAC design) | G4 prerequisite |
| #3, #6 | Governance (EL-action items) | G7 |
| #843 | Live stakeholder demo | G8 exit gate |

**ADR backlog review (HORIZON prerequisite):**

| ARCH entry | Status | Priority for M15? |
|---|---|---|
| ARCH-001 through ARCH-010 | All ACCEPTED | No action needed |
| ARCH-011 (new) | PENDING_NUMBER | Zone 1A information architecture ADR — assign ADR-017; required before G2 implementation begins |

No PENDING entries from prior milestones are more urgent than the proposed ADR-017. Zone 1A is unblocked: Phase 1 design thinking doc complete (M14 G6c, PR #1033); Architecture Review is next.

---

## Four-Agent Consultation Summary

**Business Product Owner (value prioritization):**
The Demo 6 north star is a finance ministry analyst who can show a counter-proposal branch — an alternative conditionality structure with a visible reserve arc and a PSP reading — and trace the full evidence chain for both branches. Two capabilities gate Demo 6: (1) Layer 3 self-interpreting outputs (Zone 1B trajectory sentence — #1065 — and PSP sentence — #1075), so the analyst can forward a screenshot and the finding is present without a presenter; (2) the architectural foundation for cohort disaggregation (#986) and the Zone 1A ADR (#845) so the human cost ledger is designed to be primary, not secondary.

The five IR-001–IR-005 findings from Demo 5 are the highest-priority M15 items: they represent capability gaps that became visible when real stakeholders encountered the tool. G1 must ship before #843 (live external demo) runs. The live external demo cannot achieve north star PASS while these findings remain open.

**Frontend Architect (component grouping):**
G1 (Layer 3 + IR fixes) items cluster into two component surfaces:
- Zone 1B surface: #1065 (Layer 3 sentence), #1066 (suppress "0 consecutive steps"), #1069 (Grounding strip disambiguation label)
- Zone 1A/1D surface: #1068 (L0 badge on Zone 1A trajectory), #1075 (PSP sentence in Zone 1D)

These two surfaces do not conflict — Zone 1B and Zone 1A/1D are separate component trees. They can proceed in parallel as two PRs, or as a single G1 PR if the scope is small enough (Frontend Architect recommends one PR to avoid merge sequencing overhead for a set of targeted fixes).

Zone 1A ADR (G2) will touch the same Zone 1A component tree as #1068. Sequence: implement #1068 first (targeted L0 badge fix, low risk), then proceed with ADR-017 implementation which may refactor Zone 1A more substantially. This avoids implementing against an unstable Zone 1A design.

ADR-016 Component 3 (Fidelity contextualisation, deferred from M14) is in M15 scope per ADR-016. No new ADR required — the design is in ADR-016 §Component 3. This is a separate G4 item.

**Architect (ADR prerequisites):**
ADR-017 (Zone 1A information architecture) requires an Architecture Review (ARCH-REVIEW) before authorship. The Phase 1 design thinking doc (`docs/ux/design-thinking/zone-1a-information-architecture.md`, M14 G6c) is the empirical evidence base. ARCH-011 must be marked ASSIGNED in the backlog before ADR-017 authorship begins, and the panel composition must be derived from `docs/process/agent-raci.md`.

Zone 1A is a Tier 1 ADR (touches primary viewport instrument across all three modes). Panel minimum: Architect Agent (author), UX Designer (independent sign-off required), Frontend Architect (C), Business PO (C), Customer Agent (Layer 3 assessment), Engineering Lead (A).

No new ADR is required for G1 (Layer 3 fixes are within the scope of accepted ADR-015 Component 4 — evidence chain as directive sentence in Zone 1B — and ADR-015 Component 3 for PSP). EL should confirm ADR-015 Component 4 scope covers #1065 before G1 sprint entry is filed.

**Chief Methodologist (cohort disaggregation and PSP):**
Cohort disaggregation (#986) requires design scope definition before implementation: which cohorts, which indicators, which thresholds, and how to surface them on the primary surface without requiring drawer navigation. This is design-only in M15 (implementation in M16). The CM recommends a design document approach similar to M14 G6c (Zone 1A Phase 1 design thinking) — output a design specification that gates M16 implementation.

PSP historical calibration (#1084) requires Zambia ECF backtesting data. The CM notes this is medium scope for M15: the anchor need not be exhaustive — a single validated historical case (e.g., a prior ECF programme with known compliance outcome) at PSP ≈ 0.65 would satisfy the practitioner's question from Demo 5 Q6. M15 scope: identify and document one anchor case. Full backtesting calibration of the PSP model is M16 scope.

---

## Sprint Groups

| Group | Issues | ADR gate | Wave | Description |
|---|---|---|---|---|
| G1 — Layer 3 + IR Fixes | #1065, #1066, #1068, #1069, #1075 | ADR-015 ✅ (Component 4 scope per EL confirmation) | Wave 1 | Zone 1B Layer 3 trajectory sentence; suppress zero consecutive steps; L0 badge on Zone 1A trajectory; Grounding strip initial-state label; PSP self-interpreting sentence in Zone 1D. Single PR or two parallel PRs by surface (Zone 1B and Zone 1A/1D). |
| G2 — Zone 1A ADR | #845 (Phases 2–3) | ARCH-011 → ADR-017 (new) | Wave 2 | Architecture Review (ARCH-REVIEW) → ADR-017 authorship → EL acceptance → Phase 3 implementation design. Zone 1A Tier 1 ADR: full panel required (UX Designer independent sign-off). Phase 4 (implementation) may extend to M16 depending on scope. |
| G3 — Cohort Disaggregation Design | #986 | None (design-only) | Parallel | Design specification for cohort disaggregation on primary surface — which cohorts, indicators, thresholds, and zero-interaction access path. Output: `docs/ux/design-thinking/cohort-disaggregation-design.md`. No implementation in M15. Design document gates M16 G-group. No sprint entry document required. |
| G4 — Path 1 + ADR-016 Component 3 | #975, #53 (RBAC design) | ADR-016 ✅ (Component 3 in scope) | Parallel | Path 1 approved source network query at scenario creation (Journey A GA-01). ADR-016 Component 3 (Fidelity contextualisation — deferred from M14). RBAC design (#53, prerequisite for Path 2 implementation in M16). Data Architect must update `api_contracts.yml` for any new endpoints before G4 implementation begins. |
| G5 — Process Fixes + Walkthrough Updates | #1004, #1048, #1007, #1083, #1084, #1088, #1089, #1090 | None | Parallel | Visual Spec section for intent template; Docker Alembic migrations; recompute-badge; Grounding strip date label fix; PSP calibration anchor documentation; three walkthrough updates (DEMO-123/124/129) before #843 runs. Low-risk; may proceed early in M15 before G1 ships. |
| G6 — Accessibility Validation | #990 | None | Parallel | Accessibility validation on 8GB/4-core target hardware. Run existing test suite on target hardware; document findings; file issues for any failures. No implementation in M15 unless blocking issues found. |
| G7 — Process Documentation | #1091, #3, #6 | None | Parallel | CLAUDE.md extraction to child docs (#1091); governance items (#3, #6 — EL-action, no implementation agent can act). #1091 requires reviewing all CLAUDE.md cross-references before extracting sections. |
| G8 — Live External Demo (#843) | #843 | G1 must be merged | Exit gate | Live stakeholder demo with real external participants. Gate: G1 Layer 3 fixes merged (Zone 1B/1D must show self-interpreting output before real external participants attend). Stakeholder review artifact filed after session. M15 exit gate. |

---

## Sprint Sequencing

```
G5 (fixes + walkthrough updates) ──────────────────────────────────────────┐
                                                                            │
G6 (accessibility validation — parallel) ──────────────────────────────────┤
                                                                            │
G7 (process documentation — parallel) ─────────────────────────────────────┤
                                                                            ├──► G8 (Live external demo — M15 exit)
G1 (Layer 3 + IR fixes) ────────────────────────────────────────────────── ┤
                                                                            │
G3 (cohort disaggregation design — parallel, design-only) ─────────────────┤
                                                                            │
G4 (Path 1 + ADR-016 Component 3) ─────────────────────────────────────────┤
                                                                            │
G2 (Zone 1A ADR-017) ──► ADR-017 Accepted ─► (Phase 3 implementation) ────┘
```

No sequential dependency between G1, G3, G4, G5, G6, G7 — these can proceed in parallel after EL approval of this sprint plan. G8 is gated on G1 (Layer 3 must be on screen before the live external demo runs). G2 (Zone 1A ADR) has an internal sequence: ARCH-REVIEW → ADR authorship → EL acceptance → implementation; the ADR phase may complete in M15 with Phase 4 implementation extending to M16.

G3 and G6 produce no implementation PRs — no sprint entry document required for either.

---

## Sprint Entry Gate Requirements

Per `docs/process/sprint-planning-sop.md §Sprint Entry Gate`, implementation may not begin on any sprint group until:

1. This sprint plan is EL-approved (record approval as PR comment or commit to this document)
2. A sprint entry document is filed at `docs/process/sprint-plans/m15-{group}-sprint-entry.md` per the template
3. The entry document is committed and referenced in `SESSION_STATE.md`

**Exceptions (no sprint entry document required):**
- G3 (cohort disaggregation design — design artifact only, no implementation PR)
- G6 (accessibility validation — testing and documentation only, no implementation PR unless issues found)
- G7 §1091 component (process documentation — no code, only document edits)

**ADR gate note:** G2 requires ARCH-011 assigned from the backlog and ADR-017 accepted before a G2 implementation sprint entry document can be filed. The ADR authorship phase (Architecture Review → ADR authorship → EL acceptance) proceeds under the normal ADR process, not the sprint entry gate. The sprint entry gate applies only when implementation code begins.

---

## Exit Conditions

M15 closes when all of the following are satisfied:

1. **Business PO acceptance** recorded for all user-facing G-group deliverables (G1, G4)
2. **Customer Agent Layer 3 assessment** on record for any capability serving Personas 2, 3, or 5 (G1 required: Zone 1B trajectory sentence, PSP sentence)
3. **North star test artifact** filed: a Zambian finance ministry analyst (or equivalent Demo 6 scenario) can read the Layer 3 trajectory sentence from Zone 1B and the PSP sentence from Zone 1D without specialist mediation — and forward a screenshot with both sentences visible
4. **Live stakeholder demo delivered** (#843): real external participants attended; stakeholder review artifact filed
5. **Zone 1A architectural foundation** in place: ADR-017 accepted (or Architecture Review + draft-ADR filed with EL exception if scope requires M16 for acceptance); cohort disaggregation design document filed
6. **PI Agent exit gate confirmation** recorded in the M15 sprint exit document

CI green and issue closure are necessary but not sufficient. #843 is the primary exit gate; Zone 1A ADR-017 acceptance is the secondary gate.

---

## M15 Kickoff Sequence

1. ✅ PM Agent cuts `release/m15` from `main` — DONE 2026-06-20
2. ✅ PM Agent authors this sprint plan — DONE 2026-06-20
3. ✅ EL approves sprint plan — DONE 2026-06-20
4. ⬜ PM Agent marks ARCH-011 ASSIGNED in `docs/architecture/backlog.md`; derives panel composition — at ADR-017 authorship time
5. ✅ M15 Exit Checklist issue #984 renamed to "M15 Exit Checklist — blocks milestone closure" — DONE 2026-06-20

**EL approved 2026-06-20.** No implementation PR may open against `release/m15` until a sprint entry document is filed and EL-approved for the relevant group.

---

*M15 sprint plan authored by PM Agent 2026-06-20 as part of HORIZON sweep. Release branch `release/m15` cut from `main` 2026-06-20. EL approval required before any implementation PR opens against `release/m15`.*
