# User Journeys — WorldSim Frontend

> Owned by the UX Designer Agent. Documents the primary user journeys for
> the canonical user defined in `docs/ux/north-star.md`. These journeys are
> the reference for information hierarchy decisions and for evaluating whether
> a proposed UI change supports or obstructs the user's task.
>
> Last updated: 2026-05-02 (initial journeys; two primary flows documented).

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

**Step 3 — Advance: run through the program horizon**

She advances the scenario step by step. At each step she can observe the
choropleth update and see how the attribute distribution shifts across the
country's regions or indicators.

*Information need:* The step counter ("Step N / M") must confirm each advance
completed. The choropleth color shift gives a geographic first-pass signal
before she drills into entity detail.

*Note (M5 context):* At M5, with pre-calibration epistemic bands, each step
now produces a distribution. The choropleth continues to render the point
estimate. The distribution detail is in the entity drawer.

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

**Step 5 (branching) — Real-time scenario advance**

If the IMF proposes a specific modification that differs from what was
prepared, and the specialist judges that 2–3 minutes is available to
run a new scenario:

- She opens the panel, creates a scenario with the modified parameters,
  selects it, advances 3 steps, and opens the entity drawer.

*Information need:* The scenario creation and 3-step advance must be
completable in under 3 minutes with the scenario panel open. Each advance
button click must respond within 5–10 seconds (acceptable latency for a
live simulation advance).

*This is a stretch use case.* The primary negotiation journey assumes
the scenario is already complete. Real-time advance is available but is
not the designed flow for the active negotiation mode.

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

## Journey Dependency Map

| Journey | Primary WorldSim state | Primary UI surface | ADR-006 dependency |
|---|---|---|---|
| Preparation — Step 4 | SCENARIO_RUNNING / COMPLETE | MDA alert panel | Decision 5 composite alert |
| Preparation — Step 5 | DRAWER_DATA | FrameworkPanel + cohort breakdown | Decision 4 sibling fields |
| Preparation — Step 6 | COMPARE_VIEW | DeltaChoropleth + EntityDetailDrawer | None (M4 feature) |
| Negotiation — Step 2 | SCENARIO_PRELOADED | EntityDetailDrawer (instant open) | currentStep ?? fallback |
| Negotiation — Step 3 | DRAWER_DATA | MDA alert panel | Decision 5 alert_source field |
| Negotiation — Step 4 | DRAWER_DATA | ia1_disclosure text | Decision 13 canonical phrase |
