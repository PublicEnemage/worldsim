---
name: m12-sprint-plan
type: sprint-plan
milestone: M12 — Active Control and External Sector
status: Active
authored-by: PM Agent
authored-date: 2026-06-05
el-approved: 2026-06-05
consulted:
  - Business Product Owner (value prioritization)
  - Frontend Architect (file area grouping)
  - Chief Engineer (dependency sequencing)
  - Architect (ADR prerequisites)
sop: docs/process/sprint-planning-sop.md
---

# M12 Sprint Plan — Active Control and External Sector

**Milestone:** M12 — Active Control and External Sector (GitHub Milestone 13)  
**Release branch:** `release/m12`  
**Exit checklist:** Issue #263  
**HORIZON sweep:** 2026-06-05 (kickoff ceremony)

---

## Grouping Rationale

Groups are organized by shared file areas and dependency chains. A group is one PR (or two ordered PRs for G6). Tests ship with the code in the same PR — no separate test PRs. Playwright E2E assertions ship in the same PR as the feature they gate.

---

## Wave 1 — Parallel (no cross-dependencies)

All four Wave 1 groups can be worked and merged in any order. No group depends on another within this wave.

### G1 — Instrument cluster display: #744 + #747 ✓ DONE (2026-06-05, PR #762)

**Why grouped:** Both are frontend-only additions to the Zone 1 component area. Existing `/measurement-output` already surfaces the cohort data; these issues add display. No backend changes. Sharing a PR reduces context switching across the same component tree.

**Shared files:** `ScenarioInstrumentCluster.tsx`, Zone 1A/B/C/D component tree, choropleth component (active entity highlight), layout/header area, possibly `measurement-output` API response type shape (read-only).

