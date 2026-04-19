# SCR-001: Quantity Type System and MonetaryValue Structural Change

## Review Metadata

| Field | Value |
|---|---|
| **Review ID** | SCR-001 |
| **Initiated** | 2026-04-17 |
| **Standards under review** | `CODING_STANDARDS.md` § "Monetary Arithmetic", `DATA_STANDARDS.md` § "Units and Measurements" and § "Currency and Monetary Value Standards" |
| **Linked issues** | #51 (Quantity type system, Option C), #58 (MonetaryPolicyInput split — depends on SCR-001) |
| **Reviewers** | QA Agent, Architect Agent, Chief Methodologist, Development Economist, Intergenerational Advocate |
| **Status** | Complete — pending Engineering Lead disposition |

---

## Materiality Test

**Test:** Does a compliant implementation written before this change become
non-compliant after it?

**Result: MATERIAL.**

The current `CODING_STANDARDS.md` prohibits `float` for monetary arithmetic.
It does not prohibit `dict[str, float]` as the entity attribute store — the
existing `SimulationEntity.attributes: Dict[str, float]` definition in the
ADR-001 diagram example is inside `CODING_STANDARDS.md` itself. A module that
writes `float` values into `attributes` is currently compliant. After this
change, it must fail CI.

Five distinct new constraints apply to existing and future code:
1. `SimulationEntity.attributes` must be `dict[str, Quantity]`, not `dict[str, float]`
2. `MonetaryValue` must be a `Quantity` subclass (structural relationship change)
3. Every `Quantity` must carry a `variable_type` (new required field)
4. Confidence tier must propagate arithmetically via lower-of-two (new rule)
5. Ingestion pipelines must assign `confidence_tier` explicitly — no defaulting

All five rules make previously compliant code non-compliant. This review
follows the Material Standards Change Review Sequence in `MILESTONE_RUNBOOK.md`.

**Note on scope of #58 (MonetaryPolicyInput split):** Splitting
`MonetaryPolicyInput` into `MonetaryRateInput` and `MonetaryVolumeInput` is
an ADR-002 amendment, not a standards change. However, it depends on SCR-001
completing: `MonetaryRateInput.value` would be a dimensionless `Quantity` and
`MonetaryVolumeInput.value` would be a `MonetaryValue`. SCR-001 is a hard
prerequisite for implementing Option C on #58.

---

## Draft A — Proposed CODING_STANDARDS.md Replacement

**Replaces:** § "Monetary Arithmetic: `Decimal`, Never `float`" (currently lines 164–200)
**New section title:** "Monetary and Quantity Standards"

The following block is the complete proposed replacement text, ready to splice
in at the same location:

---

### Monetary and Quantity Standards

#### Why `Quantity`, Not Raw Numbers

Every physical and economic measurement in the simulation is a `Quantity`
(defined in `DATA_STANDARDS.md §Units and Measurements`). Never raw `float`,
never raw `Decimal` without a unit. This applies to entity attributes, event
deltas, module outputs, and ingestion pipeline outputs.

**Rationale.** Float arithmetic accumulates error silently. A raw `Decimal`
carries a number but discards the unit, the provenance, the observation date,
and the confidence tier that give the number meaning. A `Quantity` makes unit
errors loud and immediate (conversion raises `UnitError` when dimensions are
incompatible), carries every value back to a registered source, and propagates
confidence through every derived computation. A finance minister whose scenario
analysis rests on a silent unit error deserves better than we can deliver with
raw numbers.

The Mars Climate Orbiter was lost to an imperial/metric unit mismatch that
produced plausible-looking wrong values for nine months. WorldSim simulations
may inform decisions about whether a country should accept an IMF program.
The bar for correctness is the same.

#### Attribute Store: `dict[str, Quantity]`

`SimulationEntity.attributes` holds `Quantity` values, not floats:

```python
# Correct
attributes: dict[str, Quantity] = {
    "gdp": Quantity(
        value=Decimal("44e9"),
        unit=USD_2015,
        observation_date=date(2023, 1, 1),
        source_registry_id="WB_WDI_GDP_2024",
        confidence_tier=1,
        variable_type=VariableType.FLOW,
    ),
    "debt_gdp_ratio": Quantity(
        value=Decimal("1.46"),
        unit=DIMENSIONLESS,
        observation_date=date(2023, 1, 1),
        source_registry_id="IMF_WEO_2024",
        confidence_tier=1,
        variable_type=VariableType.RATIO,
    ),
}

# Forbidden — loses units, provenance, confidence, and variable type
attributes: dict[str, float] = {"gdp": 44e9, "debt_gdp_ratio": 1.46}
```

Event `affected_attributes` follows the same rule: `dict[str, Quantity]`, not
`dict[str, float]`. The delta carried by an Event is a `Quantity` — it has
units, a confidence tier, and a variable type that the propagation engine
uses to apply the delta correctly.

#### The `variable_type` Field

Every `Quantity` carries a `variable_type`. The propagation engine uses this
to determine how the value behaves across timesteps:

