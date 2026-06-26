---
name: M18-GR-counter-scenario-comparison-requirements
type: requirements-intent
issue: "#1352"
parent-issue: "#1349"
status: Filed — GR phase artifacts on record; G3 sprint entry prerequisite satisfied pending Architect ADR determination
authored-by: PM Agent
authored-date: 2026-06-26
phase: GR — Requirements phase (no sprint entry required per m18-sprint-plan.md §GR exception)
artifacts-produced:
  - "§2 UX Journey — counter-scenario comparison with distributional differential"
  - "§3 Customer Agent Layer 3 — Personas 1, 2, 5 kryptonite and false precision assessment"
  - "§4 BPO Business Requirements — minimum viable form, acceptance threshold, north star test"
release-branch: release/m18
sprint-plan-reference: docs/process/sprint-plans/m18-sprint-plan.md §GR
g3-entry-prerequisite: true
---

# GR Requirements Intent: M18 — Counter-Scenario Comparison (#1352 / #1349)

> **GR phase document.** This is not an implementation intent. This document records the
> three GR phase artifacts required before the G3 sprint entry may be filed:
> (1) UX journey for counter-scenario comparison, (2) Customer Agent Layer 3 assessment
> for Personas 1, 2, and 5, and (3) BPO business requirements. Upon GR close, the Architect
> determines the ADR requirement for G3, and the G3 implementing agent files the implementation
> intent from the user stories and acceptance criteria in §4.
>
> **Parent capability:** #1349 — distributional number differential with CI bands.
> M17 delivered N=3 multi-scenario comparison (#394) — three scenario curves in Zone 1A,
> per-scenario Zone 1B threshold crossings, per-scenario PSP in Zone 1D. #1349 adds the
> HEADLINE NUMBER DIFFERENTIAL: the specific real-world count (poverty headcount) difference
> between scenarios, with CI bands, surfaced as a citable number.
>
> **Demo 7 anchor:** Act 2 — Zambia (ZMB), three restructuring scenarios. The citeable claim
> the Finance Minister's team must be able to make: "Under the IMF-proposed terms, 340,000
> more Zambians will be below the poverty threshold at programme end than under our
> counter-proposal. The direction is stable across the full uncertainty range."

---

## 1. Source and Scope

**GR issue:** #1352 — requirements phase for #1349
**Parent implementation issue:** #1349 — counter-scenario comparison — distributional number differential with CI bands
**Blocked by GR close:** G3 sprint entry; Architect ADR determination for G3; intent document and QA tests for G3

**What M17 already built (M18 GR does not re-author):**
- N=3 multi-scenario comparison Zone 1A curves (#394, on `main`)
- Per-scenario Zone 1B threshold crossing rows (CRITICAL/WARNING labels per scenario)
- Per-scenario PSP in Zone 1D
- SCENARIO_COMPARISON_PALETTE differentiation scheme

**What #1349 adds (the gap this GR phase specifies):**
The M17 comparison shows COMPOSITE SCORES in Zone 1A (e.g., Option C: 0.72 vs. Option A: 0.58).
The analyst must mentally compute the delta (0.14) and then mentally translate this to real-world
impact. #1349 closes this gap: the simulation engine computes the differential in real-world units
(poverty headcount: number of people) and surfaces it as a labeled, CI-banded number in Zone 1B.
The user reads a number, not a calculation requirement.

---

## 2. UX Journey — Counter-Scenario Comparison with Distributional Differential

**Authored by:** UX Designer Agent perspective
**Governing documents:** `docs/ux/information-hierarchy.md`, `docs/ux/personas.md §Persona 1,
§Persona 2, §Persona 5`, `docs/ux/north-star.md`, `docs/ux/user-journeys.md §Journey A Step 6`

---

### 2.1 — Who, in what mode, initiates the comparison?

**Primary user:** Eleni Papadimitriou (Persona 2 — Finance Ministry Negotiator)

**Entry state:** Preparatory — the evening before the restructuring session. She has loaded
the three Zambia restructuring scenarios using the M17 N=3 comparison infrastructure. The
instrument cluster shows three Zone 1A curves with CI bands (G1 capability), per-scenario
Zone 1B crossings, and per-scenario PSP in Zone 1D.

**Mode:** Mode 2 (Simulation) — N=3 COMPARE_VIEW. No mode switch is required for #1349.
The distributional differential is a new Zone 1B element within the existing comparison mode.

**Secondary user:** Aicha Mbaye (Persona 5 — Finance Minister) in the Demonstrative entry
state — she is being shown the three-scenario comparison by her analyst. She reads the
comparison summary from Zone 1B directly.

**The initiating question (not an interaction — a reading moment):** After confirming which
scenarios cross thresholds in Zone 1B (M17 capability), Eleni asks: "But how many people
are we talking about?" The #1349 capability makes this question answerable without a
follow-up calculation.

---

### 2.2 — At what moment does the user encounter the differential?

**The Demo 7 Act 2 sequence:**

1. Analyst loads three Zambia scenarios → N=3 COMPARE_VIEW
2. Zone 1A shows three curves with CI bands (G1) — Eleni confirms Option C stays above MDA floor
3. Zone 1B shows per-scenario crossings — "Option A: CRITICAL Q1 Poverty headcount, step 2" (M17)
4. **[NEW — #1349]** Comparison summary element appears below per-scenario rows in Zone 1B:
   - "Poverty headcount differential at programme end (step 8):"
   - "Option A vs. Option C: **+340,000 persons** below poverty threshold"
   - "95% CI: 295,000 – 395,000 · T2"
   - "Direction stable across full uncertainty range."
5. Eleni reads the number. She now has the citeable claim.
6. In the negotiation room (Journey B), she cites: "Under your proposed terms, 340,000 more
   Zambians will be below the poverty threshold at programme end. Our counter-proposal holds
   this to 80,000. This is not a directional claim with uncertainty — the direction is stable."

**Moment of encounter:** Between Zone 1B threshold crossings (M17) and any further analysis.
The comparison summary is a Zone 1 element — visible without any interaction after loading
the three scenarios.

---

### 2.3 — Dedicated UI element or emergent from Zone 1A trajectories?

**A dedicated Zone 1B element is required.** The differential cannot emerge from Zone 1A alone.

**Why Zone 1A curves are insufficient:**
- Zone 1A composite scores (0.72 vs. 0.58) do not translate to headcount without a calculation
  the user should not be required to perform
- The composite score delta (0.14) requires knowledge of the entity's population and the
  income distribution to convert to headcount — this is economist-mediated knowledge
- CI bands on composite scores do not directly yield CI bands on headcount differences
  without propagating uncertainty through the conversion — a backend computation, not a
  visual reading

**Comparison summary element — placement and format:**

Zone 1B, appended below per-scenario threshold crossing rows. This is a ZONE 1 surface:
the element is visible without scrolling in a 1280×800 viewport when N=3 comparison is active.

```
─────────────────────────────────────────────────
DISTRIBUTIONAL COMPARISON  [step 8 of 8 · T2]
─────────────────────────────────────────────────
Poverty headcount differential

Option A vs. Option C    +340,000 persons
(front-loaded vs. homegrown)   [295K – 395K  95% CI]

Option B vs. Option C    +210,000 persons
(carve-out vs. homegrown)      [175K – 255K  95% CI]

→ Direction stable across uncertainty range
─────────────────────────────────────────────────
```

Design constraints:
- The element is labeled "DISTRIBUTIONAL COMPARISON" — not "statistics" or "additional output"
- The step at which the differential is computed defaults to the TERMINAL STEP
- A step-axis link ("at step 8 of 8") indicates the current computation step; clicking it
  allows the user to change the step (secondary behavior, not required for Demo 7)
- The confidence tier badge "T2" is adjacent to the element header — not in footnotes
- The direction stability statement ("Direction stable across uncertainty range") appears
  only when it is true — when the CI interval on the differential is entirely positive
  (or entirely negative), the statement fires; when the CI interval spans zero, a
  different disclosure appears: "Direction uncertain — model uncertainty exceeds the
  estimated differential"
- The element does not render when N < 3 or when only one "reference" scenario is designated

---

### 2.4 — Interaction model: step selection or canonical point?

**Default: terminal step.** The terminal step (final programme step) is the canonical
comparison point for Demo 7 Act 2. "At programme end" is the citeable framing — it represents
the cumulative human cost outcome of the full programme conditionality.

**Rationale:** The worst-case step (peak differential) is analytically interesting but
introduces ambiguity in citation ("at the moment of maximum divergence" is harder to defend
than "at programme end"). The first MDA crossing step varies by scenario and is not a
shared reference point for comparison. The terminal step is defensible, consistent, and
program-anchored.

**Step selection (secondary behavior):** When the user selects a step on the Zone 1A step
axis, the comparison summary element updates to show the differential at that step. This
behavior is consistent with the existing step-axis shared frame principle (CLAUDE.md §UX
Architectural Commitments). Step selection is a secondary behavior — not required for the
Demo 7 minimum viable demonstration.

---

## 3. Customer Agent Layer 3 Assessment

**Authored by:** Customer Agent perspective
**Governing documents:** `docs/ux/personas.md §Persona 1, §Persona 2, §Persona 5`,
`docs/process/agent-execution-lifecycle.md §Kryptonite Design Constraint`

---

### 3.1 — Persona 1: Lucas Ferreira (Programme Analyst)

**Kryptonite check:** Does Lucas require economist mediation to use the comparison summary?

**Assessment: NO kryptonite on primary reading.** Lucas has the analytical depth to read
and validate the comparison summary independently. He understands composite scores, confidence
tiers, and headcount conversions. The comparison summary does not introduce friction for Lucas.

**Layer 3 obligation for Lucas:** The comparison summary must be REPRODUCIBLE and AUDITABLE.

- **Reproducibility:** The same three-scenario inputs must produce the same differential number.
  The computation (composite-score-to-headcount conversion + delta + CI propagation) must be
  deterministic and backend-computed, not client-side derived. Lucas must be able to state "the
  simulation engine computes this differential" — not "the UI estimates this from chart values."

- **Auditability:** The methodology behind the conversion (how composite score units map to
  poverty headcount) must be accessible from within the element. A methodology disclosure link
  or expandable panel showing: (a) the entity's base population, (b) the Q1 income share used,
  (c) the conversion factor from composite score delta to headcount, and (d) the CI propagation
  method. This is a Zone 3 surface (expandable) — not Zone 1 — but it must exist.

- **False precision assessment for Lucas:** Lucas will check the T2 tier assignment. The
  distributional differential computation derives from calibrated simulation engine outputs
  (Fosu 2011 SSA calibration, M17 G1). T2 classification is appropriate IF the conversion
  methodology is itself T2 (calibrated from published literature). If the headcount conversion
  uses a regional average or model-derived income distribution (Tier 3), the differential
  inherits Tier 3 — not Tier 2. **The implementing agent must confirm tier inheritance at
  implementation time and document it in the PR description.**

---

### 3.2 — Persona 2: Eleni Papadimitriou (Finance Ministry Negotiator)

**Kryptonite check:** Does Eleni require economist mediation to cite the comparison summary?

**Assessment: NO kryptonite IF the element is designed as specified in §2.3.**

Without #1349: Eleni sees Zone 1A curves showing composite scores 0.72 vs 0.58. She must
mentally compute a delta (0.14), translate to headcount, and know the entity's population to
form the argument "hundreds of thousands of people." This IS kryptonite — it requires background
knowledge she may not have under time pressure.

With #1349 as designed: The number "340,000 persons" is self-interpreting. "Under Option A,
340,000 more Zambians below the poverty threshold at programme end" is a complete, citable sentence
she reads from Zone 1B. No calculation required. Kryptonite removed.

**False precision risk for Eleni:**

The CI band "295,000 – 395,000" is a 34% spread. Does this undermine the argument?

**Assessment: NO, provided the direction stability statement fires.** The CI band documents
honest uncertainty, but the direction stability statement "Direction stable across uncertainty range"
tells Eleni the range does not change the argument's conclusion — Option A is worse than Option C
regardless of where within the uncertainty band the true value falls. The range in absolute terms
is still "hundreds of thousands" at either bound.

**Disclosure framing Eleni can use proactively:**
> "The exact number is uncertain — our model estimates between 295,000 and 395,000 additional
> persons. But the direction is stable: under all model configurations within the calibrated
> uncertainty range, the proposed terms produce worse poverty outcomes than our counter-proposal.
> This is an honest acknowledgment of model uncertainty, not a reason to discount the finding."

The ia1_disclosure from the existing epistemic protocol reinforces rather than undermines this
framing. Eleni can use the disclosure proactively rather than defensively.

**90-second ceiling check:** The comparison summary is a Zone 1 element. With N=3 active and
Zone 1B per-scenario rows visible, the comparison summary element appears below them. At 1280×800,
this must not require scrolling to reach. The Zone 1B layout must accommodate both the per-scenario
crossing rows AND the comparison summary element within the Zone 1 viewport allocation.

**Design constraint flagged:** Zone 1B may become vertically crowded with N=3 per-scenario rows
PLUS a comparison summary element. The implementing agent must verify at implementation time that
the comparison summary element is visible without scrolling in a 1280×800 viewport. If Zone 1B
overflow is triggered, the comparison summary MUST take precedence (scroll the per-scenario rows,
not the summary).

---

### 3.3 — Persona 5: Aicha Mbaye (Finance Minister)

**Kryptonite check:** Does Aicha require economic training to read and act on the comparison summary?

**Assessment: NO kryptonite IF the element uses plain language and avoids composite score notation.**

"340,000 additional persons below the poverty threshold" is concrete, non-technical, and actionable.
Aicha does not need to know what "Q1 poverty headcount composite" is. She needs to know that
"340,000 more Zambians fall below the poverty threshold" is the consequence of the IMF proposal
vs. her government's alternative.

**Kryptonite patterns to avoid:**
- "Q1 composite delta: +0.14 (95% CI: 0.12–0.16)" — requires composite score knowledge → KRYPTONITE
- "Poverty headcount change: −0.072 standard deviations" — requires statistical knowledge → KRYPTONITE
- "Option A poverty indicator: 0.58; Option C: 0.72; delta: 0.14 (T2)" — requires unit knowledge → KRYPTONITE
- "340,000 more persons below the poverty threshold under proposed terms" — concrete, no mediation → PASS

**Demonstrative entry state ceiling:**
Aicha has 30 seconds to read the comparison summary while the analyst narrates. The element must:
- Be visible in Zone 1 without any interaction
- Use plain-language labels (not "Q1 poverty headcount composite" but "persons below poverty threshold")
- Surface the comparison pair names (Option A / Option C or "IMF Proposed" / "Counter-Proposal")
  in words Aicha recognizes from the briefing she received before the session

**Failure mode for Aicha:** If the element uses composite-score notation or requires any UI
interaction to reveal the number, the Demo 7 Act 2 demonstrative use case fails. Aicha terminates
the demonstration. The north star test is not passed.

**Trust signal for Aicha:** Aicha's trust threshold is institutional — she trusts outputs that
her analyst trusts. The T2 badge is sufficient epistemic disclosure for the demonstrative state;
she does not need to understand what T2 means. The direction stability statement is interpretable:
"regardless of model uncertainty, the direction is clear" is the same statement she would make
about any analysis she trusts to brief the Finance Minister.

---

## 4. BPO Business Requirements

**Authored by:** Business Product Owner perspective
**Authority:** Sprint plan §BPO consultation (m18-sprint-plan.md §Demo 7 Act 2 minimum viable demo)

---

### 4.1 — Minimum Viable Form

The counter-scenario comparison capability (G3 / #1349) is MINIMALLY VIABLE when:

1. A comparison summary element appears in Zone 1B when N=3 comparison mode is active
2. The element surfaces a poverty headcount differential in real-world units (number of persons)
   between the BEST scenario (Option C — Homegrown Programme) and the IMF-PROPOSED scenario
   (Option A — EFF Front-Loaded) at the terminal programme step
3. A CI band is displayed alongside the differential (format: "X – Y  95% CI")
4. The comparison pair is labeled in plain language (not scenario letter codes alone)
5. No user calculation is required — the number is engine-computed, not user-derived
6. The direction stability statement fires when the CI interval does not span zero

Minimum viable is NOT:
- A chart or visualization of the differential over time (nice to have for full G3)
- An interactive step-selector for the differential (nice to have; terminal step default suffices for Demo 7)
- A multi-indicator comparison (poverty headcount is sufficient for Demo 7 Act 2; extending
  to health system capacity, governance, etc. is capacity-allowing scope)
- A comparison export function (not required for Demo 7)

---

### 4.2 — Acceptance Threshold

**G3 produces a PASS when:**

The Zambia three-scenario Demo 7 Act 2 scenario, loaded in N=3 COMPARE_VIEW with CI bands
from G1 active, displays a comparison summary element in Zone 1B that shows:
- The poverty headcount differential between Option A and Option C at step 8
- A CI band on that differential
- A direction stability statement (when applicable)
- The element is visible in Zone 1 without scrolling at 1280×800
- No economist mediation is required to read the element (Persona 5 legibility test)

**BPO ACCEPT is triggered when:** The BPO confirms the above from the running UI,
specifically: Aicha Mbaye's analyst narrates "Under the proposed terms, 340,000 more
Zambians fall below the poverty threshold" from the comparison summary element alone,
without reading or calculating from Zone 1A curve values. The BPO will request a screen
recording of the Demo 7 Act 2 flow before issuing formal ACCEPT.

---

### 4.3 — User Stories (G3 intent document input)

**US-1349-A (Eleni, Preparatory):**
As Eleni in the Preparatory entry state, building the counter-proposal evidence base, I need to
see the poverty headcount differential between the IMF-proposed scenario and the Zambian counter-
proposal as a specific number with a confidence range, so that I can enter the restructuring
session with a citable claim that does not require me to calculate from composite score values.

**US-1349-B (Eleni, Active Negotiation):**
As Eleni in the Active Negotiation entry state at the restructuring table, I need the differential
number to be visible in Zone 1B without any interaction, so that I can cite it within 90 seconds
of picking up the tablet without opening a drawer or navigating away from the primary viewport.

**US-1349-C (Analyst briefing Aicha, Demonstrative):**
As an analyst demonstrating the three-scenario comparison to the Finance Minister, I need the
differential element to be readable by a non-economist in under 30 seconds without explanation,
so that the Finance Minister forms a position from the comparison summary during the demonstration
rather than asking me what the number means.

**US-1349-D (Lucas, Preparatory — audit and defence):**
As Lucas in the Preparatory entry state, preparing the distributional evidence for an IMF programme
review, I need the differential computation's methodology and CI band derivation to be accessible
from within the element, so that I can defend the number under peer scrutiny from the IMF analytical
team without retrieving external documentation.

---

### 4.4 — North Star Test Assessment

**Finance minister scenario:** The Zambia Ministry of Finance analyst is in a restructuring
negotiation session with the IMF team. The IMF has presented three programme options, one of
which is the Ministry's counter-proposal (Option C — Homegrown Programme — Gradual Adjustment).
The IMF team argues that Option A (EFF Front-Loaded) produces comparable human cost outcomes
to Option C and offers stronger fiscal consolidation.

**The capability being evaluated:** The distributional number differential in Zone 1B (#1349).

**Does this capability change what the Ministry's team can argue at the table?**

**YES.** Before #1349, the Ministry's analyst can show that Option C avoids the CRITICAL threshold
crossing that Options A and B trigger (M17 N=3 comparison). This is a binary argument: "our
proposal does not cross the threshold; yours does." The IMF team can challenge this by questioning
the threshold level or the composite score construction.

After #1349, the Ministry's analyst can show a SPECIFIC NUMBER DIFFERENTIAL with CONFIDENCE BOUNDS:
"Under Option A, 340,000 more Zambians are below the poverty threshold at programme end than under
our counter-proposal. The model uncertainty is honest — the range is 295,000 to 395,000 — but
the direction is stable: this is not a modelling artefact. The difference is in the hundreds of
thousands regardless of where within the confidence interval the true value falls."

This shifts the burden of the IMF's response: they must either challenge the calibration of the
differential computation (which requires confronting the Fosu 2011 SSA calibration in ADR-017
and the M17 G1 elasticity registry changes) or acknowledge that the distributional gap exists
and propose a mechanism to address it. They cannot dismiss the finding as "unclear direction"
when the direction is stable across the full uncertainty range.

**North star test verdict: PASS.** The capability gives the Zambia Ministry of Finance a
quantified, confidence-banded, direction-stable poverty headcount differential that changes
the character of the argument from binary (threshold crossed / not crossed) to distributional
(how many people, with what confidence). This is a new class of argument the Ministry's team
can make in the room.

---

## 5. GR Close Conditions

GR (#1352) is closed when all three artifact conditions are satisfied:

| Condition | Artifact | Status |
|---|---|---|
| UX journey documented | §2 of this document | ✅ Filed 2026-06-26 |
| Customer Agent L3 on record for Personas 1, 2, 5 | §3 of this document | ✅ Filed 2026-06-26 |
| BPO business requirements on record | §4 of this document | ✅ Filed 2026-06-26 |

---

## 6. G3 Sprint Entry Prerequisites (Generated by GR Close)

Upon GR close, the following actions are required before the G3 sprint entry is filed:

### 6.1 — Architect ADR Determination (required at G3 sprint entry)

Per `m18-sprint-plan.md §Architect consultation §G3`:

> "Does counter-scenario comparison introduce a new visual encoding pattern for Zone 1B
> not addressed by ADR-017? ADR-017 covers framework × entity × branch × mode — a
> distributional differential element is arguably a new encoding dimension."

The Architect must determine before the G3 sprint entry is filed whether:

**Option A (CLEAR — no new ADR):** The comparison summary element (§2.3) is a Zone 1B
content extension within ADR-017's existing authority. ADR-017 governs Zone 1B content
and the threshold-crossing disclosure model; the distributional differential is an additional
content type within the same zone, not a new encoding dimension. ADR-017 may require
a minor amendment (new content type in §Content Taxonomy), but this does not require a
new ADR. G3 implementation proceeds.

**Option B (BLOCKED_ADR):** The comparison summary element introduces a new encoding
dimension not covered by ADR-017 — specifically, it represents a COMPARISON BETWEEN
SCENARIOS rather than threshold crossings WITHIN a scenario, which is a structurally
different use of Zone 1B. A new ADR or ADR-017 amendment is required before G3 may
open an implementation PR.

**Architect's information for this determination (from §2.3):**
- The element is placed IN Zone 1B, not in a new zone
- It appears BELOW per-scenario threshold crossing rows (M17 content)
- It computes a cross-scenario quantity (delta), not a per-scenario threshold state
- It uses different units (real-world headcount) from Zone 1B's existing MDA alert units
  (composite score thresholds)
- It introduces a new text pattern ("Direction stable across uncertainty range") with no
  existing Zone 1B precedent

These four characteristics are the Architect's inputs. The determination is the Architect's
to make, and it must be recorded explicitly in the G3 sprint entry document.

### 6.2 — G3 Intent Document

The G3 implementing agent files an implementation intent derived from:
- §2.3 (comparison summary element design)
- §4.3 (user stories US-1349-A through US-1349-D)
- §3.1/3.2/3.3 (persona Layer 3 constraints as design guardrails)

The G3 intent document must include:
- Observable application state (as verifiable by QA without source code)
- Acceptance criteria (hard-fail, no soft-skip patterns per NM-056)
- Kryptonite constraint check per persona (derived from §3)
- Backend computation specification: how the engine derives poverty headcount from composite
  scores, and how CI bands are propagated through the conversion

### 6.3 — QA Tests

QA tests for G3 are authored from the G3 intent document's acceptance criteria BEFORE the
implementation PR opens. The minimum test suite must cover:

- AC for US-1349-A: comparison summary element present in N=3 COMPARE_VIEW at step 8
- AC for US-1349-B: element visible in Zone 1 without scrolling at 1280×800
- AC for US-1349-C: element text is plain-language (no composite score notation) — assertable
  via text content of the summary element
- Persona 5 legibility gate: comparison summary is visible and contains text matching the
  poverty headcount differential pattern (number + CI range) without any click or hover

---

*GR phase document authority: `docs/process/sprint-plans/m18-sprint-plan.md §GR phase
sequencing detail`. Issue: #1352 (requirements phase for #1349). Parent issue: #1349
(counter-scenario comparison — distributional number differential with CI bands).
GR phase has no sprint entry per m18-sprint-plan.md §GR exception — this document IS
the GR close artifact. Filed: 2026-06-26. GR close is confirmed when EL acknowledges
this document and instructs PM Agent to advance the Architect ADR determination for G3.*
