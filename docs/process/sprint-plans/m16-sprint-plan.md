---
name: m16-sprint-plan
type: sprint-plan
milestone: M16 — Distributional Visibility
status: Filed — awaiting EL approval
authored-by: PM Agent
authored-date: 2026-06-23
el-approved: false
consulted-agents:
  - Business Product Owner (Demo 6 value prioritization; scope cut order)
  - Frontend Architect (zone component grouping; G1/G2 sequencing; Zone 1D layout conflict)
  - Chief Engineer (backend dependency chain; G3 25-year projection feasibility)
  - Architect (ADR prerequisites; ADR-007 coverage of #22)
sop-reference: docs/process/sprint-planning-sop.md
---

# M16 Sprint Plan — Distributional Visibility

**Status:** Filed — awaiting EL approval; implementation may not begin until EL approves this document
**Release branch:** `release/m16` (cut from `main` 2026-06-23)
**Exit checklist issue:** #985 (renamed 2026-06-23 — "M16 Exit Checklist — blocks milestone closure")
**Primary objective:** Zone 1A Phase 4 composite encoding + distributional surface (cohort disaggregation #986 + political risk #987) + 25-year human capital trajectory (#274) + live stakeholder demo with real external participants (#843 — M16 exit gate). Demo 6: "Here is who bears the cost — specifically, this cohort, at this step, for this long."

**M16 exit gate:** #843 — live stakeholder demo with real external participants. #985 (exit checklist) closes last.

---

## Kickoff Prerequisites (Status at Sprint Plan Filing)

| Step | Status | Notes |
|---|---|---|
| 1. PM Agent cuts `release/m16` from `main` | ✅ DONE 2026-06-23 | `release/m16` cut from `main` at commit 07c92b8 |
| 2. PM Agent authors `m16-sprint-plan.md` | ✅ THIS DOCUMENT | Filed 2026-06-23; EL approval pending |
| 3. EL approves sprint plan | ⬜ PENDING | Required before any G-group sprint entry opens |
| 4. #985 renamed "M16 Exit Checklist" | ✅ DONE 2026-06-23 | GitHub issue title updated |
| 5. #845 milestone corrected to M16 | ✅ DONE 2026-06-23 | Was M15 (Phase 4 is M16 scope); corrected |
| 6. CI trigger verified | ✅ CLEAR | `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` |

---

## HORIZON Scope-Completeness Check (Step 6)

Run against `CLAUDE.md §Milestone 16` and `docs/roadmap/worldsim-roadmap.md §Milestone 16`.

### Roadmap deliverables — linkage audit

| Roadmap deliverable | Issue | Status |
|---|---|---|
| Zone 1A Phase 4 — composite encoding in primary viewport | #845 | ✅ Tracked; M16 milestone corrected 2026-06-23 |
| Zone 1D delta annotations — companion to Phase 4 (BPO phase 4 gate) | #1147 | ✅ Filed 2026-06-23 (was UNTRACKED at M15 close) |
| Cohort disaggregation on primary surface | #986 | ✅ Tracked |
| Political risk summary surface for Persona 3 | #987 | ✅ Tracked |
| 25-year human capital depletion trajectory | #274 | ✅ Tracked |
| Calibrated ecological-to-financial transmission | #275 | ✅ Tracked |
| Distributional scenario comparison (variance + percentile by cohort) | #102 | ✅ Tracked |
| Uncertainty quantification — full distributional output as scenario bands | #22 | ✅ Tracked |
| Live stakeholder demo with real external participants | #843 | ✅ Tracked (M16 exit gate) |
| Demo 6 — Senegalese Finance Minister scenario | — | Covered by #843 demo preparation; no separate tracking issue required |
| Founding document AC-001/AC-002 addition | #1145 | ✅ Filed at HORIZON sweep 2026-06-23 |

**Scope gap finding (2026-06-23):** Zone 1D delta annotations were a BPO phase 4 gate condition from M15-G2 sprint exit but had no tracked issue. Filed as #1147 at kickoff.

### ADR backlog review

| ARCH entry | Status | Action |
|---|---|---|
| ARCH-001 through ARCH-011 | All ACCEPTED or ASSIGNED (ADR-017 ACCEPTED 2026-06-22) | No action needed |
| ARCH-012 | NOT FILED | No new ADR required for G1/G2/G3 core deliverables — see §ADR Prerequisites. G4 (#22) requires ADR-007 coverage confirmation before sprint entry. If coverage is insufficient, ARCH-012 would be filed then. |

No PENDING backlog entries are more urgent than current M16 work.

---

## Four-Agent Consultation Summary

### Business Product Owner — Demo 6 value prioritization

The Demo 6 north star: a Senegalese Finance Minister's team walks into an Article IV consultation with a screen showing bottom-quintile threshold crossings at step 2, a 25-year human capital trajectory, and PSP trajectory with plain-language interpretation — all visible in the primary viewport without drawer navigation. Three capabilities are required for this story to land:

1. **Zone 1A composite encoding + Zone 1D delta annotations (#845/#1147)** — the visual framework that makes distributional data legible in context; delta annotations make the PSP trajectory self-interpreting in temporal terms
2. **Cohort disaggregation (#986) + political risk summary (#987)** — the bottom-quintile story without drawer navigation; the political feasibility argument in plain language
3. **25-year human capital trajectory (#274)** — the "teachers and doctors leaving the public sector by step 6" argument; a generation-length consequence visible in the instrument

Without all three, Demo 6 cannot make the argument "this cohort, at this step, for this long." A scope cut must never touch G1, G2, or G3.

**Scope cut order if needed:** Cut G4 distributional infrastructure (#102, #275, #22 full) first — Demo 6 does not require multi-scenario comparison, ecological transmission, or full uncertainty bands. Then secondary features in G5. Never G1/G2/G3/G8.

### Frontend Architect — zone component grouping

**G1 and G2 must be sequential, not parallel.** G1 (#845/#1147) modifies the Zone 1A rendering base (composite encoding replaces single-line trajectory) and Zone 1D (delta annotations added to PSP sub-section). G2 (#986/#987) adds distributional content layers to Zone 1A (cohort rows) and extends Zone 1D (political risk sub-section). If G2 begins before G1 merges, both PRs will conflict on Zone 1A and Zone 1D component trees.

**Zone 1D layout risk:** G1 adds delta annotations to PSP (#1147); G2 adds a political risk sub-section (#987). Both land in Zone 1D. Frontend Architect must confirm Zone 1D layout spec at G1 sprint entry — specifically that the delta annotation and the political risk sub-section coexist at 1280×800 without displacing four-framework rows. This is the primary cross-group layout risk in M16.

**#986 and #987 in the same G2 group is correct.** Both affect the primary surface layout and the M15-G3 design specified them together. A shared PR reduces layout merge risk within the group.

**G5 issues** (#837, #951, #1145, #259) touch documentation, process, and intent template files — no frontend component conflicts. Can run in parallel with G1 from day one.

### Chief Engineer — backend dependency chain

**G1 is frontend-only.** Delta computation (#1147, AC-4) is client-side from existing trajectory state. No new backend endpoint required for G1. Backend already serves trajectory data including PSP values from M13.

**G2 (#986) is the primary backend risk.** DemographicModule exists (M4) but cohort-level trajectory data exposure to the frontend requires confirmation. The DA sign-off (cohort field availability for GRC/JOR/EGY/ZMB) is the critical pre-condition. If cohort fields are not already in the trajectory API response, G2 will require a backend endpoint extension — the scope of which must be determined before the sprint entry is filed.

**G2 (#987 political risk)** is lower backend risk. PSP values are already in the trajectory response from M13. The summary surface requires formatting PSP + direction/trend. Likely frontend composition from existing data; confirm at sprint entry.

**G3 (#274 25-year trajectory)** requires backend assessment before sprint entry. The current simulation runs programme-length scenarios (~8 steps for Zambia ECF). A 25-year projection at quarterly resolution requires 100 steps. The Chief Engineer must assess: (a) computation feasibility on target hardware (8GB/4-core) at 100-step depth, (b) whether a separate projection endpoint is required or the existing simulation can be configured with an extended step horizon. This assessment gates G3 sprint entry. File a pre-G3 CE assessment as an intent decision before sprint entry.

**Dependency chain:** G1 (no backend dependency — start immediately after sprint entry) → G2 backend (after DA sign-offs; can run in parallel with G1 frontend if sign-offs land early) → G3 (after CE assessment; can run in parallel with G2) → G4 (capacity-allowing; no earlier than G2 complete).

### Architect — ADR prerequisites

| Group | ADR required | Coverage | Gate |
|---|---|---|---|
| G1 (#845 Phase 4) | ADR-017 | ACCEPTED 2026-06-22 — covers composite encoding architecture | CLEAR |
| G1 (#1147 delta annotations) | ADR-015 | ACCEPTED — covers Zone 1D evidence thread; delta annotation extends the self-interpreting pattern | CLEAR |
| G2 (#986 cohort) | ADR-017 | ADR-017 disposition (b): cohort sub-zone independent; design per M15-G3 | CLEAR |
| G2 (#987 political risk) | ADR-017 + ADR-015 | Zone 1D extension per ADR-017; evidence thread per ADR-015 | CLEAR |
| G3 (#274) | None | DemographicModule extension within M4 module boundary; no new module ADR required | CLEAR |
| G4 (#22 full) | ADR-007 | **ADR-007 coverage of full distributional bands must be confirmed before G4 sprint entry.** ADR-007 covers confidence tiers and scenario banding framework. If full distributional output as scenario bands requires architectural decisions beyond ADR-007 scope, file ARCH-012 and author an amendment. CONDITIONAL — confirm at G4 sprint entry. | CONDITIONAL |
| G4 (#102, #275) | None | Within existing module boundaries (ADR-012 for #275; API extension for #102) | CLEAR |

No new ARCH entry required at kickoff. ARCH-012 may be needed for #22 — assess at G4 sprint entry.

---

## Sprint Groups

| Group | Issues | ADR gate | Wave | Description |
|---|---|---|---|---|
| G1 — Zone 1A Phase 4 + Zone 1D Delta | #845 (Phase 4), #1147 | ADR-017 ✅, ADR-015 ✅ | Wave 1 | Zone 1A composite encoding (multi-scenario/multi-entity/L0-badge per ADR-017 Phase 4); Zone 1D delta annotations (step-over-step PSP change, direction, Layer 3 self-interpreting). These two issues are BPO-gated to ship together. |
| G2 — Distributional Surface | #986, #987 | ADR-017 ✅, ADR-015 ✅ | Wave 2 (after G1 + pre-conditions) | Cohort disaggregation on primary surface (bottom-quintile threshold crossings in Zone 1B/1A area without drawer navigation); political risk summary surface (PSP trajectory + plain-language legitimacy dynamics in Zone 1D). Design complete M15-G3. Pre-conditions required before sprint entry: CM sign-off, DA sign-off, ARF confirmation, Frontend Architect layout feasibility. |
| G3 — Demo 6 Infrastructure | #274 | None (CE assessment required) | Wave 2 (parallel with G2 backend) | 25-year human capital depletion trajectory — DemographicModule extension. CE assessment of 100-step computation feasibility on target hardware required before sprint entry. Demo 6 Senegal scenario configuration included as part of this group (data prep, not a separate deliverable — covered by #843 demo preparation). |
| G4 — Distributional Infrastructure (capacity-allowing) | #102, #275, #22 (scoped) | #22: ADR-007 confirmation required | Wave 3 | Distributional scenario comparison variance/percentile (#102); calibrated ecological-to-financial transmission (#275); uncertainty quantification scoped to distributional bands on cohort output (#22 — full #22 is beyond M16 scope; scope to Demo 6 requirements only). Not Demo 6 critical path — cut here before any other group if capacity is constrained. |
| G5 — Process + Secondary Features | #837, #951, #1145, #259 | None | Wave 1 (parallel with G1) | Config-driven demo scripts; solo-use review protocol; founding document AC-001/AC-002 addition (EL-authored); CTO legibility metrics dashboard. Process and documentation work — no frontend component conflicts. #1145 is EL-authored (small documentation edit). |
| G6 — Accessibility + Performance Validation | #569 | None | Wave 3 (after G1/G2) | MV-002 Mode 3 hardware validation; accessibility re-validation on 8GB/4-core target hardware following G1/G2 primary surface changes. Pattern: M15-G6. |
| G7 — Governance | #3, #6 | None | Any (EL-action) | Single-principal separation of duties (#3) and branch protection restoration (#6). EL-action only — no sprint entry document required. May proceed at any point. |
| G8 — Live Stakeholder Demo | #843 | G1 + G2 + G3 complete | Exit gate | Live stakeholder demo with real external participants. M16 exit gate. Requires G1/G2/G3 merged and BPO-accepted before demo session is scheduled. Demo 6 story: Senegalese Finance Minister; bottom-quintile, 25-year trajectory, PSP trajectory. |

### Near-term backlog (on M16 milestone, not in a wave)

These issues are assigned to M16 but are secondary features — not Demo 6 critical path. Included in M16 if capacity remains after G1–G6 complete. Otherwise carry to M17.

| Issue | Title | Why deferred within M16 |
|---|---|---|
| #153 | feat(frontend): absolute threshold overlay on DeltaChoropleth | Enhancement; not Demo 6 critical |
| #846 | ux: DEMO-045 — Mode 3 branch comparison values absent | Enhancement; not Demo 6 critical |
| #97 | arch(api): threshold-crossing markers in compare output | API enhancement; not Demo 6 critical |
| #92 | arch(backtesting): Greece 2010 investment climate conditions | Backtesting fixture; not Demo 6 critical |

---

## Sprint Sequencing

```
G5 (process — parallel) ───────────────────────────────────────────────────────┐
                                                                                │
G7 (governance — EL-action, any time) ─────────────────────────────────────────┤
                                                                                │
G1 (Zone 1A Phase 4 + Zone 1D delta) ──────────────────────────────────────────┤
         │                                                                      │
         └── G2 pre-conditions (CM/DA/ARF/FA sign-offs — parallel with G1) ─┐  │
                                                                             ↓  │
                                        G2 (distributional surface) ─────────┤  │
                                                                             │  ├──► G8 (live demo — M16 exit)
                                        G3 (Demo 6 infrastructure) ─────────┤  │
                                                (CE assessment first)        │  │
                                                                             ↓  │
                                        G4 (distributional infra — cap-allowing)│
                                                                                │
                                        G6 (accessibility + perf validation) ──┘
```

**Critical path:** G1 → G2 (sequential on frontend) → G8. G3 can begin backend work in parallel with G2 frontend once CE assessment is complete. G4 is not on the critical path.

---

## Pre-Conditions for G2 Sprint Entry

These four items must be completed before a G2 sprint entry document is filed. They are best worked in parallel with G1 implementation.

| Pre-condition | Responsible | Target |
|---|---|---|
| CM sign-off on #986: cohort indicator scope + MDA-derived floor methodology (AC-3) | Chief Methodologist | Comment on #986 |
| CM sign-off on #987: PSP severity tier thresholds + 2pp direction sensitivity (AC-11) | Chief Methodologist | Comment on #987 |
| DA sign-off on #986: DemographicModule cohort field availability for GRC/JOR/EGY/ZMB | Data Architect | Comment on #986 |
| Architecture Review Facilitator confirmation: AC-1–AC-6 (#986) and AC-7–AC-11 (#987) reviewed | ARF | Comment on both issues |
| Frontend Architect: Zone 1D layout feasibility — delta annotations + political risk sub-section at 1280×800 | Frontend Architect | Comment on #987 (after G1 sprint entry is filed) |

---

## ADR Prerequisites Summary

| Group | ADR required | Status | Implementation may begin? |
|---|---|---|---|
| G1 | ADR-017, ADR-015 | Both ACCEPTED | Yes — after sprint entry |
| G2 | ADR-017, ADR-015 | Both ACCEPTED | Yes — after sprint entry + pre-conditions |
| G3 | None | N/A | Yes — after CE assessment + sprint entry |
| G4 | ADR-007 (confirm for #22) | Confirm coverage at sprint entry | #22 conditional on ADR-007 scope confirmation |
| G5 | None | N/A | Yes — after sprint entry |
| G6 | None | N/A | Yes — after sprint entry |
| G8 | None | N/A | Yes — after G1 + G2 + G3 BPO-accepted |

---

## Exit Conditions

M16 closes when all of the following are satisfied:

1. **Business PO acceptance** recorded for all user-facing G-group deliverables (G1, G2, G3, and any G4 items delivered)
2. **Customer Agent Layer 3 assessment** on record for any capability serving Personas 2, 3, or 5 (G1 required: Zone 1A composite encoding, Zone 1D delta annotation; G2 required: cohort disaggregation, political risk summary)
3. **North star test artifact** filed: a Senegalese Finance Minister's analyst can cite bottom-quintile threshold crossing at step N, 25-year human capital consequence, and PSP trajectory in plain language — all visible in the primary viewport without drawer navigation, in a solo unnarrated session
4. **Live stakeholder demo delivered** (#843): real external participants attended; stakeholder review artifact filed
5. **PI Agent exit gate confirmation** recorded in the M16 sprint exit document
6. **No active soft-skip patterns** in E2E suite (M15 retrospective action — confirm before M16 exit, NM-056 follow-up)

CI green and issue closure are necessary but not sufficient. #843 is the primary exit gate.

---

## Sprint Entry Gate Requirements

Per `docs/process/sprint-planning-sop.md §Sprint Entry Gate`, implementation may not begin on any sprint group until:

1. This sprint plan is EL-approved
2. A sprint entry document is filed at `docs/process/sprint-plans/m16-{group}-sprint-entry.md` per the template
3. The entry document is committed and referenced in `SESSION_STATE.md`

**Exceptions (no sprint entry document required):**
- G7 (governance — EL-action items #3 and #6; no implementation)

**G2 additional gate:** All five pre-conditions listed in §Pre-Conditions for G2 Sprint Entry must be satisfied before the G2 sprint entry document is filed.

**G3 additional gate:** CE assessment of 25-year projection feasibility (#274) must be filed (as a comment on #274 or a decision in the G3 sprint entry) before implementation begins.

---

## M16 Kickoff Sequence

1. ✅ PM Agent cuts `release/m16` from `main` — DONE 2026-06-23 at commit 07c92b8
2. ✅ CI trigger verified — `.github/workflows/ci.yml` covers `release/m*`
3. ✅ #985 renamed "M16 Exit Checklist" — DONE 2026-06-23
4. ✅ #845 milestone corrected to M16 (GitHub milestone 17) — DONE 2026-06-23
5. ✅ #1147 filed — Zone 1D delta annotations (was UNTRACKED) — DONE 2026-06-23
6. ✅ This sprint plan filed — DONE 2026-06-23
7. ⬜ EL approves sprint plan — PENDING
8. ⬜ G2 pre-conditions initiated (CM/DA/ARF/FA sign-off requests opened on #986 and #987) — immediately after EL approval
9. ⬜ G1 sprint entry filed and EL-approved — G1 is first implementation group