```python
class VariableType(Enum):
    STOCK = "stock"
    # Measures a level at a point in time.
    # Examples: foreign exchange reserves, debt outstanding, population.
    # Propagation behavior: inherits previous period value if no event changes it.

    FLOW = "flow"
    # Measures change or activity over a period.
    # Examples: GDP, exports, fiscal deficit, tax revenue.
    # Propagation behavior: resets each period; must be produced by a module or input.

    RATIO = "ratio"
    # Dimensionless fraction derived from other quantities.
    # Examples: debt/GDP, reserve coverage months, inflation rate.
    # Propagation behavior: recomputed from inputs each period; not stored independently.

    DIMENSIONLESS = "dimensionless"
    # Index or score with no natural unit — not a ratio of two quantities.
    # Examples: HDI, Freedom House score, V-Dem indicators, capability indexes.
    # Propagation behavior: update rule defined by the module that owns the variable.
```

Misclassifying a FLOW as a STOCK causes it to accumulate across periods
where it should reset. Misclassifying a STOCK as a FLOW loses the carried
balance between periods. These are simulation correctness failures, not
warnings.

**Classification reference:**

| Variable | Correct type | Common error and consequence |
|---|---|---|
| GDP | FLOW | STOCK — accumulates, producing nonsense multi-period totals |
| Exports | FLOW | STOCK |
| Fiscal deficit | FLOW | STOCK |
| Foreign exchange reserves | STOCK | FLOW — reserve level lost between periods |
| Debt outstanding | STOCK | FLOW |
| Population | STOCK | FLOW |
| Debt/GDP ratio | RATIO | STOCK — recomputing is not stored; storing creates staleness |
| Inflation rate | RATIO | FLOW |
| Reserve coverage (months of imports) | RATIO | STOCK |
| HDI | DIMENSIONLESS | RATIO — HDI is not a fraction of two commensurable quantities |
| Freedom House score | DIMENSIONLESS | RATIO |
| V-Dem indicators | DIMENSIONLESS | RATIO |
| Capability indexes (HCL outputs) | DIMENSIONLESS | RATIO |

#### Monetary Arithmetic: `Decimal`, Never `float`

All monetary arithmetic uses Python's `decimal.Decimal`. Never `float`.

```python
from decimal import Decimal, getcontext

# Set precision globally at application startup
getcontext().prec = 28

# Correct
interest_payment = principal * Decimal("0.025")

# Forbidden — float monetary arithmetic
interest_payment = principal * 0.025
```

`float` is prohibited in `backend/app/`. The CI compliance scan enforces this.
The one permitted exception is intermediate mathematical computation in NumPy
operations on dimensionless propagation weights (e.g., relationship weight
matrices). These must be explicitly commented and must not touch `Quantity`
or `MonetaryValue` values directly.

#### `MonetaryValue` as a `Quantity` Subclass

`MonetaryValue` (defined in `DATA_STANDARDS.md §Currency and Monetary Value
Standards`) is a `Quantity` subclass. All `Quantity` rules — including
`variable_type`, `confidence_tier`, and `source_registry_id` requirements —
apply to monetary values.

```python
# Correct — MonetaryValue is a Quantity, inherits all required fields
export_revenue = MonetaryValue(
    value=Decimal("1.2e9"),     # 'value' is the inherited Quantity field
    unit=USD_2015,              # canonical internal unit
    currency_code="GHS",        # source currency at ingestion (converted on write)
    price_basis=PriceBasis.CONSTANT,
    exchange_rate_type=ExchangeRateType.PPP,
    observation_date=date(2023, 1, 1),
    source_registry_id="WB_WDI_BX_2024",
    confidence_tier=1,
    variable_type=VariableType.FLOW,  # export revenue is a period flow
)

# Forbidden — bypassing MonetaryValue with raw Decimal
export_revenue = Decimal("1.2e9")
```

Do not bypass `MonetaryValue` with raw `Decimal` arithmetic except inside the
`Quantity` and `MonetaryValue` types' own implementations. Bypassing the type
loses the currency code, price basis, exchange rate type, and confidence tier
that give the number meaning in the simulation.

#### `confidence_tier` Propagation

When a calculation derives a new `Quantity` from two or more `Quantity` inputs,
the output `confidence_tier` is the **minimum** of all input tiers.

```python
# Correct — lower-of-two rule applied
def compute_debt_service_ratio(
    total_debt: Quantity,
    export_revenue: Quantity,
) -> Quantity:
    """Compute DSR; output tier is the minimum of both input tiers."""
    return Quantity(
        value=total_debt.value / export_revenue.value,
        unit=DIMENSIONLESS,
        variable_type=VariableType.RATIO,
        observation_date=max(
            total_debt.observation_date, export_revenue.observation_date
        ),
        source_registry_id=derive_composite_lineage_id([total_debt, export_revenue]),
        confidence_tier=min(total_debt.confidence_tier, export_revenue.confidence_tier),
    )

# Forbidden — tier not propagated, output silently appears as Tier 1
def compute_debt_service_ratio(debt: Decimal, revenue: Decimal) -> Decimal:
    return debt / revenue
```

**Rationale.** A derived output is never more trustworthy than its least
trustworthy input. Silently assigning a high confidence tier to a value
derived from a low-confidence estimate launders uncertainty — the output
looks authoritative when it is not. This is a deliberately conservative
policy: when inputs have identical tiers, it holds; when inputs have
unequal tiers, it preserves the weaker signal.

#### Ingestion Pipeline Requirements

Every value entering the simulation through an ingestion pipeline must, at
the ingestion boundary:

1. Have a registered `source_id` in the `SourceRegistry` before the pipeline
   writes any data
