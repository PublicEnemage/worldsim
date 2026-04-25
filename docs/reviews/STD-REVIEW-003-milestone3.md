# STD-REVIEW-003: Milestone 3 Standards Gap Inventory

**Review type:** Full — all standards documents, seeded by ARCH-REVIEW-003 Phase 2 findings
**Scope:** `docs/CODING_STANDARDS.md`, `docs/DATA_STANDARDS.md`, `docs/adr/ADR-005-human-cost-ledger.md`,
`docs/architecture/reviews/ARCH-REVIEW-003-milestone3.md`,
`docs/scenarios/module-capability-registry.md`
**Date:** 2026-04-24
**Milestone:** Milestone 3 exit / Milestone 4 readiness
**Status:** Complete — GitHub Issues created for all findings

---

## Purpose

STD-REVIEW-003 audits the standards documents for gaps that will affect
Milestone 4 implementation. It is seeded by ARCH-REVIEW-003 Phase 2
findings, which identified four areas where ADRs reference standards
requirements that have not yet been written into the standards documents.

A standards gap in this context means: an ADR or architecture review
document declares a requirement ("this is a CODING_STANDARDS.md rule")
but the corresponding standards document has not been updated to include
that rule. Developers implementing M4 features will read CODING_STANDARDS.md
and DATA_STANDARDS.md, not ADR prose. If the rule is only in the ADR, it
will not be enforced.

**Scope of this review:** Four specific areas identified by ARCH-REVIEW-003
Phase 2, plus any additional gaps discovered during document reading.

---

## Documents Read

| Document | Lines | Notes |
|---|---|---|
| `docs/CODING_STANDARDS.md` | 919 | Full read |
| `docs/DATA_STANDARDS.md` | 1122 | Full read |
| `docs/adr/ADR-005-human-cost-ledger.md` | 1131 | Full read |
| `docs/architecture/reviews/ARCH-REVIEW-003-milestone3.md` | 656 | Full read |
| `docs/scenarios/module-capability-registry.md` | 458 | Full read |

---

## Findings

### Gap 1 — CODING_STANDARDS.md: measurement_framework tagging enforcement rule absent

**Severity:** Immediate
**Required amendment:** `docs/CODING_STANDARDS.md`
**GitHub Issue:** #171

**Description:**

ADR-005 Decision 2 states explicitly:

> *"All attributes produced by new modules at M4 and later must carry an
> explicit `measurement_framework` tag — this is a CODING_STANDARDS.md
> requirement that the compliance scan must enforce."*

`docs/CODING_STANDARDS.md` has no such rule. §Human Cost Ledger Testing
(lines 703–754) covers test requirements for HCL outputs but contains no
enforcement rule for `measurement_framework` tagging. There is no compliance
scan rule flagging `QuantitySchema` instantiations that omit the field.

A developer implementing the Demographic module in M4 will read
CODING_STANDARDS.md and find no instruction requiring `measurement_framework`
on every attribute. The ADR's intent will not be enforced.

**Required amendment to CODING_STANDARDS.md:**

Add a §Measurement Framework Tagging subsection specifying:
1. All `QuantitySchema` attributes produced by M4+ module code in
   `app/simulation/` must include an explicit `measurement_framework` value
   from the ADR-005 canonical set: `financial`, `human_development`,
   `ecological`, `governance`.
2. The compliance scan must flag any `QuantitySchema` instantiation in
   `app/simulation/` that omits `measurement_framework` unless covered by a
   declared exemption list.
3. Legacy Natural Earth loader attributes that predate this rule must either
   receive a default tag or be explicitly enumerated in the exemption list
   before the first M4 module is merged.

---

### Gap 2 — DATA_STANDARDS.md: no academic literature citation format for elasticity source registration

**Severity:** Immediate
**Required amendment:** `docs/DATA_STANDARDS.md`
**GitHub Issue:** #172

**Description:**

ADR-005 Decision 1 requires `CohortElasticity.source_registry_id` to be a
registered source, invoking the prohibition on unregistered data sources from
DATA_STANDARDS.md §Data Provenance Requirements.

`docs/DATA_STANDARDS.md` §Data Provenance Requirements defines
`SourceRegistration` with the following structure:

```
source_id, source_name, source_type, coverage_start, coverage_end,
coverage_countries, simulation_variables, permanent_url, notes
```

This schema is designed for empirical datasets (World Bank WDI, IMF WEO,
Eurostat LFS). An academic literature citation — for example, Acemoglu &
Restrepo 2019 on labor market elasticities — does not map cleanly to this
schema:
- No single `coverage_countries` (a meta-analysis covers many)
- No `coverage_start`/`coverage_end` in the dataset vintage sense
- `permanent_url` may be a DOI but is not always a stable dataset URL

