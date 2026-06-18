# Data Provenance Guide

> **Purpose:** This guide explains the WorldSim confidence tier system (T1–T5),
> what each tier means for your negotiating position, and how to read and
> cite a Structural Absence Declaration in a debt restructuring session.

---

## Why Data Provenance Matters

When you walk into a negotiating session, the creditor side knows the provenance
of their data. They know whether a reserve coverage figure comes from a central
bank primary statistical release or a derived model estimate. You should know
the same thing about the data your analysis is built on.

WorldSim makes data provenance explicit at the indicator level — every output
carries a source citation and a confidence tier rating. This is not a disclaimer
buried in methodology footnotes. It is the primary signal the simulation uses
to tell you what kind of argument you can make.

---

## The Confidence Tier System (T1–T5)

### Tier 1 — Primary Official Statistics

**What it is:** Directly measured data published by authoritative primary
sources with published methodology and audit standards.

**Sources at Tier 1:** World Bank Open Data, IMF Balance of Payments Statistics,
national statistical offices publishing finalized national accounts, BIS
International Banking Statistics, WHO Global Health Observatory, UN Population
Division.

**What Tier 1 means for your negotiating position:**
Tier 1 data is citable directly — you can name the institution and vintage
in a negotiating session. "This projection uses World Bank GDP data for 2023,
finalized national accounts — the same primary source you are working from."
That is a statement the creditor side cannot dispute on provenance grounds.

**Uncertainty bound:** uncertainty_range_pct ≤ 5%

---

### Tier 2 — Derived Official Statistics

**What it is:** Calculated from Tier 1 sources by reputable institutions using
documented, reproducible methodology.

**Sources at Tier 2:** OECD calculations from national accounts, World Bank
derived indicators (e.g., GNI per capita), IMF Article IV consultation
estimates, IMF Balance of Payments Statistics derived ratios, central bank
published analytical reports.

**What Tier 2 means for your negotiating position:**
Tier 2 means the source is citable directly — you can name the institution
and vintage in a negotiating session. "IMF BOP 2024-Q1" is Tier 2. The
central bank of Jordan's annual report estimate is Tier 2 when the methodology
is published. A Tier 2 figure is not as strong as a finalized national accounts
figure, but it is primary-institution-derived and fully attributable.

**Example from the instrument cluster:**
> `Reserve Coverage (months)   CBJ Annual Report · 2023-Q4 · T2`

This annotation means: the reserve coverage figure in the simulation is derived
from the Central Bank of Jordan Annual Report, Q4 2023 vintage, at Tier 2
quality. You can cite this in a restructuring session: "Our reserve coverage
projection is seeded from CBJ 2023-Q4 — the most recent CBJ official publication."

**Uncertainty bound:** uncertainty_range_pct ≤ 15%

---

### Tier 3 — Research Estimates

**What it is:** Published estimates from peer-reviewed academic sources or
major research institutions with documented methodology and stated uncertainty
ranges.

**Sources at Tier 3:** Tax Justice Network illicit flow estimates, UNCTAD FDI
analysis, V-Dem governance indicators, Uppsala Conflict Data Program.

**What Tier 3 means for your negotiating position:**
Tier 3 figures are research-backed but not primary official statistics. They
are appropriate for framing directional arguments — "the governance trajectory
indicates institutional capacity decline" — but should not be cited as
precision measurements. Disclose that the figure is a research estimate when
citing it.

**Uncertainty bound:** uncertainty_range_pct ≤ 30%

---

### Tier 4 — Model Estimates

**What it is:** Values produced by other simulation models, including WorldSim's
own projections, synthetic estimates, or extrapolations beyond data coverage.

**What Tier 4 means for your negotiating position:**
Tier 4 outputs are model-internal estimates. They are appropriate for scenario
framing — "if the ecological deterioration trajectory continues" — but cannot
be cited as measurements. When the grounding strip shows T4 for a framework,
that framework's outputs are projections, not observations.

**In the annotation format:**
> `Ecological indicators    T4 (synthetic — regional comparables)`

This means the ecological indicators were estimated from regional comparison
data rather than direct measurement for this entity.

**Uncertainty bound:** uncertainty_range_pct ≤ 50%

---

### Tier 5 — Structural Absence Declaration

**What it is:** When data absence is itself a signal — and generating a synthetic
estimate would mask that signal — WorldSim issues a Structural Absence Declaration
rather than producing a T4 estimate.

**When STRUCTURAL_ABSENCE is declared:**
A STRUCTURAL_ABSENCE declaration appears when all of the following are true:
- No primary or derived official data exists for this indicator in this entity
- There are fewer than 3 comparable entities with sufficient data to justify
  regional inference
