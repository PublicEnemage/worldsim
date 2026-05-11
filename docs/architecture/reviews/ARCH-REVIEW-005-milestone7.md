# ARCH-REVIEW-005: Milestone 7 Exit — M8 Entry Blindspot Inventory

**Review type:** Targeted — M8 entry blindspot inventory before Ecological/Governance
module completion and ADR-005 extension authoring
**Scope:** Ecological and Governance module architecture; composite score normalization;
causal meta-map gate (Issue #218); mean-reversion channel (Issue #221); data
certification chain (Issues #252, #253)
**Facilitated by:** Architecture Review Facilitator
**Date:** 2026-05-10
**Status:** Complete — findings below; GitHub Issues created or referenced where noted

---

## Purpose

This review is the M7 exit / M8 entry architecture blindspot inventory. Milestone 7
delivered the Technical Foundation: `[SIM-INTEGRITY]` monitoring contract, STOCK
conflict detection, engine_version gap resolution, datetime deprecation cleanup, and
initial EcologicalModule and GovernanceModule. Milestone 8's core deliverable is
completing all four radar axes with real data.

Before M8 implementation decisions are locked — specifically before the ADR-005
extension for Ecological/Governance framework coverage is authored — every
architectural blindspot that M8 will expose must be named. This review identifies
six domains where the current M7 architecture will break, become ambiguous, or
produce false confidence when M8 module completion proceeds without addressing them.

---

## Domain 1: Ecological Module M8 Completion

### Current state

`EcologicalModule` (M6 minimum viable scope) produces two indicators:

- `co2_concentration_ppm` — `VariableType.STOCK`, confidence_tier 1 (NASA/NOAA)
- `land_use_pressure_index` — `VariableType.RATIO`, confidence_tier 3 (FAO GFR)

The module docstring explicitly documents M8 obligations:

> *"Full planetary boundary indicator set (`planetary_boundary_proximity`,
> `co2_trajectory`, `deforestation_rate`) added at M8 alongside
> boundary-normalized composite score methodology (ADR-005 Amendment 1
> §Amendment B M8 obligation)."*

The ecological composite score at M6 uses cross-entity percentile rank —
the same `_compute_composite_score()` function used by `financial` and
`human_development`. The API endpoint enforces a mandatory note on every
ecological `FrameworkOutput`:

> *"Ecological composite score uses cross-entity percentile rank at M6 scope.
> Planetary boundary absolute normalization is methodologically preferred and
> is deferred to M8 when the full indicator set is defined."*

### Blindspot 1-A: Planetary boundary absolute normalization has no designed computation path

The M8 obligation — boundary-normalized composite score — requires a fundamentally
different computation than percentile rank. Percentile rank is *relative*: it
measures where an entity sits among all entities in the snapshot. Planetary boundary
proximity is *absolute*: it measures where an entity's indicator value sits relative
to a fixed scientific reference threshold.

The current `_compute_composite_score()` function in `app/api/scenarios.py` is
framework-agnostic. It accepts a `framework: str` parameter but does not dispatch
on it — the same percentile rank calculation executes for all frameworks. When
governance is promoted in M8 and ecological normalization changes, this single
function must either be refactored into framework-specific dispatch or replaced with
a strategy pattern.

**The blindspot:** No design decision exists for how boundary normalization is
computed. The reference thresholds themselves (e.g., 350 ppm CO2 for the safe
climate space boundary — Rockström et al. 2009; updated Steffen et al. 2015) are
not registered in `source_registry`, not seeded as simulation reference data, and
have no database home. The `sources` table holds time-series data, not fixed
scientific reference constants. Storing planetary boundary thresholds requires either
a new table or a convention for how reference constants enter the simulation.

**What the ADR-005 M8 extension must decide:**

1. The normalization formula for ecological composite score: `indicator_value /
   boundary_threshold` (proximity ratio, 1.0 = at boundary, >1.0 = breached)?
   Or a scaled score (0 = far inside, 100 = at boundary)?
2. Which source(s) provide boundary thresholds and how they are registered.
3. The database location for fixed reference constants — new table, new column on
   `simulation_entities`, or a reference fixture file with a documented update
   protocol.
4. Whether `_compute_composite_score()` is extended with framework dispatch or
   replaced entirely.

### Blindspot 1-B: M8 indicator set is named but not defined

Three additional indicators are named in the module docstring:
`planetary_boundary_proximity`, `co2_trajectory`, `deforestation_rate`. None of
these are defined in `ECOLOGICAL_ELASTICITY_REGISTRY`. Before M8 implementation
begins, each indicator requires:

- A `VariableType` classification (STOCK, FLOW, RATIO, DIMENSIONLESS)
- A `confidence_tier` with source citation
- A data source registration (which data provider covers this indicator)
- An elasticity estimate with literature source via `LiteratureSourceRegistration`
  (DATA_STANDARDS.md §Data Provenance Requirements, from Issue #172 resolution)

The indicator set decision is upstream of the elasticity registry, which is upstream
of the module implementation. This sequence must be explicit before M8 implementation
issues are opened.

### Blindspot 1-C: `unit="dimensionless"` placeholder violates declared unit for `co2_concentration_ppm`

In `EcologicalModule.compute()` (`app/simulation/modules/ecological/module.py:121`),
all ecological indicator Quantities are produced with `unit="dimensionless"`:

```python
affected_attributes = {
    key: Quantity(
        value=delta,
        unit="dimensionless",   # ← placeholder
        ...
    )
    for key, delta in indicator_deltas.items()
}
```

The indicator `co2_concentration_ppm` declares its unit in its name. Using
`unit="dimensionless"` is internally inconsistent and would fail against any
canonical unit registry validation gate (Issue #252 Comment 1). The module
elasticities file acknowledges this gap in a comment ("Unit note: co2_concentration_ppm
is a STOCK...") but the unit is not correctly set in the Quantity constructor.

This is not a M8 new gap — it exists today. It is surfaced here because M8 will
expand the ecological indicator set, and if the `unit="dimensionless"` placeholder
pattern is used for new indicators, the unit gap multiplies.

**What must happen before M8 ecological indicators are implemented:** The unit
field must use the canonical unit string for each indicator, not a placeholder.
This requires the canonical unit registry (Issue #252 Comment 1) to exist first
so the correct unit string is defined. If the unit registry is not ready by M8
implementation start, the ecological module must at minimum use the indicator's
declared unit string (e.g., `"ppm"` for `co2_concentration_ppm`) rather than
`"dimensionless"`.

---

## Domain 2: Governance Module M8 Completion

### Current state

`GovernanceModule` exists and produces `rule_of_law_percentile` and
`democratic_quality_score`. However, `"governance"` remains in
`_UNIMPLEMENTED_FRAMEWORKS` in `app/api/scenarios.py:774`:

```python
_UNIMPLEMENTED_FRAMEWORKS = {"governance"}
```

This means the measurement-output API endpoint currently returns an empty
`indicators` dict and `composite_score=None` for governance — regardless of
what the engine computed. The governance module is operationally shielded from
the API surface. This is an intentional M6 scope decision.

### Blindspot 2-A: Governance composite score normalization methodology is undefined

When `"governance"` is removed from `_UNIMPLEMENTED_FRAMEWORKS`, the governance
framework will use `_compute_composite_score()` by default — the same percentile
rank function as financial and human_development. This may be acceptable for
governance (World Governance Indicators themselves express results as global
percentile ranks, 0–100), but the decision has not been made explicitly.

The question is not trivial: governance quality has established absolute floors
below which institutional function breaks down (a rule-of-law score below a
certain threshold means courts do not function as protection). A percentile rank
that places an entity at the 15th percentile of a scenario cohort tells a
different story than an absolute comparison to a functioning-institution floor.
Both are informative; neither substitutes for the other.

**What the ADR-005 M8 extension must decide:**

1. Whether governance uses percentile rank (consistent with financial and
   human_development) or an absolute normalization against institutional floor values.
2. If absolute: what are the floor values and which source registers them?
3. Whether the governance composite score explicitly surfaces "institutional floor"
   MDA alerts independently of the composite score value — a country at the 80th
   percentile of a scenario cohort that consists entirely of struggling states is
   not necessarily functioning well.

### Blindspot 2-B: `_UNIMPLEMENTED_FRAMEWORKS` promotion has no documented protocol

Removing `"governance"` from `_UNIMPLEMENTED_FRAMEWORKS` is a material change to
the API surface — it exposes governance scores that were previously hidden. No
documented protocol specifies what conditions must be met before this promotion
occurs:

- What test coverage is required? (Are governance indicator values tested in
  integration tests against known elasticity inputs?)
- Which ADR amendment is triggered? (ADR-005 M8 extension is the relevant document,
  but the promotion should be explicitly listed as a deliverable in that amendment.)
- Does the promotion require a compliance scan entry? (The pattern from M6 is that
  significant API surface changes appear in a compliance scan.)

Without a protocol, promotion will happen ad hoc — either too early (before
governance indicators are validated) or too late (after M8 closes with governance
still shielded). The protocol should be written in the ADR-005 M8 extension as a
named deliverable, not left to implementation judgment.

### Blindspot 2-C: Issue #211 references in Ecological and Governance module docstrings are stale

Both module docstrings contain:

> *"subscribes to gdp_growth_change which only fires when MacroeconomicModule is
> active. If MacroeconomicModule is absent, GDP-mediated [ecological/governance]
> effects are silently absent. Enforcement tracked in Issue #211 (M7)."*

Issue #211 is closed. The enforcement mechanism is architectural:
`web_scenario_runner.py:483` hardcodes `MacroeconomicModule` as always-active:

```python
modules: list[SimulationModule] = [MacroeconomicModule()]
```

The implicit dependency cannot be unmet because `MacroeconomicModule` is never
absent. The docstring references are stale — they describe a risk that the
architecture has already resolved. Stale risk references in module docstrings are
misleading to contributors and create false impressions that an open enforcement
gap exists.

**What must happen before M8 module commits:** The two docstrings must be updated
to reflect the resolved state — replacing the Issue #211 tracking note with a
statement that `MacroeconomicModule` is always active by architectural invariant
(web_scenario_runner.py) and is not a conditional dependency.

---

## Domain 3: Composite Score Normalization Architecture

### Current state

`_compute_composite_score()` in `app/api/scenarios.py:816` applies a single
normalization methodology — mean percentile rank — to all frameworks:

```python
def _compute_composite_score(
    entity_indicators: dict[str, QuantitySchema],
    all_entity_attrs: dict[str, dict[str, QuantitySchema]],
    framework: str,
) -> str | None:
    """Mean percentile rank of entity indicators across all entities at this step."""
```

The `framework` parameter is passed in but unused within the function body — the
same calculation executes regardless of framework.

### Blindspot 3-A: Framework dispatch does not exist but is required by M8

M8 will need at minimum two normalization paths:

1. **Percentile rank** — financial, human_development, possibly governance. Requires
   at least two entities in the snapshot (the `_SINGLE_ENTITY_NOTE` guard handles
   the degenerate case).

2. **Absolute boundary proximity** — ecological. Requires planetary boundary reference
   values (Blindspot 1-A). Entity count is irrelevant — a country at 415 ppm CO2
   is at a specific position relative to the 350 ppm boundary regardless of what
   other countries are doing.

The current function cannot support both paths. Either:

- The function gains framework-conditional branching, making its "mean percentile
  rank" docstring wrong for ecological cases; or
- The function is refactored into `_compute_composite_score_by_framework()` that
  dispatches to `_percentile_rank_score()` and `_boundary_proximity_score()`.

The refactoring decision is architectural — it changes the API between the endpoint
and the composite score computation — and must be decided before M8 implementation
begins to avoid a mid-milestone interface change.

### Blindspot 3-B: The single-entity guard applies to percentile rank only, not boundary normalization

`_SINGLE_ENTITY_NOTE` fires when `len(all_entity_attrs) == 1`. For percentile rank,
this is correct — rank is undefined with one entity. For boundary proximity
normalization, a single entity produces a meaningful score — the entity's absolute
distance from the planetary boundary is independent of peer count.

If ecological uses boundary normalization and governance uses percentile rank, the
`is_single_entity` guard must apply selectively by framework. Applying it uniformly
(current code) will suppress ecological scores in single-entity scenarios even when
those scores are meaningful.

**What the M8 implementation must resolve:** The `is_single_entity` guard must be
scoped to frameworks that use percentile rank, not applied to frameworks that use
absolute normalization.

---

## Domain 4: Causal Meta-Map Gate (Issue #218)

### Current state

Issue #218 (ARCH-REVIEW-005 — causal meta-map) is assigned to M8 and establishes
the machine-readable causal ontology that governs horizontal scaling decisions.
Issue #235 (Domain Intelligence Council blind interviews) is explicitly the gate
for Issue #218:

> *"This interview must be completed and synthesized before M8 architectural
> decisions are finalized — specifically before ARCH-REVIEW-005 (causal meta-map,
> Issue #218) is authored."*

### Blindspot 4-A: Sequence constraint between #235, #218, and M8 module decisions

The dependency chain is: **#235 interviews → #218 meta-map → M8 horizontal scaling
decisions**. However, M8's core deliverable (Ecological and Governance module
completion) consists of *within-contract* implementation decisions — filling out
indicator sets and elasticity registries established by existing ADR contracts.
These are not new horizontal scaling decisions; they are deliverables within ADR-005
Amendment B's existing scope.

The risk is that the #235/#218 dependency is interpreted as a gate on M8 module
completion work, when it should be a gate only on new horizontal scaling decisions
that would extend the simulation beyond its current four-framework architecture.

**What must be clarified before M8 kickoff:** The ADR-005 M8 extension must
distinguish between:

1. **Within-contract deliverables** (Ecological/Governance module completion,
   planetary boundary normalization, indicator set completion) — these proceed
   without waiting for #218.
2. **New horizontal scope decisions** (adding a fifth measurement framework,
   adding cross-domain relationship types beyond the four existing modules) —
   these require #218 to be complete first.

Without this distinction, the meta-map gate will either block deliverable work
unnecessarily or be ignored in a way that undermines its purpose for M9 scope.

### Blindspot 4-B: Module capability registry is not machine-readable

Issue #218 envisions `docs/architecture/causal-meta-map.yml` as machine-readable
causal ontology. The `docs/scenarios/module-capability-registry.md` is the current
closest artifact — it documents what each module can and cannot model. But it is
Markdown, not YAML, and has no structured schema for "declared but unimplemented"
relationships.

Before the meta-map is authored, a pre-creation checklist item from CLAUDE.md
§Canonical Artifact Locations applies: the Architect Agent must confirm the
canonical directory and naming convention for `causal-meta-map.yml` before creation.
Issue #218 proposes `docs/architecture/causal-meta-map.yml`. A find-based check
confirms no prior instances of this artifact type exist — the proposed location
stands, pending Architect Agent confirmation.

---

## Domain 5: Mean-Reversion Channel and Greece MAGNITUDE (Issue #221)

### Current state

`MacroeconomicModule` models `gdp_growth` as pure accumulation — it only moves
when a fiscal event fires. Issue #221 documents a concrete model failure: Greece
actual GDP improved from −8.9% (2011) to −6.6% (2012) without a positive fiscal
shock in the fixture, but the model produces −21.4% at step 2 and −31.4% at step 3
because no endogenous recovery mechanism exists.

The fix requires an endogenous mean-reversion term:

```
gdp_growth_t = gdp_growth_{t-1} + fiscal_delta + reversion_term
reversion_term = α × (trend_growth − gdp_growth_{t-1}) × regime_dampener
```

Issue #221 designates this as an ADR-006 amendment requiring Chief Methodologist
and Chief Engineer joint authorship.

### Blindspot 5-A: `trend_growth` is a new seeded attribute with no current home

The mean-reversion formula requires `trend_growth` as a country-level attribute
representing long-run potential growth rate. This attribute must be seeded per
country before any scenario using the recovery channel can run. The current entity
seeding infrastructure (Natural Earth loader, `simulation_entities` table) supports
`metadata` as a JSONB field but has no convention for seeding country-level
calibration parameters distinct from observational indicators.

Two options:

1. Seed `trend_growth` as a Quantity in `state_data` at step 0 (same as other
   initial state attributes). The backtesting fixture must be extended with this
   field for every case.

2. Store as a metadata field in `simulation_entities.metadata` JSONB — accessible
   to the engine without being a simulation state variable. Cleaner separation of
   calibration parameters from dynamic state, but requires a new read path in
   `MacroeconomicModule.compute()`.

**What the ADR-006 amendment must decide:** Where `trend_growth` lives and how it
is accessed. Option 1 is simpler but adds fixture maintenance overhead. Option 2
is architecturally cleaner but requires new infrastructure.

### Blindspot 5-B: ADR-006 Monte Carlo trigger second case blocked on #221

ADR-006 records a trigger condition: the Monte Carlo upgrade fires when two
independent MAGNITUDE_WITHIN_20PCT cases are validated. Argentina step 2 achieves
3.2% deviation (passing). Greece MAGNITUDE_WITHIN_20PCT at steps 2 and 3 is blocked
on #221.

Ecuador 1999–2000 (fixture referenced in commit 6b5714c) is named in Issue #221 as
a natural validation case for the recovery channel. If the mean-reversion channel
implementation achieves MAGNITUDE_WITHIN_20PCT on Ecuador step 2 (actual +2.8%
GDP recovery), Ecuador could serve as the second case, unblocking the Monte Carlo
trigger without waiting for Greece MAGNITUDE steps 2–3.

**What must be clarified in the ADR-006 amendment:** Whether Ecuador counts as a
qualifying independent case for the Monte Carlo trigger, or whether the trigger
requires a crisis-case pair (both crisis and recovery validated on the same case).
The intent of "two independent cases" was to test that the model generalizes, not
that it overfits to the calibration case. Argentina (default crisis) and Ecuador
(recovery year) are different enough to qualify as independent.

---

## Domain 6: Data Certification Architecture (Issues #252, #253)

### Current state

M8 brings the first significant wave of new data sources for Ecological and
Governance modules: World Governance Indicators (WGI), planetary boundary
reference thresholds (Rockström 2009 / Steffen 2015), potentially FAO SOFO data
for deforestation, and NASA/NOAA extended series for CO2. The current certification
architecture operates at source level (`source_registry`) with no field-level
certification (Issue #252) and no admission testing gate (Issue #253).

### Blindspot 6-A: WGI territorial conventions conflict with WorldSim declared positions

World Governance Indicators uses "Taiwan, China" as the entity label, which
conflicts with WorldSim's documented territorial position on Taiwan (DATA_STANDARDS.md
§Territorial Positions). When WGI is registered as a source and its data is loaded,
the territorial translation layer must resolve the label conflict.

This is not a new problem — the same resolution was required for other global
datasets. But WGI specifically covers Taiwan under a name that encodes a territorial
claim, not just a naming convention. The resolution decision (rename silently, flag
with a provenance note, or exclude the record) is a policy decision, not a
technical one. It must be documented in DATA_STANDARDS.md §Territorial Positions
before WGI is used in production simulation runs.

### Blindspot 6-B: `source_registry` has no `admission_status` field

Issue #253 proposes a mandatory data admission testing gate with `admission_status`
as a field on `source_registry`. This schema extension does not exist yet. When M8
registers WGI and planetary boundary sources, those sources will enter the system
without an admission status — either the field is added before M8 data loading,
or M8 data sources bypass the future admission gate by predating it.

The correct approach is to add `admission_status` to `source_registry` early (as
`UNTESTED` default for all existing sources) so that M8 data onboarding can use
the field even before the full admission testing infrastructure exists. This creates
the hook for the future gate without blocking M8 data loading.

**What must be designed before M8 data loading begins:** The `source_registry` schema
extension for `admission_status`. This is a schema change that requires a Data
Architect agent review and a `docs/schema/database.yml` update in the same commit.

---

## Consolidated Decisions Required Before M8 Implementation

Each decision below is a blocking prerequisite for specific M8 implementation
issues. None require the causal meta-map (#218) to be complete first.

| Decision | Domain | Blocking |
|---|---|---|
| Ecological composite score normalization formula (percentile rank → boundary proximity) | 1 | Ecological module completion |
| Planetary boundary reference values: source registration + database location | 1 | Ecological composite score |
| M8 ecological indicator set: `planetary_boundary_proximity`, `co2_trajectory`, `deforestation_rate` — VariableType, confidence_tier, source | 1 | Ecological elasticity registry |
| `unit="dimensionless"` placeholder replacement for existing ecological indicators | 1 | Canonical unit registry (Issue #252) |
| Governance composite score normalization: percentile rank or absolute institutional floor | 2 | Governance module promotion |
| `_UNIMPLEMENTED_FRAMEWORKS` promotion protocol: test coverage gate, ADR amendment trigger | 2 | Governance API promotion |
| Ecological/Governance module docstrings: replace stale Issue #211 references | 2 | Code hygiene (no blocking) |
| `_compute_composite_score()` refactor: framework dispatch vs. branching | 3 | Both Ecological + Governance composite scores |
| `is_single_entity` guard scoping: percentile-rank-only frameworks vs. boundary-proximity frameworks | 3 | Ecological single-entity scenario correctness |
| Within-contract vs. new-horizontal-scope boundary: clarify what #218 gates | 4 | M8 kickoff sequencing |
| `trend_growth` seeding approach: initial state Quantity vs. metadata field | 5 | Issue #221 implementation |
| Ecuador as qualifying Monte Carlo trigger second case: yes or no | 5 | ADR-006 trigger evaluation |
| `source_registry.admission_status` field: add before M8 data loading | 6 | Issue #253 future-proofing |
| WGI territorial convention: resolution policy for "Taiwan, China" label | 6 | WGI data registration |

---

## Known Limitations of This Review

This review was conducted from:
- `app/simulation/modules/ecological/module.py` and `elasticities.py`
- `app/simulation/modules/governance/module.py` and `elasticities.py`
- `app/api/scenarios.py` (composite score and framework output logic)
- `app/simulation/web_scenario_runner.py` (module instantiation)
- Issues #211, #218, #221, #235, #252, #253
- ADR-001 through ADR-006, CLAUDE.md M8 scope

It did not include:

- `MacroeconomicModule` source code — mean-reversion channel assessment (Domain 5)
  is based on Issue #221's root cause analysis, not code inspection.
- `DemographicModule` elasticity registry — the cross-module elasticity consistency
  question (whether demographic elasticities are correctly scaled for the GDP
  transmission chain) was not reviewed.
- The frontend `EntityDetailDrawer` / `RadarChart` — how boundary-normalized
  ecological scores will be displayed differs from percentile scores; this is
  frontend architectural work that follows the normalization decision.

These gaps do not change the decisions required. They are implementation-verification
tasks downstream of the architectural decisions identified here.

---

## Engineering Lead Dispositions

*To be recorded after Engineering Lead review.*

*Single-principal governance limitation applies — see CLAUDE.md §Governance.
This review was produced at M7 exit and approved by the same individual who holds
full repository authority. No independent review is available at this governance
stage. See CLAUDE.md §Governance for the documented plan to address this limitation.*
