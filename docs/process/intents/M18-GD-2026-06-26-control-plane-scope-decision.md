---
name: M18-GD-control-plane-scope-decision
type: scope-decision-document
artifact: "Artifact 5 — GD Design Package (#1359)"
issues:
  - "#1359 — Artifact 5: Scope Decision Document (EL gate)"
  - "#1354 — Control Plane Design Package (parent)"
status: "EL-approved 2026-06-26 (Decisions 1–4); Decision 5 superseded by Decision 6 (2026-06-27); Decision 6 EL-approved 2026-06-27 (all 7 shock handlers in G4)"
authored-by: PM Agent
authored-date: 2026-06-26
el-approved: "2026-06-26"
release-branch: release/m18
gd-phase: "Phase 3 — filed after Artifacts 2 (#1356) and 4 (#1358)"
downstream-unblock:
  - "ADR-019 authorship (Architect Agent, #1360) — may not begin until this document is EL-approved"
  - "G4 sprint entry (Wave 2 implementation) — may not be filed until ADR-019 is accepted"
sprint-entry-reference: "docs/process/sprint-plans/m18-gd-sprint-entry.md (EL-approved 2026-06-26)"
---

# Artifact 5 — Control Plane Scope Decision Document

> **Framing note (added 2026-06-27, per NM-072 course correction):**
> This document records M18 delivery scope decisions against the platform target
> state defined in Artifact 2 (`docs/ux/information-hierarchy.md §Control Plane
> Reserved Zone`). It does not define or modify the platform target state — that
> is Artifact 2's role. Where this document says "in M18" or "for Demo 7," those
> are delivery scope qualifiers. The target state itself is milestone-independent.
> Agents reading this document must consult Artifact 2 for the full platform target
> before interpreting any decision here as an architectural constraint.

**GD Phase 3 gate.** This document records EL decisions required before ADR-019
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

**EL decision:** ☑ Approved as drafted — with panel conditions required in ADR-019 (see EL Approval Record)

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

**EL decision:** ☑ All six in M18 — ADR-019 must specify parameter schemas and data dependency status for all six types before G4 sprint entry (see EL Approval Record)

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

**EL decision:** ☑ Approved — optimize in G4, close based on exit measurement per
recommendation above. Resolution label: Resolved if MV-002 ≤ 100ms at G4 exit;
Won't Fix otherwise. AC-009 removed from CI permanently regardless of label.

---

## Decision 4 — GrowthShock Taxonomy Gap (Post-Approval Escalation)

**Post-approval escalation.** This decision was not raised during the panel deliberation
for Decision 2. The six-type taxonomy was the input presented to the panel — the panel
deliberated whether to include all six or a deferred subset, not whether the six were
the right six. `GrowthShock` was absent, not considered and rejected.

This gap was identified during GD design work following panel deliberation. It is
escalated here as a Decision 4 amendment before ADR-019 authorship begins, so the
ADR-019 author receives a complete scope specification rather than discovering the gap
during drafting.

**Question:** Should `GrowthShock` be added as a seventh shock type in the M18 Form 2
shock taxonomy, or explicitly deferred with recorded rationale?

---

### Why GrowthShock was not in the original six

The ADR-008 taxonomy was designed around systemic risk events: political instability
(`ElectionShock`), financial attacks (`CurrencyAttack`, `CreditorDefection`), and
exogenous destabilizers (`GeopoliticalShock`, `NaturalDisaster`, `ContagionShock`).
All six model adverse shocks — events that put the system under stress.

`GrowthShock` models a different category: a counter-hypothesis shock — what if the
GDP growth rate departs from the projected baseline? This is not necessarily adverse;
it models optimistic, pessimistic, or orthogonal growth scenarios. ADR-008 did not
include it because ADR-008 addressed crisis-response modeling. Demo 7 exposes the gap:
a primary demo narrative requires testing a growth counter-claim at the negotiating table.

---

### Demo 7 requirement — Artifact 3 Customer Agent finding

The Artifact 3 Layer 3 assessment
(`docs/ux/usability-sessions/synthesis/2026-06-26-control-plane-layer3-assessment.md`)
identified `GrowthShock` as ESSENTIAL for Demo 7 Step 4 — the Troika rebuttal
scenario: the opposing analyst claims "GDP rebound will protect bottom quintile."
The ministry team's counter is to inject a GDP growth shock at the rebound step and
observe whether the modeled rebound reaches the bottom quintile or is captured
disproportionately by upper cohorts.

