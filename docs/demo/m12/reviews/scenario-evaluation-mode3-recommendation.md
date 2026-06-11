# Mode 3 Demo Scenario — Panel Recommendation

**Panel:** Development Economist Agent · Chief Methodologist Agent
**Date:** 2026-06-10
**Full deliberation:** `scenario-evaluation-mode3-deliberation.md`

---

## Recommendation

**Retain the current fixture unchanged. Branch from step 3 at fiscal_multiplier=1.30.**

No modifications to `backend/tests/fixtures/jordan_hormuz_scenario.py` are required or recommended.

---

## Rationale

The five options were evaluated against live simulation output. The current fixture (GCC +0.06 at step 3; austerity -0.03 at step 4, duration 2; branch anchor at 1.30×) is the correct design.

**Why the current fixture works:**

The Mode 3 divergence is produced by two overlapping mechanisms that peak at different steps:

| Step | Baseline JOR GDP | Branch JOR GDP (estimated) | Divergence | Mechanism |
|------|-----------------|--------------------------|------------|-----------|
| 4 | +4.92% | ~+5.60% | ~+0.68pp | 1.30× GCC multiplier (0.06 × 0.30 × 0.5 × 0.75) |
| 5 | +3.60% | ~+5.30% | ~+1.70pp | Austerity absent from branch (−0.03 × 0.5 × 0.75 = −1.125pp removed) |
| 6–8 | declining | sustained | >1pp | No conditionality drag in branch |

**The primary divergence driver is austerity removal, not multiplier amplification.** The 1.30× multiplier adds ~+0.68pp at step 4; the absence of IMF conditionality adds ~+1.70pp at step 5 and compounds onward. The demo narrative should center on this: the minister's leverage is not in securing more GCC money — it is in negotiating the conditionality terms.

**Why the alternatives were rejected:**

- **Option A (GCC at step 2):** Moving GCC to step 2 requires branching at step 2, which removes the IMF program acceptance from the branch. The counterfactual becomes "avoid the IMF entirely" rather than "negotiate better terms" — a different and less realistic scenario for the demo audience.
- **Option B (GCC +0.10):** Simulates a 1.67× GCC package, not a 1.30× multiplier. The fixture value (+0.10) and the fiscal_multiplier parameter (1.30×) are not equivalent — they test different variables. The 0.10 fixture makes the demo tell a different story ("larger package") when the platform can already tell the correct story ("better implementation efficiency") via the multiplier parameter.
- **Option D (double austerity):** Confirms that stronger conditionality (doubled austerity to -0.06 effective) deepens the baseline damage (step 5 GDP +2.48% vs +3.60%) and would increase the branch/baseline divergence to >2.8pp. But duplicating the austerity input without a political economy justification introduces a model complexity that would require explanation during the demo. The effect can be narrated verbally — "this is what IMF conditionality costs" — without engineering a harder-to-explain fixture.
- **Option E (Egypt as primary):** Egypt has no scheduled fiscal inputs; its GDP trajectory is monotonically increasing across all eight steps. There is no policy decision moment in Egypt's path. Mode 3 is not viable with Egypt as the primary entity.
- **Option C (debt rescheduling):** No reserve-injecting or debt-rescheduling instrument exists in the current engine. EmergencyInstrument operates through the governance channel only. Implementing Option C would require an ADR.

---

## Expected Zone 1A Divergence Pattern

The demo analyst should advance to at least step 5 before making the branch comparison claim. Step 4 shows meaningful but smaller divergence (+0.68pp GDP); step 5 shows the full divergence including conditionality removal (~+1.70pp GDP).

Expected unemployment trajectory (most legible human cost signal):

| Step | Baseline JOR Unemp | Branch JOR Unemp (estimated) | Divergence |
|------|-------------------|------------------------------|------------|
| 4 | 16.59% | ~16.25% | ~−0.34pp |
| 5 | 17.25% | ~16.40% | ~−0.85pp |
| 6–8 | 17.28–17.33% | declining | widening |

The unemployment reversal at step 5 in the baseline (16.59% → 17.25%) is the most important visual signal. The branch curve should continue declining while the baseline curve rises. This is the human cost story: the GCC-supported recovery is undone by conditionality within one step, but the branch sustains the improvement.

**Composite score shift (financial, percentile rank):** At step 5, baseline JOR GDP (+3.60%) is barely above EGY GDP (+3.56%) — financial composite near 0.5. Branch JOR GDP (~+5.30%) is substantially above EGY GDP (+3.56%) — financial composite should shift materially above 0.5. This is the composite score divergence visible in Zone 1A.

---

## Mandatory Demo Caveat

Reserve depletion is identical in both baseline and branch:

```
Both: 7.1 → 6.2 → 5.0 → 3.7 → 2.5 → 1.2 → 0.0 → 0.0 months
```

MDA reserve alerts fire at the same steps with the same severity in both trajectories. Better conditionality negotiation improves GDP and unemployment outcomes; it does not change Jordan's structural import dependency during the Hormuz disruption. The demo analyst must state this explicitly when presenting the comparison. The reserve crisis trajectory is not solved — it is survived under better internal conditions.

This is not a limitation of the demo. It is the honest answer to the question the demo is asking.
