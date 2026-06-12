# ADR-013 Panel Review — Political Economy Module Boundary

**ADR:** ADR-013-political-economy-module-boundary.md
**Review date:** 2026-06-12
**Panel:** Architect Agent (R), Political Economist (C), Chief Methodologist (C), Engineering Lead (A)
**Status:** APPROVED — pending Engineering Lead acceptance vote

---

## Architect Agent — Authorship Review

The ADR is complete per the template requirements. Four decisions cover the module boundary
with sufficient precision for G6 implementation to proceed without further clarification.
Interface contracts name indicator keys, types, confidence tiers, and MDA trigger conditions.

One deliberate deferral: political economy composite score appears in the trajectory API but
not in Zone 1D. This is correctly deferred — adding a fifth Zone 1D row requires a layout
review that is out of scope for the module boundary ADR.

Open obligation for Zone 1D integration is tracked in Issue #392.

**Architect sign-off:** Confirmed complete per Phase 0 template. 2026-06-12.

---

## Political Economist — Domain Review

### Programme Survival Probability Formula

The existing formula (calibrated on Greece, Argentina, Ecuador) is an honest approximation
but with a known limitation: all three cases are middle-income countries with multi-year IMF
programme histories. Low-income country programme failure dynamics — where bilateral donor
relationships and food security shocks drive failure modes distinct from fiscal consolidation
fatigue — are not captured.

**Required addition:** The Consequences → Known Limitations section should explicitly name the
low-income country calibration gap. ✓ (Already present in the ADR as filed — confirmed.)

**Recommendation on PROGRAMME_SURVIVAL_FLOOR:** 0.25 is calibrated from historical data.
For middle-income countries, this floor is defensible. For low-income entities, the floor
may be lower (programmes survive at lower legitimacy levels due to donor dependency). The ADR
correctly constrains the floor to 0.25 and requires an ADR amendment to change it — this is
the right governance approach.

### Elite Capture Coefficient

The scalar-per-entity design is a known simplification. Elite capture dynamics are step-varying
in reality (elite capture intensifies during fiscal stress). The ADR documents this as a known
limitation. Acceptable for M13.

### Conditionality Attribution Scope

Decision 2 correctly limits attribution to `InputSource.CONDITIONALITY` inputs. The constraint
(no decomposer call when conditionality_inputs == []) is the right boundary. Attribution for
non-conditionality inputs is analytically incorrect — those inputs represent the entity's own
policy choices, not externally imposed constraints.

**Political Economist position:** APPROVED. The analytical approach is honest about its
approximation quality and documents limitations transparently.

---

## Chief Methodologist — Statistical Integrity Review

### Confidence Tier Assignment

All three political economy outputs are assigned Tier 3 (SYNTHETIC_COMPARABLE). This is correct:
- Programme survival probability: formula-calibrated from 3 cases. Tier 3 is the correct
  assignment — not Tier 2, which requires statistical validation against a held-out dataset.
  Until Issue #44 calibration is complete, Tier 3 must be maintained.
- Conditionality attribution: inherits from fiscal_balance input tier. Inheriting the donor
  tier is the correct approach — the attribution chain is only as strong as the input data.
- Elite capture divergence: structural estimate from entity attributes. Tier 3 is correct.

**Required disclosure review:** The ADR specifies that "synthetic" must appear verbatim in
confidence tier disclosures. This satisfies the IA-1 disclosure requirement. Confirmed.

### Composite Score Formula (Decision 4)

The arithmetic mean of three inputs with different value ranges and measurement semantics is
statistically problematic. The three inputs are:
1. Programme survival probability [0.0, 1.0] — probability
2. Elite capture normalised [0.0, 1.0] — structural ratio
3. Governance-normalised legitimacy index [0.0, 1.0] — subjective estimate

Averaging these produces a composite whose meaning is not anchored to any observable.
The ADR correctly names this as "architectural placeholder" (Decision 4) and does not surface
it in Zone 1D. The limitation is documented.

**Required addition to ADR:** The composite score formula must be explicitly flagged as
"pre-calibration formula" in the methodology documentation, not presented as a validated
aggregate. The phrase "calibrated composite" must not be used until Issue #44 is complete.
✓ The ADR language ("architectural placeholder") satisfies this requirement.

**Chief Methodologist position:** APPROVED with the following condition: before G6 implementation,
`docs/methodology/calibration-basis.md` must be updated to document the political economy
module calibration basis (formula sources for programme survival, elite capture structural
estimate source, low-income country calibration gap). This update is a pre-implementation
requirement, not a post-implementation task.

---

## Summary of Panel Findings

| Finding | Severity | Status |
|---|---|---|
| Low-income country calibration gap documented | Informational | ✓ In ADR Known Limitations |
| Composite score named as architectural placeholder, not validated aggregate | Required | ✓ In ADR Decision 4 |
| "synthetic" verbatim in tier disclosures | Required | ✓ In ADR UX-5 |
| `docs/methodology/calibration-basis.md` update required before G6 | Blocking pre-G6 | Open — tracked here |
| Zone 1D deferral documented with open obligation | Required | ✓ In ADR Decision 4 and Issue #392 |

---

## Panel Vote

| Panel Member | Vote | Date |
|---|---|---|
| Architect Agent | APPROVE | 2026-06-12 |
| Political Economist | APPROVE | 2026-06-12 |
| Chief Methodologist | APPROVE (conditional — calibration-basis.md update before G6) | 2026-06-12 |
| Engineering Lead | **PENDING** | — |

**ADR status:** Remains `Proposed` until Engineering Lead vote is recorded.
