# WorldSim: A Founding Document

*Synthesized from the project's founding conversations, April–May 2026*
*By Imran Yousuf, Engineering Lead*

---

## Preface

This document exists because important things do not survive compression.

The operational documentation of the WorldSim project — CLAUDE.md, the Architecture Decision Records, the GitHub issues, the agent personas — is accurate and useful. But it is a compressed representation of something richer: two months of sustained thinking about a problem that matters, conducted in the form of conversations that reached their physical limits before their intellectual ones did.

What follows is an attempt to reconstruct the full mental model — the why beneath the what, the reasoning beneath the decisions, the vision beneath the architecture. It is written for three readers: the future collaborator who wants to contribute with judgment rather than just follow instructions; the institutional decision-maker who needs to understand what this tool claims and what it honestly does not; and the future Engineering Lead who may one day take stewardship of this project and needs to understand not just what was built but why each choice was made.

It is also written as a founding record — because the conversations that produced these ideas are approaching their context limits, and the ideas themselves deserve a more durable home.

---

## Part One: The Problem

### The Room Where It Happens

Somewhere in Washington, DC, or Brussels, or Geneva, a small group of people is sitting in a room making decisions that will affect millions of people who will never know this room exists.

On one side of the table: a team from the International Monetary Fund or the World Bank or a syndicate of international creditors. They have PhD economists, proprietary models, decades of institutional knowledge, and the full analytical apparatus of the most sophisticated financial institutions in the world. They know, with some precision, what the proposed programme terms will likely produce. They have scenario models. They have historical pattern libraries. They have confidence intervals.

On the other side: a finance ministry team from a country that has run out of options. They may have two or three economists. They are working with spreadsheets and public data. They are operating under extreme time pressure. They are negotiating in a second or third language. They may not fully understand the mathematical implications of the terms being offered to them. And they are making a decision with generational consequences — for their country, for their population, and most acutely for the people at the bottom of the economic distribution who will absorb the human cost of whatever is decided in this room.

This asymmetry is not accidental. It is structural. It has been structural for decades. And it has costs — costs that are measured not in basis points or debt-to-GDP ratios but in life expectancy, child malnutrition rates, educational attainment, and the accumulated loss of human capability across an entire generation.

The quinoa farmer in Bolivia does not know this room exists. He will never sit in it. But decisions made in that room will shape the conditions of his life — whether he can afford seeds, whether his children attend school, whether his community has a functioning clinic. He has no analytical capability in that room. He has no voice. He has no model.

WorldSim exists because that asymmetry is not inevitable. It is a capability gap, and capability gaps can be closed.

### The Eureka Moment

The founding insight of this project was not about technology. It was about epistemics.

When the IMF designed the first Greek programme in 2010, it assumed a fiscal multiplier of approximately 0.5. That is: for every 1% of GDP in fiscal consolidation (spending cuts and tax increases), the model predicted output would decline by 0.5%. This was the standard assumption. It was what the models said.

The actual multiplier turned out to be closer to 1.5. For every 1% of fiscal tightening, output fell by 1.5%. The programme was three times more contractionary than the model predicted. The IMF itself acknowledged this error in 2013.

The human consequences were not three times worse than expected. They were different in kind. Unemployment reached 27%. Youth unemployment exceeded 60%. The healthcare system partially collapsed. Life expectancy began to decline. Child poverty spiked. A generation of Greeks found themselves in their late twenties and thirties with no viable economic future in their country. These were predictable consequences — not in the sense that anyone predicted them, but in the sense that the data to predict them existed. The variables were present, measurable, and consequential. They were simply not in the model.

The Eureka function — as this project has named it — is not about predicting the future. It is about recovering the structure of the past. About asking: what variables were present, measurable, and consequential in historical cases, but were not surfaced by the analytical tools of the time? And then building a tool that surfaces them going forward.

The gap between what the IMF's model predicted and what actually happened to Greek unemployment, Greek child poverty, Greek life expectancy — that gap is exactly the gap WorldSim is designed to close. Not by being smarter than the IMF, but by looking at more dimensions simultaneously, and by treating the human cost ledger as a primary output rather than a secondary consideration.

### The Asymmetry Is Not Just Informational

