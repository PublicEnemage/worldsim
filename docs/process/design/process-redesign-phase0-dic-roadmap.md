# Phase 0 — Council Orchestrator ROADMAP
## Domain Guardrails and Capability Gap Priorities for UX/Persona Traceability Upstream of ADR Development

**Authored by:** Council Orchestrator  
**Date:** 2026-06-08  
**Phase:** Phase 0 — UX/Persona Traceability Upstream of ADR Development  
**Sprint entry:** `docs/process/sprint-plans/process-redesign-phase0-sprint-entry.md`  
**Status:** COMPLETE — Step 1 output filed. Prerequisite for Step 2 (UX Designer) and Step 3 (Business PO).  
**Canonical location:** `docs/process/design/process-redesign-phase0-dic-roadmap.md`

---

## Activation Record

Council Orchestrator activated in ROADMAP mode for Phase 0. Activation prompt:

> `Council Orchestrator: ROADMAP — domain guardrails for UX and capability gap priorities (Phase 0 — UX/Persona Traceability Upstream of ADR Development)`

**Mandatory reading confirmed before activation:**
- `docs/vision/worldsim-founding-document.md` — read in full
- `docs/ux/north-star.md` — read in full
- `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md` — read in full
- `docs/ux/personas.md` — read in full (all nine personas, all marquee cases)
- `SESSION_STATE.md`, `CLAUDE.md`, `docs/process/agents.md` — read per session protocol

**Standing Phase 0 DIC agents activated (blind interview protocol):**
Each agent was activated independently without access to any other agent's output. Independence is the epistemic value; pre-contaminated assessments defeat the purpose.

1. Development Economist — guardrails + capability gap priorities
2. Chief Methodologist — guardrails
3. Intergenerational Advocate — guardrails
4. Investment Agent (CATALYTIC mode) — art of the possible + capability gap priorities

---

## Part I — Blind Interview Records

*Each record below reflects the agent's independent perspective, produced without access to any other agent's findings. The tensions between perspectives are surfaced in Part II.*

---

### Interview 1 — Development Economist

**Speaks for:** Human development; Sen capability approach; HDI; distributional effects on cohorts.  
**Phase 0 question:** What must the ADR persona/UX traceability requirements never compromise from your framework's perspective? What are five binding requirements your domain places on how ADRs document connection to user needs?

---

The founding document names what is actually at stake in this process redesign: "financial recovery is not the same as recovery." The Greece 2010-2015 case made this visible — GDP turning marginally positive at step five while unemployment remained at 26.5%. That is not a simulation finding. That is what happened to real people. The ADR authorship process must be designed so that no ADR can be accepted whose capability improves the visibility of financial trajectory without simultaneously improving the visibility of human development trajectory at equivalent resolution. That is my first and most fundamental requirement.

**Binding Requirement DE-1: Human cost ledger parity is a per-ADR architectural obligation, not a standing convention.**

An ADR that touches Zone 1 layout, instrument weighting, trajectory display, or information hierarchy must explicitly state whether the human cost ledger retains equal visual weight to financial indicators after the proposed change. This must be a named acceptance criterion, not an assumed invariant. "Equal visual weight" means: in the primary viewport, without navigation, the human development trajectory occupies the same visual real estate as the financial trajectory. If an ADR modifies this balance, the ADR must document why and the deviation requires Engineering Lead exception. Demoting the human cost ledger to secondary position — even temporarily, even for a specific mode or entry state — is a mission violation that cannot be resolved by convention.

*Why this is binding and not aspirational:* DEMO4-005 established that the HCL indicator was computed but invisible. The computation was correct; the display was absent. ADR-012 did not require HCL visibility as an acceptance criterion. If DE-1 had been in the ADR template, "HCL visible in Zone 1D" would have been a named architectural requirement, not an implementation assumption.

**Binding Requirement DE-2: Persona traceability must name the income cohort served, not just the persona.**

A persona trace that says "serves Finance Ministry Negotiator (Persona 2)" does not answer the distribution question. Persona 2's marquee case (The Second Memorandum) is about arguing that a specific conditionality term crosses a CRITICAL threshold for the bottom income quintile at step 2. The ADR capability that serves this use case must name the cohort: "enables visibility of bottom-quintile poverty headcount trajectory under conditionality scenarios." An ADR that traces to a persona without naming the cohort the persona is trying to see has not answered what the persona actually needs.

*Specific cohorts that must be nameable by any ADR serving Personas 2, 3, or 5:* bottom two income quintiles; pensioners above 65 (major public transfer recipients); youth aged 18-35 in the tradable sector; children 0-5 (early childhood development indicators). An ADR for a display or analytical capability that cannot specify which of these cohorts it makes visible is an ADR for an aggregate capability only.

**Binding Requirement DE-3: Capabilities that add composite scores must document the disaggregation pathway.**

A composite Human Development score is a summary. The distributional finding — which cohort crossed which threshold — is the mission-relevant output. An ADR that adds a composite without specifying when and how users can access the per-cohort breakdown has sealed the distributional information behind the aggregate. The requirement: any ADR introducing a composite indicator must specify (a) that per-cohort breakdown is accessible from the composite display surface, (b) how many interactions it takes to reach the breakdown, and (c) whether the breakdown is accessible in the Reactive entry state (the most demanding condition). If the breakdown requires more than two interactions from the composite display in Reactive state, the ADR must document why and the deviation requires Engineering Lead exception.

