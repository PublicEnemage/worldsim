# ARCH-REVIEW-007: N>2 Supplemental Assessment — M17 G2 Phase 2

> **Artifact 3 of G2 Phase 2 architecture sprint**
> **Authored by:** Architect Agent
> **Date:** 2026-06-25
> **Supplemental to:** `docs/architecture/reviews/ARCH-REVIEW-007-milestone15.md`
> **Issue:** #394 — feat: multi-scenario comparison (>2 scenarios)
> **Authority:** `docs/process/intents/M17-G2-2026-06-25-multi-scenario-design.md §3.3`
> **Phase 1 inputs:** `docs/ux/design-thinking/multi-scenario-comparison/ux-journeys-n3.md` (Artifact 1),
> `docs/ux/design-thinking/multi-scenario-comparison/persona-mvs-n3.md` (Artifact 2)

---

## Purpose

This supplemental architecture assessment revisits the ARCH-REVIEW-007 binding constraint
(`COMPARE_VIEW N≤2/fixture`) in light of the G2 Phase 1 UX journeys and persona MVS.
It addresses the three architectural questions from the sprint plan and determines the ADR
requirement for G2 Phase 3 implementation.

---

## N>2 Assessment Against ARCH-REVIEW-007 Binding Constraint

**Original binding constraint (ARCH-REVIEW-007 §Open Question (b), 2026-06-22):**

> "Mode 1 COMPARE_VIEW multi-entity: Zone 1A supports N≤2 entities per fixture in Mode 1
> COMPARE_VIEW. Encoding: 1 composite line per entity per fixture (Fixture A = solid 100%,
> Fixture B = ghost 50% dashed)."

**The G2 N>2 requirement is structurally different from the ARCH-REVIEW-007 constraint.**

The original constraint addresses N entities across 2 fixtures (entity-level comparison):
each fixture carries one or more entities, and the two fixtures are compared by opacity
(solid baseline vs. ghost comparison). The G2 requirement addresses N scenarios for a single
entity (ZMB): three independent scenario trajectories for the same entity in Mode 2, compared
simultaneously.

These are orthogonal dimensions:
- **ARCH-REVIEW-007 entity COMPARE_VIEW:** N entities × 2 fixtures → color by entity, opacity by fixture
- **G2 scenario comparison:** 1 entity × N scenarios → color by scenario, line-style by scenario

Because the dimensions are orthogonal, the G2 N=3 scenario comparison does **not** violate
the ARCH-REVIEW-007 N≤2/fixture constraint. The existing constraint governs entity-level
comparison across fixtures; it does not govern scenario-level comparison within a single entity.

**However:** The G2 design requires the Zone 1A rendering architecture to distinguish scenario
identity by a channel pair (color + line-style) that is not currently implemented. The current
implementation uses entity color (`ENTITY_PALETTE`) and opacity (`comparisonMode: boolean`)
as the two differentiation channels. The N=3 scenario comparison requires a **scenario palette**
and **scenario line-style assignment** that are distinct from the entity palette. This is a
component-boundary change in `TrajectoryView.tsx`.

**Assessment summary:** The N>2 scenario comparison extends the compare-mode overlay within
the `TrajectoryView` component boundary. It does **not** require changes to the `composite_score`
aggregation or rendering path. It **does** require changes to the overlay logic (new scenario
palette, line-style assignment, scenario-aware terminal label rendering). This is a
**component-level extension**, not an architectural restructuring.

---

## Three Architecture Questions

### Q1: Does Zone 1A N>2 require changes to the composite_score rendering path, or only to the compare-mode overlay?

**Answer: Compare-mode overlay only. No changes to composite_score aggregation or rendering.**

The Zone 1A N=3 scenario curves use the existing `composite_score` per step from the
simulation engine's trajectory response — consistent with ARCH-REVIEW-007 Open Question (c)
decision ("Zone 1A composite = existing `composite_score` engine output"). No new aggregation
formula is introduced. The three scenarios produce three separate trajectory responses; each
trajectory response has a `composite_score` per step; `TrajectoryView` renders three curves.

**What changes in `TrajectoryView.tsx`:**