Without `GrowthShock`, the analyst must use `fiscal_multiplier` as a proxy — a
methodological compromise that a sophisticated opposing analyst (Persona 3) can
challenge on the spot. The Demo 7 Step 4 argument is only cogent if the growth
departure is modeled as what it is: a growth shock, not a fiscal lever.

---

### Architectural impact — additive, not re-architecting

The deliberation record (CE Agent, Decision 2) specifies the shock injection endpoint
as a discriminated union:

```
shock_type: enum[ElectionShock, CurrencyAttack, ...]
parameters: {type-specific dict — validated against shock_type}
inject_at_step: int
```

Adding `GrowthShock` is purely additive — new enum value, new parameter schema:

| Parameter | Type | Notes |
|---|---|---|
| `growth_rate_delta` | `float` | Departure from baseline GDP growth rate. Positive = optimistic; negative = pessimistic. |
| `duration_steps` | `int` | Steps the growth rate departure persists. |
| `distribution_asymmetry` | `float` (optional, default `0.0`) | Cohort skew on growth landing. `0` = proportional; positive = upper-cohort skew; negative = lower-cohort skew. This parameter carries the Demo 7 Step 4 argument. |

No data dependency beyond the scenario's existing cohort structure (already loaded with
the scenario — same tier as `ElectionShock` per the CE Agent's Decision 2 parameter
complexity table). No new database tables, no new reference data.

The endpoint structure is unchanged. The discriminated union is already designed to
accommodate additional types.

---

### Recommendation

Add `GrowthShock` as the seventh type in the M18 Form 2 taxonomy. Rationale:

1. **Demo 7 Step 4 cogency** — the Troika rebuttal argument is methodologically unsound
   without a growth shock. A fiscal multiplier proxy is a kryptonite vector under
   the scrutiny of a sophisticated opposing analyst (Persona 3).
2. **Architecture is already extensible** — one new enum value and one parameter schema.
   No re-architecture cost. This was the design intent of the discriminated union pattern.
3. **No data dependency** — self-contained; no new reference tables or database schema
   changes beyond what Decision 2 already mandates for `CreditorDefection` and
   `ContagionShock`.
4. **Taxonomy coherence** — extending from adverse-crisis shocks to counter-hypothesis
   shocks is a natural capability extension, not a category change. The `distribution_asymmetry`
   parameter makes `GrowthShock` analytically distinct from a fiscal lever: it directly
   models the distributional question that is at the center of Demo 7 Step 4.