There is no guidance in DATA_STANDARDS.md for how to register a literature
source. ADR-005 Decision 1 refers to DATA_STANDARDS.md as the authority but
DATA_STANDARDS.md has no provision for this case.

A developer registering `CohortElasticity` source IDs in M4 has no standard
to follow and will either invent an ad hoc citation format or force-fit the
dataset schema — either of which produces a non-uniform registry.

**Required amendment to DATA_STANDARDS.md:**

Add a `LiteratureSourceRegistration` subtype to §Data Provenance Requirements
(or add a `source_type` discriminator to `SourceRegistration`) covering:
`authors`, `year`, `title`, `journal_or_venue`, `doi_or_url`,
`estimated_elasticity_range`, `applicability_scope`.

Also specify:
- When to use the literature subtype vs. the dataset subtype
- What confidence tier is appropriate for elasticity parameters sourced from
  academic consensus (multiple agreeing papers), single-paper estimates, and
  backtesting-calibrated values

---

### Gap 3 — DATA_STANDARDS.md: MDA threshold tier upgrade evidence criteria undefined

**Severity:** Near-term
**Required amendment:** `docs/DATA_STANDARDS.md` or new `docs/methodology/mda-calibration.md`
**GitHub Issue:** #173

**Description:**

ADR-005 Decision 3 specifies:

> *"MDA thresholds ship at Tier 3 confidence. When backtesting cases provide
> enough historical breach evidence, specific thresholds will be upgraded to
> Tier 2 and documented in docs/methodology/mda-calibration.md."*

The phrase *"enough historical breach evidence"* is not defined anywhere.
`docs/DATA_STANDARDS.md` §Data Quality Tier System defines Tier 2 as
"Derived Official Statistics" — a provenance category for data sources, not
a standard for model threshold calibration evidence. The document contains no
criteria for when a model-derived threshold qualifies for a tier upgrade.

No `docs/methodology/mda-calibration.md` file exists.

Without defined criteria:
- Developers adding new backtesting cases cannot determine whether a case
  constitutes sufficient evidence to trigger a threshold upgrade
- Engineering Lead reviews of proposed upgrades have no standard to evaluate
  against
- The MDA tier upgrade pathway exists on paper but cannot function in practice

**Required amendment:**

Add to `docs/DATA_STANDARDS.md` §Data Quality Tier System, or create
`docs/methodology/mda-calibration.md`, specifying:

1. **Minimum case count**: Minimum number of independent historical breach
   cases that must be documented before a threshold is eligible for Tier 2
   upgrade
2. **Sensitivity requirement**: Minimum fraction of documented breaches the
   threshold must correctly identify (true positive rate)
3. **False positive ceiling**: Maximum acceptable false positive rate
4. **Review and approval process**: Who signs off on an upgrade and what
   documentation is required in `mda-calibration.md`

---

### Gap 4 — DATA_STANDARDS.md: no formal Known Limitation IA-1 section with canonical disclosure text

**Severity:** Immediate
**Required amendment:** `docs/DATA_STANDARDS.md`
**GitHub Issue:** #174

**Description:**

`docs/DATA_STANDARDS.md` references "Known Limitation IA-1" in multiple
places (§Confidence Tier, §Backtesting Integrity, and inline in the Quantity
type specification) but never defines it in a standalone section.

The canonical disclosure text (`IA1_CANONICAL_PHRASE`) exists in one place:

```python
# app/simulation/repositories/quantity_serde.py
IA1_CANONICAL_PHRASE = (
    "Forward projections carry inherited confidence tier without time-horizon "
    "degradation. Confidence tiers reflect data quality at observation date, not "
    "projection reliability. See DATA_STANDARDS.md Known Limitation IA-1."
)
```

This constant is normative by use — `test_ia1_disclosure_matches_canonical_phrase`
in `tests/unit/test_backtesting_fixtures.py` asserts that the Greece fixture's
`IA1_DISCLOSURE` matches it exactly. But the phrase instructs users to see
"DATA_STANDARDS.md Known Limitation IA-1" — a section that does not exist in
DATA_STANDARDS.md.

