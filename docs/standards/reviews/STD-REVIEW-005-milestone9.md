# STD-REVIEW-005: Milestone 9 Exit Standards Gap Inventory

**Review type:** Full — all standards documents, seeded by M9 ADR work (ADR-007, ADR-008, ADR-010)
**Scope:** `docs/DATA_STANDARDS.md`, `docs/CODING_STANDARDS.md`, `docs/schema/`, open STD-REVIEW-004 gaps
**Date:** 2026-05-23
**Milestone:** Milestone 9 exit / Milestone 10 readiness
**Status:** Complete — GitHub Issues referenced for all findings requiring tracking
**Issue:** #439

---

## Purpose

STD-REVIEW-005 audits the standards documents for gaps that will affect Milestone 10
implementation. M9 was a documentation, standards, and process milestone — no simulation
code shipped. The seeding for this review comes from M9 ADR acceptance (ADR-007
Synthetic Data Framework, ADR-008 UX Architecture, ADR-010 Trajectory View as Primary
Instrument) and from STD-REVIEW-004 gaps carried forward.

A standards gap means: an ADR or architecture review document declares a requirement
but the corresponding standards document has not been updated to enforce it.
Developers implementing M10 will read `DATA_STANDARDS.md` and `CODING_STANDARDS.md` —
if a rule is only in the ADR, it will not be enforced.

---

## Documents Read

| Document | Notes |
|---|---|
| `docs/DATA_STANDARDS.md` | Full read |
| `docs/CODING_STANDARDS.md` | Full read (including new §Document Referencing Convention added 2026-05-23) |
| `docs/adr/ADR-007-synthetic-data-framework.md` | Full read — accepted 2026-05-23 |
| `docs/adr/ADR-008-ux-architecture.md` | Full read — accepted 2026-05-22 |
| `docs/adr/ADR-010-trajectory-view.md` | Full read — accepted 2026-05-22 |
| `docs/schema/database.yml` | Inspected for synthetic data field drift |
| `docs/schema/simulation_state.yml` | Inspected for `Quantity` field drift |
| `docs/schema/api_contracts.yml` | Inspected for trajectory endpoint drift |
| `docs/standards/reviews/STD-REVIEW-004-milestone7.md` | Full read — carried-forward gaps assessed |

---

## STD-REVIEW-004 Carried-Forward Gaps

| STD-REVIEW-004 Gap | Severity at M7 | Status at M9 | Notes |
|---|---|---|---|
| Gap 1 — DATA_STANDARDS.md: No canonical unit registry | Immediate | Still open — Issue #252 | No M9 code changes; gap persists. M10 adds simulation modules — this becomes blocking before any new indicator with a non-dimensionless unit ships. |
| Gap 2 — DATA_STANDARDS.md: No field-level data certification | Immediate | Still open — Issue #252 | No M9 data pipeline changes; gap persists. Required before any M10 source registration for GovernanceModule or second-country fixture. |
| Gap 3 — DATA_STANDARDS.md: WGI territorial convention | Near-term | Still open — no Issue filed | File as part of governance source registration work in M10 (Criterion 3 for GovernanceModule promotion). |
| Gap 4 — CODING_STANDARDS.md: [SIM-INTEGRITY] logging formal section | Near-term | Still open | Defensive Programming section (CODING_STANDARDS.md) covers the prefix contract but has no dedicated §Logging Standards section with log level requirements. Blocking before M10 engine work. Promote to Immediate for M10. |
| Gap 5 — (per STD-REVIEW-004 structure) | — | — | STD-REVIEW-004 had five gaps; Gaps 1–4 above account for all immediate/near-term items. |

---

## M9 New Findings

### Gap M9-1 — DATA_STANDARDS.md: Synthetic data tier floor not codified

**Severity:** Immediate
**Required amendment:** `docs/DATA_STANDARDS.md`
**GitHub Issue:** #508 (ADR-007 implementation gate — Alembic migration closes this gap)

**Description:**

ADR-007 §Section 4 establishes: "No synthetic estimate may carry Tier 1 or Tier 2.
The minimum tier for any synthetic estimate is Tier 3, achievable only via Method A
(holdout-validated) or Method B (short bounded gap)."

`DATA_STANDARDS.md §Data Quality Tier System` documents Tiers 1–5 but has no statement
of this floor. A developer reading only DATA_STANDARDS.md before writing synthetic data
code would have no guidance that Tiers 1–2 are prohibited for synthetic outputs.

**Required amendment to DATA_STANDARDS.md:**

Add to the §Data Quality Tier System section, after the tier table:

> **Synthetic data tier floor:** No synthetic estimate may carry Tier 1 or Tier 2.
> Synthetic data occupies Tiers 3–5 only, assigned per the method hierarchy in
> ADR-007 §Section 4. The `max()` rule is unchanged — synthetic outputs elevate the
> output tier to at least Tier 3 regardless of real-data input tiers.

**When to resolve:** In the same commit as the `Quantity` schema extension (ADR-007
implementation sequence step 2). Not required before M10 kickoff, but required before
any synthetic data output can be produced.

---

### Gap M9-2 — DATA_STANDARDS.md: `step_event_label` not documented as mandatory fixture field

**Severity:** Immediate
**Required amendment:** `docs/DATA_STANDARDS.md`
**GitHub Issue:** #395 (step_event_label mandatory field — M10 scope)

