# Scenario Creation Guide

> **Purpose:** This guide explains what you are choosing when you create a
> WorldSim scenario — entity, time range, module configuration — and how to
> read the data provenance signals that appear before and after you run it.

---

## Before You Begin

When you create a scenario, you are not choosing a *prediction*. You are
choosing a *configuration* — which country, which time window, which policy
parameters — and WorldSim will show you what the simulation engine produces
given those inputs.

The most important thing to understand before running a scenario: the
**grounding strip** is the simulation's declaration of what it actually knows
about your chosen entity. Read it before you interpret any output.

---

## Creating a Scenario

### 1. Select an Entity

Use the entity selector dropdown to choose the country or sovereign entity you
want to analyze. Entities are identified by ISO 3166-1 alpha-3 codes
(e.g., `JOR` for Jordan, `ZMB` for Zambia, `GRC` for Greece).

**What entity selection determines:**
- Which data the grounding strip will show
- Which confidence tiers apply to the initial state
- Whether any data gaps or structural absence declarations will appear

### 2. Set the Time Window

Set the start date and the number of simulation steps. Each step represents a
discrete time period (quarter or year depending on the scenario configuration).

**Choosing step count:**
- 4–8 steps is standard for a near-term scenario analysis
- Confidence tiers degrade for forward projections beyond the data coverage
  window — see the [Data Provenance Guide](data-provenance.md) for how tier
  attenuation works

### 3. Review the Data Quality Preview

Before confirming scenario creation, a **data quality preview** will appear
showing the confidence tier for each measurement framework for the selected
entity:

```
Jordan (JOR)
  Financial indicators     — T2 · IMF BOP · 2024-Q1
  Human development        — T2 · World Bank WDI · 2023
  Ecological indicators    — T4 (synthetic — regional comparables)
  Governance indicators    — T3 · V-Dem · 2023
```

Each tier rating tells you how reliable the initial state data is for that
framework. `T2 · IMF BOP · 2024-Q1` means:

- **T2**: Tier 2 — derived official statistics, citable directly
- **IMF BOP**: the source is the IMF Balance of Payments Statistics
- **2024-Q1**: the vintage (most recent data coverage period)

If a framework shows `T4 (synthetic — regional comparables)`, the simulation
will use modeled estimates in the absence of direct data. If it shows `T5 (no
data — Structural Absence)`, that framework cannot be estimated — see the
Data Provenance Guide for how to handle this.

---

## The Grounding Strip

After a scenario is created and advanced to at least step 1, the **grounding
strip** appears below the scenario controls. The grounding strip is the
simulation's per-indicator data provenance declaration — for each input
variable, it shows the source, the vintage, and the confidence tier.

**What the grounding strip shows:**

Each row in the grounding strip follows this format:

```
[Indicator name]                    [Source · Vintage · T{N}]
Reserve coverage (months)           CBJ Annual Report · 2023-Q4 · T2
GDP growth rate (%)                 IMF WEO · 2024-Apr · T2
Political stability index           V-Dem · 2023 · T3
Ecological boundary proximity       Synthetic composite · T4
```

**Reading confidence tiers in the grounding strip:**

| Tier | Label | What it means |
|---|---|---|
| T1 | Primary official | Directly measured, primary source, methodology published |
| T2 | Derived official | Calculated from T1 sources by reputable institutions |
| T3 | Research estimate | Published estimate from peer-reviewed or major research sources |
| T4 | Model estimate | Synthetic estimate — no primary source; modeled from comparables |
| T5 | No data | Structural Absence Declaration — data absence is itself a signal |

**Why the grounding strip matters for negotiating contexts:**

If your scenario uses T1 or T2 data for a key indicator, you can cite that
source directly in a negotiating session: "This projection uses IMF BOP 2024-Q1
data for reserve coverage — we are working from the same primary source you
are." That is a different position than working from T3 or T4 estimates.

---

## Module Configuration

After entity selection, you can configure which analytical modules are active:

- **MacroeconomicModule**: GDP, fiscal balance, inflation — always active
- **HumanDevelopmentModule**: HDI-adjacent indicators, cohort disaggregation
- **EcologicalModule**: Planetary boundary proximity, land-use pressure
- **GovernanceModule**: V-Dem-based governance indicators, institutional capacity
- **PoliticalEconomyModule**: Programme survival probability, legitimacy dynamics,
  elite capture coefficient — enable when analyzing IMF/World Bank programme
  scenarios

**Enabling PoliticalEconomyModule for negotiation support:**
When this module is active, the simulation adds `programme_survival_probability`
to the Zone 1D output — the model's estimate of the political feasibility of a
proposed programme surviving through its implementation window. This is the
specific output most relevant for IMF negotiation scenarios.

---

## Advancing the Scenario

Use the step controls to advance the scenario:

- **"Next Step"**: advance one step forward
- The step counter shows "Step N / M" where N is the current step and M is
  the total configured steps
- Zone 1B will update with new threshold breach alerts at each step
- Zone 1A trajectory will extend to show the new step

**Mode 2 (Simulation):** The default mode. The simulation projects forward
from the initial state using the configured parameters.

**Mode 3 (Active Control):** Allows you to change parameters mid-scenario —
for example, increasing the fiscal multiplier to model an alternative policy
path — and then advance from that branching point. The trajectory view will
show both the baseline (Mode 2) path and the alternative (Mode 3) path
simultaneously.

---

## Interpreting Output Annotations

In Zone 1D and other output zones, annotations appear alongside indicators:

- `[T2 · IMF BOP · 2024-Q1]` — Source citation with tier rating
- `[Fiscal ×1.30]` — The parameter setting driving this output (in Mode 3)
- `[PSP 59.5%]` — Programme survival probability (when PoliticalEconomyModule
  is active)
- `[STRUCTURAL_ABSENCE — electoral violence indicator]` — No data; the absence
  is declared, not estimated

See the [Data Provenance Guide](data-provenance.md) for a full explanation of
what each annotation means and how to use it.

---

*Next: [Data Provenance Guide](data-provenance.md) — confidence tiers, Structural
Absence Declarations, and how to cite WorldSim outputs in a negotiating context.*
