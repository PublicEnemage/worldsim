---
name: path2-user-supplied-provenance-spec
type: design-artifact
artifact: 2 of 3
sprint-group: M14-G6b
authored-by: Architect Agent
authored-date: 2026-06-18
gates: M15 scoping and M16 implementation of Path 2
intent-document: docs/process/intents/M14-G6b-2026-06-18-path2-design-groundwork.md
acceptance-criteria: AC-5, AC-6
adr-amendment-to: ADR-016-scenario-grounding-architecture.md (§Provenance Type Enumeration)
---

# `USER_SUPPLIED` Provenance Type Specification — Draft ADR-016 Amendment

> **What this document is:** A draft amendment to ADR-016's provenance type enumeration,
> adding `USER_SUPPLIED` as a fifth type. This is not a new ADR and does not pass through
> the ADR acceptance process in M14. It is a design artifact that specifies what the amendment
> must contain so that the Path 2 implementation ADR can adopt it without redesign.
>
> **What it changes:** Only the provenance type enum and Grounding Strip display contract
> for user-supplied indicators. Grounding Strip layout, data quality preview, entity scope
> decisions, and simulation engine behaviour are unchanged.
>
> **Authority:** `docs/process/intents/M14-G6b-2026-06-18-path2-design-groundwork.md §AC-5, AC-6`

---

## 1. Current Provenance Type Enumeration (ADR-016 §API Contracts)

ADR-016 defines four provenance types for `DataSourceObject.source_type`:

| Enum value | Display label | Meaning |
|---|---|---|
| `OBSERVED` | observed | Data obtained directly from a primary institutional source (IMF, World Bank, central bank) with documented vintage |
| `ESTIMATED_COMPARABLE` | estimated (comparable economy) | Derived by statistical inference from comparable economies or regional distributions |
| `SYNTHETIC` | synthetic | Generated via the five-method synthetic data hierarchy (ADR-007); no observed primary source exists |
| `STRUCTURAL_ABSENCE` | not available | The indicator is structurally absent — not missing from the source registry but absent as a measurable quantity for this entity |

The backend implementation uses `confidence_tier` (integer 1–5) and `is_synthetic` (boolean)
as the runtime representation. The full enum typing of `source_type` is part of the
Path 2 implementation scope — this document specifies the fifth value to be added.

---

## 2. Amendment — Adding `USER_SUPPLIED` as Fifth Type

### 2.1 Enum Value

```
USER_SUPPLIED
```

**Rationale for all-caps enum style:** Consistent with existing four-value pattern
(`OBSERVED`, `ESTIMATED_COMPARABLE`, `SYNTHETIC`, `STRUCTURAL_ABSENCE`). The display
label is separate from the enum value — see §2.2 below.

### 2.2 Display Label (Plain English)

**Display label:** `user-supplied`

**Rationale:** "user-supplied" is plain English, immediately interpretable by a finance
ministry analyst without a glossary. It states what the value is — supplied by the user —
without implying a quality judgment. Technical alternatives that must NOT be used:

| Rejected label | Reason for rejection |
|---|---|
| `USER_DEFINED` | Suggests the value was invented or hypothetical; ministry data is real measured data |
| `SELF_REPORTED` | Has connotation of unverified survey data; inappropriate for a ministry's internal position |
| `US_PROVENANCE` | Opaque technical abbreviation; not interpretable by the primary user |
| `MINISTRY_DATA` | Scope is too narrow — Path 2 uploads may come from any institutional source, not only ministries |
| `PROPRIETARY` | Accurate but sounds exclusionary; "user-supplied" is more neutral and descriptive |

### 2.3 Grounding Strip Badge Convention

In the Grounding Strip citation line, `USER_SUPPLIED` indicators are displayed as:

```
[indicator label]: [value] [unit] — [institution name] ([provenance note, date]) · [tier] · user-supplied
```

**Canonical example:**
```
Reserve coverage: 2.80 months — Ministry of Finance (internal, 2026-06-18) · T2 · user-supplied
```

**Field breakdown:**
- `[indicator label]` — human-readable label as defined in the Grounding Strip display contract
  (e.g., "Reserve coverage")
- `[value] [unit]` — the transformed value in WorldSim canonical units (e.g., "2.80 months")
- `[institution name]` — the institution that supplied the data, as entered during the upload
  workflow or as metadata on the uploaded file. If unavailable, falls back to "User upload
  ([date])"
- `([provenance note, date])` — optional provenance note (e.g., "internal", "draft budget",
  "as-of-today"); and the upload date in ISO format (YYYY-MM-DD)
- `· [tier]` — the confidence tier label per the tier assignment rules in §3 below
- `· user-supplied` — the provenance type badge; always present for USER_SUPPLIED indicators

