# STD-REVIEW-002: Standards and Policy Review — Milestone 3

**Review type:** Full — all Domain Intelligence Council members (Track 1) and
all technical agents (Track 2), with cross-track reconciliation
**Scope:** `docs/CODING_STANDARDS.md`, `docs/DATA_STANDARDS.md`,
`docs/POLICY.md`, `docs/CONTRIBUTING.md`, Domain Intelligence Council section
of `CLAUDE.md`
**Seeded with:**
- ARCH-REVIEW-002 known-gap #87 (human cost fidelity thresholds for backtesting absent from standards — Chief Methodologist, Development Economist)
- ARCH-REVIEW-002 known-gap #91 (model confidence field distinct from data quality tier absent from standards — Chief Methodologist)
- Issue #107 implementation experience: `ia1_disclosure TEXT NOT NULL` enforcement, `ScenarioConfigSchema.initial_attributes: dict[str, dict[str, QuantitySchema]]` pattern, scenario status lifecycle (pending/running/completed/failed)
- STD-REVIEW-002 sequencing constraint recorded on Issue #61: this review runs after #107 PR merges, before Issue #111 (WebScenarioRunner) begins, and must complete before Issue #112 (backtesting) begins
**Date:** 2026-04-23
**Status:** Phase 3 Complete — findings compiled, Issues pending Engineering Lead disposition of CONFLICT findings
**PR:** docs(standards): STD-REVIEW-002 standards and policy review — Milestone 3 scenario engine

---

## Executive Summary

The Issue #107 implementation provides the most important concrete grounding for
this review: `ia1_disclosure TEXT NOT NULL` with no server default is a correct
enforcement mechanism, but `DATA_STANDARDS.md` contains no definition of the IA-1
text itself. Three different implementations — the Issue #107 DB constraint, the
Issue #112 backtesting `ia1_disclosure` field, and the Module forward-projection
metadata note in `CODING_STANDARDS.md` — will produce three different phrasings
of the same disclosure unless a canonical text is standardized.

The two known-gap findings from ARCH-REVIEW-002 are confirmed by this review.
Issue #87 (human cost fidelity thresholds) and Issue #91 (model confidence vs.
data quality tier) each identify a genuine gap that the current standards do not
address and that the backtesting implementation in Issue #112 will need to resolve
without guidance.

