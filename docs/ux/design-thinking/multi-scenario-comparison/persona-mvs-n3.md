# Persona Minimum Viable Story — Multi-Scenario Comparison (N=3)

> **Artifact 2 of G2 Phase 1 design sprint**
> **Authored by:** Customer Agent
> **Date:** 2026-06-25
> **Issue:** #394 — feat: multi-scenario comparison (>2 scenarios)
> **Authority:** `docs/process/intents/M17-G2-2026-06-25-multi-scenario-design.md §3.1`
> **Governing documents:** `docs/ux/personas.md §Persona 1, §Persona 3, §Persona 5`,
> `docs/ux/north-star.md`, `docs/ux/information-hierarchy.md §Zone 1`

---

## Scenario anchor — Demo 7 Act 2 (ZMB)

All three persona MVS assessments are anchored to the **Zambia Demo 7 Act 2** scenario:
three IMF restructuring options compared simultaneously in Mode 2 (Simulation). The
Q1 poverty headcount indicator is the primary comparison indicator; Programme Survival
Probability (Zone 1D) is the secondary.

| Scenario | Short label | Q1 poverty headcount composite at step 4 | CRITICAL floor | PSP at step 4 |
|---|---|---|---|---|
| EFF — Front-Loaded | Option A | 0.58 (below CRITICAL floor) | 0.60 | 58% |
| EFF + Social Protection Carve-Out | Option B | 0.59 (below CRITICAL floor) | 0.60 | 67% |
| Homegrown Programme — Gradual | Option C | 0.72 (above floor) | 0.60 | 74% |

