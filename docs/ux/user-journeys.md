# User Journeys — WorldSim Frontend

> Last significant revision: 2026-05-22
> Updated against: ADR-008 (UX Architecture) accepted 2026-05-22; five formal user personas (docs/ux/personas.md)
> Previous version context: Pre-persona-formalization — journeys anchored to generic analyst archetype

> Owned by the UX Designer Agent. Documents the primary user journeys for
> the canonical user defined in `docs/ux/north-star.md`. These journeys are
> the reference for information hierarchy decisions and for evaluating whether
> a proposed UI change supports or obstructs the user's task.
>
> Last updated: 2026-05-21 (EL Decisions 1/2/3 — Journey A Step 3 separated;
> Journey B extended for Mode 3; Journey C Mode 3 active control added;
> Journey D demonstrative entry state added; closes Issue #365).

---

## Journey A: Preparation — Building the Case

**Context:** The specialist is at her desk the evening before a negotiation
session. She has the IMF's proposed conditionality package in hand (or at
minimum, the fiscal adjustment path: the headline consolidation target,
program duration, and key structural terms). She opens WorldSim to determine
which terms, if any, produce unacceptable human cost risk and to build the
evidence base for challenging them.

**Entry state:** Application open, no scenario selected (BASELINE_VIEW).
She has the proposed parameters in a document beside her. Time is available —
she can explore over 20–40 minutes.

---

### Steps

**Step 1 — Orient: establish the analytical question**

She opens the scenarios panel. She has either (a) a scenario already prepared
from a prior session, or (b) needs to create one that models the proposed path.

*Information need at this step:* The scenario list must show name, status,
and creation date clearly enough to identify which scenario models the
current proposal. Status ("completed" / "pending") tells her whether she
needs to advance steps or can open results directly.

*Decision point:* Is there an existing scenario for this proposal? If yes →
select it (SCENARIO_PRELOADED if completed). If no → create one.

---

**Step 2 — Configure: model the proposed path**

She creates a scenario with the relevant entity (e.g., the country under
negotiation), programs the fiscal adjustment ControlInputs for the proposed
terms, and sets the number of steps to match the program horizon (typically
3–5 annual steps for an IMF program).

*Information need:* Confirmation that the scenario was created with the
correct parameters. The scenario name should reflect the proposal being
modeled ("IMF Draft 2026-04") for recall during active negotiation.

---

**Step 3 — Advance and inspect: run through the program horizon**

Step 3 has two distinct sub-actions that must not be conflated.

*Sub-action 3a — Advance:* She clicks the advance control. The simulation
computes the next step. The step counter increments ("Step N / M"). The
instrument cluster updates atomically — trajectory view curves extend to the
new step, the four-framework current position readout updates, any new MDA
alerts appear in the alert panel. This sub-action is complete when the step
counter confirms the advance.

*Sub-action 3b — Inspect:* She reads the instrument cluster at the new step.
The trajectory view shows whether any composite score is trending toward an
MDA floor. The alert panel shows whether any threshold has been crossed at this
step. She does not need to open the EntityDetailDrawer to complete the scan —
the Zone 1 instruments provide the pass/fail read.

The choropleth (geographic context) also updates at each step and is accessible
for geographic distribution inspection, but it is not the primary scan surface.
The trajectory view is.

She repeats 3a → 3b for each step through the full program horizon before
proceeding to Step 4.

*Note (M5 context):* At M5, with pre-calibration epistemic bands, each step
produces a distribution. The trajectory view renders point estimates. The
distribution detail (band width, alert_source) is accessible via the alert panel
and framework panels.

---

**Step 4 — Inspect: scan MDA alerts for threshold crossings**

She clicks on the entity of interest (the country, or a specific region) to
open the EntityDetailDrawer. She reads the MDA alert panel first.

*Information need at this step (the critical moment):*

- Which indicators have fired alerts? (indicator name, severity level)
- At what step did the alert first fire? (step_index in the subtitle)
- Is this a point-estimate alert or a distribution-source alert? (alert_source)
- How many steps remain before the breach becomes irreversible?

The alert panel must surface severity (WARNING / CRITICAL / TERMINAL) and
indicator name without scrolling. Cohort information (which income quintile)
is needed for the argument but is secondary to the alert scan.

*Decision point:*
- **No alerts fire across the full horizon** → The proposed path may be
  sustainable on the indicators the simulation covers. Shift to trajectory
  tracking: are indicators deteriorating even without breaching floors?
  Note the declared blindspots (ecological and governance scores are null
  at M4/M5 — some risk is unmodeled).
