# Exceptions Registry

Append-only. Each exception has a unique EX-NNN identifier.

An exception is a time-bounded, EL-approved deviation from a project specification,
threshold, architectural principle, or security requirement. Exceptions are not
permanent — every exception has an expiry condition. At expiry, the exception is either
resolved (specification restored), renewed (new EL decision required), or promoted to
a permanent specification change (which requires the same process as the original
specification).

**Types:** `threshold` | `architecture` | `security` | `process` | `data`

**Expiry discipline:** An exception that passes its expiry milestone without a renewal
or resolution decision is a compliance finding. File in `docs/compliance/scan-registry.md`
as a SCAN entry at the expired milestone's exit gate. The PI Agent holds R for flagging
expired exceptions at sprint exit.

---

## Exception Index

| ID | Type | Summary | Expiry | Status |
|---|---|---|---|---|
| EX-001 | threshold | AC-009 CI throttled render threshold raised 100ms → 200ms | G4 exit (ADR-019 §D-10) | Active |
| EX-002 | process | AC-A2 annotated with `test.fail()` during G3 pre-implementation window; CI passes while test is intentionally red | G3 Phase 3 implementation PR merged | Resolved 2026-06-28 |

---

## EX-001 — AC-009 CI throttled render threshold

**Type:** threshold
**Status:** Active
**EL Approved:** 2026-06-24
**Expiry:** M17 exit

At M17 sprint entry, this exception must be explicitly renewed (new EL decision,
new expiry) or resolved. An exception that reaches M17 exit without a decision is
a compliance finding — see expiry discipline above.

### Specification

`docs/frontend/fa-brief-m9-instrument-cluster.md §AC-009`:
AC-009 pass criterion: Mode 3 full component set render ≤ **100ms** on CI 4× throttled
profile.

### Approved Deviation

AC-009 CI throttled threshold raised to **200ms** for the duration of this exception.
The ProBook hardware validation target (MV-002, no throttle) remains ≤ 100ms —
this exception applies to the CI throttled gate only.

### Rationale

AC-009 silently skipped since Mode 3 shipped in M12 (NM-058 — wrong testid). When
corrected in M16-G6, the first real measurement produced **179ms** on the 4× throttled
CI runner. Chief Engineer assessment (2026-06-24):

- Browser-side performance marks are sound; 179ms is real (~40ms estimated at 1× speed)
- Mode 3 renders ~15 additional Recharts series elements on activation; ~40ms at 1× is
  not a usability problem for any target persona
- Threshold at 200ms (179ms + 21ms headroom) preserves regression sensitivity — any
  change that pushes past 200ms on 4× throttle represents a substantial regression
- Raising to 250ms or higher loses meaningful signal
- Genuine optimization (Recharts memoization, lazy ControlPlane mounting) is non-trivial
  and appropriate for a dedicated future sprint

### Baseline

| Measurement | Value | Environment | Date |
|---|---|---|---|
| First real AC-009 CI run (post NM-058 fix) | 179ms | GitHub Actions (ubuntu-latest, 2-core), 4× CPU throttle | 2026-06-24 |

### Linked Issue

Mode 3 render optimization enhancement issue: filed at M16-G6 exit.
Carries into M17 planning as a named obligation. If M17 exits without delivering the
optimization, a new EL decision is required to renew EX-001.

### Renewal / Resolution Conditions

At M17 sprint entry (or earlier if optimization is delivered mid-M17):

- **Resolve:** Mode 3 render optimization delivered and CI AC-009 passes at ≤ 100ms.
  Update Status to Resolved; add Resolution Record below.
- **Renew:** Optimization not delivered. New EL decision required with updated expiry.
  Renewal without a new EL decision is a process violation.
- **Promote:** If 200ms is confirmed as the correct specification (hardware measurements
  and CE assessment support it), file a permanent specification change via the FA brief
  amendment process and close this exception.

