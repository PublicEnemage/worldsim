---
name: scenario-evaluation-mode3-recommendation
type: step-5d-recommendation
sprint: M18-G6
milestone: M18
status: PASS — fm=0.85 confirmed
panel: Development Economist + Chief Methodologist
session: 2026-06-28
deliberation-file: docs/demo/m18/reviews/scenario-evaluation-mode3-deliberation.md
---

# Step 5d — Mode 3 Branch Configuration Recommendation
## Demo 7 Act 1: Senegal FiscalMultiplier Panel Verdict

**STEP 5D: PASS**

The two-agent panel (Development Economist + Chief Methodologist) confirms the following
configuration for Demo 7 Act 1. Screenshots (Step 6) may proceed.

---

## Confirmed Configuration

| Parameter | Value | Source |
|---|---|---|
| `fiscal_multiplier` | **0.85** | Panel recommendation — DE + CM confirmed |
| `branch_from_step` | **3** | G4 acceptance spec (BRANCH_FROM_STEP constant) |
| `n_steps` | **8** | G4 acceptance spec |
| entity | **SEN** (Senegal) | M18 sprint plan — Demo 7 Act 1 |
| Start date | **2024-01-01** | G4 acceptance spec |
| Ecological module | **disabled** | G4 acceptance spec |
| Political economy module | **enabled** | G4 acceptance spec |

---

## Frame A — Confirmed Parameters

*(Updates screenshot brief `docs/demo/m18/screenshot-brief.md` Frame A TBD fields)*

| Frame A field | Confirmed value |
|---|---|
| Mode | Mode 3 Active Control |
| Fiscal multiplier displayed | **0.85** |
| Branch from step | **3** |
| Zone 1A display | Baseline + branch trajectories, split visible from step 3 |
| PSP driver label (Frame B) | "Driver: fiscal sustainability" |
| CI band opacity | 5% (Mode 3) |
| MDA floor line | 0.40 (q1_poverty_headcount) |
| Floor outcome at step 6 | **CLEAR** in both baseline and branch |

---

## Panel Findings Summary

**Maximum divergence step: 8**
- HD: baseline 0.454 vs branch 0.474 — delta +0.020
- Financial: baseline 0.489 vs branch 0.529 — delta +0.040
- Divergence is constant from step 3 (level shift, not growing gap)

**Reserve independence: Adequate**
- ExternalSectorModule disabled; reserves not modeled
- Presenter must disclose at Section 6; walkthrough already contains this disclosure
- No misleading implication risk

**Narrative coherence: Confirmed**
- fm=0.85 = 15% multiplier reduction ≈ 1.5pp primary surplus target reduction
- Article IV counter-proposal framing is economically coherent for Senegalese context
- CLEAR outcome narrates as: "the standard adjustment doesn't threaten the floor; the
  counter-proposal widens the margin" — a legitimate and useful demonstration
- Minister's argument: not "we avoided crisis" but "we demonstrated that less consolidation
  produces a measurably better human outcome within the same safety envelope"

**Fiscal transmission consistency: Confirmed**
- Net multiplier 0.68 (FISCAL_MULTIPLIERS["standard"]=0.8 × fm=0.85)
- Within SSA LIC consensus range (Ilzetzki et al. 2013: 0.5–0.9)
- Mock values (+0.02 HD, +0.04 Financial from step 3) consistent with underlying module math

**Data environment disclosure:**
- Live SEN simulation with NE_110M_2024 produces flat trajectories (no growth or fiscal event data)
- Panel evaluated on G4 accepted mock values — this is a Structural Absence Declaration
- Required demo disclosure: "The stack is seeded with geographic classification data; economic
  dynamics are represented by calibrated scenario design. The trajectories shown are the
  designed representation of fiscal transmission in a Senegalese Article IV context."
- This disclosure must be added to walkthrough Section 6 (Honest Disclosures)

---

## Required Walkthrough Update (Section 6)

Add the following to `docs/demo/m18/stakeholder-walkthrough.md §Section 6 — Honest Disclosures`:

> **Trajectory design disclosure.** The Senegal simulation is seeded with Natural Earth
> geographic classification data (population, GDP stock, economic tier). Growth dynamics,
> fiscal transmission, and cohort welfare trajectories are represented by calibrated
> scenario design — the mock values accepted at G4 sprint exit (FM=0.85, BRANCH_FROM_STEP=3).
> The trajectories are the *designed* representation of what fiscal transmission would produce
> if IMF WEO macroeconomic data were loaded. The CI bands (T3, 5% opacity) reflect the
> genuine epistemic uncertainty from the data environment. This is a known limitation of
> the current data seeding; the simulation's qualitative argument — that a 15% multiplier
> reduction improves HD outcomes while maintaining fiscal safety — is consistent with the
> module's causal logic.

---

## Screenshot Brief Update (Frame A)

The screenshot brief `docs/demo/m18/screenshot-brief.md` marks Frame A step/multiplier as
TBD pending Step 5d. The confirmed values are:

- **Frame A caption:** "Act 1 · Mode 3 · SEN · fm=0.85 from step 3 · Zone 1A split"
- **Presenter action before screenshot:** Set FiscalMultiplier slider to 0.85; click
  "Apply Policy Input"; confirm branch trajectory appears from step 3
- **Expected Zone 1A state:** Two trajectory lines from step 3 onward (baseline muted,
  branch highlighted); CI bands at 5% opacity; no MDA floor alert firing

---

## Step 5d Gate Status

- [x] Live simulation runs complete: 1 baseline + 6 branch scenarios (fm=0.5/0.8/0.85/1.0/1.5/2.0)
- [x] All branch runs: 8 steps completed in status=completed
- [x] Data environment assessed: Structural Absence Declaration filed
- [x] Declared mock values evaluated: G4 spec values confirmed by DE + CM
- [x] Max divergence step identified: step 8 (HD +0.020, Financial +0.040)
- [x] Reserve independence confirmed: Section 6 disclosure adequate
- [x] Narrative coherence confirmed: fm=0.85 Article IV counter-proposal framing coherent
- [x] Fiscal transmission confirmed: net multiplier 0.68 within SSA LIC consensus
- [x] PSP driver label confirmed: "fiscal_sustainability" for fm=0.85
- [x] CI band interpretability confirmed: 5% opacity appropriate for Mode 3
- [x] Two required walkthrough updates identified (Section 6 data disclosure; Frame A TBD fields)

**STEP 5D: PASS. Screenshots (Step 6) are unblocked.**

---

*Filed: 2026-06-28. Panel: Development Economist + Chief Methodologist.*
*Deliberation: `docs/demo/m18/reviews/scenario-evaluation-mode3-deliberation.md`*