1. **`comparisonMode: boolean` → `comparisonScenarios?: ScenarioComparisonConfig[]`**

   Current `comparisonMode: boolean` prop does not carry scenario identity. N=3 requires
   the component to know which curve belongs to which scenario and what visual treatment to
   apply. The prop must be extended to carry an ordered list of scenario configurations:

   ```typescript
   interface ScenarioComparisonConfig {
     scenarioId: string;
     label: string;          // "Option A", "B", "C"
     color: string;          // e.g., "#2563EB"
     strokeDasharray?: string; // e.g., "8 2" for dashed
   }
   ```

   `comparisonMode: boolean` becomes backward-compatible (treated as `[primaryScenario]`)
   or is deprecated in favor of `comparisonScenarios`. The implementing agent determines
   the cleanest migration path at Phase 3. This is a component prop change, not an
   architectural change.

2. **SCENARIO_PALETTE constant (new, distinct from ENTITY_PALETTE)**

   A `SCENARIO_COMPARISON_PALETTE` constant in `TrajectoryView.tsx` for the three colors:
   `#2563EB` (Option A), `#D97706` (Option B), `#16A34A` (Option C). This is a constant
   addition — no rendering path change.

3. **Dynamic y-offset for terminal endpoint labels**

   The existing dynamic y-offset algorithm (ARCH-REVIEW-007 Open Question (d) decision) already
   handles endpoint label collision at N≤4. N=3 scenario labels ("A", "B", "C") are placed by
   the same algorithm. No new collision logic is required.

4. **`entityTrajectories` prop → `scenarioTrajectories` (or extension)**

   The existing `entityTrajectories: Record<string, TrajectoryResponse>` prop carries per-entity
   trajectories. For scenario comparison, the same structure applies with scenario IDs as keys
   instead of entity codes. The implementing agent may either (a) reuse `entityTrajectories`
   with scenario IDs as keys and the scenario palette override, or (b) introduce a parallel
   `scenarioTrajectories` prop. Option (a) is simpler; option (b) is cleaner for future
   maintainability. Phase 3 architecture decision — both are within the component boundary.

**Conclusion:** Zone 1A N=3 operates within the existing compare-mode overlay contract.
**No new ADR is required for Zone 1A.** An architecture review note on #394 is sufficient.

---

### Q2: Does Zone 1B per-scenario threshold crossings require a new backend data structure in the compare endpoint, or is the existing `threshold_crossings` field sufficient with client-side per-scenario composition?

**Answer: Client-side composition from N=3 parallel trajectory calls. No new backend endpoint required for Phase 3 Demo 7 scope.**

**Current state:** The existing compare endpoint
(`GET /api/v1/scenarios/compare?scenario_id=A&compare_scenario_id=B`) returns a single
`TrajectoryCompareResponse` with `threshold_crossings` as a merged field. This endpoint
was designed for N=2 and uses a single-call pattern (per information-hierarchy.md NB-7
API design decision).

**G2 N=3 option analysis:**

*Option 1: Extend the compare endpoint to N scenarios*
`GET /api/v1/scenarios/compare?scenario_ids=A,B,C&include_threshold_crossings=true`
Returns per-scenario `threshold_crossings` in the response. This is the cleanest backend
approach for N≥3 but requires: (a) new query parameter handling in the compare endpoint,
(b) a new response schema with per-scenario crossing attribution, (c) schema update to
`docs/schema/api_contracts.yml`. This constitutes a data contract change that may require
ADR coverage (see below).

*Option 2: N parallel trajectory calls with client-side per-scenario composition*
The frontend loads N=3 trajectory responses (one per scenario) independently, each carrying
the existing `threshold_crossings` array for that scenario. The Zone 1B per-scenario rows are
composed client-side by grouping the crossings from each scenario under its scenario header.
No backend change is required. The existing single-scenario trajectory endpoint already
returns `threshold_crossings` per scenario.

**Determination for Phase 3 Demo 7 scope:** Option 2 (client-side composition from N parallel
trajectory calls) is the Phase 3 implementation path. Rationale:

1. Option 2 requires zero backend changes for Phase 3 — the `threshold_crossings` field is
   already present per scenario trajectory response.
