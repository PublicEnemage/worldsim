# ADR-002: Input Orchestration Layer

## Status
Accepted

## Validity Context

**Standards Version:** 2026-04-15 (date standards documents were established)
**Valid Until:** Milestone 3 completion
**License Status:** CURRENT

**Last Reviewed:** 2026-04-21 — Milestone 2 exit review. No renewal triggers
fired during Milestone 2. License Status confirmed CURRENT. No changes to
`ControlInput` type taxonomy, audit trail schema requirements, or
`MeasurementFramework` tagging requirements occurred during this milestone.
License renewed for Milestone 3. Next scheduled review at Milestone 3
completion.

**Previously reviewed:** 2026-04-19 — Amendment 1 (SCR-001) applied. See
Amendment 1 section below. License Status renewed to CURRENT after
implementation verified by 210 passing tests and SCAN-004 (0 violations).

**Renewal Triggers** — any of the following fires the CURRENT → UNDER-REVIEW
transition:
- `ControlInput` type taxonomy changes in `CODING_STANDARDS.md` or any ADR
  amendment (e.g., new capital flow or geopolitical input types added)
- Audit trail schema requirement changes (e.g., `DATA_STANDARDS.md` adds
  data-lineage requirements that must be carried by `ControlInputAuditRecord`)
- Uncertainty quantification standard additions to `DATA_STANDARDS.md` that
  affect how events carry uncertainty (e.g., events required to carry
  confidence intervals alongside affected_attribute deltas)
- Multi-framework tagging requirements added to `CODING_STANDARDS.md` that
  affect event structure (e.g., requiring events to carry both a primary
  `MeasurementFramework` tag and secondary framework tags for cross-framework
  effects)

## Date
2026-04-16

## Context

The simulation now has a working propagation engine (ADR-001) that applies
Events to SimulationState[T] and produces SimulationState[T+1]. Modules
return Events. The engine applies them. But neither ADR-001 nor the engine
addresses a foundational question: where do Events originate?

Two distinct sources exist:

**Endogenous events** — the simulation computes these from internal state.
A macroeconomic module observes a high debt-to-GDP ratio and generates an
interest rate premium event. A climate module reads drought stress indices
and generates an agricultural output event. These events are outputs of
model equations applied to current state.

**Exogenous control inputs** — human decisions injected regardless of what
modules would compute. A finance minister raises the policy rate by 50 basis
points. A government announces tariffs. A country accepts an IMF program.
These are not outputs of simulation equations — they are decisions that
override or supplement what the model would do on its own.

Both must ultimately become Events for the propagation engine. But they have
fundamentally different characteristics:

| Property | Endogenous Events | Exogenous Control Inputs |
|---|---|---|
| Source | Module equations | Human decision |
| Determinism | Computed from state | Injected regardless of state |
| Audit trail | Implicit in module logic | Must be explicitly recorded |
| Reproducibility | Re-run module on same state | Replay the control input log |
| Scenario definition | Partial | Central — scenarios ARE their inputs |

If exogenous inputs flow through modules, the distinction disappears.
The audit trail becomes opaque. Scenarios become non-reproducible. The
same scenario run twice produces different results if modules are updated.
The architecture requires a dedicated layer that owns the exogenous path.

Additionally, Milestone 1 needs a runnable demo: seed real country data,
inject a real policy scenario, run ten timesteps, observe propagation.
The orchestration layer is the minimum required infrastructure for this.

## Decision

### The Endogenous/Exogenous Distinction

Control inputs are exogenous. Their presence in the simulation is the result
of a human decision, not a model equation. The orchestration layer is the
sole entry point for all exogenous inputs. No module handles its own
exogenous inputs directly. Every exogenous input passes through the
orchestrator, which validates it, translates it to Events, and records it
in an immutable audit trail before passing those Events to the propagation
engine alongside the endogenous Events produced by modules.

### ControlInput: The Abstract Base

All exogenous inputs inherit from `ControlInput`. Every control input carries
the information needed to reconstruct the scenario: who made the decision,
what role they held, what entity was targeted, when it takes effect, and why.

