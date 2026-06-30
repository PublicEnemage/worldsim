---
name: m18-g7-sprint-entry
type: sprint-entry
milestone: M18 — Full Argument and Demo 7
sprint-group: G7 — Demo 7 Continuation (Step 6b Remediation through Live Session)
status: EL-APPROVED — 2026-06-29
authored-by: PM Agent
authored-date: 2026-06-29
el-approved: 2026-06-29
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M18, G7: Demo 7 Continuation

**Status:** EL-APPROVED — 2026-06-29 (@PublicEnemage)
**Date authored:** 2026-06-29
**Release branch:** `release/m18`
**Sprint plan:** `docs/process/sprint-plans/m18-sprint-plan.md` (EL-approved 2026-06-26)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate`.
G7 is the Demo 7 continuation sprint. It carries all Step 6b findings (DEMO-130 through
DEMO-153) from the G6 internal review, resolves or disposes each, re-runs the nine-agent
Step 6b panel, and — if the re-review returns PASS — advances through the remaining demo
preparation steps (Step 7 IR, Step 6c audience simulation, Step 8 triage, Step 9 live
session, Step 9b recording upload) to close the demo and gate M18 exit.*

*G7 implements structural fixes across rendering (CI band geometry), layout (Zone 1B height
budget), component design (CohortImpactSection monitored-row state), and data pipeline
(psp-driver-row fixture, Human Cost Ledger indicator key). These are not isolated patches —
they constitute a coherent remediation of the demo instrument's presentation layer. The
sprint process's intent documents, QA authorship gates, and Architecture/UX sign-offs are
load-bearing here, not ceremonial.*

---

## G7 Entry Preconditions

The following must be true before any G7 implementation PR opens:

1. G6 exit document filed and PI Agent confirmed (`docs/process/sprint-plans/m18-g6-sprint-exit.md`)
2. G6 integration PR (`sprint/m18-g6` → `release/m18`) merged and CI green
3. `sprint/m18-g7` cut from `release/m18` AFTER G6 integration PR merges
4. Root cause analysis document (Step G7-0) filed and EL-reviewed before any fix intent documents are authored
5. This entry EL-approved

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| GitHub Milestone | #19 |
| Sprint group | G7 — Demo 7 Continuation |
| Release branch | `release/m18` |
| Sprint plan document | `docs/process/sprint-plans/m18-sprint-plan.md` |
| Exit checklist issue | #1340 (M18 closure gate — closes when #843 closes) |
| Sprint journal issue | TBD — PM Agent opens at G7 entry |
| DEMO-NNN namespace | Next available: DEMO-154 (DEMO-130–DEMO-153 assigned in G6 Step 6b review) |
| Wave coordination tier | Standard (G7 is sole active group at entry; G1–G6 all closed) |
| Concurrent groups at entry | 0 |
| Cross-group dependencies | G7 requires G6 integration PR merged to release/m18 before sprint/m18-g7 is cut |

---

## Section 2 — Entry Invariants Checklist

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m18` — cut 2026-06-26 at commit 151904d
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` — confirmed at M18 kickoff
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m18-sprint-plan.md` — EL-approved 2026-06-26
- [x] **G6 integration PR merged:** PR #1479 `sprint/m18-g6` → `release/m18` — MERGED 2026-06-29T23:42Z; all CI checks SUCCESS
- [x] **G6 exit confirmed by PI Agent:** `docs/process/sprint-plans/m18-g6-sprint-exit.md` — CONFIRMED 2026-06-29; sprint journal #1475 closed

### 2.2 — ADR prerequisite gate

G7 fixes are implementation corrections within the scope of existing ADRs. No new ADR is
anticipated at entry. However, two fixes may require ADR amendments pending root cause analysis:

| Fix cluster | Potential ADR impact | Gate |
|---|---|---|
| Zone 1B layout (Cluster B) | May require ADR-008 amendment if Zone 1B height-budget allocation is newly specified | Architect Agent determines at Step G7-0 before fix intent is authored |
| CohortImpactSection design (Cluster C) | May require UX Designer sign-off block in ADR-010 if monitored-row state constitutes a new instrument contract | UX Designer + Architect determine at Step G7-0 |
| CI band geometry (Cluster A) | Bug fix within ADR-007 spec — no new ADR expected | CLEAR |
| Data pipeline (Cluster D) | Bug fix — no ADR impact | CLEAR |