It would be easy to frame this as purely an information problem — the finance ministry doesn't have the right data, or the right models, or the right scenario analysis tools. Give them better tools and the asymmetry closes.

That framing is incomplete. The asymmetry is also institutional, political, and cognitive. The finance ministry team may be operating under political pressure from their own government. They may be facing a domestic political crisis. They may be sleep-deprived. They may be sitting across from people who have sat in this room dozens of times before, who know exactly where the negotiating leverage lies, who have seen this exact playbook deployed in a dozen countries.

This is why the aviation analogy is not decorative. A pilot facing spatial disorientation doesn't just need better maps. They need instruments that override the false signals their own senses are sending. They need a trusted, external, authoritative readout of reality that they can rely on when their intuitions are failing.

WorldSim is designed to be that instrument. Not a replacement for judgment — judgment is irreplaceable — but an external, transparent, methodologically honest readout of what the trajectory looks like across multiple dimensions simultaneously. Something the negotiator can point to and say: "According to this analysis, this programme path crosses the unemployment threshold at step three and does not recover within the six-year horizon. Show me the counter-analysis."

That is a different kind of conversation than the one that happened in the room in 2010.

---

## Part Two: The Analogy

### The Flight Simulator

The first extended analogy that shaped this project came not from economics but from aviation.

The Engineering Lead was learning to fly. He was struck by how aviation had solved the problem of high-stakes decision-making under uncertainty — not just technically, but institutionally. The flight simulator. The standardized instrument cluster. The checklist culture. The mandatory incident reporting. The obsessive focus on human factors and cognitive load. The Crew Resource Management training that explicitly addresses how authority gradients in a cockpit can cause crashes.

Aviation discovered, through catastrophic experience, that expert humans making decisions under stress and time pressure make systematic, predictable errors. And it built an entire discipline around compensating for those errors — not by making pilots smarter, but by designing the instruments, the procedures, and the training to surface the information that matters at the moment it matters.

The sovereign governance failures that WorldSim is designed to help prevent follow a remarkably similar typology. The project identified six failure modes from aviation that map directly to governance crises:

**The Spin** — self-sustaining deterioration where standard responses accelerate the problem. The analogy: a debt crisis where fiscal consolidation reduces output, reducing tax revenue, requiring more consolidation, reducing output further. Recovery requires counter-intuitive intervention: before attempting standard recovery maneuvers, the spin must first be broken.

**Coffin Corner** — the operating envelope narrows through individually rational decisions until no policy response avoids a binding constraint. The aircraft: at high altitude with low airspeed, increasing power causes a stall while decreasing power causes the same stall. The country: with high debt and low reserves, fiscal expansion triggers capital flight while fiscal contraction triggers recession. The Policy Maneuver Margin indicator — one of WorldSim's primary diagnostics — is the cockpit equivalent of the altitude-airspeed envelope display.

**Hypoxia** — the decision instrument itself is compromised without awareness of impairment. Pilots lose consciousness gradually in a depressurized cabin; the first symptom of oxygen deprivation is often euphoria and a sense that everything is fine. The governance equivalent: institutional capture, press freedom erosion, technocratic insularity. The decision-makers feel in control and competent. Their instruments are lying to them. The Institutional Cognitive Integrity Index is WorldSim's oxygen mask warning light.

**Backside of the Power Curve** — regime-dependent relationships where the sign of the effect inverts beyond a threshold. More thrust, counterintuitively, makes things worse. In governance: currency defense beyond a threshold depletes reserves and accelerates the attack; security crackdowns beyond a threshold generate the instability they are designed to suppress.

**Get-There-Itis** — commitment escalation overriding situational assessment. A pilot who has told their family they will be home for dinner continues a flight into worsening weather rather than diverting. A government that has publicly committed to programme targets continues a failed consolidation path rather than renegotiating. The clean-slate question — if we were encountering these conditions today with no prior commitment, would we choose this path? — is explicitly surfaced in WorldSim's interface.

**The CB Cloud** — asymmetric visibility. The pilot sees the cumulonimbus from the trailing edge, where it looks manageable. The aircraft in the cloud sees it from the leading edge, where it is lethal. Decision-makers see policy from the trailing edge: the intent, the rationale, the expected tradeoff. The affected population sees it from the leading edge: the consequences, the human cost, the irreversible damage. The human cost ledger is WorldSim's weather radar — it shows what is ahead, not what it looks like from behind.

