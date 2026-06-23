---
name: m15-g5-sprint-entry
type: sprint-entry
milestone: M15 — Human Cost Architecture
sprint-group: G5
status: EL Approved 2026-06-22 — intent document and QA tests must be filed before implementation begins
authored-by: PM Agent
authored-date: 2026-06-22
el-approved: 2026-06-22
release-branch: release/m15
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M15, G5: Process Fixes + Walkthrough Updates

**Status:** EL Approved 2026-06-22 — intent document and QA tests must be filed before implementation begins
**Date authored:** 2026-06-22
**Release branch:** `release/m15`
**Sprint plan:** `docs/process/sprint-plans/m15-sprint-plan.md` (EL Approved 2026-06-20; amended 2026-06-21)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G5 specifically. G5 is a parallel track — no sequential dependency on G2,
G3, G4, G6, or G7. Five G5 items (#1067, #1083, #1088, #1089, #1090) gate G8: they must
be merged to `release/m15` before the G8 sprint entry is filed. No implementation PR may
open against `release/m15` for G5 until this entry document is EL-approved and the intent
and QA gates below are satisfied.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M15 — Human Cost Architecture |
| GitHub Milestone | #16 |
| Sprint group | G5 — Process Fixes + Walkthrough Updates |
| Release branch | `release/m15` |
| Sprint plan document | `docs/process/sprint-plans/m15-sprint-plan.md` |
| Exit checklist issue | #984 |
| Sprint groups in scope | G5 only |
| ADR gate | None — all G5 items are within accepted ADR scope or are process/infrastructure/documentation changes |
| Implementing agents | Frontend Architect Agent (#1007, #1083, #1067); UX Designer Agent (#1088, #1089, #1090); Chief Methodologist Agent (#1084); Backend / Data Architect Agent (#1048); Architect Agent (#1004) |
| Wave | Parallel (G1 ✅ complete 2026-06-21; G3 ✅ complete 2026-06-22; no sequential dependency on G2, G4, G6, G7) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G5.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m15` cut from `main` 2026-06-20 (commit 500e50d)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed 2026-06-20 (line 5: `branches: [ main, develop, release/m* ]`;
  line 7: `branches: [ main, release/m* ]`). Ruleset ID 17751852 with 6 required checks:
  `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
  KI-005 permanent fix (`do_not_enforce_on_create: true`) applied 2026-06-20.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m15-sprint-plan.md`
  `el-approved: 2026-06-20` (EL approval recorded 2026-06-20)

### 2.2 — ADR prerequisite gate

G5 contains no items requiring a new ADR. All frontend code changes (#1007, #1083) are
bug fixes within existing application surfaces — no new surface, no new architecture.
#1067 (screenshot fix) is a demo artifact production task targeting the existing application.
Documentation changes (#1004, #1084, #1088, #1089, #1090) are process, methodology, and
walkthrough documents. The Docker migration fix (#1048) is infrastructure. None of these
require a new ADR.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G5 — #1007 (recompute-badge) | None — UI bug fix, no new surface | N/A | **CLEAR** |
| G5 — #1083 (date label) | None — UI formatting fix, within ADR-016 Component 2 scope | ADR-016 ✅ accepted 2026-06-16 | **CLEAR** |
| G5 — #1067 (screenshot fix) | None — demo artifact production | N/A | **CLEAR** |
| G5 — #1048 (Docker migrations) | None — infrastructure | N/A | **CLEAR** |
| G5 — #1004, #1084, #1088, #1089, #1090 | None — documentation / process | N/A | **CLEAR** |

- [x] All G5 ADR prerequisites are clear. No new ADR required for any G5 item. Gate: **CLEAR**.

### 2.3 — Intent document gate

*An intent document must be filed before any G5 implementation PR opens.
(Authority: docs/process/agent-execution-lifecycle.md Step 1)*

G5 contains two categories of deliverables with different observable-state forms:
- **Frontend code + demo artifacts** (#1007, #1083, #1067): user-facing application changes
  requiring observable application states in the running application
- **Documentation + process changes** (#1048, #1004, #1084, #1088, #1089, #1090): analogous
  to M14 G7 governance/onboarding sprint — observable states are document-level
  (file-existence and content-presence), not application-level

Both categories are covered by a single combined intent document.

- [ ] Intent document filed — **MUST FILE BEFORE IMPLEMENTATION PR OPENS**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #1007 — recompute-badge not visible after apply-control-change | None (UI bug fix) | `docs/process/intents/M15-G5-2026-06-22-process-fixes.md` | No — BLOCKING |
| #1083 — Grounding strip date label "2024-Q1" → "Apr 2024" | ADR-016 §Component 2 | (same intent document) | No — BLOCKING |
| #1067 — Frame B and C are same screenshot (IR-003) | None (demo artifact) | (same intent document) | No — BLOCKING |
| #1048 — Docker API container Alembic migrations (NM-049) | None (infrastructure) | (same intent document) | No — BLOCKING |
| #1004 — Visual Spec section for intent template | None (process document) | (same intent document) | No — BLOCKING |
| #1084 — PSP historical calibration anchor (DEMO-127) | None (methodology documentation) | (same intent document) | No — BLOCKING |
| #1088 — Walkthrough "0 consecutive steps" plain language (DEMO-123) | None (documentation) | (same intent document) | No — BLOCKING |
| #1089 — Walkthrough Grounding strip persistence note (DEMO-124) | None (documentation) | (same intent document) | No — BLOCKING |
| #1090 — Walkthrough methodology documentation URL (DEMO-129) | None (documentation) | (same intent document) | No — BLOCKING |

**Completeness gate — frontend items (#1007, #1083, #1067):** The QA Lead must be able to
write a Playwright test for each deliverable's acceptance criterion without reading any
implementation code. An AC that requires reading the implementation to know what to assert
is incomplete and blocks Step 2.

**Completeness gate — documentation items (#1048, #1004, #1084, #1088–#1090):** The QA Lead
must be able to write a file-existence or content-presence check against the intent document's
acceptance criteria without reviewing any authored content in draft. Each AC must specify a
testable property: a file path, a grep pattern, or a command exit code.

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before implementation
code is written. (Authority: docs/process/agent-execution-lifecycle.md Step 2)*

G5 uses two test files matching its two deliverable categories:
- `frontend/tests/e2e/m15-g5-process-fixes.spec.ts` — Playwright E2E tests for frontend code
  and demo artifact deliverables (#1007, #1083, #1067)
- `backend/tests/test_m15_g5_process_fixes.py` — pytest file-existence + content-presence
  + infrastructure tests for documentation and backend deliverables (#1048, #1004, #1084,
  #1088, #1089, #1090)

- [ ] Both QA test files authored before implementation begins — **MUST FILE BEFORE IMPLEMENTATION PR OPENS**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| #1007 — recompute-badge | `docs/process/intents/M15-G5-2026-06-22-process-fixes.md` | `frontend/tests/e2e/m15-g5-process-fixes.spec.ts` | No — BLOCKING |
| #1083 — date label fix | (same) | `frontend/tests/e2e/m15-g5-process-fixes.spec.ts` | No — BLOCKING |
| #1067 — screenshot distinctness | (same) | `frontend/tests/e2e/m15-g5-process-fixes.spec.ts` | No — BLOCKING |
| #1048 — Docker migrations | (same) | `backend/tests/test_m15_g5_process_fixes.py` | No — BLOCKING |
| #1004 — intent template Visual Spec | (same) | `backend/tests/test_m15_g5_process_fixes.py` | No — BLOCKING |
| #1084 — PSP calibration anchor | (same) | `backend/tests/test_m15_g5_process_fixes.py` | No — BLOCKING |
| #1088 — walkthrough DEMO-123 | (same) | `backend/tests/test_m15_g5_process_fixes.py` | No — BLOCKING |
| #1089 — walkthrough DEMO-124 | (same) | `backend/tests/test_m15_g5_process_fixes.py` | No — BLOCKING |
| #1090 — walkthrough DEMO-129 | (same) | `backend/tests/test_m15_g5_process_fixes.py` | No — BLOCKING |

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

G5 issues are organized into three priority tiers. The first tier gates G8; the second must
complete within G5 but does not block the G8 sprint entry; the third is addressed as capacity
allows.

---

**Tier 1 — Gates G8: must merge to `release/m15` before G8 sprint entry is filed**

| Issue | Title | Priority | Observable state (pre-implementation specification) |
|---|---|---|---|
| #1067 | demo(screenshots): Frame B and C are same screenshot (IR-003) | immediate / HIGH | `docs/demo/m15/screenshots/` contains exactly five image files (frame-a through frame-e). No two files are byte-identical: `md5sum docs/demo/m15/screenshots/frame-*.png` produces five distinct hashes. Frame B and Frame C each depict visually distinguishable content: different step positions, different Zone visibility, or different UI state. A non-technical stakeholder shown both frames side-by-side can identify — without presenter explanation — what is different. |
| #1083 | ux(grounding-strip): date label "2024-Q1" → "Apr 2024" | near-term / MEDIUM | In the running application at 1440×900 with the ZMB ECF scenario loaded, the Grounding strip renders the initial-state date reference in "Mmm YYYY" format — e.g., "Apr 2024" — not "YYYY-QN" format. Playwright: `expect(page.locator('[data-testid="grounding-strip-date"]')).not.toContainText(/\d{4}-Q\d/)` passes; `toContainText("Apr 2024")` (or the locale-correct equivalent) also passes. Applies to all entities with a quarterly-expressed reference date in `initial_state`. |
| #1088 | docs(demo): walkthrough — "0 consecutive steps" plain language (DEMO-123) | near-term / MEDIUM | `docs/demo/m15/stakeholder-walkthrough.md` exists and contains no instance of the raw phrase "0 consecutive steps" in presenter narration. Where the consecutive-steps count is explained, the walkthrough uses plain language accessible to a non-technical stakeholder (e.g., "If the breach just started at this step, the panel will show '1 consecutive step'"). Backend test: `grep -c "0 consecutive steps" docs/demo/m15/stakeholder-walkthrough.md` returns 0. |
| #1089 | docs(demo): walkthrough — Grounding strip persistence note (DEMO-124) | near-term / MEDIUM | `docs/demo/m15/stakeholder-walkthrough.md` contains an explicit presenter note in the Grounding strip narration section explaining that the strip shows the scenario's *entry-state* data, which is fixed and does not update as steps advance, and that the current simulated value appears in Zone 1B and the trajectory view — not in the strip anchor. Backend test: `grep -c "entry-state" docs/demo/m15/stakeholder-walkthrough.md` returns ≥1 in context of the Grounding strip. |
| #1090 | docs(demo): walkthrough — methodology documentation URL (DEMO-129) | near-term / LOW | `docs/demo/m15/stakeholder-walkthrough.md` contains at least one reference to the methodology documentation path — either `docs/onboarding/methodology-overview.md` or a public-facing equivalent — in the section where model calibration or methodology is discussed, enabling the presenter to direct a participant to the source directly. Backend test: `grep -c "methodology" docs/demo/m15/stakeholder-walkthrough.md` returns ≥1 in context of a named document or URL path. |

*Note on walkthrough path: `docs/demo/m15/stakeholder-walkthrough.md` does not yet exist.
G5 creates this file as a preliminary M15 walkthrough derived from `docs/demo/m14/stakeholder-walkthrough.md`
with the three DEMO-123/124/129 fixes applied. G8 will extend it with M15-specific features
when preparing for the live external demo (#843). G8 must not overwrite the three fixes
established by G5.*

---

**Tier 2 — Primary scope: must complete within G5; do not gate G8 sprint entry**

| Issue | Title | Priority | Observable state (pre-implementation specification) |
|---|---|---|---|
| #1007 | fix: recompute-badge not visible after apply-control-change | near-term / MEDIUM | In the running application at 1440×900 with a ZMB ECF scenario loaded and ≥1 step advanced, after the user changes a control value (e.g., `fiscal_multiplier`) and clicks "Apply", an element with `data-testid="recompute-badge"` (or equivalent pending-recompute indicator) is visible without requiring a page reload or additional interaction. The badge remains visible until the user advances to the next step. Playwright: after `click('[data-testid="apply-control-change"]')`, `locator('[data-testid="recompute-badge"]').isVisible()` returns true. Before the apply action, the badge must not be visible (verifies that the badge correctly indicates pending state). |
| #1048 | infra: Docker API container Alembic migrations (NM-049) | near-term / MEDIUM | Starting from a clean Docker environment (`docker compose down -v && docker compose up --build`), the API container log output shows all Alembic migrations applied without errors before the first API request is served. A `GET /api/v1/health` call to the running container returns HTTP 200. A `GET /api/v1/entities` call returns HTTP 200 with at least one entity (not a 500 error from an unapplied migration). Backend test: `test_migrations_applied_at_startup` makes an httpx call to a Docker-started container and asserts HTTP 200 on both endpoints. |
| #1084 | methodology: PSP historical calibration anchor (DEMO-127) | near-term / MEDIUM | A file at `docs/methodology/psp-calibration-anchor.md` exists and contains all of: (1) the name of at least one historical IMF ECF programme with a known compliance outcome, (2) the country, programme start year, and ECF arrangement type, (3) the documented compliance outcome (on-track / off-track / collapsed), and (4) a citation to at least one publicly available source (e.g., IMF Article IV Consultation report, ECF review, or Public Information Notice). Backend test: `find docs/methodology -name "psp-calibration-anchor.md"` exits 0; content-presence checks for "ECF", a country name, and "compliance". |
| #1004 | process: Visual Spec section for intent template | near-term / MEDIUM | `docs/process/intent-template.md` contains a section titled `## Visual Specification` (or `§Visual Specification`) that specifies: (1) when a Visual Spec is required vs. optional for frontend deliverables, (2) the minimum required fields (element selector or `data-testid`, viewport, expected visual property or text content), and (3) at least one concrete example drawn from a prior intent document. Backend test: `grep -c "Visual Spec" docs/process/intent-template.md` returns ≥1; `grep -c "data-testid" docs/process/intent-template.md` returns ≥1 (verifies example contains a selector). |

---

**Tier 3 — Tertiary scope: address as capacity allows within G5; no gate on G8 or G5 exit**

| Issue | Title | Priority | Notes |
|---|---|---|---|
| #837 | feat(demo): configuration-driven demo scripts | near-term | `demo.sh` parameterised by scenario slug so any supported entity can be used without file edits. Lower priority — M15 demo can use current hardcoded approach if G5 capacity is insufficient. |
| #951 | process: solo-use review protocol | near-term | Migrated from M14. Documents review protocol for solo Engineering Lead sessions where independent agent review is structurally unavailable. Process document only; no code changes. |
| #259 | standards: CTO legibility metrics dashboard | near-term | Standards documentation specifying legibility metrics tracked at sprint close. No code changes. |

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| #1065, #1066, #1068, #1069, #1075 | ✅ G1 — complete 2026-06-21; all five Layer 3 IR fixes merged and BPO accepted |
| #986, #987 | ✅ G3 — complete 2026-06-22; cohort disaggregation and political risk summary design documents merged PR #1109 |
| #845 (Zone 1A ADR-017) | G2 scope — Architecture Review (ARCH-REVIEW-007) + ADR-017 authorship |
| #975 (Path 1 approved source network) | G4 scope |
| ADR-016 Component 3 (Fidelity panel) | G4 scope |
| #990 (accessibility validation) | G6 scope |
| #1091, #3, #6 | G7 scope — CLAUDE.md extraction and governance items |
| #843 (live external demo) | G8 scope — M15 exit gate |
| #845 Phase 4 (Zone 1A implementation) | Out of M15 scope; separate sprint entry required; may extend to M16 |
| New backend API endpoints | G5 contains no new API surface — #1007 and #1083 are frontend-only; #1048 is migration infrastructure |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G5 — all items | None | N/A | **Yes — after EL approves this entry document and intent + QA gates are satisfied** |

No new ADR is required for any G5 item. G5 is bounded to bug fixes within existing surfaces,
demo artifact production, infrastructure, and documentation changes. The Grounding strip date
label fix (#1083) is within ADR-016 Component 2 scope (which is accepted); it is a formatting
fix, not a surface addition.

**Implementation sequencing for G5:**

1. EL approves this entry document
2. The relevant implementing agents co-author a single combined intent document at
   `docs/process/intents/M15-G5-2026-06-22-process-fixes.md` — must derive observable
   application states and document-level ACs from Section 3.1 above; Kryptonite Constraint
   Check (intent template §5) required for #1007 and #1083 (both affect Persona 2 and
   Persona 5 in the active control and Grounding strip workflows)
3. QA Lead authors both test files from the intent document — `frontend/tests/e2e/m15-g5-process-fixes.spec.ts`
   and `backend/tests/test_m15_g5_process_fixes.py` — before any implementation code is written;
   all ACs must be testable without reading any implementation code
4. Implementation PRs open targeting `release/m15` with milestone-scoped branch names
   (e.g., `feat/m15-g5-recompute-badge`, `feat/m15-g5-date-label`, `fix/m15-g5-screenshots`,
   `docs/m15-g5-walkthrough`)
5. Frontend Architect Agent Step 4 Verify: confirms observable application states for #1007,
   #1083, #1067 in the running application; documentation agents confirm file-existence and
   content-presence for Tier 1 and Tier 2 documentation items
6. Customer Agent Layer 3 assessment required for #1007 and #1083 — both affect the active
   control workflow visible to Persona 2 (Eleni, finance ministry negotiator) and Persona 5
   (Aicha, junior ministry analyst) during scenario preparation; the recompute-badge signals
   pending model output and must be self-interpreting without presenter mediation
7. Business PO Step 5 Validate: confirms all Tier 1 and Tier 2 primary-scope observable
   states are present; confirms screenshot frames B and C are visually distinct for demo
   narrative purposes; confirms the M15 walkthrough draft addresses DEMO-123, DEMO-124,
   DEMO-129 findings; timed navigation of `docs/methodology/psp-calibration-anchor.md`
   from the methodology overview in under five minutes (analogous to M14 G7 AC-7)

**G8 gate dependency:** The G8 sprint entry must not open until all five Tier 1 items
(#1067, #1083, #1088, #1089, #1090) are merged to `release/m15`. These items ensure that
the M15 demo screenshots are visually distinct per the demo narrative, the Grounding strip
date format is plain-language, and the preliminary M15 walkthrough does not contain the three
narration issues identified in the M14 simulated stakeholder session (G8 Step 9, 2026-06-20).
Real external participants must not encounter these issues at the live demo.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-22
**Sweep period:** Since M15-G2 sprint entry filed (2026-06-21) through G5 sprint entry
authorship (2026-06-22)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| NM-052 — Pre-push mypy gate non-executable locally: Python 3.13 venv with deps absent from dev environment; gate silently degraded to CI-only since M8. Permanent fix applied in PR #1108 (`feat/m15-nm052-mypy-gate`). | Near-miss (anticipatory) | Yes — NM-052 filed and resolved (PR #1108 merged to `release/m15`) | NM-052 |
| NM-049 — Docker API container Alembic migrations not applied at startup in dev stack. Pre-existing; filed during M14 G3 Step 4 Verify. Issue #1048 in G5 Tier 2 is the implementation fix. | Near-miss (reactive; pre-existing) | Yes — NM-049 filed (pre-existing); #1048 is the registered fix vehicle | NM-049 (pre-existing) |

No additional process gaps identified in the sweep period. G3 design documents (cohort
disaggregation + political risk summary design, PR #1109) merged without new process
deviations. ARF + CM sign-off pending for G3 is in-process and expected state — not a
near-miss. G4 sprint entry filed and EL-approved 2026-06-22 without new deviations.

---

## EL Approval Record

**EL approval:** 2026-06-22

> G5 sprint entry approved. Structural gates confirmed clear — release branch exists, CI trigger verified, sprint plan EL-approved. No ADR prerequisites for any G5 item; gate is clear across the board. Three-tier scope structure accepted: Tier 1 (five items gating G8: #1067, #1083, #1088, #1089, #1090) must merge before the G8 sprint entry is filed; Tier 2 (#1007, #1048, #1084, #1004) must complete within G5 but do not block G8; Tier 3 (#837, #951, #259) proceeds as capacity allows. The walkthrough approach is accepted — G5 creates `docs/demo/m15/stakeholder-walkthrough.md` as a preliminary document with DEMO-123/124/129 fixes applied; G8 extends it and must not overwrite those fixes. Observable application states in Section 3.1 are specific enough to gate QA test authorship. Intent document at `docs/process/intents/M15-G5-2026-06-22-process-fixes.md` and both QA test files must be filed before any implementation PR opens — these remain blocking conditions.
> — @PublicEnemage (2026-06-22)
