# Control Plane Column — Delta Analysis and Dependency Map

> **Type:** Architecture Analysis (GD Artifact 4, Issue #1358)
> **Parent:** #1354 — Control Plane Column Design Package
> **Date:** 2026-06-26
> **Inputs:** Artifact 1 (ARCH-REVIEW-008-m18.md) — current state; Artifact 2 (information-hierarchy.md §Control Plane Reserved Zone, revised 2026-06-26) — target state; Artifact 3 (2026-06-26-control-plane-layer3-assessment.md) — persona constraints
> **Owning agents:** Architect Agent (leads); Frontend Architect Agent (Dimensions 1–2, 4–5); CE Agent (Dimensions 3, 6)
> **Filing location:** `docs/architecture/control-plane-column-delta-analysis-m18.md`

---

## Purpose

This document translates the gap between the current state (Artifact 1) and the
target state (Artifact 2) into a buildable engineering map. It identifies what must
be built, in what order, what each piece depends on, and which gaps can proceed in
parallel. The Demo 7 minimum viable set is called out as a named subset.

---

## Dimension 1 — Frontend Layout: Moving ControlPlane into the Column

### Gap

`ControlPlane` renders as a full-width horizontal bar below `InstrumentCluster`
(`ScenarioInstrumentCluster.tsx:983–989`). The 280px column (`gridColumn: 3` of
`InstrumentCluster`) is empty in Mode 3.

### Target

The control plane content for Mode 2 and Mode 3 renders inside the 280px column.
`InstrumentCluster` must accept a `controlPlane` slot. `ScenarioInstrumentCluster`
passes the appropriate form into that slot based on the active mode.

### Engineering delta

**`InstrumentCluster.tsx`:**
- Add `controlPlane?: React.ReactNode` to `InstrumentClusterProps` (line 45–65)
- In the column div (`data-testid="zone-control-plane"`, lines 183–211):
  - Keep the Mode 1/2 placeholder conditional (`!isMode3`)
  - When `controlPlane` prop is provided, render it inside the column div
  - The Mode 3 `isMode3` guard on the placeholder already exists — no structural change

**`ScenarioInstrumentCluster.tsx`:**
- Remove the `{mode === "MODE_3" && <ControlPlane .../>}` block (lines 983–989)
- Pass the appropriate form into `<InstrumentCluster controlPlane={...}>`:
  - Mode 2: pass the new `ScenarioConfigColumn` component (Dimension 4)
  - Mode 3: pass the new `ControlPlaneColumn` component (Dimensions 2 + 3)
  - Mode 1: pass nothing (placeholder renders)

**`ControlPlane.tsx`:**
- Rename to `ControlPlaneColumn.tsx` (the old name implied a standalone bar; the new name reflects its role as column content)
- Remove `borderTop: "2px solid #8b5cf6"` — the column border is provided by the `InstrumentCluster` column container, not the component itself
- The existing JSX becomes the starting point for the policy instruments form (Dimension 2 build)

### Dependencies

None. This is a frontend-only structural change. No API changes required.

### Backend dependency?

NO.

### Sizing verification

After the move, the column must still be 280px. The `InstrumentCluster` grid already
defines `minWidth: layout.controlPlane` on the column div — this is unchanged. The
rendered content inside the column does not set its own width; it fills the column.
Playwright AC-014 (column width = 280px in all modes) will pass without modification
to the column container.

---

## Dimension 2 — Mode 3 Policy Instruments Form

### Gap summary (from Artifact 1)

| Element | Current | Required |
|---|---|---|
| Control input type selector | ABSENT | Required |
| LegitimacyConstraint parameter | ABSENT | Required |
| FiscalMultiplier parameter | PARTIAL (slider) | Keep, adopt correct blue treatment |
| Step selector | PARTIAL (branch_from_step, wrong semantics) | Replace: "apply at step" selector |
| Apply button | PARTIAL (label wrong, purple) | Rename, recolor to blue #0284c7 |
| Applied inputs history list | ABSENT | Required |
| Blue visual treatment | ABSENT (purple #8b5cf6 throughout) | Replace with #0284c7 |

### Frontend engineering delta

**`ControlPlaneColumn.tsx` (renamed from `ControlPlane.tsx`):**

1. Add `policyInputType` state: `"FiscalMultiplier" | "LegitimacyConstraint"` with
   select element (`data-testid="policy-input-type-selector"`)

2. Replace `fiscalMultiplier` + `branchStep` with type-driven param state:
   - When type = FiscalMultiplier: slider range 0.1–3.0 step 0.05
   - When type = LegitimacyConstraint: slider range 0.0–1.0 step 0.05
   - `data-testid="policy-param-slider"` on both

3. Add `policyStep` state: dropdown/number input for "Apply at step" (range 1–maxStep)
   - This replaces `branchStep`; semantics change: "at which step does this input take
     effect" vs "recompute from which step"
   - `data-testid="policy-step-selector"`

4. Rename "Apply Change" → "Apply policy input"; recolor from purple to `#0284c7`
   - `data-testid="apply-policy-input"`

5. Add `appliedInputs` state: `Array<{step: number, type: string, value: number}>`
   populated on each successful Apply; rendered as history list
   - `data-testid="policy-inputs-history"`

6. Color correction: replace all `#8b5cf6` → `#0284c7` in style constants

**`Mode3Params` interface (exported from `ControlPlaneColumn.tsx`):**
Extend to include `legitimacy_index: number | null` alongside `fiscal_multiplier`:
```ts
export interface Mode3Params {
  input_type: "FiscalMultiplier" | "LegitimacyConstraint";
  fiscal_multiplier: number;
  legitimacy_index: number | null;
  apply_at_step: number;
  branch_from_step: number;
}
```

### Backend dependency: BranchRequest extension required

**Current `BranchRequest`** (`backend/app/schemas.py:824–841`):
```python
class BranchRequest(BaseModel):
    fiscal_multiplier: float = Field(default=1.0, ge=0.1, le=3.0, ...)
    branch_from_step: int = Field(ge=0, ...)
```

**Required extension:**
```python
class BranchRequest(BaseModel):
    fiscal_multiplier: float = Field(default=1.0, ge=0.1, le=3.0, ...)
    legitimacy_index: float | None = Field(default=None, ge=0.0, le=1.0, ...)
    branch_from_step: int = Field(ge=0, ...)
```

`RebranchRequest` needs the same addition (`legitimacy_index: float | None`).

The `ScenarioConfigSchema` already has `legitimacy_index: Decimal | None` (line 313).
The `WebScenarioRunner` already reads it (comment on line 294). The branch endpoint
(`POST /scenarios/{id}/branch`, line 1563–1564) copies the baseline config and
overrides `fiscal_multiplier` — it needs to also override `legitimacy_index` when provided.

This is a **non-breaking API extension** (new optional field with default `None`).
No engine changes required — the engine already models legitimacy.

**Backend change scope:** 3 files — `schemas.py` (BranchRequest + RebranchRequest),
`api/scenarios.py` (branch handler: apply legitimacy_index from request),
`api_contracts.yml` (schema update).

---

## Dimension 3 — Mode 3 Scenario Shocks Form (complete absence)

### Gap summary

The scenario shocks form does not exist anywhere in the codebase — frontend or
backend. The `TrajectoryStep.shock_events` field exists as a stub (`= []`, never
populated). The shock taxonomy (`ElectionShock`, `CurrencyAttack`, etc.) is not
defined in any Python enum or engine module.

### Frontend engineering delta (blocked by backend)

The frontend form itself is straightforward: a React component with step selector,
shock type dropdown, magnitude slider (GrowthShock only), Inject button, and history
list. The frontend build is small. The blocker is entirely backend.

### Backend engineering delta — this is the largest gap

**Current engine capability for exogenous shocks: NONE**

The `CommodityShockConfig` (schemas.py:317) is a scenario-level configuration
parameter, not a step-level injected event. It is applied as a global modifier
during scenario setup, not injected during active control. It is not the shock
injection mechanism needed for Mode 3.

**Required backend work:**

1. **Define shock type enum** (`backend/app/schemas.py`):
   ```python
   class ShockType(str, Enum):
       GrowthShock = "GrowthShock"
       ElectionShock = "ElectionShock"
       CurrencyAttack = "CurrencyAttack"
       CreditorDefection = "CreditorDefection"
       GeopoliticalShock = "GeopoliticalShock"
       NaturalDisaster = "NaturalDisaster"
       ContagionShock = "ContagionShock"
   ```

2. **Define shock injection request schema** (`backend/app/schemas.py`):

   The schema uses a discriminated union — `shock_type` is the discriminator; each
   type carries its own named parameter fields. This is the maximalist architecture:
   every type's parameters are explicit and validated at the API boundary. Adding a
   new shock type in a future milestone is additive — one new branch in the union, one
   new handler module, no changes to the dispatch pattern.

   ```python
   class ShockInjectRequest(BaseModel):
       shock_type: ShockType
       inject_at_step: int
       # Type-specific parameters — validated against shock_type by the endpoint.
       # All are optional at the schema level; the endpoint validates that required
       # fields for the selected shock_type are present.
       # GrowthShock parameters:
       growth_rate_delta: float | None = None      # departure from baseline growth rate
       duration_steps: int | None = None           # steps the perturbation persists
       distribution_asymmetry: float | None = None # cohort skew (0 = proportional)
       # ElectionShock parameters:
       severity: float | None = None               # political uncertainty magnitude
       political_uncertainty: float | None = None  # governance disruption factor
       # CurrencyAttack parameters:
       attack_magnitude: float | None = None       # FX rate shock magnitude
       # CreditorDefection parameters:
       creditor_class: str | None = None           # enum defined in ADR-019
       share_affected: float | None = None         # fraction of class defecting
       # GeopoliticalShock parameters:
       regime_change_probability: float | None = None
       regional_contagion: bool | None = None
       # NaturalDisaster parameters:
       affected_sectors: list[str] | None = None   # sector taxonomy from scenario
       gdp_impact: float | None = None
       # ContagionShock parameters:
       source_country: str | None = None           # ISO3 code
       transmission_rate: float | None = None
   ```

   ADR-019 specifies the complete parameter schemas, validation rules per type,
   and data dependency requirements (creditor_class taxonomy; ContagionShock
   linkage table approach) before G4 sprint entry.

3. **New API endpoint** (`backend/app/api/scenarios.py`):
   `POST /scenarios/{scenario_id}/inject-shock` — applies a shock to an existing
   branch scenario. This is separate from the branch endpoint because:
   - Shocks are injected into an already-branched scenario (not a new branch)
   - A shock injection modifies the step-level trajectory from `inject_at_step` forward
   - The endpoint must re-run the scenario from `inject_at_step` with the shock applied

4. **Engine shock implementation** (simulation modules):

   **All 7 shock types are implemented in G4** (EL Decision 6, 2026-06-27).
   No incremental rollout — the full engine is built complete. Each type requires
   a defined effect on the simulation state; all mappings must be specified in
   ADR-019 before G4 begins:
   - `GrowthShock`: perturbs GDP growth rate from `inject_at_step`; applies
     `distribution_asymmetry` across cohorts. Primary Demo 7 type.
   - `ElectionShock`: step-drop to `legitimacy_index`; propagates through
     GovernanceModule confidence cascade
   - `CurrencyAttack`: FX rate shock; propagates through fiscal parameters
     (import costs, debt servicing if FX-denominated)
   - `CreditorDefection`: removes `share_affected` of `creditor_class` from
     future debt service capacity; triggers MDA creditor flight alert
   - `GeopoliticalShock`: regional stability perturbation; affects FDI inflows
     and external balance
   - `NaturalDisaster`: sector-level output reduction across `affected_sectors`;
     GDP impact distributed by sector weight
   - `ContagionShock`: cross-country transmission from `source_country` via
     contagion linkage table; affects trade and capital flow parameters

   The implementing engineer MUST NOT implement a subset and defer the rest.
   The engine dispatch pattern (registry / `ShockEffect` protocol) is designed
   for all 7 simultaneously — partial implementation risks the shortcuts that
   incremental rollout is specifically designed to prevent.

5. **Populate `TrajectoryStep.shock_events`** (trajectory endpoint):
   The `GET /scenarios/{id}/trajectory` response must populate `shock_events` at
   steps where a shock was injected, so the frontend can render orange vertical
   markers. Current stub returns `[]` always.

**Backend change scope:** NEW — schemas.py (ShockType enum, ShockInjectRequest),
api/scenarios.py (inject-shock endpoint), simulation modules (shock effects per type),
trajectory endpoint (shock_events population), api_contracts.yml.

**This is the largest single engineering dependency in the design package.** It
gates Demo 7 Act 1 Step 4 (Troika rebuttal injection) entirely.

### ADR-019 dependency

The shock type effect mappings (what each shock type does to the engine state) are
architectural decisions that must be in ADR-019 before implementation begins.
ADR-019 is Artifact 6 of this design package — it gates on Artifacts 2, 4, and 5.
Shock implementation is therefore a Wave 2 or later item.

---

## Dimension 4 — Mode 2 Column Surface

> **Corrected 2026-06-27 per NM-072.** The original version of this dimension
> described a `ScenarioConfigColumn.tsx` with editable sliders and an "Apply
> Configuration" button — based on the pre-correction Artifact 2. That description
> is superseded. Mode 2 column 3 is not a scenario parameter editor. The correct
> target is specified below.

### Gap

No Mode 2 content exists in the 280px column. The column shows only the subdued
watermark. The gap is an absent pre-flight scenario summary and absent Mode 3
activation affordance.

### Frontend engineering delta

New component: `Mode2ColumnSurface.tsx` — lightweight, no form state, no sliders.

- **Scenario summary** (read-only, 4 lines): scenario name, entity (ISO3 +
  display name), calibration vintage, run horizon. All sourced from existing
  store state — no new API fetch required.
  `data-testid="mode2-scenario-summary"`

- **"Enter Active Control" button** (only interactive element):
  `background: #0284c7`, `opacity: 0.75` (subdued — pre-active signaling).
  On click: dispatches MODE_3 transition via Zustand store.
  `data-testid="enter-active-control"`

- **Caution text** (12px, `color: rgba(0,0,0,0.45)`): plain-language description
  of what Active Control does and how to exit it.

### Backend dependency: None

All display data is already in the scenario store. No new API calls.

### Dependency on Mode 3 column layout

`Mode2ColumnSurface` and `ControlPlane` are separate components passed into the
`InstrumentCluster` `controlPlane` prop slot (Dimension 1). They share no state.
The two-component separation is an EL-mandated architectural constraint — it enables
lazy mounting of `ControlPlane` for render optimization (Issue #1217 / EX-001).
**Mode 2 column content can be built independently of Mode 3 column content.**

---

## Dimension 5 — Blue/Orange Cross-Layer Visual System

### Layer A: ControlPlane.tsx color correction

Pure color swap. Replace `#8b5cf6` with `#0284c7` in all PANEL_STYLE, APPLY_BTN_STYLE,
VALUE_STYLE, and label constants. Zero logic changes.

**Frontend-only. No backend dependency.**

### Layer B: TrajectoryView.tsx — policy inflection markers (blue)

**Current state:** No policy input markers rendered in Mode 3.

**Backend data availability:** `TrajectoryStep.policy_inputs: list[dict[str, Any]]`
already exists in the trajectory response schema (`schemas.py:137`). This field
was added at M9 as a stub. Its population status must be confirmed: if the branch
endpoint populates `policy_inputs` per step in the trajectory response, this is a
frontend-only addition. If `policy_inputs` is also always `[]` in the response,
the backend must populate it.

Action: grep the branch endpoint handler for `policy_inputs` population logic before
assuming frontend-only.

**Frontend change:** In `TrajectoryView.tsx`, add a `<ReferenceLine>` element for
each step in `policy_inputs` (blue `#0284c7`, vertical, spans chart height, labeled
with the policy input type). This mirrors the specification in US-009.

### Layer C: TrajectoryView.tsx — shock event markers (orange)

**Current state:** No shock markers rendered. `TrajectoryStep.shock_events = []` always.

**Backend dependency: YES.** The orange vertical marker cannot be drawn until the
backend populates `shock_events` at injected steps in the trajectory response. This
is a Dimension 3 backend deliverable — the shock markers are gated on the shock
injection engine.

**Frontend change (once backend populates shock_events):** In `TrajectoryView.tsx`,
add a `<ReferenceLine>` element for each step in `shock_events` (orange `#ea580c`,
vertical, spans chart height, labeled with the shock type name).

### Layer D: MDAAlertPanelZone1B.tsx — causal attribution color distinction

**Current state:** `alert.causal_attribution` is rendered as plain text when present.
No color distinction between policy-caused and shock-caused attributions.

**Backend dependency: YES** (for a clean implementation). The current `causal_attribution`
field is a free-form string. Distinguishing policy vs. shock attribution by color requires
knowing which type caused the alert. Two options:

- **Option A (preferred):** Add `cause_type: "policy" | "shock" | "multiple" | None`
  to the MDA alert data model. Frontend applies blue for "policy", orange for "shock",
  gray for "multiple". This is a backend schema addition.

- **Option B (no backend change):** Parse the `causal_attribution` string to detect
  whether it contains a shock type keyword. Brittle — couples frontend to backend
  string format. Not recommended.

**Backend change scope for Option A:** Alert model in `schemas.py` + MDA alert
generation in `web_scenario_runner.py`. Small change — the runner knows whether an
alert was triggered by a policy input or a shock injection.

**Frontend change:** In `MDAAlertPanelZone1B.tsx`, color the "Caused by:" line based
on `cause_type`: `#0284c7` for policy, `#ea580c` for shock, `#555` (current neutral)
for multiple or unknown.

---

## Dimension 6 — Render Performance and EX-001

### Current baseline

- CI throttled (4× CPU, ubuntu-latest 2-core): **179ms** measured 2026-06-24
- Hardware (MV-002, ProBook 8GB/4-core, unthrottled): **50.5ms** (M10 measurement;
  not re-validated after M11–M17 Mode 3 additions)
- EX-001 status: ACTIVE but expired at M17 exit; no renewal decision on record

### Impact of control plane column changes on render time

**Low impact items (frontend-only, no new chart components):**
- Moving ControlPlane into the column: zero impact (DOM restructuring, not chart work)
- Color corrections: zero impact
- Mode 2 config form: zero impact (renders in column, no new chart components)
- Policy instruments form additions (type selector, history list): minimal (no chart components)

**Medium impact items:**
- Policy inflection markers in TrajectoryView: each `<ReferenceLine>` adds a Recharts
  render pass. At 6 applied inputs (a realistic upper bound for Demo 7), this adds
  6 ReferenceLine components to the ComposedChart. Estimated impact: <20ms additional
  (ReferenceLine is lightweight; AC-009 test fixture uses 3 shock ReferenceLine components
  already as a reference point).

**High impact items (blocks on backend Dimension 3):**
- Shock event markers in TrajectoryView: same as policy markers — 1–3 additional
  ReferenceLine components per shock injection. These gate on backend shock implementation.

### Issue #1217 position in build sequence

Issue #1217 (Recharts memoization + lazy ControlPlane mounting) was filed to address
the current 179ms performance baseline. It is filed as G4 Wave 2, sequenced via GD/ADR-019.

**Recommended positioning:** Resolve #1217 **before or during** the column layout move
(Dimension 1), not after. Rationale: lazy ControlPlane mounting is specifically about
avoiding full re-renders when Mode 3 is entered — this is exactly the state transition
that Dimension 1 introduces. If #1217 is deferred until after the column build, the
column build establishes a new (potentially worse) performance baseline that #1217 then
has to recover. Build in the right order: optimize the mount, then mount the forms.

**EX-001 decision required before M18 closes:** The exception was set to expire at M17
exit. The options are:
- (a) Renew EX-001 at 200ms for M18 duration while #1217 is resolved (least disruptive)
- (b) Resolve #1217 first, then run AC-009 to confirm return to 100ms, then close EX-001
- (c) Close EX-001 as Won't Fix if profiling confirms the current trajectory is acceptable

This is an EL decision (EX-001 renewal requires an EL decision per the exceptions registry).
It should be captured in Artifact 5 (Scope Decision Document) so the EL makes the call
explicitly rather than leaving EX-001 in expired-but-active limbo.

---

## Dependency Map — Build Sequence

### Level 0: Frontend-only — no API changes required

Can begin immediately after Artifact 6 (ADR-019) is accepted.

| Item | Component(s) | Blocks |
|---|---|---|
| L0-A: Move ControlPlane into column slot | `InstrumentCluster.tsx`, `ScenarioInstrumentCluster.tsx` | All subsequent column work |
| L0-B: Color correction (purple → blue) | `ControlPlane.tsx` → `ControlPlaneColumn.tsx` | L0-D, L2-A |
| L0-C: Mode 2 config form (FiscalMultiplier + LegitimacyConstraint) | New `ScenarioConfigColumn.tsx` | Nothing |
| L0-D: Policy instruments form (type selector, history list, step selector) | `ControlPlaneColumn.tsx` | L1-B (blue markers in trajectory) |
| L0-E: Resolve #1217 (Recharts memoization / lazy mount) | `InstrumentCluster.tsx`, `ControlPlaneColumn.tsx` | L0-A (should precede or accompany) |

L0-C and L0-D can be built concurrently on separate branches once L0-A is merged.

### Level 1: API extension — non-breaking, small scope

| Item | Backend files | Frontend consumer | Blocks |
|---|---|---|---|
| L1-A: Extend BranchRequest + RebranchRequest with legitimacy_index | `schemas.py`, `api/scenarios.py`, `api_contracts.yml` | `ControlPlaneColumn.tsx` (L0-D) | L2-A (LegitimacyConstraint policy inputs) |
| L1-B: Populate policy_inputs per step in trajectory response (confirm or implement) | `api/scenarios.py` trajectory handler | `TrajectoryView.tsx` blue markers | Blue trajectory markers |
| L1-C: Add cause_type to MDA alert model | `schemas.py`, `web_scenario_runner.py` | `MDAAlertPanelZone1B.tsx` | Color-coded causal attribution |

L1-A, L1-B, L1-C can proceed concurrently.

### Level 2: Engine capability — significant new work (gates on ADR-019 acceptance)

| Item | Backend files | Frontend consumer | Blocks |
|---|---|---|---|
| L2-A: Implement GrowthShock in engine + inject-shock endpoint | `schemas.py`, `api/scenarios.py`, simulation modules | `ControlPlaneColumn.tsx` scenario shocks form | Demo 7 Step 4 |
| L2-B: Implement remaining shock types (ElectionShock, CurrencyAttack, etc.) | simulation modules (per-type effects) | — | Complete shock taxonomy |
| L2-C: Populate shock_events in trajectory response | `api/scenarios.py` trajectory handler | `TrajectoryView.tsx` orange markers | Orange shock markers |

L2-A must precede L2-B and L2-C. L2-B and L2-C can proceed concurrently after L2-A.

---

## Demo 7 Minimum Viable Set

Demo 7 Act 1 = Journey C Steps 1–4. Minimum viable set to enable all four steps:

| Journey C Step | Capability required | Build level |
|---|---|---|
| Step 1: Switch to Mode 3, control plane visible alongside trajectory | L0-A (column move) | **Level 0** |
| Step 2: Apply policy input → live A/B + divergence fill | L0-D (policy form) + L1-A (legitimacy API) | **Level 0 + 1** |
| Step 3: Read causal attribution, cite the finding | L1-B (policy_inputs populated) + L1-C (cause_type) | **Level 1** |
| Step 4: Inject GDP shock → alert persists | L2-A (GrowthShock engine) | **Level 2** |

**Critical path to Demo 7:** L0-A → L0-D (in parallel with L1-A, L1-B, L1-C) → L2-A.

Steps 1–3 can be demonstrated with Level 0 + Level 1 work alone. Step 4 requires the
shock engine (Level 2) — this is the binding constraint on the Demo 7 Act 1 completion
date.

**Demo 7 minimum viable for Steps 1–3 (no shock):** Level 0 + Level 1 work only.
This demonstrates: Mode 3 switch → control plane in column → policy input applied →
live A/B → causal attribution with color treatment. This is the core argument. Step 4
(shock injection) remains the strongest argument but is gated on engine work.

---

## Contradiction and Risk Register

| # | Item | Risk | Mitigation |
|---|---|---|---|
| R-1 | policy_inputs in TrajectoryStep may always be `[]` (stub) | Blue trajectory markers blocked without backend population | Confirm population status before frontend work on L1-B; if stub, add backend population in L1-B |
| R-2 | GrowthShock engine mapping is not specified | L2-A cannot begin without a defined effect on simulation state | ADR-019 must specify GrowthShock → engine parameter mapping before L2-A |
| R-3 | #1217 deferred past L0-A creates a regression | Column mount with both forms may worsen 179ms baseline | Sequence #1217 before or with L0-A (Level 0 constraint) |
| R-4 | EX-001 in expired-but-active limbo at M18 start | Compliance finding if not resolved | EL decision required in Artifact 5 |
| R-5 | Shock type effects for non-GrowthShock types unspecified | L2-B cannot begin without per-type engine mappings | These are Wave 2+ items; document as out-of-scope for Demo 7 minimum viable set |
| R-6 | Mode 2 "Apply Configuration" creates a new scenario ID | Frontend must handle scenario ID switch; existing store/fetch hooks must support live ID change | Scope this carefully in L0-C; test store ID switch before merging |

---

## Acceptance Criteria Verification

- [x] All six dimensions covered (Dimensions 1–6 above)
- [x] Backend dependencies called out for shocks form (Dimension 3) and orange markers (Dimension 5 Layer C)
- [x] Shock taxonomy backend status confirmed: **NOT modeled** in current engine; stub only; Level 2 new work required
- [x] Dependency map identifies Demo 7 minimum viable set: L0-A, L0-D, L1-A, L1-B, L1-C, L2-A (GrowthShock only)
- [x] #1217 positioned in build sequence: before or during L0-A
- [x] Mode 2 column content dependency on Mode 3 column layout addressed: independent after L0-A; concurrent build possible