**Binding Requirement DE-4: Persona traces must specify entry state, not just persona.**

Persona 2 in Preparatory state (three hours before briefing the minister) and Persona 2 in Reactive state (90 seconds to reach a specific threshold crossing) have structurally different information access requirements. An ADR that traces to "serves Finance Ministry Negotiator" without specifying the entry state cannot be verified against the right acceptance criterion. The ADR acceptance criterion must name: "In [entry state], the user can reach [specific indicator/cohort/step] in [maximum time or interaction count]."

The Development Economist's stake in entry state specificity: the bottom-quintile poverty headcount trajectory is what Persona 2 needs in Reactive state. If the ADR traces to Persona 2 generally, the implementation may serve Preparatory state well while remaining inaccessible in Reactive state — and the ADR's acceptance criterion will pass because the general persona trace is satisfied.

**Binding Requirement DE-5: ADRs for capabilities that aggregate across cohorts must document the additive vs. distributional analysis distinction.**

Aggregate GDP, aggregate employment, aggregate poverty headcount — these are legitimate indicators. But the mission of this tool is to surface what aggregates hide. An ADR that introduces an aggregate without documenting how the tool will show what is hidden behind it is not serving the mission as fully as it could. The requirement: for any new aggregate indicator, the ADR must either (a) specify the disaggregated view that complements the aggregate, or (b) explicitly acknowledge that disaggregated data is unavailable and document this as a known limitation in the instrument. Option (b) is acceptable. Option (a) is preferred. The absence of either is not acceptable.

**Development Economist — Capability Gap Priorities**

These are the analytical capabilities most directly relevant to the finance minister's negotiating position that well-resourced actors have and WorldSim's intended users do not.

*Gap DEG-1 — Cohort disaggregation as first-class output, not drill-in:* Bottom quintile, youth, pensioners as named indicators in Zone 1, visible without navigation in all three modes. The M11.5 usability sessions confirmed this is absent. The IMF's own distributional analysis tools surface cohort effects; the finance ministry side needs the same.

*Gap DEG-2 — Multiplier sensitivity map (human cost version):* At which fiscal multiplier values does the human cost trajectory cross CRITICAL thresholds? Not "what does the economy do at multiplier 1.5?" but "at what multiplier value does poverty headcount cross CRITICAL, and for which cohort first?" This is the Persona 1 marquee case made real. Blanchard-Leigh established the multiplier was 1.5; the question "what did that mean for the bottom quintile?" has never been given a systematic answer in any public tool.

*Gap DEG-3 — Human cost attribution chain:* Which specific conditionality term drove which threshold crossing. Without attribution, the finding supports a general claim but not a specific negotiating challenge. "Poverty headcount crosses CRITICAL at step 2" is a finding. "Poverty headcount crosses CRITICAL at step 2 because of the minimum wage cut applied at step 1, not the pension reduction" is a negotiating position.

---

### Interview 2 — Chief Methodologist

**Speaks for:** Statistical integrity; uncertainty quantification; distributional honesty.  
**Phase 0 question:** What must the ADR persona/UX traceability requirements never compromise from your framework's perspective? What are five binding requirements your domain places on how ADRs document connection to user needs?

---

The founding document states: "The model's blindspots are documented and visible. We are calibrated, not confident." That is an epistemic commitment that requires structural enforcement. The current ADR process does not enforce it. An ADR can be authored, panel-reviewed, and accepted without anyone verifying that the uncertainty representation requirement has been carried from the ADR level through the implementation to the display. My five requirements close that gap.

**Binding Requirement CM-1: Every ADR introducing a new output format must specify the uncertainty representation requirement alongside the format specification.**

Separating format design from uncertainty display creates predictable implementation failure. If an ADR specifies that an indicator shows as a bar chart without specifying whether the bar shows the confidence interval, the implementation will default to the simpler option — the point estimate — because the uncertainty requirement was not architectural. The correction: ADRs must include an "uncertainty display specification" section for every new output format. This section must name: (a) what confidence tier information is displayed, (b) where it appears relative to the indicator value, (c) what it shows for Tier 3 and Tier 4 estimates, and (d) what the IA1_CANONICAL_PHRASE equivalent is for this indicator type.

This requirement is not satisfied by a reference to "confidence tiers are displayed per the standard." That is a reference, not a specification. An ADR that cannot specify the uncertainty display for the capability it is introducing has not completed its methodological obligation.

**Binding Requirement CM-2: ADR persona traces must specify how the named persona encounters uncertainty disclosures.**

"Serves Persona 5 (Institutional Decision-Maker) who needs a clear directional signal" is an incomplete persona trace. Persona 5 also needs to know when that directional signal is based on a Tier 3 synthetic estimate, because a finding she cites as authoritative that is later shown to be Tier 3 will destroy the tool's credibility in exactly the institutional context where it most needs to build it. The requirement: for any ADR tracing to Persona 5, the persona trace must specify how pre-calibration disclosure appears in the Demonstrative entry state — which is Persona 5's primary access mode. A 5-minute demonstration that surfaces the finding without surfacing the confidence tier is a demonstration that has omitted the epistemic qualification the founding document requires.

Generalized: for any persona in any entry state, the ADR's persona trace must state how uncertainty is communicated in that specific context. The communication mechanism may be different in Reactive state (brief tier indicator adjacent to the alert) versus Preparatory state (full distribution band with coverage percentage) — but it must be specified, not assumed.

