---
name: m18-g4-sprint-exit
type: sprint-exit
milestone: M18 — Full Argument and Demo 7
sprint-group: G4 — Control Plane Column + Render Optimization
status: Confirmed
authored-by: Business PO / PI Agent
date: 2026-06-28
pi-confirmed: true
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M18, G4: Control Plane Column + Render Optimization

**Status:** Confirmed — all exit conditions satisfied
**Date produced:** 2026-06-28
**Release branch:** `release/m18`
**Sprint entry document:** `docs/process/sprint-plans/m18-g4-sprint-entry.md` — EL Approved 2026-06-28

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
G4 delivers the Mode 3 control plane as a column-mounted component (ADR-019): `Mode2ColumnSurface`
(read-only scenario identity + "Enter Active Control" affordance in Mode 2) and `ControlPlaneColumn`
(Form 1 Policy Instruments + Form 2 Scenario Shocks in Mode 3). Lazy-mount optimization (#1217)
removes the Mode 1/2 Recharts render cost. Backend: `POST /api/v1/scenarios/{id}/inject-shock`
with 7 ShockHandler implementations; `BranchRequest` extended with `legitimacy_index`. EX-001
closed Won't Fix — MV-002 ProBook hardware gate PASS (67.40/85.50/64.40ms, all ≤ 100ms); AC-009
`test.fixme()` removed from CI permanently. Demo 7 Act 1 minimum viable demo is now executable:
Form 1 apply triggers a counter-trajectory branch in Zone 1A simultaneously with the column —
no scroll required at 1280×800.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| Sprint group | G4 — Control Plane Column + Render Optimization (Wave 2) |
| Release branch | `release/m18` |
| Sprint entry document | `docs/process/sprint-plans/m18-g4-sprint-entry.md` |
| Exit checklist issue | #1340 |
| Sprint journal issue | #1402 |
| Date implementation completed | 2026-06-28 (PR #1432 merged to `sprint/m18-g4`) |
| CI status on sprint branch | Green — playwright-e2e PASS, test-backend PASS, lint PASS, compliance-scan PASS, branch-naming PASS; backtesting SKIPPED (confirmed at PR #1432) |

---

## Section 2 — Implementation Status

| PR | Title | Merged? | CI status | Notes |
|---|---|---|---|---|
| #1418 | `test(m18-g4): author QA tests — AC-G4-A through AC-G4-I` | ✅ Yes | Green | QA tests authored before implementation per entry §2.4 (NM-055 compliant): `frontend/tests/e2e/m18-g4-control-plane-column.spec.ts`, `backend/tests/test_m18_g4_shock_injection.py` |
| #1421 | `docs(m18-g4): file G4 intent document — control plane column` | ✅ Yes | Green | Intent document: `docs/process/intents/M18-G4-2026-06-28-control-plane-column.md` — filed before implementation PR per entry §2.3 |
| #1424 | `feat(m18-g4): control plane column — Dimension 1+2+3 (ADR-019)` | ✅ Yes | playwright-e2e FAIL (fixed by #1426 — NM-076) | All three dimensions delivered: lazy-mount + Mode2ColumnSurface + ControlPlaneColumn (Forms 1+2 + 7 shocks) + backend endpoint + schema docs. playwright-e2e failed due to pre-G4 testid renames (ADR-019 D-3) not crosschecked before merge — see NM-076. |
| #1426 | `fix(m18-g4): update pre-G4 E2E tests broken by ADR-019 D-3 testid renames` | ✅ Yes | Green | Fixes 3 broken E2E tests from NM-076: `apply-control-change` → `apply-policy-input`; `fiscal-multiplier-slider` → `policy-param-slider`; Customer Agent L3 assessment filed in same PR |
| #1429 | `fix(m18-g4): add branch-anchor-label to ControlPlaneColumn` | ✅ Yes | Green | Adds `data-testid="branch-anchor-label"` missing from initial Dimension 1 implementation |
| #1432 | `fix(m18-g4): remove AC-009 test.fixme — EX-001 closed Won't Fix` | ✅ Yes | Green — playwright-e2e PASS 9m29s | EX-001 closure: AC-009 `test.fixme()` removed; test structure preserved as comment referencing EX-001 closure record; MV-002 measurements on record in `docs/compliance/exceptions.md §EX-001` |

**Implementation status:** All six PRs merged 2026-06-28 to `sprint/m18-g4`. CI green on sprint branch at PR #1432 — playwright-e2e PASS (9m29s), test-backend PASS (37s), lint PASS (46s), compliance-scan PASS (10s), branch-naming PASS, changes PASS, session-state-size-check PASS. backtesting SKIPPED (no backtesting changes). QA tests authored in PR #1418 before implementation (PR #1424) — entry §2.4 requirement satisfied.

**Files changed across G4 PRs:**
- `frontend/src/components/InstrumentCluster.tsx` — `controlPlane?: React.ReactNode` prop; renders in `data-testid="zone-control-plane"` div
- `frontend/src/components/ScenarioInstrumentCluster.tsx` — slot management: Mode 1 → undefined; Mode 2 → `<Mode2ColumnSurface />`; Mode 3 → `<ControlPlaneColumn />`
- `frontend/src/components/ControlPlane.tsx` → `ControlPlaneColumn.tsx` — renamed; lazy-mount (mounted on Mode 3 entry, unmounted on exit; addresses #1217 Recharts render cost in Mode 1/2)
- `frontend/src/components/Mode2ColumnSurface.tsx` (new) — scenario identity block (name, entity, calibration vintage, step range) + "Enter Active Control" button; subdued visual treatment (slate-50 background, slate-400 dashed border)
- `ControlPlaneColumn.tsx` Form 1 — FiscalMultiplier slider (0.1–3.0, step 0.05) + LegitimacyConstraint numeric input; `data-testid="policy-input-type-selector"`, `data-testid="apply-policy-input"`; branch_from_step selector; policy events history (`data-testid="policy-events-history"`)
- `ControlPlaneColumn.tsx` Form 2 — 7 shock types (GrowthShock, ElectionShock, CurrencyAttack, CreditorDefection, GeopoliticalShock, NaturalDisaster, ContagionShock); `data-testid="shock-type-selector"`, `data-testid="inject-scenario-shock"`; injected shocks history (`data-testid="shock-events-history"`); GrowthShock → `distribution_asymmetry` parameter input
- `backend/app/api/scenarios.py` — `POST /api/v1/scenarios/{id}/inject-shock` endpoint; `ShockInjectRequest` discriminated union; `ShockEffect` protocol; handler registry; 7 `ShockHandler` implementations
- `backend/app/schemas.py` — `BranchRequest` extended with `legitimacy_index` field
- `docs/schema/api_contracts.yml` — inject-shock endpoint shape added (mandatory pre-implementation per CLAUDE.md §Schema registry)
- `docs/schema/simulation_state.yml` — `BranchRequest.legitimacy_index` field added (same PR as BranchRequest backend extension)
- `docs/compliance/exceptions.md §EX-001` — closure record added (Won't Fix, 2026-06-28; MV-002 measurements; AC-009 disposition)
- `frontend/tests/e2e/m18-g4-control-plane-column.spec.ts` — AC-G4-A through AC-G4-I; AC-009 test structure
- `backend/tests/test_m18_g4_shock_injection.py` — shock injection backend tests; BranchRequest extension test

**Pre-push gate confirmation:** ruff clean, mypy clean, tsc clean, vite build clean — confirmed per `.githooks/pre-push` at each push.

**EX-001 closure record (named G4 deliverable per entry §3.1):**

MV-002 ProBook hardware gate: PASS. Three unthrottled runs — 67.40ms / 85.50ms / 64.40ms — all ≤ 100ms. Resolution label: Won't Fix (CI throttled measurement remains infeasible on GHA 2-core shared runners per KI-006 — external infrastructure limitation; no application-level fix is possible). AC-009 `test.fixme()` removed from CI permanently (PR #1432). Test structure preserved as comment in `frontend/tests/e2e/trajectory-view.spec.ts` referencing EX-001 closure record. Full closure record in `docs/compliance/exceptions.md §EX-001`.

**NM-076 (filed during G4 implementation):**

G4 testid renames (ADR-019 D-3: `apply-control-change` → `apply-policy-input`, `fiscal-multiplier-slider` → `policy-param-slider`) were not crosschecked against the E2E corpus before PR #1424 merged to `sprint/m18-g4`. Three tests merged broken. sprint-branch-ci-gate does not require playwright-e2e, so auto-merge fired. Fixed by PR #1426. Process improvement: testid rename rule to be added to `docs/CODING_STANDARDS.md`. Filed in `docs/process/near-miss-registry.md §NM-076`.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| Control plane column — Mode2ColumnSurface + ControlPlaneColumn + Form 1 + Form 2 + 7 shocks + backend inject-shock endpoint + BranchRequest extension + EX-001 closure | Frontend + Backend | PASS — Persona 2 (Eleni) and Persona 5 (Aicha). Filed in PR #1426 (before unconditional BPO verdict). | **ACCEPT** (full, unconditional) 2026-06-28 | #1402#issuecomment-4827376554 (full ACCEPT); #1402#issuecomment-4827099333 (conditional ACCEPT, EX-001 condition lifted) |

**Business PO acceptance status:** Full ACCEPT. No open rejections. EX-001 condition lifted — EX-001 closed Won't Fix 2026-06-28 (PR #1432 MERGED).

---

### Customer Agent Layer 3 Assessment

*G4 serves Persona 2 (Eleni Papadimitriou — Finance Ministry Negotiator) and Persona 5 (Aicha Mbaye — Finance Minister) as primary users.
Customer Agent Layer 3 assessment filed in PR #1426 before BPO unconditional verdict per acceptance-protocol.md §1.1.
Filed: `docs/customer/CA-L3-m18-g4-control-plane-column.md`; date: 2026-06-28.*

**Summary verdicts (from filed CA L3 assessment):**

| Persona | Gate | Verdict |
|---|---|---|
| Persona 2 (Eleni — Finance Ministry Negotiator) | 90-second gate | **PASS** |
| Persona 5 (Aicha Mbaye — Finance Minister) | 5-minute gate | **PASS** |

**Persona 2 (Eleni) — PASS, no conditions:**
- "Enter Active Control" label is self-interpreting (kryptonite constraint: no mode identifier — CLEAR)
- FiscalMultiplier and LegitimacyConstraint are domain terms Eleni commands without mediation
- Branch trajectory in Zone 1A is simultaneous with Form 1 Apply — no scroll at 1280×800
- 90-second Active Negotiation ceiling: PASS

**Persona 5 (Aicha) — PASS with notation:**
- Simultaneous column action + Zone 1A consequence satisfies the Demonstrative demonstration format
- Form 1/Form 2 parameter labels (FiscalMultiplier, LegitimacyConstraint, distribution_asymmetry) require analyst narration in Demo 7 — appropriate for Persona 5's Demonstrative entry state, not a defect
- Notation on record for Demo 7 presenter script

**Overall Layer 3 assessment: PASS (both primary personas). Filed before BPO verdict — protocol satisfied.**

---

### BPO Verdict — G4 Control Plane Column

*Assessed per acceptance-protocol.md §1.1 (Frontend Feature + Backend Extension).
Conditional ACCEPT filed 2026-06-28 at #1402#issuecomment-4827099333 (condition: EX-001 closure).
Full ACCEPT filed 2026-06-28 at #1402#issuecomment-4827376554 (condition lifted — EX-001 closed Won't Fix).*

**Observable state confirmed:**

1. `Mode2ColumnSurface` in `ScenarioInstrumentCluster.tsx` slot for Mode 2: renders scenario identity block
   (scenario name, entity, calibration vintage, step range) and `data-testid="enter-active-control"` button.
   Visual treatment: slate-50 background, slate-400 dashed border. Visible at 1280×800 without scroll.

2. `ControlPlaneColumn` in `ScenarioInstrumentCluster.tsx` slot for Mode 3: lazy-mounted on Mode 3 entry,
   unmounted on exit (addresses #1217 — Recharts components do not render in Mode 1/2).

3. Form 1 (Policy Instruments, blue `#0284c7`): `data-testid="policy-input-type-selector"` present in
   Mode 3; FiscalMultiplier selection reveals slider (0.1–3.0, step 0.05, `data-testid="policy-param-slider"`);
   LegitimacyConstraint selection reveals numeric input; `data-testid="apply-policy-input"` triggers
   `PUT /api/v1/scenarios/{id}/branch` with extended BranchRequest; counter-trajectory branch appears
   in Zone 1A simultaneously with baseline without scroll.

4. Form 2 (Scenario Shocks, orange `#ea580c`): `data-testid="shock-type-selector"` lists all 7 types
   (GrowthShock, ElectionShock, CurrencyAttack, CreditorDefection, GeopoliticalShock, NaturalDisaster,
   ContagionShock); GrowthShock selection reveals `distribution_asymmetry` parameter input;
   `data-testid="inject-scenario-shock"` fires `POST /api/v1/scenarios/{id}/inject-shock`;
   `data-testid="shock-events-history"` shows injected shock entry (type + step) after injection.

5. Both form headers visible without scroll at 1280×800 (entry §2.3 Artifact 3 Q3 requirement satisfied).

6. Backend: `POST /api/v1/scenarios/{id}/inject-shock` endpoint; `ShockInjectRequest` discriminated union;
   all 7 `ShockHandler` implementations; `ShockEffect` protocol; handler registry; 422 on invalid `shock_type`.
   `BranchRequest` extended with `legitimacy_index` — `PUT /api/v1/scenarios/{id}/branch` returns 200 for
   Senegal fixture with legitimacy constraint applied.

7. Schema docs: `api_contracts.yml` updated with inject-shock endpoint shape (mandatory pre-implementation
   per CLAUDE.md §Schema registry — confirmed in same PR as backend implementation, PR #1424).
   `simulation_state.yml` updated with `BranchRequest.legitimacy_index` in same PR.

8. QA tests: `frontend/tests/e2e/m18-g4-control-plane-column.spec.ts` (AC-G4-A through AC-G4-I) and
   `backend/tests/test_m18_g4_shock_injection.py` authored in PR #1418 before implementation (PR #1424) —
   entry §2.4 satisfied. All tests pass in CI (playwright-e2e PASS at PR #1432; test-backend PASS throughout).

9. EX-001 delivered: AC-009 `test.fixme()` removed (PR #1432); test structure preserved with comment.
   MV-002 measurements on record: 67.40/85.50/64.40ms — all ≤ 100ms on ProBook local hardware.

**Kryptonite check (Persona 5 — Aicha):** "Enter Active Control" button label contains no mode
identifier ("Mode 3") — kryptonite constraint satisfied. Form parameter labels (FiscalMultiplier,
LegitimacyConstraint) require analyst narration in Demo 7; this is appropriate for Demonstrative
entry state. The action → consequence link (Form 1 apply → Zone 1A branch trajectory appears
simultaneously) is visible without scroll or navigation. Kryptonite check: PASS.

> VALIDATED — 2026-06-28. Mode2ColumnSurface: scenario identity block + "Enter Active Control"
> (`data-testid="enter-active-control"`) visible at 1280×800 Mode 2 without scroll; slate-50/slate-400
> visual treatment. ControlPlaneColumn: lazy-mounted in Mode 3; Form 1 FiscalMultiplier slider
> (`data-testid="policy-param-slider"`, 0.1–3.0 step 0.05) + LegitimacyConstraint numeric input;
> `data-testid="apply-policy-input"` triggers Zone 1A counter-trajectory branch simultaneously
> visible without scroll. Form 2: 7 shock types via `data-testid="shock-type-selector"`;
> `data-testid="inject-scenario-shock"` fires inject-shock endpoint; `data-testid="shock-events-history"`
> confirms entry. Backend: all 7 ShockHandlers registered; discriminated union validates at 422 on
> invalid type; BranchRequest.legitimacy_index accepted. Schema docs updated in same PRs as
> implementation (CLAUDE.md §Schema registry compliance). EX-001 closed Won't Fix — MV-002
> 67.40/85.50/64.40ms ≤ 100ms; AC-009 test.fixme removed (PR #1432 CI: playwright-e2e PASS 9m29s).
>
> CA L3 PASS — Persona 2 (Eleni): 90-second ceiling, FiscalMultiplier/LegitimacyConstraint
> domain-native, simultaneous Zone 1A visibility; PASS. Persona 5 (Aicha): 5-minute Demonstrative
> gate; parameter labels require analyst narration (appropriate); PASS with notation for Demo 7
> presenter script.
>
> Verdict: **ACCEPT** — full, unconditional (EX-001 condition lifted 2026-06-28).

---

### North Star Test Artifact

*Required for user-facing deliverables per CLAUDE.md §North Star Test (Process Gate).
Authored by Business PO; filed before sprint exit gate per CLAUDE.md §North Star Test process home.*

**North star question:** Does this decision make the tool more useful to a finance minister
sitting across from an IMF negotiating team, in that moment?

**Finance minister scenario:** A Senegalese Finance Ministry analyst is preparing for an IMF
Article IV consultation. The IMF's proposed conditionality package includes fiscal multiplier
assumptions the Ministry disputes. The Ministry team needs to demonstrate at the table that
no fiscal multiplier configuration between 0.5 and 2.0 avoids the bottom quintile income
index crossing the 0.40 floor before step 6 — or, if a configuration exists, to name it and
cite the step at which the threshold is no longer crossed.

**Capability evaluated:** `ControlPlaneColumn` Form 1 — FiscalMultiplier slider + "Apply policy
instrument" → Zone 1A counter-trajectory branch (simultaneous visibility, no scroll at 1280×800).

**Does this capability change what the Ministry's team can argue at the table?**

**YES — specifically and measurably.**

Before G4: The control plane was a bottom-bar element. Applying a policy instrument required
scrolling away from Zone 1A to interact with the bottom bar, then scrolling back to see the
trajectory result. Simultaneous visibility of the control input and the Zone 1A consequence was
not possible at 1280×800. In a live negotiating session, this is not a usable workflow — the
analyst cannot iterate policy configurations while maintaining eye contact with the trajectory view.

After G4: The analyst enters Active Control, iterates FiscalMultiplier via Form 1 in the column
(right-hand panel), and observes the counter-trajectory branch appear in Zone 1A simultaneously
with the baseline — no scroll, no navigation, no context switch. The argument "your proposed
multiplier 1.5 produces a bottom-quintile crossing at step 4 under our calibration, while multiplier
0.8 avoids the crossing — but the IMF's own growth assumptions require multiplier ≥ 1.2" is now
demonstrable live, in the room, with the IMF team watching the trajectory respond to each slider
position.

This is a capability that did not exist before G4. The simultaneous-visibility property is the
Demo 7 Act 1 claim. It is not an incremental improvement — it is the difference between a
demonstration that can be run live and one that cannot.

**North star test verdict: PASS.** The capability changes what the Senegalese Ministry analyst
can argue at the table — from "the model says the threshold is crossed" (which requires accepting
the model output passively) to "under your multiplier assumption, the threshold is crossed at step 4;
under our calibration, it is not crossed at multiplier 0.8" (which is an interactive, session-specific
demonstration the IMF must engage with, not dismiss).

---

## Section 4 — Open Rejections

No open rejections. Full ACCEPT verdict on record (Section 3). No REJECT verdicts issued in G4.

**NM-076 (implementation correction — not a sprint rejection):**
Three E2E tests merged broken to `sprint/m18-g4` via PR #1424 (testid renames not crosschecked
before PR was opened). Caught by post-merge CI (playwright-e2e failure triggered ci-failure-notify.yml).
Fixed in same sprint by PR #1426 before any EL review occurred. This is an implementation correction,
not a sprint rejection — the issue was caught within the sprint before integration. NM-076 filed in
`docs/process/near-miss-registry.md`. No REJECT artifact required; no sprint-level REJECT issued.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] **All implementation PRs merged; CI green on sprint branch (Section 2)**
  PRs #1418 + #1421 + #1424 + #1426 + #1429 + #1432 merged 2026-06-28 to `sprint/m18-g4`.
  CI green at final state (PR #1432): playwright-e2e PASS (9m29s), test-backend PASS (37s),
  lint PASS (46s), compliance-scan PASS (10s), branch-naming PASS, changes PASS.
  QA tests authored in PR #1418 before implementation PR #1424 (entry §2.4 — NM-055 compliant).

- [x] **Business PO ACCEPT verdict filed for each user-facing deliverable (Section 3)**
  Control plane column (Mode2ColumnSurface + ControlPlaneColumn + Form 1 + Form 2 + 7 shocks +
  backend inject-shock + BranchRequest extension + EX-001 closure): ACCEPT — full, unconditional.
  Filed 2026-06-28 at #1402#issuecomment-4827376554. Condition (EX-001 closure) confirmed lifted.

- [x] **Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables (Section 3)**
  G4 serves Persona 2 (Eleni) and Persona 5 (Aicha).
  CA L3 assessment filed in PR #1426 and recorded at #1402#issuecomment-4827097745 —
  before the unconditional BPO ACCEPT at #1402#issuecomment-4827376554. Protocol satisfied.
  Persona 2 (Eleni): PASS — 90-second ceiling, domain-native parameters, simultaneous Zone 1A visibility.
  Persona 5 (Aicha): PASS — Demonstrative gate, analyst narration appropriate for entry state; notation
  on record for Demo 7 presenter script (not a defect).

- [x] **No open rejection artifacts (Section 4)**
  No REJECT verdicts issued in G4. NM-076 is an implementation correction caught within the sprint —
  not a sprint rejection. Fixed by PR #1426 before integration.

- [x] **Near-miss entry filed for each rejection (Section 4)**
  N/A — no sprint rejections. NM-076 filed for testid rename process gap (implementation correction
  catch by CI, not a rejection artifact).

- [x] **North star test artifact on record (Section 3)**
  Filed in Section 3. Finance minister scenario: Senegalese Finance Ministry in IMF Article IV
  consultation; analyst iterates FiscalMultiplier in Form 1 column; Zone 1A shows counter-trajectory
  branch simultaneously with baseline without scroll. Ministry can demonstrate "under your multiplier
  assumption, threshold crossed at step 4; under ours, not crossed at 0.8" live in the room.
  PASS — specific capability, specific scenario, specific argument changed at the negotiating table.

- [x] **EX-001 closed and closure record on file (named G4 deliverable per entry §3.1)**
  Won't Fix. MV-002 hardware gate PASS (67.40/85.50/64.40ms ≤ 100ms). AC-009 test.fixme removed.
  Closure record in `docs/compliance/exceptions.md §EX-001`. PR #1432 MERGED 2026-06-28T20:48:02Z.

**G3 concurrent overlap determination (entry §6.4 dependency 2):**
Entry §6.4 required PM Agent to confirm at G4 exit that G3 did not incidentally write to
`ScenarioInstrumentCluster.tsx`. Confirmed: G3 implementation (PRs #1395, #1398, #1407, #1412)
wrote to `MDAAlertPanelZone1B.tsx`, `backend/app/api/scenarios.py`, `backend/app/schemas.py`,
`frontend/src/store/scenarioStepStore.ts`, `frontend/src/App.tsx`, and `docs/schema/api_contracts.yml`.
No G3 writes to `ScenarioInstrumentCluster.tsx`. Concurrent isolation confirmed — no conflict at
integration time.

**PI Agent sprint exit verdict: CONFIRMED — all exit conditions satisfied**

**PI Agent confirmation:**

> G4 sprint exit conditions are satisfied as of 2026-06-28. The control plane column (Mode2ColumnSurface
> + ControlPlaneColumn, ADR-019) and render optimization (#1217) are delivered via PRs
> #1418/#1421/#1424/#1426/#1429/#1432, all merged 2026-06-28 to `sprint/m18-g4`. CI is green at
> final sprint state — playwright-e2e PASS (9m29s) confirmed at PR #1432.
>
> Business PO ACCEPT on record — full, unconditional — at #1402#issuecomment-4827376554 (2026-06-28).
> EX-001 condition lifted: EX-001 closed Won't Fix, closure record in `docs/compliance/exceptions.md §EX-001`.
> MV-002 hardware gate PASS: 67.40/85.50/64.40ms, all ≤ 100ms on ProBook local hardware.
>
> Customer Agent Layer 3 assessment on record at `docs/customer/CA-L3-m18-g4-control-plane-column.md`
> and #1402#issuecomment-4827097745 — filed before BPO unconditional verdict. Persona 2 (Eleni): PASS,
> 90-second gate. Persona 5 (Aicha): PASS, Demonstrative gate with Demo 7 presenter script notation.
>
> North star test artifact on record and specific: Senegalese Finance Ministry analyst in IMF Article IV
> consultation. Form 1 FiscalMultiplier slider + simultaneous Zone 1A counter-trajectory branch — no scroll
> at 1280×800. Ministry can demonstrate "under your multiplier assumption, threshold crossed step 4; under
> ours, not crossed at 0.8" live in the room with IMF team. PASS — specific scenario, specific capability,
> specific argument changed at the negotiating table.
>
> Step 4 Verify source code checks:
> - `Mode2ColumnSurface`: scenario identity + "Enter Active Control" (`data-testid="enter-active-control"`)
> - `ControlPlaneColumn`: lazy-mounted on Mode 3 entry/exit; `data-testid="zone-control-plane"` in `InstrumentCluster`
> - Form 1: `data-testid="policy-input-type-selector"`, `data-testid="policy-param-slider"` (0.1–3.0, step 0.05), `data-testid="apply-policy-input"`
> - Form 2: `data-testid="shock-type-selector"` (7 types), `data-testid="inject-scenario-shock"`, `data-testid="shock-events-history"`
> - Backend: `ShockHandler` protocol; registry with 7 handlers; `ShockInjectRequest` discriminated union; 422 on invalid `shock_type`
> - `BranchRequest.legitimacy_index` in `schemas.py` + `simulation_state.yml`
> - `api_contracts.yml` inject-shock endpoint shape added in same PR as backend implementation
> - EX-001 closure: AC-009 test.fixme() removed; test structure preserved as comment; MV-002 measurements on record
> - NM-076: testid rename crosscheck gap filed; fix confirmed in PR #1426 before integration
>
> No open REJECT verdicts. No open rejection artifacts. G3 concurrent isolation confirmed: no G3 writes
> to `ScenarioInstrumentCluster.tsx` at integration time.
>
> Integration PR `sprint/m18-g4` → `release/m18` may now open. PI Agent gate comment required on
> integration PR before auto-merge is set.
>
> **G4 is CLOSED as of 2026-06-28.**
>
> — PI Agent, 2026-06-28

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for M18-G4. It supersedes any informal exit notation
in `SESSION_STATE.md` for this sprint. It is filed at
`docs/process/sprint-plans/m18-g4-sprint-exit.md`.

The PI Agent confirmation in Section 5 is the gate. G4 is closed as of 2026-06-28.

**Downstream gate:** Integration PR `sprint/m18-g4` → `release/m18` may be opened immediately.
PI Agent gate comment is required on the integration PR before auto-merge is set.
Demo 7 scheduling is unblocked — G4 PI Agent exit confirmation is on record.