```python
@dataclass(kw_only=True)
class ControlInput(ABC):
    input_id: str                       # unique identifier
    actor_id: str                       # who authorised this input
    actor_role: str                     # their role in the scenario
    target_entity: str                  # primary affected entity
    effective_date: datetime            # simulation-time effective date
    justification: str                  # human-readable rationale
    source: InputSource                 # channel through which input arrived
    timestamp: datetime                 # wall-clock creation time
    propagation_rules: list[PropagationRule]  # how generated Events propagate

    @abstractmethod
    def to_events(self, timestep: datetime) -> list[Event]: ...
```

### InputSource Enum

```python
class InputSource(Enum):
    UI = "ui"                           # web interface
    API = "api"                         # REST API call
    CLI = "cli"                         # command-line injection
    BULK_FEED = "bulk_feed"             # batch data import
    SCENARIO_SCRIPT = "scenario_script" # scripted scenario definition
    CONTINGENT_TRIGGER = "contingent_trigger"  # fired by ContingentInput
```

### Five Concrete ControlInput Subclasses

**MonetaryPolicyInput** — central bank instruments:
```python
instrument: MonetaryInstrument  # POLICY_RATE | RESERVE_REQUIREMENT |
                                 # ASSET_PURCHASE | EXCHANGE_RATE_INTERVENTION
value: Decimal                  # magnitude (rate as fraction, volume in USD)
duration_periods: int = 1       # timesteps this input remains active
```

**FiscalPolicyInput** — finance ministry instruments:
```python
instrument: FiscalInstrument    # SPENDING_CHANGE | TAX_RATE_CHANGE |
                                 # DEFICIT_TARGET | DEBT_ISSUANCE
sector: str                     # targeted sector, or "" for economy-wide
value: Decimal                  # magnitude in canonical units
duration_years: int = 1
```

**TradePolicyInput** — external-sector instruments:
```python
instrument: TradeInstrument     # TARIFF_RATE | TRADE_AGREEMENT | SANCTIONS |
                                 # EXPORT_CONTROL | CURRENCY_SWAP
source_entity: str              # entity imposing the policy
affected_sector: str            # goods | services | agriculture | technology
value: Decimal                  # tariff rate, volume, etc.
retaliation_modeled: bool = False  # include retaliation event?
```

**EmergencyPolicyInput** — crisis instruments:
```python
instrument: EmergencyInstrument # CAPITAL_CONTROLS | BANK_HOLIDAY |
                                 # DEBT_MORATORIUM | NATIONALIZATION |
                                 # IMF_PROGRAM_ACCEPTANCE | DEFAULT_DECLARATION
parameters: dict[str, Any]      # instrument-specific parameters
expected_duration: int = 1      # expected timesteps in force
```

**StructuralPolicyInput** — long-horizon institutional changes:
```python
instrument: StructuralInstrument  # PRIVATIZATION | NATIONALIZATION |
                                   # REGULATORY_CHANGE | CONSTITUTIONAL_CHANGE |
                                   # INSTITUTIONAL_REFORM
affected_sector: str
parameters: dict[str, Any]
implementation_years: int = 1     # full implementation horizon
```

### InputOrchestrator Interface

The orchestrator is the control plane for the simulation's exogenous path.

```python
class InputOrchestrator(ABC):
    @abstractmethod
    def inject(
        self,
        control_input: ControlInput,
        session_id: str,
    ) -> list[Event]:
        """Validate, translate, audit-log, and return Events for one input."""

    @abstractmethod
    def advance_timestep(
        self,
        current_state: SimulationState,
        modules: list[SimulationModule],
        scheduled_inputs: list[ControlInput],
    ) -> SimulationState:
        """One full simulation tick.

        Collects scheduled inputs, runs modules, merges all events,
        propagates, returns State[T+1].
        """

    @abstractmethod
    def check_contingents(self, state: SimulationState) -> list[ControlInput]:
        """Evaluate registered ContingentInputs against current state.

        Returns ControlInputs whose conditions are now met and whose
        cooldown has expired.
        """
```

### ControlInputAuditRecord

Every control input ever processed is recorded here. Scenarios are
reproducible by replaying their audit logs in order.