These six failure modes are not metaphors. They are structural patterns that the simulation is explicitly designed to detect, measure, and surface. The instrument cluster is not designed to display economic indicators. It is designed to display the signals that matter when these failure modes are developing.

### Where the Analogy Breaks

No analogy survives complete contact with reality, and intellectual honesty requires naming where this one breaks.

A flight simulator is real-time. WorldSim is step-based. A pilot's instruments respond continuously to control inputs; WorldSim's instruments respond at discrete steps. The cockpit principle — that control inputs and instrument readouts are spatially co-located and temporally immediate — does not translate directly to a tool where "immediate" means "after the step resolves."

A flight simulator has one aircraft with one pilot. WorldSim may have multiple entities — multiple countries, multiple actors, multiple levels of resolution — being analyzed simultaneously. The cockpit metaphor assumes a single-aircraft perspective; the instrument cluster for a multi-entity scenario requires a different design logic.

A pilot's instruments are authoritative. An altimeter reading of 3,000 feet is 3,000 feet. WorldSim's instruments have confidence tiers, uncertainty bands, and honest-null states. A Tier 3 GDP projection with a band of ±2.4% is not an altimeter. The epistemic complexity of WorldSim's outputs — the distinction between what is known, what is inferred, what is synthetic, and what is genuinely unknown — does not have a clean analogy in a flight simulator, where the instruments are either working or they are not.

These breaks in the analogy are not reasons to abandon it. They are design constraints. They tell us where the cockpit metaphor needs qualification — where "always visible" means "visible for Tier 1 and Tier 2 outputs" rather than all outputs equally, where "immediate feedback" means "within one step resolution" rather than continuous, where "single pilot perspective" means "switchable between entities" rather than locked to one view.

### The Three Modes

A flight simulator is used in three distinct ways, and WorldSim is being designed to support all three.

**Mode 1 — Replay.** The simulator runs a historical scenario. The pilot — or analyst — observes what happened, step by step. The instruments show historical outputs. This is backtesting. The Greece 2010-2015 scenario. The analyst is reviewing a completed flight path, understanding where the instruments would have shown the danger signals, and calibrating their judgment against known outcomes. This is how the model gets better. This is the Eureka function in practice.

**Mode 2 — Simulation.** The simulator runs a forward projection from configured initial conditions and scheduled inputs. The analyst builds scenarios with alternative paths. What if the consolidation was phased differently? What if the primary surplus target was 1.5% instead of 3.5%? This is scenario modelling — the construction of possible futures for deliberate comparison. The analyst is a planner, not an observer.

**Mode 3 — Active Control.** This is the mode that does not yet exist in WorldSim but is the north star of its architecture. The simulator is live. The analyst has a control plane — a set of policy instruments available in real time. They apply a control input at a specific step and watch the trajectory change. They introduce an exogenous shock — a snap election, a creditor defection, a currency crisis — and watch how the instruments respond. They are not observing or planning. They are steering. This is the IMF negotiator at the table, testing in real time whether a counterproposal would cross the human cost threshold before committing to it.

The entire UX architecture of WorldSim is being designed around Mode 3, even though Mode 3 does not yet exist. This is the governing constraint: every design decision must be compatible with a future state where a user is making real-time control inputs and watching instruments respond. Designs that are adequate for Mode 1 but incompatible with Mode 3 will require fundamental restructuring when Mode 3 is introduced. The founding architecture principle — adopted formally as a governing UX premise — is that the control plane layout zone must be reserved before the control plane is built.

---

## Part Three: The Principles

### Multi-Currency Measurement

The most consequential architectural decision in WorldSim's design is one that sounds almost trivial until you think carefully about it: **there is no master conversion rate between the measurement frameworks.**

Economic analysis almost always ends in a single unit — GDP, debt-to-GDP ratio, fiscal balance. Everything gets translated into money. This is convenient and it is sometimes necessary. But it is also a choice, and it is a choice that carries profound implications.

When you translate child malnutrition into a GDP impact, you are making a claim about what child malnutrition is worth in monetary terms. That claim involves assumptions — about future earnings capacity, about discount rates, about whose valuation of childhood health outcomes is used as the denominator. Those assumptions are never neutral. In the context of a sovereign debt negotiation, they are almost always made by the people with the most analytical power and the greatest incentive to value human outcomes at the rate that supports their preferred programme design.

