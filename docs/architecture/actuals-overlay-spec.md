# Actuals Overlay Architecture Spec — US-042

**Authors:** Data Architect, Frontend Architect
**Date:** 2026-06-03
**Authority:** ARCH-REVIEW-006 AR-006-B-004, AR-006-B-005, AR-006-B-006, AR-006-C-001
**EL sign-off:** Accepted 2026-06-03
**Closes:** Issues #604 (data model + rendering contract), #605 (confound disclosure
decision), #607 (human development parity requirement)

---

## Context

US-042 (accountability tracking overlay) requires rendering observed actuals — IMF
Article IV consultation outcomes, World Bank HIPC tracker data, government post-program
self-reports — as a distinct data series on the trajectory view (Zone 1) alongside
simulation projections.

This spec covers: data model, confidence tier protocol, engine/overlay separation
constraint, confound disclosure decision, rendering contract, sparse data handling rule,
and human development parity requirement.

---

## 1. EL Decision — Confound Disclosure (AR-006-B-005)

**Decision: Option B — API-layer constraint.** Accepted 2026-06-03.

The actuals overlay endpoint **may not return a response** without a `confound_annotation`
field. The field is required in the response schema — an empty or null value is a
validation failure, not a permitted state.

**Rationale:** The No False Precision principle (CLAUDE.md, absolute) requires that a
comparison between simulation projection and observed outcome not imply causal attribution
the model cannot support. A direct overlay without confound disclosure implies divergence
is fully attributable to policy choices — false in most real cases. Option A (rendering-layer
disclosure) relies on implementation discipline; Option B makes the constraint structural.
A confound annotation that cannot be omitted at the API layer cannot be omitted by accident
at the rendering layer. When an absolute principle is at stake, structural enforcement
is preferable to implementation-time discipline.

**CM and DE consultation:** Recorded in ARCH-REVIEW-006 §Challenge from Chief Methodologist
and §Challenge from Development Economist (`docs/architecture/reviews/ARCH-REVIEW-006-milestone10.md`).

---

## 2. Data Model

### 2.1 Storage Location

Observed actuals are stored in the `source_registry` table, not in the simulation
computation tables. They are sourced, not computed — conflating them with simulation
state would violate the engine/overlay separation constraint (AR-006-C-001, §3 below).

Each actuals data point is registered as a `SourceRegistration` entry. The actuals
series is keyed by: `(entity_id, indicator_key, vintage_date, source_id)`.

Actuals values are stored in a new table `observed_actuals`:

```sql
-- observed_actuals table (to be created in a migration)
CREATE TABLE observed_actuals (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id   TEXT NOT NULL REFERENCES simulation_entities(entity_id),
    source_id   UUID NOT NULL REFERENCES source_registry(id),
    indicator_key TEXT NOT NULL,
    step_year   INTEGER NOT NULL,   -- calendar year this observation covers
    value       NUMERIC NOT NULL,
    unit        TEXT NOT NULL,
    confidence_tier INTEGER NOT NULL CHECK (confidence_tier BETWEEN 1 AND 5),
    vintage_date DATE NOT NULL,     -- date the observation was published/retrieved
    notes       TEXT
);
```

### 2.2 Source Registry Registration Pattern

Every actuals source must be registered in `source_registry` before its data is loaded.
`DataClassification` is PUBLIC for all approved actuals sources listed in
`docs/data-sources/approved-sources.md`.

```python
SourceRegistration(
    name="IMF Article IV Consultation Outcomes — GRC 2011-2014",
    source_type=SourceType.INTERNATIONAL_ORGANIZATION,
    classification=DataClassification.PUBLIC,
    confidence_tier=2,
    vintage_date=date(2015, 6, 1),
    permanent_url="https://www.imf.org/...",  # required for PUBLIC sources
    notes="Article IV consultation staff reports, Table 3 — Fiscal Outturn",
)
```

### 2.3 Confidence Tier Assignment Protocol

| Source type | Default tier | Override conditions |
|---|---|---|
| IMF Article IV consultation staff report | 2 | Downgrade to 3 if preliminary/provisional notation present |
| World Bank HIPC tracker (published) | 2 | — |
| Government post-program self-report | 3 | Upgrade to 2 only with independent audit confirmation |
| Civil society monitoring data | 3 | Upgrade requires documented methodology review |
| Press-reconstructed historical data | 4 | — |

The confidence tier is per-observation, not per-source. A source may contribute
observations at different tiers across different indicators.

---

## 3. Engine/Overlay Separation Constraint (AR-006-C-001)

**This constraint is non-negotiable and must be enforced at the API layer.**

The actuals overlay endpoint must not route through the simulation computation path.
Observed actuals are not simulation outputs — they are externally sourced historical
observations. Routing them through the simulation engine would:

