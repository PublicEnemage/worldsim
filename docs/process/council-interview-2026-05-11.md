# Domain Intelligence Council Interview — 2026-05-11

## Interview Conditions

**Date:** 2026-05-11
**Milestone context:** M8 entry gate — Ecological and Governance Frameworks
**Gate condition:** Must be completed before ARCH-REVIEW-005 (causal meta-map, Issue #218) is authored; council feedback is an input to architectural decisions, not post-hoc validation.
**Process:** Nine council members interviewed in independent parallel instances. Each received: CLAUDE.md North Star, POLICY.md commitments summary, five-case backtesting table (v0.6.0), and four-framework measurement description. No ADRs, no implementation decisions, no architectural documents shared. Three questions per member plus an unprompted finding.
**Interviewer:** PM Agent executing Issue #235 protocol per docs/process/council-interview-prompt.md.

---

## Individual Responses

### Development Economist

**Validity:** The four-framework structure is directionally correct but missing the transmission mechanism layer — knowing that a fiscal consolidation causes human development deterioration is a thermometer reading; what a minister needs is the pathway (which specific conditionality terms create which specific capability deprivations through which institutional channels).

**Credibility:** DIRECTION_ONLY validation fails in the negotiating room because the IMF challenges magnitude, distributional incidence, and duration — the Greek fiscal multiplier mea culpa is the canonical reference the counterparty will invoke immediately.

**Priority:** Conditionality decomposition engine — attribute projected human development costs to individual program terms so the minister can contest specific conditions, not aggregate trajectories.

**Unprompted finding:** Asymmetric speed of capability destruction vs. restoration — economic indicators recover in 3–5 years; human capital destroyed (school dropout, cognitive effects of malnutrition, health worker emigration) does not recover on the same timescale or at all. The model will systematically underestimate human costs of any policy that causes a significant trough.

---

### Political Economist

**Validity:** The governance module measures outcome indicators (institutional quality, rule of law) rather than mechanism indicators — it is missing any model of the political economy of reform itself: who controls decision levers, what their material interests are, which policies are politically survivable, and how conditionality interacts with domestic political coalitions.

**Credibility:** DIRECTION_ONLY cannot contest DSA projections (the counterparty has their own fiscal model); more critically, the absence of a political feasibility constraint means the simulation models an imaginary polity with no internal politics.

**Priority:** Political feasibility corridor as a hard constraint on scenario generation — evaluating a conditionality package against parliamentary arithmetic, coalition cohesion, and historical implementation rates before running it forward; returning the maximum politically sustainable package subset that meets 80% of fiscal targets.

**Unprompted finding:** Conditionality packages that front-load costs and back-load benefits systematically destroy the implementing coalition before benefits arrive — this is a temporal sequencing problem, not a governance quality failure, and it recurs regardless of institutional quality.

---

### Ecological Economist

**Validity:** Missing ecological threshold dynamics — planetary boundary proximity treated as continuous and symmetric when it is not; a fishery at 110% of MSY is undergoing recruitment collapse that takes a decade to manifest and two decades to reverse, not a linear warning signal.

**Credibility:** Without calibrated ecological-to-financial transmission channels within the program horizon, the ecological axis is decorative in a negotiation context — a sophisticated counterparty will note the finding and move on.

**Priority:** Calibrated ecological-to-financial transmission for two high-frequency, high-materiality pathways: (1) natural resource export revenue as a function of stock health; (2) climate-driven agricultural productivity shocks as a function of rainfall anomaly and soil capital. These are the cases where ecological deterioration appears inside a 3–5 year program window.

**Unprompted finding:** The ecological framework is almost certainly implemented as a reporting layer rather than as a first-class participant in the event propagation graph — ecological state variables are event consumers, not event sources. The most dangerous ecological-financial interactions are invisible in the model by construction if this is true. The fix is architectural: ecological state changes must generate events that propagate through financial and governance modules.

---

### Geopolitical Analyst

**Validity:** Missing geopolitical classification of the debtor — a country with strategic value to a major creditor power (base access, pipeline routes, rare earth deposits, voting bloc membership) faces a structurally different negotiating environment; the creditor's political utility function for the debtor is a primary variable that the tool currently treats as a black box.

**Credibility:** DIRECTION_ONLY cannot construct the sentence "our analysis gives a 90th-percentile GDP contraction of X%" — without magnitude calibration and quantified uncertainty intervals, the tool cannot make independent claims against the fund's own DSA projections.

**Priority:** Creditor leverage decomposition — a structured breakdown of what leverage the counterparty actually holds versus what they are asserting, mapped against historical analogues where similar leverage claims were made and how often they held.

**Unprompted finding:** Negotiations are triangular (debtor, external creditor, domestic political coalition) not bilateral — the political economy constraint is not a secondary analytical layer, it is a binding constraint on which financial pathways are actually traversable, and it belongs in the core propagation graph.

---

### Intergenerational Advocate

**Validity:** Missing reversibility classification — damage across the four frameworks is treated as equally reversible, which it is not; the analysis needs to distinguish between damage that heals when GDP recovers and damage that forecloses options for the next two generations regardless of subsequent recovery.

**Credibility:** The discount rate problem is unanswered — a counterparty will immediately ask "what is your discount rate and how did you choose it?"; the tool needs to document its intergenerational discounting position and offer comparative outputs at the IMF's own discount rate assumptions alongside a low-discount alternative.

**Priority:** 25-year human capital depletion trajectory module — explicitly projecting past the program window so the minister can show the IMF team what the program looks like at year 3 and what it has caused by year 25; the Greece and Ecuador backtesting cases contain this historical evidence for validation.

**Unprompted finding:** The most structurally significant intergenerational harm in sovereign debt crises is technocratic class emigration — the destruction of the institutional analytical capacity needed to run the recovery and to use tools like WorldSim in the future; this creates a compounding vulnerability across decades and should be tracked as a first-class feedback loop.

---

### Community Resilience

**Validity:** The informal economy is entirely absent — in vulnerable countries it constitutes 40–60% of economic activity, absorbs displaced formal-sector workers, and provides the shock absorption that prevents household catastrophe from becoming mortality; the model is measuring the hospital's budget while ignoring the grandmother network actually keeping children fed.

**Credibility:** No social cohesion dynamics as mediating variable between policy shock and human development outcome — the IMF's own Greek multiplier mea culpa acknowledged this transmission was faster and more severe than models predicted; a model without this chain cannot defend its human development trajectory outputs.

**Priority:** Social Coping Capacity index — a composite tracking the remaining absorptive capacity of community-level informal systems and estimating the threshold at which that capacity fails; draws on remittance network stress, informal credit market conditions, diaspora transfer patterns, and household-level food security rather than aggregate caloric supply.

**Unprompted finding:** Community resilience is a depletable stock not a fixed parameter — Argentina's barter clubs and Greece's mutual aid networks formed rapidly but were gone within 4 years not because the crisis ended but because the social capital to run them was exhausted; the model systematically understates cumulative harm if it treats community absorptive capacity as constant throughout an extended program.

---

### Investment Agent (RISK-AVERSE)

**Validity:** Missing a disaggregated private capital stack — portfolio flows, trade finance counterparty limits, FDI, and DFI portfolios exit at different speeds with different second-order consequences (import financing collapses before fiscal financing), and conflating them misses the liquidity cliff that precedes the solvency crisis.

**Credibility:** DIRECTION_ONLY provides no additional information over a simple recession indicator; a counterparty will immediately ask for the model's mechanism for capital flight and whether it reproduces reserve drawdown pace and magnitude in the Thailand 1997 case, not merely direction.

**Priority:** Creditor composition and rollover risk module — maps the debt maturity profile against creditor type (bilateral official, multilateral, commercial bond, domestic banking, short-term trade finance) and simulates rollover failure sequences; this is structurally equivalent to what the IMF's own DSA does, making it the gap that most undermines the tool's status as independent analysis.

**Unprompted finding:** Private capital responds to what other private capital actors are expected to do — coordination dynamics, not individual fundamental assessments (Morris-Shin global games framework); a capital flight model calibrated only on fiscal ratios and reserve levels will miss the intervention windows that exist before creditor coordination tips, making avoidable crises look inevitable.

---

### Social Dynamics

**Validity:** Social dynamics are a propagation mechanism, not a measurement framework sitting alongside the others — the specific gap is threshold-dependent collective behavior and the legitimacy threshold model: the point at which population response shifts from private coping to collective action that collapses the implementing coalition.

**Credibility:** The IMF knows programs fail on social dynamics; a tool without a social stability model is less sophisticated than the fund's own internal program review process, which routinely evaluates political economy risks — the tool's credibility depends on modeling failure modes, not just trajectories.

**Priority:** Legitimacy erosion and programme abandonment probability model — takes the human development trajectory under a conditionality scenario and outputs a time-varying distribution of political survival probability; inputs are knowable (unemployment trajectory, real wage trajectory, distributional incidence, electoral proximity, coalition fragility).

**Unprompted finding:** Asymmetric social time horizons — populations in the bottom income quintile operate on weeks (will wages cover food this month?), not fiscal year cycles; the human cost ledger needs temporal resolution by cohort at month-level, not year-level, because the conditionality terms that are actual breaking points are those that cause immediate proximate harm to people with no buffer, not long-run macroeconomic deterioration.

---

### Chief Methodologist

**Validity:** DIRECTION_ONLY backtesting is a plausibility check, not validation — all five cases are well-documented disasters where GDP contraction was certain; the model could be off by a factor of three on fiscal multipliers, systematically understate contraction duration, and misrepresent distributional incidence and still pass every test listed.

**Credibility:** The weakest point is the absence of a structural model identification strategy — the IMF's counterparty will ask for the source of the fiscal multiplier estimate, its confidence interval, and how it varies with the output gap and monetary conditions; parameterization sources are undocumented; there is also scenario selection bias (only tail-event cases in the calibration set, no demonstrated validity for moderate-stress adjustment scenarios).

**Priority:** Conditional confidence interval system — uncertainty bands that narrow or widen based on the analog-case distance between the current scenario and historical calibration cases; the tool should explicitly flag when it is extrapolating beyond calibration range and when it has strong analog support, so the user knows when to trust the output.

**Unprompted finding:** Goodhart's Law / model monoculture risk — once WorldSim achieves institutional adoption, IMF counterparty teams will learn the parameterization and optimize conditionality proposals against the model's known blind spots rather than against underlying economic reality; methodological diversity and transparent uncertainty about the model's own parameterization are not optional features, they are the primary defense against the tool becoming a sophisticated manipulation surface.

---

## Cross-Cutting Themes

### Theme 1 — DIRECTION_ONLY is insufficient; magnitude calibration is the credibility floor
**Raised by:** Development Economist (Q2), Geopolitical Analyst (Q2), Investment Agent (Q2), Chief Methodologist (Q1 and Q2), Social Dynamics (implicit — tool must model failure modes not just trajectories)
**Count:** 5 of 9 members independently

The strongest cross-cutting signal in the entire interview set. All five articulate the same core argument from different domain perspectives: getting the sign right on GDP during well-documented disasters provides no independent analytical value to a finance ministry sitting across from a counterparty that already has quantitative magnitude projections. The tool's negotiating utility is zero below the magnitude calibration threshold. This finding validates the ADR-006 Monte Carlo upgrade trigger as a first-order priority, not a deferred nicety.

### Theme 2 — Political feasibility / social stability as binding constraint on policy paths, not output indicator
**Raised by:** Political Economist (Q1, Q3), Geopolitical Analyst (Q1 unprompted), Social Dynamics (Q1, Q3), Community Resilience (Q2)
**Count:** 4 of 9 members independently

Four members from distinct domain perspectives converge on the same architectural point: the political economy constraint belongs in the core propagation graph as a binding constraint on which financial pathways are actually traversable, not as a measurement axis on the radar chart. A simulation that produces financially sustainable pathways that are politically unsustainable is simulating an imaginary polity. This validates M11 Political Economy and Conditionality as a load-bearing milestone — but also raises the question of whether the governance module in M8 should be architected to participate in event propagation rather than only produce output events.

### Theme 3 — Important dynamics are observers of output, not participants in the propagation graph
**Raised by:** Ecological Economist (ecological state as event consumer not source), Social Dynamics (social dynamics as propagation mechanism not measurement layer), Community Resilience (informal economy absent from model), Investment Agent (capital stack disaggregation as sequenced propagation)
**Count:** 4 of 9 members independently

Four members identify the same architectural failure mode from different domains: the simulation is treating important causal mechanisms as reporting layers rather than as active participants in the event propagation graph. Ecological threshold crossings should generate financial events. Legitimacy thresholds should constrain which policy paths are available. Community resilience depletion should feed back into human development trajectories. Private capital coordination should propagate as a distinct event stream. This is an ARCH-REVIEW-005 finding: the causal meta-map (Issue #218) must explicitly answer which dynamics are event sources vs. event consumers, and the current architecture may be systematically misclassifying them.

### Theme 4 — Asymmetric temporality: destruction and depletion are faster and less reversible than recovery
**Raised by:** Development Economist (asymmetric destruction/restoration speed), Intergenerational Advocate (reversibility classification), Community Resilience (resilience as depletable stock), Social Dynamics (asymmetric time horizons by cohort)
**Count:** 4 of 9 members independently

Every member who addressed the temporal dimension raised the same asymmetry: things that matter — human capital, community resilience, social trust, institutional capacity — deplete quickly under crisis conditions and recover slowly or never. The simulation's treatment of these as variables that move symmetrically in both directions with economic conditions will systematically underestimate the human cost of any policy that causes a trough. This has design implications for how human development outputs are presented (distinction between recoverable and irreversible damage) and for the human cost ledger's temporal resolution (month-level vs. year-level for vulnerable cohorts).

### Theme 5 — Transmission mechanisms between frameworks are absent or uncalibrated
**Raised by:** Development Economist (policy-to-human-harm pathway), Ecological Economist (ecological-to-financial channel), Investment Agent (capital stack sequencing), Social Dynamics (legitimacy threshold to programme abandonment)
**Count:** 4 of 9 members independently

The four frameworks are measured but their interactions are not modeled with calibrated transmission mechanisms. An ecological deterioration that affects export revenue within the program horizon is invisible in the current architecture. A legitimacy threshold crossing that triggers programme abandonment is invisible. A capital coordination dynamic that accelerates the liquidity cliff before the fiscal crisis registers is invisible. This is the deeper architectural version of Theme 3.

---

## Contradictions Requiring Design Decisions

### Contradiction 1 — Primary negotiating leverage gap: geopolitical vs. political economy
**Geopolitical Analyst** names the debtor's geopolitical classification (strategic value to creditor powers) as the primary missing variable. **Political Economist** names the domestic political coalition constraint as the primary missing variable. Both are real gaps. They have different design implications and different development priorities. The Geopolitical Analyst's gap is analytical (requires data on geopolitical relationships); the Political Economist's gap is architectural (requires a constraint module in the propagation graph). These are not mutually exclusive but they compete for M11 scope.

**Design decision required:** Which of these two capabilities is the higher-priority M11 scope item? The Political Economist's constraint module has broader applicability across cases; the Geopolitical Analyst's classification system is more specific to the negotiation context but harder to parameterize without opinionated geopolitical data.

### Contradiction 2 — Uncertainty communication: wider bands vs. actionable specificity
**Chief Methodologist** advocates for conditional confidence interval widening when the model is extrapolating beyond calibration range — more honest uncertainty representation, even if it reduces apparent precision. Other members (Development Economist Q3, Investment Agent Q3) want specific new capabilities that produce new point outputs (conditionality decomposition, rollover risk module). These are in tension: adding new analytical outputs without validating their magnitude calibration could compound the core credibility problem the Chief Methodologist identifies.

**Design decision required:** Should new capability additions in M9–M12 require magnitude calibration validation before shipping, or should they ship with explicit confidence flags that communicate calibration status? The latter is more consistent with the "No False Precision" principle.

---

## Priority Ranking — Capability Additions

| Rank | Capability | Raised by | M8 fit | Target milestone |
|---|---|---|---|---|
| 1 | Magnitude calibration and quantified uncertainty (ADR-006 Monte Carlo upgrade) | Dev Economist, Geopolitical Analyst, Investment Agent, Chief Methodologist, Social Dynamics | NEXT MILESTONE — gated on Issue #221 | M10 |
| 2 | Political feasibility corridor as propagation constraint | Political Economist, Geopolitical Analyst, Social Dynamics | NEXT MILESTONE | M11 (committed) |
| 3 | Conditionality decomposition engine — attribute human costs to individual terms | Development Economist, Political Economist (close variant) | NEXT MILESTONE | M11 |
| 4 | Ecological state variables as event sources in propagation graph | Ecological Economist | THIS MILESTONE — architectural decision for Issue #218 | M8 gate input |
| 5 | Asymmetric reversibility classification for outputs | Intergenerational Advocate, Development Economist, Community Resilience | NEXT MILESTONE | M10 |
| 6 | Calibrated ecological-to-financial transmission channels | Ecological Economist | NEXT MILESTONE | M10 |
| 7 | Programme abandonment probability model | Social Dynamics, Community Resilience (close variant) | NEXT MILESTONE | M11 |
| 8 | 25-year human capital depletion trajectory | Intergenerational Advocate | NEXT MILESTONE | M11 |
| 9 | Creditor composition and rollover risk module | Investment Agent | NEXT MILESTONE | M12 |
| 10 | Social Coping Capacity / informal economy tracking | Community Resilience | NEXT MILESTONE | M12 |
| 11 | Goodhart's Law / monoculture documentation | Chief Methodologist | THIS MILESTONE — M9 standards gap | M9 |
| 12 | Creditor leverage decomposition (real vs. asserted leverage) | Geopolitical Analyst | PARKING LOT — requires geopolitical data | M12 or later |
| 13 | Private capital coordination / global games model | Investment Agent unprompted | PARKING LOT — substantial complexity | M12 or later |

---

## Recommended M8 Scope Impact

### Add to M8 gate / ARCH-REVIEW-005 input (Issue #218)

**Ecological state as event source:** The Ecological Economist's architectural finding — that ecological state variables are almost certainly event consumers rather than event sources in the current propagation graph — must be addressed explicitly in ARCH-REVIEW-005 before M8 implementation is locked. The causal meta-map (Issue #218) must specify which ecological state changes generate propagation events into the financial and governance modules, not just how financial events affect ecological indicators. This is not a new feature request; it is a check on whether the ecological module is correctly wired.

### No new items added to M8 implementation scope

The nine council members identified no gaps in the M8 committed scope (Ecological Module complete, Governance Module complete, four radar axes live, Coffin Corner indicator, MDA extended). The gaps they identified are either (a) cross-milestone architectural concerns that feed into the causal meta-map (Issue #218), or (b) M10–M12 capability work already in the milestone sequence.

### Validate M11 scope

The council responses strongly validate the M11 Political Economy and Conditionality milestone as load-bearing. Political feasibility corridor (Political Economist Q3), programme abandonment probability (Social Dynamics Q3), conditionality decomposition (Development Economist Q3), and cost front-loading sequencing (Political Economist unprompted) are all M11 scope items and were independently identified by 4 of 9 council members as the highest-priority capability additions.

---

## Issues Filed

| Issue | Title | Milestone | Rationale |
|---|---|---|---|
| #270 (comment) | Input to ARCH-REVIEW-005: ecological state as event source | M8 gate | Ecological Economist finding; must be addressed before #218 is authored |
| New | Reversibility classification for simulation outputs — recoverable vs. irreversible damage | M10 | Raised by Intergenerational Advocate, Development Economist, Community Resilience |
| New | Conditionality decomposition engine — attribute scenario costs to individual program terms | M11 | Development Economist Q3; most direct negotiation-room capability |
| New | Programme abandonment probability model — legitimacy erosion as time-varying output | M11 | Social Dynamics Q3; Community Resilience Q3 (close variant) |
| New | 25-year human capital depletion trajectory module | M11 | Intergenerational Advocate Q3; validated by Greece/Ecuador historical record |
| New | Calibrated ecological-to-financial transmission: resource export revenue + agricultural productivity | M10 | Ecological Economist Q3; prerequisite for ecological axis credibility in negotiation |
| New | Goodhart's Law documentation requirement — blindspot registry includes model monoculture risk | M9 | Chief Methodologist unprompted; Standards Foundation milestone |
