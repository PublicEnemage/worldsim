# ADR-005 Amendment 3 — Working Draft

> **Status:** ACCEPTED — committed to ADR-005-human-cost-ledger.md on 2026-05-17.
> Revision 2 accepted by Engineering Lead. Amendment text committed to
> `docs/adr/ADR-005-human-cost-ledger.md` as Amendment 3. Issue #218 closed.
> This file is preserved as a historical record of the draft and panel review process.
> See `docs/adr/ADR-005-human-cost-ledger.md §Amendment 3` for the authoritative text.
> Panel synthesis: `docs/architecture/adr-005-amendment3-panel-synthesis.md` (PR #303).

---

## Amendment 3 — M8 Ecological Framework Completion: Boundary Normalization, Strategy Dispatch, and Governance Deferred Axis

**Date:** 2026-05-17
**Closes:** #218 (ADR-005 M8 amendment — blocking prerequisite for M8 Ecological Module completion)
**Context:** Amendment 1 §Amendment B named this amendment explicitly as a blocking
prerequisite for M8 Ecological Module completion:

> *"An ADR-005 Amendment 2 addressing planetary boundary absolute normalization is a
> blocking prerequisite for M8 Ecological Module completion. This amendment explicitly
> names that obligation."*

That obligation is satisfied here — renumbered Amendment 3 because Amendment 2
(DemographicModule subscription contract) was interposed.

This amendment fires the renewal trigger listed in the Validity Context §Renewal
Triggers: *"Radar chart normalization methodology changed from percentile-based
cross-entity ranking to an alternative."* The ACCEPTED → UNDER-REVIEW transition
fires as of this amendment. The amendment itself constitutes the required review;
Engineering Lead acceptance returns the ADR License Status to CURRENT.

---

### Confirmations — No Amendment Required

**Q1 — EcologicalModule `SimulationModule` interface compatibility at M8:**
EcologicalModule's `compute(entity, state, timestep) -> list[Event]` and
`get_subscribed_events() -> list[str]` interface is unchanged at M8. The module
subscribes to GDP and fiscal events from MacroeconomicModule and produces ecological
indicator updates — this contract extends from M6 minimum viable scope without
modification. No new interface methods are required.

EcologicalModule at M8 remains an event consumer. Ecological state changes do not
generate propagation events into financial or governance modules. This is a confirmed
M8 scope boundary, not an oversight: the cross-domain ecological→financial propagation
path (e.g., fisheries depletion below MSY threshold → export revenue event → fiscal
event) requires backtesting validation before it can be a committed propagation path.
It is a M10 Engine Integrity scope item. The Ecological Economist's blind interview
finding (Issue #218 Council comment, docs/process/council-interview-2026-05-11.md
§Theme 3) must be documented in the causal meta-map (ARCH-REVIEW-005 obligation)
before M8 implementation is locked; it does not require an amendment here.

**Q2 — `MeasurementFramework` taxonomy unchanged:**
The four `MeasurementFramework` values (`FINANCIAL`, `HUMAN_DEVELOPMENT`, `ECOLOGICAL`,
`GOVERNANCE`) remain unchanged. No new framework values are added by this amendment.
The renewal trigger "MeasurementFramework taxonomy modified in any standards document
or ADR amendment" does not fire.

**Q3 — `mda_thresholds` schema extension:**
The MDA threshold system (Decision 3) requires no schema migration to accommodate
ecological or governance MDA thresholds at M8. The `mda_thresholds` table supports
any `indicator_key` and `comparison_operator` pair. New threshold seed data for
`planetary_boundary_co2_proximity > 1.0` and `planetary_boundary_land_use_proximity
> 1.0` must be added via a dedicated Alembic migration as part of the M8
EcologicalModule implementation. GovernanceModule MDA thresholds are deferred with
module promotion to M9.

---

### Decision M8-1: Ecological Composite Score — Boundary Proximity Normalization Formula

#### The problem

Amendment 1 §Amendment B established that Decision 2's percentile-rank methodology
is a category error for planetary boundary indicators: if all 177 entities in a
simulation exceed CO2 planetary boundaries — which is the current empirical reality —
percentile scores remain stable while every entity is in an unsafe operating space.
Amendment B scoped this as a deliberate M6 exception with mandatory disclosure, and
named the M8 obligation:

> *"Planetary boundary absolute normalization is methodologically preferred and is
> deferred to M8 when the full indicator set is defined."*

The normalization formula must now be specified so that M8 implementation can proceed.

#### Decision — Boundary proximity ratio, capped at 2.0

The ecological composite score normalization formula is:

```
boundary_score = min(current_value / boundary_value, 2.0)
```

**Score semantics:**
- `< 1.0` — Entity operates within the safe operating space
- `= 1.0` — Entity is exactly at the planetary boundary
- `> 1.0` — Planetary boundary exceeded
- `= 2.0` — Display ceiling: "double the safe boundary" — boundary exceedance beyond this is capped

The composite `ecological` score in `MultiFrameworkOutput` is the **mean boundary_score**
across all ecological indicators for which a boundary constant is registered.
Indicators without a registered boundary constant are excluded from the composite and
must carry a `note` disclosing the exclusion. Indicators lacking a boundary constant
must emit a `[SIM-INTEGRITY]` WARNING at computation time.

Boundary constant values are read from the `simulation_reference_constants` table
(Alembic migrations `a2b4c6d8e0f1` + `b3c5d7e9f1a2`). The query must respect
`effective_from` and `effective_through` to handle future boundary value revisions.
Constants active at M8:

| `constant_id` | Value | Unit | Source |
|---|---|---|---|
| `ECOLOGICAL_CO2_PLANETARY_BOUNDARY_PPM` | 350 | ppm | Rockström et al. 2009, *Nature* 461:472–475. doi:10.1038/461472a |
| `ECOLOGICAL_LAND_USE_PLANETARY_BOUNDARY_RATIO` | 0.25 | ratio_0_1 | Richardson et al. 2023, *Science Advances* 9(37). doi:10.1126/sciadv.adh2458 |

#### Why this formula over the alternatives

**Alternative 1 rejected — absolute difference (`current_value - boundary_value`):**
Produces indicator-specific scales with no interpretable ceiling. A CO2 difference of
70 ppm and a land-use difference of 0.1 cannot be meaningfully averaged without unit
conversion that embeds domain-specific weighting choices. The ratio form is unit-agnostic
across boundary types.

**Alternative 2 rejected — inverse proximity (`1 - current_value / boundary_value`):**
Produces negative values above the boundary: CO2 at 421 ppm yields a score of −0.203.
Negative composite scores misrepresent meaning — a score of −0.4 is not "twice as bad"
as −0.2 in a monotonically interpretable sense. The accepted formula preserves
monotonicity above the boundary (higher ratio = further from safety) while the cap
at 2.0 prevents runaway values.

**Alternative 3 rejected — retained percentile rank (existing M6 approach):**
Confirmed category error in Amendment 1. The M6 exception was deliberate and bounded;
Amendment 1 closed the M8 obligation explicitly. This alternative is foreclosed.

**Accepted formula rationale:** The ratio `current_value / boundary_value` is
interpretable without ecological domain expertise: any score above 1.0 means the
boundary is crossed. The cap at 2.0 creates a finite, comparable display range. This
convention is idiomatic to the planetary boundary literature — Rockström et al. express
boundary exceedance as a ratio of current state to the boundary value, making
WorldSim's output directly comparable to the peer-reviewed source.

#### Mandatory API note — supersedes Amendment 1 §Amendment B ecological note

The Amendment 1 §Amendment B mandatory note:
> *"Ecological composite score uses cross-entity percentile rank at M6 scope.
> Planetary boundary absolute normalization is methodologically preferred and is
> deferred to M8 when the full indicator set is defined."*

is **superseded** by this amendment. The mandatory `FrameworkOutput.note` for
`measurement_framework == "ecological"` at M8 is:

> *"Ecological composite score: mean boundary proximity ratio across registered
> indicators (formula: min(current_value / boundary_value, 2.0)). Score 1.0 =
> boundary exactly met; >1.0 = boundary exceeded; cap 2.0 = double safe boundary.
> Indicators without a registered planetary boundary constant are excluded from the
> composite. Source: simulation_reference_constants table."*

Any code path returning an ecological `FrameworkOutput` without this note is
non-compliant with this amendment. The `_ECOLOGICAL_MANDATORY_NOTE` constant in
`backend/app/api/scenarios.py` must be updated to this text in the same commit as
the boundary strategy implementation.

#### Implementation obligations

1. `_compute_composite_score()` in `backend/app/api/scenarios.py` must be refactored
   to a strategy dispatch (see Decision M8-3) before the boundary formula is implemented.
   Boundary formula must not be implemented as an if/elif branch alongside the
   percentile-rank path.

2. Boundary constant values must be read from the database (`simulation_reference_constants`
   table) at composite score computation time, not hardcoded. The query must respect
   `effective_from` and `effective_through` to handle future boundary value updates.

3. `_ECOLOGICAL_MANDATORY_NOTE` in `backend/app/api/scenarios.py` must be updated to
   the new mandatory note text (above). The old text is a compliance artifact from
   Amendment 1; retaining it after M8 implementation is a non-compliance.

4. Indicators that lack a registered boundary constant must log a `[SIM-INTEGRITY]`
   WARNING and exclude themselves from composite score computation, per
   `CODING_STANDARDS.md §Simulation Integrity Monitoring`.

---

### Decision M8-2: `is_single_entity` Guard — Ecological Framework Exemption

#### The problem

`_compute_composite_score()` in `backend/app/api/scenarios.py` contains an
`is_single_entity` guard that suppresses composite scores in single-entity scenarios,
attaching `_SINGLE_ENTITY_NOTE` to the `FrameworkOutput`. The guard exists because
a percentile rank with one entity is numerically undefined.

Boundary proximity normalization does not require multiple entities. CO2 at 421 ppm
relative to the 350 ppm boundary yields boundary_score = 1.203 regardless of how many
entities are present. The guard, applied uniformly, produces a false null ecological
composite score in single-entity scenarios (e.g., the Greece 2010–2015 demo fixture).

The UX Agent ruling (Issue #218, 2026-05-16) named this requirement explicitly:
> *"Boundary-normalized ecological scores are physically meaningful for single-entity
> scenarios (CO2 vs. 350 ppm boundary). The is_single_entity guard must not suppress
> ecological composite scores. This exemption must be specified in the ADR-005 M8
> amendment — it cannot be handled as an implementation-time judgment call."*

#### Decision — Ecological framework exempt; financial and human_development retain guard

| Framework | `is_single_entity` guard | Rationale |
|---|---|---|
| `financial` | Applies — composite score suppressed to null | Percentile rank undefined for single entity |
| `human_development` | Applies — composite score suppressed to null | Percentile rank undefined for single entity |
| `ecological` | **Exempt** — boundary proximity score computed and returned | Boundary ratio is entity-count-independent |
| `governance` | Not applicable at M8 — null axis, deferred to M9 | Guard interaction specified at M9 promotion |

The default assumption at M9 governance promotion is that governance uses percentile
rank and retains the guard. Any exemption for governance requires a Decision M9-N
amendment naming the exemption and its rationale.

#### Implementation obligations

1. Replace the unconditional `is_single_entity` guard in `_compute_composite_score()`
   with a check against a named constant `_SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS:
   frozenset[str]`, initialized to `frozenset({"ecological"})`.

2. `_SINGLE_ENTITY_NOTE` must not appear on ecological `FrameworkOutput`.

3. The exempt frameworks constant must be a module-level named constant (not an inline
   literal) so that the addition of governance at M9 is visible in code review and
   triggers the same-commit ADR amendment requirement (see §Renewal Triggers).

---

### Decision M8-3: `_compute_composite_score()` — Strategy Dispatch Pattern

#### The problem

`_compute_composite_score()` currently applies the same percentile-rank calculation
to all frameworks, ignoring the `framework` parameter. The DISPATCH DESIGN NOTE
embedded in the function's docstring (added during M7 STD-REVIEW-004 Gaps 4 and 5)
required:

> *"The implementation must use a strategy dispatch pattern so that governance can
> extend it without requiring a refactor. Design once for both, implement ecological
> first. Both ecological and governance normalization strategies must be added in the
> same ADR-005 M8 amendment commit — do not implement ecological strategy alone."*

The strategy dispatch design must be specified before implementation proceeds.

#### Decision — Framework-keyed callable map with named fallback; governance registration point defined

Strategy dispatch uses a module-level `dict[str, Callable]` keyed by framework string,
with the percentile-rank strategy as the explicit fallback for unregistered frameworks:

```python
_COMPOSITE_STRATEGIES: dict[str, Callable[..., Decimal | None]] = {
    "ecological": _boundary_proximity_strategy,
    # governance: registered at M9 promotion in the same commit as _UNIMPLEMENTED_FRAMEWORKS removal
    # See ADR-005 Decision M8-4.
}
_DEFAULT_COMPOSITE_STRATEGY = _percentile_rank_strategy
```

Dispatch logic inside `_compute_composite_score()`:

```python
strategy = _COMPOSITE_STRATEGIES.get(framework, _DEFAULT_COMPOSITE_STRATEGY)
return strategy(entity_indicators, all_entity_attrs, framework)
```

`financial` and `human_development` use `_DEFAULT_COMPOSITE_STRATEGY` via the
fallback — not explicitly registered. This is intentional: new frameworks that have
not received ADR treatment fall back to percentile rank rather than failing silently,
preserving the existing behavior for all existing frameworks.

`governance` is not registered in `_COMPOSITE_STRATEGIES` at M8. When GovernanceModule
is promoted at M9, the governance normalization strategy must be registered in
`_COMPOSITE_STRATEGIES` in the **same commit** as the `_UNIMPLEMENTED_FRAMEWORKS`
removal. The ADR-005 M9 amendment must name the strategy. A commit that removes
`"governance"` from `_UNIMPLEMENTED_FRAMEWORKS` without a same-commit strategy
registration and ADR update is non-compliant.

#### Why callable map over the alternatives

**Alternative rejected — if/elif chain:**
Adding governance requires modifying the function body. An if/elif chain obscures the
fallback behavior: a reviewer cannot determine that unregistered frameworks use
percentile rank without tracing all branches. The DISPATCH DESIGN NOTE prohibited this
explicitly. The dict approach makes the fallback visible and extension requires only a
new entry, not a body edit.

**Alternative rejected — class hierarchy or Protocol:**
Over-engineered for two to three strategy variants. A Protocol is appropriate when
strategies carry state or when variant count exceeds four or five. At M8 the variants
are: boundary proximity (ecological) and percentile rank (default). A Protocol would
add indirection without purchase. The callable map is sufficient.

#### Implementation obligations

1. Extract `_percentile_rank_strategy()` and `_boundary_proximity_strategy()` as
   module-level callables before implementing `_COMPOSITE_STRATEGIES`. Both must be
   implemented in the same commit — the DISPATCH DESIGN NOTE requirement stands.

2. Both strategy functions must have intent blocks per CODING_STANDARDS.md §Intent Blocks.

3. `_compute_composite_score()` body is refactored to the dispatch pattern. The function
   signature (`entity_indicators, all_entity_attrs, framework`) is unchanged; existing
   callers require no modification.

4. The comment above `_COMPOSITE_STRATEGIES` must name the M9 governance registration
   obligation verbatim (see code example above), so future implementors cannot miss
   the same-commit requirement.

---

### Decision M8-4: GovernanceModule Promotion — Deferred to M9

#### The problem

`GovernanceModule` is implemented (Decision 6) but `"governance"` remains in
`_UNIMPLEMENTED_FRAMEWORKS`. The M8 question is whether the five promotion criteria in
CODING_STANDARDS.md §Framework Promotion Protocol are met.

#### Assessment — Five criteria, zero met at M8 exit

| Criterion | M8 Status | Blocking gap |
|---|---|---|
| 1. Backtesting threshold | Not met | No governance indicators in any backtesting fixture; Greece 2010–2015 extension (Issue #284) covers financial and human development only |
| 2. ADR amendment accepted | Partially met | This amendment documents composite score dispatch but does not specify governance normalization methodology — governance strategy remains TBD |
| 3. Source field registry draft-certified | Not met | Governance indicators not yet draft-certified in `source_field_registry` |
| 4. `[SIM-INTEGRITY]` WARNING on unexpected null | Not met | Not implemented in GovernanceModule |
| 5. Integration test asserting non-null governance score | Not met | No integration test exists |

#### Decision — `"governance"` remains in `_UNIMPLEMENTED_FRAMEWORKS` at M8 exit; target M9

GovernanceModule promotion is a named M9 Standards Foundation deliverable. The
UX Agent ruling (Issue #218, 2026-05-16) confirmed deferral is methodologically correct:
> *"The labeled null governance axis is an asset for the methodology reviewer audience,
> not a gap. 'No False Precision' delivered in the interface is stronger than in a
> document. GovernanceModule promotion criteria (five conditions per §Framework Promotion
> Protocol) remain the gate — deferring is methodologically correct."*

All five criteria must be simultaneously met before `"governance"` is removed from
`_UNIMPLEMENTED_FRAMEWORKS`. The ADR-005 M9 amendment specifying governance normalization
methodology is a required prerequisite for criterion 2 — removal cannot precede the
accepted amendment.

#### No implementation obligation at M8

No code changes to `_UNIMPLEMENTED_FRAMEWORKS` or governance strategy registration
are required for M8. This decision is recorded to close the question definitively
so implementors do not interpret the criterion assessment independently.

---

### Decision M8-5: Null Governance Axis Rendering — Binding UX Ruling

#### The problem

When all four radar chart axes render simultaneously (information-hierarchy.md M8
Hierarchy Decision: "All four radar axes must appear simultaneously — no tabs, no
toggles"), the governance axis must communicate validation status rather than score
magnitude. Two incorrect implementations are common:

- **Zero-value render:** Renders the governance axis as a filled polygon segment at 0.0,
  implying governance score = 0.0. This misrepresents validation status as governance
  failure — the worst possible diagnostic outcome.
- **Absent axis:** Omits the axis entirely, breaking the four-axis simultaneous display
  requirement.

information-hierarchy.md M8 Hierarchy Decisions (binding table):
> *"Null axes must be visually distinct from zero-value axes — a zero governance score
> and a null governance score are categorically different; conflating them is a
> precision error."*

#### Decision — Dashed outline, "—" score, "Governance — in validation" label

Binding UX ruling (Issue #218, 2026-05-16):

| Element | Specification |
|---|---|
| Axis polygon segment | Dashed outline only; no fill; zero-area polygon segment |
| Score display | `"—"` (em dash); not `"0.00"`, not blank, not `"N/A"` |
| Axis label | `"Governance — in validation"` |
| Hover tooltip | `"Governance composite score is in validation. Promotion criteria: 0 of 5 met at M8. Target: M9."` |

Zero-value rendering is prohibited. Any implementation that renders the governance
axis as a non-null score — including 0.0 — before `"governance"` is removed from
`_UNIMPLEMENTED_FRAMEWORKS` is non-compliant with this decision and with
information-hierarchy.md Zone 1B.

#### Why this specification

The `"—"` score and `"in validation"` label are precision instruments for a specific
epistemic state: the module exists, the measurement framework is defined, the module
is implemented but not yet certified for the API surface. Zero implies measurement
and failure. Blank implies absence. Neither is true. The dashed outline preserves
the four-axis visual structure — the user sees where governance sits in the radar
geometry once promoted, without being misled about current state.

This is the same epistemic discipline applied to `ia1_disclosure` on
`MultiFrameworkOutput` and to the mandatory `FrameworkOutput.note` fields: the tool's
precision claims are visible, not hidden behind an aggregate that obscures them.

#### Implementation obligation

This ruling is binding for `RadarChart.tsx`. It is an ADR-level contract, not a
design preference. Any deviation requires an Engineering Lead decision recorded in
`docs/frontend/design-decisions.md` before implementation proceeds.

---

### Decision M8-6: EcologicalModule M8 Indicator Expansion

#### The problem

Amendment 1 §Amendment B scoped EcologicalModule to two pilot indicators at M6
(`co2_concentration_ppm`, `land_use_pressure_index`) using percentile-rank composite
scoring. The boundary normalization formula adopted in Decision M8-1 requires
indicator-specific boundary constants. This decision specifies which indicators
are added at M8 and their boundary constant associations.

#### Decision — Two boundary proximity indicators added at M8

| Attribute key | `variable_type` | `measurement_framework` | Derived from | Boundary constant |
|---|---|---|---|---|
| `planetary_boundary_co2_proximity` | RATIO | ECOLOGICAL | `co2_concentration_ppm / 350` | `ECOLOGICAL_CO2_PLANETARY_BOUNDARY_PPM` |
| `planetary_boundary_land_use_proximity` | RATIO | ECOLOGICAL | `land_use_pressure_index / 0.25` | `ECOLOGICAL_LAND_USE_PLANETARY_BOUNDARY_RATIO` |

Both are **derived quantities** computed by `EcologicalModule.compute()` from existing
attribute values and registered boundary constants. They are not sourced independently
from external data. Their `source_registry_id` must reference the boundary constant
source (Rockström 2009 or Richardson 2023), not the raw indicator source.

The M6 pilot indicators (`co2_concentration_ppm`, `land_use_pressure_index`) are
**not removed** at M8. They remain in the entity attribute store as the raw values
from which proximity indicators are derived. The FrameworkPanel (Zone 3,
information-hierarchy.md) displays both raw and derived indicators.

#### Confidence tier defaults for M8 ecological indicators

| Indicator | Default `confidence_tier` | Rationale |
|---|---|---|
| `planetary_boundary_co2_proximity` | 1 | Derived from Tier 1 Mauna Loa direct measurement series |
| `planetary_boundary_land_use_proximity` | 3 | Derived from Tier 3 FAO GFR; 5-year data requires annual interpolation |

Confidence tier propagation follows the lower-of-two (`max()`) rule per the standard.
A derived indicator cannot carry higher confidence than its source indicator.

#### Why derived proximity indicators rather than inline computation in `_compute_composite_score()`

Boundary proximity could be computed inside `_compute_composite_score()` as an
intermediate rather than persisted as entity attributes. Derived indicators as
persisted entity attributes are preferred for three reasons:

1. **Snapshot transparency:** `scenario_state_snapshots.entities_snapshot` contains
   the proximity score alongside the raw indicator. A reviewer inspecting the snapshot
   can verify the ratio without re-running the formula.

2. **MDA threshold system compatibility:** Decision 3 fires against entity attribute
   values. Registering `planetary_boundary_co2_proximity > 1.0` as an MDA threshold
   requires the proximity score to be a persisted attribute, not a computed intermediate.

3. **Extensibility pattern:** New planetary boundary domains added at M10+ follow the
   same pattern: raw value persisted → proximity derived → boundary constant registered.
   Establishing this at M8 creates the extensibility contract.

#### Implementation obligations

`EcologicalModule.compute()` at M8 must:

1. Read `co2_concentration_ppm` and `land_use_pressure_index` from the entity's current
   attribute snapshot.
2. Query `simulation_reference_constants` for both boundary constants. If either constant
   is absent, emit a `[SIM-INTEGRITY]` WARNING and omit the corresponding derived
   indicator from the step's event.
3. Compute `min(current / boundary, Decimal("2.0"))` for each, using `Decimal` arithmetic
   throughout (no intermediate float conversion).
4. Return `planetary_boundary_co2_proximity` and `planetary_boundary_land_use_proximity`
   as `Quantity` values in the event's `affected_attributes`.

Alembic migration for MDA threshold seed data for both indicators (`boundary_score > 1.0`
→ `MDASeverity.WARNING`) must be included in the M8 EcologicalModule implementation PR.

---

### Deferred Items

**Governance normalization methodology (M9):**
Amendment 1 Q4 confirmed percentile rank is methodologically valid for governance.
The M9 GovernanceModule promotion amendment will specify the normalization strategy
and register it in `_COMPOSITE_STRATEGIES`. Governance normalization must not be
implemented without an accepted ADR amendment. This item is explicitly deferred and
not open for implementation-time interpretation.

**Remaining planetary boundary domains (M10+):**
Seven of the nine planetary boundary domains are not addressed at M8: biodiversity
loss, freshwater use, biogeochemical flows (nitrogen/phosphorus), ocean acidification,
stratospheric ozone, aerosol loading, and novel entities. Each requires approved data
sources, a registered boundary constant, and confidence tier assessment before it can
contribute to the ecological composite score. M8 active domains: CO2 concentration
and land-system change only.

**Ecological→financial cross-domain propagation (M10):**
EcologicalModule at M8 remains an event consumer. Ecological state changes do not
generate propagation events into financial or governance modules. The Ecological
Economist's blind interview finding (Issue #218 Council comment) identifies this as
the most dangerous invisible interaction in the model — fisheries depletion below MSY
threshold generating export revenue events, which generate fiscal events. This is a
confirmed M10 Engine Integrity scope item. The causal meta-map (ARCH-REVIEW-005
obligation, Issue #218) must document this limitation and its M10 resolution path
before M8 implementation is locked.

---

### Renewal Triggers

**Trigger fired — radar chart normalization methodology changed:**
The trigger documented in the Validity Context §Renewal Triggers fires with this
amendment:
> *"Radar chart normalization methodology changed from percentile-based cross-entity
> ranking to an alternative"*
The ACCEPTED → UNDER-REVIEW transition has occurred. Engineering Lead acceptance of
this amendment returns the ADR to CURRENT.

**New trigger added — `_boundary_proximity_strategy()` formula:**
Any change to the boundary proximity formula, the cap value (2.0), or the
`simulation_reference_constants` lookup behavior requires this Decision M8-1 section
to be updated in the same commit.

**New trigger added — `_SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS`:**
Any addition to or removal from `_SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS` requires
Decision M8-2 to be updated in the same commit. This trigger catches the same
subscription-list drift that produced Amendment 2.

**New trigger added — `_COMPOSITE_STRATEGIES` registration:**
Any addition to `_COMPOSITE_STRATEGIES` (including governance registration at M9
promotion) requires a same-commit update to the relevant Decision section of this ADR.
The governance registration at M9 must update Decision M8-4's criterion 2 status from
"Partially met" to "Met."

---

## Questions for the Review Panel

The following architectural questions could not be resolved from the available documents
and are submitted for review panel input before this draft is committed to ADR-005.

**Q1 — Temporal validity of boundary constants in backtesting scenarios:**
The `simulation_reference_constants` seed data assigns `effective_from = 2009-09-24`
for the CO2 boundary (Rockström et al. 2009) and `effective_from = 2023-09-13` for
the land-use boundary (Richardson et al. 2023). The Greece 2010–2015 backtesting
fixture spans the period 2010–2015 — before the Richardson 2023 update. Should
backtesting scenarios use the boundary constant effective at simulation time (which
would mean the land-use boundary for 2010–2012 is undefined and excluded from the
ecological composite), or should they use the best-currently-available constant
regardless of `effective_from`? The DATA_STANDARDS.md §Backtesting Integrity
"vintage dating required for all backtesting inputs" principle suggests using
the effective-at-simulation-time value, which would exclude land-use proximity from
the Greece 2010–2012 composite score. This needs explicit disposition before
implementation — it determines how `_boundary_proximity_strategy()` handles
multi-temporal boundary queries.

**Q2 — Composite score aggregation when indicator count varies across entities:**
The mean boundary_score across registered indicators assumes every entity has the
same set of ecological indicators. If one entity has CO2 data but not land-use data,
its composite is a mean of one boundary score while another entity with both data
points is a mean of two. Should the composite be the mean of all available boundary
scores per entity (current design), or should it be restricted to the intersection
of indicators present across all entities? The percentile-rank strategy faces the
same question, but it is more visible for boundary-normalized composites where
the ecological score has a known physical interpretation per indicator.

**Q3 — Governance composite score normalization methodology:**
Decision M8-4 defers governance normalization to M9, and Amendment 1 Q4 confirmed
percentile rank is methodologically valid for governance. However, the Q4 confirmation
was written before the M8 boundary normalization decision was fully developed. Now
that ecological has a non-percentile methodology with clear rationale (boundary values
are absolute physical thresholds), should the M9 amendment re-examine whether any
governance indicators have absolute threshold equivalents (e.g., press freedom index
below a documented autocracy threshold)? Or is percentile rank confirmed as the M9
governance normalization approach without further examination? Clarifying this now
prevents the M9 amendment from having to re-litigate a question the panel has already
considered at M8.

**Q4 — `_ECOLOGICAL_MANDATORY_NOTE` replacement and forward compatibility:**
The new mandatory note text in Decision M8-1 is specific to the boundary proximity
formula at M8. When new planetary boundary domains are added at M10+, will the note
need to list all registered domains? Or should the note reference the
`simulation_reference_constants` table dynamically rather than being a static string?
The current design (`_ECOLOGICAL_MANDATORY_NOTE` as a module-level string constant)
does not accommodate dynamic note generation without additional infrastructure. The
review panel should determine whether static note text is acceptable through M10 or
whether the note field should be API-generated from the registered constants.

**Q5 — Dashed outline rendering implementation scope:**
Decision M8-5 specifies the dashed outline rendering for the null governance axis
as an ADR-level contract. The question is whether this specification belongs
primarily in this ADR or primarily in a `docs/frontend/design-decisions.md` entry
cross-referenced from here. If the specification lives only in this ADR, frontend
implementors must read ADR-005 during RadarChart implementation — which is correct
procedure but unusual for component-level work. If it is duplicated in `design-decisions.md`,
there is a risk of the two diverging. Recommended: this ADR holds the contract;
the design-decisions.md entry references this decision by number and adds only
technical implementation detail. The review panel should confirm or redirect.

---

*End of draft. Produced by Architect Agent, 2026-05-17. Panel review required before
acceptance. Do not commit to ADR-005-human-cost-ledger.md without Engineering Lead
disposition of all five panel questions.*
