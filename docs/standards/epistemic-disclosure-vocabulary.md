# Epistemic Disclosure Vocabulary Standard

**Author:** Chief Methodologist
**Date:** 2026-06-03
**Authority:** ARCH-REVIEW-006 AR-006-B-007; PI-REVIEW-002 F-005 (PR #598)
**EL sign-off:** Accepted 2026-06-03
**Status:** Active — blocks all US-043 implementation

---

## Purpose

Defines the canonical plain-language vocabulary for epistemic disclosure in community
report exports (US-043). Replaces technical confidence tier notation for non-specialist
audiences without omitting epistemic qualification — satisfying the No False Precision
principle (CLAUDE.md §Guiding Principles, absolute).

Plain-language disclosure is not a weakened form of epistemic transparency. It is
the correct form of epistemic transparency for an audience that lacks the background
to interpret "Tier 4 — Synthetic Estimate (Comparable Economy Inference)" without
further explanation. The canonical user for US-043 is a community advocacy coordinator
preparing a report for a local council, not a development economist.

---

## Trigger Condition

Any indicator with `confidence_tier >= 3` receives a plain-language disclosure in
the community report output. The disclosure **replaces** (does not omit) technical
confidence tier notation.

Tiers 1 and 2 require no disclosure — these represent observed, high-quality data
that does not require qualification for a non-specialist audience.

---

## Vocabulary Mapping

| confidence_tier | Trigger | Display string |
|---|---|---|
| 1 | No disclosure | — |
| 2 | No disclosure | — |
| 3 | `>= 3` | "Based on a model estimate from comparable countries" |
| 4 | `>= 3` | "This is an estimated figure — independent verification recommended" |
| 5 | `>= 3` | "Insufficient data — the model could not compute this reliably" |

These strings are **canonical constants**. They must not be paraphrased, abbreviated,
translated inline, or modified by the implementing pipeline without a new CM-authored
revision to this document.

---

## Placement Rule

In a two-column A4 print format, epistemic disclosure appears as an **inline qualifier**
immediately following the indicator value in parentheses.

**Example output:**

> Education enrollment rate: 68% *(This is an estimated figure — independent verification recommended)*

**Alternatives considered and rejected:**

| Option | Rationale for rejection |
|---|---|
| Footnote (numbered reference at column bottom) | Requires reader navigation away from the finding. For non-specialists reading under time pressure, this reduces the probability the disclosure is read at all. |
| Sidebar callout (boxed note in margin) | Applies to a section, not an individual indicator. A section may contain indicators of different confidence tiers — section-level callout is misleading. |
| Separate epistemic summary section | Placed after the findings, requiring the reader to cross-reference. Fails the adjacency requirement. |

**Accepted: inline qualifier.** The disclosure appears in the same visual unit as the
value it qualifies. The reader encounters the finding and its epistemic qualification
simultaneously, without navigation.

---

## Implementation Contract

The export pipeline's conditional disclosure logic must:

1. Check `confidence_tier` for each indicator before rendering.
2. If `confidence_tier >= 3`: append the display string from the vocabulary mapping
   table as an inline parenthetical, enclosed in `*(…)*` markup, immediately after
   the indicator value.
3. If `confidence_tier < 3`: render the value with no disclosure text.
4. The display string is a canonical constant — use verbatim from the table above.
5. If `confidence_tier` is `null` or missing, treat as Tier 4 ("This is an estimated
   figure — independent verification recommended") and log a data quality warning.

---

## Validation Requirements

The disclosure vocabulary must be covered by an automated test that renders a test
report containing one indicator of each confidence tier and asserts:

| confidence_tier | Expected: disclosure present | Expected: display string |
|---|---|---|
| 1 | No | — |
| 2 | No | — |
| 3 | Yes | "Based on a model estimate from comparable countries" |
| 4 | Yes | "This is an estimated figure — independent verification recommended" |
| 5 | Yes | "Insufficient data — the model could not compute this reliably" |
| null | Yes | "This is an estimated figure — independent verification recommended" |

---

## Scope Boundary

This standard governs community report export output only (US-043). It does not
govern the trajectory view, MDA alert panel, radar chart, or any other primary
instrument display. Technical confidence tier notation remains in use for those
surfaces — the canonical user for primary instruments is the finance ministry
analyst, not the community advocacy coordinator.

---

## Revision History

| Version | Date | Change | Authorised by |
|---|---|---|---|
| 1.0 | 2026-06-03 | Initial issue — closes Issue #603 | EL (@PublicEnemage) |