WorldSim produces outputs simultaneously in four accounting units: financial metrics (standard economic measures), human development units (the Sen capability approach and HDI dimensions), ecological units (planetary boundary proximity and natural capital depletion), and governance units (institutional quality, political freedom, rule of law). These are not converted into a single score. They are displayed simultaneously, with equal visual weight.

The radar chart is the primary visualization of this principle: a four-dimensional deformation of a shape, where any dimension can deteriorate independently of the others. A country's financial indicators can be improving while its human development indicators continue to deteriorate. That is not a contradiction to be resolved by applying a weighting scheme. It is the central analytical finding — the finding that the negotiator on the finance ministry side of the table most needs to see and least likely to be shown by the counterparty's models.

This is what "financial recovery is not the same as recovery" means, stated in the concrete terms of the Greece 2010-2015 scenario. At step five (2014), GDP growth turned marginally positive for the first time since the programme began. By the IMF's primary headline metric, the programme was working. By the human development metric — unemployment at 26.5%, child poverty elevated, life expectancy declining — the recovery had not begun. WorldSim makes both visible simultaneously, on the same screen, in the same moment, with equal weight.

### No False Precision

The model is not a prediction engine. This is stated explicitly in the founding documents and it deserves careful unpacking, because it is easy to say and surprisingly difficult to build a tool that actually embodies it.

A prediction engine claims to know what will happen. It produces a point estimate with a confidence interval that is typically too narrow, because the modellers are incentivized to appear precise and the audience is incentivized to want precision. The political economy of forecasting systematically produces overconfidence.

WorldSim is designed to be a structured reasoning tool. It produces distributions over scenarios, conditional on stated assumptions. The uncertainty is not a limitation to be minimized — it is information. Knowing that the distribution of GDP outcomes at step five spans from -3% to +1.5% tells you something important about how much policy confidence is warranted. Knowing that the human development confidence interval is wider than the financial interval tells you something about the data quality differential.

This principle extends to the honest treatment of model blindspots. Every limitation the model knows about — every variable it is not capturing, every domain where its fidelity is known to be weak, every relationship it is representing with a linear approximation that the real world executes non-linearly — is documented and visible. The simulation's integrity depends on its honesty about its own limitations. An analytical tool that hides its blindspots is not trustworthy. It may be more comfortable to use, but it is not trustworthy.

The Minimum Descent Altitude system is an expression of this principle in a specific form. MDA alerts do not say "this outcome will happen." They say "this trajectory, if continued, crosses a threshold below which we know that standard policy frameworks no longer provide protection and that damage becomes irreversible or generational." That is a different kind of claim — more modest, more honest, and more useful.

### Defense, Not Offense

This tool builds situational awareness and defensive capability for vulnerable actors. It is not designed to help anyone identify exploitable vulnerabilities in adversaries, execute financial attacks, or amplify power asymmetries.

The asymmetry this tool is designed to correct runs one direction. The finance ministry of a small, vulnerable country sitting across from the IMF is the direction. The corrective capability runs the same direction. The tool is not neutral — it is deliberately oriented toward the less powerful party in these negotiations.

This is a values statement, not a technical constraint. The same analytical capability that helps a finance ministry understand what a conditionality package implies for its human development trajectory could, in principle, be used by a sophisticated actor to identify where a vulnerable country's constraints lie and how to exploit them. This is the dual-use problem that the project has addressed explicitly in its policy documents.

The founding answer is: the tool is open source, so the methodology is transparent to everyone. The claim to asymmetry-correction is based not on keeping the capability secret but on making it available. The finance ministry of Bolivia can run the same analysis as the IMF. The analytical playing field is leveled by availability, not by secrecy.

### Backtesting as Epistemic Discipline

Every model relationship must be validated against historical cases before being trusted for forward projection.

This principle sounds obvious. It is, in practice, violated constantly. Economic models are validated against the data that was available when they were built, with assumptions that made the math tractable, and then deployed in conditions that differ from the validation environment in ways that the modellers knew but did not fully account for. The Greek fiscal multiplier error is the canonical example. The assumption of 0.5 was not arbitrary — it was validated against historical data from periods that were not comparable to the conditions of a sovereign debt crisis in a currency union with no monetary policy flexibility.