**Binding Requirement CM-3: ADR persona traces must name what the named persona does when the output's confidence is insufficient.**

An ADR for a capability that traces to Persona 2's Reactive entry state must also specify: "when the cited indicator is Tier 3 or lower, the MDA alert reads [X] and the user is told [Y]." This prevents the class of failure where the tool serves the use case perfectly for Tier 1 data and fails it silently for Tier 3 data — the exact data environment that the target users most commonly operate in. A persona trace that specifies only the success path has not addressed the use case's failure mode.

The founding document's "No False Precision" principle requires more than not lying about precision. It requires not being silent about imprecision. An ADR whose persona trace implies the capability serves the persona without specifying how it behaves when data quality is insufficient has created a half-specification that the implementation will complete in whatever way is most convenient.

**Binding Requirement CM-4: Confidence tier display is a named acceptance criterion in any ADR introducing a new indicator, at the indicator level.**

Not "confidence tiers are displayed per the standard" but "for indicator [X], the confidence tier is displayed as [specific UI element] in [specific location] under [specified conditions], including when confidence is Tier 3 (synthetic comparable) and Tier 4 (structural extrapolation)." The acceptance criterion must be falsifiable by inspection: a reviewer looking at the implemented indicator must be able to verify the criterion is met without referring to a separate standard document.

This requirement exists because confidence tier display is consistently deprioritized at implementation time when the ADR treats it as implied rather than specified. The six-indicator suite in M11 had three indicators whose confidence tier display was incomplete at merge; this would have been caught at ADR acceptance if CM-4 had been in the template.

**Binding Requirement CM-5: Any ADR introducing a new capability must specify the "meaninglessness threshold" behavior — what the tool produces when uncertainty is too large to be directionally informative.**

The founding document states: "When uncertainty is so large the output is directionally meaningless, the tool says so rather than generating an uninterpretable band." This is a design principle that must have an architectural expression in every ADR that introduces measurement capability. The requirement: ADRs must include a "structural absence / meaninglessness threshold" section specifying (a) what conditions trigger a Structural Absence Declaration for this capability, (b) what the user sees when the declaration fires, and (c) what action the user can take in response (e.g., "consult the data source registry to identify which inputs would reduce uncertainty below the threshold").