```python
@dataclass(kw_only=True)
class ControlInputAuditRecord:
    record_id: str
    scenario_id: str
    session_id: str
    timestep: datetime
    input_type: str              # class name of the ControlInput subclass
    source: InputSource
    actor_id: str
    actor_role: str
    justification: str
    raw_input: dict[str, Any]    # full serialised ControlInput
    translated_events: list[str] # event_ids of generated Events
    timestamp: datetime          # wall-clock time of processing
```

The `AuditLog` for Milestone 1 is an in-memory list. Persistent storage
(PostgreSQL) is introduced in Milestone 2 alongside the database layer.

### ContingentInput

This is where regime-switching and tipping point dynamics live. A
`ContingentInput` watches a state condition and fires its embedded
`ControlInput` automatically when the condition is met.

```python
@dataclass(kw_only=True)
class ContingentInput:
    contingent_id: str
    condition: StateCondition    # entity, attribute, operator, threshold
    input: ControlInput          # fires when condition is met
    cooldown_periods: int        # minimum periods between firings
    documented_rationale: str    # why this contingent exists
    empirical_basis: str         # historical cases supporting this trigger
```

`StateCondition`:
```python
@dataclass(kw_only=True)
class StateCondition:
    entity_id: str
    attribute: str
    operator: ComparisonOperator  # LT | GT | LTE | GTE | EQ
    threshold: float
```

Historical use: a contingent that fires capital controls when reserve
coverage drops below 3 months of imports models the empirically documented
IMF Article IV trigger. The `empirical_basis` field documents the case.

### ScenarioRunner: Minimum Viable Orchestrator for Milestone 1

The full `InputOrchestrator` interface is designed for a web service
(Milestone 2+). For Milestone 1, `ScenarioRunner` is the minimum viable
implementation: it accepts a prepared scenario as Python objects and
executes it synchronously, returning the complete state history.

```python
class ScenarioRunner(InputOrchestrator):
    def __init__(
        self,
        initial_state: SimulationState,
        scheduled_inputs: list[tuple[int, ControlInput]],
        modules: list[SimulationModule],
        n_steps: int,
        audit_log: AuditLog | None = None,
        contingent_inputs: list[ContingentInput] | None = None,
        session_id: str | None = None,
        timestep_delta: timedelta | None = None,  # default: 365 days
    ) -> None: ...

    def run(self) -> list[SimulationState]:
        """Execute the scenario and return the complete state history."""
```

`scheduled_inputs` is a list of `(step_index, ControlInput)` tuples.
Step 0 is the initial state; inputs at step 1 fire before the first
advance. This makes it natural to define scenarios as "at year 1, do X".

## Alternatives Considered

### Alternative 1: Modules handle their own exogenous inputs directly

Each module could accept policy parameters as configuration and inject its
own Events for policy changes. The MacroeconomicModule handles fiscal inputs.
The MonetaryModule handles rate changes.

**Rejected because:**

1. **Invisible audit trail.** When a fiscal shock appears in the output, there
   is no single place to trace it to. Was it generated by the module's equation,
   or was it an injected policy change? The distinction matters enormously for
   scenario reproducibility and for understanding what the simulation is
   actually doing.

2. **Non-reproducible scenarios.** A scenario defined as "module configuration
   parameters" is reproduced by re-running with the same configuration — which
   means the results depend on the module's current implementation. If the
   module is updated, the scenario changes. Scenarios defined as audit logs
   of ControlInputs are reproduced by replaying the log regardless of module
   changes.

3. **Module coupling.** Each module becomes responsible for both its domain
   equations AND its input channel. These are separate concerns. A module
   that handles its own input channel cannot be tested without simulating
   the input mechanism. A module that only responds to Events can be tested
   on any arbitrary Event sequence.

4. **No unified input surface.** The web UI, the API, the CLI, the scenario
   script, and contingent triggers all need to inject inputs. With
   module-handled inputs, each module needs its own input surface. With
   a unified orchestrator, all input channels converge on one interface.

### Alternative 2: Events as the only input mechanism (no ControlInput layer)

Accept that all inputs — exogenous and endogenous — are Events and build
no distinction between them. Callers construct Events directly and pass
them to the propagation engine.

**Rejected because:**

1. **Lost provenance.** An Event records source_entity_id, not who the human
   actor was. A finance minister's policy decision and a module's output look
   identical in the event log. The ControlInput layer preserves the provenance.