WorldSim's backtesting approach is different in kind. The model is run against historical cases with the inputs that were actually available at the time — not the inputs we know now were consequential, but the inputs that were measurable then. The gap between the model's output and the historical outcome is the primary signal. It is not a failure to be hidden or minimized. It is the finding.

This is the Eureka function: recovering the structure of the past. When the model runs against Greece 2010-2012 and produces a GDP contraction that is too shallow and an unemployment peak that is too low, that is a finding. It says: the model is missing something. What is the variable that was present, measurable, and consequential in the historical case that is not in the model? That question drives model improvement. The gap between prediction and outcome is not a bug — it is the primary feature.

### Open Source as Strategy

The tool must be accessible to the actors who most need it. This is not an ideological commitment to open source as a value in itself. It is a strategic conclusion that follows from the mission.

A proprietary tool with a subscription fee that only well-resourced finance ministries can afford does not level the playing field. It creates a new tier of the same asymmetry. A tool that requires expensive compute infrastructure to run is not accessible to a ministry operating on a thin budget with modest hardware.

Open source also provides the methodological transparency that gives the tool credibility. Anyone can inspect the assumptions. Anyone can challenge the normalization methodology. Anyone can propose improvements. The epistemics of the tool — its claim to be honest about what it knows, what it infers, and what it does not know — are only credible if the methodology is inspectable. Credibility through transparency is different from credibility through authority, and it is the only kind of credibility that is appropriate for a tool designed to challenge authority.

The equitable build process principle extends this logic into the development process itself. WorldSim's build, test, and development infrastructure must be accessible to contributors who do not have access to high-end hardware or expensive CI resources. A tool designed to level the playing field for vulnerable actors must not reproduce the resource asymmetry it is designed to counter in its own development infrastructure. Computational efficiency is an equity requirement, not an engineering preference.

---

## Part Four: The Architecture

### The Platform Principle

WorldSim is a situation-agnostic simulation platform. The engine, the measurement framework, the instrument architecture, and the UX are invariant across scenarios. What changes between scenarios is only the data inputs — initial conditions, scheduled policy inputs, confidence tiers, source registry entries.

The platform does not have a Greece mode, a tariff mode, or a Strait of Hormuz closure mode. It has one mode, fed with different ingredients. The kitchen stays the same. The cookware stays the same. The utensils stay the same. The only thing that changes is the ingredients, and the only thing that comes out differently is the dish.

This principle was arrived at through negative experience — through noticing that every time a new use case was proposed (What about tariffs? What about the Hormuz closure? What about annual budget planning?), the instinct was to design a new module for each case. That instinct produces a quilted-together tool: functionality that was designed for specific scenarios, that works well for those scenarios, and that creates architectural friction for scenarios it was not designed for.

The correct response to any new use case is a two-part question: what data inputs does this case require, and does the platform's current ingredient specification support them? If yes, the platform handles the case without modification. If no, the ingredient specification is extended — the data model is widened to accept a new type of input. The kitchen is not rebuilt. A new ingredient category is added to the pantry.

The tariff case requires a bilateral trade shock as an exogenous input. Does the platform support that? Not yet — the scheduled input system currently accepts fiscal policy inputs and monetary rate inputs. The extension required is to add trade policy inputs as a standard input type. That is a data model extension, not a new module.

The Hormuz closure case requires a commodity price shock as an exogenous input affecting multiple entities simultaneously. The extension required is a global commodity price parameter that propagates through the relationship graph to all entities with relevant trade exposure. That is a propagation rule addition, not a new module.

The annual budget planning case requires multi-scenario comparison across more than two scenarios. The extension required is to lift the current two-scenario comparison limit. That is a UI and API extension, not a new module.

The platform principle is a hard constraint on architectural proposals. Any proposal that requires scenario-specific modules rather than scenario-specific data inputs must document why the platform principle cannot be satisfied before it is accepted.

### The Graph, Not the Tree

The simulation engine is a multi-relational directed graph, not a tree.

The hierarchical structure — nation → region → sector → demographic cohort — is one layer of the graph. It represents administrative scope and identity. A higher node in the hierarchy has purview over a larger aggregate. This is the structure that makes intuitive sense: effects flow up from sectors to regions to nations; resources and spending flow down from nations to regions to sectors.

