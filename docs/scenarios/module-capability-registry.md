# Module Capability Registry

This document is the Domain Intelligence Council's reference for what the
WorldSim simulation can and cannot currently model. Every council review
and every scenario specification should consult this registry before
generating expectations about simulation behaviour.

This is a living document. It is updated whenever a new module is implemented
or an existing module's capabilities change. The registry is dated so that
readers can assess whether it reflects the current codebase.

**Last updated:** 2026-04-16
**Current milestone:** Milestone 1 — Simulation Core

---

## What the Simulation Can Currently Model

### Entity State Representation

The simulation can represent any entity (country, institution, region) as a
collection of named float attributes. Attributes are initialised from seed
data and can be updated by events.

**Can model:**
- Any numerical indicator that can be expressed as a float
- Entity metadata (name, ISO codes, etc.) stored separately from simulation
  attributes
- Hierarchical entity relationships (parent_id field)
- Basic spatial reference (geometry field, PostGIS integration in Milestone 2)

**Cannot currently model:**
- Attribute-level metadata (units, measurement framework tag, uncertainty range)
- Categorical attributes (regime type, currency peg status)
- Time series within an entity (only current-period state is held)

### Bilateral Relationships

The simulation can represent directed weighted relationships between pairs
of entities.

**Can model:**
- Directional trade relationships with weights reflecting coupling strength
- Debt relationships
- Alliance relationships
- Any other relationship type expressible as a directed edge with a float weight
- Multiple relationship types between the same entity pair

**Cannot currently model:**
- Dynamic relationship weights (weights are set at scenario initialisation
  and do not change during a run)
- Relationship attributes beyond weight (e.g. tariff rate, debt maturity profile)
- Relationship-level metadata (data source, vintage date)

### Event Propagation (ADR-001)

The simulation can propagate attribute deltas through the relationship graph.

**Can model:**
- Hop-by-hop attenuation: delta × attenuation_factor × edge.weight per hop
- Compound attenuation across multiple hops
- Additive accumulation from multiple propagation paths to the same entity
- Multiple propagation rules per event (different relationship types, different
  attenuation factors)
- Events that propagate along specific relationship types only
- Max_hops limiting propagation depth

**Cannot currently model:**
- Non-linear propagation (threshold effects, saturation)
- Asymmetric propagation (different behaviour in different directions)
- Relationship weight updating based on event history
- Feedback loops within a single timestep (propagation is one-pass)

### Input Orchestration (ADR-002)

The simulation can accept exogenous control inputs through the orchestration
layer.

**Can model:**
- Five input types: MonetaryPolicyInput, FiscalPolicyInput, TradePolicyInput,
  EmergencyPolicyInput, StructuralPolicyInput
- Scheduled inputs at specific timesteps
- Contingent inputs triggered by attribute threshold conditions
- Cooldown periods preventing repeated triggering
- Complete audit trail of all injected inputs
- Multi-step scenario execution with state history

**Cannot currently model:**
- Input validation against feasible policy space
- Multi-stage inputs (inputs that unfold over multiple timesteps automatically)
- Input interactions (two simultaneous inputs whose effects depend on each other)

---

## What the Simulation Cannot Currently Model

The modules listed here are specified in CLAUDE.md and planned for future
milestones. Until a module is implemented, its domain of effects cannot be
modelled endogenously. Exogenous ControlInputs can inject point-in-time
shocks as proxies, but the module's endogenous dynamics (multipliers, feedback
loops, regime-switching behaviour) are absent.

### Macroeconomic Module (Planned — Milestone X)

**Cannot currently model:**
- GDP growth rate dynamics (fiscal multiplier, consumption function)
- Inflation dynamics (Phillips curve, monetary transmission)
- Debt sustainability analysis (debt service ratios, rollover risk)
- Fiscal multiplier (including inversion in depressed demand regimes)
- Interest rate dynamics and monetary transmission mechanism
- Output gap and potential growth

**Impact on scenario outputs:** Scenarios involving fiscal consolidation,
monetary policy, or debt dynamics are missing their primary endogenous engine.
ControlInput shocks can inject first-round effects but compounding dynamics
and feedback loops are absent.

### Trade and Currency Module (Planned — Milestone X)

**Cannot currently model:**
- Bilateral trade flows and their evolution under tariff shocks
- Exchange rate dynamics (pass-through, J-curve effects)
- Terms of trade dynamics
- Trade balance and current account dynamics
- Trade diversion and deflection patterns
- Dynamic relationship weights reflecting evolving trade patterns

**Impact on scenario outputs:** Trade policy scenarios (tariffs, sanctions)
can inject first-round shocks but cannot model the rebalancing and diversion
dynamics that typically follow. The simulation has no mechanism to update
trade weights in response to policy changes.

### Monetary System Module (Planned — Milestone X)

**Cannot currently model:**
- Reserve currency dynamics
- SWIFT/payment network exposure
- Sovereign debt holdings matrix
- Currency confidence indices
- De-dollarisation dynamics
- Capital flight and sudden stop dynamics

### Capital Flow Module (Planned — Milestone X)

**Cannot currently model:**
- Foreign direct investment flows
- Portfolio flow dynamics
- Hot money and capital flight
- Illicit financial flows

### Geopolitical Module (Planned — Milestone X)

**Cannot currently model:**
- Alliance relationship dynamics
- Military capability indices
- Diplomatic channel quality
- Information environment integrity
- Escalation and de-escalation dynamics

### Climate Module (Planned — Milestone X)

**Cannot currently model:**
- Climate forcing from IPCC scenario data
- Agricultural stress indices
- Water stress and extreme event modelling
- Climate-driven migration

### Demographic and Health Module (Planned — Milestone X)

**Cannot currently model:**
- Population dynamics and cohort modelling
- Health system capacity and stress
- Education attainment dynamics
- Migration flows

### Financial Warfare Module (Planned — Milestone X)

**Cannot currently model:**
- Currency attack vulnerability indices
- Sanctions exposure modelling
- Cyber infrastructure vulnerability
- Information environment manipulation

### Institutional Cognition Module (Planned — Milestone X)

**Cannot currently model:**
- Institutional Cognitive Integrity Index
- Policy-reality divergence tracking
- Ghost flight detection (institution executing outdated programming)

---

## Interpreting Results Given Current Limitations

Any scenario run against the current simulation is modelling:
1. The first-round direct effect of the injected ControlInput on the source entity
2. Propagation of that effect through static relationship edges

The simulation is NOT modelling:
- Endogenous module responses to changed state
- Dynamic relationship weight evolution
- Multiplier and feedback loop effects
- Regime-switching behaviour
- Any of the module domains listed above as absent

**Safe conclusions from current simulation output:**
- Direction of first-round propagation through the trade/relationship network
- Relative magnitude of exposure across entities (which countries are more
  or less connected to the shock source)
- Structural network properties (which entities are hubs, which are peripheral)

**Conclusions that should not be drawn from current output:**
- Precise magnitudes (no calibrated multipliers or feedback loops)
- Dynamic trajectories over time (modules driving endogenous state change are absent)
- Policy optimisation (no endogenous response to simulate the counterfactual)
- Crisis threshold predictions (no threshold dynamics in current engine)

This registry will be updated with each milestone. Domain Intelligence Council
agents should re-read this registry before completing their scenario review
sections as the simulation's capabilities evolve.
