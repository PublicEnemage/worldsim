---
name: m17-g1-governance-sensitivity-specification
type: calibration-specification
issue: "#1248"
sprint: M17-G1
status: FILED — Wave 1 specification deliverable; closes AC-4 gate
authored-by: Chief Methodologist
authored-date: 2026-06-25
intent-document: docs/process/intents/M17-G1-2026-06-25-cm-calibration.md
implements: docs/process/sprint-plans/m17-g1-sprint-entry.md §Section 3.1 (#1248)
---

# CM Governance Sensitivity Specification — M17-G1

> **Authority:** This document is the Wave 1 specification deliverable for #1248. It answers
> the three open questions identified in the M16-G8 governance calibration gap (insights log
> entry 11, promoted 2026-06-24 to #1248). It satisfies AC-4 of the M17-G1 intent document.
>
> **Scope of this document:** Position statements on three diagnostic questions about the
> GovernanceModule's response to fiscal conditionality in the Senegal Article IV scenario.
> This document does not change any GovernanceModule code — that is Wave 2 scope, gated on
> the PI Agent's Wave 1 exit gate confirmation. It provides the CM's citable position on
> whether Wave 2 code changes are warranted, and if so, what form they should take.
>
> **The observed gap:** In the Demo 6 Senegal 8-step scenario, the governance composite
> (GOV) remains approximately 0.51 across all 8 steps while the financial composite (FIN)
> declines from 0.56 to 0.51. The near-zero governance response to IMF fiscal conditionality
> prompted this diagnostic review.

---

## Background: Current GovernanceModule Architecture

The GovernanceModule (`app/simulation/modules/governance/`) processes events via
`GOVERNANCE_ELASTICITY_REGISTRY` (three entries as of M16 close):

| Event type | Indicator key | Elasticity | Tier | Source |
|---|---|---|---|---|
| `gdp_growth_change` | `rule_of_law_percentile` | −0.08 | T2 | Haggard & Kaufman (2016) |
| `emergency_policy_imf_program_acceptance` | `democratic_quality_score` | +0.005 | T3 | Grabel (2017), IMF IEO (2018) |
| `emergency_policy_emergency_declaration` | `democratic_quality_score` | −0.05 | T3 | Bermeo (2016) |

In the Senegal Article IV scenario (8-step quarterly resolution, fiscal spending cut −3%
GDP, `imf_program_acceptance` at step 1):

- `gdp_growth_change` arrives at GovernanceModule with magnitude −0.015. Per-step
  `rule_of_law_percentile` delta: −0.015 × −0.08 = **+0.0012** per step (rule of law
  deteriorating = positive delta in the inverse-scale encoding). Over 8 steps: **+0.0096**
  total. WGI `rule_of_law_percentile` is encoded 0–100; a 0.01pp change is below visual
  resolution in Zone 1A even with adaptive y-axis scaling.

- `emergency_policy_imf_program_acceptance` emits with magnitude +1.0. `democratic_quality_score`
  delta: +1.0 × +0.005 = **+0.005** (one-step, not cumulative). This is similarly small.

The GOV composite therefore barely moves because (a) the per-step GDP → rule_of_law signal
at −0.015 shock magnitude is small by calibrated design, and (b) the IMF acceptance
pathway captures democratic quality at a modest T3 level. This raises three diagnostic
questions answered below.

---

## Question 1: Does `imf_program_acceptance` have a direct governance transmission pathway distinct from the GDP channel?

### Background

The event `imf_program_acceptance` (as a binary signal at step 1) is already processed by
the GovernanceModule via `emergency_policy_imf_program_acceptance`. This entry captures the
net governance conditionality clause effect on `democratic_quality_score` (Grabel 2017;
IMF IEO 2018). The question is whether there is an additional direct transmission from
the programme acceptance signal to `rule_of_law_percentile` — a channel distinct from
both the democratic quality entry and the GDP-mediated rule-of-law deterioration.

### Evidence review

**For a direct pathway:** IMF conditionality clauses in SSA Article IV programmes
(post-2012) routinely include anti-corruption benchmarks, statistical reporting reform,
and public financial management requirements. Coppedge et al. (V-Dem v13, 2023) show
that compliance with IMF governance conditionality clauses is associated with short-run
(1–2 year) improvements in `rule_of_law_percentile` in some SSA programmes — particularly
where the conditionality targets judiciary and audit institution reform.

**Against a direct pathway at quarterly resolution:** Bird and Rowlands (2017) find
that the post-acceptance governance effect is highly heterogeneous: it is positive where
conditionality is fully implemented but negative where governments use emergency executive
powers to achieve fiscal consolidation targets. At quarterly resolution, the programme
acceptance event represents the announcement moment — before conditionality implementation
has had measurable institutional effect. The WGI `rule_of_law_percentile` is itself
observed annually and published with an 18-month lag; a quarterly-resolution elasticity
for this annual indicator is necessarily synthetic.

**Double-counting risk:** In the Senegal Article IV scenario, `imf_program_acceptance`
is accompanied by `fiscal_policy_spending_change` events that travel through the GDP
multiplier chain to `gdp_growth_change`, which then drives the existing
`gdp_growth_change` → `rule_of_law_percentile` entry. Adding a direct acceptance →
rule_of_law path risks capturing the same fiscal conditionality effect twice.

### CM position

**CM position: NO — no new direct `imf_program_acceptance` → `rule_of_law_percentile`
entry is recommended.** The existing `emergency_policy_imf_program_acceptance` →
`democratic_quality_score` entry correctly captures the governance conditionality signal
at T3 precision. A second direct pathway to `rule_of_law_percentile` would double-count
the fiscal conditionality effect and is not supported by annual-frequency WGI data at
quarterly resolution. The current architecture is **working as designed**; the near-zero
programme acceptance effect on governance is an accurate representation of the short-run
uncertainty at T3 confidence.

**Wave 2 implication:** No new code entry warranted. This question is closed.

---

## Question 2: Does institutional capacity degradation under austerity have an empirically defensible elasticity for the GovernanceModule?

### Background

The M16-G8 finding (insights log entry 11) noted that GovernanceModule does not capture
institutional capacity degradation under austerity — specifically, the deterioration of
public service delivery capacity (education ministry staffing, health infrastructure
maintenance, statistical office capacity) as social spending is cut. This is distinct from
`rule_of_law_percentile` (which captures judicial and regulatory institutions) and from
`democratic_quality_score` (which captures political freedom indicators).

The diagnostic question is whether a `fiscal_policy_spending_change` →
`institutional_capacity_index` direct pathway is empirically defensible.

### Evidence review

**Relevant sources:**

Gupta, S., Clements, B., Baldacci, E., and Mulas-Granados, C. (2002). "Expenditure
Composition, Fiscal Adjustment, and Growth in Low-Income Countries." IMF Working Paper
WP/02/77. Documents that social spending cuts reduce service delivery capacity in LICs with
a 2–4 year implementation lag. Does not provide a specific elasticity for a quarterly-step
framework, but suggests that visible institutional capacity loss is a 8–16 step signal
at quarterly resolution.

Baldacci, E., Clements, B., Gupta, S., and Cui, Q. (2008). "Social Spending, Human Capital,
and Growth in Developing Countries." World Development 36(8): 1317–1341. Confirms the 2–4
year transmission for education and health institutional capacity; no elasticity for rule
of law or governance composite indicators.

**Key constraint:** WorldSim does not currently seed `institutional_capacity_index` for
SEN. The attribute is not in the SEN entity attributes (verified: `_SYNTHETIC_SEN_ATTRIBUTES`
in the backtesting fixture does not include `institutional_capacity_index`). A new
GovernanceElasticity entry referencing `institutional_capacity_index` as the indicator_key
would silently do nothing until the indicator is seeded — producing the classic "silent
failure" mode where the entry appears in the registry but the GovernanceModule
cannot compute because the target attribute is absent from the entity state.

### CM position

**CM position: YES in principle — but a Wave 2 entry is conditional on data work.**
An elasticity for `fiscal_policy_spending_change` → `institutional_capacity_index`
at T3 confidence is empirically defensible based on Gupta et al. (2002) and Baldacci et
al. (2008). A defensible point estimate for SSA LICs is approximately −0.015 per 1pp
fiscal spending change (Gupta 2002 Table 3, scaled to quarterly resolution and the
0–1 institutional capacity index range).

**However:** The Wave 2 implementation gate requires that `institutional_capacity_index`
be seeded for SEN before the GovernanceElasticity entry is added. The recommended
sequencing is:

1. Data work: seed `institutional_capacity_index` for SEN (source: World Bank CPIA 2023,
   T2 for Senegal's 3.3/6 score normalized to [0, 1] = 0.55; or T3 synthetic from
   ECOWAS regional average ≈ 0.50)
2. GovernanceElasticity entry: `fiscal_policy_spending_change` → `institutional_capacity_index`,
   elasticity = Decimal("−0.015"), T3, source: Gupta et al. (2002)

This sequencing prevents the silent failure mode. The data seeding and GovernanceElasticity
entry should be co-committed in the same Wave 2 PR. An entry without the seeded indicator
is a process deviation equivalent to an elasticity entry for an unregistered source.

**Wave 2 implication:** FILE a Wave 2 issue for: (1) seed SEN `institutional_capacity_index`
(World Bank CPIA 2023, T2); (2) add GovernanceElasticity entry for
`fiscal_policy_spending_change` → `institutional_capacity_index` at −0.015, T3, Gupta (2002).
The Wave 2 sprint entry must specify both data seeding and elasticity entry as co-gated
deliverables.

---

## Question 3: Is the 8-step quarterly window sufficient to manifest visible governance divergence in Zone 1A?

### Background

The GOV composite in Demo 6 remains approximately flat across 8 steps while FIN declines
visibly. The question is whether this reflects (a) an under-calibrated GovernanceModule
that should respond more strongly to short-run fiscal conditionality, or (b) a correctly
calibrated model where governance divergence is genuinely a longer-horizon signal at
quarterly resolution.

### Evidence review

**WGI temporal structure:** The World Governance Indicators — the T2 source for
`rule_of_law_percentile` — are published annually with 18-month publication lag and
are themselves composite estimates with uncertainty bounds of ±15–20 percentile points.
A quarterly simulation step represents a 3-month period; WGI cannot meaningfully
distinguish governance changes at this granularity. The existing GDP → rule_of_law
elasticity (−0.08, T2, Haggard & Kaufman 2016) was calibrated for annual-resolution
data and applied to quarterly steps under the assumption that annual effects are spread
uniformly across four quarters — a conservative approximation.

**IMF programme case studies (SSA):** Examining Senegal's own programme history (IMF ECF
2015, 2019, 2023), V-Dem Liberal Democracy Index and WGI Rule of Law show measurable
change on 3–5 year horizons, not 8-quarter windows. The Greece backtesting fixture
(2010–2015) shows governance deterioration over 20 steps, not 8. Structural governance
responses to fiscal consolidation are inherently medium-horizon signals.

**The design implication:** Attempting to engineer visible 8-step governance divergence
by revising the GDP → rule_of_law elasticity upward would require an elasticity that
is not supported by the annual-frequency WGI literature at T2, and would misrepresent
the speed of governance response to fiscal adjustment. The correct response to the
observation that governance barely moves in 8 steps is to document it as an intentional
model characteristic, not to manufacture a larger short-run response.

### CM position

**CM position: The 8-step window is insufficient to manifest visible governance
divergence, and this is working as designed.** Governance indicators measured at annual
frequency with 18-month publication lag cannot produce quarterly-resolution divergence
within 8 steps from a calibrated T2 source. The GOV composite remaining near-flat across
8 steps in the Senegal Article IV scenario is the correct model output for a T3 synthetic
baseline with T2-calibrated elasticities.

**The appropriate response is a transparency disclosure, not a recalibration:**

1. Zone 1D (or the current attestation section) should explicitly state that governance
   composite divergence is a 12–24 step (3–6 year) signal in this model's quarterly
   resolution — not an 8-step observable.
2. The Demo 6/Demo 7 walkthrough narrative (`docs/demo/`) should acknowledge this
   explicitly: "The governance composite remains stable in the 8-step window. Governance
   deterioration under fiscal consolidation is a medium-horizon (3–5 year) signal — the
   IMF programme's governance impact would be visible in a 24-step analysis."

This is consistent with the platform principle: **No False Precision**. Manufacturing an
8-step governance response that WGI data cannot support would be false precision. The
honest answer is that the tool captures governance risk correctly at the horizon where
the data supports it.

**Wave 2 implication:** FILE a Wave 2 documentation issue for Zone 1D / tooltip text
clarifying that governance divergence is a ≥12-step signal at quarterly resolution.
No GovernanceElasticity code change is warranted for this question.

---

## Summary: Wave 2 Action Items from This Specification

| Question | CM position | Wave 2 action |
|---|---|---|
| Q1: Direct `imf_program_acceptance` pathway | WORKING-AS-DESIGNED — no new entry | None |
| Q2: Institutional capacity degradation elasticity | YES in principle — conditional on data | FILE issue: seed SEN `institutional_capacity_index` + GovernanceElasticity entry, co-gated |
| Q3: 8-step window sufficiency | WORKING-AS-DESIGNED — transparency disclosure needed | FILE issue: Zone 1D / tooltip text — governance divergence is ≥12-step signal |

**Wave 2 issues to file at next HORIZON sweep (PM Agent):**

- **G2-or-later: SEN `institutional_capacity_index` seed + GovernanceElasticity entry**
  Source: World Bank CPIA 2023 for SEN (T2, 3.3/6 = 0.55 normalized); entry:
  `fiscal_policy_spending_change` → `institutional_capacity_index`, elasticity −0.015, T3,
  Gupta et al. (2002) WP/02/77. Must be co-gated: data seeding and elasticity entry in same PR.

- **G4-or-later (documentation): Zone 1D tooltip — governance horizon disclosure**
  Text: "Governance indicators (rule of law, democratic quality) respond to fiscal
  adjustment over 3–6 year horizons in this model's calibration. An 8-step quarterly
  window captures the beginning of the governance stress trajectory; full divergence
  requires a 12–24 step analysis."

---

## What This Specification Does and Does Not Claim

**Claims:**
- The current GovernanceModule architecture is correctly calibrated for the signals it
  can reliably represent at quarterly resolution with T2/T3 sources
- Q1 (imf_program_acceptance direct pathway) is closed — no new code entry warranted
- Q2 (institutional capacity) is open for Wave 2 subject to data preconditions being met
- Q3 (8-step window) is closed with a transparency disclosure recommendation

**Does not claim:**
- That the governance composite is well-calibrated for all scenarios at all horizons
- That `institutional_capacity_index` should not be added — it should be, but with proper
  data seeding and sequencing
- That the Wave 2 institutional capacity entry's elasticity (−0.015) is backtested against
  Senegal-specific data — it is T3 regionally inferred from Gupta (2002)

---

*CM authority: Chief Methodologist. Issue: #1248. Sprint: M17-G1.
Intent document: `docs/process/intents/M17-G1-2026-06-25-cm-calibration.md §3.2 State C`.
This document satisfies AC-4: three questions answered with explicit CM position lines.
Wave 2 code changes require a Wave 2 sprint entry — this specification document is the
Wave 1 deliverable only.*