2. Carry an explicit `confidence_tier` assigned from the Data Quality Tier
   System in `DATA_STANDARDS.md` — no defaulting permitted
3. Carry an explicit `variable_type` — no defaulting to `DIMENSIONLESS`
4. Be wrapped in a `Quantity` (or `MonetaryValue`) — no raw numbers after
   the ingestion boundary

The ingestion boundary is the single point at which raw source data becomes
a `Quantity`. After that boundary, no code in `backend/app/` introduces bare
floats or bare `Decimal` values as attribute values.

#### Usage Table

| Context | Correct | Forbidden |
|---|---|---|
| Entity attribute store | `dict[str, Quantity]` | `dict[str, float]`, `dict[str, Decimal]` |
| Monetary attribute | `MonetaryValue` (Quantity subclass) | `Decimal`, `float` |
| Dimensionless rate/ratio | `Quantity(variable_type=RATIO)` | bare `Decimal` as attribute |
| Capability/index | `Quantity(variable_type=DIMENSIONLESS)` | bare `float` or `Decimal` |
| Intermediate arithmetic | `Decimal` (temporary, in-function) | `float` (anywhere in backend/app/) |
| NumPy propagation weight | `float` (with explicit comment) | `Decimal` (NumPy incompatible) |
| Confidence propagation | `min(tier_a, tier_b)` | Assigning a fixed tier to derived output |
| Module output | `list[Event]` with `Quantity` deltas | `list[Event]` with float deltas |
| Event delta | `Quantity` with matching `variable_type` | `float` delta |

#### Consequential Diagram Update

The ADR-001 class diagram example in § "Diagram Standards" below must be
updated in the same commit as any implementation of this standard. Specifically:
- `SimulationEntity.attributes: Dict[str, float]` → `attributes: dict[str, Quantity]`
- `Event.affected_attributes: Dict[str, float]` → `affected_attributes: dict[str, Quantity]`
- `Relationship.attributes: Dict[str, float]` → `attributes: dict[str, Any]`
  (Relationship attributes are mixed: `weight: float` is a dimensionless
  propagation coefficient; other fields may be Quantity. Architect review
  required before mandating Quantity here — see Architect Agent findings below.)

---

*End of Draft A.*

---

## Draft B — Proposed DATA_STANDARDS.md Additions

**Modifies:** § "Units and Measurements" — adds `variable_type` field to
`Quantity` and inserts `VariableType` enum; adds "Confidence Tier Propagation"
subsection after the `Quantity` definition.

**Modifies:** § "Currency and Monetary Value Standards" — restructures
`MonetaryValue` as a `Quantity` subclass.

### B-1: Addition to § "Units and Measurements" — `Quantity` type

Replace the current `Quantity` dataclass block with:

```python
class VariableType(Enum):
    STOCK = "stock"           # level at a point in time (reserves, debt outstanding)
    FLOW = "flow"             # change over a period (GDP, exports, deficit)
    RATIO = "ratio"           # dimensionless fraction derived from other quantities
    DIMENSIONLESS = "dimensionless"  # index or score not reducible to a ratio

@dataclass(kw_only=True)
class Quantity:
    value: Decimal             # never float
    unit: Unit
    variable_type: VariableType  # required; see VariableType enum above
    observation_date: date
    source_registry_id: str    # must be registered in SourceRegistry
    confidence_tier: int       # 1–5, see Data Quality Tier System

    def convert_to(self, target_unit: Unit) -> "Quantity":
        """Convert to target unit. Raises UnitError if dimensions incompatible."""
        if self.unit.dimension != target_unit.dimension:
            raise UnitError(
                f"Cannot convert {self.unit.dimension} to {target_unit.dimension}"
            )
        ...
```

### B-2: New subsection after the `Quantity` definition

Insert after the `Quantity` block, before the `Unit` type:

---

#### Confidence Tier Propagation

When a calculation derives a new `Quantity` from existing `Quantity` inputs,
the output `confidence_tier` is the **minimum** of all input tiers.

```
confidence_tier(output) = min(confidence_tier(input₁), confidence_tier(input₂), ...)
```

This is a deliberately conservative policy. Its properties:
- **Monotone non-increasing**: derived quantities cannot be more confident
  than their least confident input.
- **Known direction bias**: it overstates uncertainty when inputs are
  independent and mutually corroborating. This is documented and accepted —
  see SCR-001 findings.
- **Not a statistical formula**: it is a policy approximation, not a
  propagation of probability distributions. Code comments must not describe
  it as a statistical rule.

The rule applies to all arithmetic derivations: ratios, sums, differences,
products. It does not apply to:
- Pure unit conversions of a single Quantity (no new uncertainty introduced)
- Currency conversions where the exchange rate carries its own `confidence_tier`
  (apply the rule to the exchange rate `Quantity` and the input monetary `Quantity`)

All functions that derive `Quantity` outputs from `Quantity` inputs must
explicitly compute and pass `confidence_tier=min(...)` — no implicit defaulting.

---

### B-3: Replacement for § "Currency and Monetary Value Standards" — `MonetaryValue` type

Replace the current `MonetaryValue` dataclass with:

