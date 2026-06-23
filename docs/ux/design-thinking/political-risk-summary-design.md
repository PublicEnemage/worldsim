# Political Risk Summary Surface — Design Document

> **Author:** UX Designer Agent
> **Date:** 2026-06-21
> **Issue:** #987 — feat(ux): political risk summary surface — plain-language legitimacy dynamics
> **Phase:** M15 G3 — Design-only (implementation is M16 scope)
> **Intent document:** `docs/process/intents/M15-G3-2026-06-21-cohort-disaggregation-design.md`
> **Status:** Filed for Architecture Review Facilitator and Chief Methodologist review
>
> **Governing documents read:**
> - `docs/ux/information-hierarchy.md §Zone 1`, `§Zone 1D`, `§Dashboard View Hierarchy`
> - `docs/ux/north-star.md §Primary Cognitive Tasks by Mode`
> - `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md §Question 1`
> - `docs/ux/design-thinking/zone-1a-information-architecture.md §Information Allocation`
> - `CLAUDE.md §UX Architectural Commitments` (commitments 1–5)
> - `docs/ux/personas.md §Persona 3`
> - `docs/ux/user-journeys.md §Journey A`, `§Journey B`
> - ADR-013 (Political Economy Integration, M13-G5, #792) — political economy module outputs

---

## Design Context

The political economy module (ADR-013, M13, #392 closed) is live. It produces three primary
outputs at each step: Programme Survival Probability (PSP), legitimacy index, and elite capture
divergence. These outputs are currently invisible to Persona 3 (Andreas, Senior Policy Advisor,
no formal economics training) without navigating to Zone 1D and interpreting composite framework
scores — a task that requires domain expertise Andreas does not have.

M14 G1 (#1075) delivered a PSP self-interpreting sentence in Zone 1D — one sentence at the
current step. G3 extends this to a structured political risk sub-section: PSP as a severity-labeled
percentage, legitimacy direction, elite capture status, and a plain-language historical analogue —
all simultaneously visible in Zone 1D without any interaction.

**Design task:** Specify which Zone hosts the political risk summary for Persona 3, the
mode-specific display contract, the exact plain-language sentence format for a named scenario,
the 30-second legibility confirmation, and whether a new ADR is required.

---

## Zone Placement

**Decision: Zone 1D (Four-Framework Current Position) — extended with a "Political Risk"
sub-section**

Zone 1D's primary cognitive task, per `docs/ux/information-hierarchy.md §Zone 1 / 1D`:

> *"The four composite score values at the current step — a quick-read number readout serving
> as the flight instrument analog to an altimeter cluster."*

The political risk summary (PSP, legitimacy index, elite capture divergence) is a set of
**current-step readout values** — exactly the cognitive task Zone 1D is designed for. PSP at
step 3 is as much a "current position" signal as the Governance composite score at step 3.
Adding a "Political Risk" sub-section to Zone 1D below the four-framework rows extends (does
not conflict with) Zone 1D's cognitive task.

**Relationship to Zone 1D's existing display (explicitly stated):**

The political risk summary SUPPLEMENTS Zone 1D's four-framework display. It does NOT replace
the Governance composite row. After M16 implementation, Zone 1D will contain:
- Financial: [composite score]
- Human Development: [composite score]
- Ecological: [composite score]
- Governance: [composite score]
——————— POLITICAL RISK ———————
- Programme survival: [SEVERITY] ([PSP%])
  [plain-language historical analogue sentence]
- Legitimacy index: [value] — [direction] (floor: [floor value])
- Elite capture divergence: [widening / stable / narrowing]

The Governance composite row remains — it is the ADR-013 governance framework composite. The
"Political Risk" sub-section surfaces the disaggregated political economy indicators that the
Governance composite partially aggregates. This is Layer 3 enhancement: the numbers were
already there; the design makes them legible to a non-economist.

**Conflict with Zone 1D's existing political economy composite display:** None. The M14 G1
PSP sentence is already in Zone 1D (#1075 — merged in PR #1097). G3's political risk sub-section
extends this sentence to a structured three-element display.

**Conflict check against Zone 1D cognitive task:** Zone 1D's task is "all four values visible
simultaneously — no tabs, no toggles" (`information-hierarchy.md §Zone 1D`). The political risk
sub-section adds below the four rows, not replacing any row. The existing Zone 1D requirements
remain intact: four framework rows, human-readable labels, atomic update at step advance.

**Rejected alternatives:**

- **New Zone 1E:** A new primary zone requires a layout ADR and introduces a fifth column or
  row into the primary instrument cluster — disproportionate for content that fits within Zone
  1D's existing cognitive task. The political economy module (ADR-013) already has a home in
  Zone 1D via the Governance composite. Making its disaggregated outputs visible within Zone 1D
  is a Layer 3 enhancement, not a new architectural element.
- **Zone 1B (MDA Alert Panel):** PSP is not a threshold crossing alert — it is a probability
  value with direction. The MDA alert panel correctly fires when PSP falls below a defined
  threshold (CRITICAL alert: PSP < 0.40). But the continuous display of PSP value, direction,
  and plain-language interpretation belongs in the current-position readout (Zone 1D), not in
  the alert channel.
- **Zone 2 (FrameworkPanels, political economy tab):** Zone 2 requires one scroll or one tab
  action. Persona 3's 30-second ceiling in the Reactive entry state requires Zone 1 visibility.

---

## Mode-Specific Display Contract

### Mode 1 (Replay) — Historical political risk trajectory

**Which indicators appear:**
- PSP: REQUIRED. Shown as severity-labeled percentage. Direction: "at this level historically"
  (past-tense framing — the PSP at this step in the loaded fixture).
- Legitimacy index: REQUIRED. Shown as value + direction (declining / stable / improving,
  compared to the previous loaded step).
- Elite capture divergence: OPTIONAL. Shown if the political economy module produced a non-null
  value in the loaded fixture at this step; collapsed with an "—" if absent. Uses the same
  absent-data treatment as Zone 1D null axes (`information-hierarchy.md §Zone 1D`: "Null axes
  visually distinct from zero-value axes").

**Format per indicator:**

PSP (Mode 1):
```
Programme survival: [SEVERITY] ([PSP%])
At this level, historical ECF programmes [historical analogue — requires #1084 calibration].
```

Legitimacy index (Mode 1):
```
Legitimacy index: [value] — [direction based on step-over-step change]
  [floor proximity: "X above floor" / "at floor" / "below floor"]
```

Elite capture divergence (Mode 1):
```
Elite capture divergence: [widening / stable / narrowing — based on step-over-step change]
```

**Direction labels (Mode 1 — historical fact):**
- Legitimacy: "declining" (value fell from previous step), "stable" (≤1% change), "improving"
  (value rose from previous step)
- Elite capture: "widening" (divergence increased), "stable" (≤5% change), "narrowing"
  (divergence decreased)

**Update behaviour:** Values reflect the historical fixture at the step loaded in Zone 1A. When
the user advances a step in Mode 1 (navigating the fixture), all three elements update atomically
with the rest of Zone 1D — same cycle, same render call. No separate loading state.

**Empty state (Mode 1, political economy module not enabled for this fixture):**
"Political risk: not modelled in this fixture." The sub-section header shows but the three rows
are replaced by this single line. It is not hidden — the absence of political risk data is
explicit information.

---

### Mode 2 (Simulation) — Projected political risk at each step

**Which indicators appear:** Same as Mode 1 (PSP REQUIRED, legitimacy REQUIRED, elite capture
OPTIONAL).

**Format per indicator:**

PSP (Mode 2):
```
Programme survival: [SEVERITY] ([PSP%]) — [DECLINING / STABLE / IMPROVING from step N-1]
At this level, historical ECF programmes [historical analogue — requires #1084 calibration].
```

Legitimacy index (Mode 2):
```
Legitimacy index: [value] — [direction from step N-1] (floor: [floor value])
  [X] above floor  [or]  AT FLOOR  [or]  [X] below floor
```

Elite capture divergence (Mode 2):
```
Elite capture divergence: [widening / stable / narrowing from step N-1] — fiscal benefit
concentration [increasing / stable / decreasing]
```

**Direction labels (Mode 2 — projection):**
- PSP direction: DECLINING (PSP fell ≥2pp from previous step), STABLE (±2pp), IMPROVING (rose
  ≥2pp). Shown in bold alongside the severity badge.
- Legitimacy direction: same 1% threshold as Mode 1.
- Elite capture: same 5% threshold as Mode 1.
- The 2pp PSP sensitivity threshold is a design decision, not a calibration claim. CM must
  confirm or adjust this threshold in their sign-off (see §M16 Implementation Gate).

**Update behaviour:** All three elements update at each step advance — same atomicity requirement
as Zone 1D per `information-hierarchy.md §Zone 1D`. The direction labels compare to the previous
step's computed value.

**Empty state (Mode 2, political economy module disabled for scenario):**
"Political risk: not modelled — enable in scenario configuration." This prompt is actionable:
the user can enable the political economy module without navigating away.

---

### Mode 3 (Active Control) — Live political risk after each control input

**Which indicators appear:** Same as Mode 2.

**Format per indicator:** Same as Mode 2, with one addition: if a control input caused a PSP
direction change (from IMPROVING to DECLINING, or vice versa), the PSP row shows a direction
reversal marker: "(reversal from previous input)". This marker persists for the current step and
clears at the next step advance.

**Update behaviour:** All three elements update after each control input propagation — same
cycle as the aggregate MDA alert panel and Zone 1A ghost/active curve update. No separate
loading state; the political risk sub-section participates in the Zone 1D atomic update.

---

## Plain-Language Sentence Specification

**Named scenario:** ZMB ECF programme at step 3. PSP = 0.38, legitimacy index = 0.42. Mode 2.

```
Zone 1D | Step 3 | ZMB ECF | Mode 2

──────── POLITICAL RISK ────────────────────────────────────────

Programme survival: CRITICAL (38%) — DECLINING
At this level, historical ECF programmes show abandonment within 3 steps.

Legitimacy index: 0.42 — declining (floor: 0.35)
  0.07 above fragility threshold

Elite capture divergence: widening — fiscal benefits concentrating

────────────────────────────────────────────────────────────────
```

**Sentence construction rules:**

"Programme survival: CRITICAL (38%) — DECLINING"
- Severity badge: CRITICAL (PSP < 0.40), WARNING (0.40–0.55), WATCH (0.55–0.70), STABLE (>0.70)
- Percentage: rounded to nearest integer (38%, not 0.3800)
- Direction label: from mode-specific contract above

"At this level, historical ECF programmes show abandonment within 3 steps."
- The historical analogue sentence. This sentence requires the PSP calibration anchor (#1084,
  G5). The specific "within N steps" figure comes from the G5 calibration document. Placeholder
  before G5 is merged: "At this level, programmes historically show elevated discontinuation risk."
  M16 implementation MUST update this to the calibrated sentence once #1084 is merged.
- Sentence is fixed text for each severity level — not dynamically computed per scenario. The
  calibration anchor (G5) establishes the historical frequency statement per severity level
  (CRITICAL, WARNING, WATCH). Dynamic scenario-specific language is M17 scope.

"Legitimacy index: 0.42 — declining (floor: 0.35)"
- Value: two decimal places (0.42, not 0.4200)
- Direction: "declining" / "stable" / "improving" (from §Mode-Specific Display Contract)
- Floor: the entity-calibrated legitimacy fragility threshold from the political economy module

"0.07 above fragility threshold"
- Computed: current value minus floor value (0.42 − 0.35 = 0.07)
- Unit: unitless distance (same units as legitimacy index)
- Label: "above fragility threshold" when above; "AT fragility threshold" at floor;
  "below fragility threshold" when below (rare — this is a severe state)

"Elite capture divergence: widening — fiscal benefits concentrating"
- Three-state label: "widening" / "stable" / "narrowing"
- Plain-language qualifier: "fiscal benefits concentrating" (widening) / "distribution stable"
  (stable) / "fiscal benefits distributing" (narrowing)
- No numeric value shown in the sub-section; the numeric value is Zone 2B content

**What the display does NOT show (and why):**
- "PSP" as an acronym: replaced with "Programme survival" — Persona 3 does not know what "PSP"
  stands for without looking it up
- "composite_score = 0.38": composite score field keys are internal; the display shows percentage
  and severity only
- "political_economy.psp": module output paths are implementation detail
- "legitimacy_index_raw": the "raw" qualifier implies a calibrated version exists, which Andreas
  cannot evaluate; only the calibrated value is shown

---

## 30-Second Legibility Check

**Scenario:** Persona 3 (Andreas Stefanidis, Senior Policy Advisor, no formal economics training)
is in a negotiating session. Mode 2. ZMB ECF at step 3. PSP = 0.38. He opens the instrument
cluster or advances to step 3. He has 30 seconds to read the political risk situation.

**What Andreas reads (from the display above, verbatim):**
- "Programme survival: CRITICAL (38%) — DECLINING"
- "At this level, historical ECF programmes show abandonment within 3 steps."
- "Legitimacy index: 0.42 — declining (floor: 0.35) · 0.07 above fragility threshold"
- "Elite capture divergence: widening — fiscal benefits concentrating"

**Time to read and act:** Line 1 is readable in 3 seconds. Line 2 (the historical analogue) is
readable in 5 seconds. Lines 3 and 4 are readable in 10 seconds each. Total: 28 seconds. ✅

**What Andreas can now say in the room (within 30 seconds, no specialist mediation):**
"Programme survival is at 38% and declining — CRITICAL. Historical programmes at this level
show abandonment within 3 steps. Legitimacy is declining and approaching the fragility threshold.
Fiscal benefits are concentrating, not distributing."

He does not need to ask what PSP stands for. He does not need a data economist present to
translate the composite score. He does not need to navigate to Zone 1D's political economy
panel in Zone 2.

**Jargon eliminated in this design (explicit list):**

1. "PSP" → "Programme survival" — replaced with a term anyone with governance experience
   understands
2. "composite_score = 0.38" → "(38%)" — percentage is universally interpretable; composite
   score with decimal is not
3. "legitimacy_index = 0.42" → "Legitimacy index: 0.42 — declining (floor: 0.35)" — the
   direction label and floor proximity convert an opaque number into an actionable signal
4. "elite_capture_divergence" → "Elite capture divergence: widening — fiscal benefits
   concentrating" — the plain-language qualifier makes the composite direction legible without
   knowing the module's field naming

**Residual specialist requirement (documented):** The historical analogue sentence ("within 3
steps") requires G5 (#1084) calibration before it can be stated with confidence. Until #1084 is
merged, the placeholder text ("elevated discontinuation risk") reduces the sentence's precision
but not its interpretability — Persona 3 can still act on "Programme survival: CRITICAL (38%) —
DECLINING" without the historical analogue. The placeholder does not constitute a kryptonite
violation; the historical analogue is an enhancement to a self-interpreting display, not the
sole means of interpretation.

---

## ADR Requirement Disposition

**Decision (b): No new ADR is required.**

The political risk summary is a Layer 3 enhancement to existing Zone 1D content within the
accepted display contract of Zone 1D. Reasoning:

1. **No new primary surface zone introduced:** The political risk sub-section lives within Zone
   1D. Zone 1D is an existing primary zone with an accepted display contract. The sub-section
   adds content below the four-framework rows — it does not create a new zone, new navigation
   element, or new viewport layout requirement.

2. **No change to Zone 1D's cognitive task contract:** Zone 1D's task remains "current-step
   readout." The political risk sub-section extends this task to include political economy
   indicators — within the same cognitive task, not a new one.

3. **ADR-013 (political economy module) is already accepted:** The political economy module's
   outputs (PSP, legitimacy index, elite capture divergence) have existing architectural
   acceptance. ADR-013 was accepted in M13. The political risk summary displays those outputs
   in the Zone 1D idiom — it does not introduce new model components.

4. **M14 G1 precedent:** The PSP self-interpreting sentence (#1075) was delivered in M14 G1
   without a new ADR. It added a sentence to Zone 1D within the accepted Zone 1D contract. G3's
   political risk sub-section extends that sentence into a structured three-element display — an
   incremental extension of the same approach.

**If the Architecture Review Facilitator disagrees with this disposition:** The Facilitator may
determine that the structured three-element display constitutes a modification of Zone 1D's
cognitive task contract sufficient to require a new ADR (under the rule that "any component
placement that conflicts with this hierarchy requires Engineering Lead sign-off" per
`information-hierarchy.md §Governing Principle`). In that case, the Facilitator names the
specific conflict at review time; this document becomes the ADR input brief; and the ADR panel
is convened before M16 sprint entry. The default disposition remains (b) — no new ADR — absent
that finding.

---

# M16 Implementation Gate

The following must be cleared before a M16 sprint entry for #987 implementation is filed.

1. **PSP historical calibration anchor (#1084, G5) — CONDITIONALLY REQUIRED:**
   The plain-language historical analogue sentence ("historical ECF programmes show abandonment
   within N steps") cannot be implemented with a specific N until G5 (#1084) is merged.
   M16 implementation may proceed with the placeholder sentence ("elevated discontinuation risk")
   before #1084 is merged — but the full historical analogue sentence is gated on G5 completion.
   M16 sprint entry may file for the full political risk sub-section but must note this dependency
   in the implementation scope. The placeholder sentence is NOT a permanent state — the sprint
   exit for #987 must confirm the historical analogue sentence is live, which requires G5 to be
   merged before M16 sprint exit.

2. **Chief Methodologist sign-off (required):** CM confirms:
   - (a) PSP severity tier assignments (CRITICAL: PSP < 0.40, WARNING: 0.40–0.55, WATCH:
     0.55–0.70, STABLE: >0.70) are consistent with historical ECF programme abandonment rates
     in the calibration dataset.
   - (b) The 2pp PSP direction change threshold (DECLINING / STABLE / IMPROVING) is appropriate
     for step-over-step sensitivity. If CM specifies a different threshold, this document is
     updated before M16 sprint entry.
   CM sign-off recorded as a review acknowledgment below or as a comment on GitHub issue #987.

3. **Zone 1D layout feasibility check (required):** Frontend Architect confirms that Zone 1D
   can accommodate the political risk sub-section (3 rows + section header + horizontal divider)
   below the four-framework rows at 1440×900 and 1280×800 without displacing the four-framework
   rows below the visible fold. If layout cannot accommodate the sub-section at 1280×800, the
   Frontend Architect proposes an alternative Zone 1D layout (e.g., collapsible "Political Risk"
   section within Zone 1D, expanded by default) before M16 sprint entry. Layout feasibility is
   a practical constraint, not a design principle constraint — the Zone 1D placement decision
   stands; the implementation form may adapt.

4. **Architecture Review Facilitator confirmation (required):** AC-7 through AC-11 confirmed
   satisfied for this document. M16 sprint entry for #987 may be filed on process grounds.

5. **No new ADR required:** Confirmed per §ADR Requirement Disposition. If the Facilitator
   overturns this at review, add: "ADR-NNN acceptance" as a dependency before proceeding to M16.

---

## Review Acknowledgments

*(Completed by reviewer at time of review — before any M16 sprint entry for #987 is filed)*

`[x]` **Chief Methodologist:** PSP severity tier thresholds (CRITICAL < 0.40, WARNING 0.40–0.55,
WATCH 0.55–0.70) confirmed consistent with historical ECF programme abandonment rates per
calibration anchor #1084 (Zambia 2022, Ghana 2023). PSP direction change sensitivity threshold
(2pp) confirmed — no adjustment required. WARNING historical analogue sentence should use
"within 6 steps" at implementation (not placeholder). M16 sprint entry for #987 may proceed
on CM grounds. 2026-06-23.

`[x]` **Architecture Review Facilitator:** AC-7 through AC-11 satisfied. ADR requirement
disposition confirmed: (b) no new ADR required. #1163 (PSP threshold legibility) is
substantively resolved by the G2 political risk sub-section design — G2 implementation
should close #1163. Note: Frontend Architect layout feasibility is a separate pre-condition;
FA conditional sign-off filed on #987 (2026-06-23). M16 sprint entry for #987 may be filed
when FA brief is authored and UX-Designer-signed. 2026-06-23.

---

*Design document version: 2026-06-21. Issue #987. M15 G3 parallel track. Implementation scope:
M16. UX Designer Agent authored. Full lifecycle authority: `docs/process/agent-execution-lifecycle.md`.*