An ADR whose capability has no specified meaninglessness behavior will, at implementation, either generate an uninterpretable band (violating No False Precision) or silently omit the indicator (violating the user's expectation that a named capability is always present).

---

### Interview 3 — Intergenerational Advocate

**Speaks for:** Future generations; irreversible thresholds; discounting injustice.  
**Phase 0 question:** What must the ADR persona/UX traceability requirements never compromise from your framework's perspective? What are five binding requirements your domain places on how ADRs document connection to user needs?

---

Every MDA threshold this simulation enforces is a statement about irreversibility. Below this threshold, the damage is not recoverable within a planning horizon. The founding document builds the aviation analogy precisely here: the Minimum Descent Altitude exists because below it, standard recovery procedures no longer work. When the tool allows an MDA TERMINAL crossing to be visually minimized, scrolled past, or architecturally demoted, it has constructed an instrument that shows the danger and then lets the user look away. My requirements exist to prevent that.

**Binding Requirement IA-1: Any ADR modifying the MDA alert panel's placement, visibility, or severity display must explicitly certify that TERMINAL alert severity remains visually distinct from WARNING with no implementation discretion.**

This is not a UX preference. TERMINAL is architecturally defined as an irreversible threshold crossing — a trajectory below which standard recovery procedures do not apply. If TERMINAL reads the same as WARNING on the instrument cluster, the user has no architectural signal that they are facing an irreversible condition rather than a recoverable one. The requirement: ADRs that touch the alert panel must include an acceptance criterion of the form: "TERMINAL alert [indicator] is visually distinguishable from WARNING at viewport [minimum supported size] without user interaction, with no color scheme or display configuration that renders them visually equivalent."

*Why "no implementation discretion":* if the ADR allows the implementation to interpret this requirement, the implementation will choose whatever is visually simplest. TERMINAL must read as TERMINAL. The ADR must be specific enough that the QA test for this criterion can be written before implementation begins.

**Binding Requirement IA-2: ADRs introducing or modifying MDA alerts must document the "irreversibility justification" for each threshold.**

An MDA floor is a claim about irreversibility. That claim requires justification — why does falling below this specific value produce damage that cannot be undone within a reasonable horizon? If the justification does not exist in the ADR, it will not exist in the implementation, and it will not exist for the user. The requirement: for each MDA threshold defined or modified by an ADR, the ADR must include: (a) the specific irreversibility claim (what becomes irreversible past this threshold, and over what horizon), (b) the empirical basis for the claim (historical cases, literature), and (c) the confidence tier of that empirical basis. A threshold without an irreversibility justification is a line drawn in sand. The ADR must make it a line drawn in evidence.

**Binding Requirement IA-3: Persona traces must specify the "generational horizon" coverage of the capability being introduced.**

A capability that shows poverty headcount trajectory for the next five programme steps is valuable. A capability that shows poverty headcount trajectory for the next five programme steps without indicating that the early-childhood malnutrition at step 2 will compound into lifetime capability deficits past step 10 is an incomplete capability. The requirement: any ADR for a capability that produces human development outputs must specify whether the output horizon is sufficient to capture the compounding effects of the identified threshold crossings. If the output horizon is insufficient, the ADR must document this as a known limitation — not silently.

Concretely: "This capability shows poverty headcount trajectory for 8 steps. Early childhood malnutrition effects compound over 15-20 years; this output does not capture those effects. Users requiring long-horizon intergenerational analysis should consult [forward capability reference]." This documentation is a user-protection requirement, not a self-deprecation exercise.

**Binding Requirement IA-4: Any ADR modifying the alert panel's scroll behavior or visible count must certify that TERMINAL and CRITICAL alerts are visible without scroll at the minimum supported viewport.**

The founding document states that the Intergenerational Advocate's guardrail is: "Irreversible thresholds must never be renderable as ignorable." An alert that requires scroll to reach is, in a Reactive entry state, an alert that may not be seen. The requirement: ADRs that modify the visible alert count, scroll behavior, or panel height must include an acceptance criterion: "Under scenario [X] with [N] active alerts at severity [Y], all TERMINAL and CRITICAL alerts are visible without scroll at viewport [minimum supported dimensions]." This criterion must be tested in CI against representative alert scenarios, not spot-checked at implementation.

**Binding Requirement IA-5: ADRs for infrastructure capabilities must trace their impact on irreversibility signal latency.**

ADR-009 (matrix computation engine) does not directly touch the alert display. But computation model choices affect which indicators can be computed in real time during Mode 3 steering — and if the matrix engine introduces latency that delays MDA alert updates, a user in an active Mode 3 session could cross an irreversible threshold before the alert appears. The requirement: ADRs for infrastructure capabilities that affect computation timing or event propagation must include a "signal latency impact" statement: "This change does/does not affect the latency between a threshold crossing event and the appearance of the corresponding MDA alert. [If does:] the new latency is [X]; the maximum acceptable latency for TERMINAL alerts is [Y]; this change [meets/does not meet] that requirement."

This requirement may produce "not applicable" statements for most infrastructure ADRs. The discipline of writing "not applicable" is the enforcement mechanism — it forces the ADR panel to consider the question, not assume the answer.

**Intergenerational Advocate — Capability Gap Priorities**

*Gap IAG-1 — Generational horizon view:* The programme window is 5-8 steps. The intergenerational effects of early childhood malnutrition, education system degradation, and youth unemployment extend 15-25 years. Sophisticated actors model these extended horizons in their scenario planning. The tool's ability to show "this poverty headcount at step 2 translates into this lifetime capability reduction for the current cohort of 5-year-olds" would be transformative for the institutional decision-maker use case.

*Gap IAG-2 — Early childhood development as named first-class indicator:* Child malnutrition, school enrollment rates, under-5 mortality — these are the indicators with the longest compounding tails. They are currently absent as named indicators. Their absence means the founding document's claim to surface what aggregates hide is incomplete in exactly the domain where hiding is most consequential.

---

### Interview 4 — Investment Agent (CATALYTIC mode)

**Speaks for:** Private capital; art of the possible; capability gap framing against the competitive landscape.  
**Phase 0 question:** What are the binding requirements your domain places on ADR traceability from the "art of the possible" and asymmetry-closing perspectives? What capability gaps should the roadmap prioritize to close the analytical asymmetry?

---

Mode: CATALYTIC. The mission of this tool is to close a specific asymmetry: a well-resourced actor at one side of the negotiating table has analytical capabilities that the less-resourced actor does not. My job in this ROADMAP activation is to name the asymmetry precisely — what can the powerful side see that WorldSim's users cannot? — and translate that into ADR authorship requirements and capability priorities.

**Binding Requirement INV-1: Every ADR for a new analytical capability must include an "asymmetry assessment."**

The asymmetry assessment is a one-paragraph statement: "Well-resourced actors with [Bloomberg/sovereign wealth fund models/IMF proprietary tools] can currently [describe the capability]. WorldSim's proposed ADR-N [closes/partially closes/does not address] this gap by [description]. The remaining gap after this ADR is [description]." Without this assessment, the ADR panel cannot verify that the capability being introduced is genuinely mission-serving versus technically interesting but asymmetry-neutral.

This requirement is most important for capabilities where the development team's instinct is "this is obviously useful." Obvious usefulness to engineers does not establish usefulness to the negotiating party with limited analytical resources. The asymmetry assessment forces the question: useful compared to what the other side has, for a user with what resources?

**Binding Requirement INV-2: ADRs for External Sector capabilities must name the investment signal they enable for the sovereign.**

Reserve drawdown, current account dynamics, FDI inflows, capital account balance — these are the signals that determine whether private capital enters or exits. They are also the signals that the IMF's own analysis tracks, that creditor syndicates monitor, and that sovereign wealth funds use to assess country risk. An ADR for External Sector capabilities that cannot name the investment signal it enables for the sovereign — "this capability allows the finance ministry to see the same reserve drawdown trajectory that the creditor team's models are using to assess rollover risk" — has not answered why this capability serves the mission.

**Binding Requirement INV-3: ADRs that introduce new analytical capabilities must specify the minimum data tier at which the capability produces actionable output.**

If a capability requires Tier 1 data to produce meaningful output, and the target user operates in a Tier 3-4 data environment, the capability's effective accessibility is zero for that user. The accessibility gap must be named in the ADR, not discovered post-implementation. The requirement: "This capability produces actionable output at data Tier [minimum tier]. For users in Tier 3-4 environments, the synthetic data inference pathway that extends this capability is [defined/undefined]. [If undefined:] this is a capability accessibility gap that must be addressed before this capability is considered mission-complete for target users in thin-data environments."

**Binding Requirement INV-4: Persona traces must include a "negotiating leverage statement" — what specific argument the named persona can make in a negotiation as a result of this capability.**

A technically comprehensive module that does not change the negotiating conversation has low mission priority. An ADR trace to "serves Persona 2 (Finance Ministry Negotiator)" is complete only if it specifies: "After accessing this capability, Persona 2 can make the following specific argument that she could not make before: [statement]." The argument must be citable and specific. "Better analysis of fiscal dynamics" is not a negotiating argument. "Poverty headcount for the bottom income quintile crosses CRITICAL at step 2 under the proposed minimum wage reduction, which our analysis shows is avoidable under the counter-proposal" is a negotiating argument.

**Binding Requirement INV-5: Roadmap prioritization must be stated in terms of asymmetry-closing impact, not analytical completeness.**

When Phase 0 outputs inform roadmap sequencing, the sequencing criterion should not be "which capability is most technically complete" or "which is most interesting to build." It should be: "which capability most directly changes what a finance ministry with limited resources can argue in a negotiation with a well-resourced counterparty?" Technical completeness and mission impact are correlated but not equivalent. ADR authorship requirements should include a one-paragraph "mission impact statement" that forces the panel to answer this question before acceptance.

**Investment Agent — Capability Gap Priority List (Art of the Possible)**

The following represent analytical capabilities that are asymmetrically available to well-resourced actors and either absent from WorldSim or present but not accessible to the target user in their most demanding entry state. Each is classified by asymmetry severity and recommended roadmap horizon.

*Gap INV-G1 — Multiplier sensitivity analysis as first-class UI function (CRITICAL asymmetry, IMMEDIATE):*  
IMF staff and sovereign wealth fund analysts can model fiscal multiplier sensitivity as a routine procedure. The founding document's eureka moment is literally about this — the Greek programme used a multiplier assumption that was wrong, and no tool existed to show the human cost implications at the correct multiplier. WorldSim can compute this; it is not surfaced as a primary user-facing function accessible to Persona 2 in Preparatory state. Closing this gap partially closes the most important analytical asymmetry in the tool's founding narrative.

*Gap INV-G2 — Real-time reserve drawdown arc under trade/external shocks (CRITICAL asymmetry, IMMEDIATE):*  
Sovereign debt traders and creditor analysis teams monitor reserve drawdown trajectories continuously. The ministry's inability to show the same trajectory means they are in negotiations where one side knows the reserve constraint and the other is arguing from GDP projections. DEMO4-001 was the technical failure; the mission failure was deeper — this is one of the asymmetry-closing capabilities the founding document is built around. The wiring exists (ExternalSectorModule events → reserve_coverage_months); the channel must be completed.

*Gap INV-G3 — Conditionality term attribution: which term drives which crossing (CRITICAL asymmetry, IMMEDIATE):*  
Troika negotiating teams know which conditionality terms have the largest human cost effects — that is institutional knowledge built over decades of programme design. A finance ministry that can show "the minimum wage cut at step 1, not the pension reduction, drives the CRITICAL poverty threshold crossing at step 2" has access to the same analysis. This is the Case 2 marquee case's core requirement. Without it, the tool produces findings but not negotiating positions.

*Gap INV-G4 — Historical precedent pattern matching (HIGH asymmetry, NEAR-TERM):*  
Sovereign debt analysts at hedge funds maintain proprietary historical pattern libraries. "This trajectory resembles Argentina 2000 at step 3" is a capability that requires institutional memory and private data on the creditor side. WorldSim's backtesting infrastructure contains the historical data; the pattern matching interface is not built. This is the Persona 3 marquee case's primary requirement.

*Gap INV-G5 — Multi-scenario PMM comparison view (HIGH asymmetry, NEAR-TERM):*  
A ministry that can show "under the proposed programme, PMM narrows to 0.1 at step 2; under our counter-proposal, it remains above 0.3" has changed the conversation from assertion to evidence. This is Mode 3's primary negotiating value proposition. The analytical capability exists; the side-by-side PMM comparison display is not built as a first-class view.

---

## Part II — Council Compilation: Tensions, Convergences, and ROADMAP Outputs

*Council Orchestrator synthesizing the four independent blind interviews. Tensions are surfaced first. Convergences follow. Neither resolves the tension — both are real.*

---

### Tensions Between Framework Perspectives

**Tension 1 — Cognitive load vs. methodological completeness (Chief Methodologist vs. UX North Star's Persona 5)**

The Chief Methodologist's binding requirements (CM-1 through CM-5) require uncertainty disclosures, meaninglessness thresholds, and per-indicator confidence tier display as architectural obligations. Persona 5 (Institutional Decision-Maker) fails her use case when the first screen requires explanation before she can read it. Her preferred format is "three formats and no others: traffic light, one-sentence finding, single annotated chart." Comprehensive uncertainty display and Persona 5's 5-minute window are in genuine tension.

*Council finding:* This tension cannot be resolved by choosing one side. The Chief Methodologist's requirements protect the tool's epistemic integrity; Persona 5's requirements protect institutional adoption. The resolution belongs at the ADR authorship level: an ADR serving Persona 5 must specify how uncertainty is communicated *within* the 5-minute window, not whether it is communicated. The "one-sentence finding per framework" format the persona specifies has room for "with [Tier 2] confidence" as a parenthetical. The ADR traceability requirements must require both: (a) the persona's time window is met, and (b) the uncertainty tier is visible within that time window. Neither requirement waives the other.

**Tension 2 — Intergenerational horizon extension vs. Reactive entry state immediacy**

The Intergenerational Advocate requires that ADRs document generational horizon coverage and that capabilities show whether their output horizon is sufficient to capture compounding effects. Persona 2 in Reactive state needs to reach a specific indicator-step-cohort answer in 90 seconds. Generational horizon documentation may add display complexity that degrades the 90-second retrieval.

*Council finding:* The tension is real but the resolution is progressive disclosure, not trade-off. The 90-second primary display shows the programme-window indicator. The generational horizon documentation is accessible from that display for users who need it — a single interaction that expands the timeline. The ADR requirement: the generational horizon information must be accessible within two interactions from the primary instrument, and the primary instrument must indicate whether the identified threshold crossing has long-horizon effects (a visual indicator, not a navigation requirement).

**Tension 3 — Asymmetry-closing prioritization (Investment Agent) vs. distributional depth (Development Economist)**

The Investment Agent prioritizes capabilities by their impact on the negotiating conversation — multiplier sensitivity, reserve drawdown attribution, conditionality term attribution. The Development Economist prioritizes capabilities by cohort disaggregation depth — bottom quintile visibility, youth indicator granularity, early childhood development. The two lists overlap but are not identical.

*Council finding:* The Development Economist's priority list is about what the tool must show to be mission-complete. The Investment Agent's priority list is about what the tool must show to change the negotiating conversation. The highest-leverage point is where the two lists intersect: multiplier sensitivity applied to specific cohorts (DE-G2 + INV-G1 as a combined requirement), and conditionality term attribution at the cohort level (DE-G3 + INV-G3 combined). ADRs for these capabilities should be framed as joint requirements, not separate features.

---

### Convergences Across All Four Agents

**Convergence C-1: The "done" definition must include observable analytical output, not just code correctness.**

All four agents independently produced requirements that boil down to this: an ADR acceptance criterion that says "the capability is implemented" is not sufficient. The acceptance criterion must say "the capability produces observable output that the named persona can use in their most demanding entry state." Development Economist requires cohort visibility in Reactive state. Chief Methodologist requires uncertainty display in every entry state. Intergenerational Advocate requires TERMINAL alert visibility without scroll. Investment Agent requires that the negotiating argument is produceable from the capability. None of these is satisfied by "PR merged and CI green."

**Convergence C-2: Capability gaps are most dangerous when they create silent false confidence.**

DEMO4-001 (reserves frozen, module appearing to function) is the canonical example. All four agents named versions of the same failure: a capability that appears to work but produces misleading output is worse than a capability that is absent, because the user does not know to distrust it. The ADR traceability requirement must include a "silent failure mode" assessment: what does this capability produce when it appears to be working but the underlying data, channel, or propagation is absent or broken? An ADR whose capability has no specified silent failure mode has not completed its quality obligation.

**Convergence C-3: The founding document's north star is not self-executing — it requires structural embodiment.**

The Development Economist, Chief Methodologist, Intergenerational Advocate, and Investment Agent all returned to the founding document as the authority their requirements derive from. The founding document is genuinely the apex of the chain. But all four noted that the founding document's principles — equal visual weight for HCL, No False Precision, irreversibility signals, asymmetry-closing — are stated as values without structural embodiment in the ADR process. Phase 0's primary function is to create that structural embodiment: a process that is traceable back to the founding document's reasoning, not just its conclusions.

---

## Part III — ROADMAP Output

### Section A: DIC Guardrail List

Five binding requirements per standing agent, suitable for encoding in the ADR template and in the UX traceability specification. These requirements are binding, not advisory. An ADR that cannot satisfy these requirements must document why and requires Engineering Lead exception.

---

**Development Economist Guardrails (DE-1 through DE-5)**

| # | Requirement | Scope | Exception path |
|---|---|---|---|
| DE-1 | ADRs touching Zone 1, trajectory display, or instrument weighting must certify human cost ledger retains equal visual weight to financial indicators | All ADRs with user-facing display implications | EL exception required; documented rationale mandatory |
| DE-2 | Persona trace must name the income cohort served (from: bottom two quintiles; pensioners 65+; youth 18-35 tradable; children 0-5) | ADRs tracing to Personas 2, 3, or 5 | If cohort is not addressable by capability, document explicitly as known limitation |
| DE-3 | ADRs adding composite indicators must specify per-cohort breakdown accessibility path and maximum interaction count in Reactive state | ADRs introducing composite or aggregate indicators | If breakdown is deferred, document as roadmap item with milestone assignment |
| DE-4 | Persona trace must specify entry state; acceptance criterion must name time/interaction ceiling for that entry state | All ADRs with persona traces | No exception path — entry state specificity is a minimum quality bar |
| DE-5 | ADRs introducing aggregate indicators must document disaggregation pathway or explicitly acknowledge its absence as a known limitation | All ADRs introducing aggregate measurement capabilities | Absence acknowledgment is acceptable; silence is not |

---

**Chief Methodologist Guardrails (CM-1 through CM-5)**

| # | Requirement | Scope | Exception path |
|---|---|---|---|
| CM-1 | ADRs introducing new output formats must include an "uncertainty display specification" section naming confidence tier display, location, and Tier 3/4 behavior | All ADRs with new display surfaces | No exception — this is a minimum quality bar; "per the standard" references are not specifications |
| CM-2 | Persona trace for Personas 4, 5, and any persona in Demonstrative entry state must specify how pre-calibration disclosure appears in that context | ADRs tracing to Personas 4, 5, or Demonstrative entry state | No exception — the 5-minute window is a constraint on the format, not a waiver of the disclosure |
| CM-3 | Persona trace must specify tool behavior when confidence is Tier 3 or lower — what the alert reads and what the user is told | All ADRs tracing to any persona in Reactive entry state | No exception — the failure path is as important as the success path |
| CM-4 | Confidence tier display is a named, falsifiable acceptance criterion at indicator level for any ADR introducing a new indicator | All ADRs introducing new indicators | No exception — "per the standard" is not an acceptance criterion |
| CM-5 | ADRs introducing measurement capabilities must specify the Structural Absence Declaration conditions: what triggers it, what the user sees, what action is available | All ADRs introducing measurement capabilities | No exception — a capability with no meaninglessness behavior will generate false precision at implementation |

---

**Intergenerational Advocate Guardrails (IA-1 through IA-5)**

| # | Requirement | Scope | Exception path |
|---|---|---|---|
| IA-1 | ADRs modifying MDA alert panel must include acceptance criterion: TERMINAL alert visually distinct from WARNING at minimum supported viewport with no implementation discretion | All ADRs touching alert panel display | EL exception required with written justification; QA test must verify criterion pre-merge |
| IA-2 | MDA thresholds introduced or modified by ADR must document the irreversibility justification: what becomes irreversible past threshold, over what horizon, based on what evidence | ADRs defining or modifying MDA floors | No exception — a threshold without an irreversibility justification is not an MDA floor, it is an arbitrary line |
| IA-3 | ADRs producing human development outputs must specify whether the output horizon captures compounding effects; if not, document this as a known limitation | All ADRs for human development capabilities | Known limitation acknowledgment is acceptable; silence is not |
| IA-4 | ADRs modifying alert panel scroll behavior or visible count must include acceptance criterion: TERMINAL and CRITICAL alerts visible without scroll at minimum supported viewport | ADRs touching alert count or scroll behavior | EL exception required with scenario-specific CI test coverage |
| IA-5 | Infrastructure ADRs affecting computation timing or event propagation must include "signal latency impact" statement covering TERMINAL alert update latency | ADRs for computation engine, propagation, or event processing | Not applicable statements are acceptable; silence is not |

---

**Investment Agent Guardrails (INV-1 through INV-5)**

| # | Requirement | Scope | Exception path |
|---|---|---|---|
| INV-1 | ADRs for analytical capabilities must include a one-paragraph "asymmetry assessment": what well-resourced actors can do, what this ADR closes, what gap remains | All ADRs introducing new analytical capabilities | If no comparable capability exists in sophisticated actor tooling, document why; this is an acceptable finding |
| INV-2 | ADRs for External Sector capabilities must name the investment signal enabled for the sovereign and the corresponding signal available to the creditor side | ADRs for External Sector, reserve management, or trade capabilities | No exception — a capability that cannot name the asymmetry it addresses has not established its mission relevance |
| INV-3 | ADRs must specify minimum data tier at which capability produces actionable output; if Tier > 2, document synthetic data inference pathway or acknowledge as accessibility gap | All ADRs introducing analytical capabilities | No exception — accessibility gap acknowledgment is mandatory; silence implies Tier 1 assumption |
| INV-4 | Persona trace to Persona 2 must include a "negotiating leverage statement": the specific argument the persona can make after accessing this capability that she could not make before | All ADRs tracing to Persona 2 (Ministry Negotiator) | No exception — if no negotiating argument is produced, the trace is incomplete |
| INV-5 | ADR panel must include a one-paragraph "mission impact statement": which capability gap this ADR closes ranked by asymmetry-closing impact | All ADRs requiring panel review | No exception — technical completeness and mission impact are not synonymous |

---

### Section B: Capability Gap Priority List

Combined priority list from Development Economist and Investment Agent perspectives. Ordered by combined mission impact.

| Priority | Gap | Description | Asymmetry Severity | Roadmap Horizon | Related Issues |
|---|---|---|---|---|---|
| 1 | Cohort-level human cost attribution chain | Which specific conditionality term drives which threshold crossing, named per income cohort | CRITICAL (DE-G3 + INV-G3) | IMMEDIATE | Closes DEMO4-001 class failure; enables Case 2 marquee |
| 2 | Multiplier sensitivity map (cohort-level) | Human cost trajectory at multiplier 0.5/1.0/1.5/2.0 by income cohort; which cohort crosses CRITICAL first at each multiplier | CRITICAL (DE-G2 + INV-G1) | IMMEDIATE | Case 1 marquee case; #746 foundation |
| 3 | Reserve drawdown arc under external shocks | Real-time reserve_coverage_months depletion as trade/commodity shocks propagate | CRITICAL (INV-G2) | IMMEDIATE | Completes DEMO4-001 fix; ExternalSectorModule wiring |
| 4 | Cohort disaggregation as Zone 1 first-class output | Bottom quintile, youth, pensioners as named indicators visible without navigation in all modes | HIGH (DE-G1) | IMMEDIATE | #747; M11.5 GAP-04 |
| 5 | Historical precedent pattern matching | "This trajectory resembles [historical case] at step [N]" as accessible Mode 1 function | HIGH (INV-G4) | NEAR-TERM | Case 3 marquee; Persona 3 primary need |
| 6 | Multi-scenario PMM comparison view | Side-by-side PMM trajectory: proposed programme vs. counter-proposal | HIGH (INV-G5) | NEAR-TERM | Mode 3 core negotiating function |
| 7 | Early childhood development indicators | Child malnutrition, under-5 mortality, school enrollment as named first-class indicators | HIGH (IAG-2) | NEAR-TERM | Closes longest-tail intergenerational gap |
| 8 | Generational horizon view | Projection 10-15 years past programme window with explicit uncertainty disclosure | MEDIUM (IAG-1) | LONG-TERM | Architecture required before implementation |

---

### Section C: Cross-Cutting Architectural Requirements for ADR Traceability

These requirements apply to all ADR types and are derived from the convergences identified in Part II. They do not belong to any single DIC agent's domain — they are Council-level findings.

**C-1: Silent failure mode specification is mandatory.**  
Every ADR must specify what the capability produces when it appears to be functioning but the underlying data source, propagation channel, or computation is absent or broken. This is the DEMO4-001 class of failure: a module that emits events but whose downstream consumer is disconnected. A capability whose silent failure mode is "appears correct but produces no change in output" is more dangerous than a capability that fails noisily. The ADR must name the silent failure mode and the detection mechanism.

**C-2: Acceptance criteria must be verifiable in the live application, not just in CI.**  
"PR merged and CI green" does not constitute a satisfied acceptance criterion for any capability whose value is measured in the user's ability to see and act on information. ADR acceptance criteria must specify the observable application state that confirms the capability is serving its stated purpose: "User can navigate from [starting state] to [specific output] in [time limit] under [entry state] conditions." This criterion cannot be satisfied by running tests against mocked data.

**C-3: The founding document's north star test must be answerable for every ADR.**  
"Does this decision make the tool more useful to a finance minister sitting across from an IMF negotiating team, in that moment?" An ADR that cannot answer this question affirmatively — with specificity about which minister, in which moment, with what capability she gains — has not established its mission relevance. The ADR template must include this test as a mandatory section. An ADR panel that cannot produce a concrete answer to this question is not ready to accept the ADR.

---

## Part IV — Step 1 Deliverables Summary

The following deliverables are confirmed complete as required by the sprint plan.

| Deliverable | Status | Location |
|---|---|---|
| DIC guardrail list — Development Economist (5 requirements) | ✅ COMPLETE | Section A, DE-1 through DE-5 |
| DIC guardrail list — Chief Methodologist (5 requirements) | ✅ COMPLETE | Section A, CM-1 through CM-5 |
| DIC guardrail list — Intergenerational Advocate (5 requirements) | ✅ COMPLETE | Section A, IA-1 through IA-5 |
| DIC guardrail list — Investment Agent (5 requirements) | ✅ COMPLETE | Section A, INV-1 through INV-5 |
| Capability gap priority list (Investment Agent + Development Economist) | ✅ COMPLETE | Section B |
| Cross-cutting architectural requirements | ✅ COMPLETE | Section C |
| Tensions between agent perspectives (surfaced, not resolved) | ✅ COMPLETE | Part II |
| Convergences across all four agents | ✅ COMPLETE | Part II |

**This document is the prerequisite for Step 2 (UX Designer) and Step 3 (Business PO).** Per the sprint plan, Step 2 may not begin until this document is filed at its canonical location.

---

## Handoff Notes for Step 2 — UX Designer

The UX Designer is required to ground UX traceability requirements in these guardrails. The specific points of engagement:

1. **Tension 1** (cognitive load vs. methodological completeness) must be resolved by the UX Designer, not deferred. The Chief Methodologist's CM-2 requirement (uncertainty disclosure in Persona 5's 5-minute window) requires a UX decision about how confidence tiers appear in the Demonstrative entry state without adding friction.

2. **DE-1** (HCL equal visual weight) is a guardrail that supersedes information hierarchy decisions. If an information hierarchy ruling would demote HCL from Zone 1, the Development Economist's guardrail governs — this requires an Engineering Lead exception with documented rationale, not a UX ruling.

3. **IA-4** (TERMINAL and CRITICAL visible without scroll at minimum viewport) is a hard constraint that the UX Designer must specify as an invariant when deriving the UX traceability requirements for alert panel ADRs.

4. The Council **does not resolve the XD-1 tension** (finance minister vs. specialist as primary persona) — that is Step 3's responsibility (Business PO, Output 2). The UX traceability requirements in Step 2 should hold this tension open rather than resolving it, noting where the two personas have different implications for UX requirements.

## Handoff Notes for Step 3 — Business PO

The Business PO's output (persona traceability requirements + persona conflict resolution ruling) must engage directly with:

1. **INV-4** (negotiating leverage statement in persona traces to Persona 2) — this is a concrete operational requirement that the Business PO's persona traceability specification should encode.

2. **DE-2** (income cohort naming in persona traces) — the Business PO's specification should define what a "valid cohort trace" looks like.

3. The **XD-1 gap** (founding document north star is Persona 5; UX north star canonical user is Persona 2) is the primary conflict resolution question for Step 3. The gap analysis in the deliberation document provides the most complete framing; this document provides the DIC perspective on why both personas matter and which use cases each serves.

---

*Document complete. Filed as Step 1 output for Phase 0 — UX/Persona Traceability Upstream of ADR Development.*  
*Council Orchestrator session record — 2026-06-08.*