```python
@dataclass(kw_only=True)
class MonetaryValue(Quantity):
    """A Quantity that is specifically a monetary amount.

    Inherits from Quantity: value, unit, variable_type, observation_date,
    source_registry_id, confidence_tier.

    The inherited 'value' field is the amount (replaces the former 'amount'
    field). The inherited 'unit' field carries the currency unit at canonical
    storage (USD_2015) or at ingestion (source currency unit before conversion).
    'currency_code' is the ISO 4217 code of the source currency; it is
    redundant with 'unit' for canonical values but required at ingestion before
    conversion so the pipeline can construct the correct Unit.
    """
    currency_code: str               # ISO 4217, e.g. "USD", "EUR", "GHS"
    price_basis: PriceBasis
    exchange_rate_type: ExchangeRateType

class PriceBasis(Enum):
    NOMINAL = "nominal"              # current prices at observation date
    CONSTANT = "constant"            # real terms; base_year encoded in unit
    PPP = "ppp"                      # PPP-adjusted; base_year encoded in unit

class ExchangeRateType(Enum):
    OFFICIAL = "official"
    PARALLEL = "parallel"            # black market / unofficial rate
    PPP = "ppp"
    FIXED = "fixed"                  # pegged rate; document peg terms in metadata
```

**Breaking change from prior definition:** The `amount` field is removed.
Access the monetary amount via the inherited `value` field. The `confidence_tier`
field is inherited from `Quantity` and is required; it was present in the prior
`MonetaryValue` definition and the requirement is unchanged.

**Cross-reference:** `CODING_STANDARDS.md § Monetary and Quantity Standards`
governs usage rules. `DATA_STANDARDS.md` governs the type contract.

---

*End of Draft B.*

---

## QA Agent: CHALLENGE

*Reviewing Draft A and Draft B for testability, CI enforceability, and
boundary definition clarity. Flagging gaps that prevent confident
verification of each new rule.*

---

### Finding QA-1: No CI rule currently prevents `dict[str, float]` — BLOCKING

**Rule:** `SimulationEntity.attributes` must be `dict[str, Quantity]`.

**Testability gap:** The existing compliance scan (`ci.yml` § compliance-scan)
checks for bare `except`, ambiguous variable names, legacy typing imports, and
monetary float literals near monetary keywords. None of these checks catch a
`dict[str, float]` annotation on an entity attribute field. A module can today
write `entity.attributes["gdp"] = 44e9` and pass every CI check.

**What is needed before this standard can be enforced:**
A new `ruff` rule or a bespoke compliance script that detects:
1. `dict[str, float]` type annotations on attributes fields in
   `SimulationEntity` subclasses
2. Direct assignment of `float` or `Decimal` values into `entity.attributes`
   (e.g., `entity.attributes[key] = 1.46` without `Quantity()` construction)

The second check is harder — it requires type-flow analysis, which `ruff`
cannot do reliably. Recommend a pattern-based heuristic for the CI scan
plus a required integration test in each module that asserts
`isinstance(entity.attributes[key], Quantity)` for every key the module writes.

**Status: BLOCKING.** The standard cannot be declared enforced without a CI
mechanism that would catch violations. Implementing without the CI check
produces a standard that is aspirational, not contractual.

---

### Finding QA-2: `variable_type` semantic correctness cannot be machine-tested

**Rule:** Every `Quantity` must carry a semantically correct `variable_type`.

**Testability gap:** CI can verify that `variable_type` is non-null and is a
valid `VariableType` enum member. It cannot verify that GDP is classified as
FLOW rather than STOCK. Semantic misclassification passes all type checks.

**What is needed:** Each module that writes attributes must include a dedicated
unit test asserting the `variable_type` of each attribute key it owns:

```python
def test_macroeconomic_module_gdp_is_classified_as_flow():
    # GDP accumulates if misclassified as STOCK; this test is the guard.
    result = MacroeconomicModule().compute(mock_entity, mock_state, timestep)
    gdp_event = next(e for e in result if "gdp" in e.affected_attributes)
    assert gdp_event.affected_attributes["gdp"].variable_type == VariableType.FLOW
```

**Status: Non-blocking** (CI cannot enforce semantics; human test authorship is
the gate). Must be included in the testing requirements section of CODING_STANDARDS.md.
Recommend adding: "Each module must include one test per attribute key it writes,
asserting the expected `variable_type`."

---

### Finding QA-3: `confidence_tier` propagation needs explicit test coverage per derived function

**Rule:** `confidence_tier(output) = min(tier_a, tier_b)`.

**Testability:** Fully machine-testable. Every function that produces a derived
`Quantity` from multiple inputs must have a unit test with unequal input tiers,
asserting the output tier equals the minimum.

**What is needed:**
```python
def test_compute_debt_service_ratio_inherits_lower_tier():
    high_confidence_debt = Quantity(..., confidence_tier=1)
    low_confidence_revenue = Quantity(..., confidence_tier=4)
    result = compute_debt_service_ratio(high_confidence_debt, low_confidence_revenue)
    assert result.confidence_tier == 4  # lower-of-two

def test_compute_debt_service_ratio_handles_equal_tiers():
    debt = Quantity(..., confidence_tier=2)
    revenue = Quantity(..., confidence_tier=2)
    result = compute_debt_service_ratio(debt, revenue)
    assert result.confidence_tier == 2
```

**Status: Non-blocking** (testable; test authorship obligation is clear). The
testing requirement should be stated explicitly: "Every derived `Quantity`
function must have a tier propagation test with non-equal input tiers."

