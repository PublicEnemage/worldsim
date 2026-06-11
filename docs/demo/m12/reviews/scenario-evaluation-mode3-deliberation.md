# Mode 3 Demo Scenario Evaluation — Two-Agent Deliberation

**Panel:** Development Economist Agent · Chief Methodologist Agent
**Scenario under evaluation:** Jordan/Egypt Strait of Hormuz Disruption (Demo 4, M12)
**Mode 3 question:** Which branch configuration (option, step, multiplier) produces the most analytically sound and perceptually visible trajectory divergence for the demo?
**Date:** 2026-06-10
**Method:** All five options evaluated against live simulation output, not model assumptions.

---

## Simulation Runs — Observed Output

All four runs conducted against the live database. Fixture reverted after each run. No changes committed.

### Baseline (GCC +0.06 at step 3; austerity -0.03 at step 4, duration 2)

Jordan (JOR):

| Step | Year | GDP Growth | Unemployment | Reserves |
|------|------|------------|--------------|----------|
| 1 | 2024 | +2.55% | 17.77% | 7.1mo |
| 2 | 2025 | +2.60% | 17.75% | 6.2mo |
| 3 | 2026 | +2.64% | 17.73% | 5.0mo |
| 4 | 2027 | +4.92% | 16.59% | 3.7mo |
| 5 | 2028 | +3.60% | 17.25% | 2.5mo |
| 6 | 2029 | +3.54% | 17.28% | 1.2mo |
| 7 | 2030 | +3.49% | 17.31% | 0.0mo |
| 8 | 2031 | +3.44% | 17.33% | 0.0mo |

Egypt (EGY): +3.06%, +3.20%, +3.33%, +3.45%, +3.56%, +3.65%, +3.73%, +3.81% (GDP); unchanged across all option runs.

**Structural observation:** Step 4 jump of +2.28pp is the GCC one-step lag. Step 5 drop of -1.32pp is the austerity one-step lag. Reserves drain is ExternalSectorModule-only — identical across all variants.

---

### Option A — GCC moved from step 3 to step 2 (value +0.06 unchanged)

Jordan (JOR):

| Step | Year | GDP Growth | Unemployment | Reserves |
|------|------|------------|--------------|----------|
| 1 | 2024 | +2.55% | 17.77% | 7.1mo |
| 2 | 2025 | +2.60% | 17.75% | 6.2mo |
| 3 | 2026 | +4.89% | 16.61% | 5.0mo |
| 4 | 2027 | +4.70% | 16.70% | 3.7mo |
| 5 | 2028 | +3.40% | 17.35% | 2.5mo |
| 6 | 2029 | +3.36% | 17.37% | 1.2mo |
| 7 | 2030 | +3.33% | 17.39% | 0.0mo |
| 8 | 2031 | +3.29% | 17.40% | 0.0mo |