2. For the Demo 7 three-scenario comparison, N=3 parallel trajectory fetches adds negligible
   latency compared to a single N=3 compare endpoint call.
3. Option 1 (a generalized N-scenario compare endpoint) is the correct long-term architecture
   for N≥4 and for reproducibility (Lucas's "serializable comparison state" requirement from
   `persona-mvs-n3.md §Lucas MVS`). It is M18 scope.

**No new ADR is required for Zone 1B in Phase 3.** The client-side composition from N
parallel trajectory calls does not change the API contract — it is a frontend state management
change (holding N trajectory responses in the scenario comparison store instead of 2).

**M18 note:** When Option 1 is implemented for N≥4 and comparison state serialization, the
compare endpoint extension will require an API contract update in `api_contracts.yml` and
may trigger an ADR depending on the schema scope. That ADR is M18 scope, not M17.

---

### Q3: Does Zone 1D per-scenario PSP require a new endpoint or a client-side multi-scenario store structure?

**Answer: Client-side multi-scenario store extension only. No new endpoint required.**

The `programme_survival_probability` value is already available per scenario in the trajectory
response at `political_economy.indicators.programme_survival_probability` (per
`api_contracts.yml §DA-G5-4`). The existing endpoint returns this field; N=3 parallel
trajectory fetches provide three PSP values.

**What changes in the frontend:**

The scenario comparison store must hold N trajectory responses (one per scenario) and expose
each scenario's PSP for Zone 1D rendering. This is a state management extension — the store
changes from holding `(active: TrajectoryResponse, baseline: TrajectoryResponse)` to
`(primary: TrajectoryResponse, comparisons: TrajectoryResponse[])`. Zone 1D reads the PSP
field from each held response and renders the three-row PSP block.

This is a frontend store restructure, not an API change. **No new endpoint. No ADR required.**

---

## ADR Determination

**Determined option: (b) — Architecture review note on #394 is sufficient. No new ADR required
before Phase 3 implementation PR opens.**

Justification:
- Zone 1A N=3: component overlay extension within `TrajectoryView` boundary; no aggregation
  change; no rendering path change
- Zone 1B N=3: client-side composition from N parallel trajectory calls; no new endpoint;
  no API contract change
- Zone 1D N=3: client-side store extension; no new endpoint; no API contract change
- The ARCH-REVIEW-007 binding constraint (`COMPARE_VIEW N≤2/fixture`) governs entity-level
  fixture comparison; the G2 N=3 scenario comparison is structurally orthogonal and does not
  require the constraint to be revised

**This assessment constitutes the architecture review note on #394.** It must be filed as a
comment on GitHub issue #394 by the Architect before Phase 3 sprint entry is formally approved.

**If EL determines that the `scenarioTrajectories` prop refactor or the store restructure
warrants a formal ADR:** ARCH-012 is available (not yet ASSIGNED per `docs/architecture/backlog.md`;
Architect must check and mark ASSIGNED before authoring). However, the Architect's provisional
determination is that neither change crosses the threshold for a formal ADR — they are
implementation decisions within established architectural boundaries, not new architectural
decisions.

---

## Phase 3 Implementation Gate

The following conditions must be confirmed before the Phase 3 sprint entry is filed and
EL-approved:

| # | Condition | Status at authorship |
|---|---|---|
| 1 | #1249 (Zone 1A curve identifiability — N=2 fix) merged to `release/m17` | ⬜ Not yet merged — blocking Phase 3 PR open (not blocking Phase 2 or sprint entry filing) |
| 2 | BPO acceptance of Phase 1 Artifacts 1 and 2 on record (filed as BPO acknowledgment in `m17-g2-sprint-entry.md §Phase 2 review`) | ⬜ Pending BPO review of Phase 1 |
| 3 | ADR gate resolved — this assessment filed on #394; Architect review note acknowledged | ⬜ Pending filing on #394 |
| 4 | Zone 1B G3 dependency noted and non-blocking for Phase 3 start — `minHeight: 80px` MDA panel guarantee applies; G3 proportional allocation resolves overflow behavior | ✅ Noted in Artifact 1 and this assessment; non-blocking for Phase 3 |
| 5 | Zone 1D client-side store restructure confirmed as non-ADR scope (this assessment) | ✅ Confirmed |
| 6 | Phase 3 intent document filed at `docs/process/intents/M17-G2-{date}-multi-scenario-comparison.md` with data-testid anchors from Artifact 1 incorporated | ⬜ Pending Phase 1 BPO acceptance |
| 7 | QA test file `frontend/tests/e2e/m17-g2-multi-scenario-comparison.spec.ts` authored from intent document before implementation begins | ⬜ Pending intent document |

