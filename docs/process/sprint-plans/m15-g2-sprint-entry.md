---
name: m15-g2-sprint-entry
type: sprint-entry
milestone: M15 — Human Cost Architecture
sprint-group: G2
status: EL Approved 2026-06-21 — intent document and QA tests must be filed before G2 work begins
authored-by: PM Agent
authored-date: 2026-06-21
el-approved: 2026-06-21
release-branch: release/m15
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M15, G2: Zone 1A Information Architecture ADR

**Status:** EL Approved 2026-06-21 — intent document and QA tests must be filed before G2 work begins
**Date authored:** 2026-06-21
**Release branch:** `release/m15`
**Sprint plan:** `docs/process/sprint-plans/m15-sprint-plan.md` (EL Approved 2026-06-20)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G2 specifically. G2 is an architecture/design sprint — its primary deliverables
are a filed Architecture Review (ARCH-REVIEW-007-milestone15.md) and an accepted ADR-017.
Phase 4 implementation (Zone 1A code changes) is out of G2 scope and may extend to M16; a
separate sprint entry will be required for Phase 4 when it begins. No architecture review
document may be filed, and no ADR-017 authorship may begin, until this entry is EL-approved.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M15 — Human Cost Architecture |
| GitHub Milestone | #16 |
| Sprint group | G2 — Zone 1A Information Architecture ADR |
| Release branch | `release/m15` |
| Sprint plan document | `docs/process/sprint-plans/m15-sprint-plan.md` |
| Exit checklist issue | #984 |
| Sprint groups in scope | G2 only |
| ADR gate | ARCH-011 → ADR-017 (new — Architect Agent claims number at authorship time) |
| Implementing agents | Architect Agent (ADR author); UX Designer Agent (Architecture Review + independent sign-off); Frontend Architect Agent (C); Business PO (C); Customer Agent (Layer 3 assessment); Engineering Lead (A) |
| Wave | Wave 2 (parallel to G3, G4, G5, G6, G7; gates G2 Phase 4 implementation which may extend to M16) |
| Issue in scope | #845 (Phases 2–3 only) |
| Hard stop cleared | ✅ 2026-06-21 — constraints PR #1102 merged to `release/m15` (AC-001 + AC-002; #53 permanently closed) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before G2 Architecture Review work begins.
An unchecked invariant blocks G2 from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m15` cut from `main` 2026-06-20 (commit 500e50d)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed 2026-06-20 (line 5: `branches: [ main, develop, release/m* ]`;
  line 7: `branches: [ main, release/m* ]`). Ruleset ID 17751852 with 6 required checks:
  `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
  KI-005 permanent fix (`do_not_enforce_on_create: true`) applied 2026-06-20.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m15-sprint-plan.md`
  `el-approved: 2026-06-20` (PR #1094 — EL approval recorded 2026-06-20)
- [x] **Constraint record PR merged:** PR #1102 merged to `release/m15` 2026-06-21
  (AC-001 private data prohibition + AC-002 synthetic substitution; #53 permanently closed;
  G4 scope confirmed as #975 + ADR-016 Component 3 only). Hard stop cleared.

### 2.2 — ADR prerequisite gate

G2 is the ADR authorship sprint. There is no antecedent ADR blocking G2 work from
beginning. ADR-017 is the *output* of G2, not a prerequisite for it. ARCH-011 marking
ASSIGNED is a required prerequisite step *within* G2 (must occur before ADR-017 authorship
begins), not an external sprint gate.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G2 — Architecture Review (Phase 2) | None | N/A | **CLEAR** |
| G2 — ADR-017 authorship (Phase 3) | ARCH-011 ASSIGNED in backlog | Currently PENDING_NUMBER — Architect Agent marks ASSIGNED at authorship start | **CLEAR — prerequisite is within-sprint step** |
| G2 Phase 4 implementation | ADR-017 accepted | Not yet authored | **BLOCKED — Phase 4 is out of this sprint's scope; separate entry required** |

**ARCH-011 ASSIGNED prerequisite:** Before the Architect Agent begins drafting ADR-017, the
Architect Agent must mark ARCH-011 ASSIGNED in `docs/architecture/backlog.md` with the ADR-017
number and the panel composition derived from `docs/process/agent-raci.md`. The number ASSIGNED
is ADR-017 (next available per the backlog ADR Registry). This is the first step of G2 Phase 3
work; it does not block the Architecture Review (Phase 2).

- [x] **ADR prerequisite gate:** No external ADR blocks G2. ARCH-011 ASSIGNED is an internal
  within-sprint step; gate: **CLEAR for G2 to begin.**

### 2.3 — Intent document gate

*For G2, an intent document must be filed before Architecture Review work begins.
G2 is an architecture/design sprint — the observable states are document-level, not
application-level. Intent document acceptance criteria must be specific enough that the
QA Lead can check them without reading any authorship drafts in progress.
(Authority: CLAUDE.md §Agent Execution Lifecycle Step 1)*

- [ ] Intent document filed for G2 deliverables — **MUST FILE BEFORE G2 WORK BEGINS**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| Phase 2: ARCH-REVIEW-007-milestone15.md (Architecture Review) | #845; Phase 1 design thinking doc | `docs/process/intents/M15-G2-2026-06-21-zone-1a-adr.md` | No — BLOCKING |
| Phase 3: ADR-017 authorship + panel sign-offs + EL acceptance | ARCH-011 → ADR-017 | (same intent document) | No — BLOCKING |

Both G2 deliverables may be covered by a single intent document
(`M15-G2-2026-06-21-zone-1a-adr.md`). The intent document must derive acceptance
criteria from the observable document states in Section 3 below.

**Completeness gate:** The QA Lead must be able to check each acceptance criterion by
reading the filed documents — not by evaluating the quality or correctness of their
contents. An acceptance criterion that requires expert judgment to verify is incomplete.

### 2.4 — QA test authorship gate

*For G2 (architecture/design sprint with no frontend code), QA tests take the form of
file-existence and content-presence checks analogous to M14 G7 governance documentation
sprint (`backend/tests/test_m14_g7_governance_onboarding.py`). Tests must be authored
from the intent document's acceptance criteria BEFORE G2 document authorship begins.
(Authority: CLAUDE.md §Agent Execution Lifecycle Step 2)*

- [ ] QA test file authored for G2 before work begins — **MUST FILE BEFORE G2 WORK BEGINS**

| Deliverable | Intent document | Test file path | Authored before work begins? |
|---|---|---|---|
| ARCH-REVIEW-007 + ADR-017 (all G2 ACs) | `docs/process/intents/M15-G2-2026-06-21-zone-1a-adr.md` | `backend/tests/test_m15_g2_zone1a_adr.py` | No — BLOCKING |

**Expected test coverage (to be specified in the intent document):**
- File existence: ARCH-REVIEW-007-milestone15.md at canonical location
- File existence: ADR-017 at `docs/adr/ADR-017-zone-1a-information-architecture.md`
- Content presence in ADR-017: required sections from `docs/adr/template.md`
- NM-042 compliance: UX Designer sign-off block has all four named fields (Reviewing agent,
  Session context, Governing documents reviewed, Concerns found)
- ARCH-011 status: `docs/architecture/backlog.md` contains `ASSIGNED — ADR-017` string
  (not PENDING_NUMBER) for ARCH-011 row
- Phase 2 readiness questions: ARCH-REVIEW addresses all three questions from
  `docs/ux/design-thinking/zone-1a-information-architecture.md §Phase 2 Readiness`

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state (pre-work specification) |
|---|---|---|---|
| #845 (Phase 2) | ux: Zone 1A information architecture — Architecture Review | immediate | `docs/architecture/reviews/ARCH-REVIEW-007-milestone15.md` exists and contains explicit assessments of all three Phase 2 readiness questions from `docs/ux/design-thinking/zone-1a-information-architecture.md §Phase 2 Readiness`: (Q1) Zone 1A's primary question per mode; (Q2) encoding channels used; (Q3) N/M limits before legibility breaks. The review also addresses the four open Phase 2 questions from §Phase 2 Readiness (Mode 3 single-entity encoding choice, multi-entity COMPARE_VIEW, composite score aggregation rule, endpoint label collision). |
| #845 (Phase 3) | ux: Zone 1A information architecture — ADR-017 authorship and acceptance | immediate | `docs/adr/ADR-017-zone-1a-information-architecture.md` exists, has been accepted by the Engineering Lead (`el-approved: [date]` in frontmatter or EL comment on #845), and satisfies all of the following: (a) ARCH-011 in `docs/architecture/backlog.md` is marked `ASSIGNED — ADR-017`; (b) UX Designer sign-off block has all four fields from NM-042 (Reviewing agent, Session context, Governing documents reviewed with named sections, Concerns found); (c) Session context field is declared (`Same session as ADR authorship — acknowledged` or `Separate session, EL-triggered YYYY-MM-DD`); (d) EL sign-off is present. |

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| #845 Phase 4 — Zone 1A implementation (code changes) | Out of G2 scope. Phase 4 implementation may extend to M16. A separate sprint entry document must be filed when Phase 4 begins; it is gated on ADR-017 acceptance. Phase 4 implementing agent will be the Frontend Architect Agent. |
| G1 (#1065, #1066, #1068, #1069, #1075) | ✅ Complete 2026-06-21 — all five Layer 3 IR fixes merged and BPO accepted |
| G3 (#986 cohort disaggregation design) | Parallel — design-only; no sprint entry required per sprint plan |
| G4 (#975 Path 1, ADR-016 C3) | Parallel — independent; no dependency on G2 |
| G5 (process fixes + walkthrough updates) | Parallel — no dependency on G2 |
| G6 (#990 accessibility validation) | Parallel — testing and documentation only |
| G7 (#1091, #3, #6) | Parallel — process documentation |
| G8 (#843 live external demo) | Gated on G1 (✅ complete) — not gated on G2 |
| ADR-016 Component 3 (Fidelity contextualisation) | G4 scope — no new ADR required; design in ADR-016 |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Work may begin? |
|---|---|---|---|
| G2 — Architecture Review (Phase 2) | None | N/A | **Yes — after EL approves this entry document and intent + QA gates are satisfied** |
| G2 — ADR-017 authorship (Phase 3) | ARCH-011 ASSIGNED | Must be done as first step of Phase 3 | **Yes — Architect Agent marks ASSIGNED before drafting begins (within-sprint prerequisite step)** |
| G2 Phase 4 implementation | ADR-017 accepted by EL | Not yet authored | **No — separate sprint entry required; Phase 4 may extend to M16** |

**Panel composition for ADR-017 (Tier 1 — UX Designer independent sign-off required):**

Per `docs/architecture/backlog.md §Panel Composition Rule` and `docs/process/agent-raci.md`,
ADR-017 is a Tier 1 frontend/UX architecture ADR. Minimum panel:

| Role | Agent | Authority |
|---|---|---|
| Author | Architect Agent | R (authors ADR-017) |
| Independent sign-off | UX Designer Agent | R (Tier 1 sign-off; NM-042 compliance required) |
| Consulted | Frontend Architect Agent | C (component design; Zone 1A refactor scope) |
| Consulted | Business PO | C (value prioritization; Persona 2 cognitive task at table) |
| Consulted | Customer Agent | Layer 3 quality assessment |
| Consulted | Chief Methodologist | C (composite score aggregation rule for multi-entity; open question Q3 from Phase 1) |
| Accountable | Engineering Lead | A (acceptance) |

*The implementing agent for Phase 4 (Frontend Architect Agent) must be included in the
ADR-017 panel per the backlog Panel Composition Rule. Frontend Architect Agent is already
listed as C above; confirm at ADR authorship time that this satisfies the implementing-agent
inclusion requirement.*

**Sequencing note for G2:**

1. EL approves this entry document
2. Architect Agent authors intent document at `docs/process/intents/M15-G2-2026-06-21-zone-1a-adr.md`
3. QA Lead authors `backend/tests/test_m15_g2_zone1a_adr.py` from intent document before
   G2 work begins (file-existence + content-presence checks as described in §2.4)
4. Architecture Review Facilitator activates Phase 2: `Architecture Review: FULL — Zone 1A information architecture (#845 Phases 2–3)`
5. Architect Agent marks ARCH-011 ASSIGNED in `docs/architecture/backlog.md` with number ADR-017
   and panel composition (before authoring ADR-017 draft)
6. Architect Agent files ARCH-REVIEW-007-milestone15.md at `docs/architecture/reviews/` addressing
   all Phase 2 readiness questions from the Zone 1A design thinking document
7. Architect Agent authors `docs/adr/ADR-017-zone-1a-information-architecture.md` using
   `docs/adr/template.md` as starting point; evidence base: Phase 1 design thinking doc +
   ARCH-REVIEW-007
8. Panel sign-offs: UX Designer Agent independent sign-off (NM-042 compliant); Frontend Architect
   Agent; Business PO; Customer Agent Layer 3 assessment
9. EL acceptance — ADR-017 accepted
10. Business PO Step 5 Validate: confirms that the accepted ADR-017 specifies a Zone 1A encoding
    that allows Persona 2 (Eleni, finance ministry negotiator) to answer the Mode 3 question
    ("did this control input help or hurt?") within the 15-second ceiling for N≤4 entities
    — without specialist mediation — and the Mode 1/2 question within the 30-second ceiling
11. G2 sprint exit document filed

**G8 gate dependency:** G8 (#843 live external demo) is NOT gated on G2. G8 is gated on G1
(✅ complete 2026-06-21). G2 ADR-017 acceptance feeds into Phase 4 implementation which is
the architectural foundation for Demo 6. G2 does not block G8.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-21
**Sweep period:** Since M15-G1 sprint exit filed (2026-06-21 — same session)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No additional process gaps identified in the sweep period. NM-051 (QA mock field name mismatch) was filed and resolved during G1 in the same session. Constraint record (AC-001 + AC-002) filed by EL as architectural decisions — not near-miss material (these are positive scope clarifications, not process defects). G4 scope update (#53 removal) recorded in SESSION_STATE only — no process gap; #53 was correctly closed will-not-implement per AC-001. | N/A | N/A | N/A |

---

## EL Approval Record

**EL approval:** 2026-06-21

> G2 sprint entry approved. Structural gates confirmed clear — release branch exists, CI trigger verified, sprint plan EL-approved, constraint record PR #1102 merged. ADR prerequisite gate clear: no external ADR blocks G2; ARCH-011 ASSIGNED is a within-sprint step. Scope correctly bounded to #845 Phases 2–3 (Architecture Review + ADR-017 authorship); Phase 4 implementation is correctly excluded with a separate sprint entry required. Panel composition for ADR-017 (Tier 1) confirmed: Architect Agent (author), UX Designer independent sign-off (NM-042 compliant session context required), Frontend Architect Agent (C), Business PO (C), Customer Agent (Layer 3), Chief Methodologist (C — composite aggregation rule), EL (A). Intent document and QA test file must be filed before Architecture Review begins — these remain blocking conditions.
> — @PublicEnemage (2026-06-21)
