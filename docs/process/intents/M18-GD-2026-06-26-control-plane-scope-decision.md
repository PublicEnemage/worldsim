---
name: M18-GD-control-plane-scope-decision
type: scope-decision-document
artifact: "Artifact 5 — GD Design Package (#1359)"
issues:
  - "#1359 — Artifact 5: Scope Decision Document (EL gate)"
  - "#1354 — Control Plane Design Package (parent)"
status: "Filed — awaiting EL approval"
authored-by: PM Agent
authored-date: 2026-06-26
el-approved: ""
release-branch: release/m18
gd-phase: "Phase 3 — filed after Artifacts 2 (#1356) and 4 (#1358)"
downstream-unblock:
  - "ADR-019 authorship (Architect Agent, #1360) — may not begin until this document is EL-approved"
  - "G4 sprint entry (Wave 2 implementation) — may not be filed until ADR-019 is accepted"
sprint-entry-reference: "docs/process/sprint-plans/m18-gd-sprint-entry.md (EL-approved 2026-06-26)"
---

# Artifact 5 — Control Plane Scope Decision Document

**GD Phase 3 gate.** This document records three EL decisions required before ADR-019
may be authored. It is filed in the intents directory by convention (per
`docs/process/sprint-plans/m18-gd-sprint-entry.md §2.3`) — it is not an
implementation intent. The agent-execution-lifecycle Step 1 obligation does not apply.

**EL approval of this document is the binding GD gate.** ADR-019 authorship begins
immediately after EL approves. No G4 sprint entry may be filed until ADR-019 is accepted.

---

## Decision 1 — Mode 2 Column 3 Scope in M18

**Question:** In M18, should InstrumentCluster column 3 be populated in Mode 2, or remain
the empty reserved zone specified in `docs/ux/information-hierarchy.md §Control Plane
Reserved Zone`?

**Background:** The information hierarchy (M9 governing premise 5) specifies that column 3
is empty-reserved in Mode 1 and Mode 2, and populated with the control plane in Mode 3.
The M18 sprint plan names a "Mode 2 scenario configuration surface" as a G4 deliverable.
This is a departure from the M9 spec and requires an explicit EL scope decision before
ADR-019 can record the Mode 2 column intent.

**Draft recommendation (PM Agent):** Populate Mode 2 column 3 with a minimal scenario
configuration surface. Content:

1. **Active scenario summary** — scenario name, entity, loaded calibration vintage, run
   horizon (start step / end step). Read-only; this tells the analyst what is loaded
   before they commit to Mode 3.
2. **Mode 3 activation control** — a single "Enter Mode 3" affordance with a brief
   caution: "Mode 3 branching cannot be undone — return to Mode 2 resets the active
   branch." This is the primary reason to populate Mode 2 column 3: Demo 7 Act 1
   requires a visible, intentional transition to Mode 3; the current bottom-bar
   ControlPlane has no such affordance.
3. **Reserved zone visual treatment** — the Mode 2 column should visually signal
   "this zone becomes active in Mode 3" — e.g., a reduced-opacity label or a blue/orange
   mode indicator. The populated-but-read-only state is deliberate; no editable fields
   in Mode 2 column 3 in M18.

**What this is not:** Mode 2 column 3 is not a scenario configuration editor in M18.
Scenario parameter adjustment (initial conditions, structural assumptions, calibration
overrides) is out of scope. The surface is read-only summary + mode transition. A richer
scenario configuration surface is a future milestone scope item.

**Governing document update required (ADR-019 / Artifact 2):** The information hierarchy
§Control Plane Reserved Zone must be updated by ADR-019 to reflect that Mode 2 column 3
carries minimal read-only content from M18 onward. The "empty reserved zone" description
applies to Mode 1 only after this change.

**EL decision:** ☐ Approved as drafted / ☐ Amended — see EL Approval Record below

---

## Decision 2 — Shock Taxonomy M18 vs. Deferred

**Question:** Does M18 G4 ship Form 2 (scenario shocks) with all six taxonomy entries,
or is a subset shipped in M18 with the remainder deferred?

**Background:** ADR-008 and the information hierarchy name six shock types:
`ElectionShock`, `CurrencyAttack`, `CreditorDefection`, `GeopoliticalShock`,
`NaturalDisaster`, `ContagionShock`. The M18 sprint plan (CE Agent consultation)
notes that Form 2 "requires a new backend endpoint or extension of the existing Mode 3
branching endpoint — new scope." The shock taxonomy and API contract must be specified
in ADR-019 before backend implementation begins.

**Demo 7 relevance:** Demo 7 Act 1 (Senegal Mode 3) exercises Form 1 (policy instruments)
— a fiscal counter-proposal applied at a specific step. Act 1 does not require Form 2
shock injection for the primary demo narrative. Form 2 is present in Mode 3 because the
control plane zone is sized for both forms simultaneously (information hierarchy §Control
Plane Reserved Zone), and removing Form 2 from the column would contradict ADR-008.

