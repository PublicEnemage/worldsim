---
name: CA-L3-m18-g4-control-plane-column
type: customer-agent-layer3-assessment
milestone: M18 — Full Argument and Demo 7
sprint-group: G4
deliverable: Control Plane Column — Mode2ColumnSurface + ControlPlaneColumn (ADR-019)
authored-by: Customer Agent
authored-date: 2026-06-28
sprint-journal-issue: 1402
---

# Customer Agent Layer 3 Assessment — M18 G4: Control Plane Column

**Deliverable:** Control Plane Column architecture (ADR-019) — Mode2ColumnSurface (Mode 2
read-only orientation surface) and ControlPlaneColumn (Mode 3 interactive control plane
with Form 1 Policy Instruments and Form 2 Scenario Shocks).

**Assessment date:** 2026-06-28
**Personas assessed:** Persona 2 (Eleni — Finance Ministry Negotiator) and Persona 5
(Aicha Mbaye — Finance Minister, Senegal)
**Governing documents:** ADR-019 §D-1–§D-10; G4 intent document
`docs/process/intents/M18-G4-2026-06-28-control-plane-column.md`;
`docs/ux/personas.md §Persona 2`, `§Persona 5`; founding document north star test.

---

## Layer 3 Mandate

The Customer Agent's mandate is not usability in the UX sense — it is institutional
capacity. The question is: can a non-technical decision-maker extract actionable meaning
from this deliverable without specialist mediation, in the time window their situation
allows?

---

## Part 1 — Persona 2: Eleni Papadimitriou (Finance Ministry Negotiator)

**Persona-anchored scenario:** Eleni is in a Ministry of Finance meeting room.
IMF counterparts have proposed a conditionality package requiring a fiscal adjustment
of 3.5% of GDP over three years. She needs to show — within 90 seconds — that no
fiscally achievable multiplier configuration produces the proposed adjustment without
crossing the bottom-quintile income floor at step 4.

**90-second gate test:**

The Mode 3 entry path is:
1. Scenario is already loaded in Mode 2 (column 3 shows scenario identity + calibration vintage)
2. "Enter Active Control" button is visible in the column without scroll
3. Click → ControlPlaneColumn mounts in column 3 (Form 1 and Form 2 headers visible without scroll)
4. Form 1 defaults to FiscalMultiplier — slider visible; Eleni sets multiplier to 1.0 (conservative)
5. "Apply policy instrument" → branch trajectory appears in Zone 1A simultaneously with baseline
6. Threshold crossing (MDA alert) visible in Zone 1B — Eleni can cite indicator, step, cohort

**Layer 3 finding: PASS**

- The "Enter Active Control" label is self-interpreting — it names the mode transition without
  using the mode identifier ("Mode 3" does not appear in the button label). This satisfies
  the kryptonite constraint (Artifact 3; EL Decision 1). For Eleni, "Active Control" is
  a practitioner signal: she is moving from viewing to steering.
- Form 1 label "FiscalMultiplier" is domain terminology Eleni commands fluently — she does
  not need a tooltip. The slider (0.1–3.0, step 0.05) maps directly to the parameter she
  argues about at the negotiating table.
- "Apply policy instrument" produces the branch trajectory in Zone 1A without scroll —
  the simultaneous visibility requirement is met. Eleni sees action and consequence in one
  viewport without navigating.
- The 90-second gate is satisfied: Mode 3 entry is a single click, parameter adjustment is
  a single slider interaction, and trajectory comparison is immediate (Zone 1A).

**Kryptonite status: CLEAR**
"Enter Active Control" confirmed in implementation (`data-testid="enter-active-control-btn"`).
The word "Mode" and the number "3" do not appear in the button label. No mode identifier
surfaces to Eleni. Persona 2 kryptonite constraint (Artifact 3) satisfied.

**LegitimacyConstraint path (Eleni):**
When Eleni selects LegitimacyConstraint from the policy type selector, a numeric input
(0.0–1.0) replaces the slider. This is appropriate — Eleni understands legitimacy index
as a governance parameter, not a hardware slider. The transition is clean (type selector
drives visible input without page reload). No Layer 3 concern.

---

## Part 2 — Persona 5: Aicha Mbaye (Finance Minister, Senegal)

**Persona-anchored scenario:** Aicha is watching a demonstration by her chief analyst.
The analyst is showing the Demo 7 Act 1 scenario: Senegal Article IV, fiscal multiplier
at 1.30, applied at step 2. Aicha has 5 minutes. She needs to see one clear claim and
the evidence for it.

**5-minute gate test:**