But this hierarchy is not the propagation medium. Effects do not travel through the parent-child edges of the hierarchy. They travel through a separate layer: the relationship graph, where edges are typed (trade, debt, alliance, currency union) and weighted, and where PropagationRules specify which event types travel along which edge types, with what attenuation, to what maximum depth.

Greece's fiscal contraction does not propagate to Germany because Germany is Greece's parent in some administrative hierarchy. It propagates because there is a trade relationship edge between GRC and DEU with a specific weight, and there are PropagationRules that specify how fiscal contraction events propagate along trade edges.

This architecture allows the simulation to represent facts that a purely hierarchical model cannot: that a currency union creates dependencies between countries at the same hierarchical level; that a debt relationship creates a dependency between a country and an international institution that is not in the hierarchical graph at all; that a geopolitical shock can propagate through an alliance network that cuts across every hierarchical boundary.

The directional intuition — resources flow down, value flows up — is not wrong. It describes a common pattern in how the propagation rules are configured for many scenarios. But it is a pattern that emerges from the configuration, not a structural property of the graph. The architecture is more general than the intuition.

### The Synthetic Data Framework

Data poverty is not a blocker. This is a founding commitment, and it required a significant architectural decision to honor it.

The tool's value proposition is highest precisely where institutional analytical capacity is lowest — global south finance ministries with thin data infrastructure and small technical teams. But those are also precisely the contexts where the data required to run a meaningful simulation analysis does not exist at sufficient quality or granularity.

The Zambia 2020 debt default case illustrates the problem. Zambia was the first African country to default during COVID-19. The human cost consequences were severe and predictable. But Zambia's macroeconomic data infrastructure in 2020 was thin. Survey data was delayed and inconsistently measured. National accounts estimates had wide error bars. A simulation that required Eurostat-quality input data to produce meaningful output would have been useless to Zambia.

The synthetic data framework addresses this through a hierarchy of inference methods. When real data is unavailable or of insufficient quality, WorldSim generates synthetic data using statistical inference from comparable economies — Bayesian hierarchical models when sufficient comparable country data exists, MICE imputation for bounded short gaps, bootstrap resampling as a fallback, structural extrapolation as a last resort before declaring structural absence.

Structural absence is important. When data absence is itself a signal — when a country has stopped reporting statistics, or expelled the measuring organization, or systematically falsified data — generating a synthetic estimate masks the signal. The honest response is a Structural Absence Declaration: the model cannot produce a meaningful estimate for this indicator in this context, and here is what data would unblock the estimate.

Every output derived from synthetic data is flagged at the indicator level — not with a global disclaimer, but per-indicator. A Tier 1 estimate based on primary source data and a Tier 4 synthetic estimate based on regional comparables must look visually distinct in the instrument cluster. Mixed-mode outputs — some real, some synthetic — require per-indicator provenance display.

The anomaly detection capability that synthetic baselines enable is deliberately constrained. Synthetic regional comparables can theoretically be used to flag when a country's published official data diverges implausibly — a form of data quality audit. But this capability is excluded from the primary instrument cluster, requires Technical Steering Committee sign-off before being enabled, is opt-in for the user, and is permanently excluded from Mode 3 (active control) sessions. The reason is specific: in an active negotiation, a false positive on the ministry's own published data can undermine the primary beneficiary's confidence in their own numbers. A tool built to serve finance ministries cannot undermine them. The asymmetry we are correcting runs one direction. So does the tool.

### The Information Asymmetry Problem Is Three-Layered

When the project first articulated the democratization mission — give the finance ministry of a vulnerable country the same analytical capability as the IMF — it was thinking primarily about the first layer: data availability. Does the data exist?

The synthetic data framework addresses that layer. But there are two more.

The second layer is data quality. Even where data exists, its reliability varies enormously. Greek unemployment data from Eurostat has a known methodology and consistent time series. Egypt's poverty rate data was suppressed and then revised. Venezuela's post-2015 macroeconomic data is deeply unreliable. The confidence tier system — which assigns Tier 1 through Tier 5 confidence levels to every indicator based on source quality, methodology, and recency — is the architectural response to this layer.

