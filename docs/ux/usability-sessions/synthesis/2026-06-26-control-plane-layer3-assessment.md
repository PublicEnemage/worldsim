# Customer Agent Layer 3 Assessment — Control Plane Column Design Package

> **Type:** Customer Agent Layer 3 Assessment (GD Artifact 3, Issue #1357)
> **Parent:** #1354 — Control Plane Column Design Package
> **Date:** 2026-06-26
> **Activation:** `Customer Agent: AUDIT — Control Plane Column design package (#1354):
> Layer 3 assessment for Persona 2 (Eleni Papadimitriou) and Persona 5 (Aicha Mbaye)
> across Mode 2 preparation and Mode 3 active negotiation contexts.`
> **Filing location:** `docs/ux/usability-sessions/synthesis/`

---

## Assessment Context

This assessment speaks for Eleni Papadimitriou (Persona 2) and Aicha Mbaye (Persona 5)
in the specific Demo 7 Act 1 scenario: Senegal Article IV, IMF negotiating team across
the table, the question of whether any fiscal instrument configuration avoids the bottom
quintile crossing the 0.40 recovery floor. It answers five specific questions filed in
Issue #1357, each with an explicit verdict where required.

Source documents consulted: `docs/ux/personas.md`, `docs/ux/user-journeys.md §Journey C
and §Journey D`, `docs/ux/information-hierarchy.md §Control Plane Reserved Zone`,
`docs/ux/user-stories-instrument-cluster-m9.md §Group 8 US-027/US-028`.

---

## Question 1 — Journey C Step 4: Is shock injection essential to Demo 7 Act 1?

**Verdict: ESSENTIAL**

The distinction between ESSENTIAL and STRENGTHENING turns on what Eleni faces after
Steps 1–3. Journey C Steps 1–3 produce a finding: the proposed minimum wage cut timing
causes a CRITICAL poverty headcount crossing at step 2. That finding is citable. The
Troika's expected response is not silence — it is a rebuttal: "Even without the delay,
the GDP rebound in year 2 will protect the bottom quintile."

That rebuttal is a testable empirical claim. If the tool cannot test it in the room,
Eleni has two options: (a) concede that she cannot respond to the rebuttal within the
session, or (b) assert from preparation analysis that the rebuttal is wrong. Option (b)
is what finance ministry negotiators do every day — they prepare and cite. But Demo 7
Act 1 is not a preparation demonstration; it is an active-control demonstration. The
entire argument for Mode 3 is that the tool can respond to a claim that was not
anticipated in preparation — in real time, at the table, with live evidence.

If the shock injection step is absent from Demo 7 Act 1, the demonstration proves
Mode 2 preparation capability with a Mode 3 framing — it does not prove Mode 3
active-control capability. The distinction is not a marketing question; it is a product
question. The Troika rebuttal scenario is the exact moment the Mode 3 claim is tested.
If the tool cannot inject the GDP shock and show that the CRITICAL alert persists,
the argument is weakened from "the tool disproved your rebuttal in real time" to
"the tool found the problem — the rebuttal would need to be evaluated separately."
The second version is a better-prepared ministry. The first version is a qualitatively
different tool.

The Eleni persona closes the tool if primary instruments require navigation (persona
failure mode 1). She does not close it when a non-primary capability is deferred. Shock
injection is a primary Mode 3 capability specified in US-028, Journey C Step 4, and the
information hierarchy — not a secondary enhancement. Its absence in Demo 7 Act 1 is
visible as a gap to any participant who has read the Demo 7 brief.

**Operational assessment:** Steps 1–3 are sufficient to produce a finding and survive
the initial Troika assertion. Step 4 is required to survive cross-examination on the
Troika's own rebuttal. For Demo 7 Act 1, where live external participants are expected
(Issue #843, live external session), the tool must perform under adversarial conditions.
An unsatisfied rebuttal in that context undermines the demonstration more than a missing
feature would.

---

## Question 2 — Mode 2 Column: Does Eleni need the fiscal multiplier in the column during preparation?

**Verdict: HIGH friction — preparation cognitive task is structurally broken without it**

Journey A Gap GA-02 describes the situation precisely: Eleni cannot access the fiscal
multiplier parameter while watching the trajectory respond. She must navigate away from
the instrument cluster to change the multiplier, then return to see the effect.

The degree of friction depends on what "Mode 2 preparation" actually requires. It requires
a parameter-response feedback loop: Eleni adjusts the fiscal multiplier, watches whether
the trajectory crosses any MDA floor, adjusts again. This is iterative. Each navigation
break interrupts the loop, forces a context switch, and requires her to reorient to the
trajectory on return. At three to five iterations — which is a modest calibration session —
she has spent more time navigating than configuring.

The Eleni persona operates in two distinct temporal regimes:
- Mode 3 Reactive state: 90-second retrieval requirement. Every action is time-critical.
- Mode 2 Preparatory state: three hours the night before. Not time-critical in the same way.

The question is whether "not time-critical" means "friction is acceptable." It does not,
for a specific reason: the friction in Mode 2 is not a slowness problem — it is a
broken-feedback-loop problem. When Eleni adjusts the fiscal multiplier without seeing
the trajectory, she is configuring blind. She brings her prior knowledge of the relationship
to form an expectation, navigates away, applies the change, returns, reads the result, and
then evaluates whether the expectation was met. This is structurally identical to writing
code without a compiler — technically feasible, high error rate, high cognitive overhead.

The instrument cluster exists precisely to close this feedback loop: the parameter and the
instrument are visible simultaneously so the relationship between cause and effect is
observable. GA-02 breaks the Mode 2 version of this loop. Fixing it in the Mode 2 column
is not an ergonomic enhancement — it is the precondition for Mode 2 preparation to work
as designed.

**Assessment for Artifact 5 scope decisions:** The Mode 2 fiscal multiplier column is
not an incremental convenience feature. It is the completion of the Mode 2 preparation
cognitive task as specified. Any scope decision that defers it must explicitly classify
Mode 2 preparation as incomplete and note what Persona 2 cannot do as a result.

---

## Question 3 — Aicha's demonstrative task: Is the two-form control plane layout legible without explanation?

**Verdict: CONDITIONAL — legible with one explanatory sentence per form; not self-explaining without it**

The two-form layout — blue for policy instruments, orange for scenario shocks — is
epistemically correct. The distinction between "what the pilot chose" and "what the
environment did to the pilot" is a meaningful category difference, and making it
visible in the layout is the right design decision (see Class A persona conflict ruling
in `docs/ux/personas.md §Persona Priority Rules`).

Aicha's legibility question is different: can she follow what is happening without
explanation? The answer is conditional on whether the action-response relationship
is observable. The action-response loop — Eleni applies a control input, the trajectory
updates, an alert fires — is observable by a non-technical observer if:

1. The action (clicking "Apply policy input") is visible
2. The trajectory change is visible immediately (live A/B, divergence fill)
3. The alert text is legible (severity + indicator name at tablet font sizes, per
   Class A ruling: "a cold reader can orient from severity and indicator name alone")

On these three criteria, the two-form layout satisfies Aicha's observational requirement
**with one explanatory sentence per form**. That sentence is: "The blue form is for policy
parameters — what we're proposing. The orange form is for market conditions — what might
happen to us." A driver providing that sentence satisfies the Class B floor (every Zone 1
element must be self-describing to a cold reader in ≤1 sentence per instrument).

The risk is layout complexity. Two forms in 280px of column height, with history lists
below each, produces a visually dense right column. If both history lists are populated
simultaneously (two applied inputs, one injected shock), the column becomes information-
dense in a way that competes for Aicha's attention alongside the trajectory view. The
Demo 7 Act 1 narrative should be designed so that history lists contain at most one or
two entries during the critical viewing window — not as a UX limitation but as a
demonstration design choice.

**Recommendation for Artifact 2 (Target State Specification):** The two-form layout
is correct. The sizing constraint is that both form *headers* must be visible without
scroll — Aicha needs to see that there are two categories of action available, even if
she does not read the forms in detail. History lists may scroll within their section;
this is acceptable.

---

## Question 4 — Kryptonite Check: Shock taxonomy breadth in Demo 7

**Verdict: MEDIUM risk — GDP/growth shock coverage is sufficient for the Troika rebuttal; edge risk is commodity price and external demand shocks**

The Demo 7 Act 1 scenario requires one shock: a positive GDP growth shock at step 2 to
test the Troika's "GDP rebound will protect the bottom quintile" claim. The taxonomy
specified in Issue #1354 — `ElectionShock`, `CurrencyAttack`, `CreditorDefection`,
`GeopoliticalShock`, `NaturalDisaster`, `ContagionShock` — does not include a GDP
growth shock by name. The Demo 7 scenario requires a shock that represents a positive
external demand or growth assumption.

This is a taxonomy design question that belongs in Artifact 2 (Target State Specification):
does the GDP rebuttal scenario map to `ContagionShock` in reverse, or does the taxonomy
require a `GrowthShock` or `ExternalDemandShock` type? If the taxonomy as specified does
not cover the primary Demo 7 use case, this must be resolved before implementation begins.

For the external participant kryptonite assessment, participants at Demo 7 (finance ministry
officials, possibly academic economists) are likely to ask about:
- Commodity price shocks: oil price, agricultural price — not in the taxonomy as specified
- External demand shocks: export demand collapse — not in the taxonomy as specified
- Sovereign credit rating events: may map to `CreditorDefection`
- Exchange rate shocks: not in the taxonomy; distinct from `CurrencyAttack`

**Recovery if a requested shock type is unavailable:** "That scenario type is on the
roadmap for the next milestone" is an acceptable Demo 7 answer for any shock not in the
taxonomy. What is not recoverable in the Demo 7 context is if the primary demonstration
shock (the GDP rebuttal injection) is not in the taxonomy — that is a Demo 7 blocker, not
an edge case.

**Recommendation:** Artifact 2 must confirm that the shock taxonomy covers a
positive GDP/growth shock. If `ContagionShock` is not the right semantic container, a
`GrowthShock` type should be added to the taxonomy before implementation begins.

---

## Question 5 — 90-second retrieval requirement under current bottom-bar layout

**Verdict: CURRENTLY FAILING — trajectory is not simultaneously visible with the control plane on 1280×800**

This is a factual observation about the current implementation, not a speculative risk.

On a 1280×800 viewport, the DOM vertical stack in Mode 3 is:
1. `ScenarioInstrumentCluster` header / entity selector / comparison controls (estimated 40–60px)
2. `InstrumentCluster` — fixed-width 1260px (580+400+280), chartHeight=320px for co-primary;
   the instrument cluster height is dominated by the column with the most content (Zone 1B
   + Zone 1C + Zone 1D combined; estimated 400–450px total column height at 1280)
3. `HumanCapitalTrajectoryPanel` — conditional; if projection_steps > 8, adds substantial height
4. `ControlPlane` bottom bar — padding 10px top/bottom, three form elements with labels and
   sliders, apply button, branch anchor annotation; estimated 140–160px

Total estimated height: 40 + 420 + 150 = 610px minimum before `HumanCapitalTrajectoryPanel`.
On 1280×800, usable viewport is approximately 770px after the browser chrome. The instrument
cluster alone fits. The `ControlPlane` bar pushes the total to 760px — at the edge of the
viewport. With any browser chrome (address bar, tabs), the ControlPlane bar is below the fold.

More critically: the `ControlPlane` is rendered *below* the InstrumentCluster. Eleni must
scroll down to reach the control inputs, then scroll back up to see the trajectory response.
The 90-second retrieval requirement assumes the trajectory and the control plane are visible
simultaneously — this is stated explicitly in Journey C Step 2: "The control plane zone must
be visible alongside the trajectory view without scroll."

The current implementation fails this requirement structurally — not because of viewport
measurement, but because the architecture places the control plane outside the instrument
cluster grid. Even if the bottom bar happens to be visible on a given display, the user
must move her eyes vertically across the full height of the instrument cluster to compare
a control input in the bottom bar against a trajectory curve at the top of the display.
On a laptop at 1280×800, this is a significant eye-travel distance under time pressure.

**Implication for GD:** The ControlPlane must move into the 280px reserved column to
satisfy the 90-second retrieval requirement. This is not a layout preference — it is the
precondition for the Mode 3 product claim ("apply a control input and observe the
instrument response simultaneously").

---

## Assessment Summary

| Question | Verdict |
|---|---|
| Q1 — Shock injection Demo 7 necessity | **ESSENTIAL** — required to survive cross-examination on Troika rebuttal; Steps 1–3 alone prove Mode 2 capability, not Mode 3 |
| Q2 — Mode 2 fiscal multiplier friction | **HIGH** — structurally breaks the parameter-response feedback loop; not an ergonomic convenience |
| Q3 — Aicha legibility of two-form layout | **CONDITIONAL** — legible with one driver sentence per form; both form headers must be visible without scroll for observational orientation |
| Q4 — Shock taxonomy kryptonite | **MEDIUM** — GDP/growth shock coverage must be confirmed in taxonomy before implementation; commodity/FX shocks are acceptable deferred-to-roadmap answers |
| Q5 — 90-second retrieval under current layout | **CURRENTLY FAILING** — ControlPlane renders outside the 280px column; trajectory and control plane are not simultaneously visible on 1280×800 |

---

## Implications for Artifact 5 (Scope Decision Document)

This assessment establishes three non-negotiable constraints for any scope decision:

1. **Shock injection is Demo 7 scope, not post-Demo 7.** The Troika rebuttal injection is
   the strongest argument the tool makes. If the scenario shocks form is not in Demo 7
   Act 1, Demo 7 demonstrates a more sophisticated Mode 2 — not Mode 3.

2. **ControlPlane must move into the 280px column.** This is not optional architectural
   cleanup — it is the structural precondition for the simultaneous-visibility requirement
   that the 90-second retrieval SLA depends on.

3. **The shock taxonomy must cover a positive GDP/growth shock before implementation
   begins.** This is a Artifact 2 dependency that Artifact 5 must verify is resolved.

These three constraints should be reflected in any implementation sequencing choice in
Artifact 5.