**Most significant Track 1 finding:** `DATA_STANDARDS.md` has no backtesting
fidelity threshold standard. The entire Greece 2010–2012 backtesting case
(Issue #112) rests on `DIRECTION_ONLY` thresholds that are defined in ADR-004 but
not in the standards documents. Future backtesting cases — Thailand 1997, Lebanon
2019, Argentina 2001 — will need a standards-level definition of what "passing
backtesting" means at each threshold type. Every case added without a standard
encodes a different implicit definition.

**Most significant Track 2 finding:** The `ScenarioConfigSchema.initial_attributes`
pattern introduced in Issue #107 stores `dict[str, dict[str, QuantitySchema]]` in
JSONB. This is not inconsistent with existing standards, but it introduces an
implicit contract — that the inner `dict[str, QuantitySchema]` uses the same JSONB
envelope format as `simulation_entities.attributes` — that is documented nowhere in
`DATA_STANDARDS.md`. If a future implementation uses a different envelope format for
`initial_attributes` than for entity attributes, scenario replay will silently corrupt
initial state values.

**Three CONVERGENT finding pairs** identified: the IA-1 canonical text standard
(T1-F1 × T2-F1), the backtesting fidelity threshold type registry (T1-F8 × T2-F3),
and the model confidence / data quality tier distinction (T1-F2 × T2-F5).

**One CONFLICT finding:** The scenario DELETE endpoint permanently destroys audit
trail data (scheduled inputs, state snapshots). The Security Agent requires
`CODING_STANDARDS.md` to mandate audit trail preservation before cascaded delete.
The QA Agent requires testable lifecycle transitions that include a DELETED status.
The Architect Agent finds that a DELETED status contradicts the ADR-004 cascade
delete design decision. This is flagged for Engineering Lead disposition.

**ADR license impact:** No renewal triggers fire against ADR-001, ADR-002, or
ADR-003. ADR-004 Decision 1 is not under review. Standard amendments in this
review are additive — they define rules for domains not previously addressed.
No existing compliant implementation becomes non-compliant.

---

## Track 1 Findings — Domain Intelligence Council

---

### Development Economist Agent — CHALLENGE

**T1-F1: `DATA_STANDARDS.md` has no canonical definition of the IA-1 Known Limitation text.**

`CODING_STANDARDS.md §confidence_tier Propagation` contains an informal statement
of the IA-1 limitation: *"Confidence tier does not account for projection horizon."*
`DATA_STANDARDS.md §Units and Measurements` contains a longer version with an
implementation note. Issue #107 introduces a third instantiation: the `ia1_disclosure`
column accepting any text the application provides.

From a human development standpoint, this matters because the IA-1 limitation is
most consequential for long-horizon projections that affect capability accumulation
across generations. A disclosure text that is vague, inconsistently worded, or
absent from a particular output point fails the people who most depend on the tool
being honest about its limitations.

**Gap:** `DATA_STANDARDS.md` must define the canonical IA-1 text — the exact phrase
that must appear verbatim in all `ia1_disclosure` fields, module output metadata,
and any output display that carries a forward-projected Quantity. One canonical text,
defined in one place. Referenced everywhere else.

---

**T1-F2: `DATA_STANDARDS.md` has no standard distinguishing model confidence from data quality tier.**

ARCH-REVIEW-002 finding #91 confirmed: `confidence_tier` (1–5) measures the quality
of the input *data*. It does not measure whether the *model* correctly represents the
relationship between variables. A scenario run with all Tier 1 data and a miscalibrated
fiscal multiplier will produce Tier 1 confidence outputs from a structurally wrong model.

From a human development perspective, this matters because the human cost ledger outputs
are derived from model-mediated relationships, not just from data. A Tier 1-confidence
output that says "poverty headcount increases by 2 million" may rest on a fiscal-to-welfare
transmission function that has never been validated against historical data. The Tier 1
label overstates confidence in the causal claim.

**Gap:** `DATA_STANDARDS.md` must add a `model_confidence` field to backtesting output
records, separate from `confidence_tier`. `model_confidence` reflects whether the
model relationship producing this output has been validated against historical data —
DIRECTION_ONLY, MAGNITUDE, CALIBRATED, or UNVALIDATED. This is not a data quality
question; it is a model validity question.

---

**T1-F3: `DATA_STANDARDS.md` has no human development indicator source standard.**

Confirmed from STD-REVIEW-001. The gap remains open. HDI components, child stunting,
maternal mortality, health system capacity — no DATA_STANDARDS.md entry. This gap
becomes concrete in Issue #87: the Greece 2010–2012 backtesting case could in
principle include human development fidelity thresholds (unemployment direction,
health spending direction), but DATA_STANDARDS.md provides no guidance on which
source to use, what methodology version to cite, or what vintage dating rule applies.

**Gap:** `DATA_STANDARDS.md` must add a Human Development Data Sources section
specifying: approved Tier 1 sources for unemployment (ILO ILOSTAT, World Bank WDI),
health spending (WHO Global Health Expenditure Database, World Bank WDI), education
(UNESCO UIS), poverty (World Bank PovcalNet). Methodology versioning and vintage
dating requirements follow the same rules as economic data.

---

### Political Economist Agent — CHALLENGE

**T1-F4: `CODING_STANDARDS.md` has no standard for scenario lifecycle state machine validity.**

Issue #107 defines scenario status as: pending → running → completed | failed.
This is a valid lifecycle, but it is defined only in the database CHECK constraint
and the ADR. `CODING_STANDARDS.md` has no standard for:
- Which transitions are valid (pending → failed is permitted by the constraint; should it be?)
- Whether transitions are reversible (can a failed scenario be reset to pending?)
- Whether the lifecycle is enforced at the application layer or only at the DB layer
- What events trigger each transition

A political economist's concern: scenario lifecycle integrity matters for reproducibility.
A scenario that transitions to running and then back to pending has had its configuration
potentially altered mid-execution. The audit trail does not show which configuration
version was actually run. This is a governance failure, not just a technical one.

**Gap:** `CODING_STANDARDS.md` must add a Simulation Lifecycle State Machine standard
defining: the valid status values, the permitted transitions, the events that trigger
each transition, and the immutability rule (configuration is frozen on transition from
pending to running — subsequent patches are rejected at the application layer).

---

### Ecological Economist Agent — CHALLENGE

**T1-F5: `DATA_STANDARDS.md` has no standard for ecological indicator representation.**

Confirmed from STD-REVIEW-001 as an open gap. The Ecological Economist notes that
the Greece 2010–2012 backtesting case, while primarily financial, had documented
ecological consequences (cuts to environmental enforcement budgets, delayed waste
management infrastructure). Backtesting fidelity thresholds that test only financial
and unemployment indicators will systematically miss model errors in ecological
transmission paths.

**Gap (horizon: near-term):** `DATA_STANDARDS.md` should add a minimum specification
for ecological data sources and variable types. This gap is not blocking Issue #112
(which uses only GDP and unemployment thresholds) but becomes blocking at Issue #44
scope (where MAGNITUDE thresholds are introduced and ecological variables may need
to be included).

---

### Geopolitical and Security Analyst Agent — CHALLENGE

**T1-F6: `POLICY.md` has no position on scenario data retention and deletion.**

Issue #107 introduces `DELETE /scenarios/{scenario_id}` with CASCADE to all
scheduled inputs and snapshots. `POLICY.md` covers territorial positions, data
source selection philosophy, and dual-use position. It has no position on:
- How long scenario data is retained before deletion is permitted
- Whether scenarios used in external briefings may be deleted
- Whether deletion is audited

From a geopolitical standpoint: a scenario that was used to brief a finance ministry
and then deleted creates an integrity gap. The briefing exists; the underlying
analysis does not. This is a gap that matters for the tool's credibility.

**Gap (horizon: near-term):** `POLICY.md` should add a scenario data retention
position: scenarios may not be deleted for a minimum period (suggest 30 days) after
last access, and deletion must be audited.

---

### Intergenerational Equity Advocate Agent — CHALLENGE

**T1-F7: `CODING_STANDARDS.md` backtesting requirements have no intergenerational
indicator coverage requirement.**

`CODING_STANDARDS.md §Backtesting Tests` requires: data source cited, fidelity
threshold specified, failure mode documented, vintage dating verified. It does not
require that any backtesting case include a threshold on an intergenerational
indicator — education spending direction, child health outcomes direction, public
investment direction.

The Greece 2010–2012 case is precisely the type of case where intergenerational
consequences were severe and measurable: education spending collapsed, youth
unemployment reached 58%, a generation's human capital formation was interrupted.
A backtesting case that tests only GDP and debt-to-GDP and claims to validate a
Greek austerity scenario is testing the wrong variables for the project's primary
mission.

**Gap:** `CODING_STANDARDS.md §Backtesting Tests` should add: *"Every backtesting
case must include at least one fidelity threshold on a human cost indicator —
unemployment direction, health spending direction, or education spending direction.
DIRECTION_ONLY is sufficient; MAGNITUDE thresholds for human cost indicators are
gated on Issue #44."*

---

### Community and Cultural Resilience Agent — CHALLENGE

**T1-F8: `DATA_STANDARDS.md` has no definition of DIRECTION_ONLY vs. MAGNITUDE threshold types.**

Backtesting thresholds are currently defined in ADR-004 Decision 3 but not in
`DATA_STANDARDS.md`. The Community Resilience Agent notes that this matters
because the distinction between "the model predicted the direction correctly" and
"the model predicted the magnitude correctly" is not a technical distinction — it is
a claim about what the simulation has actually validated.

From a community resilience standpoint: a scenario that confidently predicts the
direction of unemployment change during an IMF program but has no magnitude validation
is making a much weaker claim than its outputs may appear to make. Users who are not
specialists will not distinguish between a directional prediction and a magnitude
prediction unless the standard requires that the distinction be made explicit in output.

**Gap:** `DATA_STANDARDS.md` should add a Backtesting Fidelity Threshold Registry
section defining:
- `DIRECTION_ONLY`: the model predicts the correct sign of change (increase or
  decrease). This is a plausibility check, not a validation of magnitude or
  mechanism. False positive rate at two independent thresholds: 25%.
- `MAGNITUDE(±N units)`: the model predicts a value within ±N of the historical
  actual. Requires parameter calibration (Issue #44).
- `CALIBRATED`: the threshold is parameterized from documented historical estimation;
  the calibration source and methodology are cited.
- `UNVALIDATED`: no historical data has been used to set this threshold; the
  threshold is an engineering judgment.

This registry must appear in `ia1_disclosure` text for any backtesting run that uses
DIRECTION_ONLY thresholds.

---

### Investment and Capital Formation Agent — CHALLENGE (RISK-AVERSE mode)

**T1-F9: `CODING_STANDARDS.md` has no standard for JSONB envelope format consistency across scenarios and live entities.**

Issue #107 stores `initial_attributes` in `scenario.configuration JSONB` as
`dict[str, dict[str, QuantitySchema]]`. The `simulation_entities.attributes` JSONB
uses the same Quantity envelope format. But the standards documents do not define
this envelope format as a cross-cutting standard — it exists only in implementation
code and the ADR-003 narrative.

From a capital formation / investment reliability standpoint: if a future
implementation writes `initial_attributes` in a different format (e.g., using `amount`
instead of `value` — a field renamed in SCR-001), scenario replay will silently
corrupt initial state without a schema validation error. The standard must define
the canonical JSONB Quantity envelope format so that both `simulation_entities.attributes`
and `scenario.configuration.initial_attributes` are tested against the same contract.

**Gap:** `DATA_STANDARDS.md` must define the Quantity JSONB Envelope Format as a
formal standard: `{"value": "<str(Decimal)>", "unit": "<str>", "variable_type":
"<str>", "confidence_tier": <int 1-5>, "observation_date": "<ISO-date or null>",
"source_registry_id": "<str or null>", "measurement_framework": "<str or null>"}`.
This format must be referenced in all JSONB Quantity storage contexts.

---

### Social Dynamics and Behavioral Economics Agent — CHALLENGE

**T1-F10: `POLICY.md` has no position on simulation output use in active negotiations.**

The governance scenario (Issue #107 → WebScenarioRunner → scenario output) is
explicitly designed for use by finance ministers in IMF negotiations (the primary
use case in CLAUDE.md). `POLICY.md` does not address:
- What disclosures must accompany simulation output used in live negotiations
- Whether the tool's outputs may be represented as predictions vs. scenario analyses
- What labeling is required on scenario output that is shared with counterparties

From a social dynamics perspective: outputs used in high-stakes negotiations have
social legitimacy effects. A scenario output presented with excessive confidence
can anchor negotiations in ways that close off viable alternatives. The tool's
`DIRECTION_ONLY` backtesting status must be visible in any negotiating use context.

**Gap (horizon: near-term):** `POLICY.md` should add a section on Output Use in
Live Decision Contexts specifying: required labeling (scenario analysis, not
prediction; confidence basis stated; DIRECTION_ONLY status disclosed where
applicable).

---

### Chief Methodologist Agent — CHALLENGE

**T1-F11: `DATA_STANDARDS.md` has no standard for the 25% false-positive rate disclosure.**

ARCH-REVIEW-002 #86 documented: at 2 independent DIRECTION_ONLY thresholds, a null
model has 25% probability of passing both by chance. This is a methodological fact
that must be disclosed in any output from a DIRECTION_ONLY backtesting run. It is
currently not in any standard — only in the ARCH-REVIEW-002 document itself.

**Gap:** `DATA_STANDARDS.md §Backtesting Fidelity Threshold Registry` (T1-F8) must
include: *"DIRECTION_ONLY threshold suites with fewer than four independent indicators
have false positive rates above 6.25% against a null model. Suites with two indicators
have a 25% false positive rate. This limitation must appear verbatim in `ia1_disclosure`
for any run using fewer than four DIRECTION_ONLY thresholds."*

**T1-F12: `CODING_STANDARDS.md` has no requirement that scenario replay is tested.**

`CODING_STANDARDS.md §Backtesting Tests` requires that backtesting cases pass fidelity
thresholds. It does not require that the scenario replay mechanism itself is tested —
i.e., that running a scenario twice from the same configuration produces identical outputs.

Determinism is a correctness property that is not enforced by any current standard.
A simulation that is non-deterministic will produce different outputs from the same
scenario configuration, making backtesting comparisons meaningless.

**Gap:** `CODING_STANDARDS.md §Testing Requirements` must add: *"Determinism test
required: every scenario implementation must include a test that runs the same
scenario configuration twice and asserts that all output attributes are identical
across runs. Floating point non-determinism from module ordering is a build failure."*

---

## Track 2 Findings — Technical Agents

---

### QA Agent — CHALLENGE

**T2-F1: The `ia1_disclosure` enforcement mechanism — is the DB constraint sufficient?**

Issue #107 enforces `ia1_disclosure TEXT NOT NULL` at the database layer. This prevents
omission but does not prevent a meaningless string ("x", "n/a", "") from being stored.
The standard should distinguish between:
- **Structural enforcement** (NOT NULL constraint, DB layer): prevents empty `ia1_disclosure`
- **Content enforcement** (application layer test): verifies the text contains the
  canonical IA-1 phrase

QA recommendation: add a unit test to Issue #112 that verifies the stored
`ia1_disclosure` text contains the canonical IA-1 phrase (a substring check against
the canonical text defined by T1-F1's proposed standard). This is testable and adds
the content layer that the DB constraint cannot provide.

**Proposed test:**
```python
def test_ia1_disclosure_contains_canonical_phrase() -> None:
    """Backtesting run ia1_disclosure must contain the canonical IA-1 text."""
    record = run_greece_backtesting_fixture()
    assert IA1_CANONICAL_PHRASE in record.ia1_disclosure
```

Where `IA1_CANONICAL_PHRASE` is a module-level constant imported from a canonical
location defined by T1-F1's proposed standard.

---

**T2-F2: Scenario lifecycle transitions — testable?**

T1-F4 (Political Economist) proposes a state machine standard for scenario status.
QA assessment: the proposed transitions are testable *if* the standard defines them
precisely. Proposed tests:

```python
def test_scenario_create_starts_as_pending() -> None: ...
def test_scenario_run_transitions_to_running() -> None: ...
def test_scenario_complete_transitions_to_completed() -> None: ...
def test_scenario_patch_rejected_when_running() -> None:
    """Configuration must be immutable once status is running."""
    ...
def test_scenario_failed_status_set_on_exception() -> None: ...
```

The `pending → failed` transition (T1-F4's concern) is testable: what does the
application do if `POST /scenarios/{id}/run` is called on a scenario with invalid
entity IDs that were not caught at creation? Status should transition to failed, not
leave the scenario in an ambiguous state.

**QA finding:** `CODING_STANDARDS.md` must specify the `pending → failed` path
explicitly. Without it, implementations will diverge: some will leave the scenario
in `pending` on pre-execution validation failure; others will transition to `failed`.

---

**T2-F3: DIRECTION_ONLY threshold — is the standard testable?**

T1-F8 proposes a Backtesting Fidelity Threshold Registry in `DATA_STANDARDS.md`.
QA assessment: the proposed registry is testable only if the threshold types are
defined operationally.

Proposed test contract for DIRECTION_ONLY:
```python
def evaluate_direction_only_threshold(
    attribute: str,
    simulated_values: list[Decimal],
    actual_values: list[Decimal],
) -> bool:
    """Returns True if simulated and actual have matching direction across all steps.

    DIRECTION_ONLY does not test magnitude. A value of -0.0001 and -8.9
    are both 'negative' and both pass equally.
    """
    return all(
        (s < 0) == (a < 0) for s, a in zip(simulated_values, actual_values)
    )
```

QA finding: the function above and its signature should be added to
`CODING_STANDARDS.md` as the canonical DIRECTION_ONLY evaluator — all backtesting
cases use this function, not ad hoc comparisons. This ensures all DIRECTION_ONLY
tests are consistent and the false-positive rate analysis from T1-F11 applies
uniformly.

---

**T2-F4: `ScenarioCreateRequest` validation — testable as written?**

Review of `backend/app/api/scenarios.py` validation in `_validate_create_request()`:
- Empty name: testable ✓ (T1-F4 status machine test above covers this)
- n_steps 1–100: testable ✓ (boundary tests in `test_scenario_schemas.py` confirm)
- Step index bounds: testable ✓ (integration test `test_create_scenario_out_of_range_step_returns_422` confirms)
- Entity existence: testable ✓ (`test_create_scenario_missing_entity_returns_422` confirms)

QA finding: **no gap** — the Issue #107 validation is already testable and tested.
The unit test boundary coverage for n_steps (0, 1, 100, 101) correctly documents
that schema-level validation accepts all values but endpoint-level validation
enforces 1–100. This separation of concerns is correct.

---

**T2-F5: `model_confidence` — is T1-F2 testable?**

T1-F2 proposes a `model_confidence` field on backtesting output records. QA assessment:
testable if the field is defined as an enum.

Proposed definition:
```python
class ModelConfidence(str, Enum):
    UNVALIDATED = "UNVALIDATED"     # no historical data used
    DIRECTION_ONLY = "DIRECTION_ONLY"  # direction of change validated
    MAGNITUDE = "MAGNITUDE"         # magnitude validated within ±N
    CALIBRATED = "CALIBRATED"       # parameters calibrated from historical data
```

This enum must appear in `DATA_STANDARDS.md` as part of the T1-F2 standard.
Greece 2010–2012 initial run ships with `DIRECTION_ONLY`. The field is testable:
```python
def test_greece_backtesting_model_confidence_is_direction_only() -> None:
    assert record.model_confidence == ModelConfidence.DIRECTION_ONLY
```

---

### Architect Agent — CHALLENGE

**T2-F6: JSONB envelope inconsistency risk from `initial_attributes` pattern.**

The Issue #107 `ScenarioConfigSchema.initial_attributes: dict[str, dict[str, QuantitySchema]]`
pattern introduces a JSONB storage context where the inner dict is a Quantity envelope.
The Architect observes three risks:

1. **Envelope format divergence**: `QuantitySchema.from_jsonb()` normalizes legacy
   field names (e.g., converts `float` values to `str(Decimal(str(v)))`). If a future
   implementation writes `initial_attributes` directly without going through
   `QuantitySchema.from_jsonb()`, it may store raw numeric values that the round-trip
   through `from_jsonb()` would have normalized.

2. **Field rename hazard**: SCR-001 renamed `MonetaryValue.amount` to `MonetaryValue.value`.
   The `JSONB` format has no schema migration — a stored envelope from before SCR-001
   would fail `from_jsonb()` silently (the key is absent, a default is used).

3. **Versioning gap**: `simulation_entities.attributes` has no envelope version field.
   If the Quantity envelope format changes again, existing stored data cannot be
   distinguished from new-format data without inspecting content heuristically.

**Architect recommendation:** `DATA_STANDARDS.md` must define the canonical Quantity
JSONB Envelope Format (T1-F9) and must include an `_envelope_version` field with
the current value `"1"`. All JSONB reads must check for `_envelope_version` and
apply appropriate migration logic. This is a non-breaking addition — envelopes
without `_envelope_version` are treated as version 1.

---

**T2-F7: WebScenarioRunner (Issue #111) requires a standards entry before implementation begins.**

ADR-004 Decision 2 defines `WebScenarioRunner` wrapping `ScenarioRunner`. The
`ScenarioRunner` produces deterministic in-memory output. The `WebScenarioRunner`
writes snapshots to the database after each step. The round-trip is:

`SimulationState (Python objects) → JSONB → SimulationState (Python objects)`

There is no standard governing this round-trip. Specifically:
- `Quantity.observation_date` is stored as an ISO 8601 string in JSONB; `QuantitySchema.from_jsonb()` parses it. But `SimulationState` uses `Quantity` (with `date` type), not `QuantitySchema` (with `str` type). The de-serialization path from snapshot JSONB back to `Quantity` is not defined.
- If any `Quantity` field is `None` in the DB snapshot and the snapshot is used as the initial state for a subsequent step, the `None` propagates into arithmetic and produces a silent error.

**Architect recommendation:** Before Issue #111 implementation begins (per the
sequencing constraint on Issue #61), `CODING_STANDARDS.md` must add a
Snapshot Serialization Standard: *"Every Quantity stored as JSONB in a snapshot
must round-trip through `QuantitySchema.from_jsonb()` without data loss. The
Implementation Agent for Issue #111 must include a round-trip test:
`Quantity → JSONB → QuantitySchema → Quantity` for each field, confirming that
all values are preserved exactly (Decimal precision, date type, enum values)."*

---

**T2-F8: ADR-004 diagram requirement not yet satisfied.**

`CODING_STANDARDS.md §Diagram Standards` requires: *"Every ADR gets at least one
diagram."* ADR-004 has five decisions. The ADR-004 document references a Mermaid
diagram in `docs/architecture/ADR-004-scenario-engine.mmd` — but this file does
not exist in the repository (confirmed by review). The Issue #107 PR should have
included this diagram but did not.

**Architect finding:** This is a standards compliance gap from Issue #107.
A diagram must be added before Issue #114 (the Issue #107 PR) merges.

---

### Security and Review Agent — CHALLENGE

**T2-F9: `DELETE /scenarios/{id}` CASCADE destroys audit trail — standards gap.**

Issue #107's `DELETE /scenarios/{scenario_id}` endpoint cascades to:
- `scenario_scheduled_inputs` — the complete input sequence that defines the scenario
- `scenario_state_snapshots` — every simulation output, including `ia1_disclosure` records

The `CODING_STANDARDS.md §Agent Team Workflow Standards` and `POLICY.md` have no
data retention standard for scenario data. The Security Agent finds:

1. **Audit trail destruction**: `control_input_audit_log` records are not cascaded
   (they reference `scenario_id` as a plain text field, not an FK). But `scenario_scheduled_inputs`
   is cascaded — the audit trail of what inputs were configured for a scenario is destroyed.

2. **No authorization standard**: `DELETE /scenarios` has no authorization check.
   Any caller with API access can destroy any scenario, including scenarios that
   were used in external briefings or analyses. There is no standard requiring
   authorization for destructive operations.

3. **Orphaned audit log records**: After scenario deletion, `control_input_audit_log`
   records with the deleted `scenario_id` become orphaned — they reference a scenario
   that no longer exists. This corrupts the audit trail integrity.

**Security finding:** `CODING_STANDARDS.md` must add: *"Endpoints that destroy
persistent records must not cascade to audit trail data. `scenario_scheduled_inputs`
records must be retained for a minimum of 30 days after scenario deletion (soft
delete pattern). The hard delete endpoint must be documented as requiring operator-level
authorization, not user-level authorization."*

This is flagged as a **CONFLICT** against T2-F2's testable lifecycle requirement —
see Cross-Track Reconciliation.

---

**T2-F10: Scenario configuration stores entity IDs without validation at JSONB level.**

The `scenario.configuration JSONB` column stores `entities: list[str]` validated at
the API layer but not at the DB layer. If a scenario is created through the API (entity
IDs validated) and then a migration or admin operation modifies the configuration JSONB
directly, entity IDs that no longer exist in `simulation_entities` will not be caught
until execution time.

**Security finding:** This is a minor gap — direct DB manipulation bypasses all
application-layer controls. No standard can fully prevent it. However, `CODING_STANDARDS.md`
should add: *"JSONB configuration columns that contain entity references must not be
modified directly via SQL outside of the application layer. Migrations that modify JSONB
content must include a validation step confirming all entity references resolve."*

---

## Phase 3 — Cross-Track Reconciliation

QA Agent and Architect Agent reviewed all Track 1 findings.
Development Economist, Chief Methodologist, and Intergenerational Advocate reviewed
all Track 2 findings.

---

### Reconciliation Table

| Finding ID | Description | Status | Unified Amendment |
|---|---|---|---|
| T1-F1 | Canonical IA-1 text definition missing from DATA_STANDARDS.md | **CONVERGENT** with T2-F1 | SA-01: Add canonical IA-1 text constant to DATA_STANDARDS.md; unit test checks substring |
| T1-F2 | model_confidence field absent from standards | **CONVERGENT** with T2-F5 | SA-02: Add ModelConfidence enum to DATA_STANDARDS.md §Backtesting |
| T1-F3 | Human development indicator sources absent | **COMPATIBLE** | SA-03: Add Human Development Data Sources section to DATA_STANDARDS.md |
| T1-F4 | Scenario lifecycle state machine not in CODING_STANDARDS.md | **CONVERGENT** with T2-F2 | SA-04: Add Simulation Lifecycle State Machine standard to CODING_STANDARDS.md |
| T1-F5 | Ecological indicator representation absent | **COMPATIBLE** (horizon: near-term) | SA-05: Add Ecological Data Sources skeleton to DATA_STANDARDS.md — minimal, non-blocking |
| T1-F6 | POLICY.md has no scenario data retention position | **COMPATIBLE** | SA-06: Add Scenario Data Retention section to POLICY.md |
| T1-F7 | No intergenerational indicator threshold requirement in backtesting | **COMPATIBLE** | SA-07: Add human cost indicator threshold requirement to CODING_STANDARDS.md §Backtesting |
| T1-F8 | No DIRECTION_ONLY/MAGNITUDE threshold type registry | **CONVERGENT** with T2-F3 | SA-08: Add Backtesting Fidelity Threshold Registry to DATA_STANDARDS.md |
| T1-F9 | JSONB Quantity envelope format not formalized | **CONVERGENT** with T2-F6 | SA-09: Add Quantity JSONB Envelope Format standard to DATA_STANDARDS.md with `_envelope_version` |
| T1-F10 | POLICY.md missing output-use-in-negotiations position | **COMPATIBLE** (horizon: near-term) | SA-10: Add Output Use in Live Decision Contexts to POLICY.md |
| T1-F11 | 25% false-positive rate not in standards | **CONVERGENT** with T2-F3 (SA-08) | SA-08 extended: include false-positive rate table in threshold registry |
| T1-F12 | Determinism test not required | **COMPATIBLE** | SA-11: Add determinism test requirement to CODING_STANDARDS.md §Testing |
| T2-F4 | ScenarioCreateRequest validation — testable as written | **COMPATIBLE** — no gap | No amendment required — Issue #107 implementation is correct |
| T2-F7 | WebScenarioRunner snapshot serialization standard missing | **COMPATIBLE** | SA-12: Add Snapshot Serialization Standard to CODING_STANDARDS.md; required before Issue #111 |
| T2-F8 | ADR-004 diagram missing | **COMPATIBLE** | Not a standards amendment — a compliance gap; must be resolved in PR #114 |
| T2-F9 | DELETE CASCADE destroys audit trail | **CONFLICT** with T2-F2 | See CONFLICT C-1 below |
| T2-F10 | JSONB entity references not validated at DB layer | **COMPATIBLE** | SA-13: Add JSONB migration validation note to CODING_STANDARDS.md |

---

### CONFLICT C-1: Audit Trail vs. Lifecycle Testability

**Finding pair:** T2-F9 (Security Agent: DELETE must not cascade to audit trail data)
vs. T2-F2 (QA Agent: status lifecycle must include a testable DELETED transition)
vs. T2-F6 (Architect Agent: snapshot round-trip must be testable at all states
including post-delete)

**The conflict:**

The Security Agent requires that `scenario_scheduled_inputs` be soft-deleted (retained
for 30 days) and not cascaded on scenario deletion. This requires adding `deleted_at`
to the scenarios table and changing DELETE to a PATCH that sets `deleted_at`.

The QA Agent requires testable lifecycle transitions that include a `deleted` state.
The QA Agent's proposed tests (`test_scenario_patch_rejected_when_running`) assume
a fixed set of valid statuses; adding `deleted` changes the test contract.

The Architect Agent notes that ADR-004 Decision 1 explicitly chose CASCADE DELETE
as the design — a soft delete pattern requires an ADR amendment to Decision 1,
not just a standards change.

**Why this is a genuine conflict:** The Security Agent is proposing a change that
requires an ADR amendment (not just a standards amendment). The QA Agent's position
is compatible with either hard or soft delete provided the lifecycle is defined
precisely. The Architect Agent's position is that this is ADR scope, not standards
scope. The three positions are not reconcilable at the standards level.

**Engineering Lead disposition required:** Accept Option A (soft delete — requires
ADR-004 Decision 1 amendment, adds DELETED status, changes DELETE endpoint to PATCH),
Option B (hard delete preserved — add an explicit POLICY.md position that audit trail
data in `control_input_audit_log` is the authoritative record, not `scenario_scheduled_inputs`),
or propose Option C.

**CONFLICT C-1 is not converted to a GitHub Issue until Engineering Lead disposition.**

---

## Summary: Immediate Amendments (CONVERGENT and COMPATIBLE — non-CONFLICT)

| SA ID | Amendment | Standards Document | Priority |
|---|---|---|---|
| SA-01 | Add canonical IA-1 Known Limitation text constant | DATA_STANDARDS.md | **Immediate — blocks Issue #112** |
| SA-02 | Add ModelConfidence enum | DATA_STANDARDS.md | **Immediate — blocks Issue #112** |
| SA-03 | Add Human Development Data Sources section | DATA_STANDARDS.md | Immediate (I-87) |
| SA-04 | Add Simulation Lifecycle State Machine standard | CODING_STANDARDS.md | **Immediate — blocks Issue #111** |
| SA-05 | Add Ecological Data Sources skeleton | DATA_STANDARDS.md | Near-term |
| SA-06 | Add Scenario Data Retention section | POLICY.md | Near-term |
| SA-07 | Add human cost indicator threshold requirement to backtesting | CODING_STANDARDS.md | Immediate (I-87) |
| SA-08 | Add Backtesting Fidelity Threshold Registry (incl. false-positive table) | DATA_STANDARDS.md | **Immediate — blocks Issue #112** |
| SA-09 | Add Quantity JSONB Envelope Format standard with `_envelope_version` | DATA_STANDARDS.md | **Immediate — blocks Issue #111** |
| SA-10 | Add Output Use in Live Decision Contexts | POLICY.md | Near-term |
| SA-11 | Add determinism test requirement | CODING_STANDARDS.md | Immediate |
| SA-12 | Add Snapshot Serialization Standard (round-trip test) | CODING_STANDARDS.md | **Immediate — blocks Issue #111** |
| SA-13 | Add JSONB migration validation note | CODING_STANDARDS.md | Near-term |

---

## ADR License Status Assessment

**ADR-001** — No renewal triggers fire. The Quantity type system is unchanged. The
`dict[str, Quantity]` attribute store standard is unchanged. SA-09 formalizes the
JSONB envelope format but does not change ADR-001's type system decisions.
**License status: CURRENT confirmed.**

**ADR-002** — No renewal triggers fire. `ControlInput` taxonomy, audit trail schema,
and `MeasurementFramework` tagging requirements are unchanged. SA-04 (lifecycle state
machine) applies to scenario records, not to `ControlInput` records.
**License status: CURRENT confirmed.**

**ADR-003** — No renewal triggers fire. PostGIS schema, FastAPI patterns, and TypeScript
float prohibition are unchanged.
**License status: CURRENT confirmed.**

**ADR-004** — No renewal triggers fire for the non-CONFLICT findings. CONFLICT C-1
(soft delete vs. CASCADE DELETE) affects ADR-004 Decision 1 if Option A is chosen by
the Engineering Lead. Until Engineering Lead disposition: **License status: CURRENT,
with CONFLICT C-1 pending.**

---

## Phase 4 — Engineering Lead Synthesis (Pending)

The Engineering Lead must:

1. Dispose CONFLICT C-1 (Options A, B, or C above).
2. Approve the thirteen SA amendments for implementation.
3. Confirm ADR license statuses above.
4. Create GitHub Issues for all COMPATIBLE and CONVERGENT immediate findings.
5. Note that SA-01, SA-02, SA-08, SA-09, SA-12 are hard gates on Issue #112
   (backtesting) and SA-04, SA-09, SA-12 are hard gates on Issue #111 (WebScenarioRunner).

---

## Appendix: Milestone 3 Sequencing Implications

Per the sequencing constraint documented on Issue #61:

| Amendment | Blocks | Unblocked by |
|---|---|---|
| SA-04 (lifecycle state machine) | Issue #111 | This review complete |
| SA-09 (JSONB envelope format) | Issues #111, #112 | This review complete |
| SA-12 (snapshot serialization) | Issue #111 | This review complete |
| SA-01 (canonical IA-1 text) | Issue #112 | This review complete |
| SA-02 (ModelConfidence enum) | Issue #112 | This review complete |
| SA-08 (threshold type registry) | Issue #112 | This review complete |
| SA-07 (human cost threshold requirement) | Issue #112 | This review complete |
| CONFLICT C-1 disposition | ADR-004 Decision 1 | Engineering Lead |

STD-REVIEW-002 Phase 3 is complete. Phase 4 begins when the Engineering Lead
reviews CONFLICT C-1 and approves amendment instructions.