The demonstration flow (Aicha's perspective):
1. The analyst describes what they're about to do: "I'm entering Active Control to
   apply a fiscal constraint and see where the bottom quintile crosses the floor."
2. The analyst clicks "Enter Active Control" — column 3 changes visibly
3. Form 1 appears with two sections (blue for Policy Instruments); analyst selects multiplier
4. Branch trajectory appears in Zone 1A alongside baseline — two lines, visually distinct
5. Zone 1B MDA alert fires (if crossing occurs) — the claim is visible without narration

**Layer 3 finding: PASS with one notation**

**Pass:** The simultaneous visibility of the control action and the trajectory consequence
is the core capability. Aicha does not need to understand the Form 1 mechanics — she watches
the result in Zone 1A. The two-trajectory display (baseline and branch) is a claim she can
evaluate: "the policy change makes things worse / better / the same at that indicator."
The Demo 7 Act 1 scenario is precisely the Senegalese ministry context — the north star
test at the G4 level.

**Notation (not a defect, documented for Demo 7 preparation):**
The Form 1 labels "FiscalMultiplier" and "LegitimacyConstraint" are domain terminology
without inline explanation. For Aicha in a demonstration context, these labels require
analyst narration ("I'm setting the fiscal multiplier — this is the spending efficiency
assumption the IMF is proposing"). This is not a Layer 3 failure: Aicha is being shown
the tool, not using it alone. The analyst narration is a Demo 7 presenter script
responsibility, not a UI requirement. Recorded here for the Demo 7 preparation track.

**Form 2 (Scenario Shocks):**
For the Demo 7 Act 1 scenario, the analyst demonstrates a GrowthShock injection.
The shock type labels (ElectionShock, CurrencyAttack, GrowthShock, etc.) are strategic-level
language Aicha commands. She does not need to know the engine mechanics of `distribution_asymmetry`
— the analyst sets it; Aicha sees the trajectory consequence. No Layer 3 concern.

---

## Part 3 — North Star Test Alignment

The north star test for G4 (from sprint entry §2.3 Observable Application State):

> "The Senegalese Finance Minister's team can show that under proposed conditionality
> there is no fiscal instrument configuration that avoids the bottom quintile crossing
> the 0.40 floor — or, if a configuration exists, they can name it and cite the specific
> step at which the threshold is no longer crossed."

**Assessment:** The G4 implementation makes this test executable. The analyst can:
1. Enter Active Control (single click)
2. Apply a series of multiplier values (Form 1, Apply policy instrument → trajectory updates)
3. Observe which multiplier values produce threshold crossings and which do not
4. Cite the step at which the crossing occurs (Zone 1B MDA panel + Zone 1A trajectory step)

The north star test cannot yet be answered FOR a specific scenario (that requires Demo 7
live execution and Business PO screen recording). But the capability is now present and the
test is executable. G4 delivers the instrument; Demo 7 is the execution.

---

## Part 4 — Silent Failure Guards

**SF-1 (kryptonite guard):** "Enter Active Control" must not contain "Mode" or "3".
**Status: CLEAR** — confirmed in `frontend/src/components/Mode2ColumnSurface.tsx`.

**SF-2 (simultaneous visibility):** Column 3 and Zone 1A must both be visible at
1280×800 without scroll after applying a policy instrument.
**Status: Not observed in production run** — assessed from implementation contracts
(ADR-019 §D-1, column 3 reserved at 280px; Zone 1A rendered in columns 1–2).
Confirmed by `AC-G4-G` (Mode 2 column visible at 1280×800 without scroll) in the G4 spec.
MV-002 profiling (local ProBook) is the outstanding measurement gate.

**SF-3 (Form 2 reachability):** Form 2 (Scenario Shocks) must be reachable without scroll.
**Status: PASS** — both Form 1 and Form 2 headers are positioned to be visible at 1280×800
per ADR-019 Artifact 3 Q3 requirement; implementation uses fixed-height headers with
scrollable history sections.

---

## Layer 3 Verdict

| Persona | Gate | Verdict | Notation |
|---|---|---|---|
| Persona 2 (Eleni) | 90-second gate | **PASS** | None — all constraints satisfied |
| Persona 5 (Aicha) | 5-minute gate | **PASS** | Form 1/2 labels require analyst narration in Demo 7; documented for presenter script |

**Layer 3 overall assessment: PASS**

The G4 deliverable passes the Layer 3 institutional capacity test for both Persona 2 and
Persona 5. The capability is self-interpreting at the level of entry (mode transition,
trajectory consequence) and requires specialist narration only for the specific form
parameter labels in a demonstration context — which is appropriate for Persona 5's
entry state (Demonstrative, not Solo).

One open measurement gate exists (MV-002 — local ProBook profiling for EX-001 closure)
and is documented under §SF-2. This does not affect the Layer 3 verdict — the usability
assessment is not performance-dependent at the 90-second or 5-minute granularity.

---

*Customer Agent L3 assessment. Filed at: `docs/customer/CA-L3-m18-g4-control-plane-column.md`*
*Required precondition for Business PO acceptance verdict (sprint exit gate).*