**Conditions 1 and 2 are the hard blocking conditions for Phase 3 PR open.** Conditions 3–7
are required before Phase 3 sprint entry EL approval. Condition 4 is confirmed non-blocking.

---

## Zone 1B Data Contract Clarification

**From `m17-g2-sprint-entry.md §2.2` — resolved in this assessment:**

The existing `threshold_crossings` field from the compare endpoint (G9, PR #1201) is
not used for N=3 Phase 3. Phase 3 uses N parallel trajectory calls with client-side
per-scenario composition. The compare endpoint's `threshold_crossings` field remains
available for the existing N=2 compare use case and is unaffected by G2 Phase 3.

Future M18 scope: the compare endpoint extension for N scenarios would include a
`per_scenario_threshold_crossings` field. This is the API contract change that may
require an ADR at M18. The M17 Phase 3 implementation does not touch the compare endpoint.

---

## Technical Risk Flags

**Risk 1 — Store refactor scope (medium risk):**
Extending `useScenarioStepStore` from `(active, baseline)` to `(primary, comparisons[])` is
a non-trivial store restructure. Components that currently read `trajectory` and
`baseline_trajectory` from the store must be updated to read from the new shape. This is a
straightforward but broad change — the implementing agent must audit all store consumers
before opening the Phase 3 PR. Estimated affected components: `TrajectoryView`, `MDAAlertPanel`,
`Zone1DCurrentPosition`, `Zone1DPSPWidget`.

**Risk 2 — Zone 1B overflow at N=3 with full crossings (medium risk):**
When all three scenarios have 2–3 threshold crossings, Zone 1B contains 6–9 crossing rows
plus 3 scenario headers. The G3 proportional allocation (#1252) is the correct fix. For Phase 3,
the `overflow-y: auto` on the per-scenario crossing section with `minHeight: 80px` on the
MDA alert panel is the minimum viable guard. This is not a blocking risk — it is a known
limitation with a documented workaround.

**Risk 3 — N=3 parallel trajectory fetch latency (low risk):**
Three parallel trajectory fetches are expected to resolve within 200–400ms (consistent with
current single-trajectory fetch performance). If any single fetch fails, the comparison state
shows the available scenarios with a per-scenario loading indicator. This is a standard
loading state pattern — no architectural concern.

**Risk 4 — COMPARE_VIEW state management for N>2 (low-medium risk):**
The existing COMPARE_VIEW state (`compare_scenario_id: string | null`) must generalize to
`comparison_scenario_ids: string[]`. Consumers that currently check `compare_scenario_id !== null`
to determine COMPARE_VIEW state must be updated. This is the same audit scope as Risk 1.

---

## Architect's Summary Statement

The G2 N=3 multi-scenario comparison is architecturally achievable within the existing
component and API boundary. No new ADR is required. The implementation involves:

1. A component prop extension in `TrajectoryView.tsx` (scenario palette, line-style assignment)
2. A frontend store restructure (`useScenarioStepStore` from N=2 to N-scenario shape)
3. No backend changes for Phase 3 (client-side composition from N parallel trajectory fetches)
4. Zone 1D PSP three-row block as a component extension of the existing Zone 1D panel

These changes are within the architectural boundaries established by ADR-017 (Zone 1A encoding
contract) and the existing COMPARE_VIEW specification. Phase 3 may proceed once the gate
conditions in §Phase 3 Implementation Gate are satisfied.

---

*Architect Agent — 2026-06-25. G2 Phase 2 Artifact 3. Issue #394.*
*Supplemental to ARCH-REVIEW-007 (2026-06-22). ADR determination: option (b) — review note on #394 sufficient.*
*Phase 3 gate confirmed. Provisional position: no ARCH-012 required.*