---

### Finding QA-4: "Ingestion boundary" is not spatially defined

**Rule:** After the ingestion boundary, no code in `backend/app/` introduces
bare floats or bare `Decimal` values as attribute values.

**Gap:** The standard prohibits bare values "after the ingestion boundary" but
does not define what constitutes the boundary in code. Is it a module? A
class? A function decorator? Without a concrete boundary, "after ingestion"
is un-enforceable.

**Recommendation:** Define the ingestion boundary as the output of a specific
interface: any class implementing `IngestionPipeline` (or equivalent protocol).
The protocol's return type must be `list[Quantity]` or `list[MonetaryValue]`.
Code outside `backend/app/data/ingestion/` that produces a raw `Decimal` as
an attribute value is a violation; code inside the ingestion module that
produces raw values before the final return is not.

**Status: Non-blocking** (implementation detail to be specified in the ADR
for the ingestion module). Should be resolved before the ingestion module
ADR is written.

---

### Finding QA-5: Compliance scan needs updating

**Existing scan:** Warns on monetary float literals near monetary keywords
but does not fail.

**New rules needed in `ci.yml` compliance-scan after this standard is adopted:**
1. Fail on `dict[str, float]` or `Dict[str, float]` in files under `backend/app/`
   (pattern: `attributes.*dict.*str.*float`)
2. Fail on `event.affected_attributes.*float` assignments
3. Extend COMPLIANCE-WARN to flag bare `Decimal(...)` constructions in attribute
   writes (not in temporary arithmetic variables)

**Status: Non-blocking** (CI update is implementation-phase work). Must be
tracked as a companion task to the implementation.

---

## Architect Agent: CHALLENGE

*Reviewing Draft A and Draft B for consistency with existing ADRs, structural
soundness of the proposed type relationships, and architectural boundary
conditions that the standards do not yet address.*

---

### Finding ARCH-1: ADR-001 renewal trigger fires — BLOCKING

