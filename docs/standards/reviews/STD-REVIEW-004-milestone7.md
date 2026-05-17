# STD-REVIEW-004: Milestone 7 Exit Standards Gap Inventory

**Review type:** Full — all standards documents, seeded by ARCH-REVIEW-005 findings
**Scope:** `docs/DATA_STANDARDS.md`, `docs/CODING_STANDARDS.md`, `docs/adr/ADR-005-human-cost-ledger.md`,
`docs/architecture/reviews/ARCH-REVIEW-005-milestone7.md`,
`docs/scenarios/module-capability-registry.md`
**Date:** 2026-05-10
**Milestone:** Milestone 7 exit / Milestone 8 readiness
**Status:** Complete — GitHub Issues referenced for all findings requiring tracking

---

## Purpose

STD-REVIEW-004 audits the standards documents for gaps that will affect Milestone 8
implementation. It is seeded by ARCH-REVIEW-005 findings, which identified six
architectural domains where M8 module completion proceeds without adequate standards
coverage.

A standards gap means: an ADR or architecture review document declares a requirement
but the corresponding standards document has not been updated to include that rule.
Developers implementing M8 Ecological and Governance module completion will read
`DATA_STANDARDS.md` and `CODING_STANDARDS.md`, not ADR prose. If the rule is only
in the ADR, it will not be enforced.