These values are consistent with expected simulation engine outputs for Zambia under the
calibrated ELASTICITY_REGISTRY (M17 G1 wave 1, PR #1270 — Fosu 2011 SSA calibration).
The exact numerical values will be produced by the engine at Phase 3 implementation;
the relative ordering (C avoids crossing; A and B cross) is structurally guaranteed by
the scenario design (Option C's slower adjustment path keeps Q1 expenditure above floor
through the 8-step window).

---

## Lucas Ferreira — Persona 1 (Programme Analyst) MVS

### Specific comparison argument Lucas can make

**Scenario:** Lucas has loaded the three ZMB restructuring options in Mode 2. He is in
the Preparatory entry state — building the human cost evidence base before a programme
design session with the creditor team.

**The specific argument (from primary viewport, Zone 1A + Zone 1B, step 4):**

> "Under Option A, Q1 poverty headcount crossed the CRITICAL threshold at step 2 — the
> second quarter of programme implementation. Under Option B, the same crossing occurs at
> step 3. Option C's Q1 poverty headcount trajectory stays above the CRITICAL floor through
> step 8 — the full 8-quarter programme window. The Q1 poverty headcount difference between
> Option C and Option A at step 4 is 0.14 (composite units), corresponding to the divergence
> visible in Zone 1A. Option A and Option B produce CRITICAL human cost exposure in the first
> half of the programme; Option C does not."

**Where Lucas finds each element:**
- "Crossed at step 2 / step 3": Zone 1B, per-scenario crossing rows (Option A header →
  "CRITICAL Q1 Poverty headcount — crossed step 2"; Option B header → "CRITICAL Q1 Poverty
  headcount — crossed step 3")
- "Stays above floor through step 8": Zone 1B, Option C → "[no crossings through step 8]"
- "Q1 poverty headcount difference of 0.14": Zone 1A, terminal labels at step 4 (Option C: 0.72,
  Option A: 0.58 → delta 0.14)
- "Option A and B produce CRITICAL exposure": Zone 1B, CRITICAL severity labels under both
  scenario headers

**Reproducibility requirement:** Lucas requires that the same three-scenario setup produces
the same display for both sides of the table. The N=3 comparison state must be exportable
or shareable (URL-based scenario comparison state) so that the creditor-side analyst can
load the same three scenarios and see the same Zone 1A + Zone 1B output. This is a Phase 3
implementation requirement — the comparison state must be serializable, not session-only.

**Time constraint:** No fixed ceiling for Preparatory entry state. Lucas builds the comparison
during preparation; 60 seconds is the in-session retrieval time once the comparison is loaded.

---

## Aicha Mbaye — Persona 5 (Finance Minister / Senior Ministry Official) MVS

### 90-second legibility gate

**Scenario:** Aicha is at the restructuring negotiating session table. The creditor team
has proposed three programme options. Her analyst has pre-loaded the three-scenario comparison.
Aicha looks at the screen for 90 seconds while the creditor team presents.

**Primary anchor:** Zone 1B, Option C row — "[no crossings through step 8]"

This is the element that answers Aicha's question. The read sequence:
1. Zone 1A: Aicha sees three curves. The dotted green curve (Option C, terminal label "C") is
   highest at step 4. The solid blue (A) and dashed orange (B) curves are below the MDA floor
   dashed line. (~10 seconds for initial scan)
2. Zone 1B: Aicha reads the Option C row: "[no crossings through step 8]." Options A and B
   both show "CRITICAL Q1 Poverty headcount." (~20 seconds)
3. Total: ~30 seconds to confirm the answer. Remaining time in the 90-second window allows
   for confirming the indicator name (Q1 Poverty headcount) and the scenario label (Option C).

**What Aicha says after reading the display (literal statement):**

> "Option C — the Homegrown Programme — does not cross the poverty threshold. The other two
> options both breach it in the first year. Our position at the table is Option C."

This statement is made from Zone 1A + Zone 1B alone. The analyst does not need to narrate
the answer. The Zone 1A curve labels ("A", "B", "C" at endpoints, color-coded) and the
Zone 1B per-scenario rows (grouped under each option header) together provide the complete
answer without any additional interaction.

**Confirmation of the legibility gate:** A reviewer reading `ux-journeys-n3.md §Journey 3`
literal text block can confirm: "Aicha can identify Option C as the option avoiding Q1 CRITICAL
crossing at step 4 from Zone 1A (terminal label 'C' at 0.72, above MDA floor dashed line at
0.60) and Zone 1B (Option C: '[no crossings through step 8]'), without narration, in under
90 seconds." This confirmation is affirmative.

**Kryptonite assessment:** The 90-second legibility gate is satisfied without hover, drawer
interaction, or view navigation. Option (a) from the kryptonite check in `ux-journeys-n3.md
§Kryptonite check` — this design meets the constraint.

---

## Andreas Petrakis — Persona 3 (Political Advisor) MVS

### Per-scenario PSP comparison from Zone 1D

**Scenario:** Andreas is building the political brief before the negotiating session. He needs
to compare Programme Survival Probability across all three scenarios to identify which option
has the highest programme survival probability.

**What Andreas reads from Zone 1D (literal values at step 4):**

```
Zone 1D | Programme Survival Probability:
  Option A  [■ solid blue]   58%
  Option B  [▪ dashed orange]  67%
  Option C  [● dotted green]   74%
```

**Zone 1D display mechanism:** Per-scenario PSP values displayed simultaneously in Zone 1D
as a three-row block (per `ux-journeys-n3.md §Journey 2 — Zone 1D`). Andreas reads all three
values in a single Zone 1D scan. No view switching is required.

**Structural change assessment for Zone 1D:** The existing Zone 1D single-PSP display (one
value for the active scenario) requires extension to a three-row PSP block when N=3 comparison
is active. This is a client-side extension of the Zone 1D component — it does not require a
new API endpoint. The PSP value is already available per scenario in the existing trajectory
response (`political_economy.indicators.programme_survival_probability` per api_contracts.yml
§DA-G5-4). When three scenarios are loaded, the frontend holds three trajectory responses and
renders three PSP values from the existing field. No new backend structure is required for Zone 1D.

**The political statement Andreas makes:**

> "Option A has the lowest programme survival probability at 58%. Option C has the highest at
> 74%. Option B is in between at 67%. Combined with the poverty headcount evidence — Option C
> avoids the Q1 CRITICAL crossing — Option C is the strongest political and human cost case.
> We can defend Option C's lower fiscal surplus target by showing it is both more politically
> survivable and less damaging to the bottom quintile."

**Specific step for PSP divergence:** Step 4 is named as the step where PSP divergence is most
pronounced. In the front-loaded programme options (A and B), PSP declines sharply in the first
4 steps as social legitimacy indicators deteriorate alongside Q1 poverty headcount crossing.
Option C's slower adjustment path sustains PSP through the comparison window. The PSP
divergence at step 4 (A: 58%, B: 67%, C: 74%) is a 16-point spread between Options A and C —
sufficient for a clear political brief.

---

## Minimum Viable N=3 Implementation for Demo 7 Act 2

### Feature set required for all three personas' MVS

**Zone 1A (required):**
- Three scenario curves rendered simultaneously with the triple-channel differentiation
  (color + line-style + terminal endpoint label per `ux-journeys-n3.md §Zone 1A`)
- Curves use the `composite_score` field per scenario per step
- MDA floor line(s) rendered as shared horizontal dashed gray line(s)
- data-testid anchors: `zone1a-curve-scenario-{id}`, `zone1a-terminal-label-scenario-{id}`

**Zone 1B (required):**
- Per-scenario threshold crossing rows, grouped under scenario headers
- Scenario header with color-coded indicator matching Zone 1A (same color/line-style)
- "[no crossings through step N]" element when a scenario has no crossings
- MDA alert panel `minHeight: 80px` guarantee preserved
- data-testid anchors: `zone1b-scenario-header-{id}`, `zone1b-threshold-row-scenario-{id}`,
  `zone1b-no-crossings-{id}`

**Zone 1D (required):**
- Three-row PSP block showing per-scenario Programme Survival Probability when N=3 comparison active
- Each row: scenario color indicator, option label, PSP percentage
- data-testid anchors: `zone1d-psp-row-scenario-{id}`, `zone1d-psp-value-{id}`

**Scenario setup (fixture sufficient for Demo 7):**
A pre-configured three-scenario fixture is sufficient for Demo 7 Act 2. The full scenario
setup Journey 1 UI (where the analyst adds scenarios inline via Zone 2) should be implemented
for general use, but for the Demo 7 demonstration, a pre-loaded three-scenario state is
acceptable. **Aicha's MVS does not require her analyst to build the comparison from scratch
at the table — the comparison is prepared in advance.**

This means Phase 3 can proceed with the three-scenario comparison rendering (Zone 1A, 1B, 1D)
even if the Zone 2 "Add third scenario" UI mechanism is not fully polished — as long as the
comparison can be set up programmatically (e.g., via fixture or URL param) before the demo.

### What is explicitly deferred to M18

- N=4 and N=5 scenario support (the design scales to N=5 but Phase 3 must deliver N=3)
- Mode 3 multi-scenario interaction (Active Control with N>1 scenarios — M18 north star)
- Cross-scenario Zone 1D delta display ("Option A vs. Option C: ΔQ1 = 0.14")
- Full scenario setup UI as a polished Zone 2 flow (the inline "Add third scenario" button
  is sufficient for Phase 3 demo; a refined Zone 2 scenario management UI is M18 enhancement)
- Comparison state serialization / URL export for reproducibility (required for Lucas's full MVS;
  acceptable for Phase 3 as a hardcoded fixture; M18 scope for general use)

### BPO use of this section

The BPO uses this section to determine:
(a) Whether a partial Phase 3 implementation closes M17 with BPO acceptance — **Yes**: Zone 1A
    N=3 rendering + Zone 1B per-scenario rows + Zone 1D three-PSP block is sufficient for
    Demo 7 Act 2 BPO acceptance, with Zone 2 scenario setup UI and state serialization as M18.
(b) What the M18 carry scope is — N=4/5 support; Mode 3 multi-scenario; cross-scenario delta
    display; full Zone 2 scenario management; comparison state serialization.

---

## Kryptonite assessment — Customer Agent (applied to Artifact 2)

**Question:** Can Aicha's MVS be satisfied within the 90-second Reactive ceiling at N=3?
Or is the comparison inherently too information-dense for 90 seconds without narration?

**Assessment: Satisfied — option (a) from §Kryptonite check in ux-journeys-n3.md applies.**

The N=3 per-scenario Zone 1B grouping is the critical design decision that makes Aicha's
MVS feasible. A union Zone 1B display would force Aicha to parse scenario attribution from
each crossing row — adding a cognitive step that breaks the 90-second ceiling. The per-scenario
grouping (three headers, crossings under each, "[no crossings]" for Option C) reduces Aicha's
read to a single scan: she looks for which scenario header has no crossings. That takes under
30 seconds.

The triple-channel Zone 1A differentiation supports Aicha's read even under color vision
limitations (her advisor may project on a screen with suboptimal color rendering). The line-style
differentiation (solid/dashed/dotted) is the accessibility backstop.

**What would fail the 90-second ceiling:**
- More than 3 scenarios active (N=4 would require Aicha to scan 4 Zone 1B groups — the
  marginal cognitive cost pushes past 90 seconds for a non-specialist)
- A union Zone 1B display (requires parsing scenario attribution per row)
- Scenario labels that are not immediately legible (numeric IDs, database UUIDs — the design
  commits to human-readable "Option A / B / C" labels)

**What is sustainable within the ceiling:**
- N=3 per-scenario Zone 1B grouping
- Triple-channel Zone 1A with terminal "A/B/C" labels
- Zone 1D PSP three-row block (Aicha reads this in 5 seconds — three numbers and three labels)

**Option (a) — design meets the ceiling.** No redesign required. No scope reduction to a
"simpler N=3 display" is warranted. The design as specified in `ux-journeys-n3.md` delivers
the full Aicha MVS within 90 seconds.

---

*Customer Agent — 2026-06-25. G2 Phase 1 Artifact 2. Issue #394.*
*Reviewed against: `personas.md §Persona 1, §Persona 3, §Persona 5`,*
*`personas.md §Entry State Taxonomy §Reactive, §Preparatory`, `north-star.md`.*
*Kryptonite assessment applied: Aicha's 90-second ceiling satisfied at N=3.*