**Structural observation:** GCC fires at step 2 → GDP boost appears at step 3 (+4.89%), one step earlier. But the boost has faded by step 4 (+4.70%, vs baseline's +4.92% at step 4 from GCC at step 3). Austerity at step 4 still fires, producing step 5 drag. Critically: branching at step 2 in Mode 3 removes the IMF program acceptance (step 3) as well as the austerity (step 4) from the branch — this changes the scenario meaning from "avoid conditionality while keeping IMF relationship" to "avoid the IMF entirely." Narratively more complex. End-state GDP at step 8 (+3.29%) is lower than baseline (+3.44%) because GCC support arrived at a less leveraged moment.

---

### Option B — GCC value increased to +0.10 at step 3 (higher multiplier simulation)

Jordan (JOR):

| Step | Year | GDP Growth | Unemployment | Reserves |
|------|------|------------|--------------|----------|
| 1 | 2024 | +2.55% | 17.77% | 7.1mo |
| 2 | 2025 | +2.60% | 17.75% | 6.2mo |
| 3 | 2026 | +2.64% | 17.73% | 5.0mo |
| 4 | 2027 | +6.42% | 15.84% | 3.7mo |
| 5 | 2028 | +4.95% | 16.57% | 2.5mo |
| 6 | 2029 | +4.76% | 16.67% | 1.2mo |
| 7 | 2030 | +4.58% | 16.76% | 0.0mo |
| 8 | 2031 | +4.43% | 16.84% | 0.0mo |

**Structural observation:** Step 4 GDP at +6.42% (+1.50pp over baseline) — exactly matching formula: (0.10-0.06) × 0.5 (fiscal multiplier) × 0.75 (political feasibility) = 1.50pp. Unemployment improvement at step 4: 15.84% (vs 16.59% baseline) — 0.75pp better via Okun's law (1.50pp × 0.5 coefficient). Both improvements persist through steps 5-8. Reserves are completely unchanged — confirming reserves are decoupled from fiscal policy. This option represents what a much larger GCC package would produce (≈1.67× the baseline GCC value), not the 1.30× branch tested in the demo.

---

### Option D — Double austerity baseline (+GCC +0.06 at step 3; two spending_change -0.03 at step 4)

Jordan (JOR):

| Step | Year | GDP Growth | Unemployment | Reserves |
|------|------|------------|--------------|----------|
| 1 | 2024 | +2.55% | 17.77% | 7.1mo |
| 2 | 2025 | +2.60% | 17.75% | 6.2mo |
| 3 | 2026 | +2.64% | 17.73% | 5.0mo |
| 4 | 2027 | +4.92% | 16.59% | 3.7mo |
| 5 | 2028 | +2.48% | 17.81% | 2.5mo |
| 6 | 2029 | +2.53% | 17.78% | 1.2mo |
| 7 | 2030 | +2.58% | 17.76% | 0.0mo |
| 8 | 2031 | +2.62% | 17.74% | 0.0mo |

**Structural observation:** Step 5 GDP drops to +2.48% (from +4.92% at step 4), a -2.44pp fall vs the baseline's -1.32pp fall. The additional -1.12pp drop is exactly the additional austerity effect (0.03 × 0.5 × 0.75 = 1.125pp). Step 4 is IDENTICAL to baseline because both austerity inputs fire at step 4 and the lag means the double effect only appears at step 5. Unemployment at step 5: +17.81% (worse than baseline's +17.25% and even worse than step 3's +17.73%, meaning the GCC's unemployment improvement has been completely reversed and then some). Mode 3 branch from step 3 on this baseline would remove both austerity inputs, yielding projected step 5 GDP of ~+5.3% vs baseline step 5 of +2.48% — a >2.8pp divergence.

---

## Deliberation

**Development Economist Agent:** I want to begin with the human cost ledger before the demo mechanics. In the baseline, Jordan's unemployment at step 5 (17.25%) is 0.66pp worse than at step 4 (16.59%), after the GCC support had actually improved things. The IMF conditionality fires at the worst possible moment — peak external shock, exhausted reserves — and the benefit from the GCC support is partially undone within one step. That is the analytically honest story: bilateral support and multilateral conditionality arrive simultaneously, and the conditionality claws back what the bilateral support gave.

The Mode 3 branch that removes austerity while keeping 1.30× GCC produces a qualitatively different path: unemployment continues improving from step 4 onward instead of reversing. That is what needs to be visible in Zone 1A. If the trajectory curves show unemployment dipping at step 4 and then immediately rising at step 5 in the baseline, but continuing to fall in the branch, that is the substantive argument about what conditionality costs.

**Chief Methodologist Agent:** Let me be precise about what the runs tell us and what they don't. The reserve depletion is invariant across all variants — 7.1→6.2→5.0→3.7→2.5→1.2→0→0 months — because the ExternalSectorModule drives reserves independently of fiscal policy. This is not a limitation to apologize for; it is a methodologically correct representation of the constraint. No amount of GCC support or avoided conditionality changes Jordan's import dependency during a live Hormuz disruption. That is the honest finding.

What fiscal policy can change is GDP growth and unemployment — the internal absorption capacity of the economy. And the runs confirm that the model transmits these correctly and transparently. The Option B run shows exactly 1.50pp additional GDP at step 4, which is (0.10−0.06) × 0.5 × 0.75 = 0.015 = 1.50pp. The Option D run shows exactly -1.125pp additional GDP drag at step 5 from the second austerity input, which is 0.03 × 0.5 × 0.75 = 1.125pp. The model is behaving exactly as it should.