Milestone 7 delivered three standards document updates: the Defensive Programming
section in CODING_STANDARDS.md (PR #246), `[SIM-INTEGRITY]` logging contract
documented in practice (no dedicated standards section — see Gap 5 below), and
the field-level data certification gap formalized as Issue #252. This review
audits what was not closed.

---

## Documents Read

| Document | Notes |
|---|---|
| `docs/DATA_STANDARDS.md` | Full read |
| `docs/CODING_STANDARDS.md` | Full read |
| `docs/adr/ADR-005-human-cost-ledger.md` | Full read (Amendment B M8 obligations) |
| `docs/architecture/reviews/ARCH-REVIEW-005-milestone7.md` | Full read |
| `docs/scenarios/module-capability-registry.md` | Full read |
| `app/simulation/modules/ecological/module.py` | Inspected for unit usage |
| `app/api/scenarios.py` | Inspected for composite score computation |

---

## Findings

### Gap 1 — DATA_STANDARDS.md: No canonical unit registry

**Severity:** Immediate
**Required amendment:** `docs/DATA_STANDARDS.md`
**GitHub Issue:** #252 (Comment 1 — unit standardization requirement)

**Description:**

`EcologicalModule.compute()` produces all ecological indicator Quantities with
`unit="dimensionless"` regardless of the indicator's actual unit:

```python
# app/simulation/modules/ecological/module.py:121
affected_attributes = {
    key: Quantity(
        value=delta,
        unit="dimensionless",   # placeholder — incorrect for co2_concentration_ppm
        ...
    )
    for key, delta in indicator_deltas.items()
}
```

The indicator `co2_concentration_ppm` declares its unit in its name. The elasticity
file acknowledges this inconsistency in a comment but the module does not use the
correct unit string. The `GovernanceModule` uses `VariableType.DIMENSIONLESS` for
all governance indicators — `rule_of_law_percentile` is a percentile (0–100 range)
and should carry a unit that distinguishes it from a ratio (0–1 range).

Without a canonical unit registry, there is no authoritative source for what unit
string is correct for each internal attribute. Every new indicator added in M8
will face the same choice: use `"dimensionless"` as a placeholder or invent an
ad hoc string.

DATA_STANDARDS.md has no §Canonical Unit Registry section. There is no controlled
vocabulary for valid unit strings, no canonical unit per internal attribute, and no
validation gate that rejects Quantity instantiations with non-canonical units.

The Gimli Glider incident (1983: aircraft ran out of fuel mid-flight due to fuel
loaded in kg when the system assumed lb) and the Mars Climate Orbiter incident
(1999: spacecraft destroyed due to angular momentum reported in pound-force·seconds
by one subsystem and newton·seconds by another) are both architectural analogs to
this failure mode. WorldSim currently has no unit validation at any layer.

**Required amendment to DATA_STANDARDS.md:**

Add a §Canonical Unit Registry subsection specifying:

1. **Controlled vocabulary**: The authoritative list of valid unit strings for
   WorldSim internal attributes. At minimum: `"ppm"`, `"ratio_0_1"`,
   `"ratio_0_100"` (percentile), `"dimensionless"` (explicitly zero-dimensional,
   not a placeholder), `"USD"`, `"percent"`, `"index"`.
2. **One canonical unit per internal attribute**: For every internally produced
   attribute (not raw source data), one canonical unit string is declared.
   Deviations require a compliance scan exception.
3. **Conversion documentation requirement**: When source data arrives in a
   non-canonical unit, the conversion must be documented in the relevant
   `source_field_registry` entry (Issue #252) with the conversion formula and
   any precision loss bound.
4. **Runtime validation gate**: The compliance scan (or a module-level guard)
   must flag Quantity instantiations that use `unit="dimensionless"` for
   attributes whose canonical unit is not dimensionless.

---

### Gap 2 — DATA_STANDARDS.md: No field-level data certification standard

**Severity:** Immediate
**Required amendment:** `docs/DATA_STANDARDS.md`
**GitHub Issue:** #252

**Description:**

DATA_STANDARDS.md §Data Provenance Requirements defines source-level registration
(`SourceRegistration`, `LiteratureSourceRegistration`). This certifies that a
source is approved and describes what it covers. It does not certify how individual
fields within that source map to WorldSim's internal attribute space.

Milestone 8 will register new sources — World Governance Indicators (WGI),
planetary boundary reference data (Rockström/Steffen), expanded FAO data for
deforestation. For each source, there are potentially dozens of fields. The field
that maps to `rule_of_law_percentile` in WorldSim may be `RL.EST` in WGI XLSX
format — a numeric code whose meaning requires looking up a separate codebook.
The transformation from `RL.EST` to `rule_of_law_percentile` involves units
(WGI reports in standard normal units; WorldSim's indicator is a 0–100 percentile),
scaling, and possibly aggregation across years.

None of this is documented anywhere. When a new data engineer joins M8 and asks
"how does `RL.EST` become `rule_of_law_percentile`?", there is no artifact to point
to. The mapping lives only in extraction code — which may be wrong, may change
silently, and has no mechanism for certification by the Data Architect Agent.

This is the "naming-as-identity" failure class: `RL.EST` and `rule_of_law_percentile`
share a conceptual relationship, but the transformation between them is invisible
to the system. Conversely, two sources might both have a field called "rule of law"
that measure completely different things (the "reverse-video" failure class).

**Required amendment to DATA_STANDARDS.md:**

Add a §Field-Level Data Certification subsection specifying:

1. **`source_field_registry` structure**: For each registered source, a
   field-level dictionary entry mapping source field name → WorldSim internal
   attribute, including: source field identifier, source unit, canonical
   WorldSim unit, transformation formula or reference, confidence_tier,
   and Data Architect sign-off date.
2. **Certification requirement**: A source may not be used in a production
   simulation run unless all fields accessed from that source have a certified
   `source_field_registry` entry. Fields accessed without a certified entry
   are compliance violations.
3. **Dependent field documentation**: Where a field's meaning depends on the
   value of another field in the same record (e.g., record type determines
   column semantics), the dependency must be documented explicitly with the
   resolution logic.
4. **Cross-reference to canonical unit registry** (Gap 1): The target unit in
   each `source_field_registry` entry must be drawn from the canonical unit
   controlled vocabulary.

---

### Gap 3 — DATA_STANDARDS.md: WGI territorial convention not addressed

**Severity:** Near-term
**Required amendment:** `docs/DATA_STANDARDS.md`
**GitHub Issue:** None — file as part of WGI source registration work

**Description:**

DATA_STANDARDS.md §Territorial Positions documents WorldSim's declared positions
on contested territories: Taiwan, Palestine, Kosovo, Western Sahara, Crimea. For
Taiwan specifically, WorldSim's position must be documented (the declared position
is not inspected in this review — only the gap is identified).

World Governance Indicators (WGI) — the authoritative source for
`rule_of_law_percentile`, `control_of_corruption_index`, and related governance
attributes — uses "Taiwan, China" as the entity label, encoding a territorial claim
in a source identifier. This is not merely a naming convention difference: it is
the WGI's expression of a contested geopolitical position.

When WGI data is loaded into WorldSim and `simulation_entities` are matched by
name, a lookup for "Taiwan" will fail to match "Taiwan, China" unless a resolution
layer handles the translation. DATA_STANDARDS.md currently provides no guidance
for governance indicator source conventions that conflict with WorldSim's declared
territorial positions.

**Required amendment to DATA_STANDARDS.md:**

Add to §Territorial Positions:

1. A section on **Source-Convention Conflict Resolution**: when a registered data
   source uses entity labels that encode territorial claims differing from
   WorldSim's declared positions, the source entry must document the conflict
   and the resolution approach (silent rename, provenance note, exclusion).
2. Specifically for WGI: document the "Taiwan, China" → WorldSim entity mapping,
   including the rationale for the resolution choice, and cross-reference to
   WorldSim's declared Taiwan territorial position.
3. A requirement that the Data Architect Agent reviews all governance indicator
   source registrations for territorial convention conflicts before those sources
   are used in production simulation runs.

---

### Gap 4 — DATA_STANDARDS.md: Ecological composite score normalization methodology not documented as a data standard

**Severity:** Immediate
**Required amendment:** `docs/DATA_STANDARDS.md`
**GitHub Issue:** Linked to ARCH-REVIEW-005 Blindspot 1-A; no standalone issue yet

**Description:**

ARCH-REVIEW-005 Blindspot 1-A identifies that M8 ecological composite score must
use planetary boundary absolute normalization rather than cross-entity percentile
rank. ADR-005 Amendment B declares this obligation and defers the implementation
to M8. But the normalization methodology itself — the formula, the reference values,
and the source — is not documented in DATA_STANDARDS.md as a data standard.

Specifically:

1. **Planetary boundary reference values** (e.g., 350 ppm CO2 for safe climate
   space — Rockström et al. 2009) are fixed scientific thresholds, not time-series
   data. DATA_STANDARDS.md §Data Provenance Requirements is designed for empirical
   dataset registration. A planetary boundary threshold is not a dataset — it is
   a model calibration constant derived from peer-reviewed science.

2. No §Simulation Reference Constants section exists in DATA_STANDARDS.md. There
   is no standard for how a fixed scientific threshold enters the system: Does it
   get a `source_registry_id`? Is it stored in a dedicated table? Is it a constant
   in code? If it changes when a new scientific consensus emerges, how is the update
   governed?

3. Without a standard, the M8 ecological normalization implementation will define
   its own convention — which creates a consistency gap the first time a second
   boundary-normalized framework is added.

**Required amendment to DATA_STANDARDS.md:**

Add a §Simulation Reference Constants subsection specifying:

1. **Definition**: A simulation reference constant is a fixed numerical threshold
   or calibration value derived from scientific consensus or peer-reviewed literature
   that is not an empirical time-series observation. Planetary boundary thresholds
   are the canonical example.
2. **Registration format**: Reference constants are registered as
   `LiteratureSourceRegistration` entries (existing, from Issue #172 resolution)
   with an additional `constant_type: reference_threshold` discriminator field.
   The constant value and its unit are recorded alongside the source citation.
3. **Update governance**: When the scientific consensus changes (new Steffen et al.
   revision, for example), the old constant is not deleted — it is versioned with
   an `effective_through` date and a new entry is added. Historical simulation runs
   that used the old constant must be traceable to the constant version in effect
   at run time.
4. **Database location**: Reference constants are stored in a dedicated
   `simulation_reference_constants` table (or, if that table does not yet exist,
   as a declared constant in a registered source fixture file with a documented
   update protocol). This decision requires Data Architect sign-off before M8
   ecological module completion.

---

### Gap 5 — CODING_STANDARDS.md: No `_UNIMPLEMENTED_FRAMEWORKS` promotion protocol

**Severity:** Near-term
**Required amendment:** `docs/CODING_STANDARDS.md`
**GitHub Issue:** None — create as part of M8 governance module completion work

**Description:**

`_UNIMPLEMENTED_FRAMEWORKS = {"governance"}` in `app/api/scenarios.py` is the
mechanism by which incomplete modules are shielded from the API surface. When a
module is promoted from "initial" to "complete," removing its framework string
from this set exposes all previously hidden outputs. This is a material API surface
change.

No documented protocol specifies what conditions must be met for promotion. The
current implicit behavior is: whenever an implementer decides the module is ready,
they remove the string. This creates two failure modes:

1. **Premature promotion**: Module outputs are exposed before validation is
   complete, before the composite score normalization is decided, and before
   the ADR-005 amendment has been accepted. The API returns governance scores
   that no reviewer has verified against known historical cases.

2. **Indefinite deferral**: Without a stated completion criterion, promotion is
   perpetually deferred as "not quite ready" — the inverse failure mode, where
   completed work is not surfaced because no one declared what "complete" means.

CODING_STANDARDS.md has no section covering the `_UNIMPLEMENTED_FRAMEWORKS`
pattern, its lifecycle, or the promotion criteria.

**Required amendment to CODING_STANDARDS.md:**

Add a §Framework Promotion Protocol subsection specifying:

1. **Promotion criteria**: A framework may be removed from `_UNIMPLEMENTED_FRAMEWORKS`
   only when all of the following are true:
   - At least one historical backtesting case passes DIRECTION_ONLY thresholds for
     at least one indicator from this framework.
   - The composite score normalization methodology is documented in an accepted
     ADR amendment.
   - The `source_field_registry` entries for all indicators surfaced by this
     framework are certified (Gap 2 above).
   - A `[SIM-INTEGRITY]` WARNING is emitted when the module produces a
     `composite_score=None` outcome unexpectedly (i.e., for a reason other than
     single-entity scenario).
2. **ADR amendment trigger**: Promotion must be an explicitly named deliverable
   in the relevant ADR amendment — it cannot happen as a side effect of another
   commit.
3. **Compliance scan requirement**: The compliance scan entry at the milestone
   that promotes a framework must explicitly record the promotion and confirm
   that all promotion criteria were met.
4. **Reversion protocol**: If post-promotion validation reveals a failure, the
   string can be re-added to `_UNIMPLEMENTED_FRAMEWORKS` as a documented rollback.
   The compliance scan must record the rollback and the root cause.

---

### Gap 6 — CODING_STANDARDS.md: No `[SIM-INTEGRITY]` monitoring contract standard

**Severity:** Near-term
**Required amendment:** `docs/CODING_STANDARDS.md`
**GitHub Issue:** None — should be documented as part of M7 exit hygiene

**Description:**

Milestone 7 established the `[SIM-INTEGRITY]` prefix as a stable monitoring
contract: any log line prefixed with `[SIM-INTEGRITY]` signals a simulation
integrity anomaly that should trigger operator investigation. The three implemented
hooks are in `propagation.py` (dropped delta, STOCK conflict) and `runner.py`
(duplicate event_id).

This contract exists in code and in the M7 session history, but it is not
documented in CODING_STANDARDS.md. A developer adding a new module who discovers
an integrity anomaly during M8 implementation has no standard telling them to
use `[SIM-INTEGRITY]` rather than logging a WARNING without the prefix. The
monitoring contract's value depends entirely on the prefix being used consistently
— one untagged anomaly breaks the `grep '[SIM-INTEGRITY]'` alerting pattern.

**Required amendment to CODING_STANDARDS.md:**

Add a §Simulation Integrity Monitoring subsection specifying:

1. **Contract definition**: Any log message reporting a simulation integrity
   anomaly — unexpected state, contract violation, data conflict, or structural
   warning that operators may need to investigate — must be prefixed with
   `[SIM-INTEGRITY]` followed by a whitespace character.
2. **Log level**: `[SIM-INTEGRITY]` messages use `logging.WARNING` (not DEBUG,
   not ERROR). ERROR is reserved for exceptions that prevent the simulation from
   continuing. DEBUG is for diagnostic output. WARNING + `[SIM-INTEGRITY]` is
   the band for anomalies that are observable, continuable, and operator-relevant.
3. **Monitoring grep pattern**: `grep '\[SIM-INTEGRITY\]'` across all log output
   is the canonical pattern for extracting all integrity anomalies from a
   simulation run. Any alert pipeline or CI log check that scans for simulation
   anomalies must use this pattern.
4. **Canonical examples**: Reference the three existing hooks as canonical usage
   examples: dropped delta in `propagation.py`, STOCK attribute conflict in
   `propagation.py`, duplicate `event_id` in `runner.py`.
5. **New anomaly checklist**: Before merging any new module or propagation change,
   the implementing agent must ask: "Is there an error condition here that should
   continue + warn rather than raise? If so, is `[SIM-INTEGRITY]` used?"

---

## Summary

| Gap | Severity | Standard to Amend | Issue |
|---|---|---|---|
| 1 — No canonical unit registry in DATA_STANDARDS.md | Immediate | DATA_STANDARDS.md | #252 (Comment 1) |
| 2 — No field-level data certification standard in DATA_STANDARDS.md | Immediate | DATA_STANDARDS.md | #252 |
| 3 — WGI territorial convention conflict not addressed in DATA_STANDARDS.md | Near-term | DATA_STANDARDS.md | File with WGI source registration |
| 4 — Ecological composite score normalization methodology not a documented data standard | Immediate | DATA_STANDARDS.md | ARCH-REVIEW-005 Blindspot 1-A |
| 5 — No `_UNIMPLEMENTED_FRAMEWORKS` promotion protocol in CODING_STANDARDS.md | Near-term | CODING_STANDARDS.md | File with M8 governance promotion |
| 6 — No `[SIM-INTEGRITY]` monitoring contract documented in CODING_STANDARDS.md | Near-term | CODING_STANDARDS.md | M7 exit hygiene |

Three of six gaps are horizon:immediate — they affect code that will be written in
M8 module completion. Gaps 1 and 2 will multiply with every new M8 indicator added:
each new ecological or governance indicator without a canonical unit and a certified
source field mapping is a new instance of the Gimli Glider failure mode.

Gap 4 (ecological normalization methodology) is the most architecturally consequential:
the M8 obligation to replace percentile rank with planetary boundary normalization
cannot be implemented consistently without a data standard that defines what the
reference values are, how they are registered, and how updates to the scientific
consensus are governed.

Gap 6 (`[SIM-INTEGRITY]`) is the lowest risk of the six — the pattern exists and is
already used in three locations. The gap is documentation only, but it is the
difference between a stable monitoring contract and a convention that erodes
within two milestones.

---

## Engineering Lead Dispositions

**Date:** 2026-05-16
**Disposition for all six gaps:** ACCEPT

### Process

A three-agent independent review panel (Data Architect, QA Lead, Architect)
was convened before dispositions were recorded. Each agent received the six gap
descriptions and three questions (primary concern per gap, highest-risk gap,
ordering dependencies) independently — no draft dispositions were shared with
any agent. Panel output informed all six dispositions.

### Key Panel Findings Incorporated

1. **Gap 1 → Gap 2 ordering is sequential, not parallel.** The canonical unit
   vocabulary must exist before field mappings can be certified against it.
   Implementation order enforced: Gap 1 committed first.

2. **Gaps 2 and 3 are circularly dependent and ship in the same commit with
   joint sign-off.** Gap 2 needs Gap 3's entity resolution before certifying
   WGI field mappings; Gap 3 needs Gap 2's field registry structure for the
   provenance note. Committed together per Architect panel finding.

3. **`simulation_reference_constants` database table adopted** (Data Architect
   recommendation). The fixture-file escape hatch in the original STD-REVIEW-004
   Gap 4 description is closed. Reference constants have a fundamentally different
   access pattern from time-series source data and must live in a dedicated table.

4. **`transformation_test_id` field added to `source_field_registry` schema**
   (QA Lead panel finding). Paper certification without a verification test is not
   sufficient. Every certified field mapping must reference a passing test on a
   known input/output pair from actual source data.

5. **Unit correctness tests added as mandatory requirement** (QA Lead panel finding).
   Tests asserting `variable_type` but not `unit` are incomplete for M8 indicators.
   Every new ecological and governance indicator must assert `qty.unit == canonical_unit`.
   Added to test_ecological_module.py and test_governance_module.py in this commit set.

6. **`is_single_entity` guard scope interaction documented** (QA Lead panel finding).
   Boundary-normalized ecological composite scores are physically meaningful for a
   single entity (CO2 vs. 350 ppm boundary), unlike percentile rank. The ADR-005
   M8 amendment must specify which frameworks are exempt from the guard. TODO
   comment added in `scenarios.py` `_compute_composite_score()` dispatch note.

7. **`_compute_composite_score()` dispatch architecture designed to accommodate both
   ecological and governance normalization paths before either is implemented**
   (Architect panel finding). Dispatch comment documents the strategy pattern
   requirement — governance and ecological must be designed in parallel, not
   ecological first with governance retrofitted. Neither Gap 4 nor Gap 5 implements
   the strategy; both are documented as requiring the strategy design in ADR-005 M8.

8. **runner.py `[SIM-INTEGRITY]` prefix verified and corrected** (Architect panel
   finding confirmed by pre-work code inspection). The duplicate event_id warning at
   runner.py line 315 was missing the `[SIM-INTEGRITY]` prefix. Fixed in Gap 6 commit.
   Pre-work verification required: **prefix was ABSENT**. Code fix applied.

9. **Runtime validation gate at `Quantity` construction time, not compliance-scan-only**
   (QA Lead + Architect panel finding). CODING_STANDARDS.md §Simulation Integrity
   Monitoring §Canonical Unit Registry cross-reference documents this requirement.

10. **CI enforcement test added for Gap 5 promotion protocol** (QA Lead panel finding).
    `test_governance_is_in_unimplemented_frameworks` and companion composite_score test
    added to `test_measurement_output.py`. Promotion is the act of making the companion
    integration test pass — it is not a documentation event.

### Gap-by-Gap Dispositions

| Gap | Severity | Amendment target | Disposition |
|---|---|---|---|
| 1 — Canonical unit registry | Immediate | DATA_STANDARDS.md | ACCEPT — §Canonical Unit Registry added; ecological and governance module unit violations fixed; unit correctness tests added |
| 2 — Field-level data certification | Immediate | DATA_STANDARDS.md | ACCEPT — §Field-Level Data Certification added with transformation_test_id (QA Lead addition); committed with Gap 3 |
| 3 — WGI territorial convention | Near-term | DATA_STANDARDS.md | ACCEPT — §Source-Convention Conflict Resolution added; WGI Taiwan provenance note verbatim specified; governance source registration requirement added; committed with Gap 2 |
| 4 — Ecological composite normalization | Immediate | DATA_STANDARDS.md | ACCEPT — §Simulation Reference Constants added; dedicated table adopted; two Alembic migrations; normalization formula documented; dispatch design comment in scenarios.py |
| 5 — `_UNIMPLEMENTED_FRAMEWORKS` promotion protocol | Near-term | CODING_STANDARDS.md | ACCEPT — §Framework Promotion Protocol added; CI enforcement tests added (QA Lead addition) |
| 6 — `[SIM-INTEGRITY]` monitoring contract | Near-term | CODING_STANDARDS.md | ACCEPT — §Simulation Integrity Monitoring added; runner.py code fix applied |

### EL Decision: Gap 2 vs. Gap 3 Ordering Conflict

Data Architect recommended Gap 2 (certification infrastructure) before Gap 3.
Architect recommended Gap 3 (territorial resolution) before Gap 2 for WGI.

**Resolution:** The circular dependency is real — both agents were correct.
The resolution is to commit Gaps 2 and 3 together in the same transaction,
as they cannot be cleanly sequenced. Both amendments reference each other.
Neither is complete without the other. This is the correct disposition for a
genuine circular dependency — not a sequencing choice between them.

### EL Decision: Highest-Risk Gap

Data Architect: Gap 2 (certification infrastructure — the foundational layer
that everything else depends on). QA Lead + Architect: Gap 4 (ecological
normalization — ADR-005 Amendment B deferred obligation, misleading mandatory note).

**Resolution:** Both risk frames are valid. M8 implementation priority treats
Gap 4 as the most architecturally consequential (the ADR-005 Amendment B note
becomes permanently misleading if M8 ships without it), while Gaps 1 and 2 are
addressed first because they are prerequisites for Gap 4's certification chain.
Implementation order: Gap 1 → Gap 4 → Gaps 2+3 → Gap 6 → Gap 5.

### Single-Principal Governance Limitation

*"This exception was approved by the same individual who holds full repository
authority. No independent review is available at this governance stage. See
CLAUDE.md §Governance for the documented plan to address this limitation."*

The three-agent independent panel (Data Architect, QA Lead, Architect Agent) is
the compensating control for this limitation on this specific decision. Agents
were given the gap inventory without draft dispositions and produced independent
assessments. Where all three agents agreed (Gap 1 → Gap 2 ordering, is_single_entity
guard scope, runtime validation gate), confidence is higher. Where they disagreed
(Gap 2 vs. Gap 3 ordering, highest-risk gap ranking), the Engineering Lead
exercised judgment as documented above.