**Tests:** Component unit tests for header element and cohort indicator panel. Playwright legibility assertion at 1440×900 confirming header is visible in screenshot without scroll (required by #744 AC). Both test additions live in the same PR.

**Acceptance gates:**
- Persistent header visible in any main-viewport screenshot: `Scenario / Entity / Status`
- Active country highlighted on choropleth when scenario loaded
- Four cohort indicators in Zone 1 with value + direction + tier, alongside composites
- Cold-start agent can identify loaded scenario in turn 1 from screenshot alone

**Execution narrative:** Frontend-only PR with no backend changes. Two new components: `ScenarioIdentityHeader` (Zone 0 banner: Scenario / Entity / Status) and `CohortIndicatorsPanel` (Zone 1A strip with 4 HD indicators, polarity-aware direction arrows, confidence tier badges). Atomic `hdState` pattern (single useState) prevents stale-closure on current→prev indicator swap. Choropleth amber highlight layer added on active scenario entity. 28 unit tests across `formatStatus`, `computeDirection`, `directionGlyph`, `formatIndicatorValue`. Build gate clean. Zero backend changes required — measurement-output API already surfaced the HD data.

---

### G2 — Alert panel drill-in: #745 ✓ DONE (2026-06-05, PR #764)

**Why own group:** Alert panel expansion is architecturally distinct from display additions — it introduces click state, expansion behaviour, and possibly alert API enrichment. Different component, different interaction model. The backend surface is narrow (ensure `indicator_name` is non-null in alert response; `/trajectory` already provides the time-series data).

**Shared files:** `MDAAlertPanel.tsx` (major rewrite), alert API response shape (minor — `indicator_name` non-null enforcement).

**Tests:** Component interaction test (click → expand → time-series visible). API unit test asserting `indicator_name` is never null. Playwright: click on TERMINAL alert → detail view opens with indicator name, threshold line, and step of crossing highlighted.

**Acceptance gates:**
- Click on any alert row opens detail view: indicator time-series, MDA threshold reference line, step of crossing
- Human-readable indicator name always present
- "See alerts" text in zone-1d navigates to alert detail for that framework's primary alert
- Alert text legible at 1440×900

**Execution narrative:** Backend + frontend change. Backend: `indicator_name: str` added to `MDAAlert` schema — always non-null, title-cased from `indicator_key` via `_indicator_name()` helper, persisted in `events_snapshot` JSONB with fallback reconstruction for historical snapshots. Frontend: `Zone1BAlert` store type extended with `indicator_name`, `floor_value`, `current_value`, `approach_pct_remaining`, `consecutive_breach_steps`. Alert rows made clickable (toggle on/off); `focusedAlertMdaId` local state in `ScenarioInstrumentCluster` (UI state, not simulation state) wired to both Zone 1B and Zone 1D. `AlertDetailPanel` renders inline below the list: indicator display name (frontend registry overrides backend title-case), SVG sparkline of framework composite score trajectory with dashed MDA floor line and crossing step marker, value snapshot grid. Zone 1D gets "Primary dimension — see alerts →" button per framework row. `buildSparklinePoints` pure function + 7 new tests; 170 total tests passing.

---

### G3 — Mode 2 fiscal multiplier: #746 ✓ DONE (2026-06-05, PR #767)

**Why own group:** Has both backend schema changes (new `fiscal_multiplier` field) and a significant frontend addition (overlay comparison in `TrajectoryView.tsx`). Backend work is isolated to scenario creation path. This is the entry point for Mode 2 — keeping it separate from G1/G2 prevents a single large PR from mixing three concerns.

**Shared files:** `scenario_schemas.py` / Pydantic models (`fiscal_multiplier` field), `simulation_runner.py` (pass-through to propagation), `TrajectoryView.tsx` (two-curve overlay display), scenario creation form component (new parameter input).

**ADR prerequisite:** None — fiscal multiplier is an existing engine parameter being exposed; no new architectural boundary.

**Tests:** API schema test (fiscal_multiplier field accepted, validated 0.1–3.0). Simulation runner unit test (fiscal_multiplier propagates through). Playwright: configure two multiplier values → both curves visible in overlay → legend identifies each.

**Acceptance gates:**
- Fiscal multiplier configurable from scenario creation UI (0.1–3.0 range, default 1.0)
- Two-curve overlay or side-by-side comparison mode
- Active multiplier assumption visible in main viewport at all times
- Poverty headcount and health system capacity respond to multiplier change

**Gates:** G6b (#753 Mode 3) — fiscal multiplier is Mode 3's first instrument.

**Execution narrative:** Backend + frontend change. Backend: `fiscal_multiplier: float` added to `ScenarioConfigSchema` with Pydantic `Field(ge=0.1, le=3.0)`, default 1.0. `MacroeconomicModule.__init__()` now accepts `fiscal_multiplier_override: float = 1.0`, stored as `Decimal` and applied to both spending and tax multiplier paths (`FISCAL_MULTIPLIERS[regime] * override`). `_build_active_modules()` passes `config.fiscal_multiplier` through — no modules_config indirection. Frontend: fiscal multiplier range slider (0.1–3.0, step 0.1) added to scenario creation form with orange highlight and "Mode 2" indicator when override is active. `ScenarioIdentityHeader` gains `fiscalMultiplier` prop and `formatMultiplierLabel()` pure function — shows "Mode: 2 (Fiscal ×N.N)" in the persistent identity strip when override ≠ 1.0. `TrajectoryView` now shows baseline overlay when `mode === "MODE_2" || mode === "MODE_3"` (previously MODE_3 only), with legend entries in MODE_2. `ScenarioInstrumentCluster` accepts `comparisonScenarioId` prop — fetches that scenario's trajectory and stores as `baseline_trajectory`; sets MODE_2 when `fiscalMultiplier ≠ 1.0`. `App.tsx` extracts `fiscal_multiplier` from scenario detail and wires through. 7 new backend unit tests (schema validation, module constructor, `_build_active_modules` wiring); 8 new frontend unit tests (`formatMultiplierLabel`). 177 total frontend tests passing, ruff + build gate clean.

---

### G4 — Matrix engine production migration: #749

**Why own group:** Major backend-only architectural change. Promotes `propagate_matrix()` to the default call site, demotes iterative engine. The full backtesting suite is the test — no new test files needed, but all existing backtesting assertions must pass against the matrix engine before this merges.

**Shared files:** `matrix_propagation.py`, `simulation_runner.py` (swap call site), backtesting test suite, `test_equivalence_harness.py`, CI workflow (confirm matrix is the test target), ADR-009 status update to IMPLEMENTED.

**Tests:** Full backtesting suite passing on matrix engine. ADR-009 §Decision 3 Monte Carlo gate (1000× 15 steps) confirmed in production configuration. No fallback to iterative without explicit log entry.

**Acceptance gates:**
- `propagate_matrix()` is default for all new scenario steps
- Full backtesting suite passes (no regressions from M11 baseline)
- ADR-009 §Decision 3 performance gate confirmed on target hardware (ProBook i5-8265U)
- No silent fallback; any fallback is logged and surfaced
- ADR-009 updated to IMPLEMENTED

**Gates:** G5, G6, G7, G8 — everything downstream runs on the production engine.

---

## Wave 2 — After G4

### G5 — External sector module: #751 + #752

**Why grouped:** `BilateralTradeShock` (#751) lays the propagation routing infrastructure; `CommodityPriceShock` (#752) extends it for global-parameter distribution. Writing both together avoids two separate migrations to the same schema tables and two separate additions to the same input-type dispatch logic. #751 is a blocking prerequisite for #752.

**ADR prerequisite:** External sector module ADR must be authored and accepted before any implementation merges. Check `docs/architecture/backlog.md` for next available number and assign before drafting.

**Shared files:** New `external_sector.py` module, `scenario_schemas.py` (new scheduled input types), DB migration, relationship graph traversal in propagation layer, human cost linkage (bottom-quintile consumption channel for both shock types). Single test file covers both shock types.

**Tests:** Shock propagation unit tests (both types). Zero-dependency entity case (no effect). Human cost channel activation (bottom-quintile cohort responds within 2 steps). Import dependency coefficient fixture for Jordan (Demo 4 entity; synthetic Tier 3 flagged). Historical directional validation — 2008 oil price spike as reference for commodity shock.

**Acceptance gates:**
- `BilateralTradeShock` and `CommodityPriceShock` accepted by scenario creation API
- Both propagation types reach financial framework indicators within 1 step
- Human cost ledger shows cohort-level effects within 2 steps for both types
- External sector ADR accepted before implementation merges
- Jordan commodity import dependency coefficients in fixture (Tier 3 flagged)

**Gates:** G6, G8.

---

### G7 — Cloud compute path doc: #750

**Why own group:** Pure documentation. No code. Writes `docs/architecture/cloud-compute-path.md` (new file). Can be done any time after G4 merges — needs real matrix engine performance numbers to cite accurately.

**Shared files:** `docs/architecture/cloud-compute-path.md` (new). Requires CE review (performance accuracy).

**Tests:** None.

**Acceptance gates:**
- Document covers: what triggers cloud need, minimum viable laptop config, cloud provider options with pricing, self-hosted alternative
- Equitable Build Process constraint confirmed: standard single-country scenario stays within 8GB/4-core envelope

---

## Wave 3 — After G3 + G4 + G5

### G6a — Multi-country scenario backend: #754

**Why own group (first half of G6):** Backend-heavy. Adds `entity_ids: list[str]` to scenario creation, seeds multiple entities independently, populates relationship edges at creation, passes multi-entity runs through the matrix engine. The choropleth multi-entity highlight is a small frontend touch that ships in this PR rather than creating a micro-PR later.

**Shared files:** `scenarios.py` API endpoint, `scenario_schemas.py` (`entity_ids` field), DB migration (entity membership, relationship edges), `simulation_runner.py` (multi-entity loop), choropleth component (highlight multiple active entities simultaneously), scenario identity header (#744) extended to list all active entities.

**Tests:** API test (multi-entity creation, relationship seeding). 2-entity step advance performance gate (≤ 1.5× single-entity wall time on matrix engine). Synthetic relationship weight edge case (missing edges → Tier 4 weight, flagged).

**Acceptance gates:**
- Scenario creation API accepts `entity_ids: list[str]` (minimum 1, up to 5)
- Each entity independently seeded from source registry
- Commodity price shock (#752) distributes to all entities in one step
- Choropleth highlights all active entities
- Demo 4 Jordan scenario runs with 2 entities (Jordan + commodity reference)
- Performance gate: 2-entity step ≤ 1.5× single-entity on matrix engine

---

### G6b — Mode 3 Active Control: #753

**Why own group (second half of G6):** Frontend-heavy. Activates `zone-control-plane`. Depends on G6a (multi-entity backend) and G3 (fiscal multiplier as first instrument). ADR-008 reserved the control plane layout zone — verify whether Mode 3 interaction model is covered or requires an ADR amendment before implementation begins.

**Shared files:** `zone-control-plane` component (new), `App.tsx` (mode routing and mode indicator), `TrajectoryView.tsx` (A/B baseline vs. modified display — builds on G3's overlay work), `zone-1d` human cost delta display, mode indicator component.

**ADR prerequisite:** Confirm ADR-008 covers Mode 3 interaction model sufficiently, or file an amendment before implementation begins.

**Tests:** Playwright E2E — parameter change → trajectory recompute → both curves visible → delta in zone-1d, on Greece fixture. Mode 3 → Mode 1 → Mode 3 roundtrip without losing scenario. Performance: parameter change → update ≤ 100ms on ProBook i5-8265U (MV-002 Mode 3 gate).

**Acceptance gates:**
- `zone-control-plane` renders at least two configurable policy instruments without scroll
- Parameter change → trajectory update ≤ 100ms on ProBook
- Baseline and modified trajectories simultaneously visible with legend
- Human cost delta visible in zone-1d within same update cycle
- A/B comparison is default when parameter changed (no manual enable)
- Mode 3 reachable from Mode 1 and Mode 2 without losing loaded scenario

---

## Wave 4 — After G1–G6 all merged

### G8 — Demo 4 preparation: #755

**Prerequisites:** #744, #749, #751, #752, #753, #754 all merged. Jordan fixture data available. This group is the integration test of everything built in Waves 1–3.

**Shared files:** `backend/scripts/demo_hormuz_jordan.py` (new), `docs/demo/m12/` (new milestone demo directory per canonical artifact convention), narration document (NARRATION-RULING-1 three-layer structure), IR stakeholder review artifact at `docs/demo/m12/reviews/YYYY-MM-DD-vX.X.X-stakeholder-review.md`.

**Tests:** Demo script runs end-to-end on ProBook i5-8265U without cloud infrastructure. All screenshots pass legibility gate at 1440×900 (demo-legibility.spec.ts). Jordan fixture seeds without errors; all synthetic indicators flagged at indicator level.

**Acceptance gates:**
- Jordan fixture seeds cleanly; synthetic indicators flagged
- Hormuz scenario advances 8 steps without hitting irreversible thresholds before step 4
- Mode 3 parameter adjustment demonstrably changes the trajectory
- Human cost indicators show non-zero response to commodity shock within 2 steps
- Demo runs end-to-end on ProBook within performance budget
- Narration document reviewed against NARRATION-RULING-1
- IR stakeholder review artifact in `docs/demo/m12/reviews/`

---

## Near-Term Backlog (any wave, capacity-dependent)

| Issue | Work type | Notes |
|---|---|---|
| #725 | Backend dep — mypy pin | One-line change; rider on any backend PR |
| #644 | Frontend tooling — ESLint audit | Standalone; between any two frontend waves |
| #394 | Multi-scenario comparison (>2) | Builds on G6a; treat as Wave 3 if capacity allows |

---

## Dependency Map

```
Wave 1 (parallel):   G1 · G2 · G3 · G4
Wave 2:              G5 (needs G4) · G7 (needs G4)
Wave 3:              G6a (needs G3 + G4 + G5) → G6b (needs G6a)
Wave 4:              G8 (needs G1–G6 all merged)
```

**Critical path:** G4 → G5 → G6a → G6b → G8

G1, G2, and G3 run on the parallel track. They must merge before G8 (Demo 4 requires instrument cluster and Mode 2) and before G6b (fiscal multiplier is Mode 3's first instrument).

---

## ADR Prerequisites

| Group | ADR requirement |
|---|---|
| G5 | External sector module ADR — new module boundary. Must be authored and accepted before G5 implementation merges. Check `docs/architecture/backlog.md` for next number. |
| G6b | Confirm ADR-008 covers Mode 3 interaction model, or file amendment. Before G6b implementation begins. |
| All others | No ADR prerequisite. |