2. **No validation gate.** The orchestrator's `inject()` method validates inputs
   before translating them to Events. Raw Event construction bypasses validation.
   In a policy simulation that informs real decisions, an unvalidated input that
   produces a plausible-looking output is worse than a rejected input — it
   contaminates the analysis.

3. **No replay semantics.** A list of Events is harder to replay than a list of
   ControlInputs. ControlInputs carry enough human-readable context (justification,
   actor_role, effective_date) to make the audit log interpretable as a scenario
   narrative, not just a sequence of state mutations.

## Consequences

### Positive
- Every control input is auditable and traceable to a specific actor and decision
- Scenarios are reproducible by replaying their audit logs
- All input channels (UI, API, CLI, contingent triggers) converge on one interface
- Modules are fully decoupled from input mechanisms — they respond only to Events
- ContingentInput provides first-class support for threshold-triggered dynamics
- ScenarioRunner provides a working Milestone 1 demo path without requiring the
  full web service infrastructure

### Negative
- Every policy action requires constructing a ControlInput, then translating to
  an Event — two steps instead of one. For rapid exploratory work, this feels
  like overhead compared to directly manipulating state.
- The `to_events()` translation in each subclass encodes assumptions about how
  a policy action maps to attribute deltas. These translations are necessarily
  simplified until the full domain modules (Macroeconomic, Trade, etc.) are
  built. Milestone 1 translations are directionally correct but magnitudes
  are placeholders.
- The in-memory AuditLog in Milestone 1 is lost when the process exits.
  Scenarios must be fully replayed from source to reproduce results until
  the Milestone 2 database layer is in place.

## Diagrams

- Sequence diagram: `docs/architecture/ADR-002-sequence-timestep-cycle.mmd`
- Class diagram: `docs/architecture/ADR-002-class-controlinput-hierarchy.mmd`

## Next ADR

ADR-003 will address the PostGIS spatial data model and database schema
(originally planned as ADR-002 in the ADR-001 footer — scope shifted when
the orchestration layer proved foundational for Milestone 1).

---

## Amendment 1 — SCR-001: MonetaryInput Split and Quantity Adoption

**Date:** 2026-04-19
**Closes:** #58 (MonetaryPolicyInput split — Option C)
**Implemented in:** PR closing #51, #58, #65–#68

### What Changed

`MonetaryInstrument` split into two enums:
- `MonetaryRateInstrument` — POLICY_RATE, RESERVE_REQUIREMENT
- `MonetaryVolumeInstrument` — ASSET_PURCHASE, EXCHANGE_RATE_INTERVENTION

`MonetaryPolicyInput` split into two dataclasses:
- `MonetaryRateInput(ControlInput)` — `value: Decimal`; produces a RATIO
  `Quantity` delta (dimensionless rate change)
- `MonetaryVolumeInput(ControlInput)` — `value: MonetaryValue`; produces a
  `MonetaryValue` delta (typed monetary amount with currency, price basis,
  and exchange rate type)

**Rationale for the split:** Monetary rate instruments (policy rate, reserve
requirement) are dimensionless ratios. Monetary volume instruments (asset
purchases, FX interventions) are monetary amounts requiring a currency code,
price basis, and exchange rate type. Conflating them in a single class with
`value: Decimal` forced a type-unsafe conversion at `to_events()` time and
prevented the propagation engine from applying correct `variable_type` semantics.

All `to_events()` implementations for all `ControlInput` subclasses now produce
`affected_attributes: dict[str, Quantity]` (SCR-001 alignment). Event deltas
carry `variable_type`, `confidence_tier`, and `measurement_framework` from the
control input's semantics.

`StateCondition.is_met()` uses `entity.get_attribute_value(key) -> Decimal` then
`float()` for threshold comparison, avoiding direct float-on-entity-attribute
assignment.

### Audit Record Impact

`ControlInputAuditRecord.input_type` now records `"MonetaryRateInput"` or
`"MonetaryVolumeInput"` where it previously recorded `"MonetaryPolicyInput"`.
Existing audit logs produced before this amendment that reference
`"MonetaryPolicyInput"` remain valid historical records; replay of those logs
requires mapping the old name to the appropriate new subclass based on the
`instrument` field value.