The third layer is institutional capacity asymmetry. A finance ministry official in a large economy has hundreds of economists, data teams, Bloomberg terminals, and access to proprietary models. A finance ministry official in a low-income country may have a small team using Excel and public data sources. WorldSim's value proposition is highest precisely in the third case. But the tool must be designed so that a user with limited technical background can extract meaningful analytical value without requiring a PhD in economics to interpret the outputs.

This is a design constraint, not just a policy commitment. It means that outputs must be self-interpreting for non-technical users. A CO2 boundary proximity score of 1.8 is meaningless without knowing that 1.0 means the boundary is exactly met and 1.8 means the boundary is exceeded by 80%. The instrument must tell the user what the number means, not just display the number. The human cost ledger must be legible to a finance minister, not just to a macroeconomist.

---

## Part Five: The Vision

### What Full Deployment Looks Like

The marquee cases that the project has identified — Greece 2010, the Cyprus bail-in, Egypt 2016, Argentina's serial defaults, the Asian financial crisis, the Strait of Hormuz — are not just backtesting fixtures. They are existence proofs of the tool's potential value.

In each of these cases, a decision was made in a room by people who did not have the analytical capability that WorldSim is being designed to provide. The informational gap was real. The human cost of the gap was documented. And in each case, the data to partially close the gap existed at the time — it simply was not in the models being used.

The founding question that recurs throughout the project's history is: if this tool had existed, and if it had been available to the party with less analytical power, would the outcome have been different?

The honest answer is: we do not know. The tool would not have given the finance ministry of Greece perfect foresight in 2010. It would not have prevented the political constraints that shaped the negotiation. It would not have resolved the fundamental question of whether Greece could remain in the eurozone without a debt restructuring.

But it might have changed the quality of the debate. It might have surfaced, before the programme was signed, that the fiscal multiplier assumption of 0.5 was inconsistent with the historical pattern for economies in currency unions with no monetary policy flexibility. It might have shown that the human development trajectory under the proposed programme crossed the unemployment MDA threshold at step three and did not recover within the six-year horizon. It might have given the Greek finance ministry negotiators a specific, citable finding to put on the table: "Our analysis shows that this programme path crosses the critical floor for social legitimacy at this step. Here is the counter-proposal that achieves debt sustainability while remaining above the floor."

That is a different conversation. Not a better outcome guaranteed — but a better conversation possible.

### The Flywheel

The tool makes users better. Better users make the tool better.

This is the long-game strategy. In the short term, WorldSim provides analytical capability to actors who currently lack it. In the medium term, those actors — finance ministry analysts who have used the tool through multiple programme cycles — accumulate expertise in reading multi-framework outputs, calibrating their intuitions against the model, and contributing scenario configurations and backtesting cases back to the project. In the long term, the community of practice that forms around the tool becomes itself a form of institutional capability — a distributed analytical resource that transcends any individual institution or government.

The open source commitment is essential to this flywheel. Community intelligence that accumulates through use is as valuable as the codebase. A Kenyan central banker who has run twenty scenarios through the tool knows things about the tool's behavior in East African economic conditions that the Engineering Lead in Canada does not know. That knowledge needs pathways to flow back into the model.

### The Kryptonite Frame

Late in one of the founding conversations, the Engineering Lead mentioned that he had been listening to the radio when the song "Shut Up and Dance With Me" came on, and the word "kryptonite" triggered an immediate association: WorldSim can become the kryptonite for the global south.

Kryptonite is a leveling mechanism. It exists to make an asymmetric contest winnable. In the mythology, it is the one material that brings Superman — the overwhelmingly more powerful party — to human-scale vulnerability. It does not make the other party stronger. It removes an unfair advantage.

WorldSim is not designed to make vulnerable countries smarter than the IMF. It is designed to remove one specific unfair advantage: the analytical asymmetry that allows one party to the negotiation to know, with greater precision, what the proposed terms will likely produce for human beings who are not in the room. That asymmetry is not a feature of markets or expertise or comparative advantage. It is a product of unequal access to analytical capability. Access can be equalized.

The kryptonite frame is useful not because it is combative — the goal is not to defeat the IMF or the World Bank — but because it is honest about the orientation. The tool has a point of view. It is on the side of the finance ministry team with three economists facing a team of forty. It is on the side of the quinoa farmer whose government may make a better decision because a tool exists. It is not neutral, and pretending to be neutral would be a form of dishonesty.