- The confidence interval on any synthetic estimate would span the full feasible
  range (directionally meaningless)

A STRUCTURAL_ABSENCE is not a gap to be filled. It is a documented statement
that the data needed to compute this indicator for this entity does not exist
in computable form. The absence may itself be informative — a country that
has stopped reporting electoral violence statistics, expelled monitoring
organizations, or systematically falsified data produces a STRUCTURAL_ABSENCE
declaration whose cause is the finding.

---

## How to Cite a Structural Absence in a Negotiating Context

This is the most important use of the Structural Absence Declaration in
a ministry context.

**The scenario:** You are in a debt restructuring session. The creditor side
presents a debt sustainability analysis that treats the absence of bilateral
debt data (non-public Chinese bilateral lending) as zero. You want to challenge
this.

**What WorldSim shows:**
```
Bilateral debt (Chinese bilateral)   STRUCTURAL_ABSENCE — data not published
                                     Do not interpolate.
```

**How to cite it:**
> "Our scenario analysis flags the absence of Chinese bilateral lending data
> as a STRUCTURAL_ABSENCE_DECLARATION — the data structure exists, the debt
> obligations exist, but the values are not publicly available. Treating absent
> data as zero in a debt sustainability analysis is an assumption that requires
> justification, not a neutral default. We are requesting that the creditor's
> analysis disclose this assumption explicitly."

This argument is available to you because WorldSim distinguishes between "we
don't have the data and have filled it with a model estimate" (T4) and "the
data cannot be estimated with any reliability — treating it as zero is an active
analytical choice" (STRUCTURAL_ABSENCE). The creditor side using a standard
DSA tool may not have made this distinction explicit.

**Another example — electoral violence indicators:**
In the governance module, electoral violence indicators for entities that have
expelled V-Dem monitoring organizations will show:
```
Electoral violence indicator    T5 — STRUCTURAL_ABSENCE
                                Data absent: monitoring organization expelled 2022.
```

In a session with international creditors who want to condition programme terms
on governance improvements:

> "The simulation cannot score governance deterioration on the electoral violence
> indicator because the data infrastructure was expelled. This is not a model
> limitation — it is a documented fact about what the international monitoring
> community can observe. The governance trajectory on indicators that can be
> measured shows the following..."

This allows you to argue from what is observable rather than accepting an
imputed governance score based on unreliable inference.

---

## Reading Confidence Tier Annotations in Zone 1D

Zone 1D shows the four-framework composite display with source annotations.
Each annotation follows this format:

```
[T{N} · Source · Vintage]
```

For Tier 2:
```
[T2 · IMF BOP · 2024-Q1]
```

For Tier 3:
```
[T3 · V-Dem · 2023]
```

For Tier 4:
```
[T4 · Synthetic — regional comparables]
```

For Tier 5:
```
[T5 · STRUCTURAL_ABSENCE]
```

The annotation tells you what kind of claim the underlying number supports.

---

## Tier Attenuation for Forward Projections

Confidence tiers degrade automatically as the simulation projects forward:

- Every 5 simulation steps beyond the data coverage window, the tier increases
  by 1 (toward T5)
- This is capped at T5 — the simulation will not project further when the
  uncertainty is too large to be meaningful

**What this means in practice:**
A 4-step scenario using 2024-Q1 data may show T2 outputs at step 1 degrading
to T3 by step 4. An 8-step scenario projecting to 2028 will show T3 or T4 at
the later steps. This is honest — the model's confidence in a 2028 projection
from 2024 data is lower than its confidence in a 2025 projection.

---

## Tier Propagation Rule

When the simulation combines inputs of different tiers, the output tier is the
**maximum** (worst) of the input tiers — not an average, not the best. This is
a conservative rule: a calculation that combines a T1 input with a T3 input
produces a T3 output.

**Example:**
Reserve coverage projection combining IMF BOP data (T2) with a V-Dem
governance adjustment (T3) produces a T3-labeled output. The governance
adjustment has weakened the data quality of the combined indicator.

This rule cannot be overridden. It is enforced at the `Quantity` type level
in the simulation engine.

---

*For the full technical specification of the confidence tier system, see
[`docs/DATA_STANDARDS.md §Confidence Tier System`](../DATA_STANDARDS.md).
For synthetic data generation rules and the conditions under which
STRUCTURAL_ABSENCE is declared, see
[`docs/adr/ADR-007-synthetic-data-framework.md`](../adr/ADR-007-synthetic-data-framework.md).*