- [ ] **ADR prerequisite determination:** Architect Agent produces determination at Step G7-0. If amendments required, they are filed and accepted before the relevant fix cluster's implementation PR opens.

| Fix cluster | ADR impact | Gate |
|---|---|---|
| A — CI band geometry | None expected (ADR-007 fix) | CLEAR pending G7-0 |
| B — Zone 1B layout | Possible ADR-008 amendment | BLOCKED pending G7-0 determination |
| C — CohortImpactSection design | Possible ADR-010 UX sign-off | BLOCKED pending G7-0 determination |
| D — Data pipeline | None | CLEAR |
| E — Capture/narration/label fixes | None | CLEAR |

### 2.3 — Intent document gate

Each fix cluster must have an intent document filed before its implementation PR opens.
The root cause analysis (Step G7-0) determines the exact scope of each intent document.

- [ ] Intent documents filed for all fix clusters before the relevant implementation PR opens (not before entry — sequencing is G7-0 → per-cluster intent → QA tests → implementation)

**Intent document plan (to be completed after G7-0):**

| Fix cluster | Issues in scope | ADR reference | Intent document path | Filed? |
|---|---|---|---|---|
| A — CI band geometry | DEMO-137 (#1466); DEMO-138 (#1467); DEMO-145 (#1474) | ADR-007 | `docs/process/intents/M18-G7-A-{date}-ci-band-geometry.md` | ⏳ Pending G7-0 |
| B — Zone 1B layout | DEMO-131 (#1460); DEMO-133 (#1462); DEMO-141 (#1470) | ADR-008; possible amendment | `docs/process/intents/M18-G7-B-{date}-zone1b-layout.md` | ⏳ Pending G7-0 |
| C — CohortImpactSection | DEMO-134 (#1463); DEMO-140 (#1469) | ADR-010; possible UX sign-off | `docs/process/intents/M18-G7-C-{date}-cohort-section-design.md` | ⏳ Pending G7-0 |
| D — Data pipeline | DEMO-132 (#1461); DEMO-143 (#1472) | None (bug fix) | `docs/process/intents/M18-G7-D-{date}-data-pipeline-psp-hcl.md` | ⏳ Pending G7-0 |
| E — Capture and narration | DEMO-130/135/136/139/142/144/146 (#1459/1464/1465/1468/1471/1473/DEMO-146) | None (doc/spec fixes) | `docs/process/intents/M18-G7-E-{date}-capture-narration.md` | ⏳ Pending G7-0 |

### 2.4 — QA test authorship gate

QA tests must be authored from each intent document's acceptance criteria before implementation
code is written. For fix clusters A, B, C, D (code fixes): new or updated tests are required.
For cluster E (capture/narration doc fixes): `demo-narrated.spec.ts` re-validation is the test.

- [ ] QA tests authored for all code-fix clusters before implementation (sequenced after intent document, before implementation code)

**QA test plan (to be completed after intent documents):**

| Fix cluster | Test file | What must pass | Authored before implementation? |
|---|---|---|---|
| A — CI band geometry | `frontend/tests/e2e/demo-ci-band-geometry.spec.ts` (new) or `TrajectoryView.test.tsx` (unit) | CI band fill is `[mean - halfWidth, mean + halfWidth]` at each step; y-axis scales to trajectory range not CI ceiling; opacity constant applied correctly | ⏳ Pending intent |
| B — Zone 1B layout | `frontend/tests/e2e/demo-zone1b-layout.spec.ts` (new) | All six DistributionalComparisonSummary fields legible at 1440×900 without scroll; Zone 3 expanded panel content in viewport; comparison summary above TERMINAL alert | ⏳ Pending intent |
| C — CohortImpactSection | `frontend/tests/e2e/demo-cohort-section.spec.ts` (new) or unit test | Monitored cohort row visible at step 6 when threshold is not crossed; T3 tier badge; floor value rendered; current value rendered; temporal scope labels for current vs. historical | ⏳ Pending intent |
| D — Data pipeline | `backend/tests/integration/test_m18_g7_psp_hcl_fixture.py` (new) | `psp-driver-row` populates from SEN fixture at steps 3, 6, 8; Human Cost Ledger bottom quintile value non-null for both SEN and ZMB scenarios | ⏳ Pending intent |
| E — Capture/narration | `frontend/tests/e2e/demo-narrated.spec.ts` (updated) | Spec produces five distinct screenshots; Frame A at step 8; Frame B at step 3; no duplicate MD5s; choropleth centered on ZMB; walkthrough value matches simulation output | ⏳ Pending implementation |

### 2.5 — Prior NM verification

| NM entry | Process improvement required | Applied in G7? |
|---|---|---|
| NM-076 | Testid rename crosscheck against full E2E corpus before any rename | Yes — apply crosscheck if any testids change in fix clusters A/B/C |
| NM-077 | Explicit `--head` flag on `gh pr create` when operating across multiple worktrees | Yes — use `--head feat/m18-g7-*` explicitly |
| NM-078 | New backend test files in `backend/tests/integration/` not `backend/tests/` root | Yes — cluster D test file goes to `backend/tests/integration/` |

**New NM to be filed at G7 entry (PI Agent):**

> **NM-079 (candidate):** CI band fill geometry incorrect in `TrajectoryView.tsx`; G1 CI
> and demo legibility tests (16/16 PASS, 2026-06-28) did not detect the visual geometry
> error. The band extends to the chart ceiling rather than forming a ±half-width envelope.
> This shipped in G1, was captured in five demo screenshots, and was only detected by the
> nine-agent Step 6b visual review. Root cause: no unit test covers the CI fill geometry
> calculation; the legibility gate tests element presence, not geometric correctness.
> Process improvement: add CI band fill geometry to `TrajectoryView.test.tsx` unit test
> assertions as part of G7 Cluster A fix.

PI Agent files NM-079 in `docs/process/near-miss-registry.md` at G7 entry — this is a
pre-condition for the G7 entry gate to fully close.

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

**Carried from G6 Step 6b (defect resolution):**

| Issue | DEMO-NNN | Severity | Fix cluster |
|---|---|---|---|
| #1459 | DEMO-130 | CRITICAL | E — Capture: Frame B duplicate of Frame A |
| #1460 | DEMO-131 | CRITICAL | B — Zone 1B: Zone 3 panel content not in viewport |
| #1461 | DEMO-132 | CRITICAL | D — Data: `psp-driver-row` absent |
| #1462 | DEMO-133 | CRITICAL | B — Zone 1B: DistributionalComparisonSummary below fold |
| #1463 | DEMO-134 | CRITICAL | C — CohortImpactSection: informal workers row absent |
| #1464 | DEMO-135 | CRITICAL | E — Capture: Frame A at step 3 not step 8 |
| #1465 | DEMO-136 | CRITICAL | E — Capture: Frame C delta = 0.00 |
| #1466 | DEMO-137 | HIGH | A — CI band geometry bug |
| #1467 | DEMO-138 | HIGH | A (secondary): trajectories indistinguishable |
| #1468 | DEMO-139 | HIGH | E — Capture: choropleth on North America |
| #1469 | DEMO-140 | HIGH | C — CohortImpactSection: Zone 1B temporal contradiction |
| #1470 | DEMO-141 | HIGH | B — Zone 1B: TERMINAL alert above comparison summary |
| #1471 | DEMO-142 | HIGH | E — Label: "Policy Malevolent Margin" jargon |
| #1472 | DEMO-143 | HIGH | D — Data: Human Cost Ledger bottom quintile em dash |
| #1473 | DEMO-144 | HIGH | E — Narration: walkthrough value mismatch (340K vs ~342K) |
| #1474 | DEMO-145 | HIGH | A (secondary): CI band prominence inverted |
| DEMO-146 | — | MEDIUM | E — Doc: walkthrough filename table mismatch |
| DEMO-147 | — | MEDIUM | E — Narration: T3→T4 tier degradation unscripted |
| DEMO-148 | — | MEDIUM | E — Narration: 8 NARRATION-RULING-1 transitions missing |
| DEMO-149 | — | MEDIUM | B — Zone 1B: PSP section clipped in Act 2 |
| DEMO-150 | — | MEDIUM | D (secondary): Ecological framework value missing |
| DEMO-151 | — | MEDIUM | C (secondary): HD trajectory absent from Zone 1A |
| DEMO-152 | — | LOW | E — Label: breadcrumb shows only "OptionC" |
| DEMO-153 | — | LOW | E — Narration: Act 1 missing people-count translation |

**G7 demo completion steps (carried from G6):**

| Issue | Title | Priority |
|---|---|---|
| #843 | Demo 7 — live external session (Senegal Mode 3 + Zambia 3-scenario) | M18 gate issue |
| #1445 | Demo 7 preparation — v0.18.0 / M18 | Tracking |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Rationale |
|---|---|---|
| #1340 | M18 Exit Checklist | Closes when #843 closes — not a G7 deliverable, it is the exit gate |
| DEMO-150, DEMO-151 | Ecological value missing; HD trajectory absent from Zone 1A | Scope decision at G7-0: these are enhancement-class gaps, not demo-blocking; PI Agent and EL disposition at root cause analysis |

*Disposition decisions for MEDIUM/LOW findings (DEMO-146 through DEMO-153) are made at
Step G7-0. Some may be fixed in G7; some may be scoped to M19. All must receive an explicit
disposition decision — no finding is silently dropped.*

---

## Section 4 — Deliverable Sequence (G7 logical order)

G7 follows the same demo preparation standard but begins mid-sequence. The logical order
for G7 is:

| Step | Deliverable | Artifact path | Gate | Status |
|---|---|---|---|---|
| G7-0 | Root cause analysis and pattern document | `docs/demo/m18/reviews/YYYY-MM-DD-g7-root-cause-analysis.md` | EL-reviewed before any fix intent filed | ⏳ First step |
| G7-0b | Architect + UX sign-off on Clusters B and C | Comments on root cause doc or separate ADR amendments | Must precede intent docs for B and C | ⏳ After G7-0 |
| G7-A | Fix cluster A — CI band geometry | `frontend/src/components/TrajectoryView.tsx` | Intent + QA before implementation | ⏳ |
| G7-B | Fix cluster B — Zone 1B layout | `frontend/src/components/DistributionalComparisonSummary.tsx` + layout | Intent + QA + Arch/UX sign-off before implementation | ⏳ |
| G7-C | Fix cluster C — CohortImpactSection design | `frontend/src/components/CohortImpactSection.tsx` | Intent + QA + UX sign-off before implementation | ⏳ |
| G7-D | Fix cluster D — Data pipeline | Backend fixture + `FourFrameworkZone1D.tsx` / HCL binding | Intent + QA before implementation | ⏳ |
| G7-E | Fix cluster E — Capture, narration, label fixes | `demo-narrated.spec.ts`, `stakeholder-walkthrough.md`, component labels | Intent (combined) + spec update before re-capture | ⏳ |
| 6 (re-run) | Screenshot recapture — five frames | `docs/demo/m18/screenshots/frame-{a–e}-*.png` (replaced) | All CRITICAL fixes confirmed rendering before re-capture | ⏳ |
| 6b (re-run) | Step 6b re-review — nine-agent panel | `docs/demo/m18/reviews/YYYY-MM-DD-v0.18.0-internal-review-v2.md` | **GATE: all CRITICAL findings (#1459–#1465) resolved** | ⏳ |
| 7 | IR review — fresh Claude instance | `docs/demo/m18/reviews/YYYY-MM-DD-v0.18.0-ir-review.md` | **GATED: Step 6b re-review PASS + release/m18 → main by EL** | ⏳ |
| 6c | Audience simulation — Personas 1, 2, 3, 5 | `docs/demo/m18/reviews/YYYY-MM-DD-v0.18.0-audience-simulation.md` | **GATED: Step 7 complete; Persona 5 north star PASS gates Step 9** | ⏳ |
| 8 | DEMO-NNN triage + stakeholder review placeholder | GitHub issues; `docs/demo/m18/reviews/PENDING-v0.18.0-stakeholder-review.md` | CRITICAL resolved before Step 9 | ⏳ |
| 9 | Live stakeholder session | `docs/demo/m18/reviews/YYYY-MM-DD-v0.18.0-stakeholder-review.md` | **GATED: Persona 5 north star PASS + real external participants** | ⏳ — #843 gate |
| 9b | Screen recording upload | `gh release upload v0.18.0 recording.mp4` | Required — M18 is even-numbered | ⏳ |

---

## Section 5 — Near-Miss Sweep

**Sweep date:** 2026-06-29
**Sweep period:** Since G6 opened (2026-06-28)

| Finding | Category | PI Agent register call | NM entry |
|---|---|---|---|
| CI band fill geometry incorrect in `TrajectoryView.tsx`; shipped in G1 with CI and legibility tests green; detected only by Step 6b visual review; no unit test covers fill geometry calculation | Near-miss (reactive) | Yes — file NM-079 at G7 entry | NM-079 (to be filed) |
| CohortImpactSection designed as alert-only surface; non-breaching monitored cohorts invisible in primary viewport; the Act 1 human cost finding cohort disappeared from the demo without any test detecting the absence | Near-miss (reactive) | Yes — evaluate as NM-080 or as NM-079 sub-finding | TBD at G7-0 |

---

## Section 6 — Sprint Group Isolation

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m18-g7` |
| Cut from | `release/m18` AFTER G6 integration PR merges |
| Sprint journal issue | TBD — PM Agent opens at G7 entry after EL approval |

**PM Agent sprint sub-branch cut command** (run only after G6 integration PR merged):
```bash
git pull origin release/m18
git checkout -b sprint/m18-g7 release/m18
git push -u origin sprint/m18-g7
```

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors NM-079) | NM-079 at G7 entry |
| `docs/compliance/scan-registry.md` | PM Agent coordination lane | Compliance scan at G7 exit |
| `frontend/src/components/TrajectoryView.tsx` | Sprint sub-branch | Fix cluster A |
| `frontend/src/components/DistributionalComparisonSummary.tsx` | Sprint sub-branch | Fix clusters B, E |
| `frontend/src/components/CohortImpactSection.tsx` | Sprint sub-branch | Fix cluster C |
| `frontend/src/components/FourFrameworkZone1D.tsx` | Sprint sub-branch | Fix cluster D (psp-driver-row) |
| Backend fixture files | Sprint sub-branch | Fix cluster D |
| `frontend/tests/e2e/demo-narrated.spec.ts` | Sprint sub-branch | Fix cluster E + recapture |
| `docs/demo/m18/stakeholder-walkthrough.md` | Sprint sub-branch | Fix cluster E (narration) |
| `docs/demo/m18/screenshots/` | Sprint sub-branch | Screenshot recapture |

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes anticipated. All writes are to code, test, and documentation files.

#### 6.3a — New output paths

- [x] No new output directories introduced by G7 fix clusters.
New test files go into existing directories:
- `frontend/tests/e2e/` (new spec files for clusters A/B/C)
- `backend/tests/integration/` (cluster D backend test — NM-078 compliance: NOT `backend/tests/` root)

### 6.4 — Cross-group dependency declaration

- [x] G7 depends on G6: `sprint/m18-g7` must be cut from `release/m18` AFTER the G6 integration PR merges. This is stated in §G7 Entry Preconditions above.

No other cross-group dependencies (G7 is the sole active sprint group).

### 6.5 — Prior NM verification

| NM entry | Process improvement required | Applied in G7? |
|---|---|---|
| NM-076 | Testid rename crosscheck against E2E corpus | Yes — grep before any testid rename |
| NM-077 | Explicit `--head` flag on `gh pr create` in multi-worktree environment | Yes |
| NM-078 | New backend test files in `backend/tests/integration/` not `backend/tests/` root | Yes — cluster D test file goes to `backend/tests/integration/` |

---

## Section 7 — Customer Agent and North Star

| Field | Value |
|---|---|
| Customer Agent L3 required | Yes — Persona 5 (Aicha, Finance Minister) north star PASS at Step 6c gates Step 9. Persona 1 (Lucas) Zone 3 auditability re-assessment required after Cluster B fix. |
| North star test | Authored by Business PO at G7 exit after live session runs. Specific Zambia counter-proposal scenario naming: the finance minister scenario (Aicha, ZMB debt restructuring with IMF team); the capability evaluated (putting +342K persons on screen with CI bounds + methodology expandable in real time); whether the capability changes what the ministry team can argue at the table (yes: the IMF team must engage analytically with a specific differential, not dismiss it as a model output). |
| Serves Personas | 2 (Eleni — Finance Ministry Negotiator), 5 (Aicha — Finance Minister), 1 (Lucas — Analytical Economist), 3 (Andreas — Political Advisor) |

---

## EL Approval Record

**EL approval:** APPROVED — 2026-06-29 (@PublicEnemage)

The G7 sprint entry is approved as filed.

**Approval authorizes:**
1. PI Agent to file NM-079 in `docs/process/near-miss-registry.md` before any implementation PR opens — the near-miss entry must precede the fix, not follow it
2. PM Agent to cut `sprint/m18-g7` from `release/m18` after this approval lands in `release/m18` (via state sync PR) and open the G7 sprint journal issue
3. Implementing agents to begin Step G7-0 root cause analysis — the first and only step that may begin before per-cluster intent documents are filed

**EL notes on record:**

1. **BPO priority escalations (from #1475#issuecomment-4839161892):** Three findings carry elevated operational priority flagged by the Business PO that are not fully reflected in the cluster ordering. The implementing agent must treat these as first-in-cluster:
   - DEMO-142 ("Policy Malevolent Margin" jargon): first fix in Cluster E display-layer work, before any screenshot recapture. A jargon exposure in a stakeholder session is a professional credibility failure, not merely a rendering bug.
   - DEMO-146 (walkthrough filename table mismatch): first fix in Cluster E documentation work. A presenter briefing from the walkthrough the night before the session will be confused by mismatched filenames — this is operationally significant.
   - DEMO-148 Frame C→D act-break transition: highest-risk narration gap. Implement before recapture so the walkthrough is correct at the point screenshots are taken.

2. **G7-0 root cause analysis scope:** The root cause document must explicitly address whether DEMO-150 (Ecological value missing) and DEMO-151 (HD trajectory absent from Zone 1A) are bugs or enhancement gaps. The entry scopes them tentatively as "enhancement-class" but the EL wants a specific determination from the root cause analysis before final disposition. If they are bugs (rendering bindings that exist in the codebase but fail to populate), they are in G7 scope. If they are missing module outputs (the backend simply doesn't produce these values), they are M19 scope.

3. **Cluster B and C ADR gating is non-negotiable.** If the Architect Agent determines at G7-0 that Cluster B (Zone 1B height budget) or Cluster C (CohortImpactSection monitored-row state) constitutes a new instrument contract not covered by existing ADR-008/010 specs, the relevant ADR amendment must be accepted before the implementation PR for that cluster opens. No exceptions on timeline grounds. The demo timeline is not a reason to skip the ADR gate.

4. **Step G7-0 is EL-reviewed, not self-approved.** The root cause analysis document must be presented to EL for review and sign-off before any fix intent document is authored. The sequencing is: G7-0 document filed → EL reviews → EL signs off → per-cluster intent documents authored. EL sign-off on G7-0 is what unlocks Clusters A through E.

5. **NM-079 numbering:** The G7 sprint entry reserves NM-079 for the CI band geometry finding. The DS sprint health audit (commit 9009387, PR #1482) references "NM-079/NM-080" for the session start checklist process improvement, which predates the formal registry entries. The near-miss registry currently ends at NM-078. PI Agent assigns numbers from the next available (NM-079) in order filed. File CI band geometry as NM-079 per the convention established in this entry; the DS sprint health session start finding is NM-080 or NM-081 depending on which is filed first. The registry sequence must be continuous.

— @PublicEnemage, 2026-06-29
