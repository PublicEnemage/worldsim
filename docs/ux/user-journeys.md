# User Journeys — WorldSim Frontend

> Last significant revision: 2026-06-27
> Updated against: GD Artifact 7 (#1361) — Journey C M18 scope alignment (ADR-019 full delivery,
> all 4 steps in scope); GA-02 sequenced with M18 partial note; Journey dependency map updated.
> Previous: 2026-06-02 — Issue #576 (public advocacy journeys — Personas 6, 7, 8, 4V).

> Owned by the UX Designer Agent. Documents the primary user journeys for
> the canonical user defined in `docs/ux/north-star.md`. These journeys are
> the reference for information hierarchy decisions and for evaluating whether
> a proposed UI change supports or obstructs the user's task.
>
> Last updated: 2026-06-27 (Artifact 7 #1361 — Journey C Steps 1–4 M18 acceptance
> criteria added; GA-02 disposition note added; Journey dependency map Journey C rows
> updated to reference ADR-019. Previous: 2026-06-16 — GA-01 and GA-02 gap markers
> added to Journey A Steps 1–2).

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

*[Near-Term-Gap] — GA-01: Entity not available in the preloaded set.*

If the entity she needs is not preloaded in the system, the "If no → create
one" branch fails before it begins. At M14, the preloaded entity set is
GRC, JOR, EGY, and ZMB (EL decision 2026-06-16). Any country outside these
four — Pakistan, Kenya, Senegal, Sri Lanka, Ecuador, any country under active
IMF negotiation that is not in scope — produces a creation form with no
matching entity, no data quality preview, and no viable scenario starting
state.

This is the highest-priority data access gap in the preparation journey.
It is not a calibration gap (the model relationship is not the issue); it is
a data availability gap (the platform has no starting state for the required
entity). The user has two options today, both inadequate:

- Use GRC or another in-scope entity as a proxy → produces structurally
  wrong outputs; the human cost ledger reflects the proxy country's
  institutional and demographic starting conditions, not the target country's.
- Abandon the tool for the current negotiation → the mission has failed for
  this use case.

*Two-path resolution (staged):*

**Path 1 — User-directed query from the approved source network [M15]:**
The platform already maintains a registered source network
(`docs/data-sources/approved-sources.md`) covering World Bank Open Data, IMF
Balance of Payments Statistics, V-Dem, UNCTAD, UN Population Division, WHO
GHO, and others — all with `coverage_countries`, `simulation_variables`, and
quality tier declared in `docs/schema/database.yml §source_registry`. Path 1
extends the scenario creation form to query: "What does our registered source
network have for this entity and year?" and, where sources have coverage, to
trigger a data pull at scenario creation time rather than requiring an
administrator preload cycle.

The data quality preview (ADR-016 Component 1, M14) is the UI surface for
this: it currently shows what is preloaded; Path 1 extends it to show what is
available from registered sources and allows the user to initiate the pull.
The admin process the user described — official source onboarding with
accepted formats, license verification, `simulation_variables` mapping — is
already encoded in the source registry. Path 1 completes the circuit at
scenario creation time rather than requiring an out-of-band admin request.

This closes the entity availability gap for the majority of countries with
World Bank / IMF coverage. Countries with thin, delayed, or absent public
data fall back to the ADR-007 synthetic data framework (five-method
hierarchy: REGIONAL_AVERAGE → SYNTHETIC_COMPARABLE → STRUCTURAL_ABSENCE
chain), which already handles this case with explicit Tier 3–5 flagging.

*Design requirement:* The data quality preview panel (ADR-016 Component 1
`[data-testid="data-quality-preview"]`) must distinguish between (a) "loaded
from preloaded dataset" and (b) "available from registered source — click to
load." The pull action must complete or provide a visible progress state
within the 5-minute preparation ceiling.

**Path 2 — Ministry-owned / proprietary data upload [M16+]:**
See Gap GA-02 at Step 2 below. Path 2 is the subsequent enhancement. Path 1
is the prerequisite: the ministry must be able to confirm that the publicly
sourced baseline exists and what tier it carries before uploading proprietary
overrides that will blend with it.

*Existing artifact links:*
- `docs/data-sources/approved-sources.md` — canonical approved source list;
  Path 1's input set
- `docs/schema/database.yml §source_registry` — `simulation_variables`
  column is the existing field-to-variable mapping mechanism; `coverage_countries`
  is the entity availability index
- `docs/DATA_STANDARDS.md §Confidence Tier System` — governs how pulled data
  is tiered; user-triggered pulls follow the same rules as admin preloads
- ADR-007 (ARCH-001) — synthetic data framework; activates when Path 1 finds
  no public source coverage for a requested entity/year
- ADR-016 (ARCH-010) — data quality preview and Grounding Strip; the UI home
  for Path 1's "available / loadable" signal
- Issue #53 — Information Access Architecture (role-based output visibility);
  becomes a prerequisite for Path 2's data isolation requirement, not for Path 1