**Development Economist Agent:** On Option A — moving GCC to step 2. I initially thought this might be interesting because it shows aid arriving before the IMF enters, giving Jordan more room to negotiate from step 3 onward. But the simulation reveals a structural problem with this as a Mode 3 demo: branching at step 2 removes the IMF program from the branch entirely (IMF fires at step 3 > branch_from_step=2). The branch then becomes "what if Jordan avoided the IMF completely?" rather than "what if Jordan negotiated a better IMF deal?" The former is a different and less realistic counterfactual for a finance minister sitting at that table. You cannot branch to avoid the IMF if you're already in the negotiating room.

**Chief Methodologist Agent:** Agreed. The branch_from_step determines which scheduled_inputs survive into the branch, and the branch story must be narratively coherent with what a minister can actually do. At step 3, the minister is responding to the crisis peak. The branch from step 3 copies: ExternalSectorModule shocks (steps 1-6), IMF program acceptance (step 3), GCC support (step 3) — but does NOT copy the austerity conditionality (step 4). This represents "Jordan accepts IMF emergency support for liquidity, negotiates successfully on fiscal conditionality terms." That is a plausible, specific scenario a minister can narrate.

Branching at step 2 removes too many events. The counterfactual becomes uninterpretable for demonstration purposes.

**Development Economist Agent:** On Option B — the higher GCC value. The run produced step 4 GDP at +6.42% and unemployment at 15.84%. These are real improvements — 1.89pp unemployment improvement vs 1.14pp in the baseline. From a human development standpoint, 0.75pp better unemployment represents real lives. But I want to flag something: the step 5 unemployment in Option B is 16.57%, still worse than step 4 (15.84%). The austerity effect still fires, still claws back the gains. The mode 3 demo with Option B as the branch would show: more GCC AND no austerity, with a more dramatic baseline GDP at step 4 from the larger GCC. But the 1.30× fiscal_multiplier on a 0.06 baseline value only produces 0.078 effective GCC — the UI demo already tests this at the right scale. Testing 0.10 is testing a different scenario (67% larger GCC package), not the 1.30× amplification.

**Chief Methodologist Agent:** This is the critical distinction. Option B as a fixture modification tests a 1.67× GCC scenario (0.10/0.06). The Mode 3 branch with fiscal_multiplier=1.30 tests 1.30× on the 0.06 base = 0.078 effective GCC. The branch parameter and the fixture value serve different analytical functions. Changing the fixture to 0.10 makes the demo tell a different story: "Jordan secured a much larger absolute GCC package" rather than "the same GCC package went further because Jordan improved implementation capacity." The multiplier framing is more analytically precise — it maps to real-world concepts like fiscal absorption capacity and implementation efficiency under stress, which are legitimate bargaining variables for a finance minister.

**Development Economist Agent:** On Option D — the double-austerity baseline. I want to be direct: this is the most analytically interesting finding from these runs. Step 5 GDP at +2.48% with double austerity, vs +3.60% with single austerity, vs projected ~+5.3% in the branch — that is a 2.82pp spread. The zone 1A trajectory curve would show a sharp "V" in the baseline (up at step 4 from GCC, down sharply at step 5 from double austerity) vs a smoothly elevated branch curve. That is visually compelling.

But the narrative problem is real. Why would the IMF demand twice the fiscal adjustment? The baseline scenario already has -0.03 spending cut at step 4, duration 2. Adding a second identical input doubles conditionality without a political economy justification. A finance minister observing this demo would immediately ask: "why does the baseline have two austerity inputs?"

**Chief Methodologist Agent:** Option D also introduces a model complexity that could be confusing in a demo context. The two inputs add linearly at step 4 — which is correct model behavior — but explaining to a demo audience that the baseline has two separate -0.03 spending changes when the GCC support is one +0.06 change creates an asymmetry of presentation. The analyst needs to explain why the model has two inputs for one concept.

The right approach, if we wanted a stronger baseline/branch contrast, would be to make the single austerity input more severe (-0.05 or -0.07) rather than duplicating it. But that is a fixture redesign, not an investigative run.