**Per-framework count chip (framework header level):**
```
[N user-supplied · M observed]
```
Example: `[2 user-supplied · 3 observed]` — shown at the right of the framework header row,
matching the existing `[T2 · IMF]` chip pattern. Frameworks with no user-supplied indicators
show only the existing observed-source chip.

---

## 3. Confidence Tier Assignment Rules for `USER_SUPPLIED`

### 3.1 Default tier for user-supplied data

`USER_SUPPLIED` data does not inherit a fixed tier from the provenance type alone. The tier
is assigned based on the upload context:

| Context | Default tier assignment | Rationale |
|---|---|---|
| Ministry self-reported data for the entity being modeled | **T2** | The ministry is the primary institutional source for its own fiscal and reserve position; the data is directly observed, not inferred. This is equivalent to a central bank reporting its own reserves. |
| Data for an entity the ministry does not govern | **T3** | The ministry is not the authoritative source; the data is a secondary report or an estimate. |
| Analyst does not specify context | **T3** | Conservative default when context is unknown. |

**Why T2 (not T1):** T1 in the confidence tier system (`docs/DATA_STANDARDS.md §Confidence
Tier System`) requires a documented, publicly verifiable primary source. User-supplied data
cannot satisfy the "publicly verifiable" criterion — it is by definition non-public. The
highest tier available to user-supplied data is therefore T2 (observed, primary source, not
publicly citable). T2 is the correct representation: the data is real and observed by its
institutional owner, but cannot be independently verified by a third party.

**The ministry may justifiably claim T1 for internal purposes.** The tool displays T2
because the tool's tier system measures public verifiability, not accuracy. A ministry's
internal reserve figure may be more accurate than the IMF's published figure, but the tool
cannot adjudicate that claim on behalf of the ministry. The T2 assignment is honest about
what the tool can certify, not dismissive of the data's actual quality.

### 3.2 Tier disclosure in the Grounding Strip

The confidence tier for a user-supplied indicator is disclosed identically to observed
indicators — the `· T2` label appears in the citation line. The `user-supplied` badge
supplements the tier label; it does not replace it. This maintains the coherent tier
display contract across all provenance types.

### 3.3 `USER_SUPPLIED` and the `max()` tier propagation rule

When a computation involves both user-supplied and observed indicators:
`confidence_tier(output) = max(confidence_tier(inputs))`

This is consistent with the existing rule in `docs/DATA_STANDARDS.md §Confidence Tier
Propagation`. A computation involving a T2 user-supplied input and a T2 observed input
produces a T2 output — no tier penalty for mixing provenance types at the same tier.
A computation involving a T4 synthetic input and a T2 user-supplied input produces a T4
output — the synthetic data degrades the output tier regardless of the user-supplied input.

---

## 4. Position in the Tier Hierarchy

The full updated tier hierarchy after `USER_SUPPLIED` is added:

```
Tier 1 — observed, publicly verifiable (primary institutional source, published)
Tier 2 — observed, primary source, not publicly citable (includes USER_SUPPLIED)
Tier 3 — estimated from comparable economies or academic literature
Tier 4 — synthetic inference (ADR-007 five-method hierarchy)
Tier 5 — structural absence or direction-only validity
```

**USER_SUPPLIED slots into Tier 2.** It does not create a new tier position; it is a
subtype within Tier 2 that carries a distinct provenance badge. The ordering within Tier 2:

```
Observed-public (T1) > Observed-institutional (T1) > User-supplied (T2) > Estimated-comparable (T3) > Synthetic (T4) > Structural absence (T5)
```

Simplified as stated in `docs/ux/user-journeys.md §GA-02`:
```
observed-public → user-supplied → synthetic → structural-absence
```

This ordering reflects the assumption that ministry-supplied data, while not publicly
verifiable, is more directly observed than synthetic inference from comparable economies.
This assumption is defensible for fiscal and reserve data from the ministry responsible for
those accounts; it may be less defensible for demographic or ecological data the ministry
has not directly measured.

**ADR-007 tier stack update required at Path 2 implementation time:** The ADR-007 tier
stack document (`docs/methodology/` — the synthetic data framework description referenced in
ADR-007 § Decision 1) must be updated when Path 2 ships to add `USER_SUPPLIED` at the T2
position. This is not a new ADR; it is an amendment to the methodology documentation. The
implementing agent for Path 2 holds R for this update.

---

## 5. ADR-007 Implication

ADR-007 (Synthetic Data Framework, ARCH-001) defines a five-method synthetic data hierarchy
that activates when no primary source exists for an entity/indicator combination. The tier
system in DATA_STANDARDS derives from ADR-007's tier classification.

**What must be updated when Path 2 ships:**
ADR-007's tier stack documentation must explicitly position `USER_SUPPLIED` as a T2 variant,
distinct from both T1 observed-public data (which ADR-007's synthetic fallback activates when
absent) and T4 synthetic data (which ADR-007 produces). The update is additive — no ADR-007
decision is reversed. The statement to be added:

> "User-supplied data (Path 2 upload) is classified as T2. It sits above the synthetic
> fallback in the tier hierarchy because it represents direct institutional observation of
> the entity's state — the ministry holds this data as a primary source, even if it is not
> publicly disclosed. T1 treatment is not applied because T1 requires public verifiability,
> which user-supplied data cannot satisfy by definition."

**What does NOT change in ADR-007:**
- The synthetic data framework's five-method hierarchy (regression, regional distribution,
  HDI decomposition, time-series extrapolation, expert elicitation)
- The three-condition meaninglessness threshold
- The MDA alert tier table
- The activation logic: ADR-007 activates when no primary source exists. If a user uploads
  data for an indicator that had synthetic coverage, the user-supplied value replaces the
  synthetic value for this scenario — the synthetic framework is no longer active for that
  indicator. The scenario's initial state for that indicator is user-supplied (T2), not
  synthetic (T4).

---

## 6. Scope Boundary — What ADR-016 Elements Are NOT Changed

The following ADR-016 elements are unchanged by the `USER_SUPPLIED` amendment:

| ADR-016 element | Status |
|---|---|
| Grounding Strip layout (Zone 2, one-interaction) | Unchanged — `USER_SUPPLIED` adds entries to the existing layout, does not change its position or interaction model |
| Data quality preview (Component 1) | Unchanged — the pre-creation preview shows framework-level coverage from the shared source registry; user-uploaded data is not visible in the pre-creation preview because it has not been uploaded yet at creation-form display time |
| Entity scope decisions (GRC, JOR, EGY, ZMB) | Unchanged — Path 2 data upload is entity-agnostic; the analyst uploads data for any entity in the creation form. The four-entity M14 scope constraint applies to the preloaded source registry, not to user-supplied data |
| `/api/v1/entities/{entity_id}/data-quality` endpoint | Unchanged — this endpoint returns registry-sourced coverage quality, not user-supplied indicator quality. A separate endpoint for user-supplied metadata is part of the Path 2 implementation scope |
| `/api/v1/scenarios/{scenario_id}/initial-state` endpoint | Extended — the response shape gains a `provenance_type` field on each indicator object (nullable for existing scenarios, `"USER_SUPPLIED"` for uploaded indicators). This is a backward-compatible extension: existing API consumers that do not read `provenance_type` are unaffected |
| Fidelity contextualisation (Component 3) | Unchanged — contextualisation is based on the scenario's entity and crisis mechanism, not on whether starting values are user-supplied |
| Parameter persistence (Component 4) | Unchanged — the parameter display shows scenario control inputs, not indicator starting values; user-supplied starting values appear in the Grounding strip, not the parameter display |

---

## 7. Backend Implementation Notes (for Path 2 ADR Reference)

These notes are observations for the implementing agent, not design decisions for this
document to make. They are recorded here to prevent the Path 2 implementation ADR from
encountering surprises.

**Source object shape extension (anticipated):**
The `initial_state` API response's indicator objects currently carry `confidence_tier` and
`is_synthetic`. Path 2 will require:

```json
{
  "indicator": "reserve_coverage_months",
  "value": "2.80",
  "unit": "months",
  "confidence_tier": 2,
  "is_synthetic": false,
  "provenance_type": "USER_SUPPLIED",
  "source": "Ministry of Finance",
  "source_note": "internal",
  "vintage": "2026-06-18"
}
```

The `provenance_type` field is the explicit enum value. Its absence (null) in existing
indicators is backward-compatible: pre-Path-2 indicators continue to use `is_synthetic` for
display logic until the full enum is implemented.

**Storage implication:** User-supplied indicator values must not be stored in `source_registry`
(shared platform table) — see `data-isolation-model-sketch.md` (Artifact 3). The initial-state
response assembles user-supplied values from the user's isolated storage and merges them with
registry-sourced values at response time.

**Frontend badge rendering:** The Grounding strip renders `· user-supplied` when
`provenance_type === "USER_SUPPLIED"` on an indicator object. Existing rendering logic
(`is_synthetic` → `T4 synthetic` badge) remains unchanged for non-Path-2 indicators.

---

*Artifact 2 of 3 for M14-G6b. Authored by Architect Agent. Filed at
`docs/design/path2-data-upload/user-supplied-provenance-spec.md`. Acceptance criteria
covered: AC-5 (USER_SUPPLIED defined with display label, Grounding Strip example, tier rules,
tier hierarchy position), AC-6 (ADR-007 implication stated; ADR-016 unchanged elements
listed). See `docs/process/intents/M14-G6b-2026-06-18-path2-design-groundwork.md` for the
full AC list and EL review gate.*