*New issue required:* File a dedicated issue for Path 1 (distinct from Issue
#53 which concerns RBAC / access control, not data ingestion). Target M15.
User story: *As Eleni in the Preparatory entry state, I need to search the
approved source network for any entity's available data before creating a
scenario, so that I am not limited to four preloaded countries when modeling
a live negotiation.*

---

**Step 2 — Configure: model the proposed path**

She creates a scenario with the relevant entity (e.g., the country under
negotiation), programs the fiscal adjustment ControlInputs for the proposed
terms, and sets the number of steps to match the program horizon (typically
3–5 annual steps for an IMF program).

*Information need:* Confirmation that the scenario was created with the
correct parameters. The scenario name should reflect the proposal being
modeled ("IMF Draft 2026-04") for recall during active negotiation.

*[Sequenced: M16+] — GA-02: Starting conditions locked to preloaded data;
no mechanism to supply ministry-owned or non-public initial state values.*

> GA-02 disposition (Artifact 7, #1361, 2026-06-27): The proprietary data upload
> path (Path 2 below) remains out of scope through M18 and is sequenced to M16+
> per the original gap text. This gap is NOT resolved by the M18 control plane
> column design package (#1354). The M18 GD package delivers `Mode2ColumnSurface`
> (ADR-019 §D-2) — a read-only scenario orientation surface in the Mode 2 column 3.
> This provides scenario identity context (name, entity, calibration vintage, horizon)
> without leaving the instrument cluster. It does NOT provide ministry-owned data
> upload, parameter override, or editable starting conditions. Those capabilities
> remain GA-02 scope. The adjacent Mode 2 parameter-access concern (fiscal multiplier
> not editable from within the cluster in Mode 2) is a known limitation of ADR-019
> §D-2 (EL Decision 1 — Mode 2 column is read-only in M18) and is sequenced to a
> future milestone as a Mode 2 column enhancement.

Even when an entity is available (preloaded or pulled via Path 1 above),
the starting conditions for every indicator are drawn exclusively from the
source registry. She cannot override or supplement them with data her
ministry holds that has not been publicly released or is more current than
the latest registered source vintage.

In practice, this means:
- The reserve figure in the simulation is the latest IMF BoP vintage (e.g.,
  2024-Q1). Her ministry's internal position as of this morning may be 0.4
  months lower — a difference that changes whether a reserve floor breach
  occurs at step 2 or step 3.
- The bilateral lending terms negotiated last month — not yet publicly
  disclosed — are not in the model. The creditor side knows these terms; her
  scenario does not reflect them.
- The draft budget scenario she is carrying into the room (not yet published)
  cannot be the scenario's starting fiscal position.

The consequence: the simulation models the publicly visible version of her
country's situation, not what her ministry actually knows. When the output
cites "Reserve coverage: 3.2 months — IMF BoP 2024-Q1 · T2" and she knows
the actual position is 2.8 months, she cannot trust the threshold crossing
timing the tool is showing her. A Layer 3 output that correctly explains
reserve coverage trajectory is worse than useless if the starting value is
wrong and she has no way to correct it.

*Two-path resolution (staged):*

**Path 1 — Approved source query [M15, GA-01 above]:**
Path 1 improves source currency (more recent vintages, more complete coverage
for more entities) but does not solve the proprietary-data problem. It is a
prerequisite for Path 2, not a substitute.

**Path 2 — Ministry-owned / proprietary data upload [M16+]:**
The ministry uploads its own starting values for specific indicators: the
actual reserve position, the bilateral lending terms, the draft budget
fiscal position. These values override or supplement the preloaded baseline
for the duration of the scenario, with full provenance and tier disclosure.

This is the asymmetry reversal the founding document describes: the ministry
brings data the creditor cannot replicate from public sources, and runs
scenarios the creditor side cannot run. No other capability delivers this.

*Architecture prerequisites for Path 2:*

1. **New provenance type — `USER_SUPPLIED`:** The ADR-016 provenance enum
   (`OBSERVED | ESTIMATED_COMPARABLE | SYNTHETIC | STRUCTURAL_ABSENCE`) must
   be extended with a fifth type: `USER_SUPPLIED`. A user-supplied value
   carries different trust characteristics from an IMF-observed value and must
   be displayed distinctly in the Grounding Strip — e.g., "Reserve coverage:
   2.8 months — Ministry of Finance (internal, 2026-06-15) · user-supplied."
   The confidence tier for user-supplied data is context-dependent: a ministry
   uploading its own budget data may justifiably claim T1 for internal purposes,
   but the tool must display user-supplied data as a distinct provenance class
   rather than conflating it with institutionally-sourced T1. This is an
   ADR-016 amendment — not a new ADR — but must be scoped before Path 2
   implementation begins.

2. **Field mapping UI — the highest Layer 3 risk in Path 2:**
   The ministry's spreadsheet calls it "FX reserves (USD billions)." WorldSim's
   canonical variable is `reserve_coverage_months` (unit: months of import
   cover). The mapping from the ministry's data format to WorldSim's canonical
   variable must be:
   (a) Explicit — the user sees "You are mapping: FX reserves (USD billions)
       → reserve_coverage_months. Conversion: at current import rate of
       [X USD/month], 4.2 billion USD = 2.8 months."
   (b) Verified before scenario creation — the transformation must be
       inspectable and confirmable within the 5-minute Preparatory ceiling.
       If the mapping takes longer than 5 minutes, the minister will rush or
       skip it; both produce misconfigured scenarios cited with false confidence.
   (c) Auditable — the transformation from uploaded value to canonical unit
       must be stored in the provenance chain (`docs/DATA_STANDARDS.md
       §Transformation Steps`), not computed silently at render time.
   The existing `simulation_variables` column in `source_registry` is the
   field mapping mechanism for admin-registered sources. Path 2 extends this
   to a user-facing, per-upload mapping step. Structured templates per data
   category (fiscal, reserve, trade, demographic) should default the common
   cases so that a 10-variable upload can be mapped in under 5 minutes for
   well-understood indicator types.

3. **Data isolation — prerequisite from Issue #53:**
   User-uploaded proprietary data must be isolated to the uploading user's
   or institution's scenarios. It must not be shared across tenants, must not
   contaminate the shared source registry, and must not appear in other users'
   data quality previews. Issue #53's role-based access control architecture
   is a direct prerequisite for Path 2's data isolation requirement. Path 2
   cannot ship without Issue #53 resolved.

4. **Scenario reproducibility caveat:**
   A scenario whose starting conditions include user-supplied data cannot be
   fully reproduced by a third party. The Grounding Strip must surface this:
   "This scenario includes ministry-supplied starting values. Reproduction
   requires the uploaded dataset." This caveat must appear at scenario creation
   and be carried in any exported output — Persona 1 (Programme Analyst) and
   Persona 6 (Investigative Journalist) both require reproducibility; they must
   be warned when a scenario cannot be reproduced from public sources alone.

*Design requirement (5-minute ceiling):*
The full Path 2 workflow — upload file → map fields → confirm transformation
→ review provenance display → create scenario — must complete within 5 minutes
for a ministry analyst who is not a software engineer and is working from a
standard spreadsheet export format. This is the binding constraint on the
field mapping UI design. Any mapping workflow that exceeds this ceiling will
be skipped or rushed, producing misconfigured scenarios.

*Existing artifact links:*
- `docs/schema/database.yml §source_registry` — `simulation_variables` is the
  existing field mapping mechanism; `transformations` list in DATA_STANDARDS is
  the transformation audit trail
- `docs/DATA_STANDARDS.md §Transformation Steps` — transformation documentation
  standard; Path 2 uploads must satisfy this standard
- ADR-016 (ARCH-010) — provenance object; `USER_SUPPLIED` type must be added
  before Path 2 implementation; amendment to §API contracts
- ADR-007 (ARCH-001) — synthetic data framework; user-supplied data sits above
  synthetic in the tier hierarchy but below institutionally-observed; the
  updated tier stack becomes: observed-public → user-supplied → synthetic →
  structural-absence
- Issue #53 — Information Access Architecture; RBAC is a hard prerequisite for
  Path 2 data isolation; Path 2 must not be scoped without Issue #53 resolved
- `docs/data-sources/approved-sources.md` — approved source list; Path 2 does
  not add to this list (ministry data is user-session-scoped, not platform-wide)

*New issue required:* File a dedicated issue for Path 2 (distinct from Issue
#53 and from the Path 1 issue). Target M16+, design-first (ADR required
before implementation). The design work — field mapping UX, USER_SUPPLIED
provenance type, isolation model — should begin in M15 parallel to Path 1
implementation. User story: *As Eleni in the Preparatory entry state, I need
to upload my ministry's non-public starting values for specific indicators
and have them reflect in the scenario's initial state with full provenance
disclosure, so that my analysis reflects what my government actually knows
rather than only what has been publicly released.*

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

> **M18 scope (Artifact 7, #1361, 2026-06-27):** All four Journey C steps are
> delivered in M18 G4 per ADR-019 (EL Decision 6 — all 7 shock types in G4).
> No steps are deferred post-M18. Acceptance criteria for each step are annotated
> below, tied to ADR-019 decisions. The ADR is `Proposed` pending independent UX
> Designer sign-off (separate EL-triggered session, NM-042). G4 implementation
> begins on ADR-019 `Accepted`.

**Context:** Eleni Papadimitriou, Deputy Director, Hellenic Ministry of Finance.
February 2012. The Troika has circulated the second memorandum conditionality
package overnight. She has spent the previous three hours in Mode 2 building her
analysis and counter-proposal ("Counter_Feb2012_ModA"). At 9am she enters the
negotiation session. The Troika is now proposing a modification to the minimum
wage cut term.

**Entry state:** Application open. The "Counter_Feb2012_ModA" scenario is loaded
and complete (SCENARIO_COMPLETE, 6 steps computed). The instrument cluster is
visible at step 6. Mode 2 column shows `Mode2ColumnSurface` — scenario identity
block read-only + "Enter Active Control" button (M18 delivery, ADR-019 §D-2).

*Precondition for Mode 3:* A completed baseline scenario must exist before the
first control input is applied. Journey A is the prerequisite for Journey C.

---

### Steps

**Step 1 — Switch to Mode 3**

She clicks "Enter Active Control" in the `Mode2ColumnSurface` panel (column 3 of
the instrument cluster). The control plane column transitions from the read-only
`Mode2ColumnSurface` to the interactive `ControlPlaneColumn` — Form 1 (policy
instruments, blue `#0284c7`) and Form 2 (scenario shocks, orange `#ea580c`) are
now visible. The trajectory view remains visible — it now shows the
"Counter_Feb2012_ModA" trajectory as the baseline (single trajectory set, no ghost
curves yet — observation mode).

*Information need:* The mode switch must not navigate away from the instrument
cluster. The control plane zone must be visible alongside the trajectory view
without scroll. Both Form 1 and Form 2 headers must be visible without scroll at
1280×800. The column must confirm she is in active control mode.

*Critical constraint:* Mode switch must complete in under 3 seconds.

> *M18 acceptance criteria (ADR-019):*
> - `Mode2ColumnSurface` renders in Mode 2 column 3; `data-testid="enter-active-control-btn"` present (§D-2)
> - On click, `ControlPlaneColumn` mounts (lazy mount — §D-1, Issue #1217)
> - Both Form 1 header ("POLICY INSTRUMENTS") and Form 2 header ("SCENARIO SHOCKS") visible without scroll at 1280×800 (§D-3)
> - Mode switch completes ≤ 3 seconds; trajectory view remains uninterrupted
> - AC-014 extended: both form headers at 1280×800 asserted in Playwright

---

**Step 2 — Apply the proposed modification as a control input**

The Troika proposes: minimum wage cut applied at step 1 instead of step 2
(the 12-month delay she had built into her counter-proposal is removed).

She selects `FiscalMultiplier` from the Form 1 policy input type selector,
enters the modified parameter value, selects step 1 from the "Apply at step"
selector, and clicks "Apply policy input."

The instrument cluster updates: the baseline curves are preserved as ghost
curves (50% opacity). The active trajectory recalculates to reflect the
earlier minimum wage cut. The divergence fill region appears between the
ghost and active curves where they separate. The applied input appears in
the policy inputs history list below Form 1.

*Information need:* The live A/B comparison must be legible immediately
after the control input computes. She must see: (a) where the active
trajectory diverges from her counter-proposal baseline; (b) whether the
divergence crosses any MDA floor. The MDA alert panel causal attribution
must show "Caused by: minimum wage cut applied at step 1."

*Critical constraint:* Control input propagation must complete in under 10
seconds. The divergence fill must appear immediately on computation complete.

> *M18 acceptance criteria (ADR-019):*
> - Form 1 type selector (`data-testid="policy-input-type-selector"`) shows `FiscalMultiplier` and `LegitimacyConstraint` (§D-3)
> - `POST /scenarios/{id}/branch` extended with `legitimacy_index: float | None` (§D-4)
> - Applied input appears in `data-testid="policy-inputs-history"` (§D-3)
> - Live A/B divergence fill visible ≤ 10 seconds after button click, without any additional navigation
> - Ghost curves (50% opacity) and active curves (100%, 2px) simultaneously visible in trajectory view

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

> *M18 acceptance criteria (ADR-019):*
> - Blue policy inflection marker (`#0284c7`) visible at step 1 in TrajectoryView (Artifact 4 Dimension 5 Layer B)
> - MDA alert causal attribution shows "Caused by: [policy input]" in blue text when `cause_type = "policy"` (Artifact 4 Dimension 5 Layer D, §D-5 backend extension)
> - Alert text readable at 1024×768 tablet viewport without drawer interaction
> - Ghost baseline curves confirm counter-proposal baseline does not cross the same threshold at the same step

---

**Step 4 — Inject a scenario shock to test the Troika's rebuttal**

The Troika argues: "Even without the delay, the GDP rebound in year 2 will
protect the bottom quintile." She tests this claim by injecting a positive GDP
growth shock at step 2.

She uses the Form 2 scenario shocks section: selects `GrowthShock` from the
shock type selector, sets `growth_rate_delta` to match the Troika's rebound
projection, sets `distribution_asymmetry` to reflect upper-cohort growth skew,
selects step 2, and clicks "Inject scenario shock." The orange vertical marker
appears across all curves at step 2. The active trajectory updates.

*Information need:* The policy input marker (blue) at step 1 and the shock
marker (orange) at step 2 must be visually distinct. The alert panel must update
to show whether the GDP shock changes the threshold crossing result. If the
crossing persists after the GDP shock, her argument is reinforced: the GDP
rebound does not protect the bottom quintile under the conditionality structure.

> *M18 acceptance criteria (ADR-019):*
> - Form 2 shock type selector shows all 7 types including `GrowthShock` (§D-6, EL Decision 6)
> - `GrowthShock` parameters: `growth_rate_delta`, `duration_steps`, `distribution_asymmetry` shown in form (§D-6)
> - `POST /scenarios/{id}/inject-shock` endpoint accepts `ShockInjectRequest` (§D-5); dispatched via `SHOCK_REGISTRY` → `GrowthShockHandler` (§D-7, §D-8)
> - `TrajectoryStep.shock_events` populated at `inject_at_step`; orange `<ReferenceLine>` rendered in TrajectoryView (§D-9)
> - Injected shock appears in `data-testid="shock-events-history"` (§D-3)
> - Blue marker (step 1) and orange marker (step 2) visually distinct simultaneously
> - Alert panel shows shock-caused attribution in orange (`#ea580c`) when `cause_type = "shock"`
> - AC-015: GrowthShock injection with `growth_rate_delta = -0.03` produces GDP composite score divergence > 0.005 at step+1 vs. pre-shock trajectory

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

## Journey E: Story Investigation — The Journalist's Session

**Context:** Farida Haidari, Senior Correspondent, Economic Desk, Dawn, Karachi. She is
investigating the combined effect of Pakistan's IMF energy subsidy removal (June 2022) and
the catastrophic 2022 floods on food security for the bottom income quintile in Sindh. She
has a 2-hour session cap and no economist to mediate output for her. She arrives with a
specific hypothesis: the combined shock broke the programme's bottom-quintile protection
assumption in a way the IMF's programme design did not surface. She needs one publishable
sentence confirmed or refuted.

**Entry state:** Application open, no scenario selected (BASELINE_VIEW). IMF 7th EFF review
documents beside her. Time: 2 hours maximum.

*Critical Layer 3 constraint:* This journey must be completable by a user who has no
specialist economics training. At every step where the tool requires domain knowledge to
proceed, the journey fails. Configuration field labels, alert text, and source attribution
must all be interpretable without a Ph.D. economist in the room.

---

### Steps

**Step 1 — Orient: identify the comparison question**

She reads the scenario list. There are no pre-built scenarios for Pakistan 2022. She must
create two: Scenario A (programme + subsidy removal, no flood) and Scenario B (programme +
subsidy removal + flood displacement). She creates Scenario A first.

*Information need at this step:* The scenario creation form must present field labels in
plain language. "Energy subsidy removal" and "income displacement shock" must be recognizable
as the inputs she is configuring — not require econometric vocabulary to describe.

*Critical constraint:* She must be able to create Scenario A without opening a help document
or asking a specialist what a field means. Configuration path must take under 15 minutes.

---

**Step 2 — Run Scenario A: programme-only baseline**

She advances Scenario A through 2 steps. The MDA alert panel at each step shows no CRITICAL
food security alert — consistent with the IMF programme design's assumption that the targeted
subsidy scheme protects the bottom quintile from the energy price shock alone.

*Information need:* The MDA alert panel shows either (a) no alert, or (b) a WARNING-or-below
alert for food security. This confirms that the programme-only path, absent the flood, does
not breach the critical threshold. The absence of a CRITICAL alert is itself a finding —
she records it.

*Decision point:*
- **CRITICAL alert fires in Scenario A** → The programme design was inadequate even without
  the flood. Her hypothesis is partially wrong; the finding is stronger. She adjusts the
  narrative.
- **No CRITICAL alert in Scenario A** → Programme-only path holds. Proceed to Scenario B.

---

**Step 3 — Create Scenario B: add the flood displacement shock**

She creates Scenario B, identical to Scenario A with one addition: an agricultural income
displacement shock applied at step 1 representing the flood's impact (30% reduction in
agricultural income for 2 steps in flood-affected regions).

*Information need:* The shock input type must be selectable and its parameters
(magnitude, duration, target entity) must be configurable without specialist mediation.
The parameter labels must match her understanding of what the flood did: income loss, not
a technical propagation coefficient.

---

**Step 4 — Run Scenario B: read the combined-shock finding**

She advances Scenario B through 2 steps. The MDA alert panel fires.

*Information need — the critical moment of this journey:*

The alert panel must produce a plain-language statement that Farida can read directly:
- What happened (indicator name in English, not econometric notation)
- To whom (income cohort, not a model variable name)
- When (step index, not an internal state label)
- How severe (severity level, translated to plain language if possible: "CRITICAL" is
  acceptable; "HDI propagation chain floor breach" is not)

The source registry ID for each cited indicator must be visible — she needs to be able
to state in her article: "According to a WorldSim simulation drawing on [source], the
[indicator] for [cohort] crossed a [severity] threshold at [step]."

*Decision point:*
- **CRITICAL alert fires at step 1** → Hypothesis confirmed. The combined shock broke
  the protection assumption one step earlier than the programme model accounted for.
  She has the sentence.
- **No CRITICAL alert in Scenario B** → Hypothesis refuted or the confidence tier on
  the flood shock is too low to produce a CRITICAL breach. She either adjusts the shock
  magnitude or reports: "Our simulation found no critical threshold crossing under the
  combined shock conditions modeled — which conflicts with subsequent household data."

---

**Step 5 — Extract the citable sentence**

She reads the MDA alert. The primary finding is: "Under combined shock conditions
[programme + flood], food security for the lowest income quintile crossed a CRITICAL
threshold at step 1. Under programme-only conditions, this threshold was not breached."

She records:
- The alert text verbatim
- The source registry ID for the food security indicator
- The confidence tier (she will note this in the methodology note)
- The scenario parameters (what inputs produced this finding, for reproducibility)

*Information need:* The alert text must be specific enough to quote as a sentence without
requiring her to translate it. The ia1_disclosure must be visible and must be frameable as
epistemic honesty, not as a disqualifying caveat.

---

**Exit state:**

Farida has one of two outcomes:
1. **Hypothesis confirmed** — She has a specific, citable threshold crossing that was not
   in the official programme analysis. The article can state: "A simulation analysis shows
   that the combined shock broke the programme's protective assumption for the lowest income
   quintile at step 1 — a finding absent from the IMF's 7th review documentation."
2. **Hypothesis refuted** — The simulation does not confirm the combined-shock breach at
   CRITICAL severity. She reports the negative result honestly and investigates whether the
   confidence tier or model calibration explains the discrepancy.

In either case, the tool has served the journalism use case: it has provided a specific,
traceable, transparent analytical finding — not a narrative claim.

---

## Journey F: Legislative Brief — The Parliamentary Economist's Preparation

**Context:** James Ochieng, Senior Economist, Kenya Parliamentary Budget Office. 72 hours
before the Finance Committee hearing on the 7th IMF EFF programme review. He needs to
independently assess whether the 3.5% GDP consolidation path crosses human development
thresholds that the Treasury's programme presentation does not flag, and whether a 2%
alternative path avoids those crossings. The output is a 4-page committee brief in Hansard-
citable form.

**Entry state:** Application open, no scenario selected (BASELINE_VIEW). IMF 7th EFF
documents, KNBS data, and Treasury fiscal framework on his desk. Preparatory entry state.
72 hours available but the brief must be written, reviewed internally, and submitted before
the hearing. Session budget: 4–6 hours across the 72-hour window.

*Critical constraint:* James's brief will be cited in Hansard. Every finding must carry
an explicit confidence tier, a citable methodology source, and must be reproducible if
re-run during the hearing day. Non-reproducible or confidence-tier-absent outputs cannot
appear in the brief.

---

### Steps

**Step 1 — Orient: plan the two-scenario comparison**

He reviews the IMF 7th review documents. He identifies the two paths to compare:
- Scenario A: 3.5% GDP consolidation per IMF EFF recommendation (4 annual steps)
- Scenario B: 2% alternative consolidation (same fiscal sustainability requirement, gentler path)

He confirms that Kenya's baseline data is available in WorldSim or must be seeded. He
reads the source registry to confirm which Kenya indicators are at Tier 1–2 (World Bank
WDI, IMF Article IV) vs. Tier 3 (synthetic comparables for subnational indicators).

*Information need:* The source registry must be accessible from the tool and must allow
him to verify which Kenya data points are available and at what confidence tier before
he builds the scenario.

---

**Step 2 — Create and run Scenario A: programme path**

He creates Scenario A — Kenya, 3.5% fiscal consolidation, 4 annual steps. He seeds the
initial attributes from the Kenya 2022 baseline (KNBS, IMF data). He advances all 4 steps.

At each step, he reads the MDA alert panel and trajectory view. He records:
- Which indicators cross WARNING or CRITICAL thresholds
- At which step each crossing first occurs
- The confidence tier of each indicator

*Information need:* The step-level output must be readable without opening a drawer. The
trajectory view shows the composite score curves; the MDA alert panel shows the specific
threshold crossings with indicator name, step, severity, and confidence tier.

---

**Step 3 — Create and run Scenario B: alternative path**

He creates Scenario B — Kenya, 2% fiscal consolidation, same 4 steps. He advances all
4 steps and records which threshold crossings, if any, occur under the softer path.

*Decision point:*
- **Scenario B shows no threshold crossings where Scenario A shows crossings** → The
  alternative path avoids the human development cost identified in Scenario A. The
  committee brief can cite the specific delta: "The programme path triggers X threshold
  crossing(s) that the 2% alternative path avoids within the 4-step horizon."
- **Scenario B also shows threshold crossings** → The fiscal sustainability floor is the
  binding constraint regardless of pace. The brief will note which crossings are
  pace-sensitive and which are structural.

---

**Step 4 — Open comparison view: document the divergence**

He opens the comparison view (COMPARE_VIEW) between Scenario A and Scenario B. The
divergence timeline shows where the two paths separate and at what step each scenario's
composite scores diverge.

*Information need at this step — Hansard standard:*
- Specific indicator names at which the paths diverge, with step-level precision
- Confidence tier for each diverging indicator
- Whether the divergence is within or outside the pre-calibration uncertainty band
- Whether the methodology source (the ADR governing the fiscal multiplier or indicator
  propagation) can be cited by reference number

He extracts the tabular data: indicator, step A crossing, step B crossing, delta in
crossing timing, confidence tier.

---

**Step 5 — Access methodology documentation for citation**

Before drafting the brief, he navigates to the methodology source for the key findings.
For the fiscal multiplier assumption: he needs the ADR number and version to cite.
For the human development propagation chain: he needs the documented calibration source.

*Information need:* The methodology documentation must be accessible from within the
tool without navigating to an external GitHub repository or documentation site. He must
be able to cite: "WorldSim simulation (ADR-XXX, version M10) projects..."

*Design requirement this imposes:* A path from any indicator output to its governing
ADR reference must be present in the instrument cluster. This is not currently confirmed
as implemented — see US-036.

---

**Step 6 — Draft the committee brief**

He drafts the 4-page brief from the tabular output. He cites the tool, the ADR, the
confidence tier per indicator, and the comparison finding. He submits it for internal
PBO review before the hearing.

*Information need:* The tabular output must be extractable (ideally downloadable; if not,
readable for manual transcription). The brief must be draftable within 2 hours from the
scenario run output.

---

**Exit state:**

James has a committee brief that:
- Names the specific human development threshold crossings under the programme path,
  with indicator, step, severity, and confidence tier
- Names the crossings avoided under the 2% alternative path
- Cites the methodology by ADR reference and pre-calibration disclosure
- Is reproducible during the committee hearing if a member requests re-running

The brief's value is specificity: "The programme path triggers an education spending
WARNING at step 2 and a healthcare capacity WARNING at step 3, which the 2% alternative
path avoids within the 4-step horizon." This is the finding the committee minority report
needed.

---

## Journey G: Accountability Monitoring — The Civil Society Monitor's Review

**Context:** Abena Osei, Programme Economist, SEND Ghana. Six months into Ghana's IMF ECF
programme (signed May 2023, $3B), her field monitoring shows social protection spending
below the programme's committed floor. She has 30 days to produce a monitoring brief for
Parliament, the IMF Mission Chief, and community organizations in northern Ghana. The brief
must be citable, specific, and legible to a community audience without university education.

**Entry state:** Application open, no scenario selected (BASELINE_VIEW). Ghana ECF
programme document and Treasury quarterly expenditure data beside her. Retrospective
entry state (accountability tracking sub-mode — reference path known: the programme's
committed trajectory. Exercise: verify whether observed actuals track it).

*Panel ruling (Decision 2 — Option C):* This journey uses Mode 2 to reproduce the
committed programme baseline. The observed-actuals comparison overlay — inputting real
step-level expenditure data into the tool for divergence calculation — is not yet a
platform capability. Steps 1–5 below represent current capability. Steps 6–7 are
[Phase-3-TBD] and are the formal input to Phase 3 (Issue #577).

---

### Steps

**Step 1 — Orient: reproduce the committed baseline inputs**

She reads the Ghana ECF programme document. She identifies the committed programme inputs:
social protection spending floor (as a percentage of GDP), healthcare floor commitment,
baseline GDP growth assumption, initial poverty headcount.

She creates Scenario A — Ghana, ECF programme inputs, 4 steps — using the committed
spending levels as the initial attributes and fiscal parameters. This is the reference
scenario: what should happen if the programme's commitments are honored.

*Information need:* The scenario inputs must map to the programme document's terminology.
She must be able to say: "I am entering the programme's committed social protection floor
as this input field."

---

**Step 2 — Advance Scenario A: the committed baseline trajectory**

She advances all 4 steps. She records the projected trajectory for social protection
spending, poverty headcount, and child nutrition at committed spending levels.

*Information need at this step — the accountability reference:*
- At committed spending levels, does child nutrition hold below WARNING across all 4 steps?
- At committed spending levels, does poverty headcount decline or hold stable?
- What specific indicator values does the simulation project at committed spending?

These values become the accountability baseline: what the programme committed to produce.

---

**Step 3 — Create Scenario B: observed (below-committed) spending**

She creates Scenario B — identical to Scenario A, except she enters the observed social
protection spending level (0.3 percentage points of GDP below the committed floor, per
Treasury quarterly data).

*Information need:* The spending parameter must be editable as a direct input without
requiring her to model the fiscal mechanics. She enters: "Social protection spending:
0.9% of GDP" rather than "Apply a negative fiscal impulse of 0.3% GDP to the social
protection transfer function."

---

**Step 4 — Advance Scenario B: identify the threshold crossing**

She advances all 4 steps. She records where the below-committed spending scenario diverges
from the committed baseline.

*Decision point:*
- **Scenario B crosses child nutrition WARNING where Scenario A does not** → The social
  protection floor shortfall directly drives a threshold crossing that the programme's
  commitment was designed to prevent. This is the accountability finding.
- **Both scenarios cross the same thresholds** → The floor shortfall is not the binding
  factor for this specific indicator. She investigates which indicator shows the
  most meaningful divergence.

---

**Step 5 — Compare: document the commitment gap**

She opens the comparison view (COMPARE_VIEW). The divergence between Scenario A
(committed) and Scenario B (observed) shows: at committed spending, child nutrition
holds below WARNING at step 2. At observed spending, child nutrition crosses WARNING
at step 2 and approaches CRITICAL at step 4.

The accountability brief states: "The social protection floor shortfall is projected to
drive child malnutrition above warning threshold by step 2. This is the specific outcome
the programme's floor commitment was designed to prevent. At committed spending levels,
this threshold crossing does not occur within the 4-step programme horizon."

*Design requirement this imposes:* The comparison view must surface per-indicator
threshold crossing timing with enough precision for the brief ("step 2" not "early
in the programme"). The committed vs. observed scenario labels must be clearly
distinguishable in the comparison output.

---

**Step 6 — [Phase-3-TBD] — Observed-actuals overlay**

This step does not exist in the current architecture. The platform capability required:
Abena inputs actual quarterly Treasury expenditure data for each step — not as a
scenario parameter but as observed real-world actuals — and the tool overlays those
actuals against the simulation's projected trajectory for each indicator.

This would produce: "At step 1, simulation projected 1.2% GDP in social protection;
observed: 0.9% GDP. Divergence: −0.3 percentage points. Projected threshold crossing
without remediation: step 2." This is the direct accountability overlay.

*Why this is [Phase-3-TBD]:* No current mode accepts real-world observations as step-level
inputs alongside a simulation trajectory. The architecture would require a new data
ingestion path and a new rendering mode in the trajectory view. The DIC panel (Issue #577)
must assess whether this capability belongs in an extended Mode 1 ("observed-actuals replay"),
a new Mode 4, or as a post-processing overlay on existing trajectory output.

---

**Step 7 — [Phase-3-TBD] — Community-audience output layer**

The monitoring brief must be legible to a community leader in northern Ghana without a
university education. The current tool produces technical output: trajectory curves,
composite scores, confidence tiers, ADR references. None of these are directly legible
to a community audience without translation.

The platform capability required: a separate output layer that renders the same finding
in plain language — per commitment, per indicator — without the technical scaffolding.
"The government spent less than it promised on social protection. Our simulation shows
this shortfall is likely to drive malnutrition above safe levels by [date]. This is the
specific risk the programme's protection commitment was designed to prevent."

*Why this is [Phase-3-TBD]:* The current rendering pipeline has one output mode. A
separate community-audience rendering layer requires a new content type — not a different
chart but a different document — with different vocabulary rules, different confidence
disclosure conventions (simplified but not dishonest), and different export format.

---

**Exit state:**

Abena has a two-layer output:
- Technical layer (for the parliamentary and IMF audience): step-level comparison of
  committed vs. observed spending scenarios, with indicator-specific threshold crossings,
  confidence tiers, and ADR references. Completable with current platform.
- Community layer (for northern Ghana community organizations): plain-language summary
  of which commitments are being honored and which are not, with human-cost consequences
  stated plainly. Requires [Phase-3-TBD] community-audience rendering capability.

The accountability finding — that the social protection floor shortfall drives a specific
indicator threshold crossing that committed spending would have prevented — is produceable
from the current platform (Steps 1–5). The integrated overlay and community layer require
Phase 3 architectural work.

---

## Journey H: Backtesting with Personal Observation — The Personal-Connection Researcher

**Context:** Dr. Priya Krishnaswamy, Research Associate, Centre for Development Studies,
Thiruvananthapuram. She wants to use WorldSim to backtest India's 2020 farm law
deregulation against her Wardha district field data (47 households, 2015 survey plus
2021 follow-up). Her father is a cotton farmer in Wardha district. She is both academic
evaluator and personally invested in the simulation's accuracy. She enters in Evaluative
mode (reads methodology documentation first) before running the Retrospective (backtesting)
session.

**Entry state:** Application open. She reads methodology documentation before touching the
simulation. Evaluative mode first, then transition to Retrospective for the backtesting run.

*Critical trust condition:* When the simulation's output diverges from her field data,
she needs to see the specific model assumption that drives the divergence. A confidence
tier disclaimer is insufficient — she needs the mechanism, not just the uncertainty level.

---

### Steps

**Step 1 — Evaluate: read the agricultural income transmission methodology**

She navigates from the instrument cluster to the methodology documentation. She reads:
(a) What policy input type covers agricultural price floor removal?
(b) What is the propagation chain from farm gate price to household food security?
(c) What comparison group is used for India agricultural income estimates?
(d) What confidence tier applies to Vidarbha cotton farm income estimates?

*Information need:* The methodology documentation path must be accessible from the
instrument cluster without navigating to an external site. The agricultural propagation
chain (if implemented) must be documented with the specific elasticities used and the
source for each.

*Decision point:*
- **Agricultural income transmission chain is documented and implemented** → Proceed
  to Step 2 with trust that the simulation can answer her research question. Note the
  comparison group for potential divergence analysis.
- **Agricultural income transmission chain is not yet implemented** → [Near-Term-Gap].
  The simulation cannot serve her primary research question. She documents this as a
  calibration gap and uses WorldSim for the available indicators (rural poverty headcount,
  food security) rather than the full agricultural chain. See US-045.

---

**Step 2 — Configure: create the India farm law backtesting scenario**

She creates a backtesting scenario: India, 2020-2021, 2 annual steps, starting from the
pre-farm-law deregulation baseline. She applies the policy input: farm law deregulation
(effective removal of MSP price floor guarantee) at step 1.

*Information need:* The policy input for MSP price floor removal must be available in the
ControlInput taxonomy. If it is not (likely a [Near-Term-Gap] at M10), she uses the closest
available instrument (general agricultural subsidy change) and notes the calibration
approximation.

---

**Step 3 — Advance: record the projected agricultural income trajectory**

She advances through 2 steps. She records the projected values:
- Agricultural income trajectory for cotton farmers (rural Maharashtra)
- Household food security indicator
- Child nutrition indicator (if available)

*Information need:* The step-level indicator values must be readable without opening a
drawer. The confidence tier for each indicator must be visible per indicator.

*She records the simulation's prediction:* "Income decline projected at 18% at step 1
(Maharashtra agricultural comparables, Tier 3 SYNTHETIC_COMPARABLE)."

---

**Step 4 — Compare: her field data vs. the simulation**

She takes the simulation's projected trajectory and compares it manually to her Wardha
field data: 23% income decline observed in 2021 follow-up survey (47 households).

Divergence: 5 percentage points. The simulation underpredicts the income decline.

*Information need at this step — the core trust test:*

She needs to see why the simulation predicts 18% when her data shows 23%. The tool must
show the specific assumption driving the divergence:
- "Comparison group: Maharashtra agricultural averages (not Wardha district)"
- "Elasticity: -0.18 per MSP removal unit (from Maharashtra state regression)"
- "Wardha cotton specific: no Wardha district data available in comparison group"

If the tool cannot show this assumption, she cannot include the simulation in a journal
submission — the divergence is uninterpretable without knowing its source.

*Design requirement this imposes:* From any indicator output, the user must be able to
navigate to the specific comparison group and elasticity assumption that produced that
value. This requires methodology transparency at the assumption level, not just at the
ADR level. Current capability: ADR-level documentation accessible. Assumption-level
display: [Near-Term-Gap] — engineering work to surface the specific comparison group
ID and elasticity value in the indicator display.

---

**Step 5 — Interpret: accept or challenge the divergence**

Priya reads the comparison group disclosure: "Maharashtra agricultural comparables (not
Wardha district-specific)." She accepts the 5-point divergence as within the plausible
range for district-level vs. regional estimation. Wardha district has historically
performed worse than Maharashtra state average on agricultural income volatility — a
finding documented in her dissertation.

She notes: the simulation is calibrated to state-level patterns; her field data is
district-level. The divergence is methodologically expected, not a model error. She
can include the simulation in her journal submission with appropriate qualification:
"WorldSim projects a 18% decline using Maharashtra state agricultural comparables
(Tier 3 SYNTHETIC_COMPARABLE); our Wardha district field data shows 23%. The 5-point
difference falls within the plausible range for district-level vs. state-level estimation."

*Information need:* The confidence tier system must show SYNTHETIC_COMPARABLE with the
comparison group ID exposed. The user must be able to state, in one sentence, what
comparison group produced the estimate.

---

**Step 6 — Export: download trajectory data for journal appendix**

She exports the simulation's full trajectory output — projected agricultural income,
food security indicator, confidence tier per indicator, comparison group — as a
structured data file (CSV or JSON) for inclusion in her journal submission as a data
appendix.

*Information need:* The export format must include: indicator name, step, projected
value, confidence tier, comparison group ID, synthetic method flag, source registry IDs.
These fields are all present in the Quantity schema (QuantitySchema + ADR-007 fields).
The missing piece is a download path from the instrument cluster to this structured file.

This is [Near-Term-Gap] — the data exists; the export path does not.

---

**Step 7 — [Phase-3-TBD] — X-ray layer: structural dependency visualization**

In a subsequent session, Priya wants to show her research seminar the full causal chain
from the farm law policy input to the food security indicator. She wants a visualization
that traces: MSP price floor removal → farm gate price reduction → farm income decline →
debt service default → food expenditure reduction → child malnutrition indicator.

This is not a trajectory chart. It is a network graph showing the multi-hop causal
path through the propagation engine — the "X-ray layer" of the simulation. It answers:
"What is the model's theory of causation from policy input to human cost indicator?"

*Why this is [Phase-3-TBD]:* The current trajectory view renders outcomes (composite
scores, indicator values) across time. It does not render the causal structure that
produces those outcomes. A causal-graph visualization requires a new rendering mode —
one that reads the propagation engine's relationship graph and displays it as a navigable
dependency chain. This could live in Zone 2 (navigable context) without conflicting with
Premise 1 (Zone 1 instruments always visible). The DIC panel (Issue #577) must assess
the architectural requirements and whether this belongs in M11 or M12 scope.

---

**Exit state:**

Dr. Krishnaswamy has produced:
- A backtesting comparison between the simulation's projected agricultural income
  trajectory and her Wardha field data, with the specific comparison group and
  divergence interpretable
- The comparison group disclosure and confidence tier qualification for her journal
  submission
- A gap identification: the agricultural income transmission chain requires Wardha
  district-specific calibration (not currently available); this is a data gap she
  can document and contribute to the comparison group registry

The [Phase-3-TBD] items — trajectory export and the X-ray causal graph — are the
Phase 3 inputs for the DIC architectural review.

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
| B — Negotiation Step 5 | Mode 3 | MODE_3_ACTIVE | Control plane + live A/B trajectory | ADR-019 D-1, D-3 |
| C — Active Control Step 1 | Mode 2→3 | MODE_3_ACTIVE | Mode2ColumnSurface → ControlPlaneColumn (lazy mount) | ADR-019 D-1, D-2 |
| C — Active Control Step 2 | Mode 3 | MODE_3_ACTIVE | Trajectory view live A/B + policy inputs history | ADR-019 D-3, D-4 |
| C — Active Control Step 3 | Mode 3 | MODE_3_ACTIVE | MDA alert panel (causal attribution, blue) | ADR-019 D-3; Dimension 5 Layer B/D |
| C — Active Control Step 4 | Mode 3 | MODE_3_ACTIVE | Shock form + orange trajectory marker + alert update | ADR-019 D-5, D-6, D-7, D-8, D-9 |
| D — Demonstrative Step 1 | Mode 1 | SCENARIO_PRELOADED | Trajectory view + step axis annotation | Gap 1B fixture fields |
| D — Demonstrative Step 2 | Mode 1 | SCENARIO_PRELOADED | MDA alert panel | ADR-006 Decision 5 alert_source |
| D — Demonstrative Step 3 | Mode 1 | SCENARIO_PRELOADED | PMM widget (historical label) | Gap 5 mode-specific labels |
| E — Investigation Step 3 | Mode 2 | SCENARIO_RUNNING | MDA alert panel (plain language) | US-030 plain-language requirement |
| E — Investigation Step 4 | Mode 2 | COMPARE_VIEW | MDA alert panel (differentiated) | US-033 comparison differentiation |
| E — Investigation Step 5 | Mode 2 | DRAWER_DATA | Source attribution at indicator level | US-034 [Near-Term-Gap] |
| F — Legislative Brief Step 3 | Mode 2 | SCENARIO_RUNNING | Trajectory view + MDA alert panel | US-035 comparison |
| F — Legislative Brief Step 5 | Mode 2 | COMPARE_VIEW | Divergence timeline with indicator specificity | US-038 confidence tier in comparison |
| F — Legislative Brief Step 6 | Mode 2 | COMPLETE | Methodology documentation path | US-036 ADR reference accessible |
| F — Legislative Brief Step 7 | Mode 2 | COMPLETE | Downloadable tabular output | US-037 [Near-Term-Gap] |
| G — Accountability Step 2 | Mode 2 | SCENARIO_RUNNING | Trajectory view (committed baseline) | US-040 baseline reproduction |
| G — Accountability Step 4 | Mode 2 | COMPARE_VIEW | Divergence view (committed vs. observed spending) | US-041 spending comparison |
| G — Accountability Step 5 | [Phase-3-TBD] | ACTUALS_OVERLAY | Observed-actuals input + overlay | US-042 [Phase-3-TBD] |
| G — Accountability Step 6 | [Phase-3-TBD] | ACTUALS_OVERLAY | Community-audience output layer | US-043 [Phase-3-TBD] |
| H — Backtesting Step 1 | Mode 1 | BASELINE_VIEW | Methodology documentation | US-044 method docs accessible |
| H — Backtesting Step 3 | Mode 1 | SCENARIO_RUNNING | Trajectory view (agricultural chain) | US-045 [Near-Term-Gap] |
| H — Backtesting Step 5 | Mode 1 | COMPLETE | Divergence explainability (assumption visible) | US-047 [Near-Term-Gap] |
| H — Backtesting Step 6 | Mode 1 | COMPLETE | Trajectory data export | US-046 [Near-Term-Gap] |
| H — Backtesting Step 7 | [Phase-3-TBD] | XRAY_LAYER | Structural dependency visualization | US-048 [Phase-3-TBD] |
| Mode 1 COMPARE_VIEW | Mode 1 | COMPARE_VIEW | Inline fixture picker + dual-curve trajectory view + delta MDA panel | US-049 (closes #451) |
