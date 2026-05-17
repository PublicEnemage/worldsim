# ADR-005 Amendment 3 — Four-Agent Panel Synthesis

> **Status:** Panel review complete — Engineering Lead disposition required.
> **Date:** 2026-05-17
> **Branch:** `docs/adr-005-amendment3-panel`
> **Draft reviewed:** `docs/architecture/adr-005-amendment3-draft.md`
> (branch `origin/docs/adr-005-amendment3-draft`, not committed to ADR-005-human-cost-ledger.md)
>
> **Panel members (independent, no shared context):**
> - Data Architect
> - QA Lead
> - Ecological Economist (Domain Intelligence Council)
> - Chief Methodologist (Domain Intelligence Council)
>
> **Excluded:** Architect Agent (draft author). No prior session context, existing
> dispositions, Architect Agent reasoning, or pre-panel assessment was shared with
> any panel member. Each agent received only the full draft text and three identical
> questions.

---

## Contents

1. [Verbatim Agent Responses](#verbatim-agent-responses)
   - [Data Architect](#data-architect)
   - [QA Lead](#qa-lead)
   - [Ecological Economist](#ecological-economist)
   - [Chief Methodologist](#chief-methodologist)
2. [Cross-Cutting Concerns Table](#cross-cutting-concerns-table)
3. [Disagreements Table](#disagreements-table)
4. [Q1–Q5 Panel Dispositions](#q1q5-panel-dispositions)
5. [Highest-Risk Decision Vote](#highest-risk-decision-vote)
6. [Decisions Flagged for Revision](#decisions-flagged-for-revision)

---

## Verbatim Agent Responses

### Data Architect

#### Question 1: Per-Decision Analysis — Primary Concerns and Missing Specifications

**Decision M8-1: Boundary Proximity Normalization Formula**

My primary concern is the composite score range claim. The draft specifies `FrameworkOutput.composite_score: str | None` in `schemas.py` with an existing docstring stating "0.0–1.0 percentile rank." The boundary proximity formula produces values in `[0.0, 2.0]`, not `[0.0, 1.0]`. The `FrameworkOutput` schema docstring — which is the schema registry's contract boundary — directly contradicts the new formula's output range. This is a schema drift violation: the schema claims one range and the implementation will produce another.

The schema registry (`docs/schema/api_contracts.yml`) does not currently document the measurement-output endpoint's `FrameworkOutput.composite_score` field with a range constraint; however, `schemas.py` itself carries a docstring range claim that will be false after M8 implementation. The draft does not name this as an implementation obligation.

Missing obligation: The implementation PR must update the `FrameworkOutput` docstring in `schemas.py` to reflect that `composite_score` may be in `[0.0, 2.0]` for ecological framework rather than `[0.0, 1.0]` uniformly. The `api_contracts.yml` entry for the measurement-output endpoint must also note the framework-dependent range. These are schema registry updates required by the same-commit rule — neither is mentioned in the draft's implementation obligations.

Second concern: the draft specifies that boundary constants are read from `simulation_reference_constants` at "composite score computation time" and must respect `effective_from` / `effective_through`. But `_compute_composite_score()` in the current implementation (`scenarios.py:837`) receives only the already-parsed in-memory snapshot data — it has no database connection. The boundary constant lookup would require either injecting database access into what is currently a pure function, or pre-loading boundary constants before calling the strategy. Neither approach is specified. The draft says "must be read from the database at composite score computation time" without specifying where in the call chain the query happens. An implementor reading the draft will need to make an unguided architectural decision about whether to pass a pre-loaded constants dict into the strategy function or restructure `get_measurement_output` to fetch constants before calling `_compute_composite_score`. This is ambiguous and will produce either an incorrectly-pure function that hardcodes boundary values, or an ad-hoc query injection that is not reviewable against a contract.

Missing obligation: Specify that `get_measurement_output` (the async handler) is responsible for fetching the currently-active boundary constants from `simulation_reference_constants` before invoking `_compute_composite_score`, and that these constants are passed as a parameter to the boundary proximity strategy function. The query to use is already documented in `database.yml §query_notes` — reference it.

The formula and alternatives analysis are sound. The mandatory note text is adequately specified. The Alembic migration obligation for MDA seed data is correctly placed.

**Decision M8-2: `is_single_entity` Guard — Ecological Framework Exemption**

My primary concern is that the draft specifies replacing the unconditional `is_single_entity` guard with a check against `_SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS: frozenset[str]`, but does not specify what happens to the `note` field when an ecological composite score is successfully computed in a single-entity scenario.

Looking at the current code (`scenarios.py:1031-1036`): the ecological note is set unconditionally to `_ECOLOGICAL_MANDATORY_NOTE` when `fw == "ecological"`. The `is_single_entity` branch sets `_SINGLE_ENTITY_NOTE` only for non-ecological frameworks. This logic already works correctly for ecological, but after the strategy dispatch is in place, a single-entity ecological scenario will compute a real composite score AND set `_ECOLOGICAL_MANDATORY_NOTE` — which is correct. However, the draft does not confirm this note-assignment logic is preserved. Obligation 2 says "`_SINGLE_ENTITY_NOTE` must not appear on ecological `FrameworkOutput`" but says nothing about confirming `_ECOLOGICAL_MANDATORY_NOTE` continues to appear.

Also, the draft table says governance at M8 is "Not applicable — guard interaction specified at M9 promotion." But governance at M8 remains in `_UNIMPLEMENTED_FRAMEWORKS`, so it hits the early-return path and never reaches the guard. The table is technically correct but slightly misleading — governance never reaches the guard code at M8, not because the interaction is deferred but because the unimplemented-frameworks gate fires first. A future M9 implementor removing governance from `_UNIMPLEMENTED_FRAMEWORKS` must remember to also specify the guard interaction. This is an edge case that the renewal trigger on `_SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS` covers, but the mechanism of protection is not made explicit. No missing obligation — but the table note should be more precise.

The decision is otherwise adequately specified.

**Decision M8-3: Strategy Dispatch Pattern**

My primary concern is the callable signature contract. The draft specifies `dict[str, Callable[..., Decimal | None]]` using `...` as the parameter type. The current `_compute_composite_score()` signature is `(entity_indicators, all_entity_attrs, framework)`. After refactoring, strategy functions will be called as `strategy(entity_indicators, all_entity_attrs, framework)`. But the boundary proximity strategy needs boundary constants (see M8-1 gap above) — if constants are passed as a parameter, the callable type is `Callable[[dict, dict, str, dict], Decimal | None]` or requires currying.

The draft specifies the dispatch signature as `strategy(entity_indicators, all_entity_attrs, framework)` — which is the current `_compute_composite_score` signature — but the boundary proximity strategy needs constants that are not in that parameter set. This is a direct consequence of the M8-1 gap: the draft does not specify how boundary constants reach the strategy. Either the callable map must include constants in the signature (requiring the type annotation to change and the dispatch call to change), or `_boundary_proximity_strategy` must re-query the database itself (violating the pure-function pattern), or constants must be captured in a closure.

Missing obligation: Specify whether `_boundary_proximity_strategy` receives boundary constants via a closure (at construction time in `get_measurement_output`) or as an additional parameter (requiring the callable signature to be updated from the three-parameter form in the draft). The `Callable[..., Decimal | None]` type annotation uses `...` precisely to avoid specifying this — which defers the question to the implementor, where it will be answered inconsistently.

The callable-map-over-class-hierarchy rationale is sound. The governance registration point and the same-commit requirement are correctly specified.

**Decision M8-4: GovernanceModule Promotion Deferred to M9**

My primary concern is the criterion 2 status. The draft says "Partially met — this amendment documents composite score dispatch but does not specify governance normalization methodology." The five-criterion table in M8-4 correctly maps to the Framework Promotion Protocol in `CODING_STANDARDS.md`. The deferred status is defensible.

One schema concern: criterion 3 references "Governance indicators not yet draft-certified in `source_field_registry`." The schema registry at `docs/schema/database.yml` does not document a `source_field_registry` table. The registered tables are: `simulation_entities`, `scenarios`, `scenario_scheduled_inputs`, `scenario_state_snapshots`, `scenario_deleted_tombstones`, `mda_thresholds`, `relationships`, `territorial_designations`, `source_registry`, `backtesting_thresholds`, `control_input_audit_log`, `simulation_reference_constants`. There is no `source_field_registry` in the schema. Either this is a table that exists outside the registry (a schema drift violation if so), or this criterion references a concept that maps to a different table name. The M8-4 criterion text should reference the actual table name, or this is a phantom table that needs to be added to `database.yml`.

This is a material schema registry gap if the table exists in the codebase but is not in the registry. I cannot verify from the draft alone whether it exists — the implementor verifying this criterion will encounter either a missing table or a registry omission.

**Decision M8-5: Null Governance Axis Rendering**

My primary concern is that this decision specifies TypeScript rendering behavior (dashed outline, em dash score display) in an ADR whose implementation obligations are entirely in the Python backend. The actual `RadarAxisDatum` TypeScript interface in the existing ADR-005 Decision 4 uses `is_implemented: boolean` and `composite_score: number` — where `number` cannot represent the em dash string `"—"`.

The draft's rendering specification (em dash score display, dashed outline polygon) requires a change to the `RadarAxisDatum` TypeScript interface. Currently `composite_score` is `number` and an unimplemented framework renders as 0 via the `is_implemented` flag. The new specification requires a different visual treatment (not just a flag, but distinct rendering with dashed polygon and string display). The draft does not identify this as requiring a TypeScript type contract change.

Missing obligation: Specify that `RadarAxisDatum.composite_score` in `RadarChart.tsx` must accommodate null/undefined for unimplemented frameworks rather than relying on the `is_implemented` boolean with a 0.0 numeric fallback. The current interface comment in ADR-005 Decision 4 says "unimplemented → 0 with grayed rendering" — this directly conflicts with Decision M8-5's "zero-value rendering is prohibited" requirement. The M8-5 implementation PR must update the Decision 4 TypeScript interface specification in this ADR in the same commit (cross-ADR impact rule from CLAUDE.md Pre-PR Checklist item 4).

The Q5 disposition recommended at end of the draft (ADR holds contract, design-decisions.md references it) is architecturally correct. But the cross-ADR drift between Decision 4's `is_implemented: bool, composite_score: number` pattern and Decision M8-5's prohibition on zero rendering must be explicitly named as a same-commit obligation.

**Decision M8-6: EcologicalModule M8 Indicator Expansion**

My primary concern is the `source_registry_id` specification for derived indicators. The draft states "Their `source_registry_id` must reference the boundary constant source (Rockström 2009 or Richardson 2023), not the raw indicator source." This requires `source_registry` rows for those publications. The draft names two `constant_id` values in `simulation_reference_constants` with `doi_or_url` attributes — but `simulation_reference_constants.doi_or_url` is a string, not an FK into `source_registry`. The `source_registry` table has its own `source_id` PK.

These are two separate tables serving different purposes: `simulation_reference_constants` holds calibration constants; `source_registry` holds data source provenance. A derived `Quantity` in an entity's attribute store carries `source_registry_id` as FK into `source_registry` — not into `simulation_reference_constants`. The Rockström 2009 and Richardson 2023 papers must be registered as rows in `source_registry` (with their own `source_id` strings) before the derived proximity indicators can reference them via `source_registry_id`. The draft mentions Alembic migrations for `simulation_reference_constants` seed data (`a2b4c6d8e0f1` + `b3c5d7e9f1a2`) but does not explicitly call out that a separate Alembic migration registering these publications in `source_registry` is also required.

Missing obligation: Add as an explicit implementation obligation that the M8 EcologicalModule implementation PR must include Alembic migrations registering Rockström et al. 2009 (Nature 461:472–475) and Richardson et al. 2023 (Science Advances 9(37)) as rows in `source_registry`, with stable `source_id` values that `planetary_boundary_co2_proximity` and `planetary_boundary_land_use_proximity` Quantities can reference as `source_registry_id`.

The "derived indicators as persisted attributes" rationale is sound and serves MDA threshold compatibility well. The three-reason justification is the strongest part of this decision.

The confidence tier defaults and the lower-of-two `max()` rule application are correctly specified.

#### Question 2: Open Questions Q1–Q5 — Recommended Dispositions

**Q1 — Temporal validity of boundary constants in backtesting scenarios:**

Recommended disposition: Use the constant effective at simulation time. Use the query documented in `database.yml §query_notes §Historical run resolution`:

```sql
SELECT value FROM simulation_reference_constants
WHERE constant_id = $1
  AND effective_from <= $run_date
  AND (effective_through IS NULL OR effective_through >= $run_date)
```

The `DATA_STANDARDS.md §Backtesting Integrity` principle ("vintage dating required for all backtesting inputs") is not merely procedural — it is the epistemic foundation for distinguishing what was knowable at simulation time from what we now know. Allowing the use of a 2023 Richardson constant to evaluate a 2010–2012 scenario violates this principle: the Richardson 2023 land-use boundary was not yet published, so no 2010 decision-maker could have used it. The consequence is concrete: when the Greece 2010–2015 backtesting fixture runs steps covering 2010–2012, the land-use proximity indicator is absent from the ecological composite score for those steps. That absence is the correct output. It is not a gap to be papered over with retrospective knowledge.

Implementation obligation that follows: `_boundary_proximity_strategy()` must accept the backtesting run date as a parameter (or derive it from the simulation timestep) to execute the historical-resolution query. This means the async handler in `get_measurement_output` must pass the snapshot timestep into the boundary constant lookup, not just fetch the currently-active constant. The draft's current specification ("respect `effective_from` and `effective_through`") is correct but underspecified — it does not say which date to use as the resolution point. The answer is: the simulation timestep of the snapshot being queried.

**Q2 — Composite score aggregation when indicator count varies across entities:**

Recommended disposition: Mean of all available boundary scores per entity (the current design intent). Reject the intersection approach.

The intersection approach produces a composite score that reflects the worst-represented entity in the simulation rather than the actual entity being assessed. If one entity has CO2 data but not land-use data, restricting all entities to CO2 only degrades the information available for entities that have both. The resulting composite is less informative than the per-entity mean.

The correct approach is per-entity mean of available scores with a note field disclosing how many indicators contributed. The `FrameworkOutput.note` already exists for this purpose. An entity with one contributing indicator gets a composite of one boundary score; an entity with two gets a mean of two. The disclosure mechanism ("X of N registered boundary domains contributing") makes the difference visible without hiding information.

One addition needed in the mandatory note text: the note should state "composite is mean across N registered indicators" where N is entity-specific, so reviewers can see indicator count without digging into indicator lists. This is a small addition to the note template rather than a new field.

**Q3 — Governance composite score normalization methodology:**

Recommended disposition: Do not confirm percentile rank as the M9 approach without re-examination. Specifically: require the M9 amendment to assess whether any governance indicators have absolute threshold equivalents before defaulting to percentile rank.

The Q4 confirmation in Amendment 1 was correct for cross-entity relative comparison (where a country sits in the global governance distribution). But the development of the boundary proximity formula for ecological indicators reveals that some indicators have physically grounded absolute thresholds — the 350 ppm CO2 boundary is a fact about planetary physics, not a policy preference. Some governance indicators may have analogous threshold properties.

The Freedom House methodology publishes explicit thresholds for "Not Free" (0–35), "Partly Free" (36–71), and "Free" (72–100) categorical classifications. These are not arbitrary percentile cutoffs — they are published methodological thresholds. V-Dem similarly publishes threshold criteria for regime type transitions. If these thresholds have the same epistemic character as planetary boundaries (externally defined, not derived from the simulation's entity distribution), using percentile rank for them has the same category-error problem that Amendment 1 identified for ecological indicators.

The M9 amendment must examine this question explicitly. Confirming percentile rank now without that examination reproduces the M6 ecological decision — a defensible scope decision, but not a methodological conclusion.

**Q4 — `_ECOLOGICAL_MANDATORY_NOTE` and forward compatibility:**

Recommended disposition: The note should reference the `simulation_reference_constants` table dynamically rather than remaining a static string, but this infrastructure is not required at M8. The static note is acceptable through M10 with one constraint: the note text must reference the source table by name (which the proposed text already does: "Source: simulation_reference_constants table"), not enumerate specific indicators.

The proposed mandatory note text already satisfies the M10+ forward compatibility requirement because it describes the formula and references the table generically — it does not enumerate "CO2 and land-use" specifically. When additional planetary boundary domains are added at M10+, the note text does not need to change. Reviewers inspect the `simulation_reference_constants` table for the full indicator list.

Dynamic API-generated note text is the right long-term pattern but requires infrastructure that is disproportionate to the M8 scope. Accept the static string through M10. At M10, when the third and fourth boundary domains are added, reassess whether the static note is still serving its purpose.

One requirement: add a renewal trigger in the ADR for "static mandatory note text reviewed when planetary boundary domain count exceeds four." This gates the reassessment without requiring it now.

**Q5 — Dashed outline rendering specification location:**

Recommended disposition: This ADR holds the binding contract; `design-decisions.md` holds a cross-reference entry with implementation-specific detail only. The panel's recommended approach is correct.

The argument for this disposition: the rendering specification is not a styling preference — it encodes an epistemic commitment ("a null governance score and a zero governance score are categorically different"). That epistemic commitment is the ADR's domain. `design-decisions.md` is appropriate for "how Recharts renders a dashed polygon" (implementation technique), not for "why a dashed polygon rather than a zero-area filled segment" (epistemic rationale). Separating these into two documents with clear ownership prevents the implementation from drifting away from the rationale.

However, one obligation must be explicit: the `design-decisions.md` entry must include a machine-verifiable cross-reference to this ADR decision number (e.g., "See ADR-005 Decision M8-5"), not just a prose description. This ensures that when future frontend implementors search `design-decisions.md` for radar chart rendering guidance, they find the binding constraint rather than only implementation details. The draft should add this as a named implementation obligation.

#### Question 3: Highest Implementation Risk

**Decision M8-1** poses the highest implementation risk. The specific sentence that would reduce that risk most:

> "The boundary constant lookup query must be executed in `get_measurement_output` (the async database handler), using the snapshot's simulation timestep as `$run_date` per the historical-resolution query in `database.yml §query_notes`, and the resolved constants dict must be passed as an explicit parameter to `_boundary_proximity_strategy()` — the strategy function itself must not contain database access."

The current draft leaves the database-access question entirely unspecified. An implementor who reads only the draft will know what formula to compute but will have no guidance on where in the call chain the database query happens. The three most likely implementation errors are: (1) hardcoding boundary constants as module-level literals (defeating the `effective_from`/`effective_through` logic entirely), (2) introducing database access inside `_boundary_proximity_strategy()` itself (making the pure-function strategy pattern unpure and untestable), or (3) always fetching the currently-active constant regardless of simulation timestep (producing correct results for forward scenarios but wrong results for backtesting, which is precisely the scenario that the Greece 2010–2015 fixture exercises). All three errors are silent — none will raise an exception. Without the call-chain specification in the ADR, the implementor will make an unguided choice, the reviewer will have no contract to check against, and the backtesting fixture will silently return a wrong composite score.

---

**Summary of material gaps (Data Architect):**

1. `FrameworkOutput.composite_score` schema docstring range claim (`[0.0, 1.0]`) conflicts with the boundary proximity formula's `[0.0, 2.0]` output range — `schemas.py` and `api_contracts.yml` must be updated in the same commit as the implementation.
2. The call chain for boundary constant retrieval is unspecified — the async handler must fetch constants using the snapshot timestep, then pass them to the strategy; this must be named as an explicit implementation obligation.
3. `_boundary_proximity_strategy()` callable signature is underspecified — the `Callable[..., Decimal | None]` type annotation defers the parameter-passing question for boundary constants to the implementor.
4. `source_field_registry` referenced in M8-4 criterion 3 does not appear in `database.yml` — either the table name is wrong, or the table is missing from the schema registry.
5. `source_registry` registration for Rockström 2009 and Richardson 2023 is not named as an explicit implementation obligation in M8-6, despite being required by the `source_registry_id` contract for derived Quantity attributes.
6. Decision 4's TypeScript interface (`is_implemented: bool, composite_score: number`) directly conflicts with Decision M8-5's "zero-value rendering is prohibited" rule — the M8-5 implementation PR must update the Decision 4 interface specification in the same commit under the cross-ADR impact rule.

---

### QA Lead

#### Question 1: Per-Decision Analysis — Primary Concerns and Missing Specifications

**Decision M8-1: Boundary Proximity Normalization Formula**

Primary concern: The implementation obligations are well-specified at the formula level, but the `_compute_composite_score()` function as it exists in `scenarios.py` (lines 837–899) has a critical subtlety the draft does not resolve: the function uses the `all_entity_attrs` argument to iterate over all entities' values for percentile-rank computation. The `_boundary_proximity_strategy` will not use `all_entity_attrs` the same way — it queries the database for constants, not the entity state snapshot. The draft's implementation obligation states "Read from the database (`simulation_reference_constants` table) at composite score computation time," but `_compute_composite_score()` currently receives no database connection. The function signature `(entity_indicators, all_entity_attrs, framework)` is stated as unchanged.

This is a gap: `_boundary_proximity_strategy()` needs to call the database, but `_compute_composite_score()` has no `conn` argument and no async context. Either the strategy must receive the boundary constants as a pre-fetched argument (requiring a caller-side query before dispatch), or the function signature must change to accommodate a connection. The draft says "existing callers require no modification," which forecloses the signature-change path but does not specify how the DB lookup reaches the strategy.

Missing obligation: "The boundary constants must be fetched by the caller (`get_measurement_output`) and passed to `_compute_composite_score()` as a new `reference_constants: dict[str, Decimal]` parameter — OR `_boundary_proximity_strategy()` is a synchronous function that receives pre-fetched constants as a positional argument. One of these two options must be named explicitly. The current spec is ambiguous and will produce implementation variance."

**Consequence of the gap:** Implementors will either introduce a float conversion when fetching via asyncpg (NUMERIC → Python `Decimal` requires explicit cast, otherwise asyncpg returns a Python `float`), or they will hardcode the constants to avoid the async problem. Both are violations — the first violates the float prohibition, the second defeats the traceability rationale.

**Additional missing obligation:** Decision M8-1 requires the `simulation_reference_constants` query to "respect `effective_from` and `effective_through`." The existing Alembic migration (`b3c5d7e9f1a2`) seeds the land-use boundary with `effective_from = 2023-09-13`. For the Greece 2010–2015 backtesting fixture, this means the land-use boundary is unavailable at simulation time. The draft identifies this as open question Q1, but does not specify the fallback behavior for `_boundary_proximity_strategy()` when no constant is active at the simulation timestep. The `[SIM-INTEGRITY]` WARNING is specified for constants absent from the table entirely, but not for constants present in the table but outside the `effective_from`/`effective_through` window. This distinction matters: the query behavior, the warning text, and the backtesting fixture behavior are all different depending on whether the constant is "missing" or "temporally unavailable."

**Decision M8-2: `is_single_entity` Guard Exemption**

Primary concern: The decision is correct and adequately motivated. The implementation obligation specifying `_SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS: frozenset[str]` as a module-level constant is the right mechanism, and the renewal trigger is correctly added.

However: there is a test coverage gap not addressed in the implementation obligations. The existing test suite in `test_measurement_output.py` has a test `test_single_entity_composite_score_is_null()` at line 343 that asserts `result.outputs["financial"].composite_score is None` and `result.outputs["human_development"].composite_score is None`. There is no assertion that covers ecological composite score in a single-entity scenario — the test implicitly expects the existing behavior (None) for ecological. After this amendment, ecological should return a non-null score in single-entity scenarios.

Missing obligation: "The existing test `test_single_entity_composite_score_is_null()` must be updated in the same commit: it must assert that `result.outputs['ecological'].composite_score is not None` in a single-entity scenario that has ecological indicator data with a registered boundary constant. A separate test `test_single_entity_ecological_score_is_non_null()` must be added asserting the boundary-normalized score is returned."

Without this, the existing test will pass whether or not the exemption is correctly implemented — because the test fixture `_SINGLE_ENTITY_STATE` in `test_measurement_output.py` has no ecological attributes. The test would not catch a regression where the guard is applied to ecological anyway.

**Decision M8-3: Strategy Dispatch Pattern**

Primary concern: The callable map design is correct for the scale of this problem. The draft's code example for `_COMPOSITE_STRATEGIES` is clear. The concern is the Callable signature constraint.

The draft specifies the dispatch as:
```python
strategy = _COMPOSITE_STRATEGIES.get(framework, _DEFAULT_COMPOSITE_STRATEGY)
return strategy(entity_indicators, all_entity_attrs, framework)
```

This means `_boundary_proximity_strategy` must accept `(entity_indicators, all_entity_attrs, framework)` — the same signature as `_percentile_rank_strategy`. But `_boundary_proximity_strategy` does not use `all_entity_attrs` for anything (it computes boundary ratio from individual entity values, not cross-entity comparison). More importantly: as established in the Decision M8-1 gap above, `_boundary_proximity_strategy` needs boundary constant data that comes from the database, not from the current function arguments.

If the architectural decision is that constants are pre-fetched and injected by the caller, the strategy signature will need a fourth argument (or the constants will be passed through `all_entity_attrs` as a side-channel, which would be architecturally wrong). The draft does not reconcile these.

The `Callable[..., Decimal | None]` type annotation uses `...` (ellipsis) for the parameter types, which is deliberately loose. This is a pragmatic choice to avoid a Protocol at this scale, but it means the type system provides no enforcement that strategies are called with the right arguments.

Missing obligation: "The Callable type annotation must be narrowed to a named TypeAlias or TypeVar-bound callable once the DB lookup pathway is resolved. `Callable[..., Decimal | None]` is an acceptable interim annotation only if the callable map entries and the dispatch call site are in the same file and can be read together as a unit."

The comment naming the M9 governance registration obligation is the most important single element of this decision and is correctly specified.

**Decision M8-4: GovernanceModule Promotion Deferred to M9**

Primary concern: The five-criterion assessment table is accurate and well-justified. No implementation obligations are required, and the decision correctly forecloses implementation-time interpretation.

One gap: the draft states "This decision is recorded to close the question definitively so implementors do not interpret the criterion assessment independently." But the criterion 2 entry reads "Partially met — This amendment documents composite score dispatch but does not specify governance normalization methodology." The "Partially met" status creates an ambiguity: does an implementor reading only this amendment understand that criterion 2 is partially satisfied by this amendment's existence? Or do they need to wait for the M9 amendment?

The draft should state explicitly: "Criterion 2 is not met at M8. The partial satisfaction means only that the dispatch infrastructure is ready; it does not count as criterion 2 satisfaction. Criterion 2 is met only when a named governance normalization strategy is specified in an accepted ADR amendment and registered in `_COMPOSITE_STRATEGIES`."

This distinction matters for the CI enforcement test `test_governance_is_in_unimplemented_frameworks()` — an overeager implementor could read "Partially met" as authorization to begin governance promotion work at M8.

No other gaps in this decision.

**Decision M8-5: Null Governance Axis Rendering**

Primary concern: The rendering specification is correct and the prohibition on zero-value rendering is exactly right. The `RadarChart.tsx` current behavior at line 117–118 renders unimplemented axes at `final_score: 0` (not dashed, not labeled "in validation"). The draft correctly identifies this as prohibited.

However, the implementation obligations are incomplete for the frontend test surface.

Missing obligation 1: "A Playwright E2E test must assert that the governance axis label reads 'Governance — in validation' and that the score display is '—' (em dash). This test must exist and pass before M8 is closed. It belongs in a new spec file `tests/e2e/radar-governance-null-axis.spec.ts` or in an extension of `scenario-advance.spec.ts`."

Missing obligation 2: The specification does not address what `RadarAxisDatum.composite_score` carries for the null governance axis after this amendment. The current `EntityDetailDrawer.tsx` at line 81–82 maps `null` composite_score to `0` for the RadarAxisDatum. Decision M8-5 prohibits rendering at 0. But the current `RadarAxisDatum` type definition shows `composite_score: number` — not `number | null`. To implement the dashed outline correctly, the component needs to distinguish between "score is 0.0 because the entity has terrible governance" and "score is null because governance is in validation."

Options: change `composite_score: number` to `composite_score: number | null` in `RadarAxisDatum`, or add a dedicated `is_null_axis: boolean` field. Either requires a type change. The draft does not name this type change as a required implementation step.

Missing obligation 3: The hover tooltip text `"Governance composite score is in validation. Promotion criteria: 0 of 5 met at M8. Target: M9."` hardcodes a criterion count that will be wrong once M9 begins satisfying criteria. The draft does not address whether this text is static or dynamically sourced. A static string that says "0 of 5 met" is a false precision problem after M9 promotion work begins.

**Decision M8-6: EcologicalModule M8 Indicator Expansion**

Primary concern: The derivation chain from raw indicators to proximity scores is architecturally sound. Persisting derived proximity indicators as entity attributes (rather than computing inline) is the right call for MDA threshold system compatibility.

Missing obligation 1: The draft specifies that `EcologicalModule.compute()` must read `co2_concentration_ppm` and `land_use_pressure_index` from the entity's current attribute snapshot. But the current `EcologicalModule.compute()` signature is `(self, entity: SimulationEntity, state: SimulationState, timestep: datetime) -> list[Event]`. The `entity.attributes` dict stores `Quantity` objects in the Python layer but the snapshot representation in `state` is different — the module reads from `state.events` (prior-step events), not from `entity.attributes` directly. The draft must specify whether proximity indicators are derived from the entity's current attribute values (stored attributes) or from the magnitude of the prior-step ecological events. These are not the same thing: attributes accumulate across steps; events carry deltas for a single step.

The existing module design reads event magnitudes and computes deltas. For boundary proximity, you need the absolute current value (`co2_concentration_ppm` as a STOCK value at the current step), not just the delta. This requires reading from `entity.attributes` rather than `state.events`.

Missing obligation 1 (precise): "The M8 expansion requires `EcologicalModule.compute()` to read the current value of `co2_concentration_ppm` and `land_use_pressure_index` from `entity.attributes`, not from event magnitudes. This is architecturally different from the existing delta-computation pattern. The existing `_extract_magnitude()` helper is not applicable here. A new private function `_read_current_indicator(entity, key)` must be implemented and tested separately."

Missing obligation 2: The draft specifies the `source_registry_id` for derived proximity indicators must reference the boundary constant source, not the raw indicator source. This is correct. But the draft does not specify what `source_registry_id` values are used in the entity attribute for the raw indicators (`co2_concentration_ppm`, `land_use_pressure_index`). If those raw indicators are written with a `source_registry_id` that is not registered in `source_registry`, the proximity calculation will have a provenance gap. The M8 EcologicalModule PR must confirm that all `source_registry_id` values for raw indicators are pre-registered.

Missing obligation 3: The Alembic migration for MDA threshold seed data is required in the implementation PR, per the draft's final paragraph. But the draft does not specify what `entity_scope` pattern to use for the `mda_thresholds` seed entries. The existing seed entries in ADR-005 Decision 3 use specific glob patterns (e.g., `*:CHT:1-*-*` for cohort-specific thresholds) or `all`. For planetary boundary thresholds, the correct `entity_scope` is `all` (any country exceeding 350 ppm is in an unsafe space). This should be stated explicitly — implementors have invented wrong `entity_scope` patterns before.

#### Question 2: Open Questions Q1–Q5 — Recommended Dispositions

**Q1:** Use the effective-at-simulation-time value. Reject the "best-currently-available" approach. DATA_STANDARDS.md §Backtesting Integrity is not a convention — the fixture loader enforces it as a data integrity gate. For Greece 2010–2015, `planetary_boundary_land_use_proximity` is excluded from the ecological composite for all steps. That exclusion must trigger a `[SIM-INTEGRITY]` WARNING and the ecological `FrameworkOutput.note` must disclose it. This is a known, honest limitation — it needs to be disclosed, not solved.

The Q1 answer must be encoded in the implementation obligations for Decision M8-1 as: "When `effective_from` of a constant is later than the simulation's current timestep, the constant is treated as temporally unavailable. A `[SIM-INTEGRITY]` WARNING is emitted with the constant_id and the timestep. The indicator is excluded from the composite score. This is distinct from the case where the constant is absent from the table entirely."

**Q2:** Mean of all available boundary scores per entity (the current design intent). Reject the intersection approach. The intersection approach produces a composite score that reflects the worst-represented entity in the simulation rather than the actual entity being assessed. The correct approach is per-entity mean of available scores with a note field disclosing how many indicators contributed. Consistent with how the percentile-rank composite works for financial and human development.

**Q3:** Mandate a bounded re-examination at M9 amendment time, not a blanket confirmation now. Amendment 1 Q4's confirmation of percentile rank was written before the M8 boundary normalization decision was fully developed. The question of whether governance indicators have absolute threshold equivalents is legitimate and material. The panel cannot answer definitively without domain expertise. The Q4 confirmation should not be silently carried forward. Recommended ADR text: "Amendment 1 Q4's confirmation of percentile rank remains operative as a default at M9. The M9 amendment author must review whether any governance indicator has an equivalent to a planetary boundary — an absolute threshold below which the system enters a documented failure regime."

**Q4:** Keep static string constant through M10. Add one renewal trigger: "If `_ECOLOGICAL_MANDATORY_NOTE` is updated to enumerate specific indicator domains, it must be converted to API-generated text sourced from `simulation_reference_constants` in the same commit. Enumerating domains in a static string is non-compliant from that point forward."

**Q5:** ADR holds the contract; `design-decisions.md` entry created in the same commit as the ADR amendment, with cross-references in both directions. The additional reason to keep the contract in the ADR: the Playwright E2E test that enforces governance axis label text must reference some authoritative source. If the text lives only in `design-decisions.md`, the test must import from a frontend constant that may or may not reflect the ADR. Recommendation: "The `_GOVERNANCE_IN_VALIDATION_LABEL` and `_GOVERNANCE_IN_VALIDATION_TOOLTIP` constants in `RadarChart.tsx` must match the specification in this decision verbatim. A test in `tests/unit/` (not E2E) must assert these constants against their expected values, so that text drift is caught before a full E2E run."

#### Question 3: Highest Implementation Risk

**Decision M8-6 (EcologicalModule M8 Indicator Expansion) poses the highest implementation risk.**

The risk: the existing `EcologicalModule.compute()` reads prior-step event magnitudes (deltas) to produce ecological indicator deltas. Decision M8-6 requires computing boundary proximity from the entity's current absolute attribute value. An implementor reading Decision M8-6 in isolation — without reading the existing module code — will likely implement proximity derivation as a delta computation over the event magnitude, which is architecturally wrong. The result would be proximity scores that drift by the delta each timestep rather than reflecting the actual current concentration ratio. This bug produces a plausible-looking output (a Decimal between 0 and 2 that changes each step) that would only be caught by a test that seeds a known starting `co2_concentration_ppm` and verifies the exact boundary ratio, not just the direction.

One sentence of additional specification:

> "The proximity indicators `planetary_boundary_co2_proximity` and `planetary_boundary_land_use_proximity` are computed from the entity's accumulated current attribute value (read from `entity.attributes[key].value`), not from the step's event delta magnitude — the distinction is critical: using an event delta produces a monotonically-drifting proximity score rather than a ratio of current state to boundary, which would be computationally indistinguishable from correct behavior until an absolute-value fixture test is run."

---

**Summary of test gaps (QA Lead):**

1. Decision M8-2: New test asserting `ecological.composite_score is not None` in a single-entity scenario with ecological attribute data and registered boundary constants. Existing `test_single_entity_composite_score_is_null()` must be updated to explicitly assert ecological is excluded from the guard.
2. Decision M8-5: Playwright E2E test asserting governance axis label text and score display text. A unit test for `_GOVERNANCE_IN_VALIDATION_LABEL` constant matching the ADR specification.
3. Decision M8-6: New unit test in `test_ecological_module.py` seeding a known `co2_concentration_ppm` value on `entity.attributes`, running `EcologicalModule.compute()`, and asserting the exact boundary ratio.
4. Decision M8-1: New unit test for `_boundary_proximity_strategy()` asserting: CO2 at 421 ppm → `Decimal("1.2029")`, cap at 700 ppm → `Decimal("2.0")`, at exactly 350 ppm → `Decimal("1.0")`.

---

### Ecological Economist

#### Question 1: Per-Decision Assessment

**Decision M8-1: Boundary Proximity Normalization Formula**

Primary concern: The `land_use_pressure_index` variable is declared as a ratio whose unit is `ratio_0_1` and whose module docstring describes it as "the fraction of the safe land-system boundary consumed." If `land_use_pressure_index = 0.30` means "30% of the boundary consumed," then dividing by the registered constant `ECOLOGICAL_LAND_USE_PLANETARY_BOUNDARY_RATIO = 0.25` yields `0.30 / 0.25 = 1.2`, which correctly means the boundary has been exceeded by 20%. However, if `land_use_pressure_index` already encodes fraction-of-boundary semantics (i.e., 1.0 = boundary met), then the division by 0.25 double-normalizes and produces a score of 4.0 when the indicator reads 1.0, which is nonsensical.

This is a dimensional consistency problem. The module at `backend/app/simulation/modules/ecological/module.py:68` declares `land_use_pressure_index` with unit `ratio_0_1` and describes it as "fraction of planetary boundary threshold consumed (0–1)." If the existing indicator already expresses fraction-of-boundary with 1.0 = boundary met, then the boundary constant `0.25` cannot be its denominator without producing a nonsensical ratio. The amendment specifies `land_use_pressure_index / 0.25` but does not resolve whether the indicator is dimensioned as (a) fractional land area under cropland vs. total arable land (where 0.25 = the safe threshold in that dimensioning) or (b) fraction of the boundary itself already consumed (where 1.0 = boundary met).

The Richardson et al. 2023 land-system change boundary is quantified as 25% of global ice-free land area under cropland as the safe threshold. The correct physical interpretation is that `land_use_pressure_index` must measure land under cropland as a fraction of total ice-free land area — a physically observable quantity in the range 0–1 where 0.25 is the threshold. This is coherent with `land_use_pressure_index / 0.25` yielding meaningful proximity scores. But the existing module describes the indicator as "fraction of safe land-system boundary consumed," which would range from 0 to values above 1 once the boundary is exceeded. If that description is accurate, `land_use_pressure_index` = 1.3 already means 30% boundary exceedance, and dividing by 0.25 yields 5.2, which is wrong.

**Verdict on adequacy:** The decision does not adequately resolve this dimensional ambiguity. The amendment must explicitly specify the physical dimensioning of `land_use_pressure_index` as the denominator in the proximity computation — specifically: (a) what physical quantity does the raw indicator measure, (b) what is its expected range in current data, and (c) does division by 0.25 yield a quantity with units of "fraction-of-safe-boundary" as intended.

**Missing implementation obligation:** Add an explicit dimensional consistency check to `EcologicalModule.compute()` for M8: assert that `land_use_pressure_index` values in the initial state fall in the range expected given its physical dimensioning, and emit a `[SIM-INTEGRITY]` WARNING if the raw value is already above 1.0 before the proximity calculation (which would indicate it was already expressing boundary exceedance, making the 0.25 division a double-normalization error).

**Secondary concern on CO2 boundary:** The amendment should note that the Rockström 2009 CO2 boundary has been substantially updated in subsequent literature. The mandatory note as written is technically adequate but should confirm the note includes the publication-date provenance of the 350 ppm figure.

The cap at 2.0 is editorially reasonable but ecologically arbitrary. The formula itself is scientifically defensible and idiomatic with the Rockström et al. convention.

**Decision M8-2: `is_single_entity` Guard — Ecological Framework Exemption**

The decision is correct as stated. Boundary proximity normalization is physically meaningful for a single entity. The concern is not with the decision but with an unstated implication: after this amendment, when `is_single_entity` is True and `framework == "ecological"`, the composite score must be computed and returned non-null. The existing code structure makes this refactor straightforward, but the amendment should be explicit that the ecological branch must return a non-null `composite_score` even when `all_entity_attrs` has length 1.

**Missing implementation obligation:** The amendment specifies that `_SINGLE_ENTITY_NOTE` must not appear on ecological `FrameworkOutput`. It does not specify what the `note` field should contain for a single-entity ecological `FrameworkOutput`. After Amendment 3, the mandatory note text changes (Decision M8-1 supersedes the Amendment 1 note). The amendment specifies the new mandatory note text but does not confirm that single-entity ecological outputs receive the mandatory note rather than `_SINGLE_ENTITY_NOTE`. This is implicit from the logic but should be stated explicitly.

**Decision M8-3: `_compute_composite_score()` — Strategy Dispatch Pattern**

The decision is architecturally sound. The callable map with named fallback is the correct design for two to three variants. My concern is with a specification gap in the `_boundary_proximity_strategy()` function contract.

The decision does not specify the function signatures of the two strategies. Looking at the current `_compute_composite_score()` signature, the decision states "The function signature (`entity_indicators, all_entity_attrs, framework`) is unchanged; existing callers require no modification." But `_boundary_proximity_strategy()` requires database access to retrieve boundary constants from `simulation_reference_constants` — it cannot accept only `(entity_indicators, all_entity_attrs, framework)` and also perform a database lookup.

**Missing implementation obligation:** The amendment must specify how boundary constants reach `_boundary_proximity_strategy()` within the strategy dispatch pattern. Given the existing async codebase, the correct approach is almost certainly to pre-fetch boundary constants in `get_measurement_output()` before calling `_compute_composite_score()` and pass them as a parameter — but this changes the signature of `_compute_composite_score()` or requires a context object. The decision says "The function signature is unchanged; existing callers require no modification." That claim is inconsistent with passing database-fetched constants into the boundary strategy unless the constants are passed through `all_entity_attrs` or a context parameter that does not exist today.

**Decision M8-4: GovernanceModule Promotion — Deferred to M9**

The decision is correct and the reasoning is sound. GovernanceModule deferral to M9 is ecologically neutral. The deferral is well-specified and unambiguous. No missing obligations specific to the ecological framework.

**Decision M8-5: Null Governance Axis Rendering — Binding UX Ruling**

Outside my primary domain but within my analytical scope (honest representation of epistemic states). The dashed outline / em dash / "in validation" specification is the correct treatment for the epistemic state "module implemented, not certified." The hover tooltip reads "Promotion criteria: 0 of 5 met at M8." This is accurate and appropriately precise. I support it. The zero-value rendering prohibition is correct — conflating "not certified" with "worst possible score" is a precision error that could mislead a user into treating a certification gap as a governance failure finding. No missing obligations specific to my domain.

**Decision M8-6: EcologicalModule M8 Indicator Expansion**

This is the decision with the highest ecological domain risk.

**Concern 1 — Double-normalization risk:** The amendment specifies `planetary_boundary_land_use_proximity` is derived as `land_use_pressure_index / 0.25`. As noted in M8-1, `land_use_pressure_index` is currently described in the module as "fraction of the safe land-system boundary consumed (0–1)." If this description is physically accurate and the indicator ranges 0–1, then an entity with `land_use_pressure_index = 0.25` is already at the boundary. Dividing by 0.25 gives a proximity score of 1.0 — which is internally consistent only if "fraction consumed" means "fraction of the safe threshold value." But the module docstring says "fraction of the safe land-system boundary consumed (0–1)", which implies the indicator reaches 1.0 when the boundary is fully consumed, not at the actual physical threshold of 0.25. This ambiguity must be resolved definitively before implementation.

**Concern 2 — Source citation precision:** The amendment cites Richardson et al. 2023 as the source for `ECOLOGICAL_LAND_USE_PLANETARY_BOUNDARY_RATIO = 0.25`. Citing Richardson et al. 2023 for a value of 0.25 requires the amendment to specify precisely which Table, Figure, or supplementary dataset in Richardson et al. 2023 supports 0.25 as the land-system boundary value. The migration file cites the paper without specifying a table, figure, or supplementary dataset. The constant value 0.25 is not directly verifiable from this citation alone.

**Concern 3 — One-step lag interaction:** The existing `EcologicalModule` uses a one-step lag design (reads `state.events` from the prior step). The proximity indicators are derived from current attribute values, not from prior-step events. The amendment does not reconcile this temporal inconsistency: the raw indicators are event-driven (one-step lag), but the derived proximity indicators are supposedly computed from "current" attribute values. The wording "reads from the entity's current attribute snapshot" must be clarified to mean "reads the cumulative entity attribute state as of step N" (which already embeds the one-step-lag event effects).

**Missing implementation obligations for Decision M8-6:**

- Add an explicit dimensional consistency check to `EcologicalModule.compute()`: emit a `[SIM-INTEGRITY]` WARNING if `land_use_pressure_index` is above 1.0 before the proximity calculation.
- Require a precise internal reference (Table, Figure, supplementary dataset number) for the Richardson et al. 2023 citation for 0.25.
- Clarify "reads from the entity's current attribute snapshot" to mean cumulative state at step N, not before step-N events are applied.

#### Question 2: Open Questions Q1–Q5

**Q1:** Use the effective-at-simulation-time value, consistent with `DATA_STANDARDS.md §Backtesting Integrity`. The `_boundary_proximity_strategy()` should query `simulation_reference_constants WHERE effective_from <= simulation_date AND (effective_through IS NULL OR effective_through > simulation_date)` for each timestep date, not a simple `WHERE effective_through IS NULL`. For the Greece 2010–2015 fixture, this means `planetary_boundary_land_use_proximity` is absent from the ecological composite for all steps. That absence is correct and honest output. The mandatory note should be updated to reflect that the composite is constructed from available-at-simulation-time boundary constants.

**Q2:** Use the mean of available boundary scores per entity (the current design), not intersection-restricted scoring. Document this as a known methodological choice in the mandatory note. Intersection restriction does not solve comparability problems; it trades one comparability problem (different indicator counts) for another (forcing all entities to the lowest common denominator). The per-entity mean is correct, with a disclosure requirement: when an entity's ecological composite is derived from a different set of indicators, the `FrameworkOutput.note` must state how many boundary scores contributed.

**Q3:** Do not confirm percentile rank as the M9 approach without re-examination. The Q4 confirmation in Amendment 1 was correct for cross-entity relative comparison. But some governance indicators may have absolute threshold equivalents. `democratic_quality_score` from V-Dem identifies electoral autocracy thresholds that have some resemblance to absolute boundaries in the V-Dem framework. The M9 amendment should explicitly work through each governance indicator and determine whether a published, defensible absolute threshold exists. For most governance indicators, the answer will be "no, percentile rank is correct." For `democratic_quality_score`, it may be "yes." The M9 amendment should not assume the answer before doing this analysis.

**Q4:** Keep the static string constant through M10. Add a renewal trigger: "when more than 3 boundary domains are registered, the mandatory note approach must be revisited in the same commit as the fourth domain's addition." The proposed mandatory note text already satisfies M10+ forward compatibility because it references the table generically rather than enumerating specific domains.

**Q5:** The contract lives in this ADR; `design-decisions.md` holds a cross-reference with technical implementation detail only. The draft's own recommendation is correct. The `RadarChart.tsx` component test suite must include a test asserting that when `composite_score` is null and `framework === "governance"`, the rendered output includes neither a non-zero polygon vertex for governance nor the score value `0.00`.

#### Question 3: Highest Implementation Risk

**Decision M8-3 poses the highest implementation risk if misread or incompletely implemented.**

The risk: the strategy dispatch pattern's claim that `_compute_composite_score()`'s function signature is "unchanged" is incompatible with `_boundary_proximity_strategy()` requiring database-fetched, temporally-valid boundary constants. An implementor accepting this claim will implement the strategy without resolving the database access problem. The three failure modes (hardcode constants, synchronous DB call, wrong pre-fetch scope) are all silent — the code runs, scores are computed, but temporal validity is broken in backtesting.

One sentence of additional specification:

> "`_boundary_proximity_strategy()` must accept a pre-fetched `boundary_constants: dict[str, Decimal]` parameter — fetched from `simulation_reference_constants` in `get_measurement_output()` before strategy dispatch using a date-range query bounded by the simulation timestep — and `_compute_composite_score()` must be extended with a `context: dict[str, Any]` parameter that all strategies receive, making the signature change explicit rather than implicit; callers that do not require context pass an empty dict."

---

**Critical findings (Ecological Economist):**

1. `land_use_pressure_index` dimensional semantics must be specified explicitly. The amendment must state whether the raw indicator is dimensioned as (cropland / total land area, range 0–1, threshold at 0.25) or (fraction of boundary consumed, range 0–1, threshold at 1.0). Only the former is consistent with `/ 0.25` as the normalization denominator.
2. The strategy dispatch pattern's claim that the signature is unchanged is incompatible with the database access requirement.
3. Richardson et al. 2023 citation for the 0.25 boundary value requires a precise internal reference.

---

### Chief Methodologist

#### Preliminary Orientation

I speak for statistical integrity, uncertainty quantification, and distributional honesty. My central question throughout this review is: do the outputs this amendment enables make epistemically warranted claims? The draft is technically serious and internally consistent. My findings are gap identifications that, if unaddressed, will produce silent methodological failures of the kind this project exists to guard against. The five open questions at the end of the draft are exactly the right questions to surface.

#### Question 1: Per-Decision Assessment

**Decision M8-1: Ecological Composite Score — Boundary Proximity Normalization Formula**

Primary concern: The cap at 2.0 introduces a precision floor without adequate disclosure of what is lost above the cap.

The formula `min(current_value / boundary_value, 2.0)` is methodologically sound as far as it goes. The ratio interpretation is idiomatic to the planetary boundary literature, the unit-agnosticism is genuine, and the monotonicity argument for rejecting the inverse proximity alternative is correct.

The gap is the cap. Capping at 2.0 means that CO2 at 700 ppm and CO2 at 900 ppm both return a boundary_score of 2.0. The composite score for an entity at double the boundary and an entity at triple the boundary is identical. The mandatory note as written — "cap 2.0 = double safe boundary" — discloses the existence of the cap but does not disclose what is lost: **the composite score loses discriminating power for entities in severe exceedance.** A user seeing two entities with ecological composite score 2.0 cannot determine from the output whether one is twice over the boundary and the other is four times over. This is a false precision problem by omission.

**Specific gap:** The mandatory note in Decision M8-1 should be amended to add: "Entities operating above double the boundary value are indistinguishable in this composite; the raw indicator value must be consulted for severe exceedance cases." Without this, the note satisfies the letter of transparency but not its purpose.

**Additional gap:** The "mean boundary_score across all ecological indicators" aggregation treats CO2 boundary proximity and land-use boundary proximity as equally weighted inputs to the composite. The Rockström et al. framework does not assert that crossing the CO2 boundary by a factor of 1.2 is equally dangerous as crossing the land-use boundary by the same factor. Equal weighting is an implicit modeling assumption that has real consequences. The draft must either: (a) declare equal weighting as an explicit assumption with disclosure, or (b) explain why equal weighting is methodologically defensible for the two M8 indicators specifically. As written, equal weighting is embedded in "mean boundary_score" without any acknowledgment that this is a choice, not a neutral aggregation. This is precisely the class of false aggregation this project exists to guard against.

**Implementation obligation missing:** There is no requirement that `FrameworkOutput.note` for ecological framework include a count of how many indicators contributed to the composite. If only one of two indicators has a boundary constant, the user receives a composite with no indication of how many components it represents. The note should include an indicator count: "Composite derived from N of M registered indicators."

**Assessment:** The decision is mostly adequate but requires the cap disclosure amendment and the equal-weighting acknowledgment before the mandatory note text is finalized.

**Decision M8-2: `is_single_entity` Guard — Ecological Framework Exemption**

Primary concern: The decision is methodologically correct and the implementation specification is precise. A narrower statistical concern: the decision correctly identifies that boundary proximity is entity-count-independent, but it does not address whether the ecological composite score retains interpretive validity in single-entity scenarios because of the absence of comparative reference.

In a single-entity scenario, the financial and human_development axes are suppressed (null) because percentile rank is undefined. The ecological axis is active. The result is a radar chart where some axes show comparative performance and one axis shows absolute boundary proximity. These are not comparable quantities. The radar chart's visual form implies they are.

**Specific gap:** Decision M8-2 specifies the implementation correctly but does not flag the cross-axis interpretability problem for single-entity scenarios. The mandatory note for ecological `FrameworkOutput` in single-entity contexts should add a phrase indicating that the ecological score is an absolute boundary proximity measure, not a comparative performance score, and that direct visual comparison to percentile-based axes in multi-entity scenarios is not warranted. The radar chart rendering in single-entity mode may need to flag this interpretive asymmetry — that question should be raised with the UI/Frontend Architect, but the ADR should create the obligation.

**Implementation obligation missing:** No requirement exists that the `_SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS` constant addition triggers any disclosure change to the radar chart or FrameworkPanel display in single-entity mode.

**Assessment:** The decision is correct. The gap is a disclosure requirement for single-entity ecological scores, not a flaw in the exemption itself.

**Decision M8-3: `_compute_composite_score()` — Strategy Dispatch Pattern**

Primary concern: The fallback behavior for unregistered frameworks is a methodological risk disguised as a convenience.

The pattern `_COMPOSITE_STRATEGIES.get(framework, _DEFAULT_COMPOSITE_STRATEGY)` means that any framework string not in `_COMPOSITE_STRATEGIES` silently uses percentile rank. The draft's rationale — "preserving the existing behavior for all existing frameworks" — is engineering-comfortable but methodologically dangerous.

If a future implementor adds a framework to the system and does not register a strategy, the fallback does not fail — it computes a percentile rank and returns a score. The score is wrong (percentile rank may be a category error for the new framework), but it is not null and does not trigger a `[SIM-INTEGRITY]` WARNING. The error is invisible.

**Specific gap:** The fallback `_DEFAULT_COMPOSITE_STRATEGY` should not be a silent fallback. One of two alternatives is required:

Option A: The fallback emits a `[SIM-INTEGRITY]` WARNING when it fires for a framework that is not `financial` or `human_development` (the two frameworks for which percentile rank is methodologically validated). The warning text: "Framework '{framework}' has no registered composite strategy; using percentile rank as fallback. This may be a category error — see ADR-005 Decision M8-3."

Option B: The fallback raises an explicit error for unregistered frameworks, with `financial` and `human_development` registered explicitly rather than left to fallback. This eliminates the silent failure mode entirely.

Option A is more compatible with the existing architecture. Option B is more methodologically honest.

**Implementation obligation ambiguous:** The draft specifies that both strategy callables are dispatched with `(entity_indicators, all_entity_attrs, framework)` — implied but not stated. The callable type signature `Callable[..., Decimal | None]` uses `...` (any arguments), which means a strategy with the wrong signature compiles and fails only at call time. The type annotation should be tightened to the actual signature.

**Assessment:** The decision has a methodological integrity gap in the fallback design. The silent fallback for unregistered frameworks is a future `[SIM-INTEGRITY]` class failure waiting to happen.

**Decision M8-4: GovernanceModule Promotion — Deferred to M9**

Primary concern: The five-criteria table is well-constructed and the deferral is correct. My concern is the status of Criterion 2.

The draft marks Criterion 2 as "Partially met." In fact, the governance normalization methodology has not been specified at all — Amendment 1 Q4 confirmed percentile rank is "methodologically valid" but Q4 was a brief confirmation, not a normalization specification. The ADR does not contain a governance normalization decision analogous to Decision M8-1 for ecological.

**Specific gap:** Criterion 2 should be marked "Not met — methodology TBD" rather than "Partially met." This is not pedantic. The criterion table will be read by implementors at M9 to assess promotion readiness. "Partially met" implies one or two small items remain. "Not met" accurately communicates that the primary methodological work has not been done.

**No missing implementation obligations at M8** — the deferral is clean.

**Decision M8-5: Null Governance Axis Rendering — Binding UX Ruling**

Primary concern: The specification is precise and the reasoning is correct. My concern is a disclosure gap in the tooltip.

The hover tooltip specifies: `"Governance composite score is in validation. Promotion criteria: 0 of 5 met at M8. Target: M9."` This is excellent — it communicates that the null is a validation state, not a measurement failure.

The gap is that the tooltip does not direct the user to where they can inspect the five criteria. A sophisticated user seeing "0 of 5 met" will want to understand what the criteria are. The tooltip as written leaves them with no path forward. A link to methodology documentation or a "Learn more" affordance would close this.

**Implementation obligation missing:** The tooltip specification should include either: (a) a reference to where the promotion criteria are documented, or (b) an acknowledgment that a "See methodology" link is a UI/Frontend Architect obligation to be specified in design-decisions.md. Without this, the tooltip is a terminal disclosure.

The dashed outline specification is correct and necessary. The zero-value vs. null distinction is exactly the kind of epistemic precision failure this project must guard against.

**Decision M8-6: EcologicalModule M8 Indicator Expansion**

Primary concern: The confidence tier propagation rule is invoked but not fully specified for derived indicators.

The draft assigns:
- `planetary_boundary_co2_proximity`: Tier 1 (derived from Tier 1 Mauna Loa)
- `planetary_boundary_land_use_proximity`: Tier 3 (derived from Tier 3 FAO GFR)

The confidence tier of the derived indicator also depends on the confidence tier of the boundary constant, not only the source data. If the boundary constant itself carries uncertainty — and Rockström et al. 2009 explicitly does, noting that the 350 ppm figure is a "safe" value within a range, not a sharp threshold — then the derived proximity ratio inherits that boundary uncertainty as well as the data uncertainty.

**Specific gap:** The draft does not specify whether boundary constants carry a confidence tier, and if so, how derived indicator confidence propagates across both source data uncertainty and boundary specification uncertainty. A proximity ratio computed from a contested boundary constant should not carry Tier 1 confidence even if the source data is Tier 1. The confidence tier should be the max() of: source data tier, boundary constant tier. If boundary constants do not currently carry confidence tiers, they must be assigned one before this formula is implemented.

**Implementation obligation missing:** `simulation_reference_constants` must carry a `confidence_tier` field (or equivalent), and the derived indicator's confidence tier must be `max(source_data_tier, boundary_constant_tier)`. If this field does not exist, an Alembic migration must add it as part of the M8 EcologicalModule implementation. The current specification assigns Tier 1 to `planetary_boundary_co2_proximity` as if the 350 ppm boundary is a fact rather than a scientific judgment with associated uncertainty.

**The MDA threshold specification is correct.** Registering `boundary_score > 1.0` as MDASeverity.WARNING is methodologically appropriate. The derived indicator persistence rationale is sound.

**Assessment:** The decision is largely sound but has a material gap in boundary uncertainty propagation to confidence tiers.

#### Question 2: Open Questions Q1–Q5

**Q1:** Use effective-at-simulation-time values. Exclude indicators with no effective constant. Document the exclusion in the backtesting output as a methodologically correct vintage constraint, not a defect. The `_boundary_proximity_strategy()` must accept the simulation date as a parameter; the temporal query is per-timestep, not per-run. The Greece fixture consequence (one-indicator ecological composite throughout — land-use excluded pre-2023, and Greece ends in 2015 which is also pre-2023) should be documented in fixture expectations explicitly.

**Q2:** Per-entity mean of available indicators. The intersection approach systematically disadvantages data-rich scenarios. The comparability concern is real but the response is disclosure, not restriction. The `FrameworkOutput` must include the indicator count: "Ecological composite: mean of 2 boundary proximity indicators (CO2, land-use)." One renewal trigger warranted: "Ecological indicator count exceeds five — revisit composite aggregation methodology."

**Q3:** The M9 amendment must re-examine governance indicators for absolute threshold equivalents before confirming or rejecting percentile rank. Amendment 1 Q4 confirmation is insufficient as a methodology specification. Some governance indicators have absolute threshold equivalents: the V-Dem project, Freedom House, and Reporters Without Borders publish threshold interpretations for regime classification that are not arbitrary percentile cutoffs. A governance indicator at or below an established autocracy threshold has crossed a qualitative state boundary analogous to a planetary boundary crossing. The M9 amendment obligation: (a) audit each governance indicator for documented absolute threshold equivalents, (b) classify each as boundary-normalizable or percentile-rankable, (c) specify composite aggregation for a mixed set. This is more work than "confirm percentile rank."

**Q4:** The note must be partially dynamic — specifically, the indicator count and the list of contributing indicators must be generated at computation time, not hardcoded. The formula description and source citation can remain static. The practical split: **static** — formula text, score semantics, cap interpretation, source table reference; **dynamic** — indicator count and list ("Composite derived from 2 indicators: CO2 boundary proximity [boundary: 350 ppm], land-use boundary proximity [boundary: 0.25 ratio]"). This requires `_boundary_proximity_strategy()` to return metadata about which indicators contributed, so the note can be assembled dynamically. The `_ECOLOGICAL_MANDATORY_NOTE` constant becomes a template string with `{indicator_list}` and `{indicator_count}` substitution slots.

**Q5:** This ADR holds the binding contract. `design-decisions.md` holds implementation detail and cross-references this decision by number. No specification is duplicated. Frontends must read ADR-005 for rendering contracts. The only addition: `design-decisions.md DD-004` (or the M8 successor entry) should include a single sentence: "Rendering behavior for null vs. zero axes is fully specified in ADR-005 Decision M8-5; do not modify this entry without a corresponding ADR amendment." The concern that "frontend implementors must read ADR-005 during RadarChart implementation — which is unusual for component-level work" should not drive the document structure. Placing the specification in design-decisions.md to avoid this creates a lower-authority source of record for a high-authority decision, which is exactly backwards.

#### Question 3: Highest Implementation Risk

**Decision M8-3 (Strategy Dispatch Pattern) poses the highest implementation risk.**

The silent fallback is the failure mode. The amendment was motivated by a real methodological error — applying percentile rank to ecological indicators. The strategy dispatch is the architectural fix. But the fallback `_COMPOSITE_STRATEGIES.get(framework, _DEFAULT_COMPOSITE_STRATEGY)` means the architectural fix contains a silent path back to the original error. Any future framework added to the system that does not receive a registered strategy will be silently evaluated with percentile rank and will not fail, will not warn, and will not be caught in CI unless the test suite explicitly tests for the absence of the fallback for that framework.

The current test suite does not yet have a test asserting that all active `MeasurementFramework` values are registered in `_COMPOSITE_STRATEGIES` or explicitly exempted with rationale. Without that test, the fallback is invisible to CI.

One sentence of additional specification:

> "Any `MeasurementFramework` value not registered in `_COMPOSITE_STRATEGIES` and not in `_PERCENTILE_RANK_VALIDATED_FRAMEWORKS: frozenset[str] = frozenset({'financial', 'human_development'})` must trigger a `[SIM-INTEGRITY]` WARNING at computation time — the fallback is valid for validated frameworks only, not for any unrecognized framework string."

---

**Summary binding findings table (Chief Methodologist):**

| Finding | Decision | Severity |
|---|---|---|
| Cap at 2.0 loses discriminating power — not disclosed | M8-1 | High |
| Equal-weighting assumption not acknowledged | M8-1 | High |
| Missing indicator count in `FrameworkOutput.note` | M8-1 | Medium |
| Single-entity ecological score has cross-axis interpretability mismatch | M8-2 | Medium |
| Silent fallback for unregistered frameworks | M8-3 | High |
| Callable type annotation too loose | M8-3 | Low |
| Criterion 2 status "Partially met" overstates progress | M8-4 | Low |
| Governance tooltip lacks path to criteria inspection | M8-5 | Medium |
| Boundary constants lack confidence tiers | M8-6 | High |

**Panel disposition recommendation (Chief Methodologist):** The draft is not ready for Engineering Lead acceptance without resolution of the four High-severity findings (cap disclosure/equal-weighting in M8-1, silent fallback in M8-3, and boundary constant confidence tiers in M8-6). The Medium findings should be resolved before implementation begins.

---

## Cross-Cutting Concerns Table

Concerns raised independently by two or more agents, without coordination.

| # | Concern | Decisions | Agents | Severity |
|---|---|---|---|---|
| CC-1 | **Database access pathway for boundary constants unspecified.** `_compute_composite_score()` has no DB connection; `_boundary_proximity_strategy()` needs boundary constants from `simulation_reference_constants`. The claim "signature unchanged, existing callers require no modification" is incompatible with this requirement. The call chain must be specified — either pre-fetch in `get_measurement_output()` and pass via parameter, or via a context object. | M8-1, M8-3 | Data Architect, QA Lead, Ecological Economist | **Critical** |
| CC-2 | **`_boundary_proximity_strategy()` callable signature underspecified.** `Callable[..., Decimal | None]` uses `...` (any arguments), deferring parameter-passing for boundary constants to the implementor. Will produce inconsistent implementations. Should be narrowed to an explicit TypeAlias once the DB access pathway (CC-1) is resolved. | M8-3 | Data Architect, QA Lead, Chief Methodologist | High |
| CC-3 | **Missing indicator count in `FrameworkOutput.note`.** The ecological composite is a mean of N indicators, but the mandatory note does not state N. A user receiving a Greece ecological composite does not know whether it is based on 1 or 2 boundary proximity indicators. Comparability between entities with different indicator sets is invisible without this disclosure. | M8-1 | Chief Methodologist, Ecological Economist, QA Lead (partial) | High |
| CC-4 | **`land_use_pressure_index` dimensional ambiguity.** The module docstring describes the indicator as "fraction of the safe land-system boundary consumed (0–1)", which conflicts with the amendment's use of `/ 0.25` as the normalization denominator. If the indicator is already expressed as fraction-of-boundary-consumed (1.0 = boundary met), dividing by 0.25 produces a double-normalized result with scores up to 4.0. The physical dimensioning must be specified before implementation. | M8-1, M8-6 | Ecological Economist, QA Lead | **Critical** |
| CC-5 | **`source_registry` rows for Rockström 2009 and Richardson 2023 not named as implementation obligation.** Derived `Quantity` attributes require `source_registry_id` as FK into `source_registry`, not into `simulation_reference_constants`. The amendment specifies that proximity indicators reference the boundary constant source, but does not explicitly require Alembic migrations to register these publications in `source_registry`. | M8-6 | Data Architect, Ecological Economist | High |
| CC-6 | **Tooltip "0 of 5 met at M8" hardcodes stale criterion count.** The governance tooltip text will be factually wrong once M9 begins satisfying promotion criteria. Either the count must be dynamically sourced, or the text must omit the specific count and reference the framework promotion protocol document. | M8-5 | QA Lead, Chief Methodologist | Medium |
| CC-7 | **M8-4 Criterion 2 "Partially met" overstates progress.** "Partially met" implies the criterion is close to satisfied. In fact, the primary methodological work — specifying whether governance uses percentile rank, absolute thresholds, or hybrid — has not been done. "Not met — methodology TBD" is more accurate. An overeager M9 implementor may read "Partially met" as partial authorization. | M8-4 | QA Lead, Chief Methodologist | Low |
| CC-8 | **Decision 4's `RadarAxisDatum` TypeScript interface conflicts with M8-5 rendering requirement.** The existing `composite_score: number` type cannot represent the em dash `"—"` required by M8-5. The `is_implemented: bool → 0.0 render` pattern directly contradicts "zero-value rendering is prohibited." The M8-5 implementation PR must update the Decision 4 interface specification in the same commit (cross-ADR impact rule). | M8-5 | Data Architect, QA Lead | High |
| CC-9 | **`EcologicalModule.compute()` uses delta event pattern; proximity requires stock values.** The existing module reads `state.events` (prior-step deltas). Boundary proximity requires the entity's accumulated current attribute value, not the step delta. An implementor following the existing pattern will produce proximity scores that drift by the delta each timestep rather than reflecting the actual concentration ratio. | M8-6 | QA Lead, Ecological Economist | **Critical** |

---

## Disagreements Table

Direct conflicts between agents requiring Engineering Lead decision.

| # | Question | Agents in Conflict | Position A | Position B | Recommendation |
|---|---|---|---|---|---|
| D-1 | **Q4: Static vs. dynamic mandatory note** | Chief Methodologist vs. Data Architect / QA Lead / Ecological Economist | **CM:** Note should be partially dynamic now — indicator count and list generated at computation time; formula text remains static. The `_ECOLOGICAL_MANDATORY_NOTE` becomes a template string. | **DA/QA/EE:** Static string is acceptable through M10 as long as it references the source table generically (not enumerating domains). Add a renewal trigger at domain count > 3–4. | **Panel 3:1 majority favors static through M10.** CM's indicator-count concern is valid but can be addressed by requiring the note to state "N indicators contributing" without requiring full dynamic generation. Suggested resolution: static template with `{n_contributing}` slot filled at computation time (minimal infrastructure change). |
| D-2 | **Highest-risk decision vote** | Split 4 ways | **DA:** M8-1 (DB access pathway) | **QA:** M8-6 (delta vs. stock computation) | **EE + CM:** M8-3 (strategy dispatch fallback / DB access) | M8-3 wins 2 votes. However, all identified failure modes are silent. All four flagged risks warrant specification improvement regardless of vote. |
| D-3 | **M8-3 fallback behavior** | Chief Methodologist vs. others | **CM:** Add `_PERCENTILE_RANK_VALIDATED_FRAMEWORKS` constant; fallback emits `[SIM-INTEGRITY]` WARNING for any framework not in validated set. Explicit Option A (warn) or Option B (error). | **DA/QA/EE:** Did not explicitly address the silent fallback problem; focused on DB access gap. | **CM's position is correct.** The silent fallback is a methodological integrity gap independently of the DB access issue. Both problems must be resolved. CM's Option A (`[SIM-INTEGRITY]` WARNING) is more compatible with the existing architecture than Option B. |

---

## Q1–Q5 Panel Dispositions

### Q1 — Temporal validity of boundary constants in backtesting scenarios

**Panel disposition: Use the constant effective at simulation time. UNANIMOUS (4/4).**

All four agents independently reached the same conclusion. `DATA_STANDARDS.md §Backtesting Integrity` "vintage dating required for all backtesting inputs" is binding and applies to boundary constants as it does to entity attribute data.

**Concrete consequence:** For the Greece 2010–2015 backtesting fixture, `planetary_boundary_land_use_proximity` is absent from the ecological composite for all timesteps (Greece 2015 predates the Richardson 2023 `effective_from` of 2023-09-13). The ecological composite for the Greece fixture is CO2 proximity only. This is correct output, not a deficiency.

**Implementation obligation that must be added to Decision M8-1:** The DB query for boundary constants must use the simulation timestep date as the resolution point, not wall-clock date. The distinction between "constant absent from the table" and "constant temporally unavailable" must be explicit: both emit `[SIM-INTEGRITY]` WARNINGs, but with different warning text. The fixture expectations for Greece 2010–2015 must explicitly document the expected one-indicator ecological composite.

---

### Q2 — Composite score aggregation when indicator count varies across entities

**Panel disposition: Per-entity mean of all available boundary scores. Do not restrict to intersection. UNANIMOUS (4/4).**

Intersection restriction disadvantages data-rich entities by forcing all composites to the minimum common denominator of the least-covered entity. The correct response to indicator count asymmetry is disclosure, not restriction.

**Required addition:** The mandatory note must include a contributing indicator count (N-of-M). This satisfies both the comparability disclosure need and the Chief Methodologist's concern about opaque aggregation. The simplest implementation: `_boundary_proximity_strategy()` returns both the composite Decimal and a metadata dict `{"contributing_indicators": n, "total_registered": m}`, and the caller assembles the note string using this metadata. This resolves the D-1 disagreement via a lightweight dynamic component without requiring full note-generation infrastructure.

---

### Q3 — Governance composite score normalization methodology

**Panel disposition: M9 amendment must explicitly re-examine governance indicators for absolute threshold equivalents before confirming or defaulting to percentile rank. UNANIMOUS (4/4).**

Amendment 1 Q4 confirmation is insufficient as a methodology specification and must not be carried forward as a settled decision. The development of the ecological boundary normalization formula has changed the epistemic situation: the question is now "do any governance indicators have the same structural property as planetary boundaries?" not merely "is percentile rank valid for governance?"

**Recommended M9 amendment text:** "Amendment 1 Q4's confirmation of percentile rank remains operative as the default position for governance indicators that lack documented absolute threshold equivalents. The M9 amendment author must conduct an explicit per-indicator audit for each governance indicator in the module, assessing whether a published, peer-reviewed, externally-defined absolute threshold exists (analogous to planetary boundary constants). Indicators with such thresholds must use boundary-proximity normalization; indicators without them may use percentile rank. A mixed indicator set requires specification of composite aggregation methodology. This audit is mandatory and must be documented in the M9 amendment's 'Alternatives Considered' section."

The Ecological Economist specifically identified `democratic_quality_score` (V-Dem) as a likely candidate for absolute threshold treatment. The Data Architect flagged Freedom House's "Not Free" / "Partly Free" / "Free" categorical thresholds as documented absolute classifications.

---

### Q4 — `_ECOLOGICAL_MANDATORY_NOTE` static string vs. dynamic generation

**Panel disposition: Static through M10 with a lightweight dynamic indicator count. MAJORITY (3/4), with modification to address Chief Methodologist's concern.**

Three agents (Data Architect, QA Lead, Ecological Economist) favor static string through M10 with renewal trigger. Chief Methodologist favors partial dynamic generation now. The panel's recommended resolution threads both:

- **Static elements (no infrastructure change):** Formula text, score semantics, cap interpretation, source table reference.
- **Lightweight dynamic element (minimal change):** Contributing indicator count (`N indicators contributing`). `_boundary_proximity_strategy()` returns a metadata dict alongside the composite score; the caller assembles the note using a template string with one substitution slot. This requires no new architectural pattern — it is note string assembly.
- **Renewal trigger added:** "If `_ECOLOGICAL_MANDATORY_NOTE` is updated to enumerate specific indicator domain names, it must be converted to API-generated text sourced from `simulation_reference_constants` in the same commit. Enumerating domains in a static string is non-compliant from that point forward."
- **Second renewal trigger added:** "When the registered planetary boundary domain count exceeds four, the mandatory note approach must be reviewed in the same commit as the fourth domain's addition."

This satisfies the Chief Methodologist's epistemic requirement (composite composition is visible) without requiring full dynamic infrastructure at M8.

---

### Q5 — Dashed outline rendering: ADR vs. design-decisions.md

**Panel disposition: ADR holds the binding contract; design-decisions.md entry created in the same commit, cross-referencing by decision number only. UNANIMOUS (4/4).**

All four agents agreed with the draft's own recommendation. Two refinements required:

1. The `design-decisions.md` entry must include an explicit sentence: "Rendering behavior for null vs. zero axes is fully specified in ADR-005 Decision M8-5; do not modify this entry without a corresponding ADR amendment." This is not optional — it is the enforcement mechanism for the documentation hierarchy.
2. The M8-5 implementation obligation must name the `design-decisions.md` entry creation as a same-commit requirement, not a follow-up. The ADR contract and its design-decisions.md cross-reference must be created atomically.

---

## Highest-Risk Decision Vote

| Agent | Vote | One-sentence specification improvement |
|---|---|---|
| Data Architect | **M8-1** | "The boundary constant lookup query must be executed in `get_measurement_output` (the async database handler), using the snapshot's simulation timestep as `$run_date` per the historical-resolution query in `database.yml §query_notes`, and the resolved constants dict must be passed as an explicit parameter to `_boundary_proximity_strategy()` — the strategy function itself must not contain database access." |
| QA Lead | **M8-6** | "The proximity indicators `planetary_boundary_co2_proximity` and `planetary_boundary_land_use_proximity` are computed from the entity's accumulated current attribute value (read from `entity.attributes[key].value`), not from the step's event delta magnitude — the distinction is critical: using an event delta produces a monotonically-drifting proximity score rather than a ratio of current state to boundary, which would be computationally indistinguishable from correct behavior until an absolute-value fixture test is run." |
| Ecological Economist | **M8-3** | "`_boundary_proximity_strategy()` must accept a pre-fetched `boundary_constants: dict[str, Decimal]` parameter — fetched from `simulation_reference_constants` in `get_measurement_output()` before strategy dispatch using a date-range query bounded by the simulation timestep — and `_compute_composite_score()` must be extended with a `context: dict[str, Any]` parameter that all strategies receive, making the signature change explicit rather than implicit; callers that do not require context pass an empty dict." |
| Chief Methodologist | **M8-3** | "Any `MeasurementFramework` value not registered in `_COMPOSITE_STRATEGIES` and not in `_PERCENTILE_RANK_VALIDATED_FRAMEWORKS: frozenset[str] = frozenset({'financial', 'human_development'})` must trigger a `[SIM-INTEGRITY]` WARNING at computation time — the fallback is valid for validated frameworks only, not for any unrecognized framework string." |

**Winner: M8-3 — 2 votes (Ecological Economist, Chief Methodologist).**

Note: both agents who voted M8-3 identified different specification improvements — one targeting the DB access pathway (EE) and one targeting the silent fallback (CM). Both are critical and must both be addressed. The M8-3 implementation risk is composite: the DB access gap produces silent temporal validity failures in backtesting; the silent fallback produces silent category errors for future frameworks.

**Recommended combined specification addition for M8-3:**

Add two obligations to Decision M8-3 §Implementation Obligations:

> **Obligation 5:** `_compute_composite_score()` must accept a `context: dict[str, Any]` parameter passed through to all strategies. At M8 this context carries `boundary_constants: dict[str, Decimal]` pre-fetched from `simulation_reference_constants` in `get_measurement_output()` using a date-range query bounded by the snapshot's simulation timestep. Strategies that do not use the context receive it as an empty dict. This change does not break existing callers — they pass `context={}`.
>
> **Obligation 6:** Add `_PERCENTILE_RANK_VALIDATED_FRAMEWORKS: frozenset[str] = frozenset({"financial", "human_development"})`. The fallback `_DEFAULT_COMPOSITE_STRATEGY` must emit a `[SIM-INTEGRITY]` WARNING when it fires for any framework not in this set. Warning text: "Framework '{framework}' has no registered composite strategy; using percentile rank as fallback — this may be a category error. See ADR-005 Decision M8-3."

---

## Decisions Flagged for Revision

Summary of which decisions the panel identified as requiring revision before this draft is committed to `ADR-005-human-cost-ledger.md`, organized by severity.

### Must be resolved before Engineering Lead acceptance

| Decision | Finding | Required action |
|---|---|---|
| M8-1 | DB access call chain unspecified (CC-1) | Add implementation obligation specifying pre-fetch in `get_measurement_output()` and context parameter passing |
| M8-1 | `FrameworkOutput.composite_score` schema range conflict (DA) | Add implementation obligation: update `schemas.py` docstring and `api_contracts.yml` to note `[0.0, 2.0]` range for ecological |
| M8-1 | Equal-weighting assumption not declared (CM) | Add to mandatory note: "Equal weighting applied across contributing indicators — see ADR-005 Decision M8-1 for rationale" |
| M8-1 | Cap at 2.0 loses discriminating power — not disclosed (CM) | Add to mandatory note: "Entities operating above double the boundary value are indistinguishable in this composite; consult raw indicator values for severe exceedance cases" |
| M8-3 | Silent fallback for unregistered frameworks (CM) | Add `_PERCENTILE_RANK_VALIDATED_FRAMEWORKS`; fallback emits `[SIM-INTEGRITY]` WARNING for unvalidated frameworks |
| M8-3 | DB access gap makes "signature unchanged" claim false (CC-1) | Add `context: dict[str, Any]` parameter to `_compute_composite_score()` and all strategy callables |
| M8-5 | `RadarAxisDatum.composite_score: number` conflicts with "—" em dash display (CC-8) | Add implementation obligation: M8-5 PR must update Decision 4 TypeScript interface in same commit (cross-ADR impact rule) |
| M8-6 | `land_use_pressure_index` dimensional ambiguity (CC-4) | Add explicit specification of physical dimensioning: must be (cropland / total land area), range 0–1, threshold at 0.25; add `[SIM-INTEGRITY]` WARNING if raw value > 1.0 before proximity calculation |
| M8-6 | Delta vs. stock computation pattern (CC-9) | Add implementation obligation: proximity must read `entity.attributes[key].value` (accumulated stock), not event delta magnitude |
| M8-6 | Boundary constants lack confidence tiers (CM) | Add implementation obligation: `simulation_reference_constants` must carry `confidence_tier` field; derived indicator tier = `max(source_data_tier, boundary_constant_tier)` |

### Should be resolved before implementation begins

| Decision | Finding | Required action |
|---|---|---|
| M8-1 | Missing indicator count in `FrameworkOutput.note` (CC-3) | Modify mandatory note to include N-contributing-indicators via lightweight template substitution |
| M8-2 | Missing test obligation for single-entity ecological exemption (QA) | Add: `test_single_entity_ecological_score_is_non_null()` must be added in same commit |
| M8-2 | Note content unspecified for single-entity ecological `FrameworkOutput` (EE, QA) | Add: mandatory note (not `_SINGLE_ENTITY_NOTE`) applies to single-entity ecological outputs |
| M8-2 | Cross-axis interpretability mismatch in single-entity scenarios not disclosed (CM) | Add: single-entity ecological note must indicate score is absolute boundary proximity, not comparative |
| M8-4 | `source_field_registry` not in `database.yml` (DA) | Resolve: confirm table name (should it be `source_registry`?) and update criterion 3 text |
| M8-4 | Criterion 2 "Partially met" overstates progress (CC-7) | Change to "Not met — methodology TBD"; clarify criterion 2 is satisfied only by a named and registered strategy |
| M8-5 | Tooltip hardcodes stale criterion count (CC-6) | Resolve: either source count dynamically or omit count from static text and reference Framework Promotion Protocol |
| M8-5 | Tooltip lacks path to criteria inspection (CM) | Add: "See methodology" affordance obligation in tooltip specification |
| M8-5 | E2E test obligation for governance null axis not named (QA) | Add: Playwright test `tests/e2e/radar-governance-null-axis.spec.ts` must exist before M8 closes |
| M8-6 | `source_registry` Alembic migration not named (CC-5) | Add: explicit obligation to register Rockström 2009 and Richardson 2023 in `source_registry` with stable `source_id` values |
| M8-6 | Richardson 2023 citation needs precise internal reference (EE) | Add Table/Figure/supplementary dataset number from Richardson et al. 2023 for the 0.25 value |
| M8-6 | `entity_scope` for MDA seed data not specified (QA) | Add: `entity_scope = "all"` for planetary boundary MDA threshold entries |

### Can be resolved in implementation PR (ADR amendment not required)

| Decision | Finding | Action |
|---|---|---|
| M8-3 | `Callable[..., Decimal | None]` type annotation too loose | Tighten to explicit TypeAlias once CC-1 is resolved |
| M8-4 | Criterion 3 table note for governance guard mechanism imprecise | Clarify that governance never reaches the guard at M8 (unimplemented-frameworks gate fires first) |
| Q4 | Renewal trigger for domain count threshold | Add renewal trigger: static note revisited when 4th boundary domain registered |
| Q5 | `design-decisions.md` enforcement sentence | Add "do not modify without corresponding ADR amendment" sentence in design-decisions.md entry |

---

*End of synthesis. Produced 2026-05-17. Engineering Lead disposition of all findings required before ADR-005 Amendment 3 is committed to `docs/adr/ADR-005-human-cost-ledger.md`.*