**If EL defers:** Deferral must be recorded with explicit rationale (not "not in original
scope" — that is the gap, not a rationale). If deferred, Demo 7 Step 4 requires a
documented methodological workaround noting that `fiscal_multiplier` is used as a proxy
and naming the analytical limitation this introduces.

**EL decision:** ☑ Add GrowthShock as seventh type — approved 2026-06-26

---

## Downstream Unblock Record

On EL approval of this document, the following downstream actions unblock:

| Action | Owner | Can begin |
|---|---|---|
| ADR-019 authorship | Architect Agent | After EL approval of Decisions 1–4 and Decision 6 (Decision 5 superseded) — provided Artifacts 2 (#1356) and 4 (#1358) corrected per NM-072 and on record |
| G4 sprint entry filing | PM Agent | After ADR-019 accepted (separate-session UX Designer sign-off, Tier 1, NM-042 compliance) |
| EX-001 renewal suppressed | Compliance | No renewal required — EX-001 resolves at G4 exit per Decision 3 |

**ADR-019 inputs from this document:**
- §Decision 1 provides the Mode 2 column content specification (ADR-019 §Mode 2 state)
- §Decision 2 provides the shock taxonomy scope — six base types (ADR-019 §Form 2 shock taxonomy)
- §Decision 4 provides the GrowthShock addition (approved — add as seventh type)
- §Decision 6 supersedes Decision 5: all 7 shock handlers implemented in G4; Form 2 exposes all 7 types; ADR-019 §Form 2 defines parameter schemas for all 7 types; no deferred types
- §Decision 3 provides the render optimization obligation and EX-001 exit condition
  (ADR-019 §G4 implementation obligations)

---

## EL Approval Record

**Filed:** 2026-06-26
**EL-approved:** 2026-06-26

> All three decisions approved per panel recommendations. Panel deliberation record:
> `docs/process/intents/M18-GD-2026-06-26-control-plane-scope-decision-deliberation.md`
>
> **Decision 1 — Mode 2 column 3:** Approved. Populate with read-only scenario summary
> and Mode 3 activation control. ADR-019 must satisfy all three panel conditions before
> G4 sprint entry: (1) button label is "Enter Active Control" — not "Enter Mode 3"
> (Customer Agent kryptonite finding, Personas 2 and 5); (2) subdued visual treatment
> in Mode 2 to signal pre-active state (UX Designer); (3) two-component architecture —
> `Mode2ColumnSurface` and `ControlPlane` are separate components, not conditional
> rendering within one component (Frontend Architect).
>
> **Decision 2 — Shock taxonomy:** Approved — all six types in M18. ADR-019 must
> specify parameter schemas and data dependency status for all six types before the G4
> sprint entry is filed. Specifically: `creditor_class` enum taxonomy for
> `CreditorDefection` and the `ContagionShock` linkage approach (pre-populated table vs.
> simplified model) must be resolved in ADR-019 (CE Agent finding).
>
> **Decision 3 — EX-001:** Approved. G4 implements structural optimization (lazy
> mounting via two-component architecture, Recharts memoization). At G4 exit, re-run
> MV-002 on ProBook hardware. Resolution label: **Resolved** if MV-002 ≤ 100ms;
> **Won't Fix** otherwise. AC-009 `test.fixme()` removed from CI permanently regardless
> of label — test structure preserved with comment referencing EX-001 closure record.
> PI Agent process conditions apply: (1) resolution path recorded in
> `docs/compliance/exceptions.md §EX-001` before G4 begins; (2) EX-001 named as
> explicit deliverable in G4 sprint entry scope; (3) final closure entry with MV-002
> measurement at G4 exit.
>
> ADR-019 authorship is unblocked from this approval — still gated on Artifacts 2
> (#1356) and 4 (#1358) being on record per §Downstream Unblock Record.
>
> — @PublicEnemage (2026-06-26)

---

## Decision 6 — Shock Engine Implementation Scope for G4

**Supersedes Decision 5.** Decision 5 limited Form 2 UI to 4 types for Demo 7.
Decision 6 resolves the broader question of engine implementation scope. As engine
scope is a superset of UI scope, Decision 6 takes precedence. Decision 5 is
preserved below as a historical record of the reasoning that led to this decision.

**Question:** Does G4 build 4 shock engine handlers (matching the Decision 5 UI scope)
or all 7 (complete engine implementation regardless of UI exposure)?

**EL decision and rationale (2026-06-27):**

Build all 7 shock handlers in G4. Rationale: the risk of misinterpretation across
implementing agents is too high to scale shock handlers incrementally against a
fully-specified target architecture. Cherry-picking 4 of 7 types for engine
implementation creates ambiguity about which handlers are complete and which are
absent — this ambiguity compounds as different agents read different artifacts at
different points in time. The NM-072 sequence inversion has already demonstrated
that artifact-to-artifact confusion is a real failure mode in this design package.
The forcing-function argument applies: requiring all 7 engine handlers to be built
simultaneously forces the architecture (dispatch pattern, ShockEffect protocol,
registry) to be correct for the general case, not the 4-type case.

**Consequence for UI exposure:** Form 2 type selector shows all 7 types. Decision 5's
4-type UI restriction is superseded. "Don't slice and dice" applies to both engine
and UI — the complete taxonomy is present and functional from G4 exit.

**ADR-019 obligations from this decision:**
- `ShockEffect` protocol / registry pattern must be specified for all 7 types
- Parameter schemas for all 7 types must be fully resolved (including
  `creditor_class` enum for `CreditorDefection` and linkage table approach
  for `ContagionShock`) before G4 sprint entry is filed
- The implementing engineer must not defer any handler to M19

**EL approval:** ☑ Approved 2026-06-27

---

## Decision 5 — Form 2 MVP Shock Type Scope for Demo 7 (SUPERSEDED by Decision 6)

**Post-approval scope refinement.** Decision 2 (all seven types in M18) established the
full taxonomy. Decision 5 defines which subset is implemented and exposed in Form 2 for
Demo 7. The remaining types are deferred to M19 — they do not appear in the Form 2 type
selector and are not engine-implemented in G4.

**Question:** Of the seven approved shock types, which are implemented and exposed in
Form 2 for Demo 7?

---

### Analysis basis

The Demo 7 readiness checklist (sprint plan §Demo 7 Minimum Viable Readiness Checklist)
does not list Form 2 as a required condition. Artifact 3 Customer Agent assessment
challenges this: "Steps 1–3 alone prove Mode 2 capability, not Mode 3" — the Troika
rebuttal injection is what makes Active Control demonstrably distinct from Simulation
mode. Form 2 therefore needs at minimum one exercised, functional type for the Mode 3
claim to survive scrutiny from a sophisticated participant (Persona 3).

**Data dependency filter:** CE Agent (Decision 2 deliberation) identified two types with
data-dependent parameters — `CreditorDefection` (`creditor_class` enum) and
`ContagionShock` (linkage table). Including either in G4 scope creates an ADR-019
obligation to resolve the dependency before sprint entry. Deferring both removes that
obligation entirely and reduces ADR-019 parameter schema scope.

---

### Demo 7 type evaluation

| Type | Demo hook | Data dependency | Decision 5 verdict |
|---|---|---|---|
| `GrowthShock` | ESSENTIAL — Troika rebuttal (Demo 7 Step 4): inject positive GDP growth at rebound step; observe whether distribution reaches bottom quintile | None | **Include** |
| `ElectionShock` | HIGH — Senegal political context; governance timeline is the source of conditionality pressure the minister is navigating | None | **Include** |
| `GeopoliticalShock` | HIGH — ECOWAS/regional dynamics; demonstrates shock injection spans structural domain, not only macro | None | **Include** |
| `CurrencyAttack` | MEDIUM — Zambia Kwacha vulnerability; answers "what happens to the restructuring path if the currency comes under pressure?" in Act 2 Q&A | None | **Include** |
| `NaturalDisaster` | LOW — no specific hook in either demo narrative | None | **Defer → M19** |
| `CreditorDefection` | MEDIUM — Zambia debt context; but Act 2 is comparison-driven, not shock-injection-driven | `creditor_class` enum required | **Defer → M19** |
| `ContagionShock` | LOW — least contextually specific; highest data dependency | Linkage table required | **Defer → M19** |

---

### Decision 5 ruling

**Four types for Demo 7 — `GrowthShock`, `ElectionShock`, `GeopoliticalShock`,
`CurrencyAttack`.**

Three types deferred to M19 — `NaturalDisaster`, `CreditorDefection`, `ContagionShock`.

**UI implication:** Form 2 type selector shows exactly four types. The deferred three
do not appear. Demo presenter answer if asked: *"Four shock categories are available in
Active Control — currency attacks, election shocks, geopolitical shocks, and growth
scenario testing. We're expanding the library in the next milestone."* This is an honest
and complete answer; it does not trigger the "next release" kryptonite because it is
describing what is present, not deferring what was expected.

**Scope reduction from Decision 2 baseline:**

- Removes `NaturalDisaster`, `CreditorDefection`, `ContagionShock` from G4 engine
  implementation scope
- Removes `creditor_class` taxonomy definition obligation from ADR-019
- Removes `ContagionShock` linkage table approach from ADR-019
- ADR-019 §Form 2 shock taxonomy specifies parameter schemas for four types only;
  the deferred three are noted as M19 scope in the ADR

**The four included types span four distinct analytical domains:**
- Macro (growth rate): `GrowthShock`
- Political (governance uncertainty): `ElectionShock`
- Structural (regional dynamics): `GeopoliticalShock`
- Financial attack (exchange rate): `CurrencyAttack`

This breadth of domain coverage is the platform claim — four domains, one instrument
interface, one shared trajectory display. It is a stronger demo argument than seven
types across overlapping domains.

**EL decision:** ☑ Approved 2026-06-27 — four types for Demo 7 as specified above.

---

## Decision 4 EL Approval Record

**Filed:** 2026-06-26 (post-panel escalation)
**EL-approved:** 2026-06-26

> ☑ **Add GrowthShock as seventh type.** ADR-019 includes `GrowthShock` in the Form 2
> shock taxonomy with parameter schema: `growth_rate_delta: float`,
> `duration_steps: int`, `distribution_asymmetry: float (optional, default 0.0)`.
> CE Agent parameter schema table updated accordingly. No additional sprint scope
> change required — data dependency is self-contained (same tier as `ElectionShock`).
>
> — @PublicEnemage (2026-06-26)
