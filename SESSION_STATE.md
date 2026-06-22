# WorldSim Session State

> This file is maintained by Claude Code. It is updated at the end of
> every session as the last action before closing. Do not edit manually.
> Engineering Lead decisions and context are recorded here for session
> continuity. For permanent rules and architecture, see CLAUDE.md.

**Last updated: 2026-06-22 (M15-G4 Step 4 Verify PASS — PRs #1116+#1117 merged; CM sign-off on #975 filed; NM-053/NM-054 filed; G4 Step 5 Validate pending BPO; G5 impl complete pending EL Step 4/5)**
**Current milestone:** M15 — Human Cost Architecture (GitHub Milestone 16)
**Previous milestone:** M14 — Trust Architecture and Instrument Credibility (FORMALLY CLOSED 2026-06-20; release/m14 → main PR #1086; v0.14.0 at https://github.com/PublicEnemage/worldsim/releases/tag/v0.14.0; #968 closed; GitHub Milestone 15 closed)

---

## M15 Kickoff Prerequisites

**Release branch:** `release/m15` — ✅ cut from `main` 2026-06-20 (commit 500e50d)
**Sprint plan:** ✅ filed 2026-06-20 — `docs/process/sprint-plans/m15-sprint-plan.md` (PR pending EL approval)

| Step | Status | Notes |
|---|---|---|
| 1. PM Agent cuts `release/m15` from `main` | ✅ DONE 2026-06-20 | `release/m15` at 500e50d |
| 2. PM Agent authors `m15-sprint-plan.md` | ✅ DONE 2026-06-20 | Filed in PR opening; EL approval pending |
| 3. EL approves sprint plan | ✅ **EL APPROVED 2026-06-20** | `docs/process/sprint-plans/m15-sprint-plan.md` |
| 4. PM Agent marks ARCH-011 ASSIGNED in backlog | ✅ **DONE 2026-06-22** | ARCH-011 → ASSIGNED — ADR-017 (number 17); updated in this session |
| 5. M15 exit checklist issue #984 renamed | ✅ DONE 2026-06-20 | Renamed to "M15 Exit Checklist — blocks milestone closure" |
| 6. KI-005 permanent fix applied | ✅ DONE 2026-06-20 | `do_not_enforce_on_create: true` on Ruleset 17751852; future release branches need no Ruleset workaround |

Implementation is now unblocked. A sprint entry document must be filed and EL-approved before any G-group implementation PR opens.

---

## HORIZON Sweep — 2026-06-20

**Open issues reviewed:** 1 (insights log entry 6 — CLAUDE.md structure)
**Disposition:**
- Entry 6 (2026-06-16, CLAUDE.md refactor): **promoted → #1091** — M14 has closed; deferral condition met; issue filed for M15 scope
- All other entries: previously promoted/resolved; no change

**New issues filed this sweep:**
| Issue | Title | Trigger |
|---|---|---|
| #1088 | docs(demo): walkthrough update — "0 consecutive steps" plain-language (DEMO-123) | Slipped M14 close; required before #843 |
| #1089 | docs(demo): walkthrough update — Grounding strip persistence note (DEMO-124) | Slipped M14 close; required before #843 |
| #1090 | docs(demo): walkthrough update — methodology documentation URL (DEMO-129) | Slipped M14 close; required before #843 |
| #1091 | docs(claude-md): extract Lifecycle/Exit/DIC sections to child docs | Promoted from insights log entry 6 |

**Process gaps identified:**
- DEMO-123/124/129 walkthrough updates were due "before M14 close" per stakeholder review (session table row 182) but slipped. Filed as M15 issues above. Not a near-miss requiring NM entry — the M14 exit ceremony closed with EL acceptance; these are incremental improvements to walkthrough narration, not defects in the application.
- Issue #984 title naming discrepancy: "Milestone 16 Exit Checklist" vs. our convention "M15 Exit Checklist". Flagged for EL to confirm or request rename.

---

## Open Issues — M15 (Human Cost Architecture)

**GitHub Milestone:** 16 | **Created:** 2026-06-16 | **Status:** Planned — Demo 6 anchor; #843 is exit gate
*Zone 1A ADR + Layer 3 self-interpreting outputs + live external demo. Sets up Demo 6.*

| Issue | Title | Group | Notes |
|---|---|---|---|
| #1065 ✅ | ux(zone-1b): Layer 3 trajectory sentence — Zone 1B | G1 | ✅ CLOSED 2026-06-21 — M15-G1 Step 3 COMPLETE (PR #1097) |
| #1066 ✅ | ux(zone-1b): suppress "0 consecutive steps" when zero | G1 | ✅ CLOSED 2026-06-21 — M15-G1 Step 3 COMPLETE (PR #1097) |
| #1067 ✅ | demo(screenshots): Frame B and C are same screenshot | G5 | ✅ MERGED 2026-06-22 — PR #1121; frame-b md5 ≠ frame-c md5 (IR-003 guard) |
| #1068 ✅ | ux(zone-1a): L0 badge on Zone 1A trajectory curves | G1 | ✅ CLOSED 2026-06-21 — M15-G1 Step 3 COMPLETE (PR #1097) |
| #1069 ✅ | ux(grounding-strip): dual reserve values without disambiguation | G1 | ✅ CLOSED 2026-06-21 — M15-G1 Step 3 COMPLETE (PR #1097) |
| #1075 ✅ | ux(zone-1d): PSP self-interpreting sentence absent | G1 | ✅ CLOSED 2026-06-21 — M15-G1 Step 3 COMPLETE (PR #1097) |
| #1083 ✅ | ux(grounding-strip): date label "2024-Q1" → "Apr 2024" | G5 | ✅ MERGED 2026-06-22 — PR #1119; formatVintageDate() + grounding-strip-date testid |
| #1084 ✅ | methodology: PSP historical calibration anchor | G5 | ✅ MERGED 2026-06-22 — PR #1122; Zambia/Ghana ECF, compliance outcomes, public IMF sources |
| #1088 ✅ | docs(demo): walkthrough — "0 consecutive steps" plain language | G5 | ✅ MERGED 2026-06-22 — PR #1121; DEMO-123 fix: phrase absent |
| #1089 ✅ | docs(demo): walkthrough — Grounding strip persistence | G5 | ✅ MERGED 2026-06-22 — PR #1121; "entry-state" ×9 in walkthrough |
| #1090 ✅ | docs(demo): walkthrough — methodology URL | G5 | ✅ MERGED 2026-06-22 — PR #1121; docs/onboarding/methodology-overview.md cited ×5 |
| #1091 | docs(claude-md): extract Lifecycle/Exit/DIC to child docs | G7 | promoted from insights log entry 6; filed 2026-06-20 |
| #1048 ✅ | infra: Docker API container Alembic migrations (NM-049) | G5 | ✅ MERGED 2026-06-22 — PR #1123; entrypoint.sh runs alembic upgrade head at startup |
| #1007 ✅ | fix: recompute-badge not visible after apply-control-change | G5 | ✅ MERGED 2026-06-22 — PR #1119; immediate "pending" state before async fetch |
| #1004 ✅ | process: Visual Spec section for intent template | G5 | ✅ MERGED 2026-06-22 — PR #1122; data-testid ×4, viewport ×2 in §4b |
| #984 | M15 Exit Checklist | — | immediate \| M15 gate issue (note: title says "Milestone 16" — GitHub milestone numbering) |
| #990 | test: accessibility validation on 8GB/4-core target hardware | G6 | Filed 2026-06-16 |
| #987 | feat(ux): political risk summary surface (Persona 3) | G3 | Design in M15; implementation M16 |
| #986 | feat(ux): cohort disaggregation on primary surface | G3 | Design in M15; implementation M16 |
| #975 | feat(data): Path 1 — approved source network query | G4 | Journey A GA-01; extends ADR-016 Component 1 |
| #951 | process: solo-use review protocol | G5 | Migrated from M14 |
| #846 | ux: DEMO-045 — Mode 3 branch comparison in instrument | G4 | |
| #845 (Ph 2–4) | ux: Zone 1A information architecture — ADR-017 | G2 | Phase 1 design thinking doc done (M14 G6c) |
| #843 | plan: live stakeholder demo with real external participants | G8 | **M15 exit gate** — deferred from M14 (EL decision 2026-06-20) |
| #837 | feat(demo): configuration-driven demo scripts | G5 | |
| #569 | test(perf): MV-002 Mode 3 hardware validation | G6 | |
| #53 ✅ | arch: RBAC design (prerequisite for Path 2 in M16) | G4 | ✅ CLOSED 2026-06-21 — will-not-implement (AC-001); #976 permanently closed |
| #259 | standards: CTO legibility metrics dashboard | G5 | |
| #153 | feat(frontend): absolute threshold overlay | | |
| #97 | arch(api): threshold-crossing markers | | |
| #92 | arch(backtesting): Greece investment climate conditions | | |
| #6 | governance: branch protection restoration | G7 | EL-action |
| #3 | governance: single-principal separation of duties | G7 | EL-action |

---

## Open Work Streams — M15 (Human Cost Architecture)

### M15-G1 — Layer 3 IR Fixes (COMPLETE)

**Sprint entry:** `docs/process/sprint-plans/m15-g1-sprint-entry.md` — EL-approved 2026-06-20 (PR #1095)
**Intent document:** `docs/process/intents/M15-G1-2026-06-20-layer3-ir-fixes.md`
**QA tests (Step 2):** `frontend/tests/e2e/m15-g1-layer3-ir-fixes.spec.ts` — PR #1096 (merged)
**Issues:** #1065, #1066, #1068, #1069, #1075

| Item | Status | Notes |
|---|---|---|
| G1 sprint entry document | ✅ **EL APPROVED 2026-06-20** (PR #1095) | Five entry conditions satisfied; implementation unblocked |
| G1 QA tests (Step 2) | ✅ FILED 2026-06-20 — PR #1096 | AC-1–AC-11 authored before implementation; NM-051 prerequisite fix |
| G1 implementation (Step 3) | ✅ **MERGED 2026-06-21** — PR #1097 + PR #1098 → release/m15 | Five Layer 3 IR fixes: trajectory sentence (AC-1–4), zero-step suppression (AC-5), L0 badges (AC-6), grounding strip disambiguation (AC-7–8), PSP sentence (AC-9–11); null guard for `getIndicatorDisplayNameAny` (PR #1098) |
| G1 Step 4 Verify | ✅ **PASS 2026-06-21** | 11/11 ACs pass; NM-051 filed (indicator_key crash at Step 4); verdict in intent doc §8 |
| G1 Step 5 Validate | ✅ **BPO ACCEPT 2026-06-21** | 11/11 ACs pass live; Customer Agent Layer 3 PASS (all 4 content additions); North star PASS — Aicha can argue reserve criticality, disambiguation, and PSP meaning without specialist mediation; sprint exit filed |
| NM-051 | ✅ FILED 2026-06-21 | QA mock used alert_id/indicator_id instead of mda_id/indicator_key; undefined key crashed React tree; null guard fix in PR #1098 |
| #1065/#1066/#1068/#1069/#1075 | ✅ CLOSED 2026-06-21 | All five G1 issues closed on GitHub |

**Sprint exit document:** `docs/process/sprint-plans/m15-g1-sprint-exit.md` — PI Agent Confirmed 2026-06-21
**G8 gate status:** G8 (#843 live external demo) is now UNBLOCKED — G1 Step 5 Validate complete.

---

### M15-G2 — Zone 1A Information Architecture ADR

**Sprint entry:** `docs/process/sprint-plans/m15-g2-sprint-entry.md` — **EL APPROVED 2026-06-21** (PR #1104)
**Issue:** #845 (Phases 2–3 only)

| Item | Status | Notes |
|---|---|---|
| G2 sprint entry document | ✅ **EL APPROVED 2026-06-21** (PR #1104) | All entry invariants satisfied |
| Intent document (Step 1) | ✅ **FILED 2026-06-22** (PR #1107) | `docs/process/intents/M15-G2-2026-06-21-zone-1a-adr.md`; QA Lead checkbox ✅ |
| QA test file (Step 2) | ✅ **FILED 2026-06-22** (PR #1107) | `backend/tests/test_m15_g2_zone1a_adr.py`; 34 tests AC-1–AC-11 |
| ARCH-011 ASSIGNED in backlog | ✅ **DONE 2026-06-22** | `docs/architecture/backlog.md` — ASSIGNED — ADR-017 (number 17) |
| Phase 2 — Architecture Review (ARCH-REVIEW-007) | ✅ **AUTHORED 2026-06-22** | `docs/architecture/reviews/ARCH-REVIEW-007-milestone15.md`; four open questions resolved; binding decisions: Mode 3 composite encoding, COMPARE_VIEW N≤2/fixture, `composite_score` reuse, endpoint label y-offset algorithm |
| Phase 3 — ADR-017 authorship | ✅ **AUTHORED 2026-06-22** | `docs/adr/ADR-017-zone-1a-information-architecture.md`; Tier 1; full P-1–P-7, UX-1–UX-7, NM-042 sign-off |
| Encoding mockups | ✅ **MERGED 2026-06-22** — PR #1113 | `docs/ux/mockups/ADR-017-zone-1a-encoding-mockups.html`; 6 SVG panels; referenced from ADR-017 §Visual Mockups as relative hyperlink |
| Phase 3 — **EL acceptance** | ✅ **ACCEPTED 2026-06-22** — PR #1114 | @PublicEnemage accepted after reviewing mockups; Status → `Accepted`; `test_el_acceptance_status` now passes |
| QA tests (34/34) | ✅ **34/34 PASS 2026-06-22** | All AC-1–AC-11 pass after PR #1114 merge |
| Sprint exit document | ✅ **FILED 2026-06-22** | `docs/process/sprint-plans/m15-g2-sprint-exit.md`; PI Agent Confirmed |
| **Step 5 Validate — BPO ACCEPT** | ✅ **BPO ACCEPT 2026-06-22** | Navigation PASS; kryptonite PASS; north star PASS; Layer 3 N/A (architecture doc). Phase 4 gate: Zone 1D delta annotations required companion. Full verdict: intent §9 + sprint exit §3. |
| Phase 4 — implementation | ⬜ Out of G2 scope | Separate sprint entry required; may extend to M16. **Phase 4 entry condition:** Zone 1D delta annotations must be in same sprint as Zone 1A composite encoding (per BPO ACCEPT phase 4 gate). |

**G2 is COMPLETE.** BPO ACCEPT recorded 2026-06-22. Next for #845: Phase 4 implementation sprint entry (separate sprint). Close #845 Phases 2–3 on GitHub.

---

### M15-G3 — Cohort Disaggregation and Political Risk Summary Design

**Sprint entry:** N/A — design-only; no sprint entry required per `docs/process/sprint-plans/m15-sprint-plan.md §G3`
**Intent document:** `docs/process/intents/M15-G3-2026-06-21-cohort-disaggregation-design.md` — filed 2026-06-21
**Issues:** #986 (cohort disaggregation), #987 (political risk summary surface)

| Item | Status | Notes |
|---|---|---|
| Intent document | ✅ FILED 2026-06-21 | AC-1–AC-11 with reviewer gates; both issues covered |
| QA tests | ✅ FILED — PR #1109 | `backend/tests/test_m15_g3_cohort_political_risk_design.py` — 45 tests AC-1–AC-11 |
| cohort-disaggregation-design.md (Step 3) | ✅ **MERGED 2026-06-22** — PR #1109 → release/m15 | Zone 1B placement; income quintile + age cohort; 3 HCL indicators; MDA-derived thresholds; ADR-017 disposition (b) — independent |
| political-risk-summary-design.md (Step 3) | ✅ **MERGED 2026-06-22** — PR #1109 → release/m15 | Zone 1D extended; no new ADR required; mode-specific contracts; ZMB ECF step 3 literal example; 30-sec legibility check; #1084 gate |
| G3 QA: 45/45 pass | ✅ PASS 2026-06-22 | All ACs confirmed via pytest before commit |
| G3 Step 4 Verify | ✅ **PASS 2026-06-22** | 45/45 QA tests; all AC-1–AC-11 observable states confirmed by document read; both silent failure tests pass; verdict in intent doc §8 |
| G3 Step 5 Validate | ✅ **BPO ACCEPT 2026-06-22** | Both designs specify Layer 3 output; North star PASS (Aicha closes FINDING-03 HIGH via cohort rows; Andreas closes PSP mediation gap via political risk sub-section); Kryptonite PASS; sprint exit filed PR #1110 |
| Chief Methodologist sign-off (#986) | ⬜ Required before M16 sprint entry | Cohort indicator scope + MDA-derived floor methodology (AC-3); comment on #986 |
| CM sign-off (#987) | ⬜ Required before M16 sprint entry | PSP severity tier thresholds + 2pp direction sensitivity (AC-11); comment on #987 |
| DemographicModule output verification (#986) | ⬜ Required before M16 sprint entry | Data Architect confirms cohort field availability for GRC/JOR/EGY/ZMB |
| Architecture Review Facilitator confirmation | ⬜ Required before M16 sprint entry | AC-1–AC-6 (#986) and AC-7–AC-11 (#987); both documents reviewed |
| Zone 1D layout feasibility (#987) | ⬜ Required before M16 sprint entry | Frontend Architect confirms sub-section fits at 1280×800 without displacing 4-framework rows |

**Sprint exit document:** `docs/process/sprint-plans/m15-g3-sprint-exit.md` — PI Agent Confirmed 2026-06-22 (PR #1110)

---

### M15-G4 — Path 1 + ADR-016 Component 3

**Sprint entry:** `docs/process/sprint-plans/m15-g4-sprint-entry.md` — **EL APPROVED 2026-06-22**
**Intent document:** `docs/process/intents/M15-G4-2026-06-22-path1-fidelity-contextualisation.md` — **FILED 2026-06-22**
**Issues:** #975 (Path 1 approved source network query), ADR-016 Component 3 (Fidelity panel contextualisation)

| Item | Status | Notes |
|---|---|---|
| G4 sprint entry document | ✅ **EL APPROVED 2026-06-22** | `docs/process/sprint-plans/m15-g4-sprint-entry.md`; all structural gates clear |
| Architect scope confirmation (#975) | ✅ RESOLVED — intent §Decision Gate 1 | #975 within ADR-016 Component 1 scope; no ADR amendment required |
| CM analogous-case selection logic | ✅ RESOLVED — intent §Decision Gate 2 | Rule-based mapping: ZMB→ARG, JOR→GRC, EGY→ARG, GRC→GRC, unknown→null |
| CM sign-off on #975 | ✅ **FILED 2026-06-22 (late)** | Posted post-implementation (#975 comment); substantive CM validation was in intent doc pre-implementation; NM-053 filed for timing deviation |
| Data Architect API decisions (DA-G4-1–4) | ✅ RESOLVED — intent §Decisions Resolved | `loadable` field on `/data-quality`; async pull job POST+GET; api_contracts.yml update; new `/fidelity-context` endpoint |
| Intent document (Step 1) | ✅ **FILED 2026-06-22** | `docs/process/intents/M15-G4-2026-06-22-path1-fidelity-contextualisation.md`; 15 ACs |
| QA test files (Step 2) | ✅ **FILED 2026-06-22** | `backend/tests/test_m15_g4_path1_fidelity_contextualisation.py` + `frontend/tests/e2e/m15-g4-path1-fidelity-contextualisation.spec.ts` |
| `api_contracts.yml` update | ✅ **MERGED 2026-06-22 — PR #1116** | `/data-quality` extended; `/pull` + `/pull/{job_id}` + `/fidelity-context` added |
| G4 backend implementation (Step 3) | ✅ **MERGED 2026-06-22 — PR #1116** | `grounding.py`: `loadable` field, async pull job endpoints, `/fidelity-context` endpoint; `DataPullJob` ORM model; Alembic migration `2b821063ef81` (data_pull_jobs table + SEN seed in source_registry) |
| G4 frontend implementation (Step 3) | ✅ **MERGED 2026-06-22 — PR #1117** | `ScenarioPanel.tsx`: searchable combobox with 41 entities; `DataQualityPreview.tsx`: loadable state + pull trigger + polling; `FidelityDashboard.tsx`: scenario-specific contextualisation + SF-3 fallback; `App.tsx`: scenarioId prop wired |
| E2E test regression (NM-054) | ✅ **FIXED — PR #1117** | 6 existing tests used `.selectOption()` on now-`<input>` entity-selector; fixed to combobox fill+click pattern; NM-054 filed |
| G4 Step 4 Verify | ✅ **PASS 2026-06-22** | All 15 ACs confirmed via CI: `test-backend pass` (PR #1116 job 82762073879) + `playwright-e2e pass` (PR #1117 job 82775180511); intent doc §8 updated; two process deviations: NM-053 (CM sign-off timing), NM-054 (combobox regression) |
| G4 Step 5 Validate | ⬜ **Pending BPO** | Business PO confirms Eleni (Persona 2) can create SEN scenario within 5-min ceiling; Customer Agent Layer 3 assessment required before BPO verdict |

**Next required action:** Business PO (EL) runs Step 5 Validate — open live application with SEN scenario creation and ZMB fidelity panel; Customer Agent Layer 3 assessment; sprint exit document.

---

### M15-G5 — Process Fixes + Walkthrough Updates (Implementation COMPLETE)

**Sprint entry:** `docs/process/sprint-plans/m15-g5-sprint-entry.md` — **EL APPROVED 2026-06-22**
**Intent document:** `docs/process/intents/M15-G5-2026-06-22-process-fixes.md` — **FILED 2026-06-22**
**Issues:** #1007, #1048, #1004, #1067, #1083, #1084, #1088, #1089, #1090

| Item | Status | Notes |
|---|---|---|
| G5 sprint entry document | ✅ **EL APPROVED 2026-06-22** | Three-tier structure; Tier 1 gates G8; Tier 2 primary scope; Tier 3 capacity-allowing |
| Intent document (Step 1) | ✅ **FILED 2026-06-22** | `docs/process/intents/M15-G5-2026-06-22-process-fixes.md`; 13 ACs; 5 agents co-authored |
| QA test files (Step 2) | ✅ **FILED 2026-06-22** | `frontend/tests/e2e/m15-g5-process-fixes.spec.ts` (AC-1–6); `backend/tests/test_m15_g5_process_fixes.py` (AC-7–13) |
| **Tier 1 — #1083** (date label) | ✅ **MERGED 2026-06-22** — PR #1119 | `formatVintageDate()` + `extractReferenceDate()` + `data-testid="grounding-strip-date"` in GroundingStrip.tsx |
| **Tier 1 — #1007** (recompute-badge) | ✅ **MERGED 2026-06-22** — PR #1119 | Immediate `recomputeStatus: "pending"` before async branch POST; kryptonite-compliant badge text |
| **Tier 1 — #1067** (screenshot fix) | ✅ **MERGED 2026-06-22** — PR #1121 | 5 distinct PNGs in `docs/demo/m15/screenshots/`; frame-b md5 ≠ frame-c md5 |
| **Tier 1 — #1088** (walkthrough DEMO-123) | ✅ **MERGED 2026-06-22** — PR #1121 | "0 consecutive steps" absent; phrase count = 0 |
| **Tier 1 — #1089** (walkthrough DEMO-124) | ✅ **MERGED 2026-06-22** — PR #1121 | "entry-state" ×9 in `docs/demo/m15/stakeholder-walkthrough.md` |
| **Tier 1 — #1090** (walkthrough DEMO-129) | ✅ **MERGED 2026-06-22** — PR #1121 | `docs/onboarding/methodology-overview.md` cited ×5 |
| **Tier 2 — #1084** (PSP anchor) | ✅ **MERGED 2026-06-22** — PR #1122 | `docs/methodology/psp-calibration-anchor.md`; Zambia 2022 + Ghana 2023 ECF; public IMF sources |
| **Tier 2 — #1004** (intent template) | ✅ **MERGED 2026-06-22** — PR #1122 | §4b data-testid ×4 (≥2 ✓); viewport ×2 (≥1 ✓) |
| **Tier 2 — #1048** (Docker migrations) | ✅ **MERGED 2026-06-22** — PR #1123 | `backend/entrypoint.sh` (alembic upgrade head + exec "$@"); Dockerfile uses ENTRYPOINT+CMD |
| Tier 3 — #837 (demo.sh config-driven) | ⬜ Not started — capacity-allowing | No G8 gate dependency |
| Tier 3 — #951 (solo-use review protocol) | ⬜ Not started — capacity-allowing | No G8 gate dependency |
| Tier 3 — #259 (legibility metrics dashboard) | ⬜ Not started — capacity-allowing | No G8 gate dependency |
| **G8 gate** | ✅ **SATISFIED 2026-06-22** | All 5 Tier 1 items (#1067, #1083, #1088, #1089, #1090) merged to release/m15 — G8 sprint entry may now open |
| Step 4 Verify | ⬜ Pending EL | Frontend Architect must confirm AC-1–7 observable states in running application before sprint exit |
| Customer Agent Layer 3 | ⬜ Pending | Required for #1007 and #1083 (Persona 2/5 recompute-badge and date label) |
| Step 5 Validate (BPO) | ⬜ Pending | Business PO: screenshot distinctness, walkthrough DEMO-123/124/129 fixes, PSP anchor navigability |

**G5 implementation is complete. G8 gate is satisfied. Step 4 Verify, Customer Agent Layer 3, and Step 5 BPO Validate are the remaining exit conditions before the sprint exit document can be filed.**

---

## EL Architectural Decisions — 2026-06-21

**Authority:** Engineering Lead permanent decisions. Recorded by PM Agent.
**Constraint document:** `docs/architecture/constraints.md`

### AC-001 — Private Data Inputs Are Prohibited (Permanent)

Private, proprietary, or ministry-owned data inputs are architecturally prohibited. The shared public dataset guarantee is the epistemic foundation of WorldSim's negotiating authority — reproducibility by both parties requires both parties to be able to inspect the same public sources. Private inputs sever reproducibility.

**Founding document basis:** `docs/vision/worldsim-founding-document.md §Open Source as Strategy`

**Issue dispositions:**

| Issue | Title | Disposition |
|---|---|---|
| #976 ✅ | Path 2 — ministry-owned / proprietary data upload | CLOSED 2026-06-21 — will-not-implement (AC-001); permanent prohibition, not a capacity deferral |
| #53 ✅ | RBAC design (prerequisite for Path 2) | CLOSED 2026-06-21 — will-not-implement (AC-001); prerequisite for Path 2 which is permanently closed |
| #5 ✅ | Data marketplace — curated / user-contributed datasets | CLOSED 2026-06-21 — will-not-implement-at-this-stage; no validated real-world demand; re-open trigger: real finance ministry analyst articulates specific dataset need Path 1 cannot satisfy |
| #4 ✅ | Advanced geocoded dataset integration | CLOSED 2026-06-21 — will-not-implement-at-this-stage; no validated real-world demand; same re-open trigger |

**G4 scope confirmed (post-AC-001):** G4 = #975 (Path 1 approved source network) + ADR-016 Component 3 only. #53 removed from G4 scope.

### AC-002 — Synthetic Substitution from Public Sources Is Permitted with Mandatory Indicator-Level Disclosure

Synthetic estimates from comparable economies, regional distributions, and historical patterns are permitted and required for the democratization mission. Three mandatory conditions: indicator-level disclosure, T3 confidence tier floor, meaninglessness threshold suppression. The sparse-data problem is addressed through ADR-007 and the confidence tier system — not through private uploads.

**Founding document basis:** `docs/vision/worldsim-founding-document.md §Open Source as Strategy`; `CLAUDE.md §Synthetic Data and the Data Inference Layer`

**Future scope:** Methodology audit of ADR-007 against data-sparse countries (Chad, Yemen, Myanmar) — filed as future scope item after ADR-007 is complete; not a new capability; validates the framework against real data-poverty conditions.

### Parking Lot Dispositions (2026-06-21)

| Issue | Title | Disposition |
|---|---|---|
| #35 | Dynamic relationship weight updating | Moved to Parking Lot milestone (GitHub milestone #20) — complexity addition; deferred until core capability is battle-tested through real-world use; no trigger condition required |
| #30 | Stock vs. flow variable distinction | Moved to Parking Lot milestone (GitHub milestone #20) — complexity addition; same deferral basis |

### Insights Log

Entry 7 added to `docs/insights-log.md` (2026-06-21): AC-001 and AC-002 should be reflected in the founding document as explicit permanent governing constraints — flag for EL to author addition to `docs/vision/worldsim-founding-document.md §Open Source as Strategy`.

### Hard Stop

**No G-group sprint entry may be filed or EL-approved until the constraint record PR is merged to `release/m15`.** The constraint record (AC-001, AC-002, issue dispositions) must be on the release branch before any further G-group sprint entries reference G4 scope or open issues.

---

## Closed — M13 Active Work Streams (reference record; all G1–G8 complete)

**Kickoff complete 2026-06-12. Exit ceremony complete 2026-06-15.** Wave 1 complete 2026-06-12. Wave 2 complete 2026-06-12. All sprints complete.

**M13 kickoff status:**
1. ✅ PM Agent cuts `release/m13` from `main` — DONE 2026-06-12
2. ✅ PM Agent authors `docs/process/sprint-plans/m13-sprint-plan.md` — DONE 2026-06-12
3. ✅ ADR-013 confirmed ASSIGNED (number 13, panel confirmed) — ready to author; ARCH-007 milestone note updated M12→M13
4. ✅ #852 sequencing confirmed — blocked on alert panel ADR (new issue #908 filed; ARCH-008 PENDING_NUMBER in backlog)
5. ✅ #264 (M13 Exit Checklist) — kickoff comment posted; EL approval comment posted
6. ✅ Process Redesign Sequence (Phases 0–D) — COMPLETE; no further redesign phases
7. ✅ Sprint entry document filed — `docs/process/sprint-plans/m13-sprint-1-entry.md` — EL-approved 2026-06-12
8. ✅ Sprint plan EL approval — **recorded 2026-06-12 (PR #911)**

**Wave 1 completion status:**
- ✅ G3 (#799): Reserves non-negativity floor — merged to release/m13 (PR #912)
- ✅ G1 (#872, #874): DEMO legibility fixes — merged (PR #913)
- ✅ G4 (#27, #822, #847): Documentation — merged (PR #915)
- ✅ G2 (#871, #873, #875, #876): DEMO trajectory/Mode 3 — merged (PR #914); 4 fixes: DEMO-059 PMM scale note, DEMO-062 Zone 1D entity label, DEMO-063 inline entity labels, DEMO-064 Mode 3 comparison readout
- ✅ G5 (#792): ADR-013 — accepted 2026-06-12 (PR #916); EL acceptance recorded

**Wave 2 completion status:**
- ✅ G6 (#392): Political economy integration — merged 2026-06-12 (PR #919)
  - Intent document: `docs/process/intents/ADR-013-2026-06-12-political-economy-integration.md`
  - 26 tests AC-1–AC-6; 1334 unit tests passing
  - Calibration basis political economy section complete (sensitivity 0.80→1.50 for AC-3)
  - ✅ BPO Step 5 Validate: ACCEPT — 2026-06-12 (see intent document §8)
    - Scenario d5e10fce, GRC, legitimacy_index=0.4, political_economy enabled
    - `outputs.political_economy` confirmed as top-level framework key at step 1
    - `programme_survival_probability = 0.59500` at step 1 (absent at step 0 — DEMO4 PASS)
    - `composite_score = "0.5650"` at step 1
    - Customer Agent Layer 3: PASS (MDA alert pathway present; indicator self-describing)
    - Analytical intent: Persona 2 can cite programme survival probability as quantified political feasibility constraint
    - #392 closed (issue closed as part of BPO acceptance)

**Wave 3 complete:**
- ✅ G7 (#852): Alert panel Zone 1B persistent-detail — COMPLETE 2026-06-13 (PR #936, BPO ACCEPT)
  - Sprint entry: `docs/process/sprint-plans/m13-g7-sprint-entry.md` — EL-approved 2026-06-13 (PR #935)
  - Intent document: `docs/process/intents/ADR-014-2026-06-13-alert-panel-ux.md`
  - Step 4 Verify: PASS (2026-06-13, dev server port 5179, Hormuz scenario 558a27fe)
    - AC-1: zone-1b-top-detail visible at 1440×900 without interaction ✅
    - AC-2: data-severity="TERMINAL" on top detail slot ✅
    - AC-3: detail clientHeight > 0 at 1024×768 (98px), 1280×800 (85px), 1440×900 (85px) ✅
    - AC-5: compact rows cursor:default; click leaves detail unchanged ✅
    - AC-7: compact row height 24px ≤ 26px limit at 1024×768 ✅
    - Empty state: "No active threshold breaches." renders ✅
    - Old mda-alert-row and alert-detail-panel removed ✅
    - Mode-dependent tense: Mode 2 shows "BREACH PROJECTED" ✅
  - Step 5 Validate: BPO ACCEPT — 2026-06-13 (see below)
    - Persona 2 confirmed: open instrument cluster → TERMINAL breach evidence (severity + indicator + current vs. floor + 8 consecutive steps + confidence label) visible in Zone 1B detail slot with zero interactions
    - Customer Agent Layer 3: PASS — "Reserve coverage has fallen 2.1 months below the CRITICAL threshold. At current draw rate, full depletion occurs in 4 steps." — output is self-interpreting; ministry analyst can cite without mediation
    - North star: Zambian ministry analyst can read top threshold breach evidence with zero interactions from moment instrument cluster loads — interaction tax eliminated; argument evidence available at creditor-side parity
    - #852 closed

**Next action:** M13 EXIT CEREMONY COMPLETE 2026-06-15. G8 sprint exit filed (`docs/process/sprint-plans/m13-g8-sprint-exit.md`). All M13 issues dispositioned (11 closed, 9 migrated to M14). Reference docs updated (README, CLAUDE.md, roadmap). NM-044 filed (E2E regression gap). Required EL action: merge `release/m13` → `main`, close #264, tag release, close GitHub Milestone 9. M14 kickoff is the next agent action.

### M14 Kickoff Prerequisites (RESOLVED 2026-06-15)

**✅ HARD STOP CLEARED:** EL merged `release/m13` → `main` 2026-06-15. All G1–G8 M13 deliverables are on `main`. M14 work may proceed.

**M14 kickoff sequence status:**
1. ✅ `git pull origin main` — confirmed current (PR #957 merge; commit e63828f)
2. ✅ PM Agent cuts `release/m14` from `main` — DONE 2026-06-16
3. ✅ PM Agent authors `docs/process/sprint-plans/m14-sprint-plan.md` — DONE 2026-06-16
4. ⬜ **EL approves sprint plan** — NEXT REQUIRED ACTION before implementation begins
5. ✅ PM Agent files M14 Exit Checklist issue — DONE 2026-06-16 (**#968**; closure gate: #843)
6. ⬜ Sprint entry document filed per `docs/process/sprint-planning-sop.md §Sprint Entry Gate` — required before implementation

**HARD STOP:** No implementation PR may open against `release/m14` until the EL has approved the sprint plan and a sprint entry document is filed.

---

## Open Work Streams — M14 (Active)

**Wave structure (EL decision 2026-06-15):**
- **Wave 1 — COMPLETE:** ADR-016 (Scenario Grounding Architecture) — Accepted 2026-06-16 (PR #967)
- **Wave 2:** ADR-015 (Evidence Thread Architecture) — ✅ ACCEPTED 2026-06-16 (PR #998); implementation scope: Components 1, 2, 3 (M14); Component 4 deferred to M15

**Current state:**

| Item | Status | Next action |
|---|---|---|
| Bug #961 — GRC hardcoded in creation form | ✅ FIXED 2026-06-17 (PR #1006) | BPO Step 5 Validate pending |
| Bug #962 — step counter 'Step 0 / 8' | ✅ FIXED 2026-06-17 (PR #1006) | BPO Step 5 Validate pending |
| Bug #963 — choropleth raw DB field names | ✅ FIXED 2026-06-17 (PR #1006) | BPO Step 5 Validate pending |
| Bug #1007 — recompute-badge not visible after apply-control-change | Filed 2026-06-17 | Pre-existing; discovered during G1 Step 4 Verify; to be addressed in G5 or follow-on |
| ARCH-010 / ADR-016 — Scenario Grounding | ✅ ACCEPTED 2026-06-16 (PR #967) | G3 COMPLETE; G4 Step 4 PASS; G4 Step 5 PENDING |
| ADR-016 entity scope | GRC, JOR, EGY, ZMB (EL decision 2026-06-16) | — |
| ADR-016 Component 3 | Deferred to M15 (EL decision 2026-06-16) | — |
| ADR-016 IC-6 mitigation | Choropleth header label in M14 (EL decision 2026-06-16) | Part of G4 |
| ADR-015 — Evidence Thread Architecture | ✅ ACCEPTED 2026-06-16 (PR #998) | 6 decisions resolved; Components 1–3 in M14 scope; Component 4 → M15; Demo 5 script constraint → #997 |
| M14 sprint plan | ✅ **EL APPROVED 2026-06-16** — `docs/process/sprint-plans/m14-sprint-plan.md` | Sprint entry document required per group before implementation PR opens |
| release/m14 branch | ✅ Cut 2026-06-16 from main | Ready for feature PRs — sprint entry document required first |
| G1 sprint entry document | ✅ Filed 2026-06-16 — `docs/process/sprint-plans/m14-g1-sprint-entry.md` (PR #993) | **EL Approved 2026-06-16** (PR #996); intent doc ✅ filed (PR #999); QA tests ✅ filed (PR #1001) |
| G1 intent document | ✅ Filed 2026-06-16 — `docs/process/intents/M14-G1-2026-06-16-prerequisite-bugs.md` (PR #999) | Step 4 Verify PASS 2026-06-17 — all 7 ACs pass; Step 4 verdict recorded in §8 of intent doc |
| G1 QA tests (Step 2) | ✅ Filed 2026-06-17 — `frontend/tests/e2e/m14-g1-prerequisite-bugs.spec.ts` (PR #1001) | All 7 ACs covered; entity-selector guard pattern; AC-4/AC-5 API fixture; AC-6 label-scope |
| G1 implementation (Step 3) | ✅ MERGED 2026-06-17 — PR #1006 → release/m14 | ScenarioPanel entity selector; ScenarioControls initialStep; App.tsx initialStep prop |
| G1 Step 4 Verify | ✅ PASS 2026-06-17 | 7/7 ACs pass; 4 probes pass; pre-existing #1007 discovered and filed; verdict in intent doc §8 |
| G1 Step 5 Validate | ✅ BPO ACCEPT 2026-06-17 | All 3 observable states confirmed; Layer 3 PASS; intent doc §9; sprint exit filed |
| G3 sprint entry | ✅ EL Approved 2026-06-17 — `docs/process/sprint-plans/m14-g3-sprint-entry.md` (PR #1011 merged) | Step 2 QA tests filed before implementation; Step 3 impl merged |
| G3 QA tests (Step 2) | ✅ Filed 2026-06-17 — `backend/tests/test_m14_g3_adr016_backend.py` (PR #1011) | AC-1–AC-9 pytest+httpx; authored before implementation |
| G3 implementation (Step 3) | ✅ MERGED 2026-06-17 — PR #1011 → release/m14 | source_registry seed; entity_data_quality_coverage; /data-quality; /initial-state; api_contracts.yml |
| G3 Step 4 Verify | ✅ PASS 2026-06-17 | 9/9 ACs pass after `alembic upgrade head`; Step 4 note: migration not pre-applied at initial probe (500); verdict in intent doc §8 |
| G3 Step 5 Validate | ✅ BPO ACCEPT 2026-06-17 | JOR scenario `68b31277` — reserve_coverage_months: 7.1 months · CBJ 2023-Q4 · T2; Persona 2 north star argument enabled; Layer 3 PASS; G4 gate open; intent doc §9 |
| G4 sprint entry document | ✅ **EL APPROVED 2026-06-17** — `docs/process/sprint-plans/m14-g4-sprint-entry.md` (PR #1014) | — |
| G4 intent document | ✅ Filed 2026-06-17 — `docs/process/intents/M14-G4-2026-06-17-adr016-frontend.md` | Step 4 Verify PASS 2026-06-17 — 9/9 ACs pass; verdict in intent doc §8 |
| G4 QA tests (Step 2) | ✅ Filed 2026-06-17 — `frontend/tests/e2e/m14-g4-adr016-frontend.spec.ts` | AC-1–AC-9; guard pattern; AC-8/AC-9 route mocks; authored before implementation |
| G4 implementation (Step 3) | ✅ MERGED 2026-06-17 — PR #1015 + PR #1016 (AC-5 text fix) → release/m14 | DataQualityPreview, GroundingStrip, ScenarioParameters, IC-4/IC-6 headers, ModeSelector onWrapperClick |
| G4 Step 4 Verify | ✅ PASS 2026-06-17 | 9/9 ACs pass; AC-5 text fix required (PR #1016); `ModeSelector.onClick` bubbles noted as finding; verdict in intent doc §8 |
| G4 Step 5 Validate | ✅ BPO ACCEPT 2026-06-17 | REJECT-001 issued (AC-3: GroundingIndicator field name mismatch source_institution→source); Data Architect review confirmed contract correct; fix merged PR #1018; re-validate PASS. Layer 3 PASS. North star PASS. NM-045 filed. G4 COMPLETE. |
| NM-046 Vite HMR polling fix | ✅ MERGED 2026-06-17 (PR #1021) | `usePolling: true` added to `frontend/vite.config.ts`; resolves macOS Docker inotify gap that caused EL post-G4 visual check to show stale frontend (CBJ absent, 0/0 Ctrl+F). NM-046 filed. EL confirmed CBJ visible after `docker compose restart frontend` + hard refresh. |
| G5 sprint entry | ✅ **EL APPROVED 2026-06-17** (PR #1022 merge + correction PR #1023) | `docs/process/sprint-plans/m14-g5-sprint-entry.md`; ADR-015 Components 1–3; Data Architect Agent (not Chief Engineer) for API field consultation and `api_contracts.yml`; entry invariant satisfied; implementation unblocked |
| G5 intent document (Step 1) | ✅ FILED 2026-06-18 — PR #1025 merged | `docs/process/intents/M14-G5-2026-06-17-adr015-frontend.md`; 14 ACs across Components 1, 2, 3; observable states, visual specs, NM-045 string-presence rule applied; Data Architect decisions appended PR #1026 |
| G5 Data Architect decisions | ✅ RECORDED 2026-06-18 — PR #1026 merged | DA-G5-1: /data-quality for source annotation. DA-G5-2: /initial-state null-filtered count. DA-G5-3: `modules_config` path confirmed; ScenarioConfigSchema extension specified. DA-G5-4: Option A (measurement-output) for programme_survival_probability. DA-G5-5: GRC/EGY→ceiling, JOR/ZMB→floor. All implementation gates cleared. |
| G5 QA tests (Step 2) | ✅ FILED 2026-06-18 — `frontend/tests/e2e/m14-g5-adr015-frontend.spec.ts` | All 14 ACs covered; NM-045 rule applied throughout; AC-4/8/9/10/11 route-mock pattern; AC-14 format regex accepted per intent doc §7; TypeScript clean (0 errors) |
| G5 implementation (Step 3) | ✅ MERGED 2026-06-18 — PR #1030 → release/m14 | FourFrameworkZone1D annotations, AssumptionSurface, Political Feasibility row, PMM annotation, HCL tier expansion, Zone 1B full indicator names |
| G5 Step 4 Verify | ✅ PASS 2026-06-18 | 17/17 ACs pass; test scenario `1fcc38b9` (JOR, fiscal_multiplier=1.30, 3 steps); data-quality JOR: financial T2·IMF, HD T2·WB, ecological T4, governance T3; verdict in intent doc §8 |
| G5 Step 5 Validate | ✅ BPO ACCEPT 2026-06-18 | North star: Zambian analyst defends trajectory in restructuring session — L0 annotations answer "where does this number come from?", assumption surface shows Fiscal ×1.30 immediately, PSP visible in Zone 1D; Layer 3 PASS; sprint exit filed |
| G5 sprint exit document | ✅ FILED 2026-06-18 — `docs/process/sprint-plans/m14-g5-sprint-exit.md` | All exit conditions satisfied; PI Agent confirmed; no rejections; north star test artifact present |
| G6 sprint entry document | ✅ **EL APPROVED 2026-06-18** — `docs/process/sprint-plans/m14-g6-sprint-entry.md` (EL approval: PR #1040; QA tests: PR #1041+#1042) | Issues: #885, #950, #884, #823, #824, #22, PMM anchor; QA tests filed 2026-06-18 (E2E + backend, AC-1–AC-9); all entry invariants satisfied; implementation unblocked |
| G6 implementation (Step 3) | ✅ **MERGED 2026-06-18** — PR #1045 → release/m14 (commit 13a9b83) | Zone 1B negotiation labels (#885), Zone 1A Y axis label (#950), reserve_coverage_months seeding (#884), ecological composite tier floor T3 (#823), water_stress_index + biome_class dispatch (#824), confidence tier methodology doc (#22), PMM interpretation anchor; Alembic migration b1c2d3e4f5a6; pre-push gates: ruff ✓, mypy (pre-existing only) ✓, npm run build ✓ |
| G6 Step 4 Verify | ✅ **PASS 2026-06-18** | All 9 ACs confirmed via CI: AC-1–4 playwright-e2e (commit 65158f4); AC-5–8 test-backend; AC-9 shell find assertion. NM-047 (step_index/n_steps) + NM-048 (data-quality render race) filed — pre-existing G5 test flaws exposed and fixed in same PR. Verdict in intent doc §8. |
| G6 Step 5 Validate | ✅ BPO ACCEPT 2026-06-18 | All 9 ACs confirmed live: Zone 1B T4 "Model estimate"/T5 "Synthetic extrapolation" (Playwright 6/6); Zone 1A "Score" Y axis (Playwright); JOR reserve_coverage_months value=7.1 T2 CBJ (API); GRC ecological T3 (API); water_stress_index=0.82 T3 JOR (post-migration b1c2d3e4f5a6); calibration docs <1 min nav. Sprint exit CONFIRMED. |
| G6 sprint exit document | ✅ Filed 2026-06-18 — `docs/process/sprint-plans/m14-g6-sprint-exit.md` | Section 2 (implementation) COMPLETE; Section 3 (Customer Agent Layer 3) COMPLETE; Section 4 (no rejections) COMPLETE; Section 5 PI Agent BLOCKED pending BPO Step 5 Validate |
| G2 — ADR-015 acceptance | ✅ COMPLETE 2026-06-16 (PR #998) | EL accepted ADR-015; 6 decisions resolved; Components 1–3 M14; Component 4 → M15. G5 unblocked. No sprint entry/exit doc required (EL-action, no user-facing deliverable). |
| Intent/test naming convention | ✅ Enforced 2026-06-16 (PR #999) | M{N}-G{N} prefix on intent docs and E2E tests — CLAUDE.md, intent-template.md, sprint-planning-sop.md, sprint-entry-template.md all updated |
| M14 Exit Checklist | ✅ Filed 2026-06-16 — **#968** (closure gate: #843) | Tracks all M14 deliverables |
| CI merge gate enforcement (#970) | ✅ CLOSED 2026-06-16 | `release-branch-ci-gate` Ruleset (ID 17751852) live — 6 required checks: `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`; `--admin` removed from SESSION_STATE merge rule |
| Branch naming enforcement (#978) | ✅ CLOSED 2026-06-16 | `.github/workflows/branch-naming.yml` (PR #979); KI-003 filed (PR #980) |
| Path 1 — approved source query | ✅ Filed **#975** (M15) | Extends ADR-016 Component 1; Journey A GA-01 |
| Path 2 — proprietary data upload | ✅ Filed **#976** (M16+; design in M14 G6b) | `USER_SUPPLIED` provenance type; #53 prerequisite; Journey A GA-02 |
| G6b intent document (Step 1) | ✅ FILED 2026-06-18 — `docs/process/intents/M14-G6b-2026-06-18-path2-design-groundwork.md` | 9 ACs across 3 design artifacts; UX Designer (field mapping UX concept), Architect (`USER_SUPPLIED` provenance spec), Data Architect (isolation model sketch); all filed to `docs/design/path2-data-upload/` before M14 exit; EL review gate before sprint exit |
| G6b design artifacts (Step 3) | ✅ FILED 2026-06-18 — `docs/design/path2-data-upload/` | AC-1–AC-9 covered: `field-mapping-ux-concept.md` (UX Designer; 5-min workflow, both failure modes, caveat placement), `user-supplied-provenance-spec.md` (Architect; T2 tier, Grounding Strip format, ADR-007 implication, scope boundary), `data-isolation-model-sketch.md` (Data Architect; isolation invariant, 3 failure modes, Issue #53 requirements, out-of-scope list); EL review gate: Step 4 |
| G6b sprint exit | ✅ FILED 2026-06-18 — `docs/process/sprint-plans/m14-g6b-sprint-exit.md` (PR #1039) | PI Agent confirmed; AC-1–AC-9 PASS; BPO ACCEPT 2026-06-18; north star forward trace: "ministry-supplied reserve figure" argument architecturally specified |
| Journey A gap markers (GA-01, GA-02) | ✅ Filed 2026-06-16 (PR #974) | `docs/ux/user-journeys.md` |
| Milestone planning panel deliberation | ✅ COMPLETE 2026-06-16 | M15–M18 defined; demo arc through Demo 7; 17 issues reallocated; 5 new issues filed (#986–#990); roadmap updated |
| G6c — Zone 1A Phase 1 design thinking | ✅ COMPLETE 2026-06-18 — PR #1033 merged | Intent at `docs/process/intents/M14-G6c-2026-06-18-zone-1a-design-thinking.md`; design doc at `docs/ux/design-thinking/zone-1a-information-architecture.md`; AC-1–AC-8 satisfied; BPO ACCEPT 2026-06-18 (intent doc §8); PI Agent sprint exit CONFIRMED (`docs/process/sprint-plans/m14-g6c-sprint-exit.md`); Phase 2 Readiness section present; gates M15 Architecture Review (#845 Phase 1 closed) |
| #988 — Goodhart's Law mitigation | ✅ Filed (M14 G7) | TSC monitoring framework for parameterization gaming risk |
| #989 — Onboarding documentation | ✅ Filed (M14 G7) | Global south analyst onboarding |
| G7 intent document (Step 1) | ✅ FILED 2026-06-18 — `docs/process/intents/M14-G7-2026-06-18-governance-onboarding.md` | 7 ACs; issues #988 + #989; EL-action items #3 and #6 noted out of agent scope; sprint entry gate note embedded |
| G7 QA tests (Step 2) | ✅ FILED 2026-06-18 — `backend/tests/test_m14_g7_governance_onboarding.py` | 28 tests: AC-1–AC-6 file-existence + content-presence checks (grep equivalents); AC-4 partial automation (≥1 blindspot; BPO confirms ≥3 at Step 5); AC-7 marked skip (manual BPO timed navigation); all 25 fail pre-implementation as expected |
| G7 sprint entry document | ✅ **EL APPROVED 2026-06-18** — `docs/process/sprint-plans/m14-g7-sprint-entry.md` | No ADR gate; intent + QA pre-filed; sequencing variance noted (no gate crossed); implementation unblocked |
| G7 implementation (Step 3) | ✅ MERGED 2026-06-18 (PR #1037) | 5 docs: `docs/onboarding/` (quick-start, scenario-creation, methodology-overview, data-provenance) + `docs/governance/goodharts-law-mitigation.md`; README Getting Started section added; 27/27 automatable ACs pass; lint clean |
| G7 Step 4 Verify | ✅ PASS 2026-06-18 | AC-1–AC-6 all confirmed via pytest (27 passed, 1 skipped); shell checks pass; Step 4 verdict in intent doc §8; AC-7 manual BPO at Step 5 |
| G7 Step 5 Validate | ✅ BPO ACCEPT 2026-06-18 | AC-7 timed nav PASS (~2–3 min); AC-4 5 blindspots ✅; AC-6 4 sections ✅; Layer 3 PASS; North star PASS; sprint exit filed |
| #986 — Cohort disaggregation on primary surface | ✅ Filed (M15) | M11.5 FINDING-03 gap; Demo 6 prerequisite |
| #987 — Political risk summary surface (Persona 3) | ✅ Filed (M15) | Plain-language legitimacy dynamics |
| #990 — Accessibility validation on target hardware | ✅ Filed (M15) | 8GB/4-core laptop gate |
| G8 sprint entry document | ✅ **EL APPROVED 2026-06-19** (PR #1054) | `docs/process/sprint-plans/m14-g8-sprint-entry.md`; ZMB only; no Mode 3; reserve challenge → Grounding strip citation; demo prep standard as governing intent doc; implementation unblocked |
| G8 Step 1 — demo issue filed | ✅ COMPLETE 2026-06-19 | #1055 filed (demo: M14 stakeholder demo preparation — v0.14.0 / Milestone 14) |
| G8 Step 2 — screenshot brief | ✅ COMPLETE 2026-06-19 (PR #1056) | `docs/demo/m14/screenshot-brief.md`; five frames; thesis frame C (citation at table); ZMB; no Mode 3 |
| G8 Step 3 — `demo.sh` updated | ✅ COMPLETE 2026-06-19 (PR #1056) | M14 Demo 5 ZMB/no-Mode3; challenge-response framing; honest disclosures; NM-041 `bash -n` gate PASS |
| G8 Step 4 — `demo-narrated.spec.ts` | ✅ COMPLETE 2026-06-19 (PR #1056) | Rewritten for ZMB ECF; `demo-narrated-m12.spec.ts` archived; NM-039 sentinel; 1440×900 viewport |
| G8 Step 5 — walkthroughs | ✅ COMPLETE 2026-06-19 (PR #1056) | `docs/demo/m14/stakeholder-walkthrough.md`; root redirect updated; narration checks 5a/5c encoded in walkthrough |
| G8 Step 5b — legibility gate | ✅ PASS 2026-06-19 | `demo-legibility.spec.ts` 10/10 pass at 1440×900 |
| G8 Step 5c — NARRATION-RULING-1 | ✅ PASS 2026-06-19 | All 5 presentation steps: Umbrella + Synthesis + Transition verified |
| G8 Step 6 — screenshot capture | ✅ COMPLETE 2026-06-19 (PR #1058) | Five frames captured; Round 3 spec fixes (ecological disabled, democratic_quality_score=0.80 to reserve top alert slot); Reserve WARNING Current 2.908 / Floor 2.500 visible in Zone 1B detail slot |
| G8 Step 6b — internal nine-agent review | ✅ COMPLETE 2026-06-19 (PR #1060) | `docs/demo/m14/reviews/2026-06-19-v0.14.0-internal-review.md`; 8 findings; 4 CRITICAL/HIGH blocking walkthrough errors corrected in same PR; Issue #1059 filed (HCL narration M15 scope) |
| G8 Step 7 — Independent Review | ✅ COMPLETE 2026-06-19/20 (PR #1064 + #1070) | `docs/demo/m14/reviews/2026-06-19-v0.14.0-ir-review.md`; 10 findings (IR-001–IR-010); five CRITICAL/HIGH issues filed (#1065–#1069); three-agent panel (UX Designer, Frontend Architect, Business PO) assessed IR-001 and IR-004 |
| G8 EL decision — IR issue triage | ✅ RECORDED 2026-06-20 | IR findings do not gate Demo 5. IR-004 Path B (narration correction) applied in M14. IR-001 (#1065), IR-002 (#1066), IR-003 (#1067), IR-004 Path A (#1068), IR-005 (#1069) deferred to M15 with implementation guidance comments. All five issues moved to M15 milestone / `horizon:near-term`. |
| G8 IR-004 Path B — Zone 1D narration | ✅ COMPLETE 2026-06-20 (PR #1071) | `stakeholder-walkthrough.md` corrected: Zone 1A badge claim → Zone 1D L0 annotation reference (4 locations). Zone 1D already implements correct L0 annotations; walkthrough narration now matches application state. |
| G8 Step 6c — audience simulation | ✅ **COMPLETE 2026-06-20** (PR #1076) | `docs/demo/m14/reviews/2026-06-20-v0.14.0-audience-simulation.md`; 25 findings DEMO-097–DEMO-121; 4 CRITICAL; north star verdict: FAIL/BLOCKED |
| G8 DEMO-099 — PSP Layer 3 sentence gap | ✅ Filed as #1075 (M15) | PSP shows value only; no self-interpreting sentence; political advisor (Andreas) cannot brief Minister from number alone; paired with #1065 (Zone 1B); walkthrough narration path available |
| G8 Step 6c escalations | ✅ RECORDED 2026-06-20 | #1065 updated: now CRITICAL across 3 personas, north star FAIL; #1069 updated: CRITICAL across 2 personas, north star FAIL; EL exception paths documented on both |
| G8 EL decision — north star FAIL acceptance | ✅ RECORDED 2026-06-20 | EL accepted FAIL verdict as honest evidence of M14 underdelivery against Layer 3 / PSP promise. Decision: retain all promises as explicit M15 roadmap items in narration rather than scrubbing or claiming delivery. More honest than a pass achieved by narrowing the claim. |
| G8 Honest narration revision | ✅ COMPLETE 2026-06-20 (PR #1078) | `stakeholder-walkthrough.md` revised: (1) Layer 3 sentence framed as M15 roadmap commitment throughout; (2) dual reserve values explicitly disambiguated in Frame C narration (3.8=initial entry-state, 2.9=current simulated step 3); (3) PSP 0.65 translated into plain language in Frame D narration; (4) DEMO-100 presenter timing note added (Section 1 must complete before Frame C displayed). |
| G8 North star re-evaluation | ✅ **PASS** (conditional) | Targeted re-evaluation: revised narration allows Aicha to state primary finding without specialist mediation — presenter explicitly narrates "CRITICAL is one step away" from on-screen data, and disambiguates dual reserve values before she can question them. Condition: revised narration delivered as written. North star gate: **UNBLOCKED**. |
| G8 Step 9 — simulated stakeholder session | ✅ **COMPLETE 2026-06-20 (PR #1081)** | Simulated session (EL decision: real external participants not yet available; #843 deferred to M15). Four-persona panel: Lucas P1, Eleni P2, Andreas P3, Aicha P5. North star: **PASS (conditional)** — Aicha stated argument: "The figure you are challenging is from your institution's own publication. Our initial conditions are derived from IMF WEO April 2024." 8 new findings DEMO-122–129 (all MEDIUM or LOW). Artifact: `docs/demo/m14/reviews/2026-06-20-v0.14.0-stakeholder-review.md`. |
| G8 new findings from Step 9 | ✅ DISPOSITIONED 2026-06-20 | DEMO-122 → #1083; DEMO-127 → #1084; DEMO-123 → #1088; DEMO-124 → #1089; DEMO-129 → #1090 (all M15 scope). DEMO-125/126/128 → confirmed M15 scope (companions to #1065, #1066, #1069). DEMO-123/124/129 slipped M14 close; filed as M15 issues at 2026-06-20 HORIZON sweep. |
| #843 live external demo | ⬜ **DEFERRED TO M15** (EL decision 2026-06-20) | M14 simulated session accepted as closure evidence; real external participants required in M15. |

**Evidence base for M14 trust architecture (both ADRs):**
- Part I audit (output legibility): `docs/demo/m14/reviews/2026-06-15-ux-legibility-audit-minister-exercise.md`
- Part II audit (input confidence): `docs/demo/m14/reviews/2026-06-15-ux-input-confidence-audit-minister-exercise.md`

---

### M13 Sprint Group Status (reference)

| Group | Issues | Wave | ADR gate | Status |
|---|---|---|---|---|
| G1 — DEMO legibility | #872, #874 | Wave 1 | None | ✅ MERGED 2026-06-12 (PR #913) |
| G2 — DEMO trajectory/Mode 3 | #871, #873, #875, #876 | Wave 1 | None | ✅ MERGED 2026-06-12 (PR #914) |
| G3 — Engine fix (reserves floor) | #799 | Wave 1 | None | ✅ MERGED 2026-06-12 (PR #912) |
| G4 — Documentation | #27, #822, #847 | Wave 1 | None | ✅ MERGED 2026-06-12 (PR #915) |
| G5 — ADR-013 authorship | #792 | Wave 1 | N/A | ✅ ACCEPTED 2026-06-12 (PR #916) |
| G6 — Political economy integration | #392 | Wave 2 | ADR-013 ✅ | ✅ COMPLETE 2026-06-12 (PR #919, BPO ACCEPT, #392 closed) |
| G7 — Alert panel master-detail | #852 | Wave 3 | ADR-014 ✅ (accepted 2026-06-12) | ✅ COMPLETE 2026-06-13 (PR #936, BPO ACCEPT, #852 closed) |
| G8a — Standards/methodology/calibration | #45, #27 R1–R3, #271 (tag only), #823, #824 | Wave 3 | None | ✅ COMPLETE 2026-06-13 (PR #943, #27/#45/#271 closed; #823/#824 domain sign-offs pending) |
| G8b — Mode transition UX | #393 | Wave 3 | None | ✅ COMPLETE 2026-06-13 (PR #949, BPO ACCEPT, #393 closed) |

**Status:** All G1–G8 complete. M13 primary objectives: ADR-013 ✅, G6 ✅, G7 ✅, G8 ✅. PI Agent sprint exit confirmation and M13 exit ceremony (#264) are the remaining actions.

### G8 Sprint — Active Work Streams

**Sprint entry:** `docs/process/sprint-plans/m13-g8-sprint-entry.md` — EL-approved 2026-06-13 (PR #939)
**Sprint plan updated:** `docs/process/sprint-plans/m13-sprint-plan.md` — G8 Wave 3 added (PR #940)

**G8a — COMPLETE (PR #943, merged 2026-06-13):**
- ✅ #45 — HCL indicator standards (CODING_STANDARDS.md + DATA_STANDARDS.md) — CLOSED
- ✅ #27 R1–R3 — Calibration doc residuals (Propagation Rules section + demo docstring + ADR-001 note) — CLOSED
- ✅ #271 — Reversibility classification metadata tag (ReversibilityClassification enum, REVERSIBILITY_REGISTRY, Quantity field, round-trip serde, 24 tests) — CLOSED
- ✅ #823 — Ecological composite fixed denominator — CM APPROVE 2026-06-13 (3 constraints: fix at first call not step 0; zero-indicator → None; audit Greece fixture; implementation unblocked)
- ✅ #824 — MENA arid-economy elasticity calibration — CM + EE APPROVE 2026-06-13 (binding: −0.04, Tier 3, FAO GFR arid-subset/ICARDA, biome_class `arid_semiarid`, fallback to `high_forest_cover` with WARNING; implementation unblocked)

**G8b — COMPLETE (PR #949, BPO ACCEPT 2026-06-13, #393 closed):**
- #393 — Mode 1→2 step position preservation
  - Intent document: `docs/process/intents/G8b-2026-06-13-mode-transition-step-preservation.md`
  - ✅ Step 2 QA: `mode-transition.spec.ts` (9 E2E) + `mode-selector.test.tsx` (31 unit) — PR #947
  - ✅ Step 3 Implementation: `ModeSelector.tsx`, `ModeTransitionModal.tsx`, `setMode` store action, `current-step-display` testid — PR #949
  - ✅ Step 4 Verify: 9/9 E2E pass; AC-2 test spec correction (PR #953)
  - ✅ Step 5 BPO Validate ACCEPT: Sri Lanka 2022 marquee — Mode 1→2 at step 3 in 776ms; step preserved; entity retained; Layer 3 PASS — PR #954

**M14 deferrals confirmed (HORIZON sweep 2026-06-13):**
#22 (uncertainty quantification — M14 primary deliverable candidate), #35 (dynamic relationship weights), #102 (distributional comparison), #274 (25-year trajectory), #394 (multi-scenario comparison), #837 (config-driven demo scripts)

### Near-Term Backlog (M13 board, not in sprint waves)
All near-term issues dispositioned at HORIZON sweep 2026-06-13 — see G8 sprint and M14 deferrals above. No items remain in undispositioned near-term backlog.

---

## Open PRs

| PR | Title | Target | Status |
|---|---|---|---|
| #1098 ✅ | fix(m15-g1): guard getIndicatorDisplayNameAny against undefined key (NM-051) | release/m15 | Merged 2026-06-21 |
| #1097 ✅ | feat(m15-g1): Layer 3 IR fixes — trajectory sentence, zero-step suppression, L0 badges, grounding strip disambiguation, PSP sentence | release/m15 | Merged 2026-06-21 |
| #1096 ✅ | test(m15-g1): QA Lead Steps 1+2 — AC-1–AC-11 authored before implementation | release/m15 | Merged 2026-06-21 |
| #1095 ✅ | process(m15-g1): sprint entry document — Layer 3 IR fixes (EL-approved) | release/m15 | Merged 2026-06-20 |
| #1081 ✅ | demo(m14-g8): Step 8 + Step 9 — stakeholder review placeholder and simulated session artifact | release/m14 | Merged 2026-06-20 |
| #1080 ✅ | chore(m14): rename milestone — "Trust Architecture and Instrument Credibility" | release/m14 | Merged 2026-06-20 |
| #1078 ✅ | docs(m14-g8): honest narration revision — retain M15 promises, remove false current-delivery claims | release/m14 | Merged 2026-06-20 |
| #1076 ✅ | demo(m14-g8): Step 6c audience simulation artifact — four-persona panel, north star FAIL/BLOCKED | release/m14 | Merged 2026-06-20 |
| #1071 ✅ | docs(ir004-path-b): correct Zone 1A badge narration to Zone 1D in walkthrough | release/m14 | Merged 2026-06-20 |
| #1070 ✅ | docs(ir-review): update IR review findings table with GitHub issue numbers (#1065–#1069) | release/m14 | Merged 2026-06-19 |
| #1064 ✅ | docs(demo): M14 independent review — 2026-06-19-v0.14.0-ir-review.md | release/m14 | Merged 2026-06-19 |
| #1060 ✅ | docs(demo): M14 Demo 5 internal review + walkthrough corrections (DEMO5-001—007) | release/m14 | Merged 2026-06-19 |
| #1058 ✅ | feat(demo): Round 3 spec fixes — reserve floor visible in Zone 1B detail slot | release/m14 | Merged 2026-06-19 |
| #1057 ✅ | chore(state): G8 Phase 1 demo prep complete — Steps 2–5 merged PR #1056 | release/m14 | Merged 2026-06-19 |
| #1056 ✅ | demo(m14-g8): Steps 2–5 Demo 5 prep — ZMB screenshot brief, narrated spec, demo.sh, walkthroughs | release/m14 | Merged 2026-06-19 |
| #1054 ✅ | process(m14-g8): G8 sprint entry document — Demo 5 preparation and live stakeholder demo | release/m14 | Merged 2026-06-19 |
| #1045 ✅ | feat(m14-g6): methodology, calibration, and instrument legibility (#885, #950, #884, #823, #824, #22, PMM anchor) | release/m14 | Merged 2026-06-18 |
| #1043 ✅ | process(m14-g7): BPO ACCEPT — G7 governance and onboarding documentation | release/m14 | Merged 2026-06-18 |
| #1042 ✅ | process(m14-g6): QA tests filed + §2.4 gate checked (duplicate merge of #1041 content) | release/m14 | Merged 2026-06-18 |
| #1041 ✅ | process(m14-g6): QA tests filed + §2.4 gate checked — EL-approved entry complete | release/m14 | Merged 2026-06-18 |
| #1040 ✅ | process(m14-g6): record EL approval — sprint entry approved 2026-06-18 | release/m14 | Merged 2026-06-18 |
| #1039 ✅ | process(m14-g6b): PI Agent sprint exit — G6b COMPLETE | release/m14 | Merged 2026-06-18 |
| #1038 ✗ | process(m14-g6): G6 sprint entry — QA tests filed (closed without merge; superseded by #1041) | release/m14 | Closed 2026-06-18 |
| #1037 ✅ | docs(m14-g7): governance and onboarding documentation suite (#988, #989) | release/m14 | Merged 2026-06-18 |
| #1036 ✅ | fix(m14-g6): resolve intent document appendix — DA-G6-1, DA-G6-2, CM-G6-1 confirmed | release/m14 | Merged 2026-06-18 |
| #1035 ✅ | chore(state): G6c COMPLETE — Zone 1A Phase 1 design thinking merged PR #1033 | release/m14 | Merged 2026-06-18 |
| #1034 ✅ | design(m14-g6b): Path 2 design artifacts — field mapping UX, USER_SUPPLIED provenance, data isolation | release/m14 | Merged 2026-06-18 |
| #1033 ✅ | docs(m14-g6c): Zone 1A Phase 1 design thinking — per-mode cognitive questions, breaking points, concrete directions | release/m14 | Merged 2026-06-18 |
| #1032 ✅ | process(m14-g6b): G6b Step 1 design intent — Path 2 ministry-owned data upload groundwork | release/m14 | Merged 2026-06-18 |
| #1031 ✅ | process(m14-g5): Step 4 Verify PASS, Step 5 BPO ACCEPT, sprint exit filed | release/m14 | Merged 2026-06-18 |
| #1030 ✅ | feat(m14-g5): ADR-015 Evidence Thread Architecture — Components 1, 2, 3 | release/m14 | Merged 2026-06-18 |
| #1029 ✅ | docs(ki-004): Node.js 20 deprecation warning on actions/checkout@v4 and setup-node@v4 | release/m14 | Merged 2026-06-18 |
| #1026 ✅ | process(m14-g5): record Data Architect decisions DA-G5-1 through DA-G5-5 | release/m14 | Merged 2026-06-18 |
| #1025 ✅ | feat(m14-g5): G5 Step 1 implementation intent document — ADR-015 Components 1, 2, 3 | release/m14 | Merged 2026-06-18 |
| #1023 ✅ | process(m14-g5): record EL approval and correct Data Architect consultation role | release/m14 | Merged 2026-06-17 |
| #1022 ✅ | process(m14-g5): G5 sprint entry — ADR-015 Components 1–3 + SESSION_STATE | release/m14 | Merged 2026-06-17 (EL merge) |
| #1021 ✅ | fix(vite): usePolling: true for Docker HMR on macOS + NM-046 near-miss registry | release/m14 | Merged 2026-06-17 |
| #999 ✅ | process(m14-g1): enforce M{N}-G{N} naming for intent docs and E2E tests; file G1 intent | release/m14 | Merged 2026-06-16 |
| #980 ✅ | docs(process): KI-003 — GitHub Rulesets bootstrap problem for new required checks | release/m14 | Merged 2026-06-16 |
| #979 ✅ | ci(branch-naming): enforce milestone-scoped branch names for release/m* PRs (#978) | release/m14 | Merged 2026-06-16 |
| #977 ✅ | docs(m14-sprint-plan): add G6b — Path 2 design groundwork parallel group | release/m14 | Merged 2026-06-16 |
| #974 ✅ | docs(ux): Journey A gap markers GA-01 + GA-02 — two-path data sourcing resolution | release/m14 | Merged 2026-06-16 |
| #972 ✅ | docs(process): CI gate enforcement — release-branch-ci-gate Ruleset; remove --admin from SESSION_STATE rule | release/m14 | Merged 2026-06-16 |
| #969 ✅ | docs(adr-016): provenance amendment — STRUCTURAL_ABSENCE as provenance type, not proxy indicator | main | Merged 2026-06-16 |
| #959 ✅ | docs(m14): UX legibility audit (Part I) + ADR-015 Model Legibility Architecture | main | Merged 2026-06-15 |
| #960 ✅ | docs(m14): UX input confidence audit (Part II) — IC family + Scenario Grounding framework | main | Merged 2026-06-15 |
| #964 ✅ | docs(arch): ADR-016 Scenario Grounding Architecture (M14 Wave 1) + ARCH-010 | main | Merged 2026-06-15 |
| #966 ✅ | fix(adr-016): correct API contract authority — Data Architect Agent not Chief Engineer | main | Merged 2026-06-16 |
| #967 ✅ | docs(adr-016): EL acceptance — Proposed → Accepted, all decisions recorded | main | Merged 2026-06-16 |
| — | feat(m14): kickoff — sprint plan + session state — pushed directly to release/m14 (efdb25e) | release/m14 | Committed 2026-06-16 (no PR — direct push; note process deviation; release branch is unprotected) |
| #969 ✅ | feat(m14): ADR-016 entity scope EL decision + ARCH-010 review | release/m14 | Merged 2026-06-16 |
| #972 ✅ | feat(m14): ADR-015 Evidence Thread Architecture + ARCH-009 | release/m14 | Merged 2026-06-16 |
| #974 ✅ | feat(ux): Journey A gap markers GA-01 GA-02 in user-journeys.md | release/m14 | Merged 2026-06-16 |
| #977 ✅ | feat(ci): branch-naming milestone prefix enforcement workflow | release/m14 | Merged 2026-06-16 |
| #979 ✅ | chore(ci): add branch-naming to release-branch-ci-gate Ruleset | release/m14 | Merged 2026-06-16 |
| #980 ✅ | docs(ki-003): GitHub Rulesets bootstrapping problem | release/m14 | Merged 2026-06-16 |
| #981 ✅ | chore(state): M14 session state — CI gate, branch naming, Path 1/2, journey markers | release/m14 | Merged 2026-06-16 |
| #909 ✅ | feat(m13): kickoff — sprint plan, entry doc, ADR backlog | release/m13 | Merged 2026-06-12 |
| #910 ✅ | chore(state): M13 kickoff session state | release/m13 | Merged 2026-06-12 |
| #911 ✅ | feat(m13): EL approval recorded — sprint plan + entry doc | release/m13 | Merged 2026-06-12 |
| #912 ✅ | feat(g3): reserves non-negativity floor | release/m13 | Merged 2026-06-12 |
| #913 ✅ | fix(g1): DEMO legibility fixes — DEMO-060 DEMO-061 | release/m13 | Merged 2026-06-12 |
| #914 ✅ | feat(g2): DEMO trajectory and Mode 3 comparison display | release/m13 | Merged 2026-06-12 |
| #915 ✅ | docs(g4): calibration basis, stakeholder walkthrough, data standards | release/m13 | Merged 2026-06-12 |
| #916 ✅ | docs(adr): ADR-013 political economy module boundary (#792) | release/m13 | Merged 2026-06-12 |
| #919 ✅ | feat(political-economy): G6 — ADR-013 political economy integration | release/m13 | Merged 2026-06-12 |
| #921 ✅ | docs(adr): ADR-014 — alert panel (Zone 1B) master-detail layout (ARCH-008) | release/m13 | Merged 2026-06-12 |
| #923 ✅ | docs(adr-014): rewrite — persistent-detail + scan-only compact list model | release/m13 | Merged 2026-06-12 |
| #924 ✅ | docs(adr-014): promote mock-ups to primary design specification | release/m13 | Merged 2026-06-12 |
| #926 ✅ | docs(adr-014): accepted — EL acceptance vote 2026-06-12 (ARCH-008) | release/m13 | Merged 2026-06-12 |
| #928 ✅ | docs(adr-014): UX Designer independent sign-off — conditional, 3 intent requirements | release/m13 | Merged 2026-06-12 |
| #929 ✅ | process(nm-042): agent generated UX Designer sign-off without independent review | release/m13 | Merged 2026-06-12 |
| #930 ✅ | process(nm-042): structured UX Designer sign-off attestation — session context declaration | release/m13 | Merged 2026-06-12 |
| #935 ✅ | process(g7): EL approval of sprint entry — 2026-06-13 | release/m13 | Merged 2026-06-13 |
| #936 ✅ | feat(g7): Zone 1B persistent-detail layout — ADR-014 (#852) | release/m13 | Merged 2026-06-13 |
| #943 ✅ | feat(g8a): close #27 R1-R3, #45, #271 — calibration docs, HCL standards, reversibility schema | release/m13 | Merged 2026-06-13 |
| #947 ✅ | test(g8b): QA Lead — mode transition tests authored before implementation (#393) | release/m13 | Merged 2026-06-13 |
| #949 ✅ | feat(g8b): mode transition step preservation — ModeSelector, modal, setMode, step display | release/m13 | Merged 2026-06-13 |
| #953 ✅ | fix(g8b): AC-2 test spec correction — entity identifier containment not strict equality | release/m13 | Merged 2026-06-13 |
| #954 ✅ | process(g8b): BPO ACCEPT — mode transition step preservation (#393) | release/m13 | Merged 2026-06-13 |
| #955 ✅ | chore(state): G8b COMPLETE — BPO ACCEPT 2026-06-13; all G1–G8 done; M13 exit next | release/m13 | Merged 2026-06-13 |
| #956 ✅ | fix(e2e): update Zone 1B and mode-indicator tests for G7/G8b observable state changes (NM-044) | release/m13 | Merged 2026-06-15 |
| — | chore(m13-exit): M13 exit ceremony — pushed directly to release/m13 (9d86e8e) | release/m13 | Committed 2026-06-15 (no PR — direct push; note process deviation) |

## M11 Work Streams — 2026-06-04 Sprint

16-group sprint targeting 113 open M10/M11 issues. Groups G14–G16b completed this session.

| Group | PR | Issues Closed | Description |
|---|---|---|---|
| G14 (CI fix) | #702 ✅ | — | Fix `test_build_greece_scenario_has_five_initial_attributes` broken by trend_growth seed added in prior session |
| G15 | #703 ✅ | #40 #29 | ADR-011 non-linear propagation — PropagationMode enum (LINEAR/THRESHOLD/CASCADE), per-rule mode selection, cascade-validation-report.md, ADR-011 panel review |
| G16a | #704 ✅ | #96 #93 #157 | Political economy orchestration — InputSource.CONDITIONALITY + constraining fields, implementation_capacity scaling via get_events(), CompoundStateCondition AND/OR logic |
| G16b | #705 ✅ | #156 #159 #272 #273 #679 | PoliticalEconomyModule — legitimacy dynamics (fragility amplifier ×1.5 below 0.5 threshold), programme survival probability (DIRECTION_ONLY, tier 4), elite capture divergence (HUMAN_DEVELOPMENT framework), PoliticalContext schema, WebScenarioRunner integration, conditionality_decomposer |
| G17 | #707 ✅ | #215 #404 | Matrix engine (ADR-009 accepted 2026-06-03): `matrix_propagation.py` (propagate_matrix, LINEAR/THRESHOLD/CASCADE modes, Decimal↔float64 via str, semantic divergences documented), `matrix_tools.py` (trace_propagation, visualize_weight_matrix, profile_propagation), `test_equivalence_harness.py` (14 tests, ADR-009 §Decision 2 gate 1e-10 on all Quantity.value), `scripts/benchmark_phase2.py` (iterative vs matrix A/B report, §Decision 3 MC gate 1000×15 steps) |
| G19 | #710 ✅ | #147 #152 #36-DB | entity_state_snapshot JSONB on tombstones (populated at DELETE with last snapshot.state_data); engine_version_hash TEXT on scenarios (populated with `_GIT_COMMIT_HASH` at creation, returned by GET /scenarios/{id}); git_commit_hash ORM schema drift fix on ScenarioDeletedTombstone; MDA-DEBT-FOREIGN-CURRENCY-ROLLOVER threshold (foreign_currency_pct ≥ 0.60, gte, Tier 3) seeded in migration a4f2b6d8e1c9; 25 unit tests in `test_g19_tombstone_snapshot_engine_hash.py` |
| G20 | #711 ✅ | #151 #154 #155 | STATE_DATA_ENVELOPE_VERSION bumped "2"→"3"; `_steps_projected` added to state_data envelope at write time (records projection horizon for output-layer effective_tier computation); IA1_CANONICAL_PHRASE extended with horizon degradation schedule (+1 tier per 5 steps, capped at Tier 5); ADR-001 IA-1 marked RESOLVED (M11); `write_fidelity_artifact()` added to fidelity_report.py (JSON artifact {case_id}-{date}-{sha8}.json, CI upload-artifact@v4); `POST /scenarios/restore` endpoint (reconstructs tombstone into pending scenario, name-conflict safe, version-gate via check_reconstruction_compatibility()); 31 unit tests in `test_g20_horizon_degradation_restore.py`; 1062 total unit tests passing |
| G21 (docs) | #713 ✅ | #681 | Political economy module user stories — `docs/ux/user-stories-political-economy-m11.md`; 20 Given/When/Then stories across 11 groups: PoliticalContext configuration, implementation_capacity scaling, legitimacy seeding, social response events (fragility amplifier), conditionality structured inputs, conditionality decomposition, programme survival probability, CompoundStateCondition QA contract, elite capture coefficient, distributional divergence Zone 2 placement, Argentina backtesting DIRECTION_ONLY validation; all stories `[pytest]` / `[Playwright]` / `[Manual]` tagged; retrospective spec against G16a/G16b (PRs #703/#705) |

**Political economy module ships as M11 stretch goal (EL decision 2026-06-03).** ADR-011 (non-linear propagation) is the first M11 ADR accepted.

**M11 primary objective (matrix engine investigation) status:** COMPLETE

---

## Open Issues — M12 (Active Control and External Sector)

**GitHub Milestone:** 13 | **Status: CLOSED (2026-06-11)**

All M12 issues closed or migrated. GitHub Milestone 13 closed 2026-06-11.
Exit checklist #263 closed 2026-06-11 — full sign-off comment on the issue.
Six DEMO issues (#871–#876, DEMO-059–064) deferred to M13 with rationale (north star PASS; gaps documented in stakeholder review).
#843 (live external demo) deferred to M14 (EL decision 2026-06-11); M12 simulated session stands as M12 demo evidence.
**Demo screen recording uploaded to GitHub release v0.12.1** — https://github.com/PublicEnemage/worldsim/releases/tag/v0.12.1 (2026-06-11)

**Issue disposition summary:**
- All immediate-horizon M12 deliverables shipped (G1–G8, Wave 1 complete)
- #843 live demo → M14 | #852 alert panel UX → M13
- **#263 exit checklist → M12** (corrected 2026-06-11; gates on #843 + Phase 0 endorsement)
- Near-term issues (#392/#271/#393/#394/#27/#45) → M13
- Further near-term (#97/#153/#569/#30/#92/#259/#275) → M14
- Long-term (#214/#278/#407/#4/#5) → parking lot

---

## M12 Sprint Status — Wave 1 (2026-06-05)

Sprint plan: `docs/process/sprint-plans/m12-sprint-plan.md`
Release branch: `release/m12`
CI hotfix: NM-035 filed; `ci.yml` PR trigger updated to include `release/m*` (PR #772). `workflow_dispatch` + `force_backtesting` input added (PR #776). All G1–G7 PRs verified — backtesting suite passed on `release/m12` (run 27049255730, 2026-06-05).

**EL decision (2026-06-05):** Re-verification not required for unit/integration/E2E (covered by PR #775 CI). Backtesting gap closed via manual `workflow_dispatch` on `release/m12` — all jobs green including backtesting (53s) and Playwright E2E (3m23s). Fidelity report artifact uploaded. EL satisfied.

| Group | PR | Issues | Status |
|---|---|---|---|
| G1 — Instrument cluster display | #762 | #744 #747 | ✓ DONE |
| G2 — Alert panel drill-in | #764 | #745 | ✓ DONE |
| G3 — Mode 2 fiscal multiplier | #767 | #746 | ✓ DONE |
| G4 — Matrix engine production | #769 | #749 | ✓ DONE |
| G5 — External sector module | #773 | #751 #752 | ✓ DONE (ADR-012 accepted by EL 2026-06-05) |
| G6a — Multi-country backend | #775 | #754 #103 | ✓ DONE |
| G6b — Mode 3 Active Control | #778 | #753 | ✓ DONE |
| G7 — Cloud compute path doc | #774 | #750 | ✓ DONE |
| NB-7 — Mode 1 COMPARE_VIEW spec | #788 | #451 | ✓ DONE |
| NB-6 — ESLint audit (react-hooks/react-refresh) | #789 | #644 | ✓ DONE |
| NB-4 — Investment climate state variables | #790 | #34 | ✓ DONE |
| Mode 3 E2E fix + ia1_disclosure + cohort gap | #794 | #793 | ✓ DONE (NM-036 filed) |
| G8 — Demo 4 preparation | #796 | #755 | ✓ DONE 2026-06-07 (Jordan/Egypt Hormuz; PR #796) |
| G8b — Demo 4 critical fixes | #798 | DEMO4-001 DEMO4-002 | ✓ DONE 2026-06-07 (reserves + unemployment unfrozen; NM-037 NM-038 filed; Issue #799 opened) |
| G8c — Internal review artifact | #801 | — | ✓ DONE 2026-06-07 (`docs/demo/m12/reviews/2026-06-07-v0.12.0-internal-review.md`; 9 findings) |
| #814 fix — AlertDetailPanel scroll | #816 | #814 | ✓ DONE 2026-06-09 (`scrollIntoView` on mount; Zone 1B 135px → detail panel below fold) |
| G9 — Political economy module | — | ADR-013 | DEFERRED TO M13 (EL decision 2026-06-07: option B) |
| M12 exit compliance | #830 #831 #832 | SCAN-026 (0 violations), ADR-012 diagram, 7 ADR renewals to M13, demo walkthrough, Phase 2 A/B, NM-036 test | ✓ DONE 2026-06-10 — all M12 agent deliverables complete |
| Mode 3 scenario evaluation | #833 | `docs/demo/m12/reviews/scenario-evaluation-mode3-deliberation.md` + `scenario-evaluation-mode3-recommendation.md` — Dev Economist + Chief Methodologist panel; 4 variant runs (A/B/D); retain current fixture; branch step 3 at 1.30×; reserve invariant documented | ✓ DONE 2026-06-10 |
| Walkthrough pre-IR revision | #834 | Two-act structure; human moment opening ("There is a room where this happens"); NARRATION-RULING-1 at Steps 3–6; Greece 2014 GDP-vs-human-development asymmetry at Step 7; Argentina MAGNITUDE calibration elevated; Customer Agent accessibility corrections | ✓ DONE 2026-06-10 |
| Walkthrough conditionality framing | #835 | Step 5 clawback reading (GCC 17.73%→16.59% at step 4; conditionality 16.59%→17.25% at step 5); Step 6 precise branch mechanics ("IMF liquidity stays; austerity does not"); Step 6 reserve invariant caveat (reserves drain identically; "The reserve crisis is survived under better conditions, not avoided") | ✓ DONE 2026-06-10 |
| Walkthrough Section 4 roadmap | #836 | Feature-list replaced with capability-gaps framing — three gaps (political feasibility, conditionality design, medium-term horizon) each in Umbrella→Fact→Synthesis structure; M14 demo cadence caveat; max length +50% | ✓ DONE 2026-06-10 |
| Demo prep Steps 3 + 4 | #838 | demo.sh: M12 presenter guide (Jordan/Egypt Hormuz, 22-min two-act timing, reserve invariant caveat, demo-narrated.spec.ts reference); demo-narrated.spec.ts: M12 Playwright narrated spec — 8-step JOR/EGY scenario with commodity_price_shocks + governance seeds, Mode 3 branch at step 3 (1.30× fiscal multiplier), five frame captures at 1440×900 (frame-a–frame-e-step5-divergence.png), no-drawer Zone 1 always-visible UI pattern | ✓ DONE 2026-06-10 |

## Process Redesign Sprint — Phase A Status

**Phase A: Agent Execution Lifecycle**
**Status:** COMPLETE — EL endorsement recorded 2026-06-12 (PR #900). Phase B COMPLETE.

| Step | Agent | Output | PR | Status |
|---|---|---|---|---|
| 1 — Intent document template + observable application state definition | Architect Agent | `docs/process/intent-template.md`; `CLAUDE.md §Agent Execution Lifecycle — Observable Application State` | #900 | ✅ Merged 2026-06-12 |
| 2 — Rejection artifact specification + enforcement language | PI Agent | `CLAUDE.md §Agent Execution Lifecycle — When Verify or Validate fails` | #900 | ✅ Merged 2026-06-12 |
| 3 — Validate step + north star integration + Layer 3 gate (FD-2) | Business PO | `CLAUDE.md §Agent Execution Lifecycle — Step 5` and `§Layer 3 Quality Gate` | #900 | ✅ Merged 2026-06-12 |
| 4 — Complete lifecycle + Kryptonite constraint (FD-3) | Architect Agent | `CLAUDE.md §Agent Execution Lifecycle` (full section) | #900 | ✅ Merged 2026-06-12 |
| 5 — Enforcement review + exit artifact | PI Agent + PM Agent | `docs/process/sprint-plans/process-redesign-phaseA-exit.md` | #900 | ✅ Merged 2026-06-12 |
| 6 — EL endorsement | EL | `docs/process/sprint-plans/process-redesign-phaseA-exit.md §Part VII` | #900 | ✅ Endorsed 2026-06-12 |

**Phase B complete:** `docs/process/sprint-plans/process-redesign-phaseB-exit.md` — **EL endorsed 2026-06-12 (PR #902). Phase C COMPLETE.**

**Phase C complete:** `docs/process/sprint-plans/process-redesign-phaseC-exit.md` — **EL endorsed 2026-06-12 (PR #904). Phase D COMPLETE.**

**Phase D complete:** `docs/process/sprint-plans/process-redesign-phaseD-exit.md` — **EL endorsed 2026-06-12 (PR #906). Process Redesign Sequence (Phases 0–D) CLOSED.**

**Gaps closed by Phase A:**

| Gap | Closed by | Location |
|---|---|---|
| Execution lifecycle gap — no gate between "ADR accepted" and "PR merged" | Five-step lifecycle with enforcement gates | `CLAUDE.md §Agent Execution Lifecycle` |
| Rejection artifact gap — Verify failure had no mandatory consequence | Rejection artifact spec with sprint exit block + near-miss obligation | `CLAUDE.md §Agent Execution Lifecycle — When Verify or Validate fails` |
| **FD-2** — Layer 3 self-interpreting output has no process owner | Customer Agent Layer 3 gate at Validate step | `CLAUDE.md §Agent Execution Lifecycle — Layer 3 Quality Gate` |
| **FD-3** — Kryptonite frame never governs tradeoffs | Kryptonite design constraint at Intent authorship + Validate | `CLAUDE.md §Agent Execution Lifecycle — Kryptonite Design Constraint` |
| Intent document format gap — no standard for Implementation Intent | Canonical template with observable application state + Kryptonite check | `docs/process/intent-template.md` |

## Process Redesign Sprint — Phase B Status

**Phase B: Business PO Acceptance Protocol**
**Status:** COMPLETE — EL endorsement recorded 2026-06-12 (PR #902). Phase C OPEN.

| Step | Agent | Output | PR | Status |
|---|---|---|---|---|
| 1 — Per-work-type verification criteria (frontend, backend, docs, analytics) | Business PO | `docs/process/acceptance-protocol.md §Part 1` | #902 | ✅ Merged 2026-06-12 |
| 2 — Exception path specification + enforcement review | PI Agent | `docs/process/acceptance-protocol.md §Part 2` | #902 | ✅ Merged 2026-06-12 |
| 2b — ACCEPT mode in agents.md §Business PO | Business PO | `docs/process/agents.md §Business Product Owner Agent` | #902 | ✅ Merged 2026-06-12 |
| 2c — Sprint Exit Gate in sprint-planning-sop.md | PM Agent | `docs/process/sprint-planning-sop.md §Sprint Exit Gate` | #902 | ✅ Merged 2026-06-12 |
| 3 — Phase B exit artifact + Phase C sprint entry | PM Agent | `docs/process/sprint-plans/process-redesign-phaseB-exit.md`; `docs/process/sprint-plans/process-redesign-phaseC-sprint-entry.md` | #902 | ✅ Merged 2026-06-12 |
| 4 — EL endorsement | EL | `docs/process/sprint-plans/process-redesign-phaseB-exit.md §Part VII` | #902 | ✅ Endorsed 2026-06-12 |

**What Phase B produced:**
- **`docs/process/acceptance-protocol.md`** — per-type verification checklists (frontend, backend, docs, analytics); DEMO4 class check explicit in backend protocol; asymmetry test operationalizes FD-3 at Validate step; Customer Agent Layer 3 as precondition (not follow-up); rejection artifact triggers + format + re-acceptance process + EL exception path; PI enforcement review embedded
- **`docs/process/agents.md` amendment** — `PO: ACCEPT` activation mode with canonical protocol reference
- **`docs/process/sprint-planning-sop.md` amendment** — §Sprint Exit Gate: exit conditions, agent responsibilities at exit, what "CI green" does not substitute for, sprint exit artifact format

## Process Redesign Sprint — Phase C Status

**Phase C: Sprint Cadence Formalization**
**Status:** COMPLETE — EL endorsement recorded 2026-06-12 (PR #904). Phase D COMPLETE.

| Step | Agent | Output | PR | Status |
|---|---|---|---|---|
| 1 — Sprint entry + exit document templates | PM Agent | `docs/process/sprint-plans/templates/sprint-entry-template.md`; `docs/process/sprint-plans/templates/sprint-exit-template.md` | #904 | ✅ Merged 2026-06-12 |
| 2a — PM Agent role amendment (sprint boundary obligations) | PM Agent | `docs/process/agents.md §PM Agent — Sprint Boundary Obligations` | #904 | ✅ Merged 2026-06-12 |
| 2b — PI Agent role amendment (sprint boundary enforcement) | PI Agent | `docs/process/agents.md §Process Integrity Agent — Sprint Boundary Enforcement` | #904 | ✅ Merged 2026-06-12 |
| 2c — Sprint Entry Gate in sprint-planning-sop.md | PM Agent | `docs/process/sprint-planning-sop.md §Sprint Entry Gate` | #904 | ✅ Merged 2026-06-12 |
| 3 — Phase C exit artifact + Phase D sprint entry | PM Agent | `docs/process/sprint-plans/process-redesign-phaseC-exit.md`; `docs/process/sprint-plans/process-redesign-phaseD-sprint-entry.md` | #904 | ✅ Merged 2026-06-12 |
| 4 — EL endorsement | EL | `docs/process/sprint-plans/process-redesign-phaseC-exit.md §Part VII` | #904 | ✅ Endorsed 2026-06-12 |

**What Phase C produced:**
- **`docs/process/sprint-plans/templates/sprint-entry-template.md`** — five binary entry invariants (release branch + CI trigger, ADR gates, intent documents, QA test authorship); infrastructure sprint exception; EL approval record
- **`docs/process/sprint-plans/templates/sprint-exit-template.md`** — per-deliverable Business PO acceptance table; Layer 3 sequencing check (before verdict); PI Agent confirmation as Section 5 named gate
- **`docs/process/agents.md` PM Agent amendment** — `§Sprint Boundary Obligations`: sprint entry/exit obligations; EL-approved definition; infrastructure sprint declaration scope
- **`docs/process/agents.md` PI Agent amendment** — `§Sprint Boundary Enforcement`: unconditional near-miss obligation when sprint opens without entry doc; exit gate confirmation role; what PI Agent does and does not do
- **`docs/process/sprint-planning-sop.md` amendment** — `§Sprint Entry Gate`: five entry conditions mirroring exit gate; who confirms; infrastructure exception; entry artifact reference; §Sprint Exit Artifact updated to reference filed document over issue comment

---

## Process Redesign Sprint — Phase D Status

**Phase D: Session Boundary Discipline**
**Status:** COMPLETE — EL endorsement recorded 2026-06-12 (PR #906). Process Redesign Sequence (Phases 0–D) CLOSED.

| Step | Agent | Output | PR | Status |
|---|---|---|---|---|
| 1 — CLAUDE.md §Session Continuity amendment — §Entry and Exit Invariants | PI Agent | `CLAUDE.md §Session Continuity — §Entry and Exit Invariants` | #906 | ✅ Merged 2026-06-12 |
| 2 — PM Agent enforceability review | PM Agent | `docs/process/sprint-plans/process-redesign-phaseD-exit.md §Part III` | #906 | ✅ Merged 2026-06-12 |
| 3 — Phase D exit artifact | PM Agent | `docs/process/sprint-plans/process-redesign-phaseD-exit.md` | #906 | ✅ Merged 2026-06-12 |
| 4 — EL endorsement | EL | `docs/process/sprint-plans/process-redesign-phaseD-exit.md §Part VIII` | #906 | ✅ Endorsed 2026-06-12 |

**What Phase D produced:**
- **`CLAUDE.md §Session Continuity — §Entry and Exit Invariants`** — sprint entry hard stop (PM Agent may not authorize implementation without filed, EL-approved entry document); sprint exit hard stop (CI green + issue closure not sufficient; four named conditions required); "if it isn't written down, it doesn't exist" principle
- **`docs/process/sprint-plans/process-redesign-phaseD-exit.md`** — Phase D exit artifact with PM Agent enforceability review (Part III); PM Agent verdict: language creates genuine obligations; single-principal circularity is real but bounded (not a drafting gap); sequence closure summary (Part VII)

**Gaps closed by Phase D:**

| Gap | Closed by | Location |
|---|---|---|
| CLAUDE.md constitutional gap — sprint entry/exit gates not in primary session reading | §Entry and Exit Invariants in §Session Continuity | `CLAUDE.md §Session Continuity` |
| Agent session start had no sprint boundary obligation visible | Constitutional hard stop visible at every session start | `CLAUDE.md §Session Continuity — §Entry and Exit Invariants` |
| "If it isn't written down" had no operational form | Artifact-as-proof principle: session memory ≠ gate satisfaction | `CLAUDE.md §Session Continuity — §Entry and Exit Invariants` |

**Process Redesign Sequence — all four mechanisms operational:**

| Phase | Mechanism | Primary output | Status |
|---|---|---|---|
| Phase 0 | UX/persona → ADR traceability | ADR template; persona trace; north star process gate | ✅ Complete |
| Phase A | Agent execution lifecycle | Five-step lifecycle; rejection artifact spec; Layer 3 gate; Kryptonite constraint | ✅ Complete |
| Phase B | Business PO acceptance protocol | `acceptance-protocol.md`; ACCEPT mode in agents.md; Sprint Exit Gate in SOP | ✅ Complete |
| Phase C | Sprint cadence formalization | Sprint entry/exit templates; PM + PI role amendments; Sprint Entry Gate in SOP | ✅ Complete |
| Phase D | Session boundary discipline | CLAUDE.md §Entry and Exit Invariants | ✅ Complete |

---

## Process Redesign Sprint — Phase 0 Status

**Phase 0: UX/Persona Traceability Upstream of ADR Development**
**Status:** COMPLETE — EL endorsement recorded 2026-06-11.

| Step | Agent | Output | PR | Status |
|---|---|---|---|---|
| 1 — DIC ROADMAP | Council Orchestrator | 20 binding guardrails + 8-item gap list + Section C requirements | #805 | ✅ Merged |
| 2 — UX traceability spec | UX Designer | 3-tier ADR classification; 7-element UX implication statement; 4 hard UX invariants; Tension 1 resolution; XD-1 observations | #805 | ✅ Merged |
| 3a — Persona traceability spec | Business PO | 7-element valid persona trace; 3-tier persona obligation; canonical cohort list; negotiating leverage statement spec | #806 | ✅ Merged |
| 3b — Persona conflict resolution ruling | Business PO | `docs/ux/personas.md §Section 7` — Closes **XD-1** | #806 | ✅ Merged |
| 4 — ADR template + canonical placement | Architect Agent | `docs/adr/template.md` + CODING_STANDARDS.md reference — Closes **XD-2** | #807 | ✅ Merged |
| 5 — North star test process gate | PI Agent | `CLAUDE.md §North Star Test (Process Gate)` — Closes **FD-1**; 4 template enforcement amendments | #808 | ✅ Merged |
| 6 — EL endorsement | EL | `docs/process/sprint-plans/process-redesign-phase0-exit.md §Part VI` | — | ✅ Endorsed 2026-06-11 |

**Gaps closed:**

| Gap | Closed by | Location |
|---|---|---|
| XD-2 — Mission-to-implementation traceability never required | ADR template (Step 4) | `docs/adr/template.md` |
| XD-1 — Minister vs. specialist persona conflict unresolved | Persona conflict resolution ruling (Step 3) | `docs/ux/personas.md §Section 7` |
| FD-1 — North star test has no process home | North star test process gate (Step 5) | `CLAUDE.md §North Star Test (Process Gate)` |

---

**Internal demo — COMPLETE (command-line phase)**
- `demo_hormuz_jordan.py` run from `release/m12` post-PR-#798. Scenario `937a7999-ce59-4e3f-bc12-100f0912327a`.
- JOR reserves: 7.1→6.2→5.0→3.7→2.5→1.2→0.0→0.0 (CRITICAL MDA step 5 ✓)
- JOR unemployment: 17.77%→18.26% spike at step 5 (fiscal cut Okun's law signal ✓)
- EGY reserves: 5.3→4.8→3.9→2.9→2.0→1.1→0.1→0.1 (CRITICAL MDA step 5 ✓)
- 1292 unit tests pass; ruff clean
- To run demo: `cd backend && python -m scripts.demo_hormuz_jordan` (suppress SIM-INTEGRITY warnings with `2>/dev/null`)

**Process redesign deliberation — ON MAIN (PR #803, 2026-06-08)**
- `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md` — 590 lines
- Full verbatim deliberation: PI Agent + BPO north star test, PM Agent sequencing proposal (Phase 0 + Phases A–D), 11 north star document gaps with failure mode mapping
- Status: SUPERSEDED — Phase 0 endorsed 2026-06-11; Phase A is now open (see Phase 0 section above); all implementation gates cleared
- Also on `release/m12` via PR #802

**Awaiting EL action:**
- ~~Phase 0 EL endorsement~~ — **RECORDED 2026-06-11** (`docs/process/sprint-plans/process-redesign-phase0-exit.md §Part VI`). XD-1, XD-2, FD-1 closed.
- ~~Phase A EL endorsement~~ — **RECORDED 2026-06-12** (PR #900; `docs/process/sprint-plans/process-redesign-phaseA-exit.md §Part VII`). Execution lifecycle gap, FD-2, FD-3 closed. **Phase B outputs filed.** Entry: `docs/process/sprint-plans/process-redesign-phaseB-sprint-entry.md`.
- ~~Phase B EL endorsement~~ — **RECORDED 2026-06-12** (PR #902; `docs/process/sprint-plans/process-redesign-phaseB-exit.md §Part VII`). Acceptance protocol, ACCEPT mode in agents.md, Sprint Exit Gate in SOP active. **Phase C is now open.** Entry: `docs/process/sprint-plans/process-redesign-phaseC-sprint-entry.md`.
- ~~Phase C EL endorsement~~ — **RECORDED 2026-06-12** (PR #904; `docs/process/sprint-plans/process-redesign-phaseC-exit.md §Part VII`). Sprint entry/exit templates, Sprint Entry Gate in SOP, PM Agent + PI Agent sprint boundary obligations active. **Phase D complete.**
- ~~Phase D EL endorsement~~ — **RECORDED 2026-06-12** (PR #906; `docs/process/sprint-plans/process-redesign-phaseD-exit.md §Part VIII`). CLAUDE.md §Entry and Exit Invariants committed. **Process Redesign Sequence (Phases 0–D) CLOSED.**
- ~~Step 6c gate~~ — **PASS (2026-06-11)**: PR #880 resolved DEMO-070/071/081/090; DEMO-080 accepted as-is by EL (tablet scale, out of scope for 1440×900 live demo). Audience simulation review updated. Step 9 unblocked.
- ~~Step 9 simulated session~~ — **COMPLETE (2026-06-11)**. North star verdict: PASS. Aicha: "The conditionality dispute is about who absorbs the employment cost — the reserve crisis happens either way. That argument is now quantified." Artifact: `docs/demo/m12/reviews/2026-06-11-v0.12.1-stakeholder-review.md` (PR #886). Screenshots recaptured with PR #880 UI changes (PR #883). Two new M13 issues: #884 (reserve value not on screen), #885 (Exploratory tier on baseline vs. projection). Per-entity curves (#845) confirmed as primary unresolved UX gap.
- ~~#843 M12 live external demo~~ — **DEFERRED TO M14** (EL decision 2026-06-11). Issue repurposed as M14 closure gate: live stakeholder demo with real external participants, timed to coincide with methodology publication. M12 simulated session (north star PASS) stands as M12 closure evidence. M12 is now formally complete pending only the exit checklist (#263).
- ~~#852~~ — **DEFERRED TO M13** (EL decision 2026-06-11): alert panel master-detail UX requires Frontend architecture review, ADR, UX Designer + Design Thinking agent input.
- ~~#841 DEMO-041~~ — **CLOSED** (PR #854)
- ~~#842 DEMO-039~~ — **CLOSED** (PR #854)
- ~~#850 DEMO-052~~ — **CLOSED** (PR #854)
- ~~#851 DEMO-053~~ — **CLOSED** (PR #854)
- ~~#855 DEMO-054~~ — **CLOSED** (PR #857)
- ~~#856 DEMO-055~~ — **CLOSED** (PR #857)
- ~~#814, #752, #99, #103~~ — **CLOSED** (2026-06-11 board audit; resolved by earlier M12 PRs)
- ~~Merge PR #848~~ — **DONE** (2026-06-11)
- ~~Merge PR #854~~ — **DONE** (2026-06-11)
- ~~Merge PR #857~~ — **DONE** (2026-06-11)
- ~~UI screenshot capture~~ — **COMPLETE** (2026-06-11): all five frames recaptured at correct steps
- ~~Playwright legibility gates~~ — **PASSED** (2026-06-10): 11/11 at 1440×900
- ~~IR review~~ — **COMPLETE** (2026-06-10): 13 findings DEMO-039–051; `docs/demo/m12/reviews/2026-06-10-v0.12.0-ir-review.md`
- ~~Merge `release/m12` → `main`~~ — **DONE** (PR #839, 2026-06-10)

**M12 agent deliverables — ALL COMPLETE (2026-06-10)**

---

## Closed — M13 (Political Economy and Instrument Credibility)

**GitHub Milestone:** 9 | **Formally closed: 2026-06-15** | **Exit ceremony complete 2026-06-15**

**Exit ceremony disposition summary:**
- ~~#264~~ — M13 Exit Checklist — **PENDING EL close** (open until EL merges release/m13 → main and closes)
- ~~#27~~ — calibration basis docs — **CLOSED 2026-06-15** (G8a PR #943; auto-close missed release branch)
- ~~#45~~ — HCL indicator standards — **CLOSED 2026-06-15** (G8a PR #943; auto-close missed release branch)
- ~~#271~~ — reversibility classification — **CLOSED 2026-06-15** (G8a PR #943; auto-close missed release branch)
- ~~#392~~ — political economy constraint modeling — **CLOSED 2026-06-12** (G6 BPO ACCEPT PR #919)
- ~~#393~~ — Mode 1→2 step position preservation — **CLOSED 2026-06-13** (G8b BPO ACCEPT PR #949)
- ~~#792~~ — ADR-013 — **CLOSED 2026-06-15** (G5 accepted PR #916; exit ceremony)
- ~~#799~~ — reserves non-negativity floor — **CLOSED 2026-06-15** (G3 PR #912; exit ceremony)
- ~~#822~~ — denominator disclosure — **CLOSED 2026-06-15** (G4 PR #915; exit ceremony)
- ~~#847~~ — DEMO-046 — **CLOSED 2026-06-15** (G4 PR #915; exit ceremony)
- ~~#852~~ — alert panel Zone 1B — **CLOSED 2026-06-13** (G7 BPO ACCEPT PR #936)
- ~~#871~~ — DEMO-059 PMM — **CLOSED 2026-06-15** (G2 PR #914; exit ceremony)
- ~~#872~~ — DEMO-060 alert clip — **CLOSED 2026-06-15** (G1 PR #913; exit ceremony)
- ~~#873~~ — DEMO-062 Zone 1D — **CLOSED 2026-06-15** (G2 PR #914; exit ceremony)
- ~~#874~~ — DEMO-061 legibility — **CLOSED 2026-06-15** (G1 PR #913; exit ceremony)
- ~~#875~~ — DEMO-063 entity labels — **CLOSED 2026-06-15** (G2 PR #914; exit ceremony)
- ~~#876~~ — DEMO-064 Mode 3 comparison — **CLOSED 2026-06-15** (G2 PR #914; exit ceremony)
- ~~#908~~ — ADR-014 authorship — **CLOSED 2026-06-15** (ADR-014 accepted PRs #921–#930; exit ceremony)
- #22 → **MIGRATED M14** (uncertainty quantification — M14 primary deliverable candidate)
- #35 → **MIGRATED M14** (dynamic relationship weights)
- #102 → **MIGRATED M14** (distributional scenario comparison)
- #274 → **MIGRATED M14** (25-year trajectory)
- #394 → **MIGRATED M14** (multi-scenario comparison)
- #823 → **MIGRATED M14** (ecological composite denominator fix — DIC approval on record: CM APPROVE)
- #824 → **MIGRATED M14** (MENA calibration fix — DIC approval on record: CM + EE APPROVE)
- #837 → **MIGRATED M14** (config-driven demo scripts — HORIZON sweep 2026-06-13)
- #950 → **MIGRATED M14** (Zone 1A Y axis label — HIGH; part of #845 information architecture work)
- #951 → **MIGRATED M14** (solo-use review protocol blind spot)

---

## Closed — M14 (Trust Architecture and Instrument Credibility)

**GitHub Milestone:** 15 | **Created:** 2026-06-11 | **Status: EXIT CEREMONY COMPLETE 2026-06-20** | **Pending EL: release/m14 → main merge, v0.14.0 tag, #968 close**

**Exit ceremony disposition summary:**
- ~~#884~~ — reserve_coverage_months — **CLOSED 2026-06-20** (G6 BPO ACCEPT PR #1045)
- ~~#885~~ — Exploratory confidence tier — **CLOSED 2026-06-20** (G6 BPO ACCEPT PR #1045)
- ~~#950~~ — Zone 1A Y axis label — **CLOSED 2026-06-20** (G6 BPO ACCEPT PR #1045)
- ~~#823~~ — ecological composite denominator — **CLOSED 2026-06-20** (G6 BPO ACCEPT PR #1045)
- ~~#824~~ — MENA calibration — **CLOSED 2026-06-20** (G6 BPO ACCEPT PR #1045)
- ~~#989~~ — onboarding docs — **CLOSED 2026-06-20** (G7 BPO ACCEPT PR #1037)
- ~~#988~~ — Goodhart's Law mitigation — **CLOSED 2026-06-20** (G7 BPO ACCEPT PR #1037)
- ~~#1055~~ — demo preparation — **CLOSED 2026-06-20** (Step 9 complete)
- #843 → **MIGRATED M15** (EL decision 2026-06-20; live external participants in M15)
- #22 → **MIGRATED M16** (M14 delivered tier tag layer; full distributional bands → M16)
- #6, #3, #1007, #1004, #845 → **MIGRATED M15**
- #968 — M14 Exit Checklist — **PENDING EL close** (open until EL merges release/m14 → main)

| Issue | Title | Group | Notes |
|---|---|---|---|
| #843 | plan: M14 closure — live stakeholder demo with real external participants | G8 | **M14 gate issue** |
| #968 | chore(m14): M14 Exit Checklist | — | M14 exit checklist; closure gate: #843 |
| #961 | bug(frontend): entity hardcoded to GRC in scenario creation form | G1 | Implement after EL plan approval |
| #962 | bug(frontend): step counter shows 'Step 0 / 8' on completed scenarios | G1 | Implement after EL plan approval |
| #963 | bug(frontend): choropleth attribute selector displays raw DB field names | G1 | Implement after EL plan approval |
| #884 | ux: reserve_coverage_months not surfaced as readable metric | G6 | ✅ MERGED PR #1045 — awaiting BPO ACCEPT to close |
| #885 | ux: Exploratory confidence tier misclassifies baseline vs. projection | G6 | ✅ MERGED PR #1045 — awaiting BPO ACCEPT to close |
| #22 | feat: uncertainty quantification — disclosure layer (Tier tags per indicator) | G6 | ✅ MERGED PR #1045 — awaiting BPO ACCEPT to close; full distributional bands → M16 |
| #823 | arch(methodology): ecological composite dynamic denominator fix | G6 | ✅ MERGED PR #1045 — awaiting BPO ACCEPT to close |
| #824 | fix(engine): MENA arid-economy elasticity calibration | G6 | ✅ MERGED PR #1045 — awaiting BPO ACCEPT to close |
| #950 | ux: Zone 1A trajectory chart Y axis has no label or unit | G6 | ✅ MERGED PR #1045 — awaiting BPO ACCEPT to close |
| #845 | ux: Zone 1A information architecture — multi-dimensional encoding | G6c | Phase 1 design thinking doc only; Phases 2–4 → M15/M16 |
| #976 | feat(data): Path 2 — proprietary data upload (design artifacts only) | G6b | Design artifacts in M14; implementation → M16 |
| #3 | governance: resolve single-principal separation of duties gap | G7 | EL-action |
| #6 | governance: restore branch protection bypass restriction | G7 | EL-action |
| #988 | governance: Goodhart's Law mitigation — TSC monitoring framework | G7 | Filed 2026-06-16 |
| #989 | docs: onboarding documentation for global south finance ministry analysts | G7 | Filed 2026-06-16 |
| #997 ✅ | Demo 5 scenario script constraint: challenges must be answerable from ADR-015 Components 1–3 | G8 | **CLOSED 2026-06-19** — reserve coverage → Grounding strip citation (EL decision); no Component 4 required |
| #1055 | demo: M14 stakeholder demo preparation — v0.14.0 / Milestone 14 | G8 | Filed 2026-06-19 (Step 1); tracks G8 Phase 1+2 deliverables |
| #843 | plan: live stakeholder demo with real external participants | G8 | **DEFERRED TO M15** (EL decision 2026-06-20) — M14 simulated session accepted as closure evidence |

**M14 exit ceremony status:** G8 Step 9 COMPLETE. All feature work merged. Docker containers rebuilding with latest release/m14 code. Next: M14 exit ceremony (CLAUDE.md §Milestone Exit Ceremony): Step 1 open issue audit, Step 2 reference audit, Step 3 SESSION_STATE consistency check, Step 4 fresh session continuity test. Then EL merges release/m14 → main, tags v0.14.0, closes #968 + GitHub Milestone 15.

---

## Open Issues — M15 (Human Cost Architecture)

**GitHub Milestone:** 16 | **Created:** 2026-06-16 | **Status:** Planned — no demo
*Zone 1A ADR, cohort disaggregation design, Path 1 implementation, accessibility validation. Sets up Demo 6.*

| Issue | Title | Notes |
|---|---|---|
| #845 (Ph 2–3) | ux: Zone 1A information architecture — ARCH-REVIEW + ADR Tier 1 | Phase 1 design thinking doc in M14 G6c |
| #986 | feat(ux): cohort disaggregation on primary surface | Filed 2026-06-16; origin: M11.5 FINDING-03 (HIGH) |
| #987 | feat(ux): political risk summary surface for Persona 3 | Filed 2026-06-16 |
| #975 | feat(data): Path 1 — approved source network query at scenario creation | Journey A GA-01; extends ADR-016 Component 1 |
| #53 | arch: information access architecture (RBAC design) | Prerequisite for Path 2 (#976) implementation in M16 |
| #846 | ux: DEMO-045 — Mode 3 branch comparison values not in instrument | |
| #97 | arch(api): threshold-crossing markers in comparative output | |
| #153 | feat(frontend): absolute threshold overlay on DeltaChoropleth | |
| #92 | arch(backtesting): Greece 2010 investment climate initial conditions | |
| #837 | feat(demo): configuration-driven demo scripts | |
| #259 | standards: CTO legibility metrics dashboard | |
| #569 | test(perf): MV-002 Mode 3 hardware validation | |
| #951 | process: solo-use review protocol | |
| #990 | test: accessibility validation on 8GB/4-core target hardware | Filed 2026-06-16 |
| #1065 | ux(zone-1b): Layer 3 trajectory sentence — Zone 1B shows percentage not directive text | IR-001; Step 6c CRITICAL; escalation comment 2026-06-20 |
| #1066 | ux(zone-1b): suppress "0 consecutive steps" when breach counter is zero | IR-002; Step 6c HIGH |
| #1067 | demo(screenshots): Frame B and Frame C are the same screenshot | IR-003; Step 6c HIGH |
| #1068 | ux(zone-1a): L0 badge implementation on Zone 1A trajectory curve | IR-004 Path A; Step 6c HIGH |
| #1069 | ux(grounding-strip): dual reserve values without disambiguation label | IR-005; Step 6c CRITICAL; escalation comment 2026-06-20 |
| #1075 | ux(zone-1d): PSP self-interpreting sentence absent — political advisor cannot brief without economist mediation | DEMO-099; Step 6c CRITICAL; Filed 2026-06-20 |
| #1083 | ux(grounding-strip): date label shows 2024-Q1 but IMF WEO April is Q2 | DEMO-122; Step 9 MEDIUM; Filed 2026-06-20 |
| #1084 | methodology: PSP has no historical calibration anchor accessible from within the tool | DEMO-127; Step 9 MEDIUM; Filed 2026-06-20 |

---

## Open Issues — M16 (Distributional Visibility — Demo 6)

**GitHub Milestone:** 17 | **Created:** 2026-06-16 | **Status:** Planned — Demo 6
*Human cost ledger operationally visible. Cohort-level output, 25-year trajectory, uncertainty bands, ecological transmission.*

| Issue | Title | Notes |
|---|---|---|
| #102 | feat: distributional scenario comparison — variance + percentile range | Core Demo 6 capability |
| #274 | feat(simulation): 25-year human capital depletion trajectory | Core Demo 6 capability |
| #275 | feat(simulation): calibrated ecological-to-financial transmission | |
| #22 (full) | feat: uncertainty quantification — full distributional bands | Builds on M14 disclosure layer |
| #35 | feat(simulation): dynamic relationship weight updating | |
| #30 | feat: distinguish stock vs. flow variables in entity attribute model | |
| #976 (impl) | feat(data): Path 2 — proprietary data upload implementation | Design in M14 G6b; #53 resolves in M15 first |
| #986 (impl) | feat(ux): cohort disaggregation implementation | Design in M15 |
| #987 (impl) | feat(ux): political risk summary surface implementation | Design in M15 |

---

## Open Issues — M17 (Multi-Scenario Infrastructure)

**GitHub Milestone:** 18 | **Created:** 2026-06-16 | **Status:** Planned — no demo
*Multi-scenario comparison infrastructure, entity template library. Sets up Demo 7.*

| Issue | Title | Notes |
|---|---|---|
| #394 | platform: multi-scenario comparison (>2 scenarios) | Core Demo 7 prerequisite |
| #407 | arch(vision): simulation resolution spectrum — entity template library | |
| #5 | Architecture: data marketplace design | |
| #4 | Data: advanced geocoded dataset integration | |

---

## Closed — M11.5 (Usability Validation and Experience Audit)

**Formally closed: 2026-06-04** | **North Star:** `docs/vision/milestone-11-5-north-star.md` | **GitHub Milestone:** 14 (closed)

| Issue | Title | Gate |
|---|---|---|
| #717 ✅ | Pillar 1 — rrweb session recording integration | **Closed 2026-06-04** — PR #724 merged. `useSessionRecording` hook (rrweb `record()`, `endSession()` POST with once-only guard), `SessionRecordingBanner` (red/green fixed banner), `SessionReplayViewer` (`?replay_session=<id>`), FastAPI `POST/GET/LIST /api/v1/sessions/recording`, session artifact schema v1.0 at `docs/schema/session_recording.yml`, coordinator guide at `docs/ux/usability-sessions/how-to-run-a-session.md`. 14 backend + 9 frontend unit tests. |
| #718 ✅ | Pillar 2 — cold-start usability audit methodology | **Closed 2026-06-04** — PR #727 merged. `docs/ux/usability-sessions/pillar-2-methodology.md`: cold-start protocol, think-aloud schema (5 North Star markers + TRIED/CONCLUDED), facilitation approach, persona sequencing (P2→P1→P5 Priority A; P6/P8 Priority B), session count rationale, trace interpretation, findings classification (CRITICAL/HIGH/MEDIUM/LOW × Discovery/Comprehension/Action), verbatim task prompts for 5 personas. Status: PROPOSED — joint approval on Issue #718 by PM + UD + UT + PO required before Session 1. |
| #719 ✅ | Pillar 3 — session provenance standard and semantic component vocabulary | **Closed 2026-06-04** — PR #730 merged. `pillar-3-provenance.md`: manifest schema (app state, agent config, environment, outcome, artifact links), linking protocol (session_id primary key), versioning strategy (same-PR vocabulary update rule). `vocabulary.md`: 16 zone tokens, component + element tables for all current UI components, data-testid cross-refs, v1.0 changelog. `session_recording.yml` Pillar 3 stub resolved. `docs/ux/usability-sessions/manifests/` directory created. |
| #720 ✅ | Milestone 11.5 Exit Checklist | **Closed 2026-06-04** — exit verdict NOT READY — EVIDENCE COMPLETE; M12 blocking issues #744–#747 filed |

**M11.5 Session Status:**

| Session ID | Persona | Valid | Verdict | PR |
|---|---|---|---|---|
| 2026-06-04-persona-2-001 | Persona 2 (infra validation) | NO — cold-start violated | Infrastructure validated; Pillar 1 functional | #732 ✅ |
| 2026-06-04-persona-2-002 | Persona 2 — Finance Ministry Negotiator | NO — reclassified as developer audit | Agent used API spec + curl instead of navigating UI. Findings are real technical gaps, not usability findings. Superseded by 003. | #733 ✅ |
| 2026-06-04-persona-2-003 | Persona 2 — Finance Ministry Negotiator | **YES** — genuine cold-start, visual navigation | PARTIALLY MET — agent reached [CONCLUDED:] but ~80% from historical knowledge, ~20% from tool output. Alert panel non-interactive; no cohort data visible. | #736 ✅ |
| 2026-06-04-persona-1-001 | Persona 1 — Programme Analyst (Lucas Ferreira) | **YES** — genuine cold-start, visual navigation | NOT MET — fiscal multiplier parameter absent; alert non-interactive; no disaggregated indicators; 5 actions, 0 visible responses. | #738 ✅ |
| 2026-06-04-persona-5-001 | Persona 5 — Institutional Decision-Maker (Executive Director, IMF) | **YES** — genuine cold-start, visual navigation | PARTIALLY MET — reframed task from tradeoff to joint design failure; reached [CONCLUDED:] in 3 turns. Scenario identity unconfirmed (CRITICAL GAP); financial trajectory possibly incomplete; composite scores uninterpretable. | #739 ✅ |

**Findings from Session 3 (2026-06-04-persona-2-003) — UI usability findings:**

| Finding | Severity | Dimension | Description |
|---|---|---|---|
| FINDING-01 | CRITICAL | Action | TERMINAL alert panel non-interactive — 3 click attempts, zero navigation response or expansion |
| FINDING-02 | HIGH | Comprehension | Alert text + trajectory chart illegible at 1440×900 — 3-turn disambiguation delay on alert type |
| FINDING-03 | HIGH | Discovery | No cohort disaggregation visible — CONCLUDED answer was ~80% historical knowledge, not tool output |
| FINDING-04 | MEDIUM | Discovery | Greece not highlighted on map despite scenario loaded — 3-turn scenario-active uncertainty |
| FINDING-05 | MEDIUM | Comprehension | "Primary dimension — see alerts" misdirects to non-interactive display panel |

**Findings from Session P1-001 (2026-06-04-persona-1-001) — UI usability findings:**

| Finding | Severity | Dimension | Description |
|---|---|---|---|
| FINDING-01 | CRITICAL | Action | Fiscal multiplier parameter absent — no UI path to configure or compare 0.5 vs 1.5 multiplier |
| FINDING-02 | CRITICAL | Action | Alert panel non-interactive — replication of S003-FINDING-01; confirmed persona-independent |
| FINDING-03 | HIGH | Discovery | Poverty headcount and health system capacity not surfaced as named indicators anywhere |
| FINDING-04 | HIGH | Comprehension | Active scenario not identifiable — scenario/task mismatch risk; never resolved in 5 turns |
| FINDING-05 | MEDIUM | Action | Zone-1a and zone-1d both show composites only; no sub-indicator drill-in |

**Findings from Session P5-001 (2026-06-04-persona-5-001) — UI usability findings:**

| Finding | Severity | Dimension | Description |
|---|---|---|---|
| FINDING-01 | HIGH | Comprehension | Financial trajectory completeness — agent concluded "no recovery" but Greece historically achieved primary surplus 2014; links to Issue #221 |
| FINDING-02 | CRITICAL | Discovery | Active scenario identification — named "CRITICAL GAP" before concluding; severity escalation confirmed across all 3 Priority A sessions |
| FINDING-03 | MEDIUM | Comprehension | Composite score interpretability — Financial ~0.58, Human Development ~2.73 uninterpretable without scale, baseline, or direction indicator |

**Findings from Session 2 (2026-06-04-persona-2-002) — backend technical findings (developer audit):**

| Finding | Severity | Dimension | Description |
|---|---|---|---|
| FINDING-01 | CRITICAL | Action | Human development indicators frozen at 2010 initial values — human cost ledger produces no output |
| FINDING-02 | CRITICAL | Discovery | No cohort disaggregation — minimum wage workers, pensioners, youth invisible to measurement framework |
| FINDING-03 | HIGH | Comprehension | Composite score discrepancy: /trajectory returns scores; /measurement-output says "not meaningful" |
| FINDING-04 | HIGH | Action | Conditionality instruments too coarse — wage cut, pensions, privatisation all folded into spending_change |
| FINDING-05 | MEDIUM | Discovery | Counter-scenario creation not discoverable without developer knowledge of POST schema |
| FINDING-06 | MEDIUM | Comprehension | `indicator_name` null in MDA alert API response |

**Exit criterion status — all three Priority A sessions complete:**

| Session | Persona | Verdict |
|---|---|---|
| 2026-06-04-persona-2-003 | Finance Ministry Negotiator | PARTIALLY MET — ~80% historical knowledge, ~20% tool output |
| 2026-06-04-persona-1-001 | Programme Analyst | NOT MET — fiscal multiplier parameter absent; 0 visible UI responses |
| 2026-06-04-persona-5-001 | Institutional Decision-Maker | PARTIALLY MET — concluded in 3 turns; scenario identity and trajectory completeness unconfirmed |

**Cross-session pattern — the one finding present across ALL three Priority A sessions:** Active scenario cannot be confirmed from the main viewport. Severity: MEDIUM (P2) → HIGH (P1) → CRITICAL (P5). This is the minimum fix required before any Priority A use case can be considered served.

**Session runners:**
- `scripts/run_usability_session_interactive.py` — Interactive Playwright loop (Option 2, default). Start with: `python3 scripts/run_usability_session_interactive.py <session_id> <persona_id> [--scenario <uuid>]`. No API key required. Coordinator reads screenshots via Read tool and writes actions to IPC files.
- `scripts/run_usability_session.py` — Computer-use runner (Option 1). Requires `ANTHROPIC_API_KEY`. Separate Anthropic API billing.

**Priority A sessions:** COMPLETE (P2 S003 ✅, P1-001 ✅, P5-001 ✅). Priority B sessions (P6 Civic Researcher, P8 Community Leader) are next if EL authorises.

**M12 action items from all sessions:**
- Make TERMINAL alert panel interactive — click expands to indicator time-series + threshold progression + driver attribution (S003-FINDING-01)
- Increase alert text font size; add human-readable indicator label alongside technical key (S003-FINDING-02 + S002-FINDING-06)
- Cohort disaggregation visible in main view: youth unemployment, pensioner poverty, bottom-quintile income share (S003-FINDING-03 + S002-FINDING-02)
- Highlight active scenario country on map; show active scenario name in persistent header (S003-FINDING-04)
- Human development module must respond to fiscal policy inputs — unemployment elasticity, health expenditure linkage (S002-FINDING-01)
- Named conditionality instruments: minimum_wage_change_pct, pension_replacement_rate_change_pct, etc. (S002-FINDING-04)
- "Duplicate and modify" action on scenario cards for counter-scenario creation (S002-FINDING-05)
- Remove or caveat composite scores in single-entity scenario trajectory view (S002-FINDING-03)
- Fiscal multiplier parameter input in scenario configuration — 0.5 vs 1.5 comparison (P1-FINDING-01)
- Side-by-side or overlaid scenario comparison for parameter sensitivity analysis (P1-FINDING-01)
- Poverty headcount and health system capacity as named, disaggregated output indicators (P1-FINDING-03)
- Active scenario name + country in persistent main viewport header (P1-FINDING-04, P5-FINDING-02, S003-FINDING-04) — this is the cross-session universal finding
- Financial trajectory must show full arc including partial recovery; incomplete trajectories must be labelled (P5-FINDING-01; links to Issue #221 mean-reversion channel)
- Each composite score in zone-1d must show: current value, direction indicator (↑↓), scale tooltip; plain-language label for non-economist users (P5-FINDING-03)

**M11 formally closed:** Issue #262 closed 2026-06-04, GitHub Milestone 12 (M11) closed, tagged `v0.11.0`. Compliance gate: SCAN-025 recorded, KI-002 filed (mypy Python version mismatch, pre-existing). ADR license renewals complete (ADR-001/002/005/007/008/010 → M11.5; ADR-011 license section added; ADR-009 diagram added). Socratic Agent TEST complete (in-session 2026-06-04).

**Exit criterion (M11.5):** Can a finance ministry analyst with no prior WorldSim orientation use this tool to produce a finding they could cite in a negotiation?

**M11.5 agent deliverables — COMPLETE:**
- Priority A synthesis: `docs/ux/usability-sessions/synthesis/2026-06-04-priority-a-synthesis.md` (PR #741) — 11 findings ranked, M12 action table, exit verdict
- Feature catalogue: `docs/ux/usability-sessions/synthesis/2026-06-04-feature-catalogue.md` (PR #742) — all v0.11.0 capabilities with per-capability discoverability verdict
- Exit checklist assessment: Issue #720 comment (2026-06-04) — all completable gates closed; EL review is the remaining gate

**Remaining exit gates (EL action required):**
- EL reviews findings and confirms exit criterion verdict (NOT READY — EVIDENCE COMPLETE)
- M12 issues filed for minimum viable scope (synthesis Ranks 1–4: scenario identity header, interactive alert, fiscal multiplier UI, cohort disaggregation)
- Issue #720 closed; GitHub Milestone 14 (M11.5) closed

## Recently Merged PRs (last 5)

| PR | Title | Date |
|---|---|---|
| #898 | docs(process): milestone exit ceremony SOP + demo prep gaps (NM-041) | 2026-06-12 |
| #897 | chore(state): SESSION_STATE.md — milestone reference audit complete (PR #896) | 2026-06-12 |
| #896 | docs(roadmap): update milestone references from M8/M11 era to M13 active — README, CLAUDE.md, roadmap.md | 2026-06-12 |
| #895 | chore(state): SESSION_STATE.md — fresh session audit pass 2 (four gaps fixed) | 2026-06-12 |
| #894 | chore(state): SESSION_STATE.md — issue triage: #865/#844 closed; 9 unmilestoned issues assigned to M13/M14 | 2026-06-12 |
| #893 | chore(state): SESSION_STATE.md — M13 kickoff prerequisites, stale M8/M9 work-stream text replaced | 2026-06-12 |
| #892 | chore(state): SESSION_STATE.md — M13 now active; M12 block marked CLOSED; GitHub Milestone 13 closed | 2026-06-11 |
| #891 | chore(state): SESSION_STATE.md — demo recording uploaded to v0.12.1 release | 2026-06-11 |
| #890 | fix(demo): close missing ) in bold() call on Step 5 presenter line | 2026-06-11 |
| #889 | chore(state): fix #263 milestone label — M12 not M14 | 2026-06-11 |
| #888 | docs(process): Phase 0 EL endorsement recorded 2026-06-11 | 2026-06-11 |
| #887 | docs(process): demo-preparation-standard M12 reference table — v0.12.1 IR + audience simulation + stakeholder review | 2026-06-11 |
| #886 | docs(demo): M12 Step 9 stakeholder review — simulated session, north star PASS | 2026-06-11 |
| #883 | chore(demo): recapture M12 screenshots with PR #880 UI changes | 2026-06-11 |
| #880 | fix(demo): Step 6c gate — four annotation fixes to unblock Step 9 (closes #879) | 2026-06-11 |
| #867 | docs(process): Step 6c ordering correction — 6b → 7 → 6c → 9; IR Agent gates persona panel; prerequisite block added to Steps 7 and 6c | 2026-06-11 |
| #863 | docs(process): Step 6c Audience Simulation Panel — persona-based live demo rehearsal (Personas 1/2/5 in-character; Persona 5 north star gate; Four-Tier Review Structure; M14 forward) | 2026-06-11 |
| #862 | chore(state): SESSION_STATE.md — #263 corrected back to M12 (EL correction 2026-06-11) | 2026-06-11 |
| #857 | fix(demo): DEMO-054 testMatch guard + DEMO-055 entity priming and attributed curve references (NM-040) | 2026-06-11 |
| #854 | fix(demo): DEMO-041/052/053 pre-demo fixes — confidence tier disclosure, spatial reference, zone label → plain language | 2026-06-11 |
| #836 | docs(demo): walkthrough Section 4 — capability-gaps reframe (political feasibility, conditionality design, medium-term horizon; M14 cadence caveat) | 2026-06-10 |
| #835 | docs(demo): walkthrough conditionality framing — clawback reading, branch mechanics, reserve invariant caveat | 2026-06-10 |
| #834 | docs(demo): walkthrough pre-IR revision — two-act structure, human moment opening, NARRATION-RULING-1, Greece/Argentina framing | 2026-06-10 |
| #833 | docs(demo): Mode 3 scenario evaluation panel — deliberation + recommendation (retain fixture; branch step 3 at 1.30×) | 2026-06-10 |
| #832 | docs(adr): M12 exit license audit — renew ADR-001/002/005/007/008/010/011 to M13 | 2026-06-10 |
| #831 | docs(compliance): SCAN-026 M12 exit gate + ADR-012 Mermaid diagram (0 violations) | 2026-06-10 |
| #830 | docs+test: M12 exit artifacts — demo walkthrough, Phase 2 A/B report, NM-036 integration test | 2026-06-10 |
| #816 | fix(frontend): scroll AlertDetailPanel into view on mount (#814) | 2026-06-09 |
| #808 | docs(process): Phase 0 Step 5 — north star test process gate (CLAUDE.md) and enforcement review | 2026-06-09 |
| #796 | feat(demo): G8 — Jordan/Egypt Hormuz Demo 4 (closes #755) | 2026-06-07 |
| #795 | chore(state): SESSION_STATE.md — NM-036 ia1_disclosure branch snapshot | 2026-06-07 |
| #794 | fix(e2e+engine): Mode 3 E2E selector fix + ia1_disclosure copy + cohort reconstruction gap (closes #793) | 2026-06-07 |
| #791 | chore(state): SESSION_STATE.md — Wave C complete (NB-4/NB-6/NB-7 merged) | 2026-06-07 |
| #790 | feat(engine): NB-4 — investment climate state variables: sovereign_risk_premium, fdi_stock_pct_gdp, portfolio_flow_velocity, credit_rating_score (closes #34) | 2026-06-07 |
| #789 | fix(frontend): NB-6 — ESLint audit: 80 violations in react-hooks, react-refresh, no-unused-expressions (closes #644) | 2026-06-07 |
| #788 | docs(ux): NB-7 — Mode 1 COMPARE_VIEW spec: entry point, API design, Persona 3 user story (closes #451) | 2026-06-07 |
| #778 | feat(mode3): G6b — Mode 3 Active Control branch-and-recompute (closes #753) | 2026-06-05 |
| #775 | feat(engine): G6a — multi-country scenario backend, threshold_crossed, multi-entity choropleth + identity header | 2026-06-05 |
| #774 | docs(arch): G7 — cloud compute path document (closes #750) | 2026-06-05 |
| #773 | feat(engine): G5 — external sector module: BilateralTradeShock + CommodityPriceShock (ADR-012) | 2026-06-05 |
| #772 | ci: NM-035 hotfix — add release/m* to ci.yml pull_request and push branch triggers | 2026-06-05 |
| #769 | feat(engine): G4 — matrix engine production migration (closes #749) | 2026-06-05 |
| #767 | feat(ux): G3 — Mode 2 fiscal multiplier parameter input (closes #746) | 2026-06-05 |
| #764 | feat(ux): G2 — MDA alert panel interactive drill-in (closes #745) | 2026-06-05 |
| #762 | feat(ux): G1 — instrument cluster display + scenario identity header (closes #744 #747) | 2026-06-05 |
| #759 | process(integrity): NM-034 — PM Agent filed NM entries without PI activation | 2026-06-05 |
| #758 | process(raci): NM registry no-delegation clause — PI Agent activation required before any NM entry | 2026-06-05 |
| #740 | chore(state): SESSION_STATE.md — M11.5 Priority A sessions complete (PRs #736/#738/#739) | 2026-06-04 |
| #739 | ux(pillar-2): Session P5-001 — Persona 5 cold-start findings (Executive board briefing) | 2026-06-04 |
| #738 | feat(ux): session P1-001 Persona 1 findings — fiscal multiplier analysis NOT MET | 2026-06-04 |
| #737 | chore(state): SESSION_STATE.md — session 003 Persona 2 complete; Priority A sessions P1/P5 next | 2026-06-04 |
| #736 | feat(ux): M11.5 session 003 — genuine cold-start Persona 2 visual navigation findings | 2026-06-04 |
| #735 | feat(ux): computer-use session runner + reclassify session 002 as developer audit | 2026-06-04 |
| #733 | feat(ux): M11.5 Session 2 — Persona 2 cold-start usability session, 6 findings | 2026-06-04 |
| #732 | feat(ux): M11.5 Session 1 — Pillar 1 infra validation, sessions.py path fix | 2026-06-04 |
| #731 | chore(state): SESSION_STATE.md — Pillar 3 merged (PR #730, closes #719); all pre-session gates closed | 2026-06-04 |
| #727 | docs(ux): Pillar 2 cold-start usability audit methodology — M11.5 (closes #718) | 2026-06-04 |
| #724 | feat(usability): Pillar 1 rrweb session recording layer — M11.5 (closes #717) | 2026-06-04 |
| #722 | chore(compliance): M11 exit — ADR renewals, Mermaid diagrams, SCAN-025, KI-002 | 2026-06-04 |
| #715 | docs(vision): M11.5 North Star — usability validation and experience audit | 2026-06-04 |
| #713 | docs(ux): political economy module user stories — M11 Issue #681 | 2026-06-04 |
| #711 | feat(simulation): G20 — horizon degradation envelope, fidelity artifact, restore endpoint — closes #151 #154 #155 | 2026-06-04 |
| #710 | feat(simulation): G19 — tombstone entity_state_snapshot, engine_version_hash, debt MDA threshold — closes #147 #152 #36-DB | 2026-06-04 |
| #707 | feat(engine): matrix computation engine — ADR-009 parallel run, equivalence harness, interpretability tools, Phase 2 A/B benchmark — closes #215 #404 | 2026-06-04 |
| #705 | feat(political-economy): PoliticalEconomyModule — legitimacy, survival, elite capture — closes #156 #159 #272 #273 #679 | 2026-06-04 |
| #704 | feat(orchestration): political economy constraints — closes #96 #93 #157 | 2026-06-04 |
| #703 | feat(engine): non-linear propagation — THRESHOLD and CASCADE modes — closes #40 #29 | 2026-06-04 |
| #702 | test(fixtures): fix Greece attribute count test for trend_growth seed | 2026-06-04 |
| #676 | docs(demo): NM-032 + DEMO-018/019/020 — screenshot viewport mismatch and live application findings | 2026-06-03 |
| #658 | docs(demo): add issue numbers to M10 stakeholder review findings | 2026-06-02 |
| #656 | docs(process): demo review naming consistency — NM-031 | 2026-06-02 |
| #655 | docs(ux): NARRATION-RULING-1 — institutionalize three-layer narration structure | 2026-06-02 |
| #645 | docs(demo): Step 4 narration — honest scope framing replaces false recovery claim | 2026-06-02 |
| #640 | docs(process): NM-028/029/030 — Demo 3 near-miss filings | 2026-06-02 |
| #639 | fix(demo3): four CRITICAL blocking bugs — trajectory re-fetch, governance event mismatch, ecological temporal guard, boundary constant fetch | 2026-06-02 |
| #635 | fix(process): M10 immediate issues — process docs, ADR threshold, PR checklist, step annotation, fidelity labels (closes #395, #512, #535, #536, #538, #539, #541, #543) | 2026-06-02 |
| #631 | docs(process): agent-raci docs/demo/ ownership + UX/UI standards document (closes #537, #620) | 2026-06-02 |
| #629 | docs(process): demo preparation standard M10 update — screenshot naming, legibility gate, narration check (closes #379, #628) | 2026-06-02 |
| #626 | test(e2e): demo advancement flow and legibility regression guards (closes #376, #377) | 2026-06-02 |
| #624 | fix(fixture): Argentina Demo 3 — emergency_declaration at step 2 triggers governance MDA (closes #615) | 2026-06-02 |
| #622 | fix(frontend): Zone 1D ecological boundary annotation + AttributeSelector display names (closes #616, #617) | 2026-06-02 |
| #618 | docs(demo): Demo 3 IR review — v0.10 Argentina + instrument cluster (closes #347 DEMO-006) | 2026-06-02 |
| #601 | docs(architecture): ARCH-REVIEW-006 — Issue #577 targeted architectural scope review | 2026-06-02 |
| #598 | docs(ux): US-043 No False Precision correction — epistemic disclosure criterion (PI-REVIEW-002 F-005) | 2026-06-02 |
| #596 | process(pi-review): PI-REVIEW-002 — Issue #577 [Phase-3-TBD] scope assessment | 2026-06-02 |
| #594 | docs(ux): public advocacy user journeys (E–H) and user stories US-030–US-048 (closes #576) | 2026-06-02 |
| #592 | docs(ux): public advocacy personas — Personas 6–8 and Persona 4V (closes #575) | 2026-06-02 |
| #587 | feat(zone-1c): PMM live computation — Issue #496 (IR-002) | 2026-06-02 |
| #585 | feat(governance): GovernanceModule promoted to live axis — ADR-005 Amendment 4 (closes #556, #499) | 2026-06-02 |
| #583 | feat(frontend): default step labels from start year — IR-004 (closes #498) | 2026-06-02 |
| #578 | docs(mv): MV-002 hardware validation complete — ProBook i5-8265U results recorded, Issue #550 closed | 2026-06-01 |
| #565 | feat(benchmark): Phase 1 engine baseline benchmark script — Issue #514 | 2026-05-31 |
| #564 | chore(python): Python 3.12 → 3.13 in pyproject.toml, .python-version, ci.yml, CONTRIBUTING.md | 2026-05-31 |
| #551 | process(exit): Issue Disposition Audit SOP — milestone exit cleanup codified (NM-026) | 2026-05-29 |
| #548 | process(audit): PI-AUDIT-002 — end-to-end feature delivery pipeline | 2026-05-25 |
| #533 | process(agents): Customer Agent — Layer 3 institutional capacity (closes #532) | 2026-05-25 |
| #530 | process(pi-review): PI Agent REVIEW — agent team organization (PI-REVIEW-001); Issues #521–#529 | 2026-05-25 |
| #519 | process(pi-audit): inaugural PI Agent four-lens audit — NM-021, NM-022, scan ordering fix | 2026-05-25 |
| #517 | feat(process): Define Process Integrity Agent (closes #516) | 2026-05-25 |
| #515 | docs(process): NM-020 — backend compute baseline gap; fix stale Chief Engineer ADR ref; backlog prerequisite rule | 2026-05-25 |
| #511 | chore(state): SESSION_STATE.md — M9 exit ceremony complete (PRs #509 + #510) | 2026-05-25 |
| #510 | docs(adr): ADR-007 accepted — panel review, Mermaid diagram, ADR-001/002 renewals, document referencing convention, STD-REVIEW-005, SCAN-023 | 2026-05-23 |
| #509 | docs(adr): ADR-005 Amendment 4 + ADR-007 Synthetic Data Framework (Proposed) — M9 exit ceremony | 2026-05-23 |
| #501 | docs(ir): M9 instrument cluster IR review + M8 DEMO triage (Issue #493) | 2026-05-23 |
| #491 | test(e2e): #463 PR 2 — Greece integration suite + AC-001/002 skip removed (closes #463) | 2026-05-23 |
| #490 | feat(frontend): wire InstrumentCluster into App.tsx — Zone 1 instruments live (Issue #463 PR 1) | 2026-05-23 |
| #489 | test(qa): #459 — remaining acceptance tests: ModeIndicator, AC-006 RTL, AC-013, US-026 | 2026-05-23 |
| #487 | feat(frontend): PMMWidgetZone1C + FourFrameworkZone1D — Zone 1C/1D instruments (Issue #462) | 2026-05-23 |
| #481 | chore(state): SESSION_STATE.md — session end 2026-05-23 (PRs #479–#480) | 2026-05-23 |
| #480 | test(qa): retrofit instrument cluster spec — split Type 1/Type 2 ACs, remove blanket skip (closes #473) | 2026-05-23 |
| #479 | process(nm): NM-018 — hammer-nail; panel composition principle for pre-EL consultations | 2026-05-23 |
| #468 | feat(api): GET /scenarios/{id}/trajectory endpoint (closes #458) | 2026-05-23 |
| #466 | docs(process): PM Agent pre-EL consultation — standing automatic capability (closes #464) | 2026-05-23 |
| #456 | docs(process): PM Agent issue hierarchy rule — Epic → Feature → Task, binary spawning | 2026-05-23 |
| #454 | docs(ux): resolve UX-RULING-1/2/3 — alert tense markers, null CSS class, mode labels | 2026-05-23 |
| #452 | docs(ux): US-GAP-001 resolved — Mode 1 COMPARE_VIEW placeholder; EL decision M10 (Issue #451) | 2026-05-23 |
| #449 | docs(ux): M9 instrument cluster user stories — 29 stories, QA + FA consumers (closes #441) | 2026-05-23 |
| #447 | docs(process): NM-014 systemic root cause — micro-management cycle and correct locus of specification | 2026-05-23 |
| #445 | docs(process): PR merge gate — mandatory pause + SESSION_STATE auto-merge exception | 2026-05-23 |
| #438 | docs(process): blameless continuous improvement principle — Aviation SMS in CLAUDE.md | 2026-05-23 |
| #436 | docs(process): near-miss registry — NM-008 through NM-013, agent team growth and DIC founding | 2026-05-23 |
| #435 | docs(process): near-miss registry — NM-001 through NM-007, Aviation SMS methodology | 2026-05-23 |
| #434 | chore(state): SESSION_STATE.md — PR #432 + #433 merged; Issue #431 closed | 2026-05-23 |
| #433 | docs(process): file ownership table and HORIZON file authority audit (closes #431) | 2026-05-23 |
| #432 | docs(process): file authority rule in CLAUDE.md — agents must not write to owned files without prior owner review | 2026-05-23 |
| #429 | docs(adr+schema): ADR-010 D6+D2 amendments; CM reference range consultation; api_contracts + database.yml | 2026-05-23 |
| #417 | docs(process): ADR-008 panel review artifact and panel review process standard | 2026-05-22 |
| #416 | docs(adr): ADR-008 — UX architecture: instrument cluster, viewport, and interaction model (closes #397) | 2026-05-22 |
| #409 | docs(vision): WorldSim technical concepts — 18 architectural concepts with reasoning | 2026-05-22 |
| #408 | docs(roadmap): WorldSim roadmap M9–M13 with demo arc, long-term direction, and process integration | 2026-05-22 |
| #427 | docs(frontend): EL decisions A/B/C recorded — trajectory endpoint unblocked | 2026-05-22 |
| #426 | docs(frontend): Six-agent parallel consultation — DA-F2/F4/F5 pre-implementation record | 2026-05-22 |
| #425 | docs(frontend): Architect Agent review of Data Architect findings (DA-F1–F5) | 2026-05-22 |
| #422 | docs(frontend): FA brief — three-agent review findings incorporated | 2026-05-22 |
| #421 | docs(frontend): M9 FA brief — instrument cluster implementation (ADR-008 + ADR-010) | 2026-05-22 |
| #420 | docs(adr): ADR-010 accepted — EL decision recorded with rationale; ARCH-004 → ACCEPTED | 2026-05-22 |
| #401 | docs(process): agent-raci.md — RACI chart for all 15 agents (closes #369, #301) | 2026-05-21 |
| #399 | docs(ux): UX document updates — EL Decisions 1/2/3 (north-star, information-hierarchy, user-journeys) | 2026-05-21 |
| #390 | docs(ux): UX first-principles depth — six gaps closed, revised six premises (closes #363) | 2026-05-21 |
| #388 | docs(ux): persona-grounded UX review — Case B and governing premises vs. five personas (closes #387) | 2026-05-21 |
| #385 | docs(ux): user persona document — five personas, entry state taxonomy, marquee cases (closes #362) | 2026-05-20 |
| #384 | docs(process): agent working agreements — all 15 agents (closes #360) | 2026-05-20 |
| #383 | docs(vision): WorldSim founding document — synthesized from April-May 2026 founding conversations | 2026-05-20 |
| #373 | docs(adr): Chief Methodologist consultation — synthetic data framework (closes #361) | 2026-05-19 |
| #372 | docs(claude): CLAUDE.md structural refactor — closes #359 | 2026-05-19 |
| #371 | chore(state): design foundation sequence — 12 issues #359–#370 filed | 2026-05-19 |
| #356 | docs(ux): M8 interaction model critique — panel synthesis (UX Designer, Dev Economist, Chief Methodologist) | 2026-05-18 |
| v0.8.0 | GitHub Release — Milestone 8 formal close | 2026-05-19 |
| #399 | docs(ux): UX document updates — EL Decisions 1/2/3 (north-star, information-hierarchy, user-journeys) | 2026-05-21 |
| #396 | chore(state): SESSION_STATE.md — EL Decisions 1/2/3 recorded; Issue #364 closed; Issues #392–#395 filed | 2026-05-21 |
| #391 | chore(state): SESSION_STATE.md — PR #390 merged; Issue #363 closed; Issue #364 unblocked | 2026-05-21 |
| #390 | docs(ux): UX first-principles depth — six gaps closed, revised six premises (closes #363) | 2026-05-21 |
| #388 | docs(ux): persona-grounded UX review — Case B and governing premises vs. five personas (closes #387) | 2026-05-21 |
| v0.8.0 | GitHub Release — Milestone 8 formal close | 2026-05-19 |
| #355 | docs(ux): M8 interaction model critique — UX Design Thinking Agent first activation (closes #353) | 2026-05-18 |
| #354 | docs(process): add UX Design Thinking Agent to agents.md (closes #353) | 2026-05-18 |
| #352 | chore(state): update SESSION_STATE.md — PR #351 open (IR issues #342–#350 + M8 walkthrough) | 2026-05-18 |
| #351 | docs(demo): M8 IR review issues filed (#342–#350) + M8 stakeholder walkthrough | 2026-05-18 |
| #340 | fix(demo): three demo polish fixes + M8 IR Agent stakeholder review | 2026-05-18 |
| #339 | docs(demo): M8 demo — updated demo.sh, narrated spec, five screenshots captured (closes #233) | 2026-05-18 |
| #338 | chore(demo): switch TTS voice to Zoe (Enhanced) | 2026-05-18 |
| #336 | fix(dev): Python 3.12 Docker image rebuild — startup version guard, CONTRIBUTING docs | 2026-05-18 |
| #335 | chore(state): SESSION_STATE.md update — PR #334 merged, demo prep standard, board cleanup | 2026-05-18 |

---

## Open Issues — M9 Horizon:Immediate (this session)

| Issue | Title | Status / Gate |
|---|---|---|
| #473 ✅ | test(qa): retrofit instrument-cluster spec — split component ACs into task scope; remove blanket skip | Closed — PR #480 merged; Type 1 ACs distributed to #460/#461/#462 via comments; integration spec created |
| #460 ✅ | feat(frontend): TrajectoryView — Zone 1A (instrument cluster) | Closed — PR #484 merged |
| #461 ✅ | feat(frontend): MDA Alert Panel — Zone 1B (instrument cluster) | Closed — PR #486 merged |
| #462 ✅ | feat(frontend): PMM + Four-Framework — Zone 1C/1D (instrument cluster) | Closed — PR #487 merged |
| #463 ✅ | test(e2e): Greece integration Playwright suite | Closed — PR #490 (App.tsx wiring) + PR #491 (Greece suite) merged |
| #367 ✅ | docs(demo): persona-anchored IR review re-run (Persona 2) | Closed — superseded by M9 instrument cluster redesign; see #493 |
| #368 ✅ | docs(demo): DEMO issues re-triage #342–#350 | Closed — superseded by M9 instrument cluster redesign; see #493 |
| #493 ✅ | M9 demo — IR review + DEMO triage against Greece fixture with M9 cluster | Closed — PR #501 merged |

---

## Open Issues — M10 Horizon:Immediate (active)

| Issue | Title | Status / Gate |
|---|---|---|
| #550 ✅ | test(e2e): MV-002 hardware render baseline — TrajectoryView ≤ 100ms on ProBook | **Closed 2026-06-01** — AC-007 ✅ PASSED ≤ 100ms (4× throttle active), AC-008 ✅ PASSED ≤ 100ms (4× throttle active). Machine: HP ProBook i5-8265U, 8 GiB RAM, 4 cores, Windows 11. PR #578. |
| #495 ✅ | feat(frontend): wire mda_alerts into MDA Alert Panel — Zone 1B live data (IR-001 Critical) | **Closed** — measurement-output fetch wired in ScenarioInstrumentCluster.tsx; store.setMdaAlerts() called after each step advance. |
| #496 ✅ | feat(api): PMM live computation backend endpoint (IR-002) | **Closed 2026-06-02** — PR #587 merged. Per-step PMM embedded in trajectory response; frontend syncs to store on step change. |
| #497 ✅ | feat(frontend): persistent scenario state + demonstrative entry — localStorage + URL param (IR-003) | **Closed 2026-06-02** — PR #584 merged. localStorage `worldsim_last_scenario` key; URL `?scenario=` param takes precedence. |
| #498 ✅ | feat(frontend): default step labels from start year (IR-004) | **Closed 2026-06-02** — PR #583 merged. Start year input in create form; `start_date` passed to backend. |
| #499 ✅ | fix(frontend): remove governance "(in validation)" annotation (IR-005) | **Closed 2026-06-02** — PR #585 merged as part of Issue #556 (governance promotion). |
| #500 ✅ | feat(frontend): Zone 1D loading state skeleton (IR-006) | **Closed** (prior session) — PR #582 merged. |
| #553 ✅ | feat(fixture): Argentina 2000–2002 second country fixture — IMF debt crisis (Demo 3) | **Closed 2026-06-02** — PR #590 merged. `build_argentina_demo_scenario()`: n_steps=4, EcologicalModule + GovernanceModule, NOAA MLO 2000 CO2 seed, WGI/V-Dem ARG 2000 governance seeds, step_metadata event labels (steps 1–3 SIGNIFICANT). `step_metadata` added to `ScenarioConfigSchema` (was being stripped by Pydantic on POST). Demo script at `backend/scripts/demo_argentina_2001_2002.py`. |
| #556 ✅ | feat(governance): GovernanceModule M10 promotion — ADR-005 Amendment 4 | **Closed 2026-06-02** — PR #585 merged. All five criteria met. |
| #675 | fix(demo): demo-narrated.spec.ts captures at 1280×720 — mismatches legibility gate (1440×900) and live demo viewport | **Filed 2026-06-03** — Milestone M11, horizon:near-term. Three required fixes: (1) `page.setViewportSize({ width: 1440, height: 900 })` in demo spec; (2) update `SCREENSHOT_DIR` to `m{N}/screenshots/` each milestone; (3) update demo-preparation-standard Steps 4 and 6 with explicit viewport requirement. Root cause of DEMO-020. NM-032. |
| #674 | fix(frontend): DEMO-020 — Zone 1A y-axis tick labels clipped at left component boundary | **Filed 2026-06-03** — Milestone M11, horizon:near-term. `margin.left` on `ComposedChart` too narrow for 6-char labels when ecological score >1.0. Fix: increase to 48–56px or format ticks to 4-char precision. Confirm with `demo-legibility.spec.ts` at 1440×900. |
| #673 | demo: DEMO-019 — PMM None state ("—") has no explanation for non-specialist users | **Filed 2026-06-03** — Milestone M11, horizon:near-term. UX copy change in `PMMWidgetZone1C.tsx`: conditional sub-label when `pmm_value` is null. "All thresholds breached — see alerts" or equivalent. Distinct from DEMO-016 (nonzero PMM precision). |
| #672 | demo: DEMO-018 — Zone 1A legend shows raw variable names for CI upper bound and active curves | **Filed 2026-06-03** — Milestone M11, horizon:near-term. Pass `legendType="none"` on CI/ghost `<Line>` components or add explicit `name` prop. `getIndicatorDisplayNameAny()` fix (#617) covered AttributeSelector, not Recharts legend derived keys. |
| #667 | demo: DEMO-010 — M10 screenshots unverified as post-fix state | **Filed 2026-06-03** — Milestone M11, horizon:near-term. Verify whether `docs/demo/m10/screenshots/` files are pre- or post-DEMO-003/005 fix. Attestation required in SEQUENCE.md. |
| #668 | demo: DEMO-011 — Frame D not re-captured after DEMO-005 fix | **Filed 2026-06-03** — Milestone M11, horizon:near-term. Frame D Zone 1A legend overlap fix (PR #345) may not be reflected in repository artifact. Re-capture or attestation required. |
| #669 | demo: DEMO-013 — dashed curve convention not narrated in M10 walkthrough | **Filed 2026-06-03** — Milestone M11, horizon:near-term. Screenshot brief §Key Narration Notes #2 requirement unimplemented. Add dashed=projected/solid=historical sentence to Section 2 Step 2. Walkthrough doc only — no implementation required. |
| #670 | demo: DEMO-017 — Human Development composite trajectory absent from M10 walkthrough narration | **Filed 2026-06-03** — Milestone M11, horizon:near-term. Human cost arc not narrated in Section 2. Must name at least one capability domain and one affected cohort class. Step 5c NARRATION-RULING-1 self-check required after update. |
| #569 | test(e2e): AC-009 re-run — Mode 3 advance-step → render ≤ 100ms (hardware baseline) | Deferred M12 — Mode 3 not yet built. Blocked by Mode 3 implementation. |
| #22 | feat(engine): confidence_tier split — per-indicator separate from composite | **Deferred to M11 (2026-06-03)** — Required by ADR-007 (`is_synthetic`, `synthetic_method` Quantity fields) but ADR-007 framework is not implemented in M10. Rationale comment posted on issue. |
| #27 | feat(engine): Monte Carlo distribution output — replaces point estimates with scenario bands | **Deferred to M11 (2026-06-03)** — Foundational to ADR-007 No False Precision principle (pessimistic/realistic/optimistic bands). Cannot be scoped before ADR-009 (engine computation model) is accepted; ADR-009 is M11 work. Rationale comment posted on issue. |
| #43 | feat(engine): backtesting validation harness — model vs. historical divergence scoring | **Deferred to M11 (2026-06-03)** — No Phase 1 baseline benchmarks consumed yet (delivered in M10 but not yet integrated into a validation harness); blocked by sparse matrix proof-of-concept (M11 core deliverable). Rationale comment posted on issue. |
| #45 | feat(engine): engine fidelity dashboard — model vs. actuals gap visualization | **Deferred to M11 (2026-06-03)** — Downstream of #43 (backtesting harness). Cannot ship a gap visualization before the harness that computes the gaps exists. Rationale comment posted on issue. |
| #575 ✅ | docs(ux): public advocacy personas — Investigative Journalist, Parliamentary Economist, Civil Society Monitor, Persona 4V | **Closed 2026-06-02** — PR #592 merged. Panel: PO Agent (R), UX Designer (C), Development Economist (C), Political Economist (C), Customer Agent (C). Four additions: Persona 6 (Farida Haidari, journalist, Dawn/Pakistan), Persona 7 (James Ochieng, Kenya PBO), Persona 8 (Abena Osei, SEND Ghana), Persona 4V (Dr. Priya Krishnaswamy, CDS/JNU). Primary Cases 6 (Pakistan flood + IMF combined shock), 7 (Kenya committee brief), 8 (Ghana accountability gap), Persona 4V marquee case (The Wardha Divergence). Retrospective entry state extended to cover accountability tracking sub-mode (no 7th state). Customer Agent finding: integrated observed-actuals input (Persona 8 accountability use case) is not a current platform capability — flagged in Persona 8 failure mode and Primary Case 8 exit criteria; roadmap item. |
| #574 | Epic: Vision-to-Architecture Bridge — personas → user experiences → technical concepts | **Filed 2026-06-01** — Three child issues: #575 ✅ (personas extension, closed PR #592), #576 ✅ (user experiences for second ring, closed PR #594), #577 (Phase 3 DIC technical concept review — unblocked). No active horizon assignment — EL to prioritize M10 or M11. |
| #577 | docs(ux): Phase 3 DIC technical concept review — [Phase-3-TBD] stories from Issue #576 | **ARCH-REVIEW-006 complete (PR #601, 2026-06-02). 11 child issues filed #603–#614 (2026-06-02).** 16 blindspots classified: 1 Immediate, 12 Near-Term, 3 Long-Term. One Immediate blocker: CM must author vocabulary mapping standard (#603, AR-006-B-007) before any US-043 implementation begins. Full findings: `docs/architecture/reviews/ARCH-REVIEW-006-milestone10.md`. Tracking comment posted on #577. |
| #615 ✅ | fix(fixture): Argentina Demo 3 — verify MDA alerts fire at step 2+; adjust governance seed if floor does not breach | **Closed 2026-06-02** — PR #624 merged. `emergency_declaration` added at step 2 (state of siege, December 19 2001 — concurrent with sovereign default). GovernanceModule one-step lag: processed at step 3, reducing `democratic_quality_score` by 0.05 (Bermeo 2016 elasticity). Score path: 0.71 → 0.715 (step 2, imf effect) → **0.665** (step 3) ≤ 0.70 floor → MDA WARNING fires at step 3. Three new regression tests including `test_build_argentina_demo_scenario_governance_mda_breach_math` (elasticity arithmetic gate). Wrong comment about base scheduled_inputs also corrected. |
| #616 ✅ | fix(frontend): Zone 1D ecological boundary annotation — "(1.0 = boundary)" sub-label or tooltip | **Closed 2026-06-02** — PR #622 merged. `"1.0 = boundary"` sub-label (9px, muted) added below "Ecological" row label in `FourFrameworkZone1D.tsx`. Ecological row only. `data-testid="ecological-boundary-note"` for future E2E assertion. |
| #617 ✅ | fix(frontend): AttributeSelector display names — add getIndicatorDisplayNameAny(), wire into AttributeSelector.tsx | **Closed 2026-06-02** — PR #622 merged. `getIndicatorDisplayNameAny(key)` added to `indicatorDisplayNames.ts` (iterates all framework blocks, title-case fallback). Wired into `AttributeSelector.tsx` — dropdown now shows "GDP Growth (%, FLOW)" instead of "gdp_growth (%, FLOW)". |
| #376 ✅ | test(e2e): Playwright demo advancement flow test — scenario advance, choropleth change, MDA accumulation, radar legibility | **Closed 2026-06-02** — PR #626 merged. `demo-advancement-flow.spec.ts`: 5 tests at 1440×900 — all four Zone 1 instruments live at every step; `choropleth-map` `data-step` attribute increments 0→1→2→3 (DEMO-001 guard); Zone 1B MDA panel live/non-blank at every step (DEMO-004 guard); Zone 1D framework scores non-empty at final step; advance button disabled exactly at step 3 (no overshoot). `ChoroplethMap.tsx`: `data-testid="choropleth-map"` + `data-step={currentStep ?? 0}` added to outer container. |
| #377 ✅ | test(e2e): legibility assertions — minimum font size, non-truncation, visibility for all demo components | **Closed 2026-06-02** — PR #626 merged. `demo-legibility.spec.ts`: 6 tests at 1440×900 — Zone 1 instrument bounding boxes non-zero (DEMO-002/003/005/006 guard); Zone 1C PMM value rendered ≥ 20px; Zone 1D framework labels ≥ 10px and not overflow-clipped; `ecological-boundary-note` visible with "1.0 = boundary" text (#616 regression guard); null composite rows carry dashed left border, live rows carry solid border (DEMO-006 guard); Zone 1B MDA text not overflow-clipped (DEMO-003 guard). |
| #342 ✅ | demo(choropleth): single-entity scenario shows no visible change across steps (DEMO-001) | **Closed 2026-06-02** — UX-RULING-4 (binding). FA Agent proposed HUD overlay on choropleth and Zone 1D attribute row; both declined. Root cause reframed: choropleth is a geographic context surface, not a change instrument. M10 fix: narration update (child #628, closed PR #629). M11 fix: Option B scenario-relative color scale (cross-step range endpoint required). |
| #343 ✅ | demo(radar): thesis frame asymmetry not independently legible without narration (DEMO-002) | **Closed 2026-06-02** — Substantially resolved by M9/M10 instrument cluster redesign. Narrow-drawer root cause no longer exists; Zone 1A is primary viewport instrument. M10 IR review: "substantially resolved." |
| #346 ✅ | demo(radar): axis labels and scores not legible at drawer scale (DEMO-005) | **Closed 2026-06-02** — Resolved by M9/M10 instrument cluster redesign. Zone 1D covers multi-framework readout in primary viewport; font sizes validated by `demo-legibility.spec.ts`. M10 IR review: "Significant→Minor." |
| #379 ✅ | process: demo preparation standard as pre-condition — standard must exist and be read before demo assembly begins | **Closed 2026-06-02** — PR #629 merged. `demo-preparation-standard.md`: Step 5a (narration instrument check, UX-RULING-4), Step 5b (legibility Playwright gate), Step 6 amendment (screenshot naming in presentation order). Carried forward from M9. |
| #628 ✅ | demo(script): update Demo 3 narration — route quantitative change to Zone 1A, not choropleth | **Closed 2026-06-02** — PR #629 merged. Child of #342, spawned from UX-RULING-4. `demo_argentina_2001_2002.py`: presenter instruction block in `_print_divergence_narrative` routes narrator to Zone 1A, not choropleth. |
| #537 ✅ | process: docs/demo/ file ownership — PM Agent must be R on demo preparation sequence | **Closed 2026-06-02** — PR #631 merged. `docs/demo/` row added to `docs/process/agent-raci.md` File Ownership table. PM Agent is R; Customer Agent and UX Designer are C. Demo preparation is a blocking exit requirement per milestone. |
| #535 ✅ | MILESTONE_RUNBOOK.md: update milestone definition table to reflect M9 exit | **Closed 2026-06-02** — PR #635 merged. Table expanded from M0–M4 (M1 marked "In Progress") to M0–M13 with current status. M0–M9 Complete, M10 Current, M11–M13 Upcoming. |
| #536 ✅ | CONTRIBUTING.md: fix stale 'branch from develop' instruction | **Closed 2026-06-02** — PR #635 merged. All four "branch from develop" occurrences replaced with "branch from main". |
| #538 ✅ | Document 'significant feature' threshold for ADR requirement | **Closed 2026-06-02** — PR #635 merged. Explicit ADR threshold criteria table added to `CODING_STANDARDS.md §ADR Requirements`: 8 rows covering new module/API/methodology (new ADR), interface changes (amendment), bug/visual/docs (no ADR). PM + Architect jointly own ambiguous calls. |
| #539 ✅ | Add Customer Agent as 13th standing consultation obligation for UX-facing ADRs | **Closed 2026-06-02** — PR #635 merged. Architect → Customer Agent obligation added to `agent-raci.md §Standing Consultation Obligations`. Customer Agent added to UX-design ADR minimum panel (C — Layer 3 usability finding). |
| #541 ✅ | PR template: require cross-ADR impact enumeration as a required field | **Closed 2026-06-02** — PR #635 merged. "ADRs Affected" section added to `CONTRIBUTING.md` PR template (step 8) and Pre-PR Checklist (§3) with table template. |
| #543 ✅ | ADR-006 Decision 12: evaluate CI-enforcement path for Playwright phases 3–4 | **Closed 2026-06-02** — PR #635 merged. Playwright phases 3–4 attestation added to `CONTRIBUTING.md` Pre-PR Checklist §5 for instrument-cluster frontend PRs. Mode transition safety (Phase 3) and render budget (Phase 4) attestation text required in PR description. CI enforcement evaluation deferred to M11. |
| #395 ✅ | data: step_event_label mandatory field — Mode 1 fixtures without event labels are incomplete | **Closed 2026-06-02** — PR #635 merged. `DATA_STANDARDS.md §Scenario Fixture Step Annotation` added: step_metadata JSONB contract, significance enum (ROUTINE/SIGNIFICANT/CRITICAL), label constraints (≤8 words AND ≤32 chars), mandatory coverage rule. Greece fixture `build_greece_scenario()` updated with step_metadata for all 6 steps — all SIGNIFICANT, step 6 CRITICAL. Argentina fixture already compliant. |
| #512 ✅ | fix(fidelity): stale 'Deferred to M7' labels in backtesting dashboard | **Closed 2026-06-02** — PR #635 merged. `FidelityDashboard.tsx`: "Deferred to M7" → "M11" in both gap card notes (GRC #221, ARG #222), both milestone fields, and ADR-006 trigger line footer. Issues #221/#222 are open on M11; no work was delivered in M7/M8/M9. |
| #620 ✅ | docs(ux): UX/UI standards document — consolidated settled decisions with authority citations | **Closed 2026-06-02** — PR #631 merged. `docs/ux/standards.md` created with 15 sections: Framework Color Contract, Color Semantic Contract, Zone 1 Always-Visible Constraint, Zone Layout Dimensions, Choropleth Role (UX-RULING-4), Zone 1D Content Constraint (UX-RULING-4), Null vs. Zero Rendering, MDA Alert Sort Order, Mode-Specific Alert Tense (UX-RULING-1), Mode Indicator Labels (UX-RULING-3), Confidence Tier Visual, Zustand Atomic Update Contract, Loading/Error State Patterns, Step Annotation Rule, Automatic A/B Split (Mode 3). EL sign-off required for any amendment. |

---

## Open Issues — M8 Horizon:Immediate

All Horizon:Immediate issues are now closed. M8 feature-complete.

| Issue | Title | Status |
|---|---|---|
| #269 | Demo scenario — Greece 2010–2015 | Closed ✅ — merged PR #328 |
| #317 | Indicator display name mapping layer | Closed ✅ — merged PR #329 |
| #318 | Mandatory ecological note → Zone 3 expandable | Closed ✅ — merged PR #329 |
| #319 | Radar chart transition animation | Closed ✅ — merged PR #329 |
| #320 | Coffin Corner / PMM Zone 1 widget | Closed ✅ — merged PR #329 |

---

## Open Issues — M8 Horizon:Near-Term

| Issue | Title | Blocked by |
|---|---|---|
| #233 | Screenshot artifact bundle | Closed ✅ — merged PR #339 (five frames), PR #340 (polish + IR review) |
| #221 | Mean-reversion channel (Greece step5 MAGNITUDE) | Nothing — unblocked ✅ |
| #222 | Contemporaneous processing path | Nothing — unblocked ✅ |
| #258 | Mandatory intent blocks | #285 (merged ✅) |
| #332 | Docker image stale — Python 3.11 cached, Python 3.12 required | Closed ✅ — merged PR #336 |

**Re-milestoned to M9** (removed from M8 board this session): #286 (intent_gap_check.py), #299 (Intent Block Author Agent), #300 (Data Quality Agent), #301 (agent-raci.md)

---

## Pending Engineering Lead Decisions

| Decision | Context | Status |
|---|---|---|
| Demo 3 financial narration gap — "financial arc recovered" vs. 0.0000 composite | Step 4 narration replaced (PR #645). New wording directs audience to indicator panel for GDP +9%, acknowledges Kirchner recovery is real, notes governance composite healing slowly, and is explicit that the full recovery arc is M11 scope. "Financial arc has recovered" removed. | **RESOLVED ✅ 2026-06-02** |
| #221 mean-reversion channel — M10 or M11? | Option B selected 2026-05-30: M11 deferral confirmed. Greece MAGNITUDE fidelity gap at stabilisation cases acknowledged. Demo 3 proceeds without mean-reversion channel. Roadmap updated (hard-constraint language removed; rationale recorded). Decision posted on #261 and #221. | Complete ✅ — 2026-05-30 |
|---|---|---|
| Trajectory endpoint implementation | FastAPI route + Pydantic model + normalized_absolute_strategy backend function. All prerequisites complete. May begin. | Ready — unblocked |
| US-GAP-001 — Andreas Mode 1 comparative case surface | **Resolved.** EL decision 2026-05-23: M10 gap. Issue #451 filed. information-hierarchy.md §COMPARE_VIEW Mode 1 placeholder added. user-stories file updated to reflect partial M9 service for Persona 3. | Complete ✅ — PR #452 |
| UX-RULING US-016 — alert text strings per mode | **Resolved.** Mode 1: `"crossed"` present; `"is projected"` + `"Caused by:"` absent. Mode 2: `"is projected to cross"`. Mode 3: ` — ` separator; starts with `"CRITICAL"` or `"WARNING"`. PR #454. | Complete ✅ — 2026-05-23 |
| UX-RULING US-022 — null vs. zero CSS class | **Resolved.** Null → `score-value--null` (opacity ≤ 60%). Numeric/zero → `score-value--numeric`. PR #454. | Complete ✅ — 2026-05-23 |
| UX-RULING US-026 — mode indicator label strings | **Resolved.** Mode 1: `"Replay"`. Mode 2: `"Simulation"`. Mode 3: `"Active Control"`. PR #454. | Complete ✅ — 2026-05-23 |
|---|---|---|
| Decision A (DA-F2): MDA floor overlays deferred to M10 | M9 trajectory view ships without MDA floor ReferenceLines except ecological WARNING at y=1.0 (boundary-crossing, defensible without backtesting). CM consultation on indicator inventory + reference ranges authorized as M10 prerequisite. M10-B schema confirmed (new mda_composite_floors table with cm_approval_reference column). ADR-010 Decision 6 amendment pending. | Complete ✅ — 2026-05-22 |
| Decision B (DA-F4): Path A selected — normalized absolute composite for single-entity trajectory | Path A: four framework curves rendered for single-entity scenarios; financial/HD use normalized absolute value composite (Tier 3 floor); strokeDasharray="8 3"; "single-country index" legend + tooltip; Zone 3 methodology note mandatory. CM reference range consultation is the hard implementation gate. ADR-010 Decision 2 amendment + Issue #193 update required. | Complete ✅ — 2026-05-22 |
| Decision C (DA-F5): step_metadata JSONB option (a) confirmed | step_metadata key in scenarios.configuration JSONB; no migration; 1-based step index keys; SIGNIFICANT or ROUTINE values (never STANDARD). ADR-010 Decision 2 minor amendment pending. | Complete ✅ — 2026-05-22 |
|---|---|---|
| ADR-010 acceptance | All 4 INCORPORATE items approved with rationale: FA-R3 (dense array contract — one null meaning only); FA-R4+UD-R1 (provisional hex values, UX Designer authority, RACI boundary correct); CM-R1 (No False Precision — deferral placeholder required); CM-R3 (composite-score floors only — indicator projection is methodologically dishonest). ADR-010 status → Accepted. ARCH-004 → ACCEPTED in backlog. M9 FA brief unblocked. | Complete ✅ — 2026-05-22 |
| ADR-008 acceptance | All 6 INCORPORATE items applied; EL decision recorded (Option A: stacked forms, ~280px); ADR-008 status → Accepted; ARCH-002 → ACCEPTED in backlog. Issue #397 closed. FA brief (FA-C1–FA-C5) deferred to M9. | Complete ✅ — 2026-05-22 |
| GovernanceModule promotion path | Deferred from M8 demo — five criteria not yet met — target M9 | Decided: deferred |
| M8 formal close / M9 kickoff | Issue #370 filed — gate: retrospective + compliance scan + Socratic Agent TEST + #209 exit checklist | Complete ✅ — v0.8.0 released, Issue #209 closed |
| M9 UX architecture — EL Decision 1 (north-star formulation) | Adopted: per-mode formulation. Mode 1: trajectory reconstruction AND historical pattern recognition. Mode 2: threshold-safe path construction. Mode 3: real-time steering within human cost constraints. All 13 marquee cases validated. | Complete ✅ — recorded on #364 (2026-05-21) |
| M9 UX architecture — EL Decision 2 (viewport architecture) | Adopted: primary viewport is the instrument cluster. Zone 1B vs 1C superseded. EntityDetailDrawer demoted to detail/methodology surface. Entity selector is persistent header element. | Complete ✅ — recorded on #364 (2026-05-21) |
| M9 UX architecture — EL Decision 3 (comparison mode conditional) | Adopted: conditional switch extended to all three modes. Single-entity Mode 2: divergence timeline. Multi-entity Mode 2: DeltaChoropleth. Mode 3: automatic live A/B (no invoke). DeltaChoropleth deprecated for single-entity and Mode 3. | Complete ✅ — recorded on #364 (2026-05-21) |

---

## Key Decisions Made — Recent Sessions

| Decision | Rationale | Date |
|---|---|---|
| Milestone 11.5 established — usability validation milestone between M11 and M12 (2026-06-04) | GitHub Milestone 14 created: "Milestone 11.5 — Usability Validation and Experience Audit". North Star document merged as `docs/vision/milestone-11-5-north-star.md` (PR #715) — governing intent document, no prescription of methodology. Four issues filed: #717 (Pillar 1 — rrweb session recording, engineering prerequisite, FA Agent + DA Agent), #718 (Pillar 2 — cold-start usability audit methodology, PM + UX Designer + UX Design Thinking + PO Agents), #719 (Pillar 3 — session provenance standard and semantic component vocabulary, DA Agent + PM Agent), #720 (exit checklist). Gate sequence: #717 and #719 must close before #718 methodology is approved; #718 must close before any session begins. Exit criterion: can a finance ministry analyst with no prior WorldSim orientation produce a finding they could cite in a negotiation? | 2026-06-04 |
| M11 near-term issues re-milestoned to M12 + #681 political economy user stories authored (2026-06-04) | Two actions: (1) 17 open M11 near-term issues re-milestoned to M12 (GitHub milestone 13): #30 #43 #45 #92 #95 #102 #103 #259 #271 #274 #275 #392 #393 #644 #13 #22 #27. These are backlog/enhancement items not required for M11 closure; they carry to M12 alongside Mode 3 and external sector module work. (2) #681 (political economy module user stories) authored as retrospective specification against delivered G16a/G16b implementation. 20 Given/When/Then stories across 11 groups. Closes #681. PR #713 merged. M11 remaining gate: exit checklist #262 only. | 2026-06-04 |
| M11 board cleanup — 45 stale issues re-milestoned; Issue #40 reopened; elite capture #679 filed (2026-06-03) | Three actions: (1) PM HORIZON Step 6 gap filed — elite capture dynamics (#679, M11, enhancement, horizon:near-term) was a named roadmap deliverable with no tracking issue. Issue body defines scope (capture coefficient per sector/cohort, distributional divergence in human cost ledger, Argentina backtesting validation), dependencies (conditionality modelling, political feasibility constraints), and CM acceptance gate. (2) Issue #40 reopened — closure comment incorrectly equated the Human Cost Ledger ADR-005 (accepted, CLAUDE.md current) with the Non-Linear Propagation Architecture ADR that #40 actually tracked (never authored). Non-linear propagation ADR does not exist; Issue #29 (implementation) remains open on M11. Corrective comment posted explaining conflation. Re-milestoned to M11. (3) Batch re-milestoning: 22 open M9 issues and 22 open M10 issues moved to M11 (#30 #89 #102 #184 #349 #393 #513 #522–#529 #540 #542–#547 #574 + M9: #13 #49 #57 #98 #100 #121 #125 #127 #128 #158 #234 #252 #253 #258 #259 #276 #286 #299 #300 #374 #375 #412); #451 (Mode 1 COMPARE_VIEW) re-milestoned to M12 — Mode 1 is M12 territory. None of these represented missed M10/M9 core deliverables — all are backlog process, standards, and enhancement items. | 2026-06-03 |
| M10 FULLY CLOSED — Socratic Agent TEST complete (2026-06-03) | Socratic Agent TEST conducted at high-level architectural level (EL preference: no implementation-level detail). Three areas confirmed: (1) GovernanceModule promotion — null/tentative display → active threshold monitoring and full MDA alert participation; (2) PMM "—" at Step 3 Argentina — no policy headroom when all thresholds breached (governance floor + ecological boundary simultaneously); (3) Argentina fixture — Platform Principle validated, second country required no new engine modes or scenario-specific code, only new data inputs. Mental model confirmed sound. Comment posted on Issue #261. Issue #261 closed. M11 is now the active milestone. | 2026-06-03 |
| NM-032 + DEMO-018/019/020 from live application comparison (PR #676, 2026-06-03) | Engineering Lead compared a live application screenshot at Step 3/4 (>1440px display) against repository artifact frame-c (1280×720 Playwright capture). Three new MEDIUM findings: DEMO-018 (CI legend raw variable names — `getIndicatorDisplayNameAny()` fix covered AttributeSelector, not Recharts legend entries for derived keys; Issue #672), DEMO-019 (PMM "—" None state has no contextual explanation for non-specialists; Issue #673), DEMO-020 (Zone 1A y-axis tick labels clipped at left boundary when ecological score >1.0; `margin.left` too narrow for 6-char labels; invisible at 1280×720; Issue #674). Root cause: demo screenshot spec captures at 1280×720 while legibility gate validates at 1440×900 and live demo presents at ≥1440px — the review chain reviews a different visual artifact than what the stakeholder sees. NM-032 filed. Fix issue #675 (M11): set `page.setViewportSize({ width: 1440, height: 900 })` in demo spec before each capture; update SCREENSHOT_DIR to m10/screenshots/; update demo-preparation-standard Steps 4 and 6 with explicit viewport requirement. | 2026-06-03 |
| Step 6b internal team review process + M10 inaugural artifact (PR #666, closes #663, 2026-06-03) | Three-tier review structure (self-check → internal panel → IR Agent) documented in `demo-preparation-standard.md`. Step 6b defines the nine-agent panel (FA, UX Designer, UX Design Thinking, PO, Customer, QA Lead, DA, Chief Methodologist, Dev Economist), DEMO-NNN finding format, CRITICAL resolution criteria (a/b/c), and gate definition. Inaugural M10 artifact (`docs/demo/m10/reviews/2026-06-03-v0.10.0-internal-review.md`) produces DEMO-010 through DEMO-017. Four MEDIUM findings filed as #667–#670 (all M11, near-term). Internal Demo Reviews added to CLAUDE.md canonical artifact locations table. | 2026-06-03 |
| Demo/IR process gaps 2 + 4 remediated (PR #665, 2026-06-03) | Gap 2: demo cycle added as named step 4 of MILESTONE_RUNBOOK.md closure ceremony (even-numbered milestones only). Gap 4: HIGH finding tracking requirement added to Step 8 of `demo-preparation-standard.md` — issue number must appear in review artifact summary table before Step 9. Gaps 1 (severity vocabulary) + 3 (sequencing) filed as Issue #664 for M11. Gap 1 vocabulary corrected in Issue #663 body. | 2026-06-03 |
| CLAUDE.md frontend pre-push gate added (2026-06-03) — retrospective requirement #3 | For any branch modifying files under `frontend/src/`, run `cd frontend && npm run build` before pushing. Must exit 0. Adds a sibling rule to the existing backend pre-push lint gate. Near-miss record: SCAN-024 (7 TS6133 errors accumulated across M10 PRs without detection because this gate did not exist). This was the third blocking requirement from the M10 retrospective posted on Issue #261. | 2026-06-03 |
| M10 retrospective posted on Issue #261 (2026-06-03) | Three questions answered per CLAUDE.md §Milestone Retrospective Process. Three blocking M11 requirements identified: (1) Playwright E2E regression suite for Zone 1 before any Zone 1 refactor; (2) component rendering test for MDA columnWidth calculation before any Zone 1B layout change; (3) frontend TypeScript build added to pre-push gate (CLAUDE.md updated this session). Retrospective posted as comment on GitHub Issue #261. | 2026-06-03 |
| ADR license audit complete — all six ADRs extended to M11 (PR #661, 2026-06-03) | ADR-001: no triggers fired (no schema changes in M10). ADR-002: GovernanceModule `EMERGENCY_DECLARATION` is GovernanceModule-internal enum, not a `ControlInput` taxonomy addition — no trigger. ADR-005: Amendment 5 appended — GovernanceModule promotion 5/5 criteria met; M9 normalization obligation discharged; M9 tooltip obligation discharged (IR-005, #499). ADR-007: not implemented in M10, no Quantity schema changes. ADR-008: step_event_label content fix ≠ schema rename; Zone 1 implementation per spec is not a trigger. ADR-010: PMM API extension fields not consumed by TrajectoryView; note that ADR-009 streaming decision may trigger shared state architecture trigger in M11. | 2026-06-03 |
| Issues #22/#27/#43/#45 re-milestoned to M11 with deferral rationale (2026-06-03) | All four were `horizon:immediate` in M10 but undelivered. #22 (confidence_tier split): requires ADR-007 Quantity fields not yet implemented. #27 (Monte Carlo bands): cannot scope before ADR-009 (engine computation model, M11 core deliverable). #43 (backtesting harness): blocked by sparse matrix proof-of-concept (M11). #45 (fidelity dashboard): downstream of #43. Substantive rationale comments posted on each GitHub issue before re-milestoning. | 2026-06-03 |
| SCAN-024 compliance scan complete — 7 TS6133 errors fixed, CHANGELOG v0.10.0 merged (PR #660, 2026-06-03) | Ruff: clean (0 violations). TypeScript build: clean post-fix (7 TS6133 unused import errors on M10 new components + dead `ConfidenceBadge` component removed from `TrajectoryView.tsx`; `getConfidenceBadgeVisible()` predicate retained — exported and tested). mypy: not run locally (no venv); CI runs on every PR. SCAN-024 appended to scan-registry.md. ADR renewals flagged for M11. CHANGELOG v0.10.0 entry added. | 2026-06-03 |
| M10 stakeholder review artifact complete — PR #658 (2026-06-02) | Issue numbers added to all five IR-S7 findings in `docs/demo/m10/reviews/2026-06-02-v0.10.0-stakeholder-review.md`, matching M8 convention. IR-S7-001/002 → #647 (closed, PR #651); IR-S7-003 → #634 (demo umbrella, screenshot-resolution only); IR-S7-004 → #648 (closed, PR #650); IR-S7-005 → #342 (DEMO-001 root cause, M11 Option B). Summary table updated with Issue and Resolution columns. | 2026-06-02 |
| Stakeholder screen recording complete (2026-06-02) | EL ran the demo manually via `./scripts/demo.sh` + QuickTime at 1440×900 using the updated `docs/demo/stakeholder-walkthrough.md` script (PR #654). No Playwright re-run required — narration changes are in the script, not the application UI. | 2026-06-02 |
| NARRATION-RULING-1 codified — PR #655 (closes #652 process hardening) | Three-layer narration structure (umbrella → facts → synthesis) added as §16 to `docs/ux/standards.md`. Step 5c self-check added to `docs/process/demo-preparation-standard.md` — gates each milestone's walkthrough against NARRATION-RULING-1 before the IR Agent sees it. Prevents presenter-skill dependency for the "so what" at each demo step. | 2026-06-02 |
| Demo review naming consistency — NM-031, PR #656 | M10 review files renamed to canonical convention: `demo3-screenshot-ir.md` → `2026-06-02-v0.10.0-stakeholder-review.md`; `demo3-ir.md` → `2026-06-02-v0.10.0-pre-gate-triage.md`. Demo prep standard strengthened with explicit naming rule, mandatory pre-creation `find` command, canonical suffix definitions. Root cause: standard stated the pattern in a folder diagram but had no enforcement step. | 2026-06-02 |
| Demo 3 Step 9 complete — stakeholder demo session confirmed end-to-end (PRs #649–#651) | Playwright demo spec ran at 1440×900 (1 passed, 4.3m). Five frames captured. PMM trajectory API confirmed: Steps 0–1 = 0.2857 (governance headroom ≈ 0.29, CO2 breach excluded), Step 2 = 0.4286 (↑ Kirchner improvement), Steps 3–4 = None (governance threshold breached). Zone 1B full-density cards render at 400px column (WARNING cards legible). Issues #634/#647/#648/#345 closed. Issue #652 filed (narration legibility — umbrella framing and synthesis; M10 Near-Term). | 2026-06-02 |
| PMM breach-exclusion fix — skip breached thresholds (PR #650, closes #648) | Root cause: ecological CO2 boundary (≥ 1.0) breached from step 0 in Argentina (seed ≈ 1.056); old min(margins) collapsed to 0, masking governance headroom. Fix: `_compute_pmm_for_step` skips thresholds with margin == 0. MDA alerts carry the breach signal; PMM measures remaining headroom on non-breached thresholds. Returns None when all thresholds breached (shown as "—" in UI). 31 unit tests pass; three new tests replace `test_min_across_thresholds` (which encoded the old wrong contract). | 2026-06-02 |
| Zone 1B responsive columnWidth fix (PR #651, closes #647) | Root cause: `MDAAlertPanelZone1B` hardcoded `columnWidth={240}` in ScenarioInstrumentCluster — always compact (11px, abbreviated labels) regardless of viewport. At 1440×900 the co-primary column is 400px → should be full-density (12px, full severity labels, untruncated names). Fix: exported `LAYOUT` and `useViewportBreakpoint` from InstrumentCluster; ScenarioInstrumentCluster now passes `LAYOUT[bp].coPrimary` as columnWidth. Resolves IR-S7-001 (CRITICAL) from Demo 3 IR review. | 2026-06-02 |
| EL decision — Demo 3 narration legibility gap (Issue #652) | Narration delivers facts without scaffolding: no umbrella sentence (why now?), no synthesis sentence (so what?), no connective tissue between steps. Same compression-over-legibility problem as Issue #621 applied to narration. EL instructed: file Issue #652, assign M10 Near-Term; independent reviewer activation using senior fiscal policy analyst framing (someone who has sat on both sides of a programme negotiation). UX Designer Agent is R; PM Agent is C. Rewrite should not change factual content — only add framing. | 2026-06-02 |
| Financial narration EL decision — Step 4 wording (PR #645) | Replaced "the financial arc has recovered" with honest scope framing: directs audience to the GDP indicator panel (showing +9%), acknowledges the Kirchner recovery is real, notes governance healing slowly, and explicitly names the recovery arc as M11 scope. Resolves the demo-blocking narration gap identified in Demo 3 review (Issue #634). Three M11 issues filed from panel review: #642 (EmergencyPolicyInput integration test — mandatory before M11 exit), #643 (ESLint exhaustive-deps audit), #644 (setTrajectory refactor — must not set current_step as side effect). All three assigned to Milestone 11 via GitHub API. | 2026-06-02 |
| Demo 3 CRITICAL bug cluster fixed + screenshots captured (PR #639) | Four bugs fixed: (1) `ScenarioInstrumentCluster.tsx` trajectory useEffect depended only on `[scenarioId]` — never re-fetched after step advances; fixed to `[scenarioId, currentStep]` with step-0 guard. (2) `setTrajectory` store action sets `current_step: trajectory.step_count`, clobbering prop-driven step; fixed by immediately re-asserting `currentStep` after `setTrajectory`. (3) GovernanceModule `_SUBSCRIBED_EVENTS` used bare instrument names (`"emergency_declaration"`); `EmergencyPolicyInput.to_events()` emits `"emergency_policy_emergency_declaration"` — corrected throughout module + elasticity registry + unit tests. (4) EcologicalModule temporal guard blocked pre-2009 CO2 proximity for Argentina (2001 start); fixed with per-constant `retroactive` flag; `_fetch_active_boundary_constants` changed to `WHERE effective_from <= NOW()`. Five Demo 3 screenshots captured with real data. Governance MDA-GOV-DEMOCRACY-FLOOR fires at step 3 (DQS 0.665 < 0.70). IR-004 Playwright test fixed: `page.waitForResponse` before `advanceStep`, then `page.waitForFunction` polls DOM for year text. Known gap: financial composite stays 0.0000 from step 2 (Kirchner recovery not in fixture) — narration "financial arc recovered" does not match instrument output; decision required before demo session. | 2026-06-02 |
| NM-028/029/030 filed + panel review posted (PR #640, comment on #634) | Three near-misses filed: NM-028 (IR-004 silent no-op — hasSvg guard returned early for one milestone; same anti-pattern as NM-027; no-op check not run at wire-up merge boundary); NM-029 (GovernanceModule event_type false positive coverage — 25 unit tests passed with wrong synthetic event_type strings, never crossing EmergencyPolicyInput adapter; highest-severity of the three); NM-030 (EcologicalModule temporal guard silently blocked retroactive CO2 proximity for pre-2009 backtesting without user-visible error). Four-agent panel review (Architect, Frontend Architect, QA Lead, UX Designer) posted to Issue #634. Key panel findings: `setTrajectory` should not set `current_step` (FA — store design flaw, follow-up issue needed); ESLint `exhaustive-deps` rule should be audited and enforced (would have caught the useEffect missing-dependency bug); integration test required for input adapter → subscriber event_type contract; financial 0.0000 vs. "recovered" narration is a demo-blocking UX gap requiring EL decision. | 2026-06-02 |
| M10 Immediate process sweep complete (PR #635) — 8 issues closed | MILESTONE_RUNBOOK.md table corrected to M0–M13; CONTRIBUTING.md stale develop-branch instructions replaced; ADR threshold criteria table added to CODING_STANDARDS.md; "ADRs Affected" and Playwright phases 3–4 attestation added to PR checklist; Customer Agent added as 13th standing consultation obligation (UX-facing ADRs); step_event_label mandatory field standard added to DATA_STANDARDS.md; Greece fixture annotated with step_metadata; FidelityDashboard M7 labels updated to M11. Remaining M10 Immediate: #261 (exit checklist), #345 (DEMO-004 manual run), #634 (demo prep Steps 2–6, Step 7, 8, 9). | 2026-06-02 |
| IR review (PR #618) is a pre-gate triage artifact, not the Step 7 review for Issue #634 | The earlier IR review predates UX-RULING-4 and was conducted without screenshots. Step 7 on Issue #634 remains unchecked. The proper Step 7 review requires: Steps 2–6 complete (UX Agent screenshot brief, demo.sh update, Playwright spec update, walkthrough update, screenshot capture), then a fresh IR session with screenshots in UX Agent brief sequence and UX-RULING-4 narration discipline in scope. | 2026-06-02 |
| docs/demo/ RACI ownership established; UX/UI standards document created (PR #631) | PM Agent is now R on `docs/demo/` — demo preparation is a blocking exit requirement per milestone. `docs/ux/standards.md` created as the canonical consolidated standards document (15 sections, 15 settled decisions). EL sign-off required for any new standard or existing change. UX Designer Agent is R; Frontend Architect Agent is Required C. | 2026-06-02 |
| UX-RULING-4 — choropleth is a context surface, not a change instrument; #342/DEMO-001 closed as narration-fix scope | FA Agent proposed two fixes for DEMO-001 (HUD overlay on choropleth; supplementary Zone 1D attribute row). UX Designer declined both as hierarchy inversions. Ruling reframed the root cause: the demo narration was pointing at the wrong instrument. M10 fix: narration update only (child #628, PR #629). M11 fix: Option B scenario-relative color scale (requires cross-step range endpoint — scoped for M11). Zone 1D is composite scores only (no raw indicator rows) until a new UX ruling authorises an expansion. | 2026-06-02 |
| DEMO issue dispositions — full sweep complete (2026-06-02) | Closed: #342 (DEMO-001, narration), #343 (DEMO-002, redesign), #346 (DEMO-005, redesign), #348 (DEMO-007, #616 fix), #350 (DEMO-009, #617 fix), #379 (demo standard), #628 (narration script). Left open: #345 (DEMO-004, investigation required — manual Argentina demo run needed), #349 (DEMO-008, screenshot naming — near-term, addressed in demo standard Step 6). | 2026-06-02 |
| DEMO issue dispositions — #348/DEMO-007 + #350/DEMO-009 closed; #345/DEMO-004 data precondition noted (2026-06-02) | #348 (DEMO-007, "boundary reference absent") closed — resolved by PR #622 (#616: `ecological-boundary-note` span; regression-guarded by `demo-legibility.spec.ts` in PR #626). #350 (DEMO-009, "attribute selector raw field names") closed — resolved by PR #622 (#617: `getIndicatorDisplayNameAny()` wired). #345 (DEMO-004, "alerts appear identical across steps") left open with data-precondition comment: PR #624 (#615) provides Argentina governance alert variation at step 3; the test gate is `demo-advancement-flow.spec.ts` test 3 (Zone 1B live/non-blank). Close #345 after a full demo run-through confirms visual accumulation end-to-end. #342/343/346/349 remain open (not addressed by this session's PRs). | 2026-06-02 |
| Demo 3 readiness gate COMPLETE — PRs #622 + #624 (2026-06-02) | All three IR-M10 gate items closed: #615 (governance MDA breach — `emergency_declaration` at step 2, GovernanceModule one-step lag → score 0.665 at step 3 ≤ 0.70 floor); #616 (Zone 1D ecological annotation — "1.0 = boundary" sub-label); #617 (AttributeSelector display names — `getIndicatorDisplayNameAny()`). Demo 3 is presentation-ready. Root cause of #615: fixture comment falsely claimed `emergency_declaration` was already in base scheduled_inputs; it was not; `default_declaration` is not subscribed by GovernanceModule. | 2026-06-02 |
| Demo 3 IR review complete — PR #618 (2026-06-02) | IR review at `docs/demo/m10/reviews/2026-06-02-v0.10.0-pre-gate-triage.md` (renamed from `demo3-ir.md` for naming consistency — NM-031). All six M9 IR findings (IR-001–IR-006) confirmed closed by M10 PRs. DEMO issue re-triage: #347 (DEMO-006) CLOSED — governance live; #342 (DEMO-001) Critical→Minor — Zone 1A is primary instrument; #343 (DEMO-002) Substantially resolved; #346 (DEMO-005) Significant→Minor — Zone 1D covers it. Three new findings: IR-M10-001 (Argentina MDA accumulation uncertainty → #615), IR-M10-002 (ecological Zone 1D annotation gap → #616), IR-M10-003 (AttributeSelector raw field names → #617). Demo 3 readiness gate: #615/#616/#617 must close before Demo 3 presentation. Positive: all four Zone 1 instruments live, governance live (4th axis solid, no longer dashed), Platform Principle demonstrated. | 2026-06-02 |
| ARCH-REVIEW-006 complete — Issue #577 scope review; 11 child issues filed (#603–#614) | Architecture Review Facilitator TARGETED review produced 16 blindspots across US-039/042/043/048. One Immediate blocker: CM vocabulary mapping standard (#603, AR-006-B-007) must be authored before US-043 implementation begins. 11 GitHub Issues filed as Issue #577 children (#603–#614) with tracking comment on #577. Zone 1/2 bidirectional coupling atom (AR-006-B-011, #609) and Zone 2 multi-view model (AR-006-B-012, #610) are the two architectural pre-decisions for US-048. Branch-and-recompute CE assessment (AR-006-B-001, #604) is the prerequisite for US-039 M12 scoping. `docs/architecture/reviews/ARCH-REVIEW-006-milestone10.md`. | 2026-06-02 |
| EL decision — US-039 milestone confirmed M12 | No urgency to pull US-039 (Mode 3 real-time parameter change) into M11. Mode 3 is the M12 core deliverable; building the control plane form before Mode 3 instrumentation exists would be premature. Exception path (Mode 2 quick-create variant) not pursued. Issue #577 pre-activation blocker resolved. | 2026-06-02 |
| US-043 No False Precision correction applied (PR #598) | PI-REVIEW-002 F-005 resolved. Three changes to `docs/ux/user-stories-public-advocacy-m10.md`: (1) north-star sentence: "removes confidence tier notation" → "replaces technical confidence tier notation with plain-language epistemic disclosure"; (2) technical-notation criterion scoped to primary content only, with cross-reference to disclosure criterion; (3) new acceptance criterion added: for any indicator with confidence_tier ≥ 3, community report must contain plain-language epistemic disclosure per vocabulary mapping standard (Tier 3 → "Based on a model estimate from comparable countries"; Tier 4 → "This is an estimated figure — independent verification recommended"; Tier 5 → "Insufficient data — the model could not compute this reliably"). Chief Methodologist is Required Consultant on vocabulary mapping standard before implementation begins. QA may now write the pytest criterion for disclosure presence. | 2026-06-02 |
| PI-REVIEW-002 complete — Issue #577 scope assessed (PR #596) | Four [Phase-3-TBD] stories from Issue #576 classified: US-039 → Extension of Mode 3 (M12; exception path to M11 if Mode 2 variant confirmed by UX Designer); US-042 → Post-processing overlay recommended — epistemically correct; Mode 4 rejected; Mode 1 extension possible with DA input (M11); US-043 → Standalone rendering/export tool — HIGH No False Precision risk: acceptance criteria must add plain-language epistemic disclosure vocabulary (Tier 3/4/5) before implementation begins (M11); US-048 → New Zone 2 surface + backend provenance API — bidirectional Zone 1/2 coupling novel; Chief Engineer gates on graph traversal feasibility; ADR-009 may be prerequisite (M11 or M12). Key process clarification: correct Issue #577 activation is `Architecture Review: TARGETED`, not `Council Orchestrator: ORCHESTRATE`. Pre-activation blockers: PO Agent corrects US-043 acceptance criteria; EL confirms US-039 milestone. | 2026-06-02 |
| Issue #576 closed — public advocacy user journeys and stories complete (PR #594) | Journeys E–H added to `docs/ux/user-journeys.md`: Journey E (Farida Haidari — Pakistan 2022 combined-shock story investigation; Layer 3 constraint; 2-hour cap; MDA plain-language exit), Journey F (James Ochieng — Kenya EFF committee brief; 72-hour Hansard standard; ADR methodology citation; downloadable tabular output), Journey G (Abena Osei — Ghana ECF accountability monitoring; Option C ratified: Mode 2 committed baseline is genuine service; observed-actuals overlay and community output layer classified [Phase-3-TBD]), Journey H (Dr. Priya Krishnaswamy — India 2020 farm law backtesting vs. Wardha field data; 5pp divergence accepted within plausible range given comparison group; X-ray layer [Phase-3-TBD] in Zone 2). `docs/ux/user-stories-public-advocacy-m10.md` created: 19 stories US-030–US-048 — 6 [Playwright] QA-unblocked, 9 [Near-Term-Gap] blocked pending tracking issues, 4 [Phase-3-TBD] as formal input to Issue #577. Retrospective entry state extended in dependency map with two sub-modes (historical calibration / accountability tracking). | 2026-06-02 |
| Issue #575 closed — public advocacy personas panel complete (PR #592) | Four additions to `docs/ux/personas.md`: Persona 6 (Investigative Journalist — Farida Haidari, Dawn/Pakistan; primary cognitive task is producing a single publishable sentence from the MDA alert panel without specialist mediation; marquee case: Pakistan 2022 flood + IMF energy subsidy combined-shock failing the programme's bottom-quintile protection assumption); Persona 7 (Parliamentary Economist — James Ochieng, Kenya PBO; 72-hour deadline and Hansard citation standard; marquee case: Kenya 2023 EFF committee minority report that lacked specific threshold/step/cohort evidence); Persona 8 (Civil Society Monitor — Abena Osei, SEND Ghana; Retrospective accountability sub-mode; marquee case: Ghana 2023 ECF social protection floor breach; platform gap: integrated observed-actuals input not yet a capability); Persona 4V (Personal-Connection Researcher — Dr. Priya Krishnaswamy, CDS/JNU; Vidarbha cotton farmer father; marquee case: The Wardha Divergence — backtesting India 2020 farm law deregulation against 47-household field survey). Retrospective entry state extended to two sub-modes (historical calibration + accountability tracking). No 7th entry state required. | 2026-06-02 |
| Argentina Demo 3 complete — Issue #553 closed (PR #590) | `build_argentina_demo_scenario()` added to `tests/fixtures/argentina_2001_2002_scenario.py` following the `build_greece_demo_scenario()` pattern. Extends the 2-step backtesting base to 4 steps (2001–2004 arc through Kirchner recovery). EcologicalModule enabled with CO2 seed 369.5 ppm (NOAA MLO 2000); GovernanceModule enabled with rule_of_law_percentile=33.2 (WGI ARG 2000) and democratic_quality_score=0.71 (V-Dem LDI ARG 2000). step_metadata event labels: step 1 "Zero Deficit Plan / Blindaje" (SIGNIFICANT), step 2 "Default / Peso devaluation" (SIGNIFICANT), step 3 "Kirchner recovery begins" (SIGNIFICANT), step 4 ROUTINE. Latent bug fixed: `step_metadata` added as declared field to `ScenarioConfigSchema` in `app/schemas.py` — field was already read by the trajectory endpoint from `cfg_raw` but was silently stripped by Pydantic on POST. Demo walkthrough script at `backend/scripts/demo_argentina_2001_2002.py`. 21 new unit tests (51 total in `test_argentina_backtesting_fixtures.py`). | 2026-06-02 |
| NM-027 — AC-007/AC-008 silent no-ops; QA Lead + FA process improvements (PR #570, closes #568, #571) | AC-007 (trajectory-render performance mark) and AC-008 (advance-step-btn testid) were silent no-ops for one full milestone. `TrajectoryView.tsx`: `useLayoutEffect` + `requestAnimationFrame` pattern fires `performance.measure("trajectory-render-initial", ...)` once per mount. `ScenarioControls.tsx`: `data-testid="advance-step-btn"` added to advance button. Four process findings encoded: QA-NM027-F1 (HORIZON skip audit extended to `if (value !== null)` guard pattern); QA-NM027-F2 (guarded tests must carry explicit implementation dependency record); FA-NM027-F1 (pre-PR checklist distinguishes structural vs behavioural ACs); FA-NM027-F2 (FA brief authorship standard — `[behavioural]` annotation required). Issue #550 (MV-002) unblocked. Issue #569 (M12 AC-009 re-run) open. | 2026-06-01 |
| CI playwright-e2e fixed — system Chrome replaces CDN download (PR #570) | Five consecutive `playwright-e2e` cancellations traced to Playwright Chromium CDN delivering at ~40 KB/s on free-tier runner (~60-min download). Fix: `playwright.config.ts` uses `channel: "chrome"` (system-installed Google Chrome on ubuntu-latest runners — no download). `ci.yml`: removed cache + conditional install steps; kept only `npx playwright install-deps chromium` (fast apt-get, ~2 min). Timeout restored to 30 min. CI green on first run after fix. | 2026-06-01 |
| Issue #514 complete — Phase 1 engine baseline benchmarks (PRs #565 + #566) | Script (`backend/scripts/benchmark_phase1.py`) and results document (`docs/architecture/engine-baseline-benchmarks-m10.md`) merged. Two machines measured: M1 Pro dev machine and ProBook (i5-8265U, 8 GiB, Windows 11). Key findings: (1) edge density, not entity count, drives propagation cost; (2) ProBook throughput ~5,750 MC runs/s — within interactive budget; (3) memory negligible (< 0.2 MiB at largest config); (4) no blocking constraint for ADR-009. Five findings documented for ADR-009 authoring. | 2026-05-31 |
| Python 3.12 → 3.13 upgrade — PR #564 | pyproject.toml, .python-version, ci.yml (4 jobs), and CONTRIBUTING.md updated to Python 3.13. Rationale: dev machine runs 3.13.11; benchmark comparisons require identical Python version across machines; upgrading configs is correct over downgrading dev environment. | 2026-05-31 |
| IB + DQ agents fully defined; CE activated — PR #563 (closes #523 + #524) | IB Agent (Intent Block Author): full working agreement, RACI row 7 promoted I→R (divergence detection is compliance function), activation prompt template at `docs/process/intent-block-author-prompt.md`. DQ Agent (Data Quality): full working agreement, certification battery, activation prompt template at `docs/process/data-quality-agent-prompt.md`. CE Agent: status promoted Defined-inactive → Active (M10, Issue #514). PM HORIZON step 7: Defined-inactive activation audit added (checks open milestone board against each Defined-inactive agent's trigger each sweep). | 2026-05-31 |
| Recurring metadata alignment check — PR #562 (closes #561) | MILESTONE_RUNBOOK.md: Kickoff Gate step 0 (four-artifact metadata alignment check) and Closure Ceremony step 7 (same check before next milestone creation) added. Four artifacts: GitHub milestone title/description, CLAUDE.md §What We Are Building First, CLAUDE.md §Milestone Roadmap, roadmap.md. Root cause of six M10 kickoff discrepancies: no ceremony step prompted the check. | 2026-05-31 |
| M10 kickoff gate complete (2026-05-30) — PR #557 | PM Agent scope-completeness check run against CLAUDE.md and roadmap. Finding 1 RESOLVED: GovernanceModule promotion was untracked — Issue #556 filed (M10 Immediate, five ADR-005 criteria). Finding 2 EL DECISION PENDING: #221 (mean-reversion channel) — roadmap stated "hard constraint, cannot be deferred past M10" but board split moved it to M11; EL must choose Option A (revert #221 to M10) or Option B (accept M11 deferral + roadmap update). Roadmap updated (PR #557): Argentina confirmed (#553), Phase 1 benchmarks in M10 (#514), scope linkage issue numbers added. Kickoff baseline posted on exit checklist #261. Pre-implementation gate sequence: #523 → #524 → EL decision on #221 → #514 → #550. No implementation PR may open until EL confirms baseline. | 2026-05-30 |
| M10/M11 issue split executed (2026-05-30) | Four-batch milestone reorganization: (1) 11 unmilestoned issues → M10 Immediate (#514, #523, #524, #535–#539, #541, #543, #550); (2) 12 unmilestoned issues → M10 Near-Term (#522, #525–#529, #540, #542, #544–#547); (3) 11 Demo-3-critical issues upgraded M10 Near-Term → M10 Immediate (#342, #343, #345–#348, #350, #496–#498, #500); (4) 23 engine/SA-* standards issues pushed M10 → M11 (#29, #44, #46, #91–#92, #95, #103, #116, #118–#119, #122–#123, #147, #151–#152, #154–#155, #160, #173, #221–#222, #271, #275). Board: M10 = 54 open (34 Immediate / 20 Near-Term), M11 = 42 open, unmilestoned = 0. Kept in M10 (foundational, ADR-007/Demo 3 prerequisites): #22, #27, #30, #43, #45, #89, #102, #184, #451. | 2026-05-30 |
| Argentina 2000–2002 second country fixture filed — Issue #553 | Demo 3 anchor issue filed: `feat(fixture): Argentina 2000–2002 second country fixture — IMF debt crisis (Demo 3)`. Milestone: M10, horizon:immediate. CM data availability check is the blocking prerequisite before implementation begins — CM must validate all core WorldSim indicators at Tier 1–2 for the 1999–2003 window (IMF IFS/WEO, WDI, INDEC 2000–2002 pre-manipulation era, V-Dem, ILO, UNESCO). Argentina selected over Iceland 2008–2011 and South Korea 1997–1999: IMF SBA data Tier 1, INDEC 2000–2002 Tier 1–2 (pre-manipulation), V-Dem Tier 1, distinct political economy from Greece. Demo 3 requires all four Zone 1 axes live with Argentina data + Greece comparison. | 2026-05-30 |
| Issue Disposition Audit SOP + NM-026 (PR #551) | Codified milestone exit issue cleanup as a blocking pre-step in MILESTONE_RUNBOOK.md §Issue Disposition Audit. Root: Issue #514 closed COMPLETED during M9 exit without delivering the benchmark document — NM-020 referenced it (documented the gap) which EL interpreted as resolution. Three rules now explicit: (1) COMPLETED closures require PR or EL comment; (2) near-miss filing does not close the issue it references; (3) manual gates must have GitHub issues. NM-026 filed (Reactive, High). Issue #514 reopened (M10 blocking prerequisite for ADR-009). Issue #550 created for MV-002 frontend render baseline. M9 exit window audit: #514 confirmed only bad closure; all others legitimate. | 2026-05-29 |
| PI-AUDIT-002 complete (PR #548) — end-to-end pipeline audit | All 8 pipeline stages documented. 14 findings (F-RUNBOOK-1, F-CONTRIB-1, F-AGENTS-1/2, F-PIPELINE-1/2/3/4, F-ADR-1 through F-ADR-9). Capstone: Political Feasibility Score widget traced through 14 pipeline steps — 5 FRAGILE or BREAKDOWN. Three near-miss entries filed (NM-023: CONTRIBUTING.md "branch from develop" stale; NM-024: Playwright phases 3–4 not CI-enforceable; NM-025: demo story ownership gap). 13 GitHub issues filed (#535–#547). Highest-leverage M10 blockers: #538 (ADR threshold criteria), #541 (cross-ADR impact PR field), #543 (Playwright enforcement). Audit doc: `docs/process/audits/PI-AUDIT-002-pipeline-2026-05-25.md`. | 2026-05-25 |
| Customer Agent defined (PR #533, closes #532) | Active agent (CU) for Layer 3 institutional capacity asymmetry — the gap identified in PI-REVIEW-001 F-001. Mandate: ensure WorldSim outputs are usable without specialist mediation by Personas 2 (Ministry Negotiator), 3 (Political Advisor), and 5 (Institutional Decision-Maker). Canonical question: does this output make sense to Aicha Mbaye's chief of staff, alone with a tablet, in five minutes, without Lucas Ferreira in the room? Three activation modes: AUDIT (Layer 3 usability pass/fail), ADOPTION (institutional adoption pathway), BRIEF (customer voice for EL). Standing gates: 90-second retrieval window (Persona 2 Reactive) and 5-minute demonstration window (Persona 5 Reactive). RACI: C on Rows 1/2/3/8; R on docs/customer/ artifacts. Three standing consultation obligations added to agent-raci.md cross-agent patterns (CU → UX Designer, CU → PO, CU → Ar). File authority: agents.md (PM R ✓, EL C satisfied by EXECUTE); agent-raci.md decision-type grounding additions flagged for Ar review per NM-021. | 2026-05-25 |
| PI Agent REVIEW — agent team organization (PR #530, closes no issue — REVIEW mode produces findings doc) | Agent team assessed against the Founding Document's three-layered asymmetry frame. Nine findings across six concrete gaps (F-001–F-006) and three systemic observations (S-001–S-004, S-001 descriptive only). Key structural gap: Layer 3 information asymmetry (institutional capacity) has no dedicated agent. Secondary gaps: backtesting Eureka function (learning from historical divergences) has no owner; IB and DQ agents must be defined before M10 implementation begins; CE activation trigger has fired (Issue #514 commissioned) but CE remains defined-inactive; Mode 3 zone compatibility has no standing implementation gate; DIC blind interview protocol not encoded at the individual member level. Nine GitHub issues filed (#521–#529). Comment filed on Issue #278 (technocratic emigration orphan — M11 triage recommendation). Findings document: `docs/process/audits/PI-REVIEW-001-agent-team-2026-05-25.md`. | 2026-05-25 |
| PI Agent inaugural four-lens audit complete (PR #519) | Registry lens: near-miss registry header corrected (PM→PI), count updated (19→22 entries). Process adherence lens: two file authority violations across PRs #515 and #517 filed as NM-021. Compliance lens: scan ordering inversion corrected (SCAN-022 before SCAN-023) — third occurrence confirmed systemic. Systemic lens: stale cross-reference pattern filed as NM-022 (CE ADR ref stale 3+ milestones; registry header stale after PR #517; no standing detection process). Process improvements applied: PM Agent and Implementation Agents pre-commit checklists (file authority check per NM-021); PI Agent working agreement (enhanced scan ordering rule; ownership transfer checklist per NM-022); Architect Agent AMEND mode (ADR number cross-reference grep per NM-022); agent-raci.md Notes column clarifications for backlog.md and agent-raci.md rows (per NM-021). | 2026-05-25 |
| Process Integrity Agent defined (PR #517, closes #516) | New standing agent (PI) owns the process health evidence trail: near-miss-registry.md, known-issues-registry.md, compliance scan registry, ADR license audit. PM becomes Informed on registry files; PI is author of record. Four activation modes: REGISTER, AUDIT (four-lens: registry health / process adherence / compliance / systemic clustering), SCAN, REVIEW. File ownership transferred: near-miss-registry.md + known-issues-registry.md PM→PI; scan-registry.md Sr→PI (Sr becomes Required C on security-relevant findings). PM working agreement updated: PM determines categorization, routes to `Process Integrity Agent: REGISTER`. PI added to RACI matrix: R on rows 6 (process/milestone) and 7 (compliance). CE stale ref fixed in agent-raci.md Agent Key and Cells with Implicit I Only (ADR-007 → ADR-009). | 2026-05-25 |
| NM-020 filed — backend compute baseline gap; stale CE ADR ref fixed; backlog prerequisite clause rule added (PR #515) | Phase 1 baseline benchmarks for the iterative simulation engine (comprehensive profiling: per-step cost at 1/10/100 entities, propagation cost as edges scale, Monte Carlo throughput) were never established as a tracked work item despite being listed as a prerequisite for ADR-009 authoring across three milestones. Root causes: (1) backlog Notes "Do not author until X" creates no GitHub issue; (2) stale CE ADR reference in agents.md (ADR-007 → ADR-009 in three locations); (3) naming collision — MV-002 is a frontend render gate, not a compute baseline; (4) Chief Engineer Defined-inactive with no HORIZON obligation for its activation prerequisite. Five process improvements: Issue #514 filed (Phase 1 baseline benchmarks, assign to M10 when created); agents.md stale refs corrected; backlog prerequisite clause rule added to docs/architecture/backlog.md; MV-002 explicitly scoped as frontend-only in mv-gates.md; HORIZON check extension documented. | 2026-05-25 |
| ADR-007 accepted — Synthetic Data Framework (PR #510, closes #508) | Seven-section framework: five-method hierarchy (Bayesian > MICE > Bootstrap > Structural Extrapolation > Structural Absence), mandatory per-indicator disclosure (never suppressible), scenario banding (pessimistic/realistic/optimistic), confidence tier sub-labels (Tiers 3–5), MDA alert behavior by tier (Tier 3 advisory amber / Tier 4 secondary panel only / Tier 5 none), three-condition meaninglessness threshold, anomaly detection (TSC sign-off required). Four INCORPORATE items applied from panel review (CM, Data Architect, Development Economist). `Quantity` gains 4 new fields: `is_synthetic: bool`, `synthetic_method: str \| None`, `comparison_group_id: str \| None`, `holdout_validated: bool \| None` — all new, none pre-existing. Comparison group registry follows `source_registry` pattern (Issue #300, managed by Data Quality Agent). ADR-007 Mermaid flowchart at `docs/architecture/ADR-007-method-selection-flowchart.mmd`. ARCH-001 in backlog: ACCEPTED. | 2026-05-23 |
| ADR-005 Amendment 4 — GovernanceModule M9 exit formal assessment (PR #509, closes #507) | Five promotion criteria assessed: all Not Met. GovernanceModule formally deferred to M10. M9 Governance Normalization Obligation recorded: before specifying governance composite score strategy, must audit each of five indicators for absolute threshold equivalents (V-Dem electoral autocracy threshold, RSF press freedom floor, WJP rule of law breakpoints). ADR-005 M8-5 tooltip obligation updated: Target M9 → Target M10. License renewed for M10. | 2026-05-23 |
| Document referencing convention — Issue #398 resolved (PR #510) | Three conventions added to `docs/CODING_STANDARDS.md §Document Referencing Convention`: (1) revision header on all living documents (format specified); (2) ADRs as stable reference points vs. living documents; (3) PR Cross-references section — required field on all PRs that update a living document. Revision headers added to six living documents: `north-star.md`, `information-hierarchy.md`, `user-journeys.md`, `simulation-framework.md`, `CLAUDE.md`, `docs/process/agents.md`. PR template updated. CONTRIBUTING.md updated. | 2026-05-23 |
| STD-REVIEW-005 complete — M9 exit standards gap inventory (PR #510, closes #439) | Eight gaps total. Carried from STD-REVIEW-004: (1) no canonical unit registry (#252), (2) no field-level data certification (#252), (3) WGI territorial convention (no Issue), (4) [SIM-INTEGRITY] logging formal section (promote to Immediate for M10). New M9 gaps: M9-1 synthetic data tier floor (#508 implementation gate), M9-2 `step_event_label` mandatory fixture field (#395), M9-3 per-indicator badge disclosure (no Issue), M9-4 document referencing convention (RESOLVED this PR). Three M10 kickoff gates: (1) [SIM-INTEGRITY] logging section before first M10 engine PR; (2) `step_event_label` in DATA_STANDARDS.md before first M10 backtesting fixture; (3) synthetic data tier floor in DATA_STANDARDS.md before Quantity schema extension Alembic migration. Schema drift check: no drift (M9 docs-only). | 2026-05-23 |
| SCAN-023 filed — M9 milestone-exit compliance scan (PR #510) | Documentation-only milestone — no simulation code, no Python/TypeScript/Alembic files, no compliance scan tool applicable. All ADRs CURRENT at M9 exit: ADR-001/002 renewed for M10; ADR-007 accepted 2026-05-23; ADR-008/010 accepted 2026-05-22; ADR-003/004/005/006 reviewed and CURRENT. 809 unit tests unchanged from M8 (no code shipped in M9). Three M10 kickoff gates documented in STD-REVIEW-005. | 2026-05-23 |
| ADR-001 and ADR-002 license renewals — Valid Until M10 (PR #510) | ADR-001 (Simulation Core Data Model): `Valid Until` extended to Milestone 10. M9 exit review entry added: no renewal triggers fired — M9 was documentation-only. M8 exit review entry added (SCAN-022, previously missing). ADR-002 (Input Orchestration Layer): same pattern. M9 review note: ADR-007 adds Quantity fields — this is NOT an ADR-002 trigger (ControlInput taxonomy unchanged). | 2026-05-23 |
| All M9 horizon:immediate issues closed or formally deferred (Issue #213 comment) | Formal deferral comment posted on Issue #213 covering all remaining open M9 issues. Issues closed this session: #507 (ADR-005 Amendment 4), #508 (ADR-007 accepted), #251 (architecture backlog), #378 (architecture backlog process), #439 (STD-REVIEW-005), #398 (document referencing convention). M9 is now in human-gate phase. | 2026-05-23 |
| Issue #493 closed — M9 IR review + M8 DEMO triage complete (PR #501) | IR review at `docs/demo/m9/reviews/2026-05-23-v0.9-instrument-cluster-ir.md`. Six findings (IR-001–IR-006) filed as #495–#500 for M10. Two root causes: (A) data layer not wired to Zone 1B/1C — mda_alerts always [], PMM always null; (B) session state and entry-state architecture not implemented — landing screen is choropleth, step annotations absent for user-created scenarios. Root Cause B from M8 (drawer legibility) fully resolved by M9 architecture. M8 DEMO triage: #344 closed (text legibility resolved); #342/#343/#346/#347/#349 transformed + re-milestoned to M10; #345/#348/#350 persist to M10. Six M10 issues: #495 (IR-001 Critical — mda_alerts wiring), #496 (IR-002 — PMM endpoint), #497 (IR-003 — persistent scenario state/demonstrative entry), #498 (IR-004 — default step labels from start year), #499 (IR-005 — governance "(in validation)" inline), #500 (IR-006 — loading state). | 2026-05-23 |
| Issue #463 fully closed — Zone 1 cluster live in App.tsx + Greece Playwright suite (PRs #489–#491) | PR #489 closed the four remaining QA acceptance test gaps (#459): ModeIndicator component + 13 Vitest tests; AC-006 RTL atomicity test (act() boundary, Vitest cleanup fix); AC-013 "(exp)" confidence badge Playwright guard; US-026 mode-indicator RTL act() test. PR #490 wired InstrumentCluster into App.tsx via ScenarioInstrumentCluster: trajectory fetch + parse (array→Record, Decimal string→number, boundary_proximity→normalized_absolute); data-testid duplication fixed in InstrumentCluster wrapper divs. PR #491 completed Issue #463 PR 2: removed test.skip() from AC-001/AC-002; added selectScenario() helper; created greece-integration.spec.ts (5 tests: smoke, mode indicator "Replay", data-current-step tracking, governance null AC-015, per-step cluster consistency + Mode 2 no-op guard). | 2026-05-23 |
| Zone 1A/1B/1C/1D instrument cluster complete (PRs #484–#487) | All four co-primary instruments shipped: `TrajectoryView.tsx` (Zone 1A — ComposedChart, 4 active + 4 ghost Lines, divergence fills, CVD-safe framework colors, Mode 1 custom tick, (exp) badge, Path A dashed curves); `MDAAlertPanelZone1B.tsx` (Zone 1B — TERMINAL→CRITICAL→WARNING sort, compact 3-line at <320px / full-density at ≥320px, mode-specific tense, negotiation labels, causal attribution Mode 3 only); `PMMWidgetZone1C.tsx` (Zone 1C — mode-specific label, direction arrow, pending state at 40% opacity); `FourFrameworkZone1D.tsx` (Zone 1D — 4 framework scores derived from Zustand atom, null→`score-value--null`+"—", numeric→`score-value--numeric`). Store extended: `Zone1BAlert`, `mda_alerts`, `pmm_value`, `pmm_direction`, `setPmmState`. 104/104 Vitest tests passing. All Playwright E2E guards use isVisible no-op pattern pending App.tsx integration (#463). | 2026-05-23 |
| TrajectoryView Zone 1A merged (PR #484, closes #460) | `TrajectoryView.tsx` (ComposedChart: 4 active Lines, 4 ghost Lines, Area divergence fills, ecological WARNING ReferenceLine, ADR-007-gated band infrastructure, Mode 1 custom tick, (exp) badge, Path A single-entity dashed curves); `InstrumentCluster.tsx` (two-column layout 480/240/280px at 1024×768, 580/400/280px at 1280×800, 280px control plane always rendered); `scenarioStepStore.ts` (Zustand atom, single-set() atomicity invariant); `frameworkColors.ts` (UX Designer ruling — teal #1A8FA0 replaces green #3A7A4B after CVD deuteranopia collision identified); DD-012–DD-015 added; FA brief CVD Validation Result recorded; MV-001 closed; 31/31 Vitest tests passing; AC-003/004/005 Playwright guards added (element not in App.tsx yet); MV-002 hardware validation pending before M9 exits. | 2026-05-23 |
| Known Issues registry established — distinct category from near-misses (PR #482) | External infrastructure limitations (GitHub Actions, third-party APIs) cannot be fixed by process redesign — filing them as near-misses produces improvement recommendations against things we cannot change. Known Issues live in `docs/process/known-issues-registry.md`; near-misses in `docs/process/near-miss-registry.md`. Categorisation rule: if the fix requires changing our own code/process → near-miss; if the fix requires waiting for an upstream vendor → Known Issue. KI-001 filed: GitHub Actions `pull_request` event silently fails to fire (workaround: empty retriggering commit). CLAUDE.md, agents.md, agent-raci.md all updated. | 2026-05-23 |
| Instrument cluster spec retrofit — blanket skip removed, Type 1/Type 2 split completed (PR #480, closes #473) | `instrument-cluster.spec.ts` deleted; `instrument-cluster-integration.spec.ts` created with only AC-001 and AC-002 (Type 2 integration-level, individual `test.skip()` per test — no file-level blanket suppression). Component-level ACs (AC-003–AC-014) distributed to implementing issues: AC-003–013 → #460 (TrajectoryView) with full test code; AC-014 + component tests → #462 (PMM + Four-Framework); component tests → #461 (MDA Alert Panel). CI green: no `test.skip(true, ...)` in any instrument cluster spec file. | 2026-05-23 |
| NM-018 filed — hammer-nail: technical panel produced engineering solutions to a process problem (PR #479) | Three technical agents (Architect, Frontend Architect, QA Lead) consulted on skip governance; all three produced engineering solutions (CI guard, skip registry, DOM-presence fixture) to what was a process problem (missing AC categorization rule). PO Agent and UX Designer Agent immediately identified the correct root cause. Root cause of the near-miss: no rule existed requiring PM Agent to evaluate whether panel composition matched the problem's root cause domain, not just its surface presentation. Standing fix: panel composition principle added to PM Agent pre-EL consultation protocol in `docs/process/agents.md §PM Agent — Pre-EL Consultation` between steps 2 and 3. | 2026-05-23 |
| PO Agent standing responsibilities — dual consumer + sequence gate (PR #477, closes #470) | Two non-negotiable standing responsibilities added to PO working agreement: (1) Stories serve QA Lead and Frontend Architect equally — a story too vague for QA to write a meaningful test, or too abstracted for FA to make the right tradeoffs, is a weak story; (2) Stories → tests → implementation sequence gate — the PO owns enforcement; a story session is not complete until the stories doc is merged, a QA test authorship issue is filed blocking implementation, and the issue hierarchy is established. RACI rows 2 and 3 updated: PO consultation trigger now explicitly names QA/FA story consumers. | 2026-05-23 |
| Type 1/Type 2 AC categorization rule — CODING_STANDARDS + QA Lead + PO working agreements (PR #476, closes #474) | Before any QA E2E spec is authored against a multi-component feature, ACs must be categorized: Type 1 (component-level — testable when one component ships alone; lives in implementation task PR scope) vs Type 2 (integration-level — testable only when all named components coexist; lives in dedicated `<feature>-integration.spec.ts`). `test.skip(true, ...)` at file scope is a process violation for any spec containing Type 1 ACs. QA Lead working agreement (new) makes categorization the first standing commitment. PO pre-authorship check added. Documented in `docs/CODING_STANDARDS.md §E2E Pre-implementation Test Categorization`. | 2026-05-23 |
| NM-017 filed — story–test–implementation decomposition mismatch (PR #475, anticipatory) | 16 instrument cluster ACs were suppressed by a blanket `test.skip(true, ...)` because zone-level and component-level ACs were bundled in a single spec file while implementation was decomposed into three Task Issues (#460/461/462). Engineering Lead identified the structural gap through governance anxiety about skip management — before any component shipped. Root cause: no AC categorization rule existed. Severity: High (CI blind spot across primary viewport ACs). Response: retrofit Issue #473 + process change Issue #474 (now complete via PR #476). | 2026-05-23 |
| NM-016 + pre-push lint gate added to CLAUDE.md (PR #472, closes #471) | Two parallel agents (Issues #458 and #459) pushed PRs without running `ruff check .` locally. Both failed CI on I001/E501 — trivially preventable in two seconds locally. Root cause: agent prompts specified `pytest` but not `ruff`. Pre-push lint gate added to CLAUDE.md constitution: `cd backend && ruff check . && mypy app/` required before any push touching Python files. Local ruff==0.7.2 is identical to CI-pinned version — no environment gap. NM-016 filed. | 2026-05-23 |
| Backend trajectory endpoint merged (PR #468, closes #458) | `GET /scenarios/{scenario_id}/trajectory` FastAPI endpoint live on main. Key contracts: `SINGLE_ENTITY_REFERENCE_RANGES` dict (gdp_growth, reserve_coverage_months, unemployment_rate, net_enrollment_secondary — health_expenditure excluded as non-monotonic); `normalized_absolute_strategy` function; ecological MDA floor (WARNING at 1.0) built in application code (no M9 DB table); `mda_floors` at response root; `step_significance` from `step_metadata` JSONB; Pydantic v2 schemas (`TrajectoryResponse`, `TrajectoryStep`, `TrajectoryFrameworkPoint`, `MDAFloorRecord`). 13 unit tests in `test_trajectory_endpoint.py`. | 2026-05-23 |
| QA pre-implementation test authorship merged (PR #469, closes #459) | `frontend/tests/e2e/instrument-cluster.spec.ts` — 16 ACs (AC-001 through AC-014) as Playwright E2E gates. All tests wrapped with `test.skip(true, ...)` pending #460/461/462 (this skip is the subject of retrofit Issue #473). `page.emulate()` Puppeteer bug fixed → CDP session (`Emulation.setCPUThrottlingRate`). `frontend/src/components/__tests__/TrajectoryView.test.ts` — Vitest unit tests for AC-010/013/015. `backend/tests/fixtures/test_greece_fixture_step_metadata.py` — 13 pytest CI gate tests for AC-012 (step_event_label ≤8 words AND ≤32 chars). `frontend/tests/manual-validation/mv-gates.md` — MV-001/002/003 procedures. | 2026-05-23 |
| Playwright test skip governance — three-agent consultation (anticipatory) | Engineering Lead asked how to prevent `test.skip()` from being abused or forgotten. Architect (skip registry — hermetic), Frontend Architect (DOM-presence fixture — self-healing), and QA Lead (test.fixme() + milestone exit gate) each assessed independently. Unanimous finding: skip must be visible and self-expiring. Key divergence: registry (auditable) vs DOM-presence (no maintenance). Recommendation: DOM-presence as runtime control + test.fixme() for visibility + Type 1/Type 2 discipline as root fix. Root fix (Type 1/Type 2 rule) eliminates the problem structurally — per NM-017, the correct fix is decomposition discipline, not skip governance tooling. | 2026-05-23 |
| PM Agent pre-EL consultation — standing automatic capability (PR #466, closes #464) | Pre-EL consultation added to PM Agent working agreement as automatic standing responsibility. Three trigger conditions: [EL-DECISION] tag in any document; pending entry in SESSION_STATE.md §Pending EL Decisions; any agent raising an EL-authority question. Four-step process: identify → activate independently → synthesize → surface recommendation. RACI framing: EL holds A; PM Agent holds R for the consultation — cold questions reaching EL without prior consultation are a PM Agent failure. Disagreement handling: PM Agent names divergence and surfaces all positions; does not resolve. | 2026-05-23 |
| Issue hierarchy rule encoded permanently (PR #456); M9 trajectory endpoint epic filed (#457–#463) | Binary three-level issue hierarchy (Epic → Feature → Task) added to PM Agent working agreement in agents.md and referenced in CLAUDE.md. Spawning rule: children created only when >1 agent OR >1 PR required — agent-count-based, not complexity-based. M9 instrument cluster epic #457 filed with six child Feature Issues: #458 (backend trajectory endpoint), #459 (QA test authorship — pre-implementation gate), #460 (TrajectoryView Zone 1A), #461 (MDA Alert Panel Zone 1B), #462 (PMM + Four-Framework Zone 1C/1D), #463 (Greece integration Playwright suite). #459 explicitly blocks #460/461/462. #463 spawns Level 3 Task Issues when prerequisites complete. Pre-EL consultation standing capability filed as #464 — PM Agent auto-coordinates before any EL decision reaches EL. | 2026-05-23 |
| UX-RULING-1/2/3 resolved — QA gate fully unblocked (PR #454) | UX Designer Agent resolved all three open Playwright assertion placeholders in the M9 instrument cluster user stories. RULING-1 (US-016): alert tense markers per mode — Mode 1 `"crossed"`, Mode 2 `"is projected to cross"`, Mode 3 ` — ` separator format; advisory language exclusions. RULING-2 (US-022): null composite score → CSS class `score-value--null` (opacity ≤ 60%); numeric/zero → `score-value--numeric`. RULING-3 (US-026): mode indicator labels — `"Replay"` / `"Simulation"` / `"Active Control"`. All 29 stories now fully testable. QA gate UNBLOCKED. | 2026-05-23 |
| US-GAP-001 — Mode 1 comparable-case comparison deferred to M10 | Pre-EL consultation: UX Design Thinking Agent, PO Agent, Architect Agent — unanimous M10 verdict. Key finding: the gap was narrower than stated. ADR-010 Decision 11 and FA brief §UD-R2 already specify the rendering layer for multi-case Mode 1 (step alignment, stacked entity dates). The missing piece is the Zone 2 entry point for selecting the second fixture — a COMPARE_VIEW architecture question, not an instrument cluster question. Mode 1 block added to `information-hierarchy.md §COMPARE_VIEW` with decision space documented. User stories file updated: US-GAP-001 converted from pending to resolved; M9 service level for Persona 3 stated explicitly (orientation sufficient; comparison M10). Issue #451 filed with full M10 deliverable spec. PR #452. | 2026-05-23 |
| M9 instrument cluster user stories — 29 stories authored (Issue #441, PR #449) | PO Agent: EXECUTE. Two consumers: QA Lead (writes acceptance tests from stories before implementation) and Frontend Architect (implements to stories as user-value specification). 29 stories across 9 groups (US-001–US-029): Zone 1 Completeness, Trajectory View, MDA Alert Panel, PMM Widget, Four-Framework Current Position, Atomicity, Persistent Header, Control Plane Reserved Zone, Performance. All stories include Given/When/Then acceptance criteria tagged by test method [Playwright], [Vitest], [RTL], [pytest], [Manual]. Three [UX-RULING] placeholders (US-016, US-022, US-026) await UX Designer observable-string rulings. One [EL-DECISION] gap finding (US-GAP-001): Andreas Mode 1 comparative-case comparison requires a surface not in M9 spec — EL to decide M9 or M10. File: `docs/ux/user-stories-instrument-cluster-m9.md`. | 2026-05-23 |
| NM-014 systemic root cause expanded — micro-management cycle named | The contributing factor section was accurate but incomplete. Expanded with a full nine-step cycle analysis: mistakes → more prescription → reduced agent reasoning → more mistakes → more prescription. Named the analogy to the tech lead failure mode. Stated the correct structural response: issues carry prescription, standing documents carry rules, agents write their plan before executing, prompts are outcome-oriented. Prescriptive prompting weight upgraded from "under investigation" to "confirmed as significant — both symptom and perpetuating mechanism." PR #447. | 2026-05-23 |
| PR merge gate rule added to CLAUDE.md — mandatory pause + SESSION_STATE.md auto-merge exception | After opening any PR, Claude Code must stop all git operations, report the PR URL, and wait for user merge confirmation before pulling main or starting the next task. Exception: SESSION_STATE.md-only PRs are pre-authorized for auto-merge once the `changes` CI status check passes. Rationale: eliminates the concurrent-terminal race condition (two processes operating git on the same local repo without coordination) while preserving the human as merge coordinator and CI gate — especially important in parallel-session scenarios. PR #445. | 2026-05-23 |
| Branch protection remediation — `changes` and `compliance-scan` added to required status checks | Root-cause analysis of the checkout@v6 CI failure revealed that `changes` (the path-filter gate job) and `compliance-scan` were absent from required status checks. Only `lint`, `test-backend`, and `playwright-e2e` were required — all downstream of `changes`. When `changes` fails, downstream jobs are skipped-due-to-dependency-failure, potentially not blocking merges. Applied immediately via GitHub API (no PR required). Required checks now: `changes`, `test-backend`, `lint`, `playwright-e2e`, `compliance-scan`. NM-015 filed. | 2026-05-23 |
| NM-014 + NM-015 filed — near-miss registry now 15 entries | NM-014: file edit reported as complete without being committed to a branch (agents.md in PO Agent EXECUTE). Process improvement: personal commit gate — a change is not reportable as done until it is on a branch and committed. NM-015: CI gate job (`changes`) was not a required status check; compliance-scan also absent. Process improvement: required checks must include the root gate job, not just its downstream dependents. Milestone exit checklist checkpoint added. PR #443. | 2026-05-23 |
| CI fix — actions/checkout@v6 → @v4 | The April 19 checkout@v6 upgrade was intentional (Node.js 20 deprecation, v6 released January 2026) and appears to have regressed recently. All 7 occurrences across ci.yml and milestone-automation.yml updated to @v4 (current stable). This unblocked PR #443. PR #444. | 2026-05-23 |
| Near-miss registry created — NM-001 through NM-013 | `docs/process/near-miss-registry.md` created using Aviation SMS epistemology: near-misses treated with same rigor as incidents because they reveal hazards without the cost of failure. 7 reactive entries (NM-001–NM-007) + 6 anticipatory entries (NM-008–NM-013). Recurring pattern identified: agent acting in domain belonging to another agent without required consultation (NM-005, NM-006, NM-007). Second pattern: six entries are anticipatory — Engineering Lead sensing structural gaps before failure. Registry maintenance section defines template, severity levels, and the key question: "caught by process or by a person?" PR #435 + PR #436. | 2026-05-23 |
| PR board cleared — all stale PRs confirmed merged | 14 PRs that appeared open in SESSION_STATE were confirmed merged via GitHub. Open PRs table cleared. Board is clean. | 2026-05-23 |
| File authority rule + ownership table — Issue #431 closed | CLAUDE.md §Architectural Principles now includes the file authority rule: agents must verify they hold R before writing any file; if another agent holds R, produce a draft and request owner review before committing. `docs/process/agent-raci.md §File Ownership` added: 24-row lookup table (file/directory, Owner R, Required Consultant C) covering all major files; §Near-Miss section documents PR #429 incident (two substantive errors caught by retroactive DA+Ar review); §What 'C' Means in Practice defines the correct draft → C review → incorporate → commit sequence. HORIZON mode in `docs/process/agents.md` expanded from one-liner to five numbered sweep steps; step 5 = FILE AUTHORITY AUDIT. PR #432 (CLAUDE.md rule) + PR #433 (table + HORIZON step). | 2026-05-23 |
| Issue #428 prerequisites complete — trajectory endpoint unblocked | (1) ADR-010 D6 amendment: M9 deferral of MDA floors; ecological WARNING at 1.0; M10-B schema. (2) CM reference range consultation: gdp_growth [-0.10, 0.06]; reserve_coverage_months [0.0, 12.0]; unemployment_rate [0.02, 0.30] inverted; net_enrollment_secondary [0.40, 1.00]; health_expenditure excluded; Tier 3 floor. (3) ADR-010 D2 amendment: scoring_basis three-value enum (percentile_rank / normalized_absolute / boundary_proximity); single-entity contract; step_metadata JSONB. DA+Ar review: scoring_basis ecological value corrected to "boundary_proximity" (was "percentile_rank" — semantically incorrect); db_reads M10 comment fix. PR #429 merged. Issue #428 closed. | 2026-05-23 |
| EL Decisions A/B/C recorded — trajectory endpoint implementation unblocked | Decision A: MDA floor overlays deferred to M10; ecological WARNING at 1.0 authorized for M9; CM consultation on reference ranges authorized; M10-B schema confirmed. Decision B: Path A selected — normalized absolute composite for single-entity trajectory; four curves; Tier 3 confidence floor; CM reference range consultation is the hard next gate. Decision C: step_metadata JSONB option (a) confirmed. All recorded on Issue #366. Issue #193 updated. PR #427. | 2026-05-22 |
| Six-agent parallel consultation — DA-F2/F4/F5 pre-implementation record | CM, UX Design Thinking, UX Designer, Data Architect, QA Lead, Frontend Architect activated simultaneously. Key rulings: (1) CM: single-entity normalized absolute composite is methodologically sound (Tier 3 floor); Path A requires pre-declared reference ranges before endpoint can compute. (2) CM: composite-score MDA floors cannot be defined without backtesting — defer to M10; ecological WARNING at 1.0 is only M9 exception. (3) UT: four-curve Mode 1 Greece is M9 exit requirement; DA-F4 is demo scope decision. (4) UD: Path A rulings (strokeDasharray="8 3", legend labels, tooltip) and Path B rulings (40px amber strip, approved text) recorded. (5) DA: step_metadata JSONB confirmed valid; scoring_basis field for Path A; single_entity_advisory at response root for Path B; mda_floors structural error in stub identified. (6) QA: AC-009 corrected (3 shock ReferenceLines, not 6+); AC-015 broadened to all four Lines. (7) FA: atom unchanged for all paths; connectNulls={false} confirmed on all 8 Lines; single_entity_advisory must not be atom field. Three EL decisions still pending. PR #426. | 2026-05-22 |
| Architect Agent review of Data Architect findings — three EL decisions required | Data Architect found 5 schema gaps (DA-F1–F5). Architect dispositions: DA-F1 stub adequate; DA-F2 defer MDA floor overlays to M10 + CM consultation; DA-F3 correct as-is; DA-F4 CRITICAL (Greece Mode 1 blocked — single-entity null; CM + ADR-010 amendment required); DA-F5 step_metadata JSONB approach confirmed. Arch-F1: "STANDARD" → "ROUTINE" correction applied. Three EL decisions pending. PR #425. | 2026-05-22 |
| UX Designer sign-off — conditional on CVD | 4/5 items confirmed (layout, stacking, compact row, badge). Colors pending MV-001. PR #423. | 2026-05-22 |
| M9 FA brief — three-agent review complete | All 10 findings INCORPORATE. Compact alert row (UD-F1), badge 11px (UD-F2), act() boundary (QA-F1), MV gates added. PR #422. | 2026-05-22 |
| M9 FA brief authored — instrument cluster | Frontend Architect Agent: EXECUTE. All 11 deferred brief items (FA-C1–FA-C5 from ADR-008; FA-R1, FA-R2, FA-R4/UD-R1, FA-R5, UD-R2, UD-R3 from ADR-010) resolved with named acceptance criteria. Key decisions: Zustand atom for Zone 1 atomicity (DD-012); merged-key `<Area>` for divergence fill (DD-013); 32-char step annotation constraint (DD-014); 280px control plane confirmed (DD-015). Layout constants: 480px trajectory / 240px co-primary / 280px control plane at 1024×768; 580/400/280 at 1280×800. CVD validation procedure specified; result pending UX Designer sign-off. Brief at `docs/frontend/fa-brief-m9-instrument-cluster.md`. | 2026-05-22 |
| ADR-010 drafted, panel-reviewed, and accepted | Architect Agent: EXECUTE. 10 decisions (Recharts SVG, GET /scenarios/{id}/trajectory endpoint, shared state atom, governance null rendering, composite-score-level MDA floors, Mode 1 step axis annotation, Mode 3 live A/B ghost curves and divergence fill, policy/shock markers, confidence tier visual, ADR-007-gated band infrastructure). 11 findings (4 INCORPORATE applied, 5 BRIEF, 1 LOG, 1 combined). EL approved all 4 INCORPORATE items with rationale recorded in `docs/adr/reviews/ADR-010-panel-review.md`. ADR-010 status: Accepted. M9 FA brief is unblocked. | 2026-05-22 |
| ADR-008 accepted — PR open | All 6 INCORPORATE items applied to ADR-008. EL decision recorded in `docs/adr/reviews/ADR-008-panel-review.md`: all 6 approved; FA-C3 ruling = Option A (stacked forms, ~280px control plane zone). ADR-008 status: Accepted. ARCH-002 in backlog: ACCEPTED. Issue #397 closed. Five FA brief items (FA-C1–FA-C5) deferred to M9 FA brief — none reverse an ADR decision. | 2026-05-22 |
| ADR-008 panel review artifact created — PR #417 | Full three-agent panel review completed and captured as `docs/adr/reviews/ADR-008-panel-review.md` (first instance of new artifact type). 12 findings registered: 4 from UX Designer (UX-F1–UX-F4), 5 from Frontend Architect (FA-C1–FA-C5), 3 from Chief Methodologist (CM-1–CM-3). Architect dispositions: 6 INCORPORATE, 3 BRIEF, 1 JOINT EL+UX RULING → BRIEF, 1 LOG, 1 BRIEF+Open Risks. FA concurrence recorded. EL decision record left blank for EL to complete. CLAUDE.md §Canonical Artifact Locations and CODING_STANDARDS.md §ADR Requirements updated to standardize panel review process for all future ADRs. | 2026-05-22 |
| ADR-008 drafted — PR #416 | Architect Agent: EXECUTE activated. Read all required documents (backlog, agent-raci, Issue #364, first-principles-depth, north-star, information-hierarchy, user-journeys). 17 decisions covering viewport inversion, zone assignments, all three modes, blue/orange cross-layer visual system, confidence tier differentiation, Mode 1 step annotation (fixture CI gate), live A/B comparison (automatic), control plane reserved zone. Status: Proposed — pending four-member panel review (UX Designer, Frontend Architect, Chief Methodologist, Engineering Lead). | 2026-05-22 |
| RACI-grounded ADR panel composition rule — added to #405 scope | ADR-008 panel omitted Frontend Architect despite FA being C on all architectural decisions per agent-raci.md row 1. Root cause: panel copied from M8 critique panel (conceptual framing question) rather than derived from the RACI. Rule added to Issue #405 scope: before naming any ADR panel, consult agent-raci.md; any R or C agent must be included or exclusion documented. Implementing agent is always required. Minimum panels by ADR type: frontend ADR → Frontend Architect; engine ADR → Chief Engineer; data ADR → Chief Methodologist; UX ADR → UX Designer. ADR-008 (Issue #397) is the first application of the corrected rule — FA already added to that panel this session. | 2026-05-22 |
| M12 renamed — "Active Control and External Sector" | Previous GitHub title "Analyst Tooling and External Sector" undersold Mode 3; roadmap doc used a third variant "Transformation and External Sector". Renamed to "Active Control and External Sector" — names the two user-facing deliverables (Mode 3 and the external sector module) without naming the matrix engine migration as the lead. GitHub milestone description field also confirmed stale. Milestone registry gap filed as #412 (M9, near-term). | 2026-05-22 |
| Board cleanup — re-milestone SA-*/backtesting family M9→M10; #394 M9→M12; 6 horizon labels added | 10 issues re-milestoned M9→M10 (#91, #103, #116, #118, #119, #122, #123, #160, #173, #393) — SA-*/backtesting standards family moves with #43 (confidence_tier split) as an engine integrity prerequisite. #394 (multi-scenario comparison >2) re-milestoned M9→M12 — roadmap explicitly places this in M12 as the TC-3 Kenya budget planning enabler. horizon:near-term added to #271, #272, #273, #274, #275; horizon:long-term added to #278. Post-cleanup: 0 open issues without milestone, 0 without horizon label. | 2026-05-22 |
| WorldSim roadmap document created — docs/roadmap/worldsim-roadmap.md | M9–M13 arc established through demo-anchored working-backwards analysis. Demo 3 at M10 (WorldSim works: all four axes, second country, instrument cluster). Demo 4 at M12 (Hormuz closure on a standard laptop — democratization mission made concrete). Long-term resolution spectrum (entity template library), two-path infrastructure model. CLAUDE.md §Milestone Roadmap compressed to two-paragraph pointer. MILESTONE_RUNBOOK.md §Roadmap Update added as mandatory exit ceremony step. milestone-roadmap-m6-m8.md archived with header note. ADR numbering registry established: ADR-007=synthetic data, ADR-008=UX architecture, ADR-009=engine computation, ADR-010=trajectory view. Architecture Backlog at docs/architecture/backlog.md prevents informal ADR number assignment. | 2026-05-22 |
| Issue #365 closed — UX document updates PR #399 | north-star.md: §1 replaced with §Primary Cognitive Tasks by Mode (three per-mode formulations; M4-era 'threshold alarm detection' superseded); §2 extended to three modes; personas.md reference added. information-hierarchy.md: Governing Principle updated to per-mode framing; Zone 1 restructured — entity selector as persistent header, trajectory view as 1A primary, MDA alert panel 1B, PMM 1C, four-framework current position 1D; radar chart moved to Zone 2 (2A); EntityDetailDrawer demoted to detail/methodology surface; COMPARE_VIEW replaced with three-mode conditional (single-entity Mode 2: divergence timeline; multi-entity Mode 2: DeltaChoropleth; Mode 3: automatic live A/B); DeltaChoropleth deprecated for single-entity and Mode 3; Control Plane Reserved Zone section added; M9 hierarchy decisions table (8 decisions). user-journeys.md: Journey A Step 3 separated into advance (3a) and inspect (3b); Journey B Step 5 reframed as Mode 3 control input; Journey C (Mode 3 active control — Eleni February 2012) and Journey D (demonstrative entry state — Aicha Mbaye) added; dependency map extended to 15 rows across all four journeys and three modes. Issues #366 and #368 unblocked. | 2026-05-21 |
| EL Decisions 1/2/3 recorded — Issue #364 closed; Issue #365 unblocked; four gap issues filed | Decision 1 (north-star): per-mode formulation adopted — Mode 1: trajectory reconstruction AND historical pattern recognition; Mode 2: threshold-safe path construction; Mode 3: real-time steering within human cost constraints. All 13 marquee cases validated. Two M11 gaps correctly surfaced (Argentina/Ukraine political economy constraint); two engineering gaps filed (#393 Mode 1→2 transition, #394 multi-scenario comparison). Decision 2 (viewport): instrument cluster as primary viewport adopted; EntityDetailDrawer demoted to detail/methodology; entity selector as persistent header element. Decision 3 (comparison): conditional switch extended to Mode 3 — automatic live A/B with no invoke required; DeltaChoropleth deprecated for single-entity and Mode 3. Four gap issues: #392 (M11 political economy), #393 (Mode 1→2 transition), #394 (multi-scenario), #395 (step_event_label mandatory). Issue #364 closed. Issue #365 (UX document updates) now unblocked. | 2026-05-21 |
| Issue #363 implemented — UX first-principles depth (PR #390 merged) | docs/ux/design-thinking/worldsim-ux-architecture-first-principles-depth.md. Six gaps closed. Gap 1A: Mode 3 walkthrough for Eleni (February 2012), 10-component Frontend Architect requirement table. Gap 1B: mandatory Mode 1 step axis annotation — three fixture fields (effective_from, step_event_label, step_significance); missing step_event_label on SIGNIFICANT steps is an incomplete fixture. Gap 2: three analogy breaks qualified (atomic simultaneous updates; entity selector always visible; Tier 4 instrument visual differentiation). Gap 3: blue/orange cross-layer visual system for policy inputs vs. exogenous shocks; causal attribution in alert text is the negotiating instrument. Gap 4: Mode 3 live A/B comparison is automatic — any control input creates the split; ghost baseline at 50% opacity with divergence fill region. Gap 5: mode transition design — persistent vs. mode-specific instruments; single modal confirmation only for unsaved state loss. Revised six governing premises: Premise 3 mandated with Mode 1 step annotation (most consequential); Premise 4 extended for multiple Mode 1 cognitive tasks; Premise 6 new (methodology as Zone 2 mandatory). Issue #364 unblocked. | 2026-05-21 |
| Issue #387 implemented — persona-grounded UX review (PR #388) | docs/ux/design-thinking/persona-grounded-ux-review.md. Three activations: UX Design Thinking Agent (Q1–Q3), Development Economist (Eleni February 2012 walkthrough), Political Economist (Andreas Preparatory state). Key finding: Case B holds for all five personas architecturally; four specification extensions required. Most consequential: step axis annotation (calendar date + event label) is mandatory in Mode 1 — without it, Premises 3 optimizes for Personas 1 and 2 while Personas 3 and 5 cannot orient. Issue #363 must accompany Persona 2 Gap 1 walkthrough with parallel Mode 1 specification for Persona 3 pattern recognition. | 2026-05-21 |
| Issue #362 implemented — user persona document | docs/ux/personas.md (1352 lines). Five personas (8 dimensions each): Programme Analyst, Finance Ministry Negotiator, Political Advisor, Academic Researcher, Institutional Decision-Maker. Six entry states with 60-sec opening screen requirements and failure conditions. Five primary marquee cases (European sovereign debt history) with testable exit criteria. Five secondary marquee cases (Argentina, Egypt, Sri Lanka, Ukraine, Zambia) with structural gap verdicts. Three tertiary use cases as ingredient specifications (Canadian steel tariffs, Hormuz closure, Kenya budget). Product scope statement. Synthetic data framework integrated for Cases E/TC-2/TC-3. Platform principle applied throughout. EL review required before canonical. PR #385. | 2026-05-20 |
| Issue #360 implemented — 15 agent working agreements | docs/process/agents.md: 15 working agreements appended (one per agent) in each agent's own voice. Five sections: understanding of the mission, unique contribution, observable behavioral commitments, where the agent asks for help, where it offers help. PR #384. | 2026-05-20 |
| Founding document committed | docs/vision/worldsim-founding-document.md created from April-May 2026 founding conversations (six parts: The Problem, The Analogy, The Principles, The Architecture, The Vision, Honest Limitations). CLAUDE.md §Founding Document reference added. PR #383. | 2026-05-20 |
| Architect Agent consultation — simulation graph mental model | EL's BST mental model is approximately correct for the administrative hierarchy (parent_id) but the propagation medium is the relationship graph, not the hierarchy. Two-graph architecture: Graph 1 (parent_id = identity/scope); Graph 2 (relationships list with relationship_type = propagation medium). Events propagate along typed edges; no rollup. Each entity computes from events it receives. | 2026-05-20 |
| Issue #370 (M8 formal close issue) — still open | Work is done (v0.8.0 released, retrospective complete) but the issue itself was not explicitly closed this session. Needs explicit close. | 2026-05-20 |
| M8 formal close complete | All six exit gates satisfied; v0.8.0 tagged and released; Issue #209 closed; CHANGELOG updated; demo recording attached to GitHub release | 2026-05-19 |
| Issue #361 Chief Methodologist consultation — synthetic data framework | docs/architecture/synthetic-data-consultation.md (41.5k chars, 560 lines). Five questions answered. Method hierarchy: Bayesian > MICE > Bootstrap > structural extrapolation > structural absence. Three-condition meaninglessness threshold. MDA tier table (full/advisory/exploratory/none). Anomaly detection requires TSC sign-off, opt-in, Mode 3 excluded, governance indicators excluded. ADR-007 outline produced. PR #373. | 2026-05-19 |
| Issue #359 implemented — CLAUDE.md structural refactor | docs/architecture/simulation-framework.md created (7.7k chars); CLAUDE.md reduced to 28,375 chars; role-based mandatory reading table added; three new principle sections (Platform Principle, Synthetic Data, UX Architectural Commitments); three-mode architecture referenced. PR #372. | 2026-05-19 |
| Design foundation sequence filed — 12 issues #359–#370 | PM Agent: EXECUTE — all 12 design foundation issues filed in dependency order. Issues #359–#363 are Immediate horizon; #364–#369 are Near-Term; #370 (M8 formal close) is Immediate and runs in parallel. | 2026-05-19 |
| UX first principles review completed — Case B verdict (PR #356) | docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md. Root finding: current UI inverts instrument/context relationship (choropleth primary, instruments in drawer). Mode 3 active control requires instruments always visible — current architecture fails this. Case B: rethink warranted before M9. Minimum rethink = three document changes + reserved control plane zone. Five M9 governing premises produced. Highest-priority action: update information-hierarchy.md governing principle. Decision 2 (timeline zone assignment) reframed as wrong question — defer and address as viewport architecture question. | 2026-05-18 |
| M8 UX panel synthesis completed (PR #356) | Three-agent panel (UX Designer, Development Economist, Chief Methodologist) independently reviewed Design Thinking Agent M8 critique (PR #355). Nine cross-cutting concerns; three EL decisions required; four premises revised/rejected; six premises unanimously confirmed; six additive findings. Highest-priority EL decision: north-star.md Primary Cognitive Task formulation — load-bearing for all hierarchy changes. | 2026-05-18 |
| UX Design Thinking Agent activated (PR #353/#354/#355) | Issue #353 filed; agent persona added to agents.md (PR #354); M8 critique produced at docs/ux/design-thinking/m8-interaction-model-critique.md (PR #355). Core diagnosis: WorldSim is a spatial comparison tool applied to a temporal problem; trajectory view should be Zone 1B primary instrument. | 2026-05-18 |
| M8 DEMO issues filed (PR #351) | All nine IR findings filed as GitHub issues #342–#350; assigned to M8 milestone. Root Cause B (#343 DEMO-002) is highest-priority: resolves DEMO-002/003/005/006 simultaneously. IR review updated with issue numbers. | 2026-05-18 |
| M8 stakeholder walkthrough created (PR #351) | docs/demo/m8/stakeholder-walkthrough.md — v0.8.0 presenter guide; six-step Greece narration; Honest Disclosures section; governance honest-null Q&A; root redirect updated. | 2026-05-18 |
| M8 IR Agent review completed (PR #340) | Nine findings (DEMO-001–009); 2 CRITICAL, 4 SIGNIFICANT, 3 MINOR. Root Cause B (drawer too narrow/dense) explains DEMO-002/003/005/006 simultaneously — highest-priority fix. docs/demo/m8/reviews/2026-05-18-v0.8.0-stakeholder-review.md. | 2026-05-18 |
| M8 demo polish fixes merged (PR #340) | gdp_growth choropleth error fixed (switch after step 1); drawer opened at step 4 for primary surplus narration; compare scenario extended to 6 steps with matching initial_attributes so DeltaChoropleth has step 6 data. | 2026-05-18 |
| M8 milestone board cleanup (this session) | Exit checklists #261–#264 and #213 were systematically off-by-one milestone; corrected. #286/#299/#301 re-milestoned to M9; #217/#95 re-milestoned to M10. #142 closed (stale). | 2026-05-18 |
| Demo preparation standard established (PR #334) | docs/process/demo-preparation-standard.md defines the biennial demo cadence. M6 artifacts archived to docs/demo/m6/. M8 screenshot brief (UX Agent) saved to docs/demo/m8/screenshot-brief.md. Thesis frame: Frame C, Step 5 (2014) — asymmetric radar. | 2026-05-18 |
| Python 3.12 Docker fix merged (PR #336, closes #332) | Rebuilt image on python:3.12-slim (confirmed 3.12.13 in container). Added `sys.version_info < (3, 12)` startup guard to app/main.py (# noqa: UP036 — ruff UP036 fires because target-version=py312, guard is operationally needed for stale images). Documented `docker compose build api` in CONTRIBUTING.md Step 3. | 2026-05-18 |
| EcologicalModule delta path bug fixed (PR #328) | For STOCK indicators, emit new absolute value (current + elasticity_delta) not the raw delta. The propagation engine replaces STOCK attributes — emitting the raw ~-0.08 elasticity value would overwrite the 388 ppm seed with a tiny negative, corrupting all subsequent proximity computations. | 2026-05-18 |
| gdp_direction_step5_positive deferred to Issue #221 | MacroeconomicModule has no endogenous recovery mechanism; fiscal consolidation accumulates without rebound channel. Engine produces -0.434 at step 5 vs historical +0.007. Moved from blocking CI gate to deferred_thresholds. | 2026-05-18 |
| co2_concentration_ppm seed (388 ppm, NOAA MLO 2010) required for demo scenario | Without seed, EcologicalModule stock path has no attribute at step 1 → null proximity. Added to build_greece_demo_scenario() initial_attributes. | 2026-05-18 |
| M8 frontend UX four issues implemented (PR #329 ✅) | #317 display name registry + #318 ecological note → Zone 3A + #320 PMM Zone 1C widget (null placeholder M8) + #319 radar 250ms animation + prefers-reduced-motion guard + null-axis animation guard; tsc clean, 10/10 tests | 2026-05-18 |
| Null governance axis merged (Issue #315, PR #323 ✅) | `RadarAxisDatum.composite_score: number \| null` live on main; null = dashed hollow dot; `GOVERNANCE_IN_VALIDATION_LABEL`/`TOOLTIP` constants + `computeFinalScore()` pure function; DD-011 sentinel; 10 Vitest tests | 2026-05-18 |
| M8 ecological backend merged (Issues #312–#314, PR #324 ✅) | Strategy dispatch, proximity indicators, migrations. land_use_pressure_index is pre-normalized (no division by 0.25). Ecological exempt from single-entity guard. | 2026-05-18 |
| Greece fixture 2015 merged (Issue #316, PR #321 ✅) | Steps 4–6 actuals, DIRECTION_ONLY thresholds, capital controls, ECOLOGICAL_COMPOSITE_DISCLOSURE. | 2026-05-18 |
| M9–M13 milestone sequence approved | M9 Standards Foundation → M10 Engine Integrity → M11 Political Economy → M12 Analyst Tooling → M13 Methodology Publication | 2026-05-11 |

---

## Architectural State — Key Facts for Session Continuity

**ADR-007 Synthetic Data Framework — accepted ✅ (PR #510). Live in `docs/adr/ADR-007-synthetic-data-framework.md`.**

- Five-method hierarchy: Bayesian Structural (Method A, requires ≥10 comparables + holdout) → MICE (Method B, bounded gap ≤3 periods) → Bootstrap Resampling (Method C) → Structural Extrapolation (Method D) → Structural Absence (Method E, generates bounds only)
- Quantity schema extension (4 new fields — M10 implementation prerequisite, Alembic migration required): `is_synthetic: bool`, `synthetic_method: str | None`, `comparison_group_id: str | None`, `holdout_validated: bool | None`
- MDA alert behavior: Tier 3 → advisory amber dashed in primary cluster; Tier 4 → exploratory signal secondary panel only; Tier 5 → no alert; CI straddling MDA floor → blue "Cannot determine MDA status" in primary cluster
- Comparison group registry: follows `source_registry` pattern, new table required before Method A deployment, managed by Data Quality Agent (Issue #300)
- Anomaly detection: opt-in, Modes 1+2 only, TSC sign-off before production, governance indicators permanently excluded
- Panel review artifact: `docs/adr/reviews/ADR-007-panel-review.md`. Mermaid diagram: `docs/architecture/ADR-007-method-selection-flowchart.mmd`

**ADR-005 Amendment 4 — GovernanceModule PROMOTED ✅ (PR #585, Issue #556). Governance axis live as of M10.**

- All five promotion criteria met at M10. Governance composite live via `normalized_absolute_strategy`.
- `SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS = frozenset({"ecological", "governance"})` — governance exempt from single-entity null suppression and single-entity note.
- `_UNIMPLEMENTED_FRAMEWORKS = set()` — empty; governance removed at promotion.
- Three elasticities: `gdp_growth_change→rule_of_law_percentile` (-0.08), `imf_program_acceptance→democratic_quality_score` (+0.005), `emergency_declaration→democratic_quality_score` (-0.05; Bermeo 2016).
- MDA threshold seeded: `MDA-GOV-DEMOCRACY-FLOOR` — `democratic_quality_score ≤ 0.70 → WARNING` (migration `e3b7f1c9d5a2`).
- Greece M10 demo fixture: WGI 2010 rule-of-law seed (60.0), V-Dem 2010 LDI seed (0.72), `emergency_declaration` at step 5 → MDA alert fires step 6.
- `EmergencyInstrument.EMERGENCY_DECLARATION = "emergency_declaration"` added to enum.
- `FourFrameworkZone1D.tsx`: `(in validation)` annotation removed (IR-005 resolved).
- `greenlet==3.1.1` added to requirements.txt (SQLAlchemy async on Python 3.13 CI).
- Promotion gate tests in `test_measurement_output.py` removed; replaced by backtesting integration test.

**PMM live computation — merged ✅ (PR #587, Issue #496 IR-002). Breach-exclusion fix — PR #650 (closes #648):**
- `PMMRecord` schema: `value` (Decimal-as-str, [0,1]) + `direction` ("up"/"down"/"flat")
- `TrajectoryStep.pmm: PMMRecord | None` — null when no applicable threshold has matching indicator, OR when all thresholds are already breached
- `_pmm_indicator_margin()`: [0,1] headroom for one threshold; approach window = `floor * approach_pct`; both `lte` (lower-bound) and `gte` (upper-bound) operators supported
- `_compute_pmm_for_step()`: **skips breached thresholds (margin == 0)**; min-of-margins across non-breached applicable thresholds; returns None when all thresholds breached (displayed as "—"); direction from prev-step delta vs ±0.01; cohort-scoped thresholds skipped; entity-scoped thresholds matched by exact entity_id
- MDA thresholds fetched once per trajectory request (not per step)
- Argentina Demo 3 PMM path: Steps 0–1 ≈ 0.2857 (governance headroom; ecological CO2 breach excluded), Step 2 ≈ 0.4286 (↑ Kirchner recovery improvement), Steps 3–4 = None / "—" (governance threshold breached by emergency_declaration at step 2)
- Frontend: `useEffect([currentStep, store.trajectory])` in `ScenarioInstrumentCluster` syncs `pmm_value`/`pmm_direction` to Zustand store; `TrajectoryStep` store type extended with `pmm` field
- 31 unit tests: `backend/tests/unit/test_pmm_computation.py` (3 new breach-exclusion tests replace old `test_min_across_thresholds`)

**ADR-001 + ADR-002 — renewed ✅ (PR #661). Valid Until Milestone 11.**

- No renewal triggers fired in M10. ADR-001: no schema changes. ADR-002: GovernanceModule `EMERGENCY_DECLARATION` is an internal enum, not a ControlInput taxonomy addition.
- M10 exit review entries added (SCAN-024, 2026-06-03).

**ADR-005 — Amendment 5 appended ✅ (PR #661). Valid Until Milestone 11.**

- GovernanceModule M10 promotion formally recorded: all 5/5 criteria met.
- M9 obligations discharged: normalization audit complete; tooltip annotation removed (IR-005, #499).

**ADR-007 — renewed ✅ (PR #661). Valid Until Milestone 11.**

- Not implemented in M10. No Quantity schema changes. No triggers fired.

**ADR-008 — renewed ✅ (PR #661). Valid Until Milestone 11.**

- step_event_label content fix ≠ schema rename (trigger requires rename/retype/removal). Zone 1 implementation per spec is not a trigger. AC-006 RTL confirms simultaneous update contract.

**ADR-010 — renewed ✅ (PR #661). Valid Until Milestone 11.**

- PMM API extension fields (`pmm_value`, `pmm_direction`) not consumed by TrajectoryView — Zone 1A data contract unchanged. Note: ADR-009 streaming decision may trigger shared state architecture trigger in M11.

**ADR-005 Amendment 3 — merged ✅ (PR #309). Now live in `docs/adr/ADR-005-human-cost-ledger.md`.**

**M8 demo scenario — merged ✅ (PR #328). Implements Issue #269:**
- `build_greece_demo_scenario()` in `tests/fixtures/greece_2010_scenario.py`
- EcologicalModule enabled via `modules_config: {ecological: {enabled: True}}`
- CO2 seed: `co2_concentration_ppm = 388.0 ppm` (NOAA MLO 2010) in initial_attributes
- 5 backtesting tests in `tests/backtesting/test_greece_m8_demo.py`
- CLI demo: `backend/scripts/demo_greece_2010_2015.py`
- `gdp_direction_step5_positive` moved to deferred_thresholds (Issue #221)
- EcologicalModule STOCK delta path: emits `current + elasticity_delta` (not raw delta)

**M8 ecological backend — merged ✅ (PR #324). Implements Issues #312, #313, #314:**
- `_compute_composite_score` now async with three-branch dispatch; ecological uses `_boundary_proximity_strategy`
- `_ECOLOGICAL_MANDATORY_NOTE_TEMPLATE` with `{n_indicators}` slot
- `_SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS = frozenset({"ecological", "governance"})` — both exempt from single-entity null suppression (governance added M10 PR #585)
- Migrations: `c1a4e7f2d9b3` (confidence_tier), `d2b5f8a3e6c4` (ecological MDA thresholds)
- EcologicalModule: stock-path proximity computation from `entity.attributes`; temporal guards per `effective_from`
- `land_use_pressure_index` proximity uses `min(v, 2.0)` — no division by 0.25 (double-normalization prevention)

**M8 frontend UX — merged ✅ (PR #329). Implements Issues #317, #318, #319, #320:**
- `INDICATOR_DISPLAY_NAMES` registry in `RadarChart.tsx` — human-readable labels for all M8 indicators
- Zone 3A expandable ecological note — `EcologicalNoteDrawer` component
- PMM Zone 1C widget — `PolicyManoeuvreMeter` null placeholder (M8 scope)
- Radar chart 250ms CSS transition animation — `prefers-reduced-motion` + null-axis guard

**Frontend — null governance axis (Issue #315, PR #323 ✅ merged):**
- `RadarAxisDatum.composite_score: number | null` live on main
- `GOVERNANCE_IN_VALIDATION_LABEL` + `GOVERNANCE_IN_VALIDATION_TOOLTIP` exported constants
- `computeFinalScore(composite_score: number | null, weight: number): number | null` exported pure function
- Null axis: dashed hollow SVG circle (`strokeDasharray="2 2"`, `fill="none"`); Recharts polygon gap
- DD-011 in `docs/frontend/design-decisions.md` with sentinel

**M8 UX Design Thinking work stream — complete (PRs #355, #356):**
- Critique: `docs/ux/design-thinking/m8-interaction-model-critique.md` — six ranked premise changes; core diagnosis: WorldSim is spatial comparison tool applied to temporal problem
- Panel synthesis: `docs/ux/design-thinking/m8-critique-panel-synthesis.md` — three-agent panel; nine cross-cutting concerns; three EL decisions
- First principles review: `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md` — supersedes synthesis on conflicts
  - Case B verdict: architecture rethink before M9 implementation
  - Root finding: choropleth (context) occupies primary viewport; instruments (radar, PMM, MDA alerts) are in 25% drawer — inverted
  - Four primary flight instruments named (trajectory view, PMM, MDA alerts, four-framework current position) — all must be always visible without drawer
  - Decision 1 (north-star formulation): extend to per-mode tasks, not single formulation
  - Decision 2 (timeline zone assignment): wrong question — defer, reframe as viewport architecture question
  - Decision 3 (compare mode conditional): correct question — add Mode 3 case (always temporal, never choropleth)
  - Five M9 governing premises: (1) instruments in primary viewport, (2) instruments always visible without drawer, (3) step axis is shared frame for all instruments, (4) primary cognitive task per mode, (5) control plane reserved in layout before built
  - Highest-priority action: update information-hierarchy.md governing principle
- UX Design Thinking Agent persona: `docs/process/agents.md` — activation: `UX Design Thinking Agent: CRITIQUE — [scope]`

**Demo preparation standard — established ✅ (PR #334):**
- `docs/process/demo-preparation-standard.md` — nine-step biennial demo cadence; reference cases M6 (#220) and M8 (#333)
- `docs/demo/m6/` — M6 review and walkthrough archived
- `docs/demo/m8/screenshot-brief.md` — UX Agent five-frame brief for Issue #233
- Thesis frame: Frame C, Step 5 (2014) — asymmetric radar (financial partial recovery, HD depressed)
- Presentation sequence: C → A → B → D → E (lead with thesis)
- #233 closed ✅ — demo.sh updated, spec rewritten (M8), five frames captured, IR Agent review filed
- IR review: `docs/demo/m8/reviews/2026-05-18-v0.8.0-stakeholder-review.md` — 9 findings, issues TBF
- `docs/demo/stakeholder-walkthrough.md` is M6-era — needs M8 update before next review cycle

**Standards state:**
- Canonical unit registry: in DATA_STANDARDS.md §Canonical Unit Registry (PR #282)
- Field-level certification standard: in DATA_STANDARDS.md §Field-Level Data Certification (PR #282)
- simulation_reference_constants table: migrations a2b4c6d8e0f1 + b3c5d7e9f1a2 (PR #282)
- Intent block format: ratified in CODING_STANDARDS.md §Intent Blocks (PR #288)
- Framework promotion protocol: in CODING_STANDARDS.md §Framework Promotion Protocol (PR #282)
- [SIM-INTEGRITY] monitoring contract: in CODING_STANDARDS.md §Simulation Integrity Monitoring (PR #282)
- Disposition review standard: docs/process/disposition-review-standard.md (PR #283)

**Legibility baseline:**
- M7 baseline mean audit score: 6.8/10
- Lowest scoring function: `_reconstruct_state_from_snapshot` — 5/10 (fixed in PR #289)
- Baseline document: docs/standards/legibility-baseline-m7.md
- Blind audit prompt: docs/process/blind-code-audit-prompt.md

**M8 gate status (all clear):**
- #235 DIC blind interviews ✅
- #255 Legibility metrics baseline ✅
- #256 North Star CODING_STANDARDS ✅
- #257 Blind code audit ✅

---

## Session Update Instructions

At the end of every Claude Code session, update this file:
1. Update "Last updated" date
2. Move completed streams to Recently Merged PRs
3. Add any new open issues to the appropriate horizon section
4. Record any Engineering Lead decisions made
5. Update ADR-005 amendment scope if decisions were made
6. If a new agent was activated or defined this session, verify `docs/process/agents.md` is current before closing
7. This update is the **last action** of every session before closing

<!-- branch-protection-skip-test: 2026-06-16T16:19:16Z -->