- **WARNING alerts only** → Document the indicators at risk. They may not
  justify a challenge on their own but establish a deterioration trend.
- **CRITICAL or TERMINAL alerts** → These are the primary evidence for the
  negotiating argument. Document: indicator, step, severity, cohort.

---

**Step 5 — Drill down: identify the argument components**

For each CRITICAL or TERMINAL alert, she opens the FrameworkPanel for the
relevant framework (typically human_development or financial). She examines:

- The indicator value at the alert step vs. the floor value
- The confidence tier of the indicator (a Tier 1 or Tier 2 alert is more
  defensible than Tier 4 or 5)
- The cohort breakdown: which income quintile and age band is most affected?

*Information need:* The cohort breakdown must be readable without excessive
scrolling. The confidence tier of each indicator must be visible in the
indicator row (already rendered in FrameworkPanel at M4).

*Decision point:* Is the alert based on a high-confidence indicator (Tier 1–2)
or a derived/estimated one (Tier 3–5)? A CRITICAL breach in a Tier 1 indicator
is a strong argument; a Tier 5 breach requires an epistemic caveat.

---

**Step 6 — Compare: build the counter-proposal evidence**

She creates a second scenario modeling an alternative path — the same fiscal
outcome but with softer conditionality on the terms most likely to cross
thresholds (e.g., a more gradual consolidation in year 2, or protection of
a specific social expenditure floor).

She uses compare mode (COMPARE_VIEW with DeltaChoropleth) to visualize the
divergence between the two scenarios geographically, then opens the entity
drawer for the entity of interest in the comparison scenario and verifies that
fewer alerts fire.

*Information need:* The delta choropleth must show the direction and magnitude
of divergence clearly. The entity drawer must be accessible in compare mode
for the primary scenario (it is, per ui-state-machine.md).

*Exit from this step:* She has two scenarios — the original proposal and her
counter-proposal — with documented threshold crossings in the former and
fewer/later crossings in the latter.

---

**Exit state:**

The specialist has a structured analysis:
- Which specific indicators cross thresholds under the proposed path
- At which program step each crossing occurs
- Which population cohorts bear the heaviest impact
- A counter-scenario demonstrating that alternative terms reduce crossing risk
- Confidence tier for each piece of evidence (what can be asserted with
  confidence vs. what carries model uncertainty)

She is ready to make the argument at the negotiating table.

---

## Journey B: Active Negotiation — Citing the Finding

**Context:** The specialist is in the negotiation room. IMF staff have just
proposed a specific modification to the program — or the original proposal
is being discussed and she needs to make her human cost argument. She has
WorldSim open on a tablet. She completed the preparation journey the previous
evening. The analysis is already done; she needs to retrieve and cite it
within approximately 90 seconds.

**Entry state:** Application open with the preparation scenario already
loaded and completed (SCENARIO_COMPLETE or SCENARIO_PRELOADED). The scenario
was selected either before entering the room or by quickly finding it in the
panel. People are talking. A document is on the table. The clock is running.

---

### Steps

**Step 1 — Locate: confirm the right scenario is active**

She confirms the scenario name displayed in the header matches the scenario
she prepared. If it does not, she opens the scenarios panel briefly, selects
the correct scenario, and closes the panel.