**Development Economist Agent:** On Option E (Egypt as primary entity) — we did not run this because the Egypt trajectory is unchanged across all variants (EGY has no scheduled fiscal inputs in the fixture). Egypt's GDP grows monotonically at +3.06% to +3.81% across all eight steps. The drama in this scenario is Jordan's, not Egypt's. Egypt provides the comparison baseline for the composite score calculation, but Egypt's trajectory does not contain the policy decision moment that Mode 3 is demonstrating. Option E is not viable.

**Chief Methodologist Agent:** On Option C (debt rescheduling alongside GCC) — also not run because the instrument would require an EmergencyInstrument type, and the existing instrument set does not include a reserve injection or debt rescheduling instrument. IMF_PROGRAM_ACCEPTANCE operates through the governance channel, not a direct reserve injection. Any debt rescheduling instrument in the current architecture would produce no quantitative effect on reserves. This would be methodologically dishonest to include in a demo. Option C cannot be implemented in the current engine without an ADR.

**Development Economist Agent:** Converging on a recommendation. The current fixture at baseline is the right design. The Mode 3 branch from step 3 at 1.30× tells a coherent story: Jordan is in the IMF negotiating room at step 3, accepts the emergency liquidity backstop (which is in the branch at 1.30×), but negotiates successfully on fiscal conditionality (which is not in the branch). The GDP divergence at step 4 is visible (+0.68pp from 1.30× GCC vs 1.0×), and the unemployment divergence at step 5 is more substantial because the austerity drag is absent from the branch. That is the story that is both methodologically sound and humanly meaningful.

**Chief Methodologist Agent:** Agreed. One calibration note: the 1.30× multiplier at step 4 produces an estimated additional +0.68pp GDP in the branch vs baseline (0.06 × 0.30 × 0.5 × 0.75 = 0.00675 = 0.675pp). The austerity removal contributes an additional ~+1.125pp at step 5 (the -0.03 × 0.5 × 0.75 that disappears from the branch). So the branch divergence peaks at step 5, not step 4. Zone 1A should display this correctly if the branch endpoint is set to step 5 or beyond.

The composite score (financial percentile rank JOR vs EGY) will show divergence at step 5 if JOR branch GDP (+5.3% estimated) clearly exceeds EGY GDP (+3.56%). At the same step, baseline JOR GDP (+3.60%) only barely exceeds EGY GDP (+3.56%), so the financial composite score is near 0.5 in the baseline but should shift materially above 0.5 in the branch. This is the visible composite score change the demo requires.

**Development Economist Agent:** One final concern for the record. The reserves continue draining identically in the branch — 3.7→2.5→1.2→0→0 months. The branch does not rescue Jordan from the reserve crisis; it only improves GDP and employment trajectory. A finance minister needs to know this. The Mode 3 demo, if presented honestly, should make clear that the "better negotiating outcome" improves the economic trajectory but does not solve the structural import dependency problem. The MDA alerts on reserve coverage will still fire in the branch, at the same steps, with the same severity. The demo should not imply that better fiscal negotiation substitutes for reserve rebuilding.

**Chief Methodologist Agent:** This is the most important caveat for the demo narrative. The branch shows what better fiscal terms accomplish; it does not show what they don't accomplish. The analyst presenting the demo should explicitly note that reserve MDA alerts are identical in both trajectories. This is not a limitation of the demo — it is the honest answer to "what can conditionality negotiation actually change?"

---

## Panel Agreement

Both agents agree:

1. **Retain the current fixture** — GCC +0.06 at step 3, austerity -0.03 at step 4, duration 2. No fixture modifications should be committed.
2. **Branch from step 3 at fiscal_multiplier=1.30** — the documented anchor in the fixture and Issue #817. No change to branch parameters.
3. **The 1.30× multiplier is the right parameter** — but the primary divergence driver is austerity removal (step 5), not multiplier amplification (step 4). Zone 1A should run to at least step 5 before the demo analyst makes the comparison claim.
4. **Options A, B, D, E are not recommended** — for reasons documented above.
5. **Reserve depletion caveat is mandatory** — the demo narrative must acknowledge that MDA reserve alerts are identical in baseline and branch, and that better conditionality negotiation does not change the structural external vulnerability.
