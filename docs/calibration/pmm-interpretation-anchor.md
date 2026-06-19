# PMM Interpretation Anchor

> **What this document is:** An explanation of the Political-Macro-Market (PMM)
> composite score displayed in Zone 1C of the WorldSim instrument cluster.
> It explains what the score represents, why it shows `[T3 composite · pre-cal]`,
> and what the pre-calibration status means for a finance ministry analyst who
> encounters it in a session.
>
> **Referenced from:** Calibration index (`docs/calibration/README.md`).
> Zone 1C PMM annotation. ADR-015 Component 1 (placeholder annotation).
>
> **Audience:** Persona 2 (Finance Ministry Negotiator) and Persona 1 (IMF Programme
> Analyst). Readable without specialist mediation.

---

## What the PMM score represents

The PMM composite score is a single scalar [0, 1] that aggregates three dimensions
of a sovereign's policy position:

1. **Political feasibility** — How much of the recommended policy package can the
   current government realistically implement given its legitimacy position and
   elite capture constraints. Derived from the PoliticalEconomyModule (ADR-013):
   `programme_survival_probability` × `implementation_capacity_modifier`.

2. **Macro trajectory** — Where the financial framework composite is headed: the
   rate of change of the financial composite score across the last 2–3 simulation
   steps, normalized to [−1, +1]. Positive = improving. Negative = deteriorating.

3. **Market signal** — A synthetic proxy for market confidence derived from the
   reserve coverage trajectory and the MDA breach pattern. Specifically: the ratio
   of steps without a TERMINAL breach to total steps projected so far, weighted by
   the reserve_coverage_months current value vs. the MDA floor.

**The PMM is not a prediction.** It is a real-time summary of where the simulation
stands on three dimensions the finance ministry team is likely to be asked about
in a session: "Can your government actually do this?", "Is the macro situation
getting better or worse?", and "What does the reserve position signal?"

The composite is an unweighted mean of the three normalized components. A PMM of
0.65 means the scenario is scoring roughly 65% across these three dimensions combined.

---

## What `[T3 composite · pre-cal]` means

Zone 1C displays the PMM as:

```
PMM  0.65
[T3 composite · pre-cal]
```

**T3 composite:** The confidence tier of the PMM is T3. This is because:
- The political feasibility component uses `programme_survival_probability` (T4,
  DIRECTION_ONLY per ADR-013 §CM constraint)
- The macro trajectory component uses the financial composite, which includes T3
  indicators (reserve_coverage_months with projection degradation)
- The market signal uses the MDA breach count, which is a model output (T4)

The composite tier follows the max() rule: T4 inputs → composite is T4. But the
PMM is annotated T3 during the pre-calibration phase because the weighting and
component methodology has not yet been externally validated. Once ADR-007 (PMM
calibration) is accepted and backtesting against historical cases is complete, the
tier annotation will reflect the actual tier derivation.

**pre-cal:** The PMM component weights, normalization method, and backtesting
calibration are not yet complete. ADR-007 (PMM calibration) is future work —
deferred beyond M14. The annotation `pre-cal` is a permanent disclosure until
ADR-007 is accepted and the calibration is complete.

**What this means for a ministry analyst:** The PMM score is a directional signal
during the pre-calibration phase. Use it to orient the team: "Are we above or
below 0.5? Is the trend improving?" Do not cite the PMM score itself in external
negotiations — cite the individual indicators it summarizes (reserve_coverage_months,
programme_survival_probability) which have their own defensibility tiers.

---

## What the PMM is not

- **Not a probability of default.** The PMM has no direct relationship to credit
  default probability. Use the reserve_coverage_months trajectory and the MDA
  breach pattern for default-adjacent arguments.

- **Not a ranking.** The PMM is scenario-specific. A PMM of 0.65 in a JOR scenario
  cannot be compared to a PMM of 0.65 in a GRC scenario — the component values are
  not cross-country normalized in the pre-calibration phase.

- **Not a recommendation.** The PMM summarizes the current trajectory. It does not
  recommend what action to take. Use Mode 2 (Simulation) to explore how different
  policy inputs change the PMM trajectory.

---

## When the PMM annotation will change

The `[T3 composite · pre-cal]` annotation will be updated when:

1. ADR-007 (PMM calibration) is accepted by the full ADR panel
2. The PMM has been backtested against at least two historical sovereign stress
   episodes (per ADR-007 §backtesting requirement)
3. The component weights have been reviewed and accepted by the Chief Methodologist
4. The external validation process (M14 TSC formation) has reviewed the methodology

Until all four conditions are met, the annotation remains `pre-cal`. The Finance
Ministry analyst can treat this as: "This PMM is calibrated enough to use for
directional analysis in this session, but not calibrated enough to cite externally
without the caveat that it is a pre-calibration model estimate."

---

## How to navigate from this anchor to the confidence tier system

For a full explanation of what T1–T5 means and which indicators carry which tiers,
see [Confidence Tier Assignment Methodology](confidence-tier-assignment-methodology.md).

For the PMM annotation format in Zone 1C and the L0 annotation system:
see ADR-015 §Component 1 and the G5 intent document at
`docs/process/intents/M14-G5-2026-06-17-adr015-frontend.md`.

For the political economy module that contributes the feasibility component:
see ADR-013 and the calibration basis documentation at
`docs/methodology/calibration-basis.md` (filed under M13 G8a).

---

*PMM Interpretation Anchor — M14 calibration documentation.*
*Authored by Chief Methodologist Agent for M14 G6 — PMM anchor deliverable.*
*Status: pre-calibration. ADR-007 target: M15–M16.*
*Document version: 2026-06-18.*
