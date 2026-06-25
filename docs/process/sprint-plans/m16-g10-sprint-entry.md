---
name: m16-g10-sprint-entry
type: sprint-entry
milestone: M16 — Distributional Visibility
sprint-group: G10
status: EL Approved 2026-06-24 — work may begin per sequencing in §4
authored-by: PM Agent
authored-date: 2026-06-24
el-approved: 2026-06-24
release-branch: release/m16
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M16, G10: Pre-Demo Polish

**Status:** EL Approved 2026-06-24 — work may begin per sequencing in §4
**Date authored:** 2026-06-24
**Release branch:** `release/m16`
**Sprint plan:** `docs/process/sprint-plans/m16-sprint-plan.md` (EL Approved 2026-06-23; amended 2026-06-24 to add G10)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G10 formalizes five Customer Agent Layer 3 pre-demo conditions that were filed across three
sprint exits (G1, G3, G4) as required before the live Demo 6 session (#843). These items were
named in PI Agent confirmations but held no sprint group assignment. G10 is a G8 gate condition:
#843 may not be scheduled until all five G10 fixes are confirmed merged to `release/m16`.
G10 is not capacity-allowing — it is on the critical path to G8.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M16 — Distributional Visibility |
| GitHub Milestone | #17 |
| Sprint group | G10 — Pre-Demo Polish |
| Release branch | `release/m16` |
| Sprint plan document | `docs/process/sprint-plans/m16-sprint-plan.md` |
| Exit checklist issue | #985 |
| Sprint groups in scope | G10 only |
| ADR gate | None |
| Implementing agent | Frontend Developer (all five fixes are frontend/UX) |
| Wave | Wave 2+ — begins as soon as source CA conditions are filed; must complete before G8 is scheduled |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any G10 implementation PR is opened.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m16` cut from `main` 2026-06-23 (commit 07c92b8)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at kickoff 2026-06-23 (line 5: `branches: [ main, develop, release/m* ]`;
  line 7: `branches: [ main, release/m* ]`). Ruleset ID 17751852 with 6 required checks.
  KI-005 permanent fix (`do_not_enforce_on_create: true`) applied 2026-06-20.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m16-sprint-plan.md`
  `el-approved: 2026-06-23` (PR #1148); amended 2026-06-24 to add G10.

### 2.2 — ADR prerequisite gate

G10 contains no items requiring a new ADR. All five fixes are narrow, bounded changes to
existing components — text substitution, label addition, or tooltip addition — none of which
introduces a new architectural surface or crosses a module boundary:

| Issue | Required ADR | ADR status | Gate |
|---|---|---|---|
| #1162 — Zone 1A attribution anchor | None — within existing DivergenceFillLayer component | N/A | **CLEAR** |
| #1177 — Milestone sentence year anchor | None — output template text change | N/A | **CLEAR** |
| #1178 — T3 badge L0 legibility | None — within existing badge/tooltip component | N/A | **CLEAR** |
| #1179 — Q2 curve asymmetry label | None — within existing chart annotation layer | N/A | **CLEAR** |
| #1184 — SAD badge L0 legibility | None — within existing badge/tooltip component | N/A | **CLEAR** |

- [x] No ADR prerequisites for G10. Gate: **CLEAR**.

### 2.3 — Intent document gate

All five G10 issues produce user-facing application state. However, the scope of each fix
is fully bounded by the Customer Agent Layer 3 condition that produced it: the CA assessment
names the exact failure mode, the affected persona, and the required observable state change.
The §3.1 observable state declarations in this sprint entry constitute the implementation
specification for each fix — they derive directly from the CA condition language and are
specific enough to gate QA test authorship.

No separate intent document files are required for G10 items. The sprint entry §3.1
observable state serves as the intent specification, and the implementing agent must not
expand scope beyond what the CA condition and observable state together define.

*CA-condition-bounded fixes — §3.1 observable states serve as the intent specification;
no separate intent document files required.*

| Issue | CA source | §3.1 observable state is the specification? | Separate intent file required? |
|---|---|---|---|
| #1162 | G1 C1 (Customer Agent) | Yes | No |
| #1177 | G3 CA-1 (Customer Agent) | Yes | No |
| #1178 | G3 CA-2 (Customer Agent) | Yes | No |
| #1179 | G3 CA-3 (Customer Agent) | Yes | No |
| #1184 | G4 CA-G4-1 (Customer Agent) | Yes | No |

### 2.4 — QA test authorship gate

Each fix produces a specific, testable observable state in the running application. QA test
assertions must be authored before each fix's implementation PR opens. Given the narrow
scope, assertions may extend existing G1/G3/G4 E2E spec files rather than requiring
standalone files — the implementing agent has discretion, but each fix must have at least
one authored test assertion that fails before the fix and passes after.

| Issue | Test approach | Test file (new or extend) | Authored before implementation? |
|---|---|---|---|
| #1162 — attribution anchor | E2E: divergence fill has `data-entity` or tooltip attribution text | Extend `frontend/tests/e2e/m16-g1-zone1a-phase4-composite.spec.ts` or new `m16-g10-predemo-polish.spec.ts` | ⬜ NOT YET — **BLOCKING** |
| #1177 — year anchor | E2E: milestone sentence contains year (e.g., "by 2030") not `[step N]` pattern | Extend `frontend/tests/e2e/m16-g3-25year-human-capital-trajectory.spec.ts` or new file | ⬜ NOT YET — **BLOCKING** |
| #1178 — T3 badge legibility | E2E: T3 badge element has accessible tooltip text or expanded label visible without hover | Extend G3 spec or new file | ⬜ NOT YET — **BLOCKING** |
| #1179 — Q2 asymmetry label | E2E: Q2 curve annotation or legend entry explains floor absence or suppression | Extend G3 spec or new file | ⬜ NOT YET — **BLOCKING** |
| #1184 — SAD badge legibility | E2E: SAD badge element has accessible tooltip text or expanded label visible without hover | Extend `frontend/tests/e2e/m16-g4-distributional-infrastructure.spec.ts` or new file | ⬜ NOT YET — **BLOCKING** |

*All five are BLOCKING — implementation PRs may not open until the corresponding assertion
is authored and committed to `release/m16`.*

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

All five issues derive from Customer Agent Layer 3 assessments produced at G1, G3, and G4
sprint exits. Each fix is explicitly bounded to the minimum change that satisfies the CA
condition — scope must not expand beyond that boundary without a new sprint entry amendment.

---

**#1162 — Zone 1A divergence fill attribution anchor**
*Source: G1 sprint exit, Customer Agent C1*

| Field | Value |
|---|---|
| Issue | #1162 |
| CA source | G1 sprint exit §3 C1 — "Zone 1A divergence fill needs proximate entity attribution anchor before live demo (#843)" |
| Persona affected | Persona 2 (Finance Ministry Negotiator) — first encounter |
| Observable state | In Zone 1A, when a divergence fill is displayed between two entity trajectories, a visible attribution anchor — tooltip, label, or annotation — identifies which entity pair the fill represents without requiring the user to cross-reference a legend or hover over a line. The anchor is visible in the default (non-hover, non-interaction) viewport state. |
| Scope boundary | Minimum change to the `DivergenceFillLayer` component (or equivalent) to add the attribution text. No layout changes to Zone 1A. No changes to fill colouring or trigger logic. |

---

**#1177 — Milestone sentence step-reference → year anchor**
*Source: G3 sprint exit, Customer Agent CA-1*

| Field | Value |
|---|---|
| Issue | #1177 |
| CA source | G3 sprint exit §3 CA-1 — "`[step N]` reference in milestone sentence is technical noise for Persona 5; year anchor sufficient" |
| Persona affected | Persona 5 (Finance Minister) — first encounter |
| Observable state | The 25-year human capital trajectory milestone sentence (Zone 1B or trajectory annotation) renders a calendar year (e.g., "by 2030") in place of — or in addition to — the `[step N]` technical reference. The year is derived from the scenario start date and step resolution. `[step N]` notation does not appear as the sole time reference for Persona 5-facing text. |
| Scope boundary | Output template or rendering function for the milestone sentence only. No changes to backend projection logic. No changes to how steps are stored or computed. |

---

**#1178 — T3 badge L0 legibility**
*Source: G3 sprint exit, Customer Agent CA-2*

| Field | Value |
|---|---|
| Issue | #1178 |
| CA source | G3 sprint exit §3 CA-2 — "`T3` badge text not self-interpreting at L0; hover tooltip provides context but not visible without interaction" |
| Persona affected | Persona 5 (Finance Minister) — first encounter at L0 |
| Observable state | The T3 confidence tier badge is legible at L0 (no hover, no interaction) without specialist mediation. Either: (a) the badge displays expanded text (e.g., "T3 — Inferred") alongside or instead of the bare "T3" label, or (b) an always-visible sub-label beneath the badge provides the confidence tier meaning. Hover tooltip may remain as supplementary detail but must not be the sole source of interpretation. |
| Scope boundary | Badge component rendering only. No changes to confidence tier logic or data. No changes to Zone 1A/1B/1D layout. |

---

**#1179 — Q2 curve asymmetry label**
*Source: G3 sprint exit, Customer Agent CA-3*

| Field | Value |
|---|---|
| Issue | #1179 |
| CA source | G3 sprint exit §3 CA-3 — "Q2 curve silence unexplained on-screen; no MDA-HD-POVERTY-Q2 floor is registered (correct) but asymmetry not labeled" |
| Persona affected | Persona 5 (Finance Minister) — first encounter |
| Observable state | When the Q2 (second quintile) poverty headcount trajectory is absent or suppressed from the chart (because no MDA floor is registered for Q2), an on-screen explanation is visible without hover or drawer navigation — either a legend annotation ("Q2 floor not registered — suppressed"), a chart annotation at the Q2 position, or an always-visible note below the chart. The absence is labeled, not silent. |
| Scope boundary | Chart annotation or legend component for the 25-year trajectory display only. No changes to suppression logic, floor registration, or any backend behavior. |

---

**#1184 — SAD badge L0 legibility**
*Source: G4 sprint exit, Customer Agent CA-G4-1*

| Field | Value |
|---|---|
| Issue | #1184 |
| CA source | G4 sprint exit §3 CA-G4-1 — `"SAD" badge text not self-interpreting at L0 — needs tooltip or expanded label before Demo 6` |
| Persona affected | Persona 5 (Finance Minister) first encounter; Persona 2 (Finance Ministry Negotiator) |
| Observable state | The SAD (Structural Absence Declaration) badge is legible at L0 without specialist mediation. Either: (a) the badge displays expanded text (e.g., "SAD — Structural Absence") alongside or instead of the bare "SAD" label, or (b) an always-visible sub-label provides the meaning. Parallel treatment to #1178 (T3 badge) — the solution pattern should be consistent between the two badge types. Hover tooltip may remain but must not be the sole source of interpretation at L0. |
| Scope boundary | Badge component rendering only — same component updated for #1178 if T3 and SAD share a badge rendering path. No changes to SAD logic or SyntheticDataEngine behavior. |

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| G1/G2/G3/G4/G5/G6/G7/G8/G9 issues | In their respective sprint groups |
| #1147 Zone 1D delta annotations beyond G1 scope | G1 closed |
| ADR-017 P-6 per-framework delta baseline (G1 C3) | Documented scope-alignment note in G1 exit; no issue filed; no G10 scope |
| CA-G4-2 Zone 1D badge wiring deferral (#22 AC-F6) | Documented forward gap in G4 exit; no Demo 6 impact; no G10 scope |
| Full badge system redesign or design-language audit | G10 scope is minimum fix for #1178 and #1184; a systematic badge design pass is future work |
| Any backend changes | All five G10 fixes are frontend rendering changes only |
| Any Zone 1A/1B/1D layout changes | G10 fixes are annotations, labels, and badge text — no layout changes |

---

## Section 4 — ADR Prerequisite Summary

| Issue | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| #1162 — attribution anchor | None | N/A | **Yes — after EL approves this entry and QA test assertion is authored** |
| #1177 — year anchor | None | N/A | **Yes — after EL approves this entry and QA test assertion is authored** |
| #1178 — T3 badge legibility | None | N/A | **Yes — after EL approves this entry and QA test assertion is authored** |
| #1179 — Q2 asymmetry label | None | N/A | **Yes — after EL approves this entry and QA test assertion is authored** |
| #1184 — SAD badge legibility | None | N/A | **Yes — after EL approves this entry and QA test assertion is authored; consistent treatment with #1178 recommended** |

**Implementation sequencing for G10:**

1. EL approves this entry document
2. QA test assertions authored for all five issues — may be authored in batch (one spec extension or one new file covering all five) and committed to `release/m16` in a single PR before any implementation opens
3. All five fix PRs may proceed in parallel after test authorship — no sequential dependency between issues within G10. Recommended batch: #1178 and #1184 together (badge legibility — same component pattern); #1177 and #1179 together (trajectory annotation — same rendering context); #1162 independently
4. Each PR targets `release/m16` with a milestone-scoped branch name (e.g., `fix/m16-g10-zone1a-attribution-anchor`, `fix/m16-g10-milestone-year-anchor`)
5. Frontend pre-push build gate mandatory before each push: `cd frontend && npm run build` must exit 0
6. All G10 PRs follow the autonomous merge protocol: poll CI until all checks are terminal (pass or skipped, none failed), then `gh pr merge <number> --merge`
7. Once all five issues are confirmed merged, the implementing agent reports to the PM Agent and PI Agent for G8 scheduling gate confirmation

**G8 gate effect:** G8 (#843) may not be scheduled until this step 7 confirmation is recorded. The PI Agent's G8 scheduling gate check must include explicit confirmation that all five G10 issues are closed.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-24
**Sweep period:** M16 G9 sprint entry filing (2026-06-24) through G10 sprint entry filing (2026-06-24)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| Five CA-condition pre-demo issues (#1162, #1177, #1178, #1179, #1184) were named in three PI Agent sprint exit confirmations (G1, G3, G4) as required before the live session, but held no sprint group assignment, no sprint entry, no sequencing declaration, and no explicit slot in the sprint plan Sprint Groups table. The sprint plan exit conditions did not name them. Between G1 exit (2026-06-23) and this entry (2026-06-24), these five items existed as informal obligations documented only in prose confirmations — not in the plan's structured group list. Any agent reading the sprint plan alone would not know they exist or that they gate G8. Root cause: the CA assessment → issue-filing pattern was established in the SOP but the SOP did not require that CA-condition issues be assigned to a sprint group before the next group entry is filed. Fix: G10 entry formalizes this group; sprint plan amended. Severity: LOW — gap existed for one calendar day; no implementation was blocked; the PI Agent exit confirmations consistently named the issues. | process gap — low severity | PI Agent register call: this finding should be assessed for NM entry — the process gap (CA-condition issues unassigned to a sprint group) is a systemic pattern risk if not formalized. Recommend PI Agent determine whether to file as NM or as a SOP amendment note. | TBD — PI Agent determination |

---

## EL Approval Record

**EL approval:** 2026-06-24

> G10 sprint entry approved. Structural gates confirmed clear. No ADR prerequisites for any G10 issue; all five fixes are within existing component boundaries. Classification accepted: all five are user-facing; §3.1 observable state declarations serve as the intent specification (no separate intent document files required) — scope is explicitly bounded to the minimum fix the CA condition names and must not expand beyond that boundary without a sprint entry amendment. QA test assertions are required before each implementation PR opens; extending existing G1/G3/G4 spec files is permitted. G8 gate effect noted and accepted: #843 may not be scheduled until all five G10 issues are confirmed merged and the implementing agent records completion with the PI Agent. Near-miss sweep finding noted — PI Agent to determine whether the CA-condition orphaning gap warrants an NM entry or a SOP amendment note. Work may begin per §4 sequencing, after QA assertions are authored.
> — @PublicEnemage (2026-06-24)