### M17 Status Update — 2026-06-25

**Action taken (EL direction):** AC-009 converted from `test()` to `test.fixme()` in
`frontend/tests/e2e/trajectory-view.spec.ts`. CI consistently returned 712ms–771ms vs the
200ms threshold on GHA 2-core shared runners — 3–4× above even the raised threshold.
The performance gate provides no CI signal at this runner tier.

**Authority:** EL direction 2026-06-25 during G2 sprint entry PR (#1289) CI review.
KI-006 filed (`docs/process/known-issues-registry.md`): external infrastructure limitation.
NM-064 filed (`docs/process/near-miss-registry.md`): test.fixme() authorized per NM-056.

**Expiry:** EX-001 expiry condition (M17 exit) unchanged. At M17 exit, EL to decide:
(a) remove AC-009 from the test suite and replace with a local developer gate, or
(b) convert to a Playwright `--trace` perf annotation (record without assert), or
(c) close as Won't Fix if Mode 3 render performance is confirmed acceptable by FE profiling.

### M18 Status Update — 2026-06-28

**EX-001 passed M17 exit without renewal or resolution — compliance finding would normally
apply (expiry discipline above). EL direction via ADR-019 §D-10 and G4 sprint entry
§EX-001 Pre-Implementation Condition provides the resolution path.**

ADR-019 §D-10 (accepted 2026-06-27, PR #1393) specifies the EX-001 resolution procedure
for G4 exit:

1. Implement Issue #1217 (Recharts memoization + lazy `ControlPlaneColumn` mounting) in
   the same PR as the column layout move (Dimension 1 of G4), before adding form content.
2. Run MV-002 profiling gate at G4 Dimension 1 implementation PR submission (local,
   unthrottled ProBook hardware); record measurement in PR description.
3. After G4 Dimension 3 CI merge: AC-009 `test.fixme()` behavior observed on CI runner.
   - If ≤ 200ms on CI: restore AC-009 from `test.fixme()` to `test()` at 100ms threshold.
     Close EX-001 as **Resolved**.
   - If > 200ms on CI (KI-006 infrastructure limitation persists): remove AC-009 from
     Playwright CI suite permanently; replace with local developer gate (`npm run test:perf`).
     Close EX-001 as **Won't Fix**.
4. AC-009 `test.fixme()` removed from CI permanently regardless of resolution label.
   Test structure preserved with comment referencing EX-001 closure record.

**Expiry condition updated:** G4 exit (ADR-019 §D-10). This supersedes the expired M17
exit condition. The resolution path is the active commitment. At G4 exit, PI Agent confirms
EX-001 closure record is present in this registry before exit gate passes.

**Authority:** EL-approved ADR-019 §D-10 (2026-06-27); G4 sprint entry §EX-001
Pre-Implementation Condition (EL-approved 2026-06-28).

---

## EX-002 — AC-A2 `test.fail()` pre-implementation annotation

**Type:** process
**Status:** Active
**EL Approved:** 2026-06-25
**Expiry:** G3 Phase 3 implementation PR merged (removing `test.fail()` is a required step in that PR)

### Specification

`docs/process/intents/M17-G3-2026-06-25-zone-1b-proportional-allocation.md §5 AC-A2`:
AC-A2 is a regression guard — it must be hard-fail (red) before G3 implementation and
hard-pass (green) after. The intent document §5 states: **"No soft-skip patterns (NM-056
guard): AC-A2 must be hard-fail. No `test.skip()`, `test.fixme()`, or conditional skips."**

### Approved Deviation

`test.fail()` applied to AC-A2 in `frontend/tests/e2e/m17-g3-zone-1b-allocation.spec.ts`
during the pre-G3-implementation window. CI treats the expected failure as a passing state;
CI will fail (correctly) when G3 Phase 3 adds `data-testid="zone-1b-mda-panel-wrapper"` and
AC-A2 unexpectedly passes, signalling the implementing engineer to remove `test.fail()`.

`test.fail()` is not a soft-skip. The test still runs and still must fail — the annotation
only prevents the pre-implementation red from blocking CI on the early-filed QA PR (#1290).
This is distinct from `test.skip()` and `test.fixme()` (which suppress execution entirely).
The NM-056 guard against soft-skip patterns is not violated.

### Rationale

PR #1290 (`chore/m17-g3-early-qa-filing`) filed the G3 regression guard test before G3 Phase 3
implementation, causing CI to block on the intentionally-red AC-A2. Previous pre-implementation
QA tests used early-return guards to stay green; AC-A2 opted out (by design — the whole point
is to confirm it's red before implementation). No SOP guidance existed for this case (NM-065).

EL direction 2026-06-25: annotate with `test.fail()`, file EX-002, file NM-065, document
reversal steps in the intent document.

### Testid reconciliation (same PR)

AC-A2 locator updated from `zone-1b-mda-panel` to `zone-1b-mda-panel-wrapper` (per ADR-018
and intent doc §5). The original testid in the early-filed test was a shorthand; the correct
ADR-018 testid is `zone-1b-mda-panel-wrapper`.

### Linked artifacts

- NM-065 (`docs/process/near-miss-registry.md`) — process gap: no SOP for intentionally-red pre-implementation tests
- PR #1290 (`chore/m17-g3-early-qa-filing`) — early QA test PR; AC-A2 is the failing test
- ADR-018 (`docs/adr/ADR-018-zone-1b-proportional-allocation.md`) — implementation contract specifying `zone-1b-mda-panel-wrapper` testid
- Intent doc §5 — AC-A2 specification and reversal steps

### Expiry and Resolution

**Expiry condition:** G3 Phase 3 implementation PR is merged.

**Resolution steps (required in the Phase 3 implementation PR):**
1. G3 Phase 3 adds `data-testid="zone-1b-mda-panel-wrapper"` to `InstrumentCluster.tsx`
2. Run playwright locally — AC-A2 passes (testid exists, height ≥ 80px)
3. Playwright reports "unexpected pass" because `test.fail()` is still present → CI would fail
4. Remove `test.fail()` and its comment from AC-A2 in `m17-g3-zone-1b-allocation.spec.ts`
5. Re-run playwright — AC-A2 passes cleanly
6. Push; update Status to Resolved in this registry

### Resolution Record — 2026-06-28

**Date:** 2026-06-28
**Resolution label:** Resolved
**Authority:** G3 sprint exit confirmation (sprint exit doc: `docs/process/sprint-plans/m18-g3-sprint-exit.md`; PI Agent confirmation on sprint journal #1377)

G3 Phase 3 implementation (PR #1407/#1412 merged to sprint/m18-g3; integration PR #1417 merged to release/m18 2026-06-28) delivered `data-testid="zone-1b-mda-panel-wrapper"` in `InstrumentCluster.tsx`. All five resolution steps confirmed:
- Step 1: `zone-1b-mda-panel-wrapper` testid added to `InstrumentCluster.tsx` (G3 Phase 3)
- Step 2: AC-A2 passes in G3 Playwright CI suite (integration PR #1417 playwright-e2e GREEN)
- Steps 3–4: `test.fail()` removed from AC-A2 in `m17-g3-zone-1b-allocation.spec.ts` during G3 Phase 3 (verified by grep — no `test.fail()` on test line 456 as of 2026-06-28)
- Step 5: AC-A2 passes cleanly (no `test.fail()` annotation present)
- Step 6: Status updated to Resolved in this registry

---

## Registry Maintenance

Exception entries are permanent — never delete or modify a closed entry.
When an exception is resolved or renewed, update **Status** in the index table and
append a **Resolution Record** or **Renewal Record** to the entry body (date, outcome,
approver).

Expiry ≠ resolution. An expired, unrenewed exception is a compliance finding.
