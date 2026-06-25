---
name: m16-g5-sprint-entry
type: sprint-entry
milestone: M16 — Distributional Visibility
sprint-group: G5
status: EL Approved 2026-06-23 — work may begin per priority order (#1145 first; #837/#951/#259 parallel, capacity-allowing)
authored-by: PM Agent
authored-date: 2026-06-23
el-approved: 2026-06-23
release-branch: release/m16
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M16, G5: Process + Secondary Features

**Status:** EL Approved 2026-06-23 — work may begin per priority order (#1145 first; #837/#951/#259 parallel, capacity-allowing)
**Date authored:** 2026-06-23
**Release branch:** `release/m16`
**Sprint plan:** `docs/process/sprint-plans/m16-sprint-plan.md` (EL Approved 2026-06-23)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G5 specifically. G5 is a Wave 1 parallel track — no sequential dependency
on G1, G2, G3, G4, G6, or G8. G5 issues touch documentation, process, and tooling only;
no frontend component conflicts. None of the G5 issues are on the Demo 6 critical path or
the G8 gate. Per the BPO sprint plan consultation: if capacity must be cut, cut G4
distributional infrastructure first, then G5 secondary features — never G1/G2/G3/G8.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M16 — Distributional Visibility |
| GitHub Milestone | #17 |
| Sprint group | G5 — Process + Secondary Features |
| Release branch | `release/m16` |
| Sprint plan document | `docs/process/sprint-plans/m16-sprint-plan.md` |
| Exit checklist issue | #985 |
| Sprint groups in scope | G5 only |
| ADR gate | None |
| Implementing agents | EL (authoring #1145); PM Agent (#837); PI Agent (#951); Technical Standards Agent (#259) |
| Wave | Wave 1 — parallel with G1 from day one; no sequential dependency on any other group |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any G5 work begins.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m16` cut from `main` 2026-06-23 (commit 07c92b8)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at kickoff 2026-06-23 (line 5: `branches: [ main, develop, release/m* ]`;
  line 7: `branches: [ main, release/m* ]`). Ruleset ID 17751852 with 6 required checks:
  `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
  KI-005 permanent fix (`do_not_enforce_on_create: true`) applied 2026-06-20 — no Ruleset
  workaround required for this or future release branches.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m16-sprint-plan.md`
  `el-approved: 2026-06-23` (PR #1148 merged 2026-06-23)

### 2.2 — ADR prerequisite gate

G5 contains no items requiring a new ADR. All four issues are documentation, process, and
tooling changes with no new application surface:

- **#1145** — addition to `docs/vision/worldsim-founding-document.md`; governing document
  update that makes implicit constraints explicit; no new architectural surface
- **#837** — configuration refactor of `scripts/demo.sh` and the narrated Playwright spec;
  within the existing demo preparation standard; no new application surface or API
- **#951** — process document edit to `docs/process/demo-preparation-standard.md §Step 6b`;
  no code changes; no new application surface
- **#259** — CTO legibility metrics infrastructure; CI step addition and documentation
  at milestone exit; no new application surface

The sprint plan Architect consultation confirms G5 is in the "None" row of the ADR
prerequisites table.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G5 — #1145 (founding document addition) | None | N/A | **CLEAR** |
| G5 — #837 (configuration-driven demo scripts) | None | N/A | **CLEAR** |
| G5 — #951 (solo-use review protocol) | None | N/A | **CLEAR** |
| G5 — #259 (CTO legibility metrics dashboard) | None | N/A | **CLEAR** |

- [x] No ADR prerequisites for G5. Gate: **CLEAR**.

### 2.3 — Intent document gate

G5 contains no user-facing deliverables in the UX persona sense. All four issues produce
documentation, process, or tooling changes that do not create or modify application surfaces
visible to any of the five primary personas in the running application. Observable states
for each issue are document-level (file existence, content presence) or tooling-level
(script behavior), not application-level.

*Infrastructure sprint — no user-facing deliverables — intent documents not required.*

Each issue's observable state is specified in Section 3.1. A PR for any G5 issue must
satisfy the stated observable state before merging; the observable state serves as the
acceptance criterion without requiring a separate intent document artifact.

### 2.4 — QA test authorship gate

G5 produces no Playwright E2E application states and no backend API behaviors requiring a
test file. #1145 is EL-authored and verified by EL review before the PR opens. For #837,
#951, and #259, observable states are verified in-PR by the implementing agent using file
existence, content presence (grep), and script execution checks appropriate to each issue.

*Infrastructure sprint — no user-facing deliverables — test authorship gate not required.*

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

G5 issues are ordered by horizon label. #1145 (`horizon:immediate`) is the highest priority
and must ship in M16 regardless of capacity pressure. The remaining three items
(`horizon:near-term`) are capacity-allowing secondary features that may be deferred to M17
if M16 capacity is constrained — in priority order: #837, #951, #259.

---

**Immediate — #1145**

| Issue | Title | Priority | Observable state (pre-implementation specification) |
|---|---|---|---|
| #1145 | docs(founding): add AC-001 and AC-002 as explicit permanent constraints in founding document | immediate / HIGH | `docs/vision/worldsim-founding-document.md §Open Source as Strategy` (or a clearly labelled subsection within it) contains all of: (1) AC-001 named as an explicit permanent prohibition — private, proprietary, or ministry-owned data inputs are architecturally prohibited — with the rationale that reproducibility by both parties requires both parties to inspect the same public sources; (2) AC-002 named as an explicit standing permission with conditions — synthetic estimates from comparable economies, regional distributions, and historical patterns are permitted, with mandatory indicator-level disclosure, T3 confidence tier floor, and meaninglessness threshold suppression; (3) both constraints identified as permanent architectural constraints (not strategic commitments or guidelines), so that a contributor reading the founding document understands the full data input architecture without separately consulting `docs/architecture/constraints.md`. EL-authored — PR opened and self-reviewed by EL before merging to `release/m16`. |

---

**Near-term — capacity-allowing; priority order: #837, #951, #259**

| Issue | Title | Priority | Observable state (pre-implementation specification) |
|---|---|---|---|
| #837 | feat(demo): configuration-driven demo scripts | near-term / MEDIUM | `scripts/demo.sh --milestone N` (where N is a milestone number, e.g., `16`) executes without error and produces presenter guide output derived from the corresponding milestone's demo documents (`docs/demo/m{N}/stakeholder-walkthrough.md` and `docs/demo/m{N}/screenshot-brief.md`). The hardcoded M10 Argentina content no longer appears in `scripts/demo.sh` or `frontend/tests/e2e/demo-narrated.spec.ts` outside of historical demo directories. `--milestone N` is the sole input required to switch demo cycles; no in-place content edit of either file is required to run a new milestone's demo. At minimum `--milestone 16` succeeds on the M16 demo documents; the general parameterisation pattern is in place for future milestones. |
| #951 | process: solo-use review protocol | near-term / MEDIUM | `docs/process/demo-preparation-standard.md §Step 6b` (or an added subsection within it) contains a named solo-use gate specifying all of: (1) at least one Step 6b panel reviewer must evaluate screenshots without reading the walkthrough first; (2) findings from this reviewer are tagged `[SOLO]` in the finding format; (3) a CRITICAL or HIGH solo-use finding blocks Step 7 under the same three-condition criteria as all other Step 6b findings; (4) the Customer Agent (Layer 3 usability — non-specialist user without specialist mediation) is the designated solo-use reviewer, consistent with their existing Step 6b lens. |
| #259 | standards: CTO legibility metrics dashboard | near-term / LOW | A legibility section is added to the M16 exit checklist (or to `docs/standards/legibility-baseline-m16.md` as a milestone-close artifact) recording the Tier 1 tolerance thresholds from issue #259 (mean cognitive complexity green/yellow/red, p90 function length, silent failure surface count, test-to-implementation ratio). At minimum: the tolerance threshold table and current-milestone values are documented in a named file accessible from the exit checklist. If a CI step is added, it runs without error on the current codebase. The Tier 2 and Tier 3 metrics (blind audit, assumption documentation rate) are out of scope for M16 and are noted as qualitative / future work. |

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| #845, #1147 — Zone 1A Phase 4 + Zone 1D delta annotations | G1 scope — sequential prerequisite for G2; frontend implementation |
| #986, #987 — distributional surface (cohort + political risk) | G2 scope — requires G2 pre-conditions and G1 merge |
| #274 — 25-year human capital trajectory | G3 scope — requires CE feasibility assessment before sprint entry |
| #102, #275, #22 — distributional infrastructure | G4 scope — capacity-allowing; not Demo 6 critical path |
| #569 — MV-002 Mode 3 hardware validation | G6 scope — after G1/G2 primary surface changes |
| #3, #6 — governance | G7 scope — EL-action; separate entry |
| #843 — live stakeholder demo | G8 scope — M16 exit gate |
| #1145 comprehensive cross-document AC-001/AC-002 consistency sweep | #1145 is bounded to the `§Open Source as Strategy` founding document addition; a full audit of all downstream documents for AC-001/AC-002 consistency is a separate initiative |
| Full #837 Phase 2 automation (structured `demo-config.yml` generation tooling) | G5 scope is the CLI parameterisation (`--milestone N`) and content derivation from existing walkthrough and screenshot-brief documents; YAML generation tooling is a future phase if #837 is extended |
| #259 Tier 2/3 metrics — blind audit mean score, assumption documentation rate | Semi-automated and qualitative leading indicators; not CI-computable; tracked qualitatively and recorded in exit notes, not in automated tooling for M16 |
| Any new backend API endpoints | G5 contains no backend API changes |
| Any frontend application component changes | G5 contains no frontend application component changes — `frontend/tests/e2e/demo-narrated.spec.ts` is demo tooling, not an application component |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G5 — #1145 | None | N/A | **Yes — EL-action; no ADR prerequisite** |
| G5 — #837 | None | N/A | **Yes — after EL approves this entry document** |
| G5 — #951 | None | N/A | **Yes — after EL approves this entry document** |
| G5 — #259 | None | N/A | **Yes — after EL approves this entry document** |

**Implementation sequencing for G5:**

1. EL approves this entry document (this step)
2. All four G5 items may proceed in parallel after EL approval — no sequential dependency
   between G5 issues
3. **#1145 (EL-authored):** EL authors the AC-001/AC-002 addition to
   `docs/vision/worldsim-founding-document.md §Open Source as Strategy`; EL self-reviews
   the observable state before opening the PR; targets `release/m16` with a milestone-scoped
   branch name (e.g., `docs/m16-g5-founding-document-ac001-ac002`); autonomous merge after
   CI passes
4. **#837 (PM Agent):** PM Agent refactors `scripts/demo.sh` and `frontend/tests/e2e/demo-narrated.spec.ts`
   to accept `--milestone N`; derives content from M16 demo documents; verifies observable
   state (hardcoded M10 content absent; `--milestone 16` runs cleanly) before opening PR;
   targets `release/m16` with a milestone-scoped branch name
   (e.g., `feat/m16-g5-config-demo-scripts`)
5. **#951 (PI Agent):** PI Agent edits `docs/process/demo-preparation-standard.md §Step 6b`
   to add the named solo-use gate; verifies observable state (named solo-use gate present;
   `[SOLO]` tag defined; Customer Agent designated) before opening PR; targets `release/m16`
   with a milestone-scoped branch name (e.g., `docs/m16-g5-solo-use-review-protocol`)
6. **#259 (Technical Standards Agent):** Technical Standards Agent establishes the M16
   legibility metrics tracking entry (exit checklist legibility section or
   `docs/standards/legibility-baseline-m16.md`); records Tier 1 threshold table and
   current-milestone values; verifies observable state before opening PR; targets
   `release/m16` with a milestone-scoped branch name
   (e.g., `docs/m16-g5-cto-legibility-dashboard`)
7. All G5 PRs follow the autonomous merge protocol: poll CI until all checks are terminal
   (pass or skipped, none failed), then `gh pr merge <number> --merge`

**G8 gate dependency:** None — G5 completion is not a gate on G8 (#843 live stakeholder
demo). G5 items may be in progress or complete concurrently with G1, G2, G3, and G8.

**Scope-cut authority:** If M16 capacity is constrained, G5 near-term items may be deferred
to M17 in priority order: #259 first, then #951, then #837. #1145 (`horizon:immediate`) must
ship in M16. Per the BPO sprint plan consultation: cut G4 before any G5 deferral.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-23
**Sweep period:** M15 exit ceremony (2026-06-23) through M16 G5 sprint entry filing (2026-06-23)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified. The G1 sprint entry sweep (same date, same session) covers the same period with no findings. No deviations from SOP occurred during M16 kickoff or G1/G7 sprint entry authorship. NM-056 (soft-skip masked AC-4 mock bug) is pre-existing and its follow-up action is registered in M16 exit conditions (sprint plan §Exit Conditions item 6) — no new NM required. | N/A | N/A | N/A |

---

## EL Approval Record

**EL approval:** 2026-06-23

> G5 sprint entry approved. Structural gates confirmed clear — release branch exists, CI trigger verified, sprint plan EL-approved. No ADR prerequisites for any G5 item; gate is clear across the board. Infrastructure sprint classification accepted: no intent document or QA test gate applies to any G5 item. Priority order accepted: #1145 (`horizon:immediate`) ships in M16 regardless of capacity; #837, #951, #259 (`horizon:near-term`) are capacity-allowing and may be deferred to M17 in order #259 → #951 → #837. Scope-cut authority noted: cut G4 before any G5 deferral. G5 is not on the G8 critical path. Work may begin.
> — @PublicEnemage (2026-06-23)