**Trigger text (ADR-001 § Validity Context):**
> "Stock vs. flow variable distinction added to `DATA_STANDARDS.md §
> Units and Measurements` in ways that require structural changes to
> `SimulationEntity.attributes`"

**Analysis:** Draft B adds `VariableType` (with STOCK and FLOW members) to
`DATA_STANDARDS.md § Units and Measurements`, and changes
`SimulationEntity.attributes` from `dict[str, float]` to `dict[str, Quantity]`.
This is verbatim what the trigger describes. Both conditions are met.

Additionally, the second trigger also fires:
> "Data model unit standard changes in `DATA_STANDARDS.md` that affect
> attribute store design (e.g., stock vs. flow distinction added to `Quantity`)"

The parenthetical example is exactly the change SCR-001 proposes.

**Required action:** ADR-001 must transition CURRENT → UNDER-REVIEW before
implementation of this standards change proceeds. This is the Architecture
License Framework dependency rule — no implementation may proceed under an
ADR that should be UNDER-REVIEW but has not been transitioned.

The UNDER-REVIEW period for ADR-001 will require re-examining:
- Whether `dict[str, Quantity]` is the correct generic container or whether a
  typed `AttributeStore` class would be more robust
- How `variable_type` affects the propagation engine's apply-delta logic
- Whether Event deltas carry `variable_type` matching the target attribute
  (a FLOW delta applied to a STOCK attribute has different semantics)

**Status: BLOCKING.**

---

### Finding ARCH-2: ADR-002 renewal trigger fires — BLOCKING

**Trigger text (ADR-002 § Validity Context):**
> "Uncertainty quantification standard additions to `DATA_STANDARDS.md`
> that affect how events carry uncertainty (e.g., events required to carry
> confidence intervals alongside affected_attribute deltas)"

**Analysis:** Draft A mandates that `Event.affected_attributes` becomes
`dict[str, Quantity]`. A `Quantity` carries `confidence_tier`. This means
every event delta now carries a confidence tier. The trigger text references
"confidence intervals" while Draft A/B propose tiers (not intervals), but
the intent is identical: events now carry uncertainty metadata that they did
not before. The trigger fires.

**Required action:** ADR-002 must transition CURRENT → UNDER-REVIEW before
implementation proceeds. The UNDER-REVIEW period must examine:
- Whether `ControlInput.to_events()` outputs `Event` deltas as `Quantity`
  with appropriate `confidence_tier` assignments
- Whether `InputOrchestrator.inject()` has a type contract that reflects
  `dict[str, Quantity]` in the returned `list[Event]`
- The `ContingentInput.condition.threshold: float` field — if the threshold
  is being compared to a `Quantity`-valued attribute, is the comparison valid?

**Status: BLOCKING.**

---

### Finding ARCH-3: `MonetaryValue` as `Quantity` subclass — Python dataclass inheritance constraints

**Issue:** Python `dataclass` inheritance with `kw_only=True` requires that all
parent fields without defaults precede child fields. `Quantity` has five
required fields (no defaults): `value`, `unit`, `variable_type`,
`observation_date`, `source_registry_id`, `confidence_tier`. `MonetaryValue`
adds three: `currency_code`, `price_basis`, `exchange_rate_type`.

With `kw_only=True` on both classes this is handled — all arguments are
keyword-only and ordering is not constrained. Draft B specifies `kw_only=True`
on `Quantity`; the same must be explicit on `MonetaryValue`. This is a
implementation note, not a design flaw.

**Second issue:** The prior `MonetaryValue` had an `amount` field; the new
design replaces it with the inherited `value` field. Any existing code that
accesses `monetary_value.amount` will break. This is the expected consequence
of the structural change, but it must be a tracked migration task.

**Status: Non-blocking** (implementation constraint; resolved by `kw_only=True`
and migration tracking).

---

### Finding ARCH-4: `Relationship.weight` and `Relationship.attributes` scope unclear

**Issue:** Draft A mandates `dict[str, Quantity]` for entity attributes and
event deltas. `Relationship` has two analogous fields:
- `weight: float` — dimensionless propagation coefficient used in NumPy
  matrix operations
- `attributes: dict[str, float]` — relationship-specific data (trade volume,
  debt amount, etc.)

Draft A explicitly permits `float` for "NumPy propagation weights" with a
comment. `Relationship.weight` is exactly this — it must remain `float` for
NumPy compatibility. But `Relationship.attributes` may contain measured
quantities (e.g., bilateral trade volume in USD_2015, outstanding debt in
USD_2015) that should be `Quantity`.

**Recommendation:** `Relationship.weight: float` is explicitly permitted
(NumPy weight, not a measurement). `Relationship.attributes` should follow
the same `dict[str, Quantity]` rule as entity attributes for measured
quantities. Add this to Draft A's usage table.

**Status: Non-blocking** (clarification needed in Draft A, not a blocking
design gap).

---

### Finding ARCH-5: `variable_type` on Event deltas — propagation semantic gap

**Issue:** An Event delta is a change-to-be-applied to an attribute. If the
attribute is a STOCK and the delta is a FLOW-typed change, is that valid?

Example: an Event carries `affected_attributes["reserves"] = Quantity(-5e9, ...,
variable_type=FLOW)`. `reserves` is a STOCK. The delta is FLOW-typed because
it represents a change over a period. The propagation engine must add the
delta to the stock's current value. This is semantically coherent — but the
standard does not specify the rule for delta `variable_type` relative to the
target attribute's `variable_type`.

**Recommendation:** The standard should specify: "Event deltas for STOCK
attributes carry `variable_type=FLOW` (they are the flow that changes the
stock). Event deltas for FLOW and RATIO attributes carry the same type as the
attribute. The propagation engine applies `new_value = current + delta` for
STOCK targets and `new_value = delta` for FLOW targets (flows reset each
period)."

**Status: Non-blocking** (can be addressed in the ADR-001 renewal; flagged
here so it is not forgotten).

---

## Domain Council Spot Review

*Three domain intelligence agents reviewed Draft A and Draft B from their
respective frameworks. Activation mode: CHALLENGE.*

---

### Chief Methodologist: CHALLENGE

**Framework:** Statistical integrity, uncertainty quantification, mathematical
honesty of simulation outputs.

---

**Finding CM-1: Lower-of-two is statistically biased in a known direction — BLOCKING**

The lower-of-two `confidence_tier` rule is a policy approximation, not a
statistical formula. When two input sources are independent and corroborating,
their combination legitimately increases confidence beyond either alone. A Tier
2 GDP estimate corroborated by an independent Tier 2 fiscal data source is
more reliable than either alone — lower-of-two ignores this and assigns Tier 2,
which is the same as if no corroboration existed.

The direction of bias is systematic and known: the rule always overstates
uncertainty. This is defensible as a conservative policy choice — in a tool
used for high-stakes sovereign decisions, erring toward wider confidence bands
is the correct failure mode. But the standards document must explicitly state:

> *"The lower-of-two rule is a deliberately conservative policy approximation,
> not a statistical formula. It systematically overstates uncertainty when
> inputs are independent and mutually corroborating. This is the intended
> behavior: in a tool informing sovereign policy decisions, overstatement of
> uncertainty is the preferred failure mode. Code comments must not describe
> this rule as a statistical derivation."*

Without this statement, implementors may assume the rule has statistical
derivation and either: (a) resist it when they understand it is biased, or
(b) invoke it in statistical contexts where a proper formula should be used
instead.

**Status: BLOCKING.** The standard mandates a specific arithmetic rule with
potentially misleading interpretation. The rationale and its limitations must
be documented before the rule is mandated.

---

**Finding CM-2: STOCK/FLOW taxonomy is ambiguous for position variables with both interpretations**

Government debt is correctly classified as STOCK (balance sheet position).
But "change in government debt" (the primary deficit) is a FLOW. The standard
says STOCK for debt and FLOW for fiscal deficit — correct, but the relationship
between them is not stated.

The propagation engine presumably computes:
`debt[t+1] = debt[t] + fiscal_deficit[t]`

This is a STOCK updated by a FLOW delta — which is ARCH-5 above. The standard
should confirm this is the intended pattern and state the invariant: "A STOCK
attribute is updated each period by adding any FLOW events targeting it. A FLOW
attribute is reset each period and accumulated from FLOW events during the
period."

Without this invariant, two implementors building different modules will make
incompatible assumptions about how STOCK and FLOW interact at update time.

**Status: Non-blocking** (the gap is in the propagation engine specification,
not the Quantity type standard; add to ADR-001 renewal scope).

---

**Finding CM-3: Confidence tier propagation does not account for non-linear transformations**

For a ratio `A / B` where both A and B have relative errors `ε_A` and `ε_B`,
the resulting ratio has relative error approximately `√(ε_A² + ε_B²)` (for
small errors and independent sources). For two Tier 1 sources (low relative
error), the derived ratio is still Tier 1 by lower-of-two — which is correct
when the absolute errors are small. But for two Tier 3 sources (higher relative
error), compounding via a ratio produces worse-than-Tier-3 reliability, yet
lower-of-two assigns Tier 3.

**Assessment:** This is a known limitation of the lower-of-two approximation
and is acceptable given the documented conservative intent. The limitation
should be noted in the standards as a caveat: "For derived quantities involving
non-linear combinations of multiple uncertain inputs, lower-of-two may
understate the compound uncertainty. Review derived Tier 3 or lower outputs
for compounded non-linear uncertainty before presenting them to users."

**Status: Non-blocking** (known limitation of an acknowledged approximation;
documentation is the remedy).

---

### Development Economist: CHALLENGE

**Framework:** Human development capability approach; distributional outcomes;
human cost ledger (HCL) outputs.

---

**Finding DE-1: DIMENSIONLESS is the least-wrong classification for capability variables but requires a caveat**

The Human Cost Ledger produces capability outputs: health-adjusted life years,
literacy rates, school enrollment ratios, child mortality rates, freedom
indices. The standard classifies these as DIMENSIONLESS.

This is correct within the taxonomy — these are not stocks (they don't carry
over a balance), not flows (they're not period totals), not ratios in the
dimensional-analysis sense. DIMENSIONLESS is the right slot.

However, the classification risks implying that capability indicators are
*merely* dimensionless numbers — analogous to a propagation weight or a
dimensionless coefficient in a physics equation. Capability variables in the
Sen framework represent opportunity sets for human flourishing. They should be
treated with different epistemic weight than the HDI is an arbitrary composite.

**Recommendation:** Add to the standard's DIMENSIONLESS definition:
> *"DIMENSIONLESS includes all index and score variables regardless of their
> conceptual richness. The classification describes storage behavior, not
> the significance of the variable. A capability index (HDI dimension, child
> mortality rate) is DIMENSIONLESS by this taxonomy and also a primary output
> with equal display weight to financial indicators — the classification does
> not diminish this."*

**Status: Non-blocking** (clarification, not a blocking design gap).

---

**Finding DE-2: PPP encoding for `MonetaryValue` HCL outputs needs explicit unit guidance**

Draft B specifies that `MonetaryValue` inherits `unit: Unit` from `Quantity`.
The canonical internal unit is `USD_2015`. For HCL outputs that use PPP-adjusted
values (per `DATA_STANDARDS.md §PPP vs. Market Rate Assignment`), is the `unit`
field `USD_2015` regardless of `exchange_rate_type=PPP`? Or is there a
`USD_2015_PPP` unit distinct from `USD_2015` market-rate?

This matters because a PPP-adjusted GDP and a market-rate GDP with the same
`Decimal` value mean different things in cross-country comparison. Storing
both as `unit=USD_2015` while relying on `exchange_rate_type` to distinguish
them works only if every consuming function checks both fields.

**Recommendation:** Specify in Draft B: "For PPP-adjusted monetary values,
`unit=USD_2015_PPP` (a distinct `Unit` instance with the PPP annotation).
For market-rate values, `unit=USD_2015`. Do not use `exchange_rate_type` alone
to distinguish — the `unit` field must encode the conversion basis."

**Status: Non-blocking** (implementation detail; should be resolved in the
ingestion module ADR).

---

### Intergenerational Advocate: CHALLENGE

**Framework:** Long-run consequences; future generations; irreversible
thresholds; epistemic honesty about long-horizon projections.

---

**Finding IA-1: No time-horizon confidence degradation rule — BLOCKING**

The lower-of-two rule propagates confidence based on input source quality.
It does not account for time elapsed between observation and projection.

A Tier 1 GDP observation from 2023 produces a Tier 1 projection for 2053 under
the current rule. This is epistemic misrepresentation: a 30-year projection is
not Tier 1 data regardless of the quality of its historical anchor.

For HCL outputs especially — child mortality rates in 2040, capability deficits
in 2050 — presenting a Tier 1 confidence level on a multi-decade projection
falsely implies the precision of measurement where only the uncertainty of
long-run forecasting exists.

**Proposed rule:** Forward projections beyond a defined time horizon from the
`observation_date` automatically degrade `confidence_tier`:
- Projection ≤ 5 years from `observation_date`: no automatic degradation
- Projection 5–15 years: minimum tier of 3 (regardless of input tier)
- Projection > 15 years: minimum tier of 4

This rule applies in addition to lower-of-two — the output tier is the maximum
of `min(input_tiers)` and the horizon-based floor.

**Rationale:** The simulation is built for sovereign decision-making. A HCL
output showing Tier 1 confidence for a 30-year human capability projection
will be read as high-confidence. If a finance minister makes a decision based
on that reading, and the projection later proves wrong because structural breaks
occurred in year 8 (as they routinely do), the tool has contributed to the
harm it was built to prevent.

**Status: BLOCKING.** Before mandating confidence tier propagation rules,
the absence of time-horizon degradation must be documented as a known
limitation — and flagged as a required Milestone 2 addition. It is not
acceptable to mandate a confidence rule for a forward-projection tool that
does not degrade confidence with projection horizon.

---

**Finding IA-2: Display guidance for Tier 4 HCL outputs**

The lower-of-two rule correctly assigns Tier 4 to a derived quantity combining
Tier 1 historical data with Tier 4 projected inputs. Users see `confidence_tier=4`
on HCL outputs derived from such combinations. Is tier visibility sufficient,
or does Tier 4 on an HCL output require an explicit display warning?

**Recommendation:** Add to the display guidance in `DATA_STANDARDS.md §Output
Attribution`: "HCL outputs with `confidence_tier ≥ 4` must display an explicit
warning at the HCL panel level: 'One or more inputs to this human cost estimate
have low confidence. Treat this output as illustrative, not predictive.'" This
ensures the tier is not just a number in a tooltip but a visible signal.

**Status: Non-blocking** (display guidance; implementation-phase concern).

---

## Findings Summary

### BLOCKING Findings

These must be resolved or explicitly addressed before implementation proceeds.

| ID | Source | Finding |
|---|---|---|
| **QA-1** | QA Agent | No CI rule prevents `dict[str, float]` attribute stores — standard unenforceable without compliance scan update |
| **ARCH-1** | Architect Agent | ADR-001 renewal trigger fires — ADR-001 must move to UNDER-REVIEW before implementation |
| **ARCH-2** | Architect Agent | ADR-002 renewal trigger fires — ADR-002 must move to UNDER-REVIEW before implementation |
| **CM-1** | Chief Methodologist | Lower-of-two rule mandated without documenting its known statistical bias — misleading to implementors |
| **IA-1** | Intergenerational Advocate | No time-horizon confidence degradation rule — Tier 1 input produces Tier 1 label on 30-year projections |

### Non-Blocking Findings

Tracked for resolution at implementation phase or in the ADR renewal period.

| ID | Source | Finding |
|---|---|---|
| QA-2 | QA Agent | `variable_type` semantic correctness requires per-module per-attribute test coverage |
| QA-3 | QA Agent | Every derived Quantity function needs a tier propagation unit test with unequal input tiers |
| QA-4 | QA Agent | "Ingestion boundary" needs concrete spatial definition in the ingestion module ADR |
| QA-5 | QA Agent | Compliance scan needs new rules after this standard is adopted |
| ARCH-3 | Architect Agent | Python dataclass inheritance with `kw_only=True` — implementation constraint documented |
| ARCH-4 | Architect Agent | `Relationship.weight` and `Relationship.attributes` scope clarification needed in Draft A |
| ARCH-5 | Architect Agent | Delta `variable_type` relative to target attribute type — propagation semantic gap |
| CM-2 | Chief Methodologist | STOCK updated by FLOW delta invariant not stated in standard |
| CM-3 | Chief Methodologist | Non-linear compound uncertainty understated by lower-of-two for Tier 3 inputs |
| DE-1 | Development Economist | DIMENSIONLESS classification needs caveat for capability variables |
| DE-2 | Development Economist | PPP encoding for MonetaryValue HCL outputs needs explicit unit guidance |
| IA-2 | Intergenerational Advocate | Tier 4 HCL outputs need explicit display warning, not just tier indicator |

---

## Engineering Lead Disposition

*To be completed after Engineering Lead review of this document.*

Options for each BLOCKING finding:

**QA-1** (CI enforcement): Approve standard on condition that a companion
implementation issue for the compliance scan update is created and must close
before any module implementing the new attribute store merges.

**ARCH-1 and ARCH-2** (ADR renewal): Accept that both ADRs must be moved to
UNDER-REVIEW as part of the implementation PR — not a gate on the standards
change, but a gate on any implementation building on it. The standard can be
adopted; implementation is the gate.

**CM-1** (Lower-of-two rationale): Approve standard with addition of explicit
conservative-policy language to the rule. No design change needed — documentation
addition only.

**IA-1** (Time-horizon degradation): Two options:
- **Option A:** Adopt the lower-of-two rule for Milestone 2 as stated, with
  an explicit "Known Limitation" note that time-horizon degradation is not
  yet implemented and will be added in Milestone 3 alongside the scenario
  engine (which is the first milestone producing forward projections at scale).
- **Option B:** Add the time-horizon degradation rule to Draft A/B now, accepting
  that it is more complex but catching the problem before projections are built.

---

## Consequential Actions

Upon Engineering Lead approval (with any disposition decisions recorded above):

1. **Create GitHub Issues** for each BLOCKING finding (links to this document)
2. **Move ADR-001 and ADR-002 to UNDER-REVIEW** (License Status field update +
   Last Reviewed note) in a separate commit on the implementation branch
3. **Update Draft A and Draft B** with any changes from the disposition
4. **Open implementation PR** modifying `CODING_STANDARDS.md` and
   `DATA_STANDARDS.md` per the approved drafts
5. **Create companion compliance-scan update issue** (QA-1) — must close
   before any module implementing `dict[str, Quantity]` can merge
6. **Update scan registry** with SCR-001 entry after implementation merges

---

*Compiled by Engineering Lead session (Claude Sonnet 4.6), 2026-04-17.*
*This document is the output of the Material Standards Change Review Sequence
per `docs/MILESTONE_RUNBOOK.md`. No standards documents have been modified.
No code has been implemented. This review is complete; disposition is pending.*