*Information need:* Scenario name in the header, readable at a glance.
The step counter confirms the scenario is at its final step ("Step 3 / 3 —
Complete" or equivalent) — meaning the analysis is fully computed.

*Critical constraint:* This step must take under 10 seconds.

---

**Step 2 — Open: tap the entity to access the drawer**

She taps the entity of interest on the choropleth map.

*Information need:* The EntityDetailDrawer must open immediately and show
measurement output — not a loading placeholder, not the "advance scenario"
placeholder. The `currentStep ?? selectedScenarioSteps` fallback (documented
in state-ownership.md) ensures this even if the status-check useEffect has
not yet resolved.

*Critical constraint:* The drawer must show data, not a loading state, within
2–3 seconds of tap. A loading spinner is acceptable briefly; a placeholder
that requires action ("advance the scenario…") is not.

---

**Step 3 — Scan: read the top MDA alert**

She reads the MDA alert panel. This is the primary surface.

*Information need in 5 seconds:*
- Severity level (WARNING / CRITICAL / TERMINAL)
- Indicator name (poverty headcount, health system capacity, etc.)
- Step index at which the breach fires
- Top affected cohort (bottom income quintile, working-age population)

The alert must be readable at tablet font sizes without scrolling.
At M5, the alert includes alert_source ("distribution" vs "point_estimate") —
this tells her whether she can say "the model confirms this breach" vs.
"the distribution places material probability at this breach."

*Decision point:*
- **Relevant alert visible immediately** → Proceed to Step 4. End-to-end
  time: under 30 seconds from picking up the tablet.
- **Relevant alert requires scrolling to find** → UX failure state.
  The top 1–3 alerts must be immediately visible (M6 design requirement:
  no scroll required for the top alerts).
- **No relevant alert for the specific modified term being discussed** →
  She must either advance a new scenario in real time (Step 5, branching
  path) or acknowledge the question and return to it at a break.

---

**Step 4 — Cite: formulate the argument**

She reads the alert as evidence, not as an alarm. The language is
declarative: "Under this path, poverty headcount crosses the critical
threshold in year 3. The simulation shows this occurs specifically for
the bottom income quintile. In comparable historical cases…"

The ia1_disclosure at the bottom of the drawer is visible. She may
reference it proactively: "These projections are from a pre-calibration
model, and even accounting for model uncertainty, the central estimate
shows year-3 breach."

*Information need:* The alert text and indicator value must be precise
enough to cite without ambiguity. The pre-calibration disclosure must
not undermine the argument — it should be frameable as epistemic honesty,
not as a caveat that invalidates the finding.

---

**Step 5 (branching) — Real-time control input via Mode 3**

If the IMF proposes a specific modification that differs from what was
prepared, and the specialist judges that 2–3 minutes are available:

She switches to Mode 3 (Active Control). She applies the proposed
modification as a control input — not as a new scenario. The baseline
ghost curves (her prepared scenario) remain visible at 50% opacity. The
active trajectory updates immediately to reflect the proposed term. The
MDA alert panel causal attribution confirms whether the proposed term is
what causes the threshold crossing she identified the night before.

*Information need:* The mode switch and first control input must be
completable in under 60 seconds. Control input propagation must update
the instrument cluster within 5–10 seconds. The live A/B comparison
(baseline ghost vs. active) must be legible at tablet font sizes without
additional interaction.

*This is a stretch use case.* The primary negotiation journey (Steps 1–4)
assumes the analysis is already complete and the specialist is citing it.
Mode 3 active control is available for real-time modification but requires
that a completed baseline scenario exists (Journey A must be complete first).

Full Mode 3 journey: Journey C below.

---

**Exit state:**

The specialist has cited a specific threshold crossing with indicator,
step, severity, and cohort. One of three outcomes:

1. **IMF acknowledges and proposes modification** → The argument achieved
   its purpose. The tool provided the analytical standing to challenge
   a specific term with quantified evidence.
2. **IMF disputes the model assumption** → This is also the intended
   outcome. The tool has shifted the negotiation to the correct level:
   methodology and assumptions, not assertion vs. assertion. The explicit
   confidence tiers and pre-calibration disclosure make this debate possible.
3. **IMF proposes a different conditionality structure** → She returns
   the tool to the preparation journey to analyze the new proposal.

---

## Journey C: Active Control — Real-Time Steering (Mode 3)

**Context:** Eleni Papadimitriou, Deputy Director, Hellenic Ministry of Finance.
February 2012. The Troika has circulated the second memorandum conditionality
package overnight. She has spent the previous three hours in Mode 2 building her
analysis and counter-proposal ("Counter_Feb2012_ModA"). At 9am she enters the
negotiation session. The Troika is now proposing a modification to the minimum
wage cut term.

**Entry state:** Application open. The "Counter_Feb2012_ModA" scenario is loaded
and complete (SCENARIO_COMPLETE, 6 steps computed). The instrument cluster is
visible at step 6. She switches to Mode 3.

*Precondition for Mode 3:* A completed baseline scenario must exist before the
first control input is applied. Journey A is the prerequisite for Journey C.

---

### Steps

**Step 1 — Switch to Mode 3**

She taps "MODE 3 — ACTIVE CONTROL" in the mode indicator in the primary viewport
header. The control plane zone (reserved in the primary viewport) populates with
the policy instruments form and the scenario shocks form. The trajectory view
remains visible — it now shows the "Counter_Feb2012_ModA" trajectory as the
baseline (single trajectory set, no ghost curves yet — observation mode).

*Information need:* The mode switch must not navigate away from the instrument
cluster. The control plane zone must be visible alongside the trajectory view
without scroll. The mode indicator must confirm she is in Mode 3.

*Critical constraint:* Mode switch must complete in under 3 seconds.

---

**Step 2 — Apply the proposed modification as a control input**

The Troika proposes: minimum wage cut applied at step 1 instead of step 2
(the 12-month delay she had built into her counter-proposal is removed).

She selects the policy input type, enters the modified parameter, selects
step 1, and clicks "Apply policy input."

The instrument cluster updates: the baseline curves are preserved as ghost
curves (50% opacity). The active trajectory recalculates to reflect the
earlier minimum wage cut. The divergence fill region appears between the
ghost and active curves where they separate.

*Information need:* The live A/B comparison must be legible immediately
after the control input computes. She must see: (a) where the active
trajectory diverges from her counter-proposal baseline; (b) whether the
divergence crosses any MDA floor. The MDA alert panel causal attribution
must show "Caused by: minimum wage cut applied at step 1."

*Critical constraint:* Control input propagation must complete in under 10
seconds. The divergence fill must appear immediately on computation complete.

---

**Step 3 — Read the causal attribution and cite the finding**

The MDA alert panel fires:
```
CRITICAL — poverty_headcount — bottom_quintile — step 2
Caused by: minimum wage cut applied at step 1
```

This is the finding. The earlier application of the minimum wage cut pushes
poverty headcount across the CRITICAL threshold at step 2 — one step earlier
than her counter-proposal baseline.

She reads the alert text directly to the Troika: "Under the proposed timing,
poverty headcount crosses the critical threshold in month 6 of the programme,
specifically for the bottom income quintile. In our counter-proposal, with the
12-month delay, the crossing does not occur."

*Information need:* The alert text must be readable at tablet font sizes without
expanding. The causal attribution must be specific enough to cite verbatim.
The ghost baseline curves must confirm that the counter-proposal baseline does
not cross the same threshold.

---

**Step 4 — Inject a scenario shock to test the Troika's rebuttal**

The Troika argues: "Even without the delay, the GDP rebound in year 2 will
protect the bottom quintile." She tests this claim by injecting a positive GDP
shock at step 2.

She uses the scenario shocks form: selects step 2, selects shock type, clicks
"Inject scenario shock." The orange vertical marker appears across all curves
at step 2. The active trajectory updates.

*Information need:* The policy input marker (blue) at step 1 and the shock
marker (orange) at step 2 must be visually distinct. The alert panel must update
to show whether the GDP shock changes the threshold crossing result. If the
crossing persists after the GDP shock, her argument is reinforced.

---

**Exit state:**

The specialist has demonstrated in real time that:
- The proposed timing change (minimum wage cut at step 1) causes a CRITICAL
  threshold crossing at step 2
- The GDP rebound assumption does not eliminate the crossing (if the alert
  persists after the shock injection)
- The causal attribution is traceable to the specific proposed term

One of three outcomes, same as Journey B Step 4, but with live evidence rather
than prepared evidence.

---

## Journey D: Demonstrative — Orientation for Aicha Mbaye

**Context:** Aicha Mbaye, IMF Executive Board Member. She has been invited to
observe a WorldSim session. She is not the driver — she will not advance steps,
apply control inputs, or configure scenarios. She needs to understand what the
instrument cluster shows, what the threshold system means, and why this tool
represents a capability shift for vulnerable-country finance ministries.

She has 60 seconds to orient before the driver begins the session. She has no
prior exposure to WorldSim.

**Entry state:** Application open, a pre-loaded historical fixture ("Greece
2010–2015, six steps") visible on a large display. The instrument cluster shows
step 1 (May 2010). Mode 1 (Replay).

This is the same scenario the driver will advance step by step. Aicha is reading
the instrument cluster, not controlling it.

---

### Steps

**Step 1 — Read the instrument cluster in 20 seconds**

The driver names each instrument once. Aicha can read the step axis annotation:
"Step 1 — May 2010 — Troika memorandum signed." She can read the four composite
score curves: financial deteriorating, human development stable, ecological
stable, governance stable.

*Orientation need:* Within 20 seconds, Aicha must be able to read: (a) what
country and time period; (b) which frameworks are deteriorating; (c) that this
is a historical replay, not a prediction.

*Design requirement this imposes:* The step axis calendar date and event label
must be readable at display-screen sizes without interaction. The entity name
must be in the persistent header. The mode indicator must confirm "MODE 1 —
REPLAY." These three elements must be legible to a cold reader with no tool
knowledge.

---

**Step 2 — MDA alert panel as threshold orientation**

The driver reads one alert: "CRITICAL — unemployment rate — working-age adults
— step 3." Aicha asks what "CRITICAL" means.

*Information need:* The severity label (CRITICAL) and the indicator and step
are readable without expansion. The driver explains: "CRITICAL means the
indicator has crossed the floor below which comparable historical cases produced
social instability. Step 3 is 2012 — two years into the programme."

Aicha does not need to interact with the panel to read the finding. She needs
to understand the hierarchy: TERMINAL > CRITICAL > WARNING.

---

**Step 3 — PMM widget as capacity orientation**

The driver points to the PMM widget: "Policy Maneuver Margin — historical: 0.23,
declining." Aicha asks what this means.

The driver explains: "This tells the minister how much policy room remains. At
0.23 and declining, the country is approaching the point where no policy response
avoids a binding constraint. In February 2012, this was already severely
constrained."

*Information need:* The PMM value and trend arrow must be legible at a glance.
The label "Policy Maneuver Margin — historical" must make the framing clear without
explanation beyond the driver's single sentence.

---

**Exit state:**

Within 60 seconds, Aicha understands:
- What the instrument cluster shows (four frameworks, shared step axis, historical
  replay)
- What threshold crossings mean and how severity is classified
- What the PMM represents and why it matters in a negotiation context

She is ready to follow the session without needing to drive the tool. The
demonstrative entry state is not a simplified mode — it is the same instrument
cluster, read by a cold observer rather than a trained driver.

*Design requirement this imposes on the instrument cluster:* Every Zone 1 element
must be self-describing enough that a cold reader can orient within one
explanatory sentence per instrument. Labels, values, and severity systems must
not require prior training to parse. This is the audience-size test: if it works
for Aicha in 60 seconds, it works for any finance ministry official who encounters
WorldSim for the first time.

---

## Journey Dependency Map

| Journey | Mode | Primary WorldSim state | Primary UI surface | Dependency |
|---|---|---|---|---|
| A — Preparation Step 3a | Mode 2 | SCENARIO_RUNNING | Trajectory view (advance confirmation) | Step counter |
| A — Preparation Step 3b | Mode 2 | SCENARIO_RUNNING | Trajectory view + MDA alert panel | EL Decision 2 viewport |
| A — Preparation Step 4 | Mode 2 | SCENARIO_RUNNING / COMPLETE | MDA alert panel | ADR-006 Decision 5 composite alert |
| A — Preparation Step 5 | Mode 2 | DRAWER_DATA | FrameworkPanel + cohort breakdown | ADR-006 Decision 4 sibling fields |
| A — Preparation Step 6 | Mode 2 | COMPARE_VIEW (single-entity) | Divergence timeline | EL Decision 3 |
| B — Negotiation Step 2 | Mode 3 | SCENARIO_PRELOADED | Instrument cluster (instant load) | currentStep ?? fallback |
| B — Negotiation Step 3 | Mode 3 | DRAWER_DATA | MDA alert panel | ADR-006 Decision 5 alert_source |
| B — Negotiation Step 4 | Mode 3 | DRAWER_DATA | ia1_disclosure text | ADR-006 Decision 13 canonical phrase |
| B — Negotiation Step 5 | Mode 3 | MODE_3_ACTIVE | Control plane + live A/B trajectory | EL Decision 3 Gap 4 |
| C — Active Control Step 2 | Mode 3 | MODE_3_ACTIVE | Trajectory view live A/B | EL Decision 3 Gap 4 |
| C — Active Control Step 3 | Mode 3 | MODE_3_ACTIVE | MDA alert panel (causal attribution) | Gap 3 blue/orange system |
| C — Active Control Step 4 | Mode 3 | MODE_3_ACTIVE | Shock marker on trajectory view | Gap 3 orange vertical marker |
| D — Demonstrative Step 1 | Mode 1 | SCENARIO_PRELOADED | Trajectory view + step axis annotation | Gap 1B fixture fields |
| D — Demonstrative Step 2 | Mode 1 | SCENARIO_PRELOADED | MDA alert panel | ADR-006 Decision 5 alert_source |
| D — Demonstrative Step 3 | Mode 1 | SCENARIO_PRELOADED | PMM widget (historical label) | Gap 5 mode-specific labels |