**Draft recommendation (PM Agent):** Ship all six shock types in M18. Rationale:

1. **Taxonomy is already specified** — no new design work. `ElectionShock`,
   `CurrencyAttack`, `CreditorDefection`, `GeopoliticalShock`, `NaturalDisaster`,
   `ContagionShock` are named in ADR-008 and the information hierarchy. Deferring
   half the taxonomy introduces a partially-populated Form 2 that looks incomplete
   at the Demo 7 table.
2. **Backend work is the same** — whether one shock type or six is shipped, the
   branching endpoint extension is needed. The API contract covers the taxonomy as a
   whole; partial implementation is not lower effort.
3. **Form 2 is present in both demos** — Act 2 (Zambia three-scenario) runs in Mode 3
   or Mode 2/1. The shock forms must be consistently present across all Mode 3 sessions.

**Partial-delivery option (if EL disagrees):** If Demo 7 Act 1 script explicitly calls
out a shock injection, ship `ElectionShock` and `GeopoliticalShock` first (highest
demo-relevance). Defer `CurrencyAttack`, `CreditorDefection`, `NaturalDisaster`,
`ContagionShock` to a post-M18 sprint. This requires a process exception for a
partially-populated taxonomy that ADR-019 must explicitly record.

**EL decision:** ☐ All six in M18 / ☐ Partial — specify subset below:

*If partial: _________________________*

---

## Decision 3 — EX-001 Disposition

**Question:** How is the expired Mode 3 render optimization exception (EX-001) resolved
in M18?

**Background:** EX-001 raised the AC-009 CI throttled threshold from 100ms to 200ms.
It expired at M17 exit. At M17, the AC-009 test was converted to `test.fixme()` because
CI runners returned 712–771ms vs the 200ms threshold (3–4× above threshold; KI-006 on
record as an external infrastructure limitation). The EX-001 M17 status update named
three resolution options:
- (a) Remove AC-009 from the test suite, replace with a local developer gate
- (b) Convert to a Playwright `--trace` annotation (record without assert)
- (c) Close as Won't Fix if Mode 3 render performance is confirmed acceptable

G4 (Mode 3 column implementation) includes genuine render optimization (#1217):
Recharts memoization and lazy ControlPlane mounting. The G4 PR must address
the performance gap — the sprint plan requires this in the same PR as the column
restructuring to avoid rebase risk.

**Draft recommendation (PM Agent):** Attempt genuine optimization in G4; close EX-001
based on G4 exit measurement.

Specifically:
1. **G4 implementing agent** runs the local MV-002 profiling gate (no throttle) before
   the G4 implementation PR merges. If Mode 3 full component set render is ≤ 100ms
   local (no throttle), proceed to CI measurement.
2. **CI gate:** If post-G4 CI measurement is ≤ 200ms on the 4× throttled runner,
   restore AC-009 from `test.fixme()` to `test()` at the 100ms threshold and close
   EX-001 as **Resolved**.
3. **If CI measurement remains above threshold** (KI-006 infrastructure limitation
   persists): close EX-001 via option (a) — remove AC-009 from the Playwright CI suite,
   replace with a documented local developer gate (`npm run test:perf` or `npm run
   profile:mode3`). The CI exception closes because the CI assertion is replaced, not
   because the performance problem is fixed. KI-006 remains on record.
4. **Option (b) trace annotation** is not recommended — recording without asserting
   produces performance data no one will act on. If the local gate approach (option a)
   is taken, that gate must have a pass criterion and must be run by the implementing
   agent at PR submission.

**What must not happen:** EX-001 must not carry into M19 without an explicit EL renewal
decision. This is the third milestone at which EX-001 reaches its expiry. An expired
exception that silently carries forward is a compliance finding.

**EL decision:** ☐ Approved — optimize in G4, close based on exit measurement per
recommendation above / ☐ Amended — see EL Approval Record below

---

## Downstream Unblock Record

On EL approval of this document, the following downstream actions unblock:

| Action | Owner | Can begin |
|---|---|---|
| ADR-019 authorship | Architect Agent | Immediately after EL approval of this document, **provided Artifacts 2 (#1356) and 4 (#1358) are also on record** |
| G4 sprint entry filing | PM Agent | After ADR-019 accepted (separate-session UX Designer sign-off, Tier 1, NM-042 compliance) |
| EX-001 renewal suppressed | Compliance | No renewal required — EX-001 resolves at G4 exit per Decision 3 |

**ADR-019 inputs from this document:**
- §Decision 1 provides the Mode 2 column content specification (ADR-019 §Mode 2 state)
- §Decision 2 provides the shock taxonomy scope (ADR-019 §Form 2 shock taxonomy)
- §Decision 3 provides the render optimization obligation and EX-001 exit condition
  (ADR-019 §G4 implementation obligations)

---

## EL Approval Record

**Filed:** 2026-06-26
**Awaiting EL review and approval**

*EL to record approval or amendment below. ADR-019 authorship begins on EL approval.*

> ___
> — @PublicEnemage (date: ______)