The enforcement chain is:
- DB: `ia1_disclosure NOT NULL` (syntactic) — enforces presence of a string
- Code: `validate_ia1_disclosure()` (Issue #144) — enforces non-empty/non-whitespace
- Test: `test_ia1_disclosure_matches_canonical_phrase` — enforces the Greece
  fixture matches `IA1_CANONICAL_PHRASE`

None of these enforce that a developer writing a *new* module uses the canonical
phrase rather than an arbitrary non-empty string. The canonical text must be
normative in DATA_STANDARDS.md, not inferred from Python code.

ARCH-REVIEW-003 BI3-I-01 and its multiple council agents (Development Economist,
Intergenerational Advocate, Political Economist) independently identified this
gap as the most consequential unaddressed finding from the IA-1 compliance
exception. When M4 introduces multi-decade Human Cost Ledger projections, the
`ia1_disclosure` content is the primary user-facing signal about projection
reliability.

**Required amendment to DATA_STANDARDS.md:**

Add a standalone §Known Limitation IA-1 section specifying:

1. **Definition**: Forward projections carry inherited confidence tier from the
   observation date without time-horizon degradation. Confidence tier reflects
   data quality at observation, not projection reliability.
2. **Canonical disclosure text**: The exact phrase all `ia1_disclosure` fields
   must contain. This must match `IA1_CANONICAL_PHRASE` in `quantity_serde.py`
   (and that constant should reference this section as its authoritative source).
3. **Required disclosure elements**: (a) reference to IA-1 limitation by name,
   (b) statement that confidence tier reflects observation quality not projection
   reliability, (c) reference to DATA_STANDARDS.md Known Limitation IA-1.
4. **Placeholder prohibition**: A string that passes `validate_ia1_disclosure()`
   but does not include the required elements is prohibited. All implementations
   must use the canonical phrase.
5. **Cross-reference**: Issue #69 (compliance exception deferring time-horizon
   degradation to M4), Issue #144 (semantic validation implementation).

---

## Additional Gap Identified During Reading

### Gap 5 — ARCH-REVIEW-003 BI3-N-10 / Issue #160: fidelity report statistical power statement has no format standard

**Severity:** Near-term
**Required amendment:** `docs/CODING_STANDARDS.md` or `docs/DATA_STANDARDS.md`
**GitHub Issue:** #160 (already exists from ARCH-REVIEW-003 creation)

**Description:**

ARCH-REVIEW-003 BI3-N-10 (Chief Methodologist) and Issue #160 call for adding
a statistical power statement to all fidelity reports. However, neither
CODING_STANDARDS.md nor DATA_STANDARDS.md specifies what this statement must
contain, where it must appear in the report, or what format it must take.

Without a format standard in a standards document, Issue #160 will be
implemented ad hoc. The resulting statement may differ in wording between
the Greece 2010–2012 fixture and future fixtures (Thailand 1997, Issue #141;
Greece extension, Issue #142), making the power statement non-comparable
across backtesting cases.

**Required amendment:**

Add to `docs/CODING_STANDARDS.md` §Backtesting Requirements or to
`docs/DATA_STANDARDS.md` §Backtesting Integrity:

1. A required statistical power statement format for all fidelity reports,
   specifying that "PASS" means direction-correct on N binary sign checks
   and does not imply quantitative accuracy or distributional fitness.
2. The statement must appear as a fixed section in every `format_fidelity_report()`
   output, above the threshold results table.
3. Future backtesting cases (Thailand, etc.) must use the same format.

*Note: Issue #160 already tracks the implementation. This gap is that
the implementation target has no format standard to implement against.
This gap is noted for completeness; a separate issue is not needed as
#160 can be amended to include the format standard specification.*

---

## Summary

| Gap | Severity | Standard to Amend | Issue |
|---|---|---|---|
| 1 — measurement_framework tagging enforcement missing from CODING_STANDARDS.md | Immediate | CODING_STANDARDS.md | #171 |
| 2 — No academic literature citation format in DATA_STANDARDS.md §Data Provenance | Immediate | DATA_STANDARDS.md | #172 |
| 3 — MDA threshold tier upgrade evidence criteria undefined | Near-term | DATA_STANDARDS.md | #173 |
| 4 — No formal Known Limitation IA-1 section in DATA_STANDARDS.md | Immediate | DATA_STANDARDS.md | #174 |
| 5 — Fidelity report statistical power statement has no format standard | Near-term | CODING_STANDARDS.md or DATA_STANDARDS.md | #160 (amend) |

Three of five gaps are horizon:immediate — they affect code that will be
written in M4 module implementation and will be invisible to compliance scans
until the standards documents are updated.

Gap 4 (Known Limitation IA-1) is the most consequential: the canonical
disclosure phrase instructs users to read DATA_STANDARDS.md for the full
IA-1 context, but that section does not exist. Every `ia1_disclosure` field
in production currently references a non-existent document section.

---

## Engineering Lead Dispositions

*To be recorded at time of STD-REVIEW-003 review.*

*Single-principal governance limitation applies — see CLAUDE.md §Governance.*

| Gap | Disposition |
|---|---|
| Gap 1 (#171) | |
| Gap 2 (#172) | |
| Gap 3 (#173) | |
| Gap 4 (#174) | |
| Gap 5 (#160) | |
