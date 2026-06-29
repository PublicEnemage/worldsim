---
name: m18-sprint-plan
type: sprint-plan
milestone: M18 — Full Argument and Demo 7
status: EL-approved 2026-06-26; G6 CLOSED 2026-06-29 (integration PR #1479 → release/m18); G7 sprint entry filed 2026-06-29 (pending EL approval)
authored-by: PM Agent
authored-date: 2026-06-26
el-approved: 2026-06-26
consulted-agents:
  - Business Product Owner (Demo 7 value prioritization; scope cut order; Mode 3 as Act 1 anchor)
  - Frontend Architect (file area grouping; Wave 1 parallel safety; Wave 2 sequencing; InstrumentCluster.tsx conflict map)
  - Computation Engine Agent (backend dependency chain; N=3 API carry-forward from M17; shock injection scope)
  - DevSecOps Agent (new dependencies; output path coverage; backend test-results/ gap)
  - Architect (ADR prerequisite confirmation; G3 ADR determination gate; ADR-019 design-first sequencing)
sop-reference: docs/process/sprint-planning-sop.md
---

# M18 Sprint Plan — Full Argument and Demo 7

**Status:** EL-approved 2026-06-26 (PR #1364) — Wave 1 sprint entries may be filed and approved; pre-wave GD and GR phases may begin immediately
**Release branch:** `release/m18` — cut from `main` 2026-06-26 at commit 8cffc86 (after sync PR #1366)
**Exit checklist issue:** #1340 (M18 Exit Checklist — blocks milestone closure)
**GitHub Milestone:** #19

**Primary objective:** Demo 7 — the complete analytical argument at the negotiating table. Two acts: Act 1 (Senegal, Mode 3 active control) asks "is there a configuration that avoids the bottom quintile crossing the 0.40 floor?" — both outcomes are valid answers. Act 2 (Zambia, three-scenario comparison) shows the counter-proposal as a specific number differential with confidence bands and a historical precedent.

**M18 exit gate:** PI Agent exit gate confirmation, with BPO acceptance for all Wave 1 and Wave 2 user-facing deliverables. Demo 7 live session (#843) is the milestone north star — it is the last mandatory deliverable before M18 closes. #1340 closes last.

**M18 thesis:** M17 proved the engine is calibrated. M18 delivers the complete argument: inputs cited, methodology transparent, human cost visible, alternatives compared, counter-scenario quantified. The question M18 answers is not "what can the engine model" — it is "what instrument does the finance minister hold in her hands when the IMF team says this is the only viable path?" M18's answer: a counter-proposal with a specific number differential, a confidence band, a historical precedent, and a programme survival probability. And if no counter-proposal within the fiscal envelope prevents the crossing — that is the most powerful finding the tool can produce.

---

## Kickoff Prerequisites (Status at Sprint Plan Filing)

| Step | Status | Notes |
|---|---|---|
| 1. EL merges `release/m17` → `main` (admin bypass) | ✅ DONE 2026-06-26 | PR #1341 merged (M17 exit ceremony); `main` at 0ccf938 |
| 2. PM Agent authors `m18-sprint-plan.md` | ✅ THIS DOCUMENT | Filed 2026-06-26 |
| 3. EL approves sprint plan | ⏳ PENDING | EL approval required before Wave 1 sprint entries open |
| 4. PM Agent cuts `release/m18` from `main` | ⏳ PENDING | Cut immediately after EL approval |
| 5. CI trigger verified | ✅ CLEAR | `.github/workflows/ci.yml` covers `release/m*` and `sprint/m*` (verified 2026-06-26) |
| 6. #1340 named M18 Exit Checklist | ✅ DONE | Already filed at M18 open |
| 7. Issue audit complete | ✅ DONE | Full HORIZON sweep below |

---

## HORIZON Scope-Completeness Check

Full M18 issue audit completed 2026-06-26. All 18 M18 issues accounted for.

### Roadmap deliverables — linkage audit

| Roadmap deliverable | Issue | Group | Status |
|---|---|---|---|
| CI bands on Zone 1A trajectory curves — ADR-007 full implementation | #1254 | G1 | ✅ Tracked |
| PSP driver decomposition — dominant signal category alongside severity label | #1255 | G2 | ✅ Tracked |
| Counter-scenario comparison — distributional differential with CI bands | #1349 | G3 (blocked: GR) | ✅ Tracked; requirements phase gates sprint entry |
| Mode 3 render optimization — EX-001 expired | #1217 | G4 | ✅ Tracked; control plane ADR-019 gates sprint entry |
| Control plane column — Mode 2 + Mode 3 full column vision | #1354 + #1355–#1361 | GD (design) | ✅ Tracked; 7-artifact design package; EL gate on Artifact 5 |
| Demo 7 — live external session (Senegal Act 1 + Zambia Act 2) | #843 | Milestone exit gate | ✅ Tracked |

### Design package — linkage audit

| Artifact | Issue | Pre-wave phase | Status |
|---|---|---|---|
| Artifact 1 — current state audit | #1355 | GD Phase 1 | ✅ Tracked; may begin immediately |
| Artifact 2 — target state specification | #1356 | GD Phase 2 | ✅ Tracked; after Artifact 1 |
| Artifact 3 — Customer Agent Layer 3 assessment | #1357 | GD Phase 1 | ✅ Tracked; may begin immediately |
| Artifact 4 — delta analysis and dependency map | #1358 | GD Phase 2 | ✅ Tracked; after Artifact 1 |
| Artifact 5 — scope decision document (EL gate) | #1359 | GD Phase 3 | ✅ Tracked; EL approval required; blocks ADR-019 authorship |
| Artifact 6 — ADR-019: Control Plane Column | #1360 | GD Phase 4 | ✅ Tracked; ASSIGNED in backlog; may not be authored until Artifacts 2, 4, 5 on record |
| Artifact 7 — Journey C update + Journey A GA-02 resolution | #1361 | GD Phase 4 | ✅ Tracked; after ADR-019 initiated |

### Full issue-to-group mapping

| Issue | Title | Group | Wave | Priority |
|---|---|---|---|---|
| #1340 | M18 Exit Checklist | — (gate) | — | Milestone exit gate |
| #843 | Demo 7 — live stakeholder demo | — (exit gate) | Exit | Primary deliverable |
| #1354 | Control Plane Design Package (parent) | GD | Pre-wave | Design-first gate |
| #1355 | Artifact 1 — current state audit | GD | Pre-wave Phase 1 | **Immediate** |
| #1356 | Artifact 2 — target state spec | GD | Pre-wave Phase 2 | After Artifact 1 |
| #1357 | Artifact 3 — Customer Agent L3 | GD | Pre-wave Phase 1 | **Immediate** |
| #1358 | Artifact 4 — delta analysis | GD | Pre-wave Phase 2 | After Artifact 1 |
| #1359 | Artifact 5 — scope decision (EL gate) | GD | Pre-wave Phase 3 | After Artifacts 2+4 |
| #1360 | Artifact 6 — ADR-019 | GD | Pre-wave Phase 4 | After EL approves #1359 |
| #1361 | Artifact 7 — Journey C + GA-02 | GD | Pre-wave Phase 4 | After ADR-019 initiated |
| #1352 | Requirements phase for #1349 | GR | Pre-wave | **Immediate** |
| #1254 | CI bands on Zone 1A | G1 | Wave 1 | High |
| #1255 | PSP driver decomposition | G2 | Wave 1 | High |
| #1349 | Counter-scenario comparison | G3 | Wave 2 (blocked: GR) | High — Demo 7 Act 2 |
| #1217 | Mode 3 render optimization | G4 | Wave 2 (blocked: ADR-019) | High — EX-001 expired |
| #1256 | Path 2 proprietary data | — | Capacity-allowing | Low — closed 2026-06-27 (open-source strategy) |
| #1238 | DEMO6-009 narration fix | G5 | Wave 3 (capacity-allowing) | Low — CLOSED 2026-06-28 (fix was already in commit 6e8f618) |
| #1059 | HCL narration integration | — | Capacity-allowing | Low — CLOSED 2026-06-28 (superseded by G5 scope decision) |
| #1422 | Zone 3 auditability panel (US-1349-D) | G5 | Wave 3 (capacity-allowing) | High — Demo 7 Act 2 Lucas analytical scrutiny path |
| #1445 | Demo 7 preparation tracking | G6 | Wave 4 | Demo prep issue; G6 walkthrough, screenshot brief, Step 5d, narrated spec, frames, Step 6b review |
| #1459–#1474 | Step 6b DEMO-130–DEMO-153 findings (16 CRITICAL+HIGH issues) | G7 | Wave 4 (continued) | All CRITICAL and HIGH findings from the Step 6b nine-agent internal review (2026-06-29) — see `docs/demo/m18/reviews/2026-06-29-v0.18.0-internal-review.md` for full DEMO-NNN list |

### ADR backlog review

Performed 2026-06-26. Full sweep on record. Findings:

| Entry | Status | M18 relevance |
|---|---|---|
| ARCH-001 through ARCH-010 | All ACCEPTED | Clear — no action |
| ARCH-011 (ADR-017) | ACCEPTED 2026-06-22 | G1 governing authority for Zone 1A CI bands — CLEAR |
| ARCH-012 (ADR-018) | ACCEPTED 2026-06-25 | Zone 1B allocation — implementation complete; CLEAR |
| ARCH-013 (ADR-019) | ASSIGNED — design artifacts required first | G4 gate — may not be authored until #1359 EL-approved; may not be accepted without separate-session UX Designer sign-off (Tier 1, NM-042) |

No PENDING_NUMBER entries in backlog. No hidden ADRs awaiting activation.

---

## Five-Agent Consultation Summary

### Business Product Owner — Demo 7 value prioritization

M18's output is the complete argument at the negotiating table. Not a new capability demonstration — a full analytical stack that a minister's team can use live, under challenge, against a creditor side with institutional resources.

**Two-act Demo 7 structure:** Act 1 (Senegal, Mode 3) is the more powerful of the two — it is the only place in the WorldSim platform where the user applies an instrument and watches the counter-trajectory emerge in real time. Act 2 (Zambia, three-scenario comparison) is the distributional evidence act — already technically possible from M17 multi-scenario infrastructure (#394), but requiring the counter-scenario comparison number differential (#1349) and CI bands (#1254) to be complete.

**Scope cut order if capacity is constrained:**

1. Never cut Demo 7 itself (#843) — the milestone premise is a live external session
2. Never cut G1 (CI bands, #1254) — uncertainty bands are the epistemic foundation; "calibrated, not confident" cannot be demonstrated without them
3. Never cut G2 (PSP decomposition, #1255) — Demo 7 Act 1 requires the analyst to read "why" the PSP changed, not just the value
4. Never cut G4 control plane column work — Mode 3 Act 1 without the column populated is a failed demo; EX-001 has expired
5. Cut G3 (#1349) implementation to skeleton minimum if capacity is tight — Demo 7 Act 2 can demonstrate three-scenario comparison visually even without the full distributional differential UI; the infrastructure exists from M17. Degrade gracefully, don't eliminate.
6. Cut GD design artifacts to the minimum that unblocks ADR-019 and G4 — Artifact 5 is the EL gate; Artifacts 6 and 7 can be started without being complete at time of G4 sprint entry if ADR-019 has sufficient authorship for EL acceptance
7. Deferred items (#1256, #1238, #1059) are capacity-allowing — cut without demo impact

**Demo 7 Act 1 minimum viable demo (Senegal, Mode 3):**
The analyst must be able to: (1) activate Mode 3 from the current scenario state; (2) apply a fiscal counter-proposal via the policy input form; (3) observe the live A/B comparison trajectory; (4) read the causal attribution in Zone 1B explaining why the threshold crossing occurred or was avoided. The column must be populated — the current purple bottom-bar ControlPlane is not acceptable for a live external demo.

**Demo 7 Act 2 minimum viable demo (Zambia, three-scenario comparison):**
The analyst must be able to: (1) load three Zambia restructuring scenarios simultaneously; (2) read the Zone 1A trajectory differentiation across three curves; (3) cite the specific poverty headcount differential between the IMF proposed terms and the Zambian counter-proposal. The number "340,000 additional people below the poverty threshold under proposed terms vs. 80,000 under the counter-proposal" must be defensible and visually grounded.

### Frontend Architect — File area grouping and conflict assessment

The M18 issue board spans four distinct file area clusters. The parallel/sequential determination for Wave 1 and Wave 2 follows from the conflict analysis.

**G1 (#1254 — CI bands, Zone 1A):**
Primary files: `frontend/src/components/TrajectoryView.tsx` (CI ribbon rendering), `frontend/src/stores/` (uncertainty data shape), `backend/app/simulation/banding_engine.py` or equivalent uncertainty output method. Incidental: `InstrumentCluster.tsx` (minor — if passing band data as a prop to TrajectoryView). The CI band data format must be defined in the API contract and schema before implementation — `docs/schema/api_contracts.yml` and `docs/schema/simulation_state.yml` must be updated in the same PR.

**G2 (#1255 — PSP decomposition, Zone 1D):**
Primary files: Zone 1D component (likely `frontend/src/components/Zone1dSection.tsx` or the PSP sub-component within InstrumentCluster), `backend/app/simulation/political_economy_module.py` (PSP decomposition logic). No overlap with G1's TrajectoryView.tsx or banding engine. **G1 and G2 are safe to run in parallel in Wave 1** — they share no primary file areas and have minimal incidental risk at `InstrumentCluster.tsx`.

**G3 (#1349 — counter-scenario comparison):**
Primary files: new distributional comparison component (`frontend/src/components/CounterScenarioDiff.tsx` or similar), `ScenarioInstrumentCluster.tsx` (new rendering path for comparison mode), backend comparison endpoint (new route). Overlaps `ScenarioInstrumentCluster.tsx` with G4. **G3 and G4 must not run concurrently** — both touch `ScenarioInstrumentCluster.tsx`. Sequence: G4 first (control plane column restructures ScenarioInstrumentCluster), then G3 builds on the stable layout.

**G4 (Mode 3 control plane + #1217):**
Primary files: `InstrumentCluster.tsx` (column 3 population — major structural change), `ControlPlane.tsx` (replacement of bottom-bar with column-resident component), new `ControlPlaneForm1.tsx` / `ControlPlaneForm2.tsx` components, `ScenarioInstrumentCluster.tsx` (mode transition logic). This is the largest frontend change in M18. **Must not run concurrently with G3** (ScenarioInstrumentCluster overlap). Recommended: G4 → G3. G1 and G2 must complete before G4 opens if they touch InstrumentCluster.tsx — verify at sprint entry.

**Render optimization concern (#1217):** The 50.5ms local / >179ms CI-throttled vs. 100ms target gap (from EX-001) is in scope for G4. The Recharts memoization and lazy ControlPlane mounting (Issue #1217) must be addressed in the same G4 PR as the column restructuring — separate optimization-only PRs on a component being actively restructured create rebase risk.

### Computation Engine Agent — Backend dependency chain

**G1 backend (#1254):** Uncertainty banding engine exists from M5 (ADR-007). The M18 extension produces CI band data in the trajectory API response format. Dependency: the CI band output must be validated against the Zambia scenario before G1 exits — the Demo 7 Act 2 CI band claim ("confidence band on the number differential") must be computable from backend data, not hardcoded. Integration test in CI is required.

**G2 backend (#1255):** PSP decomposition requires extending `PoliticalEconomyModule` to expose which driver categories (governance, fiscal sustainability, external balance, social stability) contributed to the PSP change at each step. This is a backend-only change with a new JSON field on the PSP output. No dependency on G1.

**G3 backend (#1349):** The N=3 multi-scenario comparison API from M17 (#394) is the prerequisite. **Before G3 sprint entry is filed, verify that the M17 multi-scenario comparison endpoint is on `main` and working** — a backend integration test must confirm this. If the M17 endpoint has issues on `main`, they must be resolved before G3 begins. The distributional differential computation (poverty headcount delta across scenarios at each step) is new — not merely a frontend composition from existing endpoint output.

**G4 backend (control plane):** The `branch_from_step` computation (Mode 3 branching from a given step) exists in the current backend per the ControlPlane.tsx implementation. The new shock injection capability (Form 2 — injecting `ElectionShock`, `CurrencyAttack`, `CreditorDefection`, `GeopoliticalShock`, `NaturalDisaster`, `ContagionShock`) requires a new backend endpoint or extension of the existing Mode 3 branching endpoint. This is new scope — the shock taxonomy and API contract must be specified as part of ADR-019 before backend implementation begins.

**Critical path:** G1 backend (CI bands) and G2 backend (PSP decomposition) are independent and can run in parallel. G3 backend (comparison diff) depends on M17's comparison API being stable on main. G4 backend (shock injection) depends on ADR-019 specifying the shock API contract.

### DevSecOps Agent — Infrastructure and dependency review

**New dependencies:**
- G1 (#1254): No new Python or npm dependencies expected. Uncertainty banding uses existing statistical primitives (numpy already in requirements). ✅
- G2 (#1255): No new dependencies. PSP module extension uses existing architecture. ✅
- G3 (#1349): If a specialized comparison visualization is needed, assess at sprint entry. Existing Recharts primitives should be sufficient — no new npm dependency expected. ✅ (pending confirmation at sprint entry)
- G4 (control plane): No new npm dependencies — React form primitives and Recharts already present. ✅

**Output path coverage (NM-069 process improvement):**
- `backend/test-results/` appears as an untracked directory in the current git status. This path is not covered by `.gitignore` — it must be added. **Action: DS Agent to open `infra/m18-gitignore-backend-test-results` PR targeting `release/m18` to add `backend/test-results/` to `.gitignore` as the first action after `release/m18` is cut.** This is a pre-wave infrastructure prerequisite — all sprint groups must check this is merged before their test PRs open.
- `frontend/test-results/`, `frontend/playwright-report/`, `frontend/session-screenshots/` — already covered by `.gitignore` from NM-069 fix (PR #1346, merged M18 kickoff prep).

**CI/CD compatibility:**
- All groups operate within existing CI infrastructure (Python + Node, GitHub Actions free-tier). No new CI configuration required.
- Pre-push hook `.githooks/pre-push` is active for all contributors (PR #1346). Sprint entries must confirm hook is installed locally.

**Near-miss process improvements applicable from M17:**
- NM-069 (output path coverage) — DS infra lane action for `backend/test-results/` above
- NM-070 (pre-push gate) — hook confirmed active; all sprint entries verify local installation
- NM-071 (wave concurrency ceiling) — ceiling is 5 concurrent groups; M18 Wave 1 has 2 groups (G1, G2) — well within Standard tier

### Architect — ADR prerequisite confirmation

**G1 (#1254 — CI bands):** ADR-007 (synthetic data framework, ACCEPTED) is the methodology authority for CI band computation. ADR-017 (Zone 1A information architecture, ACCEPTED 2026-06-22) is the visual encoding authority — CI bands are a confidence overlay on Zone 1A trajectories and fall within ADR-017's §Decision table for framework × branch rendering. No new ADR required. **CLEAR.**

**G2 (#1255 — PSP decomposition):** ADR-015 (Model Legibility / Evidence Thread Architecture, ACCEPTED 2026-06-16) authorizes Zone 1D basis annotation and evidence threading. PSP driver decomposition is a Zone 1D content addition within the existing evidence thread model. No new ADR required. **CLEAR.**

**G3 (#1349 — counter-scenario comparison):** No ADR exists yet. The #1352 requirements phase must answer: does counter-scenario comparison introduce a new visual encoding pattern for Zone 1A (distributional diff overlay) not addressed by ADR-017? ADR-017 covers framework × entity × branch × mode — a "distributional differential" view is arguably a new encoding dimension. **Architect assesses at G3 sprint entry, after #1352 closes.** If a new ADR is required, it gates G3 implementation. If the encoding is derivable from ADR-017's existing authority (e.g., the differential is presented as a Zone 1B content extension rather than a new Zone 1A view), implementation proceeds without a new ADR. This determination must be explicit in the G3 sprint entry document. **BLOCKED pending GR close and Architect determination.**

**G4 (control plane column + #1217):** ADR-019 (ARCH-013, ASSIGNED) is required. May not be authored until Artifacts 2, 4, and 5 of the design package (#1356, #1358, #1359) are on record and EL has approved the scope decision (#1359). Must not be accepted without independent UX Designer sign-off in a separate EL-triggered session (Tier 1, NM-042 compliance). **BLOCKED pending GD design package completion.**

---

## Sprint Groups

| Group | Issues | Phase | Wave | Description |
|---|---|---|---|---|
| GD — Control Plane Design Package | #1354, #1355–#1361 | Four phases (see below) | Pre-wave | 7-artifact design package: current state audit → target spec → delta analysis → EL scope decision → ADR-019 → Journey updates. Artifacts 1 (#1355) and 3 (#1357) may begin immediately. Gates all Mode 2+Mode 3 control plane implementation. |
| GR — Requirements Phase for #1349 | #1352 | Single phase (design/requirements) | Pre-wave | UX Designer journey for counter-scenario comparison + Customer Agent Layer 3 for Personas 1, 2, 5 + BPO business requirements and user stories. Must close before G3 sprint entry is filed. May begin immediately. |
| G1 — CI Bands on Zone 1A | #1254 | Implementation | Wave 1 | CI band ribbons on trajectory curves; ADR-007 full implementation; backend uncertainty output extension; Zone 1A rendering. ADR prerequisite: ADR-007 + ADR-017 (both ACCEPTED). **CLEAR.** |
| G2 — PSP Driver Decomposition | #1255 | Implementation | Wave 1 | PSP dominant driver category exposed in Zone 1D; backend PoliticalEconomyModule extension. ADR prerequisite: ADR-015 (ACCEPTED). **CLEAR.** Runs in parallel with G1. |
| G3 — Counter-Scenario Comparison | #1349 | Implementation | Wave 2 | Distributional number differential with CI bands for Demo 7 Act 2; builds on M17 N=3 comparison API. ADR prerequisite: **TBD at sprint entry after GR closes.** Blocked until GR close and Architect determination. |
| G4 — Control Plane Column | #1217 + control plane impl | Implementation | Wave 2 | Mode 3 column populated in InstrumentCluster column 3 (replacing bottom-bar ControlPlane); Mode 2 scenario configuration surface; blue/orange visual system; shock taxonomy (Form 2); history list; render optimization (#1217). ADR prerequisite: ADR-019 — **BLOCKED until ADR-019 accepted.** Must complete before G3 if both Wave 2 groups are active (ScenarioInstrumentCluster conflict). |
| G5 — Demo 7 Readiness | #1422, #1238 (closed), NM-076 CODING_STANDARDS improvement | Implementation | Wave 3 (capacity-allowing) | Zone 3 auditability panel for DistributionalComparisonSummary (expand/collapse methodology detail — AC-1422-A through AC-1422-G). Sprint branch: `sprint/m18-g5`. Sprint journal: #1435. EL-approved 2026-06-28. CLOSED 2026-06-28 — integration PR #1443 MERGED. |
| G6 — Demo 7 Preparation | #1445 (demo prep issue), #843 reference | Implementation | Wave 4 (Demo prep) | Stakeholder walkthrough, screenshot brief, Step 5d mode evaluation, narrated spec (`demo-narrated.spec.ts`), five frames (1440×900 capture), Step 6b nine-agent internal review. Sprint branch: `sprint/m18-g6`. Sprint journal: #1475. CLOSED 2026-06-29 — Step 6b unanimous FAIL (9/9 agents; 7 CRITICAL, 9 HIGH, 6 MEDIUM, 2 LOW; DEMO-130–DEMO-153; issues #1459–#1474 filed). Integration PR #1479 → `release/m18`. |
| G7 — Demo 7 Continuation | #1459–#1474 (DEMO-130–DEMO-153 findings), #843 (exit gate) | Implementation | Wave 4 (continued) | Resolution of all Step 6b findings across five fix clusters: A (CI band geometry — `TrajectoryView.tsx` fill bug, DEMO-137/138/145), B (Zone 1B layout contract — sticky-bottom height budget failure), C (CohortImpactSection alert-only design — UX sign-off required), D (data pipeline — psp-driver-row + HCL bottom quintile key mismatch), E (capture/narration/label fixes). G7-0 root cause analysis doc precedes all fix intent documents. Sprint branch: `sprint/m18-g7` (to be cut after G6 integration PR merges). Sprint entry filed 2026-06-29 — pending EL approval. |

### GD Phase sequencing detail

```
GD Phase 1 (no sprint entry — may begin immediately after sprint plan EL approval):
  UX Designer / Architect: Artifact 1 (#1355) — current state audit
                           (InstrumentCluster.tsx column 3, ControlPlane.tsx, TrajectoryView.tsx gaps)
  Customer Agent: Artifact 3 (#1357) — Layer 3 assessment for Personas 2 (Lucas) and 5 (Aicha)
        │
        ↓ Artifact 1 complete
        │
GD Phase 2 (no sprint entry — after Artifact 1):
  UX Designer: Artifact 2 (#1356) — target state specification
               (full column vision for Mode 2 + Mode 3; blue/orange visual system; forms and history)
  Architect: Artifact 4 (#1358) — delta analysis and dependency map
             (gap between current and target; implementation sequencing; ADR-019 scope boundary)
        │
        ↓ Artifacts 2 and 4 complete
        │
GD Phase 3 (no sprint entry — EL gate):
  EL: Artifact 5 (#1359) — scope decision document
      (Mode 2 column scope; shock taxonomy in M18 vs. later; EX-001 EL disposition)
        │
        ↓ EL approves Artifact 5
        │
GD Phase 4 (no sprint entry — ADR authorship):
  Architect: Artifact 6 (#1360) — ADR-019: Control Plane Column
             (authored from Artifacts 2+4+5; Tier 1 — UX Designer independent sign-off in separate session)
  UX Designer: Artifact 7 (#1361) — Journey C update + Journey A GA-02 resolution
             (after ADR-019 scope is known)
        │
        ↓ ADR-019 accepted (separate UX Designer session for sign-off)
        │
G4 sprint entry opens — Mode 3 column implementation begins
```

### GR (Requirements) phase sequencing detail

```
GR (no sprint entry — may begin immediately):
  UX Designer: Journey for counter-scenario comparison
               (how does Eleni or Lucas compare two fiscal paths? zone layout? reading order?)
  Customer Agent: Layer 3 for Personas 1, 2, 5 on counter-scenario comparison need
  BPO: Business requirements and user stories from journey output
        │
        ↓ GR closes — all three artifacts on record
        │
G3 sprint entry:
  Architect determines: does #1349 require ADR-017 amendment? (→ BLOCKED_ADR)
                        or is it within ADR-017 existing scope? (→ CLEAR)
  Intent document filed from BPO user stories
  QA tests authored from acceptance criteria
  Implementation begins
```

### Wave structure diagram

```
Immediately (after EL sprint plan approval):
  GD Phase 1 — Artifacts 1 + 3 (current state audit + Customer Agent Layer 3)
  GR — #1352 requirements phase (UX journeys + Customer Agent + BPO)
  
        ↓ Artifact 1 complete → GD Phase 2
        
  GD Phase 2 — Artifacts 2 + 4 (target spec + delta analysis)
  
        ↓ Artifacts 2+4 → GD Phase 3
        
  GD Phase 3 — Artifact 5 (EL scope decision gate) ←── EL must approve before GD Phase 4

Wave 1 (after release branch cut + sprint plan EL approval; G1 and G2 in parallel):
  G1 — CI Bands #1254 ─────────────────────────────────┐
  G2 — PSP Decomposition #1255 ────────────────────────┤
  [GD Phase 4: ADR-019 authorship — runs alongside]    │
  [GR: continues toward close — runs alongside]        │
                                                        │
        ↓ G1 + G2 exit; ADR-019 accepted; GR complete  │
                                                        │
Wave 2 (after Wave 1 + gates):                          │
  G4 — Control Plane Column ───────────────────────────┤
  [G3 may open after GR close + Architect clearance —  │
   but not concurrently with G4 on ScenarioIC.tsx]     │
                                                        │
        ↓ G4 exits → G3 opens                          │
        ↓ G3 exits                                      │
                                                        │
Wave 3 (capacity-allowing; after G3 exits):             │
  G5 — Zone 3 Auditability #1422 ─────────────────────┤  ✅ CLOSED 2026-06-28
  (NM-076 CODING_STANDARDS improvement)                 │     Integration PR #1443 MERGED
                                                        │
        ↓ G5 exits                                      │
                                                        │
Wave 4 — Demo 7 Preparation and Continuation:           │
  G6 — Demo 7 Preparation (Steps 1–6b) ───────────────┤  ✅ CLOSED 2026-06-29
       walkthrough, screenshot brief, Step 5d,          │     Step 6b: unanimous FAIL
       narrated spec, five frames, Step 6b review       │     DEMO-130–DEMO-153 filed
       ↓ Step 6b FAIL → G7 opened                       │     Integration PR #1479 → release/m18
                                                        │
  G7 — Demo 7 Continuation ───────────────────────────┤  ⬜ ACTIVE — sprint entry pending EL approval
       G7-0 root cause analysis                         │     sprint/m18-g7 to cut after #1479 merges
       Cluster A: CI band geometry fix                  │
       Cluster B: Zone 1B layout fix                    │
       Cluster C: CohortImpactSection design            │
       Cluster D: data pipeline (psp-driver + HCL)     │
       Cluster E: capture/narration/label fixes         │
       ↓ Step 6b re-review PASS gate                    │
       Steps 7, 6c, 8, 9, 9b                            │
                                                        ├─► Demo 7 (#843)
        ↓ G7 exits                                      │
                                                        │
Demo 7 live session ────────────────────────────────────┘
        ↓ #843 complete
M18 Exit (#1340 closes)
```

**Wave 2 concurrency note (NM-071 compliance):** G4 and G3 must not have open implementation PRs simultaneously due to `ScenarioInstrumentCluster.tsx` conflict. G4 exits before G3 opens. If capacity allows G3 to begin before G4 exits, PM Agent must confirm that G3's implementation scope does not touch `ScenarioInstrumentCluster.tsx` before opening G3's sprint sub-branch.

---

## Wave 1 Entry Gate

**Wave 1 sprint entries may open when:**
1. This sprint plan is EL-approved (recorded in frontmatter or #1340 comment)
2. `release/m18` branch cut from main
3. DS Agent infra PR (`infra/m18-gitignore-backend-test-results`) merged to `release/m18`
4. Individual sprint entry documents filed and EL-approved per sprint entry template

G1 and G2 are immediately unblocked (no ADR prerequisites outstanding). They may open their sprint entries and sub-branches (`sprint/m18-g1`, `sprint/m18-g2`) as soon as conditions 1–3 above are confirmed.

---

## Wave 2 Entry Gates

**G4 (control plane) may open when:**
1. ADR-019 accepted (separate-session UX Designer sign-off obtained)
2. G1 and G2 have exited (to avoid InstrumentCluster.tsx conflicts)
3. G4 sprint entry document filed and EL-approved

**G3 (counter-scenario) may open when:**
1. GR close confirmed (all three artifacts on record: UX journey, Customer Agent Layer 3, BPO requirements)
2. Architect has determined ADR requirement (and ADR accepted if required)
3. Intent document filed from BPO user stories
4. QA tests authored from acceptance criteria
5. G4 has exited OR PM Agent confirms G3 scope does not touch ScenarioInstrumentCluster.tsx
6. G3 sprint entry document filed and EL-approved

---

## Wave 3 Entry Gate

**G5 (Zone 3 auditability) may open when:**
1. G3 has exited (distributional comparison summary is stable; G5 extends it)
2. G5 sprint entry document filed and EL-approved (filed 2026-06-28; EL-approved 2026-06-28 — PR #1436)
3. Intent document filed (filed 2026-06-28 — PR #1437)
4. QA tests authored (filed 2026-06-28 — PR #1438)

G5 is capacity-allowing and does not block Demo 7 scheduling. It improves the analytical scrutiny path for Persona 1 (Lucas) in Demo 7 Act 2 but is not on the critical path.

**G5 exit status:** ✅ CONFIRMED 2026-06-28 — integration PR #1443 MERGED to `release/m18`.

---

## Wave 4 Entry Gates

### G6 (Demo 7 Preparation)

**G6 entry conditions — all satisfied (CLOSED 2026-06-29):**
1. ✅ G5 exited — distributional comparison summary stable
2. ✅ G6 sprint entry filed and EL-approved (filed prior session)
3. ✅ Demo prep standard Steps 1–6b executed — walkthrough, screenshot brief, Step 5d mode evaluation, narrated spec, five frames, Step 6b nine-agent review
4. ✅ Step 6b gate verdict: unanimous FAIL — 7 CRITICAL, 9 HIGH, 6 MEDIUM, 2 LOW (DEMO-130–DEMO-153; issues #1459–#1474)

**G6 exit status:** Integration PR #1479 (`sprint/m18-g6` → `release/m18`) open with auto-merge. PI Agent confirmation checklist pending (6 conditions — `docs/process/sprint-plans/m18-g6-sprint-exit.md §6`).

### G7 (Demo 7 Continuation)

**G7 may open when:**
1. G6 integration PR #1479 merges to `release/m18` (auto-merge pending CI)
2. PI Agent confirms G6 exit (6-condition checklist in `m18-g6-sprint-exit.md §6`)
3. G7 sprint entry document EL-approved — filed 2026-06-29 at `docs/process/sprint-plans/m18-g7-sprint-entry.md`; **pending EL approval**
4. PM Agent cuts `sprint/m18-g7` from `release/m18` after G6 integration PR merges
5. PM Agent opens G7 sprint journal issue

**G7 pre-implementation sequencing:**
- G7-0 root cause analysis document filed and EL-reviewed — **must precede all fix intent documents**
- Architect + UX sign-off on clusters B (Zone 1B) and C (CohortImpactSection) — determines whether ADR-008 / ADR-010 amendments are required
- Per-cluster intent document → QA authorship → implementation (five clusters may not all run concurrently; see G7 entry `§4`)
- NM-079 filed at G7 entry (CI band fill geometry shipped G1 undetected; no unit test covers fill geometry calculation)

**G7 exit gate:** Step 6b re-review PASS (nine-agent panel) is required before Steps 7, 6c, 8, 9, 9b may proceed. North star test authored by BPO after live session #843 runs.

---

## Demo 7 Minimum Viable Readiness Checklist

Demo 7 (#843) schedules when all of the following are confirmed by PM Agent:

| Readiness condition | Source |
|---|---|
| Act 1: Mode 3 column populated with Form 1 (policy input) visible in InstrumentCluster column 3 | G4 exit |
| Act 1: Live A/B trajectory comparison visible on apply | G4 exit |
| Act 1: Causal attribution in Zone 1B for Mode 3 active | G4 exit or backend verification |
| Act 1: Senegal Article IV scenario runs in Mode 3 without EX-001 exceedance | G4 exit + MV-002 re-run |
| Act 2: Three Zambia scenarios loaded simultaneously with curve differentiation | M17 N=3 infrastructure (#394, on main) |
| Act 2: CI bands visible on Zone 1A trajectories | G1 exit |
| Act 2: PSP driver decomposition readable in Zone 1D | G2 exit |
| Act 2: Distributional differential number visible for comparison (minimum viable) | G3 exit or degraded mode |
| Demo script: Act 1 narrator narration + Act 2 narrator narration approved by BPO | Demo prep |

---

## Exit Conditions

M18 closes when all of the following are satisfied:

1. **G1 exit confirmed by PI Agent** — CI bands on Zone 1A; integration test in CI; BPO ACCEPT ✅ CONFIRMED 2026-06-28 (integration PR #1411 MERGED)
2. **G2 exit confirmed by PI Agent** — PSP decomposition in Zone 1D; BPO ACCEPT ✅ CONFIRMED 2026-06-28 (integration PR #1408 MERGED)
3. **G3 exit confirmed by PI Agent** — counter-scenario comparison; BPO ACCEPT; Customer Agent Layer 3 for Personas 1 + 5 ✅ CONFIRMED 2026-06-28 (integration PR #1417 MERGED)
4. **G4 exit confirmed by PI Agent** — control plane column populated (Mode 2 + Mode 3); #1217 render optimization; BPO ACCEPT; Customer Agent Layer 3 for Personas 2 + 5; EX-001 status resolved ✅ CONFIRMED 2026-06-28 (integration PR #1433 MERGED)
5. **North star test artifact on record** for G3 + G4: "The Senegalese Finance Minister's team can show that under proposed conditionality there is no fiscal instrument configuration that avoids the bottom quintile crossing the 0.40 floor — or, if a configuration exists, they can name it and cite the specific step at which the threshold is no longer crossed. The Zambian ministry can show the number differential between restructuring options with confidence bands." ✅ G3 + G4 north star on record; G7 north star filed by BPO after #843 runs.
6. **G5 exit confirmed by PI Agent** (capacity-allowing) — Zone 3 auditability panel (#1422); BPO ACCEPT; Customer Agent Layer 3 for Persona 1 ✅ CONFIRMED 2026-06-28 (integration PR #1443 MERGED)
7. **G6 exit confirmed by PI Agent** — demo prep artifacts through Step 6b FAIL gate; all DEMO-130–DEMO-153 findings documented; issues #1459–#1474 filed; integration PR #1479 merged ⬜ PI Agent confirmation checklist pending (`m18-g6-sprint-exit.md §6`)
8. **G7 exit confirmed by PI Agent** — all CRITICAL findings resolved or dispositioned; Step 6b nine-agent re-review PASS; Steps 7, 6c, 8 complete; BPO ACCEPT; Customer Agent Layer 3 for Personas 2, 3, 5; north star test filed after #843 runs ⬜ Pending G7 implementation
9. **Demo 7 live session complete** (#843 closed) — external participants attended; stakeholder review on record ⬜ Pending G7 completion
10. **PI Agent exit gate confirmation** recorded in the M18 sprint exit document ⬜ Pending
11. **#1340** (M18 Exit Checklist) closed ⬜ Pending

---

## Sprint Entry Gate Requirements

Per `docs/process/sprint-planning-sop.md §Sprint Entry Gate`, implementation may not begin on any sprint group until a sprint entry document is filed at `docs/process/sprint-plans/m18-{group}-sprint-entry.md` using the template at `docs/process/sprint-plans/templates/sprint-entry-template.md` and is EL-approved.

**GD exception:** No sprint entry required for design package phases (GD Phase 1–4). These are design work only — no implementation code. Artifacts are committed to `docs/` branches and filed via PRs targeting `release/m18`. The EL gate is Artifact 5 (#1359) approval.

**GR exception:** No sprint entry required for #1352 requirements phase. This is requirements capture only — UX journeys, Customer Agent consultation, BPO requirements. No implementation code. GR output is the sprint entry prerequisite for G3.

**G1 and G2 sprint entries:** May be filed simultaneously after this sprint plan is EL-approved and Wave 1 entry gate conditions are met (see above). Both are Standard tier (2 concurrent groups well within ceiling).

**G3 sprint entry:** Must cite GR as closed, Architect ADR determination as on record, intent document filed, and QA tests authored. The Architect determination on ADR requirement is a required field in the G3 sprint entry document.

**G4 sprint entry:** Must cite ADR-019 as accepted, G1 and G2 exits confirmed, intent document filed, and QA tests authored. EX-001 exception disposition must be recorded: either renewed with a new expiry target, or closed as resolved by G4 implementation.

---

## M18 Kickoff Sequence

1. ✅ EL merges `release/m17` → `main` — DONE 2026-06-26
2. ✅ PM Agent authors `m18-sprint-plan.md` — THIS DOCUMENT (2026-06-26)
3. ✅ EL approves sprint plan — PR #1364 merged 2026-06-26
4. ✅ PM Agent cuts `release/m18` from `main` — cut 2026-06-26 at commit 8cffc86 (sync PR #1366 merged)
5. ✅ DS Agent: `backend/test-results/` already in `.gitignore` (PR #1346 — no action needed)
6. ✅ G1 sprint entry filed and EL-approved 2026-06-26 (PR #1369; approval recorded in entry doc)
7. ✅ G2 sprint entry filed and EL-approved 2026-06-26 (PR #1369; approval recorded in entry doc)
8. ⬜ GD Phase 1 begins (Artifacts 1 + 3) — immediately after EL sprint plan approval
9. ⬜ GR begins (#1352) — immediately after EL sprint plan approval
10. ⬜ Wave 1 exit gates confirmed by PI Agent (G1, G2)
11. ⬜ GD Phase 3 (Artifact 5 EL gate) passed → GD Phase 4 → ADR-019 authored and accepted
12. ⬜ G4 sprint entry filed and EL-approved → Wave 2 G4 begins
13. ⬜ GR close confirmed → G3 Architect determination → G3 sprint entry → Wave 2 G3 begins
14. ⬜ Wave 2 exit gates confirmed by PI Agent (G4 before G3)
15. ✅ G5 sprint entry filed and EL-approved 2026-06-28 (PR #1436) — Wave 3 capacity-allowing group
16. ✅ G5 intent document filed 2026-06-28 (PR #1437)
17. ✅ G5 QA tests filed 2026-06-28 (PR #1438)
18. ✅ G5 implementation complete 2026-06-28 (#1422 — PR #1439 merged; #1238 verified closed)
19. ✅ G5 exit gate confirmed by PI Agent (#1422 BPO ACCEPT + CA L3 PASS — 2026-06-28; integration PR #1443 MERGED to `release/m18`)
20. ✅ G6 sprint entry filed and EL-approved (prior session, 2026-06-29) — Wave 4 Demo prep
21. ✅ G6 demo prep artifacts complete 2026-06-29 — walkthrough, screenshot brief, Step 5d docs, narrated spec, five frames (PR #1449/#1457/#1458/#1476 merged to `sprint/m18-g6`)
22. ✅ G6 Step 6b nine-agent internal review complete 2026-06-29 — unanimous FAIL; DEMO-130–DEMO-153; issues #1459–#1474 filed; PR #1478 → `sprint/m18-g6` (auto-merge)
23. ✅ G6 sprint exit document filed 2026-06-29 (`m18-g6-sprint-exit.md`); integration PR #1479 → `release/m18` (auto-merge)
24. ⬜ G6 exit gate confirmed by PI Agent — 6-condition checklist in `m18-g6-sprint-exit.md §6`
25. ⬜ G7 sprint entry EL-approved — entry filed 2026-06-29 at `m18-g7-sprint-entry.md`; **EL approval required before implementation begins**
26. ⬜ PM Agent cuts `sprint/m18-g7` from `release/m18` (after G6 integration PR #1479 merges); PM Agent opens G7 sprint journal issue
27. ⬜ G7-0 root cause analysis document filed and EL-reviewed (precedes all fix intent documents)
28. ⬜ G7 implementation — five fix clusters (A: CI band geometry, B: Zone 1B layout, C: CohortImpactSection, D: data pipeline, E: capture/narration); NM-079 filed at G7 entry
29. ⬜ G7 Step 6b re-review — nine-agent panel re-run; PASS gate required before Step 7 opens
30. ⬜ Demo 7 minimum viable readiness checklist confirmed → Demo 7 session scheduled
31. ⬜ Demo 7 live session complete (#843) → stakeholder review on record; north star test authored by BPO
32. ⬜ G7 exit gate confirmed by PI Agent → M18 sprint exit document filed
33. ⬜ PI Agent M18 exit gate confirmation → #1340 closes

---

## EL Approval Record

**EL approval:** 2026-06-26 (PR #1364 merged)

> Sprint plan approved. Wave structure (Pre-wave GD + GR → Wave 1 G1+G2 → Wave 2 G4→G3 → Demo 7) confirmed. ADR prerequisites clear. Release branch cut. Pre-wave phases (GD #1354 and GR #1352) may begin immediately. Wave 1 sprint entries (G1 and G2) may be filed — each requires separate EL approval before implementation PR opens.
> — @PublicEnemage (2026-06-26)