**Description:**

ADR-010 Decision 1 mandates `step_event_label` as a mandatory field on all Mode 1
scenario fixtures, enabling step axis annotation in the trajectory view (Issue #395).

`DATA_STANDARDS.md` has no fixture schema section that would communicate this
requirement to fixture authors. Without a fixture schema reference, fixture authors
adding a new backtesting fixture in M10 (Argentina or Ecuador) will not know to include
`step_event_label`, and the trajectory view will render without calendar-date labels.

**Required amendment to DATA_STANDARDS.md:**

Add a §Scenario Fixture Schema Requirements subsection specifying:

1. `step_event_label: str` — mandatory on all Mode 1 fixtures. Describes the
   historical event occurring at this step (e.g., "2010-Q2: Troika programme begins").
2. Format: human-readable, suitable for display in the step axis annotation layer.
3. Cannot be null or empty on any fixture step — validation gate required.

**When to resolve:** Before any M10 backtesting fixture is authored. Issue #395 tracks
the implementation; this gap closes when DATA_STANDARDS.md is updated in the same
commit as the first M10 fixture using `step_event_label`.

---

### Gap M9-3 — DATA_STANDARDS.md: Synthetic data per-indicator badge not in disclosure requirements

**Severity:** Near-term
**Required amendment:** `docs/DATA_STANDARDS.md`
**GitHub Issue:** None — file as part of ADR-007 implementation

**Description:**

ADR-007 §Section 2 establishes per-indicator synthetic badges as mandatory and
never-suppressible. This is a data provenance requirement — the badge must appear
regardless of display mode, configuration, or export format.

DATA_STANDARDS.md §Data Provenance Requirements defines source-level registration but
has no mandatory display obligation for synthetic indicators. A frontend developer
implementing the trajectory view in M10 who reads only DATA_STANDARDS.md before
implementing indicator display would not know the per-indicator badge is mandatory.

**Required amendment:** Add a §Synthetic Data Disclosure Obligations subsection
cross-referencing ADR-007 §Section 2, listing the five mandatory disclosures, and
explicitly stating these may not be suppressed by any frontend configuration.

**When to resolve:** Before M10 frontend implementation of the trajectory view and
radar chart. Not a M10 kickoff gate.

---

### Gap M9-4 — CODING_STANDARDS.md: No document referencing convention (resolved this PR)

**Severity:** Immediate
**Required amendment:** `docs/CODING_STANDARDS.md`
**GitHub Issue:** #398

**Description:**

Living documents were updated in M8 and M9 without a convention for revision headers or
stable reference points. Documents referencing `information-hierarchy.md` or
`north-star.md` could not determine which era of those documents the reference was
written against.

**Status: Resolved in this PR (2026-05-23).** Three conventions added to
CODING_STANDARDS.md §Document Referencing Convention: (1) revision header on all living
documents, (2) ADRs as stable reference points, (3) PR cross-references section. PR
template updated. CONTRIBUTING.md updated. Revision headers added to six living
documents. Closes Issue #398.

---

## Schema Drift Check

M9 delivered no simulation code changes. Schema files were not required to be updated
in M9. Confirmed no drift:

| Schema file | M9 changes required? | Status |
|---|---|---|
| `docs/schema/database.yml` | No — no Alembic migrations in M9 | No drift |
| `docs/schema/simulation_state.yml` | No — `Quantity` fields unchanged in M9 | No drift — ADR-007 schema extension is M10 implementation work |
| `docs/schema/api_contracts.yml` | No — no API endpoint changes in M9 | No drift |

**Note:** ADR-007 requires four new `Quantity` fields. `docs/schema/simulation_state.yml`
must be updated in the same commit as the Alembic migration (ADR-007 implementation
sequence step 2). This is not a M9 gap — it is a M10 implementation prerequisite.

---

## Summary

| Finding | Severity | Issue | Status |
|---|---|---|---|
| Carried: No canonical unit registry | Immediate (promote for M10) | #252 | Open |
| Carried: No field-level data certification | Immediate (promote for M10) | #252 | Open |
| Carried: WGI territorial convention | Near-term | None filed | Open |
| Carried: [SIM-INTEGRITY] logging formal section | Immediate (promote for M10) | None filed | Open — file before M10 kickoff |
| M9-1: Synthetic data tier floor | Immediate | #508 (implementation gate) | Open |
| M9-2: `step_event_label` mandatory fixture field | Immediate | #395 | Open |
| M9-3: Synthetic data per-indicator badge disclosure | Near-term | None filed | Open |
| M9-4: Document referencing convention | Immediate | #398 | **Resolved** (this PR) |

---

## Milestone 10 Kickoff Gates (from this review)

The following standards gaps must be resolved before the first M10 implementation
issue can be closed:

1. **[SIM-INTEGRITY] logging formal section** — file an issue and resolve before first
   M10 engine PR. The `[SIM-INTEGRITY]` prefix is used across the codebase without a
   governing standards document.

2. **`step_event_label` fixture requirement in DATA_STANDARDS.md** — resolve in the
   same commit as the first M10 backtesting fixture (Argentina or Ecuador).

3. **Synthetic data tier floor in DATA_STANDARDS.md** — resolve in the same commit as
   the `Quantity` schema extension Alembic migration.

All three are pre-implementation gates, not pre-kickoff gates. M10 kickoff may proceed.