1. Risk conflation with simulation output in the data provenance chain
2. Allow the simulation engine to modify actuals (e.g., through normalization or smoothing)
3. Obscure the categorical distinction between "what the model projected" and "what was observed"

**Implementation requirement:** The endpoint at `GET /api/v1/scenarios/{id}/actuals` (see
§6 below, cross-referenced with `docs/schema/api_contracts.yml`) reads directly from
`observed_actuals` joined against `source_registry`. It does not call any simulation
computation function, does not read from `scenario_state_snapshots`, and does not invoke
the propagation engine.

This constraint must be verified by an integration test that confirms the actuals endpoint
returns data when the simulation engine is unavailable (e.g., in a test environment where
the engine is mocked out).

---

## 4. Rendering Contract

### 4.1 Visual Treatment

Observed actuals series must be visually distinct from simulation output series in all
rendering contexts. The distinction applies across all framework indicator curves.

| Property | Simulation output series | Observed actuals series |
|---|---|---|
| Line style | Solid | Dashed |
| Opacity | 100% | 85% |
| Marker | None | Circle marker at each observation point |
| Legend label | "[Indicator] (projected)" | "[Indicator] (observed — [Source abbrev])" |
| Tooltip | Standard simulation tooltip | Source name, vintage date, confidence tier label |

The framework color contract (Financial: `#2271B3`, Human Development: `#D4841A`,
Ecological: `#1A8FA0`, Governance: `#7B50A8`) applies to actuals series using the same
color as the simulation series for the same indicator. Visual distinction is achieved
through line style and marker, not color. This preserves the framework color contract
(UX Standards §1) while keeping actuals visually distinct.

### 4.2 Human Development Parity (AR-006-B-006)

Human development actuals **receive equal visual weight to financial actuals**. There
is no secondary-tier or optional treatment for human development indicator actuals. The
accountability tracking use case (US-042) is specifically a human cost ledger use case —
its primary analytical value is whether promised human development outcomes materialized.

**Implementation requirement:**
- The actuals overlay API endpoint must support human development indicator actuals
  without any optional treatment (e.g., it must not return human development actuals in
  a separate, optional response field or require a distinct query parameter)
- The trajectory view component must render human development actuals with the same
  visual prominence as financial actuals — no secondary opacity reduction, no legend
  deprioritization, no "show more" gating

This is an explicit Human Cost Ledger principle requirement, not a feature option.

### 4.3 Confound Disclosure Rendering (per EL Decision, §1)

The confound annotation returned by the API (§5.2) must be rendered as a persistent
note adjacent to the actuals overlay panel or control. It is not a tooltip — it must
be visible without hover. The annotation is structural disclosure, not a fine-print
disclaimer.

### 4.4 Sparse Data Handling

Observed actuals are not available for every time step in the simulation window.
The rendering contract for gaps:

- **Broken line:** The actuals series renders as a broken line with visible gaps where
  observations are absent. No interpolation. No null-connected segments.
- **Sparse observation markers:** Circle markers appear only at steps where an observation
  exists. No ghost markers at unobserved steps.
- **Gap annotation:** A tooltip on the gap region reads "No observation recorded for
  this period."

**Rationale:** Interpolating between sparse observations creates false continuity —
it implies knowledge of the intervening period that the data does not provide. A broken
line is honest about what is known. This is a No False Precision requirement.

---

## 5. API Contract Summary

The full API contract is maintained in `docs/schema/api_contracts.yml`. This section
provides a structural summary for implementers.

### 5.1 Endpoint

`GET /api/v1/scenarios/{scenario_id}/actuals`

Returns the observed actuals series for all indicators with registered actuals data
for the given scenario entity. Does not route through the simulation engine.

### 5.2 Required Response Fields

```yaml
confound_annotation:
  type: string
  required: true
  description: >
    Non-null, non-empty explanation that divergence between projection and actuals
    cannot be attributed solely to policy choices. Canonical text: "Divergence between
    projected and observed outcomes may reflect factors unrelated to the policy scenario
    modelled, including external shocks, data revision, and implementation variance.
    Causal attribution to policy choices alone is not supported by this comparison."
  validation: must not be null, empty, or absent — API layer enforcement
```

---

## 6. Cross-References

- `docs/schema/api_contracts.yml` — full actuals endpoint contract
- `docs/DATA_STANDARDS.md §DataClassification` — source classification rules
- `docs/DATA_STANDARDS.md §Confidence Tier System` — tier definitions
- `docs/architecture/reviews/ARCH-REVIEW-006-milestone10.md` — originating blindspots
- `docs/data-sources/approved-sources.md` — approved actuals sources