### The North Star

All of it comes down to a specific room, a specific table, and a specific person.

A finance minister of a small, vulnerable country is sitting across a table from an IMF negotiating team. She has limited time. She has limited staff. She has generational consequences riding on the decision she is about to make.

Does this decision make the tool more useful to that person in that moment?

If yes, proceed. If no, reconsider.

The quinoa farmer in Bolivia does not know this tool exists. Build it as if he does.

---

## Part Six: Honest Limitations and Open Questions

No founding document is complete without the list of things that are not yet resolved — the questions the project has named but not answered, the limitations it has identified but not addressed.

### What WorldSim Does Not Do

WorldSim does not model individual human behavior. It models aggregate behavior of demographic cohorts — income quintiles, age bands, employment sectors. The transition to agent-based modeling at the individual level is a known direction but not a current capability or near-term target.

WorldSim does not model real-time market dynamics. Currency attacks, bond market movements, bank runs — these operate on timescales of hours and minutes, not the annual or monthly timesteps that WorldSim currently uses. The adaptive temporal resolution architecture — which can switch to daily resolution when a crisis threshold is detected — is the long-term response to this limitation, but it is not yet implemented.

WorldSim does not currently model geopolitical constraints on programme design. The Pakistan case — where IMF programme design is constrained by US-Pakistan security relationships — is outside the current scope. The tool models the economic logic of a programme; it does not model the political economy of why certain programme designs are or are not available given geopolitical alignments. The political economy module (M11) is intended to address this, but the full problem is harder than any single module can solve.

WorldSim does not model cascade dynamics across sectors. The Bangladesh fuel shortage case — where a fuel shortage cascades to telecommunications towers, which cascades to financial services, which cascades to remittance flows — requires a causal meta-map of cross-sector dependencies that has been identified as a needed architectural element but has not been built. The causal meta-map is a long-term architectural commitment.

### What Is Not Yet Known

Whether the tool will achieve adoption by the actors it is designed to serve — finance ministry analysts in vulnerable countries — is an open question. Technical capability is not sufficient. The tool must be accessible, understandable, and trusted by those users. None of those properties are guaranteed by good engineering.

Whether the Goodhart's Law problem can be managed is an open question. Once WorldSim achieves institutional adoption, the indicators it tracks and the thresholds it sets may begin to be gamed. Countries may structure their programmes to avoid triggering MDA alerts rather than to genuinely address the underlying conditions. The tool's design includes explicit Goodhart's Law awareness — the methodology is transparent and the assumptions are inspectable — but it is not immune.

Whether the synthetic data framework will produce outputs that are useful rather than misleading in data-poor contexts is an open question. The methodological commitments are sound. The Chief Methodologist consultation has produced a rigorous framework. But the real-world test — running the tool against a country like Chad or Yemen with genuinely thin data — has not yet happened.

---

## Epilogue: The Project as Process

This document is a snapshot of a process that is ongoing.

The WorldSim project began as a conversation about what to build — a software developer returning to practice after fifteen years in management, interested in building something real rather than something theoretical. It became, fairly quickly, a conversation about a problem that mattered. And it has evolved, through two months of sustained dialogue, into something that feels like the beginning of an institution.

Not an institution in the formal sense — no staff, no office, no budget. But an institution in the sense that there are now values that have been articulated and committed to. There are architectural principles that have been arrived at through reasoning and will be defended through reasoning. There are documented processes for how decisions get made, how the model gets improved, how the community of contributors grows.

The founding conversations that produced this document will eventually be inaccessible — context limits are real, and the history compresses. This document is an attempt to preserve what matters from those conversations: not the technical decisions (those live in the ADRs and the code), not the operational procedures (those live in CLAUDE.md and the process documents), but the reasoning — the why beneath the what, the values beneath the architecture, the vision beneath the implementation.

The quinoa farmer in Bolivia does not know this project exists. We are building it as if he does.

---

*Document version 1.0 — synthesized May 2026 from the founding conversations of April–May 2026.*
*Canonical location: `docs/vision/worldsim-founding-document.md`*
*This document is the soul of the project. The operational documents are its skeleton. The code is its body. All three are needed.*
